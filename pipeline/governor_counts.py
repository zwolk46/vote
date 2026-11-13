"""pipeline/governor_counts.py: governors' counts: a fusion candidate's every party line, and the state's own count.

Written 2026-11-13 by worker D3 on the orchestrator's message of 04:44 UTC:
  "CT and NY 2018 governors: sum every line. A fusion candidate's votes are the sum of his lines in the official
  count, so one line understates both the candidate and n. List the moves."
  "IN 2024 governor: the certified count wins. "Certified: T" is the agency's own word in its own data, which 15:16
  accepts. A file name or URL is what it refuses. Take Braun 1,566,081 and McCormick 1,183,741, name the archive in the
  source, and list the move. D2 is done, so it is yours."
Reason (the orchestrator, 2026-11-07 18:54): "n enters p directly", so a count that is short moves p by the same
factor. M2 found all three (checks/M2-REPORT.md section 14.1, item 10); data/local/REPORT.md section 35 lists the moves.

The record's source, Cha, Kuriwaki and Snyder (Harvard Dataverse doi:10.7910/DVN/DGDRDT, v4.1), gives these three
contests as follows [measured]: Connecticut's and New York's 2018 nominees on their own party's line alone, and
Indiana's 2024 two nominees alone, at figures under the state's archive.

The sources (each read once, kept in $VOTE_CACHE with its .meta.json):
  Connecticut 2018  the Secretary of the State's Election History, the 2018 general's governor contest
                    (https://electionhistory.ct.gov/contest/3781, read 2026-11-13 04:49 UTC): each candidate's votes on
                    each line, the page's data as served. Lamont 694,510 (Democratic 676,649, Working Families 17,861);
                    Stefanowski 650,138 (Republican 624,750, Independent 25,388); Griebel 54,741; Hanscomb 6,086;
                    Greenstein 1,254; Whitnum, a write-in, 74; "Total Votes Cast" 1,406,803 [stated]. The page lists
                    the count under "Official Sources": "Statement of Vote 2018", page 7 [stated]. That is the mark
                    taken, the page's own words under 15:16 ("marks them certified or official"). It also says: "The
                    election from the original source document contained data entry errors that have been preserved"
                    and "There are discrepancies in precinct reporting in the Town of Woodstock" [stated]. Algara and
                    Amlani's county returns give Lamont 694,510 and Stefanowski 650,138, and MEDSL's precinct file
                    694,509 and 650,132, every line summed [measured].
  New York 2018     Algara and Amlani's county returns (Harvard Dataverse doi:10.7910/DVN/DGUMFI; the file D2's build
                    reads, pipeline/intake/algara_amlani.py), summed over the 62 counties, none missing: Cuomo 3,635,340
                    and Molinaro 2,207,602, each nominee's lines together [measured]. New York's State Board refused us
                    (2026-11-07 18:49), so its own count is not read, and MEDSL's 2018 file holds the governor in 57 of
                    the 62 counties (data/local/check-volume.json). That the authors' figures are every line is read
                    from Connecticut, where they equal the Secretary of the State's lines summed to the vote [inferred].
                    The other three candidates ran on one line each, and keep the dataset's figures.
  Indiana 2024      Indiana's results archive of the 2024 general (https://enr.indianavoters.in.gov/archive/2024General/,
                    read 2026-11-07 08:40 UTC by pipeline/intake/in_enr.py), whose settings say "Certified": "T":
                    Braun 1,566,081, McCormick 1,183,741, Rainwater 129,781 and Stried, a write-in, 52.

Added on the orchestrator's message of 05:26 UTC, on the fusion scan's second count (data/local/check-fusion.json):
  "Yes to the requests: one each to West Virginia (2012), Missouri (2008, 2012, 2016) and Utah (2008), for the state's
  certified governor count. Under 15:16, a count bearing the mark wins, so take it and list the move. A state that
  refuses or answers without the mark settles nothing on its own. Then the two-witness rule of 05:15 applies wherever
  it fits. Otherwise 19:04 applies." And: "Maine 2010: no request, since the SoS refused."
  West Virginia 2012  the Secretary of State's statewide results page of the 2012 general (apps.sos.wv.gov, read
                    2026-11-13 05:30 UTC), headed "Official Results" [stated]: Tomblin 335,468, Maloney 303,291,
                    Johnson 16,787, Moran 8,909, "Official Total Votes" 664,455. Cha's figures are 11% to 13% under
                    them; Algara and Amlani's agree [measured]. The page also says its pages "should not be relied on
                    as official results until certified" and that 1,846 of 1,892 precincts report; both are quoted in
                    the source's note.
  Utah 2008         the Lieutenant Governor's 2008 general workbook, which the historical election results page links
                    (read 2026-11-13 05:30 UTC), its Governor sheet's Total row: Huntsman 734,049, Springmeyer 186,503,
                    Schanze 24,820 and Doughton, a write-in, 153; total 945,525. The workbook bears no mark, so it
                    stands only as the second of two witnesses: Algara and Amlani's county returns agree with it within
                    TWO_AGREE for both nominees (05:15 (3)); Cha's figures are 5% to 6% under it [measured].
  Missouri 2008, 2012, 2016
                    the Secretary of State's official returns (read 2026-11-13 05:29 UTC), headed "Official Election
                    Returns ... As announced by the Board of State Canvassers" (2008, 2012) and "OFFICIAL RESULTS"
                    (2016) [stated]: equal to the record's two nominees to the vote [measured], so no figure moves; the
                    record gains a note. Algara and Amlani's county returns are the short count: in 2016 by Kansas
                    City's own rows of the state's file (Koster 98,336, Greitens 25,284) [measured].
  Maine 2010        no request. A note: Algara and Amlani give Mitchell, third, 5.5% over the record; the deciding pair
                    is LePage and Cutler, and p is not computed for the contest (ME_2010_NOTE).

What it does (run again, it changes nothing):
  fix_cha(contests)   the same counts in Cha's contests as D2's build reads them (pipeline/chambers.py _load,
                      pipeline/intake/build_congress.py cha_index): the nominees' votes and the contest's total, so that
                      every fit, back-test and last-race index takes them. It stops where a contest's figures are
                      neither the dataset's nor the fixed ones.
  main()              each record: its candidates' votes (Connecticut's with their lines, in `lines`), the candidates
                      the source names and the dataset leaves out (Connecticut's write-in; Indiana's Rainwater and
                      write-in), total_votes, the source, two_party, n (the two leaders' votes less one, as D2's build
                      sets it) and each p scaled to the new n (method "density": event = f_half / n), a note; and the
                      file's sources block. Then the last-race input of each later record whose last race is one of
                      these (Connecticut and New York 2022, West Virginia 2016, Utah's 2010 special), read again from
                      chambers.last_governor_index(); and the notes of Missouri's three and Maine 2010 (notes_only).
Then pipeline/d2_labels.py, and pipeline/chambers.py odd, backtest, compute and history, as for Hawaii 2018
(pipeline/governor_hi2018.py; data/local/REPORT.md section 30).

Run:  VOTE_CACHE=/tmp/vote-cache python3 -I pipeline/governor_counts.py
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fetch as F  # noqa: E402

REPO = os.path.dirname(HERE)
CT_PAGE = os.path.join(F.CACHE, "ct_sots", "contest-3781.html")
CT_URL = "https://electionhistory.ct.gov/contest/3781"
AA = os.path.join(F.CACHE, "algara_amlani", "normalized", "governors.json")
AA_FILE = os.path.join(F.CACHE, "algara_amlani", "dataverse_shareable_gubernatorial_county_returns_1865_2020.Rdata")
IN_ENR = os.path.join(F.CACHE, "in_enr", "normalized", "2024General.jsonl")
IN_CHECKS = os.path.join(F.CACHE, "in_enr", "normalized", "checks-2024General.json")
WV_PAGE = os.path.join(F.CACHE, "wv_sos", "raw", "results-2012-eid13-statewide.html")
UT_FILE = os.path.join(F.CACHE, "ut_lg", "raw", "2008Gen.xls")
MO_FILES = {2008: os.path.join(F.CACHE, "mo_sos", "raw", "AllRacesGeneralNovember2008.pdf"),
            2012: os.path.join(F.CACHE, "mo_sos", "raw", "2012GeneralElection.pdf"),
            2016: os.path.join(F.CACHE, "mo_sos", "raw", "ActualResults-November82016-GeneralElection.pdf")}
TWO_AGREE = 0.004   # the orchestrator, 2026-11-13 05:15 (3): two counts within 0.4% by candidate stand against one
TAG = "the count (pipeline/governor_counts.py): "
CHA_NOTE = "governors' totals here leave out candidates under ten votes"
NOTE_LAST = ("the last governor race's Democratic share ({state}) reads the count taken in pipeline/governor_counts.py "
             "(the orchestrator, 2026-11-13 04:44 and 05:26; data/local/REPORT.md section 35)")

# the record's candidates (Cha's names) and their figures: the dataset's, and the count taken here [measured]
FIX = {
    "2018-governor-CT": {
        "key": (2018, "CT"), "source_key": "ct_sots",
        "was": {"LAMONT, EDWARD M. (NED)": 676649, "STEFANOWSKI, BOB": 624750, "GRIEBEL, R. NELSON (OZ)": 54741,
                "HANSCOMB, RODNEY": 6086, "GREENSTEIN, MARK STEWART": 1254},
        "names": {"LAMONT, EDWARD M. (NED)": "Ned Lamont and Susan Bysiewicz",
                  "STEFANOWSKI, BOB": "Bob Stefanowski and Joe Markley",
                  "GRIEBEL, R. NELSON (OZ)": "Oz Griebel and Monty E. Frank",
                  "HANSCOMB, RODNEY": "Rodney Hanscomb and Jeffrey Thibeault",
                  "GREENSTEIN, MARK STEWART": "Mark Stewart Greenstein and John Demitrus"},
        "add": [("WHITNUM, LEE", "W-I", "Lee Whitnum and Jacey Wyatt")],
        "expect": {"Ned Lamont and Susan Bysiewicz": (694510, [("Democratic", 676649), ("Working Families", 17861)]),
                   "Bob Stefanowski and Joe Markley": (650138, [("Republican", 624750), ("Independent", 25388)]),
                   "Oz Griebel and Monty E. Frank": (54741, None), "Rodney Hanscomb and Jeffrey Thibeault": (6086, None),
                   "Mark Stewart Greenstein and John Demitrus": (1254, None),
                   "Lee Whitnum and Jacey Wyatt": (74, None)},
        "total": 1406803,
    },
    "2018-governor-NY": {
        "key": (2018, "NY"), "source_key": "algara_amlani",
        "was": {"CUOMO, ANDREW M.": 3424416, "MOLINARO, MARCUS J. (MARC)": 1926485, "HAWKINS, HOWIE": 103946,
                "SHARPE, LARRY": 95033, "MINER, STEPHANIE A.": 55441},
        "now": {"CUOMO, ANDREW M.": 3635340, "MOLINARO, MARCUS J. (MARC)": 2207602},
        "add": [],
    },
    "2012-governor-WV": {
        "key": (2012, "WV"), "source_key": "wv_sos",
        "was": {"TOMBLIN, EARL RAY": 297207, "MALONEY, WILLIAM (BILL)": 273130, "JOHNSON, JESSE CLARENCE, JR.": 15179,
                "MORAN, DAVID D. (DAVE)": 7934},
        "names": {"TOMBLIN, EARL RAY": "EARL RAY TOMBLIN", "MALONEY, WILLIAM (BILL)": "BILL MALONEY",
                  "JOHNSON, JESSE CLARENCE, JR.": "JESSE JOHNSON", "MORAN, DAVID D. (DAVE)": "DAVID MORAN"},
        "add": [],
        "expect": {"EARL RAY TOMBLIN": 335468, "BILL MALONEY": 303291, "JESSE JOHNSON": 16787, "DAVID MORAN": 8909},
        "total": 664455,
    },
    "2008-governor-UT": {
        "key": (2008, "UT"), "source_key": "ut_lg",
        "was": {"HUNTSMAN, JON M., JR.": 700565, "SPRINGMEYER, BOB": 175301, "SCHANZE, DELL (SUPERDELL)": 23449},
        "names": {"HUNTSMAN, JON M., JR.": 'Huntsman & Herbert "R"', "SPRINGMEYER, BOB": 'Springmeyer & Valdez "D"',
                  "SCHANZE, DELL (SUPERDELL)": 'Schanze & Hobbs "L"'},
        "add": [("DOUGHTON", "W-I", "Doughton (Write in)")],
        "expect": {'Huntsman & Herbert "R"': 734049, 'Springmeyer & Valdez "D"': 186503, 'Schanze & Hobbs "L"': 24820,
                   "Doughton (Write in)": 153},
        "total": 945525,
    },
    "2024-governor-IN": {
        "key": (2024, "IN"), "source_key": "in_enr",
        "was": {"BRAUN, MIKE": 1561279, "MCCORMICK, JENIFFER": 1179967},
        "names": {"BRAUN, MIKE": "Mike Braun & Micah Beckwith", "MCCORMICK, JENIFFER": "Jennifer G. McCormick & Terry Goodin"},
        "add": [("RAINWATER, DONALD", "Lbt", "Donald Rainwater & Tonya Hudson"),
                ("STRIED, CHRISTOPHER RYAN", "W-I", "Christopher Ryan Stried (W/I)")],
        "expect": {"Mike Braun & Micah Beckwith": 1566081, "Jennifer G. McCormick & Terry Goodin": 1183741,
                   "Donald Rainwater & Tonya Hudson": 129781, "Christopher Ryan Stried (W/I)": 52},
    },
}

NOTES = {
    "2018-governor-CT": (
        "the candidates' votes are the Connecticut Secretary of the State's count (its Election History, which lists "
        "the Statement of Vote 2018 under 'Official Sources'), each candidate's lines summed (in `lines`): Lamont "
        "694,510 (Democratic 676,649, Working Families 17,861), Stefanowski 650,138 (Republican 624,750, Independent "
        "25,388); the write-in Whitnum's 74 are added, so the total is the page's 'Total Votes Cast', 1,406,803. Cha, "
        "Kuriwaki and Snyder give each nominee's own party line alone (676,649 and 624,750). n and each p follow the "
        "lines summed, and so do D2's fits of later years and Connecticut 2022's last-governor-race input (the "
        "orchestrator, 2026-11-13 04:44: \"A fusion candidate's votes are the sum of his lines in the official "
        "count\"; data/local/REPORT.md section 35)"),
    "2018-governor-NY": (
        "Cuomo's and Molinaro's votes are each nominee's every party line, 3,635,340 and 2,207,602: Algara and "
        "Amlani's county returns summed over the 62 counties, none missing. Cha, Kuriwaki and Snyder give each "
        "nominee's own party line alone (3,424,416 and 1,926,485); the other three ran on one line each and keep "
        "their figures. New York's State Board refused us (2026-11-07 18:49), so its own count is not read; that "
        "the authors' figures are every line is read from Connecticut 2018, where they equal the Secretary of the "
        "State's lines summed to the vote [inferred]. n and each p follow the lines summed, and so do D2's fits of "
        "later years and New York 2022's last-governor-race input (the orchestrator, 2026-11-13 04:44; "
        "data/local/REPORT.md section 35)"),
    "2012-governor-WV": (
        "the candidates' votes are the West Virginia Secretary of State's count, its results page for the general of "
        "2012-11-06 headed '★★★ Official Results ★★★': Tomblin 335,468, Maloney 303,291, Johnson 16,787 and Moran "
        "8,909, 'Official Total Votes: 664,455' (the page adds that its results 'do not include write-in candidate "
        "information'). Cha, Kuriwaki and Snyder give 297,207, 273,130, 15,179 and 7,934, each 9.6% to 12.9% under it; "
        "Algara and Amlani's county returns give Tomblin 335,468 and Maloney 303,291, the state's figures to the vote "
        "[measured]. The count with the mark wins (the orchestrator, 2026-11-07 15:16; 2026-11-13 05:26: \"a count "
        "bearing the mark wins, so take it and list the move\"); n and each p follow it, and so do D2's fits of later "
        "years and West Virginia 2016's last-governor-race input (data/local/REPORT.md section 35)"),
    "2008-governor-UT": (
        "the candidates' votes are the Utah Lieutenant Governor's results of the 2008 general (the workbook its "
        "historical results page links as '2008 General', its Governor sheet's Total row): Huntsman 734,049, "
        "Springmeyer 186,503, Schanze 24,820 and the write-in Doughton's 153. The workbook bears no certified or "
        "official mark; Algara and Amlani's county returns give Huntsman 734,049 and Springmeyer 186,503, the "
        "state's figures to the vote, against Cha, Kuriwaki and Snyder's 700,565 and 175,301 [measured]. Two "
        "independent counts that agree by candidate stand against one (the orchestrator, 2026-11-13 05:15 (3) and "
        "05:26: \"Then the two-witness rule of 05:15 applies wherever it fits\"); n and each p follow them, and so "
        "do D2's fits of later years and the last-governor-race inputs that read 2008 (data/local/REPORT.md "
        "section 35)"),
    "2024-governor-IN": (
        "the candidates' votes are Indiana's results archive of the 2024 general, whose data says Certified: T "
        "(the orchestrator, 2026-11-13 04:44: \"the certified count wins\"): Braun 1,566,081, McCormick 1,183,741, "
        "Rainwater 129,781 and the write-in Stried's 52. Cha, Kuriwaki and Snyder list the two nominees alone, at "
        "1,561,279 and 1,179,967. n and each p follow the certified count (data/local/REPORT.md section 35)"),
}


def _meta(path):
    if not (os.path.exists(path) and os.path.exists(path + ".meta.json")):
        raise SystemExit(f"governor_counts: {path} (and its .meta.json) is not in the cache")
    with open(path + ".meta.json") as f:
        return json.load(f)


def ct_2018():
    """The Secretary of the State's 2018 governor contest, from the page's own data: ({name: (votes, lines)}, total,
    source). Stops where the page is not that contest, does not list the Statement of Vote under 'Official Sources',
    or its figures are not the ones expected."""
    meta = _meta(CT_PAGE)
    with open(CT_PAGE, encoding="utf-8", errors="replace") as f:
        s = f.read()
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', s, re.S)
    if not m or "Official Sources" not in s:
        raise SystemExit("governor_counts: Connecticut's page has no data, or does not say 'Official Sources'")
    c = json.loads(m.group(1))["props"]["pageProps"]["contest"]
    if (c["office"]["name"], c["division"]["displayName"], c["event"]["startDate"][:10], c["event"]["type"]["name"],
            c["isSpecial"]) != ("Governor", "State of Connecticut", "2018-11-06", "General", False):
        raise SystemExit("governor_counts: Connecticut's page is not the 2018 general's governor contest")
    files = [x["file"]["title"] for x in c.get("files") or []]
    if files != ["Statement of Vote 2018"]:
        raise SystemExit(f"governor_counts: Connecticut's page names its sources {files}")
    got, total = {}, None
    for x in c["candidates"]:
        if x["displayName"] == "Total Votes Cast":
            total = x["nVotes"]
            continue
        if x["displayName"] == "Total Ballots Cast":
            continue
        lines = None
        if (x.get("party2") or {}).get("name"):
            lines = [(x["party"]["name"], x["nVotesParty1"]), (x["party2"]["name"], x["nVotesParty2"])]
            if x.get("party3") or sum(v for _, v in lines) != x["nVotes"]:
                raise SystemExit(f"governor_counts: Connecticut's lines for {x['displayName']} do not add up")
        got[x["displayName"]] = (x["nVotes"], lines)
    fx = FIX["2018-governor-CT"]
    want = {k: (v, [tuple(t) for t in ln] if ln else None) for k, (v, ln) in fx["expect"].items()}
    if {k: (v, [tuple(t) for t in ln] if ln else None) for k, (v, ln) in got.items()} != want or total != fx["total"]:
        raise SystemExit(f"governor_counts: Connecticut's page reads {got}, total {total}")
    src = {"name": "Connecticut Secretary of the State, Election History: 2018 Nov 6, General Election, Governor "
                   "(the page's data, each candidate's votes by line)",
           "url": CT_URL, "read_utc": meta["read_utc"],
           "licence": "no licence printed; the State of Connecticut's public election returns",
           "mark": "official (the page lists the count under 'Official Sources': 'Statement of Vote 2018', page 7)",
           "via": CT_URL,
           "note": ("sha256 " + meta["sha256"][:16] + "; the page also says 'The election from the original source "
                    "document contained data entry errors that have been preserved' and 'There are discrepancies in "
                    "precinct reporting in the Town of Woodstock'")}
    return got, total, src


def ny_2018():
    """Algara and Amlani's New York 2018 governor, summed over its counties: ({record name: votes}, the record's
    source, the file's source block as D2's build writes it)."""
    with open(AA) as f:
        d = json.load(f)
    hit = [e for e in d["elections"] if e["year"] == 2018 and e["state"] == "NY" and e["type"] == "G"]
    if len(hit) != 1:
        raise SystemExit(f"governor_counts: {len(hit)} New York 2018 elections in Algara and Amlani's file")
    e = hit[0]
    if (e["counties"], e["counties_missing"], e["D"], e["R"]) != (62, 0, 3635340, 2207602):
        raise SystemExit(f"governor_counts: Algara and Amlani's New York 2018 reads {e}")
    if not ("Cuomo" in e["dem_nominee"] and "Molinaro" in e["rep_nominee"]):
        raise SystemExit(f"governor_counts: Algara and Amlani's New York 2018 nominees are {e['dem_nominee']}, "
                         f"{e['rep_nominee']}")
    meta = _meta(AA_FILE)
    src = {"name": d["source"]["name"], "url": meta["url"], "read_utc": meta["read_utc"], "licence": "CC0 1.0", "mark": "stated",
           "via": "https://doi.org/10.7910/DVN/DGUMFI",
           "note": ("the two nominees' votes, county returns summed to the state over 62 counties, none missing, by "
                    "pipeline/intake/algara_amlani.py: the authors' compilation, not a state's certified total; the "
                    "other three candidates' votes are Cha, Kuriwaki and Snyder's (v4.1), since the authors give the "
                    "others only as the county total less the two nominees")}
    return {"CUOMO, ANDREW M.": e["D"], "MOLINARO, MARCUS J. (MARC)": e["R"]}, src, d["source"]


def in_2024():
    """Indiana's archive's 2024 governor: ({archive name: votes}, source). Stops where the archive is not certified."""
    with open(IN_CHECKS) as f:
        chk = json.load(f)
    if chk.get("certified") != "T" or (chk.get("settings") or {}).get("Certified") != "T":
        raise SystemExit("governor_counts: Indiana's 2024 archive does not say Certified: T")
    hit = []
    with open(IN_ENR) as f:
        for line in f:
            c = json.loads(line)
            if c.get("title") == "Governor & Lt. Governor":
                hit.append(c)
    if len(hit) != 1:
        raise SystemExit(f"governor_counts: {len(hit)} governor contests in Indiana's 2024 archive")
    got = {" ".join(x["name"].split()): x["votes"] for x in hit[0]["candidates"]}
    if got != FIX["2024-governor-IN"]["expect"]:
        raise SystemExit(f"governor_counts: Indiana's archive reads {got}")
    src = {"name": "Indiana Election Division, results archive of the 2024 General Election (Governor & Lt. Governor)",
           "url": chk["source"]["url"], "read_utc": chk["source"]["read_utc"],
           "licence": "no licence printed; the State of Indiana's public election returns",
           "mark": "certified (the archive's settings say \"Certified\": \"T\", version 20241213_160047)",
           "via": chk["source"]["url"], "note": f"sha256 {chk['source']['sha256'][:16]}; {hit[0]['file']}"}
    return got, src


def _page_text(path):
    import html
    with open(path, encoding="utf-8", errors="replace") as f:
        t = f.read()
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t)))


def wv_2012():
    """The West Virginia Secretary of State's statewide results page of the 2012 general, its Governor contest:
    ({name: votes}, total, source). Stops where the page is not that page, lacks its 'Official Results' heading, or
    its figures are not the ones expected."""
    meta = _meta(WV_PAGE)
    s = _page_text(WV_PAGE)
    if "General Election - November 6, 2012 ★★★ Official Results ★★★" not in s:
        raise SystemExit("governor_counts: West Virginia's page is not the 2012 general's, headed Official Results")
    m = re.search(r"Back To Top Governor Contest Code: DA Candidate Party Votes Percentage State Total (.*?) "
                  r"Official Total Votes: ([\d,]+) Back To Top", s)
    if not m:
        raise SystemExit("governor_counts: West Virginia's page has no Governor contest")
    got = {}
    for name, party, votes in re.findall(r"([A-Z][A-Z .'-]+?) (Democrat|Republican|Mountain|Libertarian) "
                                         r"([\d,]+) [\d.]+% [\d,]+", m.group(1)):
        got[name.strip()] = int(votes.replace(",", ""))
    total = int(m.group(2).replace(",", ""))
    fx = FIX["2012-governor-WV"]
    if got != fx["expect"] or total != fx["total"]:
        raise SystemExit(f"governor_counts: West Virginia's page reads {got}, total {total}")
    src = {"name": "West Virginia Secretary of State, Election Results Center: Statewide Results, General Election - "
                   "November 6, 2012, Governor",
           "url": meta["url"], "read_utc": meta["finished_utc"],
           "licence": "no licence printed; the State of West Virginia's public election returns",
           "mark": "official (the page is headed '★★★ Official Results ★★★')", "via": meta["url"],
           "note": ("sha256 " + meta["sha256"][:16] + "; the page also says its pages 'should not be relied on as "
                    "official results until certified', 'Results do not include write-in candidate information', and "
                    "'Number of Precincts 1892 Number of Precincts Reporting 1846'")}
    return got, total, src


def ut_2008():
    """The Utah Lieutenant Governor's 2008 general workbook, its Governor sheet's Total row: ({name: votes}, total,
    source). LibreOffice converts the old binary workbook in the cache (as pipeline/intake/fec_federal_elections.py
    does for the FEC's), and openpyxl reads it. Stops where the figures are not the ones expected, or Algara and
    Amlani's two nominees are not within TWO_AGREE of them (the workbook bears no mark, so it stands only with a
    second count)."""
    import subprocess
    import openpyxl
    meta = _meta(UT_FILE)
    conv = os.path.join(F.CACHE, "converted")
    out = os.path.join(conv, os.path.basename(UT_FILE) + "x")
    if not os.path.exists(out):
        os.makedirs(conv, exist_ok=True)
        subprocess.run(["libreoffice", "--headless", "--convert-to", "xlsx", "--outdir", conv, UT_FILE],
                       check=True, capture_output=True)
    wb = openpyxl.load_workbook(out, read_only=True, data_only=True)
    rows = [list(r) for r in wb["Governor"].iter_rows(values_only=True)]
    head = next(r for r in rows if r and r[0] == "COUNTY")
    tot = next(r for r in rows if r and r[0] == "Total")
    got = {str(h).strip(): int(v) for h, v in zip(head[4:], tot[4:]) if h}
    total = int(tot[len([h for h in head if h])])
    fx = FIX["2008-governor-UT"]
    if got != fx["expect"] or total != fx["total"]:
        raise SystemExit(f"governor_counts: Utah's workbook reads {got}, total {total}")
    with open(AA) as f:
        e = [x for x in json.load(f)["elections"] if x["year"] == 2008 and x["state"] == "UT" and x["type"] == "G"]
    if len(e) != 1 or abs(e[0]["R"] / got['Huntsman & Herbert "R"'] - 1) > TWO_AGREE or \
            abs(e[0]["D"] / got['Springmeyer & Valdez "D"'] - 1) > TWO_AGREE:
        raise SystemExit("governor_counts: Algara and Amlani's Utah 2008 does not agree with the workbook")
    src = {"name": "Utah Lieutenant Governor, 2008 General (the workbook its historical election results page "
                   "links), Governor sheet, Total row",
           "url": meta["url"], "read_utc": meta["finished_utc"],
           "licence": "no licence printed; the State of Utah's public election returns",
           "mark": ("stated (the workbook bears no certified or official mark; it stands with Algara and Amlani's "
                    "county returns, equal to it for both nominees: the orchestrator, 2026-11-13 05:15 (3))"),
           "via": "https://vote.utah.gov/vote/historical-election-results",
           "note": "sha256 " + meta["sha256"][:16]}
    return got, total, src


def mo_official(year):
    """Missouri's official returns of a general (the Secretary of State's file in the cache): (the Democrat's votes,
    the Republican's, the file's heading words), read with pdftotext."""
    import subprocess
    path = MO_FILES[year]
    _meta(path)
    t = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True, check=True).stdout
    if year == 2008:
        head = "Official Election Returns ... As announced by the Board of State Canvassers on Tuesday, December 02, 2008"
        ok = "Official Election Returns" in t and "As announced by the Board of State Canvassers" in t
        sec = t[t.index("\nGovernor"):]
        d = int(re.search(r"Nixon, Jeremiah W\. \(Jay\)\s+DEM\s+([\d,]+)", sec).group(1).replace(",", ""))
        r = int(re.search(r"Hulshof, Kenny\s+REP\s+([\d,]+)", sec).group(1).replace(",", ""))
    elif year == 2012:
        head = ("Official Election Returns ... As announced by the Board of State Canvassers on Wednesday, December 5, "
                "2012")
        ok = "Official Election Returns" in t and "As announced by the Board of State Canvassers" in t
        sec = t[t.index("  Governor  "):]
        d = int(re.search(r"Jeremiah W\. \(Jay\) Nixon\s+Democratic\s+([\d,]+)", sec).group(1).replace(",", ""))
        r = int(re.search(r"David \(Dave\) Spence\s+Republican\s+([\d,]+)", sec).group(1).replace(",", ""))
    else:
        head = "Missouri Office of Secretary of State / OFFICIAL RESULTS / General Election - November 8, 2016"
        ok = "OFFICIAL RESULTS" in t and "General Election - November 8, 2016" in t
        i = t.index("Chris Koster Eric Greitens")
        tot = re.search(r"\nTotal\s+(\d+)\s+(\d+)\s", t[i:])
        d, r = int(tot.group(1)), int(tot.group(2))
    if not ok:
        raise SystemExit(f"governor_counts: Missouri's {year} file is not headed as official returns")
    return d, r, head


AGREE = {   # the record's count, equal to the state's official returns (the orchestrator, 2026-11-13 05:26)
    "2008-governor-MO": 2008, "2012-governor-MO": 2012, "2016-governor-MO": 2016}
AGREE_NOTE = ("the count (pipeline/governor_counts.py): Missouri's official returns ({head}; {url}, read {read}) give "
              "the Democrat {d:,} and the Republican {r:,}, this record's figures to the vote; Algara and Amlani's "
              "county returns give {ad:,} and {ar:,} [measured], short by {kd:,} and {kr:,}{kc}. So the record's count "
              "stands with the state's (the orchestrator, 2026-11-13 05:26: \"one each to ... Missouri (2008, 2012, "
              "2016) ... for the state's certified governor count\"; data/local/REPORT.md section 35)")
KC_2016 = (98336, 25284)   # Kansas City's own rows in Missouri's 2016 official results, Koster and Greitens [measured]
ME_2010_NOTE = ("the count (pipeline/governor_counts.py): Algara and Amlani's county returns give Mitchell 109,087 "
                "against this record's 103,387 (+5.5%) and LePage 217,862 against 218,065 (-0.1%), and name no other "
                "candidate, so Cutler's count has no second count [measured]. The deciding pair is LePage and Cutler; "
                "Mitchell ran third. p is not computed here, since the top two are not a Democrat and a Republican, "
                "and Maine 2014's last governor race is 2006's, so no p reads these figures. Maine's Secretary of "
                "State refused us, so no state count is read (the orchestrator, 2026-11-13 05:26; data/local/REPORT.md "
                "section 35)")


def counts():
    """{record id: ({record name: votes}, {record name: lines or None}, added [(name, party, votes)], the record's
    source, the file's source block)}."""
    out = {}
    got, total, src = ct_2018()
    fx = FIX["2018-governor-CT"]
    out["2018-governor-CT"] = ({n: got[s][0] for n, s in fx["names"].items()},
                               {n: got[s][1] for n, s in fx["names"].items()},
                               [(n, p, got[s][0]) for n, p, s in fx["add"]], src, src)
    got, src, file_src = ny_2018()
    out["2018-governor-NY"] = ({**FIX["2018-governor-NY"]["was"], **got}, {}, [], src, file_src)
    for rid, reader in (("2012-governor-WV", wv_2012), ("2008-governor-UT", ut_2008)):
        got, total, src = reader()
        fx = FIX[rid]
        out[rid] = ({n: got[s_] for n, s_ in fx["names"].items()}, {},
                    [(n, p_, got[s_]) for n, p_, s_ in fx["add"]], src, src)
    got, src = in_2024()
    fx = FIX["2024-governor-IN"]
    out["2024-governor-IN"] = ({n: got[s] for n, s in fx["names"].items()}, {},
                               [(n, p, got[s]) for n, p, s in fx["add"]], src, src)
    return out


def fix_cha(contests):
    """Cha, Kuriwaki and Snyder's normalized contests with the three governors' nominees at the counts taken here and
    the contest's total; the dataset's other candidates stand. In place; returns the list. Stops where a contest is not
    found once, or its figures are neither the dataset's nor these."""
    for rid, (now, _, added, _, _) in counts().items():
        year, st = FIX[rid]["key"]
        hit = [c for c in contests if c["year"] == year and c["office"] == "governor" and c["state"] == st
               and not c["special"]]
        if len(hit) != 1:
            raise SystemExit(f"governor_counts.fix_cha: {len(hit)} {st} {year} governor contests in Cha's file")
        c = hit[0]
        old = {a["name"]: a["votes"] for a in c["candidates"]}
        if old != FIX[rid]["was"] and old != {**FIX[rid]["was"], **now}:
            raise SystemExit(f"governor_counts.fix_cha: Cha's {st} {year} votes are not the dataset's as expected: {old}")
        for a in c["candidates"]:
            a["votes"] = now.get(a["name"], a["votes"])
        c["totalvotes"] = sum(now.get(n, v) for n, v in old.items()) + sum(v for _, _, v in added)
        c["count_fixed"] = f"pipeline/governor_counts.py: {rid}"
    return contests


def _sources_block(lines, key, src):
    """The file's top-level sources block with `key` added before "model" (as pipeline/governor_hi2018.py does)."""
    text = "\n".join(lines)
    if f'"{key}": {{' in text.split(' "model": {')[0]:
        return lines
    block = [" " + b for b in json.dumps({key: src}, indent=1, ensure_ascii=False).split("\n")[1:-1]]
    k = lines.index(' "model": {')
    if lines[k - 1] != " }," or lines[k - 2] != "  }":
        raise SystemExit("governor_counts: the file's sources block does not end where expected")
    lines[k - 2] = lines[k - 2] + ","
    lines[k - 1:k - 1] = block
    return lines


def fix_record(rid, rec, now, lines_of, added, src):
    """The record with the counts taken here; returns [(p under, was, now)]."""
    res = rec["result"]
    cands = res["candidates"]
    old = {c["name"]: c["votes"] for c in cands}
    have = {c["name"] for c in cands}
    base = {n: v for n, v in old.items() if n not in {a for a, _, _ in added}}
    if base != FIX[rid]["was"] and base != {**FIX[rid]["was"], **now}:
        raise SystemExit(f"governor_counts: {rid}'s votes are not the dataset's as expected: {old}")
    for c in cands:
        if c["name"] in now:
            c["votes"] = now[c["name"]]
        if lines_of.get(c["name"]):
            c["lines"] = [{"party": p, "votes": v} for p, v in lines_of[c["name"]]]
    for n, p, v in added:
        if n not in have:
            cands.append({"name": n, "party": p, "votes": v})
    cands.sort(key=lambda c: -c["votes"])
    res["total_votes"] = sum(c["votes"] for c in cands)
    res["source"] = src
    tp = rec["two_party"]
    tp["votes"] = [next(c["votes"] for c in cands if c["name"] == n) for n in tp["candidates"]]
    n_old, n = tp["n_other_voters"], sum(tp["votes"]) - 1
    tp["n_other_voters"] = n
    tp["share_first"] = round(tp["votes"][0] / sum(tp["votes"]), 6)
    b = rec.get("ballot") or {}
    on = [c for c in cands if c["party"] not in ("D", "R") and not c["party"].startswith("W-I")]
    if b.get("others") is not None:
        b["others"] = len(on)
    moves = []
    p = rec["p"]
    if p.get("method") != "density" or p.get("n") not in (n_old, n):
        raise SystemExit(f"governor_counts: {rid}'s p is not a density p on n {n_old}: {p.get('method')}, {p.get('n')}")
    for x in [p] + list(p.get("alongside") or []):
        if x.get("method") != "density":
            raise SystemExit(f"governor_counts: a p of {rid} under {x['under']} is not a density p")
        was = x["value"]
        x["event"] = x["f_half"] / n
        x["value"] = x["event"] / 2
        moves.append((x["under"], was, x["value"]))
    p["n"] = n
    note = TAG + NOTES[rid]
    # the dataset's note on its totals (candidates under ten votes left out) is not the state's, whose count is taken
    # whole where the state gives every candidate (Connecticut, Indiana); New York keeps it for its other candidates
    drop = (CHA_NOTE,) if rid != "2018-governor-NY" else ()
    rec["notes"] = [x for x in rec["notes"] if not x.startswith(TAG) and not x.startswith(drop or ("\0",))] + [note]
    return moves


def last_race(fixed):
    """Every governor record after the first fixed year whose forecast input "last_governor_race" is one of the fixed
    contests, read again from chambers.last_governor_index() (with fix_cha); returns [(id, was, now)]."""
    import chambers as CH
    idx = CH.last_governor_index()
    moves = []
    for year in range(min(y for y, _ in fixed) + 1, 2026):
        path = os.path.join(REPO, "data", "governor", f"{year}.json")
        if not os.path.exists(path):
            continue
        with open(path) as f:
            lines = f.read().split("\n")
        hit = False
        for i, l in enumerate(lines):
            if not l.startswith('  {"id":"') or '"last_governor_race":{"year":' not in l:
                continue
            comma = l.endswith(",")
            rec = json.loads(l.strip().rstrip(","))
            st = rec["place"]["state"]
            lg = rec["forecast_inputs"]["last_governor_race"]
            if (lg["year"], st) not in fixed:   # a special too (Utah 2010's reads Utah 2008)
                continue
            now = CH.last_governor_race(idx, st, year)
            if now is None or now[0] != lg["year"]:
                raise SystemExit(f"governor_counts.last_race: {rec['id']}'s last race now reads {now}")
            new = {"year": now[0], "share_D": now[1], "special": now[2], "source": now[3]}
            note = NOTE_LAST.format(state=f"{rec['place']['name']} {lg['year']}")
            if new != lg or note not in rec["notes"]:
                if new != lg:
                    moves.append((rec["id"], lg["share_D"], now[1]))
                rec["forecast_inputs"]["last_governor_race"] = new
                if note not in rec["notes"]:
                    rec["notes"] = [x for x in rec["notes"] if not x.startswith(NOTE_LAST.split("(")[0] + "(")]
                    rec["notes"].append(note)
                lines[i] = "  " + json.dumps(rec, separators=(",", ":"), ensure_ascii=False) + ("," if comma else "")
                hit = True
        if hit:
            with open(path, "w") as f:
                f.write("\n".join(lines))
    return moves


def notes_only():
    """The records whose count a state's official returns confirm (AGREE), and Maine 2010 (ME_2010_NOTE): a note
    each, the counts unchanged; stops where a record's figures are not the state's. Returns [(id, note)]."""
    with open(AA) as f:
        aa = {(e["year"], e["state"]): e for e in json.load(f)["elections"] if e["type"] == "G"}
    done = []
    for rid in list(AGREE) + ["2010-governor-ME"]:
        year = int(rid[:4])
        path = os.path.join(REPO, "data", "governor", f"{year}.json")
        with open(path) as f:
            lines = f.read().split("\n")
        at = [i for i, l in enumerate(lines) if l.startswith('  {"id":"' + rid + '"')]
        if len(at) != 1:
            raise SystemExit(f"governor_counts: {rid} is found {len(at)} times in {path}")
        comma = lines[at[0]].endswith(",")
        rec = json.loads(lines[at[0]].strip().rstrip(","))
        cands = rec["result"]["candidates"]
        if rid in AGREE:
            d, r, head = mo_official(AGREE[rid])
            rd = next(c["votes"] for c in cands if c["party"] == "D")
            rr = next(c["votes"] for c in cands if c["party"] == "R")
            if (rd, rr) != (d, r):
                raise SystemExit(f"governor_counts: {rid}: the record has {rd}, {rr}; the state {d}, {r}")
            e = aa[(year, "MO")]
            kd, kr = d - e["D"], r - e["R"]
            if year == 2016:
                if (kd, kr) != KC_2016:
                    raise SystemExit(f"governor_counts: {rid}: Algara and Amlani's shortfall is {kd}, {kr}")
                kc = (", which are Kansas City's own rows in the state's 2016 returns to the vote: Algara and Amlani's "
                      "rows lack Kansas City, which reports apart from Jackson County")
            else:
                kc = (" (the state's file gives no rows by county; in 2016 the shortfall is Kansas City's own rows to "
                      "the vote)")
            meta = _meta(MO_FILES[AGREE[rid]])
            note = AGREE_NOTE.format(head=head, url=meta["url"], read=meta["finished_utc"], d=d, r=r, ad=e["D"],
                                     ar=e["R"], kd=kd, kr=kr, kc=kc)
        else:
            e = aa[(2010, "ME")]
            got = {c["name"]: c["votes"] for c in cands}
            if (e["D"], e["R"], got.get("MITCHELL, ELIZABETH H. (LIBBY)"), got.get("LEPAGE, PAUL R.")) != \
                    (109087, 217862, 103387, 218065) or rec["p"].get("value") is not None:
                raise SystemExit(f"governor_counts: {rid} is not as read")
            note = ME_2010_NOTE
        rec["notes"] = [x for x in rec["notes"] if not x.startswith(TAG)] + [note]
        lines[at[0]] = "  " + json.dumps(rec, separators=(",", ":"), ensure_ascii=False) + ("," if comma else "")
        with open(path, "w") as f:
            f.write("\n".join(lines))
        done.append((rid, note))
    return done


def main():
    cs = counts()
    for year in sorted({FIX[r]["key"][0] for r in FIX}):
        path = os.path.join(REPO, "data", "governor", f"{year}.json")
        with open(path) as f:
            lines = f.read().split("\n")
        for rid in [r for r in FIX if FIX[r]["key"][0] == year]:
            now, lines_of, added, src, file_src = cs[rid]
            at = [i for i, l in enumerate(lines) if l.startswith('  {"id":"' + rid + '"')]
            if len(at) != 1:
                raise SystemExit(f"governor_counts: {rid} is found {len(at)} times in {path}")
            line = lines[at[0]]
            comma = line.endswith(",")
            rec = json.loads(line.strip().rstrip(","))
            n_old = rec["two_party"]["n_other_voters"]
            moves = fix_record(rid, rec, now, lines_of, added, src)
            lines[at[0]] = "  " + json.dumps(rec, separators=(",", ":"), ensure_ascii=False) + ("," if comma else "")
            lines = _sources_block(lines, FIX[rid]["source_key"], file_src)
            print(f"{rid}: n {n_old:,} -> {rec['two_party']['n_other_voters']:,}; total {rec['result']['total_votes']:,}")
            for under, a, b in moves:
                print(f"  p under {under[:60]}: {a:.6g} -> {b:.6g} ({b / a:.5f}x)")
        with open(path, "w") as f:
            f.write("\n".join(lines))
    for rid, a, b in last_race({FIX[r]["key"] for r in FIX}):
        print(f"{rid}: last governor race, the Democrat's two-party share {a:.6f} -> {b:.6f}")
    for rid, note in notes_only():
        print(f"{rid}: note: {note[:140]}...")


if __name__ == "__main__":
    main()
