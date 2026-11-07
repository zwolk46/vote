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
                     r"OVER ?VOTES?|UNDER ?VOTES?|NONE OF THE|UNCOMMITTED|EXHAUSTED|\bUNRESOLVED\b", re.I)


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
    return {"matched": True, "pairs": [[a["name"], a["votes"], pr[id(a)]["name"], pr[id(a)]["votes"]] for a in named],
            "klarner": kv, "medsl": mv, "ratio": None if ratio is None else round(ratio, 5),
            "flag_a": ratio is not None and abs(ratio - 1) > RATIO_OFF,
            "unopposed": unopposed,
            "others": [{"name": x["name"], "votes": x["votes"], "party": x.get("party"), "write_in": _is_write_in(x)}
                       for x in others],
            "flag_b": b_test and unopposed and bool(others), "b_tested": b_test,
            "medsl_ballot_unpaired": len([x for x in others if not _is_write_in(x)])}


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
    return {"column": col, "candidates": [{"name": n.replace("(W/I)", "").strip(), "votes": v,
                                            "write_in": "(W/I)" in n} for n, v in cs]}


def check():
    import local as L
    cs = L.load_klarner(raw=True)
    cs = L.c38(L.nh_2022(L.certified_votes(cs)))
    canv = id_canvass()
    out = {"about": ("Klarner's legislative districts beside MEDSL's, one by one (pipeline/local_districts.py; the "
                     "orchestrator's orders of 2026-11-07 21:21 and 21:26; data/local/REPORT.md section 32)"),
           "rules": {"ratio_off_over": RATIO_OFF, "held_at_or_over": HOLD_GAP, "doubled_within": DOUBLE_TOL},
           "years": {}}
    for year in YEARS:
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
                    continue
                pr, b_test = prs[groups[id(m)].index(kc)], False
                tallies["shared: (a) only"] += 1
            t = test(kc, m, pr, b_test)
            if not t["matched"]:
                tallies["candidates not paired"] += 1
                continue
            tallies["tested"] += 1
            if not (t["flag_a"] or t["flag_b"]):
                continue
            f = {"id": klarner_id(kc), "state": kc["state"], "chamber": "state-upper" if kc["sen"] else "state-lower",
                 "dname": kc["dname"] or None, "dno": kc["dno"] or None, "post": kc["geopost"] or kc["mmdpost"] or None,
                 "eseats": kc["eseats"], "medsl_district": m["district"], "medsl_file": m["file"],
                 "flags": [x for x, y in (("a", t["flag_a"]), ("b", t["flag_b"])) if y], **t}
            f.update(outcome(kc, t, year, canv))
            flags.append(f)
            tallies[f"flag {'+'.join(f['flags'])}: {f['outcome']}"] += 1
        out["years"][str(year)] = {"tallies": dict(sorted(tallies.items())), "shared_by_state": dict(sorted(shared.items())),
                                   "flags": sorted(flags, key=lambda f: (f["state"], f["chamber"], f["id"]))}
        print(year, dict(sorted(tallies.items())))
    with open(CHECK, "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
        f.write("\n")
    return out


def outcome(kc, t, year, canv):
    """The outcome of a flagged district (OUTCOMES in the module's docstring), and what the build does."""
    src = (kc.get("votes_source") or {}).get("source")
    if src:
        return {"outcome": "settled earlier", "by": src}
    if kc["state"] == "ID" and year == 2022 and canv:
        s = settle_id(kc, t, canv)
        if s:
            return {"outcome": "settled by the state", "by": "Idaho's 2022 canvass (cached)", "state_count": s}
    r = t["ratio"]
    ballot_others = [x for x in t["others"] if not x["write_in"]]
    if "a" in [x for x, y in (("a", t["flag_a"]),) if y] and r is not None and \
            all(p[1] and abs(p[3] / p[1] - 0.5) <= 0.5 * DOUBLE_TOL for p in t["pairs"] if p[1]) and not ballot_others:
        return {"outcome": "MEDSL taken", "mark": "Klarner's figures are doubled; MEDSL's counts"}
    gaps = []
    if t["flag_a"]:
        gaps.append(abs(r - 1))
    if t["flag_b"] and ballot_others:
        tot = t["medsl"] + sum(x["votes"] for x in t["others"])
        gaps.append(sum(x["votes"] for x in ballot_others) / tot if tot else 1.0)
    if not gaps:   # a (b) flag whose others are all write-ins
        return {"outcome": "write-in rule"}
    g = max(gaps)
    return {"outcome": "held" if g >= HOLD_GAP else "noted", "gap": round(g, 5),
            "write_ins_added": bool(t["flag_b"] and any(x["write_in"] for x in t["others"]))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["check"])
    ap.parse_args()
    check()


if __name__ == "__main__":
    main()
