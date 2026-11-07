"""C21. #65 and #66, New Jersey's 2024 local contests gated by county (the orchestrator's rulings of 10:45 and 11:16;
the third pass's item 5): checked from the sources themselves, fetched by curl into m2lib.CACHE/nj (the Division of
Elections' three Official Lists, MEDSL's 2024-nj-precinct-general.csv, the five county clerks' files D3 read).
  21.1 the state's lists (my own reading of the PDFs' text) against D1's president and D2's Senate and twelve House
       districts: every candidate's county lines add up to its total; the Democrat's and Republican's totals equal;
  21.2 MEDSL by county against the lists: each county's Democratic and Republican count in each federal office (the
       House by its district's part of the county), the counties that add up at the 0.5% line (16 in every office,
       Gloucester in two, four in none) and each county's worst miss, against data/local/check-nj.json;
  21.3 the row checks on the file's local rows: repeated rows; a total line among a contest's precincts; and the
       bound of 11:16 (a precinct's votes in a contest against its ballots cast times the contest's vote-for-N);
  21.4 the file's 1,301 local contests and 49 questions rebuilt from MEDSL's rows: candidates and votes, the gate
       (released only where the county adds up in all three offices), the held reasons and the counts;
  21.5 the five county clerks' official counts against the file (Camden, Hunterdon, Ocean, Sussex read by me; Morris
       refused me with HTTP 403, so D3's reading of it stands unverified here);
  21.6 the 52 p New Jersey's released contests got: 43 by the like-race route against my own pool, 9 by the partisan
       route from their recorded inputs, and p = 0 for the 246 unopposed; and which p files #65, #66 and #68 changed.
Votes of a precinct and candidate are MEDSL's TOTAL row where it has one, else the sum of its modes (pipeline/intake/
medsl_precinct.py resolve; MEDSL's README). [measured] throughout; the record's figures [stated].
"""
import collections
import csv
import glob
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402
import m2d3 as D  # noqa: E402
import c15_d3_refit as C15  # noqa: E402

NJ = os.path.join(L.CACHE, "nj")
COUNTIES = ["ATLANTIC", "BERGEN", "BURLINGTON", "CAMDEN", "CAPE MAY", "CUMBERLAND", "ESSEX", "GLOUCESTER", "HUDSON",
            "HUNTERDON", "MERCER", "MIDDLESEX", "MONMOUTH", "MORRIS", "OCEAN", "PASSAIC", "SALEM", "SOMERSET", "SUSSEX",
            "UNION", "WARREN"]
FIPS = {c: f"34{2 * i + 1:03d}" for i, c in enumerate(COUNTIES)}   # the Census numbers them alphabetically, odd
ORD = {w: i + 1 for i, w in enumerate("First Second Third Fourth Fifth Sixth Seventh Eighth Ninth Tenth Eleventh Twelfth".split())}
TALLY = re.compile(r"^\s{40,}(" + "|".join(COUNTIES) + r")\s+(.*?)\s+([\d,]+)\s*$")   # a county line sits 40+ spaces in
ADDRESS = re.compile(r", NJ \d{5}\s*$")   # an address line ("UNION CITY, NJ 07087") is not a county line
TOTAL = re.compile(r"^\s+Total\s+([\d,]+)\s*$")
CAND = re.compile(r"^(\S.*?)\s{2,}(?:.*?\s{2,})?([A-Z][A-Za-z .'/&-]*)\s*$")
DIST = re.compile(r"^(\w+) Congressional District:")
LINE = 0.005
NOT_CANDS = ("WRITE-IN", "OVERVOTES", "UNDERVOTES", "UNDERVOTE", "CONTEST TOTAL", "TOTAL VOTES CAST", "NO PETITION FILED")
FEDERAL = ("US PRESIDENT", "US SENATE", "US HOUSE")


def num(s):
    return int(s.replace(",", ""))


