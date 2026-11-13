"""pipeline/local_va_leg.py: Virginia's legislatures of 2023 and 2025, from the Department of Elections' results as read
before it refused us (pipeline/intake/va_elect.py), gated within the certifying source, in the layout
pipeline/local_medsl.py writes.

Written 2026-11-07 by worker D3 (briefs/D3-data-local.md, step 2) at the orchestrator's order of 10:35: "queue the
odd-year legislatures after Klarner's 2022 (MS, NJ, VA 2023; NJ, VA 2025) from each state's certified files, each with
a gate you propose. Reason: law 5 and Zach's 03:13 word, as much data as can be found." Klarner's Virginia ends with
the House of Delegates of 2021, and MEDSL holds no odd year.

What the files hold [stated: the rendered pages and the Media Export files; measured: what va_elect.py reads]:
  2023  "2023 November General and Special Elections", November 7, 2023: the Senate of Virginia's 40 districts and the
        House of Delegates' 100 ("Member, Senate of Virginia (1st District)", ...), each "Vote for only one".
  2025  "2025 November General", November 4, 2025: the House of Delegates' 100, and the Governor (D2's level,
        data/governor/2025.json), the Lieutenant Governor and the Attorney General.
  Each contest: each candidate's party and votes, a write-in line, and each locality's (county or independent city)
  line with its precincts. The page marks each contest's winner "Winner"; 2023's page as read shows all 140 of its
  legislature's contests, and 2025's its first 50 contests (the three statewide and districts 1-47), so in districts
  48-100 of 2025 the winner is taken as the leading candidate for the one seat, and marked so ([inferred]; the
  orchestrator, 18:32: "a figure resting on a page we saw and one resting on a rule we applied must look different in
  the record").

Routes (pipeline/local.py's, as for MEDSL's 2024 legislatures in pipeline/local_medsl.py):
  - A contest with one name on the ballot: p 0, unless write-ins drew local.WRITE_IN_STRONG of the winner's votes.
  - One Democrat against one Republican: route (a). Its class:
      2023: class C. No result on 2023's lines before 2023 is in the sources taken in: Klarner's Virginia races of 2019
            and 2021 carry his district regimes of 2011 and 2019 [measured].
      2025: the district's 2023 contest is its last result on the same lines where at least local_medsl.SAME_LINES of
            its 2025 precincts were among its 2023 precincts (the rule for 2024 against 2022): class A if a Democrat and
            a Republican both drew votes in 2023, class B if one did, else class C.
    Incumbency is matched by name (local_medsl.name_keys, as for 2024), +1 for a Democrat, -1 for a Republican, to the
    winners of the chamber's last general before: 2023, Klarner's Senate of 2019 and House of Delegates of 2021; 2025,
    the House of Delegates of 2023 read here. No special election since those is read (the Department refused us
    before any was), so a member elected in one counts as not sitting [measured gap].
    The chamber's lean is its last general before the year: the mean Democratic share of its contested single-seat
    races, minus 1/2 (Klarner's 2019 Senate and 2021 House for 2023; the 2023 House read here for 2025).
    Fitted on every earlier race of route (a) in the sources taken in (the orchestrator, 11:56: "earlier cycles only
    means every earlier contest"): for 2023, Klarner's of 1968-2022; for 2025, those, New Jersey's and Virginia's
    Senates and House of 2023, and MEDSL's 2024 legislatures.
  - Other contests with more names than seats: route (b), like past races of their class.
  And 2023 feeds the later years: its route (a) races join the fit of 2024 and 2025 (partisan_rows), its other contests
  the like races of 2024 and after (class_rows).

The gate within the certifying source (2023 has no federal or statewide contest on its ballot; 2025's Governor is D2's,
read from the same site at 12:46) [proposed, for the orchestrator's ruling; the orchestrator's list of 18:32]:
  (a) the election's page, rendered, is headed "OFFICIAL RESULTS", the Department's results page links it (directly,
      or by its Election Results Directory, which lists it), and its "Media Export" link is the file read; and where the
      page shows a contest, its candidates and votes are the file's;
  (b) each contest's locality lines add up, option by option, write-ins included, to its statewide count, and no
      locality line names an option the statewide count lacks;
  (c) its localities are the district's own: as many locality lines as the page prints ("Localities reporting n/n",
      all reporting); in 2025's districts the page as read did not show, the same localities as the district's 2023
      contest, whose count the 2023 page prints [the lines are the same; measured: each of the 100 House districts
      has the same localities in both years];
  (d) 2025: the file's Governor equals D2's data/governor/2025.json to the vote, and D2's is the same site's count of
      the same election.
  A contest that fails (a)'s last part, (b) or (c) is held; a year that fails the rest of (a), or (d), holds all.
  Recorded beside it, not a gate: each locality line's precincts add up to it (not so in some, noted on the record).

  check()  the gates: data/local/check-va-legislature.json.

Run:  VOTE_CACHE=/tmp/vote-cache python3 -I pipeline/local_va_leg.py check
"""
import argparse
import collections
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fetch as F  # noqa: E402
from intake import va_elect as VA  # noqa: E402
import local as L  # noqa: E402

