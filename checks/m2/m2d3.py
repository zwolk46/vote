"""checks/m2/m2d3.py: worker M2's own reading of D3's levels (data/state-upper, data/state-lower, data/local,
data/measure), for checks c14 and c15.

Written 2026-11-07 by worker M2 (briefs/M2-check-computed-p.md, the amendment of 07:44, item 4). It imports nothing
from pipeline/ (the brief: a check that runs the same code finds nothing that code gets wrong); the conventions below
are read off data/local/REPORT.md sections 2, 7, 8 and 9 and model/MODEL.md sections 3 and 7, with pipeline/local.py,
local_medsl.py, local_ncsbe.py and measures.py read only to learn what each recorded field means.

The files are read once into slim rows (`rows(level)`): the id, year, state, the forecast's route and class, the
like-race counts (N like races, k in the window, the window), the partisan mean and sd, the recorded inputs, the
deciding pair, the p block, and the result's candidates (party, votes, name, incumbent) so that a class can be rebuilt
from what the file says was on the ballot.

Formulas (REPORT section 2; MODEL section 3):
  like races      q = k / N over the window's half-width h (0.01, widening to 0.02 then 0.05 until k >= 10);
                  f(1/2) = q / (2h); p = f / (2n) in the density form, or the exact lattice sum with a normal of
                  mean 1/2 and sd_eq = 1 / (sqrt(2 pi) f) where n < 1,000 or n sd^2 < 6.25 (pipeline/core.py, 'auto').
  partisan        f(1/2) = normal density at 1/2 with the forecast's mean and sd; the same rule for exact or density;
                  t4 beside it (scale sd / sqrt 2).
  local, calibrated (the orchestrator's ruling of 06:38, REPORT section 7): like races, f(1/2) x factor and p again
                  from sd_eq of the calibrated f; partisan, p and f(1/2) x factor, the method as before.
  measures        f(t) = k / N / (2h) at the threshold t; yes = (1 - t) f / n, no = t f / n, value the larger,
                  event = f / n (MODEL section 7, pipeline/measures.py p_block).
"""
import collections
import glob
import json
import math
import os
import re

import numpy as np
from scipy import stats

import m2lib as M

LEVELS = ("state-upper", "state-lower", "local", "measure")
WINDOWS = (0.01, 0.02, 0.05)
MIN_IN_WINDOW = 10
MIN_CLASS = 100
EXACT_BELOW_N = 1000
EXACT_BELOW_N_SD2 = 6.25
BINS = (0, 3000, 10000, 30000, float("inf"))
CLASS_RE = re.compile(r"for the class '(.+)'\s*$")
SQRT2PI = math.sqrt(2 * math.pi)


# ------------------------------------------------------------------------------------------ the files
def level_files(level):
    return sorted(glob.glob(os.path.join(M.DATA, level, "[0-9]*", "*.json")))


def slim(level, head, c):
    p = c.get("p") or {}
    fc = c.get("forecasts") or []
    f = fc[-1] if fc else {}
    status = "value" if "value" in p else "not_computed" if "not_computed" in p else "none"
    reason = p.get("not_computed") or p.get("reason")
    cls = f.get("class")
    if cls is None and reason:
        m = CLASS_RE.search(reason)
        cls = m.group(1) if m else None
    kind = "two_party" if "two_party" in c else "boundary" if "boundary" in c else "two_way" if "two_way" in c else None
    res = c.get("result") or {}
    return {"id": c["id"], "level": level, "year": c["year"], "state": c["place"]["state"], "date": c.get("date"),
            "election": c.get("election"), "seats": c.get("seats") or 1, "src": res.get("source"),
            "votes_source": res.get("votes_source"), "status": status, "reason": reason, "route": f.get("route"),
            "cls": cls, "cls_recorded": f.get("class") is not None, "N": f.get("like_races", f.get("like_measures")),
            "kin": f.get("in_window"), "win": f.get("window"), "q": f.get("q"), "cal": f.get("calibration"),
            "note": f.get("note"), "fitted_on": f.get("fitted_on"), "share": f.get("share"),
            "inputs": c.get("forecast_inputs"), "pair": c.get(kind) if kind else None, "pair_kind": kind, "p": p,
            "cands": [(a.get("party"), a.get("votes"), a.get("name"), bool(a.get("incumbent")), a.get("won"))
                      for a in res.get("candidates", [])],
            "total_votes": res.get("total_votes"), "office": c.get("office"), "office_type": c.get("office_type"),
            "office_scope": c.get("office_scope"), "counties": (c.get("place") or {}).get("counties"),
            "question": c.get("question"), "t": (c.get("threshold") or {}).get("t"), "yes_share": res.get("yes_share"),
            "commit": head.get("p_commit"), "by": head.get("p_computed_by")}


_CACHE = {}


def rows(level):
    """Every contest of a level as a slim row, read once."""
    if level not in _CACHE:
        out = []
        for path in level_files(level):
            with open(path) as fh:
                d = json.load(fh)
            for c in d["contests"]:
                out.append(slim(level, d, c))
        _CACHE[level] = out
    return _CACHE[level]


# ------------------------------------------------------------------------------------------ formulas
def window_h(win):
    return round((win[1] - win[0]) / 2, 2) if win else None


