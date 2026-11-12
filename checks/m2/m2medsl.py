"""checks/m2/m2medsl.py: M2's own reader of MEDSL's precinct files and of North Carolina's State Board results files,
for the fifth pass (c34, c36).

Reads the raw files checks/m2/fetch_fifth_pass.sh fetched (MEDSL's 2016 local set, its 2018 per-state zips and 2020
local zip from GitHub, its 2022 and 2024 Dataverse files; the State Board's results_pct zips) and summarises each once
into ~/.cache/vote-m2/fifth/derived/<file>.json (a deterministic summary of the raw file, remade if missing):
  counties_all      "ST|date" -> every five-digit county with a positive vote in any contest below Congress (MEDSL's
                    dataverse STATE or LOCAL; the candidate not a total or a blank line);
  county_precincts  "ST|date|county" -> the county's precincts in the file on the date: from 2018, a precinct key with
                    a positive vote in any contest of any kind; in 2016, every key on a general-election row (as
                    pipeline/intake/medsl_county_precincts.py counts them, so that the counts can be compared; the
                    precinct key is (county FIPS, jurisdiction FIPS or jurisdiction, precinct), as that script's);
  state_contests    "ST|date|office|district" (dataverse STATE, stage GEN) -> its counties with a positive vote, the
                    magnitudes on its rows, its precincts with a vote, its candidates' votes;
  questions         "ST|date|county|office|district" (dataverse LOCAL, or any row of the 2016 local set, whose
                    candidate is an answer: answer_of) -> its precincts with a positive vote, every precinct key on
                    its rows, the yes and no votes.
A precinct's votes for a candidate are its TOTAL row where it has one, else the sum of its modes (MEDSL's README).
Nothing from pipeline/ is imported; the total and blank lines MEDSL keeps as candidates are listed here again
(NOT_CANDIDATES, _META), copied from pipeline/intake/medsl_precinct.py so that the same rows are skipped.
"""
import collections
import csv
import hashlib
import io
import json
import os
import re
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402

FIFTH = os.path.join(L.CACHE, "fifth")
DERIVED = os.path.join(FIFTH, "derived")
csv.field_size_limit(1 << 24)

# copied from pipeline/intake/medsl_precinct.py (NOT_CANDIDATES and _META), so that the same rows are read as no candidate
NOT_CANDIDATES = {"", "OVERVOTES", "UNDERVOTES", "OVER VOTES", "UNDER VOTES", "BLANK", "BLANK VOTES", "SPOILED",
                  "TOTAL VOTES", "BALLOTS CAST", "REGISTERED VOTERS", "OVERVOTE", "UNDERVOTE", "NONE OF THE ABOVE",
                  "CONTEST TOTAL", "CAST VOTES", "VOID", "BLANKS", "BLANK BALLOTS", "INVALID VOTES", "INVALID",
                  "NO CANDIDATE FILED", "NO PETITION FILED",
                  "PUBLIC COUNTER", "ABSENTEE / MILITARY", "AFFIDAVIT", "FEDERAL", "MANUALLY COUNTED EMERGENCY",
                  "SPECIAL VOTES", "BLANK/VOID", "NONE OF THESE CANDIDATES"}
_META = re.compile(r"^(TOTAL\b|VOTE FOR \d|TIMES (BLANK|OVER|UNDER)|.*\b(VOTES CAST|BALLOTS CAST|REGISTERED VOTERS|OVER ?VOTES?|"
                   r"UNDER ?VOTES?|BLANK VOTES?)\b)")
ANSWERS = {"YES", "NO", "FOR", "AGAINST", "APPROVE", "REJECT", "APPROVED", "REJECTED", "ACCEPT", "RETAIN",
           "NOT RETAIN", "DO NOT RETAIN", "BONDS YES", "BONDS NO", "YES ON", "NO ON", "FOR THE MEASURE",
           "AGAINST THE MEASURE", "IN FAVOR", "OPPOSED", "IN FAVOR OF", "YES FOR APPROVAL", "NO FOR REJECTION"}


def is_meta(cand):
    c = cand.strip().upper()
    return c in NOT_CANDIDATES or bool(_META.match(c))