YEARS = (2023, 2025)
SOURCE_KEY = "va_elect"
TITLE = re.compile(r"Member, (Senate of Virginia|House of Delegates) \((\d+)(?:st|nd|rd|th) District\)")
LEVEL = {"Senate of Virginia": "state-upper", "House of Delegates": "state-lower"}
SEN = {"Senate of Virginia": 1, "House of Delegates": 0}
REGULAR = {2023: {"Senate of Virginia", "House of Delegates"}, 2025: {"House of Delegates"}}
PARTY = {"Democratic": "DEMOCRAT", "Republican": "REPUBLICAN"}
LAST_KLARNER = {"Senate of Virginia": 2019, "House of Delegates": 2021}   # docstring: incumbency
GOVERNOR_D2 = os.path.join(L.REPO, "data", "governor", "2025.json")
CHECK = os.path.join(L.REPO, "data", "local", "check-va-legislature.json")
GATE_BY = {2023: "within the certifying source (no federal or statewide contest on the ballot)",
           2025: "within the certifying source, and its Governor equal to D2's data/governor/2025.json"}
RULED = ("proposed by worker D3; the orchestrator, 2026-11-07 18:49 UTC: accepted as proposed, with the 9th Senate "
         "district of 2023 held (\"like NJ's, it can be checked from the read files alone, and the Governor match ties "
         "them to a count already gated\")")


_LOADED = {}


def load(year):
    """The year's normalized election, or None if it is not in the cache (read once a run, so that a contest is the
    same object wherever it is read)."""
    if year not in _LOADED:
        path = os.path.join(VA.NORM, f"{year}-general.json")
        if not os.path.exists(path):
            return None
        with open(path) as f:
            _LOADED[year] = json.load(f)
    return _LOADED[year]


def _leg(c):
    m = TITLE.fullmatch(c["title"])
    return (m.group(1), m.group(2)) if m else None


def _governor_equal():
    res = load(2025)
    with open(GOVERNOR_D2) as f:
        d2 = [r for r in json.load(f)["contests"] if r["place"]["state"] == "VA"]
    gov = [c for c in res["contests"] if c["title"] == "Governor"]
    mine = sorted((o["name"], o["votes"]) for o in gov[0]["options"]) if len(gov) == 1 else None
    theirs = sorted((x["name"], x["votes"]) for x in d2[0]["result"]["candidates"]) if len(d2) == 1 else None
    url = d2[0]["result"]["source"].get("url", "") if len(d2) == 1 else ""
    same = url.startswith(VA.SITE) and VA.ELECTION[2025] in url
    ok = mine is not None and mine == theirs and same
    return [ok, (f"the file's Governor equals D2's data/governor/2025.json to the vote for each of its {len(mine)} "
                 f"lines, and D2's is the same site's count of the same election ({url}, read "
                 f"{d2[0]['result']['source'].get('read_utc')})") if ok else
            f"the file's Governor differs from D2's data/governor/2025.json (read here {mine}, D2's {theirs}, same "
            f"site and election: {same})"]


