"""C8 (second pass, briefs/M2-check-computed-p.md amendment of 07:44, item 1). Every Senate, House and governor
p as the files stand after D2's rounds 2-5 (#29, #32, #35, #38), recomputed from its contest's recorded inputs:

  8.1 value_uncalibrated = f(1/2) / (2 n) from the forecast's mean, sd and tails (normal, or t4 at scale sd/sqrt2);
      then value = value_uncalibrated x F / (1 + (F - 1) q) with F the recorded near-tie factor and q the
      forecast's own chance of 49-51% (REPORT 2.6); event = 2 value; every block of p and of p.alongside;
  8.2 the forecast rebuilt from the file's model block and the contest's forecast_inputs by the file's own
      mean_is and sd_is: mean = 1/2 + national_forecast + b_lean lean + b_inc inc [+ b_lag (lag - 1/2)], shrunk
      1/2 + lambda (mean - 1/2) where the level's variant of record shrinks (REPORT 2.7); national_forecast =
      c . z, national_sd = k s_a sqrt(1 + z (Z'Z)^-1 z'), s_e = k s_e_fitted, sd = sqrt(national_sd^2 + s_e^2);
  8.3 the near-tie factor each forecast carries is the one the model block gives its level (one factor) or its
      band of |mean - 1/2| (the House's band scheme), and a forecast carries none where the block has none;
  8.4 538's entries: the implied sd, p's estimated relative error (sd's error x |z^2 - 1|) and the 20% rule (#33);
  8.5 stage_two.inputs: mean, own_sd and swing_loading as REPORT 4 derives them from the forecast the seat's p
      stands under (the model's own: s_e, 1; 538's: sqrt(sd538^2 - s_a^2), 1; and the marked seats).
Nothing is imported from pipeline/. The fits themselves are redone in c9_fit2.py.
"""
import glob
import math
import os
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402

LEVELS = ("senate", "house", "governor")
TOL = 1e-9      # the files now hold mean and sd at full precision (REPORT 0.4, item 6)


def files(level):
    return sorted(glob.glob(os.path.join(L.DATA, level, "*.json")))


def near_q(mean, sd, tails):
    return float(L.cdf(0.51, mean, sd, tails) - L.cdf(0.49, mean, sd, tails))


def band_factor(m, mean):
    """The near-tie factor the model block gives a forecast with this mean: (factor, scheme) or (None, None)."""
    nt = (m or {}).get("near_tie") or {}
    if not nt.get("scheme"):
        return None, None
    if nt["scheme"] == "level":
        return nt["factor"], "level"
    d = abs(mean - 0.5)
    bands = nt["by_band"]
    b = max(i for i, x in enumerate(bands) if d >= x["band_from"])
    return bands[b]["factor"], "band"


class Tally:
    def __init__(self):
        self.n = 0
        self.worst = (0.0, None, None, None)
        self.bad = []

    def add(self, cid, rec, new, tol=TOL, label=""):
        self.n += 1
        if rec is None or new is None:
            self.bad.append((cid, rec, new, "missing", label))
            return
        d = abs(new / rec - 1.0) if rec != 0 else abs(new - rec)
        if d > self.worst[0]:
            self.worst = (d, cid, rec, new)
        if d > tol:
            self.bad.append((cid, rec, new, d, label))

    def report(self, what, show=6):
        d, cid, rec, new = self.worst
        print(f"    {what}: {self.n} compared; largest relative difference {d:.2e}"
              + (f" ({cid}: recorded {rec:.8g}, here {new:.8g})" if cid else "") + f"; {len(self.bad)} beyond {TOL:g}")
        for cid, rec, new, dd, label in self.bad[:show]:
            print(f"       MISMATCH {cid} {label}: recorded {rec} here {new} ({dd})")


