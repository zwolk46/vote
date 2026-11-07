"""pipeline/intake/bls_earnings.py: average hourly earnings, national and by state, for the cost of an hour.

Source of the series: U.S. Bureau of Labor Statistics (BLS), Current Employment Statistics.
  CES0500000003   average hourly earnings of all employees, total private, national, seasonally adjusted
                  (the series the model's $38.00 comes from, research/frameworks-benefit-cost-v2.md 4.3);
  CES0500000008   the same for production and nonsupervisory employees (a lower-wage reading);
  SMU<ss>000000500000003   the State and Metro Area series of the same measure for the state with FIPS code <ss>,
                  statewide, total private, not seasonally adjusted. Titles, units and seasonal adjustment
                  are as FRED's series pages print them (cached beside the values).

How it is read (the orchestrator's ruling of 2026-11-07 07:21, thread "Orchestrate the vote site"):
  1. FRED, Federal Reserve Bank of St. Louis, reads all 53 series: https://fred.stlouisfed.org/graph/fredgraph.csv?id=<series>
     (the download link on each series page), with the series page for the title. FRED names BLS as the
     source of every one of these series (page: "Source: U.S. Bureau of Labor Statistics"). The record marks
     them second-hand: via "FRED, Federal Reserve Bank of St. Louis", origin the BLS series id. Reason: BLS's own
     data service (api.bls.gov, version 1) allows 25 requests a day per address, and this network's address
     had used them up by the second request of the session ("daily threshold ... has been reached"); BLS's
     flat files (download.bls.gov) and help pages answer "Access Denied" to curl and were not tried another way
     (briefs/_COMMON.md 6). A free version 2 key needs an email address, and the maker's is never used.
  2. The check against BLS itself: every BLS API response cached in $VOTE_CACHE/cost/bls/ (written by an earlier
     step of this script or by `--bls`) is compared with FRED month by month, and each difference is recorded.
     `--bls` asks the BLS API for the next batch of series, once, and stops at the first refusal; run it after
     the daily limit has reset. The orchestrator asked for at least five states checked against BLS directly.

Licence. FRED prints that some series are copyrighted and says to read the series notes; BLS data are a U.S.
Government work, for which BLS prints no copyright restriction [stated by BLS; the page was not re-read here].
The FRED notes for these series name only BLS as the source and print no other restriction on the page read
[measured, 2026-11-07].

Run:  python3 pipeline/intake/bls_earnings.py [--bls]       writes data/cost/wages.json
Rules kept: one request every 4 seconds to one host, curl's own user agent, no contact detail, a stop at the first
refusal (briefs/_COMMON.md 13 and 15), through pipeline/fetch.py.
"""
import csv
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import congress_common as cc  # noqa: E402

BLS_API = "https://api.bls.gov/publicAPI/v1/timeseries/data/"
FRED_CSV = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={}"
FRED_PAGE = "https://fred.stlouisfed.org/series/{}"
STATES = {  # state FIPS code -> postal abbreviation (50 states and DC)
    "01": "AL", "02": "AK", "04": "AZ", "05": "AR", "06": "CA", "08": "CO", "09": "CT", "10": "DE", "11": "DC",
    "12": "FL", "13": "GA", "15": "HI", "16": "ID", "17": "IL", "18": "IN", "19": "IA", "20": "KS", "21": "KY",
    "22": "LA", "23": "ME", "24": "MD", "25": "MA", "26": "MI", "27": "MN", "28": "MS", "29": "MO", "30": "MT",
    "31": "NE", "32": "NV", "33": "NH", "34": "NJ", "35": "NM", "36": "NY", "37": "NC", "38": "ND", "39": "OH",
    "40": "OK", "41": "OR", "42": "PA", "44": "RI", "45": "SC", "46": "SD", "47": "TN", "48": "TX", "49": "UT",
    "50": "VT", "51": "VA", "53": "WA", "54": "WV", "55": "WI", "56": "WY"}
NATIONAL = ["CES0500000003", "CES0500000008"]
FRED_ID = {"CES0500000008": "AHETPI"}   # FRED files BLS's CES0500000008 under its own id (not read at BLS; see the series page)


def fid(sid):
    return FRED_ID.get(sid, sid)

ELECTION_YEARS = list(range(2008, 2026, 2))
BLS_WINDOWS = [(2007, 2016), (2017, 2026)]


def state_series(fips):
    return f"SMU{fips}000000500000003"


ALL_SERIES = NATIONAL + [state_series(f) for f in STATES]


# ------------------------------------------------------------------ FRED

def fred_values(sid):
    sid_bls, sid = sid, fid(sid)
    rec = cc.fetch(FRED_CSV.format(sid), f"cost/fred/{sid}.csv", min_bytes=200)
    vals = {}
    with open(os.path.join(cc.CACHE, rec["path"]), newline="", encoding="utf-8") as f:
        r = csv.reader(f)
        hdr = next(r)
        if hdr[1] != sid:
            raise cc.Refused(f"FRED returned {hdr} for {sid}")
        for d, v in r:
            if v not in ("", "."):
                y, m = int(d[:4]), int(d[5:7])
                vals[(y, m)] = v
    return vals, rec


