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

def load(year):
    out = []
    for path in sorted(glob.glob(os.path.join(NORM, str(year), "*.jsonl"))):
        with open(path) as f:
            out.extend(json.loads(line) for line in f)
    return out


def checks(year):
    with open(os.path.join(NORM, f"checks-{year}.json")) as f:
        return json.load(f)


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
        c = kl[k]
        kd = sum(a["votes"] or 0 for a in c["cands"] if a["party"] == "d")
        kr = sum(a["votes"] or 0 for a in c["cands"] if a["party"] == "r")
        md = sum(x["votes"] for x in m["candidates"] if major(x) == "D" and not x.get("writein"))
        mr = sum(x["votes"] for x in m["candidates"] if major(x) == "R" and not x.get("writein"))
        kw = max((a for a in c["cands"] if not a["scattering"]), key=lambda a: a["votes"] or 0, default=None)
        mw = max(ballot(m["candidates"]) or m["candidates"], key=lambda x: x["votes"], default=None)
        same_winner = bool(kw and mw and name_key(kw["name"])[0] == name_key(mw["name"])[0])
        out["same winner" if same_winner else "winner differs"] += 1
        if kd == md and kr == mr:
            out["D and R votes identical"] += 1
        else:
            tot = max(kd + kr, 1)
            rel = (abs(kd - md) + abs(kr - mr)) / tot
            out["D and R votes within 1%" if rel <= 0.01 else "D and R votes differ by more than 1%"] += 1
            diffs.append({"state": k[0], "chamber": "state-upper" if k[1] else "state-lower", "district": dn,
                          "klarner": [kd, kr], "medsl": [md, mr], "relative": round(rel, 4),
                          "same_winner": same_winner})
    diffs.sort(key=lambda d: -d["relative"])
    return {"tallies": dict(out), "differences": diffs}


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
            by22[(m["state"], m["office"], m["district"])] = m
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
        prev = by22.get((m["state"], m["office"], m["district"]))
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
        if name_key(d[0]["name"]) + ("D",) in st_sit:
            inc += 1
        if name_key(r[0]["name"]) + ("R",) in st_sit:
            inc -= 1
        Lv = lean.get((m["state"], sen))
        rows.append({"m": m, "year": 2024, "state": m["state"], "sen": sen,
                     "y": d[0]["votes"] / (d[0]["votes"] + r[0]["votes"]), "N": d[0]["votes"] + r[0]["votes"],
                     "cls": cls, "xl": xl, "ulag": ulag, "inc": inc, "L": Lv[0] if Lv else 0.0,
                     "L_year": Lv[1] if Lv else None, "Lmiss": 0 if Lv else 1, "lines": lines, "last": last,
                     "d": d[0], "r": r[0], "ballot": b})
    return rows


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
    if m["stage"] != "GEN":
        return ("not computed", f"a {m['stage'].lower()} contest: {L.METHOD} classes local races at general elections")
    if len(b) <= k:
        return ("zero", "one name on the ballot for each seat (unopposed): p is 0")
    if any(x.get("votes_missing_in_some_precincts") for x in b):
        return ("not computed", "the source redacts some precincts' counts for this contest")
    nd = sum(1 for x in b if major(x) == "D")
    nr = sum(1 for x in b if major(x) == "R")
    ot = office_type(m["office"])
    if k > 1:
        slate = ("both major parties on the ballot" if nd and nr else "one major party or none")
        return ("boundary", f"local {ot}, {k if k < 4 else '4+'} seats at once, {slate}")
    if nd == 1 and nr == 1:
        return ("not computed", "a local race between a Democrat and a Republican: the model's own forecast for "
                                "these needs the place's partisan lean, which D3-v1.1 has at state legislative level only")
    nonpartisan = all((x.get("party") or "NONPARTISAN") in ("NONPARTISAN", "") for x in b)
    kind = ("nonpartisan" if nonpartisan else "one major party against others" if nd + nr == 1 else
            "two or more of one major party" if nd + nr >= 2 else "no Democrat or Republican")
    n = len(b)
    return ("class", f"local {ot}, {kind}, {n if n < 4 else '4+'} candidates")


