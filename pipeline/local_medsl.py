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

Run:  VOTE_CACHE=/tmp/vote-cache python3 pipeline/local_medsl.py check2018
      VOTE_CACHE=/tmp/vote-cache python3 pipeline/local_medsl.py check2022
      VOTE_CACHE=/tmp/vote-cache python3 pipeline/local_medsl.py backtest-local-partisan
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
YEARS = (2018, 2020, 2022, 2024)
MEASURE_YEARS = (2016,) + YEARS   # 2016: MEDSL's older sets, read for their questions only
KLARNER_CHECKED = (2018, 2022)   # years whose MEDSL legislative returns are checked against Klarner's, the record
GITHUB_YEARS = {2018: "MEDSL/2018-elections-official", 2020: "MEDSL/2020-elections-official"}


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
QFIX = collections.defaultdict(collections.Counter)   # year -> what fix_questions did, for the report


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
    return certified_la(certified_in(certified_nc(fix_questions(out, year), year), year), year)


def certified_nc(contests, year):
    """North Carolina's local races and questions of MEDSL's general date, from the State Board's own file
    (pipeline/local_ncsbe.py) in place of MEDSL's: where two sources hold one contest the certified one wins (brief D3,
    step 2). MEDSL's North Carolina file joins contests the State Board keeps apart (Cherokee County's three
    commissioner districts in 2018, the Court of Appeals' three seats in 2024) and files the 2024 amendment as 100
    county questions (data/local/check-ncsbe.json). The governor and Congress stay MEDSL's; the legislature stays
    MEDSL's contests, with the State Board's counts where they differ (certified_legislature)."""
    import local_ncsbe as NS
    if not glob.glob(os.path.join(NS.NORM, f"{year}_11_*.jsonl")):
        raise SystemExit(f"the State Board's {year} file is not in the cache: run pipeline/intake/ncsbe.py list, "
                         f"fetch and read first")
    nc = NS.medsl_shape(year)
    if nc is None:
        print(f"{year}: the State Board's North Carolina file fails its gate; MEDSL's North Carolina contests kept")
        return contests
    if year == 2016:   # MEDSL's 2016 is read for its questions only
        nc = [c for c in nc if c["question"]]
    keep = [c for c in contests if not (c["state"] == "NC" and (c["question"] or is_local_level(c)))]
    if year not in KLARNER_CHECKED and year >= 2024:   # the years whose legislature MEDSL's build writes
        certified_legislature(keep, year)
    return keep + nc


CERTIFIED_NOTE = ("votes: the North Carolina State Board of Elections' certified counts ({file}), in place of "
                  "MEDSL's, which differ ({diff}); the certified one wins (brief D3, step 2)")
CERTIFIED_LEG = collections.Counter()


def certified_legislature(contests, year):
    """North Carolina's legislative generals of the year: the State Board's counts in place of MEDSL's where they
    differ (48 of 170 in 2024, by a few votes; data/local/check-ncsbe.json, legislature_medsl_2024). Candidates are
    matched by party for the Democrat and the Republican, by name otherwise, and, where each side has one candidate
    of neither major party, those two; a contest whose named candidates do not all match keeps MEDSL's. Each changed
    contest carries `votes_source` and a note with both counts. Called only when the State Board's file passes its
    gate (certified_nc)."""
    import local_ncsbe as NS
    d = next((x for x in NS.load_dates() if x.startswith(str(year)) and NS.is_general_date(x)), None)
    dates = {d: NS.load_dates()[d]}
    NS.split_party(dates)
    NS.classify(dates)
    meta = NS.checks_of(d)["source"]
    ns = collections.defaultdict(list)
    for c in dates[d]:
        if c.get("_level") == "legislature":
            ns[c["_leg"]].append(c)
    CERTIFIED_LEG.clear()
    for c in contests:
        if c["state"] != "NC" or c["office"] not in LEG or c["question"] or c["stage"] != "GEN" or c["special"]:
            continue
        hit = ns.get(("state-upper" if LEG[c["office"]] else "state-lower", int(district_no(c["district"]) or 0)))
        if not hit or len(hit) != 1 or (c.get("magnitude") or 1) != 1:
            CERTIFIED_LEG["kept MEDSL's: no single State Board contest"] += 1
            continue
        named = [x for x in hit[0]["choices"] if not _is_generic(x["name"])]
        mine = [a for a in c["candidates"] if not a.get("writein") and not _is_generic(a["name"])]
        minor_m = [a for a in mine if NS._major(a.get("party")) is None]
        minor_n = [x for x in named if NS._major(x["party"]) is None]
        new = {}
        for a in mine:
            pa = NS._major(a.get("party"))
            if pa:
                m = [x for x in named if NS._major(x["party"]) == pa]
            else:
                m = [x for x in named if NS._major(x["party"]) is None and name_key(x["name"]) == name_key(a["name"])]
                if not m and len(minor_m) == 1 and len(minor_n) == 1:
                    m = minor_n
            if len(m) != 1:
                new = None
                break
            new[id(a)] = m[0]
        if new is None or len(new) != len(named):
            CERTIFIED_LEG["kept MEDSL's: the candidates do not all match"] += 1
            continue
        diff = [(a["name"], new[id(a)]["name"], a["votes"], new[id(a)]["votes"]) for a in mine
                if a["votes"] != new[id(a)]["votes"]]
        if not diff:
            CERTIFIED_LEG["equal"] += 1
            continue
        for a in mine:
            a["votes"] = new[id(a)]["votes"]
        f = meta["url"].rsplit("/", 1)[1]
        c["votes_source"] = {"source": "ncsbe", "file": f, "medsl": {n: v for n, _, v, _ in diff}}
        c["certified_note"] = CERTIFIED_NOTE.format(file=f, diff="; ".join(
            f"{b}: {v:,} in MEDSL's, {w:,} certified" for _, b, v, w in diff))
        CERTIFIED_LEG["replaced by the certified counts"] += 1
    print(f"{year}: North Carolina's legislature against the State Board's: {dict(CERTIFIED_LEG)}")


CERTIFIED_STATES = collections.defaultdict(set)   # year -> states whose own certified file replaced MEDSL's


def certified_in(contests, year):
    """Indiana's legislature, local races and questions of 2024, from the state's own certified file
    (pipeline/local_in.py) in place of MEDSL's, whose Indiana counts fall short of the certified presidential count
    (quality()): the certified one wins (brief D3, step 2; the orchestrator, 08:08 and 08:32). The presidency, Congress
    and the governor stay MEDSL's lines here (D1's and D2's are the record for them). Indiana is then no longer held
    back in `year` (build: bad[year])."""
    if year != 2024:
        return contests
    import local_in as LI
    st = LI.medsl_shape(year)
    if st is None:
        print(f"{year}: Indiana's own file is missing or fails its gate; MEDSL's Indiana contests kept")
        return contests
    keep = [c for c in contests if not (c["state"] == "IN" and (c["question"] or c["office"] in LEG
                                                                 or is_local_level(c)))]
    CERTIFIED_STATES[year].add("IN")
    return keep + st


def certified_la(contests, year):
    """Louisiana's local races and questions of 2024, from the Secretary of State's official results
    (pipeline/local_la.py) in place of MEDSL's, which count Election Day only (quality()): the certified one wins (brief
    D3, step 2; the orchestrator, 08:08 and 10:17). The presidency and Congress stay MEDSL's lines here (D1's and D2's
    are the record for them). Louisiana is then no longer held back in `year` (build: bad[year])."""
    if year != 2024:
        return contests
    import local_la as LA
    st = LA.medsl_shape(year)
    if st is None:
        print(f"{year}: Louisiana's own file is missing or fails its gate; MEDSL's Louisiana contests kept")
        return contests
    keep = [c for c in contests if not (c["state"] == "LA" and (c["question"] or c["office"] in LEG
                                                                 or is_local_level(c)))]
    CERTIFIED_STATES[year].add("LA")
    return keep + st


