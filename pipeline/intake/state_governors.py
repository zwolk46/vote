"""pipeline/intake/state_governors.py: the most recent governor contests, from each state's own certified results.

Written 2026-11-07 by worker D2, on the orchestrator's word of 12:35 UTC: "please also add the governors no source you
read reaches: KY and MS 2023, and NJ and VA 2025. Take each from the state's own certified results (KY State Board of
Elections, MS Secretary of State, NJ Division of Elections, VA Department of Elections), by script." Reason (the
orchestrator): these are the most recent governor races on the record, and law 5 asks for every one true sources
allow. Cha, Kuriwaki and Snyder end in 2021 and Algara and Amlani in 2020, so these four are in neither.

The gate is the orchestrator's for Louisiana 2023 (2026-11-07 11:16), within the certifying source: (a) the result is
marked official or certified; (b) its parts (counties, or Virginia's counties and cities) add up to its total; (c) it
equals the state's own posted statewide result. A contest that fails any is written with the failure ("held") and no
result of it is used.

Refused, and not tried again or another way (the orchestrator, 12:40: "record them and try nothing else"):
  - Kentucky 2023. The State Board of Elections' 2023 results page answered curl with HTTP 403 and "The request is
    blocked." (the site's own firewall, not this system's proxy), 2026-11-07 12:39 UTC.
  - Mississippi 2023. The Secretary of State's page for the 2023 general election loads, but its results sit in a frame
    on sos.ms.gov itself, and that page answered curl with HTTP 403, Cloudflare's "Attention Required!" challenge,
    2026-11-07 12:39 UTC. The orchestrator (12:40): "MS's frame sits on sos.ms.gov itself, so it stays refused."
  These are written as REFUSED below and copied into each year's file; the script does not request them again. A later
  reader may try once by hand; a refusal is recorded, never routed round.

New Jersey 2025: the Division of Elections' "Official List" for governor, linked from its 2025 page as "Official
General Election Results: Governor", read with D3's pipeline/intake/nj_sos.py (links and parse, unchanged): one line
per candidate and county and a "Total" line per candidate. (a) the list is the Official List, dated on each page;
(b) each candidate's 21 county lines add up to its Total line; (c) the Total lines are the state's posted statewide
result. Also checked: each county's own copy on the same page ("<County> County General Election Results: Governor",
municipality by municipality, with a "Federal Overseas" line in some), whose lines must add up to its Total line,
and whose Total line must equal the four candidates' figures for that county in the statewide list, as a set (the
copy's column order is read from no header here). The list gives no write-in ("personal choice") votes.

Virginia 2025: the Department of Elections' results site, enr.elections.virginia.gov, which the Department's own page
(https://www.elections.virginia.gov/resultsreports/election-results/) names for "November 4, 2025 General and Special
Elections". The site's script reads the election from its API (/results/public/api/elections/<jurisdiction>/<election>
/data, and /data/ballot-item/<id> for one contest's breakdown by locality) and its reports from /cdn/results/
<jurisdiction id>/<file> [stated: the site's own scripts, main-*.js and its chunks, read 2026-11-07]. (a) the election
is marked "isOfficialResults": true; (b) the contest's 133 localities (Virginia's counties and independent cities) add
up, option by option, to its statewide count; (c) the statewide count is the site's own, the summary it posts. Also
checked: the site's "Election Results" report (a CSV, precinct by precinct), whose rows for each named candidate must
add up to the same count; its write-in cells are empty, so the write-ins are checked on (b) only.

Virginia since 18:27 UTC (worker D3, 2026-11-07, for the refit of the governors): the Department refused D3 at
18:27:48 UTC, and a refusal binds the whole agency (the orchestrator, 18:30), so the API files above are not requested
again. va_cached() reads the same contest from the election's "Media Export", which D3's pipeline/intake/va_elect.py
read at 18:24 UTC, before the refusal (the orchestrator, 18:30: Virginia's 2023 and 2025 counts come only from files
read before it), by the same gate: (a) the election's page is headed "OFFICIAL RESULTS"; (b) its 133 localities add up
to its statewide count; (c) the page shows that count. Its four figures equal those va() read at 12:46 UTC.

Run from the repository root:  python3 -I pipeline/intake/state_governors.py [2023 2025]
Writes $VOTE_CACHE/state_gov/normalized/governor-<year>.json: {"year", "contests": [{"state", "date", "title",
"candidates": [{"name", "party", "votes", "write_in"}], "total_votes", "parts", "source", "gate", "checks", "held"}],
"refused": [...]}.
"""
import collections
import csv
import json
import os
import re
import subprocess
import sys
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import fetch as F  # noqa: E402
import nj_sos as NJ  # noqa: E402

