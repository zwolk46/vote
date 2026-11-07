"""pipeline/local_nj.py: New Jersey's official 2024 results (pipeline/intake/nj_sos.py) against the certified federal
counts, and MEDSL's 2024 New Jersey file against them, county by county.

Written 2026-11-07 by worker D3 (briefs/D3-data-local.md, step 2) at the orchestrator's orders of 08:08 ("For the 2024
legislatures of IN, LA and NJ, read each state's own certified results where a file is reachable by script, with a
gate against D2's federal counts on the same dates as for North Carolina") and 10:35 ("NJ 2024 as ordered ... its 2024
file holds local contests and any legislative specials; read what is there").

What is there [measured: the Division of Elections' 2024 page, links outside its HTML comments]: official general
results for president, US Senate and US House, each as a list by county; the special election of NJ-10 (federal); the
party primaries' federal offices and delegates. New Jersey elects its legislature in odd years, and the page lists no
legislative special. Its county, municipal and school board results are not on it: the county clerks hold them.

Why the county comparison: MEDSL's 2024 New Jersey file is 14.4% over D1's certified presidential count, so its New
Jersey contests are held back (data/local/REPORT.md section 6). The state's lists give each county's certified count,
so they show which counties' MEDSL counts add up, office by office. They cannot gate a local contest: they hold no local
office, and a county's federal counts adding up does not show that its other offices' rows do.

  gate()    the state's lists' Democratic and Republican votes against D1's president, D2's Senate and D2's House
            districts: (worst relative miss, words).
  check()   the gate, and MEDSL's Democratic and Republican candidates by county (president, Senate, each House
            district's part of the county) against the state's: data/local/check-nj.json. Candidates are matched by
            surname, since MEDSL leaves the party empty in some counties' rows. The line is local_medsl.QUALITY_LINE.

Run:  VOTE_CACHE=/tmp/vote-cache python3 -I pipeline/local_nj.py check
"""
import argparse
import collections
import csv
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fetch as F  # noqa: E402
from intake import nj_sos as SOS  # noqa: E402
import local as L  # noqa: E402
import local_medsl as LM  # noqa: E402

YEAR = 2024
MEDSL_FILE = os.path.join("medsl", "raw", "2024-13731174-2024-nj-precinct-general.csv")
OFFICES = {"President": ("president", "US PRESIDENT"), "US Senate": ("senate", "US SENATE"),
           "House of Representatives": ("house", "US HOUSE")}
SUFFIX = {"JR", "SR", "II", "III", "IV"}


def load():
    path = os.path.join(SOS.NORM, f"{YEAR}-general.json")
    if not os.path.exists(path):
        raise SystemExit(f"{path} is missing: run pipeline/intake/nj_sos.py read --year {YEAR}")
    with open(path) as f:
        return json.load(f)


def _side(x):
    s = " ".join(x.get("slogans") or [x.get("party", "")]).upper()
    return "D" if s.startswith("DEMOCRATIC") else "R" if s.startswith("REPUBLICAN") else None


def _cert_side(party):
    p = (party or "").upper()
    return "D" if p.startswith("DEMOCRAT") else "R" if p.startswith("REPUBLICAN") else None


def _surname(name):
    w = [x for x in re.sub(r"[^A-Z ]", " ", name.upper()).split() if x not in SUFFIX]
    return w[-1] if w else ""


def gate(st=None):
    st = st or load()
    worst, what = 0.0, []
    for office, (level, _) in OFFICES.items():
        mine = [c for c in st["contests"] if c["office"] == office]
        with open(os.path.join(L.REPO, "data", level, f"{YEAR}.json")) as f:
            cert = [x for x in json.load(f)["contests"] if x["place"]["state"] == "NJ" and not x.get("special")]
        if level == "house":
            byd = {int(x["place"]["district"]): x for x in cert}
            pairs = [(c, byd[c["district"]]) for c in mine if c["district"] in byd]
        else:
            pairs = [(mine[0], cert[0])] if mine and cert else []
        for side in ("D", "R"):
            a = b = 0
            for c, k in pairs:
                aa = sum(x["total"] or 0 for x in c["candidates"] if _side(x) == side)
                bb = sum(x["votes"] for x in k["result"]["candidates"] if _cert_side(x.get("party")) == side)
                if bb:
                    worst = max(worst, abs(aa - bb) / bb)
                a, b = a + aa, b + bb
            what.append(f"{level} {side} {a:,} against {b:,}" + (f" ({len(pairs)} districts)" if level == "house" else ""))
    return worst, "; ".join(what)


