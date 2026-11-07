"""pipeline/local_districts.py: Klarner's legislative districts beside MEDSL's, one by one, in every year both hold.

Written 2026-11-07 by worker D3 on the orchestrator's orders of 21:21 and 21:26. Reason (21:21): "n enters p, and an
opponent missing turns a real p into 0"; part 2 of the volume test (pipeline/local_volume.py) flags state-years, and
"a single bad district hides in the median" (M2's check c38 found two: Idaho 2022 Senate 1 and Vermont 2018
Chittenden). The orders:
  21:21 "Add two district-level checks across every Klarner-MEDSL overlap: (a) flag any district whose ratio is off 1
        by more than 3%; (b) flag any Klarner record coded uncontested where MEDSL shows another candidate with votes
        beyond scattered write-ins. Settle each by the state where it answers. Where it doesn't, use the 19:04 rules."
  21:26 "(1) A (b) flag where MEDSL's other candidate is a write-in, by MEDSL's write-in mark or the state's (W/I), is
        not a ballot opponent. Apply the existing write-in rule to it, as you did for Idaho SD1. The record stays
        uncontested only where that rule says so. (2) Settle a flag from the state only where its file is already
        cached or the state answers one request. Otherwise apply the 19:04 rules district by district: a gap of 5% or
        more is held, and a gap under 5% is kept with a note. (3) List every flag with its outcome: settled by the
        state, MEDSL taken (with its mark), held, noted, or write-in rule. Count the p moved, lost and gained by level
        and year. (4) Run the check across every overlap year, not only 2018 and 2022."
  19:04 (for a doubled count, New Hampshire 2022) "Use MEDSL's counts where every candidate matches by name, marked
        'Klarner's figures are doubled; MEDSL's counts'."

The overlap: Klarner's returns end in 2022; MEDSL's files hold a legislature in 2016 (its state file, as
local_volume.scan_2016 adds it up), 2018 and 2022 (2020's file is local offices only). Klarner's contests are read as
the build reads them before this check (NC's State Board counts, New Hampshire 2022, c38), so a district those fixes
settled is listed as settled, with its source.

Matching: a Klarner general contest is matched to the MEDSL contest of its state and chamber that names every one of
its named candidates by surname (MEDSL's district number, and in New Hampshire's House its county, decide between
several); its candidates are paired one to one by surname (and first initial where a surname repeats). A Klarner
contest that no MEDSL contest names in full is listed as unmatched and not tested.
  (a) the ratio: MEDSL's votes over Klarner's, the paired candidates added up; flagged off 1 by more than 3%.
  (b) a Klarner contest with no more names on the ballot than seats (pipeline/local.py structure: "unopposed") where
      MEDSL names another candidate with votes who is not a write-in total ("WRITE-IN", "SCATTERING").
Outcomes (OUTCOMES): settled earlier (a fix the build makes already), settled by the state (a file in the cache:
Idaho's 2022 canvass), MEDSL taken (Klarner's figures doubled to within 2%, every candidate paired, MEDSL naming no
other on the ballot: the 19:04 rule), write-in rule (a (b) flag whose other candidates are write-ins, added to the
contest as write-ins, party w, for pipeline/local.py's rule to read), held (a gap of 5% or more: |ratio - 1|, or for a
(b) flag the share of the district's votes MEDSL gives candidates Klarner lacks), noted (a gap under 5%).

Run:  VOTE_CACHE=/tmp/vote-cache python3 -I pipeline/local_districts.py check   (writes data/local/check-districts.json)
The build (pipeline/local.py load_klarner, district_checks) reads that file.
"""
import argparse
import collections
import glob
import io
import json
import os
import re
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fetch as F  # noqa: E402

REPO = os.path.dirname(HERE)
CHECK = os.path.join(REPO, "data", "local", "check-districts.json")
YEARS = (2016, 2018, 2022)
RATIO_OFF = 0.03      # (a): off 1 by more than this
HOLD_GAP = 0.05       # 19:04, district by district: held at this gap or more, noted under it
DOUBLE_TOL = 0.02     # Klarner's figures doubled: MEDSL's within 2% of half of them, every candidate
NORM = os.path.join(F.CACHE, "medsl", "normalized")
ID_CANVASS = os.path.join(F.CACHE, "id_sos", "raw", "2022_General_Canvass.zip")
WRITE_IN_MARK = re.compile(r"\(W/I\)|\bWRITE[- ]?IN\b", re.I)


def _sur(name):
    import local_medsl as M
    return M.name_key(name)[0]


def _surs(name):
    import local_medsl as M
    return {k[0] for k in M.name_keys(name)}


