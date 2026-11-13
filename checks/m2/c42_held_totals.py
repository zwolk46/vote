"""C42 (eighth pass; the orchestrator's words of 2026-11-12 23:11 UTC: "First, #96 and #97 ... Send me two things at once if
they come up: any p that moves more than 2x, and any record whose count fails a test"). #97 (main 9118755 -> 2ea7c2e): D3's
held-totals step (data/local/REPORT.md section 31; the orders of 2026-11-07 17:44, 18:49, 20:28, 20:30, 20:55, 21:03 and
21:21), every move listed in data/local/moves-held-totals.json, its tests in data/local/check-over-ballot.json and
data/local/check-listed-rows.json.

  42.1 The moves file against my own diff of every local, measure, state-lower and state-upper record between the two
       commits: the codes (A G I T P B N L R Q O, W-), p before and after, the ratios; Virginia's gate words.
  42.2 c38's two districts: Vermont 2018's Chittenden Senate from MEDSL's own rows (the 'CHI' district, six seats) against
       the record, and my like-race p at both commits (the file's x3.49); Idaho 2022's Senate 1 from MEDSL's rows under the
       seventh pass's subtotal rule and from the state's canvass workbook (sheet 'Leg Dist 1'), and the write-in share.
  42.3 The over-ballot test from my own reading of the raw files (m2medsl.ballots_summary: every precinct's ballots cast
       as the orchestrator's reading of 11:16 and 17:44 (3) defines them, written apart from pipeline/local_volume.py part 4
       and local_medsl.over_ballot) against every row of check-over-ballot.json: the votes, the figure, the ratio, the
       verdict; and the statewide one-seat contests of MEDSL's files that the check does not list.
  42.4 Every row of check-listed-rows.json found in its raw file: the row's votes, and for the rows with a difference
       share the contest's total with and without it.
  42.5 Oregon 2024's Supreme Court: the abstract fetched from the Secretary of State's records system (one request,
       ~/.cache/vote-m2/eighth/src/index.txt), its two positions' county lines and Totals, the words 'official' and
       'certified', and the records' holds and notes.
  42.6 Arizona 2024's Corporation Commission in MEDSL's file (seats by county; Maricopa's and Pima's lines against the
       president's), and the records of M2's readings (b)-(d): Idaho's recalls, North Carolina's Courts of Appeals, the
       'Town of' questions.
[measured] throughout; D3's words and the records' own figures [stated].
"""
import collections
import glob
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402
import m2d3 as D  # noqa: E402
import m2medsl as M  # noqa: E402
import c40_pr_checks as C40  # noqa: E402
import c41_governor_refit as C41  # noqa: E402

BEFORE, AFTER = "9118755", "2ea7c2e"
MV = os.path.join(L.DATA, "local", "moves-held-totals.json")
OVER = os.path.join(L.DATA, "local", "check-over-ballot.json")
LISTED = os.path.join(L.DATA, "local", "check-listed-rows.json")
SRC = os.path.join(L.CACHE, "eighth", "src")
LEVELS = ("local", "measure", "state-lower", "state-upper")
h1, h2 = C41.h1, C40.h2


def records_at(root, f):
    p = os.path.join(root, f)
    if not os.path.exists(p):
        return {}
    with open(p) as fh:
        return {c["id"]: c for c in json.load(fh)["contests"]}


# ------------------------------------------------------------------------------------------ 42.1 the moves file

