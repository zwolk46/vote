"""pipeline/local_nj_leg.py: New Jersey's legislatures of 2023 and 2025, from the Division of Elections' Official Lists
(pipeline/intake/nj_sos.py), gated within the certifying source, in the layout pipeline/local_medsl.py writes.

Written 2026-11-07 by worker D3 (briefs/D3-data-local.md, step 2) at the orchestrator's orders of 10:17 ("odd-year
legislatures after 2022 (MS, NJ, VA 2023; NJ, VA 2025)") and 16:47 ("NJ 2023 and 2025 legislatures from the Official
Lists ... each gets a proposed gate"). Why: Klarner's record ends with 2022, and MEDSL holds no odd year, so the state's
own lists are the only source of New Jersey's 2023 and 2025 legislatures read.

What the lists hold [stated: the files; measured: what pipeline/intake/nj_sos.py reads from them]:
  2023  "Official List: Candidates for State Senate For GENERAL ELECTION 11/07/2023 Election" (40 districts) and the
        same for General Assembly (40), dated 12/06/2023 on their pages.
  2025  "Candidates for General Assembly For GENERAL ELECTION 11/04/2025 Election" (40 districts), "Candidates for
        State Senate" in the Thirty-Fifth Legislative District only, and Governor (D2's level, data/governor/2025.json),
        dated 12/03/2025.
  Each district's heading names its counties ("First Legislative District: ATLANTIC (part) - CAPE MAY - CUMBERLAND
  (part) Counties"); each candidate has a line per county and a "Total"; "* denotes incumbent", the heading says; and
  "(w)" follows the names of those elected [inferred: in every contest of both years it marks exactly the leading
  candidates for the seats, 1 in the Senate and 2 in the Assembly].

Seats. Each Senate district elects one member and each Assembly district two at once [measured: Klarner's New Jersey
Assembly contests of 2017, 2019 and 2021 have 2 seats each and his Senate contests 1; the lists mark 2 winners in each
Assembly district and 1 in each Senate district in both years].

Specials. The Senate's 2025 list holds one district, while 2023's holds all 40, so the Thirty-Fifth's contest of 2025 is
taken as an election to fill a vacancy [inferred: the lists; no law read], recorded with p not computed (a special
election: the model's own forecasts are fitted to regular elections).

Routes (pipeline/local.py's, as for MEDSL's 2024 legislatures in pipeline/local_medsl.py):
  - A contest with one name for each seat: p 0.
  - The Senate of 2023, one Democrat against one Republican: route (a), class C, since no last result on the same lines
    is read (the lists hold no precincts to compare lines by; MEDSL's 2024 legislatures take class C wherever the lines
    are not shown to be the same). Incumbency is the list's own mark ("* denotes incumbent") [stated], +1 for a
    Democrat, -1 for a Republican. The chamber's lean is Klarner's last New Jersey Senate before (2021): the mean
    Democratic share of its contested single-seat races, minus 1/2. Fitted on Klarner's races of earlier years only.
  - Other Senate contests: route (b), like past races of their class.
  - The Assembly: route (c), "general, 2 seats at once", by slate, like past races at the boundary between the second
    and third.
  Like races are every earlier contest in the sources taken in (the orchestrator, 2026-11-07 11:56: "earlier cycles
  only means every earlier contest"): for 2023, Klarner's of 1967-2022; for 2025, those, Louisiana's 2023 (deciding
  rounds), New Jersey's 2023 and MEDSL's 2024 legislatures. And 2023 feeds the later years in turn: its Senate's
  Democrat-against-Republican races join route (a)'s fit for 2024 and after (partisan_rows), its other contests the
  like races of 2024 and after (class_rows).

The gate within the certifying source (2023 has no federal or statewide contest on its ballot; 2025's only statewide
contest is the Governor's, which D2 read from the same list) [proposed, for the orchestrator's ruling]:
  (a) each list is linked from the Division's page of its year as "Official General Election Results: ..." and its
      pages are headed "Official List";
  (b) each candidate's county lines add up to its "Total", each contest's own "Total" equals its candidates' totals,
      and the list's last page counts as many candidates as are read;
  (c) each candidate's county lines are in the counties its district's heading names;
  (d) 2025: the Governor's list read here equals D2's data/governor/2025.json, candidate by candidate, and is the same
      file (sha256).
  A contest that fails (b) or (c) is held; a list that fails (a), or a year that fails (d), holds all its contests.
  Recorded beside it, not a gate: each district's named counties are the same in the Senate's and the Assembly's lists
  of 2023 and in the Assembly's of 2025.

  check()  the gates: data/local/check-nj-legislature.json.

Run:  VOTE_CACHE=/tmp/vote-cache python3 -I pipeline/local_nj_leg.py check
"""
import argparse
import collections
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fetch as F  # noqa: E402
from intake import nj_sos as SOS  # noqa: E402
import local as L  # noqa: E402

