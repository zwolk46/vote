"""checks/m2/c33_one_county.py: #85 (a7eb84b, against f5a4ac4): a local question MEDSL holds in one county's file only
is counted whole where the place its title names lies wholly in that county, by the Census Bureau's 2020
place-by-county file (item 5 of the orchestrator's order; pipeline/places.py, local_medsl.one_place). The fourth pass
(the orchestrator, 2026-11-07 15:50: "every inferred match and a sample of the stated ones against the Census file,
the guards, and LA's x1.0435").

  33.1 the moves file (data/measure/moves-one-county.json) against my own diff of every record between f5a4ac4 and
       a7eb84b [measured]
  33.2 the two Census files fetched again (checks/m2/fetch_fourth_pass.sh): their hashes against the records' source
       blocks, their columns, what they hold [measured]
  33.3 the one-county questions derived again from the records at f5a4ac4; pipeline/places.py's match written again
       here (copied, not imported) on each; the 722 counted whole against the records' place_whole; then, by my own
       reading and not the pipeline's, every one of the 722 (all 280 inferred, all 442 stated) against the Census
       file and the guards; the 280 inferred listed [measured]
  33.4 Louisiana: the pool of its local measures counted whole with its 8 of 2020 in it, every 2024 p recomputed from
       my own pool, the x1.0435, the 2023 reasons, and the back-test at the questions' own thresholds [measured]

Nothing in pipeline/ or model/ is imported. Run from the repository root: python3 checks/m2/c33_one_county.py
"""
import collections
import hashlib
import json
import os
import re
import subprocess
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402
import c27_local_thresholds as C27  # noqa: E402
import c30_ballot_texts as C30  # noqa: E402
import c31_statewide_filed_local as C31  # noqa: E402

BEFORE = "f5a4ac4"   # #84 merged
AFTER = "a7eb84b"    # #85 merged
MOVES = "data/measure/moves-one-county.json"
FOURTH = os.path.join(L.CACHE, "fourth")
at = C30.at


def show(commit, path):
    return json.loads(subprocess.run(["git", "show", f"{commit}:{path}"], capture_output=True, text=True, cwd=L.ROOT).stdout)


# ---------------------------------------------------------------------------------------------- 33.1
def section_1():
    print("### 33.1 the moves file against my own diff of the records, f5a4ac4 to a7eb84b")
    allf = C31.changed_files(BEFORE, AFTER, under=".")
    recf = [x for x in allf if re.search(r"data/measure/\d{4}/[A-Z]{2}\.json$", x)]
    print(f"  files changed: {len(allf)}; record files {len(recf)}; others: " + ", ".join(x for x in allf if x not in recf))
    before, after = C31.load_records(BEFORE, recf), C31.load_records(AFTER, recf)
    changed = {cid: C31.deep_paths(before[cid], after[cid]) for cid in set(before) & set(after) if before[cid] != after[cid]}
    top = {cid: sorted({x.split(".")[0] for x in v}) for cid, v in changed.items()}
    stamps = {cid for cid, v in top.items() if v == ["p"] and changed[cid] == ["p.commit"]}
    print(f"  records new {len(set(after) - set(before))}, gone {len(set(before) - set(after))}, changed {len(changed)} (p.commit stamp alone {len(stamps)})")
    for paths, n in collections.Counter(tuple(v) for v in top.values()).most_common():
        print(f"    {n:5d}  {', '.join(paths)}")
    mv = show(AFTER, MOVES)
    recs = {r["id"]: r for r in mv["records"]}
    print(f"  the moves file: {len(recs)} records, summary {mv['summary']} (against {mv.get('against')}); its ids == my changed ids less the stamps: "
          f"{set(recs) == set(changed) - stamps}" + ("" if set(recs) == set(changed) - stamps else f" (mine not listed {len((set(changed) - stamps) - set(recs))}, listed not mine {len(set(recs) - set(changed))})"))
    tal = collections.Counter()
    what = collections.Counter()
    for cid, r in recs.items():
        b, a = before.get(cid), after.get(cid)
        if b is None or a is None:
            tal["not in both commits"] += 1
            continue
        pb, pa = b.get("p") or {}, a.get("p") or {}
        pv = lambda p: p.get("value") if "value" in p else p.get("not_computed")  # noqa: E731
        whole = "place_whole" in a
        if whole:
            w = "counted whole: not computed, " + ("same reason" if pb.get("not_computed") == pa.get("not_computed") else "reason changed")
        else:
            w = "pool only: " + ("p moved" if "value" in pa and pa.get("value") != pb.get("value") else "not computed, reason changed")
        what[w] += 1
        same = (sorted(r["fields_changed"]) == top[cid], r["counted_whole"] == whole, r.get("place") == (a.get("place_whole") or {}).get("place"),
                r.get("mark") == (a.get("place_whole") or {}).get("mark"), r["p_before"] == pv(pb), r["p_after"] == pv(pa), r["what"] == w,
                r.get("ratio") is None or abs(r["ratio"] - pa["value"] / pb["value"]) < 5e-5)
        tal["fields, whole, place, mark, p before and after, what and ratio all as the records" if all(same) else f"DIFFERS {same}"] += 1
        if not all(same):
            print(f"    {cid[:60]}: {same} | {r['what']} vs {w}")
    print(f"  the records against the moves file: {dict(tal)}")
    print(f"  my kinds: {dict(what)}; the file's summary: {mv['summary']}; equal: {dict(what) == mv['summary']}")
    return before, after, mv


