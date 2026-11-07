"""pipeline/intake/chen_waits.py: voting wait times by state, November 2016, from smartphone location data.

Source. Keith Chen, Kareem Haggag, Devin G. Pope and Ryne Rohla, replication archive for "Racial Disparities in Voting
Wait Times: Evidence from Smartphone Data", Review of Economics and Statistics; Harvard Dataverse,
doi:10.7910/DVN/RRHANS (version 1.1, 2023-03-02), licence CC0 1.0 as the dataset record prints it [measured].
Files read: voterwaittimes_filtered.tab (the 154,489 filtered waits, one row per phone and polling place: medians and
shares over 30 minutes are computed from it), county_voterwaittimes.tab (the county and state summary the authors built), cces_comparison.tab (the
authors' state and district summary of the 2016 CCES survey's wait question beside their own), ReadMe.pdf and
2-CreateAnalysisDatasets.do (how the figures were built), the dataset record JSON.

What the figure is (from the do-file, lines 310 to 324 and 549 to 551; the ReadMe, items 3 to 6):
  - pings of smartphones (SafeGraph) within 60 metres of a polling place building's centre on Election Day, 8 Nov 2016;
  - for each device and polling place, wait = the midpoint of a lower bound (time between the earliest and latest ping
    inside the circle) and an upper bound (the lower bound plus the gaps to the pings just before and after);
  - only "likely voters" (not at more than one polling place on Election Day, not at their polling place on other
    days), who entered the polling place, who ping at least 12 hours of the day, and whose upper bound is 1 to 120
    minutes (the do-file's reasonablevalues);
  - state average = the plain mean of those waits over the state; the authors' empirical-Bayes shrunk state average is
    also in the file. The number counts all the time the phone was at the polling place, so it includes the time
    spent voting, not only standing in line [stated by the authors; the line is read as such, [inferred]].
It is a measure of one election (2016 general), of a sample of phones, in 46 of the 51 jurisdictions: Alaska, Colorado,
Hawaii, Oregon and Washington are absent from the file [measured: the file has no row for them].
Check: the state Ns add up to 154,489, the size of the analysis sample the ReadMe gives (voterwaittimes_filtered.dta).

Run: python3 pipeline/intake/chen_waits.py        (writes data/cost/chen-waits.json)
"""
import csv
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import congress_common as cc  # noqa: E402

API = "https://dataverse.harvard.edu"
DOI = "doi:10.7910/DVN/RRHANS"
FILES = {"county_voterwaittimes.tab": 4161010, "cces_comparison.tab": 4160997, "ReadMe.pdf": 4160998,
         "2-CreateAnalysisDatasets.do": 4161011, "voterwaittimes_filtered.tab": 4161008}
ABBR = set(cc.STATES_50) | {"DC"}  # the 50 states and DC
SAMPLE_N = 154489  # the ReadMe: "154,489 wait times after applying the four filters"


def f(x):
    x = (x or "").strip()
    return float(x) if x not in ("", ".") else None