_GATES = {}


def gate(year):
    """{"year": [ok, words], "contests": {title: held reason or None}}, the gate of the docstring (once a run)."""
    if year not in _GATES:
        _GATES[year] = _gate(year)
    return _GATES[year]


def _gate(year):
    res = load(year)
    why = []
    if not res["official"]:
        why.append("its page is not headed 'OFFICIAL RESULTS'")
    out = {"year": [not why, "; ".join(why) or (f"the page is headed {res['official_text']!r}; {res['linked']}; its "
                                                 f"'Media Export' link is the file read")],
           "contests": {}}
    if year == 2025 and out["year"][0]:
        out["year"] = _governor_equal()
    prior = {}
    if year == 2025 and load(2023) is not None:
        prior = {_leg(c): c for c in load(2023)["contests"] if _leg(c)}
    for c in res["contests"]:
        if not _leg(c):
            continue
        w = []
        if c["page"]["shown"] and not c["page"]["equal"]:
            w.append("the page shows other candidates or votes than the file holds")
        if not c["parts_add_up"]:
            if c["extra_in_localities"]:
                w.append("its locality lines count " + "; ".join(
                    f"{e['votes']:,} votes for {e['name']} (in {', '.join(e['localities'])})"
                    for e in c["extra_in_localities"]) + ", whom its statewide count does not hold")
            else:
                w.append("its locality lines do not add up to its statewide count")
        if c["page"]["shown"]:
            a, _, n = (c["page"]["localities_reporting"] or "/").partition("/")
            if not (a == n == str(c["localities"])):
                w.append(f"the page prints 'Localities reporting {c['page']['localities_reporting']}', and the file "
                         f"has {c['localities']} locality lines")
        else:
            p = prior.get(_leg(c))
            if p is None or p["locality_ids"] != c["locality_ids"]:
                w.append("the page as read did not show this contest, and its localities are not its district's of "
                         "2023")
        out["contests"][c["title"]] = "; ".join(w) or None
    return out


def _held(g, c):
    if not g["year"][0]:
        return f"held by the gate: {g['year'][1]}"
    if g["contests"].get(c["title"]):
        return f"held by the gate: {g['contests'][c['title']]}"
    return None


def _gate_field(g, c, year):
    """The record's `gate`, in the shape of New Jersey's (data/README.md)."""
    why = g["contests"].get(c["title"]) or ""
    out = {"by": GATE_BY[year], "ruled": RULED, "official": g["year"][0] if year == 2023 else load(year)["official"],
           "official_how": "the results site's page of the election, rendered, headed 'OFFICIAL RESULTS', and linked "
                           "from the Department's results page",
           "page_equal": None if not c["page"]["shown"] else "other candidates or votes" not in why,
           "parts_add_up": c["parts_add_up"],
           "localities_own": "Localities reporting" not in why and "not its district's" not in why,
           "localities_how": ("as many locality lines as the page prints ('Localities reporting "
                              f"{c['page']['localities_reporting']}')" if c["page"]["shown"] else
                              "the page as read did not show it: the same localities as its district's 2023 contest")}
    if year == 2025:
        out["statewide_equal"] = g["year"][1]
    return out


def _cands(c):
    """The contest's candidates in local_medsl's shape (party DEMOCRAT and REPUBLICAN as MEDSL writes them). Where the
    page showed the contest, won_marked is its "Winner" mark; elsewhere local_medsl._cands_out takes the leader."""
    out = []
    for o in c["options"]:
        x = {"name": o["name"], "votes": o["votes"], "as_named": True, "writein": o["write_in"],
             "party": PARTY.get(o["party"] or "", (o["party"] or "").upper())}
        if c["page"]["shown"]:
            x["won_marked"] = True if o.get("winner_marked") else None
        out.append(x)
    return out


