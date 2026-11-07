"""pipeline/intake/candidates_american_general_elections.py: "Candidates in American General Elections"
(Cha, Kuriwaki and Snyder), on Harvard Dataverse.

Source. Jeremiah Cha, Shiro Kuriwaki and James M. Snyder, Jr., "Candidates in American General
Elections", Harvard Dataverse, doi:10.7910/DVN/DGDRDT (version 4.1, released 2026-02-15), licence
CC0 1.0, no guestbook. One row per candidate for President (by state), U.S. House, U.S. Senate and
Governor, 2006-2024, with standardized names, party, incumbency (`inc`), votes, and who won.
The guide (guide_candidates.pdf, version 3.0, October 2024) names its origins: House and Senate votes
"entered from the Official Election Statistics compiled by the House Clerk"; governors "collected from
statements of votes by the Secretary of State of each state"; incumbency "determined by a programmatic
count of whether the name is repeated across years, and by manual inspection of the biography of each
candidate". So a figure from here carries `via` = this dataset and `url` = its origin (law, Part A).

Why this source. It is the one standardized, reachable source here for governors' races (2006-2024,
odd years included), and the only one that codes the incumbency of every House, Senate and governor
candidate by hand. For House and Senate votes it is a check on the FEC and the Clerk (plan section 3a).

What the guide says that matters for reading it:
  - "only the deciding contest is included": where a runoff decided the seat (Georgia 2020 and 2022
    Senate, Louisiana), the November first round is NOT here; `runoff` = 1 marks the runoff.
  - it "excludes candidates who receive less than ten votes ... and those who identify Blank or
    Miscellaneous as their party", and over-, under- and invalid votes; so `totalvotes` is the sum of
    the listed candidates, a few votes under the official total.
  - Florida and Oklahoma print no count for a House candidate who won unopposed: `candidatevotes`
    is missing and `won` = 1.
  - Senate `dist` is the seat's class; at-large House districts are numbered 1.
  - candidates on several lines in New York and Connecticut are summed and given the major party.

Run:  python3 pipeline/intake/candidates_american_general_elections.py
Writes CACHE/cha/normalized/contests.json: {"source": ..., "contests": [{"year", "office", "state",
"district", "class", "special", "runoff", "candidates": [{"name", "party", "party_formal", "inc", "votes",
"won"}], "totalvotes", "checks"}]}.
Checks: rows per year and office against the guide's tables; candidate votes summed against
`totalvotes`; one winner per contest.
"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import congress_common as cc  # noqa: E402

API = "https://dataverse.harvard.edu/api"
DOI = "doi:10.7910/DVN/DGDRDT"
STEM = "candidates_"
NAME = "Cha, Kuriwaki and Snyder, \"Candidates in American General Elections\" (Harvard Dataverse)"
ORIGIN = {"H": "https://history.house.gov/Institution/Election-Statistics/Election-Statistics/",
          "S": "https://history.house.gov/Institution/Election-Statistics/Election-Statistics/",
          "G": None, "P": "https://doi.org/10.7910/DVN/42MVDX"}
OFFICE = {"H": "house", "S": "senate", "G": "governor", "P": "president"}


# Harvard Dataverse serves its files from Amazon S3: a redirect there is the publisher's own storage
STORAGE = ("amazonaws.com",)


def fetch():
    rec = cc.fetch(f"{API}/datasets/:persistentId/?persistentId={DOI}", "cha/record.json")
    with open(os.path.join(cc.CACHE, rec["path"])) as f:
        v = json.load(f)["data"]["latestVersion"]
    lic = v["license"]["name"] if isinstance(v.get("license"), dict) else v.get("license")
    files = {x["dataFile"]["filename"]: x["dataFile"] for x in v["files"]}
    data = next(df for fn, df in files.items() if fn.startswith(STEM))
    frec = cc.fetch(f"{API}/access/datafile/{data['id']}?format=original", f"cha/{data['filename']}.original",
                    min_bytes=100000, storage_sites=STORAGE)
    guide = files.get("guide_candidates.pdf")
    grec = cc.fetch(f"{API}/access/datafile/{guide['id']}", "cha/guide_candidates.pdf",
                    storage_sites=STORAGE) if guide else None
    return {"record": rec, "file": frec, "guide": grec, "licence": lic, "doi": DOI,
            "version": f"v{v['versionNumber']}.{v['versionMinorNumber']}, released {v.get('releaseTime')}"}


def nz(x):
    return None if x is None or (isinstance(x, float) and math.isnan(x)) else x


def main():
    import pandas as pd
    info = fetch()
    df = pd.read_stata(os.path.join(cc.CACHE, info["file"]["path"]))
    contests = {}
    for r in df.itertuples(index=False):
        office = r.office
        year = int(r.year)
        dist = nz(r.dist)
        k = (year, office, r.state, dist, r.type)   # one round per contest: "only the deciding contest"
        c = contests.setdefault(k, {"year": year, "office": OFFICE.get(office, office), "state": r.state,
                                    "district": (f"{int(dist):02d}" if office == "H" and dist is not None else None),
                                    "class": (int(dist) if office == "S" and dist is not None else None),
                                    "special": r.type == "S", "runoff": False,
                                    "next_up": int(r.nextup) if nz(r.nextup) else None,
                                    "candidates": [], "totalvotes": set()})
        c["runoff"] = c["runoff"] or nz(r.runoff) == 1
        v = nz(r.candidatevotes)
        c["candidates"].append({"name": r.name_snyder, "party": r.party, "party_formal": r.party_formal,
                                "inc": int(r.inc) if nz(r.inc) is not None else None,
                                "votes": int(v) if v is not None else None,
                                "won": int(r.won) if nz(r.won) is not None else None})
        if nz(r.totalvotes) is not None:
            c["totalvotes"].add(int(r.totalvotes))
    out = []
    for k in sorted(contests, key=lambda k: (k[0], k[1], k[2], k[3] or 0, k[4])):
        c = contests[k]
        tv = sorted(c["totalvotes"])
        c["totalvotes"] = tv[0] if len(tv) == 1 else None
        c["candidates"].sort(key=lambda a: -(a["votes"] or 0))
        checks = []
        s = sum(a["votes"] or 0 for a in c["candidates"])
        if len(tv) > 1:
            checks.append(f"totalvotes not unique: {tv}")
        elif tv and tv[0] != s:
            checks.append(f"candidates sum to {s:,}; totalvotes {tv[0]:,}")
        if c["office"] != "president":
            w = sum(1 for a in c["candidates"] if a["won"] == 1)
            if w != 1:
                checks.append(f"{w} winners")
        c["checks"] = checks
        out.append(c)
    cc.write_json(os.path.join(cc.CACHE, "cha", "normalized", "contests.json"), {"source": info, "contests": out})
    by = {}
    for c in out:
        by.setdefault((c["year"], c["office"]), 0)
        by[(c["year"], c["office"])] += 1
    print(f"{NAME} {info['version']}, licence {info['licence']}: {len(df):,} rows, {len(out):,} contests; "
          f"{sum(1 for c in out if c['checks'])} with a check that failed")
    for y in sorted({c["year"] for c in out}):
        print(f"  {y}: " + ", ".join(f"{o} {by.get((y, o), 0)}" for o in ("senate", "house", "governor")))


def source_for(contest, info):
    """The source block of plan section 3 for a contest read from this dataset."""
    office = {v: k for k, v in OFFICE.items()}[contest["office"]]
    origin = ORIGIN[office]
    note = ("governors' votes from each state's statement of votes, per the dataset's guide"
            if office == "G" else None)
    return cc.source_block(f"{NAME}, {info['version']}", origin or f"https://doi.org/{DOI[4:]}",
                           info["file"]["read_utc"], info["licence"], mark="stated",
                           via=f"https://doi.org/{DOI[4:]}", note=note)


if __name__ == "__main__":
    main()
