"""C2. The Electoral College stage: W = P(the unit's electoral votes decide | the unit is tied), recomputed
by methods other than the pipeline's (briefs/M2-check-computed-p.md, item 2).

The pipeline (pipeline/college.swing_model) finds W on a 401-point uniform grid of the national swing by a
dynamic programme over the other units. Here, under the same joint forecast (v_j = mu_j + delta + eps_j,
delta ~ N(0, s_d^2) common, eps_j independent, normal or t4 matched on sd), two other methods:
  Fourier     the other units' electoral-vote count by characteristic functions (prefix and suffix products
              on the unit circle, inverted by the FFT), integrated over the swing given the tie on a finer,
              wider Simpson grid (1,201 points over +-12 s_d);
  Monte Carlo importance sampling: draw the swing and every unit's error from the prior, and weight each
              draw for unit i by the likelihood of a tie in i given the swing. No grid, no count by
              recursion; its standard error is reported.
Every year with the model's own forecast (1984-2024), every unit, including Maine's and Nebraska's districts
where the record models them; then 538's marginals with the model's swing (2016, three models; 2020
polls-plus), and the Economist's 2020 draws recounted from the raw file, with the window's width varied and
a local-linear estimate beside the count.
"""
import csv
import io
import os
import sys
import zipfile

import numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402

TOL_W = 1e-4          # Fourier vs the record: both are exact integrals; they differ only by quadrature
MC_DRAWS = 1_000_000
TABLE_YEARS = (1984, 2000, 2016, 2024)


def own_inputs(doc):
    units, mu, ev, W_rec, Wu_rec, fh_rec = [], [], [], [], [], []
    s_nat = s_state = None
    total = majority = None
    for c in doc["contests"]:
        for f in c["forecasts"]:
            if f["by"] != "the model's own":
                continue
            units.append(c["id"].split("-", 2)[2])
            mu.append(f["share"]["mean"])
            ev.append(f["unit_ev"])
            s_nat, s_state = f["share"]["national_sd"], f["share"]["state_sd"]
            p = f["p"]
            W_rec.append(p["W"] if p else None)
            Wu_rec.append(p["W_unconditional"] if p else None)
            fh_rec.append(p["f_half"] if p else None)
            total, majority = c["stage_two"]["inputs"]["total_ev"], c["stage_two"]["inputs"]["majority"]
    return units, np.array(mu), np.array(ev), s_nat, s_state, W_rec, Wu_rec, fh_rec, total, majority


def fte_inputs(doc, model):
    units, mu, tau, ev, W_rec, fallback = [], [], [], [], [], []
    total = majority = None
    s_d_text = None
    own = [f for c in doc["contests"] for f in c["forecasts"] if f["by"] == "the model's own"]   # one sd a year
    for c in doc["contests"]:
        for f in c["forecasts"]:
            if f["by"] != "538" or f.get("model") != model or f["share"] is None:
                continue
            units.append(c["id"].split("-", 2)[2])
            mu.append(f["share"]["mean"])
            if f["share"]["sd"] is None:
                tau.append(own[0]["share"]["sd"])            # the pipeline's rule: the own forecast's sd
                fallback.append(units[-1])
            else:
                tau.append(f["share"]["sd"])
            ev.append(f["unit_ev"])
            W_rec.append(f["p"]["W"] if f["p"] else None)
            total, majority = c["stage_two"]["inputs"]["total_ev"], c["stage_two"]["inputs"]["majority"]
            if f["p"] and s_d_text is None:
                m = f["p"]["method"]
                s_d_text = float(m.split("national swing sd ")[1].split(")")[0].split(",")[0])
    return units, np.array(mu), np.array(tau), np.array(ev), W_rec, fallback, total, majority, s_d_text


def compare(label, units, W_rec, W_new, tol):
    rows = [(u, r, n) for u, r, n in zip(units, W_rec, W_new) if r is not None]
    diffs = [abs(n / r - 1.0) if r > 0 else abs(n - r) for _, r, n in rows]
    worst = max(range(len(rows)), key=lambda k: diffs[k])
    bad = [(u, r, n, d) for (u, r, n), d in zip(rows, diffs) if d > tol]
    print(f"  {label}: {len(rows)} units; largest relative difference {diffs[worst]:.2e} "
          f"({rows[worst][0]}: record {rows[worst][1]:.6g}, here {rows[worst][2]:.6g}); {len(bad)} beyond {tol:g}")
    for u, r, n, d in bad:
        print(f"     MISMATCH {u}: record {r:.6g} here {n:.6g} rel {d:.2e}")
    return bad


