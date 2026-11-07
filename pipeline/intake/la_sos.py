"""pipeline/intake/la_sos.py: Louisiana's official election results, from the Secretary of State's results site.

Written 2026-11-07 by worker D3 (briefs/D3-data-local.md, step 2) at the orchestrator's order of 08:08 ("For the 2024
legislatures of IN, LA and NJ, read each state's own certified results where a file is reachable by script, with a
gate against D2's federal counts on the same dates as for North Carolina") and of 10:17 ("Go on with LA 2024").
MEDSL's 2024 Louisiana file counts Election Day only (its README; −48.9% against D1's certified presidential count),
so its Louisiana contests are held back (data/local/REPORT.md section 6); the state's own file can take their place if
it passes the gate. Plan section 3a: data comes in by script; raw files stay in a cache outside the repository.

Source: the Secretary of State's results site, https://voterportal.sos.la.gov/. Its configuration
(/ElectionResults/GraphicalConfig) names the data and download addresses, and its list of elections
(/ElectionResults/ElectionResults/Data?blob=ElectionDates.htm) gives each date with "ResultsOfficial" ("1" is
official) [stated]. Each date's results are one workbook, the site's own download:
  https://s3-us-west-2.amazonaws.com/mediaresults.sos.la.gov/HumanReadableElectionResults/<YYYYMMDD>/
      Election+Results+(<MM-DD-YYYY>).xlsx
with a sheet "Multi-Parish(Parish)" (contests on more than one parish's ballot, by parish), "Multi-Parish(Precinct)"
(the same by precinct, not read) and one sheet per parish for its own contests (by precinct, with early voting as its
own line). Each contest is a title line ("Mayor -- Town of Melville", "Aldermen -- Village of Morse (2 to be elected)",
"Fire Protection District No. 10 -- $50 Parcel Fee Renewal - BOC - 10 Yrs."), its choices ("Name (REP)", "YES",
"NO"), and "Total Votes". The site prints no licence; these are the state's public election returns [stated: the
site; the licence: none printed].

What it does:
  fetch   downloads the list of elections and each official date's workbook of a year through pipeline/fetch.py
          (4 s between requests; a refusal stops it).
  read    writes $VOTE_CACHE/la_sos/normalized/<year>.jsonl (one contest per line) and checks-<year>.json.

Run:  VOTE_CACHE=/tmp/vote-cache python3 pipeline/intake/la_sos.py fetch|read [--year 2024]
"""
import argparse
import collections
import datetime
import json
import os
import re
import sys
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import fetch as F  # noqa: E402

SITE = "https://voterportal.sos.la.gov/"
DATES_URL = SITE + "ElectionResults/ElectionResults/Data?blob=ElectionDates.htm"
XLSX = ("https://s3-us-west-2.amazonaws.com/mediaresults.sos.la.gov/HumanReadableElectionResults/{ymd}/"
        "Election+Results+({mdy}).xlsx")
ROOT = os.path.join(F.CACHE, "la_sos")
NORM = os.path.join(ROOT, "normalized")
for _d in ("raw", "normalized"):   # fetch.py makes the cache itself, not folders inside it
    os.makedirs(os.path.join(ROOT, _d), exist_ok=True)
LICENCE = "no licence printed; the Louisiana Secretary of State's official election returns, public records"
SEATS = re.compile(r"\s*\((\d+) to be elected\)\s*$")
PARTY = re.compile(r"^(.*?)\s*\(([A-Z]+)\)\s*$")
ANSWER = re.compile(r"^(YES|NO|FOR|AGAINST)\s*(RECALL)?$", re.I)   # "ForRecall", "AgainstRecall": a recall


def _dates_name():
    return "la_sos/raw/ElectionDates.json"


def _xlsx_name(d):
    return f"la_sos/raw/{d:%Y%m%d}.xlsx"


def elections(year):
    """The official dates of `year`, from the site's list of elections: [(date, PKElectionID)]."""
    path = F.fetch(DATES_URL, _dates_name())
    with open(path, encoding="utf-8-sig") as f:
        d = json.load(f)
    out = []
    for x in d["Dates"]["Date"]:
        dt = datetime.datetime.strptime(x["ElectionDate"], "%m/%d/%Y").date()
        if dt.year == year:
            out.append((dt, x["PKElectionID"], x["ResultsOfficial"]))
    return sorted(out)