def fred_page(sid):
    sid_bls, sid = sid, fid(sid)
    rec = cc.fetch(FRED_PAGE.format(sid), f"cost/fred/series_{sid}.html", min_bytes=1000)
    h = open(os.path.join(cc.CACHE, rec["path"]), encoding="utf-8", errors="replace").read()
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", h, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t).replace("&nbsp;", " ").replace("&nbsp", " ")
    t = re.sub(r"\s+", " ", t)
    title = re.search(r"(Average Hourly Earnings of [^|(]+?) \(" + re.escape(sid) + r"\)", t)
    bls_code = re.search(r"The source code is: (\S+)", t)
    src = re.search(r"Notes Source: (U\.S\. Bureau of Labor Statistics)", t)
    units = re.search(r"Units: (Dollars per Hour ?,? ?(?:Not )?Seasonally Adjusted)", t)
    return {"title": title.group(1).strip() if title else None,
            "source_named": src.group(1) if src else None,
            "units": units.group(1).replace(" ,", ",") if units else None,
            "fred_id": sid, "bls_source_code_on_page": bls_code.group(1) if bls_code else None,
            "page_sha256": rec["sha256"], "page_read_utc": rec["read_utc"]}


# ------------------------------------------------------------------ BLS (the check)

def bls_post(series, start, end, tag):
    body = json.dumps({"seriesid": series, "startyear": str(start), "endyear": str(end)})
    name = f"cost/bls/{tag}_{start}_{end}.json"
    full = os.path.join(cc.CACHE, name)
    meta_p = full + ".meta.json"
    os.makedirs(os.path.dirname(full), exist_ok=True)
    if not (os.path.exists(full) and os.path.exists(meta_p)):
        time.sleep(4.0)
        out = subprocess.run(["curl", "-sS", "--max-time", "120", "-X", "POST", "-H", "Content-type: application/json",
                              "-d", body, "-o", full + ".part", "-w", "%{http_code}", BLS_API], capture_output=True, text=True)
        head = open(full + ".part", encoding="utf-8", errors="replace").read(600) if os.path.exists(full + ".part") else ""
        if out.returncode != 0 or int(out.stdout.strip() or 0) >= 400 or '"status":"REQUEST_SUCCEEDED"' not in head[:200]:
            if os.path.exists(full + ".part"):
                os.remove(full + ".part")
            # a refusal (the daily limit of 25 requests, a bad request) is never cached: it would stand for the answer
            raise cc.Refused("BLS API refused: " + head.replace("\n", " ")[:300])
        os.replace(full + ".part", full)
        json.dump({"url": BLS_API, "request": json.loads(body), "read_utc": cc.now_utc(), "bytes": os.path.getsize(full),
                   "sha256": hashlib.sha256(open(full, "rb").read()).hexdigest()}, open(meta_p, "w"), indent=1)
    return json.load(open(full)), json.load(open(meta_p))


def bls_cached():
    """Every successful BLS API response in the cache: {series: {(y, m): (value, preliminary)}} and the request records."""
    vals, recs = {}, []
    d = os.path.join(cc.CACHE, "cost", "bls")
    if not os.path.isdir(d):
        return vals, recs
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".json") or fn.endswith(".meta.json"):
            continue
        data = json.load(open(os.path.join(d, fn)))
        meta = json.load(open(os.path.join(d, fn + ".meta.json")))
        if data.get("status") != "REQUEST_SUCCEEDED":
            continue
        recs.append({"file": fn, "series": len(data["Results"]["series"]), "read_utc": meta["read_utc"], "sha256": meta["sha256"]})
        for s in data["Results"]["series"]:
            for row in s["data"]:
                if row["period"].startswith("M") and row["period"] != "M13":
                    prelim = any(fn_.get("code", "").upper() == "P" for fn_ in row.get("footnotes") or [])
                    vals.setdefault(s["seriesID"], {})[(int(row["year"]), int(row["period"][1:]))] = (row["value"], prelim)
    return vals, recs


def bls_fetch_next():
    """Ask BLS for the first batch/window not cached yet; one request; a refusal stops and is returned as text."""
    for (a, b) in BLS_WINDOWS:
        for k in range(0, len(ALL_SERIES), 25):
            tag = f"b{k // 25}"
            if os.path.exists(os.path.join(cc.CACHE, "cost", "bls", f"{tag}_{a}_{b}.json")):
                continue
            try:
                bls_post(ALL_SERIES[k:k + 25], a, b, tag)
                return f"fetched {tag} {a}-{b}"
            except cc.Refused as e:
                return str(e)
    return "every batch already cached"


# ------------------------------------------------------------------ build