def local_rows(contests):
    rows = []
    for m in contests:
        if m["dataverse"] != "LOCAL" or m["question"]:
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
    srcs = {y: _src_medsl(y, chk[y], chk[y].get("files", {}).keys()) for y in YEARS}
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
    rows24 = {id(r_["m"]): r_ for r_ in leg_rows_2024(m[2024], m[2022], klarner)}
    for year in YEARS:
        for c in m[year]:
            if c["office"] not in LEG:
                continue
            level = "state-upper" if LEG[c["office"]] else "state-lower"
            if year == 2022:
                continue   # Klarner's 2022 is the record; MEDSL's 2022 is its check (check_2022)
            rec = {"id": cid(f"{year}-{level}-{c['state']}-{L._slug(c['district'] or 'at large')}"
                             + ("" if c["stage"] == "GEN" and not c["special"] else f"-{c['stage'].lower()}"
                                + ("-special" if c["special"] else ""))),
                   "year": year, "date": c["date"] or None, "level": level,
                   "place": {"state": c["state"], "district": (district_no(c["district"]) or c["district"] or None)},
                   "election": ("general" if c["stage"] == "GEN" else c["stage"].lower())
                               + (", special" if c["special"] else ""),
                   "seats": c["magnitude"] if (c.get("magnitude") or 1) > 1 else None,
                   "result": {"candidates": _cands_out(c["candidates"], c.get("magnitude") or 1),
                              "total_votes": sum(x["votes"] for x in c["candidates"]), "source": "medsl"},
                   "forecasts": []}
            p = {}
            b = ballot(c["candidates"])
            k = c.get("magnitude") or 1
            r_ = rows24.get(id(c))
            top = sorted(c["candidates"], key=lambda x: -x["votes"])
            if len(b) <= k:
                p = {"value": 0.0, "event": 0.0, "reason": "one name on the ballot for each seat (unopposed): p is 0"}
                counts[f"{level} {year}: p = 0"] += 1
            elif r_ is None:
                p["not_computed"] = ("not a single-seat general with one Democrat and one Republican on the ballot: "
                                     f"{L.METHOD}'s like-race classes for these are of Klarner's years and are not "
                                     "yet applied to MEDSL's 2024 returns")
                counts[f"{level} {year}: not computed, other structure"] += 1
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
    lrows = {y: local_rows(m[y]) for y in YEARS}
    dens = {}
    for year in YEARS:
        train = [r_ for y in YEARS if y < year for r_ in lrows[y]]
        by_m = {id(r_["m"]): r_ for r_ in lrows[year]}
        for c in m[year]:
            if c["dataverse"] != "LOCAL" or c["question"]:
                continue
            route, key = local_structure(c)
            rec = {"id": cid(f"{year}-local-{c['state']}-{L._slug(c['office'])[:60]}-{L._slug(c['district'] or '')}"
                             .rstrip("-")),
                   "year": year, "date": c["date"] or None, "level": "local",
                   "place": {"state": c["state"], "district": c["district"] or None, "counties": c["counties"]},
                   "office": c["office"].title(), "office_type": office_type(c["office"]),
                   "election": ("general" if c["stage"] == "GEN" else c["stage"].lower())
                               + (", special" if c["special"] else ""),
                   "seats": c["magnitude"] if (c.get("magnitude") or 1) > 1 else None,
                   "result": {"candidates": _cands_out(c["candidates"], c.get("magnitude") or 1),
                              "total_votes": sum(x["votes"] for x in c["candidates"]), "source": "medsl"},
                   "forecasts": []}
            p = {}
            if route == "zero":
                p = {"value": 0.0, "event": 0.0, "reason": key}
                counts[f"local {year}: p = 0"] += 1
            elif route == "not computed":
                p["not_computed"] = key
                counts[f"local {year}: not computed, {key.split(':')[0][:50]}"] += 1
            else:
                r_ = by_m.get(id(c))
                top = sorted(c["candidates"], key=lambda x: -x["votes"])
                kk = c["magnitude"] if route == "boundary" else 1
                if r_ is None:
                    p["not_computed"] = "no votes for the deciding pair"
                    counts[f"local {year}: not computed, no votes"] += 1
                elif any(x.get("writein") or _is_generic(x["name"]) for x in top[kk - 1:kk + 1]):
                    p["not_computed"] = ("a write-in line is in the pair that decided this contest; the like-race "
                                         "classes are of candidates on the ballot")
                    counts[f"local {year}: not computed, write-in in the deciding pair"] += 1
                else:
                    b = sorted(ballot(c["candidates"]), key=lambda x: -x["votes"])
                    pair = b[kk - 1:kk + 1]
                    n = pair[0]["votes"] + pair[1]["votes"] - 1
                    rec["boundary" if route == "boundary" else "two_party"] = {
                        "votes": [pair[0]["votes"], pair[1]["votes"]], "n_other_voters": n,
                        "share_first": round(pair[0]["votes"] / max(n + 1, 1), 6)}
                    if (year, key) not in dens:
                        dens[(year, key)] = L.class_density(train, key)
                    f, N, h, kin = dens[(year, key)]
                    if f is None:
                        p["not_computed"] = (f"fewer than {L.MIN_CLASS} like races in earlier years in the sources "
                                             f"taken in ({N}) for the class '{key}'")
                        counts[f"local {year}: not computed, too few like races"] += 1
                    else:
                        fc = {"by": "the model's own", "method": L.METHOD, "route": route, "class": key,
                              "like_races": N, "window": [round(0.5 - h, 2), round(0.5 + h, 2)], "in_window": kin,
                              "q": round(f * 2 * h, 5), "source": "model"}
                        if route == "boundary":
                            fc["note"] = "not yet checked"
                        rec["forecasts"].append(fc)
                        if with_p and n >= 1 and f > 0:
                            sd_eq = 1.0 / (math.sqrt(2 * math.pi) * f)
                            p = L._p_block(n, 0.5, sd_eq, f"the model's own ({L.METHOD}), like past races", commit)
                            counts[f"local {year}: p computed, {route}"] += 1
                        elif with_p:
                            p = {"value": 0.0, "event": 0.0, "reason": f"no like race in {N} finished within the window"}
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
            yes = sum(x["votes"] for x in c["candidates"] if x["name"] in ("YES", "FOR", "APPROVE", "RETAIN"))
            no = sum(x["votes"] for x in c["candidates"] if x["name"] in ("NO", "AGAINST", "REJECT", "NOT RETAIN",
                                                                          "DO NOT RETAIN"))
            rec = {"id": cid(f"{year}-measure-{c['state']}-{L._slug(c['office'])[:60]}"
                             + (f"-{L._slug(c['subject'])}" if c.get("subject") else "")
                             + ("" if scope == "statewide" else f"-{c['counties'][0]}")),
                   "year": year, "date": c["date"] or None, "level": "measure",
                   "place": {"state": c["state"], "district": c["district"] or None,
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
                "sources": {"medsl": srcs[year], "model": src_model, "nara": src_nara, "klarner": src_klarner}}
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