# ---------------------------------------------------------------------------------------------- 33.2
def plain(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return " ".join(s.upper().replace("'S", "S").split())


KINDS_RE = re.compile(r"^(.*?) (city and borough|city|town|village|borough|municipality|township)$")


def read_census():
    """my own reading of the two files: places (active incorporated only) by state, name and kind; every row by
    geoid; county names; active county subdivisions by state and name"""
    pp = os.path.join(FOURTH, "census_places.txt")
    cp = os.path.join(FOURTH, "census_cousub.txt")
    places = collections.defaultdict(dict)
    by_geoid = collections.defaultdict(list)
    county_names = collections.defaultdict(dict)
    stats = collections.Counter()
    with open(pp, encoding="utf-8") as f:
        head = f.readline().rstrip("\n").split("|")
        for line in f:
            st, sfp, cfp, cname, pfp, _ns, pname, typ, _cls, fs = line.rstrip("\n").split("|")
            stats["rows"] += 1
            base_c = re.sub(r" (County|Parish|Borough|Census Area|Municipality|City and Borough|city)$", "", cname)
            county_names[st][plain(base_c)] = sfp + cfp
            by_geoid[sfp + pfp].append((sfp + cfp, cname, typ, fs, pname))
            if typ != "INCORPORATED PLACE" or fs != "A":
                stats["rows not an active incorporated place"] += 1
                continue
            stats["rows of active incorporated places"] += 1
            m = KINDS_RE.match(re.sub(r"\s*\(.*\)$", "", pname))
            name, kind = (m.group(1), m.group(2)) if m else (re.sub(r"\s*\(.*\)$", "", pname), "")
            p = places[st].setdefault((plain(name), kind.upper()), {"geoid": sfp + pfp, "census_name": pname, "counties": {}})
            if p["geoid"] != sfp + pfp:
                p["ambiguous"] = True
            p["counties"][sfp + cfp] = cname
    subs = collections.defaultdict(lambda: collections.defaultdict(set))
    with open(cp, encoding="utf-8") as f:
        head2 = f.readline().rstrip("\n").split("|")
        for line in f:
            st, sfp, cfp, _cn, _cfp, _ns, sname, _cls, fs = line.rstrip("\n").split("|")
            stats["cousub rows"] += 1
            if fs != "A":
                continue
            stats["cousub rows active"] += 1
            m = KINDS_RE.match(sname)
            subs[st][plain(m.group(1) if m else sname)].add((sfp + cfp, plain(sname)))
    return places, by_geoid, county_names, subs, stats, head, head2


def section_2(after):
    print("### 33.2 the Census files fetched again")
    src = None
    for c in after.values():
        pass
    for f in C31.record_files(AFTER):
        d = at(AFTER, f)
        s = (d or {}).get("sources") or {}
        if "census_places" in s:
            src = s
            break
    for name, key in (("census_places.txt", "census_places"), ("census_cousub.txt", "census_cousub")):
        p = os.path.join(FOURTH, name)
        h = hashlib.sha256(open(p, "rb").read()).hexdigest() if os.path.exists(p) else None
        rec = (src or {}).get(key) or {}
        print(f"  {name}: sha256 {h[:16] if h else 'not fetched'}... equals the record's source block ({rec.get('read_utc')}): {h == rec.get('sha256')}; "
              f"url as the record's: {rec.get('url', '').endswith(name.replace('census_', 'national_').replace('places', 'place_by_county2020').replace('cousub', 'cousub2020'))}")
    places, by_geoid, county_names, subs, stats, head, head2 = read_census()
    print(f"  columns: {head}; {head2}")
    multi = sum(1 for st in places for p in places[st].values() if len(p["counties"]) > 1)
    amb = sum(1 for st in places for p in places[st].values() if p.get("ambiguous"))
    print(f"  {dict(stats)}; active incorporated places (by state, name and kind) {sum(len(v) for v in places.values())}, in more than one county {multi}, "
          f"a name and kind shared by two places of a state {amb}")
    return places, by_geoid, county_names, subs


# ---------------------------------------------------------------------------------------------- 33.3
# pipeline/places.py match(), written again here on my own reading of the files (copied, not imported)
MCD_TOWNS = {"CT", "MA", "ME", "NH", "NY", "RI", "VT", "WI", "MN"}
_TYPED = re.compile(r"\b(CITY|TOWN|VILLAGE|BOROUGH) OF\s+")
_KIND_WORDS = {"CITY", "TOWN", "VILLAGE", "BOROUGH"}
_NOT_PLACE = re.compile(r"\bSCHOOLS?\b|\bDISTRICT\b|\bDIST\b|\bUSD\b|\bISD\b|\bCISD\b|\bESD\b|\bHSD\b|\bUHSD\b|"
                        r"\bUNION (#|HSD|HS\b|NO\b)|\bBOE\b|BOARD OF EDUCATION|\bUNIFIED\b|\bCOLLEGE\b|"
                        r"\bCOUNTY\b|\bPARISH\b|\bTOWNSHIP\b|\bTWP\b")
_SPECIAL = re.compile(r"\b(FIRE|HOSPITAL|LIBRARY|PORT|TRANSIT|WATER|SEWER|SANITARY|SANITATION|IRRIGATION|CEMETERY|"
                      r"AUTHORITY|AREA|REGIONAL|JOINT|CONSOLIDATED|PARK|RECREATION|UTILITY|UTILITIES|AMBULANCE|EMS|"
                      r"DRAINAGE|LEVEE|CONSERVANCY|AIRPORT|HEALTH|MOSQUITO)\b")
_OREGON_NO = re.compile(r"^\d+-\d+\s*:?\s*")
_AFTER_HYPHEN = re.compile(r"(QUESTION|PROP|PROPOSITION|MEASURE|ISSUE|BOND|REFERENDUM|SPECIAL|\d)")


def match(office, state, county, places, county_names, subs):
    t = plain(office)
    t = _OREGON_NO.sub("", t)
    mine = places.get(state, {})
    if _NOT_PLACE.search(t):
        return None, "the title names a district, a county, a parish or a township"
    names = collections.defaultdict(list)
    for k, v in mine.items():
        names[k[0]].append((k, v))
    hit = None
    for m in _TYPED.finditer(t):
        kind, words = m.group(1), t[m.end():].split()
        for n in range(min(6, len(words)), 0, -1):
            name = " ".join(words[:n]).strip(" .,-:;()")
            if n == 1 and name not in names and "-" in name:
                name = name.split("-")[0]
            same = [(k, v) for k, v in names.get(name, ()) if k[1] == kind or (kind == "CITY" and k[1] == "")]
            if same:
                hit = ("stated", f"the title says '{kind} OF {name}'", same)
            elif names.get(name) and not (kind == "TOWN" and state in MCD_TOWNS):
                hit = ("inferred", f"the title says '{kind} OF {name}'; the Census calls it a "
                       f"{names[name][0][0][1].lower() or 'place'}", names[name])
            if hit:
                break
        if hit:
            break
    if hit is None:
        for n in sorted(names, key=len, reverse=True):
            if t == n or t.startswith(n + " ") or t.startswith(n + ",") or t.startswith(n + ":"):
                hit = ("inferred", f"the title begins with the place's name '{n}'", names[n])
                break
            if t.startswith(n + "- ") or t.startswith(n + " -"):
                hit = ("inferred", f"the title begins with the place's name '{n}'", names[n])
                break
            if t.startswith(n + "-"):
                if not _AFTER_HYPHEN.match(t[len(n) + 1:].strip()):
                    return None, f"the place's name '{n}' is joined by a hyphen to another name"
                hit = ("inferred", f"the title begins with the place's name '{n}'", names[n])
                break
        if hit is None:
            return None, "the title names no incorporated place of the state"
        n = hit[2][0][0][0]
        rest = t[len(n):]
        if _SPECIAL.search(rest):
            return None, f"the title names a special body after the place's name ('{_SPECIAL.search(rest).group(0)}')"
        w = rest.replace(":", " ").replace(",", " ").split()[:2]
        if w and w[0] in _KIND_WORDS and len(hit[2]) == 1 and w[0] != hit[2][0][0][1]:
            return None, f"the title's word '{w[0]}' after the name is not the place's kind"
        if len(w) == 2 and w[1] in _KIND_WORDS and w[0] not in _KIND_WORDS:
            return None, f"the name goes on past the place's ('{n} {w[0]} {w[1]}')"
        other = {full for cf, full in subs[state].get(n, ()) if cf == county} - {plain(x[1]["census_name"]) for x in hit[2]}
        if other and not (w and len(hit[2]) == 1 and w[0] == hit[2][0][0][1]):
            return None, (f"the name is also a town's or township's in the county ({', '.join(sorted(other))}), "
                          "so the title does not show which holds the question")
        if county_names[state].get(n) == county:
            return None, "a county of the same name is the record's county, so the county's own question is likelier"
    mark, how, cands = hit
    if len(cands) > 1 or any(v.get("ambiguous") for _, v in cands):
        return None, "the name is more than one place in the state"
    (name, kind), p = cands[0]
    if len(p["counties"]) > 1:
        return None, f"the place lies in {len(p['counties'])} counties"
    if county not in p["counties"]:
        return None, "the place lies in another county than the record's"
    return {"place": p["census_name"], "geoid": p["geoid"], "county": county, "county_name": p["counties"][county],
            "how": how, "mark": mark}, None


D3_TABLE = {"counted whole, the place [stated]": 442, "counted whole, the place [inferred]": 280,
            "held: the title names no incorporated place": 1345, "held: the title names a district, county, parish or township": 938,
            "held: a retention": 880, "held: the place lies in 2 or 3 counties": 50, "held: a county of the same name is the record's": 20,
            "held: a special body after the name": 9, "held: the name is also a town's or township's in the county": 5,
            "held: hyphen join, name goes on, or another county": 3}


def d3_label(found, why):
    if found:
        return f"counted whole, the place [{found['mark']}]"
    if why.startswith("the title names no incorporated"):
        return "held: the title names no incorporated place"
    if why.startswith("the title names a district"):
        return "held: the title names a district, county, parish or township"
    if why == "a retention":
        return "held: a retention"
    if why.startswith("the place lies in") and "counties" in why:
        return "held: the place lies in 2 or 3 counties"
    if why.startswith("a county of the same name"):
        return "held: a county of the same name is the record's"
    if why.startswith("the title names a special body"):
        return "held: a special body after the name"
    if why.startswith("the name is also a town"):
        return "held: the name is also a town's or township's in the county"
    if "hyphen" in why or "goes on" in why or "another county" in why or "not the place's kind" in why:
        return "held: hyphen join, name goes on, or another county"
    return "held: " + why[:40]


# my own reading of a whole question, apart from the pipeline's rules (the guards as plain tests on the title)
_BODY_WORDS = re.compile(r"\b(SCHOOLS?|DISTRICT|DIST|USD|ISD|CISD|ESD|HSD|UHSD|BOE|UNIFIED|COLLEGE|COUNTY|PARISH|TOWNSHIP|TWP|"
                         r"FIRE|HOSPITAL|LIBRARY|PORT|TRANSIT|WATER|SEWER|SANITARY|SANITATION|IRRIGATION|CEMETERY|AUTHORITY|AREA|"
                         r"REGIONAL|JOINT|CONSOLIDATED|PARK|RECREATION|UTILITY|UTILITIES|AMBULANCE|EMS|DRAINAGE|LEVEE|CONSERVANCY|"
                         r"AIRPORT|HEALTH|MOSQUITO)\b")


def my_reading(title, st, county, pw, places, by_geoid, county_names, subs):
    t = _OREGON_NO.sub("", plain(title))
    m = KINDS_RE.match(re.sub(r"\s*\(.*\)$", "", pw["place"]))
    name = plain(m.group(1) if m else pw["place"])
    rows = by_geoid.get(pw["geoid"], [])
    tests = collections.OrderedDict()
    tests["Census: the geoid has one row, in the record's county, an active incorporated place"] = (
        len(rows) == 1 and rows[0][0] == county == pw["county"] and rows[0][2] == "INCORPORATED PLACE" and rows[0][3] == "A")
    tests["Census: no other active incorporated place of that name in the state"] = sum(1 for (n, k), v in places.get(st, {}).items() if n == name) == 1 and not any(v.get("ambiguous") for (n, k), v in places.get(st, {}).items() if n == name)
    tests["title: begins with the name, bare or after CITY/TOWN/VILLAGE/BOROUGH OF"] = bool(re.match(r"^((CITY|TOWN|VILLAGE|BOROUGH) OF )?" + re.escape(name) + r"(\b|$)", t))
    tests["title: no district, county, school or special-body word anywhere"] = not _BODY_WORDS.search(t)
    tests["Census: no other active county subdivision of the name in the county"] = not ({full for cf, full in subs[st].get(name, ()) if cf == county} - {plain(pw["place"])})
    tests["Census: the county is not of the same name"] = county_names[st].get(name) != county
    return tests


def section_3(before, after, places, by_geoid, county_names, subs):
    print("### 33.3 the one-county questions derived again, matched again, and read again")
    recs_b = C31.load_records(BEFORE, C31.record_files(BEFORE))
    recs_a = C31.load_records(AFTER, C31.record_files(AFTER))
    mine = [c for c in recs_b.values() if c.get("question") and (c.get("result") or {}).get("source") == "medsl" and c["question"].get("scope") == "local"]
    where = collections.defaultdict(set)
    key = lambda c: (c["place"]["state"], c["question"]["title"].upper(), (c["question"].get("subject") or "").upper(), c.get("date"))  # noqa: E731
    for c in mine:
        where[key(c)].update(c["place"].get("counties") or [])
    one = [c for c in mine if len(where[key(c)]) == 1]
    print(f"  local questions of MEDSL's at f5a4ac4: {len(mine)}; held in one county's file only (the same state, title, subject and date in no other): {len(one)} "
          f"(D3: 3,972 after the retentions' and the no-county lines are counted among them); in more than one county's file {len(mine) - len(one)}")
    tal = collections.Counter()
    whole = {}
    d3 = collections.Counter()
    for c in one:
        q = c["question"]
        if q.get("kind") == "retention":
            found, why = None, "a retention"
        elif len(c["place"].get("counties") or []) != 1:
            found, why = None, "the line names no county"
        else:
            found, why = match(q["title"], c["place"]["state"], c["place"]["counties"][0], places, county_names, subs)
        d3[d3_label(found, why)] += 1
        if found:
            whole[c["id"]] = found
    rec_whole = {cid: c["place_whole"] for cid, c in recs_a.items() if c.get("place_whole")}
    print(f"  counted whole by my run of the match: {len(whole)}; records with place_whole at a7eb84b: {len(rec_whole)}; the same ids: {set(whole) == set(rec_whole)}")
    eq = sum(1 for cid, f in whole.items() if rec_whole.get(cid) == f)
    print(f"  place_whole (place, geoid, county, county_name, how, mark) equal in {eq} of {len(whole)}")
    for cid in [cid for cid, f in whole.items() if rec_whole.get(cid) != f][:5]:
        print(f"    {cid}: mine {whole[cid]} | record {rec_whole.get(cid)}")
    print("  the counts, mine | D3's table (REPORT section 22):")
    for lab, n in D3_TABLE.items():
        print(f"    {d3.get(lab, 0):5d} | {n:5d}  {lab}")
    extra = {k: v for k, v in d3.items() if k not in D3_TABLE}
    print(f"    other labels of mine: {extra or 'none'}; my total over D3's rows {sum(d3.get(k, 0) for k in D3_TABLE)} (D3: 3,972)")
    by_year = collections.Counter(int(cid[:4]) for cid in whole)
    print(f"  whole by year: {dict(sorted(by_year.items()))} (D3: 259, 109, 52, 6, 296)")
    # my own reading of every whole question
    print("  every whole question read again, apart from the pipeline's rules (tests passed, by mark):")
    res = collections.defaultdict(collections.Counter)
    fails = collections.defaultdict(list)
    inferred = []
    for cid, pw in sorted(rec_whole.items()):
        c = recs_a[cid]
        st, county = c["place"]["state"], c["place"]["counties"][0]
        tests = my_reading(c["question"]["title"], st, county, pw, places, by_geoid, county_names, subs)
        for k, v in tests.items():
            res[pw["mark"]][k] += int(v)
            if not v:
                fails[(pw["mark"], k)].append((st, c["question"]["title"], pw["place"]))
        if pw["mark"] == "inferred":
            inferred.append((st, c["year"], c["question"]["title"], pw["place"], pw["county_name"]))
    for mark in ("stated", "inferred"):
        n = sum(1 for pw in rec_whole.values() if pw["mark"] == mark)
        print(f"    [{mark}] {n} questions:")
        for k, v in res[mark].items():
            print(f"      {v:4d} of {n}  {k}")
    for (mark, k), items in sorted(fails.items()):
        print(f"    [{mark}] fails '{k}' ({len(items)}):")
        for st, title, place in items[:12]:
            print(f"      {st}: {title[:70]!r} -> {place}")
        if len(items) > 12:
            print(f"      ... {len(items) - 12} more")
    print(f"  the {len(inferred)} inferred matches (state, year, title -> place, county), for the eye:")
    for st, y, title, place, cname in inferred:
        print(f"    {st} {y}: {title[:72]} -> {place} ({cname})")


# ---------------------------------------------------------------------------------------------- 33.4
def la_rows(commit):
    out = []
    for f in C31.record_files(commit):
        if not f.endswith("/LA.json"):
            continue
        d = at(commit, f)
        for c in d["contests"]:
            q, res = c.get("question") or {}, c.get("result") or {}
            if not q or q.get("scope") != "local":
                continue
            if res.get("source") not in ("la_sos",) and not c.get("place_whole"):
                continue
            yes, no = C27.yes_no(c)
            out.append(dict(c=c, year=c["year"], kind=q.get("kind"), yes=yes, no=no, src=res.get("source")))
    return out


def section_4():
    print("### 33.4 Louisiana: the pool with its 8 whole questions of 2020, every 2024 p recomputed, the x1.0435, the back-test")
    rows_a, rows_b = la_rows(AFTER), la_rows(BEFORE)
    pool = collections.defaultdict(list)
    for r in rows_a:
        if r["yes"] + r["no"] > 0 and r["kind"] == "measure" and not r["c"].get("one_answer_only"):
            pool[r["year"]].append(r["yes"] / (r["yes"] + r["no"]))
    pool_b = collections.defaultdict(list)
    for r in rows_b:
        if r["yes"] + r["no"] > 0 and r["kind"] == "measure" and not r["c"].get("one_answer_only"):
            pool_b[r["year"]].append(r["yes"] / (r["yes"] + r["no"]))
    print(f"  the pool of Louisiana's local measures counted whole, by year: now {dict(sorted((y, len(v)) for y, v in pool.items()))}; before #85 {dict(sorted((y, len(v)) for y, v in pool_b.items()))}; "
          f"sources now {dict(collections.Counter(r['src'] for r in rows_a))}")
    before_p = {r["c"]["id"]: r["c"].get("p") or {} for r in rows_b}
    tal = collections.Counter()
    ratios = collections.Counter()
    out = []
    for r in rows_a:
        c = r["c"]
        p = c.get("p") or {}
        if r["year"] != 2024 or "value" not in p:
            continue
        t = (c.get("threshold") or {}).get("t")
        train = [s for y, ss in pool.items() if y < 2024 for s in ss]
        f, N, h, k = C27.density_at(train, t)
        n = r["yes"] + r["no"] - 1
        mine = f / (2 * n) if t == 0.5 else max((1 - t) * f / n, t * f / n)
        fc = (c.get("forecasts") or [{}])[-1]
        same = (abs(mine - p["value"]) / p["value"] <= 1e-5, fc.get("like_measures") == N, fc.get("in_window") == k, fc.get("window") == [round(t - h, 4), round(t + h, 4)])
        tal["p, N, k and window equal" if all(same) else f"DIFFERS {same}"] += 1
        pb = before_p.get(c["id"], {}).get("value")
        if pb:
            ratios[round(p["value"] / pb, 4)] += 1
        s = r["yes"] / (r["yes"] + r["no"])
        out.append(dict(q=k / N, own=abs(s - t) <= h, near={hh: (sum(1 for x in train if abs(x - t) <= hh) / len(train), abs(s - t) <= hh) for hh in C27.WINDOWS}))
    print(f"  2024 p: {dict(tal)}; ratio to the p before #85: {dict(ratios)}; (15/307)/(14/299) = {(15 / 307) / (14 / 299):.4f}")
    reasons = collections.Counter((r["c"].get("p") or {}).get("not_computed", "")[:75] for r in rows_a if r["year"] == 2023 and "value" not in (r["c"].get("p") or {}))
    print(f"  2023 without p: {dict(reasons)}")
    r20 = [r for r in rows_a if r["year"] == 2020 and r["c"].get("place_whole")]
    print(f"  the 8 of 2020 counted whole: {len(r20)}; their reasons: {dict(collections.Counter((r['c'].get('p') or {}).get('not_computed', 'p')[:60] for r in r20))}")
    rec = (L.load_json(os.path.join(L.DATA, "measure", "backtest-measures.json")).get("at_threshold_local") or {}).get("all years local measure, LA") or {}
    own = (sum(o["q"] for o in out), sum(o["own"] for o in out))
    near = {hh: (sum(o["near"][hh][0] for o in out), sum(o["near"][hh][1] for o in out)) for hh in C27.WINDOWS}
    print(f"  the back-test at the questions' own thresholds, all years with p ({len(out)} measures): own window {own[0]:.1f}/{own[1]} (record {rec.get('own_window')}); "
          + "; ".join(f"within {hh:.0%} {e:.1f}/{s}" for hh, (e, s) in near.items()) + f" (record {rec.get('near_threshold')})")


def main():
    print(f"##### c33 one-county titles counted whole (#85): HEAD {L.git_head()}")
    before, after, mv = section_1()
    places, by_geoid, county_names, subs = section_2(after)
    section_3(before, after, places, by_geoid, county_names, subs)
    section_4()


if __name__ == "__main__":
    main()
