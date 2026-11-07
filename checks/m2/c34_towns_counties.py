"""c34: D3's #86 (e524840): towns and townships counted whole by the Census Bureau's 2020 county subdivision file,
counties' own questions counted whole where they cover the county's whole file, and M2's three readings as fixed.

The orchestrator (2026-11-07 16:53 UTC): "#86: towns and townships against the cousub file (active governments, the
name-clash guard); counties' own questions against your own precinct coverage; the 20 partial ones; M2's three
readings as fixed (the 866 wording, the 26 superintendents, the whole-vote test giving 25)."

What this does (every figure [measured] unless marked):
  34.1 the moves file (data/measure/moves-towns-counties.json) against my own diff of every measure, local and
       primary file between bdac161 (before: main with M2's #69) and e524840 (after): the records that changed, what
       changed in each, its code; the p values (none moved, D3 says); the other files that changed.
  34.2 the 165 towns and townships against my own reading of national_cousub2020.txt: an active government (FUNCSTAT
       A) in the record's county, the only subdivision of that name there, the Census's name; the name-clash guard (a
       name that is also an active incorporated place's in the county is held unless the title says the kind); and
       each title read again apart from the pipeline's rules.
  34.3 every one-county question matched again by a copy of pipeline/places.py's new rule (checks/m2/m2places.py,
       which says it is a copy; D3's table of REPORT §23 reproduced row by row); then each county's own question's
       precincts and its county's precincts counted by me from MEDSL's own files (checks/m2/m2medsl.py), for the 134
       counted whole and the 20 held as covering part of the county.
  34.4 the three readings: data/local/moves-fixes-c24.json's 854 rows now coded 'C' (p before equal to p after) and
       its 866 'P'; the 26 state superintendents against c29's own reading; the vote test counted in whole votes on
       North Carolina's other-dates pool (25 within 10 votes, 23 in the share form).
Nothing from pipeline/ is imported.
"""
import collections
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402
import m2medsl as M  # noqa: E402
import m2places as P  # noqa: E402
import c27_local_thresholds as C27  # noqa: E402
import c31_statewide_filed_local as C31  # noqa: E402
import c33_one_county as C33  # noqa: E402

BEFORE = "bdac161"   # main with #69 (M2's third pass)
AFTER = "e524840"    # #86 merged
MOVES = "data/measure/moves-towns-counties.json"
FIXES = "data/local/moves-fixes-c24.json"
LEVELS = ("measure", "local", "primary")


def show(commit, path):
    r = subprocess.run(["git", "show", f"{commit}:{path}"], capture_output=True, text=True, cwd=L.ROOT)
    return json.loads(r.stdout) if r.returncode == 0 and r.stdout else None


def record_files(commit, levels=LEVELS):
    r = subprocess.run(["git", "ls-tree", "-r", "--name-only", commit, "data/"], capture_output=True, text=True, cwd=L.ROOT)
    return sorted(x for x in r.stdout.split("\n") if re.search(r"data/(" + "|".join(levels) + r")/\d{4}/[A-Z]{2}\.json$", x))


def pval(c):
    p = c.get("p") or {}
    return p.get("value") if "value" in p else p.get("not_computed")


# ---------------------------------------------------------------------------------------------- 34.1
def my_codes(b, a, paths):
    """the moves file's codes, derived from the two records: W counted whole now, U place_whole gained its unit only,
    R the reason's words changed (no p before or after), Q a note's words changed, B the p block changed only in its
    note, T the type changed"""
    codes = set()
    pb, pa = b.get("p") or {}, a.get("p") or {}
    if b.get("office_type") != a.get("office_type"):
        codes.add("T")
    if a.get("place_whole") and not b.get("place_whole"):
        codes.add("W")
    elif a.get("place_whole") and b.get("place_whole") and set(paths) <= {"place_whole.unit", "p.commit"}:
        codes.add("U")
    if "not_computed" in pa and "not_computed" in pb and pa["not_computed"] != pb["not_computed"]:
        codes.add("R")
    if b.get("notes") != a.get("notes") or pb.get("note") != pa.get("note"):
        codes.add("Q")
    if "value" in pa and "value" in pb and pa["value"] == pb["value"] and {k for k in set(pa) | set(pb) if pa.get(k) != pb.get(k)} - {"note"}:
        codes.add("B")   # D3's B is on the blocks whose own commit stamp moved with the note (its code's words say "only in its note")
    return codes


