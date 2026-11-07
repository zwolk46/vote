"""pipeline/intake/id_sos.py: Idaho's official results of the 2022 general election, its statewide offices and questions.

Written 2026-11-07 by worker D3 on the orchestrator's rulings of 18:54 ("(a) Idaho 2022: yes, all six statewide offices
from the state's marked page, with the canvass as the check") and 19:04 ("Power County is missing, so statewide offices
come from the state's page"). Reason (the orchestrator): "n enters p directly, so a doubled count halves a figure we
show"; MEDSL's 2022 Idaho file counts each county twice (a "COUNTY TOTAL" precinct beside its precincts) and lacks
Power County (16077) in most offices [measured, data/local/REPORT.md section 29]. Plan section 3a: data comes in by
script; raw files stay in a cache outside the repository.

Sources, read 2026-11-07 between 18:49 and 18:51 UTC and kept in $VOTE_CACHE/id_sos/raw (each with a .meta.json):
  election-results.html   the Secretary of State's results page (https://sos.idaho.gov/elections-division/idaho-
                          election-results/, served from https://voteidaho.gov/election-results/). Under "General
                          Election - November 8, 2022" it links "Statewide Results" to the results site below and
                          "Canvass Files" to the canvass [stated: the page].
  statewide-124-1.html    the results site's statewide page (https://www.livevoterturnout.com/ENR/idaho/124/1/en/
                          Index_124.html), headed "OFFICIAL ELECTION RESULTS", "Fully Reporting 44", "Total Counties
                          44" [stated: the page]. A vendor's host counts where a state page that answers names it and
                          the vendor marks the count official (the orchestrator's ruling of 12:40): this one does both.
                          Each contest: "Contest: <title>", then per candidate "<name> (<PTY>)", "<name>, <PARTY>[,
                          Winner]", the votes and the share. It lists no write-in line.
  2022_General_Canvass.zip the canvass (https://archive.sos.idaho.gov/elections/data/results/2022/
                          2022_General_Canvass.zip): "22 General Statewide - County.xlsx", each sheet headed "Issued by
                          Lawerence Denney, Secretary of State", with a row for each county and a TOTAL row. The check.
The state prints no licence; these are its public election returns.

What it does (read): checks that the state page links both files for the 2022 general, that the results page carries
its official heading with all 44 counties reporting, and that every statewide contest's total on the page equals the
canvass's TOTAL row to the vote, candidate by candidate (the gate); writes $VOTE_CACHE/id_sos/normalized/2022-general.json
with each statewide contest: its candidates (the page's votes and winner marks), the canvass's write-in lines the page
does not list, and the canvass's Power County column. No request is made.

Run:  VOTE_CACHE=/tmp/vote-cache python3 pipeline/intake/id_sos.py read
"""
import argparse
import html
import io
import json
import os
import re
import sys
import unicodedata
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import fetch as F  # noqa: E402

ROOT = os.path.join(F.CACHE, "id_sos")
RAW = os.path.join(ROOT, "raw")
NORM = os.path.join(ROOT, "normalized")
STATE_PAGE = "election-results.html"
RESULTS = "statewide-124-1.html"
RESULTS_URL = "https://www.livevoterturnout.com/ENR/idaho/124/1/en/Index_124.html"
CANVASS = "2022_General_Canvass.zip"
CANVASS_URL = "https://archive.sos.idaho.gov/elections/data/results/2022/2022_General_Canvass.zip"
WORKBOOK = "22 General Statewide - County.xlsx"
GENERAL = "General Election - November 8, 2022"
# the statewide contests: the results page's title, MEDSL's office, and the canvass's sheet and its columns for it
CONTESTS = [
    ("Lieutenant Governor", "LIEUTENANT GOVERNOR", "Lt Gov & SoS", (0, 3)),
    ("Secretary of State", "SECRETARY OF STATE", "Lt Gov & SoS", (3, 6)),
    ("State Controller", "STATE CONTROLLER", "SC & ST", (0, 3)),
    ("State Treasurer", "STATE TREASURER", "SC & ST", (3, 5)),
    ("Attorney General", "ATTORNEY GENERAL", "AG & SOPI", (0, 2)),
    ("Superintendent of Public Instruction", "SUPERINTENDENT OF PUBLIC INSTRUCTION", "AG & SOPI", (2, 4)),
]
LICENCE = "no licence printed; the Idaho Secretary of State's public election returns"


def _need(name):
    p = os.path.join(RAW, name)
    if not (os.path.exists(p) and os.path.exists(p + ".meta.json")):
        raise SystemExit(f"{p} (and its .meta.json) is not in the cache")
    with open(p + ".meta.json") as f:
        return p, json.load(f)


