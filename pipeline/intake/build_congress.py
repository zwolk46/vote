"""pipeline/intake/build_congress.py: build data/senate/<year>.json, data/house/<year>.json and
data/governor/<year>.json from the normalized caches the other intake scripts write.

Written 2026-11-07 by worker D2. Reads only the cache (CACHE); run the source scripts first:
  fec_federal_elections.py <year>      House and Senate results, 2006-2022 (the source of record)
  clerk_statistics.py 2024             House and Senate results, 2024 (the source of record)
  candidates_american_general_elections.py   governors (the source of record), and the check on House
                                             and Senate, with incumbency for every year
  medsl_dataverse.py senate president  the check on Senate results; state presidential vote
  downballot_pres_by_cd.py             district presidential vote
  nara_electoral_college.py            president's party
  algara_amlani.py governors           governors of 1978-2004 (the source of record before Cha's 2006), and of the
                                       odd years 1977-2005 (and a contest Cha does not hold, or holds only its winner)
  la_sos_governor.py 2023              Louisiana's governor of 2023, from the Secretary of State (D3's reader)
  ms_governor_rule.py                  Mississippi's rule for electing its governor before 2020 (HC 47 of 2020)
  state_governors.py 2023 2025         New Jersey's and Virginia's governors of 2025 from the states' certified
                                       results, and the refusals of Kentucky's and Mississippi's 2023 results

What it writes for each contest (plan section 3, with the fields data/README.md adds):
  result     from the source of record, every candidate and line it prints;
  checks     the same contest in the check source, and every difference between the two (plan 3a);
  forecast_inputs   what the model's own forecast is built from (pipeline/chambers.py);
  p          not yet computed where the forecast is needed (the method waits on the orchestrator's
             approval, brief step 2); 0 where only one candidate ran; "not computed" with the reason where
             the structure is one the model does not yet compute (model section 7: runoffs, ranked choice).

Run:  python3 pipeline/intake/build_congress.py <year> [<year> ...]
"""
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import congress_common as cc  # noqa: E402
from downballot_pres_by_cd import LEAN_INPUT  # noqa: E402
import chambers  # noqa: E402  (pipeline/chambers.py: the governors' last race, read the same way as the fit's)

COMMIT = chambers.git_head()   # the commit of the code that writes a p = 0 block (M2 1.5)
GOV_INDEX = None

ELECTION_DAY = {2006: "2006-11-07", 2008: "2008-11-04", 2010: "2010-11-02", 2012: "2012-11-06",
                2014: "2014-11-04", 2016: "2016-11-08", 2018: "2018-11-06", 2020: "2020-11-03",
                2022: "2022-11-08", 2024: "2024-11-05"}
FEC_DOC = {2006: "https://www.fec.gov/introduction-campaign-finance/election-results-and-voting-information/federal-elections-2006/"}
D_LABELS = {"D", "DEM", "DFL", "DNL", "DEMOCRAT", "DEMOCRATIC", "DEMOCRATIC-FARMER-LABOR",
            "DEMOCRATIC-NONPARTISAN LEAGUE", "DEMOCRATIC-NPL"}
R_LABELS = {"R", "REP", "REPUBLICAN"}
# ranked-choice general elections: Maine for Congress from 2018, Alaska for every office from 2022
RCV = {("ME", "senate"): 2018, ("ME", "house"): 2018, ("AK", "senate"): 2022, ("AK", "house"): 2022,
       ("AK", "governor"): 2022}
NOT_COMPUTED = "not computed"


def general_election_day(year):
    """The Tuesday after the first Monday in November (2 U.S.C. 7 for Congress; the even-year governor elections
    of 1978-2004 that Algara and Amlani hold were held with the general election)."""
    import datetime
    d = datetime.date(year, 11, 1)
    first_monday = d + datetime.timedelta(days=(0 - d.weekday()) % 7)
    return (first_monday + datetime.timedelta(days=1)).isoformat()


for _y in range(chambers.GOV_FROM, 2006, 2):
    ELECTION_DAY[_y] = general_election_day(_y)
# the odd years (the orchestrator, 2026-11-07 12:01): Kentucky, Mississippi, New Jersey and Virginia hold the governor's
# election on the same Tuesday of November (inferred; for Mississippi section 140 of its Constitution says so, as HC 47
# of 2020 prints it). Louisiana's rounds are on Saturdays of October and November, a date each record gives or lacks
for _y in chambers.ODD_YEARS:
    ELECTION_DAY[_y] = general_election_day(_y)
ODD_STATES = chambers.ODD_STATES
LA_GOV = ("Louisiana elects its governor in an open primary: a candidate with a majority is elected, else the two "
          "leaders meet in a runoff weeks later; the record is the deciding round, a first round or a runoff, and p is "
          "not computed for either (model section 7: two-round systems and runoffs are not yet computed; as for the "
          "state's congressional elections)")
OFF_CYCLE = ("a governor election in an odd year in a state that elects its governor in even years (a special election, "
             "or the later round of an even year's election) [inferred: every other governor election of the state in "
             "the sources is in an even year]; the sources read here give no date for it, and the model's forecasts are "
             "fitted to the regular general elections")
MS_RULE_URL = "https://billstatus.ls.state.ms.us/documents/2020/html/HC/HC0047SG.htm"
MS_BEFORE_2020 = (
    "Mississippi's governor needed two majorities until the amendment of 2020: the candidate with the most votes in "
    "each county or House district was \"holden to have received as many votes as such county or district is "
    "entitled to members in the House of Representatives, which last named votes are hereby designated 'electoral "
    "votes'\", and \"The person found to have received a majority of all the electoral votes, and also a majority of "
    "the popular vote, shall be declared elected\"; else \"the House of Representatives shall proceed to choose a "
    "Governor from the two persons who shall have received the highest number of popular votes\" (Constitution of "
    "1890, sections 140 and 141, as the Legislature's House Concurrent Resolution 47 of 2020 prints them, struck and "
    "repealed; source ms_hc47_2020). So one vote can decide by crossing the popular majority line or by changing a "
    "district's electoral vote, which the tie form does not measure, and p is not computed (the orchestrator, "
    "2026-11-07 12:11)")
MS_FROM_2023 = ("Mississippi's governor needs a majority since the amendment of 2020, else a runoff (section 140 as HC 47 "
                "of 2020 proposed it: \"If no person receives a majority of the votes, then a runoff election shall be "
                "held\"); with three or more candidates with votes this is a first round (model section 7; the "
                "orchestrator, 2026-11-07 12:11)")


def governor_structure(year, state, n_voted, special):
    """The reason p is not computed for a governor contest of a structure the model does not compute, else None:
    Louisiana's two rounds, Mississippi's two majorities before 2020 (and a first round after), and an odd-year
    contest outside the five states that elect their governors in odd years."""
    if year % 2 and (state not in ODD_STATES or special):
        return OFF_CYCLE
    if state == "LA":
        return LA_GOV
    if state == "MS" and year <= 2019:
        return MS_BEFORE_2020
    if state == "MS" and n_voted >= 3:
        return MS_FROM_2023
    return None
SOURCE_POOL = {}
SOURCES = {}      # the file's top-level "sources": blocks that fields of this script's own name by key


