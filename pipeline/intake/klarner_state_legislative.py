"""pipeline/intake/klarner_state_legislative.py: Carl Klarner's State Legislative Election Returns, 1967-2022.

Written 2026-11-07 by worker D3 (briefs/D3-data-local.md, step 2), in the shape plan/PLAN.md section 3a gives
every intake script: download to a cache outside the repository, check, convert.

Source. Carl Klarner, "State Legislative Election Returns, 1967-2022", Harvard Dataverse,
doi:10.7910/DVN/FJOGJB, version 1.0, released 2024-06-12, licence CC0 1.0 (the record's licence field; no
terms of use). Klarner compiles official returns: "from state Web sites" as posted when collected, and from the
earlier ICPSR editions (research/historical-close-races-v2.md section 5). The record does not name the origin
of each figure, so every figure from here carries via = this dataset and is marked "stated"
(law, Part A, "a true source": a compilation that names where its figures come from; here it names them by kind,
not race by race, which the source block says).

Files read (Dataverse file ids, original format):
  10273085  127_slers_1967to2022_forsharing20230810   one row per candidate, party line and (2013-2016) county,
                                                      every election type: generals, specials, primaries,
                                                      runoffs, Louisiana's two rounds (418,894 rows)
  10273086  202slers_uoa_contest20230810              one row per general-type contest, with Klarner's own
                                                      contest variables: two-party share, incumbency, the
                                                      same seat's previous result (the "lag" variables)
  10273084  208slers_uoa_cand_contest20230810         one row per candidate per general-type contest
  10273089  203slers_uoa_cham_year20230810            seats up per chamber and year
  and the four codebooks (.docx).

What it writes (to $VOTE_CACHE/klarner/normalized/, never to the repository):
  contests.jsonl   one contest per line: the key, the date, the election type, the district, every candidate with
                   votes summed over party lines and counties, and for general-type contests Klarner's contest
                   variables; pipeline/local.py builds data/ from it.
  checks.json      the checks below, with every difference listed.

Checks (plan 3a: row counts, and totals against the totals the source itself prints):
  1. rows read = 418,894, the count the dataset record and research/historical-close-races-v2.md give;
  2. for every general-type contest, the candidates' votes summed from file 127 against Klarner's own dvote,
     rvote and ovote in file 202, party by party;
  3. for every candidate in a general-type contest, votes from file 127 against file 208;
  4. seats elected per chamber and year (the sum of the seats of contests whose winner takes office at the
     session's start, "deter" = 1) against file 203's seatsup.

Run:  VOTE_CACHE=/tmp/vote-cache python3 pipeline/intake/klarner_state_legislative.py
"""
import collections
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import fetch as F  # noqa: E402  (pipeline/fetch.py, D1's: the one fetch every intake script uses)

csv.field_size_limit(1 << 26)

API = "https://dataverse.harvard.edu/api"
DOI = "doi:10.7910/DVN/FJOGJB"
FILES = {
    "candidate": (10273085, "127_slers_1967to2022_forsharing20230810.csv"),
    "contest": (10273086, "202slers_uoa_contest20230810.csv"),
    "cand_contest": (10273084, "208slers_uoa_cand_contest20230810.csv"),
    "cham_year": (10273089, "203slers_uoa_cham_year20230810.csv"),
}
CODEBOOKS = {
    "codebook_candidate": (10273083, "codebook_candidate.docx"),
    "codebook_contest": (10273082, "codebook_contest.docx"),
    "codebook_candcontest": (10273088, "codebook_candcontest.docx"),
    "codebook_chamyear": (10273087, "codebook_chamyear.docx"),
}
EXPECTED_ROWS = 418894
OUT = os.path.join(F.CACHE, "klarner", "normalized")

# The contest a row belongs to (the codebook's unit "a contest": year month day etype sid sen dname dno geopost
# mmdpost; regime added because a special election on the old map can share a day with a general on the new one).
CONTEST_KEY = ("year", "month", "day", "etype", "sid", "sen", "dname", "dno", "geopost", "mmdpost", "regime")
# File 202 has no month and day; its contests are general-type, one per post and year.
CONTEST_202_KEY = ("year", "etype", "sid", "sen", "dname", "dno", "geopost", "mmdpost", "regime")
# Klarner's contest variables carried into the normalized record for general-type contests (codebook of file 202).
CONTEST_VARS = ("dtype", "dseats", "eseats", "deter", "dvote", "rvote", "ovote", "dcand", "rcand", "ocand",
                "dwin", "rwin", "owin", "dinc", "rinc", "oinc", "inc", "dper", "dontuse", "vmiss", "bigthird",
                "mixeduncont", "partuncont", "uncont", "redist", "propup", "termzmax",
                "dperlag", "dwinlag", "dvotelag", "rvotelag", "ovotelag", "inclag", "uncontlag",
                "partuncontlag", "mixeduncontlag", "bigthirdlag", "dontuselag", "yearminlag", "yearmaxlag")