_YES = re.compile(r"^(YES|FOR|IN FAVOR|APPROVE|APPROVED|ACCEPT|RETAIN|BONDS YES)\b|\b(- |\()?YES\)?$")
_NO = re.compile(r"^(NO|AGAINST|OPPOSED|REJECT|REJECTED|NOT RETAIN|DO NOT RETAIN|BONDS NO)\b|\b(- |\()?NO\)?$")


def answer_of(cand):
    """YES or NO where a candidate line is a question's answer ('YES', 'For', 'Yes - Jefferson County Amendment',
    'AGAINST THE PROPOSITION - NO'; MEDSL's 2016 files word the answers so), else None"""
    c = " ".join(cand.strip().upper().split())
    if c in ANSWERS:
        return "NO" if c.startswith(("NO", "AGAINST", "REJECT", "OPPOSED", "NOT RETAIN", "DO NOT RETAIN", "BONDS NO")) else "YES"
    if _YES.search(c) and not _NO.search(c):
        return "YES"
    if _NO.search(c) and not _YES.search(c):
        return "NO"
    if " - " in c:   # 'JUDI FULLER - AGAINST', 'JUDI FULLER - FOR RECALLING JUDI FULLER' (ID 2024): the part after the name
        return answer_of(c.split(" - ", 1)[1])
    return None


def fips5(x):
    x = (x or "").strip()
    if re.fullmatch(r"\d{1,5}(\.0+)?", x):
        return f"{int(float(x)):05d}"
    return x


def office_key(o):
    """one spelling of an office: upper case, single spaces, no spaces inside brackets, no trailing punctuation
    (pipeline/intake/medsl_precinct.py _office16 reads 2016's offices so; applied here to every year's for matching)"""
    o = re.sub(r"\s+", " ", (o or "").upper()).strip().rstrip(",.;")
    return re.sub(r"\(\s+", "(", re.sub(r"\s+\)", ")", o))


def rows(path):
    """the rows of a csv, or of every csv inside a zip (read in place)"""
    if path.lower().endswith(".zip"):
        with zipfile.ZipFile(path) as z:
            for member in z.namelist():
                if member.lower().endswith((".csv", ".tab", ".txt")) and not member.startswith("__MACOSX"):
                    with z.open(member) as raw:
                        delim = "\t" if member.lower().endswith(".tab") else ","
                        yield from csv.DictReader(io.TextIOWrapper(raw, encoding="utf-8", errors="replace"), delimiter=delim)
        return
    with open(path, newline="", encoding="utf-8", errors="replace") as f:
        yield from csv.DictReader(f)


def _resolve(modes):
    if "TOTAL" in modes:
        return modes["TOTAL"]
    if any(x is None for x in modes.values()):
        return None
    return sum(modes.values())


def fetched():
    """key -> path of what checks/m2/fetch_fifth_pass.sh fetched (HTTP 200), and the git-shown MEDSL zips by name"""
    out = {}
    p = os.path.join(FIFTH, "index.txt")
    if not os.path.exists(p):
        return out
    for line in open(p):
        f = line.rstrip("\n").split("\t")
        if f[0] == "medsl" and len(f) >= 4 and os.path.exists(f[3]):
            out["medsl:2018:" + os.path.basename(f[3])] = f[3]
        elif len(f) >= 6 and f[1] == "200" and os.path.exists(f[5]):
            out[f[0]] = f[5]
    return out


def medsl_file(year, st):
    """the raw MEDSL file of a state-year, among those fetched: 2018 and 2024 by state, 2022 by its own names, 2020
    and 2016 the one file"""
    f = fetched()
    if year == 2016:
        return f.get("medsl:2016:2016-precinct-local.csv")
    return _one_file(f, year, st)


def medsl_files(year, st):
    """every raw MEDSL file of a state-year the pipeline reads its questions from: 2016's two sets (local and state),
    else the one file"""
    f = fetched()
    if year == 2016:
        return [p for k in ("medsl:2016:2016-precinct-local.csv", "medsl:2016:2016-precinct-state.csv") for p in [f.get(k)] if p]
    p = _one_file(f, year, st)
    return [p] if p else []


