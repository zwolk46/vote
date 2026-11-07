"""checks/m2/m2lib.py: worker M2's own implementation of the model's formulas, for checking data/.

Written 2026-11-07 by worker M2 (briefs/M2-check-computed-p.md). It imports nothing from pipeline/ or
model/math/ (the brief: a check that runs the same code finds nothing that code gets wrong). numpy and
scipy only. Every definition follows model/MODEL.md section 3 and model/MATH.md sections 0, 1 and 4:

  n       the number of OTHER voters: the two leading candidates' votes less one.
  mean    the forecast mean of the Democrat's two-party share; sd its standard deviation.
  tails   "normal": Normal(mean, sd^2). "t4": a Student-t with 4 degrees of freedom matched on the same
          standard deviation, so its scale is sd / sqrt(2) (a t4 with scale s has variance 2 s^2).
  p       f(1/2) / (2 n) in the density form; or the exact lattice sum, a tie by lot counting one half.
  event   2 p.
  W       P(the unit's electoral votes decide the College | the unit's count is tied), MATH 4.1.
"""
import hashlib
import json
import os
import subprocess

import numpy as np
from scipy import integrate, stats

SQRT2 = np.sqrt(2.0)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(ROOT, "data")
CACHE = os.environ.get("VOTE_M2_CACHE", os.path.expanduser("~/.cache/vote-m2"))


# ------------------------------------------------------------------------------------------ densities
def f_half(mean, sd, tails="normal"):
    """The forecast density of the share at one half."""
    if tails == "normal":
        return float(stats.norm.pdf(0.5, loc=mean, scale=sd))
    if tails == "t4":
        return float(stats.t.pdf(0.5, df=4, loc=mean, scale=sd / SQRT2))
    raise ValueError(tails)


def cdf(x, mean, sd, tails="normal"):
    if tails == "normal":
        return stats.norm.cdf(x, loc=mean, scale=sd)
    return stats.t.cdf(x, df=4, loc=mean, scale=sd / SQRT2)


def own_pres_pdf(x, mean, s_nat, s_state):
    """The density at x of mean + delta + eps, delta ~ N(0, s_nat^2), eps ~ t4 matched on sd s_state
    (D1's own forecast, data/president/REPORT.md): a convolution, integrated by quadrature."""
    sc = s_state / SQRT2
    g = lambda d: stats.norm.pdf(d, 0.0, s_nat) * stats.t.pdf(x - mean - d, 4, 0.0, sc)  # noqa: E731
    v, _ = integrate.quad(g, -12 * s_nat, 12 * s_nat, limit=200)
    return float(v)


def own_pres_cdf(x, mean, s_nat, s_state):
    sc = s_state / SQRT2
    g = lambda d: stats.norm.pdf(d, 0.0, s_nat) * stats.t.cdf(x - mean - d, 4, 0.0, sc)  # noqa: E731
    v, _ = integrate.quad(g, -12 * s_nat, 12 * s_nat, limit=200)
    return float(v)


def p_density(n, f):
    return f / (2.0 * n)


def p_exact(n, mean, sd, tails="normal", points=400001):
    """The lattice sum, a tie by lot: p = 1/2 P(X = n/2) (n even) or 1/2 P(X = (n-1)/2) (n odd), with
    X | v ~ Binomial(n, v) and v the forecast, truncated to (0, 1); Simpson's rule on a grid of v."""
    k = n // 2 if n % 2 == 0 else (n - 1) // 2
    if tails == "normal":
        lo, hi = mean - 15 * sd, mean + 15 * sd
        w = lambda v: stats.norm.pdf(v, mean, sd)  # noqa: E731
    else:
        lo, hi = 0.0, 1.0
        w = lambda v: stats.t.pdf(v, 4, mean, sd / SQRT2)  # noqa: E731
    lo, hi = max(lo, 1e-9), min(hi, 1 - 1e-9)
    v = np.linspace(lo, hi, points)
    wv = w(v)
    wv = wv / integrate.simpson(wv, x=v)
    pmf = np.exp(stats.binom.logpmf(k, n, v))
    return 0.5 * float(integrate.simpson(pmf * wv, x=v))


