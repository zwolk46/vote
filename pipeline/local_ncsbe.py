"""pipeline/local_ncsbe.py: North Carolina's State Board of Elections returns, every date from 2000, in the plan's layout.

Written 2026-11-07 by worker D3 (briefs/D3-data-local.md, steps 2, 4 and 6; the orchestrator, 07:25 and 07:30: NC SBE
by script, the results_pct files, the most contests for the fewest tokens). Reads pipeline/intake/ncsbe.py's cache.

  check   compares the State Board's counts with the sources already in data/: D1's certified presidential totals,
          Klarner's state legislative returns (2000-2022) and MEDSL's (2024), and MEDSL's local races and questions
          (2016-2024); writes data/local/check-ncsbe.json.
  build   writes every contest the files hold below Congress and the governor:
            data/local/<year>/NC.json     local offices, and the state's other offices (courts, district attorneys,
                                          the Council of State), as data/README.md says for MEDSL's;
            data/measure/<year>/NC.json   questions (referenda, bonds, amendments);
            data/primary/<year>/NC.json   party primaries, of every office below Congress and the governor.
          The legislature's general elections are Klarner's (to 2022) and MEDSL's (2024) in data/state-*/; the State
          Board's counts of them go to the check, not into a second copy. Where MEDSL already writes a year's North
          Carolina file (its general election dates), the State Board's contests of that date are compared, not
          written twice; its contests of the year's other dates are added to the same file beside MEDSL's.

What the files cannot show, and how it is handled (each said in the contest's own words):
  - Seats: the files give "vote for" from 2014 only. Before, a race with more names than one has unknown seats, so
    winners are not marked and p is not computed.
  - Which round: the files do not say whether a date is a primary, a first round or a runoff. A contest whose name
    carries a party ("... - DEM", "... (REP)") is that party's primary, and a second primary when the same name was on
    an earlier ballot that year. Before 2008 the names carry no party: on a date other than a November general, a
    contest whose names all carry one party code is that party's primary, and one carrying several is split by party.
    A nonpartisan contest whose name is on a later ballot that year is a first round (a primary or an election that
    went to a runoff); one whose name was on an earlier ballot is a second round. All of these are [inferred].
    "The same name" is the same name in the same place: on another date, a contest of the name whose counties
    overlap this one's (keyed on the name alone until 2026-11-07 11:57 UTC, when M2's check c19 found same-named
    contests of different counties read as rounds of one; the orchestrator, 11:44).
    A November contest whose name was on an earlier ballot that year is that contest's deciding round, after a
    nonpartisan primary or a first round, in odd and even years alike: the November count is the one that elects, so
    p is computed by the route's classes, and the contest is marked so (the orchestrator, 2026-11-07 09:53 UTC; added
    09:55 UTC). The earlier round stays not computed (model section 7), and so does a second round on another date.
  - Winners: the files do not mark them; the leading names for the seats are taken as won [inferred], and none at a
    tie for the last seat, as for MEDSL.
p: 0 for one name on the ballot for each seat. Otherwise, from 2014, the like-race route (D3-v1.1) fitted on North
Carolina's own contests of earlier years (nc_key; approved by the orchestrator at 08:08 with its back-test,
data/local/backtest-ncsbe.json), uncalibrated; every contest out of its reach says why.

Run:  VOTE_CACHE=/tmp/vote-cache python3 pipeline/local_ncsbe.py check|build
"""
import argparse
import collections
import csv
import datetime
import functools
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fetch as F  # noqa: E402
from intake import clerk_house as CLERK  # noqa: E402
import local as L  # noqa: E402
import local_medsl as LM  # noqa: E402

NORM = os.path.join(F.CACHE, "ncsbe", "normalized")
SITE = "https://dl.ncsbe.gov/ENRS/"
SOURCE_KEY = "ncsbe"
# the latest date's count is four days old at reading and not yet certified [inferred]: no live data (the maker, 03:13)
NOT_CERTIFIED = {"2026_11_03": "the count of 2026-11-03, four days old when read, is not yet certified: left out until "
                               "it is (no live data, the maker's words of 03:13)"}
PARTY_SUFFIX = re.compile(r"\s*(?:-\s*|\()\s*(DEM|REP|LIB|GRE|CST|UNA|REF|WTP|JUS|NLB)\)?\s*$")
FEDERAL = re.compile(r"^(US |U\.S\.|UNITED STATES|PRESIDENT|PRESIDENTIAL PREFERENCE|STRAIGHT PARTY)")
GOVERNOR = re.compile(r"^(NC )?GOVERNOR\b")
LEG = re.compile(r"^(?:NC )?(?:STATE )?(SENATE|HOUSE)(?: OF REPRESENTATIVES)?(?: DISTRICT)?\s*\(?0*(\d+)[A-Z]?\)?")
STATE_OFFICE = re.compile(r"^NC |SUPREME COURT|COURT OF APPEALS|SUPERIOR COURT JUDGE|DISTRICT COURT JUDGE|"
                          r"DISTRICT ATTORNEY|^CT OF APPEALS")
ANSWER = re.compile(r"^(YES|NO|FOR|AGAINST)\b", re.I)
PARTY_WORD = {"DEM": "D", "REP": "R"}
PRIMARY_WORD = {"DEM": "Democratic primary", "REP": "Republican primary"}


def _iso(d):
    return d.replace("_", "-")


def load_dates():
    """{date: [contests]} for every date read by the intake, the uncertified left out (a fresh copy each call:
    split_party and classify change it in place)."""
    out = {}
    for path in sorted(glob.glob(os.path.join(NORM, "*.jsonl"))):
        d = os.path.basename(path)[:-6]
        if d in NOT_CERTIFIED:
            continue
        with open(path) as f:
            out[d] = [json.loads(x) for x in f]
    return out


def checks_of(d):
    with open(os.path.join(NORM, f"checks-{d}.json")) as f:
        return json.load(f)


