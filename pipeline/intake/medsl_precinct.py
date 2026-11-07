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
     not show which place holds it;
  4. checks: the rows read against the row count Dataverse records for the file, where it records one; and the
     presidency's totals by state and candidate against D1's certified totals in data/president/<year>.json.
Writes $VOTE_CACHE/medsl/normalized/<year>/<ST>.jsonl (one contest per line) and checks-<year>.json.

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
}
OUT = os.path.join(F.CACHE, "medsl", "normalized")
csv.field_size_limit(1 << 24)

# answers on a yes-or-no question, and the separators states put between a question's subject and its answer
ANSWERS = {"YES", "NO", "FOR", "AGAINST", "APPROVE", "REJECT", "APPROVED", "REJECTED", "ACCEPT", "RETAIN",
           "NOT RETAIN", "DO NOT RETAIN", "BONDS YES", "BONDS NO", "YES ON", "NO ON", "FOR THE MEASURE",
           "AGAINST THE MEASURE", "IN FAVOR", "OPPOSED"}
NOT_CANDIDATES = {"", "OVERVOTES", "UNDERVOTES", "OVER VOTES", "UNDER VOTES", "BLANK", "BLANK VOTES", "SPOILED",
                  "TOTAL VOTES", "BALLOTS CAST", "REGISTERED VOTERS", "OVERVOTE", "UNDERVOTE", "NONE OF THE ABOVE"}
GENERIC = {"WRITE-IN", "WRITEIN", "WRITE IN", "SCATTERING", "WRITE-INS", "UNCERTIFIED WRITE-IN", "UNQUALIFIED WRITE-IN"}


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
        if not name.lower().endswith((".csv", ".tab")) or "codebook" in name.lower() or name.endswith(".md"):
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

def read_file(path):
    """Rows of one MEDSL file into {contest key: {precinct key: {candidate key: {mode: votes or None}}}}."""
    agg = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(dict)))
    pres = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(dict)))
    n = 0
    states = collections.Counter()
    with open(path, newline="", encoding="utf-8", errors="replace") as f:
        for row in csv.DictReader(f):
            n += 1
            dv = row.get("dataverse", "")
            cand = (row.get("candidate") or "").strip()
            if cand.upper() in NOT_CANDIDATES:
                continue
            st = row.get("state_po", "")
            states[st] += 1
            v = row.get("votes", "")
            try:
                votes = int(float(v))
            except ValueError:
                votes = None          # "*": redacted (MEDSL's README)
            mode = (row.get("mode") or "TOTAL").upper()
            pk = (row.get("county_fips", ""), row.get("jurisdiction_fips", ""), row.get("precinct", ""))
            ckey = (cand, row.get("party_detailed", ""), row.get("party_simplified", ""), row.get("writein", ""))
            if dv == "PRESIDENT":
                pres[st][pk][ckey][mode] = (pres[st][pk][ckey].get(mode) or 0) + (votes or 0)
                continue
            if dv not in ("STATE", "LOCAL"):
                continue
            k = (st, row.get("date", ""), row.get("stage", ""), row.get("special", ""), dv, row.get("office", ""),
                 row.get("district", ""), row.get("magnitude", ""))
            cell = agg[k][pk][ckey]
            if votes is None:
                cell[mode] = None
            elif cell.get(mode, 0) is not None:
                cell[mode] = cell.get(mode, 0) + votes
    return agg, pres, n, states


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


