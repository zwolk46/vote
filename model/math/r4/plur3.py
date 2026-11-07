import math, sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from plur import two_cand, three_cand
cases = [
 ("3 cand, forecast (.40,.38,.22), kappa=400", (0.40,0.38,0.22), 400),
 ("3 cand, forecast (.36,.34,.30), kappa=400", (0.36,0.34,0.30), 400),
 ("3 cand, forecast (.45,.45,.10), kappa=400", (0.45,0.45,0.10), 400),
]
for N in [1000, 10000]:
    q2 = two_cand(N, (0.51,0.49), 400)
    print("N=%d two-cand (.51,.49) kappa=400: Q_A=%.6g N*Q=%.3f" % (N, q2, N*q2))
    for name, mu, kappa in cases:
        Q = three_cand(N, mu, kappa)
        print("N=%d %s: Q1=%.6g Q2=%.6g Q3=%.6g  N*Q=%s" % (N, name, Q[0], Q[1], Q[2], ["%.3f" % (N*q) for q in Q]))
    # knife-edge, known shares
    for mu in [(1/3,1/3,1/3), (0.4,0.4,0.2), (0.45,0.45,0.10)]:
        Q = three_cand(N, mu, None)
        q2k = two_cand(N, (0.5,0.5))
        print("N=%d known shares %s: Q1=%.6g Q2=%.6g Q3=%.6g | two-cand known (.5,.5) Q_A=%.6g" % (N, tuple(round(m,3) for m in mu), Q[0], Q[1], Q[2], q2k))
