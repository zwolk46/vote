"""c48: the eighth pass's section 19, second part: D3's #109 (main b35fede; data/local/REPORT.md section 35) against
b350d5e, the district checks' third pass (moves-district-checks-3.json) and check-volume's DC ballots.

The orchestrator, 2026-11-13 07:38 UTC (the brief is quoted whole in c47): "... Senate 36 on MEDSL; the 0.4% two-witness
rule (6 IN 2016 records, House 75 back); over-seats on every covered record (Grand Isle, Windham and Rutland on MEDSL; IN 2018
untested for want of rows); the zero-row counties (IN 2022 House 23 and 66, KY 2016 House 28); 107 spelling pairs; DC at
231,700. My compare against main: 1 lost, 9 gained, 14,997 moved, none over 2x."

Sections (each from my own reading of MEDSL's raw files (one pass each, cached), Indiana's 2016 archive and Utah's 2016
canvass (fetched in section 18), the DC Board's certified PDF, and the records at the two commits; nothing from pipeline/
imported; a rule of the build that must be applied is copied here and says so):
  48.1  moves-district-checks-3.json against my own diff of every D3 record, b350d5e -> b35fede (c46's pattern); the 9 new
        p and the p beyond 1%
  48.2  Indiana 2016: Senate 36 on MEDSL's count; the settle test by candidate (D3's settle_agree copied) and the 0.4%
        two-witness rule (two_against_state copied) on every Indiana 2016 record, against D3's flags; Utah 2016's canvass
  48.3  the spelling pairs: D3's _spelled_alike and _given copied on my MEDSL legislative contests of 2016, 2018 and 2022;
        each line's precincts from the raw files; summed or not, against D3's list; the summed votes in the records
  48.4  over-seats on every record: D3's district_ballots copied (a precinct's ballots: its most votes in a statewide
        one-seat contest with rows in 90% of the state's precincts) on every record of 2016, 2018 and 2022 at b350d5e
        (Klarner's count, D3's matcher), against D3's over list and his flags' figures; Indiana 2018's Washington County
  48.5  the zero-row counties: Indiana 2022's Cass, Daviess, Scott and Monroe, Kentucky 2016's Jefferson, from the raw
        files; the records' outcomes
  48.6  DC 2018: check-volume.json's DC rows at the Board's 231,700 (the certified PDF read apart); the wards
  48.7  New York 2018's at-large reasons (84.53%, 73.51%) from MEDSL's governor lines; the forecast inputs behind the p
        moved beyond 1%
[measured] throughout unless marked; D3's words [stated].
Run from the repository root: python3 -I checks/m2/c48_district_checks_3.py [1 2 3 4 5 6 7]
"""
import collections
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402
import m2medsl as M  # noqa: E402
import c40_pr_checks as C40  # noqa: E402
import c41_governor_refit as C41  # noqa: E402
import c42_held_totals as C42  # noqa: E402
import c43_district_checks as C43  # noqa: E402
import c46_district_checks_2 as C46  # noqa: E402

BEFORE, AFTER = "b350d5e", "b35fede"
SRC = os.path.join(L.CACHE, "eighth", "src")
DERIVED = os.path.join(L.CACHE, "eighth", "derived")
YEARS = (2016, 2018, 2022)
RATIO_OFF = 0.03       # D3's RATIO_OFF, copied
TWO_AGREE = 0.004      # D3's TWO_AGREE, copied (the orchestrator, 2026-11-13 05:15 (3))
OVER_SEATS = 1.10      # D3's OVER_SEATS, copied
OVER_SEATS_MEDSL = 1.0   # D3's OVER_SEATS_MEDSL, copied
STATEWIDE_SPREAD = 0.9   # D3's STATEWIDE_SPREAD, copied
TOP_OFFICES = {"PRESIDENT", "US PRESIDENT", "US SENATE", "U.S. SENATE", "GOVERNOR"}   # D3's TOP_OFFICES, copied
NOT_GIVEN = {"JR", "SR", "II", "III", "IV", "MR", "MRS", "MS", "DR"}   # D3's, copied
NOT_PERSON = re.compile(r"\d|\bVOTES?\b|QUALIFIED", re.I)   # D3's, copied
ZERO_COUNTIES = {(2022, "IN"): {"18017", "18027", "18143", "18105"}, (2016, "KY"): {"21111"}}
IN_2018_FILE = "2018-in-precinct-general.zip"


def h1(s):
    print("\n" + "=" * 100 + f"\n{s}\n" + "=" * 100)


def at(commit, rel):
    return os.path.join(C41.worktree(commit), rel)


def records_at(commit, f):
    return C42.records_at(C41.worktree(commit), f)


def record_of(kid, commit=AFTER):
    return C46.record_of(kid, commit)


def pval(c):
    return C40.pval(c)


def dkey(d):   # D3's _dkey, copied: the district's number without zeros, else the string in capitals
    d = (d or "").strip().upper()
    return C43.dno_of(d) or d


def fips5(x):   # D3's P.fips5, copied: five digits, a leading zero where the file dropped it
    s = str(x or "").strip()
    if s.endswith(".0"):
        s = s[:-2]
    return s.zfill(5) if s.isdigit() else s


def ivotes(r):
    try:
        return int(float(r.get("votes") or 0))
    except ValueError:
        return 0


# ------------------------------------------------------------------------------------------ 48.1 the moves file