def section_1():
    print("### 34.1 the moves file against my own diff of the records, bdac161 to e524840")
    allf = C31.changed_files(BEFORE, AFTER, under=".")
    recf = [x for x in allf if re.search(r"data/(measure|local|primary)/\d{4}/[A-Z]{2}\.json$", x)]
    print(f"  files changed: {len(allf)}; record files {len(recf)} ({dict(collections.Counter(x.split('/')[1] for x in recf))}); others: "
          + ", ".join(x for x in allf if x not in recf))
    before, after = C31.load_records(BEFORE, recf), C31.load_records(AFTER, recf)
    changed = {cid: C31.deep_paths(before[cid], after[cid]) for cid in set(before) & set(after) if before[cid] != after[cid]}
    stamps = {cid for cid, v in changed.items() if v == ["p.commit"]}
    print(f"  records new {len(set(after) - set(before))}, gone {len(set(before) - set(after))}, changed {len(changed)} (p.commit stamp alone {len(stamps)})")
    top = collections.Counter(tuple(sorted({x.split('.')[0] for x in v})) for cid, v in changed.items() if cid not in stamps)
    for paths, n in top.most_common():
        print(f"    {n:5d}  {', '.join(paths)}")
    moved = [cid for cid in changed if "value" in (after[cid].get("p") or {}) and "value" in (before[cid].get("p") or {})
             and after[cid]["p"]["value"] != before[cid]["p"]["value"]]
    became = [cid for cid in changed if ("value" in (after[cid].get("p") or {})) != ("value" in (before[cid].get("p") or {}))]
    print(f"  p values that moved: {len(moved)}; p that became computed or uncomputed: {len(became)} (D3: none)")
    mv = show(AFTER, MOVES)
    recs = {r[0]: r for r in mv["records"]}
    mine = set(changed) - stamps
    print(f"  the moves file: {len(recs)} records (against {mv.get('against')}); codes {mv['codes'].keys() and sorted(mv['codes'])}; summary {mv['summary']}")
    print(f"  its ids == my changed ids less the stamps: {set(recs) == mine}" + ("" if set(recs) == mine else
          f" (mine not listed {sorted(mine - set(recs))[:5]}, listed not mine {sorted(set(recs) - mine)[:5]})"))
    tal = collections.Counter()
    bycode = collections.Counter()
    pdiff = collections.Counter()
    for cid, r in recs.items():
        b, a = before.get(cid), after.get(cid)
        if b is None or a is None:
            tal["not in both commits"] += 1
            continue
        codes = my_codes(b, a, changed.get(cid, []))
        if "Q" in r[8] and "value" in (a.get("p") or {}):
            pa_, pb_ = a.get("p") or {}, b.get("p") or {}
            pdiff[(",".join(sorted(r[8])), ",".join(sorted(k for k in set(pa_) | set(pb_) if pa_.get(k) != pb_.get(k))))] += 1
        file_codes = set(r[8])
        same = (codes == file_codes, r[3] == b.get("office_type"), r[4] == a.get("office_type"), r[5] == pval(b), r[6] == pval(a))
        tal["codes, types and p before and after all as the records" if all(same) else f"DIFFERS {same}"] += 1
        if not all(same):
            print(f"    {cid[:70]}: file {sorted(file_codes)} mine {sorted(codes)} | {same}")
        bycode[(cid.split("-")[1], ",".join(sorted(file_codes)))] += 1
    print(f"  the records against the moves file: {dict(tal)}")
    print(f"  the noted p blocks (code, what differs in the p block): {dict(pdiff)} (D3's B where the block's own commit stamp moved with the note; "
          "Q alone where the note alone; the code's words, 'its block changed only in its note', fit the Q rows better: a reading)")
    units = collections.Counter()
    for cid, r in recs.items():
        if "W" in r[8]:
            pw = after[cid]["place_whole"]
            units[f"W: counted whole, the {pw['unit']} [{pw['mark']}]"] += 1
    print(f"  the W rows by unit and mark: {dict(units)} (D3: county subdivision 136 stated, 29 inferred; county 8 stated, 126 inferred)")
    print(f"  rows by level and code: {dict(sorted(bycode.items()))}")
    return before, after, mv


