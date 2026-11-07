"""C24 (third pass, item 5: D3's #73, office types read by the office; the orchestrator's relay of 12:34 UTC). The
office type of every local and primary record is now read from the office's words with the place's name taken off,
state short forms and the seat's district (pipeline/local_medsl.py office_type; read, not imported). Checked: the moves
file (data/local/moves-office-types.json, 13,390 rows) against my own diff of every contest between main before #73
(a2433b1) and #73 (7fd4565), so that every p that changed is accounted for; the orchestrator's count of 141 p gone by id
against the file's 103; a sample of the largest moves recomputed from my own pools (c15), the 136 newly computed p and
the 103 no longer computed; the 115 legislative contests that left data/local (Rhode Island 2022, Virginia 2018, Arizona
2022): where they went and whether the legislature's route holds them; the two Rhode Island 2024 state senate p that
moved; and the twenty most common names of each type (office-types-top20.json) read for misfiled offices.
Own implementation; nothing from pipeline/ is imported. [measured] throughout; the record's own figures [stated].
"""
import collections
import json
import math
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402
import m2d3 as D  # noqa: E402
import c15_d3_refit as C15  # noqa: E402
import c23_nc_rounds_by_place as C23  # noqa: E402

BEFORE, AFTER = "a2433b1", "7fd4565"
C75 = "de31d9b"
LEVELS = ("local", "primary", "measure", "state-lower", "state-upper")
LEG_NAMES = {"REPRESENTATIVE IN GENERAL ASSEMBLY": "lower", "SENATOR IN GENERAL ASSEMBLY": "upper", "HOUSE OF DELEGATES": "lower",
             "STATE REPRESENTATIVE": "lower", "STATE SENATOR": "upper"}


def h1(s):
    print("\n" + s)


def at(commit, path):
    r = subprocess.run(["git", "show", f"{commit}:{path}"], capture_output=True, text=True, cwd=L.ROOT)
    return json.loads(r.stdout) if r.returncode == 0 else None


def changed(a, b, path="data/"):
    return subprocess.run(["git", "diff", "--name-only", a, b, "--", path], capture_output=True, text=True, cwd=L.ROOT).stdout.split()


def contest_files(a, b):
    return [f for f in changed(a, b) if f.endswith(".json") and len(f.split("/")) == 4 and f.split("/")[1] in LEVELS]


def pval(c):
    return (c.get("p") or {}).get("value")


def class_of(c):
    p = c.get("p") or {}
    m = re.search(r"for the class '([^']*)'", p.get("not_computed") or "")
    return p.get("class") or (m.group(1) if m else None)