_POS = re.compile(r"^(YES|FOR|IN FAVOR)\b")
_NEG = re.compile(r"^(NO|AGAINST|OPPOSED)\b(?! (NAME|CANDIDATE))")


def side(name):
    """'yes', 'no' or None for an answer line: the answer words, or a line that begins with one ('FOR BONDS',
    'AGAINST PROPOSED TAXATION', 'YES-LOCAL AMENDMENT NO 1', 'NO TO REJECT')."""
    n = (name or "").upper().strip()
    if n in YES_WORDS:
        return "yes"
    if n in NO_WORDS:
        return "no"
    if _POS.match(n):
        return "yes"
    if _NEG.match(n):
        return "no"
    return None


def yes_no(c):
    return (sum(x["votes"] for x in c["candidates"] if side(x["name"]) == "yes"),
            sum(x["votes"] for x in c["candidates"] if side(x["name"]) == "no"))


_QSTOP = {"FOR", "AGAINST", "THE", "PROPOSAL", "BONDS", "BOND", "APPROVAL", "YES", "NO", "QUESTION", "OF", "A", "AN",
          "AND", "TO", "ON", "IN", "MEASURE"}


def _qtokens(c):
    return set(re.findall(r"[A-Z0-9]+", (c["office"] + " " + (c.get("subject") or "")).upper())) - _QSTOP


def fix_questions(contests, year):
    """Three faults of MEDSL's question lines, found in the output [measured]:
    1. a question filed as a candidate contest, its answers worded as candidates ('FOR BONDS' and 'AGAINST BONDS',
       Alabama's 'YES-LOCAL AMENDMENT NO 1'): two lines on the ballot, one a yes and one a no; read as a question;
    2. 'REJECTED' alone under a candidate office (Michigan's 2022 rejected ballots in Ottawa County): not a
       question; left out;
    3. a question split in two, its yes line and its no line under offices or subjects worded apart (Oklahoma's
       2024 '... FOR THE PROPOSAL' and '... AGAINST THE PROPOSAL', a judge's name spelled two ways): a yes-only and
       a no-only piece over the same counties whose words, answer words aside, overlap by half or more are joined.
    A one-sided piece left over is kept, and its p is not computed (the source gives one answer only)."""
    fx = QFIX[year]
    cand_offices = {(c["state"], c["office"]) for c in contests if not c["question"]}
    out, pieces = [], collections.defaultdict(lambda: {"yes": [], "no": []})
    for c in contests:
        if not c["question"]:
            b = [x for x in c["candidates"] if not x.get("writein") and not _is_generic(x["name"])]
            sides = sorted(side(x["name"]) or "" for x in b)
            if len(b) == 2 and sides == ["no", "yes"]:
                c["question"] = True
                c["read_as_question"] = "its two lines are a yes and a no"
                fx["candidate contest read as a question"] += 1
            else:
                out.append(c)
                continue
        names = {x["name"] for x in c["candidates"]}
        if names == {"REJECTED"} and (c["state"], c["office"]) in cand_offices:
            fx["rejected-ballot line under a candidate office, left out"] += 1
            continue
        y, n = yes_no(c)
        has_y = any(side(x["name"]) == "yes" for x in c["candidates"])
        has_n = any(side(x["name"]) == "no" for x in c["candidates"])
        if has_y != has_n:
            pieces[(c["state"], c["date"], c["stage"], c["special"], tuple(sorted(c["counties"])))][
                "yes" if has_y else "no"].append(c)
            continue
        out.append(c)
    for key, g in pieces.items():
        left_no = list(g["no"])
        for cy in g["yes"]:
            ty = _qtokens(cy)
            best, bj = None, 0.0
            for cn in left_no:
                tn = _qtokens(cn)
                j = len(ty & tn) / len(ty | tn) if ty | tn else 0.0
                if j > bj:
                    best, bj = cn, j
            if best is not None and bj >= 0.5:
                left_no.remove(best)
                cy["candidates"] = cy["candidates"] + best["candidates"]
                cy["joined_from"] = [cy["office"] + (" / " + cy["subject"] if cy.get("subject") else ""),
                                     best["office"] + (" / " + best["subject"] if best.get("subject") else "")]
                fx["one-sided pieces joined into one question"] += 1
            else:
                cy["one_answer_only"] = True
                fx["one-sided piece left (yes only)"] += 1
            out.append(cy)
        for cn in left_no:
            cn["one_answer_only"] = True
            fx["one-sided piece left (no only)"] += 1
            out.append(cn)
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
    elif year in KLARNER_CHECKED:
        path = os.path.join(L.REPO, "data", "local", f"check-{year}-medsl-klarner.json")
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

def check_2022(klarner=None, medsl=None, year=2022):
    """Single-member districts both sources name the same way (a number, no county name or post): are the
    Democrat's and the Republican's votes, and the winner, the same? Returns the tallies and every difference.
    The same check runs for 2018 (year=2018), MEDSL's GitHub-held returns of that year beside Klarner's."""
    klarner = klarner or L.load_klarner()
    medsl = medsl or load(year)
    kl = {}
    for c in klarner:
        if c["year"] == year and c["etype"] == "g" and c["eseats"] == 1 and not c["dname"] and not c["geopost"] \
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
    return L._p_like(n, f, f"the model's own ({L.METHOD}), like past races", commit)


# ------------------------------------------------------------------ local Democrat-against-Republican races

def county_lean(chk_prev, bad_prev, c):
    """The place's lean for a local race (the orchestrator, 06:16): the Democrats' two-party share of the US House
    vote of the previous general election in the race's counties, minus one half, from MEDSL's own returns of that
    year. None, with the reason, where a county's House race was not contested by both parties in every precinct,
    or the previous year's file for the state is not sound."""
    st = c["state"]
    if st in bad_prev:
        return None, "the previous general's returns for this state are held back (see the state's check)"
    rows = (chk_prev.get("house_by_county") or {}).get(st) or {}
    if not c["counties"]:
        return None, "the source places this contest in no county"
    dv = rv = 0
    for county in c["counties"]:
        r = rows.get(county)
        if not r:
            return None, f"no US House vote for county {county} in the previous general's returns"
        if not r[2]:
            return None, f"county {county}'s US House race was not contested by both parties throughout"
        dv += r[0]
        rv += r[1]
    if dv + rv <= 0:
        return None, "no Democratic or Republican US House vote in the race's counties"
    return dv / (dv + rv) - 0.5, None


def local_partisan_rows(contests, chk_prev, bad_prev, year):
    """Single-seat general races below the legislature with one Democrat and one Republican on the ballot, as rows
    for route (a)'s class C: no last result, incumbency not matched (0), the county's lean."""
    rows = []
    for c in contests:
        if not is_local_level(c) or c["special"] or c["stage"] != "GEN" or c.get("magnitude") != 1:
            continue
        b, d, r = _two_party(c)
        if len(d) != 1 or len(r) != 1 or d[0]["votes"] <= 0 or r[0]["votes"] <= 0:
            continue
        lean, why = county_lean(chk_prev, bad_prev, c)
        rows.append({"m": c, "year": year, "state": c["state"], "cls": "C", "inc": 0, "xl": 0.0, "ulag": 0,
                     "L": lean if lean is not None else 0.0, "Lmiss": 0, "lean_missing": why,
                     "N": d[0]["votes"] + r[0]["votes"], "y": d[0]["votes"] / (d[0]["votes"] + r[0]["votes"]),
                     "d": d[0], "r": r[0]})
    return rows