def main(argv):
    note_bls = bls_fetch_next() if "--bls" in argv else None
    fred, fred_recs, pages = {}, {}, {}
    for sid in ALL_SERIES:
        fred[sid], fred_recs[sid] = fred_values(sid)
        pages[sid] = fred_page(sid)
    bls, bls_recs = bls_cached()

    # the check: FRED against BLS, month by month, wherever BLS was read
    cmp_by_series, diffs = {}, []
    for sid, d in bls.items():
        n = 0
        for key, (v, _) in d.items():
            if key in fred[sid]:
                n += 1
                if abs(float(v) - float(fred[sid][key])) > 1e-9:
                    diffs.append({"series": sid, "year": key[0], "month": key[1], "bls": v, "fred": fred[sid][key]})
            else:
                diffs.append({"series": sid, "year": key[0], "month": key[1], "bls": v, "fred": None})
        cmp_by_series[sid] = n
    prelim = {sid: {k: p for k, (v, p) in d.items()} for sid, d in bls.items()}

    def one(sid, abbr=None):
        d = fred[sid]
        last = max(d)
        by_year = {}
        for y in ELECTION_YEARS:
            months = {m: float(d[(y, m)]) for (yy, m) in d if yy == y}
            if not months:
                continue
            by_year[str(y)] = {"november": months.get(11), "mean_of_months": round(sum(months.values()) / len(months), 4),
                               "months": len(months), "first_month": min(months), "last_month": max(months)}
        out = {"series": sid, "fred_id": fid(sid), "bls_source_code_on_page": pages[sid]["bls_source_code_on_page"], "title": pages[sid]["title"], "units": pages[sid]["units"], "source_named_by_fred": pages[sid]["source_named"],
               "first_observation": {"year": min(d)[0], "month": min(d)[1]},
               "latest": {"year": last[0], "month": last[1], "value": float(d[last]),
                          "preliminary": (prelim.get(sid) or {}).get(last)},
               "by_election_year": by_year,
               "checked_against_bls_months": cmp_by_series.get(sid, 0),
               "fred_csv": {"read_utc": fred_recs[sid]["read_utc"], "sha256": fred_recs[sid]["sha256"]},
               "fred_page": {"read_utc": pages[sid]["page_read_utc"], "sha256": pages[sid]["page_sha256"]}}
        return out

    read_utc = max(r["read_utc"] for r in fred_recs.values())
    out = {
        "about": "Average hourly earnings in dollars, for the value of an hour in the cost of voting (model section 6). National default: CES0500000003, all employees, total private, seasonally adjusted. Values are read from FRED (second-hand; origin BLS) and checked month by month against the BLS API where BLS was read (check).",
        "source": {"name": "FRED, Federal Reserve Bank of St. Louis: BLS Current Employment Statistics and State and Metro Area series (fredgraph.csv per series)",
                   "url": "https://fred.stlouisfed.org/", "read_utc": read_utc,
                   "licence": "FRED prints that some series are copyrighted and refers to the series notes; the notes of these series name only the U.S. Bureau of Labor Statistics as source and print no other restriction [measured]; BLS data are a U.S. Government work",
                   "mark": "stated", "via": "FRED, Federal Reserve Bank of St. Louis",
                   "origin": {"name": "U.S. Bureau of Labor Statistics, Current Employment Statistics (national) and State and Metro Area Employment, Hours, and Earnings (state)", "url": "https://www.bls.gov/ces/"},
                   "note": "Second-hand by the orchestrator's ruling of 2026-11-07 07:21: the BLS API's daily limit (25 requests per address) was reached; BLS's help pages and flat files answered Access Denied and were not tried another way."},
        "check_against_bls": {
            "method": "month-by-month comparison of every BLS API response held in the cache with FRED's value for the same series and month",
            "bls_requests_read": bls_recs, "series_checked": len(cmp_by_series),
            "months_compared": sum(cmp_by_series.values()), "differences": diffs,
            "series_checked_list": sorted(cmp_by_series),
            "bls_request_this_run": note_bls,
            "open": "BLS API batches not yet read (daily limit reached on 2026-11-07); run `python3 pipeline/intake/bls_earnings.py --bls` after the limit resets to read the next batch, and again until all four are cached."},
        "national": {sid: one(sid) for sid in NATIONAL},
        "states": {abbr: one(state_series(f), abbr) for f, abbr in STATES.items()},
        "unread": [{"what": "BLS documentation of the State and Metro Area series format (www.bls.gov/help/hlpforma.htm) and the series catalog (download.bls.gov/pub/time.series/)",
                    "reason": "HTTP 403 Access Denied to curl (2026-11-07); not tried another way (briefs/_COMMON.md 6)"}],
    }
    dest = os.path.join(cc.DATA, "cost")
    os.makedirs(dest, exist_ok=True)
    with open(os.path.join(dest, "wages.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
        f.write("\n")
    nat = out["national"]["CES0500000003"]["latest"]
    print(f"FRED series read: {len(fred)}; national latest {nat}; BLS months compared {sum(cmp_by_series.values())} "
          f"over {len(cmp_by_series)} series, differences {len(diffs)}; BLS request: {note_bls}")


if __name__ == "__main__":
    main(sys.argv[1:])
