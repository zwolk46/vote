"""C5. The published figures the record compares itself with (briefs/M2-check-computed-p.md, item 4):
  5.1 The Economist, 2020: the record's p over its published p_decisive_vote runs from 0.14 (Ohio) to 1.32
      (Arizona). Gelman, Silver and Edlin's method (research/decisiveness-models-v2.md 3.1 B: the share of draws
      in which the state is necessary, times the t4 density at zero of the state's vote margin among those
      draws, fitted by mean and scale) is run on the Economist's own 80,000 draws, to see whether it is the
      Economist's method; then what separates it from the record's window count.
  5.2 Gelman, King and Boscardin, 1992 ("about 1 in 10 million", a tie a full decision: 1 in 20 million as p)
      against the record's 1 in 45.6 million: the record's 1992 forecast recomputed under other horizons and
      error sizes, to see which difference carries the gap.
  5.3 Gelman, Silver and Edlin, 2008 (close states about 1 in 10 million; average 1 in 60 million; New York,
      California and Texas about 1 in a billion) against the record's own forecast (NM 1 in 15.9 million, VA
      35.7, NH 23.5, CO 22.1; CA 152 million): a poll-based 2008 forecast (The Economist's 2008 back-test
      table of state means and intervals, its us-potus-model repository, MIT/CC BY 4.0, read outside the
      repository) run through the record's College stage, to see whether poll-based state errors reproduce
      GSE's pattern.
Nothing here chooses a figure for the site; both readings are given where either is defensible.
"""
import csv
import io
import math
import os
import re
import sys
import zipfile

import numpy as np
from scipy import stats, optimize

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402

SQRT2 = math.sqrt(2.0)
ECON_README = os.path.join(L.CACHE, "economist_us-potus-model_README.md")
ECON_README_SHA = "70dd5e44601c7e3ec37a5e6d067a62e24ae4d5a29743468c432a61fdc624fab1"
ECON_README_COMMIT = "b89e602ec03e81c797c66cf2743af6fdae4aa526 (2020-10-15)"


def load_econ_draws():
    z = zipfile.ZipFile(os.path.join(L.CACHE, "economist_model_output.zip"))
    name = [n for n in z.namelist() if n.endswith("/electoral_college_simulations.csv")][0]
    rd = csv.reader(io.StringIO(z.read(name).decode("utf-8")))
    head = next(rd)
    states = head[3:]
    data = np.array([[float(x) for x in r] for r in rd])
    ks = [n for n in z.namelist() if n.endswith("/key_states_summary.csv")][0]
    key = {r["state"]: r for r in csv.DictReader(io.StringIO(z.read(ks).decode("utf-8")))}
    return states, data[:, 1].astype(int), data[:, 3:], key


def gse_on_draws(shares, dem_ev, ev, i, n, scale_div=1.0, tails="t4", amb_step=1e-4):
    """GSE's two factors on a forecaster's draws for unit i, the margin in votes (n the two-party count)."""
    K = shares.shape[0]
    won_i = shares[:, i] > 0.5
    amb_i = np.isclose(shares[:, i], 0.5, atol=amb_step / 10)
    dem_other = np.where(won_i & ~amb_i, dem_ev - ev[i], dem_ev)      # as the record reads the published total
    margin_other = 2 * dem_other - (538 - ev[i])                      # Democrat minus Republican, other units
    nec_full = np.abs(margin_other) < ev[i]
    nec_half = np.abs(margin_other) == ev[i]
    P_nec = (nec_full.sum() + 0.5 * nec_half.sum()) / K
    sub = nec_full | nec_half
    m = n * (2 * shares[sub, i] - 1)
    if sub.sum() < 3:
        return P_nec, int(sub.sum()), float("nan"), float("nan"), float("nan")
    M, S = m.mean(), m.std(ddof=1)
    if tails == "t4":
        dens = stats.t.pdf(0.0, 4, loc=M, scale=S / scale_div)
    else:
        dens = stats.norm.pdf(0.0, M, S / scale_div)
    return P_nec, int(sub.sum()), M, S, P_nec * dens


