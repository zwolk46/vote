"""pipeline/intake/algara_amlani.py: Algara and Amlani's county returns for governor, 1865-2020, summed to states.

Written 2026-11-07 by worker D2 (briefs/D2-data-congress.md; the orchestrator's round of 06:36 UTC, item 1:
"take in Algara and Amlani's county returns (CC0) by script. That adds the earlier governor races as contests,
and lets 2006 to 2016 be fitted on earlier cycles." Reason: the maker wants as much data as can be found, and
this both adds races and restores p).

Source. Carlos Algara and Sharif Amlani, "Replication Data for: Partisanship & Nationalization in American
Elections: Evidence from Presidential, Senatorial, & Gubernatorial Elections in the U.S. Counties, 1872-2020",
Harvard Dataverse, doi:10.7910/DVN/DGUMFI, licence CC0 1.0 (the record's licence field), no guestbook. The
file taken is dataverse_shareable_gubernatorial_county_returns_1865_2020.Rdata (data frame
gov_elections_release), described in the dataset's County_Level_Dataset_Manual_READ_ME.pdf (2021-08-30):
one row per county and election, with the Democratic and Republican nominees' votes, the county's total
vote, and the seat's status (an incumbent's party and re-election bid, or an open seat), which the authors
coded from Congressional Quarterly. Alaska is not in it (no consistent counties); 37 of 2,499 elections since
1865 are missing (the manual lists them; none after 1954).

What this script makes of it: one record per election (the authors' election_id, year and state), with the
two nominees' votes and the total summed over the counties, the number of counties and of counties with a
missing count, and the seat's status. The votes are a SUM OF COUNTY RETURNS compiled by the authors, not a
state's certified total, and the other candidates are known only as the total minus the two nominees, not by
name. The Rdata is read by pipeline/intake/rdata_reader.py (no R here), and checked against the MD5 Dataverse
publishes for the file.

Check (plan section 3a, two sources): every governor election of 2006-2020 in both this source and Cha,
Kuriwaki and Snyder (pipeline/intake/candidates_american_general_elections.py) is compared, nominee by
nominee; the differences are written with the records.

Run:  python3 pipeline/intake/algara_amlani.py governors
Writes CACHE/algara_amlani/normalized/governors.json.
"""
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import congress_common as cc  # noqa: E402
import rdata_reader  # noqa: E402

API = "https://dataverse.harvard.edu/api"
DOI = "doi:10.7910/DVN/DGUMFI"
GOV_FILE = "dataverse_shareable_gubernatorial_county_returns_1865_2020.Rdata"
MANUAL = "County_Level_Dataset_Manual_READ_ME.pdf"
OUT = os.path.join(cc.CACHE, "algara_amlani", "normalized", "governors.json")

# seat_status (manual 3.2, item 9): the incumbent's party when the incumbent runs; an open seat otherwise
INCUMBENT = {"Democratic Incumbent": 1, "Republican Incumbent": -1}