def medsl_contests(year):
    """MEDSL's general legislative contests of `year`: {state, sen, district, counties, candidates, file}."""
    import local_medsl as M
    import local_volume as V
    out = []
    if year == 2016:
        scan = V.scan_2016()
        groups = collections.defaultdict(list)
        for st, t in scan["leg"].items():
            for k, v in t.items():
                off, dist, cand, party, wi = k.split("|")
                groups[(st, 1 if "SENAT" in off else 0, dist)].append(
                    {"name": cand, "votes": v, "party": party or None, "writein": wi.upper() == "TRUE"})
        for (st, sen, dist), cs in groups.items():
            out.append({"state": st, "sen": sen, "district": dist, "counties": [], "candidates": _merge_lines(cs),
                        "file": scan["file"], "stage": "GEN"})
        return out
    for p in sorted(glob.glob(os.path.join(NORM, str(year), "*.jsonl"))):
        with open(p) as f:
            for line in f:
                m = M.relabel(json.loads(line))
                if m["office"] not in M.LEG or m["stage"] not in ("GEN", "GEN RECOUNT") or m["special"]:
                    continue
                out.append({"state": m["state"], "sen": M.LEG[m["office"]], "district": m["district"],
                            "counties": m.get("counties") or [], "candidates": _merge_lines(m["candidates"]),
                            "file": m["file"]["name"], "stage": m["stage"], "post": m.get("post"),
                            "magnitude": m.get("magnitude")})
    return out


GENERIC = re.compile(r"^\s*$|^OTHERS?$|\bALL OTHERS\b|SCATTER|\bVOIDS?\b|\bBLANKS?\b|FEDERAL BALLOTS|\bTOTALS?\b|"
                     r"OVER ?VOTES?|UNDER ?VOTES?|NONE OF THE|UNCOMMITTED|EXHAUSTED|\bUNRESOLVED\b|"
                     # New York's 2016 file carries its ballot kinds as lines of their own
                     r"^(AFFIDAVIT|FEDERAL|ABSENTEE(/MILITARY)?|MILITARY|MANUALLY COUNTED EMERGENCY|EMERGENCY|"
                     r"SPECIAL PRESIDENTIAL|PUBLIC COUNTER)$", re.I)


NOT_VOTES = re.compile(r"OVER ?VOTES?|UNDER ?VOTES?|\bBLANKS?\b|\bVOIDS?\b|\bTOTALS?\b|FEDERAL BALLOTS", re.I)


def _generic(x):
    """A line that is not a person: a write-in total ("WRITE-IN", "SCATTERING"), MEDSL's "ALL OTHERS", blanks, voids,
    totals, over- and undervotes."""
    import local_medsl as M
    n = x["name"].strip()
    return bool(GENERIC.search(n)) or (M._is_generic(n) and not re.search(r"[A-Z]{2,}\s+[A-Z]{2,}", re.sub(
        r"\(?W/I\)?|WRITE[- ]?INS?:?", "", n.upper())))


def _merge_lines(cands):
    """A candidate's lines (fusion parties, or a mode's) added up into one, by the name as written: Klarner gives
    each candidate once, its lines summed (the fusion rule of 19:04)."""
    out = {}
    for x in cands:
        k = " ".join(x["name"].upper().split())
        if k in out:
            out[k]["votes"] = (out[k]["votes"] or 0) + (x["votes"] or 0)
            out[k]["writein"] = out[k]["writein"] and bool(x.get("writein"))
            out[k]["lines"] += 1
        else:
            out[k] = {"name": x["name"], "votes": x["votes"] or 0, "party": x.get("party"),
                      "writein": bool(x.get("writein")), "lines": 1}
    return list(out.values())


def _is_write_in(x):
    return bool(x.get("writein")) or bool(WRITE_IN_MARK.search(x["name"]))


def match(kc, pool):
    """The MEDSL contests that name every named candidate of Klarner's contest kc."""
    import local as L
    import local_medsl as M
    named = [a for a in kc["cands"] if not a["scattering"]]
    ks = [_sur(a["name"]) for a in named]
    if not ks or not all(ks):
        return []
    hits = []
    for m in pool.get((kc["state"], kc["sen"]), []):
        ms = set()
        for x in m["candidates"]:
            ms |= _surs(x["name"])
        if all(s in ms for s in ks):
            hits.append(m)
    if len(hits) > 1 and str(kc["dno"]).isdigit():
        h = [m for m in hits if M.district_no(re.sub(r"\D", "", m["district"] or "") or None) == str(int(kc["dno"]))]
        hits = h or hits
    if len(hits) > 1 and kc["state"] == "NH" and kc["sen"] == 0:
        h = [m for m in hits if L.NH_COUNTY.get(kc["dname"]) in m["counties"]]
        hits = h or hits
    if len(hits) > 1:
        rc = [m for m in hits if m["stage"] == "GEN RECOUNT"]
        hits = rc if len(rc) == 1 else hits
    return hits