def major(parties):
    """'D', 'R' or None from a candidate's party lines (FEC codes or the Clerk's names). A write-in line
    such as 'W(D)' or 'Write-in (Democratic)' is not a nomination."""
    for p in parties or []:
        for part in re.split(r"[/,]", p):
            q = part.strip().rstrip("*").upper()
            if q.startswith("W(") or q.startswith("WRITE"):
                continue
            if q in D_LABELS:
                return "D"
            if q in R_LABELS:
                return "R"
    return None


def last_name(name):
    """'Warnock, Raphael' / 'Raphael Warnock' / 'WARNOCK, RAPHAEL GAMALIEL' -> 'WARNOCK'."""
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().upper().replace(".", "")
    if "," in s:
        return s.split(",")[0].strip().split()[-1]
    toks = [t for t in s.replace(",", " ").split() if t not in ("JR", "SR", "II", "III", "IV")]
    return toks[-1] if toks else s


# ----------------------------------------------------------------------------- sources of record
def record_contests(year):
    """Senate and House contests from the source of record for the year, in one shape:
    {office, state, district, special, candidates[{name, party, parties, votes, incumbent?, scattered}],
     other_lines, printed_total, runoff, source, notes}"""
    out = []
    if year == 2024:
        k = cc.read_json(os.path.join(cc.CACHE, "clerk", "normalized", "2024.json"))
        f = k["file"]
        src = cc.source_block("Clerk of the House, Statistics of the Presidential and Congressional Election "
                              "of November 5, 2024 (published 2025-03-10), from official sources",
                              f["url"], f["read_utc"], "a publication of the U.S. House; no licence printed",
                              mark="stated", note=f"sha256 {f['sha256'][:16]}")
        for c in k["contests"]:
            if c["state"] not in cc.STATES_50:
                continue
            cands = [{"name": a["name"], "party": "/".join(a["parties"]), "parties": a["parties"],
                      "votes": a["votes"], "unopposed": a["votes"] is None, "scattered": False}
                     for a in c["candidates"]]
            others = [{"name": o["label"], "party": None, "parties": [], "votes": o["votes"], "scattered": True}
                      for o in c["other_lines"]]
            total = sum((a["votes"] or 0) for a in cands + others)
            out.append({"office": c["office"], "state": c["state"], "district": c["district"],
                        "special": c["special"], "candidates": cands + others, "printed_total": None,
                        "computed_total": total, "runoff": None, "source": src, "notes": list(c["notes"])})
        return out
    d = cc.read_json(os.path.join(cc.CACHE, "fec", "normalized", f"{year}.json"))
    if d is None:
        raise SystemExit(f"run pipeline/intake/fec_federal_elections.py {year} first")
    f = d["file"]
    src = cc.source_block(f"Federal Election Commission, Federal Elections {year}: Election Results for the "
                          f"U.S. Senate and the U.S. House of Representatives (official results)",
                          f["url"], f["read_utc"], "US federal public record; the FEC prints no licence",
                          mark="stated", note=f"sha256 {f['sha256'][:16]}")
    for c in d["contests"]:
        if c["state"] not in cc.STATES_50:
            continue
        cands = []
        runoff = []
        for a in c["candidates"]:
            cands.append({"name": a["name"], "party": "/".join(a["parties"]), "parties": a["parties"],
                          "votes": a["votes"], "incumbent_fec": a["incumbent"], "scattered": a["scattered"],
                          "unopposed": a["votes"] is None and (a.get("text") or "").lower().startswith("unopposed"),
                          "fec_id": a["fec_id"]})
            if a.get("runoff_votes"):
                runoff.append({"name": a["name"], "party": "/".join(a["parties"]), "votes": a["runoff_votes"]})
        out.append({"office": c["office"], "state": c["state"], "district": c["district"],
                    "special": c["special"], "candidates": cands, "printed_total": c["printed_total"],
                    "computed_total": sum((a["votes"] or 0) for a in cands),
                    "runoff": ({"candidates": runoff, "total": c.get("printed_runoff_total")} if runoff else None),
                    "source": src, "notes": list(c["notes"])})
    return out


def cha_index():
    d = cc.read_json(os.path.join(cc.CACHE, "cha", "normalized", "contests.json"))
    if d is None:
        raise SystemExit("run pipeline/intake/candidates_american_general_elections.py first")
    idx = {}
    for c in d["contests"]:
        k = (c["year"], c["office"], c["state"], c["district"], c["special"])
        idx.setdefault(k, []).append(c)
    return d["source"], idx


def cha_source(info, office):
    origin = ("https://history.house.gov/Institution/Election-Statistics/Election-Statistics/"
              if office in ("house", "senate") else None)
    return cc.source_block(f"Cha, Kuriwaki and Snyder, Candidates in American General Elections, "
                           f"Harvard Dataverse doi:10.7910/DVN/DGDRDT, {info['version']}",
                           origin or "https://doi.org/10.7910/DVN/DGDRDT", info["file"]["read_utc"],
                           info["licence"], mark="stated", via="https://doi.org/10.7910/DVN/DGDRDT",
                           note=("governors' votes from each state's statement of votes (the dataset's guide)"
                                 if office == "governor" else "votes from the Clerk's Election Statistics (the "
                                 "dataset's guide); incumbency hand-coded by the authors"))


def match_cha(idx, year, office, state, district, special):
    """The Cha contest for this one; at-large House districts are numbered 1 there."""
    for d in ([district] + (["01"] if district == "AL" else [])):
        cs = idx.get((year, office, state, d, special))
        if cs:
            return [c for c in cs if not c["runoff"]] or cs
    return []


# ----------------------------------------------------------------------------- checks between sources
def compare(rec_cands, cha_c):
    """Differences between the source of record's candidates and Cha's, matched by cha_entry."""
    diffs = []
    if cha_c.get("runoff"):
        return ["the check source holds only the runoff, the deciding round (its guide); the November round "
                "is not checked"]
    for a in rec_cands:
        if a["scattered"] or a["votes"] is None:
            continue
        b = cha_entry(a, cha_c["candidates"])
        if b is None:
            if (a["votes"] or 0) >= 10:      # Cha leaves out candidates under ten votes
                diffs.append(f"{a['name']} ({a['votes']:,}) is not in the check source")
            continue
        if b["votes"] is not None and b["votes"] != a["votes"]:
            diffs.append(f"{a['name']}: {a['votes']:,} here, {b['votes']:,} in the check source "
                         f"({b['votes'] - a['votes']:+,})")
    return diffs


def first_name(name):
    """'Johnson, Dustin (Dusty)' / 'Dusty Johnson' -> 'DUSTIN' / 'DUSTY': the first given name, for telling apart
    two candidates of one last name."""
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().upper().replace(".", "")
    s = re.sub(r"\([^)]*\)", " ", s)
    toks = (s.split(",", 1)[1] if "," in s else s).split()
    return toks[0] if toks else ""


