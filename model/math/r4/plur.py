# Exact decisiveness calculations for plurality, 2 and 3 candidates. All [measured] here.
# Q_j = P(j wins | one more vote for j) - P(j wins | that voter abstains); ties broken uniformly among tied leaders.
import math, sys
import numpy as np

def lg_table(N, a=None):
    if a is None:
        return np.array([math.lgamma(i+1) for i in range(N+1)])
    return np.array([math.lgamma(i+a) for i in range(N+1)])

def two_cand(N, mu, kappa=None):
    # others' votes for A ~ Binomial(N, mu) (kappa None) or Beta-Binomial with alpha=kappa*mu
    x = np.arange(N+1)
    lf = lg_table(N)
    if kappa is None:
        logp = lf[N]-lf[x]-lf[N-x] + x*math.log(mu[0]) + (N-x)*math.log(mu[1])
    else:
        a0, a1 = kappa*mu[0], kappa*mu[1]
        la0, la1 = lg_table(N, a0), lg_table(N, a1)
        logp = lf[N]-lf[x]-lf[N-x] + la0[x] + la1[N-x] - math.lgamma(a0) - math.lgamma(a1) + math.lgamma(kappa) - math.lgamma(N+kappa)
    p = np.exp(logp)
    def w(a, b):  # A's win prob
        return np.where(a > b, 1.0, np.where(a == b, 0.5, 0.0))
    QA = float(np.sum(p*(w(x+1, N-x) - w(x, N-x))))
    return QA

def three_cand(N, mu, kappa=None):
    # returns Q_1, Q_2, Q_3
    lf = lg_table(N)
    if kappa is not None:
        a = [kappa*m for m in mu]
        la = [lg_table(N, ai) for ai in a]
        const = math.lgamma(kappa) - math.lgamma(N+kappa) - sum(math.lgamma(ai) for ai in a)
    Q = np.zeros(3)
    x2 = np.arange(N+1)
    for x1 in range(N+1):
        x2v = x2[:N-x1+1]
        x3v = N - x1 - x2v
        if kappa is None:
            logp = lf[N]-lf[x1]-lf[x2v]-lf[x3v] + x1*math.log(mu[0]) + x2v*math.log(mu[1]) + x3v*math.log(mu[2])
        else:
            logp = lf[N]-lf[x1]-lf[x2v]-lf[x3v] + la[0][x1] + la[1][x2v] + la[2][x3v] + const
        p = np.exp(logp)
        c = np.stack([np.full_like(x2v, x1), x2v, x3v])  # counts, shape 3 x m
        def win(c, j):
            m = c.max(axis=0)
            tied = (c == m).sum(axis=0)
            return np.where(c[j] == m, 1.0/tied, 0.0)
        for j in range(3):
            c2 = c.copy(); c2[j] += 1
            Q[j] += float(np.sum(p*(win(c2, j) - win(c, j))))
    return Q

if __name__ == "__main__":
    print("== two candidates, known shares (0.5,0.5): exact Q_A vs sqrt(2/(pi N))/2 style comparison")
    for N in [100, 1000, 10000, 100000, 1000000]:
        q = two_cand(N, (0.5, 0.5))
        print(N, "Q_A=%.6g" % q, " 1/sqrt(2 pi N)=%.6g" % (1/math.sqrt(2*math.pi*N)), " sqrt(2/(pi N))=%.6g" % math.sqrt(2/(math.pi*N)))
    print("== two candidates, uncertain shares, Beta-Binomial, mu=(.51,.49)")
    for kappa in [100, 400, 2500]:
        for N in [1000, 10000, 100000]:
            q = two_cand(N, (0.51, 0.49), kappa)
            sd = math.sqrt(.51*.49/(kappa+1))
            print("kappa=%d sd_share=%.4f N=%d Q_A=%.6g  N*Q_A=%.4g" % (kappa, sd, N, q, N*q))
