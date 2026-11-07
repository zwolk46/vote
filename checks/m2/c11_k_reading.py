"""C11 (second pass, item 3). The spread factor k: a reading, choosing nothing. D2 (REPORT 7) finds the House's
forecast sd wider than its results in every year 2010-2024 after shrinkage (z rms 0.75-0.92) and suspects k, the
RMS of z over every earlier scored year, lags errors that have shrunk. Here, under each level's variant of record:
  11.1 the out-of-sample z rms by year, k of record, and the k that would have given z rms 1 that year;
  11.2 alternatives fitted on earlier years only (k over the last 1, 2 or 3 scored cycles; a line through the
       years' z rms read at the forecast year): z rms by year, log score, coverage and the near-even counts with
       the near-tie factor refitted under each; D2's three tests of 2.7 applied against the record;
  11.3 what each would do to p: the density at 1/2 with its refitted factor against the record's, by year and by
       band of |mean - 1/2|, and the sum over the scored races (the expected number of exact ties).
"""
import os
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2fit as F  # noqa: E402
import m2lib as L  # noqa: E402

RECORD = {"house": "none", "senate": "none", "governor": "none"}   # after #51: round 5 withdrawn, every level D2-v3
RECORD_SCHEME = {"house": "level", "senate": None, "governor": None}   # after #53: the Senate's factor out under the robustness test
WIN = {0.01: "49-51%", 0.02: "48-52%", 0.05: "45-55%"}
BANDL = ["0.00-0.05", "0.05-0.10", "0.10-0.20", "0.20 up"]


def vname(level, kmode):
    return RECORD[level] if kmode == "all" else f"{RECORD[level]}|{kmode}"


def density_half(a, F_, tails):
    """The forecast density at 1/2 with the near-tie factor: f(1/2) F / Z (the p of the files is this over 2n)."""
    mu, sd = a["mu"], a["sd"]
    f = stats.norm.pdf(0.5, mu, sd) if tails == "normal" else stats.t.pdf(0.5, 4, mu, sd / F.SQRT2)
    return f * F_ / (1 + (F_ - 1) * a["q1"])


def three_tests(ref, alt, min_count=F.VARIANT_MIN_COUNT):
    """D2's three tests of 2.7, the alternative against a reference scored the same way."""
    better = alt["mean_log_score"] > ref["mean_log_score"]
    nearer = abs(alt["within"][0.01]["expected"] - alt["within"][0.01]["seen"]) < abs(ref["within"][0.01]["expected"] - ref["within"][0.01]["seen"])
    further = []
    for b in F.VARIANT_SAFE:
        for w, x0 in ref["by_band"][b]["within"].items():
            if x0["seen"] < min_count and x0["expected"] < min_count:
                continue
            x = alt["by_band"][b]["within"][w]
            if abs(x["expected"] - x["seen"]) > abs(x0["expected"] - x0["seen"]):
                further.append(f"{BANDL[b]} {WIN[w]}")
    return better, nearer, further


