"""C4b. The presidency's own forecast (horizon and t4 scale) and 538's implied-sd rule (item 3, continued).

4.3 The model's own presidential forecast (pipeline/own_forecast.py) is refitted here from the record's inputs
    (data/president/inputs/: the FEC and MEDSL results, 538's national averages on 9 September and on the eve)
    and compared with the national and state error sds in every year's file. The 2024 horizon: the input is
    538's average of 12 September 2024 (the last reachable), and the errors are fitted to the 9 September
    averages of 1976-2020; the eve fit is shown beside it for the size of the difference. The t4 scale: the
    record's state error is t4 with scale sd/sqrt(2), so that its variance equals sd^2; the alternative reading
    (scale = sd) is shown for the size of the difference. The two t4 cdf formulas in the pipeline's code are
    checked against scipy, retyped here.
4.4 538's implied sd = (mean - 1/2) / Phi^-1(chance), kept where its estimated relative error is under 20%:
    the simulation-run counts the record inferred from the step in 538's chances are re-measured from the
    four checking-our-work CSVs (fetched outside the repository, sha256 printed); the error of every entry is
    recomputed; and the error's effect on p, which is what the site shows, is measured: d ln f(1/2) / d ln sd
    = z^2 - 1, so a 20% sd error is a 60% p error at z = 2 and a 160% one at z = 3.
"""
import csv
import math
import os
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402

INPUTS = os.path.join(L.DATA, "president", "inputs")
YEARS = list(range(1976, 2025, 4))
SQRT2 = math.sqrt(2.0)
CSV_SHA = {   # measured at fetch time this session (checks/m2/OUTPUT.txt records the run)
    "fte_presidential_elections.csv": "president", "fte_us_senate_elections.csv": "senate",
    "fte_us_house_elections.csv": "house", "fte_governors_elections.csv": "governor"}


def results():
    fec = L.load_json(os.path.join(INPUTS, "fec_president.json"))["years"]
    medsl = L.load_json(os.path.join(INPUTS, "medsl_president.json"))["years"]
    out = {}
    for y in YEARS:
        if str(y) in fec:
            out[y] = {s: (v["dem"], v["rep"]) for s, v in fec[str(y)].items()}
        else:
            out[y] = {s: (v["dem"]["votes"], v["rep"]["votes"]) for s, v in medsl[str(y)].items()}
    return out


def shares(res):
    v = {y: {s: d / (d + r) for s, (d, r) in st.items()} for y, st in res.items()}
    V = {y: sum(d for d, _ in st.values()) / sum(d + r for d, r in st.values()) for y, st in res.items()}
    return v, V


def polls(when):
    doc = L.load_json(os.path.join(INPUTS, "fte_poll_averages.json"))["years"]
    out = {}
    for y, d in doc.items():
        us = d[when]["units"]["US"]
        dem = us["dem"] if us["dem"] is not None else us["dem_trend_adjusted"]
        rep = us["rep"] if us["rep"] is not None else us["rep_trend_adjusted"]
        out[int(y)] = (dem / (dem + rep), d[when]["date"])
    return out


def fit(t, v, V, N):
    nat_years = [y for y in YEARS if y < t and y in N]
    nat_res = [V[y] - N[y] for y in nat_years]
    s_nat = math.sqrt(sum(r * r for r in nat_res) / len(nat_res))
    st_res = []
    for y in YEARS:
        if 1980 <= y < t:
            sw = V[y] - V[y - 4]
            st_res += [(v[y][s] - v[y - 4][s]) - sw for s in v[y]]
    s_state = math.sqrt(sum(r * r for r in st_res) / len(st_res))
    return s_nat, s_state, nat_years, nat_res


def t4_cdf_own(x):
    """pipeline/own_forecast.T4, retyped: 1/2 + (1/2) sin(a) (1 + cos(a)^2 / 2), a = atan(x/2)."""
    a = math.atan(x / 2.0)
    return 0.5 + 0.5 * math.sin(a) * (1 + 0.5 * math.cos(a) ** 2)