def pair(kc, m):
    """{id(Klarner candidate): MEDSL candidate}, one to one by surname (first initial where it repeats)."""
    import local_medsl as M
    named = [a for a in kc["cands"] if not a["scattering"]]
    left = [x for x in m["candidates"] if not _generic(x)]
    out = {}
    for a in sorted(named, key=lambda a: -(a["votes"] or 0)):
        s, i = M.name_key(a["name"])
        hit = [x for x in left if s in _surs(x["name"])]
        if len(hit) > 1:
            hit = [x for x in hit if M.name_key(x["name"])[1] == i] or hit
        if len(hit) > 1:   # one name in several lines (fusion, or a recount's): the line with the most votes
            hit = [max(hit, key=lambda x: x["votes"] or 0)]
        if not hit:
            return None
        out[id(a)] = hit[0]
        left.remove(hit[0])
    return out


def test(kc, m, pr=None, b_test=True):
    """The two tests on a matched pair: (a) the ratio, (b) another candidate beside an unopposed one (not where the
    MEDSL contest is shared by several districts: its other lines may be any of theirs)."""
    import local as L
    pr = pr if pr is not None else pair(kc, m)
    if pr is None:
        return {"matched": False}
    named = [a for a in kc["cands"] if not a["scattering"]]
    kv = sum(a["votes"] or 0 for a in named if a["votes"])
    mv = sum(pr[id(a)]["votes"] or 0 for a in named if a["votes"])
    used = {id(x) for x in pr.values()}
    others = [x for x in m["candidates"] if id(x) not in used and not _generic(x) and (x["votes"] or 0) > 0]
    # a name that is one of Klarner's in another line (a fusion line, a recount's line) is not another candidate
    ksur = {_sur(a["name"]) for a in named}
    others = [x for x in others if not (_surs(x["name"]) & ksur)]
    unopposed = len(L.on_ballot(kc["cands"])) <= (kc["eseats"] or 1)
    ratio = mv / kv if kv else None
    # MEDSL's write-in lines not paired (its write-in totals, scattering, and named write-ins): the scattering, should
    # MEDSL's counts be taken; over- and undervotes, blanks, voids and totals are no one's votes
    rest = [x for x in m["candidates"] if id(x) not in used and (_is_write_in(x) or re.search(
        r"SCATTER|WRITE[- ]?IN|^OTHERS?$|\bALL OTHERS\b", x["name"], re.I)) and not NOT_VOTES.search(x["name"])]
    return {"matched": True, "pairs": [[a["name"], a["votes"], pr[id(a)]["name"], pr[id(a)]["votes"]] for a in named],
            "klarner": kv, "medsl": mv, "ratio": None if ratio is None else round(ratio, 5),
            "flag_a": ratio is not None and abs(ratio - 1) > RATIO_OFF,
            "unopposed": unopposed,
            "others": [{"name": x["name"], "votes": x["votes"], "party": x.get("party"), "write_in": _is_write_in(x)}
                       for x in others],
            "flag_b": b_test and unopposed and bool(others), "b_tested": b_test,
            "medsl_ballot_unpaired": len([x for x in others if not _is_write_in(x)]),
            "medsl_write_ins": sum(x["votes"] or 0 for x in rest)}


COVER_GAP = 0.02      # the orchestrator, 22:26 (a): the chamber's rows missing beyond 2% of a county's precincts
COVER_VERSION = 4
COVER_YEARS = {2016: (2016, 2018), 2018: (2016, 2018), 2022: (2022, 2024), 2024: (2022, 2024)}   # MEDSL's files on the same lines


def _dkey(district):
    import local_medsl as M
    d = (district or "").strip().upper()
    return M.district_no(d) or d