def _tokens(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        s = f.read()
    s = re.sub(r"<script.*?</script>|<style.*?</style>", "", s, flags=re.S | re.I)
    return [html.unescape(t).strip() for t in re.split(r"<[^>]+>", s) if t.strip()]


def _key(name):
    """A name to compare across the page and the canvass: (surname, first initial), accents, a write-in mark and a
    parenthesis dropped ("Raúl R. Labrador" on the page, "Raul Labrador" in the canvass)."""
    n = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().upper()
    toks = [re.sub(r"[^A-Z]", "", t) for t in re.sub(r"\(W/I\)|\([^)]*\)", " ", n).split()]
    toks = [t for t in toks if t]
    return (toks[-1], toks[0][:1]) if toks else ("", "")


def page_contests(toks):
    """{title: [{name, party, votes, winner}]} from the results page's tokens."""
    out = {}
    for i, t in enumerate(toks):
        if not t.startswith("Contest: "):
            continue
        title = t[len("Contest: "):]
        j = toks.index("Percentage", i) + 1
        cands = []
        while j + 3 < len(toks) and re.fullmatch(r".+ \([A-Z]+\)", toks[j]) and re.fullmatch(r"[\d,]+", toks[j + 2]):
            long = toks[j + 1]
            party = long.split(", ")[1] if ", " in long else None
            cands.append({"name": re.sub(r" \([A-Z]+\)$", "", toks[j]), "party": party,
                          "votes": int(toks[j + 2].replace(",", "")), "winner": long.endswith(", Winner")})
            j += 4
        out[title] = cands
    return out


def canvass(path):
    """{sheet: {"names": [...], "rows": {county or TOTAL: [votes...]}}} from the canvass workbook."""
    import openpyxl
    with zipfile.ZipFile(path) as z:
        member = next(m for m in z.namelist() if m.endswith(WORKBOOK))
        wb = openpyxl.load_workbook(io.BytesIO(z.read(member)), read_only=True, data_only=True)
    out = {}
    for ws in wb.worksheets:
        rows = list(ws.iter_rows(values_only=True))
        head = [str(c) for c in rows[0] if c is not None]
        hdr = next(i for i, r in enumerate(rows) if r and r[0] in ("County", "Precinct"))
        names = [c for c in rows[hdr][1:] if c]
        body = {}
        for r in rows[hdr + 1:]:
            if r and r[0] and isinstance(r[1], (int, float)):
                body[str(r[0]).strip().upper()] = [int(v or 0) for v in r[1:1 + len(names)]]
        out[ws.title] = {"names": names, "rows": body, "issued": head}
    return out


def read():
    page, page_meta = _need(STATE_PAGE)
    res, res_meta = _need(RESULTS)
    can, can_meta = _need(CANVASS)
    toks = _tokens(page)
    with open(page, encoding="utf-8", errors="replace") as f:
        s = f.read()
    i = s.find(GENERAL)
    if i < 0:
        raise SystemExit(f"id_sos: the state page has no heading {GENERAL!r}")
    nxt = re.search(r"(General|Primary) Election - [A-Z][a-z]+ \d+, \d{4}", s[i + len(GENERAL):])
    seg = s[i:i + len(GENERAL) + (nxt.start() if nxt else len(s))]   # this election's block, to the next heading
    pairs = {(html.unescape(re.sub(r"<[^>]+>", " ", t)).strip(), h)
             for h, t in re.findall(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', seg, re.S)}
    if ("Statewide Results", RESULTS_URL) not in pairs or ("Canvass Files", CANVASS_URL) not in pairs:
        raise SystemExit("id_sos: the state page's 2022 general does not link the results page and the canvass")
    rt = _tokens(res)
    k = rt.index("OFFICIAL ELECTION RESULTS")
    if rt[k:k + 11] != ["OFFICIAL ELECTION RESULTS", "Counties Reporting", "100%", "Not Reporting", "0",
                        "Partially Reporting", "0", "Fully Reporting", "44", "Total Counties", "44"]:
        raise SystemExit(f"id_sos: the results page's heading reads {rt[k:k + 11]}")
    pc = page_contests(rt)
    cv = canvass(can)
    contests = []
    for title, office, sheet, (a, b) in CONTESTS:
        sh = cv[sheet]
        if not any("Issued by" in h and "Secretary of State" in h for h in sh["issued"]):
            raise SystemExit(f"id_sos: the canvass sheet {sheet!r} is not headed as issued by the Secretary of State")
        names = sh["names"][a:b]
        total = dict(zip(names, sh["rows"]["TOTAL"][a:b]))
        power = dict(zip(names, sh["rows"]["POWER"][a:b]))
        cands = pc.get(title)
        if not cands:
            raise SystemExit(f"id_sos: no contest {title!r} on the results page")
        by = {_key(n): n for n in names}
        gate = []
        for c in cands:
            n = by.get(_key(c["name"]))
            if n is None:
                raise SystemExit(f"id_sos: {title}: {c['name']} is not in the canvass")
            c["canvass_total"] = total[n]
            c["canvass_power"] = power[n]
            gate.append(c["votes"] == total[n])
        listed = {_key(c["name"]) for c in cands}
        writeins = [{"name": n, "votes": total[n], "canvass_power": power[n], "writein": True}
                    for n in names if _key(n) not in listed]
        if any("(W/I)" not in w["name"] for w in writeins):
            raise SystemExit(f"id_sos: {title}: the canvass names a candidate the page does not: {writeins}")
        contests.append({"title": title, "office": office, "candidates": cands, "canvass_writeins": writeins,
                         "equal_to_canvass": all(gate), "canvass_sheet": sheet})
    if not all(c["equal_to_canvass"] for c in contests):
        raise SystemExit("id_sos: a statewide total on the results page differs from the canvass: "
                         + "; ".join(c["title"] for c in contests if not c["equal_to_canvass"]))
    out = {"year": 2022, "election": GENERAL,
           "source": {"page": page_meta, "results": res_meta, "canvass": can_meta, "licence": LICENCE,
                      "mark": "the results page's heading 'OFFICIAL ELECTION RESULTS', all 44 counties fully reporting",
                      "check": "each candidate's total equals the canvass's TOTAL row to the vote"},
           "contests": contests}
    os.makedirs(NORM, exist_ok=True)
    with open(os.path.join(NORM, "2022-general.json"), "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    for c in contests:
        print(f"{c['title']}: " + ", ".join(f"{x['name']} {x['votes']:,}" for x in c["candidates"])
              + "".join(f", {w['name']} {w['votes']:,} (canvass)" for w in c["canvass_writeins"])
              + f"; equal to the canvass: {c['equal_to_canvass']}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["read"])
    ap.parse_args()
    read()


if __name__ == "__main__":
    main()
