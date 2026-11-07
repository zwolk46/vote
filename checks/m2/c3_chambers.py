"""C3. Chamber control: P(the seat decides control | the seat is tied), MATH section 4.2, recomputed by
methods other than the pipeline's (briefs/M2-check-computed-p.md, item 2), and the coherence of
"538's seat p x the model's own P(decides | tie)".

The pipeline (pipeline/chambers.stage_two) builds the count of Democratic seats by a dynamic programme over
every modelled seat on a 401-point uniform grid of the common swing, removes seat i by deconvolution
(remove_seat), and weights the grid by the normal density of the swing given the tie. Here, under the same
model (y_j = mean_j + d + e_j, d ~ N(0, sd_a^2) common, e_j ~ N(0, s_e^2) independent):
  Fourier     the other seats' count by characteristic functions (prefix and suffix products, no
              deconvolution), on a 1,201-point Simpson grid of the swing, the tie's likelihood forming the
              conditional (the same closed form as MATH 4.2, reached without it);
  Monte Carlo importance sampling over the whole chamber (every Senate year; the House in 2018, 2022, 2024).
Every chamber-year 2006-2024, every modelled seat, against the record's P_decides_given_tie and
P_decides_unconditional. Then, for the seats whose p is 538's, what conditioning on 538's own mean (rather
than the model's) would do to the control p.
"""
import os
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402

TOL = 1e-6
MC_HOUSE_YEARS = (2018, 2022, 2024)


