"""Intake: U.S. Census Bureau, resident population of each state (and DC, and the nation), presidential years 1976-2024.

Written 2026-11-07 by worker D1 (briefs/D1-data-president.md; plan/PLAN.md section 3a).

Why: B* per person divides by a population (the brief names state population; the law's per-person reading
names the jurisdiction the office serves, which for the presidency is the nation). Both are written.

Sources, all from the Census Bureau's Population Estimates Program at www2.census.gov, each the estimate
for 1 July of the election year unless marked (a work of the U.S. Government, 17 U.S.C. 105, no copyright):
  1976        e7080sta.txt, "Intercensal Estimates of the Resident Population of States, 1970 to 1980":
              23 age lines per state, summed here (the file prints no state total).
  1980-1988   st8090ts.txt, "Intercensal Estimates of the Total Resident Population of States: 1980 to
              1990"; 1980 is the census count of 1 April 1980 (the file has no July 1980 column).
  1992, 1996  st-99-03.txt, "ST-99-3 State Population Estimates: Annual Time Series, July 1, 1990 to July 1,
              1999" (postcensal, vintage 1999).
  2000-2008   st-est00int-alldata.csv, intercensal estimates 2000-2010, the all-ages, all-races row.
  2012, 2016  nst-est2020-alldata.csv, vintage 2020 estimates 2010-2020 (postcensal).
  2020, 2024  NST-EST2024-ALLDATA.csv, vintage 2024 estimates 2020-2024 (postcensal).

Checks: 51 jurisdictions each year; where the file prints a national total, the states sum to it (exactly,
or the difference is printed and stops the script if over 0.01%); 1976 is the sum of the state lines.

Writes data/president/inputs/census_population.json: {year: {state: population, "US": population}}.
Run from the repository root:  python3 pipeline/intake/census_population.py
"""
import csv
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import fetch  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "data", "president", "inputs", "census_population.json")
BASE = "https://www2.census.gov/programs-surveys/popest/"
FILES = {
    "e7080sta.txt": BASE + "tables/1900-1980/state/asrh/e7080sta.txt",
    "st8090ts.txt": BASE + "tables/1980-1990/state/asrh/st8090ts.txt",
    "st-99-03.txt": BASE + "tables/1990-2000/state/totals/st-99-03.txt",
    "st-est00int-alldata.csv": BASE + "datasets/2000-2010/intercensal/state/st-est00int-alldata.csv",
    "nst-est2020-alldata.csv": BASE + "datasets/2010-2020/state/totals/nst-est2020-alldata.csv",
    "NST-EST2024-ALLDATA.csv": BASE + "datasets/2020-2024/state/totals/NST-EST2024-ALLDATA.csv",
}
TITLES = {
    "e7080sta.txt": "Intercensal Estimates of the Resident Population of States, 1970 to 1980 (e7080sta.txt)",
    "st8090ts.txt": "Intercensal Estimates of the Total Resident Population of States: 1980 to 1990 (st8090ts.txt)",
    "st-99-03.txt": "ST-99-3 State Population Estimates: Annual Time Series, July 1, 1990 to July 1, 1999",
    "st-est00int-alldata.csv": "Intercensal Estimates of the Resident Population of States, 2000-2010",
    "nst-est2020-alldata.csv": "Annual Estimates of the Resident Population of States, 2010-2020 (vintage 2020)",
    "NST-EST2024-ALLDATA.csv": "Annual Estimates of the Resident Population of States, 2020-2024 (vintage 2024)",
}
NAMES = {"Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA", "Colorado": "CO",
         "Connecticut": "CT", "Delaware": "DE", "District of Columbia": "DC", "Florida": "FL", "Georgia": "GA",
         "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
         "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA",
         "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO", "Montana": "MT",
         "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM",
         "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
         "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
         "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
         "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"}
CODES = set(NAMES.values())


DIFFS = {}


def check(y, states, us):
    """The states sum to the printed national total; a difference (the file's own rounding) is kept and printed."""
    d = sum(states.values()) - us
    assert abs(d) <= 1e-4 * us, (y, sum(states.values()), us)
    if d:
        DIFFS[y] = d
        print(f"  {y}: the states sum to {sum(states.values()):,}, the file prints {us:,} for the nation"
              f" (difference {d:+,}); the printed national figure is kept")


def path(name):
    return fetch.fetch(FILES[name], "census_" + name)


def y1976():
    tot = {}
    for line in open(path("e7080sta.txt"), encoding="latin-1"):
        m = re.match(r"^\s*\d+\s+([A-Z]{2})\s+\S+\s+((?:\d+\s+){10}\d+)\s*$", line)
        if m and m.group(1) in CODES:
            vals = [int(v) for v in m.group(2).split()]       # 4/1/70, 7/1/71 ... 7/1/79, 4/1/80
            tot[m.group(1)] = tot.get(m.group(1), 0) + vals[6]  # 7/1/76
    assert set(tot) == CODES, sorted(CODES - set(tot))
    tot["US"] = sum(tot.values())
    return {1976: tot}, "7/1/76; the sum of each state's 23 age lines; US is the sum of the states and DC"