def cha_entry(a, cha_cands):
    """Cha's entry for the source of record's candidate a, within the contest matched on year, office, state,
    district and special (match_cha): the one of the same last name; among several of one last name, the one with
    the same votes, else the same first name; with no name to go by, the one candidate with the same votes. None
    where none is found or it stays ambiguous. Reason (M2's second pass, the orchestrator 2026-11-07 08:06): keyed
    by last name alone, a second candidate of that name overwrote the first (South Dakota at large 2024, the two
    Johnsons; Utah's Senate 2006, Orrin and Julian Hatch)."""
    same = [b for b in cha_cands if last_name(b["name"]) == last_name(a["name"])]
    if len(same) > 1:
        same = ([b for b in same if a["votes"] is not None and b["votes"] == a["votes"]]
                or [b for b in same if first_name(b["name"]) == first_name(a["name"])])
    if len(same) > 1 and len({(b["votes"], b["inc"]) for b in same}) == 1:
        # the source lists some candidates twice under two spellings with the same votes (Louisiana's Senate
        # 2022, "La Fontaine Olson" and "Olson"): one candidate
        return same[0]
    if len(same) == 1:
        return same[0]
    if same:
        return None
    by_votes = [b for b in cha_cands if a["votes"] and b["votes"] == a["votes"]]
    return by_votes[0] if len(by_votes) == 1 else None


def incumbency(rec_cands, cha_c, year):
    """inc = +1 if the Democratic nominee is an incumbent, -1 if the Republican nominee is, 0 otherwise, as the fit
    defines it (chambers.fit_rows; REPORT 2.2): Cha, Kuriwaki and Snyder's hand coding of the two nominees. The
    nominees are the race's two sides as structure() takes them: the candidate with the most votes on a Democratic
    line (or an independent who caucuses with the Democrats), and the one with the most votes on a Republican line;
    a write-in line is not a nomination (major). Each is found in Cha by cha_entry; where Cha does not hold the
    contest or the candidate, the source of record's own incumbent mark on that same nominee (the FEC, 2006-2022).
    Reason (M2's second pass, 08:06): the mark was taken from any candidate on a major line, so a candidate who was
    not the nominee set it (Crowley on New York 14's lines in 2018 after losing the primary; Bentivolio's write-in in
    Michigan 11, 2014)."""
    cha = cha_c["candidates"] if cha_c else []
    inc = {"D": 0, "R": 0}
    via = set()
    for side in ("D", "R"):
        on = [a for a in rec_cands if not a.get("scattered") and a["votes"]
              and (major(a["parties"]) == side or (side == "D" and major(a["parties"]) is None
                                                    and a.get("state_caucus_D")))]
        if not on:
            continue
        a = max(on, key=lambda x: x["votes"])
        b = cha_entry(a, cha)
        if b is not None and b["inc"] is not None:
            via.add("cha")
            inc[side] = 1 if b["inc"] == 1 else 0
        elif a.get("incumbent_fec"):
            via.add("fec")
            inc[side] = 1
    return inc["D"] - inc["R"], sorted(via)


# ----------------------------------------------------------------------------- structure
def structure(year, office, state, cands, special):
    """None if the race is a two-way race the model's own forecast covers; else (kind, reason)."""
    real = [a for a in cands if not a["scattered"]]
    voted = [a for a in real if a["votes"]]
    if len(real) == 1 or len(voted) <= 1:
        return ("uncontested", "only one candidate was on the ballot") if len(real) == 1 else \
            ("uncontested", "only one candidate received votes")
    if office == "governor":
        why = governor_structure(year, state, len(voted), special)
        if why:
            return (NOT_COMPUTED, why)
    if state == "LA" and office in ("house", "senate"):
        return (NOT_COMPUTED, "Louisiana's congressional election in November is an open primary: a "
                "majority wins outright, else the top two meet in a December runoff (model section 7)")
    if state == "GA" and len(voted) >= 3:
        return (NOT_COMPUTED, "Georgia requires a majority; with three or more candidates a runoff can "
                "follow (model section 7: runoffs are not yet computed)")
    if (state, office) in RCV and year >= RCV[(state, office)] and len(voted) >= 3:
        return (NOT_COMPUTED, f"counted by ranked choice ({'Maine' if state == 'ME' else 'Alaska'} from "
                f"{RCV[(state, office)]}) with three or more candidates (model section 7)")
    if state == "VT" and office == "governor" and len(voted) >= 3:
        return (NOT_COMPUTED, "Vermont's legislature chooses the governor when no candidate has a majority "
                "(Vermont Constitution, ch. II, sec. 47); with three or more candidates that can happen")
    top2 = sorted(voted, key=lambda a: -a["votes"])[:2]
    # an independent who caucuses with the Democrats (Sanders, King) stands as the Democrat, as 538 also has it
    parties = [major(a["parties"]) or ("D" if a.get("state_caucus_D") else None) for a in top2]
    if parties == ["D", "D"] and any(a.get("state_caucus_D") for a in top2):
        return (NOT_COMPUTED, "a Democrat against an independent who caucuses with the Democrats (Connecticut "
                "2006); the model's own forecast is fitted to races of a Democrat against a Republican")
    if parties[0] == parties[1] and parties[0] is not None:
        return (NOT_COMPUTED, "the top two are of one party (a top-two or open special election, or, in "
                "Connecticut in 2006, Lieberman on a Democratic and a third-party line against the Democratic "
                "nominee); the model's own forecast is fitted to races of a Democrat against a Republican")
    if set(parties) != {"D", "R"}:
        return (NOT_COMPUTED, "the top two are not a Democrat and a Republican; the model's own forecast is "
                "fitted to races of a Democrat against a Republican")
    return None


# independents who caucus with the Democrats, by state and last name (Senate.gov party divisions: "the
# Independent and the Independent Democrat caucused with the Democrats")
CAUCUS_D = {("ME", "KING"), ("VT", "SANDERS"), ("CT", "LIEBERMAN")}


def ballot(cands, state):
    """Who was on the ballot, by party, from the source of record: counts of Democratic and Republican
    nominees, and of independents who caucus with the Democrats. Known before the election."""
    real = [a for a in cands if not a["scattered"]]
    return {"D": sum(1 for a in real if major(a["parties"]) == "D"),
            "R": sum(1 for a in real if major(a["parties"]) == "R"),
            "caucus_D": [a["name"] for a in real if major(a["parties"]) is None
                         and (state, last_name(a["name"])) in CAUCUS_D],
            "others": sum(1 for a in real if major(a["parties"]) is None)}


# ----------------------------------------------------------------------------- inputs
def pres_inputs():
    ps = cc.read_json(os.path.join(cc.CACHE, "medsl", "normalized", "president_state.json"))
    db = cc.read_json(os.path.join(cc.CACHE, "downballot", "normalized", "pres_by_cd.json"))
    nara = {r["year"]: r for r in cc.read_json(os.path.join(cc.CACHE, "nara", "normalized",
                                                              "electoral_college.json"))}
    share, nat = {}, {}
    for r in ps["rows"]:
        if r["D"] + r["R"]:
            share[(r["year"], r["state"])] = r["D"] / (r["D"] + r["R"])
    for y in {r["year"] for r in ps["rows"]}:
        D = sum(r["D"] for r in ps["rows"] if r["year"] == y)
        R = sum(r["R"] for r in ps["rows"] if r["year"] == y)
        nat[y] = D / (D + R)
    i = ps["source"]
    medsl_src = cc.source_block("MIT Election Data and Science Lab, U.S. President 1976-2024, Harvard "
                                "Dataverse doi:10.7910/DVN/42MVDX, " + i["version"],
                                i["file"]["url"], i["file"]["read_utc"], i["licence"], mark="stated",
                                via="https://doi.org/10.7910/DVN/42MVDX")
    return share, nat, medsl_src, db, nara


