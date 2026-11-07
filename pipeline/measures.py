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
LOCAL_THRESHOLDS = os.path.join(L.REPO, "data", "measure", "thresholds-local.json")   # step (b)
BALLOT_TEXTS = os.path.join(L.REPO, "data", "measure", "ballot-texts.json")   # step (a): each held question's own words
STATEWIDE_COVER = 0.9   # a question filed with the state's offices is statewide when it carries at least this share
                        # of the most precincts any of the state's contests carries that year; and where the source
                        # names counties, the source holds the whole state when the year's contests carry at least
                        # this share of the most counties any year's do (MEDSL's 2016 file holds one South Dakota
                        # county; Alaska's files before 2024 name no county at all)

_RET_WORDS = re.compile(r"RETENTION|RETAIN")
_COURT = re.compile(r"\b(JUDGE|JUSTICE|COURT|MAGISTRATE)\b")
_RET_SUBJECT = re.compile(r"\bBE RETAINED\b")
# a tax, bond or fee proposition that names a court or justice system ('Parishwide Criminal Justice Proposition, 3.16
# Mills Renewal'; 'Florida Parishes Juvenile Justice Dist., 3 Mills Ext.': Louisiana 2023-2024) is a measure
_TAX_WORDS = re.compile(r"\b(MILLS?|MILLAGE|TAX|BONDS?|PARCEL FEE)\b")


def kind_of(c):
    """'retention' for a judge's yes-or-no question, else 'measure'. A title that reads as an amendment, a statute,
    a bond or a convention question is a measure even where it names a court ('STATEWIDE AMENDMENT NO. 2 -
    STATEWIDE BUSINESS COURT')."""
    office, subject = c["office"].upper(), (c.get("subject") or "").upper()
    if any(x["name"] in ("RETAIN", "NOT RETAIN", "DO NOT RETAIN") for x in c["candidates"]):
        return "retention"
    if type_of(c) in ("amendment", "statute", "bond", "convention"):
        return "measure"
    if _TAX_WORDS.search(office) and not _RET_WORDS.search(office):
        return "measure"
    if _RET_WORDS.search(office) or _COURT.search(office):
        return "retention"
    # a ballot text names the judge to be retained; "retain" alone in a text is often a school levy's purpose
    # ("the retention and attraction of teachers", "retaining ... teachers": Indiana's 2024 school levies) [measured]
    if _RET_SUBJECT.search(subject) or _COURT.search(subject):
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
        book = {"rules": [], "states": {}}
    else:
        with open(THRESHOLDS) as f:
            book = json.load(f)
    if os.path.exists(LOCAL_THRESHOLDS):   # local questions' rules, kept apart (scope "local")
        with open(LOCAL_THRESHOLDS) as f:
            loc = json.load(f)
        book["rules"] = book["rules"] + [dict(r, scope="local") for r in loc["rules"]]
        book["local_states"] = loc["states"]
    if os.path.exists(BALLOT_TEXTS):   # step (a): what each held statewide question's own ballot text shows
        with open(BALLOT_TEXTS) as f:
            book["ballot_texts"] = json.load(f)["questions"]
    return book


def _in_year(r, year):
    return (r.get("from_year") or 0) <= year <= (r.get("to_year") or 9999)


