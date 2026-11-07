"""Governors' incumbency: every nominee's code checked against the record's own last race for the seat, and the codes
the record or the state's own roster of governors proves wrong, fixed (the orchestrator, 2026-11-07 13:06 UTC).

Reason (the orchestrator): "incumbency is an input to every governor's forecast. One miscode found by chance means we
need to know how many others there are." The one found by chance: Cha, Kuriwaki and Snyder code New Jersey 2021's
Murphy 0, though he won in 2017 (data/congress/REPORT.md 9.6).

The check (survey):
  - Every governor contest in data/governor/*.json is read, Louisiana apart (its two rounds: no p, and not in the fit).
  - A nominee is the candidate with the most votes on a Democratic (or Republican) line, by build_congress.major,
    as the files take it (fusion lines such as New York's "D,WF,Indep" and Minnesota's DFL count; a write-in does
    not).
  - Each nominee's code is the one the source carries:
      - Cha's inc, found by the nominee's exact name within Cha's own contest, so not through build_congress's
        last-name join (cha_entry); or
      - Algara and Amlani's seat status.
  - It is set against whether the nominee won the state's previous governor contest in the files (for the first
    contest of a state, Algara and Amlani's last race before 1977).
  - Two kinds of disagreement are listed:
      A. the nominee won the last race and is not coded 1;
      B. the nominee is coded 1 (or Cha's 2 or 3) and did not win the last race;
      C. the nominee is coded 1 and won the last race, which was a special election (Cha's guide codes that 2).
  - A nominee of B may be a governor who took office mid-term, which the last race cannot show. For those the state's
    own roster of governors is read where it answers. Where it does not, the code is kept and marked inferred (the
    orchestrator).

What counts as an incumbent is the record's, unchanged (REPORT 2.2 and 0.2), and made to hold in every year (the
orchestrator, 2026-11-07 13:43 UTC: "Keep the definition of record and make every era match it. Don't add a new
variant."; reason: "an input has to mean one thing in every year it is fitted on. This rule is fixed now, before any
score, and it is the one the record already uses."):
  - Cha's code 1 only, and Algara and Amlani's "Incumbent" seat status.
  - Cha's 2 (an incumbent elected in a special election) and 3 (a senator appointed by the governor, in the guide;
    Cha uses it for governors who succeeded too) read as not incumbents. Counting them was tested and not adopted
    (REPORT 0.2).
  - So "a successor who was not elected to the seat is not the incumbent, and this holds in every year" (13:43):
      - Algara and Amlani code such successors "Incumbent". Where the state's roster confirms the succession, the
        seat status is recoded to the successor party's "Open Seat" (0). Where no roster answers, the code is kept
        and marked inferred.
      - Cha codes Brewer (AZ 2010) 1 and its other successors 3: she is recoded 3, which reads as 0.
      - Cha codes Tomblin (WV 2012, who won the 2011 special) 1 and Brown (OR 2018) and Herbert (UT 2012), in the
        same place, 2: he is recoded 2, which reads as 0 (kind C; D2's reading of the 13:43 rule, not named in it).
  - A nominee Cha codes 2 or 3 is coded right by Cha's own guide, and the code is kept.

The fixes are applied where the source is read: fix_cha (chambers.fit_rows, chambers.odd_governor_rows,
build_congress.cha_index) and fix_aa (chambers.aa_governors, build_congress.AA_SOURCE). Each governor contest the
check looked at carries forecast_inputs.incumbency_check (note).

Usage:
  python3 pipeline/governor_incumbency.py check        # the survey, the rosters' gate, and the table
  python3 pipeline/governor_incumbency.py moves REV    # every governor p and model term that moved since REV
Writes data/congress/governor-incumbency.json. The rosters are read with pipeline/fetch.py into
$CACHE/rosters/ (fetch_rosters) and stay outside the repository.
"""
import collections
import glob
import html
import json
import os
import re
import subprocess
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "intake"))
sys.path.insert(0, HERE)
import congress_common as cc  # noqa: E402

TABLE = os.path.join(REPO, "data", "congress", "governor-incumbency.json")
ASKED = "the orchestrator, 2026-11-07 13:06 UTC; its rule for successors, 13:43 UTC"

# The states' own rosters of governors that answered (read 2026-11-07 13:11-13:16 UTC), each with the words the
# check rests on. gate() finds every quote in the cached file before the table is written.
ROSTERS = {
    "AL": ("Alabama Department of Archives and History, Alabama Governors",
           "https://archives.alabama.gov/research/guidance/fast-facts/officials/governor.aspx", "rosters/AL.html"),
    "AR": ("Arkansas Secretary of State, State Governors (1975 - Present)",
           "https://sos.arkansas.gov/education/educational-media/governors-of-arkansas-portrait-gallery/"
           "state-governors-1975-present", "rosters/AR.html"),
    "AZ": ("Office of the Arizona Governor, Arizona Governors",
           "https://azgovernor.gov/governor/arizona-governors", "rosters/AZ.html"),
    "CA": ("California State Library, Governors' Gallery: Arnold Schwarzenegger",
           "https://governors.library.ca.gov/38-schwarzenegger.html", "rosters/CA.html"),
    "CT": ("Connecticut State Library, Roster of Connecticut Governors - Finding Aids",
           "https://portal.ct.gov/csl/research/governors-of-connecticut/finding-aids", "rosters/CT.html"),
    "MN": ("Minnesota Legislative Reference Library, Minnesota Governors, 1849-Present",
           "https://www.lrl.mn.gov/mngov/gov.aspx", "rosters/MN.html"),
    "NV": ("Nevada State Library, Archives and Public Records, Governors",
           "https://nsla.nv.gov/archives-governor", "rosters/NV.html"),
    "SC": ("South Carolina Legislative Manual, 2026, The Governor",
           "https://www.scstatehouse.gov/man26/04_Gov.pdf", "rosters/SC.pdf"),
    "TX": ("Legislative Reference Library of Texas, Texas Governors",
           "https://lrl.texas.gov/legeleaders/governors/govBrowse.cfm", "rosters/TX.html"),
    "VT": ("Vermont Legislature, Governors of Vermont (2018)",
           "https://legislature.vermont.gov/assets/All-House-Documents/Governors2018.pdf", "rosters/VT.pdf"),
}

