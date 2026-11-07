"""pipeline/local_nj.py: New Jersey's official 2024 results (pipeline/intake/nj_sos.py) against the certified federal
counts, and MEDSL's 2024 New Jersey file against them, county by county.

Written 2026-11-07 by worker D3 (briefs/D3-data-local.md, step 2) at the orchestrator's orders of 08:08 ("For the 2024
legislatures of IN, LA and NJ, read each state's own certified results where a file is reachable by script, with a
gate against D2's federal counts on the same dates as for North Carolina") and 10:35 ("NJ 2024 as ordered ... its 2024
file holds local contests and any legislative specials; read what is there").

What is there [measured: the Division of Elections' 2024 page, links outside its HTML comments]: official general
results for president, US Senate and US House, each as a list by county; the special election of NJ-10 (federal); the
party primaries' federal offices and delegates. New Jersey elects its legislature in odd years, and the page lists no
legislative special. Its county, municipal and school board results are not on it: the county clerks hold them.

Why the county comparison: MEDSL's 2024 New Jersey file is 14.4% over D1's certified presidential count, so its New
Jersey contests are held back (data/local/REPORT.md section 6). The state's lists give each county's certified count,
so they show which counties' MEDSL counts add up, office by office. They cannot gate a local contest: they hold no local
office, and a county's federal counts adding up does not show that its other offices' rows do.

  gate()    the state's lists' Democratic and Republican votes against D1's president, D2's Senate and D2's House
            districts: (worst relative miss, words).
  check()   the gate, and MEDSL's Democratic and Republican candidates by county (president, Senate, each House
            district's part of the county) against the state's: data/local/check-nj.json. Candidates are matched by
            surname, since MEDSL leaves the party empty in some counties' rows. The line is local_medsl.QUALITY_LINE.

Run:  VOTE_CACHE=/tmp/vote-cache python3 -I pipeline/local_nj.py check
"""
import argparse
import collections
import csv
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fetch as F  # noqa: E402
from intake import nj_sos as SOS  # noqa: E402
import local as L  # noqa: E402
import local_medsl as LM  # noqa: E402

YEAR = 2024
MEDSL_FILE = os.path.join("medsl", "raw", "2024-13731174-2024-nj-precinct-general.csv")
OFFICES = {"President": ("president", "US PRESIDENT"), "US Senate": ("senate", "US SENATE"),
           "House of Representatives": ("house", "US HOUSE")}
SUFFIX = {"JR", "SR", "II", "III", "IV"}


def load():
    path = os.path.join(SOS.NORM, f"{YEAR}-general.json")
    if not os.path.exists(path):
        raise SystemExit(f"{path} is missing: run pipeline/intake/nj_sos.py read --year {YEAR}")
    with open(path) as f:
        return json.load(f)


def _side(x):
    s = " ".join(x.get("slogans") or [x.get("party", "")]).upper()
    return "D" if s.startswith("DEMOCRATIC") else "R" if s.startswith("REPUBLICAN") else None


def _cert_side(party):
    p = (party or "").upper()
    return "D" if p.startswith("DEMOCRAT") else "R" if p.startswith("REPUBLICAN") else None


def _surname(name):
    w = [x for x in re.sub(r"[^A-Z ]", " ", name.upper()).split() if x not in SUFFIX]
    return w[-1] if w else ""


def gate(st=None):
    st = st or load()
    worst, what = 0.0, []
    for office, (level, _) in OFFICES.items():
        mine = [c for c in st["contests"] if c["office"] == office]
        with open(os.path.join(L.REPO, "data", level, f"{YEAR}.json")) as f:
            cert = [x for x in json.load(f)["contests"] if x["place"]["state"] == "NJ" and not x.get("special")]
        if level == "house":
            byd = {int(x["place"]["district"]): x for x in cert}
            pairs = [(c, byd[c["district"]]) for c in mine if c["district"] in byd]
        else:
            pairs = [(mine[0], cert[0])] if mine and cert else []
        for side in ("D", "R"):
            a = b = 0
            for c, k in pairs:
                aa = sum(x["total"] or 0 for x in c["candidates"] if _side(x) == side)
                bb = sum(x["votes"] for x in k["result"]["candidates"] if _cert_side(x.get("party")) == side)
                if bb:
                    worst = max(worst, abs(aa - bb) / bb)
                a, b = a + aa, b + bb
            what.append(f"{level} {side} {a:,} against {b:,}" + (f" ({len(pairs)} districts)" if level == "house" else ""))
    return worst, "; ".join(what)


