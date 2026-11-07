"""pipeline/local_volume.py: the volume test of MEDSL's precinct files, and the holds and notes it decides.

Written 2026-11-07 by worker D3 on the orchestrator's rulings of 18:54, 19:04, 19:13 and 19:49. Reason (the orchestrator,
18:54): "n enters p directly, so a doubled count halves a figure we show"; a share test cannot see a count that is
doubled or missing a county, since the shares stay the same. The rulings:
  18:54 (b) "Volume test for every MEDSL state-year taken in": part 1, "the precinct sum of the top contest (president,
        governor, Senate or House) against our independent count, with 0.5% as the bound"; part 2, "where MEDSL and
        Klarner overlap (2016-2022), compare candidate by candidate. Flag a state-year where more than 5% of matched
        candidates sit at a ratio of 2 or 1/2 (+-1%), or where the median ratio is off 1 by more than 3%". "Settle each
        flag by the state's own count. Hold the wrong source's records unless a rule fixes them exactly."
  19:04 3. "Apply the fusion rule (a candidate's party lines summed) to CT and NY, and test again." "Settle the
        remaining flags from the state where it answers." "An unsettled flag of 5% or more holds the state-year's MEDSL
        records. Under 5%, keep them with a note giving the difference and why it is unsettled." Reason: "a structural
        fault like doubling or a missing county shows as a large gap, while a small unsettled gap moves p by about the
        same small fraction, well inside the forecast's own spread. The note keeps it visible."
  19:13 1. Maine 2016: "use D1's 2016 president (or D2's House) as part 1's top contest, which is what part 1 should do
        in any year without a governor"; 4. New Jersey 2018: "hold only the MEDSL records whose area includes
        Middlesex"; 5. "NY 2018 held; NY 2022, MI 2022 and IN 2018 kept with notes: agreed."
  19:49 1. "NJ 2018: hold Hunterdon-area records too. That matches NJ 2024's county gate, which held any county past
        0.5% on federal offices." 3. "ME 2016: hold the 53". 5. "list in REPORT which state-years part 1 or part 2
        could test, and which neither could. Then add part 3, a structural scan of every MEDSL file. Look for aggregate
        rows beside precinct rows (names like "COUNTY TOTAL", "TOTAL" or "CUMULATIVE"), and any row equal to the sum of
        the other rows for the same contest, county and candidate. Apply the ID rule where it reproduces the parts
        exactly; list the rest for me. Reason: Idaho's fault was structural, and a scan can find it where no second
        count exists."

Part 1's top contest: the governor where the state elected one that year (D2's data/governor/<year>.json, not a
special), else the US House (D2's data/house/<year>.json, as pipeline/intake/medsl_precinct.py check_house adds it up,
every line's votes together). MEDSL's 2016 files hold no federal contest, so 2016's part 1 is the governor alone. 2020's
MEDSL file is local offices only (2020-all-states-local-precinct-general.csv): no top contest to test, and Klarner's
2020 is not beside it in part 2 either; 2020 is listed as untested. 2024 has its own gate (local_medsl.quality: the
president against D1's certified count, at the same 0.5%).

Governors are matched by surname: D2's two leading candidates, against MEDSL's lines for that surname. A fusion
candidate (Connecticut, New York) has several lines; both readings are tried, the lines summed (the ruling's rule) and
the line of D2's party alone (where D2's source reports that line only: Connecticut's Lamont and Stefanowski, 2018,
data/governor/2018.json). The lines summed are the miss; the own line is used only where it comes within part 1's
bound, and otherwise is written beside the miss [the reading].

Settlements read from the states' own files (no request is made here; each was read once, between 19:07 and 19:12 UTC,
and is kept in $VOTE_CACHE/volume/raw with its .meta.json):
  Hawaii 2018      the Office of Elections' certified summary (pipeline/governor_hi2018.py): D2's Tupola 137,719 was
                   the dataset's typo for 131,719; with D2's file fixed, MEDSL equals it.
  New Jersey 2018  the Division of Elections' "Official List" of 12/03/2018 for the House, by county, every candidate:
                   its total equals D2's; MEDSL is short in Middlesex (-18.04%) and Hunterdon (-0.78%) and within 0.5%
                   in every other county.
  DC 2018          the Board of Elections' "General Election 2018 - Certified Results" page (rendered): MEDSL's mayor
                   equals it to the vote. DC elects no governor and D2 holds no House count for it.

Part 3 (scan): every MEDSL raw file of the five years, row by row, for rows named as totals beside precinct rows and
rows equal to the sum of the others (scan_file); the normalizer's rules (medsl_precinct.drop_county_totals and
drop_sum_rows) drop those that reproduce their parts exactly, and check() lists the rest in check-volume.json "part3".

Run:  VOTE_CACHE=/tmp/vote-cache python3 pipeline/local_volume.py scan --year <year>   (each year; the cache)
      VOTE_CACHE=/tmp/vote-cache python3 pipeline/local_volume.py check    (writes data/local/check-volume.json)
The build (local_medsl.load) reads that file through volume_gate.
"""
import argparse
import collections
import glob
import html
import json
import os
import re
import statistics
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "intake"))
import fetch as F  # noqa: E402

REPO = os.path.dirname(HERE)
CHECK = os.path.join(REPO, "data", "local", "check-volume.json")
NORM = os.path.join(F.CACHE, "medsl", "normalized")
RAWDIR = os.path.join(F.CACHE, "medsl", "raw")
VRAW = os.path.join(F.CACHE, "volume", "raw")
VNORM = os.path.join(F.CACHE, "volume", "normalized")
LINE = 0.005          # part 1's bound (ruling 18:54 (b))
TWO_SHARE = 0.05      # part 2: more than 5% of matched candidates at 2 or 1/2
TWO_TOL = 0.01        # +-1% of the ratio
MEDIAN_OFF = 0.03     # part 2: the median ratio off 1 by more than 3%
HOLD_AT = 0.05        # an unsettled flag of 5% or more holds (ruling 19:04 3)
YEARS = (2016, 2018, 2022)
GOV = re.compile(r"GOVERNOR( AND LIEUTENANT GOVERNOR| & LIEUTENANT GOVERNOR|/LIEUTENANT GOVERNOR)?")
STATE_2016 = "2016-3345337-2016-precinct-state.csv"

