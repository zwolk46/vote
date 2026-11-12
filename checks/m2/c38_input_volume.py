"""C38. The input-volume check of the seventh pass (the orchestrator's words of 2026-11-07 18:54 and 20:28): for every
state-year with a computed p, the count the p's n comes from against a count that does not come from the same file,
and the list of every state-year off by more than 0.5%. Built apart from D3's pipeline/local_volume.py and its
report section 29, which were not read before this was written (the orchestrator's reason: two volume checks built
separately catch what one alone misses); c39 compares the two lists.

Why a volume check: every earlier check reproduces p from the record's own inputs, so a doubled count (MEDSL's Idaho
2022 file, Klarner's New Hampshire 2022) passes them all, since shares are unchanged while n doubles.

What is compared (every figure [measured] from the raw files in ~/.cache/vote-m2/, D1's and D2's records [stated]):
  38.1 the inventory: every p by level, its source file and state-year (what each later section covers).
  38.2 MEDSL's precinct files (the p of data/local, data/measure, the 2024 legislatures, NH 2022's votes): each file's
       President, US Senate, US House (by district) and Governor totals, added up by m2medsl.volume_summary over
       every row, against D1's and D2's certified totals; and the file's rows named as totals (COUNTY TOTAL, -1).
  38.3 Klarner's state legislative returns against MEDSL's STATE SENATE and STATE HOUSE totals by district, where a
       MEDSL file exists (2016's state set, 2018's files, 2022's): the state-year's matched districts' sums, the
       candidates at exactly twice the other's count, the unmatched districts.
  38.4 North Carolina's State Board files (data/local, measure, primary from ncsbe): each general election's
       President, US Senate, US House, Governor and legislative totals against D1, D2 and Klarner.
  38.5 Indiana's 2024 files (in_enr): the federal and state offices against D1 and D2, the legislatures against
       MEDSL's 2024 Indiana file.
  38.6 Louisiana's 2024 workbook (la_sos): the presidency and the six House seats against D1 and D2 (c18's gate again,
       from my own parse).
  38.7 D1's and D2's records themselves against MEDSL's state-level files (U.S. President 1976-2024, U.S. Senate
       1976-2024, U.S. House 1976-2024) and against the precinct files of 38.2.
  38.8 the state-years with p and no second count in any source read (MEDSL's 2020 local set, North Carolina's odd
       years and primaries, New Jersey's and Virginia's 2023 and 2025 lists, Klarner before 2016 and in 2020), and
       for Klarner's a coarse tier: the chamber's total against D2's US House or D1's presidential total that day.
  38.9 the list: every state-year off by more than 0.5% on a direct comparison, with the side the p rests on.
Thresholds: 0.5% on a state-year's summed comparison (the orchestrator's); a contest is listed when off by more than
0.5% too, and a candidate at exactly 2x is counted. Nothing from pipeline/ is imported.
"""
import collections
import csv
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402
import m2medsl as M  # noqa: E402

CACHE = L.CACHE
SEVENTH = os.path.join(CACHE, "seventh")
KLARNER = os.path.join(CACHE, "klarner_202slers_uoa_contest20230810.csv")
TOL = 0.005
LEVELS_D3 = ("state-upper", "state-lower", "local", "measure", "primary")
csv.field_size_limit(1 << 24)


def pct(a, b):
    return (a - b) / b if b else float("nan")


def fmtr(a, b):
    return f"{a:,} vs {b:,} ({pct(a, b):+.2%})" if b else f"{a:,} vs {b:,}"


def nkey(s):
    return re.sub(r"[^A-Z0-9]", "", (s or "").upper())


VT_ABBR = {"ADD": "ADDISON", "BEN": "BENNINGTON", "CAL": "CALEDONIA", "CHI": "CHITTENDEN", "ESX": "ESSEX", "ESS": "ESSEX",
           "FRA": "FRANKLIN", "GI": "GRANDISLE", "LAM": "LAMOILLE", "ORA": "ORANGE", "ORL": "ORLEANS", "RUT": "RUTLAND",
           "WAS": "WASHINGTON", "WDH": "WINDHAM", "WDS": "WINDSOR"}   # MEDSL's 2018 Vermont codes (ADD-1, ADDRUT, WDH-WDS-1)


def vt_key(code):
    """MEDSL's Vermont code in Klarner's words: ADD1 -> ADDISON1, ADDRUT -> ADDISONRUTLAND, GI-CHI -> GRANDISLECHITTENDEN"""
    c = nkey(code)
    m = re.match(r"^([A-Z]+)(\d*)$", c)
    if not m:
        return c
    letters, digits = m.groups()
    out = ""
    pat = re.compile("^(" + "|".join(sorted(VT_ABBR, key=len, reverse=True)) + ")")
    while letters:
        mm = pat.match(letters)
        if not mm:
            return c
        out += VT_ABBR[mm.group(1)]
        letters = letters[len(mm.group(1)):]
    return out + digits


def dkey(code):
    """one key for a legislative district code: digits -> the number (001A, '1, seat 2' -> 1); else letters and
    digits with the number last (BELKNAP 1, 'Belknap 1' -> BELKNAP1; ADDISON-1 -> ADDISON1; '10th Bristol',
    Klarner's 'bristol 10' -> BRISTOL10; 'DISTRICT 5' -> 5)"""
    c = (code or "").strip().upper()
    c = re.sub(r"^(DISTRICT|DIST\.?|SD|HD|LD)\s*", "", c)
    c = re.sub(r"\b(POSITION|POS|SEAT)\s*[A-Z0-9]+\b", "", c).strip()   # Washington's two positions, 'seat 2': one district
    c = re.sub(r"(?<=\d)[AB]$", "", c)   # Idaho's 1A and 1B: one district
    m = re.match(r"^0*(\d+)", c)
    if m and not re.search(r"[A-Z]{2,}", c):
        return str(int(m.group(1)))
    c = re.sub(r"\b(AND|&)\b", " ", c)   # 'Bristol and Plymouth' (MEDSL), 'bristol plymouth' (Klarner)
    m = re.match(r"^0*(\d+)(ST|ND|RD|TH)?\s+(.+)$", c)
    if m:
        return nkey(m.group(3)) + str(int(m.group(1)))
    m = re.match(r"^(.*?)\s*0*(\d+)$", c)
    if m and m.group(1):
        return nkey(m.group(1)) + str(int(m.group(2)))
    return nkey(c)


# ------------------------------------------------------------------------------------------ the records
def every_p():
    """every record with a computed p: (level, year, state, source, votes_source) -> count, and the files the source
    block names"""
    out = collections.Counter()
    files = collections.defaultdict(set)
    for level in LEVELS_D3:
        for f in sorted(glob.glob(os.path.join(L.DATA, level, "[0-9]*", "*.json"))):
            d = L.load_json(f)
            srcs = d.get("sources") or {}
            for c in d.get("contests", []):
                p = c.get("p") or {}
                if "value" not in p:
                    continue
                s = (c.get("result") or {}).get("source") or "?"
                vs = (c.get("result") or {}).get("votes_source") or ""
                key = (level, d["year"], d["state"], s, vs)
                out[key] += 1
                note = (srcs.get(vs or s) or {}).get("note") or ""
                m = re.search(r"files? ([^;]+)$", note)
                if m:
                    for fn in re.split(r",\s*", m.group(1)):
                        files[key].add(fn.strip())
    for level in ("president", "governor", "senate", "house"):
        for f in sorted(glob.glob(os.path.join(L.DATA, level, "[0-9]*.json"))):
            d = L.load_json(f)
            for c in d.get("contests", []):
                p = c.get("p") or {}
                if "value" not in p:
                    continue
                src = (c.get("result") or {}).get("source") or {}
                name = src.get("name", "?") if isinstance(src, dict) else str(src)
                out[(level, d["year"], c["place"]["state"], name[:40], "")] += 1
    return out, files


