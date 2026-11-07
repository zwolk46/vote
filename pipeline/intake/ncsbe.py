"""pipeline/intake/ncsbe.py: North Carolina State Board of Elections, precinct results for every election date.

Written 2026-11-07 by worker D3 (briefs/D3-data-local.md, step 2; the orchestrator, 07:25: "OpenElections and NC
SBE first: by script, the most contests for the fewest tokens"). Plan section 3a: data comes in by script; raw files
stay in a cache outside the repository; the script checks what it reads.

Source: the State Board's public download site, https://dl.ncsbe.gov/ (an Amazon S3 bucket, `dl.ncsbe.gov`), folder
ENRS/, one folder per election date (ENRS/<YYYY_MM_DD>/). Its ReadMe_PUBLIC_DATA.txt: the files "are considered public
information per NC General Statutes" (G.S. 132-1). Each date with machine-readable results has results_pct_<date>.zip
(or .txt): every contest on that date's ballots, by county, precinct and choice, in one of the layouts
ENRS/layout_results_pct.txt describes (it changed in 2007, 2008, 2010, 2014 and 2018). Dates before that are PDFs.

What it does:
  list    reads the bucket's listing (S3 ListObjectsV2, one folder at a time) and records, per election date, its
          results file or that it has none; writes $VOTE_CACHE/ncsbe/inventory.json.
  fetch   downloads every results file once through pipeline/fetch.py (4 s between requests; a refusal stops it).
  read    reads every fetched file into contests (one per contest per date): $VOTE_CACHE/ncsbe/normalized/<date>.jsonl,
          and checks-<date>.json (rows read, rows kept, contests, votes; the layout used).
Which rows form one contest: from 2014 the file's own `contest group id` links a contest's lines across counties; before
2014, the contest's name (and its district, where the file has one) within its county, and across counties only for a
contest the file marks as statewide or a district's.

Run:  VOTE_CACHE=/tmp/vote-cache python3 pipeline/intake/ncsbe.py list|fetch|read [--dates 2024_11_05,...]
"""
import argparse
import collections
import csv
import io
import json
import os
import re
import sys
import time
import urllib.parse
import xml.etree.ElementTree as ET
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import fetch as F  # noqa: E402

BUCKET = "https://s3.amazonaws.com/dl.ncsbe.gov"
SITE = "https://dl.ncsbe.gov"
ROOT = os.path.join(F.CACHE, "ncsbe")
NORM = os.path.join(ROOT, "normalized")
LICENCE = ("public records of the North Carolina State Board of Elections (N.C. Gen. Stat. 132-1, as the site's "
           "ReadMe_PUBLIC_DATA.txt says); no licence printed")
_NS = "{http://s3.amazonaws.com/doc/2006-03-01/}"
for _d in ("listing", "raw", "normalized"):   # fetch.py makes the cache itself, not folders inside it
    os.makedirs(os.path.join(ROOT, _d), exist_ok=True)
_DATE = re.compile(r"^ENRS/(\d{4})_(\d{2})_(\d{2})/$")
csv.field_size_limit(1 << 24)


def _list(prefix):
    """One S3 ListObjectsV2 page set for a prefix, by folder (delimiter /): (keys with sizes, sub-prefixes)."""
    keys, subs, token = [], [], None
    while True:
        q = {"list-type": "2", "prefix": prefix, "delimiter": "/"}
        if token:
            q["continuation-token"] = token
        name = os.path.join("ncsbe", "listing", (prefix.strip("/").replace("/", "_") or "root")
                            + (f"-{len(keys)}" if token else "") + ".xml")
        path = F.fetch(f"{BUCKET}?{urllib.parse.urlencode(q)}", name, refresh=True)
        root = ET.parse(path).getroot()
        for c in root.findall(_NS + "Contents"):
            keys.append((c.find(_NS + "Key").text, int(c.find(_NS + "Size").text)))
        for p in root.findall(_NS + "CommonPrefixes"):
            subs.append(p.find(_NS + "Prefix").text)
        if root.findtext(_NS + "IsTruncated") != "true":
            return keys, subs
        token = root.findtext(_NS + "NextContinuationToken")


