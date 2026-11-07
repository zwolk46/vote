"""pipeline/intake/medsl_precinct.py: MIT Election Data and Science Lab precinct returns, every office below Congress.

Written 2026-11-07 by worker D3 (briefs/D3-data-local.md, step 2). Plan section 3a: data comes in by script; raw files
stay in a cache outside the repository; the script checks what it reads.

Sources (Harvard Dataverse, MEDSL, CC0 1.0, no guestbook; data/sources/local.md):
  2024  "Precinct-Level Returns 2024 by Individual State"  doi:10.7910/DVN/NYTPDU   one file per state, every office
  2022  "Precinct-Level Returns 2022 by Individual State"  doi:10.7910/DVN/UYQIEP   one file per state, and local files
The 2018 and 2020 sets sit behind a Dataverse guestbook (a name and an email): the maker's call, not taken (law 10).

What it does, per file:
  1. fetches it once through pipeline/fetch.py (4 s between requests to a host; a refusal stops the script);
  2. reads every row, and keeps the rows of offices below Congress (MEDSL's `dataverse` STATE and LOCAL), and the
     presidency's rows for the check in 4;
  3. adds the votes up to one record per contest and candidate. Modes: where a precinct reports a TOTAL row for a
     candidate, that row alone is used; otherwise its modes are summed (MEDSL's README, "Warnings": modes split
     apart and a TOTAL row can both be present). A count MEDSL redacts ("*") marks the candidate's votes missing.
     Which rows form one contest: MEDSL names the office and the district, but not every office name is unique
     within a state (two towns' "CITY COUNCIL"), so precincts are joined into one contest only where they share a
     named candidate; yes-or-no questions (measures, retentions) are one contest per question statewide when MEDSL
     files them as state questions, and per question and county when local, since a local question's wording does
     not show which place holds it. A county's own sum filed as a precinct ("COUNTY TOTAL", Idaho's 2022 file) is
     dropped where the county's precincts add up to it (drop_county_totals; the orchestrator's ruling of 19:04);
  4. checks: the rows read against the row count Dataverse records for the file, where it records one; and the
     presidency's totals by state and candidate against D1's certified totals in data/president/<year>.json.
Writes $VOTE_CACHE/medsl/normalized/<year>/<ST>-<file id>.jsonl (one contest per line; a state can have two
files, its own and a local one) and checks-<year>.json.

Run:  VOTE_CACHE=/tmp/vote-cache python3 pipeline/intake/medsl_precinct.py 2024 [--states DE,CO]
"""
import argparse
import collections
import csv
import json
import os
import re
import sys
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import fetch as F  # noqa: E402

REPO = os.path.dirname(os.path.dirname(HERE))
API = "https://dataverse.harvard.edu/api"
DATASETS = {
    2024: {"doi": "doi:10.7910/DVN/NYTPDU", "title": "Precinct-Level Returns 2024 by Individual State"},
    2022: {"doi": "doi:10.7910/DVN/UYQIEP", "title": "Precinct-Level Returns 2022 by Individual State"},
    # MEDSL's own GitHub repositories, read by git (the orchestrator, 06:16: no guestbook there). Both now say they
    # are deprecated in favour of the Dataverse sets; 2018's files are still at its head, 2020's were deleted on
    # 2023-10-24 and are read at the commit before (its local returns only).
    2018: {"github": "MEDSL/2018-elections-official", "commit": "42055b11dcd5477bc125cdec5a18fbcc60fb6bed",
           "collection": "2018_precincts",
           "paths": r"^individual_states/2018-[a-z]{2}-precinct-general\.zip$",
           "title": "2018 precinct-level election returns (GitHub, MEDSL/2018-elections-official)"},
    2020: {"github": "MEDSL/2020-elections-official", "commit": "a450bb45da90cda13a8e8ce2556c3a1d90dce324",
           "collection": "2020_precincts",
           "paths": r"^all_states/2020-all-states-local-precinct-general\.zip$",
           "title": "2020 local precinct-level election returns (GitHub, MEDSL/2020-elections-official)"},
}
# 2016: MEDSL's older layout (no party groups, no seat counts, no dataverse column), read for its questions only
# (the orchestrator, 06:16: "Then MEDSL 2016 measures"): the state and the local set, both CC0 1.0, no guestbook.
SETS_2016 = [(3345337, "2016-precinct-state.csv", "STATE", "doi:10.7910/DVN/GSZG1O",
              "State Precinct-Level Returns 2016"),
             (3345356, "2016-precinct-local.csv", "LOCAL", "doi:10.7910/DVN/Q8OHRS",
              "Local Precinct-Level Returns 2016")]
OUT = os.path.join(F.CACHE, "medsl", "normalized")
csv.field_size_limit(1 << 24)

# answers on a yes-or-no question, and the separators states put between a question's subject and its answer
ANSWERS = {"YES", "NO", "FOR", "AGAINST", "APPROVE", "REJECT", "APPROVED", "REJECTED", "ACCEPT", "RETAIN",
           "NOT RETAIN", "DO NOT RETAIN", "BONDS YES", "BONDS NO", "YES ON", "NO ON", "FOR THE MEASURE",
           "AGAINST THE MEASURE", "IN FAVOR", "OPPOSED", "IN FAVOR OF", "YES FOR APPROVAL", "NO FOR REJECTION"}
NOT_CANDIDATES = {"", "OVERVOTES", "UNDERVOTES", "OVER VOTES", "UNDER VOTES", "BLANK", "BLANK VOTES", "SPOILED",
                  "TOTAL VOTES", "BALLOTS CAST", "REGISTERED VOTERS", "OVERVOTE", "UNDERVOTE", "NONE OF THE ABOVE",
                  # seen in the 2024 files as candidates' names: totals, void and blank ballots, empty lines
                  "CONTEST TOTAL", "CAST VOTES", "VOID", "BLANKS", "BLANK BALLOTS", "INVALID VOTES", "INVALID",
                  "NO CANDIDATE FILED", "NO PETITION FILED",
                  # and in 2022's: New York City's ballot-count lines, void ballots, Nevada's "none of these"
                  "PUBLIC COUNTER", "ABSENTEE / MILITARY", "AFFIDAVIT", "FEDERAL", "MANUALLY COUNTED EMERGENCY",
                  "SPECIAL VOTES", "BLANK/VOID", "NONE OF THESE CANDIDATES"}
GENERIC = {"WRITE-IN", "WRITEIN", "WRITE IN", "SCATTERING", "WRITE-INS", "UNCERTIFIED WRITE-IN", "UNQUALIFIED WRITE-IN",
           "ALL OTHERS", "SCATTER", "SCATTERED", "MISC", "OTHERS", "UNRESOLVED", "UNKNOWN", "FICTIONAL"}