def main():
    print("C8. CONGRESS AND GOVERNORS AFTER #38: EVERY p FROM ITS RECORDED INPUTS, THE FORECASTS REBUILT, F, lambda, 538, STAGE TWO")
    print(f"repository HEAD {L.git_head()}")
    grand = {}
    for level in LEVELS:
        print(f"\n== {level}")
        T = {k: Tally() for k in ("f_half", "value_uncal", "multiplier", "value", "event", "mean", "mean_unshrunk", "sd",
                                  "nat_fc", "nat_sd", "s_e", "model_sd", "rho", "factor", "sd538", "p_rel", "st2_mean",
                                  "st2_own_sd", "st2_lam", "ctl_value")}
        counts = {"files": 0, "contests": 0, "p>0": 0, "p=0": 0, "not computed": 0, "blocks": 0, "own blocks": 0,
                  "538 blocks": 0, "calibrated": 0, "shrunk": 0, "no factor (band 0.10 up or none)": 0,
                  "538 entries": 0, "538 first": 0, "538 unusable": 0, "538 rule disagrees": 0, "st2 model": 0,
                  "st2 marked": 0, "t4 first": 0}
        rule_bad = []
        for path in files(level):
            doc = L.load_json(path)
            year = doc["year"]
            m = doc.get("model")
            ch = doc.get("chamber") or {}
            counts["files"] += 1
            lam = ((m or {}).get("variant") or {}).get("shrink")
            lam = lam["factor"] if lam else None
            if m and "c" not in m:
                print(f"    {level} {year}: model block without fitted terms ({m.get('note') or m.get('method')}); no forecast of the model's own")
                m = None
            if m:
                # 8.2 the model block's own arithmetic: national_forecast, national_sd, s_e, sd, rho
                P = None
                # z from the year: midterm and the sitting president's party, taken from any contest's inputs
                fi0 = next((c["forecast_inputs"] for c in doc["contests"] if c.get("forecast_inputs")), None)
                if fi0:
                    P = 1 if fi0["president_party"] == "D" else -1
                    M = 1 if fi0["midterm"] else 0
                    z = np.array([1.0, M * P, (1 - M) * P])
                    nat = float(z @ np.array(m["c"]))
                    nat_sd = m["k"] * m["s_a"] * math.sqrt(1.0 + float(z @ np.array(m["ZtZ_inv"]) @ z))
                    s_e = m["k"] * m["s_e_fitted"]
                    sd = math.sqrt(nat_sd ** 2 + s_e ** 2)
                    T["nat_fc"].add(f"{level} {year}", m["national_forecast"], nat)
                    T["nat_sd"].add(f"{level} {year}", m["national_sd"], nat_sd)
                    T["s_e"].add(f"{level} {year}", m["s_e"], s_e)
                    T["model_sd"].add(f"{level} {year}", m["sd"], sd)
                    T["rho"].add(f"{level} {year}", m["rho"], nat_sd ** 2 / sd ** 2)
                    if ch:
                        T["nat_sd"].add(f"{level} {year} chamber", ch["common_swing_sd"], nat_sd)
                        T["s_e"].add(f"{level} {year} chamber", ch["own_sd"], s_e)
            for c in doc["contests"]:
                counts["contests"] += 1
                p = c.get("p") or {}
                if p.get("value") is None:
                    counts["not computed"] += 1
                    continue
                if p["value"] == 0.0:
                    counts["p=0"] += 1
                    continue
                counts["p>0"] += 1
                n = p["n"]
                fi = c.get("forecast_inputs") or {}
                # 8.4 every 538 entry: implied sd and p's error
                for f in c["forecasts"]:
                    if f["by"] != "538":
                        continue
                    counts["538 entries"] += 1
                    sh = f.get("share") or {}
                    chance = (f.get("chance") or {}).get("D")
                    if sh.get("sd") is None or chance in (None, 0.0, 1.0):
                        counts["538 unusable"] += 1
                        continue
                    chR = (f.get("chance") or {}).get("R")
                    q = chance / (chance + chR)          # 538's chance renormalized over the Democrat and the Republican
                    zq = stats.norm.ppf(q)
                    sd538 = (sh["mean"] - 0.5) / zq
                    T["sd538"].add(f"{c['id']} {f.get('version')}", sh["sd"], sd538, tol=1e-9)
                    if f.get("p_relative_error") is not None and f.get("simulations"):
                        # the chance's sampling error over N runs, through Phi^-1, and the mean's printed rounding
                        # the chance's sampling error over N runs carried through Phi^-1 at both ends (the larger
                        # end), as the record's note says; the mean's printed rounding (half its last digit) is
                        # not in the files, so it is left out here: a small extra term near even
                        N = f["simulations"]
                        dq = math.sqrt(q * (1 - q) / N)
                        ends = [q - dq, q + dq]
                        sd_rel = max(abs(stats.norm.ppf(e) - zq) for e in ends) / abs(zq) if 0 < min(ends) and max(ends) < 1 else float("inf")
                        p_rel = sd_rel * abs(zq ** 2 - 1)
                        T["p_rel"].add(f"{c['id']} {f.get('version')}", f["p_relative_error"], p_rel, tol=0.05,
                                       label=f"sd_rel rec {f.get('sd_relative_error'):.4g} here {sd_rel:.4g}")
                        unusable = f.get("unusable_kind")
                        if (f["p_relative_error"] >= 0.20) != (unusable == "p's error 20% or more") and unusable not in ("chance 0 or 1", "candidate not matched"):
                            counts["538 rule disagrees"] += 1
                            rule_bad.append((c["id"], f.get("version"), f["p_relative_error"], unusable))
                    else:
                        counts["538 unusable"] += 1
                if p["under"].startswith("538"):
                    counts["538 first"] += 1
                blocks = [p] + (p.get("alongside") or [])
                for b in blocks:
                    counts["blocks"] += 1
                    f = c["forecasts"][b["of_forecast"]]
                    mean, sd, tails = f["share"]["mean"], f["share"]["sd"], f["share"]["tails"]
                    fh = L.f_half(mean, sd, tails)
                    pu = L.p_density(n, fh)
                    cal = f.get("calibration")
                    cid = f"{c['id']} [{f['by']}{' ' + str(f.get('version')) if f.get('version') else ''} {tails}]"
                    T["f_half"].add(cid, b["f_half"], fh)
                    if f["by"] == "538":
                        counts["538 blocks"] += 1
                        T["value_uncal"].add(cid, b["value"], pu)
                        T["value"].add(cid, b["value"], pu)
                    else:
                        counts["own blocks"] += 1
                        if b is p and tails == "t4":
                            counts["t4 first"] += 1
                        if cal:
                            counts["calibrated"] += 1
                            F = cal["factor"]
                            mult = F / (1 + (F - 1) * near_q(mean, sd, tails))
                            T["multiplier"].add(cid, cal["multiplier"], mult)
                            T["value_uncal"].add(cid, b["value_uncalibrated"], pu)
                            T["value"].add(cid, b["value"], pu * mult)
                        else:
                            if "value_uncalibrated" in b:
                                T["value_uncal"].add(cid, b["value_uncalibrated"], pu)
                            T["value"].add(cid, b["value"], pu)
                        # 8.3 whose factor
                        F_block, scheme = band_factor(m, mean)
                        if cal:
                            T["factor"].add(cid, cal["factor"], F_block if F_block is not None else float("nan"),
                                            label=f"scheme {scheme} vs recorded {cal.get('scheme')}")
                        elif F_block is not None and F_block != 1.0:
                            T["factor"].add(cid, 1.0, F_block, label="forecast carries no calibration but the block gives a factor")
                        else:
                            counts["no factor (band 0.10 up or none)"] += 1
                        # 8.2 the forecast's mean and sd from the inputs
                        if m and fi:
                            P = 1 if fi["president_party"] == "D" else -1
                            M = 1 if fi["midterm"] else 0
                            z = np.array([1.0, M * P, (1 - M) * P])
                            nat = float(z @ np.array(m["c"]))
                            raw = 0.5 + nat + m["b_lean"] * fi["lean"] + m["b_inc"] * fi["incumbency"]
                            if m.get("b_lag") is not None:
                                raw += m["b_lag"] * (fi["last_governor_race"]["share_D"] - 0.5)
                            mu = 0.5 + lam * (raw - 0.5) if lam is not None else raw
                            if lam is not None:
                                counts["shrunk"] += 1
                                T["mean_unshrunk"].add(cid, f["share"].get("mean_unshrunk"), raw)
                            T["mean"].add(cid, mean, mu)
                            T["sd"].add(cid, sd, m["sd"])
                    T["event"].add(cid, b["event"], 2 * b["value"])
                    if b.get("control"):
                        T["ctl_value"].add(cid, b["control"]["value"], b["value"] * b["control"]["P_decides_given_tie"])
                # 8.5 stage two inputs
                st2 = c.get("stage_two") or {}
                inp = st2.get("inputs") or {}
                if inp.get("entered_as") == "model" and ch:
                    counts["st2 model"] += 1
                    f = c["forecasts"][p["of_forecast"]]
                    s_a, s_e = ch["common_swing_sd"], ch["own_sd"]
                    T["st2_mean"].add(c["id"], inp["mean"], f["share"]["mean"])
                    if f["by"] == "538":
                        sd538 = f["share"]["sd"]
                        if sd538 > s_a * (1 + 1e-9):
                            own, lamb = math.sqrt(sd538 ** 2 - s_a ** 2), 1.0
                        else:
                            counts["st2 marked"] += 1
                            rho = s_a ** 2 / (s_a ** 2 + s_e ** 2)
                            own, lamb = sd538 * math.sqrt(1 - rho), sd538 * math.sqrt(rho) / s_a
                            if not inp.get("marginal_note"):
                                print(f"       {c['id']}: sd538 {sd538:.5f} <= s_a {s_a:.5f} but no marginal_note")
                    else:
                        own, lamb = s_e, 1.0
                    T["st2_own_sd"].add(c["id"], inp["own_sd"], own)
                    T["st2_lam"].add(c["id"], inp["swing_loading"], lamb)
        print("  counts:", ", ".join(f"{k} {v}" for k, v in counts.items()))
        print("  8.1 p from the forecast's mean, sd, tails and the near-tie factor (every block of p and p.alongside):")
        for k in ("f_half", "value_uncal", "multiplier", "value", "event", "ctl_value"):
            T[k].report({"f_half": "f(1/2)", "value_uncal": "value_uncalibrated (or value where no factor) = f(1/2)/(2n)",
                         "multiplier": "multiplier = F / (1 + (F - 1) q)", "value": "value (= value_uncalibrated x multiplier)",
                         "event": "event = 2 value", "ctl_value": "control value = value x P(decides | tie)"}[k])
        print("  8.2 the forecast rebuilt from the model block and forecast_inputs (mean_is, sd_is):")
        for k in ("nat_fc", "nat_sd", "s_e", "model_sd", "rho", "mean_unshrunk", "mean", "sd"):
            T[k].report({"nat_fc": "national_forecast = c . z", "nat_sd": "national_sd = k s_a sqrt(1 + z (Z'Z)^-1 z') (and chamber.common_swing_sd)",
                         "s_e": "s_e = k s_e_fitted (and chamber.own_sd)", "model_sd": "sd = sqrt(national_sd^2 + s_e^2)",
                         "rho": "rho = national_sd^2 / sd^2", "mean_unshrunk": "mean_unshrunk = 1/2 + national_forecast + b_lean lean + b_inc inc [+ b_lag (lag - 1/2)]",
                         "mean": "mean (shrunk by the variant's lambda where it shrinks)", "sd": "the forecast's sd = the model's sd"}[k])
        print("  8.3 whose near-tie factor each forecast carries (the model block's level factor or band factor):")
        T["factor"].report("factor")
        print("  8.4 538's entries: implied sd = (mean - 1/2) / Phi^-1(chance); p's error = sd's error x |z^2 - 1| (the 20% rule of #33):")
        T["sd538"].report("implied sd")
        T["p_rel"].report("p_relative_error (tolerance 5%: the sd's error here is the chance's sampling error over the run count alone)")
        print(f"    the 20% rule: {counts['538 rule disagrees']} entries where (p_relative_error >= 0.20) disagrees with unusable_kind")
        for r in rule_bad[:8]:
            print("       ", r)
        print("  8.5 stage_two.inputs from the forecast p stands under (REPORT 4):")
        for k in ("st2_mean", "st2_own_sd", "st2_lam"):
            T[k].report({"st2_mean": "mean", "st2_own_sd": "own_sd", "st2_lam": "swing_loading"}[k])
        grand[level] = (counts, {k: (t.worst[0], len(t.bad)) for k, t in T.items()})
    print("\n== summary")
    for level, (counts, ws) in grand.items():
        worst = max(v[0] for v in ws.values())
        nbad = sum(v[1] for k, v in ws.items() if k != "p_rel")
        print(f"  {level}: {counts['p>0']} contests with p > 0, {counts['blocks']} blocks; largest relative difference over every "
              f"comparison but p_rel {worst:.2e}; {nbad} comparisons beyond tolerance")


if __name__ == "__main__":
    main()
