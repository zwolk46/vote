"""Intake: FiveThirtyEight's presidential general-election polling averages, national and by state, 1976-2024.

Written 2026-11-07 by worker D1 (briefs/D1-data-president.md; plan/PLAN.md section 3a).

Why: the model's own forecast, for years with no published forecast, is built like Gelman, King and
Boscardin's from "variables known before the election such as the polls two months out" (model/MODEL.md
section 3, "Which forecast"). These are the polls, as averaged by 538.

Sources, both from github.com/fivethirtyeight/data at the commit 4c1ff5e3aef1816ae04af63218015066e186c147
(2025-02-25), licence CC BY 4.0 (the repository's LICENSE file):
  polls/pres_pollaverages_1968-2016.csv  538's averages for 1968-2016 ("full archive 1968-2016"), daily;
      538 computed these afterwards from the polls of each year, so the information is of the time and the
      averaging is later.
  polls/2024-averages/presidential_general_averages_2024-09-12_uncorrected.csv  538's averages for 2020
      (to 3 November) and 2024 (1 March to 12 September 2024). 538's README: a bug "was overestimating Vice
      President Kamala Harris's margin over former President Donald Trump by 0.1 percentage points" from
      23 August to 12 September 2024; the corrected file is at projects.fivethirtyeight.com, which now
      redirects to ABC News and cannot be read. This uncorrected copy is the only one here, and is marked so.

What it writes: data/president/inputs/fte_poll_averages.json, for each cycle 1976-2024, the averages on
9 September (about eight weeks before the election, the first date the 1968-2016 file has in every
cycle, and a date the 2024 file covers) and on the last date in the file (election day, except 2024):
for the nation and each state 538 averaged, the Democratic and Republican nominees' percent, from the
column pct_estimate, and pct_trend_adjusted beside it where the file has it (2020 has only the latter).

Checks: every cycle has a national average on both dates; the nominees are matched by surname to the
Democratic and Republican nominees in MEDSL's returns (data/president/inputs/medsl_president.json), and
the script stops if a cycle has no match or two.

Run from the repository root:  python3 pipeline/intake/fte_poll_averages.py
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
OUT = os.path.join(ROOT, "data", "president", "inputs", "fte_poll_averages.json")
MEDSL = os.path.join(ROOT, "data", "president", "inputs", "medsl_president.json")
COMMIT = "4c1ff5e3aef1816ae04af63218015066e186c147"
RAW = f"https://raw.githubusercontent.com/fivethirtyeight/data/{COMMIT}/"
FILES = {"old": "polls/pres_pollaverages_1968-2016.csv",
         "new": "polls/2024-averages/presidential_general_averages_2024-09-12_uncorrected.csv"}
NAMES = {"Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA", "Colorado": "CO",
         "Connecticut": "CT", "Delaware": "DE", "District of Columbia": "DC", "Florida": "FL", "Georgia": "GA",
         "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
         "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA",
         "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO", "Montana": "MT",
         "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM",
         "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
         "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
         "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
         "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY",
         "National": "US", "ME-1": "ME-1", "ME-2": "ME-2", "NE-1": "NE-1", "NE-2": "NE-2", "NE-3": "NE-3"}


def iso(d):
    """'9/9/2016' -> '2016-09-09'; ISO dates pass through."""
    if "/" in d:
        m, dd, y = d.split("/")
        return f"{y}-{int(m):02d}-{int(dd):02d}"
    return d


def surname(name):
    parts = [p for p in name.replace(",", " ").split() if p.rstrip(".").lower() not in ("jr", "sr", "ii", "iii")]
    return parts[-1].lower()


def num(s):
    return float(s) if s not in ("", None) else None


def main():
    medsl = json.load(open(MEDSL))["years"]
    nominees = {y: (medsl[y]["PA"]["dem"]["name"].split(",")[0].lower(),
                    medsl[y]["PA"]["rep"]["name"].split(",")[0].lower()) for y in medsl}
    rows = []
    for key, rel in FILES.items():
        name = f"fte_data_{COMMIT[:7]}_{rel.split('/')[-1]}"
        path = fetch.fetch(RAW + rel, name)
        for r in csv.DictReader(open(path, encoding="utf-8")):
            if key == "old" and not r["modeldate"]:     # 132 rows of 1972 carry no date; 1972 is not used
                continue
            rows.append({"cycle": r["cycle"], "state": r["state"], "date": iso(r.get("modeldate") or r["date"]),
                         "candidate": r.get("candidate_name") or r["candidate"],
                         "pct_estimate": num(r.get("pct_estimate")),
                         "pct_trend_adjusted": num(r.get("pct_trend_adjusted")), "file": key})
    by = collections.defaultdict(list)
    for r in rows:
        if r["cycle"] in nominees:
            by[r["cycle"]].append(r)
    out = {}
    for y in sorted(by):
        rs = by[y]
        dname, rname = nominees[y]
        cands = {r["candidate"] for r in rs}
        dm = [c for c in cands if surname(c) == dname]
        rm = [c for c in cands if surname(c) == rname]
        assert len(dm) == 1 and len(rm) == 1, (y, dname, rname, sorted(cands))
        dates = {r["date"] for r in rs if r["state"] == "National"}
        ref = f"{y}-09-09"
        assert ref in dates, (y, min(dates))
        snaps = {}
        for label, date in (("two_months_out", ref), ("last", max(dates))):
            units = {}
            for r in rs:
                if r["date"] != date or r["candidate"] not in (dm[0], rm[0]):
                    continue
                code = NAMES.get(r["state"], r["state"])
                u = units.setdefault(code, {})
                side = "dem" if r["candidate"] == dm[0] else "rep"
                u[side] = r["pct_estimate"]
                u[side + "_trend_adjusted"] = r["pct_trend_adjusted"]
            units = {k: v for k, v in units.items() if "dem" in v and "rep" in v}
            assert "US" in units, (y, label)
            snaps[label] = {"date": date, "units": dict(sorted(units.items()))}
        out[y] = {"dem": dm[0], "rep": rm[0], "file": rs[0]["file"], **snaps}
        us = snaps["two_months_out"]["units"]["US"]
        d, r_ = us["dem"] if us["dem"] is not None else us["dem_trend_adjusted"], \
            us["rep"] if us["rep"] is not None else us["rep_trend_adjusted"]
        print(f"{y}: {dm[0]} {d:.1f}, {rm[0]} {r_:.1f} nationally on {ref};"
              f" {len(snaps['two_months_out']['units']) - 1} states averaged then; last date {snaps['last']['date']}")
    sources = {}
    for key, rel in FILES.items():
        m = fetch.meta(f"fte_data_{COMMIT[:7]}_{rel.split('/')[-1]}")
        note = ("538's averages computed afterwards from each year's polls" if key == "old" else
                "the uncorrected copy: 538 says its averages overstated Harris's margin by 0.1 points from "
                "23 August to 12 September 2024; the corrected file is not reachable")
        sources[key] = fetch.source(f"FiveThirtyEight, data repository, {rel} (commit {COMMIT[:7]})", m["url"],
                                    m["read_utc"], "CC BY 4.0", "stated", note=note, sha256=m["sha256"])
    doc = {"about": "538's presidential polling averages on 9 September and on the last date, normalised by "
                    "pipeline/intake/fte_poll_averages.py. dem and rep are percent of the whole vote "
                    "(pct_estimate); the _trend_adjusted columns are 538's trend-adjusted estimates.",
           "sources": sources, "years": out}
    with open(OUT, "w") as f:
        json.dump(doc, f, indent=1)
        f.write("\n")
    print(f"wrote {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