# ---------------------------------------------------------------- 21.1 the state's lists
def read_list(office):
    """pdftotext -layout of the Official List: [{office, district, name, party, counties {county: votes}, total}].
    A candidate's county lines can run over a page break, where the list repeats the candidate's name line."""
    txt = os.path.join(NJ, f"{office}.txt")
    if not os.path.exists(txt):
        subprocess.run(["pdftotext", "-layout", os.path.join(NJ, f"{office}.pdf"), txt], check=True)
    out, cur, district = [], None, None
    for line in open(txt, encoding="utf-8", errors="replace"):
        line = line.rstrip("\n")
        m = DIST.match(line)
        if m:
            district = ORD[m.group(1)]
            continue
        m = TALLY.match(line)
        if m and cur is not None and not ADDRESS.search(line):
            cur["counties"][m.group(1)] = cur["counties"].get(m.group(1), 0) + num(m.group(3))
            continue
        m = TOTAL.match(line)
        if m and cur is not None:
            cur["total"] = num(m.group(1))
            if cur["counties"]:
                out.append(cur)
            cur = None   # a name repeated with the contest's total (NJ-12) has no county lines and is dropped
            continue
        if line and not line[0].isspace() and not line.startswith(("(", "Name", "Candidate", "Total", "12/")) \
                and "Official List" not in line and re.search(r"\s{2,}", line):
            name = re.split(r"\s+(?=P\.?O\.? BOX|\d)", re.split(r"\s{2,}", line)[0].strip())[0].strip()   # a long name runs into its address
            tail = line.rstrip()
            party = "Democratic" if tail.endswith("Democratic") else "Republican" if tail.endswith("Republican") else "other"
            if cur is not None and cur["name"] == name:
                continue   # the same candidate, continued on the next page
            cur = {"office": office, "district": district, "name": name, "party": party, "counties": {}, "total": None}
    return out


def section_1():
    print("21.1 The state's three Official Lists against D1 and D2")
    lists = {o: read_list(o) for o in ("president", "us-senate", "us-house")}
    for o, cs in lists.items():
        bad = [c for c in cs if sum(c["counties"].values()) != c["total"]]
        print(f"  {o}: {len(cs)} candidates read; county lines add up to the candidate's total in {len(cs) - len(bad)}" + (f"; NOT in {[(c['name'], sum(c['counties'].values()), c['total']) for c in bad]}" if bad else ""))
    def dr(cs):
        return {p: sum(c["total"] for c in cs if c["party"] == w) for p, w in (("D", "Democratic"), ("R", "Republican"))}
    pres = [c for c in L.load_json(os.path.join(L.DATA, "president", "2024.json"))["contests"] if c["place"]["state"] == "NJ"][0]
    d1 = {p: sum(x["votes"] for x in pres["result"]["candidates"] if x["party"] == w) for p, w in (("D", "Democratic"), ("R", "Republican"))}
    s = dr(lists["president"])
    print(f"  president: the state D {s['D']:,} R {s['R']:,}; D1 D {d1['D']:,} R {d1['R']:,}: {'equal' if s == d1 else 'DIFFER'}")
    sen = [c for c in L.load_json(os.path.join(L.DATA, "senate", "2024.json"))["contests"] if c["id"] == "2024-senate-NJ"][0]
    d2 = {p: sum(x["votes"] for x in sen["result"]["candidates"] if x["party"] == w) for p, w in (("D", "Democrat"), ("R", "Republican"))}
    s = dr(lists["us-senate"])
    print(f"  Senate: the state D {s['D']:,} R {s['R']:,}; D2 D {d2['D']:,} R {d2['R']:,}: {'equal' if s == d2 else 'DIFFER'}")
    house = {c["id"]: c for c in L.load_json(os.path.join(L.DATA, "house", "2024.json"))["contests"] if c["id"].startswith("2024-house-NJ-")}
    eq, diff = 0, []
    for k in range(1, 13):
        cs = [c for c in lists["us-house"] if c["district"] == k]
        s = dr(cs)
        h = house[f"2024-house-NJ-{k:02d}"]
        d2 = {p: sum(x["votes"] for x in h["result"]["candidates"] if x["party"] == w) for p, w in (("D", "Democrat"), ("R", "Republican"))}
        mine = sorted(c["total"] for c in cs)
        theirs = sorted(x["votes"] for x in h["result"]["candidates"])
        if s == d2 and mine == theirs:
            eq += 1
        else:
            diff.append((k, s, d2, mine, theirs))
    print(f"  House: the twelve districts' D and R totals and every candidate's votes equal D2's in {eq} of 12" + (f"; differ {diff}" if diff else ""))
    worst = 0.0
    for o, cs in lists.items():
        pass
    return lists


# ---------------------------------------------------------------- MEDSL
def load_medsl():
    """MEDSL's rows: {(county, office, district): {precinct: {candidate: {mode: votes}}}} with party and magnitude."""
    path = os.path.join(NJ, "medsl", "2024-nj-precinct-general.csv")
    csv.field_size_limit(10 ** 9)
    by = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(dict)))
    party, mag, rows_seen = {}, {}, collections.Counter()
    with open(path, newline="", encoding="utf-8", errors="replace") as f:
        for r in csv.DictReader(f):
            key = (r["county_name"], r["office"], r["district"])
            mode = (r["mode"] or "TOTAL").upper()
            cell = by[key][r["precinct"]][r["candidate"]]
            cell[mode] = cell.get(mode, 0) + int(r["votes"] or 0)
            party[(key, r["candidate"])] = r["party_simplified"]
            if r["magnitude"]:
                mag[key] = int(float(r["magnitude"]))
            rows_seen[(r["county_name"], r["precinct"], r["office"], r["district"], r["candidate"], mode)] += 1
    return by, party, mag, rows_seen


