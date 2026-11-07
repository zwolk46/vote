# [measured] Probability that one extra vote for party j adds a seat to j under D'Hondt (ties by lot ~ 1/2).
# Model: shares ~ Dirichlet(kappa*mu); others' votes ~ Poisson(N*share_i); party j's own count ~ Poisson(N*share_j), integrated analytically.
import math, sys
import numpy as np
lg = np.vectorize(math.lgamma)

def q_party(N, M, mu, kappa, draws=20000, seed=1, chunk=2000):
    rng = np.random.default_rng(seed)
    K = len(mu)
    out = np.zeros(K)
    for j in range(K):
        tot = 0.0; n = 0
        others = [i for i in range(K) if i != j]
        while n < draws:
            m = min(chunk, draws-n)
            sh = rng.dirichlet(np.array(mu)*kappa, size=m)       # m x K
            lam = N*sh
            vo = rng.poisson(lam[:, others]).astype(np.int64)    # m x (K-1)
            d = np.arange(1, M+1)
            # all quotients of others: m x (K-1) x M
            quo = vo[:, :, None] / d[None, None, :]
            flat = quo.reshape(m, -1)
            order = np.argsort(-flat, axis=1)[:, :M]             # top M quotient indices
            top_idx = order                                       # r-th largest = top_idx[:, r-1]
            # for s=1..M need the (M-s+1)-th largest quotient among others
            r = M - np.arange(1, M+1) + 1                         # M..1
            sel = np.take_along_axis(top_idx, (r-1)[None, :].repeat(m, 0), axis=1)  # m x M indices into flat
            party = sel // M                                      # which other party
            dd = (sel % M) + 1                                    # divisor
            vq = np.take_along_axis(vo, party, axis=1)            # votes of that party
            s = np.arange(1, M+1)[None, :]
            num = s * vq                                          # T = num/dd
            T_floor = num // dd
            is_int = (num % dd == 0)
            lam_j = lam[:, j][:, None]
            def logpmf(k):
                k = np.maximum(k, 0)
                return k*np.log(lam_j) - lam_j - lg(k+1)
            # non-integer T: c=1 at v=floor(T). integer T: c=1/2 at v=T and v=T-1
            p_nonint = np.exp(logpmf(T_floor))
            p_int = 0.5*np.exp(logpmf(T_floor)) + 0.5*np.exp(logpmf(T_floor-1))
            contrib = np.where(is_int, p_int, p_nonint).sum(axis=1)
            tot += contrib.sum(); n += m
        out[j] = tot/n
    return out

if __name__ == "__main__":
    cases = [
      ("council-sized: M=27, N=4,000 valid votes", 4000, 27, (.30,.25,.20,.15,.10)),
      ("district: M=5, N=50,000", 50000, 5, (.35,.30,.20,.10,.05)),
      ("district: M=10, N=100,000", 100000, 10, (.35,.30,.20,.10,.05)),
      ("national list: M=150, N=5,000,000", 5000000, 150, (.30,.25,.20,.15,.10)),
    ]
    for name, N, M, mu in cases:
        for kappa in [400]:
            q = q_party(N, M, mu, kappa, draws=6000 if M>50 else 20000)
            print(name, "kappa=%d" % kappa)
            print("   shares", mu)
            print("   Q_j (P that one more vote adds a seat):", ["%.3g" % x for x in q])
            print("   M/N = %.3g ; Q_j / (M/N) = %s" % (M/N, ["%.2f" % (x/(M/N)) for x in q]))