@functools.lru_cache(maxsize=None)
def county_fips():
    """NC county names to FIPS codes, from the county_name and county_fips columns of MEDSL's 2024 NC file."""
    path = os.path.join(F.CACHE, "medsl", "raw", "2024-13731149-2024-nc-precinct-general.csv")
    m = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            m[row["county_name"].upper()] = row["county_fips"]
    return m, F.meta(os.path.join("medsl", "raw", "2024-13731149-2024-nc-precinct-general.csv"))


def is_general_date(d):
    """A November date: the even years' general election and the odd years' municipal one."""
    return d[5:7] == "11"


def _ballot(c):
    return [x for x in c["choices"] if not LM._is_generic(x["name"])]


def is_question(c):
    b = _ballot(c)
    return len(b) >= 1 and all(ANSWER.match(x["name"]) for x in b)


def split_party(dates):
    """Before 2008 the names carry no party: split a primary date's contests by the parties of their names."""
    for d, cs in dates.items():
        if is_general_date(d) or int(d[:4]) >= 2008:
            continue
        out = []
        for c in cs:
            parties = {x["party"] for x in _ballot(c) if x["party"]}
            if PARTY_SUFFIX.search(c["contest"]) or is_question(c) or not parties:
                out.append(c)
                continue
            for p in sorted(parties):
                cc = dict(c, choices=[x for x in c["choices"] if x["party"] == p], party_of_names=p)
                out.append(cc)
            left = [x for x in c["choices"] if not x["party"]]
            if left:
                out.append(dict(c, choices=left, party_of_names=""))
        dates[d] = out


def classify(dates):
    """Each contest's level, its office's place, its party (primaries) and its round, as the docstring says."""
    by_year = collections.defaultdict(list)
    for d in sorted(dates):
        by_year[d[:4]].append(d)
    # (year, name, party) -> [(date, its counties)]: a round is the same contest only in the same place, so another
    # date's contest of the name is a round of this one only where their counties overlap (M2's check c19, #69; the
    # orchestrator, 2026-11-07 11:44: "a round is the same contest only in the same place"). The files give no
    # district id (every contest's district is empty [measured]), so the place is the counties. Overlap, not
    # equality: a city across two counties can show only one in a round its other county's voters did not vote in
    # (Hickory's aldermen, 2019) [measured].
    seen = collections.defaultdict(list)
    for d in sorted(dates):
        for c in dates[d]:
            m = PARTY_SUFFIX.search(c["contest"])
            party = m.group(1) if m else c.get("party_of_names")
            if party is None and not is_general_date(d) and int(d[:4]) < 2008:
                party = None
            base = PARTY_SUFFIX.sub("", c["contest"]).strip()
            c["_base"], c["_party"] = base, party or None
            seen[(d[:4], base, party or None)].append((d, frozenset(c["counties"])))
    for d in sorted(dates):
        for c in dates[d]:
            base, party = c["_base"], c["_party"]
            here = set(c["counties"])
            ds = [x for x, where in seen[(d[:4], base, party)] if where & here]
            earlier, later = [x for x in ds if x < d], [x for x in ds if x > d]
            leg = LEG.match(base)
            if FEDERAL.match(base) or GOVERNOR.match(base) or "STRAIGHT PARTY" in base:   # a town's too (2011)
                c["_level"] = None
            elif is_question(c):
                c["_level"] = "measure"
            elif party:
                c["_level"] = "primary"
            else:
                c["_level"] = "legislature" if leg and is_general_date(d) else "local"
            if leg:
                c["_leg"] = ("state-upper" if leg.group(1) == "SENATE" else "state-lower", int(leg.group(2)))
            if party:
                c["_round"] = ("second primary" if earlier else "primary", earlier or later)
            elif is_general_date(d):
                c["_round"] = ("after an earlier round" if earlier else "general", earlier)
            else:
                c["_round"] = ("first round" if later else "second round" if earlier else "election", later or earlier)
    return dates


DECIDING = "deciding round after an earlier round"


def deciding_words(earlier):
    """A November contest whose name was on an earlier ballot that year: its deciding round (the orchestrator,
    2026-11-07 09:53 UTC: "the November count is the one that elects")."""
    on = ", ".join(_iso(x) for x in sorted(set(earlier)))
    return (f"{DECIDING} on {on} (a nonpartisan primary or a first round that went to a runoff; the source does not "
            f"say which) [inferred]")


def election_words(c, d):
    kind, other = c["_round"]
    on = ", ".join(_iso(x) for x in sorted(set(other)))   # a date once, though two contests of the name are on it
    if c["_level"] == "measure":   # a question has no rounds: one of the same title on another date is another question
        w = (("general" if int(d[:4]) % 2 == 0 else "general (odd year: municipal)") if is_general_date(d) else
             f"election on {_iso(d)}, not a November general (the source does not say its kind)")
        return w + (f"; a question of the same title was on the ballot on {on} too" if other else "")
    if c["_party"]:
        w = PRIMARY_WORD.get(c["_party"], f"{c['_party']} primary (the party's code in the source)")
        if kind == "second primary":
            return f"{w}, second primary (the same contest was on the ballot on {on}) [inferred]"
        return w + (f" (a second primary followed on {on}) [inferred]" if other else "")
    if kind == "general":
        return "general" if d[:4] and int(d[:4]) % 2 == 0 else "general (odd year: municipal)"
    if kind == "after an earlier round":
        return deciding_words(other)
    if kind == "first round":
        return (f"first round: the same contest is on the ballot again on {on} (a nonpartisan primary or a first "
                f"round that went to a runoff; the source does not say which) [inferred]")
    if kind == "second round":
        return f"second round, after {on} (the source does not say whether a runoff or an election) [inferred]"
    return f"election on {_iso(d)}, not a November general (the source does not say its kind)"


def seats_of(c):
    return c.get("vote_for") if c.get("vote_for") else (1 if len(_ballot(c)) <= 1 else None)


