"""pipeline/intake/nm_sos.py: New Mexico's official results for its Public Education Commission, by district.

Written 2026-11-07 by worker D3 on the orchestrator's ruling of 16:19: "NM's PEC members are elected by district, so
find the district or hold them". Reason (the orchestrator): "a race's class is set by what the contest elects". MEDSL's
2022 file gives New Mexico's Public Education Commissioner contests no district [measured: its rows' district column is
empty], so its five candidates, each the only name in precincts of its own, were read as five contests of no district.
Plan section 3a: data comes in by script; raw files stay in a cache outside the repository.

Source: the Secretary of State's results archive, https://www.sos.nm.gov/sos-archive/election-results-archive/
<year>-election-results/, links "<year> General Election Official Results" to its results site (electionresults.sos.
nm.gov, eid <n>). That site's own menu links "Public Education Commission", resultsSW.aspx?type=ECX&map=CTY&eid=<n>:
one block per contest ("Public Education Commissioner DISTRICT 2"), each candidate's name, party and votes, the
contest's "total votes", and its precincts reported ("Precincts Fully: 238 / 238") [stated: the page]. The page marks
its results official in the archive's link text [stated]. The site prints no licence; these are the state's public
election returns.

What it does:
  read   fetches the archive page and the year's Public Education Commission page through pipeline/fetch.py (4 s
         between requests; a refusal stops it), checks that the archive links the year's general's official results
         to the eid read, that every contest's candidates add up to its total and that every precinct reported, and
         writes $VOTE_CACHE/nm_sos/normalized/<year>-pec.json.

Run:  VOTE_CACHE=/tmp/vote-cache python3 pipeline/intake/nm_sos.py read --year 2022
"""
import argparse
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import fetch as F  # noqa: E402

ARCHIVE = "https://www.sos.nm.gov/sos-archive/election-results-archive/{year}-election-results/"
PEC = "https://electionresults.sos.nm.gov/resultsSW.aspx?type=ECX&map=CTY&eid={eid}"
EID = {2022: 2838}   # the archive's "2022 General Election Official Results" link, electionresults.sos.nm.gov/?eid=2838
ROOT = os.path.join(F.CACHE, "nm_sos")
NORM = os.path.join(ROOT, "normalized")
for _d in ("raw", "normalized"):   # fetch.py makes the cache itself, not folders inside it
    os.makedirs(os.path.join(ROOT, _d), exist_ok=True)
LICENCE = "no licence printed; the New Mexico Secretary of State's official election returns, public records"


def _num(s):
    return int(s.replace(",", "").strip())


def parse(path):
    """[{office, district, candidates: [{name, party, votes}], total, precincts: [fully, of]}] of one results page."""
    with open(path, encoding="utf-8", errors="replace") as f:
        s = f.read()
    blocks = re.split(r'<div class="display-results-box-a">\s*<h1>', s)[1:]
    out = []
    for b in blocks:
        title = html.unescape(b[:b.index("</h1>")]).strip()
        m = re.match(r"^(.*?)\s+DISTRICT\s+(\d+)$", title)
        if not m:
            raise SystemExit(f"nm_sos: a contest's title is not '<office> DISTRICT <n>': {title!r}")
        cands = [{"name": " ".join(html.unescape(n).split()), "party": html.unescape(p).strip(), "votes": _num(v)}
                 for n, p, v in re.findall(r'display-results-box-d">\s*<h1>([^<]*)</h1>\s*<h2[^>]*>([^<]*)</h2>.*?'
                                           r'display-results-box-f">\s*<h1>([\d,]+)</h1>', b, flags=re.S)]
        total = re.search(r'display-results-box-total">\s*<h2>([\d,]+)</h2>', b)
        prec = re.search(r"Precincts Fully:\s*([\d,]+)\s*/\s*([\d,]+)", b)
        out.append({"office": m.group(1), "district": m.group(2), "candidates": cands,
                    "total": _num(total.group(1)) if total else None,
                    "precincts": [_num(prec.group(1)), _num(prec.group(2))] if prec else None})
    return out


def read(year):
    eid = EID[year]
    a = F.fetch(ARCHIVE.format(year=year), f"nm_sos/raw/{year}-election-results.html")
    with open(a, encoding="utf-8", errors="replace") as f:
        arch = f.read()
    texts = [html.unescape(t).strip() for t in
             re.findall(rf'href="https://electionresults\.sos\.nm\.gov/\?eid={eid}"[^>]*>([^<]*)<', arch)]
    want = f"{year} General Election Official Results"
    if want not in texts:   # the page links it twice: an image's link, then the text's
        raise SystemExit(f"nm_sos: the {year} archive does not link eid {eid} as the general's official results")
    name = f"nm_sos/raw/{year}-general-pec-{eid}.html"
    contests = parse(F.fetch(PEC.format(eid=eid), name))
    for c in contests:
        c["adds_up"] = c["total"] == sum(x["votes"] for x in c["candidates"])
        c["all_precincts"] = bool(c["precincts"]) and c["precincts"][0] == c["precincts"][1]
    res = {"year": year, "archive": dict(F.meta(f"nm_sos/raw/{year}-election-results.html"),
                                         link_text=want),
           "page": dict(F.meta(name)), "licence": LICENCE, "contests": contests}
    if not contests or not all(c["adds_up"] and c["all_precincts"] for c in contests):
        raise SystemExit(f"nm_sos: {year}: a contest does not add up or did not report every precinct")
    with open(os.path.join(NORM, f"{year}-pec.json"), "w") as f:
        json.dump(res, f, indent=1)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("what", choices=["read"])
    ap.add_argument("--year", type=int, default=2022)
    a = ap.parse_args()
    res = read(a.year)
    for c in res["contests"]:
        print(c["office"], c["district"], c["candidates"], c["total"], c["precincts"])


if __name__ == "__main__":
    main()