FIPS = {}   # county name -> FIPS code, from the file's county_name and county_fips columns (medsl_by_county)


def medsl_by_county():
    """{(office, district or None, county, surname): votes} from MEDSL's file, every mode added up."""
    from intake import medsl_precinct as MP
    out = collections.Counter()
    path = os.path.join(F.CACHE, MEDSL_FILE)
    want = {v[1]: k for k, v in OFFICES.items()}
    with open(path, newline="", encoding="utf-8", errors="replace") as f:
        for r in csv.DictReader(f):
            if r["county_name"] in SOS.COUNTIES and r["county_fips"]:
                FIPS.setdefault(r["county_name"], MP.fips5(r["county_fips"]))
            if r["office"] in want:
                d = int(r["district"]) if want[r["office"]] == "House of Representatives" else None
                out[(want[r["office"]], d, r["county_name"], _surname(r["candidate"]))] += int(float(r["votes"] or 0))
    return out


FEDERAL = ("US PRESIDENT", "US SENATE", "US HOUSE")
TOTAL_ROW = re.compile(r"\bTOTAL\b", re.I)


def _resolve(modes):
    """One precinct's votes for one candidate, as the intake reads them: its TOTAL row where it has one, else the sum of
    its modes (pipeline/intake/medsl_precinct.py resolve)."""
    return modes["TOTAL"] if "TOTAL" in modes else sum(modes.values())


def medsl_rows():
    """MEDSL's New Jersey rows, read once: ({(office, district, magnitude): {precinct key: {candidate: {mode: votes}}}},
    {precinct key: the most votes cast there for one federal office}, {row key: times it appears})."""
    from intake import medsl_precinct as MP
    rows = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(dict)))
    fed = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(dict)))
    seen = collections.Counter()
    with open(os.path.join(F.CACHE, MEDSL_FILE), newline="", encoding="utf-8", errors="replace") as f:
        for r in csv.DictReader(f):
            cand = (r["candidate"] or "").strip()
            if MP.is_meta(cand) or r.get("stage", "GEN") != "GEN":
                continue
            pk = (MP.fips5(r["county_fips"]), r["jurisdiction_fips"], r["precinct"])
            mode = (r["mode"] or "TOTAL").upper()
            try:
                v = int(float(r["votes"]))
            except ValueError:
                v = 0
            seen[(r["office"], r["district"], r["magnitude"]) + pk + (cand, mode)] += 1
            if r["office"] in FEDERAL:
                cell = fed[pk][(r["office"], r["district"])]
            elif r["dataverse"] == "LOCAL":
                mag = r["magnitude"]
                try:
                    mag = int(float(mag))
                except ValueError:
                    mag = None
                cell = rows[(r["office"], r["district"], mag)][pk]
            else:
                continue
            cell[cand][mode] = cell[cand].get(mode, 0) + v
    most = {pk: max(sum(_resolve(m) for m in cands.values()) for cands in offices.values())
            for pk, offices in fed.items()}
    return rows, most, seen


