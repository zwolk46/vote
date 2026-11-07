"""C16. The near-even notes' two tests (the orchestrator, 2026-11-07 11:04 UTC).

Each p of the House's and the Senate's own forecast, and each statewide measure p, carries a note built from its route's
back-test ("more near-even finishes than it forecast (105 against 87.5 within 1 point, 2010 to 2024), so p may be low").
The orchestrator's rule for such a note: it stands only where two tests of the same record lean the same way,
  (s) seen against expected within the share line the note uses (1 point for the House, the Senate and the governors;
      5 points for the statewide measures);
  (v) seen against expected within k votes, k the smallest of 1,000, 5,000, 10,000, 20,000 and 50,000 at which 5 or more
      are expected;
a test counts only with 5 or more seen or expected (the tested-cell rule), and where only one counts the note stands on it.
Each is computed here over the note's own years, by my own implementation, on two sets of the same record:
  (A) the back-test's own rows, which the notes' figures come from (D2's 3,047 House and 256 Senate races of 2010-2024,
      rebuilt in m2fit as in the second pass, each year forecast from earlier years only under the variant of record,
      the House with its level near-tie factor as fitted on earlier years, the Senate and the governors with none);
  (B) the files' forecasts of record (the p the site shows: the model's own forecast of every contest that carries one,
      with its recorded near-tie factor), which hold 50 fewer House races and one fewer Senate race than (A), since the
      files give no p to specials, ranked-choice counts, Georgia's majority rule and Louisiana's open primary;
and for a measure the class's earlier like measures, as backtest-measures.json counts them. The chance of a count that far off is the one-sided tail (at or beyond the count seen,
on the side it fell) of the sum of the contests' own Bernoulli chances, exact by convolution, with the Poisson tail beside.
[measured] throughout; the note's own figures are quoted from the files [stated].
"""
import collections
import re
import glob
import os
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402
import m2d3 as D  # noqa: E402
import c15_d3_refit as C15  # noqa: E402
import m2fit as F  # noqa: E402

KS = (1000, 5000, 10000, 20000, 50000)
MIN_COUNT = 5
LEVELS = (("house", 2010, 2024, 0.01), ("senate", 2010, 2024, 0.01), ("governor", 2006, 2024, 0.01))
MEASURE_YEARS = (2018, 2024)


def own_forecast(c):
    for f in c.get("forecasts") or []:
        if f["by"] == "the model's own":
            return f
    return None


def q_window(x, m, sd, tails):
    return float(L.cdf(0.5 + x, m, sd, tails) - L.cdf(0.5 - x, m, sd, tails))


def p_within(x, m, sd, tails, F, q0):
    """P(|share - 1/2| <= x) under the forecast with the near-tie factor F on its 49-51% window and the forecast
    renormalised (data/congress/REPORT.md section 2.6): the window's mass times F, the rest as it was."""
    q = q_window(x, m, sd, tails)
    return (F * min(q, q0) + max(q - q0, 0.0)) / (1.0 + (F - 1.0) * q0)


def tail(ps, seen):
    """The one-sided chance of a count at or beyond `seen` on its side of the expected count: exact for the sum of
    independent Bernoulli(p_i) (by convolution), and Poisson with the same mean."""
    e = float(sum(ps))
    dist = np.array([1.0])
    for p in ps:
        dist = np.convolve(dist, [1.0 - p, p])
    if seen >= e:
        return e, float(dist[seen:].sum()), float(stats.poisson.sf(seen - 1, e))
    return e, float(dist[:seen + 1].sum()), float(stats.poisson.cdf(seen, e))


def congress_rows(level, y0, y1):
    rows, left = [], collections.Counter()
    for path in L.congress_files(level):
        doc = L.load_json(path)
        y = doc["year"]
        if not (y0 <= y <= y1):
            continue
        for c in doc["contests"]:
            f, tp = own_forecast(c), c.get("two_party")
            if f is None:
                left["no forecast of the model's own"] += 1
                continue
            if not tp or not tp.get("votes") or sum(tp["votes"]) <= 0:
                left["no two-party result"] += 1
                continue
            sh, cal = f["share"], f.get("calibration") or {}
            v = tp["votes"]
            n = v[0] + v[1]
            rows.append({"id": c["id"], "year": y, "m": sh["mean"], "sd": sh["sd"], "tails": sh["tails"],
                         "F": cal.get("factor", 1.0), "mult": cal.get("multiplier"), "n": n,
                         "dev": abs(v[0] / n - 0.5), "margin": abs(v[0] - v[1])})
    return rows, left


