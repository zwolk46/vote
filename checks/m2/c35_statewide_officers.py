"""c35: D3's #87 (afbb7bd): every single-seat statewide executive office in a state office's contest typed
"statewide officer" (359 records; 385 with #86's superintendents); no p moved.

The orchestrator (2026-11-07 16:53 UTC): "#87: the 359 retyped records against the office rule, and the 50 changed
reasons." The rule (16:08, verbatim in data/local/REPORT.md §24): "A single-seat statewide executive office in a state
office's contest is typed "statewide officer", read the way you read the superintendents. That covers treasurer,
auditor or comptroller, secretary of state, lieutenant governor, attorney general, and the single commissioners
(agriculture, insurance, labour, public service where one seat is elected statewide)."

What this does (every figure [measured] unless marked):
  35.1 the moves file (data/local/moves-statewide-officers.json) against my own diff of every local, primary, measure
       and state legislative file between e524840 (before: #86) and afbb7bd (after): the records that changed, what
       changed, the codes; p values (none moved, D3 says).
  35.2 the office rule read again by me, from the orchestrator's words: every state-scope record at afbb7bd whose
       office's whole name is one of the offices named (my own patterns, not the pipeline's), with no district and not
       one county's; against the 385 typed "statewide officer". Every state-scope office left untyped, grouped, against
       D3's list of what was left for a ruling (commissions, boards, judges, Montana's clerk, the District's, Illinois's).
  35.3 the 50 changed reasons: the count of like races each reason gives, before and after, against my own count of
       the class's members in earlier years, from the records' own classes at each commit (the pools of MEDSL's route
       and of North Carolina's own, as c15 draws them); the 69 retyped records whose reason now names the new class too.
  35.4 no p moved: every p value equal between the two commits; the 40 of the 359 with a p keep it; which other files
       changed (back-tests, calibration), no verdict read from them.
Nothing from pipeline/ is imported.
"""
import collections
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402
import m2d3 as D  # noqa: E402
import c15_d3_refit as C15  # noqa: E402
import c31_statewide_filed_local as C31  # noqa: E402
import c34_towns_counties as C34  # noqa: E402

BEFORE = "e524840"   # #86 merged
AFTER = "afbb7bd"    # #87 merged
MOVES = "data/local/moves-statewide-officers.json"
LEVELS = ("local", "primary", "measure", "state-lower", "state-upper")


# ---------------------------------------------------------------------------------------------- 35.1
def my_codes(b, a):
    codes = set()
    pb, pa = b.get("p") or {}, a.get("p") or {}
    if b.get("office_type") != a.get("office_type"):
        codes.add("T")
    if "not_computed" in pa and "not_computed" in pb and pa["not_computed"] != pb["not_computed"]:
        codes.add("R")
    return codes


