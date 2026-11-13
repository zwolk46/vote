"""c43: the eighth pass's second end, #100 (D3's district checks, main d680bd4) against 346273e.

The orchestrator, 2026-11-13 00:26 UTC: "D3's district-checks PR is merged as #100 (d680bd4, squashed from 5d2970c), so it
joins your eighth pass as planned. Your end moves from 346273e to d680bd4, since #100 is the only change between them. Check
it as you checked #96 and #97: every p it moves (moves-district-checks.json, 197 lost, 72,754 moved, none over 2x by my
compare), the coverage rule as built (US House rows as the county gate, contests released on their own whole rows, a
statewide contest held past 2% of the state's votes), and Idaho's seven districts a year. Also read the 141 of your 249
Klarner districts that D3's list leaves off. D3 says 80 are within 3% on the named candidates, a difference between your D+R
or all-lines sums and its named-candidate sums. Say what the other 61 are. ... put #100 in a further section with its own
run, so that #96 and #97 are not held for it. The reason is that a fixed end must not move under a run already started."

Sections (each from my own reading of the raw files, the records at the two commits and Klarner's file; nothing from
pipeline/ imported; rules of the build that must be applied are copied here and say so):
  43.1 moves-district-checks.json against my own diff of every record, 346273e -> d680bd4
  43.2 my 249 districts of c38 beside D3's check: the 108 on both lists, the 80 "within 3%", the 35 untested, the 26 settled
  43.3 MEDSL's coverage from the raw files: the county gate (US House rows), the released contests, the statewide contests
  43.4 the coarse tier: Idaho 1984-1990 (the 2x line, seven districts a year) and South Carolina's Senate 1976 and 1980
  43.5 every flag's outcome on the records at d680bd4; the held flags' lost p
  43.6 the over-ballot check's rows added at d680bd4 (the state's own counts tested too)
Run from the repository root: python3 -I checks/m2/c43_district_checks.py [1 2 3 4 5 6]
"""
import collections
import csv
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402
import m2medsl as M  # noqa: E402
import c40_pr_checks as C40  # noqa: E402
import c41_governor_refit as C41  # noqa: E402
import c42_held_totals as C42  # noqa: E402

BEFORE, AFTER = "346273e", "d680bd4"
DERIVED = os.path.join(L.CACHE, "fifth", "derived")
KLARNER = os.path.join(L.CACHE, "klarner_202slers_uoa_contest20230810.csv")
C38 = os.path.join(L.ROOT, "checks", "m2", "c38-districts.json")


def h1(s):
    print("\n" + "=" * 100 + f"\n{s}\n" + "=" * 100)


def at(commit, rel):
    return os.path.join(C41.worktree(commit), rel)


def records_at(commit, f):
    return C42.records_at(C41.worktree(commit), f)


# ------------------------------------------------------------------------------------------ 43.1 the moves file

