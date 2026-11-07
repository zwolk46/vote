"""pipeline/local_la.py: Louisiana's official results of 2023 and 2024 (pipeline/intake/la_sos.py), gated, compared
with MEDSL's Louisiana file (2024), and put in the shape pipeline/local_medsl.py reads.

Written 2026-11-07 by worker D3 (briefs/D3-data-local.md, step 2) at the orchestrator's orders of 08:08 and 10:17
("Go on with LA 2024"). Why: MEDSL's 2024 Louisiana file counts Election Day only, so it falls 48.9% short of D1's
certified presidential count and its Louisiana contests are held back (no p; data/local/REPORT.md section 6). Where two
sources hold one contest the certified one wins (brief D3, step 2). So, if the state's file passes the gate,
local_medsl.load(2024) reads Louisiana's local races and questions from it in place of MEDSL's (certified_la there),
with MEDSL's routes; the presidency and Congress stay D1's and D2's. Louisiana elects no legislature in 2024.

2023 (added 2026-11-07 at the orchestrator's orders of 10:35, "LA 2023 ... by the same script", and 11:16, the gate):
MEDSL holds no 2023, so the state's file is the only source of Louisiana's 2023 legislature, local races and
questions. Its ballots carry no federal contest to gate against, so the gate is within the certifying source
(source_gate): (a) each date is marked official on the site's list; (b) each contest's parishes or precincts add up to
its total; (c) each contest on more than one parish's ballot equals the Secretary of State's own posted results of
its date (the site's RacesCandidates_Multiparish and Votes_Multiparish files). The ruling names (c) for the statewide
offices of 2023-10-14; it is applied to every multi-parish contest of every date, a wider read of the same check. A
contest that fails (b) or (c) is held; every record says "gate: within the certifying source (no federal contest on
the ballot)". The governor is D2's level, and D2's data/governor/ holds even years only, so Louisiana's 2023 governor
is left out and the gate's comparison of it is recorded in data/local/check-la.json only.

Louisiana's rounds (each said in the contest's own words). Its local offices are filled at a primary, open to every
candidate, and, where no one is elected there, a general election between the leaders a few weeks later: in 2024 the
primaries of 2024-03-23 and 2024-11-05 and the generals of 2024-04-27 and 2024-12-07; in 2023 the primaries of
2023-03-25 and 2023-10-14 and the generals of 2023-04-29 and 2023-11-18, and a special election to the House's 93rd
district on 2023-02-18 and 2023-03-25 [inferred: the dates of the source's list, and the contests it repeats from the
first of each pair to the second: 9 of 9 contests of 2023-04-29, 130 of 130 of 2023-11-18, and the one of
2023-03-25 that was on 2023-02-18]. La. R.S. 18:402, which sets the dates, was read on 2026-11-07 at 10:46 UTC
(https://legis.la.gov/Legis/Law.aspx?d=81545), as amended through Acts 2025, No. 386: its text pairs each season's
primary with a general on a later Saturday, but its dates are not 2023's or 2024's, since it was amended after them
(Acts 2024, No. 640; Acts 2025, No. 386). So the pairing rests on the source's repeated contests, and the statute is
cited for the pairing's form only (the orchestrator, 2026-11-07 11:16).
  - A contest on a primary date is the first round of a two-round system: recorded with its result, p not computed
    (model section 7), as for Klarner's Louisiana legislature. Its candidates on the general's ballot are marked
    "to runoff"; where no general followed, the leading candidates for the seats are taken as elected [inferred].
  - A contest on a general date whose parish and title (seats aside) were on that pair's primary is its deciding
    round, and takes the routes' classes, marked "deciding round after an earlier round" (the orchestrator's ruling of
    2026-11-07 09:53 UTC for North Carolina: "the November count is the one that elects") [inferred: the ruling's
    reason holds for Louisiana's generals; the orchestrator is told]. 2023-03-25 is both: the general of the
    93rd district's special and the spring primary; a contest on it is the deciding round where it was on 2023-02-18,
    else a first round.
  - A contest on a general date with no such primary in the source is recorded, p not computed, with that reason.
  - A contest on a date of neither kind: if the source holds it on the year's general already, it is a new election
    of that contest (2023-12-16: two contests whose generals of 2023-11-18 ended in exact ties, 178 to 178 and 224 to
    224, held again between the same two candidates [inferred: the source's workbooks; no law read]); else a special
    election [inferred]. Either way recorded, p not computed (a special election: the model's forecasts are fitted to
    regular elections). The tied general itself is its contest's deciding round and keeps its p, with a note.
  - The legislature (2023): the House and Senate on 2023-10-14 (first round) and 2023-11-18 (the deciding round) are
    written to data/state-lower/ and data/state-upper/ (legislature_records). The deciding round takes Klarner's
    runoff route (pipeline/local.py, route (d): like past runoffs of 1967-2022, classed "after an open or general first
    round" and by how far the first round's leader of the two led, from the first round's count), as Klarner's
    Louisiana runoffs of 2019 do. The 93rd district's special is recorded, p not computed.
  - A question has no rounds. Questions are kept as the source gives them, each date its own.
  - The parties' own committees (the Democratic and Republican state central and parish executive committees, DSCC,
    RSCC, DPEC and RPEC) are elected "every four years at the same time as the presidential preference primary
    election", and "the candidate who receives the greater number of votes cast shall be elected", seat by seat, ties
    by lot (La. R.S. 18:443(B) and 18:444(B), read 2026-11-07 at 11:16 UTC, Law.aspx?d=81577 and d=81580) [stated].
    So each is decided at 2024-03-23 in one round. They are kept (the orchestrator's ruling of 2026-11-07 10:35: "put
    the party committees in ... Mark them as party offices whose voters are the party's own, compute them where a
    route fits"), with `party_office` on the record and the routes of their seats and ballot like any local office,
    in an office type of their own, "party committee" (the orchestrator, 2026-11-07 11:30: "a like-race class must
    hold like races"). Their voters are the party's own [inferred: La. R.S. 18:1280.21(B), Law.aspx?d=81288, gives
    each elector at that primary only his own party's candidates; the ruling]. 2023 has none.
Left out: the presidency, its party primaries and Congress (D1's and D2's levels), and the governor (D2's).

  gate()         2024: the file's Democratic and Republican votes for president (D1's data/president/2024.json) and
                 each House district (D2's data/house/2024.json) against the certified ones on 2024-11-05: (worst
                 relative miss, words); the line is local_medsl.QUALITY_LINE, as for North Carolina and Indiana.
  source_gate()  2023: the gate within the certifying source, contest by contest (above).
  check()        the gates, and MEDSL's Louisiana contests of 2024-11-05 against the state's: data/local/check-la.json.
  medsl_shape()  the state's contests below the legislature in local_medsl's load() shape, or None if a file is
                 missing, not official on the site's list, or (2024) fails the gate.
  legislature_records()  2023's House and Senate, as records of the plan's layout.

Run:  VOTE_CACHE=/tmp/vote-cache python3 pipeline/local_la.py check   (fetches the posted results of 2023 once)
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
from intake import la_sos as SOS  # noqa: E402
import local as L  # noqa: E402
import local_medsl as LM  # noqa: E402

YEAR = 2024        # the year gated against the federal counts (gate)
ODD_YEARS = (2023,)   # gated within the certifying source (source_gate; the orchestrator, 2026-11-07 11:16)
YEARS = ODD_YEARS + (YEAR,)
SOURCE_KEY = "la_sos"
PAIRS = {2024: {"2024-04-27": "2024-03-23", "2024-12-07": "2024-11-05"},   # general date -> its primary (docstring)
         2023: {"2023-03-25": "2023-02-18", "2023-04-29": "2023-03-25", "2023-11-18": "2023-10-14"}}
PRIMARIES = {y: set(v.values()) for y, v in PAIRS.items()}
LEG_DATES = {2023: ("2023-10-14", "2023-11-18")}   # the legislature's regular election (docstring); others: special
LEG_OFFICE = {"State Representative": "state-lower", "State Senator": "state-upper"}
GOVERNOR = re.compile(r"^Governor$")
GATE_BY = "within the certifying source (no federal contest on the ballot)"   # the orchestrator's words, 11:16
POSTED = SOS.SITE + "ElectionResults/ElectionResults/Data?blob={ymd}/{what}_Multiparish.htm"
PARTY = {"DEM": "DEMOCRAT", "REP": "REPUBLICAN", "LBT": "LIBERTARIAN", "GRN": "GREEN", "IND": "INDEPENDENT",
         "NOPTY": "NO PARTY", "OTHER": "OTHER", "": "NONPARTISAN"}
FEDERAL = re.compile(r"^(Presidential Electors|Presidential Nominee|U\. S\. (Representative|Senator))")
PARTY_COMMITTEE = re.compile(r"^(DSCC|RSCC|DPEC|RPEC) Member")
COMMITTEES = {"DSCC": ("D", "the Democratic Party's state central committee", "18:443"),
              "RSCC": ("R", "the Republican Party's state central committee", "18:443"),
              "DPEC": ("D", "the Democratic Party's parish executive committee", "18:444"),
              "RPEC": ("R", "the Republican Party's parish executive committee", "18:444")}
LAW_URL = {"18:443": "https://legis.la.gov/Legis/Law.aspx?d=81577", "18:444": "https://legis.la.gov/Legis/Law.aspx?d=81580",
           "18:1280.21": "https://legis.la.gov/Legis/Law.aspx?d=81288", "18:402": "https://legis.la.gov/Legis/Law.aspx?d=81545"}
STATE_OFFICE = re.compile(r"^(District Judge|Judge, Court of Appeal|Justice, Supreme Court|PSC|District Attorney|"
                          r"BESE|Judge)")
N_PARISHES = 64
MEDSL_FIPS_FILE = os.path.join("medsl", "raw", "2024-13731147-2024-la-precinct-general.csv")


def load(year=YEAR):
    path = os.path.join(SOS.NORM, f"{year}.jsonl")
    if not os.path.exists(path):
        raise SystemExit(f"Louisiana's {year} file is not in the cache: run pipeline/intake/la_sos.py fetch and read "
                         f"--year {year}")
    with open(path) as f:
        return [json.loads(line) for line in f]


def checks_of(year=YEAR):
    with open(os.path.join(SOS.NORM, f"checks-{year}.json")) as f:
        return json.load(f)


def _key(s):
    return re.sub(r"[^A-Z]", "", s.upper())


def parish_fips():
    """Parish names to FIPS codes, from the county_name and county_fips columns of MEDSL's 2024 Louisiana file."""
    m = {}
    with open(os.path.join(F.CACHE, MEDSL_FIPS_FILE), newline="") as f:
        for row in csv.DictReader(f):
            m[_key(row["county_name"])] = row["county_fips"]
    return m, F.meta(MEDSL_FIPS_FILE)