def row_checks(contests, rows=None, most=None, seen=None):
    """For each of MEDSL's New Jersey contests (the intake's normalized ones), the orchestrator's checks of 10:45 on its
    rows: (a) a row repeated for the same precinct, office, candidate and mode; (b) a precinct line that is a total,
    named so or equal for every candidate to all the contest's other precincts added up (Gloucester's presidential
    failure: a "COUNTY TOTAL" line beside its municipalities); (c) a precinct whose votes in the contest exceed the most
    it cast for one federal office times the contest's vote-for-N (the number of candidates on the ballot where MEDSL
    gives no vote-for-N). Returns [reasons] for each contest, in order: empty where none applies."""
    from intake import medsl_precinct as MP
    if rows is None:
        rows, most, seen = medsl_rows()
    out = []
    for c in contests:
        names = {x["name"] for x in c["candidates"]}
        prec = {pk: {n: m for n, m in cands.items() if n in names}
                for pk, cands in rows.get((c["office"], c["district"], c["magnitude"]), {}).items()
                if pk[0] in c["counties"]}
        prec = {pk: v for pk, v in prec.items() if v}
        why = [] if prec else ["its rows are not found in the file"]
        rep = sum(1 for pk, cands in prec.items() for n, modes in cands.items() for mode in modes
                  if seen[(c["office"], c["district"], "" if c["magnitude"] is None else str(c["magnitude"]))
                          + pk + (n, mode)] > 1)
        if rep:
            why.append(f"{rep} of its rows repeat for the same precinct, office, candidate and mode")
        tot = {n: sum(_resolve(cands[n]) for cands in prec.values() if n in cands) for n in names}
        for pk, cands in prec.items():
            vs = {n: _resolve(m) for n, m in cands.items()}
            if TOTAL_ROW.search(pk[2]) or (len(prec) > 1 and any(tot.values()) and
                                           all(2 * vs.get(n, 0) == tot[n] for n in names if tot[n])):
                why.append(f"precinct '{pk[2]}' is a total line beside the precincts it adds up")
                break
        n_ = c["magnitude"] or sum(1 for x in c["candidates"] if not MP.is_generic(x["name"]))
        over = [pk for pk, cands in prec.items()
                if sum(_resolve(m) for m in cands.values()) > most.get(pk, 0) * max(n_, 1)]
        if over:
            why.append(f"{len(over)} of its {len(prec)} precincts count more votes than the most they cast for one "
                       f"federal office times {n_} (e.g. '{over[0][2]}')")
        out.append(why)
    return out


def county_misses(st=None, med=None):
    """{county: {office: worst relative miss of MEDSL's D and R candidates against the state's list}}."""
    st = st or load()
    med = med if med is not None else medsl_by_county()
    out = collections.defaultdict(lambda: {"president": None, "senate": None, "house": None})
    for c in st["contests"]:
        lv = OFFICES[c["office"]][0]
        for x in c["candidates"]:
            if _side(x) is None:
                continue
            for county, v in x["counties"].items():
                m = med.get((c["office"], c["district"], county, _surname(x["name"])), 0)
                off = abs(m - v) / v if v else 0.0
                out[county][lv] = max(out[county][lv] or 0.0, off)
    return dict(out)