def d12():
    """D1's and D2's certified counts: (office, year, st, district, special) -> {"total", "cands", "source", "date"};
    office PRESIDENT / US SENATE / US HOUSE / GOVERNOR; district "" for a state, else D2's code (01, AL) or D1's
    district (1, 2); a district total missing in the record is the candidates' sum (marked)"""
    out = {}
    for level, office in (("president", "PRESIDENT"), ("senate", "US SENATE"), ("house", "US HOUSE"), ("governor", "GOVERNOR")):
        for f in sorted(glob.glob(os.path.join(L.DATA, level, "[0-9]*.json"))):
            d = L.load_json(f)
            for c in d.get("contests", []):
                r = c.get("result") or {}
                cands = {nkey(x.get("name")): x.get("votes") or 0 for x in r.get("candidates") or []}
                cands_named = {x.get("name") or "": x.get("votes") or 0 for x in r.get("candidates") or []}
                total = r.get("total_votes")
                summed = total is None
                if summed:
                    total = sum(cands.values())
                src = r.get("source") or {}
                out[(office, d["year"], c["place"]["state"], str(c["place"].get("district") or ""), bool(c.get("special")))] = {
                    "total": total, "cands": cands, "cands_named": cands_named, "summed": summed, "date": c.get("date"), "id": c["id"],
                    "source": (src.get("name") if isinstance(src, dict) else str(src)) or "?"}
    return out


# ------------------------------------------------------------------------------------------ Klarner
def klarner():
    """Klarner's general-election contests: (year, st, chamber, dkey) -> {"votes", "d", "r", "o", "rows", "seats",
    "uncont", "vmiss"}; chamber 'state-upper' for sen=1; the rows of one district (one per seat post) added up"""
    out = {}
    with open(KLARNER, newline="", encoding="utf-8", errors="replace") as f:
        for r in csv.DictReader(f):
            if r.get("etype") != "g":
                continue
            ch = "state-upper" if r.get("sen") == "1" else "state-lower"
            code = (r.get("dname") or "") + " " + (r.get("dno") or "") if r.get("dname") else (r.get("dno") or "")
            k = (int(r["year"]), r["sab"], ch, dkey(code))
            d, rr, o = (int(float(r.get(x) or 0)) for x in ("dvote", "rvote", "ovote"))
            c = out.setdefault(k, {"votes": 0, "d": 0, "r": 0, "o": 0, "rows": 0, "seats": 0, "seats_sq": 0, "uncont": 0, "vmiss": 0, "code": code})
            c["votes"] += d + rr + o
            c["d"] += d
            c["r"] += rr
            c["o"] += o
            c["rows"] += 1
            c["seats"] += int(float(r.get("eseats") or 1))
            c["seats_sq"] += int(float(r.get("eseats") or 1)) ** 2
            c["uncont"] += int(r.get("uncont") == "1")
            c["vmiss"] += int(r.get("vmiss") == "1")
    return out


# ------------------------------------------------------------------------------------------ MEDSL
def medsl_volumes():
    """every volume summary in the cache: (year, st, office, district) -> the contest dict with its file"""
    out = {}
    files = {}
    for f in sorted(glob.glob(os.path.join(M.DERIVED, "*.volume.json"))):
        s = L.load_json(f)
        files[s["file"]] = {"sha256": s["sha256"], "rows": s["rows"], "year": s["year"], "contests": len(s["contests"]),
                            "total_rows": sum(c.get("sub_rows", c["total_rows"]) for c in s["contests"].values())}
        for k, c in s["contests"].items():
            st, date, office, district = k.split("|")
            c = dict(c)
            # the measure compared is the file with its subtotal rows left out (m2medsl.volume_summary's no_sub); the
            # cruder count by name alone (no_total) is kept beside it
            c["named_total"], c["named_total_rows"] = c["no_total"], c["total_rows"]
            c["no_total"], c["total_rows"] = c.get("no_sub", c["no_total"]), c.get("sub_rows", c["total_rows"])
            c["file"] = s["file"]
            c["date"] = date
            out[(s["year"], st, office, district)] = c
    return out, files


def medsl_state_files():
    """MEDSL's state-level files (fetch_seventh_pass.sh; the Senate file from the first pass's cache):
    (office, year, st, district, special) -> {"total": totalvotes, "cands": {name: votes}}"""
    out = {}
    paths = [("PRESIDENT", os.path.join(SEVENTH, "medsl_state", "1976-2024-president.csv")),
             ("US HOUSE", os.path.join(SEVENTH, "medsl_state", "1976-2024-house.tab")),
             ("US SENATE", os.path.join(CACHE, "medsl_1976-2024-senate-state.csv"))]
    for office, p in paths:
        if not os.path.exists(p):
            continue
        with open(p, newline="", encoding="utf-8", errors="replace") as f:
            delim = "\t" if p.endswith(".tab") else ","
            for r in csv.DictReader(f, delimiter=delim):
                if (r.get("stage") or "GEN").upper() != "GEN":
                    continue
                if office == "US HOUSE" and (r.get("runoff") or "").upper() in ("TRUE", "T"):
                    continue
                district = ""
                if office == "US HOUSE":
                    dd = (r.get("district") or "").strip()
                    district = "AL" if dd in ("0", "000", "AL") else f"{int(dd):02d}" if dd.isdigit() else dd
                special = (r.get("special") or "").upper() in ("TRUE", "T")
                k = (office, int(r["year"]), r["state_po"], district, special)
                c = out.setdefault(k, {"total": None, "cands": collections.Counter(), "unofficial": set()})
                try:
                    c["total"] = int(float(r.get("totalvotes") or 0))
                except ValueError:
                    pass
                try:
                    c["cands"][nkey(r.get("candidate"))] += int(float(r.get("candidatevotes") or 0))
                except ValueError:
                    pass
                c["unofficial"].add((r.get("unofficial") or "").upper())
    return out




# ------------------------------------------------------------------------------------------ comparisons
STATEWIDE = ("PRESIDENT", "US SENATE", "GOVERNOR")


def surname(name):
    """the record's surname: the part before the comma (D2 'MORRISEY, PATRICK'; D1 'HARRIS, KAMALA D.'), else the
    last word; 'ARMSTRONG AND STRINDEN' -> ARMSTRONG"""
    n = (name or "").upper()
    n = n.split(",")[0] if "," in n else n
    n = re.split(r"\s+(AND|&|/)\s+", n)[0]
    n = re.sub(r"\b(JR|SR|II|III|IV)\b\.?", "", n)
    words = [w for w in re.split(r"[^A-Z]+", n) if w]
    return words[-1] if "," not in (name or "") and words else (words[0] if words else "")


def lead_match(a_cands, b_cands):
    """the record's leading candidate's votes in the file: the file's one candidate whose key holds the record's
    surname (a fusion state's party lines were added under one name already); (surname, file votes, record votes)"""
    if not b_cands:
        return None, None, None
    lead_key = max(b_cands, key=b_cands.get)
    b_lead = b_cands[lead_key]
    # b_cands is keyed by nkey(name); the surname is read off the key's end for 'LAST, FIRST' forms kept in order
    return lead_key, None, b_lead


def lead_votes(a_cands, rec):
    """(surname, the file's votes for the record's leading candidate, the record's votes), the surname found in
    exactly one file name; None where it is not"""
    if not rec["cands_named"]:
        return None, None, None
    name, b = max(rec["cands_named"].items(), key=lambda kv: kv[1])
    sn = surname(name)
    if len(sn) < 3:
        return sn, None, b
    hits = [(k, v) for k, v in a_cands.items() if sn in k]
    if len(hits) != 1:
        # several lines (a fusion state's party lines, or two namesakes): the sum where every hit holds the first name too
        first = [w for w in re.split(r"[^A-Z]+", name.upper().split(",")[-1]) if len(w) > 1]
        hits = [(k, v) for k, v in hits if first and first[0] in k]
        if len(hits) != 1:
            return sn, None, b
    return sn, hits[0][1], b