def resolve(modes):
    return modes["TOTAL"] if "TOTAL" in modes else sum(modes.values())


def contest_votes(prec):
    """{candidate: votes} over a contest's precincts, by resolve."""
    out = collections.Counter()
    for cands in prec.values():
        for a, m in cands.items():
            out[a] += resolve(m)
    return out


def surname(name):
    """The last name, without '(w)', '*' and the suffixes Jr., Sr., II, III."""
    toks = [t for t in re.sub(r"\(.*?\)|\*", " ", name).upper().split() if re.sub(r"[^A-Z]", "", t) not in ("JR", "SR", "II", "III", "IV", "")]
    return re.sub(r"[^A-Z]", "", toks[-1]) if toks else ""


def same_surname(medsl_name, sn):
    """MEDSL's surname against the state's: equal, or one ends with the other (WATSON-COLEMAN against COLEMAN)."""
    a = surname(medsl_name)
    return bool(a and sn) and (a == sn or a.endswith(sn) or sn.endswith(a))


def section_2(lists, by, party):
    print("21.2 MEDSL's counts by county against the state's lists (0.5% line)")
    rec = L.load_json(os.path.join(L.DATA, "local", "check-nj.json"))["medsl_by_county"]
    # the state's lines: {county: {(office, district, party): votes}}
    state = collections.defaultdict(dict)
    for o, cs in lists.items():
        for c in cs:
            if c["party"] not in ("Democratic", "Republican"):
                continue
            for county, v in c["counties"].items():
                state[county][(o, c["district"], c["party"][0], surname(c["name"]))] = v
    off = collections.defaultdict(dict)
    plain_eq_resolve = True
    for county in COUNTIES:
        for (o, dist, p, sn), v in state[county].items():
            key = (county, {"president": "US PRESIDENT", "us-senate": "US SENATE", "us-house": "US HOUSE"}[o], "STATEWIDE" if dist is None else str(dist).zfill(3) if False else None)
            # MEDSL's district strings: find the key for this office in this county
            cands = None
            for k in by:
                if k[0] == county and k[1] == key[1] and (dist is None or re.sub(r"\D", "", k[2]).lstrip("0") == str(dist)):
                    cands = by[k]
                    break
            if cands is None:
                off[county][(o, dist, p)] = None
                continue
            votes = contest_votes(cands)
            plain = collections.Counter()
            for cc in cands.values():
                for a, m in cc.items():
                    plain[a] += sum(m.values())
            mine = sum(n for a, n in votes.items() if same_surname(a, sn))
            pl = sum(n for a, n in plain.items() if same_surname(a, sn))
            if mine != pl:
                plain_eq_resolve = False
            off[county][(o, dist, p)] = (mine, v, mine / v - 1 if v else None, pl)
    adds_all, some, none_ = [], [], []
    worst_cmp = []
    for county in COUNTIES:
        byo = collections.defaultdict(list)
        for (o, dist, p), x in off[county].items():
            byo[o].append(x)
        ok = {o: all(x is not None and abs(x[2]) <= LINE for x in xs) for o, xs in byo.items()}
        worst = {o: max(abs(x[2]) for x in xs if x is not None) for o, xs in byo.items()}
        (adds_all if all(ok.values()) else some if any(ok.values()) else none_).append(county)
        r = rec["counties"].get(county, {})
        rw = r.get("worst_off", {})
        mine_w = {"president": worst.get("president"), "senate": worst.get("us-senate"), "house": worst.get("us-house")}
        same = all(abs(mine_w[k] - rw.get(k, -9)) < 2e-4 or (rw.get(k, 0) > 1 and mine_w[k] > 0.9) for k in mine_w)
        worst_cmp.append((county, same, mine_w, rw))
    print(f"  counties adding up in all three offices: {len(adds_all)} ({adds_all}); in some only: {some}; in none: {none_}")
    print(f"  the record: all three {len(rec['counties_adding_up_in_every_federal_office'])} ({rec['counties_adding_up_in_every_federal_office'] == adds_all}); some only {rec['counties_adding_up_in_some_federal_offices_only']} ({rec['counties_adding_up_in_some_federal_offices_only'] == some})")
    ns = [w for w in worst_cmp if not w[1]]
    print(f"  each county's worst miss per office as the record's (within 2e-4, or both over the line by a multiple): {len(worst_cmp) - len(ns)} of 21" + (f"; differ: {ns[:4]}" if ns else ""))
    for county in none_ + some:
        xs = off[county]
        print(f"    {county:11s} " + "; ".join(f"{o}{'' if dist is None else ' ' + str(dist)} {p} {x[0]:,}/{x[1]:,} ({x[2]:+.4f})" for (o, dist, p), x in sorted(xs.items(), key=lambda kv: (kv[0][0], kv[0][1] or 0, kv[0][2])) if x is not None and abs(x[2]) > LINE)[:6])
    print(f"  MEDSL's rows summed plainly (every mode added) give the same county counts as the TOTAL-else-modes rule: {plain_eq_resolve} "
          f"(where not, a county has both a TOTAL row and its modes, so a plain sum counts them twice)")
    # the record's own 'medsl' numbers: which rule do they follow?
    rec_rule = collections.Counter()
    odd = []
    for county in COUNTIES:
        for line, x in rec["counties"].get(county, {}).get("lines", {}).items():
            m = re.match(r"^(president|senate|house(?: \d+)?) ([DR])$", line)
            if not m:
                continue
            o = {"president": "president", "senate": "us-senate"}.get(m.group(1).split()[0], "us-house")
            dist = int(m.group(1).split()[1]) if " " in m.group(1) else None
            mine = off[county].get((o, dist, m.group(2)))
            if mine is None:
                rec_rule["no line of mine"] += 1
            elif x["medsl"] == mine[0]:
                rec_rule["as the TOTAL-else-modes rule"] += 1
            elif x["medsl"] == mine[3]:
                rec_rule["as the plain sum"] += 1
            else:
                rec_rule["neither"] += 1
            if mine is not None and x["medsl"] != mine[0]:
                odd.append(f"{county} {line}: record {x['medsl']:,}, mine {mine[0]:,} (plain sum {mine[3]:,}), the state {x['state']:,}")
    print(f"  the record's 'medsl' county counts against mine: {dict(rec_rule)}" + ("".join("\n    " + o for o in odd[:16]) if odd else ""))
    return adds_all