def _one_file(f, year, st):
    if year == 2020:
        p = os.path.join(L.CACHE, "fourth", "medsl", "2020-all-states-local-precinct-general.zip")
        return p if os.path.exists(p) else None
    if year == 2018:
        for k, p in f.items():
            if k.startswith("medsl:2018:") and p.endswith(f"2018-{st.lower()}-precinct-general.zip"):
                return p
        p = os.path.join(L.CACHE, "fourth", "medsl", f"2018-{st.lower()}-precinct-general.zip")
        return p if os.path.exists(p) else None
    if year == 2024:
        return f.get(f"medsl:2024:2024-{st.lower()}-precinct-general.csv")
    if year == 2022:
        for k, p in f.items():
            n = os.path.basename(p).lower()
            if k.startswith("medsl:2022:") and (n.startswith(f"2022-{st.lower()}-") or n.startswith(st.lower() + "22")
                                                 or n.startswith(st.lower() + "-") or n.startswith(st.lower() + "_")
                                                 or (st == "CO" and n.startswith("colorado"))):   # MEDSL's own names
                return p
    return None


def summary(path, year):
    """the derived summary of one raw file (made once; read from the cache after)"""
    os.makedirs(DERIVED, exist_ok=True)
    out_path = os.path.join(DERIVED, os.path.basename(path) + ".json")
    if os.path.exists(out_path):
        with open(out_path) as f:
            return json.load(f)
    sha = L.sha256(path)
    counties_all = collections.defaultdict(set)
    county_pk = collections.defaultdict(set)
    state_c = {}      # (st, date, office, district) -> {pk: {cand: {mode: votes}}}, magnitudes
    state_mag = collections.defaultdict(set)
    quest = {}        # (st, date, county, office, district) -> {pk: {cand: {mode: votes}}}
    quest_all_pk = collections.defaultdict(set)
    n = 0
    for r in rows(path):
        n += 1
        if year == 2016:
            st = r.get("state_postal", "")
            stage = (r.get("stage") or "").upper()
            if stage != "GEN":
                continue
            date = "2016-11-08"
            dv = "LOCAL"
            pk = (fips5(r.get("county_fips", "")), r.get("jurisdiction", ""), r.get("precinct", ""))
        else:
            st = r.get("state_po", "")
            stage = (r.get("stage") or "").upper()
            date = r.get("date", "")
            dv = r.get("dataverse", "")
            pk = (fips5(r.get("county_fips", "")), r.get("jurisdiction_fips", ""), r.get("precinct", ""))
        cand = (r.get("candidate") or "").strip()
        try:
            votes = int(float(r.get("votes") or ""))
        except ValueError:
            votes = None
        if is_meta(cand):
            continue
        if year == 2016:   # any general-election row of the file (the pipeline's county counts: meta lines aside)
            county_pk[(st, date, pk[0])].add(pk)
        elif votes is not None and votes > 0:
            county_pk[(st, date, pk[0])].add(pk)
        mode = (r.get("mode") or "TOTAL").upper()
        office = office_key(r.get("office"))
        district = (r.get("district") or "").strip()
        if dv in ("STATE", "LOCAL") and votes is not None and votes > 0 and re.fullmatch(r"\d{5}", pk[0]):
            counties_all[(st, date)].add(pk[0])
        if dv == "STATE" and stage == "GEN":
            key = (st, date, office, district)
            cell = state_c.setdefault(key, {}).setdefault(pk, {}).setdefault(cand.upper(), {})
            cell[mode] = None if votes is None or cell.get(mode, 0) is None else cell.get(mode, 0) + votes
            state_mag[key].add((r.get("magnitude") or "").strip())
        ans = answer_of(cand) if (dv == "LOCAL" or year == 2016) else None
        if ans:
            key = (st, date, pk[0], office, district)
            cell = quest.setdefault(key, {}).setdefault(pk, {}).setdefault(ans, {})
            cell[mode] = None if votes is None or cell.get(mode, 0) is None else cell.get(mode, 0) + votes
            quest_all_pk[key].add(pk)

    def fold(precincts):
        voted = set()
        tot = collections.Counter()
        for pk, cands in precincts.items():
            for c, modes in cands.items():
                v = _resolve(modes)
                if v is not None:
                    tot[c] += v
                if (v or 0) > 0:
                    voted.add(pk)
        return voted, tot
    sc = {}
    for key, precincts in state_c.items():
        voted, tot = fold(precincts)
        sc["|".join(key)] = {"counties": sorted({pk[0] for pk in voted}), "precincts": len(voted),
                             "magnitudes": sorted(state_mag[key]), "cands": dict(tot)}
    qs = {}
    for key, precincts in quest.items():
        voted, tot = fold(precincts)
        qs["|".join(key)] = {"precincts": len(voted), "all_keys": len(quest_all_pk[key]), "answers": dict(tot)}
    out = {"file": os.path.basename(path), "sha256": sha, "rows": n, "year": year,
           "counties_all": {"|".join(k): sorted(v) for k, v in counties_all.items()},
           "county_precincts": {"|".join(k): len(v) for k, v in county_pk.items()},
           "state_contests": sc, "questions": qs}
    with open(out_path, "w") as f:
        json.dump(out, f)
    return out