# What the rulings decide for each flag the test raises. The build stops on a flag this table does not answer, so a
# new flag cannot pass unseen. "hold": every MEDSL record of the state-year is held; "hold_counties": the records
# whose area includes a county named by the settlement are held; "note": kept, with the note; "settled": the state's
# own count settles it and nothing is held; "held_already": the state-year's records are already held by the quality
# gate (local_medsl.quality); "no_records": MEDSL's file gives no record for that state-year.
VERDICTS = {
    (2016, "ME"): ("hold", "ruling 19:13 1",
                   "MEDSL's 2016 state file is short of Klarner's Maine legislature (median ratio {median:.3f}, "
                   "{matched} candidates matched) and neither of MEDSL's 2016 files holds a federal contest to test it "
                   "against (D1's president or D2's House), and the state refused (19:12 UTC); an unsettled flag of "
                   "5% or more holds the state-year's MEDSL records"),
    (2018, "NY"): ("hold", "rulings 19:04 3 and 19:13 5",
                   "MEDSL's 2018 New York precincts add up to {worst_pct} of D2's certified count for governor "
                   "({reading}); its governor's votes lie in {medsl_counties} of the state's 62 counties, and the "
                   "State Board refused (18:49 UTC); a missing county is a structural fault, so the state-year's MEDSL "
                   "records are held"),
    (2018, "NJ"): ("hold_counties", "ruling 19:13 4",
                   "MEDSL's 2018 New Jersey precincts add up to {worst_pct} of D2's certified US House count; the "
                   "Division of Elections' Official List (12/03/2018), whose total equals D2's, shows MEDSL's precincts "
                   "short in {counties_named} and within 0.5% in every other county, so records whose area includes "
                   "one of those counties are held and the rest kept"),
    (2018, "OR"): ("settled", "ruling 19:49 5",
                   "MEDSL's 2018 Oregon file filed some counties' sums as precincts named TOTAL beside their precincts; "
                   "the county-total rule drops them (medsl_precinct.drop_county_totals), and its governor then equals "
                   "D2's certified count to the vote"),
    (2018, "IN"): ("note", "rulings 19:04 3 and 19:13 5",
                   "MEDSL's 2018 Indiana precincts add up to {worst_pct} of D2's certified US House count (Indiana "
                   "elected no governor in 2018); not settled, since the state's 2018 results were not found at its "
                   "archive's addresses; under 5%, so kept"),
    (2018, "HI"): ("settled", "ruling 19:13 3",
                   "D2's count was the dataset's 137,719 for Tupola; the Office of Elections' certified summary has "
                   "131,719, equal to MEDSL's (pipeline/governor_hi2018.py)"),
    (2018, "CT"): ("settled", "ruling 19:04 3",
                   "D2's source gives each governor candidate's own party line; MEDSL's lines equal them"),
    (2022, "NY"): ("note", "rulings 19:04 3 and 19:13 5",
                   "MEDSL's 2022 New York precincts add up to {worst_pct} of D2's certified count for governor "
                   "({reading}); not settled, since the State Board refused (18:49 UTC); under 5%, "
                   "so kept"),
    (2022, "MI"): ("note", "rulings 19:04 3 and 19:13 5",
                   "MEDSL's 2022 Michigan precincts add up to {worst_pct} of D2's certified count for governor; not "
                   "settled, since the state's results site refused earlier today; under 5%, so kept"),
    (2022, "AR"): ("held_already", "local_medsl.quality",
                   "MEDSL's 2022 Arkansas precincts add up to {worst_pct} of D2's certified count for governor; the "
                   "state-year's records are already held by the share check"),
    (2022, "IN"): ("held_already", "local_medsl.quality",
                   "MEDSL's 2022 Indiana file adds up to {worst_pct} of D2's certified US House count; the "
                   "state-year's records are already held by the share check"),
    (2022, "NH"): ("settled", "ruling 19:04 1",
                   "Klarner's figures are doubled; MEDSL's counts stand, and Klarner's 2022 legislature takes them "
                   "where every candidate matches by name (pipeline/local.py nh_2022)"),
    (2022, "ID"): ("settled", "ruling 19:04 2",
                   "MEDSL's file counted each county twice (a COUNTY TOTAL line beside its precincts); the rule that "
                   "drops such a line where the precincts add up to it (medsl_precinct.drop_county_totals) leaves "
                   "Power County's absence alone"),
    (2022, "NJ"): ("no_records", "-",
                   "MEDSL's 2022 New Jersey file holds two legislative lines and no local contest, so it gives no "
                   "record"),
}


def _pct(x):
    return f"{100 * (1 + x):.2f}%"


def _surname_tokens(name):
    """The words of a MEDSL name (the first name of a ticket), with and without its punctuation run together."""
    first = re.split(r"\s*/\s*|\s+AND\s+|\s*&\s*", name.upper())[0]
    return set(re.sub(r"[^A-Z ]", " ", first).split()) | set(re.sub(r"[^A-Z ]", "", first).split())


def _gov_records(year):
    with open(os.path.join(REPO, "data", "governor", f"{year}.json")) as f:
        d = json.load(f)
    return {c["place"]["state"]: c for c in d["contests"] if not c.get("special") and c["place"]["state"]}


def _medsl_states(year):
    out = collections.defaultdict(list)
    for p in sorted(glob.glob(os.path.join(NORM, str(year), "*.jsonl"))):
        out[os.path.basename(p).split("-")[0]].append(p)
    return out


def _raw_path(year, st):
    """MEDSL's raw file for a state-year (2018's GitHub zips, 2022's state files), or None."""
    pats = [f"{year}-github-{year}-{st.lower()}-precinct-general.zip", f"{year}-*-{st.lower()}22_cleaned.csv",
            f"{year}-*-{year}-{st.lower()}-*.csv", f"{year}-*-{year}-{st.lower()}-*.zip"]
    for pat in pats:
        hit = sorted(glob.glob(os.path.join(RAWDIR, pat)))
        if hit:
            return hit[0]
    return None


def _gov_lines(path, st):
    """{(candidate, party_detailed): votes} for a state's regular general governor rows in a raw MEDSL file."""
    import medsl_precinct as P
    agg = collections.defaultdict(lambda: collections.defaultdict(dict))
    for r in P._rows(path):
        if (r.get("state_po") or st) != st or not GOV.fullmatch((r.get("office") or "").upper()):
            continue
        if (r.get("stage") or "GEN").upper() != "GEN" or (r.get("special") or "").upper() == "TRUE":
            continue
        try:
            v = int(float(r.get("votes") or 0))
        except ValueError:
            v = 0
        pk = (r.get("county_fips"), r.get("jurisdiction_fips"), r.get("precinct"))
        ck = (r.get("candidate") or "", (r.get("party_detailed") or "").upper())
        m = agg[ck].setdefault(pk, {})
        mode = (r.get("mode") or "TOTAL").upper()
        m[mode] = m.get(mode, 0) + v
    return {ck: sum(P.resolve(m) or 0 for m in pp.values()) for ck, pp in agg.items()}


PARTY_WORD = {"D": ("DEMOCRAT", "DEMOCRATIC"), "R": ("REPUBLICAN",)}