def mc_compare(label, units, W_rec, W_mc, se):
    zs = []
    for u, r, m, s in zip(units, W_rec, W_mc, se):
        if r is None:
            continue
        zs.append(((m - r) / s if s > 0 else 0.0, u, r, m, s))
    big = [z for z in zs if abs(z[0]) > 3]
    worst = max(zs, key=lambda z: abs(z[0]))
    print(f"  {label}: {len(zs)} units; largest |z| = |W_mc - W_record| / se: {abs(worst[0]):.2f} ({worst[1]}: record "
          f"{worst[2]:.5g}, Monte Carlo {worst[3]:.5g} +- {worst[4]:.2g}); {len(big)} beyond 3 se "
          f"(about {0.0027 * len(zs):.1f} expected by chance)")
    for z, u, r, m, s in big:
        print(f"     {u}: record {r:.5g}, Monte Carlo {m:.5g} +- {s:.2g} (z {z:+.1f})")


def main():
    print("C2. THE ELECTORAL COLLEGE: W GIVEN THE TIE, BY METHODS OTHER THAN THE PIPELINE'S")
    print(f"repository HEAD {L.git_head()}")
    print("2.1 The model's own forecast, every year: Fourier count on a 1,201-point Simpson grid (+-12 s_d), and "
          f"importance-sampling Monte Carlo ({MC_DRAWS:,} draws, seed 12345)")
    for path in L.president_files():
        doc = L.load_json(path)
        y = doc["year"]
        units, mu, ev, s_nat, s_state, W_rec, Wu_rec, fh_rec, total, majority = own_inputs(doc)
        if not units:
            print(f"  {y}: no own forecast in the record")
            continue
        assert ev.sum() == total, (y, ev.sum(), total)
        s_unit = np.full(len(units), s_state)
        four = L.W_fourier(mu, s_unit, ev, s_nat, total, majority, "t4")
        districts = [u for u in units if "-" in u]
        print(f"  {y}: {len(units)} units ({len(districts)} districts: {', '.join(districts) or 'none'}), total {total}, "
              f"majority {majority}, s_nat {s_nat:.5f}, s_state {s_state:.5f}")
        compare(f"  {y} f(1/2) by Fourier-grid quadrature vs the record", units, fh_rec, four["f_half"], TOL_W)
        compare(f"  {y} W by Fourier vs the record", units, W_rec, four["W"], TOL_W)
        compare(f"  {y} W_unconditional by Fourier vs the record", units, Wu_rec, four["W_unconditional"], TOL_W)
        W_mc, se, ess = L.W_montecarlo(mu, s_unit, ev, s_nat, total, majority, "t4", MC_DRAWS)
        mc_compare(f"  {y} W by Monte Carlo vs the record", units, W_rec, W_mc, se)
        if y in TABLE_YEARS:
            print(f"     {'unit':8s} {'ev':>3s} {'mean':>8s} {'W record':>10s} {'W Fourier':>10s} {'W MC':>10s} {'+-':>8s} "
                  f"{'ess':>8s} {'W uncond':>10s}")
            order = sorted(range(len(units)), key=lambda k: -(W_rec[k] or 0))
            for k in order:
                if W_rec[k] is None:
                    continue
                print(f"     {units[k]:8s} {ev[k]:3d} {mu[k]:8.4f} {W_rec[k]:10.5f} {four['W'][k]:10.5f} {W_mc[k]:10.5f} "
                      f"{se[k]:8.1e} {ess[k]:8.0f} {Wu_rec[k]:10.5f}")

    print("2.2 538's marginals (mean, implied sd, normal) with the model's own national swing: 2016 (three models) "
          "and 2020 (polls-plus; its districts are the record's p)")
    for y, models in ((2016, ("polls-plus", "polls-only", "now-cast")), (2020, ("polls-plus",))):
        doc = L.load_json(os.path.join(L.DATA, "president", f"{y}.json"))
        for model in models:
            units, mu, tau, ev, W_rec, fallback, total, majority, s_d_text = fte_inputs(doc, model)
            assert ev.sum() == total, (y, model, ev.sum(), total)
            own = [f for c in doc["contests"] for f in c["forecasts"] if f["by"] == "the model's own"][0]
            s_nat = own["share"]["national_sd"]
            s_d = min(s_nat, 0.95 * tau.min())
            capped = s_d < s_nat
            print(f"  {y} 538 {model}: {len(units)} units; s_d {s_d:.5f} ({'capped at 0.95 of the smallest sd' if capped else 'the own national sd'}; "
                  f"the record's method text says {s_d_text:.4f}); fallback units given the own sd: {fallback or 'none'}")
            assert abs(s_d - s_d_text) < 6e-5, (s_d, s_d_text)
            s_unit = np.sqrt(np.maximum(tau ** 2 - s_d ** 2, 1e-12))
            four = L.W_fourier(mu, s_unit, ev, s_d, total, majority, "normal")
            compare(f"  {y} {model} W by Fourier vs the record", units, W_rec, four["W"], TOL_W)
            W_mc, se, ess = L.W_montecarlo(mu, s_unit, ev, s_d, total, majority, "normal", MC_DRAWS)
            mc_compare(f"  {y} {model} W by Monte Carlo vs the record", units, W_rec, W_mc, se)
            if model == "polls-plus":
                print(f"     {'unit':8s} {'ev':>3s} {'mean':>8s} {'sd':>8s} {'W record':>10s} {'W Fourier':>10s} {'W MC':>10s} {'+-':>8s}")
                order = sorted(range(len(units)), key=lambda k: -(W_rec[k] or 0))
                for k in order[:12] + [k for k in range(len(units)) if "-" in units[k]]:
                    if W_rec[k] is None:
                        continue
                    print(f"     {units[k]:8s} {ev[k]:3d} {mu[k]:8.4f} {tau[k]:8.4f} {W_rec[k]:10.5f} {four['W'][k]:10.5f} "
                          f"{W_mc[k]:10.5f} {se[k]:8.1e}")

    print("2.3 The Economist's 2020 draws, recounted from the raw file (electoral_college_simulations.csv)")
    econ_zip = os.path.join(L.CACHE, "economist_model_output.zip")
    rec = L.load_json(os.path.join(L.DATA, "president", "inputs", "economist_2020.json"))
    if not os.path.exists(econ_zip):
        print(f"  the zip is not in the cache ({econ_zip}); 2.3 skipped")
        return
    h = L.sha256(econ_zip)
    print(f"  zip sha256 {h} ({'matches' if h == rec['states']['OH'] and False else ''}record's source sha256 "
          f"{'matches' if h == rec['source']['sha256'] else 'DIFFERS'})")
    z = zipfile.ZipFile(econ_zip)
    name = [n for n in z.namelist() if n.endswith("/electoral_college_simulations.csv")][0]
    rd = csv.reader(io.StringIO(z.read(name).decode("utf-8")))
    head = next(rd)
    states = head[3:]
    data = np.array([[float(x) for x in r] for r in rd])
    K = data.shape[0]
    dem_ev = data[:, 1].astype(int)
    shares = data[:, 3:]
    ev = np.array([rec["states"][s]["ev"] for s in states])
    total, majority, step = 538, 270, 1e-4
    assert ev.sum() == total and K == rec["draws"]
    doc20 = L.load_json(os.path.join(L.DATA, "president", "2020.json"))
    econ_rec = {}
    for c in doc20["contests"]:
        for f in c["forecasts"]:
            if f["by"] == "The Economist" and f["p"]:
                econ_rec[c["place"]["state"]] = f
    won = shares > 0.5
    amb = np.isclose(shares, 0.5, atol=step / 10)
    base = (won & ~amb) @ ev
    print(f"  {K:,} draws, {len(states)} states; draws with a state printed at exactly one half: {int(amb.any(axis=1).sum())}")
    # (a) the record's counts, recounted
    worst = 0.0
    for i, s in enumerate(states):
        for kw, k in enumerate((25, 50, 100, 200)):
            in_win = np.abs(shares[:, i] - 0.5) <= k * step + step / 10
            E_rest = np.where(won[:, i] & ~amb[:, i], dem_ev - ev[i], dem_ev)
            only_i = amb[:, i] & (amb.sum(axis=1) == 1)
            E_rest = np.where(only_i, base, E_rest)
            unclear = amb[:, i] & (amb.sum(axis=1) > 1)
            w = L.window_weights(int(ev[i]), total, majority)
            use = in_win & ~unclear
            weighted = float(np.sum([w[int(E)] for E in E_rest[use]])) if use.any() else 0.0
            r = rec["states"][s]["sims"]["windows"][kw]
            assert r["k_steps"] == k
            if r["in_window"] != int(in_win.sum()) or abs(r["weighted"] - weighted) > 1e-9:
                print(f"     MISMATCH {s} k={k}: record in_window {r['in_window']} weighted {r['weighted']}; here {int(in_win.sum())} {weighted}")
                worst = 1.0
    print(f"  (a) the record's window counts (in_window, weighted) for k = 25, 50, 100, 200 steps: "
          f"{'all 204 recounted exactly' if worst == 0 else 'see MISMATCH lines'}")
    # (b) W and the joint density by other estimators
    print("  (b) W by window width, and by a local-linear fit of w on (share - 1/2) within +-0.03 (its intercept),")
    print("      and p_state's numerator (the share's density at one half) by the window count vs a normal fit of the state's draws;")
    print("      ratio = the Fourier-free estimate / the record's W (k = 100, the record's window)")
    print(f"     {'state':5s} {'ev':>3s} {'mean':>7s} {'sd':>7s} {'W rec':>9s} {'W k=50':>9s} {'W k=200':>9s} {'W loclin':>9s} {'+-':>8s} "
          f"{'f(1/2) win':>10s} {'f normal':>9s} {'ratio f':>8s}")
    rows = []
    for i, s in enumerate(states):
        if s not in econ_rec:
            continue
        p = econ_rec[s]["p"]
        W_rec = p["W"]
        x = shares[:, i] - 0.5
        E_rest = np.where(won[:, i] & ~amb[:, i], dem_ev - ev[i], dem_ev)
        w = L.window_weights(int(ev[i]), total, majority)
        wv = w[np.clip(E_rest, 0, len(w) - 1)]
        def W_k(k):
            m = np.abs(x) <= k * step + step / 10
            return wv[m].sum() / m.sum() if m.sum() else float("nan")
        m = np.abs(x) <= 0.03
        X = np.column_stack([np.ones(m.sum()), x[m]])
        beta, *_ = np.linalg.lstsq(X, wv[m], rcond=None)
        resid = wv[m] - X @ beta
        cov = np.linalg.inv(X.T @ X) * (resid @ resid) / max(m.sum() - 2, 1)
        W_ll, se_ll = float(beta[0]), float(np.sqrt(cov[0, 0]))
        mean, sd = x.mean() + 0.5, x.std()
        f_win = (np.abs(x) <= 100 * step + step / 10).sum() / (K * 0.0201)
        f_norm = stats.norm.pdf(0.5, mean, sd)
        rows.append((W_rec, s, ev[i], mean, sd, W_k(50), W_k(200), W_ll, se_ll, f_win, f_norm))
    for W_rec, s, e, mean, sd, w50, w200, wll, sell, fwin, fnorm in sorted(rows, reverse=True)[:20]:
        print(f"     {s:5s} {e:3d} {mean:7.4f} {sd:7.4f} {W_rec:9.5f} {w50:9.5f} {w200:9.5f} {wll:9.5f} {sell:8.1e} "
              f"{fwin:10.4f} {fnorm:9.4f} {fwin / fnorm:8.4f}")
    bound = [s for s, f in econ_rec.items() if f["p"].get("window_weighted", 0) < 10]
    print(f"  states whose record W rests on fewer than 10 weighted draws (the record marks these): {len(bound)}: {', '.join(sorted(bound))}")


if __name__ == "__main__":
    main()
