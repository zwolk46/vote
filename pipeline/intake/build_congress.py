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
import congress_common as cc  # noqa: E402
from downballot_pres_by_cd import LEAN_INPUT  # noqa: E402

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
    """Differences between the source of record's candidates and Cha's, matched by last name."""
    diffs = []
    if cha_c.get("runoff"):
        return ["the check source holds only the runoff, the deciding round (its guide); the November round "
                "is not checked"]
    pool = {last_name(a["name"]): a for a in cha_c["candidates"]}
    by_votes = {a["votes"]: a for a in cha_c["candidates"] if a["votes"]}
    for a in rec_cands:
        if a["scattered"] or a["votes"] is None:
            continue
        b = pool.get(last_name(a["name"])) or by_votes.get(a["votes"])
        if b is None:
            if (a["votes"] or 0) >= 10:      # Cha leaves out candidates under ten votes
                diffs.append(f"{a['name']} ({a['votes']:,}) is not in the check source")
            continue
        if b["votes"] is not None and b["votes"] != a["votes"]:
            diffs.append(f"{a['name']}: {a['votes']:,} here, {b['votes']:,} in the check source "
                         f"({b['votes'] - a['votes']:+,})")
    return diffs


def incumbency(rec_cands, cha_c, year):
    """inc = +1 (a Democratic incumbent runs), -1 (a Republican one), 0; from Cha by last name, else the
    FEC's own mark (2006-2022 results workbooks mark the seat's incumbent)."""
    pool = {last_name(a["name"]): a for a in (cha_c["candidates"] if cha_c else [])}
    by_votes = {a["votes"]: a for a in (cha_c["candidates"] if cha_c else []) if a["votes"]}
    inc = {"D": 0, "R": 0}
    via = set()
    for a in rec_cands:
        m = major(a["parties"])
        if m is None and a.get("state_caucus_D"):
            m = "D"
        if m is None:
            continue
        b = pool.get(last_name(a["name"])) or by_votes.get(a["votes"])
        if b is not None and b["inc"] is not None:
            via.add("cha")
            if b["inc"] == 1:
                inc[m] = 1
        elif a.get("incumbent_fec"):
            via.add("fec")
            inc[m] = 1
    return inc["D"] - inc["R"], sorted(via)


# ----------------------------------------------------------------------------- structure
def structure(year, office, state, cands, special):
    """None if the race is a two-way race the model's own forecast covers; else (kind, reason)."""
    real = [a for a in cands if not a["scattered"]]
    voted = [a for a in real if a["votes"]]
    if len(real) == 1 or len(voted) <= 1:
        return ("uncontested", "only one candidate was on the ballot") if len(real) == 1 else \
            ("uncontested", "only one candidate received votes")
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
    parties = [major(a["parties"]) for a in top2]
    if parties[0] == parties[1] and parties[0] is not None:
        return (NOT_COMPUTED, "the top two are of one party (a top-two or open special election); the "
                "model's own forecast is fitted to races of a Democrat against a Republican")
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
    py = year - 4 if year % 4 == 0 else year - 2
    sitting = nara[max(y for y in nara if y < year)]
    SOURCES["medsl_president"] = medsl_src
    SOURCES[f"nara_{sitting['year']}"] = sitting["source"]
    out = {"pres_year": py, "national_share_D": round(nat[py], 6), "national_source": "medsl_president",
           "incumbency": inc, "incumbency_source": ("cha" if "cha" in inc_via else "record" if inc_via else None),
           "midterm": year % 4 != 0, "president_party": sitting["party"],
           "president_source": f"nara_{sitting['year']}"}
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
    return out


# ----------------------------------------------------------------------------- contests
def contest(year, office, c, cha_c, cha_src, P):
    district = c.get("district") if office == "house" else None
    special = c["special"]
    cands = c["candidates"]
    kind = structure(year, office, c["state"], cands, special)
    for a in cands:
        a["state_caucus_D"] = (c["state"], last_name(a["name"])) in CAUCUS_D and major(a["parties"]) is None
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
                    "commit": None, "not_computed": None, "reason": kind[1]}
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
                "not_computed": "pending: the model's own forecast method awaits the orchestrator's approval "
                                "(briefs/D2-data-congress.md step 2)", "reason": None}
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


def build(year):
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
    SOURCE_POOL.update(SOURCES)
    for (y, office, st, dist, special), cs in sorted(idx.items()):
        if y == year and office in ("house", "senate") and st in cc.STATES_50:
            d = None if office == "senate" else ("AL" if (office, st, "AL", special) in seen and dist == "01" else dist)
            if (office, st, d, special) not in seen:
                by_level[office + "_missing"] = by_level.get(office + "_missing", []) + [f"{st}-{dist}{' special' if special else ''}"]
                if office == "senate" and any(k[0] == "senate" and k[1] == st for k in seen):
                    continue   # Arizona 2020: the same contest, a special in one source and not in the other
                by_level[office].append(cha_only(year, office, st, d, special, cs, cha_src, P))
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
