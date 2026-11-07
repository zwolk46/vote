"""S4. Two stages: a state then the Electoral College; a seat then a chamber.

The product p_i = P(state i tie event) x P(the state's electoral votes decide | that tie) is an identity
(conditional probability). The usual formula replaces the conditional by the unconditional
P(the state's electoral votes decide), which assumes the states are independent. This script
measures what that costs when a share rho of each state's forecast variance is a common
national swing, using the Economist's 2016 back-test means (data/economist_2016_backtest.csv),
the 2016 electoral votes (data/electoral_votes_2016.csv) and the 2016 two-party vote by state
(data/medsl_2016_state_totals.csv). Everything is computed exactly by dynamic programming over
states for each value of the national swing, then integrated over the swing on a grid.
Cited in model/MATH.md section 4."""
import csv
import math
import numpy as np
from common import normal_density, fmt, one_in

erf = np.vectorize(math.erf)


def Phi(x):
    return 0.5 * (1.0 + erf(np.asarray(x, dtype=float) / math.sqrt(2.0)))


def read(path):
    with open(path) as f:
        rows = [ln for ln in f if not ln.startswith("#")]
    return list(csv.DictReader(rows))


econ = {r["state"]: (float(r["mean"]), float(r["se"])) for r in read("data/economist_2016_backtest.csv")}
ev = {r["state"]: int(r["ev"]) for r in read("data/electoral_votes_2016.csv")}
n2 = {r["state"]: int(r["dem"]) + int(r["rep"]) for r in read("data/medsl_2016_state_totals.csv")}
states = sorted(ev)
assert len(states) == 51 and all(s in econ and s in n2 for s in states)
mu = np.array([econ[s][0] for s in states])
# README: se = (high - mean)/1.68, high the 97.5% quantile; for a normal, high - mean = 1.96 sd
tau = np.array([econ[s][1] * 1.68 / 1.96 for s in states])
e = np.array([ev[s] for s in states])
n = np.array([n2[s] for s in states], dtype=float)
tau0 = tau.min()                     # the typical state (se 0.024 -> sd 0.0206)
PI_HOUSE = 0.5                       # A's chance if the College ties 269-269 (the House decides; unknown ex ante)

print("=" * 78)
print("S4. TWO STAGES: STATE THEN ELECTORAL COLLEGE; SEAT THEN CHAMBER")
print("=" * 78)
print(f"\n4.0 Inputs: 51 states, {int(e.sum())} electoral votes, two-party vote {int(n.sum()):,}; state forecast sd from")
print(f"    0.0206 to {tau.max():.4f} (Economist se x 1.68/1.96); national swing share rho of the typical state's variance.")


def ev_window_prob(i, d_mean, d_sd, rho):
    """E[ weight(E_-i) ] where E_-i = A's electoral votes from the other states, the national swing
    delta ~ N(d_mean, d_sd^2), state j wins for A with chance Phi((mu_j + delta - 1/2)/s_j) given delta,
    s_j^2 = tau_j^2 - rho tau0^2. weight = 1 for 270 - e_i <= E <= 268 (the flip decides outright),
    PI_HOUSE at E = 269 - e_i (the flip makes a 269 tie), 1 - PI_HOUSE at E = 269 (the flip breaks one)."""
    s_d = math.sqrt(rho) * tau0
    if d_sd < 1e-12:
        grid = np.array([d_mean])
        w = np.array([1.0])
    else:
        grid = np.linspace(d_mean - 6 * d_sd, d_mean + 6 * d_sd, 241)
        w = np.exp(-0.5 * ((grid - d_mean) / d_sd) ** 2)
        w /= w.sum()
    s = np.sqrt(np.maximum(tau ** 2 - s_d ** 2, 1e-12))
    dist = np.zeros((len(grid), 539))
    dist[:, 0] = 1.0
    for j in range(len(states)):
        if j == i:
            continue
        q = Phi((mu[j] + grid - 0.5) / s[j])[:, None]
        shifted = np.zeros_like(dist)
        shifted[:, e[j]:] = dist[:, :539 - e[j]]
        dist = dist * (1 - q) + shifted * q
    weight = np.zeros(539)
    lo, hi = 270 - e[i], 268
    weight[max(lo, 0):hi + 1] = 1.0
    if 269 - e[i] >= 0:
        weight[269 - e[i]] = PI_HOUSE
    weight[269] = 1.0 - PI_HOUSE
    return float((dist @ weight * w).sum())


