"""pipeline/local_va.py: Virginia's local contests and questions of 2023, from the Department of Elections' results as
read before it refused us (pipeline/intake/va_elect.py), gated within the certifying source, in the shape
pipeline/local_medsl.py reads (medsl_shape), as Louisiana's 2023 are (pipeline/local_la.py).

Written 2026-11-13 by worker D3 (briefs/D3-data-local.md, step 2), the queue's next item after the district checks
(handoff/workers/D3.md): data/local/REPORT.md section 28 said of the 2023 file, "The same 2023 file also holds
Virginia's 2023 local contests (clerks, Commonwealth's attorneys, sheriffs, boards of supervisors, school boards, town
councils), already in the cache from before the refusal. They are not taken in here. They could be, with nothing
requested." Reason: the orchestrator's order of 2026-11-07 10:35 and Zach's 03:13 word, as much data as can be found.
Nothing is requested from the Department: it refused us at 2026-11-07 18:27:48 UTC, and what was read before stands
(the orchestrator, 18:30).

What the file holds [measured: the cached Media Export, export-2023-Nov-Gen.json, read 2026-11-07 18:23:02 UTC]:
  - its statewide list (results.ballotItems, 183 contests): the legislature's 140 (pipeline/local_va_leg.py) and 43
    local contests on more than one locality's ballot (the clerks, Commonwealth's attorneys and sheriffs a county
    shares with a city, James City County's and Williamsburg's treasurer, and the towns of Brodnax, Scottsville and
    St. Paul, which lie in two counties each), each with its statewide count and each locality's line. The page shows
    all 183, each with its "Winner" mark;
  - each locality's own list (localResults, 133 counties and independent cities): those contests' lines, and 1,405
    contests on one locality's ballot alone (1,396 for offices, 9 questions), each with its locality's count, option
    by option, and its precincts' lines. The page does not show these, so no "Winner" mark of theirs was seen: the
    winners are the leading candidates for the seats [inferred], and the record says so (the orchestrator, 18:32: "a
    figure resting on a page we saw and one resting on a rule we applied must look different in the record").
  - no candidate's party in any local contest: the file's politicalParty is empty for every local option and the
    page prints none [measured]: the Code of Virginia gives a candidate's party on the ballot for federal, statewide
    and General Assembly offices only (section 24.2-613 B, CODE_613). The record shows no party, and the method's
    class reads "party not given in the source" (pipeline/local_medsl.py PARTY_NOT_GIVEN), its reason naming that
    section; except a school board's contests, whose candidates the Code has "nominated only by petition" (section
    22.1-57.3 E, CODE_NONPARTISAN), so no party nominates them: classed nonpartisan and pooled with the nonpartisan
    like races of their office and seats (the orchestrator, 2026-11-13 00:55 (c) and 07:48).
  - three kinds of option: an option the file numbers ("cs" and a number) is a name on the ballot; "wi-" and the
    contest's number is the write-in line; an option the file keys by a name ("TakeraN.Walker-3-") is a write-in
    candidate counted by name: the two such options in contests the page shows (Brodnax's and Scottsville's councils)
    each sit there beside an "Adjudicated Write-Ins" line of the same votes [inferred from those two; measured: their
    votes]. So such an option is read as a write-in, not as a name on the ballot.

Each contest: its office and district from its title ("Member Board of Supervisors (Cloyd District)": the office,
then the district; "Sheriff (Goochland County)": the office, then the locality's name, so no district); its seats, the
file's voteFor [stated]; special where its title says "Special" [stated]; its localities' FIPS codes from the
county_name and county_fips columns of MEDSL's 2024 Virginia precinct file, matched by name, each the state's code 51
and the locality's own code in the file [measured: all 133].

The gate within the certifying source (2023 has no federal or statewide contest on its ballot) [proposed, for the
orchestrator's ruling; it extends the gate ruled for the 2023 legislature at 18:49, pipeline/local_va_leg.py]:
  (a) the year: the election's page, rendered, is headed "OFFICIAL RESULTS", the Department's results page links it
      by its Election Results Directory, and its "Media Export" link is the file read (local_va_leg.gate(2023)["year"],
      the legislature's own); a contest on the page: its candidates and votes are the file's;
  (b) a contest on more than one locality's ballot: its locality lines add up, option by option, to its statewide
      count, and no locality line names an option the statewide count lacks; a contest on one locality's ballot: its
      count is that locality's line, so there is nothing to add up;
  (c) a contest on more than one locality's ballot: as many locality lines as the page prints ("Localities reporting
      n/n", all reporting); one on one locality's ballot: all its precincts reporting (the file's precinctsReporting
      equal to its precinctsParticipating) and its locality's every reporting group "Fully Reported";
  (d) the over-ballot test within the locality, as the orchestrator's of 17:44 for statewide contests ("hold one
      that exceeds the day's highest-vote statewide contest by more than 10%, and list for me any between 1.0x and
      1.1x"; and 21:55: every count shown is tested whatever its source): the file gives no ballots cast, so a
      contest's votes for each seat (all its lines, write-ins too, over its seats; a question's yes and no) against
      the highest-vote contest of the locality's whole ballot (_tops: each chamber's lines in the locality summed, and
      each other contest of one seat or question put to the whole locality). Held above OVER_LINE times it; listed
      between 1.0 and OVER_LINE. For a contest on more than one locality's ballot, each of its locality lines is
      read so.
  A contest that fails (a)'s last part, (b), (c) or (d) is held; a year that fails the rest of (a) holds all.
  Recorded beside it, not a gate (as for the legislature): each option's precinct lines add up to its locality line
  (not so in some localities, noted on the record).

  check()  the gate: data/local/check-va-local.json.

Run:  VOTE_CACHE=/tmp/vote-cache python3 -I pipeline/local_va.py check
"""
import collections
import csv
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fetch as F  # noqa: E402
from intake import va_elect as VA  # noqa: E402
import local as L  # noqa: E402
import local_va_leg as VAL  # noqa: E402