def _md5(path):
    h = hashlib.md5()
    with open(os.path.join(cc.CACHE, path), "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch_files():
    rec = cc.fetch(f"{API}/datasets/:persistentId/?persistentId={DOI}", "algara_amlani/record.json")
    with open(os.path.join(cc.CACHE, rec["path"])) as f:
        meta = json.load(f)["data"]
    v = meta["latestVersion"]
    files = {f["dataFile"]["filename"]: f["dataFile"] for f in v["files"]}
    out = {}
    for name in (GOV_FILE, MANUAL):
        df = files[name]
        # Harvard Dataverse serves its files from Amazon S3: a redirect there is the publisher's own storage
        r = cc.fetch(f"{API}/access/datafile/{df['id']}", f"algara_amlani/{name}", storage_sites=("amazonaws.com",))
        got = _md5(r["path"])
        if got != df["md5"]:
            raise SystemExit(f"{name}: MD5 {got}, Dataverse publishes {df['md5']}")
        r["md5"] = got
        out[name] = r
    lic = v["license"]["name"] if isinstance(v.get("license"), dict) else v.get("license")
    return rec, out, f"v{v['versionNumber']}.{v['versionMinorNumber']}, released {v.get('releaseTime')}", lic


def governors():
    rec, files, version, lic = fetch_files()
    objs = rdata_reader.load(os.path.join(cc.CACHE, files[GOV_FILE]["path"]))
    df = rdata_reader.data_frame(objs["gov_elections_release"])
    n = len(df["election_id"])
    races = {}
    for i in range(n):
        eid = df["election_id"][i]
        r = races.setdefault(eid, {"election_id": eid, "year": int(df["election_year"][i]), "state": df["state"][i],
                                   "type": df["election_type"][i], "seat_status": df["seat_status"][i],
                                   "dem_nominee": df["dem_nominee"][i], "rep_nominee": df["rep_nominee"][i],
                                   "D": 0, "R": 0, "total": 0, "counties": 0, "counties_missing": 0})
        d, rp, tot = (df["democratic_raw_votes"][i], df["republican_raw_votes"][i], df["raw_county_vote_totals"][i])
        r["counties"] += 1
        if d is None or rp is None or tot is None:
            r["counties_missing"] += 1
            continue
        r["D"] += int(round(d))
        r["R"] += int(round(rp))
        r["total"] += int(round(tot))
        for k in ("seat_status", "dem_nominee", "rep_nominee"):
            if df[k][i] != r[k]:
                raise SystemExit(f"{eid}: {k} differs between counties ({r[k]!r}, {df[k][i]!r})")
    out = []
    for r in sorted(races.values(), key=lambda r: (r["year"], r["state"])):
        for k in ("dem_nominee", "rep_nominee"):
            if r[k] in ("None", "", None):
                r[k] = None
        r["others"] = r["total"] - r["D"] - r["R"]
        r["incumbency"] = INCUMBENT.get(r["seat_status"], 0)
        if r["others"] < 0:
            # a county's total below its two nominees' votes (some nineteenth-century rows): the others' vote
            # is unknown, not negative
            r["others"] = None
            r["note"] = "the county totals sum to less than the two nominees' votes; the others' vote is unknown"
        out.append(r)
    print(f"{n} county rows, {len(out)} elections, {out[0]['year']}-{out[-1]['year']}; "
          f"{sum(1 for r in out if r['counties_missing'])} with a county count missing")

    # the second source: Cha, Kuriwaki and Snyder, 2006-2020
    cha = cc.read_json(os.path.join(cc.CACHE, "cha", "normalized", "contests.json"))
    checks = []
    if cha:
        idx = {}
        for c in cha["contests"]:
            if c["office"] == "governor" and not c["runoff"]:
                idx.setdefault((c["year"], c["state"]), []).append(c)
        for r in out:
            if r["year"] < 2006:
                continue
            cs = idx.get((r["year"], r["state"]))
            if not cs:
                checks.append({"election_id": r["election_id"], "difference": "not in Cha, Kuriwaki and Snyder"})
                continue
            c = cs[0]
            for party, key in (("D", "D"), ("R", "R")):
                v = sum(a["votes"] or 0 for a in c["candidates"] if a["party"] == party)
                if v != r[key]:
                    checks.append({"election_id": r["election_id"], "party": party, "algara_amlani": r[key],
                                   "cha": v, "relative": (r[key] - v) / v if v else None})
        big = [x for x in checks if x.get("relative") is not None and abs(x["relative"]) > 0.001]
        print(f"against Cha 2006-2020: {sum(1 for r in out if r['year'] >= 2006)} elections, {len(checks)} "
              f"differences, {len(big)} over 0.1%")
    src = cc.source_block(f"Algara and Amlani, Replication Data for: Partisanship & Nationalization in American "
                          f"Elections (county returns, governor 1865-2020), Harvard Dataverse {DOI}, {version}",
                          files[GOV_FILE]["url"], files[GOV_FILE]["read_utc"], lic, mark="stated",
                          via="https://doi.org/10.7910/DVN/DGUMFI",
                          note="county returns summed to the state by pipeline/intake/algara_amlani.py; the "
                               "authors' compilation, not a state's certified total; other candidates only as the "
                               "county total less the two nominees; the seat's status as the authors coded it from "
                               "Congressional Quarterly (the dataset's manual, 2021-08-30)")
    cc.write_json(OUT, {"source": src, "files": files, "record": rec, "elections": out, "check_against_cha": checks})
    print(f"wrote {OUT}")


if __name__ == "__main__":
    for a in sys.argv[1:] or ["governors"]:
        {"governors": governors}[a]()