def fetch_all(year):
    out = []
    for dt, pk, official in elections(year):
        if official != "1":
            print(f"{dt}: not official on the site's list; not fetched (no live data)")
            continue
        F.fetch(XLSX.format(ymd=f"{dt:%Y%m%d}", mdy=f"{dt:%m-%d-%Y}"), _xlsx_name(dt))
        out.append(str(dt))
    return out


def _rows(ws):
    return [[x for x in r if x is not None] for r in ws.iter_rows(values_only=True)]


def _choice(s):
    s = " ".join(str(s).split())
    m = PARTY.match(s)
    return (m.group(1), m.group(2)) if m else (s, "")


def parse(path, dt):
    """The contests of one workbook: the multi-parish sheet by parish, and each parish's own sheet."""
    import openpyxl
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")   # the workbook carries no default style
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    out = []
    for sheet in wb.sheetnames:
        if sheet == "Multi-Parish(Precinct)":
            continue
        multi = sheet == "Multi-Parish(Parish)"
        rows = _rows(wb[sheet])
        i = 0
        while i < len(rows) - 2:
            r = rows[i]
            if not (len(r) == 1 and isinstance(r[0], str) and rows[i + 2][:1] == ["Total Votes"] and i >= 3
                    and not rows[i - 1]):
                i += 1
                continue
            title = " ".join(r[0].split())
            names = rows[i + 1]
            total = rows[i + 2][1:]
            if len(total) != len(names):
                raise SystemExit(f"{path} {sheet}: '{title}' has {len(names)} choices and {len(total)} totals")
            j, lines = i + 3, []
            while j < len(rows) and rows[j]:
                lines.append(rows[j])
                j += 1
            seats = SEATS.search(title)
            base = SEATS.sub("", title)
            office, _, place = base.partition(" -- ")
            question = all(ANSWER.match(str(x).strip()) for x in names)
            cands = []
            for k, x in enumerate(names):
                name, party = _choice(x)
                cands.append({"name": name, "party": party, "votes": int(total[k] or 0)})
            parishes = [str(ln[0]).strip() for ln in lines] if multi else [sheet]
            for ln in lines:   # each parish's line, or each precinct's and the early vote, adds up to the total
                if len(ln) != len(names) + 1:
                    raise SystemExit(f"{path} {sheet}: '{title}': a line of {len(ln)} cells")
            sums = [sum(int(ln[k + 1] or 0) for ln in lines) for k in range(len(names))]
            out.append({"date": str(dt), "title": title, "office": office.strip(), "place": place.strip() or None,
                        "seats": int(seats.group(1)) if seats else 1, "kind": "question" if question else "office",
                        "multi_parish": multi, "sheet": sheet, "parishes": parishes,
                        "early_voting_line": any(str(ln[0]).strip().startswith("Early Voting") for ln in lines),
                        "lines_add_up": sums == [c["votes"] for c in cands], "candidates": cands})
            i = j
    return out


def read(year):
    out, t = [], collections.Counter()
    files = {}
    for dt, pk, official in elections(year):
        if official != "1":
            continue
        name = _xlsx_name(dt)
        path = os.path.join(F.CACHE, name)
        if not os.path.exists(path):
            raise SystemExit(f"{name} is not in the cache: run fetch first")
        cs = parse(path, dt)
        files[str(dt)] = dict(F.meta(name), election_id=pk, official=official, contests=len(cs))
        for c in cs:
            t[f"{dt} {'multi-parish' if c['multi_parish'] else 'parish'} {c['kind']}"] += 1
            t["lines do not add up"] += not c["lines_add_up"]
        out += cs
    with open(os.path.join(NORM, f"{year}.jsonl"), "w") as f:
        for c in out:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    dm = F.meta(_dates_name())
    checks = {"year": year, "dates_list": {"url": dm["url"], "read_utc": dm["read_utc"], "sha256": dm["sha256"]},
              "files": files, "contests": dict(sorted(t.items()))}
    with open(os.path.join(NORM, f"checks-{year}.json"), "w") as f:
        json.dump(checks, f, indent=1)
    return out, checks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("what", choices=["fetch", "read"])
    ap.add_argument("--year", type=int, default=2024)
    a = ap.parse_args()
    if a.what == "fetch":
        print(fetch_all(a.year))
    else:
        _, checks = read(a.year)
        print(json.dumps(checks, indent=1))


if __name__ == "__main__":
    main()