def main():
    print("C11. THE SPREAD FACTOR k: A READING (chosen: nothing)")
    print(f"repository HEAD {L.git_head()}")
    rows = F.all_rows()["rows"]
    F.set_special_lines(rows, "t-2")
    years = F.VARIANT_YEARS
    for Lv in F.LEVELS:
        rec = RECORD[Lv]
        tails = F.VARIANTS[rec][1]
        print(f"\n== {Lv} (variant of record: {rec}, near-tie scheme {RECORD_SCHEME[Lv]})")
        print("11.1 OUT-OF-SAMPLE z = (result - mean)/sd BY YEAR UNDER THE RECORD: rms over the year's races, k of record, and k x rms (the k that would have given rms 1)")
        sc = F.near_scored(rows, rec)
        line = []
        for T in years:
            a = sc.get((Lv, T))
            if a is None:
                continue
            m, _ = F.variant_model(rows, Lv, T, rec)
            z = (a["y"] - a["mu"]) / a["sd"]
            near = np.abs(a["mu"] - 0.5) < 0.05
            line.append(f"{T}: rms {np.sqrt((z ** 2).mean()):.3f} (within 5 pt of even {np.sqrt((z[near] ** 2).mean()) if near.any() else float('nan'):.2f}, n {len(z)}) k {m['k']:.3f} -> {m['k'] * np.sqrt((z ** 2).mean()):.3f}")
        print("  " + "; ".join(line))
        allz = np.concatenate([(sc[(Lv, T)]["y"] - sc[(Lv, T)]["mu"]) / sc[(Lv, T)]["sd"] for T in years if (Lv, T) in sc])
        print(f"  all {len(allz)} races 2010-2024: z rms {np.sqrt((allz ** 2).mean()):.3f}; |z| > 1.96 in {(np.abs(allz) > 1.96).mean():.1%} (5% if the sd were right); mean z {allz.mean():+.3f}")

        print("11.2 ALTERNATIVES FITTED ON EARLIER YEARS ONLY: k by year, z rms by year, the score 2010-2024 with the near-tie factor refitted under each")
        ref = None
        scores = {}
        for kmode in F.K_MODES:
            v = vname(Lv, kmode)
            nt = F.near_tie_test(rows, v)
            sch = nt["adopted"].get(Lv)
            s = F.variant_score(rows, Lv, v, years, sch=sch)
            scores[kmode] = (s, sch)
            ks, zs = [], []
            for T in years:
                a = F.near_scored(rows, v).get((Lv, T))
                if a is None:
                    continue
                m, _ = F.variant_model(rows, Lv, T, v)
                z = (a["y"] - a["mu"]) / a["sd"]
                ks.append(f"{m['k']:.3f}")
                zs.append(f"{np.sqrt((z ** 2).mean()):.2f}")
            if kmode == "all":
                ref = s
                tests = ""
            else:
                better, nearer, further = three_tests(ref, s)
                tests = f"  vs the record: log score {'up' if better else 'DOWN'}, 49-51% {'nearer' if nearer else 'NOT nearer'}, safe cells further: {further or 'none'} -> {'passes' if better and nearer and not further else 'fails'}"
            print(f"  k {kmode:6s} scheme {str(sch):5s} k by year {' '.join(ks)} | z rms {' '.join(zs)} | log score {s['mean_log_score']:.5f} z rms {s['z_rms']:.3f} "
                  f"cov {s['coverage'][0]:.3f}/{s['coverage'][1]:.3f}/{s['coverage'][2]:.3f} 49-51% {s['within'][0.01]['expected']:.1f} vs {s['within'][0.01]['seen']} "
                  f"48-52% {s['within'][0.02]['expected']:.1f} vs {s['within'][0.02]['seen']} 45-55% {s['within'][0.05]['expected']:.1f} vs {s['within'][0.05]['seen']}{tests}")
            if kmode != "all":
                cells = "; ".join(f"{BANDL[b]}: " + ", ".join(f"{WIN[w]} {s['by_band'][b]['within'][w]['expected']:.1f}/{ref['by_band'][b]['within'][w]['expected']:.1f} vs {s['by_band'][b]['within'][w]['seen']}" for w in WIN) for b in F.VARIANT_SAFE)
                print(f"      safe bands (this / record vs seen): {cells}; z rms by band " + " ".join(f"{BANDL[b]} {s['by_band'][b]['z_rms']:.2f}/{ref['by_band'][b]['z_rms']:.2f}" for b in range(4) if s['by_band'][b]['races']))

        print("11.3 WHAT EACH WOULD DO TO p: the density at 1/2 with its factor, against the record's (p = density / 2n): median ratio and the 10th-90th percentiles by band, by year; the sum (expected exact ties) ratio")
        a_rec = F.near_scored(rows, rec)
        for kmode in F.K_MODES[1:]:
            v = vname(Lv, kmode)
            sch_v, sch_r = scores[kmode][1], RECORD_SCHEME[Lv]
            a_alt = F.near_scored(rows, v)
            ratios, bands, yrs, sum_rec, sum_alt = [], [], [], 0.0, 0.0
            by_year = {}
            for T in years:
                if (Lv, T) not in a_rec:
                    continue
                ar, aa = a_rec[(Lv, T)], a_alt[(Lv, T)]
                Fr = F.factors_for(rows, Lv, T, ar, sch_r, rec)
                Fa = F.factors_for(rows, Lv, T, aa, sch_v, v)
                fr, fa = density_half(ar, Fr, tails), density_half(aa, Fa, tails)
                n2 = np.array([r["n2"] for r in F.test_rows(rows, Lv, T)], float)
                pr, pa = fr / (2 * n2), fa / (2 * n2)
                sum_rec += pr.sum()
                sum_alt += pa.sum()
                by_year[T] = (pa.sum() / pr.sum(), np.median(fa / fr))
                ratios.append(fa / fr)
                bands.append(np.array([max(i for i, x in enumerate(F.VARIANT_BANDS) if abs(m0 - 0.5) >= x) for m0 in ar["mu"]]))
            ratios, bands = np.concatenate(ratios), np.concatenate(bands)
            print(f"  k {kmode:6s}: sum of p alt/record {sum_alt / sum_rec:.3f}; median ratio {np.median(ratios):.3f} (10th-90th {np.percentile(ratios, 10):.3f}-{np.percentile(ratios, 90):.3f}); by band "
                  + ", ".join(f"{BANDL[b]} {np.median(ratios[bands == b]):.3f}" for b in range(4) if (bands == b).any())
                  + "; by year (sum ratio, median) " + " ".join(f"{T} {x[0]:.2f}/{x[1]:.2f}" for T, x in by_year.items()))
        # the 2024 forecasts in the files, under each k: the record's own p and the ratio (the forecast of record is the file's)
    print("\n  D2's reading (REPORT 7): House z rms 0.92, 0.86, 0.75, 0.83, 0.92, 0.89, 0.82, 0.76 for 2010-2024 after shrinkage; within 5 points of even 0.80; Senate 0.57-0.93; governors 0.72-1.36.")
    print("  Chosen here: nothing. The alternatives are fitted on earlier years only and scored the way D2's variants were, so the orchestrator can read them against the same tests.")


if __name__ == "__main__":
    main()