def cands_out(c, seats):
    b = sorted(c["choices"], key=lambda x: -x["votes"])
    order = sorted(_ballot(c), key=lambda x: -x["votes"])
    tie = seats and len(order) > seats and order[seats - 1]["votes"] == order[seats]["votes"]
    second = c["_party"] and c["_round"][0] == "primary" and c["_round"][1]
    winners = set() if (not seats or tie or second) else {x["name"] for x in order[:seats]}
    out = []
    for x in b:
        code = x["party"] or None
        party = ("write-in" if LM._is_generic(x["name"]) else PARTY_WORD.get(code, code))
        rec = {"name": x["name"], "party": party, "votes": x["votes"], "won": True if x["name"] in winners else None}
        if code and code not in PARTY_WORD:
            rec["party_code"] = code
        out.append(L._compact(rec))
    return out


def p_of(c, seats):
    kind = c["_round"][0]
    b = _ballot(c)
    if c["_level"] == "measure":
        return {"not_computed": "not computed in this step: North Carolina's questions need the threshold their law sets "
                                "(step (b) for local questions) and the like-past-measures forecast fitted to earlier "
                                "years"}
    if kind in ("first round", "second primary"):
        return {"not_computed": "a first round or a second primary: model section 7 records runoff systems' rounds "
                                "with their results and does not compute p for them"}
    if seats and len(b) <= seats:
        swi = LM.strong_write_in([{"name": x["name"], "votes": x["votes"]} for x in c["choices"]], seats)
        if swi:
            return {"not_computed": "one name on the ballot for each seat, but write-ins received votes near the last "
                                    f"winner's: {L.METHOD} has no forecast route for write-in contests"}
        return {"value": 0.0, "event": 0.0, "reason": "one name on the ballot for each seat (unopposed): p is 0"}
    if not seats:
        return {"not_computed": "the number of seats is not in the source (its files give it from 2014 only)"}
    if kind == "second round":   # a deciding round in November is computed (DECIDING); on another date it is not
        return {"not_computed": "a second round on a date other than November's (perhaps a runoff): model section 7 "
                                "does not compute p for runoffs, and the source does not say which this is"}
    if c["_party"] and c["_round"][1]:
        return {"not_computed": "a second primary followed, so this primary was a first round: model section 7 records "
                                "runoff systems' rounds with their results and does not compute p for them"}
    return None   # the like-race route (nc_key, class_p)


# ------------------------------------------------------------------ the model's own forecast: like races, NC's own
FIRST_FIT_YEAR = 2014   # seats are in the files from 2014 only, so like races are counted from then


def nc_key(c):
    """(route, class, seats) of a contest the like-race route can take (p_of gave it no other answer): the classes of
    REPORT section 7 (scope, office type, the kind of field, candidates; seats at once at the boundary), with two more
    fixed before any score (the orchestrator, 08:08): 'a Democrat against a Republican', since these dates have no
    county lean, and primaries by office type and candidates, p between the top two (model section 7)."""
    seats = seats_of(c)
    b = _ballot(c)
    base = c["_base"]
    ot = "state legislature" if c.get("_leg") else LM.office_type(base)
    scope = "state legislature" if c.get("_leg") else "state" if STATE_OFFICE.search(base) else "local"
    lead = (scope if scope == "state legislature" else f"{scope} {ot}")
    n = len(b)
    if c["_level"] == "primary":
        return "class", f"primary, {lead}, {n if n < 4 else '4+'} candidates" + (f", {seats} seats" if seats > 1
                                                                                 else ""), seats
    nd = sum(1 for x in b if _major(x["party"]) == "D")
    nr = sum(1 for x in b if _major(x["party"]) == "R")
    if seats > 1:
        slate = "both major parties on the ballot" if nd and nr else "one major party or none"
        return "boundary", f"{lead}, {seats if seats < 4 else '4+'} seats at once, {slate}", seats
    if nd == 1 and nr == 1 and n == 2:
        return "class", f"{lead}, a Democrat against a Republican", 1
    kind = ("nonpartisan" if all(not x["party"] for x in b) else "one major party against others" if nd + nr == 1
            else "two or more of one major party" if nd + nr >= 2 else "no Democrat or Republican")
    return "class", f"{lead}, {kind}, {n if n < 4 else '4+'} candidates", 1


def _shape(c):
    return {"candidates": [{"name": x["name"], "votes": x["votes"]} for x in c["choices"]]}


def like_rows(dates):
    """Every contest the route can take, with its class and its result: the share of the leading two (at the
    boundary, the last winner and the first loser) that the first of them won."""
    out = []
    for d, cs in dates.items():
        if int(d[:4]) < FIRST_FIT_YEAR:
            continue
        for c in cs:
            if c["_level"] not in ("local", "primary") or p_of(c, seats_of(c)) is not None:
                continue
            route, key, k = nc_key(c)
            top = sorted(c["choices"], key=lambda x: -x["votes"])
            if any(LM._is_generic(x["name"]) for x in top[k - 1:k + 1]):
                continue
            b = sorted(_ballot(c), key=lambda x: -x["votes"])
            x1, x2 = b[k - 1]["votes"], b[k]["votes"]
            if x1 + x2 > 0:
                out.append({"year": int(d[:4]), "date": d, "key": key, "route": route, "level": c["_level"],
                            "s": max(x1, x2) / (x1 + x2), "n": x1 + x2, "c": c})
    return out


def backtest(rows):
    """Each year forecast from earlier years only: finishes in the class window, expected against seen."""
    years = sorted({r["year"] for r in rows})
    by = {}
    for y in years:
        train = [r for r in rows if r["year"] < y]
        dens = {}
        t = collections.defaultdict(lambda: [0, 0.0, 0])
        for r in rows:
            if r["year"] != y:
                continue
            if r["key"] not in dens:
                dens[r["key"]] = L.class_density(train, r["key"])
            f, N, h, kin = dens[r["key"]]
            if f is None:
                continue
            for g in (r["level"], r["route"], "all"):
                t[g][0] += 1
                t[g][1] += kin / N
                t[g][2] += r["s"] <= 0.5 + h
        by[str(y)] = {g: {"forecast": v[0], "expected_in_window": round(v[1], 1), "seen_in_window": v[2]}
                      for g, v in sorted(t.items())}
    pooled = collections.defaultdict(lambda: [0, 0.0, 0])
    for y, v in by.items():
        for g, x in v.items():
            pooled[g][0] += x["forecast"]
            pooled[g][1] += x["expected_in_window"]
            pooled[g][2] += x["seen_in_window"]
    return_cal = calibration(rows)
    return {"about": "the like-race route (D3-v1.1) on North Carolina's State Board contests: each year forecast "
                     f"from North Carolina's earlier years only (from {FIRST_FIT_YEAR}, when the files begin to give "
                     "seats); for each contest, the chance its class gave of finishing in the class's window around "
                     "1/2, against whether it did. Built by pipeline/local_ncsbe.py build.",
            "by_year": by, "pooled": {g: {"forecast": v[0], "expected_in_window": round(v[1], 1),
                                          "seen_in_window": v[2]} for g, v in sorted(pooled.items())},
            "calibration": return_cal}


