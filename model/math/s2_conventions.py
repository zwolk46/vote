"""S2. The published conventions reconciled with ours, and the flagged examples settled.

Our convention: p = rise in A's chance of winning when a ballot for A is counted rather
than not counted, ties by the jurisdiction's rule; p ~ f_v(1/2)/(2n) with f_v the forecast
density of A's share among the n other voters.  Cited in model/MATH.md sections 2 and 3."""
import math
from common import (normal_density, t_density, p_random_voting_exact, swing_from_pmf, p_from_pmf,
                    binomial_pmf, betabinomial_pmf, normalmix_pmf, fmt, one_in, SQRT2PI)

print("=" * 78)
print("S2. PUBLISHED CONVENTIONS AND FLAGGED EXAMPLES")
print("=" * 78)

# ------------------------------------------------------------- 2.1 random voting constant
print("\n2.1 Random voting (every other voter a fair coin): the constant, by exact count")
for n in [1000, 1001, 10000, 10001]:
    pmf = lambda k, n=n: binomial_pmf(k, n, 0.5)
    sw = swing_from_pmf(pmf, n)
    p = p_from_pmf(pmf, n)
    print(f"    n={n}: swing (A-vs-B, GKT/GKBafumi 'voting power') = {sw:.6f}   sqrt(2/(pi n)) = {math.sqrt(2 / (math.pi * n)):.6f}"
          f"   p (counted-vs-not) = {p:.6f}   1/sqrt(2 pi n) = {1 / math.sqrt(2 * math.pi * n):.6f}")
print("    C(1000,500)/2^1000 =", f"{math.exp(math.lgamma(1001) - 2 * math.lgamma(501) - 1000 * math.log(2)):.6f}",
      " (GKT's printed binomial expression lacks the factor 2^-(n-1); with it, this number)")
print("    2/sqrt(pi) = 1.1284 (the extraction error in the first-pass report) is neither constant.")

# ------------------------------------------------------------- 2.2 GKT eq. (2)/(5) and the differential
print("\n2.2 GKT 2002 eq. (2) and (5): density of the DIFFERENTIAL V = v_A - v_B = 2v - 1 at zero, over n")
print("    f_V(0) = f_v(1/2)/2, so f_V(0)/n = f_v(1/2)/(2n) = our p, which is HALF of the paper's own definition")
print("    (power = P(A wins | vote A) - P(A wins | vote B) = the swing ~ f_v(1/2)/n). Under random voting:")
n = 10001
fV0 = 1.0 / (SQRT2PI * (1.0 / math.sqrt(n)))        # sd of the differential V_bar is 1/sqrt(n)
print(f"    n={n}: f_V(0)/n = {fV0 / n:.6f} = 1/sqrt(2 pi n) = {1 / math.sqrt(2 * math.pi * n):.6f}; the exact swing beside it in the paper is sqrt(2/(pi n)) = {math.sqrt(2 / (math.pi * n)):.6f}")
print("    GKT eq. (6), 1/(n sd(V)), drops the constant 1/sqrt(2 pi) = 0.399 as well (a proportionality).")

# ------------------------------------------------------------- 2.3 GKBafumi 1.84/n
print("\n2.3 Gelman, Katz & Bafumi 2004, p. 663: '10,000 voters, forecast 52% with standard error 3%'")
printed_expr = (1 / (SQRT2PI * 0.03)) * math.exp(-0.5 * (0.05 / 0.03) ** 2)
from_inputs = (1 / (SQRT2PI * 0.03)) * math.exp(-0.5 * (0.02 / 0.03) ** 2)
var_slip = (1 / math.sqrt(2 * math.pi * 0.03)) * math.exp(-0.5 * (0.02 / 0.03) ** 2)
print(f"    the printed expression [1/(sqrt(2 pi) 0.03)] exp(-0.5 (0.05/0.03)^2)  = {printed_expr:.3f}   (R1's 3.316)")
print(f"    the stated inputs, distance 0.02 = 0.52 - 0.50                        = {from_inputs:.3f}   (R4's 10.65; GKB 1998 section 5 formula)")
print(f"    with 0.03 under the square root as a variance, distance 0.02           = {var_slip:.3f}   (the printed 1.84)")
print(f"    so 1.84 reproduces only by treating the 3% standard error as a variance in the normalising constant.")
print(f"    Under the stated inputs the density is {from_inputs:.2f}: event/swing {from_inputs:.2f}/n, our p {from_inputs / 2:.2f}/n = {fmt(from_inputs / 2 / 10000)} at n = 10,000.")
pe = p_from_pmf(lambda k: normalmix_pmf(k, 10000, 0.52, 0.03), 10000)
print(f"    exact p for that forecast at n = 10,000 (binomial kernel folded in): {fmt(pe)} = {pe * 10000:.3f}/n")

