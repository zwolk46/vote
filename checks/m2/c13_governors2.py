"""C13 (second pass, item 1). The governor test of the first pass (M2-REPORT 3.1) run again on the files after #38
(governors from 1978, the last race as a predictor, t4 first): contests decided by k votes or fewer, expected
under the forecast each p rests on (P(|D - R| <= k) = 2 p k in the density form, capped at 1) against the number
seen, over every governor with p (1986-2024) and over 2006-2024 alone; the same in share (within x points of
even); and against data/congress/history.json's governor row. Also what the normal beside the t4 would give.
"""
import os
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402

KS = (1, 10, 100, 1000, 5000, 10000, 20000, 50000)
PTS = (0.0025, 0.005, 0.01, 0.02, 0.05)


def poisson_tail(expected, seen):
    """P(X <= seen) and P(X >= seen) for X ~ Poisson(expected)."""
    return float(stats.poisson.cdf(seen, expected)), float(stats.poisson.sf(seen - 1, expected))


def run(span, label):
    exp = {k: 0.0 for k in KS}
    seen = {k: 0 for k in KS}
    exp_n = {k: 0.0 for k in KS}
    exp_pt = {x: 0.0 for x in PTS}
    seen_pt = {x: 0 for x in PTS}
    n = 0
    own = 0
    cases = []
    for y in span:
        path = os.path.join(L.DATA, "governor", f"{y}.json")
        if not os.path.exists(path):
            continue
        doc = L.load_json(path)
        for c in doc["contests"]:
            p = c.get("p") or {}
            if not p.get("value"):
                continue
            n += 1
            tp = c["two_party"]
            margin = abs(tp["votes"][0] - tp["votes"][1])
            nn = p["n"]
            f = c["forecasts"][p["of_forecast"]]
            mean, sd, tails = f["share"]["mean"], f["share"]["sd"], f["share"]["tails"]
            if f["by"] == "the model's own":
                own += 1
            share = tp["votes"][0] / sum(tp["votes"])
            dshare = abs(share - 0.5)
            for k in KS:
                exp[k] += min(1.0, 2 * p["value"] * k)
                seen[k] += margin <= k
            # the normal beside it (the model's own only; 538's is normal already)
            fn = next((g for g in c["forecasts"] if g["by"] == "the model's own" and g["share"]["tails"] == "normal"), None)
            if fn:
                pn = L.p_density(nn, L.f_half(fn["share"]["mean"], fn["share"]["sd"], "normal"))
                if f["by"] == "the model's own":
                    mult = p["value"] / L.p_density(nn, L.f_half(mean, sd, tails))
                    pn *= mult
                else:
                    pn = p["value"]
                for k in KS:
                    exp_n[k] += min(1.0, 2 * pn * k)
            for x in PTS:
                exp_pt[x] += float(L.cdf(0.5 + x, mean, sd, tails) - L.cdf(0.5 - x, mean, sd, tails))
                seen_pt[x] += dshare <= x
            if margin <= 5000:
                cases.append((c["id"], margin, p["value"], p["under"][:24]))
    print(f"  {label}: {n} contests with p ({own} under the model's own, {n - own} under 538)")
    print(f"    {'k votes':>8s} {'expected':>9s} {'seen':>5s} {'P(X<=seen)':>11s} {'P(X>=seen)':>11s}   {'expected, normal first':>22s}")
    for k in KS:
        lo, hi = poisson_tail(exp[k], seen[k])
        print(f"    {k:8d} {exp[k]:9.2f} {seen[k]:5d} {lo:11.3f} {hi:11.3f}   {exp_n[k]:22.2f}")
    print(f"    in share: " + "; ".join(f"within {x * 100:g} pt: {exp_pt[x]:.1f} expected, {seen_pt[x]} seen" for x in PTS))
    print(f"    decided by 5,000 votes or fewer: {cases}")
    return exp, seen


def main():
    print("C13. THE GOVERNOR TEST AGAIN AFTER #38: CONTESTS DECIDED BY k VOTES OR FEWER, EXPECTED AGAINST SEEN")
    print(f"repository HEAD {L.git_head()}")
    e1, s1 = run(range(1986, 2025, 2), "every governor with p, 1986-2024")
    e2, s2 = run(range(2006, 2025, 2), "2006-2024 (the span of the first pass)")
    e3, s3 = run(range(1986, 2005, 2), "1986-2004 (Algara and Amlani's years)")
    h = L.load_json(os.path.join(L.DATA, "congress", "history.json"))["by_level"]["governor"]
    print(f"  history.json's governor row: contests {h['contests']}; " + "; ".join(f"k={k}: {h['expected'][str(k)]:.2f}/{h['seen'][str(k)]}" for k in (1, 1000, 5000, 10000, 20000)))
    print(f"  here, 1986-2024: " + "; ".join(f"k={k}: {e1[k]:.2f}/{s1[k]}" for k in (1, 1000, 5000, 10000, 20000)))
    print("  the first pass (M2-REPORT 3.1, D2 #24, 2006-2024, normal first, no last race): within 5,000 votes 4.38 expected, 0 seen (P 0.013)")


if __name__ == "__main__":
    main()
