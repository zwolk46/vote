"""C4. The forecasts behind Senate, House and governor p (briefs/M2-check-computed-p.md, item 3):
  4.1 the governors' miss (no race within 5,000 votes against 4.4 expected; 61% of races inside the 50%
      interval): the cause, and options with what each does to the governors' p (none applied);
  4.2 leave-one-cycle-out (the record's scheme, D2-v1) against a fit on earlier cycles only: the change in p
      by level and cycle.
The model is refitted here by M2's own code from the record's inputs (data/<level>/<year>.json: the
Democrat's two-party share, lean, incumbency, the sitting president and the midterm flag), without
pipeline/. The governors' rows reproduce the record's fit exactly (232 races; coefficients to 1e-7). For
the Senate and the House the record's fit used Cha, Kuriwaki and Snyder's candidate rows, whose party
coding this re-reading of the FEC lines cannot reproduce in full (minor write-in and fusion lines), so the
Senate and House sets here are smaller by a few per cent and the coefficients differ in the third decimal;
every comparison in 4.2 is between two fits on the same rows.
"""
import math
import os
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402

YEARS = list(range(2006, 2025, 2))
CAP = 0.25
SQRT2 = math.sqrt(2.0)


def merged_candidates(c):
    by = {}
    for a in c["result"]["candidates"]:
        if not a.get("votes"):
            continue
        k = (a.get("name") or "").strip().upper()
        e = by.setdefault(k, {"votes": 0, "parties": set()})
        e["votes"] += a["votes"]
        mp = L.major_party(a["party"])
        if mp:
            e["parties"].add(mp)
    return by


def rows_from_record(level):
    """One row per race whose two leading candidates (lines merged by name) are a Democrat and a Republican
    and no other candidate of either label has 2% of their vote, with the record's forecast inputs."""
    rows, reasons = [], {}
    for path in L.congress_files(level):
        doc = L.load_json(path)
        for c in doc["contests"]:
            fi = c.get("forecast_inputs") or {}
            by = merged_candidates(c)
            if len(by) < 2:
                reasons["one candidate"] = reasons.get("one candidate", 0) + 1
                continue
            top = sorted(by, key=lambda k: -by[k]["votes"])
            a, b = top[0], top[1]
            pa, pb = by[a]["parties"], by[b]["parties"]
            if not ({pa, pb} == {frozenset({"D"}), frozenset({"R"})} if False else (pa == {"D"} and pb == {"R"}) or (pa == {"R"} and pb == {"D"})):
                reasons["top two not a D and an R"] = reasons.get("top two not a D and an R", 0) + 1
                continue
            n2 = by[a]["votes"] + by[b]["votes"]
            if any(by[k]["parties"] & {"D", "R"} and by[k]["votes"] >= 0.02 * n2 for k in top[2:]):
                reasons["another D or R with 2% or more"] = reasons.get("another D or R with 2% or more", 0) + 1
                continue
            if fi.get("lean") is None or fi.get("incumbency") is None:
                reasons["no lean or incumbency recorded"] = reasons.get("no lean or incumbency recorded", 0) + 1
                continue
            d = a if pa == {"D"} else b
            own = [f for f in c["forecasts"] if f["by"] == "the model's own" and f["share"]["tails"] == "normal"]
            p = c["p"]
            own_p = None
            if p.get("value") is not None:
                if p["under"].startswith("the model's own") and "normal" in p["under"]:
                    own_p = p["value"]
                for al in p.get("alongside", []):
                    if al["under"].startswith("the model's own") and al["under"].endswith("normal"):
                        own_p = al["value"]
            rows.append({"id": c["id"], "year": c["year"], "level": level, "state": c["place"]["state"],
                         "y": by[d]["votes"] / n2, "n2": n2, "n": p.get("n"), "lean": fi["lean"], "inc": fi["incumbency"],
                         "P": 1 if fi["president_party"] == "D" else -1, "M": 1 if fi["midterm"] else 0,
                         "rec_mean": own[0]["share"]["mean"] if own else None, "rec_sd": own[0]["share"]["sd"] if own else None,
                         "rec_own_p": own_p, "site_p": p.get("value"), "site_own_first": bool(p.get("value")) and p["under"].startswith("the model's own"),
                         "f_half": p.get("f_half")})
    return rows, reasons


