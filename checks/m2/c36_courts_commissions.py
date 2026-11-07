"""c36: D3's #88 (8406745): the orchestrator's rulings of 2026-11-07 16:19 applied: a supreme court or appellate seat
elected statewide in a one-seat contest typed "statewide judge" (142 records), a statewide commission seat electing
one seat typed "statewide officer" (14, with Montana's Clerk of the Supreme Court, 2), New Mexico's 2022 Public
Education Commissioners given their districts and the official votes (5), Illinois's two 2018 stray lines held, and
21 p lost to the smaller pools.

The orchestrator (2026-11-07 16:53 UTC): "#88: the "every county" test for the 142 statewide judges and the 5 near
misses; the 14 commission seats by their own seat count; the 21 lost p, by your pool counts (8 and 94); NM PEC's
districts." The rulings (16:19, verbatim in data/local/REPORT.md section 25): 1. "A statewide contest for a commission
seat that elects one seat, by the source's own vote-for or seat count, is a "statewide officer". Where it elects more
than one, it keeps the board type. Where the source does not show the count, hold it as a board and do not infer the
count." 2. "A supreme court or appellate seat elected statewide in a one-seat contest is typed "statewide judge".
Retentions stay retentions, and the other judges keep their type." 3. "MT's Clerk of the Supreme Court is a statewide
officer." 4. "NM's PEC members are elected by district, so find the district or hold them." 5. "IL 2018's two stray
lines: identify them from the State Board's results and fix or hold them, with the reason."

What this does (every figure [measured] unless marked):
  36.1 the moves file (data/local/moves-courts-commissions.json) against my own diff of every record file between
       afbb7bd (before: #87) and 8406745 (after): the records that changed, the codes (T type, R reason, L p lost,
       I id changed, Q note), types and p before and after; the 21 lost p.
  36.2 the "every county" test, from MEDSL's own files (my summaries of the raw files, checks/m2/m2medsl.py) and the
       State Board's results_pct files: for every state-scope record of a court, a commission or the clerk in the
       files fetched, the counties its votes are in against the counties any of the state's contests on that date has
       votes in, and the source's own seat count (MEDSL's magnitude; the State Board's vote-for); my own type by the
       rulings against the record's; the 5 near misses D3 lists (Oregon 2024 positions 1 and 7, Washington 2022
       positions 1, 5 and 6) with my counts.
  36.3 the 14 commission seats and Montana's clerk by their own seat count; the commission contests that keep the
       board type (more than one seat, or not every county).
  36.4 the 21 lost p: each reason's count of like races against my own count from the records' classes at 8406745
       (c35.pools_at), and the class's count before (at afbb7bd) that let p be computed; the two Illinois strays read
       in MEDSL's 2018 file.
  36.5 New Mexico's Public Education Commissioners: the Secretary of State's page (fetched by fetch_fifth_pass.sh)
       read with my own copy of pipeline/intake/nm_sos.py's patterns (said so), the archive's link to it, each
       district's candidate, votes, total and precincts against the records; MEDSL's own counts from the 2022 file
       against result.medsl_votes.
Nothing from pipeline/ is imported; the patterns copied are marked.
"""
import collections
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402
import m2medsl as M  # noqa: E402
import c31_statewide_filed_local as C31  # noqa: E402
import c34_towns_counties as C34  # noqa: E402
import c35_statewide_officers as C35  # noqa: E402

BEFORE = "afbb7bd"   # #87 merged
AFTER = "8406745"    # #88 merged
MOVES = "data/local/moves-courts-commissions.json"
LEVELS = ("local", "primary", "measure", "state-lower", "state-upper")
# copied from pipeline/local_medsl.py at 8406745 (#88), so that the rule is applied here as the pipeline words it;
# nothing is imported
STATE_COMMISSION = re.compile(r"\bCOM+IS+I[O0]N(ERS?)?\b")
STATE_COURT = re.compile(r"\bSUPREME\b|\bAPPEALS\b|\bAPPELLATE\b|\bCOMMONWEALTH COURT\b|\bCT OF APP\b")
RETENTION = re.compile(r"RETENTION|RETAIN")
CLERK = re.compile(r"CLERK OF THE SUPREME COURT")
REASON_N = re.compile(r"fewer than 100 like races in earlier years in the sources taken in \((\d+)\) for the class '([^']+)'")
FIFTH = os.path.join(L.CACHE, "fifth")
NEAR_FILES = ("data/local/2022/WA.json", "data/local/2024/OR.json")   # D3's near misses (REPORT section 25)