def fips_source():
    _, fm = parish_fips()
    return F.source("parish FIPS codes: the county_name and county_fips columns of MEDSL's 2024 Louisiana precinct "
                    "file", fm["url"], fm["read_utc"], "CC0 1.0", mark="stated")


def _major(party):
    return {"DEM": "D", "REP": "R"}.get(party)


def _cert_major(party):
    """D1's and D2's party words ('Democratic', 'D', ...), as local_in's _major reads them."""
    p = (party or "").upper()
    return "D" if p in ("D", "DEM", "DEMOCRAT", "DEMOCRATIC") else "R" if p in ("R", "REP", "REPUBLICAN") else None


def _house_district(title):
    m = re.search(r"(\d+)(st|nd|rd|th) Congressional District", title)
    return int(m.group(1)) if m else None


def gate(cs=None):
    """(worst relative miss, words) of the file's D and R votes on 2024-11-05 against D1's and D2's certified
    counts."""
    cs = [c for c in (cs or load()) if c["date"] == "2024-11-05"]
    worst, what = 0.0, []
    for pat, level in (("Presidential Electors", "president"), ("U. S. Representative", "house")):
        mine = [c for c in cs if c["office"].startswith(pat)]
        with open(os.path.join(L.REPO, "data", level, f"{YEAR}.json")) as f:
            cert = [x for x in json.load(f)["contests"] if x["place"]["state"] == "LA" and not x.get("special")]
        if level == "house":
            byd = {int(x["place"]["district"]): x for x in cert}
            pairs = [([c], [byd[_house_district(c["title"])]]) for c in mine if _house_district(c["title"]) in byd]
        else:
            pairs = [(mine, cert)]
        for side in ("D", "R"):
            a = sum(x["votes"] for m_, _ in pairs for c in m_ for x in c["candidates"] if _major(x["party"]) == side)
            b = sum(x["votes"] for _, c_ in pairs for c in c_ for x in c["result"]["candidates"]
                    if _cert_major(x.get("party")) == side)
            if not b:
                continue
            what.append(f"{level} {side} {a:,} against {b:,}" + (f" ({len(pairs)} districts)" if level == "house" else ""))
            for m_, c_ in pairs:
                aa = sum(x["votes"] for c in m_ for x in c["candidates"] if _major(x["party"]) == side)
                bb = sum(x["votes"] for c in c_ for x in c["result"]["candidates"] if _cert_major(x.get("party")) == side)
                if bb:
                    worst = max(worst, abs(aa - bb) / bb)
    return worst, "; ".join(what)