YEARS = (2023, 2025)
SOURCE_KEY = "nj_sos"
LEVEL = {"State Senate": "state-upper", "General Assembly": "state-lower"}
SEATS = {"State Senate": 1, "General Assembly": 2}   # docstring: Seats
LISTS = {2023: ("state-senate", "general-assembly"), 2025: ("general-assembly", "state-senate-35ld", "governor")}
DATE = {2023: "2023-11-07", 2025: "2025-11-04"}   # the lists' "For GENERAL ELECTION 11/07/2023 Election" [stated]
OFFICES_OF_LIST = {"state-senate": ("State Senate",), "general-assembly": ("General Assembly",),
                   "state-senate-35ld": ("State Senate",), "governor": ("Governor",)}
REGULAR = {2023: {"State Senate", "General Assembly"}, 2025: {"General Assembly"}}   # docstring: Specials
PARTY = {"DEMOCRATIC": "DEMOCRAT", "REPUBLICAN": "REPUBLICAN"}
GOVERNOR_D2 = os.path.join(L.REPO, "data", "governor", "2025.json")
CHECK = os.path.join(L.REPO, "data", "local", "check-nj-legislature.json")
GATE_BY = {2023: "within the certifying source (no federal or statewide contest on the ballot)",
           2025: "within the certifying source, and its Governor's list equal to D2's data/governor/2025.json"}


_LOADED = {}


def load(year):
    """The year's normalized lists, or None if any is missing from the cache (read once a run, so that a contest is
    the same object wherever it is read)."""
    if year in _LOADED:
        return _LOADED[year]
    path = os.path.join(SOS.NORM, f"{year}-general.json")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        res = _LOADED[year] = json.load(f)
    if set(res["files"]) != set(LISTS[year]):
        raise SystemExit(f"local_nj_leg: {year}: the lists read are {sorted(res['files'])}, not {sorted(LISTS[year])}")
    return res


def _heading_official(name):
    """Whether every page of a cached list is headed "Official List" (pdftotext's text, page by page)."""
    path = os.path.join(F.CACHE, name)
    txt = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True, check=True).stdout
    pages = [p for p in txt.split("\f") if p.strip()]
    return bool(pages) and all("Official List" in p.splitlines()[0] for p in pages)


_GATES = {}


def gate(year):
    """{"lists": {file: [ok, words]}, "contests": {(office, district): held reason or None}, "year": [ok, words],
    "counties_by_office": {office: {district: [(county, part)]}}}, the gate of the docstring (read once a run)."""
    if year not in _GATES:
        _GATES[year] = _gate(year)
    return _GATES[year]


