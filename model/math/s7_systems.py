"""S7. R4's stylised calculations for other electoral systems (research/electoral-systems-v2.md), re-run
verbatim from r4/, then checked by a different route where one exists. Cited in model/MATH.md section 7."""
import math
import os
import subprocess
import sys
import numpy as np
from common import binomial_pmf, betabinomial_pmf, p_from_pmf, normal_density, fmt, one_in

HERE = os.path.dirname(os.path.abspath(__file__))
R4 = os.path.join(HERE, "r4")
sys.path.insert(0, R4)

print("=" * 78)
print("S7. OTHER ELECTORAL SYSTEMS: R4'S CALCULATIONS RE-RUN AND CHECKED")
print("=" * 78)

# ------------------------------------------------------------------ 7.1 verbatim re-runs
print("\n7.1 R4's seven scripts, copied verbatim (r4/README.md), re-run here. Their output follows each name.")
for name in ["plur.py", "plur3.py", "pr.py", "pr_check.py", "ref.py", "ref2.py", "chamber.py"]:
    print(f"\n--- r4/{name} ---")
    out = subprocess.run([sys.executable, name], cwd=R4, capture_output=True, text=True)
    print(out.stdout.rstrip())
    if out.returncode != 0:
        print("STDERR:", out.stderr.rstrip())

from plur import two_cand, three_cand          # noqa: E402  (R4's exact lattice sums)
from ref import Q as ref_Q                     # noqa: E402

# ------------------------------------------------------------------ 7.2 plurality with three candidates
print("\n7.2 Plurality, three candidates, KNOWN shares: the top-two tie has the difference x1 - x2 with variance")
print("    n (p1 + p2), so Q ~ 1/sqrt(2 pi n (p1 + p2)) = two-way Q / sqrt(p1 + p2) (when the third is out of reach).")
for N in [1000, 10000]:
    q2 = two_cand(N, (0.5, 0.5))
    for mu in [(0.45, 0.45, 0.10), (0.40, 0.40, 0.20), (1 / 3, 1 / 3, 1 / 3)]:
        Q = three_cand(N, mu, None)
        pred = q2 / math.sqrt(mu[0] + mu[1])
        print(f"    N={N} shares {tuple(round(m, 3) for m in mu)}: R4 exact Q1 = {Q[0]:.6g}; two-way/sqrt(p1+p2) = {pred:.6g}; ratio {Q[0] / pred:.4f}")
print("    Sound; at equal thirds the match includes three-way ties and shared wins, by the same count.")

print("\n7.3 Plurality, three candidates, Dirichlet forecast (kappa = 400): the continuous route.")
print("    Candidate 1 can tie with either rival j. For the pair (1, j): s = v1 + vj ~ Beta(kappa(mu1+muj), kappa mu_k)")
print("    and r = v1/(v1+vj) ~ Beta(kappa mu1, kappa muj), independent; D = v1 - vj = s(2r - 1) has density")
print("    f_D(0) = f_r(1/2) E[1[s > 2/3]/(2s)] (the third must be below the tied pair, 1 - s < s/2). Q1 ~ sum_j f_D(0)/n,")
print("    with the count noise (sd sqrt(s/n) in D) folded in by a normal approximation.")


def beta_pdf(x, a, b):
    return math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + (a - 1) * math.log(x) + (b - 1) * math.log1p(-x))


def pair_density(mu, j, kappa):
    k = 3 - j                      # the third candidate's index (candidate 0 against j)
    a_r, b_r = kappa * mu[0], kappa * mu[j]
    a_s, b_s = kappa * (mu[0] + mu[j]), kappa * mu[k]
    fr = beta_pdf(0.5, a_r, b_r)
    sg = np.linspace(2 / 3 + 1e-9, 1 - 1e-9, 1001)
    fs = np.array([beta_pdf(x, a_s, b_s) for x in sg])
    fD0 = fr * np.trapezoid(fs / (2 * sg), sg)
    sbar = a_s / (a_s + b_s)
    sd_r = math.sqrt(a_r * b_r / ((a_r + b_r) ** 2 * (a_r + b_r + 1)))
    return fD0, sbar, 2 * sbar * sd_r