def ols(X, y):
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return beta, y - X @ beta


def fit(rows, years, lag=False):
    R = [r for r in rows if r["year"] in years and (not lag or r.get("lag") is not None)]
    ys = sorted({r["year"] for r in R})
    X = np.array([[1.0 if r["year"] == t else 0.0 for t in ys] + [r["lean"], r["inc"]] + ([r["lag"] - 0.5] if lag else []) for r in R])
    y = np.array([r["y"] - 0.5 for r in R])
    beta, res = ols(X, y)
    a = dict(zip(ys, beta[:len(ys)]))
    s_e = float(np.sqrt((res ** 2).sum() / (len(y) - X.shape[1])))
    x = np.minimum(np.abs(X @ beta), CAP)
    g, _ = ols(np.column_stack([np.ones_like(x), x]), np.abs(res) * math.sqrt(math.pi / 2))
    PM = {r["year"]: (r["P"], r["M"]) for r in R}
    Z = np.array([[1.0, PM[t][1] * PM[t][0], (1 - PM[t][1]) * PM[t][0]] for t in ys])
    av = np.array([a[t] for t in ys])
    c, d = ols(Z, av)
    dof = len(ys) - 3
    s_a = float(np.sqrt((d ** 2).sum() / dof)) if dof >= 1 else float("nan")
    return {"years": ys, "n": len(R), "a": a, "b_lean": float(beta[len(ys)]), "b_inc": float(beta[len(ys) + 1]),
            "b_lag": float(beta[len(ys) + 2]) if lag else None, "s_e": s_e, "g": [float(v) for v in g],
            "c": [float(v) for v in c], "s_a": s_a, "ZtZ_inv": np.linalg.inv(Z.T @ Z), "lag": lag}


def national(m, P, M):
    z = np.array([1.0, M * P, (1 - M) * P])
    return float(z @ np.array(m["c"])), m["s_a"] * math.sqrt(1.0 + float(z @ m["ZtZ_inv"] @ z))


def predict(m, r, sd_a, hetero=False):
    a_hat, _ = national(m, r["P"], r["M"])
    mean = 0.5 + a_hat + m["b_lean"] * r["lean"] + m["b_inc"] * r["inc"] + ((m["b_lag"] * (r["lag"] - 0.5)) if m["lag"] else 0.0)
    s_e = (m["g"][0] + m["g"][1] * min(abs(mean - 0.5), CAP)) if hetero else m["s_e"]
    return mean, math.sqrt(sd_a ** 2 + s_e ** 2)


def loco_rmse(rows):
    """The record's sd_a: the root-mean-square miss of the national forecast over the ten cycles, each from a
    fit on the other nine, against the full fit's year effect."""
    full = fit(rows, YEARS)
    miss = []
    for T in YEARS:
        m = fit(rows, [t for t in YEARS if t != T])
        P, M = next((r["P"], r["M"]) for r in rows if r["year"] == T)
        miss.append(full["a"][T] - national(m, P, M)[0])
    return math.sqrt(sum(x * x for x in miss) / len(miss)), miss, full


def f_half_normal(mean, sd):
    return stats.norm.pdf(0.5, mean, sd)


def f_half_t4(mean, sd):
    return stats.t.pdf(0.5, 4, mean, sd / SQRT2)


