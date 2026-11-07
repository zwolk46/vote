"""pipeline/intake/nara_electoral_college.py: who won each presidential election, from the National
Archives' Electoral College results pages.

Source. National Archives and Records Administration, Office of the Federal Register, "Electoral College
Results", one page per election (https://www.archives.gov/electoral-college/<year>), each printing the
President and Vice President elected, their party, and the electoral votes. A federal public record; no
licence printed.

Why. The model's own forecast for Senate, House and governor races uses one fact about each year known
before the election: which party held the presidency (the president's party tends to lose ground at a
midterm). Control of the Senate at 50-50 turns on the Vice President's vote, so the Vice President in
office when the new Senate meets is needed too: after a presidential election, the one just elected;
after a midterm, the one in office.

Run:  python3 pipeline/intake/nara_electoral_college.py [first_year last_year]   (default 1976 2024)
      python3 pipeline/intake/nara_electoral_college.py states [first_year last_year]  (default 1900 2024)
Writes CACHE/nara/normalized/electoral_college.json: [{"year", "president", "party", "vice_president",
"electoral_votes", "opponent", "opponent_party", "source"}].
Checks: the winner's electoral votes reach the printed majority.

`states` (added by D1 for the presidency, 2026-11-07; moved here from D1's nara_electoral_votes.py so that
the National Archives' pages have one script, plan section 3a) reads the same pages' state tables: each
state's electoral votes and how its electors voted for President, with NARA's notes (faithless and blank
electors), and writes data/president/inputs/nara_electoral_votes.json, committed. Reason: the College
stage needs every state's electoral votes in every year. Checks: the states' votes sum to the printed total;
each candidate's column sums to the printed "Total" row; 51 jurisdictions from 1964. Before 1900 the pages
are laid out differently (no "Total/Majority" line in the summary table), and the parser stops there rather
than guess. NARA's privacy page puts NARA's own works under CC0 1.0 (research/decisiveness-models-v2.md
section 3.5).
"""
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import congress_common as cc  # noqa: E402

URL = "https://www.archives.gov/electoral-college/{y}"
LICENCE = "US federal public record (National Archives); no licence printed"


def text(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        t = f.read()
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S)
    t = html.unescape(re.sub(r"<[^>]+>", "\n", t))
    return [x.strip() for x in t.splitlines() if x.strip()]


def parse(year):
    rec = cc.fetch(URL.format(y=year), f"nara/electoral_college_{year}.html", min_bytes=5000)
    L = text(os.path.join(cc.CACHE, rec["path"]))
    i = L.index(f"{year} Electoral College Results")
    block = L[i:i + 40]

    def after(label):
        j = block.index(label)
        return block[j + 1]
    pres = after("President")
    opp = after("Main Opponent")
    m, mo = re.match(r"(.+?)\s*\[(\w+)\]", pres), re.match(r"(.+?)\s*\[(\w+)\]", opp)
    win_ev = int(re.search(r"Winner:\s*(\d+)", " ".join(block)).group(1))
    total, majority = map(int, re.search(r"Total/Majority:\s*(\d+)/(\d+)", " ".join(block)).groups())
    # "Richard B. Cheney (286)" in older pages, "Kamala D. Harris [D]" in 2020 and 2024
    vp = re.match(r"(.+?)\s*[\(\[]", after("Vice President") + " (")
    out = {"year": year, "president": m.group(1), "party": m.group(2), "electoral_votes": win_ev,
           "total": total, "majority": majority, "opponent": mo.group(1), "opponent_party": mo.group(2),
           "vice_president": vp.group(1) if vp else None,
           "source": cc.source_block(f"National Archives, {year} Electoral College Results", rec["url"],
                                     rec["read_utc"], LICENCE, mark="stated")}
    if win_ev < majority:
        out["check"] = f"winner's {win_ev} electoral votes are under the majority {majority}"
    return out


def main(first, last):
    rows = [parse(y) for y in range(first, last + 1, 4)]
    cc.write_json(os.path.join(cc.CACHE, "nara", "normalized", "electoral_college.json"), rows)
    for r in rows:
        print(f"{r['year']}: {r['president']} [{r['party']}] {r['electoral_votes']}/{r['total']}, "
              f"VP {r['vice_president']}{'; ' + r['check'] if r.get('check') else ''}")


# ------------------------------------------------------------------------------------------------------------
# State tables (D1)
STATES_OUT = os.path.join(cc.DATA, "president", "inputs", "nara_electoral_votes.json")
NAMES = {v: k for k, v in cc.STATE_NAMES.items() if k in cc.STATES_50 or k == "DC"}


def _cells(row):
    return [re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", c)).replace("\xa0", " ")).strip()
            for c in re.findall(r"<t[dh](?:\s[^>]*)?>(.*?)</t[dh]>", row, flags=re.S)]