def governor(year, st, rec, paths):
    """Part 1 by governor: D2's two leading candidates against MEDSL's lines, both readings (module docstring)."""
    import local_medsl as M
    med = []
    for p in paths:
        with open(p) as f:
            for line in f:
                m = json.loads(line)
                if GOV.fullmatch(m["office"]) and m["stage"] == "GEN" and not m.get("special"):
                    med.append(m)
    if not med:
        return None
    d2 = sorted([c for c in rec["result"]["candidates"] if c.get("votes")], key=lambda c: -c["votes"])[:2]
    rows, raw_lines = [], None
    for c in d2:
        key = M.name_key(c["name"])[0]
        summed = sum(x["votes"] for m in med for x in m["candidates"] if key in _surname_tokens(x["name"]))
        rows.append({"candidate": c["name"], "party": c.get("party"), "d2": c["votes"], "medsl_lines_summed": summed})
    for r in rows:
        r["miss_lines_summed"] = round(r["medsl_lines_summed"] / r["d2"] - 1, 5)
    worst = max(rows, key=lambda r: abs(r["miss_lines_summed"]))["miss_lines_summed"]
    reading = "the party lines summed"
    if abs(worst) > LINE:
        path = _raw_path(year, st)
        if path:
            raw_lines = _gov_lines(path, st)
            for r in rows:
                key = M.name_key(r["candidate"])[0]
                own = [v for (n, pdet), v in raw_lines.items()
                       if key in _surname_tokens(n) and pdet in PARTY_WORD.get(r["party"], ())]
                r["medsl_own_line"] = sum(own) if own else None
                r["miss_own_line"] = round(sum(own) / r["d2"] - 1, 5) if own else None
            if all(r.get("miss_own_line") is not None for r in rows):
                w2 = max(rows, key=lambda r: abs(r["miss_own_line"]))["miss_own_line"]
                if abs(w2) <= LINE:   # D2's source reports each candidate's own line (Connecticut 2018)
                    worst, reading = w2, "each candidate's own party line, as D2's source reports it"
                else:
                    reading += f"; on each candidate's own party line, {_pct(w2)}"
    counties = sorted({x for m in med for x in (m.get("counties") or []) if re.fullmatch(r"\d{5}", x or "")})
    return {"top": "governor", "d2_source": rec["result"]["source"]["name"][:80], "rows": rows,
            "worst": worst, "reading": reading, "medsl_contests": len(med), "medsl_counties": len(counties),
            "raw_file_read": os.path.basename(_raw_path(year, st)) if raw_lines is not None else None}


def house(year, st):
    """Part 1 by the US House: medsl_precinct.check_house's "all" row (every line's votes together, D2's count)."""
    p = os.path.join(NORM, f"checks-{year}.json")
    if not os.path.exists(p):
        return None
    with open(p) as f:
        rows = (json.load(f).get("house_by_party") or {}).get(st)
    a = next((r for r in rows or [] if r["party"] == "all"), None)
    if not a or not a["certified"]:
        return None
    return {"top": "US House", "d2_source": f"data/house/{year}.json", "d2": a["certified"],
            "medsl": a["medsl_precincts"], "worst": round(a["medsl_precincts"] / a["certified"] - 1, 5),
            "reading": "every line's votes together"}


# ------------------------------------------------------------------ 2016: MEDSL's state file, read once

def scan_2016():
    """MEDSL's 2016 state file's governors and legislatures, by state, its precincts added up (as the normalizer
    resolves a precinct's modes): cached in $VOTE_CACHE/volume/normalized/medsl-2016-state.json, keyed by the raw
    file's sha256."""
    raw = os.path.join(RAWDIR, STATE_2016)
    with open(raw + ".meta.json") as f:
        sha = json.load(f).get("sha256")
    out_p = os.path.join(VNORM, "medsl-2016-state.json")
    if os.path.exists(out_p):
        with open(out_p) as f:
            d = json.load(f)
        if d.get("sha256") == sha:
            return d
    gov = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(dict)))
    leg = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(dict)))
    import csv
    with open(raw, newline="", encoding="utf-8", errors="replace") as f:
        for r in csv.DictReader(f):
            if (r["stage"] or "").lower() != "gen" or (r["special"] or "").upper() == "TRUE":
                continue
            try:
                v = int(float(r["votes"]))
            except ValueError:
                v = 0
            o = (r["office"] or "").strip().upper()
            st = r["state_postal"]
            pk = (r["county_fips"], r["jurisdiction"], r["precinct"])
            mode = (r["mode"] or "total").lower()
            if GOV.fullmatch(o):
                c = gov[st][pk][(r["candidate"], r["party"], r["writein"])]
            elif o in ("STATE HOUSE", "STATE SENATE", "STATE REPRESENTATIVE", "STATE SENATOR"):
                c = leg[st][pk][(o, r["district"], r["candidate"], r["party"], r["writein"])]
            else:
                continue
            c[mode] = c.get(mode, 0) + v

    def res(m):
        return m["total"] if "total" in m else sum(m.values())
    d = {"sha256": sha, "file": STATE_2016, "gov": {}, "leg": {}}
    for name, src in (("gov", gov), ("leg", leg)):
        for st, pp in src.items():
            t = collections.Counter()
            for cs in pp.values():
                for ck, m in cs.items():
                    t["|".join(ck)] += res(m)
            d[name][st] = dict(t)
    os.makedirs(VNORM, exist_ok=True)
    with open(out_p, "w") as f:
        json.dump(d, f)
    return d


def governor_2016(st, rec, scan):
    import local_medsl as M
    t = scan["gov"].get(st)
    if not t:
        return None
    d2 = sorted([c for c in rec["result"]["candidates"] if c.get("votes")], key=lambda c: -c["votes"])[:2]
    rows = []
    for c in d2:
        key = M.name_key(c["name"])[0]
        v = sum(n for k, n in t.items() if key in _surname_tokens(k.split("|")[0]))
        rows.append({"candidate": c["name"], "party": c.get("party"), "d2": c["votes"], "medsl_lines_summed": v,
                     "miss_lines_summed": round(v / c["votes"] - 1, 5)})
    worst = max(rows, key=lambda r: abs(r["miss_lines_summed"]))["miss_lines_summed"]
    return {"top": "governor", "d2_source": rec["result"]["source"]["name"][:80], "rows": rows, "worst": worst,
            "reading": "the party lines summed", "medsl_file": STATE_2016}


# ------------------------------------------------------------------ part 2: MEDSL beside Klarner

def _klarner_by_district(kl, year):
    import local_medsl as M
    K = collections.defaultdict(lambda: collections.defaultdict(int))
    for c in kl:
        if c["year"] == year and c["etype"] == "g" and c["dno"]:
            d = str(int(c["dno"])) if str(c["dno"]).isdigit() else str(c["dno"])
            for a in c["cands"]:
                if a.get("scattering") or not a.get("votes"):
                    continue
                K[(c["state"], c["sen"], d)][M.name_key(a["name"])] += a["votes"]
    return K


def _summary(rs):
    n = len(rs)
    med = statistics.median(rs)
    two = sum(1 for r in rs if abs(r - 2) <= 2 * TWO_TOL or abs(r - 0.5) <= 0.5 * TWO_TOL)
    return {"matched": n, "median": round(med, 4), "at_2_or_half": two, "share_at_2_or_half": round(two / n, 4),
            "flag": two / n > TWO_SHARE or abs(med - 1) > MEDIAN_OFF}