YEARS = (2023, 2025)   # 2025: the orchestrator, 2026-11-13 00:55 (e): "2025's 564 local contests from the cache, same
#                        gate and rulings, own PR. Scope is every level"
SOURCE_KEY = "va_elect"
EXPORT = {y: f"{VA.RAW}/export-{VA.ELECTION[y]}.json" for y in YEARS}
MEDSL_FIPS_FILE = os.path.join("medsl", "raw", "2024-13731156-2024-va-precinct-general.csv")
CHECK = os.path.join(L.REPO, "data", "local", "check-va-local.json")
OVER_LINE = 1.10   # pipeline/local_medsl.py OVER_TOP: a small excess over another contest can be real
OVER_LINE_UNOPPOSED = 1.50   # against an unopposed comparator (the orchestrator, 2026-11-13 00:55 (b), OVER_UNOPPOSED)
# (b) The orchestrator, 2026-11-13 00:55: "A refinement at every level. An unopposed comparator undercounts ballots by
# roll-off, often 10 to 30%. Against one, list up to 1.5 and hold only above 1.5; a two-seat race filed as one still
# reads near 2.0 and is caught. So Halifax's and Cumberland's sheriffs and Norton's clerk are listed, the comparator
# named in the note." A contest is read, as before, against its locality's highest-vote figure; where that figure is
# unopposed, it is held only above OVER_LINE_UNOPPOSED and listed between 1 and that line, and the note names the
# figure as unopposed. A figure is unopposed where its contest has no more names on the ballot than seats (write-in
# lines aside), and a
# chamber's lines summed are unopposed where any of the chamber's contests in the locality is [worker D3's reading:
# its voters there who skip that contest are missing from the sum].

# (c) The orchestrator, 2026-11-13 00:55: "The 519 stay without p, reason "party not given in the source". Like races
# must be like in party status. Pooling a race of unknown party with partisan or nonpartisan ones uses another kind of
# race's spread. One exception: where the Code of Virginia puts an office on the ballot without party (school board,
# for one), read that section once at law.lis.virginia.gov and name it." Read once (2026-11-13 07:42:41 UTC): the
# Code's Form of ballot, whose subsection B gives a candidate's party on the ballot for three kinds of office alone
# (CODE_613["words"]) [stated], so every local office is on the ballot without party. That reached all 519, and the
# orchestrator narrowed the rule (07:48): "a contest is nonpartisan only where the Code says parties may not nominate
# for that office. Being unlabeled on the ballot is not enough. You may read up to two more sections at
# law.lis.virginia.gov: the one on how school board candidates are nominated, and the one on soil and water
# conservation directors. Name each section and quote its words. Where a section bars party nomination, class that
# office's contests nonpartisan and pool them with nonpartisan like races of the same office and seats ... Every other
# office stays "party not given in the source", with § 24.2-613 B named in the reason as why the source prints no
# party." Read, one request each, the article page that holds the section (2026-11-13 07:50):
#   - school boards: section 22.1-57.3 E (Election of school board members): "In order to have their names placed on
#     the ballot, all candidates shall be nominated only by petition as provided by general law pursuant to
#     § 24.2-506." [stated] "Only by petition" leaves no party nomination, so a school board's contests are
#     nonpartisan [worker D3's reading of "bars"];
#   - soil and water conservation directors: section 10.1-523 A (Nominating petitions): "nominating petitions,
#     statements of qualifications, and declarations of candidacy shall be filed with the general registrar ... to
#     nominate candidates for elected directors of such districts" [stated]. It names petitions as the way to
#     nominate, but not as the only way, and says nothing of parties, so it is not read as a bar [worker D3's
#     reading; for the orchestrator]: the directors' contests stay "party not given in the source".
CODE_613 = {"section": "Code of Virginia, section 24.2-613 (Form of ballot), subsection B",
            "url": "https://law.lis.virginia.gov/vacode/title24.2/chapter6/section24.2-613/",
            "cache": os.path.join("va_code", "section24.2-613.html"),
            "words": "For elections for federal, statewide, and General Assembly offices only, each candidate who has "
                     "been nominated by a political party or in a primary election shall be identified by the name of "
                     "his political party."}