# ------------------------------------------------------------------------------------------ North Carolina
def ncsbe_summary(path):
    """one State Board results_pct file: contest name -> {counties, vote_for values, choices' votes, precincts};
    the columns by the file's own header (county, contest_name or contest, choice or name_on_ballot, vote_for,
    total_votes or total_vote_count or ballot_count; pipeline/intake/ncsbe.py names the layouts)"""
    os.makedirs(DERIVED, exist_ok=True)
    out_path = os.path.join(DERIVED, os.path.basename(path) + ".json")
    if os.path.exists(out_path):
        with open(out_path) as f:
            return json.load(f)
    with zipfile.ZipFile(path) as z:
        names = [n for n in z.namelist() if not n.endswith("/")]
        raw = z.read(names[0])
    text = raw.decode("utf-8-sig", errors="replace") if raw[:3] == b"\xef\xbb\xbf" else raw.decode("latin-1")
    first = text.split("\n", 1)[0]
    delim = "\t" if first.count("\t") > first.count(",") else ","
    rd = csv.reader(io.StringIO(text), delimiter=delim)
    row1 = next(rd)
    head = None
    pending = []
    if row1 and row1[0].strip().lower().startswith("county"):
        head = [re.sub(r"[^a-z0-9]+", "_", h.strip().lower()).strip("_") for h in row1]
    else:
        x = [v.strip() for v in row1]
        if len(x) >= 10 and all(re.match(r"^\d+$", v) for v in x[6:10]):
            head = ["county", "election_dt", "precinct", "contest", "name_on_ballot", "party_cd", "election_day_count",
                    "absentee_count", "provisional_count", "total_vote_count"]
        else:
            head = ["county", "election_dt", "precinct_abbrv", "precinct", "contest_name", "name_on_ballot", "party_cd",
                    "ballot_count", "ftp_date"]
        pending = [row1]
    con = {}
    n = 0
    for row in pending + list(rd):
        if not row or all(not v.strip() for v in row):
            continue
        r = dict(zip(head, (v.strip() for v in row)))
        n += 1
        name = re.sub(r"\s+", " ", r.get("contest_name") or r.get("contest") or "").strip()
        choice = r.get("choice") or r.get("name_on_ballot") or ""
        v = (r.get("total_votes") or r.get("total_vote_count") or r.get("ballot_count") or "").replace(",", "")
        votes = int(float(v)) if re.match(r"^-?\d+(\.\d+)?$", v) else None
        if not name or not choice or votes is None:
            continue
        c = con.setdefault(name, {"counties": set(), "vote_for": set(), "choices": collections.Counter(), "precincts": set()})
        c["counties"].add((r.get("county") or "").upper())
        c["vote_for"].add((r.get("vote_for") or "").strip())
        c["choices"][choice.upper()] += votes
        c["precincts"].add(((r.get("county") or "").upper(), r.get("precinct") or r.get("precinct_abbrv") or ""))
    out = {"file": os.path.basename(path), "sha256": L.sha256(path), "rows": n, "columns": head,
           "contests": {k: {"counties": sorted(v["counties"]), "n_counties": len(v["counties"]),
                            "vote_for": sorted(v["vote_for"]), "choices": dict(v["choices"]),
                            "precincts": len(v["precincts"])} for k, v in con.items()}}
    with open(out_path, "w") as f:
        json.dump(out, f)
    return out