SUFFIXES = {"JR", "SR", "II", "III", "IV", "V"}
# the Democratic Party's state parties under their own names (MEDSL's 2024 files simplify them to DEMOCRAT)
DEMOCRATIC_AFFILIATES = {"DEMOCRATIC-FARMER-LABOR", "DEMOCRATIC-NPL", "DEMOCRATIC-NONPARTISAN LEAGUE", "DFL"}
_META = re.compile(r"^(TOTAL\b|VOTE FOR \d|TIMES (BLANK|OVER|UNDER)|.*\b(VOTES CAST|BALLOTS CAST|REGISTERED VOTERS|OVER ?VOTES?|"
                   r"UNDER ?VOTES?|BLANK VOTES?)\b)")


def is_meta(cand):
    """A row that counts no candidate: totals, registration, over- and undervotes (MEDSL keeps some as candidates)."""
    c = cand.strip().upper()
    return c in NOT_CANDIDATES or bool(_META.match(c))


def is_generic(name):
    """Write-in totals and lines that name no one ('*NOT QUALIFIED 1*'): never used to join precincts."""
    n = name.strip().upper()
    return n in GENERIC or n.startswith("*") or "WRITE-IN" in n or "WRITE IN" in n or "WRITEIN" in n


def name_tokens(name):
    """A name's words, letters only, without nicknames in quotes or brackets and without Jr or III."""
    n = re.sub(r'"[^"]*"|\([^)]*\)', " ", name.upper()).replace(".", " ").replace(",", " ")
    toks = [re.sub(r"[^A-Z]", "", t) for t in n.split()]
    return [t for t in toks if t and t not in SUFFIXES]


def same_person(a, b):
    """Two spellings of one candidate's name in one contest: the same words in any order ('LATHROP WILL',
    'WILL LATHROP'), or the same surname with the same or a missing first initial ('G BORRELLO', 'BORRELLO',
    'GEORGE M BORRELLO'). Used only inside one contest, where two candidates rarely share a surname."""
    ta, tb = name_tokens(a), name_tokens(b)
    if not ta or not tb:
        return False
    if len(ta) > 1 and sorted(ta) == sorted(tb):
        return True
    if ta[-1] != tb[-1]:
        return False
    ia = ta[0][0] if len(ta) > 1 else ""
    ib = tb[0][0] if len(tb) > 1 else ""
    return not ia or not ib or ia == ib


def split_answer(cand):
    """('BERKENKOTTER', 'YES') for 'BERKENKOTTER - YES'; ('', 'YES') for 'YES'; None for a person's name."""
    c = cand.strip().upper()
    if c in ANSWERS:
        return "", c
    m = re.match(r"^(.*?)[\s\-:,/]+(YES|NO|FOR|AGAINST|RETAIN|NOT RETAIN|DO NOT RETAIN)$", c)
    if m and m.group(1):
        return m.group(1).strip(" -:,/"), m.group(2)
    return None


# ------------------------------------------------------------------ the dataset's record and files

def _git(*args, cwd=None):
    import subprocess
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=False).stdout


def github_files(year):
    """The files of a GitHub-held year: a blob-less clone of the repository in the cache, the commit fetched, each
    file written to the cache by `git show` at that commit, with a meta file as pipeline/fetch.py writes one."""
    import datetime
    import hashlib
    d = DATASETS[year]
    repo_dir = os.path.join(F.CACHE, "medsl", "git", d["github"].split("/")[1])
    if not os.path.isdir(os.path.join(repo_dir, ".git")):
        os.makedirs(os.path.dirname(repo_dir), exist_ok=True)
        _git("clone", "-q", "--filter=blob:none", "--no-checkout", f"https://github.com/{d['github']}", repo_dir)
    try:
        _git("cat-file", "-e", d["commit"], cwd=repo_dir)
    except Exception:
        _git("fetch", "-q", "--filter=blob:none", "origin", d["commit"], cwd=repo_dir)
    names = [x for x in _git("ls-tree", "-r", "--name-only", d["commit"], cwd=repo_dir).decode().split("\n")
             if re.match(d["paths"], x)]
    out = []
    for path in sorted(names):
        base = path.rsplit("/", 1)[-1]
        raw = f"medsl/raw/{year}-github-{base}"
        dest = os.path.join(F.CACHE, raw)
        if not os.path.exists(dest + ".meta.json"):
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "wb") as f:
                f.write(_git("show", f"{d['commit']}:{path}", cwd=repo_dir))
            h = hashlib.sha256()
            with open(dest, "rb") as f:
                for chunk in iter(lambda: f.read(1 << 20), b""):
                    h.update(chunk)
            with open(dest + ".meta.json", "w") as f:
                json.dump({"url": f"https://github.com/{d['github']}/blob/{d['commit']}/{path}", "served_from": "git",
                           "read_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
                           "bytes": os.path.getsize(dest), "sha256": h.hexdigest()}, f, indent=1)
        out.append({"id": "github", "name": base, "raw": raw})
    return out


def _digests(path):
    """(bytes, md5) of a file, and of each member if it is a zip: the Dataverse records an MD5 for each file."""
    import hashlib
    import zipfile

    def md5(fh):
        h = hashlib.md5()
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
        return h.hexdigest()
    with open(path, "rb") as f:
        out = {"bytes": os.path.getsize(path), "md5": md5(f), "members": {}}
    if path.endswith(".zip"):
        with zipfile.ZipFile(path) as z:
            for i in z.infolist():
                if not i.is_dir() and not i.filename.startswith("__MACOSX"):
                    with z.open(i) as fh:
                        out["members"][i.filename.rsplit("/", 1)[-1]] = {"bytes": i.file_size, "md5": md5(fh)}
    return out