def forecast_inputs(year, office, state, district, inc, inc_via, P, special=False):
    share, nat, medsl_src, db, nara = P
    py = chambers.last_pres_year(year)     # in an odd year, the presidential election before it
    sitting = nara[max(y for y in nara if y < year)]
    SOURCES["medsl_president"] = medsl_src
    SOURCES[f"nara_{sitting['year']}"] = sitting["source"]
    out = {"pres_year": py, "national_share_D": round(nat[py], 6), "national_source": "medsl_president",
           "incumbency": inc, "incumbency_source": ("cha" if "cha" in inc_via else "record" if inc_via else None),
           "midterm": year % 4 != 0 if year % 2 == 0 else None, "president_party": sitting["party"],
           "president_source": f"nara_{sitting['year']}"}
    if year % 2:
        # neither a midterm nor a presidential year (chambers.ODD_TERMS: the route's term of record for odd years)
        out["odd_year"] = True
    if office == "house" and special and (year - 2) in LEAN_INPUT:
        # a House special fills the old Congress's term and is held on the old Congress's lines (2018: Pennsylvania's
        # 7th and 15th, on the lines of 2016 though the new map elected the new Congress the same day), so its lean
        # is the presidential vote on the lines of the House election two years before
        old = LEAN_INPUT[year - 2][0]
        k = f"{state}-{district}"
        x = db["districts"].get(old, {}).get(k, {}).get(str(py))
        if x is None:
            out["lean"] = None
            out["lean_missing"] = f"no {py} presidential vote on the lines of {year - 2} (the old Congress's, on which a special is held) in The Downballot's sheets"
            return out
        sh = db["sheets"][old]
        out["district_share_D"] = round(x["two_party_D"], 6)
        out["lean"] = round(x["two_party_D"] - nat[py], 6)
        out["lines"] = f"the old Congress's: those of {year - 2}, on which a special election is held"
        SOURCES[f"downballot_{old}"] = {k2: sh[k2] for k2 in ("name", "url", "read_utc", "licence", "mark", "via", "note")}
        out["lean_source"] = f"downballot_{old}"
        return out
    if office == "house":
        li = db["lean_inputs"].get(str(year), {})
        k = f"{state}-{district}"
        if k not in li:
            out["lean"] = None
            out["lean_missing"] = (f"no {py} presidential vote on the lines of {year} in The Downballot's sheets "
                                   f"(searched once more 2026-11-07: The Downballot's data guide, its 2024 sheet, "
                                   f"Daily Kos Elections' tables; none reachable)")
            # for control of the chamber only (orchestrator, 2026-11-07 03:46): the same day's presidential
            # vote on these lines, minus that day's national share; inferred, and known only after the vote
            lines = {2024: "2024", 2012: "2012", 2016: "2016"}.get(year)
            x = db["districts"].get(lines, {}).get(k, {}).get(str(year)) if lines else None
            if x and year in nat:
                sh = db["sheets"][lines]
                SOURCES[f"downballot_{lines}"] = {k2: sh[k2] for k2 in ("name", "url", "read_utc", "licence",
                                                                         "mark", "via", "note")}
                out["lean_same_day"] = {"value": round(x["two_party_D"] - nat[year], 6), "pres_year": year,
                                        "district_share_D": round(x["two_party_D"], 6),
                                        "national_share_D": round(nat[year], 6),
                                        "source": f"downballot_{lines}",
                                        "mark": "inferred",
                                        "use": "control of the chamber only; never the seat's own p"}
            return out
        x = li[k]
        sh = db["sheets"][x["sheet"]]
        out["district_share_D"] = round(x["two_party_D"], 6)
        out["lean"] = round(x["two_party_D"] - nat[py], 6)
        SOURCES[f"downballot_{x['sheet']}"] = {k2: sh[k2] for k2 in ("name", "url", "read_utc", "licence", "mark",
                                                                      "via", "note")}
        out["lean_source"] = f"downballot_{x['sheet']}"
    else:
        s = share.get((py, state))
        out["state_share_D"] = round(s, 6) if s is not None else None
        out["lean"] = round(s - nat[py], 6) if s is not None else None
        out["lean_source"] = "medsl_president"
    if office == "governor":
        # the state's last governor race that a Democrat and a Republican led (method D2-v2, the orchestrator,
        # 2026-11-07 05:58, item 5); from Cha, Kuriwaki and Snyder, which begins in 2006
        global GOV_INDEX
        if GOV_INDEX is None:
            GOV_INDEX = chambers.last_governor_index()
        lg = chambers.last_governor_race(GOV_INDEX, state, year)
        if lg:
            out["last_governor_race"] = {"year": lg[0], "share_D": lg[1], "special": lg[2], "source": lg[3]}
            if lg[3] == "algara_amlani":
                SOURCES["algara_amlani"] = AA_SOURCE()
        else:
            out["last_governor_race"] = None
            out["last_governor_race_missing"] = (
                f"no earlier governor race in {state} that a Democrat and a Republican led is in Cha, Kuriwaki and "
                f"Snyder (from 2006) or Algara and Amlani (before 2006)"
                + (f"; {chambers.AA_INCOMPLETE[state]}" if state in chambers.AA_INCOMPLETE else ""))
    return out


# ----------------------------------------------------------------------------- contests
def contest(year, office, c, cha_c, cha_src, P):
    district = c.get("district") if office == "house" else None
    special = c["special"]
    cands = c["candidates"]
    for a in cands:
        a["state_caucus_D"] = (c["state"], last_name(a["name"])) in CAUCUS_D and major(a["parties"]) is None
    kind = structure(year, office, c["state"], cands, special)
    inc, inc_via = incumbency(cands, cha_c, year)
    real = [a for a in cands if not a["scattered"]]
    voted = sorted([a for a in real if a["votes"]], key=lambda a: -a["votes"])
    top2 = voted[:2]
    total = c["printed_total"] if c["printed_total"] is not None else c["computed_total"]
    rec = {
        "id": cc.contest_id(year, office, c["state"], district, special),
        "year": year, "date": ELECTION_DAY[year], "level": office,
        "place": {"state": c["state"], "district": district,
                  "name": cc.STATE_NAMES[c["state"]] + (f" {int(district)}" if district and district != "AL"
                                                         else " at large" if district == "AL" else "")},
        "special": special,
        "result": {"certified": True,
                   "candidates": [{"name": a["name"], "party": a["party"], "votes": a["votes"]} for a in cands],
                   "total_votes": total, "source": c["source"]},
        "two_party": ({"candidates": [a["name"] for a in top2], "votes": [a["votes"] for a in top2],
                       "n_other_voters": sum(a["votes"] for a in top2) - 1,
                       "share_first": round(top2[0]["votes"] / sum(a["votes"] for a in top2), 6)}
                      if len(top2) == 2 else None),
        "forecasts": [],
        "population": None,
        "stage_two": {"of": "Senate control" if office == "senate" else "House control" if office == "house"
                      else None, "inputs": {}, "source": None},
        "p": None,
        "forecast_inputs": None,
        "checks": [],
        "notes": list(c.get("notes") or []),
    }
    if office == "governor":
        rec["stage_two"] = None
    pop = POP.get(year)
    if pop:
        key = f"{c['state']}-{district}" if office == "house" else None
        x = pop["districts"].get(key) if key else pop["states"].get(c["state"])
        if x:
            SOURCES["census_acs"] = pop["source"]
            rec["population"] = {"value": x["value"], "of": "district" if key else "state",
                                 "moe": x.get("moe"), "source": pop["source"]}
    if c.get("printed_total") is not None and c["printed_total"] != c["computed_total"]:
        rec["notes"].append(f"candidates and lines sum to {c['computed_total']:,}; the source prints "
                            f"{c['printed_total']:,}")
    if cha_c and office != "governor":
        SOURCES["cha"] = cha_src
        rec["checks"].append({"against": "cha", "differences": compare(cands, cha_c)})
    if c.get("runoff"):
        rec["notes"].append("runoff: " + ", ".join(f"{a['name']} {a['votes']:,}" for a in c["runoff"]["candidates"])
                            + (f" (total {c['runoff']['total']:,})" if c["runoff"]["total"] else ""))
    rec["ballot"] = ballot(cands, c["state"])
    if kind and kind[0] == "uncontested":
        rec["p"] = {"value": 0.0, "event": 0.0, "under": None, "computed_by": "pipeline/intake/build_congress.py",
                    "commit": COMMIT, "not_computed": None, "reason": kind[1]}
        return rec
    fi = forecast_inputs(year, office, c["state"], district, inc, inc_via, P, special)
    rec["forecast_inputs"] = fi
    if kind:
        rec["p"] = {"value": None, "event": None, "under": None, "computed_by": None, "commit": None,
                    "not_computed": kind[1], "reason": None}
        return rec
    if fi.get("lean") is None:
        rec["p"] = {"value": None, "event": None, "under": None, "computed_by": None, "commit": None,
                    "not_computed": fi.get("lean_missing") or "no presidential vote for the state", "reason": None}
        return rec
    rec["p"] = {"value": None, "event": None, "under": None, "computed_by": None, "commit": None,
                "not_computed": "pending: p is computed by pipeline/chambers.py compute", "reason": None}
    return rec