def section_1():
    print(f"### 35.1 the moves file against my own diff of the records, {BEFORE} to {AFTER}")
    allf = C31.changed_files(BEFORE, AFTER, under=".")
    recf = [x for x in allf if re.search(r"data/(" + "|".join(LEVELS) + r")/\d{4}/[A-Z]{2}\.json$", x)]
    print(f"  files changed: {len(allf)}; record files {len(recf)} ({dict(collections.Counter(x.split('/')[1] for x in recf))}); others: "
          + ", ".join(x for x in allf if x not in recf))
    before, after = C31.load_records(BEFORE, recf), C31.load_records(AFTER, recf)
    changed = {cid: C31.deep_paths(before[cid], after[cid]) for cid in set(before) & set(after) if before[cid] != after[cid]}
    stamps = {cid for cid, v in changed.items() if v == ["p.commit"]}
    print(f"  records new {len(set(after) - set(before))}, gone {len(set(before) - set(after))}, changed {len(changed)} (p.commit stamp alone {len(stamps)})")
    for paths, n in collections.Counter(tuple(sorted({x.split('.')[0] for x in v})) for cid, v in changed.items() if cid not in stamps).most_common():
        print(f"    {n:5d}  {', '.join(paths)}")
    moved = [cid for cid in changed if "value" in (after[cid].get("p") or {}) and "value" in (before[cid].get("p") or {}) and after[cid]["p"]["value"] != before[cid]["p"]["value"]]
    became = [cid for cid in changed if ("value" in (after[cid].get("p") or {})) != ("value" in (before[cid].get("p") or {}))]
    print(f"  p values that moved: {len(moved)}; p that became computed or uncomputed: {len(became)} (D3: none)")
    mv = C34.show(AFTER, MOVES)
    recs = {r[0]: r for r in mv["records"]}
    mine = set(changed) - stamps
    print(f"  the moves file: {len(recs)} records (against {mv.get('against')}); summary {mv['summary']}")
    print(f"  its ids == my changed ids less the stamps: {set(recs) == mine}" + ("" if set(recs) == mine else
          f" (mine not listed {sorted(mine - set(recs))[:5]}, listed not mine {sorted(set(recs) - mine)[:5]})"))
    tal = collections.Counter()
    for cid, r in recs.items():
        b, a = before.get(cid), after.get(cid)
        if b is None or a is None:
            tal["not in both commits"] += 1
            continue
        same = (my_codes(b, a) == set(r[8]), r[3] == b.get("office_type"), r[4] == a.get("office_type"), r[5] == C34.pval(b), r[6] == C34.pval(a))
        tal["codes, types and p before and after all as the records" if all(same) else f"DIFFERS {same}"] += 1
        if not all(same):
            print(f"    {cid[:70]}: file {r[8]} mine {sorted(my_codes(b, a))} | {same}")
    print(f"  the records against the moves file: {dict(tal)}")
    T = [cid for cid, r in recs.items() if "T" in r[8]]
    print(f"  T rows {len(T)} (D3: 359: 316 local, 43 primary): by level {dict(collections.Counter(cid.split('-')[1] for cid in T))}; types before "
          f"{dict(collections.Counter(recs[cid][3] for cid in T))}; by office (upper) count {len(mv.get('typed_by_office', {}))} names, {sum(mv.get('typed_by_office', {}).values())} records")
    return before, after, mv


# ---------------------------------------------------------------------------------------------- 35.2
# my own reading of the ruling's list: the office's whole name, with a state's own prefix allowed ('NC ', 'STATE ',
# 'WASHINGTON STATE - '), names one of the offices the orchestrator listed (and the superintendents of #86)
PREFIX = re.compile(r"^(NC |STATE |[A-Z]+ STATE - )")
MY_OFFICES = [
    ("treasurer or chief financial officer", re.compile(r"^(TREASURER( OF STATE)?|GENERAL TREASURER|CHIEF FINANCIAL OFFICER)$")),
    ("auditor", re.compile(r"^AUDITOR( OF (STATE|ACCOUNTS|PUBLIC ACCOUNTS)| GENERAL| AND INSPECTOR)?$")),
    ("comptroller or controller", re.compile(r"^(COMPTROLLER|CONTROLLER)( GENERAL)?$")),
    ("secretary of state", re.compile(r"^SECRETARY OF (THE )?(STATE|COMMONWEALTH)$")),
    ("lieutenant governor", re.compile(r"^(LIEUTENANT|LT\.?) GOVERNOR$")),
    ("attorney general", re.compile(r"^ATTORNEY GENERAL( - [A-Z ]+)?$")),
    ("superintendent of public instruction", re.compile(r"^(?=.*(SCHOOL|EDUCATION|INSTRUCTION)).*(SUPERINTENDENT|\bSUPT\b|SUPER\. OF PUBLIC INSTRUCTION)")),
    ("commissioner of agriculture", re.compile(r"^((COMMISSIONER|SECRETARY) OF AGRICULTURE( AND INDUSTRIES)?|AGRICULTURE COMMISSIONER)$")),
    ("commissioner of insurance", re.compile(r"^(COMMISSIONER OF INSURANCE|INSURANCE COMMISSIONER)$")),
    ("commissioner of labor", re.compile(r"^(COMMISSIONER OF (LABOR|THE BUREAU OF LABOR AND INDUSTRIES)|LABOR COMMISSIONER)$")),
    ("commissioner of lands", re.compile(r"^(COMMISSIONER OF (PUBLIC|STATE|SCHOOL AND PUBLIC) LANDS|PUBLIC LANDS COMMISSIONER)$")),
    ("mine inspector", re.compile(r"^(STATE )?MINE INSPECTOR$")),   # PREFIX takes a leading 'STATE ' off first
]
# words that would name one of the listed offices somewhere in a longer name (to list what my whole-name reading leaves)
LOOSE = re.compile(r"TREASURER|AUDITOR|COMPTROLLER|CONTROLLER|SECRETARY OF|LIEUTENANT GOVERNOR|LT\.? GOV|ATTORNEY GENERAL|"
                   r"SUPERINTENDENT|COMMISSIONER|INSPECTOR|CHIEF FINANCIAL")