# Rosters that did not answer. Nothing else was tried for these: no other host of a refusing agency (so not
# floridamemory.com or arts-culture.dos.fl.gov, which are the Florida Department of State's too), and no copy of the
# page elsewhere. Reason: "If a tool or the network refuses you, stop that part and tell the orchestrator at once;
# never route around a refusal." Reported to the orchestrator at 13:14 UTC.
ROSTERS_NOT_READ = {
    "FL": {"url": "https://dos.fl.gov/florida-facts/florida-history/florida-governors/kenneth-hood-mackay-jr/",
           "answer": "HTTP 403", "utc": "2026-11-07 13:11"},
    "MO": {"url": "https://sos.mo.gov/archives/history/historicallistings/governors",
           "answer": "HTTP 403", "utc": "2026-11-07 13:11"},
    "NH": {"url": "https://www.nh.gov/almanac/governors.htm", "answer": "HTTP 403", "utc": "2026-11-07 13:11"},
    "WI": {"url": "https://docs.legis.wisconsin.gov/misc/lrb/blue_book/2025_2026/180_historical_lists.pdf",
           "answer": "the connection was reset (curl 35), at 13:11 and again at 13:16 (one retry, as a network "
                     "error)", "utc": "2026-11-07 13:16"},
    "ID": {"url": ["https://sos.idaho.gov/blue_book/2018/2017-2018_Bluebook_Complete.pdf",
                   "https://sos.idaho.gov/blue_book/2021/03_Executive.pdf",
                   "https://sos.idaho.gov/blue_book/blue_book_2025-2026.pdf"],
           "answer": "HTTP 404 at each address (found by a search engine); the Blue Book was not found",
           "utc": "2026-11-07 13:17-13:18"},
    "MA": {"url": None, "answer": "no roster of the Commonwealth's own was found by search", "utc": None},
}

LAST = "the seat's last race in the record"
SUC = ("a successor, not elected to the seat, is not the incumbent (the orchestrator, 2026-11-07 13:43; the record "
       "reads Cha's 3 so, REPORT 0.2): ")
DEF = ("the record reads Cha's 2 and 3 as not incumbents (REPORT 2.2; counting them was tested in 0.2 and not "
       "adopted), so the code is kept")

