"""pipeline/intake/census_acs_population.py: population of each state and congressional district, from
the Census Bureau's American Community Survey 1-year estimates, table B01003 (Total Population).

Source. U.S. Census Bureau, American Community Survey 1-year estimates, table-based summary file,
https://www2.census.gov/programs-surveys/acs/summary_file/<year>/table-based-SF/data/1YRData/
acsdt1y<year>-b01003.dat (pipe-delimited: GEO_ID | B01003_E001 estimate | B01003_M001 margin of error).
A federal public record; no licence printed. The Census API (api.census.gov) now refuses requests
without a key (it redirects to missing_key.html, read 2026-11-07); this file server needs none.

Which estimate serves which election: the ACS year of the election, whose congressional districts are
those elected that year (ACS 2024 holds the 119th Congress's districts, 5001900US; ACS 2022 the 118th's,
5001800US). GEO_ID: 0400000US<state FIPS> for a state; 50019 00US<state FIPS><district> for a
district, district 00 at large and 98 for the District of Columbia's delegate.

Run:  python3 pipeline/intake/census_acs_population.py [year ...]   (default 2024 2022)
Writes CACHE/census/normalized/population_<year>.json: {"states": {"AL": {"value", "moe"}}, "districts":
{"AL-01": {...}}, "source": {...}}. Checks: 50 states and DC; 435 districts plus DC and Puerto Rico;
districts of a state sum to the state's estimate within the margins.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import congress_common as cc  # noqa: E402

URL = "https://www2.census.gov/programs-surveys/acs/summary_file/{y}/table-based-SF/data/1YRData/acsdt1y{y}-b01003.dat"
LICENCE = "US federal public record (Census Bureau); no licence printed"
# Census Bureau state FIPS codes (ANSI INCITS 38)
FIPS = {"01": "AL", "02": "AK", "04": "AZ", "05": "AR", "06": "CA", "08": "CO", "09": "CT", "10": "DE", "11": "DC",
        "12": "FL", "13": "GA", "15": "HI", "16": "ID", "17": "IL", "18": "IN", "19": "IA", "20": "KS", "21": "KY",
        "22": "LA", "23": "ME", "24": "MD", "25": "MA", "26": "MI", "27": "MN", "28": "MS", "29": "MO", "30": "MT",
        "31": "NE", "32": "NV", "33": "NH", "34": "NJ", "35": "NM", "36": "NY", "37": "NC", "38": "ND", "39": "OH",
        "40": "OK", "41": "OR", "42": "PA", "44": "RI", "45": "SC", "46": "SD", "47": "TN", "48": "TX", "49": "UT",
        "50": "VT", "51": "VA", "53": "WA", "54": "WV", "55": "WI", "56": "WY", "72": "PR"}


def parse(year):
    rec = cc.fetch(URL.format(y=year), f"census/acsdt1y{year}-b01003.dat", min_bytes=50000)
    states, districts = {}, {}
    with open(os.path.join(cc.CACHE, rec["path"])) as f:
        head = f.readline().strip().split("|")
        assert head[:2] == ["GEO_ID", "B01003_E001"], head
        for line in f:
            g, e, m = line.strip().split("|")[:3]
            if g.startswith("0400000US") and g[9:11] in FIPS:
                states[FIPS[g[9:11]]] = {"value": int(e), "moe": int(m) if m.lstrip("-").isdigit() and int(m) >= 0 else None}
            elif g.startswith("500") and g[5:9] == "00US" and g[9:11] in FIPS:
                st, dd = FIPS[g[9:11]], g[11:13]
                key = f"{st}-{'AL' if dd in ('00', '98') else dd}"
                districts[key] = {"value": int(e), "moe": int(m) if m.lstrip("-").isdigit() and int(m) >= 0 else None,
                                  "congress": int(g[3:5]) + 100 if g[3:5].isdigit() else None}
    checks = []
    if len([s for s in states if s != "PR"]) != 51:
        checks.append(f"{len(states)} states and territories, not 51 plus Puerto Rico")
    n_cd = len([k for k in districts if not k.startswith(("DC", "PR"))])
    if n_cd != 435:
        checks.append(f"{n_cd} districts, not 435")
    for st, v in states.items():
        ds = [x["value"] for k, x in districts.items() if k.startswith(st + "-")]
        if ds and abs(sum(ds) - v["value"]) > max(1000, 0.005 * v["value"]):
            checks.append(f"{st}: districts sum to {sum(ds):,}, the state estimate is {v['value']:,}")
    src = cc.source_block(f"U.S. Census Bureau, American Community Survey {year} 1-year estimates, table B01003 "
                          f"Total Population", rec["url"], rec["read_utc"], LICENCE, mark="stated",
                          note=f"a survey estimate with a 90% margin of error (moe); sha256 {rec['sha256'][:16]}")
    out = {"year": year, "states": states, "districts": districts, "source": src, "checks": checks}
    cc.write_json(os.path.join(cc.CACHE, "census", "normalized", f"population_{year}.json"), out)
    print(f"ACS {year}: {len(states)} states, {len(districts)} districts; checks: {checks or 'all pass'}")
    return out


if __name__ == "__main__":
    for y in [int(a) for a in sys.argv[1:]] or [2024, 2022]:
        parse(y)