def section_1():
    h1(f"48.1 moves-district-checks-3.json against my own diff of every D3 record, {BEFORE} -> {AFTER}")
    mv = L.load_json(at(AFTER, "data/local/moves-district-checks-3.json"))
    rows = {}
    for r in mv["records"]:
        rows.setdefault(r[0], []).append(r)
    print(f"  the file: {len(mv['records']):,} rows, {len(rows):,} ids, against {mv.get('against')} (the code alone, its data main's at 72d1d60, which equal {BEFORE}'s D3 files; my diff is main to main)")
    print(f"  its summary: {json.dumps(mv['summary'])}")
    files = subprocess.run(["git", "diff", "--name-only", BEFORE, AFTER, "--", "data/"], capture_output=True, text=True, cwd=L.ROOT).stdout.split()
    data_files = [f for f in files if re.match(r"^data/(local|primary|measure|state-lower|state-upper)/\d{4}/[A-Z]{2}\.json$", f)]
    d2_files = [f for f in files if re.match(r"^data/(governor|house|senate|president)/\d{4}\.json$", f)]
    print(f"  data files changed: {len(files)}; D3's record files: {len(data_files)} {dict(collections.Counter(f.split('/')[1] for f in data_files))}; D2's: {len(d2_files)} (c47); "
          f"other: {[f for f in files if f not in data_files and f not in d2_files]}")
    mine = collections.Counter()
    agree, dis, seen, worst, stamps, pdiff, rdiff = 0, collections.Counter(), set(), [], 0, 0, 0
    within = collections.Counter()
    moved, new_p, lost_p = [], [], []
    for f in data_files:
        lv, yr = f.split("/")[1], f.split("/")[2]
        b, a = records_at(BEFORE, f), records_at(AFTER, f)
        for i in sorted(set(b) | set(a)):
            code = C40.my_code(b.get(i), a.get(i))
            if not code:
                continue
            d = C40.what_differs(b.get(i) or {}, a.get(i) or {})
            if tuple(d) == ("p.commit",):
                stamps += 1
                continue
            c = code[0]
            if c in ("B", "Q", "O", "R") and any((b.get(i) or {}).get(k) != (a.get(i) or {}).get(k) for k in ("type", "office_type")):
                c = "T"
            pb, pa = pval(b.get(i) or {}), pval(a.get(i) or {})
            if c == "P":
                moved.append((pa / pb if pb else None, i, lv, yr))
                other = [x for x in d if not (x.startswith("p.") or x.startswith("forecasts") or x.startswith("forecast_inputs") or x in ("p", "two_party"))]
                if pb and abs(pa / pb - 1) <= 0.01 and not other:
                    within[(lv, yr)] += 1
                    seen.add(i)
                    continue
            if c == "N":
                new_p.append((i, pa, (a.get(i) or {}).get("p", {}).get("under"), str((b.get(i) or {}).get("p", {}).get("not_computed"))[:80]))
            if c == "L":
                lost_p.append((i, pb))
            mine[(lv, c)] += 1
            seen.add(i)
            hits = rows.get(i)
            if not hits:
                worst.append((i, c, "not in the moves file", d[:6]))
                continue
            theirs = set()
            for row in hits:
                theirs |= set(row[8])
            ok = c in theirs or (c in ("Q", "O", "B", "R") and theirs & {"Q", "O", "R", "B"})
            if ok:
                agree += 1
            else:
                dis[(lv, c, tuple(sorted(theirs)))] += 1
                worst.append((i, c, tuple(sorted(theirs)), d[:6]))
            for row in hits:
                if isinstance(row[5], str) or isinstance(row[6], str):
                    continue
                if (row[5] is None) != (pb is None) or (row[6] is None) != (pa is None) \
                        or (pb is not None and abs(row[5] - pb) > 1e-9 * max(abs(pb), 1e-300)) \
                        or (pa is not None and abs(row[6] - pa) > 1e-9 * max(abs(pa), 1e-300)):
                    pdiff += 1
                    if pdiff <= 5:
                        print(f"    p before/after differ from the record: {i} row {row[5]} {row[6]} record {pb} {pa}")
                if pb and pa and row[7] is not None and abs(row[7] - round(pa / pb, 4)) > 1.5e-4:
                    rdiff += 1
                    if rdiff <= 5:
                        print(f"    ratio differs: {i} row {row[7]} mine {pa / pb:.4f}")
    not_mine = [i for i in rows if i not in seen]
    print("  my diff, by level and code (p moved within 1% and nothing else counted apart): " + "; ".join(f"{lv} {k} {v}" for (lv, k), v in sorted(mine.items())))
    print(f"  rows whose code I share: {agree} of {len(seen) - sum(within.values())} ids listed in my diff; codes differing: {sum(dis.values())}; "
          f"ids in my diff but not in the file: {len([w for w in worst if w[2] == 'not in the moves file'])}; ids in the file but not in my diff: {len(not_mine)} {not_mine[:5]}")
    print(f"  p before/after other than the record's: {pdiff}; ratios off by more than 1.5e-4: {rdiff}; records differing in p.commit alone: {stamps}")
    for (lv, c, theirs), v in sorted(dis.items(), key=lambda kv: -kv[1])[:10]:
        ex = [w for w in worst if w[1] == c and w[2] == theirs][:2]
        print(f"    mine {c} theirs {theirs} {lv}: {v}; e.g. " + "; ".join(f"{e[0]} differs in {e[3]}" for e in ex))
    for w in [w for w in worst if w[2] == "not in the moves file"][:8]:
        print(f"    not in the file: {w[0]} mine {w[1]} differs in {w[3]}")
    print(f"  p moved within 1% and nothing else, by level and year (mine; the file lists every P row apart): {sum(within.values())} in {len(within)} cells: "
          + "; ".join(f"{lv} {yr} {v}" for (lv, yr), v in sorted(within.items())))
    mv_all = [m for m in moved if m[0] is not None]
    over2 = [m for m in mv_all if m[0] > 2 or m[0] < 0.5]
    print(f"  p moved (every P in my diff): {len(mv_all)}; over 2x either way: {len(over2)} {over2[:5]}; extremes: min {min(mv_all)[0]:.4f} {min(mv_all)[1]}, max {max(mv_all)[0]:.4f} {max(mv_all)[1]}")
    bands = collections.Counter()
    for r_, i, lv, yr in mv_all:
        bands["within 0.1%" if abs(r_ - 1) <= 0.001 else "0.1-1%" if abs(r_ - 1) <= 0.01 else "1-10%" if abs(r_ - 1) <= 0.1 else "beyond 10%"] += 1
    print(f"  bands: {dict(bands)}; the file's P rows: {len([r for r in mv['records'] if 'P' in r[8]]):,} (the orchestrator: 14,997 moved in all, 14,525 here)")
    beyond = sorted([m for m in mv_all if abs(m[0] - 1) > 0.01], key=lambda m: m[0])
    print(f"  beyond 1%: {len(beyond)} (D3's message: 14): " + "; ".join(f"{i} x{r_:.4f}" for r_, i, lv, yr in beyond))
    print(f"  new p ({len(new_p)}; the orchestrator: 9 gained): " + "; ".join(f"{i} {pa:.3e} ({str(u)[:30]}; was: {w})" for i, pa, u, w in sorted(new_p)))
    print(f"  p lost ({len(lost_p)}): {lost_p}")
    # the forecast inputs behind the moves beyond 1%
    print("  the moves beyond 1%: what else changed in the record")
    for r_, i, lv, yr in beyond:
        f = f"data/{lv}/{yr}/{i.split('-')[3] if lv.startswith('state') else i.split('-')[2]}.json"
        b, a = records_at(BEFORE, f).get(i), records_at(AFTER, f).get(i)
        d = C40.what_differs(b, a)
        fi_b, fi_a = b.get("forecast_inputs") or {}, a.get("forecast_inputs") or {}
        fid = {k: (fi_b.get(k), fi_a.get(k)) for k in set(fi_b) | set(fi_a) if fi_b.get(k) != fi_a.get(k) and not isinstance(fi_b.get(k), dict)}
        print(f"    {i}: x{r_:.4f}; differs in {[x for x in d if not x.startswith('p.')][:6]}; forecast inputs changed: {json.dumps(fid)[:300]}; votes before {[(c['name'], c['votes']) for c in b['result']['candidates']][:3]} "
              f"after {[(c['name'], c['votes']) for c in a['result']['candidates']][:3]}; n {b['p'].get('n')} -> {a['p'].get('n')}")
    return mv


# ------------------------------------------------------------------------------------------ 48.2 Indiana 2016

def within(a, b, tol):   # D3's _within, copied
    return (not a and not b) or (bool(b) and abs((a or 0) / b - 1) <= tol)


def state_pairs(cands, state_cands):
    """D3's _state_pairs, copied: Klarner's ballot candidates paired with the state's by surname (name_key against name_keys,
    _finds), each once, the state naming no other ballot candidate: [[Klarner's name, votes, the state's name, votes]] or None."""
    ballot = C46.on_ballot(cands)
    sb = [x for x in state_cands if not x["write_in"]]
    pairs = []
    for a in ballot:
        hit = [x for x in sb if C46.finds(C46.name_key(a["name"]), C46.name_keys(x["name"]))]
        if len(hit) != 1:
            return None
        pairs.append([a["name"], a["votes"], hit[0]["name"], hit[0]["votes"]])
    return pairs if len(sb) == len(ballot) else None


def settle_agree(cands, state_cands, medsl_pairs):
    """D3's settle_agree, copied: each candidate's state count within RATIO_OFF of Klarner's (Klarner's count stands, 'klarner'),
    or else of MEDSL's with every candidate paired (MEDSL's count stands, 'medsl'); None where neither."""
    pairs = state_pairs(cands, state_cands)
    if not pairs:
        return None
    if all(within(p_[3], p_[1], RATIO_OFF) for p_ in pairs):
        return {"with": "klarner", "pairs": pairs}
    med = {p_[0]: p_[3] for p_ in medsl_pairs}
    if set(med) != {p_[0] for p_ in pairs} or not all(med[p_[0]] for p_ in pairs):
        return None
    if all(within(p_[3], med[p_[0]], RATIO_OFF) for p_ in pairs):
        return {"with": "medsl", "pairs": [[p_[0], p_[1], med[p_[0]], p_[2], p_[3]] for p_ in pairs]}
    return None