# (year, state, special, side) -> the nominee as the source names them, the code the source carries, the verdict,
# why, the roster and its quotes (or None), and the fix (or None). The verdicts:
#   fixed      the code is wrong by its own meaning or by the definition of record in every year (13:43), and the
#              record or the state's roster proves it;
#   kept       Cha's code 2 or 3, right by Cha's own guide (DEF);
#   inferred   the roster did not answer or was not found; the code is kept, unproven.
# (Until 13:43 a successor the roster confirmed was "confirmed" and kept; the orchestrator's rule of 13:43 recodes
# them.)
CHECKS = {
    # A. won the last race, not coded 1
    (2021, "NJ", False, "D"): ("MURPHY, PHILIP", 0, "fixed",
                               "Cha codes him 0, but he won " + LAST + " (2017, data/governor/2017.json, from Algara "
                               "and Amlani) and is the nominee: the incumbent", None, None,
                               {"cha": (0, 1)}),
    (2018, "AR", False, "R"): ("HUTCHINSON, WILLIAM (ASA)", 0, "fixed",
                               "Cha codes him 0, but he won " + LAST + " (2014, data/governor/2014.json) and is the "
                               "nominee: the incumbent; Arkansas's roster agrees (served 2015-2023)", "AR",
                               ["Asa Hutchinson Born: December 3, 1950, at Bentonville, Arkansas. Died: n/a Buried: "
                                "n/a Served: 2015-2023"], {"cha": (0, 1)}),
    (2018, "OR", False, "D"): ("BROWN, KATE", 2, "kept",
                               "Cha codes her 2, an incumbent elected in a special election; she won " + LAST +
                               ", the special of 2016 (data/governor/2016.json); " + DEF, None, None, None),
    (2012, "UT", False, "R"): ("HERBERT, GARY RICHARD", 2, "kept",
                               "Cha codes him 2, an incumbent elected in a special election; he won " + LAST +
                               ", the special of 2010 (data/governor/2010.json); " + DEF, None, None, None),
    # B. coded 1 (or 2 or 3), did not win the last race. Proven by the record: both nominees coded 1, and only one
    # can be the sitting governor; the record's last race says which
    (2019, "KY", False, "D"): ("BESHEAR, ANDY", 1, "fixed",
                               "Cha codes both nominees 1; the Republican, Bevin, won " + LAST + " (2015, "
                               "data/governor/2015.json), so Beshear is not the incumbent", None, None,
                               {"cha": (1, 0)}),
    (2020, "VT", False, "D"): ("ZUCKERMAN, DAVID E. (DAVE)", 1, "fixed",
                               "Cha codes both nominees 1; the Republican, Scott, won " + LAST + " (2018, "
                               "data/governor/2018.json), so Zuckerman is not the incumbent", None, None,
                               {"cha": (1, 0)}),
    # proven by the state's roster
    (1982, "MN", False, "D"): ("Perpich, Rudy", "Democratic Incumbent", "fixed",
                               "Algara and Amlani code an incumbent's bid, but Minnesota's roster has Al Quie in "
                               "office from 1/4/1979 and Perpich from 1/3/1983 (his first time, 12/29/1976): in "
                               "November 1982 the governor was Quie, who was not a nominee. An open seat, held by "
                               "the Independent-Republicans", "MN",
                               ["Rudy Perpich 1/3/1983 36th", "Al Quie 1/4/1979 35th", "Rudy Perpich 12/29/1976 34th"],
                               {"aa": ("Democratic Incumbent", "Republican Open Seat")}),
    # successors, fixed: the state's roster shows the nominee took office mid-term without winning the seat's last
    # race. By the orchestrator's rule of 13:43 ("a successor who was not elected to the seat is not the incumbent,
    # and this holds in every year"), as the record reads Cha's code 3, they are not incumbents: an open seat, held
    # by the successor's party.
    (1994, "AL", False, "D"): ("Folsom, James E. Jr.", "Democratic Incumbent", "fixed",
                               SUC + "he succeeded Hunt (" + LAST + ", 1990) on April 22, 1993", "AL",
                               ["James E. Folsom Jr. Cullman April 22, 1993 - 1995 Democrat Lieutenant Governor "
                                "Folsom became governor when Governor Hunt was convicted for ethics violations."],
                               {"aa": ("Democratic Incumbent", "Democratic Open Seat")}),
    (1994, "AR", False, "D"): ("Tucker, Jim Guy", "Democratic Incumbent", "fixed",
                               SUC + "he served the balance of Clinton's term (" + LAST + ", 1990)", "AR",
                               ["He served the balance of the Clinton term and then was elected to a four-year term in "
                                "November 1994.", "Served: 1979-1981; 1983-1992"],
                               {"aa": ("Democratic Incumbent", "Democratic Open Seat")}),
    (1998, "AR", False, "R"): ("Huckabee, Mike", "Republican Incumbent", "fixed",
                               SUC + "he became governor in July 1996 when Tucker (" + LAST + ", 1994) resigned",
                               "AR", ["He became Governor of Arkansas in July 1996 when his predecessor resigned."],
                               {"aa": ("Republican Incumbent", "Republican Open Seat")}),
    (1978, "AZ", False, "D"): ("Babbitt, Bruce", "Democratic Incumbent", "fixed",
                               SUC + "the roster has Castro (" + LAST + ", 1974) to 1977, Bolin 1977 to 1978 and "
                               "Babbitt from 1978; it gives years only, but either way Babbitt did not win the seat "
                               "before 1978", "AZ",
                               ["Raul H. Castro 1975 to 1977", "Harvey Wesley Bolin 1977 to 1978",
                                "Bruce Babbitt 1978 to 1987"],
                               {"aa": ("Democratic Incumbent", "Democratic Open Seat")}),
    (1998, "AZ", False, "R"): ("Hull, Jane Dee", "Republican Incumbent", "fixed",
                               SUC + "the roster has Symington (" + LAST + ", 1994) to 1997 and Hull from 1997", "AZ",
                               ["J. Fife Symington 1991 to 1997", "Jane Dee Hull 1997 to 2003"],
                               {"aa": ("Republican Incumbent", "Republican Open Seat")}),
    (2010, "AZ", False, "R"): ("BREWER, JANICE (JAN)", 1, "fixed",
                               SUC + "Cha codes her 1, but the roster has Napolitano (" + LAST + ", 2006) to 2009 and "
                               "Brewer from 2009; Cha codes the other successors 3", "AZ",
                               ["Janet Napolitano 2003 to 2009", "Janice K. Brewer 2009 to 2015"], {"cha": (1, 3)}),
    (1982, "CT", False, "D"): ("O'Neill, William A.", "Democratic Incumbent", "fixed",
                               SUC + "the roster has Grasso (" + LAST + ", 1978) to 1980 and O'Neill from 1980", "CT",
                               ["Ella T. Grasso 1975-80", "William A. O\u2019Neill 1980-91"],
                               {"aa": ("Democratic Incumbent", "Democratic Open Seat")}),
    (1978, "MN", False, "D"): ("Perpich, Rudy", "Democratic Incumbent", "fixed",
                               SUC + "he assumed office 12/29/1976, after Anderson (" + LAST + ", 1974)", "MN",
                               ["Wendell Anderson 1/4/1971 33rd", "Rudy Perpich 12/29/1976 34th"],
                               {"aa": ("Democratic Incumbent", "Democratic Open Seat")}),
    (1990, "NV", False, "D"): ("Miller, Robert J.", "Democratic Incumbent", "fixed",
                               SUC + "the roster has Bryan (" + LAST + ", 1986) to Jan 3, 1989 and Miller from then",
                               "NV", ["Richard Hudson Bryan Jan 3, 1983 - Jan 3, 1989",
                                      "Bob Miller Jan 3, 1989 - Jan 4, 1999"],
                               {"aa": ("Democratic Incumbent", "Democratic Open Seat")}),
    (2002, "TX", False, "R"): ("Perry, Rick", "Republican Incumbent", "fixed",
                               SUC + "he was sworn in December 21, 2000, after Bush (" + LAST + ", 1998) resigned",
                               "TX", ["Rick Perry R December 21, 2000\u2013January 20, 2015; 76th\u201384th "
                                      "Legislatures Sworn in after Bush resignation."],
                               {"aa": ("Republican Incumbent", "Republican Open Seat")}),
    (1992, "VT", False, "D"): ("Dean, Howard B.", "Democratic Incumbent", "fixed",
                               SUC + "he became governor in 1991 by reason of the death of Snelling (" + LAST +
                               ", 1990)", "VT",
                               ["^^^Howard Dean, Burlington ....................... 1991-2003",
                                "Lieutenant Governor, Governor by reason of the death of Gov. Snelling"],
                               {"aa": ("Democratic Incumbent", "Democratic Open Seat")}),
    # C. won the last race, which was a special election, and coded 1: Cha's guide codes that 2, as it codes Brown
    # (OR 2018) and Herbert (UT 2012), and the record reads 2 as not an incumbent (the orchestrator, 13:43: "an input
    # has to mean one thing in every year it is fitted on")
    (2012, "WV", False, "D"): ("TOMBLIN, EARL RAY", 1, "fixed",
                               "Cha codes him 1, but he won " + LAST + " as a special election (2011, "
                               "data/governor/2011.json): Cha's guide codes that 2, as it does Brown (OR 2018) and "
                               "Herbert (UT 2012), and the record reads 2 as not an incumbent", None, None,
                               {"cha": (1, 2)}),
    # kept: Cha's 2 or 3 (DEF); the roster, where it answered, shows the nominee sat
    (2018, "AL", False, "R"): ("IVEY, KAY E.", 3, "kept",
                               "Cha codes her 3; the roster: she became governor in 2017 when Bentley (" + LAST +
                               ", 2014) resigned; " + DEF, "AL",
                               ["Lieutenant Governor Ivey became governor when Governor Robert Bentley resigned"], None),
    (2006, "CA", False, "R"): ("SCHWARZENEGGER, ARNOLD", 2, "kept",
                               "Cha codes him 2 (elected in the recall of 2003, which the record does not hold; Davis "
                               "won " + LAST + ", 2002); the roster: governor 2003-2011; " + DEF, "CA",
                               ["Arnold Schwarzenegger 2003–2011"], None),
    (2006, "CT", False, "R"): ("RELL, M. JODI", 3, "kept",
                               "Cha codes her 3; the roster: governor 2004-2011 (Rowland won " + LAST + ", 2002); " +
                               DEF, "CT", ["M. Jodi Rell 2004-2011"], None),
    (2018, "SC", False, "R"): ("MCMASTER, HENRY D.", 3, "kept",
                               "Cha codes him 3; the Legislative Manual: assumed office January 24, 2017 (Haley won " +
                               LAST + ", 2014); " + DEF, "SC",
                               ["assumed office of Gov. on Jan. 24, 2017; elected Gov. Nov. 6, 2018"], None),
    (2020, "MO", False, "R"): ("PARSON, MIKE", 3, "kept",
                               "Cha codes him 3 (Greitens won " + LAST + ", 2016); Missouri's roster refused (HTTP "
                               "403), so not checked; " + DEF, None, None, None),
    (2018, "IA", False, "R"): ("REYNOLDS, KIM", 3, "kept",
                               "Cha codes her 3 (Branstad won " + LAST + ", 2014); no roster read, since no roster "
                               "could move a p; " + DEF, None, None, None),
    (2010, "IL", False, "D"): ("QUINN, PATRICK G. (PAT)", 3, "kept",
                               "Cha codes him 3 (Blagojevich won " + LAST + ", 2006); no roster read, since no roster "
                               "could move a p; " + DEF, None, None, None),
    (2006, "MA", False, "R"): ("HEALEY, KERRY MURPHY", 3, "kept",
                               "Cha codes her 3 (Romney won " + LAST + ", 2002, and was not a nominee); no roster of "
                               "the Commonwealth's own was found; " + DEF, None, None, None),
    (2022, "NY", False, "D"): ("HOCHUL, KATHLEEN COURTNEY (KATHY)", 3, "kept",
                               "Cha codes her 3 (Cuomo won " + LAST + ", 2018); no roster read, since no roster "
                               "could move a p; " + DEF, None, None, None),
    (2016, "OR", True, "D"): ("BROWN, KATE", 3, "kept",
                              "Cha codes her 3 (Kitzhaber won " + LAST + ", 2014); no roster read, since no roster "
                              "could move a p; " + DEF, None, None, None),
    (2010, "UT", True, "R"): ("HERBERT, GARY RICHARD", 3, "kept",
                              "Cha codes him 3 (Huntsman won " + LAST + ", 2008); no roster read, since no roster "
                              "could move a p; " + DEF, None, None, None),
    (2010, "AK", False, "R"): ("PARNELL, SEAN R.", 3, "kept",
                               "Cha codes him 3 (Palin won " + LAST + ", 2006); no roster read, since no roster "
                               "could move a p; " + DEF, None, None, None),
    # inferred: coded the incumbent, did not win the last race, and the state's roster did not answer
    (1998, "FL", False, "D"): ("MacKay, Kenneth H.", "Democratic Incumbent", "inferred",
                               "Chiles won " + LAST + " (1994) and was not a nominee; Florida's roster refused (HTTP "
                               "403), so the code is kept, unproven", None, None, None),
    (1988, "NH", False, "D"): ("McEachern, Paul", "Democratic Incumbent", "inferred",
                               "Sununu won " + LAST + " (1986) and was not a nominee; New Hampshire's roster refused "
                               "(HTTP 403), so the code is kept, unproven", None, None, None),
    (1978, "WI", False, "D"): ("Schreiber, Martin J.", "Democratic Incumbent", "inferred",
                               "Lucey won " + LAST + " (1974) and was not a nominee; the Blue Book's list did not "
                               "answer (the connection was reset twice), so the code is kept, unproven", None, None,
                               None),
    (2002, "WI", False, "R"): ("McCallum, Scott", "Republican Incumbent", "inferred",
                               "Thompson won " + LAST + " (1998) and was not a nominee; the Blue Book's list did not "
                               "answer (the connection was reset twice), so the code is kept, unproven", None, None,
                               None),
    (1978, "ID", False, "D"): ("Evans, John V.", "Democratic Incumbent", "inferred",
                               "Andrus won " + LAST + " (1974) and was not a nominee; Idaho's Blue Book was not found "
                               "(HTTP 404), so the code is kept, unproven", None, None, None),
    (1998, "MA", False, "R"): ("Cellucci, Argeo Paul", "Republican Incumbent", "inferred",
                               "Weld won " + LAST + " (1994) and was not a nominee; no roster of the Commonwealth's "
                               "own was found, so the code is kept, unproven", None, None, None),
}