def contests(year):
    """[(level, chamber, district, contest, candidates, special)] of the year's legislature."""
    res = load(year)
    if res is None:
        return []
    out = []
    for c in res["contests"]:
        k = _leg(c)
        if k:
            out.append((LEVEL[k[0]], k[0], k[1], c, _cands(c), k[0] not in REGULAR[year]))
    return out


def _lean(prow, sen, year):
    """The chamber's lean for year: its last general before in prow (Klarner's, or 2023's read here), the mean
    Democratic share of its contested single-seat races minus 1/2, and that year."""
    by = collections.defaultdict(list)
    for r_ in prow:
        if r_["state"] == "VA" and r_["sen"] == sen and r_["year"] < year:
            by[r_["year"]].append(r_["y"])
    if not by:
        return None
    t = max(by)
    return sum(by[t]) / len(by[t]) - 0.5, t


def _sitting(year, chamber, LM):
    """{(surname, initial, party)}: the winners of the chamber's last general before year (docstring)."""
    out = set()
    if year == 2023:
        for c in L.load_klarner():
            if c["state"] == "VA" and c["sen"] == SEN[chamber] and c["year"] == LAST_KLARNER[chamber] \
                    and c["etype"] == "g":
                for a in c["cands"]:
                    if a["outcome"] == "w" and a["party"] in ("d", "r"):
                        out.add(LM.name_key(a["name"]) + (a["party"].upper(),))
    else:
        for level, ch, dist, c, cands, special in contests(2023):
            if ch == chamber and not special:
                for x in cands:
                    if x.get("won_marked") and LM.major(x):
                        out.add(LM.name_key(x["name"]) + (LM.major(x),))
    return out


def _last(c, year, LM):
    """2025: (class, xl, ulag, last, lines share) from the district's 2023 contest (docstring)."""
    if year != 2025 or load(2023) is None:
        return "C", 0.0, 0, None, None
    prior = {_leg(p): p for p in load(2023)["contests"] if _leg(p)}
    p = prior.get(_leg(c))
    if p is None or not c["precinct_ids"]:
        return "C", 0.0, 0, None, None
    lines = len(set(c["precinct_ids"]) & set(p["precinct_ids"])) / len(c["precinct_ids"])
    if lines < LM.SAME_LINES:
        return "C", 0.0, 0, None, lines
    pc = _cands(p)
    dv = sum(x["votes"] for x in LM.ballot(pc) if LM.major(x) == "D")
    rv = sum(x["votes"] for x in LM.ballot(pc) if LM.major(x) == "R")
    if dv > 0 and rv > 0:
        return "A", dv / (dv + rv) - 0.5, 0, dv / (dv + rv), lines
    if dv > 0 or rv > 0:
        return "B", 0.0, (1 if dv > 0 else -1), ("D" if dv > 0 else "R"), lines
    return "C", 0.0, 0, None, lines


def partisan_rows(year, prow, LM):
    """Route (a)'s rows of the year: one Democrat and one Republican on the ballot, both with votes, regular, not held,
    in pipeline/local.py partisan_rows' layout (docstring: class, incumbency, lean)."""
    if year not in YEARS or load(year) is None:
        return []
    g = gate(year)
    rows = []
    sitting = {ch: _sitting(year, ch, LM) for ch in REGULAR[year]}
    for level, ch, dist, c, cands, special in contests(year):
        if special or _held(g, c):
            continue
        b = LM.ballot(cands)
        d = [x for x in b if LM.major(x) == "D"]
        r = [x for x in b if LM.major(x) == "R"]
        if len(d) != 1 or len(r) != 1 or d[0]["votes"] <= 0 or r[0]["votes"] <= 0:
            continue
        inc = (1 if any(k + ("D",) in sitting[ch] for k in LM.name_keys(d[0]["name"])) else 0) - \
            (1 if any(k + ("R",) in sitting[ch] for k in LM.name_keys(r[0]["name"])) else 0)
        lean = _lean(prow, SEN[ch], year)
        cls, xl, ulag, last, lines = _last(c, year, LM)
        rows.append({"c": c, "cands": cands, "year": year, "state": "VA", "sen": SEN[ch],
                     "y": d[0]["votes"] / (d[0]["votes"] + r[0]["votes"]), "N": d[0]["votes"] + r[0]["votes"],
                     "cls": cls, "xl": xl, "ulag": ulag, "inc": inc, "L": lean[0] if lean else 0.0,
                     "L_year": lean[1] if lean else None, "Lmiss": 0 if lean else 1, "d": d[0], "r": r[0],
                     "last": last, "lines": lines})
    return rows