def two_against_state(cands, state_cands, medsl_pairs, matched):
    """D3's two_against_state, copied: Klarner's and MEDSL's counts within TWO_AGREE of each other for every candidate, the
    state's (unmarked) off Klarner's by more than TWO_AGREE for one or more."""
    if not matched:
        return None
    pairs = state_pairs(cands, state_cands)
    if not pairs:
        return None
    med = {p_[0]: p_[3] for p_ in medsl_pairs}
    if set(med) != {p_[0] for p_ in pairs}:
        return None
    if not all(within(med[p_[0]], p_[1], TWO_AGREE) for p_ in pairs):
        return None
    if all(within(p_[3], p_[1], TWO_AGREE) for p_ in pairs):
        return None
    return [[p_[0], p_[1], med[p_[0]], p_[2], p_[3]] for p_ in pairs]


def section_2():
    h1("48.2 Indiana 2016: Senate 36 on MEDSL's count; the settle test by candidate and the 0.4% two-witness rule on every record, against D3's flags")
    arch = C46.in_archive()
    print(f"  the archive (my copy, section 18): {len([k for k in arch if k[0] == 1])} Senate and {len([k for k in arch if k[0] == 0])} House contests; its settings have no 'Certified' field "
          f"[measured in section 18: D3's STATE_MARKED (IN, 2016) False]")
    chk = L.load_json(at(AFTER, "data/local/check-districts.json"))
    chk_b = L.load_json(at(BEFORE, "data/local/check-districts.json"))
    flags = {f["id"]: f for f in chk["years"]["2016"]["flags"] if f["id"].startswith("2016-IN-")}
    flags_b = {f["id"]: f for f in chk_b["years"]["2016"]["flags"] if f["id"].startswith("2016-IN-")}
    print(f"  D3's Indiana 2016 flags: {len(flags)} {dict(collections.Counter(f['outcome'] for f in flags.values()))}; at {BEFORE}: {dict(collections.Counter(f['outcome'] for f in flags_b.values()))}")
    tas = chk["years"]["2016"].get("two_against_state") or []
    print(f"  D3's two_against_state list: {[(x['id'], x['outcome']) for x in tas]}")
    # Senate 36
    for kid in ("2016-IN-upper--36--",):
        b, a = record_of(kid, BEFORE), record_of(kid, AFTER)
        m = C46.d3_match(b, merged_pool(2016, "IN"))
        print(f"  Senate 36 (the pool with my spelling decisions applied: MEDSL's 'JACK SANDLIN' and 'JACK E. SANDLIN' lines, 4,676 and 22,034 in my volume summary): before {[(c['name'], c['votes']) for c in b['result']['candidates']]} (source {b['result'].get('source')}, votes_source {b['result'].get('votes_source')}); "
              f"after {[(c['name'], c['votes']) for c in a['result']['candidates']]} (votes_source {a['result'].get('votes_source')}); p {pval(b)} -> {pval(a)} (x{pval(a) / pval(b):.4f}); n {b['p'].get('n')} -> {a['p'].get('n')}")
        print(f"    my MEDSL pairs: {m.get('pairs')}; ratio {m.get('ratio')}; the archive: {arch.get((1, '36'))}")
        print(f"    D3's flag: outcome {flags.get(kid, {}).get('outcome')}; pairs {flags.get(kid, {}).get('pairs')}; note: {[n for n in a.get('notes', []) if 'state' in n][:1]}"[:900])
    # every Indiana 2016 record
    tal = collections.Counter()
    two_mine = []
    settle_rows = []
    detail = {}
    for lv, sen in (("state-lower", 0), ("state-upper", 1)):
        recs_b = records_at(BEFORE, f"data/{lv}/2016/IN.json")
        recs_a = records_at(AFTER, f"data/{lv}/2016/IN.json")
        pool = merged_pool(2016, "IN")
        for rid, b in sorted(recs_b.items()):
            a = recs_a.get(rid)
            dno = C43.dno_of(b["place"]["district"].split(",")[0])
            sc = arch.get((sen, dno))
            if sc is None:
                tal["no archive contest"] += 1
                continue
            state_cands = [{"name": n, "votes": v, "write_in": w} for n, v, w in sc]
            cands = C46.rec_cands(b)
            m = C46.d3_match(b, pool)
            mp = [(p_[0], p_[1], p_[2], p_[3]) for p_ in m.get("pairs", [])] if m.get("matched") else []
            kid = f"2016-IN-{'upper' if sen else 'lower'}--{dno}--"
            fl = flags.get(kid)
            st_ = settle_agree(cands, state_cands, mp)
            two = two_against_state(cands, state_cands, mp, m.get("matched"))
            if two:
                two_mine.append((kid, two, fl["outcome"] if fl else "not flagged"))
            if two or kid in {x["id"] for x in tas}:
                detail[kid] = (m.get("matched"), mp, [(n, v) for n, v, w in sc], st_, two is not None)
            if fl is not None:
                settle_rows.append((kid, fl["outcome"], fl.get("ratio"), (st_ or {}).get("with"), two is not None, m.get("flag_a"), m.get("flag_b")))
                tal[("flagged", fl["outcome"][:45], "settle by candidate: " + str((st_ or {}).get("with")))] += 1
            else:
                tal[("not flagged", "settle by candidate: " + str((st_ or {}).get("with")), "my flag_a" if m.get("flag_a") else "")] += 1
    print(f"\n  every Indiana 2016 record, the settle test by candidate (D3's settle_agree copied) and D3's flags:")
    for k, v in sorted(tal.items(), key=str):
        print(f"    {str(k):110s} {v}")
    print(f"  the flagged records, D3's outcome beside my settle-by-candidate result (klarner: the state agrees with Klarner on every candidate; medsl: with MEDSL; None: neither):")
    for row in sorted(settle_rows):
        kid, out, ratio, w, two, fa, fb = row
        exp = {"klarner": "settled by the state: Klarner's count stands", "medsl": "settled by the state: MEDSL's count stands"}.get(w)
        agree = (exp is not None and out.startswith(exp)) or (exp is None and not out.startswith("settled by the state")) or (two and out.startswith("two counts"))
        print(f"    {kid:26s} D3 {out[:58]:58s} ratio {ratio!s:8s} mine {str(w):8s} two_against {str(two):5s} {'ok' if agree else 'DIFFERS'}")
    print(f"\n  the two-witness rule (two_against_state copied) on every record: mine {len(two_mine)} {[(k, o) for k, _, o in two_mine]}; D3's {len(tas)}; same set: "
          f"{ {k for k, _, _ in two_mine} == {x['id'] for x in tas} }")
    for kid in sorted(set(detail)):
        matched, mp, sc, st_, two = detail[kid]
        print(f"    {kid}: {'mine too' if two else 'D3 alone'}; matched {matched}; MEDSL pairs {mp}; the state's {sc}; settle {(st_ or {}).get('with')}")
    # House 75, 38, 39
    for kid in ("2016-IN-lower--75--", "2016-IN-lower--38--", "2016-IN-lower--39--"):
        b, a = record_of(kid, BEFORE), record_of(kid, AFTER)
        print(f"  {kid}: p {pval(b)} -> {pval(a)}; D3's outcome {flags.get(kid, {}).get('outcome')} (before {flags_b.get(kid, {}).get('outcome')}); after's reason/note: "
              f"{str(a['p'].get('not_computed') or a['p'].get('reason'))[:120]} | {[n[:200] for n in a.get('notes', []) if 'state' in n.lower()][:1]}")
    # Utah 2016
    tot = C46.ut_canvass_totals()
    ut_flags = [f for f in chk["years"]["2016"]["flags"] if f["id"].startswith("2016-UT-")]
    print(f"\n  Utah 2016 (the canvass's multi-county Senate page, TOTAL row by name: {tot}); D3's Utah flags: {[(f['id'], f['outcome']) for f in ut_flags]}")
    for f in ut_flags:
        kid = f["id"]
        b = record_of(kid, BEFORE)
        if b is None:
            continue
        hits = []
        for x in b["result"]["candidates"]:
            h = [(n, v) for n, v in tot.items() if C46.surname_match(x["name"], n)]
            hits.append((x["name"], x["votes"], h, [round(v / x["votes"] - 1, 4) for _, v in h] if x["votes"] else None))
        print(f"    {kid}: {hits}")