def _base(title):
    return SOS.SEATS.sub("", title)


def _yr(date):
    return int(date[:4])


def rounds(cs):
    """For each contest (by id()), its round: ("first", the general's date or None, that contest), ("deciding", the
    primary's date, that contest), ("general, no primary", None, None), ("again", the general's date, that contest)
    for a later election of a contest the source holds on the year's general, ("other date", None, None), or
    ("party committee", None, None); None for a question. A date both a general and a primary (2023-03-25) gives
    the deciding round where the contest was on the earlier primary, else the first."""
    on = collections.defaultdict(dict)
    for c in cs:
        if c["kind"] == "office":
            on[("multi" if c["multi_parish"] else c["sheet"], _base(c["title"]))][c["date"]] = c
    out = {}
    for c in cs:
        if c["kind"] != "office":
            out[id(c)] = None
            continue
        if PARTY_COMMITTEE.match(c["office"]):   # one round, the most votes elected (La. R.S. 18:443, 18:444)
            out[id(c)] = ("party committee", None, None)
            continue
        k = ("multi" if c["multi_parish"] else c["sheet"], _base(c["title"]))
        pairs, prim = PAIRS[_yr(c["date"])], PRIMARIES[_yr(c["date"])]
        if c["date"] in pairs and pairs[c["date"]] in on[k]:
            p = pairs[c["date"]]
            out[id(c)] = ("deciding", p, on[k][p])
        elif c["date"] in prim:
            g = next((d for d, p in pairs.items() if p == c["date"] and d in on[k]), None)
            out[id(c)] = ("first", g, on[k].get(g))
        elif c["date"] in pairs:
            out[id(c)] = ("general, no primary", None, None)
        else:
            g = max((d for d in on[k] if d in pairs and d < c["date"]), default=None)
            out[id(c)] = ("again", g, on[k][g]) if g else ("other date", None, None)
    return out


