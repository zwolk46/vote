# [measured] referendum / supermajority / small-electorate decisiveness. Binary contest, N other voters, all vote Yes or No.
import math
import numpy as np
def lgt(N, a=None):
    return np.array([math.lgamma(i+1) if a is None else math.lgamma(i+a) for i in range(N+1)])
def dist(N, mu=None, kappa=None):
    # distribution of Y (yes votes among N others). mu = expected yes share. kappa None -> binomial (known share)
    x = np.arange(N+1); lf = lgt(N)
    if kappa is None:
        logp = lf[N]-lf[x]-lf[N-x] + x*math.log(mu) + (N-x)*math.log(1-mu)
    else:
        a, b = kappa*mu, kappa*(1-mu)
        logp = lf[N]-lf[x]-lf[N-x] + lgt(N,a)[x] + lgt(N,b)[N-x] - math.lgamma(a)-math.lgamma(b)+math.lgamma(kappa)-math.lgamma(N+kappa)
    return x, np.exp(logp)
def passes(Y, X, t):
    # proposal passes if Y/(Y+X) >= t for t>0.5 ; for t=0.5 simple majority with fair coin on tie ; returns prob
    tot = Y + X
    if abs(t-0.5) < 1e-12:
        return np.where(Y > X, 1.0, np.where(Y == X, 0.5, 0.0))
    return np.where(Y >= t*tot - 1e-9, 1.0, 0.0)
def Q(N, mu, kappa, t):
    x, p = dist(N, mu, kappa)
    Y = x; X = N - x
    yes = float(np.sum(p*(passes(Y+1, X, t) - passes(Y, X, t))))     # effect of a Yes ballot on passage vs abstain
    no  = float(np.sum(p*(passes(Y, X, t) - passes(Y, X+1, t))))      # effect of a No ballot on blocking, vs abstain
    return yes, no
if __name__ == "__main__":
    print("== known shares (binomial), simple majority, mu=0.5: Q_yes ~ 1/sqrt(2 pi N)")
    for N in [9, 19, 29, 99, 999, 9999]:
        y, n = Q(N, 0.5, None, 0.5)
        print("N=%d  Q_yes=%.4f Q_no=%.4f  1/sqrt(2piN)=%.4f" % (N, y, n, 1/math.sqrt(2*math.pi*N)))
    print("== uncertain share (kappa=400, sd 2.5pts at mu=.5), N=10,000 others; thresholds 0.5, 0.6, 2/3")
    N = 10000
    for mu in [0.50, 0.55, 0.60, 0.667]:
        row = []
        for t in [0.5, 0.6, 2/3]:
            y, n = Q(N, mu, 400, t)
            row.append("t=%.3f: Q_yes=%.3g Q_no=%.3g" % (t, y, n))
        print("forecast yes share %.3f | " % mu + " | ".join(row))
    print("== small electorates, uncertain share kappa=20 (sd ~11pts), forecast .5 and .6; simple majority")
    for N in [9, 19, 29, 99, 999]:
        out = []
        for mu in [0.5, 0.6]:
            y, n = Q(N, mu, 20, 0.5)
            out.append("mu=%.1f Q_yes=%.4f" % (mu, y))
        print("N=%d " % N + " ".join(out))
