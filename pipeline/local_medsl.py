"""pipeline/local_medsl.py: contests from MEDSL's precinct returns (pipeline/intake/medsl_precinct.py) into data/.

Written 2026-11-07 by worker D3 (briefs/D3-data-local.md, steps 3 to 6), beside pipeline/local.py, whose method it uses.

  state legislatures, 2024   route (a) of method D3-v1.1 (pipeline/local.py), fitted on Klarner's 1967-2022 races
                             (earlier years only); the seat's last result is its 2022 result where its lines are
                             unchanged (measured: the precincts it covers in 2024 and 2022), else class C
  state legislatures, 2022   a second source for Klarner's 2022 returns: both read, the differences listed (plan 3a)
  local races, 2022 and 2024 routes (b) and (c), like past races, classed by office and structure; each year from the
                             like races of earlier years in the sources taken in
  measures, 2022 and 2024    recorded; p awaits the measure's threshold and a forecast route (brief step 4)

Files: data/<level>/<year>/<ST>.json, compact, one contest per line, as pipeline/local.py writes them.

Run:  VOTE_CACHE=/tmp/vote-cache python3 pipeline/local_medsl.py check2022
      VOTE_CACHE=/tmp/vote-cache python3 pipeline/local_medsl.py build [--out DIR]
"""
import argparse
import collections
import datetime
import glob
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import core  # noqa: E402
import fetch as F  # noqa: E402
import local as L  # noqa: E402

NORM = os.path.join(F.CACHE, "medsl", "normalized")
SAME_LINES = 0.8          # share of a district's 2024 precincts also in its 2022 precincts for "lines unchanged"
LEG = {"STATE HOUSE": 0, "STATE SENATE": 1}
YEARS = (2022, 2024)


# ------------------------------------------------------------------ inputs

_WA_LEG = re.compile(r"^LEGISLATIVE DISTRICT (\d+) - STATE (SENATOR|REPRESENTATIVE)(?: POS\.? ?(\d+))?")


def relabel(m):
    """Washington files its legislature as local offices named by district ('LEGISLATIVE DISTRICT 9 - STATE
    REPRESENTATIVE POS. 1'): read as the state house or senate, the district and the position."""
    x = _WA_LEG.match(m["office"])
    if x:
        m["office_as_filed"] = m["office"]
        m["office"] = "STATE SENATE" if x.group(2) == "SENATOR" else "STATE HOUSE"
        m["district"] = x.group(1)
        m["post"] = x.group(3)
        m["dataverse"] = "STATE"
    return m


EMPTY = collections.Counter()   # contests with no vote anywhere: lines a file lists for every precinct, left out


def load(year):
    out = []
    for path in sorted(glob.glob(os.path.join(NORM, str(year), "*.jsonl"))):
        with open(path) as f:
            for line in f:
                c = relabel(json.loads(line))
                if not any(x["votes"] for x in c["candidates"]):
                    EMPTY[year] += 1
                    continue
                out.append(c)
    return out


def leg_key(m):
    return (m["state"], m["office"], district_no(m["district"]) or m["district"], m.get("post"))


YES_WORDS = {"YES", "FOR", "APPROVE", "APPROVED", "ACCEPT", "RETAIN", "BONDS YES", "YES ON", "FOR THE MEASURE",
             "IN FAVOR", "IN FAVOR OF", "YES FOR APPROVAL"}
NO_WORDS = {"NO", "AGAINST", "REJECT", "REJECTED", "NOT RETAIN", "DO NOT RETAIN", "BONDS NO", "NO ON",
            "AGAINST THE MEASURE", "OPPOSED", "NO FOR REJECTION"}
GOVERNOR = re.compile(r"^GOVERNOR\b(?! *'S COUNCIL)")   # D2's level; a lieutenant governor or a council stays here


def checks(year):
    with open(os.path.join(NORM, f"checks-{year}.json")) as f:
        return json.load(f)


QUALITY_LINE = 0.005   # a state whose federal totals, added up from MEDSL's precincts, miss the certified ones by more
RCV_EXPLAINED = {"ME": "Maine counts its federal races by ranked choice, and MEDSL's precinct counts are first-round "
                       "counts (its README); its state and local races are not counted that way"}


SPREADSHEET_ROWS = 1048575   # 2**20 rows less a header: a file of exactly this length was likely cut by a spreadsheet
RANKED = {"AK": "counted by ranked choice (Alaska's state offices from 2022; MEDSL's 2022 README: its counts are the "
                "first choices before any redistribution): a vote works through the rounds, so p is not computed "
                "(model section 7); recorded with its first-choice counts"}


KLARNER_LINE = 0.10   # 2022: a state where more than this share of districts differ from Klarner's (share or parties) is unsound