def governors(year, cha_src, idx, P):
    out = []
    for (y, office, st, dist, special), cs in sorted(idx.items(), key=lambda kv: (kv[0][2], kv[0][4])):
        if y != year or office != "governor" or st not in cc.STATES_50:
            continue
        c = [x for x in cs if not x["runoff"]] or cs
        c = c[0]
        cands = [{"name": a["name"], "party": a["party_formal"] or a["party"], "parties": [a["party"]],
                  "votes": a["votes"], "scattered": False} for a in c["candidates"]]
        rec = {"office": "governor", "state": st, "district": None, "special": special, "candidates": cands,
               "printed_total": None, "computed_total": sum(a["votes"] or 0 for a in cands), "runoff": None,
               "source": cha_source(cha_src, "governor"),
               "notes": ["governors' totals here leave out candidates under ten votes, blank, over- and "
                         "under-votes (the dataset's guide)"]}
        r = contest(year, "governor", rec, {"candidates": c["candidates"]}, cha_src, P)
        r["notes"] += [f"source check: {x}" for x in c["checks"]]
        out.append(r)
    return out


_AA = {}


def AA_SOURCE():
    if "source" not in _AA:
        d = cc.read_json(os.path.join(cc.CACHE, "algara_amlani", "normalized", "governors.json"))
        _AA["source"], _AA["elections"] = d["source"], d["elections"]
    return _AA["source"]


def aa_structure(r):
    """None if the race is a two-way race of a Democrat against a Republican the model covers; else (kind, reason).
    The source gives the other candidates only as a total (r["others"])."""
    D, R, o = r["D"], r["R"], r["others"]
    if r["state"] in chambers.AA_INCOMPLETE:
        return (NOT_COMPUTED, chambers.AA_INCOMPLETE[r["state"]])
    if o is None:
        return (NOT_COMPUTED, "the source's county totals sum to less than the two nominees' votes")
    if (D == 0) != (R == 0) and o == 0:
        return ("uncontested", "only one candidate received votes")
    why = governor_structure(r["year"], r["state"], (D > 0) + (R > 0) + (o > 0), False)
    if why:
        return (NOT_COMPUTED, why)
    if D == 0 or R == 0:
        return (NOT_COMPUTED, "no Democrat or no Republican received votes; the source names no other candidate, so "
                "who the top two were is not known")
    if o >= min(D, R):
        return (NOT_COMPUTED, f"a candidate other than the two nominees may be among the top two: the source gives the "
                f"others' vote only as a total ({o:,}), which is at least the second nominee's")
    if r["state"] == "GA" and o > 0:
        return (NOT_COMPUTED, "Georgia requires a majority; with a third candidate a runoff can follow (model section 7: "
                "runoffs are not yet computed)")
    if r["state"] == "VT" and o > 0:
        return (NOT_COMPUTED, "Vermont's legislature chooses the governor when no candidate has a majority (Vermont "
                "Constitution, ch. II, sec. 47); with a third candidate that can happen")
    return None


def aa_governors(year, P):
    """The governor contests of an even year before 2006, from Algara and Amlani's county returns summed to the
    state (pipeline/intake/algara_amlani.py): the record, with no second source read for these years."""
    AA_SOURCE()
    out = []
    for r in _AA["elections"]:
        if r["year"] != year or r["state"] not in cc.STATES_50:
            continue
        SOURCES["algara_amlani"] = _AA["source"]
        cands = [{"name": r["dem_nominee"], "party": "D", "votes": r["D"]},
                 {"name": r["rep_nominee"], "party": "R", "votes": r["R"]}]
        cands = [a for a in cands if a["name"] is not None or a["votes"]]
        if r["others"]:
            cands.append({"name": "others (not named in the source)", "party": None, "votes": r["others"]})
        top2 = sorted([a for a in cands if a["party"] and a["votes"]], key=lambda a: -a["votes"])[:2]
        notes = [f"the votes are Algara and Amlani's county returns summed over {r['counties']} counties; not the "
                 f"state's certified total, and other candidates appear only as the total less the two nominees",
                 f"date: the general election day (the Tuesday after the first Monday in November), inferred; the "
                 f"source gives the year"]
        if r["counties_missing"]:
            notes.append(f"{r['counties_missing']} of the {r['counties']} counties have no count in the source "
                         f"(left out of the sums)")
        if r.get("note"):
            notes.append(r["note"])
        rec = {
            "id": cc.contest_id(year, "governor", r["state"]),
            "year": year, "date": ELECTION_DAY[year], "level": "governor",
            "place": {"state": r["state"], "district": None, "name": cc.STATE_NAMES[r["state"]]},
            "special": False,
            "result": {"certified": None, "candidates": cands, "total_votes": r["total"],
                       "votes_incomplete": bool(r["counties_missing"]) or r["state"] in chambers.AA_INCOMPLETE,
                       "source": _AA["source"]},
            "two_party": ({"candidates": [a["name"] for a in top2], "votes": [a["votes"] for a in top2],
                           "n_other_voters": sum(a["votes"] for a in top2) - 1,
                           "share_first": round(top2[0]["votes"] / sum(a["votes"] for a in top2), 6)}
                          if len(top2) == 2 else None),
            "forecasts": [], "population": None, "stage_two": None, "p": None, "forecast_inputs": None,
            "checks": [{"against": None, "differences": ["no second source read for this contest (Cha, Kuriwaki "
                                                         "and Snyder begin in 2006)"]}],
            "notes": notes,
            "ballot": {"D": int(bool(r["dem_nominee"])), "R": int(bool(r["rep_nominee"])), "caucus_D": [],
                       "others": None},
        }
        kind = aa_structure(r)
        if kind and kind[0] == "uncontested":
            rec["p"] = {"value": 0.0, "event": 0.0, "under": None, "computed_by": "pipeline/intake/build_congress.py",
                        "commit": COMMIT, "not_computed": None, "reason": kind[1]}
            out.append(rec)
            continue
        fi = forecast_inputs(year, "governor", r["state"], None, r["incumbency"], {"algara_amlani"}, P)
        fi["incumbency_source"] = "algara_amlani"
        fi["seat_status"] = r["seat_status"]
        rec["forecast_inputs"] = fi
        if kind:
            rec["p"] = {"value": None, "event": None, "under": None, "computed_by": None, "commit": None,
                        "not_computed": kind[1], "reason": None}
        elif fi.get("lean") is None:
            rec["p"] = {"value": None, "event": None, "under": None, "computed_by": None, "commit": None,
                        "not_computed": fi.get("lean_missing") or "no presidential vote for the state", "reason": None}
        else:
            rec["p"] = {"value": None, "event": None, "under": None, "computed_by": None, "commit": None,
                        "not_computed": "pending: p is computed by pipeline/chambers.py compute", "reason": None}
        out.append(rec)
    return out