# ------------------------------------------------------------- 2.4 Myatt & Fisher 6n
print("\n2.4 Myatt & Fisher 2002 Lemma 1 eq. (2): Pr[x1 = x2 > x3] ~ (integral_{1/3}^{1/2} f(z,z,1-2z) dz)/(6n) as printed")
print("    Check with a uniform belief f = 2 on the simplex (every outcome of n voters equally likely):")
for n in [302, 3002, 30002]:          # n = 2 mod 3 so that x1 = x2 = x3 + 1 is possible
    cnt = sum(1 for i in range(n + 1) if 3 * i > n and 2 * i <= n)   # x1 = x2 = i, x3 = n - 2i < i
    tot = (n + 2) * (n + 1) // 2
    pr = cnt / tot
    cnt3 = 1 if (n - 2) % 3 == 0 else 0     # x1 = x2 = x3 + 1 exists iff n = 2 mod 3
    print(f"    n={n}: n Pr[x1=x2>x3] = {n * pr:.5f}  (integral of f over [1/3,1/2] = 1/3 = 0.33333; printed /6 would give 0.05556);"
          f"  n^2 Pr[x1=x2=x3+1] = {n * n * cnt3 / tot:.4f} (f(1/3,1/3,1/3) = 2)" if cnt3 else
          f"    n={n}: n Pr[x1=x2>x3] = {n * pr:.5f}  (integral = 1/3; printed /6 would give 0.05556); x1=x2=x3+1 impossible at this n")
print("    So the two-way constant is the integral over n, not over 6n; Proposition 1 and eq. (3) are as printed.")

# ------------------------------------------------------------- 2.5 GSE density and scale
print("\n2.5 Gelman, Silver & Edlin 2012: 'the density at 0 of the Student-t (4 df), mean M, scale S' of the margin in votes")
S = 1.0
print(f"    t4 density at its centre with scale S:      {t_density(0, 0, S):.4f}/S")
print(f"    t4 with standard deviation S (scale S/sqrt2): {t_density(0, 0, S / math.sqrt(2)):.4f}/S")
print(f"    normal with sd S:                            {normal_density(0, 0, S):.4f}/S")
print("    (a) with S as the t's scale parameter the centre density is 0.375/S, 0.94 of a normal's with sd S; with S")
print("        as the t's standard deviation (scale S/sqrt 2) it is 0.530/S, 1.33 of it: a spread of sqrt(2) at the centre.")
print("    (b) the margin in votes takes every second integer, so 'the density at 0' is g(0) = f_v(1/2)/(2n) = our p,")
print("        while P(exact tie) = 2 g(0). The paper does not say which it intends; as written, its figure is in our")
print("        convention; if an exact-tie probability was intended, its figures are twice ours.")

# ------------------------------------------------------------- 2.6 GKB 1998 numbers
print("\n2.6 Gelman, King & Boscardin 1998: the printed numbers, reproduced and converted")
f = normal_density(0.5, 0.515, 0.056)
print(f"    popular vote 1992: normal mean 51.5%, sd 5.6%, 92 million voters: f(1/2) = {f:.4f}; f/n = {fmt(f / 92e6)} = {one_in(f / 92e6)} (paper: 1 in 13.3 million; an exact tie, no 1/2)")
print(f"      under our convention p = f/(2n) = {fmt(f / 184e6)} = {one_in(f / 184e6)}")
f2 = normal_density(0.5, 0.5, 0.02)
print(f"    section 5 bound, tau = 2%, mu = 1/2: f(1/2) = {f2:.3f} -> '20/n' (event); ours 10/n; at n = 200,000: event {fmt(f2 / 2e5)} ('1 in 10,000'), ours {fmt(f2 / 4e5)}")
rough = (0.18 / 0.04) * 0.5 * (2 / 11) * (1 / 50)
print(f"    section 5 rough presidential: (.18/.04) x 1/2 x (2/11) x (e/50) = {rough:.5f} e/n (printed .008 e/n); e = 10, n = 2,000,000: {fmt(rough * 10 / 2e6)} = {one_in(rough * 10 / 2e6)} (printed 1 in 25 million)")
print("      here the 1/2 is explained as 'casting a vote, not switching a preference', i.e. OUR half, so this rough")
print("      figure is already in our convention; the model computation (eqs. 1-3) has no state-level half and is twice ours.")