LOCAL_PARTISAN_OK = (0.40, 0.60)   # the orchestrator, 06:16: compute only if the back-test's 50% interval holds 40-60%


def lean_rows(year, contests=None):
    """The local Democrat-against-Republican rows of a year with their lean from the previous general's US House
    vote by county, or None where the sources taken in hold no such vote for that year."""
    prev = year - 2
    if prev not in YEARS or not (checks(prev).get("house_by_county") or {}):
        return None
    return local_partisan_rows(contests if contests is not None else load(year), checks(prev), quality(prev), year)


def _lean_reason(why):
    """The kind of reason a lean is missing, without the county's code: for the tallies."""
    return re.sub(r"county \d+('s)?", lambda mt: "a county" + (mt.group(1) or ""), why or "")


def backtest_local_partisan(write=True, years=None, prow=None, pres=None):
    """Route (a)'s class-C terms, fitted on Klarner's races before the year, applied to the year's local races
    between one Democrat and one Republican with the county's previous-general US House lean: the forecasts against
    what happened. {year: tallies}; written to data/local/backtest-local-partisan.json."""
    if prow is None:
        pres, _ = L.president_party()
        prow = [r_ for r_ in L.partisan_rows(L.load_klarner()) if r_["year"] in pres]
    res = {}
    for year in years or YEARS:
        rows = lean_rows(year)
        if rows is None:
            continue
        M, k = L.fit_before(prow, pres, year)
        res[year] = _backtest_one(M, k, rows, quality(year), pres)
    if write:
        with open(os.path.join(L.REPO, "data", "local", "backtest-local-partisan.json"), "w") as f:
            json.dump({"about": "route (a)'s class-C terms (fitted on Klarner's state legislative races of earlier "
                                "years only) applied to local races between one Democrat and one Republican, the "
                                "place's lean read from the US House vote of the previous general in the race's "
                                "counties (MEDSL's precinct returns): the forecast against what happened. Built by "
                                "pipeline/local_medsl.py backtest-local-partisan.",
                       "rule": f"p is computed for a year only if its 50% interval holds between "
                               f"{LOCAL_PARTISAN_OK[0]:.0%} and {LOCAL_PARTISAN_OK[1]:.0%} of outcomes",
                       "years": {str(y): v for y, v in res.items()}}, f, indent=1)
    return res


def _backtest_one(M, k, rows, bad, pres):
    from statistics import NormalDist
    used = [r_ for r_ in rows if r_["lean_missing"] is None and r_["m"]["state"] not in bad]
    z = {"50": 0.6744897501960817, "80": 1.2815515655446004, "95": 1.959963984540054}
    out = {"races": len(rows), "with_lean": len(used),
           "held_back_state": sum(1 for r_ in rows if r_["lean_missing"] is None and r_["m"]["state"] in bad),
           "lean_missing": dict(collections.Counter(_lean_reason(r_["lean_missing"]) for r_ in rows
                                                    if r_["lean_missing"]).most_common())}
    if M is None:
        out["fit"] = None
        return out
    cov = collections.Counter()
    exp49 = seen49 = e100 = s100 = bias = 0.0
    by_type = collections.defaultdict(lambda: [0, 0])
    for r_ in used:
        m, sd, a = L.predict_partisan(M, r_, pres)
        y = r_["y"]
        for kz, v in z.items():
            cov[kz] += abs(y - m) <= v * sd
        nd = NormalDist(m, sd)
        exp49 += nd.cdf(0.51) - nd.cdf(0.49)
        seen49 += 0.49 <= y <= 0.51
        h = 50 / r_["N"]
        e100 += nd.cdf(0.5 + h) - nd.cdf(0.5 - h)
        s100 += abs(r_["d"]["votes"] - r_["r"]["votes"]) <= 100
        bias += m - y
        t = office_type(r_["m"]["office"])
        by_type[t][0] += 1
        by_type[t][1] += abs(y - m) <= z["50"] * sd
    n = max(len(used), 1)
    out.update({"in_intervals_50_80_95": {kz: round(v / n, 3) for kz, v in cov.items()},
                "within_49_51": {"expected": round(exp49, 1), "seen": int(seen49)},
                "within_100_votes": {"expected": round(e100, 1), "seen": int(s100)},
                "mean_forecast_minus_outcome": round(bias / n, 4),
                "in_50_interval_by_office_type": {t: [v[0], round(v[1] / v[0], 3)] for t, v in sorted(by_type.items())},
                "fit": {"earlier_years_of_kind": k, "years_fitted": [M["years_fitted"][0], M["years_fitted"][-1]],
                        "method": L.METHOD}})
    out["computed"] = bool(used) and LOCAL_PARTISAN_OK[0] <= out["in_intervals_50_80_95"].get("50", 0) <= \
        LOCAL_PARTISAN_OK[1]
    return out


def check_oaarcy():
    """MEDSL's 2022 state offices set (OAARCY, read by `medsl_precinct.py 2022 --oaarcy`) beside UYQIEP's files for the
    same states: the contests each holds and how each compares with Klarner's 2022 legislatures."""
    oa = []
    for path in sorted(glob.glob(os.path.join(NORM, "oaarcy-2022", "*.jsonl"))):
        with open(path) as f:
            oa += [relabel(json.loads(line)) for line in f]
    oa = fix_questions([c for c in oa if any(x["votes"] for x in c["candidates"])], 2022)
    states = sorted({c["state"] for c in oa})
    base = load(2022)
    a = check_2022(medsl=base)
    b = check_2022(medsl=[c for c in base if c["state"] not in states] + oa)

    def keyset(cs):
        return sorted((c["office"], c["district"], c.get("subject") or "", tuple(sorted(
            (x["name"], x["votes"]) for x in c["candidates"]))) for c in cs)
    return {"about": "OAARCY (doi:10.7910/DVN/OAARCY, State Offices Precinct-Level Returns 2022) beside UYQIEP's 2022 "
                     "files for the states OAARCY holds among AR, AZ, ID, IN, MD, MI, ND and WA. Built by "
                     "pipeline/local_medsl.py check-oaarcy.",
            "states_in_oaarcy": states,
            "by_state": {st: {"contests_uyqiep": sum(1 for c in base if c["state"] == st),
                              "contests_oaarcy": sum(1 for c in oa if c["state"] == st),
                              "same_contests_and_votes": keyset([c for c in base if c["state"] == st]) ==
                              keyset([c for c in oa if c["state"] == st]),
                              "against_klarner_uyqiep": a["by_state"].get(st),
                              "against_klarner_oaarcy": b["by_state"].get(st)} for st in states}}


def _near_table(rows_, groups):
    out = {}
    for r_ in rows_:
        for grp in groups(r_):
            y = out.setdefault(grp, {"measures": 0, "near": {}})
            y["measures"] += 1
            for hh, (q, seen) in r_["near"].items():
                z = y["near"].setdefault(hh, [0.0, 0])
                z[0] += q
                z[1] += seen
    for y in out.values():
        y["near"] = {f"within {float(hh):.0%}": {"expected": round(v[0], 1), "seen": v[1]}
                     for hh, v in sorted(y.pop("near").items(), key=lambda kv: float(kv[0]))}
    return dict(sorted(out.items()))


