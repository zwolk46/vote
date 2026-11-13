"""c46: the eighth pass's section 18, D3's #106 (the district checks' second pass, main 72d1d60) against 78a82f2.

The orchestrator, 2026-11-13 04:45 UTC: "D3's #106, the district checks' second pass, is merged as 72d1d60 (REPORT §34;
moves-district-checks-2.json against 510b089; check-districts-new.json). Check it in your next section, with its end at
72d1d60. Check four things: the 284 newly tested records and their outcomes; Indiana 2016's archive settling 39 flags; the
Census county lists holding 12 records of 2022; and Michigan's precinct-name joins (1,930 to 829). Check also Rutland on
MEDSL's counts (x1.72) and Arenac's clerk settling HD99. My compare: 40 gained, 1 lost, 16,739 moved, none over 2x."

Sections (each from my own reading of the raw files, the state and county files fetched once more
(checks/m2/fetch_eighth_pass.sh; the Census's two zips from D3's copies at /mnt/project-files/d3/census-sld/, their
sha256 checked) and the records at the two commits; nothing from pipeline/ imported; a rule of the build that must be
applied is copied here and says so):
  46.1  moves-district-checks-2.json against my own diff of every record, 78a82f2 -> 72d1d60; the p moved over 2x
  46.2  the 284 newly tested records: D3's matcher copied piece by piece (name keys, compound parts, weak write-ins,
        the number among several hits, pairing, the two tests) on my records at 78a82f2 and my MEDSL summaries, each
        record's pairs, sums, flags and outcome beside D3's; the "another district's contest" rule; D3's rerun of my 249
  46.3  Indiana's 2016 results archive and Utah's 2016 canvass, read apart: every Indiana 2016 flag and Utah's three
  46.4  the Census's 2022 block equivalency files: each district's counties and block shares; the 22 flags with a
        Census gap, whether any flag still held has one, and what MEDSL's file holds in the counties I read as gaps
        and D3 does not (rows of 0 votes)
  46.5  Michigan's precinct names: my copy of the join rule on MEDSL's 2022 Michigan rows against D3's lists; every
        join of the 829 under the rule; Wayne's top contest and its US House gap; Ottawa's REJECTED lines
  46.6  Vermont 2018: Rutland's precincts, ballots and counts; Franklin held; the over-seats figures of every held flag
  46.7  Michigan 2022: Wayne's nameless Senate lines (3 and 10), House 10's write-in line, House 27, House 99 by county
        and Arenac's official file, the Attorney General's rows
  46.8  DC 2018's at-large Council: the Board's certified PDF, the record's seats and reason, the over-ballot entry
  46.9  Virginia 2023: the 65 name-keyed notes and the three unconfirmed
  46.10 D2's governor totals and Maine's 2nd district: no p moved; the second counts beside MEDSL's from my summaries;
        Indiana 2018's class B moves
Run from the repository root: python3 -I checks/m2/c46_district_checks_2.py [1 2 3 4 5 6 7 8 9 10]
"""
import collections
import io
import itertools
import json
import os
import re
import subprocess
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402
import m2medsl as M  # noqa: E402
import c40_pr_checks as C40  # noqa: E402
import c41_governor_refit as C41  # noqa: E402
import c42_held_totals as C42  # noqa: E402
import c43_district_checks as C43  # noqa: E402

BEFORE, AFTER = "78a82f2", "72d1d60"
SRC = os.path.join(L.CACHE, "eighth", "src")
KLARNER_IDS_WITH_RECORDS = {}


def h1(s):
    print("\n" + "=" * 100 + f"\n{s}\n" + "=" * 100)


def at(commit, rel):
    return os.path.join(C41.worktree(commit), rel)


def records_at(commit, f):
    return C42.records_at(C41.worktree(commit), f)