# ------------------------------------------------------------------------------------------ the raw-file pass (48.3-48.5)

def given(name):   # D3's _given, copied
    n = re.sub(r'"+', '"', name.upper())
    toks = set()
    for a, b, c in re.findall(r"\(([^)]*)\)|\"([^\"]*)\"|'([^']*)'", n):
        toks |= set(re.findall(r"[A-Z]{2,}", a or b or c))
    rest = re.sub(r"\([^)]*\)|\"[^\"]*\"|'[^']*'", " ", n)
    rest = rest.split(",", 1)[1] if "," in rest else " ".join(rest.split()[:-1])
    return (toks | set(re.findall(r"[A-Z]{2,}", rest))) - NOT_GIVEN


def spelled_alike(a, b):   # D3's _spelled_alike, copied (surs: local_medsl.name_keys' surnames, c46's copy; generic: c46's copy)
    if " ".join(a["name"].upper().split()) == " ".join(b["name"].upper().split()):
        return False
    if any(C46.generic(x) or NOT_PERSON.search(x["name"]) or not x["name"].strip() for x in (a, b)):
        return False
    return bool(C46.surs(a["name"]) & C46.surs(b["name"])) and bool(given(a["name"]) & given(b["name"]))


def spell_key(st, sen, district, name):   # D3's _spell_key, copied
    return f"{st}|{sen}|{dkey(district)}|{' '.join(name.upper().split())}"


def states_with_records(year):
    out = set()
    for lv in ("state-lower", "state-upper"):
        d = at(AFTER, f"data/{lv}/{year}")
        if os.path.isdir(d):
            out |= {n[:2] for n in os.listdir(d) if re.fullmatch(r"[A-Z]{2}\.json", n)}
    return out


def leg_office(office, district):
    """(sen, district) where the row's office is a legislature's (D3's relabel: LEG, LEG_NAMES, Washington's filed names), else None."""
    o = (office or "").strip().upper()
    x = C43.WA_LEG.match(o)
    if x:
        return (1 if x.group(2) == "SENATOR" else 0), x.group(1)
    if o in C43.LEG_NAMES:
        return C43.LEG_NAMES[o], district
    return None


def statewide_one_seat(r, office):   # D3's _statewide_one_seat, copied
    dv = (r.get("dataverse") or "").strip().upper()
    if not dv:
        return office in TOP_OFFICES
    if dv in ("PRESIDENT", "SENATE"):
        return True
    return dv == "STATE" and (r.get("district") or "").strip().upper() == "STATEWIDE" and (r.get("magnitude") or "1").strip() in ("1", "1.0")


def raw_files(year):
    out = []
    for y, p in M.all_raw_files():
        if y != year:
            continue
        if year == 2016 and not os.path.basename(p).endswith("precinct-state.csv"):
            continue
        out.append(p)
    return out




SPELL_OFFICE = re.compile(r"STATE (HOUSE|SENATE|REPRESENTATIVE|SENATOR|ASSEMBLY)|GENERAL ASSEMBLY")   # D3's spelling_precincts' filter, copied


def precinct_pass(path, year, want_spell, want_counties):
    """One pass over a raw MEDSL file, D3's district_ballots' reading copied (stage GEN, not special; a precinct key of county
    fips5, jurisdiction_fips or jurisdiction, precinct; meta names, rows named as totals and NOT_A_CONTEST offices skipped;
    votes > 0 mark a county as voted): for every legislative district (st|sen|dkey) its precincts; for every statewide one-seat
    contest its votes by precinct, TOTAL and the other modes apart; the counties with rows and with votes. Beside it, D3's
    spelling_precincts' reading copied (its own office filter, the raw precinct key county_fips|jurisdiction_fips or
    jurisdiction|precinct, every row, by mode) for the spelling lines wanted; and the rows of the counties wanted (48.5).
    Cached in DERIVED by the file's size and mtime and the wants."""
    os.makedirs(DERIVED, exist_ok=True)
    stt = os.stat(path)
    cache = os.path.join(DERIVED, f"p19-{os.path.basename(path)}.json")
    stamp = {"size": stt.st_size, "mtime": int(stt.st_mtime), "spell": sorted(want_spell), "counties": sorted(want_counties), "version": 4}
    if os.path.exists(cache):
        d = L.load_json(cache)
        if d.get("stamp") == stamp:
            return d
    leg = collections.defaultdict(set)
    tot = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    oth = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    seen, voted = collections.defaultdict(set), collections.defaultdict(set)
    spell = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    crows = collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0, set()]))
    n = 0
    for r in M.rows(path):
        n += 1
        st = r.get("state_po") or r.get("state_postal") or ""
        if (r.get("stage") or "").upper() != "GEN" or (r.get("special") or "").strip().upper() == "TRUE":
            continue
        office = (r.get("office") or "").strip().upper()
        cand = (r.get("candidate") or "").strip()
        prec = r.get("precinct") or ""
        v = ivotes(r)
        if want_spell and SPELL_OFFICE.search(office):   # D3's spelling_precincts, copied: every row of the line, by mode
            k = spell_key(st, 1 if "SENAT" in office else 0, r.get("district"), cand)
            if k in want_spell:
                pk = "|".join(str(x or "") for x in (r.get("county_fips"), r.get("jurisdiction_fips") or r.get("jurisdiction"), prec))
                spell[k][pk][(r.get("mode") or "TOTAL").upper()] += v
        county = fips5(r.get("county_fips") or "")
        if (st, county) in want_counties:
            e = crows[f"{st}|{county}"][f"{office}|{C43.dno_of(r.get('district')) or (r.get('district') or '').strip()}"]
            e[0] += 1
            e[1] += v
            e[2].add(prec)
        seen[st].add(county)
        if M.is_meta(cand) or C43.AGG_NAME.search(prec) or C43.COUNTY_TOTAL.search(prec.strip().upper()):
            continue
        if C43.NOT_A_CONTEST.search(office):
            continue
        if v > 0:
            voted[st].add(county)
        pk = f"{county}|{' '.join((r.get('jurisdiction_fips') or r.get('jurisdiction') or '').upper().split())}|{' '.join(prec.upper().split())}"
        lo = leg_office(office, r.get("district") or "")
        if lo is not None:
            sen, dist = lo
            leg[f"{st}|{sen}|{dkey(dist)}"].add(pk)
            continue
        if cand.upper() in C43.ANSWERS or not statewide_one_seat(r, office):
            continue
        key = f"{office}|{(r.get('district') or '').strip()}"
        (tot if (r.get("mode") or "").strip().upper() == "TOTAL" else oth)[st][key][pk] += v
    out = {"stamp": stamp, "rows": n,
           "leg": {k: sorted(v) for k, v in leg.items()},
           "tot": {st: {k: dict(c) for k, c in d.items()} for st, d in tot.items()},
           "oth": {st: {k: dict(c) for k, c in d.items()} for st, d in oth.items()},
           "seen": {st: sorted(v) for st, v in seen.items()}, "voted": {st: sorted(v) for st, v in voted.items()},
           "spell": {k: {pk: dict(m) for pk, m in d.items()} for k, d in spell.items()},
           "county_rows": {k: {kk: [e[0], e[1], len(e[2])] for kk, e in d.items()} for k, d in crows.items()}}
    with open(cache, "w") as f:
        json.dump(out, f)
    return out


