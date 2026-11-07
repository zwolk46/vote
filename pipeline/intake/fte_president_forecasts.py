"""Intake: FiveThirtyEight's published presidential forecasts by state, 2008-2020, from "checking-our-work-data".

Written 2026-11-07 by worker D1 (briefs/D1-data-president.md; plan/PLAN.md section 3a).

Source: github.com/fivethirtyeight/checking-our-work-data, file presidential_elections.csv, read at the
commit f6d5b2e1d6da2889345d381c41431f9a4ee208dd (2023-02-02), the data behind 538's "How Good Are
FiveThirtyEight Forecasts?". Licence: CC BY 4.0 (the repository's LICENSE file, "Attribution 4.0
International"). Each row is one candidate in one state (or Maine or Nebraska district) on one forecast date,
with 538's projected vote share and chance of winning as published, and the outcome.

What the file holds, as measured on 2026-11-07:
  2008  one forecast date (election day), chance of winning only (no projected vote share);
  2012  daily from 2012-05-31, chance of winning only;
  2016  daily from 2016-06-08, three models: polls-plus, polls-only, now-cast; share and chance;
  2020  daily from 2020-08-12, polls-plus; share and chance.
  The 538 forecast pages and their own data files (projects.fivethirtyeight.com) now redirect to ABC News
  and cannot be read (research/decisiveness-models-v2.md section 1), so this file is the only copy here.

What it writes: data/president/inputs/fte_president_forecasts.json, the forecast of election day (the last
forecast date, which is election day in every year) for every unit and model: each candidate's projected
share (percent of the whole vote, as published) and chance of winning, and the outcome columns.
No figure is derived here; the sd that a share and a chance imply is computed, and marked inferred, in
pipeline/president.py.

Checks: the four years and the models above; 51 states and DC each year, plus the Maine and Nebraska
districts from 2012 (5 units); the forecast date of every kept row equals the election date; in each unit
the candidates' chances of winning sum to 1 within 0.001 (in the national row, "US", the remainder is
538's chance that no candidate wins a majority of electoral votes, 0.45% in 2020).

Run from the repository root:  python3 pipeline/intake/fte_president_forecasts.py
"""
import collections
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import fetch  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "data", "president", "inputs", "fte_president_forecasts.json")
COMMIT = "f6d5b2e1d6da2889345d381c41431f9a4ee208dd"
URL = f"https://raw.githubusercontent.com/fivethirtyeight/checking-our-work-data/{COMMIT}/presidential_elections.csv"
NAME = f"fte_checking-our-work_{COMMIT[:7]}_presidential_elections.csv"
EXPECT = {"2008": [""], "2012": [""], "2016": ["now-cast", "polls-only", "polls-plus"], "2020": ["polls-plus"]}


def num(s):
    return float(s) if s not in ("", None) else None


def main():
    path = fetch.fetch(URL, NAME)
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    by = collections.defaultdict(list)
    for r in rows:
        assert r["office"] == "President", r
        by[(r["year"], r["forecast_type"])].append(r)
    got = collections.defaultdict(list)
    for y, ft in by:
        got[y].append(ft)
    assert {y: sorted(v) for y, v in got.items()} == EXPECT, dict(got)

    out = {}
    for (y, ft), rs in sorted(by.items()):
        last = max(r["forecast_date"] for r in rs)
        assert last == rs[0]["election_date"], (y, ft, last)
        units = collections.OrderedDict()
        for r in rs:
            if r["forecast_date"] != last:
                continue
            d = r["district"]
            unit = r["state"] if d in ("", "0") else f"{r['state']}-{d}"
            units.setdefault(unit, []).append({
                "party": r["party"], "candidate": r["candidate"] or None,
                "projected_voteshare": num(r["projected_voteshare"]), "probwin": num(r["probwin"]),
                "actual_voteshare": num(r["actual_voteshare"]), "probwin_outcome": num(r["probwin_outcome"])})
        states = [u for u in units if "-" not in u and u != "US"]
        assert len(states) == 51, (y, ft, len(states))
        if y != "2008":
            assert sorted(u for u in units if "-" in u) == ["ME-1", "ME-2", "NE-1", "NE-2", "NE-3"], (y, ft)
        for u, cs in units.items():
            s = sum(c["probwin"] for c in cs)
            if u == "US":            # the national row: what is left is 538's chance that no one wins a majority
                assert 0.98 < s <= 1 + 1e-9, (y, ft, u, s)
                continue
            assert abs(s - 1) < 1e-3, (y, ft, u, s)
        out.setdefault(y, {})[ft or "published"] = {"forecast_date": last, "units": dict(sorted(units.items()))}
        print(f"{y} {ft or '(one model)'}: {len(units)} units on {last}"
              f" ({'with' if units[states[0]][0]['projected_voteshare'] is not None else 'without'} projected shares)")

    m = fetch.meta(NAME)
    doc = {"about": "FiveThirtyEight's published presidential forecasts on election day, by unit and model, "
                    "normalised by pipeline/intake/fte_president_forecasts.py. projected_voteshare is percent of the "
                    "whole vote as 538 published it; probwin is 538's chance that the candidate wins the unit.",
           "source": fetch.source("FiveThirtyEight, checking-our-work-data, presidential_elections.csv (commit "
                                  f"{COMMIT[:7]}, 2023-02-02)", URL, m["read_utc"], "CC BY 4.0", "stated",
                                  note="538's published forecasts as kept by 538 for its calibration page; the "
                                       "forecast pages themselves now redirect to ABC News",
                                  sha256=m["sha256"]),
           "years": out}
    with open(OUT, "w") as f:
        json.dump(doc, f, indent=1)
        f.write("\n")
    print(f"wrote {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