def section_1():
    h1(f"43.1 moves-district-checks.json against my own diff of every record, {BEFORE} -> {AFTER}")
    import subprocess
    mv = L.load_json(at(AFTER, "data/local/moves-district-checks.json"))
    rows = {r[0]: r for r in mv["records"]}
    print(f"  the file: {len(mv['records'])} rows, {len(rows)} ids, against {mv.get('against')} (the branch before the rebuild; "
          f"my diff is main to main)")
    print(f"  its summary: {json.dumps(mv['summary'])}")
    files = subprocess.run(["git", "diff", "--name-only", BEFORE, AFTER, "--", "data/"], capture_output=True, text=True,
                           cwd=L.ROOT).stdout.split()
    data_files = [f for f in files if re.match(r"^data/(local|primary|measure|state-lower|state-upper)/\d{4}/[A-Z]{2}\.json$", f)
                  or re.match(r"^data/(governor|house|senate|president)/\d{4}\.json$", f)]
    print(f"  data files changed: {len(files)}; record files: {len(data_files)} {dict(collections.Counter(f.split('/')[1] for f in data_files))}; "
          f"other: {[f for f in files if f not in data_files]}")
    mine = collections.Counter()
    agree, dis, seen, worst = 0, collections.Counter(), set(), []
    pdiff = rdiff = 0
    lost = collections.Counter()
    lost_ids = collections.defaultdict(list)
    moved = []          # (ratio, id) for every p that moved
    within = collections.Counter()   # p moved by 1% or less and nothing else but forecasts/forecast_inputs: by level and year
    gone_new = {"G": [], "A": []}
    stamps = 0
    for f in data_files:
        lv, yr = f.split("/")[1], f.split("/")[2]
        b, a = records_at(BEFORE, f), records_at(AFTER, f)
        for i in sorted(set(b) | set(a)):
            code = C40.my_code(b.get(i), a.get(i))
            if not code:
                continue
            d = C40.what_differs(b.get(i) or {}, a.get(i) or {})
            if tuple(d) == ("p.commit",):
                stamps += 1   # the p's commit stamp alone: no change (the file counts stamps aside)
                continue
            c = code[0]
            if c in ("B", "Q", "O", "R") and any((b.get(i) or {}).get(k) != (a.get(i) or {}).get(k) for k in ("type", "office_type")):
                c = "T"
            pb, pa = C40.pval(b.get(i) or {}), C40.pval(a.get(i) or {})
            if c == "P":
                moved.append((pa / pb if pb else None, i))
                other = [x for x in d if not (x.startswith("p.") or x.startswith("forecasts") or x.startswith("forecast_inputs") or x in ("p", "two_party"))]
                if pb and abs(pa / pb - 1) <= 0.01 and not other:
                    within[(lv, yr)] += 1
                    seen.add(i)
                    continue   # counted, not listed, in the file
            mine[(lv, c)] += 1
            seen.add(i)
            if c == "L":
                lost[(lv, yr)] += 1
                lost_ids[(lv, yr)].append(i)
            if c in ("G", "A"):
                gone_new[c].append(i)
            row = rows.get(i)
            if row is None:
                worst.append((i, c, "not in the moves file", d[:6]))
                continue
            theirs = tuple(row[8])
            ok = c in theirs or (c == "Q" and "O" in theirs) or (c == "O" and "Q" in theirs) or (c == "R" and ("Q" in theirs or "O" in theirs)) \
                or (c == "B" and ("Q" in theirs or "O" in theirs))
            if ok:
                agree += 1
            else:
                dis[(lv, c, theirs)] += 1
                worst.append((i, c, theirs, d[:6]))
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
    print(f"  p before/after other than the record's: {pdiff}; ratios off by more than 1.5e-4: {rdiff}; records differing in p.commit alone (a stamp): {stamps}")
    for (lv, c, theirs), v in sorted(dis.items(), key=lambda kv: -kv[1])[:10]:
        ex = [w for w in worst if w[1] == c and w[2] == theirs][:2]
        print(f"    mine {c} theirs {theirs} {lv}: {v}; e.g. " + "; ".join(f"{e[0]} differs in {e[3]}" for e in ex))
    for w in [w for w in worst if w[2] == "not in the moves file"][:8]:
        print(f"    not in the file: {w[0]} mine {w[1]} differs in {w[3]}")
    print(f"  records gone (G): {len(gone_new['G'])} {gone_new['G'][:5]}; new (A): {len(gone_new['A'])} {gone_new['A'][:5]}")
    # the p lost, by level and year, against the file's L rows and D3's count (197)
    theirs_L = collections.Counter((r[1].split("/")[1], r[1].split("/")[2]) for r in mv["records"] if "L" in r[8])
    print(f"  p lost (L), mine: {sum(lost.values())} {dict(sorted(lost.items()))}")
    print(f"  p lost (L), the file: {sum(theirs_L.values())} {dict(sorted(theirs_L.items()))}; equal by level and year: {lost == theirs_L}")
    for k in sorted(lost):
        ids = lost_ids[k]
        if k[0] in ("state-lower", "state-upper") and k[1] in ("1984", "1986", "1988", "1990"):
            ds = sorted({re.sub(r"__seat_\d+$", "", i.split("-ID-")[1]) for i in ids}, key=lambda x: int(x))
            print(f"    {k}: {len(ids)} posts of Idaho's districts {ds}")
    # every p that moved: the extremes, none over 2x
    mv_r = [r for r, i in moved if r is not None]
    over2 = [(r, i) for r, i in moved if r is not None and (r > 2 or r < 0.5)]
    print(f"  p moved (P), mine: {len(moved)} (listed in the file: {sum(1 for r in mv['records'] if 'P' in r[8])} rows; counted within 1%: "
          f"{sum(v['records'] for lv in mv['p_moved_within_1pct'].values() for v in lv.values())}); mine within 1% and nothing else: {sum(within.values())}; "
          f"by more than 1%: {sum(1 for r in mv_r if abs(r - 1) > 0.01)}; by more than 3%: {sum(1 for r in mv_r if abs(r - 1) > 0.03)}; "
          f"range x{min(mv_r):.4f} to x{max(mv_r):.4f}; over 2x or under 1/2: {len(over2)} {over2[:5]}")
    theirs_w = {(lv, y): v["records"] for lv, x in mv["p_moved_within_1pct"].items() for y, v in x.items()}
    diff_w = {k: (within.get(k, 0), theirs_w.get(k, 0)) for k in set(within) | set(theirs_w) if within.get(k, 0) != theirs_w.get(k, 0)}
    print(f"  within 1%, by level and year, mine against the file's: {len(diff_w)} differing {dict(sorted(diff_w.items())) if len(diff_w) < 12 else list(sorted(diff_w.items()))[:12]}")
    for r in mv["records"]:
        if "T" in r[8] or "G" in r[8] or "A" in r[8] or ("L" in r[8] and r[1].split("/")[1] == "measure"):
            print(f"    file row: {r[0]} | {r[2]} | type {r[3]} -> {r[4]} | p {r[5]} -> {r[6]} | ratio {r[7]} | {r[8]}")


# ------------------------------------------------------------------------------------------ 43.2 the 249 districts

SUFFIX = {"JR", "SR", "II", "III", "IV", "V"}
GENERIC = re.compile(r"^\s*$|^OTHERS?$|\bALL OTHERS\b|SCATTER|\bVOIDS?\b|\bBLANKS?\b|\bTOTALS?\b|OVER ?VOTES?|UNDER ?VOTES?|"
                     r"NONE OF THE|UNCOMMITTED|WRITE[- ]?INS?\b|^(AFFIDAVIT|FEDERAL|ABSENTEE(/MILITARY)?|MILITARY|MANUALLY COUNTED EMERGENCY|"
                     r"EMERGENCY|SPECIAL PRESIDENTIAL|PUBLIC COUNTER)$|^\[WRITE-IN\]$|^YES$|^NO$", re.I)
WA_LEG = re.compile(r"^LEGISLATIVE DISTRICT (\d+) - STATE (SENATOR|REPRESENTATIVE)(?: POS\.? ?(\d+))?")   # the build's _WA_LEG, copied
LEG_NAMES = {"STATE HOUSE": 0, "STATE SENATE": 1, "REPRESENTATIVE IN GENERAL ASSEMBLY": 0, "SENATOR IN GENERAL ASSEMBLY": 1,
             "HOUSE OF DELEGATES": 0, "STATE REPRESENTATIVE": 0, "STATE SENATOR": 1, "STATE ASSEMBLY": 0}   # the build's LEG and LEG_NAMES, copied (plus STATE ASSEMBLY)


def ktokens(name):
    """Klarner's 'surname, given' -> the surname's parts in capitals (a hyphen or a space splits it); MEDSL's 'GIVEN SURNAME'
    -> its tokens. A part under three letters is no match on its own."""
    s = re.sub(r"[.'’]", "", name.upper())
    s = re.sub(r"\(.*?\)", " ", s)
    if "," in s:
        s = s.split(",")[0]
    toks = [t for t in re.split(r"[\s\-/]+", s) if t and t not in SUFFIX]
    return [t for t in toks if len(t) >= 3] or toks


def mtokens(name):
    s = re.sub(r"[.'’]", "", name.upper())
    s = re.sub(r"\(.*?\)", " ", s)
    return [t for t in re.split(r"[\s\-/,]+", s) if t and t not in SUFFIX]