CHA_FIX = {(y, st, sp, x[0]): x[6]["cha"] for (y, st, sp, side), x in CHECKS.items() if x[6] and "cha" in x[6]}
AA_FIX = {(y, st): x[6]["aa"] for (y, st, sp, side), x in CHECKS.items() if x[6] and "aa" in x[6]}


def fix_cha(contests):
    """Cha, Kuriwaki and Snyder's contests (the normalized file's list), with the governors' codes CHECKS fixes set,
    in place. Each fix must find its nominee with the code it corrects. The candidate keeps the source's code as
    inc_source."""
    hit = collections.Counter()
    for c in contests:
        if c["office"] != "governor":
            continue
        for a in c["candidates"]:
            k = (c["year"], c["state"], bool(c["special"]), a["name"])
            if k in CHA_FIX:
                frm, to = CHA_FIX[k]
                if a.get("inc_source", a["inc"]) != frm:
                    raise SystemExit(f"governor_incumbency: {k} is coded {a['inc']} in Cha, not {frm}")
                a["inc_source"], a["inc"] = frm, to
                hit[k] += 1
    missing = [k for k in CHA_FIX if not hit[k]]
    if missing:
        raise SystemExit(f"governor_incumbency: no Cha nominee for {missing}")
    return contests


def fix_aa(elections):
    """Algara and Amlani's governor elections, with the seat statuses CHECKS fixes set (and incumbency from them),
    in place. The election keeps the source's status as seat_status_source."""
    hit = collections.Counter()
    for r in elections:
        k = (r["year"], r["state"])
        if k in AA_FIX:
            frm, to = AA_FIX[k]
            if r.get("seat_status_source", r["seat_status"]) != frm:
                raise SystemExit(f"governor_incumbency: {k} has seat status {r['seat_status']!r}, not {frm!r}")
            r["seat_status_source"], r["seat_status"] = frm, to
            r["incumbency"] = 1 if to == "Democratic Incumbent" else -1 if to == "Republican Incumbent" else 0
            hit[k] += 1
    missing = [k for k in AA_FIX if not hit[k]]
    if missing:
        raise SystemExit(f"governor_incumbency: no Algara and Amlani election for {missing}")
    return elections