# ---------------------------------------------------------------------------------------------- 36.1
def my_codes(b, a):
    codes = set()
    pb, pa = b.get("p") or {}, a.get("p") or {}
    if b.get("office_type") != a.get("office_type"):
        codes.add("T")
    if "not_computed" in pa and "not_computed" in pb and pa["not_computed"] != pb["not_computed"]:
        codes.add("R")
    if "value" in pb and "value" not in pa:
        codes.add("L")
    if b.get("notes") != a.get("notes"):
        codes.add("Q")
    return codes


def section_1():
    print(f"### 36.1 the moves file against my own diff of the records, {BEFORE} to {AFTER}")
    allf = C31.changed_files(BEFORE, AFTER, under=".")
    recf = [x for x in allf if re.search(r"data/(" + "|".join(LEVELS) + r")/\d{4}/[A-Z]{2}\.json$", x)]
    print(f"  files changed: {len(allf)}; record files {len(recf)} ({dict(collections.Counter(x.split('/')[1] for x in recf))}); others: "
          + ", ".join(x for x in allf if x not in recf))
    before, after = C31.load_records(BEFORE, recf), C31.load_records(AFTER, recf)
    changed = {cid: C31.deep_paths(before[cid], after[cid]) for cid in set(before) & set(after) if before[cid] != after[cid]}
    stamps = {cid for cid, v in changed.items() if v == ["p.commit"]}
    new, gone = sorted(set(after) - set(before)), sorted(set(before) - set(after))
    print(f"  records new {len(new)}, gone {len(gone)}, changed {len(changed)} (p.commit stamp alone {len(stamps)})")
    print(f"    new: {new}\n    gone: {gone}")
    for paths, n in collections.Counter(tuple(sorted({x.split('.')[0] for x in v})) for cid, v in changed.items() if cid not in stamps).most_common():
        print(f"    {n:5d}  {', '.join(paths)}")
    moved = [cid for cid in changed if "value" in (after[cid].get("p") or {}) and "value" in (before[cid].get("p") or {}) and after[cid]["p"]["value"] != before[cid]["p"]["value"]]
    lost = [cid for cid in changed if "value" in (before[cid].get("p") or {}) and "value" not in (after[cid].get("p") or {})]
    gained = [cid for cid in changed if "value" not in (before[cid].get("p") or {}) and "value" in (after[cid].get("p") or {})]
    print(f"  p values that moved: {len(moved)}; p lost: {len(lost)} (D3: 21); p gained: {len(gained)}")
    mv = C34.show(AFTER, MOVES)
    recs = {r[0]: r for r in mv["records"]}
    mine = (set(changed) - stamps) | set(new)
    print(f"  the moves file: {len(recs)} records (its 'against': {mv.get('against')}); summary {mv['summary']}; p_lost {mv.get('p_lost')}")
    print(f"  its ids == my changed ids less the stamps, with the new ids: {set(recs) == mine}" + ("" if set(recs) == mine else
          f" (mine not listed {sorted(mine - set(recs))[:6]}, listed not mine {sorted(set(recs) - mine)[:6]})"))
    tal = collections.Counter()
    for cid, r in recs.items():
        b, a = before.get(cid), after.get(cid)
        if a is None:
            tal["not at the after commit"] += 1
            continue
        if b is None:
            tal[f"new id ({','.join(r[8])}): type after and p after as the record" if r[4] == a.get("office_type") and r[6] == C34.pval(a) else "new id: DIFFERS"] += 1
            continue
        same = (my_codes(b, a) == set(r[8]), r[3] == b.get("office_type"), r[4] == a.get("office_type"), r[5] == C34.pval(b), r[6] == C34.pval(a))
        tal["codes, types and p before and after all as the records" if all(same) else f"DIFFERS {same}"] += 1
        if not all(same):
            print(f"    {cid[:70]}: file {r[8]} mine {sorted(my_codes(b, a))} | {same}")
    print(f"  the records against the moves file: {dict(tal)}")
    T = [cid for cid, r in recs.items() if "T" in r[8]]
    print(f"  T rows {len(T)}: by type after {dict(collections.Counter(recs[cid][4] for cid in T))}; by level {dict(collections.Counter(cid.split('-')[1] for cid in T))}; "
          f"types before {dict(collections.Counter(recs[cid][3] for cid in T))}")
    print(f"  statewide judges at {AFTER}: {sum(1 for c in after.values() if c.get('office_type') == 'statewide judge')} in the changed files; "
          f"by source {dict(collections.Counter((c.get('result') or {}).get('source') for c in after.values() if c.get('office_type') == 'statewide judge'))}")
    return before, after, mv


