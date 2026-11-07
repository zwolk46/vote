"""c29: D3's #80 (2827d85): the fixes from M2's check of #73 (c24): Virginia's 2018 House of Delegates 8th district
back as a special, school superintendents typed as officers, REPORT section 15's count.

The orchestrator (2026-11-07 14:21 UTC): "#80, D3's fixes from your c24: VA HoD-8 is back, and 176 superintendents
are retyped. 1,720 p moved by at most x1.017, and MT 30093 moved x0.5."

What this does (every figure [measured] unless marked):
  29.1 the moves file (data/local/moves-fixes-c24.json) against my own diff of every local, primary and state
       legislative file between 1a6d752 (before) and 2827d85 (after): type changes, p changes, reason changes, the
       added record.
  29.2 the superintendents by my own reading of D3's words (SUPERINTENDENT, SUPT or SUPER. OF PUBLIC INSTRUCTION with
       SCHOOL, EDUCATION or INSTRUCTION in the office's words): count, by state and year, their type now; against
       176 (and c24's 167).
  29.3 Virginia's 2018 House of Delegates 8th district: the record in data/state-lower/2018/VA.json against the one
       #73 dropped (data/local/2018/VA.json at a2433b1).
  29.4 Montana county 30093's superintendent (x0.5) and the 30 largest of the 1,720 moves, recomputed from my own
       pools (c15's).
Own implementation; nothing from pipeline/ is imported.
"""
import collections
import glob
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

BEFORE, AFTER = "1a6d752", "2827d85"
PRE73 = "a2433b1"
MOVES = os.path.join(L.DATA, "local", "moves-fixes-c24.json")
SUPT = re.compile(r"SUPERINTENDENT|\bSUPT\b|SUPER\. OF PUBLIC INSTRUCTION")
SCHOOL = re.compile(r"SCHOOL|EDUCATION|INSTRUCTION")
OFFICER = "clerk, treasurer or other county officer"


def rel(a, b):
    return abs(a - b) / max(abs(a), abs(b), 1e-300)


def at(commit, path):
    r = subprocess.run(["git", "show", f"{commit}:{path}"], capture_output=True, text=True, cwd=L.ROOT)
    return json.loads(r.stdout) if r.returncode == 0 and r.stdout else None


def changed_files():
    r = subprocess.run(["git", "diff", "--name-only", BEFORE, AFTER, "--", "data/"], capture_output=True, text=True, cwd=L.ROOT)
    return [x for x in r.stdout.split("\n") if x]


def pval(c):
    return (c.get("p") or {}).get("value")


def reason(c):
    return (c.get("p") or {}).get("not_computed")


