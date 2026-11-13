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
    page prints none [measured]. The record shows no party, and the method's class reads "party not given in the
    source" (pipeline/local_medsl.py PARTY_NOT_GIVEN), never "nonpartisan".
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

YEARS = (2023,)
SOURCE_KEY = "va_elect"
EXPORT = {2023: f"{VA.RAW}/export-{VA.ELECTION[2023]}.json"}
MEDSL_FIPS_FILE = os.path.join("medsl", "raw", "2024-13731156-2024-va-precinct-general.csv")
CHECK = os.path.join(L.REPO, "data", "local", "check-va-local.json")
OVER_LINE = 1.10   # pipeline/local_medsl.py OVER_TOP: a small excess over another contest can be real
BALLOT_ID = re.compile(r"cs\d+")
WRITE_IN_ID = re.compile(r"wi-")
SPECIAL = re.compile(r"\bSPECIAL\b", re.I)
GATE_BY = "within the certifying source (no federal or statewide contest on the ballot)"
RULED = "proposed by worker D3, 2026-11-13; for the orchestrator's ruling"
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


def _option(o):
    oid = o["id"]
    kind = "ballot" if BALLOT_ID.fullmatch(oid) else "write-in line" if WRITE_IN_ID.match(oid) else \
        "write-in by name" if not oid.startswith("bms") else "question"
    return {"name": o["name"].strip(), "votes": o["voteCount"], "kind": kind}


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
             "counties": sorted("51" + i for i in lids), "options": opts, "shared": shared}
        why, notes, ok = [], [], {}
        if shared:
            n = norm[sb["name"].strip()]
            c["page"] = n["page"]
            won = {o["name"] for o in n["options"] if o.get("winner_marked")}
            for o in opts:
                o["winner_marked"] = o["name"] in won
            ok["page_equal"], ok["parts_add_up"] = n["page"]["equal"], n["parts_add_up"]
            if not n["page"]["equal"]:
                why.append("the page shows other candidates or votes than the file holds")
            if not n["parts_add_up"]:
                why.append("its locality lines count " + "; ".join(
                    f"{e['votes']:,} votes for {e['name']} (in {', '.join(e['localities'])})"
                    for e in n["extra_in_localities"]) + ", whom its statewide count does not hold"
                    if n["extra_in_localities"] else "its locality lines do not add up to its statewide count")
            a, _, t = (n["page"]["localities_reporting"] or "/").partition("/")
            ok["all_reporting"] = a == t == str(n["localities"])
            if not ok["all_reporting"]:
                why.append(f"the page prints 'Localities reporting {n['page']['localities_reporting']}', and the "
                           f"file has {n['localities']} locality lines")
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
            top, name, _ = max(others) if others else (None, None, None)
            r = mine / top if top else None
            over.append({"locality": lr["name"].title(), "votes_per_seat": round(mine, 1), "top": top, "top_name": name,
                         "ratio": None if r is None else round(r, 4)})
        worst = max((o for o in over if o["ratio"] is not None), key=lambda o: o["ratio"], default=None)
        c["over_ballot"] = {"worst": worst, "verdict": "untested" if worst is None else
                            "held" if worst["ratio"] > OVER_LINE else "listed" if worst["ratio"] > 1 else "passes"}
        if c["over_ballot"]["verdict"] == "held":
            why.append(f"its {worst['votes_per_seat']:,.0f} votes for each seat in {worst['locality']} are "
                       f"{worst['ratio']:.2f} times the {worst['top']:,} of {worst['top_name']}, the highest-vote "
                       f"contest of that locality's whole ballot, more than the {OVER_LINE} times a count can reach "
                       f"[measured]")
        elif c["over_ballot"]["verdict"] == "listed":
            notes.append(f"the over-ballot test within the locality: its {worst['votes_per_seat']:,.0f} votes for each "
                         f"seat in {worst['locality']} are {worst['ratio']:.3f} times the {worst['top']:,} of "
                         f"{worst['top_name']}, the highest-vote contest of that locality's whole ballot; between 1.0 "
                         f"and {OVER_LINE} times, which can be real, so kept and listed [measured]")
        if short:
            notes.append("the precinct lines do not add up to the locality line for "
                         + "; ".join(f"{s['option']} in {s['locality']} ({s['precincts']:,} against "
                                     f"{s['locality_line']:,})" for s in short[:4])
                         + (f"; and {len(short) - 4} more" if len(short) > 4 else "")
                         + " [measured]; the locality line is the count (recorded beside the gate, not a part of it)")
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
    out, cham = [], collections.Counter()
    for b in lr["ballotItems"]:
        v = sum(o["voteCount"] for o in b["ballotOptions"])
        m = LEG_TITLE.match(b["name"])
        if m:
            cham[m.group(1)] += v
        elif (b["voteFor"] == 1 or b["contestType"] == "BallotMeasure") and b["precinctsParticipating"] == n:
            out.append((v, " ".join(b["name"].split()), b["id"]))
    out += [(v, f"{POSS[ch]} lines in {lr['name'].title()}, summed", None) for ch, v in cham.items()]
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
    rec = {"by": GATE_BY, "ruled": RULED, "official": g[0],
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
            x = {"name": o["name"], "votes": o["votes"], "as_named": True, "party": None,
                 "writein": o["kind"] != "ballot"}
            if c["shared"]:
                x["won_marked"] = True if o["winner_marked"] else None
            cands.append(x)
        out.append(dict(base, magnitude=c["seats"], question=False, candidates=cands, party_not_given=True))
    return out


def source_block(year):
    res = VAL.load(year)
    fx, fp = res["files"]["export"], res["files"]["election"]
    note = (f"the results site's page of '{res['name']}' ({fp['url']}, {fp['how']}, finished {fp['finished_utc']}, "
            f"sha256 {fp['sha256'][:16]}; headed {res['official_text']!r}) and its 'Media Export' file ({fx['url']}, "
            f"finished {fx['finished_utc']}, sha256 {fx['sha256'][:16]}, created {res['export_created_utc'][:19]}Z), "
            f"read by pipeline/intake/va_elect.py before the Department refused us (2026-11-07 18:27:48 UTC; nothing "
            f"is requested from it again). Gate {GATE_BY} (pipeline/local_va.py; data/local/check-va-local.json), "
            f"proposed: the page headed 'OFFICIAL RESULTS' and linked from the Department's results page, the figures "
            f"it shows the file's, a shared contest's locality lines adding up to its statewide count and as many as "
            f"the page prints, a one-locality contest all reporting, and the over-ballot test within each locality. "
            f"The file gives no party for any local candidate, and marks no winner; the page marks the shared "
            f"contests' winners")
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