def compare_dataverse(year):
    """The GitHub-held files of a year against MEDSL's Dataverse sets of the same year (the orchestrator, 06:16:
    "compare their files to the Dataverse sets"). Reads the collection's list of datasets and each dataset's
    record (names, sizes and MD5 digests are public; the files themselves sit behind a guestbook and are not read),
    and matches each GitHub file, or each file inside a GitHub zip, by MD5, else by name. Written to checks."""
    d = DATASETS[year]
    lst = F.fetch(f"{API}/dataverses/{d['collection']}/contents", f"medsl/collection-{d['collection']}.json")
    with open(lst) as f:
        items = json.load(f)["data"]
    dv_files = []
    sets = []
    for it in items:
        if it.get("type") != "dataset":
            continue
        doi = f"{it['protocol']}:{it['authority']}/{it['identifier']}"
        url = f"{API}/datasets/:persistentId/?persistentId={urllib.parse.quote(doi, safe=':/')}"
        path = F.fetch(url, f"medsl/record-{it['identifier'].replace('/', '-')}.json")
        with open(path) as f:
            v = json.load(f)["data"]["latestVersion"]
        title = next((x["value"] for x in v["metadataBlocks"]["citation"]["fields"] if x["typeName"] == "title"), "")
        sets.append({"doi": doi, "title": title, "files": len(v["files"]),
                     "licence": (v.get("license") or {}).get("name") if isinstance(v.get("license"), dict)
                     else v.get("license")})
        for x in v["files"]:
            df = x["dataFile"]
            dv_files.append({"doi": doi, "name": df.get("originalFileName") or df["filename"],
                             "bytes": df.get("originalFileSize") or df.get("filesize"), "md5": df.get("md5") or
                             (df.get("checksum") or {}).get("value")})
    by_md5 = {f["md5"]: f for f in dv_files if f["md5"]}
    by_name = collections.defaultdict(list)
    for f in dv_files:
        by_name[f["name"].rsplit(".", 1)[0].lower()].append(f)
    rows = []
    for fi in github_files(year):
        dg = _digests(os.path.join(F.CACHE, fi["raw"]))
        parts = [(fi["name"], dg["bytes"], dg["md5"])] + [(n, m["bytes"], m["md5"]) for n, m in dg["members"].items()]
        for name, nbytes, md5 in parts:
            hit = by_md5.get(md5)
            if hit:
                rows.append({"github": name, "bytes": nbytes, "same_md5_as": f"{hit['doi']} {hit['name']}"})
                continue
            near = by_name.get(name.rsplit(".", 1)[0].lower(), [])
            rows.append({"github": name, "bytes": nbytes, "same_md5_as": None,
                         "same_name_in": [{"doi": h["doi"], "name": h["name"], "bytes": h["bytes"]} for h in near]})
    out = {"collection": f"https://dataverse.harvard.edu/dataverse/{d['collection']}", "datasets": sets,
           "github_files": rows,
           "identical": sum(1 for r in rows if r["same_md5_as"]),
           "same_name_differs": sum(1 for r in rows if not r["same_md5_as"] and r["same_name_in"]),
           "no_counterpart": sum(1 for r in rows if not r["same_md5_as"] and not r["same_name_in"])}
    checks_path = os.path.join(OUT, f"checks-{year}.json")
    checks = {}
    if os.path.exists(checks_path):
        with open(checks_path) as f:
            checks = json.load(f)
    checks["dataverse_comparison"] = out
    with open(checks_path, "w") as f:
        json.dump(checks, f, indent=1)
    return out


def record(year):
    doi = DATASETS[year]["doi"]
    url = f"{API}/datasets/:persistentId/?persistentId={urllib.parse.quote(doi, safe=':/')}"
    path = F.fetch(url, f"medsl/record-{year}.json")
    with open(path) as f:
        return json.load(f)["data"]["latestVersion"], F.meta(f"medsl/record-{year}.json")


def data_files(year, rec):
    out = []
    for f in rec["files"]:
        df = f["dataFile"]
        name = df.get("originalFileName") or df["filename"]
        if not name.lower().endswith((".csv", ".tab", ".zip")) or "codebook" in name.lower() or name.endswith(".md"):
            continue
        out.append({"id": df["id"], "name": name, "ingested": bool(df.get("originalFileName")),
                    "bytes": df.get("originalFileSize") or df.get("filesize")})
    return out


def file_state(year, name):
    """The state a 2024 file covers, from its name ('2024-co-precinct-general.csv'); None if not by name."""
    m = re.match(r"^\d{4}-([a-z]{2})-", name)
    return m.group(1).upper() if m else None


def ddi_rows(file_id, year):
    """The row count Dataverse records for an ingested file (its DDI metadata's caseQnty), or None."""
    try:
        path = F.fetch(f"{API}/access/datafile/{file_id}/metadata/ddi", f"medsl/ddi-{year}-{file_id}.xml")
    except F.Refused:
        return None
    with open(path, encoding="utf-8", errors="replace") as f:
        m = re.search(r"<caseQnty>(\d+)</caseQnty>", f.read())
    return int(m.group(1)) if m else None


# ------------------------------------------------------------------ read and add up

def _rows(path):
    """The rows of a MEDSL csv, or of every csv inside a MEDSL zip (read in place, never extracted or run)."""
    if path.lower().endswith(".zip"):
        import io
        import zipfile
        with zipfile.ZipFile(path) as z:
            for member in z.namelist():
                if member.lower().endswith((".csv", ".tab", ".txt")) and not member.startswith("__MACOSX"):
                    with z.open(member) as raw:
                        delim = "\t" if member.lower().endswith(".tab") else ","
                        yield from csv.DictReader(io.TextIOWrapper(raw, encoding="utf-8", errors="replace"),
                                                  delimiter=delim)
        return
    with open(path, newline="", encoding="utf-8", errors="replace") as f:
        yield from csv.DictReader(f)


def fips5(x):
    """A county's FIPS code as five digits: MEDSL's 2022 Alabama file writes 1001 for 01001, and others 1001.0."""
    x = (x or "").strip()
    if re.fullmatch(r"\d{1,5}(\.0+)?", x):
        return f"{int(float(x)):05d}"
    return x


def read_file(path, only_states=None):
    """Rows of one MEDSL file into {contest key: {precinct key: {candidate key: {mode: votes or None}}}}; only the
    states named, where only_states is given."""
    agg = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(dict)))
    pres = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(dict)))
    house = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(dict)))
    n = 0
    states = collections.Counter()
    for row in _rows(path):
        n += 1
        dv = row.get("dataverse", "")
        cand = (row.get("candidate") or "").strip()
        if is_meta(cand):
            continue
        st = row.get("state_po", "")
        if only_states and st not in only_states:
            continue
        states[st] += 1
        v = row.get("votes", "")
        try:
            votes = int(float(v))
        except ValueError:
            votes = None          # "*": redacted (MEDSL's README)
        mode = (row.get("mode") or "TOTAL").upper()
        pk = (fips5(row.get("county_fips", "")), row.get("jurisdiction_fips", ""), row.get("precinct", ""))
        psim, pdet = row.get("party_simplified", ""), row.get("party_detailed", "")
        if psim == "OTHER" and pdet.upper() in DEMOCRATIC_AFFILIATES:
            psim = "DEMOCRAT"   # the 2022 files file Minnesota's DFL and North Dakota's Democratic-NPL as other
        ckey = (cand, pdet, psim, row.get("writein", ""))
        if dv in ("PRESIDENT", "HOUSE") and row.get("stage", "GEN") == "GEN":
            bucket = pres if dv == "PRESIDENT" else house
            bucket[st][pk][ckey][mode] = (bucket[st][pk][ckey].get(mode) or 0) + (votes or 0)
            continue
        if dv not in ("STATE", "LOCAL"):
            continue
        mag = row.get("magnitude", "")
        try:
            mag = str(int(float(mag)))
        except ValueError:
            pass
        k = (st, row.get("date", ""), row.get("stage", ""), row.get("special", ""), dv, row.get("office", ""),
             row.get("district", ""), mag)
        cell = agg[k][pk][ckey]
        if votes is None:
            cell[mode] = None
        elif cell.get(mode, 0) is not None:
            cell[mode] = cell.get(mode, 0) + votes
    return agg, pres, house, n, states