def quality(year):
    """{state: reason} for states whose MEDSL counts cannot be trusted to add up. 2024: the same files' presidential
    totals, added up from the precincts, against D1's certified totals (by candidate). 2022: the same files' state
    legislative districts against Klarner's 2022 returns (check_2022), the record for them. A file of exactly a
    spreadsheet's row limit, in any year. (The US House check in the intake's checks is kept as a diagnostic, not used
    here: D2's totals include blank-ballot lines in some states and name parties in words that vary, so they do not
    compare line for line.)"""
    chk = checks(year)
    out = {}
    for name, f in chk.get("files", {}).items():
        if f.get("rows_read") == SPREADSHEET_ROWS:
            for st in f.get("states", {}):
                out[st] = (f"the source's {year} file for this state ({name}) has {SPREADSHEET_ROWS:,} rows, the most a "
                           f"spreadsheet holds, so it is likely cut short [inferred]; p not computed")
    if year % 4 == 0:
        for st, rs in (chk.get("president") or {}).items():
            if st in out or not isinstance(rs, list):
                continue
            worst = None
            for r in rs:
                if not r.get("certified"):
                    continue
                rel = abs((r.get("medsl_precincts") or 0) - r["certified"]) / r["certified"]
                if worst is None or rel > worst[0]:
                    worst = (rel, r)
            if worst and worst[0] > QUALITY_LINE and st not in RCV_EXPLAINED:
                out[st] = (f"the source's {year} counts for this state do not add up to the certified presidential "
                           f"totals (off by {100 * worst[0]:.1f}% for {worst[1].get('candidate')}, "
                           f"pipeline/intake/medsl_precinct.py's check), so its counts for this contest may be "
                           f"incomplete or double-counted; p not computed")
    elif year == 2022:
        path = os.path.join(L.REPO, "data", "local", "check-2022-medsl-klarner.json")
        if os.path.exists(path):
            with open(path) as f:
                kc = json.load(f)
            for st, t in kc.get("by_state", {}).items():
                if st in out or not t.get("matched"):
                    continue
                off = (t.get("two-party share differs by more than 1 point", 0)
                       + t.get("a major party's candidate in one source only", 0)) / t["matched"]
                if off > KLARNER_LINE:
                    out[st] = (f"the source's {year} state legislative returns for this state differ from Klarner's "
                               f"in the two-party share by more than 1 point, or in which major parties ran, in "
                               f"{100 * off:.0f}% of its {t['matched']} districts compared "
                               f"(data/local/check-2022-medsl-klarner.json), so its counts are not relied on")
    return out


def _letters(s):
    return re.sub(r"[^A-Z]", "", s.upper())


SUFFIXES = {"JR", "SR", "II", "III", "IV", "V"}


def name_key(name):
    """(surname, first initial), from MEDSL's 'FIRST MIDDLE LAST' or Klarner's 'last, first middle'."""
    n = re.sub(r'"[^"]*"|\([^)]*\)', " ", name.upper()).replace(".", " ")
    if "," in n:
        last, rest = n.split(",", 1)
        first = [t for t in rest.split() if _letters(t) and _letters(t) not in SUFFIXES]
        return _letters(last), (_letters(first[0])[:1] if first else "")
    toks = [t for t in n.split() if _letters(t) and _letters(t) not in SUFFIXES]
    if not toks:
        return "", ""
    return _letters(toks[-1]), _letters(toks[0])[:1]


def name_keys(name):
    """name_key, and for 'FIRST MIDDLE LAST' also the last two words run together, as Klarner writes a compound
    surname ('duncanmoore, parker' for PARKER DUNCAN MOORE)."""
    k = name_key(name)
    out = {k}
    if "," not in name:
        n = re.sub(r'"[^"]*"|\([^)]*\)', " ", name.upper()).replace(".", " ")
        toks = [_letters(t) for t in n.split() if _letters(t) and _letters(t) not in SUFFIXES]
        if len(toks) >= 3:
            out.add((toks[-2] + toks[-1], k[1]))
    return out


def major(c):
    p = (c.get("party") or "").upper()
    return "D" if p == "DEMOCRAT" else "R" if p == "REPUBLICAN" else None


def _is_generic(name):
    n = name.strip().upper()
    return n in {"WRITE-IN", "WRITEIN", "WRITE IN", "SCATTERING", "WRITE-INS"} or n.startswith("*") or "WRITE" in n


def ballot(cands):
    """Candidates on the ballot: not write-ins, not write-in totals."""
    return [c for c in cands if not c.get("writein") and not _is_generic(c["name"])]


def district_no(d):
    m = re.fullmatch(r"0*(\d+)", d or "")
    return m.group(1) if m else None


# ------------------------------------------------------------------ 2022: MEDSL beside Klarner

def check_2022(klarner=None, medsl=None):
    """Single-member districts both sources name the same way (a number, no county name or post): are the
    Democrat's and the Republican's votes, and the winner, the same? Returns the tallies and every difference."""
    klarner = klarner or L.load_klarner()
    medsl = medsl or load(2022)
    kl = {}
    for c in klarner:
        if c["year"] == 2022 and c["etype"] == "g" and c["eseats"] == 1 and not c["dname"] and not c["geopost"] \
                and not c["mmdpost"] and c["dno"]:
            kl[(c["state"], c["sen"], c["dno"])] = c
    out = collections.Counter()
    by_state = collections.defaultdict(collections.Counter)
    diffs = []
    for m in medsl:
        if m["office"] not in LEG or m["stage"] != "GEN" or m["special"] or m.get("magnitude") not in (1, None):
            continue
        dn = district_no(m["district"])
        k = (m["state"], LEG[m["office"]], dn)
        if dn is None or k not in kl:
            out["medsl contest without a like-named Klarner contest"] += 1
            continue
        out["matched"] += 1
        by_state[k[0]]["matched"] += 1
        c = kl[k]
        kd = sum(a["votes"] or 0 for a in c["cands"] if a["party"] == "d")
        kr = sum(a["votes"] or 0 for a in c["cands"] if a["party"] == "r")
        md = sum(x["votes"] for x in m["candidates"] if major(x) == "D" and not x.get("writein"))
        mr = sum(x["votes"] for x in m["candidates"] if major(x) == "R" and not x.get("writein"))
        kw = max((a for a in c["cands"] if not a["scattering"]), key=lambda a: a["votes"] or 0, default=None)
        mw = max(ballot(m["candidates"]) or m["candidates"], key=lambda x: x["votes"], default=None)
        same_winner = bool(kw and mw and name_key(kw["name"])[0] in {k[0] for k in name_keys(mw["name"])})
        out["same winner" if same_winner else "winner differs"] += 1
        by_state[k[0]]["same winner" if same_winner else "winner differs"] += 1
        # the two-party share is what the forecast reads; a count scaled the same for both (one source doubling a
        # district) leaves it whole, so the share is compared, and the scale is listed
        if kd == md and kr == mr:
            word = "D and R votes identical"
        elif (kd > 0) != (md > 0) or (kr > 0) != (mr > 0):
            word = "a major party's candidate in one source only"
        elif abs(kd / (kd + kr) - md / (md + mr)) <= 0.01:
            word = "two-party share within 1 point, counts differ"
        else:
            word = "two-party share differs by more than 1 point"
        out[word] += 1
        by_state[k[0]][word] += 1
        if word != "D and R votes identical":
            tot = max(kd + kr, 1)
            diffs.append({"state": k[0], "chamber": "state-upper" if k[1] else "state-lower", "district": dn,
                          "klarner": [kd, kr], "medsl": [md, mr], "relative": round((abs(kd - md) + abs(kr - mr)) / tot, 4),
                          "medsl_over_klarner": round((md + mr) / tot, 3), "what": word, "same_winner": same_winner})
    diffs.sort(key=lambda d: -d["relative"])
    return {"tallies": dict(out), "by_state": {s_: dict(v) for s_, v in sorted(by_state.items())},
            "differences": diffs}