# ---------------------------------------------------------------- 21.3 row checks and the bound
SUMMARY = re.compile(r"^TOTAL |REGISTERED VOTERS")   # MEDSL's summary 'offices' (TOTAL BALLOTS CAST, ...), not contests


def local_keys(by):
    return [k for k in by if k[1] not in FEDERAL and not SUMMARY.match(k[1])]


def section_3(by, party, mag, rows_seen):
    print("21.3 The row checks on MEDSL's local rows, and the ballots-cast bound of 11:16")
    rec = L.load_json(os.path.join(L.DATA, "local", "check-nj.json"))["county_gate"]
    lk = local_keys(by)
    dup = sum(1 for k, v in rows_seen.items() if v > 1 and k[2] not in FEDERAL)
    print(f"  local contests (county, office, district) in MEDSL's file: {len(lk):,}; repeated rows (the same county, precinct, office, district, candidate and mode twice): {dup}")
    total_line = []
    for k in lk:
        prec = by[k]
        names = [p for p in prec if "TOTAL" in p.upper()]
        if names:
            total_line.append((k, names[:2]))
            continue
        if len(prec) >= 3 and any(a not in NOT_CANDS for cands in prec.values() for a in cands):   # a contest with a named candidate
            sums = collections.Counter()
            per = {}
            for p, cands in prec.items():
                per[p] = {a: resolve(m) for a, m in cands.items()}
                for a, v in per[p].items():
                    sums[a] += v
            for p, pv in per.items():
                if pv and all(sums[a] - pv[a] == pv[a] for a in pv) and sum(pv.values()) > 0:
                    total_line.append((k, [p]))
                    break
    byc = collections.Counter(k[0] for k, _ in total_line)
    print(f"  contests with a precinct named TOTAL or equal to all its other precincts added up: {len(total_line)}, by county {dict(byc)} (the record: none in the released counties; Bergen 160)"
          + "".join(f"\n    {k[0]} '{k[1]}' {k[2]!r}: {names} ({len(by[k])} precincts; votes {dict(contest_votes(by[k]))})" for k, names in total_line if k[0] not in ("BERGEN", "GLOUCESTER")))
    # ballots cast per precinct: over vote-for-1 contests (magnitude 1), votes + overvotes + undervotes, or CONTEST TOTAL where larger
    ballots = collections.defaultdict(int)
    for k, prec in by.items():
        if mag.get(k) != 1:
            continue
        for p, cands in prec.items():
            cast = sum(resolve(m) for a, m in cands.items() if a not in ("CONTEST TOTAL", "TOTAL VOTES CAST"))
            ct = max([resolve(m) for a, m in cands.items() if a in ("CONTEST TOTAL", "TOTAL VOTES CAST")] or [0])
            ballots[(k[0], p)] = max(ballots[(k[0], p)], cast, ct)
    held = []
    for k in lk:
        prec = by[k]
        named = {a for cands in prec.values() for a in cands if a not in NOT_CANDS}
        n_ = mag.get(k) or len(named)
        over = []
        for p, cands in prec.items():
            v = sum(resolve(m) for a, m in cands.items() if a not in ("CONTEST TOTAL", "TOTAL VOTES CAST", "OVERVOTES", "UNDERVOTES", "UNDERVOTE"))
            b = ballots.get((k[0], p), 0)
            if b and v > b * max(n_, 1):
                over.append((p, v, b))
            elif not b and v > 0 and False:
                over.append((p, v, None))
        if over:
            held.append((k, n_, len(prec), over[:3], k in mag))
    print(f"  contests with a precinct over its ballots cast times vote-for-N ({'the number of candidates named where MEDSL gives no vote-for-N'}): {len(held)} (the record holds 1: Delanco Township's board of education, 334 against 327 in 1 of 7 precincts)")
    for k, n_, np_, over, has in held[:8]:
        print(f"    {k[0]} '{k[1]}' {k[2]!r}: vote-for-{n_} ({'MEDSL' if has else 'candidates named'}), {len(over)} of {np_} precincts, e.g. {over[0][0]!r} {over[0][1]} against {over[0][2]}")
    print(f"  precincts with a ballots-cast figure: {len(ballots):,}; the record's held-by-the-row-checks: {[x['office'] for x in rec['held_by_the_row_checks']]}")
    # the old bound (the president's votes) for the two Camden contests
    for office in ("CAMDEN COUNTY CLERK", "CAMDEN SHERIFF"):
        k = ("CAMDEN", office, "")
        for kk in by:
            if kk[0] == "CAMDEN" and kk[1].startswith(office.split(" ", 1)[1] if False else office):
                k = kk
        if k in by:
            pres = {p: sum(resolve(m) for a, m in cands.items() if a not in NOT_CANDS or a == "WRITE-IN") for p, cands in by[("CAMDEN", "US PRESIDENT", "STATEWIDE")].items()}
            o = sum(1 for p, cands in by[k].items() if sum(resolve(m) for a, m in cands.items() if a not in ("CONTEST TOTAL", "TOTAL VOTES CAST", "OVERVOTES", "UNDERVOTES")) > pres.get(p, 0))
            print(f"  {k[1]}: precincts over the president's votes there (the bound of 10:45, withdrawn 11:16): {o} of {len(by[k])} (the record: clerk 6, sheriff 8); over the ballots cast: {sum(1 for p, cands in by[k].items() if sum(resolve(m) for a, m in cands.items() if a not in ('CONTEST TOTAL', 'TOTAL VOTES CAST', 'OVERVOTES', 'UNDERVOTES')) > ballots.get((k[0], p), 0))}")
    return held, total_line