def district_ballots(d, st, keys):
    """D3's district_ballots' second half, copied: a precinct's votes in a contest are its TOTAL mode's or its other modes' sum,
    whichever is more; a statewide contest is 'wide' with rows in STATEWIDE_SPREAD of the state's precincts with any; a
    district's ballots = the sum over its precincts of the most votes in a wide contest; left out where a precinct has none.
    {key: [precincts, ballots, the wide contests reaching the district]}."""
    tot, oth = d["tot"].get(st, {}), d["oth"].get(st, {})
    ks = set(tot) | set(oth)
    votes = {k: {q: max(tot.get(k, {}).get(q, 0), oth.get(k, {}).get(q, 0)) for q in set(tot.get(k, {})) | set(oth.get(k, {}))} for k in ks}
    allp = set().union(*[set(v) for v in votes.values()]) if votes else set()
    wide = [k for k in ks if allp and len(votes[k]) >= STATEWIDE_SPREAD * len(allp)]
    out = {}
    for k in keys:
        ps = d["leg"].get(k)
        if not ps or not wide:
            continue
        b = [max(votes[c].get(q, 0) for c in wide) for q in ps]
        if all(b):
            out[k] = [len(ps), sum(b), sorted({c.split("|")[0] for c in wide if any(votes[c].get(q) for q in ps)})]
    return out, wide, len(allp)


_PASSES = {}


def passes(year):
    """The pass over every raw file of the year, with the year's spelling lines and zero-row counties wanted; {path: result}."""
    if year in _PASSES:
        return _PASSES[year]
    want_spell = frozenset(spell_key(st, sen, dist, x["name"]) for st, sen, dist, a, b, _ in spelling_pairs(year) for x in (a, b))
    want_counties = frozenset((st, c) for (y, st), cs in ZERO_COUNTIES.items() if y == year for c in cs)
    out = {}
    for p in raw_files(year):
        out[p] = precinct_pass(p, year, want_spell, want_counties)
    _PASSES[year] = out
    return out


# ------------------------------------------------------------------------------------------ 48.3 the spellings

def spelling_pairs(year):
    """Every pair of lines spelled alike in my MEDSL legislative contests of the year (c43's pool, every state with records):
    [(st, sen, district, a, b, file)]."""
    out = []
    for st in sorted(states_with_records(year)):
        for m in C43.leg_contests(year, st):
            cs = [{"name": n, "votes": v} for n, v in m["cands"].items()]
            for i, a in enumerate(cs):
                for b in cs[i + 1:]:
                    if spelled_alike(a, b):
                        out.append((st, m["sen"], m["district"], a, b, m["file"]))
    return out


_DECISIONS = {}


def spelling_decisions(year):
    """My spelling decisions of the year, D3's merge_spellings copied: {(st, chamber, dkey[, group no]): {lines [[name, votes,
    precincts with votes, counties]], summed, why_not}}. A line's precincts are the rows with votes (P.resolve: the TOTAL mode
    where present, else the modes' sum), a row named as a total (AGG_NAME on the precinct) not counted; the lines the pairs
    connect are one group; summed where every line has a precinct and no precinct gives two lines votes."""
    if year in _DECISIONS:
        return _DECISIONS[year]
    pairs = spelling_pairs(year)
    ps = passes(year)
    pre = {}
    for d in ps.values():
        for k, v in d["spell"].items():
            pre.setdefault(k, {}).update(v)
    mine = {}
    by_contest = collections.defaultdict(list)
    for st, sen, dist, a, b, f in pairs:
        by_contest[(st, sen, dkey(dist), dist)].append((a, b))
    for (st, sen, dk, dist), prs in by_contest.items():
        groups = []
        for a, b in prs:
            g = [x for x in groups if any(y is a or y is b for y in x)]
            new = [a, b] + [y for x in g for y in x]
            groups = [x for x in groups if not any(x is y for y in g)] + [list({id(y): y for y in new}.values())]

        def where(x):
            pp = pre.get(spell_key(st, sen, dist, x["name"])) or {}
            res = {pk: (m["TOTAL"] if "TOTAL" in m else sum(m.values())) for pk, m in pp.items()}
            return {pk for pk, v in res.items() if v and not C43.AGG_NAME.search(pk.split("|", 2)[2])}, res
        for gi, g in enumerate(groups):
            sets = {id(x): where(x) for x in g}
            why = None
            if any(not sets[id(x)][0] for x in g):
                why = ("a line has votes only on a row named as a total" if any(any(sets[id(x)][1].values()) for x in g if not sets[id(x)][0])
                       else "a line is not found in MEDSL's raw file")
            elif any(sets[id(a)][0] & sets[id(b)][0] for i, a in enumerate(g) for b in g[i + 1:]):
                why = "a precinct gives both lines votes"
            mine[(st, "state-upper" if sen else "state-lower", dk) + ((gi,) if gi else ())] = {
                "lines": sorted([[x["name"], x["votes"], len(sets[id(x)][0]), sorted({pk.split("|", 1)[0] for pk in sets[id(x)][0]})] for x in g], key=lambda l_: -(l_[1] or 0)),
                "summed": why is None, "why_not": why, "pairs": len(prs)}
    _DECISIONS[year] = (pairs, mine)
    return _DECISIONS[year]


_MERGED = {}


def merged_pool(year, st):
    """C43's MEDSL legislative contests of the state with my spelling decisions applied (D3's merge: the summed line keeps the
    larger line's name, as his pool holds them before the match)."""
    if (year, st) in _MERGED:
        return _MERGED[(year, st)]
    pairs, dec = spelling_decisions(year)
    pool = C43.leg_contests(year, st)
    merged = 0
    for m in pool:
        k = (st, "state-upper" if m["sen"] else "state-lower", dkey(m["district"]))
        for kk, g in dec.items():
            if kk[:3] != k or not g["summed"]:
                continue
            names = [l_[0] for l_ in g["lines"]]
            if not all(n in m["cands"] for n in names):
                continue
            total = sum(m["cands"].pop(n) or 0 for n in names)
            m["cands"][names[0]] = total
            merged += 1
    _MERGED[(year, st)] = pool
    return pool


