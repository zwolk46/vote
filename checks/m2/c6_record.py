"""C6. The record against the forecasts, the presidency (MATH section 8.2; briefs/M2-check-computed-p.md, item 5):
contests decided by k votes or fewer, expected under the forecast each p rests on, against the number seen,
1984-2024 (the years with p), with the states nearest a tie listed. P(|D - R| <= k) = 2 p_state k in the density
form (p_state = f(1/2) / (2n)), capped at 1; the same test under the other forecasts kept beside the record's
(538's models and the Economist's) where they exist.
"""
import os
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402

KS = (1, 10, 100, 1000, 5000, 10000, 20000, 50000, 100000)


def main():
    print("C6. THE RECORD AGAINST THE FORECASTS: PRESIDENTIAL CONTESTS DECIDED BY k VOTES OR FEWER")
    print(f"repository HEAD {L.git_head()}")
    exp_all = {k: 0.0 for k in KS}
    cdf_all = {k: 0.0 for k in KS}
    seen_all = {k: 0 for k in KS}
    by_fc = {}
    cases = []
    n_contests = 0
    print(f"    {'year':>4s} {'contests':>8s} " + " ".join(f"{'k=' + str(k):>14s}" for k in KS) + "   (expected / seen)")
    for path in L.president_files():
        doc = L.load_json(path)
        y = doc["year"]
        exp = {k: 0.0 for k in KS}
        cdfe = {k: 0.0 for k in KS}
        seen = {k: 0 for k in KS}
        m = 0
        for c in doc["contests"]:
            if not c["p"] or not c["result"]:
                continue
            p_state = c["p"]["p_state"]
            margin = abs(c["result"]["dem"] - c["result"]["rep"])
            n = c["p"]["n_other_voters"]
            under = c["p"]["under"]
            f = next(f for f in c["forecasts"] if (f["by"] == under) or (f["by"] == "538" and under == f"538 ({f.get('model')})"))
            sh = f["share"]
            if under == "the model's own":
                F = lambda x: L.own_pres_cdf(x, sh["mean"], sh["national_sd"], sh["state_sd"])
            else:
                F = lambda x: stats.norm.cdf(x, sh["mean"], sh["sd"])      # the Economist: its draws' mean and sd read as a normal
            m += 1
            for k in KS:
                exp[k] += min(1.0, 2 * p_state * k)
                cdfe[k] += F(0.5 + k / (2 * n)) - F(0.5 - k / (2 * n))
                seen[k] += int(margin <= k)
            if margin <= 20000:
                cases.append((margin, c["id"], c["p"]["under"], p_state, c["result"]["two_party"]))
            # the other forecasts kept beside
            for f in c["forecasts"]:
                if not f.get("p") or not f["p"].get("p_state"):
                    continue
                key = (f["by"] + (f" {f['model']}" if f.get("model") else ""))
                d = by_fc.setdefault(key, {"n": 0, "exp": {k: 0.0 for k in KS}, "seen": {k: 0 for k in KS}, "years": set()})
                d["n"] += 1; d["years"].add(y)
                for k in KS:
                    d["exp"][k] += min(1.0, 2 * f["p"]["p_state"] * k)
                    d["seen"][k] += int(margin <= k)
        if m == 0:
            print(f"    {y:4d}: no p")
            continue
        n_contests += m
        for k in KS:
            exp_all[k] += exp[k]; seen_all[k] += seen[k]; cdf_all[k] += cdfe[k]
        print(f"    {y:4d} {m:8d} " + " ".join(f"{exp[k]:7.3f} / {seen[k]:<4d}" for k in KS))
    print(f"    {'all':>4s} {n_contests:8d} " + " ".join(f"{exp_all[k]:7.3f} / {seen_all[k]:<4d}" for k in KS))
    print(f"    {'cdf':>4s} {'':8s} " + " ".join(f"{cdf_all[k]:7.3f} / {seen_all[k]:<4d}" for k in KS)
          + "   (expected by the forecast's cdf over the band, which the density form at 1/2 understates where the mean is far from even)")
    print("    P(seen or fewer | the forecasts), Poisson, cdf form: " + ", ".join(f"k={k}: {stats.poisson.cdf(seen_all[k], cdf_all[k]):.3f}" for k in KS))
    print("    P(seen or more | the forecasts), cdf form: " + ", ".join(f"k={k}: {1 - stats.poisson.cdf(seen_all[k] - 1, cdf_all[k]):.3f}" for k in KS))
    print("    the contests decided by 20,000 votes or fewer, with the forecast's P(within that margin):")
    for margin, cid, under, p_state, n2 in sorted(cases):
        print(f"      {cid:22s} margin {margin:6d} of {n2:>10,d}; p_state {p_state:.3e}; P(|D-R| <= margin) {min(1, 2 * p_state * margin):.3f}; under {under[:40]}")
    print("    the same test under every forecast kept in the record (its own p_state), over the contests it covers:")
    for key, d in sorted(by_fc.items()):
        yrs = sorted(d["years"])
        print(f"      {key:28s} {d['n']:4d} contests, {yrs[0]}-{yrs[-1]}: " + " ".join(f"k={k}: {d['exp'][k]:.2f}/{d['seen'][k]}" for k in (100, 1000, 5000, 10000, 20000, 50000)))


if __name__ == "__main__":
    main()