def backtest_rows(level, y0, y1):
    """The back-test's own rows (set A): m2fit's rebuild of D2's rows with each year's out-of-sample forecast under the
    variant of record ('none': the mean as fitted, normal tails) and, for the House, the level factor of its year."""
    rows = F.all_rows()["rows"]
    sc = F.near_scored(rows, "none")
    out = []
    for (Lv, T), a in sorted(sc.items()):
        if Lv != level or not (y0 <= T <= y1):
            continue
        test = F.test_rows(rows, Lv, T)
        assert len(test) == len(a["mu"])
        Fs = F.factors_for(rows, Lv, T, a, "level" if level == "house" else None, "none")
        for r, mu, sd, y, f in zip(test, a["mu"], a["sd"], a["y"], Fs):
            out.append({"id": r["id"], "year": T, "m": float(mu), "sd": float(sd), "tails": "normal", "F": float(f),
                        "mult": None, "n": r["n2"], "dev": abs(float(y) - 0.5), "margin": abs(2 * float(y) - 1) * r["n2"]})
    return out, {}


def two_tests(label, ps_s, seen_s, line, ladder, years_s, note=None):
    """ps_s: each contest's chance within the share line; seen_s: 0/1; ladder: {k: (ps_k, seen_k)}; years_s: {year: (exp, seen)}.
    Prints (s), (v) and the verdict; returns (lean_s, lean_v, stands)."""
    e_s, ex_s, po_s = tail(ps_s, int(sum(seen_s)))
    n_s = int(sum(seen_s))
    lean = lambda s, e: "more" if s > e else ("fewer" if s < e else "as many")  # noqa: E731
    print(f"    (s) within {line:.0%} of 1/2: expected {e_s:.2f}, seen {n_s}" + (f" (the note: {note})" if note else "")
          + f": {lean(n_s, e_s)} than forecast; chance of a count that far off: {ex_s:.3f} exact, {po_s:.3f} Poisson")
    print("        by year (expected / seen): " + "; ".join(f"{y} {e:.1f}/{s}" for y, (e, s) in sorted(years_s.items())))
    parts, chosen = [], None
    res = {}
    for k in KS:
        ps_k, seen_k = ladder[k]
        e_k, ex_k, po_k = tail(ps_k, int(sum(seen_k)))
        res[k] = (e_k, int(sum(seen_k)), ex_k, po_k)
        parts.append(f"{k:,} votes {e_k:.2f}/{int(sum(seen_k))}")
        if chosen is None and e_k >= MIN_COUNT:
            chosen = k
    print("    (v) within k votes (expected / seen): " + "; ".join(parts))
    if chosen is None:
        chosen = KS[-1]
        print(f"        no k of the five reaches {MIN_COUNT} expected; the largest, {chosen:,}, is taken")
    e_k, n_k, ex_k, po_k = res[chosen]
    print(f"        the note's k = {chosen:,} (the smallest with {MIN_COUNT} or more expected): seen {n_k} against {e_k:.2f}: "
          f"{lean(n_k, e_k)} than forecast; chance of a count that far off: {ex_k:.3f} exact, {po_k:.3f} Poisson")
    counts_s = max(e_s, n_s) >= MIN_COUNT
    counts_v = max(e_k, n_k) >= MIN_COUNT
    ls, lv = lean(n_s, e_s), lean(n_k, e_k)
    if counts_s and counts_v:
        if ls == lv:
            verdict, stands = f"both tests count and lean the same way ({ls} than forecast): the note stands", True
        else:
            verdict, stands = f"both tests count and lean opposite ways ((s) {ls}, (v) {lv}): the note goes", False
    elif counts_s or counts_v:
        which = "(s)" if counts_s else "(v)"
        verdict, stands = f"only {which} counts (the other has under {MIN_COUNT} seen and expected): the note stands on it ({ls if counts_s else lv} than forecast)", True
    else:
        verdict, stands = "neither test counts: no note", False
    print(f"    verdict: {verdict}")
    return ls, lv, stands, (e_s, n_s, ex_s), (chosen, e_k, n_k, ex_k)


