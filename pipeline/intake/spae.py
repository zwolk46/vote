"""pipeline/intake/spae.py: time in line to vote, and how people voted, by state, from MIT's Survey of the
Performance of American Elections (SPAE).

Source. MIT Election Data and Science Lab (Charles Stewart III), "Survey of the Performance of American Elections",
Harvard Dataverse, every file open (no guestbook) and CC0 1.0 (the dataset's licence field), except 2024:
    2008  doi:10.7910/DVN/1FYT4P   spae_2008.tab                    (file 2433003)
    2012  doi:10.7910/DVN/WP8RHI   MITU0017_OUTPUT.tab              (file 2437448)
    2014  doi:10.7910/DVN/28979    MITU0019_OUTPUT_50state_1.tab    (file 2531942)  the 50-state sample; the
          ten-state oversample (doi:10.7910/DVN/28981) is separately weighted and is not combined
    2016  doi:10.7910/DVN/Y38VIQ   MITU0022_OUTPUT.tab              (file 3012345)
    2020  doi:10.7910/DVN/FSGX7Z   MITU0031_OUTPUT2.tab             (file 4461637)
    2022  doi:10.7910/DVN/SPU2XP   MITU0042_OUTPUT_0120.tab         (file 7103004)
    2024  doi:10.7910/DVN/GWBAP5   the data files need a Guestbook response (a name and an email): not filled,
          the maker's call (law 10); the intake reports it as gated. MIT Election Lab's own pages point only to
          that Dataverse record (read 2026-11-07).
There was no SPAE in 2010 or 2018 (the 2018 figures in MIT's reports come from the Cooperative Election Study).

The question. "Approximately, how long did you have to wait in line to vote?" (the questionnaires, quoted in
the DDI codebooks cached beside the data), asked of people who voted in person; answers: 1 not at all, 2 less
than 10 minutes, 3 10-30 minutes, 4 31 minutes to 1 hour, 5 more than 1 hour (open text for the minutes),
and "don't know". Mode of voting: 1 in person on Election Day, 2 in person before Election Day, 3 by mail or
absentee. Variables by year: line length q12 (2008), q10 (2012), Q13 (2014, 2016), Q14 (2020), Q12 (2022);
mode q5/q5b (2008), q4 (2012), Q4 (later); state inputstate (a FIPS code; 2012: regstate, state of
registration); weight "case weight" (2008, 2012, 2014, 2016), "Registered Voter State Weight" (2020),
"State RV Weights" (weight_stacked, 2022).

What is computed, by state and year, among respondents who gave a wait category (1 to 5):
  n                      respondents (unweighted) and the weighted shares of the five categories [measured: the
                         survey's own answers, weighted];
  mean_minutes_midpoint  the categories at their midpoints (0, 5, 20, 45, and a top value) [inferred: a convention
                         (Stewart 2013 recodes the categories to midpoints); the top category has no upper end,
                         so its value is the mean of the minutes respondents wrote in that year, where at least 30
                         could be read, else 90];
  mean_minutes_lower_bound  the categories at their lower ends (0, 0, 10, 31, 60) [inferred]: a floor, since
                         every answer is at least that;
  se_minutes             the standard error of the midpoint mean, from the weighted deviations (a linearized
                         sum, ignoring the weighting's design effect) [inferred]: read it as a lower bound;
  mode_shares_survey     how the state's voters in the sample said they voted (all respondents with a mode).
These are survey estimates of about 200 voters per state (400 to 1,000 in a few) and are marked thin under 60 with
a wait answer. The weights are the survey's state weights; no national average is formed from them here.

Run:  python3 pipeline/intake/spae.py          (downloads the files into the cache once; writes data/cost/spae-waits.json)
"""
import csv
import json
import os
import re
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import congress_common as cc  # noqa: E402
from bls_earnings import STATES  # noqa: E402   (FIPS -> postal code, the 50 states and DC)

