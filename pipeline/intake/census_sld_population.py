"""pipeline/intake/census_sld_population.py: the 2020 Census population of each state legislative district, upper
and lower chamber, on the lines of the 2024 election cycle (and of 2022), from the Census Bureau's own tabulation.

Written 2026-11-07 by worker D2, on the orchestrator's word of 11:39 UTC: "add each 2024 state legislative district's
population from the Census Bureau, by script ... the 2020 Census counts tabulated to those lines, or ACS 5-year totals
on them." Reason (the orchestrator): the site divides B* among the people a seat serves, and law 8 says every figure
comes from a named true source.

Sources. U.S. Census Bureau, 2020 Census, a work of the U.S. Government (17 U.S.C. 105; no licence printed):
  cd119  the 119th Congressional District Summary File (CD119), v. 2024-12-05,
         https://www2.census.gov/programs-surveys/decennial/2020/data/119th-congressional-district-summary-file/
         <State_Name>/<st>2020.cd19.zip. Its state legislative districts are the "Current State Legislative Districts
         (SLDs) (2024 Election Cycle)": "States participating in Phase 4 of the 2020 Census Redistricting Data Program
         voluntarily provided the Census Bureau with the 2024 election cycle boundaries ... All 50 states, plus the
         District of Columbia and Puerto Rico, participated" (its technical documentation, appendix A, A-21).
  cd118  the 118th Congressional District Summary File (CD118), v. 2023-08-31, the same layout, .../118th-congressional-
         district-summary-file/<State_Name>/<st>2020.cd18.zip, whose SLDs are those of the 2022 election cycle.
Why the census counts and not ACS 5-year totals: they are the full count, with no sampling error, where ACS totals
are survey estimates with a margin of error; they are the counts the 2020-cycle plans were drawn from; and the Bureau
tabulates them to each cycle's own lines in every state, as its technical documentation states.

What is read. Only the geographic header file of each state's zip (<st>geo2020.cd19 or .cd18; pipe-delimited, UTF-8,
the 97 fields of the 2020 Census geographic header, GEO_FIELDS below), whose POP100 is the "Population Count (100%)"
of each record. Summary level 040 is the state; 610 a state legislative district (upper chamber); 620 one of the
lower chamber. Only the whole-district records are kept (GEOCOMP 00). Code ZZZ is "districts not defined" (water,
usually), kept and marked. Nothing is apportioned: each figure is the Bureau's own count for that district.

Checks: each chamber's districts sum to the state's POP100 exactly, or the script stops.

Run from the repository root:  python3 pipeline/intake/census_sld_population.py [cd119] [cd118]  (default: both)
Writes CACHE/census/normalized/sld_population_<product>.json:
  {"product", "title", "states": {"NH": {"population", "upper": [{"code", "basename", "name", "lsadc",
   "population"}], "lower": [...]}}, "files": {"NH": {url, path, bytes, sha256, read_utc}}}
"""
import json
import os
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import congress_common as cc  # noqa: E402

PRODUCTS = {
    "cd119": {"dir": "119th-congressional-district-summary-file", "ext": "cd19", "sld": "24", "cycle": 2024,
              "title": "U.S. Census Bureau, 2020 Census 119th Congressional District Summary File (CD119), v. "
                       "2024-12-05: the geographic header's POP100 for state legislative districts of the 2024 "
                       "election cycle (summary levels 610 and 620)",
              "techdoc": "https://www2.census.gov/programs-surveys/decennial/2020/technical-documentation/"
                         "complete-tech-docs/119th-congressional-district-summary-file/"
                         "2020census-119thcongressional-districts-techdoc.pdf"},
    "cd118": {"dir": "118th-congressional-district-summary-file", "ext": "cd18", "sld": "22", "cycle": 2022,
              "title": "U.S. Census Bureau, 2020 Census 118th Congressional District Summary File (CD118), v. "
                       "2023-08-31: the geographic header's POP100 for state legislative districts of the 2022 "
                       "election cycle (summary levels 610 and 620)",
              "techdoc": "https://www2.census.gov/programs-surveys/decennial/2020/technical-documentation/"
                         "complete-tech-docs/118th-congressional-district-summary-file/"
                         "2020census-118thcongressional-districts-techdoc.pdf"},
}
BASE = "https://www2.census.gov/programs-surveys/decennial/2020/data/"
LICENCE = "a work of the U.S. Government (17 U.S.C. 105); no licence printed"
# The 2020 Census geographic header, field for field (CD119 technical documentation, chapter 3); checked below
# against each file's own field count
GEO_FIELDS = (
    "FILEID STUSAB SUMLEV GEOVAR GEOCOMP CHARITER CIFSN LOGRECNO GEOID GEOCODE REGION DIVISION STATE STATENS COUNTY "
    "COUNTYCC COUNTYNS COUSUB COUSUBCC COUSUBNS SUBMCD SUBMCDCC SUBMCDNS ESTATE ESTATECC ESTATENS CONCIT CONCITCC "
    "CONCITNS PLACE PLACECC PLACENS TRACT BLKGRP BLOCK AIANHH AIHHTLI AIANHHFP AIANHHCC AIANHHNS AITS AITSFP AITSCC "
    "AITSNS TTRACT TBLKGRP ANRC ANRCCC ANRCNS CBSA MEMI CSA METDIV NECTA NMEMI CNECTA NECTADIV CBSAPCI NECTAPCI UA "
    "UATYPE UR CD116 CD118 CD119 CD120 CD121 SLDU18 SLDU22 SLDU24 SLDU26 SLDU28 SLDL18 SLDL22 SLDL24 SLDL26 SLDL28 "
    "VTD VTDI ZCTA SDELM SDSEC SDUNI PUMA AREALAND AREAWATR BASENAME NAME FUNCSTAT GCUNI POP100 HU100 INTPTLAT "
    "INTPTLON LSADC PARTFLAG UGA").split()