def rule_for(c, kind, book, year, rid=None):
    """(rule, how, None) or (None, None, the reason p is not computed) for a statewide measure or retention. `how`
    says how the rule was matched to the question: by the type its title states, or because every rule read for the
    state's measures sets the same threshold. Where the title leaves it open, the question's own ballot text, read in
    step (a) (`rid`, its record's id, in data/measure/ballot-texts.json), gives its type and whether a special rule's
    condition holds."""
    text = (book.get("ballot_texts") or {}).get(rid) if rid else None
    if text is None and c.get("filed_local"):   # the state's list of its statewide measures (local_medsl.join_statewide)
        q = c["filed_local"]["listed"]
        text = {"type": q.get("type"), "type_mark": q.get("type_mark"), "proposer": q.get("proposer"),
                "fact": q.get("fact"), "said_by": "the state's list of its statewide measures",
                "file": "data/measure/statewide-filed-local.json"}
    who = proposer_of(c, text)
    who = who if who[0] else None
    st = c["state"]
    states = book.get("states", {})
    mine = [r for r in book["rules"] if r["state"] == st and _in_year(r, year) and r.get("scope") != "local"]
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
    tty = (text or {}).get("type")
    if tty and tty != ty:   # the ballot text's own words give the type where the title does not, or says otherwise
        said = "states" if text.get("type_mark") == "stated" else f"shows [{text.get('type_mark')}]"
        how_t = (f"by the type {text.get('said_by', 'the ballot text')} {said} ({tty}; "
                 f"{text.get('file', 'data/measure/ballot-texts.json')})" +
                 (f", not the title's ({ty})" if ty is not None else ""))
        ty = tty
    else:
        how_t = None
    if ty == "advisory":
        return None, None, "an advisory question: the law read sets no threshold for it"
    pool = [r for r in mine if r["type"] != "retention"]
    if not pool:
        return None, None, f"the thresholds of this state's measures are not read for {year}"
    if ty is not None:
        pool = [r for r in pool if r["type"] == ty]
        if not pool:
            return None, None, f"the threshold of this state's {ty}s is not read"
        how = how_t or f"by the type the source's title states ({ty})"
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
    fact = (text or {}).get("fact") or {}
    if special and fact.get("applies") is not None:   # the ballot text settles whether the special rule's case holds
        pick = special if fact["applies"] else general
        if pick and len({form(r) for r in pick}) == 1 and len({r["only_if"] for r in special}) == 1:
            return _one(pick, f"{how}; {text.get('said_by', 'the ballot text')} shows it is "
                              f"{'' if fact['applies'] else 'not '}{special[0]['only_if']} [{fact['mark']}] "
                              f"({text.get('file', 'data/measure/ballot-texts.json')})", who)
    unshown = ("; its ballot text, read in step (a), does not show it either (data/measure/ballot-texts.json)"
               if text and not text.get("said_by") else "")
    if not general:
        return None, None, (f"the general threshold is not read; {special[0]['citation']} covers only "
                            f"{special[0]['only_if']}" + (unshown if special and fact.get("applies") is None else ""))
    if all(r.get("compound") or r.get("t") is None for r in general):
        return _one(general, how, who)
    if len({form(r) for r in general}) > 1:
        return None, None, ("the state's law sets different thresholds for different kinds of measure, and the "
                            "source's title does not show which kind this is")
    other = [r for r in special if form(r) != form(general[0])]
    if other:
        return None, None, (f"{other[0]['citation']} sets another threshold for {other[0]['only_if']}, and the "
                            f"source does not show whether this measure is one" + unshown)
    return _one(general, how, who)


def local_rule_for(c, book, year):
    """(rule, how, None) or (None, None, the reason p is not computed) for a local question whose place the source
    shows (step (b): the orchestrator, 2026-11-07 06:16, "local thresholds read from the governing state law or p not
    computed (never inferred 1/2)"). A local rule names the kind of question it governs and how to know one by its
    title or ballot words (`match`, a pattern on them, with `match_also` and `dates` where set); the question takes
    the first rule in the file's order its words match (the rules for one place's own act come before the general
    law's), and none where they match none. A rule that `hold`s p back says why: the source does not show which law
    governs the question, or the law read leaves its threshold open."""
    st = c["state"]
    mine = [r for r in book["rules"] if r["state"] == st and r.get("scope") == "local" and _in_year(r, year)]
    if not mine:
        why = ((book.get("local_states") or {}).get(st) or {}).get("not_read")
        return None, None, ("the thresholds of this state's local questions are not read" + (f": {why}" if why else
                                                                                               ""))
    words = " ".join((c["office"] + " " + (c.get("subject") or "")).upper().split())
    for r in mine:
        if (re.search(r["match"], words) and (not r.get("match_also") or re.search(r["match_also"], words))
                and (not r.get("dates") or (c.get("date") or "") in r["dates"])):
            break
    else:
        return None, None, ("the source's words do not show which kind of local question this is among the kinds "
                            "whose law was read")
    if r.get("hold"):
        return None, None, f"{r['kind']}: {r['hold']}"
    if r.get("advisory"):
        return None, None, f"an advisory question: the law read sets no threshold for it ({r['citation']})"
    return _one([r], f"by the kind the source's words show ({r['kind']})"
                + (f"; {r['match_note']}" if r.get("match_note") else ""))


