"""pipeline/intake/fivethirtyeight_checking_our_work.py: FiveThirtyEight's published forecasts, as kept in its
repository "checking-our-work-data", for every race it forecast. One script for the whole repository: the
Senate, House and governor files are read here (worker D2); the presidential files are to be added to this
same script (worker D1), not to a second one (plan section 3a; the orchestrator, 2026-11-07 04:12 UTC).

Source. FiveThirtyEight, "checking-our-work-data", https://github.com/fivethirtyeight/checking-our-work-data,
the data behind "How Good Are FiveThirtyEight Forecasts?". Read at commit f6d5b2e1d6da2889345d381c41431f9a4ee208dd
("Update forecasts", 2023-02-02) through raw.githubusercontent.com (public files; allowed by the orchestrator,
2026-11-07 03:46). Licence: Creative Commons Attribution 4.0 International (the repository's LICENSE file,
read here), so a figure taken from it is shown with "FiveThirtyEight" named.

Files and columns (each row: one candidate in one race in one version of one day's forecast):
  us_senate_elections.csv, governors_elections.csv:
      year, office, state, special, election_date, forecast_date, forecast_type, party, candidate,
      projected_voteshare, actual_voteshare, probwin, probwin_outcome
  us_house_elections.csv: the same with district in place of special.
  Coverage: Senate 2008-2022 (vote shares from 2014 on), House 2010 and 2018-2022 (vote shares from 2018),
  governors 2010, 2018, 2022 (vote shares from 2018). forecast_type: lite, classic, deluxe (2018-2022);
  polls-plus, polls-only, now-cast (2016); none before. State is a postal code except in 2014 (full names);
  "US" rows are the national forecast of the chamber; special is "true", "1" or blank-or-false.

What this script keeps: for each race and each version, the last forecast dated before Election Day (the
orchestrator, 04:12: "use the last forecast dated before Election Day, and record its date as as_of"); where
the file holds no forecast before Election Day (2008, 2010: one forecast, dated Election Day), that one,
marked. For each candidate in it: party, name, projected share (in percent, as printed), chance (probwin).

Run:  python3 pipeline/intake/fivethirtyeight_checking_our_work.py
Writes CACHE/fivethirtyeight/normalized/checking_our_work_congress.json:
  {"source": {...}, "versions_order": {"senate": {"2018": ["lite", ...]}}, "races": {"senate|2018|AZ|-|0":
   {"versions": {"lite": {"as_of", "dated_election_day", "candidates": [{"party", "name", "share", "chance",
   "actual"}]}}}}}
Also kept: "simulations", the run count each year's version moved in steps of (every chance a multiple of
1/N; inferred), and "share_decimals", the printed precision of the projected shares.
Checks: every race has a D or an R row; within one race, version and date, the chances sum to 1 (within 0.01).
"""
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import congress_common as cc  # noqa: E402

COMMIT = "f6d5b2e1d6da2889345d381c41431f9a4ee208dd"
BASE = f"https://raw.githubusercontent.com/fivethirtyeight/checking-our-work-data/{COMMIT}/"
FILES = {"senate": "us_senate_elections.csv", "house": "us_house_elections.csv",
         "governor": "governors_elections.csv"}
NAME_TO_ABBR = {v: k for k, v in cc.STATE_NAMES.items()}


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def race_key(level, year, state, district, special):
    return f"{level}|{year}|{state}|{district or '-'}|{1 if special else 0}"