def file_contests(mv):
    """the MEDSL contests to compare with D1 and D2: (year, st, office, dcode, special) -> {"nt", "raw", "cands",
    "total_rows", "counties", "file", "date"}; a statewide office's rows under several district codes added up"""
    out = {}
    for (year, st, office, district), c in mv.items():
        if office not in STATEWIDE + ("US HOUSE",):
            continue
        special = district.endswith(" SPECIAL")
        dcode = district.replace(" SPECIAL", "")
        if office == "US HOUSE":
            dcode = "AL" if dcode in ("0", "000", "", "AL", "AT LARGE", "STATEWIDE") else (f"{int(dcode):02d}" if dcode.isdigit() else dcode)
        else:
            dcode = ""
        cell = out.setdefault((year, st, office, dcode, special), {"nt": 0, "raw": 0, "cands": collections.Counter(), "total_rows": 0,
                                                                   "counties": set(), "file": c["file"], "date": c["date"], "codes": []})
        cell["nt"] += sum(c["no_total"].values())
        cell["raw"] += sum(c["cands"].values())
        cell["cands"].update(c["no_total"])
        cell["total_rows"] += c["total_rows"]
        cell["counties"].update(c["counties"])
        cell["codes"].append(district)
    return out


def section_38_2(mv, mf, rec, inv):
    """MEDSL's precinct files against D1 and D2; returns the flagged state-years, the state-years with p and no
    comparison, and each file's statewide standing (for 38.3)"""
    print("38.2 MEDSL's precinct files: President, US Senate, US House and Governor totals against D1's and D2's certified counts")
    print(f"  files summarised: {len(mf)} (m2medsl.volume_summary: every row of the named offices, a precinct's TOTAL row where it has one, else its modes added;"
          " a statewide office's rows under several district codes added up)")
    rests = collections.defaultdict(lambda: collections.Counter())
    for (level, year, st, src, vs), n in inv.items():
        if src == "medsl" or vs == "medsl":
            rests[(year, st)][level] += n
    fc = file_contests(mv)
    by_sy = collections.defaultdict(list)
    for (year, st, office, dcode, special), c in fc.items():
        r = rec.get((office, year, st, dcode, special))
        if r is None and office == "US HOUSE" and dcode == "01":
            r = rec.get((office, year, st, "AL", special))
        if r is None:
            by_sy[(year, st)].append({"office": office, "district": dcode, "special": special, "file": c["file"], "no_record": True,
                                      "raw": c["raw"], "no_total": c["nt"]})
            continue
        sn, a_lead, b_lead = lead_votes(c["cands"], r)
        by_sy[(year, st)].append({"office": office, "district": dcode, "special": special, "file": c["file"], "raw": c["raw"], "no_total": c["nt"],
                                  "rec": r["total"], "off_raw": pct(c["raw"], r["total"]), "off": pct(c["nt"], r["total"]),
                                  "total_rows": c["total_rows"], "lead": sn, "a_lead": a_lead, "b_lead": b_lead,
                                  "lead_off": pct(a_lead, b_lead) if a_lead is not None and b_lead else None,
                                  "rec_id": r["id"], "summed": r["summed"], "counties": len(c["counties"])})
    flagged = []
    standing = {}
    summary = collections.Counter()
    print(f"  state-years with a file and a certified count to compare: {len(by_sy)}; those a p rests on: {sum(1 for k in by_sy if k in rests)}")
    print("  (off = the file with its subtotal rows left out: a row named as a total whose votes equal its county's other rows added up,"
          " or a row whose name the county's other rows extend (\"Allendale\" beside \"Allendale 1\", \"Allendale 2\"...) and whose votes"
          " equal them added up; raw = every row; lead = the record's leading candidate's votes, file vs record, where the surname is found in one file name)")
    for (year, st), rows in sorted(by_sy.items()):
        with_rec = [x for x in rows if not x.get("no_record")]
        if not with_rec:
            summary["no record to compare"] += 1
            continue
        a = sum(x["no_total"] for x in with_rec)
        b = sum(x["rec"] for x in with_rec)
        a_raw = sum(x["raw"] for x in with_rec)
        leads = [x for x in with_rec if x["lead_off"] is not None]
        a_l = sum(x["a_lead"] for x in leads)
        b_l = sum(x["b_lead"] for x in leads)
        off = pct(a, b)
        off_l = pct(a_l, b_l) if leads else None
        worst = max(with_rec, key=lambda x: abs(x["off"]) if x["off"] == x["off"] else 0)
        n_off = sum(1 for x in with_rec if abs(x["off"]) > TOL)
        n_off_l = sum(1 for x in leads if abs(x["lead_off"]) > TOL)
        total_rows = sum(x["total_rows"] for x in with_rec)
        on = rests.get((year, st))
        standing[(year, st)] = {"off": off, "off_lead": off_l, "contests": len(with_rec), "file": with_rec[0]["file"]}
        tag = "p rests on it" if on else "no p rests on it"
        line = (f"  {year} {st} {with_rec[0]['file']}: {len(with_rec)} contests, sum {fmtr(a, b)}, raw {fmtr(a_raw, b)}; leading candidates "
                + (f"{fmtr(a_l, b_l)} over {len(leads)}, {n_off_l} off >0.5%" if leads else "not matched")
                + f"; {n_off} contests off >0.5% (worst {worst['office']} {worst['district']}{' special' if worst['special'] else ''} {fmtr(worst['no_total'], worst['rec'])}"
                + (f", lead {worst['lead']} {fmtr(worst['a_lead'], worst['b_lead'])}" if worst["a_lead"] is not None and worst["b_lead"] else "")
                + f"); subtotal rows {total_rows:,}; {tag}" + (f" ({dict(on)})" if on else ""))
        if abs(off) > TOL or n_off or total_rows:
            print(line)
            if on and (abs(off) > TOL or n_off):
                flagged.append({"year": year, "state": st, "file": with_rec[0]["file"], "sum_off": off, "lead_off": off_l, "contests_off": n_off,
                                "leads_off": n_off_l, "worst": f"{worst['office']} {worst['district']} {fmtr(worst['no_total'], worst['rec'])}",
                                "p": dict(on)})
            summary["listed"] += 1
        else:
            summary["every contest within 0.5%"] += 1
        no_rec = [x for x in rows if x.get("no_record")]
        if no_rec:
            summary["contests without a record"] += len(no_rec)
    print(f"  summary: {dict(summary)}")
    missing = sorted(k for k in rests if k not in by_sy)
    print(f"  state-years whose p rest on a MEDSL file with no comparison here: {len(missing)}: " + ", ".join(f"{y} {s}" for y, s in missing))
    return flagged, missing, standing