def _cell(r):
    """The robustness test's cell for a like-race row: its route and office type, as pipeline/local_medsl.py's
    calibrate_local has them (primaries apart)."""
    c = r["c"]
    scope = "state legislature" if c.get("_leg") else "state" if STATE_OFFICE.search(c["_base"]) else "local"
    ot = "" if c.get("_leg") else " " + LM.office_type(c["_base"])
    return f"{'primary, ' if r['level'] == 'primary' else ''}{r['route']}, {scope}{ot}"


def calibration(rows):
    """The 06:38 rule's factor (seen over expected in the class windows, pooled over earlier years; a year is scored
    where the earlier years expected 30 or more), under the robustness test of the brief's amendment of 2026-11-07
    08:36 (pipeline/local_medsl.py, _cal_score): adopted only if it improves the out-of-sample test over the scored
    years with no tested cell made worse, and again with any one scored year left out. Rewritten 2026-11-07 10:04 UTC:
    before, a factor was adopted when it only brought the pooled count nearer, and each forecast's note said, as a fixed
    text, that it did not (true until the deciding rounds of 09:53 entered the pool). Not applied to p either way
    here: where it would pass, the orchestrator is told first [inferred: a change to the forecast is the
    orchestrator's to see before it stands]."""
    recs = collections.defaultdict(list)
    for y in sorted({r["year"] for r in rows}):
        train = [r for r in rows if r["year"] < y]
        dens = {}
        for r in rows:
            if r["year"] != y:
                continue
            if r["key"] not in dens:
                dens[r["key"]] = L.class_density(train, r["key"])
            f, N, h, kin = dens[r["key"]]
            if f is None:
                continue
            recs[(r["level"], y)].append((None, _cell(r), kin / N, r["s"] <= 0.5 + h))
    out = {}
    for g in ("local", "primary"):
        years = sorted(y for gg, y in recs if gg == g)
        factors, scored = {}, []
        for t in years:
            pe = sum(e for y in years if y < t for _, _, e, _ in recs[(g, y)])
            ps = sum(sn for y in years if y < t for _, _, _, sn in recs[(g, y)])
            if pe >= LM.CAL_MIN_EXPECTED:
                factors[t] = {"own": {}, "pooled": ps / pe}
                scored.append(t)
        if not scored:
            out[g] = {"scored_years": [], "adopted": False, "why": "no year has 30 or more expected in earlier years"}
            continue
        test = LM._cal_score(recs, g, scored, factors)
        loo = {str(t): (LM._cal_score(recs, g, [y for y in scored if y != t], factors) if len(scored) > 1 else
                        {"passes": False, "why": "no scored year is left: the only scored year is " + str(t)})
               for t in scored}
        for v in loo.values():
            v.pop("by_office_type", None)
        out[g] = {"factors": {str(t): round(f["pooled"], 3) for t, f in factors.items()},
                  "scored_years": scored, "test": test, "leave_one_year_out": loo,
                  "adopted": test["passes"] and all(v["passes"] for v in loo.values()),
                  "robustness_rule": "adopted only if it improves the out-of-sample test (the count in the class "
                                     "windows nearer, and the deviance by office type lower) over every scored year "
                                     f"with no tested cell made worse (a tested cell: {LM.CAL_CELL_MIN} or more seen "
                                     "or expected), and again with any one scored year left out (brief D3, amended "
                                     "2026-11-07 08:36)"}
    return out


def cal_note(cal):
    """Each forecast's note on the calibration, from the record (calibration's result), not a fixed text."""
    c = cal.get("local", {})
    if c.get("adopted"):
        return ("no calibration applied: the factor fitted on earlier years passes the robustness test and waits for "
                "the orchestrator (data/local/backtest-ncsbe.json, calibration)")
    t = c.get("test") or {}
    why = ("it makes tested cells worse: " + ", ".join(t["tested_cells_made_worse"]) if t.get("tested_cells_made_worse")
           else "it does not improve the test" if t and not t.get("improves") else
           "it fails with a scored year left out")
    return f"no calibration: the factor fitted on earlier years fails the robustness test, since {why} " \
           f"(data/local/backtest-ncsbe.json, calibration)"


def _slug(x):
    return L._slug(x)[:70]


OWN_COUNTY_NOTE = ("one county's own contest: the State Board's file gives each county's this same name, which carries "
                   "no place, so it is read as one contest per county (pipeline/intake/ncsbe.py, generic)")