def main():
    lic = cc.fetch(BASE + "LICENSE", "fivethirtyeight/cow/LICENSE", min_bytes=1000)
    with open(os.path.join(cc.CACHE, lic["path"])) as f:
        licence_text = f.read(200)
    assert "Attribution 4.0 International" in licence_text, licence_text[:80]
    races, order, checks, reads = {}, {}, [], {}
    for level, fname in FILES.items():
        rec = cc.fetch(BASE + fname, f"fivethirtyeight/cow/{fname}", min_bytes=100000)
        reads[level] = rec
        order[level] = {}
        rows = {}
        with open(os.path.join(cc.CACHE, rec["path"]), newline="") as f:
            for r in csv.DictReader(f):
                st = r["state"] if len(r["state"]) == 2 else NAME_TO_ABBR.get(r["state"], r["state"])
                if st == "US":
                    continue
                y = int(r["year"])
                vt = r["forecast_type"] or "only"
                order[level].setdefault(str(y), [])
                if vt not in order[level][str(y)]:
                    order[level][str(y)].append(vt)
                dist = None
                if level == "house":
                    dist = f"{int(r['district']):02d}" if r["district"].isdigit() else r["district"]
                special = r.get("special", "").lower() in ("true", "1")
                k = race_key(level, y, st, dist, special)
                rows.setdefault(k, {}).setdefault(vt, {}).setdefault(r["forecast_date"], []).append(
                    {"party": r["party"], "name": r["candidate"] or None,
                     "share": num(r["projected_voteshare"]), "chance": num(r["probwin"]),
                     "actual": num(r["actual_voteshare"]), "election_date": r["election_date"]})
        for k, by_v in rows.items():
            out = {}
            for vt, by_date in by_v.items():
                eday = next(iter(by_date.values()))[0]["election_date"]
                before = [d for d in by_date if d < eday]
                day = max(before) if before else max(by_date)
                cands = [{x: a[x] for x in ("party", "name", "share", "chance", "actual")} for a in by_date[day]]
                s = sum(a["chance"] or 0 for a in cands)
                if abs(s - 1) > 0.01:
                    checks.append(f"{k} {vt} {day}: chances sum to {s:.3f}")
                if not any(a["party"] in ("D", "R") for a in cands):
                    checks.append(f"{k} {vt}: no D or R row")
                out[vt] = {"as_of": day, "dated_election_day": not before, "election_date": eday,
                           "candidates": cands}
            races[k] = {"versions": out}
    # The chances move in fixed steps where 538 counted simulation runs: every chance is a multiple of 1/N.
    # N is the smallest of the usual run counts that fits 99% of the chances of a year's version (inferred;
    # the orchestrator, 04:20: "if 538's chances move in fixed steps, take the step as one simulation run").
    # None where no step fits (Senate 2014). The shares' printed precision: decimals of the percent.
    steps, share_decimals = {}, {}
    for k, r in races.items():
        level, year = k.split("|")[:2]
        for vt, f in r["versions"].items():
            key = (level, year, vt)
            for a in f["candidates"]:
                if a["chance"] is not None and 0 < a["chance"] < 1:
                    steps.setdefault(key, []).append(a["chance"])
                if a["share"] is not None:
                    t = repr(a["share"])
                    share_decimals[key] = max(share_decimals.get(key, 0), len(t.split(".")[1]) if "." in t else 0)
    sims = {}
    for (level, year, vt), vs in steps.items():
        n_fit = None
        for N in (1000, 2000, 4000, 5000, 10000, 20000, 25000, 40000, 50000, 100000):
            if sum(1 for v in vs if abs(v * N - round(v * N)) < 1e-6) / len(vs) >= 0.99:
                n_fit = N
                break
        sims.setdefault(level, {}).setdefault(year, {})[vt] = n_fit
    decs = {}
    for (level, year, vt), dd in share_decimals.items():
        decs.setdefault(level, {}).setdefault(year, {})[vt] = dd
    src = {level: cc.source_block(
        f"FiveThirtyEight, checking-our-work-data, {FILES[level]} (the data behind \"How Good Are "
        f"FiveThirtyEight Forecasts?\"), commit {COMMIT[:7]}", reads[level]["url"], reads[level]["read_utc"],
        "CC BY 4.0 (the repository's LICENSE)", mark="stated",
        via="https://github.com/fivethirtyeight/checking-our-work-data",
        note=f"sha256 {reads[level]['sha256'][:16]}") for level in FILES}
    out = {"source": src, "versions_order": order, "simulations": sims, "simulations_mark": "inferred",
           "share_decimals": decs, "races": races, "checks": checks}
    cc.write_json(os.path.join(cc.CACHE, "fivethirtyeight", "normalized", "checking_our_work_congress.json"), out)
    n = {L: sum(1 for k in races if k.startswith(L + "|")) for L in FILES}
    print(f"538 checking-our-work: races {n}; checks: {len(checks)}; simulation runs (inferred): {sims}")
    for c in checks[:15]:
        print("  ", c)


if __name__ == "__main__":
    main()
