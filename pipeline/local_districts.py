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
Since 2026-11-13 (data/local/REPORT.md sections 34 and 35): settled by the state, Klarner's or MEDSL's count standing
(the state's count within 3% of one of them, candidate by candidate: settle_agree), settled by the county (COUNTY_READ),
MEDSL taken or held over seats times the ballots (over_seats_pass, every tested record in a district MEDSL's file
covers), held where the ballot is not read (BALLOT_UNREAD), and, beside the flags, two counts against the state's
(two_against_state: Klarner's and MEDSL's within 0.4% of each other, the state's unmarked count off).

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
            named = [x for x in cs if x["name"].strip() or not (x["party"] or "").strip()]
            nameless = [{"party": x["party"], "votes": x["votes"], "counties": []} for x in cs
                        if not x["name"].strip() and (x["party"] or "").strip()]
            out.append({"state": st, "sen": sen, "district": dist, "counties": [],
                        "candidates": _attach_nameless(_merge_lines(named), nameless),
                        "file": scan["file"], "stage": "GEN"})
        return merge_spellings(year, out)
    nl = nameless_lines(year)
    for p in sorted(glob.glob(os.path.join(NORM, str(year), "*.jsonl"))):
        with open(p) as f:
            for line in f:
                m = M.relabel(json.loads(line))
                if m["office"] not in M.LEG or m["stage"] not in ("GEN", "GEN RECOUNT") or m["special"]:
                    continue
                lines = nl.get(f"{m['state']}|{M.LEG[m['office']]}|{_dkey(m['district'])}", [])
                out.append({"state": m["state"], "sen": M.LEG[m["office"]], "district": m["district"],
                            "counties": sorted(set(m.get("counties") or []) | {c for x in lines for c in x["counties"]
                                                                                 if x.get("attached")}),
                            "candidates": _attach_nameless(_merge_lines(m["candidates"]), lines),
                            "file": m["file"]["name"], "stage": m["stage"], "post": m.get("post"),
                            "magnitude": m.get("magnitude")})
    return merge_spellings(year, out)


def _attach_nameless(cands, lines):
    """MEDSL's lines with a party and no name added to the one candidate of the contest who holds that party (the
    orchestrator, 2026-11-13: "a nameless line whose party is held by one candidate in the contest matches that
    candidate"); a line whose party no candidate, or several, hold is left out, as a nameless line was before. Each
    line is marked attached or not, and the candidate keeps what was added (nameless_added)."""
    for x in lines:
        hold = [c for c in cands if (c.get("party") or "").strip().upper() == x["party"].strip().upper()
                and c["name"].strip() and not c.get("writein")]
        x["attached"] = len(hold) == 1
        if x["attached"]:
            c = hold[0]
            c["votes"] = (c["votes"] or 0) + x["votes"]
            c["lines"] += 1
            c.setdefault("nameless_added", []).append([x["party"], x["votes"], x["counties"]])
    return cands


def nameless_lines(year):
    """MEDSL's legislative lines with a party and no candidate's name, from each raw file of `year` (the normalized
    files leave them out, as lines that name no one): {"ST|sen|district key": [{party, votes, counties}]}, a precinct's
    votes its TOTAL mode's or its other modes' sum, whichever is more. Cached in $VOTE_CACHE/volume/normalized/
    nameless-<year>.json by the files' sha256."""
    import local_medsl as M
    import local_volume as V
    import medsl_precinct as P
    files = [p_ for _, p_ in V.raw_files(year) if p_]
    shas = []
    for p_ in files:
        with open(p_ + ".meta.json") as f:
            shas.append(json.load(f).get("sha256"))
    cp = os.path.join(V.VNORM, f"nameless-{year}.json")
    if os.path.exists(cp):
        with open(cp) as f:
            d = json.load(f)
        if d.get("sha256s") == shas:
            return d["lines"]
    tot = collections.defaultdict(collections.Counter)
    oth = collections.defaultdict(collections.Counter)
    for p_ in files:
        for r in P._rows(p_):
            if (r.get("candidate") or "").strip() or (r.get("stage") or "").upper() not in ("GEN", "GEN RECOUNT") or \
                    (r.get("special") or "").strip().upper() == "TRUE":
                continue
            party = (r.get("party_simplified") or "").strip()
            if not party:
                continue
            m = M.relabel({"office": (r.get("office") or "").strip().upper(), "district": r.get("district") or ""})
            if m["office"] not in M.LEG or not _dkey(m["district"]):
                continue
            st = r.get("state_po") or r.get("state_postal") or ""
            county = P.fips5(r.get("county_fips") or "")
            k = (f"{st}|{M.LEG[m['office']]}|{_dkey(m['district'])}", party, county, r.get("jurisdiction_fips") or "",
                 _pnorm(r.get("precinct") or ""))
            try:
                v = int(float(r.get("votes") or 0))
            except ValueError:
                v = 0
            (tot if (r.get("mode") or "").strip().upper() == "TOTAL" else oth)[k[:2]][k[2:]] += v
    lines = collections.defaultdict(list)
    for kp in sorted(set(tot) | set(oth)):
        ps = set(tot[kp]) | set(oth[kp])
        v = sum(max(tot[kp].get(q, 0), oth[kp].get(q, 0)) for q in ps)
        if v:
            lines[kp[0]].append({"party": kp[1], "votes": v, "counties": sorted({q[0] for q in ps})})
    with open(cp, "w") as f:
        json.dump({"sha256s": shas, "lines": lines}, f)
    return lines


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


# ------------------------------------------------------------------ one candidate under two spellings
# The orchestrator, 2026-11-13 04:44: "Two spellings of one name: agreed for the next step. Sum the lines where their
# precincts are apart and the names share a surname and a given name, and list each pair. A name split by county is
# one candidate's count." Reason: MEDSL spells one candidate one way in one county's rows and another way in the next
# (New York 2016's Senate 58: "Leslie Burke" 35,115 and "Leslie Danks Burke" 17,371, Klarner 52,488), and the pairing
# took the larger line alone (data/local/REPORT.md sections 34 and 35).
SPELL_VERSION = 1
NOT_GIVEN = {"JR", "SR", "II", "III", "IV", "MR", "MRS", "MS", "DR"}
NOT_PERSON = re.compile(r"\d|\bVOTES?\b|QUALIFIED", re.I)
SPELLINGS = {}   # year -> every pair found, with what was decided (written into check-districts.json)


def _given(name):
    """A name's given names and nicknames, two letters or more: "Mary L. (Mimi) Pruett" gives MARY and MIMI,
    "Alley, Larry W." gives LARRY; the surname and a suffix are left out."""
    n = re.sub(r'"+', '"', name.upper())
    toks = set()
    for a, b, c in re.findall(r"\(([^)]*)\)|\"([^\"]*)\"|'([^']*)'", n):
        toks |= set(re.findall(r"[A-Z]{2,}", a or b or c))
    rest = re.sub(r"\([^)]*\)|\"[^\"]*\"|'[^']*'", " ", n)
    rest = rest.split(",", 1)[1] if "," in rest else " ".join(rest.split()[:-1])
    return (toks | set(re.findall(r"[A-Z]{2,}", rest))) - NOT_GIVEN


def _spelled_alike(a, b):
    """Two named lines that may be one candidate: their names differ as written, and share a surname (any of their
    surname keys, local_medsl.name_keys) and a given name or nickname (_given)."""
    if " ".join(a["name"].upper().split()) == " ".join(b["name"].upper().split()):
        return False
    if any(_generic(x) or NOT_PERSON.search(x["name"]) or not x["name"].strip() for x in (a, b)):
        return False
    return bool(_surs(a["name"]) & _surs(b["name"])) and bool(_given(a["name"]) & _given(b["name"]))


def _spell_key(st, sen, district, name):
    return f"{st}|{sen}|{_dkey(district or '')}|{' '.join(name.upper().split())}"


def spelling_precincts(year, contests):
    """{_spell_key: {precinct: votes}} for every line of a pair spelled alike in `year`'s legislative contests, read
    from MEDSL's raw files (the 2016 state file; 2018's and 2022's state files): the precincts where the line has
    votes. Cached in $VOTE_CACHE/volume/normalized/spellings-<year>.json, keyed by the raw files' sha256."""
    import local_volume as V
    import medsl_precinct as P
    want = collections.defaultdict(set)
    for m in contests:
        cs = m["candidates"]
        for i, a in enumerate(cs):
            for b in cs[i + 1:]:
                if _spelled_alike(a, b):
                    want[m["state"]] |= {_spell_key(m["state"], m["sen"], m["district"], x["name"]) for x in (a, b)}
    if not want:
        return {}
    paths = ({st: os.path.join(V.RAWDIR, V.STATE_2016) for st in want} if year == 2016 else
             {st: V._raw_path(year, st) for st in want})
    shas = {}
    for st, p_ in sorted(paths.items()):
        with open(p_ + ".meta.json") as f:
            shas[st] = json.load(f).get("sha256")
    wanted = {k: sorted(v) for k, v in sorted(want.items())}
    cache = os.path.join(V.VNORM, f"spellings-{year}.json")
    if os.path.exists(cache):
        with open(cache) as f:
            d = json.load(f)
        if (d.get("version"), d.get("sha256"), d.get("want")) == (SPELL_VERSION, shas, wanted):
            return d["precincts"]
    out = collections.defaultdict(lambda: collections.defaultdict(dict))
    for p_ in sorted(set(paths.values())):
        for r in P._rows(p_):
            st = r.get("state_po") or r.get("state_postal")
            if st not in want or (r.get("stage") or "GEN").upper() != "GEN" or (r.get("special") or "").upper() == "TRUE":
                continue
            o = (r.get("office") or "").upper()
            if not re.search(r"STATE (HOUSE|SENATE|REPRESENTATIVE|SENATOR|ASSEMBLY)|GENERAL ASSEMBLY", o):
                continue
            k = _spell_key(st, 1 if "SENAT" in o else 0, r.get("district"), r.get("candidate") or "")
            if k not in want[st]:
                continue
            try:
                v = int(float(r.get("votes") or 0))
            except ValueError:
                v = 0
            pk = "|".join(str(x or "") for x in (r.get("county_fips"), r.get("jurisdiction_fips") or
                                                 r.get("jurisdiction"), r.get("precinct")))
            mode = (r.get("mode") or "TOTAL").upper()
            out[k][pk][mode] = out[k][pk].get(mode, 0) + v
    res = {k: {pk: P.resolve(m) for pk, m in pp.items()} for k, pp in out.items()}
    os.makedirs(V.VNORM, exist_ok=True)
    with open(cache, "w") as f:
        json.dump({"version": SPELL_VERSION, "sha256": shas, "want": wanted, "precincts": res}, f)
    return res


def merge_spellings(year, contests):
    """Each contest's lines spelled alike (_spelled_alike) summed into one where their precincts are apart: no precinct
    gives both lines votes. A precinct is a row of MEDSL's raw file with votes for the line, its name not one that
    reads as a total (local_volume.AGG_NAME: Kentucky 2016's Jefferson County files a row named "Cumulative:" that
    repeats one walk-in row under the other spelling, Jason Michael NEMES 487 beside Jason Nemes's "WALK-IN 3RD F-G"
    487 [measured]). A group of more than two spellings is summed only where every pair in it is apart. The summed
    line keeps the larger line's name and party and lists its spellings (`spellings`). In place; every pair found is
    listed in SPELLINGS[year] with what was decided."""
    import local_volume as V
    pre = spelling_precincts(year, contests)
    found = []
    for m in contests:
        cs = m["candidates"]
        pairs = [(a, b) for i, a in enumerate(cs) for b in cs[i + 1:] if _spelled_alike(a, b)]
        if not pairs:
            continue

        def where(x):
            pp = pre.get(_spell_key(m["state"], m["sen"], m["district"], x["name"])) or {}
            return {pk for pk, v in pp.items() if v and not V.AGG_NAME.search(pk.split("|", 2)[2])}, pp
        groups = []   # the lines the pairs connect
        for a, b in pairs:
            g = [x for x in groups if any(y is a or y is b for y in x)]
            new = [a, b] + [y for x in g for y in x]
            groups = [x for x in groups if not any(x is y for y in g)] + [list({id(y): y for y in new}.values())]
        for g in groups:
            sets = {id(x): where(x) for x in g}
            why = None
            if any(not sets[id(x)][0] for x in g):
                why = ("a line has votes only on a row named as a total"
                       if any(any(sets[id(x)][1].values()) for x in g if not sets[id(x)][0])
                       else "a line is not found in MEDSL's raw file")
            elif any(sets[id(a)][0] & sets[id(b)][0] for i, a in enumerate(g) for b in g[i + 1:]):
                why = "a precinct gives both lines votes"
            row = {"state": m["state"], "chamber": "state-upper" if m["sen"] else "state-lower",
                   "district": m["district"],
                   "lines": [[x["name"], x["votes"], len(sets[id(x)][0]),
                              sorted({pk.split("|", 1)[0] for pk in sets[id(x)][0]})] for x in g],
                   "summed": why is None}
            if why:
                row["why_not"] = why
            else:
                keep = max(g, key=lambda x: x["votes"] or 0)
                keep["spellings"] = [[x["name"], x["votes"]] for x in sorted(g, key=lambda x: -(x["votes"] or 0))]
                keep["votes"] = sum(x["votes"] or 0 for x in g)
                keep["lines"] = sum(x.get("lines", 1) for x in g)
                keep["writein"] = all(x.get("writein") for x in g)
                m["candidates"] = [x for x in m["candidates"] if x is keep or all(x is not y for y in g)]
                row["votes"] = keep["votes"]
            found.append(row)
    SPELLINGS[year] = sorted(found, key=lambda r: (r["state"], r["chamber"], r["district"], r["lines"][0][0]))
    return contests


def _named(kc):
    """Klarner's named candidates a match must find: every one but a write-in line (party w) under the write-in rule's
    strong threshold, WRITE_IN_STRONG of the last winner's votes (pipeline/local.py), which MEDSL's file may leave out
    (the orchestrator, 2026-11-13: "A write-in line under the write-in rule's strong threshold does not block a
    match"; Utah 2016's Senate 19 has a 1-vote write-in, Seguin, that MEDSL does not name) [stated]."""
    import local as L
    named = [a for a in kc["cands"] if not a["scattering"]]
    ballot = sorted([a for a in named if a["party"] != "w"], key=lambda a: -(a["votes"] or 0))
    k = kc["eseats"] or 1
    last = (ballot[k - 1]["votes"] or 0) if len(ballot) >= k else 0
    return [a for a in named if not (a["party"] == "w" and (a["votes"] or 0) < max(1, L.WRITE_IN_STRONG * last))]


PART_MIN = 3   # a compound surname's part is matched only from three letters, and with the first initial


def _part(s, t):
    """Whether one surname key is a part of the other, a compound or hyphenated surname (the orchestrator,
    2026-11-13: "A compound or hyphenated surname matches on any of its parts"): Klarner runs a compound surname's
    parts together ('mazzariellohooker, cheryl m'), MEDSL may give one part ('CHERYL HOOKER', Vermont 2018's Rutland
    Senate) or join them with a hyphen, which the key drops, so a part is the other key's start or end [measured]."""
    if s == t:
        return True
    a, b = (s, t) if len(s) < len(t) else (t, s)
    return len(a) >= PART_MIN and (b.startswith(a) or b.endswith(a))


def _finds(key, keys):
    """Whether a (surname, initial) key is among a contest's keys: the surname alike, or a part of a compound one with
    the same first initial."""
    s, i = key
    return any(s == t for t, _ in keys) or any(_part(s, t) and i and i == j for t, j in keys)


def _last_line(m, seats):
    lines = sorted((x["votes"] or 0 for x in m["candidates"] if not _generic(x)), reverse=True)
    return lines[seats - 1] if len(lines) >= seats else 0


def _ballot_sized(kc, m):
    """Whether MEDSL's contest m gives each of Klarner's candidates with a ballot-sized count (at least WRITE_IN_STRONG
    of Klarner's last winner) a line of ballot size in m too (at least WRITE_IN_STRONG of m's last winner): a contest
    that names them only in write-in lines is another district's (Vermont 2018: Essex-Orleans's write-in lines name
    all four of Franklin's candidates, with 1 to 3 votes each) [measured]. The mirror of the 2026-11-13 rule that a
    write-in line under the strong threshold does not block a match: neither does it make one [worker D3's
    reading]."""
    import local as L
    pr = pair(kc, m)
    if pr is None:
        return False
    k = kc["eseats"] or 1
    ballot = L.on_ballot(kc["cands"])
    kl = (ballot[k - 1]["votes"] or 0) if len(ballot) >= k else 0
    ml = _last_line(m, k)
    return all((pr[id(a)]["votes"] or 0) >= L.WRITE_IN_STRONG * ml for a in ballot
               if id(a) in pr and (a["votes"] or 0) >= L.WRITE_IN_STRONG * kl)


_KEYS = {}


def _keys_of(m):
    """A MEDSL contest's surnames and (surname, initial) keys, kept once per contest."""
    import local_medsl as M
    if id(m) not in _KEYS:
        ms = set()
        for x in m["candidates"]:
            ms |= M.name_keys(x["name"])
        _KEYS[id(m)] = ({t for t, _ in ms}, ms, m)
    return _KEYS[id(m)][:2]


def match(kc, pool):
    """The MEDSL contests that name every named candidate of Klarner's contest kc (but a weak write-in, _named)."""
    import local as L
    import local_medsl as M
    named = _named(kc)
    ks = [M.name_key(a["name"]) for a in named]
    if not ks or not all(k[0] for k in ks):
        return []
    hits = []
    for m in pool.get((kc["state"], kc["sen"]), []):
        surs, ms = _keys_of(m)
        if all(k[0] in surs or _finds(k, ms) for k in ks):
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
    if len(hits) > 1:
        h = [m for m in hits if _ballot_sized(kc, m)]
        hits = h or hits
    return hits


def pair(kc, m):
    """{id(Klarner candidate): MEDSL candidate}, one to one by surname (first initial where it repeats; a compound
    surname's part, _finds, where no surname is alike). A weak write-in (not in _named) is paired where MEDSL names it
    and left out where it does not."""
    import local_medsl as M
    named = [a for a in kc["cands"] if not a["scattering"]]
    must = {id(a) for a in _named(kc)}
    left = [x for x in m["candidates"] if not _generic(x)]
    out = {}
    for a in sorted(named, key=lambda a: -(a["votes"] or 0)):
        s, i = M.name_key(a["name"])
        hit = [x for x in left if s in _surs(x["name"])]
        if not hit:   # a compound surname's part
            hit = [x for x in left if _finds((s, i), M.name_keys(x["name"]))]
        else:
            # beside a whole one, a part only where it is the same name on two lines, its surnames among the whole
            # one's (Kentucky 2016's House 41: Klarner's "Woodson Scott", MEDSL's "Attica Scott" with Klarner's
            # 13,257 and "Attica Woodson SCOTT" with 434 on one row named "Cumulative:" [measured]), so the larger
            # line below; a part of another name is not (Vermont 2016 files its House in one contest, where a part
            # would reach other districts' candidates)
            whole = set().union(*(_surs(x["name"]) for x in hit))
            hit += [x for x in left if x not in hit and _finds((s, i), M.name_keys(x["name"]))
                    and _surs(x["name"]) <= whole]
        if len(hit) > 1:
            hit = [x for x in hit if M.name_key(x["name"])[1] == i] or hit
        if len(hit) > 1:   # one name in several lines (fusion, or a recount's): the line with the most votes
            hit = [max(hit, key=lambda x: x["votes"] or 0)]
        if not hit:
            if id(a) in must:
                return None
            continue
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
    import local_medsl as M
    allnamed = [a for a in kc["cands"] if not a["scattering"]]
    named = [a for a in allnamed if id(a) in pr]   # a weak write-in MEDSL does not name is left out of both sums
    kv = sum(a["votes"] or 0 for a in named if a["votes"])
    mv = sum(pr[id(a)]["votes"] or 0 for a in named if a["votes"])
    used = {id(x) for x in pr.values()}
    others = [x for x in m["candidates"] if id(x) not in used and not _generic(x) and (x["votes"] or 0) > 0]
    # a name that is one of Klarner's in another line (a fusion line, a recount's line) is not another candidate
    kkeys = {M.name_key(a["name"]) for a in allnamed}
    others = [x for x in others if not any(_finds(k, M.name_keys(x["name"])) for k in kkeys)]
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
COVER_VERSION = 15   # 14: the precinct names joined are kept; 15: joined more strictly, and a question by its votes
COVER_YEARS = {2016: (2016, 2018), 2018: (2016, 2018), 2022: (2022, 2024), 2024: (2022, 2024)}   # MEDSL's files on the same lines


def _dkey(district):
    import local_medsl as M
    d = (district or "").strip().upper()
    return M.district_no(d) or d


# lines that count no office's contest, filed as offices: registration, ballots cast and straight-party tallies
# (MEDSL's 2022 Wayne County, Michigan, files 'STRAIGHT PARTY' in 1,253 precincts, more than any contest's 1,069, and
# 'REGISTERED VOTERS' as an office) [measured]
NOT_A_CONTEST = re.compile(r"\bSTRAIGHT PARTY\b|^REGISTERED VOTERS\b|\bBALLOTS CAST\b|^VOTERS?\b|\bTURNOUT\b|"
                           r"\bVOTING STATISTICS\b|^$")   # and Idaho 2022's 'COUNTYWIDE VOTING STATISTICS', blank offices


def _cover_family(office, district):
    """The contests on every ballot below the state's: the US House by its districts (an at-large seat is statewide),
    and each chamber of the legislature (keyed apart)."""
    if office == "US HOUSE":   # a row with no district is still the precinct's row (MEDSL's 2022 Santa Cruz County,
        d = _dkey(district)    # Arizona, files 9 of its 35 precincts' US House rows with no district) [measured]
        return None if d and (not d.lstrip("0") or d in ("AT-LARGE", "AT LARGE", "STATEWIDE")) else ("US HOUSE",)
    return None


def _loose(diff, have, ps):
    """The precincts of `diff` whose rows the family has under another jurisdiction code or a joined name, taken out:
    a precinct name the county's top contest gives only once that the family has under any code, or one of its
    '/'-joined parts that the family names whole or as a part. MEDSL's 2024 Maine file codes one place's precinct
    apart across contests (blank, the county's code, the town's) and files an unorganized township alone in one
    contest and joined to a town in another ('T7 SD TWP', 'GOULDSBORO/T7 SD TWP') [measured]. A name the top
    contest gives more than once (a 'PRECINCT 1' in several towns) is not matched so."""
    if not diff or not have:
        return diff
    once = collections.Counter(q[1] for q in ps)
    names = {q[1] for q in have}
    parts = names | {x.strip() for q in have for x in q[1].split("/") if x.strip()}
    return {q for q in diff if once[q[1]] > 1 or not (
        q[1] in names or any(x.strip() in parts for x in q[1].split("/") if x.strip()))}


def _pnorm(prec):
    """A precinct's name with case and spacing folded, and the spreadsheet carriage return MEDSL's 2022 Michigan file
    leaves in some names ('CHARTER TOWNSHIP OF CANTON,_X000D_PRECINCT 1') read as a space [measured]."""
    return " ".join(prec.upper().replace("_X000D_", " ").split())


# words that name no place and no unit, left out of a precinct name before names are matched: 'CITY', 'VILLAGE',
# 'TOWNSHIP' and 'WARD' are kept, since a city and a township of one name are two places in Michigan and Kansas
# ('CITY OF MILAN' and 'MILAN TOWNSHIP', 'LONE ELM CITY' and 'LONE ELM TOWNSHIP' [measured]); 'TWP' is read as
# 'TOWNSHIP', and Michigan's ', A MICHIGAN CITY' after a village's name is left out
P_GENERIC = {"THE", "OF", "CHARTER", "PRECINCT", "PCT", "AND"}
P_SAME = {"TWP": "TOWNSHIP"}


def _edits(a, b, cap=2):
    """Levenshtein distance, stopped above cap."""
    if abs(len(a) - len(b)) > cap:
        return cap + 1
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        if min(cur) > cap:
            return cap + 1
        prev = cur
    return prev[-1]


def _pcore(name):
    """A precinct name's words, sorted, and its numbers: the words that name no place and no unit ('OF', 'CHARTER',
    'PRECINCT', and a misspelling of it within two letters, 'PRECICNT') left out, and leading zeros dropped."""
    name = re.sub(r",? A MICHIGAN CITY\b", "", name)
    toks = re.findall(r"[A-Z]+|\d+", name)
    nums = tuple(str(int(t)) for t in toks if t.isdigit())
    words = tuple(sorted(P_SAME.get(t, t) for t in toks if not t.isdigit() and t not in P_GENERIC
                         and not (len(t) >= 6 and _edits(t, "PRECINCT") <= 2)))
    return words, nums


def precinct_equivalences(ps, names):
    """{a precinct key some contest gives: the top contest's key for it}, in one county: a name the top contest lacks
    is joined to the one top-contest name with the same jurisdiction code and numbers whose words (_pcore) are the
    same, or one word apart by one letter, both words of six letters or more ('BROWNSTON' for 'BROWNSTOWN',
    'FOODHILLS' for 'FOOTHILLS') [worker D3's rule]. A name with several such matches, or none, is left apart. A first
    rule also joined words two letters apart and a name whose words held the other's: it joined 'CITY OF DEARBORN'
    to 'CITY OF DEARBORN HEIGHTS', Detroit's absent voter counting boards ('AVCB 100') to its precincts, 'EAST' to
    'WEST' and 'PART A' to 'PART B' [measured], so it was narrowed."""
    extra = {q for q in names if q not in ps}
    if not extra:
        return {}
    lone = collections.defaultdict(list)
    for c in ps:
        w, n = _pcore(c[1])
        lone[(c[0], n)].append((c, w))
    out = {}
    for q in sorted(extra):
        w, n = _pcore(q[1])

        def near(cw):   # the same words, or one word apart by one letter, both of six letters or more
            if cw == w:
                return True
            a, b = collections.Counter(cw), collections.Counter(w)
            da, db = list((a - b).elements()), list((b - a).elements())
            return (len(da) == len(db) == 1 and min(len(da[0]), len(db[0])) >= 6
                    and _edits(da[0], db[0], 1) <= 1)
        hit = [c for c, cw in lone.get((q[0], n), []) if near(cw)]
        if len(hit) == 1:
            out[q] = hit[0]
    return out


def _coverage_file(path, year, out):
    """One raw MEDSL file's rows, county by county: the precincts with votes in each general contest (each precinct's
    votes: its TOTAL mode's or its other modes' sum, whichever is more), each chamber's precincts, the US House's, and the counties of each
    chamber's districts (into `out`)."""
    import local_medsl as M
    import local_volume as V
    import medsl_precinct as P
    per = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))   # (st, county) -> contest -> pk
    tot = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))   # the same, TOTAL mode only
    fam = collections.defaultdict(lambda: collections.defaultdict(set))   # (st, county) -> family -> precincts
    # contests answered yes or no: a file can name their precincts apart (Virginia 2018); a question is a contest
    # whose answer lines hold most of its votes, since a candidate contest can carry a line named like an answer
    # (MEDSL's 2022 Michigan file: 'REJECTED' lines in Ottawa County's governor and Secretary of State rows, which
    # made those contests questions for every county and Wayne's top contest a US House seat) [measured]
    ans_v, all_v = collections.Counter(), collections.Counter()
    for r in P._rows(path):
        if (r.get("stage") or "").upper() != "GEN":
            continue
        # a special contest's rows still show the file holds the precinct's rows for its family, though it is never
        # the top contest: MEDSL's 2024 Texas file marks the regular TX-18 contest special, so 240 Harris County
        # precincts would otherwise have no US House row [measured]
        special = (r.get("special") or "").strip().upper() == "TRUE"
        cand = (r.get("candidate") or "").strip()
        # a line with a party and no name is a candidate's line (the orchestrator, 2026-11-13: "a nameless line whose
        # party is held by one candidate in the contest matches that candidate"; MEDSL's 2022 Wayne County, Michigan,
        # files its State Senate 3 and 10 lines so) [measured]
        if P.is_meta(cand) and not (cand == "" and (r.get("party_simplified") or "").strip()):
            continue
        prec = r.get("precinct") or ""
        if V.AGG_NAME.search(prec) or P.COUNTY_TOTAL.search(prec.strip().upper()):
            continue
        office = (r.get("office") or "").strip().upper()
        if NOT_A_CONTEST.search(office):
            continue
        st = r.get("state_po") or r.get("state_postal") or ""
        county = P.fips5(r.get("county_fips") or "")
        # a precinct by its name with case and spacing folded: MEDSL's 2024 Maine file names Hancock County's precincts
        # in capitals in some contests and not in others ('SWAN'S ISLAND', "Swan's Island") [measured]; spelled apart
        # across contests, it is joined by precinct_equivalences below
        pk = (" ".join((r.get("jurisdiction_fips") or r.get("jurisdiction") or "").upper().split()), _pnorm(prec))
        m = M.relabel({"office": office, "district": r.get("district") or ""})
        if special:
            if m["office"] in M.LEG and _dkey(m["district"]):
                fam[(st, county)][("LEG", M.LEG[m["office"]])].add(pk)
            elif _cover_family(m["office"], m["district"]):
                fam[(st, county)][_cover_family(m["office"], m["district"])].add(pk)
            continue
        try:
            v = int(float(r.get("votes") or 0))
        except ValueError:
            v = 0
        if m["office"] in M.LEG:
            sen, dk = M.LEG[m["office"]], _dkey(m["district"])
            if dk:   # a row with no district (MEDSL's 2016 Maricopa County rows) is no district's row (22:42 item 4)
                out["districts"].setdefault(f"{st}|{sen}|{dk}", set()).add(county)
                fam[(st, county)][("LEG", sen)].add(pk)
            continue
        f_ = _cover_family(m["office"], m["district"])
        if f_:
            fam[(st, county)][f_].add(pk)
        k = (m["office"], r.get("district") or "", (r.get("dataverse") or "").upper())
        per[(st, county)][k][pk] += v
        all_v[k] += max(v, 0)
        if cand.upper() in P.ANSWERS:
            ans_v[k] += max(v, 0)
        if (r.get("mode") or "").strip().upper() == "TOTAL":
            tot[(st, county)][k][pk] += v
    if year not in out["years_counted"]:
        return
    questions = {k for k in ans_v if ans_v[k] > 0.5 * all_v[k]}
    n_c = collections.Counter(st for st, _ in per)
    spread = collections.Counter((st, k) for (st, _), cs in per.items() for k, c in cs.items() if any(c.values()))

    def short(ps, tv, have):
        """Precincts of the top contest a contest's rows miss: the set difference, but no more than the difference in
        counts, since a file can name the same precinct apart in two contests (MEDSL's 2018 Virginia files add '(08)'
        to a question's absentee precincts) [measured]; then the set difference's size and its votes in the top
        contest (scaled by the first over the second where they differ, in local_districts.check)."""
        diff = _loose(ps - have, have, ps)
        n = min(len(diff), max(0, len(ps) - len(have))) if have else len(ps)
        return [n, len(diff), sum(tv[q] for q in diff)]

    for (st, county), cs in per.items():
        votes = {}
        for k, c in cs.items():
            # a precinct's votes: its TOTAL mode's or its other modes' sum, whichever is more, since a file can give
            # both (the other modes then add up to the TOTAL), or give one candidate a TOTAL line of 0 beside another's
            # modes (MEDSL's 2018 Delaware file: US Senate, New Castle County) [measured]
            t = tot[(st, county)].get(k, {})
            votes[k] = {q: max(t.get(q, 0), n - t.get(q, 0)) for q, n in c.items() if max(t.get(q, 0), n - t.get(q, 0)) > 0}
        # the top contest: the candidate contest with votes in the most precincts (a question only where the county
        # has no candidate contest), since MEDSL's 2018 Virginia file names a question's absentee precincts apart,
        # one per congressional district [measured]
        tops = [k for k in votes if votes[k] and k not in questions] or [k for k in votes if votes[k]]
        top = max(tops, key=lambda k: (len(votes[k]), sum(votes[k].values()))) if tops else None
        tv = votes[top] if top else {}
        ps = set(tv)
        # names spelled apart from the top contest's, joined to them (the orchestrator, 2026-11-13: "Normalize
        # precinct names before the gate's match, list each equivalence, and recompute every county")
        eq = precinct_equivalences(ps, set().union(*[set(v) for v in votes.values()], *fam[(st, county)].values()))
        if eq:
            out.setdefault("equivalences", {}).setdefault(str(year), {})[f"{st}|{county}"] = sorted(
                [" / ".join(a), " / ".join(b)] for a, b in eq.items())
            votes = {k: {eq.get(q, q): n for q, n in v.items()} for k, v in votes.items()}
            fam[(st, county)] = {f_: {eq.get(q, q) for q in v} for f_, v in fam[(st, county)].items()}
        fs = fam[(st, county)]
        rec = {"top": " ".join(x for x in top if x) if top else None, "precincts": len(ps),
               "top_votes": sum(tv.values())}
        # each family of contests on every ballot below the state's: [precincts with its rows, precincts of the top
        # contest it misses, their votes]
        rec["families"] = {}
        for name, key in (("lower", ("LEG", 0)), ("upper", ("LEG", 1)), ("us_house", ("US HOUSE",))):
            have = fs.get(key, set())
            rec["families"][name] = [len(have)] + short(ps, tv, have)
            if name != "us_house":
                rec[name + "_missing"] = rec["families"][name][1]
            elif ps and have and rec["families"][name][1] / len(ps) > COVER_GAP:   # for the reader: what is missing
                rec["us_house_eg"] = {"missing": sorted(" / ".join(q) for q in ps - have)[:8],
                                      "have": sorted(" / ".join(q) for q in have)[:4]}
                # the contests whose own rows are in the top contest's precincts (within 2%): their district is the
                # county, and their rows are not missing in it (22:19 item 1: "any contest whose rows are missing in
                # part of its district"); MEDSL's 2024 Monroe County Clerk has rows in all 655 precincts [measured]
                rec["whole_contests"] = sorted(f"{k[0]}|{k[1]}" for k in votes
                                               if short(ps, tv, set(votes[k]))[0] / len(ps) <= COVER_GAP)
        # 22:19 item 1 for a statewide contest (rows in 90% of the state's counties): the precincts of the county's
        # top contest its rows miss, where that is more than 2% of them (New York 2024's Proposal One has rows in 31 of
        # Monroe County's 655 precincts) [measured]
        if n_c[st] > 1:
            rec["statewide_short"] = {}
            for k in cs:
                if k == top or spread[(st, k)] < 0.9 * n_c[st]:
                    continue
                n, nd, v = short(ps, tv, set(votes[k]))
                if ps and n / len(ps) > COVER_GAP:
                    rec["statewide_short"][f"{k[0]}|{k[1]}"] = [n, nd, v]
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
         "districts": {k: sorted(v) for k, v in out["districts"].items()}, "counties": out["counties"],
         "equivalences": out.get("equivalences", {})}
    with open(out_p, "w") as f:
        json.dump(d, f)
    return d