COUNTY_TOTAL = re.compile(r"^COUNTY[ _-]?TOTALS?$")


def drop_county_totals(agg):
    """A county's own sum filed as a precinct beside the county's precincts: MEDSL's 2022 Idaho file
    (2022-id-local-precinct-general.csv) gives each of its 44 counties a precinct named "COUNTY TOTAL" in nearly every
    office, so that the county is counted twice [measured, data/local/REPORT.md section 29]. The orchestrator's ruling
    of 2026-11-07 19:04: "apply the COUNTY TOTAL rule, marked, since it reproduces the canvass to the vote in every
    county MEDSL has". The rule: a candidate's line in a precinct of that name is dropped where the same contest key,
    county and candidate have lines in the county's other precincts and those add up to it; a line that is the
    county's only one for its candidate stays (Lincoln County's Commissioner district 3, one name in the total alone);
    a line whose precincts add up to something else stays too, and is counted, so that the check shows it.
    agg is {key: {precinct key: {candidate key: {mode: votes}}}}, with the county code first in the precinct key.
    Returns {"dropped": lines, "kept_alone": lines, "kept_unequal": lines}."""
    out = collections.Counter()
    for k, precincts in agg.items():
        by_county = collections.defaultdict(list)
        for pk in precincts:
            by_county[pk[0]].append(pk)
        for county, pks in by_county.items():
            totals = [pk for pk in pks if COUNTY_TOTAL.match((pk[2] or "").strip().upper())]
            for tk in totals:
                for ck in list(precincts[tk]):
                    others = [precincts[pk][ck] for pk in pks if pk not in totals and ck in precincts[pk]]
                    if not others:
                        out["kept_alone"] += 1
                        continue
                    if sum(resolve(m) or 0 for m in others) == (resolve(precincts[tk][ck]) or 0):
                        del precincts[tk][ck]
                        out["dropped"] += 1
                    else:
                        out["kept_unequal"] += 1
                if not precincts[tk]:
                    del precincts[tk]
    return dict(out)


def merge_statewide(agg):
    """An office filed STATEWIDE in some rows and under a district in others (Santa Cruz County, Arizona, files the
    2024 propositions under its supervisor districts) is one statewide office: its rows join the STATEWIDE key,
    each precinct keeping its own district, so that candidates' contests are still told apart by their names."""
    wide = {}
    for k in agg:
        if k[6] == "STATEWIDE":
            wide[k[:6]] = k
    moved = 0
    for k in list(agg):
        if k[6] != "STATEWIDE" and k[:6] in wide:
            target = agg[wide[k[:6]]]
            for pk, cands in agg.pop(k).items():
                for ck, modes in cands.items():
                    cell = target[pk + (k[6],)][ck]
                    for m_, v in modes.items():
                        cell[m_] = None if (v is None or cell.get(m_, 0) is None) else cell.get(m_, 0) + v
            moved += 1
    return moved


def resolve(modes):
    """One precinct's votes for one candidate: its TOTAL row where it has one, else the sum of its modes."""
    if "TOTAL" in modes:
        return modes["TOTAL"]
    if any(x is None for x in modes.values()):
        return None
    return sum(modes.values())


class _UF:
    def __init__(self):
        self.p = {}

    def find(self, x):
        self.p.setdefault(x, x)
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[rb] = ra


LEGISLATIVE = {"STATE HOUSE", "STATE SENATE"}
# Washington files its legislature as local offices named by district ("LEGISLATIVE DISTRICT 9 - STATE SENATOR")
_LEGISLATIVE_NAMED = re.compile(r"^LEGISLATIVE DISTRICT \d+ - STATE (SENATOR|REPRESENTATIVE)")


def is_legislative(office):
    return office in LEGISLATIVE or bool(_LEGISLATIVE_NAMED.match(office))
DROPPED = collections.Counter()   # lines that form no contest: write-in totals alone, with no candidate named


def contests_of(k, precincts):
    """Split one office-and-district key into contests, and add each one up. Returns a list of contest dicts.
    Yes-or-no lines and candidates' lines are taken apart first: one office name can hold both (a county's recall
    question beside another county's race for the same office, both filed as "DISTRICT ATTORNEY")."""
    yn = {}
    for pk, cands in precincts.items():
        for ck in cands:
            sa = split_answer(ck[0])
            if sa is not None:
                yn[ck] = sa
    qprec, cprec = {}, {}
    for pk, cands in precincts.items():
        q = {ck: m for ck, m in cands.items() if ck in yn}
        c = {ck: m for ck, m in cands.items() if ck not in yn}
        if q:
            qprec[pk] = q
        if c:
            cprec[pk] = c
    out = _contests(k, qprec, yn, True) if qprec else []
    for x in (_contests(k, cprec, yn, False) if cprec else []):
        if any(not is_generic(c["name"]) for c in x["candidates"]):
            out.append(x)
        else:
            DROPPED[k[0]] += 1
    return out