CODE_NONPARTISAN = {
    "school board": {"section": "Code of Virginia, section 22.1-57.3 (Election of school board members; election of "
                                "tie breaker), subsection E",
                     "url": "https://law.lis.virginia.gov/vacodefull/title22.1/chapter5/article7/",
                     "cache": os.path.join("va_code", "title22.1-chapter5-article7.html"),
                     "words": "In order to have their names placed on the ballot, all candidates shall be nominated "
                              "only by petition as provided by general law pursuant to § 24.2-506.",
                     "match": re.compile(r"\bSCHOOL BOARD\b", re.I)}}
CODE_READ_NOT_BAR = {"section": "Code of Virginia, section 10.1-523 (Nominating petitions; posting of notice), "
                                "subsection A",
                     "url": "https://law.lis.virginia.gov/vacodefull/title10.1/chapter5/article3/",
                     "cache": os.path.join("va_code", "title10.1-chapter5-article3.html"),
                     "words": "to nominate candidates for elected directors of such districts"}
WHY_NO_PARTY = ("the source prints no party because the Code of Virginia, section 24.2-613 B, gives a candidate's "
                "party on the ballot \"For elections for federal, statewide, and General Assembly offices only\" "
                "({url}, read {read}, sha256 {sha}) [stated]; the ballot's label is not the office's party status, so "
                "the contest is not pooled with partisan or nonpartisan races (the orchestrator, 2026-11-13 07:48)")
# The orchestrator, 2026-11-13 08:07: "VA 2025's "Chairman School Board" goes with the school boards. § 22.1-57.3:3 B
# makes the chairman the at-large member elected under § 22.1-57.3, so subsection E's petition-only rule reaches it."
# Section 22.1-57.3:3 is printed on the article page read for section 22.1-57.3 (its sha256 is checked with E's words).
# Its subsection A confines it to counties with the county executive form that border an urban county executive
# county [stated], which Prince William (2023's chairman) is and Page (2025's) is not [inferred]; Page's chairman is
# read as a member of its elected school board, elected under section 22.1-57.3, so E reaches it all the same
# [inferred; for the orchestrator].
CHAIR_SCHOOL = re.compile(r"\bCHAIRMAN\b.*\bSCHOOL BOARD\b", re.I)
CHAIR_WORDS = ("The member of the school board who is elected at large at the initial or any subsequent election shall "
               "be the chairman of the school board during his term of office")
CHAIR_NOTE = ("the chairman of the school board is a member of the elected school board, elected under section "
              "22.1-57.3, so its subsection E reaches the chairman's contest: in the counties section 22.1-57.3:3 "
              "governs, its subsection B says \"{words}\" [stated], and elsewhere the chairman elected by the voters is "
              "read as the at-large member [inferred] (the orchestrator, 2026-11-13 08:07)")
NONPARTISAN_NOTE = ("nonpartisan: the {section} says \"{words}\" ({url}, read {read}, sha256 {sha}) "
                    "[stated], so no party nominates for this office; classed nonpartisan and pooled with the "
                    "nonpartisan like races of its office and seats (the orchestrator, 2026-11-13 00:55 (c) and "
                    "07:48)")


def _code_text(entry):
    """The cached page's text, tags and whitespace aside, and its meta; a SystemExit if it lacks the words quoted."""
    import html as _html
    m = F.meta(entry["cache"])
    with open(os.path.join(F.CACHE, entry["cache"]), encoding="utf-8") as f:
        text = " ".join(_html.unescape(re.sub(r"<[^>]+>", " ", f.read())).split())
    text = re.sub(r" ([.,;:])", r"\1", text)   # a linked section number leaves a space before its stop
    if entry["words"] not in text:
        raise SystemExit(f"local_va: the cached {entry['section']} does not hold the words quoted")
    return text, m