def _coverage_file(path, year, out):
    """One raw MEDSL file's rows, county by county: the precincts with votes in each general contest, and for each
    chamber the precincts with its rows and the counties of each of its districts (into `out`)."""
    import local_medsl as M
    import local_volume as V
    import medsl_precinct as P
    per = collections.defaultdict(lambda: collections.defaultdict(set))   # (st, county) -> contest -> precincts
    rows_in = collections.defaultdict(lambda: collections.defaultdict(set))   # the same, rows with no votes too
    pv = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))   # votes by precinct
    for r in P._rows(path):
        if (r.get("stage") or "").upper() != "GEN" or (r.get("special") or "").upper() == "TRUE":
            continue
        cand = (r.get("candidate") or "").strip()
        if P.is_meta(cand):
            continue
        prec = r.get("precinct") or ""
        if V.AGG_NAME.search(prec) or P.COUNTY_TOTAL.search(prec.strip().upper()):
            continue
        st = r.get("state_po") or r.get("state_postal") or ""
        county = P.fips5(r.get("county_fips") or "")
        pk = (r.get("jurisdiction_fips") or r.get("jurisdiction") or "", prec)
        m = M.relabel({"office": (r.get("office") or "").strip().upper(), "district": r.get("district") or ""})
        try:
            v = int(float(r.get("votes") or 0))
        except ValueError:
            v = 0
        if m["office"] in M.LEG:
            sen, dk = M.LEG[m["office"]], _dkey(m["district"])
            if dk:   # a row with no district (MEDSL's 2016 Maricopa County rows) is no district's row
                out["districts"].setdefault(f"{st}|{sen}|{dk}", set()).add(county)
                per[(st, county)][("LEG", sen)].add(pk)
        else:
            k = (m["office"], r.get("district") or "", (r.get("dataverse") or "").upper())
            rows_in[(st, county)][k].add(pk)
            if v > 0:
                per[(st, county)][k].add(pk)
                if k[1].strip().upper() in ("", "STATEWIDE", "000"):   # a contest of the whole state, by its votes
                    pv[(st, county)][k][pk] += v
    if year in out["years_counted"]:
        # a contest with rows in at least 90% of its state's counties is statewide; a precinct of a county's top
        # contest with no row of any other contest (no district's row, no local one) is one whose district-level
        # rows the file lacks (MEDSL's 2024 Monroe County, New York: M2's seventh pass, the orchestrator, 22:19)
        n_c = collections.Counter(st for st, _ in rows_in)
        spread = collections.Counter((st, k) for (st, _), cs in rows_in.items() for k in cs)
        for (st, county), cs in per.items():
            tops = [k for k in cs if k[0] != "LEG"]
            top = max(tops, key=lambda k: len(cs[k])) if tops else None
            ps = cs[top] if top else set()
            rec = {"top": " ".join(x for x in top if x) if top else None, "precincts": len(ps)}
            for sen in (0, 1):
                have = cs.get(("LEG", sen), set())
                rec[("upper" if sen else "lower") + "_missing"] = len(ps - have)
            local = set().union(*[x for k, x in rows_in[(st, county)].items()
                                  if spread[(st, k)] < 0.9 * n_c[st]], cs.get(("LEG", 0), set()),
                                cs.get(("LEG", 1), set()))
            rec["only_statewide"] = len(ps - local)
            # the same by votes: the county's statewide contest with the most votes, its votes in those precincts
            vt = max(pv[(st, county)].values(), key=lambda x: sum(x.values()), default=collections.Counter())
            rec["top_votes"] = sum(vt.values())
            rec["only_statewide_votes"] = sum(v for q, v in vt.items() if q not in local)
            out["counties"][f"{st}|{county}"] = rec


def coverage(year):
    """MEDSL's own coverage of each chamber, county by county (the orchestrator, 2026-11-07 22:26 (a)): the precincts
    of the day's top contest in the county (the general contest with votes in the most precincts) that have no row of
    the chamber; and each district's counties, from every MEDSL file on the same lines (COVER_YEARS). Cached in
    $VOTE_CACHE/volume/normalized/coverage-<year>.json."""
    import local_volume as V
    files = []
    for y in COVER_YEARS[year]:
        if y == 2016:
            files.append((y, os.path.join(V.RAWDIR, V.STATE_2016)))
        else:
            files += [(y, p_) for _, p_ in V.raw_files(y) if p_]
    shas = []
    for _, p_ in files:
        with open(p_ + ".meta.json") as f:
            shas.append(json.load(f).get("sha256"))
    out_p = os.path.join(V.VNORM, f"coverage-{year}.json")
    if os.path.exists(out_p):
        with open(out_p) as f:
            d = json.load(f)
        if d.get("sha256s") == shas and d.get("version") == COVER_VERSION:
            return d
    out = {"districts": {}, "counties": {}, "years_counted": {year}}
    for y, p_ in files:
        _coverage_file(p_, y, out)
    d = {"version": COVER_VERSION, "sha256s": shas, "files": [os.path.basename(p_) for _, p_ in files],
         "districts": {k: sorted(v) for k, v in out["districts"].items()}, "counties": out["counties"]}
    with open(out_p, "w") as f:
        json.dump(d, f)
    return d