def section_38_3(kl, mv, inv, standing):
    """Klarner against MEDSL by chamber and district"""
    print("38.3 Klarner's legislative returns against MEDSL's STATE SENATE and STATE HOUSE totals by district")
    rests = collections.defaultdict(lambda: collections.Counter())
    for (level, year, st, src, vs), n in inv.items():
        if src == "klarner" and level in ("state-upper", "state-lower"):
            rests[(year, st, level)][vs or "klarner"] += n
    m_by = collections.defaultdict(dict)   # (year, st, chamber) -> dkey -> {nt, raw, cands, codes}
    for (year, st, office, district), c in mv.items():
        if office not in ("STATE SENATE", "STATE HOUSE"):
            continue
        ch = "state-upper" if office == "STATE SENATE" else "state-lower"
        k = vt_key(district) if (st == "VT" and year != 2016 and re.match(r"^[A-Z]", district.upper())) else dkey(district)
        cell = m_by[(year, st, ch)].setdefault(k, {"nt": 0, "raw": 0, "cands": collections.Counter(), "codes": [], "d": 0, "r": 0, "party_known": False})
        cell["nt"] += sum(c["no_total"].values())
        cell["raw"] += sum(c["cands"].values())
        cell["cands"].update(c["no_total"])
        cell["codes"].append(district)
        for cand, v in c["no_total"].items():
            pty = (c.get("party") or {}).get(cand, "")
            if pty:
                cell["party_known"] = True
            if pty.startswith("DEM"):
                cell["d"] += v
            elif pty.startswith("REP"):
                cell["r"] += v
    k_by = collections.defaultdict(dict)
    for (year, st, ch, k), c in kl.items():
        k_by[(year, st, ch)][k] = c
    flagged = []
    details = []     # every matched district off by more than 5% (or at exactly 2x), for checks/m2/c38-districts.json
    summary = collections.Counter()
    twice = []
    print(f"  chamber-years in Klarner: {len(k_by)}; with a MEDSL file summarised: {sum(1 for k in k_by if k in m_by)}")
    print("  (matched = the district keys on both sides with votes on both; chamber = every district's votes on each side;"
          " file = the MEDSL file's statewide standing from 38.2)")
    for key in sorted(k_by):
        if key not in m_by:
            continue
        year, st, ch = key
        kd, md = k_by[key], m_by[key]
        matched = [k for k in kd if k in md and kd[k]["votes"] > 0 and md[k]["nt"] > 0]
        a = sum(kd[k]["votes"] for k in matched)
        b = sum(md[k]["nt"] for k in matched)
        off = pct(a, b)
        ka = sum(c["votes"] for c in kd.values())
        mb = sum(c["nt"] for c in md.values())
        mraw = sum(c["raw"] for c in md.values())
        per = [(k, kd[k]["votes"], md[k]["nt"], md[k]["raw"]) for k in matched]
        # the two parties alone (Klarner's dvote + rvote against MEDSL's Democratic and Republican lines), where
        # MEDSL names parties and the two lines carry at least 80% of the district's votes on both sides: write-ins
        # and minor lines, which Klarner's ovote may leave out, set aside; a file whose Democratic line is filed as
        # OTHER (Minnesota's DFL, North Dakota's Dem-NPL in 2022) falls back to every vote
        dr = [(k, kd[k]["d"] + kd[k]["r"], md[k]["d"] + md[k]["r"]) for k in matched
              if md[k]["party_known"] and md[k]["d"] + md[k]["r"] >= 0.8 * md[k]["nt"] and kd[k]["d"] + kd[k]["r"] >= 0.8 * kd[k]["votes"]]
        a_dr = sum(x for k, x, y in dr)
        b_dr = sum(y for k, x, y in dr)
        n_off_dr = sum(1 for k, x, y in dr if abs(pct(x, y)) > TOL)
        worst_dr = max(dr, key=lambda t: abs(pct(t[1], t[2]))) if dr else None
        n_off = sum(1 for k, x, y, z in per if abs(pct(x, y)) > TOL)
        # each district by its measure: the two parties where that holds, else every vote
        dr_k = {k: (x, y) for k, x, y in dr}
        chosen = [(k, dr_k[k][0], dr_k[k][1], "D+R") if k in dr_k else (k, x, y, "all") for k, x, y, z in per]
        n_big = sum(1 for k, x, y, m in chosen if abs(pct(x, y)) > 0.05)
        worst_c = max(chosen, key=lambda t: abs(pct(t[1], t[2]))) if chosen else None
        a_c = sum(x for k, x, y, m in chosen)
        b_c = sum(y for k, x, y, m in chosen)
        n_2x = sum(1 for k, x, y, z in per if x == 2 * y)
        n_half = sum(1 for k, x, y, z in per if 2 * x == y)
        n_half_raw = sum(1 for k, x, y, z in per if 2 * x == z)
        k_only = [k for k in kd if k not in md]
        m_only = [k for k in md if k not in kd]
        k_novotes = [k for k in kd if k in md and kd[k]["votes"] == 0]
        on = rests.get(key)
        worst = max(per, key=lambda t: abs(pct(t[1], t[2]))) if per else None
        fs = standing.get((year, st))
        file_note = (f"file {fs['off']:+.2%}" + (f" (leaders {fs['off_lead']:+.2%})" if fs.get("off_lead") is not None else "") + f" over {fs['contests']}") if fs else "file: no statewide contest to stand on"
        line = (f"  {year} {st} {ch}: {len(matched)} districts matched, Klarner {fmtr(a, b)} MEDSL; chamber {fmtr(ka, mb)}"
                + (f" (MEDSL raw {mraw:,})" if mraw != mb else "") + f"; {n_off} off >0.5%"
                + (f" (worst district {worst[0]}: {fmtr(worst[1], worst[2])})" if worst else "")
                + (f"; D+R alone {fmtr(a_dr, b_dr)} over {len(dr)}, {n_off_dr} off >0.5%" + (f" (worst {worst_dr[0]}: {fmtr(worst_dr[1], worst_dr[2])})" if worst_dr and n_off_dr else "") if dr else "; D+R: no parties in the file (or the two lines under 80% of the votes)")
                + (f"; by each district's measure {fmtr(a_c, b_c)}, {n_big} off >5%" + (f" (worst {worst_c[0]}: {fmtr(worst_c[1], worst_c[2])} by {worst_c[3]})" if worst_c and n_big else ""))
                + (f"; Klarner at exactly 2x MEDSL: {n_2x}" if n_2x else "") + (f"; MEDSL at exactly 2x Klarner: {n_half}" if n_half else "")
                + (f"; MEDSL raw at exactly 2x Klarner: {n_half_raw}" if n_half_raw and n_half_raw != n_half else "")
                + f"; only in Klarner {len(k_only)}" + (f" ({', '.join(k_only[:6])})" if k_only else "")
                + f", only in MEDSL {len(m_only)}" + (f" ({', '.join(m_only[:6])})" if m_only else "")
                + (f", no votes in Klarner {len(k_novotes)}" if k_novotes else "")
                + f"; {file_note}" + ("; p rests on " + ", ".join(f"{'Klarner' if k == 'klarner' else k + chr(39) + 's votes'} ({v} p)" for k, v in sorted(on.items())) if on else "; no p rests on Klarner here"))
        use_off = pct(a_c, b_c) if chosen else pct(ka, mb)
        n_off_c = sum(1 for k, x, y, m in chosen if abs(pct(x, y)) > TOL)
        for k, x, y, m in chosen:
            if abs(pct(x, y)) > 0.05 or x == 2 * y or 2 * x == y:
                details.append({"year": year, "state": st, "chamber": ch, "district": k, "klarner": x, "medsl": y, "by": m, "off": round(pct(x, y), 4),
                                "medsl_codes": md[k]["codes"], "klarner_rows": kd[k]["rows"], "klarner_code": kd[k].get("code"),
                                "p_rests_on": dict(on) if on else {}})
        if abs(use_off) > TOL or n_big or n_2x or n_half or n_half_raw or not matched:
            print(line)
            summary["listed"] += 1
            if on:
                flagged.append({"year": year, "state": st, "chamber": ch, "sum_off": use_off, "by": "each district's measure" if chosen else "chamber totals",
                                "matched": len(matched), "districts_off": n_off_c, "big": n_big,
                                "chamber_off": pct(ka, mb), "twice": n_2x, "half": n_half, "half_raw": n_half_raw,
                                "worst": f"{worst_c[0]}: {fmtr(worst_c[1], worst_c[2])} by {worst_c[3]}" if worst_c else "no district matched", "file": file_note, "p": dict(on)})
        else:
            summary["within 0.5% in aggregate, no district off >5%, no exact doubling"] += 1
        if n_2x or n_half or n_half_raw:
            twice.append((year, st, ch, n_2x, n_half, n_half_raw, len(matched)))
    print(f"  summary: {dict(summary)}")
    print("  chamber-years with a district at exactly 2x (Klarner 2x MEDSL / MEDSL 2x Klarner / MEDSL raw 2x Klarner, of matched): "
          + "; ".join(f"{y} {s} {c} {a}/{b}/{r} of {m}" for y, s, c, a, b, r, m in twice))
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "c38-districts.json")
    with open(out, "w") as f:
        json.dump({"what": "every state legislative district matched between Klarner's contest file and a MEDSL precinct file whose votes differ by"
                           " more than 5% (by the two parties' lines where both carry 80% of the district, else every vote) or stand at exactly"
                           " twice the other side; the seventh pass's c38_input_volume.py, section 38.3; evidence for D3's reconciliation, not data",
                   "districts": sorted(details, key=lambda d: (d["year"], d["state"], d["chamber"], str(d["district"])))}, f, indent=1)
    print(f"  {len(details)} districts off by more than 5% (or at exactly 2x) written to {os.path.relpath(out)}")
    return flagged