def congress(level, y0, y1, line, which):
    rows, left = backtest_rows(level, y0, y1) if which == "A" else congress_rows(level, y0, y1)
    withF = sum(1 for r in rows if r["F"] != 1.0)
    # the recorded multiplier against F / (1 + (F - 1) q0), q0 my window mass: the same window and tails
    worst = 0.0
    for r in rows:
        r["q0"] = q_window(0.01, r["m"], r["sd"], r["tails"])
        if r["mult"] is not None:
            worst = max(worst, abs(r["F"] / (1 + (r["F"] - 1) * r["q0"]) / r["mult"] - 1))
    tails = collections.Counter(r["tails"] for r in rows)
    what = ("the back-test's own rows, each year forecast from earlier years only (set A)" if which == "A"
            else "the files' forecasts of record with a two-party result (set B)")
    print(f"  {level}, {y0}-{y1}, {what}: {len(rows):,} contests"
          + (f" (left out: {dict(left)})" if left else "") + f"; tails {dict(tails)}; {withF:,} carry a near-tie factor"
          + (f" (the recorded multiplier against F / (1 + (F - 1) q0) with my window mass: largest relative difference {worst:.1e})" if withF else ""))
    ps_s = [p_within(line, r["m"], r["sd"], r["tails"], r["F"], r["q0"]) for r in rows]
    seen_s = [int(r["dev"] < line) for r in rows]   # as the record counts 49-51%: strictly inside
    years = collections.defaultdict(lambda: [0.0, 0])
    for r, p, s in zip(rows, ps_s, seen_s):
        years[r["year"]][0] += p
        years[r["year"]][1] += s
    ladder = {}
    for k in KS:
        ladder[k] = ([p_within(k / (2.0 * r["n"]), r["m"], r["sd"], r["tails"], r["F"], r["q0"]) for r in rows],
                     [int(r["margin"] <= k + 1e-6) for r in rows])
    note = None
    for path in L.congress_files(level):
        doc = L.load_json(path)
        for c in doc["contests"]:
            nt = (c.get("p") or {}).get("note")
            if nt:
                note = nt[nt.find("(") + 1:nt.find(")")]
                break
        if note:
            break
    return two_tests(level, ps_s, seen_s, line, ladder, {y: tuple(v) for y, v in years.items()}, note)


def measures():
    """Statewide measures (class 'statewide measure'), 2018-2024, like past measures: (s) the class's earlier measures'
    share within 5 points of 1/2 (backtest-measures.json near_half, which the note cites), (v) their share within
    k/(2n) of 1/2 (the same record read at the votes line), n the measure's yes + no."""
    pool = C15.measure_pool()
    by_key = collections.defaultdict(list)
    for y, k, s, rid in pool:
        by_key[k].append((y, s))
    n_of = {}
    for r in D.rows("measure"):
        yes = sum(a[1] or 0 for a in r["cands"] if C15.side(a[2]) == "yes")
        no = sum(a[1] or 0 for a in r["cands"] if C15.side(a[2]) == "no")
        n_of[r["id"]] = yes + no
    rows = []
    for y, key, s, rid in pool:
        if key != "statewide measure" or not (MEASURE_YEARS[0] <= y <= MEASURE_YEARS[1]):
            continue
        tr = np.array([x for yy, x in by_key[key] if yy < y])
        if not len(tr):
            continue
        rows.append({"id": rid, "year": y, "s": s, "n": n_of[rid], "tr": tr})
    rec_n = ((L.load_json(os.path.join(L.DATA, "measure", "backtest-measures.json")).get("near_half") or {}).get("all years statewide measure") or {}).get("measures")
    print(f"  statewide measures, {MEASURE_YEARS[0]}-{MEASURE_YEARS[1]}: {len(rows)} measures whose class has earlier years "
          f"(backtest-measures.json near_half 'all years statewide measure': {rec_n}); by year "
          + ", ".join(f"{y} {c}" for y, c in sorted(collections.Counter(r['year'] for r in rows).items())))
    emp = lambda r, x: float(np.mean(np.abs(r["tr"] - 0.5) <= x + 1e-12))  # noqa: E731
    ps_s = [emp(r, 0.05) for r in rows]
    seen_s = [int(abs(r["s"] - 0.5) <= 0.05 + 1e-12) for r in rows]
    years = collections.defaultdict(lambda: [0.0, 0])
    for r, p, s in zip(rows, ps_s, seen_s):
        years[r["year"]][0] += p
        years[r["year"]][1] += s
    ladder = {k: ([emp(r, k / (2.0 * r["n"])) for r in rows], [int(abs(2 * r["s"] - 1) * r["n"] <= k + 0.5) for r in rows]) for k in KS}
    note_fig = next((m.group(0) for r in D.rows("measure") for m in [re.search(r"\d+ against [\d.]+", ((r.get("p") or {}).get("note") or ""))] if m), "none")
    out = two_tests("measures", ps_s, seen_s, 0.05, ladder, {y: tuple(v) for y, v in years.items()}, note_fig)
    # the same (v) in the p's own form: the class density at 1/2 by the D3-v1.1 window rule (100 or more like measures),
    # f x k / n inside the window, the empirical share beyond it
    parts = []
    for k in KS:
        e = s_ = 0.0
        m = 0
        for r in rows:
            f, N, h, kin = D.density_at(r["tr"], 0.5)
            if f is None:
                continue
            x = k / (2.0 * r["n"])
            e += min(1.0, f * 2 * x) if x <= h + 1e-12 else emp(r, x)
            s_ += int(abs(2 * r["s"] - 1) * r["n"] <= k + 0.5)
            m += 1
        parts.append(f"{k:,} votes {e:.2f}/{int(s_)}")
    print(f"    (v) again in the p's own density form, over the {m} measures whose class has 100 or more earlier like measures: " + "; ".join(parts))
    return out


