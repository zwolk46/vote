"""C41 (eighth pass; the orchestrator's words of 2026-11-12 23:11 UTC: "Start the eighth pass now with its end fixed at
346273e, main's head at the merge. Its scope is three items. First, #96 and #97 ..."). #96 (main 46825da -> 9118755): D3's
rerun of D2's governor build with Hawaii 2018's governor at the Office of Elections' certified count (Tupola 131,719; the
orchestrator's order of 2026-11-07 19:49, item 2; data/local/REPORT.md section 30), every move listed in
data/local/moves-governor-hi-refit.json.

  41.1 The moves file against my own diff of every governor, House and Senate record between the two commits (the codes,
       p before and after, the ratios of the p beside), and the files' own blocks.
  41.2 My own refit (m2fit: Cha's, MEDSL's and the files' rows, as c9) with and without the certified figures, against the
       model blocks before and after: the terms' relative differences, and the ratio of every moved governor p from my fits
       against the file's ratio.
  41.3 The back-test files and history.json: every leaf that changed, against D3's words.
[measured] throughout; D3's words [stated].
"""
import collections
import copy
import json
import math
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402
import m2fit as F  # noqa: E402
from c9_fit2 import RECORD_VARIANT  # noqa: E402

BEFORE, AFTER = "46825da", "9118755"
MV = os.path.join(L.DATA, "local", "moves-governor-hi-refit.json")
WT = os.path.join(L.CACHE, "eighth", "wt")
STAMPS = ("commit", "read_utc")


def h1(s):
    print("\n" + "=" * 100 + f"\n{s}\n" + "=" * 100)


def worktree(commit):
    path = os.path.join(WT, commit)
    if not os.path.exists(os.path.join(path, "data")):
        os.makedirs(WT, exist_ok=True)
        subprocess.run(["git", "worktree", "add", "--detach", path, commit], cwd=L.ROOT, check=True, capture_output=True)
    return path


def leaves(x, path=""):
    if isinstance(x, dict):
        for k, v in x.items():
            if k in STAMPS:
                continue
            yield from leaves(v, f"{path}.{k}" if path else k)
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from leaves(v, f"{path}[{i}]")
    else:
        yield path, x


def diff_leaves(b, a):
    lb, la = dict(leaves(b)), dict(leaves(a))
    out = []
    for k in sorted(set(lb) | set(la)):
        vb, va = lb.get(k, "<absent>"), la.get(k, "<absent>")
        if vb != va:
            out.append((k, vb, va))
    return out


def pval(c):
    return ((c or {}).get("p") or {}).get("value")


def beside(c):
    return [x.get("value") for x in (((c or {}).get("p") or {}).get("alongside") or [])]


def my_codes(b, a):
    """My codes for a D2 record, in the file's letters: P p moved; A a p beside moved; F forecasts' shares changed;
    I forecast inputs changed; Q notes changed; B p unchanged and its block (or the forecasts' calibration) changed;
    O other fields; G gained; X lost."""
    if b is None:
        return ["G"]
    if a is None:
        return ["X"]
    codes = []
    pb, pa = pval(b), pval(a)
    if (pb is None) != (pa is None) or (pb is not None and pa is not None and abs(pa - pb) > 1e-12 * max(abs(pb), 1e-300)):
        codes.append("P")
    bb, ba = beside(b), beside(a)
    if len(bb) != len(ba) or any((x is None) != (y is None) or (x is not None and abs(y - x) > 1e-12 * max(abs(x), 1e-300)) for x, y in zip(bb, ba)):
        codes.append("A")
    fb, fa = b.get("forecasts") or [], a.get("forecasts") or []
    shares_b = [(f.get("share") or {}) for f in fb]
    shares_a = [(f.get("share") or {}) for f in fa]
    if shares_b != shares_a:
        codes.append("F")
    if (b.get("forecast_inputs") or {}) != (a.get("forecast_inputs") or {}):
        codes.append("I")
    if (b.get("notes") or []) != (a.get("notes") or []):
        codes.append("Q")
    rest_b = {k: v for k, v in b.items() if k not in ("p", "forecasts", "forecast_inputs", "notes")}
    rest_a = {k: v for k, v in a.items() if k not in ("p", "forecasts", "forecast_inputs", "notes")}
    other = [k for k, _, _ in diff_leaves(rest_b, rest_a)]
    # the block: p's other fields, and the forecasts' calibration
    # the block: every leaf of p but the values (the near-tie factor shown beside a House or Senate p sits in
    # alongside[i].near_tie_not_of_record)
    pblock = [k for k, _, _ in diff_leaves({k: v for k, v in (b.get("p") or {}).items() if k != "value"},
                                           {k: v for k, v in (a.get("p") or {}).items() if k != "value"}) if not re.fullmatch(r"alongside\[\d+\]\.value", k)]
    cal = [k for k, _, _ in diff_leaves([f.get("calibration") for f in fb], [f.get("calibration") for f in fa])]
    if "P" not in codes and (pblock or cal):
        codes.append("B")
    if other:
        codes.append("O")
    return codes