def record(c, d, fips, commit):
    year = int(d[:4])
    seats = seats_of(c)
    level = c["_level"]
    base = c["_base"]
    counties = sorted({fips[x] for x in c["counties"] if x in fips})
    scope = "state" if STATE_OFFICE.search(base) else "local"
    where = "" if len(c["counties"]) != 1 or scope == "state" else "-" + _slug(c["counties"][0])
    rec = {"id": f"{year}-{level}-NC-ncsbe-{_iso(d)}-{_slug(base)}{('-' + c['_party'].lower()) if c['_party'] else ''}"
                 f"{where}",
           "year": year, "date": _iso(d), "level": level,
           "place": {"state": "NC", "district": c.get("district"),
                     "counties": None if scope == "state" and len(c["counties"]) >= 100 else counties},
           "election": election_words(c, d)}
    total = sum(x["votes"] for x in c["choices"])
    if level == "measure":
        yes = sum(x["votes"] for x in c["choices"] if LM.side(x["name"]) == "yes")
        no = sum(x["votes"] for x in c["choices"] if LM.side(x["name"]) == "no")
        rec["question"] = {"title": base, "kind": "measure",
                           "scope": "statewide" if len(c["counties"]) >= 100 else "local"}
        rec["result"] = {"candidates": [{"name": x["name"], "votes": x["votes"]} for x in c["choices"]],
                         "total_votes": total, "source": SOURCE_KEY,
                         "yes_share": round(yes / (yes + no), 6) if yes + no else None}
    else:
        if level == "primary" and c.get("_leg"):
            rec["office"] = c["_leg"][0]
            rec["place"]["district"] = str(c["_leg"][1])
        else:
            rec["office"] = base.title()
            rec["office_type"] = LM.office_type(base)
            rec["office_scope"] = scope
        rec["seats"] = seats if (seats or 1) > 1 else None
        rec["result"] = {"candidates": cands_out(c, seats), "total_votes": total, "source": SOURCE_KEY}
    notes = [OWN_COUNTY_NOTE] if c.get("own_county") else []
    if not seats and level != "measure":
        notes.append("seats not in the source before 2014: winners not marked")
    if c.get("party_of_names") is not None and not PARTY_SUFFIX.search(c["contest"]):
        notes.append("the source's names carry no party before 2008: this primary's party is its candidates' party "
                     "code, and the source's one contest of this name on this date is split by party [inferred]")
    rec["notes"] = notes or None
    rec["forecasts"] = []
    rec["p"] = p_of(c, seats)
    return rec


# ------------------------------------------------------------------ the gate, and MEDSL's shape
def _major(party):
    p = (party or "").upper()
    return "D" if p in ("DEM", "D", "DEMOCRATIC", "DEMOCRAT") else "R" if p in ("REP", "R", "REPUBLICAN") else None


FED_FILES = {"president": re.compile(r"^(US PRESIDENT|PRESIDENT)"), "senate": re.compile(r"^US SENATE"),
             "house": re.compile(r"^(US HOUSE|US CONGRESS|U\.S\. HOUSE)")}


def gate(dates):
    """{date: (share, words)} for each November date of an even year: how far the file's Democratic and Republican
    votes for the presidency and the Senate (the House, district by district, in a year with neither) fall from the
    certified ones in D1's and D2's files (data/<president|senate|house>/<year>.json); in a year those files do not
    reach, from the Clerk of the House's statistics, the Senate and every House district (pipeline/intake/clerk_house.py,
    read for 2002 at the orchestrator's order of 08:32). A date whose counts miss by more than MEDSL's line
    (local_medsl.QUALITY_LINE) is a file posted before the final count [inferred]; its contests carry a note."""
    out = {}
    for d, cs in sorted(dates.items()):
        if not is_general_date(d) or int(d[:4]) % 2:
            continue
        worst, what = 0.0, []
        statewide = any(FED_FILES[lv].match(c["contest"]) for lv in ("president", "senate") for c in cs)
        for level, pat in FED_FILES.items():
            path = os.path.join(L.REPO, "data", level, f"{d[:4]}.json")
            mine = [c for c in cs if pat.match(c["contest"])]
            clerk = None
            if not os.path.exists(path) and level in ("senate", "house") and os.path.exists(CLERK.path(d[:4])):
                with open(CLERK.path(d[:4])) as f:   # a year D2's files do not reach: the Clerk of the House's
                    clerk = json.load(f)              # statistics (pipeline/intake/clerk_house.py; the orchestrator, 08:32)
            if not mine or not (os.path.exists(path) or clerk) or (level == "house" and statewide and not clerk):
                continue   # the statewide contests where there are any: one count each, the cleanest comparison
            if clerk:
                cert = [x for x in clerk["contests"] if x["office"] == level and x["place"]["state"] == "NC"]
            else:
                with open(path) as f:
                    cert = [x for x in json.load(f)["contests"] if x["place"]["state"] == "NC"]
            if not cert:
                continue
            pairs = [(mine, cert)]
            if level == "house":   # district by district: a district one file lacks is not a shortfall of the other
                dn = lambda s_: int(re.search(r"(\d+)", s_).group(1)) if re.search(r"(\d+)", s_ or "") else None
                byc = collections.defaultdict(list)
                for x in cert:
                    if not x.get("special"):
                        byc[dn(x["place"].get("district"))].append(x)
                both = lambda xs, key: {_major(x.get("party")) for x in xs} >= {"D", "R"}
                pairs = [([c], byc[dn(c["contest"])]) for c in mine
                         if len(byc.get(dn(c["contest"]), [])) == 1 and both(c["choices"], 0)
                         and both(byc[dn(c["contest"])][0]["result"]["candidates"], 0)]
            for side in ("D", "R"):
                a = sum(x["votes"] for m_, _ in pairs for c in m_ for x in c["choices"] if _major(x["party"]) == side)
                b = sum(x["votes"] for _, c_ in pairs for c in c_ for x in c["result"]["candidates"]
                        if _major(x.get("party")) == side)
                if b:
                    what.append(f"{level}{' (the Clerk of the House)' if clerk else ''} {side} {a:,} against {b:,}"
                                + (f" ({len(pairs)} districts in both)" if level == "house" else ""))
                    worst = max([worst] + [abs(sum(x["votes"] for c in m_ for x in c["choices"]
                                                   if _major(x["party"]) == side)
                                               - sum(x["votes"] for c in c_ for x in c["result"]["candidates"]
                                                     if _major(x.get("party")) == side))
                                           / max(1, sum(x["votes"] for c in c_ for x in c["result"]["candidates"]
                                                        if _major(x.get("party")) == side))
                                           for m_, c_ in pairs if level == "house"] + [abs(a - b) / b])
        out[d] = (worst, "; ".join(what))
    return out


