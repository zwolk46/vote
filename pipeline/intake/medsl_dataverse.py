"""pipeline/intake/medsl_dataverse.py: MIT Election Data and Science Lab datasets on Harvard Dataverse.

Source. MIT Election Data and Science Lab (MEDSL), datasets on Harvard Dataverse, read through Dataverse's
documented native API (https://guides.dataverse.org/en/latest/api/native-api.html and the data access
API). Every MEDSL record read so far carries the licence CC0 1.0 and no terms of use
(research/historical-close-races-v2.md section 5). MEDSL is a compiler: its federal files name the Clerk
of the House's "Statistics of the Congressional Election" as their source, so a figure from here is
marked with `via` = MEDSL and `url` = the Clerk (law, Part A, "a true source": a compilation that names
its origins).

Datasets this script knows (DOI, file):
  senate     doi:10.7910/DVN/PEJ5QU  "U.S. Senate statewide 1976-2024"   1976-2024-senate.tab (or .csv)
  president  doi:10.7910/DVN/42MVDX  "U.S. President 1976-2024"          1976-2024-president.tab
Files behind a Dataverse "guestbook" (a form asking a name and email) are NOT fetched: giving those to an
outside party is the maker's word (law 10). The House file (IG0UN2) is one of them.

Run:  python3 pipeline/intake/medsl_dataverse.py senate [president] [president_detail]
Writes CACHE/medsl/<key>/... and CACHE/medsl/normalized/senate.json (contests by year).
`president_detail` (added by D1 for the presidency, 2026-11-07) writes data/president/inputs/
medsl_president.json, committed: every candidate of every state-year summed over the party lines the
candidate ran on, the two nominees, the leading two, and the rows that are not candidates. It also checks
the file against the MD5 Dataverse publishes for it.
Checks: row counts; every contest's candidate votes are summed and compared with MEDSL's own
`totalvotes` column; contests per year are counted.
"""
import csv
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import congress_common as cc  # noqa: E402

API = "https://dataverse.harvard.edu/api"
DATASETS = {
    "senate": ("doi:10.7910/DVN/PEJ5QU", "1976-2024-senate"),
    "president": ("doi:10.7910/DVN/42MVDX", "1976-2024-president"),
}
LICENCE = "CC0 1.0 (Dataverse licence field)"


def record(key):
    doi, _ = DATASETS[key]
    rec = cc.fetch(f"{API}/datasets/:persistentId/?persistentId={doi}", f"medsl/{key}/record.json",
                   refresh=False)
    with open(os.path.join(cc.CACHE, rec["path"])) as f:
        meta = json.load(f)["data"]
    return rec, meta


def fetch_file(key):
    rec, meta = record(key)
    _, stem = DATASETS[key]
    v = meta["latestVersion"]
    lic = (v.get("license") or {}).get("name") if isinstance(v.get("license"), dict) else v.get("license")
    files = v["files"]
    pick = [f for f in files if f["dataFile"]["filename"].startswith(stem)]
    if not pick:
        raise SystemExit(f"{key}: no file named {stem}* in {[f['dataFile']['filename'] for f in files]}")
    df = pick[0]["dataFile"]
    # Harvard Dataverse serves its files from Amazon S3: a redirect there is the publisher's own storage
    frec = cc.fetch(f"{API}/access/datafile/{df['id']}?format=original", f"medsl/{key}/{stem}.original",
                    storage_sites=("amazonaws.com",))
    version = f"v{v.get('versionNumber')}.{v.get('versionMinorNumber')}, released {v.get('releaseTime')}"
    return {"record": rec, "file": frec, "filename": df["filename"], "file_id": df["id"],
            "version": version, "licence": lic, "doi": DATASETS[key][0]}


