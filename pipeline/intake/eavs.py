"""pipeline/intake/eavs.py: how ballots were cast, by state, from the Election Assistance Commission's Election
Administration and Voting Survey (EAVS), 2016 to 2024.

Source. U.S. Election Assistance Commission, "Election Administration and Voting Survey" (EAVS), the biennial survey of
every election jurisdiction (about 6,460: counties, and towns in New England and Wisconsin), Section F1
"Total Participation in the General Election by mode of voting". The EAC's public-release data files, from
https://www.eac.gov/research-and-data/studies-and-reports (the page's own links):
  2024  2024_EAVS_for_Public_Release_nolabel_V2_csv.zip   (version 2, in the 2026-02 folder of the EAC site; the codebook is in 2025-06)
  2022  2022_EAVS_for_Public_Release_nolabel_V1_CSV.zip
  2020  2020_EAVS_for_Public_Release_nolabel_V1.2_CSV.zip (V1.2, December 2023)
  2018  EAVS_2018_for_Public_Release_Updates3.csv
  2016  EAVS_2016_for_Public_Release_nolabel_V1.1_CSV.zip (V1.1, December 2023)
Licence: a publication of a U.S. Government agency; the page prints no licence or terms [measured, 2026-11-07].
Earlier EAVS years (2004 to 2014: Excel, SPSS and DBF sets in section files with other layouts) are listed in
data/sources/cost.md and are not taken here.

What F1 asks (the instruments for 2018 to 2024, cached beside the data, say the same in these words):
  F1a  total number of voters who cast a ballot that was counted, all modes;
  F1b  voters who cast a ballot at a physical polling place on Election Day (not provisional ballots or mail
       ballots dropped off at the polls);
  F1c  UOCAVA voters (military and overseas) who voted by absentee ballot or FWAB;
  F1d  voters who cast a domestic civilian mail ballot (in jurisdictions that do not conduct elections by mail);
  F1e  voters whose provisional ballot was counted;
  F1f  voters who cast a ballot at an in-person early voting location (in-person early or in-person absentee);
  F1g  voters who cast a mail ballot in a jurisdiction that conducts elections by mail (every voter is mailed one);
  F1h  other (2016 also F1i and F1j).
The special values: -88 "does not apply", -77 "valid skip" (both read as zero); -99 and the text "Data not available"
(counted as unreported, not as zero) (the codebooks).

What is computed, per state and year: the sum over the state's jurisdictions of each variable; the number of
jurisdictions that did not report it; and shares of F1a. Derived shares (marked [inferred]):
  mail_share            (F1d + F1g) / F1a;
  early_in_person_share F1f / F1a;
  election_day_share    (F1b + F1e) / F1a   (provisional ballots are cast in person, mostly on Election Day);
  uocava_share          F1c / F1a.
A jurisdiction's parts need not add to its F1a (each reports its own, and a mode may be left blank: -99, "Data not
available"). Totals and mode counts are summed over every jurisdiction with a reported F1a; the ratio of the parts'
sum to F1a is recorded. The SHARES are computed only over jurisdictions whose parts add to their F1a within 3%,
because a blank mode would otherwise show as a share of zero (Connecticut 2024 left Election Day blank in all 169
towns; Mississippi 2024 left mail and early blank in all 82 counties). A state whose consistent jurisdictions hold
under 80% of its ballots has no shares ("shares_withheld", with the reason) [inferred: my rule; the tolerance and
the 80% are choices]. The 50 states and DC are taken; the territories
(American Samoa, Guam, Northern Mariana Islands, Puerto Rico, U.S. Virgin Islands) are not.

Check against a published total: pipeline/intake/eavs.py records the national sums; the EAC's comprehensive report for
each year states a national total of voters, noted beside it in data/cost/REPORT.md.

Run:  python3 pipeline/intake/eavs.py        (downloads into the cache once; writes data/cost/eavs-mode.json)
"""
import csv
import io
import json
import os
import sys
import zipfile
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import congress_common as cc  # noqa: E402
from bls_earnings import STATES  # noqa: E402