def _contests(k, precincts, yn, is_question):
    st, date, stage, special, dv, office, district, magnitude = k
    groups = collections.defaultdict(list)    # group key -> precinct keys
    if is_question:
        # one question per subject (a retention's judge, or none), statewide for a state question, per county if local
        for pk, cands in precincts.items():
            subjects = {yn[ck][0] for ck in cands if ck in yn}
            for s in subjects:
                groups[(s, "" if dv == "STATE" else pk[0])].append(pk)
    else:
        uf = _UF()
        first_by_cand = {}
        # a legislative district with its number given is one contest: its counties' spellings of a name differ
        # ('T O'MARA', 'THOMAS FELLERS O'MARA'), so precincts also join on the surname and party there; anywhere,
        # on the same words in another order ('LATHROP WILL')
        numbered = (office in LEGISLATIVE and district not in ("", "STATEWIDE")) or bool(_LEGISLATIVE_NAMED.match(office))
        for pk, cands in precincts.items():
            uf.find(pk)
            for ck in cands:
                name = ck[0].upper()
                if is_generic(name) or ck in yn:
                    continue
                toks = name_tokens(name)
                keys = [name]
                if len(toks) > 1:
                    keys.append(("words",) + tuple(sorted(toks)))
                if numbered and toks:
                    keys.append(("surname", toks[-1], ck[2]))
                for key in keys:
                    if key in first_by_cand:
                        uf.union(first_by_cand[key], pk)
                    else:
                        first_by_cand[key] = pk
        comp = collections.defaultdict(list)
        for pk in precincts:
            comp[uf.find(pk)].append(pk)
        # precincts with only write-in totals join their county's one component, if it has exactly one
        # and so do precincts whose only names are write-ins, where every county they lie in has one such component
        named_comp = {r: ps for r, ps in comp.items()
                      if any(not is_generic(ck[0]) and ck[3] != "TRUE" for p in ps for ck in precincts[p])}
        by_county = collections.defaultdict(set)
        for r, ps in named_comp.items():
            for p in ps:
                by_county[p[0]].add(r)
        for r, ps in comp.items():
            if r in named_comp:
                groups[("", r)].extend(ps)
                continue
            near = set().union(*(by_county[p[0]] for p in ps))
            target = next(iter(near)) if len(near) == 1 else None
            groups[("", target if target is not None else r)].extend(ps)
    out = []
    for (subject, _), pks in groups.items():
        tot = collections.defaultdict(int)
        missing = set()
        for pk in pks:
            for ck, modes in precincts[pk].items():
                if is_question and (ck not in yn or yn[ck][0] != subject):
                    continue
                v = resolve(modes)
                if v is None:
                    missing.add(ck)
                else:
                    tot[ck] += v
        cands = []
        for ck in set(tot) | missing:
            name, pdet, psim, wi = ck
            c = {"name": yn[ck][1] if is_question else name, "votes": tot.get(ck, 0)}
            if ck in missing:
                c["votes_missing_in_some_precincts"] = True
            if not is_question:
                c["party"] = psim or None
                if pdet and pdet != psim:
                    c["party_detailed"] = pdet
                if wi == "TRUE":
                    c["writein"] = True
            cands.append(c)
        if is_question:   # one line per answer: a state that splits YES across lines adds them
            merged = collections.defaultdict(lambda: {"votes": 0})
            for c in cands:
                m = merged[c["name"]]
                m["name"] = c["name"]
                m["votes"] += c["votes"]
                if c.get("votes_missing_in_some_precincts"):
                    m["votes_missing_in_some_precincts"] = True
            cands = list(merged.values())
        else:
            cands = merge_lines(cands, magnitude == "1")
        cands.sort(key=lambda c: -c["votes"])
        # some files list every precinct of the state under an office, with 0 votes where it is not on the ballot:
        # the contest's place is its precincts with a vote in it
        voted = [pk for pk in pks if any((resolve(m_) or 0) > 0 for ck, m_ in precincts[pk].items()
                                         if not is_question or (ck in yn and yn[ck][0] == subject))]
        counties = sorted({pk[0] for pk in voted})
        extra = {}
        if is_legislative(office):   # kept so that a district's lines can be compared across years (pipeline/local.py)
            extra["precinct_ids"] = sorted({"|".join(pk[:3]) for pk in voted})
        out.append({**extra, "state": st, "date": date, "stage": stage, "special": special == "TRUE", "dataverse": dv,
                    "office": office, "district": district, "subject": subject or None,
                    "magnitude": int(magnitude) if magnitude.isdigit() else None,
                    "question": is_question, "precincts": len(voted), "counties": counties,
                    "candidates": cands})
    return out


MAJOR = ("DEMOCRAT", "REPUBLICAN")


def merge_lines(cands, single_seat):
    """One candidate per person: a candidate on several parties' lines (New York's and Oregon's fusion) and a name
    spelled differently in different counties are one candidate with the votes of all their lines, which are kept
    under "lines". Names merge on the same words in any order; in a race for one seat, also on the same surname and
    first initial (same_person). Write-in lines merge only on the same name."""
    groups = []
    for c in sorted(cands, key=lambda c: -c["votes"]):
        wi = bool(c.get("writein")) or is_generic(c["name"])
        for g in groups:
            h = g[0]
            hw = bool(h.get("writein")) or is_generic(h["name"])
            if wi or hw:
                if wi and hw and h["name"] == c["name"]:
                    g.append(c)
                    break
                continue
            # by surname only between lines that are not two different major parties (a Democrat Smith and a
            # Republican Smith are two people; one person on both lines has the same name on both)
            clash = {h.get("party"), c.get("party")} >= set(MAJOR)
            if h["name"] == c["name"] or (single_seat and not clash and same_person(h["name"], c["name"])) or \
                    (len(name_tokens(h["name"])) > 1 and sorted(name_tokens(h["name"])) == sorted(name_tokens(c["name"]))):
                g.append(c)
                break
        else:
            groups.append([c])
    out = []
    for g in groups:
        if len(g) == 1:
            out.append(g[0])
            continue
        parties = {x.get("party") for x in g}
        majors = [p_ for p_ in MAJOR if p_ in parties]
        m = {"name": max((x["name"] for x in g), key=lambda n: (len(name_tokens(n)), len(n))),
             "votes": sum(x["votes"] for x in g)}
        if len(majors) == 2:
            m["party"] = "DEMOCRAT AND REPUBLICAN"
        elif majors:
            m["party"] = majors[0]
        else:
            top = max(g, key=lambda x: (bool(x.get("party")), x["votes"]))
            m["party"] = top.get("party")
            if top.get("party_detailed"):
                m["party_detailed"] = top["party_detailed"]
        if any(x.get("writein") for x in g):
            m["writein"] = True
        if any(x.get("votes_missing_in_some_precincts") for x in g):
            m["votes_missing_in_some_precincts"] = True
        m["lines"] = [{k: v for k, v in (("name", x["name"] if x["name"] != m["name"] else None),
                                         ("party", x.get("party")), ("party_detailed", x.get("party_detailed")),
                                         ("votes", x["votes"])) if v is not None} for x in g]
        out.append(m)
    return out


def _flat(cands):
    out = []
    for x in cands:
        if not x.get("lines"):
            out.append(x)
            continue
        for ln in x["lines"]:
            y = {"name": ln.get("name", x["name"]), "votes": ln["votes"]}
            for k in ("party", "party_detailed"):
                if ln.get(k):
                    y[k] = ln[k]
            for k in ("writein", "votes_missing_in_some_precincts"):
                if x.get(k):
                    y[k] = True
            out.append(y)
    return out