def alnum(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def rec_norm(place_district):
    m = re.match(r"^(.*?)(?:,\s*(?:seat|position|post)\s*(\w+))?$", (place_district or "").strip().lower())
    return (alnum(m.group(1)), (m.group(2) or "").lower())


def kid_norm(kid):
    """'2018-VT-lower-bennington-2-2-' -> (2018, 'VT', 'state-lower', ('bennington2', '2'))."""
    head, dno, geopost, mmdpost = kid.rsplit("-", 3)
    year, st, ch, dname = head.split("-", 3)
    return int(year), st, "state-" + ch, (alnum(dname + " " + dno), (geopost or mmdpost or "").lower())


_REC_CACHE = {}


def record_of(kid, commit=AFTER):
    year, st, lv, key = kid_norm(kid)
    f = f"data/{lv}/{year}/{st}.json"
    ck = (commit, f)
    if ck not in _REC_CACHE:
        recs = records_at(commit, f)
        _REC_CACHE[ck] = {rec_norm(r["place"]["district"]): r for r in recs.values()}
    return _REC_CACHE[ck].get(key)


# ------------------------------------------------------------------------------------------ 46.1 the moves file

def section_1():
    h1(f"46.1 moves-district-checks-2.json against my own diff of every record, {BEFORE} -> {AFTER}")
    mv = L.load_json(at(AFTER, "data/local/moves-district-checks-2.json"))
    rows = {}
    for r in mv["records"]:
        rows.setdefault(r[0], []).append(r)
    print(f"  the file: {len(mv['records'])} rows, {len(rows)} ids, against {mv.get('against')} (the code alone, its data main's at {BEFORE}; my diff is main to main)")
    print(f"  its summary: {json.dumps(mv['summary'])}")
    files = subprocess.run(["git", "diff", "--name-only", BEFORE, AFTER, "--", "data/"], capture_output=True, text=True, cwd=L.ROOT).stdout.split()
    data_files = [f for f in files if re.match(r"^data/(local|primary|measure|state-lower|state-upper)/\d{4}/[A-Z]{2}\.json$", f)
                  or re.match(r"^data/(governor|house|senate|president)/\d{4}\.json$", f)]
    print(f"  data files changed: {len(files)}; record files: {len(data_files)} {dict(collections.Counter(f.split('/')[1] for f in data_files))}; "
          f"other: {[f for f in files if f not in data_files]}")
    mine = collections.Counter()
    agree, dis, seen, worst, stamps, pdiff, rdiff = 0, collections.Counter(), set(), [], 0, 0, 0
    within = collections.Counter()
    moved, new_p, lost_p = [], [], []
    d2 = []
    for f in data_files:
        lv, yr = f.split("/")[1], f.split("/")[2].split(".")[0]
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
            pb, pa = C40.pval(b.get(i) or {}), C40.pval(a.get(i) or {})
            if lv in ("governor", "house", "senate", "president"):
                d2.append((i, c, d[:6], pb, pa))
                continue
            if c == "P":
                moved.append((pa / pb if pb else None, i, lv, yr))
                other = [x for x in d if not (x.startswith("p.") or x.startswith("forecasts") or x.startswith("forecast_inputs") or x in ("p", "two_party"))]
                if pb and abs(pa / pb - 1) <= 0.01 and not other:
                    within[(lv, yr)] += 1
                    seen.add(i)
                    continue
            if c == "N":
                new_p.append((i, pa))
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
    # the counts within 1%
    theirs_w = mv.get("p_moved_within_1pct", {})
    tw = {(lv, yr): v["records"] for lv, d in theirs_w.items() for yr, v in d.items()}
    same = sum(1 for k in set(tw) | set(within) if tw.get(k, 0) == within.get(k, 0))
    print(f"  p moved within 1% and nothing else, by level and year: mine {sum(within.values())} in {len(within)} cells, the file {sum(tw.values())} in {len(tw)}; cells equal {same} of {len(set(tw) | set(within))}; "
          f"differing: {[(k, within.get(k, 0), tw.get(k, 0)) for k in sorted(set(tw) | set(within)) if tw.get(k, 0) != within.get(k, 0)][:8]}")
    # the p moved, in all
    mv_all = [m for m in moved if m[0] is not None]
    over2 = [m for m in mv_all if m[0] > 2 or m[0] < 0.5]
    print(f"  p moved (every P in my diff): {len(mv_all)}; over 2x either way: {len(over2)} {over2[:5]}; extremes: min {min(mv_all)[0]:.4f} {min(mv_all)[1]}, max {max(mv_all)[0]:.4f} {max(mv_all)[1]}")
    bands = collections.Counter()
    for r, i, lv, yr in mv_all:
        x = abs(r - 1)
        bands[(lv, "<=1%" if x <= 0.01 else "1-10%" if x <= 0.10 else "10-12%" if x <= 0.12 else ">12%")] += 1
    print(f"  by band: {dict(sorted(bands.items()))}")
    big = sorted([m for m in mv_all if abs(m[0] - 1) > 0.10], key=lambda m: m[0])
    print(f"  moved more than 10%: {len(big)}: " + "; ".join(f"{i} x{r:.4f}" for r, i, lv, yr in big))
    print(f"  new p (N): {len(new_p)} {collections.Counter(i.split('-')[1] + ' ' + i.split('-')[3] + ' ' + i.split('-')[0] for i, _ in new_p)}")
    print(f"  p lost (L): {len(lost_p)} {lost_p}")
    print(f"  D2's records in my diff (governor, house): {len(d2)}: " + "; ".join(f"{i} {c} {d}" + (f" p {pb}->{pa}" if pb != pa else "") for i, c, d, pb, pa in d2))
    ct = L.load_json(at(AFTER, "data/congress/check-totals.json"))
    print(f"  data/congress/check-totals.json: {json.dumps({k: (v if not isinstance(v, (list, dict)) else len(v)) for k, v in ct.items()})[:600]}")


# ------------------------------------------------------------------------------------------ 46.2 the 284 newly tested

def strong_line(rec):
    """The write-in rule's strong line, copied: 10% of the last winner's votes."""
    w = [c.get("votes") or 0 for c in rec["result"]["candidates"] if c.get("won")]
    return 0.1 * min(w) if w else 0.0


# ---- D3's matcher of #106, copied piece by piece (pipeline/local_districts.py: _part, _finds, _named, _ballot_sized, match,
# pair, test; pipeline/local_medsl.py: name_key, name_keys, _is_generic; pipeline/local.py: on_ballot, NH_COUNTY), run on my own
# records and my own volume summaries of MEDSL's files. Said here because the rule checked is the rule copied: a difference
# between my outcome and D3's then comes from the inputs, not from another reading of the rule. Inputs that differ: my summaries
# hold no recount stage (D3 prefers a 'GEN RECOUNT' contest among several hits) and no writein column (a MEDSL write-in is read
# from its name alone); the seats are the record's winners (D3: Klarner's eseats).

SUFFIXES = {"JR", "SR", "II", "III", "IV", "V"}
PART_MIN = 3          # D3's PART_MIN: a compound surname's part is matched only from three letters, and with the first initial
RATIO_OFF = 0.03      # D3's RATIO_OFF: (a) off 1 by more than this
WRITE_IN_STRONG = 0.10   # pipeline/local.py's WRITE_IN_STRONG
D3_GENERIC = re.compile(r"^\s*$|^OTHERS?$|\bALL OTHERS\b|SCATTER|\bVOIDS?\b|\bBLANKS?\b|FEDERAL BALLOTS|\bTOTALS?\b|"
                        r"OVER ?VOTES?|UNDER ?VOTES?|NONE OF THE|UNCOMMITTED|EXHAUSTED|\bUNRESOLVED\b|"
                        r"^(AFFIDAVIT|FEDERAL|ABSENTEE(/MILITARY)?|MILITARY|MANUALLY COUNTED EMERGENCY|EMERGENCY|"
                        r"SPECIAL PRESIDENTIAL|PUBLIC COUNTER)$", re.I)
NOT_VOTES = re.compile(r"OVER ?VOTES?|UNDER ?VOTES?|\bBLANKS?\b|\bVOIDS?\b|\bTOTALS?\b|FEDERAL BALLOTS", re.I)
WRITE_IN_MARK = re.compile(r"\(W/I\)|\bWRITE[- ]?IN\b", re.I)
NH_COUNTY = {"belknap": "33001", "carroll": "33003", "cheshire": "33005", "coos": "33007", "grafton": "33009",
             "hillsborough": "33011", "merrimack": "33013", "rockingham": "33015", "strafford": "33017", "sullivan": "33019"}


def letters(s):
    return re.sub(r"[^A-Z]", "", s.upper())


def name_key(name):
    """(surname, first initial), from MEDSL's 'FIRST MIDDLE LAST' or Klarner's 'last, first middle' (local_medsl.name_key, copied)."""
    n = re.sub(r'"[^"]*"|\([^)]*\)', " ", name.upper()).replace(".", " ")
    if "," in n:
        last, rest = n.split(",", 1)
        first = [t for t in rest.split() if letters(t) and letters(t) not in SUFFIXES]
        return letters(last), (letters(first[0])[:1] if first else "")
    toks = [t for t in n.split() if letters(t) and letters(t) not in SUFFIXES]
    if not toks:
        return "", ""
    return letters(toks[-1]), letters(toks[0])[:1]


def name_keys(name):
    """name_key, and for 'FIRST MIDDLE LAST' also the last two words run together (local_medsl.name_keys, copied)."""
    k = name_key(name)
    out = {k}
    if "," not in name:
        n = re.sub(r'"[^"]*"|\([^)]*\)', " ", name.upper()).replace(".", " ")
        toks = [letters(t) for t in n.split() if letters(t) and letters(t) not in SUFFIXES]
        if len(toks) >= 3:
            out.add((toks[-2] + toks[-1], k[1]))
    return out


def medsl_is_generic(name):   # local_medsl._is_generic, copied
    n = name.strip().upper()
    return n in {"WRITE-IN", "WRITEIN", "WRITE IN", "SCATTERING", "WRITE-INS"} or n.startswith("*") or "WRITE" in n


def generic(x):   # local_districts._generic, copied
    n = x["name"].strip()
    return bool(D3_GENERIC.search(n)) or (medsl_is_generic(n) and not re.search(r"[A-Z]{2,}\s+[A-Z]{2,}", re.sub(
        r"\(?W/I\)?|WRITE[- ]?INS?:?", "", n.upper())))


def surs(name):
    return {k[0] for k in name_keys(name)}


def part(s, t):   # local_districts._part, copied
    if s == t:
        return True
    a, b = (s, t) if len(s) < len(t) else (t, s)
    return len(a) >= PART_MIN and (b.startswith(a) or b.endswith(a))


def finds(key, keys):   # local_districts._finds, copied
    s, i = key
    return any(s == t for t, _ in keys) or any(part(s, t) and i and i == j for t, j in keys)


def is_write_in(x):   # local_districts._is_write_in; my summaries carry no writein column, so the name alone
    return bool(x.get("writein")) or bool(WRITE_IN_MARK.search(x["name"]))


def rec_cands(rec):
    """The record's candidates in the shape D3's functions read: party 'w' for a write-in line, scattering flagged."""
    out = []
    for c in rec["result"]["candidates"]:
        name = (c.get("name") or "").strip()
        p = (c.get("party") or "").lower()
        out.append({"name": name, "party": "w" if p in ("write-in", "writein", "w") else p, "votes": c.get("votes") or 0,
                    "scattering": name.lower() == "scattering" or bool(C43.GENERIC.search(name)), "won": bool(c.get("won"))})
    return out


def rec_seats(rec):
    return max(1, len([c for c in rec["result"]["candidates"] if c.get("won")]))


def on_ballot(cands):   # local.on_ballot, copied
    named = [a for a in cands if not a["scattering"] and a["party"] != "w"]
    named.sort(key=lambda a: -(a["votes"] or 0))
    return named


def named_of(cands, seats):   # local_districts._named, copied
    named = [a for a in cands if not a["scattering"]]
    ballot = sorted([a for a in named if a["party"] != "w"], key=lambda a: -(a["votes"] or 0))
    k = seats or 1
    last = (ballot[k - 1]["votes"] or 0) if len(ballot) >= k else 0
    return [a for a in named if not (a["party"] == "w" and (a["votes"] or 0) < max(1, WRITE_IN_STRONG * last))]


def contest_cands(m):
    if "_cands" not in m:
        m["_cands"] = [{"name": n, "votes": v} for n, v in m["cands"].items()]
        ms = set()
        for x in m["_cands"]:
            ms |= name_keys(x["name"])
        m["_keys"] = ({t for t, _ in ms}, ms)
    return m["_cands"]


def last_line(mc, seats):
    lines = sorted((x["votes"] or 0 for x in mc if not generic(x)), reverse=True)
    return lines[seats - 1] if len(lines) >= seats else 0


def pair(cands, seats, m):   # local_districts.pair, copied
    named = [a for a in cands if not a["scattering"]]
    must = {id(a) for a in named_of(cands, seats)}
    left = [x for x in contest_cands(m) if not generic(x)]
    out = {}
    for a in sorted(named, key=lambda a: -(a["votes"] or 0)):
        s, i = name_key(a["name"])
        hit = [x for x in left if s in surs(x["name"])]
        if not hit:
            hit = [x for x in left if finds((s, i), name_keys(x["name"]))]
        else:
            whole = set().union(*(surs(x["name"]) for x in hit))
            hit += [x for x in left if x not in hit and finds((s, i), name_keys(x["name"])) and surs(x["name"]) <= whole]
        if len(hit) > 1:
            hit = [x for x in hit if name_key(x["name"])[1] == i] or hit
        if len(hit) > 1:
            hit = [max(hit, key=lambda x: x["votes"] or 0)]
        if not hit:
            if id(a) in must:
                return None
            continue
        out[id(a)] = hit[0]
        left.remove(hit[0])
    return out


def ballot_sized(cands, seats, m):   # local_districts._ballot_sized, copied
    pr = pair(cands, seats, m)
    if pr is None:
        return False
    k = seats or 1
    ballot = on_ballot(cands)
    kl = (ballot[k - 1]["votes"] or 0) if len(ballot) >= k else 0
    ml = last_line(contest_cands(m), k)
    return all((pr[id(a)]["votes"] or 0) >= WRITE_IN_STRONG * ml for a in ballot
               if id(a) in pr and (a["votes"] or 0) >= WRITE_IN_STRONG * kl)


def match(cands, seats, dno, pool, st, dname):   # local_districts.match, copied (no recount stage in my summaries)
    named = named_of(cands, seats)
    ks = [name_key(a["name"]) for a in named]
    if not ks or not all(k[0] for k in ks):
        return []
    hits = []
    for m in pool:
        contest_cands(m)
        s, ms = m["_keys"]
        if all(k[0] in s or finds(k, ms) for k in ks):
            hits.append(m)
    if len(hits) > 1 and dno:
        h = [m for m in hits if C43.dno_of(re.sub(r"\D", "", m["district"] or "") or None) == str(int(dno))]
        hits = h or hits
    if len(hits) > 1 and st == "NH":
        h = [m for m in hits if NH_COUNTY.get(dname) in (m.get("counties") or {})]
        hits = h or hits
    if len(hits) > 1:
        h = [m for m in hits if ballot_sized(cands, seats, m)]
        hits = h or hits
    return hits


def d3_match(rec, contests):
    """D3's match, pair and test on one record: the same outputs as c43's my_match (pairs, klarner, medsl, ratio, others,
    district, file) with D3's flag_a, flag_b and unopposed; unmatched where the hits are not one, or the one hit bears another
    district's number (D3's 'another district's contest')."""
    cands = rec_cands(rec)
    seats = rec_seats(rec)
    head = rec["place"]["district"].split(",")[0].strip()
    mt = re.search(r"(\d+)$", head)
    dno = mt.group(1) if mt else None   # D3's kc["dno"]: the district's number ('Addison 5' -> 5; 'Bennington 2, position 2' -> 2)
    dname = re.sub(r"[\s\d]+$", "", head).strip().lower()
    # D3's pool holds the general stage only (medsl_contests: stage GEN or GEN RECOUNT, not special); my summaries carry the
    # special's name in the district ('1st Suffolk and Middlesex SPECIAL', Massachusetts 2016)
    contests = [m for m in contests if "SPECIAL" not in (m["district"] or "").upper()]
    hits = match(cands, seats, dno, contests, rec["place"]["state"], dname)
    named = named_of(cands, seats)
    if len(hits) != 1:
        return {"matched": False, "hits": len(hits), "named": len(named)}
    m = hits[0]
    if C43.dno_of(head) and C43.dno_of(m["district"]) and C43.dno_of(m["district"]) != C43.dno_of(head):
        return {"matched": False, "hits": 1, "named": len(named), "other_district": m["district"], "key": m["key"]}
    pr = pair(cands, seats, m)
    if pr is None:
        return {"matched": False, "hits": 1, "named": len(named), "unpaired": True}
    allnamed = [a for a in cands if not a["scattering"]]
    paired = [a for a in allnamed if id(a) in pr]
    kv = sum(a["votes"] or 0 for a in paired if a["votes"])
    mv = sum(pr[id(a)]["votes"] or 0 for a in paired if a["votes"])
    used = {id(x) for x in pr.values()}
    mc = contest_cands(m)
    others = [x for x in mc if id(x) not in used and not generic(x) and (x["votes"] or 0) > 0]
    kkeys = {name_key(a["name"]) for a in allnamed}
    others = [x for x in others if not any(finds(k, name_keys(x["name"])) for k in kkeys)]
    unopposed = len(on_ballot(cands)) <= (seats or 1)
    ratio = mv / kv if kv else None
    return {"matched": True, "key": m["key"], "pairs": [(a["name"], a["votes"], pr[id(a)]["name"], pr[id(a)]["votes"]) for a in paired],
            "klarner": kv, "medsl": mv, "ratio": ratio, "flag_a": ratio is not None and abs(ratio - 1) > RATIO_OFF,
            "unopposed": unopposed, "others": [(x["name"], x["votes"]) for x in others], "flag_b": unopposed and bool(others),
            "district": m["district"], "file": m["file"], "seats": seats}


_WI_CACHE = {}


def writein_names(year, st):
    """{candidate name upper: True} for the rows marked writein TRUE in the state's raw file(s) of the year (2018+)."""
    if (year, st) in _WI_CACHE:
        return _WI_CACHE[(year, st)]
    out = set()
    for y, path in M.all_raw_files():
        if y != year or year == 2016:
            continue
        base = os.path.basename(path).lower()
        if not (base.startswith(f"{year}-{st.lower()}-") or base.startswith(st.lower()) or base.startswith(f"{st.lower()}22") or base.startswith(f"{st.lower()}_")):
            continue
        for r in M.rows(path):
            if (r.get("state_po") or "").upper() != st:
                continue
            if (r.get("writein") or "").strip().upper() == "TRUE":
                out.add((r.get("candidate") or "").strip().upper())
    _WI_CACHE[(year, st)] = out
    return out


def section_2():
    h1("46.2 The 284 newly tested records (check-districts-new.json): D3's matcher copied piece by piece, on my records and my MEDSL summaries, beside D3's pairs and outcomes")
    new = L.load_json(at(AFTER, "data/local/check-districts-new.json"))
    chk = L.load_json(at(AFTER, "data/local/check-districts.json"))
    flags = {f["id"]: f for v in chk["years"].values() for f in v["flags"]}
    cont_cache = {}
    tally = collections.Counter()
    out_tally = collections.Counter()
    bad, nofile, noted = [], [], []
    for y, v in new["years"].items():
        print(f"  {y}: newly tested {len(v['newly_tested'])} (before: {dict(collections.Counter(r['before'] for r in v['newly_tested']))}); "
              f"outcomes {dict(collections.Counter(r['outcome'] for r in v['newly_tested']))}; outcome changed {len(v['outcome_changed'])}; no longer tested {len(v.get('no_longer_tested', []))}")
        for e in v["newly_tested"]:
            kid = e["id"]
            year, st, lv, key = kid_norm(kid)
            # the record at BEFORE: Klarner's counts as D3's check read them (at AFTER a 'write-in rule' record carries MEDSL's
            # write-in lines as candidates, and Rutland MEDSL's counts)
            rec = record_of(kid, BEFORE)
            if rec is None:
                tally["no record found"] += 1
                bad.append((kid, "no record"))
                continue
            ck = (year, st)
            if ck not in cont_cache:
                cont_cache[ck] = C43.leg_contests(year, st)
            sen = 1 if lv == "state-upper" else 0
            res = d3_match(rec, [m for m in cont_cache[ck] if m["sen"] == sen])
            if not res["matched"]:
                have_file = any(m["sen"] == sen for m in cont_cache[ck])
                tally["mine unmatched" if have_file else "mine unmatched: no MEDSL file of the chamber in my caches"] += 1
                if have_file:
                    bad.append((kid, f"mine unmatched {json.dumps(res)[:160]}; D3 {e['medsl_district']} {e['klarner']} {e['medsl']} {e['outcome']}"))
                else:
                    nofile.append(kid)
                continue
            tally["matched"] += 1
            weak = {x["name"] for x in rec["result"]["candidates"] if (x.get("party") or "").lower() in ("write-in", "writein", "w") and (x.get("votes") or 0) < strong_line(rec)}
            k_strong = sum(p[1] for p in res["pairs"] if p[0] not in weak)
            m_strong = sum(p[3] for p in res["pairs"] if p[0] not in weak)
            ok_k = res["klarner"] == e["klarner"] or k_strong == e["klarner"]
            ok_m = res["medsl"] == e["medsl"] or m_strong == e["medsl"]
            ok_d = C43.dno_of(res["district"]) == C43.dno_of(e["medsl_district"]) if C43.dno_of(e["medsl_district"]) else res["district"].upper().replace(" ", "") == e["medsl_district"].upper().replace(" ", "")
            tally["Klarner sum equal" if ok_k else "Klarner sum differs"] += 1
            tally["MEDSL sum equal" if ok_m else "MEDSL sum differs"] += 1
            tally["district equal" if ok_d else "district differs"] += 1
            # my flags
            fa, fb = res["flag_a"], res["flag_b"]
            mine_flags = set(["a"] if fa else []) | set(["b"] if fb else [])
            theirs = set(e.get("flags") or [])
            tally["flags equal" if mine_flags == theirs else "flags differ"] += 1
            if not (ok_k and ok_m and ok_d and mine_flags == theirs):
                bad.append((kid, f"mine K {res['klarner']} M {res['medsl']} d {res['district']} flags {sorted(mine_flags)} pairs {res['pairs'][:4]} others {res['others'][:3]}; "
                                 f"D3 K {e['klarner']} M {e['medsl']} d {e['medsl_district']} flags {e.get('flags')} {e['outcome']}"))
            # the outcome against the flags and the record
            oc = e["outcome"]
            out_tally[oc] += 1
            f = flags.get(kid)
            if oc == "passes":
                ok = not theirs and not mine_flags and f is None
            elif oc == "write-in rule":
                wi = writein_names(year, st) if year != 2016 else set()
                ok = "b" in theirs and f is not None and all(n in wi or "WRITE" in n for n, _ in res["others"]) and abs((res["ratio"] or 0) - 1) <= 0.03
                if not ok:
                    bad.append((kid, f"write-in rule: others {res['others'][:4]} marked write-in in the raw file: {[n in wi for n, _ in res['others']][:4]}; ratio {res['ratio']}"))
            elif oc.startswith("kept"):
                ok = f is not None and bool((f.get("coverage") or {}).get("gaps"))
            elif oc.startswith("settled by the state"):
                ok = f is not None and st in ("IN", "UT")
            elif oc == "noted":
                ok = f is not None and (("a" in theirs and abs(f["ratio"] - 1) < 0.05) or "b" in theirs)
                noted.append((kid, f"ratio {f.get('ratio') if f else None} flags {sorted(theirs)} others {res['others'][:3]} b_tested {(f or {}).get('b_tested')} unopposed {(f or {}).get('unopposed')}"))
            elif oc == "held":
                ok = f is not None and "a" in theirs
            elif oc == "MEDSL taken":
                ok = f is not None and f.get("over_seats") and f["over_seats"].get("over")
            else:
                ok = False
            tally["outcome consistent" if ok else "outcome inconsistent"] += 1
            if not ok and oc != "noted":
                bad.append((kid, f"outcome {oc} not consistent: flags {sorted(theirs)} in check-districts {f is not None} coverage {(f or {}).get('coverage')}"))
    print(f"  my tally: {dict(tally)}")
    print(f"  outcomes: {dict(out_tally)}")
    print(f"  untested by me for want of the chamber's MEDSL file in my caches ({len(nofile)}): {dict(collections.Counter(k.split('-')[0] + ' ' + k.split('-')[1] for k in nofile))}")
    print(f"  the noted ({len(noted)}): " + "; ".join(f"{k}: {w}" for k, w in noted))
    print(f"  records to look at ({len(bad)}):")
    for kid, why in bad:
        print(f"    {kid}: {why}")
    # the record no longer tested, and the "another district's contest" rule on it and Texas 2016 House 42
    for kid in ("2016-HI-lower--51--", "2016-TX-lower--42--"):
        rec = record_of(kid)
        year, st, lv, key = kid_norm(kid)
        ck = (year, st)
        if ck not in cont_cache:
            cont_cache[ck] = C43.leg_contests(year, st)
        res = d3_match(rec, [m for m in cont_cache[ck] if m["sen"] == (1 if lv == "state-upper" else 0)]) if rec else None
        print(f"  {kid}: Klarner {[(x['name'], x.get('party'), x.get('votes')) for x in rec['result']['candidates']] if rec else None}; p after {json.dumps((rec or {}).get('p'))[:120]}; my matcher: {json.dumps(res)[:300]}")
    print(f"  D3's tallies: " + "; ".join(f"{y}: " + ", ".join(f"{k} {v}" for k, v in sorted(chk['years'][y]['tallies'].items()) if 'another' in k or k in ('tested', 'unmatched', 'matched to several')) for y in chk["years"]))
    # D3's rerun of my 249
    cmp_ = L.load_json(at(AFTER, "data/local/check-districts-m2.json"))
    cmp_b = L.load_json(at(BEFORE, "data/local/check-districts-m2.json"))
    print(f"  D3's comparison with my 249 (check-districts-m2.json): before {json.dumps(cmp_b['tally'])}; after {json.dumps(cmp_['tally'])}")
    moved_kind = [(r["year"], r["state"], r["chamber"], r["district"], b["here"], r["here"]) for r in cmp_["m2"]
                  for b in cmp_b["m2"] if (b["year"], b["state"], b["chamber"], b["district"]) == (r["year"], r["state"], r["chamber"], r["district"]) and b["here"] != r["here"]]
    print(f"  my districts whose kind changed: {len(moved_kind)}: " + "; ".join(f"{y} {s} {c[6:]} {d!r}: {b} -> {a}" for y, s, c, d, b, a in moved_kind))


# ------------------------------------------------------------------------------------------ 46.3 Indiana's archive, Utah's canvass

def in_archive():
    """{(sen, district number): [(name, votes, write_in)]} from the archive's two legislative files, read apart."""
    out = {}
    for sen, fn in ((1, "OffCatC_1766_A.json"), (0, "OffCatC_1787_A.json")):
        with open(os.path.join(SRC, "in_enr_2016", fn), encoding="utf-8-sig") as f:
            d = json.load(f)
        d = d.get("Root", d)
        races = (d.get("StatewideSummary") or {}).get("Race") or []
        for r in (races if isinstance(races, list) else [races]):
            mt = re.search(r"District 0*(\d+)$", r["OFFICE_TITLE"].strip())
            cs = (r.get("Candidates") or {}).get("Candidate") or []
            if mt:
                out[(sen, mt.group(1))] = [(x["NAME_ON_BALLOT"].replace("(W/I)", "").strip(), int(x.get("TOTAL") or 0), "(W/I)" in x["NAME_ON_BALLOT"])
                                           for x in (cs if isinstance(cs, list) else [cs])]
    return out


def surname_match(klarner_name, archive_name):
    sur = C43.ktokens(klarner_name)
    toks = set(C43.mtokens(archive_name))
    return any(t in toks or any(len(x) >= 5 and t.endswith(x) for x in toks) for t in sur)


def ut_canvass_totals():
    """The Utah canvass's multi-county Senate page: each candidate's TOTAL figure, by the column its name starts in."""
    txt = subprocess.run(["pdftotext", "-layout", os.path.join(SRC, "ut_lg", "2016-General-Election-Statewide-Canvass-3.pdf"), "-"],
                         capture_output=True, text=True, check=True).stdout.split("\n")
    out = {}
    for i, line in enumerate(txt):
        if "Deana Froerer" in line and "Allen M. Christensen" in line:
            names = [(m.start(), m.group(0).strip()) for m in re.finditer(r"\S+(?: \S+)*", line)]
            # the next line can continue a wrapped name ('Michael Joseph' / 'Seguin (Write-in)')
            for j in range(i + 1, min(i + 60, len(txt))):
                if re.match(r"^\s*TOTAL\b", txt[j]):
                    nums = [(m.start(), m.group(0)) for m in re.finditer(r"[\d,]+", txt[j]) if m.start() > 10]
                    for pos, num in nums:
                        nearest = min(names, key=lambda nm: abs(nm[0] - pos))
                        out[nearest[1]] = int(num.replace(",", ""))
                    break
            break
    return out


def section_3():
    h1("46.3 Indiana's 2016 results archive and Utah's 2016 canvass, read apart from D3's readers")
    idx = {}
    for line in open(os.path.join(SRC, "index.txt")):
        p = line.rstrip("\n").split("\t")
        if len(p) >= 6:
            idx[p[0]] = p
    for k in ("in2016:settings", "in2016:categories", "in2016:OffCatC_1766", "in2016:OffCatC_1787", "ut:canvass2016", "dc:certified2018", "arenac:official2022"):
        p = idx.get(k)
        print(f"  {k}: http {p[1]} at {p[2]} UTC, {p[6]} bytes, sha256 {p[5][:16]}..." if p else f"  {k}: not fetched")
    with open(os.path.join(SRC, "in_enr_2016", "settings.json"), encoding="utf-8-sig") as f:
        st_ = json.load(f).get("Root", {})
    print(f"  the archive's settings: CurrentElection {st_.get('CurrentElection')}, WriteTime {st_.get('WriteTime')}, Certified {json.dumps(st_.get('Certified'))!s} "
          f"(keys holding 'ertif': {[k for k in st_ if 'ertif' in k]})")
    arch = in_archive()
    print(f"  the archive's legislative contests: {len([k for k in arch if k[0] == 1])} Senate, {len([k for k in arch if k[0] == 0])} House; write-in lines {sum(1 for v in arch.values() for c in v if c[2])}")
    chk = L.load_json(at(AFTER, "data/local/check-districts.json"))
    chk_b = L.load_json(at(BEFORE, "data/local/check-districts.json"))
    before = {f["id"]: f for f in chk_b["years"]["2016"]["flags"]}
    fl = [f for f in chk["years"]["2016"]["flags"] if f["id"].startswith("2016-IN-")]
    print(f"  Indiana 2016's flags at {AFTER}: {len(fl)} {dict(collections.Counter(f['outcome'] for f in fl))}; at {BEFORE}: "
          f"{dict(collections.Counter(f['outcome'] for f in chk_b['years']['2016']['flags'] if f['id'].startswith('2016-IN-')))}")
    tally = collections.Counter()
    for f in fl:
        kid = f["id"]
        rec = record_of(kid)
        year, st, lv, key = kid_norm(kid)
        dno = kid.split("-")[4]
        a = arch.get((1 if lv == "state-upper" else 0, dno))
        if rec is None or a is None:
            tally["no record or no archive contest"] += 1
            print(f"    {kid}: record {rec is not None}, archive contest {a is not None}")
            continue
        named = [x for x in rec["result"]["candidates"] if (x.get("votes") or 0) > 0 and not C43.GENERIC.search(x["name"])]
        ok_all, worst = True, 0.0
        lines = []
        for x in named:
            hits = [c for c in a if surname_match(x["name"], c[0])]
            if len(hits) != 1:
                ok_all = False
                lines.append(f"{x['name']} {x['votes']}: archive {hits}")
                continue
            off = hits[0][1] / x["votes"] - 1 if x["votes"] else None
            worst = max(worst, abs(off)) if off is not None else worst
            if off is None or abs(off) > 0.03:
                ok_all = False
            lines.append(f"{x['name']} K {x['votes']:,} A {hits[0][1]:,} ({off:+.4f})")
        settled = f["outcome"].startswith("settled by the state")
        tally[("archive agrees within 3%" if ok_all else "archive disagrees or unmatched", "D3 settled" if settled else f"D3 {f['outcome']}")] += 1
        exact = all(" (+0.0000)" in ln for ln in lines)
        if not ok_all or not settled:
            print(f"    {kid}: {f['outcome']} (before: {before.get(kid, {}).get('outcome')}); ratio {f.get('ratio')}; {'; '.join(lines)}")
        elif not exact:
            print(f"    {kid}: settled, archive within 3% but not exact: {'; '.join(lines)}")
    print(f"  Indiana 2016, flag by flag: {dict(tally)}")
    n_set = [f["id"] for f in fl if f["outcome"].startswith("settled by the state")]
    was = collections.Counter(before.get(i, {}).get("outcome", "not flagged before (newly tested)") for i in n_set)
    print(f"  settled by the state: {len(n_set)}; what they were at {BEFORE}: {dict(was)}")
    # every Indiana 2016 record's count against the archive, flagged or not (does the archive agree where MEDSL does?)
    recs = records_at(AFTER, "data/state-lower/2016/IN.json")
    recs.update(records_at(AFTER, "data/state-upper/2016/IN.json"))
    agree = collections.Counter()
    for r in recs.values():
        sen = 1 if r["level"] == "state-upper" else 0
        a = arch.get((sen, C43.dno_of(r["place"]["district"])))
        if a is None:
            agree["no archive contest"] += 1
            continue
        named = [x for x in r["result"]["candidates"] if (x.get("votes") or 0) > 0 and not C43.GENERIC.search(x["name"])]
        offs = []
        for x in named:
            hits = [c for c in a if surname_match(x["name"], c[0])]
            offs.append(hits[0][1] / x["votes"] - 1 if len(hits) == 1 and x["votes"] else None)
        if any(o is None for o in offs):
            agree["a candidate unmatched"] += 1
        elif all(abs(o) < 1e-9 for o in offs):
            agree["exact"] += 1
        elif all(abs(o) <= 0.03 for o in offs):
            agree["within 3%"] += 1
        else:
            agree["off"] += 1
            ms = [m for m in C43.leg_contests(2016, "IN") if m["sen"] == sen and C43.dno_of(m["district"]) == C43.dno_of(r["place"]["district"])]
            print(f"    off the archive: {r['id']} Klarner {[(x['name'], x['votes']) for x in named]}; archive {a}; MEDSL's lines {[sorted(m['cands'].items(), key=lambda nv: -nv[1])[:5] for m in ms]}")
    print(f"  every Indiana 2016 record against the archive: {dict(agree)}")
    # Utah
    tot = ut_canvass_totals()
    print(f"  Utah's canvass, the multi-county Senate page's TOTAL row by name: {tot}")
    ut = records_at(AFTER, "data/state-upper/2016/UT.json")
    for d in ("19", "20", "23"):
        r = [x for x in ut.values() if x["place"]["district"].strip() == d][0]
        f = [x for x in chk["years"]["2016"]["flags"] if x["id"] == f"2016-UT-upper--{d}--"]
        lines = []
        for x in r["result"]["candidates"]:
            hit = [(n, v) for n, v in tot.items() if surname_match(x["name"], n)]
            lines.append(f"{x['name']} K {x.get('votes')} canvass {hit}")
        print(f"    Senate {d}: outcome {f[0]['outcome'] if f else 'no flag'} (before {before.get(f'2016-UT-upper--{d}--', {}).get('outcome')}); {'; '.join(lines)}; p {json.dumps(r.get('p'))[:80]}")
    first = [ln.strip() for ln in subprocess.run(["pdftotext", "-l", "1", "-layout", os.path.join(SRC, "ut_lg", "2016-General-Election-Statewide-Canvass-3.pdf"), "-"], capture_output=True, text=True).stdout.split("\n") if ln.strip()]
    print("  the canvass's heading, as pdftotext gives the first page: " + " | ".join(first[:4]))


# ------------------------------------------------------------------------------------------ 46.4 the Census's counties

def census_districts():
    """{'ST|sen|district number': Counter(county FIPS -> blocks)} from the two zips (each block's GEOID's first five digits
    are its county; a district coded with letters is left out, as D3 does)."""
    out = collections.defaultdict(collections.Counter)
    for chamber, sen in (("sldu", 1), ("sldl", 0)):
        zp = os.path.join(SRC, "census_sld", f"{chamber}_2022.zip")
        with zipfile.ZipFile(zp) as z:
            for member in z.namelist():
                if not member.endswith(".txt"):
                    continue
                st = member.split("_")[1]
                with z.open(member) as raw:
                    for line in io.TextIOWrapper(raw, encoding="latin-1"):
                        g, _, d = line.strip().partition(",")
                        if not g.isdigit() or not d.strip().isdigit():
                            continue
                        out[f"{st}|{sen}|{int(d)}"][g[:5]] += 1
    return out


def raw_rows_by_county(year, st, counties):
    """{(office, district number, county fips): [rows, votes, precincts]} from the state's raw MEDSL file(s) of the year, every
    office, for the counties named; a state's file is the one whose name carries the state's code (2018 and later)."""
    out = {}
    for y, path in M.all_raw_files():
        if y != year:
            continue
        base = os.path.basename(path).lower()
        if not (f"-{st.lower()}-" in base or base.startswith(st.lower())):
            continue
        for r in M.rows(path):
            c = (r.get("county_fips") or "").strip()
            if c not in counties or (r.get("state_po") or "").upper() != st:
                continue
            try:
                v = int(float(r.get("votes") or 0))
            except ValueError:
                v = 0
            k = ((r.get("office") or "").upper(), C43.dno_of(r.get("district")) or (r.get("district") or "").strip(), c)
            e = out.setdefault(k, [0, 0, set()])
            e[0] += 1
            e[1] += v
            e[2].add(r.get("precinct"))
    return out



def section_4():
    h1("46.4 The Census's 2022 block equivalency files: each district's counties, against D3's Census gaps on the 2022 flags")
    for fn in ("sldu_2022.zip", "sldl_2022.zip"):
        p = os.path.join(SRC, "census_sld", fn)
        meta = L.load_json(p + ".meta.json")
        print(f"  {fn}: {os.path.getsize(p):,} bytes, sha256 {L.sha256(p)} (D3's .meta.json: {meta.get('sha256')}, fetched {meta.get('finished_utc')} from {meta.get('url')})")
    cen = census_districts()
    print(f"  districts read: {len(cen)} ({len([k for k in cen if k.split('|')[1] == '1'])} upper, {len([k for k in cen if k.split('|')[1] == '0'])} lower); states {len({k.split('|')[0] for k in cen})}")
    chk = L.load_json(at(AFTER, "data/local/check-districts.json"))
    chk_b = L.load_json(at(BEFORE, "data/local/check-districts.json"))
    before = {f["id"]: f for f in chk_b["years"]["2022"]["flags"]}
    fl = chk["years"]["2022"]["flags"]
    cont_cache = {}
    extra = []
    tally = collections.Counter()
    for f in fl:
        kid = f["id"]
        year, st, lv, key = kid_norm(kid)
        sen = 1 if lv == "state-upper" else 0
        dno = C43.dno_of(kid.split("-")[4])
        if not dno:
            tally["named district (no number)"] += 1
            continue
        c = cen.get(f"{st}|{sen}|{dno}")
        if not c:
            tally["no Census district"] += 1
            print(f"    {kid}: no Census district {st}|{sen}|{dno}")
            continue
        total = sum(c.values())
        # MEDSL's counties of the district: the contest's own rows (my volume summaries), votes in the county
        if (year, st) not in cont_cache:
            cont_cache[(year, st)] = C43.leg_contests(year, st)
        ms = [m for m in cont_cache[(year, st)] if m["sen"] == sen and C43.dno_of(m["district"]) == dno]
        medsl_counties = {k for m in ms for k, v in (m.get("counties") or {}).items() if v}
        my_gaps = {k: round(v / total, 4) for k, v in c.items() if k not in medsl_counties}
        d3_gaps = {g[0]: g[2] for g in (f.get("coverage") or {}).get("gaps", []) if g[1] == "census"}
        d3_all = {g[0] for g in (f.get("coverage") or {}).get("gaps", [])}
        d3_census = set((f.get("coverage") or {}).get("census_counties") or [])
        if f.get("coverage") is None:
            tally["D3 read no coverage (coverage null)"] += 1
            if my_gaps and not ms:
                tally["  of them, no MEDSL contest of the district in my summaries"] += 1
            elif my_gaps:
                tally["  of them, with a Census county that has no row of the district"] += 1
                print(f"    {kid}: {f['outcome']} (ratio {f.get('ratio')}), D3 read no coverage; Census counties {sorted(c)}; MEDSL's rows of the district in {sorted(medsl_counties)}; counties with no row {my_gaps}")
            continue
        same_list = set(c) == d3_census
        tally["Census county list equal to D3's" if same_list else "Census county list differs"] += 1
        same_gaps = set(my_gaps) == set(d3_gaps) and all(abs(my_gaps[k] - d3_gaps[k]) <= 1.5e-4 for k in my_gaps)
        same_any = set(my_gaps) == d3_all
        tally["Census gaps equal" if same_gaps else "gaps equal counting D3's plain gaps" if same_any else "gaps differ"] += 1
        if (my_gaps or d3_gaps or not same_list) and not same_gaps and not same_any:
            print(f"    {kid}: {f['outcome']} (before {before.get(kid, {}).get('outcome', 'not flagged')}); Census counties {len(c)} (D3 {len(d3_census)}{'' if same_list else ' DIFFER'}); "
                  f"my gaps (no row of the district in MEDSL's contest) {my_gaps}; D3's census gaps {d3_gaps}; MEDSL contests {len(ms)} counties {sorted(medsl_counties)}")
            if f["outcome"].startswith("held") and my_gaps:
                print(f"      ** still held with a Census county that has no row **")
        for county in my_gaps:
            if county not in d3_all:
                extra.append((kid, year, st, sen, dno, county, my_gaps[county], f["outcome"]))
    print(f"  the 2022 flags against the Census: {dict(tally)}")
    # the counties I list as gaps and D3 does not: what MEDSL's file holds there (D3's rows_in counts a county with any row of
    # the district, a row of 0 votes too; my summaries count a county with votes)
    print(f"  counties a gap in my reading and not in D3's ({len(extra)}): the chamber's rows MEDSL's file holds there")
    for (year, st), grp in itertools.groupby(sorted(extra, key=lambda e: (e[1], e[2])), key=lambda e: (e[1], e[2])):
        grp = list(grp)
        rows = raw_rows_by_county(year, st, {e[5] for e in grp})
        later = raw_rows_by_county(year + 2, st, {e[5] for e in grp}) if year in (2016, 2022) else {}
        for kid, _, _, sen, dno, county, share, oc in grp:
            office = "STATE SENATE" if sen else "STATE HOUSE"
            r = rows.get((office, dno, county), [0, 0, set()])
            allv = sum(v[1] for k, v in rows.items() if k[2] == county)
            legv = sum(v[1] for k, v in rows.items() if k[2] == county and k[0] == office)
            l2 = later.get((office, dno, county), [0, 0, set()])
            print(f"    {kid} ({oc}): county {county} (Census share {share}): rows of the district {r[0]} in {len(r[2])} precincts, votes {r[1]:,}; "
                  f"the county's {office} rows carry {legv:,} votes over every district, all its offices {allv:,}; the {year + 2} file: {l2[0]} rows, {l2[1]:,} votes")
    kept = [f for f in fl if f["outcome"].startswith("kept") and any(g[1] == "census" for g in (f.get("coverage") or {}).get("gaps", []))]
    was = collections.Counter(before.get(f["id"], {}).get("outcome", "not flagged before") for f in kept)
    only_census = [f for f in kept if all(g[1] == "census" for g in f["coverage"]["gaps"])]
    print(f"  kept with a Census gap: {len(kept)} (before: {dict(was)}); kept by the Census alone (no other gap): {len(only_census)}: "
          f"{[(f['id'], before.get(f['id'], {}).get('outcome')) for f in only_census]}")
    print(f"  of those, held or noted before -> kept now: {len([f for f in only_census if before.get(f['id'], {}).get('outcome') in ('held', 'noted')])}")
    # the share threshold: the smallest Census share that kept a record
    shares = sorted((g[2], f["id"]) for f in kept for g in f["coverage"]["gaps"] if g[1] == "census")
    print(f"  Census shares of the gaps: smallest {shares[:3]}, largest {shares[-3:]}")


# ------------------------------------------------------------------------------------------ 46.5 Michigan's precinct names

P_GENERIC = {"THE", "OF", "CHARTER", "PRECINCT", "PCT", "AND"}   # D3's P_GENERIC, copied
P_SAME = {"TWP": "TOWNSHIP"}   # D3's P_SAME, copied
WATCH = {"HEIGHTS", "EAST", "WEST", "NORTH", "SOUTH", "CITY", "TOWNSHIP", "VILLAGE", "AVCB", "PART", "UPPER", "LOWER"}


def edits(a, b, cap=2):   # D3's _edits, copied
    if abs(len(a) - len(b)) > cap:
        return cap + 1
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        if min(cur) > cap:
            return cap + 1
        prev = cur
    return prev[-1]


def pcore(name):   # D3's _pcore, copied
    name = re.sub(r",? A MICHIGAN CITY\b", "", name)
    toks = re.findall(r"[A-Z]+|\d+", name)
    nums = tuple(str(int(t)) for t in toks if t.isdigit())
    words = tuple(sorted(P_SAME.get(t, t) for t in toks if not t.isdigit() and t not in P_GENERIC and not (len(t) >= 6 and edits(t, "PRECINCT") <= 2)))
    return words, nums


def near(cw, w):   # D3's near, copied: the same words, or one word apart by one letter, both of six letters or more
    if cw == w:
        return True
    a, b = collections.Counter(cw), collections.Counter(w)
    da, db = list((a - b).elements()), list((b - a).elements())
    return len(da) == len(db) == 1 and min(len(da[0]), len(db[0])) >= 6 and edits(da[0], db[0], 1) <= 1


def join_names(ps, names):   # D3's precinct_equivalences, copied
    extra = {q for q in names if q not in ps}
    lone = collections.defaultdict(list)
    for c in ps:
        w, n = pcore(c[1])
        lone[(c[0], n)].append((c, w))
    out = {}
    for q in sorted(extra):
        w, n = pcore(q[1])
        hit = [c for c, cw in lone.get((q[0], n), []) if near(cw, w)]
        if len(hit) == 1:
            out[q] = hit[0]
    return out


def pnorm(s):
    """D3's normalization before the match, copied: case, spacing and Excel's _x000D_."""
    return " ".join(s.replace("_x000D_", " ").upper().split())


def mi_2022_rows():
    for y, path in M.all_raw_files():
        if os.path.basename(path) == "2022-mi-local-precinct-general.zip":
            return path, M.rows(path)
    raise SystemExit("no Michigan 2022 file")


def michigan_coverage():
    """MEDSL's 2022 Michigan rows, county by county: every contest's precincts and votes (a precinct's votes its TOTAL
    mode's or its other modes' sum, whichever is more), with D3's question rule copied (a contest is a question only where
    its answer lines hold most of its votes) and its nameless-party-line rule (a nameless line with a party is a line)."""
    path, it = mi_2022_rows()
    cells = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(int))))
    # county -> contest -> precinct key -> mode -> votes
    ans = collections.defaultdict(lambda: [0, 0])   # (county, contest) -> [answer-line votes, all votes]
    rejected = collections.Counter()
    for r in it:
        if (r.get("stage") or "GEN").upper() != "GEN":
            continue
        cand = (r.get("candidate") or "").strip()
        if M.is_meta(cand) and not (cand == "" and (r.get("party_simplified") or "").strip()):
            continue
        office = (r.get("office") or "").strip().upper()
        if C43.NOT_A_CONTEST.search(office):
            continue
        county = M.fips5(r.get("county_fips") or "")
        key = (office, (r.get("district") or "").strip().upper(), (r.get("special") or "").strip().upper() == "TRUE")
        pk = (r.get("jurisdiction_fips") or "", pnorm(r.get("precinct") or ""))
        try:
            v = int(float(r.get("votes") or 0))
        except ValueError:
            v = 0
        mode = (r.get("mode") or "TOTAL").upper()
        cells[county][key][pk][mode] += v
        if cand.upper() in C43.ANSWERS:
            ans[(county, key)][0] += v
            if cand.upper() == "REJECTED":
                rejected[(county, office)] += v
        ans[(county, key)][1] += v
    out = {}
    for county, contests in cells.items():
        cc = {}
        for key, pks in contests.items():
            a, t = ans[(county, key)]
            question = t > 0 and a > t / 2
            prec = {}
            for pk, modes in pks.items():
                tot = modes.get("TOTAL", 0)
                other = sum(v for m, v in modes.items() if m != "TOTAL")
                prec[pk] = max(tot, other)
            cc[key] = {"question": question, "precincts": prec}
        out[county] = cc
    return out, rejected