def main():
    print("C16. THE NEAR-EVEN NOTES' TWO TESTS: THE SHARE LINE AND THE VOTES LINE, OVER EACH NOTE'S OWN YEARS")
    print(f"repository HEAD {L.git_head()}")
    print(f"  a test counts with {MIN_COUNT} or more seen or expected; a note stands where the two tests that count lean the same way; "
          "the chance is one-sided, at or beyond the count seen on the side it fell (exact: the sum of the contests' own chances; Poisson beside)")
    summary = []
    print("  A. the back-test's own rows (the record the notes cite):")
    for level, y0, y1, line in LEVELS:
        summary.append((f"{level} (A)", congress(level, y0, y1, line, "A")))
    print("  B. the files' forecasts of record (the contests whose p carry the note):")
    for level, y0, y1, line in LEVELS:
        summary.append((f"{level} (B)", congress(level, y0, y1, line, "B")))
    print("  C. the statewide measures:")
    summary.append(("statewide measures", measures()))
    print("  summary:")
    for label, (ls, lv, stands, s, v) in summary:
        print(f"    {label:20s} (s) {s[1]} against {s[0]:.1f} ({ls}; chance {s[2]:.3f}); (v) at {v[0]:,} votes {v[2]} against {v[1]:.1f} ({lv}; chance {v[3]:.3f}); "
              f"the note {'stands' if stands else 'goes'}")
    after_67({label: x for label, x in summary})


def after_67(summary):
    """D. D2's #67 (the ruling of 11:01, relayed 11:16): data/congress/history.json records each note's two tests with
    M2's counts (set A), and the note is written only where it stands. Checked: the recorded counts against mine, the
    recorded verdicts, and which p blocks carry a near-even note today."""
    print("  D. after D2's #67: history.json's lean_note block against set A, and the notes on the p blocks")
    h = L.load_json(os.path.join(L.DATA, "congress", "history.json"))
    ln = h.get("lean_note") or {}
    for level in ("house", "senate", "governor"):
        r = ln.get(level)
        if not r:
            print(f"    {level}: no lean_note block in history.json")
            continue
        ls, lv, stands, s, v = summary[f"{level} (A)"]
        same = (r["s"]["seen"] == s[1] and abs(r["s"]["expected"] - s[0]) < 0.051 and r["v"]["within_votes"] == v[0]
                and r["v"]["seen"] == v[2] and abs(r["v"]["expected"] - v[1]) < 0.051 and bool(r["stands"]) == stands)
        print(f"    {level}: the record (s) {r['s']['seen']} against {r['s']['expected']} within {r['s']['within']}, (v) {r['v']['seen']} against {r['v']['expected']} within {r['v']['within_votes']:,} votes, "
              f"stands {r['stands']}; mine (s) {s[1]} against {s[0]:.1f}, (v) {v[2]} against {v[1]:.1f} at {v[0]:,}, stands {stands}: {'the same' if same else 'DIFFER'}")
    g = h.get("governor_note") or {}
    print(f"    governor_note: note {g.get('note')!r}, written on {g.get('written_on')} p blocks (its own 5,000-vote count {g.get('seen')} against {g.get('expected', 0):.2f})")
    for level in ("house", "senate", "governor"):
        t = collections.Counter()
        odd = collections.Counter()
        for path in L.level_files(level) if hasattr(L, "level_files") else sorted(glob.glob(os.path.join(L.DATA, level, "[0-9]*.json"))):
            doc = L.load_json(path)
            for c in doc["contests"]:
                p = c.get("p") or {}
                note = p.get("note") or ""
                (odd if doc["year"] % 2 else t)["near-even note" if "near-even" in note else "another note" if note else "no note"] += 1
        print(f"    {level}: p blocks by note: {dict(t)}" + (" (the note stands: expected on the model's own p)" if level == "house" else " (the note goes: none expected)")
              + (f"; odd years (the odd-year governors, #74: their own note, c25) {dict(odd)}" if odd else ""))


if __name__ == "__main__":
    main()
