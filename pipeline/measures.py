"""pipeline/measures.py: ballot measures and retentions from MEDSL's precinct returns, with p where the law and the
like-past-measures route allow it.

Written 2026-11-07 by worker D3 (briefs/D3-data-local.md, step 4), for pipeline/local_medsl.py's build.

The orchestrator's ruling of 2026-11-07 06:16: "Measures: approved, except local thresholds are never inferred.
Read statewide thresholds from each constitution or statute, with URLs ... Where it cannot be read, p is not
computed, with that reason ... The like-past-measures route is approved, marked as the model's own ... Refit with
2016 added, report the calibration again, and say in REPORT.md if it still under-forecasts near 1/2."

  threshold   data/measure/thresholds.json: each state's rule, read from its constitution or statute, with the
              URL, the words and the time read. A measure gets the rule for its type (an amendment, a statute, a
              bond, a convention question, a retention), the type read from the source's title; where the state's
              rules for the possible types agree, the type is not needed. A rule that turns on more than the yes
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
STATEWIDE_COVER = 0.9   # a question filed with the state's offices is statewide when its votes come from at least this
                        # share of the state's counties (the counties any of the state's contests carry in the year)

_RET = re.compile(r"RETENTION|RETAIN|\b(JUDGE|JUSTICE|COURT|MAGISTRATE)\b")


def kind_of(c):
    """'retention' for a judge's yes-or-no question, else 'measure'."""
    text = (c["office"] + " " + (c.get("subject") or "")).upper()
    if _RET.search(text) or any(x["name"] in ("RETAIN", "NOT RETAIN", "DO NOT RETAIN") for x in c["candidates"]):
        return "retention"
    return "measure"


def county_counts(contests_by_year):
    """{state: the most counties any one year's contests in the state carry}: the reference for STATEWIDE_COVER
    (a year's file can hold only some counties, as MEDSL's 2016 file does for South Dakota)."""
    out = collections.Counter()
    for year, cs in contests_by_year.items():
        by = collections.defaultdict(set)
        for c in cs:
            by[c["state"]].update(c["counties"])
        for st, s in by.items():
            out[st] = max(out[st], len(s))
    return out


def scope_of(c, ncounties):
    if c["dataverse"] == "STATE" and ncounties.get(c["state"]) and \
            len(c["counties"]) >= STATEWIDE_COVER * ncounties[c["state"]]:
        return "statewide"
    return "local"


_TYPES = [
    ("convention", r"\bCONVENTION\b"),
    ("bond", r"\bBONDS?\b|\$[0-9]"),
    ("amendment", r"CONSTITUTION|\bAMEND|\bCON\.? AMEND|^CA NO\b|\bCI-\d|\bHJR\b|\bSJR\b|JOINT RESOLUTION"),
    ("statute", r"\bINITIATIVE\b|\bINITIATED\b|\(STATUTORY\)|REFERRED LAW|REFERENDUM|\bAN ACT\b|\bI-\d"),
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
        return {"rules": []}
    with open(THRESHOLDS) as f:
        return json.load(f)


def rule_for(c, kind, rules, year):
    """(rule, None) or (None, the reason p is not computed) for a statewide measure or retention."""
    st = c["state"]
    mine = [r for r in rules if r["state"] == st and (r.get("from_year") or 0) <= year <= (r.get("to_year") or 9999)]
    if not mine:
        return None, f"the threshold for this state's {kind}s is not yet read from its constitution or statute"
    if kind == "retention":
        rs = [r for r in mine if r["type"] == "retention"]
        if not rs:
            return None, "the threshold for this state's judicial retentions is not yet read from its constitution"
        return _one(rs)
    ty = type_of(c)
    cand = [r for r in mine if r["type"] != "retention" and not r.get("only_if")]
    if ty is not None:
        exact = [r for r in mine if r["type"] == ty]
        if exact:
            special = [r for r in exact if r.get("only_if")]
            if special:
                return None, (f"{special[0]['citation']} sets another threshold for {special[0]['only_if']}, and the "
                              f"source's title does not show whether this {ty} is one")
            return _one([r for r in exact if not r.get("only_if")])
    # the title does not settle the type, or the state has no rule of that name: the rules must all agree
    if cand and len({(r.get("t"), r.get("compound")) for r in cand}) == 1 and \
            not any(r.get("only_if") for r in mine if r["type"] != "retention"):
        return _one(cand[:1])
    return None, ("the state's constitution sets different thresholds for different kinds of measure, and the "
                  "source's title does not show which kind this is")


def _one(rs):
    r = rs[0]
    if r.get("compound") or r.get("t") is None:
        return None, (f"{r['citation']}: {r.get('compound') or r.get('rule')}: the threshold turns on more than the yes "
                      f"share of those voting on the question, and the model forecasts that share only")
    return r, None


def rows(contests, year, ncounties):
    out = []
    for c in contests:
        if not c["question"] or c.get("one_answer_only"):
            continue
        yes, no = yes_no(c)
        if yes + no <= 0:
            continue
        out.append({"key": f"{scope_of(c, ncounties)} {kind_of(c)}", "s": yes / (yes + no), "n": yes + no,
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