def _tied(c):
    order = sorted(c["candidates"], key=lambda x: -x["votes"])
    k = c["seats"]
    return len(order) > k and order[k - 1]["votes"] == order[k]["votes"]


def _won(c, r):
    """The source marks no winners. A first round's candidates on the general's ballot go "to runoff"; any who led
    them all were elected in it; where no general followed, the leaders for the seats were [inferred]. Elsewhere, the
    leaders for the seats, none at a tie for the last (local_medsl's rule)."""
    order = sorted(c["candidates"], key=lambda x: -x["votes"])
    k = c["seats"]
    if r and r[0] == "first" and r[2] is not None:
        later = {x["name"] for x in r[2]["candidates"]}
        top = max((x["votes"] for x in order if x["name"] in later), default=0)
        return {x["name"]: ("to runoff" if x["name"] in later else True if x["votes"] > top else None) for x in order}
    winners = set() if _tied(c) else {x["name"] for x in order[:k]}
    return {x["name"]: (True if x["name"] in winners else None) for x in order}


def election_words(r, date):
    pairs, prim = PAIRS[_yr(date)], PRIMARIES[_yr(date)]
    if r is None:
        return "election" + (" (Louisiana's primary date)" if date in prim and date not in pairs else
                             " (Louisiana's general election date)" if date in pairs and date not in prim else
                             " (Louisiana's general election date and primary date)" if date in pairs else "")
    if r[0] == "first":
        return (f"first round: Louisiana's primary, its general election followed on {r[1]}" if r[1] else
                "first round: Louisiana's primary, decided in it (no general election of this contest followed)") + \
            " [inferred]"
    if r[0] == "party committee":
        return ("the party's own election of its committee's members, held with the presidential preference primary "
                "and decided in it: the most votes are elected (La. R.S. 18:443, 18:444) [stated]")
    if r[0] == "deciding":
        return f"deciding round after an earlier round on {r[1]} (Louisiana's general election after its primary) " \
               f"[inferred]"
    if r[0] == "again":
        return (f"a new election of this contest, after its general election on {r[1]}"
                + (" ended in an exact tie" if _tied(r[2]) else "") + " [inferred]")
    if r[0] == "other date":
        return "a date that is neither a primary nor a general of the year's pairs in the source: a special " \
               "election [inferred]"
    return "Louisiana's general election date, with no primary of this contest in the source [inferred]"


def held_round(r, date):
    """Why a candidate contest's round gets no p, or None."""
    if r is None:
        return None
    if r[0] == "first":
        return ("the first round of Louisiana's two-round system: a vote there works through who is elected "
                "outright or advances (model section 7); recorded, p not computed")
    if r[0] == "general, no primary":
        return ("on Louisiana's general election date, with no primary of this contest in the source, so which "
                "round it is cannot be read: p not computed")
    if r[0] in ("again", "other date"):
        return ("a special election (" + election_words(r, date).split(" [")[0] + "): the model's own "
                "forecasts are fitted to regular elections; recorded, p not computed")
    return None


def tie_note(c, r, later):
    """A deciding round that ended in an exact tie and was held again (rounds: "again")."""
    if r and r[0] == "deciding" and _tied(c) and later:
        return (f"an exact tie: no one was elected at this count, and the source holds a new election of the same "
                f"contest on {later} [inferred: the source's workbooks]")
    return None