# The orchestrator's ruling of 2026-11-07 10:45, its fourth part: "Compare a sample of 5 released contests from 5
# different counties with the county clerk's own posted official results, where the clerk's site answers; record
# refusals, don't route round them. If any of the 5 misses by more than 0.5%, hold that county." Reason given: the law's
# rule for a compilation is that its figures are checked against their origins where a reader would ask.
# The sample, fixed before any count was compared: the five released counties whose clerk's site answered with its
# official 2024 general-election results (read 2026-11-07 after 10:45 UTC), and in each its board of county
# commissioners, the one county office on every ballot there, so that the contest runs through every precinct the
# county files. `label` is the words the file prints to say what it is [measured: each file].
CLERKS = [
    dict(county="CAMDEN", office="CAMDEN MEMBERS OF THE BOARD OF COUNTY COMMISSIONERS", form="summary",
         title="Members of the Board of County Commissioners", label="OFFICIAL RESULTS",
         url="https://camdencounty.com/wp-content/elections/general2024/2024_General_Election_Canvasser.pdf",
         name="nj_clerks/raw/camden-2024-general-canvasser.pdf"),
    dict(county="HUNTERDON", office="HUNTERDON BOARD OF COUNTY COMMISSIONERS", form="table",
         title="BOARD OF COUNTY COMMISSIONERS", label="OFFICIAL RESULTS",
         url="https://www.co.hunterdon.nj.us/DocumentCenter/View/15968/G2024-Official-Elections-Results-PDF",
         name="nj_clerks/raw/hunterdon-2024-general-official.pdf"),
    dict(county="MORRIS", office="MORRIS BOARD OF COUNTY COMMISSIONERS", form="summary",
         title="BOARD OF COUNTY COMMISSIONERS", label="OFFICIAL RESULTS",
         url="https://www.morriscountyclerk.org/files/sharedassets/clerk/v/6/elections/past-results/"
             "2024-general-summary-report-official.pdf",
         name="nj_clerks/raw/morris-2024-general-summary-official.pdf"),
    dict(county="OCEAN", office="MEMBER OF THE BOARD OF COMMISSIONERS", form="canvass",
         title="MEMBER OF THE BOARD OF COMMISSIONERS (3 YR TERM)", label="Ocean County Board of Canvassers Report",
         url="http://www.co.ocean.nj.us//WebContentFiles//bfb4b48c-439f-43b6-8cb1-32fce6d673b8.pdf",
         name="nj_clerks/raw/ocean-2024-general-canvass.pdf"),
    dict(county="SUSSEX", office="SUSSEX COUNTY COMMISSIONER", form="summary", title="COUNTY COMMISSIONER",
         label="OFFICIAL RESULTS",
         url="https://www.sussexcountyclerk.org/DocumentCenter/View/3051/Official-Election-Results-Countywide-Summary-PDF",
         name="nj_clerks/raw/sussex-2024-general-official-summary.pdf"),
]
# What the other released counties' clerks' sites gave, 2026-11-07 after 10:45 UTC [measured]: recorded, not routed
# round. The five held counties (Atlantic, Bergen, Gloucester, Mercer, Union) were not tried: they are held already.
CLERKS_NOT_READ = {
    "BURLINGTON": "the county's pages answered, but those read did not lead to its 2024 official results",
    "CAPE MAY": "the county's pages answered, but those read did not lead to its 2024 official results",
    "CUMBERLAND": "the clerk's 2024 summary report answered, but the file heads itself 'Unoffical' (sic), so it is not "
                  "the official results",
    "ESSEX": "the clerk's results page answered; its results host (Clarity) refused with HTTP 403",
    "HUDSON": "the clerk's site answered HTTP 202 with an empty body",
    "MIDDLESEX": "refused: HTTP 403 ('Access Denied')",
    "MONMOUTH": "the clerk's site answered HTTP 202 with an empty body",
    "PASSAIC": "refused: HTTP 403",
    "SALEM": "a bot challenge page ('One moment, please...')",
    "SOMERSET": "refused: HTTP 403 ('Access Denied')",
    "WARREN": "refused: HTTP 403",
}
CLERKS_REFUSED_TOO = {   # within the five read
    "HUNTERDON": "its results by municipality: connection reset (its results by district answered, and are read)",
    "SUSSEX": "sussexcountynj.gov: the proxy's HTTP 502 (the clerk's own site, sussexcountyclerk.org, answered, and is "
              "read)",
}
NUM = re.compile(r"\d[\d,]*")
SPOT = {}   # the last spotcheck, as county_gate used it


def _key(name):
    from intake import medsl_precinct as MP
    s = re.sub(r"\((?:[A-Z]{1,4})\)", " ", name)
    s = re.sub(r"^\s*(?:DEM|REP|IND|LIB|GRN|CON)\s+", "", s)
    return "WRITE-IN" if MP.is_generic(s) or re.match(r"\s*write-?in", s, re.I) else _surname(s)