# ------------------------------------------------------------------------------------------------ 24.1 the moves file
def section_1():
    h1("24.1 The moves file against my own diff of every contest between main before #73 and #73")
    mv = L.load_json(os.path.join(L.DATA, "local", "moves-office-types.json"))
    print(f"  the file: before {mv['before_commit']}, after code {mv['after_code_commits']}; columns {mv['columns']}; counts {json.dumps(mv['counts'])[:700]}")
    rows = {r[0]: r for r in mv["contests"]}
    print(f"  rows {len(rows)} ({len(mv['contests'])} listed); kinds {dict(collections.Counter(r[6] for r in mv['contests']))}")
    files = contest_files(BEFORE, AFTER)
    print(f"  contest files changed: {len(files)} {dict(collections.Counter(f.split('/')[1] for f in files))}")
    before, after = {}, {}
    for f in files:
        for c in (at(BEFORE, f) or {"contests": []})["contests"]:
            before[c["id"]] = c
        for c in (at(AFTER, f) or {"contests": []})["contests"]:
            after[c["id"]] = c
    kinds, bad, pairs, ratios = collections.Counter(), [], collections.Counter(), []
    removed_with_p, gone = [], []
    for i in set(before) | set(after):
        lv = i.split("-")[1]
        b, a = before.get(i), after.get(i)
        if b is None:
            k = "added"
        elif a is None:
            k = "removed"
            if pval(b) is not None:
                removed_with_p.append(i)
        else:
            pb, pa = pval(b), pval(a)
            tc = b.get("office_type") != a.get("office_type")
            if pb is not None and pa is not None and abs(pb - pa) > 1e-12 * max(abs(pb), abs(pa)):
                k = "T+P" if tc else "P"
                if pb:
                    ratios.append((pa / pb, i))
            elif pb is None and pa is not None:
                k = "N"
            elif pb is not None and pa is None:
                k = "X"
                gone.append(i)
            elif tc:
                k = "T"
            else:
                k = None
            if tc:
                pairs[(b.get("office_type"), a.get("office_type"))] += 1
        if k is None:
            if i in rows:
                bad.append((i, "listed, but neither type nor p changed", rows[i][6]))
            continue
        kinds[(lv, k)] += 1
        r = rows.get(i)
        if r is None:
            bad.append((i, k, "not listed"))
            continue
        if r[6] != k:
            bad.append((i, k, r[6]))
            continue
        if b is not None and a is not None:
            if r[2] != b.get("office_type") or r[3] != a.get("office_type"):
                bad.append((i, "types", r[2:4], b.get("office_type"), a.get("office_type")))
            for want, have in ((r[4], pval(b)), (r[5], pval(a))):
                if (want is None) != (have is None) or (want is not None and abs(want - have) > 1e-9 * max(abs(have), 1e-300)):
                    bad.append((i, "p", r[4:6], pval(b), pval(a)))
    print("  my diff: " + "; ".join(f"{lv} {k} {v}" for (lv, k), v in sorted(kinds.items())))
    print(f"  rows disagreeing with my diff (kind, types or p): {len(bad)} {bad[:6]}; every change is a row and every row a change: {'yes' if not bad and sum(kinds.values()) == len(rows) else 'NO'} ({sum(kinds.values())} vs {len(rows)})")
    rs = sorted(x for x, _ in ratios)
    print(f"  p moved (P and T+P): {len(rs)}; ratio after/before min {rs[0]:.3f}, median {rs[len(rs) // 2]:.3f}, 90% within {max(rs[int(0.05 * len(rs))], 1 / rs[int(0.05 * len(rs))]):.3f} and {rs[int(0.95 * len(rs))]:.3f}, max {rs[-1]:.3f}; "
          f"by more than x2 or under x1/2: {sum(1 for x in rs if x > 2 or x < 0.5)} (record: median 1.12, 90% within 1.26, largest 2.46, 8 over 2)")
    print(f"  p gone by id: {len(gone)} X (p no longer computed) + {len(removed_with_p)} removed records that had p = {len(gone) + len(removed_with_p)} "
          f"(the orchestrator counted 141 against the file's 103); the removed with p: " + ", ".join(f"{k} {v}" for k, v in collections.Counter(i[:4] + ' ' + i.split('-')[2] + (' question' if 'QUESTION' in i else ' legislature') for i in removed_with_p).items()))
    rem = [i for i in before if i not in after]
    print(f"  removed records {len(rem)}: " + ", ".join(f"{k} {v}" for k, v in sorted(collections.Counter(i[:4] + ' ' + i.split('-')[2] + ' ' + ('legislature' if any(x in i for x in ('GENERAL_ASSEMBLY', 'HOUSE_OF_DELEGATES', 'STATE_REPRESENTATIVE')) else 'straight party' if 'STRAIGHT' in i else 'question') for i in rem).items()))
          + f"; added {sum(1 for i in after if i not in before)} ({dict(collections.Counter(i.split('-')[1] for i in after if i not in before))})")
    xs = [after[i] for i in gone]
    print(f"  the 103 no longer computed, by reason: {dict(collections.Counter((x['p'].get('not_computed') or '')[:60] for x in xs))}; by year, state and type after: "
          + ", ".join(f"{k[0]} {k[1]} {k[2]} {v}" for k, v in collections.Counter((x['id'][:4], x['id'].split('-')[2], x.get('office_type')) for x in xs).most_common(9))
          + f"; school boards among them {sum(1 for x in xs if x.get('office_type') == 'school board')}, North Carolina's 2023 school boards {sum(1 for x in xs if x['id'].startswith('2023-local-NC') and x.get('office_type') == 'school board')} (D3's REPORT 15: '69 of these are North Carolina's 2023 school boards')")
    print("  type changes, the eight largest: " + "; ".join(f"{a} -> {b}: {v:,}" for (a, b), v in pairs.most_common(8)) + f"; records whose type changed {sum(pairs.values()):,} (record 7,638)")
    return rows, before, after, ratios