# ------------------------------------------------------------------ 2023: the gate within the certifying source

def _posted_name(date, what):
    return f"la_sos/raw/{date.replace('-', '')}-{what}_Multiparish.json"


def _list(x):
    """The site's files give a lone element as an object, not a list of one (2023-02-18's one race)."""
    return x if isinstance(x, list) else [x]


def posted(date):
    """The Secretary of State's own posted results of `date` for the contests on more than one parish's ballot:
    {title: {"seats": n, "votes": {choice: votes}}}, and the two files' metadata. Fetched once (pipeline/fetch.py)."""
    ymd = date.replace("-", "")
    paths = {w: F.fetch(POSTED.format(ymd=ymd, what=w), _posted_name(date, w)) for w in ("RacesCandidates", "Votes")}
    with open(paths["RacesCandidates"], encoding="utf-8-sig") as f:
        races = _list(json.load(f)["Races"]["Race"])
    with open(paths["Votes"], encoding="utf-8-sig") as f:
        votes = {x["ID"]: {ch["ID"]: int(ch["VoteTotal"]) for ch in _list(x["Choice"])}
                 for x in _list(json.load(f)["Races"]["Race"])}
    out = {}
    for x in races:
        v = votes.get(x["ID"], {})
        out[" ".join(x["SpecificTitle"].split())] = {
            "seats": int(x["NumberToBeElected"] or 1),
            "votes": {SOS._choice(ch["Desc"])[0]: v.get(ch["ID"]) for ch in _list(x["Choice"])}}
    return out, {w: F.meta(_posted_name(date, w)) for w in paths}


def source_gate(cs, year):
    """{id(contest): (held reason or None, the record's gate words)} by the orchestrator's gate of 2026-11-07 11:16
    for a year with no federal contest on the ballot, and the tallies for the check."""
    meta = checks_of(year)
    out, t, files = {}, collections.Counter(), {}
    post = {}
    for d in sorted({c["date"] for c in cs if c["multi_parish"]}):
        post[d], fm = posted(d)
        files[d] = {w: {"url": m["url"], "read_utc": m["read_utc"], "sha256": m["sha256"]} for w, m in fm.items()}
    for c in cs:
        official = meta["files"][c["date"]].get("official") == "1"
        rec = {"by": GATE_BY, "ruled": "the orchestrator, 2026-11-07 11:16 UTC",
               "official": official, "parts_add_up": c["lines_add_up"]}
        why = []
        if not official:
            why.append("its date is not marked official on the site's list")
        if not c["lines_add_up"]:
            why.append("its parishes' or precincts' lines do not add up to its total in the workbook")
        if c["multi_parish"]:
            hit = post[c["date"]].get(_base(c["title"]))
            mine = {x["name"]: x["votes"] for x in c["candidates"]}
            if hit is None:
                rec["posted_results"] = "not found in the posted results of its date"
                why.append("it is not found by its title in the Secretary of State's posted results of its date")
            elif hit["votes"] != mine or hit["seats"] != c["seats"]:
                miss = sum(abs((hit["votes"].get(n) or 0) - v) for n, v in mine.items())
                rec["posted_results"] = f"differ by {miss:,} votes over its choices"
                why.append(f"its counts differ from the Secretary of State's posted results of its date by {miss:,} "
                           f"votes over its choices")
            else:
                rec["posted_results"] = "equal, choice by choice"
            t[f"{c['date']} multi-parish: posted results " + rec["posted_results"].split(",")[0].split(" by ")[0]] += 1
        else:
            rec["posted_results"] = ("not compared: one parish's own contest (the posted multi-parish results hold "
                                     "the contests on more than one parish's ballot)")
        t["parts add up" if c["lines_add_up"] else "parts do not add up"] += 1
        held = None
        if why:
            held = ("held by the gate within the certifying source (the orchestrator, 2026-11-07 11:16): "
                    + "; ".join(why) + "; p not computed")
            t["held"] += 1
        out[id(c)] = (held, rec)
    return out, {"tallies": dict(sorted(t.items())), "posted_files": files}


def _ready(year):
    """(contests, the files' metadata) of a year whose every date is marked official on the site's list, else None."""
    if year not in YEARS or not os.path.exists(os.path.join(SOS.NORM, f"{year}.jsonl")):
        return None
    cs, meta = load(year), checks_of(year)
    if any(f.get("official") != "1" for f in meta["files"].values()):
        return None
    return cs, meta


def _again(cs, rd):
    """id(general) -> the date of its later election (rounds: "again")."""
    return {id(r[2]): c["date"] for c in cs if (r := rd[id(c)]) and r[0] == "again"}