def note(year, state, special):
    """forecast_inputs.incumbency_check for a governor contest the check looked at, else None."""
    out = [{"side": side, "nominee": x[0], "code_in_source": x[1], "verdict": x[2], "why": x[3],
            "roster": x[4]} for (y, st, sp, side), x in sorted(CHECKS.items())
           if (y, st, sp) == (year, state, bool(special))]
    if not out:
        return None
    return {"nominees": out, "table": "data/congress/governor-incumbency.json", "asked": ASKED}


# ----------------------------------------------------------------------------- the survey
def _norm(s):
    return unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().upper().replace(".", "")


def _split(name):
    """(surname, first names and nicknames) of a name written "LAST, FIRST (NICK)" or "First Last"."""
    s = _norm(name)
    nick = re.findall(r"\(([^)]*)\)", s)
    s = re.sub(r'\([^)]*\)|"[^"]*"', " ", s)
    sfx = ("JR", "SR", "II", "III", "IV")
    if "," in s:
        last, first = s.split(",", 1)
        last = last.split()[-1] if last.split() else last
        firsts = first.split()
    else:
        t = [x for x in s.split() if x not in sfx]
        last, firsts = (t[-1], t[:-1]) if t else (s, [])
    return last.strip(), [x for x in firsts if x not in sfx] + [n.strip() for n in nick]