for mu in [(0.40, 0.38, 0.22), (0.45, 0.45, 0.10), (0.36, 0.34, 0.30)]:
    kappa = 400
    terms = [pair_density(mu, j, kappa) for j in (1, 2)]
    for N in [1000, 10000]:
        Q = three_cand(N, mu, kappa)
        cont = sum(fD0 * sd_D / math.sqrt(sd_D ** 2 + sbar / N) for fD0, sbar, sd_D in terms)
        print(f"    shares {mu}, N={N}: f_D(0) for rivals 2, 3 = {terms[0][0]:.3f}, {terms[1][0]:.3f}; continuous N Q1 ~ {cont:.3f};"
              f" R4 exact N Q1 = {N * Q[0]:.3f}; ratio {cont / (N * Q[0]):.3f}")
print("    Sound to within the normal approximation of the count noise (within 5% at N = 1,000, under 1% at 10,000).")
print("    Note the lattice: with a third candidate x1 - x2 takes EVERY integer, so both the tie and the one-short")
print("    event occur for either parity and Q ~ f_D(0)/n, with no further 1/2; in the two-way case f_D(0) = f_v(1/2)/2.")

# ------------------------------------------------------------------ 7.4 list PR
print("\n7.4 List PR, 'about M/N': two parties under D'Hondt, exact. Q = E[seats_1(X+1) - seats_1(X)] with X the")
print("    count for party 1 among N others, v ~ Beta(kappa mu, kappa(1-mu)). If E[seats_1] ~ M v over the forecast's")
print("    spread, Q ~ (M/N) dE[seats]/d(M v) = M/N. Ties at the last seat by lot (1/2).")


def dhondt_two(k, N, M):
    """seats of party 1 with k votes against N - k, D'Hondt, M seats; last-seat tie counts 1/2."""
    q1 = [(k / s, 1) for s in range(1, M + 1)]
    q2 = [((N - k) / s, 2) for s in range(1, M + 1)]
    allq = sorted(q1 + q2, key=lambda t: -t[0])
    cut = allq[M - 1][0]
    sure = sum(1 for q, w in allq if q > cut and w == 1)
    tied1 = sum(1 for q, w in allq if q == cut and w == 1)
    tied = sum(1 for q, w in allq if q == cut)
    need = M - sum(1 for q, w in allq if q > cut)
    return sure + (need * tied1 / tied if tied else 0.0)


for (N, M, mu0) in [(4000, 27, 0.30), (4000, 27, 0.10), (50000, 5, 0.35), (50000, 5, 0.05)]:
    seats = [dhondt_two(k, N, M) for k in range(N + 2)]
    for kappa in [400, 100000]:
        Q = sum(betabinomial_pmf(k, N, kappa, mu0) * (seats[k + 1] - seats[k]) for k in range(N + 1))
        sd = math.sqrt(mu0 * (1 - mu0) / (kappa + 1))
        print(f"    N={N:,} M={M} mu={mu0} kappa={kappa} (sd {sd:.4f}, i.e. {sd * M:.2f} seats): Q = {fmt(Q)}; M/N = {fmt(M / N)}; Q/(M/N) = {Q / (M / N):.3f}")
print("    Sound as 'about M/N' when the forecast spans half a seat or more (sd x M >~ 0.4 above); when it spans a")
print("    tenth of a seat or less, Q is whatever the staircase does at the mean, from 0 to 2.7 x M/N above.")
print("    R4's pr.py (five parties, Poisson counts) finds Q_j/(M/N) from 0.70 to 0.99 where M is 27 or 150, and")
print("    from 0.00 to 0.91 where M is 5 or 10: the same pattern. A seat is not an outcome in the site's sense, so")
print("    'M/N' is the chance one ballot moves one seat, not the chance it changes a winner.")

# ------------------------------------------------------------------ 7.5 referendums
print("\n7.5 Referendum with a threshold t on the Yes share. Z = (1 - t) Y - t X decides (pass iff Z >= 0); a Yes ballot")
print("    adds (1 - t) to Z, a No ballot subtracts t, so with g the density of Z at 0: Q_yes ~ (1 - t) g, Q_no ~ t g,")
print("    Q_no / Q_yes = t / (1 - t): 1.5 at t = 0.6 and 2 at t = 2/3. R4's ref2.py (averaged over N):")
from ref2 import Qavg            # noqa: E402
for mu0 in [0.60, 0.667]:
    for t in [0.6, 2 / 3]:
        y, n_ = Qavg(10000, mu0, 400, t)
        print(f"    forecast Yes {mu0}, t = {t:.3f}: Q_no/Q_yes = {n_ / y:.3f} (t/(1-t) = {t / (1 - t):.3f})")