# ------------------------------------------------------------------------------------------ North Carolina
NC_GENERALS = ("2000-11-07", "2002-11-05", "2004-11-02", "2006-11-07", "2008-11-04", "2010-11-02", "2012-11-06", "2014-11-04",
               "2016-11-08", "2018-11-06", "2020-11-03", "2022-11-08", "2024-11-05")
_NC_HOUSE = re.compile(r"^US (HOUSE OF REP(RESENTATIVES|\.)|CONGRESS|HOUSE) ?\(?(DISTRICT )?0*(\d+)(ST|ND|RD|TH)?( DISTRICT)?\)?(.*)$")
_NC_SEN = re.compile(r"^NC (STATE )?SENATE ?\(?(DISTRICT )?0*(\d+)\)?$")
_NC_HSE = re.compile(r"^NC HOUSE( OF REPRESENTATIVES)? ?\(?(DISTRICT )?0*(\d+)\)?$")


def nc_office(name):
    """(office, district, special) of a State Board contest name, or None"""
    n = name.strip().upper()
    if "PRESIDENT" in n and "VICE" in n or n in ("PRESIDENT", "US PRESIDENT"):
        return ("PRESIDENT", "", False)
    if n == "US SENATE":
        return ("US SENATE", "", False)
    if n in ("GOVERNOR", "NC GOVERNOR"):
        return ("GOVERNOR", "", False)
    m = _NC_HOUSE.match(n)
    if m:
        return ("US HOUSE", f"{int(m.group(4)):02d}", "UNEXPIRED" in (m.group(7) or ""))
    m = _NC_SEN.match(n)
    if m:
        return ("STATE SENATE", str(int(m.group(3))), False)
    m = _NC_HSE.match(n)
    if m:
        return ("STATE HOUSE", str(int(m.group(3))), False)
    return None


def nc_path(date):
    n = f"results_pct_{date.replace('-', '')}.zip"
    for d in (os.path.join(M.FIFTH, "ncsbe"), os.path.join(SEVENTH, "ncsbe")):
        if os.path.exists(os.path.join(d, n)):
            return os.path.join(d, n)
    return None


def section_38_4(rec, kl, inv):
    print("38.4 North Carolina's State Board files (the p of data/local, measure and primary from ncsbe): each general election's"
          " President, US Senate, US House, Governor and legislative totals against D1, D2 and Klarner")
    rests = collections.defaultdict(lambda: collections.Counter())
    for (level, year, st, src, vs), n in inv.items():
        if st == "NC" and (src == "ncsbe" or vs == "ncsbe"):
            rests[year][level] += n
    flagged = []
    for date in NC_GENERALS:
        path = nc_path(date)
        year = int(date[:4])
        if not path:
            print(f"  {date}: file not in the cache")
            continue
        s = M.ncsbe_summary(path)
        rows = []
        for name, c in s["contests"].items():
            o = nc_office(name)
            if not o:
                continue
            office, district, special = o
            cands = {nkey(k): v for k, v in c["choices"].items()}
            total = sum(cands.values())
            if office in ("STATE SENATE", "STATE HOUSE"):
                ch = "state-upper" if office == "STATE SENATE" else "state-lower"
                k = kl.get((year, "NC", ch, district))
                if k and k["votes"] > 0:
                    rows.append({"office": office, "district": district, "a": total, "b": k["votes"], "off": pct(total, k["votes"]), "vs": "Klarner",
                                 "n_counties": c["n_counties"]})
                continue
            r = rec.get((office, year, "NC", district, special))
            if r is None:
                continue
            sn, a_lead, b_lead = lead_votes(cands, r)
            rows.append({"office": office, "district": district, "a": total, "b": r["total"], "off": pct(total, r["total"]), "vs": "D1" if office == "PRESIDENT" else "D2",
                         "lead": sn, "a_lead": a_lead, "b_lead": b_lead, "lead_off": pct(a_lead, b_lead) if a_lead is not None and b_lead else None,
                         "n_counties": c["n_counties"]})
        if not rows:
            print(f"  {date}: no contest to compare (the file names {len(s['contests'])} contests)")
            continue
        fed = [x for x in rows if x["vs"] != "Klarner"]
        leg = [x for x in rows if x["vs"] == "Klarner"]
        on = rests.get(year)
        parts = []
        if fed:
            a, b = sum(x["a"] for x in fed), sum(x["b"] for x in fed)
            leads = [x for x in fed if x["lead_off"] is not None]
            n_off = sum(1 for x in fed if abs(x["off"]) > TOL)
            n_off_l = sum(1 for x in leads if abs(x["lead_off"]) > TOL)
            worst = max(fed, key=lambda x: abs(x["off"]))
            parts.append(f"federal and statewide {len(fed)} contests vs D1/D2: {fmtr(a, b)}, {n_off} off >0.5% (worst {worst['office']} {worst['district']} {fmtr(worst['a'], worst['b'])}"
                         + (f", lead {worst['lead']} {fmtr(worst['a_lead'], worst['b_lead'])}" if worst.get("a_lead") is not None and worst.get("b_lead") else "") + ")"
                         + (f"; leaders {fmtr(sum(x['a_lead'] for x in leads), sum(x['b_lead'] for x in leads))} over {len(leads)}, {n_off_l} off" if leads else ""))
            if on and (abs(pct(a, b)) > TOL or n_off):
                flagged.append({"year": year, "state": "NC", "file": os.path.basename(path), "sum_off": pct(a, b), "contests_off": n_off, "leads_off": n_off_l if leads else None,
                                "worst": f"{worst['office']} {worst['district']} {fmtr(worst['a'], worst['b'])}", "vs": "D1/D2", "p": dict(on)})
        if leg:
            a, b = sum(x["a"] for x in leg), sum(x["b"] for x in leg)
            n_off = sum(1 for x in leg if abs(x["off"]) > TOL)
            worst = max(leg, key=lambda x: abs(x["off"]))
            parts.append(f"legislature {len(leg)} districts vs Klarner: {fmtr(a, b)}, {n_off} off >0.5% (worst {worst['office']} {worst['district']} {fmtr(worst['a'], worst['b'])})")
            if on and (abs(pct(a, b)) > TOL or n_off):
                flagged.append({"year": year, "state": "NC", "file": os.path.basename(path), "sum_off": pct(a, b), "contests_off": n_off,
                                "worst": f"{worst['office']} {worst['district']} {fmtr(worst['a'], worst['b'])}", "vs": "Klarner", "p": dict(on)})
        print(f"  {date} ({os.path.basename(path)}): " + "; ".join(parts) + ("; p rests on the Board's files this year (" + ", ".join(f"{k} {v}" for k, v in on.items()) + ")" if on else "; no p this year"))
    return flagged


# ------------------------------------------------------------------------------------------ Indiana
IN_CATS = {"1019": "PRESIDENT", "1006": "US SENATE", "1005": "US HOUSE", "1007": "GOVERNOR", "1018": "STATE SENATE", "1039": "STATE HOUSE"}
ORDINALS = {w: i + 1 for i, w in enumerate(("FIRST", "SECOND", "THIRD", "FOURTH", "FIFTH", "SIXTH", "SEVENTH", "EIGHTH", "NINTH", "TENTH"))}


