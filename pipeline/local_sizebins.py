"""pipeline/local_sizebins.py: the robustness test of route (c), the boundary route, by size.

Written 2026-11-07 by worker D3 (briefs/D3-data-local.md, amended 08:36) at the orchestrator's order of 09:36: "as a
separate step under the robustness test: size bins for the boundary route (c). M2 finds it 12% low under 3,000 votes
and 20% high over 30,000. Adopt only if the test passes." The design was fixed in data/local/REPORT.md section 11
(10:10 UTC) before this was run; this script follows it and nothing else.

The variant (pipeline/local.py, class_density_by_size): the class density is read off the class's earlier like races
in the contest's own size bin, falling back to the class as a whole where the bin holds fewer than 100. Three pools,
each tested apart, each year forecast from the pool's earlier years only:
  legislatures   Klarner's multi-seat generals 1968-2022 (pipeline/local.py class_rows), and MEDSL's 2024 legislature
                 forecast from Klarner's 1967-2022 (its contests read from data/state-*/2024/)
  medsl local    MEDSL's local races at the boundary, 2020-2024 (pipeline/local_medsl.py local_rows)
  ncsbe          North Carolina's State Board, from 2015 (pipeline/local_ncsbe.py like_rows)
The counts are backtest.json's class tallies: within 49-51% (0.02 f), within 10 votes (10.5 f / n), a margin of 0 or
1 (1.5 f / n), each capped at 1. It improves where the 49-51% count comes nearer the count seen and the Poisson deviance
of the 49-51% counts over the cells (class and size bin) falls; a cell and count is tested where its count seen or
expected (as the record stands) is 5 or more, and made worse where the variant moves it further from the count seen.
Adopted in a pool only if it improves with no tested cell made worse over all scored years, and again with any one
scored year left out.

Run:  VOTE_CACHE=/tmp/vote-cache python3 pipeline/local_sizebins.py      writes data/local/size-bins-test.json
"""
import collections
import datetime
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import local as L  # noqa: E402
import local_medsl as LM  # noqa: E402

COUNTS = ("49_51", "within_10_votes", "margin_0_or_1")
CELL_MIN = LM.CAL_CELL_MIN   # 5, D2's rule
BIN_NAMES = [f"{L.BINS[i]:,.0f}-{L.BINS[i + 1]:,.0f}" if L.BINS[i + 1] != float("inf") else f"{L.BINS[i]:,.0f} or more"
             for i in range(len(L.BINS) - 1)]


def _expected(f, n):
    return {"49_51": min(1.0, 0.02 * f), "within_10_votes": min(1.0, f * 10.5 / n),
            "margin_0_or_1": min(1.0, 1.5 * f / n)}


def _seen(s, n):
    margin = round((2 * s - 1) * n)
    return {"49_51": s <= 0.51, "within_10_votes": margin <= 10, "margin_0_or_1": margin <= 1}


def _forecast(scored, train_of):
    """For each scored row (year, key, s, n), the record's density and the variant's, from train_of(year)."""
    out, dens, vdens = [], {}, {}
    for r in scored:
        t = r["year"]
        if (t, r["key"]) not in dens:
            dens[(t, r["key"])] = L.class_density(train_of(t), r["key"])
        f = dens[(t, r["key"])][0]
        if f is None:
            continue
        b = L.size_bin(r["n"])
        if (t, r["key"], b) not in vdens:
            vdens[(t, r["key"], b)] = L.class_density_by_size(train_of(t), r["key"], r["n"])
        v = vdens[(t, r["key"], b)]
        out.append({"year": t, "key": r["key"], "bin": b, "own_bin": v[5], "rec": _expected(f, r["n"]),
                    "var": _expected(v[0], r["n"]), "seen": _seen(r["s"], r["n"])})
    return out


def _score(recs, years):
    cells = collections.defaultdict(lambda: {c: [0.0, 0.0, 0] for c in COUNTS})
    bins = collections.defaultdict(lambda: {c: [0.0, 0.0, 0] for c in COUNTS})
    n = own = 0
    for r in recs:
        if r["year"] not in years:
            continue
        n += 1
        own += r["own_bin"]
        for tgt in (cells[(r["key"], r["bin"])], bins[r["bin"]]):
            for c in COUNTS:
                tgt[c][0] += r["rec"][c]
                tgt[c][1] += r["var"][c]
                tgt[c][2] += r["seen"][c]
    tot = [sum(v["49_51"][i] for v in cells.values()) for i in range(3)]
    db = LM._deviance([(v["49_51"][0], v["49_51"][2]) for v in cells.values()])
    da = LM._deviance([(v["49_51"][1], v["49_51"][2]) for v in cells.values()])
    worse = sorted(f"{k[0]}; {BIN_NAMES[k[1]]} votes; {c}" for k, v in cells.items() for c in COUNTS
                   if max(v[c][0], v[c][2]) >= CELL_MIN and abs(v[c][1] - v[c][2]) > abs(v[c][0] - v[c][2]))
    improves = abs(tot[1] - tot[2]) < abs(tot[0] - tot[2]) and da < db
    return {"years": sorted(years), "contests": n, "contests_with_their_own_bin": own,
            "seen_49_51": int(tot[2]), "expected_49_51_record": round(tot[0], 1),
            "expected_49_51_variant": round(tot[1], 1), "deviance_record": round(db, 2),
            "deviance_variant": round(da, 2), "improves": improves, "tested_cells_made_worse": worse,
            "passes": improves and not worse,
            "by_size_bin": {BIN_NAMES[b]: {c: {"record": round(v[c][0], 1), "variant": round(v[c][1], 1),
                                               "seen": int(v[c][2])} for c in COUNTS} for b, v in sorted(bins.items())},
            "tested_cells": sum(1 for v in cells.values() for c in COUNTS if max(v[c][0], v[c][2]) >= CELL_MIN)}