def part2(year, kl, scan=None):
    """{state: summary} of MEDSL's legislative candidates' votes over Klarner's, matched by district and name."""
    import local_medsl as M
    K = _klarner_by_district(kl, year)
    mv = collections.defaultdict(lambda: collections.defaultdict(int))   # (st, sen, dist) -> {name: votes}
    if year == 2016:
        for st, t in scan["leg"].items():
            for k, v in t.items():
                off, dist, cand, party, wi = k.split("|")
                m = re.search(r"(\d+)", dist or "")
                if wi.upper() == "TRUE" or not v or M._is_generic(cand) or not m:
                    continue
                mv[(st, 1 if "SENATE" in off or "SENATOR" in off else 0, str(int(m.group(1))))][cand] += v
    else:
        for p in sorted(glob.glob(os.path.join(NORM, str(year), "*.jsonl"))):
            with open(p) as f:
                for line in f:
                    m = M.relabel(json.loads(line))
                    if m["office"] not in M.LEG or m["stage"] != "GEN" or m["special"]:
                        continue
                    dn = M.district_no(m["district"])
                    if dn is None:
                        continue
                    for x in M.ballot(m["candidates"]):
                        if x["votes"]:
                            mv[(m["state"], M.LEG[m["office"]], dn)][x["name"]] += x["votes"]
    rs = collections.defaultdict(list)
    for dk, cs in mv.items():
        kv = K.get(dk)
        if not kv:
            continue
        got = collections.defaultdict(int)
        for cand, v in cs.items():
            hit = [q for q in M.name_keys(cand) if q in kv]
            if hit:
                got[hit[0]] += v
        for q, v in got.items():
            rs[dk[0]].append(v / kv[q])
    return {st: _summary(r) for st, r in sorted(rs.items())}


# ------------------------------------------------------------------ settlements from the states' own files

def _meta(name):
    p = os.path.join(VRAW, name)
    with open(p + ".meta.json") as f:
        return p, json.load(f)


NJ_COUNTIES = ("ATLANTIC", "BERGEN", "BURLINGTON", "CAMDEN", "CAPE MAY", "CUMBERLAND", "ESSEX", "GLOUCESTER", "HUDSON",
               "HUNTERDON", "MERCER", "MIDDLESEX", "MONMOUTH", "MORRIS", "OCEAN", "PASSAIC", "SALEM", "SOMERSET",
               "SUSSEX", "UNION", "WARREN")