def section_1():
    h1("42.1 moves-held-totals.json against my own diff of every local, measure, state-lower and state-upper record, "
       f"{BEFORE} -> {AFTER}")
    wb, wa = C41.worktree(BEFORE), C41.worktree(AFTER)
    mv = L.load_json(MV)
    rows = {r[0]: r for r in mv["records"]}
    print(f"  the file: {len(mv['records'])} rows, {len(rows)} ids, against {mv.get('against')}; summary: {json.dumps(mv['summary'])}")
    print(f"  groups: {list(mv['groups'])}")
    import subprocess
    files = subprocess.run(["git", "diff", "--name-only", BEFORE, AFTER, "--", "data/"], capture_output=True, text=True, cwd=L.ROOT).stdout.split()
    data_files = [f for f in files if re.match(r"^data/(local|primary|measure|state-lower|state-upper)/\d{4}/[A-Z]{2}\.json$", f)
                  or re.match(r"^data/(governor|house|senate)/\d{4}\.json$", f)]
    print(f"  data files changed between the commits: {len(files)}; record files: {len(data_files)} "
          f"{dict(collections.Counter(f.split('/')[1] for f in data_files))}; other data files: "
          f"{[f for f in files if f not in data_files]}")
    mine = collections.Counter()
    agree, dis, seen, worst = 0, collections.Counter(), set(), []
    pdiff = rdiff = 0
    gone_new = {"G": [], "A": []}
    va_gate = collections.Counter()
    by_group_mine = collections.defaultdict(list)
    for f in data_files:
        lv = f.split("/")[1]
        b, a = records_at(wb, f), records_at(wa, f)
        for i in sorted(set(b) | set(a)):
            code = C40.my_code(b.get(i), a.get(i))
            if not code:
                continue
            d = C40.what_differs(b.get(i) or {}, a.get(i) or {})
            # the letters c40 does not derive: T (the type changed), W- (a question no longer counted whole), I (id changed)
            c = code[0]
            if c in ("B", "Q", "O", "R"):
                if any((b.get(i) or {}).get(k) != (a.get(i) or {}).get(k) for k in ("type", "office_type")):
                    c = "T"
                elif any(x.startswith("place.") or x in ("whole", "counted", "counted_whole", "coverage") for x in d):
                    c = "W-"
            mine[(lv, c)] += 1
            seen.add(i)
            if c in ("G", "A"):
                gone_new[c].append(i)
            if lv in ("state-lower", "state-upper") and "/VA.json" in f and i in a and i in b:
                gb, ga = str((b[i].get("gate") or {}).get("ruled")), str((a[i].get("gate") or {}).get("ruled"))
                nb_, na_ = " ".join(b[i].get("notes") or []), " ".join(a[i].get("notes") or [])
                va_gate[("the ruling's words added to gate.ruled", "accepted as proposed, with the 9th Senate district of 2023 held" in ga
                         and "accepted as proposed" not in gb)] += 1
                va_gate[("'not explained' added to a note", "not explained" in na_ and "not explained" not in nb_)] += 1
                if "not explained" in na_ and "not explained" not in nb_:
                    print(f"    'not explained' added: {i}: ...{na_[na_.index('not explained') - 120:na_.index('not explained') + 60]}")
            row = rows.get(i)
            if row is None:
                worst.append((i, c, "not in the moves file", d[:5]))
                continue
            theirs = tuple(row[8])
            ok = c in theirs or (c == "Q" and "O" in theirs) or (c == "O" and "Q" in theirs) or (c == "R" and ("Q" in theirs or "O" in theirs)) \
                or (c == "B" and ("Q" in theirs or "O" in theirs))
            if ok:
                agree += 1
            else:
                dis[(lv, c, theirs)] += 1
                worst.append((i, c, theirs, d[:5]))
            pb, pa = C40.pval(b.get(i) or {}), C40.pval(a.get(i) or {})
            if isinstance(row[5], str) or isinstance(row[6], str):
                continue
            if (row[5] is None) != (pb is None) or (row[6] is None) != (pa is None) \
                    or (pb is not None and abs(row[5] - pb) > 1e-9 * max(abs(pb), 1e-300)) \
                    or (pa is not None and abs(row[6] - pa) > 1e-9 * max(abs(pa), 1e-300)):
                pdiff += 1
                print(f"    p before/after differ from the record: {i} row {row[5]} {row[6]} record {pb} {pa}")
            if pb and pa and row[7] is not None and abs(row[7] - round(pa / pb, 4)) > 1.5e-4:
                rdiff += 1
                print(f"    ratio differs: {i} row {row[7]} mine {pa / pb:.4f}")
    not_mine = [i for i in rows if i not in seen]
    print("  my diff, by level and code: " + "; ".join(f"{lv} {k} {v}" for (lv, k), v in sorted(mine.items())))
    print(f"  rows whose code I share: {agree} of {len(seen)} ids in my diff; codes differing: {sum(dis.values())}; ids in my diff "
          f"but not in the file: {len([w for w in worst if w[2] == 'not in the moves file'])}; ids in the file but not in my diff: "
          f"{len(not_mine)} {not_mine[:5]}")
    print(f"  p before/after other than the record's: {pdiff}; ratios off by more than 1.5e-4: {rdiff}")
    for (lv, c, theirs), v in sorted(dis.items(), key=lambda kv: -kv[1])[:12]:
        ex = [w for w in worst if w[1] == c and w[2] == theirs][:2]
        print(f"    mine {c} theirs {theirs} {lv}: {v}; e.g. " + "; ".join(f"{e[0]} differs in {e[3]}" for e in ex))
    for w in [w for w in worst if w[2] == "not in the moves file"][:8]:
        print(f"    not in the file: {w[0]} mine {w[1]} differs in {w[3]}")
    print(f"  records gone (G): {gone_new['G']}; new (A): {gone_new['A']}")
    print(f"  Virginia 2023/2025 gate words (records in both commits): {dict(va_gate)}")
    # the file's own p columns: the one P and the one L
    for r in mv["records"]:
        if "P" in r[8] or "L" in r[8] or "T" in r[8] or "G" in r[8]:
            print(f"    file row: {r[0]} | {r[2]} | type {r[3]} -> {r[4]} | p {r[5]} -> {r[6]} | ratio {r[7]} | {r[8]}")
    # every row's codes against what the file's summary counts
    cnt = collections.Counter()
    for r in mv["records"]:
        for c in r[8]:
            cnt[(r[1].split("/")[1], c)] += 1
    print("  the file's rows by level and letter: " + "; ".join(f"{lv} {c} {v}" for (lv, c), v in sorted(cnt.items())))
    return {"agree": agree, "seen": len(seen), "dis": sum(dis.values()), "not_mine": len(not_mine), "pdiff": pdiff, "rdiff": rdiff}


# ------------------------------------------------------------------------------------------ 42.2 c38's two districts

def surname(name):
    """'ashe, tim' -> 'ASHE'; 'TIM ASHE' -> 'ASHE' (the last token, suffixes dropped)."""
    s = name.upper().replace(".", "")
    if "," in s:
        return s.split(",")[0].strip()
    toks = [t for t in s.split() if t not in ("JR", "SR", "II", "III", "IV")]
    return toks[-1] if toks else s


def medsl_contest(path, year, office, district):
    """Candidate -> votes (a precinct's TOTAL row where it has one, else its modes summed; subtotal rows left out) and the
    write-in flag, for one contest of a raw file; and the raw sums with every row."""
    cells = {}
    wi = {}
    for r in M.rows(path):
        if (r.get("office") or "").strip().upper() != office or (r.get("district") or "").strip().upper() != district:
            continue
        if (r.get("stage") or "GEN").upper() != "GEN":
            continue
        pk = (M.fips5(r.get("county_fips", "")), r.get("jurisdiction_fips", ""), r.get("precinct", ""))
        cand = (r.get("candidate") or "").strip().upper()
        if M.is_meta(cand):
            continue
        try:
            v = int(float(r.get("votes") or ""))
        except ValueError:
            continue
        mode = (r.get("mode") or "TOTAL").upper()
        cell = cells.setdefault(pk, {}).setdefault(cand, {})
        cell[mode] = cell.get(mode, 0) + v
        wi[cand] = (r.get("writein") or "").strip().upper() in ("TRUE", "T", "1", "YES")
    resolved = {pk: {c: M._resolve(m) for c, m in cs.items()} for pk, cs in cells.items()}
    resolved = {pk: {c: v for c, v in cs.items() if v is not None} for pk, cs in resolved.items()}
    subs = M._subtotal_rows(resolved)
    out, out_all = collections.Counter(), collections.Counter()
    for pk, cs in resolved.items():
        for c, v in cs.items():
            out_all[c] += v
            if pk not in subs:
                out[c] += v
    return out, out_all, wi, len(resolved), len(subs)


