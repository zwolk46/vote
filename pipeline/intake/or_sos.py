"""pipeline/intake/or_sos.py: Oregon's official abstract of votes of the 2024 general election, for the statewide
contests MEDSL's file holds in part.

Written 2026-11-07 by worker D3 on the orchestrator's orders of 17:44 ("read held contests' certified totals where the
agency answers ... ID and OR SoS"), 19:49 (item 4: "a file name in a URL is not a mark. Two things count: a mark
printed on the document, or the agency's own words for it on the page that links it (the link text or the records
system's title) ... If the agency's page calls it "Official Results", it counts and you record those words") and
20:28 ("OR 2024's mark with its one request"). Reason (the ruling of 16:47): a statewide contest whose lines miss
counties that voted that day is held unless the state's own total is read, since a partial count would show the
wrong n and could draw the wrong winner. Plan section 3a: data comes in by script; raw files stay in a cache outside
the repository.

Sources, kept in $VOTE_CACHE/or_sos/raw (each with a .meta.json):
  or-2024-general-abstract.pdf   the Secretary of State's records system, DocumentStream.ashx?uri=13735458 (read
      2026-11-07 19:38:47 UTC; found by a web search for its heading). Headed on every page "November 5, 2024, General
      Election Abstract of Votes"; one page per contest, a line per county with each candidate's votes, a "Total" line,
      "** Elected" beside the winner [stated: the document]. The document prints no word "official" or "certified".
  or-2024-abstract-record-viewer.html   the records system's Record Viewer for the same record (ORSOSWebDrawer/
      Recordhtml/13735458, redirected to ORSOSCMSearch/Search/RecordViewer.aspx?uri=13735458; one request, 20:56:06
      UTC), which titles the record "2024 November General Election Official Results(2).PDF" (its lblTitle) and shows
      the document from the same DocumentStream address [stated: the page]. That is the records system's title, which
      the ruling of 19:49 counts; the title is the uploaded file's own name, kept by the records system.
The state prints no licence; these are its public election returns.

Oregon 2022: no abstract of the 2022 general election was found (two web searches of the state's hosts, 20:57 UTC,
found its statistical summary and some counties' canvasses only), so none was requested, and the 2022 contest MEDSL
holds in part stays held.

What it does (read): checks that the record viewer titles the record with the words "Official Results" and shows the
same document; reads each contest of CONTESTS from the abstract (its candidates, the county lines and the Total line);
checks that there are 36 county lines and that each candidate's county lines add up to the Total line (the gate: a
contest that fails it is written with its differences and not used, pipeline/local_medsl.py _or_state); writes
$VOTE_CACHE/or_sos/normalized/2024-general.json. No request is made.

Found [measured]: Position 7 passes. Position 1's write-in line ("Misc.") does not: its county lines add up to 26,078,
its Total line reads 26,077; the named candidate's lines add up exactly.

Run:  VOTE_CACHE=/tmp/vote-cache python3 -I pipeline/intake/or_sos.py read
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

ROOT = os.path.join(F.CACHE, "or_sos")
RAW = os.path.join(ROOT, "raw")
NORM = os.path.join(ROOT, "normalized")
ABSTRACT = "or-2024-general-abstract.pdf"
VIEWER = "or-2024-abstract-record-viewer.html"
URI = "13735458"
HEADING = "November 5, 2024, General Election Abstract of Votes"
# the abstract's title and position, and MEDSL's office and district for the contest
CONTESTS = [("Judge of the Supreme Court", "Position 1", "JUDGE OF THE SUPREME COURT", "POSITION 1"),
            ("Judge of the Supreme Court", "Position 7", "JUDGE OF THE SUPREME COURT", "POSITION 7")]
COUNTIES = 36
LICENCE = "no licence printed; the Oregon Secretary of State's public election returns"


def _need(name):
    p = os.path.join(RAW, name)
    if not (os.path.exists(p) and os.path.exists(p + ".meta.json")):
        raise SystemExit(f"{p} (and its .meta.json) is not in the cache")
    with open(p + ".meta.json") as f:
        return p, json.load(f)


def viewer_title(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        s = f.read()
    m = re.search(r'<span id="lblTitle">(.*?)</span>', s, re.S)
    if not m:
        raise SystemExit("or_sos: the record viewer has no title")
    shows = f"DocumentStream.ashx?uri={URI}" in s
    return html.unescape(m.group(1)).strip(), shows


def _num(t):
    return int(t.replace(",", ""))


def contest(pages, title, position):
    """{candidates: [{name, votes, elected, misc}], counties: {county: [votes]}, total: [votes]} from the contest's page."""
    hit = []
    for pg in pages:
        lines = pg.split("\n")
        for i, l in enumerate(lines):
            if l.strip() == title and i + 1 < len(lines) and lines[i + 1].strip() == position:
                hit.append((lines, i))
    if len(hit) != 1:
        raise SystemExit(f"or_sos: {title}, {position}: found on {len(hit)} pages")
    lines, i = hit[0]
    if not any(HEADING in l for l in lines[:i]):
        raise SystemExit(f"or_sos: {title}, {position}: the page is not headed {HEADING!r}")
    j = i + 2
    last = [t for t in re.split(r"\s{2,}", lines[j].strip()) if t]
    k = next(n for n in range(j + 1, len(lines)) if lines[n].strip().startswith("County"))
    first = [t for t in re.split(r"\s{2,}", lines[k].strip()[len("County"):].strip()) if t]
    counties, total = {}, None
    for l in lines[k + 1:]:
        m = re.match(r"^\s*([A-Z][A-Za-z .]+?)\s{2,}([\d,]+(?:\s+[\d,]+)*)\s*$", l)
        if not m:
            if counties and total is not None:
                break
            continue
        nums = [_num(x) for x in m.group(2).split()]
        if m.group(1).strip() == "Total":
            total = nums
        else:
            counties[m.group(1).strip()] = nums
    if total is None or len(total) != len(last):
        raise SystemExit(f"or_sos: {title}, {position}: {len(last)} columns named, a Total line of {total}")
    named = [x for x in last if x != "Misc."]
    if len(first) != len(named):
        raise SystemExit(f"or_sos: {title}, {position}: first names {first} against surnames {named}")
    fn = iter(first)
    cands = []
    for col, x in enumerate(last):
        misc = x == "Misc."
        sur = x.lstrip("*")
        cands.append({"name": "Misc." if misc else f"{next(fn)} {sur}", "surname": None if misc else sur,
                      "votes": total[col], "elected": x.startswith("**"), "misc": misc})
    diff = [f"{c['name']}: its county lines add up to {sum(v[col] for v in counties.values()):,}, its Total line "
            f"{total[col]:,}" for col, c in enumerate(cands) if sum(v[col] for v in counties.values()) != total[col]]
    if len(counties) != COUNTIES:
        diff.append(f"{len(counties)} county lines, not {COUNTIES}")
    return {"title": title, "position": position, "candidates": cands, "counties": counties,
            "adds_up": not diff, "differences": diff}