# --------------------------------------------------------------------------------------- 24.2 the largest moves, recomputed
def section_2(rows, ratios):
    h1("24.2 The largest moves, the 136 newly computed and the 103 no longer computed, from my own pools (2023 left out, as the record stood at #73)")
    feed = {r[0] for r in L.load_json(os.path.join(L.DATA, "local", "moves-2023-feed.json"))["contests"]}
    big = sorted(ratios, key=lambda x: -abs(math.log(x[0])))
    top = [i for x, i in big[:40]] + [i for x, i in big[40:] if x > 2 or x < 0.5]
    skip = [i for i in top if i in feed]
    top = [i for i in top if i not in feed]
    print(f"  the sample: the 40 largest moves by |log ratio| and every move beyond x2, less {len(skip)} moved again by #75 (checked in c26): {len(top)}; ratios {min(x for x, i in big if i in top):.3f} to {max(x for x, i in big if i in top):.3f}")
    medsl, nc, miss = C15.local_pools(odd_la=False)
    nc_pool = [row for row in nc if row[0] >= C15.NC_FIRST]
    allrows = C23.nc_rows()
    prim_pool = C23.primary_pool(allrows)
    loc = {r["id"]: r for r in D.rows("local")}
    pri = {r["id"]: r for r in D.rows("primary")}
    def recompute(ids, label):
        lrows = [loc[i] for i in ids if i in loc and loc[i]["status"] == "value" and loc[i]["route"] in ("class", "boundary")]
        prows = [pri[i] for i in ids if i in pri and pri[i]["status"] == "value" and pri[i]["route"] == "class"]
        cm = [r for r in lrows if C15.medsl_route(r)]
        cn = [r for r in lrows if not C15.medsl_route(r)]
        if cm:
            C15.compare_like(cm, medsl, f"{label}: {len(cm)} local on MEDSL's route")
        if cn:
            C15.compare_like(cn, nc_pool, f"{label}: {len(cn)} local on the State Board's route")
        if prows:
            C15.compare_like(prows, prim_pool, f"{label}: {len(prows)} primaries")
        worst, n = 0.0, 0
        for r in lrows + prows:
            pool = medsl if r["level"] == "local" and C15.medsl_route(r) else nc_pool if r["level"] == "local" else prim_pool
            f, N, h, k = D.class_density([s for y, key, s in pool if key == r["cls"] and y < r["year"]])
            if f is None:
                continue
            pm, meth, fh = D.p_auto(r["p"]["n"], 0.5, D.sd_eq(f))
            worst = max(worst, D.rel(pm, r["p"]["value"]))
            n += 1
        print(f"    p recomputed from my (N, k, h) for {n}: worst relative difference {worst:.1e}; today's status of the ids {dict(collections.Counter((loc.get(i) or pri.get(i) or {}).get('status', 'not in the files') for i in ids))}")
    recompute(top, "the largest moves")
    new = [i for i, r in rows.items() if r[6] == "N" and i not in feed]
    recompute(new, f"the newly computed ({len(new)} of 136, less those #75 moved)")
    xs = [i for i, r in rows.items() if r[6] == "X"]
    few, many, nocls = 0, [], 0
    for i in xs:
        r = loc.get(i) or pri.get(i)
        if r is None:
            continue
        cls = re.search(r"for the class '([^']*)'", r["reason"] or "")
        if not cls:
            nocls += 1
            continue
        pool = medsl if r["level"] == "local" and C15.medsl_route(r) else nc_pool if r["level"] == "local" else prim_pool
        n = sum(1 for y, key, s in pool if key == cls.group(1) and y < r["year"])
        if n < D.MIN_CLASS:
            few += 1
        else:
            many.append((i, cls.group(1), n))
    print(f"  the 103 no longer computed: my pool holds fewer than 100 earlier like races of their class for {few}; 100 or more for {len(many)} {many[:3]}; no class in the reason {nocls}")


# ------------------------------------------------------------------------------- 24.3 the 115 legislative contests
def major(p):
    p = (p or "").upper()
    return "D" if p in ("D", "DEM", "DEMOCRAT", "DEMOCRATIC") else "R" if p in ("R", "REP", "REPUBLICAN") else None


