"""checks/m2/c14_d3_recompute.py: every p in D3's levels recomputed from the inputs the files record (M2's second
pass, item 4; the brief's amendment of 07:44). Levels: data/state-upper, data/state-lower, data/local, data/measure.

14.1  The inventory: every contest's status, route and method, beside data/local/REPORT.md sections 4, 7 and 8.
14.2  Every p from the recorded inputs, by my own implementation (checks/m2/m2d3.py, m2lib.py):
      the deciding pair (n = the two's votes less one, the first's share), the like-race density f = k/N/(2h) and
      q = k/N, the partisan density from the recorded mean and sd (with the t4 beside it), the exact-or-density rule
      (n < 1,000 or n sd^2 < 6.25), the local calibration factor, the measures' threshold form, and event = 2p.
      Where an input is recorded rounded (mean and sd to 4 decimals, the factor to 4), the record must lie within
      the range the rounding allows (the envelope over the corners).
14.3  What the records say about themselves: the window's rule (k >= 10 or the widest window), N >= 100, the
      calibration blocks against data/local/calibration-local.json.

Reads the repository's data/ only. Run: python3 checks/m2/c14_d3_recompute.py
"""
import collections
import json
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2d3 as D  # noqa: E402
import m2lib as M  # noqa: E402

LIKE_ROUTES = ("class", "boundary", "runoff", "like past measures")


def h1(s):
    print("\n" + "=" * 100 + f"\n{s}\n" + "=" * 100)


def norm_reason(s):
    import re
    s = re.sub(r"\(\d[\d,]*\)", "(N)", s)
    s = re.sub(r"'[^']*'", "'...'", s)
    s = re.sub(r"\d+%", "N%", s)
    s = re.sub(r"\d[\d,]* votes", "N votes", s)
    s = re.sub(r"\(\d[\d,]*\)", "(N)", s)
    return s.split(":")[0][:110]


class Tally:
    """Counts of checks by name, with the worst failures kept."""

    def __init__(self):
        self.ok = collections.Counter()
        self.bad = collections.Counter()
        self.worst = collections.defaultdict(list)

    def add(self, name, passed, rid, detail, size=0.0):
        if passed:
            self.ok[name] += 1
        else:
            self.bad[name] += 1
            w = self.worst[name]
            w.append((size, rid, detail))
            if len(w) > 200:
                w.sort(key=lambda x: -x[0])
                del w[60:]

    def report(self, label):
        print(f"\n  {label}: checks by name (passed / failed)")
        for name in sorted(set(self.ok) | set(self.bad)):
            print(f"    {name:60s} {self.ok[name]:8d} / {self.bad[name]:6d}")
        for name, w in sorted(self.worst.items()):
            w.sort(key=lambda x: -x[0])
            print(f"    worst failures of '{name}' ({self.bad[name]}):")
            for size, rid, detail in w[:8]:
                print(f"      {rid}: {detail}")