def fips_source():
    _, fmeta = county_fips()
    return F.source("county FIPS codes: the county_name and county_fips columns of MEDSL's 2024 North Carolina "
                    "precinct file", fmeta["url"], fmeta["read_utc"], "CC0 1.0", mark="stated")


def medsl_shape(year):
    """North Carolina's contests of MEDSL's general date of `year`, from the State Board, in the shape
    pipeline/local_medsl.py's load() gives: the certified file wins where two sources hold one contest (brief D3,
    step 2). The legislature, the governor and Congress stay MEDSL's. None if the file is missing or fails the gate."""
    dates = load_dates()
    d = next((x for x in dates if x.startswith(str(year)) and is_general_date(x)), None)
    if d is None:
        return None
    if gate({d: dates[d]}).get(d, (0,))[0] > LM.QUALITY_LINE:
        return None
    split_party(dates)
    classify(dates)
    fips, _ = county_fips()
    meta = checks_of(d)["source"]
    out = []
    for c in dates[d]:
        if c["_level"] not in ("local", "measure"):
            continue
        statewide = len(c["counties"]) >= 100
        base = c["_base"]
        out.append({"state": "NC", "date": _iso(d), "stage": "GEN", "special": False,
                    "dataverse": "STATE" if (statewide or STATE_OFFICE.search(base)) else "LOCAL",
                    "office": base, "district": "STATEWIDE" if statewide else "", "subject": None,
                    "magnitude": c.get("vote_for"), "question": c["_level"] == "measure",
                    "own_county": c.get("own_county") or None,
                    "earlier_round": (c["_round"][1] if c["_round"][0] == "after an earlier round" and
                                      c["_level"] == "local" else None),
                    "precincts": c["n_precincts"], "counties": sorted({fips[x] for x in c["counties"] if x in fips}),
                    "candidates": [{"name": x["name"], "votes": x["votes"], "as_named": True,
                                    "party": {"D": "DEMOCRAT", "R": "REPUBLICAN"}.get(_major(x["party"]),
                                                                                     x["party"] or "NONPARTISAN")}
                                   for x in c["choices"]],
                    "source": SOURCE_KEY, "file": {"name": meta["url"].rsplit("/", 1)[1], "url": meta["url"],
                                                   "read_utc": meta["read_utc"], "sha256": meta["sha256"]}})
    return out


def medsl_dates(dates):
    """MEDSL's general dates (its years): the contests local_medsl.py writes from the State Board's file."""
    return {d for d in dates for y in LM.MEASURE_YEARS if d.startswith(str(y)) and is_general_date(d)}


# ------------------------------------------------------------------ checks
def _dr(c):
    d = sum(x["votes"] for x in c["choices"] if x["party"] == "DEM")
    r = sum(x["votes"] for x in c["choices"] if x["party"] == "REP")
    return d, r