def join_unnumbered(contests):
    """Some counties leave a legislative contest's district out (New York, 2024): each such piece joins the one
    numbered district of the same office whose candidate it names (same_person, same party), so that the district's
    count is whole. Returns the contests left and the number of pieces joined."""
    numbered = collections.defaultdict(list)
    for c in contests:
        if is_legislative(c["office"]) and c["district"] not in ("", "STATEWIDE") and not c["question"]:
            numbered[(c["state"], c["date"], c["stage"], c["special"], c["office"])].append(c)
    keep, joined = [], 0
    for c in contests:
        if not (is_legislative(c["office"]) and c["district"] == "" and not c["question"]):
            keep.append(c)
            continue
        named = [x for x in c["candidates"] if not x.get("writein") and not is_generic(x["name"])]
        targets = [t for t in numbered[(c["state"], c["date"], c["stage"], c["special"], c["office"])]
                   if any(x.get("party") == y.get("party") and same_person(x["name"], y["name"])
                          for x in named for y in t["candidates"] if not y.get("writein") and not is_generic(y["name"]))]
        if len(targets) != 1:
            keep.append(c)
            continue
        t = targets[0]
        t["candidates"] = sorted(merge_lines(_flat(t["candidates"]) + _flat(c["candidates"]), t["magnitude"] == 1),
                                 key=lambda x: -x["votes"])
        t["precincts"] += c["precincts"]
        t["counties"] = sorted(set(t["counties"]) | set(c["counties"]))
        if "precinct_ids" in t or "precinct_ids" in c:
            t["precinct_ids"] = sorted(set(t.get("precinct_ids", [])) | set(c.get("precinct_ids", [])))
        t["pieces_without_district_joined"] = t.get("pieces_without_district_joined", 0) + 1
        joined += 1
    return keep, joined


def house_by_county(house):
    """{state: {county FIPS: [Democratic votes, Republican votes, 1 if every precinct's House race had both]}}: the
    US House vote by county, the lean a local race's forecast reads (the orchestrator, 06:16). A candidate's votes
    on every line count for the party whose line the candidate holds (fusion: New York, Connecticut). A precinct is
    contested when a Democrat and a Republican are both printed on its ballot (not write-ins), whatever their
    votes there; a county with any precinct that is not is marked 0."""
    out = {}
    for st, precincts in house.items():
        by = collections.defaultdict(lambda: [0, 0, 1])
        for pk, cands in precincts.items():
            party = {}
            for ck in cands:
                if ck[2] in ("DEMOCRAT", "REPUBLICAN") and (ck[3] or "").upper() not in ("TRUE", "1", "YES"):
                    party.setdefault(ck[0], set()).add(ck[2])
            party = {c: next(iter(ps)) for c, ps in party.items() if len(ps) == 1}
            dv = rv = 0
            for ck, modes in cands.items():
                v = resolve(modes) or 0
                if party.get(ck[0]) == "DEMOCRAT":
                    dv += v
                elif party.get(ck[0]) == "REPUBLICAN":
                    rv += v
            row = by[pk[0]]
            row[0] += dv
            row[1] += rv
            listed = set(party.values())
            if listed != {"DEMOCRAT", "REPUBLICAN"} and any((resolve(m) or 0) > 0 for m in cands.values()):
                row[2] = 0
        out[st] = {c: v for c, v in sorted(by.items()) if c}
    return out


def president_totals(pres):
    out = {}
    for st, precincts in pres.items():
        tot = collections.defaultdict(int)
        for pk, cands in precincts.items():
            for ck, modes in cands.items():
                v = resolve(modes)
                tot[ck[0]] += v or 0
        out[st] = dict(tot)
    return out


# ------------------------------------------------------------------ the checks against D1's certified totals

def _norm(name):
    """'TRUMP, DONALD J.' and 'DONALD J TRUMP' to one key: the surname."""
    name = name.upper().replace(".", "")
    if "," in name:
        return name.split(",")[0].strip()
    parts = [p for p in name.split() if p not in ("JR", "SR", "II", "III")]
    return parts[-1] if parts else name


def check_president(year, totals):
    path = os.path.join(REPO, "data", "president", f"{year}.json")
    if not os.path.exists(path):
        return {"note": f"{path} not found"}
    with open(path) as f:
        d1 = json.load(f)
    out = {}
    for c in d1["contests"]:
        st = c["place"]["state"]
        if c["place"].get("district") or st not in totals:
            continue
        mine = collections.defaultdict(int)
        for name, v in totals[st].items():
            mine[_norm(name)] += v
        rows = []
        for cand in c["result"]["candidates"]:
            if cand.get("from"):          # D1 marks the candidates it took from MEDSL itself: not a check
                continue
            key = _norm(cand["name"])
            rows.append({"candidate": cand["name"], "certified": cand["votes"], "medsl_precincts": mine.get(key),
                         "difference": (mine.get(key) or 0) - cand["votes"]})
        out[st] = rows
    return out


def check_house(year, house):
    """The US House vote by state, MEDSL's precincts added up, against D2's certified results (data/house/<year>.json,
    from the Clerk's and the FEC's official results): every line's votes together ("all"), and the Democrats' and the
    Republicans' where D2's candidate stands on that party's line alone. D2 gives a fusion candidate's votes on all
    their lines together, which MEDSL splits by line, so only the "all" row is compared in every state."""
    path = os.path.join(REPO, "data", "house", f"{year}.json")
    if not os.path.exists(path) or not house:
        return {}
    with open(path) as f:
        d2 = json.load(f)
    cert = collections.defaultdict(collections.Counter)
    fusion = set()
    for c in d2["contests"]:
        if c.get("special"):
            continue
        for cand in c["result"]["candidates"]:
            v = cand.get("votes") or 0
            cert[c["place"]["state"]]["all"] += v
            word = (cand.get("party") or "")
            if word in ("Democrat", "Republican"):
                cert[c["place"]["state"]][word[0]] += v
            elif "/" in word:
                fusion.add(c["place"]["state"])
    out = {}
    for st, precincts in house.items():
        mine = collections.Counter()
        for pk, cands in precincts.items():
            for ck, modes in cands.items():
                v = resolve(modes) or 0
                mine["all"] += v
                p_ = {"DEMOCRAT": "D", "REPUBLICAN": "R"}.get(ck[2])
                if p_:
                    mine[p_] += v
        rows = [{"party": "all", "certified": cert[st]["all"], "medsl_precincts": mine["all"],
                 "difference": mine["all"] - cert[st]["all"]}]
        if st not in fusion:
            rows += [{"party": p_, "certified": cert[st][p_], "medsl_precincts": mine[p_],
                      "difference": mine[p_] - cert[st][p_]} for p_ in ("D", "R")]
        out[st] = rows
    return out


# ------------------------------------------------------------------ main