ROOT = os.path.join(F.CACHE, "state_gov")
NORM = os.path.join(ROOT, "normalized")
GATE_BY = "within the certifying source (no federal contest on the ballot)"
GATE_RULED = "the orchestrator, 2026-11-07 11:16 UTC (set for Louisiana 2023), applied to these on 12:35 UTC"

REFUSED = {
    2023: [
        {"state": "KY", "who": "Kentucky State Board of Elections",
         "url": "https://elect.ky.gov/results/2020-2029/Pages/2023.aspx", "when_utc": "2026-11-07T12:39Z",
         "answer": "HTTP 403, \"The request is blocked.\" (the site's own firewall)",
         "tried": "curl once; nothing else (no WebFetch, no other host)"},
        {"state": "MS", "who": "Mississippi Secretary of State",
         "url": "https://sos.ms.gov/elections/electionresults_aspx/elections_results_2023_generalG.aspx",
         "when_utc": "2026-11-07T12:39Z",
         "answer": "HTTP 403, Cloudflare's \"Attention Required!\" challenge; the page is the frame that "
                   "https://www.sos.ms.gov/elections-voting/election-results/2023/2023-general-election-results "
                   "(which loads) shows the results in",
         "tried": "curl once; nothing else (no WebFetch, no other host)"},
    ],
}

# ----------------------------------------------------------------------------- New Jersey
NJ_LICENCE = NJ.LICENCE
NJ_COUNTY_SLUG = {c: c.lower().replace(" ", "") for c in NJ.COUNTIES}


def _nj_county_copy(path):
    """(its count lines' columns summed, the Total line's numbers, the number of count lines) of one county's copy: a
    line per municipality, and a "Federal Overseas" line in the counties that print one."""
    txt = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True, check=True).stdout
    sums, total, n = None, None, 0
    for line in txt.splitlines():
        nums = re.findall(r"(?<![\w,])\d[\d,]*(?![\w,])", line)
        if re.match(r"^\s*Total\s", line):
            total = [int(x.replace(",", "")) for x in nums]
            continue
        head = line.strip()
        if not nums or not head or head[0].isdigit() or "NJDOE" in line:
            continue
        name = re.split(r"\s{2,}", head)[0]
        if not re.search(r"[A-Za-z]", name):
            continue
        row = [int(x.replace(",", "")) for x in nums]
        if sums is None:
            sums = [0] * len(row)
        if len(row) != len(sums):
            raise SystemExit(f"{path}: a municipality line with {len(row)} numbers, not {len(sums)}: {line!r}")
        sums = [a + b for a, b in zip(sums, row)]
        n += 1
    return sums, total, n