def section_2():
    h1("42.2 c38's two districts: Vermont 2018 Chittenden and Idaho 2022 Senate 1")
    wb, wa = C41.worktree(BEFORE), C41.worktree(AFTER)
    h2("  Vermont 2018, Chittenden Senate (six seats): MEDSL's 'CHI' rows against the record after; my like-race p at both commits")
    vt = M.medsl_file(2018, "VT")
    cands, cands_all, wi, npk, nsub = medsl_contest(vt, 2018, "STATE SENATE", "CHI")
    rb = records_at(wb, "data/state-upper/2018/VT.json")["2018-state-upper-VT-Chittenden"]
    ra = records_at(wa, "data/state-upper/2018/VT.json")["2018-state-upper-VT-Chittenden"]
    named = {c: v for c, v in cands.items() if not wi.get(c)}
    wins = {c: v for c, v in cands.items() if wi.get(c)}
    print(f"    MEDSL rows: {npk} precinct keys, {nsub} subtotal rows; named candidates {len(named)}, write-in lines {len(wins)} "
          f"(their votes {sum(wins.values()):,}); every row summed: {sum(cands_all.values()):,}; subtotals out: {sum(cands.values()):,}")
    by_sur = collections.defaultdict(list)
    for c, v in named.items():
        by_sur[surname(c)].append((c, v))
    ok = bad = 0
    for cand in ra["result"]["candidates"]:
        hits = by_sur.get(surname(cand["name"]), [])
        v = hits[0][1] if len(hits) == 1 else None
        same = v == cand["votes"]
        ok += same
        bad += not same
        kb = [x for x in rb["result"]["candidates"] if x["name"] == cand["name"]]
        print(f"    {cand['name']:<28} record after {cand['votes']:>7,}  MEDSL {str(v):>7}  {'=' if same else '!='}   "
              f"record before (Klarner) {kb[0]['votes']:>9,}  ratio {kb[0]['votes'] / cand['votes']:.2f}" if kb else "")
    print(f"    candidates equal to MEDSL's: {ok}; unequal: {bad}; MEDSL surnames not in the record: "
          f"{[s for s in by_sur if s not in {surname(c['name']) for c in ra['result']['candidates']}]}")
    print(f"    record total_votes after {ra['result']['total_votes']:,} (D3: 310,430); my named sum {sum(named.values()):,}; "
          f"with the write-in lines {sum(cands.values()):,}; before (Klarner) {rb['result']['total_votes']:,} (D3: 1,096,537)")
    rat = [x['votes'] / y['votes'] for x in rb['result']['candidates'] for y in ra['result']['candidates'] if x['name'] == y['name']]
    print(f"    Klarner/MEDSL ratios: {min(rat):.2f} to {max(rat):.2f} (D3: 2.78 to 3.83)")
    # my p at each commit
    for tag, root, rec in (("before", wb, rb), ("after", wa, ra)):
        slim = D.slim("state-upper", {"state": "VT", "year": 2018, "contests": [rec]} if False else L.load_json(os.path.join(root, "data/state-upper/2018/VT.json")), rec)
        p, how = C40.p_of_record(root, slim, {})
        print(f"    {tag}: record p {C40.pval(rec)}; route {slim['route']} cls {slim['cls']} n {C40.record_n(slim)}; my p {p} ({how})")
    pb_, pa_ = C40.pval(rb), C40.pval(ra)
    print(f"    the file's ratio x3.49: record {pa_ / pb_:.3f}")
    C40.forget(wb)
    h2("  Idaho 2022, Senate 1: MEDSL's rows under the subtotal rule, and the canvass workbook's sheet 'Leg Dist 1'")
    idf = M.medsl_file(2022, "ID")
    cands, cands_all, wi, npk, nsub = medsl_contest(idf, 2022, "STATE SENATE", "001")
    print(f"    MEDSL: {npk} precinct keys, {nsub} subtotal rows (the COUNTY TOTAL rows); every row summed {dict(cands_all)}; "
          f"subtotals out {dict(cands)}; write-in marks {wi}")
    import openpyxl
    wbk = openpyxl.load_workbook(os.path.join(SRC, "id", "2022_General_Canvass", "22 General Legislative - Precinct.xlsx"), read_only=True)
    ws = wbk["Leg Dist 1"]
    names, sums, counties, co_rows = None, None, [], []
    for row in ws.iter_rows(values_only=True):
        vals = list(row)
        if vals[0] == "Precinct":
            names = vals[1:5]
            sums = [0, 0, 0, 0]
            continue
        if names is None:
            continue
        if isinstance(vals[0], str) and vals[0].strip() in ("CO. TOTAL", "DIST. TOTAL"):
            co_rows.append((vals[0], vals[1:5]))
            continue
        if isinstance(vals[0], str) and all(v is None for v in vals[1:5]):
            counties.append(vals[0])
            continue
        if all(isinstance(v, (int, float)) for v in vals[1:5]):
            for j in range(4):
                sums[j] += vals[j + 1]
    print(f"    canvass sheet 'Leg Dist 1': columns {names}; counties {counties}; precinct rows summed: "
          f"{dict(zip(names, sums))}; the sheet's total rows are formulas {co_rows[-1]}")
    hern = sums[0]
    john = sums[1]
    print(f"    Herndon canvass {hern:,} = MEDSL {cands.get('SCOTT HERNDON')} = record {records_at(wa, 'data/state-upper/2022/ID.json')['2022-state-upper-ID-1']['result']['candidates'][0]['votes']}: "
          f"{hern == cands.get('SCOTT HERNDON') == 13064}; Johnson canvass {john:,} = MEDSL {cands.get('STEVEN R JOHNSON')}: {john == cands.get('STEVEN R JOHNSON') == 9025}; "
          f"share of Herndon's {john / hern:.3f} (D3: 69%, more than the write-in rule's 10%)")
    ra = records_at(wa, "data/state-upper/2022/ID.json")["2022-state-upper-ID-1"]
    rb = records_at(wb, "data/state-upper/2022/ID.json")["2022-state-upper-ID-1"]
    print(f"    record before: {[(c['name'], c.get('party'), c['votes']) for c in rb['result']['candidates']]} p {C40.pval(rb)}; "
          f"after: {[(c['name'], c.get('party'), c['votes']) for c in ra['result']['candidates']]} p {ra['p']}")


