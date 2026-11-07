"""C20. #61, route (c)'s size bins under the robustness test (the third pass's item 3): data/local/size-bins-test.json
reproduced by my own implementation of the variant and the test (data/local/REPORT.md section 11, fixed before the
record's run), on my own pools:
  legislatures: Klarner's multi-seat generals (the state files' Klarner-sourced contests that my reading of the ballot
                sends to route (c), m2d3.structure_state), each year forecast from the earlier years, and MEDSL's 2024
                legislature contests the files forecast at the boundary, from Klarner's years;
  ncsbe:        the State Board's route-(c) contests from 2014 (c15's North Carolina pool, with the deciding rounds);
  medsl local:  MEDSL's local route-(c) contests 2018-2024.
The variant: the class density from the class's earlier like races in the contest's own size bin (0-3,000, 3,000-10,000,
10,000-30,000, 30,000 or more votes of the deciding pair) where that holds 100 or more, else the class as a whole. The
counts: within 49-51% (0.02 f), within 10 votes (10.5 f/n), a margin of 0 or 1 (1.5 f/n), each capped at 1; seen from
the deciding pair. Cells: (class, bin) and count, tested where seen or expected is 5 or more; worse where the variant moves
further from the count seen. Improves: the 49-51% total nearer and the Poisson deviance over the 49-51% cells lower;
passes: improves with no tested cell worse; adopted only if it passes with every one scored year left out as well.
Then: which files #61 (a195785) changed. [measured]; the record's figures [stated].
"""
import collections
import glob
import json
import math
import os
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402
import m2d3 as D  # noqa: E402
import c15_d3_refit as C15  # noqa: E402

COUNTS = ("49_51", "within_10_votes", "margin_0_or_1")
CELL_MIN = 5
BIN_NAMES = ["0-3,000", "3,000-10,000", "10,000-30,000", "30,000 or more"]


def expected(f, n):
    return {"49_51": min(1.0, 0.02 * f), "within_10_votes": min(1.0, f * 10.5 / n), "margin_0_or_1": min(1.0, 1.5 * f / n)}


def seen_of(s, n):
    margin = round((2 * s - 1) * n)
    return {"49_51": s <= 0.51, "within_10_votes": margin <= 10, "margin_0_or_1": margin <= 1}


def deviance(pairs):
    d = 0.0
    for e, s in pairs:
        if e <= 0:
            continue
        d += 2 * ((s * math.log(s / e) if s > 0 else 0.0) - (s - e))
    return d


def forecast(scored, train_of):
    """scored: rows (year, key, s, n); train_of(year): the training rows. The record's density and the variant's."""
    out, dens, vdens = [], {}, {}
    for y, key, s, n in scored:
        if (y, key) not in dens:
            tr = train_of(y)
            dens[(y, key)] = D.class_density([x[2] for x in tr if x[1] == key])
        f = dens[(y, key)][0]
        if f is None:
            continue
        b = D.size_bin(n)
        if (y, key, b) not in vdens:
            tr = train_of(y)
            sub = [x[2] for x in tr if x[1] == key and D.size_bin(x[3]) == b]
            if len(sub) >= D.MIN_CLASS:
                vdens[(y, key, b)] = (D.class_density(sub)[0], True)
            else:
                vdens[(y, key, b)] = (f, False)
        v, own = vdens[(y, key, b)]
        out.append({"year": y, "key": key, "bin": b, "own": own, "rec": expected(f, n), "var": expected(v, n), "seen": seen_of(s, n)})
    return out


def score(recs, years):
    cells = collections.defaultdict(lambda: {c: [0.0, 0.0, 0] for c in COUNTS})
    bins = collections.defaultdict(lambda: {c: [0.0, 0.0, 0] for c in COUNTS})
    n = own = 0
    for r in recs:
        if r["year"] not in years:
            continue
        n += 1
        own += r["own"]
        for tgt in (cells[(r["key"], r["bin"])], bins[r["bin"]]):
            for c in COUNTS:
                tgt[c][0] += r["rec"][c]
                tgt[c][1] += r["var"][c]
                tgt[c][2] += r["seen"][c]
    tot = [sum(v["49_51"][i] for v in cells.values()) for i in range(3)]
    db = deviance([(v["49_51"][0], v["49_51"][2]) for v in cells.values()])
    da = deviance([(v["49_51"][1], v["49_51"][2]) for v in cells.values()])
    worse = sorted(f"{k[0]}; {BIN_NAMES[k[1]]} votes; {c}" for k, v in cells.items() for c in COUNTS
                   if max(v[c][0], v[c][2]) >= CELL_MIN and abs(v[c][1] - v[c][2]) > abs(v[c][0] - v[c][2]))
    tested = sum(1 for v in cells.values() for c in COUNTS if max(v[c][0], v[c][2]) >= CELL_MIN)
    improves = abs(tot[1] - tot[2]) < abs(tot[0] - tot[2]) and da < db
    return {"contests": n, "own": own, "seen": int(tot[2]), "rec": tot[0], "var": tot[1], "db": db, "da": da, "improves": improves,
            "worse": worse, "tested": tested, "passes": improves and not worse,
            "by_bin": {BIN_NAMES[b]: {c: (v[c][0], v[c][1], int(v[c][2])) for c in COUNTS} for b, v in sorted(bins.items())}}