def same_person(a, b):
    """"name" when the surnames agree and a first name or nickname agrees (its first three letters, or an initial),
    "surname" when the surnames agree and one has no first name, False when only the surnames agree, else None."""
    la, fa = _split(a)
    lb, fb = _split(b)
    if la != lb:
        return None
    if not fa or not fb:
        return "surname"
    for x in fa:
        for y in fb:
            if x[:3] == y[:3] or (len(x) == 1 and y[0] == x) or (len(y) == 1 and x[0] == y):
                return "name"
    return False


def _winner(c):
    cs = [a for a in c["result"]["candidates"] if a["votes"]]
    named = [a for a in cs if not (a["name"] or "").startswith("others (not named")]
    oth = sum(a["votes"] for a in cs if (a["name"] or "").startswith("others (not named"))
    if not named:
        return None
    w = max(named, key=lambda a: a["votes"])
    return None if oth and oth >= w["votes"] else w["name"]


def _aa_winner(r):
    D, R, o = r["D"] or 0, r["R"] or 0, r["others"] or 0
    if o >= max(D, R):
        return None
    return r["dem_nominee"] if D > R else r["rep_nominee"]


def survey():
    """The disagreements (A, B and C above), as [(year, state, special, side, nominee, code in the source, kind, last
    race's year, its winner, the code's source)], from the files and the sources as they come (before fix_cha and
    fix_aa), and the cases it cannot settle (no last winner, or a surname-only match)."""
    cha = cc.read_json(os.path.join(cc.CACHE, "cha", "normalized", "contests.json"))["contests"]
    aa = cc.read_json(os.path.join(cc.CACHE, "algara_amlani", "normalized", "governors.json"))["elections"]
    chx = collections.defaultdict(list)
    for c in cha:
        if c["office"] == "governor":
            chx[(c["year"], c["state"], bool(c["special"]))].append(c)
    aax = {(r["year"], r["state"]): r for r in aa}
    rec = collections.defaultdict(list)
    for f in sorted(glob.glob(os.path.join(REPO, "data", "governor", "*.json"))):
        for c in cc.read_json(f)["contests"]:
            rec[c["place"]["state"]].append(c)
    from build_congress import major     # the files' own rule for a nominee's side (fusion lines, DFL, write-ins)
    out, odd = [], []
    for st, cs in rec.items():
        if st == "LA":
            continue
        cs = sorted(cs, key=lambda c: (c["year"], c["date"] or f"{c['year']}-12-31"))
        for i, c in enumerate(cs):
            if i:
                lw, ly = _winner(cs[i - 1]), cs[i - 1]["year"]
            else:
                p = sorted([r for r in aa if r["state"] == st and 1950 <= r["year"] < c["year"]],
                           key=lambda r: r["year"])
                lw, ly = (_aa_winner(p[-1]), p[-1]["year"]) if p else (None, None)
            src = (c.get("forecast_inputs") or {}).get("incumbency_source")
            noms = {}
            for a in c["result"]["candidates"]:
                s = major([a["party"]]) if a["party"] else None
                if s and a["votes"] and (s not in noms or a["votes"] > noms[s][1]):
                    noms[s] = (a["name"], a["votes"])
            k3 = (c["year"], st, bool(c["special"]))
            for s, (n, v) in noms.items():
                if src == "cha":
                    cc_ = [x for x in chx[k3] if not x["runoff"]] or chx[k3]
                    hit = [a["inc"] for x in cc_ for a in x["candidates"] if a["name"] == n]
                    code = hit[0] if hit else None
                    is_inc = code == 1
                elif src == "algara_amlani":
                    code = aax[(c["year"], st)]["seat_status"]
                    is_inc = code == ("Democratic Incumbent" if s == "D" else "Republican Incumbent")
                else:
                    code, is_inc = src, False
                if lw is None:
                    if is_inc or code in (2, 3):
                        odd.append((k3, s, n, "the last race's winner is not known"))
                    continue
                m = same_person(n, lw)
                if m == "surname":
                    odd.append((k3, s, n, f"a surname-only match with {lw}"))
                won = m in ("name", "surname")
                if won and not is_inc:
                    out.append(k3 + (s, n, code, "A", ly, lw, src))
                elif not won and (is_inc or code in (2, 3)):
                    out.append(k3 + (s, n, code, "B", ly, lw, src))
                elif won and is_inc and i and cs[i - 1]["special"]:
                    out.append(k3 + (s, n, code, "C", ly, lw, src))
    return sorted(out), odd