# ------------------------------------------------------------- 2.7 Mulligan & Hunter
print("\n2.7 Mulligan & Hunter (NBER WP 8590): eq. (3) f(1/2)/(v+1) is P(tie | v even) = the EVENT, twice our p")
print(f"    f(1/2) from Figure 5: (1/6000)(2/3)(20001) = {(1 / 6000) * (2 / 3) * 20001:.3f} (printed '~ 2'); uniform A on [0.25,0.75] gives f = 2 exactly")
print("    eq. (4): P(pivot election) ~ 1.5 f/(v+1) (parity-averaged: f/(v+1) for v even, 2f/(v+1) for v odd)")
print("    'pivotal vote' frequency = f/(v+1): all v ballots in a tie, half of them in a one-vote win.  Ours: f/(2(v+1)).")
print("    '2/v' per ballot (f = 2) is therefore 1/v in our convention; '1 in 89,000' is 1 in 178,000.")
# footnote 14
v, A = 100000, 0.61
log10_normal = (-0.5 * (v * (A - 0.5)) ** 2 / (v * A * (1 - A)) - 0.5 * math.log(2 * math.pi * v * A * (1 - A))) / math.log(10)
log10_exact = (math.lgamma(v + 1) - 2 * math.lgamma(v / 2 + 1) + (v / 2) * (math.log(A) + math.log(1 - A))) / math.log(10)
print(f"    footnote 14, v = 100,000, A = 0.61: normal-density value 10^{log10_normal:.1f} (printed 10^-1108); exact binomial 10^{log10_exact:.1f}")

# ------------------------------------------------------------- 2.8 EGK and Barnett
print("\n2.8 Edlin, Gelman & Kaplan 2007 and Barnett 2020 are in our convention")
print("    EGK: differential uniform on +-6% -> f_V(0) = 1/0.12 = 8.33; p = f_V(0)/n = 1/(0.12 n), stated to be 'half the")
print("        probability that a single vote can make or break an exact tie'. Share density f_v(1/2) = 1/0.06 = 16.7;")
print(f"        ours f_v/(2n) = {16.6667 / 2:.2f}/n = 1/(0.12 n). K = 10 is a differential uniform on +-5%: {1 / 0.10:.0f}/n. Check at n = 1,000,000: {fmt(1 / (0.12 * 1e6))}.")
print("    Barnett: EB = (1/2) B d with d = P(the one tie event possible for the parity) ~ f_v(1/2)/n, so (1/2) d = our p;")
print("        his bound d >= 1/N (two candidates each with at least a 10% chance, the others all voting, N large) is p >= 1/(2N).")
print(f"        His $134.92 = (1/2)(33e9)/122,293,322 = {0.5 * 33e9 / 122293322:.2f}.")

# ------------------------------------------------------------- 2.9 the table
print("\n2.9 Summary: what each source's printed p is, in our convention (multiply by the factor)")
rows = [
    ("Gelman, King & Boscardin 1998, eqs. 1-3 (model)", "event f/n at the state; 1/2 only on an EV tie", "x 1/2"),
    ("  same paper, section 5 rough .008 e/n and 20/n", "1/2 for casting in the rough formula; 20/n is the event", "rough: x 1; 20/n: x 1/2"),
    ("Gelman, Katz & Tuerlinckx 2002, definition and exact count", "swing = P(win|A) - P(win|B)", "x 1/2"),
    ("  same paper, eqs. (2), (5) as printed", "density of the differential over n = f_v/(2n)", "x 1 (inconsistent with its definition by 2)"),
    ("Gelman, Katz & Bafumi 2004, eq. (2), sqrt(2/pi)/sqrt(n), 1.84/n", "swing", "x 1/2 (and 1.84 -> 10.65)"),
    ("Gelman, Silver & Edlin 2012", "density at 0 of the margin in votes (t4)", "x 1 as written; x 1/2 if an exact tie was meant; centre scale spread sqrt(2)"),
    ("Edlin, Gelman & Kaplan 2007, p = K/n, 1/(0.12 n)", "coin-flip halved", "x 1"),
    ("Barnett 2020, EB = (1/2) B d", "d = event; the 1/2 is outside", "(1/2) d = p, x 1"),
    ("Mulligan & Hunter 2003, f(1/2)/(v+1), 2/v, 1 in 89,000", "pivotal-ballot frequency = event", "x 1/2"),
]
for a, b, c in rows:
    print(f"    {a:<62} {b:<48} {c}")