def section_1():
    h1("41.1 moves-governor-hi-refit.json against my own diff of every governor, House and Senate record, " + f"{BEFORE} -> {AFTER}")
    mv = L.load_json(MV)
    rows = {r[0]: r for r in mv["records"]}
    print(f"  the file: {len(mv['records']):,} rows ({len(rows):,} ids), against {mv['against']}; stamp_only {mv.get('stamp_only')}; "
          f"summary {json.dumps(mv['summary'])}")
    wb, wa = worktree(BEFORE), worktree(AFTER)
    files = subprocess.run(["git", "diff", "--name-only", BEFORE, AFTER, "--", "data/governor", "data/house", "data/senate"],
                           capture_output=True, text=True, cwd=L.ROOT).stdout.split()
    print(f"  data files changed: {len(files)} " + str(dict(collections.Counter(f.split('/')[1] for f in files))))
    mine, agree, dis, unlisted, examples = collections.Counter(), 0, collections.Counter(), collections.Counter(), []
    pdiff, rdiff, bdiff, seen, stamp_only = 0, 0, 0, set(), 0
    blocks_mine = {}
    for f in files:
        lv = f.split("/")[1]
        db = json.load(open(os.path.join(wb, f)))
        da = json.load(open(os.path.join(wa, f)))
        b = {c["id"]: c for c in db["contests"]}
        a = {c["id"]: c for c in da["contests"]}
        hb = {k: v for k, v in db.items() if k != "contests"}
        ha = {k: v for k, v in da.items() if k != "contests"}
        dl = diff_leaves(hb, ha)
        if dl:
            blocks_mine[f] = dl
        for i in sorted(set(b) | set(a)):
            code = my_codes(b.get(i), a.get(i))
            if not code:
                if diff_leaves(b.get(i), a.get(i)) == [] and json.dumps(b.get(i), sort_keys=True) != json.dumps(a.get(i), sort_keys=True):
                    stamp_only += 1
                continue
            seen.add(i)
            mine[(lv, ",".join(code))] += 1
            row = rows.get(i)
            if row is None:
                unlisted[(lv, ",".join(code))] += 1
                if len(examples) < 6:
                    examples.append((i, code, "not in the file", [k for k, _, _ in diff_leaves(b.get(i), a.get(i))][:5]))
                continue
            theirs = list(row[7])
            same = set(code) == set(theirs) or (set(code) - {"B", "F", "O"}) == (set(theirs) - {"B", "F", "O"})
            if same:
                agree += 1
            else:
                dis[(lv, ",".join(code), ",".join(theirs))] += 1
                if len(examples) < 12:
                    examples.append((i, code, theirs, [k for k, _, _ in diff_leaves(b.get(i), a.get(i))][:6]))
            pb, pa = pval(b.get(i)), pval(a.get(i))
            if (row[3] is None) != (pb is None) or (row[4] is None) != (pa is None) \
                    or (pb is not None and abs(row[3] - pb) > 1e-9 * max(abs(pb), 1e-300)) \
                    or (pa is not None and abs(row[4] - pa) > 1e-9 * max(abs(pa), 1e-300)):
                pdiff += 1
                if pdiff <= 3:
                    print(f"    p before/after differ from the record: {i} row {row[3]} {row[4]} record {pb} {pa}")
            if pb and pa and row[5] is not None and abs(row[5] - pa / pb) > 1.5e-6 * max(1.0, abs(row[5])) + 6e-7:
                rdiff += 1
                if rdiff <= 3:
                    print(f"    ratio off the record's: {i} row {row[5]} record {pa / pb:.6f}")
            bb, ba = beside(b.get(i)), beside(a.get(i))
            mine_r = [round(y / x, 6) if x else None for x, y in zip(bb, ba)]
            if len(row[6]) != len(mine_r) or any(m_ is None or t_ is None or abs(m_ - t_) > 1.5e-6 for m_, t_ in zip(mine_r, row[6])):
                bdiff += 1
                if bdiff <= 3:
                    print(f"    the p beside's ratios differ: {i} row {row[6]} mine {mine_r}")
    listed_not_mine = [i for i in rows if i not in seen]
    print("  my diff, by level and codes: " + "; ".join(f"{lv} {k} {v}" for (lv, k), v in sorted(mine.items())))
    print(f"  records whose only difference is a stamp (commit, read_utc), left out as the file does: {stamp_only:,} (the file's stamp_only {mv.get('stamp_only')})")
    print(f"  rows whose codes I share (B, F and O read as one kind): {agree:,} of {len(seen):,} ids in my diff; differing: {sum(dis.values())}; "
          f"ids in my diff but not in the file: {sum(unlisted.values())} {dict(unlisted) if unlisted else ''}; in the file but not in my diff: "
          f"{len(listed_not_mine)} {listed_not_mine[:5]}")
    print(f"  p before/after other than the record's: {pdiff}; ratios off the record's: {rdiff}; the p beside's ratios off: {bdiff}")
    for (lv, mc, tc), v in sorted(dis.items(), key=lambda kv: -kv[1])[:8]:
        print(f"    mine {mc} theirs {tc} {lv}: {v}")
    for e in examples[:8]:
        print(f"    e.g. {e[0]}: mine {e[1]}, theirs {e[2]}; differs in {e[3]}")
    # the moved governor p, by year, and the range of the ratios
    moved = [r for r in mv["records"] if "P" in r[7]]
    by = collections.Counter(r[0].split("-")[0] for r in moved)
    rs = sorted((r[5], r[0]) for r in moved)
    print(f"  the file's moved p: {len(moved)} ({dict(sorted(by.items()))}); ratios from {rs[0][0]} ({rs[0][1]}) to {rs[-1][0]} ({rs[-1][1]}) "
          f"(D3: 29, x0.9950 Wyoming 2022 to x1.0003 Vermont 2020); under: {dict(collections.Counter(r[2][:20] for r in moved))}")
    # the files' own blocks
    fb = mv.get("file_blocks") or {}
    print(f"\n  the files' own blocks: the file lists {len(fb)}; my diff finds {len(blocks_mine)} files with a block leaf changed; "
          f"same set: {set(fb) == set(blocks_mine)}; mine not theirs {sorted(set(blocks_mine) - set(fb))[:5]}; theirs not mine {sorted(set(fb) - set(blocks_mine))[:5]}")
    kinds = collections.Counter()
    for f, dl in sorted(blocks_mine.items()):
        kinds[(f.split("/")[1], tuple(sorted({re.sub(r"\[\d+\]", "[]", k.split(".")[0] + ("." + k.split(".")[1] if "." in k else "")) for k, _, _ in dl})))] += 1
    for (lv, ks), v in sorted(kinds.items()):
        print(f"    {lv}: {v} file(s) differ in {list(ks)[:8]}")
    for f in ("data/governor/2022.json", "data/governor/2024.json", "data/governor/2020.json"):
        if f in blocks_mine:
            print(f"    {f}: " + "; ".join(f"{k} {vb!s:.10} -> {va!s:.10}" for k, vb, va in blocks_mine[f] if k.startswith("model.") and not k.startswith("model.ZtZ"))[:600])
    return wb, wa, mv