def in_enr_races():
    """Indiana's 2024 certified results by office category (fetch_seventh_pass.sh): (office, district) -> {cands, total}"""
    def L_(x):
        return x if isinstance(x, list) else ([x] if x else [])
    out = {}
    for cat, office in IN_CATS.items():
        path = os.path.join(SEVENTH, "in_enr", f"OffCatC_{cat}_A.json")
        if not os.path.exists(path):
            continue
        d = L.load_json(path)
        root = d.get("Root", d)
        for r in L_((root.get("StatewideSummary") or {}).get("Race")):
            title = r.get("OFFICE_TITLE", "")
            district = ""
            if office == "US HOUSE":
                w = next((w for w in ORDINALS if w in title.upper()), None)
                district = f"{ORDINALS[w]:02d}" if w else title
            elif office in ("STATE SENATE", "STATE HOUSE"):
                m = re.search(r"District\s*0*(\d+)", title)
                district = m.group(1) if m else title
            cands = {}
            for c in L_((r.get("Candidates") or {}).get("Candidate")):
                cands[nkey(c.get("NAME_ON_BALLOT"))] = int(c.get("TOTAL") or 0)
            out[(office, district)] = {"cands": cands, "total": sum(cands.values()), "title": title}
    return out


def section_38_5(rec, mv, inv):
    print("38.5 Indiana's 2024 certified results (in_enr): the federal and state offices against D1 and D2, the legislatures against MEDSL's 2024 Indiana file")
    races = in_enr_races()
    if not races:
        print("  the files are not in the cache")
        return []
    on = collections.Counter()
    for (level, year, st, src, vs), n in inv.items():
        if st == "IN" and year == 2024 and src == "in_enr":
            on[level] += n
    flagged = []
    fed = []
    for (office, district), c in sorted(races.items()):
        if office in ("STATE SENATE", "STATE HOUSE"):
            continue
        r = rec.get((office, 2024, "IN", district, False))
        if r is None:
            fed.append(f"{office} {district}: no record")
            continue
        sn, a_lead, b_lead = lead_votes(c["cands"], r)
        off = pct(c["total"], r["total"])
        fed.append(f"{office} {district}: {fmtr(c['total'], r['total'])}" + (f", lead {sn} {fmtr(a_lead, b_lead)}" if a_lead is not None and b_lead else ""))
        if abs(off) > TOL:
            flagged.append({"year": 2024, "state": "IN", "file": "in_enr", "sum_off": off, "worst": f"{office} {district} {fmtr(c['total'], r['total'])}", "vs": "D1/D2", "p": dict(on)})
    print("  " + "; ".join(fed))
    for office, ch in (("STATE SENATE", "state-upper"), ("STATE HOUSE", "state-lower")):
        mine = {d: c for (o, d), c in races.items() if o == office}
        m_by = {}
        for (year, st, o, district), c in mv.items():
            if year == 2024 and st == "IN" and o == office:
                k = dkey(district)
                cell = m_by.setdefault(k, {"nt": 0})
                cell["nt"] += sum(c["no_total"].values())
        matched = [d for d in mine if dkey(d) in m_by and mine[d]["total"] > 0 and m_by[dkey(d)]["nt"] > 0]
        a = sum(mine[d]["total"] for d in matched)
        b = sum(m_by[dkey(d)]["nt"] for d in matched)
        per = [(d, mine[d]["total"], m_by[dkey(d)]["nt"]) for d in matched]
        n_off = sum(1 for d, x, y in per if abs(pct(x, y)) > TOL)
        worst = max(per, key=lambda t: abs(pct(t[1], t[2]))) if per else None
        print(f"  {office}: {len(mine)} districts in the state's files, {len(matched)} matched in MEDSL's: state {fmtr(a, b)} MEDSL, {n_off} off >0.5%"
              + (f" (worst district {worst[0]}: {fmtr(worst[1], worst[2])})" if worst else "") + ("" if m_by else "; MEDSL's 2024 Indiana file not summarised"))
    print(f"  p resting on the state's files: {dict(on)}; MEDSL's Indiana file stands at the figures of 38.2 (held back by D3, report section 6)")
    return flagged


# ------------------------------------------------------------------------------------------ Louisiana
def section_38_6(rec, inv):
    print("38.6 Louisiana's workbooks (la_sos): 2024-11-05's presidency and six House seats against D1 and D2 (c18's gate, from my own parse); 2023's governor")
    import c18_louisiana as C18
    on = collections.Counter()
    for (level, year, st, src, vs), n in inv.items():
        if st == "LA" and src == "la_sos":
            on[(year, level)] += n
    flagged = []
    path = os.path.join(C18.ROOT, "20241105.xlsx")
    if not os.path.exists(path):
        print("  2024-11-05: workbook not in the cache")
        return flagged
    cs, bad = C18.parse(path, "2024-11-05")
    parts = []
    for c in cs:
        if not C18.FEDERAL.match(c["title"]) or not c["multi"]:
            continue
        cands = {nkey(x["name"]): x["votes"] for x in c["cands"]}
        if c["title"].startswith("Presidential Electors"):
            r = rec.get(("PRESIDENT", 2024, "LA", "", False))
            office, district = "PRESIDENT", ""
        else:
            m = re.search(r"(\d+)(st|nd|rd|th) Congressional", c["title"])
            district = f"{int(m.group(1)):02d}" if m else ""
            r = rec.get(("US HOUSE", 2024, "LA", district, False))
            office = "US HOUSE"
        if r is None:
            continue
        total = sum(cands.values())
        sn, a_lead, b_lead = lead_votes(cands, r)
        off = pct(total, r["total"])
        parts.append(f"{office} {district}: {fmtr(total, r['total'])}" + (f", lead {sn} {fmtr(a_lead, b_lead)}" if a_lead is not None and b_lead else ""))
        if abs(off) > TOL:
            flagged.append({"year": 2024, "state": "LA", "file": "20241105.xlsx", "sum_off": off, "worst": f"{office} {district} {fmtr(total, r['total'])}", "vs": "D1/D2",
                            "p": {k[1]: v for k, v in on.items() if k[0] == 2024}})
    print("  2024-11-05: " + "; ".join(parts) + f"; p resting on the 2024 workbooks: {dict((k[1], v) for k, v in on.items() if k[0] == 2024)}")
    path = os.path.join(C18.ROOT, "20231014.xlsx")
    if os.path.exists(path):
        cs, bad = C18.parse(path, "2023-10-14")
        g = [c for c in cs if c["title"] == "Governor" and c["multi"]]
        r = rec.get(("GOVERNOR", 2023, "LA", "", False))
        if g and r:
            total = sum(x["votes"] for x in g[0]["cands"])
            print(f"  2023-10-14 Governor: the workbook {fmtr(total, r['total'])} D2's record, which is from the same Secretary of State's results (not a second count);"
                  f" p resting on the 2023 workbooks: {dict((k[1], v) for k, v in on.items() if k[0] == 2023)}: no second count exists in the sources read")
    return flagged