def inventory():
    _, subs = _list("ENRS/")
    out = {"read_utc": F._now_utc(), "listing": f"{BUCKET}?list-type=2&prefix=ENRS/&delimiter=/", "dates": {}}
    for sub in sorted(subs):
        m = _DATE.match(sub)
        if not m:
            continue
        keys, _ = _list(sub)
        names = {k.rsplit("/", 1)[1]: z for k, z in keys if not k.endswith("/")}
        res = sorted(n for n in names if re.match(r"^results_pct_\d{8}\.(zip|txt|csv)$", n))
        d = "_".join(m.groups())
        out["dates"][d] = {"results": res, "bytes": [names[n] for n in res],
                           "other_kinds": sorted({re.sub(r"[_\d]+(\.\w+)$", r"\1", n) for n in names} - set(res))}
    os.makedirs(ROOT, exist_ok=True)
    with open(os.path.join(ROOT, "inventory.json"), "w") as f:
        json.dump(out, f, indent=1)
    have = sum(1 for v in out["dates"].values() if v["results"])
    print(f"{len(out['dates'])} election dates listed; {have} with a precinct results file")
    return out


def load_inventory():
    with open(os.path.join(ROOT, "inventory.json")) as f:
        return json.load(f)


def fetch_all(dates=None):
    inv = load_inventory()
    for d, v in sorted(inv["dates"].items()):
        if dates and d not in dates:
            continue
        for n in v["results"]:
            url = f"{SITE}/ENRS/{d}/{n}"
            F.fetch(url, os.path.join("ncsbe", "raw", n), storage_sites=("amazonaws.com",))
            print("fetched", n)


# -- reading ------------------------------------------------------------------------------------------------------
HEADLESS = {   # layout_results_pct.txt, "before January 1, 2007" and "between January 1, 2007 and January 1, 2008"
    9: ["county", "election_dt", "precinct_abbrv", "precinct", "contest_name", "name_on_ballot", "party_cd",
        "ballot_count", "ftp_date"],
    10: ["county", "election_dt", "precinct", "contest", "name_on_ballot", "party_cd", "election_day_count",
         "absentee_count", "provisional_count", "total_vote_count"],
}


def _rows(path):
    """Every data row of a results file as a dict keyed by its own header, lower-cased with spaces as _."""
    if path.endswith(".zip"):
        with zipfile.ZipFile(path) as z:
            names = [n for n in z.namelist() if not n.endswith("/")]
            if len(names) != 1:
                raise ValueError(f"{path}: expected one file in the zip, found {names}")
            raw = z.read(names[0])
    else:
        with open(path, "rb") as f:
            raw = f.read()
    text = raw.decode("utf-8-sig", errors="replace") if raw[:3] == b"\xef\xbb\xbf" else raw.decode("latin-1")
    if sum(1 for ln in text.splitlines() if ln.strip()) < 2:   # an empty file: the date's results were not posted
        return
    first = text.split("\n", 1)[0]
    delim = "\t" if first.count("\t") > first.count(",") else ","
    rd = csv.reader(io.StringIO(text), delimiter=delim)
    row1 = next(rd)
    if row1 and row1[0].strip().lower().startswith("county"):
        head = [re.sub(r"[^a-z0-9]+", "_", h.strip().lower()).strip("_") for h in row1]
        pending = []
    else:   # some files have no header line: the layout is told by the number of columns (layout_results_pct.txt)
        x = [v.strip() for v in row1]
        head = (HEADLESS[9] if len(x) >= 9 and re.match(r"^(\d{4}-\d\d-\d\d|\d\d/\d\d/\d{4})", x[8]) else
                HEADLESS[10] if len(x) >= 10 and all(re.match(r"^\d+$", v) for v in x[6:10]) else None)
        if head is None:
            raise ValueError(f"{path}: no header and {len(row1)} columns, which no layout in layout_results_pct.txt has")
        pending = [row1]
    for row in pending + [r for r in rd]:
        if not row or all(not x.strip() for x in row):
            continue
        yield dict(zip(head, (x.strip() for x in row))), head


def _int(x):
    x = (x or "").replace(",", "").strip()
    return int(float(x)) if x and re.match(r"^-?\d+(\.\d+)?$", x) else None