CENSUS_BEF = os.path.join(F.CACHE, "census-sld", "raw")
CENSUS_NORM = os.path.join(F.CACHE, "census-sld", "normalized", "counties-2022.json")
CENSUS_YEARS = (2022,)   # the lines the Census's 2022 block equivalency files hold
CENSUS_VERSION = 2   # the cache holds each county's block count
CENSUS_URL = "https://www2.census.gov/programs-surveys/decennial/rdo/mapping-files/2023/2022-state-legislative-bef/"
CENSUS_PAGE = "https://www.census.gov/geographies/mapping-files/2023/dec/rdo/2022-state-legislative-bef.html"


def _census_metas():
    out = {}
    for chamber in ("sldu", "sldl"):
        p_ = os.path.join(CENSUS_BEF, f"{chamber}_2022.zip.meta.json")
        if os.path.exists(p_):
            with open(p_) as f:
                out[f"{chamber}_2022.zip"] = json.load(f)
    return out


def census_counties():
    """The counties of each state legislative district on the 2022 lines, from the Census's 2022 State Legislative
    Block Equivalency Files (sldu_2022.zip and sldl_2022.zip: each block's GEOID, whose first five digits are its
    county, and its district; fetched once, 2026-11-13, cached, from CENSUS_URL, the files the Census's page
    CENSUS_PAGE links): {"ST|sen|district number": {county: the district's blocks there}} (the orchestrator,
    2026-11-13: "a district's counties are its MEDSL rows plus the Census's 2020 SLD-to-county relationship for its
    lines, one fetch, cached"). Districts the Census codes with letters (not a number) are left out [worker D3's
    choice: MEDSL's names for them are not the Census's codes]."""
    if os.path.exists(CENSUS_NORM):
        with open(CENSUS_NORM) as f:
            d = json.load(f)
        if d.get("version") == CENSUS_VERSION:
            return d["districts"]
    out = collections.defaultdict(collections.Counter)
    metas = {}
    for chamber, sen in (("sldu", 1), ("sldl", 0)):
        zp = os.path.join(CENSUS_BEF, f"{chamber}_2022.zip")
        with open(zp + ".meta.json") as f:
            metas[chamber] = json.load(f)
        with zipfile.ZipFile(zp) as z:
            for member in z.namelist():
                if not member.endswith(".txt"):   # the zip's 0_ReadMe.pdf
                    continue
                st = member.split("_")[1]   # '26_MI_SLDU22.txt'

                with z.open(member) as raw:
                    for line in io.TextIOWrapper(raw, encoding="latin-1"):
                        g, _, d = line.strip().partition(",")
                        if not g.isdigit() or not d.strip().isdigit():
                            continue
                        out[f"{st}|{sen}|{int(d)}"][g[:5]] += 1
    os.makedirs(os.path.dirname(CENSUS_NORM), exist_ok=True)
    d = {"version": CENSUS_VERSION, "sources": metas,
         "districts": {k: dict(sorted(v.items())) for k, v in sorted(out.items())}}
    with open(CENSUS_NORM, "w") as f:
        json.dump(d, f)
    return d["districts"]