# ------------------------------------------------------------------------------------------ 42.3 the over-ballot test

WRITEIN_RE = re.compile(r"^(WRITE-?IN|WRITE IN|WRITE-INS|WRITEINS|SCATTERING|SCATTERED)\b")


def norm_district(d):
    d = (d or "").strip().upper()
    return "" if d in M.STATEWIDE_DISTRICTS else d


GOVERNOR_RE = re.compile(r"^GOVERNOR\b(?! *'S COUNCIL)")   # D2's level, not a local record (the lieutenant governor and a council stay)


def my_over_ballot(year):
    """My over-ballot test for a year from the ballots summaries: every statewide one-seat candidate contest of dataverse
    STATE with votes in every county of its day; its votes (subtotal rows left out) against the sum over its live
    precincts of the bound (another one-seat contest's votes + overvotes + undervotes or total line, the largest, or a
    line named as the ballots cast), where every live precinct has one; else against the day's highest-vote statewide
    contest (the other whole one-seat STATE contests not held, the whole STATE questions, the whole PRESIDENT and
    SENATE contests); held above 1 (ballots) or 1.1 (top); listed between 1 and 1.1 against the top. Iterated: a
    contest held is no one's top."""
    out = {}
    for y, path in M.all_raw_files():
        if y != year:
            continue
        s = M.ballots_summary(path, year)
        for sd in {k.split("|")[0] + "|" + k.split("|")[1] for k in s["contests"]}:
            st, date = sd.split("|")
            day = s["counties_of_day"].get(sd, 0)
            cs = {k: v for k, v in s["contests"].items() if k.startswith(sd + "|")}
            whole = {k: v for k, v in cs.items() if day and v["counties"] >= day}
            one = {k: v for k, v in whole.items() if k.split("|")[2] == "STATE" and not v["answers"]
                   and v["magnitudes"] in (["1"], ["1.0"]) and not k.endswith(" SPECIAL")}
            read = {k for k in one if not GOVERNOR_RE.match(k.split("|")[3])}   # the local files' level (D2 holds the governors)
            asked = {k: v for k, v in whole.items() if v["answers"]}   # a question of any dataverse put to every county
            fed = {k: v for k, v in whole.items() if k.split("|")[2] in ("PRESIDENT", "SENATE") and not v["answers"]}
            bounds = s["bounds"].get(sd, {})
            held = set()
            for _ in range(4):
                res = {}
                for k, v in one.items():
                    votes = sum(v["cands"].values())
                    b_sum, nb = 0, 0
                    for pk in v["live"]:
                        e = bounds.get(pk)
                        if not e:
                            continue
                        c_ = [f[0] for f in e[:-1] if f[1] != k][:1]
                        if e[-1] is not None:
                            c_.append(e[-1])
                        if c_:
                            b_sum += max(c_)
                            nb += 1
                    if v["live"] and nb == len(v["live"]):
                        res[k] = ("ballots cast", b_sum, votes / b_sum if b_sum else None, nb, len(v["live"]))
                        continue
                    tops = [(sum(o["cands"].values()), o_k) for o_k, o in one.items() if o_k != k and o_k not in held]
                    tops += [(sum(o["cands"].values()), o_k + " (a question)") for o_k, o in asked.items()]
                    tops += [(sum(o["cands"].values()), o_k) for o_k, o in fed.items()]
                    if not tops:
                        res[k] = ("untested", None, None, nb, len(v["live"]))
                        continue
                    t_, name = max(tops)
                    res[k] = ("top", t_, votes / t_ if t_ else None, nb, len(v["live"]), name)
                new = {k for k, r in res.items() if r[2] is not None and ((r[0] == "ballots cast" and r[2] > 1) or (r[0] == "top" and r[2] > 1.1))}
                if new == held:
                    break
                held = new
            for k, r in res.items():
                if k not in read:
                    continue
                verdict = "held" if k in held else ("listed" if r[0] == "top" and r[2] is not None and r[2] > 1 else ("untested" if r[0] == "untested" else "passes"))
                out[k] = {"votes": sum(one[k]["cands"].values()), "votes_all": sum(one[k]["cands_all"].values()), "against": r[0], "figure": r[1],
                          "ratio": r[2], "bounded": r[3], "live": r[4], "verdict": verdict, "of": r[5] if len(r) > 5 else None,
                          "counties": one[k]["counties"], "day": day}
            # the one-seat STATE contests not whole, for the listing
            for k, v in cs.items():
                if k not in whole and k.split("|")[2] == "STATE" and not v["answers"] and v["magnitudes"] in (["1"], ["1.0"]):
                    out[k] = {"votes": sum(v["cands"].values()), "against": "not whole", "figure": None, "ratio": None, "verdict": "not whole",
                              "counties": v["counties"], "day": day}
    return out