# ---------------------------------------------------------------------------------------------- 36.2
def slug(s):
    return re.sub(r"[^A-Za-z0-9]", "_", s).strip("_")


def nc_contest(cid, con):
    """the State Board contest of a North Carolina record, by the id's slug of the contest's name"""
    parts = cid.split("-")
    tail = "-".join(parts[3:])   # after '<year>-<level>-NC-'; the State Board's own dates add 'ncsbe-<date>-' first
    tail = re.sub(r"^ncsbe-\d{4}-\d{2}-\d{2}-", "", tail)
    party = None
    m = re.match(r"^(.*)-([a-z]+)$", tail)
    if parts[1] == "primary" and m:
        tail, party = m.group(1), m.group(2)
    hits = [n for n in con if slug(n).lower() == tail.lower() or (party and slug(n).lower() in (f"{tail}__{party}".lower(), f"{tail}_{party}".lower()))]
    if not hits and tail:
        hits = [n for n in con if slug(n).lower().startswith(tail.lower()) and (not party or party.upper() in n.upper())]
    return hits


def my_type(office, before_type, whole, seats):
    """the rulings of 16:19 as I read them: a court seat (not a retention, not a clerk) elected statewide in a one-seat
    contest 'statewide judge'; a commission seat so elected 'statewide officer' (from the board type); Montana's Clerk
    of the Supreme Court 'statewide officer'; else the type it had"""
    o = office.upper()
    if CLERK.search(o):
        return "statewide officer"
    if whole and seats == 1 and not RETENTION.search(o) and "CLERK" not in o:
        if STATE_COURT.search(o):
            return "statewide judge"
        if STATE_COMMISSION.search(o) and before_type == "council, commission or board":
            return "statewide officer"
    return before_type


def seats_of(mags):
    """the source's own seat count: MEDSL's magnitude where its contest's rows give one value ('1', '1.0'), else None"""
    vals = set()
    for m in mags:
        try:
            v = float(m)
        except (TypeError, ValueError):
            continue
        if v == int(v):
            vals.add(int(v))
    return vals.pop() if len(vals) == 1 and len({str(m).strip() for m in mags if str(m).strip()}) == 1 else None


def medsl_contest(c, s):
    """the summary's state contests of a record: the office's key and the district (a record with none takes the
    file's '' or 'STATEWIDE')"""
    st, date = c["place"]["state"], c.get("date")
    office = M.office_key(c["office"])
    dist = (c["place"].get("district") or "").strip().upper()
    out = {}
    for k, v in s["state_contests"].items():
        p = k.split("|")
        if p[0] != st or p[1] != date or "|".join(p[2:-1]) != office:
            continue
        d = p[-1].strip().upper()
        if d == dist or (not dist and d in ("", "STATEWIDE")) or (dist == "STATEWIDE" and d == ""):
            out[k] = v
    if not out:
        out = {k: v for k, v in s["state_contests"].items() if k.split("|")[0] == st and k.split("|")[1] == date and "|".join(k.split("|")[2:-1]) == office}
        return out, "office only"
    return out, "office and district"


