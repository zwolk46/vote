"""pipeline/local.py: state legislatures, local races, primaries and ballot measures, from the intake caches to data/.

Written 2026-11-07 by worker D3 (briefs/D3-data-local.md, steps 3 to 6). It reads the normalized caches the intake
scripts in pipeline/intake/ write, builds the model's own forecast for each contest (no forecaster published one
for any race at these levels: model section 4), computes p with pipeline/core.py's p_contest (never a second
version of it), and writes one compact file per level, year and state:

  data/state-upper/<year>/<ST>.json   state senates (and Nebraska's one chamber)
  data/state-lower/<year>/<ST>.json   state houses and assemblies
  data/primary/<year>/<ST>.json       primaries, with the office they nominate for
  data/local/<year>/<ST>.json, data/measure/<year>/<ST>.json   (from the precinct sources, as they are taken in)

Each file is {level, year, state, about, sources: {key: source block}, model: {...}, contests: [...]}, one contest
per line, in the layout of plan/PLAN.md section 3; the fields added are in data/README.md ("Fields added by D3").

THE MODEL'S OWN FORECAST, method D3-v1.1: D3-v1 as proposed to the orchestrator with its back-test (brief step 3),
approved 05:06 with one change, that each year is fitted on earlier years only, and with runoffs added at its word.
Routes by what is known before the election:

  (a) "partisan": a single-seat general election whose two leading candidates are a Democrat and a Republican.
      The Democrat's share of the two-party vote is
          y = 1/2 + a_t + b . x + g_(state, chamber, t) + e
      with x, all known before the election, in one of three classes:
          A  the seat's last result was contested: (its Democratic share - 1/2), incumbency, the chamber's lean
          B  the seat's last result was uncontested: which party won it unopposed, incumbency, the chamber's lean
          C  no last result on these lines (redistricted, or new): incumbency, the chamber's lean
      incumbency = +1 for a Democratic incumbent running, -1 for a Republican one, 0 for an open seat (Klarner's
      "inc"); the chamber's lean = the mean Democratic share of the contested single-seat races in the same
      state and chamber at its previous election, minus 1/2. a_t, the year's swing, is forecast from whether t is
      a presidential year, a midterm or an odd year, and the sitting president's party (National Archives), as
      D2-v1 does for Congress. g is the state-and-chamber's own swing that year, e the race's own error; the
      forecast is normal with sd = sqrt(s_a^2 + s_g^2 + s_e^2), s_e by class and size, and a Student-t with 4
      degrees of freedom on the same sd beside it. Each year is forecast from a fit on earlier years only (the
      orchestrator, 05:06: "a coefficient fitted partly on later years is something no voter knew"), and only
      when the fit has at least MIN_EARLIER earlier years of the same kind, the fewest the back-test supports.
      This is Gelman & King's and Gelman, King & Boscardin's route (the last result and incumbency).
  (b) "class": every other contest the model can count: primaries, nonpartisan races, a major party against a
      minor one. The forecast is the spread of like past races' results (Mulligan & Hunter's route, model
      section 3), read through the model's own lay form: q, the share of the class's races in earlier years whose
      two leading candidates finished between 49% and 51% of their combined vote, gives f(1/2) = 50 q and p =
      25 q / n (model section 3, "the form a person can say aloud"). The same f(1/2) for every race of the
      class; p through pipeline/core.py with a normal of that height at 1/2. The class is named in each forecast.
  (c) "boundary": a race that fills several seats at once ("vote for k"): route (b) applied to the two
      candidates either side of the boundary between the last winner and the first loser (model section 7), for a
      ballot that marks one of them and not the other. Marked the model's own and not yet checked; M2 checks it.

  (d) "runoff": the second round of a runoff (party primaries in runoff states, Louisiana's second round,
      Georgia's general runoffs) is its own two-way race (the orchestrator, 05:06): route (b) on like past
      runoffs, classed by kind and by how far ahead the first round's leader of the two finished, known before
      the second round. Marked.

Not computed, with the reason recorded (model section 7): first rounds of two-round systems (a vote there works
through who advances), top-two primaries (a boundary between second and third), special elections (the
forecasts are fitted to regular elections), contests whose votes are not reported, and years or classes with too
few earlier races to fit on. A race with one name on the ballot has p = 0, said so; write-in votes against it are
recorded.

Run:
  VOTE_CACHE=/tmp/vote-cache python3 pipeline/local.py backtest          writes data/local/backtest.json
  VOTE_CACHE=/tmp/vote-cache python3 pipeline/local.py build [--out DIR] [--with-p] [--sample]
"""
import argparse
import collections
import datetime
import json
import math
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import core  # noqa: E402  (p_contest: the one implementation of the model's formula)
import fetch as F  # noqa: E402

METHOD = "D3-v1.1"
KLARNER = os.path.join(F.CACHE, "klarner", "normalized")
NARA = os.path.join(F.CACHE, "nara", "normalized", "electoral_college.json")
BINS = (0, 3000, 10000, 30000, float("inf"))     # two-party votes: the race's own error is fitted by size
SMALL_COUNT = {"general": 0.05, "primary": 0.02}   # a count this far under its chamber's median is held back
MIN_CLASS = 100          # route (b) needs at least this many like races in earlier years
MIN_EARLIER = 3          # route (a): earlier years of the same kind (presidential, midterm, odd) a fit needs, read off the back-test
MIN_IN_WINDOW = 10       # and at least this many of them in the window, or the window widens
WINDOWS = (0.01, 0.02, 0.05)
STATE_NAMES = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California", "CO": "Colorado",
    "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
    "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana",
    "ME": "Maine", "MD": "Maryland", "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota",
    "MS": "Mississippi", "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
    "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York", "NC": "North Carolina",
    "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania",
    "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas",
    "UT": "Utah", "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
    "WI": "Wisconsin", "WY": "Wyoming", "DC": "District of Columbia"}
