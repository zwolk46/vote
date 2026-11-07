"""pipeline/college.py: the Electoral College stage of p, computed exactly, never by the independence shortcut.

Written 2026-11-07 by worker D1 (briefs/D1-data-president.md step 4; model/MODEL.md section 3; model/MATH.md
section 4; model/math/s4_two_stage.py, whose method this generalises).

The identity (MATH section 4): for a voter in unit i (a state, or a Maine or Nebraska district),
    p_i = P(unit i's count is tied, our convention)  x  W_i,
    W_i = P(unit i's electoral votes decide the College | unit i is tied).
W_i is a conditional probability. Replacing it by the unconditional P(the unit's votes decide) assumes the
units are independent; the brief forbids that shortcut, because a tie in a state that leans 10 points says
the national swing was large (S4 measures the cost).

The window. Let E be the electoral votes the other units give candidate A (the Democrat here), and e_i the
unit's own. The unit's flip changes the winner by
    w(E) = win(E + e_i) - win(E),   win(x) = 1 if x >= majority, PI_HOUSE if 2x = total (a College tie),
                                    0 otherwise,
so w = 1 when the flip moves A from losing to winning outright, and PI_HOUSE (one half) when it moves the
College between a tie and a decision, as in S4: a tie goes to the House, whose choice is "ex ante unknowable",
the two-way tie rule of the model.

Three ways to get E's distribution given the tie, each used where its inputs exist:
  dp_stage_two      a forecast of means and sds per unit, with a common national swing of stated sd and
                    independent unit errors (normal): E's distribution exactly by dynamic programming over
                    units, integrated over the swing conditional on the tie (as S4).
  sims_window       a forecaster's own joint simulations (the Economist, 2020): the draws whose unit share
                    lies in a narrow window around one half, each weighted by w(E) of that draw; p's numerator
                    is then a count over draws, no shape assumed.
  mvn_stage_two     a forecaster's published means, sds and correlation matrix, read as a multivariate normal:
                    the other units' shares given the tie are normal with the conditional mean and covariance,
                    and W is estimated by drawing from that conditional. Used where the window holds too few
                    draws (the safe states), and beside sims_window as a check where both work.
"""
import math

import numpy as np

PI_HOUSE = 0.5


def window_weights(e_i, total, majority, pi_house=PI_HOUSE):
    """w(E) for E = 0..total - e_i: how much the unit's flip changes A's chance of winning the College."""
    def win(x):
        if x >= majority:
            return 1.0
        return pi_house if 2 * x == total else 0.0
    return np.array([win(E + e_i) - win(E) for E in range(total - e_i + 1)])


def _phi_cdf(x):
    x = np.asarray(x, dtype=float)
    return 0.5 * (1.0 + np.vectorize(math.erf)(x / math.sqrt(2.0)))


def dp_stage_two(i, mu, tau, ev, s_d, total, majority, grid_n=241, pi_house=PI_HOUSE):
    """W_i for unit i under the normal forecast v_j = mu_j + delta + eps_j, delta ~ N(0, s_d^2) common to all
    units, eps_j ~ N(0, tau_j^2 - s_d^2) independent; tau_j is unit j's whole forecast sd (so s_d <= min tau).
    Conditional on v_i = 1/2, delta ~ N(m, v) with m = (1/2 - mu_i) s_d^2 / tau_i^2 and
    v = s_d^2 (tau_i^2 - s_d^2) / tau_i^2. Returns (W_conditional, W_unconditional)."""
    mu, tau, ev = np.asarray(mu, float), np.asarray(tau, float), np.asarray(ev, int)
    assert s_d <= tau.min() + 1e-12, "the common swing cannot exceed a unit's whole sd"
    s = np.sqrt(np.maximum(tau ** 2 - s_d ** 2, 1e-18))
    w = window_weights(int(ev[i]), total, majority, pi_house)
    others = [j for j in range(len(mu)) if j != i]
    out = []
    for conditional in (True, False):
        if conditional:
            m = (0.5 - mu[i]) * s_d ** 2 / tau[i] ** 2
            sd = math.sqrt(max(s_d ** 2 * (tau[i] ** 2 - s_d ** 2) / tau[i] ** 2, 0.0))
        else:
            m, sd = 0.0, s_d
        if sd < 1e-12:
            grid, gw = np.array([m]), np.array([1.0])
        else:
            grid = np.linspace(m - 6 * sd, m + 6 * sd, grid_n)
            gw = np.exp(-0.5 * ((grid - m) / sd) ** 2)
            gw /= gw.sum()
        size = total - int(ev[i]) + 1
        dist = np.zeros((len(grid), size))
        dist[:, 0] = 1.0
        for j in others:
            q = _phi_cdf((mu[j] + grid - 0.5) / s[j])[:, None]
            shifted = np.zeros_like(dist)
            shifted[:, ev[j]:] = dist[:, :size - ev[j]]
            dist = dist * (1 - q) + shifted * q
        out.append(float(((dist @ w) * gw).sum()))
    return out[0], out[1]