# ------------------------------------------------------------------ 2024 state legislatures, route (a)

def _two_party(m):
    b = ballot(m["candidates"])
    d = [x for x in b if major(x) == "D"]
    r = [x for x in b if major(x) == "R"]
    return b, d, r


def leg_rows_2024(m24, m22, klarner):
    """Route (a) rows for 2024's single-seat general races with one Democrat and one Republican on the ballot."""
    by22 = {}
    for m in m22:
        if m["office"] in LEG and m["stage"] == "GEN" and not m["special"]:
            by22[leg_key(m)] = m
    # sitting members by name: the 2022 winners (MEDSL) and Klarner's winners of 2020 to 2022, by state and chamber
    sitting = collections.defaultdict(set)
    for m in m22:
        if m["office"] in LEG and m["stage"] == "GEN":
            b = ballot(m["candidates"])
            k = m.get("magnitude") or 1
            for x in sorted(b, key=lambda x: -x["votes"])[:k]:
                if major(x):
                    sitting[(m["state"], LEG[m["office"]])].add(name_key(x["name"]) + (major(x),))
    for c in klarner:
        if c["year"] in (2020, 2021, 2022) and c["etype"] in ("g", "gs", "ssg"):
            for a in c["cands"]:
                if a["outcome"] == "w" and a["party"] in ("d", "r"):
                    sitting[(c["state"], c["sen"])].add(name_key(a["name"]) + (a["party"].upper(),))
    # the chamber's lean: Klarner's previous election of the chamber (mean D share of its contested seats)
    prow = L.partisan_rows(klarner)
    shares = collections.defaultdict(list)
    for r_ in prow:
        shares[(r_["state"], r_["sen"], r_["year"])].append(r_["y"])
    lean = {}
    for (s, sen, t), v in shares.items():
        if t >= 2024:
            continue
        if (s, sen) not in lean or t > lean[(s, sen)][1]:
            lean[(s, sen)] = (sum(v) / len(v) - 0.5, t)
    rows = []
    for m in m24:
        if m["office"] not in LEG or m["stage"] != "GEN" or m["special"] or (m.get("magnitude") or 1) != 1:
            continue
        b, d, r = _two_party(m)
        if len(d) != 1 or len(r) != 1 or d[0]["votes"] <= 0 or r[0]["votes"] <= 0:
            continue
        sen = LEG[m["office"]]
        prev = by22.get(leg_key(m)) if m["district"] not in ("", "STATEWIDE") else None
        lines = None
        cls, xl, ulag, last = "C", 0.0, 0, None
        if prev and prev.get("precinct_ids") and m.get("precinct_ids"):
            a24, a22 = set(m["precinct_ids"]), set(prev["precinct_ids"])
            lines = len(a24 & a22) / max(len(a24), 1)
            if lines >= SAME_LINES:
                pb, pd, pr = _two_party(prev)
                dv = sum(x["votes"] for x in pd)
                rv = sum(x["votes"] for x in pr)
                if dv > 0 and rv > 0:
                    cls, xl, last = "A", dv / (dv + rv) - 0.5, dv / (dv + rv)
                elif dv > 0 or rv > 0:
                    cls, ulag, last = "B", (1 if dv > 0 else -1), ("D" if dv > 0 else "R")
        inc = 0
        st_sit = sitting.get((m["state"], sen), set())
        if any(k + ("D",) in st_sit for k in name_keys(d[0]["name"])):
            inc += 1
        if any(k + ("R",) in st_sit for k in name_keys(r[0]["name"])):
            inc -= 1
        Lv = lean.get((m["state"], sen))
        rows.append({"m": m, "year": 2024, "state": m["state"], "sen": sen,
                     "y": d[0]["votes"] / (d[0]["votes"] + r[0]["votes"]), "N": d[0]["votes"] + r[0]["votes"],
                     "cls": cls, "xl": xl, "ulag": ulag, "inc": inc, "L": Lv[0] if Lv else 0.0,
                     "L_year": Lv[1] if Lv else None, "Lmiss": 0 if Lv else 1, "lines": lines, "last": last,
                     "d": d[0], "r": r[0], "ballot": b})
    return rows


