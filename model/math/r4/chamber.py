# [measured, stylised] P(a given seat's outcome decides majority control | that seat is exactly tied), 435-seat chamber.
import math
import numpy as np
def Phi(x): return 0.5*(1+np.vectorize(math.erf)(x/math.sqrt(2)))
def run(m0, base_sd=14.0, tau=3.0, sig_nat=2.0, seed=0, nS=61):
    rng = np.random.default_rng(seed)
    m = rng.normal(m0, base_sd, 434)      # baseline Democratic margin (points) of the other 434 seats
    ss = np.linspace(-4, 4, nS)*sig_nat; w = np.exp(-0.5*np.linspace(-4,4,nS)**2); w /= w.sum()
    pk = np.zeros(435); ed = 0.0; ed2 = 0.0
    for s, ws in zip(ss, w):
        p = Phi((m + s)/tau)
        dp = np.zeros(435); dp[0] = 1.0
        for pj in p:
            dp[1:] = dp[1:]*(1-pj) + dp[:-1]*pj
            dp[0] *= (1-pj)
        pk += ws*dp
        mean = p.sum(); ed += ws*mean; ed2 += ws*(mean**2 + (p*(1-p)).sum())
    # pk[k] = P(D wins exactly k of the other 434). Seat i decides control iff k = 217 (D reaches 218 only with i).
    sd = math.sqrt(ed2 - ed**2)
    return pk[217], ed, sd, pk[216:219]
print("Stylised chamber: 434 other seats, baseline margins ~ N(m0, 14 pts), idiosyncratic sd 3 pts, national swing sd sigma_nat.")
for sig in [1.0, 2.0, 3.0]:
    for m0 in [0.0, 3.0, 6.0]:
        vals = [run(m0, sig_nat=sig, seed=s) for s in range(3)]
        p = np.mean([v[0] for v in vals]); ed = np.mean([v[1] for v in vals]); sd = np.mean([v[2] for v in vals])
        print("sigma_nat=%.1f m0=%+.1f: expected D seats among others=%.0f (sd %.1f)  P(tip | seat tied)=%.4f  (1 in %.0f)" % (sig, m0, ed, sd, p, 1/p if p>0 else float('inf')))