def join_check():
    """Whether the files' incumbency, which build_congress takes through its last-name join (cha_entry; #45), is the
    one Cha's codes give the two nominees found by their exact names (after fix_cha): {contests, agree, differ}.
    Reason (the orchestrator, 13:06): a disagreement could be "Cha's coding or your join"."""
    from build_congress import major
    cha = fix_cha(cc.read_json(os.path.join(cc.CACHE, "cha", "normalized", "contests.json"))["contests"])
    chx = collections.defaultdict(list)
    for c in cha:
        if c["office"] == "governor":
            chx[(c["year"], c["state"], bool(c["special"]))].append(c)
    n, differ = 0, []
    for f in sorted(glob.glob(os.path.join(REPO, "data", "governor", "*.json"))):
        for c in cc.read_json(f)["contests"]:
            fi = c.get("forecast_inputs") or {}
            if fi.get("incumbency_source") != "cha":
                continue
            noms = {}
            for a in c["result"]["candidates"]:
                s = major([a["party"]]) if a["party"] else None
                if s and a["votes"] and (s not in noms or a["votes"] > noms[s][1]):
                    noms[s] = (a["name"], a["votes"])
            k = (c["year"], c["place"]["state"], bool(c["special"]))
            cs = [x for x in chx[k] if not x["runoff"]] or chx[k]
            net = 0
            for s, (name, _) in noms.items():
                hit = [a["inc"] for x in cs for a in x["candidates"] if a["name"] == name]
                if not hit:
                    differ.append(f"{c['id']}: {name} not found by name in Cha")
                    break
                net += (1 if hit[0] == 1 else 0) * (1 if s == "D" else -1)
            else:
                n += 1
                if net != fi["incumbency"]:
                    differ.append(f"{c['id']}: the file {fi['incumbency']:+d}, Cha by name {net:+d}")
    return {"contests": n, "agree": n - sum(1 for d in differ if "the file" in d), "differ": differ}


# ----------------------------------------------------------------------------- the rosters
def _text(path):
    if path.endswith(".pdf"):
        t = subprocess.run(["pdftotext", path, "-"], capture_output=True, text=True, check=True).stdout
    else:
        with open(path, encoding="utf-8", errors="replace") as f:
            t = f.read()
        t = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<script.*?</script>|<style.*?</style>", " ", t)))
    return re.sub(r"\s+", " ", t)


def fetch_rosters():
    """Read each roster that answered into $CACHE/rosters/ (once; pipeline/fetch.py, 4 s per host)."""
    import fetch
    for st, (_, url, name) in ROSTERS.items():
        fetch.fetch(url, name)


def gate():
    """The source block of each roster, after finding every quote CHECKS takes from it in the file as read."""
    import fetch
    need = collections.defaultdict(list)
    for x in CHECKS.values():
        if x[4]:
            need[x[4]] += x[5]
    out = {}
    for st, (title, url, name) in ROSTERS.items():
        path = os.path.join(cc.CACHE, name)
        if not os.path.exists(path):
            raise SystemExit(f"missing {path}: run python3 pipeline/governor_incumbency.py fetch")
        t = _text(path)
        lost = [q for q in need[st] if re.sub(r"\s+", " ", q) not in t]
        if lost:
            raise SystemExit(f"governor_incumbency: {st}'s roster does not hold {lost}")
        m = fetch.meta(name)
        out[st] = {**cc.source_block(title, url, m["read_utc"], "not stated (a state's own public page)",
                                     mark="stated"),
                   "sha256": m["sha256"], "quotes": need[st]}
    unused = set(need) - set(ROSTERS)
    if unused:
        raise SystemExit(f"governor_incumbency: no roster for {unused}")
    return out