def backtest_measures(mtest, mhalf):
    """Like past measures out of sample: each year's classes come from earlier years only. Near 1/2, for every
    statewide question whose class has earlier years (its threshold read or not): the class's chance of finishing
    within 1, 2 and 5 points of 1/2 added up, beside how many did. At the threshold, the same for the measures given
    a forecast, and within the forecast's own window."""
    half = _near_table(mhalf, lambda r_: (f"{r_['year']} {r_['key']} (trained on {r_['train']})", f"all years {r_['key']}"))
    at_t = {}
    for r_ in mtest:
        for grp in (f"{r_['year']}", "all years"):
            y = at_t.setdefault(grp, {"measures": 0, "own_window": [0.0, 0], "near_threshold": {}})
            y["measures"] += 1
            y["own_window"][0] += r_["q_own"]
            y["own_window"][1] += r_["in_own"]
            for hh, (q, seen) in r_["near"].items():
                z = y["near_threshold"].setdefault(hh, [0.0, 0])
                z[0] += q
                z[1] += seen
    for y in at_t.values():
        y["own_window"] = {"expected": round(y["own_window"][0], 1), "seen": y["own_window"][1]}
        y["near_threshold"] = {f"within {float(hh):.0%}": {"expected": round(v[0], 1), "seen": v[1]}
                               for hh, v in sorted(y["near_threshold"].items(), key=lambda kv: float(kv[0]))}
    return {"about": "statewide measures and retentions, like past measures out of sample (each year's class from "
                     "earlier years only): expected and seen counts finishing near 1/2 (every statewide question) "
                     "and near the threshold (those given a forecast). Built by pipeline/local_medsl.py build.",
            "near_half": half, "at_threshold": dict(sorted(at_t.items()))}


def backtest_local_classes(files):
    """Routes (b) and (c) for local races, out of sample: each year's like-race classes come from earlier years
    only, so the year's own outcomes test them. For each contest given p, the class's chance of finishing within
    its window (q) is added up and set beside how many did."""
    out = {}
    for (level, year, st), cs in files.items():
        if level != "local":
            continue
        for c in cs:
            fc = [x for x in c.get("forecasts", []) if x.get("route") in ("class", "boundary")]
            if not fc or "value" not in c.get("p", {}):
                continue
            x = fc[-1]
            tp = c.get("two_party") or c.get("boundary")
            inw = x["window"][0] <= tp["share_first"] <= x["window"][1]
            y = out.setdefault(str(year), {"contests": 0, "expected_in_window": 0.0, "seen_in_window": 0,
                                          "by_office_type": {}})
            k = f"{x['route']}, {c.get('office_scope', 'local')} {c.get('office_type', '')}".strip()
            t = y["by_office_type"].setdefault(k, [0, 0.0, 0])
            y["contests"] += 1
            y["expected_in_window"] += x["q"]
            y["seen_in_window"] += inw
            t[0] += 1
            t[1] += x["q"]
            t[2] += inw
    for y in out.values():
        y["expected_in_window"] = round(y["expected_in_window"], 1)
        y["seen_over_expected"] = round(y["seen_in_window"] / y["expected_in_window"], 3) if y["expected_in_window"] else None
        y["by_office_type"] = {k: {"contests": v[0], "expected": round(v[1], 1), "seen": v[2]}
                               for k, v in sorted(y["by_office_type"].items(), key=lambda kv: -kv[1][0])}
    return {"about": "local races given p by like past races (routes (b) and (c), method " + L.METHOD + "): the "
                     "chance each class gives of finishing within its window around one half, added up over the "
                     "year's contests, beside how many did. Classes come from earlier years only. Built by "
                     "pipeline/local_medsl.py build.", "years": dict(sorted(out.items()))}


CAL_MIN_EXPECTED = 30   # the orchestrator, 06:38: an office type gets its own factor only with about 30 or more
                         # expected near-1/2 races in the fitting years; otherwise the fitting years' races pooled
CAL_NOTE = "calibrated to earlier years' near-ties"


def _near_half(rec):
    """(route group, office-type key, chance the forecast gave of finishing near 1/2, whether it did) for a local
    record with a forecast; None otherwise. Near 1/2 is the class's window for like races, 49-51% for the
    Democrat-against-Republican route."""
    fc = rec.get("forecasts") or []
    if not fc:
        return None
    x = fc[-1]
    if x.get("route") in ("class", "boundary"):
        tp = rec.get("two_party") or rec.get("boundary")
        return ("like races", f"{x['route']}, {rec.get('office_scope', 'local')} {rec.get('office_type', '')}",
                x["q"], x["window"][0] <= tp["share_first"] <= x["window"][1])
    if x.get("route") == "partisan" and rec.get("two_party"):
        m, sd = x["share"]["mean"], x["share"]["sd"]
        e = L._ncdf(0.51, m, sd) - L._ncdf(0.49, m, sd)
        return ("partisan", f"partisan, {rec.get('office_scope', 'local')} {rec.get('office_type', '')}", e,
                abs(rec["two_party"]["share_first"] - 0.5) <= 0.01)
    return None


def _deviance(pairs):
    """Poisson deviance of seen counts against expected ones, summed over office types: lower is closer."""
    d = 0.0
    for e, s_ in pairs:
        if e <= 0:
            continue
        d += 2 * ((s_ * math.log(s_ / e) if s_ > 0 else 0.0) - (s_ - e))
    return d


CAL_CELL_MIN = 5   # the robustness test's tested cells (brief D3, amended 08:36: "no tested cell made worse"): an
                   # office type whose count seen or expected (as the forecast stands) is 5 or more, D2's rule for its
                   # near-even cells (data/congress/REPORT.md section 0.1), so that both builds test alike
CAL_OUT_NOTE = ("the near-tie calibration of #31 (the orchestrator, 06:38), taken out by the robustness test (brief D3, "
                "amended 2026-11-07 08:36: adopted only if it improves the out-of-sample test, and still does, with no "
                "tested cell made worse, when any one scored year is left out); data/local/calibration-local.json")


def _cal_score(recs, group, years, factors):
    """The out-of-sample test of a route's factors over the scored `years`, each year with its own factor (fitted on
    the years before it): near 1/2, expected before and after against seen, overall and by office type, and the
    deviance by office type. It improves where the count comes nearer and the deviance falls; a tested cell (CAL_CELL_MIN)
    is made worse where its expected count moves further from its seen one."""
    by_b = collections.defaultdict(lambda: [0.0, 0.0, 0])
    n = 0
    for t in years:
        f_t = factors[t]
        for rec, key, e, seen in recs.get((group, t), []):
            k = f_t["own"].get(key, f_t["pooled"])
            by_b[key][0] += e
            by_b[key][1] += e * k
            by_b[key][2] += seen
            n += 1
    eb, ea, sn = (sum(v[i] for v in by_b.values()) for i in range(3))
    db, da = _deviance([(v[0], v[2]) for v in by_b.values()]), _deviance([(v[1], v[2]) for v in by_b.values()])
    worse = sorted(k for k, v in by_b.items() if max(v[0], v[2]) >= CAL_CELL_MIN and abs(v[1] - v[2]) > abs(v[0] - v[2]))
    improves = abs(ea - sn) < abs(eb - sn) and da < db
    return {"years": list(years), "contests": n, "seen_near_half": int(sn), "expected_before": round(eb, 1),
            "expected_after": round(ea, 1), "deviance_by_office_type_before": round(db, 2),
            "deviance_after": round(da, 2), "improves": improves, "tested_cells_made_worse": worse,
            "passes": improves and not worse,
            "by_office_type": {k: {"expected_before": round(v[0], 1), "expected_after": round(v[1], 1),
                                   "seen": int(v[2]), "tested": max(v[0], v[2]) >= CAL_CELL_MIN}
                               for k, v in sorted(by_b.items(), key=lambda kv: -kv[1][0])}}