def stage_two(i, rho, conditional):
    s_d2 = rho * tau0 ** 2
    if conditional:
        # delta | v_i = 1/2 for v_i = mu_i + delta + eps_i, eps_i ~ N(0, tau_i^2 - s_d2)
        m = (0.5 - mu[i]) * s_d2 / tau[i] ** 2
        v = s_d2 * (tau[i] ** 2 - s_d2) / tau[i] ** 2
        return ev_window_prob(i, m, math.sqrt(max(v, 0.0)), rho)
    return ev_window_prob(i, 0.0, math.sqrt(s_d2), rho)


f_half = np.array([normal_density(0.5, mu[i], tau[i]) for i in range(51)])
p_state = f_half / (2 * n)       # stage one, our convention (lot / parity-averaged)

print("\n4.1 Stage two per state: W = P(the state's electoral votes decide the College | the state is tied), and")
print("    the unconditional W' used by the product formula. rho = 0 (independent states): W = W' exactly.")
print("    p = p_state x W, with p_state = f_i(1/2)/(2 n_i) and n_i the 2016 two-party vote.")
rhos = [0.0, 0.3, 0.5, 0.7]
W = {rho: np.array([stage_two(i, rho, True) for i in range(51)]) for rho in rhos}
Wu = {rho: np.array([stage_two(i, rho, False) for i in range(51)]) for rho in rhos}
hdr = f"{'st':>3} {'ev':>3} {'mu':>6} {'tau':>6} {'n (2-party)':>12} {'p_state':>9} {'W rho=0':>9}"
for rho in rhos[1:]:
    hdr += f" {'W|tie .' + str(rho)[2:]:>9} {'W .' + str(rho)[2:]:>9}"
hdr += f" {'p rho=.5':>10}"
print(hdr)
for i, st in enumerate(states):
    line = f"{st:>3} {e[i]:>3} {mu[i]:>6.3f} {tau[i]:>6.4f} {int(n[i]):>12,} {fmt(p_state[i], 3):>9} {W[0.0][i]:>9.4f}"
    for rho in rhos[1:]:
        line += f" {W[rho][i]:>9.4f} {Wu[rho][i]:>9.4f}"
    line += f" {fmt(p_state[i] * W[0.5][i], 3):>10}"
    print(line)

print("\n4.2 What independence costs: ratio of the product formula (W') to the conditional (W), by rho")
for rho in rhos[1:]:
    r = Wu[rho] / np.maximum(W[rho], 1e-300)
    g1 = [i for i in range(51) if abs(mu[i] - 0.5) < 0.015]
    g2 = [i for i in range(51) if 0.015 <= abs(mu[i] - 0.5) < 0.03]
    g3 = [i for i in range(51) if 0.03 <= abs(mu[i] - 0.5) < 0.10]
    far = [i for i in range(51) if abs(mu[i] - 0.5) >= 0.10 and W[rho][i] > 1e-6]
    zero = [states[i] for i in range(51) if W[rho][i] <= 1e-6]
    print(f"    rho = {rho}: ratio W'/W for states within 1.5 points of even ({len(g1)}): {r[g1].min():.3f} to {r[g1].max():.3f};"
          f" 1.5 to 3 points ({len(g2)}): {r[g2].min():.3f} to {r[g2].max():.3f}; 3 to 10 points ({len(g3)}): {r[g3].min():.2f} to {r[g3].max():.2f};"
          f" 10 points or more: {r[far].min():.2g} to {r[far].max():.2g}, and W|tie below 1e-6 in {', '.join(zero) or 'none'}")
for st in ["FL", "NH", "PA", "UT", "WV", "DC"]:
    i = states.index(st)
    print(f"    {st}: mu = {mu[i]:.3f}; W|tie at rho 0, .3, .5, .7 = " + ", ".join(f"{W[r][i]:.4f}" for r in rhos)
          + "; W' = " + ", ".join(f"{Wu[r][i]:.4f}" for r in rhos))