def section_3():
    h1("48.3 The spelling pairs: D3's _spelled_alike and _given copied on my MEDSL contests; each line's precincts from the raw files; against D3's list")
    chk = L.load_json(at(AFTER, "data/local/check-districts.json"))
    sp = chk["spellings"]
    print(f"  D3's list: {sp['about'][:200]}...; by year {[(y, len(v)) for y, v in sp.items() if y != 'about']}")
    for year in YEARS:
        pairs, mine = spelling_decisions(year)
        theirs = sp.get(str(year), [])
        # a group is keyed by its contest and its lines' names (a contest may hold two groups; D3 lists each as a row)
        th = {(r["state"], r["chamber"], dkey(r["district"]), frozenset(" ".join(l_[0].upper().split()) for l_ in r["lines"])): r for r in theirs}
        mine = {k[:3] + (frozenset(" ".join(l_[0].upper().split()) for l_ in v["lines"]),): v for k, v in mine.items()}
        same_set = set(mine) == set(th)
        print(f"\n  {year}: my pairs {len(pairs)} in {len(mine)} groups ({dict(collections.Counter(k[0] for k in mine))}); D3's rows {len(theirs)} ({dict(collections.Counter(r['state'] for r in theirs))}); "
              f"same groups: {same_set}; mine not D3's {len(set(mine) - set(th))} {sorted(k[:3] for k in set(mine) - set(th))[:8]}; D3's not mine {len(set(th) - set(mine))} {sorted(k[:3] for k in set(th) - set(mine))[:8]}")
        tal = collections.Counter()
        for k in sorted(set(mine) & set(th)):
            m_, t_ = mine[k], th[k]
            names_same = {l_[0].upper() for l_ in m_["lines"]} == {l_[0].upper() for l_ in t_["lines"]}
            votes_same = sorted(l_[1] for l_ in m_["lines"]) == sorted(l_[1] for l_ in t_["lines"])
            prec_same = sorted((l_[0].upper(), l_[2], tuple(l_[3])) for l_ in m_["lines"]) == sorted((l_[0].upper(), l_[2], tuple(l_[3])) for l_ in t_["lines"])
            dec_same = m_["summed"] == t_["summed"] and (m_["summed"] or m_["why_not"] == t_.get("why_not"))
            tal[(f"names {'same' if names_same else 'DIFFER'}", f"votes {'same' if votes_same else 'DIFFER'}", f"precincts and counties {'same' if prec_same else 'DIFFER'}", f"decision {'same' if dec_same else 'DIFFERS'}")] += 1
            if not (names_same and votes_same and prec_same and dec_same):
                print(f"    {k[:3]}: mine {m_}; D3 {{'lines': {t_['lines']}, 'summed': {t_['summed']}, 'why_not': {t_.get('why_not')}}}")
        for k, v in sorted(tal.items()):
            print(f"    {k}: {v}")
        for k in sorted(set(mine) ^ set(th), key=str)[:16]:
            print(f"    only {'mine' if k in mine else 'D3'}: {k[:3]}: {mine.get(k) or th.get(k)}")
        summed = [k for k, v in mine.items() if v["summed"]]
        print(f"    mine summed {len(summed)}, not summed {len(mine) - len(summed)} ({dict(collections.Counter(v['why_not'] for v in mine.values() if not v['summed']))}); "
              f"D3 summed {sum(1 for r in theirs if r['summed'])}, not {sum(1 for r in theirs if not r['summed'])} ({dict(collections.Counter(r.get('why_not') for r in theirs if not r['summed']))})")
        # the records: the summed figure in the record at AFTER (where the record is matched to the contest)
        hit, miss, ex = 0, 0, []
        for k in summed:
            st, lv, dk = k[:3]
            total = sum(l_[1] or 0 for l_ in mine[k]["lines"])
            keep = mine[k]["lines"][0][0]
            recs = records_at(AFTER, f"data/{lv}/{year}/{st}.json")
            found = [r for r in recs.values() if any((c.get("votes") == total) for c in r["result"]["candidates"]) and
                     (dkey(r["place"]["district"].split(",")[0]) == dk or C43.dno_of(r["place"]["district"].split(",")[0]) == dk)]
            if found:
                hit += 1
            else:
                miss += 1
                if len(ex) < 6:
                    ex.append((k, keep, total))
        print(f"    the summed lines' totals found as a candidate's votes in a record of the district at {AFTER}: {hit} of {len(summed)}; not found: {miss} {ex} "
              f"(a Klarner record keeps Klarner's count unless MEDSL's is taken, so a summed MEDSL line shows in the record only where MEDSL's count stands)")


# ------------------------------------------------------------------------------------------ 48.4 over-seats