def section_3(before, after):
    h1("24.3 The 115 legislative contests filed as local: where they went, and the legislature's route")
    leg = [c for i, c in before.items() if i.split("-")[1] == "local" and (c.get("office") or "").upper() in LEG_NAMES and not c.get("question")]
    print(f"  before #73, local records whose office names a legislature: {len(leg)} " + str(dict(collections.Counter((c['id'][:4], c['place']['state'], (c.get('office') or '').upper()) for c in leg)))
          + f"; still in data/local after #73: {sum(1 for c in leg if c['id'] in after)}; with p before: {sum(1 for c in leg if pval(c) is not None)}")
    st_files = [f for f in changed(BEFORE, AFTER, "data/state-lower/") + changed(BEFORE, AFTER, "data/state-upper/")]
    print(f"  state files #73 changed: {st_files}")
    # Rhode Island 2022 against the state files (Klarner's), district by district
    tal = collections.Counter()
    for c in leg:
        y, st = int(c["id"][:4]), c["place"]["state"]
        ch = "state-" + LEG_NAMES[(c.get("office") or "").upper()]
        path = f"data/{ch}/{y}/{st}.json"
        d = at(AFTER, path)
        if d is None:
            tal[(st, y, ch, "no state file of the year")] += 1
            continue
        dist = str(c["place"].get("district") or "").lstrip("0")
        hits = [x for x in d["contests"] if str(x["place"].get("district") or "").lstrip("0") == dist]
        if len(hits) != 1:
            tal[(st, y, ch, f"{len(hits)} contests of the district in the state file")] += 1
            continue
        x = hits[0]
        mine = {s: sum(a["votes"] or 0 for a in c["result"]["candidates"] if major(a.get("party")) == s) for s in "DR"}
        theirs = {s: sum(a["votes"] or 0 for a in x["result"]["candidates"] if major(a.get("party")) == s) for s in "DR"}
        same = mine == theirs
        wb = {a["name"].upper() for a in c["result"]["candidates"] if a.get("won")}
        tal[(st, y, ch, "D and R votes identical" if same else f"votes differ", "state p " + ("computed" if pval(x) is not None else "not computed"), x["result"].get("source") if isinstance(x["result"].get("source"), str) else "?")] += 1
    print("  each against the state file's contest of its district (the legislature's record, unchanged by #73): " + "; ".join(f"{k} {v}" for k, v in sorted(tal.items(), key=str)))
    for f, by in (("data/local/check-2022-medsl-klarner.json", ("RI", "AZ")), ("data/local/check-2018-medsl-klarner.json", ("VA", "NC"))):
        b, a = at(BEFORE, f), at(AFTER, f)
        print(f"  {f.split('/')[-1]}: tallies before {json.dumps(b['tallies'])[:200]}")
        print(f"     after  {json.dumps(a['tallies'])[:200]}; by state " + "; ".join(f"{s} before {b['by_state'].get(s)} after {a['by_state'].get(s)}" for s in by))
    # the two Rhode Island 2024 state senate p
    h1("  the two Rhode Island 2024 state senate p that moved")
    b, a = at(BEFORE, "data/state-upper/2024/RI.json"), at(AFTER, "data/state-upper/2024/RI.json")
    bi = {c["id"]: c for c in b["contests"]}
    ri22 = {a_["name"].upper(): c["id"] for i, c in before.items() if i.startswith("2022-local-RI-SENATOR") for a_ in c["result"]["candidates"] if a_.get("won")}
    kl22 = {a_["name"].upper() for c in (at(AFTER, "data/state-upper/2022/RI.json") or {"contests": []})["contests"] for a_ in c["result"]["candidates"]}
    moved = 0
    for c in a["contests"]:
        x = bi.get(c["id"])
        if x is None or pval(c) == pval(x):
            continue
        moved += 1
        fb, fa = (x.get("forecasts") or [{}])[0].get("share", {}), (c.get("forecasts") or [{}])[0].get("share", {})
        ib, ia = (x.get("forecast_inputs") or {}), (c.get("forecast_inputs") or {})
        pm, meth, fh = D.p_auto(c["p"]["n"], fa.get("mean"), fa.get("sd"))
        won = [a_["name"] for a_ in c["result"]["candidates"] if a_.get("won")]
        print(f"    {c['id']}: p {pval(x):.6g} -> {pval(c):.6g} (x{pval(c) / pval(x):.3f}); inputs before {ib} after {ia}; mean {fb.get('mean')} -> {fa.get('mean')} (sd {fa.get('sd')}); "
              f"p from the recorded mean and sd {pm:.6g} ({meth}, rel {D.rel(pm, pval(c)):.1e}); the winner {won} is a 2022 senate winner in MEDSL's file: {[w.upper() in ri22 for w in won]}, named so in Klarner's 2022 file: {[w.upper() in kl22 for w in won]}")
    print(f"    contests whose p moved {moved}; the 2022 senate names in Klarner's file for these: " + ", ".join(n for n in kl22 if "SOSNOWSKI" in n or "CRUZ" in n))