def settle_nj_2018():
    """The Division of Elections' Official List for the 2018 House, every candidate's votes by county, against MEDSL's
    precincts by county (its raw file's House rows, as the normalizer adds them up), and the list's total against D2's.
    Counties off by more than LINE are named."""
    page, page_meta = _meta("nj-election-information-2018.html")
    pdf, meta = _meta("nj-2018-official-general-election-results-us-house.pdf")
    with open(page, encoding="utf-8", errors="replace") as f:
        s = f.read()
    links = {(re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", t))).strip(), h)
             for h, t in re.findall(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', s, re.S)}
    if ("Official General Election Results: U.S. House of Representatives",
            "assets/pdf/election-results/2018/2018-official-general-election-results-us-house.pdf") not in links:
        raise SystemExit("local_volume: the Division's 2018 page does not link the House official results")
    txt = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True, check=True).stdout
    if "Official List" not in txt or "For GENERAL ELECTION 11/06/2018 Election" not in txt:
        raise SystemExit("local_volume: the NJ file is not the 2018 general's Official List")
    by = collections.Counter()   # county: every candidate's votes there, all districts
    pat = re.compile(r"^\s{20,}(" + "|".join(NJ_COUNTIES) + r")\s+\S.*?\s{2,}([\d,]+)\s*$")
    for line in txt.splitlines():
        m = pat.match(line)
        if m and not re.search(r", NJ \d{5}", line):   # not a candidate's address ("ATLANTIC CITY, NJ 08401")
            by[m.group(1)] += int(m.group(2).replace(",", ""))
    if set(by) != set(NJ_COUNTIES):
        raise SystemExit(f"local_volume: the Official List's counties read {sorted(by)}")
    with open(os.path.join(REPO, "data", "house", "2018.json")) as f:
        d2 = sum(x.get("votes") or 0 for c in json.load(f)["contests"] if c["place"]["state"] == "NJ"
                 and not c.get("special") for x in c["result"]["candidates"])
    import medsl_precinct as P
    agg = collections.defaultdict(lambda: collections.defaultdict(dict))
    for r in P._rows(_raw_path(2018, "NJ")):
        if r.get("state_po") != "NJ" or r.get("dataverse") != "HOUSE" or (r.get("stage") or "GEN") != "GEN":
            continue
        cand = (r.get("candidate") or "").strip()
        if P.is_meta(cand):
            continue
        try:
            v = int(float(r.get("votes") or 0))
        except ValueError:
            v = 0
        pk = (r.get("county_fips"), r.get("jurisdiction_fips"), r.get("precinct"))
        m = agg[((r.get("county_name") or "").upper(), cand)].setdefault(pk, {})
        mode = (r.get("mode") or "TOTAL").upper()
        m[mode] = m.get(mode, 0) + v
    med = collections.Counter()
    for (county, _), pp in agg.items():
        med[county] += sum(P.resolve(m) or 0 for m in pp.values())
    fips = {"ATLANTIC": "34001", "BERGEN": "34003", "BURLINGTON": "34005", "CAMDEN": "34007", "CAPE MAY": "34009",
            "CUMBERLAND": "34011", "ESSEX": "34013", "GLOUCESTER": "34015", "HUDSON": "34017", "HUNTERDON": "34019",
            "MERCER": "34021", "MIDDLESEX": "34023", "MONMOUTH": "34025", "MORRIS": "34027", "OCEAN": "34029",
            "PASSAIC": "34031", "SALEM": "34033", "SOMERSET": "34035", "SUSSEX": "34037", "UNION": "34039",
            "WARREN": "34041"}
    rows, short = {}, []
    for name in NJ_COUNTIES:
        miss = med[name] / by[name] - 1
        rows[fips[name]] = {"county": name.title(), "list": by[name], "medsl": med[name], "miss": round(miss, 5)}
        if abs(miss) > LINE:
            short.append(fips[name])
    return {"source": {"page": page_meta, "file": meta, "mark": "the file's heading 'Official List', dated 12/03/2018"},
            "list_total": sum(by.values()), "d2_total": d2, "list_equals_d2": sum(by.values()) == d2,
            "by_county": rows, "counties": short}


def settle_dc_2018():
    """The Board of Elections' certified mayor count against MEDSL's mayor contest."""
    page, meta = _meta("dc-2018-general-rendered.html")
    with open(page, encoding="utf-8", errors="replace") as f:
        s = re.sub(r"<script.*?</script>|<style.*?</style>", "", f.read(), flags=re.S)
    t = [html.unescape(x).strip() for x in re.split(r"<[^>]+>", s) if x.strip()]
    if "General Election 2018 - Certified Results" not in t:
        raise SystemExit("local_volume: the DC page is not marked 'General Election 2018 - Certified Results'")
    i = t.index("MAYOR OF THE DISTRICT OF COLUMBIA")
    board = {}
    j = i + 1
    while j + 1 < len(t) and t[j] not in ("OVER VOTES", "UNDER VOTES"):
        if re.fullmatch(r"[\d,]+", t[j + 1]):
            board[t[j]] = int(t[j + 1].replace(",", ""))
            j += 4 if j + 3 < len(t) and t[j + 3] == "%" else 2
        else:
            j += 1
    med = None
    for p in glob.glob(os.path.join(NORM, "2018", "DC-*.jsonl")):
        with open(p) as f:
            for line in f:
                m = json.loads(line)
                if m["office"] == "MAYOR":
                    med = {x["name"]: x["votes"] for x in m["candidates"]}
    bt, mt = sum(board.values()), sum((med or {}).values())
    return {"source": {"page": meta, "mark": "the page's heading 'General Election 2018 - Certified Results'"},
            "board": board, "medsl": med, "board_total": bt, "medsl_total": mt, "equal": bt == mt,
            "worst": round(mt / bt - 1, 5) if bt else None}


# ------------------------------------------------------------------ part 3: the structural scan of every file

AGG_NAME = re.compile(r"\bTOTALS?\b|CUMULATIVE|^ALL PRECINCTS$", re.I)


def raw_files(year):
    """The raw MEDSL files the normalizer reads for a year (its checks file's names), as cache paths."""
    with open(os.path.join(NORM, f"checks-{year}.json")) as f:
        names = list(json.load(f)["files"])
    out = []
    for n in names:
        hit = sorted(glob.glob(os.path.join(RAWDIR, f"{year}-github-{n}")) +
                     glob.glob(os.path.join(RAWDIR, f"{year}-[0-9]*-{n}")))
        out.append((n, hit[0] if hit else None))
    return out


def _listed(out, contest, county, p, kind, votes):
    """A row part 3 lists and does not drop, in full, where scan_file was asked to collect them (out["listed_rows"])."""
    if "listed_rows" in out:
        out["listed_rows"].append({"contest": list(contest), "county": county, "precinct": p[2], "kind": kind,
                                   "votes": [[c[0], c[1], c[2], v] for c, v in votes.items() if v]})


def _scan_groups(groups, out):
    """One state's {(contest, county): {precinct: {candidate: votes}}} into the file's tallies (scan_file)."""
    import medsl_precinct as P
    for (contest, county), pp in groups.items():
        if len(pp) < 2:
            continue
        named = [p for p in pp if AGG_NAME.search(p[2] or "")]
        plain = [p for p in pp if p not in set(named)]
        cands = {c for p in pp for c in pp[p]}
        plain_tot = {c: sum(pp[q].get(c, 0) for q in plain) for c in cands}
        for p in named:
            nm = re.sub(r"\s+", " ", (p[2] or "").strip().upper())
            t = out["named"].setdefault(nm, collections.Counter())
            if not any(any(pp[q].values()) for q in plain):
                t["alone"] += 1
                _listed(out, contest, county, p, "named, alone", pp[p])
                continue
            eq = all(pp[p].get(c, 0) == plain_tot[c] for c in cands)
            t["equal" if eq else "unequal"] += 1
            if not (eq and P.COUNTY_TOTAL.search(nm)):   # what the county-total rule does not drop
                _listed(out, contest, county, p, "named, equal" if eq else "named, unequal", pp[p])
            if eq and len(out["examples_named"]) < 40:
                out["examples_named"].append({"contest": list(contest), "county": county, "precinct": p[2]})
        # a row that is not named as a total but equals the sum of the others, for every candidate of the contest
        live = [q for q in plain if any(pp[q].values())]
        tot = {c: sum(pp[q].get(c, 0) for q in live) for c in cands}
        for p in live:
            if len(live) - 1 < 2:
                break
            if all(2 * pp[p].get(c, 0) == tot[c] for c in cands):
                others = [q for q in live if q != p]
                out["unnamed_equal"] += 1
                if sum(1 for c in cands if pp[p].get(c, 0)) < 2:   # the guard of drop_sum_rows keeps it
                    _listed(out, contest, county, p, "equal to the rest, one candidate with votes", pp[p])
                if len(out["examples_unnamed"]) < 40:
                    out["examples_unnamed"].append({"contest": list(contest), "county": county, "precinct": p[2],
                                                    "candidates": len(cands), "others": len(others)})


def scan_file(path, keep=frozenset(), collect=False):
    """Part 3 for one raw file: every row read, precincts resolved as the normalizer does (a TOTAL mode where there
    is one, else the modes added up), grouped by contest (state, office, district, stage, special, dataverse) and
    county. Counts the rows named as totals (AGG_NAME) beside other precincts, whether each equals the others' sum for
    every candidate, and the rows not so named that equal the others' sum for every candidate (at least two others).
    A state's groups are tallied when the file moves on to the next state, which keeps memory to one state; a state
    in `keep` (one whose rows the file gives in more than one block, found by a first pass) is held to the end of the
    file, so that a total row in one block and its precincts in another are seen together."""
    import medsl_precinct as P
    out = {"named": {}, "examples_named": [], "unnamed_equal": 0, "examples_unnamed": [], "rows": 0,
           "states_seen_twice": []}
    if collect:
        out["listed_rows"] = []
    groups = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(dict)))
    cur, done = None, set()

    def flush(final=False):
        res = {}
        for k in [k for k in groups if final or k[0][0] not in keep]:
            res[k] = {p: {c: (P.resolve(m) or 0) for c, m in cs.items()} for p, cs in groups.pop(k).items()}
        _scan_groups(res, out)
    for r in P._rows(path):
        out["rows"] += 1
        st = r.get("state_po") or r.get("state_postal") or ""
        if st != cur:
            if cur is not None:
                flush()
                done.add(cur)
            if st in done:
                out["states_seen_twice"].append(st)
            cur = st
        cand = (r.get("candidate") or "").strip()
        if P.is_meta(cand):
            continue
        try:
            v = int(float(r.get("votes") or 0))
        except ValueError:
            v = 0
        contest = (st, (r.get("office") or "").upper(), r.get("district") or "", (r.get("stage") or "").upper(),
                   (r.get("special") or "").upper(), (r.get("dataverse") or "").upper())
        county = P.fips5(r.get("county_fips") or "")
        pk = (county, r.get("jurisdiction_fips") or r.get("jurisdiction") or "", r.get("precinct") or "")
        ck = (cand, (r.get("party_detailed") or r.get("party") or "").upper(), (r.get("writein") or "").upper())
        mode = (r.get("mode") or "TOTAL").upper()
        m = groups[(contest, county)][pk].setdefault(ck, {})
        m[mode] = (m.get(mode) or 0) + v
    flush(final=True)
    out["named"] = {k: dict(v) for k, v in out["named"].items()}
    return out


def scan(year, collect=False):
    """Part 3 for every file of a year, cached in $VOTE_CACHE/volume/normalized/scan-<year>.json; with collect, every
    row it lists and does not drop, in full, in rows-<year>.json instead (for listed_rows_check)."""
    res = {}
    for name, path in raw_files(year):
        if path is None:
            res[name] = {"read": False, "why": "not in the cache"}
            continue
        r = scan_file(path, collect=collect)
        if r["states_seen_twice"]:
            again = sorted(set(r["states_seen_twice"]))
            r = scan_file(path, keep=frozenset(again), collect=collect)
            r["held_whole"] = again
        r["raw"] = os.path.basename(path)
        res[name] = r
        print(year, name, r["rows"], {k: v for k, v in r["named"].items()}, "unnamed equal", r["unnamed_equal"],
              flush=True)
    os.makedirs(VNORM, exist_ok=True)
    if collect:
        res = {n: {"raw": r.get("raw"), "listed_rows": r.get("listed_rows", [])} for n, r in res.items()}
    with open(os.path.join(VNORM, f"{'rows' if collect else 'scan'}-{year}.json"), "w") as f:
        json.dump(res, f, indent=1)
    return res


LISTED_LINE = 0.005   # the orchestrator, 20:28: a listed row that moves its record by more than 0.5% gets a note


