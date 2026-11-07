"""C9 (second pass, item 1). The model's own forecast refitted by M2's own code (m2fit.py) from the sources, year by
year on earlier cycles only, against every file's model block (data/<level>/<year>.json) and backtest.json:
  9.1 the rows: counts by level, year and source against D2's; the inputs against the files' forecast_inputs;
  9.2 each year's fit: b_lean, b_inc, b_lag, s_e_fitted, s_a, c, (Z'Z)^-1, national_forecast, national_sd; the
      House of 2008-2012 on the Senate's national terms;
  9.3 k, the calibration factor: the RMS of z over the earlier years' raw out-of-sample forecasts (CAL_MIN 3), and
      k refitted on the shrunk means where the variant shrinks (model.k, calibration.years and races);
  9.4 lambda, the shrinkage factor: the 1/sd^2-weighted slope through 1/2 (variant.shrink.factor, years, races);
  9.5 F, the near-tie factor of record: one factor per level (the Senate) or by band (the House), own if the fitting
      years expect 30 or more near-ties, else pooled over levels, else none: factor, expected, seen, fitted_on;
  9.6 the model's own mean and sd of every contest, from the refit, against the file's (the fit rows' means).
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402
import m2fit as F  # noqa: E402

RECORD_VARIANT = {"house": "none", "senate": "none", "governor": "none"}   # after #51: round 5 withdrawn, every level D2-v3
RECORD_SCHEME = {"house": "level", "senate": "level", "governor": None}


def rel(a, b):
    if a is None or b is None:
        return float("nan")
    return abs(b / a - 1.0) if a != 0 else abs(b - a)


def main():
    print("C9. THE FITS REDONE: ROWS, COEFFICIENTS, k, lambda AND F AGAINST THE FILES' MODEL BLOCKS")
    print(f"repository HEAD {L.git_head()}")
    for url, name, sha in (F.CHA, F.MEDSL):
        path, h = L.fetch(url, name, sha)
        print(f"  {name}: sha256 {h} [measured; matches the one recorded in m2fit.py]")
    d = F.all_rows()
    rows = d["rows"]
    b = L.load_json(os.path.join(L.DATA, "congress", "backtest.json"))
    print("\n9.1 THE ROWS")
    print(f"  rows {len(rows)} (D2's backtest.json: {b['rows']}); skipped: {d['skipped']}")
    print(f"  D2's skipped: {b['skipped']}")
    ic = d["incumbency_check"]
    print(f"  the inferred-incumbency check on MEDSL's regular Senate races of 2006-2024 against Cha: {ic['races']} races, "
          f"{ic['agree']} agree ({ic['agree'] / ic['races']:.1%}); differ: {ic['differ']}")
    print(f"  D2's: {b['incumbency_check']['races']} races, {b['incumbency_check']['agree']} agree; differ: {b['incumbency_check']['differ']}")
    by = {}
    for r in rows:
        by.setdefault((r["level"], r["year"]), []).append(r)
    for level in F.LEVELS:
        print(f"  {level} rows by year: " + ", ".join(f"{y} {len(by[(level, y)])}" for (l_, y) in sorted(by) if l_ == level))
    # the inputs against the files
    for level in F.LEVELS:
        rs = [r for r in rows if r["level"] == level and r.get("id")]
        dl = [r for r in rs if r.get("file_lean") is not None and abs(r["file_lean"] - r["lean"]) > 2e-6]
        di = [r for r in rs if r.get("file_inc") is not None and r["file_inc"] != r["inc"]]
        dg = [r for r in rs if level == "governor" and r.get("file_lag") is not None and r.get("lag") is not None and abs(r["file_lag"] - r["lag"]) > 1e-9]
        print(f"  {level}: {len(rs)} rows matched to a file contest; lean differs from forecast_inputs in {len(dl)} "
              f"({', '.join(f'{r['id']} {r['lean']:.6f} vs {r['file_lean']:.6f}' for r in dl[:3])}); incumbency differs in {len(di)} "
              f"({', '.join(f'{r['id']} Cha {r['inc']:+d} vs file {r['file_inc']:+d}' for r in di)}); last race differs in {len(dg)}")

    print("\n9.2 EACH YEAR'S FIT AGAINST THE FILE'S MODEL BLOCK (relative differences; the House of 2008-2012 on the Senate's terms)")
    print(f"  {'level year':16s} {'cycles':>6s} {'races':>11s} {'b_lean':>9s} {'b_inc':>9s} {'b_lag':>9s} {'s_e_fit':>9s} {'s_a':>9s} {'c (max)':>9s} {'ZtZ (max)':>9s} {'nat fc':>9s} {'nat sd':>9s} {'k':>9s} {'lambda':>9s}")
    worst = {}
    for level in F.LEVELS:
        for path in sorted(os.listdir(os.path.join(L.DATA, level))):
            doc = L.load_json(os.path.join(L.DATA, level, path))
            year, m = doc["year"], doc.get("model") or {}
            if "c" not in m:
                continue
            variant = RECORD_VARIANT[level]
            mm, fy = F.variant_model(rows, level, year, variant)
            if mm is None:
                print(f"  {level} {year}: no fit here ({len(fy)} earlier cycles) but the file has one")
                continue
            nat, nat_sd = F.national(mm, year)
            lam_rec = (m.get("variant") or {}).get("shrink")
            lam_rec = lam_rec["factor"] if lam_rec else None
            lam = mm["shrink"]["factor"] if mm.get("shrink") else None
            diffs = {"b_lean": rel(m["b_lean"], mm["b_lean"]), "b_inc": rel(m["b_inc"], mm["b_inc"]),
                     "b_lag": rel(m["b_lag"], mm["b_lag"]) if m.get("b_lag") is not None else float("nan"),
                     "s_e_fit": rel(m["s_e_fitted"], mm["s_e"]), "s_a": rel(m["s_a"], mm["s_a"]),
                     "c": max(abs(x - y) for x, y in zip(m["c"], mm["c"])),
                     "ZtZ": max(abs(x - y) for rx, ry in zip(m["ZtZ_inv"], mm["ZtZ_inv"]) for x, y in zip(rx, ry)),
                     "nat_fc": abs(m["national_forecast"] - nat), "nat_sd": rel(m["national_sd"], nat_sd),
                     "k": rel(m["k"], mm["k"]), "lambda": rel(lam_rec, lam) if lam_rec is not None else (0.0 if lam is None else float("nan"))}
            races_ok = m["races"] == mm["n"]
            fy_ok = m["fit_years"] == mm["years"] and (m.get("calibration") or {}).get("years") == mm["calibration"]["years"]
            print(f"  {level + ' ' + str(year):16s} {len(mm['years']):>6d} {str(m['races']) + '/' + str(mm['n']):>11s} "
                  + " ".join(f"{diffs[k]:9.1e}" if diffs[k] == diffs[k] else f"{'-':>9s}" for k in ("b_lean", "b_inc", "b_lag", "s_e_fit", "s_a", "c", "ZtZ", "nat_fc", "nat_sd", "k", "lambda"))
                  + ("" if races_ok else "  RACES DIFFER") + ("" if fy_ok else "  YEARS DIFFER")
                  + ("  (Senate's terms)" if mm.get("national_from") else ""))
            for k, v in diffs.items():
                if v == v and v > worst.get((level, k), (0, None))[0]:
                    worst[(level, k)] = (v, year)
    for level in F.LEVELS:
        print(f"  {level}, largest over the years: " + ", ".join(f"{k} {v:.1e} ({y})" for (l_, k), (v, y) in sorted(worst.items()) if l_ == level))
    print("  (the House specials here take the files' lines convention, m2fit.SPECIAL_LINES 't-2': a special's district presidential vote")
    print("   on the lines of t-2, the lines it was held on; D2's fit rows read it so since #51, having taken the sheet of its own year before)")

    print("\n9.2b THE HOUSE AGAIN WITH THE SPECIALS ON THE SHEET OF THEIR OWN YEAR (D2's rows before #51): the same relative differences")
    moved = F.set_special_lines(rows, "own")
    sp = [r for r in rows if r["level"] == "house" and r["special"] and r.get("lean_own") is not None and abs(r["lean_own"] - r["lean_t2"]) > 1e-4]
    print(f"  {moved} special rows move; {len(sp)} by more than 1e-4: " + ", ".join(f"{r['id'][:-8]} {r['lean_t2']:+.3f} (file, and D2's rows since #51) vs {r['lean_own']:+.3f} (D2's rows before #51)" for r in sp))
    for path in sorted(os.listdir(os.path.join(L.DATA, "house"))):
        doc = L.load_json(os.path.join(L.DATA, "house", path))
        year, m = doc["year"], doc.get("model") or {}
        if "c" not in m or m.get("national_from"):
            continue
        mm, fy = F.variant_model(rows, "house", year, RECORD_VARIANT["house"])
        nat, nat_sd = F.national(mm, year)
        lam_rec = (m.get("variant") or {}).get("shrink")
        lam_rec = lam_rec["factor"] if lam_rec else None
        lam = mm["shrink"]["factor"] if mm.get("shrink") else None
        print(f"  house {year}: b_lean {rel(m['b_lean'], mm['b_lean']):.1e} b_inc {rel(m['b_inc'], mm['b_inc']):.1e} s_e_fit {rel(m['s_e_fitted'], mm['s_e']):.1e} "
              f"s_a {rel(m['s_a'], mm['s_a']):.1e} nat sd {rel(m['national_sd'], nat_sd):.1e} k {rel(m['k'], mm['k']):.1e} lambda {rel(lam_rec, lam) if lam_rec and lam else float('nan'):.1e}")
    F.set_special_lines(rows, "t-2")

    print("\n9.3-9.4 k AND lambda BY YEAR AGAINST backtest.json (variants.k_by_year, shrink_by_year), every level, 2010-2024")
    vt = b["variants"]
    for level in F.LEVELS:
        line = []
        for T in F.VARIANT_YEARS:
            kr = vt["k_by_year"][level][str(T)]
            sr = vt["shrink_by_year"][level][str(T)]
            sh = F.shrink_factor(rows, level, T)
            k0 = F.calibration(rows, level, T)["k"]
            k1 = F.calibration(rows, level, T, sh)["k"]
            lam = sh["factor"] if sh else None
            lr = sr["factor"] if sr else None
            line.append(f"{T}: k {k0:.4f}/{kr['none']:.4f} k' {k1:.4f}/{kr['shrunk']:.4f} lam {lam if lam is None else round(lam, 4)}/{lr if lr is None else round(lr, 4)}")
        print(f"  {level} (mine/D2's): " + "; ".join(line))

    print("\n9.5 THE NEAR-TIE FACTOR OF RECORD, EVERY YEAR WITH ONE, AGAINST THE FILE'S model.near_tie")
    print("  (own factor where the level's fitting years expect 30 or more near-ties, else pooled, else none; F solves sum F q/(1+(F-1)q) = seen)")
    for level in F.LEVELS:
        sch = RECORD_SCHEME[level]
        if not sch:
            print(f"  {level}: no scheme of record (none adopted); the file says: " + str(L.load_json(os.path.join(L.DATA, level, "2024.json"))["model"]["near_tie"].get("note"))[:90])
            continue
        for path in sorted(os.listdir(os.path.join(L.DATA, level))):
            doc = L.load_json(os.path.join(L.DATA, level, path))
            year, m = doc["year"], doc.get("model") or {}
            nt = m.get("near_tie") or {}
            if not nt.get("scheme"):
                continue
            variant = RECORD_VARIANT[level]
            if sch == "level":
                mine = F.near_tie_factor(rows, level, year, 0.5, "level", variant)
                recs = [(nt.get("factor", 1.0), nt.get("expected"), nt.get("seen"), nt.get("fitted_on") or {}, nt.get("of"))]
                mines = [mine]
            else:
                recs = [(x["factor"], x["expected"], x["seen"], x.get("fitted_on") or {}, x.get("of")) for x in nt["by_band"]]
                mines = [F.near_tie_factor(rows, level, year, 0.5 + bf + 1e-9, "band", variant) for bf in F.NEAR_BANDS]
            parts = []
            for (fr, er, sr, fo, of), mi in zip(recs, mines):
                fo_ok = {k: v for k, v in fo.items()} == {k: v for k, v in mi["fitted_on"].items()}
                parts.append(f"F {fr:.4f}/{mi['factor']:.4f} exp {er if er is None else round(er, 2)}/{mi['expected'] if mi['expected'] is None else round(mi['expected'], 2)} "
                             f"seen {sr}/{mi['seen']}" + ("" if fo_ok else " FITTED-ON YEARS DIFFER") + (f" [{(of or 'none')[:12]}]"))
            print(f"  {level} {year}: " + " | ".join(parts))

    print("\n9.6 EVERY CONTEST'S OWN FORECAST FROM THE REFIT (the fit rows): mean and sd against the file's")
    for level in F.LEVELS:
        n, wm, ws, ex = 0, 0.0, 0.0, None
        for path in sorted(os.listdir(os.path.join(L.DATA, level))):
            doc = L.load_json(os.path.join(L.DATA, level, path))
            year, m = doc["year"], doc.get("model") or {}
            if "c" not in m:
                continue
            mm, _ = F.variant_model(rows, level, year, RECORD_VARIANT[level])
            if mm is None:
                continue
            byid = {c["id"]: c for c in doc["contests"]}
            for r in F.test_rows(rows, level, year):
                c = byid.get(r.get("id"))
                if not c:
                    continue
                own = next((f for f in c["forecasts"] if f["by"] == "the model's own"), None)
                if not own:
                    continue
                mu, sd, _ = F.predict(mm, r)
                dm, ds = abs(mu - own["share"]["mean"]), rel(own["share"]["sd"], sd)
                n += 1
                if dm > wm:
                    wm, ex = dm, (c["id"], own["share"]["mean"], mu, r["inc"], (c.get("forecast_inputs") or {}).get("incumbency"))
                ws = max(ws, ds)
        print(f"  {level}: {n} contests; largest |mean difference| {wm:.2e} ({ex}); largest relative sd difference {ws:.1e}")
        print(f"     (a mean difference beyond 1e-6 is an input that differs from the file's: the incumbency cases of 9.1, or a special's lines (9.2b))")


if __name__ == "__main__":
    main()