# who put a question on the ballot, as its title says it [stated: the title's words]; read only to cite the rule that
# governs its kind where several rules set the same share (the orchestrator, 2026-11-07 14:36: "Cite the rule that
# governs each question by its kind, not the first general rule in the file that sets the same share")
_PROPOSER_WORDS = (("initiative", r"INITIATIVE PETITION|PROPOSED BY INITIATIVE|CONSTITUTIONAL INITIATIVE|\bCI-\d|"
                                  r"\bINITIATIVE (MEASURE )?(NO\.? ?)?\d|LEGISLATIVE INITIATIVE|\bINITIATED\b"),
                   ("legislature", r"LEGISLATIVE REFERENDUM|\bLR-?\d|REFERRED BY THE (LEGISLATURE|LEGISLATIVE ASSEMBLY|"
                                   r"GENERAL ASSEMBLY)|\b[HS]JR ?\d|\(ACT (NO\. )?\d+[^)]*\b[HS]B ?\d+"))


def proposer_of(c, text=None):
    """(who, how) for the question: from its ballot text where read (step (a)), else from its title's words; (None,
    None) where neither shows it."""
    pr = (text or {}).get("proposer")
    if pr:
        return pr["who"], (f"[{pr['mark']}: {text.get('said_by', 'the ballot text read')}, "
                           f"{text.get('file', 'data/measure/ballot-texts.json')}]")
    t = " ".join((c["office"] + " " + (c.get("subject") or "")).upper().split())
    hits = {who for who, pat in _PROPOSER_WORDS if re.search(pat, t)}
    return (hits.pop(), "[stated: the title's words]") if len(hits) == 1 else (None, None)


def _one(rs, how, who=None):
    """The rule of `rs` (all setting the same threshold) that governs the question: where they are several, the one
    for its proposer (`proposer` on the rule; a rule without it governs any proposer), and where the source does not
    show which governs, every one that could, cited together."""
    seen, cands = set(), []
    for r in rs:
        if r["citation"] not in seen:
            seen.add(r["citation"]); cands.append(r)
    # one law read two ways is one rule: a citation whose parts all lie in another's ('Wyo. Const. art. 20, §1' in
    # 'Wyo. Stat. 22-2-117(d); Wyo. Const. art. 20, §1') is that one, not a second rule that could govern
    parts = [set(x["citation"].split("; ")) for x in cands]
    cands = [x for i, x in enumerate(cands)
             if not any(j != i and parts[i] < parts[j] for j in range(len(cands)))]
    whom, narrowed = (who[0] if who else None), False
    if whom and len(cands) > 1:
        fit = [r for r in cands if whom in (r.get("proposer") or [])]
        if fit:
            narrowed = len(cands)
            cands = fit + [r for r in cands if not r.get("proposer")]
            narrowed = len(cands) < narrowed
    r = cands[0]
    cite = r["citation"] if len(cands) == 1 else ", or ".join(x["citation"] for x in cands)
    if r.get("compound") or r.get("t") is None:
        return None, None, (f"{cite}" + (" (the source does not show which of these governs it)" if len(cands) > 1
                                         else "") + f": {r.get('compound') or r.get('rule')}: the threshold turns on more than "
                            f"the yes share of those voting on the question, and the model forecasts that share only")
    if narrowed and len(cands) == 1:
        how += f"; proposed by the {whom} {who[1]}, so {r['citation']} governs ({r['applies_to']})"
    elif len(cands) > 1:
        how += ("; the source does not show which of these governs it (" + "; ".join(
            f"{x['citation']}: {x['applies_to']}" for x in cands) + "), and each sets this share")
        r = dict(r, citation=cite, also_governs=[{k: x.get(k) for k in ("citation", "applies_to", "url", "quote",
                                                                          "read_utc") if x.get(k) is not None}
                                                 for x in cands[1:]])
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
                    "year": year, "state": c["state"],
                    # counted whole: a state's own file that shows the question's place (not MEDSL's by county),
                    # or one county's question whose place lies wholly in it (local_medsl.one_place)
                    "whole": c.get("source", "medsl") != "medsl" or bool(c.get("one_place"))})
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
