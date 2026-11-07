"""pipeline/measures.py: ballot measures and retentions from MEDSL's precinct returns, with p where the law and the
like-past-measures route allow it.

Written 2026-11-07 by worker D3 (briefs/D3-data-local.md, step 4), for pipeline/local_medsl.py's build.

The orchestrator's ruling of 2026-11-07 06:16: "Measures: approved, except local thresholds are never inferred.
Read statewide thresholds from each constitution or statute, with URLs ... Where it cannot be read, p is not
computed, with that reason ... The like-past-measures route is approved, marked as the model's own ... Refit with
2016 added, report the calibration again, and say in REPORT.md if it still under-forecasts near 1/2."

  threshold   data/measure/thresholds.json: each state's rule, read from its constitution or statute, with the
              URL, the words and the time read. A measure gets the rule for its type (an amendment, a statute, a
              bond, a convention question, a retention), the type read from the source's title; where the title
              does not give it, the state's rules must all agree and must cover every kind of question it puts to
              voters ("complete" in the file). An exception that turns on what a measure does (a new tax, a repeal
              only, a wildlife law) holds p back where the source does not show whether the measure is one. A rule that turns on more than the yes
              share of those voting on the question (a turnout floor, a share of all ballots cast) is recorded and
              p is not computed: the model forecasts the share, not the ballots left blank.
  forecast    like past measures: the density of the yes share at the threshold t among the measures of the same
              class (statewide or local; measure or retention) of earlier years in the sources taken in, through
              the lay form of the like-race route (MIN_CLASS races at least; the window widens 1, 2, 5 points).
  p           model section 7: a Yes ballot decides with chance about (1 - t) f(t) / n, a No ballot t f(t) / n,
              n the other voters on the question.
"""
import collections
import json
import os
import re

import local as L

HERE = os.path.dirname(os.path.abspath(__file__))
THRESHOLDS = os.path.join(L.REPO, "data", "measure", "thresholds.json")
STATEWIDE_COVER = 0.9   # a question filed with the state's offices is statewide when it carries at least this share
                        # of the most precincts any of the state's contests carries that year; and where the source
                        # names counties, the source holds the whole state when the year's contests carry at least
                        # this share of the most counties any year's do (MEDSL's 2016 file holds one South Dakota
                        # county; Alaska's files before 2024 name no county at all)

_RET_WORDS = re.compile(r"RETENTION|RETAIN")
_COURT = re.compile(r"\b(JUDGE|JUSTICE|COURT|MAGISTRATE)\b")


def kind_of(c):
    """'retention' for a judge's yes-or-no question, else 'measure'. A title that reads as an amendment, a statute,
    a bond or a convention question is a measure even where it names a court ('STATEWIDE AMENDMENT NO. 2 -
    STATEWIDE BUSINESS COURT')."""
    text = (c["office"] + " " + (c.get("subject") or "")).upper()
    if any(x["name"] in ("RETAIN", "NOT RETAIN", "DO NOT RETAIN") for x in c["candidates"]):
        return "retention"
    if type_of(c) in ("amendment", "statute", "bond", "convention"):
        return "measure"
    if _RET_WORDS.search(text) or _COURT.search(text):
        return "retention"
    return "measure"


def _known(counties):
    return {x for x in counties if x and x != "NA"}


def coverage(contests_by_year):
    """The references for scope_of: the most precincts any contest of the state carries in each year, and the most
    named counties any one year's contests of the state carry."""
    prec, cnty = collections.Counter(), collections.Counter()
    for year, cs in contests_by_year.items():
        by = collections.defaultdict(set)
        for c in cs:
            prec[(c["state"], year)] = max(prec[(c["state"], year)], c.get("precincts") or 0)
            by[c["state"]].update(_known(c["counties"]))
        for st, s in by.items():
            cnty[st] = max(cnty[st], len(s))
    return {"precincts": prec, "counties": cnty}


def scope_of(c, ref, year):
    """'statewide', 'partial' (a statewide question in a year whose source holds only part of the state) or
    'local'. A state's own file read by county, with no precinct count (Indiana's, pipeline/local_in.py), is
    statewide when it covers the state's counties."""
    if c["dataverse"] != "STATE":
        return "local"
    if c.get("precincts") is None and c.get("source") not in (None, "medsl"):
        known = _known(c["counties"])
        n = ref["counties"][c["state"]]
        return "statewide" if n and len(known) >= STATEWIDE_COVER * n else "local"
    if (c.get("precincts") or 0) < STATEWIDE_COVER * ref["precincts"][(c["state"], year)]:
        return "local"
    known = _known(c["counties"])
    if known and ref["counties"][c["state"]] and len(known) < STATEWIDE_COVER * ref["counties"][c["state"]]:
        return "partial"
    return "statewide"


# The type as the source's title states it, in the words states use for it. 'REFERENDUM' and 'INITIATIVE PETITION'
# alone do not settle it (Oklahoma's legislative referendums and initiative petitions can each amend the
# constitution), nor a dollar figure (Oregon's 2016 Measure 97 is a tax), so they leave the type unread.
_TYPES = [
    ("convention", r"\bCONVENTION\b"),
    ("bond", r"\bBONDS?\b|GENERAL OBLIGATION"),
    ("amendment", r"CONSTITUTION|\bAMEND|\bCON\.? AMEND|^CA NO\b|\bCI-\d|\bHJR\b|\bSJR\b|JOINT RESOLUTION"),
    ("statute", r"\(STATUTORY\)|REFERRED LAW|REFERRED ACT|\bAN ACT\b|LEGISLATIVE INITIATIVE|INITIATED MEASURE|"
                r"INITIATIVE MEASURE|INITIATIVE NO\b|^INITIATIVE \d|\bI-\d|REFERENDUM MEASURE"),
    ("advisory", r"\bADVISORY\b"),
]