def section_5():
    h1("46.5 Michigan 2022's precinct names: my copy of the join rule on MEDSL's rows, against D3's lists; Wayne's top contest and gaps")
    chk = L.load_json(at(AFTER, "data/local/check-districts.json"))
    pe = chk["precinct_equivalences"]
    allj = [(y, k, a, b) for y in ("2016", "2018", "2022", "2024") for k, v in pe[y].items() for a, b in v]
    print(f"  D3's joins: {len(allj)} in all; by year {dict(collections.Counter(y for y, _, _, _ in allj))}; Michigan 2022's {len([1 for y, k, _, _ in allj if y == '2022' and k.startswith('MI|')])}, Wayne's {len([1 for y, k, _, _ in allj if k == 'MI|26163'])}")
    # every join under my copy of the rule, and the watch words
    fail, watch = [], []
    for y, k, a, b in allj:
        ja, jb = a.split(" / ", 1), b.split(" / ", 1)
        wa, na = pcore(pnorm(ja[1] if len(ja) > 1 else a))
        wb, nb = pcore(pnorm(jb[1] if len(jb) > 1 else b))
        if not (na == nb and near(wa, wb) and ja[0] == jb[0]):
            fail.append((y, k, a, b))
        da = (set(wa) ^ set(wb)) & WATCH
        if da:
            watch.append((y, k, a, b, sorted(da)))
    print(f"  joins my copy of the rule would not make: {len(fail)} {fail[:6]}")
    print(f"  joins whose differing words are in the watch list {sorted(WATCH)}: {len(watch)} {watch[:6]}")
    # D3's own first-rule examples, checked absent
    for pat in ("DEARBORN HEIGHTS", "AVCB", "PART A", "LONE ELM"):
        hits = [(a, b) for y, k, a, b in allj if pat in a or pat in b]
        bad = [(a, b) for a, b in hits if pcore(pnorm(a.split(' / ', 1)[-1]))[0] != pcore(pnorm(b.split(' / ', 1)[-1]))[0]]
        print(f"    '{pat}': joins naming it {len(hits)}, of which the two names' words differ: {len(bad)} {bad[:3]}")
    # my own joins on Michigan's rows
    cov, rejected = michigan_coverage()
    print(f"  Michigan 2022's rows: {len(cov)} counties; REJECTED lines by county and office: {dict(rejected)}")
    mine = {}
    tops = {}
    for county, contests in cov.items():
        cand_c = {k: v for k, v in contests.items() if not v["question"] and not k[2]}
        if not cand_c:
            continue
        top = max(cand_c.items(), key=lambda kv: (len([p for p, v in kv[1]["precincts"].items() if v > 0]), sum(kv[1]["precincts"].values())))
        ps = {p for p, v in top[1]["precincts"].items() if v > 0}
        tops[county] = (top[0], len(ps), sum(top[1]["precincts"].values()))
        names = set()
        for k, v in contests.items():
            names |= {p for p, vv in v["precincts"].items() if vv > 0}
        j = join_names(ps, names)
        mine[county] = {f"{q[0]} / {q[1]}": f"{c[0]} / {c[1]}" for q, c in j.items()}
    d3 = {}
    for k, v in pe["2022"].items():
        if k.startswith("MI|"):
            d3[k.split("|")[1]] = {a: b for a, b in v}
    counties = sorted(set(mine) | set(d3))
    eq = sum(1 for c in counties if mine.get(c, {}) == d3.get(c, {}))
    print(f"  Michigan's counties with joins: mine {len([c for c in mine if mine[c]])}, D3 {len(d3)}; counties where the two sets are equal: {eq} of {len(counties)}; "
          f"joins mine {sum(len(v) for v in mine.values())}, D3's {sum(len(v) for v in d3.values())}")
    for c in counties:
        if mine.get(c, {}) != d3.get(c, {}):
            m, d = mine.get(c, {}), d3.get(c, {})
            print(f"    {c}: mine only {[(a, b) for a, b in m.items() if d.get(a) != b][:4]}; D3 only {[(a, b) for a, b in d.items() if m.get(a) != b][:4]}")
    print(f"  the top contest by county (my rule copy): {dict(collections.Counter(t[0][0] for t in tops.values()))}; Wayne: {tops.get('26163')}")
    # Wayne's US House and Attorney General gaps after the joins
    w = cov["26163"]
    top_key = tops["26163"][0]
    ps = {p for p, v in w[top_key]["precincts"].items() if v > 0}
    top_votes = {p: v for p, v in w[top_key]["precincts"].items()}
    j = join_names(ps, {p for k, v in w.items() for p, vv in v["precincts"].items() if vv > 0})
    for fam, keys in (("US House", [k for k in w if k[0] == "US HOUSE"]), ("Attorney General", [k for k in w if k[0] == "ATTORNEY GENERAL"]), ("State House", [k for k in w if k[0] == "STATE HOUSE"]), ("State Senate", [k for k in w if k[0] == "STATE SENATE"])):
        have = set()
        for k in keys:
            have |= {j.get(p, p) for p, v in w[k]["precincts"].items() if v > 0}
        miss = ps - have
        print(f"    Wayne, {fam} rows ({len(keys)} contests): precincts of the top contest missed {len(miss)} of {len(ps)} ({len(miss) / len(ps):.1%}), "
              f"holding {sum(top_votes[p] for p in miss) / sum(top_votes.values()):.2%} of its votes; e.g. {sorted(miss)[:4]}")
    print(f"    Wayne's joins (mine): {len(mine.get('26163', {}))}; the Brownston ones: {len([a for a in mine.get('26163', {}) if 'BROWNSTON,' in a or 'BROWNSTON ' in a])}; "
          f"D3's: {len(d3.get('26163', {}))}")
    # Indiana 2022 Senate 21's Howard County gap, and the statewide-short entries
    ss = chk.get("statewide_short", {})
    print(f"  statewide_short at {AFTER}: {json.dumps({y: len(v) for y, v in ss.items()}) if isinstance(ss, dict) else len(ss)}")
    txt = json.dumps(ss)
    for word in ("Aroostook", "23003", "ATTORNEY GENERAL", "26163"):
        print(f"    '{word}' in statewide_short: {txt.count(word)}")
    inc = chk.get("incomplete_counties", {})
    inc_b = L.load_json(at(BEFORE, "data/local/check-districts.json")).get("incomplete_counties", {})
    print(f"  incomplete_counties: {json.dumps({y: len(v) for y, v in inc.items()})} (before {json.dumps({y: len(v) for y, v in inc_b.items()})})")
    for y in inc:
        if not isinstance(inc[y], list):
            continue
        for c in inc[y]:
            if isinstance(c, dict) and str(c.get("county") or c.get("fips")) in ("18067", "26163"):
                print(f"    {y} {json.dumps(c)[:400]}")
            elif isinstance(c, str) and ("18067" in c or "26163" in c):
                print(f"    {y} {c[:400]}")