# --------------------------------------------------------------------------------------- the College
def window_weights(e_i, total, majority, pi_house=0.5):
    """w(E) for E = A's electoral votes from the other units: the change in A's chance of the presidency
    when unit i flips to A. A College tie (2E = total) is worth pi_house (the House decides, a lot)."""
    E = np.arange(total - e_i + 1)

    def win(x):
        return np.where(x >= majority, 1.0, np.where(2 * x == total, pi_house, 0.0))
    return win(E + e_i) - win(E)


def others_ev_pmf(q, ev):
    """P(the units give A exactly E electoral votes) from each unit's win chance q (an array, one per
    unit, or a (G, units) array over a grid) by polynomial multiplication of the generating functions,
    numpy.convolve: a different implementation of the same exact count."""
    q = np.atleast_2d(np.asarray(q, float))
    out = []
    for row in q:
        poly = np.array([1.0])
        for qj, e in zip(row, ev):
            factor = np.zeros(e + 1)
            factor[0], factor[e] = 1.0 - qj, qj
            poly = np.convolve(poly, factor)
        out.append(poly)
    return np.array(out)


def W_quadrature(i, mu, s_unit, ev, s_d, total, majority, tails, nodes=241, pi_house=0.5):
    """W_i under the swing model (v_j = mu_j + delta + eps_j, delta ~ N(0, s_d^2), eps_j independent of
    sd s_unit[j], normal or t4 matched on sd), by Gauss-Hermite quadrature over delta given the tie, and
    the exact count of the other units' electoral votes by polynomial multiplication. Returns (f_half,
    W, W_unconditional)."""
    mu, s_unit, ev = np.asarray(mu, float), np.asarray(s_unit, float), np.asarray(ev, int)
    # the posterior of delta given v_i = 1/2 is proportional to the prior times eps_i's density at
    # 1/2 - mu_i - delta; integrate on a wide, fine grid (not Gauss-Hermite: the t4 likelihood can be far
    # from the prior's centre)
    grid = np.linspace(-12 * s_d, 12 * s_d, nodes)
    prior = stats.norm.pdf(grid, 0.0, s_d)
    if tails == "normal":
        like = stats.norm.pdf(0.5 - mu[i] - grid, 0.0, s_unit[i])
        qmat = stats.norm.sf((0.5 - mu[None, :] - grid[:, None]) / s_unit[None, :])
    else:
        like = stats.t.pdf(0.5 - mu[i] - grid, 4, 0.0, s_unit[i] / SQRT2)
        qmat = stats.t.sf((0.5 - mu[None, :] - grid[:, None]) / (s_unit[None, :] / SQRT2), 4)
    dg = grid[1] - grid[0]
    fh = float(np.sum(prior * like) * dg)
    post = prior * like
    post /= post.sum()
    pri = prior / prior.sum()
    others = [j for j in range(len(mu)) if j != i]
    pm = others_ev_pmf(qmat[:, others], ev[others])          # (nodes, total - e_i + 1)
    w = window_weights(int(ev[i]), total, majority, pi_house)
    by = pm[:, :len(w)] @ w
    return fh, float((by * post).sum()), float((by * pri).sum())