def class_rows(year, LM):
    """The year's contests for route (b) as like races of later years, in pipeline/local.py class_rows' layout: the
    class key and the deciding pair's share. Regular, not held, more names than seats."""
    if year not in YEARS or load(year) is None:
        return []
    g = gate(year)
    rows = []
    for level, ch, dist, c, cands, special in contests(year):
        if special or _held(g, c):
            continue
        route, key = LM.leg_structure({"candidates": cands, "magnitude": 1})
        if route != "class":
            continue
        b = sorted(LM.ballot(cands), key=lambda x: -x["votes"])
        x1, x2 = b[0]["votes"], b[1]["votes"]
        if x1 + x2 > 0:
            rows.append({"c": c, "year": year, "key": key, "s": max(x1, x2) / (x1 + x2), "n": x1 + x2})
    return rows


INC_OF = {2023: "matched by name to the winners of Klarner's last {chamber} ({y}); no special election since is read "
                "(the Department refused us)",
          2025: "matched by name to the winners of the {chamber} of 2023 read here; no special election since is read "
                "(the Department refused us)"}


def _fitted_on(M, year):
    return (f"fitted on Klarner's races of {min(M['years_fitted'])}-2022" if year == 2023 else
            f"fitted on the races of {min(M['years_fitted'])}-{max(M['years_fitted'])} in the sources taken in "
            "(Klarner's, New Jersey's and Virginia's of 2023, and MEDSL's 2024 legislatures)")