def my_office(office):
    o = PREFIX.sub("", " ".join(str(office or "").upper().split()))
    for name, pat in MY_OFFICES:
        if pat.search(o):
            return name
    return None


def section_2(after):
    print(f"### 35.2 the office rule read again by me, over every state-scope record at {AFTER}")
    state = {cid: c for cid, c in after.items() if c.get("office_scope") == "state" and cid.split("-")[1] in ("local", "primary")}
    typed = {cid for cid, c in state.items() if c.get("office_type") == "statewide officer"}
    print(f"  state-scope records (local and primary): {len(state)}; typed 'statewide officer': {len(typed)} (D3: 385 = 359 + 26)")
    mine = {}
    for cid, c in state.items():
        name = my_office(c.get("office"))
        d = (c.get("place") or {}).get("district")
        counties = (c.get("place") or {}).get("counties")
        if name and d in (None, "", "STATEWIDE") and (counties is None or len(counties) != 1):
            mine[cid] = name
    print(f"  by my reading of the ruling's list (the office's whole name, no district, not one county's): {len(mine)}; the same ids as the typed: {set(mine) == typed}"
          + ("" if set(mine) == typed else f"; mine not typed {sorted(set(mine) - typed)[:8]}; typed not mine {sorted(typed - set(mine))[:8]}"))
    print(f"  by office: {dict(collections.Counter(mine.values()).most_common())}")
    print("  D3's table: attorney general 71, secretary of state 66, treasurer or CFO 66, auditor 43, lieutenant governor 37, agriculture 19, insurance 19, comptroller 14, labor 14, lands 8, mine inspector 2 (359); plus 26 superintendents")
    # what the whole-name reading leaves among state-scope records that carry one of the words, and the rest
    left = collections.Counter()
    examples = collections.defaultdict(list)
    for cid, c in state.items():
        if cid in mine:
            continue
        o = " ".join(str(c.get("office") or "").upper().split())
        d = (c.get("place") or {}).get("district")
        counties = (c.get("place") or {}).get("counties")
        why = ("a district" if d not in (None, "", "STATEWIDE") else "one county's" if counties is not None and len(counties) == 1 else "whole state")
        if my_office(c.get("office")):
            k = f"a listed office, but {why}"
        elif LOOSE.search(o):
            k = "a listed office's word in a longer name" if why == "whole state" else f"a listed office's word in a longer name, {why}"
        elif c.get("office_type") == "judge":
            k = f"a judge ({why})"
        else:
            k = f"another office ({why}), typed {c.get('office_type')}"
        left[k] += 1
        if len(examples[k]) < 6 and (o, c["place"]["state"]) not in [(e[0], e[1]) for e in examples[k]]:
            examples[k].append((o, c["place"]["state"], c["year"]))
    print(f"  state-scope records my reading leaves ({sum(left.values())}):")
    for k, n in left.most_common():
        print(f"    {n:5d}  {k}: " + "; ".join(f"{o} ({st} {y})" for o, st, y in examples[k]))
    # the whole-state ones with a listed word in a longer name: every office name, for the eye (D3's 'counted for a ruling')
    names = collections.Counter(" ".join(str(c.get("office") or "").upper().split()) for cid, c in state.items()
                                if cid not in mine and LOOSE.search(" ".join(str(c.get("office") or "").upper().split()))
                                and (c.get("place") or {}).get("district") in (None, "", "STATEWIDE")
                                and ((c.get("place") or {}).get("counties") is None or len((c.get("place") or {}).get("counties")) != 1))
    print(f"  whole-state offices with a listed word in a longer name, untyped ({sum(names.values())}): {dict(names.most_common())}")
    print("  D3 counted for a ruling: 13 commission members by their commission's name, 10 Michigan board seats, 8 OHA trustees, NM's 3 PEC, DC's 3, 145 statewide-court judges, MT's clerk 2, DC's AG and Mayor, IL's 2 strays")
    # the three conditions on every typed record
    bad = [cid for cid in typed if (after[cid].get("place") or {}).get("district") not in (None, "", "STATEWIDE")
           or ((after[cid].get("place") or {}).get("counties") is not None and len(after[cid]["place"]["counties"]) == 1)]
    print(f"  typed records with a district or one county: {len(bad)} {bad[:5]}")
    return state, typed, mine