def calibrate_local(files):
    """The orchestrator's ruling of 06:38 on local races given p by like races or by the transferred partisan
    route: a factor (seen over expected near 1/2) fitted on years before the one it is applied to, by office type
    where the fitting years expected about 30 or more such races, else pooled; adopted for a route only if it
    improves the out-of-sample test. Since the brief's amendment of 08:36 the test is the robustness test: every year
    with a factor is scored (each with its own factor); the factors must improve the test over all of them with no
    tested cell made worse, and again with any one scored year left out. A route with one scored year cannot show the
    second, so it fails: the default is no change [inferred: the amendment's words, "the model's default is no
    change"]. Where adopted, p is calibrated (and a year with no earlier year to fit on has none); where not, p stays
    uncalibrated and each p a factor would have moved carries calibration_not_of_record beside it. Changes the
    records in place; returns the report."""
    recs = collections.defaultdict(list)   # (group, year) -> [(rec, key, e, seen)]
    for (level, year, st), cs in files.items():
        if level != "local":
            continue
        for rec in cs:
            nh = _near_half(rec)
            if nh:
                recs[(nh[0], year)].append((rec, nh[1], nh[2], nh[3]))
    report = {}
    for group in ("like races", "partisan"):
        years = sorted(y for g, y in recs if g == group)
        factors = {}
        for t in years:
            fit_years = [y for y in years if y < t]
            if not fit_years:
                factors[t] = None
                continue
            by = collections.defaultdict(lambda: [0.0, 0])
            for y in fit_years:
                for _, key, e, seen in recs[(group, y)]:
                    by[key][0] += e
                    by[key][1] += seen
            pe, ps = sum(v[0] for v in by.values()), sum(v[1] for v in by.values())
            own = {k: v[1] / v[0] for k, v in by.items() if v[0] >= CAL_MIN_EXPECTED}
            factors[t] = {"fitted_on": fit_years, "pooled": ps / pe if pe else 1.0, "own": own,
                          "fit_counts": {k: [round(v[0], 1), v[1]] for k, v in by.items()}}
        rep_g = {"factors": {str(t): (None if f is None else {
            "fitted_on": f["fitted_on"], "pooled": round(f["pooled"], 3),
            "own": {k: round(v, 3) for k, v in sorted(f["own"].items())},
            "fit_counts_expected_seen": dict(sorted(f["fit_counts"].items()))}) for t, f in factors.items()}}
        scored = [t for t in years if factors.get(t) and recs.get((group, t))]
        if scored:
            rep_g["test"] = _cal_score(recs, group, scored, factors)
            rep_g["leave_one_year_out"] = {
                str(t): (_cal_score(recs, group, [y for y in scored if y != t], factors) if len(scored) > 1 else
                         {"passes": False, "why": "no scored year is left: this route's only scored year is " + str(t)})
                for t in scored}
            adopt = rep_g["test"]["passes"] and all(v["passes"] for v in rep_g["leave_one_year_out"].values())
        else:
            adopt = False
        rep_g["robustness_rule"] = ("adopted only if it improves the out-of-sample test (the count near 1/2 nearer, "
                                    "and the deviance by office type lower) over every scored year with no tested "
                                    f"cell made worse (a tested cell: {CAL_CELL_MIN} or more seen or expected), and "
                                    "again with any one scored year left out (brief D3, amended 2026-11-07 08:36)")
        rep_g["adopted"] = adopt
        report[group] = rep_g
        for t in years:
            f = factors[t]
            for rec, key, e, seen in recs[(group, t)]:
                p = rec.get("p") or {}
                if "value" not in p or not p.get("value"):
                    continue
                fc = rec["forecasts"][-1]
                if f is None:
                    if adopt:
                        fc["note"] = (fc.get("note", "") + "; " if fc.get("note") else "") + \
                            f"p {CAL_NOTE}: no earlier year in the sources taken in has these forecasts to fit on"
                        rec["p"] = {"not_computed": f"this route's p is {CAL_NOTE} (the orchestrator, 2026-11-07), "
                                                    f"and no earlier year in the sources taken in has its forecasts "
                                                    f"to fit the factor on"}
                    continue
                k = f["own"].get(key)
                factor, of = (k, key) if k is not None else (f["pooled"], "pooled over the fitting years' races")
                cal = {"factor": round(factor, 4), "of": of, "fitted_on": f["fitted_on"],
                       "what": "seen over expected near 1/2 in the fitting years' out-of-sample forecasts"}
                if group == "like races":
                    q = L._compact(L._p_like(p["n"], p["f_half"] * factor, f"{p['under']}, {CAL_NOTE}", None))
                else:
                    q = dict(p)
                    q["value"], q["event"], q["f_half"] = p["value"] * factor, p["event"] * factor, p["f_half"] * factor
                    q["under"] = f"{p['under']}, {CAL_NOTE}"
                    if p.get("alongside", {}).get("t4"):
                        t4 = dict(p["alongside"]["t4"])
                        t4["value"], t4["event"] = t4["value"] * factor, t4["event"] * factor
                        q["alongside"] = {"t4": t4}
                    q = L._compact(q)
                if adopt:
                    fc["calibration"] = cal
                    rec["p"] = q
                else:
                    rec["p"] = dict(p, calibration_not_of_record=dict(cal, value=q["value"], note=CAL_OUT_NOTE))
    return report


def local_partisan_p(rec, c, rows, ok, fit, bt, pres, year, commit, with_p, counts):
    """The transferred partisan route for a local race between one Democrat and one Republican (the orchestrator,
    06:16: route (a)'s class-C terms with the county's House lean, marked "transferred, not yet checked")."""
    label = f"local {year}"
    if rows is None:
        counts[f"{label}: not computed, D against R, no lean in the sources"] += 1
        return {"not_computed": f"a race between a Democrat and a Republican: the model's forecast for these reads "
                                f"the place's lean from the US House vote by county at the previous general "
                                f"({year - 2}), which the sources taken in do not hold"}
    r_ = rows.get(id(c))
    if r_ is None:
        counts[f"{label}: not computed, no votes"] += 1
        return {"not_computed": "no votes for the Democrat or the Republican"}
    if r_["lean_missing"]:
        counts[f"{label}: not computed, D against R, lean missing"] += 1
        return {"not_computed": "a race between a Democrat and a Republican, whose forecast reads the place's lean: "
                                + r_["lean_missing"]}
    M, k = fit
    if M is None or k < L.MIN_EARLIER:
        counts[f"{label}: not computed, too few earlier years"] += 1
        return {"not_computed": "too few earlier years to fit on"}
    mean, sd, a = L.predict_partisan(M, r_, pres)
    n = r_["N"] - 1
    rec["two_party"] = {"votes": [r_["d"]["votes"], r_["r"]["votes"]], "n_other_voters": n,
                        "share_first": round(r_["y"], 6)}
    rec["forecast_inputs"] = {"class": "C", "incumbency": 0, "lean": round(r_["L"], 4), "lean_year": year - 2,
                              "lean_of": "the Democrats' two-party share of the US House vote in the race's counties "
                                         "at the previous general, minus one half (MEDSL's precinct returns)",
                              "swing": round(a, 4)}
    rec["forecasts"].append({"by": "the model's own", "method": L.METHOD, "route": "partisan",
                             "share": {"of": "Democrat, two-party", "mean": round(mean, 4), "sd": round(sd, 4),
                                       "tails": "normal"},
                             "note": "transferred, not yet checked: route (a)'s class-C terms, fitted on Klarner's "
                                     "state legislative races of earlier years, applied with the county's US House "
                                     "lean; incumbency not matched (taken as 0); back-test in "
                                     "data/local/backtest-local-partisan.json",
                             "source": "model"})
    top = sorted(c["candidates"], key=lambda x: -x["votes"])
    if any(x.get("writein") or _is_generic(x["name"]) for x in top[:2]) or {major(top[0]), major(top[1])} != {"D", "R"}:
        counts[f"{label}: not computed, D and R not the top two"] += 1
        return {"not_computed": "the two leading lines were not the Democrat and the Republican, so the forecast of "
                                "the Democrat against the Republican is not of the pair that decided this contest "
                                "(model section 7)"}
    if not ok:
        cov = (bt or {}).get("in_intervals_50_80_95", {}).get("50")
        counts[f"{label}: not computed, D against R, back-test outside the line"] += 1
        return {"not_computed": f"the back-test of this transferred route on {year}'s races "
                                + (f"held {cov:.0%} of outcomes in its 50% interval, " if cov is not None else "")
                                + f"outside {LOCAL_PARTISAN_OK[0]:.0%}-{LOCAL_PARTISAN_OK[1]:.0%}"}
    if not with_p:
        return {}
    t4 = core.p_contest(n, mean, sd, "t4")
    counts[f"{label}: p computed, partisan (transferred)"] += 1
    p = L._p_block(n, mean, sd, f"the model's own ({L.METHOD}), normal; transferred, not yet checked", commit,
                   {"t4": {"value": t4["p"], "event": t4["event"], "method": t4["method"]}})
    # class C's terms, but with the race's own counties' lean, not a chamber's (L.FORECAST_SCOPE)
    p["forecast_scope"] = "the race's counties (class C's terms with the counties' US House lean)"
    return p


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
    if m.get("held_round"):   # a round the source's own state file marks as not the deciding one (local_la.py)
        return ("not computed", m["held_round"])
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
        return ("partisan", f"a {scope} race between a Democrat and a Republican")
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
        c = {"name": x["name"].title() if not (_is_generic(x["name"]) or x.get("as_named")) else x["name"],
             "party": _party_word(x),
             "votes": x["votes"], "won": x["won_marked"] if "won_marked" in x else True if id(x) in winners else None}
        if x.get("votes_missing_in_some_precincts"):
            c["votes_incomplete"] = True
        if x.get("lines"):   # a candidate on several parties' lines, or spelled differently by county: each line
            c["lines"] = [{k: v for k, v in (("name", ln["name"].title() if ln.get("name") else None),
                                             ("party", _party_word({"name": "", **ln})), ("votes", ln["votes"]))
                           if v is not None} for ln in x["lines"]]
        out.append(c)
    return out