def leg_contests(year, st):
    """MEDSL's legislative contests of a state and year from my volume summaries: [{sen, district, post, cands{name: votes},
    party, key, file}]; Washington's are read from their filed names (the build's relabel, copied)."""
    out = []
    for y, path in M.all_raw_files():
        if y != year:
            continue
        p = os.path.join(DERIVED, os.path.basename(path) + ".volume.json")
        if not os.path.exists(p):
            continue
        d = L.load_json(p)
        for key, c in d["contests"].items():
            parts = key.split("|")
            if parts[0] != st:
                continue
            office, district = parts[2], parts[3] if len(parts) > 3 else ""
            post = None
            x = WA_LEG.match(office)
            if x:
                sen, district, post = (1 if x.group(2) == "SENATOR" else 0), x.group(1), x.group(3)
            elif office in LEG_NAMES:
                sen = LEG_NAMES[office]
            else:
                continue
            out.append({"sen": sen, "district": district, "post": post, "cands": c["no_total"] or c["cands"], "party": c.get("party") or {},
                        "key": key, "file": os.path.basename(path), "counties": c.get("counties") or {}})
    return out


def dno_of(d):
    m = re.fullmatch(r"0*(\d+)", (d or "").strip())
    return m.group(1) if m else None


def kid_parts(kid):
    """'2016-WA-lower--39--1' -> (year, state, level, (district key, post))."""
    head, dno, geopost, mmdpost = kid.rsplit("-", 3)
    year, st, ch, dname = head.split("-", 3)
    return int(year), st, "state-" + ch, (" ".join(f"{dname} {dno}".split()).lower(), geopost or mmdpost)


def rec_key(place_district):
    m = re.match(r"^(.*?)(?:,\s*(?:seat|position|post)\s*(\w+))?$", place_district.strip().lower())
    return (" ".join(m.group(1).split()), m.group(2) or "")


def record_of(kid, recs_cache):
    year, st, lv, key = kid_parts(kid)
    f = f"data/{lv}/{year}/{st}.json"
    if f not in recs_cache:
        recs_cache[f] = records_at(BEFORE, f)
    for r in recs_cache[f].values():
        if rec_key(r["place"]["district"]) == key:
            return r
    return None


def my_match(rec, contests):
    """My own named-candidate test: the MEDSL contests of the chamber whose lines name every named candidate of the record
    (by a part of the surname); among several, the one whose district number is the record's; the pairs and the ratio."""
    named = [x for x in rec["result"]["candidates"] if (x.get("votes") or 0) > 0 and not GENERIC.search(x["name"]) and x["name"].strip()]
    ks = [ktokens(x["name"]) for x in named]
    hits = []
    for m in contests:
        toks = {t for n in m["cands"] for t in mtokens(n)}
        if all(any(t in toks or any(len(x) >= 5 and t.endswith(x) for x in toks) for t in k) for k in ks):
            hits.append(m)
    dno = dno_of(rec["place"]["district"].split(",")[0])
    if len(hits) > 1 and dno:
        h = [m for m in hits if dno_of(m["district"]) == dno]
        hits = h or hits
    if len(hits) != 1:
        return {"matched": False, "hits": len(hits), "named": len(named)}
    m = hits[0]
    pairs, used = [], set()
    for x, k in zip(named, ks):
        cands = [(n, v) for n, v in m["cands"].items() if n not in used and any(t in mtokens(n) or any(len(x) >= 5 and t.endswith(x) for x in mtokens(n)) for t in k)]
        if not cands:
            return {"matched": False, "hits": 1, "named": len(named), "unpaired": x["name"]}
        n, v = max(cands, key=lambda nv: nv[1])
        used.add(n)
        pairs.append((x["name"], x["votes"], n, v))
    kv = sum(p[1] for p in pairs)
    mvv = sum(p[3] for p in pairs)
    others = [(n, v) for n, v in m["cands"].items() if n not in used and v > 0 and not GENERIC.search(n)]
    return {"matched": True, "key": m["key"], "pairs": pairs, "klarner": kv, "medsl": mvv, "ratio": mvv / kv if kv else None,
            "others": others, "district": m["district"]}