# ---------------------------------------------------------------------------------------------- 34.2
SUB_KINDS_RE = re.compile(r"^(.*?) (charter township|township|town|plantation|borough|city|village|gore|grant|location|"
                          r"purchase|reservation|unorganized territory)$")
_SUB_BODY = re.compile(r"\b(SCHOOLS?|DISTRICT|DIST|USD|ISD|CISD|ESD|HSD|UHSD|BOE|UNIFIED|COLLEGE|COUNTY|PARISH|CITY|VILLAGE|BOROUGH|"
                       r"FIRE|HOSPITAL|LIBRARY|PORT|TRANSIT|WATER|SEWER|SANITARY|SANITATION|IRRIGATION|CEMETERY|AUTHORITY|AREA|"
                       r"REGIONAL|JOINT|CONSOLIDATED|PARK|RECREATION|UTILITY|UTILITIES|AMBULANCE|EMS|DRAINAGE|LEVEE|CONSERVANCY|"
                       r"AIRPORT|HEALTH|MOSQUITO)\b")


def read_cousub():
    """my own reading of national_cousub2020.txt: every row by its ten-digit geoid, and the active ones by state and
    base name"""
    by_geoid = {}
    active = collections.defaultdict(list)
    stats = collections.Counter()
    with open(os.path.join(P.FOURTH, "census_cousub.txt"), encoding="utf-8") as f:
        head = f.readline().rstrip("\n").split("|")
        for line in f:
            st, sfp, cfp, cname, cofp, ns, sname, cls, fs = line.rstrip("\n").split("|")
            stats["rows"] += 1
            stats[f"FUNCSTAT {fs}"] += 1
            m = SUB_KINDS_RE.match(sname)
            base, kind = (m.group(1), m.group(2)) if m else (sname, "")
            row = dict(st=st, county=sfp + cfp, county_name=cname, name=sname, base=C33.plain(base), kind=kind.upper(),
                       classfp=cls, funcstat=fs, geoid=sfp + cfp + cofp)
            by_geoid[row["geoid"]] = row
            if fs == "A":
                active[(st, row["base"])].append(row)
    return by_geoid, active, stats, head