def _clerk_counts(spec, txt, keys):
    """{surname or WRITE-IN: votes} for the contest titled spec["title"] in the clerk's file, read three ways:
    summary  a "Summary Results Report": the title line at the margin (Camden's file repeats it, indented, over each
             precinct's page), then a line per candidate whose first number is its total;
    canvass  Ocean's report by municipality: the title once per municipality, a line per candidate ending in
             "votes percent%", added up over the municipalities;
    table    Hunterdon's results by district: the title over a table whose columns are named by rotated headers;
             the "Totals" row, its numbers taken in the order of the contest's own headers (`keys`)."""
    out = collections.Counter()
    lines = txt.splitlines()
    if spec["form"] == "summary":
        at = [i for i, l in enumerate(lines) if l.rstrip() == spec["title"]]   # at the margin: the county's summary
        if len(at) != 1:
            raise ValueError(f"{spec['county']}: the title is found {len(at)} times")
        started = False
        for l in lines[at[0] + 1:]:
            if l.startswith("Total Votes Cast") or (started and not l.strip()):
                break
            m = re.match(r"^(\S.*?)\s{2,}(\d[\d,]*)\b", l)
            if m and not m.group(1).startswith(("Vote For", "No Nomination")):
                out[_key(m.group(1))] += int(m.group(2).replace(",", ""))
                started = True
    elif spec["form"] == "canvass":
        inside = False
        for l in lines:
            if spec["label"] in l:
                inside = False
            elif l.strip() == spec["title"]:
                inside, out["__sections__"] = True, out["__sections__"] + 1
            elif inside:
                m = re.match(r"^\s+(.+?)\s{2,}(\d+)\s+[\d.]+%\s*$", l)
                if m:
                    out[_key(m.group(1))] += int(m.group(2))
    else:
        for page in txt.split("\f"):
            pl = page.splitlines()
            if not any(spec["title"] in l for l in pl[:8]):
                continue
            pos = {}
            for l in pl:
                for k in keys:
                    w = "Write-in Totals" if k == "WRITE-IN" else k
                    if k not in pos and re.search(rf"\b{re.escape(w)}\b", l, re.I):
                        pos[k] = re.search(rf"\b{re.escape(w)}\b", l, re.I).start()
            tot = [l for l in pl if re.match(r"^Totals\s", l)]
            if tot:
                if len(pos) != len(keys):
                    raise ValueError(f"{spec['county']}: headers found for {sorted(pos)}, not {sorted(keys)}")
                nums = [int(x.replace(",", "")) for x in NUM.findall(tot[0])]
                for k, v in zip(sorted(pos, key=pos.get), nums):
                    out[k] = v
    return out


def spotcheck(contests):
    """The ruling's fourth part: each CLERKS contest's candidates in the source (as built, `contests`) against the
    clerk's official file, by surname: {county: {"office", "file", "worst_miss", "misses": {surname: [source, clerk]},
    "holds": bool}} and, for a file not read, {"refused": why}."""
    import subprocess
    out = {}
    for spec in CLERKS:
        try:
            path = F.fetch(spec["url"], spec["name"])
        except F.Refused as e:
            out[spec["county"]] = {"office": spec["office"], "refused": str(e)}
            continue
        txt = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True, check=True).stdout
        fips = FIPS.get(spec["county"])
        mine = [c for c in contests if c["state"] == "NJ" and c["office"] == spec["office"] and c["counties"] == [fips]]
        if len(mine) != 1 or spec["label"] not in txt:
            raise SystemExit(f"{spec['county']}: {len(mine)} contests named {spec['office']}, or the file lacks "
                             f"'{spec['label']}'")
        src = collections.Counter()
        for x in mine[0]["candidates"]:
            src[_key(x["name"])] += x["votes"]
        clerk = _clerk_counts(spec, txt, list(src))
        sections = clerk.pop("__sections__", None)
        misses = {k: [src.get(k, 0), clerk.get(k, 0)] for k in sorted(set(src) | set(clerk))}
        worst = max(abs(a - b) / b if b else (1.0 if a else 0.0) for a, b in misses.values())
        m = F.meta(spec["name"])
        out[spec["county"]] = {"office": spec["office"], "file": spec["url"], "read_utc": m.get("read_utc"),
                               "sha256": m.get("sha256"), "label": spec["label"], "form": spec["form"],
                               "municipal_sections": sections, "misses": misses, "worst_miss": round(worst, 6),
                               "holds": worst > LM.QUALITY_LINE}
    return out