def medsl_shape(year=YEAR):
    """Louisiana's contests of `year` below the legislature (not federal, not the governor, not the legislature) in
    local_medsl's load() shape; None if the file is missing, a date is not official, or (2024) the file fails the
    gate. 2023's carry the gate within the certifying source contest by contest (source_gate)."""
    got = _ready(year)
    if got is None or (year == YEAR and gate(got[0])[0] > LM.QUALITY_LINE):
        return None
    cs, meta = got
    sg = source_gate(cs, year)[0] if year in ODD_YEARS else {}
    fips, _ = parish_fips()
    rd = rounds(cs)
    again = _again(cs, rd)
    out = []
    for c in cs:
        if FEDERAL.match(c["office"]) or GOVERNOR.match(c["office"]) or c["office"] in LEG_OFFICE:
            continue
        fm = meta["files"][c["date"]]
        parishes = sorted({fips[_key(p)] for p in c["parishes"] if _key(p) in fips})
        statewide = len(parishes) == N_PARISHES
        r = rd[id(c)]
        title = ", ".join(x for x in (c["office"], c["place"]) if x).upper()   # "MAYOR, TOWN OF MELVILLE"
        base = {"state": "LA", "date": c["date"], "stage": "GEN", "special": False, "subject": None,
                "precincts": None, "counties": parishes, "source": SOURCE_KEY, "id_date": True,
                "election_words": election_words(r, c["date"]),
                "file": {"name": fm["url"].rsplit("/", 1)[1], "url": fm["url"], "read_utc": fm["read_utc"],
                         "sha256": fm["sha256"]}}
        if id(c) in sg:
            base["source_gate"] = {"held": sg[id(c)][0], "record": sg[id(c)][1]}
        if c["kind"] == "question":
            amendment = c["office"].startswith("CA No.")
            out.append(dict(base, dataverse="STATE" if statewide else "LOCAL", office=title,
                            district="STATEWIDE" if statewide else "", magnitude=None, question=True,
                            question_type="Constitutional Amendment" if amendment and statewide else None,
                            candidates=[{"name": re.sub(r"^(FOR|AGAINST)\s*RECALL$", r"\1 RECALL", x["name"].upper()),
                                         "votes": x["votes"]} for x in c["candidates"]]))   # "ForRecall": a recall
            continue
        won = _won(c, r)
        cands = [{"name": x["name"], "votes": x["votes"], "as_named": True, "won_marked": won[x["name"]],
                  "party": PARTY.get(x["party"], x["party"])} for x in c["candidates"]]
        rec = dict(base, dataverse="STATE" if (statewide or STATE_OFFICE.match(c["office"])) else "LOCAL",
                   office=title, district="STATEWIDE" if statewide else "", magnitude=c["seats"],
                   question=False, candidates=cands, held_round=held_round(r, c["date"]),
                   earlier_round=[r[1]] if r and r[0] == "deciding" else None)
        tn = tie_note(c, r, again.get(id(c)))
        if tn:
            rec["notes"] = [tn]
        if r and r[0] == "party committee":
            side, body, sec = COMMITTEES[c["office"].split()[0]]
            rec["party_office"] = {"party": side, "body": body, "law": f"La. R.S. {sec}", "law_url": LAW_URL[sec],
                                   "voters": "the party's own [inferred: La. R.S. 18:1280.21(B); the orchestrator's "
                                             "ruling of 2026-11-07 10:35]"}
        out.append(rec)
    return out


RUNOFF_KIND = "after an open or general first round"   # pipeline/local.py RUNOFF_KIND["larunoff"]
FIRST_ROUND_WHY = ("the first round of a two-round system: a vote there works through who advances (model section 7); "
                   "recorded, p not computed")   # pipeline/local.py structure(), for Klarner's Louisiana first rounds


def runoff_key(c, first):
    """pipeline/local.py's runoff_key for a Louisiana general after its primary: the kind, and how far ahead the first
    round's leader of the two finished in the first round (their share of the two's first-round votes)."""
    two = sorted(LM.ballot(c["candidates"]), key=lambda x: -x["votes"])[:2]
    v = {x["name"]: x["votes"] for x in first["candidates"]} if first else {}
    got = [v.get(x["name"]) for x in two]
    if len(two) == 2 and all(g is not None for g in got) and sum(got) > 0:
        s = max(got) / sum(got)
        return (f"runoff {RUNOFF_KIND}, first-round leader of the two within 10 points" if s < 0.55 else
                f"runoff {RUNOFF_KIND}, first-round leader of the two ahead by 10 points or more")
    return f"runoff {RUNOFF_KIND}, first round not found in the source"


def _district(place):
    m = re.match(r"(\d+)(st|nd|rd|th) (Representative|Senatorial) District$", place or "")
    return m.group(1) if m else None