# ------------------------------------------------------------------------------------------ D1 and D2 against MEDSL's state files
def section_38_7(rec, ms, mv, inv):
    print("38.7 D1's and D2's records against MEDSL's state-level files (U.S. President 1976-2024; U.S. Senate 1976-2024 from the first pass's cache;"
          " U.S. House 1976-2024 sits behind a Dataverse guestbook, not taken: law 10) and against the precinct files of 38.2")
    rests = {}
    for (level, year, st, src, vs), n in inv.items():
        if level in ("president", "senate", "house", "governor"):
            rests[(level, year, st)] = (n, src)
    flagged = []
    summary = collections.Counter()
    for office, level in (("PRESIDENT", "president"), ("US SENATE", "senate")):
        n_cmp = 0
        offs = []
        for (o, year, st, district, special), r in sorted(rec.items()):
            if o != office or district:
                continue
            f = ms.get((office, year, st, "", special))
            if f is None:
                summary[f"{office}: no row in MEDSL's file"] += 1
                continue
            n_cmp += 1
            a_total = sum(f["cands"].values())
            off = pct(a_total, r["total"])
            sn, a_lead, b_lead = lead_votes(f["cands"], r)
            lead_off = pct(a_lead, b_lead) if a_lead is not None and b_lead else None
            same = "MIT Election Data" in r["source"]
            on = rests.get((level, year, st))
            if abs(off) > TOL or (lead_off is not None and abs(lead_off) > TOL):
                offs.append(f"{year} {st}{' special' if special else ''}: file {fmtr(a_total, r['total'])}" + (f", lead {sn} {fmtr(a_lead, b_lead)}" if lead_off is not None else "")
                            + (" [D1's source is this file]" if same else "") + (f" [p {on[0]}]" if on else ""))
                if on and (lead_off is None or abs(lead_off) > TOL):
                    flagged.append({"year": year, "state": st, "file": f"MEDSL {office} state file", "sum_off": off, "lead_off": lead_off,
                                    "worst": f"{office} {fmtr(a_total, r['total'])}", "vs": level, "p": {level: on[0]}, "same_source": same})
                summary[f"{office}: off"] += 1
            else:
                summary[f"{office}: within 0.5% (totals and leaders)"] += 1
        print(f"  {office}: {n_cmp} records compared")
        for x in offs:
            print("    " + x)
    # governors and the House: the precinct files (38.2's comparison, read from the record's side)
    fc = file_contests(mv)
    for office, level in (("GOVERNOR", "governor"), ("US HOUSE", "house")):
        n_cmp = 0
        offs = []
        for (o, year, st, district, special), r in sorted(rec.items()):
            if o != office:
                continue
            f = fc.get((year, st, office, district, special))
            if f is None:
                continue
            n_cmp += 1
            off = pct(f["nt"], r["total"])
            sn, a_lead, b_lead = lead_votes(f["cands"], r)
            lead_off = pct(a_lead, b_lead) if a_lead is not None and b_lead else None
            on = rests.get((level, year, st))
            if lead_off is not None and abs(lead_off) > TOL or (lead_off is None and abs(off) > TOL):
                offs.append(f"{year} {st} {district}{' special' if special else ''}: file {fmtr(f['nt'], r['total'])}" + (f", lead {sn} {fmtr(a_lead, b_lead)}" if lead_off is not None else "")
                            + (f" [p {on[0]}]" if on else ""))
                summary[f"{office}: leaders off (or totals, where no leader matched)"] += 1
            elif abs(off) > TOL:
                summary[f"{office}: totals off, leaders within 0.5%"] += 1
                if office == "GOVERNOR" and f["nt"] > r["total"] * (1 + TOL):
                    offs.append(f"{year} {st}: file {fmtr(f['nt'], r['total'])}, lead {sn} {fmtr(a_lead, b_lead)}: the record's total is short of the file's with the leader equal"
                                + (f" [p {on[0]}]" if on else ""))
            else:
                summary[f"{office}: within 0.5%"] += 1
        print(f"  {office}: {n_cmp} records compared with a precinct file")
        for x in offs:
            print("    " + x)
    print(f"  summary: {dict(summary)}")
    return flagged