def y1980s():
    out = {1980: {}, 1984: {}, 1988: {}}
    cols = None
    for line in open(path("st8090ts.txt"), encoding="latin-1"):
        if re.match(r"^\s+(4/80cen|7/85)", line):
            cols = line.split()
            continue
        m = re.match(r"^([A-Z]{2})\s+([\d\s]+)$", line.rstrip())
        if m and cols:
            vals = dict(zip(cols, (int(v) for v in m.group(2).split())))
            for y, c in ((1980, "4/80cen"), (1984, "7/84"), (1988, "7/88")):
                if c in vals:
                    out[y][m.group(1)] = vals[c]
    for y in out:
        us = out[y].pop("US")
        assert set(out[y]) == CODES, (y, sorted(CODES - set(out[y])))
        check(y, out[y], us)
        out[y]["US"] = us
    return out, "1980: the census count of 1 April 1980; 1984 and 1988: 1 July"


def y1990s():
    out = {1992: {}, 1996: {}}
    cols = None
    for line in open(path("st-99-03.txt"), encoding="latin-1"):
        if re.match(r"^\s+7/1/9\d", line):
            cols = line.split()
            continue
        m = re.match(r"^\s+\d\s+([A-Za-z .]+?)\s{2,}([\d\s]+)$", line.rstrip())
        if m and cols:
            name = m.group(1).strip()
            vals = dict(zip(cols, (int(v) for v in m.group(2).split())))
            code = "US" if name == "United States" else NAMES.get(name)
            for y, c in ((1992, "7/1/92"), (1996, "7/1/96")):
                if code and c in vals:
                    out[y][code] = vals[c]
    for y in out:
        us = out[y].pop("US")
        assert set(out[y]) == CODES, (y, sorted(CODES - set(out[y])))
        check(y, out[y], us)
        out[y]["US"] = us
    return out, "1 July"


def y_csv(name, years, filt):
    out = {y: {} for y in years}
    for r in csv.DictReader(open(path(name), encoding="latin-1")):
        if not filt(r):
            continue
        code = "US" if r["NAME"] == "United States" else NAMES.get(r["NAME"])
        if code:
            for y in years:
                out[y][code] = int(r[f"POPESTIMATE{y}"])
    for y in years:
        us = out[y].pop("US")
        assert set(out[y]) == CODES, (y, sorted(CODES - set(out[y])))
        check(y, out[y], us)
        out[y]["US"] = us
    return out, "1 July"


def main():
    parts = [
        ("e7080sta.txt",) + y1976(),
        ("st8090ts.txt",) + y1980s(),
        ("st-99-03.txt",) + y1990s(),
        ("st-est00int-alldata.csv",) + y_csv("st-est00int-alldata.csv", [2000, 2004, 2008],
                                             lambda r: r["SEX"] == "0" and r["ORIGIN"] == "0" and r["RACE"] == "0"
                                             and r["AGEGRP"] == "0"),
        ("nst-est2020-alldata.csv",) + y_csv("nst-est2020-alldata.csv", [2012, 2016],
                                             lambda r: r["SUMLEV"] in ("010", "040")),
        ("NST-EST2024-ALLDATA.csv",) + y_csv("NST-EST2024-ALLDATA.csv", [2020, 2024],
                                             lambda r: r["SUMLEV"] in ("010", "040")),
    ]
    doc = {"about": "U.S. Census Bureau resident population by state, normalised by "
                    "pipeline/intake/census_population.py. US is the nation (50 states and DC).",
           "years": {}, "sources": {}}
    for name, years, when in parts:
        m = fetch.meta("census_" + name)
        for y in sorted(years):
            doc["years"][str(y)] = years[y]
            doc["sources"][str(y)] = fetch.source(
                "U.S. Census Bureau, Population Estimates Program: " + TITLES[name], m["url"], m["read_utc"],
                "public domain (a work of the U.S. Government, 17 U.S.C. 105)", "stated", note=when,
                sha256=m["sha256"])
            if y in DIFFS:
                doc["sources"][str(y)]["note"] += (f"; the states sum to {DIFFS[y]:+,} from the printed national"
                                                   " total, which is kept as US")
            print(f"{y}: 51 jurisdictions, US {years[y]['US']:,} ({name})")
    doc["years"] = dict(sorted(doc["years"].items()))
    doc["sources"] = dict(sorted(doc["sources"].items()))
    with open(OUT, "w") as f:
        json.dump(doc, f, indent=1)
        f.write("\n")
    print(f"wrote {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