B = "https://www.eac.gov"
YEARS = {
    2024: dict(url="/sites/default/files/2026-02/2024_EAVS_for_Public_Release_nolabel_V2_csv.zip", member="2024_EAVS_for_Public_Release_nolabel_V2.csv", version="2 (file folder 2026-02)",
               instrument="/sites/default/files/2024-04/2024_EAVS_FINAL_508c.pdf"),
    2022: dict(url="/sites/default/files/2023-06/2022_EAVS_for_Public_Release_nolabel_V1_CSV.zip", member="2022_EAVS_for_Public_Release_nolabel_V1.csv", version="1.0 (2023-06)",
               instrument="/sites/default/files/EAVS%202022/2022_EAVS_FINAL_508c.pdf"),
    2020: dict(url="/sites/default/files/2023-12/2020_EAVS_for_Public_Release_nolabel_V1.2_CSV.zip", member="2020_EAVS_for_Public_Release_nolabel_V1.2_CSV.csv", version="1.2 (2023-12)",
               instrument="/sites/default/files/Research/2020EAVS.pdf"),
    2018: dict(url="/sites/default/files/Research/EAVS_2018_for_Public_Release_Updates3.csv", member=None, version="Updates3",
               instrument="/sites/default/files/eac_assets/1/6/2018_EAC_Election_Administration_and_Voting_Survey_Instrument.pdf"),
    2016: dict(url="/sites/default/files/2023-12/EAVS_2016_for_Public_Release_nolabel_V1.1_CSV.zip", member="EAVS_2016_Final_Data_for_Public_Release_nolabel_V1.1_CSV.csv", version="1.1 (2023-12)",
               instrument="/sites/default/files/eac_assets/1/28/2016_EAVS_Instrument.pdf"),
}
# The EAC's own comprehensive report for each year states a national total of voters whose ballot was counted
# (F1a, all rows including the territories). The script downloads the report, turns it to text (pdftotext) and
# looks for the number; the check passes only if it is found [measured].
REPORTS = {
    2024: ("https://www.eac.gov/sites/default/files/2025-07/2024_EAVS_Report_508.pdf", 158211780),
    2022: ("https://www.eac.gov/sites/default/files/2023-06/2022_EAVS_Report_508c.pdf", 112054124),
    2020: ("https://www.eac.gov/sites/default/files/document_library/files/2020_EAVS_Report_Final_508c.pdf", 161303109),
    2018: ("https://www.eac.gov/sites/default/files/eac_assets/1/6/2018_EAVS_Report.pdf", 120314461),
    2016: ("https://www.eac.gov/sites/default/files/eac_assets/1/6/2016_EAVS_Comprehensive_Report.pdf", 140114502),
}
CONSISTENT_TOLERANCE = 0.03   # a jurisdiction's modes may differ from its total by this share and still count in the shares
MIN_COVERAGE = 0.80           # a state's shares are shown only if jurisdictions that add up hold this share of its ballots
VARS = ["F1a", "F1b", "F1c", "F1d", "F1e", "F1f", "F1g", "F1h", "F1i", "F1j"]
NAMES = {"F1a": "total", "F1b": "election_day_in_person", "F1c": "uocava", "F1d": "mail", "F1e": "provisional",
         "F1f": "early_in_person", "F1g": "mail_in_all_mail_jurisdictions", "F1h": "other", "F1i": "other_2", "F1j": "other_3"}
ABBR = set(STATES.values())


def num(v):
    """(value, status): status 'ok', 'na' (-88, -77: read as zero) or 'missing' (-99, 'Data not available', blank)."""
    v = (v or "").strip()
    if v == "":
        return 0.0, "missing"
    try:
        x = float(v.replace(",", ""))
    except ValueError:
        return 0.0, "missing"
    if x in (-88.0, -77.0):
        return 0.0, "na"
    if x < 0:
        return 0.0, "missing"
    return x, "ok"