# ------------------------------------------------------------------------------------------ no second count; the coarse tier
def section_38_8(inv, kl, rec, mv, standing):
    print("38.8 The state-years with p and no second count in any source read, and the coarse tier for Klarner's")
    have_file = {(y, s) for (y, s, o, d) in mv}
    none = collections.defaultdict(lambda: collections.Counter())
    for (level, year, st, src, vs), n in inv.items():
        if src == "medsl" and (year, st) not in standing:
            none[("MEDSL file without a federal or statewide contest to compare" if (year, st) in have_file else "MEDSL file not summarised", year)][st] += n
        elif src == "ncsbe" and level in ("local", "measure", "primary"):
            pass   # 38.4: the general elections; the odd years and primaries below
        elif src in ("nj_sos", "va_elect"):
            none[("the state's own list, nothing else holds that day", year)][st] += n
        elif src == "la_sos" and year == 2023:
            none[("the state's own workbooks, D2's governor from the same", year)][st] += n
    nc_years = collections.Counter()
    for (level, year, st, src, vs), n in inv.items():
        if src == "ncsbe" and level == "primary":
            nc_years[("NC primaries", year)] += n
        elif src == "ncsbe" and year % 2 == 1:
            nc_years[("NC odd-year municipal elections", year)] += n
    for k, v in sorted(none.items()):
        print(f"  {k[0]}, {k[1]}: {sum(v.values()):,} p in {len(v)} states (" + ", ".join(f"{s} {n}" for s, n in sorted(v.items())) + ")")
    for k, v in sorted(nc_years.items()):
        print(f"  {k[0]}, {k[1]}: {v:,} p (the Board's file of that date holds no contest D1, D2 or Klarner count)")
    # Klarner: each chamber-year's votes per contested district against the day's statewide reference, read against
    # the same chamber's other years of the decade. Reason: a chamber's votes per district relative to the state's
    # turnout is a steady figure (its seats per district and its contested share change slowly; the day's statewide
    # count carries the turnout), so a doubled year stands out as about 2x the chamber's own median, where the ratio
    # to the reference alone does not (New Hampshire's 400-seat House runs at 4-5x the governor's total every year).
    # A half-Senate year keeps its votes per contested district, so the staggering does not show.
    print("  Klarner's chamber-years without a MEDSL file: the chamber's votes over what its contested seats would draw from the day's statewide reference (D2's House total"
          " 2006 on, else D1's presidential total, else D2's governor that year), against the same chamber's median over its other"
          " years with the same number of districts (within 10%), else the decade's; flagged over 1.5x or under 0.5x the median, or a lone year")
    k_by = collections.defaultdict(lambda: collections.Counter())
    for (year, st, ch, k), c in kl.items():
        k_by[(year, st, ch)]["votes"] += c["votes"]
        k_by[(year, st, ch)]["districts"] += 1
        k_by[(year, st, ch)]["seats_all"] += c["seats"]
        if c["votes"] > 0:
            k_by[(year, st, ch)]["contested"] += 1
            k_by[(year, st, ch)]["seats_contested"] += c["seats"]
            k_by[(year, st, ch)]["seats_sq"] += c["seats_sq"]
    rests = set()
    for (level, year, st, src, vs), n in inv.items():
        if src == "klarner" and level in ("state-upper", "state-lower"):
            rests.add((year, st, level))
    house = collections.Counter()
    for (o, year, st, district, special), r in rec.items():
        if o == "US HOUSE" and not special:
            house[(year, st)] += r["total"]
    norm = {}      # (year, st, ch) -> (votes per contested district / reference, how, ref)
    n_ref = collections.Counter()
    for key in sorted(k_by):
        year, st, ch = key
        ref = None
        if house.get((year, st)):
            ref, how = house[(year, st)], "House"
        elif ("PRESIDENT", year, st, "", False) in rec:
            ref, how = rec[("PRESIDENT", year, st, "", False)]["total"], "President"
        elif ("GOVERNOR", year, st, "", False) in rec:
            ref, how = rec[("GOVERNOR", year, st, "", False)]["total"], "Governor"
        if not ref or not k_by[key]["contested"]:
            continue
        # the expected votes of a chamber whose contested seats are k_1..k_m (eseats, one per contest row): a voter in a
        # k-seat district casts up to k votes, and a k-seat district holds about k/N of the state's voters, so the
        # chamber's votes come to about T * sum(k^2) / N for the day's statewide count T and N the chamber's seats (the
        # most any year within ten years elected, uncontested ones in); the ratio votes * N / (T * sum(k^2)) is 1 for
        # a full single-member chamber, 1 for a half-Senate year, and holds steady through a chamber's multi-member
        # years and its single-member ones alike (Idaho's 1984-1990 districts of up to six representatives, North
        # Carolina's, South Carolina's and West Virginia's before their reforms)
        n_full = max(k_by[o]["seats_all"] for o in k_by if o[1] == st and o[2] == ch and abs(o[0] - year) <= 10) or 1
        sq = max(k_by[key]["seats_sq"], 1)
        norm[key] = (k_by[key]["votes"] * n_full / (ref * sq), how, ref)
    flagged = []
    judged = collections.Counter()
    for key in sorted(k_by):
        year, st, ch = key
        if key not in rests or (year, st) in standing:
            continue
        if key not in norm:
            judged["no reference that day"] += 1
            continue
        # peers: the chamber's other years with the same number of districts (within 10%: the same structure, since
        # multi-member chambers that went single-member, North Carolina's or West Virginia's, changed their per-district
        # votes for good), else the decade's other years, else every other year
        d0 = k_by[key]["districts"]
        others = [(y, s2, c2) for (y, s2, c2) in norm if s2 == st and c2 == ch and (y, s2, c2) != key]
        peers = [norm[o][0] for o in others if abs(k_by[o]["districts"] - d0) <= 0.1 * d0]
        if len(peers) < 2:
            decade = (year - 2) // 10
            peers = [norm[o][0] for o in others if (o[0] - 2) // 10 == decade]
        if len(peers) < 2:
            peers = [norm[o][0] for o in others]
        if not peers:
            judged["a lone year for its chamber"] += 1
            flagged.append({"year": year, "state": st, "chamber": ch, "ratio": None, "how": norm[key][1], "votes": k_by[key]["votes"], "ref": norm[key][2],
                            "contested": k_by[key]["contested"], "seats": k_by[key]["seats_contested"], "peers": 0})
            continue
        med = sorted(peers)[len(peers) // 2]
        ratio = norm[key][0] / med
        judged["judged"] += 1
        if ratio > 1.5 or ratio < 0.5:
            flagged.append({"year": year, "state": st, "chamber": ch, "ratio": ratio, "how": norm[key][1], "votes": k_by[key]["votes"], "ref": norm[key][2],
                            "contested": k_by[key]["contested"], "seats": k_by[key]["seats_contested"], "peers": len(peers)})
    print(f"  chamber-years with p and no MEDSL file: {dict(judged)}; flagged {len(flagged)}")
    for f in sorted(flagged, key=lambda f: -(f["ratio"] or 0)):
        print(f"    {f['year']} {f['state']} {f['chamber']}: {f['votes']:,} over {f['contested']} contested districts ({f['seats']} seats), the day's {f['how']} {f['ref']:,}; "
              + (f"{f['ratio']:.2f}x the chamber's median over {f['peers']} other years" if f["ratio"] is not None else "no other year of this chamber to read it against"))
    return flagged


if __name__ == "__main__":
    print(f"C38 input volume; {L.git_head()}")
    inv, inv_files = every_p()
    print("38.1 The inventory: every computed p by level, source and state-year")
    by = collections.defaultdict(lambda: collections.Counter())
    for (level, year, st, src, vs), n in inv.items():
        by[(level, src[:40], vs)]["p"] += n
        by[(level, src[:40], vs)]["state-years"] += 1
    for k, v in sorted(by.items()):
        print(f"  {k[0]:12s} {k[1]:42s} {('votes ' + k[2]) if k[2] else '':14s} {v['p']:>8,} p in {v['state-years']:>5,} state-years")
    rec = d12()
    kl = klarner()
    mv, mf = medsl_volumes()
    ms = medsl_state_files()
    f2, miss2, standing = section_38_2(mv, mf, rec, inv)
    f3 = section_38_3(kl, mv, inv, standing)
    f4 = section_38_4(rec, kl, inv)
    f5 = section_38_5(rec, mv, inv)
    f6 = section_38_6(rec, inv)
    f7 = section_38_7(rec, ms, mv, inv)
    f8 = section_38_8(inv, kl, rec, mv, standing)
    print("38.9 The list: every state-year with p off by more than 0.5% on a direct comparison (the side the p rests on first)")
    print("  MEDSL precinct files (38.2), by the file's totals; the leaders' column tells a total's convention (blank and write-in lines) from a short or doubled file:")
    for f in sorted(f2, key=lambda f: (f["year"], f["state"])):
        print(f"    {f['year']} {f['state']} {f['file']}: totals {f['sum_off']:+.2%}, leaders " + (f"{f['lead_off']:+.2%}" if f.get("lead_off") is not None else "not matched")
              + f", {f['contests_off']} contests off (leaders off {f.get('leads_off')}); worst {f['worst']}; p {f['p']}")
    print(f"  Klarner against MEDSL (38.3), each district by the two parties' votes where the file names them (else every vote): {len(f3)} chamber-years"
          " off by more than 0.5% in aggregate, or with a district off by more than 5%, or with a district at exactly twice the other side")
    for f in sorted(f3, key=lambda f: (f["year"], f["state"], f["chamber"])):
        print(f"    {f['year']} {f['state']} {f['chamber']}: {f['sum_off']:+.2%} by {f['by']} over {f['matched']} districts, {f['districts_off']} off >0.5%, {f.get('big', 0)} off >5%; worst {f['worst']}"
              + (f"; Klarner 2x: {f['twice']}" if f["twice"] else "") + (f"; MEDSL 2x: {f['half']}" if f["half"] else "") + (f"; MEDSL raw 2x: {f['half_raw']}" if f["half_raw"] else "")
              + f"; {f['file']}; p {f['p']}")
    for name, fl in (("North Carolina (38.4)", f4), ("Indiana (38.5)", f5), ("Louisiana (38.6)", f6), ("D1 and D2 against MEDSL's state files (38.7)", f7)):
        print(f"  {name}: {len(fl)}")
        for f in fl:
            print(f"    {f['year']} {f['state']} {f['file']}: {f['sum_off']:+.2%} vs {f['vs']}; worst {f['worst']}; p {f['p']}")
    print(f"  Klarner's coarse tier (38.8): {len(f8)} chamber-years whose votes, over what their seats would draw from the day's statewide count, stand over 1.5x or under 0.5x"
          " the chamber's own median for the decade (or stand alone)")
    for f in sorted(f8, key=lambda f: (f["year"], f["state"])):
        print(f"    {f['year']} {f['state']} {f['chamber']}: " + (f"{f['ratio']:.2f}x the chamber's median ({f['how']} as the reference)" if f["ratio"] is not None else "a lone year"))
    # one line per state-year, for the comparison with D3's list
    sy = collections.defaultdict(list)
    for f in f2:
        sy[(f["year"], f["state"])].append(f"MEDSL file vs D1/D2 totals {f['sum_off']:+.1%}" + (f", leaders {f['lead_off']:+.1%}" if f.get("lead_off") is not None else "")
                                           + f", {f['contests_off']} contests off, worst {f['worst']} (p {f['p']})")
    for f in f3:
        sy[(f["year"], f["state"])].append(f"Klarner vs MEDSL {f['chamber']} {f['sum_off']:+.1%}, {f.get('big', 0)} districts off >5%"
                                           + (f", Klarner 2x in {f['twice']}" if f["twice"] else "") + (f", MEDSL 2x in {f['half']}" if f["half"] else "")
                                           + (f", MEDSL raw 2x in {f['half_raw']}" if f["half_raw"] else "") + f", worst {f['worst']} (p {f['p']})")
    for name, fl in (("NC Board file", f4), ("Indiana's files", f5), ("Louisiana's workbooks", f6), ("D1/D2 vs MEDSL state file", f7)):
        for f in fl:
            sy[(f["year"], f["state"])].append(f"{name} {f['sum_off']:+.1%} vs {f['vs']}, worst {f['worst']} (p {f['p']})")
    for f in f8:
        sy[(f["year"], f["state"])].append(f"Klarner {f['chamber']} coarse: " + (f"{f['ratio']:.2f}x the chamber's median" if f["ratio"] is not None else "a lone year"))
    print(f"  The state-years, one line each: {len(sy)}")
    for (year, st), reasons in sorted(sy.items()):
        print(f"    {year} {st}: " + " | ".join(reasons))
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "c38-state-years.json")
    with open(out, "w") as f:
        json.dump({"what": "every state-year with p that c38 lists (38.2-38.8), with each comparison's words; for c39's comparison with D3's check-volume.json",
                   "state_years": [{"year": y, "state": st, "reasons": r} for (y, st), r in sorted(sy.items())]}, f, indent=1)
    print(f"  written to {os.path.relpath(out)}")