def type_of(c):
    """The measure's type as its title in the source shows it, or None where the title does not say."""
    t = c["office"].upper() + " " + (c.get("subject") or "").upper()
    for name, pat in _TYPES:
        if re.search(pat, t):
            return name
    return None


def load_thresholds():
    if not os.path.exists(THRESHOLDS):
        return {"rules": [], "states": {}}
    with open(THRESHOLDS) as f:
        return json.load(f)


def _in_year(r, year):
    return (r.get("from_year") or 0) <= year <= (r.get("to_year") or 9999)


def rule_for(c, kind, book, year):
    """(rule, how, None) or (None, None, the reason p is not computed) for a statewide measure or retention. `how`
    says how the rule was matched to the question: by the type its title states, or because every rule read for the
    state's measures sets the same threshold."""
    st = c["state"]
    states = book.get("states", {})
    mine = [r for r in book["rules"] if r["state"] == st and _in_year(r, year)]
    if not mine:
        why = (states.get(st) or {}).get("not_read")
        return None, None, (f"the thresholds of this state's {kind}s are not read: {why}" if why else
                            f"the thresholds of this state's {kind}s are not read from its constitution or statute "
                            f"for {year}")
    if kind == "retention":
        rs = [r for r in mine if r["type"] == "retention"]
        if not rs:
            return None, None, "the threshold of this state's judicial retentions is not read"
        return _one(rs, "retention")
    ty = type_of(c)
    if ty == "advisory":
        return None, None, "an advisory question: the law read sets no threshold for it"
    pool = [r for r in mine if r["type"] != "retention"]
    if not pool:
        return None, None, f"the thresholds of this state's measures are not read for {year}"
    if ty is not None:
        pool = [r for r in pool if r["type"] == ty]
        if not pool:
            return None, None, f"the threshold of this state's {ty}s is not read"
        how = f"by the type the source's title states ({ty})"
    else:
        if not (states.get(st) or {}).get("complete"):
            return None, None, ("the source's title does not give the measure's type, and the rules read for this "
                                "state do not cover every kind of statewide question it puts to voters")
        # a convention question's title names the convention, so an untyped title is not one [inferred]
        pool = [r for r in pool if r["type"] != "convention"]
        how = ("the source's title does not give the type; every rule read for the state's measures (but its "
               "convention question) sets this threshold")
    general = [r for r in pool if not r.get("only_if")]
    special = [r for r in pool if r.get("only_if")]
    form = lambda r: (r.get("t"), r.get("compound"))
    if not general:
        return None, None, (f"the general threshold is not read; {special[0]['citation']} covers only "
                            f"{special[0]['only_if']}")
    if all(r.get("compound") or r.get("t") is None for r in general):
        return _one(general, how)
    if len({form(r) for r in general}) > 1:
        return None, None, ("the state's law sets different thresholds for different kinds of measure, and the "
                            "source's title does not show which kind this is")
    other = [r for r in special if form(r) != form(general[0])]
    if other:
        return None, None, (f"{other[0]['citation']} sets another threshold for {other[0]['only_if']}, and the "
                            f"source does not show whether this measure is one")
    return _one(general, how)


def _one(rs, how):
    r = rs[0]
    if r.get("compound") or r.get("t") is None:
        return None, None, (f"{r['citation']}: {r.get('compound') or r.get('rule')}: the threshold turns on more than "
                            f"the yes share of those voting on the question, and the model forecasts that share only")
    return r, how, None


def rows(contests, year, ref):
    """The like-past-measures rows of a year: each question's class and yes share. A question in a year whose
    source holds only part of the state is left out (its share is not the state's)."""
    out = []
    for c in contests:
        if not c["question"] or c.get("one_answer_only"):
            continue
        scope = scope_of(c, ref, year)
        if scope == "partial":
            continue
        yes, no = yes_no(c)
        if yes + no <= 0:
            continue
        out.append({"key": f"{scope} {kind_of(c)}", "s": yes / (yes + no), "n": yes + no,
                    "year": year, "state": c["state"]})
    return out


def density_at(train, key, t):
    """f(t) for one class from like past measures: the share of the class's measures whose yes share finished
    within h of t, over 2h, h widening 1, 2, 5 points as the like-race route's does. (f, measures, h, in window)."""
    s = [r_["s"] for r_ in train if r_["key"] == key]
    N = len(s)
    if N < L.MIN_CLASS:
        return None, N, None, None
    for h in L.WINDOWS:
        k = sum(1 for x in s if abs(x - t) <= h)
        if k >= L.MIN_IN_WINDOW or h == L.WINDOWS[-1]:
            return k / N / (2.0 * h), N, h, k


def p_block(f, t, n, under):
    yes, no = (1 - t) * f / n, t * f / n
    return {"value": max(yes, no), "value_of": "either ballot" if t == 0.5 else ("a No ballot" if t > 0.5 else
                                                                                 "a Yes ballot"),
            "yes": yes, "no": no, "event": f / n, "threshold": t, "f_t": f, "n": n, "under": under,
            "method": "density, threshold form (model section 7)"}


def yes_no(c):
    import local_medsl as LM
    return LM.yes_no(c)