def _gate(year):
    res = load(year)
    out = {"lists": {}, "contests": {}, "year": [True, "no federal or statewide contest on the ballot: the gate is the "
                                                     "lists' own (a)-(c)" if year == 2023 else None]}
    for k, f in res["files"].items():
        name = f"nj_sos/raw/{year}-official-general-results-{k}.pdf"
        why = []
        if not f["link_text"].startswith("Official General Election Results: "):
            why.append(f"linked as {f['link_text']!r}")
        if not _heading_official(name):
            why.append("a page not headed 'Official List'")
        if f["candidates_on_last_page"] != f["candidates"]:
            why.append(f"its last page counts {f['candidates_on_last_page']} candidates, {f['candidates']} read")
        out["lists"][k] = [not why, "; ".join(why) or "linked as official, every page headed 'Official List', and its "
                                                      "last page's count of candidates equal to those read"]
    for c in res["contests"]:
        why = []
        if not all(x["adds_up"] for x in c["candidates"]):
            why.append("a candidate's county lines do not add up to its Total")
        if c.get("total_adds_up") is False:
            why.append("the contest's Total is not its candidates' totals added up")
        named = {x["county"] for x in c.get("counties_named") or []}
        if c["district"] is not None and (not named or any(set(x["counties"]) - named for x in c["candidates"])):
            why.append("a county line outside the counties its district's heading names")
        out["contests"][(c["office"], c["district"])] = "; ".join(why) or None
    if year == 2025:
        with open(GOVERNOR_D2) as f:
            d2 = [r for r in json.load(f)["contests"] if r["place"]["state"] == "NJ"]
        gov = [c for c in res["contests"] if c["office"] == "Governor"]
        mine = sorted((x["name"], x["total"]) for x in gov[0]["candidates"]) if len(gov) == 1 else None
        theirs = sorted((x["name"], x["votes"]) for x in d2[0]["result"]["candidates"]) if len(d2) == 1 else None
        sha = F.meta(f"nj_sos/raw/{year}-official-general-results-governor.pdf")["sha256"]
        same_file = len(d2) == 1 and f"sha256 {sha[:16]}" in (d2[0]["result"]["source"].get("note") or "")
        ok = mine is not None and mine == theirs and same_file
        out["year"] = [ok, (f"the Governor's list equals D2's data/governor/2025.json for each of its "
                            f"{len(mine)} candidates, and is the same file (sha256 {sha[:16]})") if ok else
                       f"the Governor's list differs from D2's data/governor/2025.json (read here {mine}, D2's "
                       f"{theirs}, same file: {same_file})"]
    by = collections.defaultdict(dict)
    for c in res["contests"]:
        if c["office"] in LEVEL:
            by[c["office"]][c["district"]] = [(x["county"], x["part"]) for x in c.get("counties_named") or []]
    out["counties_by_office"] = by
    return out


def _held(g, c, year):
    k = next(k for k in LISTS[year] if c["office"] in OFFICES_OF_LIST[k])
    if not g["year"][0]:
        return f"held by the gate: {g['year'][1]}"
    if k and not g["lists"][k][0]:
        return f"held by the gate: its list was {g['lists'][k][1]}"
    if g["contests"][(c["office"], c["district"])]:
        return f"held by the gate: {g['contests'][(c['office'], c['district'])]}"
    return None


def _cands(c):
    """The contest's candidates in local_medsl's shape (party DEMOCRAT and REPUBLICAN as MEDSL writes them)."""
    return [{"name": x["name"], "votes": x["total"], "won_marked": True if x["w"] else None,
             "party": PARTY.get(x["party"].upper(), x["party"].upper()), "incumbent": x["incumbent"]}
            for x in c["candidates"]]


def contests(year):
    """[(level, contest, candidates, special)] of the year's legislature."""
    res = load(year)
    if res is None:
        return []
    out = []
    for c in res["contests"]:
        if c["office"] in LEVEL:
            out.append((LEVEL[c["office"]], c, _cands(c), c["office"] not in REGULAR[year]))
    return out