def metrics(rows, means, sds, tails="normal", label=""):
    y = np.array([r["y"] for r in rows]); m = np.array(means); s = np.array(sds); n2 = np.array([r["n2"] for r in rows])
    if tails == "normal":
        u = stats.norm.cdf((y - m) / s)
        fh = stats.norm.pdf((0.5 - m) / s) / s
    else:
        u = stats.t.cdf((y - m) / (s / SQRT2), 4)
        fh = stats.t.pdf((0.5 - m) / (s / SQRT2), 4) / (s / SQRT2)
    cov = {q: float(np.mean(np.abs(u - 0.5) <= q / 2)) for q in (0.5, 0.8, 0.95)}
    z = (y - m) / s
    within1 = float(sum((stats.norm.cdf((0.51 - mi) / si) - stats.norm.cdf((0.49 - mi) / si)) if tails == "normal" else
                        (stats.t.cdf((0.51 - mi) / (si / SQRT2), 4) - stats.t.cdf((0.49 - mi) / (si / SQRT2), 4)) for mi, si in zip(m, s)))
    p = fh / (2 * n2)
    exp5k = float(np.sum(np.minimum(1.0, 2 * p * 5000)))
    ls = float(np.mean(np.log(fh * 0 + (stats.norm.pdf((y - m) / s) / s if tails == "normal" else stats.t.pdf((y - m) / (s / SQRT2), 4) / (s / SQRT2)))))
    return {"cover": cov, "z_sd": float(z.std(ddof=1)), "within1_exp": within1, "within1_seen": int(np.sum(np.abs(y - 0.5) <= 0.01)),
            "exp5k": exp5k, "seen5k": int(np.sum(np.abs(2 * y - 1) * n2 <= 5000)), "p": p, "log_score": ls}