def hash_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ------------------------------------------------------------------------------------------ the seventh pass: volume
# The offices whose totals a second count exists for (D1's presidency, D2's Senate, House and governors, Klarner's
# legislatures), by one spelling each; MEDSL's 2018-2024 files name them so already, 2016's in title case.
VOLUME_OFFICES = {"US PRESIDENT": "PRESIDENT", "PRESIDENT": "PRESIDENT", "PRESIDENT AND VICE PRESIDENT": "PRESIDENT",
                  "US SENATE": "US SENATE", "US SENATOR": "US SENATE", "UNITED STATES SENATOR": "US SENATE",
                  "US HOUSE": "US HOUSE", "US REPRESENTATIVE": "US HOUSE", "UNITED STATES REPRESENTATIVE": "US HOUSE",
                  "GOVERNOR": "GOVERNOR", "GOVERNOR AND LIEUTENANT GOVERNOR": "GOVERNOR", "GOVERNOR AND LT GOVERNOR": "GOVERNOR",
                  "STATE SENATE": "STATE SENATE", "STATE SENATOR": "STATE SENATE",
                  "STATE HOUSE": "STATE HOUSE", "STATE REPRESENTATIVE": "STATE HOUSE", "STATE ASSEMBLY": "STATE HOUSE",
                  "HOUSE OF DELEGATES": "STATE HOUSE", "GENERAL ASSEMBLY": "STATE HOUSE"}
_TOTAL_ROW = re.compile(r"\bTOTAL\b|^-1$|^ALL$")


def _near(a, b, tol, slack=10):
    """within tol of b, or within slack votes where b is at least 50 (a small place's provisional line can be filed
    under the municipality); a row of a few votes beside rows of none is no subtotal"""
    return a == b or abs(a - b) <= max(tol * b, slack if b >= 50 else 0)


def _subtotal_rows(resolved):
    """the precinct keys that are subtotals of other rows in their county (see volume_summary): a row named as a total
    whose votes equal the county's other rows (not named as totals) added up, or a row whose name the county's other
    rows extend (name + ' ' or '-', not themselves named as totals) and whose votes equal those rows added up"""
    by_county = collections.defaultdict(list)
    for pk, rv in resolved.items():
        by_county[pk[0]].append(pk)
    subs = set()

    def equal(rv, rows):
        if not rows or not rv:
            return False
        s = collections.Counter()
        for q in rows:
            s.update(resolved[q])
        if not _near(sum(rv.values()), sum(s.values()), 0.005):
            return False
        lead = max(rv, key=rv.get)
        return _near(rv[lead], s.get(lead, 0), 0.01) and rv[lead] > 0

    for county, pks in by_county.items():
        named = [pk for pk in pks if _TOTAL_ROW.search((pk[2] or "").upper())]
        plain = [pk for pk in pks if pk not in named]
        for t in named:
            if equal(resolved[t], plain):
                subs.add(t)
        by_name = collections.defaultdict(list)
        for pk in plain:
            by_name[(pk[2] or "").strip().upper()].append(pk)
        # each row's parent is the longest other name its own name extends; a row that is itself a parent is no child
        parent_of = {}
        for nm in by_name:
            for i in range(len(nm) - 1, 0, -1):
                if nm[i] in " -" and nm[:i] in by_name:
                    parent_of[nm] = nm[:i]
                    break
        parents = set(parent_of.values())
        kids = collections.defaultdict(list)
        for nm, par in parent_of.items():
            if nm not in parents:
                kids[par].extend(by_name[nm])
        for nm in parents:
            if nm and kids.get(nm):
                for pk in by_name[nm]:
                    if equal(resolved[pk], kids[nm]):
                        subs.add(pk)
    return subs