def record_and_files():
    """Fetch the dataset record and every file (once; the cache keeps them). Returns the version line and
    the meta records."""
    rec_path = F.fetch(f"{API}/datasets/:persistentId/?persistentId={DOI}", "klarner/record.json")
    with open(rec_path) as f:
        v = json.load(f)["data"]["latestVersion"]
    lic = v.get("license")
    lic = lic.get("name") if isinstance(lic, dict) else lic
    version = f"v{v['versionNumber']}.{v['versionMinorNumber']}, released {v.get('releaseTime')}"
    names = {f["dataFile"]["id"]: f["dataFile"]["filename"] for f in v["files"]}
    metas = {}
    for key, (fid, name) in list(FILES.items()) + list(CODEBOOKS.items()):
        fmt = "?format=original" if name.endswith(".csv") else ""
        F.fetch(f"{API}/access/datafile/{fid}{fmt}", f"klarner/{name}", storage_sites=("amazonaws.com",))
        metas[key] = F.meta(f"klarner/{name}")
        metas[key]["dataverse_filename"] = names.get(fid)
    return {"version": version, "licence": lic, "doi": DOI, "files": metas}


def _num(x):
    x = (x or "").strip()
    if x == "" or x == ".":
        return None
    try:
        v = float(x)
    except ValueError:
        return None
    return int(v) if v == int(v) else v


def _rows(name):
    with open(os.path.join(F.CACHE, "klarner", name), encoding="utf-8", newline="") as f:
        yield from csv.DictReader(f)