def section_2():
    h1("43.2 My 249 districts (c38-districts.json, 5% or more off by the district's code) beside D3's check-districts-m2.json")
    c38 = L.load_json(C38)["districts"]
    cmp_ = L.load_json(at(AFTER, "data/local/check-districts-m2.json"))
    chk = L.load_json(at(AFTER, "data/local/check-districts.json"))
    flags = {f["id"]: f for v in chk["years"].values() for f in v["flags"]}
    print(f"  D3's tally of my 249: {json.dumps(cmp_['tally'])}")
    print(f"  D3's flags not on my list: {json.dumps(cmp_['flags_not_on_m2s_list'])}")
    by_key = {(r["year"], r["state"], r["chamber"], " ".join(r["district"].split()).lower()): r for r in cmp_["m2"]}
    recs_cache, cont_cache = {}, {}
    tally = collections.Counter()
    agree_flag = collections.Counter()
    untested = []
    within = collections.Counter()
    for r in c38:
        k = (r["year"], r["state"], r["chamber"], " ".join(r["klarner_code"].split()).lower())
        d3 = by_key.get(k)
        if d3 is None:
            tally["not in D3's file"] += 1
            print(f"    not in D3's comparison: {k}")
            continue
        kind = d3["here"]
        ck = (r["year"], r["state"])
        if ck not in cont_cache:
            cont_cache[ck] = leg_contests(r["year"], r["state"])
        sen = 1 if r["chamber"] == "state-upper" else 0
        contests = [m for m in cont_cache[ck] if m["sen"] == sen]
        # my own test on each of the district's records (a post is its own record)
        results = []
        for kid in d3["ids"]:
            rec = record_of(kid, recs_cache)
            if rec is None:
                results.append((kid, None, None))
                continue
            results.append((kid, rec, my_match(rec, contests)))
        mine_ok = [x for x in results if x[2] and x[2]["matched"]]
        if results and all(x[2] and x[2]["matched"] for x in results):
            kv = sum(x[2]["klarner"] for x in results)
            mvv = sum(x[2]["medsl"] for x in results)
            ratio = mvv / kv if kv else None
        else:
            ratio = None
        tally[kind] += 1
        p_on = r.get("p_rests_on")
        if kind == "both":
            # D3's flag ratio against mine
            got = [flags[kid] for kid in d3["ids"] if kid in flags]
            if ratio is not None and got:
                theirs = sum(f["medsl"] for f in got) / sum(f["klarner"] for f in got) if sum(f["klarner"] for f in got) else None
                agree_flag["ratio within 1e-3 of D3's" if theirs and abs(theirs - ratio) < 1e-3 else "ratio differs"] += 1
                if theirs and abs(theirs - ratio) >= 1e-3:
                    print(f"    both, ratios differ: {k}: D3 {theirs:.4f} ({[f['outcome'] for f in got]}) mine {ratio:.4f} {[x[2]['pairs'] for x in results][:1]}")
            else:
                agree_flag["mine unmatched"] += 1
            continue
        if kind == "M2 only: within 3% here":
            if ratio is not None:
                within["within 3% by my own match" if abs(ratio - 1) <= 0.03 else f"off by my match"] += 1
                if abs(ratio - 1) > 0.03:
                    print(f"    'within 3% here' but off by my match: {k}: mine {ratio:.4f} (Klarner {kv:,}, MEDSL named {mvv:,}; by the code {r['by']} {r['medsl']:,}); "
                          f"pairs {[x[2]['pairs'] for x in results]}")
            else:
                within["mine unmatched"] += 1
                print(f"    'within 3% here' and mine unmatched: {k}: {[(x[0], x[2]) for x in results]}")
            continue
        if kind == "M2 only: settled before this check":
            continue
        # the 35: say what each is
        lines = []
        for kid, rec, res in results:
            if rec is None:
                lines.append(f"no record {kid}")
                continue
            named = [(x["name"], x.get("party"), x.get("votes")) for x in rec["result"]["candidates"]]
            dno = dno_of(rec["place"]["district"].split(",")[0])
            name = rec["place"]["district"].split(",")[0].strip().upper()
            code_contests = [m for m in contests if (dno and dno_of(m["district"]) == dno) or
                             (not dno and (m["district"].upper() == name[:3] or name.split()[0] in m["district"].upper()) and sum(m["cands"].values()) > 0)]
            ml = [(m["district"], m["post"], sorted(m["cands"].items(), key=lambda nv: -nv[1])[:8]) for m in code_contests]
            lines.append(f"record {rec['id']}: Klarner {named} total {rec['result'].get('total_votes')}; p {json.dumps(rec.get('p'))[:90]}; "
                         f"my match {json.dumps(res)[:200]}; MEDSL's lines of code {dno}: {ml}")
        untested.append((k, kind, r, lines))
    print(f"  my tally of D3's kinds: {dict(tally)}")
    print(f"  the 108 on both lists, D3's named-candidate ratio against mine: {dict(agree_flag)}")
    print(f"  the 80 'within 3% here', by my own named-candidate match: {dict(within)}")
    print(f"  the {len(untested)} D3 leaves untested (unmatched, not paired, matched to several), one by one:")
    for k, kind, r, lines in untested:
        print(f"    {k[0]} {k[1]} {k[2][6:]} {k[3]!r} [{kind[8:]}]: c38 Klarner {r['klarner']:,} vs MEDSL by {r['by']} {r['medsl']:,} (off {r['off']:+.3f}); p rests on {r.get('p_rests_on')}")
        for ln in lines:
            print(f"        {ln}")
    # the 26 settled before: my own earlier findings
    settled = [r for r in cmp_["m2"] if r["here"] == "M2 only: settled before this check"]
    print(f"  the {len(settled)} 'settled before this check': {collections.Counter((r['year'], r['state'], r['chamber']) for r in settled)} "
          f"(c38's own findings: Vermont 2018 Chittenden and Idaho 2022 Senate 1 by #97, New Hampshire 2022's doubled Senate by #95)")


# ------------------------------------------------------------------------------------------ 43.3 the coverage gate

NOT_A_CONTEST = re.compile(r"\bSTRAIGHT PARTY\b|^REGISTERED VOTERS\b|\bBALLOTS CAST\b|^VOTERS?\b|\bTURNOUT\b|\bVOTING STATISTICS\b|^$")   # the build's, copied
AGG_NAME = re.compile(r"\bTOTALS?\b|CUMULATIVE|^ALL PRECINCTS$", re.I)   # the build's local_volume.AGG_NAME, copied
COUNTY_TOTAL = re.compile(r"(^|[ _-])TOTALS?$")   # the build's medsl_precinct.COUNTY_TOTAL, copied
ANSWERS = {"YES", "NO", "FOR", "AGAINST", "APPROVE", "REJECT", "APPROVED", "REJECTED", "ACCEPT", "RETAIN", "NOT RETAIN", "DO NOT RETAIN",
           "BONDS YES", "BONDS NO", "YES ON", "NO ON", "FOR THE MEASURE", "AGAINST THE MEASURE", "IN FAVOR", "OPPOSED", "IN FAVOR OF",
           "YES FOR APPROVAL", "NO FOR REJECTION"}   # the build's, copied
COVER_GAP = 0.02


def family_of(office, district):
    """('LEG', 0/1) for a chamber's row with a district, ('US HOUSE',) for a US House row by district, else None."""
    x = WA_LEG.match(office)
    if x:
        return ("LEG", 1 if x.group(2) == "SENATOR" else 0)
    if office in LEG_NAMES:
        d = (district or "").strip().upper()
        return ("LEG", LEG_NAMES[office]) if (dno_of(d) or d) else None   # a row with no district is no district's row (22:42 item 4)
    if office == "US HOUSE":
        d = (district or "").strip().upper()
        dn = dno_of(d) or d
        return None if dn and (not dn.lstrip("0") or dn in ("AT-LARGE", "AT LARGE", "STATEWIDE")) else ("US HOUSE",)
    return None


def loose(diff, have, ps):
    """The build's _loose rule, copied: a missed precinct whose name (given once by the top contest) the family has under
    another code, or one of whose '/'-joined parts it names, is not missed."""
    if not diff or not have:
        return diff
    once = collections.Counter(q[1] for q in ps)
    names = {q[1] for q in have}
    parts = names | {x.strip() for q in have for x in q[1].split("/") if x.strip()}
    return {q for q in diff if once[q[1]] > 1 or not (q[1] in names or any(x.strip() in parts for x in q[1].split("/") if x.strip()))}