def rows(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        head = f.read(4096)
        f.seek(0)
        dialect = "excel-tab" if head.count("\t") > head.count(",") else "excel"
        return list(csv.DictReader(f, dialect=dialect))


def senate():
    info = fetch_file("senate")
    rs = rows(os.path.join(cc.CACHE, info["file"]["path"]))
    contests = {}
    for r in rs:
        if (r.get("stage") or "gen").lower() not in ("gen", "general"):
            continue
        y = int(r["year"])
        st = r["state_po"].strip()
        spec = str(r.get("special", "")).strip().upper() in ("TRUE", "1")
        k = (y, st, spec)
        c = contests.setdefault(k, {"year": y, "state": st, "special": spec, "candidates": {},
                                    "totalvotes": set(), "rows": 0, "mode": set()})
        c["rows"] += 1
        c["mode"].add(r.get("mode", ""))
        tv = cc.to_int(r.get("totalvotes"))
        if tv is not None:
            c["totalvotes"].add(tv)
        name = (r.get("candidate") or "").strip()
        writein = str(r.get("writein", "")).strip().upper() == "TRUE"
        party = (r.get("party_simplified") or r.get("party_detailed") or "").strip()
        votes = cc.to_int(r.get("candidatevotes")) or 0
        a = c["candidates"].setdefault(name or "(blank)", {"name": name, "parties": [], "votes": 0,
                                                            "writein": writein})
        a["votes"] += votes
        if party and party not in a["parties"]:
            a["parties"].append(party)
    out = []
    for k in sorted(contests):
        c = contests[k]
        s = sum(a["votes"] for a in c["candidates"].values())
        tv = sorted(c["totalvotes"])
        checks = []
        if len(tv) == 1 and tv[0] != s:
            checks.append(f"candidate rows sum to {s:,}; MEDSL totalvotes {tv[0]:,}")
        elif len(tv) > 1:
            checks.append(f"MEDSL totalvotes not unique: {tv}")
        out.append({"year": c["year"], "state": c["state"], "special": c["special"],
                    "candidates": sorted(c["candidates"].values(), key=lambda a: -a["votes"]),
                    "totalvotes": tv[0] if len(tv) == 1 else None, "rows": c["rows"],
                    "modes": sorted(c["mode"]), "checks": checks})
    cc.write_json(os.path.join(cc.CACHE, "medsl", "normalized", "senate.json"), {"source": info, "contests": out})
    years = sorted({c["year"] for c in out})
    print(f"MEDSL Senate {info['version']}, licence {info['licence']}: {len(rs):,} rows, {len(out)} general "
          f"contests, {years[0]}-{years[-1]}; {sum(1 for c in out if c['checks'])} with a sum differing from totalvotes")
    return info, out


def president():
    info = fetch_file("president")
    rs = rows(os.path.join(cc.CACHE, info["file"]["path"]))
    by = {}
    for r in rs:
        y, st = int(r["year"]), r["state_po"].strip()
        d = by.setdefault((y, st), {"year": y, "state": st, "D": 0, "R": 0, "total": cc.to_int(r["totalvotes"])})
        ps = (r.get("party_simplified") or "").upper()
        v = cc.to_int(r.get("candidatevotes")) or 0
        if ps == "DEMOCRAT":
            d["D"] += v
        elif ps == "REPUBLICAN":
            d["R"] += v
    out = sorted(by.values(), key=lambda d: (d["year"], d["state"]))
    cc.write_json(os.path.join(cc.CACHE, "medsl", "normalized", "president_state.json"), {"source": info, "rows": out})
    print(f"MEDSL President {info['version']}, licence {info['licence']}: {len(rs):,} rows, {len(out)} state-years")
    return info, out


# ------------------------------------------------------------------------------------------------------------
# The presidency in detail (D1, 2026-11-07; moved here from D1's medsl_president.py so that MEDSL has one
# script, plan section 3a). Reason for the detail: the presidential contests list every candidate, and the
# check against the FEC needs each nominee's votes summed over the lines the nominee ran on.
PRES_OUT = os.path.join(cc.DATA, "president", "inputs", "medsl_president.json")
NOT_CANDIDATES = {"", "SCATTERING", "OTHER", "OTHERS", "BLANK VOTE/SCATTERING", "NONE OF THE ABOVE",
                  "BLANK VOTE", "NONE OF THESE CANDIDATES", "OVER VOTE", "BLANK VOTE/VOID VOTE/SCATTERING",
                  "VOID VOTE", "BLANK VOTES", "OVERVOTES", "UNDERVOTES", "VOID", "WRITE-IN", "SPOILED"}
# state-years where the rows do not sum to totalvotes, measured 2026-11-07 (rows minus totalvotes)
KNOWN_TOTAL_GAPS = {("2024", "DC"): 2535, ("2024", "NY"): -874}
PRES_YEARS = [str(y) for y in range(1976, 2025, 4)]


def _md5(path):
    import hashlib
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def president_detail():
    import collections
    info = fetch_file("president")
    path = os.path.join(cc.CACHE, info["file"]["path"])
    _, meta = record("president")
    df = next(f["dataFile"] for f in meta["latestVersion"]["files"] if f["dataFile"]["id"] == info["file_id"])
    want = (df.get("checksum") or {}).get("value") or df.get("md5")
    got = _md5(path)
    assert want and got == want, f"MD5 {got} is not Dataverse's {want} for datafile {info['file_id']}"
    rs = rows(path)
    by = collections.defaultdict(list)
    for r in rs:
        by[(r["year"], r["state_po"])].append(r)
    years = sorted({y for y, _ in by})
    assert years == PRES_YEARS, years
    for y in years:
        assert len([1 for (yy, _) in by if yy == y]) == 51, y
    out = {}
    for (y, st), group in sorted(by.items()):
        total = int(group[0]["totalvotes"])
        assert all(int(r["totalvotes"]) == total for r in group), (y, st)
        gap = sum(int(r["candidatevotes"]) for r in group) - total
        assert gap == KNOWN_TOTAL_GAPS.get((y, st), 0), (y, st, gap)
        cands = collections.OrderedDict()
        others = collections.Counter()
        for r in group:
            name = r["candidate"].strip()
            v = int(r["candidatevotes"])
            if name.upper() in NOT_CANDIDATES:
                others[name or "(blank name)"] += v
                continue
            c = cands.setdefault(name, {"name": name, "votes": 0, "lines": [], "parties": set(), "writein": True})
            c["votes"] += v
            c["lines"].append({"party_detailed": r["party_detailed"], "votes": v})
            c["parties"].add(r["party_simplified"])
            c["writein"] = c["writein"] and str(r["writein"]).upper() == "TRUE"   # write-in only if every line is
        ranked = sorted(cands.values(), key=lambda c: -c["votes"])
        for c in ranked:
            c["parties"] = sorted(p for p in c["parties"] if p)

        def nominee(party):
            # the party's leading candidate (MEDSL marks every 2020 DC row a write-in, so the flag is not used)
            m = [c for c in ranked if party in c["parties"]]
            return {"name": m[0]["name"], "votes": m[0]["votes"]} if m else None

        out.setdefault(y, {})[st] = {
            "state": group[0]["state"].title(), "totalvotes": total,
            "dem": nominee("DEMOCRAT"), "rep": nominee("REPUBLICAN"),
            "top_two": [{"name": c["name"], "votes": c["votes"], "parties": c["parties"]} for c in ranked[:2]],
            # the party lines are kept only where a candidate ran on more than one (fusion), to keep the file small
            "candidates": [dict({"name": c["name"], "votes": c["votes"], "parties": c["parties"],
                                 "writein": c["writein"]}, **({"lines": c["lines"]} if len(c["lines"]) > 1 else {}))
                           for c in ranked],
            "not_candidates": dict(others), "medsl_version": group[0]["version"]}
    url = f"{API}/access/datafile/{info['file_id']}?format=original"
    doc = {"about": "MEDSL state presidential returns, normalised by pipeline/intake/medsl_dataverse.py "
                    "(president_detail). Votes per candidate are summed over the party lines the candidate ran on.",
           "source": dict(cc.source_block(f"MIT Election Data and Science Lab, U.S. President 1976-2024, Harvard "
                                          f"Dataverse {info['doi']}, {info['version']}, file {info['filename']}",
                                          url, info["file"]["read_utc"], "CC0 1.0", "stated",
                                          via="MEDSL's compilation of state election offices' returns",
                                          note=f"checked against Dataverse's MD5 {want}"),
                          sha256=info["file"]["sha256"]),
           "known_total_gaps": {f"{y} {s}": g for (y, s), g in KNOWN_TOTAL_GAPS.items()},
           "years": out}
    cc.write_json(PRES_OUT, doc)
    for y in years:
        d = sum(out[y][s]["dem"]["votes"] for s in out[y])
        r = sum(out[y][s]["rep"]["votes"] for s in out[y])
        t = sum(out[y][s]["totalvotes"] for s in out[y])
        odd = [s for s in out[y] if {c["name"] for c in out[y][s]["top_two"]}
               != {out[y][s]["dem"]["name"], out[y][s]["rep"]["name"]}]
        print(f"{y}: 51 jurisdictions; Democratic {d:,}, Republican {r:,}, totalvotes {t:,};"
              f" leading two not the two nominees in: {', '.join(odd) or 'none'}")
    print(f"wrote {os.path.relpath(PRES_OUT, cc.REPO)}")
    return doc


if __name__ == "__main__":
    for key in (sys.argv[1:] or ["senate"]):
        {"senate": senate, "president": president, "president_detail": president_detail}[key]()