def aa_not_in_cha(year, cha_rows, P):
    """The governor contests of an even year from 2006 that Cha, Kuriwaki and Snyder do not hold, from Algara and
    Amlani's county sums, the record for them as for New Jersey 2017 (build_odd_governors): Rhode Island 2010 (the
    orchestrator, 2026-11-07 12:35: "Yes to RI 2010")."""
    have = {r["place"]["state"] for r in cha_rows}
    out = []
    for r in aa_governors(year, P):
        if r["place"]["state"] in have:
            continue
        r["notes"].append("Cha, Kuriwaki and Snyder do not hold this contest, so Algara and Amlani's county sums "
                          "stand as the record")
        r["checks"] = [{"against": None, "differences": ["no second source read for this contest (Cha, Kuriwaki and "
                                                         "Snyder do not hold it)"]}]
        out.append(r)
    return out


POP = {}
# a special election the November record leaves out, held on a date one of the chambers' own pages gives
OFF_DATE = {(2010, "senate", "MA"): ("2010-01-19", "U.S. Senate, Party Division, 111th Congress, note 4: \"Scott Brown (R) "
                                     "of Massachusetts, elected January 19, 2010, was seated, replacing appointed "
                                     "Senator Paul Kirk (D).\"")}
NOT_NOVEMBER = ("a special election the November record (the FEC's Federal Elections; for 2024 the Clerk's "
                "Statistics) leaves out, mostly because it was held on another date; the model's own forecast is "
                "for November's general election, and no published forecast for it was read here")


def cha_only(year, office, st, d, special, cs, cha_src, P):
    """A contest only Cha, Kuriwaki and Snyder hold (special elections on other dates): their record stands as
    the source of record, with no second source to check it against, and p is not computed."""
    c = [x for x in cs if not x["runoff"]] or cs
    runoff_only = not [x for x in cs if not x["runoff"]]
    c = c[0]
    cands = [{"name": a["name"], "party": a["party_formal"] or a["party"], "parties": [a["party"]],
              "votes": a["votes"], "scattered": False} for a in c["candidates"]]
    rec = {"office": office, "state": st, "district": d, "special": special, "candidates": cands,
           "printed_total": None, "computed_total": sum(a["votes"] or 0 for a in cands), "runoff": None,
           "source": cha_source(cha_src, office),
           "notes": ["in the check source only: " + NOT_NOVEMBER]
                    + (["the source holds only the runoff, the deciding round"] if runoff_only else [])}
    r = contest(year, office, rec, None, cha_src, P)
    r["result"]["certified"] = None
    r["notes"].append("certified: the source compiles official returns and does not say, contest by contest, "
                      "whether a count is the certified one")
    when = OFF_DATE.get((year, office, st))
    r["date"] = when[0] if when else None
    if when:
        r["notes"].append(f"date: {when[1]}")
    else:
        r["notes"].append("date: not given by the sources read here")
    r["checks"] = [{"against": None, "differences": ["no second source read for this contest"]}]
    if r["p"]["value"] is None:
        why = r["p"]["not_computed"] or ""
        r["p"]["not_computed"] = NOT_NOVEMBER if why.startswith("pending") or not why else f"{why}; and {NOT_NOVEMBER}"
    return r


def build_early_governors(year):
    """An even year before 2006: governors only, from Algara and Amlani."""
    P = pres_inputs()
    SOURCES.clear()
    contests = sorted(aa_governors(year, P), key=lambda r: r["id"])
    srcs = {"algara_amlani": AA_SOURCE()}
    srcs.update({k: v for k, v in SOURCES.items()})
    out = {"level": "governor", "year": year,
           "about": f"Governor contests of {year}, in the layout of plan/PLAN.md section 3 with the fields "
                    f"data/README.md adds. Built by pipeline/intake/build_congress.py from Algara and Amlani's county "
                    f"returns (pipeline/intake/algara_amlani.py) and the caches named in each source block. Alaska is "
                    f"not in the source.",
           "missing_from_record": [], "sources": srcs, "contests": contests}
    cc.write_contest_file(os.path.join(cc.DATA, "governor", f"{year}.json"), out)
    n_p0 = sum(1 for r in contests if r["p"]["value"] == 0.0)
    n_pend = sum(1 for r in contests if (r["p"]["not_computed"] or "").startswith("pending"))
    print(f"{year} governor: {len(contests)} contests; uncontested {n_p0}; awaiting the forecast {n_pend}; not computed "
          f"{len(contests) - n_p0 - n_pend}")


# ----------------------------------------------------------------------------- the odd-year governors
LA_SOS_LICENCE = "no licence printed; the Louisiana Secretary of State's official election returns, public records"
DATE_NOTE = ("date: the general election day (the Tuesday after the first Monday in November), inferred; the source "
             "gives the year")


def ms_rule_source():
    """The source block of Mississippi's rule before 2020 (pipeline/intake/ms_governor_rule.py's file)."""
    m = cc.read_json(os.path.join(cc.CACHE, "law", "MS", "hc47-2020-html.raw.meta.json"))
    if m is None:
        raise SystemExit("run pipeline/intake/ms_governor_rule.py first")
    return cc.source_block("Mississippi Legislature, 2020 Regular Session, House Concurrent Resolution 47 (as adopted "
                           "by the House and Senate): sections 140 to 143 of the Constitution of 1890 as they read, "
                           "the words it strikes from section 140 marked", m["url"], m["read_utc"],
                           "a public record of the Mississippi Legislature; no licence printed", mark="stated",
                           note=f"sha256 {m['sha256'][:16]}; read by pipeline/intake/ms_governor_rule.py through D4's "
                                f"state_law.py, the host's certificate chain completed from its own CA Issuers address "
                                f"with verification on (the orchestrator, 2026-11-07 08:00); the text as it read when "
                                f"the amendment was proposed in 2020, no earlier text read")