def run(year, only=None):
    gh = "github" in DATASETS[year]
    if gh:
        rec, rec_meta = {}, None
        files = github_files(year)
    else:
        rec, rec_meta = record(year)
        files = data_files(year, rec)
    os.makedirs(os.path.join(OUT, str(year)), exist_ok=True)
    checks_path = os.path.join(OUT, f"checks-{year}.json")
    checks = {}
    if os.path.exists(checks_path):
        with open(checks_path) as f:
            checks = json.load(f)
    checks.setdefault("files", {})
    checks.setdefault("president", {})
    for fi in files:
        st = file_state(year, fi["name"])
        if only and (st or "") not in only:
            continue
        if gh:
            raw, expected = fi["raw"], None
            path = os.path.join(F.CACHE, raw)
        else:
            raw = f"medsl/raw/{year}-{fi['id']}-{fi['name']}"
            url = f"{API}/access/datafile/{fi['id']}" + ("?format=original" if fi["ingested"] else "")
            path = F.fetch(url, raw, storage_sites=("amazonaws.com",))
            expected = ddi_rows(fi["id"], year) if fi["ingested"] else None
        first = next(iter(_rows(path)), {})
        if "party_simplified" not in first or "county_fips" not in first:
            # MEDSL's older layout (party, county by name, no magnitude): 2018's Wisconsin file. Its offices are
            # the state's own (governor, statewide officers, legislature), which Klarner records; no local race.
            checks["files"][fi["name"]] = {"read": False, "why": "the file is in MEDSL's older layout (no "
                                           "party_simplified, county_fips or magnitude columns); it holds state "
                                           "offices only, which Klarner records for the legislature",
                                           "columns": sorted(first)}
            print(f"{fi['name']}: not read (older layout)", flush=True)
            continue
        agg, pres, house, n, states = read_file(path)
        totals = drop_county_totals(agg)
        totals_federal = drop_county_totals({**{("P", s): v for s, v in pres.items()},
                                             **{("H", s): v for s, v in house.items()}})
        moved = merge_statewide(agg)
        contests = []
        for k, precincts in agg.items():
            contests.extend(contests_of(k, precincts))
        contests, joined = join_unnumbered(contests)
        by_state = collections.defaultdict(list)
        for c in contests:
            by_state[c["state"]].append(c)
        m = F.meta(raw)
        for s, cs in by_state.items():
            fid = fi["id"] if not gh else re.sub(r"[^a-z0-9]+", "-", fi["name"].lower().rsplit(".", 1)[0])
            with open(os.path.join(OUT, str(year), f"{s}-{fid}.jsonl"), "w") as f:
                for c in cs:
                    c["file"] = {"id": fi["id"], "name": fi["name"], "url": m["url"], "read_utc": m["read_utc"],
                                 "sha256": m["sha256"]}
                    f.write(json.dumps(c, ensure_ascii=False, separators=(",", ":")) + "\n")
        checks["files"][fi["name"]] = {"rows_read": n, "rows_recorded_by_dataverse": expected,
                                       "rows_ok": (expected is None) or (expected == n),
                                       "contests": len(contests), "states": dict(states),
                                       "district_keys_joined_to_statewide": moved,
                                       "legislative_pieces_without_district_joined": joined,
                                       "county_total_lines": totals, "county_total_lines_federal": totals_federal}
        checks["president"].update(check_president(year, president_totals(pres)))
        checks.setdefault("house_by_party", {}).update(check_house(year, house))
        checks.setdefault("house_by_county", {}).update(house_by_county(house))
        checks.setdefault("write_in_lines_alone", {}).update(dict(DROPPED))
        print(f"{fi['name']}: {n:,} rows (Dataverse records {expected}), {len(contests):,} contests", flush=True)
        with open(checks_path, "w") as f:
            json.dump(checks, f, indent=1)
    if gh:
        d = DATASETS[year]
        checks["record"] = {"github": d["github"], "commit": d["commit"], "title": d["title"],
                            "licence": "no licence file in the repository",
                            "read_utc": F.meta(files[0]["raw"])["read_utc"] if files else None,
                            "url": f"https://github.com/{d['github']}/tree/{d['commit']}"}
    else:
        checks["record"] = {"doi": DATASETS[year]["doi"],
                            "version": f"{rec.get('versionNumber')}.{rec.get('versionMinorNumber')}",
                            "licence": (rec.get("license") or {}).get("name") if isinstance(rec.get("license"), dict)
                            else rec.get("license"),
                            "read_utc": rec_meta["read_utc"], "url": rec_meta["url"]}
    with open(checks_path, "w") as f:
        json.dump(checks, f, indent=1)
    return checks


_YES16 = re.compile(r"^(YES|FOR|IN FAVOR|APPROVE|APPROVED|ACCEPT|RETAIN)\b")
_NO16 = re.compile(r"^(NO|AGAINST|OPPOSED|REJECT|REJECTED|NOT RETAIN|DO NOT RETAIN)\b(?! (NAME|CANDIDATE|CONFIDENCE))")


def _answer16(cand):
    if _NO16.match(cand):
        return "NO"
    if _YES16.match(cand) and not re.match(r"^FOR (ALL|UNOPPOSED)", cand):
        return "YES"
    return None


def _office16(o):
    """One spelling for a 2016 office across counties: upper case, single spaces, none inside brackets."""
    o = re.sub(r"\s+", " ", (o or "").upper()).strip().rstrip(",.;")
    return re.sub(r"\(\s+", "(", re.sub(r"\s+\)", ")", o))


# MEDSL's 2022 state offices set (OAARCY), read for the eight states whose UYQIEP file is named a local file, to
# see whether it holds state offices those files lack. It does not [measured, 2026-11-07]: it holds ID, IN, ND and
# WA only, the same 363 contests their UYQIEP files give, and none for AR, AZ, MD or MI. So it is read to a folder of
# its own (normalized/oaarcy-2022) for that comparison (pipeline/local_medsl.py check-oaarcy), and not into 2022.
OAARCY = {"id": 14249788, "name": "STATE_precinct_general.csv", "doi": "doi:10.7910/DVN/OAARCY",
          "title": "State Offices Precinct-Level Returns 2022", "states": ("AR", "AZ", "ID", "IN", "MD", "MI", "ND", "WA")}