def leg_structure(m):
    """(route, class key or reason) for a MEDSL state legislative general, in the classes pipeline/local.py's
    structure() gives Klarner's generals, so that like races of 1967-2022 forecast it. Ex ante: who is on the ballot."""
    b = ballot(m["candidates"])
    k = m.get("magnitude") or 1
    if len(b) <= k:
        return ("zero", "one name on the ballot for each seat (unopposed): p is 0")
    nd = sum(1 for x in b if major(x) == "D")
    nr = sum(1 for x in b if major(x) == "R")
    if k > 1:
        slate = ("both major parties running a full slate" if nd >= k and nr >= k else
                 "both major parties running, one short of a full slate" if nd and nr else
                 "one major party or none against the others")
        return ("boundary", f"general, {k if k < 4 else '4+'} seats at once, {slate}")
    if nd == 1 and nr == 1:
        return ("partisan", None)
    if nd + nr == 0:
        if all((x.get("party") or "") == "NONPARTISAN" for x in b):
            return ("class", "general, nonpartisan")
        return ("class", "general, no Democrat or Republican on the ballot")
    if nd + nr == 1:
        return ("class", "general, one major party against minor parties or independents")
    return ("class", "general, two candidates of one major party")


def strong_write_in(cands, seats):
    """An unopposed race where write-ins got at least L.WRITE_IN_STRONG of the last winner's votes: the share, else
    None. MEDSL mostly counts write-ins together, so a total that large counts too."""
    b = sorted(ballot(cands), key=lambda x: -x["votes"])
    last = b[seats - 1]["votes"] if len(b) >= seats else 0
    w = sorted((x for x in cands if x.get("writein") or _is_generic(x["name"])), key=lambda x: -x["votes"])
    if w and w[0]["votes"] > 0 and w[0]["votes"] >= max(1, L.WRITE_IN_STRONG * last):
        return w[0]["votes"] / last if last else None, _is_generic(w[0]["name"])
    return None


def class_p(rec, c, route, key, train, dens, cache_key, commit, with_p, counts, label, pair_k):
    """Routes (b) and (c) for one contest: the deciding pair, the class density from like races of earlier years,
    p. Returns the p block."""
    top = sorted(c["candidates"], key=lambda x: -x["votes"])
    if any(x.get("writein") or _is_generic(x["name"]) for x in top[pair_k - 1:pair_k + 1]):
        counts[f"{label}: not computed, write-in in the deciding pair"] += 1
        return {"not_computed": "a write-in line is in the pair that decided this contest; the like-race classes "
                                "are of candidates on the ballot"}
    b = sorted(ballot(c["candidates"]), key=lambda x: -x["votes"])
    pair = b[pair_k - 1:pair_k + 1]
    if len(pair) < 2 or pair[0]["votes"] + pair[1]["votes"] <= 0:
        counts[f"{label}: not computed, no votes"] += 1
        return {"not_computed": "no votes for the deciding pair"}
    n = pair[0]["votes"] + pair[1]["votes"] - 1
    rec["boundary" if route == "boundary" else "two_party"] = {
        "votes": [pair[0]["votes"], pair[1]["votes"]], "n_other_voters": n,
        "share_first": round(pair[0]["votes"] / (n + 1), 6)}
    if cache_key not in dens:
        dens[cache_key] = L.class_density(train, key)
    f, N, h, kin = dens[cache_key]
    if f is None:
        counts[f"{label}: not computed, too few like races"] += 1
        return {"not_computed": f"fewer than {L.MIN_CLASS} like races in earlier years in the sources taken in "
                                f"({N}) for the class '{key}'"}
    fc = {"by": "the model's own", "method": L.METHOD, "route": route, "class": key, "like_races": N,
          "window": [round(0.5 - h, 2), round(0.5 + h, 2)], "in_window": kin, "q": round(f * 2 * h, 5),
          "source": "model"}
    if route == "boundary":
        fc["note"] = "not yet checked"
    rec["forecasts"].append(fc)
    if not with_p:
        return {}
    if f <= 0:
        return {"value": 0.0, "event": 0.0, "reason": f"no like race in {N} finished within the window"}
    counts[f"{label}: p computed, {route}"] += 1
    sd_eq = 1.0 / (math.sqrt(2 * math.pi) * f)
    return L._p_block(n, 0.5, sd_eq, f"the model's own ({L.METHOD}), like past races", commit)


# ------------------------------------------------------------------ local races: classes of like races

OFFICE_TYPES = [
    ("school board", r"SCHOOL|BOARD OF EDUCATION|COLLEGE|EDUCATION|TRUSTEE|UNIVERSITY|REGENT"),
    ("judge", r"JUDGE|JUSTICE|COURT|MAGISTRATE|PROBATE"),
    ("prosecutor", r"ATTORNEY|PROSECUTOR|SOLICITOR"),
    ("sheriff or constable", r"SHERIFF|CONSTABLE|MARSHAL|POLICE"),
    ("mayor or executive", r"MAYOR|EXECUTIVE|JUDGE EXECUTIVE|FIRST SELECTMAN"),
    ("special district", r"DISTRICT DIRECTOR|WATER|FIRE|HOSPITAL|HEALTH|PARK|SANITARY|UTILITY|IRRIGATION|TRANSIT|"
                         r"AIRPORT|PORT|LIBRARY|CEMETERY|SOIL|CONSERVATION|DRAINAGE|LEVEE|MOSQUITO|TRANSPORTATION"),
    ("clerk, treasurer or other county officer", r"CLERK|TREASURER|ASSESSOR|RECORDER|REGISTRAR|REGISTER|COLLECTOR|"
                                                r"AUDITOR|CORONER|SURVEYOR|APPRAISER|SUPERVISOR OF ELECTIONS|"
                                                r"COMPTROLLER|CONTROLLER|ENGINEER|SUPERINTENDENT"),
    ("council, commission or board", r"COUNCIL|ALDERM|COMMISSION|SUPERVISOR|SELECT|LEVY COURT|BOARD|TRUSTEE|"
                                     r"FREEHOLDER|LEGISLAT|REPRESENTATIVE|DELEGATE|ASSEMBLY|WARD|MEMBER"),
]