def section_4():
    h1("48.4 Over-seats on every record: D3's district_ballots copied on every record of 2016, 2018 and 2022 at the BEFORE commit (Klarner's count), against D3's")
    chk = L.load_json(at(AFTER, "data/local/check-districts.json"))
    for year in YEARS:
        ps = passes(year)
        by_state_file = {}
        for p, d in ps.items():
            for st in d["seen"]:
                by_state_file.setdefault(st, []).append(p)
        yv = chk["years"][str(year)]
        os_ = yv.get("over_seats") or {}
        def nk(kid):   # D3's id -> (st, chamber, c46's district key), the same key a record's place gives through C46.rec_norm
            y_, st_, lv_, key_ = C46.kid_norm(kid)
            return (st_, lv_, key_)
        d3_over = {nk(r["id"]): r for r in os_.get("over", [])}
        d3_read = {nk(f["id"]): f for f in yv["flags"] if isinstance(f.get("over_seats"), dict) and f["over_seats"].get("read")}
        d3_unread = {nk(f["id"]): f for f in yv["flags"] if isinstance(f.get("over_seats"), dict) and not f["over_seats"].get("read")}
        d3_flags = {nk(f["id"]): f for f in yv["flags"]}
        not_read_ids = {nk(k) for v in (os_.get("not_read", {}).get("by_state") or {}).values() for k in v.get("flagged", [])}
        print(f"\n  {year}: raw files {len(ps)} ({sum(d['rows'] for d in ps.values()):,} rows); D3: tested {os_.get('tested')}, over {list(d3_over)}, not read {json.dumps(os_.get('not_read', {}).get('by_state'))[:300]}; "
              f"flags with over_seats read {len(d3_read)}, not read {len(d3_unread)} ({dict(collections.Counter(f['over_seats']['why'][:60] for f in d3_unread.values()))})")
        blank = {st: sorted(set(d["seen"][st]) - set(d.get("voted", {}).get(st, []))) for d in ps.values() for st in d["seen"] if set(d["seen"][st]) - set(d.get("voted", {}).get(st, []))}
        print(f"    counties with rows but no contest's votes (D3's 'blank'): {blank}")
        tal = collections.Counter()
        over_mine = []
        cmp = collections.Counter()
        cmp_ex = []
        n_rec = 0
        for st in sorted(states_with_records(year)):
            files = by_state_file.get(st, [])
            if not files:
                tal["no raw file of the state"] += 1
                continue
            pool = merged_pool(year, st)
            d = ps[files[0]] if len(files) == 1 else None
            if d is None:   # several files hold the state (not expected): the first with the state's legislative rows
                d = next((ps[p] for p in files if any(k.startswith(st + "|") for k in ps[p]["leg"])), ps[files[0]])
            keys_all = [k for k in d["leg"] if k.startswith(st + "|")]
            got, wide, nprec = district_ballots(d, st, keys_all)
            for lv, sen in (("state-lower", 0), ("state-upper", 1)):
                f = f"data/{lv}/{year}/{st}.json"
                if not os.path.exists(at(BEFORE, f)):
                    continue
                for rid, b in records_at(BEFORE, f).items():
                    n_rec += 1
                    rk = (st, lv, C46.rec_norm(b["place"]["district"]))
                    m = C46.d3_match(b, pool)
                    if not m.get("matched"):
                        tal["unmatched by D3's matcher (my copy)"] += 1
                        continue
                    k = f"{st}|{sen}|{dkey(m['district'])}"
                    bb = got.get(k)
                    kid = None
                    head = b["place"]["district"].split(",")[0].strip()
                    if bb is None:
                        tal["no ballots (no wide contest reaches the district's precincts, or no precinct)" if k in d["leg"] else "the district's key has no precincts in the pass"] += 1
                        continue
                    seats = m["seats"] or 1
                    xk, xm = m["klarner"] / (seats * bb[1]), m["medsl"] / (seats * bb[1])
                    tal["read"] += 1
                    if xk > OVER_SEATS:
                        over_mine.append((rid, st, lv, head, m["district"], seats, bb[0], bb[1], round(xk, 4), round(xm, 4), bb[2][:3], m["klarner"], m["medsl"], rk, round(m["ratio"], 4) if m["ratio"] else None))
                    # D3's figures on the same record (his flags carry over_seats; their ids are the records')
                    fl = d3_read.get(rk)
                    if fl is not None:
                        o = fl["over_seats"]
                        if dkey(fl["medsl_district"]) != dkey(m["district"]):
                            cmp["D3 matched another MEDSL district"] += 1
                        same = o["precincts"] == bb[0] and o["ballots"] == bb[1]
                        cmp["precincts and ballots equal" if same else "DIFFER"] += 1
                        if not same and len(cmp_ex) < 8:
                            cmp_ex.append((rid, "mine", bb[0], bb[1], round(xk, 4), "D3", o["precincts"], o["ballots"], o["klarner_x"], o.get("by")))
                        elif same and abs(o["klarner_x"] - xk) > 0.01:
                            # D3's paired sum leaves out the write-in lines below the strong line (his _named; the record's weak
                            # write-ins are 'others'); my d3_match pairs every named line, so Klarner's sum over the named lines alone:
                            strong = {a["name"] for a in C46.named_of(C46.rec_cands(b), seats)}
                            kv2 = sum(p_[1] or 0 for p_ in m["pairs"] if p_[0] in strong)
                            xk2 = kv2 / (seats * bb[1])
                            if abs(o["klarner_x"] - xk2) <= 0.01:
                                cmp["klarner_x equal once the write-ins below the strong line are left out, as D3's pairs leave them"] += 1
                            else:
                                cmp["klarner_x differs (Klarner's paired sum or the seats)"] += 1
                                if len(cmp_ex) < 8:
                                    cmp_ex.append((rid, "mine x", round(xk, 4), round(xk2, 4), m["klarner"], seats, "D3", o["klarner_x"], fl["klarner"], o["seats"]))
                    elif rk in d3_unread:
                        cmp["D3 not read: " + d3_unread[rk]["over_seats"]["why"][:50]] += 1
        print(f"    records {n_rec:,}: {dict(tal)}")
        print(f"    my ballots against D3's on his flags with over_seats read: {dict(cmp)}; e.g. {cmp_ex[:6]}")
        print(f"    mine over {OVER_SEATS} (Klarner's paired count over seats x ballots): {len(over_mine)}; D3's over list: {len(d3_over)}")
        why_not_d3 = collections.Counter()
        for row in sorted(over_mine, key=lambda r: -r[8]):
            rid, st, lv, head, md, seats, np_, bal, xk, xm, by, kv, mvv, rk, ratio = row
            d3row = d3_over.get(rk)
            fl = d3_flags.get(rk)
            a = records_at(AFTER, f"data/{lv}/{year}/{st}.json").get(rid)
            if d3row:
                why = "D3 lists it over"
            elif fl is not None and fl.get("over_seats", {}).get("read") is False:
                why = "D3's flag: over-seats not read (" + fl["over_seats"]["why"][:45] + ")"
            elif fl is not None and not fl.get("covered"):
                why = "D3's flag: not covered (" + str(fl.get("outcome"))[:40] + ")"
            elif fl is not None:
                why = "D3's flag read, not over: " + json.dumps(fl.get("over_seats"))[:80]
            elif rk in not_read_ids or (year == 2018 and st == "IN"):
                why = "D3: not read, the state's file has a blank county"
            elif ratio is not None and abs(ratio - 1) > RATIO_OFF:
                why = f"MEDSL's count off Klarner's by more than 3% (x{ratio}) and no flag of D3's: his pool differs here"
            else:
                why = "no flag of D3's and MEDSL's count within 3%: D3 did not test it (not covered, or shared)"
            why_not_d3[why.split(" (")[0].split(": ")[0] + (": " + why.split(": ")[1].split(" (")[0] if ": " in why else "")] += 1
            print(f"      {rid} ({md}): seats {seats}, precincts {np_}, ballots {bal:,} (by {by}); Klarner {kv:,} x{xk}, MEDSL {mvv:,} x{xm} (MEDSL/Klarner x{ratio}); {why}; "
                  f"the record after: votes_source {a['result'].get('votes_source') if a else None}, p {pval(a) if a else None}; counties of MEDSL's district precincts "
                  f"{sorted({pk.split('|')[0] for pk in ps[by_state_file[st][0]]['leg'].get(f'{st}|{1 if lv == 'state-upper' else 0}|{dkey(md)}', [])})[:6]}")
        print(f"    why D3's list lacks mine: {dict(why_not_d3)}")
        # the three Vermont districts
        if year == 2018:
            for kid in ("2018-VT-upper-grandisle---", "2018-VT-upper-windham---", "2018-VT-upper-rutland---"):
                a, b = record_of(kid, AFTER), record_of(kid, BEFORE)
                print(f"    {kid}: Klarner {sum(c['votes'] for c in b['result']['candidates']):,} -> MEDSL {sum(c['votes'] for c in a['result']['candidates']):,}; p {pval(b)} -> {pval(a)}; "
                      f"D3's over row {json.dumps({k: v for k, v in d3_over.get(nk(kid), {}).items() if k in ('precincts', 'ballots', 'klarner_x', 'medsl_x', 'outcome', 'outcome_before')})}")
            # Washington County, Indiana
            inp = next((p for p in ps if os.path.basename(p) == IN_2018_FILE), None)
            if inp:
                d = ps[inp]
                print(f"    Indiana 2018's file: counties with rows {len(d['seen'].get('IN', []))}, with a contest's votes {len(d.get('voted', {}).get('IN', []))}; blank {sorted(set(d['seen']['IN']) - set(d['voted']['IN']))} "
                      f"(D3: 18175, Washington County, 'BALLOTS CAST' rows alone; 101 records not read, Senate 47 among them)")
                n_in = sum(len(records_at(BEFORE, f"data/{lv}/2018/IN.json")) for lv in ("state-lower", "state-upper"))
                print(f"    Indiana 2018 records: {n_in}; D3's not_read by_state IN records {os_.get('not_read', {}).get('by_state', {}).get('IN', {}).get('records')} (the records whose match was covered; the rest untested for other reasons)")


# ------------------------------------------------------------------------------------------ 48.5 zero rows

def section_5():
    h1("48.5 The zero-row counties: Indiana 2022's Cass, Daviess, Scott and Monroe; Kentucky 2016's Jefferson; the records' outcomes")
    chk = L.load_json(at(AFTER, "data/local/check-districts.json"))
    for (year, st), counties in sorted(ZERO_COUNTIES.items()):
        ps = passes(year)
        for p, d in ps.items():
            for key, offices in sorted(d.get("county_rows", {}).items()):
                if not key.startswith(st + "|"):
                    continue
                rows = sum(v[0] for v in offices.values())
                votes = sum(v[1] for v in offices.values())
                precs = max((v[2] for v in offices.values()), default=0)
                leg = {k: v for k, v in offices.items() if k.split("|")[0] in ("STATE HOUSE", "STATE SENATE", "STATE REPRESENTATIVE", "STATE SENATOR")}
                print(f"  {year} {st} county {key.split('|')[1]} ({os.path.basename(p)}): rows {rows:,}, votes {votes:,}, precincts (most in an office) {precs}; offices {len(offices)}; "
                      f"legislative rows {[(k, v) for k, v in sorted(leg.items())][:8]}")
                print(f"    offices with any votes: {[(k, v[1]) for k, v in offices.items() if v[1]][:8]}")
        flags = {f["id"]: f for f in chk["years"][str(year)]["flags"]}
        kids = {(2022, "IN"): ["2022-IN-lower--23--", "2022-IN-lower--66--", "2022-IN-lower--38--", "2022-IN-lower--45--", "2022-IN-lower--63--", "2022-IN-lower--69--", "2022-IN-upper--39--", "2022-IN-upper--43--"],
                (2016, "KY"): ["2016-KY-lower--28--", "2016-KY-lower--33--"]}[(year, st)]
        for kid in kids:
            b, a = record_of(kid, BEFORE), record_of(kid, AFTER)
            fl = flags.get(kid, {})
            cov = fl.get("coverage") or {}
            print(f"  {kid}: p {pval(b) if b else '-'} -> {pval(a) if a else '-'}; D3's outcome {fl.get('outcome')}; coverage gaps {cov.get('gaps')} (by {str(cov.get('by'))[:40]}); "
              f"the record's reason/note: {str((a or {}).get('p', {}).get('not_computed') or '')[:100]} | {[n[:160] for n in (a or {}).get('notes', []) if 'cover' in n or 'zero' in n][:1]}")


# ------------------------------------------------------------------------------------------ 48.6 DC

