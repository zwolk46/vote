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

Run:  python3 pipeline/intake/medsl_dataverse.py senate [president]
Writes CACHE/medsl/<key>/... and CACHE/medsl/normalized/senate.json (contests by year).
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
    frec = cc.fetch(f"{API}/access/datafile/{df['id']}?format=original", f"medsl/{key}/{stem}.original")
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


if __name__ == "__main__":
    for key in (sys.argv[1:] or ["senate"]):
        {"senate": senate, "president": president}[key]()