def district_cover(kc, m, year, cov, full_upper):
    """22:26 (a): the counties of MEDSL's district (from every MEDSL file on the same lines, and the contest's own)
    where MEDSL lacks the chamber's rows beyond 2% of the county's precincts: {"counties", "gaps": [[county,
    missing, precincts]], "by"}. A staggered upper chamber is read by the lower chamber's rows."""
    st, sen = kc["state"], kc["sen"]
    up_upper, up_lower = full_upper
    counties = set(cov["districts"].get(f"{st}|{sen}|{_dkey(m['district'])}", [])) | set(m.get("counties") or [])
    # 2022's lines: the Census's counties of the district too; one where MEDSL's file has no row of the district is
    # missing (the orchestrator, 2026-11-13: "A listed county with no rows for the district counts as missing")
    blocks = census_counties().get(f"{st}|{sen}|{_dkey(m['district'])}", {}) \
        if year in CENSUS_YEARS and _dkey(m["district"]).isdigit() else {}
    census = set(blocks)
    rows_in = set(counties)   # the counties where MEDSL's files have rows of the district
    # the chamber's own rows; a staggered chamber by the other's, where that one is all up; neither all up: the day's
    # top contest stands in, and a county it lacks leaves the district untested (the orchestrator, 22:42 (3))
    own, other = (up_upper, up_lower) if sen else (up_lower, up_upper)
    ch = ("upper" if sen else "lower") if st in own else ("lower" if sen else "upper") if st in other else "top"
    # a Census county's gap carries the share of the district's blocks that lie in it (a block may hold no one; the
    # files give no population), so a sliver can be told from a part [measured: the block counts]
    gaps = [[county, "census", round(blocks[county] / sum(blocks.values()), 4)] for county in sorted(census - rows_in)]
    for county in sorted(counties):
        rec = cov["counties"].get(f"{st}|{county}")
        if rec is None:   # the county has no row of this year's file at all
            gaps.append([county, None, None])
            continue
        if not rec["precincts"]:   # every row of the county, in every office, has 0 votes: a row of zeros carries no
            # count, so it cannot show coverage (the orchestrator, 2026-11-13 05:38 (1): "a county whose rows are all
            # zero is missing, not covered"; Indiana 2022's Cass, Daviess and Scott [measured])
            share = round(blocks[county] / sum(blocks.values()), 4) if county in blocks else None
            gaps.append([county, "zero", share])
            continue
        if ch != "top" and rec["precincts"] and rec[ch + "_missing"] / rec["precincts"] > COVER_GAP:
            gaps.append([county, rec[ch + "_missing"], rec["precincts"]])
    by = (f"the {ch} chamber's rows" + ("" if ch == ("upper" if sen else "lower") else
                                        f" (the {'upper' if sen else 'lower'} chamber is staggered)")
          if ch != "top" else "the day's top contest (neither chamber is all up)")
    return {"counties": sorted(counties | census), "gaps": gaps, "by": by, "untested": ch == "top" and bool(gaps),
            "census_counties": sorted(census) if census else None}