def county_gate(contests, year):
    """The orchestrator's ruling of 2026-11-07 10:45: MEDSL's New Jersey contests of 2024 are no longer held back as a
    state, but county by county. A contest is released, with its routes, when every county it lies in adds up in all
    three federal offices at local_medsl.QUALITY_LINE (county_misses) and its rows pass row_checks. Each New Jersey
    contest of `year` gets `county_gate`: {"held": the reason or None, "record": the record's `gate` field}. Reason:
    the statewide miss comes from five counties, and the row checks test the failure seen in Gloucester."""
    nj = [c for c in contests if c["state"] == "NJ"]
    if year != YEAR or not nj:
        return contests
    misses = county_misses()   # fills FIPS
    if sorted(FIPS) != sorted(SOS.COUNTIES):
        raise SystemExit(f"MEDSL's New Jersey file names other counties than the state's 21: {sorted(FIPS)}")
    NAME = {v: k.title() for k, v in FIPS.items()}
    ok = {FIPS[k] for k, v in misses.items() if all(x is not None and x <= LM.QUALITY_LINE for x in v.values())}
    SPOT.clear()
    SPOT.update(spotcheck(nj))
    clerk_held = {FIPS[k]: v for k, v in SPOT.items() if v.get("holds")}
    whys = row_checks(nj)
    for c, why in zip(nj, whys):
        cs = c["counties"]
        out_ = [x for x in cs if x not in ok]
        rec = {"by": "county", "line": LM.QUALITY_LINE, "check": "data/local/check-nj.json",
               "counties": {x: {k: (None if v is None else round(v, 4)) for k, v in misses.get(
                   NAME[x].upper(), {}).items()} for x in cs},
               "row_checks": why or "passed"}
        spot = [v for k, v in SPOT.items() if v.get("office") == c["office"] and [FIPS[k]] == cs and "misses" in v]
        if spot:
            rec["clerk_check"] = {k: spot[0][k] for k in ("file", "sha256", "worst_miss")}
        if out_:
            worst = max((v for x in out_ for v in misses.get(NAME[x].upper(), {}).values() if v is not None),
                        default=None)
            held = (f"the source's {year} counts for {', '.join(NAME[x] for x in out_)} County do not add up to the "
                    f"certified federal counts there (president, Senate and House, by county"
                    + (f"; off by up to {100 * worst:.1f}%" if worst is not None else "") +
                    "; pipeline/local_nj.py), so its counts for this contest may be incomplete or double-counted; "
                    "p not computed")
        elif any(x in clerk_held for x in cs):
            x = next(x for x in cs if x in clerk_held)
            held = (f"the county clerk's official {year} count for {NAME[x]} County's {clerk_held[x]['office'].lower()} "
                    f"differs from the source's by {100 * clerk_held[x]['worst_miss']:.1f}% (pipeline/local_nj.py "
                    "spotcheck), so the source's counts there may be unsound; p not computed")
        elif why:
            held = "its rows fail the county gate's checks (" + "; ".join(why) + "); p not computed"
        else:
            held = None
        rec["released"] = held is None
        c["county_gate"] = {"held": held, "record": rec}
    return contests