def cover_summary(path, year):
    """One raw file's coverage, county by county, cached in derived/<file>.cover.json: the top contest (the candidate contest
    with votes in the most precincts), its precincts and votes; for each family (lower, upper, us_house) the precincts with
    its rows and the top's precincts they miss [n capped by the count difference, the set difference, their votes]; every
    contest's [precincts, votes, missed n, missed votes] for the released and statewide readings."""
    base = os.path.basename(path)
    out_p = os.path.join(DERIVED, base + ".cover.json")
    if os.path.exists(out_p):
        d = L.load_json(out_p)
        if d.get("version") == 3:
            return d
    per = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0])))   # (st,county) -> contest -> pk -> [TOTAL, other]
    fam = collections.defaultdict(lambda: collections.defaultdict(set))
    questions = set()
    for r in M.rows(path):
        if (r.get("stage") or "GEN").strip().upper() != "GEN":
            continue
        cand = (r.get("candidate") or "").strip()
        if M.is_meta(cand):
            continue
        prec = r.get("precinct") or ""
        if AGG_NAME.search(prec) or COUNTY_TOTAL.search(prec.strip().upper()):
            continue
        office = (r.get("office") or "").strip().upper()
        if NOT_A_CONTEST.search(office):
            continue
        st = r.get("state_po") or r.get("state_postal") or ""
        county = M.fips5(r.get("county_fips") or "")
        pk = (" ".join((r.get("jurisdiction_fips") or r.get("jurisdiction") or "").upper().split()), " ".join(prec.upper().split()))
        district = r.get("district") or ""
        f_ = family_of(office, district)
        special = (r.get("special") or "").strip().upper() == "TRUE"
        if f_:
            fam[(st, county)][f_].add(pk)
        if special:
            continue
        try:
            v = int(float(r.get("votes") or 0))
        except ValueError:
            v = 0
        if f_ and f_[0] == "LEG":
            continue   # a chamber's rows are a family, never the top contest, as in the build
        k = f"{office}|{district}|{(r.get('dataverse') or '').upper()}"
        cell = per[(st, county)][k][pk]
        if (r.get("mode") or "").strip().upper() == "TOTAL":
            cell[0] += v
        else:
            cell[1] += v
        if cand.upper() in ANSWERS:
            questions.add((st, county, k))
    counties = {}
    for (st, county), cs in per.items():
        votes = {}
        for k, c in cs.items():
            vv = {q: max(t, o) for q, (t, o) in c.items() if max(t, o) > 0}
            if vv:
                votes[k] = vv
        tops = [k for k in votes if (st, county, k) not in questions] or list(votes)
        top = max(tops, key=lambda k: (len(votes[k]), sum(votes[k].values()))) if tops else None
        tv = votes[top] if top else {}
        ps = set(tv)
        fs = fam[(st, county)]

        def short(have):
            diff = loose(ps - have, have, ps)
            n = min(len(diff), max(0, len(ps) - len(have))) if have else len(ps)
            return [n, len(diff), sum(tv[q] for q in diff)]
        rec = {"top": top, "precincts": len(ps), "top_votes": sum(tv.values()), "families": {}}
        for name, key in (("lower", ("LEG", 0)), ("upper", ("LEG", 1)), ("us_house", ("US HOUSE",))):
            have = fs.get(key, set())
            rec["families"][name] = [len(have)] + short(have)
            if name == "us_house" and ps and have and rec["families"][name][1] / len(ps) > COVER_GAP:
                rec["us_house_missing_eg"] = sorted(" / ".join(q) for q in ps - have)[:8]
        rec["contests"] = {k: [len(votes[k]), sum(votes[k].values())] + short(set(votes[k])) for k in votes}
        counties[f"{st}|{county}"] = rec
    d = {"version": 3, "file": base, "year": year, "counties": counties}
    with open(out_p, "w") as f:
        json.dump(d, f)
    return d