def published_check(y, states_total, territories_total):
    """The file's F1a over every row (states, DC and territories) against the number the EAC's report prints."""
    url, published = REPORTS[y]
    res = {"file_total_all_rows": int(states_total + territories_total), "of_which_states_and_dc": int(states_total),
           "of_which_territories": int(territories_total), "report_url": url, "report_total": published}
    try:
        rec = cc.fetch(url, f"cost/eavs/report{y}.pdf", min_bytes=100000)
    except Exception as e:  # a refusal or a missing file is recorded, not worked round
        res.update(status="report not read", reason=str(e)[:200])
        return res
    txt = os.path.join(cc.CACHE, rec["path"][:-4] + ".txt")
    if not os.path.exists(txt):
        os.system(f'pdftotext -layout "{os.path.join(cc.CACHE, rec["path"])}" "{txt}" 2>/dev/null')
    text = open(txt, encoding="utf-8", errors="replace").read()
    res.update(report_sha256=rec["sha256"], report_read_utc=rec["read_utc"])
    if published is None:
        res.update(status="no published total recorded")
        return res
    found = f"{published:,}" in text
    res["report_total_found_in_text"] = found
    res["difference_file_minus_report"] = int(states_total + territories_total) - published
    res["status"] = "matches" if found and res["difference_file_minus_report"] == 0 else "differs"
    return res