def listed_rows_summary():
    """Every row part 3 lists and does not drop (scan with collect: rows-<year>.json in the cache), for the build's
    with-and-without test (local_medsl.listed_rows). The orchestrator, 2026-11-07 20:28: "The listed rows, (a) and
    (b): leave them listed and not dropped. For each one, compute the record it falls in with and without the row.
    Where the difference is more than 0.5% of the record's total, add a note on the record ("a possible total row in
    the source, not dropped"). Otherwise the list in REPORT is enough. Reason: the state-year tests pass, so the only
    question left is whether any one shown count is visibly off." Rows of the federal dataverses (PRESIDENT, SENATE,
    HOUSE) are counted only: they fall in no record of these files, whose federal counts are D1's and D2's."""
    out = {"line": LISTED_LINE, "years": {}}
    for year in (2016, 2018, 2020, 2022, 2024):
        p = os.path.join(VNORM, f"rows-{year}.json")
        if not os.path.exists(p):
            raise SystemExit(f"{p} is missing: run pipeline/local_volume.py rows --year {year} first")
        with open(p) as f:
            r = json.load(f)
        rows, federal = [], collections.Counter()
        for name, x in r.items():
            for row in x.get("listed_rows") or []:
                if row["contest"][5] in ("PRESIDENT", "SENATE", "HOUSE"):
                    federal[f"{row['contest'][0]} {row['contest'][5]}: {row['kind']}"] += 1
                else:
                    rows.append(dict(row, file=name))
        out["years"][str(year)] = {"rows": rows, "federal_counted_only": dict(sorted(federal.items()))}
    return out


# ------------------------------------------------------------------ part 4: ballots cast, for the over-ballot test

# The orchestrator's order of 2026-11-07 17:44 (3): "The over-ballot test runs in every year. Hold a one-seat contest
# whose votes exceed ballots cast, where the source gives them. Where it doesn't, hold one that exceeds the day's
# highest-vote statewide contest by more than 10%, and list for me any between 1.0x and 1.1x. Reason: one seat can't
# draw more votes than there were ballots, while a small excess over the top contest can be real." Ballots cast are
# read as the ruling of 11:16 read them for New Jersey (pipeline/local_nj.py medsl_rows): in a precinct, a vote-for-1
# contest's votes plus its overvotes plus its undervotes, or its "CONTEST TOTAL" line, or a line the file names as the
# ballots cast there; the largest of these. A contest is bounded by the other contests' figures only, never its own,
# since a contest whose lines are counted twice counts its over- and undervotes twice too [the reading].
OVER_NAMES = {"OVERVOTES", "OVER VOTES", "OVERVOTE", "OVER VOTE"}
UNDER_NAMES = {"UNDERVOTES", "UNDER VOTES", "UNDERVOTE", "UNDER VOTE"}
BALLOTS_NAMES = {"BALLOTS CAST", "BALLOTS CAST-TOTAL", "BALLOTS CAST - TOTAL", "TOTAL BALLOTS CAST",
                 "NUMBER OF BALLOTS CAST"}
CONTEST_TOTAL = "CONTEST TOTAL"
TOP_DATAVERSES = ("PRESIDENT", "SENATE", "STATE")   # a statewide contest's dataverse in MEDSL's files (not HOUSE)
BALLOTS_YEARS = (2018, 2022, 2024)   # 2016 is read for its questions only, 2020's file is local offices only


def _one(m):
    """A line's votes from its modes, as the normalizer resolves them: its TOTAL mode where it has one."""
    return m["TOTAL"] if "TOTAL" in m else sum(m.values())


def ballots_file(path):
    """Part 4 for one raw file: for each GEN contest of one seat (MEDSL's magnitude 1), by state and date, its votes by
    precinct; each precinct's ballots cast as the file gives them (OVER_NAMES and UNDER_NAMES beside a contest's votes,
    its CONTEST TOTAL, or a line in BALLOTS_NAMES). Returns the statewide contests of dataverse STATE (the ones the
    local files take) with their votes and the bound, and each state-date's statewide candidate contests (TOP_DATAVERSES)
    with their votes and counties, for the day's highest-vote statewide contest."""
    import medsl_precinct as P
    lines = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(dict)))
    named = collections.defaultdict(lambda: collections.defaultdict(dict))   # (st, date) -> pk -> {line: modes}
    counties = collections.defaultdict(set)
    rows = 0
    for r in P._rows(path):
        rows += 1
        if (r.get("stage") or "").upper() != "GEN":
            continue
        st, date = r.get("state_po") or "", r.get("date") or ""
        cand = " ".join((r.get("candidate") or "").upper().split())
        county = P.fips5(r.get("county_fips") or "")
        pk = (county, r.get("jurisdiction_fips") or "", r.get("precinct") or "")
        mode = (r.get("mode") or "TOTAL").upper()
        try:
            v = int(float(r.get("votes") or 0))
        except ValueError:
            v = 0
        if cand in BALLOTS_NAMES:
            m = named[(st, date)][pk].setdefault((r.get("office") or "", cand), {})
            m[mode] = m.get(mode, 0) + v
            continue
        if (r.get("magnitude") or "") not in ("1", "1.0"):
            continue
        dv = (r.get("dataverse") or "").upper()
        k = (st, date, r.get("office") or "", r.get("district") or "", (r.get("special") or "").upper(), dv)
        if cand in OVER_NAMES:
            part = "over"
        elif cand in UNDER_NAMES:
            part = "under"
        elif cand == CONTEST_TOTAL:
            part = "total"
        elif P.is_meta(cand):
            continue
        else:
            part = "votes"
            if v:
                counties[(st, date)].add(county)
        m = lines[k][pk].setdefault((part, cand), {})
        m[mode] = m.get(mode, 0) + v
    # each contest's figures by precinct
    per = {}
    for k, pp in lines.items():
        per[k] = {pk: {"votes": sum(_one(m) for (part, _), m in c.items() if part == "votes"),
                       "has_over": any(part == "over" for part, _ in c), "has_under": any(part == "under" for part, _ in c),
                       "over_under": sum(_one(m) for (part, _), m in c.items() if part in ("over", "under")),
                       "total": max([_one(m) for (part, _), m in c.items() if part == "total"] or [None],
                                    key=lambda x: -1 if x is None else x)}
                  for pk, c in pp.items()}
    # each precinct's two best figures from contests, and the named lines
    best = collections.defaultdict(list)   # (st, date, pk) -> [(figure, contest key)]
    for k, pp in per.items():
        for pk, f in pp.items():
            fig = []
            if f["has_over"] and f["has_under"]:
                fig.append(f["votes"] + f["over_under"])
            if f["total"] is not None:
                fig.append(f["total"])
            if fig:
                best[(k[0], k[1], pk)].append((max(fig), k))
    for key in best:
        best[key] = sorted(best[key], key=lambda x: -x[0])[:2]
    namedmax = {(sd[0], sd[1], pk): max(_one(m) for m in ls.values()) for sd, pp in named.items() for pk, ls in pp.items()}
    tested, tops = [], collections.defaultdict(list)
    for k, pp in per.items():
        st, date, office, district, special, dv = k
        votes = sum(f["votes"] for f in pp.values())
        cs = {pk[0] for pk, f in pp.items() if f["votes"]}
        if dv in TOP_DATAVERSES and votes and counties[(st, date)] <= cs and \
                not all(P.split_answer(c) for (part, c) in {x for c in lines[k].values() for x in c} if part == "votes"):
            tops[f"{st} {date}"].append({"dataverse": dv, "office": office, "district": district, "special": special,
                                         "votes": votes})
        if dv != "STATE" or not votes:
            continue
        bound, bounded, used = 0, 0, collections.Counter()
        live = [pk for pk, f in pp.items() if f["votes"]]
        for pk in live:
            o = [b for b in best.get((st, date, pk), []) if b[1] != k]
            nm = namedmax.get((st, date, pk))
            cand = ([(o[0][0], "another contest's votes, overvotes and undervotes or its contest total")] if o else []) \
                + ([(nm, "a line the file names as the ballots cast")] if nm is not None else [])
            if cand:
                b = max(cand)
                bound += b[0]
                bounded += 1
                used[b[1]] += 1
        tested.append({"state": st, "date": date, "office": office, "district": district, "special": special,
                       "votes": votes, "precincts": len(live), "precincts_bounded": bounded,
                       "ballots_cast": bound if bounded == len(live) else None,
                       "ballots_cast_in_bounded_precincts": bound, "bound_from": dict(used),
                       "counties": len(cs), "counties_of_day": len(counties[(st, date)])})
    return {"rows": rows, "tested": tested, "tops": {sd: sorted(t, key=lambda x: -x["votes"]) for sd, t in tops.items()},
            "counties_of_day": {f"{st} {date}": sorted(c) for (st, date), c in counties.items()}}


