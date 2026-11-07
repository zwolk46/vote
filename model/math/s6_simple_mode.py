"""S6. The simplest lay formula, and its error against the exact p over real election sizes.

Candidates (n = other voters, v = forecast share of A, f = its density at 1/2):
  (F) full:      p = f(1/2)/(2n)
  (Q) lay:       p = 25 q1 / n,  q1 = P(share within one point of 50-50) = P(0.49 <= v <= 0.51)
  (K) constant:  p = K/n with K fixed (Edlin-Gelman-Kaplan's 1/(0.12 n) = 8.33/n; '10/n')
Cited in model/MATH.md section 6."""
import math
from common import normalmix_pmf, p_from_pmf, normal_density, fmt

print("=" * 78)
print("S6. THE SIMPLEST LAY FORMULA")
print("=" * 78)


def Phi(z):
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def q1(mu, tau, w=0.01):
    return Phi((0.5 + w - mu) / tau) - Phi((0.5 - w - mu) / tau)


print("\n6.1 Why 25 q1 / n: q1 ~ 0.02 f(1/2) when the forecast is wider than the one-point window, so")
print("    25 q1 / n ~ 0.5 f(1/2) / n = f(1/2)/(2n). The ratio q1 / (0.02 f(1/2)) at mu = 1/2:")
for tau in [0.005, 0.01, 0.015, 0.02, 0.03, 0.05, 0.10]:
    print(f"    tau = {tau:.3f}: q1 = {q1(0.5, tau):.4f}, 0.02 f = {0.02 * normal_density(0.5, 0.5, tau):.4f}, ratio = {q1(0.5, tau) / (0.02 * normal_density(0.5, 0.5, tau)):.3f}")
print("    (a narrower window, +-0.5 point and 50 q/n, tracks f more closely but is harder to say)")

print("\n6.2 Error of each candidate against the exact p (normal forecast, binomial kernel folded in)")
print("    columns: exact p; then ratio candidate / exact for (F) f/(2n), (Q) 25 q1/n, (K) 8.33/n, (K') 10/n")
print(f"{'n':>10} {'mu':>5} {'tau':>5} {'exact p':>11} {'F':>7} {'Q':>7} {'K8.33':>7} {'K10':>7}")
worst = {"F": 0.0, "Q": 0.0}
cases = []
for n in [300, 1000, 3000, 10000, 100000, 1000000, 7000000, 16000000]:
    for mu in [0.50, 0.52, 0.55, 0.60]:
        for tau in [0.02, 0.03, 0.05, 0.10]:
            if (mu - 0.5) > 2.5 * tau:
                continue            # beyond 2.5 sd the race is not close; see 6.3
            pe = p_from_pmf(lambda k: normalmix_pmf(k, n, mu, tau), n)
            F = normal_density(0.5, mu, tau) / (2 * n)
            Q = 25 * q1(mu, tau) / n
            K1, K2 = 8.3333 / n, 10.0 / n
            cases.append((n, mu, tau, pe, F / pe, Q / pe, K1 / pe, K2 / pe))
            print(f"{n:>10} {mu:>5} {tau:>5} {fmt(pe):>11} {F / pe:>7.3f} {Q / pe:>7.3f} {K1 / pe:>7.2f} {K2 / pe:>7.2f}")
sub = [c for c in cases if c[0] >= 1000 and c[2] >= 0.02]
print(f"    over the rows with n >= 1,000: (F) within a factor {max(max(c[4], 1 / c[4]) for c in sub):.2f} of exact, "
      f"(Q) within {max(max(c[5], 1 / c[5]) for c in sub):.2f}; (K) 8.33/n ranges from {min(c[6] for c in sub):.2f} to {max(c[6] for c in sub):.2f}")
sub2 = [c for c in cases if c[0] >= 1000 and c[2] >= 0.03]
print(f"    over the rows with n >= 1,000 and tau >= 0.03: (Q) within a factor {max(max(c[5], 1 / c[5]) for c in sub2):.2f}")
sub3 = [c for c in cases if c[0] >= 10000 and c[2] >= 0.03]
print(f"    over the rows with n >= 10,000 and tau >= 0.03: (Q) within a factor {max(max(c[5], 1 / c[5]) for c in sub3):.3f}")

print("\n6.3 The constant K cannot stand in for the forecast: f(1/2) over the range of real races")
for mu, tau in [(0.5, 0.02), (0.5, 0.05), (0.52, 0.03), (0.55, 0.03), (0.55, 0.05), (0.60, 0.05), (0.65, 0.05), (0.60, 0.10)]:
    f = normal_density(0.5, mu, tau)
    print(f"    mu = {mu:.2f}, tau = {tau:.2f}: f(1/2) = {f:8.3f}; p n = {f / 2:7.3f}; 25 q1 = {25 * q1(mu, tau):7.3f}")
print("    A 60-40 race forecast with sd 5 points has p n = 0.54 against 3.99 for a 50-50 race, a factor 7; a 65-35")
print("    race has 0.044, a factor 90: the constant K must carry the closeness, which no single K can.")

print("\n6.4 Reading the draft's 'closeness divided by voters': with closeness q1 (within one point) the lay")
print("    formula is p = 25 q1 / n; the EVENT probability (a tie or one-vote win among the others) is 50 q1 / n,")
print("    twice it; 'closeness / voters' with no constant is neither. At q1 = 0.3, n = 100,000:")
print(f"    p = {25 * 0.3 / 1e5:.2e} (1 in {1e5 / (25 * 0.3):,.0f}); event = {50 * 0.3 / 1e5:.2e}; q1/n = {0.3 / 1e5:.2e} (1 in {1e5 / 0.3:,.0f}).")

print("\n6.5 Sizes in the brief: from a few hundred voters to a presidential state (stage one only)")
for n, mu, tau in [(300, 0.5, 0.05), (2000, 0.52, 0.04), (30000, 0.51, 0.03), (300000, 0.53, 0.025), (3000000, 0.49, 0.02), (9122861, 0.496, 0.0206)]:
    pe = p_from_pmf(lambda k: normalmix_pmf(k, n, mu, tau), n)
    Q = 25 * q1(mu, tau) / n
    print(f"    n = {n:>9,}, mu = {mu}, tau = {tau}: exact p = {fmt(pe)} (1 in {1 / pe:,.0f}); 25 q1/n = {fmt(Q)}; ratio {Q / pe:.3f}")
print("    (the last row is Florida 2016 in the Economist back-test, mean 0.496, sd 0.0206, two-party vote 9,122,861: see S4 for stage two)")
