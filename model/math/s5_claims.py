"""S5. Every mathematical claim in model/MODEL-DRAFT.md sections 2, 3, 7 and 8, checked.

Each block names the claim, computes what it needs, and prints the verdict used in model/MATH.md
section 5 (holds / holds under stated conditions / wrong, with the corrected statement)."""
import math
from common import (normalmix_pmf, tmix_pmf, binomial_pmf, betabinomial_pmf, p_from_pmf,
                    normal_density, t_density, fmt, one_in)

print("=" * 78)
print("S5. THE CLAIMS OF MODEL-DRAFT.md, SECTIONS 2, 3, 7, 8")
print("=" * 78)

# ------------------------------------------------------------------ 5.1
print("\n5.1 Section 2: 'the expected outcome when you vote, minus when you don't, equals p times B, and nothing else'")
print("    E[gain] = P(M=0) (U_A - U_tie) + P(M=-1) (U_tie - U_B). With B = U_A - U_B this is p B exactly when")
print("    U_tie = (U_A + U_B)/2, i.e. when a tie settled by a fair lot is valued at its expectation; and for any")
print("    deterministic tie rule (only one term is non-zero and U_tie is U_A or U_B). Numerically, n = 1000 and 1001:")
for n in [1000, 1001]:
    pmf = lambda k, n=n: betabinomial_pmf(k, n, 400, 0.51)
    P0 = pmf(n // 2) if n % 2 == 0 else 0.0
    Pm1 = pmf((n - 1) // 2) if n % 2 == 1 else 0.0
    p = p_from_pmf(pmf, n)
    for Ut in [0.5, 0.3]:
        gain = P0 * (1.0 - Ut) + Pm1 * (Ut - 0.0)
        print(f"    n={n}: U_A=1, U_B=0, U_tie={Ut}: E[gain] = {fmt(gain)}; p B = {fmt(p)}; ratio {gain / p:.3f}")
print("    Verdict: holds under the stated condition (a tie is worth the average of the two outcomes, or the")
print("    jurisdiction's rule is deterministic); otherwise a tie-value term is added. With parity unknown ex ante")
print("    the two cases average to p B for any tie value.")

# ------------------------------------------------------------------ 5.2
print("\n5.2 Section 2 arithmetic: B* = C / p")
for p, C in [(1e-7, 4), (1e-7, 12), (1 / 60e6, 4), (1 / 60e6, 12)]:
    print(f"    p = {p:.3g} ({one_in(p)}), C = ${C}: B* = ${C / p:,.0f}")
print("    Verdict: '$40 to $120 million' holds; '$230 to $720 million' should read $240 to $720 million")
print("    (C = $4 at p = 1 in 60 million gives $240 million; $230 million needs C = $3.83).")

# ------------------------------------------------------------------ 5.3
print("\n5.3 Section 3: 'with a fair coin breaking ties, p = 1/2 x [chance of an exact tie + chance your side is one short]'")
print("    Holds under a fair lot. At a given n only one of the two chances is non-zero (an exact tie needs n even,")
print("    one short needs n odd); so p = (1/2) P(tie) or (1/2) P(one short), never a sum of two non-zero terms.")
print("    Under a deterministic tie rule the formula is wrong for either parity (p = 0 or p = P(event)); see S1.1.")
print("    'Either way, your ballot moves the result half a win': holds under the lot (W rises by 1/2 in each event).")

# ------------------------------------------------------------------ 5.4
print("\n5.4 Section 3: 'the 1/2 appears in Gelman, King & Boscardin (1998) and Barnett (2020)'")
print("    Barnett 2020: yes, EB = (1/2) B d, d the exact-tie event. GKB 1998: yes in the section-5 rough formula")
print("    ('for casting a vote, not switching a preference'); no in the model of eqs. 1-3, whose state-level term")
print("    is the event probability f/n and whose 1/2 weights the Electoral-College tie ends. Verdict: holds in part.")

# ------------------------------------------------------------------ 5.5
print("\n5.5 Section 3: 'p ~ (how likely the race is to land at dead even) / (number of voters), up to a small constant'")
print("    Holds with the constant stated: p = f(1/2)/(2n) with f the forecast density of the share at one half, or")
print("    p = 25 q1 / n with q1 = P(share within one point of even). Without the constant, 'closeness / voters' is")
print("    off by a factor that depends on what 'closeness' means (S6.4). The error of the approximation is")
print("    +1/(8 n tau^2) at mu = 1/2 (S1.3): small once n tau^2 exceeds ~10.")

# ------------------------------------------------------------------ 5.6
print("\n5.6 Section 3, table row 1: 'p falls roughly as 1 / N'")
print(f"{'N':>9} {'tau=0.03: N p':>14} {'tau=0.01: N p':>14} {'known 50-50: N p':>17} {'sqrt(N/(2 pi))':>15}")
for N in [100, 1000, 10000, 100000, 1000000]:
    p3 = p_from_pmf(lambda k: normalmix_pmf(k, N, 0.5, 0.03), N)
    p1 = p_from_pmf(lambda k: normalmix_pmf(k, N, 0.5, 0.01), N)
    p0 = p_from_pmf(lambda k: binomial_pmf(k, N, 0.5), N)
    print(f"{N:>9} {N * p3:>14.3f} {N * p1:>14.3f} {N * p0:>17.3f} {math.sqrt(N / (2 * math.pi)):>15.3f}")
print("    Verdict: holds under the condition that the forecast uncertainty is wider than the vote-count noise,")
print("    n tau^2 >> 1 (N p is then constant). With a KNOWN 50-50 split p falls as 1/sqrt(N); with any other")
print("    known split it falls exponentially (S1.4). The reason given ('the same uncertainty is spread over more")
print("    possible margins') is the right one for the forecast regime.")

# ------------------------------------------------------------------ 5.7
print("\n5.7 Section 3, table row 2: 'p falls steeply, faster than exponentially, as the forecast moves away from 50-50'")
print("    p(d)/p(0) for an expected margin d = |mu - 1/2| in units of the forecast sd (n = 1,000,000):")
print(f"{'d/sd':>6} {'normal':>12} {'exp(-d^2/2)':>12} {'t4 (same sd)':>13} {'t4 (same scale)':>16}")
n = 1_000_000
base_n = p_from_pmf(lambda k: normalmix_pmf(k, n, 0.5, 0.03), n)
base_t = p_from_pmf(lambda k: tmix_pmf(k, n, 0.5, 0.03 / math.sqrt(2)), n)
base_ts = p_from_pmf(lambda k: tmix_pmf(k, n, 0.5, 0.03), n)
for z in [1, 2, 3, 5]:
    mu = 0.5 + 0.03 * z
    pn = p_from_pmf(lambda k: normalmix_pmf(k, n, mu, 0.03), n)
    pt = p_from_pmf(lambda k: tmix_pmf(k, n, mu, 0.03 / math.sqrt(2)), n)
    pts = p_from_pmf(lambda k: tmix_pmf(k, n, mu, 0.03), n)
    print(f"{z:>6} {pn / base_n:>12.3g} {math.exp(-0.5 * z * z):>12.3g} {pt / base_t:>13.3g} {pts / base_ts:>16.3g}")
print("    Verdict: holds for a normal forecast (p falls as exp(-d^2/(2 tau^2)), faster than exponential).")
print("    Wrong for a heavy-tailed forecast: with Gelman, Silver & Edlin's t(4) the fall is polynomial, (1 +")
print("    d^2/(4 s^2))^(-5/2), slower than exponential beyond ~3 sd. Corrected: 'steeply; how steeply depends on")
print("    the forecast's tails, and real forecasts have tails heavier than a normal'.")

# ------------------------------------------------------------------ 5.8
print("\n5.8 Section 3, table row 3: 'more uncertainty helps a lopsided race and hurts a dead-even one'")
print("    p ~ (1/tau) exp(-d^2/(2 tau^2)) / (2n) is maximised at tau = d. n = 100,000:")
print(f"{'mu':>6} " + " ".join(f"{'tau=' + str(t):>11}" for t in [0.01, 0.02, 0.03, 0.05, 0.10]))
for mu in [0.50, 0.51, 0.52, 0.55, 0.60]:
    vals = [p_from_pmf(lambda k: normalmix_pmf(k, 100000, mu, t), 100000) for t in [0.01, 0.02, 0.03, 0.05, 0.10]]
    print(f"{mu:>6} " + " ".join(f"{fmt(v, 3):>11}" for v in vals))
print("    Verdict: holds with the dividing line stated: more uncertainty helps when the expected margin exceeds")
print("    one forecast sd (|mu - 1/2| > tau) and hurts when it is within one sd. 'Lopsided' and 'dead-even' are")
print("    the two ends; a race 2 points off with a 3-point sd is hurt by more uncertainty.")

# ------------------------------------------------------------------ 5.9
print("\n5.9 Section 3, table row 4: 'structure multiplies stages: p = (chance your state is tied) x (chance it then decides)'")
print("    An identity when the second factor is the conditional probability given the tie; an approximation")
print("    (independent states) when it is the unconditional one. S4 measures the gap: a few percent for close")
print("    states, orders of magnitude for lopsided ones, where p is negligible anyway. Verdict: holds under the")
print("    stated condition, with 'then decides' read as 'decides, given that your state is tied'.")

# ------------------------------------------------------------------ 5.10
print("\n5.10 Section 7: 'with recounts and noise, your ballot still shifts the chance your side is declared the winner")
print("     by about the same p'. Let pi(m) = P(A is declared the winner | counted margin m), a logistic of width w")
print("     votes (w = 0 is the sharp rule). gain = sum_M P(M) [pi(M+1) - pi(M)], exact lattice sum; n = 100,000.")


_PMF_CACHE = {}


def margin_pmf(n, mu, tau, half_width=20000):
    key = (n, mu, tau, half_width)
    if key not in _PMF_CACHE:
        ks = list(range(max(0, n // 2 - half_width), min(n, n // 2 + half_width) + 1))
        _PMF_CACHE[key] = (ks, [normalmix_pmf(k, n, mu, tau, m=10001) for k in ks])
    return _PMF_CACHE[key]


def sigmoid(x):
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    z = math.exp(x)
    return z / (1.0 + z)


def gain_with_noise(n, mu, tau, w):
    ks, pm = margin_pmf(n, mu, tau)

    def pi(m):
        if w == 0:
            return 1.0 if m > 0 else (0.5 if m == 0 else 0.0)
        return sigmoid(m / w)
    return sum(P * (pi(2 * k - n + 1) - pi(2 * k - n)) for k, P in zip(ks, pm))


for mu in [0.50, 0.52]:
    p_sharp = p_from_pmf(lambda k: normalmix_pmf(k, 100000, mu, 0.03), 100000)
    row = []
    for w in [10, 100, 1000, 3000, 10000]:
        g = gain_with_noise(100000, mu, 0.03, w)
        row.append(f"w={w}: {g / p_sharp:.3f}")
    print(f"     mu = {mu}: sharp p = {fmt(p_sharp)}; gain / p for " + ", ".join(row))
print("     (n tau = 3,000 votes is the forecast's own spread in votes; the sum over k runs 20,000 either side of n/2)")
print("     Verdict: holds under the condition that the zone of recount-and-noise uncertainty is narrow next to the")
print("     forecast's spread (w << n tau); the sum telescopes to the density of the margin at zero, which is p. When")
print("     the zone is as wide as the forecast (w ~ n tau) the gain differs from p (the table's w = 3,000 column), and")
print("     the right measure is the smoothed one. The draft's 'about the same p' is right for every real election,")
print("     where recount zones are a few hundred votes against forecast spreads of tens of thousands.")

# ------------------------------------------------------------------ 5.11
print("\n5.11 Section 2: 'p is the chance that your ballot changes the winner'")
print("     P(the declared winner differs with and without your ballot) = sum_M P(M) P(differs | M). Under a lot the")
print("     coin that decides a tie is the same coin either way, so at M = 0 the winner differs iff the coin would")
print("     have gone to B (1/2), and at M = -1 iff it now goes to A (1/2): (1/2)P(M=0) + (1/2)P(M=-1) = p. Under a")
print("     deterministic rule the winner differs iff the one event occurs, = p. Verdict: holds (with the coin")
print("     coupled across the two worlds; any other coupling gives a larger 'differs' probability and p is the")
print("     rise in A's chance, which is what the decision needs).")

# ------------------------------------------------------------------ 5.12
print("\n5.12 Sections 2 and 8: '1 in 10 million' (best-placed 2008 states) and '1 in 60 million' (average 2008 voter)")
print("     are Gelman, Silver & Edlin's figures. As written in their text (the density at 0 of the margin in votes)")
print("     they are in our convention; if an exact-tie probability was intended they are twice ours (S2.5). Their")
print("     scale convention adds a factor of up to sqrt(2) either way at the centre. Verdict: usable as ours, with")
print("     that caveat stated beside them; B* = C/p then holds as computed in 5.2.")

# ------------------------------------------------------------------ 5.13
print("\n5.13 Section 8: 'the arithmetic is one line: p ~ closeness / voters, and B* = C / p'")
print("     Holds with the constant of 5.5 and the two-stage factor of 5.9 where a state or a seat feeds a larger")
print("     body; the simple mode's error is bounded in S6.2 (within a factor 1.2 of the exact p for n >= 1,000 and")
print("     forecast sd >= 2 points; within 1.03 for n >= 10,000 and sd >= 3 points).")
