# Independent brute-force check of pr.py: direct D'Hondt with ties by lot, adding one vote to party j.
import sys, math
import numpy as np
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from pr import q_party

def dhondt_seats(v, M, rng):
    # v: array K ints. returns seats array; ties at last seat broken by lot
    K = len(v)
    quo = []
    for i in range(K):
        for d in range(1, M+1):
            quo.append((v[i]/d, i))
    quo.sort(key=lambda t: -t[0])
    seats = np.zeros(K, dtype=int)
    cutoff = quo[M-1][0]
    sure = [q for q in quo if q[0] > cutoff]
    tied = [q for q in quo if q[0] == cutoff]
    for q in sure: seats[q[1]] += 1
    need = M - len(sure)
    idx = rng.permutation(len(tied))[:need]
    for t in idx: seats[tied[t][1]] += 1
    return seats

def brute(N, M, mu, kappa, j, draws, seed=5):
    rng = np.random.default_rng(seed)
    K = len(mu); gains = 0.0
    for _ in range(draws):
        sh = rng.dirichlet(np.array(mu)*kappa)
        v = rng.poisson(N*sh)
        s0 = dhondt_seats(v, M, rng)[j]
        v2 = v.copy(); v2[j] += 1
        s1 = dhondt_seats(v2, M, rng)[j]
        gains += (s1 - s0)
    return gains/draws

N, M, mu, kappa = 400, 5, (.35,.30,.20,.10,.05), 400
print("analytic:", q_party(N, M, mu, kappa, draws=40000, seed=2))
print("brute j=0:", brute(N, M, mu, kappa, 0, 60000))
print("brute j=1:", brute(N, M, mu, kappa, 1, 60000))
print("brute j=3:", brute(N, M, mu, kappa, 3, 60000))