def sub_reading(title, st, county, pw, by_geoid, active, places):
    t = P._OREGON_NO.sub("", C33.plain(title))
    row = by_geoid.get(pw["geoid"])
    m = SUB_KINDS_RE.match(pw["place"])
    base = C33.plain(m.group(1) if m else pw["place"])
    kind = (m.group(2) if m else "").upper()
    tests = collections.OrderedDict()
    tests["Census: the geoid is one row, FUNCSTAT A, in the record's county, named as the record says"] = bool(
        row and row["funcstat"] == "A" and row["county"] == county == pw["county"] and row["name"] == pw["place"])
    tests["Census: the only active subdivision of that base name in the county"] = sum(
        1 for r in active.get((st, base), []) if r["county"] == county) == 1
    stated = re.search(r"\b(TOWN|TOWNSHIP|CHARTER TOWNSHIP|PLANTATION) OF " + re.escape(base) + r"(\b|$)", t) or \
        re.match(r"^" + re.escape(base) + r" (TOWNSHIP|TWP|TOWN|CHARTER TOWNSHIP|PLANTATION)(\b|$)", t)
    begins = re.match(r"^" + re.escape(base) + r"(\b|$)", t)
    if pw["mark"] == "stated":
        tests["title: says the kind and the name ('TOWN OF X', 'TOWNSHIP OF X', 'X TOWNSHIP', 'X TWP', 'X TOWN')"] = bool(stated)
        said = (stated.group(1) if stated and stated.lastindex and stated.group(1) in ("TOWN", "TOWNSHIP", "CHARTER TOWNSHIP", "PLANTATION")
                else (stated.group(1) if stated else ""))
        said = "TOWNSHIP" if said == "TWP" else said
        tests["title: the kind it says is the Census's kind"] = (said == kind) or (said == "TOWNSHIP" and kind == "CHARTER TOWNSHIP")
    else:
        tests["title: begins with the subdivision's name"] = bool(begins)
        clash = [v for (pn, k), v in places.get(st, {}).items() if pn == base and county in v["counties"] and v["census_name"] != pw["place"]]
        tests["name clash: no active incorporated place of the same name in the county (the title does not say which)"] = not clash
    tests["title: no district, school, county or special-body word"] = not _SUB_BODY.search(re.sub(r"\b(TOWN|TOWNSHIP|CHARTER TOWNSHIP|PLANTATION) OF\b|\b(TOWNSHIP|TWP|TOWN)\b", " ", t))
    return tests


def section_2(after):
    print("### 34.2 the 165 towns and townships against my own reading of the county subdivision file")
    h = L.sha256(os.path.join(P.FOURTH, "census_cousub.txt"))
    src = None
    for f in C31.record_files(AFTER):
        s = (show(AFTER, f) or {}).get("sources") or {}
        if "census_cousub" in s:
            src = s["census_cousub"]
            break
    print(f"  census_cousub.txt sha256 {h[:16]}... equals the record's source block: {h == (src or {}).get('sha256')} (read {(src or {}).get('read_utc')})")
    by_geoid, active, stats, head = read_cousub()
    print(f"  columns {head}; {dict(stats)}")
    places, _, _, _, _, _, _ = C33.read_census()
    subs = {cid: c for cid, c in after.items() if (c.get("place_whole") or {}).get("unit") == "county subdivision"}
    print(f"  records whose unit is a county subdivision at e524840: {len(subs)} (D3: 165: 136 stated, 29 inferred); by mark "
          f"{dict(collections.Counter(c['place_whole']['mark'] for c in subs.values()))}; by state and year "
          f"{dict(sorted(collections.Counter((c['place']['state'], c['year']) for c in subs.values()).items()))}")
    res = collections.defaultdict(collections.Counter)
    fails = collections.defaultdict(list)
    kinds = collections.Counter()
    for cid, c in sorted(subs.items()):
        pw = c["place_whole"]
        st, county = c["place"]["state"], c["place"]["counties"][0]
        kinds[(pw["mark"], by_geoid.get(pw["geoid"], {}).get("kind"))] += 1
        for k, v in sub_reading(c["question"]["title"], st, county, pw, by_geoid, active, places).items():
            res[pw["mark"]][k] += int(v)
            if not v:
                fails[(pw["mark"], k)].append((st, c["question"]["title"], pw["place"]))
    print(f"  the Census's kinds of the subdivisions, by mark: {dict(sorted(kinds.items()))}")
    for mark in ("stated", "inferred"):
        n = sum(1 for c in subs.values() if c["place_whole"]["mark"] == mark)
        print(f"    [{mark}] {n} questions:")
        for k, v in res[mark].items():
            print(f"      {v:4d} of {n}  {k}")
    for (mark, k), items in sorted(fails.items()):
        print(f"    [{mark}] fails '{k}' ({len(items)}):")
        for st, title, place in items[:12]:
            print(f"      {st}: {title[:70]!r} -> {place}")
    inferred = [(c["place"]["state"], c["year"], c["question"]["title"], c["place_whole"]["place"], c["place_whole"]["county_name"])
                for c in subs.values() if c["place_whole"]["mark"] == "inferred"]
    print(f"  the {len(inferred)} inferred matches (state, year, title -> subdivision, county), for the eye:")
    for st, y, title, place, cname in sorted(inferred):
        print(f"    {st} {y}: {title[:72]} -> {place} ({cname})")
    # the name-clash guard the other way: the held questions whose reason is the clash
    return by_geoid, active, places