def nj(year):
    links = NJ.links(year)
    hit = [(h, t) for h, t in links if h.endswith(f"/{year}-official-general-results-governor.pdf")]
    if len(hit) != 1:
        raise SystemExit(f"NJ {year}: {len(hit)} links to the statewide governor list on the year page")
    href, text = hit[0]
    name = f"nj_sos/raw/{year}-official-general-results-governor.pdf"
    path = F.fetch(NJ.BASE + href.lstrip("/"), name)
    cs, listed = NJ.parse(path)
    gov = [c for c in cs if c["office"] == "Governor"]
    if len(gov) != 1:
        raise SystemExit(f"NJ {year}: {len(gov)} governor contests in the list")
    c = gov[0]
    txt = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True, check=True).stdout
    dated = sorted(set(re.findall(r"^(\d\d/\d\d/\d{4})\s+Official List", txt, re.M)))
    when = re.search(r"For GENERAL ELECTION (\d\d)/(\d\d)/(\d{4}) Election", txt)
    date = f"{when.group(3)}-{when.group(1)}-{when.group(2)}"
    counties_all = all(set(x["counties"]) == set(NJ.COUNTIES) for x in c["candidates"])
    parts_add_up = all(x["adds_up"] for x in c["candidates"]) and counties_all
    official = text.startswith("Official General Election Results") and bool(dated)
    # the county copies
    copies, copy_fail = {}, []
    for county in NJ.COUNTIES:
        slug = NJ_COUNTY_SLUG[county]
        h = [hh for hh, _ in links if hh.endswith(f"/{year}-official-general-results-governor-{slug}.pdf")]
        if len(h) != 1:
            copy_fail.append(f"{county}: {len(h)} links to its copy")
            continue
        cname = f"nj_sos/raw/{year}-official-general-results-governor-{slug}.pdf"
        cp = F.fetch(NJ.BASE + h[0].lstrip("/"), cname)
        sums, total, n = _nj_county_copy(cp)
        mine = sorted(x["counties"][county] for x in c["candidates"])
        ok_sum = sums == total
        ok_list = total is not None and sorted(total) == mine
        copies[county] = {"url": F.meta(cname)["url"], "read_utc": F.meta(cname)["read_utc"],
                          "sha256": F.meta(cname)["sha256"], "lines": n,
                          "lines_add_up": ok_sum, "total_equals_the_list": ok_list}
        if not ok_sum:
            copy_fail.append(f"{county}: its lines sum to {sums}, its Total line {total}")
        if not ok_list:
            copy_fail.append(f"{county}: its Total line {total} against the list's {mine}")
    held = []
    if not official:
        held.append("the list is not marked official")
    if not parts_add_up:
        held.append("a candidate's county lines do not add up to its Total line, or a county is missing")
    if copy_fail:
        held.append("the county copies do not agree: " + "; ".join(copy_fail))
    m = F.meta(name)
    cands = [{"name": x["name"], "party": x["party"], "votes": x["total"], "write_in": False} for x in c["candidates"]]
    return {
        "state": "NJ", "date": date, "title": "Governor", "candidates": cands,
        "total_votes": sum(x["votes"] for x in cands), "parts": {"kind": "counties", "n": len(NJ.COUNTIES)},
        "source": {"name": "New Jersey Division of Elections, Official List: Candidates for Governor, General Election "
                           f"{when.group(1)}/{when.group(2)}/{when.group(3)} (\"{text}\")",
                   "url": m["url"], "read_utc": m["read_utc"], "sha256": m["sha256"], "bytes": m["bytes"],
                   "via": NJ.PAGE.format(year=year), "licence": NJ_LICENCE,
                   "dated": dated, "candidates_on_last_page": listed},
        "gate": {"by": GATE_BY, "ruled": GATE_RULED,
                 "official": official,
                 "official_how": f"the Official List, dated {', '.join(dated)} on its pages, linked as \"{text}\"",
                 "parts_add_up": parts_add_up,
                 "parts_how": "each candidate's 21 county lines add up to its Total line",
                 "statewide_equal": "equal: the record is the statewide list's own Total lines",
                 "county_copies": copies},
        "checks": [{"against": "the 21 county copies on the Division's 2025 page", "differences": copy_fail}],
        "notes": ["the Official List gives no write-in (personal choice) votes; the total is the listed candidates'"],
        "held": "; ".join(held) or None,
    }


# ----------------------------------------------------------------------------- Virginia
VA_PAGE = "https://www.elections.virginia.gov/resultsreports/election-results/"
VA_SITE = "https://enr.elections.virginia.gov"
VA_LICENCE = "no licence printed; the Virginia Department of Elections' official election results, public records"
VA_ELECTION = {2025: ("Virginia", "2025-November-General")}


def _text(xs):
    return next((x["text"] for x in xs or [] if x["languageId"] == "en"), None)


