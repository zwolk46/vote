"""Shared mathematics for the M1 check (Python 3 standard library plus numpy).

Definitions used everywhere in model/MATH.md and these scripts:

  n      the number of OTHER voters (your ballot excluded); they all vote A or B.
  X      the number of them who vote A; M = 2X - n is A's margin among them.
  v      a share: X/n once realised, or the forecast share before the election.
  W(M)   the probability that A wins given the others' margin M, under a tie rule:
           lot:   W = 1 if M > 0, 1/2 if M = 0, 0 if M < 0
           A:     W = 1 if M >= 0 else 0        (a tie goes to A)
           B:     W = 1 if M > 0 else 0         (a tie goes to B)
           pi:    W = 1 if M > 0, pi if M = 0, 0 if M < 0   (a tie is settled by a
                  new election or a body, and A's chance in that settlement is pi)
  p      the quantity the site needs: the rise in A's chance of winning when your
         ballot for A is counted rather than not counted, everyone else unchanged:
             p = sum_M P(M) [W(M + 1) - W(M)].
  swing  the rise when your ballot for A replaces a ballot for B (A-versus-B):
             swing = sum_M P(M) [W(M + 1) - W(M - 1)].

The distributions of X offered here:
  binomial(n, v0)                 every other voter votes A with a KNOWN chance v0
  betabinomial(n, kappa, mu)      v ~ Beta(kappa mu, kappa (1 - mu)), X | v ~ Bin(n, v)
  normalmix(n, mu, tau)           v ~ Normal(mu, tau^2) truncated to (0, 1), X | v ~ Bin(n, v)
  tmix(n, mu, s, df)              v ~ Student-t(df) with centre mu and scale s, X | v ~ Bin
All four are exact to numerical precision (the mixtures are integrated on a fine grid of v).
"""
import math
import numpy as np

SQRT2PI = math.sqrt(2.0 * math.pi)


# ---------------------------------------------------------------- exact pmfs

def log_binom_pmf(k, n, v):
    """log P(X = k) for X ~ Bin(n, v); k may be an int, v an array in (0, 1)."""
    v = np.asarray(v, dtype=float)
    return (math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
            + k * np.log(v) + (n - k) * np.log1p(-v))


def binomial_pmf(k, n, v0):
    if k < 0 or k > n:
        return 0.0
    return float(np.exp(log_binom_pmf(k, n, v0)))


def betabinomial_pmf(k, n, kappa, mu):
    """P(X = k) with v ~ Beta(a, b), a = kappa mu, b = kappa (1 - mu). Closed form."""
    if k < 0 or k > n:
        return 0.0
    a, b = kappa * mu, kappa * (1.0 - mu)
    lg = (math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
          + math.lgamma(k + a) + math.lgamma(n - k + b) - math.lgamma(n + a + b)
          + math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b))
    return math.exp(lg)


def _grid(mu, width, m=200001):
    lo = max(1e-9, mu - width)
    hi = min(1 - 1e-9, mu + width)
    return np.linspace(lo, hi, m)


def normalmix_pmf(k, n, mu, tau, m=200001):
    """P(X = k) with v ~ N(mu, tau^2) truncated to (0,1), X | v ~ Bin(n, v); grid integral."""
    if k < 0 or k > n:
        return 0.0
    v = _grid(mu, 12 * tau, m)
    w = np.exp(-0.5 * ((v - mu) / tau) ** 2)
    w /= np.trapezoid(w, v)
    return float(np.trapezoid(np.exp(log_binom_pmf(k, n, v)) * w, v))


def tmix_pmf(k, n, mu, s, df=4, m=400001):
    """P(X = k) with v ~ t_df(centre mu, scale s) truncated to (0,1), X | v ~ Bin(n, v)."""
    if k < 0 or k > n:
        return 0.0
    v = _grid(mu, 0.5, m)
    w = (1.0 + ((v - mu) / s) ** 2 / df) ** (-(df + 1) / 2.0)
    w /= np.trapezoid(w, v)
    return float(np.trapezoid(np.exp(log_binom_pmf(k, n, v)) * w, v))


# ------------------------------------------------------------- p and swing

def p_from_pmf(pmf, n, rule="lot", pi=0.5):
    """p = sum_M P(M) [W(M+1) - W(M)] for a pmf(k) of X = number of A votes among n others.
    Only M = 0 (k = n/2, n even) and M = -1 (k = (n-1)/2, n odd) can contribute."""
    if n % 2 == 0:
        P0 = pmf(n // 2)            # others tied
        Pm1 = 0.0
    else:
        P0 = 0.0
        Pm1 = pmf((n - 1) // 2)     # A one short
    if rule == "lot":
        pi = 0.5
    elif rule == "A":
        pi = 1.0
    elif rule == "B":
        pi = 0.0
    elif rule == "pi":
        pass
    else:
        raise ValueError(rule)
    # W(1) - W(0) = 1 - pi at M = 0;  W(0) - W(-1) = pi - 0 at M = -1
    return (1.0 - pi) * P0 + pi * Pm1


def swing_from_pmf(pmf, n, rule="lot", pi=0.5):
    """swing = sum_M P(M) [W(M+1) - W(M-1)]: contributions at M = 0 and M = +-1."""
    if rule == "lot":
        pi = 0.5
    elif rule == "A":
        pi = 1.0
    elif rule == "B":
        pi = 0.0
    if n % 2 == 0:
        return pmf(n // 2) * 1.0               # M = 0: W(1) - W(-1) = 1
    k = (n - 1) // 2
    # M = -1 (k A votes): W(0) - W(-2) = pi ;  M = +1 (k+1 A votes): W(2) - W(0) = 1 - pi
    return pi * pmf(k) + (1.0 - pi) * pmf(k + 1)


# --------------------------------------------------------- approximations

def normal_density(x, mu, sd):
    return math.exp(-0.5 * ((x - mu) / sd) ** 2) / (SQRT2PI * sd)


def t_density(x, mu, s, df=4):
    c = math.gamma((df + 1) / 2.0) / (math.gamma(df / 2.0) * math.sqrt(df * math.pi) * s)
    return c * (1.0 + ((x - mu) / s) ** 2 / df) ** (-(df + 1) / 2.0)


def p_density_approx(n, f_half):
    """p ~ f(1/2) / (2 n): the forecast density of the share at one half over twice the voters."""
    return f_half / (2.0 * n)


def p_convolved_normal(n, mu, tau):
    """The same with the binomial noise folded in: sd^2 = tau^2 + 1/(4n); exact as tau -> 0."""
    sd = math.sqrt(tau ** 2 + 0.25 / n)
    return normal_density(0.5, mu, sd) / (2.0 * n)


def p_random_voting_exact(n):
    """Known 50-50 shares: p = (1/2) C(n, n/2) / 2^n (n even) or (1/2) C(n, (n-1)/2) / 2^n (n odd)."""
    k = n // 2 if n % 2 == 0 else (n - 1) // 2
    return 0.5 * math.exp(math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1) - n * math.log(2))


def fmt(x, d=4):
    if x == 0:
        return "0"
    return f"{x:.{d}g}"


def one_in(x):
    return f"1 in {1.0 / x:,.0f}" if x > 0 else "never"