# the 50 states: the Bureau's directory name for each
STATES = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California", "CO": "Colorado",
    "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
    "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana",
    "ME": "Maine", "MD": "Maryland", "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi",
    "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New_Hampshire", "NJ": "New_Jersey",
    "NM": "New_Mexico", "NY": "New_York", "NC": "North_Carolina", "ND": "North_Dakota", "OH": "Ohio",
    "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode_Island", "SC": "South_Carolina",
    "SD": "South_Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont", "VA": "Virginia",
    "WA": "Washington", "WV": "West_Virginia", "WI": "Wisconsin", "WY": "Wyoming"}


def read_state(product, st):
    """The state's POP100 and its upper- and lower-chamber districts, from its geographic header."""
    P = PRODUCTS[product]
    rec = cc.fetch(f"{BASE}{P['dir']}/{STATES[st]}/{st.lower()}2020.{P['ext']}.zip",
                   f"census/{product}/{st.lower()}2020.{P['ext']}.zip", min_bytes=1_000_000)
    member = f"{st.lower()}geo2020.{P['ext']}"
    out = {"population": None, "upper": [], "lower": []}
    with zipfile.ZipFile(os.path.join(cc.CACHE, rec["path"])) as z:
        with z.open(member) as f:
            for raw in f:
                try:
                    line = raw.decode("utf-8")
                except UnicodeDecodeError:
                    # the README says UTF-8, but some names are in Latin-1 (Arizona's "ñ" is the byte 0xf1);
                    # only names are affected, never a count
                    line = raw.decode("latin-1")
                    out["latin1_lines"] = out.get("latin1_lines", 0) + 1
                v = line.rstrip("\r\n").split("|")
                if len(v) != len(GEO_FIELDS):
                    raise SystemExit(f"{member}: {len(v)} fields, the layout has {len(GEO_FIELDS)}")
                g = dict(zip(GEO_FIELDS, v))
                if g["STUSAB"] != st:
                    raise SystemExit(f"{member}: a record of {g['STUSAB']}")
                if g["GEOCOMP"] != "00":
                    continue
                if g["SUMLEV"] == "040":
                    out["population"] = int(g["POP100"])
                elif g["SUMLEV"] in ("610", "620"):
                    ch = "upper" if g["SUMLEV"] == "610" else "lower"
                    code = g[("SLDU" if ch == "upper" else "SLDL") + P["sld"]]
                    out[ch].append({"code": code, "basename": g["BASENAME"], "name": g["NAME"],
                                    "lsadc": g["LSADC"], "geoid": g["GEOID"], "population": int(g["POP100"])})
    for ch in ("upper", "lower"):
        if out[ch]:
            s = sum(d["population"] for d in out[ch])
            if s != out["population"]:
                raise SystemExit(f"{product} {st} {ch}: districts sum to {s}, the state is {out['population']}")
            codes = [d["code"] for d in out[ch]]
            if len(set(codes)) != len(codes) or not all(codes):
                raise SystemExit(f"{product} {st} {ch}: codes missing or repeated")
    return out, rec


def main(argv):
    for product in (argv or ["cd119", "cd118"]):
        P = PRODUCTS[product]
        res = {"product": product, "title": P["title"], "techdoc": P["techdoc"], "cycle": P["cycle"],
               "licence": LICENCE, "states": {}, "files": {}}
        for st in STATES:
            res["states"][st], res["files"][st] = read_state(product, st)
            s = res["states"][st]
            print(f"{product} {st}: population {s['population']:,}; {len(s['upper'])} upper, {len(s['lower'])} lower "
                  f"(ZZZ included)", flush=True)
        cc.write_json(os.path.join(cc.CACHE, "census", "normalized", f"sld_population_{product}.json"), res)


if __name__ == "__main__":
    main(sys.argv[1:])