def section_3():
    h1("43.3 MEDSL's coverage from the raw files: the county gate, the released contests and the statewide contests, against check-districts.json")
    chk = L.load_json(at(AFTER, "data/local/check-districts.json"))
    print("  the rule as built (D3, §32; my reading of local_districts.py): a county is short where the US House's rows (by district) miss more "
          "than 2% of the precincts of the county's top contest holding more than 2% of its votes; a state that left a US House seat off the "
          "ballot is not read; a contest whose own rows are in the county's precincts within 2% is released ('whole_contests'); a statewide "
          "contest (rows in 90% of the state's counties) is held where the votes its rows miss are over 2% of the state's, else noted")
    for year in (2018, 2022, 2024):
        cov = {}
        n_files = 0
        for y, path in M.all_raw_files():
            if y != year:
                continue
            d = cover_summary(path, year)
            n_files += 1
            cov.update(d["counties"])
        off = sorted({(c["place"]["state"], c["place"]["district"]) for c in L.load_json(at(AFTER, f"data/house/{year}.json"))["contests"]
                      if not c.get("special") and not c["result"].get("total_votes")})
        skip = {st for st, _ in off}
        mine = {}
        for k, v in sorted(cov.items()):
            st, county = k.split("|")
            n_p = v["precincts"]
            if not n_p:
                continue
            have, n, nd, votes = v["families"]["us_house"]
            share = round(votes * (n / nd if nd else 0) / v["top_votes"], 4) if v["top_votes"] else None
            if st not in skip and have and n / n_p > COVER_GAP and share is not None and share > COVER_GAP:
                whole = sorted(ck for ck, (np_, vv, n_, nd_, v_) in v["contests"].items() if np_ and n_ / n_p <= COVER_GAP)
                mine[k] = {"precincts": n_p, "top": v["top"], "top_votes": v["top_votes"], "us_house": [n, share],
                           "lower": v["families"]["lower"][1], "upper": v["families"]["upper"][1], "whole": whole, "eg": v.get("us_house_missing_eg", [])}
        theirs = chk["incomplete_counties"][str(year)]
        print(f"\n  {year}: {n_files} files, {len(cov)} counties; off the ballot (data/house): {off}; D3's: {chk['incomplete_counties'].get('off_ballot_' + str(year))}")
        print(f"    counties short by the US House's rows: mine {len(mine)} {sorted(mine)}; D3's {len(theirs)} {sorted(theirs)}; "
              f"both {len(set(mine) & set(theirs))}")
        for k in sorted(set(mine) | set(theirs)):
            m_, t_ = mine.get(k), theirs.get(k)
            if m_ and t_:
                same = (m_["precincts"] == t_["precincts"] and m_["us_house"][0] == t_["short"][0][1] and abs(m_["us_house"][1] - t_["short"][0][2]) < 5e-4
                        and m_["lower"] == t_["lower"] and m_["upper"] == t_["upper"] and m_["top_votes"] == t_["top_votes"])
                print(f"    {k}: {'the same' if same else 'DIFFER'}: mine precincts {m_['precincts']} top {m_['top']} {m_['top_votes']:,} US House missed {m_['us_house']} "
                      f"lower {m_['lower']} upper {m_['upper']} released {len(m_['whole'])} | D3 precincts {t_['precincts']} top {t_['top']} {t_['top_votes']:,} "
                      f"short {t_['short']} lower {t_['lower']} upper {t_['upper']} released {len(t_['whole_contests'])}")
                mw = {w.split("|")[0] + "|" + w.split("|")[1] for w in m_["whole"] if not w.split("|")[0] in ("US PRESIDENT", "US SENATE") or True}
                tw = set(t_["whole_contests"])
                mw2 = {"|".join(w.split("|")[:2]) for w in m_["whole"]}
                if mw2 != tw:
                    print(f"        released contests: mine {sorted(mw2)[:10]}; D3 {sorted(tw)[:10]}")
                if m_["eg"] and not same:
                    print(f"        e.g. missed: {m_['eg'][:4]}")
            elif m_:
                print(f"    {k}: mine only: precincts {m_['precincts']} top {m_['top']} US House missed {m_['us_house']} lower {m_['lower']} upper {m_['upper']}; e.g. {m_['eg'][:3]}")
            else:
                print(f"    {k}: D3 only: {t_['short']} precincts {t_['precincts']} top {t_['top']}")
        # the statewide contests: rows in 90% of the state's counties, missing over 2% of a county's precincts and votes
        n_c = collections.Counter(k.split("|")[0] for k in cov)
        spread = collections.Counter()
        for k, v in cov.items():
            st = k.split("|")[0]
            for ck in v["contests"]:
                spread[(st, ck)] += 1
        state_top = collections.Counter()
        for k, v in cov.items():
            state_top[k.split("|")[0]] += v["top_votes"]
        sw = {}
        for k, v in cov.items():
            st, county = k.split("|")
            n_p = v["precincts"]
            if not n_p or n_c[st] <= 1:
                continue
            for ck, (np_, vv, n, nd, votes) in v["contests"].items():
                if ck == v["top"] or spread[(st, ck)] < 0.9 * n_c[st]:
                    continue
                share = round(votes * (n / nd if nd else 0) / v["top_votes"], 4) if v["top_votes"] else None
                if n / n_p > COVER_GAP and share is not None and share > COVER_GAP:
                    sw.setdefault(st, {}).setdefault("|".join(ck.split("|")[:2]), {})[county] = [n, n_p, share, round(share * v["top_votes"])]
        mine_sw = {}
        for st, d in sw.items():
            for key, e in d.items():
                ss = round(sum(x[3] for x in e.values()) / state_top[st], 4)
                mine_sw[(st, key)] = (ss, "held" if ss > COVER_GAP else "noted", e)
        t_sw = {(st, key): (e["state_share"], e["verdict"], e["counties"]) for st, d in chk["statewide_short"][str(year)].items() for key, e in d.items()}
        both = set(mine_sw) & set(t_sw)
        same_v = sum(1 for k in both if mine_sw[k][1] == t_sw[k][1] and abs(mine_sw[k][0] - t_sw[k][0]) < 5e-4)
        print(f"    statewide contests short in a county: mine {len(mine_sw)}, D3's {len(t_sw)}, both {len(both)}, the same share and verdict {same_v}")
        print(f"      held, mine: {sorted(k for k, v in mine_sw.items() if v[1] == 'held')}")
        print(f"      held, D3's: {sorted(k for k, v in t_sw.items() if v[1] == 'held')}")
        for k in sorted(set(mine_sw) ^ set(t_sw))[:12]:
            v = mine_sw.get(k) or t_sw.get(k)
            print(f"      {'mine only' if k in mine_sw else 'D3 only'}: {k} share {v[0]} {v[1]} counties {list(v[2].items())[:3]}")
        for k in sorted(both):
            if not (mine_sw[k][1] == t_sw[k][1] and abs(mine_sw[k][0] - t_sw[k][0]) < 5e-4):
                print(f"      differ: {k} mine {mine_sw[k][:2]} {list(mine_sw[k][2].items())[:3]} D3 {t_sw[k][:2]} {list(t_sw[k][2].items())[:3]}")
    # the gate's effect on the records (the moves): Monroe's Assembly, Kennebec's two, New York's Proposal One
    print("\n  the gate on the records at d680bd4 [measured from the records]:")
    for f, ids in (("data/state-lower/2024/NY.json", [f"2024-state-lower-NY-{d}" for d in (130, 133, 134, 135, 136, 137, 138, 139)]),
                   ("data/measure/2024/NY.json", ["2024-measure-NY-STATE_PROPOSAL_ONE"]),
                   ("data/local/2018/ME.json", None)):
        b, a = records_at(BEFORE, f), records_at(AFTER, f)
        if ids is None:
            ids = [i for i in a if "23011" in json.dumps(a[i].get("place") or {}) or "Kennebec" in json.dumps(a[i].get("place") or {})]
            ids = [i for i in ids if (a[i].get("held_reason") or "") != (b.get(i, {}).get("held_reason") or "")]
        for i in ids:
            ra, rb = a.get(i), b.get(i)
            if ra is None:
                print(f"    {i}: not at {AFTER}")
                continue
            print(f"    {i}: p before {C40.pval(rb or {})} after {C40.pval(ra)}; held_reason after: {str(ra.get('held_reason'))[:160]}")


# ------------------------------------------------------------------------------------------ 43.4 the coarse tier