def contests_of(k, precincts):
    """Split one office-and-district key into contests, and add each one up. Returns a list of contest dicts."""
    st, date, stage, special, dv, office, district, magnitude = k
    yn = {}
    for pk, cands in precincts.items():
        for ck in cands:
            sa = split_answer(ck[0])
            if sa is not None:
                yn[ck] = sa
    named_all = {ck for cands in precincts.values() for ck in cands}
    is_question = bool(named_all) and all(ck in yn or ck[0].upper() in GENERIC for ck in named_all) and bool(yn)
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
        for pk, cands in precincts.items():
            uf.find(pk)
            for ck in cands:
                name = ck[0].upper()
                if name in GENERIC or ck in yn:
                    continue
                if name in first_by_cand:
                    uf.union(first_by_cand[name], pk)
                else:
                    first_by_cand[name] = pk
        comp = collections.defaultdict(list)
        for pk in precincts:
            comp[uf.find(pk)].append(pk)
        # precincts with only write-in totals join their county's one component, if it has exactly one
        named_comp = {r: ps for r, ps in comp.items()
                      if any(ck[0].upper() not in GENERIC for p in ps for ck in precincts[p])}
        by_county = collections.defaultdict(set)
        for r, ps in named_comp.items():
            for p in ps:
                by_county[p[0]].add(r)
        for r, ps in comp.items():
            if r in named_comp:
                groups[("", r)].extend(ps)
                continue
            cs = {p[0] for p in ps}
            target = next(iter(by_county[next(iter(cs))])) if len(cs) == 1 and len(by_county[next(iter(cs))]) == 1 else None
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
        cands.sort(key=lambda c: -c["votes"])
        counties = sorted({pk[0] for pk in pks})
        out.append({"state": st, "date": date, "stage": stage, "special": special == "TRUE", "dataverse": dv,
                    "office": office, "district": district, "subject": subject or None,
                    "magnitude": int(magnitude) if magnitude.isdigit() else None,
                    "question": is_question, "precincts": len(pks), "counties": counties,
                    "candidates": cands})
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


# ------------------------------------------------------------------ main

def run(year, only=None):
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
        raw = f"medsl/raw/{year}-{fi['id']}-{fi['name']}"
        url = f"{API}/access/datafile/{fi['id']}" + ("?format=original" if fi["ingested"] else "")
        path = F.fetch(url, raw, storage_sites=("amazonaws.com",))
        expected = ddi_rows(fi["id"], year) if fi["ingested"] else None
        agg, pres, n, states = read_file(path)
        contests = []
        for k, precincts in agg.items():
            contests.extend(contests_of(k, precincts))
        by_state = collections.defaultdict(list)
        for c in contests:
            by_state[c["state"]].append(c)
        m = F.meta(raw)
        for s, cs in by_state.items():
            with open(os.path.join(OUT, str(year), f"{s}.jsonl"), "w") as f:
                for c in cs:
                    c["file"] = {"id": fi["id"], "name": fi["name"], "url": m["url"], "read_utc": m["read_utc"],
                                 "sha256": m["sha256"]}
                    f.write(json.dumps(c, ensure_ascii=False, separators=(",", ":")) + "\n")
        checks["files"][fi["name"]] = {"rows_read": n, "rows_recorded_by_dataverse": expected,
                                       "rows_ok": (expected is None) or (expected == n),
                                       "contests": len(contests), "states": dict(states)}
        checks["president"].update(check_president(year, president_totals(pres)))
        print(f"{fi['name']}: {n:,} rows (Dataverse records {expected}), {len(contests):,} contests", flush=True)
        with open(checks_path, "w") as f:
            json.dump(checks, f, indent=1)
    checks["record"] = {"doi": DATASETS[year]["doi"], "version": f"{rec.get('versionNumber')}.{rec.get('versionMinorNumber')}",
                        "licence": (rec.get("license") or {}).get("name") if isinstance(rec.get("license"), dict) else rec.get("license"),
                        "read_utc": rec_meta["read_utc"], "url": rec_meta["url"]}
    with open(checks_path, "w") as f:
        json.dump(checks, f, indent=1)
    return checks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("year", type=int, choices=sorted(DATASETS))
    ap.add_argument("--states", default="")
    a = ap.parse_args()
    only = {s.strip().upper() for s in a.states.split(",") if s.strip()} or None
    run(a.year, only)


if __name__ == "__main__":
    main()