# ---------------------------------------------------------------------------------------------- 35.3
REASON_N = re.compile(r"fewer than 100 like races in earlier years in the sources taken in \((\d+)\) for the class '(.+)'$")


def pools_at(commit):
    """(MEDSL pool, NC pool): (year, class) rows from the records' own classes at the commit (a forecast's class, or
    the class a 'fewer than 100 like races' reason names; a write-in pair's structure rebuilt as c15 does), the pools
    drawn as c15.local_pools draws them: MEDSL's route and North Carolina's own (from 2014, every date, primaries too)"""
    files = C34.record_files(commit, ("local", "primary"))
    medsl, nc = [], []
    for f in files:
        d = C34.show(commit, f)
        level = f.split("/")[1]
        for c in (d or {}).get("contests", []):
            r = D.slim(level, d, c)
            reason = r["reason"] or ""
            cls = r["cls"]
            if cls is None and (reason.startswith("a write-in line is in the pair") or reason.startswith("no earlier year to fit on")):
                # the first year's races (2014 in North Carolina) name no class in their reason, yet the pipeline pools
                # them for the years after; a write-in pair's structure is rebuilt as c15 does
                if level == "primary":   # the State Board's primary classes (pipeline/local_ncsbe.py nc_key, copied: by
                    b = C15.ballot_local(r)   # office type and candidates, seats at the end where more than one)
                    k = r["seats"] or 1
                    if len(b) > k:
                        cls = f"primary, {r['office_scope']} {r['office_type']}, {len(b) if len(b) < 4 else '4+'} candidates" + (f", {k} seats" if k > 1 else "")
                else:
                    st = C15.structure_local(r, nc=(r["state"] == "NC" and not C15.medsl_route(r)))
                    cls = st[1] if st[0] in ("class", "boundary", "partisan") else None
            if not cls:
                continue
            if level == "primary":
                nc.append((r["year"], cls, r["id"]))
            elif C15.medsl_route(r):
                medsl.append((r["year"], cls, r["id"]))
            if r["state"] == "NC" and r["year"] >= C15.NC_FIRST and level == "local":
                nc.append((r["year"], cls, r["id"]))
    return medsl, nc


def count_like(pool, cls, year):
    return sum(1 for y, k, _ in pool if k == cls and y < year)