def t4_cdf_chambers(x):
    """pipeline/chambers.t4_cdf, retyped: 1/2 + x (x^2 + 6) / (2 (x^2 + 4)^1.5)."""
    t2 = x * x
    return 0.5 + x * (t2 + 6.0) / (2.0 * (t2 + 4.0) ** 1.5)


def main():
    print("C4b. THE PRESIDENCY'S OWN FORECAST (HORIZON, t4 SCALE) AND 538'S IMPLIED-SD RULE")
    print(f"repository HEAD {L.git_head()}")
    # ------------------------------------------------------------------ 4.3
    print("4.3 The model's own presidential forecast, refitted from the record's inputs")
    res = results()
    v, V = shares(res)
    two = polls("two_months_out")
    eve = polls("eve")
    print("    538's national averages in the record: year, 9 September (date), eve (date), two-party Democratic share; the result")
    for y in YEARS:
        print(f"      {y}: {two[y][0]:.4f} ({two[y][1]}), {eve[y][0]:.4f} ({eve[y][1]}); result {V[y]:.4f}")
    N_two = {y: s for y, (s, _) in two.items()}
    N_eve = {y: s for y, (s, d) in eve.items() if d[5:] >= "11-01"}
    print("    year, the poll the record used, s_nat and s_state here vs the record's file; and s_nat under the other horizon")
    worst = 0.0
    for y in range(1984, 2025, 4):
        doc = L.load_json(os.path.join(L.DATA, "president", f"{y}.json"))
        own = next(f for c in doc["contests"] for f in c["forecasts"] if f["by"] == "the model's own")
        used_eve = eve[y][1][5:] >= "11-01"
        N = N_eve if used_eve else N_two
        s_nat, s_state, nat_years, nat_res = fit(y, v, V, N)
        s_nat_other, _, other_years, _ = fit(y, v, V, N_two if used_eve else N_eve)
        worst = max(worst, abs(s_nat - own["share"]["national_sd"]), abs(s_state - own["share"]["state_sd"]))
        print(f"      {y}: {'eve' if used_eve else 'input ' + eve[y][1] + ', errors at 9 September'} ({eve[y][1] if used_eve else two[y][1]}); s_nat {s_nat:.6f} (record {own['share']['national_sd']:.6f}), "
              f"s_state {s_state:.6f} (record {own['share']['state_sd']:.6f}); {len(nat_years)} cycles {nat_years[0]}-{nat_years[-1]}; "
              f"s_nat under the {'9 September' if used_eve else 'eve'} horizon: {s_nat_other:.4f} ({len(other_years)} cycles)")
    print(f"    largest difference from the record's sds: {worst:.1e}")
    # 2024: the horizon's weight on p
    doc = L.load_json(os.path.join(L.DATA, "president", "2024.json"))
    pa = next(c for c in doc["contests"] if c["id"] == "2024-president-PA")
    own = next(f for f in pa["forecasts"] if f["by"] == "the model's own")
    s_nat, s_state = own["share"]["national_sd"], own["share"]["state_sd"]
    s_nat_eve, _, _, _ = fit(2024, v, V, N_eve)
    mean = own["share"]["mean"]
    fh_rec = L.own_pres_pdf(0.5, mean, s_nat, s_state)
    fh_eve = L.own_pres_pdf(0.5, mean, s_nat_eve, s_state)
    print(f"    2024 Pennsylvania (mean {mean:.5f}): the input is the 12 September average, the national error sd {s_nat:.4f} is fitted to the "
          f"9 September averages of 1976-2020 (a horizon 3 days longer than the input's). f(1/2) {fh_rec:.4f} (record {own['p']['f_half']:.4f}). "
          f"With the eve-fitted national sd ({s_nat_eve:.4f}, 1976-2020), which no 2024 eve average exists to pair with, f(1/2) would be {fh_eve:.4f} "
          f"({fh_eve / fh_rec:.3f} x); W would move too (not recomputed: no such forecast is proposed)")
    # 2024 national input: how far the 12 September average sat from the result
    print(f"    the 12 September 2024 average {two[2024][0]:.4f} ({two[2024][1]}) against the result {V[2024]:.4f}: residual {V[2024] - two[2024][0]:+.4f}, "
          f"{(V[2024] - two[2024][0]) / s_nat:+.2f} national sds")
    # t4 scale
    print("    t4 scale: the record's state error is t4 with scale s_state / sqrt(2) (variance = s_state^2). Alternative readings for 2024 PA:")
    for label, s_st, tails in (("record: t4, scale sd/sqrt2 (sd matched)", s_state, "t4"),
                               ("t4 with scale = sd (variance 2 sd^2)", s_state * SQRT2, "t4"),
                               ("normal state error, same sd", s_state, "normal")):
        if tails == "t4":
            fh = L.own_pres_pdf(0.5, mean, s_nat, s_st)
        else:
            fh = stats.norm.pdf(0.5, mean, math.sqrt(s_nat ** 2 + s_st ** 2))
        print(f"      {label:44s} f(1/2) {fh:.4f}  ratio to the record {fh / fh_rec:.3f}")
    xs = [-3.0, -1.5, -0.7, 0.0, 0.4, 1.2, 2.5, 5.0]
    e1 = max(abs(t4_cdf_own(x) - stats.t.cdf(x, 4)) for x in xs)
    e2 = max(abs(t4_cdf_chambers(x) - stats.t.cdf(x, 4)) for x in xs)
    print(f"    the pipeline's two t4 cdf formulas (own_forecast.T4, chambers.t4_cdf), retyped, against scipy.stats.t.cdf(x, 4) at {len(xs)} points: "
          f"largest differences {e1:.1e}, {e2:.1e}; both are applied at z sqrt(2) = (x - mean) / (sd / sqrt(2)), the sd-matched scale")

    # ------------------------------------------------------------------ 4.4
    print("4.4 538's implied sd: the run counts re-measured from the chances' steps, every entry's error recomputed, and the error's effect on p")
    cands = (500, 1000, 2000, 2500, 4000, 5000, 8000, 10000, 20000, 25000, 40000, 50000, 80000, 100000, 200000)
    measured = {}
    for fname, level in CSV_SHA.items():
        path = os.path.join(L.CACHE, fname)
        if not os.path.exists(path):
            print(f"  {fname} not in the cache; skipped")
            continue
        print(f"  {fname}: sha256 {L.sha256(path)}")
        rows = list(csv.DictReader(open(path)))
        by = {}
        for r in rows:
            try:
                q = float(r["probwin"])
            except ValueError:
                continue
            if 0 < q < 1:
                by.setdefault((r["year"], r["forecast_type"] or "-"), []).append((q, r["probwin"]))
        for (year, vt), vals in sorted(by.items()):
            qs = np.array([q for q, _ in vals])
            decimals = max(len(s.split(".")[1]) if "." in s else 0 for _, s in vals)
            fits = {N: float(np.mean(np.abs(qs * N - np.round(qs * N)) < 1e-6)) for N in cands}
            N_fit = next((N for N in cands if fits[N] >= 0.99), None)
            N_all = next((N for N in cands if fits[N] >= 0.999999), None)
            uniq = np.unique(qs)
            gaps = np.diff(uniq)
            if N_fit is None:
                # the record's inference may rest on the races alone: the chances off every step are listed
                top = max(fits.values())
                best = next(N for N in cands if fits[N] >= top - 0.005)     # the coarsest step that fits as well
                off = sorted({(r_["state"], r_["party"], r_["probwin"]) for r_ in rows if r_["year"] == year and (r_["forecast_type"] or "-") == vt
                              and r_["probwin"] and 0 < float(r_["probwin"]) < 1 and abs(float(r_["probwin"]) * best - round(float(r_["probwin"]) * best)) >= 1e-6})
                print(f"        no N fits 99%: the best is {best} at {fits[best]:.4f}; the rows off that step are {sorted({o[0] for o in off})} "
                      f"(e.g. {off[0] if off else None}); with those rows aside the step is {best}" if fits[best] >= 0.95 else
                      f"        no N fits 99%: the best is {best} at {fits[best]:.4f}")
                if fits[best] >= 0.95:
                    N_fit = best
            measured[(level, year, vt)] = N_fit
            print(f"      {level} {year} {vt:11s}: {len(qs):6d} chances, printed to {decimals} decimals, {len(uniq)} distinct; smallest step between distinct "
                  f"chances {gaps.min():.2e}; smallest N with 99% whole multiples of 1/N: {N_fit} (fit {fits[N_fit] if N_fit else float('nan'):.4f}); "
                  f"with every chance: {N_all}")
    # the record's inferred counts
    fte_p = L.load_json(os.path.join(INPUTS, "fte_president_forecasts.json"))["years"]
    print("    the record's run counts (presidency: runs_inferred; Congress: each 538 entry's 'simulations') against the re-measurement:")
    for y, models in sorted(fte_p.items()):
        for mname, m in models.items():
            key = ("president", y, mname if mname != "default" else "-")
            print(f"      president {y} {mname:11s}: record {m.get('runs_inferred')} (step {m.get('probwin_step')}); re-measured {measured.get(key, measured.get(('president', y, '-')))}")
    rec_sims = {}
    for level in ("senate", "house", "governor"):
        for path in L.congress_files(level):
            doc = L.load_json(path)
            for c in doc["contests"]:
                for f in c["forecasts"]:
                    if f["by"] == "538" and f.get("simulations") is not None:
                        rec_sims[(level, str(c["year"]), f.get("version") or "-")] = f.get("simulations")
    for key in sorted(rec_sims):
        mk = key
        print(f"      {key[0]} {key[1]} {key[2]:11s}: record {rec_sims[key]}; re-measured {measured.get(mk)}"
              f"{'' if rec_sims[key] == measured.get(mk) else '   <-- differs'}")
    # every Congress entry's error recomputed
    print("    every Congress 538 entry's sd relative error recomputed (chance sampling error sqrt(q(1-q)/N) carried through Phi^-1 at both ends, "
          "and the two-party mean's rounding at half the last printed digit of the percent, in quadrature) against the record's sd_relative_error:")
    share_dec = {}   # decimals of the printed percent shares, from the CSVs
    for fname, level in CSV_SHA.items():
        path = os.path.join(L.CACHE, fname)
        if not os.path.exists(path):
            continue
        for r in csv.DictReader(open(path)):
            s = r["projected_voteshare"]
            if s:
                k = (level, r["year"], r["forecast_type"] or "-")
                share_dec[k] = max(share_dec.get(k, 0), len(s.split(".")[1]) if "." in s else 0)
    amp = []
    worst, n_cmp, n_bad = 0.0, 0, 0
    for level in ("senate", "house", "governor"):
        for path in L.congress_files(level):
            doc = L.load_json(path)
            for c in doc["contests"]:
                for f in c["forecasts"]:
                    if f["by"] != "538" or not f.get("share") or f["share"].get("sd") is None:
                        continue
                    ch = f["chance"]
                    dk = "D" if "D" in ch else "I"
                    q = ch[dk] / (ch[dk] + ch["R"])
                    mean, sd = f["share"]["mean"], f["share"]["sd"]
                    z = stats.norm.ppf(q)
                    N = f.get("simulations")
                    if N:
                        dq = math.sqrt(q * (1 - q) / N)
                        ends = [q - dq, q + dq]
                        rel_q = math.inf if min(ends) <= 0 or max(ends) >= 1 else max(abs(stats.norm.ppf(e) - z) for e in ends) / abs(z)
                    else:
                        rel_q = 0.0
                    dec = share_dec.get((level, str(c["year"]), f.get("version") or "-"), 5)
                    d_share = 0.5 * 10 ** -(dec + 2)
                    rel_m = d_share / abs(mean - 0.5)
                    rel = math.sqrt(rel_q ** 2 + rel_m ** 2)
                    rec = f.get("sd_relative_error")
                    if rec is not None and not math.isinf(rel):
                        n_cmp += 1
                        d = abs(rel - rec)
                        worst = max(worst, d)
                        if d > 6e-4:
                            n_bad += 1
                            if n_bad <= 5:
                                print(f"      differs: {c['id']} {f.get('version')}: here {rel:.4f}, record {rec:.4f} (decimals here {dec})")
                    zz = (mean - 0.5) / sd
                    first = c["p"].get("value") and c["p"]["under"].startswith(f"538 ({f.get('version')})")
                    amp.append((level, c["year"], c["id"], f.get("version"), zz, rel if not math.isinf(rel) else float("nan"),
                                abs(zz * zz - 1) * (rel if not math.isinf(rel) else float("nan")), bool(first), f.get("unusable_kind")))
    print(f"      {n_cmp} entries compared; largest difference {worst:.2e} (the record rounds to four decimals); {n_bad} beyond 6e-4")
    # the presidency's recorded errors
    worst_p, n_p = 0.0, 0
    for y in (2008, 2012, 2016, 2020):
        doc = L.load_json(os.path.join(L.DATA, "president", f"{y}.json"))
        for c in doc["contests"]:
            for f in c["forecasts"]:
                if f["by"] != "538" or not f.get("share") or f["share"].get("sd") is None:
                    continue
                e = f["share"]["sd_rel_error"]
                q = f["win_prob"]
                mean, sd = f["share"]["mean"], f["share"]["sd"]
                z = stats.norm.ppf(q)
                N = e["runs"]
                dq = math.sqrt(q * (1 - q) / N)
                ends = [q - dq, q + dq]
                rel_q = math.inf if min(ends) <= 0 or max(ends) >= 1 else max(abs(stats.norm.ppf(x) - z) for x in ends) / abs(z)
                rel = math.sqrt(rel_q ** 2 + (e["mean_rounding"] / abs(mean - 0.5)) ** 2)
                n_p += 1
                worst_p = max(worst_p, abs(rel - e["value"]))
                zz = (mean - 0.5) / sd
                first = c["p"] and c["p"]["under"] == f"538 ({f['model']})"
                amp.append(("president", y, c["id"], f["model"], zz, rel, abs(zz * zz - 1) * rel, bool(first), None))
    print(f"      presidency: {n_p} entries' sd_rel_error.value recomputed from the recorded runs and mean rounding; largest difference {worst_p:.1e}")
    # the amplification
    print("    the error's effect on p: relative error of p = |z^2 - 1| x relative error of sd, z = (mean - 1/2) / sd")
    print(f"      {'where':22s} {'entries':>7s} {'sd err median':>13s} {'p err median':>12s} {'p err 90%':>9s} {'p err max':>9s} {'p err >= 20%':>12s} {'>= 50%':>7s} {'>= 100%':>8s}")
    groups = {}
    for a in amp:
        groups.setdefault((a[0], "site's p (538 first)" if a[7] else "kept beside (not first)"), []).append(a)
    for (level, which), g in sorted(groups.items()):
        pe = np.array([x[6] for x in g if not math.isnan(x[6])])
        se = np.array([x[5] for x in g if not math.isnan(x[5])])
        print(f"      {level + ', ' + which:38s} {len(g):7d} {np.median(se):13.3f} {np.median(pe):12.3f} {np.quantile(pe, 0.9):9.3f} {pe.max():9.3f} "
              f"{int((pe >= 0.2).sum()):12d} {int((pe >= 0.5).sum()):7d} {int((pe >= 1.0).sum()):8d}")
    first = [a for a in amp if a[7]]
    worst_first = sorted(first, key=lambda a: -(a[6] if not math.isnan(a[6]) else 0))[:8]
    print("      the site's 538-first entries with the largest p error:")
    for a in worst_first:
        print(f"        {a[2]:24s} {a[3] or '':11s} z {a[4]:+6.2f} sd err {a[5]:.3f} -> p err {a[6]:.2f}")
    rejected = [a for a in amp if a[8] == "implied sd's error 20% or more"]
    ok_by_p = [a for a in rejected if not math.isnan(a[6]) and a[6] < 0.2]
    first_bad = [a for a in first if not math.isnan(a[6]) and a[6] >= 0.2]
    print(f"      under a rule on p's error instead (|z^2 - 1| x sd error < 20%): of the {len(rejected)} Congress entries the record rejects for the sd's error, "
          f"{len(ok_by_p)} would pass (their z is near 1, where p hardly depends on sd); of the {len(first)} entries the site shows first, "
          f"{len(first_bad)} would fail")


if __name__ == "__main__":
    main()