def W_montecarlo(mu, s_unit, ev, s_d, total, majority, tails, draws, seed=12345, pi_house=0.5, weights=None, chunk=200000):
    """W_i for every unit at once by importance sampling: draw (delta, eps) from the prior, then weight
    each draw, for unit i, by the likelihood of v_i = 1/2 given delta (the eps of the other units are
    independent of it). Returns (W, se, ess) arrays over units. A method unlike the pipeline's grid."""
    rng = np.random.default_rng(seed)
    mu, s_unit, ev = np.asarray(mu, float), np.asarray(s_unit, float), np.asarray(ev, int)
    U = len(mu)
    W = np.zeros(U)
    se = np.zeros(U)
    ess = np.zeros(U)
    acc_num = np.zeros(U)
    acc_den = np.zeros(U)
    acc_num2 = np.zeros(U)
    acc_den2 = np.zeros(U)
    acc_cross = np.zeros(U)
    done = 0
    while done < draws:
        m = min(chunk, draws - done)
        delta = rng.normal(0.0, s_d, m)
        if tails == "normal":
            eps = rng.normal(0.0, 1.0, (m, U)) * s_unit
        else:
            eps = rng.standard_t(4, (m, U)) * (s_unit / SQRT2)
        v = mu + delta[:, None] + eps
        won = v > 0.5
        E_all = won @ ev
        for i in range(U):
            if tails == "normal":
                like = stats.norm.pdf(0.5 - mu[i] - delta, 0.0, s_unit[i])
            else:
                like = stats.t.pdf(0.5 - mu[i] - delta, 4, 0.0, s_unit[i] / SQRT2)
            E_rest = E_all - won[:, i] * ev[i]
            w = window_weights(int(ev[i]), total, majority, pi_house) if weights is None else np.asarray(weights, float)
            val = w[np.clip(E_rest, 0, len(w) - 1)] * (E_rest < len(w))
            acc_num[i] += (like * val).sum()
            acc_den[i] += like.sum()
            acc_num2[i] += ((like * val) ** 2).sum()
            acc_den2[i] += (like ** 2).sum()
            acc_cross[i] += (like * like * val).sum()
        done += m
    N = draws
    W = acc_num / acc_den
    # delta-method standard error of a ratio estimator
    mn, md = acc_num / N, acc_den / N
    vn = acc_num2 / N - mn ** 2
    vd = acc_den2 / N - md ** 2
    cv = acc_cross / N - mn * md
    var = (vn - 2 * W * cv + W ** 2 * vd) / (md ** 2 * N)
    se = np.sqrt(np.maximum(var, 0.0))
    ess = acc_den ** 2 / np.maximum(acc_den2, 1e-300)
    return W, se, ess


# ------------------------------------------------------------------------------------------ the data
def load_json(path):
    with open(path) as f:
        return json.load(f)


def president_files():
    return [os.path.join(DATA, "president", f"{y}.json") for y in range(1976, 2025, 4)]


def congress_files(level):
    return [os.path.join(DATA, level, f"{y}.json") for y in range(2006, 2025, 2)]


D_LABELS = {"D", "DEM", "DFL", "DNL", "DEMOCRAT", "DEMOCRATIC", "DEMOCRATIC-FARMER-LABOR",
            "DEMOCRATIC-NONPARTISAN LEAGUE", "DEMOCRATIC-NPL"}
R_LABELS = {"R", "REP", "REPUBLICAN"}


def major_party(label):
    """'D', 'R' or None from a party label as the record prints it (the same reading as the builder's:
    fusion lines split on '/' and ',', write-in lines ignored)."""
    import re
    for part in re.split(r"[/,]", label or ""):
        q = part.strip().rstrip("*").upper()
        if q.startswith("W(") or q.startswith("WRITE"):
            continue
        if q in D_LABELS:
            return "D"
        if q in R_LABELS:
            return "R"
    return None


def dem_share(contest):
    """The Democrat's share of the two leading candidates' vote, from the record; None if the top two
    are not one Democrat and one Republican (an independent who caucuses with the Democrats counts as
    the Democrat, as the builder has it)."""
    tp = contest["two_party"]
    names, votes = tp["candidates"], tp["votes"]
    cands = {c["name"]: c for c in contest["result"]["candidates"]}
    caucus = set(contest.get("ballot", {}).get("caucus_D") or [])
    parties = []
    for nm in names:
        c = cands.get(nm)
        p = major_party(c["party"]) if c else None
        if p is None and nm in caucus:
            p = "D"
        parties.append(p)
    if sorted(parties) != ["D", "R"]:
        return None
    d = votes[parties.index("D")]
    return d / sum(votes)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(url, name, expected_sha256=None):
    """curl -sSL into the cache outside the repository (briefs/_COMMON.md 6); the file's hash is checked
    against the one the data worker recorded where one is given."""
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, name)
    if not os.path.exists(path):
        subprocess.run(["curl", "-sSL", "-o", path, url], check=True)
    h = sha256(path)
    if expected_sha256 and h != expected_sha256:
        raise SystemExit(f"{name}: sha256 {h} differs from the recorded {expected_sha256}")
    return path, h