def _src_medsl(year, chk, files):
    rec = chk.get("record", {})
    if year == 2016:
        sets = rec.get("sets", [])
        return F.source("MIT Election Data and Science Lab, " + " and ".join(
                            f"{x['title']} (Harvard Dataverse {x['doi']})" for x in sets),
                        sets[0]["url"] if sets else None, sets[0]["read_utc"] if sets else None, "CC0 1.0",
                        mark="stated", note="MEDSL's older layout, read for its questions only by "
                                            "pipeline/intake/medsl_precinct.py 2016; files " + ", ".join(sorted(files)))
    if year in GITHUB_YEARS:
        return F.source(f"MIT Election Data and Science Lab, {year} precinct-level returns, GitHub "
                        f"{GITHUB_YEARS[year]} at commit {rec.get('commit', '')[:12]}", rec.get("url"),
                        rec.get("read_utc"), "no licence file in the repository; MEDSL's Dataverse sets of the same "
                        "year are CC0 1.0", mark="stated", via=f"https://github.com/{GITHUB_YEARS[year]}",
                        note="MEDSL's own earlier release, read by git (the repository now points to its Dataverse "
                             "sets, which sit behind a guestbook; pipeline/intake/medsl_precinct.py --compare-dataverse "
                             "matches the files by MD5); added up to the contest by pipeline/intake/medsl_precinct.py, "
                             "files " + ", ".join(sorted(files)))
    doi = {2024: "doi:10.7910/DVN/NYTPDU", 2022: "doi:10.7910/DVN/UYQIEP"}[year]
    return F.source(f"MIT Election Data and Science Lab, Precinct-Level Returns {year} by Individual State, Harvard "
                    f"Dataverse {doi}, version {rec.get('version')}", f"https://doi.org/{doi.split(':', 1)[1]}",
                    rec.get("read_utc"), "CC0 1.0", mark="stated", via=f"https://doi.org/{doi.split(':', 1)[1]}",
                    note="precinct returns compiled by MEDSL from each state's official sources (named per state in "
                         "its README); added up to the contest by pipeline/intake/medsl_precinct.py, files "
                         + ", ".join(sorted(files)))


def _deciding_words(earlier):
    """The State Board's November contests whose name was on an earlier ballot that year (pipeline/local_ncsbe.py,
    medsl_shape): the deciding round, in the State Board route's words, so that both routes mark it alike (the
    orchestrator, 2026-11-07 09:53 UTC)."""
    import local_ncsbe as NS
    return NS.deciding_words(earlier)


def _owns(r):
    """The contests this build writes: MEDSL's, Indiana's own of 2024 (certified_in), and the State Board's of MEDSL's
    general dates (certified_nc)."""
    src = (r.get("result") or {}).get("source")
    return src in ("medsl", "in_enr", "la_sos") or (src == "ncsbe" and (r.get("date") or "")[5:7] == "11" and r.get("year") in MEASURE_YEARS
                              and (r.get("level") == "measure" or r.get("year") in YEARS))


