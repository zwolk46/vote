"""C12 (second pass, item 1). Control of the chamber after #38, with each seat's own sd and swing loading read from
stage_two.inputs (own_sd, swing_loading, mean), the common swing's sd from the chamber block, and the Vice
President's tie vote at the presidential chance in presidential years (REPORT 4):
  12.1 every House and Senate year 2008-2024, every modelled seat: P(decides | tie) and P(decides) by a Fourier
       count of the other seats over a 1,201-point Simpson grid of the swing, the tie's likelihood forming the
       conditional, y_i = mean_i + swing_loading_i d + e_i with e_i ~ N(0, own_sd_i^2) (no deconvolution, no
       dynamic programme); the marked seats (538's sd not above the swing's) carry their recorded loading;
  12.2 the Senate in presidential years: P(decides | tie) = pi P(others give 49 - not-up D) + (1 - pi) P(50 - not-up D),
       and the recorded _if_VP_D and _if_VP_R; pi against the presidential chance D1's record gives;
  12.3 importance-sampling Monte Carlo for every Senate year and the House of 2014, 2022 and 2024.
"""
import os
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402

TOL = 1e-6
MC_HOUSE_YEARS = (2014, 2022, 2024)
NODES = 1201


def chamber_inputs(doc, level):
    ids, means, own_sd, lam, kinds, P_rec, P0_rec, PD_rec, PR_rec, marked = [], [], [], [], [], [], [], [], [], []
    fixed_D = fixed_other = 0
    for c in doc["contests"]:
        st2 = c.get("stage_two") or {}
        if not st2.get("of") or not st2.get("inputs"):
            continue
        inp = st2["inputs"]
        k = inp["entered_as"]
        if k == "fixed":
            if inp["fixed"] == "D":
                fixed_D += 1
            else:
                fixed_other += 1
            continue
        ids.append(c["id"])
        means.append(inp["mean"])
        own_sd.append(inp["own_sd"])
        lam.append(inp["swing_loading"])
        kinds.append(k)
        P_rec.append(inp.get("P_decides_given_tie"))
        P0_rec.append(inp.get("P_decides_unconditional"))
        PD_rec.append(inp.get("P_decides_given_tie_if_VP_D"))
        PR_rec.append(inp.get("P_decides_given_tie_if_VP_R"))
        marked.append(bool(inp.get("marginal_note")))
    ch = doc.get("chamber") or {}
    if not ids or "common_swing_sd" not in ch:
        return None
    sd_a = ch["common_swing_sd"]
    n_entries = len(ids) + fixed_D + fixed_other
    if level == "house":
        piv = {(217 if n_entries == 435 else n_entries // 2): 1.0}
        notup_D, pi = 0, None
    else:
        pi = ch["vice_president"]["P_democrat"]
        notup_D = ch["seats_not_up"]["D"]
        piv = {49 - notup_D: pi, 50 - notup_D: 1 - pi}
    assert ch["seats_fixed_D"] == fixed_D and ch["seats_fixed_other"] == fixed_other
    return dict(ids=ids, means=np.array(means), own_sd=np.array(own_sd), lam=np.array(lam), kinds=kinds, P_rec=P_rec,
                P0_rec=P0_rec, PD_rec=PD_rec, PR_rec=PR_rec, marked=marked, sd_a=sd_a, fixed_D=fixed_D,
                fixed_other=fixed_other, piv=piv, notup_D=notup_D, pi=pi, vp=ch.get("vice_president"))


def fourier(ci):
    """P(decides | tie), P(decides), and the two VP branches, for every seat with a mean, by characteristic functions."""
    U = len(ci["ids"])
    sd_a = ci["sd_a"]
    grid = np.linspace(-12 * sd_a, 12 * sd_a, NODES)
    h = grid[1] - grid[0]
    simp = np.ones(NODES)
    simp[1:-1:2], simp[2:-1:2] = 4.0, 2.0
    simp *= h / 3
    prior = stats.norm.pdf(grid, 0, sd_a)
    qmat = stats.norm.cdf((ci["means"][None, :] + ci["lam"][None, :] * grid[:, None] - 0.5) / ci["own_sd"][None, :])
    ev = np.ones(U, int)
    pmf = L.all_others_pmf_fft(qmat, ev)          # (U, nodes, U): P(the others give exactly k | d)
    W = {}
    for name, piv in (("all", ci["piv"]),) + ((("D", {49 - ci["notup_D"]: 1.0}), ("R", {50 - ci["notup_D"]: 1.0})) if ci["pi"] is not None else ()):
        w = np.zeros(U)
        for k, wt in piv.items():
            kk = k - ci["fixed_D"]
            if 0 <= kk < U:
                w[kk] += wt
        by = pmf[:, :, :U] @ w                     # (U, nodes)
        post = prior[None, :] * stats.norm.pdf((0.5 - ci["means"][:, None] - ci["lam"][:, None] * grid[None, :]) / ci["own_sd"][:, None]) / ci["own_sd"][:, None]
        Wt = (simp[None, :] * post * by).sum(axis=1) / (simp[None, :] * post).sum(axis=1)
        W0 = (simp[None, :] * prior[None, :] * by).sum(axis=1)
        W[name] = (Wt, W0)
    return W


def montecarlo(ci, draws, seed=12345, chunk=100_000):
    rng = np.random.default_rng(seed)
    U = len(ci["ids"])
    w = np.zeros(U + 1)
    for k, wt in ci["piv"].items():
        kk = k - ci["fixed_D"]
        if 0 <= kk <= U:
            w[kk] += wt
    num = np.zeros(U)
    den = np.zeros(U)
    num2 = np.zeros(U)
    den2 = np.zeros(U)
    done = 0
    while done < draws:
        m = min(chunk, draws - done)
        d = rng.normal(0, ci["sd_a"], m)
        y = ci["means"][None, :] + ci["lam"][None, :] * d[:, None] + rng.normal(0, 1, (m, U)) * ci["own_sd"][None, :]
        won = y > 0.5
        tot = won.sum(axis=1)
        # for seat i: the others' count = tot - won_i; the weight w[others]; the tie likelihood of seat i given d
        like = stats.norm.pdf((0.5 - ci["means"][None, :] - ci["lam"][None, :] * d[:, None]) / ci["own_sd"][None, :]) / ci["own_sd"][None, :]
        others = tot[:, None] - won.astype(int)
        val = w[others]
        num += (like * val).sum(axis=0)
        den += like.sum(axis=0)
        num2 += ((like * val) ** 2).sum(axis=0)
        den2 += (like ** 2).sum(axis=0)
        done += m
    W = num / den
    # a ratio estimator's standard error, by the delta method on independent draws
    n = draws
    var = (num2 / n - (num / n) ** 2) / n
    se = np.sqrt(np.maximum(var, 0)) / (den / n)
    return W, se


def compare(label, ids, rec, new, tol):
    rows = [(u, r, x) for u, r, x in zip(ids, rec, new) if r is not None]
    if not rows:
        print(f"    {label}: nothing recorded")
        return []
    diffs = [abs(x / r - 1.0) if r > 0 else abs(x - r) for _, r, x in rows]
    k = max(range(len(rows)), key=lambda j: diffs[j])
    bad = [(u, r, x, d) for (u, r, x), d in zip(rows, diffs) if d > tol]
    print(f"    {label}: {len(rows)} seats; largest relative difference {diffs[k]:.2e} ({rows[k][0]}: record {rows[k][1]:.6g}, "
          f"here {rows[k][2]:.6g}); {len(bad)} beyond {tol:g}")
    for u, r, x, d in bad[:8]:
        print(f"       MISMATCH {u}: record {r:.6g} here {x:.6g} rel {d:.2e}")
    return bad


def presidential_chance(year, whole=False):
    """The chance the Democratic ticket wins, from D1's record of the year: 538's US row where 538 stands first there,
    else the model's own College chance computed here from its state forecasts (states whole, a 269 tie half)."""
    doc = L.load_json(os.path.join(L.DATA, "president", f"{year}.json"))
    unders = [c["p"]["under"] for c in doc["contests"] if (c.get("p") or {}).get("under")]
    top = max(set(unders), key=unders.count)
    if top.startswith("538"):
        model = top.split("(")[1].split(")")[0]
        fte = L.load_json(os.path.join(L.DATA, "president", "inputs", "fte_president_forecasts.json"))
        f = fte["years"][str(year)][model]
        us = {a["party"]: a for a in f["units"]["US"]}
        return us["D"]["probwin"], f"538 ({model}) US row, {f['forecast_date']}"
    units, s_nat, s_state = {}, None, None
    for c in doc["contests"]:
        for f in c["forecasts"]:
            if f["by"] == "the model's own":
                units[c["place"]["state"] + (f"-{c['place']['district']}" if c["place"].get("district") else "")] = (f["share"]["mean"], f["unit_ev"])
                s_nat, s_state = f["share"]["national_sd"], f["share"]["state_sd"]
    if whole:   # the states whole: a state with districts takes its whole-state mean and all its electoral votes
        agg = {}
        for u, (m, e) in units.items():
            st = u.split("-")[0]
            agg.setdefault(st, [None, 0])
            agg[st][1] += e
            if "-" not in u:
                agg[st][0] = m
        units = {st: (m, e) for st, (m, e) in agg.items()}
    mu = np.array([m for m, e in units.values()])
    ev = np.array([e for m, e in units.values()], int)
    total = int(ev.sum())
    grid = np.linspace(-12 * s_nat, 12 * s_nat, NODES)
    h = grid[1] - grid[0]
    simp = np.ones(NODES)
    simp[1:-1:2], simp[2:-1:2] = 4.0, 2.0
    simp *= h / 3
    prior = stats.norm.pdf(grid, 0, s_nat)
    sc = s_state / np.sqrt(2.0)
    q = stats.t.sf((0.5 - mu[None, :] - grid[:, None]) / sc, 4)            # P(D wins unit | swing), t4 state error
    # the count of D electoral votes by polynomial multiplication at each node
    pm = np.zeros((NODES, total + 1))
    pm[:, 0] = 1.0
    for j in range(len(mu)):
        e = ev[j]
        new = pm * (1 - q[:, j:j + 1])
        new[:, e:] += pm[:, :total + 1 - e] * q[:, j:j + 1]
        pm = new
    E = np.arange(total + 1)
    win = np.where(2 * E > total, 1.0, np.where(2 * E == total, 0.5, 0.0))
    pD = float((simp * prior * (pm @ win)).sum())
    return pD, f"the model's own College chance recomputed here ({len(mu)} units{', states whole' if whole else ''}, {total} electoral votes, t4 state error, Simpson over the national swing)"


def main():
    print("C12. CHAMBER CONTROL AFTER #38: P(decides | tie) WITH EACH SEAT'S OWN sd AND SWING LOADING, THE VP AT THE PRESIDENTIAL CHANCE")
    print(f"repository HEAD {L.git_head()}")
    for level in ("senate", "house"):
        for path in L.congress_files(level):
            doc = L.load_json(path)
            y = doc["year"]
            if not doc.get("chamber") or not any((c.get("stage_two") or {}).get("of") for c in doc["contests"]):
                print(f"  {level} {y}: no control computed")
                continue
            ci = chamber_inputs(doc, level)
            if ci is None:
                print(f"  {level} {y}: control not computed in the file ({(doc.get('contests') or [{}])[0].get('stage_two', {}).get('note', '')[:90]}...)")
                continue
            U = len(ci["ids"])
            nm = sum(ci["marked"])
            print(f"  {level} {y}: {U} seats with a mean ({ci['kinds'].count('model')} modelled, {ci['kinds'].count('inferred')} inferred; "
                  f"{nm} marked, loading {', '.join(f'{l:.3f}' for l, mk in zip(ci['lam'], ci['marked']) if mk)[:60] if nm else '-'}), "
                  f"fixed D {ci['fixed_D']}, other {ci['fixed_other']}, "
                  f"{'not-up D ' + str(ci['notup_D']) + ', pi ' + f'{ci['pi']:.4f}, ' if level == 'senate' else ''}"
                  f"pivots {ci['piv']}, sd_a {ci['sd_a']:.5f}, own_sd {ci['own_sd'].min():.4f}-{ci['own_sd'].max():.4f}")
            W = fourier(ci)
            compare(f"{level} {y} P(decides | tie) Fourier vs record", ci["ids"], ci["P_rec"], W["all"][0], TOL)
            compare(f"{level} {y} P(decides) unconditional Fourier vs record", ci["ids"], ci["P0_rec"], W["all"][1], TOL)
            if level == "senate" and y % 4 == 0:
                compare(f"{level} {y} P(decides | tie) if the VP is a Democrat", ci["ids"], ci["PD_rec"], W["D"][0], TOL)
                compare(f"{level} {y} P(decides | tie) if the VP is a Republican", ci["ids"], ci["PR_rec"], W["R"][0], TOL)
                mix = ci["pi"] * W["D"][0] + (1 - ci["pi"]) * W["R"][0]
                compare(f"{level} {y} pi P(VP D branch) + (1 - pi) P(VP R branch) vs P(decides | tie)", ci["ids"], ci["P_rec"], mix, 1e-12)
                pD, how = presidential_chance(y)
                if not how.startswith("538"):
                    pW, howW = presidential_chance(y, whole=True)
                    print(f"    the same with the states whole ({howW.split('(')[1]}: {pW:.6f}; difference from the record {abs(pW - ci['pi']):.2e}")
                print(f"    the VP's chance: chamber.vice_president.P_democrat {ci['pi']:.6f} ({ci['vp'].get('by')}); {how}: {pD:.6f}; "
                      f"difference {abs(pD - ci['pi']):.2e}")
            if nm:
                mk = [i for i, m in enumerate(ci["marked"]) if m]
                print(f"    marked seats: " + "; ".join(f"{ci['ids'][i]} lam {ci['lam'][i]:.3f} own_sd {ci['own_sd'][i]:.4f} P rec {ci['P_rec'][i]:.5f} here {W['all'][0][i]:.5f}" for i in mk[:6]))
            if level == "senate" or y in MC_HOUSE_YEARS:
                draws = 2_000_000 if level == "senate" else 400_000
                W_mc, se = montecarlo(ci, draws, chunk=200_000 if level == "senate" else 40_000)
                zs = [((m - r) / s if s > 0 else 0.0, u, r, m, s) for u, r, m, s in zip(ci["ids"], ci["P_rec"], W_mc, se) if r is not None]
                big = [z for z in zs if abs(z[0]) > 3]
                worst = max(zs, key=lambda z: abs(z[0]))
                print(f"    Monte Carlo ({draws:,} draws): largest |z| {abs(worst[0]):.2f} ({worst[1]}: record {worst[2]:.5g}, MC {worst[3]:.5g} +- {worst[4]:.2g}); "
                      f"{len(big)} of {len(zs)} beyond 3 se ({0.0027 * len(zs):.1f} expected)")
                for z, u, r, m, s in big[:6]:
                    print(f"       {u}: record {r:.5g}, MC {m:.5g} +- {s:.2g} (z {z:+.1f})")
            if (level, y) in (("senate", 2024), ("house", 2024), ("senate", 2014)):
                order = sorted(range(U), key=lambda k: -(ci["P_rec"][k] or 0))
                print(f"       {'seat':22s} {'mean':>8s} {'own_sd':>7s} {'lam':>6s} {'P rec':>9s} {'P here':>9s} {'P uncond':>9s}" + ("   if VP D   if VP R" if ci["pi"] is not None else ""))
                for k in order[:8]:
                    if ci["P_rec"][k] is None:
                        continue
                    print(f"       {ci['ids'][k]:22s} {ci['means'][k]:8.4f} {ci['own_sd'][k]:7.4f} {ci['lam'][k]:6.3f} {ci['P_rec'][k]:9.5f} {W['all'][0][k]:9.5f} {ci['P0_rec'][k]:9.5f}"
                          + (f" {W['D'][0][k]:9.5f} {W['R'][0][k]:9.5f}" if ci["pi"] is not None else ""))


if __name__ == "__main__":
    main()