def ballots(year):
    """Part 4 for every file of a year, cached in $VOTE_CACHE/volume/normalized/ballots-<year>.json."""
    res = {}
    for name, path in raw_files(year):
        if path is None:
            res[name] = {"read": False, "why": "not in the cache"}
            continue
        r = ballots_file(path)
        r["raw"] = os.path.basename(path)
        res[name] = r
        given = sum(1 for t in r["tested"] if t["ballots_cast"] is not None)
        print(year, name, r["rows"], "tested", len(r["tested"]), "with ballots cast", given, flush=True)
    os.makedirs(VNORM, exist_ok=True)
    with open(os.path.join(VNORM, f"ballots-{year}.json"), "w") as f:
        json.dump(res, f, indent=1)
    return res


def ballots_summary():
    """Part 4 from the cache, for check-volume.json: by year, the statewide contests of one seat in MEDSL's files with
    their votes and the ballots cast where the file gives them in every precinct, and each state-date's statewide
    candidate contests (the day's highest-vote statewide contest is the first that is not the contest itself)."""
    out = {"rule": "the orchestrator's order of 2026-11-07 17:44 (3); pipeline/local_volume.py part 4",
           "untested": {"2016": "MEDSL's 2016 files are read for their questions only (no seat counts)",
                        "2020": "MEDSL's 2020 file holds local offices only"}}
    for year in BALLOTS_YEARS:
        p = os.path.join(VNORM, f"ballots-{year}.json")
        if not os.path.exists(p):
            raise SystemExit(f"{p} is missing: run pipeline/local_volume.py ballots --year {year} first")
        with open(p) as f:
            b = json.load(f)
        tested, tops = [], {}
        for name, r in b.items():
            if not r.get("rows"):
                continue
            for t in r["tested"]:
                tested.append(dict(t, file=name))
            for sd, t in r["tops"].items():
                tops.setdefault(sd, []).extend(t)
        out[str(year)] = {"tested": sorted(tested, key=lambda t: (t["state"], t["date"], t["office"], t["district"])),
                          "tops": {sd: sorted(t, key=lambda x: -x["votes"]) for sd, t in sorted(tops.items())}}
    return out


# ------------------------------------------------------------------ the check

