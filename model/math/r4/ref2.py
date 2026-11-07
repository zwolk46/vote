import math, sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from ref import Q
def Qavg(N0, mu, kappa, t, width=30):
    ys = []; ns = []
    for N in range(N0, N0+width):
        y, n = Q(N, mu, kappa, t); ys.append(y); ns.append(n)
    return sum(ys)/width, sum(ns)/width
print("Referendum with threshold t on Yes/(Yes+No); others N~10,000 (averaged over N=10000..10029 to avoid lattice artefacts); Dirichlet-style uncertainty kappa=400 (sd 2.5 pts at 50%)")
print("Q_yes = P(pass | I vote Yes) - P(pass | I abstain); Q_no = P(pass | abstain) - P(pass | I vote No)")
for mu in [0.50, 0.55, 0.60, 0.667]:
    row = []
    for t in [0.5, 0.6, 2/3]:
        y, n = Qavg(10000, mu, 400, t)
        row.append("t=%.3f: yes=%.3g no=%.3g" % (t, y, n))
    print("forecast Yes %.3f | " % mu + " | ".join(row))