def section_2(before, after):
    print("### 36.2 the 'every county' test and the seat count, from the files, for every court, commission or clerk record of state scope")
    # every state-scope record at AFTER in the changed files, plus the files of the states and years the moves name
    pool = dict(after)
    for f in NEAR_FILES:   # the files D3's near misses sit in, whether or not #88 changed them
        for cid, c in C31.load_records(AFTER, [f]).items():
            pool.setdefault(cid, c)
            before.setdefault(cid, (C31.load_records(BEFORE, [f]).get(cid) or c))
    recs = [c for c in pool.values() if c.get("office_scope") == "state" and c.get("office")
            and (STATE_COURT.search(c["office"].upper()) or STATE_COMMISSION.search(c["office"].upper()) or CLERK.search(c["office"].upper()))]
    print(f"  state-scope records at {AFTER} (changed files, and {', '.join(NEAR_FILES)}) whose office names a court, a commission or the clerk: {len(recs)}; by type "
          f"{dict(collections.Counter(c.get('office_type') for c in recs))}; by source {dict(collections.Counter((c.get('result') or {}).get('source') for c in recs))}")
    summaries, nc_sum = {}, {}
    tal = collections.Counter()
    judges = collections.Counter()
    near = []
    nc_rows = []
    left = collections.Counter()
    typed_mine = collections.Counter()
    for c in sorted(recs, key=lambda c: c["id"]):
        cid, st, year, date = c["id"], c["place"]["state"], c["year"], c.get("date")
        src = (c.get("result") or {}).get("source")
        b = before.get(cid) or {}
        bt = b.get("office_type") or c.get("office_type")
        if src == "ncsbe":
            path = M.fetched().get(f"ncsbe:{date}")
            if not path:
                left[f"North Carolina {date}: results file not fetched"] += 1
                continue
            if path not in nc_sum:
                nc_sum[path] = M.ncsbe_summary(path)
            con = nc_sum[path]["contests"]
            hits = nc_contest(cid, con)
            if len(hits) != 1:
                left[f"North Carolina: {len(hits)} contests match the id"] += 1
                print(f"    not matched: {cid[:80]}: {hits[:3]}")
                continue
            k = con[hits[0]]
            whole = k["n_counties"] >= 100
            seats = int(k["vote_for"][0]) if len(k["vote_for"]) == 1 and k["vote_for"][0].isdigit() else None
            mine = my_type(c["office"], bt, whole, seats)
            ok = mine == c.get("office_type")
            tal[f"North Carolina: my type == the record's ({ok})"] += 1
            if c.get("office_type") == "statewide judge" or mine == "statewide judge":
                judges[(c.get("office_type"), mine, f"counties {k['n_counties']}", f"vote_for {sorted(k['vote_for'])}")] += 1
            if not ok:
                print(f"    DIFFERS: {cid[:80]}: record {c.get('office_type')}, mine {mine} (counties {k['n_counties']}, vote_for {sorted(k['vote_for'])}; "
                      f"names on the ballot {len([x for x in (c.get('result') or {}).get('candidates', []) if x.get('party') != 'write-in'])}: the pipeline's seats_of reads one name as one seat where the file gives no vote-for, a reading)")
            continue
        if src != "medsl":
            left[f"source {src}"] += 1
            continue
        paths = M.medsl_files(year, st)
        if not paths:
            left[f"{year} {st}: MEDSL file not fetched"] += 1
            continue
        path = paths[0]
        if path not in summaries:
            summaries[path] = M.summary(path, year)
        s = summaries[path]
        con, how = medsl_contest(c, s)
        if not con:
            left[f"{year}: contest not found in the file by office"] += 1
            print(f"    not found: {cid[:80]} office key {M.office_key(c['office'])!r} district {c['place'].get('district')!r}")
            continue
        allc = set(s["counties_all"].get(f"{st}|{date}", []))
        got = set()
        mags = set()
        for v in con.values():
            got.update(v["counties"])
            mags.update(v["magnitudes"])
        whole = len(allc) > 1 and allc <= got
        seats = seats_of(mags)
        mine = my_type(c["office"], bt, whole, seats)
        ok = mine == c.get("office_type")
        tal[f"MEDSL: my type == the record's ({ok}); matched by {how}" + ("" if len(con) == 1 else f", {len(con)} contests")] += 1
        if c.get("office_type") == "statewide judge" or mine == "statewide judge":
            judges[(c.get("office_type"), mine, "every county" if whole else f"{len(got & allc)} of {len(allc)} counties", f"magnitude {sorted(mags)}")] += 1
        if STATE_COURT.search(c["office"].upper()) and not RETENTION.search(c["office"].upper()) and not whole and len(allc) - len(got & allc) <= 10 and len(allc) > 1:
            near.append((cid, len(got & allc), len(allc), sorted(mags), c.get("office_type")))
        if not ok:
            print(f"    DIFFERS: {cid[:80]}: record {c.get('office_type')}, mine {mine} (counties {len(got & allc)} of {len(allc)}, magnitude {sorted(mags)}, before {bt})")
        typed_mine[(bt, mine)] += 1
    print(f"  the records against my own reading of the rulings from the files: {dict(tal)}")
    print(f"  left out: {dict(left) or 'none'}")
    print(f"  the type before -> my type (MEDSL records): {dict(typed_mine)}")
    print("  the statewide judges (record's type, my type, counties, seats):")
    for k, n in sorted(judges.items(), key=lambda kv: -kv[1]):
        print(f"    {n:4d}  {k}")
    print(f"  court seats of MEDSL's within 10 counties of every county but not all (D3's near misses: OR 2024 positions 1 and 7 in 28 and 26 of 36; WA 2022 positions 1, 5 and 6 in 38 of 39, 3 seats each):")
    for cid, g, a, mags, t in sorted(near):
        print(f"    {cid[:80]}: {g} of {a} counties, magnitude {mags}, type {t}")
    print(f"  files read: " + "; ".join(f"{os.path.basename(p)} ({s['rows']:,} rows, sha256 {s['sha256'][:12]})" for p, s in sorted(summaries.items())))
    print(f"  State Board files read: " + "; ".join(f"{os.path.basename(p)} ({s['rows']:,} rows, sha256 {s['sha256'][:12]})" for p, s in sorted(nc_sum.items())))
    return summaries