# ---------------------------------------------------------------------------------------------- 34.3
D3_TABLE = [("counted whole, the place [stated]", 442), ("counted whole, the place [inferred]", 280),
            ("counted whole, the county subdivision [stated]", 136), ("counted whole, the county subdivision [inferred]", 29),
            ("counted whole, the county [stated]", 8), ("counted whole, the county [inferred]", 126),
            ("held: the title names no incorporated place or county subdivision", 1177), ("held: a retention", 880),
            ("held: the title names a district or a school", 620),
            ("held: 'Township' naming no subdivision with a government of its own", 54),
            ("held: a county or parish, but not the record's", 50), ("held: the place lies in 2 or 3 counties", 50),
            ("held: another body's word in a county's question", 45), ("held: a county of the same name is the record's", 21),
            ("held: the county's own question covers fewer than all its precincts", 20), ("held: a special body after the name", 11),
            ("held: a place or town of the county also named", 8),
            ("held: the name is both a place's and a town's or township's in the county", 5),
            ("held: something in parentheses after the county", 4), ("held: a part of the county", 2),
            ("held: a hyphen join, a name that goes on, or another county", 4)]


def d3_label(found, why):
    if found:
        return f"counted whole, the {found['unit']} [{found['mark']}]"
    w = why
    if w.startswith("the title names no incorporated place or county subdivision"):
        return "held: the title names no incorporated place or county subdivision"
    if w.startswith("the title names no county subdivision"):
        return "held: 'Township' naming no subdivision with a government of its own"
    if w == "a retention":
        return "held: a retention"
    if w.startswith("the title names a district"):
        return "held: the title names a district or a school"
    if w.startswith("the title names a county or parish, but not"):
        return "held: a county or parish, but not the record's"
    if w.startswith("the place lies in") and "counties" in w:
        return "held: the place lies in 2 or 3 counties"
    if w.startswith("the title names another body"):
        return "held: another body's word in a county's question"
    if w.startswith("a county of the same name"):
        return "held: a county of the same name is the record's"
    if w.startswith("partial"):
        return "held: the county's own question covers fewer than all its precincts"
    if w == "not counted by me":
        return "held by D3; not counted by me (its file not fetched or the question not found)"
    if w.startswith("the title names a special body"):
        return "held: a special body after the name"
    if w.startswith("the title names a place or town"):
        return "held: a place or town of the county also named"
    if w.startswith("the name is both") or w.startswith("the name is also"):
        return "held: the name is both a place's and a town's or township's in the county"
    if w.startswith("the title names something in parentheses"):
        return "held: something in parentheses after the county"
    if w.startswith("the title names a part"):
        return "held: a part of the county"
    return "held: a hyphen join, a name that goes on, or another county"


def one_county_questions(commit):
    recs = C31.load_records(commit, C31.record_files(commit))
    mine = [c for c in recs.values() if c.get("question") and (c.get("result") or {}).get("source") == "medsl" and c["question"].get("scope") == "local"]
    where = collections.defaultdict(set)
    key = lambda c: (c["place"]["state"], c["question"]["title"].upper(), (c["question"].get("subject") or "").upper(), c.get("date"))  # noqa: E731
    for c in mine:
        where[key(c)].update(c["place"].get("counties") or [])
    return recs, mine, [c for c in mine if len(where[key(c)]) == 1]