DV = "https://dataverse.harvard.edu/api/access/datafile/{}"
DV_DATASET = "https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/{}"
YEARS = {
    2008: dict(doi="1FYT4P", file=2433003, name="spae_2008.tab", state="inputstate", weight="weight", line="q12", mode=["q5", "q5b"]),
    2012: dict(doi="WP8RHI", file=2437448, name="MITU0017_OUTPUT.tab", state="regstate", weight="weight", line="q10", mode=["q4"]),
    2014: dict(doi="28979", file=2531942, name="MITU0019_OUTPUT_50state_1.tab", state="inputstate", weight="weight", line="Q13", mode=["Q4"]),
    2016: dict(doi="Y38VIQ", file=3012345, name="MITU0022_OUTPUT.tab", state="inputstate", weight="weight", line="Q13", mode=["Q4"]),
    2020: dict(doi="FSGX7Z", file=4461637, name="MITU0031_OUTPUT2.tab", state="inputstate", weight="weight", line="Q14", mode=["Q4"]),
    2022: dict(doi="SPU2XP", file=7103004, name="MITU0042_OUTPUT_0120.tab", state="inputstate", weight="weight_stacked", line="Q12", mode=["Q4"]),
}
GATED = {2024: dict(doi="GWBAP5", note="data files need a Dataverse Guestbook response (name and email); not filled (law 10); MIT Election Lab's pages link only to this record")}
CAT_LABEL = {1: "not at all", 2: "less than 10 minutes", 3: "10-30 minutes", 4: "31 minutes to 1 hour", 5: "more than 1 hour"}
MID = {1: 0.0, 2: 5.0, 3: 20.0, 4: 45.0}
LOW = {1: 0.0, 2: 0.0, 3: 10.0, 4: 31.0, 5: 60.0}
MODE_LABEL = {1: "in person on Election Day", 2: "in person before Election Day", 3: "by mail or absentee"}


def minutes_from_text(t):
    """Minutes a respondent wrote for 'more than 1 hour': '2 hours', '90 minutes', '1 hour 15 minutes', '1.5'.
    A bare number up to 10 is read as hours, a bare number of 15 or more as minutes, else not read."""
    t = (t or "").strip().lower()
    if not t:
        return None
    t = t.replace("1/2", ".5").replace("½", ".5")
    h = re.search(r"(\d+(?:\.\d+)?)\s*(?:hours?|hrs?|h\b)", t)
    m = re.search(r"(\d+(?:\.\d+)?)\s*(?:minutes?|mins?|m\b)", t)
    tot = 0.0
    if h:
        tot += float(h.group(1)) * 60
    if m:
        tot += float(m.group(1))
    if h or m:
        return tot if 60 <= tot <= 600 else None
    if re.fullmatch(r"\d+(?:\.\d+)?", t):
        v = float(t)
        if 1 <= v <= 10:
            return v * 60
        if 60 <= v <= 600:
            return v
    return None


def wmean(pairs):
    sw = sum(w for _, w in pairs)
    return sum(x * w for x, w in pairs) / sw if sw else None