OVER_SEATS = 1.10   # a count over its seats times the ballots, by more than the over-ballot test's line (10%)
# (b) The orchestrator, 2026-11-13 00:55: "A refinement at every level. An unopposed comparator undercounts ballots by
# roll-off, often 10 to 30%. Against one, list up to 1.5 and hold only above 1.5". The district's ballots are each
# precinct's votes in the statewide contest of one seat with the most there; where every contest giving them has one
# name on the ballot (write-ins aside), the line is OVER_SEATS_UNOPPOSED. In MEDSL's files of 2016 to 2022, ten
# statewide contests have one name, all of 2018 (Alabama's agriculture commissioner and treasurer, Idaho's controller
# and treasurer, Minnesota's chief justice, Nebraska's attorney general and treasurer, South Carolina's comptroller
# and superintendent, Wyoming's superintendent), each in a state whose governor's contest has more than one
# [measured: scratch scan of the files].
OVER_SEATS_UNOPPOSED = 1.50
STATEWIDE_SPREAD = 0.9   # a statewide contest: rows in 90% of the state's precincts with any row


TOP_OFFICES = {"PRESIDENT", "US PRESIDENT", "US SENATE", "U.S. SENATE", "GOVERNOR"}


def _statewide_one_seat(r, office):
    """A row of a statewide contest of one seat: MEDSL's president and US Senate lines, or a state office its file
    marks statewide (district STATEWIDE) with one seat; in a file without dataverse (2016's), the president, the US
    Senate and the governor by name. A county's office in every county is not one (Vermont 2018's assistant judges,
    two a county, which MEDSL files with one seat and an empty district) [measured: Rutland]."""
    dv = (r.get("dataverse") or "").strip().upper()
    if not dv:
        return office in TOP_OFFICES
    if dv in ("PRESIDENT", "SENATE"):
        return True
    return dv == "STATE" and (r.get("district") or "").strip().upper() == "STATEWIDE" and \
        (r.get("magnitude") or "1").strip() in ("1", "1.0")


