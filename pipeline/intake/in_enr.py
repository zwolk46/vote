"""pipeline/intake/in_enr.py: Indiana's certified results of the 2024 general election, from the state's results
site's archive.

Written 2026-11-07 by worker D3 (briefs/D3-data-local.md) at the orchestrator's order of 08:08: "For the 2024
legislatures of IN, LA and NJ, read each state's own certified results where a file is reachable by script, with a
gate against D2's federal counts on the same dates as for North Carolina." MEDSL's 2024 Indiana file does not add up
to D1's certified presidential count, so its Indiana contests are held back (data/local/REPORT.md section 6); the
state's own file can take their place if it passes the gate. Plan section 3a: data comes in by script; raw files stay
in a cache outside the repository; the script checks what it reads.

Source: Indiana's election results site, https://enr.indianavoters.in.gov/, whose archive keeps each election's
page and data: https://enr.indianavoters.in.gov/archive/2024General/. Its page says "Results for the November 2024
General Election are final, subject to pending local recounts/special elections", and its data/settings.json says
"Certified": "T" [stated]. The page's footer: "Copyright 1989 - <year>. Quest Information Systems, Inc. All Rights
Reserved." (the site's maker); no licence for the data is printed.

The site's own scripts (Scripts/EnrAngular/...) fetch, and so this reads:
  data/settings.json                          the election, its date, "Certified", and VersionType (the files' suffix)
  data/statewideElectionsC_<v>.json            the office categories, under the headings Federal, State, Local
  data/OffCatC_<id>_<v>.json                   one category's races: StatewideSummary.Race[] (title, seats,
                                               candidates with party, total and isWinner) and its regions' races
                                               by county (Jurisdiction.FIPS)
  data/statewideElectionsR_<v>.json            the counties with questions
  data/JurR_<FIPS>_<v>.json                    one county's questions: type, title, text, yes and no
A question on more than one county's ballot is one question, joined by its type, title and text.

What it does:
  fetch   downloads those files once through pipeline/fetch.py (4 s between requests; a refusal stops it).
  read    writes $VOTE_CACHE/in_enr/normalized/<election>.jsonl (one contest per line) and checks-<election>.json.

Run:  VOTE_CACHE=/tmp/vote-cache python3 pipeline/intake/in_enr.py fetch|read [--election 2024General]
"""
import argparse
import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import fetch as F  # noqa: E402

SITE = "https://enr.indianavoters.in.gov/"
BASE = SITE + "archive/{election}/data/"
ROOT = os.path.join(F.CACHE, "in_enr")
NORM = os.path.join(ROOT, "normalized")
for _d in ("raw", "normalized"):   # fetch.py makes the cache itself, not folders inside it
    os.makedirs(os.path.join(ROOT, _d), exist_ok=True)
DATES = {"2024General": "2024-11-05"}
LICENCE = ("no licence printed; the page's footer reads 'Copyright 1989 - <year>. Quest Information Systems, Inc. "
           "All Rights Reserved.' (the site's maker); the counts are the state's certified results")


def _name(election, file):
    return f"in_enr/raw/{election}/{file}"


def _get(election, file):
    os.makedirs(os.path.join(ROOT, "raw", election), exist_ok=True)
    path = F.fetch(BASE.format(election=election) + file, _name(election, file))
    with open(path, encoding="utf-8-sig") as f:
        d = json.load(f)
    return d.get("Root", d) if isinstance(d, dict) else d


def _list(x):
    """The site's JSON gives one item as an object and several as a list."""
    if x is None:
        return []
    return x if isinstance(x, list) else [x]


def fetch_all(election):
    settings = _get(election, "settings.json")
    v = settings["VersionType"]
    offices = _get(election, f"statewideElectionsC_{v}.json")
    for head in _list(offices["List"]):
        for item in _list((head.get("Items") or {}).get("Item")):
            _get(election, f"OffCatC_{item['OFFICECATEGORYID']}_{v}.json")
    refs = _get(election, f"statewideElectionsR_{v}.json")
    for reg in _list((refs.get("Regions") or {}).get("Region")):
        _get(election, f"JurR_{reg['FIPS']}_{v}.json")
    return settings