def la_sos_governors(year, P):
    """Louisiana's governor contest of `year` from the Secretary of State (pipeline/intake/la_sos_governor.py), gated
    within the certifying source as D3 gates that year's other contests."""
    d = cc.read_json(os.path.join(cc.CACHE, "la_sos", "normalized", f"governor-{year}.json"))
    if d is None:
        raise SystemExit(f"run pipeline/intake/la_sos_governor.py {year} first")
    out = []
    for c in d["contests"]:
        wb = c["workbook"]
        src = cc.source_block(d["source"]["name"], wb["url"], wb["read_utc"], LA_SOS_LICENCE, mark="stated",
                              via=d["source"]["url"],
                              note=f"the workbook of {c['date']} (sha256 {wb['sha256'][:16]}), its sheet "
                                   f"'Multi-Parish(Parish)', read by D3's pipeline/intake/la_sos.py; the date marked "
                                   f"official on the site's list of elections ({d['dates_list']['url']}, read "
                                   f"{d['dates_list']['read_utc']})")
        SOURCES["la_sos"] = src
        cands = [{"name": x["name"], "party": x["party"], "parties": [x["party"]], "votes": x["votes"],
                  "scattered": False} for x in c["candidates"]]
        rec = {"office": "governor", "state": "LA", "district": None, "special": False, "candidates": cands,
               "printed_total": None, "computed_total": c["total_votes"], "runoff": None, "source": src,
               "notes": [f"the Secretary of State's count over the {c['parishes']} parishes, the parties as the source "
                         f"prints them (REP, DEM, IND, NOPTY: no party)"]}
        r = contest(year, "governor", rec, None, None, P)
        r["date"] = c["date"]
        r["result"]["certified"] = True
        r["notes"].append(f"date: {c['date']}, stated (the source's date of the workbook); a candidate had a majority, "
                          f"so no later round was held for this contest (the site's posted results of the year's later "
                          f"dates hold no contest titled Governor)")
        g = c["gate"]
        r["gate"] = {k: g[k] for k in ("by", "ruled", "official", "parts_add_up", "posted_results")}
        r["checks"] = [{"against": "the Secretary of State's posted results of its date (" +
                                   g["posted_files"]["Votes"]["url"] + f", read {g['posted_files']['Votes']['read_utc']}, "
                                   f"sha256 {g['posted_files']['Votes']['sha256'][:16]}; the same file D3's "
                                   f"data/local/check-la.json compared)",
                        "differences": [] if g["posted_results"].startswith("equal") else [c["held"]]}]
        if c["held"]:
            r["p"] = {"value": None, "event": None, "under": None, "computed_by": None, "commit": None,
                      "not_computed": "held by the gate within the certifying source: " + c["held"], "reason": None}
        out.append(r)
    return out


STATE_GOV_SRC = {"NJ": "nj_doe", "VA": "va_elect"}


def state_gov_governors(year, P):
    """The governor contests of `year` from the states' own certified results (pipeline/intake/state_governors.py:
    New Jersey and Virginia 2025), gated within the certifying source as Louisiana's 2023 is; and the refusals of the
    year's other states (Kentucky and Mississippi 2023)."""
    d = cc.read_json(os.path.join(cc.CACHE, "state_gov", "normalized", f"governor-{year}.json"))
    if d is None:
        return [], {}
    out = []
    for c in d["contests"]:
        s = c["source"]
        src = cc.source_block(s["name"], s["url"], s["read_utc"], s["licence"], mark="stated", via=s["via"],
                              note=f"sha256 {s['sha256'][:16]}; read by pipeline/intake/state_governors.py; "
                                   + c["gate"]["official_how"])
        SOURCES[STATE_GOV_SRC[c["state"]]] = src
        cands = [{"name": x["name"], "party": x["party"], "parties": [x["party"] or ("Write-In" if x["write_in"] else "")],
                  "votes": x["votes"], "scattered": bool(x["write_in"])} for x in c["candidates"]]
        rec = {"office": "governor", "state": c["state"], "district": None, "special": False, "candidates": cands,
               "printed_total": None, "computed_total": c["total_votes"], "runoff": None, "source": src,
               "notes": [f"the state's own count over its {c['parts']['n']} {c['parts']['kind']}, the parties as the "
                         f"source prints them"] + c["notes"]}
        r = contest(year, "governor", rec, None, None, P)
        r["date"] = c["date"]
        r["result"]["certified"] = True
        r["notes"].append(f"date: {c['date']}, stated (the source's date of the election)")
        g = c["gate"]
        r["gate"] = {k: g[k] for k in ("by", "ruled", "official", "official_how", "parts_add_up", "parts_how",
                                       "statewide_equal")}
        r["checks"] = [{"against": ch["against"], "differences": ch["differences"]} for ch in c["checks"]]
        fi = r.get("forecast_inputs")
        if fi is not None:
            inc, how = chambers.state_gov_incumbency(c, year)
            fi["incumbency"] = inc
            fi["incumbency_source"] = "inferred"
            fi["incumbency_how"] = how
            SOURCES["cha"] = cha_source(cha_index()[0], "governor")
        if c["held"]:
            r["p"] = {"value": None, "event": None, "under": None, "computed_by": None, "commit": None,
                      "not_computed": "held by the gate within the certifying source: " + c["held"], "reason": None}
        out.append(r)
    refused = {x["state"]: x for x in d.get("refused", [])}
    return out, refused


def _off_round(r, why):
    """A contest whose date the sources do not give (Louisiana's rounds before 2023; a special or later round)."""
    r["date"] = None
    r["notes"] = [n for n in r["notes"] if not n.startswith("date:")] + [f"date: not given by the sources read here; {why}"]