def class_density(shares, h_list=WINDOWS, min_in=MIN_IN_WINDOW, min_class=MIN_CLASS):
    """The lay form on a class: shares are the leading candidate's share of the deciding pair (>= 1/2).
    Returns (f, N, h, k) or (None, N, None, None) below min_class."""
    N = len(shares)
    if N < min_class:
        return None, N, None, None
    s = np.asarray(shares)
    for h in h_list:
        k = int(np.sum(s <= 0.5 + h + 1e-12))
        if k >= min_in or h == h_list[-1]:
            return k / N / (2.0 * h), N, h, k


def density_at(shares, t, h_list=WINDOWS, min_in=MIN_IN_WINDOW, min_class=MIN_CLASS):
    """The same at a threshold t for measures: shares are yes shares, the window two-sided about t."""
    N = len(shares)
    if N < min_class:
        return None, N, None, None
    s = np.asarray(shares)
    for h in h_list:
        k = int(np.sum(np.abs(s - t) <= h + 1e-12))
        if k >= min_in or h == h_list[-1]:
            return k / N / (2.0 * h), N, h, k


def sd_eq(f):
    return 1.0 / (SQRT2PI * f)


def method_rule(n, sd):
    return "exact" if (n < EXACT_BELOW_N or n * sd * sd < EXACT_BELOW_N_SD2) else "density"


def p_auto(n, mean, sd, tails="normal"):
    """p as pipeline/core.py's 'auto' chooses it, by my own implementation: (p, method, f_half)."""
    f = M.f_half(mean, sd, tails)
    use = method_rule(n, sd)
    if use == "exact":
        p = M.p_exact(n, mean, sd, tails)
        if not (p > 0.0) or not math.isfinite(p):
            p, use = f / (2.0 * n), "density (the exact sum underflowed)"
    else:
        p = f / (2.0 * n)
    return p, use, f


def size_bin(n):
    for i in range(len(BINS) - 1):
        if n < BINS[i + 1]:
            return i
    return len(BINS) - 2


def rel(a, b):
    """Relative difference of a against b (b the record), inf where only one is zero."""
    if a is None or b is None:
        return None
    if b == 0:
        return 0.0 if a == 0 else float("inf")
    return abs(a - b) / abs(b)


def envelope(fn, boxes):
    """min and max of fn over the corners (and centre) of the boxes [(lo, hi), ...]: the range a value can take when
    its inputs were recorded rounded. fn takes one argument per box."""
    import itertools
    vals = [fn(*[(lo + hi) / 2 for lo, hi in boxes])]
    for corner in itertools.product(*[(lo, hi) for lo, hi in boxes]):
        vals.append(fn(*corner))
    return min(vals), max(vals)


def within(v, lo, hi, tol=1e-5):
    """v recorded to 6 significant figures lies in [lo, hi] allowing that rounding."""
    if v is None:
        return False
    slack = tol * max(abs(lo), abs(hi), abs(v))
    return lo - slack <= v <= hi + slack


# ------------------------------------------------------------------------------------------ the structure of a contest
MAJOR = {"D": "D", "R": "R"}
NAMED_EXCLUDED = ("write-in",)


def named(cands):
    """Candidates on the ballot: not write-ins, not the source's 'scattering' (REPORT section 2: p is between the
    deciding pair of candidates on the ballot; pipeline/local.py two_leading)."""
    return [a for a in cands if a[0] != "write-in" and (a[2] or "").strip().lower() != "scattering"]


def structure_state(r):
    """(route, class) for a state legislative general in the file, as REPORT section 2 defines the classes: by the
    seats at once, and the Democrats and Republicans on the ballot. None where the file's election is not a
    general of the kinds route (b)/(c) covers, or a candidate's votes are missing."""
    el = r["election"] or ""
    if el not in ("general", "general, for the rest of a term", "special general of the whole chamber"):
        return None
    cands = r["cands"]
    if any(a[1] is None for a in cands if (a[2] or "").strip().lower() != "scattering"):
        return None
    nm = sorted(named(cands), key=lambda a: -(a[1] or 0))
    k = r["seats"] or 1
    if len(nm) <= k:
        return ("zero", None)
    nd = sum(1 for a in nm if a[0] == "D")
    nr = sum(1 for a in nm if a[0] == "R")
    if k > 1:
        slate = ("both major parties running a full slate" if nd >= k and nr >= k else
                 "both major parties running, one short of a full slate" if nd and nr else
                 "one major party or none against the others")
        return ("boundary", f"general, {k if k < 4 else '4+'} seats at once, {slate}")
    if nd == 1 and nr == 1:
        return ("partisan", None)
    if nd + nr == 0:
        if all(a[0] == "nonpartisan" for a in nm):
            return ("class", "general, nonpartisan")
        return ("class", "general, no Democrat or Republican on the ballot")
    if nd + nr == 1:
        return ("class", "general, one major party against minor parties or independents")
    return ("class", "general, two candidates of one major party")


def deciding_pair(r, k):
    """The k-th and (k+1)-th named candidates by votes: (x1, x2) or None."""
    nm = sorted(named(r["cands"]), key=lambda a: -(a[1] or 0))
    if len(nm) <= k:
        return None
    return nm[k - 1][1], nm[k][1]


def fmt(x, d=4):
    return M.fmt(x, d)