def test(name, recs, rec):
    print(f"\n  {name}:")
    if not recs:
        print(f"    no contest has a forecast (no class with 100 or more earlier like races); the record: {rec.get('test', {}).get('contests')} contests, adopted {rec.get('adopted')}")
        return
    years = sorted({r["year"] for r in recs})
    a = score(recs, set(years))
    t = rec["test"]
    rt = rec["test"]["seen_49_51"]
    print("    scored years, seen within 49-51% (the record's, from its leave-one-year-out): " + ", ".join(
        f"{y} {sum(r['seen']['49_51'] for r in recs if r['year'] == y)} ({rt - rec['leave_one_year_out'][str(y)]['seen_49_51'] if str(y) in rec['leave_one_year_out'] and 'seen_49_51' in rec['leave_one_year_out'][str(y)] else '-'})" for y in years))
    print(f"    {a['contests']:,} contests ({t['contests']:,}), with their own bin {a['own']:,} ({t['contests_with_their_own_bin']:,}); 49-51%: record {a['rec']:.1f} ({t['expected_49_51_record']}), "
          f"variant {a['var']:.1f} ({t['expected_49_51_variant']}), seen {a['seen']} ({t['seen_49_51']}); deviance {a['db']:.2f} -> {a['da']:.2f} ({t['deviance_record']} -> {t['deviance_variant']}); "
          f"improves {a['improves']} ({t['improves']}); tested cells worse {len(a['worse'])} of {a['tested']} ({len(t['tested_cells_made_worse'])} of {t['tested_cells']}); passes {a['passes']} ({t['passes']})")
    rw = set(t["tested_cells_made_worse"])
    mw = set(a["worse"])
    print(f"    the cells made worse: the same {len(rw & mw)}; mine only {sorted(mw - rw)}; record only {sorted(rw - mw)}")
    for b, v in a["by_bin"].items():
        rb = t["by_size_bin"].get(b, {})
        print(f"    {b:15s} " + "; ".join(f"{c} {v[c][0]:.1f}/{v[c][1]:.1f} vs {v[c][2]} ({rb.get(c, {}).get('record')}/{rb.get(c, {}).get('variant')} vs {rb.get(c, {}).get('seen')})" for c in COUNTS))
    fails = []
    diff = []
    for y in years:
        if len(years) == 1:
            fails.append(y)
            continue
        x = score(recs, set(years) - {y})
        r2 = rec["leave_one_year_out"].get(str(y), {})
        if not x["passes"]:
            fails.append(y)
        if r2 and (x["passes"] != r2.get("passes") or abs(x["var"] - r2.get("expected_49_51_variant", -1)) > 0.15):
            diff.append(f"{y}: mine {x['rec']:.1f}/{x['var']:.1f} vs {x['seen']} passes {x['passes']}; record {r2.get('expected_49_51_record')}/{r2.get('expected_49_51_variant')} vs {r2.get('seen_49_51')} passes {r2.get('passes')}")
    print(f"    leave one scored year out: fails without {len(fails)} of {len(years)} years ({len(rec['fails_without'])} of {len(rec['leave_one_year_out'])}); adopted {a['passes'] and not fails} ({rec['adopted']})"
          + (f"; years where mine and the record differ: {diff[:6]}" if diff else "; every year's count and verdict as the record's"))


def pool_legislatures():
    rows = []
    for level in ("state-upper", "state-lower"):
        for r in D.rows(level):
            if r["src"] != "klarner":
                continue
            st = D.structure_state(r)
            if st is None or st[0] != "boundary":
                continue
            pr = D.deciding_pair(r, r["seats"])
            if pr is None or pr[0] + pr[1] <= 0:
                continue
            rows.append((r["year"], st[1], max(pr) / (pr[0] + pr[1]), pr[0] + pr[1]))
    rows24 = []
    for path in sorted(glob.glob(os.path.join(L.DATA, "state-*", "2024", "*.json"))):
        for c in L.load_json(path)["contests"]:
            fc = (c.get("forecasts") or [{}])[-1]
            if fc.get("route") == "boundary" and c.get("boundary"):
                v = c["boundary"]["votes"]
                rows24.append((2024, fc["class"], max(v) / sum(v), sum(v)))
    print(f"  legislatures: {len(rows):,} Klarner route-(c) rows {min(r[0] for r in rows)}-{max(r[0] for r in rows)} (my reading of the ballot), {len(rows24)} MEDSL 2024 rows at the boundary")
    recs = forecast(rows, lambda t: [r for r in rows if r[0] < t])
    recs += forecast(rows24, lambda t: rows)
    return recs


