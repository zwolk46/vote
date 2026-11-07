"""pipeline/intake/medsl_county_precincts.py: how many precincts each county has in MEDSL's precinct files, so that a
county's own question can be checked to cover the county's whole file.

Written 2026-11-07 by worker D3, on the orchestrator's word of 15:43 UTC: a county's or parish's own question is
counted whole only if "the title names the record's own county or parish", it "has no words of another body", and
"the record covers that county's whole file". Reason (the orchestrator): "every voter on a county's own question is
in that county"; the third test makes sure that the record is the question's whole count in MEDSL's file, not part.

It reads the raw files already in the cache (pipeline/intake/medsl_precinct.py fetched them; nothing is downloaded),
with that script's own reader (_rows) and precinct key, so that the counts are counted the same way as a contest's
`precincts`:
  2016   (the older sets, read for their questions only): a contest's precincts are every precinct key on its rows,
         so a county's are every key on any general-election row of the same file in that county.
  2018-  a contest's precincts are those with a vote in it, so a county's are those with a vote in any contest on
         that date in that county.
The precinct key is (county FIPS, jurisdiction, precinct), as medsl_precinct.py's.

Writes $VOTE_CACHE/medsl/normalized/county-precincts-<year>.json: {"counts": {"<file>|<state>|<date>|<county>": n},
"files": [names read]}.
Run:  VOTE_CACHE=/tmp/vote-cache python3 pipeline/intake/medsl_county_precincts.py 2016 2018 2020 2024
"""
import collections
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import fetch as F  # noqa: E402
import medsl_precinct as MP  # noqa: E402

NORM = os.path.join(F.CACHE, "medsl", "normalized")
RAW = os.path.join(F.CACHE, "medsl", "raw")


def _raw_path(year, name):
    hits = [p for p in glob.glob(os.path.join(RAW, f"{year}-*-{name}")) if not p.endswith(".meta.json")]
    if len(hits) != 1:
        raise SystemExit(f"county_precincts: {year} {name}: {len(hits)} raw files in the cache, not one")
    return hits[0]


def count(year):
    if year == 2016:
        names = [n for _, n, _, _, _ in MP.SETS_2016]
    else:
        with open(os.path.join(NORM, f"checks-{year}.json")) as f:
            names = sorted(json.load(f)["files"])
    seen = collections.defaultdict(set)
    for name in names:
        path = _raw_path(year, name)
        for row in MP._rows(path):
            if MP.is_meta((row.get("candidate") or "").strip()):
                continue
            county = MP.fips5(row.get("county_fips", ""))
            if year == 2016:
                if (row.get("stage") or "").upper() != "GEN":
                    continue
                st, date = row.get("state_postal", ""), "2016-11-08"
                pk = (county, row.get("jurisdiction", ""), row.get("precinct", ""))
            else:
                try:
                    if int(float(row.get("votes") or "")) <= 0:
                        continue
                except ValueError:
                    continue
                st, date = row.get("state_po", ""), row.get("date", "")
                pk = (county, row.get("jurisdiction_fips", ""), row.get("precinct", ""))
            seen[f"{name}|{st}|{date}|{county}"].add(pk)
        print(f"{year} {name}: read", flush=True)
    out = {"year": year, "files": names, "counts": {k: len(v) for k, v in sorted(seen.items())}}
    with open(os.path.join(NORM, f"county-precincts-{year}.json"), "w") as f:
        json.dump(out, f, indent=0)
    print(f"{year}: {len(out['counts'])} counties written")


if __name__ == "__main__":
    for y in sys.argv[1:]:
        count(int(y))
