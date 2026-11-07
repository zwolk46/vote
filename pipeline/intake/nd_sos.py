"""pipeline/intake/nd_sos.py: North Dakota's official results of a general election, its statewide and judicial contests.

Written 2026-11-07 by worker D3 on the orchestrator's ruling of 16:47: "ND's 8: retype them from the state's results if
they are district court seats", and "(c) If it still misses counties: use the state's marked total, if one is read, as
the record's count". Reason (the orchestrator): "a shown figure has to be the whole contest's count of record". MEDSL's
2022 file names North Dakota's district court judgeships "JUSTICE OF THE SUPREME COURT", with the judicial district in
the district column, and adds each district's judgeships up into one contest of one seat [measured: eight such contests,
one of six names]; its 2024 file misses Eddy County (38027) from the State Auditor's contest [measured].
Plan section 3a: data comes in by script; raw files stay in a cache outside the repository.

Source: the Secretary of State's "Election Results" page, https://www.sos.nd.gov/elections/election-results, links each
general's results ("General Election - November 8, 2022") to the state's results site, results.sos.nd.gov, whose front
page heads them "Official 2022 General Election Results" (<h1><span>Official</span> 2022 General Election Results</h1>)
[stated: the page's HTML], and links its "Statewide" and "Judicial" contests (ResultsSW.aspx, type SW and JD). Each
contest is a block: its name ("Judge of the District Court No. 1 Northeast Central"), "Vote For 1", "Precincts Fully:
21 / 21", each candidate's name, party and votes, the row of each winner marked "Elected contest-wide", and its "Total
Votes" [stated: the page]. The pages are server-written HTML, read by curl; no data endpoint is called. The site prints
no licence; these are the state's public election returns.

What it does:
  read   fetches the archive page, the year's front page and its statewide and judicial pages through
         pipeline/fetch.py (4 s between requests; a refusal stops it), checks that the archive links the general to the
         front page, that the front page carries the official heading and links both pages, that every contest's
         candidates add up to its total and that every precinct reported, and writes
         $VOTE_CACHE/nd_sos/normalized/<year>-general.json.

Run:  VOTE_CACHE=/tmp/vote-cache python3 pipeline/intake/nd_sos.py read --year 2022
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

ARCHIVE = "https://www.sos.nd.gov/elections/election-results"
SITE = "https://results.sos.nd.gov/"
# the archive's link for each general [stated: the archive page, read 2026-11-07]: its words, and the front page
GENERAL = {2022: ("General Election - November 8, 2022", "Default.aspx?map=Cty&eid=vxUYQ0lrpP4."),
           2024: ("General Election - November 5, 2024", "Default.aspx?map=Cty")}
PAGES = {"statewide": "ResultsSW.aspx?text=All&type=SW&map=CTY", "judicial": "ResultsSW.aspx?text=Race&type=JD&map=CTY&area=District"}
ROOT = os.path.join(F.CACHE, "nd_sos")
NORM = os.path.join(ROOT, "normalized")
for _d in ("raw", "normalized"):   # fetch.py makes the cache itself, not folders inside it
    os.makedirs(os.path.join(ROOT, _d), exist_ok=True)
LICENCE = "no licence printed; the North Dakota Secretary of State's official election returns, public records"


def _text(s):
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", s)).split())


def _num(s):
    return int(s.replace(",", "").strip())


def parse(path):
    """[{office, vote_for, precincts: [fully, of], candidates: [{name, party, votes, won}], total}] of one page."""
    with open(path, encoding="utf-8", errors="replace") as f:
        s = f.read()
    out = []
    for b in re.split(r'<div class="display-results-box-a">', s)[1:]:
        title = _text(re.search(r"<h1>(.*?)</h1>", b, re.S).group(1))
        vote_for = re.search(r"<h2>\s*Vote For (\d+)\s*</h2>", b)
        prec = re.search(r"Precincts Fully:\s*([\d,]+)\s*/\s*([\d,]+)", b)
        body = b[b.index("candidate-rows"):b.index("display-results-box-totalvotes")]
        cands = []
        for row in re.split(r'<div class="section group', body)[1:]:
            name = re.search(r'display-results-box-d"[^>]*>\s*<h2>(.*?)</h2>', row, re.S)
            votes = re.search(r'display-results-box-g"[^>]*>([\d,]+)</h2>', row)
            party = re.search(r'display-results-box-e">\s*<div[^>]*>([^<]*)</div>', row)
            if not (name and votes):
                raise SystemExit(f"nd_sos: {title!r}: a candidate row without a name or votes")
            n = _text(name.group(1))
            if n.split() == ["write-in", "write-in"]:   # the page's write-in row prints its label twice (shown, hidden)
                n = "write-in"
            cands.append({"name": n, "party": party.group(1).strip() if party else None, "votes": _num(votes.group(1)),
                          "won": row.lstrip().startswith("winner") or ' winner"' in row[:40],
                          "writein": n == "write-in"})
        total = re.search(r'display-results-box-total">([\d,]+)</h2>', b)
        out.append({"office": title, "vote_for": int(vote_for.group(1)) if vote_for else None,
                    "precincts": [_num(prec.group(1)), _num(prec.group(2))] if prec else None,
                    "candidates": cands, "total": _num(total.group(1)) if total else None})
    return out


def read(year):
    words, front = GENERAL[year]
    a = F.fetch(ARCHIVE, f"nd_sos/raw/election-results-{year}.html")
    with open(a, encoding="utf-8", errors="replace") as f:
        arch = f.read()
    links = [(html.unescape(h), _text(t)) for h, t in re.findall(r'href="([^"]+)"[^>]*>(.*?)</a>', arch, re.S)]
    if (SITE + front, words) not in links:
        raise SystemExit(f"nd_sos: the archive does not link {words!r} to {SITE + front}")
    fp = F.fetch(SITE + front, f"nd_sos/raw/{year}-general-front.html")
    with open(fp, encoding="utf-8", errors="replace") as f:
        fs = f.read()
    heading = f"<h1><span>Official</span> {year} General Election Results</h1>"
    if heading not in fs:
        raise SystemExit(f"nd_sos: the {year} front page does not carry {heading!r}")
    eid = front.split("eid=")[1] if "eid=" in front else None
    res = {"year": year, "archive": dict(F.meta(f"nd_sos/raw/election-results-{year}.html"), link_text=words),
           "front": dict(F.meta(f"nd_sos/raw/{year}-general-front.html"), official=heading), "licence": LICENCE,
           "pages": {}, "contests": {}}
    for k, rel in PAGES.items():
        url = SITE + rel + (f"&eid={eid}" if eid else "")
        if rel not in fs and rel.replace("&", "&amp;") not in fs:
            raise SystemExit(f"nd_sos: the {year} front page does not link its {k} page ({rel})")
        name = f"nd_sos/raw/{year}-general-{k}.html"
        page = F.fetch(url, name)
        with open(page, encoding="utf-8", errors="replace") as f:
            if heading not in f.read():
                raise SystemExit(f"nd_sos: the {year} {k} page does not carry {heading!r}")
        cs = parse(page)
        for c in cs:
            c["adds_up"] = c["total"] == sum(x["votes"] for x in c["candidates"])
            c["all_precincts"] = bool(c["precincts"]) and c["precincts"][0] == c["precincts"][1]
        if not cs or not all(c["adds_up"] and c["all_precincts"] for c in cs):
            raise SystemExit(f"nd_sos: {year} {k}: a contest does not add up or did not report every precinct")
        res["pages"][k] = dict(F.meta(name))
        res["contests"][k] = cs
    with open(os.path.join(NORM, f"{year}-general.json"), "w") as f:
        json.dump(res, f, indent=1)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("what", choices=["read"])
    ap.add_argument("--year", type=int, default=2022)
    a = ap.parse_args()
    res = read(a.year)
    for k, cs in res["contests"].items():
        for c in cs:
            print(k, "|", c["office"], c["vote_for"], c["precincts"], [(x["name"], x["votes"], x["won"]) for x in c["candidates"]])


if __name__ == "__main__":
    main()