def section_3():
    h1("42.3 The over-ballot test from my own reading of the raw files against check-over-ballot.json")
    chk = L.load_json(OVER)
    print(f"  the check: {chk['about'][:200]}...; untested years {chk.get('untested_years')}")
    wa = C41.worktree(AFTER)
    totals = collections.Counter()
    for year in (2018, 2022, 2024):
        theirs = chk[str(year)]
        mine = my_over_ballot(year)
        h2(f"  {year}: the check lists {len(theirs)} contests; my test reads {sum(1 for v in mine.values() if v['verdict'] != 'not whole')} "
           f"whole one-seat STATE contests ({sum(1 for v in mine.values() if v['verdict'] == 'not whole')} not whole)")
        agree_v = agree_k = agree_votes = agree_fig = 0
        miss = []
        used = set()
        diffs = []
        for t in theirs:
            cands_ = [k for k in mine if k.split("|")[0] == t["state"] and k.split("|")[3] == t["office"].upper()
                      and norm_district(k.split("|")[4]) == norm_district(t["district"])]
            if len(cands_) != 1:   # a check row of a special election
                cands_ = [k for k in mine if k.split("|")[0] == t["state"] and k.split("|")[3] == t["office"].upper()
                          and norm_district(k.split("|")[4].replace(" SPECIAL", "")) == norm_district(t["district"])]
            if len(cands_) != 1:
                miss.append((t["state"], t["office"], t["district"], t["verdict"], len(cands_)))
                continue
            k = cands_[0]
            used.add(k)
            m = mine[k]
            sv = m["votes"] == t["votes"]
            sk = m["against"] == t["against"]
            sf = (m["figure"] == t["figure"]) if sk else False
            sr = m["ratio"] is not None and t["ratio"] is not None and abs(m["ratio"] - t["ratio"]) < 6e-4
            svd = m["verdict"] == t["verdict"]
            agree_votes += sv
            agree_k += sk
            agree_fig += sf
            agree_v += svd
            totals[("rows", year)] += 1
            totals[("verdict", year)] += svd
            if not (sv and sk and sf and svd):
                diffs.append((t, m, k))
        print(f"    rows matched to my contests: {len(theirs) - len(miss)} of {len(theirs)}; votes equal {agree_votes}; the same test "
              f"(ballots cast / top) {agree_k}; the same figure {agree_fig}; the same verdict {agree_v}")
        if miss:
            print(f"    the check's rows I did not match: {miss[:12]}{' ...' if len(miss) > 12 else ''}")
            allc = {}
            for y_, path in M.all_raw_files():
                if y_ == year:
                    s_ = M.ballots_summary(path, year)
                    for k, v in s_["contests"].items():
                        allc[k] = (v["magnitudes"], v["counties"], s_["counties_of_day"].get("|".join(k.split("|")[:2])), v["answers"], sum(v["cands"].values()))
            shown = set()
            for st, office, district, verdict, n in miss:
                if (st, office) in shown:
                    continue
                shown.add((st, office))
                ks = [(k.split("|")[2], k.split("|")[4], allc[k]) for k in allc if k.split("|")[0] == st and office.upper() in k.split("|")[3]]
                print(f"      {st} {office}: my summary holds {ks[:4]}")
        kinds = collections.Counter()
        for t, m, k in diffs:
            kinds[("votes" if m["votes"] != t["votes"] else "") + ("|test" if m["against"] != t["against"] else "") +
                  ("|figure" if m["against"] == t["against"] and m["figure"] != t["figure"] else "") +
                  ("|verdict" if m["verdict"] != t["verdict"] else "")] += 1
        print(f"    rows differing in something: {len(diffs)} {dict(kinds)}")
        vd = [abs(m["votes"] / t["votes"] - 1) for t, m, k in diffs if m["votes"] != t["votes"] and t["votes"]]
        va = sum(1 for t, m, k in diffs if m["votes"] != t["votes"] and m.get("votes_all") == t["votes"])
        if vd:
            print(f"    votes differing: {len(vd)}, by at most {max(vd):.2%} of the check's; equal to my sum with every row (the subtotal rule aside): {va}")
        for t, m, k in diffs[:40]:
            print(f"      {t['state']} {t['office']} {t['district'] or ''}: D3 votes {t['votes']:,} {t['against']} {t['figure']} ratio {t['ratio']} {t['verdict']} | "
                  f"mine votes {m['votes']:,} (every row {m.get('votes_all', 0):,}) {m['against']} {m['figure']} ratio {None if m['ratio'] is None else round(m['ratio'], 4)} {m['verdict']} "
                  f"(bounded {m.get('bounded')}/{m.get('live')}; counties {m['counties']}/{m['day']}{'; top ' + str(m['of']) if m.get('of') else ''})")
        for verdict in ("held", "listed"):
            th = sorted((t["state"], t["office"], t["ratio"]) for t in theirs if t["verdict"] == verdict)
            mi = sorted((k.split("|")[0], k.split("|")[3], round(m["ratio"], 4)) for k, m in mine.items() if m["verdict"] == verdict)
            print(f"    {verdict}: D3 {th}; mine {mi}")
        # my whole one-seat contests the check does not list
        extra = [(k, m) for k, m in mine.items() if k not in used and m["verdict"] != "not whole"]
        print(f"    my whole one-seat STATE contests the check does not list: {len(extra)}")
        loc = {}
        for f in glob.glob(os.path.join(wa, "data", "local", str(year), "*.json")):
            st = os.path.basename(f)[:2]
            loc[st] = L.load_json(f)["contests"]
        reasons = collections.Counter()
        for k, m in sorted(extra):
            st, date, dv, office, district = k.split("|")
            recs = [c for c in loc.get(st, []) if (c.get("office") or "").upper() == office
                    and norm_district(c.get("district") or (c.get("place") or {}).get("district")) == norm_district(district)]
            if not recs:
                recs = [c for c in loc.get(st, []) if (c.get("office") or "").upper() == office]
            r0 = recs[0] if recs else None
            if r0 is None:
                why = "no local record of the office"
            else:
                res_ = r0.get("result") or {}
                why = (f"{len(recs)} record(s), e.g. {r0['id']}: votes_source {res_.get('votes_source')}, source {res_.get('source')}; total {res_.get('total_votes')}; "
                       f"seats {r0.get('seats')}; question {r0.get('question')}; held {str(r0.get('held_reason'))[:60]!r}; p {json.dumps(r0.get('p'))[:80]}")
            reasons["no local record" if r0 is None else ("the state's own count" if r0 and (r0.get("result") or {}).get("votes_source") not in (None, "medsl")
                    else "held" if r0 and r0.get("held_reason") else "a record of MEDSL's count")] += 1
            print(f"      {k}: votes {m['votes']:,} {m['against']} ratio {None if m['ratio'] is None else round(m['ratio'], 3)} {m['verdict']}; {why[:230]}")
        print(f"    {dict(reasons)}")
    print(f"  all years: rows {sum(v for (k, y), v in totals.items() if k == 'rows')}, the same verdict "
          f"{sum(v for (k, y), v in totals.items() if k == 'verdict')}")