def main():
    rec = {}
    for name, fid in FILES.items():
        rec[name] = cc.fetch(f"{API}/api/access/datafile/{fid}", f"cost/chen/{name}", min_bytes=500, storage_sites=("amazonaws.com",))
    meta = cc.fetch(f"{API}/api/datasets/:persistentId/?persistentId={DOI}", "cost/chen/dv_RRHANS.json", min_bytes=1000)
    dv = json.load(open(os.path.join(cc.CACHE, meta["path"])))["data"]["latestVersion"]
    licence = dv["license"]["name"]
    with open(os.path.join(cc.CACHE, rec["county_voterwaittimes.tab"]["path"]), encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    with open(os.path.join(cc.CACHE, rec["cces_comparison.tab"]["path"]), encoding="utf-8") as fh:
        cces = list(csv.DictReader(fh, delimiter="\t"))
    cces_by_state = {}
    for r in cces:
        cces_by_state[r["state_name"]] = f(r["state_cces_waittime_avg_ebayes"])
    waits = {}   # postal code -> list of waits, from the individual-level file
    with open(os.path.join(cc.CACHE, rec["voterwaittimes_filtered.tab"]["path"]), encoding="utf-8") as fh:
        n_ind = 0
        for r in csv.DictReader(fh, delimiter="\t"):
            n_ind += 1
            waits.setdefault(r["state_abb"], []).append(float(r["waittime"]))
    allw = sorted(x for v in waits.values() for x in v)

    def med(v):
        v = sorted(v)
        k = len(v)
        return v[k // 2] if k % 2 else (v[k // 2 - 1] + v[k // 2]) / 2

    def share_over(v, m):
        return sum(1 for x in v if x > m) / len(v)

    states = {}
    for r in rows:
        st = r["state_abb"]
        if st in states or st not in ABBR:
            continue
        states[st] = {"name": r["state_name"],
                      "mean_minutes": round(f(r["state_waittime_avg"]), 2), "sd_minutes": round(f(r["state_waittime_sd"]), 2),
                      "n_waits": int(f(r["state_waittime_N"])),
                      "mean_minutes_empirical_bayes": round(f(r["state_waittime_avg_ebayes"]), 2),
                      "cces_survey_mean_minutes_empirical_bayes": None if cces_by_state.get(r["state_name"]) is None else round(cces_by_state[r["state_name"]], 2)}
        w = waits.get(st, [])
        states[st]["median_minutes"] = round(med(w), 2) if w else None
        states[st]["share_over_30_minutes"] = round(share_over(w, 30), 4) if w else None
        states[st]["se_minutes"] = round(states[st]["sd_minutes"] / states[st]["n_waits"] ** 0.5, 2)
    total_n = sum(s["n_waits"] for s in states.values())
    pooled = sum(s["mean_minutes"] * s["n_waits"] for s in states.values()) / total_n
    ok = total_n == SAMPLE_N and n_ind == SAMPLE_N
    mean_ind = sum(allw) / len(allw)
    national = {"n_waits": len(allw), "mean_minutes": round(mean_ind, 2), "median_minutes": round(med(allw), 2),
                "share_over_30_minutes": round(share_over(allw, 30), 4), "share_over_60_minutes": round(share_over(allw, 60), 4)}
    state_n_county = sum(f(r["county_waittime_N"]) or 0 for r in rows)
    src = [cc.source_block(f"Chen, Haggag, Pope and Rohla, Racial Disparities in Voting Wait Times (replication archive), {n}",
                           f"{API}/api/access/datafile/{fid}", rec[n]["read_utc"], licence, mark="measured",
                           via="Harvard Dataverse, " + DOI, note=f"{rec[n]['bytes']} bytes, sha256 {rec[n]['sha256']}")
           for n, fid in FILES.items()]
    out = {"about": "Average time at the polling place by state, general election of 8 November 2016, from smartphone location data (see pipeline/intake/chen_waits.py for what is and is not measured).",
           "election": "2016 general", "mark": "measured (a sample of phones; the time includes voting itself)",
           "sources": src,
           "national_all_filtered_waits": national,
           "check": {"individual_rows": n_ind, "state_n_sum": total_n, "county_n_sum": int(state_n_county), "readme_sample_size": SAMPLE_N, "matches": ok and int(state_n_county) == SAMPLE_N},
           "pooled_mean_minutes": round(pooled, 2), "individual_mean_equals_pooled": abs(mean_ind - pooled) < 0.01, "states_in_file": len(states),
           "states_absent": sorted(ABBR - set(states)),
           "states": dict(sorted(states.items())),
           "note": ("mean_minutes is the plain mean of the waits in the authors' filtered sample; se_minutes = sd / sqrt(n) treats the phones as independent "
                    "draws (phones at one polling place are not), so it is a floor on the error. cces_survey_mean_minutes_empirical_bayes is the authors' "
                    "shrunk state mean of the 2016 CCES survey answers as they converted them, carried for comparison.")}
    dest = os.path.join(cc.DATA, "cost")
    os.makedirs(dest, exist_ok=True)
    with open(os.path.join(dest, "chen-waits.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    print(national, "individual rows", n_ind, len(states), "states; N", total_n, "county N", int(state_n_county), "matches sample:", out["check"]["matches"], "pooled", out["pooled_mean_minutes"])


if __name__ == "__main__":
    main()