def legislature_records(year, ktrain, kdens, cid, commit, with_p, counts):
    """{(level, year, "LA"): [records]}: the year's House and Senate (2023) in the layout pipeline/local_medsl.py
    writes for MEDSL's 2024 legislatures. The deciding round takes Klarner's runoff route on Klarner's like past
    runoffs of earlier years (ktrain: pipeline/local.py class_rows); the first round and the special are recorded,
    p not computed."""
    got = _ready(year) if year in ODD_YEARS else None
    if got is None:
        return {}
    cs, meta = got
    sg, _ = source_gate(cs, year)
    rd = rounds(cs)
    train = [r_ for r_ in ktrain if r_["year"] < year]
    out = collections.defaultdict(list)
    for c in cs:
        level = LEG_OFFICE.get(c["office"])
        if level is None:
            continue
        dist = _district(c["place"])
        r = rd[id(c)]
        special = c["date"] not in LEG_DATES[year]
        won = _won(c, r)
        cands = [{"name": x["name"], "votes": x["votes"], "as_named": True, "won_marked": won[x["name"]],
                  "party": PARTY.get(x["party"], x["party"])} for x in c["candidates"]]
        rec = {"id": cid(f"{year}-{level}-LA-{dist or L._slug(c['place'] or '')}-{c['date']}"
                         + ("-special" if special else "")),
               "year": year, "date": c["date"], "level": level, "place": {"state": "LA", "district": dist},
               "election": ("special election: " if special else "") + election_words(r, c["date"]),
               "seats": c["seats"] if c["seats"] > 1 else None,
               "result": {"candidates": LM._cands_out(cands, c["seats"]),
                          "total_votes": sum(x["votes"] for x in c["candidates"]), "source": SOURCE_KEY},
               "forecasts": [], "gate": sg[id(c)][1]}
        label = f"{level} {year}"
        b = LM.ballot(c["candidates"])
        if sg[id(c)][0]:
            p = {"not_computed": sg[id(c)][0]}
            counts[f"{label}: not computed, held by the gate"] += 1
        elif special:
            p = {"not_computed": "a special election: the model's own forecasts are fitted to regular elections"}
            counts[f"{label}: not computed, special"] += 1
        elif len(b) <= c["seats"]:
            p = {"value": 0.0, "event": 0.0, "reason": "one name on the ballot for each seat (unopposed): p is 0"}
            counts[f"{label}: p = 0"] += 1
        elif r and r[0] == "first":
            p = {"not_computed": FIRST_ROUND_WHY}
            counts[f"{label}: not computed, first round"] += 1
        elif r and r[0] == "deciding" and c["seats"] == 1:
            key = runoff_key(c, r[2])
            shape = {"candidates": cands}
            p = LM.class_p(rec, shape, "runoff", key, train, kdens, (year, key), commit, with_p, counts, label, 1)
            if rec["forecasts"]:
                rec["forecasts"][-1]["note"] = ("the second round of a runoff, its own two-way race, from like past "
                                                f"runoffs (Klarner's returns of {min(r_['year'] for r_ in train)}-"
                                                f"{max(r_['year'] for r_ in train)})")
            if p.get("under"):
                p["under"] = f"the model's own ({L.METHOD}), like past runoffs"
        else:
            p = {"not_computed": held_round(r, c["date"]) or f"no forecast route applies (a structure {L.METHOD} "
                                                               f"does not cover)"}
            counts[f"{label}: not computed, {(r or ('?',))[0]}"] += 1
        rec["p"] = p
        out[(level, year, "LA")].append(rec)
    return dict(out)


def source_block(year=YEAR):
    meta = checks_of(year)
    files = "; ".join(f"{d} ({f['url'].rsplit('/', 1)[1]}, sha256 {f['sha256'][:12]}, {f['contests']} contests)"
                      for d, f in sorted(meta["files"].items()))
    read = max(f["read_utc"] for f in meta["files"].values())
    note = (f"each date marked official on the site's list of elections ('ResultsOfficial': '1'); files read by "
            f"pipeline/intake/la_sos.py: {files}")
    if year in ODD_YEARS:
        posted_ = sorted({d for d in meta["files"] if os.path.exists(os.path.join(F.CACHE, _posted_name(d, "Votes")))})
        note += ("; gated within the certifying source against the site's own posted results of the contests on more "
                 "than one parish's ballot (" + ", ".join(
                     f"{d}: {F.meta(_posted_name(d, 'Votes'))['url']}, read {F.meta(_posted_name(d, 'Votes'))['read_utc']}"
                     for d in posted_) + ")")
    return F.source("Louisiana Secretary of State, official election results (the results site's workbook of each "
                    "date)", SOS.SITE, read, SOS.LICENCE, mark="stated", note=note)