def volume_summary(path, year):
    """the seventh pass's summary of one raw MEDSL file, made once into derived/<file>.volume.json: for every contest
    of the offices in VOLUME_OFFICES (any dataverse, any stage marked GEN or unmarked), "ST|date|office|district" ->
      cands      candidate -> votes over every row (a precinct's TOTAL row where it has one, else its modes summed);
      no_total   the same with the rows whose precinct is named as a total (TOTAL, -1, ALL) left out;
      no_sub     the same with the rows that are subtotals of other rows left out (the seventh pass's rule, made apart
                 from the pipeline's: a row named as a total whose votes equal the county's other rows added up, or a
                 row whose name the county's other rows extend ("Allendale" beside "Allendale 1", "Allendale 2",
                 "Allendale Provisional": New Jersey 2024's Bergen county; a row's parent is the longest other name
                 its own extends, and a row that is itself a parent is nobody's child) and whose votes equal those
                 rows added up; equal = the contest's votes within 0.5% or 10 votes and the leading candidate's within
                 1% or 10 votes);
      counties   county FIPS -> votes over every row;
      total_rows votes on the rows left out of no_total; sub_rows votes on the rows left out of no_sub; subtotals
                 the names of up to twelve rows left out of no_sub;
      precincts  the precinct keys with a positive vote; magnitudes; rows;
      party      candidate -> party (party_simplified, else party_detailed; 2016's party), the first seen.
    The stage: 2018-2024 files mark it (GEN); 2016's state file holds the general only. A row marked special (a special
    Senate race beside the regular one) goes under the district with ' SPECIAL' added."""
    os.makedirs(DERIVED, exist_ok=True)
    out_path = os.path.join(DERIVED, os.path.basename(path) + ".volume.json")
    if os.path.exists(out_path):
        with open(out_path) as f:
            return json.load(f)
    sha = L.sha256(path)
    cells = {}       # key -> {pk: {cand: {mode: votes}}}
    mags = collections.defaultdict(set)
    nrows = collections.Counter()
    party = {}       # key -> {cand: party_simplified (else party_detailed), the first seen}
    n = 0
    for r in rows(path):
        n += 1
        office = VOLUME_OFFICES.get(office_key(r.get("office")))
        if not office:
            continue
        stage = (r.get("stage") or "GEN").upper()
        if stage != "GEN":
            continue
        if year == 2016:
            st = r.get("state_postal", "")
            date = "2016-11-08"
            pk = (fips5(r.get("county_fips", "")), r.get("jurisdiction", ""), r.get("precinct", ""))
        else:
            st = r.get("state_po", "")
            date = r.get("date", "")
            pk = (fips5(r.get("county_fips", "")), r.get("jurisdiction_fips", ""), r.get("precinct", ""))
        cand = (r.get("candidate") or "").strip()
        if is_meta(cand):
            continue
        try:
            votes = int(float(r.get("votes") or ""))
        except ValueError:
            votes = None
        mode = (r.get("mode") or "TOTAL").upper()
        district = (r.get("district") or "").strip()
        if (r.get("special") or "").strip().upper() in ("TRUE", "T", "1", "YES"):
            district += " SPECIAL"   # a special Senate race beside the regular one (GA 2020, MS 2018): kept apart
        key = (st, date, office, district)
        cell = cells.setdefault(key, {}).setdefault(pk, {}).setdefault(cand.upper(), {})
        cell[mode] = None if votes is None or cell.get(mode, 0) is None else cell.get(mode, 0) + votes
        mags[key].add((r.get("magnitude") or "").strip())
        nrows[key] += 1
        party.setdefault(key, {}).setdefault(cand.upper(), ((r.get("party_simplified") or r.get("party_detailed") or r.get("party") or "").strip().upper()))
    out_c = {}
    for key, precincts in cells.items():
        cands, no_total, no_sub, counties = collections.Counter(), collections.Counter(), collections.Counter(), collections.Counter()
        total_rows = sub_rows = 0
        voted = set()
        resolved = {}    # pk -> {cand: votes}
        for pk, cs in precincts.items():
            rv = {}
            for c, modes in cs.items():
                v = _resolve(modes)
                if v is not None:
                    rv[c] = v
            resolved[pk] = rv
        subs = _subtotal_rows(resolved)
        for pk, rv in resolved.items():
            is_total = bool(_TOTAL_ROW.search((pk[2] or "").upper()))
            for c, v in rv.items():
                cands[c] += v
                counties[pk[0]] += v
                if is_total:
                    total_rows += v
                else:
                    no_total[c] += v
                if pk in subs:
                    sub_rows += v
                else:
                    no_sub[c] += v
                if v > 0:
                    voted.add(pk)
        out_c["|".join(key)] = {"cands": dict(cands), "no_total": dict(no_total), "no_sub": dict(no_sub), "counties": dict(counties),
                                "total_rows": total_rows, "sub_rows": sub_rows, "subtotals": sorted(pk[2] for pk in subs)[:12],
                                "precincts": len(voted), "magnitudes": sorted(mags[key]),
                                "rows": nrows[key], "party": party.get(key, {})}
    out = {"file": os.path.basename(path), "sha256": sha, "rows": n, "year": year, "contests": out_c}
    with open(out_path, "w") as f:
        json.dump(out, f)
    return out