# ------------------------------------------------------------------------------------------ 46.6 Vermont 2018

STATEWIDE_ONE_SEAT = {"US SENATE", "GOVERNOR", "LIEUTENANT GOVERNOR", "ATTORNEY GENERAL", "SECRETARY OF STATE", "STATE TREASURER", "AUDITOR OF ACCOUNTS", "US PRESIDENT"}


def section_6():
    h1("46.6 Vermont 2018: Rutland on MEDSL's counts (x1.72), Franklin held, the over-seats figures of every held flag")
    path = [p for y, p in M.all_raw_files() if os.path.basename(p) == "2018-vt-precinct-general.zip"][0]
    sen = collections.defaultdict(lambda: collections.defaultdict(int))    # district -> (county, jur, precinct) -> votes
    sen_c = collections.defaultdict(lambda: collections.defaultdict(int))  # district -> candidate -> votes
    county_p = collections.defaultdict(set)                                 # county -> precincts (any contest)
    sw = collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0]))   # office -> precinct -> [candidate votes, all lines]
    mount_holly = collections.Counter()
    for r in M.rows(path):
        if (r.get("stage") or "GEN").upper() != "GEN":
            continue
        pk = (r.get("county_fips"), r.get("jurisdiction_fips"), r.get("precinct"))
        county_p[r.get("county_fips")].add(pk)
        office = (r.get("office") or "").upper()
        cand = (r.get("candidate") or "").strip().upper()
        try:
            v = int(float(r.get("votes") or 0))
        except ValueError:
            v = 0
        if office == "STATE SENATE":
            d = (r.get("district") or "").strip()
            sen[d][pk] += v
            if not M.is_meta(cand):
                sen_c[d][cand] += v
            if "MOUNT HOLLY" in (r.get("precinct") or "").upper() or "MT HOLLY" in (r.get("precinct") or "").upper():
                mount_holly[d] += v
        if office in STATEWIDE_ONE_SEAT and (r.get("district") or "").strip().upper() in ("STATEWIDE", "", "000"):
            sw[office][pk][1] += v
            if not M.is_meta(cand):
                sw[office][pk][0] += v
    rut = {pk for pk, v in sen["RUT"].items() if v > 0}
    rut_county = county_p["50021"]
    print(f"  Senate RUT rows: {len(rut)} precincts with votes ({len(sen['RUT'])} rows' precincts); Rutland County's precincts in any contest: {len(rut_county)}; "
          f"RUT precincts outside Rutland County: {len([p for p in rut if p[0] != '50021'])}; Rutland County precincts with no RUT row: {sorted(p[2] for p in rut_county - rut)}")
    print(f"  Mount Holly's Senate rows by district: {dict(mount_holly)}")
    for label, pks in (("the district's precincts", rut), ("the county's precincts", rut_county)):
        by_c = {o: sum(sw[o][p][0] for p in pks if p in sw[o]) for o in sw}
        by_all = {o: sum(sw[o][p][1] for p in pks if p in sw[o]) for o in sw}
        print(f"    ballots read from statewide one-seat contests over {label} ({len(pks)}): candidates' votes {dict(sorted(by_c.items()))}; all lines {dict(sorted(by_all.items()))}; "
              f"max candidates {max(by_c.values())}, max all lines {max(by_all.values())}")
    rec_a = record_of("2018-VT-upper-rutland---")
    rec_b = record_of("2018-VT-upper-rutland---", BEFORE)
    kl = sum(c["votes"] for c in rec_b["result"]["candidates"])
    named = {n: v for n, v in sen_c["RUT"].items() if not C43.GENERIC.search(n)}
    six = sorted(named.items(), key=lambda nv: -nv[1])[:6]
    s6 = sum(v for _, v in six)
    s_all = sum(sen_c["RUT"].values())
    ballots_d = max(sum(sw[o][p][1] for p in rut if p in sw[o]) for o in sw)
    print(f"  Klarner's six (record at {BEFORE}): {[(c['name'], c['votes']) for c in rec_b['result']['candidates']]} = {kl:,}; per ballot {kl / ballots_d:.2f}, x seats {kl / (3 * ballots_d):.3f}")
    print(f"  MEDSL's six leading named: {six} = {s6:,} ({s6 / ballots_d:.2f} a ballot, x seats {s6 / (3 * ballots_d):.3f}); every line {s_all:,}; named lines {len(named)}")
    print(f"  the record at {AFTER}: {[(c['name'], c['votes']) for c in rec_a['result']['candidates']]} total {rec_a['result'].get('total_votes')}; p before {C40.pval(rec_b)} after {C40.pval(rec_a)} "
          f"x{C40.pval(rec_a) / C40.pval(rec_b):.4f}; n before {rec_b['p'].get('n')} after {rec_a['p'].get('n')}; votes_source {rec_a['result'].get('votes_source')}; note: {json.dumps(rec_a.get('notes'))[:300]}")
    # pair one to one
    pairs = []
    for c in rec_b["result"]["candidates"]:
        hit = [(n, v) for n, v in named.items() if any(t in C43.mtokens(n) or any(len(x) >= 5 and t.endswith(x) for x in C43.mtokens(n)) for t in C43.ktokens(c["name"]))]
        pairs.append((c["name"], c["votes"], hit))
    print(f"  pairs: {pairs}")
    fr_a, fr_b = record_of("2018-VT-upper-franklin---"), record_of("2018-VT-upper-franklin---", BEFORE)
    print(f"  Franklin: p before {C40.pval(fr_b)} after {C40.pval(fr_a)}; reason: {json.dumps(fr_a['p'])[:300]}")
    fra = {n: v for n, v in sen_c["FRA"].items() if not C43.GENERIC.search(n)}
    print(f"    MEDSL's FRA named lines: {sorted(fra.items(), key=lambda nv: -nv[1])[:6]}; Klarner's {[(c['name'], c['votes']) for c in fr_b['result']['candidates']]}")
    chk = L.load_json(at(AFTER, "data/local/check-districts.json"))
    held = [f for v in chk["years"].values() for f in v["flags"] if f["outcome"].startswith("held") or f["outcome"] == "MEDSL taken"]
    over = [(f["id"], f["outcome"], f["over_seats"]) for f in held if isinstance(f.get("over_seats"), dict) and f["over_seats"].get("read")]
    print(f"  held flags: {len(held)}; with over_seats read: {len(over)}; of them 'over' (Klarner above seats x ballots): "
          f"{[(i, o, x['klarner_x'], x['medsl_x'], x['seats'], x['precincts']) for i, o, x in over if x.get('over')]}")
    print(f"  over_seats not read (why): {dict(collections.Counter(f['over_seats']['why'] for f in held if isinstance(f.get('over_seats'), dict) and not f['over_seats'].get('read')))}; "
          f"held with no over_seats field: {len([f for f in held if not isinstance(f.get('over_seats'), dict)])}")
    print(f"  the build's OVER_SEATS_RULED (read, not imported): {subprocess.run(['grep', '-n', '^OVER_SEATS_RULED', os.path.join(L.ROOT, 'pipeline', 'local_districts.py')], capture_output=True, text=True).stdout.strip()}")
    rul = chk["rules"]
    print(f"  the check's rules: {json.dumps(rul)}")