def read_date(d, path):
    """The contests of one election date."""
    contests = {}
    n_rows = kept = 0
    head = None
    bad = collections.Counter()
    for r, head in _rows(path):
        n_rows += 1
        county = (r.get("county") or r.get("county_name") or "").upper()
        name = r.get("contest_name") or r.get("contest") or ""
        choice = r.get("choice") or r.get("name_on_ballot") or ""
        votes = _int(r.get("total_votes") or r.get("total_vote_count") or r.get("ballot_count"))
        if not name or not choice:
            bad["no contest or choice"] += 1
            continue
        if votes is None:
            bad["no vote count"] += 1
            continue
        ctype = r.get("contest_type") or ""
        group = r.get("contest_group_id") or ""
        district = r.get("district") or ""
        district = "" if district.upper() in ("NOT FOUND", "") else district
        name = re.sub(r"\s+", " ", name).strip()
        # one contest: from 2014 and before 2010 the contest's name, across counties (the names carry their place:
        # "CITY OF ARCHDALE MAYOR", "ALAMANCE COUNTY BOARD OF COMMISSIONERS"); 2010-2013 names a county's own contests
        # without the county ("BOARD OF COMMISSIONERS", type C), so those are one per county
        key = (county, name, district) if ("contest_type" in r and "contest_group_id" not in r and ctype != "S") \
            else ("", name, district)
        c = contests.get(key)
        if c is None:
            c = contests[key] = {"date": d, "contest": name, "contest_type": ctype, "group": group or None,
                                 "district": district or None, "vote_for": _int(r.get("vote_for")),
                                 "counties": set(), "precincts": set(), "choices": {}}
        c["counties"].add(county)
        c["precincts"].add((county, r.get("precinct") or r.get("precinct_abbrv") or ""))
        party = (r.get("choice_party") or r.get("party") or r.get("party_cd") or "").strip()
        choice = re.sub(r"\s+", " ", choice).strip()
        ch = c["choices"].setdefault(choice, {"votes": 0, "party": collections.Counter(), "flags": collections.Counter()})
        ch["votes"] += votes
        if party:
            ch["party"][party] += votes or 1
        for fl in ("winner_status", "runoff_status", "recount_status"):   # 2010-2013 only
            if r.get(fl) not in (None, "", "0"):
                ch["flags"][f"{fl}={r[fl]}"] += 1
        kept += 1
    out = []
    for c in contests.values():
        c["counties"] = sorted(c["counties"])
        c["n_precincts"] = len(c.pop("precincts"))
        c["choices"] = [{"name": k, "votes": v["votes"],
                         "party": v["party"].most_common(1)[0][0] if v["party"] else None,
                         "flags": dict(v["flags"]) or None}
                        for k, v in sorted(c["choices"].items(), key=lambda kv: -kv[1]["votes"])]
        out.append(c)
    check = {"date": d, "file": os.path.basename(path), "header": head, "rows": n_rows, "rows_kept": kept,
             "rows_left_out": dict(bad), "contests": len(out),
             "votes": sum(ch["votes"] for c in out for ch in c["choices"])}
    return out, check


def read_all(dates=None):
    inv = load_inventory()
    os.makedirs(NORM, exist_ok=True)
    for d, v in sorted(inv["dates"].items()):
        if dates and d not in dates:
            continue
        for n in v["results"]:
            path = os.path.join(F.CACHE, "ncsbe", "raw", n)
            if not os.path.exists(path):
                print("not fetched:", n)
                continue
            out, check = read_date(d, path)
            check["source"] = F.meta(os.path.join("ncsbe", "raw", n))
            with open(os.path.join(NORM, f"{d}.jsonl"), "w") as f:
                for c in out:
                    f.write(json.dumps(c, separators=(",", ":")) + "\n")
            with open(os.path.join(NORM, f"checks-{d}.json"), "w") as f:
                json.dump(check, f, indent=1)
            print(d, check["rows"], "rows,", check["contests"], "contests,", check["rows_left_out"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["list", "fetch", "read"])
    ap.add_argument("--dates", default="")
    a = ap.parse_args()
    dates = set(filter(None, a.dates.split(",")))
    {"list": lambda: inventory(), "fetch": lambda: fetch_all(dates), "read": lambda: read_all(dates)}[a.step]()


if __name__ == "__main__":
    main()