def medsl_by_county():
    """{(office, district or None, county, surname): votes} from MEDSL's file, every mode added up."""
    out = collections.Counter()
    path = os.path.join(F.CACHE, MEDSL_FILE)
    want = {v[1]: k for k, v in OFFICES.items()}
    with open(path, newline="", encoding="utf-8", errors="replace") as f:
        for r in csv.DictReader(f):
            if r["office"] in want:
                d = int(r["district"]) if want[r["office"]] == "House of Representatives" else None
                out[(want[r["office"]], d, r["county_name"], _surname(r["candidate"]))] += int(float(r["votes"] or 0))
    return out


def check():
    st = load()
    worst, words = gate(st)
    med = medsl_by_county()
    by_county = collections.defaultdict(dict)
    for c in st["contests"]:
        for x in c["candidates"]:
            side = _side(x)
            if side is None:
                continue
            for county, v in x["counties"].items():
                m = med.get((c["office"], c["district"], county, _surname(x["name"])), 0)
                k = OFFICES[c["office"]][0] + (f" {c['district']}" if c["district"] else "")
                by_county[county][f"{k} {side}"] = {"medsl": m, "state": v, "off": round((m - v) / v, 4) if v else None}
    out = {}
    for county in SOS.COUNTIES:
        t = by_county[county]
        worst_of = {lv: max((abs(r["off"]) for k, r in t.items() if k.startswith(lv) and r["off"] is not None),
                            default=None) for lv in ("president", "senate", "house")}
        out[county] = {"worst_off": worst_of,
                       "adds_up": {lv: (w is not None and w <= LM.QUALITY_LINE) for lv, w in worst_of.items()},
                       "lines": dict(sorted(t.items()))}
    every = [c for c, r in out.items() if all(r["adds_up"].values())]
    split = [c for c, r in out.items() if len(set(r["adds_up"].values())) > 1]
    res = {"about": "New Jersey's official 2024 general-election lists (pipeline/intake/nj_sos.py) against D1's and "
                    "D2's certified counts, and MEDSL's 2024 New Jersey file against the lists by county. Built by "
                    "pipeline/local_nj.py check.",
           "state_page": st["page"],
           "state_files": {k: {x: v[x] for x in ("url", "read_utc", "sha256", "link_text", "contests", "candidates",
                                                 "all_add_up")} for k, v in st["files"].items()},
           "what_the_state_page_holds": "official general results for president, US Senate and US House by county; "
                                        "NJ-10's special election; the primaries' federal offices and delegates. No "
                                        "legislative contest and no county, municipal or school board contest.",
           "gate": {"worst_miss": round(worst, 6), "fails": worst > LM.QUALITY_LINE, "counts": words},
           "medsl_by_county": {"line": LM.QUALITY_LINE,
                               "counties_adding_up_in_every_federal_office": every,
                               "counties_adding_up_in_some_federal_offices_only": split,
                               "counties": out}}
    path = os.path.join(L.REPO, "data", "local", "check-nj.json")
    with open(path, "w") as f:
        json.dump(res, f, indent=1)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("what", choices=["check"])
    ap.parse_args()
    res = check()
    print(json.dumps({k: res[k] for k in ("gate",)}, indent=1))
    m = res["medsl_by_county"]
    print("every office:", m["counties_adding_up_in_every_federal_office"])
    print("some only:", m["counties_adding_up_in_some_federal_offices_only"])
    for c, r in m["counties"].items():
        print(f"{c:12s}", {k: (None if v is None else round(v, 4)) for k, v in r["worst_off"].items()})


if __name__ == "__main__":
    main()