def district_ballots(path, wants):
    """The ballots of MEDSL districts, from one raw file: {(state, sen, district key): [precincts with the district's
    rows, ballots]}, a precinct's ballots being its votes in the statewide candidate contest of one seat with the most
    there (_statewide_one_seat, with rows in STATEWIDE_SPREAD of the state's precincts; a precinct's votes in a contest
    are its TOTAL mode's
    or its other modes' sum, whichever is more, as coverage counts them). A district whose precincts no statewide
    contest reaches is left out. `wants`: the (state, sen, district key) to read. Read only where MEDSL's file covers
    the district (district_cover: no county missing the chamber's rows), so its precincts are the district's [worker
    D3's reading; M2 read Vermont 2018's Rutland so: "MEDSL's Rutland governor rows hold 24,483 ballots on all 32
    precincts"]. Also returns, by state, the counties with rows in the file but no contest's votes (a ballots-cast
    line alone, or zeros): MEDSL's 2018 Indiana file gives Washington County (18175) a "BALLOTS CAST" line of 9,541
    in its 21 precincts and no contest's row [measured]."""
    import local_medsl as M
    import local_volume as V
    import medsl_precinct as P
    states = {w[0] for w in wants}
    tot = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))   # st -> contest -> pk
    oth = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    names = collections.defaultdict(lambda: collections.defaultdict(set))   # st -> contest -> names on the ballot
    dist = collections.defaultdict(set)
    seen, voted = collections.defaultdict(set), collections.defaultdict(set)   # st -> counties with a row; with votes
    for r in P._rows(path):
        st = r.get("state_po") or r.get("state_postal") or ""
        if st not in states or (r.get("stage") or "").upper() != "GEN" or \
                (r.get("special") or "").strip().upper() == "TRUE":
            continue
        county = P.fips5(r.get("county_fips") or "")
        seen[st].add(county)
        cand = (r.get("candidate") or "").strip()
        prec = r.get("precinct") or ""
        if P.is_meta(cand) or V.AGG_NAME.search(prec) or P.COUNTY_TOTAL.search(prec.strip().upper()):
            continue
        office = (r.get("office") or "").strip().upper()
        if NOT_A_CONTEST.search(office):
            continue
        try:
            if int(float(r.get("votes") or 0)) > 0:
                voted[st].add(county)
        except ValueError:
            pass
        pk = (county,
              " ".join((r.get("jurisdiction_fips") or r.get("jurisdiction") or "").upper().split()),
              " ".join(prec.upper().split()))
        m = M.relabel({"office": office, "district": r.get("district") or ""})
        if m["office"] in M.LEG:
            k = (st, M.LEG[m["office"]], _dkey(m["district"]))
            if k in wants:
                dist[k].add(pk)
            continue
        if cand.upper() in P.ANSWERS or not _statewide_one_seat(r, office):
            continue
        try:
            v = int(float(r.get("votes") or 0))
        except ValueError:
            v = 0
        key = (office, r.get("district") or "")
        (tot if (r.get("mode") or "").strip().upper() == "TOTAL" else oth)[st][key][pk] += v
        if (r.get("writein") or "").strip().upper() != "TRUE" and "WRITE" not in cand.upper():
            names[st][key].add(cand.upper())
    out = {}
    for st in states:
        keys = set(tot[st]) | set(oth[st])
        votes = {k: {q: max(tot[st][k].get(q, 0), oth[st][k].get(q, 0)) for q in set(tot[st][k]) | set(oth[st][k])}
                 for k in keys}
        allp = set().union(*[set(v) for v in votes.values()]) if votes else set()
        wide = [k for k in keys if allp and len(votes[k]) >= STATEWIDE_SPREAD * len(allp)]
        for k in [w for w in wants if w[0] == st]:
            ps = dist.get(k, set())
            if not ps or not wide:
                continue
            b = [max(votes[c].get(q, 0) for c in wide) for q in ps]
            if all(b):
                by = {c for c in wide if any(votes[c].get(q) for q in ps)}
                # (b): the figure rests on unopposed contests alone where every contest giving it has one name
                out[k] = [len(ps), sum(b), sorted({c[0] for c in by}),
                          all(len(names[st][c]) <= 1 for c in by)]
    return out, {st: sorted(seen[st] - voted[st]) for st in states if seen[st] - voted[st]}


OVER_MARK = "Klarner's count is over its seats times the ballots; MEDSL's counts"


def _raw_path(year, name):
    import local_volume as V
    if year == 2016:
        return os.path.join(V.RAWDIR, V.STATE_2016)
    hit = [p_ for n, p_ in V.raw_files(year) if p_ and (n == name or os.path.basename(p_).endswith(name))]
    return hit[0] if hit else None


# The over-seats test of every tested record whose district MEDSL's file covers (the orchestrator, 2026-11-13 05:15
# (4): "Build the over-seats test for every record with ballots, not Rutland alone, and list what it flags"; "If
# either is still over, treat it as Rutland: MEDSL taken where covered and passing every test, else held"; 01:15:
# "A count over seats times ballots, like Rutland's, cannot be right whatever the coverage"). The ballots are the
# district's own precincts' (those with the district's rows in MEDSL's file: Vermont 2018's Grand Isle district is
# Colchester's two precincts and four of Grand Isle County's five towns, Alburgh's Senate rows being Franklin's; its
# Windham district is 24 of Windham County's precincts, Wilmington's Senate rows being Bennington's [measured]).
OVER_SEATS_MEDSL = 1.0   # MEDSL's count taken only where it is within its seats times the ballots
OVER_HELD = "held: Klarner's count is over its seats times the ballots"
OVER_BLANK = ("MEDSL's file has rows but no contest's votes in count{s} {c} of the state, and the district's counties are "
              "read from MEDSL's rows alone (no Census list for these lines), so its precincts, and the ballots read "
              "from them, may lack a county of the district")


def over_seats_pass(year, flags, tallies, tested):
    """Every tested record of the year (tested: [(flag or None, the record's test figures)], each with the district's
    id, MEDSL file and district, seats and counts), in a district MEDSL's file covers (no county missing the chamber's
    rows) and not shared with another district, set against the district's ballots (district_ballots). Klarner's
    count over its seats times the ballots by more than OVER_SEATS: MEDSL's counts are taken (OVER_MARK) where MEDSL's
    are within OVER_SEATS_MEDSL of them, every candidate paired with votes and no other name on MEDSL's ballot; else
    the record is held (OVER_HELD). A flag's own outcome gives way only where it was held or noted, or kept for a gap
    in MEDSL's file; a district settled by a state or a county keeps that outcome, the figures beside. Not read where
    the file has a county with no contest's votes and the district's counties are MEDSL's rows alone (OVER_BLANK): the
    record keeps the outcome its other tests give. Returns the list of every record over, and those not read by
    state (for check-districts.json)."""
    by_file = collections.defaultdict(list)
    for f in tested:
        if f.get("covered"):
            by_file[f["medsl_file"]].append(f)
    over, unread = [], {}
    by_id = {f["id"]: f for f in flags}
    for name, fs in sorted(by_file.items()):
        path = _raw_path(year, name)
        if not path:
            continue
        wants = {(f["state"], 1 if f["chamber"] == "state-upper" else 0, _dkey(f["medsl_district"])) for f in fs}
        got, blank = district_ballots(path, wants)
        for f in fs:
            b = got.get((f["state"], 1 if f["chamber"] == "state-upper" else 0, _dkey(f["medsl_district"])))
            fl = by_id.get(f["id"])
            if blank.get(f["state"]) and year not in CENSUS_YEARS:
                # a county of the file with no contest's votes, where the district's counties are MEDSL's rows alone:
                # the district may take it in, unseen, so its precincts and their ballots may lack it (Indiana 2018's
                # Senate 47: Klarner 47,917, MEDSL 38,554, Washington County's ballots cast 9,541 [measured])
                if fl is not None:
                    fl["over_seats"] = {"read": False, "why": OVER_BLANK.format(
                        c=", ".join(blank[f["state"]]), s="y" if len(blank[f["state"]]) == 1 else "ies")}
                u = unread.setdefault(f["state"], {"counties": blank[f["state"]], "records": 0, "flagged": []})
                u["records"] += 1
                if fl is not None:
                    u["flagged"].append(f["id"])
                continue
            if not b:
                if fl is not None:
                    fl["over_seats"] = {"read": False, "why": "no statewide contest reaches the district's precincts"}
                continue
            seats = f["eseats"] or 1
            xk, xm = f["klarner"] / (seats * b[1]), f["medsl"] / (seats * b[1])
            line = OVER_SEATS_UNOPPOSED if b[3] else OVER_SEATS
            os_ = {"read": True, "precincts": b[0], "ballots": b[1], "by": b[2], "by_unopposed": b[3], "line": line,
                   "seats": seats, "klarner_per_ballot": round(f["klarner"] / b[1], 3),
                   "medsl_per_ballot": round(f["medsl"] / b[1], 3), "klarner_x": round(xk, 4), "medsl_x": round(xm, 4),
                   "over": xk > line}
            if fl is not None:
                fl["over_seats"] = os_
            if xk <= line:
                continue
            take = xm <= OVER_SEATS_MEDSL and not [x for x in f["others"] if not x["write_in"]] and \
                all(p_[1] and p_[3] for p_ in f["pairs"])
            row = {"id": f["id"], "medsl_file": name, "flagged": fl is not None,
                   "outcome_before": fl["outcome"] if fl is not None else "passed", **os_}
            if fl is not None and (fl["outcome"].startswith("settled") or fl["outcome"] == "MEDSL taken"):
                row["outcome"] = fl["outcome"]
                over.append(row)
                continue
            if fl is None:   # a record no flag raised: listed with its figures as a flag of its own
                fl = {k: f[k] for k in ("id", "state", "chamber", "dname", "dno", "post", "eseats", "medsl_district",
                                         "medsl_file")}
                fl.update({k: v for k, v in f.items() if k in ("matched", "pairs", "klarner", "medsl", "ratio", "flag_a",
                                                               "unopposed", "others", "flag_b", "b_tested",
                                                               "medsl_ballot_unpaired", "medsl_write_ins")})
                fl.update({"flags": ["over seats"], "outcome": "passed", "covered": True, "over_seats": os_})
                flags.append(fl)
                by_id[fl["id"]] = fl
            else:
                tallies[f"flag {'+'.join(fl['flags'])}: {fl['outcome']}"] -= 1
            if take:
                fl["outcome"], fl["mark"] = "MEDSL taken", OVER_MARK
                fl.pop("coverage", None)
            else:
                fl["outcome"] = OVER_HELD
            tallies[f"flag {'+'.join(fl['flags'])}: {fl['outcome']}"] += 1
            row["outcome"] = fl["outcome"]
            over.append(row)
    for k in [k for k, v in tallies.items() if v == 0]:
        del tallies[k]
    return sorted(over, key=lambda r: r["id"]), dict(sorted(unread.items()))


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