# ---------------------------------------------------------------- 21.4 the file
def norm(s):
    return re.sub(r"[^A-Z0-9]", "", s.upper())


def named_votes(v):
    """MEDSL's named candidates' votes (sorted) and the write-ins' sum, as D3's intake takes them: rows with no name and
    BLANK are not candidates (medsl_precinct.NOT_CANDIDATES), and write-in lines of one name with and without a
    suffix (JR, SR, II, III) are one person (medsl_precinct.same_person)."""
    merged = collections.Counter()
    for a, n in v.items():
        if a in NOT_CANDS or not a.strip() or a in ("BLANK", "YES", "NO", "FOR", "AGAINST"):   # medsl_precinct's NOT_CANDIDATES and ANSWERS
            continue
        merged[" ".join(x for x in a.split() if x not in ("JR", "SR", "II", "III", "IV", "V"))] += n
    return sorted(merged.values()), sum(n for a, n in v.items() if a == "WRITE-IN")


def section_4(by, party, mag, adds_all, held_rows):
    print("21.4 The file's contests rebuilt from MEDSL's rows, and the gate")
    loc = L.load_json(os.path.join(L.DATA, "local", "2024", "NJ.json"))["contests"]
    meas = L.load_json(os.path.join(L.DATA, "measure", "2024", "NJ.json"))["contests"]
    fips_to = {v: k for k, v in FIPS.items()}
    idx = collections.defaultdict(list)
    for k in local_keys(by):
        idx[(k[0], norm(k[1]))].append(k)
    t = collections.Counter()
    bad = []
    gate_ok = collections.Counter()
    released_set = set(adds_all)
    held_keys = {k for k, *_ in held_rows}
    groups = collections.defaultdict(list)
    for c in loc:
        county = fips_to[c["place"]["counties"][0]]
        groups[(county, norm(c["office"]))].append(c)
    matched_ids = set()
    for (county, office), cs in groups.items():
        ks = idx.get((county, office), [])
        want = sorted(x["votes"] for c in cs for x in c["result"]["candidates"] if x["name"].upper() != "WRITE-IN")
        want_w = sum(x["votes"] for c in cs for x in c["result"]["candidates"] if x["name"].upper() == "WRITE-IN")
        hit = None
        for k in ks:
            got, got_w = named_votes(contest_votes(by[k]))
            if got == want and got_w == want_w:
                hit = k
                break
        if hit is None and len(ks) > 1:   # the file's contests of the office split MEDSL's keys (by district)
            merged = collections.Counter()
            for k in ks:
                merged.update(contest_votes(by[k]))
            got, got_w = named_votes(merged)
            if got == want and got_w == want_w:
                hit = ks[0]
        answers = [(k, a, n) for k in ks for a, n in contest_votes(by[k]).items() if a in ("YES", "NO", "FOR", "AGAINST") and n > 0.1 * max(1, sum(contest_votes(by[k]).values()))]
        if answers:
            t["MEDSL's rows hold a YES or NO choice with over a tenth of the votes (a question recorded as an office)"] += len(cs)
            bad.append(f"{cs[0]['id'][14:]}: the file's names {[(x['name'], x['votes']) for c in cs for x in c['result']['candidates']][:3]}, p {cs[0]['p']}; MEDSL's rows " + "; ".join(f"{a} {n:,}" for _, a, n in answers) + f" (medsl_precinct.ANSWERS drops NO, FOR and AGAINST as answers; 'YES/SI' is not in it)")
        if hit is None:
            t["not matched"] += len(cs)
            names_f = {x["name"].upper() for c in cs for x in c["result"]["candidates"]}
            names_m = {a for k in ks for a in contest_votes(by[k]) if a not in NOT_CANDS and a.strip()}
            bad.append(f"{cs[0]['id'][14:]}: the file {sum(want):,} votes over {len(want)} names, MEDSL " + "; ".join(f"{sum(named_votes(contest_votes(by[k]))[0]):,} over {len(named_votes(contest_votes(by[k]))[0])}" for k in ks[:2])
                       + f"; names in MEDSL's rows only {sorted(names_m - names_f)[:4]}, in the file only {sorted(names_f - names_m)[:4]}")
        else:
            t["matched (every named candidate's votes, and the write-ins' sum)" + (" as a group" if len(cs) > 1 else "")] += len(cs)
            matched_ids.update(c["id"] for c in cs)
    for c in loc:
        county = fips_to[c["place"]["counties"][0]]
        g = c.get("gate") or {}
        reason = (c["p"].get("not_computed") or "")
        rel_mine = county in released_set and "ballots cast" not in reason
        rec_rel = bool(g.get("released"))
        gate_ok[("released" if rec_rel else "held", "as mine" if rec_rel == rel_mine else "NOT as mine")] += 1
    print(f"  local contests {len(loc):,}: {dict(t)}")
    for b in bad:
        print(f"    not matched: {b}")
    print(f"  the gate on each: {dict(gate_ok)}; the record's counts: {L.load_json(os.path.join(L.DATA, 'local', 'check-nj.json'))['county_gate']['contests']}")
    st = collections.Counter()
    for c in loc:
        county = fips_to[c["place"]["counties"][0]]
        p = c["p"]
        if "value" in p:
            st[("released" if county in released_set else "HELD COUNTY", "p " + ("0 (unopposed)" if p["value"] == 0 else "computed, " + (c.get("forecasts") or [{}])[-1].get("route", "?")))] += 1
        else:
            r = p.get("not_computed") or ""
            st[("released" if county in released_set else "held county", "county does not add up" if "do not add up" in r else "ballots cast" if "ballots cast" in r else "other reason")] += 1
    print("  p by the gate: " + "; ".join(f"{k[0]}, {k[1]}: {v}" for k, v in sorted(st.items())))
    mq = collections.Counter()
    for c in meas:
        county = fips_to[c["place"]["counties"][0]] if c["place"].get("counties") else None
        g = c.get("gate") or {}
        mq[("released" if g.get("released") else "held", "as mine" if bool(g.get("released")) == (county in released_set) else "NOT as mine", "p" if "value" in c["p"] else "no p")] += 1
    print(f"  questions {len(meas)}: {dict(mq)}")
    return loc