# ------------------------------------------------------------------------------------------ 42.4 the listed rows

def section_4():
    h1("42.4 Every row of check-listed-rows.json in its raw file: the row's votes, and the contest's totals with and without it")
    chk = L.load_json(LISTED)
    print(f"  the check: {chk['about'][:300]}...")
    by_file = collections.defaultdict(list)
    for y in ("2016", "2018", "2020", "2022", "2024"):
        for r in chk[y]:
            by_file[(int(y), r["file"])].append(r)
    print(f"  rows by year: {[(y, len(chk[y])) for y in ('2016', '2018', '2020', '2022', '2024')]}; files: {len(by_file)}; "
          f"with a difference share: {sum(1 for y in chk if y.isdigit() for r in chk[y] if 'difference_share' in r)}; noted: "
          f"{sum(1 for y in chk if y.isdigit() for r in chk[y] if r.get('noted'))}")
    found = notfound = votes_eq = votes_ne = 0
    share_ok = share_bad = 0
    examples = []
    kinds_found = collections.Counter()
    for (year, fname), rs in sorted(by_file.items()):
        paths = [p for yy, p in M.all_raw_files() if os.path.basename(p) == fname]
        paths += [p for p in glob.glob(os.path.join(SRC, "medsl22", fname))]   # MEDSL's 2022 New Jersey and Vermont files from its GitHub (index.txt)
        if not paths:
            notfound += len(rs)
            print(f"    raw file not cached: {fname} ({len(rs)} rows)")
            continue
        path = paths[0]
        want = {}
        for r in rs:
            want[(r["county"], r["precinct"], (r["office"] or "").upper(), norm_district(r["district"]))] = r
        contests_needed = {(w[2], w[3]) for w in want}
        row_votes = collections.Counter()
        row_hits = collections.Counter()
        cont = collections.defaultdict(lambda: collections.defaultdict(dict))   # (office, district) -> pk -> cand -> {mode: v}
        cont_counties = collections.defaultdict(set)
        for r in M.rows(path):
            office = (r.get("office") or "").strip().upper()
            district = norm_district(r.get("district"))
            if (office, district) not in contests_needed:
                continue
            if (r.get("stage") or "GEN").upper() != "GEN":
                continue
            if year == 2016:
                county = M.fips5(r.get("county_fips", ""))
                pk = (county, r.get("jurisdiction", ""), r.get("precinct", ""))
            else:
                county = M.fips5(r.get("county_fips", ""))
                pk = (county, r.get("jurisdiction_fips", ""), r.get("precinct", ""))
            cand = (r.get("candidate") or "").strip().upper()
            if M.is_meta(cand):
                continue
            try:
                v = int(float(r.get("votes") or ""))
            except ValueError:
                continue
            mode = (r.get("mode") or "TOTAL").upper()
            dv = (r.get("dataverse") or "").upper()
            wi = (r.get("writein") or "").strip().upper() in ("TRUE", "T", "1", "YES") or WRITEIN_RE.match(cand)
            cell = cont[(office, district, dv)][pk].setdefault((cand, bool(wi)), {})
            cell[mode] = cell.get(mode, 0) + v
            cont_counties[(office, district, dv)].add(county)
            key = (county, r.get("precinct", ""), office, district)
            if key in want:
                row_hits[key] += 1
        # resolve
        res = {}
        for ck, pks in cont.items():
            res[ck] = {pk: {c: M._resolve(m) for c, m in cs.items()} for pk, cs in pks.items()}
        for key, r in want.items():
            county, precinct, office, district = key
            # the contest the row falls in: the one of its office/district whose counties hold the row's county; its dataverse
            cks = [ck for ck in res if ck[0] == office and ck[1] == district and county in cont_counties[ck]]
            local_office = any(ck[2] == "LOCAL" for ck in cks)   # a county office: its contest is the county's own rows
            pks = [pk for ck in cks for pk in res[ck] if pk[0] == county and pk[2] == precinct]
            if not pks:
                notfound += 1
                if len(examples) < 10:
                    examples.append((year, fname, key, "row not found"))
                continue
            found += 1
            kinds_found[r["kind"]] += 1
            rv = sum(v for ck in cks for pk in res[ck] if pk[0] == county and pk[2] == precinct for v in res[ck][pk].values() if v is not None)
            if rv != r["row_votes"] and len(examples) < 30:
                examples.append((year, fname, key, "the row's lines: " + str([(ck[2], pk[1], c_, v) for ck in cks for pk in res[ck] if pk[0] == county and pk[2] == precinct for c_, v in res[ck][pk].items()])[:300]))
            if rv == r["row_votes"]:
                votes_eq += 1
            else:
                votes_ne += 1
                if len(examples) < 30:
                    examples.append((year, fname, key, f"row votes {rv} vs the check's {r['row_votes']}"))
            if "difference_share" in r and r.get("total_with") is not None:
                # the contest's total as the record counts it: the named candidates' lines (a write-in line is no candidate)
                tw = sum(v for ck in cks for pk in res[ck] if not local_office or pk[0] == county for (c_, wi), v in res[ck][pk].items() if v is not None and not wi)
                share = rv / tw if tw else None
                ok = tw == r["total_with"] and share is not None and abs(share - r["difference_share"]) < 1e-5
                share_ok += ok
                share_bad += not ok
                if not ok and len(examples) < 40:
                    examples.append((year, fname, key, f"total with {tw} vs {r['total_with']}; share {share} vs {r['difference_share']}"))
    print(f"  rows found in the raw file: {found}; not found: {notfound}; row votes equal to the check's: {votes_eq}; unequal: {votes_ne}")
    print(f"  rows with a difference share: total with and share equal: {share_ok}; unequal: {share_bad}")
    print(f"  kinds found: {dict(kinds_found)}")
    for e in examples:
        print(f"    {e}")
    # the noted rows and the records' notes at the commit after
    wa = C41.worktree(AFTER)
    noted = [(y, r) for y in chk if y.isdigit() for r in chk[y] if r.get("noted")]
    with_note = 0
    for y, r in noted:
        if not r.get("record"):
            continue
        st = r["state"]
        lv = "local"
        recs = records_at(wa, f"data/local/{y}/{st}.json")
        rec = recs.get(r["record"])
        if rec is None:
            for lv_ in ("state-lower", "state-upper", "measure"):
                rec = records_at(wa, f"data/{lv_}/{y}/{st}.json").get(r["record"])
                if rec:
                    break
        ok = rec is not None and any("possible total row" in n for n in (rec.get("notes") or []))
        with_note += ok
        if not ok:
            print(f"    noted row whose record carries no 'possible total row' note: {y} {r['record']} {'(no record)' if rec is None else ''}")
    print(f"  noted rows: {len(noted)}; their records carrying the note at {AFTER}: {with_note} (D3: 27 records, 23 of them 'equal to the rest')")