# ------------------------------------------------------------------------------------------ 46.7 Michigan 2022

def resolve(modes):
    """A line's votes from its modes, D3's rule copied: its TOTAL mode's or its other modes' sum, whichever is more."""
    tot = modes.get("TOTAL", 0)
    other = sum(v for m, v in modes.items() if m != "TOTAL")
    return max(tot, other)


def section_7():
    h1("46.7 Michigan 2022: Wayne's nameless Senate lines, House 10, House 27, House 99 and Arenac's file, the Attorney General")
    path, it = mi_2022_rows()
    raw = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(int))))
    # (office, district, county) -> (cand, party) -> precinct -> mode -> votes
    gov_raw = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(int)))   # county -> precinct -> mode -> governor candidates' votes
    hd99_raw = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(int)))
    ag_p, sos_p = collections.defaultdict(set), collections.defaultdict(set)
    for r in it:
        if (r.get("stage") or "GEN").upper() != "GEN":
            continue
        office = (r.get("office") or "").upper()
        d = (r.get("district") or "").strip()
        county = M.fips5(r.get("county_fips") or "")
        cand = (r.get("candidate") or "").strip().upper()
        party = (r.get("party_simplified") or r.get("party_detailed") or "").strip().upper()
        try:
            v = int(float(r.get("votes") or 0))
        except ValueError:
            v = 0
        mode = (r.get("mode") or "TOTAL").upper()
        pk = (r.get("jurisdiction_fips") or "", pnorm(r.get("precinct") or ""))
        if office == "STATE SENATE" and d.lstrip("0") in ("3", "10", "34", "35", "12", "36") or office == "STATE HOUSE" and d.lstrip("0") in ("10", "27", "99"):
            if not (M.is_meta(cand) and not (cand == "" and party)):
                raw[(office, d.lstrip("0"), county)][(cand, party)][pk][mode] += v
        if office == "STATE HOUSE" and d.lstrip("0") == "99" and not M.is_meta(cand):
            hd99_raw[county][pk][mode] += v
        if office == "GOVERNOR" and not M.is_meta(cand):
            gov_raw[county][pk][mode] += v
        if office == "ATTORNEY GENERAL" and v > 0:
            ag_p[county].add(pk)
        if office == "SECRETARY OF STATE" and v > 0:
            sos_p[county].add(pk)
    lines = collections.defaultdict(lambda: collections.defaultdict(int))   # (office, district, county) -> (cand, party) -> votes, modes resolved a precinct at a time
    for key, cs in raw.items():
        for cp, pks in cs.items():
            lines[key][cp] = sum(resolve(m) for m in pks.values())
    gov = {c: {pk: resolve(m) for pk, m in pks.items()} for c, pks in gov_raw.items()}
    hd99 = {c: {pk: resolve(m) for pk, m in pks.items()} for c, pks in hd99_raw.items()}
    print(f"  modes in the file's Wayne rows: {sorted({m for key, cs in raw.items() if key[2] == '26163' for pks in cs.values() for ms in pks.values() for m in ms})} (each line's votes: its TOTAL mode's or its other modes' sum, whichever is more; D3's rule, copied)")
    for office, d, kl in (("STATE SENATE", "3", "2022-MI-upper--3--"), ("STATE SENATE", "10", "2022-MI-upper--10--"), ("STATE SENATE", "34", None), ("STATE SENATE", "35", "2022-MI-upper--35--")):
        rec = record_of(kl) if kl else None
        allc = collections.defaultdict(int)
        nameless = []
        for (o, dd, county), cs in lines.items():
            if o == office and dd == d:
                for (c, p), v in cs.items():
                    allc[(c, p)] += v
                    if c == "":
                        nameless.append((county, p, v))
        named_sum = sum(v for (c, p), v in allc.items() if c and not C43.GENERIC.search(c))
        nl = sum(v for (c, p), v in allc.items() if c == "")
        wi = sum(v for (c, p), v in allc.items() if C43.GENERIC.search(c))
        print(f"  Senate {d}: lines {sorted(allc.items(), key=lambda kv: -kv[1])[:6]}; nameless lines by county {nameless}; named {named_sum:,} + nameless {nl:,} = {named_sum + nl:,}; write-in/other lines {wi}; "
              f"Klarner {sum(c['votes'] for c in rec['result']['candidates']) if rec else None} {[(c['name'], c.get('party'), c['votes']) for c in rec['result']['candidates']] if rec else ''}; "
              f"p before {C40.pval(record_of(kl, BEFORE)) if kl else ''} after {C40.pval(rec) if rec else ''}")
        if rec:
            # the nameless line's party against the record's one candidate of that party
            for county, p, v in nameless:
                of_party = [c for c in rec["result"]["candidates"] if (c.get("party") or "").upper() in (p, p[:1], {"DEMOCRAT": "D", "REPUBLICAN": "R"}.get(p, p)) and (c.get("party") or "").lower() != "write-in"]
                print(f"      nameless {p} {v:,} in {county}: the record's candidates of that party: {[(c['name'], c['votes']) for c in of_party]}")
    for d, kl in (("10", "2022-MI-lower--10--"), ("27", "2022-MI-lower--27--"), ("99", "2022-MI-lower--99--")):
        rec = record_of(kl)
        allc = collections.defaultdict(int)
        byc = collections.defaultdict(lambda: collections.defaultdict(int))
        for (o, dd, county), cs in lines.items():
            if o == "STATE HOUSE" and dd == d:
                for (c, p), v in cs.items():
                    allc[(c, p)] += v
                    byc[county][(c, p)] += v
        print(f"  House {d}: lines {sorted(allc.items(), key=lambda kv: -kv[1])[:6]}; all lines {sum(allc.values()):,}; Klarner {[(c['name'], c['votes']) for c in rec['result']['candidates']]} = {sum(c['votes'] for c in rec['result']['candidates']):,}; "
              f"counties {sorted(byc)}; p before {C40.pval(record_of(kl, BEFORE))} after {C40.pval(rec)}; reason/notes: {json.dumps(rec['p'].get('not_computed') or rec.get('notes'))[:260]}")
        if d == "99":
            for county in sorted(byc):
                g = sum(gov[county].get(p, 0) for p in hd99[county])
                h = sum(hd99[county].values())
                print(f"      {county}: HD99 lines {dict(byc[county])} = {h:,}; governor's votes in the same precincts {g:,}; ratio {h / g if g else None:.3f}")
            # Arenac's file
            txt = subprocess.run(["pdftotext", "-layout", os.path.join(SRC, "arenac", "Official_Nov_8_2022_ElectionSummaryReportRPT.pdf"), "-"], capture_output=True, text=True).stdout.split("\n")
            head = " | ".join(ln.strip() for ln in txt[:10] if ln.strip())
            i = [k for k, ln in enumerate(txt) if "99th District" in ln][0]
            block = [ln.strip() for ln in txt[i:i + 14] if ln.strip()]
            print(f"      Arenac's file, head: {head}")
            print(f"      Arenac's 99th block: {block}")
            kish = int(re.search(r"Kish\s+DEM\s+([\d,]+)", "\n".join(block)).group(1).replace(",", ""))
            hoad = int(re.search(r"Hoadley\s+REP\s+([\d,]+)", "\n".join(block)).group(1).replace(",", ""))
            wi = re.search(r"Unresolved Write-In\s+(\d+)", "\n".join(block))
            medsl_arenac = dict(byc["26011"])
            others = {c: sum(v for cc, v in allc.items() if cc == c) - medsl_arenac.get(c, 0) for c in allc}
            print(f"      Arenac official: Kish {kish:,}, Hoadley {hoad:,}, unresolved write-ins {wi.group(1) if wi else None}; MEDSL's Arenac lines {medsl_arenac}; "
                  f"the other counties' lines {dict(others)}; with Arenac's official in place: Kish {others.get(('KENNETH A KISH', 'DEMOCRAT'), sum(v for (c, p), v in others.items() if 'KISH' in c)) + kish:,}, "
                  f"Hoadley {sum(v for (c, p), v in others.items() if 'HOADLEY' in c) + hoad:,}")
    # the Attorney General and Secretary of State in Wayne
    w_sos, w_ag = sos_p["26163"], ag_p["26163"]
    print(f"  Wayne: Secretary of State precincts {len(w_sos)}, Attorney General precincts {len(w_ag)}; SoS precincts with no AG row {len(w_sos - w_ag)} ({len(w_sos - w_ag) / len(w_sos):.1%})")
    rec = [r for r in records_at(AFTER, "data/local/2022/MI.json").values() if r["id"] == "2022-local-MI-ATTORNEY_GENERAL"][0]
    rec_b = [r for r in records_at(BEFORE, "data/local/2022/MI.json").values() if r["id"] == "2022-local-MI-ATTORNEY_GENERAL"][0]
    print(f"  the Attorney General record: reason before ({len(rec_b['p']['not_computed'])} chars) / after ({len(rec['p']['not_computed'])} chars); after adds: {rec['p']['not_computed'][len(rec_b['p']['not_computed']):][:500]}")