def block_terms(m):
    return {"b_lean": m["b_lean"], "b_inc": m["b_inc"], "b_lag": m.get("b_lag"), "s_e_fitted": m.get("s_e_fitted"), "s_e": m["s_e"],
            "s_a": m["s_a"], "c0": m["c"][0], "c1": m["c"][1], "c2": m["c"][2], "k": m.get("k"), "national_sd": m.get("national_sd"), "sd": m.get("sd")}


def my_terms(m):
    # my fit's s_e is the fitted one; the block's s_e carries k (s_e = k x s_e_fitted), so s_e_fitted is the term compared
    return {"b_lean": m["b_lean"], "b_inc": m["b_inc"], "b_lag": m.get("b_lag"), "s_e_fitted": m["s_e"], "s_e": m["s_e"] * m.get("k", 1.0),
            "s_a": m["s_a"], "c0": m["c"][0], "c1": m["c"][1], "c2": m["c"][2], "k": m.get("k"), "national_sd": None, "sd": None}


def rel(a, b):
    if a is None or b is None:
        return None
    return abs(a - b) / max(abs(b), 1e-12)


def section_2(wb, wa, mv):
    h1("41.2 My own refit with and without Hawaii 2018's certified figures, against the model blocks before and after")
    d = F.all_rows()
    rows = d["rows"]
    print(f"  rows {len(rows):,} (c9's); the certified figures applied on load: {d.get('certified_applied')}")
    r0 = next(r for r in rows if r.get("id") == "2018-governor-HI")
    print(f"  Hawaii 2018's governor row: Cha's y {r0['cha_y']:.6f} (n2 {r0['cha_n2']:,}); certified y {r0['y']:.6f} (n2 {r0['n2']:,}): "
          f"Tupola at Cha's figure {round(r0['cha_n2'] * (1 - r0['cha_y'])):,} against the certified 131,719; D2's record before and after: two_party [244934, 131719] (unchanged, from #95)")
    r22 = next((r for r in rows if r["level"] == "governor" and r["state"] == "HI" and r["year"] == 2022), None)
    print(f"  Hawaii 2022's last-race input: mine {r22['lag']:.6f}; the record's forecast_inputs.last_governor_race.share_D before 0.640094 -> after 0.650291 [stated: the files]")
    rows_after = copy.deepcopy(rows)
    rows_before = copy.deepcopy(rows)
    F.apply_certified(rows_before, on=False)
    years = sorted({int(f[:4]) for f in os.listdir(os.path.join(wa, "data", "governor")) if f.endswith(".json")})
    even = [t for t in years if t % 2 == 0 and t >= 2020]
    print(f"\n  {'year':6s} {'terms':10s} " + " ".join(f"{k:>10s}" for k in ("b_lean", "b_inc", "b_lag", "s_e", "s_a", "c0", "c1", "c2", "k")))
    fits = {}
    for label, rr, wt in (("before", rows_before, wb), ("after", rows_after, wa)):
        F._RAW.clear()
        F._SC.clear()
        for t in even:
            m, fy = F.variant_model(rr, "governor", t, RECORD_VARIANT["governor"])
            blk = json.load(open(os.path.join(wt, "data", "governor", f"{t}.json")))["model"]
            fits[(label, t)] = (m, blk)
            mt, bt = my_terms(m), block_terms(blk)
            print(f"  {t:<6d} {label + ', mine':10s} " + " ".join(f"{mt[k]:10.6f}" for k in ("b_lean", "b_inc", "b_lag", "s_e", "s_a", "c0", "c1", "c2", "k")))
            print(f"  {'':6s} {'block':10s} " + " ".join(f"{bt[k]:10.6f}" for k in ("b_lean", "b_inc", "b_lag", "s_e", "s_a", "c0", "c1", "c2", "k")))
            worst = max((rel(mt[k], bt[k]), k) for k in ("b_lean", "b_inc", "b_lag", "s_e", "s_a", "c0", "c1", "c2", "k") if bt.get(k) is not None)
            print(f"  {'':6s} {'rel diff':10s} largest {worst[0]:.1e} ({worst[1]}); calibration races mine {m['calibration'].get('races') if isinstance(m.get('calibration'), dict) else '?'} / the block's {(blk.get('calibration') or {}).get('races')}; the block's fit races {blk.get('races')}")
    print("\n  the change before -> after, the blocks' against my fits' (a sign and size test of the refit):")
    for t in even:
        mb, bb = fits[("before", t)]
        ma, ba = fits[("after", t)]
        mt_b, mt_a, bt_b, bt_a = my_terms(mb), my_terms(ma), block_terms(bb), block_terms(ba)
        print(f"    {t}: " + "; ".join(f"{k} block {bt_a[k] - bt_b[k]:+.2e} mine {mt_a[k] - mt_b[k]:+.2e}" for k in ("b_lean", "b_inc", "b_lag", "s_e", "s_a", "c0", "c1", "k")))
    # every moved governor p (even years) from my fits before and after
    print("\n  the moved governor p of the even years, the ratio after/before from my fits against the file's:")
    moved = [r for r in mv["records"] if "P" in r[7] and r[1].startswith("data/governor")]
    byid = {r.get("id"): r for r in rows if r.get("id")}
    tal = collections.Counter()
    worst = []
    for row in sorted(moved):
        cid = row[0]
        t = int(cid[:4])
        if t % 2:
            tal["odd year (c25's route; the blocks below)"] += 1
            continue
        r = byid.get(cid)
        if r is None:
            tal["no row of mine"] += 1
            continue
        rb = next(x for x in rows_before if x.get("id") == cid)
        ra = next(x for x in rows_after if x.get("id") == cid)
        mb, _ = fits[("before", t)]
        ma, _ = fits[("after", t)]
        mean_b, sd_b, _ = F.predict(mb, rb)
        mean_a, sd_a, _ = F.predict(ma, ra)
        tails = "normal" if "normal" in row[2] else "t4"
        fb_, fa_ = L.f_half(mean_b, sd_b, tails), L.f_half(mean_a, sd_a, tails)
        ratio = fa_ / fb_
        d_ = abs(ratio - row[5])
        band = "within 1e-4" if d_ <= 1e-4 else "within 1e-3" if d_ <= 1e-3 else "beyond 1e-3"
        same_dir = (ratio - 1) * (row[5] - 1) > 0 or abs(ratio - 1) < 1e-5 or abs(row[5] - 1) < 1e-5
        tal[(band, "same direction" if same_dir else "OPPOSITE")] += 1
        worst.append((d_, cid, row[5], round(ratio, 6)))
        # the p beside (the model's own, t4) where the file lists it
    for k_, v in sorted(tal.items(), key=str):
        print(f"    {str(k_):50s} {v}")
    worst.sort(reverse=True)
    for d_, cid, theirs, mine_ in worst[:6]:
        print(f"    {cid}: file x{theirs:.6f}, mine x{mine_:.6f}")
    # the odd years: the p follow their files' blocks (c8's rule), and the blocks' terms changed
    print("\n  the odd years' moved p: p recomputed from each record's own forecast (density: f(1/2)/(2n)) before and after, and the files' blocks:")
    for row in sorted(moved):
        cid = row[0]
        t = int(cid[:4])
        if t % 2 == 0:
            continue
        f_ = f"data/governor/{t}.json"
        cb = next(c for c in json.load(open(os.path.join(wb, f_)))["contests"] if c["id"] == cid)
        ca = next(c for c in json.load(open(os.path.join(wa, f_)))["contests"] if c["id"] == cid)
        out = []
        for c in (cb, ca):
            p = c["p"]
            fc = c["forecasts"][p["of_forecast"]]
            pm = L.p_density(p["n"], L.f_half(fc["share"]["mean"], fc["share"]["sd"], fc["share"]["tails"]))
            out.append((p["value"], pm, fc["share"]["mean"], fc["share"]["sd"]))
        print(f"    {cid}: before p {out[0][0]:.6e} (from its forecast {out[0][1]:.6e}; mean {out[0][2]:.6f} sd {out[0][3]:.6f}) -> after {out[1][0]:.6e} "
              f"(from its forecast {out[1][1]:.6e}; mean {out[1][2]:.6f} sd {out[1][3]:.6f}); ratio {row[5]}")
    # the odd-year files' blocks: what changed
    for f_ in sorted(f for f in os.listdir(os.path.join(wa, "data", "governor")) if int(f[:4]) % 2 and f.endswith(".json")):
        hb = {k: v for k, v in json.load(open(os.path.join(wb, "data", "governor", f_))).items() if k != "contests"}
        ha = {k: v for k, v in json.load(open(os.path.join(wa, "data", "governor", f_))).items() if k != "contests"}
        dl = diff_leaves(hb, ha)
        if dl:
            print(f"    {f_}: " + "; ".join(f"{k} {vb!s:.9} -> {va!s:.9}" for k, vb, va in dl[:6]) + (f" ... ({len(dl)} leaves)" if len(dl) > 6 else ""))


