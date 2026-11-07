"""Intake: National Archives (NARA), Electoral College results by state, one page per election.

Written 2026-11-07 by worker D1 (briefs/D1-data-president.md; plan/PLAN.md section 3a).

Source: https://www.archives.gov/electoral-college/<year>, the National Archives' table for each
election: every state's electoral votes ("Electoral Vote of each State") and how its electors voted for
President and Vice-President. NARA's terms: "Works of the U.S. Government that have been produced by the
National Archives and Records Administration are in the public domain [...] under the terms of the
Creative Commons CC0 1.0 Universal license" (archives.gov/global-pages/privacy.html, as read by R1,
research/decisiveness-models-v2.md section 3.5). The tables are NARA's own.

What it writes: data/president/inputs/nara_electoral_votes.json, for every year: each state's electoral
votes (the allocation, which is what a state's result puts at stake), the electoral votes each candidate
received there, the national totals and the majority, and NARA's notes (faithless or blank electors).

Checks: the states' electoral votes sum to the printed total; the candidates' columns sum to the printed
"Total" row; 51 jurisdictions from 1964 (DC votes from 1964 under the 23rd Amendment).

Run from the repository root:  python3 pipeline/intake/nara_electoral_votes.py [first_year [last_year]]
(default 1900 to 2024). The pages go back to 1789, but before 1900 they are laid out differently (no
"Total/Majority" line in the summary table), and this parser stops there rather than guess.
"""
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import fetch  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "data", "president", "inputs", "nara_electoral_votes.json")
URL = "https://www.archives.gov/electoral-college/{y}"
NAMES = {"Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA", "Colorado": "CO",
         "Connecticut": "CT", "Delaware": "DE", "District of Columbia": "DC", "Florida": "FL", "Georgia": "GA",
         "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
         "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA",
         "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO", "Montana": "MT",
         "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM",
         "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
         "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
         "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
         "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"}


def cells(row):
    return [re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", c)).replace("\xa0", " ")).strip()
            for c in re.findall(r"<t[dh](?:\s[^>]*)?>(.*?)</t[dh]>", row, flags=re.S)]


def num(s):
    s = re.sub(r"[^0-9]", "", s)
    return int(s) if s else 0


def parse(year, text):
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)     # 2012 keeps old cells in comments
    tables = re.findall(r"<table.*?</table>", text, flags=re.S)
    summary = [cells(r) for r in re.findall(r"<tr[^>]*>(.*?)</tr>", tables[0], flags=re.S)]
    notes = " ".join(c[1] for c in summary if c and c[0].startswith("Notes") and len(c) > 1)
    total_line = next(c for c in summary if c and c[0].rstrip("*") == "Electoral Vote")
    tm = re.search(r"Total/Majority:\s*(\d+)\s*/\s*(\d+)", " ".join(total_line))
    total_ev, majority = int(tm.group(1)), int(tm.group(2))
    main = max(tables[1:], key=lambda t: t.count("<tr"))
    rows = [cells(r) for r in re.findall(r"<tr[^>]*>(.*?)</tr>", main, flags=re.S)]
    # the second header row names the presidential candidates first, then the vice-presidential ones
    orig = [re.sub(r"\s*\(\d+\)$", "", h) for h in rows[1]]   # footnote marks: "Dukakis, of Massachusetts (1)"
    head = [f"{h} ({orig[:i + 1].count(h)})" if orig.count(h) > 1 else h   # 2016 heads four columns "Other"
            for i, h in enumerate(orig)]
    n_pres = (len(head)) // 2 if len(rows[2]) == 2 + len(head) else None
    states, totals = {}, None
    for r in rows[2:]:
        if not r:
            continue
        if r[0].startswith("Total"):
            totals = [num(x) for x in r[1:]]
            continue
        if r[0].startswith(("Notes", "*")) or r[0] == "":     # 1944: a footnote row under the table
            continue
        name = re.sub(r"[\s\d*]+$", "", r[0])          # footnote marks: "Texas ***", "Indiana 1" (2024)
        if name not in NAMES:
            raise ValueError(f"{year}: unknown row {r[0]!r}")
        ev = num(r[1])
        pres = [num(x) for x in r[2:2 + n_pres]] if n_pres else []
        states[NAMES[name]] = {"ev": ev, "pres": dict(zip(head[:n_pres], pres))}
    assert sum(s["ev"] for s in states.values()) == total_ev, (year, sum(s["ev"] for s in states.values()))
    if totals is not None and n_pres:
        assert totals[0] == total_ev, (year, totals)
        for j, cand in enumerate(head[:n_pres]):
            assert sum(s["pres"][cand] for s in states.values()) == totals[1 + j], (year, cand)
    return {"total_ev": total_ev, "majority": majority, "candidates": head[:n_pres] if n_pres else [],
            "notes": notes, "states": states}


def main():
    a = sys.argv[1:]
    first = int(a[0]) if a else 1900
    last = int(a[1]) if len(a) > 1 else 2024
    doc = {"about": "National Archives electoral-vote tables, normalised by pipeline/intake/nara_electoral_votes.py."
                    " ev is the state's electoral votes; pres is how its electors voted for President.",
           "years": {}, "sources": {}}
    if os.path.exists(OUT):
        doc = json.load(open(OUT))
    for y in range(first, last + 1, 4):
        name = f"nara_electoral_college_{y}.html"
        path = fetch.fetch(URL.format(y=y), name)
        res = parse(y, open(path, encoding="utf-8", errors="replace").read())
        if y >= 1964:
            assert len(res["states"]) == 51, (y, len(res["states"]))
        doc["years"][str(y)] = res
        m = fetch.meta(name)
        doc["sources"][str(y)] = fetch.source(f"National Archives, Electoral College results, {y}", m["url"],
                                              m["read_utc"], "CC0 1.0 (NARA's own works)", "stated",
                                              sha256=m["sha256"])
        print(f"{y}: {len(res['states'])} jurisdictions, {res['total_ev']} electoral votes, majority "
              f"{res['majority']}; " + ", ".join(f"{c} {sum(s['pres'].get(c, 0) for s in res['states'].values())}"
                                                for c in res["candidates"]))
    doc["years"] = dict(sorted(doc["years"].items()))
    doc["sources"] = dict(sorted(doc["sources"].items()))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(doc, f, indent=1)
        f.write("\n")
    print(f"wrote {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