def _num(x):
    x = re.sub(r"[^0-9]", "", x)
    return int(x) if x else 0


def parse_states(year, page):
    page = re.sub(r"<!--.*?-->", "", page, flags=re.S)     # 2012 keeps old cells in comments
    tables = re.findall(r"<table.*?</table>", page, flags=re.S)
    summary = [_cells(r) for r in re.findall(r"<tr[^>]*>(.*?)</tr>", tables[0], flags=re.S)]
    notes = " ".join(c[1] for c in summary if c and c[0].startswith("Notes") and len(c) > 1)
    total_line = next(c for c in summary if c and c[0].rstrip("*") == "Electoral Vote")
    tm = re.search(r"Total/Majority:\s*(\d+)\s*/\s*(\d+)", " ".join(total_line))
    total_ev, majority = int(tm.group(1)), int(tm.group(2))
    main = max(tables[1:], key=lambda t: t.count("<tr"))
    rows = [_cells(r) for r in re.findall(r"<tr[^>]*>(.*?)</tr>", main, flags=re.S)]
    # the second header row names the presidential candidates first, then the vice-presidential ones
    orig = [re.sub(r"\s*\(\d+\)$", "", h) for h in rows[1]]   # footnote marks: "Dukakis, of Massachusetts (1)"
    head = [f"{h} ({orig[:i + 1].count(h)})" if orig.count(h) > 1 else h   # 2016 heads four columns "Other"
            for i, h in enumerate(orig)]
    n_pres = len(head) // 2 if len(rows[2]) == 2 + len(head) else None
    states, totals = {}, None
    for r in rows[2:]:
        if not r:
            continue
        if r[0].startswith("Total"):
            totals = [_num(x) for x in r[1:]]
            continue
        if r[0].startswith(("Notes", "*")) or r[0] == "":     # 1944: a footnote row under the table
            continue
        name = re.sub(r"[\s\d*]+$", "", r[0])          # footnote marks: "Texas ***", "Indiana 1" (2024)
        if name not in NAMES:
            raise ValueError(f"{year}: unknown row {r[0]!r}")
        pres = [_num(x) for x in r[2:2 + n_pres]] if n_pres else []
        states[NAMES[name]] = {"ev": _num(r[1]), "pres": dict(zip(head[:n_pres], pres))}
    assert sum(s["ev"] for s in states.values()) == total_ev, (year, sum(s["ev"] for s in states.values()))
    if totals is not None and n_pres:
        assert totals[0] == total_ev, (year, totals)
        for j, cand in enumerate(head[:n_pres]):
            assert sum(st["pres"][cand] for st in states.values()) == totals[1 + j], (year, cand)
    if year >= 1964:
        assert len(states) == 51, (year, len(states))
    return {"total_ev": total_ev, "majority": majority, "candidates": head[:n_pres] if n_pres else [],
            "notes": notes, "states": states}


def main_states(first, last):
    doc = cc.read_json(STATES_OUT) or {}
    doc.setdefault("years", {})
    doc.setdefault("sources", {})
    doc["about"] = ("National Archives electoral-vote tables, normalised by pipeline/intake/nara_electoral_college.py "
                    "(states). ev is the state's electoral votes; pres is how its electors voted for President.")
    for y in range(first, last + 1, 4):
        rec = cc.fetch(URL.format(y=y), f"nara/electoral_college_{y}.html", min_bytes=5000)
        with open(os.path.join(cc.CACHE, rec["path"]), encoding="utf-8", errors="replace") as f:
            res = parse_states(y, f.read())
        doc["years"][str(y)] = res
        doc["sources"][str(y)] = dict(cc.source_block(
            f"National Archives, Electoral College results, {y}", rec["url"], rec["read_utc"],
            "CC0 1.0 (NARA's own works)", "stated"), sha256=rec["sha256"])
        print(f"{y}: {len(res['states'])} jurisdictions, {res['total_ev']} electoral votes, majority "
              f"{res['majority']}; " + ", ".join(f"{c} {sum(s['pres'].get(c, 0) for s in res['states'].values())}"
                                                for c in res["candidates"]))
    doc["years"] = dict(sorted(doc["years"].items()))
    doc["sources"] = dict(sorted(doc["sources"].items()))
    cc.write_json(STATES_OUT, doc)
    print(f"wrote {os.path.relpath(STATES_OUT, cc.REPO)}")


if __name__ == "__main__":
    if sys.argv[1:2] == ["states"]:
        a = [int(x) for x in sys.argv[2:4]]
        main_states(*(a if len(a) == 2 else (1900, 2024)))
    else:
        a = [int(x) for x in sys.argv[1:3]]
        main(*(a if len(a) == 2 else (1976, 2024)))