def read():
    pdf, pdf_meta = _need(ABSTRACT)
    view, view_meta = _need(VIEWER)
    title, shows = viewer_title(view)
    if "Official Results" not in title or not shows:
        raise SystemExit(f"or_sos: the record viewer titles the record {title!r} (shows the document: {shows})")
    txt = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True, check=True).stdout
    pages = txt.split("\f")
    out = []
    for t, pos, office, district in CONTESTS:
        c = contest(pages, t, pos)   # a contest that fails the gate is written with its differences, and not used
        c.update({"office": office, "district": district})
        out.append(c)
    res = {"year": 2024, "election": HEADING,
           "source": {"abstract": pdf_meta, "viewer": view_meta, "licence": LICENCE,
                      "mark": f"the records system titles the record {title!r} (its Record Viewer, which shows the "
                              f"document)", "title": title,
                      "check": f"each candidate's {COUNTIES} county lines add up to its Total line"},
           "contests": out}
    os.makedirs(NORM, exist_ok=True)
    with open(os.path.join(NORM, "2024-general.json"), "w") as f:
        json.dump(res, f, indent=1, ensure_ascii=False)
    for c in out:
        print(f"{c['title']}, {c['position']}: " + ", ".join(f"{x['name']} {x['votes']:,}"
                                                           + (" (elected)" if x["elected"] else "")
                                                           for x in c["candidates"])
              + f"; {len(c['counties'])} counties, adding up: {c['adds_up']}"
              + (f" ({'; '.join(c['differences'])})" if c["differences"] else ""))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["read"])
    ap.parse_args()
    read()


if __name__ == "__main__":
    main()