def git_head():
    out = subprocess.run(["git", "-C", ROOT, "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
    return out.stdout.strip()


def fmt(x, d=4):
    if x is None:
        return "none"
    if x == 0:
        return "0"
    return f"{x:.{d}g}"


def one_in(p):
    return f"1 in {1 / p:,.0f}" if p and p > 0 else "never"


def all_others_pmf_fft(qmat, ev, length=None):
    """For every unit i at once: P(the OTHER units give A exactly E electoral votes), from the units' win
    chances qmat (nodes, U) at each quadrature node, by characteristic functions: the generating function
    of E without unit i is the product over j != i of (1 - q_j + q_j z^{e_j}), formed on the unit circle as
    prefix and suffix products and inverted by the FFT. Returns (U, nodes, length). A method unlike the
    pipeline's dynamic programme (and unlike numpy.convolve)."""
    qmat = np.atleast_2d(np.asarray(qmat, float))
    ev = np.asarray(ev, int)
    G, U = qmat.shape
    total = int(ev.sum())
    if length is None:
        length = 1
        while length < total + 1:
            length *= 2
    freqs = np.fft.rfftfreq(length) * 2 * np.pi                  # theta_k = 2 pi k / length
    z = np.exp(-1j * np.outer(ev, freqs))                       # (U, F): z^{e_j}, the sign of numpy.fft.rfft
    factors = (1.0 - qmat)[:, :, None] + qmat[:, :, None] * z[None, :, :]   # (G, U, F)
    ones = np.ones((G, 1, factors.shape[2]), dtype=complex)
    prefix = np.concatenate([ones, np.cumprod(factors, axis=1)[:, :-1, :]], axis=1)
    suffix = np.concatenate([np.cumprod(factors[:, ::-1, :], axis=1)[:, ::-1, :][:, 1:, :], ones], axis=1)
    cf = prefix * suffix                                          # (G, U, F) without unit j
    pmf = np.fft.irfft(cf, n=length, axis=2)                      # (G, U, length)
    pmf = np.clip(pmf, 0.0, None)
    return np.transpose(pmf, (1, 0, 2))


def W_fourier(mu, s_unit, ev, s_d, total, majority, tails, nodes=1201, pi_house=0.5, span=12.0, weights=None):
    """W_i for every unit under the swing model, by quadrature over the national swing on a fine grid
    (+-span s_d, `nodes` points, Simpson weights) and the Fourier count of the other units' electoral
    votes. Returns dict of arrays f_half, W, W_unconditional (each length U)."""
    mu, s_unit, ev = np.asarray(mu, float), np.asarray(s_unit, float), np.asarray(ev, int)
    U = len(mu)
    grid = np.linspace(-span * s_d, span * s_d, nodes)
    h = grid[1] - grid[0]
    simp = np.ones(nodes)
    simp[1:-1:2], simp[2:-1:2] = 4.0, 2.0
    simp *= h / 3.0
    prior = stats.norm.pdf(grid, 0.0, s_d)
    x = 0.5 - mu[None, :] - grid[:, None]                         # (G, U): eps_j needed for a tie in j
    if tails == "normal":
        like = stats.norm.pdf(x, 0.0, s_unit[None, :])
        qmat = stats.norm.sf(x / s_unit[None, :])
    else:
        like = stats.t.pdf(x, 4, 0.0, s_unit[None, :] / SQRT2)
        qmat = stats.t.sf(x / (s_unit[None, :] / SQRT2), 4)
    pmf = all_others_pmf_fft(qmat, ev)                             # (U, G, length)
    out = {"f_half": np.zeros(U), "W": np.zeros(U), "W_unconditional": np.zeros(U)}
    for i in range(U):
        w = window_weights(int(ev[i]), total, majority, pi_house) if weights is None else np.asarray(weights, float)
        by = pmf[i][:, :len(w)] @ w                                # (G,)
        post = prior * like[:, i]
        fh = float((simp * post).sum())
        out["f_half"][i] = fh
        out["W"][i] = float((simp * post * by).sum() / fh)
        out["W_unconditional"][i] = float((simp * prior * by).sum())
    return out