def check():
    import local as L
    kl = L.load_klarner(raw=True)
    out = {"about": "the volume test of MEDSL's precinct files (pipeline/local_volume.py; the orchestrator's rulings "
                    "of 2026-11-07 18:54, 19:04 and 19:13; data/local/REPORT.md section 29)",
           "line": LINE, "part2_rule": {"share_at_2_or_half_over": TWO_SHARE, "ratio_tolerance": TWO_TOL,
                                        "median_off_over": MEDIAN_OFF},
           "untested": {"2020": "MEDSL's 2020 file holds local offices only (no top contest), and part 2's overlap "
                                "with Klarner is 2016-2022 for the years MEDSL's files hold a legislature",
                        "2024": "tested by local_medsl.quality (the president against D1's certified count)"},
           "years": {}}
    scan = scan_2016()
    for year in YEARS:
        G = _gov_records(year)
        states = _medsl_states(year)
        p1 = {}
        for st in sorted(states):
            if year == 2016:
                r = governor_2016(st, G[st], scan) if st in G else None
            else:
                r = governor(year, st, G[st], states[st]) if st in G else None
                r = r or house(year, st)
            if year == 2018 and st == "DC":
                dc = settle_dc_2018()
                r = {"top": "mayor (DC elects no governor; D2 holds no House count for it)",
                     "d2_source": "the Board of Elections' certified results", "worst": dc["worst"],
                     "reading": "every candidate's votes together", "settlement": dc}
            p1[st] = r or {"top": None, "why": "no governor that year and no House count beside MEDSL's (MEDSL's "
                                               "2016 files hold no federal contest)" if year == 2016 else
                           "no governor that year and no House count beside MEDSL's"}
            if r:
                p1[st]["flag"] = abs(r["worst"]) > LINE
        p2 = part2(year, kl, scan)
        flags = sorted({st for st, r in p1.items() if r.get("flag")} | {st for st, r in p2.items() if r["flag"]})
        y = {"part1": p1, "part2": p2, "flags": {}}
        for st in flags:
            v = VERDICTS.get((year, st))
            f = {"part1": p1.get(st, {}).get("flag", False), "part2": p2.get(st, {}).get("flag", False),
                 "verdict": v[0] if v else None, "by": v[1] if v else None}
            if (year, st) == (2018, "NJ"):
                f["settlement"] = settle_nj_2018()
            y["flags"][st] = f
        # a flag that the fixes have cleared since the rulings (Hawaii 2018 after D2's file is fixed; Idaho 2022
        # after the county-total rule) is listed as passing
        y["cleared"] = {f"{y_}-{st}": v[2] for (y_, st), v in VERDICTS.items()
                        if y_ == year and v[0] == "settled" and st not in flags}
        out["years"][str(year)] = y
        print(year, "part 1 tested", sum(1 for r in p1.values() if r.get("top")), "of", len(p1), "; flags:",
              {st: (f["verdict"], p1.get(st, {}).get("worst"), p2.get(st, {}).get("median")) for st, f in y["flags"].items()})
    out["coverage"] = coverage(out)
    out["part3"] = part3_summary()
    out["ballots"] = ballots_summary()
    out["listed_rows"] = listed_rows_summary()
    with open(CHECK, "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
        f.write("\n")
    return out


def coverage(out):
    """Which of each year's MEDSL state-years part 1 or part 2 could test, and which neither (the orchestrator,
    19:49: "list in REPORT which state-years part 1 or part 2 could test, and which neither could")."""
    cov = {}
    for year in YEARS:
        y = out["years"][str(year)]
        states = sorted(y["part1"])
        p1 = sorted(st for st, r in y["part1"].items() if r.get("top"))
        p2 = sorted(set(y["part2"]) & set(states))
        cov[str(year)] = {"states": len(states), "part1": p1, "part2": p2,
                          "neither": sorted(set(states) - set(p1) - set(p2))}
    st20 = sorted(_medsl_states(2020))
    cov["2020"] = {"states": len(st20), "part1": [], "part2": [], "neither": st20,
                   "why": "MEDSL's 2020 file holds local offices only: no governor, House or legislature"}
    with open(os.path.join(NORM, "checks-2024.json")) as f:
        pres = sorted(json.load(f).get("president") or {})
    st24 = sorted(_medsl_states(2024))
    cov["2024"] = {"states": len(st24), "president_gate": sorted(set(pres) & set(st24)),
                   "neither": sorted(set(st24) - set(pres)),
                   "why": "2024's test is local_medsl.quality: the president against D1's certified count"}
    return cov


def part3_summary():
    """The structural scan (scan) of each year's files, from the cache: the files with rows named as totals beside
    precincts, or rows that equal the others' sum."""
    out = {}
    for year in (2016, 2018, 2020, 2022, 2024):
        p = os.path.join(VNORM, f"scan-{year}.json")
        if not os.path.exists(p):
            out[str(year)] = {"scanned": False}
            continue
        with open(p) as f:
            sc = json.load(f)
        files = {}
        for name, r in sc.items():
            if not r.get("rows"):
                files[name] = {"read": False, "why": r.get("why")}
                continue
            if r["named"] or r["unnamed_equal"] or r["states_seen_twice"]:
                files[name] = {k: r[k] for k in ("rows", "named", "unnamed_equal", "examples_named",
                                                 "examples_unnamed", "states_seen_twice", "held_whole")
                                if k in r}
        import medsl_precinct as P
        for name, f in files.items():
            if "named" in f:
                f["rule_drops"] = sorted(n for n, t in f["named"].items() if P.COUNTY_TOTAL.search(n) and t.get("equal"))
                f["listed_for_the_orchestrator"] = sorted(n for n, t in f["named"].items()
                                                          if not (P.COUNTY_TOTAL.search(n) and t.get("equal")))
        with open(os.path.join(NORM, f"checks-{year}.json")) as f:
            chk = json.load(f).get("files") or {}
        for name, f in files.items():
            c_ = chk.get(name) or {}
            for k_ in ("county_total_lines", "county_total_lines_federal", "sum_rows", "sum_rows_federal",
                       "sum_rows_where"):
                if c_.get(k_):
                    f.setdefault("normalizer", {})[k_] = c_[k_]
        out[str(year)] = {"scanned": True, "files": len(sc), "rows": sum(r.get("rows") or 0 for r in sc.values()),
                          "files_with_findings": files}
    return out


# ------------------------------------------------------------------ the gate the build reads

_CACHE = {}


def _load_check():
    if "c" not in _CACHE:
        if not os.path.exists(CHECK):
            raise SystemExit("data/local/check-volume.json is missing: run pipeline/local_volume.py check first")
        with open(CHECK) as f:
            _CACHE["c"] = json.load(f)
    return _CACHE["c"]


def words(year, st):
    """The verdict's words for a flagged state-year, filled from the check."""
    c = _load_check()["years"][str(year)]
    kind, by, text = VERDICTS[(year, st)]
    p1 = c["part1"].get(st) or {}
    p2 = c["part2"].get(st) or {}
    f = c["flags"].get(st) or {}
    names = " and ".join(f"{r['county']} County ({100 * r['miss']:+.2f}%)"
                         for k, r in sorted((f.get("settlement") or {}).get("by_county", {}).items(),
                                            key=lambda kv: kv[1]["county"])
                         if k in (f.get("settlement") or {}).get("counties", []))
    return text.format(worst_pct=_pct(p1["worst"]) if p1.get("worst") is not None else "?",
                       reading=p1.get("reading", ""), median=p2.get("median", 0), matched=p2.get("matched", 0),
                       counties_named=names, medsl_counties=p1.get("medsl_counties", "?")) + \
        f" (data/local/check-volume.json; {by})"


# Counties whose MEDSL counts are missing, so that a record whose area includes one is held whatever the test says:
# Idaho 2022's Power County (the orchestrator's ruling of 19:04: "Any other ID 2022 MEDSL record whose area includes
# Power County is held"). The six statewide offices take the state's own counts (local_medsl.id_statewide) and are
# not held.
COUNTY_HOLDS = {
    (2022, "ID"): (["16077"], "ruling 19:04 2",
                   "MEDSL's 2022 Idaho file lacks Power County's precincts in this contest's offices, so a record whose "
                   "area includes Power County is held"),
}


def volume_gate(contests, year):
    """c["volume_gate"] = {"held": the reason or None, "note": the words or None, "record": the record's
    volume_check field} on each MEDSL contest of a flagged state-year (VERDICTS). Stops on a flag without a verdict."""
    if year not in YEARS:
        return contests
    c = _load_check()["years"][str(year)]
    missing = [st for st, f in c["flags"].items() if f["verdict"] is None]
    if missing:
        raise SystemExit(f"local_volume: {year}'s volume test flags {missing}, which no ruling answers (VERDICTS)")
    for m in contests:
        ch = COUNTY_HOLDS.get((year, m["state"]))
        if ch and set(ch[0]) & set(m.get("counties") or []) and (m.get("state_votes") or {}).get("source") != "id_sos":
            m["volume_gate"] = {"held": f"{ch[2]} (data/local/check-volume.json; {ch[1]}); p not computed",
                                "note": None, "record": {"verdict": "hold_counties", "counties_held": ch[0],
                                                         "check": "data/local/check-volume.json", "by": ch[1]}}
            continue
        f = c["flags"].get(m["state"])
        if not f or f["verdict"] in ("settled", "no_records"):
            continue
        kind = f["verdict"]
        text = words(year, m["state"])
        rec = {"verdict": kind, "check": "data/local/check-volume.json", "by": f["by"]}
        if kind == "hold":
            m["volume_gate"] = {"held": text + "; p not computed", "note": None, "record": rec}
        elif kind == "hold_counties":
            bad = set(f["settlement"]["counties"])
            inside = sorted(bad & set(m.get("counties") or []))
            rec["counties_held"] = sorted(bad)
            if inside:
                m["volume_gate"] = {"held": text + "; p not computed", "note": None, "record": rec}
            else:
                m["volume_gate"] = {"held": None, "note": text + "; this record's area lies outside it", "record": rec}
        elif kind in ("note", "held_already"):
            m["volume_gate"] = {"held": None, "note": text, "record": rec}
    return contests


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["check", "scan2016", "scan", "rows", "ballots"])
    ap.add_argument("--year", type=int)
    a = ap.parse_args()
    if a.cmd == "scan":
        scan(a.year)
    elif a.cmd == "rows":
        scan(a.year, collect=True)
    elif a.cmd == "ballots":
        ballots(a.year)
    elif a.cmd == "scan2016":
        d = scan_2016()
        print("2016 state file: governors in", sorted(d["gov"]), "; legislatures in", len(d["leg"]), "states")
    else:
        check()


if __name__ == "__main__":
    main()