def records(year, prow, pres, ktrain, kdens, cid, commit, with_p, counts, LM):
    """{(level, year, "VA"): [records]}: the year's Senate and House of Delegates. prow: route (a)'s rows of every
    earlier year in the sources taken in; ktrain: like races of every earlier year."""
    if year not in YEARS or load(year) is None:
        return {}
    import core
    g = gate(year)
    res = load(year)
    rows = {id(r_["c"]): r_ for r_ in partisan_rows(year, prow, LM)}
    M, kfit = L.fit_before(prow, pres, year)
    train = [r_ for r_ in ktrain if r_["year"] < year]
    out = collections.defaultdict(list)
    for level, ch, dist, c, cands, special in contests(year):
        rec = {"id": cid(f"{year}-{level}-VA-{dist}" + ("-special" if special else "")),
               "year": year, "date": res["date"], "level": level, "place": {"state": "VA", "district": dist},
               "election": "general, special" if special else "general",
               "seats": None,
               "result": {"candidates": LM._cands_out(cands, 1), "total_votes": sum(x["votes"] for x in cands),
                          "source": SOURCE_KEY},
               "forecasts": [], "gate": _gate_field(g, c, year)}
        for y in rec["result"]["candidates"]:
            if y["won"]:
                y["won_mark"] = "stated" if c["page"]["shown"] else "inferred"
        rec["place"]["localities"] = c["localities"]
        if c["precincts_short"]:
            rec.setdefault("notes", []).append(
                "the source's precinct lines add up to fewer votes than its locality line: " + "; ".join(
                    f"{s['option']} in {s['locality']}, {s['precincts']:,} against {s['locality_line']:,}"
                    for s in c["precincts_short"])
                + "; not explained (no source read says why); the record is the locality lines, which add up to the "
                  "statewide count the page shows (the orchestrator, 18:49: \"say that in the note only if a source "
                  "states it; otherwise say 'not explained'\")")
        if not c["page"]["shown"]:
            rec.setdefault("notes", []).append(
                "the winner is the leading candidate for the one seat [inferred]: the results page as read showed its "
                "first 50 contests, not this one, so its 'Winner' mark was not seen")
        label = f"{level} {year}"
        b = LM.ballot(cands)
        route, key = LM.leg_structure({"candidates": cands, "magnitude": 1})
        swi = LM.strong_write_in(cands, 1) if route == "zero" else None
        held = _held(g, c)
        if held:   # with one name on the ballot as well: L.HELD_ONE_NAME (ruling of 2026-11-13 00:26)
            p = {"not_computed": L.held_one_name(held) if route == "zero" else held}
            counts[f"{label}: not computed, held by the gate"] += 1
        elif special:
            p = {"not_computed": "a special election: the model's own forecasts are fitted to regular elections"}
            counts[f"{label}: not computed, special"] += 1
        elif route == "zero" and swi:
            share, generic = swi
            p = {"not_computed": "one name on the ballot for each seat, but write-ins received "
                                 + (f"{100 * share:.0f}% of the last winner's votes" if share else "votes")
                                 + (" (counted together, so whether one write-in candidate did is not reported)"
                                    if generic else "")
                                 + f": {L.METHOD} has no forecast route for write-in contests"}
            counts[f"{label}: not computed, unopposed with strong write-ins"] += 1
        elif route == "zero":
            p = {"value": 0.0, "event": 0.0, "reason": key}
            counts[f"{label}: p = 0"] += 1
        elif route in ("class", "boundary"):
            p = LM.class_p(rec, {"candidates": cands}, route, key, train, kdens, (year, key), commit, with_p, counts,
                           label, 1)
            if rec["forecasts"]:
                rec["forecasts"][-1]["note"] = ("like races of every earlier year in the sources taken in, "
                                                f"{min(r_['year'] for r_ in train)}-{max(r_['year'] for r_ in train)}")
        else:
            r_ = rows.get(id(c))
            top = sorted(cands, key=lambda x: -x["votes"])
            if r_ is None:
                p = {"not_computed": "no votes for the Democrat or the Republican"}
                counts[f"{label}: not computed, no votes"] += 1
            elif any(x.get("writein") or LM._is_generic(x["name"]) for x in top[:2]) or \
                    {LM.major(top[0]), LM.major(top[1])} != {"D", "R"}:
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
                inputs = {"class": r_["cls"], "incumbency": r_["inc"], "lean": round(r_["L"], 4),
                          "lean_year": r_["L_year"], "swing": round(a, 4),
                          "incumbency_of": INC_OF[year].format(chamber=ch, y=LAST_KLARNER[ch])}
                if year == 2025:
                    inputs["lines_unchanged_share"] = None if r_["lines"] is None else round(r_["lines"], 3)
                if r_["cls"] == "A":
                    inputs.update({"last_D": round(r_["last"], 4), "last_year": 2023})
                elif r_["cls"] == "B":
                    inputs.update({"last_unopposed": r_["last"], "last_year": 2023})
                rec["forecast_inputs"] = inputs
                note = _fitted_on(M, year) + "; incumbency matched by name"
                if year == 2023:
                    note += "; class C, since no last result on the same lines is read"
                rec["forecasts"].append({"by": "the model's own", "method": L.METHOD, "route": "partisan",
                                         "share": {"of": "Democrat, two-party", "mean": round(mean, 4),
                                                   "sd": round(sd, 4), "tails": "normal"},
                                         "note": note, "source": "model"})
                if with_p:
                    t4 = core.p_contest(n, mean, sd, "t4")
                    p = L._p_block(n, mean, sd, f"the model's own ({L.METHOD}), normal", commit,
                                   {"t4": {"value": t4["p"], "event": t4["event"], "method": t4["method"]}})
                    p["forecast_scope"] = L.FORECAST_SCOPE[r_["cls"]]
                    counts[f"{label}: p computed, partisan"] += 1
                else:
                    p = {}
        rec["p"] = p
        out[(level, year, "VA")].append(rec)
    return dict(out)