# ------------------------------------------------------------------------------------------ 46.8 DC 2018

def section_8():
    h1("46.8 DC 2018's at-large Council: the Board's certified results PDF, the record's seats and reason, the over-ballot entry")
    txt = subprocess.run(["pdftotext", "-layout", os.path.join(SRC, "dc_boe", "November_6_2018_General_Election_Certified_Results.pdf"), "-"], capture_output=True, text=True).stdout.split("\n")
    print(f"  the heading: {' / '.join(ln.strip() for ln in txt[:3] if ln.strip())}")

    def block(title):
        i = [k for k, ln in enumerate(txt) if ln.strip() == title][0]
        out = {}
        for ln in txt[i + 1:i + 16]:
            if not ln.strip():
                continue
            m = re.match(r"^\s*(.+?)\s{2,}((?:[\d,]+\s+){8})([\d,]+)\s*$", ln)
            if m:
                out[m.group(1).strip()] = int(m.group(3).replace(",", ""))
            elif ln.strip().isupper() and not re.search(r"\d", ln):
                break
        return out
    ballots = [ln for ln in txt if ln.strip().startswith("CityWide")]
    bc = int(re.findall(r"[\d,]+", ballots[1])[-1].replace(",", "")) if len(ballots) > 1 else None
    al = block("AT-LARGE MEMBER OF THE COUNCIL")
    my = block("MAYOR OF THE DISTRICT OF COLUMBIA")
    cands = {k: v for k, v in al.items() if k not in ("OVER VOTES", "UNDER VOTES")}
    print(f"  Ballots Cast (CityWide): {bc:,}")
    print(f"  at-large: candidates and write-in {sum(cands.values()):,} ({cands}); over {al.get('OVER VOTES')}, under {al.get('UNDER VOTES'):,}; all {sum(al.values()):,} = {sum(al.values()) / bc:.3f} x ballots cast")
    print(f"  Mayor: marks and blanks {sum(my.values()):,} ({my}); the at-large's all / the Mayor's {sum(al.values()) / sum(my.values()):.4f}")
    rec_a = [r for r in records_at(AFTER, "data/local/2018/DC.json").values() if r["id"] == "2018-local-DC-DC_COUNCILMEMBER-AT_LARGE"][0]
    rec_b = [r for r in records_at(BEFORE, "data/local/2018/DC.json").values() if r["id"] == "2018-local-DC-DC_COUNCILMEMBER-AT_LARGE"][0]
    print(f"  the record: seats {rec_b.get('seats')} -> {rec_a.get('seats')}; won before {[c['name'] for c in rec_b['result']['candidates'] if c.get('won')]} after {[c['name'] for c in rec_a['result']['candidates'] if c.get('won')]}; "
          f"total_votes {rec_a['result'].get('total_votes'):,} (the PDF's candidates and write-in {sum(cands.values()):,}); p: {json.dumps(rec_a['p'])}")
    print(f"  seats_note: {rec_a.get('seats_note', '')[:400]}")
    print(f"  notes: {json.dumps(rec_a.get('notes'))[:400]}")
    ob = L.load_json(at(AFTER, "data/local/check-over-ballot.json"))
    hits = [e for e in ob.get("2018", []) if isinstance(e, dict) and e.get("state") == "DC" and "AT" in str(e.get("district", "")).upper()]
    print(f"  check-over-ballot.json 2018 DC at-large: {json.dumps(hits)[:600]}")
    vol = L.load_json(at(AFTER, "data/local/check-volume.json"))
    s = json.dumps(vol)
    i = s.find("462964")
    print(f"  check-volume.json mentions 462,964 (the at-large's two votes a ballot as DC's ballots): {s.count('462964')} time(s); context: {s[max(0, i - 300):i + 100] if i >= 0 else ''}")
    # the partisan back-test (REPORT: 51.8 -> 51.7 within 100, deviance 16.86 -> 16.85)
    for commit in (BEFORE, AFTER):
        rep = at(commit, "data/local/REPORT.md")
        txt2 = open(rep).read()
        m = re.findall(r"within 100 votes[^\n]{0,160}", txt2)
        print(f"    {commit} REPORT lines on 'within 100 votes': {len(m)}; last: {m[-1][:160] if m else ''}")