def district_cover(kc, m, year, cov, full_upper):
    """22:26 (a): the counties of MEDSL's district (from every MEDSL file on the same lines, and the contest's own)
    where MEDSL lacks the chamber's rows beyond 2% of the county's precincts: {"counties", "gaps": [[county,
    missing, precincts]], "by"}. A staggered upper chamber is read by the lower chamber's rows."""
    st, sen = kc["state"], kc["sen"]
    up_upper, up_lower = full_upper
    counties = set(cov["districts"].get(f"{st}|{sen}|{_dkey(m['district'])}", [])) | set(m.get("counties") or [])
    # the chamber's own rows; a staggered chamber by the other's, where that one is all up; neither all up: the day's
    # top contest stands in, and a county it lacks leaves the district untested (the orchestrator, 22:42 (3))
    own, other = (up_upper, up_lower) if sen else (up_lower, up_upper)
    ch = ("upper" if sen else "lower") if st in own else ("lower" if sen else "upper") if st in other else "top"
    gaps = []
    for county in sorted(counties):
        rec = cov["counties"].get(f"{st}|{county}")
        if rec is None:   # the county has no row of this year's file at all
            gaps.append([county, None, None])
            continue
        if ch != "top" and rec["precincts"] and rec[ch + "_missing"] / rec["precincts"] > COVER_GAP:
            gaps.append([county, rec[ch + "_missing"], rec["precincts"]])
    by = (f"the {ch} chamber's rows" + ("" if ch == ("upper" if sen else "lower") else
                                        f" (the {'upper' if sen else 'lower'} chamber is staggered)")
          if ch != "top" else "the day's top contest (neither chamber is all up)")
    return {"counties": sorted(counties), "gaps": gaps, "by": by, "untested": ch == "top" and bool(gaps)}


def klarner_id(kc):
    return f"{kc['year']}-{kc['state']}-{'upper' if kc['sen'] else 'lower'}-{kc['dname'] or ''}-{kc['dno'] or ''}" \
           f"-{kc['geopost'] or ''}-{kc['mmdpost'] or ''}"


def id_canvass():
    """Idaho's 2022 legislative canvass (pipeline/intake/id_sos.py's cached file): {district: {column: [(name,
    votes)]}} from each sheet 'Leg Dist N', its DIST. TOTAL row (a district of one county: its one CO. TOTAL row)."""
    import openpyxl
    if not os.path.exists(ID_CANVASS):
        return None
    with zipfile.ZipFile(ID_CANVASS) as z:
        name = next(n for n in z.namelist() if n.endswith("22 General Legislative - Precinct.xlsx"))
        wb = openpyxl.load_workbook(io.BytesIO(z.read(name)), read_only=True, data_only=True)
    out = {}
    for ws in wb.worksheets:
        mt = re.fullmatch(r"Leg Dist (\d+)", ws.title.strip())
        if not mt:
            continue
        rows = [r for r in ws.iter_rows(values_only=True)]
        hdr = next(i for i, r in enumerate(rows) if r and any(x in ("ST SEN", "ST REP A", "ST REP B") for x in r))
        names = next(r for r in rows[hdr:] if r and r[0] == "Precinct")
        tot = [r for r in rows if r and r[0] == "DIST. TOTAL"] or [r for r in rows if r and r[0] == "CO. TOTAL"]
        if len(tot) != 1:   # a district of several counties without its district's total row
            continue
        tot = tot[0]
        cols, cur = {}, None
        for j, h in enumerate(rows[hdr]):
            if h in ("ST SEN", "ST REP A", "ST REP B"):
                cur = h
            elif h is not None:
                cur = None
            if cur and j < len(names) and names[j]:
                cols.setdefault(cur, []).append((str(names[j]).strip(), int(tot[j] or 0)))
        out[mt.group(1)] = cols
    return out


def settle_id(kc, t, canv):
    """Idaho 2022 from the state's canvass: the column naming Klarner's candidates; its counts and its write-in
    marks."""
    named = [a for a in kc["cands"] if not a["scattering"]]
    ks = {_sur(a["name"]) for a in named}
    d = canv.get(str(int(kc["dno"]))) if str(kc["dno"]).isdigit() else None
    if not d:
        return None
    want = ["ST SEN"] if kc["sen"] else ["ST REP A", "ST REP B"]
    cols = [(c, d[c]) for c in want if c in d and ks <= {_sur(n.replace("(W/I)", "")) for n, _ in d[c]}]
    if len(cols) != 1:
        return None
    col, cs = cols[0]
    with open(ID_CANVASS + ".meta.json") as f:
        meta = json.load(f)
    return {"column": col, "file": f"{os.path.basename(ID_CANVASS)} / 22 General Legislative - Precinct.xlsx / "
                                   f"Leg Dist {int(kc['dno'])}", "url": meta["url"], "read_utc": meta["read_utc"],
            "sha256": meta["sha256"],
            "candidates": [{"name": n.replace("(W/I)", "").strip(), "votes": v, "write_in": "(W/I)" in n}
                           for n, v in cs]}


