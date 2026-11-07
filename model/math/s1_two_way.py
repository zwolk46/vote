"""S1. The two-way race, exactly: p under each tie rule, and the two standard approximations.

Everything printed here is cited in model/MATH.md section 1."""
import math
import sys
from common import (binomial_pmf, betabinomial_pmf, normalmix_pmf, tmix_pmf, p_from_pmf,
                    swing_from_pmf, normal_density, t_density, p_density_approx,
                    p_convolved_normal, p_random_voting_exact, fmt, one_in)

print("=" * 78)
print("S1. THE TWO-WAY RACE, EXACTLY")
print("=" * 78)

# ---------------------------------------------------------------- 1.1 tie rules
print("\n1.1 p under each tie rule, exact, for a Beta-binomial forecast (kappa = 400, mu = 0.51)")
print("    n = other voters. p = sum_M P(M)[W(M+1) - W(M)]. 'pi' = a tie is settled by a new election")
print("    or a body in which A's chance is pi (here pi = 0.3). 'A' and 'B' = the tie goes to that side.")
print(f"{'n':>8} {'parity':>6} {'lot':>11} {'A':>11} {'B':>11} {'pi=0.3':>11} {'f/(2n)':>11} {'swing(lot)':>11}")
for n in [1000, 1001, 10000, 10001, 100000, 100001]:
    pmf = lambda k, n=n: betabinomial_pmf(k, n, 400, 0.51)
    # exact Beta density of the share at one half
    a, b = 400 * 0.51, 400 * 0.49
    f_half = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + (a - 1) * math.log(0.5) + (b - 1) * math.log(0.5))
    vals = [p_from_pmf(pmf, n, r) for r in ("lot", "A", "B")] + [p_from_pmf(pmf, n, "pi", 0.3)]
    print(f"{n:>8} {'even' if n % 2 == 0 else 'odd':>6} " + " ".join(f"{fmt(v):>11}" for v in vals)
          + f" {fmt(p_density_approx(n, f_half)):>11} {fmt(swing_from_pmf(pmf, n)):>11}")
print("    Reading: under a lot, p is the same for either parity and equals f(1/2)/(2n) to the")
print("    approximation's accuracy. Under a deterministic rule p is 0 for one parity and f(1/2)/n for")
print("    the other; the average over the two parities is again f(1/2)/(2n), for any pi.")

# ------------------------------------------------- 1.2 the lattice and the two densities
print("\n1.2 The two standard approximations and their constants (normal forecast of the share, mean mu, sd tau)")
print("    (a) share density: P(M = 0 or M = -1 event) ~ f_v(1/2)/n ; p ~ f_v(1/2)/(2n)")
print("    (b) margin density: the margin in votes m = 2X - n has density g(0) = f_v(1/2)/(2n) at zero,")
print("        and takes every SECOND integer, so P(m = 0) ~ 2 g(0) = f_v(1/2)/n, and p = g(0) exactly")
print("        the density of the margin in votes at zero (nothing more).")
for (mu, tau, n) in [(0.5, 0.03, 10000), (0.52, 0.03, 10000), (0.5, 0.02, 200000), (0.515, 0.056, 92_000_000)]:
    f_half = normal_density(0.5, mu, tau)
    p_exact = p_from_pmf(lambda k: normalmix_pmf(k, n, mu, tau), n)
    print(f"    mu={mu} tau={tau} n={n:,}: f_v(1/2)={f_half:.4f}  event f/n={fmt(f_half / n)}  "
          f"p=f/(2n)={fmt(f_half / (2 * n))}  exact p={fmt(p_exact)}  ratio exact/approx={p_exact / (f_half / (2 * n)):.4f}")

# ------------------------------------------------- 1.3 error of the density approximation
print("\n1.3 Relative error of p ~ f(1/2)/(2n) and of the convolved form sd^2 = tau^2 + 1/(4n), exact p as the reference")
print("    (normal forecast, mu = 0.50 unless shown; the exact p integrates the binomial kernel over the forecast)")
print(f"{'n':>9} {'tau':>6} {'mu':>6} {'exact p':>11} {'f/(2n)':>11} {'err %':>8} {'convolved':>11} {'err %':>8}")
for n in [100, 300, 1000, 3000, 10000, 100000, 1000000]:
    for tau in [0.01, 0.03, 0.10]:
        for mu in [0.50, 0.55]:
            if mu == 0.55 and tau == 0.01:
                continue
            pe = p_from_pmf(lambda k: normalmix_pmf(k, n, mu, tau), n)
            pa = p_density_approx(n, normal_density(0.5, mu, tau))
            pc = p_convolved_normal(n, mu, tau)
            print(f"{n:>9} {tau:>6} {mu:>6} {fmt(pe):>11} {fmt(pa):>11} {100 * (pa / pe - 1):>8.1f} {fmt(pc):>11} {100 * (pc / pe - 1):>8.1f}")