def coverage(c, summaries):
    """(the question's precincts, the county's precincts in the file on the date) from my own summary of MEDSL's file;
    None where the file is not fetched or the question is not found in it"""
    st, year, date = c["place"]["state"], c["year"], c.get("date")
    county = c["place"]["counties"][0]
    paths = M.medsl_files(year, st)
    if not paths:
        return None, None, "the file is not fetched"
    office = M.office_key(c["question"]["title"])
    plain = office.split("|")[0].strip()   # 2016's titles carry '|<county>' after the question (MEDSL's own office text, or the pipeline's)
    n_c = None
    for path in paths:   # 2016: the local set, then the state set; the county's count is the file's own (as the pipeline keys it)
        if path not in summaries:
            summaries[path] = M.summary(path, year)
        s = summaries[path]
        hits = [v for k, v in s["questions"].items() if k.split("|")[:3] == [st, date, county]
                and (k.split("|")[3] == office or k.split("|")[3].split("|")[0].strip() == plain or "|".join(k.split("|")[3:-1]).strip() == office)]
        if not hits:
            if n_c is None:
                n_c = s["county_precincts"].get(f"{st}|{date}|{county}")
            continue
        n_q = max(h["all_keys"] if year == 2016 else h["precincts"] for h in hits)
        return n_q, s["county_precincts"].get(f"{st}|{date}|{county}"), f"{len(hits)} contest(s) of the title in the county ({os.path.basename(path)})"
    return None, n_c, "the question is not found in the file by its title and county"