def check(dates):
    out = {"about": "North Carolina State Board of Elections counts (pipeline/intake/ncsbe.py), compared with the "
                    "sources already in data/. Built by pipeline/local_ncsbe.py check.",
           "gate": {_iso(d): ({"worst_miss": round(w, 6), "fails": w > LM.QUALITY_LINE, "counts": t} if t else
                              {"checked": False, "why": "no certified federal file for this year in data/"})
                    for d, (w, t) in gate(dates).items()},
           "president": [], "legislature_klarner": {}, "legislature_medsl_2024": {}, "medsl_local": {}}
    # 1. presidency: D1's certified totals (data/president/<year>.json)
    for d, cs in sorted(dates.items()):
        if not (is_general_date(d) and int(d[:4]) % 4 == 0):
            continue
        pres = [c for c in cs if re.match(r"^(US PRESIDENT|PRESIDENT)", c["contest"])]
        path = os.path.join(L.REPO, "data", "president", f"{d[:4]}.json")
        if not pres or not os.path.exists(path):
            continue
        with open(path) as f:
            d1 = [x for x in json.load(f)["contests"] if x["place"]["state"] == "NC"][0]
        d1v = {x["party"]: x["votes"] for x in d1["result"]["candidates"] if x["party"] in ("Democratic", "Republican")}
        dv, rv = _dr(pres[0])
        out["president"].append({"date": _iso(d), "ncsbe": {"D": dv, "R": rv},
                                 "d1": {"D": d1v.get("Democratic"), "R": d1v.get("Republican")},
                                 "equal": dv == d1v.get("Democratic") and rv == d1v.get("Republican")})
    # 2. the legislature's generals: Klarner (to 2022), MEDSL (2024)
    kl = collections.defaultdict(list)
    for k in L.load_klarner(raw=True):   # Klarner's own counts, before certified_votes
        if k["state"] == "NC" and k["etype"] == "g" and k["year"] >= 2000:
            kl[(k["year"], "state-upper" if k["sen"] else "state-lower", int(k["dno"]))].append(k)
    for d, cs in sorted(dates.items()):
        if not is_general_date(d) or int(d[:4]) % 2:
            continue
        year = int(d[:4])
        t = collections.Counter()
        diffs = []
        for c in cs:
            if c.get("_level") != "legislature":
                continue
            dv, rv = _dr(c)
            ks = kl.get((year, *c["_leg"]))
            if year > 2022:
                continue
            if not ks:
                t["not in Klarner"] += 1
                continue
            k = ks[0]["klarner"]
            if ks[0].get("dseats", 1) != 1:
                t["multi-member, not compared"] += 1
                continue
            if (k["dvote"] or 0) == dv and (k["rvote"] or 0) == rv:
                t["equal"] += 1
            else:
                t["differ"] += 1
                diffs.append({"district": f"{c['_leg'][0]} {c['_leg'][1]}", "ncsbe": [dv, rv],
                              "klarner": [k["dvote"], k["rvote"]]})
        if t:
            out["legislature_klarner"][str(year)] = {"tally": dict(t), "differences": diffs[:40]}
    # 2b. the legislature's 2024 generals: MEDSL's own counts (before certified_legislature), by named candidates
    d24 = next((x for x in dates if x.startswith("2024") and is_general_date(x)), None)
    paths = glob.glob(os.path.join(LM.NORM, "2024", "NC-*.jsonl"))
    if d24 and paths:
        mine = collections.defaultdict(list)
        for c in dates[d24]:
            if c.get("_level") == "legislature":
                mine[c["_leg"]].append(c)
        t = collections.Counter()
        diffs = []
        for p in paths:
            with open(p) as f:
                for m in (json.loads(ln) for ln in f):
                    if m.get("office") not in LM.LEG or m.get("question") or m.get("stage") != "GEN" or m.get("special"):
                        continue
                    key = ("state-upper" if LM.LEG[m["office"]] else "state-lower", int(LM.district_no(m["district"]) or 0))
                    hit = mine.get(key)
                    if not hit:
                        t["not in the State Board's file"] += 1
                        continue
                    a = sorted((x["votes"] for x in m["candidates"] if not x.get("writein") and not LM._is_generic(x["name"])),
                               reverse=True)
                    b = sorted((x["votes"] for x in hit[0]["choices"] if not LM._is_generic(x["name"])), reverse=True)
                    if a == b:
                        t["equal"] += 1
                    else:
                        t["differ"] += 1
                        diffs.append({"district": f"{key[0]} {key[1]}", "ncsbe": b, "medsl": a,
                                      "largest_difference": max((abs(x - y) for x, y in zip(a, b)), default=None)})
        out["legislature_medsl_2024"] = {"date": _iso(d24), "tally": dict(t),
                                         "differences": sorted(diffs, key=lambda x: -(x["largest_difference"] or 0))}
    # 3. MEDSL's NC contests (its general dates): the same contests, by their candidates' names and votes
    for year in LM.MEASURE_YEARS:
        d = next((x for x in dates if x.startswith(str(year)) and is_general_date(x)), None)
        paths = glob.glob(os.path.join(LM.NORM, str(year), "NC-*.jsonl"))
        if not d or not paths:
            continue
        med = []
        for p in paths:
            with open(p) as f:
                med += [x for x in (json.loads(ln) for ln in f) if "state" in x]
        mine = {}
        for c in dates[d]:
            if c.get("_level") in (None,):
                continue
            mine.setdefault(_sig(c["choices"]), []).append(c)
        t = collections.Counter()
        diffs = []
        for m in med:
            if m["office"] in LM.LEG or LM.GOVERNOR.match(m["office"]) or m.get("dataverse") not in ("STATE", "LOCAL"):
                continue
            if year == 2016 and not m["question"]:
                continue
            kind = "question" if m["question"] else "race"
            hit = mine.get(_sig(m["candidates"]))
            if hit:
                t[f"{kind}: equal"] += 1
                continue
            names = _names(m["candidates"])
            near = [c for cs in mine.values() for c in cs if _names(c["choices"]) == names] if names else []
            if near:
                t[f"{kind}: same names, votes differ"] += 1
                diffs.append({"office": m["office"], "district": m["district"],
                              "medsl": sorted((x["votes"] for x in m["candidates"]), reverse=True)[:4],
                              "ncsbe": sorted((x["votes"] for x in near[0]["choices"]), reverse=True)[:4]})
            else:
                t[f"{kind}: not found in the State Board's file"] += 1
                if len(diffs) < 80:
                    diffs.append({"office": m["office"], "district": m["district"], "medsl": [
                        (x["name"], x["votes"]) for x in m["candidates"]][:4], "ncsbe": None})
        out["medsl_local"][str(year)] = {"date": _iso(d), "tally": dict(t), "examples": diffs[:60]}
    return out


def _names(cands):
    return frozenset(LM.name_key(x["name"]) for x in cands if not LM._is_generic(x["name"]) and not ANSWER.match(x["name"]))


def _sig(cands):
    """A contest's signature: its lines' votes, the write-in lines left out (MEDSL and the State Board group them
    differently)."""
    return tuple(sorted((x["votes"] for x in cands if not LM._is_generic(x["name"])), reverse=True))


# ------------------------------------------------------------------ build
def source_block(year_dates, files_meta):
    names = ", ".join(f"{_iso(d)} ({m['url'].rsplit('/', 1)[1]}, sha256 {m['sha256'][:12]})" for d, m in files_meta)
    first = files_meta[0][1]
    return F.source("North Carolina State Board of Elections, precinct results by contest (results_pct files of "
                    "the public download site's ENRS folder)", SITE, first["read_utc"],
                    "public records under N.C. Gen. Stat. 132-1, as the site's ReadMe_PUBLIC_DATA.txt says; no "
                    "licence printed", mark="stated",
                    note="the state's own certified counts, by county, precinct and choice, added up to the contest "
                         "by pipeline/intake/ncsbe.py; files read: " + names)


def block_for(records):
    """The State Board's source block for a file: every results file its State Board contests, or its contests with
    the State Board's counts (result.votes_source), come from."""
    ds = sorted({r["date"].replace("-", "_") for r in records if SOURCE_KEY in ((r.get("result") or {}).get("source"),
                                                                              (r.get("result") or {}).get("votes_source"))})
    return source_block(ds, [(d, checks_of(d)["source"]) for d in ds]) if ds else None