def code_reads():
    """(why the source prints no party, {office type: (match, its note)}), from the sections as read."""
    _, m = _code_text(CODE_613)
    why = WHY_NO_PARTY.format(url=CODE_613["url"], read=m["read_utc"], sha=m["sha256"])
    _code_text(CODE_READ_NOT_BAR)
    nonp = {}
    for k, e in CODE_NONPARTISAN.items():
        text, me = _code_text(e)
        if k == "school board" and CHAIR_WORDS not in text:
            raise SystemExit("local_va: the cached school board article does not hold section 22.1-57.3:3 B's words")
        nonp[k] = (e["match"], NONPARTISAN_NOTE.format(section=e["section"], words=e["words"], url=e["url"],
                                                       read=me["read_utc"], sha=me["sha256"]))
    return why, nonp


BALLOT_ID = re.compile(r"cs\d+")
WRITE_IN_ID = re.compile(r"wi-")
SPECIAL = re.compile(r"\bSPECIAL\b", re.I)
GATE_BY = VAL.GATE_BY   # 2023: no federal or statewide contest on the ballot; 2025: its Governor equal to D2's
RULED = ("proposed by worker D3; the orchestrator, 2026-11-13 00:55 (a): \"Agreed as proposed: the legislature's gate, "
         "plus the over-ballot test per locality against the ballot's highest-vote contest (held above 1.1, listed "
         "above 1.0)\"; (b): against an unopposed one, held above 1.5 and listed up to it")
WINNER_NOTE = ("the winners are the leading candidates for the seats [inferred]: the Department's file marks no "
               "winner, and its results page as read shows the contests on more than one locality's ballot, not this "
               "one, so no 'Winner' mark of it was seen")


def _key(name):
    s = re.sub(r" COUNTY$", "", name.upper().replace("&", "AND"))
    return re.sub(r"[^A-Z]", "", s)


def locality_fips():
    """Locality names to FIPS codes, from the county_name and county_fips columns of MEDSL's 2024 Virginia file."""
    m = collections.defaultdict(set)
    with open(os.path.join(F.CACHE, MEDSL_FIPS_FILE), newline="") as f:
        for row in csv.DictReader(f):
            m[_key(row["county_name"])].add(row["county_fips"])
    return {k: v.pop() for k, v in m.items() if len(v) == 1}, F.meta(MEDSL_FIPS_FILE)


def fips_source():
    _, fm = locality_fips()
    return F.source("locality FIPS codes: the county_name and county_fips columns of MEDSL's 2024 Virginia precinct "
                    "file, matched by name to the Department's localities", fm["url"], fm["read_utc"], "CC0 1.0",
                    mark="stated", note="each the state's code 51 and the locality's own code in the Department's "
                                        "file [measured: all 133]")


_READ = {}


def read(year):
    """The year's local contests, gated: [contest] in this module's own shape (once a run)."""
    if year not in _READ:
        _READ[year] = _read(year)
    return _READ[year]


def _title(name, localities):
    """(office, district) from a contest's title: the last bracket is the district, unless it names the contest's
    localities."""
    t = " ".join(name.split()).strip()
    m = re.fullmatch(r"(.*?)\s*\(([^()]*)\)", t)
    if not m:
        return t.rstrip("."), ""
    office, inner = m.group(1).rstrip(" ."), m.group(2).strip()
    names = {_key(x) for x in inner.split(",")}
    return office, "" if names <= {_key(x) for x in localities} else inner


WINNER_NOTE_UNSHOWN = ("the winners are the leading candidates for the seats [inferred]: the Department's file marks "
                       "no winner, and its results page as read (its first 50 contests) does not show this one, so no "
                       "'Winner' mark of it was seen")
NAMED_NOTE = ("the file keys {who} by a name, not by a ballot number: read as a write-in counted by name [inferred], "
              "as the page confirms in the two contests it shows with such options (Brodnax's and Scottsville's "
              "councils, each beside an 'Adjudicated Write-Ins' line of the same votes)")
NAMED_UNCONFIRMED = ("the page does not show this contest, and the name-keyed {who} outpolls a name on the ballot "
                     "({ballot}) for a seat, so its being a write-in is not confirmed here; it stays not computed "
                     "either way: as a write-in by the write-in rule, as a name on the ballot for having no party in "
                     "the source (the orchestrator, 2026-11-13 01:20)")


def _option(o):
    oid = o["id"]
    kind = "ballot" if BALLOT_ID.fullmatch(oid) else "write-in line" if WRITE_IN_ID.match(oid) else \
        "write-in by name" if not oid.startswith("bms") else "question"
    return {"name": o["name"].strip(), "votes": o["voteCount"], "kind": kind, "party": o.get("politicalParty")}