def read(election):
    settings = _get(election, "settings.json")
    v = settings["VersionType"]
    offices = _get(election, f"statewideElectionsC_{v}.json")
    refs = _get(election, f"statewideElectionsR_{v}.json")
    # county names to FIPS codes: the questions' index lists every county with both
    fips_of = {r["JURISDICTION_NAME"]: r["FIPS"] for r in _list((refs.get("Regions") or {}).get("Region"))}
    out, t = [], collections.Counter()
    files = {}
    for head in _list(offices["List"]):
        for item in _list((head.get("Items") or {}).get("Item")):
            fn = f"OffCatC_{item['OFFICECATEGORYID']}_{v}.json"
            d = _get(election, fn)
            files[fn] = F.meta(_name(election, fn))
            counties, places = collections.defaultdict(set), collections.defaultdict(set)
            for reg in _list(((d.get("OfficeCategory") or {}).get("Regions") or {}).get("Region")):
                # a region is a county ("Locality", with MAP_FIPS) or a district; a race's own jurisdiction is a
                # county (with its FIPS code), or a district or precinct (a school corporation, a town: named only)
                own = (reg.get("MAP_FIPS") or fips_of.get(reg.get("MAP_JURISDICTION_NAME"))) \
                    if reg.get("MAP_JURISDICTION_TYPE") == "Locality" else None
                for r in _list((reg.get("Races") or {}).get("Race")):
                    j = r.get("Jurisdiction") or {}
                    fips = j.get("FIPS") or own
                    if fips:
                        counties[r["OFFICEID"]].add(fips)
                    if j.get("JURISDICTION_TYPE") in ("District", "Precinct") and j.get("JURISDICTION_NAME"):
                        places[r["OFFICEID"]].add(j["JURISDICTION_NAME"].strip())
            for r in _list((d.get("StatewideSummary") or {}).get("Race")):
                cands = [{"name": x["NAME_ON_BALLOT"], "party": x.get("PARTY") or "", "votes": int(x.get("TOTAL") or 0),
                          "won": x.get("isWinner") == "T"}
                         for x in _list((r.get("Candidates") or {}).get("Candidate"))]
                out.append({"date": DATES[election], "kind": "office", "heading": head["Heading"],
                            "category_id": item["OFFICECATEGORYID"], "category": item["OFFICE_CATEGORY_NAME"],
                            "office_id": r["OFFICEID"], "title": r["OFFICE_TITLE"],
                            "seats": int(r.get("NumofSeats") or 0) or None,
                            "counties": sorted(counties.get(r["OFFICEID"], ())),
                            "places": sorted(places.get(r["OFFICEID"], ())), "candidates": cands, "file": fn})
                t[f"{head['Heading']}: {item['OFFICE_CATEGORY_NAME']}"] += 1
    qs = {}
    for reg in _list((refs.get("Regions") or {}).get("Region")):
        fn = f"JurR_{reg['FIPS']}_{v}.json"
        d = _get(election, fn)
        files[fn] = F.meta(_name(election, fn))
        for rr in _list((((d.get("Region") or {}).get("Reporting_Regions")) or {}).get("Regions")):
            for q in _list((rr.get("Referendums") or {}).get("Referendum")):
                key = (q.get("REFERENDUM_TYPE_NAME"), q.get("REFERENDUM_TITLE"), q.get("REFERENDUM_TEXT"))
                if key not in qs:
                    qs[key] = {"date": DATES[election], "kind": "question", "type": key[0], "title": key[1],
                               "text": key[2], "yes": 0, "no": 0, "counties": [], "files": []}
                c = qs[key]
                c["yes"] += int(q.get("POSITIVE_RESULTS") or 0)
                c["no"] += int(q.get("NEGATIVE_RESULTS") or 0)
                c["counties"].append(reg["FIPS"])
                c["files"].append(fn)
    for c in qs.values():
        c["counties"] = sorted(set(c["counties"]))
        t[f"question: {c['type']}"] += 1
        out.append(c)
    with open(os.path.join(NORM, f"{election}.jsonl"), "w") as f:
        for c in out:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    sm = F.meta(_name(election, "settings.json"))
    checks = {"election": election, "date": DATES[election], "certified": settings.get("Certified"),
              "settings": {k: settings.get(k) for k in ("CurrentElection", "ElectionType", "Certified", "VersionCode",
                                                        "VersionType", "WriteTime")},
              "source": {"url": SITE + f"archive/{election}/", "read_utc": sm["read_utc"], "sha256": sm["sha256"]},
              "contests": dict(sorted(t.items())), "files": len(files) + 3,
              "bytes": sum(m["bytes"] for m in files.values())}
    with open(os.path.join(NORM, f"checks-{election}.json"), "w") as f:
        json.dump(checks, f, indent=1)
    return out, checks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("what", choices=["fetch", "read"])
    ap.add_argument("--election", default="2024General")
    a = ap.parse_args()
    if a.what == "fetch":
        s = fetch_all(a.election)
        print(json.dumps({k: s.get(k) for k in ("CurrentElection", "Certified", "VersionCode", "VersionType")}))
    else:
        out, checks = read(a.election)
        print(json.dumps(checks, indent=1))


if __name__ == "__main__":
    main()