def _lean(prow, year):
    """The Senate's lean for year: Klarner's last New Jersey Senate before it, its contested single-seat races' mean
    Democratic share minus 1/2, and that year (pipeline/local.py partisan_rows, the chamber's lean)."""
    by = collections.defaultdict(list)
    for r_ in prow:
        if r_["state"] == "NJ" and r_["sen"] == 1 and r_["year"] < year:
            by[r_["year"]].append(r_["y"])
    if not by:
        return None
    t = max(by)
    return sum(by[t]) / len(by[t]) - 0.5, t


def partisan_rows(year, prow, LM):
    """Route (a)'s rows of the year's Senate: one Democrat and one Republican on the ballot, both with votes, regular,
    not held, in pipeline/local.py partisan_rows' layout (class C; docstring)."""
    if year not in YEARS or load(year) is None:
        return []
    g = gate(year)
    lean = _lean(prow, year)
    rows = []
    for level, c, cands, special in contests(year):
        if level != "state-upper" or special or _held(g, c, year):
            continue
        b = LM.ballot(cands)
        d = [x for x in b if LM.major(x) == "D"]
        r = [x for x in b if LM.major(x) == "R"]
        if len(d) != 1 or len(r) != 1 or d[0]["votes"] <= 0 or r[0]["votes"] <= 0:
            continue
        inc = (1 if d[0]["incumbent"] else 0) - (1 if r[0]["incumbent"] else 0)
        rows.append({"c": c, "cands": cands, "year": year, "state": "NJ", "sen": 1,
                     "y": d[0]["votes"] / (d[0]["votes"] + r[0]["votes"]), "N": d[0]["votes"] + r[0]["votes"],
                     "cls": "C", "xl": 0.0, "ulag": 0, "inc": inc, "L": lean[0] if lean else 0.0,
                     "L_year": lean[1] if lean else None, "Lmiss": 0 if lean else 1, "d": d[0], "r": r[0]})
    return rows


def class_rows(year, LM):
    """The year's contests for routes (b) and (c) as like races of later years, in pipeline/local.py class_rows'
    layout: the class key and the deciding pair's share. Regular, not held, more names than seats."""
    if year not in YEARS or load(year) is None:
        return []
    g = gate(year)
    rows = []
    for level, c, cands, special in contests(year):
        if special or _held(g, c, year):
            continue
        k = SEATS[c["office"]]
        route, key = LM.leg_structure({"candidates": cands, "magnitude": k})
        if route not in ("class", "boundary"):
            continue
        b = sorted(LM.ballot(cands), key=lambda x: -x["votes"])
        x1, x2 = (b[k - 1]["votes"], b[k]["votes"]) if route == "boundary" else (b[0]["votes"], b[1]["votes"])
        if x1 + x2 > 0:
            rows.append({"c": c, "year": year, "key": key, "s": max(x1, x2) / (x1 + x2), "n": x1 + x2})
    return rows