# ---------------------------------------------------------------------------------------------- 29.1
def section_1(moves):
    print("### 29.1 the moves file against my diff of the contest files")
    rows = moves["contests"]
    cols = moves["columns"]
    print(f"  moves file: {len(rows)} rows, columns {cols}; counts {moves['counts']}")
    why = collections.Counter(r[6] for r in rows)
    print(f"  rows by why: {dict(why)}")
    mine = {}
    added = []
    for path in changed_files():
        if not re.search(r"data/(local|primary|state-lower|state-upper)/\d{4}/[A-Z]{2}\.json$", path):
            continue
        b, a = at(BEFORE, path), at(AFTER, path)
        bb = {c["id"]: c for c in (b or {}).get("contests", [])}
        aa = {c["id"]: c for c in (a or {}).get("contests", [])}
        for i in set(bb) | set(aa):
            cb, ca = bb.get(i), aa.get(i)
            if cb is None:
                added.append((path, i))
                continue
            if ca is None:
                mine[i] = ("removed", None, None, None, None)
                continue
            tb, ta = cb.get("office_type"), ca.get("office_type")
            pb, pa = pval(cb), pval(ca)
            rb, ra = reason(cb), reason(ca)
            kinds = []
            if tb != ta:
                kinds.append("T")
            if (pb is None) != (pa is None) or (pb is not None and pa is not None and rel(pb, pa) > 1e-12):
                kinds.append("P")
            if pa is None and pb is None and rb != ra:
                kinds.append("R")
            if kinds:
                mine[i] = ("+".join(kinds), tb, ta, pb, pa)
    print(f"  my diff: {len(mine)} contests changed in type, p or reason; added {added}; removed {sum(1 for v in mine.values() if v[0] == 'removed')}")
    ids = {r[0]: r for r in rows}
    print(f"  in both {len(set(mine) & set(ids))}; in my diff only {sorted(set(mine) - set(ids))[:5] or 'none'}; in the moves file only "
          f"{sorted(set(ids) - set(mine))[:5] or 'none'} (the added row: {[r[0] for r in rows if r[6] == 'added']})")
    agree = collections.Counter()
    for i, (kind, tb, ta, pb, pa) in mine.items():
        r = ids.get(i)
        if not r:
            continue
        same = (r[6] == kind and r[2] == tb and r[3] == ta and ((r[4] is None and pb is None) or (r[4] is not None and pb is not None and rel(r[4], pb) <= 1e-9))
                and ((r[5] is None and pa is None) or (r[5] is not None and pa is not None and rel(r[5], pa) <= 1e-9)))
        agree["equal (why, types, p before and after)" if same else f"differs: file {r[6]} {r[2]}->{r[3]}, mine {kind} {tb}->{ta}"] += 1
    print(f"  row by row: {dict(agree)}")
    # the moves rows my diff does not show: what differs in their p block between the two commits
    only = sorted(set(ids) - set(mine))
    keys = collections.Counter()
    same_p = 0
    cache = {}
    for i in only:
        r = ids[i]
        if r[6] == "added":
            continue
        if r[4] is not None and r[5] is not None and rel(r[4], r[5]) <= 1e-12:
            same_p += 1
        y, st = i[:4], i.split("-")[2]
        lv = i.split("-")[1]
        path = f"data/{lv}/{y}/{st}.json"
        if path not in cache:
            cache[path] = ({c["id"]: c for c in (at(BEFORE, path) or {}).get("contests", [])},
                           {c["id"]: c for c in (at(AFTER, path) or {}).get("contests", [])})
        bb, aa = cache[path]
        pb, pa = (bb.get(i) or {}).get("p") or {}, (aa.get(i) or {}).get("p") or {}
        diff = tuple(sorted(k for k in set(pb) | set(pa) if pb.get(k) != pa.get(k)))
        keys[diff] += 1
    print(f"  the {len(only)} rows in the moves file only: p_before equals p_after in {same_p}; what differs in their p block "
          f"between {BEFORE} and {AFTER}: {dict(keys)}")
    P = [r for r in rows if r[6] in ("P", "T+P")]
    print(f"  P rows: {len(P)}; p value moved in {sum(1 for r in P if r[4] and r[5] and rel(r[4], r[5]) > 1e-12)}, unchanged in {sum(1 for r in P if r[4] is not None and r[5] is not None and rel(r[4], r[5]) <= 1e-12)}")
    rat = sorted(r[5] / r[4] for r in P if r[4] and r[5] and rel(r[4], r[5]) > 1e-12)
    print(f"  the P rows whose p moved: {len(rat)}; ratios {rat[0]:.4f} to {rat[-1]:.4f} (D3: 1,720 moved by at most x1.017); beyond 2% {sum(1 for x in rat if abs(x - 1) > 0.02)}")
    return mine


# ---------------------------------------------------------------------------------------------- 29.2
def section_2(moves):
    print("### 29.2 the superintendents by my own reading of D3's words")
    found = []
    for level in ("local", "primary"):
        for path in sorted(glob.glob(os.path.join(L.DATA, level, "[0-9]*", "*.json"))):
            d = L.load_json(path)
            for c in d["contests"]:
                words = " ".join(str(c.get("office_as_filed") or c.get("office") or "").upper().split())
                if SUPT.search(words) and SCHOOL.search(words):
                    found.append((c["id"], c.get("state") or d.get("state"), d["year"], c.get("office_type"), c.get("office_scope"), words, level))
    print(f"  {len(found)} contests whose office names a superintendent with school, education or instruction (D3: 176; c24: 167 with 'SUPERINTENDENT' alone)")
    print(f"  by level {dict(collections.Counter(f[6] for f in found))}; by type now {dict(collections.Counter(f[3] for f in found))}; scope {dict(collections.Counter(f[4] for f in found))}")
    print(f"  by state {dict(collections.Counter(f[1] for f in found).most_common())}; by year {dict(sorted(collections.Counter(f[2] for f in found).items()))}")
    print(f"  D3: AL 61, MT 47, FL 30, AZ 17, IL 16, GA 2, SC 2, NC 1; 2018 64, 2020 47, 2022 2, 2024 62, 2000 1")
    still = [f for f in found if f[3] == "school board"]
    print(f"  still typed school board: {len(still)} {[f[0] for f in still][:5]}")
    T = {r[0] for r in moves["contests"] if r[6] in ("T", "T+P")}
    print(f"  the moves file's T rows: {len(T)}; of my {len(found)}: in T {len(T & {f[0] for f in found})}, not in T {sorted({f[0] for f in found} - T)[:5] or 'none'}; T not in mine {sorted(T - {f[0] for f in found})[:5] or 'none'}")
    not_t = sorted({f[0] for f in found} - T)
    tb = collections.Counter()
    cache = {}
    for i in not_t:
        lv, y, st = i.split("-")[1], i[:4], i.split("-")[2]
        path = f"data/{lv}/{y}/{st}.json"
        if path not in cache:
            cache[path] = {c["id"]: c for c in (at(BEFORE, path) or {}).get("contests", [])}
        tb[(cache[path].get(i) or {}).get("office_type")] += 1
    print(f"  the {len(not_t)} not in T: their type at {BEFORE} {dict(tb)} (already officers: no move to list); by state "
          f"{dict(collections.Counter(i.split('-')[2] for i in not_t))}")
    sw = [f for f in found if f[4] == "state"]
    print(f"  statewide offices among them (D3: four): {len(sw)} {[f[0] for f in sw]}")