def section_3(before, after):
    print("### 34.3 the one-county questions matched again by the new rule; the counties' own questions by my own precinct counts")
    recs_b, mine, one = one_county_questions(BEFORE)
    print(f"  local questions of MEDSL's at {BEFORE}: {len(mine)}; held in one county's file only: {len(one)} (D3: 3,972)")
    summaries = {}
    d3 = collections.Counter()
    whole = {}
    partial = []
    cov = collections.Counter()
    cov_detail = []
    for c in one:
        q = c["question"]
        if q.get("kind") == "retention":
            found, why = None, "a retention"
        elif len(c["place"].get("counties") or []) != 1:
            found, why = None, "the line names no county"
        else:
            found, why = P.match(q["title"], c["place"]["state"], c["place"]["counties"][0])
        if found and found["unit"] == "county":
            n_q, n_c, how = coverage(c, summaries)
            rec = (after.get(c["id"]) or {}).get("place_whole") or {}
            if n_q is None or n_c is None:
                cov[f"not counted by me: {how}"] += 1
                cov_detail.append((c["id"], how, rec.get("precincts"), rec.get("county_precincts")))
                found = {**found, "precincts": rec.get("precincts"), "county_precincts": rec.get("county_precincts"), "mine": None}
                if not rec:   # D3 held it; I cannot count it, so it goes under its own label, not D3's partial row
                    found, why = None, "not counted by me"
            elif n_q != n_c:
                partial.append((c["id"], n_q, n_c, rec))
                found, why = None, f"partial: {n_q} of {n_c}"
            else:
                found = {**found, "precincts": n_q, "county_precincts": n_c}
        d3[d3_label(found, why)] += 1
        if found:
            whole[c["id"]] = found
    rec_whole = {cid: c["place_whole"] for cid, c in after.items() if c.get("place_whole")}
    print(f"  counted whole by my run: {len(whole)} (D3: 1,021); records with place_whole at {AFTER}: {len(rec_whole)}; the same ids: {set(whole) == set(rec_whole)}"
          + ("" if set(whole) == set(rec_whole) else f" (mine only {sorted(set(whole) - set(rec_whole))[:4]}; record only {sorted(set(rec_whole) - set(whole))[:4]})"))
    eq = collections.Counter()
    for cid, f in whole.items():
        r = rec_whole.get(cid)
        if r is None:
            continue
        f2 = {k: v for k, v in f.items() if k != "mine"}
        if f2 == r:
            eq["place_whole equal (unit, place, geoid, county, county_name, how, mark; precincts and county_precincts for a county)"] += 1
        else:
            eq["DIFFERS: " + ", ".join(k for k in sorted(set(f2) | set(r)) if f2.get(k) != r.get(k))] += 1
    print(f"  the whole questions' place_whole against the records: {dict(eq)}")
    print("  the counts, mine | D3's table (REPORT section 23):")
    tot = 0
    for lab, n in D3_TABLE:
        print(f"    {d3.get(lab, 0):5d} | {n:5d}  {lab}")
        tot += d3.get(lab, 0)
    extra = {k: v for k, v in d3.items() if k not in dict(D3_TABLE)}
    print(f"    other labels of mine: {extra or 'none'}; my total over D3's rows {tot} (D3: 3,972)")
    new = {cid for cid in whole if not (before.get(cid) or {}).get("place_whole")}
    print(f"  newly whole (no place_whole at {BEFORE}): {len(new)} (D3: 299); by unit and mark "
          f"{dict(collections.Counter((whole[c]['unit'], whole[c]['mark']) for c in new))}")
    print(f"  by year, all whole: {dict(sorted(collections.Counter(int(cid[:4]) for cid in whole).items()))} (D3: 303, 123, 70, 6, 519)")
    # the counties' own questions: my counts against the records'
    print("  the counties' own questions, my precinct counts (from MEDSL's own files) against the records':")
    cnt = collections.Counter()
    for cid, f in whole.items():
        if f["unit"] != "county":
            continue
        r = rec_whole.get(cid) or {}
        if f.get("mine", 1) is None:
            cnt["not counted by me (file not fetched or question not found)"] += 1
        elif f["precincts"] == r.get("precincts") and f["county_precincts"] == r.get("county_precincts"):
            cnt["precincts and county_precincts equal to the record's, and equal to each other"] += 1
        else:
            cnt[f"DIFFERS: mine {f['precincts']}/{f['county_precincts']}, record {r.get('precincts')}/{r.get('county_precincts')}"] += 1
    print(f"    {dict(cnt)}")
    for cid, how, rp, rc in cov_detail:
        print(f"    not counted: {cid[:70]}: {how}; " + (f"the record says {rp} of {rc}" if rp is not None else "the record holds it (no place_whole)"))
    print(f"  files read: " + "; ".join(f"{os.path.basename(p)} ({s['rows']:,} rows, sha256 {s['sha256'][:12]})" for p, s in sorted(summaries.items())))
    print(f"  the county's own questions held as covering part of the county, by my counts: {len(partial)} (D3: 20)")
    for cid, n_q, n_c, rec in sorted(partial):
        print(f"    {cid[:78]}: {n_q} of {n_c}" + (f"; the record counts it whole ({rec})" if rec else ""))
    return whole


# ---------------------------------------------------------------------------------------------- 34.4
SUPT = re.compile(r"SUPERINTENDENT|\bSUPT\b|SUPER\. OF PUBLIC INSTRUCTION")
SCHOOL = re.compile(r"SCHOOL|EDUCATION|INSTRUCTION")


