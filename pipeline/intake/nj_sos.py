"""pipeline/intake/nj_sos.py: New Jersey's official election results, from the Division of Elections' "Official List".

Written 2026-11-07 by worker D3 (briefs/D3-data-local.md, step 2) at the orchestrator's orders of 08:08 ("For the 2024
legislatures of IN, LA and NJ, read each state's own certified results where a file is reachable by script, with a
gate against D2's federal counts on the same dates as for North Carolina") and 10:35 ("NJ 2024 as ordered ... its 2024
file holds local contests and any legislative specials; read what is there"). MEDSL's 2024 New Jersey file is 14.4%
over D1's certified presidential count, so its New Jersey contests are held back (data/local/REPORT.md section 6).
Plan section 3a: data comes in by script; raw files stay in a cache outside the repository.

Source: the Division of Elections' page for each year, https://www.nj.gov/state/elections/election-information-<year>.shtml.
It links each official result as a PDF, "Official List: Candidates for <office> For GENERAL ELECTION <date> Election",
one line per candidate and county ("BURLINGTON  DEMOCRATIC  132,275") and a "Total" line per candidate [stated: the
files]. Links inside the page's HTML comments are old drafts and are not read. The site prints no licence; these are
the state's public election returns.

What it does:
  links   lists the year page's PDF links outside its comments, with their link texts.
  read    downloads the year's official general-election results (`<year>-official-general-results-<office>.pdf`,
          the statewide lists, not the per-county copies) through pipeline/fetch.py (4 s between requests; a refusal
          stops it), reads them with pdftotext, and writes $VOTE_CACHE/nj_sos/normalized/<year>-general.json.
          Every candidate's county lines must add up to its "Total" line.

Run:  VOTE_CACHE=/tmp/vote-cache python3 pipeline/intake/nj_sos.py links|read [--year 2024]
"""
import argparse
import html
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import fetch as F  # noqa: E402

PAGE = "https://www.nj.gov/state/elections/election-information-{year}.shtml"
BASE = "https://www.nj.gov/state/elections/"
ROOT = os.path.join(F.CACHE, "nj_sos")
NORM = os.path.join(ROOT, "normalized")
for _d in ("raw", "normalized"):   # fetch.py makes the cache itself, not folders inside it
    os.makedirs(os.path.join(ROOT, _d), exist_ok=True)
LICENCE = "no licence printed; the New Jersey Division of Elections' official election returns, public records"
COUNTIES = ["ATLANTIC", "BERGEN", "BURLINGTON", "CAMDEN", "CAPE MAY", "CUMBERLAND", "ESSEX", "GLOUCESTER", "HUDSON",
            "HUNTERDON", "MERCER", "MIDDLESEX", "MONMOUTH", "MORRIS", "OCEAN", "PASSAIC", "SALEM", "SOMERSET", "SUSSEX",
            "UNION", "WARREN"]
ORDINAL = {w: i + 1 for i, w in enumerate(
    "First Second Third Fourth Fifth Sixth Seventh Eighth Ninth Tenth Eleventh Twelfth Thirteenth Fourteenth Fifteenth "
    "Sixteenth Seventeenth Eighteenth Nineteenth Twentieth".split())}
# a county line starts in the county column, 40 or more spaces in; an address line ("UNION CITY, NJ 07087") nearer
TALLY = re.compile(r"^\s{40,}(" + "|".join(COUNTIES) + r")\s*(\S.*?)\s+([\d,]+)\s*$")
TOTAL = re.compile(r"^\s{20,}Total\s+([\d,]+)\s*$")
OFFICE = re.compile(r"^\s*Candidates for (.+?)\s*$")
DISTRICT = re.compile(r"^\s*(\w+(?:-\w+)?) (Congressional|Legislative) District\b")


def links(year):
    """[(href, text)] of the year page's PDF links, outside HTML comments."""
    path = F.fetch(PAGE.format(year=year), f"nj_sos/raw/election-information-{year}.html")
    with open(path, encoding="utf-8", errors="replace") as f:
        s = f.read()
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    out = []
    for href, text in re.findall(r'<a [^>]*href="([^"]*\.pdf)"[^>]*>(.*?)</a>', s, flags=re.S):
        out.append((href, " ".join(html.unescape(re.sub(r"<[^>]+>", " ", text)).split())))
    return out


def _official_general(year):
    pat = re.compile(rf"/{year}/{year}-official-general-results-([a-z-]+)\.pdf$")
    out = []
    for href, text in links(year):
        m = pat.search(href)
        if m and not any(m.group(1).endswith("-" + c.lower().replace(" ", "")) for c in COUNTIES) \
                and not re.search(r"-district\d+$", m.group(1)):
            out.append((m.group(1), BASE + href.lstrip("/"), text))
    return out


