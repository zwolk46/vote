"""pipeline/intake/cost_assemble.py: put the cost inputs side by side, by state, and write the national default.

Reads the files the other intake scripts wrote (no download, no new source):
  data/cost/wages.json        bls_earnings.py   average hourly earnings, private employees (BLS via FRED)
  data/cost/spae-waits.json   spae.py           time in line, MIT SPAE 2008 to 2022
  data/cost/chen-waits.json   chen_waits.py     time at the polling place, smartphone data, 2016
  data/cost/eavs-mode.json    eavs.py           ballots by mode, EAC EAVS 2016 to 2024
  data/cost/cps-voting.json   cps_voting.py     how citizens say they voted, CPS 2020 to 2024
and writes
  data/cost/by-state.json        one record per state and DC with every input beside the others, and the cost each
                                 basis gives (minutes x wage / 60), the arithmetic written out;
  data/cost/national-default.json  the site's default C and where each of its two inputs comes from.
No figure is introduced here: every number is copied from one of the files above or is minutes x wage / 60 of two such
numbers [inferred: the product is arithmetic, the choice of the products shown is mine].

What the cost means. The minutes are the time of a person who votes in person (SPAE asks in-person voters; Chen
measures phones at polling places on Election Day), so the cost applies to them; a mail voter has no line and no trip
(the mail share beside it says how many that is). The wage values all time at the average hourly earnings of private
employees, the convention of the model (model §6); travel and the time to register or to learn about the contest are
not measured by any source here.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import congress_common as cc  # noqa: E402

COST = os.path.join(cc.DATA, "cost")
DEFAULT_MINUTES = 14       # model §6: the median time at the polls, Chen et al. 2016
DEFAULT_WAGE_SERIES = "CES0500000003"
MEAN_MINUTES = 19          # model §6: the mean in the same study


def load(name):
    with open(os.path.join(COST, name), encoding="utf-8") as f:
        return json.load(f)


def dollars(minutes, wage):
    return round(minutes * wage / 60, 2)


def main():
    wages, spae, chen, eavs, cps = (load(n) for n in ("wages.json", "spae-waits.json", "chen-waits.json", "eavs-mode.json", "cps-voting.json"))
    nat = wages["national"][DEFAULT_WAGE_SERIES]
    w_nat = nat["latest"]["value"]
    nat_latest = {"series": DEFAULT_WAGE_SERIES, "title": nat["title"], "value": w_nat, "year": nat["latest"]["year"], "month": nat["latest"]["month"]}
    default = {
        "about": "The site's default cost of casting a vote, and each input's source. Computed by pipeline/intake/cost_assemble.py from the other files in data/cost/.",
        "default_cost_dollars": dollars(DEFAULT_MINUTES, w_nat),
        "formula": f"{DEFAULT_MINUTES} minutes x ${w_nat:.2f} an hour / 60",
        "inputs": {
            "minutes": {"value": DEFAULT_MINUTES, "what": "the median time at the polling place on Election Day 2016 (smartphone measure, includes the time spent voting)",
                        "from": "model/MODEL.md section 6 (Chen, Haggag, Pope and Rohla, arXiv 1909.00024)", "mark": "stated",
                        "replication_check": {"median_minutes_of_the_154489_filtered_waits": chen["national_all_filtered_waits"]["median_minutes"],
                                              "mean_minutes": chen["national_all_filtered_waits"]["mean_minutes"],
                                              "share_over_30_minutes": chen["national_all_filtered_waits"]["share_over_30_minutes"],
                                              "file": "data/cost/chen-waits.json", "mark": "measured (computed from the authors' public file; rounds to the model's 14 and 19 minutes)"}},
            "hourly_wage": {"value": w_nat, "what": nat["title"] + " (" + nat["units"] + ")",
                            "month": f"{nat['latest']['year']}-{nat['latest']['month']:02d}", "series": DEFAULT_WAGE_SERIES,
                            "from": "FRED, Federal Reserve Bank of St. Louis (origin: U.S. Bureau of Labor Statistics, Current Employment Statistics)",
                            "mark": "stated", "file": "data/cost/wages.json",
                            "check": "FRED's value equals the BLS API's in every month the cache holds (wages.json check_against_bls)"}},
        "with_the_mean": {"minutes": MEAN_MINUTES, "dollars": dollars(MEAN_MINUTES, w_nat), "formula": f"{MEAN_MINUTES} minutes x ${w_nat:.2f} / 60"},
        "not_measured": ["travel to the polling place", "time to register", "time to learn about the contest", "child care, lost pay or other costs beyond the minutes valued at the average wage"],
        "who_it_applies_to": "a voter who votes in person; a mail voter has no line and no trip (mail shares by year: national_mode_shares)",
        "national_mode_shares": {
            "eavs_administrative": {y: {k: v[k] for k in ("national_mail_share", "national_early_in_person_share", "national_election_day_share")} for y, v in eavs["years"].items()},
            "cps_self_reported": {y: v["national_weighted_mode_shares_in_states_and_dc"] for y, v in cps["years"].items()},
            "note": "EAVS counts ballots by the way they were cast (election_day = F1b + F1e; the small remainder is UOCAVA and other); CPS is what citizens say, weighted. The two do not have to agree."},
        "sources_files": ["wages.json", "chen-waits.json", "eavs-mode.json", "cps-voting.json", "spae-waits.json"],
    }
    # states that vote almost wholly by mail, by year
    by_year = {}
    for y, v in eavs["years"].items():
        by_year[y] = sorted(st for st, s in v["states"].items() if (s.get("mail_share") or 0) >= 0.9)
    default["states_with_mail_share_at_least_90_percent_eavs"] = by_year
    default["states_with_mail_share_at_least_90_percent_eavs_note"] = "only among states whose EAVS shares are usable that year (see shares_withheld in eavs-mode.json); a state that left its modes blank cannot appear"

    out = {"about": "Every cost input by state, side by side, from the other files in data/cost/ (pipeline/intake/cost_assemble.py). Costs are minutes x hourly earnings / 60, written out.",
           "default_cost_dollars": default["default_cost_dollars"], "states": {}}
    for st in sorted(wages["states"]):
        w = wages["states"][st]
        wl = w["latest"]
        rec = {"wage": {"series": w["series"], "title": w["title"], "latest": {"year": wl["year"], "month": wl["month"], "value": wl["value"]},
                        "november_of_election_years": {y: v["november"] for y, v in w["by_election_year"].items()}}}
        bases = []
        c = chen["states"].get(st)
        if c:
            rec["chen_2016"] = {k: c[k] for k in ("mean_minutes", "median_minutes", "share_over_30_minutes", "n_waits", "se_minutes")}
            bases.append(("Chen et al. 2016, median at the polling place", c["median_minutes"]))
            bases.append(("Chen et al. 2016, mean at the polling place", c["mean_minutes"]))
        rec["spae"] = {}
        for y, v in spae["years"].items():
            s = v["states"].get(st)
            if s:
                rec["spae"][y] = {k: s[k] for k in ("n_with_wait_answer", "mean_minutes_midpoint", "mean_minutes_lower_bound", "se_minutes", "share_over_30_minutes", "thin")}
        for y in ("2022", "2020"):
            s = rec["spae"].get(y)
            if s and not s["thin"]:
                bases.append((f"SPAE {y}, mean of the answers at their midpoints (in-person voters)", s["mean_minutes_midpoint"]))
        rec["eavs"] = {}
        for y, v in eavs["years"].items():
            s = v["states"].get(st)
            if s:
                rec["eavs"][y] = {k: s.get(k) for k in ("total_ballots", "mail_share", "early_in_person_share", "election_day_share", "uocava_share")}
        rec["cps"] = {}
        for y, v in cps["years"].items():
            s = v["states"].get(st)
            if s:
                rec["cps"][y] = {k: s.get(k) for k in ("voted_share", "mail_share", "early_in_person_share", "election_day_share", "n_voters_with_mode")}
        wage_now = wl["value"]
        rec["cost_dollars"] = [{"basis": b, "minutes": m, "dollars_at_state_wage": dollars(m, wage_now),
                                "formula_state_wage": f"{m} minutes x ${wage_now:.2f} / 60", "dollars_at_national_wage": dollars(m, w_nat)} for b, m in bases]
        rec["state_wage_note"] = f"state wage is the latest month, {wl['year']}-{wl['month']:02d}; national wage ${w_nat:.2f} ({nat_latest['year']}-{nat_latest['month']:02d})"
        out["states"][st] = rec
    with open(os.path.join(COST, "national-default.json"), "w", encoding="utf-8") as f:
        json.dump(default, f, indent=1)
        f.write("\n")
    with open(os.path.join(COST, "by-state.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
        f.write("\n")
    print("default", default["default_cost_dollars"], "; states", len(out["states"]))


if __name__ == "__main__":
    main()