def _read(year):
    if load_export(year) is None:
        return None
    x, meta = load_export(year)
    fips, _ = locality_fips()
    names = {lr["id"]: lr["name"].title() for lr in x["localResults"]}
    for lid, n in names.items():
        if fips.get(_key(n)) != "51" + lid:
            raise SystemExit(f"local_va {year}: {n} ({lid}) is not FIPS 51{lid} in MEDSL's file")
    state_items = {b["id"]: b for b in x["results"]["ballotItems"]}
    norm = {c["title"]: c for c in VAL.load(year)["contests"]}
    full = {lr["id"]: all(s["status"] == "Fully Reported" for s in lr["reportingStatuses"]) for lr in x["localResults"]}
    out = []
    tops = {lr["id"]: _tops(lr) for lr in x["localResults"]}   # (d): each locality's figures to test against
    by_item = collections.defaultdict(list)
    for lr in x["localResults"]:
        for b in lr["ballotItems"]:
            by_item[b["id"]].append((lr, b))
    for iid, parts in by_item.items():
        b0 = parts[0][1]
        if iid in state_items and b0["name"].startswith("Member, "):
            continue   # the legislature: pipeline/local_va_leg.py
        if iid in state_items and " ".join(b0["name"].split()).upper() == "GOVERNOR":
            continue   # D2's (data/governor/2025.json), against which the year is gated
        shared = iid in state_items
        if not shared and len(parts) != 1:
            raise SystemExit(f"local_va {year}: {b0['name']} is on {len(parts)} localities' lists, not the state's")
        lids = sorted(lr["id"] for lr, _ in parts)
        office, district = _title(b0["name"], [names[i] for i in lids])
        sb = state_items.get(iid)
        opts = [_option(o) for o in (sb or b0)["ballotOptions"]]
        c = {"item": iid, "title": " ".join(b0["name"].split()), "office": office.upper(), "district": district,
             "office_title": office,
             "seats": b0["voteFor"], "question": b0["contestType"] == "BallotMeasure",
             "special": bool(SPECIAL.search(b0["name"])), "localities": lids,
             "counties": sorted("51" + i for i in lids), "options": opts, "shared": shared,
             # a statewide office (2025's Lieutenant Governor and Attorney General), on every locality's ballot: the
             # state's other offices are written with the local records, as MEDSL's are (local_medsl.is_local_level)
             "statewide": shared and len(parts) == len(x["localResults"])}
        why, notes, ok = [], [], {}
        if shared:
            n = norm[sb["name"].strip()]
            c["page"] = n["page"]
            won = {o["name"] for o in n["options"] if o.get("winner_marked")}
            for o in opts:
                o["winner_marked"] = o["name"] in won
            shown = n["page"]["shown"]
            ok["page_equal"], ok["parts_add_up"] = n["page"]["equal"] if shown else None, n["parts_add_up"]
            if shown and not n["page"]["equal"]:
                why.append("the page shows other candidates or votes than the file holds")
            if not n["parts_add_up"]:
                why.append("its locality lines count " + "; ".join(
                    f"{e['votes']:,} votes for {e['name']} (in {', '.join(e['localities'])})"
                    for e in n["extra_in_localities"]) + ", whom its statewide count does not hold"
                    if n["extra_in_localities"] else "its locality lines do not add up to its statewide count")
            if shown:
                a, _, t = (n["page"]["localities_reporting"] or "/").partition("/")
                ok["all_reporting"] = a == t == str(n["localities"])
                if not ok["all_reporting"]:
                    why.append(f"the page prints 'Localities reporting {n['page']['localities_reporting']}', and the "
                               f"file has {n['localities']} locality lines")
            else:   # 2025's page as read shows its first 50 contests: (c) as for a one-locality contest, line by line
                ok["all_reporting"] = all(b_["precinctsReporting"] == b_["precinctsParticipating"] and full[lr_["id"]]
                                          for lr_, b_ in parts)
                if not ok["all_reporting"]:
                    why.append("not all reporting in " + ", ".join(
                        f"{lr_['name'].title()} ({b_['precinctsReporting']} of {b_['precinctsParticipating']} "
                        f"precincts, its groups {[s['status'] for s in lr_['reportingStatuses']]})"
                        for lr_, b_ in parts if not (b_["precinctsReporting"] == b_["precinctsParticipating"]
                                                     and full[lr_["id"]])))
                if not c["question"]:
                    notes.append(WINNER_NOTE_UNSHOWN)
            short = n["precincts_short"]
        else:
            lr, b = parts[0]
            ok["page_equal"], ok["parts_add_up"] = None, None
            ok["all_reporting"] = b["precinctsReporting"] == b["precinctsParticipating"] and full[lr["id"]]
            if not ok["all_reporting"]:
                why.append(f"not all reporting: {b['precinctsReporting']} of {b['precinctsParticipating']} precincts, "
                           f"its locality's groups {[s['status'] for s in lr['reportingStatuses']]}")
            short = [{"locality": lr["name"].title(), "option": o["name"].strip(), "locality_line": o["voteCount"],
                      "precincts": sum(p["voteCount"] for p in o["precinctResults"] or [])}
                     for o in b["ballotOptions"]
                     if o["precinctResults"] is None or sum(p["voteCount"] for p in o["precinctResults"]) != o["voteCount"]]
            if not c["question"]:
                notes.append(WINNER_NOTE)
        # (d) the over-ballot test within the locality, each locality line read
        over = []
        for lr, b in parts:
            v = sum(o["voteCount"] for o in b["ballotOptions"])
            mine = v / (b["voteFor"] or 1) if not c["question"] else v
            others = [t for t in tops[lr["id"]] if t[2] != iid]
            top, name, _, un = max(others) if others else (None, None, None, False)
            r = mine / top if top else None
            over.append({"locality": lr["name"].title(), "votes_per_seat": round(mine, 1), "top": top,
                         "top_name": name, "top_unopposed": un, "line": OVER_LINE_UNOPPOSED if un else OVER_LINE,
                         "ratio": None if r is None else round(r, 4)})
        read_ = [o for o in over if o["ratio"] is not None]
        # the locality line shown: one over its line if any (the furthest over it), else the highest ratio
        worst = max(read_, key=lambda o: (o["ratio"] > o["line"], o["ratio"] / o["line"] if o["ratio"] > o["line"]
                                          else o["ratio"]), default=None)
        c["over_ballot"] = {"worst": worst, "verdict": "untested" if worst is None else
                            "held" if worst["ratio"] > worst["line"] else "listed" if worst["ratio"] > 1 else "passes"}
        if worst is not None:
            unop = (f", unopposed (an unopposed contest loses its voters who skip it, so the line against it is "
                    f"{OVER_LINE_UNOPPOSED} times: the orchestrator, 2026-11-13 00:55 (b))" if worst["top_unopposed"]
                    else "")
            what = (f"its {worst['votes_per_seat']:,.0f} votes for each seat in {worst['locality']} are "
                    f"{worst['ratio']:.3f} times the {worst['top']:,} of {worst['top_name']}, the highest-vote "
                    f"contest of that locality's whole ballot{unop}")
        if c["over_ballot"]["verdict"] == "held":
            why.append(f"{what}: more than the {worst['line']} times a count can reach [measured]")
        elif c["over_ballot"]["verdict"] == "listed":
            notes.append(f"the over-ballot test within the locality: {what}; between 1.0 and {worst['line']} times, "
                         f"which can be real, so kept and listed [measured]")
        if short:
            notes.append("the precinct lines do not add up to the locality line for "
                         + "; ".join(f"{s['option']} in {s['locality']} ({s['precincts']:,} against "
                                     f"{s['locality_line']:,})" for s in short[:4])
                         + (f"; and {len(short) - 4} more" if len(short) > 4 else "")
                         + " [measured]; the locality line is the count (recorded beside the gate, not a part of it)")
        # the write-in by name reading (the orchestrator, 2026-11-13 (d): "Each record it touches says so in its note
        # and names the two contests the page confirms"; 01:20: where the page does not show the contest and the
        # name-keyed option outpolls a ballot name, "its being a write-in is not confirmed there")
        wn = [o for o in opts if o["kind"] == "write-in by name"]
        if wn:
            notes.append(NAMED_NOTE.format(who=", ".join(f"{o['name']} ({o['votes']:,})" for o in wn)))
            ballot_ = [o for o in opts if o["kind"] == "ballot"]
            k = c["seats"] or 1
            lead = sorted(ballot_ + wn, key=lambda o: -o["votes"])[:k]
            beat = [o for o in wn if o in lead and o["votes"] > 0]
            if beat and len(ballot_) >= k:
                last = min((o for o in ballot_ if o not in lead), key=lambda o: -o["votes"], default=None)
                c["named_write_in_wins"] = [o["name"] for o in beat]
                if not shared:
                    notes.append(NAMED_UNCONFIRMED.format(who=", ".join(f"{o['name']} ({o['votes']:,})" for o in beat),
                                                          ballot=f"{last['name']} ({last['votes']:,})" if last else "a "
                                                          "name on the ballot"))
        c["precincts_short"] = short
        c["checks"] = ok
        c["held"] = "; ".join(why) or None
        c["notes"] = notes
        out.append(c)
    return out