def all_raw_files():
    """every raw MEDSL file in the caches, (year, path): fifth/medsl and fourth/medsl by name"""
    out = []
    for d in (os.path.join(FIFTH, "medsl"), os.path.join(L.CACHE, "fourth", "medsl")):
        if not os.path.isdir(d):
            continue
        for n in sorted(os.listdir(d)):
            if not n.lower().endswith((".csv", ".zip", ".tab")):
                continue
            m = re.match(r"^(20\d\d)", n)
            year = int(m.group(1)) if m else (2022 if re.search(r"22|cleaned|final|colorado|louisiana|carolina", n) else None)
            if year:
                out.append((year, os.path.join(d, n)))
    return out


# ------------------------------------------------------------------------------------------ the eighth pass
BALLOT_LINE = re.compile(r"^(CONTEST TOTAL|BALLOTS CAST|TOTAL BALLOTS( CAST)?|VOTES CAST|TOTAL VOTES CAST|CAST VOTES|BALLOTS)$")
OVER_LINE = re.compile(r"^(OVER ?VOTES?|TIMES OVER VOTED)$")
UNDER_LINE = re.compile(r"^(UNDER ?VOTES?|TIMES UNDER VOTED|BLANK VOTES?|BLANKS?|TIMES BLANK VOTED)$")
STATEWIDE_DISTRICTS = {"", "STATEWIDE", "STATE", "AT LARGE", "AT-LARGE", "ATLARGE", "ALL", "0", "000", "NA", "N/A", "NONE", "STATE WIDE"}