def normalize():
    info = record_and_files()
    contests = collections.OrderedDict()
    nrows = 0
    for r in _rows(FILES["candidate"][1]):
        nrows += 1
        key = tuple(r[k] for k in CONTEST_KEY)
        c = contests.get(key)
        if c is None:
            c = contests[key] = {
                "key": dict(zip(CONTEST_KEY, key)), "state": r["sab"], "sen": int(r["sen"]),
                "dname": r["dname"], "dno": r["dno"], "geopost": r["geopost"], "mmdpost": r["mmdpost"],
                "etype": r["etype"], "year": int(r["year"]), "month": _num(r["month"]), "day": _num(r["day"]),
                "dtype": _num(r["dtype"]), "dseats": _num(r["dseats"]), "eseats": _num(r["eseats"]),
                "deter": _num(r["deter"]), "uncert": set(), "cands": collections.OrderedDict(), "rows": 0}
        c["rows"] += 1
        for u in r["uncert"].split():
            c["uncert"].add(u)
        scat = r["last"].strip().lower() == "scattering" or r["cand"].strip().lower() == "scattering"
        ck = "scattering" if scat else (r["candid"] or r["cand"])
        a = c["cands"].get(ck)
        if a is None:
            a = c["cands"][ck] = {"name": "scattering" if scat else r["cand"], "candid": _num(r["candid"]),
                                  "party": r["partyt"] or None, "lines": [], "votes": 0, "vote_missing": False,
                                  "outcome": r["outcome"] or None, "exper": r["exper"] or None,
                                  "scattering": scat}
        v = _num(r["vote"])
        if v is None:
            a["vote_missing"] = True
        else:
            a["votes"] += v
        line = r["party"] or r["partyz"]
        if line and line not in a["lines"]:
            a["lines"].append(line)
        if a["outcome"] != r["outcome"] and r["outcome"]:
            a.setdefault("outcomes_seen", sorted({a["outcome"] or "", r["outcome"]}))
    # Klarner's contest file: general-type contests
    c202 = {}
    for r in _rows(FILES["contest"][1]):
        c202[tuple(r[k] for k in CONTEST_202_KEY)] = {k: _num(r.get(k)) for k in CONTEST_VARS}
    by202 = collections.defaultdict(list)
    for key, c in contests.items():
        k2 = (key[0],) + key[3:]           # drop month and day
        by202[k2].append(key)
    checks = {"rows_read": nrows, "rows_expected": EXPECTED_ROWS, "rows_ok": nrows == EXPECTED_ROWS,
              "contest_vs_202": [], "cand_vs_208": [], "seats_vs_203": [], "unmatched_202": []}
    for k2, vars_ in c202.items():
        keys = by202.get(k2)
        if not keys:
            checks["unmatched_202"].append(dict(zip(CONTEST_202_KEY, k2)))
            continue
        for key in keys:
            contests[key]["klarner"] = vars_
    # check 2: the Democratic and Republican sums against file 202's dvote and rvote. Its ovote is compared
    # too but only counted: it is 0 in thousands of contests where file 127 lists non-major candidates with
    # votes (1968 California among them), so it is not a total of those candidates' votes [measured].
    nchk2 = 0
    o_diff = 0
    for key, c in contests.items():
        kv = c.get("klarner")
        if not kv or kv.get("vmiss") == 1:
            continue
        sums = {"d": 0, "r": 0, "o": 0}
        for a in c["cands"].values():
            p = a["party"]
            if a["scattering"] or p == "w":
                continue
            side = "d" if p == "d" else "r" if p == "r" else "o"
            sums[side] += a["votes"]
        nchk2 += 1
        if kv.get("ovote") is not None and sums["o"] != kv["ovote"]:
            o_diff += 1
        diff = {s: (sums[s], kv.get(s + "vote")) for s in ("d", "r")
                if kv.get(s + "vote") is not None and sums[s] != kv.get(s + "vote")}
        if diff:
            checks["contest_vs_202"].append({"contest": c["key"], "differences": diff})
    checks["contest_vs_202_checked"] = nchk2
    checks["ovote_differs_from_127"] = o_diff
    # check 3: candidate votes against file 208
    nchk3 = 0
    idx = {}
    for key, c in contests.items():
        k2 = (key[0],) + key[3:]
        for a in c["cands"].values():
            if a["candid"] is not None:
                idx[k2 + (str(a["candid"]),)] = (a["votes"], a["vote_missing"])
    for r in _rows(FILES["cand_contest"][1]):
        k = tuple(r[k] for k in CONTEST_202_KEY) + (str(_num(r["candid"])),)
        got = idx.get(k)
        want = _num(r["vote"])
        nchk3 += 1
        if got is None:
            checks["cand_vs_208"].append({"key": k, "issue": "candidate not found in file 127's contests"})
        elif want is not None and not got[1] and got[0] != want:
            checks["cand_vs_208"].append({"key": k, "file127": got[0], "file208": want})
    checks["cand_vs_208_checked"] = nchk3
    # check 4: seats elected per chamber-year against file 203
    seats = collections.Counter()
    for c in contests.values():
        if c["deter"] == 1 and c["eseats"] and not c["etype"].startswith(("dp", "rp", "ttp")):
            winners = sum(1 for a in c["cands"].values() if a["outcome"] == "w")
            seats[(c["state"], c["sen"], c["year"])] += winners
    st_ab = {}
    for c in contests.values():
        st_ab[c["key"]["sid"]] = c["state"]
    n4 = 0
    for r in _rows(FILES["cham_year"][1]):
        k = (st_ab.get(r["sid"], r["state"]), int(r["sen"]), int(r["year"]))
        want = _num(r["seatsup"])
        got = seats.get(k, 0)
        n4 += 1
        if want is not None and got != want:
            checks["seats_vs_203"].append({"state": k[0], "sen": k[1], "year": k[2], "winners_in_127": got,
                                           "seatsup_203": want})
    checks["seats_vs_203_checked"] = n4
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "contests.jsonl"), "w") as f:
        for c in contests.values():
            c = dict(c)
            c["uncert"] = sorted(c["uncert"])
            c["cands"] = list(c["cands"].values())
            f.write(json.dumps(c, ensure_ascii=False, separators=(",", ":")) + "\n")
    with open(os.path.join(OUT, "info.json"), "w") as f:
        json.dump(info, f, indent=1)
    summary = {k: (len(v) if isinstance(v, list) else v) for k, v in checks.items()}
    with open(os.path.join(OUT, "checks.json"), "w") as f:
        json.dump({"summary": summary, **checks}, f, indent=1, default=list)
    et = collections.Counter(c["etype"] for c in contests.values())
    print(f"Klarner SLERs {info['version']}, licence {info['licence']}: {nrows:,} rows "
          f"({'as expected' if nrows == EXPECTED_ROWS else 'EXPECTED %d' % EXPECTED_ROWS}); "
          f"{len(contests):,} contests; general-type joined to file 202: "
          f"{sum(1 for c in contests.values() if 'klarner' in c):,}")
    print("checks:", json.dumps(summary))
    print("election types:", et.most_common(12))
    return info, contests, checks


if __name__ == "__main__":
    normalize()