LEG_TITLE = re.compile(r"Member, (Senate of Virginia|House of Delegates) \(")
POSS = {"Senate of Virginia": "the Senate of Virginia's", "House of Delegates": "the House of Delegates'"}


def _tops(lr):
    """(d): the figures a locality's contests are tested against, [(votes, name, item id)]: each chamber's lines in the
    locality summed (every voter there has one senator and one delegate), and each other contest of one seat, and each
    question, put to the whole locality (its precincts all the locality's: the most precincts of any contest there).
    A contest of several seats is no figure (a voter may use fewer votes than seats), nor is one of part of the
    locality."""
    n = max(b["precinctsParticipating"] or 0 for b in lr["ballotItems"])
    out, cham, cham_un = [], collections.Counter(), set()
    for b in lr["ballotItems"]:
        v = sum(o["voteCount"] for o in b["ballotOptions"])
        names = sum(1 for o in b["ballotOptions"] if BALLOT_ID.fullmatch(o["id"]))
        unopposed = b["contestType"] != "BallotMeasure" and names <= (b["voteFor"] or 1)   # (b)
        m = LEG_TITLE.match(b["name"])
        if m:
            cham[m.group(1)] += v
            if unopposed:
                cham_un.add(m.group(1))
        elif (b["voteFor"] == 1 or b["contestType"] == "BallotMeasure") and b["precinctsParticipating"] == n:
            out.append((v, " ".join(b["name"].split()), b["id"], unopposed))
    out += [(v, f"{POSS[ch]} lines in {lr['name'].title()}, summed", None, ch in cham_un) for ch, v in cham.items()]
    return out