def test(recs):
    years = sorted({r["year"] for r in recs})
    all_ = _score(recs, set(years))
    loo = {}
    for t in years:
        if len(years) == 1:
            loo[str(t)] = {"passes": False, "why": f"no scored year is left: the only scored year is {t}"}
            continue
        x = _score(recs, set(years) - {t})
        loo[str(t)] = {k: x[k] for k in ("expected_49_51_record", "expected_49_51_variant", "seen_49_51",
                                         "deviance_record", "deviance_variant", "improves", "tested_cells_made_worse",
                                         "passes")}
    fails = sorted(t for t, v in loo.items() if not v["passes"])
    return {"test": all_, "leave_one_year_out": loo, "fails_without": fails,
            "adopted": all_["passes"] and not fails}


def pool_legislatures():
    crow = L.class_rows(L.load_klarner())
    scored = [r for r in crow if "seats at once" in r["key"]]
    recs = _forecast(scored, lambda t: [r for r in crow if r["year"] < t])
    # MEDSL's 2024 legislature: the contests the files give a boundary forecast, from Klarner's 1967-2022
    rows24 = []
    for path in glob.glob(os.path.join(L.REPO, "data", "state-*", "2024", "*.json")):
        with open(path) as f:
            for c in json.load(f)["contests"]:
                fc = (c.get("forecasts") or [{}])[-1]
                if fc.get("route") == "boundary" and c.get("boundary"):
                    v = c["boundary"]["votes"]
                    rows24.append({"year": 2024, "key": fc["class"], "s": max(v) / sum(v), "n": sum(v)})
    recs += _forecast(rows24, lambda t: crow)
    return recs


def pool_medsl_local():
    m = {y: LM.load(y) for y in LM.YEARS}
    bad = {y: LM.quality(y) for y in LM.YEARS}
    for y, sts in LM.CERTIFIED_STATES.items():
        for st in sts:
            bad.get(y, {}).pop(st, None)
    lrows = {y: LM.local_rows([c for c in m[y] if c["state"] not in bad[y]]) for y in LM.YEARS}
    for y, rs in lrows.items():
        for r in rs:
            r["year"] = y
    allrows = [r for rs in lrows.values() for r in rs]
    scored = [r for r in allrows if r["route"] == "boundary"]
    return _forecast(scored, lambda t: [r for r in allrows if r["year"] < t])


def pool_ncsbe():
    import local_ncsbe as NS
    dates = NS.load_dates()
    NS.split_party(dates)
    NS.classify(dates)
    rows = NS.like_rows(dates)
    scored = [r for r in rows if r["route"] == "boundary"]
    return _forecast(scored, lambda t: [r for r in rows if r["year"] < t])


def main():
    out = {"about": "the robustness test of route (c), the boundary route, by size (data/local/REPORT.md section 11, "
                    "fixed 2026-11-07 10:10 UTC before any score): the class density from the same size bin of the "
                    "deciding pair's votes against the record's class density, each pool apart, each year forecast "
                    "from the pool's earlier years only. Built by pipeline/local_sizebins.py.",
           "written_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
           "method": L.METHOD, "commit": L.git_commit(), "bins": BIN_NAMES, "cell_min": CELL_MIN, "pools": {}}
    for name, fn in (("legislatures", pool_legislatures), ("medsl local", pool_medsl_local), ("ncsbe", pool_ncsbe)):
        recs = fn()
        out["pools"][name] = test(recs)
        t = out["pools"][name]
        print(name, json.dumps({k: t["test"][k] for k in ("contests", "contests_with_their_own_bin", "seen_49_51",
                                                          "expected_49_51_record", "expected_49_51_variant",
                                                          "deviance_record", "deviance_variant", "improves",
                                                          "passes")}), "fails without", t["fails_without"][:8],
              "adopted", t["adopted"])
    with open(os.path.join(L.REPO, "data", "local", "size-bins-test.json"), "w") as f:
        json.dump(out, f, indent=1)
        f.write("\n")


if __name__ == "__main__":
    main()
