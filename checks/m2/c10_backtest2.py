"""C10 (second pass, item 2). D2's adoption back-tests redone by my own implementation (m2fit): the near-tie scheme
test (REPORT 2.6; backtest.json `near_tie`), the variants test (REPORT 2.7; `variants`) and the near-tie test
refitted under each variant (`near_tie_by_variant`). Every fit, k, lambda and factor is on earlier years only by
construction (m2fit.fit_years, calibration, shrink_factor, near_tie_factor). Then the rule as written against what
was applied, and where a decision would flip: the margin of each test, and the adoption under small changes of
the rule (the minimum count, strictness, the years, one year left out, bands by the variant's own mean).
The House specials take the files' lines convention here (m2fit.SPECIAL_LINES "t-2"), D2's too since #51;
c9 shows the files' convention beside it.
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2fit as F  # noqa: E402
import m2lib as L  # noqa: E402

WIN = {0.01: "49-51%", 0.02: "48-52%", 0.05: "45-55%"}
BANDL = ["|mean - 1/2| 0.00-0.05", "|mean - 1/2| 0.05-0.10", "|mean - 1/2| 0.10-0.20", "|mean - 1/2| 0.20 up"]
NBANDL = ["|mean - 1/2| from 0.00", "|mean - 1/2| from 0.05", "|mean - 1/2| from 0.10"]


class Diff:
    def __init__(self):
        self.n, self.worst, self.bad = 0, (0.0, None), []

    def add(self, what, mine, rec, tol=1e-6):
        if mine is None or rec is None:
            if (mine is None) != (rec is None):
                self.bad.append((what, mine, rec))
            return
        d = abs(float(mine) - float(rec))
        self.n += 1
        if d > self.worst[0]:
            self.worst = (d, (what, mine, rec))
        if d > tol:
            self.bad.append((what, mine, rec))

    def report(self, label):
        w = self.worst
        print(f"    {label}: {self.n} numbers compared; largest |difference| {w[0]:.2e}" + (f" at {w[1][0]} (mine {w[1][1]:.6g}, record {w[1][2]:.6g})" if w[1] else "")
              + f"; {len(self.bad)} beyond tolerance" + (f": {self.bad[:6]}" if self.bad else ""))


def fmt_flags(r):
    return "".join("Y" if r.get(k) else "n" for k in ("raises_log_score", "count_nearer", "safe_seats_supported"))


def section_near(rows, b):
    print("\n10.1 THE NEAR-TIE SCHEME TEST UNDER none (REPORT 2.6; backtest.json near_tie): mine against D2's")
    print("  (three tests on the years a scheme reaches: raises the log score; 49-51% count nearer; the safe band (|mean - 1/2| >= 0.10) not further)")
    rec = b["near_tie"]
    nt = F.near_tie_test(rows, "none")
    D = Diff()
    print(f"  {'level':9s} {'scheme':7s} {'races':>5s} {'log score mine / D2':>22s} {'49-51% exp mine / D2 / seen':>30s} {'48-52%':>16s} {'45-55%':>16s} {'safe 49-51%':>16s} {'tests':>5s} ")
    for Lv in F.LEVELS:
        r, rr = nt["by_level"][Lv], rec["by_level"][Lv]
        D.add(f"{Lv} years", len(r["years"]), len(rr["years"]))
        for sch in ("none", "level", "band"):
            x, xx = r[sch], rr[sch]
            D.add(f"{Lv} {sch} races", x["races"], xx["races"])
            D.add(f"{Lv} {sch} log score", x["mean_log_score"], xx["mean_log_score"], 2e-6)
            for i, c in enumerate(("0.5", "0.8", "0.95")):
                D.add(f"{Lv} {sch} coverage {c}", x["coverage"][i], xx["coverage"][c], 1e-6)
            for w, lab in WIN.items():
                D.add(f"{Lv} {sch} within {lab}", x["within"][w]["expected"], xx["within"][lab]["expected"], 2e-4)
                D.add(f"{Lv} {sch} within {lab} seen", x["within"][w]["seen"], xx["within"][lab]["seen"])
            for bi, lab in enumerate(NBANDL):
                D.add(f"{Lv} {sch} band {lab}", x["by_band"][bi]["expected"], xx["within_49_51_by_band"][lab]["expected"], 2e-4)
            if sch != "none":
                for k in ("raises_log_score", "count_nearer", "safe_seats_supported", "improves", "robust"):
                    D.add(f"{Lv} {sch} {k}", int(bool(x.get(k))), int(bool(xx.get(k))))
                if "round_5_cells" in x or "round_5_cells" in xx:
                    c5, cc5 = x.get("round_5_cells") or {}, xx.get("round_5_cells") or {}
                    D.add(f"{Lv} {sch} round 5 cells improves", int(bool(c5.get("improves"))), int(bool(cc5.get("improves"))))
                    D.add(f"{Lv} {sch} round 5 cells tested", len(c5.get("safe_bands_tested") or []), len(cc5.get("safe_bands_tested") or []))
                    D.add(f"{Lv} {sch} round 5 cells further", len(c5.get("safe_bands_further") or []), len(cc5.get("safe_bands_further") or []))
                    lo, llo = x.get("leave_one_year_out") or {}, xx.get("leave_one_year_out") or {}
                    for y in sorted(set(lo) | set(int(t) for t in llo)):
                        a, bb = lo.get(y) or {}, llo.get(str(y)) or {}
                        D.add(f"{Lv} {sch} without {y} improves", int(bool(a.get("improves"))), int(bool(bb.get("improves"))))
                        D.add(f"{Lv} {sch} without {y} fails", len(a.get("fails") or []), len(bb.get("fails") or []))
                        if a.get("mean_log_score_gain") is not None and bb.get("mean_log_score_gain") is not None:
                            D.add(f"{Lv} {sch} without {y} log score gain", a["mean_log_score_gain"], bb["mean_log_score_gain"], 2e-6)
            print(f"  {Lv:9s} {sch:7s} {x['races']:5d} {x['mean_log_score']:10.5f} / {xx['mean_log_score']:8.5f} "
                  f"{x['within'][0.01]['expected']:9.2f} / {xx['within']['49-51%']['expected']:6.2f} / {x['within'][0.01]['seen']:3d}   "
                  f"{x['within'][0.02]['expected']:6.1f} / {xx['within']['48-52%']['expected']:6.1f}  {x['within'][0.05]['expected']:6.1f} / {xx['within']['45-55%']['expected']:6.1f}  "
                  f"{x['by_band'][2]['expected']:5.1f} / {xx['within_49_51_by_band'][NBANDL[2]]['expected']:5.1f} vs {x['by_band'][2]['seen']:2d}   "
                  + (f"{fmt_flags(x)} / {fmt_flags(xx)}" if sch != "none" else ""))
        for sch in ("level", "band"):
            x, xx = r[sch], rr[sch]
            if "round_5_cells" not in x and "round_5_cells" not in xx:
                continue
            c5, cc5 = x.get("round_5_cells") or {}, xx.get("round_5_cells") or {}
            lo, llo = x.get("leave_one_year_out") or {}, xx.get("leave_one_year_out") or {}
            print(f"  {Lv:9s} {sch:6s} round 5's cells: tested {len(c5.get('safe_bands_tested') or [])} / {len(cc5.get('safe_bands_tested') or [])}, "
                  f"further {len(c5.get('safe_bands_further') or [])} / {len(cc5.get('safe_bands_further') or [])}; fails without "
                  f"{[y for y in sorted(lo) if not lo[y]['improves']] or 'no year'} / {[int(y) for y in sorted(llo) if not llo[y]['improves']] or 'no year'}; "
                  f"robust {bool(x.get('robust'))} / {bool(xx.get('robust'))}")
        print(f"  {Lv:9s} adopted: mine {r['adopted']!r}, D2 {rr['adopted']!r}")
        D.add(f"{Lv} adopted", {None: 0, "level": 1, "band": 2}[r["adopted"]], {None: 0, "level": 1, "band": 2}[rr["adopted"]])
    print("  (the rule since D2's #53 (09:10; REPORT 0.2): a scheme is adopted only if it passes round 4's three tests, round 5's cells on the safe")
    print("   bands (10-20 and 20+ points; 49-51, 48-52 and 45-55%, where seen or expected is 5 or more), and both with any one scored year left out)")
    D.report("the near-tie test's cells")
    # the factors of every year
    D2 = Diff()
    print("  the factors by year (one factor | by band), mine / D2's; 'of': own = the level's own earlier years, pooled = every level's, - = none")
    for Lv in F.LEVELS:
        r, rr = nt["by_level"][Lv], rec["by_level"][Lv]
        line = []
        for T in sorted(int(t) for t in rr["factors_by_year"]):
            m = r["factors_by_year"].get(T) or r["factors_by_year"].get(str(T))
            x = rr["factors_by_year"][str(T)]
            D2.add(f"{Lv} {T} level F", m["level"]["factor"], x["level"]["factor"], 1e-4)
            D2.add(f"{Lv} {T} level seen", m["level"]["seen"], x["level"]["seen"])
            D2.add(f"{Lv} {T} level expected", m["level"]["expected"], x["level"]["expected"], 1e-3)
            for bi in range(3):
                D2.add(f"{Lv} {T} band{bi} F", m["band"][bi]["factor"], x["band"][bi]["factor"], 1e-4)
                D2.add(f"{Lv} {T} band{bi} seen", m["band"][bi]["seen"], x["band"][bi]["seen"])

            def of(e):
                return "-" if not e.get("of") else ("own" if "own" in str(e["of"]) else "pooled")
            line.append(f"{T}: {m['level']['factor']:.4f}/{x['level']['factor']:.4f} {of(m['level'])}/{of(x['level'])} | "
                        + " ".join(f"{m['band'][bi]['factor']:.3f}/{x['band'][bi]['factor']:.3f}" for bi in range(3)))
        print(f"    {Lv}: " + "; ".join(line))
    D2.report("the factors and their fitting counts")
    return nt


def section_variants(rows, b):
    print("\n10.2 THE VARIANTS TEST (REPORT 2.7; backtest.json variants): mine against D2's, 2010-2024")
    print("  (three tests against none: raises the log score; 49-51% nearer; in the safe bands 0.10-0.20 and 0.20 up no tested count further; tested where seen or none's expected >= 5)")
    rec = b["variants"]
    vt = F.variant_test(rows)
    D = Diff()
    print(f"  {'level':9s} {'variant':7s} {'near-tie':8s} {'races':>5s} {'log score mine / D2':>22s} {'49-51% mine / D2 / seen':>28s} {'48-52%':>15s} {'45-55%':>15s} {'tests':>7s} {'tested, further (mine / D2)'}")
    for Lv in F.LEVELS:
        r, rr = vt["by_level"][Lv], rec["by_level"][Lv]
        for v in ("none", "shrink", "t4", "both"):
            x, xx = r[v], rr[v]
            D.add(f"{Lv} {v} races", x["races"], xx["races"])
            D.add(f"{Lv} {v} log score", x["mean_log_score"], xx["mean_log_score"], 2e-6)
            D.add(f"{Lv} {v} near-tie scheme", {None: 0, "level": 1, "band": 2}[x["near_tie"]], {None: 0, "level": 1, "band": 2}[xx["near_tie"]])
            for i, c in enumerate(("0.5", "0.8", "0.95")):
                D.add(f"{Lv} {v} coverage {c}", x["coverage"][i], xx["coverage"][c], 1e-6)
            for w, lab in WIN.items():
                D.add(f"{Lv} {v} within {lab}", x["within"][w]["expected"], xx["within"][lab]["expected"], 2e-4)
                D.add(f"{Lv} {v} within {lab} seen", x["within"][w]["seen"], xx["within"][lab]["seen"])
            for bi, lab in enumerate(BANDL):
                g, gg = x["by_band"][bi], xx["by_band"][lab]
                D.add(f"{Lv} {v} {lab} races", g["races"], gg["races"])
                D.add(f"{Lv} {v} {lab} log score", g["mean_log_score"], gg["mean_log_score"], 2e-6)
                for w, wl in WIN.items():
                    D.add(f"{Lv} {v} {lab} {wl}", g["within"][w]["expected"], gg["within"][wl]["expected"], 2e-4)
                    D.add(f"{Lv} {v} {lab} {wl} seen", g["within"][w]["seen"], gg["within"][wl]["seen"])
                for t_, tl in ((0.05, "5%"), (0.01, "1%")):
                    D.add(f"{Lv} {v} {lab} beyond {tl}", g["tail"][t_]["expected"], gg["beyond_quantile_toward_half"][tl]["expected"], 1e-6)
                    D.add(f"{Lv} {v} {lab} beyond {tl} seen", g["tail"][t_]["seen"], gg["beyond_quantile_toward_half"][tl]["seen"])
            if v != "none":
                for k in ("raises_log_score", "count_nearer", "safe_seats_supported", "improves"):
                    D.add(f"{Lv} {v} {k}", int(bool(x.get(k))), int(bool(xx.get(k))))
                mine_t = [f"{BANDL[bb]}, {WIN[w]}" for bb, w in x["safe_bands_tested"]]
                mine_f = [f"{BANDL[bb]}, {WIN[w]}" for bb, w in x["safe_bands_further"]]
                D.add(f"{Lv} {v} tested cells", len(mine_t), len(xx["safe_bands_tested"]))
                D.add(f"{Lv} {v} further cells", len(mine_f), len(xx["safe_bands_further"]))
                if sorted(mine_t) != sorted(xx["safe_bands_tested"]) or sorted(mine_f) != sorted(xx["safe_bands_further"]):
                    D.bad.append((f"{Lv} {v} tested/further cells differ", (mine_t, mine_f), (xx["safe_bands_tested"], xx["safe_bands_further"])))
            print(f"  {Lv:9s} {v:7s} {str(x['near_tie']):8s} {x['races']:5d} {x['mean_log_score']:10.5f} / {xx['mean_log_score']:8.5f} "
                  f"{x['within'][0.01]['expected']:8.2f} / {xx['within']['49-51%']['expected']:6.2f} / {x['within'][0.01]['seen']:3d}  "
                  f"{x['within'][0.02]['expected']:6.1f} / {xx['within']['48-52%']['expected']:6.1f} {x['within'][0.05]['expected']:6.1f} / {xx['within']['45-55%']['expected']:6.1f}  "
                  + (f"{fmt_flags(x)} / {fmt_flags(xx)}  {len(x['safe_bands_tested'])}, {len(x['safe_bands_further'])} / {len(xx['safe_bands_tested'])}, {len(xx['safe_bands_further'])}" if v != "none" else ""))
        rec_pass = [v for v in ("shrink", "t4", "both") if rr[v]["improves"]]
        rec_best3 = max(rec_pass, key=lambda v: rr[v]["mean_log_score"]) if rec_pass else "none"
        print(f"  {Lv:9s} adopted: mine {r['adopted']!r} (the three tests), D2 {rr['adopted']!r} (D2's adds the robustness test, 10.6; "
              f"its best under the three tests {rec_best3!r})")
        D.add(f"{Lv} adopted under the three tests", ["none", "shrink", "t4", "both"].index(r["adopted"]), ["none", "shrink", "t4", "both"].index(rec_best3))
    D.report("the variants test's cells")
    print("  the safe bands, House, expected vs seen (mine / D2), with the results beyond the 5% and 1% quantiles toward 1/2:")
    for v in ("none", "shrink", "t4", "both"):
        for bi in (2, 3):
            g, gg = vt["by_level"]["house"][v]["by_band"][bi], rec["by_level"]["house"][v]["by_band"][BANDL[bi]]
            print(f"    {BANDL[bi]:24s} {v:7s} " + "  ".join(f"{WIN[w]} {g['within'][w]['expected']:5.2f}/{gg['within'][WIN[w]]['expected']:5.2f} vs {g['within'][w]['seen']}" for w in WIN)
                  + f"  beyond 5%: {g['tail'][0.05]['seen']}/{gg['beyond_quantile_toward_half']['5%']['seen']} vs {g['tail'][0.05]['expected']:.1f}; 1%: {g['tail'][0.01]['seen']}/{gg['beyond_quantile_toward_half']['1%']['seen']} vs {g['tail'][0.01]['expected']:.1f}")
    # lambda and k by year
    D3 = Diff()
    for Lv in F.LEVELS:
        for T in F.VARIANT_YEARS:
            sh, shr = vt["shrink_by_year"][Lv][T], rec["shrink_by_year"][Lv][str(T)]
            D3.add(f"{Lv} {T} lambda", sh["factor"] if sh else None, shr["factor"] if shr else None, 1e-6)
            if sh and shr:
                D3.add(f"{Lv} {T} lambda years", len(sh["years"]), len(shr["years"]))
                D3.add(f"{Lv} {T} lambda races", sh["races"], shr["races"])
            for kk in ("none", "shrunk"):
                D3.add(f"{Lv} {T} k {kk}", vt["k_by_year"][Lv][T][kk], rec["k_by_year"][Lv][str(T)][kk], 1e-6)
    D3.report("lambda and k by year (shrink_by_year, k_by_year)")
    return vt


def section_near_by_variant(rows, b):
    print("\n10.3 THE NEAR-TIE TEST REFITTED UNDER EACH VARIANT (backtest.json near_tie_by_variant): adopted scheme and log scores, mine / D2's")
    D = Diff()
    for v in ("shrink", "t4", "both"):
        nt, rec = F.near_tie_test(rows, v), b["near_tie_by_variant"][v]
        line = []
        for Lv in F.LEVELS:
            r, rr = nt["by_level"][Lv], rec["by_level"][Lv]
            for sch in ("none", "level", "band"):
                D.add(f"{v} {Lv} {sch} log score", r[sch]["mean_log_score"], rr[sch]["mean_log_score"], 2e-6)
                D.add(f"{v} {Lv} {sch} 49-51%", r[sch]["within"][0.01]["expected"], rr[sch]["within"]["49-51%"]["expected"], 1e-4)
            D.add(f"{v} {Lv} adopted", {None: 0, "level": 1, "band": 2}[r["adopted"]], {None: 0, "level": 1, "band": 2}[rr["adopted"]])
            line.append(f"{Lv}: {r['adopted']}/{rr['adopted']} (" + ", ".join(f"{sch} {r[sch]['mean_log_score']:.5f}/{rr[sch]['mean_log_score']:.5f}" for sch in ("none", "level", "band")) + ")")
        print(f"  {v}: " + "; ".join(line))
    D.report("near_tie_by_variant")


def section_rule(b):
    print("\n10.4 THE RULE AS WRITTEN (REPORT 2.6, 2.7, 0.1) AGAINST WHAT WAS APPLIED (chambers.py near_tie_test, variant_test, as backtest.json records it)")
    print("  Written: a scheme/variant is adopted only if, on the years it reaches, it (1) raises the mean log score, (2) brings the 49-51% count")
    print("  nearer the count seen, (3) moves no safe-band count further from the count seen; of those that pass, the better log score.")
    print("  Applied (reproduced above): (1) and (2) strict (>, <); (3) 'further' strict (>), so an equal distance passes; the variants'")
    print("  safe cells are tested where the count seen or none's expected is 5 or more; bands by none's mean; the near-tie test's safe")
    print("  band is 49-51% in |mean - 1/2| >= 0.10 only. Both tests pick the best log score among those that pass.")
    # every fit on earlier years only: the fitting years recorded
    bad = []
    for Lv in F.LEVELS:
        for T, sh in b["variants"]["shrink_by_year"][Lv].items():
            if sh and any(int(y) >= int(T) for y in sh["years"]):
                bad.append((Lv, T, "lambda", sh["years"]))
        for T, x in b["near_tie"]["by_level"][Lv]["factors_by_year"].items():
            for e in [x["level"]] + x["band"]:
                for L_, ys in (e.get("fitted_on") or {}).items():
                    if any(int(y) >= int(T) for y in ys):
                        bad.append((Lv, T, "F", L_, ys))
    for Lv in F.LEVELS:
        for f in L.congress_files(Lv):
            doc = L.load_json(f)
            m = doc.get("model") or {}
            T = doc["year"]
            if m.get("fit_years") and any(int(y) >= T for y in m["fit_years"]):
                bad.append((Lv, T, "fit_years", m["fit_years"]))
            if (m.get("calibration") or {}).get("years") and any(int(y) >= T for y in m["calibration"]["years"]):
                bad.append((Lv, T, "k years", m["calibration"]["years"]))
    print(f"  every recorded fitting set (fit_years, k, lambda, F) holds earlier years only: {'yes' if not bad else 'NO: ' + str(bad[:5])} [measured over the files and backtest.json]")
    # the adoption as recorded follows the rule as reproduced
    print("  Since #51 (REPORT 0.1) a fourth condition: (4) the three hold with any one scored year left out (10.6 below).")
    for Lv in F.LEVELS:
        r = b["variants"]["by_level"][Lv]
        passing = [v for v in ("shrink", "t4", "both") if r[v]["improves"]]
        robust = [v for v in passing if r[v].get("robust")]
        best3 = max(passing, key=lambda v: r[v]["mean_log_score"]) if passing else "none"
        best = max(robust, key=lambda v: r[v]["mean_log_score"]) if robust else "none"
        print(f"  {Lv}: variants passing (1)-(3) {passing or 'none'} (best {best3!r}); passing (4) too {robust or 'none'}; the best log score among them "
              f"{best!r}; recorded adopted {r['adopted']!r} -> {'consistent' if best == r['adopted'] else 'INCONSISTENT'}")


def margins(vt, rec_adopted, title="\n10.5 WHERE A DECISION WOULD FLIP"):
    print(title)
    print("  (a) The margin of each test, each variant against none (positive = passes): log score gain; 49-51% distance none - variant;")
    print("      the smallest safe-cell margin (none's distance - the variant's; a tested cell fails where this is negative).")
    for Lv in F.LEVELS:
        r = vt["by_level"][Lv]
        b0 = r["none"]
        for v in ("shrink", "t4", "both"):
            x = r[v]
            if not x["races"]:
                continue
            dls = x["mean_log_score"] - b0["mean_log_score"]
            dcount = abs(b0["within"][0.01]["expected"] - b0["within"][0.01]["seen"]) - abs(x["within"][0.01]["expected"] - x["within"][0.01]["seen"])
            cells = []
            for bb, w in x["safe_bands_tested"]:
                g, g0 = x["by_band"][bb]["within"][w], b0["by_band"][bb]["within"][w]
                cells.append((abs(g0["expected"] - g0["seen"]) - abs(g["expected"] - g["seen"]), f"{BANDL[bb]} {WIN[w]}: none {g0['expected']:.2f}, {v} {g['expected']:.2f} vs {g['seen']} seen"))
            worst = min(cells) if cells else None
            print(f"    {Lv:9s} {v:7s} log score {dls:+.5f}; 49-51% nearer by {dcount:+.2f}; "
                  + (f"tightest safe cell {worst[0]:+.3f} ({worst[1]})" if worst else "no safe cell tested")
                  + f"; {'passes' if x['improves'] else 'fails'}")


def alternatives(rows, rec_adopted):
    print("  (b) The adoption under changes of the rule (house / senate / governor), against the record "
          + "/".join(rec_adopted[Lv] for Lv in F.LEVELS) + ":")
    runs = [("as written (min count 5, 'further' strict, 2010-2024, bands by none's mean)", {})]
    for mc in (3, 4, 6, 8, 10):
        runs.append((f"min count {mc}", {"min_count": mc}))
    runs.append(("'further' not strict (an equal distance fails)", {"strict_further": False}))
    runs.append(("bands by the variant's own mean", {"bands_by_none": False}))
    for y0 in (2012, 2014, 2016, 2018):
        runs.append((f"years {y0}-2024", {"years": list(range(y0, 2025, 2))}))
    for y in F.VARIANT_YEARS:
        runs.append((f"without {y}", {"years": [t for t in F.VARIANT_YEARS if t != y]}))
    flips = []
    for label, kw in runs:
        vt = F.variant_test(rows, with_years=False, **kw)
        ad = [vt["adopted"][Lv] for Lv in F.LEVELS]
        changed = [Lv for Lv in F.LEVELS if vt["adopted"][Lv] != rec_adopted[Lv]]
        print(f"    {label:62s} {'/'.join(ad):22s} {'<- flips: ' + ', '.join(changed) if changed else ''}")
        if changed:
            flips.append((label, changed, {Lv: (vt['adopted'][Lv], {v: fmt_flags(vt['by_level'][Lv][v]) for v in ('shrink', 't4', 'both') if vt['by_level'][Lv][v]['races']}) for Lv in changed}))
    print("  (c) The flips, with each variant's three tests (raises log score, count nearer, safe cells) under that rule:")
    for label, changed, detail in flips:
        print(f"    {label}: {detail}")
    if not flips:
        print("    none")


def near_margins(nt, rows):
    print("  (d) The near-tie scheme test under none (2.6): margins of each scheme against none, and the two schemes against each other")
    for Lv in F.LEVELS:
        r = nt["by_level"][Lv]
        b0 = r["none"]
        for sch in ("level", "band"):
            x = r[sch]
            dls = x["mean_log_score"] - b0["mean_log_score"]
            dcount = abs(b0["within"][0.01]["expected"] - b0["within"][0.01]["seen"]) - abs(x["within"][0.01]["expected"] - x["within"][0.01]["seen"])
            dsafe = abs(b0["by_band"][2]["expected"] - b0["by_band"][2]["seen"]) - abs(x["by_band"][2]["expected"] - x["by_band"][2]["seen"])
            print(f"    {Lv:9s} {sch:6s} log score {dls:+.5f}; 49-51% nearer by {dcount:+.2f}; safe band {dsafe:+.3f}; {'passes' if x['improves'] else 'fails'}")
        if r["level"]["improves"] and r["band"]["improves"]:
            print(f"    {Lv:9s} level over band in log score: {r['level']['mean_log_score'] - r['band']['mean_log_score']:+.6f}")
    # leave one year out of the near-tie test's scoring years (the factors stay as fitted): the test's own record of it
    print("  (e) The near-tie schemes with one year left out of the scoring (factors as fitted; round 4's tests and round 5's cells), by level:")
    for Lv in F.LEVELS:
        r = nt["by_level"][Lv]
        for sch in ("level", "band"):
            lo = r[sch].get("leave_one_year_out") or {}
            if not lo:
                print(f"    {Lv:9s} {sch:6s} no year reached")
                continue
            print(f"    {Lv:9s} {sch:6s} " + "; ".join(f"without {y}: {'passes' if lo[y]['improves'] else 'fails (' + ', '.join(str(f) for f in lo[y]['fails']) + ')'}"
                                                       for y in sorted(lo)))


def robustness(rows, b, nt):
    print("\n10.6 THE ROBUSTNESS TEST (the orchestrator, 08:36; REPORT 0.1; backtest.json leave_one_year_out, robust): a variant is adopted")
    print("  only if it passes the three tests on all scored years and with any one scored year left out; mine against D2's")
    rec = b["variants"]["by_level"]
    full = F.variant_test(rows, with_years=False)
    loo = {y: F.variant_test(rows, years=[t for t in F.VARIANT_YEARS if t != y], with_years=False) for y in F.VARIANT_YEARS}
    D = Diff()
    for Lv in F.LEVELS:
        robust_pass = []
        for v in ("shrink", "t4", "both"):
            r = full["by_level"][Lv][v]
            if not r["races"]:
                continue
            fails = [y for y in F.VARIANT_YEARS if not loo[y]["by_level"][Lv][v]["improves"]]
            robust = bool(r["improves"] and not fails)
            rr = rec[Lv].get(v) or {}
            rl = rr.get("leave_one_year_out") or {}
            rfails = sorted(int(y) for y, x in rl.items() if not x.get("improves"))
            D.add(f"{Lv} {v} passes on all years", int(bool(r["improves"])), int(bool(rr.get("improves"))))
            D.add(f"{Lv} {v} years failing when left out", int(fails == rfails), 1)
            D.add(f"{Lv} {v} robust", int(robust), int(bool(rr.get("robust"))))
            for y in F.VARIANT_YEARS:
                x, xx = loo[y]["by_level"][Lv][v], rl.get(str(y)) or {}
                if xx:
                    D.add(f"{Lv} {v} without {y} log score gain", x["mean_log_score"] - loo[y]["by_level"][Lv]["none"]["mean_log_score"], xx.get("mean_log_score_gain"), 2e-6)
                    D.add(f"{Lv} {v} without {y} 49-51% expected", x["within"][0.01]["expected"], (xx.get("count_49_51") or {}).get("expected"), 1e-4)
            print(f"    {Lv:9s} {v:7s} all years {fmt_flags(r)} {'passes' if r['improves'] else 'fails'}; fails without {fails or 'no year'}; robust {robust}"
                  f"   (D2: {'passes' if rr.get('improves') else 'fails'}; fails without {rfails or 'no year'}; robust {rr.get('robust')})")
            if robust:
                robust_pass.append(v)
        best = max(robust_pass, key=lambda v: full["by_level"][Lv][v]["mean_log_score"]) if robust_pass else "none"
        print(f"    {Lv:9s} adopted under the robustness test: mine {best!r}, D2 {b['variants']['adopted'][Lv]!r}")
        D.add(f"{Lv} adopted", int(best == b["variants"]["adopted"][Lv]), 1)
    D.report("the robustness test's cells")
    print("  the near-tie schemes under none, the same rule (factors as fitted; round 4's tests, round 5's cells, any one year left out): mine / D2's")
    rec_nt = b["near_tie"]["by_level"]
    for Lv in F.LEVELS:
        r, rr = nt["by_level"][Lv], rec_nt[Lv]
        for sch in ("level", "band"):
            x, xx = r[sch], rr[sch]
            lo, llo = x.get("leave_one_year_out") or {}, xx.get("leave_one_year_out") or {}
            fails = [y for y in sorted(lo) if not lo[y]["improves"]]
            rfails = [int(y) for y in sorted(llo) if not llo[y]["improves"]]
            D.add(f"{Lv} near-tie {sch} robust", int(bool(x.get("robust"))), int(bool(xx.get("robust"))))
            print(f"    {Lv:9s} {sch:6s} all years {'passes' if x['improves'] else 'fails'} / {'passes' if xx.get('improves') else 'fails'}; "
                  f"round 5's cells {'pass' if (x.get('round_5_cells') or {}).get('improves') else 'fail'} / {'pass' if (xx.get('round_5_cells') or {}).get('improves') else 'fail'}; "
                  f"fails without {fails or 'no year'} / {rfails or 'no year'}; robust {bool(x.get('robust'))} / {bool(xx.get('robust'))}")
        print(f"    {Lv:9s} adopted under the rule: mine {r['adopted']!r}, D2 {rr['adopted']!r}")
    D.report("the near-tie schemes under the robustness rule")
    print("    (D2's #53, 09:10, took the near-tie factors again under this rule; the House's level scheme stands; the Senate's level fails round 5's")
    print("     48-52% cell in the 10-20 point band and without 2012, 2014, 2020 and 2024, so the Senate carries no near-tie factor as of record)")


def main():
    print("C10. D2'S ADOPTION BACK-TESTS REDONE: THE NEAR-TIE SCHEME, THE VARIANTS, AND WHERE A DECISION WOULD FLIP")
    print(f"repository HEAD {L.git_head()}")
    b = L.load_json(os.path.join(L.DATA, "congress", "backtest.json"))
    F.SPECIAL_LINES = "t-2"
    rows = F.all_rows()["rows"]
    F.set_special_lines(rows, "t-2")
    print(f"  rows {len(rows)} (backtest.json: {b['rows'] if isinstance(b.get('rows'), int) else len(b.get('rows', []))}); the House specials on the files' lines (t-2), D2's convention since #51")
    nt = section_near(rows, b)
    vt = section_variants(rows, b)
    section_near_by_variant(rows, b)
    section_rule(b)
    rec_adopted = b["variants"]["adopted"]
    margins(vt, rec_adopted)
    alternatives(rows, rec_adopted)
    near_margins(nt, rows)
    robustness(rows, b, nt)
    print("\n  Under D2's former convention for the House specials (the sheet of the special's own year, before #51; c9 9.2b), the same decisions:")
    F.set_special_lines(rows, "own")
    vt2 = F.variant_test(rows, with_years=False)
    nt2 = F.near_tie_test(rows, "none")
    print(f"    variants adopted {'/'.join(vt2['adopted'][Lv] for Lv in F.LEVELS)}; near-tie scheme under none {'/'.join(str(nt2['adopted'][Lv]) for Lv in F.LEVELS)}; "
          f"House log scores none {vt2['by_level']['house']['none']['mean_log_score']:.5f}, shrink {vt2['by_level']['house']['shrink']['mean_log_score']:.5f}")
    for Lv in F.LEVELS:
        r = vt2["by_level"][Lv]
        print(f"    {Lv}: " + "; ".join(f"{v} {fmt_flags(r[v])} further {[f'{BANDL[bb]} {WIN[w]}' for bb, w in r[v]['safe_bands_further']]}" for v in ("shrink", "t4", "both") if r[v]["races"]))
    margins(vt2, rec_adopted, title="  the margins under the former convention (as 10.5 (a)):")
    F.set_special_lines(rows, "t-2")


if __name__ == "__main__":
    main()
