"""S8. What Mulligan & Hunter's '1 in 89,252' and Klarner's counts estimate, and how they relate to ex ante p.

Inputs are the figures R2 measured from the NBER working paper and from Klarner's data, as recorded in
research/historical-close-races-v2.md sections 1a and 1b (quoted in model/MATH.md section 8)."""
import math
from common import fmt, one_in

print("=" * 78)
print("S8. THE HISTORICAL FREQUENCIES")
print("=" * 78)


def poisson_cdf(k, lam):
    return sum(math.exp(-lam + j * math.log(lam) - math.lgamma(j + 1)) for j in range(k + 1))


def poisson_ci(k, alpha=0.05):
    """Exact (Garwood) two-sided interval for a Poisson mean given a count k."""
    def solve(target, which):
        lo, hi = 1e-9, 10.0 * (k + 10)
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            v = poisson_cdf(k - 1, mid) if which == "lower" else poisson_cdf(k, mid)
            # lower: P(X >= k | L) = alpha/2  <=> cdf(k-1 | L) = 1 - alpha/2 ; upper: cdf(k | U) = alpha/2
            if v > target:          # the cdf falls as the mean rises: a mean too small gives too large a cdf
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)
    L = 0.0 if k == 0 else solve(1 - alpha / 2, "lower")
    U = solve(alpha / 2, "upper")
    return L, U


# ---------------------------------------------------------------- 8.1
print("\n8.1 Mulligan & Hunter's figures, reproduced from the paper's numbers (R2, section 1a)")
US_votes = 16577 * 111370
ST_votes = 40036 * 23658
print(f"    US House 1898-1992: 16,577 elections x 111,370 average votes = {US_votes:,} ballots; one one-vote race")
print(f"      (NY-36 1910, 20,685 to 20,684). 20,685 / {US_votes:,} = {20685 / US_votes:.3e} = {one_in(20685 / US_votes)}  (abstract: 1 in 89,000)")
print(f"      counting both finalists' ballots, 41,369: {one_in(41369 / US_votes)}")
print(f"    State legislatures 1968-89: 40,036 elections x 23,658 = {ST_votes:,} ballots; 2 ties and 7 one-vote races.")
print(f"      all 61,328 ballots in the nine: {one_in(61328 / ST_votes)} (abstract: 1 in 15,000); the US treatment, 37,104: {one_in(37104 / ST_votes)}")

# ---------------------------------------------------------------- 8.2
print("\n8.2 What a per-ballot frequency estimates. Let election e have N_e voters and forecast density f_e of the")
print("    share at one half. Ex ante, with parity unknown: P(exact tie) ~ f_e/(2 N_e), P(one-vote win) ~ f_e/N_e,")
print("    and our p_e = f_e/(2 N_e), the event (tie or one short) ~ f_e/N_e.")
print("    'Ballots cast for a candidate who tied or won by one' count N_e in a tie and ~N_e/2 in a one-vote win, so")
print("    E[count_e] ~ N_e [f_e/(2N_e)] + (N_e/2)[f_e/N_e] = f_e. The frequency F = sum count_e / sum N_e therefore")
print("    estimates sum_e f_e / sum_e N_e = the ballot-weighted average of the EVENT probability f_e/N_e,")
print("    which is twice the ballot-weighted average of our p_e. Counting every ballot in a pivot election gives")
print("    1.5 sum f_e / sum N_e (M&H's eq. 4), three times the average p.")
for label, F, mult in [("US '1 in 89,252' (winner's ballots)", 20685 / US_votes, 2.0),
                       ("state '1 in 15,444' (all ballots)", 61328 / ST_votes, 3.0),
                       ("state in the US treatment, '1 in 25,527'", 37104 / ST_votes, 2.0)]:
    print(f"    {label}: implied ballot-weighted average p = F/{mult:.0f} = {fmt(F / mult)} = {one_in(F / mult)}")
fbar_us = (20685 / US_votes) * 111370
fbar_st = (61328 / ST_votes) * 23658 / 1.5
print(f"    Implied average density at one half: US f-bar = F x average N = {fbar_us:.2f}; state f-bar = {fbar_st:.2f}")
print("    (M&H's own Figure 5 reading is f ~ 2 for the whole sample; GKB's '18% of states within 2 points' is")
print("    f ~ 4.5 for presidential-state forecasts: House and state-legislative races are on average less close.)")

# ---------------------------------------------------------------- 8.3
print("\n8.3 The sampling error of a count of one")
for label, k, denom in [("US House one-vote races", 1, 16577), ("state legislative ties or one-vote races", 9, 40036)]:
    L, U = poisson_ci(k)
    print(f"    {label}: {k} in {denom:,}; 95% interval for the expected count [{L:.3f}, {U:.2f}], i.e. the rate")
    print(f"      is known to within a factor {U / k:.1f} above and {k / L:.1f} below the point estimate")
L1, U1 = poisson_ci(1)
print(f"    So '1 in 89,252' is a point estimate from one event; the data are consistent with {one_in(20685 / US_votes * U1)} and with {one_in(20685 / US_votes * L1)}.")

# ---------------------------------------------------------------- 8.4
print("\n8.4 Klarner's counts (state legislative general elections 1968-2022; R2, section 1b)")
for label, k, m in [("all contests with a margin", 52, 109093), ("single-seat contests", 30, 99165), ("2018-2024 (seats)", 5, 23830)]:
    L, U = poisson_ci(k)
    print(f"    {label}: {k} events (margin 0 or 1) in {m:,}: {fmt(k / m)} per contest ({one_in(k / m)}); 95% [{L / m:.2e}, {U / m:.2e}]")
print("    A per-CONTEST event rate estimates the contest-average of P(margin 0 or 1) = 1.5 f_e/N_e (parity averaged),")
print("    i.e. 3 x the contest-average of p_e. Contest averages weight small districts heavily (p_e ~ 1/N_e), so")
print(f"    the implied contest-average p = {fmt(52 / 109093 / 3)} ({one_in(52 / 109093 / 3)}) is not comparable to M&H's")
print("    ballot-weighted figure, which weights large districts. Both are averages over every contest, lopsided")
print("    ones included; neither is the p of any particular contest.")

# ---------------------------------------------------------------- 8.5
print("\n8.5 Relation to the ex ante p, in one line each")
print("    (i) F estimates an average of event probabilities over a population of elections, not a probability for one.")
print("    (ii) The ex ante p for one election can be far from that average: 1/(2N) x f_e with f_e from 0 (a 70-30")
print("         race) to ~20 (a dead heat with a 2-point sd); the population average f-bar is about 1 to 2.")
print("    (iii) F counts the first official margin; later counts and recounts move it (M&H's own check cut their")
print("          unweighted frequency by 50% and the vote-weighted by 76%), so F overstates how often a ballot settled")
print("          the result under section 7's smoothed definition.")
print("    (iv) The reality check the model can pass: the sum over a population of elections of the model's")
print("         event probabilities should land inside the Poisson interval of the observed count. For Klarner's")
print(f"         universe that is 52 events with 95% interval [{poisson_ci(52)[0]:.0f}, {poisson_ci(52)[1]:.0f}]; the check needs a forecast")
print("         for each contest, which no source read provides. What can be checked now is the average density:")
print(f"         F x N-bar = {fbar_us:.2f} (US) and {fbar_st:.2f} (state), against ~2 from M&H's own Figure 5.")