# ------------------------------------------------------------------------------------------ 46.9 Virginia's notes

def section_9():
    h1("46.9 Virginia 2023's local records: the 65 name-keyed write-in notes and the three unconfirmed")
    a = records_at(AFTER, "data/local/2023/VA.json")
    b = records_at(BEFORE, "data/local/2023/VA.json")
    noted = {i: r for i, r in a.items() if any("write-in" in n and ("keyed" in n or "name-keyed" in n or "by name" in n) for n in (r.get("notes") or []))}
    unconf = {i: r for i, r in a.items() if any("not confirmed" in n or "does not show" in n for n in (r.get("notes") or []))}
    changed = [i for i in a if (a[i].get("notes") or []) != (b.get(i, {}).get("notes") or [])]
    print(f"  records whose notes changed: {len(changed)}; with a write-in-by-name note: {len(noted)}; saying the page does not confirm it: {len(unconf)} {sorted(unconf)}")
    for i in sorted(unconf):
        print(f"    {i}: {[n for n in a[i]['notes'] if 'not confirmed' in n or 'does not show' in n][0][:400]}; p {json.dumps(a[i].get('p'))[:120]}")
    ex = next(iter(noted.values()))
    print(f"  a note, e.g. {ex['id']}: {[n for n in ex['notes'] if 'write-in' in n][0][:500]}")
    # beside c45's reading of the export: the contests with a name-keyed option
    try:
        import c45_va_gate as C45
        cs = C45.local_contests()
        named = [c for c in cs if any(kind == "write-in by name" for _, _, _, kind in c["options"])]
        print(f"  c45's reading of the export: contests with a name-keyed option {len(named)} (options {sum(1 for c in named for _, _, _, kind in c['options'] if kind == 'write-in by name')})")
        idx = C45.file_index(cs)
        hit = 0
        for r in noted.values():
            c = C45.contest_of(r, idx)
            if c is not None and c in named:
                hit += 1
        print(f"  of the {len(noted)} noted records, matched to a contest with a name-keyed option: {hit}")
    except Exception as e:   # noqa: BLE001
        print(f"  c45's export reading not run here: {e!r}")
    p_changed = [i for i in a if C40.pval(a[i]) != C40.pval(b.get(i, {}))]
    print(f"  Virginia records whose p changed: {len(p_changed)}")