def build(out_dir, with_p=True):
    commit = L.git_commit()
    klarner = L.load_klarner()
    pres, nara_rows = L.president_party()
    m = {y: load(y) for y in MEASURE_YEARS}
    chk = {y: checks(y) for y in MEASURE_YEARS}
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
    bad = {y: quality(y) for y in MEASURE_YEARS}
    for y, sts in CERTIFIED_STATES.items():   # a state whose own certified file replaced MEDSL's (certified_in)
        for st in sts:
            bad[y].pop(st, None)
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
            if year in KLARNER_CHECKED or year < 2024:
                continue   # Klarner's 1967-2022 are the record; MEDSL's 2018 and 2022 are its check (check_2022)
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
                              "total_votes": sum(x["votes"] for x in c["candidates"]),
                              "source": c.get("source", "medsl")},
                   "forecasts": []}
            if c.get("votes_source"):   # North Carolina's certified counts in place of MEDSL's (certified_legislature)
                rec["result"]["votes_source"] = "ncsbe"
                rec["notes"] = [c["certified_note"]]
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
                    p["forecast_scope"] = L.FORECAST_SCOPE[r_["cls"]]
                    counts[f"{level} {year}: p computed, partisan"] += 1
            rec["p"] = p
            files[(level, year, c["state"])].append(L._compact(rec))

    # -- local races: routes (b) and (c), from like races of earlier years
    lrows = {y: local_rows([c for c in m[y] if c["state"] not in bad[y]]) for y in YEARS}
    dens = {}
    bt = backtest_local_partisan(write=True, prow=prow, pres=pres)
    lp = {}
    for y in YEARS:
        rows_y = lean_rows(y, m[y])
        lp[y] = None if rows_y is None else {id(r_["m"]): r_ for r_ in rows_y}
    fits = {y: L.fit_before(prow, pres, y) if lp[y] is not None else (None, 0) for y in YEARS}
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
            rec = {"id": cid(f"{year}-local-{c['state']}-{L._slug(c['office'])[:60]}-{L._slug(where)}".rstrip("-")
                             + (f"-{c['date']}" if c.get("id_date") else "")),
                   "year": year, "date": c["date"] or None, "level": "local",
                   "place": {"state": c["state"], "district": None if c["district"] in ("", "STATEWIDE") else c["district"],
                             "counties": None if scope == "state" and c["district"] == "STATEWIDE" else c["counties"]},
                   "office": c["office"].title(), "office_type": office_type(c["office"]), "office_scope": scope,
                   "election": c.get("election_words") or ((("general" if c["stage"] == "GEN" else
                                                               c["stage"].lower())
                                                              + (", special" if c["special"] else ""))
                                                             if not c.get("earlier_round") else
                                                             _deciding_words(c["earlier_round"])),
                   "seats": c["magnitude"] if (c.get("magnitude") or 1) > 1 else None,
                   "result": {"candidates": _cands_out(c["candidates"], c.get("magnitude") or 1),
                              "total_votes": sum(x["votes"] for x in c["candidates"]),
                              "source": c.get("source", "medsl")},
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
            elif route == "partisan":
                p = local_partisan_p(rec, c, lp[year], bool(bt.get(year, {}).get("computed")),
                                     fits[year],
                                     bt.get(year), pres, year, commit, with_p, counts)
            elif route == "not computed":
                p["not_computed"] = key
                counts[f"local {year}: not computed, {key.split(':')[0][:50]}"] += 1
            else:
                p = class_p(rec, c, route, key, train, dens, (year, key), commit, with_p, counts, f"local {year}",
                            c["magnitude"] if route == "boundary" else 1)
            rec["p"] = p
            files[("local", year, c["state"])].append(L._compact(rec))

    # -- measures and retentions: the threshold from the state's law, the forecast from like past measures
    import measures as MS
    book = MS.load_thresholds()
    mref = MS.coverage({y: m[y] for y in MEASURE_YEARS})
    mrows = {y: MS.rows([c for c in m[y] if c["state"] not in bad[y]], y, mref) for y in MEASURE_YEARS}
    mdens, mtest, mhalf = {}, [], []
    for year in MEASURE_YEARS:
        train = [r_ for y in MEASURE_YEARS if y < year for r_ in mrows[y]]
        for r_ in mrows[year]:     # the route's calibration near 1/2: every statewide question, threshold read or not
            if r_["key"].startswith("statewide"):
                tr = [x["s"] for x in train if x["key"] == r_["key"]]
                if tr:
                    mhalf.append({"year": year, "key": r_["key"], "train": len(tr),
                                  "near": {str(hh): [sum(1 for x in tr if abs(x - 0.5) <= hh) / len(tr),
                                                     abs(r_["s"] - 0.5) <= hh] for hh in L.WINDOWS}})
    # the orchestrator, 2026-11-07 07:25: write the route's near-1/2 shortfall onto each p it gives, in these words
    hw = str(L.WINDOWS[-1])
    mnote = {}
    for key in {r_["key"] for r_ in mhalf}:
        rs = [r_ for r_ in mhalf if r_["key"] == key]
        exp, got = sum(r_["near"][hw][0] for r_ in rs), sum(r_["near"][hw][1] for r_ in rs)
        if got > exp:
            mnote[key] = (f"this route's back-test shows more near-even finishes than it forecast ({got} against "
                          f"{exp:.1f} within {L.WINDOWS[-1] * 100:.0f} points, {min(r_['year'] for r_ in rs)} to "
                          f"{max(r_['year'] for r_ in rs)}), so p may be low")
    for year in MEASURE_YEARS:
        train = [r_ for y in MEASURE_YEARS if y < year for r_ in mrows[y]]
        for c in m[year]:
            if not c["question"]:
                continue
            kind, scope = MS.kind_of(c), MS.scope_of(c, mref, year)
            yes, no = yes_no(c)
            rec = {"id": cid(f"{year}-measure-{c['state']}-{L._slug(c['office'])[:60]}"
                             + (f"-{L._slug(c['subject'])}" if c.get("subject") else "")
                             + ("" if scope == "statewide" else f"-{c['counties'][0] if c['counties'] else 'none'}")
                             + (f"-{c['date']}" if c.get("id_date") else "")),
                   "year": year, "date": c["date"] or None, "level": "measure",
                   "place": {"state": c["state"], "district": None if c["district"] in ("", "STATEWIDE") else c["district"],
                             "counties": None if scope == "statewide" else c["counties"]},
                   "question": {"title": c["office"].title(), "subject": (c.get("subject") or "").title() or None,
                                "kind": kind, "scope": scope, "type": MS.type_of(c) if kind == "measure" else None},
                   "result": {"candidates": [{"name": x["name"], "votes": x["votes"],
                                              "votes_incomplete": True if x.get("votes_missing_in_some_precincts")
                                              else None} for x in c["candidates"]],
                              "total_votes": sum(x["votes"] for x in c["candidates"]),
                              "source": c.get("source", "medsl"),
                              "yes_share": round(yes / (yes + no), 6) if yes + no else None},
                   "forecasts": []}
            notes = []
            # MEDSL's wording of a local question does not show its place; the State Board's file names it (or the
            # question is one county's own: pipeline/intake/ncsbe.py, generic), and Indiana's gives each question
            # once with its counties and its type, title and text
            by_county = c.get("source", "medsl") == "medsl"
            if scope == "local" and by_county:
                notes.append("counted by county: MEDSL's wording of a local question does not show which place holds "
                             "it, so a question held across several counties appears once per county")
            if c.get("own_county"):
                import local_ncsbe as NS
                notes.append(NS.OWN_COUNTY_NOTE)
            if c.get("read_as_question"):
                notes.append("filed in the source as a candidate contest; read as a question, since its two lines are "
                             "a yes and a no")
            if c.get("joined_from"):
                notes.append("the source files its yes and its no under different wordings (" +
                             " | ".join(x.title() for x in c["joined_from"]) + "); joined")
            if notes:
                rec["notes"] = notes
            label = f"measure {year}"
            if c.get("one_answer_only"):
                p = {"not_computed": "the source gives one answer only for this question (its other answer is filed "
                                     "apart under other words and could not be matched)"}
                counts[f"{label}: not computed, one answer only"] += 1
            elif yes + no <= 0:
                p = {"not_computed": "no yes or no votes"}
                counts[f"{label}: not computed, no votes"] += 1
            elif c["state"] in bad[year]:
                p = {"not_computed": bad[year][c["state"]]}
                counts[f"{label}: not computed, the state's counts do not add up"] += 1
            elif any(x.get("votes_missing_in_some_precincts") for x in c["candidates"]):
                p = {"not_computed": "the source redacts some precincts' counts for this question"}
                counts[f"{label}: not computed, redacted"] += 1
            elif scope == "partial":
                p = {"not_computed": "a statewide question, but the source holds only part of the state's counties "
                                     "this year, so its count is not the state's"}
                counts[f"{label}: not computed, the source holds part of the state"] += 1
            elif scope == "local":
                p = {"not_computed": f"a local {kind}: its threshold is the one state law sets for its kind of "
                                     f"{'measure' if kind == 'measure' else 'judge'}, which the source's wording does "
                                     f"not show" + (", and the place that holds it is not shown either (it is "
                                                    "counted by county)" if by_county else "")
                                     + "; not inferred (the orchestrator, 2026-11-07 06:16)"}
                counts[f"{label}: not computed, local"] += 1
            else:
                rule, how, why = MS.rule_for(c, kind, book, year)
                if rule is None:
                    p = {"not_computed": why}
                    counts[f"{label}: not computed, threshold: {why.split(':')[0][:70]}"] += 1
                else:
                    t = rule["t"]
                    key = f"{scope} {kind}"
                    rec["threshold"] = {k: rule.get(k) for k in ("t", "rule", "citation", "url", "quote", "read_utc")}
                    rec["threshold"]["matched"] = how
                    if (year, key, t) not in mdens:
                        mdens[(year, key, t)] = MS.density_at(train, key, t)
                    f, N, h, kin = mdens[(year, key, t)]
                    n = yes + no - 1
                    rec["two_way"] = {"votes": [yes, no], "n_other_voters": n, "share_yes": round(yes / (yes + no), 6)}
                    if f is None:
                        p = {"not_computed": f"fewer than {L.MIN_CLASS} like measures in earlier years in the sources "
                                             f"taken in ({N}) for the class '{key}'"}
                        counts[f"{label}: not computed, too few like measures"] += 1
                    else:
                        rec["forecasts"].append({"by": "the model's own", "method": L.METHOD, "route": "like past measures",
                                                 "class": key, "like_measures": N,
                                                 "window": [round(t - h, 4), round(t + h, 4)], "in_window": kin,
                                                 "q": round(f * 2 * h, 5), "source": "model"})
                        s_ = yes / (yes + no)
                        tr = [r_["s"] for r_ in train if r_["key"] == key]
                        mtest.append({"year": year, "key": key, "t": t, "s": s_, "q_own": f * 2 * h,
                                      "in_own": abs(s_ - t) <= h,
                                      "near": {str(hh): [sum(1 for x in tr if abs(x - t) <= hh) / len(tr),
                                                         abs(s_ - t) <= hh] for hh in L.WINDOWS}})
                        if not with_p:
                            p = {}
                        elif f <= 0:
                            p = {"value": 0.0, "event": 0.0, "reason": f"no like measure of {N} finished within "
                                                                      f"{h:.0%} of the threshold"}
                            counts[f"{label}: p = 0, no like measure near the threshold"] += 1
                        else:
                            p = MS.p_block(f, t, n, f"the model's own ({L.METHOD}), like past measures")
                            if key in mnote:
                                p["note"] = mnote[key]
                            counts[f"{label}: p computed, {key}"] += 1
            rec["p"] = p
            counts[f"{label}: {scope} {kind}"] += 1
            files[("measure", year, c["state"])].append(L._compact(rec))

    write_checks = out_dir == os.path.join(L.REPO, "data") or os.environ.get("D3_WRITE_CHECKS")
    if write_checks:
        with open(os.path.join(L.REPO, "data", "measure", "backtest-measures.json"), "w") as f:
            json.dump(backtest_measures(mtest, mhalf), f, indent=1)
        with open(os.path.join(L.REPO, "data", "local", "backtest-local-classes.json"), "w") as f:
            json.dump(backtest_local_classes(files), f, indent=1)
    cal = calibrate_local(files)
    for g, r in cal.items():
        if r["adopted"]:
            for (level, year, st), cs in files.items():
                if level == "local":
                    for rec in cs:
                        nh = _near_half(rec)
                        if nh and nh[0] == g:
                            if "value" in rec["p"] and (rec["forecasts"][-1].get("calibration") or not rec["p"]["value"]):
                                counts[f"local {year}: {g}: p calibrated" if rec["p"]["value"] else
                                       f"local {year}: {g}: p = 0"] += 1
                            elif CAL_NOTE in rec["p"].get("not_computed", ""):
                                counts[f"local {year}: {g}: not computed, no earlier year to calibrate on"] += 1
    if write_checks:
        with open(os.path.join(L.REPO, "data", "local", "calibration-local.json"), "w") as f:
            json.dump({"about": "the orchestrator's ruling of 2026-11-07 06:38: local races' p by like races, and by "
                                "the transferred Democrat-against-Republican route, calibrated to earlier years' "
                                "near-ties (seen over expected near 1/2), by office type where the fitting years "
                                f"expected {CAL_MIN_EXPECTED} or more, else pooled; adopted for a route only if it "
                                "passes the robustness test (brief D3, amended 2026-11-07 08:36: it improves the "
                                "out-of-sample test, the count near 1/2 and the deviance by office type, over every "
                                "scored year with no tested cell made worse, and still does with any one scored year "
                                "left out; each route's robustness_rule). Where not adopted, p is uncalibrated and each "
                                "p the factor would move carries calibration_not_of_record. Built by "
                                "pipeline/local_medsl.py build.", "routes": cal}, f, indent=1)
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
        others, other_src, _ = L.kept_from_others(path, _owns)
        head["sources"] = dict(other_src, **head["sources"])
        used = {(x.get("result") or {}).get("source") for x in cs + others}
        if "medsl" not in used:   # North Carolina's local file of 2022: every contest is the State Board's now
            del head["sources"]["medsl"]
        certified = any((x.get("result") or {}).get("votes_source") == "ncsbe" for x in cs + others)
        if "ncsbe" in used or certified:   # the State Board's contests, or its counts (certified_legislature): every
            import local_ncsbe as NS        # file they come from, and for its contests their FIPS codes' source
            head["sources"]["ncsbe"] = NS.block_for(cs + others)
            if "ncsbe" in used:
                head["sources"]["fips"] = NS.fips_source()
        if "la_sos" in used:   # Louisiana's own official results (certified_la), and its parishes' FIPS codes
            import local_la as LA
            head["sources"]["la_sos"] = LA.source_block()
            head["sources"]["fips"] = LA.fips_source()
        if "in_enr" in used:   # Indiana's own certified file (certified_in)
            import local_in as LI
            head["sources"]["in_enr"] = LI.source_block()
        L.write_level_file(path, head, cs + others)
        sz = os.path.getsize(path)
        total += sz
        by_level[level] += sz
    # a state's file from an earlier build that this build no longer writes would stand stale beside the rest
    # (Michigan's 2022 measures, which were rejected-ballot lines until the fix of 2026-11-07): remove it
    for level, year in {(lv, y) for lv, y, _ in files}:
        for path in glob.glob(os.path.join(out_dir, level, str(year), "*.json")):
            st = os.path.basename(path)[:-5]
            if (level, year, st) not in files and len(st) == 2:
                others, other_src, ohead = L.kept_from_others(path, _owns)
                if others:   # another source's contests stay; the file is theirs now
                    print(f"kept {os.path.relpath(path, out_dir)}: no MEDSL {level} contests there, but another "
                          f"source's")
                    continue
                os.remove(path)
                print(f"removed {os.path.relpath(path, out_dir)}: this build has no {level} contests there")
    print(f"wrote {sum(len(v) for v in files.values()):,} contests in {len(files):,} files, {total / 1e6:.1f} MB: "
          + ", ".join(f"{k} {v / 1e6:.1f} MB" for k, v in sorted(by_level.items())))
    counts.update({f"left out, no vote anywhere, {y}": EMPTY[y] for y in YEARS})
    print(json.dumps(dict(sorted(counts.items())), indent=1))
    return files, counts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("what", choices=["check2018", "check2022", "check-oaarcy", "build", "backtest-local-partisan"])
    ap.add_argument("--out", default=os.path.join(L.REPO, "data"))
    a = ap.parse_args()
    if a.what in ("check2018", "check2022"):
        year = int(a.what[5:])
        out = check_2022(year=year)
        path = os.path.join(L.REPO, "data", "local", f"check-{year}-medsl-klarner.json")
        with open(path, "w") as f:
            json.dump(out, f, indent=1)
        print(json.dumps(out["tallies"], indent=1))
    elif a.what == "check-oaarcy":
        out = check_oaarcy()
        with open(os.path.join(L.REPO, "data", "local", "check-2022-oaarcy.json"), "w") as f:
            json.dump(out, f, indent=1)
        print(json.dumps({st: {k: v for k, v in x.items() if not k.startswith("against")} for st, x in
                          out["by_state"].items()}, indent=1))
    elif a.what == "backtest-local-partisan":
        print(json.dumps(backtest_local_partisan(), indent=1))
    else:
        build(a.out)


if __name__ == "__main__":
    main()