def records(year, prow, pres, ktrain, kdens, cid, commit, with_p, counts, LM):
    """{(level, year, "NJ"): [records]}: the year's Senate and Assembly. prow: route (a)'s rows of earlier years
    (Klarner's, and 2023's for later years); ktrain: like races of every earlier year."""
    if year not in YEARS or load(year) is None:
        return {}
    import core
    g = gate(year)
    rows = {id(r_["c"]): r_ for r_ in partisan_rows(year, prow, LM)}
    M, kfit = L.fit_before(prow, pres, year)
    train = [r_ for r_ in ktrain if r_["year"] < year]
    out = collections.defaultdict(list)
    for level, c, cands, special in contests(year):
        k = SEATS[c["office"]]
        dist = str(c["district"])
        rec = {"id": cid(f"{year}-{level}-NJ-{dist}" + ("-special" if special else "")),
               "year": year, "date": DATE[year], "level": level, "place": {"state": "NJ", "district": dist},
               "election": "general, special" if special else "general",
               "seats": k if k > 1 else None,
               "result": {"candidates": LM._cands_out(cands, k), "total_votes": sum(x["votes"] for x in cands),
                          "source": SOURCE_KEY},
               "forecasts": [], "gate": GATE_BY[year]}
        for x, y in zip(sorted(cands, key=lambda x: -x["votes"]), rec["result"]["candidates"]):
            if x["incumbent"]:
                y["incumbent"] = True
        rec["place"]["counties_named"] = [x["county"].title() + (" (part)" if x["part"] else "")
                                          for x in c.get("counties_named") or []]
        named = [x["county"] for x in c.get("counties_named") or []]
        for x in c["candidates"]:   # a county the heading names, printed with no count [measured: 2023, SD 29]
            gap = [n.title() for n in named if n not in x["counties"]]
            if gap:
                rec.setdefault("notes", []).append(
                    f"the list prints no count for {x['name'].title()} in {' and '.join(gap)} County, which the "
                    f"district's heading names; the Total, {x['total']:,}, is the other counties' lines added up")
        label = f"{level} {year}"
        b = LM.ballot(cands)
        route, key = LM.leg_structure({"candidates": cands, "magnitude": k})
        held = _held(g, c, year)
        if held:
            p = {"not_computed": held}
            counts[f"{label}: not computed, held by the gate"] += 1
        elif special:
            p = {"not_computed": "a special election: the model's own forecasts are fitted to regular elections"}
            counts[f"{label}: not computed, special"] += 1
            rec["notes"] = ["an election to fill a vacancy [inferred: the Division's 2025 list of the State Senate "
                            "holds this district only, while 2023's holds all 40]"]
        elif route == "zero":
            p = {"value": 0.0, "event": 0.0, "reason": key}
            counts[f"{label}: p = 0"] += 1
        elif route in ("class", "boundary"):
            p = LM.class_p(rec, {"candidates": cands}, route, key, train, kdens, (year, key), commit, with_p, counts,
                           label, k if route == "boundary" else 1)
            if rec["forecasts"]:
                rec["forecasts"][-1]["note"] = ((rec["forecasts"][-1].get("note", "") + "; ") if route == "boundary"
                                                else "") + ("like races of every earlier year in the sources taken "
                                                            f"in, {min(r_['year'] for r_ in train)}-"
                                                            f"{max(r_['year'] for r_ in train)}")
        else:
            r_ = rows.get(id(c))
            top = sorted(cands, key=lambda x: -x["votes"])
            if r_ is None:
                p = {"not_computed": "no votes for the Democrat or the Republican"}
                counts[f"{label}: not computed, no votes"] += 1
            elif {LM.major(top[0]), LM.major(top[1])} != {"D", "R"}:
                p = {"not_computed": "the two leading lines were not the Democrat and the Republican, so the forecast "
                                     "of the Democrat against the Republican is not of the pair that decided this "
                                     "contest (model section 7)"}
                counts[f"{label}: not computed, D and R not the top two"] += 1
            elif M is None or kfit < L.MIN_EARLIER:
                p = {"not_computed": "too few earlier years to fit on"}
                counts[f"{label}: not computed, too few earlier years"] += 1
            else:
                mean, sd, a = L.predict_partisan(M, r_, pres)
                n = r_["N"] - 1
                rec["two_party"] = {"votes": [r_["d"]["votes"], r_["r"]["votes"]], "n_other_voters": n,
                                    "share_first": round(r_["y"], 6)}
                rec["forecast_inputs"] = {"class": "C", "incumbency": r_["inc"], "lean": round(r_["L"], 4),
                                          "lean_year": r_["L_year"], "swing": round(a, 4),
                                          "incumbency_of": "the list's own mark ('* denotes incumbent')"}
                rec["forecasts"].append({"by": "the model's own", "method": L.METHOD, "route": "partisan",
                                         "share": {"of": "Democrat, two-party", "mean": round(mean, 4),
                                                   "sd": round(sd, 4), "tails": "normal"},
                                         "note": f"fitted on Klarner's races of {min(M['years_fitted'])}-"
                                                 f"{max(M['years_fitted'])}; class C, since no last result on the "
                                                 "same lines is read", "source": "model"})
                if with_p:
                    t4 = core.p_contest(n, mean, sd, "t4")
                    p = L._p_block(n, mean, sd, f"the model's own ({L.METHOD}), normal", commit,
                                   {"t4": {"value": t4["p"], "event": t4["event"], "method": t4["method"]}})
                    p["forecast_scope"] = L.FORECAST_SCOPE["C"]
                    counts[f"{label}: p computed, partisan"] += 1
                else:
                    p = {}
        rec["p"] = p
        out[(level, year, "NJ")].append(rec)
    return dict(out)