# ------------------------------------------------------------------------------------------ 46.10 D2's totals; Indiana 2018

def section_10():
    h1("46.10 D2's governor totals and Maine's 2nd district (no p moved); the second counts beside MEDSL's from my summaries; Indiana 2018's class B")
    ct = L.load_json(at(AFTER, "data/congress/check-totals.json"))
    print(f"  check-totals.json: {json.dumps({k: (v if not isinstance(v, (list, dict)) else f'{type(v).__name__}[{len(v)}]') for k, v in ct.items()})[:500]}")
    rows = ct.get("governors") or ct.get("records") or ct.get("rows") or [v for v in ct.values() if isinstance(v, list)][0]
    ex = rows[0] if rows else None
    print(f"  a row: {json.dumps(ex)[:500]}")
    # MEDSL's governor sums from my volume summaries, beside the record's total_votes and the file's second count
    for yr in (2018, 2020, 2022, 2024):
        recs = records_at(AFTER, f"data/governor/{yr}.json")
        recs_b = records_at(BEFORE, f"data/governor/{yr}.json")
        gov = {}
        for y, path in M.all_raw_files():
            if y != yr:
                continue
            p = os.path.join(C43.DERIVED, os.path.basename(path) + ".volume.json")
            if not os.path.exists(p):
                continue
            d = L.load_json(p)
            for key, c in d["contests"].items():
                parts = key.split("|")
                if parts[2] == "GOVERNOR" and parts[3] in ("", "STATEWIDE"):
                    gov[parts[0]] = sum(v for n, v in (c["no_total"] or c["cands"]).items() if not C43.GENERIC.search(n))
        flagged = [r for r in recs.values() if r["result"].get("total_votes_of")]
        for r in flagged:
            st = r["place"]["state"]
            tv = r["result"]["total_votes"]
            m = gov.get(st)
            print(f"    {r['id']}: total_votes {tv:,} ({r['result']['total_votes_of']}); MEDSL's named lines in my summary {m:,} ({m / tv - 1:+.2%})" if m else
                  f"    {r['id']}: total_votes {tv:,} ({r['result']['total_votes_of']}); no MEDSL governor contest in my summaries for {st} {yr}; "
                  f"note: {[n for n in r.get('notes', []) if 'total' in n.lower()][:1]}"[:400])
            print(f"      p {C40.pval(recs_b[r['id']])} -> {C40.pval(r)}; two_party before {recs_b[r['id']].get('two_party')} after {r.get('two_party')}" if recs_b[r["id"]].get("two_party") != r.get("two_party") or C40.pval(recs_b[r["id"]]) != C40.pval(r) else f"      p and two_party unchanged")
    me = [r for r in records_at(AFTER, "data/house/2024.json").values() if r["id"] == "2024-house-ME-02"][0]
    me_b = [r for r in records_at(BEFORE, "data/house/2024.json").values() if r["id"] == "2024-house-ME-02"][0]
    print(f"  ME-02 2024: candidates before {[(c['name'], c['votes']) for c in me_b['result']['candidates']]} after {[(c['name'], c['votes']) for c in me['result']['candidates']]}; "
          f"total {me_b['result']['total_votes']} -> {me['result']['total_votes']}; rcv_lines {me['result'].get('rcv_lines')}; two_party {me_b.get('two_party')} -> {me.get('two_party')}; ballot.others {me_b.get('ballot', {}).get('others')} -> {me.get('ballot', {}).get('others')}; p {json.dumps(me['p'])[:200]}")
    # Indiana 2018's House, class B
    a = records_at(AFTER, "data/state-lower/2018/IN.json")
    b = records_at(BEFORE, "data/state-lower/2018/IN.json")
    cls = collections.Counter()
    leans = collections.Counter()
    moved = []
    for i, r in a.items():
        rb = b.get(i)
        if not rb:
            continue
        c = (r.get("forecast_inputs") or {}).get("class")
        pa, pb = C40.pval(r), C40.pval(rb)
        if pa and pb:
            cls[(c, "moved >10%" if abs(pa / pb - 1) > 0.10 else "moved 1-10%" if abs(pa / pb - 1) > 0.01 else "within 1%")] += 1
            if abs(pa / pb - 1) > 0.10:
                moved.append((i, round(pa / pb, 4), c))
        lb, la = (rb.get("forecast_inputs") or {}).get("lean"), (r.get("forecast_inputs") or {}).get("lean")
        if c == "B":
            leans[(lb, la)] += 1
    print(f"  Indiana 2018 House by class and move: {dict(sorted(cls.items(), key=lambda kv: str(kv)))}; class B leans (before, after): {dict(leans)}")
    print(f"  moved more than 10%: {moved}")
    # the chamber's 2016 lean: from the 2016 records' two-party shares (what class B takes)
    for commit in (BEFORE, AFTER):
        r16 = records_at(commit, "data/state-lower/2016/IN.json")
        shares = [r["two_party"]["share_first"] for r in r16.values() if r.get("two_party") and C40.pval(r) is not None and r["two_party"].get("votes") and len(r["two_party"]["votes"]) == 2]
        print(f"    {commit}: Indiana 2016 House records with p and a two-party share: {len(shares)}; mean share_first {sum(shares) / len(shares):.4f}")


def main():
    want = sys.argv[1:] or ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    for s in want:
        globals()[f"section_{s}"]()


if __name__ == "__main__":
    main()