def check():
    st = load()
    worst, words = gate(st)
    med = medsl_by_county()
    by_county = collections.defaultdict(dict)
    for c in st["contests"]:
        for x in c["candidates"]:
            side = _side(x)
            if side is None:
                continue
            for county, v in x["counties"].items():
                m = med.get((c["office"], c["district"], county, _surname(x["name"])), 0)
                k = OFFICES[c["office"]][0] + (f" {c['district']}" if c["district"] else "")
                by_county[county][f"{k} {side}"] = {"medsl": m, "state": v, "off": round((m - v) / v, 4) if v else None}
    out = {}
    for county in SOS.COUNTIES:
        t = by_county[county]
        worst_of = {lv: max((abs(r["off"]) for k, r in t.items() if k.startswith(lv) and r["off"] is not None),
                            default=None) for lv in ("president", "senate", "house")}
        out[county] = {"worst_off": worst_of,
                       "adds_up": {lv: (w is not None and w <= LM.QUALITY_LINE) for lv, w in worst_of.items()},
                       "lines": dict(sorted(t.items()))}
    every = [c for c, r in out.items() if all(r["adds_up"].values())]
    split = [c for c, r in out.items() if len(set(r["adds_up"].values())) > 1]
    res = {"about": "New Jersey's official 2024 general-election lists (pipeline/intake/nj_sos.py) against D1's and "
                    "D2's certified counts, and MEDSL's 2024 New Jersey file against the lists by county. Built by "
                    "pipeline/local_nj.py check.",
           "state_page": st["page"],
           "state_files": {k: {x: v[x] for x in ("url", "read_utc", "sha256", "link_text", "contests", "candidates",
                                                 "all_add_up")} for k, v in st["files"].items()},
           "what_the_state_page_holds": "official general results for president, US Senate and US House by county; "
                                        "NJ-10's special election; the primaries' federal offices and delegates. No "
                                        "legislative contest and no county, municipal or school board contest.",
           "gate": {"worst_miss": round(worst, 6), "fails": worst > LM.QUALITY_LINE, "counts": words},
           "medsl_by_county": {"line": LM.QUALITY_LINE,
                               "counties_adding_up_in_every_federal_office": every,
                               "counties_adding_up_in_some_federal_offices_only": split,
                               "counties": out}}
    res["county_gate"] = gate_summary()
    path = os.path.join(L.REPO, "data", "local", "check-nj.json")
    with open(path, "w") as f:
        json.dump(res, f, indent=1)
    return res


def gate_summary():
    """What county_gate did to MEDSL's 2024 New Jersey contests, as the build reads them (local_medsl.load)."""
    import local_nj as NJ   # the module local_medsl's build uses: run as a script, this file is __main__
    cs = [c for c in LM.load(YEAR) if c["state"] == "NJ"]
    why = collections.Counter()
    by_rows = []
    for c in cs:
        h = c["county_gate"]["held"]
        kind = "questions" if c.get("question") else "offices"
        if h is None:
            why[f"released: {kind}"] += 1
        elif h.startswith("the source's"):
            why[f"held by county: {kind}"] += 1
        elif h.startswith("the county clerk's"):
            why[f"held by the clerk check: {kind}"] += 1
        else:
            why[f"held by the row checks: {kind}"] += 1
            by_rows.append({"office": c["office"], "district": c["district"], "counties": c["counties"],
                            "row_checks": c["county_gate"]["record"]["row_checks"]})
    rel = {NJ.FIPS[k]: k for k in NJ.FIPS}
    released = sorted({x for c in cs for x, m in c["county_gate"]["record"]["counties"].items()
                       if all(v is not None and v <= LM.QUALITY_LINE for v in m.values())})
    return {"ruling": "the orchestrator's of 2026-11-07 10:45",
            "line": LM.QUALITY_LINE,
            "released_counties": [rel[x] for x in released],
            "held_counties": sorted(set(SOS.COUNTIES) - {rel[x] for x in released}),
            "contests": dict(sorted(why.items())),
            "held_by_the_row_checks": by_rows,
            "clerk_check": NJ.SPOT,
            "clerks_not_read": CLERKS_NOT_READ,
            "refused_within_the_five_read": CLERKS_REFUSED_TOO}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("what", choices=["check"])
    ap.parse_args()
    res = check()
    print(json.dumps({k: res[k] for k in ("gate",)}, indent=1))
    m = res["medsl_by_county"]
    print("every office:", m["counties_adding_up_in_every_federal_office"])
    print("some only:", m["counties_adding_up_in_some_federal_offices_only"])
    g = res["county_gate"]
    print("county gate:", g["contests"], "| held counties:", g["held_counties"])
    print("clerk check:", {k: v.get("worst_miss", v.get("refused")) for k, v in g["clerk_check"].items()})
    for c, r in m["counties"].items():
        print(f"{c:12s}", {k: (None if v is None else round(v, 4)) for k, v in r["worst_off"].items()})


if __name__ == "__main__":
    main()
