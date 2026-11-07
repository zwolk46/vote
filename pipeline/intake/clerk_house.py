"""pipeline/intake/clerk_house.py: the Clerk of the House's "Statistics of the Congressional Election", read for a
state's certified Senate and House counts in a year that D2's files (data/senate, data/house) do not reach.

Written 2026-11-07 by worker D3 (briefs/D3-data-local.md) at the orchestrator's order of 08:32: gate North Carolina's
2002 State Board file "against the Clerk of the House's statistics for the November 5, 2002 election, North Carolina's
13 House districts. ... If it passes, the State Board's 2002 counts win for every 2002 contest." The reason: a State
Board file wins over another source only where a certified count shows it complete (pipeline/local_ncsbe.py, gate).

Source: https://clerk.house.gov/member_info/electionInfo/<year>election.pdf, the Clerk's compilation of each state's
official returns, a US House publication (a federal public record; no licence printed). The PDF is turned into text
with pdftotext -layout (poppler) and read for the named states' candidate lines:
    "FOR UNITED STATES SENATOR" / "FOR UNITED STATES REPRESENTATIVE", then lines like
    " 1. Greg Dority, Republican ........ 50,907" (the number starts a district; later lines carry it on).
Each state's lines end at its "Recapitulation of Votes Cast" table, which repeats them.

Writes $VOTE_CACHE/clerk/normalized/<year>.json: {source, contests[{office, place{state, district}, special,
result{candidates[{name, party, votes}]}}]}, the subset of D2's layout that pipeline/local_ncsbe.py's gate reads.

Run:  VOTE_CACHE=/tmp/vote-cache python3 pipeline/intake/clerk_house.py 2002 --states NC
"""
import argparse
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import fetch as F  # noqa: E402

ROOT = os.path.join(F.CACHE, "clerk")
NORM = os.path.join(ROOT, "normalized")
for _d in ("raw", "normalized"):   # fetch.py makes the cache itself, not folders inside it
    os.makedirs(os.path.join(ROOT, _d), exist_ok=True)
URL = "https://clerk.house.gov/member_info/electionInfo/{year}election.pdf"
TITLE = "Clerk of the US House of Representatives, Statistics of the Congressional Election of {date}"
LICENCE = "a US House publication (federal public record); no licence printed"
STATES = {"NC": "NORTH CAROLINA"}
ALL_STATES = {"ALABAMA", "ALASKA", "ARIZONA", "ARKANSAS", "CALIFORNIA", "COLORADO", "CONNECTICUT", "DELAWARE", "FLORIDA",
              "GEORGIA", "HAWAII", "IDAHO", "ILLINOIS", "INDIANA", "IOWA", "KANSAS", "KENTUCKY", "LOUISIANA", "MAINE",
              "MARYLAND", "MASSACHUSETTS", "MICHIGAN", "MINNESOTA", "MISSISSIPPI", "MISSOURI", "MONTANA", "NEBRASKA",
              "NEVADA", "NEW HAMPSHIRE", "NEW JERSEY", "NEW MEXICO", "NEW YORK", "NORTH CAROLINA", "NORTH DAKOTA", "OHIO",
              "OKLAHOMA", "OREGON", "PENNSYLVANIA", "RHODE ISLAND", "SOUTH CAROLINA", "SOUTH DAKOTA", "TENNESSEE",
              "TEXAS", "UTAH", "VERMONT", "VIRGINIA", "WASHINGTON", "WEST VIRGINIA", "WISCONSIN", "WYOMING",
              "AMERICAN SAMOA", "DISTRICT OF COLUMBIA", "GUAM", "NORTHERN MARIANA ISLANDS", "PUERTO RICO",
              "VIRGIN ISLANDS"}
_CAND = re.compile(r"^\s*(?:(\d+)\.\s+)?(\S.*?),\s+([A-Za-z][A-Za-z\-' ]*?)\s*\.{2,}\s*([\d,]+)\s*$")


def path(year):
    return os.path.join(NORM, f"{year}.json")


def read(year, states):
    name = f"clerk/raw/{year}election.pdf"
    pdf = F.fetch(URL.format(year=year), name)
    txt = pdf + ".txt"
    subprocess.run(["pdftotext", "-layout", pdf, txt], check=True)
    with open(txt, encoding="utf-8", errors="replace") as f:
        lines = f.read().splitlines()
    heads = {v: k for k, v in STATES.items() if k in states}
    out, st, office, special, district, recap = [], None, None, False, None, False
    for ln in lines:
        s = ln.strip()
        bare = re.sub(r"\s*[—-]+\s*Continued$", "", s)
        if bare in ALL_STATES:   # a state's heading, or its "—Continued" page heading
            if heads.get(bare) != st:
                office, district, recap = None, None, False
            st = heads.get(bare)
            continue
        if not st or recap:
            continue
        if s.startswith("Recapitulation of Votes Cast"):
            recap = True
            continue
        if s.startswith("FOR UNITED STATES SENATOR"):
            office, special, district = "senate", "UNEXPIRED" in s, None
            continue
        if s.startswith("FOR UNITED STATES REPRESENTATIVE"):
            office, special, district = "house", "UNEXPIRED" in s, None
            continue
        if s == "AT LARGE":
            district = "0"
            continue
        m = _CAND.match(ln)
        if not m or not office:
            continue
        if m.group(1):
            district = m.group(1)
        key = (office, district if office == "house" else None, special)
        if not out or (out[-1]["office"], out[-1]["place"]["district"], out[-1]["special"]) != key \
                or out[-1]["place"]["state"] != st:
            out.append({"office": office, "place": {"state": st, "district": key[1]}, "special": special,
                        "result": {"candidates": []}})
        out[-1]["result"]["candidates"].append({"name": m.group(2).strip(), "party": m.group(3).strip(),
                                                "votes": int(m.group(4).replace(",", ""))})
    meta = F.meta(name)
    src = F.source(TITLE.format(date=f"November {year}"), meta["url"], meta["read_utc"], LICENCE, mark="stated",
                   note="the Clerk's compilation of the states' official returns; read by pipeline/intake/clerk_house.py "
                        "with pdftotext -layout", sha256=meta["sha256"])
    with open(path(year), "w") as f:
        json.dump({"source": src, "states": sorted(states), "contests": out}, f, indent=1)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("year", type=int)
    ap.add_argument("--states", default="NC")
    a = ap.parse_args()
    out = read(a.year, a.states.split(","))
    for c in out:
        print(c["place"]["state"], c["office"], c["place"]["district"], c["special"],
              [(x["party"], x["votes"]) for x in c["result"]["candidates"]])


if __name__ == "__main__":
    main()