def office_type(office):
    o = office.upper()
    for name, pat in OFFICE_TYPES:
        if re.search(pat, o):
            return name
    return "other local office"


def local_structure(m):
    """(route, class key or reason) for a MEDSL local candidate contest; ex ante: who is on the ballot."""
    b = ballot(m["candidates"])
    k = m.get("magnitude")
    if k is None:
        return ("not computed", "the number of seats is not verified in the source (MEDSL's magnitude is empty)")
    if m["special"]:
        return ("not computed", "a special election: the model's own forecasts are fitted to regular elections")
    if "RECOUNT" in m["stage"]:
        return ("not computed", "a recount's count, recorded beside the general's")
    if m["stage"] != "GEN":
        return ("not computed", f"a {m['stage'].lower()} contest: {L.METHOD} classes local races at general elections")
    if len(b) <= k:
        return ("zero", "one name on the ballot for each seat (unopposed): p is 0")
    if any(x.get("votes_missing_in_some_precincts") for x in b):
        return ("not computed", "the source redacts some precincts' counts for this contest")
    nd = sum(1 for x in b if major(x) == "D")
    nr = sum(1 for x in b if major(x) == "R")
    ot = office_type(m["office"])
    scope = "state" if m["dataverse"] == "STATE" else "local"
    if k > 1:
        slate = ("both major parties on the ballot" if nd and nr else "one major party or none")
        return ("boundary", f"{scope} {ot}, {k if k < 4 else '4+'} seats at once, {slate}")
    if nd == 1 and nr == 1:
        return ("not computed", f"a {scope} race between a Democrat and a Republican: the model's own forecast for "
                                f"these needs the place's partisan lean, which {L.METHOD} has at state legislative "
                                f"level only")
    nonpartisan = all((x.get("party") or "NONPARTISAN") in ("NONPARTISAN", "") for x in b)
    kind = ("nonpartisan" if nonpartisan else "one major party against others" if nd + nr == 1 else
            "two or more of one major party" if nd + nr >= 2 else "no Democrat or Republican")
    n = len(b)
    return ("class", f"{scope} {ot}, {kind}, {n if n < 4 else '4+'} candidates")


def is_local_level(m):
    """Contests written to data/local/: local offices, and the state's other offices (its courts, boards and
    statewide officers), which plan section 3 gives no level of their own; not the legislature, not the governor."""
    return not m["question"] and m["office"] not in LEG and not GOVERNOR.match(m["office"])


def local_rows(contests):
    rows = []
    for m in contests:
        if not is_local_level(m):
            continue
        route, key = local_structure(m)
        if route not in ("class", "boundary"):
            continue
        b = sorted(ballot(m["candidates"]), key=lambda x: -x["votes"])
        kk = m["magnitude"] if route == "boundary" else 1
        x1, x2 = b[kk - 1]["votes"], b[kk]["votes"]
        if x1 + x2 <= 0:
            continue
        rows.append({"m": m, "key": key, "s": max(x1, x2) / (x1 + x2), "n": x1 + x2, "route": route})
    return rows


# ------------------------------------------------------------------ build

def _party_word(x):
    p = (x.get("party") or "").upper()
    if p == "DEMOCRAT":
        return "D"
    if p == "REPUBLICAN":
        return "R"
    if p == "DEMOCRAT AND REPUBLICAN":
        return "D and R"
    if x.get("writein") or _is_generic(x["name"]):
        return "write-in"
    if p in ("", "NONPARTISAN"):
        return "nonpartisan" if p else None
    return (x.get("party_detailed") or p).lower()


def _cands_out(cands, seats=1):
    b = sorted(cands, key=lambda x: -x["votes"])
    order = sorted(ballot(cands), key=lambda x: -x["votes"])
    # MEDSL does not mark winners: the leading candidates on the ballot are taken as won [inferred], except at a tie
    tie = len(order) > seats and order[seats - 1]["votes"] == order[seats]["votes"]
    winners = set() if tie else {id(x) for x in order[:seats]}
    out = []
    for x in b:
        c = {"name": x["name"].title() if not _is_generic(x["name"]) else x["name"], "party": _party_word(x),
             "votes": x["votes"], "won": True if id(x) in winners else None}
        if x.get("votes_missing_in_some_precincts"):
            c["votes_incomplete"] = True
        if x.get("lines"):   # a candidate on several parties' lines, or spelled differently by county: each line
            c["lines"] = [{k: v for k, v in (("name", ln["name"].title() if ln.get("name") else None),
                                             ("party", _party_word({"name": "", **ln})), ("votes", ln["votes"]))
                           if v is not None} for ln in x["lines"]]
        out.append(c)
    return out