# ---------------------------------------------------------------------------------------------- 36.3
def section_3(before, after, mv, summaries):
    print("### 36.3 the commission seats and Montana's clerk, by the source's own seat count")
    T = [r for r in mv["records"] if "T" in r[8] and r[4] == "statewide officer"]
    print(f"  T rows typed 'statewide officer': {len(T)} (D3: 16 = 14 commission seats + Montana's clerk 2)")
    for r in sorted(T, key=lambda r: r[0]):
        c = after[r[0]]
        st, year, date = c["place"]["state"], c["year"], c.get("date")
        paths = M.medsl_files(year, st)
        line = f"    {r[0][:70]}: {r[3]} -> {r[4]}"
        if not paths:
            print(line + "; file not fetched")
            continue
        s = summaries.get(paths[0]) or M.summary(paths[0], year)
        summaries[paths[0]] = s
        con, how = medsl_contest(c, s)
        allc = set(s["counties_all"].get(f"{st}|{date}", []))
        got, mags = set(), set()
        for v in con.values():
            got.update(v["counties"])
            mags.update(v["magnitudes"])
        print(line + f"; magnitude {sorted(mags)}; counties {len(got & allc)} of {len(allc)}; p {r[5]} -> {r[6]}")
    # commission contests of state scope that keep the board type
    keep = [c for c in after.values() if c.get("office_scope") == "state" and STATE_COMMISSION.search((c.get("office") or "").upper())
            and c.get("office_type") == "council, commission or board" and (c.get("result") or {}).get("source") == "medsl"]
    print(f"  state-scope commission contests that keep 'council, commission or board' at {AFTER} (changed files): {len(keep)}")
    tal = collections.Counter()
    for c in sorted(keep, key=lambda c: c["id"]):
        st, year, date = c["place"]["state"], c["year"], c.get("date")
        paths = M.medsl_files(year, st)
        if not paths:
            tal["file not fetched"] += 1
            continue
        s = summaries.get(paths[0]) or M.summary(paths[0], year)
        summaries[paths[0]] = s
        con, how = medsl_contest(c, s)
        allc = set(s["counties_all"].get(f"{st}|{date}", []))
        got, mags = set(), set()
        for v in con.values():
            got.update(v["counties"])
            mags.update(v["magnitudes"])
        whole = len(allc) > 1 and allc <= got
        k = seats_of(mags)
        why = ("not found" if not con else "no seat count in the file" if k is None else "more than one seat" if k > 1
               else "not every county" if not whole else "every county, one seat: DIFFERS")
        tal[why] += 1
        print(f"    {c['id'][:70]}: magnitude {sorted(mags)}, counties {len(got & allc)} of {len(allc)}: {why}")
    print(f"  why they keep it: {dict(tal)}")