# ---------------------------------------------------------------- 21.5 the clerks
def section_5(loc):
    print("21.5 The five county clerks' official counts against the file")
    rec = L.load_json(os.path.join(L.DATA, "local", "check-nj.json"))["county_gate"]["clerk_check"]
    d = os.path.join(NJ, "clerks")
    def txt(name):
        p = os.path.join(d, f"{name}.txt")
        if not os.path.exists(p):
            subprocess.run(["pdftotext", "-layout", os.path.join(d, f"{name}.pdf"), p], check=True)
        return open(p, encoding="utf-8", errors="replace").read().split("\n")
    def file_contest(office_words):
        for c in loc:
            if norm(c["office"]) == norm(office_words):
                return c
    for county, r in rec.items():
        c = file_contest(r["office"])
        fv = {("WRITEIN" if x["name"].upper() == "WRITE-IN" else surname(x["name"])): x["votes"] for x in c["result"]["candidates"]} if c else {}
        name = county.lower()
        if county == "MORRIS":
            print(f"  Morris: the clerk's site answered my curl with HTTP 403 (refused; not retried), so D3's reading (worst miss {r['worst_miss']}, 6 votes) stands unverified here; the file's contest {c['id'] if c else None}")
            continue
        lines = txt(name)
        got = {}
        if county == "CAMDEN":
            i = next(i for i, ln in enumerate(lines) if ln.strip() == "Members of the Board of County Commissioners")
            for ln in lines[i:i + 40]:
                m = re.match(r"^([A-Za-z.,' -]+?)\s*\((D|R)\)\s+([\d,]+)", ln)
                if m:
                    got[surname(m.group(1).replace(",", ""))] = num(m.group(3))
                if re.match(r"^\s*Write-?In Totals\s+([\d,]+)", ln, re.I):
                    got["WRITEIN"] = num(re.match(r"^\s*Write-?In Totals\s+([\d,]+)", ln, re.I).group(1))
                    break
        elif county == "SUSSEX":
            i = next(i for i, ln in enumerate(lines) if ln.strip() == "COUNTY COMMISSIONER")
            for ln in lines[i:i + 12]:
                m = re.match(r"^\s*(DEM|REP|NON|IND)\s+(.+?)\s{2,}([\d,]+)\s+[\d.]+%", ln)
                if m:
                    got[surname(m.group(2))] = num(m.group(3))
                m = re.match(r"^\s*(Write-?in|Personal Choice)\S*\s+([\d,]+)", ln, re.I)
                if m:
                    got["WRITEIN"] = num(m.group(2))
        elif county == "OCEAN":
            # the canvass: each municipality's section lists the contest's candidates with their votes and a percent
            in_block = False
            sections = 0
            for ln in lines:
                if "MEMBER OF THE BOARD OF COMMISSIONERS" in ln:
                    in_block = True
                    sections += 1
                    continue
                if in_block:
                    m = re.match(r"^\s*(REP|DEM|NON|IND)?\s*([A-Za-z.' -]+?)\s{2,}([\d,]+)\s+[\d.]+%\s*$", ln)
                    if m:
                        got[surname(m.group(2))] = got.get(surname(m.group(2)), 0) + num(m.group(3))
                    elif re.match(r"^\s*(Write-?in|Personal Choice)", ln, re.I):
                        m2 = re.search(r"([\d,]+)\s+[\d.]+%", ln)
                        if m2:
                            got["WRITEIN"] = got.get("WRITEIN", 0) + num(m2.group(1))
                    elif ln.strip() and ln.strip().isupper() and "(" in ln and "COMMISSIONERS" not in ln:
                        in_block = False
            got["_sections"] = sections
        elif county == "HUNTERDON":
            # results by district: each page a table whose 'Totals' row carries the commissioners' columns first
            tot = None
            for j, ln in enumerate(lines):
                if ln.startswith("Totals"):
                    nums = [num(x) for x in re.findall(r"[\d,]+", ln)]
                    if all(v in nums for v in fv.values()):
                        tot = (j + 1, nums)
                        break
            got = {"_totals_row": tot}
        if "_totals_row" in got:
            tot = got["_totals_row"]
            print(f"  Hunterdon: a 'Totals' row of the clerk's results by district carrying every count of the file's candidates {sorted(fv.items())}: "
                  + (f"line {tot[0]}, {tot[1][:5]} (its first five columns), so no miss" if tot else "NONE FOUND") + f" (the record: worst miss {r['worst_miss']})")
            continue
        sections = got.pop("_sections", None)
        cmp = {k: (got.get(k), fv.get(k)) for k in sorted(set(got) | set(fv))}
        worst = max((abs(a / b - 1) for a, b in cmp.values() if a and b), default=None)
        print(f"  {county.title()}{'' if sections is None else f' ({sections} municipal sections added up)'}: clerk/file " + ", ".join(f"{k} {a}/{b}" for k, (a, b) in cmp.items()) + f"; worst miss {worst if worst is None else f'{worst:.2e}'} (the record {r['worst_miss']}); holds (over 0.5%): {bool(worst and worst > LINE)}")