UT_CANVASS = os.path.join(F.CACHE, "ut_lg", "raw", "2016-General-Election-Statewide-Canvass-3.pdf")
IN_ARCHIVE = os.path.join(F.CACHE, "in_enr", "raw", "2016General")
# Indiana's 2018 archive: one request (the orchestrator, 2026-11-13 06:52: "IN 2018 SD47: one request to Indiana's 2018
# archive is allowed"), its State Senator file reached through two index pages (settings.json, statewideElectionsC_A
# .json; "Index pages followed to reach the one file count as one request"), 2026-11-13 07:37:47 to 07:38:24 UTC. Its
# settings print "Certified":"T" [stated], a certified mark (15:16). Its State Representative file: one more request
# (the orchestrator, 2026-11-13 09:21: "Indiana 2018's House flags: one request to the archive's 2018 House file is
# allowed, as for the Senate"), 2026-11-13 09:21:33 UTC, its address from the cached statewideElectionsC_A.json.
IN_ARCHIVE_2018 = os.path.join(F.CACHE, "in_enr", "raw", "2018General")
IN_2018_SENATE = "OffCatC_2180_A.json"   # office category 2180, "State Senator", in statewideElectionsC_A.json
IN_2018_HOUSE = "OffCatC_2201_A.json"    # office category 2201, "State Representative", in statewideElectionsC_A.json


def _cols(line, pat=r"\S+(?: \S+)*"):
    """The pieces of a pdftotext -layout line split on two or more spaces, with their columns."""
    return [(m.start(), m.group(0)) for m in re.finditer(pat, line)]


def ut_2016_senate():
    """Utah's 2016 statewide canvass (vote.utah.gov, one request on 2026-11-13; cached by worker D3), its State Senate
    pages: {district: [{name, votes, write_in}]}. Each page has a row of district headings (a heading can wrap onto
    the line above and below), one row of candidates' names, one of their parties ('(Write-in)' marks a write-in),
    a TOTAL row and a 'Contest Sum' row. The TOTAL row's figures are split into runs that add up to each contest sum
    in turn, the headings ordered by column give the districts, and the names pair with the figures by order; a page
    whose counts do not line up so is not read [worker D3's reading of the layout]."""
    import subprocess
    if not os.path.exists(UT_CANVASS):
        return None
    txt = subprocess.run(["pdftotext", "-layout", UT_CANVASS, "-"], capture_output=True, text=True, check=True).stdout
    out = {}
    for page in txt.split("\f"):
        lines = page.split("\n")
        if not any("Utah Senate - District" in x or re.search(r"Utah Senate -\s*$", x) for x in lines[:3]):
            continue
        try:
            i_tot = next(i for i, x in enumerate(lines) if x.strip().startswith("TOTAL"))
            i_sum = next(i for i, x in enumerate(lines) if x.strip().startswith("Contest Sum"))
            i_cty = next(i for i, x in enumerate(lines) if x.strip() == "County")
        except StopIteration:
            continue
        heads = []   # (column, district) from the heading rows, wrapped ones by their 'District N' line below
        for j in range(0, i_cty):
            for c, piece in _cols(lines[j], r"Utah Senate - District \d+|District \d+|Utah Senate -"):
                mt = re.search(r"District (\d+)", piece)
                if piece.startswith("Utah Senate - District"):
                    heads.append((c, mt.group(1)))
                elif piece == "Utah Senate -":
                    below = [p_ for jj in (j + 1, j + 2) if jj < i_cty
                             for c2, p_ in _cols(lines[jj], r"District \d+") if abs(c2 - c) <= 4]
                    if below:
                        heads.append((c, re.search(r"\d+", below[0]).group(0)))
        heads.sort()
        names = [p_ for _, p_ in _cols(lines[i_cty - 1])]
        parties = [p_ for _, p_ in _cols(lines[i_cty + 1])]
        vals = [int(x.replace(",", "")) for x in re.findall(r"[\d,]+", lines[i_tot].split("TOTAL", 1)[1])]
        sums = [int(x.replace(",", "")) for x in re.findall(r"[\d,]+", lines[i_sum].split("Contest Sum", 1)[1])]
        if not (len(names) == len(parties) == len(vals)) or len(sums) != len(heads):
            continue
        k, runs = 0, []
        for tgt in sums:
            j, acc = k, 0
            while j < len(vals) and acc < tgt:
                acc += vals[j]
                j += 1
            if acc != tgt:
                break
            runs.append((k, j))
            k = j
        if len(runs) != len(sums) or k != len(vals):
            continue
        for (a, b), (_, d) in zip(runs, heads):
            out[d] = [{"name": (names[i] + " " + parties[i].replace("(Write-in)", "")).strip()
                       if "Write-in" in parties[i] else names[i], "votes": vals[i], "write_in": "Write-in" in parties[i]}
                      for i in range(a, b)]
    return out


def in_2016():
    """Indiana's results archive of the 2016 general (enr.indianavoters.in.gov/archive/2016General, read by worker D3 on
    2026-11-13 through pipeline/intake/in_enr.py's reader: settings.json, the category list and the State Senator and
    State Representative files): {(sen, district): [{name, votes, write_in}]}; '(W/I)' marks a write-in."""
    return in_archive(IN_ARCHIVE, ((1, "OffCatC_1766_A.json"), (0, "OffCatC_1787_A.json")))


def _first_last(name):
    """The archive writes a name first name first, a suffix after a comma ('James W. Merritt, Jr', 2018's Senate 31;
    'Rudy M. Howard, Jr.', 2016) [measured]; the name readers take a comma for 'LAST, FIRST', so the suffix's comma
    is dropped ('James W. Merritt Jr')."""
    return re.sub(r",\s*(JR|SR|II|III|IV|V)\.?$", r" \1", name, flags=re.I)


def in_archive(folder, files):
    """An Indiana results archive's legislative office files as read: {(sen, district): [{name, votes, write_in}]};
    None if a file is not in the cache."""
    out = {}
    for sen, fn in files:
        p_ = os.path.join(folder, fn)
        if not os.path.exists(p_):
            return None
        with open(p_, encoding="utf-8-sig") as f:
            d = json.load(f)
        d = d.get("Root", d)
        races = (d.get("StatewideSummary") or {}).get("Race") or []
        for r in races if isinstance(races, list) else [races]:
            mt = re.search(r"District 0*(\d+)$", r["OFFICE_TITLE"].strip())
            cs = (r.get("Candidates") or {}).get("Candidate") or []
            if mt:
                out[(sen, mt.group(1))] = [{"name": _first_last(x["NAME_ON_BALLOT"].replace("(W/I)", "").strip()),
                                            "votes": int(x.get("TOTAL") or 0), "write_in": "(W/I)" in x["NAME_ON_BALLOT"]}
                                           for x in (cs if isinstance(cs, list) else [cs])]
    return out


STATE_FILES = {
    ("UT", 2016): ("Utah's 2016 statewide canvass", "vote.utah.gov", UT_CANVASS),
    ("IN", 2016): ("Indiana's results archive of the 2016 general", "enr.indianavoters.in.gov", IN_ARCHIVE),
    ("IN", 2018): ("Indiana's results archive of the 2018 general (its State Senator file)", "enr.indianavoters.in.gov",
                   IN_ARCHIVE_2018)}
# the file whose meta the source names, by state, year and chamber (1 the upper; else the settings, or the file itself)
STATE_META = {("IN", 2018, 1): IN_2018_SENATE, ("IN", 2018, 0): IN_2018_HOUSE}
STATE_NAME = {("IN", 2018, 0): "Indiana's results archive of the 2018 general (its State Representative file)"}
STATE_CACHE = {}


# A state count that bears a certified mark wins (the orchestrator, 2026-11-07 15:16); these two bear none [measured:
# Indiana's 2016 archive's settings.json has no 'Certified' field, where its 2024 archive says "Certified": "T"; Utah's
# canvass, read by pdftotext, has no word 'certif', 'canvass' or 'official' in its text]
STATE_MARKED = {("UT", 2016): False, ("IN", 2016): False, ("IN", 2018): True}   # 2018: "Certified":"T" [measured]
TWO_AGREE = 0.004   # the orchestrator, 2026-11-13 05:15 (3): "two independent counts that agree by candidate within
#                     0.4% stand against one state count that bears no certified mark"
TWO_OUTCOME = "two counts agree against the state's: Klarner's count stands"


def state_district(kc):
    """The state's own count of Klarner's district from STATE_FILES, read once a state-year: [{name, votes,
    write_in}], or None."""
    key = (kc["state"], kc["year"])
    if key not in STATE_FILES or not str(kc["dno"]).isdigit():
        return None
    if key not in STATE_CACHE:
        STATE_CACHE[key] = ut_2016_senate() if key == ("UT", 2016) else in_2016() if key == ("IN", 2016) else \
            in_archive(IN_ARCHIVE_2018, ((1, IN_2018_SENATE), (0, IN_2018_HOUSE)))
    d = STATE_CACHE[key]
    if not d:
        return None
    return d.get(str(int(kc["dno"]))) if key == ("UT", 2016) and kc["sen"] else \
        d.get((kc["sen"], str(int(kc["dno"])))) if key[0] == "IN" else None


def _state_pairs(kc, cs):
    """Klarner's ballot candidates paired with the state's by surname, each once, the state naming no other on the
    ballot: [[Klarner's name, Klarner's votes, the state's name, the state's votes]], or None."""
    import local as L
    import local_medsl as M
    ballot = L.on_ballot(kc["cands"])
    sb = [x for x in cs if not x["write_in"]]
    pairs = []
    for a in ballot:
        hit = [x for x in sb if _finds(M.name_key(a["name"]), M.name_keys(x["name"]))]
        if len(hit) != 1:
            return None
        pairs.append([a["name"], a["votes"], hit[0]["name"], hit[0]["votes"]])
    return pairs if len(sb) == len(ballot) else None


