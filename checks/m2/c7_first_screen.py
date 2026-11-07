"""C7. The figures a reader sees first, recomputed by hand (briefs/M2-check-computed-p.md, item 6): the closest
states of 2024, 2020, 2016 and 2008 and the average voter's p each year (data/president/REPORT.md section 1's
table and each year's file summary), and the closest House, Senate and governor races (data/congress/REPORT.md
section 5's table). "By hand" here: each figure from its contest's own forecast numbers and count by the formulas
of model/MATH.md written out again in this script (the normal density, the t4 density, the convolution of the
own forecast's two errors by quadrature, the Economist's window count), not by any pipeline function; W is the
record's (recomputed independently in c2_college.py).
"""
import math
import os
import re
import sys

import numpy as np
from scipy import integrate, stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402

SQRT2 = math.sqrt(2.0)


def normal_density_at_half(mean, sd):
    z = (0.5 - mean) / sd
    return math.exp(-0.5 * z * z) / (sd * math.sqrt(2 * math.pi))


def t4_density(x, scale):
    # the Student-t with 4 degrees of freedom: (3/8) (1 + x^2/4)^(-5/2) / scale
    u = x / scale
    return 0.375 * (1 + u * u / 4.0) ** -2.5 / scale


def own_density_at_half(mean, s_nat, s_state):
    """v = mean + delta + eps, delta ~ N(0, s_nat^2), eps ~ t4 with scale s_state / sqrt2: the density at 1/2 is
    the integral over delta of the normal density times the t4 density at 1/2 - mean - delta."""
    f = lambda d: math.exp(-0.5 * (d / s_nat) ** 2) / (s_nat * math.sqrt(2 * math.pi)) * t4_density(0.5 - mean - d, s_state / SQRT2)
    v, _ = integrate.quad(f, -12 * s_nat, 12 * s_nat, limit=200)
    return v


def one_in(p):
    return f"1 in {round(1 / p):,}"


def main():
    print("C7. THE FIRST-SCREEN FIGURES, BY HAND")
    print(f"repository HEAD {L.git_head()}")
    rep = open(os.path.join(L.ROOT, "data", "president", "REPORT.md")).read()
    table = {}
    for m in re.finditer(r"^\| (\d{4}) \| ([\d,]+) \| ([^|]+) \|", rep, re.M):
        table.setdefault(int(m.group(1)), (int(m.group(2).replace(",", "")), m.group(3).strip()))   # section 1's table comes first
    print("7.1 The presidency: each year's average voter (vote-weighted mean of the states' p) and the closest states, against the files and data/president/REPORT.md")
    print(f"    {'year':>4s} {'avg p by hand':>13s} {'1 in':>14s} {'file':>14s} {'REPORT':>14s}   closest states by hand (REPORT in brackets)")
    for path in L.president_files():
        doc = L.load_json(path)
        y = doc["year"]
        if not doc.get("summary"):
            continue
        states = [c for c in doc["contests"] if c["p"] and c["result"] and not c["place"]["district"]]
        num = sum(c["p"]["value"] * c["result"]["two_party"] for c in states)
        den = sum(c["result"]["two_party"] for c in states)
        avg = num / den
        top = sorted(states, key=lambda c: -c["p"]["value"])[:3]
        hand = []
        for c in top:
            under = c["p"]["under"]
            n = c["result"]["two_party"] - 1
            assert n == c["p"]["n_other_voters"]
            W = c["p"]["W"]
            if under == "the model's own":
                f = next(f for f in c["forecasts"] if f["by"] == "the model's own")["share"]
                fh = own_density_at_half(f["mean"], f["national_sd"], f["state_sd"])
                p = fh / (2 * n) * W
            elif under.startswith("538"):
                model = under.split("(")[1].rstrip(")")
                f = next(f for f in c["forecasts"] if f["by"] == "538" and f.get("model") == model)["share"]
                fh = normal_density_at_half(f["mean"], f["sd"])
                p = fh / (2 * n) * W
            else:   # the Economist: weighted decisive draws / (draws x width) / (2n)
                pb = c["p"]
                p = pb["window_weighted"] / (80000 * pb["window_width"]) / (2 * n)
            hand.append((c["place"]["state"], p, c["p"]["value"]))
        ok = all(abs(p / rec - 1) < 1e-6 for _, p, rec in hand)
        print(f"    {y:4d} {avg:13.4e} {one_in(avg):>14s} {one_in(doc['summary']['vote_weighted_mean_p']):>14s} {'1 in ' + format(table[y][0], ','):>14s}   "
              + ", ".join(f"{s} {one_in(p)}" for s, p, _ in hand) + f"  [{table[y][1]}]" + ("" if ok else "   <-- DIFFERS from the file"))
    print("7.2 The closest House, Senate and governor races: the largest p of each year and level by hand (normal density at the forecast's mean and sd, "
          "over twice the count), against the file and data/congress/REPORT.md section 5 (the file's mean and sd are rounded to six decimals, "
          "so the last digit of '1 in' can differ by one)")
    rep = open(os.path.join(L.ROOT, "data", "congress", "REPORT.md")).read()
    ctable = {}
    for m in re.finditer(r"^\| (\d{4}) (Senate|House|governor) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| ([^|]+) \| ([^|]*)\|", rep, re.M):
        ctable[(int(m.group(1)), m.group(2).lower())] = (m.group(8).strip(), m.group(9).strip())
    print(f"    {'year, level':16s} {'contest':22s} {'mean':>8s} {'sd':>8s} {'n':>10s} {'f(1/2)':>8s} {'p by hand':>10s} {'1 in':>14s} {'file':>14s}   REPORT")
    for level in ("senate", "house", "governor"):
        for path in L.congress_files(level):
            doc = L.load_json(path)
            y = doc["year"]
            with_p = [c for c in doc["contests"] if (c.get("p") or {}).get("value")]
            if not with_p:   # since D2's #29 House 2006 carries no p (no lagged inputs); read only
                print(f"    {y} {level}: no contest with p in the file")
                continue
            best = max(with_p, key=lambda c: c["p"]["value"])
            under = best["p"]["under"]
            if under.startswith("538"):
                ver = under.split("(")[1].split(")")[0]
                f = next(f for f in best["forecasts"] if f["by"] == "538" and f.get("version") == ver)["share"]
            else:
                f = next(f for f in best["forecasts"] if f["by"] == "the model's own" and f["share"]["tails"] == "normal")["share"]
            n = best["p"]["n"]
            fh = normal_density_at_half(f["mean"], f["sd"])
            p = fh / (2 * n)
            rec = best["p"]["value"]
            rpt = ctable.get((y, level), ("?", ""))[0]
            flag = "" if abs(p / rec - 1) < 2e-4 else "   <-- DIFFERS from the file"
            print(f"    {str(y) + ' ' + level:16s} {best['id']:22s} {f['mean']:8.4f} {f['sd']:8.4f} {n:10,d} {fh:8.3f} {p:10.3e} {one_in(p):>14s} {one_in(rec):>14s}   {rpt}{flag}")


if __name__ == "__main__":
    main()