def load_export(year):
    name = EXPORT.get(year)
    if not name or not os.path.exists(os.path.join(F.CACHE, name)):
        return None
    with open(os.path.join(F.CACHE, name)) as f:
        return json.load(f), F.meta(name)


def _year_gate(year):
    return VAL.gate(year)["year"]


def _gate_record(c, year):
    g = _year_gate(year)
    rec = {"by": GATE_BY[year], "ruled": RULED, "official": g[0],
           "official_how": "the results site's page of the election, rendered, headed 'OFFICIAL RESULTS', and linked "
                           "from the Department's results page by its Election Results Directory",
           "shared": c["shared"], "page_equal": c["checks"]["page_equal"],
           "parts_add_up": c["checks"]["parts_add_up"], "all_reporting": c["checks"]["all_reporting"],
           "over_ballot": c["over_ballot"]["verdict"],
           "precincts_add_up": not c["precincts_short"]}
    if c["over_ballot"]["worst"]:
        rec["over_ballot_ratio"] = c["over_ballot"]["worst"]["ratio"]
    return rec


def medsl_shape(year):
    """Virginia's local contests and questions of `year` in local_medsl's load() shape (as local_la.medsl_shape), each
    with the gate within the certifying source (source_gate); None if the file is not in the cache."""
    if year not in YEARS or read(year) is None:
        return None
    _, meta = load_export(year)
    g = _year_gate(year)
    why_no_party, nonp = code_reads()
    out = []
    for c in read(year):
        held = (f"held by the gate: {g[1]}" if not g[0] else f"held by the gate: {c['held']}" if c["held"] else None)
        base = {"state": "VA", "date": VAL.load(year)["date"][:10], "stage": "GEN", "special": c["special"],
                "subject": None, "precincts": None, "counties": c["counties"], "source": SOURCE_KEY, "id_date": False,
                "file": {"name": meta["url"].rsplit("/", 1)[1], "url": meta["url"], "read_utc": meta["read_utc"],
                         "sha256": meta["sha256"]},
                "source_gate": {"held": held, "record": _gate_record(c, year)},
                "dataverse": "LOCAL", "office": c["office"], "office_title": c["office_title"],
                "district": c["district"]}
        if c["notes"]:
            base["notes"] = list(c["notes"])
        if c["question"]:
            out.append(dict(base, magnitude=None, question=True, question_type=None,
                            candidates=[{"name": o["name"].upper(), "votes": o["votes"]} for o in c["options"]]))
            continue
        cands = []
        for o in c["options"]:
            x = {"name": o["name"], "votes": o["votes"], "as_named": True,
                 "party": VAL.PARTY.get(o["party"] or "", (o["party"] or "").upper()) if c["statewide"] else None,
                 "writein": o["kind"] != "ballot"}
            if c["shared"]:
                x["won_marked"] = True if o["winner_marked"] else None
            cands.append(x)
        hit = [note for match, note in nonp.values() if match.search(c["office"])]
        if hit and CHAIR_SCHOOL.search(c["office"]):
            hit.append(CHAIR_NOTE.format(words=CHAIR_WORDS))
        if c["statewide"]:   # a statewide office's ballot names its candidates' parties (section 24.2-613 B)
            out.append(dict(base, magnitude=c["seats"], question=False, candidates=cands, dataverse="STATE"))
        elif hit:
            out.append(dict(base, magnitude=c["seats"], question=False, candidates=cands, party_not_given=False,
                            notes=list(base.get("notes") or []) + hit))
        else:
            out.append(dict(base, magnitude=c["seats"], question=False, candidates=cands, party_not_given=True,
                            party_not_given_why=why_no_party))
    return out