def main():
    print("C5. PUBLISHED FIGURES: THE ECONOMIST 2020, GKB 1992, GSE 2008")
    print(f"repository HEAD {L.git_head()}")
    # ------------------------------------------------------------------ 5.1
    print("5.1 The Economist, 2020: GSE's method on the Economist's own draws (P(necessary) x t4 density at 0 of the vote margin "
          "among the necessary draws), against its published p_decisive_vote and the record's window count")
    states, dem_ev, shares, key = load_econ_draws()
    econ = L.load_json(os.path.join(L.DATA, "president", "inputs", "economist_2020.json"))
    ev = np.array([econ["states"][s]["ev"] for s in states])
    doc = L.load_json(os.path.join(L.DATA, "president", "2020.json"))
    rec = {}
    for c in doc["contests"]:
        for f in c["forecasts"]:
            if f["by"] == "The Economist":
                rec[c["place"]["state"]] = (f, c["two_party"] if "two_party" in c else c["result"]["two_party"], c["result"]["two_party"])
    print(f"    {'state':5s} {'ev':>3s} {'P(nec)':>8s} {'p_tipping':>9s} {'draws':>6s} {'M/S':>6s} {'p GSE-t4':>9s} {'published':>9s} {'ratio':>6s} "
          f"{'p record':>9s} {'rec/pub':>7s} {'GSE-normal/pub':>14s} {'t4 scale S/sqrt2 /pub':>21s}")
    rows = []
    for i, s in enumerate(states):
        f, _, n2 = rec[s]
        n = n2 - 1
        P_nec, k, M, S, p_t4 = gse_on_draws(shares, dem_ev, ev, i, n)
        _, _, _, _, p_norm = gse_on_draws(shares, dem_ev, ev, i, n, tails="normal")
        _, _, _, _, p_t4b = gse_on_draws(shares, dem_ev, ev, i, n, scale_div=SQRT2)
        pub = f["p_published"]
        p_rec = f["p"]["value"] if f["p"] else None
        rows.append((pub, s, ev[i], P_nec, float(key[s]["p_tipping_point"]), k, M / S if S else float("nan"), p_t4, pub, p_t4 / pub, p_rec,
                     (p_rec / pub) if p_rec else float("nan"), p_norm / pub, p_t4b / pub))
    for r in sorted(rows, reverse=True):
        pub, s, e, P_nec, tip, k, ms, p_t4, pub, rat, p_rec, rr, rn, rb = r
        print(f"    {s:5s} {e:3d} {P_nec:8.4f} {tip:9.4f} {k:6d} {ms:6.2f} {p_t4:9.3e} {pub:9.3e} {rat:6.3f} "
              f"{(p_rec if p_rec else float('nan')):9.3e} {rr:7.3f} {rn:14.3f} {rb:21.3f}")
    rat = np.array([r[9] for r in rows])
    with_p = [r for r in rows if r[10]]
    print(f"    GSE-t4 / published over 51 states: median {np.median(rat):.3f}, range {rat.min():.3f}-{rat.max():.3f}; "
          f"within 10% in {int(np.sum(np.abs(rat - 1) < 0.1))} states, within 25% in {int(np.sum(np.abs(rat - 1) < 0.25))}")
    print(f"    P(necessary) against p_tipping_point: largest |difference| {max(abs(r[3] - r[4]) for r in rows):.4f} "
          f"(p_tipping_point is the share of draws in which the state is the tipping-point state, a different quantity)")
    rr = np.array([r[11] for r in with_p])
    print(f"    the record's window p / published over the {len(with_p)} states with a record p: median {np.median(rr):.3f}, range {rr.min():.3f}-{rr.max():.3f}")
    # a different n would scale every state alike: the n the published figure implies under GSE's method, against the
    # 2016 and 2020 two-party counts
    doc16 = L.load_json(os.path.join(L.DATA, "president", "2016.json"))
    n16 = {c["place"]["state"]: c["result"]["two_party"] for c in doc16["contests"] if not c["place"]["district"]}
    imp = []
    for r in rows:
        s = r[1]; f, _, n2 = rec[s]
        imp.append((s, r[7] * (n2 - 1) / r[8], n2 - 1, n16[s]))
    big = [x for x in imp if rec[x[0]][0]["p"]]
    a = np.array([x[1] / x[2] for x in big]); b = np.array([x[1] / x[3] for x in big])
    print(f"    the n the published figure implies if the method is GSE's (n_implied = p_GSE x n_2020 / p_published), over the {len(big)} states with a record p: "
          f"n_implied / n_2020 median {np.median(a):.3f} (10-90% {np.quantile(a, .1):.2f}-{np.quantile(a, .9):.2f}); n_implied / n_2016 median {np.median(b):.3f} "
          f"({np.quantile(b, .1):.2f}-{np.quantile(b, .9):.2f}); n_2020 / n_2016 median {np.median([x[2] / x[3] for x in big]):.3f}")
    # what separates the two on the same draws: the window's joint count vs the parametric density
    print("    the same draws, two readings of P(tie and decisive) for the states the record computes:")
    print(f"    {'state':5s} {'window: weighted/in-window/K/width':>36s} {'GSE: P(nec) x f_t4(0)':>22s} {'empirical f(0) among nec, +-0.01':>32s} {'t4 fit f(0)':>11s} {'normal fit':>10s}")
    for r in sorted(with_p, reverse=True)[:16]:
        s = r[1]; i = states.index(s)
        f, _, n2 = rec[s]; n = n2 - 1
        P_nec, k, M, S, p_t4 = gse_on_draws(shares, dem_ev, ev, i, n)
        won_i = shares[:, i] > 0.5
        dem_other = np.where(won_i, dem_ev - ev[i], dem_ev)
        margin_other = 2 * dem_other - (538 - ev[i])
        sub = np.abs(margin_other) <= ev[i]
        x = shares[sub, i] - 0.5
        emp = np.mean(np.abs(x) <= 0.01 + 1e-5) / 0.0201 / (2 * n) if sub.sum() else float("nan")   # per-vote density, our convention
        print(f"    {s:5s} {f['p']['window_weighted']:8.0f}/{f['p']['window_draws']:6d}/80000/0.0201 -> {f['p']['value']:9.3e} "
              f"{P_nec:7.4f} x {stats.t.pdf(0, 4, M, S):9.3e} = {p_t4:9.3e} {P_nec * emp:32.3e} {P_nec * stats.t.pdf(0, 4, M, S):11.3e} {P_nec * stats.norm.pdf(0, M, S):10.3e}")

    # ------------------------------------------------------------------ 5.2
    print("5.2 Gelman, King and Boscardin, 1992: the record's 1992 forecast under other horizons and error sizes")
    doc = L.load_json(os.path.join(L.DATA, "president", "1992.json"))
    units, mu, ev92, n92, w92 = [], [], [], [], []
    for c in doc["contests"]:
        own = next(f for f in c["forecasts"] if f["by"] == "the model's own")
        units.append(c["place"]["state"]); mu.append(own["share"]["mean"]); ev92.append(own["unit_ev"])
        n92.append(c["p"]["n_other_voters"]); w92.append(c["result"]["two_party"])
    mu, ev92, n92, w92 = map(np.array, (mu, ev92, n92, w92))
    own = next(f for c in doc["contests"] for f in c["forecasts"] if f["by"] == "the model's own")
    s_nat0, s_state0 = own["share"]["national_sd"], own["share"]["state_sd"]
    polls = L.load_json(os.path.join(L.DATA, "president", "inputs", "fte_poll_averages.json"))["years"]["1992"]
    def nat(when):
        us = polls[when]["units"]["US"]
        return us["dem"] / (us["dem"] + us["rep"]), polls[when]["date"]
    eve_mean, eve_date = nat("eve"); sep_mean, sep_date = nat("two_months_out")
    print(f"    the record: national mean {eve_mean:.4f} (538's average of {eve_date}), s_nat {s_nat0:.4f}, s_state {s_state0:.4f} (t4); "
          f"the 9 September average {sep_mean:.4f} ({sep_date}); the result {0.5348:.4f}; GKB's error sds: national 2.5%, regional 2.5% (5.0% South), state 3.5% (B4 ledger)")
    print(f"    {'forecast':58s} {'avg p (vote-weighted)':>21s} {'1 in':>12s} {'P(D wins)':>9s} {'spread max/min (50 states)':>26s} {'highest':>14s}")
    def run(label, shift, s_nat, s_state, tails):
        mm = mu + shift
        r = L.W_fourier(mm, np.full(len(mm), s_state), ev92, s_nat, 538, 270, tails)
        p = r["f_half"] / (2 * n92) * r["W"]
        avg = (p * w92).sum() / w92.sum()
        # P(D wins the College) under the same joint model, from the Fourier count of every unit
        grid = np.linspace(-12 * s_nat, 12 * s_nat, 1201); h = grid[1] - grid[0]
        simp = np.ones(1201); simp[1:-1:2], simp[2:-1:2] = 4.0, 2.0; simp *= h / 3
        prior = stats.norm.pdf(grid, 0, s_nat)
        x = 0.5 - mm[None, :] - grid[:, None]
        q = stats.norm.sf(x / s_state) if tails == "normal" else stats.t.sf(x / (s_state / SQRT2), 4)
        pmf = L.others_ev_pmf(q, ev92)      # every unit
        win = pmf[:, 270:].sum(axis=1) + 0.5 * pmf[:, 269]
        PD = float((simp * prior * win).sum())
        keep = [k for k, u in enumerate(units) if u != "DC"]
        print(f"    {label:58s} {avg:21.3e} {1 / avg:12,.0f} {PD:9.3f} {p[keep].max() / p[keep].min():26.0f} {units[int(np.argmax(p))]} 1 in {1 / p.max():,.0f}")
        return avg
    run("record: eve mean, s_nat .022, s_state .0425, t4", 0.0, s_nat0, s_state0, "t4")
    run("9 September mean and its fit (s_nat .035, s_state .0425), t4", sep_mean - eve_mean, 0.0350, s_state0, "t4")
    run("eve mean, GKB-size errors: s_nat .035 (nat+regional), s_state .035, t4", 0.0, 0.035, 0.035, "t4")
    run("eve mean, s_nat .035, s_state .035, normal", 0.0, 0.035, 0.035, "normal")
    run("eve mean, s_nat .050, s_state .035, t4", 0.0, 0.050, 0.035, "t4")
    run("a closer mean (0.52, hypothetical), s_nat .022, s_state .0425, t4", 0.52 - eve_mean, s_nat0, s_state0, "t4")
    run("a closer mean (0.52, hypothetical), s_nat .035, s_state .035, t4", 0.52 - eve_mean, 0.035, 0.035, "t4")

    # ------------------------------------------------------------------ 5.3
    print("5.3 Gelman, Silver and Edlin, 2008: a poll-based 2008 forecast (The Economist's back-test table) through the record's College stage")
    if not os.path.exists(ECON_README):
        print(f"    {ECON_README} not in the cache; skipped")
        return
    h = L.sha256(ECON_README)
    print(f"    source: TheEconomist/us-potus-model README.md, commit {ECON_README_COMMIT}, sha256 {h} ({'as recorded' if h == ECON_README_SHA else 'DIFFERS from the recorded hash'}); "
          "its 2008 table 'Predictions for each state': mean, low, high, prob, se (se = (high - mean) / 1.68 in its README.Rmd; polls up to election day: a back-test)")
    text = open(ECON_README).read()
    sec = text.split("### 2008")[1].split("### 2012")[0]
    tab = sec.split("Predictions for each state")[1]
    table = {}
    for line in tab.splitlines():
        m = re.match(r"\|\s*(\S+)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|", line)
        if m:
            table[m.group(1)] = tuple(float(m.group(k)) for k in range(2, 7))
    nat_row = [k for k in table if len(k) > 2 or not k.isalpha()]
    print(f"    rows read: {len(table)} (national row label {nat_row}); national mean {table[nat_row[0]][0] if nat_row else float('nan')}, "
          f"prob {table[nat_row[0]][3] if nat_row else float('nan')}")
    doc = L.load_json(os.path.join(L.DATA, "president", "2008.json"))
    units, n08, ev08, w08, own_mu, own_p = [], [], [], [], [], []
    for c in doc["contests"]:
        if c["place"]["district"] or not c["p"]:
            continue
        own = next(f for f in c["forecasts"] if f["by"] == "the model's own")
        units.append(c["place"]["state"]); n08.append(c["p"]["n_other_voters"]); ev08.append(own["unit_ev"]); w08.append(c["result"]["two_party"])
        own_mu.append(own["share"]["mean"]); own_p.append(c["p"]["value"])
    n08, ev08, w08, own_p = map(np.array, (n08, ev08, w08, own_p))
    own = next(f for c in doc["contests"] for f in c["forecasts"] if f["by"] == "the model's own")
    mu_e = np.array([table[u][0] for u in units])
    se_e = np.array([table[u][4] for u in units])
    sd_e = (np.array([table[u][2] for u in units]) - mu_e) / 1.96     # the interval read as a normal 95% one
    print(f"    the Economist's 2008 state sds: se as printed median {np.median(se_e):.4f}; (high - mean)/1.96 median {np.median(sd_e):.4f}; "
          f"the record's own 2008 sd {own['share']['sd']:.4f} (s_nat {own['share']['national_sd']:.4f}, s_state {own['share']['state_sd']:.4f})")
    PD_target = table[nat_row[0]][3] if nat_row else None

    def PD_of(s_d, sd, tails):
        s_unit = np.sqrt(np.maximum(sd ** 2 - s_d ** 2, 1e-8))
        grid = np.linspace(-12 * s_d, 12 * s_d, 801); hh = grid[1] - grid[0]
        simp = np.ones(801); simp[1:-1:2], simp[2:-1:2] = 4.0, 2.0; simp *= hh / 3
        prior = stats.norm.pdf(grid, 0, s_d)
        x = 0.5 - mu_e[None, :] - grid[:, None]
        q = stats.norm.sf(x / s_unit) if tails == "normal" else stats.t.sf(x / (s_unit / SQRT2), 4)
        pmf = L.others_ev_pmf(q, ev08)
        win = pmf[:, 270:].sum(axis=1) + 0.5 * pmf[:, 269]
        return float((simp * prior * win).sum())
    gse_pub = {"NM": 1e-7, "VA": 1e-7, "NH": 1e-7, "CO": 1e-7, "OH": 3.1e-8, "UT": 2e-10, "DC": 2e-12, "NY": 1e-9, "CA": 1e-9, "TX": 1e-9}
    print(f"    {'reading of the table':54s} {'s_d':>6s} {'P(D)':>6s} {'avg 1 in':>10s} {'NM':>6s} {'VA':>6s} {'NH':>6s} {'CO':>6s} {'OH':>6s} {'NY':>7s} {'CA':>7s} {'TX':>7s} {'UT':>9s} {'DC':>9s}   (1 in millions; GSE: ~10, 10, 10, 10, 32, 1000, 1000, 1000, 5000, 500000)")
    def show(label, sd, tails, s_d=None):
        if s_d is None and PD_target:
            lo, hi = 0.002, 0.95 * sd.min()
            f_lo, f_hi = PD_of(lo, sd, tails) - PD_target, PD_of(hi, sd, tails) - PD_target
            s_d = optimize.brentq(lambda v: PD_of(v, sd, tails) - PD_target, lo, hi) if f_lo * f_hi < 0 else (lo if abs(f_lo) < abs(f_hi) else hi)
        s_unit = np.sqrt(np.maximum(sd ** 2 - s_d ** 2, 1e-8))
        r = L.W_fourier(mu_e, s_unit, ev08, s_d, 538, 270, tails)
        p = r["f_half"] / (2 * n08) * r["W"]
        avg = (p * w08).sum() / w08.sum()
        g = lambda u: 1 / p[units.index(u)] / 1e6
        print(f"    {label:54s} {s_d:6.4f} {PD_of(s_d, sd, tails):6.3f} {1 / avg / 1e6:10.1f} {g('NM'):6.1f} {g('VA'):6.1f} {g('NH'):6.1f} {g('CO'):6.1f} {g('OH'):6.1f} {g('NY'):7.0f} {g('CA'):7.0f} {g('TX'):7.0f} {g('UT'):9.0f} {g('DC'):9.3g}")
    gr = lambda u: 1 / own_p[units.index(u)] / 1e6
    avg_rec = (own_p * w08).sum() / w08.sum()
    print(f"    {'the record (own forecast, uniform swing, t4)':54s} {own['share']['national_sd']:6.4f} {'':6s} {1 / avg_rec / 1e6:10.1f} {gr('NM'):6.1f} {gr('VA'):6.1f} {gr('NH'):6.1f} {gr('CO'):6.1f} {gr('OH'):6.1f} {gr('NY'):7.0f} {gr('CA'):7.0f} {gr('TX'):7.0f} {gr('UT'):9.0f} {gr('DC'):9.3g}")
    print("    (the table's national win probability is 1.000: an election-day back-test, so no national swing sd can be fitted to it; "
          "a late-October forecast would carry more. Rows with a stated s_d:)")
    show("Economist means, sd = se, t4, s_d = 0.010", se_e, "t4", 0.010)
    show("Economist means, sd = se, t4, s_d = 0.015", se_e, "t4", 0.015)
    show("Economist means, sd = se, t4, s_d = 0.020", se_e, "t4", 0.020)
    show("Economist means, sd = (high-mean)/1.96, t4, s_d = 0.015", sd_e, "t4", 0.015)
    # the record's own means with poll-sized state errors
    mu_rec = np.array(own_mu)
    def show_own(label, s_nat, s_state, tails):
        r = L.W_fourier(mu_rec, np.full(len(mu_rec), s_state), ev08, s_nat, 538, 270, tails)
        p = r["f_half"] / (2 * n08) * r["W"]
        avg = (p * w08).sum() / w08.sum()
        g = lambda u: 1 / p[units.index(u)] / 1e6
        print(f"    {label:54s} {s_nat:6.4f} {'':6s} {1 / avg / 1e6:10.1f} {g('NM'):6.1f} {g('VA'):6.1f} {g('NH'):6.1f} {g('CO'):6.1f} {g('OH'):6.1f} {g('NY'):7.0f} {g('CA'):7.0f} {g('TX'):7.0f} {g('UT'):9.0f} {g('DC'):9.3g}")
    show_own("own means, s_nat .0207, s_state .020 (poll-sized), t4", own["share"]["national_sd"], 0.020, "t4")
    show_own("own means, s_nat .0207, s_state .0374 (record), normal", own["share"]["national_sd"], own["share"]["state_sd"], "normal")
    print(f"    mean |Economist mean - own mean| over 51 states: {np.mean(np.abs(mu_e - mu_rec)):.4f}; |Economist mean - result|: "
          f"{np.mean(np.abs(mu_e - np.array([next(c['result']['dem'] / c['result']['two_party'] for c in doc['contests'] if c['place']['state'] == u) for u in units]))):.4f}; "
          f"|own mean - result|: {np.mean(np.abs(mu_rec - np.array([next(c['result']['dem'] / c['result']['two_party'] for c in doc['contests'] if c['place']['state'] == u) for u in units]))):.4f}")


if __name__ == "__main__":
    main()