def _src_medsl(year, chk, files):
    doi = {2024: "doi:10.7910/DVN/NYTPDU", 2022: "doi:10.7910/DVN/UYQIEP"}[year]
    rec = chk.get("record", {})
    return F.source(f"MIT Election Data and Science Lab, Precinct-Level Returns {year} by Individual State, Harvard "
                    f"Dataverse {doi}, version {rec.get('version')}", f"https://doi.org/{doi.split(':', 1)[1]}",
                    rec.get("read_utc"), "CC0 1.0", mark="stated", via=f"https://doi.org/{doi.split(':', 1)[1]}",
                    note="precinct returns compiled by MEDSL from each state's official sources (named per state in "
                         "its README); added up to the contest by pipeline/intake/medsl_precinct.py, files "
                         + ", ".join(sorted(files)))


def build(out_dir, with_p=True):
    commit = L.git_commit()
    klarner = L.load_klarner()
    pres, nara_rows = L.president_party()
    m = {y: load(y) for y in YEARS}
    chk = {y: checks(y) for y in YEARS}
    files = collections.defaultdict(list)
    counts = collections.Counter()
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    src_model = F.source(f"the model's own forecast, method {L.METHOD}",
                         "https://github.com/zwolk46/vote/blob/main/data/local/REPORT.md", now, None, mark="inferred",
                         note="each year forecast from a fit on earlier years only; no polls are used")
    src_nara = F.source("National Archives, Electoral College Results (the sitting president's party)",
                        "https://www.archives.gov/electoral-college", nara_rows[0]["source"]["read_utc"],
                        "US federal public record; no licence printed", mark="stated")
    info = L.klarner_info()
    src_klarner = F.source(f"Carl Klarner, State Legislative Election Returns, 1967-2022, Harvard Dataverse "
                           f"{info['doi']}, {info['version']} (the races route (a) is fitted on)",
                           "https://doi.org/10.7910/DVN/FJOGJB", info["files"]["candidate"]["read_utc"], info["licence"],
                           mark="stated")
    bad = {y: quality(y) for y in YEARS}
    seen = set()

    def cid(base):
        x, k = base, 2
        while x in seen:
            x = f"{base}~{k}"
            k += 1
        seen.add(x)
        return x

    # -- state legislatures, 2024: route (a)
    prow = [r_ for r_ in L.partisan_rows(klarner) if r_["year"] in pres]
    M, kfit = L.fit_before(prow, pres, 2024)
    m22_sound = [c for c in m[2022] if c["state"] not in bad[2022]]   # last results and like races: sound states only
    rows24 = {id(r_["m"]): r_ for r_ in leg_rows_2024(m[2024], m22_sound, klarner)}
    ktrain = [r_ for r_ in L.class_rows(klarner) if r_["year"] < 2024]   # like races of earlier years only
    kdens = {}
    pieces = collections.Counter(leg_key(c) + (c["stage"], c["special"]) for c in m[2024]
                                 if c["office"] in LEG and not c["question"])
    for year in YEARS:
        for c in m[year]:
            if c["office"] not in LEG or c["question"]:
                continue
            level = "state-upper" if LEG[c["office"]] else "state-lower"
            if year == 2022:
                continue   # Klarner's 2022 is the record; MEDSL's 2022 is its check (check_2022)
            dist = district_no(c["district"]) or (c["district"] if c["district"] not in ("", "STATEWIDE") else None)
            lead = sorted(ballot(c["candidates"]) or c["candidates"], key=lambda x: -x["votes"])
            rec = {"id": cid(f"{year}-{level}-{c['state']}-"
                             + (L._slug(dist) if dist else "district-not-given-" + L._slug(lead[0]["name"] if lead else ""))
                             + (f"-position-{c['post']}" if c.get("post") else "")
                             + ("" if c["stage"] == "GEN" and not c["special"] else f"-{L._slug(c['stage'])}"
                                + ("-special" if c["special"] else ""))),
                   "year": year, "date": c["date"] or None, "level": level,
                   "place": {"state": c["state"], "district": dist, "position": c.get("post")},
                   "election": ("general" if c["stage"] == "GEN" else c["stage"].lower())
                               + (", special" if c["special"] else ""),
                   "seats": c["magnitude"] if (c.get("magnitude") or 1) > 1 else None,
                   "result": {"candidates": _cands_out(c["candidates"], c.get("magnitude") or 1),
                              "total_votes": sum(x["votes"] for x in c["candidates"]), "source": "medsl"},
                   "forecasts": []}
            if c.get("office_as_filed"):
                rec["office_as_filed"] = c["office_as_filed"].title()
            if not dist:
                rec.setdefault("notes", []).append("the source gives no district number for this contest; it is "
                                                   "pieced together from its precincts' candidates")
            p = {}
            b = ballot(c["candidates"])
            k = c.get("magnitude") or 1
            r_ = rows24.get(id(c))
            top = sorted(c["candidates"], key=lambda x: -x["votes"])
            route, key = leg_structure(c)
            label = f"{level} {year}"
            swi = strong_write_in(c["candidates"], k) if route == "zero" else None
            if c["state"] in bad[year]:
                p["not_computed"] = bad[year][c["state"]]
                counts[f"{label}: not computed, the state's counts do not add up"] += 1
            elif c["state"] in RANKED and route != "zero":
                p["not_computed"] = RANKED[c["state"]]
                counts[f"{label}: not computed, ranked choice"] += 1
            elif c["stage"] != "GEN" or c["special"]:
                p["not_computed"] = ("a recount's count, recorded beside the general's" if "RECOUNT" in c["stage"]
                                     else "a special election: the model's own forecasts are fitted to regular "
                                          "elections")
                counts[f"{label}: not computed, special or recount"] += 1
            elif c["district"] == "" or (dist and pieces[leg_key(c) + (c["stage"], c["special"])] > 1):
                p["not_computed"] = ("the source splits this district's returns into more than one contest (its "
                                     "counties do not list the same candidates), so this count may not be the "
                                     "district's whole count")
                counts[f"{label}: not computed, the district is split in the source"] += 1
            elif c.get("magnitude") is None:
                p["not_computed"] = "the number of seats is not verified in the source (MEDSL's magnitude is empty)"
                counts[f"{label}: not computed, seats not given"] += 1
            elif route == "zero" and swi:
                share, generic = swi
                p["not_computed"] = ("one name on the ballot for each seat, but write-ins received "
                                     + (f"{100 * share:.0f}% of the last winner's votes" if share else "votes")
                                     + (" (counted together, so whether one write-in candidate did is not reported)"
                                        if generic else "")
                                     + f": {L.METHOD} has no forecast route for write-in contests")
                counts[f"{label}: not computed, unopposed with strong write-ins"] += 1
            elif route == "zero":
                p = {"value": 0.0, "event": 0.0, "reason": key}
                counts[f"{label}: p = 0"] += 1
            elif route in ("class", "boundary"):
                p = class_p(rec, c, route, key, ktrain, kdens, key, commit, with_p, counts, label,
                            k if route == "boundary" else 1)
                if rec["forecasts"]:
                    rec["forecasts"][-1]["note"] = ((rec["forecasts"][-1].get("note", "") + "; ") if route ==
                                                    "boundary" else "") + "like races from Klarner's 1967-2022 returns"
            elif r_ is None:
                p["not_computed"] = "no votes for the Democrat or the Republican"
                counts[f"{label}: not computed, no votes"] += 1
            else:
                mean, sd, a = L.predict_partisan(M, r_, pres)
                n = r_["N"] - 1
                rec["two_party"] = {"votes": [r_["d"]["votes"], r_["r"]["votes"]], "n_other_voters": n,
                                    "share_first": round(r_["y"], 6)}
                inputs = {"class": r_["cls"], "incumbency": r_["inc"], "lean": round(r_["L"], 4),
                          "lean_year": r_["L_year"], "swing": round(a, 4),
                          "lines_unchanged_share": None if r_["lines"] is None else round(r_["lines"], 3)}
                if r_["cls"] == "A":
                    inputs.update({"last_D": round(r_["last"], 4), "last_year": 2022})
                elif r_["cls"] == "B":
                    inputs.update({"last_unopposed": r_["last"], "last_year": 2022})
                rec["forecast_inputs"] = inputs
                rec["forecasts"].append({"by": "the model's own", "method": L.METHOD, "route": "partisan",
                                         "share": {"of": "Democrat, two-party", "mean": round(mean, 4),
                                                   "sd": round(sd, 4), "tails": "normal"},
                                         "note": "fitted on Klarner's races of 1967-2022; incumbency matched by name",
                                         "source": "model"})
                if any(x.get("writein") or _is_generic(x["name"]) for x in top[:2]) or \
                        {major(top[0]), major(top[1])} != {"D", "R"}:
                    p["not_computed"] = ("the two leading lines were not the Democrat and the Republican, so the "
                                         "forecast of the Democrat against the Republican is not of the pair that "
                                         "decided this contest (model section 7)")
                    counts[f"{level} {year}: not computed, D and R not the top two"] += 1
                elif M is None or kfit < L.MIN_EARLIER:
                    p["not_computed"] = "too few earlier years to fit on"
                elif with_p:
                    t4 = core.p_contest(n, mean, sd, "t4")
                    p = L._p_block(n, mean, sd, f"the model's own ({L.METHOD}), normal", commit,
                                   {"t4": {"value": t4["p"], "event": t4["event"], "method": t4["method"]}})
                    counts[f"{level} {year}: p computed, partisan"] += 1
            rec["p"] = p
            files[(level, year, c["state"])].append(L._compact(rec))

    # -- local races: routes (b) and (c), from like races of earlier years
    lrows = {y: local_rows([c for c in m[y] if c["state"] not in bad[y]]) for y in YEARS}
    dens = {}
    for year in YEARS:
        train = [r_ for y in YEARS if y < year for r_ in lrows[y]]
        for c in m[year]:
            if not is_local_level(c):
                continue
            route, key = local_structure(c)
            scope = "state" if c["dataverse"] == "STATE" else "local"
            where = "-".join(x for x in (c["district"] if c["district"] not in ("", "STATEWIDE") else "",
                                         ("county-" + c["counties"][0]) if c["counties"] and scope == "local" else "")
                             if x)
            rec = {"id": cid(f"{year}-local-{c['state']}-{L._slug(c['office'])[:60]}-{L._slug(where)}".rstrip("-")),
                   "year": year, "date": c["date"] or None, "level": "local",
                   "place": {"state": c["state"], "district": None if c["district"] in ("", "STATEWIDE") else c["district"],
                             "counties": None if scope == "state" and c["district"] == "STATEWIDE" else c["counties"]},
                   "office": c["office"].title(), "office_type": office_type(c["office"]), "office_scope": scope,
                   "election": ("general" if c["stage"] == "GEN" else c["stage"].lower())
                               + (", special" if c["special"] else ""),
                   "seats": c["magnitude"] if (c.get("magnitude") or 1) > 1 else None,
                   "result": {"candidates": _cands_out(c["candidates"], c.get("magnitude") or 1),
                              "total_votes": sum(x["votes"] for x in c["candidates"]), "source": "medsl"},
                   "forecasts": []}
            p = {}
            if c["state"] in bad[year] and route != "zero":
                p["not_computed"] = bad[year][c["state"]]
                counts[f"local {year}: not computed, the state's counts do not add up"] += 1
            elif scope == "state" and c["state"] in RANKED and route != "zero":
                p["not_computed"] = RANKED[c["state"]]
                counts[f"local {year}: not computed, ranked choice"] += 1
            elif route == "zero" and (swi := strong_write_in(c["candidates"], c.get("magnitude") or 1)):
                share, generic = swi
                p["not_computed"] = ("one name on the ballot for each seat, but write-ins received "
                                     + (f"{100 * share:.0f}% of the last winner's votes" if share else "votes")
                                     + (" (counted together, so whether one write-in candidate did is not reported)"
                                        if generic else "")
                                     + f": {L.METHOD} has no forecast route for write-in contests")
                counts[f"local {year}: not computed, unopposed with strong write-ins"] += 1
            elif route == "zero":
                p = {"value": 0.0, "event": 0.0, "reason": key}
                counts[f"local {year}: p = 0"] += 1
            elif route == "not computed":
                p["not_computed"] = key
                counts[f"local {year}: not computed, {key.split(':')[0][:50]}"] += 1
            else:
                p = class_p(rec, c, route, key, train, dens, (year, key), commit, with_p, counts, f"local {year}",
                            c["magnitude"] if route == "boundary" else 1)
            rec["p"] = p
            files[("local", year, c["state"])].append(L._compact(rec))

    # -- measures and retentions: recorded, p not yet computed
    for year in YEARS:
        for c in m[year]:
            if not c["question"]:
                continue
            kind = "retention" if "RETENTION" in c["office"].upper() or "RETAIN" in " ".join(
                x["name"] for x in c["candidates"]) else "measure"
            scope = "statewide" if c["dataverse"] == "STATE" else "local"
            yes = sum(x["votes"] for x in c["candidates"] if x["name"] in YES_WORDS)
            no = sum(x["votes"] for x in c["candidates"] if x["name"] in NO_WORDS)
            rec = {"id": cid(f"{year}-measure-{c['state']}-{L._slug(c['office'])[:60]}"
                             + (f"-{L._slug(c['subject'])}" if c.get("subject") else "")
                             + ("" if scope == "statewide" else f"-{c['counties'][0]}")),
                   "year": year, "date": c["date"] or None, "level": "measure",
                   "place": {"state": c["state"], "district": None if c["district"] in ("", "STATEWIDE") else c["district"],
                             "counties": None if scope == "statewide" else c["counties"]},
                   "question": {"title": c["office"].title(), "subject": (c.get("subject") or "").title() or None,
                                "kind": kind, "scope": scope},
                   "result": {"candidates": [{"name": x["name"], "votes": x["votes"],
                                              "votes_incomplete": True if x.get("votes_missing_in_some_precincts")
                                              else None} for x in c["candidates"]],
                              "total_votes": sum(x["votes"] for x in c["candidates"]), "source": "medsl",
                              "yes_share": round(yes / (yes + no), 6) if yes + no else None},
                   "forecasts": [],
                   "p": {"not_computed": "the threshold the measure's law sets, and a forecast route for measures, "
                                         "are not yet settled (brief step 4; proposed to the orchestrator)"}}
            if scope == "local":
                rec.setdefault("notes", []).append(
                    "counted by county: MEDSL's wording of a local question does not show which place holds it, so a "
                    "question held across several counties appears once per county")
            counts[f"measure {year}: {scope} {kind}"] += 1
            files[("measure", year, c["state"])].append(L._compact(rec))

    total = 0
    by_level = collections.Counter()
    for (level, year, st), cs in sorted(files.items()):
        head = {"level": level, "year": year, "state": st,
                "about": f"{level} contests of {year} in {L.STATE_NAMES.get(st, st)}, in the layout of plan/PLAN.md "
                         f"section 3 with the fields data/README.md adds (D3). Built by pipeline/local_medsl.py from "
                         f"pipeline/intake/medsl_precinct.py's cache.",
                "p_computed_by": "pipeline/local_medsl.py", "p_commit": commit,
                "sources": {"medsl": _src_medsl(year, chk[year], [n for n, f in chk[year].get("files", {}).items()
                                                                  if st in f.get("states", {})]),
                            "model": src_model, "nara": src_nara, "klarner": src_klarner}}
        path = os.path.join(out_dir, level, str(year), f"{st}.json")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            body = json.dumps(head, ensure_ascii=False, separators=(",", ":"))
            f.write(body[:-1] + ',"contests":[\n')
            f.write(",\n".join(json.dumps(x, ensure_ascii=False, separators=(",", ":")) for x in cs))
            f.write("\n]}\n")
        sz = os.path.getsize(path)
        total += sz
        by_level[level] += sz
    print(f"wrote {sum(len(v) for v in files.values()):,} contests in {len(files):,} files, {total / 1e6:.1f} MB: "
          + ", ".join(f"{k} {v / 1e6:.1f} MB" for k, v in sorted(by_level.items())))
    counts.update({f"left out, no vote anywhere, {y}": EMPTY[y] for y in YEARS})
    print(json.dumps(dict(sorted(counts.items())), indent=1))
    return files, counts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("what", choices=["check2022", "build"])
    ap.add_argument("--out", default=os.path.join(L.REPO, "data"))
    a = ap.parse_args()
    if a.what == "check2022":
        out = check_2022()
        path = os.path.join(L.REPO, "data", "local", "check-2022-medsl-klarner.json")
        with open(path, "w") as f:
            json.dump(out, f, indent=1)
        print(json.dumps(out["tallies"], indent=1))
    else:
        build(a.out)


if __name__ == "__main__":
    main()