def section_6():
    h1("48.6 DC 2018: check-volume.json's DC rows at the Board's 231,700; the Board's certified PDF read apart; the wards")
    pdf = os.path.join(SRC, "dc_boe", "November_6_2018_General_Election_Certified_Results.pdf")
    txt = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True).stdout
    tl = txt.split("\n")
    head = [ln for ln in tl[:12] if "Ward" in ln]
    bc = next(i for i, ln in enumerate(tl) if ln.strip() == "Ballots Cast")
    rv = next(i for i, ln in enumerate(tl) if ln.strip() == "Registered Voters")
    row = next(ln for ln in tl[bc + 1:bc + 4] if "CityWide" in ln)
    rrow = next(ln for ln in tl[rv + 1:rv + 4] if "CityWide" in ln)
    figs = [int(x.replace(",", "")) for x in re.findall(r"[\d,]+", row)]
    rfigs = [int(x.replace(",", "")) for x in re.findall(r"[\d,]+", rrow)]
    print(f"  the Board's PDF (fetched in section 18, {os.path.getsize(pdf):,} bytes), its first page's columns {head[:1]}: 'Registered Voters' CityWide {rfigs}; 'Ballots Cast' CityWide {figs} "
          f"(wards 1 to 8, then the city: {figs[-1]:,}; the wards sum to {sum(figs[:-1]):,})")
    wards = {str(i + 1): v for i, v in enumerate(figs[:-1])}
    for commit in (BEFORE, AFTER):
        v = L.load_json(at(commit, "data/local/check-volume.json"))
        s = json.dumps(v)
        dc_rows = []
        def walk(x, path=""):
            if isinstance(x, dict):
                if x.get("state") == "DC" and "ballots_cast" in x:
                    x = dict(x)
                    x["year"] = re.search(r"\b(20\d\d)\b", path).group(1) if re.search(r"\b(20\d\d)\b", path) else path[:40]
                    dc_rows.append(x)
                for k, y in x.items():
                    walk(y, path + "." + k)
            elif isinstance(x, list):
                for y in x:
                    walk(y, path)
        walk(v)
        print(f"\n  check-volume.json at {commit}: '231700' appears {s.count('231700')} times, '462964' {s.count('462964')}; DC rows with ballots_cast: {len(dc_rows)} (years {dict(collections.Counter(str(r.get('year')) for r in dc_rows))}); "
              f"their ballots_cast values {dict(collections.Counter(r['ballots_cast'] for r in dc_rows))}; ballots_cast_source: {dict(collections.Counter(str(r.get('ballots_cast_source'))[:80] for r in dc_rows))}")
        for r in dc_rows[:14]:
            w = C43.dno_of(str(r.get("district")))
            exp = (wards.get(w) if w else (figs[-1] if str(r.get("district")).upper() in ("STATEWIDE", "AT-LARGE") else None)) if r.get("year") == "2018" else None
            print(f"    {r.get('year')} {r.get('office')} {r.get('district')}: votes {r.get('votes'):,} precincts {r.get('precincts')} ballots_cast {r.get('ballots_cast'):,} ratio {r.get('votes') / r.get('ballots_cast'):.3f}"
                  + (f" ballots_cast_rows {r.get('ballots_cast_rows')}" if 'ballots_cast_rows' in r else "")
                  + (f"; the PDF's {exp:,} {'EQUAL' if exp == r.get('ballots_cast') else 'DIFFERS' if commit == AFTER else ('half' if exp * 2 == r.get('ballots_cast') else 'differs')}" if exp else ""))
        # the at-large record
        recs = records_at(commit, "data/local/2018/DC.json")
        al = [r for r in recs.values() if "AT-LARGE" in r["id"].upper() or "AT_LARGE" in r["id"].upper()]
        for r in al[:2]:
            print(f"    {r['id']}: seats {r.get('election', {}).get('seats') if isinstance(r.get('election'), dict) else r.get('seats')}; p {pval(r)}; reason {str(r['p'].get('not_computed') or r['p'].get('reason'))[:160]}")


# ------------------------------------------------------------------------------------------ 48.7 New York's reasons

def section_7():
    h1("48.7 New York 2018's at-large reasons from MEDSL's governor lines; the forecast inputs behind the moves beyond 1%")
    path = next(p for y, p in M.all_raw_files() if os.path.basename(p) == "2018-ny-precinct-general.zip")
    by_cand = collections.defaultdict(lambda: collections.defaultdict(int))   # candidate -> party -> votes (TOTAL or other modes, D3's rule per precinct is max; here the file's TOTAL rows)
    modes = collections.Counter()
    counties = set()
    for r in M.rows(path):
        if (r.get("office") or "").strip().upper() != "GOVERNOR":
            continue
        modes[(r.get("mode") or "").upper()] += 1
        cand = (r.get("candidate") or "").strip().upper()
        if M.is_meta(cand):
            continue
        counties.add(fips5(r.get("county_fips")))
        by_cand[cand][(r.get("party_detailed") or r.get("party") or "").upper()] += ivotes(r)
    print(f"  MEDSL's 2018 New York governor rows: modes {dict(modes)}; counties {len(counties)}")
    for c, ps in sorted(by_cand.items(), key=lambda kv: -sum(kv[1].values()))[:6]:
        print(f"    {c}: every line {sum(ps.values()):,} {dict(ps)}")
    # D3's reading (local_volume's governor test, copied): each of the record's top two candidates against MEDSL's lines summed over
    # the names sharing the surname; the worst of the two is the reason's figure; beyond 0.5%, each one's own party line too
    for commit in (BEFORE, AFTER):
        rec = records_at(commit, "data/governor/2018.json")["2018-governor-NY"]
        top2 = sorted([c for c in rec["result"]["candidates"] if c.get("votes")], key=lambda c: -c["votes"])[:2]
        rows = []
        for c in top2:
            sur = C46.name_key(c["name"])[0]
            lines = {n: ps for n, ps in by_cand.items() if sur in C46.surs(n)}
            summed = sum(sum(ps.values()) for ps in lines.values())
            own = sum(v for ps in lines.values() for pd, v in ps.items() if pd in {"D": ("DEMOCRAT", "DEMOCRATIC"), "R": ("REPUBLICAN",)}.get(c["party"], ()))
            rows.append((c["name"], c["party"], c["votes"], summed, round(summed / c["votes"], 5), own, round(own / c["votes"], 5)))
        worst = max(rows, key=lambda r: abs(r[4] - 1))
        print(f"  the record at {commit} (total {rec['result']['total_votes']:,}): " + "; ".join(f"{n} ({p}) {v:,}: MEDSL's lines summed {sm:,} = {r1 * 100:.2f}%, own line {ow:,} = {r2 * 100:.2f}%" for n, p, v, sm, r1, ow, r2 in rows)
              + f"; the worst: {worst[0]} {worst[4] * 100:.2f}% (own line {worst[6] * 100:.2f}%)")
    for rid in ("2018-local-NY-COMPTROLLER", "2018-local-NY-ATTORNEY_GENERAL"):
        b = records_at(BEFORE, "data/local/2018/NY.json").get(rid)
        a = records_at(AFTER, "data/local/2018/NY.json").get(rid)
        print(f"  {rid}: before '{str(b['p'].get('not_computed'))[:130]}...'; after '{str(a['p'].get('not_computed'))[:170]}...'")
    print("  (D3's 95.97% before and 84.53% / 73.51% after are the worst nominee's figures above: Cuomo's before, Molinaro's after, the record's count for governor having grown by his other lines)")


def main():
    which = [int(a) for a in sys.argv[1:]] or [1, 2, 3, 4, 5, 6, 7]
    print(f"c48: section 19, second part; {BEFORE} -> {AFTER}; sections {which}")
    for n in which:
        globals()[f"section_{n}"]()


if __name__ == "__main__":
    main()