def source_block(year):
    res = load(year)
    g = gate(year)
    files = "; ".join(f"{k}: {f['url']} (sha256 {f['sha256'][:16]}, {f['contests']} contests, {f['candidates']} "
                      f"candidates)" for k, f in sorted(res["files"].items()) if k != "governor")
    read = max(f["read_utc"] for k, f in res["files"].items() if k != "governor")
    note = (f"the Official Lists of the State Senate and General Assembly, read by pipeline/intake/nj_sos.py: {files}. "
            f"Gate {GATE_BY[year]} (pipeline/local_nj_leg.py; data/local/check-nj-legislature.json): each list "
            f"linked as official and headed 'Official List', its county lines adding up, its candidates' county "
            f"lines within the counties its districts' headings name"
            + (f"; {g['year'][1]}" if year == 2025 else ""))
    return F.source(f"New Jersey Division of Elections, Official Lists of the General Election of {DATE[year]}: "
                    + " and ".join({"state-senate": "State Senate", "general-assembly": "General Assembly",
                                    "state-senate-35ld": "State Senate, 35th Legislative District"}[k]
                                   for k in LISTS[year] if k != "governor"),
                    SOS.PAGE.format(year=year), read, SOS.LICENCE, mark="stated", via="pipeline/intake/nj_sos.py",
                    note=note)


def check():
    out = {"about": "the gate within the certifying source of New Jersey's 2023 and 2025 legislatures (pipeline/"
                    "local_nj_leg.py, docstring): (a) each list linked as official and headed 'Official List', its last "
                    "page's count of candidates equal to those read; (b) each candidate's county lines adding up to "
                    "its Total and each contest's Total to its candidates'; (c) each candidate's county lines within "
                    "the counties its district's heading names; (d) 2025: the Governor's list equal to D2's "
                    "data/governor/2025.json and the same file. Proposed by worker D3, 2026-11-07, for the "
                    "orchestrator's ruling.", "years": {}}
    for year in YEARS:
        if load(year) is None:
            out["years"][str(year)] = "not read"
            continue
        g = gate(year)
        held = {f"{o} {d}": w for (o, d), w in g["contests"].items() if w}
        same = {}
        cbo = g["counties_by_office"]
        if year == 2023:
            same["senate_and_assembly"] = cbo["State Senate"] == cbo["General Assembly"]
        out["years"][str(year)] = {
            "lists": g["lists"], "year": g["year"], "contests": len(g["contests"]), "contests_held": held,
            "districts_counties_same": same}
    if all(str(y) in out["years"] and isinstance(out["years"][str(y)], dict) for y in YEARS):
        a = gate(2023)["counties_by_office"]["General Assembly"]
        b = gate(2025)["counties_by_office"]["General Assembly"]
        out["years"]["2025"]["districts_counties_same"]["assembly_2023_and_2025"] = a == b
    with open(CHECK, "w") as f:
        json.dump(out, f, indent=1)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("what", choices=["check"])
    ap.parse_args()
    print(json.dumps(check(), indent=1))


if __name__ == "__main__":
    main()