def main():
    out = {"about": "Time in line to vote and how people voted, by state, from MIT's Survey of the Performance of American Elections (CC0 1.0): the survey's own answers, weighted by its state weights. See pipeline/intake/spae.py for the definitions.",
           "years": {}, "gated": {}, "unread": []}
    for y, c in sorted(YEARS.items()):
        meta_rec = cc.fetch(DV_DATASET.format(c["doi"]), f"cost/spae/dv_{c['doi']}.json", storage_sites=("amazonaws.com",))
        ds = json.load(open(os.path.join(cc.CACHE, meta_rec["path"])))["data"]["latestVersion"]
        lic = (ds.get("license") or {}).get("name")
        fmeta = [f for f in ds["files"] if f["dataFile"]["id"] == c["file"]][0]
        assert fmeta["dataFile"]["filename"] == c["name"] and not fmeta.get("restricted"), (y, fmeta["dataFile"])
        rec = cc.fetch(DV.format(c["file"]), f"cost/spae/spae{y}.tab", storage_sites=("amazonaws.com",), min_bytes=1000)
        with open(os.path.join(cc.CACHE, rec["path"]), encoding="utf-8", errors="replace", newline="") as f:
            rows = list(csv.DictReader(f, delimiter="\t"))
        src = cc.source_block(f"Survey of the Performance of American Elections {y} ({c['name']})",
                              f"https://doi.org/10.7910/DVN/{c['doi']}", rec["read_utc"], lic or "CC0 1.0", mark="measured",
                              note=f"file {c['file']}, {rec['bytes']} bytes, sha256 {rec['sha256']}; Dataverse dataset version {ds.get('versionNumber')}.{ds.get('versionMinorNumber')}, released {ds.get('releaseTime', '')[:10]}")
        # the top category's minutes this year, from the open text
        tcol = {2008: "q12_t", 2012: "q10_t", 2014: "Q13_t", 2016: "Q13_t", 2020: "Q14_t", 2022: "Q12_t"}[y]
        tops = []
        for r in rows:
            if r[c["line"]].strip() == "5":
                mm = minutes_from_text(r.get(tcol, ""))
                if mm is not None:
                    tops.append(mm)
        top_val = round(sum(tops) / len(tops), 2) if len(tops) >= 30 else 90.0
        top_how = f"mean of {len(tops)} readable written answers" if len(tops) >= 30 else f"90 assumed ({len(tops)} readable written answers, under 30)"
        by_state = defaultdict(list)
        for r in rows:
            try:
                fips = f"{int(r[c['state']]):02d}"
            except ValueError:
                continue
            by_state[fips].append(r)
        states = {}
        for fips, rs in sorted(by_state.items()):
            if fips not in STATES:
                continue
            w_of = lambda r: float(r[c["weight"]])  # noqa: E731
            # wait
            ans = [(int(r[c["line"]]), w_of(r)) for r in rs if r[c["line"]].strip() in ("1", "2", "3", "4", "5")]
            modes = []
            for r in rs:
                for mv in c["mode"]:
                    if r.get(mv, "").strip() in ("1", "2", "3"):
                        modes.append((int(r[mv]), w_of(r)))
                        break
            rec_st = {"n_respondents": len(rs), "n_with_wait_answer": len(ans)}
            if ans:
                sw = sum(w for _, w in ans)
                shares = {CAT_LABEL[k]: round(sum(w for cat, w in ans if cat == k) / sw, 4) for k in CAT_LABEL}
                mids = {**MID, 5: top_val}
                xs = [(mids[cat], w) for cat, w in ans]
                m = wmean(xs)
                se = (sum((w * (x - m)) ** 2 for x, w in xs) ** 0.5) / sw
                lows = wmean([(LOW[cat], w) for cat, w in ans])
                rec_st.update({"wait_shares": shares, "mean_minutes_midpoint": round(m, 2), "se_minutes": round(se, 2),
                               "mean_minutes_lower_bound": round(lows, 2),
                               "share_over_30_minutes": round(shares["31 minutes to 1 hour"] + shares["more than 1 hour"], 4),
                               "thin": len(ans) < 60})
            if modes:
                sw = sum(w for _, w in modes)
                rec_st["mode_shares_survey"] = {"n": len(modes), **{MODE_LABEL[k]: round(sum(w for mo, w in modes if mo == k) / sw, 4) for k in MODE_LABEL}}
            states[STATES[fips]] = rec_st
        out["years"][str(y)] = {"source": src, "file": c["name"], "weight": c["weight"], "state_variable": c["state"],
                                "line_variable": c["line"], "mode_variables": c["mode"],
                                "top_category_minutes": top_val, "top_category_how": top_how,
                                "respondents": len(rows), "states": states,
                                "states_missing": sorted(set(STATES.values()) - set(states))}
        print(y, len(rows), "respondents", len(states), "states; top bin", top_val, top_how)
    for y, g in GATED.items():
        out["gated"][str(y)] = {"doi": f"https://doi.org/10.7910/DVN/{g['doi']}", "why": g["note"]}
    out["unread"] = [
        {"what": "SPAE 2024 microdata", "reason": GATED[2024]["note"]},
        {"what": "the 2014 ten-state oversample (doi:10.7910/DVN/28981)", "reason": "separately weighted; not combined with the 50-state sample"},
    ]
    dest = os.path.join(cc.DATA, "cost")
    os.makedirs(dest, exist_ok=True)
    with open(os.path.join(dest, "spae-waits.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
        f.write("\n")


if __name__ == "__main__":
    main()