print("    Reading: for a state within 1.5 points of even the two agree within about 10% at any rho, because")
print("    conditioning on a near-even state moves the national swing little; at 2 to 3 points off they differ by")
print("    up to a third at rho = 0.5. For a lopsided state they differ by orders of")
print("    magnitude: a tie in Utah (mu 0.375) implies a swing that hands A almost every state, so W|tie falls; but")
print("    p_state there is already ~1e-10 or less, so the error lands on numbers that do not matter. The product")
print("    formula is safe where p is large and wrong where p is negligible.")

print("\n4.3 The average voter's p (vote-weighted mean of p_i), and the College-level total")
for rho in rhos:
    pi_ = p_state * W[rho]
    pu = p_state * Wu[rho]
    print(f"    rho = {rho}: average p (conditional) = {fmt((pi_ * n).sum() / n.sum())} ({one_in((pi_ * n).sum() / n.sum())});"
          f" product formula = {fmt((pu * n).sum() / n.sum())}; max state p = {fmt(pi_.max())} ({states[int(pi_.argmax())]})")
print("    Reading: the national swing lowers every W (it makes the College less likely to sit on a knife-edge")
print("    through any one state's e_i, since states move together), independent of the conditioning question.")
print("    The 1/2 on the House in the window weights is 'ex ante unknowable', as in the two-way tie rule.")

# --------------------------------------------------------------------- chamber (stylised)
print("\n4.4 A seat then a chamber (STYLISED inputs: 435 seats, the other 434 with forecast means spread evenly")
print("    from 0.30 to 0.70, each with sd 0.03, a common swing with share rho of that variance; this seat tied).")
print("    A's majority needs 218 of 435; the flip of this seat decides iff the other 434 give A exactly 217.")
M = 434
mu_s = 0.30 + 0.40 * (np.arange(M) + 0.5) / M
tau_s = 0.03


def seat_window(d_mean, d_sd, rho):
    s_d = math.sqrt(rho) * tau_s
    if d_sd < 1e-12:
        grid, w = np.array([d_mean]), np.array([1.0])
    else:
        grid = np.linspace(d_mean - 6 * d_sd, d_mean + 6 * d_sd, 241)
        w = np.exp(-0.5 * ((grid - d_mean) / d_sd) ** 2)
        w /= w.sum()
    s = math.sqrt(tau_s ** 2 - s_d ** 2)
    dist = np.zeros((len(grid), M + 1))
    dist[:, 0] = 1.0
    for j in range(M):
        q = Phi((mu_s[j] + grid - 0.5) / s)[:, None]
        shifted = np.zeros_like(dist)
        shifted[:, 1:] = dist[:, :M]
        dist = dist * (1 - q) + shifted * q
    return float((dist[:, 217] * w).sum()), float(((dist * np.arange(M + 1)).sum(axis=1) * w).sum())


print(f"{'this seat mu':>13} {'rho':>5} {'P(217|tie)':>11} {'P(217)':>9} {'ratio':>7} {'E[seats|tie]':>13}")
for mu_i in [0.50, 0.45, 0.40]:
    for rho in rhos:
        s_d2 = rho * tau_s ** 2
        m = (0.5 - mu_i) * s_d2 / tau_s ** 2
        v = s_d2 * (tau_s ** 2 - s_d2) / tau_s ** 2
        pc, es = seat_window(m, math.sqrt(max(v, 0)), rho)
        pu, _ = seat_window(0.0, math.sqrt(s_d2), rho)
        print(f"{mu_i:>13.2f} {rho:>5} {pc:>11.4f} {pu:>9.4f} {pc / pu:>7.3f} {es:>13.1f}")
print("    Reading: with 434 other seats the conditioning bites harder than in the College, because the swing")
print("    implied by a tie in a seat that leans 10 points moves the expected seat count by tens of seats.")
print("    R4's chamber.py takes P(exactly 217) unconditionally (its rows are the 'P(217)' column, with its own")
print("    draws of means); that is the rho = 0 case, or the product formula at rho > 0. See S7.")