def source_block(year):
    res = VAL.load(year)
    fx, fp = res["files"]["export"], res["files"]["election"]
    note = (f"the results site's page of '{res['name']}' ({fp['url']}, {fp['how']}, finished {fp['finished_utc']}, "
            f"sha256 {fp['sha256']}; headed {res['official_text']!r}) and its 'Media Export' file ({fx['url']}, "
            f"finished {fx['finished_utc']}, sha256 {fx['sha256']}, created {res['export_created_utc'][:19]}Z), "
            f"read by pipeline/intake/va_elect.py before the Department refused us (2026-11-07 18:27:48 UTC; nothing "
            f"is requested from it again). Gate {GATE_BY[year]} (pipeline/local_va.py; data/local/check-va-local.json), "
            f"proposed: the page headed 'OFFICIAL RESULTS' and linked from the Department's results page, the figures "
            f"it shows the file's, a shared contest's locality lines adding up to its statewide count and as many as "
            f"the page prints, a one-locality contest all reporting, and the over-ballot test within each locality. "
            f"The file gives no party for any local candidate (the Code of Virginia, section 24.2-613 B, prints a "
            f"party on the ballot for federal, statewide and General Assembly offices only), and marks no winner; the "
            f"page marks the shared contests' winners")
    return F.source(f"Virginia Department of Elections, results of the {res['name']}, {res['date']}: local offices "
                    f"and questions", fp["url"], fx["read_utc"], VA.LICENCE, mark="stated",
                    via="pipeline/intake/va_elect.py", note=note, sha256=fx["sha256"])


def check():
    out = {"about": "the gate within the certifying source of Virginia's 2023 local contests and questions "
                    "(pipeline/local_va.py, docstring), proposed by worker D3 on 2026-11-13: (a) the election's page "
                    "headed 'OFFICIAL RESULTS', linked from the Department's results page, its Media Export link the "
                    "file read, and the figures it shows the file's; (b) a shared contest's locality lines adding up "
                    "to its statewide count; (c) all reporting; (d) the over-ballot test within each locality. Held "
                    "where a part fails. Beside it: precinct lines against locality lines. Built by "
                    "pipeline/local_va.py check.",
           "years": {}}
    for y in YEARS:
        cs = read(y)
        if cs is None:
            continue
        g = _year_gate(y)
        t = collections.Counter()
        for c in cs:
            t[("shared" if c["shared"] else "one locality") + (", question" if c["question"] else "")] += 1
            t["held" if c["held"] or not g[0] else "kept"] += 1
            t[f"over-ballot: {c['over_ballot']['verdict']}"] += 1
            t["write-in by name" if any(o["kind"] == "write-in by name" for o in c["options"]) else
              "no write-in by name"] += 1
            if c["precincts_short"]:
                t["precinct lines short of the locality line (noted)"] += 1
        out["years"][str(y)] = {
            "year_gate": {"passes": g[0], "words": g[1]}, "tallies": dict(sorted(t.items())),
            "held": [{"title": c["title"], "localities": c["localities"], "why": c["held"]} for c in cs if c["held"]],
            "listed": [{"title": c["title"], **c["over_ballot"]["worst"]} for c in cs
                       if c["over_ballot"]["verdict"] == "listed"],
            "precincts_short": [{"title": c["title"], "lines": c["precincts_short"]} for c in cs
                                if c["precincts_short"]],
            "over_ballot_highest": sorted(({"title": c["title"], **c["over_ballot"]["worst"]} for c in cs
                                           if c["over_ballot"]["worst"]), key=lambda r: -r["ratio"])[:25]}
    with open(CHECK, "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
        f.write("\n")
    for y, r in out["years"].items():
        print(y, json.dumps(r["tallies"]))
    return out


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        check()
    else:
        raise SystemExit(__doc__)