def inventory():
    h1("14.1 The inventory of D3's levels [measured]")
    for level in D.LEVELS:
        rs = D.rows(level)
        st = collections.Counter(r["status"] for r in rs)
        years = sorted({r["year"] for r in rs})
        src = collections.Counter((r["src"], r["by"]) for r in rs)
        print(f"\n{level}: {len(rs):,} contests, years {years[0]}-{years[-1]} ({len(years)} years); "
              f"p with a value {st['value']:,}, not computed {st['not_computed']:,}, no p block {st['none']:,}")
        print("  result source / p computed by: " + "; ".join(f"{k[0]}/{k[1]} {v:,}" for k, v in src.most_common()))
        rm = collections.Counter()
        for r in rs:
            if r["status"] == "value":
                rm[(r["route"], r["p"].get("method"), "calibrated" if r["cal"] else "", "t4" if r["p"].get("alongside") else "")] += 1
        print("  p with a value, by route / method:")
        for k, v in sorted(rm.items(), key=lambda kv: (str(kv[0][0]), str(kv[0][1]))):
            print(f"    {str(k[0]):22s} {str(k[1]):42s} {k[2]:10s} {k[3]:3s} {v:8,}")
        zero = [r for r in rs if r["status"] == "value" and r["route"] is None]
        zr = collections.Counter((r["p"]["value"] == 0 and r["p"].get("event") == 0, norm_reason(r["reason"] or "")) for r in zero)
        print("  p with a value and no forecast:")
        for k, v in zr.most_common():
            print(f"    value 0: {k[0]!s:5s} {v:8,}  {k[1]}")
        nc = collections.Counter(norm_reason(r["reason"] or "") for r in rs if r["status"] == "not_computed")
        print(f"  not computed, the reasons ({len(nc)} kinds), the largest:")
        for k, v in nc.most_common(14):
            print(f"    {v:8,}  {k}")
        if level == "measure":
            qk = collections.Counter((r["question"] or {}).get("scope") + " " + (r["question"] or {}).get("kind") for r in rs if r["question"])
            print("  questions by scope and kind: " + "; ".join(f"{k} {v:,}" for k, v in qk.most_common()))
    # the report's figures, for the eye
    su, sl = D.rows("state-upper"), D.rows("state-lower")
    both = su + sl
    kl = [r for r in both if r["src"] == "klarner"]
    cnt = collections.Counter(r["route"] for r in kl if r["status"] == "value")
    print("\nREPORT section 4 counts the Klarner-built levels together with data/primary (189,103 contests; p computed "
          "93,285: (a) 72,273, (b) 10,993, (c) 8,875, (d) 1,144; p = 0: 66,534). Here, state-upper and state-lower "
          f"from Klarner only (no primaries): {len(kl):,} contests; p computed by route: "
          + ", ".join(f"{k} {v:,}" for k, v in sorted(cnt.items(), key=str))
          + f"; p = 0: {sum(1 for r in kl if r['status'] == 'value' and r['route'] is None):,}.")
    loc = D.rows("local")
    for y in (2024, 2022, 2020, 2018):
        ry = [r for r in loc if r["year"] == y and r["src"] == "medsl"]
        v = collections.Counter(r["route"] for r in ry if r["status"] == "value")
        print(f"local {y} (MEDSL): {len(ry):,} contests; p computed: like races {v['class'] + v['boundary']:,} "
              f"(class {v['class']:,}, boundary {v['boundary']:,}), partisan {v['partisan']:,}; p = 0: {v[None]:,} "
              f"(REPORT section 7: 2024 19,704 contests, p for 3,013 = 2,066 like-race + 947 partisan, p = 0 for 10,158; "
              f"2020 8,956, p = 0 for 3,617; 2022 441; 2018 14,177).")
    ms = D.rows("measure")
    v = collections.Counter((r["year"], r["status"] == "value") for r in ms if r["route"] == "like past measures")
    print("measure: p computed by year: " + ", ".join(f"{y} {n}" for (y, ok), n in sorted(v.items()) if ok)
          + " (REPORT section 8: 64, 22 in 2022 and 42 in 2024).")