print("    Reading: at mu = 1/2 the error of f/(2n) is +1/(8 n tau^2) to first order (the binomial noise widens the")
print("    forecast by sd^2 -> tau^2 + 1/(4n)): 12.5% at n tau^2 = 1, 4.6% at 2.7, 1.4% at 9, 0.1% at 100. Off centre")
print("    the sign reverses (the widening lifts a tail). The convolved form is within 1% everywhere in the table.")
print("    First-order thresholds: within 2% once n tau^2 > 6.25, within 10% once n tau^2 > 1.25; n tau^2 > 6.25 means")
print("    the forecast's spread in votes, n tau, is at least 5 times the count noise sqrt(n)/2.")

# ------------------------------------------------- 1.4 known share
print("\n1.4 A KNOWN share (no forecast uncertainty): the two regimes")
print(f"{'n':>9} {'v0':>6} {'exact p':>12} {'1/sqrt(2 pi n)':>15} {'(1/2)sqrt(2/(pi n))[4v(1-v)]^(n/2)':>36}")
for n in [9, 99, 999, 9999, 99999, 999999]:
    for v0 in [0.5, 0.51, 0.55]:
        pe = p_from_pmf(lambda k: binomial_pmf(k, n, v0), n)
        appr = 0.5 * math.sqrt(2 / (math.pi * n)) * (4 * v0 * (1 - v0)) ** (n / 2)
        print(f"{n:>9} {v0:>6} {fmt(pe):>12} {fmt(1 / math.sqrt(2 * math.pi * n)):>15} {fmt(appr):>36}")
print("    Reading: at a known 50-50 split p falls as 1/sqrt(n) (p = 1/sqrt(2 pi n), half of sqrt(2/(pi n)));")
print("    at any other known split it falls exponentially (for v0 = 0.51, n = 999,999 the factor [4v(1-v)]^(n/2) = exp(-200)).")

# ------------------------------------------------- 1.5 the t forecast
print("\n1.5 A Student-t(4) forecast instead of a normal (Gelman, Silver & Edlin's choice): centre and tails")
n = 1_000_000
for mu in [0.50, 0.52, 0.55, 0.60, 0.70]:
    tau = 0.03
    pn = p_from_pmf(lambda k: normalmix_pmf(k, n, mu, tau), n)
    s_same_sd = tau / math.sqrt(2.0)      # t4 with the same sd as the normal (sd = s sqrt(2))
    pt_sd = p_from_pmf(lambda k: tmix_pmf(k, n, mu, s_same_sd), n)
    pt_scale = p_from_pmf(lambda k: tmix_pmf(k, n, mu, tau), n)   # t4 with scale = tau
    print(f"    mu={mu}: normal(sd {tau}) p={fmt(pn)}   t4(sd {tau}) p={fmt(pt_sd)}   t4(scale {tau}) p={fmt(pt_scale)}")
print("    Reading: at the centre the three differ by at most 1.33 (t4 with sd 0.03: 0.530/sd against the normal's")
print("    0.399/sd; t4 with scale 0.03: 0.375/s, i.e. 0.94 of the normal). At mu = 0.70 the normal is 2e-10 of its")
print("    centre value, the t4 between 4e-4 and 2e-3 of its own.")
print("    GSE's District of Columbia example (normal 5e-85, t4 2e-12) is this tail difference.")

# ------------------------------------------------- 1.6 B* arithmetic
print("\n1.6 Break-even stakes B* = C / p are a rearrangement of p B > C (p > 0); with the EVENT probability")
print("    in place of p, B* is half what it should be. Example: p = 1e-7, C = $4 and $12:")
for C in (4.0, 12.0):
    print(f"    C = ${C:.0f}: B* = ${C / 1e-7:,.0f};  with the event probability 2e-7 one would print ${C / 2e-7:,.0f}")
print("    p = 1/60,000,000: C = $4 gives B* = $240,000,000 (not $230 million; $228 million needs C = $3.80).")