def section_4(before, after, mv):
    print("### 34.4 the three readings from c29 and c27, as fixed")
    fa, fb = show(AFTER, FIXES), show(BEFORE, FIXES)
    rows = fa["contests"]
    codes = collections.Counter(r[6] for r in rows)
    c_rows = [r for r in rows if r[6] == "C"]
    p_rows = [r for r in rows if r[6] == "P"]
    print(f"  (1) {FIXES}: codes now {dict(codes)} (before {dict(collections.Counter(r[6] for r in fb['contests']))}); 'C' rows with p before equal to p after: "
          f"{sum(1 for r in c_rows if r[4] == r[5])} of {len(c_rows)}; 'P' rows whose p moved: {sum(1 for r in p_rows if r[4] != r[5])} of {len(p_rows)} "
          f"(c29 found 866 moved of 1,720); the same ids as before: {set(r[0] for r in rows) == set(r[0] for r in fb['contests'])}")
    rep = subprocess.run(["git", "show", f"{AFTER}:data/local/REPORT.md"], capture_output=True, text=True, cwd=L.ROOT).stdout
    print(f"  REPORT section 15 now says '866 other p move': {'866 other p move' in rep}; its correction names c29 §29.1: {'c29 §29.1' in rep}")
    # (2) the state superintendents
    found = {cid: c for cid, c in after.items() if cid.split("-")[1] in ("local", "primary")
             and SUPT.search(" ".join(str(c.get("office") or "").upper().split())) and SCHOOL.search(" ".join(str(c.get("office") or "").upper().split()))
             and c.get("office_scope") == "state"}
    T = {r[0] for r in mv["records"] if "T" in r[8]}
    print(f"  (2) state-scope superintendents by my reading at {AFTER}: {len(found)} (c29 §29.2 found 26); the moves file's T rows: {len(T)}; the same ids: {set(found) == T}"
          + ("" if set(found) == T else f" (mine not T {sorted(set(found) - T)[:5]}; T not mine {sorted(T - set(found))[:5]})"))
    pv = lambda c: (c.get("p") or {}).get("value")  # noqa: E731
    print(f"    their type now: {dict(collections.Counter(c.get('office_type') for c in found.values()))}; p value (or none) unchanged in "
          f"{sum(1 for cid in found if pv(before[cid]) == pv(after[cid]))} of {len(found)}; the reason's words changed in "
          f"{sum(1 for cid in found if pval(before[cid]) != pval(after[cid]))} (D3: 10 name the new class); "
          f"with a p value: {sum(1 for c in found.values() if 'value' in (c.get('p') or {}))} (D3: 3)")
    # (3) the vote test in whole votes
    rows = [r for r in C27.local_rows("NC") if r["scope"] == "local" and "value" in (r["c"].get("p") or {}) and r["date"] not in C27.MEDSL_GENERAL]
    print(f"  (3) North Carolina's other-dates pool at HEAD (its measure files unchanged since {AFTER}): {len(rows)} questions with p (D3: 306)")
    for k in (10, 100):
        whole_v = sum(1 for r in rows if abs(r["yes"] - r["no"]) <= k)
        share = sum(1 for r in rows if abs(r["yes"] / (r["yes"] + r["no"]) - 0.5) <= k / (2.0 * (r["yes"] + r["no"])))
        exact = sum(1 for r in rows if abs(r["yes"] - r["no"]) == k)
        print(f"    within {k} votes: in whole votes {whole_v}; in the share form in floating point {share}; margin exactly {k}: {exact}")
    notes = collections.Counter(re.sub(r"\d[\d.,]*", "#", (r["c"].get("p") or {}).get("note") or "")[:120] for r in rows)
    n25 = sum(1 for r in rows if "25 against 21.9" in ((r["c"].get("p") or {}).get("note") or ""))
    print(f"    notes saying '25 against 21.9': {n25} of {len(rows)}; note shapes {dict(notes)}")
    bt = show(AFTER, "data/local/backtest-ncsbe.json")
    ln = ((bt or {}).get("questions_at_threshold") or {}).get("lean_note") or {}
    print(f"    backtest-ncsbe.json at {AFTER}: vote test {ln.get('vote_test')}; share test {ln.get('share_test')}")
    by_year = collections.Counter(r["year"] for r in rows if abs(r["yes"] - r["no"]) <= 10)
    print(f"    the 25 by year: {dict(sorted(by_year.items()))} (D3: 2016 2 to 3, 2021 2 to 3)")


def main():
    print(f"##### c34 towns, townships and counties' own questions (#86): HEAD {L.git_head()}")
    before, after, mv = section_1()
    section_2(after)
    section_3(before, after)
    section_4(before, after, mv)


if __name__ == "__main__":
    main()