def build(out_dir, dates):
    commit = L.git_commit()
    fips, fmeta = county_fips()
    # the block a like-race forecast cites (its "source": "model"), written into every file that holds one
    src_model = F.source(f"the model's own forecast, method {L.METHOD}",
                         "https://github.com/zwolk46/vote/blob/main/data/local/REPORT.md",
                         datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"), None,
                         mark="inferred", note="each year forecast from a fit on earlier years only; no polls are used")
    mdates = medsl_dates(dates)
    gated = gate(dates)
    rows = like_rows(dates)
    dens = {}
    with open(os.path.join(out_dir, "local", "backtest-ncsbe.json"), "w") as f:
        bt = backtest(rows)
        json.dump(bt, f, indent=1)
    note = cal_note(bt["calibration"])
    files = collections.defaultdict(list)
    used = collections.defaultdict(list)
    counts = collections.Counter()
    seen_ids = set()
    klarner_primary = {int(os.path.basename(os.path.dirname(p))) for p in
                       glob.glob(os.path.join(out_dir, "primary", "*", "NC.json"))
                       if _sources_of(p) - {SOURCE_KEY}}
    for d in sorted(dates):
        year = int(d[:4])
        for c in dates[d]:
            level = c["_level"]
            if level is None:
                counts["left out: the presidency, Congress or the governor (D1's and D2's levels), or straight-party "
                       "lines"] += 1
                continue
            if level == "legislature":
                counts["left out: the legislature's generals (Klarner's and MEDSL's; compared in the check)"] += 1
                continue
            if level == "primary" and c.get("_leg") and year in klarner_primary:
                counts["left out: legislative primaries of a year Klarner's file holds"] += 1
                continue
            if d in mdates and (level == "measure" or (level == "local" and year in LM.YEARS)):
                counts["written by pipeline/local_medsl.py: MEDSL's general date, the State Board's counts"] += 1
                continue
            rec = record(c, d, fips, commit)
            if rec["p"] is None:
                rec["p"] = route_p(rec, c, d, rows, dens, commit, counts, note)
            rec = L._compact(rec)
            if gated.get(d, (0,))[0] > LM.QUALITY_LINE:
                rec["notes"] = (rec.get("notes") or []) + [
                    f"this date's file falls short of the certified federal counts by up to {100 * gated[d][0]:.1f}% "
                    f"({gated[d][1]}): it was likely posted before the final count [inferred], so its counts are "
                    f"the State Board's posted ones, not the certified"]
            k, n = rec["id"], 2
            while rec["id"] in seen_ids:
                rec["id"] = f"{k}~{n}"
                n += 1
            seen_ids.add(rec["id"])
            files[(level, year)].append(rec)
            if d not in used[(level, year)]:
                used[(level, year)].append(d)
            p = rec["p"]
            counts[f"{level}: " + ("p = 0" if p.get("value") == 0 else "p computed" if "value" in p else
                                   "not computed, " + p["not_computed"][:60])] += 1
    total = 0
    for (level, year), recs in sorted(files.items()):
        meta = [(d, checks_of(d)["source"]) for d in used[(level, year)]]
        src = source_block(used[(level, year)], meta)
        path = os.path.join(out_dir, level, str(year), "NC.json")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        others, other_src, head = L.kept_from_others(path, lambda r: owns(r, mdates))
        if others:   # another source's file: ours go in beside its contests, each with its own p's script and commit
            for r in recs:
                r["p"] = dict(r["p"], computed_by="pipeline/local_ncsbe.py", commit=commit)
            head = dict(head)
            head["sources"] = dict(other_src, **{SOURCE_KEY: block_for(others + recs)})
            head["sources"].setdefault("fips", fips_source())
            out = others + recs
        else:
            head = {"level": level, "year": year, "state": "NC",
                    "about": f"{level} contests of {year} in North Carolina, in the layout of plan/PLAN.md section 3 "
                             f"with the fields data/README.md adds (D3). Built by pipeline/local_ncsbe.py from "
                             f"pipeline/intake/ncsbe.py's cache.",
                    "p_computed_by": "pipeline/local_ncsbe.py", "p_commit": commit,
                    "party_codes": {"D": "the source's DEM", "R": "the source's REP",
                                    "other codes": "the source's own three-letter code, in party and party_code; its "
                                                   "layout files give no codebook"},
                    "sources": {SOURCE_KEY: src,
                                "fips": fips_source()}}
            out = recs
        if any(f.get("source") == "model" for r in recs for f in r.get("forecasts") or []):
            head["sources"].setdefault("model", src_model)
        L.write_level_file(path, head, out)
        total += os.path.getsize(path)
    print(json.dumps(dict(sorted(counts.items())), indent=1))
    print(f"{sum(len(v) for v in files.values())} contests in {len(files)} files, {total / 2**20:.2f} MiB")


def route_p(rec, c, d, rows, dens, commit, counts, cal_note_text):
    year = int(d[:4])
    if year < FIRST_FIT_YEAR:
        return {"not_computed": f"before {FIRST_FIT_YEAR}: the files give no seats, so no like races are counted"}
    route, key, k = nc_key(c)
    train = [r for r in rows if r["year"] < year]
    if not train:
        return {"not_computed": f"no earlier year to fit on ({FIRST_FIT_YEAR} is the first year counted)"}
    p = LM.class_p(rec, _shape(c), route, key, train, dens, (year, key), commit, True, collections.Counter(),
                   rec["level"], k)
    if rec["forecasts"]:
        rec["forecasts"][-1]["fitted_on"] = f"North Carolina's State Board contests of {FIRST_FIT_YEAR}-{year - 1}"
        rec["forecasts"][-1]["note"] = "; ".join(x for x in (rec["forecasts"][-1].get("note"), cal_note_text) if x)
    return p


def owns(r, mdates):
    """The contests this build writes: the State Board's, on dates other than MEDSL's general dates."""
    medsl_writes = (r.get("date", "").replace("-", "_") in mdates
                    and (r.get("level") == "measure" or r.get("year") in LM.YEARS))
    return (r.get("result") or {}).get("source") == SOURCE_KEY and not medsl_writes


def _sources_of(path):
    with open(path) as f:
        d = json.load(f)
    return {(c.get("result") or {}).get("source") for c in d.get("contests", [])}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["check", "build"])
    ap.add_argument("--out", default=os.path.join(L.REPO, "data"))
    a = ap.parse_args()
    dates = load_dates()
    split_party(dates)
    classify(dates)
    if a.step == "check":
        out = check(dates)
        with open(os.path.join(L.REPO, "data", "local", "check-ncsbe.json"), "w") as f:
            json.dump(out, f, indent=1)
        print(json.dumps({"president": out["president"],
                          "klarner": {y: v["tally"] for y, v in out["legislature_klarner"].items()},
                          "medsl": {y: v["tally"] for y, v in out["medsl_local"].items()}}, indent=1))
    else:
        build(a.out, dates)


if __name__ == "__main__":
    main()