PARTY = {"d": "D", "r": "R", "nm": "other", "np": "nonpartisan", "w": "write-in", "m": None, "b": "D and R"}
# Klarner's numeric party codes (codebook_candidate.docx, "Appendix C: Party Codes"), for candidates outside the two
# parties whose party line is a code, not a name: (the party in words, the codebook's own words).
_MINOR = "minor party or independent, party not named"
KLARNER_CODES = {
    "4001": ("unknown", "no party identified in the data"),
    "4005": (_MINOR, "some type of non-major party candidate: not listed in either the Democratic or Republican primary"),
    "4006": (_MINOR, "combination of 4005 and 99997"),
    "4007": ("no party", "returns explicitly say that the candidate isn't affiliated with a party"),
    "4008": (_MINOR, "assumed non-major party because no party was listed next to the name in the returns, where "
                     "parties were generally listed"),
    "4009": (_MINOR, "assumed non-major party: not listed among candidates filing for the Democratic and Republican "
                     "primaries"),
    "4010": (_MINOR, "assumed non-major party because the candidate wasn't listed in the returns"),
    "4011": (_MINOR, "coded 908 in the earlier SLERs, which could indicate a non-partisan election, but in a state "
                     "and year with partisan elections; judged non-major party"),
    "5000": (_MINOR, "non-major party candidate of some type"),
    "99993": (_MINOR, "known to be non-major party from returns, but party not specified"),
    "99994": (_MINOR, "combination of codes 99995 and 99997"),
    "99995": (_MINOR, "assumed non-major party: a party code with no value in the ICPSR codebook, which other "
                      "candidates with the same code were found to be"),
    "99997": (_MINOR, "assumed non-major party because the election is fully contested and no party was given in "
                      "the prior database"),
    "99998": (_MINOR, "non-major party candidate, but party not specified"),
}


# ------------------------------------------------------------------ inputs

def load_klarner():
    with open(os.path.join(KLARNER, "contests.jsonl")) as f:
        return [json.loads(line) for line in f]


def klarner_info():
    with open(os.path.join(KLARNER, "info.json")) as f:
        return json.load(f)