def parse(path):
    """The contests of one Official List, [{office, district, candidates: [{name, party, slogans, total, counties}]}],
    and the list's own count of candidates (its last page, "Total Candidates").
    `party` is the name line's party column; `slogans` the county lines' own, which name the party the same way on
    every page."""
    txt = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True, check=True).stdout
    contests, office, district, cand, name_end, party_at, listed = [], None, None, None, None, None, None
    for line in txt.splitlines():
        if line.startswith("Candidate Totals for Party"):   # the last page: candidates by party, not votes
            name_end = None
            continue
        m = re.match(r"^Total Candidates\s+(\d+)\s*$", line)
        if m:
            listed = int(m.group(1))
            continue
        m = OFFICE.match(line)
        if m:
            office = m.group(1)
            continue
        if line.startswith("Name ") and "Address" in line:   # each page's header gives the columns
            name_end, party_at = line.index("Address"), line.index("Party")
            continue
        m = DISTRICT.match(line)
        if m:
            district = ORDINAL.get(m.group(1).split("-")[0], m.group(1))
            continue
        m = TALLY.match(line)
        if m and cand is not None:
            cand["counties"][m.group(1)] = cand["counties"].get(m.group(1), 0) + int(m.group(3).replace(",", ""))
            if m.group(2) not in cand["slogans"]:   # the county lines' party column ("DEMOCRATIC", "GREEN PARTY")
                cand["slogans"].append(m.group(2))
            continue
        m = TOTAL.match(line)
        if m and cand is not None:
            cand["total"] = int(m.group(1).replace(",", ""))
            cand = None
            continue
        if name_end and line[:1].strip() and line[:1] != "(" and len(line) > party_at and \
                not re.match(r"\d{2}/\d{2}/\d{4}", line) and not line.startswith("Total Candidates"):
            name = " ".join(re.sub(r"\(w\)|\*", " ", line[:name_end]).split())
            chunks = re.split(r"\s{2,}", line[name_end:].strip())
            if len(chunks) > 1:   # the address, then the party, set apart by a run of spaces
                party = chunks[-1]
            else:                 # the address ran into the party's column: the party starts after it
                at = party_at if line[party_at - 1] == " " else line.find(" ", party_at)
                if at < 0:        # or the party's own word holds the column: it starts at that word
                    at = line.rfind(" ", 0, party_at) + 1
                party = " ".join(line[at:].split())
            key = (office, district)
            if not contests or (contests[-1]["office"], contests[-1]["district"]) != key:
                contests.append({"office": office, "district": district, "candidates": []})
            last = contests[-1]["candidates"][-1] if contests[-1]["candidates"] else None
            if last is not None and last is cand and last["name"] == name:
                continue   # the same candidate again at the top of the next page: the list goes on
            cand = {"name": name, "party": party, "slogans": [], "counties": {}, "total": None}
            contests[-1]["candidates"].append(cand)
    for c in contests:
        for x in c["candidates"]:
            x["adds_up"] = x["total"] is not None and sum(x["counties"].values()) == x["total"]
        # the last candidate's name again, with no county line and a "Total" equal to all the contest's candidates'
        # votes added up: that line is the contest's total, not another candidate [measured: NJ-12, 2024]
        for x in list(c["candidates"]):
            same = [y for y in c["candidates"] if y is not x and y["name"] == x["name"]]
            if same and not x["counties"] and x["total"] == sum(y["total"] or 0 for y in c["candidates"] if y is not x):
                c["contest_total_line"] = x["total"]
                c["candidates"].remove(x)
    return contests, listed


def read(year):
    out, files = [], {}
    for office, url, text in _official_general(year):
        name = f"nj_sos/raw/{year}-official-general-results-{office}.pdf"
        path = F.fetch(url, name)
        cs, listed = parse(path)
        files[office] = dict(F.meta(name), link_text=text, contests=len(cs),
                             candidates=sum(len(c["candidates"]) for c in cs), candidates_on_last_page=listed,
                             all_add_up=all(x["adds_up"] for c in cs for x in c["candidates"]))
        out += cs
    res = {"year": year, "page": PAGE.format(year=year), "files": files, "contests": out}
    with open(os.path.join(NORM, f"{year}-general.json"), "w") as f:
        json.dump(res, f, indent=1)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("what", choices=["links", "read"])
    ap.add_argument("--year", type=int, default=2024)
    a = ap.parse_args()
    if a.what == "links":
        for href, text in links(a.year):
            print(href, "|", text)
    else:
        res = read(a.year)
        print(json.dumps(res["files"], indent=1))


if __name__ == "__main__":
    main()