def main():
    out = {"about": "How ballots were cast, by state and general-election year, from the EAC's EAVS Section F1 (see pipeline/intake/eavs.py for the definitions).",
           "years": {}, "unread": []}
    for y, c in sorted(YEARS.items()):
        name = f"cost/eavs/eavs{y}" + (".csv.zip" if c["member"] else ".csv")
        rec = cc.fetch(B + c["url"], name, min_bytes=100000)
        inst = cc.fetch(B + c["instrument"], f"cost/eavs/eavs{y}_instrument.pdf", min_bytes=50000)
        path = os.path.join(cc.CACHE, rec["path"])
        if c["member"]:
            with zipfile.ZipFile(path) as z:
                raw = z.read(c["member"]).decode("utf-8", "replace")
        else:
            raw = open(path, encoding="utf-8", errors="replace").read()
        rows = list(csv.DictReader(io.StringIO(raw)))
        stkey = "State_Abbr" if "State_Abbr" in rows[0] else "State"   # 2016 prints the abbreviation in "State"
        agg = defaultdict(lambda: {"juris": 0, "juris_with_total": 0, "sum": defaultdict(float), "missing": defaultdict(int),
                                   "csum": defaultdict(float), "consistent": 0})
        territories = defaultdict(int)
        territory_total = defaultdict(float)
        for r in rows:
            st = r[stkey].strip()
            if st not in ABBR:
                territories[st] += 1
                territory_total[st] += max(num(r.get("F1a"))[0], 0)
                continue
            a = agg[st]
            a["juris"] += 1
            tot, tst = num(r.get("F1a"))
            if tst != "ok":
                a["missing"]["F1a"] += 1
                continue
            a["juris_with_total"] += 1
            a["sum"]["F1a"] += tot
            vals = {}
            for v in VARS[1:]:
                if v not in r:
                    continue
                x, s = num(r[v])
                vals[v] = x
                a["sum"][v] += x
                if s == "missing" and not (v in ("F1h", "F1i", "F1j")):
                    a["missing"][v] += 1
            # The shares use only jurisdictions whose modes add up to their own total (within CONSISTENT_TOLERANCE):
            # a mode left blank (-99, "Data not available") would otherwise show as a share of zero.
            if tot > 0 and abs(sum(vals.values()) / tot - 1) <= CONSISTENT_TOLERANCE:
                a["consistent"] += 1
                a["csum"]["F1a"] += tot
                for v, x in vals.items():
                    a["csum"][v] += x
        states = {}
        for st in sorted(agg):
            a = agg[st]
            T = a["sum"]["F1a"]
            S = a["sum"]
            parts = sum(S[v] for v in VARS[1:])
            rec_st = {"jurisdictions": a["juris"], "jurisdictions_with_total": a["juris_with_total"],
                      "total_ballots": int(T),
                      "by_mode": {NAMES[v]: int(S[v]) for v in VARS[1:] if v in rows[0] and (S[v] or v in ("F1b", "F1c", "F1d", "F1e", "F1f", "F1g"))},
                      "jurisdictions_not_reporting": {NAMES[v]: a["missing"][v] for v in ["F1a"] + VARS[1:7] if a["missing"][v]},
                      "parts_sum_over_total": round(parts / T, 4) if T else None}
            C = a["csum"]
            coverage = C["F1a"] / T if T else 0
            rec_st["share_basis"] = {"jurisdictions_whose_modes_add_to_their_total": a["consistent"], "ballots_in_them": int(C["F1a"]),
                                     "share_of_state_ballots": round(coverage, 4)}
            if T and coverage >= MIN_COVERAGE:
                rec_st["mail_share"] = round((C["F1d"] + C["F1g"]) / C["F1a"], 4)
                rec_st["early_in_person_share"] = round(C["F1f"] / C["F1a"], 4)
                rec_st["election_day_share"] = round((C["F1b"] + C["F1e"]) / C["F1a"], 4)
                rec_st["uocava_share"] = round(C["F1c"] / C["F1a"], 4)
            else:
                rec_st["shares_withheld"] = (f"only {coverage:.0%} of the state's ballots are in jurisdictions whose reported modes add up to their own total "
                                             f"(within {CONSISTENT_TOLERANCE:.0%}); a mode left unreported would show as a share of zero")
            states[st] = rec_st
        usable = [st for st in states if "mail_share" in states[st]]
        nat_c = defaultdict(float)
        for st in usable:
            for v, x in agg[st]["csum"].items():
                nat_c[v] += x
        nat_total = sum(s["total_ballots"] for s in states.values())
        nat = {k: sum(s["by_mode"].get(k, 0) for s in states.values()) for k in NAMES.values()}
        src = cc.source_block(f"U.S. Election Assistance Commission, {y} Election Administration and Voting Survey, public-release data (CSV), version {c['version']}",
                              B + c["url"], rec["read_utc"], "a U.S. Government publication; no licence or terms printed on the page",
                              mark="measured",
                              note=f"{rec['bytes']} bytes, sha256 {rec['sha256']}; instrument {B + c['instrument']} sha256 {inst['sha256']}")
        check = published_check(y, nat_total, sum(territory_total.values()))
        out["years"][str(y)] = {"source": src, "check_against_published_total": check, "jurisdictions_in_file": len(rows), "territories_not_taken": dict(territories),
                                "national_sum_of_states": {"total_ballots": nat_total, **{k: v for k, v in nat.items() if v}},
                                "national_mail_share": round((nat_c["F1d"] + nat_c["F1g"]) / nat_c["F1a"], 4),
                                "national_early_in_person_share": round(nat_c["F1f"] / nat_c["F1a"], 4),
                                "national_election_day_share": round((nat_c["F1b"] + nat_c["F1e"]) / nat_c["F1a"], 4),
                                "national_shares_basis": {"states_used": len(usable), "states_withheld": sorted(set(states) - set(usable)),
                                                          "ballots_used": int(nat_c["F1a"]), "share_of_national_ballots": round(nat_c["F1a"] / nat_total, 4)},
                                "states": states}
        print(y, len(rows), "rows;", len(states), "states; total", nat_total, "withheld", sorted(set(states) - set(usable)), "mail", out["years"][str(y)]["national_mail_share"],
              "early", out["years"][str(y)]["national_early_in_person_share"], "election day", out["years"][str(y)]["national_election_day_share"])
    out["unread"] = [{"what": "EAVS 2004 to 2014 (Excel, SPSS, DBF section files)", "reason": "other layouts (section files, different item numbers); listed in data/sources/cost.md, not taken in this run"}]
    dest = os.path.join(cc.DATA, "cost")
    os.makedirs(dest, exist_ok=True)
    with open(os.path.join(dest, "eavs-mode.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
        f.write("\n")


if __name__ == "__main__":
    main()