def ballots_summary(path, year):
    """the eighth pass's summary of one raw MEDSL file, made once into derived/<file>.ballots.json, for an over-ballot
    test written apart from pipeline/local_medsl.py over_ballot: every statewide contest of the STATE, PRESIDENT and
    SENATE dataverses (stage GEN or unmarked): a district in STATEWIDE_DISTRICTS, or an office and district whose rows
    span at least half the counties those dataverses' rows span in the file (a seat-numbered statewide court, read in a
    first pass over the file), "ST|date|dataverse|office|district" ->
      cands        candidate -> votes (a precinct's TOTAL row where it has one, else its modes summed), with the rows
                   that are subtotals of other rows left out (the seventh pass's rule, _subtotal_rows); cands_all the
                   same with every row;
      answers      True where every name is a ballot answer (a question);
      magnitudes, precincts (keys with a row), rows;
      ballots      the ballots cast in the contest's precincts as the file gives them: per precinct, a line named as
                   the ballots cast or the contest's total (BALLOT_LINE), else the candidates' votes plus the overvote
                   and undervote lines where the precinct has both; summed over the precincts that have a figure
                   (sum), with their count (with_figure) and the kinds of figure seen.
    A row marked special goes under the district with ' SPECIAL' added, as in volume_summary."""
    os.makedirs(DERIVED, exist_ok=True)
    out_path = os.path.join(DERIVED, os.path.basename(path) + ".ballots.json")
    if os.path.exists(out_path):
        with open(out_path) as f:
            return json.load(f)
    sha = L.sha256(path)
    # the first pass: the counties each (dataverse, office, district) spans
    span = collections.defaultdict(set)
    all_counties = set()
    for r in rows(path):
        dv = (r.get("dataverse") or "").strip().upper()
        if dv not in ("STATE", "PRESIDENT", "SENATE") or (r.get("stage") or "GEN").upper() != "GEN":
            continue
        county = fips5(r.get("county_fips", ""))
        all_counties.add(county)
        span[(dv, (r.get("office") or "").strip().upper(), (r.get("district") or "").strip().upper())].add(county)
    wide = {k for k, cs in span.items() if k[2] in STATEWIDE_DISTRICTS or (all_counties and len(cs) >= 0.5 * len(all_counties))}
    cells = {}       # key -> {pk: {cand: {mode: votes}}}  (candidates)
    meta = {}        # key -> {pk: {kind: {mode: votes}}}   (ballot, over, under lines)
    mags = collections.defaultdict(set)
    nrows = collections.Counter()
    n = 0
    for r in rows(path):
        n += 1
        stage = (r.get("stage") or "GEN").upper()
        if stage != "GEN":
            continue
        dv = (r.get("dataverse") or "").strip().upper()
        district = (r.get("district") or "").strip().upper()
        if (dv, (r.get("office") or "").strip().upper(), district) not in wide:
            continue
        if year == 2016:
            st = r.get("state_postal", "")
            date = "2016-11-08"
            pk = (fips5(r.get("county_fips", "")), r.get("jurisdiction", ""), r.get("precinct", ""))
        else:
            st = r.get("state_po", "")
            date = r.get("date", "")
            pk = (fips5(r.get("county_fips", "")), r.get("jurisdiction_fips", ""), r.get("precinct", ""))
        office = (r.get("office") or "").strip().upper()
        if not office:
            continue
        if (r.get("special") or "").strip().upper() in ("TRUE", "T", "1", "YES"):
            district += " SPECIAL"
        key = (st, date, dv, office, district)
        cand = (r.get("candidate") or "").strip().upper()
        try:
            votes = int(float(r.get("votes") or ""))
        except ValueError:
            votes = None
        mode = (r.get("mode") or "TOTAL").upper()
        kind = None
        if BALLOT_LINE.match(cand):
            kind = "ballots"
        elif OVER_LINE.match(cand):
            kind = "over"
        elif UNDER_LINE.match(cand):
            kind = "under"
        if kind:
            cell = meta.setdefault(key, {}).setdefault(pk, {}).setdefault(kind, {})
        elif is_meta(cand):
            continue
        else:
            cell = cells.setdefault(key, {}).setdefault(pk, {}).setdefault(cand, {})
        cell[mode] = None if votes is None or cell.get(mode, 0) is None else cell.get(mode, 0) + votes
        mags[key].add((r.get("magnitude") or "").strip())
        nrows[key] += 1
    out_c = {}
    for key, precincts in cells.items():
        resolved = {}
        for pk, cs in precincts.items():
            rv = {}
            for c, modes in cs.items():
                v = _resolve(modes)
                if v is not None:
                    rv[c] = v
            resolved[pk] = rv
        subs = _subtotal_rows(resolved)
        cands, cands_all = collections.Counter(), collections.Counter()
        b_sum, with_fig, kinds = 0, 0, collections.Counter()
        for pk, rv in resolved.items():
            for c, v in rv.items():
                cands_all[c] += v
                if pk not in subs:
                    cands[c] += v
            if pk in subs:
                continue
            m = {k: _resolve(mm) for k, mm in meta.get(key, {}).get(pk, {}).items()}
            fig = None
            if m.get("ballots") is not None:
                fig, k_ = m["ballots"], "ballots line"
            elif m.get("over") is not None and m.get("under") is not None:
                fig, k_ = sum(rv.values()) + m["over"] + m["under"], "votes + over + under"
            if fig is not None:
                b_sum += fig
                with_fig += 1
                kinds[k_] += 1
        names = [c for c in cands_all if c]
        out_c["|".join(key)] = {"cands": dict(cands), "cands_all": dict(cands_all), "answers": bool(names) and all(answer_of(c) for c in names),
                                "magnitudes": sorted(mags[key]), "precincts": len(resolved), "subtotal_rows": len(subs), "rows": nrows[key],
                                "ballots": {"sum": b_sum, "with_figure": with_fig, "kinds": dict(kinds)}}
    out = {"file": os.path.basename(path), "sha256": sha, "rows": n, "year": year, "counties_all": len(all_counties),
           "contests": out_c, "spans": {"|".join(k): len(span[k]) for k in wide}}
    with open(out_path, "w") as f:
        json.dump(out, f)
    return out