def recompute():
    h1("14.2 Every p from the recorded inputs, by my own implementation [measured]")
    cal_file = json.load(open(os.path.join(M.DATA, "local", "calibration-local.json")))
    cal_tab = {}
    for group, g in cal_file["routes"].items():
        for y, f in g["factors"].items():
            if f:
                cal_tab[(group, int(y))] = f
    maxrel = collections.defaultdict(float)
    for level in D.LEVELS:
        T = Tally()
        rs = D.rows(level)
        n_exact = 0
        for r in rs:
            if r["status"] != "value":
                continue
            p, rid = r["p"], r["id"]
            if r["route"] is None:
                T.add("p = 0: value and event 0, reason says unopposed", p["value"] == 0 and p.get("event") == 0 and
                      "unopposed" in (r["reason"] or ""), rid, r["reason"])
                continue
            if p["value"] == 0 and "reason" in p:
                T.add("value 0 with a reason (no like race in the window)", True, rid, p["reason"])
                continue
            # the deciding pair
            pair = r["pair"]
            if pair:
                v0, v1 = pair["votes"]
                n = v0 + v1 - 1
                key = "share_yes" if r["pair_kind"] == "two_way" else "share_first"
                T.add("pair: n = the two's votes less one", pair["n_other_voters"] == n, rid, f"{pair['n_other_voters']} vs {n}")
                T.add("pair: the first's share = votes[0] / (n + 1)", abs(pair[key] - round(v0 / (n + 1), 6)) <= 1.5e-6, rid,
                      f"{pair[key]} vs {v0 / (n + 1):.6f}")
                T.add("p.n = the pair's n", p.get("n") == n, rid, f"p.n {p.get('n')} vs {n}")
            else:
                T.add("pair block present", False, rid, "no two_party/boundary/two_way block")
                continue
            n = p.get("n")
            factor = (r["cal"] or {}).get("factor")
            fbox = [(factor - 5e-5, factor + 5e-5)] if factor else []
            if r["route"] in LIKE_ROUTES:
                h = D.window_h(r["win"])
                N, kin = r["N"], r["kin"]
                T.add("like races: the window is 1, 2 or 5 points about the centre", h in D.WINDOWS and
                      abs(r["win"][0] + r["win"][1] - 2 * (r["t"] if r["route"] == "like past measures" else 0.5)) < 1e-9,
                      rid, f"window {r['win']}")
                T.add("like races: k >= 10 in the window, or the widest window", kin >= D.MIN_IN_WINDOW or h == D.WINDOWS[-1],
                      rid, f"k {kin} at h {h}")
                T.add("like races: N >= 100", N >= D.MIN_CLASS, rid, f"N {N}")
                T.add("like races: q = k / N to 5 decimals", abs(r["q"] - round(kin / N, 5)) < 1e-9, rid,
                      f"q {r['q']} vs {kin / N:.5f}")
                f = kin / N / (2 * h)
                if r["route"] == "like past measures":
                    t = r["t"]
                    T.add("measure: p.threshold = the threshold read", p.get("threshold") == t, rid, f"{p.get('threshold')} vs {t}")
                    yes, no = (1 - t) * f / n, t * f / n
                    for name, mine, rec in (("measure: f_t = k/N/(2h)", f, p.get("f_t")), ("measure: yes = (1 - t) f / n", yes, p.get("yes")),
                                            ("measure: no = t f / n", no, p.get("no")), ("measure: value = the larger", max(yes, no), p["value"]),
                                            ("measure: event = f / n", f / n, p.get("event"))):
                        d = D.rel(mine, rec)
                        maxrel[(level, name)] = max(maxrel[(level, name)], d if d is not None else 9)
                        T.add(name, d is not None and d <= 1e-5, rid, f"{rec} vs {mine:.6g}", d or 0)
                    of = "either ballot" if t == 0.5 else ("a No ballot" if t > 0.5 else "a Yes ballot")
                    T.add("measure: value_of", p.get("value_of") == of, rid, f"{p.get('value_of')} vs {of}")
                    continue
                # like races: f(1/2), calibrated for local where a factor is recorded
                lo, hi = D.envelope(lambda k_=1.0: f * k_, fbox) if fbox else (f, f)
                d = D.rel(p.get("f_half"), f * (factor or 1.0))
                maxrel[(level, "like: f_half")] = max(maxrel[(level, "like: f_half")], d)
                T.add("like races: f_half = k/N/(2h) (x factor where calibrated)", D.within(p.get("f_half"), lo, hi), rid,
                      f"f_half {p.get('f_half')} vs {f * (factor or 1.0):.6g} (k {kin}, N {N}, h {h}, factor {factor})", d)
                fc = p["f_half"]   # the recorded (calibrated) density is what p was computed from
                s = D.sd_eq(fc)
                use = D.method_rule(n, s)
                T.add("like races: exact where n < 1,000 or n sd^2 < 6.25, density otherwise", p.get("method") == use, rid,
                      f"method {p.get('method')} vs {use} (n {n}, sd_eq {s:.4g}, n sd^2 {n * s * s:.3g})")
                if p.get("method") == "exact":
                    n_exact += 1
                    if fbox:
                        plo = M.p_exact(n, 0.5, D.sd_eq(f * fbox[0][0]))
                        phi = M.p_exact(n, 0.5, D.sd_eq(f * fbox[0][1]))
                        lo, hi = min(plo, phi), max(plo, phi)
                    else:
                        lo = hi = M.p_exact(n, 0.5, s)
                    d = D.rel(p["value"], (lo + hi) / 2)
                    maxrel[(level, "like: p exact")] = max(maxrel[(level, "like: p exact")], d)
                    T.add("like races: p = the exact lattice sum at sd_eq", D.within(p["value"], lo, hi, 2e-5), rid,
                          f"p {p['value']} vs {(lo + hi) / 2:.6g}", d)
                    if not D.within(p["value"], lo, hi, 2e-5):
                        # the pipeline's normal is cut to (0, 1) and renormalised (model/math/common.py normalmix_pmf),
                        # which raises a flat like-race density by 1/mass: the record against that sum
                        if fbox:
                            rlo = M.p_exact(n, 0.5, D.sd_eq(f * fbox[0][0]), renormalize=True)
                            rhi = M.p_exact(n, 0.5, D.sd_eq(f * fbox[0][1]), renormalize=True)
                            rlo, rhi = min(rlo, rhi), max(rlo, rhi)
                        else:
                            rlo = rhi = M.p_exact(n, 0.5, s, renormalize=True)
                        T.add("like races: where the exact sum fails, the record = the sum of the normal cut to (0, 1) and renormalised",
                              D.within(p["value"], rlo, rhi, 2e-5), rid, f"p {p['value']} vs renormalised {(rlo + rhi) / 2:.6g}",
                              D.rel(p["value"], (rlo + rhi) / 2))
                else:
                    mine = fc / (2 * n)
                    d = D.rel(p["value"], mine)
                    maxrel[(level, "like: p density")] = max(maxrel[(level, "like: p density")], d)
                    T.add("like races: p = f_half / (2n)", d <= 1e-5, rid, f"p {p['value']} vs {mine:.6g}", d)
            elif r["route"] == "partisan":
                sh = r["share"]
                mean, sd = sh["mean"], sh["sd"]
                T.add("partisan: tails normal, of the Democrat", sh.get("tails") == "normal" and "Democrat" in sh.get("of", ""), rid, str(sh))
                boxes = [(mean - 5e-5, mean + 5e-5), (sd - 5e-5, sd + 5e-5)] + fbox
                fn = lambda m_, s_, k_=1.0: M.f_half(m_, s_) * k_   # noqa: E731
                lo, hi = D.envelope(fn, boxes)
                f0 = M.f_half(mean, sd) * (factor or 1.0)
                d = D.rel(p.get("f_half"), f0)
                maxrel[(level, "partisan: f_half")] = max(maxrel[(level, "partisan: f_half")], d)
                T.add("partisan: f_half = the normal density at 1/2 (x factor where calibrated)", D.within(p.get("f_half"), lo, hi), rid,
                      f"f_half {p.get('f_half')} vs {f0:.6g} [{lo:.6g}, {hi:.6g}] (mean {mean}, sd {sd}, factor {factor})", d)
                rules = {D.method_rule(n, s_) for s_ in (sd - 5e-5, sd, sd + 5e-5)}
                T.add("partisan: exact where n < 1,000 or n sd^2 < 6.25, density otherwise",
                      p.get("method") in rules, rid, f"method {p.get('method')} vs {rules} (n {n}, sd {sd}, n sd^2 {n * sd * sd:.3g})")
                t4 = (p.get("alongside") or {}).get("t4")
                T.add("partisan: a t4 beside it", bool(t4), rid, "no alongside.t4")
                if p.get("method") == "exact":
                    n_exact += 1
                    fn = lambda m_, s_, k_=1.0: M.p_exact(n, m_, s_) * k_   # noqa: E731
                    lo, hi = D.envelope(fn, boxes)
                    mid = M.p_exact(n, mean, sd) * (factor or 1.0)
                    d = D.rel(p["value"], mid)
                    maxrel[(level, "partisan: p exact")] = max(maxrel[(level, "partisan: p exact")], d)
                    T.add("partisan: p = the exact lattice sum (x factor)", D.within(p["value"], lo, hi, 2e-5), rid,
                          f"p {p['value']} vs {mid:.6g} [{lo:.6g}, {hi:.6g}]", d)
                    if t4:
                        fn = lambda m_, s_, k_=1.0: M.p_exact(n, m_, s_, "t4") * k_   # noqa: E731
                        lo, hi = D.envelope(fn, boxes)
                        mid = M.p_exact(n, mean, sd, "t4") * (factor or 1.0)
                        d = D.rel(t4["value"], mid)
                        T.add("partisan: the t4's p (exact, x factor)", D.within(t4["value"], lo, hi, 2e-5) and t4.get("method") == "exact",
                              rid, f"t4 {t4['value']} ({t4.get('method')}) vs {mid:.6g} [{lo:.6g}, {hi:.6g}]", d)
                else:
                    mine = p["f_half"] / (2 * n)
                    d = D.rel(p["value"], mine)
                    maxrel[(level, "partisan: p density")] = max(maxrel[(level, "partisan: p density")], d)
                    T.add("partisan: p = f_half / (2n)", d <= 1e-5, rid, f"p {p['value']} vs {mine:.6g}", d)
                    if t4:
                        fn = lambda m_, s_, k_=1.0: M.f_half(m_, s_, "t4") * k_ / (2 * n)   # noqa: E731
                        lo, hi = D.envelope(fn, boxes)
                        mid = M.f_half(mean, sd, "t4") * (factor or 1.0) / (2 * n)
                        d = D.rel(t4["value"], mid)
                        maxrel[(level, "partisan: t4 density")] = max(maxrel[(level, "partisan: t4 density")], d)
                        T.add("partisan: the t4's p = t4 density at 1/2 / (2n) (x factor)", D.within(t4["value"], lo, hi) and t4.get("method") == "density",
                              rid, f"t4 {t4['value']} ({t4.get('method')}) vs {mid:.6g} [{lo:.6g}, {hi:.6g}]", d)
                if t4:
                    T.add("partisan: the t4's event = 2 p", D.rel(t4.get("event"), 2 * t4["value"]) <= 1e-5, rid, f"{t4.get('event')} vs {2 * t4['value']:.6g}")
            else:
                T.add("route known", False, rid, f"route {r['route']}")
                continue
            d = D.rel(p.get("event"), 2 * p["value"])
            T.add("event = 2 p", d is not None and d <= 1e-5, rid, f"event {p.get('event')} vs {2 * p['value']:.6g}")
            # the calibration block against calibration-local.json
            if r["cal"]:
                group = "like races" if r["route"] in ("class", "boundary") else "partisan"
                f = cal_tab.get((group, r["year"]))
                key = f"{r['route']}, {r['office_scope']} {r['office_type']}"
                if f is None:
                    T.add("calibration: a factor for this year in calibration-local.json", False, rid, f"{group} {r['year']}")
                else:
                    own = f["own"].get(key)
                    want, of = (own, key) if own is not None else (f["pooled"], "pooled over the fitting years' races")
                    T.add("calibration: factor and 'of' match calibration-local.json (own by office type else pooled)",
                          abs(r["cal"]["factor"] - want) <= 6e-4 and r["cal"]["of"] == of and r["cal"]["fitted_on"] == f["fitted_on"],
                          rid, f"{r['cal']} vs {want} ({of}), fitted on {f['fitted_on']}")
                T.add("calibration: 'calibrated' in p.under", "calibrated" in p.get("under", ""), rid, p.get("under"))
            elif level == "local" and r["src"] == "medsl" and r["year"] in (2022, 2024):
                T.add("local 2022/2024 MEDSL p without a calibration block", False, rid, f"{r['route']} {p.get('under')}")
        T.report(f"{level} ({n_exact:,} exact sums recomputed)")
    print("\n  largest relative differences, record against my own figure:")
    for k, v in sorted(maxrel.items()):
        print(f"    {k[0]:12s} {k[1]:24s} {v:.3g}")


if __name__ == "__main__":
    print(f"c14: D3's levels recomputed from the recorded inputs; repository HEAD {M.git_head()}")
    inventory()
    recompute()