def _state_meta(kc):
    name, host, path = STATE_FILES[(kc["state"], kc["year"])]
    k3 = (kc["state"], kc["year"], int(kc["sen"]))
    name = STATE_NAME.get(k3, name)
    meta_p = (path + ".meta.json") if os.path.isfile(path) else \
        os.path.join(path, STATE_META.get(k3, "settings.json") + ".meta.json")
    with open(meta_p) as f:
        meta = json.load(f)
    return {"source": name, "host": host, "url": meta.get("url"), "read_utc": meta.get("finished_utc") or
            meta.get("read_utc"), "sha256": meta.get("sha256"), "marked": STATE_MARKED[(kc["state"], kc["year"])]}


def _within(a, b, tol):
    """a within tol of b, as a share of b (both zero: within)"""
    return (not a and not b) or (bool(b) and abs((a or 0) / b - 1) <= tol)


def settle_agree(kc, t):
    """A flag settled by the state's published results agreeing with one source (the orchestrator, 2026-11-13 01:15:
    "Settling a flag needs only the state's own count agreeing with one source ... the notes say 'the state's published
    results agree' and never 'certified'"; 05:15 (2): "The settle test compares candidates, not totals"): the state's
    district names each of Klarner's ballot candidates once by surname, no other ballot name, and each candidate's
    count is within RATIO_OFF of Klarner's (Klarner's count stands, "with": "klarner"), or else of MEDSL's, every
    candidate paired with MEDSL's lines (MEDSL's count stands, "with": "medsl": 05:15 (1), Indiana 2016's Senate 36,
    "the state agrees with MEDSL on both candidates, so MEDSL's count stands")."""
    cs = state_district(kc)
    if not cs:
        return None
    pairs = _state_pairs(kc, cs)
    if not pairs:
        return None
    out = dict(_state_meta(kc), write_ins=[[x["name"], x["votes"]] for x in cs if x["write_in"]])
    if all(_within(p_[3], p_[1], RATIO_OFF) for p_ in pairs):
        kv, sv = sum(p_[1] or 0 for p_ in pairs), sum(p_[3] for p_ in pairs)
        return dict(out, pairs=pairs, ratio=round(sv / kv, 5) if kv else None, **{"with": "klarner"})
    med = {p_[0]: p_[3] for p_ in t["pairs"]}
    if set(med) != {p_[0] for p_ in pairs} or not all(med[p_[0]] for p_ in pairs):
        return None
    if all(_within(p_[3], med[p_[0]], RATIO_OFF) for p_ in pairs):
        mv, sv = sum(med[p_[0]] for p_ in pairs), sum(p_[3] for p_ in pairs)
        return dict(out, pairs=[[p_[0], p_[1], med[p_[0]], p_[2], p_[3]] for p_ in pairs],
                    ratio=round(sv / mv, 5), **{"with": "medsl"})
    return None