# ----------------------------------------------------------------------------- the table
def check():
    found, odd = survey()
    if odd:
        raise SystemExit(f"governor_incumbency: cases the survey cannot settle: {odd}")
    keys = {r[:4] for r in found}
    if keys != set(CHECKS):
        raise SystemExit(f"governor_incumbency: the survey finds {sorted(keys - set(CHECKS))} not in CHECKS, and "
                         f"CHECKS holds {sorted(set(CHECKS) - keys)} the survey does not find")
    for r in found:
        x = CHECKS[r[:4]]
        if (x[0], x[1]) != (r[4], r[5]):
            raise SystemExit(f"governor_incumbency: {r[:4]} is {r[4]!r} coded {r[5]!r} in the source, not "
                             f"{x[0]!r} coded {x[1]!r}")
    rosters = gate()
    joined = join_check()
    if joined["differ"]:
        raise SystemExit(f"governor_incumbency: the join and Cha's codes by name differ: {joined['differ']}")
    rows = []
    for r in found:
        y, st, sp, side, name, code, kind, ly, lw, src = r
        x = CHECKS[r[:4]]
        rows.append({"contest": cc.contest_id(y, "governor", st, special=sp), "side": side, "nominee": name,
                     "code_in_source": code, "source": src,
                     "kind": kind, "last_race": {"year": ly, "winner": lw}, "verdict": x[2], "why": x[3],
                     "roster": x[4], "fix": ({"from": x[6].get("cha", x[6].get("aa"))[0],
                                              "to": x[6].get("cha", x[6].get("aa"))[1]} if x[6] else None)})
    old = cc.read_json(TABLE) or {}
    out = {
        "written_by": "pipeline/governor_incumbency.py check",
        "asked": ASKED,
        "what": ("every governor nominee's incumbency code set against the seat's last race in the record "
                 "(data/governor/*.json, Louisiana apart); kind A: won the last race and not coded 1; kind B: coded 1 "
                 "(or Cha's 2 or 3) and did not win it; kind C: coded 1 and won it, a special election (Cha's guide "
                 "codes that 2)"),
        "rule": ("the definition of record in every year (the orchestrator, 2026-11-07 13:43 UTC): \"a successor who "
                 "was not elected to the seat is not the incumbent, and this holds in every year\"; Cha's 2 and 3 "
                 "read as not incumbents (REPORT 0.2); \"Don't add a new variant.\" Reason: \"an input has to mean "
                 "one thing in every year it is fitted on.\""),
        "codes": ("Cha, Kuriwaki and Snyder's inc, found by the nominee's exact name within Cha's contest (not "
                  "build_congress's join); Algara and Amlani's seat status before 2006 and where Cha lacks the "
                  "contest. The record counts Cha's 1 only (REPORT 2.2, 0.2)"),
        "contests_read": None,
        "counts": dict(collections.Counter(r["verdict"] for r in rows)),
        "join_check": {**joined, "what": "the files' incumbency, through build_congress's last-name join "
                                         "(cha_entry), against Cha's codes for the nominees found by exact name"},
        "checks": rows,
        "rosters": rosters,
        "rosters_not_read": ROSTERS_NOT_READ,
        "limits": ["a successor the source codes as not an incumbent cannot be found without every state's roster "
                   "(the last race shows only who won it)",
                   "a roster that gives years only (AZ 1978, AR 1994, CT 1982) does not show the day the governor "
                   "took office"],
    }
    out["contests_read"] = sum(1 for f in glob.glob(os.path.join(REPO, "data", "governor", "*.json"))
                               for c in cc.read_json(f)["contests"] if c["place"]["state"] != "LA")
    if "p_moved" in old:
        out["p_moved"] = old["p_moved"]
    cc.write_json(TABLE, out)
    print(f"{len(rows)} disagreements: {out['counts']}; rosters gated: {sorted(rosters)}")


def moves(rev):
    """Every governor p, and every model term, that differs from the files at rev: written into the table."""
    def at(path):
        r = subprocess.run(["git", "-C", REPO, "show", f"{rev}:{os.path.relpath(path, REPO)}"], capture_output=True,
                           text=True)
        return json.loads(r.stdout) if r.returncode == 0 else None

    def own(p):
        for a in (p or {}).get("alongside") or []:
            if a["under"].startswith("the model's own") and a["under"].endswith(", normal"):
                return a["value"]
        return None
    p_moved, own_moved, inputs, models = [], [], [], {}
    for f in sorted(glob.glob(os.path.join(REPO, "data", "governor", "*.json"))):
        new, old = cc.read_json(f), at(f)
        if old is None:
            continue
        oc = {c["id"]: c for c in old["contests"]}
        for c in new["contests"]:
            o = oc.get(c["id"])
            if o is None:
                continue
            a, b = (o["p"] or {}).get("value"), (c["p"] or {}).get("value")
            if a != b:
                p_moved.append({"contest": c["id"], "before": a, "after": b,
                                "ratio": (b / a) if a and b else None,
                                "under": (c["p"] or {}).get("under")})
            a2, b2 = own(o["p"]), own(c["p"])
            u = (c["p"] or {}).get("under") or ""
            if a2 != b2 and u.startswith("538"):
                own_moved.append({"contest": c["id"], "before": a2, "after": b2,
                                  "ratio": (b2 / a2) if a2 and b2 else None})
            fi0, fi1 = o.get("forecast_inputs") or {}, c.get("forecast_inputs") or {}
            if fi0.get("incumbency") != fi1.get("incumbency"):
                inputs.append({"contest": c["id"], "before": fi0.get("incumbency"), "after": fi1.get("incumbency")})
        m0, m1 = old.get("model") or {}, new.get("model") or {}
        d = {k: [m0.get(k), m1.get(k)] for k in ("b_lean", "b_inc", "b_lag", "k", "s_e")
             if m0.get(k) != m1.get(k)}
        if d:
            models[os.path.basename(f)[:-5]] = d
    rs = sorted(x["ratio"] for x in p_moved if x["ratio"])
    t = cc.read_json(TABLE)
    t["p_moved"] = {"against": rev, "incumbency_moved": inputs, "p": p_moved,
                    "p_ratio": ({"n": len(rs), "min": rs[0], "median": rs[len(rs) // 2], "max": rs[-1]} if rs else None),
                    "model_own_beside_538": own_moved, "models": models}
    cc.write_json(TABLE, t)
    print(f"incumbency moved in {len(inputs)} contests; p moved in {len(p_moved)}"
          + (f" (ratio {rs[0]:.4f} to {rs[-1]:.4f}, median {rs[len(rs) // 2]:.4f})" if rs else "")
          + f"; the model's own beside 538 moved in {len(own_moved)}; model terms moved in {len(models)} files")


if __name__ == "__main__":
    if sys.argv[1:2] == ["fetch"]:
        fetch_rosters()
    elif sys.argv[1:2] == ["check"]:
        check()
    elif sys.argv[1:2] == ["moves"] and len(sys.argv) == 3:
        moves(sys.argv[2])
    else:
        raise SystemExit(__doc__)