def check():
    import local as L
    cs = L.load_klarner(raw=True)
    cs = L.c38(L.nh_2022(L.certified_votes(cs)))
    canv = id_canvass()
    out = {"about": ("Klarner's legislative districts beside MEDSL's, one by one (pipeline/local_districts.py; the "
                     "orchestrator's orders of 2026-11-07 21:21 and 21:26; data/local/REPORT.md section 32)"),
           "rules": {"ratio_off_over": RATIO_OFF, "held_at_or_over": HOLD_GAP, "doubled_within": DOUBLE_TOL},
           "years": {}}
    ups = {sen: collections.Counter((st, y) for st, y, _, _ in {(c["state"], c["year"], c["dname"], c["dno"])
                                                                for c in cs if c["etype"] == "g" and c["sen"] == sen})
           for sen in (0, 1)}

    def all_up(sen, year):   # a chamber with all its seats up: its districts this year at least 90% of its most
        u = ups[sen]
        return {st for (st, y) in u if y == year and u[(st, y)] >= 0.9 * max(u.get((st, y_), 0)
                                                                              for y_ in range(2012, 2023, 2))}
    for year in YEARS:
        cov = coverage(year)
        # an upper chamber with all its seats up this year (its districts this year at least 90% of its most in
        # 2012-2022); one that is staggered leaves whole districts without a row, so the lower chamber's rows stand
        # in for the file's coverage of each county
        full_upper = (all_up(1, year), all_up(0, year))
        status = {}
        pool = collections.defaultdict(list)
        for m in medsl_contests(year):
            pool[(m["state"], m["sen"])].append(m)
        states = {k[0] for k in pool}
        tallies, flags = collections.Counter(), []
        found = []
        for kc in cs:
            if kc["year"] != year or kc["etype"] != "g" or kc["state"] not in states:
                continue
            hits = match(kc, pool)
            if len(hits) != 1:
                tallies["unmatched" if not hits else "matched to several"] += 1
                status[klarner_id(kc)] = ["unmatched" if not hits else "matched to several"]
                continue
            found.append((kc, hits[0]))
        # a MEDSL contest that several of Klarner's districts match (a county's lines filed as one district, as in
        # MEDSL's 2016 New Hampshire House) is no one district's count: those are not tested
        groups = collections.defaultdict(list)
        for kc, m in found:
            groups[id(m)].append(kc)
        shared = collections.Counter()
        for kc, m in found:
            pr, b_test = None, True
            if len(groups[id(m)]) > 1:   # several districts' lines filed as one contest (posts, seats A and B, a
                # county): each tested on its own candidates for (a) where every district's pairs are apart
                prs = [pair(k_, m) for k_ in groups[id(m)]]
                lines = [id(x) for p_ in prs if p_ for x in p_.values()]
                if any(p_ is None for p_ in prs) or len(lines) != len(set(lines)):
                    tallies["a MEDSL contest that several districts match, not paired apart"] += 1
                    shared[kc["state"]] += 1
                    status[klarner_id(kc)] = ["shared, not paired apart", m["district"]]
                    continue
                pr, b_test = prs[groups[id(m)].index(kc)], False
                tallies["shared: (a) only"] += 1
            t = test(kc, m, pr, b_test)
            if not t["matched"]:
                tallies["candidates not paired"] += 1
                status[klarner_id(kc)] = ["candidates not paired", m["district"]]
                continue
            tallies["tested"] += 1
            status[klarner_id(kc)] = ["tested", m["district"], t["klarner"], t["medsl"],
                                      (kc.get("votes_source") or {}).get("source")]
            if not (t["flag_a"] or t["flag_b"]):
                continue
            f = {"id": klarner_id(kc), "state": kc["state"], "chamber": "state-upper" if kc["sen"] else "state-lower",
                 "dname": kc["dname"] or None, "dno": kc["dno"] or None, "post": kc["geopost"] or kc["mmdpost"] or None,
                 "eseats": kc["eseats"], "medsl_district": m["district"], "medsl_file": m["file"],
                 "flags": [x for x, y in (("a", t["flag_a"]), ("b", t["flag_b"])) if y], **t}
            f.update(outcome(kc, t, year, canv, district_cover(kc, m, year, cov, full_upper)))
            flags.append(f)
            tallies[f"flag {'+'.join(f['flags'])}: {f['outcome']}"] += 1
        out["years"][str(year)] = {"tallies": dict(sorted(tallies.items())), "shared_by_state": dict(sorted(shared.items())),
                                   "flags": sorted(flags, key=lambda f: (f["state"], f["chamber"], f["id"]))}
        print(year, dict(sorted(tallies.items())))
        import local_volume as V
        with open(os.path.join(V.VNORM, f"districts-status-{year}.json"), "w") as f:
            json.dump(status, f)
    # 22:19: the counties whose district-level and local rows MEDSL's file lacks, for the contests MEDSL's counts are
    # shown for (local_medsl.coverage_gate); 2020's file holds local offices only, with no statewide contest to read by
    out["incomplete_counties"] = {}
    for year in (2018, 2022, 2024):
        cov = coverage(year)
        out["incomplete_counties"][str(year)] = {
            k: {"only_statewide": v["only_statewide"], "precincts": v["precincts"],
                "only_statewide_votes": v["only_statewide_votes"], "top_votes": v["top_votes"], "top": v["top"]}
            for k, v in sorted(cov["counties"].items())
            if v["top_votes"] and v["only_statewide_votes"] / v["top_votes"] > COVER_GAP}
    out["incomplete_counties"]["about"] = (
        "counties where precincts holding more than 2% of the votes of the county's statewide contest with the most "
        "votes have no row of any other contest (a contest with rows in 90% of the state's counties is statewide): "
        "their district-level and local rows are missing (M2 measured Monroe's by its presidential vote, 29.0%); read "
        "by votes, not precinct counts, so that one small precinct of federal-only ballots does not hold a county "
        "[worker D3's reading]; 2020 untested: MEDSL's file holds local offices only")
    with open(CHECK, "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
        f.write("\n")
    return out


def outcome(kc, t, year, canv, cover=None):
    """The outcome of a flagged district (OUTCOMES in the module's docstring), and what the build does."""
    src = (kc.get("votes_source") or {}).get("source")
    if src:
        return {"outcome": "settled earlier", "by": src}
    if kc.get("held_reason"):   # held by an earlier rule (New Hampshire 2022's names, nh_2022)
        return {"outcome": "settled earlier", "by": "held"}
    if kc["state"] == "ID" and year == 2022 and canv:
        s = settle_id(kc, t, canv)
        if s:
            return {"outcome": "settled by the state", "by": "Idaho's 2022 canvass (cached)", "state_count": s}
    r = t["ratio"]
    ballot_others = [x for x in t["others"] if not x["write_in"]]
    voted = [p for p in t["pairs"] if p[1]]
    if t["flag_a"] and r is not None and len(voted) >= 2 and not ballot_others and \
            all(abs(p[3] / p[1] - 0.5) <= 0.5 * DOUBLE_TOL for p in voted):   # one candidate at half is no pattern
        return {"outcome": "MEDSL taken", "mark": "Klarner's figures are doubled; MEDSL's counts"}
    gaps, uncovered = [], None
    if cover is not None and cover.get("untested"):   # 22:42 (3): neither chamber all up, the file lacks a county
        return {"outcome": "untested: MEDSL's file does not cover the district", "coverage": cover}
    if t["flag_a"] and r < 1 and cover is not None and cover["gaps"]:
        # 22:26 (b): MEDSL lacks the chamber's rows in part of the district, which explains a Klarner count above
        # MEDSL's; (c) a Klarner count below MEDSL's partial count is not explained so, and goes on to the gap rule
        uncovered = cover
    elif t["flag_a"]:
        gaps.append(abs(r - 1))
    if t["flag_b"] and ballot_others:
        tot = t["medsl"] + sum(x["votes"] for x in t["others"])
        gaps.append(sum(x["votes"] for x in ballot_others) / tot if tot else 1.0)
    if uncovered and not gaps:
        return {"outcome": "kept: MEDSL does not cover the district", "coverage": uncovered}
    if not gaps:   # a (b) flag whose others are all write-ins
        return {"outcome": "write-in rule"}
    g = max(gaps)
    out = {"outcome": "held" if g >= HOLD_GAP else "noted", "gap": round(g, 5),
           "write_ins_added": bool(t["flag_b"] and any(x["write_in"] for x in t["others"]))}
    if uncovered:
        out["coverage"] = uncovered
    if cover is not None:
        out["covered"] = not cover["gaps"]
    return out


COMPARE = os.path.join(REPO, "data", "local", "check-districts-m2.json")


def compare(m2_path):
    """22:19 item 2: M2's list of Klarner districts 5% or more off MEDSL (checks/m2/c38-districts.json, M2's seventh
    pass) beside these checks' flags, each difference with its reason. Reads check-districts.json and the per-contest
    statuses check() leaves in the cache."""
    import local as L
    import local_volume as V
    with open(m2_path) as f:
        m2 = json.load(f)["districts"]
    with open(CHECK) as f:
        chk = json.load(f)
    kl = {klarner_id(c): c for c in L.c38(L.nh_2022(L.certified_votes(L.load_klarner(raw=True))))
          if c["etype"] == "g"}
    flags = {f["id"]: f for v in chk["years"].values() for f in v["flags"]}
    status = {}
    for y in YEARS:
        with open(os.path.join(V.VNORM, f"districts-status-{y}.json")) as f:
            status.update(json.load(f))

    def ids(r):
        code = " ".join(r["klarner_code"].split()).lower()
        return sorted(k for k, c in kl.items() if c["year"] == r["year"] and c["state"] == r["state"]
                      and ("state-upper" if c["sen"] else "state-lower") == r["chamber"]
                      and " ".join(f"{c['dname'] or ''} {c['dno'] or ''}".split()).lower() == code)
    rows, tally, seen = [], collections.Counter(), set()
    for r in m2:
        mine = ids(r)
        seen.update(mine)
        got = [flags[k] for k in mine if k in flags]
        if got:
            why = "flagged here too: " + "; ".join(f"{f['id']} ({'+'.join(f['flags'])}, {f['outcome']})" for f in got)
            kind = "both"
        elif not mine:
            why, kind = "no Klarner general contest of that code here", "M2 only: no contest"
        else:
            st_ = [status.get(k) for k in mine]
            if any(x and x[0] == "tested" and x[4] for x in st_):
                kind = "M2 only: settled before this check"
                why = "a fix the build makes already, before this check reads the contest (" + ", ".join(
                    sorted({x[4] for x in st_ if x and x[0] == "tested" and x[4]})) + "); M2 reads Klarner's raw file"
            elif any(x and x[0] == "tested" for x in st_):
                x = next(x for x in st_ if x and x[0] == "tested")
                kind = "M2 only: within 3% here"
                why = (f"tested here on the named candidates matched by surname: Klarner {x[2]:,}, MEDSL {x[3]:,} "
                       f"(district {x[1]!r}); M2 reads MEDSL's rows of the district's code ({r['by']}): "
                       f"{r['medsl']:,} against Klarner's {r['klarner']:,}")
            elif any(x is None for x in st_):
                kind = "M2 only: not tested here"
                why = ("not among the contests tested: its state has no legislative contest in MEDSL's file this "
                       "year by this check's reading, or the contest was held earlier")
                if any(kl[k].get("held_reason") for k in mine):
                    kind, why = "M2 only: held before this check", "held by an earlier rule (nh_2022)"
            else:
                kind = "M2 only: " + st_[0][0]
                why = {"unmatched": "no MEDSL contest of its chamber names all its candidates by surname, so it is "
                                    "untested here (22:26 (e)); M2 matches by the district's code",
                       "matched to several": "several MEDSL contests name all its candidates; untested here",
                       "shared, not paired apart": "MEDSL files several districts' lines as one contest whose "
                                                   "candidates do not pair apart; untested here",
                       "candidates not paired": "its candidates do not pair one to one; untested here"}.get(
                    st_[0][0], st_[0][0])
        tally[kind] += 1
        rows.append({"year": r["year"], "state": r["state"], "chamber": r["chamber"], "district": r["klarner_code"],
                     "m2": {"klarner": r["klarner"], "medsl": r["medsl"], "off": r["off"], "by": r["by"]},
                     "ids": mine, "here": kind, "reason": why})
    only_here = collections.Counter()
    for k, f in flags.items():
        if k in seen:
            continue
        a = f["ratio"] is not None and abs(f["ratio"] - 1) >= 0.05
        only_here[f"{k[:4]}: " + ("(a) off 5% or more on the named candidates; M2's by D+R or every vote, or "
                                  "matched by code" if a and "a" in f["flags"] else
                                  "(a) off 3% to 5%, under M2's line" if "a" in f["flags"] else
                                  "(b) only: M2 does not test an uncontested record")] += 1
    out = {"about": ("M2's list of Klarner districts 5% or more off MEDSL (checks/m2/c38-districts.json) beside "
                     "data/local/check-districts.json (the orchestrator, 2026-11-07 22:19, item 2)"),
           "tally": dict(sorted(tally.items())), "flags_not_on_m2s_list": dict(sorted(only_here.items())),
           "m2": rows}
    with open(COMPARE, "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(json.dumps(out["tally"], indent=1), json.dumps(out["flags_not_on_m2s_list"], indent=1))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["check", "compare"])
    ap.add_argument("--m2", default=os.path.join(REPO, "checks", "m2", "c38-districts.json"))
    a = ap.parse_args()
    if a.cmd == "check":
        check()
    else:
        compare(a.m2)


if __name__ == "__main__":
    main()