# ---------------------------------------------------------------------------------------------- 36.4
def section_4(before, after, mv):
    print("### 36.4 the 21 lost p, by my own pool counts; the two Illinois strays")
    Lr = [r for r in mv["records"] if "L" in r[8]]
    print(f"  L rows: {len(Lr)} (D3: 21: 7 statewide judge, 12 judge, 2 held stray lines)")
    pa_m, pa_nc = C35.pools_at(AFTER)
    pb_m, pb_nc = C35.pools_at(BEFORE)
    tal = collections.Counter()
    for r in sorted(Lr, key=lambda r: r[0]):
        cid = r[0]
        a, b = after[cid], before[cid]
        m = REASON_N.search(r[6] or "")
        year = a["year"]
        if not m:
            print(f"    {cid[:70]}: p {r[5]} -> held: {(r[6] or '')[:90]}")
            tal["held (no class count)"] += 1
            continue
        n_rec, cls = int(m.group(1)), m.group(2)
        n_mine = C35.count_like(pa_m, cls, year)
        bcls = ((b.get("forecasts") or [{}])[-1].get("class")) or ""
        n_b = C35.count_like(pb_m, bcls, year) if bcls else None
        tal[f"{cls}: record {n_rec}, mine {n_mine} ({'equal' if n_rec == n_mine else 'DIFFERS'})"] += 1
        print(f"    {cid[:70]}: p {r[5]} -> none; class '{cls}' {n_rec} like races (mine {n_mine}); before: class '{bcls}' with {n_b} (mine) like races")
    print(f"  the counts: {dict(tal)}")
    # the Illinois strays in MEDSL's 2018 file
    paths = M.medsl_files(2018, "IL")
    if paths:
        rows = [r for r in M.rows(paths[0]) if (r.get("candidate") or "").strip().upper() == "MARY ARLINE VANN-METCALF"]
        print(f"  MEDSL 2018 Illinois ({os.path.basename(paths[0])}): rows naming MARY ARLINE VANN-METCALF: {len(rows)}")
        for r in rows:
            print(f"    office {r.get('office')!r}, district {r.get('district')!r}, county {r.get('county_name')!r} {r.get('county_fips')!r}, precinct {r.get('precinct')!r}, "
                  f"party {r.get('party_detailed')!r}, writein {r.get('writein')!r}, mode {r.get('mode')!r}, votes {r.get('votes')!r}, dataverse {r.get('dataverse')!r}")
        for cid in ("2018-local-IL-COMPTROLLER~2", "2018-local-IL-TREASURER~2"):
            a = after.get(cid) or {}
            print(f"    {cid}: type {a.get('office_type')}, p {C34.pval(a)!s:.100}; result {json.dumps(a.get('result'))[:160]}")
    else:
        print("  MEDSL 2018 Illinois: file not fetched")


# ---------------------------------------------------------------------------------------------- 36.5
def parse_pec(path):
    """the Secretary of State's Public Education Commission page: [{office, district, candidates, total, precincts}]
    (the patterns are copied from pipeline/intake/nm_sos.py parse at 8406745, so that the page is read the same way;
    nothing is imported)"""
    with open(path, encoding="utf-8", errors="replace") as f:
        s = f.read()
    blocks = re.split(r'<div class="display-results-box-a">\s*<h1>', s)[1:]
    out = []
    for b in blocks:
        title = html.unescape(b[:b.index("</h1>")]).strip()
        m = re.match(r"^(.*?)\s+DISTRICT\s+(\d+)$", title)
        cands = [{"name": " ".join(html.unescape(n).split()), "party": html.unescape(p).strip(), "votes": int(v.replace(",", ""))}
                 for n, p, v in re.findall(r'display-results-box-d">\s*<h1>([^<]*)</h1>\s*<h2[^>]*>([^<]*)</h2>.*?'
                                           r'display-results-box-f">\s*<h1>([\d,]+)</h1>', b, flags=re.S)]
        total = re.search(r'display-results-box-total">\s*<h2>([\d,]+)</h2>', b)
        prec = re.search(r"Precincts Fully:\s*([\d,]+)\s*/\s*([\d,]+)", b)
        out.append({"title": title, "office": m.group(1) if m else None, "district": m.group(2) if m else None, "candidates": cands,
                    "total": int(total.group(1).replace(",", "")) if total else None,
                    "precincts": [int(prec.group(1).replace(",", "")), int(prec.group(2).replace(",", ""))] if prec else None})
    return out