def chamber_inputs(doc, level):
    """The seats as the record entered them: modelled (own mean), inferred (mean, no p), fixed D/R/other."""
    ids, means, kinds, P_rec, P0_rec, cs = [], [], [], [], [], []
    fixed_D = fixed_other = 0
    for c in doc["contests"]:
        st2 = c.get("stage_two") or {}
        if not st2.get("of") or not (st2.get("inputs") or {}).get("entered_as"):
            continue   # since D2's #29 a chamber-year without control carries an empty inputs block and a note (read only)
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
        kinds.append(k)
        P_rec.append(inp.get("P_decides_given_tie"))
        P0_rec.append(inp.get("P_decides_unconditional"))
        cs.append(c)
    ch = doc["chamber"]
    sd_a, s_e = ch["common_swing_sd"], ch["own_sd"]
    n_entries = len(ids) + fixed_D + fixed_other
    if level == "house":
        piv = {(217 if n_entries == 435 else n_entries // 2): 1.0}
        notup_D = 0
    else:
        pi = ch["vice_president"]["P_democrat"]
        notup_D = ch["seats_not_up"]["D"]
        piv = {k: w for k, w in ((49, pi), (50, 1 - pi)) if w > 0}
        piv = {k - notup_D: w for k, w in piv.items()}
    # weights over the OTHER modelled seats' Democratic count kk = k - fixed_D
    w = np.zeros(len(ids))          # others' count runs 0..len(ids)-1
    for k, wt in piv.items():
        kk = k - fixed_D
        if 0 <= kk < len(w):
            w[kk] += wt
    assert ch["seats_fixed_D"] == fixed_D and ch["seats_fixed_other"] == fixed_other, (fixed_D, fixed_other, ch)
    return dict(ids=ids, means=np.array(means), kinds=kinds, P_rec=P_rec, P0_rec=P0_rec, contests=cs,
                sd_a=sd_a, s_e=s_e, fixed_D=fixed_D, fixed_other=fixed_other, piv=piv, w=w, notup_D=notup_D)


def compare(label, ids, rec, new, tol):
    rows = [(u, r, n) for u, r, n in zip(ids, rec, new) if r is not None]
    diffs = [abs(n / r - 1.0) if r > 0 else abs(n - r) for _, r, n in rows]
    k = max(range(len(rows)), key=lambda j: diffs[j])
    bad = [(u, r, n, d) for (u, r, n), d in zip(rows, diffs) if d > tol]
    print(f"    {label}: {len(rows)} seats; largest relative difference {diffs[k]:.2e} ({rows[k][0]}: record "
          f"{rows[k][1]:.6g}, here {rows[k][2]:.6g}); {len(bad)} beyond {tol:g}")
    for u, r, n, d in bad[:10]:
        print(f"       MISMATCH {u}: record {r:.6g} here {n:.6g} rel {d:.2e}")
    return bad


def main():
    print("C3. CHAMBER CONTROL: P(decides | tie) BY METHODS OTHER THAN THE PIPELINE'S, AND 538 x OWN COHERENCE")
    print(f"repository HEAD {L.git_head()}")
    print("3.1 Every chamber-year, every modelled seat: Fourier count on a 1,201-point Simpson grid (tolerance 1e-6), "
          "and importance-sampling Monte Carlo where run")
    coherence = []
    for level in ("senate", "house"):
        for path in L.congress_files(level):
            doc = L.load_json(path)
            y = doc["year"]
            if not any(((c.get("stage_two") or {}).get("inputs") or {}).get("entered_as") for c in doc["contests"]):
                print(f"  {level} {y}: control not computed in the file ({(doc['contests'][0].get('stage_two') or {}).get('note', '')[:90]}...)")
                continue   # the read only: the first pass's files all carried control (D2's #29 fits on earlier cycles only)
            ci = chamber_inputs(doc, level)
            U = len(ci["ids"])
            print(f"  {level} {y}: {U} seats with a mean ({ci['kinds'].count('model')} modelled, {ci['kinds'].count('inferred')} inferred), "
                  f"fixed D {ci['fixed_D']}, fixed other {ci['fixed_other']}, "
                  f"{'not-up D ' + str(ci['notup_D']) + ', ' if level == 'senate' else ''}pivots over all seats {ci['piv']}, "
                  f"sd_a {ci['sd_a']:.5f}, s_e {ci['s_e']:.5f}")
            s_unit = np.full(U, ci["s_e"])
            ev = np.ones(U, int)
            four = L.W_fourier(ci["means"], s_unit, ev, ci["sd_a"], U, None, "normal", nodes=1201, weights=ci["w"])
            compare(f"{level} {y} P(decides | tie) by Fourier vs the record", ci["ids"], ci["P_rec"], four["W"], TOL)
            compare(f"{level} {y} P(decides), unconditional, by Fourier vs the record", ci["ids"], ci["P0_rec"],
                    four["W_unconditional"], TOL)
            if level == "senate" or y in MC_HOUSE_YEARS:
                draws = 2_000_000 if level == "senate" else 400_000
                W_mc, se, ess = L.W_montecarlo(ci["means"], s_unit, ev, ci["sd_a"], U, None, "normal", draws,
                                               weights=ci["w"], chunk=50_000 if level == "house" else 200_000)
                zs = [((m - r) / s if s > 0 else 0.0, u, r, m, s) for u, r, m, s in zip(ci["ids"], ci["P_rec"], W_mc, se) if r is not None]
                big = [z for z in zs if abs(z[0]) > 3]
                worst = max(zs, key=lambda z: abs(z[0]))
                print(f"    {level} {y} P(decides | tie) by Monte Carlo ({draws:,} draws): largest |z| {abs(worst[0]):.2f} "
                      f"({worst[1]}: record {worst[2]:.5g}, MC {worst[3]:.5g} +- {worst[4]:.2g}); {len(big)} of {len(zs)} beyond 3 se "
                      f"({0.0027 * len(zs):.1f} expected)")
                for z, u, r, m, s in big[:8]:
                    print(f"       {u}: record {r:.5g}, MC {m:.5g} +- {s:.2g} (z {z:+.1f})")
            if (level, y) in (("senate", 2024), ("house", 2022)):
                order = sorted(range(U), key=lambda k: -(ci["P_rec"][k] or 0))
                print(f"       {'seat':22s} {'mean':>8s} {'P rec':>9s} {'P Fourier':>9s} {'P uncond':>9s}")
                for k in order[:10]:
                    if ci["P_rec"][k] is None:
                        continue
                    print(f"       {ci['ids'][k]:22s} {ci['means'][k]:8.4f} {ci['P_rec'][k]:9.5f} {four['W'][k]:9.5f} {ci['P0_rec'][k]:9.5f}")
            # 3.2 inputs: seats whose p is 538's
            for k, c in enumerate(ci["contests"]):
                p = c["p"]
                if not p.get("value") or not p["under"].startswith("538") or ci["P_rec"][k] is None:
                    continue
                ver = p["under"].split("(")[1].split(")")[0]
                f = next(f for f in c["forecasts"] if f["by"] == "538" and f.get("version") == ver)
                coherence.append((level, y, k, c["id"], f["share"]["mean"], f["share"]["sd"], ci, p))
    print("3.2 '538's seat p x the model's own P(decides | tie)': what conditioning on 538's mean would do")
    print("    (a) the record: the swing given the tie from the model's own mean for the seat;")
    print("    (b) the swing given the tie from 538's mean, with the model's sd_a and s_e;")
    print("    (c) 538's mean and sd as the seat's marginal: s_e,i = sqrt(sd_538^2 - sd_a^2) (as the presidency treats 538),")
    print("        where sd_538 > 1.05 sd_a, else (b).")
    print("    control p = seat p (538's, unchanged) x P; so ratio = P(b or c) / P(a).")
    by_year = {}
    for level, y, k, cid, m538, sd538, ci, p in coherence:
        by_year.setdefault((level, y), []).append((k, cid, m538, sd538, ci, p))
    for (level, y), rows in sorted(by_year.items()):
        ci = rows[0][4]
        U = len(ci["ids"])
        ev = np.ones(U, int)
        sd_a, s_e = ci["sd_a"], ci["s_e"]
        # (b): replace seat i's mean by 538's, one seat at a time, and read its own W
        idx = [r[0] for r in rows]
        mu_b = ci["means"].copy()
        # the others' means stay the model's; only the tied seat's mean changes, so run one Fourier pass per
        # changed seat would be U passes; instead note that W_i depends on mean_i only through the conditional
        # of the swing, so compute it directly: posterior over the swing from 538's mean, others' count unchanged
        grid = np.linspace(-12 * sd_a, 12 * sd_a, 1201)
        h = grid[1] - grid[0]
        simp = np.ones(1201); simp[1:-1:2], simp[2:-1:2] = 4.0, 2.0; simp *= h / 3
        prior = stats.norm.pdf(grid, 0, sd_a)
        qmat = stats.norm.sf((0.5 - ci["means"][None, :] - grid[:, None]) / s_e)
        pmf = L.all_others_pmf_fft(qmat, ev)
        out = []
        for k, cid, m538, sd538, _, p in rows:
            by = pmf[k][:, :U] @ ci["w"]
            post_a = prior * stats.norm.pdf(0.5 - ci["means"][k] - grid, 0, s_e)
            Pa = (simp * post_a * by).sum() / (simp * post_a).sum()
            post_b = prior * stats.norm.pdf(0.5 - m538 - grid, 0, s_e)
            Pb = (simp * post_b * by).sum() / (simp * post_b).sum()
            if sd538 > 1.05 * sd_a:
                s_i = np.sqrt(sd538 ** 2 - sd_a ** 2)
                post_c = prior * stats.norm.pdf(0.5 - m538 - grid, 0, s_i)
                Pc = (simp * post_c * by).sum() / (simp * post_c).sum()
            else:
                Pc = Pb
            out.append((cid, ci["means"][k], m538, sd538, Pa, Pb, Pc, p["value"], p["control"]["value"]))
        rb = np.array([o[5] / o[4] for o in out])
        rc = np.array([o[6] / o[4] for o in out])
        print(f"  {level} {y}: {len(out)} seats with 538's p; P(b)/P(a) median {np.median(rb):.3f}, range {rb.min():.3f}-{rb.max():.3f}; "
              f"P(c)/P(a) median {np.median(rc):.3f}, range {rc.min():.3f}-{rc.max():.3f}; "
              f"sum of control p over these seats: (a) {sum(o[8] for o in out):.3e}, (b) {sum(o[7] * o[5] for o in out):.3e}, (c) {sum(o[7] * o[6] for o in out):.3e}")
        worst = sorted(out, key=lambda o: -abs(np.log(o[6] / o[4])))[:5]
        print(f"       {'seat':22s} {'own mean':>8s} {'538 mean':>8s} {'538 sd':>7s} {'P(a)':>9s} {'P(b)':>9s} {'P(c)':>9s} {'control p (a)':>14s} {'(c)':>10s}")
        for cid, mo, m5, sd5, Pa, Pb, Pc, pv, ctl in worst:
            print(f"       {cid:22s} {mo:8.4f} {m5:8.4f} {sd5:7.4f} {Pa:9.5f} {Pb:9.5f} {Pc:9.5f} {ctl:14.3e} {pv * Pc:10.3e}")


if __name__ == "__main__":
    main()