# ---------------------------------------------------------------------------------------------- 29.3
def section_3():
    print("### 29.3 Virginia's 2018 House of Delegates 8th district")
    new = L.load_json(os.path.join(L.DATA, "state-lower", "2018", "VA.json"))
    old = at(PRE73, "data/local/2018/VA.json") or {}
    cn = [c for c in new["contests"] if "DELEGATES" in str(c.get("office_as_filed") or c.get("office") or "").upper() or "8" in str(c.get("district"))]
    co = [c for c in old.get("contests", []) if "DELEGATES" in str(c.get("office_as_filed") or c.get("office") or "").upper()]
    print(f"  new file: {len(new['contests'])} contests; candidates for the special {[c['id'] for c in cn]}; the old local file at {PRE73}: {[c['id'] for c in co]}")
    if cn and co:
        a, b = cn[0], co[0]
        same = {k: (a.get(k) == b.get(k)) for k in ("office_as_filed", "office")}
        ca = [(x["name"], x.get("party"), x["votes"]) for x in a["result"]["candidates"]]
        cb = [(x["name"], x.get("party"), x["votes"]) for x in b["result"]["candidates"]]
        print(f"  election {a.get('election')!r} (old {b.get('election')!r}); district {a.get('district')!r}; special {a.get('special')}; office_as_filed {a.get('office_as_filed')!r} ({same})")
        print(f"  candidates new {ca}; old {cb}; {'equal' if ca == cb else 'DIFFER'}; total {a['result'].get('total_votes')} vs {b['result'].get('total_votes')}; "
              f"counties {sorted((a.get('place') or {}).get('counties') or a.get('counties') or [])} vs {sorted((b.get('place') or {}).get('counties') or b.get('counties') or [])}")
        print(f"  p: {(a.get('p') or {})}")


# ---------------------------------------------------------------------------------------------- 29.4
def section_4(moves):
    print("### 29.4 Montana 30093's superintendent and the 30 largest moves, recomputed from my own pools (c15)")
    rows = D.rows("local")
    by_id = {r["id"]: r for r in rows}
    medsl, nc, miss = C15.local_pools()
    tp = [r for r in moves["contests"] if r[6] == "T+P"]
    big = sorted((r for r in moves["contests"] if r[6] == "P" and r[4] and r[5]), key=lambda r: -abs(math.log(r[5] / r[4])))[:30]
    for r in tp:
        c = by_id.get(r[0])
        print(f"  {r[0]}: {r[1]!r}; type {r[2]} -> {r[3]}; p {r[4]} -> {r[5]} (x{r[5] / r[4]:.3f}); class now {c['cls'] if c else None}, N {c['N'] if c else None}, in window {c['kin'] if c else None}")
        # the class before, at BEFORE
        y = r[0][:4]
        st = r[0].split("-")[2]
        b = at(BEFORE, f"data/local/{y}/{st}.json")
        cb = next((x for x in (b or {}).get("contests", []) if x["id"] == r[0]), None)
        if cb:
            fc = (cb.get("forecasts") or [{}])[-1]
            print(f"    before: class {fc.get('class')!r}, like races {fc.get('like_races') or fc.get('N')}, in window {fc.get('in_window')}, q {fc.get('q')}")
    sample = [by_id[r[0]] for r in tp + big if r[0] in by_id and by_id[r[0]].get("route") == "class"]
    print(f"  recomputing {len(sample)} contests (the T+P row and the 30 largest P moves, those on the like-race route):")
    bad = C15.compare_like(sample, medsl, "MEDSL route")
    print(f"  mismatches: {len(bad) if bad is not None else 'see above'}")
    print("  the 30 largest P moves: " + "; ".join(f"{r[0].split('-', 3)[-1][:28]} x{r[5] / r[4]:.4f}" for r in big[:8]) + " ...")


def main():
    print(f"c29: #80 (D3's fixes from c24); HEAD {L.git_head()}; before {BEFORE}, after {AFTER}")
    moves = L.load_json(MOVES)
    section_1(moves)
    section_2(moves)
    section_3()
    section_4(moves)


if __name__ == "__main__":
    main()