# ------------------------------------------------------------------------------------------ 42.5 Oregon's abstract

def section_5():
    h1("42.5 Oregon 2024's Supreme Court: the Secretary of State's abstract (records system uri 13735458), fetched once")
    idx = open(os.path.join(SRC, "index.txt")).read()
    print("  " + idx.replace("\n", "\n  ").strip())
    pdf = os.path.join(SRC, "or-2024-abstract.pdf")
    txt = os.path.join(SRC, "or", "abstract.txt")
    if not os.path.exists(txt):
        import subprocess
        os.makedirs(os.path.dirname(txt), exist_ok=True)
        subprocess.run(["pdftotext", "-layout", pdf, txt], check=True)
    text = open(txt).read()
    lines = text.split("\n")
    heads = sum(1 for ln in lines if "November 5, 2024, General Election Abstract of Votes" in ln)
    pages = text.count("\f") + 1
    print(f"  sha256 {L.sha256(pdf)}; pdftotext -layout: {len(lines):,} lines, {pages} pages, {heads} headed 'November 5, 2024, General Election Abstract of Votes'")
    for w in (r"\bofficial\b", r"\bofficials?\b", r"\bcertified\b", r"certif", r"\bunofficial\b"):
        n = len(re.findall(w, text, flags=re.I))
        print(f"  the word '{w}': {n} occurrences" + (f" e.g. {[ln.strip()[:100] for ln in lines if re.search(w, ln, re.I)][:3]}" if n else ""))
    # the two positions
    for pos in ("Position 1", "Position 7"):
        i = next(j for j, ln in enumerate(lines) if "Judge of the Supreme Court" in ln and pos in lines[j + 1])
        block = lines[i:i + 50]
        head = block[2].split()
        cand = head[0].lstrip("*")
        county_lines, total = [], None
        for ln in block[4:]:
            m = re.match(r"^\s*([A-Za-z][A-Za-z ]+?)\s+([\d,]+)\s+([\d,]+)\s*$", ln)
            if m:
                a, b = int(m.group(2).replace(",", "")), int(m.group(3).replace(",", ""))
                if m.group(1).strip() == "Total":
                    total = (a, b)
                else:
                    county_lines.append((m.group(1).strip(), a, b))
        sa, sb = sum(x[1] for x in county_lines), sum(x[2] for x in county_lines)
        print(f"  {pos}: {cand} (marked ** Elected); {len(county_lines)} county lines; county sums {sa:,} / Misc. {sb:,}; Total line {total[0]:,} / {total[1]:,}; "
              f"candidate sum = Total: {sa == total[0]}; Misc. sum = Total: {sb == total[1]} (difference {sb - total[1]:+d})")
    # the records
    wa = C41.worktree(AFTER)
    wb = C41.worktree(BEFORE)
    recs = records_at(wa, "data/local/2024/OR.json")
    before = records_at(wb, "data/local/2024/OR.json")
    for i, c in recs.items():
        if "SUPREME" in i.upper() or "supreme" in (c.get("title") or c.get("office") or "").lower():
            b = before.get(i) or {}
            print(f"  record {i}: type {c.get('type')}; p {c.get('p')}; held_reason: {str(c.get('held_reason'))[:400]}")
            print(f"    notes: {[n[:300] for n in (c.get('notes') or [])]}")
            print(f"    differs from before in: {C40.what_differs(b, c)}; before p {b.get('p')}")
    src = L.load_json(os.path.join(wa, "data/local/2024/OR.json")).get("sources", {})
    print(f"  the file's sources.or_sos: {json.dumps(src.get('or_sos'))[:400]}")


# ------------------------------------------------------------------------------------------ 42.6 Arizona's commission and M2's readings