def pool_nc(first):
    """c15's North Carolina pool with the deciding pair's votes: every State Board contest from `first` the route can
    take (the record's like_rows takes every date, the November dates of MEDSL's years too, which the files forecast
    on MEDSL's route; the key then from my own reading by the State Board's classes)."""
    rows = []
    for r in D.rows("local"):
        if r["state"] != "NC" or r["year"] < first or r["src"] != "ncsbe":
            continue
        if r["status"] == "value" and r["route"] is None:
            continue
        reason = r["reason"] or ""
        if r["status"] == "not_computed" and not any(reason.startswith(x) for x in C15.POOL_REASONS):
            continue
        k = r["seats"] or 1
        if r["pair"]:
            v0, v1 = r["pair"]["votes"]
        else:
            b = C15.ballot_local(r)
            if len(b) <= k:
                continue
            v0, v1 = b[k - 1][1], b[k][1]
        if v0 + v1 <= 0:
            continue
        top = sorted([a for a in r["cands"] if a[1] is not None], key=lambda a: -a[1])
        if any(C15._generic(a[2]) for a in top[k - 1:k + 1]):
            continue
        key = r["cls"] if (not C15.medsl_route(r) and r["cls"]) else C15.structure_local(r, nc=True)[1]
        if key and "seats at once" in key:
            rows.append((r["year"], key, max(v0, v1) / (v0 + v1), v0 + v1))
    print(f"  ncsbe from {first}: {len(rows):,} route-(c) rows; by year " + ", ".join(f"{y} {c}" for y, c in sorted(collections.Counter(r[0] for r in rows).items())))
    return forecast(rows, lambda t: [r for r in rows if r[0] < t])


def pool_medsl():
    rows = []
    for r in D.rows("local"):
        if not C15.medsl_route(r) or r["status"] == "value" and r["route"] is None:
            continue
        reason = r["reason"] or ""
        if r["status"] == "not_computed" and not any(reason.startswith(x) for x in C15.POOL_REASONS):
            continue
        k = r["seats"] or 1
        if r["pair"]:
            v0, v1 = r["pair"]["votes"]
        else:
            b = C15.ballot_local(r)
            if len(b) <= k:
                continue
            v0, v1 = b[k - 1][1], b[k][1]
        if v0 + v1 <= 0:
            continue
        key = r["cls"] if (r["route"] in ("class", "boundary") or (r["cls"] and not r["route"])) else None
        if key and "seats at once" in key:
            rows.append((r["year"], key, max(v0, v1) / (v0 + v1), v0 + v1))
    print(f"  medsl local: {len(rows):,} route-(c) rows; classes with 100 or more earlier rows for some year: "
          + str(sum(1 for y in sorted({r[0] for r in rows}) for key in {r[1] for r in rows} if sum(1 for r in rows if r[1] == key and r[0] < y) >= D.MIN_CLASS)))
    return forecast(rows, lambda t: [r for r in rows if r[0] < t])


def main():
    print("C20. #61: ROUTE (c)'S SIZE BINS UNDER THE ROBUSTNESS TEST, REPRODUCED ON MY OWN POOLS")
    print(f"repository HEAD {L.git_head()}")
    rec = json.load(open(os.path.join(L.DATA, "local", "size-bins-test.json")))
    print(f"  the record: written {rec['written_utc']}, commit {rec['commit']}, bins {rec['bins']}, cell_min {rec['cell_min']}")
    test("legislatures", pool_legislatures(), rec["pools"]["legislatures"])
    for first in (2014, 2015):
        test(f"ncsbe (from {first})", pool_nc(first), rec["pools"]["ncsbe"])
    test("medsl local", pool_medsl(), rec["pools"]["medsl local"])
    out = subprocess.run(["git", "diff", "--stat", "a195785~1", "a195785"], cwd=L.ROOT, capture_output=True, text=True).stdout
    files = [l.split("|")[0].strip() for l in out.strip().split("\n")[:-1]]
    print(f"\n  files #61 (a195785) changed: {files}; p files (data/<level>/<year>/) among them: {[f for f in files if '/20' in f or '/19' in f]}")


if __name__ == "__main__":
    main()