def _sig(cands):
    return tuple(sorted((x["votes"] for x in cands if not LM._is_generic(x["name"]) and not x.get("writein")),
                        reverse=True))


def check():
    cs = load()
    w, words = gate(cs)
    rd = rounds(cs)
    t = collections.Counter()
    for c in cs:
        if FEDERAL.match(c["office"]):
            t["left out: the presidency, its primaries and Congress"] += 1
        else:
            r = rd[id(c)]
            t[f"{c['date']}: " + ("question" if r is None else r[0])] += 1
    # MEDSL's Louisiana contests of 2024-11-05, held back: the same names, and how far their votes fall short
    med = []
    for p in sorted(os.listdir(os.path.join(LM.NORM, str(YEAR)))):
        if p.startswith("LA-"):
            with open(os.path.join(LM.NORM, str(YEAR), p)) as f:
                med += [json.loads(ln) for ln in f]
    mine = {}
    for c in cs:
        if c["date"] == "2024-11-05":
            mine.setdefault(frozenset(LM.name_key(x["name"]) for x in c["candidates"]), []).append(c)
    m_t, ratios = collections.Counter(), []
    for m in med:
        if "state" not in m or m.get("dataverse") not in ("STATE", "LOCAL") or m["office"] in LM.LEG:
            continue
        names = frozenset(LM.name_key(x["name"]) for x in m["candidates"] if not LM._is_generic(x["name"])
                          and not x.get("writein"))
        hit = mine.get(names)
        if not hit:
            m_t["MEDSL: not found by its candidates' names in the state's file"] += 1
            continue
        a, b = sum(x["votes"] for x in m["candidates"]), sum(x["votes"] for x in hit[0]["candidates"])
        m_t["MEDSL: found"] += 1
        if b:
            ratios.append(a / b)
    ratios.sort()
    out = {"about": "Louisiana's official 2024 results (pipeline/intake/la_sos.py) against the certified federal "
                    "counts, and MEDSL's 2024 Louisiana contests against them. Built by pipeline/local_la.py check.",
           "gate": {"worst_miss": round(w, 6), "fails": w > LM.QUALITY_LINE, "counts": words},
           "contests": dict(sorted(t.items())),
           "medsl_2024_11_05": dict(m_t, medsl_votes_over_the_states_median=round(ratios[len(ratios) // 2], 4)
                                    if ratios else None)}
    for y in ODD_YEARS:
        out[str(y)] = check_odd(y)
    with open(os.path.join(L.REPO, "data", "local", "check-la.json"), "w") as f:
        json.dump(out, f, indent=1)
        f.write("\n")
    return out


def check_odd(year):
    """The year's gate within the certifying source, and its contests by round and level."""
    got = _ready(year)
    if got is None:
        return {"read": False, "why": "a file is missing from the cache or a date is not marked official"}
    cs, meta = got
    _, g = source_gate(cs, year)
    rd = rounds(cs)
    t = collections.Counter()
    gov = []
    for c in cs:
        r = rd[id(c)]
        if GOVERNOR.match(c["office"]):
            t["left out: the governor (D2's level; data/governor/ holds even years only)"] += 1
            gov.append(c["date"])
            continue
        lv = LEG_OFFICE.get(c["office"], "question" if c["kind"] == "question" else "local")
        t[f"{c['date']} {lv}: " + ("question" if r is None else r[0])] += 1
    ties = [{"general": r[1], "again": c["date"], "contest": f"{r[2]['sheet']}: {r[2]['title']}",
             "general_votes": [x["votes"] for x in r[2]["candidates"]], "again_votes": [x["votes"] for x in c["candidates"]]}
            for c in cs if (r := rd[id(c)]) and r[0] == "again"]
    return {"about": f"Louisiana's official {year} results: no federal contest on the ballot, so the gate is within "
                     f"the certifying source (the orchestrator, 2026-11-07 11:16): (a) each date official on the site's "
                     f"list, (b) each contest's parishes or precincts add up to its total, (c) each contest on more "
                     f"than one parish's ballot equals the Secretary of State's own posted results of its date "
                     f"(ruled for the statewide offices of {LEG_DATES[year][0]}; applied to every multi-parish "
                     f"contest). A contest failing (b) or (c) is held.",
            "official": {d: f.get("official") == "1" for d, f in sorted(meta["files"].items())},
            "gate": g, "contests": dict(sorted(t.items())), "held_again": ties}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("what", choices=["check"])
    ap.parse_args()
    print(json.dumps(check(), indent=1))


if __name__ == "__main__":
    main()