def section_3(wb, wa):
    h1("41.3 The back-test files and history.json: every leaf that changed")
    for f_ in ("data/congress/backtest.json", "data/congress/backtest-governor-odd.json", "data/congress/history.json"):
        b = json.load(open(os.path.join(wb, f_)))
        a = json.load(open(os.path.join(wa, f_)))
        dl = diff_leaves(b, a)
        tops = collections.Counter(k.split(".")[0] + ("." + k.split(".")[1] if "." in k else "") for k, _, _ in dl)
        print(f"  {f_}: {len(dl)} leaves differ, under " + "; ".join(f"{k} {v}" for k, v in sorted(tops.items(), key=lambda kv: -kv[1])[:8]))
        biggest = sorted(((abs(va / vb - 1) if isinstance(vb, float) and isinstance(va, float) and vb else 1.0), k, vb, va) for k, vb, va in dl)[-3:]
        for d_, k, vb, va in biggest:
            print(f"    largest relative change {d_:.2e}: {k}: {vb!s:.40} -> {va!s:.40}")
        for k, vb, va in dl:
            if k in ("schemes.earlier_calibrated.governor.pooled_2006_2024.mean_log_score", "plain.mean_log_score") or k.endswith("verdict") or k.endswith("adopted"):
                print(f"    {k}: {vb} -> {va}")
        verdicts = [(k, vb, va) for k, vb, va in dl if isinstance(vb, (bool, str)) or isinstance(va, (bool, str))]
        print(f"    leaves that are words or verdicts, changed: {len(verdicts)} {verdicts[:4]}")
    print("  D3 (section 30): the governors' pooled log score 1.14362 -> 1.14380; k of 2020, 2022 and 2024 in the fifth place; the odd-year plain route 1.09708 -> 1.09701; no verdict changes")


def main():
    print(f"C41 #96, the governor refit with Hawaii 2018's certified count; {L.git_head()}")
    wb, wa, mv = section_1()
    section_2(wb, wa, mv)
    section_3(wb, wa)


if __name__ == "__main__":
    main()