def two_against_state(kc, t):
    """The orchestrator, 2026-11-13 05:15 (3): "two independent counts that agree by candidate within 0.4% stand
    against one state count that bears no certified mark. The note gives the state's figures. A count with the mark
    wins under 15:16": Klarner's and MEDSL's counts within TWO_AGREE of each other for every candidate, the state's
    (unmarked) off Klarner's by more than TWO_AGREE for one or more. Returns the figures, or None."""
    cs = state_district(kc)
    if not cs or not t.get("matched") or STATE_MARKED.get((kc["state"], kc["year"])):
        return None
    pairs = _state_pairs(kc, cs)
    if not pairs:
        return None
    med = {p_[0]: p_[3] for p_ in t["pairs"]}
    if set(med) != {p_[0] for p_ in pairs}:
        return None
    if not all(_within(med[p_[0]], p_[1], TWO_AGREE) for p_ in pairs):
        return None
    if all(_within(p_[3], p_[1], TWO_AGREE) for p_ in pairs):
        return None
    return dict(_state_meta(kc), pairs=[[p_[0], p_[1], med[p_[0]], p_[2], p_[3]] for p_ in pairs],
                write_ins=[[x["name"], x["votes"]] for x in cs if x["write_in"]])


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
           "rules": {"ratio_off_over": RATIO_OFF, "held_at_or_over": HOLD_GAP, "doubled_within": DOUBLE_TOL,
                     "over_seats_held_over": OVER_SEATS, "over_seats_medsl_within": OVER_SEATS_MEDSL,
                     "two_agree_within": TWO_AGREE, "compound_part_min": PART_MIN},
           "years": {}}
    ups = {sen: collections.Counter((st, y) for st, y, _, _ in {(c["state"], c["year"], c["dname"], c["dno"])
                                                                for c in cs if c["etype"] == "g" and c["sen"] == sen})
           for sen in (0, 1)}

    def all_up(sen, year):   # a chamber with all its seats up: its districts this year at least 90% of its most
        u = ups[sen]         # on the same lines (2012-2020, or 2022 with 2012-2020): Vermont's chambers of 2022 have
        last = 2021 if year < 2022 else 2023   # 16 and 109 districts to 13 and 81 before (81% and 74%) [measured]
        return {st for (st, y) in u if y == year and u[(st, y)] >= 0.9 * max(u.get((st, y_), 0)
                                                                              for y_ in range(2012, last, 2))}
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
        found, tested, two_agree = [], [], []
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
        # where one of them has the contest's own district number and the others other numbers, the contest is that
        # one's: the others matched it by a name alone (Hawaii 2016's House 51, unopposed, on House 36's contest)
        # [worker D3's reading]
        by_id = {id(m): m for _, m in found}
        drop = set()
        for gid, ks in groups.items():
            md = _dkey(by_id[gid]["district"])
            if len(ks) < 2 or not md.isdigit() or not all(str(k_["dno"] or "").isdigit() for k_ in ks):
                continue
            own_ = [k_ for k_ in ks if int(k_["dno"]) == int(md)]
            if len(own_) == 1 and all(int(k_["dno"]) != int(md) for k_ in ks if k_ is not own_[0]):
                for k_ in ks:
                    if k_ is not own_[0]:
                        drop.add(id(k_))
                        tallies["matched only to another district's contest"] += 1
                        status[klarner_id(k_)] = ["matched only to another district's contest", by_id[gid]["district"]]
                groups[gid] = own_
        found = [(kc, m) for kc, m in found if id(kc) not in drop]
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
            if not (kc.get("votes_source") or {}).get("source") and not kc.get("held_reason"):
                two = two_against_state(kc, t)
                if two:
                    two_agree.append({"id": klarner_id(kc), "medsl_file": m["file"], "flagged": bool(
                        t["flag_a"] or t["flag_b"]), "outcome": TWO_OUTCOME, "state_count": two})
                if b_test:   # the over-seats test: a district of its own (a shared contest's precincts are several's)
                    cv = district_cover(kc, m, year, cov, full_upper)
                    tested.append({"id": klarner_id(kc), "state": kc["state"],
                                   "chamber": "state-upper" if kc["sen"] else "state-lower",
                                   "dname": kc["dname"] or None, "dno": kc["dno"] or None,
                                   "post": kc["geopost"] or kc["mmdpost"] or None, "eseats": kc["eseats"],
                                   "medsl_district": m["district"], "medsl_file": m["file"],
                                   "covered": not cv["gaps"] and not cv.get("untested"), **t})
            if not (t["flag_a"] or t["flag_b"]):
                continue
            f = {"id": klarner_id(kc), "state": kc["state"], "chamber": "state-upper" if kc["sen"] else "state-lower",
                 "dname": kc["dname"] or None, "dno": kc["dno"] or None, "post": kc["geopost"] or kc["mmdpost"] or None,
                 "eseats": kc["eseats"], "medsl_district": m["district"], "medsl_file": m["file"],
                 "flags": [x for x, y in (("a", t["flag_a"]), ("b", t["flag_b"])) if y], **t}
            f.update(outcome(kc, t, year, canv, district_cover(kc, m, year, cov, full_upper)))
            flags.append(f)
            tallies[f"flag {'+'.join(f['flags'])}: {f['outcome']}"] += 1
        over, unread = over_seats_pass(year, flags, tallies, tested)
        out["years"][str(year)] = {"tallies": dict(sorted(tallies.items())), "shared_by_state": dict(sorted(shared.items())),
                                   "flags": sorted(flags, key=lambda f: (f["state"], f["chamber"], f["id"])),
                                   "over_seats": {"tested": len([f for f in tested if f["covered"]]),
                                                  "not_read": {"why": OVER_BLANK.format(c="(by state, below)", s="ies"),
                                                               "by_state": unread},
                                                  "over": over},
                                   "two_against_state": two_agree}
        print(year, dict(sorted(tallies.items())))
        import local_volume as V
        with open(os.path.join(V.VNORM, f"districts-status-{year}.json"), "w") as f:
            json.dump(status, f)
    # 22:19: the counties whose district-level and local rows MEDSL's file lacks, for the contests MEDSL's counts are
    # shown for (local_medsl.coverage_gate); 2020's file holds local offices only, with no statewide contest to read by
    out["incomplete_counties"] = {}
    out["statewide_short"] = {}

    def share(v, n, nd, votes):   # the missed precincts' share of the top contest's votes (scaled by n / nd)
        return round(votes * (n / nd if nd else 0) / v["top_votes"], 4) if v["top_votes"] else None

    for year in (2018, 2022, 2024):
        cov = coverage(year)
        inc, sw = {}, {}
        # a state that left an unopposed US House seat off the ballot (D2's record: no votes) has precincts with no
        # US House row by law, so its counties are not read by the House's rows
        with open(os.path.join(REPO, "data", "house", f"{year}.json")) as f:
            off_ballot = sorted({(c["place"]["state"], c["place"]["district"]) for c in json.load(f)["contests"]
                                 if not c.get("special") and not c["result"].get("total_votes")})
        skip = {st for st, _ in off_ballot}
        state_top = collections.Counter()
        for k, v in cov["counties"].items():
            state_top[k.split("|")[0]] += v["top_votes"] or 0
        for k, v in sorted(cov["counties"].items()):
            st, county = k.split("|")
            n_p = v["precincts"]
            if not n_p:
                continue
            have, n, nd, votes = v["families"]["us_house"]
            x = share(v, n, nd, votes)
            # the US House by district, where the county has any (none: an at-large seat, or none on the ballot, as
            # Louisiana and Oklahoma leave an unopposed one off); the chambers are not read here, since several
            # states leave unopposed seats off the ballot or the file (Florida, Oklahoma, Texas and Kansas 2022)
            if st not in skip and have and n / n_p > COVER_GAP and x is not None and x > COVER_GAP:
                inc[k] = {"precincts": n_p, "top": v["top"], "top_votes": v["top_votes"],
                          "short": [["us_house", n, x]],
                          "lower": v["families"]["lower"][1], "upper": v["families"]["upper"][1],
                          "missing_eg": v.get("us_house_eg", {}).get("missing", []),
                          "whole_contests": v.get("whole_contests", [])}
            for key, (n, nd, votes) in v.get("statewide_short", {}).items():
                x = share(v, n, nd, votes)
                if x is not None and x > COVER_GAP:
                    sw.setdefault(st, {}).setdefault(key, {"counties": {}})["counties"][county] = [
                        n, n_p, x, round(x * v["top_votes"])]
        # a statewide contest's district is the state: the votes its rows miss, against the state's (the counties'
        # top contests summed); held at more than 2%, as a county is (22:26 (a)), else kept with a note
        for st, d in sw.items():
            for key, e in d.items():
                e["state_share"] = round(sum(x[3] for x in e["counties"].values()) / state_top[st], 4)
                e["verdict"] = "held" if e["state_share"] > COVER_GAP else "noted"
        out["incomplete_counties"][str(year)] = inc
        out["incomplete_counties"]["off_ballot_" + str(year)] = off_ballot
        out["statewide_short"][str(year)] = sw
    # the precinct names joined to the top contest's before the gate's match (the orchestrator, 2026-11-13 01:04 (1):
    # "Normalize precinct names before the gate's match, list each equivalence, and recompute every county")
    out["precinct_equivalences"] = {
        "about": ("by the year of MEDSL's file and state|county: [the name as a contest's rows give it, the top "
                  "contest's name it is joined to], each 'jurisdiction / precinct'; a name in no row of the county's "
                  "top contest joins the one top-contest name with the same jurisdiction code and the same numbers, "
                  "where their words are equal or, both six letters or more, within two letters' edits or one's words "
                  "among the other's, generic words aside (local_districts.precinct_equivalences)")}
    for y in (2016, 2018, 2022, 2024):
        out["precinct_equivalences"][str(y)] = coverage(y).get("equivalences", {}).get(str(y), {})
    out["spellings"] = {
        "about": ("MEDSL's lines of one contest spelled alike, their names sharing a surname and a given name or "
                  "nickname: summed into one candidate's count where no precinct gives both lines votes, a row named "
                  "as a total not counted a precinct (the orchestrator, 2026-11-13 04:44: \"Sum the lines where their "
                  "precincts are apart and the names share a surname and a given name, and list each pair. A name "
                  "split by county is one candidate's count\"); by year: lines [name, votes, precincts with votes, "
                  "counties], summed, and why not where they are not (local_districts.merge_spellings)")}
    for y in YEARS:
        out["spellings"][str(y)] = SPELLINGS.get(y, [])
    out["census_block_files"] = {"about": "the 2022 lines' counties of each district (census_counties)",
                                 "url": CENSUS_URL, "linked_from": CENSUS_PAGE,
                                 "files": {k: {x: m.get(x) for x in ("url", "finished_utc", "bytes", "sha256")}
                                           for k, m in _census_metas().items()}}
    out["incomplete_counties"]["about"] = (
        "counties where the US House's rows (by district, where the county has any) miss more than 2% of the precincts "
        "of the county's top contest (the most precincts with votes), holding more than 2% of its votes: [family, "
        "precincts missed, share of the top contest's votes]; with the chambers' precincts missed beside, not read "
        "since several states leave unopposed seats off the ballot or the file; a state that left a US House seat "
        "off the ballot (off_ballot_<year>, from data/house) is not read. Their "
        "district-level and local rows are missing (MEDSL's 2024 Monroe County: the Assembly's rows miss 185 of 655 "
        "precincts and the US House's 200, M2's seventh pass; the orchestrator, 22:19 item 1). Precincts missed are "
        "counted as the set difference but no more than the difference in counts, since a file can name one precinct "
        "apart in two contests, and their votes are the set difference's scaled by the ratio of the two [worker D3's "
        "reading]. whole_contests: the contests whose own rows are in the county's precincts (within 2%), so their "
        "district is the county and their rows are not missing in it: not held by the county [worker D3's reading]. "
        "missing_eg: up to eight of the precincts missed. 2020 untested: MEDSL's file holds local offices only")
    out["statewide_short"]["about"] = (
        "statewide contests (rows in 90% of the state's counties) whose rows miss more than 2% of a county's top "
        "contest's precincts, holding more than 2% of its votes: state -> office|district -> counties -> county -> "
        "[precincts missed, the county's precincts, share of the top contest's votes, those votes]; state_share: "
        "the votes missed against the state's (the counties' top contests summed). Held by local_medsl.coverage_gate "
        "where state_share is over 2% (the district is the state; 22:19 item 1: \"any contest whose rows are "
        "missing in part of its district\"), else kept with a note, unless the state's own count is read [worker "
        "D3's reading]")
    with open(CHECK, "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
        f.write("\n")
    return out


# A district whose count all of MEDSL's lines confirm, with one candidate's votes on the file's WRITE-IN line, where
# no source read says whether that candidate was on the ballot (the orchestrator, 2026-11-13 01:04 (3), on M2's
# reading of Michigan 2022: "The count is confirmed. Before p returns, read whether Corcoran was on the ballot; if he
# was a write-in, the write-in rule applies"; Michigan's Secretary of State refused on 11-07 and Wayne County's Clerk
# gave an empty reply at 01:25:44 UTC on 11-13, so it is not read). {Klarner id: (the candidate, Klarner's surname key)}.
# A district whose gap one county's own official results fill (the orchestrator, 2026-11-13 01:15 (1): "For HD27, SD12
# and HD99, one request each to the clerk of the county where the gap lies, if you can tell which"; a county clerk is
# another agency than the Secretary of State, which refused). Michigan 2022's House 99: MEDSL's lines are in six
# counties, and in Arenac (26011) its 2,160 for Mike Hoadley are 0.30 of the governor's votes in the same precincts,
# against 0.95 to 0.98 in the other five [measured], so the gap lies in Arenac; its clerk's file, headed "Official",
# gives Kenneth A. Kish (DEM) 2,160 and Mike Hoadley (REP) 4,847, and 15 unresolved write-ins [stated: the file]. MEDSL
# files Kish's Arenac figure under Hoadley's name and lacks Hoadley's. {Klarner id: the reading}.
COUNTY_READ = {"2022-MI-lower--99--": {
    "county": "26011", "clerk": "Arenac County Clerk",
    "url": "https://arenaccountymi.gov/docs/Clerk/Election%20Results/2022/Official%20Nov%208,%202022%20Election"
           "SummaryReportRPT.pdf",
    "read_utc": "2026-11-13T02:22:25Z",
    "sha256": "113c24ce1c2bb601ae1f3d64f046db1b72b28f7e2545b7bc5707b302c10a270d",
    "title": "Election Summary Report, General Election, Arenac County, Michigan, November 08, 2022, Official",
    "official": {"kish": 2160, "hoadley": 4847}, "write_ins": 15,
    "medsl_in_county": {"kish": 0, "hoadley": 2160}}}


def county_read(kc, t):
    """For COUNTY_READ: MEDSL's lines with the county's own official figures in place of MEDSL's for that county; if
    each candidate's sum then equals Klarner's, Klarner's count stands; else the build stops."""
    e = COUNTY_READ[klarner_id(kc)]
    pairs = []
    for p_ in t["pairs"]:
        sur = p_[0].split(",")[0].strip()
        if sur not in e["official"]:
            raise SystemExit(f"county_read: {klarner_id(kc)}: {sur} is not in the county's reading")
        with_county = p_[3] - e["medsl_in_county"][sur] + e["official"][sur]
        if with_county != p_[1]:
            raise SystemExit(f"county_read: {klarner_id(kc)}: {sur}: {with_county} against Klarner's {p_[1]}")
        pairs.append([p_[0], p_[1], p_[3], with_county])
    return {"outcome": "settled by the county: Klarner's count stands", "by": e["clerk"],
            "county_count": {k: e[k] for k in ("county", "clerk", "url", "read_utc", "sha256", "title", "official",
                                                 "write_ins", "medsl_in_county")}, "county_pairs": pairs}


BALLOT_UNREAD = {"2022-MI-lower--10--": ("Mark Corcoran", "corcoran")}
BALLOT_UNREAD_TOL = 0.01   # all of MEDSL's lines, the WRITE-IN line with them, within 1% of Klarner's count


def ballot_unread(kc, t):
    """For BALLOT_UNREAD: the figures, if the WRITE-IN line makes up the candidate's gap and all lines confirm Klarner's
    count; else the build stops (the record is not the one the ruling read)."""
    who, key = BALLOT_UNREAD[klarner_id(kc)]
    pr = [p_ for p_ in t["pairs"] if p_[0].split(",")[0].strip() == key]
    if len(pr) != 1:
        raise SystemExit(f"ballot_unread: {klarner_id(kc)}: {who} not paired once")
    all_lines = t["medsl"] + t["medsl_write_ins"]
    gap = pr[0][1] - pr[0][3]
    if abs(all_lines / t["klarner"] - 1) > BALLOT_UNREAD_TOL or abs(t["medsl_write_ins"] / gap - 1) > 0.05:
        raise SystemExit(f"ballot_unread: {klarner_id(kc)}: the WRITE-IN line no longer makes up {who}'s votes")
    return {"outcome": "held: whether a candidate was on the ballot is not read", "who": who,
            "klarner_votes": pr[0][1], "medsl_named": pr[0][3], "write_in_line": t["medsl_write_ins"],
            "all_lines": all_lines}


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
    s_ = settle_agree(kc, t)
    if s_ and s_["with"] == "klarner":
        return {"outcome": "settled by the state: Klarner's count stands", "by": s_["source"], "state_count": s_}
    if s_ and s_["with"] == "medsl" and not [x for x in t["others"] if not x["write_in"]]:
        return {"outcome": "settled by the state: MEDSL's count stands", "by": s_["source"], "state_count": s_}
    if klarner_id(kc) in BALLOT_UNREAD:
        return ballot_unread(kc, t)
    if klarner_id(kc) in COUNTY_READ:
        return county_read(kc, t)
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
                       "candidates not paired": "its candidates do not pair one to one; untested here",
                       "matched only to another district's contest": "the one MEDSL contest that names its candidates "
                                                                     "is another district's, by its number; untested "
                                                                     "here"}.get(
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