def section_3(before, after, mv):
    print("### 35.3 the 50 changed reasons: their counts of like races against my own counts from each commit's records")
    R = [r for r in mv["records"] if r[8] == ["R"]]
    TR = [r for r in mv["records"] if r[8] == ["T", "R"]]
    print(f"  rows coded R alone: {len(R)} (D3: 50); T and R: {len(TR)} (D3: 69); every R reason of the 'fewer than 100 like races (N) for the class' shape: "
          f"{all(REASON_N.search(r[5]) and REASON_N.search(r[6]) for r in R)}")
    pb_m, pb_nc = pools_at(BEFORE)
    pa_m, pa_nc = pools_at(AFTER)
    print(f"  pools: MEDSL's route {len(pb_m)} -> {len(pa_m)} class rows; North Carolina's own {len(pb_nc)} -> {len(pa_nc)}")
    tal = collections.Counter()
    for r in R + TR:
        cid = r[0]
        mb, ma = REASON_N.search(r[5] or ""), REASON_N.search(r[6] or "")
        if not ma:
            tal["after: not a like-races reason"] += 1
            continue
        year = int(cid[:4])
        level = cid.split("-")[1]
        is_nc = level == "primary" or (cid.split("-")[2] == "NC" and not C15.medsl_route(D.slim(level, {}, after[cid])))
        n_after = count_like(pa_nc if is_nc else pa_m, ma.group(2), year)
        ok_a = n_after == int(ma.group(1))
        if mb:
            n_before = count_like(pb_nc if is_nc else pb_m, mb.group(2), year)
            ok_b = n_before == int(mb.group(1))
        else:
            ok_b = None
        key = ("R" if r[8] == ["R"] else "T,R") + (": before and after equal" if ok_a and ok_b else ": after equal" if ok_a and ok_b is None else
                                                  f": DIFFERS (before {ok_b}, after {ok_a})")
        tal[key] += 1
        if not ok_a or ok_b is False:
            print(f"    {cid[:70]}: record {mb.group(1) if mb else '-'} -> {ma.group(1)}; mine {n_before if mb else '-'} -> {n_after} for '{ma.group(2)}'"
                  + ("" if mb is None or mb.group(2) == ma.group(2) else f" (before: '{mb.group(2)}')"))
    print(f"  {dict(tal)}")
    classes = collections.Counter((re.search(r"for the class '(.+)'", r[6]).group(1) if re.search(r"for the class '(.+)'", r[6]) else r[6][:50]) for r in TR)
    print(f"  the T,R rows' new classes: {dict(classes.most_common(8))}")
    other = collections.Counter(r[6][:60] for r in mv["records"] if "T" in r[8] and "R" not in r[8] and isinstance(r[6], str))
    print(f"  the T rows without R, their unchanged reasons (shapes): {dict(other.most_common(6))}")


# ---------------------------------------------------------------------------------------------- 35.4
def section_4(before, after, mv):
    print("### 35.4 no p moved")
    T = [r for r in mv["records"] if "T" in r[8]]
    with_p = [r for r in T if isinstance(r[5], (int, float))]
    print(f"  of the {len(T)} T rows, with a p value: {len(with_p)} (D3: 40); p after equal to p before in {sum(1 for r in with_p if r[5] == r[6])}; "
          f"their p: {dict(collections.Counter('0 (unopposed)' if r[5] == 0 else 'a Democrat against a Republican' for r in with_p))}")
    for name in ("data/local/backtest-local-partisan.json", "data/local/calibration-local.json"):
        b, a = C34.show(BEFORE, name), C34.show(AFTER, name)
        print(f"  {name}: changed {b != a}; top-level keys that differ: {[k for k in sorted(set(b) | set(a)) if b.get(k) != a.get(k)]} (no verdict read)")


def main():
    print(f"##### c35 single-seat statewide executive offices typed statewide officer (#87): HEAD {L.git_head()}")
    before, after, mv = section_1()
    section_2(after)
    section_3(before, after, mv)
    section_4(before, after, mv)


if __name__ == "__main__":
    main()