print("    At a FIXED N the pass condition Y >= t N sits on the lattice of Y, and whether a Yes or a No ballot can cross")
print("    it depends on the fractional part of t N: t = 0.6, forecast Yes 0.60, N = 10,000 to 10,004 (R4's ref.py Q):")
for N in range(10000, 10005):
    y, n_ = ref_Q(N, 0.60, 400, 0.6)
    print(f"      N = {N}: t N = {0.6 * N:.1f}; Q_yes = {fmt(y)}; Q_no = {fmt(n_)}")
print("    The ex ante N is uncertain by far more than five, so the average over N is the right ex ante quantity and")
print("    R4's averaging is legitimate; the fixed-N values are artefacts of an exactly known turnout.")

# ------------------------------------------------------------------ 7.6 quorum
print("\n7.6 A turnout quorum (STRUCTURE, with a stylised number). Let the proposal fail unless turnout T >= q R")
print("    (R registered). A ballot can change the outcome in two ways: the ordinary tie among those who vote, and")
print("    completing the quorum when T would have fallen one short. Ex ante, with f_T the density of the turnout")
print("    share at q (over R) and P(pass | quorum met) the chance the vote itself passes:")
print("      Q_yes ~ f_v(1/2)/(2N) x P(quorum met | tie)  +  f_T(q)/R x P(pass | quorum met, T = qR)")
print("      Q_no  ~ f_v(1/2)/(2N) x P(quorum met | tie)  -  f_T(q)/R x P(pass | quorum met, T = qR)   (a No ballot that")
print("              completes the quorum HELPS the proposal; a No voter who wants it to fail should abstain).")
R, N = 1_000_000, 520_000
fT = normal_density(0.50, 0.52, 0.03)
fv = normal_density(0.5, 0.56, 0.04)
print(f"    Stylised: R = {R:,}, turnout forecast 52% (sd 3), q = 50%; Yes share forecast 56% (sd 4), P(pass | quorum) = 0.93:")
print(f"      tie term f_v(1/2)/(2N) = {fmt(fv / (2 * N))}; quorum term f_T(q)/R x 0.93 = {fmt(fT / R * 0.93)}: the quorum term is {fT / R * 0.93 / (fv / (2 * N)):.1f} x the tie term.")
print("    No published counterpart was read; R4 gave structure only, and so does this.")

# ------------------------------------------------------------------ 7.7 tiny electorates
print("\n7.7 Tiny electorates: exact binomial at a known 50-50 split (R4's ref.py, S1.4):")
for N in [9, 19, 29, 99]:
    pe = p_from_pmf(lambda k: binomial_pmf(k, N, 0.5), N)
    print(f"    N = {N}: exact p = {pe:.4f}; 1/sqrt(2 pi N) = {1 / math.sqrt(2 * math.pi * N):.4f} ({100 * (1 / math.sqrt(2 * math.pi * N) / pe - 1):.1f}% high)")
print("    Sound; the exact lattice sum is the model's own below a few hundred voters (the approximation is 8% high at N = 9).")

# ------------------------------------------------------------------ 7.8 runoff, IRV, STV
print("\n7.8 Runoff, IRV, STV: R4 made no calculation, and reports Baltz's closed forms as unreliable against exact")
print("    counts (1/2 to 1/21 of exact). Structure only: a two-round runoff gives p = p(first round settles it or")
print("    sets the pair) + sum over pairs P(pair) x p(final | pair); IRV sums over elimination orders; STV over")
print("    quotas and transfers. Each term is a two-way p of the kind in S1 with the pair's conditional forecast, so")
print("    the model can compute them by enumeration for small N and by simulation otherwise; nothing here is")
print("    offered as the model's own number.")

# ------------------------------------------------------------------ 7.9 chamber
print("\n7.9 Chamber: R4's chamber.py reports P(other 434 seats give exactly 217) without conditioning on the tied")
print("    seat (its 'P(tip | seat tied)' is the unconditional P(217)); S4.4 shows the conditional one. Its magnitude")
print("    (1 in 39 to 1 in 93 at m0 = 0) agrees with S4.4's unconditional column (0.015 to 0.022 at rho 0.3-0.7).")
print("    Its rows are a function of three random draws of 434 seat means (seed 0, 1, 2), as R4's note says.")

print("\n7.10 Verdicts: sound enough for the model's own use: two-way exact (7.7), plurality-3 (7.2, 7.3), list PR as")
print("     'about M/N' when the forecast spans a seat (7.4), referendum thresholds with N averaged (7.5). Structure")
print("     only, no number: quorum (7.6), runoff/IRV/STV (7.8). Chamber: use the conditional form (7.9, S4.4).")