# ---------------------------------------------------------------- 21.6 the 52 p
def section_6(loc):
    print("21.6 The p New Jersey's released contests got, and which p files #65, #66 and #68 changed")
    rows = [r for r in D.rows("local") if r["state"] == "NJ" and r["year"] == 2024]
    medsl, nc, miss = C15.local_pools()
    cm = [r for r in rows if r["route"] in ("class", "boundary") and r["N"] is not None]
    C15.compare_like(cm, medsl, "New Jersey 2024's like-race p (the record: 43), like races from MEDSL's earlier years")
    txt = subprocess.run(["git", "show", "97e5141~1:data/local/2024/NJ.json"], cwd=L.ROOT, capture_output=True, text=True).stdout
    before = {c["id"]: c["p"].get("value") for c in json.loads(txt)["contests"]}
    new_p = [r for r in rows if r["status"] == "value" and r["p"]["value"] != 0 and before.get(r["id"]) in (None, 0)]
    print(f"  before #65 (97e5141~1): {len(before):,} contests, {sum(1 for v in before.values() if v)} with p other than 0, {sum(1 for v in before.values() if v == 0)} with p 0; today: {sum(1 for r in rows if r['status'] == 'value' and r['p']['value'] != 0)} with p other than 0, of which new {len(new_p)} (the record: 52 = 43 + 9); by route {dict(collections.Counter(r['route'] for r in new_p))}")
    part = [r for r in rows if r["route"] == "partisan" and r["status"] == "value"]
    worst = []
    for r in part:
        n = r["pair"]["votes"][0] + r["pair"]["votes"][1]
        f = r["share"]
        p, method, fh = D.p_auto(n, f["mean"], f["sd"], f.get("tails", "normal"))
        worst.append((abs(p / r["p"]["value"] - 1), r["id"], p, r["p"]["value"], method, r["p"].get("method")))
    worst.sort(reverse=True)
    print(f"  partisan-route p (the record: 9): {len(part)}; recomputed from the recorded mean, sd and n: largest relative difference {worst[0][0]:.1e} ({worst[0][1]}: mine {worst[0][2]:.4e} {worst[0][4]}, record {worst[0][3]:.4e} {worst[0][5]})" if worst else "  no partisan p")
    zero = [r for r in rows if r["status"] == "value" and r["p"]["value"] == 0]
    bad0 = [r["id"] for r in zero if sum(1 for a in r["cands"] if a[0] != "write-in" and a[2].upper() != "WRITE-IN") > (r["seats"] or 1)]
    print(f"  p = 0 (unopposed): {len(zero)} (the record: 246); with more names than seats among them: {len(bad0)}" + (f" {bad0[:3]}" if bad0 else ""))
    for pr, c in (("#65", "97e5141"), ("#66", "d2e26ac"), ("#68", "8990525")):
        out = subprocess.run(["git", "diff", "--stat=200", f"{c}~1", c], cwd=L.ROOT, capture_output=True, text=True).stdout
        files = [l.split("|")[0].strip() for l in out.strip().split("\n")[:-1]]
        pf = [f for f in files if re.match(r"data/[a-z-]+/\d{4}/", f)]
        print(f"  {pr} ({c}) changed {len(files)} files; p files among them: {pf}")


def main():
    print("C21. #65 AND #66: NEW JERSEY 2024 BY COUNTY, FROM THE STATE'S LISTS, MEDSL'S ROWS AND THE CLERKS' FILES")
    print(f"repository HEAD {L.git_head()}")
    for name in ("president.pdf", "us-senate.pdf", "us-house.pdf", os.path.join("medsl", "2024-nj-precinct-general.csv")):
        if not os.path.exists(os.path.join(NJ, name)):
            print(f"  {name} is not in {NJ}: fetched by curl from the Division of Elections' page and Harvard Dataverse (doi:10.7910/DVN/NYTPDU, file 13731174); skipped")
            return
    lists = section_1()
    by, party, mag, rows_seen = load_medsl()
    print(f"  MEDSL's file: {sum(rows_seen.values()):,} rows read; {len(by):,} contests (county, office, district); {len({(k[0], p) for k, prec in by.items() for p in prec}):,} county-precincts")
    adds_all = section_2(lists, by, party)
    held_rows, total_line = section_3(by, party, mag, rows_seen)
    loc = section_4(by, party, mag, adds_all, held_rows)
    section_5(loc)
    section_6(loc)


if __name__ == "__main__":
    main()