def section_6():
    h1("42.6 Arizona 2024's Corporation Commission in MEDSL's file; the records of M2's readings (b)-(d)")
    az = M.medsl_file(2024, "AZ")
    by_county = collections.defaultdict(lambda: {"mags": set(), "districts": set(), "votes": 0, "over": 0, "under": 0, "has": set()})
    cells = {}   # (office kind, county, pk, cand) -> {mode: votes}
    pres_office = collections.Counter()
    pres_meta_names = collections.Counter()
    for r in M.rows(az):
        office = (r.get("office") or "").upper()
        if (r.get("stage") or "GEN").upper() != "GEN":
            continue
        county = M.fips5(r.get("county_fips", ""))
        cand = (r.get("candidate") or "").strip().upper()
        try:
            v = int(float(r.get("votes") or ""))
        except ValueError:
            continue
        mode = (r.get("mode") or "TOTAL").upper()
        pk = (county, r.get("jurisdiction_fips", ""), r.get("precinct", ""))
        if "PRESIDENT" in office and (r.get("dataverse") or "").upper() == "PRESIDENT":
            pres_office[office] += 1
            cell = cells.setdefault(("pres" if not M.is_meta(cand) else "pres_meta", county, pk, cand), {})
            cell[mode] = cell.get(mode, 0) + v
            if M.is_meta(cand):
                pres_meta_names[cand] += v
        if "CORPORATION COMMISSION" not in office:
            continue
        e = by_county[county]
        e["mags"].add((r.get("magnitude") or "").strip())
        e["districts"].add((r.get("district") or "").strip())
        kind = "over" if M.OVER_LINE.match(cand) else "under" if M.UNDER_LINE.match(cand) else None if M.is_meta(cand) else "votes"
        if kind:
            cell = cells.setdefault(("cc", county, pk, (kind, cand)), {})
            cell[mode] = cell.get(mode, 0) + v
    pres, pres_meta = collections.Counter(), collections.Counter()
    for (what, county, pk, cand), modes in cells.items():
        v = M._resolve(modes)
        if v is None:
            continue
        if what == "pres":
            pres[county] += v
        elif what == "pres_meta":
            pres_meta[county] += v
        else:
            by_county[county][cand[0]] += v
            by_county[county]["has"].add(cand[0])
    print(f"  the president's office names: {dict(pres_office)}")
    print(f"  counties with Corporation Commission rows: {len(by_county)}; magnitudes by county: "
          f"{dict(collections.Counter(tuple(sorted(e['mags'])) for e in by_county.values()))}; districts: "
          f"{dict(collections.Counter(tuple(sorted(e['districts'])) for e in by_county.values()))}")
    for county, name in (("04013", "Maricopa"), ("04019", "Pima"), ("04023", "Santa Cruz")):
        e = by_county.get(county)
        if not e:
            continue
        tot = e["votes"] + e["over"] + e["under"]
        print(f"  {name}: magnitudes {sorted(e['mags'])}, districts {sorted(e['districts'])}, votes {e['votes']:,} over {e['over']:,} under {e['under']:,} "
              f"= {tot:,}; president's candidate lines {pres[county]:,} (its other lines, {dict(pres_meta_names) if county == '04013' else '...'}: {pres_meta[county]:,}); "
              f"ratio {tot / pres[county]:.2f}, or {tot / (pres[county] + pres_meta[county]):.2f} with them (D3: Maricopa 6,213,612 / 2,078,930, Pima 1,550,565 / 518,466, 2.99)")
    wa, wb = C41.worktree(AFTER), C41.worktree(BEFORE)
    recs = records_at(wa, "data/local/2024/AZ.json")
    for i, c in recs.items():
        if "CORPORATION" in i.upper():
            print(f"  record {i}: seats {c.get('seats')}; pieces joined {len(c.get('pieces_joined') or [])}; p {c.get('p')}; total {c['result'].get('total_votes')}")
    h2("  (b) Idaho 2024's recalls: the two local records gone, the two questions carrying both answers")
    lb, la = records_at(wb, "data/local/2024/ID.json"), records_at(wa, "data/local/2024/ID.json")
    mb, ma = records_at(wb, "data/measure/2024/ID.json"), records_at(wa, "data/measure/2024/ID.json")
    gone = [i for i in lb if i not in la]
    print(f"    local records gone: {gone}")
    for i in ma:
        if "RECALL" in i.upper() and (i not in mb or mb[i] != ma[i]):
            c = ma[i]
            print(f"    question {i}: answers {[(x.get('name') or x.get('answer'), x['votes']) for x in c['result']['candidates']]} "
                  f"(before: {[(x.get('name') or x.get('answer'), x['votes']) for x in mb[i]['result']['candidates']] if i in mb else 'none'}); p {c.get('p')}")
    h2("  (c) North Carolina 2008 and 2010 Court of Appeals: typed judge")
    for y, seat in ((2008, "Martin"), (2010, "Steelman")):
        rb_, ra_ = records_at(wb, f"data/local/{y}/NC.json"), records_at(wa, f"data/local/{y}/NC.json")
        for i in ra_:
            if seat.upper() in i.upper() and "COURT_OF_APPEALS" in i:
                print(f"    {i}: office_type {rb_[i].get('office_type')} -> {ra_[i].get('office_type')}; p {C40.pval(rb_[i])} -> {C40.pval(ra_[i])}; "
                      f"candidates {len(ra_[i]['result']['candidates'])}; title {ra_[i].get('title')!r}")
    h2("  (d) the 'Town of' guard: five 2024 questions of NY and RI now counted by county")
    for st in ("NY", "RI"):
        mb_, ma_ = records_at(wb, f"data/measure/2024/{st}.json"), records_at(wa, f"data/measure/2024/{st}.json")
        for i in ma_:
            if i in mb_ and mb_[i] != ma_[i]:
                d = C40.what_differs(mb_[i], ma_[i])
                print(f"    {i}: differs in {d}; place {json.dumps(ma_[i].get('place'))[:200]}; before place {json.dumps(mb_[i].get('place'))[:200]}; p {ma_[i].get('p')}")
        new = [i for i in ma_ if i not in mb_]
        gone = [i for i in mb_ if i not in ma_]
        if new or gone:
            print(f"    {st}: new ids {new}; gone {gone}")
    h2("  Arizona 2022's Attorney General: count_stage")
    rb_, ra_ = records_at(wb, "data/local/2022/AZ.json"), records_at(wa, "data/local/2022/AZ.json")
    for i in ra_:
        if "ATTORNEY" in i.upper():
            print(f"    {i}: result.count_stage {ra_[i]['result'].get('count_stage')!r} (before {rb_[i]['result'].get('count_stage')!r}); p {C40.pval(ra_[i])}; "
                  f"differs in {C40.what_differs(rb_[i], ra_[i])}")


def main():
    which = sys.argv[1:] or ["1", "2", "3", "4", "5", "6"]
    for w in which:
        globals()[f"section_{w}"]()


if __name__ == "__main__":
    main()