def build_odd_governors(year):
    """An odd year: the governors of Kentucky, Louisiana, Mississippi, New Jersey and Virginia, and any other governor
    contest the sources hold for the year (the orchestrator, 2026-11-07 12:01). The record is Cha, Kuriwaki and Snyder
    where they hold the contest (2007-2021), as for the even years; Algara and Amlani's county sums before (1977-2005),
    and where Cha does not hold it or holds only its winner; Louisiana's 2023 from the Secretary of State."""
    P = pres_inputs()
    SOURCES.clear()
    cha_src, idx = cha_index()
    AA_SOURCE()
    aa = {r["state"]: r for r in _AA["elections"] if r["year"] == year}
    by_state = {}
    for r in governors(year, cha_src, idx, P):
        st = r["place"]["state"]
        voted = [a for a in r["result"]["candidates"] if a["votes"]]
        a = aa.get(st)
        if len(voted) <= 1 and a and sum(1 for v in (a["D"], a["R"], a["others"]) if v) > 1:
            # Louisiana 2007: Cha holds only the winner of the open primary
            continue
        SOURCES["cha"] = cha_source(cha_src, "governor")
        r["notes"].append(DATE_NOTE)
        by_state[st] = r
    for r in aa_governors(year, P):
        st = r["place"]["state"]
        if st in by_state:
            continue
        if year >= 2006:
            held = [x for k, cs in idx.items() if k[0] == year and k[1] == "governor" and k[2] == st for x in cs]
            r["notes"].append("Cha, Kuriwaki and Snyder hold only this contest's winner (" + ", ".join(
                f"{a['name']} {a['votes']:,}" for x in held for a in x["candidates"]) + "), so Algara and Amlani's "
                "county sums, which hold the other candidates, stand as the record" if held else
                "Cha, Kuriwaki and Snyder do not hold this contest, so Algara and Amlani's county sums stand as the "
                "record")
        by_state[st] = r
    la = os.path.join(cc.CACHE, "la_sos", "normalized", f"governor-{year}.json")
    if os.path.exists(la):
        for r in la_sos_governors(year, P):
            by_state["LA"] = r
    sg, refused = state_gov_governors(year, P)
    for r in sg:
        by_state[r["place"]["state"]] = r
    for st, r in by_state.items():
        if r["date"] is None or st == "LA" and r["result"]["source"].get("name", "").startswith("Louisiana"):
            continue
        if st == "LA":
            _off_round(r, "Louisiana's rounds are held on Saturdays of October and November, not on the general "
                          "election day")
        elif st not in ODD_STATES or r["special"]:
            _off_round(r, "an odd-year election in a state that elects its governor in even years")
    contests = sorted(by_state.values(), key=lambda r: r["id"])
    srcs = dict(SOURCES)
    if any(r["place"]["state"] == "MS" for r in contests):
        srcs["ms_hc47_2020"] = ms_rule_source()
    missing = [f"{st}: not in the sources read here (Cha, Kuriwaki and Snyder end in 2021, Algara and Amlani in 2019"
               + ("; Louisiana's own file is read for 2023 only" if st == "LA" else "") + ")"
               + (f"; the state's own results were refused: {refused[st]['who']}, {refused[st]['url']}, "
                  f"{refused[st]['when_utc']}: {refused[st]['answer']}; {refused[st]['tried']} (the orchestrator, "
                  f"2026-11-07 12:40: \"record them and try nothing else\")" if st in refused else "")
               for st in ODD_STATES if st not in by_state and (year % 4 == 3) == (st in ("KY", "LA", "MS"))]
    out = {"level": "governor", "year": year,
           "about": f"Governor contests of {year}, an odd year, in the layout of plan/PLAN.md section 3 with the fields "
                    f"data/README.md adds. Built by pipeline/intake/build_congress.py from Cha, Kuriwaki and Snyder "
                    f"(2007-2021), Algara and Amlani's county returns (before, and where Cha lacks a contest), "
                    f"Louisiana's Secretary of State (2023) and New Jersey's and Virginia's certified results (2025), "
                    f"as each contest's source block says. The forecast is the "
                    f"governors' route fitted on the even years before it (data/congress/REPORT.md section 8).",
           "missing_from_record": [], "not_in_sources": missing, "sources": srcs, "contests": contests}
    cc.write_contest_file(os.path.join(cc.DATA, "governor", f"{year}.json"), out)
    n_p0 = sum(1 for r in contests if r["p"]["value"] == 0.0)
    n_pend = sum(1 for r in contests if (r["p"]["not_computed"] or "").startswith("pending"))
    print(f"{year} governor: {len(contests)} contests ({', '.join(r['place']['state'] for r in contests)}); uncontested "
          f"{n_p0}; awaiting the forecast {n_pend}; not computed {len(contests) - n_p0 - n_pend}"
          + (f"; not in the sources: {missing}" if missing else ""))


def build(year):
    if year % 2:
        return build_odd_governors(year)
    if year < 2006:
        return build_early_governors(year)
    pop = cc.read_json(os.path.join(cc.CACHE, "census", "normalized", f"population_{year}.json"))
    if pop:
        POP[year] = pop
    cha_src, idx = cha_index()
    P = pres_inputs()
    rec = record_contests(year)
    by_level = {"senate": [], "house": [], "governor": []}
    seen = set()
    for c in rec:
        cha_cs = match_cha(idx, year, c["office"], c["state"], c.get("district"), c["special"])
        r = contest(year, c["office"], c, cha_cs[0] if cha_cs else None, cha_source(cha_src, c["office"]), P)
        if not cha_cs:
            SOURCES["cha"] = cha_source(cha_src, c["office"])
            r["checks"].append({"against": "cha", "differences": ["contest not found in the check source"]})
        by_level[c["office"]].append(r)
        seen.add((c["office"], c["state"], c.get("district") if c["office"] == "house" else None, c["special"]))
    by_level["governor"] = governors(year, cha_src, idx, P)
    by_level["governor"] += aa_not_in_cha(year, by_level["governor"], P)
    SOURCE_POOL.update(SOURCES)
    for (y, office, st, dist, special), cs in sorted(idx.items()):
        if y == year and office in ("house", "senate") and st in cc.STATES_50:
            d = None if office == "senate" else ("AL" if (office, st, "AL", special) in seen and dist == "01" else dist)
            if (office, st, d, special) not in seen:
                by_level[office + "_missing"] = by_level.get(office + "_missing", []) + [f"{st}-{dist}{' special' if special else ''}"]
                if office == "senate" and any(k[0] == "senate" and k[1] == st for k in seen):
                    continue   # Arizona 2020: the same contest, a special in one source and not in the other
                by_level[office].append(cha_only(year, office, st, d, special, cs, cha_src, P))
    SOURCE_POOL.update(SOURCES)
    for level in ("senate", "house", "governor"):
        SOURCES.clear()
        SOURCES["cha"] = cha_source(cha_src, level)
        for r in by_level[level]:
            fi = r.get("forecast_inputs") or {}
            for k in ("national_source", "president_source", "lean_source"):
                if fi.get(k) and fi[k] not in SOURCES:
                    SOURCES[fi[k]] = SOURCE_POOL[fi[k]]
            if (fi.get("lean_same_day") or {}).get("source"):
                SOURCES[fi["lean_same_day"]["source"]] = SOURCE_POOL[fi["lean_same_day"]["source"]]
            # the last governor race's own source (Algara and Amlani before 2006): its block was left out of the
            # file's sources though the field names it (D2, 2026-11-07, found while adding Rhode Island 2010)
            lg = fi.get("last_governor_race") or {}
            if lg.get("source") == "algara_amlani":
                SOURCES["algara_amlani"] = AA_SOURCE()
            if r["result"]["source"] is _AA.get("source"):
                SOURCES["algara_amlani"] = AA_SOURCE()
        contests = sorted(by_level[level], key=lambda r: r["id"])
        out = {"level": level, "year": year,
               "about": f"{level.capitalize()} contests of {year}, in the layout of plan/PLAN.md section 3 with "
                        f"the fields data/README.md adds. Built by pipeline/intake/build_congress.py from the "
                        f"caches of the intake scripts named in each source block.",
               "missing_from_record": by_level.get(level + "_missing", []),
               "sources": dict(SOURCES),
               "contests": contests}
        path = os.path.join(cc.DATA, level, f"{year}.json")
        cc.write_contest_file(path, out)
        n_p0 = sum(1 for r in contests if r["p"] and r["p"]["value"] == 0.0)
        n_nc = sum(1 for r in contests if r["p"] and r["p"]["value"] is None and not
                   r["p"]["not_computed"].startswith("pending"))
        n_pend = sum(1 for r in contests if r["p"] and (r["p"]["not_computed"] or "").startswith("pending"))
        n_diff = sum(1 for r in contests for ch in r["checks"] if ch["differences"])
        print(f"{year} {level}: {len(contests)} contests; uncontested {n_p0}; not computed {n_nc}; awaiting the "
              f"forecast {n_pend}; with a difference from the check source {n_diff}; in the check source only "
              f"{len(by_level.get(level + '_missing', []))}")


if __name__ == "__main__":
    for y in [int(a) for a in sys.argv[1:]] or [2024, 2022]:
        build(y)
