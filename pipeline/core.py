"""pipeline/core.py: p for one two-way contest, the computation every data worker shares.

Written 2026-11-07 by worker D1 (briefs/D1-data-president.md, step 1). Every p the site shows for a
real contest is computed through this file, so the site has one implementation of the model's formula
(plan/PLAN.md section 3). It builds on model/math/common.py, the functions the model's own figures were
checked with (model/math/run_all.sh writes model/math/OUTPUT.txt), by import, not by copying.

Definitions (model/MODEL.md section 3; model/MATH.md sections 0 and 1):

  n      the number of OTHER voters in the contest, your ballot excluded. For a two-way race this is
         the votes of the two leading candidates (the two-party vote), as in the model.
  mean   the forecast's mean of the two-party share of the side your ballot is for, as a fraction.
         In the density form p does not depend on the side (f(1/2) is the same either way). In the
         exact sum it is identical for either side at an even n; at an odd n your side needs the others
         to leave it one short, so the two sides differ by about |mean - 1/2| / (n sd^2) (1.1% at
         n = 1,001, mean 0.52, sd 0.04), the same order as the density form's own error, and only
         where "auto" uses the exact sum. A worker who shows p for both sides of a small race calls
         p_contest once for each.
  sd     the forecast's standard deviation of that share, as a fraction (2.5 points is 0.025).
  tails  "normal": the share is Normal(mean, sd^2), truncated to (0, 1);
         "t4": a Student-t with 4 degrees of freedom matched on the same standard deviation, that is
         with scale sd / sqrt(2), truncated to (0, 1) (model section 9.5; MATH section 1.5).
  p      the chance that who wins differs between your ballot counted and not counted, everyone else
         the same, a tie settled by a fair lot counting as half (model sections 1, 3 and 9.2). Before
         the election it is the same under every tie rule (MATH section 1.1).
  event  the chance that the count without your ballot lands within one vote: tied, or your side one
         short. It is twice p. It is named whenever it is shown and never shown as p (law 2b; model
         section 9.2).

How p is computed (model section 3, "The one-line formula" and "How good it is"):

  "exact"    the lattice sum. X, the other voters' count for your side, has the binomial count folded
             into the forecast by numerical integration (common.normalmix_pmf or common.tmix_pmf); and
             p = 1/2 P(X = n/2) for an even n (the others tied) or 1/2 P(X = (n-1)/2) for an odd n
             (your side one short), the fair-lot value (common.p_from_pmf).
  "density"  the one-line formula p = f(1/2) / (2n), with f the forecast density of the share at 1/2
             (common.normal_density, common.t_density, common.p_density_approx).
  "auto"     the exact sum where the model says to use it, the density form elsewhere. The model gives
             two conditions, and either one sends a contest to the exact sum:
               - fewer than 1,000 other voters (model section 3: "Below 1,000 voters the site computes
                 the exact sum");
               - n x sd^2 below 6.25 (model section 3, the table's first row: "once n x (forecast
                 spread)^2 is above about 6 [...]; below that, the site uses the exact sum"; MATH
                 section 1.3: the density form is within 2% of the exact sum once n sd^2 > 6.25, at an
                 even forecast).
             If the exact sum underflows to zero (a forecast so lopsided that floating point cannot hold
             it), the density form is returned and the method says so.

Accuracy of "auto" where it picks the density form (MATH sections 1.3 and 6.2): the density form's
relative error is about +1/(8 n sd^2) at an even normal forecast, so under 2% there; off centre it turns
negative and grows with the distance from 1/2 in standard deviations (-2.3% at n = 10,000, sd 0.03,
mean 0.55). For a t4 forecast the error at the centre is about +2.5/(8 n sd^2), so up to 5% at the
threshold. At the sizes of statewide and congressional races (n in the hundreds of thousands or more)
every one of these is under 1% for any forecast within 10 standard deviations of even. A worker who
needs the exact value anywhere passes method="exact".
"""
import importlib.util
import math
import os

_COMMON_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                             os.pardir, "model", "math", "common.py"))
_spec = importlib.util.spec_from_file_location("vote_model_math_common", _COMMON_PATH)
common = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(common)

EXACT_BELOW_N = 1000          # model section 3: the exact sum below 1,000 voters
EXACT_BELOW_N_SD2 = 6.25      # model section 3, table row 1; MATH section 1.3: n sd^2 > 6.25 for 2%
TAILS = ("normal", "t4")
METHODS = ("auto", "exact", "density")


def _check(n, mean, sd, tails, method):
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError(f"n must be a whole number of other voters, at least 1 (got {n!r})")
    if not (0.0 < mean < 1.0):
        raise ValueError(f"mean must be a share strictly between 0 and 1 (got {mean!r})")
    if not (sd > 0.0) or not math.isfinite(sd):
        raise ValueError(f"sd must be a positive share (got {sd!r})")
    if tails not in TAILS:
        raise ValueError(f"tails must be one of {TAILS} (got {tails!r})")
    if method not in METHODS:
        raise ValueError(f"method must be one of {METHODS} (got {method!r})")


def forecast_density_at_half(mean, sd, tails="normal"):
    """f(1/2): the forecast density of the share at a dead heat (untruncated; the truncation to (0, 1)
    changes nothing at the precision shown for any real forecast)."""
    if tails == "normal":
        return common.normal_density(0.5, mean, sd)
    return common.t_density(0.5, mean, sd / math.sqrt(2.0), 4)


def p_exact(n, mean, sd, tails="normal"):
    """The lattice sum, fair lot: common.p_from_pmf over common.normalmix_pmf or common.tmix_pmf."""
    if tails == "normal":
        return common.p_from_pmf(lambda k: common.normalmix_pmf(k, n, mean, sd), n, rule="lot")
    s = sd / math.sqrt(2.0)
    return common.p_from_pmf(lambda k: common.tmix_pmf(k, n, mean, s, df=4), n, rule="lot")


def p_density(n, mean, sd, tails="normal"):
    """The one-line formula p = f(1/2) / (2n)."""
    return common.p_density_approx(n, forecast_density_at_half(mean, sd, tails))


def p_contest(n, mean, sd, tails="normal", method="auto"):
    """p and the event for one two-way contest. See the module text for every term.

    Returns a dict:
      p        the chance your counted ballot changes who wins (a tie by lot counts half);
      event    the chance the count without your ballot lands within one vote, = 2 p;
      method   "exact" or "density": which computation gave p;
      f_half   f(1/2), the forecast density of the share at a dead heat (p = f_half / (2 n) in the
               density form; shown in the site's full mode);
      n, mean, sd, tails   the inputs, echoed so a record of p carries what it was computed from.
    """
    _check(n, mean, sd, tails, method)
    f_half = forecast_density_at_half(mean, sd, tails)
    use = method
    if method == "auto":
        use = "exact" if (n < EXACT_BELOW_N or n * sd * sd < EXACT_BELOW_N_SD2) else "density"
    if use == "exact":
        p = p_exact(n, mean, sd, tails)
        if not (p > 0.0) or not math.isfinite(p):
            p = common.p_density_approx(n, f_half)
            use = "density (the exact sum underflowed)"
    else:
        p = common.p_density_approx(n, f_half)
    return {"p": p, "event": 2.0 * p, "method": use, "f_half": f_half,
            "n": n, "mean": mean, "sd": sd, "tails": tails}


def one_in(p):
    """'1 in N' with N = 1/p rounded to a whole number, as the model and MATH print it."""
    return common.one_in(p)