def sims_window(shares, dem_ev, ev, i, k_steps, step, total, majority, pi_house=PI_HOUSE):
    """Counts over a forecaster's joint draws for unit i. shares: (K, units) two-party shares for A, printed
    to a grid of `step` (1e-4 for the Economist); dem_ev: (K,) A's electoral votes in each draw as published
    (the tie-breaker where a printed share is exactly one half); the window is |share - 1/2| <= k_steps*step,
    of width (2 k_steps + 1) * step. Returns a dict of counts; p's numerator density is
    weighted / (K * width)."""
    K = shares.shape[0]
    e = np.asarray(ev, int)
    won = shares > 0.5
    amb = np.isclose(shares, 0.5, atol=step / 10)
    base = (won & ~amb) @ e                      # A's electoral votes from the units not printed at one half
    rem = dem_ev - base                          # what the ambiguous units gave A, by the published total
    e_i = int(e[i])
    in_win = np.abs(shares[:, i] - 0.5) <= k_steps * step + step / 10
    E_rest = np.where(won[:, i] & ~amb[:, i], dem_ev - e_i, dem_ev).astype(int)
    # unit i printed at one half: E_rest is clear only if it is the only ambiguous unit in the draw
    n_amb = amb.sum(axis=1)
    only_i = amb[:, i] & (n_amb == 1)
    E_rest = np.where(only_i, base, E_rest)
    unclear = amb[:, i] & (n_amb > 1)
    # another unit at one half and unit i clear: dem_ev already holds the resolved total, so E_rest is right
    w = window_weights(e_i, total, majority, pi_house)
    use = in_win & ~unclear
    weights = w[np.clip(E_rest[use], 0, len(w) - 1)]
    return {"draws": int(K), "k_steps": int(k_steps), "width": (2 * k_steps + 1) * step,
            "in_window": int(in_win.sum()), "dropped_unclear": int((in_win & unclear).sum()),
            "weighted": float(weights.sum()), "decisive_full": int((weights == 1.0).sum()),
            "decisive_half": int(np.isclose(weights, pi_house).sum()),
            # the published totals agree with the units in every draw with no unit at one half
            "draws_total_mismatch": int((rem[~amb.any(axis=1)] != 0).sum())}


def mvn_stage_two(i, mu, sd, corr, ev, total, majority, draws=40000, seed=1, pi_house=PI_HOUSE):
    """W_i from a multivariate normal reading of a forecaster's means, sds and correlations: draw the other
    units given unit i = 1/2 from the conditional normal, count w(E). Also the unconditional W for the
    record. Seeded, so reruns give the same figure; the Monte Carlo error is returned."""
    mu, sd, ev = np.asarray(mu, float), np.asarray(sd, float), np.asarray(ev, int)
    cov = np.asarray(corr, float) * np.outer(sd, sd)
    o = [j for j in range(len(mu)) if j != i]
    c_oi = cov[o, i]
    cond_mu = mu[o] + c_oi * (0.5 - mu[i]) / cov[i, i]
    cond_cov = cov[np.ix_(o, o)] - np.outer(c_oi, c_oi) / cov[i, i]
    rng = np.random.default_rng(seed)
    L = np.linalg.cholesky(cond_cov + 1e-12 * np.eye(len(o)))
    x = cond_mu + rng.standard_normal((draws, len(o))) @ L.T
    E = (x > 0.5) @ ev[o]
    w = window_weights(int(ev[i]), total, majority, pi_house)
    vals = w[E]
    Lf = np.linalg.cholesky(cov + 1e-12 * np.eye(len(mu)))
    y = mu + rng.standard_normal((draws, len(mu))) @ Lf.T
    Eu = (y[:, o] > 0.5) @ ev[o]
    vu = w[Eu]
    return {"W": float(vals.mean()), "W_se": float(vals.std() / math.sqrt(draws)),
            "W_unconditional": float(vu.mean()), "draws": draws, "seed": seed}