def president_party():
    """{election year t: +1 if the sitting president on Election Day in t is a Democrat, -1 if a Republican}, from
    the National Archives' Electoral College results (pipeline/intake/nara_electoral_college.py): the president
    in office in November of year t was elected in the last presidential election before t (Kennedy and Johnson,
    Nixon and Ford, share a party, so a death or resignation does not change it)."""
    with open(NARA) as f:
        rows = json.load(f)
    won = {r["year"]: (1 if r["party"] == "D" else -1) for r in rows}
    out = {}
    for t in range(min(won) + 1, max(won) + 5):
        e = 4 * ((t - 1) // 4)
        if e in won:
            out[t] = won[e]
    return out, rows


def cycle(t):
    return "presidential" if t % 4 == 0 else "midterm" if t % 4 == 2 else "odd"


def two_leading(cands):
    named = [a for a in cands if not a["scattering"] and a["party"] != "w"]
    named.sort(key=lambda a: -(a["votes"] or 0))
    return named


def top_named(cands):
    """Every named candidate, write-ins included (not the source's 'scattering'), by votes: the pairs that decide."""
    named = [a for a in cands if not a["scattering"]]
    named.sort(key=lambda a: -(a["votes"] or 0))
    return named


WRITE_IN_STRONG = 0.10   # a write-in with at least this share of the last winner's votes makes an unopposed race a contest


def size_bin(n):
    for i in range(len(BINS) - 1):
        if n < BINS[i + 1]:
            return i
    return len(BINS) - 2


# ------------------------------------------------------------------ route (a): partisan

def partisan_rows(contests):
    """One row per single-seat general-type contest with one Democrat and one Republican on the ballot, with votes.
    Who is on the ballot is known before the election; who finishes in the first two is not (law 2a)."""
    rows = []
    for c in contests:
        kv = c.get("klarner")
        if not kv or c["etype"] not in ("g", "gs", "ssg") or c["eseats"] != 1:
            continue
        if any(a["vote_missing"] for a in c["cands"] if not a["scattering"]):
            continue
        lead = two_leading(c["cands"])
        ds = [a for a in lead if a["party"] == "d"]
        rs = [a for a in lead if a["party"] == "r"]
        if len(ds) != 1 or len(rs) != 1:
            continue
        d, r = ds[0]["votes"], rs[0]["votes"]
        if d <= 0 or r <= 0:
            continue
        lag, ul = kv.get("dperlag"), kv.get("uncontlag")
        if lag is None:
            cls, xl, ulag = "C", 0.0, 0
        elif ul == 1:
            cls, xl, ulag = "B", 0.0, (1 if lag > 50 else -1)
        else:
            cls, xl, ulag = "A", lag / 100.0 - 0.5, 0
        rows.append({"c": c, "year": c["year"], "state": c["state"], "sen": c["sen"], "y": d / (d + r),
                     "N": d + r, "cls": cls, "xl": xl, "ulag": ulag, "inc": kv.get("inc") or 0})
    # the chamber's lean: mean D share of the same state and chamber's contested seats at its previous election
    by = collections.defaultdict(list)
    for r_ in rows:
        by[(r_["state"], r_["sen"], r_["year"])].append(r_["y"])
    years = collections.defaultdict(list)
    for (s, sen, t) in by:
        years[(s, sen)].append(t)
    prev = {}
    for k, ts in years.items():
        ts.sort()
        for a, b in zip(ts, ts[1:]):
            prev[(k[0], k[1], b)] = (float(np.mean(by[(k[0], k[1], a)])) - 0.5, a)
    for r_ in rows:
        L = prev.get((r_["state"], r_["sen"], r_["year"]))
        r_["L"], r_["L_year"], r_["Lmiss"] = (L[0], L[1], 0) if L else (0.0, None, 1)
    return rows


COLS = ["B", "C", "A_last", "A_inc", "A_lean", "B_unopposed", "B_inc", "B_lean", "C_inc", "C_lean", "lean_missing"]


def _x(r_, j, X, i):
    c = r_["cls"]
    if c == "A":
        X[i, j["A_last"]], X[i, j["A_inc"]], X[i, j["A_lean"]] = r_["xl"], r_["inc"], r_["L"]
    elif c == "B":
        X[i, j["B"]], X[i, j["B_unopposed"]], X[i, j["B_inc"]], X[i, j["B_lean"]] = 1, r_["ulag"], r_["inc"], r_["L"]
    else:
        X[i, j["C"]], X[i, j["C_inc"]], X[i, j["C_lean"]] = 1, r_["inc"], r_["L"]
    X[i, j["lean_missing"]] = r_["Lmiss"]


def fit_partisan(rows, pres):
    ys = sorted({r_["year"] for r_ in rows})
    yi = {t: i for i, t in enumerate(ys)}
    k = len(ys)
    j = {c: k + i for i, c in enumerate(COLS)}
    X = np.zeros((len(rows), k + len(COLS)))
    for i, r_ in enumerate(rows):
        X[i, yi[r_["year"]]] = 1
        _x(r_, j, X, i)
    y = np.array([r_["y"] - 0.5 for r_ in rows])
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ b
    coef = {c: float(b[j[c]]) for c in COLS}
    year_effect = {t: float(b[yi[t]]) for t in ys}
    swing, resid, df, n_kind = {}, [], 0, {}
    for cy in ("presidential", "midterm", "odd"):
        ts = [t for t in ys if cycle(t) == cy and t in pres]
        n_kind[cy] = len(ts)
        if not ts:
            continue
        v = np.array([year_effect[t] for t in ts])
        if len(ts) >= 2 and len({pres[t] for t in ts}) > 1:
            A, npar = np.array([[1.0, pres[t]] for t in ts]), 2
        else:   # one party in the White House in every earlier year of this kind: the mean swing only
            A, npar = np.ones((len(ts), 1)), 1
        s, *_ = np.linalg.lstsq(A, v, rcond=None)
        swing[cy] = [float(s[0]), float(s[1]) if npar == 2 else 0.0]
        resid += list(v - A @ s)
        df += len(ts) - npar
    s_a = math.sqrt(sum(e * e for e in resid) / df) if df > 0 else None
    groups = collections.defaultdict(list)
    for i, r_ in enumerate(rows):
        groups[(r_["state"], r_["sen"], r_["year"])].append(i)
    within = [float(res[ix].var(ddof=1)) for ix in groups.values() if len(ix) > 1]
    se2 = float(np.mean(within))
    gm = np.array([res[ix].mean() for ix in groups.values()])
    gn = np.array([len(ix) for ix in groups.values()])
    s_g = math.sqrt(max(float(np.mean(gm ** 2 - se2 / gn)), 0.0))
    w = collections.defaultdict(list)
    for ix in groups.values():
        if len(ix) < 2:
            continue
        mu, f = res[ix].mean(), len(ix) / (len(ix) - 1)
        for i in ix:
            w[(rows[i]["cls"], size_bin(rows[i]["N"]))].append((res[i] - mu) ** 2 * f)
    s_e = {f"{c}{b_}": math.sqrt(float(np.mean(v))) for (c, b_), v in w.items()}
    return {"years_fitted": ys, "races_fitted": len(rows), "coef": coef, "swing": swing, "s_a": s_a, "s_g": s_g,
            "s_e": s_e, "year_effect": year_effect, "earlier_years_of_kind": n_kind}


def fit_before(rows, pres, t):
    """The fit for year t, on earlier years only (the orchestrator, 05:06: a coefficient fitted partly on later
    years is something no voter knew). Returns (fit or None, earlier years of t's kind)."""
    train = [r_ for r_ in rows if r_["year"] < t]
    if not train:
        return None, 0
    M = fit_partisan(train, pres)
    k = M["earlier_years_of_kind"].get(cycle(t), 0)
    if M["s_a"] is None or cycle(t) not in M["swing"]:
        return None, k
    return M, k


def predict_partisan(M, r_, pres):
    c, t = M["coef"], r_["year"]
    sw = M["swing"][cycle(t)]
    a = sw[0] + sw[1] * pres[t]
    m = 0.5 + a + c["lean_missing"] * r_["Lmiss"]
    if r_["cls"] == "A":
        m += c["A_last"] * r_["xl"] + c["A_inc"] * r_["inc"] + c["A_lean"] * r_["L"]
    elif r_["cls"] == "B":
        m += c["B"] + c["B_unopposed"] * r_["ulag"] + c["B_inc"] * r_["inc"] + c["B_lean"] * r_["L"]
    else:
        m += c["C"] + c["C_inc"] * r_["inc"] + c["C_lean"] * r_["L"]
    se = M["s_e"].get(f"{r_['cls']}{size_bin(r_['N'])}") or max(M["s_e"].values())
    sd = math.sqrt(M["s_a"] ** 2 + M["s_g"] ** 2 + se ** 2)
    return min(max(m, 0.001), 0.999), sd, a


# ------------------------------------------------------------------ route (b) and (c): like past races

def class_key_primary(c, lead):
    k = min(len(lead), 4)
    inc = any(a.get("exper") == "inc" for a in lead)
    return f"primary, {k if k < 4 else '4+'} candidates, {'an incumbent running' if inc else 'open seat'}"


# a runoff's second round and the first rounds it can follow (Klarner's election types)
RUNOFF_FIRST = {"dprunoff": ("dpfunsettled", "dpfpartunsettled"), "rprunoff": ("rpfunsettled",),
                "larunoff": ("lafunsettled",), "grunoff": ("gfunsettled", "gfpartunsettled")}
RUNOFF_KIND = {"dprunoff": "after a party primary", "rprunoff": "after a party primary",
               "larunoff": "after an open or general first round", "grunoff": "after an open or general first round"}


def _seat(c):
    return (c["year"], c["state"], c["sen"], c["dname"], c["dno"], c["geopost"], c["mmdpost"])


def first_round_index(contests):
    idx = collections.defaultdict(list)
    for c in contests:
        if any(c["etype"] in v for v in RUNOFF_FIRST.values()):
            idx[_seat(c)].append(c)
    return idx


def runoff_key(c, idx):
    """The class of a runoff's second round, from what was known before it: its kind, and how far ahead the
    first round's leader of the two finished in the first round (their share of the two's first-round votes)."""
    named = two_leading(c["cands"])[:2]
    fr = [x for x in idx.get(_seat(c), []) if x["etype"] in RUNOFF_FIRST[c["etype"]]]
    kind = RUNOFF_KIND[c["etype"]]
    if fr:
        v = {a["candid"]: a["votes"] for a in fr[0]["cands"] if not a["scattering"]}
        got = [v.get(a["candid"]) for a in named]
        if all(g is not None for g in got) and sum(got) > 0:
            s = max(got) / sum(got)
            return (f"runoff {kind}, first-round leader of the two within 10 points" if s < 0.55 else
                    f"runoff {kind}, first-round leader of the two ahead by 10 points or more")
    return f"runoff {kind}, first round not found in the source"


def class_rows(contests):
    """Rows for route (b): plurality contests decided by their own count that route (a) does not cover, and the
    second rounds of runoffs, each a two-way race (the orchestrator, 05:06)."""
    rows = []
    idx = first_round_index(contests)
    for c in contests:
        lead = two_leading(c["cands"])
        if len(lead) < 2 or any(a["vote_missing"] for a in c["cands"] if not a["scattering"]):
            continue
        kind = structure(c)
        if kind[0] not in ("class", "boundary", "runoff"):
            continue
        if kind[0] == "runoff":
            kind = ("runoff", runoff_key(c, idx))
        if kind[0] == "boundary":
            k = c["eseats"]
            if len(lead) <= k:
                continue
            x1, x2 = lead[k - 1]["votes"], lead[k]["votes"]
        else:
            x1, x2 = lead[0]["votes"], lead[1]["votes"]
        if x1 + x2 <= 0:
            continue
        rows.append({"c": c, "year": c["year"], "key": kind[1], "s": max(x1, x2) / (x1 + x2), "n": x1 + x2})
    return rows


def class_density(train_rows, key):
    """f(1/2) for one class from like past races, through the model's own lay form (model section 3): q, the share of
    the class's races whose two leading candidates finished between 49% and 51% of their combined vote, gives
    f(1/2) = 50 q, so p = f(1/2) / (2n) = 25 q / n. Where fewer than MIN_IN_WINDOW races of the class fall in that
    window, it widens to 48-52% (f = 25 q') and then 45-55% (f = 10 q''), and says so. Returns (f, races in the
    class, the window's half-width, races in the window)."""
    s = [r_["s"] for r_ in train_rows if r_["key"] == key]
    N = len(s)
    if N < MIN_CLASS:
        return None, N, None, None
    for h in WINDOWS:
        k = sum(1 for x in s if x <= 0.5 + h)
        if k >= MIN_IN_WINDOW or h == WINDOWS[-1]:
            return k / N / (2.0 * h), N, h, k


# ------------------------------------------------------------------ the structure of each contest

PRIMARY_PLURALITY = ("dp", "rp", "indepp", "workp", "conservativep", "liberp", "greenp", "constp", "amerp",
                     "indepamerp", "progp", "dpdoesnotcount", "rpdoesnotcount")


def structure(c):
    """(route, class key or reason) for a normalized Klarner contest."""
    et = c["etype"]
    kv = c.get("klarner") or {}
    named = two_leading(c["cands"])
    if any(a["vote_missing"] for a in c["cands"] if not a["scattering"]) and len(named) > 1:
        return ("not computed", "the source does not report every candidate's votes")
    if len(named) <= (c["eseats"] or 1):
        return ("zero", "one name on the ballot for each seat (unopposed): p is 0; write-in votes against it are "
                        "recorded" if any(a["party"] == "w" or a["scattering"] for a in c["cands"]) else
                        "one name on the ballot for each seat (unopposed): p is 0")
    if et in RUNOFF_FIRST:
        if (c["eseats"] or 1) > 1:
            return ("not computed", f"a runoff for several seats at once: not computed in {METHOD}")
        return ("runoff", "the second round of a runoff, its own two-way race")
    if et.startswith("la") or "runoff" in et or "funset" in et or "fsettled" in et or "fpartunset" in et \
            or et in ("gfunsettled",):
        if "runoff" in et:
            return ("not computed", "a runoff in a special election: the model's own forecasts are fitted to "
                                    "regular elections")
        return ("not computed", "the first round of a two-round system: a vote there works through who advances "
                                "(model section 7); recorded, p not computed")
    if et == "ttp":
        return ("not computed", "a top-two primary: the first two advance, so it is decided at the boundary "
                                f"between second and third; not computed in {METHOD}")
    if et in PRIMARY_PLURALITY or (et.endswith("p") and not et.startswith("s")):
        if (c["eseats"] or 1) > 1:
            return ("not computed", f"a primary that nominates several candidates at once: not computed in {METHOD}")
        return ("class", class_key_primary(c, named))
    if et in ("g", "gs", "ssg"):
        k = c["eseats"] or 1
        nd = sum(1 for a in named if a["party"] == "d")
        nr = sum(1 for a in named if a["party"] == "r")
        if k > 1:
            slate = ("both major parties running a full slate" if nd >= k and nr >= k else
                     "both major parties running, one short of a full slate" if nd and nr else
                     "one major party or none against the others")
            return ("boundary", f"general, {k if k < 4 else '4+'} seats at once, {slate}")
        if nd == 1 and nr == 1:
            return ("partisan", None)
        if nd + nr == 0:
            if all(a["party"] == "np" for a in named):
                return ("class", "general, nonpartisan")
            return ("class", "general, no Democrat or Republican on the ballot")
        if nd + nr == 1:
            return ("class", "general, one major party against minor parties or independents")
        return ("class", "general, two candidates of one major party")
    if et.startswith("s") or et.startswith("nps") or et == "appointed":
        return ("not computed", "a special election: the model's own forecasts are fitted to regular elections")
    return ("not computed", f"election type {et!r} not handled by {METHOD}")


# ------------------------------------------------------------------ normal and t4, numpy only

def _ncdf(x, m, s):
    return 0.5 * (1.0 + math.erf((x - m) / (s * math.sqrt(2.0))))


def _npdf(x, m, s):
    return math.exp(-0.5 * ((x - m) / s) ** 2) / (s * math.sqrt(2.0 * math.pi))


def _t4_logpdf(x, m, sd):
    s = sd / math.sqrt(2.0)
    z = (x - m) / s
    return math.log(0.375 / s) - 2.5 * math.log1p(z * z / 4.0)


Z = {"50": 0.6744897501960817, "80": 1.2815515655446004, "95": 1.959963984540054}


def _tally(e, y, N, m, sd):
    """One held-out race into the back-test tallies. sd here already includes the count's own noise."""
    z = (y - m) / sd
    for q, zz in Z.items():
        e[f"in_{q}"] += abs(z) <= zz
    e["races"] += 1
    f = _npdf(0.5, m, sd)
    e["expected_49_51"] += _ncdf(0.51, m, sd) - _ncdf(0.49, m, sd)
    e["seen_49_51"] += 0.49 <= y <= 0.51
    margin = abs(2 * round(y * N) - N)
    for kv in (100, 10):
        h = kv / (2.0 * N)
        e[f"expected_within_{kv}_votes"] += _ncdf(0.5 + h, m, sd) - _ncdf(0.5 - h, m, sd)
        e[f"seen_within_{kv}_votes"] += margin <= kv
    # a margin of 0 or 1 among N two-party votes, parity unknown before the election: 1.5 f(1/2) / N (MATH 8.2)
    e["expected_margin_0_or_1"] += 1.5 * f / N
    e["seen_margin_0_or_1"] += margin <= 1
    e["log_score_normal"] += -0.5 * z * z - math.log(sd * math.sqrt(2 * math.pi))
    e["log_score_t4"] += _t4_logpdf(y, m, sd)


def _finish(e):
    n = e["races"] or 1
    out = dict(e)
    for q in Z:
        out[f"in_{q}"] = round(e[f"in_{q}"] / n, 4)
    for k in ("log_score_normal", "log_score_t4"):
        out[k] = round(e[k] / n, 4)
    for k in list(out):
        if k.startswith("expected"):
            out[k] = round(out[k], 2)
    return out


# ------------------------------------------------------------------ back-test

def _class_tally(e, f, r_):
    n = r_["n"]
    margin = round((2 * r_["s"] - 1) * n)
    e["races"] += 1
    e["expected_49_51"] += min(1.0, f * 0.02)
    e["seen_49_51"] += r_["s"] <= 0.51
    e["expected_within_10_votes"] += min(1.0, f * 10.5 / n)
    e["seen_within_10_votes"] += margin <= 10
    e["expected_margin_0_or_1"] += min(1.0, 1.5 * f / n)
    e["seen_margin_0_or_1"] += margin <= 1


def _bucket(k):
    return str(k) if k < 6 else "6-9" if k < 10 else "10 or more"


def backtest(contests=None, write=True):
    """Each year forecast from a fit on earlier years only (the orchestrator, 05:06). Route (a) is tallied by how
    many earlier years of the same kind (presidential, midterm, odd) its fit had, so MIN_EARLIER can be read off;
    the headline tallies are for the years with at least MIN_EARLIER."""
    contests = contests or load_klarner()
    pres, _ = president_party()
    rows = [r_ for r_ in partisan_rows(contests) if r_["year"] in pres]
    years = sorted({r_["year"] for r_ in rows})
    by_k = collections.defaultdict(collections.Counter)
    allp, per_year, by_size, by_cls = collections.Counter(), {}, collections.defaultdict(collections.Counter), \
        collections.defaultdict(collections.Counter)
    unfit = {}
    for t in years:
        M, k = fit_before(rows, pres, t)
        tr = [r_ for r_ in rows if r_["year"] == t]
        if M is None:
            unfit[t] = {"races": len(tr), "earlier_years_of_kind": k}
            continue
        e = collections.Counter()
        for r_ in tr:
            m, sd, _ = predict_partisan(M, r_, pres)
            sdn = math.sqrt(sd * sd + 0.25 / r_["N"])
            _tally(e, r_["y"], r_["N"], m, sdn)
            _tally(by_k[_bucket(k)], r_["y"], r_["N"], m, sdn)
            if MIN_EARLIER is not None and k >= MIN_EARLIER:
                _tally(by_size[size_bin(r_["N"])], r_["y"], r_["N"], m, sdn)
                _tally(by_cls[r_["cls"]], r_["y"], r_["N"], m, sdn)
                _tally(allp, r_["y"], r_["N"], m, sdn)
        per_year[t] = dict(_finish(e), earlier_years_of_kind=k)
    full = fit_partisan(rows, pres)
    # routes (b), (c) and runoffs: each year from the like races of earlier years only
    crow = class_rows(contests)
    cyears = sorted({r_["year"] for r_ in crow})
    cls_all = collections.defaultdict(collections.Counter)
    cls_unfit = collections.Counter()
    for t in cyears:
        tr = [r_ for r_ in crow if r_["year"] < t]
        dens = {}
        for r_ in crow:
            if r_["year"] != t:
                continue
            if r_["key"] not in dens:
                dens[r_["key"]] = class_density(tr, r_["key"])
            f = dens[r_["key"]][0]
            if f is None:
                cls_unfit[r_["key"]] += 1
                continue
            _class_tally(cls_all[r_["key"]], f, r_)
    cls_sum = collections.Counter()
    for v in cls_all.values():
        cls_sum.update(v)
    out = {
        "method": METHOD, "written_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "about": "Back-test of the model's own forecast for state legislative races, each year forecast from a fit "
                 "on earlier years only. Route a: single-seat general elections with one Democrat and one "
                 "Republican on the ballot; the headline tallies are for years whose fit had at least "
                 f"{MIN_EARLIER} earlier years of the same kind (presidential, midterm, odd), the fewest the "
                 "back-test by earlier years supports ('partisan.by_earlier_years_of_kind'). Routes b and c and "
                 "runoffs: like past races, from earlier years only. 'in_50' is the share of races inside their "
                 "50% interval; 'expected' counts sum the forecast's probabilities, 'seen' counts what happened. "
                 "A margin of 0 or 1 is the check of brief step 5.",
        "partisan": {"min_earlier_years_of_kind": MIN_EARLIER, "all": _finish(allp),
                     "by_earlier_years_of_kind": {k: _finish(v) for k, v in sorted(by_k.items(), key=lambda x: _ord(x[0]))},
                     "by_year": per_year, "years_without_a_fit": unfit,
                     "by_size_two_party_votes": {f"{BINS[i]}-{BINS[i + 1]}": _finish(v) for i, v in sorted(by_size.items())},
                     "by_class": {k: _finish(v) for k, v in sorted(by_cls.items())},
                     "fit_on_all_years": {k: full[k] for k in ("races_fitted", "coef", "swing", "s_a", "s_g", "s_e")}},
        "class": {"all": {kk: (round(vv, 2) if isinstance(vv, float) else vv) for kk, vv in cls_sum.items()},
                  "by_class": {k: {kk: (round(vv, 2) if isinstance(vv, float) else vv) for kk, vv in v.items()}
                               for k, v in sorted(cls_all.items())},
                  "races_without_enough_earlier_like_races": dict(sorted(cls_unfit.items()))},
    }
    if write:
        path = os.path.join(REPO, "data", "local", "backtest.json")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(out, f, indent=1)
            f.write("\n")
    return out


def _ord(k):
    return {"6-9": 6, "10 or more": 10}.get(k, int(k) if k.isdigit() else 99)


# ------------------------------------------------------------------ build data/

LOWER_NAME = {"CA": "Assembly", "NV": "Assembly", "NY": "Assembly", "WI": "Assembly", "NJ": "General Assembly",
              "MD": "House of Delegates", "VA": "House of Delegates", "WV": "House of Delegates"}
ETYPE_WORDS = {"g": "general", "gs": "general, for the rest of a term", "ssg": "special general of the whole chamber",
               "s": "special", "ttp": "top-two primary", "dp": "Democratic primary", "rp": "Republican primary"}


def chamber_name(state, sen):
    if state == "NE":
        return "Legislature"
    return "Senate" if sen == 1 else LOWER_NAME.get(state, "House of Representatives")


def district_label(c):
    parts = []
    if c["dname"]:
        parts.append(c["dname"].title())
    if c["dno"]:
        parts.append(str(c["dno"]))
    label = " ".join(parts) or "at large"
    if c["geopost"]:
        label += f", position {c['geopost']}"
    if c["mmdpost"]:
        label += f", seat {c['mmdpost']}"
    return label


def _slug(x):
    return "".join(ch if ch.isalnum() else "_" for ch in x).strip("_")


def git_commit():
    try:
        return subprocess.run(["git", "-C", REPO, "rev-parse", "--short", "HEAD"], capture_output=True,
                              text=True).stdout.strip() or None
    except OSError:
        return None


def _cands(c):
    out = []
    for a in sorted(c["cands"], key=lambda a: (a["scattering"], -(a["votes"] or 0))):
        won = {"w": True, "l": False, "r": "to runoff", "t": "tied"}.get(a["outcome"], None)
        party = PARTY.get(a["party"], a["party"])
        code = None
        if party == "other" and a["lines"]:
            party = a["lines"][0]
            if party == "nm":     # Klarner's own abbreviation for a non-major party with no name
                party = _MINOR
            elif str(party).isdigit():
                code = str(party)
                party = KLARNER_CODES.get(code, ("unknown",))[0]
        x = {"name": a["name"], "party": party, "votes": None if a["vote_missing"] else a["votes"],
             "won": won if won else None, "party_code": code}
        if a.get("exper") == "inc":
            x["incumbent"] = True
        out.append(x)
    return out


def _p_block(n, mean, sd, under, commit, alongside=None):
    r = core.p_contest(n, mean, sd, "normal")
    out = {"value": r["p"], "event": r["event"], "under": under, "method": r["method"], "f_half": r["f_half"],
           "n": n}
    if alongside:
        out["alongside"] = alongside
    return out


def _compact(x):
    """Drop every field whose value is None (data/README.md, D3: an absent field means null), recursively."""
    if isinstance(x, dict):
        return {k: _compact(v) for k, v in x.items() if v is not None}
    if isinstance(x, list):
        return [_compact(v) for v in x]
    if isinstance(x, float):
        return float(f"{x:.6g}")
    return x


def build(out_dir, with_p=False, sample=False):
    contests = load_klarner()
    info = klarner_info()
    pres, nara_rows = president_party()
    commit = git_commit()
    read_utc = info["files"]["candidate"]["read_utc"]
    src_klarner = F.source(
        f"Carl Klarner, State Legislative Election Returns, 1967-2022, Harvard Dataverse {info['doi']}, "
        f"{info['version']}", "https://doi.org/10.7910/DVN/FJOGJB", read_utc, info["licence"], mark="stated",
        via="https://doi.org/10.7910/DVN/FJOGJB",
        note="compiled by Klarner from official state returns (state election offices' websites when collected, "
             "and the earlier ICPSR editions); the origin of each race is not named, and whether a count is "
             "before or after a recount is not stated per race",
        sha256=info["files"]["candidate"]["sha256"])
    src_nara = F.source("National Archives, Electoral College Results (the sitting president's party)",
                        "https://www.archives.gov/electoral-college", nara_rows[0]["source"]["read_utc"],
                        "US federal public record; no licence printed", mark="stated")
    src_model = F.source(f"the model's own forecast, method {METHOD}", "https://github.com/zwolk46/vote/blob/main/data/local/REPORT.md",
                         datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"), None,
                         mark="inferred", note="each year forecast from a fit on earlier years only; no polls are used")
    rows = [r_ for r_ in partisan_rows(contests) if r_["year"] in pres]
    by_contest = {id(r_["c"]): r_ for r_ in rows}
    crow = class_rows(contests)
    by_crow = {id(r_["c"]): r_ for r_ in crow}
    years = sorted({c["year"] for c in contests})
    fits, dens_cache = {}, {}
    files = collections.defaultdict(list)
    counts = collections.Counter()
    seen_ids = set()
    fit_k = {}
    for t in years:
        if t in pres and any(r_["year"] == t for r_ in rows):
            fits[t], fit_k[t] = fit_before(rows, pres, t)
    totals = collections.defaultdict(list)
    for c in contests:
        tv = sum(a["votes"] for a in c["cands"] if not a["vote_missing"])
        if tv:
            totals[(c["state"], c["sen"], c["year"], c["etype"])].append(tv)
    median_total = {k: float(np.median(v)) for k, v in totals.items()}
    for c in contests:
        t = c["year"]
        route, why = structure(c)
        tv = sum(a["votes"] for a in c["cands"] if not a["vote_missing"])
        med = median_total.get((c["state"], c["sen"], t, c["etype"]))
        kind = "primary" if (route == "class" and why and why.startswith("primary")) or \
            c["etype"] in ("dprunoff", "rprunoff") else "general"
        if route in ("partisan", "class", "boundary", "runoff") and med and tv < SMALL_COUNT[kind] * med:
            route, why = ("not computed", f"the count, {tv:,} votes, is under {round(100 * SMALL_COUNT[kind])}% of the "
                                          f"median of the chamber's {c['etype']} contests that year ({med:,.0f}): "
                                          f"likely incomplete in the source; to be checked at a second source")
        lvl_office = "state-upper" if c["sen"] == 1 else "state-lower"
        et = c["etype"]
        is_primary = (route == "class" and why and why.startswith("primary")) or et == "ttp" or \
            ("p" in et and et not in ("g", "gs", "ssg", "appointed") and not et.startswith("la") and
             not et.startswith("s") and et not in ("grunoff", "gfunsettled", "gfpartunsettled"))
        level = "primary" if is_primary else lvl_office
        st = c["state"]
        dist = district_label(c)
        cid = f"{t}-{level}-{st}-{_slug(dist)}"
        if is_primary:
            cid = f"{t}-primary-{lvl_office}-{st}-{_slug(dist)}-{et}"
        elif et != "g":
            cid += f"-{et}"
        if cid in seen_ids and c["month"]:
            cid += f"-{c['month']:02d}{c['day'] or 0:02d}"
        k = 2
        while cid in seen_ids:
            cid = cid.rsplit("~", 1)[0] + f"~{k}"
            k += 1
        seen_ids.add(cid)
        rec = {"id": cid, "year": t,
               "date": f"{t}-{c['month']:02d}-{c['day']:02d}" if c["month"] and c["day"] else None,
               "level": level, "place": {"state": st, "district": dist},
               "election": ETYPE_WORDS.get(et, et), "seats": c["eseats"] if (c["eseats"] or 1) > 1 else None}
        if is_primary:
            rec["office"] = lvl_office
        cands = _cands(c)
        named = [x for x in cands if x["party"] != "write-in" and x["name"] != "scattering"]
        total = sum(x["votes"] or 0 for x in cands)
        rec["result"] = {"candidates": cands, "total_votes": total, "source": "klarner"}
        rec["forecasts"] = []
        p = {}
        notes = []
        kv = c.get("klarner") or {}
        if kv.get("dontuse") == 1:
            notes.append("Klarner advises against analysing this contest (dontuse = 1)")
        if c["uncert"]:
            notes.append("Klarner marks uncertainty about: " + ", ".join(c["uncert"]))
        k_seats = c["eseats"] or 1
        tn = top_named(c["cands"])
        everyone = sorted(c["cands"], key=lambda a: -(a["votes"] or 0))
        scattering_decides = lambda kk: any(a["scattering"] for a in everyone[kk - 1:kk + 1])  # noqa: E731
        SCATTER_WHY = ("the source's 'scattering' (write-in votes counted together) finished in the deciding pair, "
                       "and whether one write-in candidate did is not reported")
        if route == "zero":
            ballot = [a for a in tn if a["party"] != "w"]
            last = ballot[k_seats - 1]["votes"] if len(ballot) >= k_seats else 0
            wi = [a for a in tn if a["party"] == "w" and (a["votes"] or 0) >= max(1, WRITE_IN_STRONG * (last or 0))]
            if wi and (a_w := wi[0]["votes"] or 0) > 0:
                share = (f"{100 * a_w / last:.0f}% of the last winner's votes" if last else "votes, with no "
                         "candidate on the ballot")
                route, why = ("not computed", f"one name on the ballot for each seat, but a write-in candidate "
                                              f"received {share}: {METHOD} has no forecast route for write-in "
                                              f"contests")
        if route == "zero":
            p.update({"value": 0.0, "event": 0.0, "reason": why})
            counts["p = 0 (unopposed)"] += 1
        elif route == "not computed":
            p["not_computed"] = why
            counts["not computed: " + why.split(":")[0].split(",")[0]] += 1
        elif route == "partisan" and id(c) in by_contest and (fits.get(t) is None or fit_k.get(t, 0) < MIN_EARLIER):
            p["not_computed"] = (f"fewer than {MIN_EARLIER} earlier {cycle(t)} years to fit the forecast on "
                                 f"({fit_k.get(t, 0)}): {METHOD} fits each year on earlier years only")
            counts["not computed: too few earlier years"] += 1
        elif route == "partisan" and id(c) in by_contest and t in fits:
            r_ = by_contest[id(c)]
            M = fits[t]
            mean, sd, a = predict_partisan(M, r_, pres)
            lead = two_leading(c["cands"])
            d = next(x for x in lead if x["party"] == "d")
            rr = next(x for x in lead if x["party"] == "r")
            off_pair = {tn[0]["party"], tn[1]["party"]} != {"d", "r"}
            n = d["votes"] + rr["votes"] - 1
            rec["two_party"] = {"votes": [d["votes"], rr["votes"]], "n_other_voters": n,
                                "share_first": round(d["votes"] / (n + 1), 6)}
            inputs = {"class": r_["cls"], "incumbency": r_["inc"], "lean": round(r_["L"], 4),
                      "lean_year": r_["L_year"], "swing": round(a, 4)}
            if r_["cls"] == "A":
                inputs.update({"last_D": round(r_["xl"] + 0.5, 4), "last_year": kv.get("yearmaxlag")})
            elif r_["cls"] == "B":
                inputs.update({"last_unopposed": "D" if r_["ulag"] > 0 else "R", "last_year": kv.get("yearmaxlag")})
            rec["forecast_inputs"] = inputs
            rec["forecasts"].append({"by": "the model's own", "method": METHOD, "route": "partisan",
                                     "share": {"of": "Democrat, two-party", "mean": round(mean, 4), "sd": round(sd, 4),
                                               "tails": "normal"}, "source": "model"})
            if scattering_decides(1):
                p["not_computed"] = SCATTER_WHY
                counts["not computed: scattering in the deciding pair"] += 1
            elif off_pair:   # the orchestrator, 05:17: p is between the top two (model section 7)
                p["not_computed"] = ("the two leading candidates were not the Democrat and the Republican, so the "
                                     "model's own forecast of the Democrat against the Republican is not of the pair "
                                     "that decided this contest (model section 7: p is between the top two)")
                counts["not computed: D and R not the top two"] += 1
            elif with_p:
                t4 = core.p_contest(n, mean, sd, "t4")
                p = _p_block(n, mean, sd, f"the model's own ({METHOD}), normal", commit,
                             {"t4": {"value": t4["p"], "event": t4["event"], "method": t4["method"]}})
                counts["p computed: partisan"] += 1
            else:
                p["not_computed"] = "awaiting the orchestrator's approval of the forecast method (brief step 3)"
                counts["forecast built: partisan"] += 1
        elif route in ("class", "boundary", "runoff") and id(c) in by_crow:
            r_ = by_crow[id(c)]
            key = r_["key"]
            if (t, key) not in dens_cache:
                dens_cache[(t, key)] = class_density([x for x in crow if x["year"] < t], key)
            f, N, h, kin = dens_cache[(t, key)]
            lead = two_leading(c["cands"])
            kk = (c["eseats"] or 1) if route == "boundary" else 1
            pair = lead[kk - 1:kk + 1]
            n = pair[0]["votes"] + pair[1]["votes"] - 1
            fld = "boundary" if route == "boundary" else "two_party"
            rec[fld] = {"votes": [pair[0]["votes"], pair[1]["votes"]], "n_other_voters": n,
                        "share_first": round(pair[0]["votes"] / (n + 1), 6)}
            if scattering_decides(kk):
                p["not_computed"] = SCATTER_WHY
                counts["not computed: scattering in the deciding pair"] += 1
            elif any(a["party"] == "w" for a in tn[kk - 1:kk + 1]):
                p["not_computed"] = ("a write-in candidate is in the pair that decided this contest; the like-race "
                                     f"classes of {METHOD} are of candidates on the ballot (model section 7: p is "
                                     "between the deciding pair)")
                counts["not computed: a write-in in the deciding pair"] += 1
            elif f is None:
                p["not_computed"] = f"fewer than {MIN_CLASS} like races in earlier years ({N}) for the class '{key}'"
                counts["not computed: too few like races"] += 1
            else:
                q = f * 2 * h
                fc = {"by": "the model's own", "method": METHOD, "route": route, "class": key,
                      "like_races": N, "window": [round(0.5 - h, 2), round(0.5 + h, 2)], "in_window": kin,
                      "q": round(q, 5), "source": "model"}
                if route == "boundary":
                    fc["note"] = "not yet checked"
                if route == "runoff":
                    fc["note"] = "the second round of a runoff, its own two-way race, from like past runoffs"
                rec["forecasts"].append(fc)
                if with_p and n >= 1:
                    if f > 0:
                        sd_eq = 1.0 / (math.sqrt(2 * math.pi) * f)
                        p = _p_block(n, 0.5, sd_eq, f"the model's own ({METHOD}), like past "
                                                     f"{'runoffs' if route == 'runoff' else 'races'}", commit)
                    else:
                        p.update({"value": 0.0, "event": 0.0,
                                  "reason": f"no like race in {N} finished within {round(50 - 100 * h)}-{round(50 + 100 * h)}%"})
                    counts[f"p computed: {route}"] += 1
                elif not with_p:
                    p["not_computed"] = "awaiting the orchestrator's approval of the forecast method (brief step 3)"
                    counts[f"forecast built: {route}"] += 1
        else:
            p["not_computed"] = f"no forecast route applies (a structure {METHOD} does not cover)"
            counts["not computed: no route"] += 1
        rec["p"] = p or None
        if notes:
            rec["notes"] = notes
        files[(level, t, st)].append(_compact(rec))
        counts["contests"] += 1
    if sample:
        keep = {("NH", 2022), ("MN", 2022), ("TX", 2022), ("MT", 1974)}
        files = {k: v for k, v in files.items() if (k[2], k[1]) in keep or (k[0], k[1], k[2]) == ("primary", 2014, "NH")}
    total_bytes = 0
    by_level = collections.Counter()
    for (level, t, st), cs in sorted(files.items()):
        obj = {"level": level, "year": t, "state": st,
               "about": f"{level} contests of {t} in {STATE_NAMES.get(st, st)}, in the layout of plan/PLAN.md section 3 with the "
                        f"fields data/README.md adds (D3). Built by pipeline/local.py from "
                        f"pipeline/intake/klarner_state_legislative.py's cache.",
               "chamber": {"state-upper": f"{STATE_NAMES.get(st, st)} {chamber_name(st, 1)}",
                           "state-lower": f"{STATE_NAMES.get(st, st)} {chamber_name(st, 0)}"},
               "p_computed_by": "pipeline/local.py", "p_commit": commit,
               "party_codes": {k: f"Klarner's codebook (Appendix C): {KLARNER_CODES[k][1]}" if k in KLARNER_CODES
                               else "not in Klarner's codebook" for k in sorted({a["party_code"] for x in cs
                               for a in x["result"]["candidates"] if a.get("party_code")})} or None,
               "sources": {"klarner": src_klarner, "nara": src_nara, "model": src_model},
               "contests": cs}
        path = os.path.join(out_dir, level, str(t), f"{st}.json")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            head = {k: v for k, v in obj.items() if k != "contests" and v is not None}
            body = json.dumps(head, ensure_ascii=False, separators=(",", ":"))
            f.write(body[:-1] + ',"contests":[\n')
            f.write(",\n".join(json.dumps(x, ensure_ascii=False, separators=(",", ":")) for x in cs))
            f.write("\n]}\n")
        sz = os.path.getsize(path)
        total_bytes += sz
        by_level[level] += sz
    print(f"wrote {sum(len(v) for v in files.values()):,} contests in {len(files):,} files, "
          f"{total_bytes / 1e6:.1f} MB: " + ", ".join(f"{k} {v / 1e6:.1f} MB" for k, v in sorted(by_level.items())))
    print(json.dumps(counts, indent=1))
    return files, counts


# ------------------------------------------------------------------ command line

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("what", choices=["backtest", "build"])
    ap.add_argument("--out", default=os.path.join(REPO, "data"))
    ap.add_argument("--with-p", action="store_true")
    ap.add_argument("--sample", action="store_true")
    a = ap.parse_args()
    if a.what == "backtest":
        out = backtest()
        print(json.dumps(out["partisan"]["all"], indent=1))
        print(json.dumps(out["partisan"]["by_size_two_party_votes"], indent=1))
        print(json.dumps(out["partisan"]["by_class"], indent=1))
        print(json.dumps(out["class"], indent=1))
    else:
        build(a.out, with_p=a.with_p, sample=a.sample)


if __name__ == "__main__":
    main()