def source_block(year):
    res = load(year)
    g = gate(year)
    fx, fp = res["files"]["export"], res["files"]["election"]
    note = (f"the results site's page of '{res['name']}' ({fp['url']}, {fp['how']}, finished {fp['finished_utc']}, "
            f"sha256 {fp['sha256'][:16]}; headed {res['official_text']!r}) and its 'Media Export' file ({fx['url']}, "
            f"finished {fx['finished_utc']}, sha256 {fx['sha256'][:16]}, created {res['export_created_utc'][:19]}Z), "
            f"read by pipeline/intake/va_elect.py before the Department refused us (2026-11-07 18:27:48 UTC; nothing "
            f"is requested from it again). Gate {GATE_BY[year]} (pipeline/local_va_leg.py; "
            f"data/local/check-va-legislature.json): the page headed 'OFFICIAL RESULTS' and linked from the "
            f"Department's results page, its figures the file's, each contest's locality lines adding up to its "
            f"statewide count, its localities the district's own"
            + (f"; {g['year'][1]}" if year == 2025 else ""))
    return F.source(f"Virginia Department of Elections, results of the {res['name']}, {res['date']}: "
                    + ("Senate of Virginia and House of Delegates" if year == 2023 else "House of Delegates"),
                    fp["url"], fx["read_utc"], VA.LICENCE, mark="stated", via="pipeline/intake/va_elect.py",
                    note=note, sha256=fx["sha256"])


def check():
    out = {"about": "the gate within the certifying source of Virginia's 2023 and 2025 legislatures (pipeline/"
                    "local_va_leg.py, docstring): (a) the election's page headed 'OFFICIAL RESULTS', linked from the "
                    "Department's results page, its Media Export link the file read, and the figures it shows the "
                    "file's; (b) each contest's locality lines adding up to its statewide count, naming no option it "
                    "lacks; (c) its localities the district's own (as many as the page prints; in 2025's contests the "
                    "page as read did not show, its district's 2023 localities); (d) 2025: the Governor equal to "
                    "D2's data/governor/2025.json. Proposed by worker D3, 2026-11-07, for the orchestrator's ruling. "
                    "Beside it, not a gate: each locality line's precincts adding up to it.", "years": {}}
    for year in YEARS:
        res = load(year)
        if res is None:
            out["years"][str(year)] = "not read"
            continue
        g = gate(year)
        leg = [c for c in res["contests"] if _leg(c)]
        out["years"][str(year)] = {
            "year": g["year"], "contests": len(leg),
            "shown_on_the_page": sum(c["page"]["shown"] for c in leg),
            "winners_inferred": sum(1 for c in leg if not c["page"]["shown"]),
            "contests_held": {t: w for t, w in g["contests"].items() if w},
            "precincts_short_of_their_locality_line": {c["title"]: c["precincts_short"] for c in leg
                                                       if c["precincts_short"]},
            "files": {k: {kk: v[kk] for kk in ("url", "finished_utc", "sha256", "how") if kk in v}
                      for k, v in res["files"].items()}}
    if all(isinstance(out["years"].get(str(y)), dict) for y in YEARS):
        a = {_leg(c): c["locality_ids"] for c in load(2023)["contests"] if _leg(c) and _leg(c)[0] == "House of Delegates"}
        b = {_leg(c): c["locality_ids"] for c in load(2025)["contests"] if _leg(c)}
        out["years"]["2025"]["house_districts_with_2023_localities"] = sum(1 for k in b if a.get(k) == b[k])
    with open(CHECK, "w") as f:
        json.dump(out, f, indent=1)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("what", choices=["check"])
    ap.parse_args()
    print(json.dumps(check(), indent=1)[:4000])


if __name__ == "__main__":
    main()