def run_oaarcy(out_dir=None):
    """The eight states' 2022 state offices from OAARCY, into out_dir (default: the 2022 normalized folder),
    one file per state named by the file's id."""
    out_dir = out_dir or os.path.join(OUT, "oaarcy-2022")
    os.makedirs(out_dir, exist_ok=True)
    raw = f"medsl/raw/2022-{OAARCY['id']}-{OAARCY['name']}"
    path = F.fetch(f"{API}/access/datafile/{OAARCY['id']}", raw, timeout_s=3600, storage_sites=("amazonaws.com",))
    agg, pres, house, n, states = read_file(path, set(OAARCY["states"]))
    merge_statewide(agg)
    contests = []
    for k, precincts in agg.items():
        contests.extend(contests_of(k, precincts))
    contests, joined = join_unnumbered(contests)
    m = F.meta(raw)
    by_state = collections.defaultdict(list)
    for c in contests:
        by_state[c["state"]].append(c)
    for st_, cs in by_state.items():
        with open(os.path.join(out_dir, f"{st_}-{OAARCY['id']}.jsonl"), "w") as f:
            for c in cs:
                c["file"] = {"id": OAARCY["id"], "name": OAARCY["name"], "url": m["url"], "read_utc": m["read_utc"],
                             "sha256": m["sha256"], "doi": OAARCY["doi"]}
                f.write(json.dumps(c, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"{OAARCY['name']}: {n:,} rows read, {sum(states.values()):,} in the eight states, {len(contests):,} contests",
          flush=True)
    return {"rows_read": n, "states": dict(states), "contests": len(contests),
            "legislative_pieces_without_district_joined": joined}


def run_2016():
    """2016's questions from MEDSL's state and local precinct sets (older layout). A contest is the office's
    rows in a state under one spelling (_office16), across its counties; it is a question when every line on it
    other than write-ins and ballot counts is a yes or a no, and it has both. A precinct's votes for an answer are
    its total row where it has one, else the sum of its modes."""
    os.makedirs(os.path.join(OUT, "2016"), exist_ok=True)
    checks = {"files": {}, "president": {}, "house_by_county": {}, "record": {"sets": []}}
    for fid, name, dv, doi, title in SETS_2016:
        raw = f"medsl/raw/2016-{fid}-{name}"
        path = F.fetch(f"{API}/access/datafile/{fid}?format=original", raw, timeout_s=3600,
                       storage_sites=("amazonaws.com",))
        agg = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(dict)))
        other = set()
        n = 0
        states = collections.Counter()
        for row in _rows(path):
            n += 1
            st = row.get("state_postal", "")
            states[st] += 1
            cand = re.sub(r"\s+", " ", (row.get("candidate") or "").upper()).strip()
            k = (st, row.get("stage", "").upper(), (row.get("special") or "").upper() == "TRUE",
                 _office16(row.get("office")), (row.get("district") or "").strip())
            if not cand or is_meta(cand) or (row.get("writein") or "").upper() == "TRUE" or is_generic(cand):
                continue
            a = _answer16(cand)
            if a is None:
                other.add(k)
                continue
            if k in other:
                continue
            try:
                v = int(float(row.get("votes") or ""))
            except ValueError:
                v = None
            pk = (fips5(row.get("county_fips", "")), row.get("jurisdiction", ""), row.get("precinct", ""))
            mode = (row.get("mode") or "TOTAL").upper()
            cell = agg[k][pk][a]
            cell[mode] = None if v is None or cell.get(mode, 0) is None else cell.get(mode, 0) + v
        m = F.meta(raw)
        by_state = collections.defaultdict(list)
        for k, precincts in agg.items():
            if k in other:
                continue
            tot = collections.Counter()
            missing = set()
            counties = set()
            for pk, cands in precincts.items():
                for a, modes in cands.items():
                    v = resolve(modes)
                    if v is None:
                        missing.add(a)
                    else:
                        tot[a] += v
                if any((resolve(md) or 0) > 0 for md in cands.values()):
                    counties.add(pk[0])
            if set(tot) != {"YES", "NO"} or not sum(tot.values()):
                continue
            st, stage, special, office, district = k
            by_state[st].append({"state": st, "date": "2016-11-08" if stage == "GEN" else "", "stage": stage,
                                 "special": special, "dataverse": dv, "office": office, "district": district,
                                 "subject": None, "magnitude": 1, "question": True, "precincts": len(precincts),
                                 "counties": sorted(c for c in counties if c),
                                 "candidates": [{"votes": tot[a], "name": a, **({"votes_missing_in_some_precincts":
                                                                                 True} if a in missing else {})}
                                                for a in ("YES", "NO")],
                                 "file": {"id": fid, "name": name, "url": m["url"], "read_utc": m["read_utc"],
                                          "sha256": m["sha256"]}})
        nq = 0
        joined = 0
        for st, cs in by_state.items():
            # a county spelling the office apart ("TWELEVE" for "TWELVE"): near-identical wording, other counties
            import difflib
            cs.sort(key=lambda c: -len(c["counties"]))
            keep = []
            for c in cs:
                for k in keep:
                    if (k["stage"], k["special"], k["district"]) == (c["stage"], c["special"], c["district"]) and \
                            not set(k["counties"]) & set(c["counties"]) and \
                            difflib.SequenceMatcher(None, k["office"], c["office"]).ratio() >= 0.95:
                        for x, y in zip(k["candidates"], c["candidates"]):
                            x["votes"] += y["votes"]
                            if y.get("votes_missing_in_some_precincts"):
                                x["votes_missing_in_some_precincts"] = True
                        k["counties"] = sorted(set(k["counties"]) | set(c["counties"]))
                        k["precincts"] += c["precincts"]
                        k.setdefault("joined_from", [k["office"]]).append(c["office"])
                        joined += 1
                        break
                else:
                    keep.append(c)
            cs[:] = keep
            with open(os.path.join(OUT, "2016", f"{st}-{fid}.jsonl"), "w") as f:
                for c in cs:
                    f.write(json.dumps(c, ensure_ascii=False, separators=(",", ":")) + "\n")
            nq += len(cs)
        checks["files"][name] = {"rows_read": n, "rows_recorded_by_dataverse": None, "rows_ok": True,
                                 "contests": nq, "states": dict(states), "questions_only": True,
                                 "spellings_joined": joined}
        checks["record"]["sets"].append({"doi": doi, "title": title, "licence": "CC0 1.0", "read_utc": m["read_utc"],
                                         "url": f"https://doi.org/{doi.split(':', 1)[1]}"})
        print(f"{name}: {n:,} rows, {nq:,} questions", flush=True)
    with open(os.path.join(OUT, "checks-2016.json"), "w") as f:
        json.dump(checks, f, indent=1)
    return checks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("year", type=int, choices=sorted(DATASETS) + [2016])
    ap.add_argument("--states", default="")
    ap.add_argument("--oaarcy", action="store_true", help="2022: read OAARCY's eight states to a folder of their own")
    ap.add_argument("--compare-dataverse", action="store_true",
                    help="a GitHub-held year: compare its files with MEDSL's Dataverse sets, by MD5")
    a = ap.parse_args()
    if a.oaarcy:
        print(json.dumps(run_oaarcy(), indent=1))
        return
    if a.compare_dataverse:
        r = compare_dataverse(a.year)
        print(json.dumps({k: v for k, v in r.items() if k != "github_files"}, indent=1))
        return
    if a.year == 2016:
        run_2016()
        return
    only = {s.strip().upper() for s in a.states.split(",") if s.strip()} or None
    run(a.year, only)


if __name__ == "__main__":
    main()