# ----------------------------------------------------------------------------- 24.4 the twenty names of each type
def section_4(after):
    h1("24.4 The twenty most common names of each type (office-types-top20.json), recounted and read for misfiled offices")
    rec = L.load_json(os.path.join(L.DATA, "local", "office-types-top20.json"))["types"]
    mine = collections.defaultdict(collections.Counter)
    for lv in ("local", "primary"):
        for path in sorted(D.level_files(lv)):
            d = L.load_json(path)
            for c in d["contests"]:   # as pipeline/office_types_audit.py counts (read, not imported): the name as filed, the states' offices and the legislature's primaries out
                if not c.get("office_type") or c.get("office_scope") == "state":
                    continue
                o = " ".join((c.get("office_as_filed") or c.get("office") or "").upper().split())
                if o in ("STATE-LOWER", "STATE-UPPER"):
                    continue
                mine[c["office_type"]][o] += 1
    eq = 0
    for t, v in rec.items():
        top = sorted(mine[t].items(), key=lambda x: (-x[1], x[0]))[:20]   # the audit's order: count, then name
        same = top == [(n.upper(), k) for n, k in v["top"][:20]] and sum(mine[t].values()) == v["contests"] and len(mine[t]) == v["names"]
        eq += same
        if not same:
            print(f"    {t}: mine {sum(mine[t].values())} contests, {len(mine[t])} names (record {v['contests']}, {v['names']}); top differs at " + str([(a, b) for a, b in zip(top, [(n.upper(), k) for n, k in v['top'][:20]]) if a != b][:2]))
    print(f"  types {len(rec)}; my recount over data/local and data/primary equal in contests, names and the twenty (name and count) for {eq}")
    # my reading
    sup = [c for lv in ("local", "primary") for path in D.level_files(lv) for c in L.load_json(path)["contests"] if "SUPERINTENDENT" in (c.get("office") or "").upper() and c.get("office_scope") != "state"]
    print(f"  my reading of the twenty: a school superintendent (an executive, one seat) is read as 'school board' (a body): {len(sup)} contests named superintendent, types {dict(collections.Counter(c.get('office_type') for c in sup))}, "
          f"with p computed {sum(1 for c in sup if pval(c) is not None)}; names {dict(collections.Counter(' '.join((c.get('office') or '').upper().split()) for c in sup).most_common(4))}")
    for t, names in (("sheriff or constable", ("JAILER",)), ("prosecutor", ("ATTORNEY", "ATTORNEY GENERAL", "CITY ATTORNEY")), ("council, commission or board", ("COUNTY AGRICULTURAL EXTENSION COUNCIL", "SINGLE MEMBER DISTRICT")),
                     ("other local office", ("LIEUTENANT GOVERNOR", "SECRETARY OF STATE")), ("judge", ("CHANCERY COURT", "COUNTY COURT"))):
        print(f"    {t}: " + "; ".join(f"'{n}' {mine[t].get(n, 0)}" for n in names))


def main():
    print("C24. D3's #73: OFFICE TYPES READ BY THE OFFICE: THE MOVES FILE, THE 141 GONE, THE LARGEST MOVES RECOMPUTED, THE 115 LEGISLATIVE CONTESTS, THE TWENTY NAMES")
    print(f"repository HEAD {L.git_head()}")
    rows, before, after, ratios = section_1()
    section_2(rows, ratios)
    section_3(before, after)
    section_4(after)


if __name__ == "__main__":
    main()