def main():
    print("C4. CONGRESS AND GOVERNOR FORECASTS: THE GOVERNORS' MISS, AND LEAVE-ONE-CYCLE-OUT VS EARLIER CYCLES ONLY")
    print(f"repository HEAD {L.git_head()}")
    bt = L.load_json(os.path.join(L.DATA, "congress", "backtest.json"))
    ROWS = {}
    for level in ("governor", "senate", "house"):
        rows, reasons = rows_from_record(level)
        ROWS[level] = rows
        full = fit(rows, YEARS)
        rec = bt["fit"][level]
        print(f"  {level}: {len(rows)} rows rebuilt from the record (skipped: {reasons}); the record's fit used {rec['n']}. "
              f"Full fit here: b_lean {full['b_lean']:.4f} (record {rec['b_lean']:.4f}), b_inc {full['b_inc']:.4f} ({rec['b_inc']:.4f}), "
              f"s_e {full['s_e']:.4f} ({rec['s_e']:.4f}), s_a {full['s_a']:.4f} ({rec['s_a']:.4f})")

    # ------------------------------------------------------------------ 4.1 governors
    print("4.1 The governors")
    rows = ROWS["governor"]
    sd_a_rec = bt["national_sd"]["governor"]
    rmse, misses, full = loco_rmse(rows)
    print(f"  national sd (root-mean-square leave-one-out miss of the national forecast): here {rmse:.5f}, record {sd_a_rec:.5f}")
    # the record's leave-one-cycle-out forecasts, reproduced
    means, sds, worst = [], [], 0.0
    folds = {}
    for T in YEARS:
        folds[T] = fit(rows, [t for t in YEARS if t != T])
    for r in rows:
        mean, sd = predict(folds[r["year"]], r, rmse)
        means.append(mean); sds.append(sd)
        if r["rec_mean"] is not None:
            worst = max(worst, abs(mean - r["rec_mean"]), abs(sd - r["rec_sd"]))
    print(f"  the record's own forecast (leave-one-cycle-out) reproduced for {sum(1 for r in rows if r['rec_mean'] is not None)} races: "
          f"largest difference in mean or sd {worst:.2e} (the record rounds to six decimals)")
    base = metrics(rows, means, sds)
    y = np.array([r["y"] for r in rows]); m = np.array(means); s = np.array(sds); n2 = np.array([r["n2"] for r in rows])
    z = (y - m) / s
    u = stats.norm.cdf(z)
    print(f"  (a) calibration of the record's governor forecast, {len(rows)} races: standardized residual sd {z.std(ddof=1):.3f} "
          f"(1 if the sd is right), mean {z.mean():+.3f}, skew {stats.skew(z):+.2f}, excess kurtosis {stats.kurtosis(z):+.2f}; "
          f"PIT deciles {np.histogram(u, bins=10, range=(0, 1))[0].tolist()}; coverage 50/80/95%: "
          f"{base['cover'][0.5]:.2f}/{base['cover'][0.8]:.2f}/{base['cover'][0.95]:.2f}")
    x = np.abs(m - 0.5)
    for lo, hi in ((0, 0.03), (0.03, 0.06), (0.06, 0.1), (0.1, 0.3)):
        k = (x >= lo) & (x < hi)
        print(f"      |mean - 1/2| in [{lo}, {hi}): {k.sum():3d} races; residual sd {np.std(y[k] - m[k], ddof=1):.4f} vs forecast sd {s[k].mean():.4f} "
              f"(ratio {np.std(y[k] - m[k], ddof=1) / s[k].mean():.2f}); 50% coverage {np.mean(np.abs(u[k] - 0.5) <= 0.25):.2f}")
    print("  (b) races near even, expected under the forecast vs seen: in share, |y - 1/2| <= h")
    for h in (0.0025, 0.005, 0.01, 0.02, 0.05):
        e = float(sum(stats.norm.cdf((0.5 + h - mi) / si) - stats.norm.cdf((0.5 - h - mi) / si) for mi, si in zip(m, s)))
        seen = int(np.sum(np.abs(y - 0.5) <= h))
        print(f"      h = {h:<6}: expected {e:6.2f}, seen {seen:3d}, P(seen or fewer | forecast) {stats.poisson.cdf(seen, e):.3f}")
    pr = [r for r in rows if r["site_p"] is not None]           # the races with p (the record's within-k test)
    print(f"      in votes, |D - R| <= k, over the {len(pr)} races with p, from the record's p (the site's mix of 538 and own; P = 2 p k in the density form):")
    p_site = np.array([r["site_p"] for r in pr])
    y_p = np.array([r["y"] for r in pr]); n2_p = np.array([r["n2"] for r in pr])
    for k in (1000, 2000, 5000, 10000, 20000, 50000):
        e = float(np.sum(np.minimum(1.0, 2 * p_site * k)))
        seen = int(np.sum(np.abs(2 * y_p - 1) * n2_p <= k))
        print(f"      k = {k:<6}: expected {e:6.2f}, seen {seen:3d}, P(seen or fewer) {stats.poisson.cdf(seen, e):.3f}")
    close = sorted(pr, key=lambda r: abs(2 * r["y"] - 1) * r["n2"])[:8]
    print("      the closest governor races by votes:")
    for r in close:
        print(f"        {r['id']:20s} margin {abs(2 * r['y'] - 1) * r['n2']:7.0f} votes, share {r['y']:.4f}; forecast {r['rec_mean']:.4f} +- {r['rec_sd']:.4f}"
              f"{'' if r['site_own_first'] else ' (538 first)'}")
    within1 = [r for r in pr if abs(r["y"] - 0.5) <= 0.01]
    e_cond = sum(min(1.0, 5000 / (0.02 * r["n2"])) for r in within1)
    print(f"      given the {len(within1)} races that did finish within 1 point, {e_cond:.2f} would be expected within 5,000 votes "
          f"if the forecast density were flat across the point; the chance of none is {math.exp(-e_cond):.2f}")
    own_first = np.array([r["site_own_first"] for r in pr])
    zp = np.array([(r["y"] - r["rec_mean"]) / r["rec_sd"] for r in pr])
    print(f"      the own forecast's standardized residual sd where the site's p is the model's own ({own_first.sum()} races): {zp[own_first].std(ddof=1):.3f}; "
          f"where the site's p is 538's ({(~own_first).sum()} races, 2018 and 2022): {zp[~own_first].std(ddof=1):.3f}")
    z538 = []
    for r in pr:
        if r["site_own_first"]:
            continue
        doc = L.load_json(os.path.join(L.DATA, "governor", f"{r['year']}.json"))
        c = next(c for c in doc["contests"] if c["id"] == r["id"])
        ver = c["p"]["under"].split("(")[1].split(")")[0]
        f = next(f for f in c["forecasts"] if f["by"] == "538" and f.get("version") == ver)
        z538.append((r["y"] - f["share"]["mean"]) / f["share"]["sd"])
    z538 = np.array(z538)
    print(f"      538's own forecast there (the version the site shows), standardized residual sd {z538.std(ddof=1):.3f}, mean {z538.mean():+.3f}: "
          f"538's implied sds ran wide for the governors of 2018 and 2022 [measured]")
    # ---- options, each applied to every governor race of the record (leave-one-cycle-out, as the record)
    rows_all = rows
    rows = pr
    means = [mm for mm, r in zip(means, rows_all) if r["site_p"] is not None]
    sds = [ss for ss, r in zip(sds, rows_all) if r["site_p"] is not None]
    base = metrics(rows, means, sds)
    print(f"  (c) options for the governors' own forecast over the {len(rows)} races with p, each leave-one-cycle-out as the record (nothing applied):")
    print(f"      {'option':52s} {'z sd':>5s} {'50/80/95%':>14s} {'within 1pt exp/seen':>20s} {'within 5k exp/seen':>19s} {'log score':>9s} {'p ratio median (10-90%)':>24s}")

    def show(label, mm, ss, tails="normal"):
        r_ = metrics(rows, mm, ss, tails)
        ratio = r_["p"] / base["p"]
        print(f"      {label:52s} {r_['z_sd']:5.3f} {r_['cover'][0.5]:.2f}/{r_['cover'][0.8]:.2f}/{r_['cover'][0.95]:.2f} "
              f"{r_['within1_exp']:9.1f} / {r_['within1_seen']:<8d} {r_['exp5k']:8.2f} / {r_['seen5k']:<8d} {r_['log_score']:9.3f} "
              f"{np.median(ratio):8.3f} ({np.quantile(ratio, 0.1):.2f}-{np.quantile(ratio, 0.9):.2f})")
        return r_
    show("A0 the record: normal, one s_e", means, sds)
    show("A1 t4 tails, same sd (the record's 'alongside')", means, sds, "t4")
    mh, sh = zip(*[predict(folds[r["year"]], r, rmse, hetero=True) for r in rows])
    show("A2 heteroskedastic s_e(x) = g0 + g1 min(|mean-1/2|, .25)", list(mh), list(sh))
    show("A3 sd scaled by the back-test's z sd (0.93)", means, [v * base["z_sd"] for v in sds])
    # A4: the state's last governor result as a term (available 2010 on from the record itself)
    last = {}
    for r in sorted(rows_all, key=lambda r: r["year"]):
        key = r["state"]
        r["lag"] = last.get(key)
        last[key] = r["y"]
    have = [r for r in rows_all if r.get("lag") is not None]
    full_lag = fit(have, YEARS, lag=True)
    print(f"      A4 a lagged term (the state's last governor race in the record, {len(have)} races 2010-2024): full-fit b_lag {full_lag['b_lag']:+.3f}, "
          f"b_lean {full_lag['b_lean']:.3f}, s_e {full_lag['s_e']:.4f} vs {fit(have, YEARS)['s_e']:.4f} without it on the same rows")
    yrs_lag = sorted({r["year"] for r in have})
    ml, sl, base_l_m, base_l_s = [], [], [], []
    for r in have:
        tr = [t for t in yrs_lag if t != r["year"]]
        fl = fit(have, tr, lag=True)
        f0 = fit(have, tr)
        a, b = predict(fl, r, rmse); ml.append(a); sl.append(b)
        a, b = predict(f0, r, rmse); base_l_m.append(a); base_l_s.append(b)
    b0 = metrics(have, base_l_m, base_l_s); b1 = metrics(have, ml, sl)
    print(f"         leave-one-cycle-out on those races: without lag z sd {b0['z_sd']:.3f}, 50% {b0['cover'][0.5]:.2f}, log score {b0['log_score']:.3f}; "
          f"with lag z sd {b1['z_sd']:.3f}, 50% {b1['cover'][0.5]:.2f}, log score {b1['log_score']:.3f}; p ratio median {np.median(b1['p'] / b0['p']):.3f} "
          f"({np.quantile(b1['p'] / b0['p'], 0.1):.2f}-{np.quantile(b1['p'] / b0['p'], 0.9):.2f})")

    # ------------------------------------------------------------------ 4.2 expanding window
    print("4.2 Leave-one-cycle-out (the record) against a fit on earlier cycles only, 2014-2024 (the first year with "
          "four earlier cycles for the national swing's three terms)")
    print("    p here is the model's own normal p for every row (the 'alongside' p where 538 is first); the national sd is "
          "(i) the record's, unchanged, and (ii) from earlier cycles only: the root-mean-square miss of the national forecast "
          "over the cycles before T that themselves had four earlier cycles, where three or more exist, else the fit's own prediction sd")
    for level in ("senate", "house", "governor"):
        rows = ROWS[level]
        rmse, misses, full = loco_rmse(rows)
        rec_sd = bt["national_sd"][level]
        print(f"  {level}: national sd here {rmse:.4f} (record {rec_sd:.4f})")
        print(f"      {'T':>4s} {'n':>4s} {'b_lean loco/exp':>16s} {'s_e loco/exp':>14s} {'nat fc loco/exp':>16s} {'sd_a (ii)':>9s} {'p exp/loco median (10-90%)':>27s} {'sum p ratio':>11s} {'with sd_a (ii)':>14s} {'site p affected':>15s}")
        exp_misses = []
        for T in [t for t in YEARS if t >= 2014]:
            test = [r for r in rows if r["year"] == T]
            lo = fit(rows, [t for t in YEARS if t != T])
            ex = fit(rows, [t for t in YEARS if t < T])
            P, M = test[0]["P"], test[0]["M"]
            a_lo, _ = national(lo, P, M)
            a_ex, sd_ols = national(ex, P, M)
            exp_misses.append(full["a"][T] - a_ex)
            prior = exp_misses[:-1]
            sd_ii = math.sqrt(sum(v * v for v in prior) / len(prior)) if len(prior) >= 3 else sd_ols
            p_lo, p_ex, p_ex2 = [], [], []
            for r in test:
                m1, s1 = predict(lo, r, rmse)
                m2, s2 = predict(ex, r, rmse)
                m3, s3 = predict(ex, r, sd_ii)
                n = r["n"] or r["n2"] - 1
                p_lo.append(f_half_normal(m1, s1) / (2 * n)); p_ex.append(f_half_normal(m2, s2) / (2 * n)); p_ex2.append(f_half_normal(m3, s3) / (2 * n))
            p_lo, p_ex, p_ex2 = map(np.array, (p_lo, p_ex, p_ex2))
            ratio = p_ex / p_lo
            own_first = sum(1 for r in test if r["site_own_first"])
            print(f"      {T:4d} {len(test):4d} {lo['b_lean']:7.3f}/{ex['b_lean']:<7.3f} {lo['s_e']:6.4f}/{ex['s_e']:<6.4f} {a_lo:+7.3f}/{a_ex:<+7.3f} {sd_ii:9.4f} "
                  f"{np.median(ratio):8.3f} ({np.quantile(ratio, 0.1):.2f}-{np.quantile(ratio, 0.9):.2f}) {p_ex.sum() / p_lo.sum():11.3f} {p_ex2.sum() / p_lo.sum():14.3f} {own_first:7d} of {len(test)}")


if __name__ == "__main__":
    main()