def va(year):
    jur, eid = VA_ELECTION[year]
    pg = F.fetch(VA_PAGE, "va_elect/raw/election-results-page.html")
    with open(pg, encoding="utf-8", errors="replace") as f:
        named = f"{VA_SITE}/results/public/virginia/{eid}".lower() in f.read().lower()
    if not named:
        raise SystemExit(f"VA {year}: the Department's results page does not name {VA_SITE} for {eid}")
    dname = f"va_elect/raw/{eid}-data.json"
    d = json.load(open(F.fetch(f"{VA_SITE}/results/public/api/elections/{jur}/{eid}/data", dname)))
    e = d["election"]
    gov = [b for b in d["ballotItems"] if _text(b["name"]) == "Governor" and not b.get("parentId")]
    if len(gov) != 1:
        raise SystemExit(f"VA {year}: {len(gov)} statewide contests named Governor")
    g = gov[0]
    opts = g["summaryResults"]["ballotOptions"]
    state = {o["nativeId"]: o["voteCount"] for o in opts}
    bname = f"va_elect/raw/{eid}-data-governor.json"
    b = json.load(open(F.fetch(f"{VA_SITE}/results/public/api/elections/{jur}/{eid}/data/ballot-item/{g['id']}",
                               bname)))["ballotItemWithBreakdown"]
    loc = collections.Counter()
    for r in b["breakdownResults"]:
        for o in r["ballotOptions"]:
            loc[o["nativeId"]] += o["voteCount"]
    n_loc = len(b["breakdownResults"])
    parts_add_up = dict(loc) == state and n_loc == g["reportingStatus"]["totalUnits"] == \
        g["reportingStatus"]["reportingUnits"]
    # the precinct report
    rep = [r for c in e["publicReportCategories"] for r in c["reports"] if r["reportName"] == "Election Results"]
    if len(rep) != 1:
        raise SystemExit(f"VA {year}: {len(rep)} reports named Election Results")
    rname = f"va_elect/raw/{eid}-Election-Results.csv"
    rpath = F.fetch(f"{VA_SITE}/cdn/results/{e['jurisdictionId']}/{urllib.parse.quote(rep[0]['blobName'])}", rname)
    pre, blank = collections.Counter(), collections.Counter()
    with open(rpath, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if r["OfficeTitle"] != "Governor" or r["DistrictType"] != "state":
                continue
            if r["TOTAL_VOTES"] == "":
                blank[r["CandidateId"] or r["CandidateName"]] += 1
                continue
            pre[r["CandidateId"]] += int(r["TOTAL_VOTES"])
    named_ids = [o["nativeId"] for o in opts if not o["isWriteIn"]]
    report_equal = all(pre[i] == state[i] for i in named_ids) and set(pre) == set(named_ids)
    differences = [] if report_equal else [f"{i}: report {pre[i]:,}, statewide {state[i]:,}" for i in named_ids
                                           if pre[i] != state[i]]
    official = e["isOfficialResults"] is True
    held = []
    if not official:
        held.append("the election is not marked official")
    if not parts_add_up:
        held.append("its localities do not add up to its statewide count")
    if not report_equal:
        held.append("the precinct report differs from the statewide count: " + "; ".join(differences))
    if g["voteTotal"] != sum(state.values()):
        held.append(f"the site's vote total {g['voteTotal']:,} is not its options' sum {sum(state.values()):,}")
    dm, bm, rm = F.meta(dname), F.meta(bname), F.meta(rname)
    cands = [{"name": _text(o["name"]), "party": _text((o.get("party") or {}).get("name")),
              "votes": o["voteCount"], "write_in": bool(o["isWriteIn"])} for o in opts]
    return {
        "state": "VA", "date": e["electionDate"], "title": "Governor", "candidates": cands,
        "total_votes": g["voteTotal"], "parts": {"kind": "localities (counties and independent cities)", "n": n_loc},
        "source": {"name": f"Virginia Department of Elections, election results: {_text(e['name'])}, Governor (the "
                           f"results site's statewide count)",
                   "url": dm["url"], "read_utc": dm["read_utc"], "sha256": dm["sha256"], "bytes": dm["bytes"],
                   "via": VA_PAGE, "licence": VA_LICENCE,
                   "published_utc": e["publishDate"], "as_of_utc": g["reportingStatus"]["asOf"]},
        "gate": {"by": GATE_BY, "ruled": GATE_RULED,
                 "official": official,
                 "official_how": f"the election is marked \"isOfficialResults\": true on the results site (published "
                                 f"{e['publishDate'][:16]}Z; {g['reportingStatus']['reportingUnits']} of "
                                 f"{g['reportingStatus']['totalUnits']} localities reporting)",
                 "parts_add_up": parts_add_up,
                 "parts_how": f"the contest's {n_loc} localities ({bm['url']}, read {bm['read_utc']}, sha256 "
                              f"{bm['sha256'][:16]}) add up, option by option, write-ins included, to the statewide "
                              f"count",
                 "statewide_equal": "equal: the record is the site's own statewide count",
                 "precinct_report": {"url": rm["url"], "read_utc": rm["read_utc"], "sha256": rm["sha256"],
                                     "named_candidates_equal": report_equal,
                                     "write_in_cells_empty": sum(blank.values())}},
        "checks": [{"against": f"the site's Election Results report, precinct by precinct ({rm['url']}, read "
                               f"{rm['read_utc']}, sha256 {rm['sha256'][:16]}): the named candidates; its write-in "
                               f"cells are empty", "differences": differences}],
        "notes": [],
        "held": "; ".join(held) or None,
    }


VA_REFUSED_UTC = "2026-11-07T18:27:48Z"


def va_cached(year):
    """Virginia's governor from the Department's own files as read before it refused us (D3's
    pipeline/intake/va_elect.py cache: the "Media Export" of the election, read 18:24 UTC, with the page that heads it
    "OFFICIAL RESULTS"), by the same gate as va(). Written 2026-11-07 by worker D3 for the refit of the governors (the
    orchestrator, 19:49, item 2: "refetch D2's governor sources from the documented downloads D2 already used, with no
    new hosts"). Reason: the Department refused D3 at 18:27:48 UTC (apps.elections.virginia.gov, 403), and a refusal
    binds the whole agency (the orchestrator, 18:30), so va() is not run again; the orchestrator's standing rule of
    18:30 lets Virginia's 2023 and 2025 counts come from files read before the refusal. No request is made."""
    p = os.path.join(F.CACHE, "va_elect", "normalized", f"{year}-general.json")
    if not os.path.exists(p):
        raise SystemExit(f"VA {year}: {p} is missing: run pipeline/intake/va_elect.py {year} (it reads its cache only)")
    with open(p) as f:
        d = json.load(f)
    gov = [c for c in d["contests"] if c["title"] == "Governor"]
    if len(gov) != 1:
        raise SystemExit(f"VA {year}: {len(gov)} contests named Governor in the export")
    g, ex = gov[0], d["files"]["export"]
    if not ex["finished_utc"] < VA_REFUSED_UTC:
        raise SystemExit(f"VA {year}: the export was read at {ex['finished_utc']}, not before the refusal")
    official = d["official"] is True
    parts_add_up = bool(g["parts_add_up"]) and not g["extra_in_localities"] and g["localities"] == 133
    page_equal = bool(g["page"]["shown"] and g["page"]["equal"])
    held = []
    if not official:
        held.append("the election is not headed OFFICIAL RESULTS")
    if not parts_add_up:
        held.append("its localities do not add up to its statewide count")
    if not page_equal:
        held.append("the results page does not show the export's statewide count")
    if g["statewide_total"] != sum(o["votes"] for o in g["options"]):
        held.append("the statewide total is not its options' sum")
    cands = [{"name": o["name"], "party": o["party"], "votes": o["votes"], "write_in": bool(o["write_in"])}
             for o in g["options"]]
    return {
        "state": "VA", "date": d["date"], "title": "Governor", "candidates": cands,
        "total_votes": g["statewide_total"],
        "parts": {"kind": "localities (counties and independent cities)", "n": g["localities"]},
        "source": {"name": f"Virginia Department of Elections, election results: {d['name']}, Governor (the results "
                           f"site's Media Export, read before the Department refused us)",
                   "url": ex["url"], "read_utc": ex["read_utc"], "sha256": ex["sha256"], "bytes": ex["bytes"],
                   "via": VA_PAGE, "licence": VA_LICENCE, "export_created_utc": d.get("export_created_utc"),
                   "cache": "va_elect/normalized (pipeline/intake/va_elect.py)"},
        "gate": {"by": GATE_BY, "ruled": GATE_RULED,
                 "official": official,
                 "official_how": f"the election's page is headed \"{d['official_text']}\" (rendered "
                                 f"{d['files']['election']['finished_utc']})",
                 "parts_add_up": parts_add_up,
                 "parts_how": f"the contest's {g['localities']} localities in the export add up, option by option, "
                              f"write-ins included, to its statewide count",
                 "statewide_equal": "equal: the export's statewide count, which the results page shows "
                                    f"(localities reporting {g['page']['localities_reporting']})"},
        "checks": [{"against": "the results page's own statewide count for the contest", "differences":
                    [] if page_equal else ["the page's count differs or is not shown"]}],
        "notes": ["read from the Media Export cached before the Department's refusal of 18:27:48 UTC; the API files "
                  "va() reads were not requested again"],
        "held": "; ".join(held) or None,
    }


# Virginia from the cached export (va_cached), not the API (va): the Department refused at 18:27:48 UTC (above)
READERS = {2025: [nj, va_cached]}


def governors(year):
    out = {"year": year, "contests": [], "refused": REFUSED.get(year, [])}
    for read in READERS.get(year, []):
        out["contests"].append(read(year))
    os.makedirs(NORM, exist_ok=True)
    with open(os.path.join(NORM, f"governor-{year}.json"), "w") as f:
        json.dump(out, f, indent=1)
    return out


def main(argv):
    for y in [int(a) for a in argv] or [2023, 2025]:
        o = governors(y)
        for c in o["contests"]:
            g = c["gate"]
            print(f"{y} {c['state']} {c['date']}: " + ", ".join(f"{x['name']} {x['votes']:,}" for x in c["candidates"])
                  + f"; total {c['total_votes']:,} over {c['parts']['n']} {c['parts']['kind']}; official "
                  f"{g['official']}; parts add up {g['parts_add_up']}; held {c['held']}")
            for ch in c["checks"]:
                print(f"   check: {ch['against'][:90]}: {ch['differences'] or 'no difference'}")
        for r in o["refused"]:
            print(f"{y} {r['state']}: refused, {r['answer'][:60]} ({r['when_utc']})")


if __name__ == "__main__":
    main(sys.argv[1:])