def section_5(after, summaries):
    print("### 36.5 New Mexico's 2022 Public Education Commissioners: the Secretary of State's page against the records")
    page = os.path.join(FIFTH, "nm_sos_pec_2022.html")
    arch = os.path.join(FIFTH, "nm_sos_archive_2022.html")
    idx = {k: (u, p, sha) for k, u, p, sha in [(x[0], x[4], x[5], x[6]) for x in (ln.split("\t") for ln in open(os.path.join(FIFTH, "index.txt"))) if len(x) >= 7]}
    for key in ("nm_sos:archive:2022", "nm_sos:pec:2022"):
        if key in idx:
            print(f"  {key}: {idx[key][0]} (sha256 {idx[key][2][:12]})")
    with open(arch, encoding="utf-8", errors="replace") as f:
        a = f.read()
    texts = [html.unescape(t).strip() for t in re.findall(r'href="https://electionresults\.sos\.nm\.gov/\?eid=2838"[^>]*>([^<]*)<', a)]
    print(f"  the archive page's link texts to eid 2838: {texts} (D3: '2022 General Election Official Results', linked twice)")
    con = parse_pec(page)
    print(f"  contests on the page: {len(con)} (D3: 5); titles {[c['title'] for c in con]}")
    recs = {c["place"].get("district"): c for c in after.values() if c["id"].startswith("2022-local-NM-PUBLIC_EDUCATION_COMMISSIONER")}
    print(f"  records at {AFTER}: {sorted(recs)} (by district)")
    tal = collections.Counter()
    nm_path = (M.medsl_files(2022, "NM") or [None])[0]
    medsl = {}
    if nm_path:
        s = summaries.get(nm_path) or M.summary(nm_path, 2022)
        summaries[nm_path] = s
        for k, v in s["state_contests"].items():
            if k.startswith("NM|2022-11-08|PUBLIC EDUCATION COMMISSIONER|"):
                print(f"  MEDSL's 2022 file ({os.path.basename(nm_path)}): contest key {k!r}: counties {len(v['counties'])}, precincts {v['precincts']}, magnitude {v['magnitudes']}, candidates {v['cands']}")
                medsl.update({n.upper(): x for n, x in v["cands"].items()})
    for c in con:
        r = recs.get(c["district"])
        if r is None:
            tal["no record for the district"] += 1
            continue
        rc = r["result"]["candidates"]
        names_ok = {x["name"].upper() for x in rc} == {x["name"].upper() for x in c["candidates"]}
        votes_ok = all(any(y["name"].upper() == x["name"].upper() and y["votes"] == x["votes"] for y in c["candidates"]) for x in rc)
        adds = c["total"] == sum(x["votes"] for x in c["candidates"])
        full = bool(c["precincts"]) and c["precincts"][0] == c["precincts"][1]
        mv_ok = all(medsl.get(n.upper()) == v for n, v in (r["result"].get("medsl_votes") or {}).items()) if medsl else None
        print(f"    district {c['district']}: page {[(x['name'], x['party'], x['votes']) for x in c['candidates']]}, total {c['total']} (adds up {adds}), precincts {c['precincts']} (all reported {full}); "
              f"record names equal {names_ok}, votes equal {votes_ok}, votes_source {r['result'].get('votes_source')}, medsl_votes {r['result'].get('medsl_votes')} "
              f"== MEDSL's own count {mv_ok}; counties {len(r['place'].get('counties') or [])}; p {C34.pval(r)}")
        tal["page and record agree" if names_ok and votes_ok and adds and full else "DIFFERS"] += 1
    print(f"  {dict(tal)}")


def main():
    print(f"##### c36 statewide judges, commission seats, the lost p and New Mexico's PEC (#88): HEAD {L.git_head()}")
    before, after, mv = section_1()
    summaries = section_2(before, after)
    section_3(before, after, mv, summaries)
    section_4(before, after, mv)
    section_5(after, summaries)


if __name__ == "__main__":
    main()