def section_4():
    h1("43.4 The coarse tier from Klarner's file and D1's and D2's counts: Idaho 1984-1990 (the 2x line) and South Carolina's Senate 1976 and 1980")
    rows = [r for r in csv.DictReader(open(KLARNER, encoding="utf-8", errors="replace")) if r["etype"] == "g"]
    cases = {("SC", 1976): ("president", (1,)), ("SC", 1980): ("president", (1,)), ("ID", 1984): ("president", (0, 1)),
             ("ID", 1986): ("governor", (0, 1)), ("ID", 1988): ("president", (0, 1)), ("ID", 1990): ("governor", (0, 1))}   # the build's COARSE, copied
    mv = L.load_json(at(AFTER, "data/local/moves-district-checks.json"))
    lost = {r[0] for r in mv["records"] if "L" in r[8]}
    for (st, year), (level, chambers) in sorted(cases.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        turn = next(sum(x["votes"] or 0 for x in c["result"]["candidates"]) for c in L.load_json(at(AFTER, f"data/{level}/{year}.json"))["contests"]
                    if c["place"]["state"] == st and not c.get("special"))
        for sen in chambers:
            sel = [r for r in rows if r["sab"] == st and int(r["year"]) == year and r["sen"] == str(sen)]
            byd = collections.defaultdict(list)
            for r in sel:
                byd[(r["dname"], r["dno"])].append(r)
            tot = lambda r: int(r["dvote"] or 0) + int(r["rvote"] or 0) + int(r["ovote"] or 0)   # noqa: E731
            one_post = sum(max(tot(r) for r in rs) for rs in byd.values())
            x = one_post / turn
            x_all = sum(tot(r) for r in sel) / turn
            chamber = "Senate" if sen else "House"
            if x <= 1:
                print(f"  {st} {year} {chamber}: {len(sel)} posts in {len(byd)} districts; one post per district {one_post:,} = {x:.3f}x the {turn:,} votes for {level}; "
                      f"all posts {x_all:.3f}x: no district held (the posts explain the chamber's total)")
                continue
            ratio = {d: max(tot(r) for r in rs) / (turn * len(rs) / len(sel)) for d, rs in byd.items()}
            held = sorted((d for d, rr in ratio.items() if rr > 2.0), key=lambda d: int(d[1]))
            posts_held = sum(len(byd[d]) for d in held)
            # the records lost at d680bd4 for these districts
            lv = "state-upper" if sen else "state-lower"
            lost_here = sorted(i for i in lost if i.startswith(f"{year}-{lv}-{st}-"))
            lost_d = sorted({re.sub(r"__seat_\d+$", "", i.split(f"-{st}-")[1]) for i in lost_here}, key=lambda s: int(s))
            print(f"  {st} {year} {chamber}: {len(sel)} posts in {len(byd)} districts; one post per district {one_post:,} = {x:.3f}x the {turn:,} votes for {level} "
                  f"(all posts {x_all:.3f}x); over the 2x line: {[d[1] for d in held]} ({posts_held} posts; ratios {[round(ratio[d], 2) for d in held]}); "
                  f"the others' largest ratio {max(rr for d, rr in ratio.items() if d not in held):.2f}; "
                  f"p lost at {AFTER} in the file: {len(lost_here)} posts of districts {lost_d}; equal: {[d[1] for d in held] == lost_d}")
            near = sorted(((round(rr, 3), d[1]) for d, rr in ratio.items() if 1.6 < rr <= 2.0), reverse=True)[:4]
            if near:
                print(f"      nearest under the line: {near}")
    # the kept posts' notes and the held reasons at d680bd4
    cnt = collections.Counter()
    for year in (1984, 1986, 1988, 1990):
        for lv in ("state-lower", "state-upper"):
            a = records_at(AFTER, f"data/{lv}/{year}/ID.json")
            for i, r in a.items():
                notes = " ".join(r.get("notes") or [])
                if r.get("held_reason") and C40.pval(r) is None:
                    cnt[(year, "held, no p" if "2 times" in str(r.get("held_reason")) else "held, another reason")] += 1
                elif "within 2 times" in notes or "kept [measured]" in notes:
                    cnt[(year, "kept with the note")] += 1
                else:
                    cnt[(year, "neither")] += 1
    print(f"  Idaho's records at {AFTER}: {dict(sorted(cnt.items()))} (D3: 21 posts held a year, 84 in all; 420 kept with a note)")
    for year in (1976, 1980):
        a = records_at(AFTER, f"data/state-upper/{year}/SC.json")
        n = sum(1 for r in a.values() if "counted per voter" in " ".join(r.get("notes") or []))
        print(f"  South Carolina's Senate {year}: {len(a)} records, {n} with the posts note, {sum(1 for r in a.values() if r.get('held_reason'))} held")


# ------------------------------------------------------------------------------------------ 43.5 the flags' outcomes

def section_5():
    h1(f"43.5 Every flag of check-districts.json and its outcome on the records at {AFTER}")
    chk = L.load_json(at(AFTER, "data/local/check-districts.json"))
    recs_b, recs_a = {}, {}
    tally = collections.Counter()
    bad = []
    lost_by_year = collections.Counter()
    for year, v in chk["years"].items():
        print(f"  {year}: {json.dumps(v['tallies'])}")
        for f in v["flags"]:
            kid = f["id"]
            y, st, lv, key = kid_parts(kid)
            path = f"data/{lv}/{y}/{st}.json"
            if path not in recs_a:
                recs_a[path] = records_at(AFTER, path)
                recs_b[path] = records_at(BEFORE, path)
            ra = next((r for r in recs_a[path].values() if rec_key(r["place"]["district"]) == key), None)
            rb = next((r for r in recs_b[path].values() if rec_key(r["place"]["district"]) == key), None)
            out = f["outcome"]
            if ra is None:
                tally[(out, "no record at AFTER")] += 1
                bad.append((kid, out, "no record"))
                continue
            dump = json.dumps(ra)
            notes = " ".join(ra.get("notes") or []) + " " + json.dumps(ra.get("result", {}).get("note") or "")
            # a legislative record has no held_reason field: a held one says so in p.not_computed ("neither count is relied on")
            held = bool(ra.get("held_reason")) or "neither count is relied on" in json.dumps(ra.get("p") or {})
            pa, pb = C40.pval(ra), C40.pval(rb or {})
            if out == "held":
                ok = held and pa is None
                if ok and pb is not None:
                    lost_by_year[year] += 1
            elif out == "noted":
                ok = "MEDSL" in dump and not held   # the rule (21:26): "a gap under 5% is kept with a note"
            elif out.startswith("kept"):
                ok = "MEDSL" in dump and not held   # the rule (22:26 (b)): "stays, with a note naming the counties and the share missing"
            elif out == "write-in rule":
                ok = any((x.get("party") or "").lower() in ("w", "write-in", "writein") or x.get("write_in") for x in ra["result"]["candidates"]) or "write-in" in notes.lower()
            elif out == "MEDSL taken":
                ok = (ra["result"].get("source") == "medsl") or "MEDSL's counts" in notes
            elif out == "settled by the state":
                ok = ra["result"].get("source") not in (None, "klarner") or "canvass" in notes.lower()
            elif out == "settled earlier":
                ok = True
            elif out.startswith("untested"):
                ok = not held or bool(rb and rb.get("held_reason"))
            else:
                ok = False
            tally[(out, "as the outcome says" if ok else "NOT as the outcome says")] += 1
            if not ok:
                bad.append((kid, out, {"held": held, "p": pa, "source": ra["result"].get("source"), "notes": notes[:160]}))
    print("  outcomes on the records: " + "; ".join(f"{o} / {s}: {n}" for (o, s), n in sorted(tally.items())))
    print(f"  held flags whose record had a p before: {dict(lost_by_year)} (D3: 2016 52, 2018 22, 2022 30 = 104)")
    mv = L.load_json(at(AFTER, "data/local/moves-district-checks.json"))
    lost_ids = {r[0] for r in mv["records"] if "L" in r[8] and r[1].split("/")[2] in ("2016", "2018", "2022") and r[1].split("/")[1].startswith("state-")}
    held_recs = set()
    for year, v in chk["years"].items():
        for f in v["flags"]:
            if f["outcome"] == "held":
                y, st, lv, key = kid_parts(f["id"])
                path = f"data/{lv}/{y}/{st}.json"
                r = next((r for r in recs_a.get(path, {}).values() if rec_key(r["place"]["district"]) == key), None)
                if r:
                    held_recs.add(r["id"])
    print(f"  the file's p lost in 2016/2018/2022 (state legislatures): {len(lost_ids)}; the held flags' records: {len(held_recs)}; lost but not a held flag's record: "
          f"{sorted(lost_ids - held_recs)[:8]}; held flags' records not lost: {sorted(held_recs - lost_ids)[:8]}")
    for b in bad[:12]:
        print(f"    {b}")


# ------------------------------------------------------------------------------------------ 43.6 the over-ballot rows added

def section_6():
    h1(f"43.6 check-over-ballot.json: the rows added at {AFTER} (the state's own counts tested too, 21:55 (2))")
    b = L.load_json(at(BEFORE, "data/local/check-over-ballot.json"))
    a = L.load_json(at(AFTER, "data/local/check-over-ballot.json"))

    def rows_of(d):
        out = {}
        for y, v in d.items():
            if not str(y).isdigit():
                continue
            for r in (v if isinstance(v, list) else v.get("rows", [])):
                out[(y, r["state"], r["office"], r.get("district"))] = r
        return out
    rb, ra = rows_of(b), rows_of(a)
    new = {k: r for k, r in ra.items() if k not in rb}
    gone = [k for k in rb if k not in ra]
    changed = [(k, rb[k], ra[k]) for k in ra if k in rb and (rb[k].get("verdict") != ra[k].get("verdict") or rb[k].get("votes") != ra[k].get("votes") or rb[k].get("figure") != ra[k].get("figure"))]
    print(f"  rows before {len(rb)}, after {len(ra)}; added {len(new)} (D3: 31), gone {len(gone)}, changed {len(changed)}")
    print(f"  added, by verdict: {collections.Counter(r.get('verdict') for r in new.values())}; by state and year: {collections.Counter((k[0], k[1]) for k in new)}")
    for k, r in sorted(new.items()):
        if r.get("verdict") != "passes":
            print(f"    {k}: {json.dumps(r)[:240]}")
    for k, x, y in changed[:10]:
        print(f"    changed: {k}: {x.get('votes')} {x.get('figure')} {x.get('verdict')} -> {y.get('votes')} {y.get('figure')} {y.get('verdict')}")
    # the added rows: the ratio's arithmetic, the figure against the file's other rows of the same state and day (the
    # day's top is one figure), and the votes against the record's own total at d680bd4
    arith = fig_same = fig_diff = votes_same = votes_diff = no_rec = 0
    for k, r in sorted(new.items()):
        y, st = k[0], k[1]
        if r.get("ratio") is not None and r.get("figure"):
            arith += abs(r["votes"] / r["figure"] - r["ratio"]) < 6e-5
        others = [x for kk, x in rb.items() if kk[0] == y and kk[1] == st and x.get("against") == r.get("against") and x.get("figure")]
        if others:
            if any(x["figure"] == r["figure"] for x in others):
                fig_same += 1
            else:
                fig_diff += 1
                print(f"    figure differs from the day's other rows: {k}: {r.get('figure')} ({r.get('of')}) others {sorted({x['figure'] for x in others})[:3]}")
        # the record
        recs = records_at(AFTER, f"data/local/{y}/{st}.json")
        hit = [x for x in recs.values() if (x.get("office") or x.get("title") or "").upper() == r["office"] and
               ((x.get("place") or {}).get("district") or None) in (r.get("district"), None, "", "STATEWIDE") and x["result"].get("total_votes") == r["votes"]]
        if hit:
            votes_same += 1
        else:
            near = [x for x in recs.values() if (x.get("office") or x.get("title") or "").upper() == r["office"]]
            if near:
                votes_diff += 1
                print(f"    votes differ from the record's: {k}: row {r['votes']} records {[x['result'].get('total_votes') for x in near][:3]}")
            else:
                no_rec += 1
    print(f"  the added rows: ratio = votes / figure in {arith} of {len(new)}; figure equal to the day's other rows' {fig_same}, differing {fig_diff}; "
          f"votes equal to a record's total {votes_same}, differing {votes_diff}, no record of the office found {no_rec}")


def main():
    want = [int(x) for x in sys.argv[1:]] or [1, 2, 3, 4, 5, 6]
    for n in want:
        globals()[f"section_{n}"]()


if __name__ == "__main__":
    main()
