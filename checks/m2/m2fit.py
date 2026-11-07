"""checks/m2/m2fit.py: M2's own rebuild of D2's fit rows, fits, calibrations and tests (data/congress/REPORT.md
sections 2.2-2.7), written from the report's words for the second pass (briefs/M2-check-computed-p.md, the
amendment of 07:44). Nothing is imported from pipeline/. Used by c9_fit2.py (the fits, k, lambda, F against the
files), c10_backtest2.py (D2's back-tests and adoption decisions) and c11_k_reading.py (the spread factor).

Sources, fetched outside the repository (m2lib.CACHE) and checked by sha256:
  Cha, Kuriwaki and Snyder, Candidates in American General Elections v4.1 (Harvard Dataverse DGDRDT, CC0):
      the rows of 2006-2024 at every level, and the governors' last race from 2006;
  MEDSL, U.S. Senate statewide 1976-2024 v8 (Dataverse PEJ5QU, CC0): the Senate rows of 1982-2004;
  the presidential two-party shares by state come from D1's committed data/president/inputs/medsl_president.json
      (MEDSL's U.S. President file), summed as D2 sums them (party_simplified DEMOCRAT and REPUBLICAN lines);
  the governors of 1978-2004 come from the files data/governor/<year>.json themselves (Algara and Amlani's county
      sums, which this check does not refetch), with the last race the file records.
"""
import csv
import json
import math
import os
import re
import sys
import unicodedata

import numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402

CHA = ("https://dataverse.harvard.edu/api/access/datafile/13461690?format=original", "cha_candidates_2006-2024.dta",
       "64580af7dbe9b4ca12bd908bab5f98ef723374280794eb5e3617038fd758f4b4")
MEDSL = ("https://dataverse.harvard.edu/api/access/datafile/13887039?format=original", "medsl_1976-2024-senate-state.csv",
         "6f745db1b4a0026ad837e74428f9ed6f3f77fa51eb6f858b58ebdbc186fdb3bd")
DOWNBALLOT = {  # the lines sheets for the three House rows (2008 MA-05, NC-04; 2022 IL-03) whose lean the files lack
    2008: ("https://docs.google.com/spreadsheets/d/1l7W130tPRF6dQ4JoqlQJSJexnEg4rZct-7kwDXqgoLE/export?format=csv&gid=429358610",
           "downballot_sheet_2006.csv", "cabd4860a9e7d8ace7d0991b8460af535b8870ca1ab3e08ce17b532a758acb95", 5, 2004),
    2018: ("https://docs.google.com/spreadsheets/d/1zLNAuRqPauss00HDz4XbTH2HqsCzMe0pR8QmD1K8jk8/export?format=csv",
           "downballot_sheet_2018.csv", "1ac29ca1575210f62470732cacd2b8d0203b6219ef5223bf12ae309f54f7a23e", 3, 2016),
    2022: ("https://docs.google.com/spreadsheets/d/1CKngqOp8fzU22JOlypoxNsxL6KSAH920Whc-rd7ebuM/export?format=csv",
           "downballot_sheet_2022.csv", "40a174a694dc147cdb3fc423b09f4293b3ed191a0053dcd6f5b9a1d3f80f52a2", 3, 2020)}
# A House special held for the old seat: the files give it the district presidential vote on the lines of t-2 (the
# lines it was held on); D2's fit rows (chambers.py, fit_rows) give it the sheet of its own year t. "own" reproduces
# D2's fits; "t-2" is the files' reading. Each special row carries both (lean_own, lean_t2).
SPECIAL_LINES = "t-2"
STATES_50 = ("AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND "
             "OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY").split()
LEVELS = ("house", "senate", "governor")
FIT_FROM = {"house": 2006, "senate": 1982, "governor": 1978}
K_MIN, CAL_MIN = 4, 3
# the sitting president's party on election day of each even year (National Archives, as every file's
# forecast_inputs.president_party records it; checked against those fields in c9)
SITTING = {1978: "D", 1980: "D", 1982: "R", 1984: "R", 1986: "R", 1988: "R", 1990: "R", 1992: "R", 1994: "D", 1996: "D",
           1998: "D", 2000: "D", 2002: "R", 2004: "R", 2006: "R", 2008: "R", 2010: "D", 2012: "D", 2014: "D", 2016: "D",
           2018: "R", 2020: "R", 2022: "D", 2024: "D"}
NEAR_W, NEAR_MIN_EXPECTED, NEAR_BANDS, NEAR_WINDOWS = 0.01, 30, (0.0, 0.05, 0.10), (0.01, 0.02, 0.05)
VARIANTS = {"none": (False, "normal"), "shrink": (True, "normal"), "t4": (False, "t4"), "both": (True, "t4")}
# a third element names how k is fitted (c11, item 3): "all" = D2's, the RMS of z over every earlier scored year;
# "lastN" = over the last N scored years; "trend" = a line through the years' RMS z, read at the forecast year
K_MODES = ("all", "last1", "last2", "last3", "trend")
for _v, _t in list(VARIANTS.items()):
    for _k in K_MODES[1:]:
        VARIANTS[f"{_v}|{_k}"] = (_t[0], _t[1], _k)
VARIANT_YEARS = list(range(2010, 2025, 2))
VARIANT_BANDS, VARIANT_SAFE, VARIANT_MIN_COUNT, TAIL_LEVELS = (0.0, 0.05, 0.10, 0.20), (2, 3), 5, (0.05, 0.01)
SQRT2 = math.sqrt(2.0)
ROWS_CACHE = os.path.join(L.CACHE, "m2_fit_rows.json")


def P_of(t):
    return 1 if SITTING[t] == "D" else -1


def M_of(t):
    return 0 if t % 4 == 0 else 1


def last_pres_year(t):
    return t - 4 if t % 4 == 0 else t - 2


# ------------------------------------------------------------------------------------------------ inputs
def pres_shares():
    """{year: {state: the Democrat's two-party share, "US": the national one}} as D2 sums MEDSL's file: the votes
    on lines whose simplified party is DEMOCRAT or REPUBLICAN (a fusion line of another party is left out)."""
    d = L.load_json(os.path.join(L.DATA, "president", "inputs", "medsl_president.json"))
    out = {}
    for y, states in d["years"].items():
        D = R = 0
        for st, s in states.items():
            dv = rv = 0
            for c in s["candidates"]:
                if "lines" in c:
                    for ln in c["lines"]:
                        if ln["party_detailed"] in ("DEMOCRAT", "DEMOCRATIC-FARMER-LABOR", "DEMOCRATIC-NPL", "DEMOCRATIC-NONPARTISAN LEAGUE"):
                            dv += ln["votes"]
                        elif ln["party_detailed"] == "REPUBLICAN":
                            rv += ln["votes"]
                elif c["parties"] == ["DEMOCRAT"]:
                    dv += c["votes"]
                elif c["parties"] == ["REPUBLICAN"]:
                    rv += c["votes"]
            D += dv
            R += rv
            if dv + rv:
                out.setdefault(int(y), {})[st] = dv / (dv + rv)
        out[int(y)]["US"] = D / (D + R)
    return out


_DB = {}


def downballot_lean(year, state, district, ps):
    """The Downballot's two-party Democratic share on the lines of a House year, less the national share, read from
    the lines sheet (whole percent on the 2006-2010 lines, one decimal on the 2022 lines), for a regular election
    whose lean the file does not carry. The sheet's reading is checked against every file lean of the year in c9."""
    if year not in DOWNBALLOT:
        return None
    if year not in _DB:
        url, name, sha, col, py = DOWNBALLOT[year]
        path, _ = L.fetch(url, name, sha)
        rows = list(csv.reader(open(path, encoding="utf-8", newline="")))
        hdr = next(i for i, r in enumerate(rows) if r and r[0].strip() in ("District", "CD"))
        out = {}
        for r in rows[hdr + 1:]:
            if not r or not re.match(r"^[A-Z]{2}-(AL|\d{2})$", r[0].strip()):
                continue
            try:
                D, R = float(r[col].replace(",", "")), float(r[col + 1].replace(",", ""))
            except ValueError:
                continue
            out[r[0].strip()] = D / (D + R)
        _DB[year] = (out, py)
    out, py = _DB[year]
    key = f"{state}-{district}"
    if key not in out and district == "01":
        key = f"{state}-AL"
    return out[key] - ps[py]["US"] if key in out else None


def last_name(name):
    """A candidate's last name as D2 matches it: the part before a comma, else the last token; accents dropped;
    jr/sr/ii/iii/iv dropped; a quoted or bracketed nickname dropped."""
    if "Ã" in name:
        try:
            name = name.encode("latin-1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass
    name = "".join(ch for ch in unicodedata.normalize("NFKD", name) if not unicodedata.combining(ch))
    if "," in name:
        name = name.split(",")[0]
    toks = [t for t in re.split(r"[\s.]+", name.lower()) if t and t not in ("jr", "sr", "ii", "iii", "iv")]
    toks = [t.strip('"()') for t in toks if not (t.startswith('"') or t.startswith("("))] or toks
    return toks[-1] if toks else ""


def top_two_DR(cands):
    D = [a for a in cands if a["party"] == "D" and a["votes"]]
    R = [a for a in cands if a["party"] == "R" and a["votes"]]
    if len(D) != 1 or len(R) != 1:
        return None
    top2 = sorted([a for a in cands if a["votes"]], key=lambda a: -a["votes"])[:2]
    if {a["party"] for a in top2} != {"D", "R"}:
        return None
    return D[0], R[0]


def cha_contests():
    import pandas as pd
    path, _ = L.fetch(CHA[0], CHA[1], CHA[2])
    df = pd.read_stata(path, convert_categoricals=False)
    contests = {}
    nz = lambda x: None if x is None or (isinstance(x, float) and math.isnan(x)) else x  # noqa: E731
    for r in df.itertuples(index=False):
        dist = nz(r.dist)
        k = (int(r.year), r.office, r.state, dist, r.type)
        c = contests.setdefault(k, {"year": int(r.year), "office": {"H": "house", "S": "senate", "G": "governor", "P": "president"}[r.office],
                                    "state": r.state, "district": f"{int(dist):02d}" if r.office == "H" and dist is not None else None,
                                    "special": r.type == "S", "runoff": False, "candidates": []})
        c["runoff"] = c["runoff"] or nz(r.runoff) == 1
        v = nz(r.candidatevotes)
        c["candidates"].append({"name": r.name_snyder, "party": r.party, "inc": int(r.inc) if nz(r.inc) is not None else None,
                                "votes": int(v) if v is not None else None})
    return list(contests.values())


def file_inputs():
    """{(level, year, state, district, special): (forecast_inputs, two_party, id)} from data/<level>/<year>.json."""
    out = {}
    for level in LEVELS:
        for path in sorted(os.listdir(os.path.join(L.DATA, level))):
            doc = L.load_json(os.path.join(L.DATA, level, path))
            for c in doc["contests"]:
                out[(level, doc["year"], c["place"]["state"], c["place"].get("district"), bool(c.get("special")))] = \
                    (c.get("forecast_inputs") or {}, c.get("two_party"), c["id"], c)
    return out


def last_governor_index(cha, finputs):
    """{state: [(year, share, special, source)]}: every governor race a Democrat and a Republican led: Cha from 2006
    (odd years and specials included, runoffs excluded); before 2006 the files' recorded last races (Algara and
    Amlani's), since this check does not refetch the county file."""
    out = {}
    for c in cha:
        if c["office"] != "governor" or c["runoff"]:
            continue
        dr = top_two_DR(c["candidates"])
        if dr:
            out.setdefault(c["state"], []).append((c["year"], dr[0]["votes"] / (dr[0]["votes"] + dr[1]["votes"]), c["special"], "cha"))
    seen = set()
    for (level, y, st, d, sp), (fi, tp, cid, c) in finputs.items():
        if level != "governor":
            continue
        lg = fi.get("last_governor_race")
        if lg and lg["year"] < 2006 and (st, lg["year"], lg.get("special")) not in seen:
            seen.add((st, lg["year"], lg.get("special")))
            out.setdefault(st, []).append((lg["year"], lg["share_D"], bool(lg.get("special")), "file:" + lg["source"]))
    return out


def last_governor_race(index, state, year):
    past = [x for x in index.get(state, []) if x[0] < year]
    return max(past, key=lambda x: x[0]) if past else None


def cha_rows(cha, ps, finputs, gov):
    rows, skipped = [], {}

    def skip(w):
        skipped[w] = skipped.get(w, 0) + 1
    for c in cha:
        t, Lv = c["year"], c["office"]
        if Lv not in LEVELS or t % 2 or t < 2006:
            continue
        if c["runoff"]:
            skip("runoff")
            continue
        dr = top_two_DR(c["candidates"])
        if not dr:
            skip("not one D and one R leading")
            continue
        D, R = dr
        py = last_pres_year(t)
        lean_own = None
        if Lv == "house":
            key = None
            for d_ in (c["district"], "AL" if c["district"] == "01" else None):
                if d_ and (Lv, t, c["state"], d_, c["special"]) in finputs:
                    key = (Lv, t, c["state"], d_, c["special"])
                    break
            fi = finputs[key][0] if key else {}
            lean = fi.get("lean")
            src = "cha"
            if lean is None and not c["special"]:
                lean = downballot_lean(t, c["state"], c["district"], ps)
                src = "cha+downballot"
            if lean is None:
                skip("no district presidential vote from before the election (file inputs)")
                continue
            lean_own = None
            if c["special"] and Lv == "house":
                reg = finputs.get((Lv, t, c["state"], c["district"], False))
                lean_own = reg[0].get("lean") if reg else None
                if lean_own is None:
                    lean_own = downballot_lean(t, c["state"], c["district"], ps)
        else:
            if c["state"] not in ps.get(py, {}):
                skip("no state presidential vote")
                continue
            lean = ps[py][c["state"]] - ps[py]["US"]
            key = (Lv, t, c["state"], None, c["special"])
            fi = finputs.get(key, ({},))[0]
        inc = (1 if D["inc"] == 1 else 0) - (1 if R["inc"] == 1 else 0)
        n2 = D["votes"] + R["votes"]
        row = {"year": t, "level": Lv, "state": c["state"], "district": c["district"], "special": c["special"],
               "y": D["votes"] / n2, "n2": n2, "lean": lean, "inc": inc, "P": P_of(t), "M": M_of(t),
               "source": src if Lv == "house" else "cha", "id": finputs[key][2] if key in finputs else None,
               "lean_t2": lean if c["special"] and Lv == "house" else None, "lean_own": lean_own,
               "file_lean": fi.get("lean"), "file_inc": fi.get("incumbency")}
        if Lv == "governor":
            lg = last_governor_race(gov, c["state"], t)
            row["lag"] = lg[1] if lg else None
            row["lag_year"] = lg[0] if lg else None
            flg = fi.get("last_governor_race")
            row["file_lag"] = flg["share_D"] if flg else None
        rows.append(row)
    return rows, skipped


def medsl_senate_contests():
    path, _ = L.fetch(MEDSL[0], MEDSL[1], MEDSL[2])
    contests = {}
    with open(path, encoding="utf-8", errors="replace") as f:
        for r in csv.DictReader(f):
            if (r.get("stage") or "gen").lower() not in ("gen", "general"):
                continue
            y, st = int(r["year"]), r["state_po"].strip()
            spec = str(r.get("special", "")).strip().upper() in ("TRUE", "1")
            c = contests.setdefault((y, st, spec), {"year": y, "state": st, "special": spec, "candidates": {}, "totalvotes": set()})
            try:
                c["totalvotes"].add(int(float(r["totalvotes"])))
            except (TypeError, ValueError):
                pass
            name = (r.get("candidate") or "").strip()
            party = (r.get("party_simplified") or r.get("party_detailed") or "").strip()
            try:
                votes = int(float(r.get("candidatevotes") or 0))
            except ValueError:
                votes = 0
            a = c["candidates"].setdefault(name or "(blank)", {"name": name, "parties": [], "votes": 0})
            a["votes"] += votes
            if party and party not in a["parties"]:
                a["parties"].append(party)
    out = []
    for k in sorted(contests):
        c = contests[k]
        tv = sorted(c["totalvotes"])
        out.append({"year": c["year"], "state": c["state"], "special": c["special"],
                    "candidates": sorted(c["candidates"].values(), key=lambda a: -a["votes"]),
                    "totalvotes": tv[0] if len(tv) == 1 else None})
    return out


def medsl_party(a):
    labels = " ".join(a["parties"]).upper()
    d, r = "DEMOCRAT" in labels, "REPUBLICAN" in labels
    return "D" if d and not r else "R" if r and not d else None


def cls(y):
    return {2: 1, 4: 2, 0: 3}[y % 6]


def inferred_incumbency(state_contests, t, dr):
    prev = [c for c in state_contests if (c["year"] == t - 6 and not c["special"] and cls(c["year"]) == cls(t))
            or (c["special"] and t - 6 < c["year"] < t)]
    winners = {last_name(max(c["candidates"], key=lambda a: a["votes"] or 0)["name"]) for c in prev}
    D, R = dr
    d_inc, r_inc = last_name(D["name"]) in winners, last_name(R["name"]) in winners
    return (1 if d_inc else 0) - (1 if r_inc else 0) if d_inc != r_inc else 0


def medsl_senate_rows(ps):
    medsl = medsl_senate_contests()
    by_state = {}
    for c in medsl:
        by_state.setdefault(c["state"], []).append(c)
    rows, skipped = [], {}

    def skip(w):
        skipped[w] = skipped.get(w, 0) + 1
    for c in medsl:
        t = c["year"]
        if not (FIT_FROM["senate"] <= t < 2006) or c["state"] not in STATES_50:
            continue
        if c["special"]:
            skip("MEDSL special")
            continue
        cands = [{"name": a["name"], "party": medsl_party(a), "votes": a["votes"]} for a in c["candidates"]]
        dr = top_two_DR(cands)
        if not dr:
            skip("MEDSL: not a D and an R leading")
            continue
        lead = max(a["votes"] or 0 for a in cands)
        if c["state"] in ("GA", "LA") and lead < 0.5 * (c["totalvotes"] or 0):
            skip("MEDSL: GA or LA, leader under half")
            continue
        py = last_pres_year(t)
        if c["state"] not in ps.get(py, {}):
            skip("no state presidential vote")
            continue
        D, R = dr
        n2 = D["votes"] + R["votes"]
        rows.append({"year": t, "level": "senate", "state": c["state"], "district": None, "special": False,
                     "y": D["votes"] / n2, "n2": n2, "lean": ps[py][c["state"]] - ps[py]["US"],
                     "inc": inferred_incumbency(by_state[c["state"]], t, dr), "P": P_of(t), "M": M_of(t), "source": "medsl",
                     "id": None})
    return rows, skipped, medsl, by_state


def incumbency_check(rows, medsl_by_state):
    """D2's inferred rule on MEDSL's regular Senate races of 2006-2024 against Cha's hand coding (the fit rows)."""
    agree, n, wrong = 0, 0, []
    for r in rows:
        if r["level"] != "senate" or r["year"] < 2006 or r["special"] or r["source"] != "cha":
            continue
        mc = [c for c in medsl_by_state.get(r["state"], []) if c["year"] == r["year"] and not c["special"]]
        if len(mc) != 1:
            continue
        cands = [{"name": a["name"], "party": medsl_party(a), "votes": a["votes"]} for a in mc[0]["candidates"]]
        dr = top_two_DR(cands)
        if not dr:
            continue
        n += 1
        inf = inferred_incumbency(medsl_by_state[r["state"]], r["year"], dr)
        if inf == r["inc"]:
            agree += 1
        else:
            wrong.append(f"{r['year']} {r['state']}: inferred {inf:+d}, Cha {r['inc']:+d}")
    return {"races": n, "agree": agree, "differ": wrong}


def aa_governor_rows(finputs):
    """Governors of 1978-2004 from the files: the two nominees' votes and the others' line (Algara and Amlani's county
    sums), a row where both nominees had votes and the others' total is below the smaller nominee's; Missouri out."""
    rows, skipped = [], {}

    def skip(w):
        skipped[w] = skipped.get(w, 0) + 1
    for (level, t, st, d, sp), (fi, tp, cid, c) in sorted(finputs.items(), key=lambda kv: str(kv[0])):
        if level != "governor" or not (FIT_FROM["governor"] <= t < 2006) or t % 2 or st not in STATES_50:
            continue
        if st == "MO":
            skip("AA: Missouri")
            continue
        cands = c["result"]["candidates"]
        D = sum(a["votes"] or 0 for a in cands if a.get("party") == "D")
        R = sum(a["votes"] or 0 for a in cands if a.get("party") == "R")
        others = sum(a["votes"] or 0 for a in cands if a.get("party") not in ("D", "R"))
        if not D or not R or others >= min(D, R):
            skip("AA: not a D and an R leading")
            continue
        py = last_pres_year(t)
        lg = fi.get("last_governor_race")
        n2 = D + R
        rows.append({"year": t, "level": "governor", "state": st, "district": None, "special": False, "y": D / n2, "n2": n2,
                     "lean": fi["lean"], "inc": fi["incumbency"], "P": P_of(t), "M": M_of(t), "source": "file(aa)", "id": cid,
                     "lag": lg["share_D"] if lg else None, "lag_year": lg["year"] if lg else None,
                     "file_lag": lg["share_D"] if lg else None, "file_lean": fi["lean"], "file_inc": fi["incumbency"]})
    return rows, skipped


def set_special_lines(rows, mode):
    """Point every House special row's lean at the chosen convention ("own": D2's, the sheet of its own year;
    "t-2": the files', the lines it was held on); rows without the other reading keep the files'."""
    n = 0
    for r in rows:
        if r["level"] == "house" and r["special"]:
            want = r.get("lean_own") if mode == "own" else r.get("lean_t2")
            if want is None:
                want = r.get("lean_t2") if r.get("lean_t2") is not None else r["lean"]
            if abs(want - r["lean"]) > 1e-12:
                n += 1
            r["lean"] = want
    reset()
    return n


def all_rows(refresh=False):
    """Every fit row, with the counts skipped and the checks of the inputs against the files; cached."""
    if not refresh and os.path.exists(ROWS_CACHE):
        out = L.load_json(ROWS_CACHE)
        if all("lean_own" in r or r["level"] != "house" for r in out["rows"]):
            set_special_lines(out["rows"], SPECIAL_LINES)
            return out
    ps = pres_shares()
    finputs = file_inputs()
    cha = cha_contests()
    gov = last_governor_index(cha, finputs)
    rows, sk = cha_rows(cha, ps, finputs, gov)
    more, sk2, medsl, by_state = medsl_senate_rows(ps)
    gmore, sk3 = aa_governor_rows(finputs)
    sk.update(sk2)
    sk.update(sk3)
    out = {"rows": rows + more + gmore, "skipped": sk, "incumbency_check": incumbency_check(rows, by_state),
           "pres_shares": {str(y): v for y, v in ps.items()}}
    os.makedirs(L.CACHE, exist_ok=True)
    with open(ROWS_CACHE, "w") as f:
        json.dump(out, f)
    set_special_lines(out["rows"], SPECIAL_LINES)
    return out


# --------------------------------------------------------------------------------------------------- fits
def ols(X, y):
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return beta, y - X @ beta


def fit(rows, level, years, national_from=None):
    lag = level == "governor"
    R = [r for r in rows if r["level"] == level and r["year"] in years and (not lag or r.get("lag") is not None)]
    ys = sorted({r["year"] for r in R})
    X = np.array([[1.0 if r["year"] == t else 0.0 for t in ys] + [r["lean"], r["inc"]] + ([r["lag"] - 0.5] if lag else []) for r in R])
    y = np.array([r["y"] - 0.5 for r in R])
    beta, res = ols(X, y)
    a = {t: float(b) for t, b in zip(ys, beta[:len(ys)])}
    s_e = float(np.sqrt((res ** 2).sum() / (len(y) - X.shape[1])))
    base = {"level": level, "years": ys, "n": len(R), "a": a, "b_lean": float(beta[len(ys)]), "b_inc": float(beta[len(ys) + 1]),
            "b_lag": float(beta[len(ys) + 2]) if lag else None, "lag": lag, "s_e": s_e}
    if national_from is not None:
        return dict(base, c=list(national_from["c"]), s_a=national_from["s_a"], ZtZ_inv=national_from["ZtZ_inv"],
                    national_from={"level": national_from["level"], "years": national_from["years"]})
    Z = np.array([[1.0, M_of(t) * P_of(t), (1 - M_of(t)) * P_of(t)] for t in ys])
    if len(ys) - 3 < 1:
        raise ValueError("too few cycles")
    if np.linalg.matrix_rank(Z) < 3:
        raise ValueError("one party")
    c, d = ols(Z, np.array([a[t] for t in ys]))
    return dict(base, c=[float(v) for v in c], s_a=float(np.sqrt((d ** 2).sum() / (len(ys) - 3))), ZtZ_inv=np.linalg.inv(Z.T @ Z).tolist())


def fit_years(level, T):
    return list(range(FIT_FROM[level], T, 2))


_RAW = {}


def raw_model(rows, level, year):
    ck = (level, year)
    if ck in _RAW:
        return _RAW[ck]
    fy = [t for t in fit_years(level, year) if any(r["level"] == level and r["year"] == t for r in rows)]
    out = None, fy
    try:
        if len(fy) >= K_MIN:
            out = fit(rows, level, fy), fy
        elif level == "house" and fy:
            ms, _ = raw_model(rows, "senate", year)
            if ms is not None:
                out = fit(rows, level, fy, national_from=ms), fy
    except ValueError:
        pass
    _RAW[ck] = out
    return out


def national(m, t):
    z = np.array([1.0, M_of(t) * P_of(t), (1 - M_of(t)) * P_of(t)])
    a_hat = float(z @ np.array(m["c"]))
    return a_hat, m["s_a"] * math.sqrt(1.0 + float(z @ np.array(m["ZtZ_inv"]) @ z)) * m.get("k", 1.0)


def predict(m, r):
    a_hat, sd_a = national(m, r["year"])
    mean = 0.5 + a_hat + m["b_lean"] * r["lean"] + m["b_inc"] * r["inc"] + (m["b_lag"] * (r["lag"] - 0.5) if m["lag"] else 0.0)
    sh = m.get("shrink")
    if sh:
        mean = 0.5 + sh["factor"] * (mean - 0.5)
    return mean, math.sqrt(sd_a ** 2 + (m["s_e"] * m.get("k", 1.0)) ** 2), a_hat


def test_rows(rows, Lv, T):
    return [r for r in rows if r["level"] == Lv and r["year"] == T and (Lv != "governor" or r.get("lag") is not None)]


_SC = {}


def raw_scored(rows, level):
    """{T: [(mean, sd, y)]} of the level's raw out-of-sample forecasts (k = 1, no shrinkage)."""
    if level not in _SC:
        out = {}
        for T in range(FIT_FROM[level], 2025, 2):
            test = test_rows(rows, level, T)
            m, _ = raw_model(rows, level, T)
            if m is None or not test:
                continue
            out[T] = [(mu, sd, r["y"]) for r in test for mu, sd, _ in [predict(m, r)]]
        _SC[level] = out
    return _SC[level]


def calibration(rows, level, year, shrink=None, kmode="all"):
    sc = raw_scored(rows, level)
    yrs = [t for t in sorted(sc) if t < year]
    if len(yrs) < CAL_MIN:
        return {"k": 1.0, "years": yrs, "races": sum(len(sc[t]) for t in yrs)}
    lam = shrink["factor"] if shrink else None
    if kmode != "all":
        def rms(t):
            z = [((y - mu) if lam is None else (y - 0.5 - lam * (mu - 0.5))) / sd for mu, sd, y in sc[t]]
            return math.sqrt(sum(x * x for x in z) / len(z)), len(z)
        if kmode.startswith("last"):
            use = yrs[-int(kmode[4:]):]
            z2 = sum(rms(t)[0] ** 2 * rms(t)[1] for t in use)
            n = sum(rms(t)[1] for t in use)
            return {"k": math.sqrt(z2 / n), "years": use, "races": n, "kmode": kmode}
        if kmode == "trend":
            xs = np.array(yrs, float)
            ys = np.array([rms(t)[0] for t in yrs])
            b1, b0 = np.polyfit(xs, ys, 1)
            k = float(min(1.5, max(0.5, b0 + b1 * year)))
            return {"k": k, "years": yrs, "races": sum(len(sc[t]) for t in yrs), "kmode": kmode, "slope_per_cycle": float(2 * b1)}
        raise ValueError(kmode)
    zs = [((y - mu) if lam is None else (y - 0.5 - lam * (mu - 0.5))) / sd for t in yrs for mu, sd, y in sc[t]]
    return {"k": math.sqrt(sum(z * z for z in zs) / len(zs)), "years": yrs, "races": len(zs)}


def shrink_factor(rows, level, year):
    sc = raw_scored(rows, level)
    yrs = [t for t in sorted(sc) if t < year]
    if len(yrs) < CAL_MIN:
        return None
    num = sum((mu - 0.5) * (y - 0.5) / sd ** 2 for t in yrs for mu, sd, y in sc[t])
    den = sum((mu - 0.5) ** 2 / sd ** 2 for t in yrs for mu, sd, y in sc[t])
    return {"factor": num / den, "years": yrs, "races": sum(len(sc[t]) for t in yrs)}


def variant_model(rows, level, year, variant):
    m, fy = raw_model(rows, level, year)
    if m is None:
        return None, fy
    shrink, tails = VARIANTS[variant][:2]
    kmode = VARIANTS[variant][2] if len(VARIANTS[variant]) > 2 else "all"
    sh = shrink_factor(rows, level, year) if shrink else None
    cal = calibration(rows, level, year, sh, kmode)
    return dict(m, k=cal["k"], calibration=cal, shrink=sh, tails=tails, variant=variant), fy


# ---------------------------------------------------------------------------------------- distributions
def cdf(x, mean, sd, tails):
    z = (x - mean) / sd
    return stats.norm.cdf(z) if tails == "normal" else stats.t.cdf(z * SQRT2, 4)


def logpdf(x, mean, sd, tails):
    if tails == "normal":
        return stats.norm.logpdf(x, mean, sd)
    return stats.t.logpdf(x, 4, mean, sd / SQRT2)


def near_q(mean, sd, tails, w=NEAR_W):
    return cdf(0.5 + w, mean, sd, tails) - cdf(0.5 - w, mean, sd, tails)


def near_band(mean):
    d = abs(mean - 0.5)
    return max(i for i, b in enumerate(NEAR_BANDS) if d >= b)


# ----------------------------------------------------------------------------------------- near ties
_NEAR = {}


def near_scored(rows, variant):
    """{(level, T): {"mu", "sd", "y", "q1", "inside", "band"}} as arrays: every year's out-of-sample forecasts under
    the variant (before the factor); q1 the forecast's chance of 49-51%."""
    ck = ("scored", variant)
    if ck not in _NEAR:
        out = {}
        tails = VARIANTS[variant][1]
        for Lv in LEVELS:
            for T in range(FIT_FROM[Lv], 2025, 2):
                test = test_rows(rows, Lv, T)
                m, _ = variant_model(rows, Lv, T, variant)
                if m is None or not test:
                    continue
                pr = [predict(m, r) for r in test]
                mu = np.array([x[0] for x in pr])
                sd = np.array([x[1] for x in pr])
                y = np.array([r["y"] for r in test])
                out[(Lv, T)] = {"mu": mu, "sd": sd, "y": y, "q1": near_q(mu, sd, tails),
                                "inside": np.abs(y - 0.5) < NEAR_W,
                                "band": np.array([near_band(x) for x in mu])}
        _NEAR[ck] = out
    return _NEAR[ck]


def solve_factor(qs, seen):
    """F with sum F q / (1 + (F - 1) q) = seen (bisection: the expected count in the window equals the one seen)."""
    qs = np.asarray(qs)
    lo, hi = 1e-3, 50.0
    for _ in range(200):
        F = (lo + hi) / 2
        lo, hi = (F, hi) if (F * qs / (1 + (F - 1) * qs)).sum() < seen else (lo, F)
    return (lo + hi) / 2


def near_groups(rows, year, scheme, variant):
    """(own, pooled): {group: [q1 array, seen, {level: years}]} over every level's scored years before `year`;
    groups by level (scheme level) or by (level, band) and band (scheme band)."""
    own, pool = {}, {}
    for (Lv, T), a in near_scored(rows, variant).items():
        if T >= year:
            continue
        for b in (range(len(NEAR_BANDS)) if scheme == "band" else (None,)):
            sel = (a["band"] == b) if b is not None else np.ones(len(a["mu"]), bool)
            if not sel.any():
                continue
            for g, k in ((own, Lv if b is None else (Lv, b)), (pool, "all" if b is None else b)):
                e = g.setdefault(k, [[], 0, {}])
                e[0].append(a["q1"][sel])
                e[1] += int(a["inside"][sel].sum())
                e[2].setdefault(Lv, set()).add(T)
    return own, pool


def near_tie_factor(rows, level, year, mean, scheme, variant):
    """The near-tie factor for a forecast of `level` in `year` with this mean under the scheme: own if the level's
    (and band's) fitting years expect 30 or more near-ties, else pooled over levels, else none (factor 1)."""
    b = near_band(mean) if scheme == "band" else None
    ck = ("factor", variant, scheme, year, level, b)
    if ck in _NEAR:
        return _NEAR[ck]
    cc_ = ("counts", variant, scheme, year)
    if cc_ not in _NEAR:
        _NEAR[cc_] = near_groups(rows, year, scheme, variant)
    own, pool = _NEAR[cc_]
    out = {"factor": 1.0, "of": None, "fitted_on": {}, "expected": None, "seen": None}
    for groups, k, of in ((own, level if scheme == "level" else (level, b), "own"), (pool, "all" if scheme == "level" else b, "pooled")):
        e = groups.get(k)
        if e:
            qs = np.concatenate(e[0])
            if qs.sum() >= NEAR_MIN_EXPECTED:
                out = {"factor": solve_factor(qs, e[1]), "of": of, "fitted_on": {L_: sorted(ys) for L_, ys in sorted(e[2].items())},
                       "expected": float(qs.sum()), "seen": e[1]}
                break
    _NEAR[ck] = out
    return out


def factors_for(rows, level, T, a, scheme, variant):
    """The factor of each forecast in the scored block a under the scheme (an array)."""
    if scheme is None:
        return np.ones(len(a["mu"]))
    if scheme == "level":
        return np.full(len(a["mu"]), near_tie_factor(rows, level, T, 0.5, "level", variant)["factor"])
    fb = np.array([near_tie_factor(rows, level, T, 0.5 + bf + 1e-9, "band", variant)["factor"] for bf in NEAR_BANDS])
    return fb[a["band"]]


def cdf_near(x, mean, sd, tails, F):
    q1 = near_q(mean, sd, tails)
    base = cdf(x, mean, sd, tails)
    extra = (F - 1) * np.maximum(0.0, cdf(np.minimum(x, 0.5 + NEAR_W), mean, sd, tails) - cdf(0.5 - NEAR_W, mean, sd, tails))
    return (base + extra) / (1 + (F - 1) * q1)


def _scored_block(a, F, tails):
    """Per-forecast log score, PIT and window expectations under factors F (arrays)."""
    mu, sd, y, q1 = a["mu"], a["sd"], a["y"], a["q1"]
    Z = 1 + (F - 1) * q1
    ls = logpdf(y, mu, sd, tails) + np.where(a["inside"], np.log(F), 0.0) - np.log(Z)
    u = cdf_near(y, mu, sd, tails, F)
    win = {w: ((near_q(mu, sd, tails, w=w) + (F - 1) * q1) / Z, np.abs(y - 0.5) < w) for w in NEAR_WINDOWS}
    return ls, u, win, F * q1 / Z, Z


def near_score(rows, level, scheme, years, variant):
    n, ls, cov = 0, 0.0, np.zeros(3)
    win = {w: [0.0, 0] for w in NEAR_WINDOWS}
    by_band = {b: [0.0, 0] for b in range(len(NEAR_BANDS))}
    tails = VARIANTS[variant][1]
    for (Lv, T), a in sorted(near_scored(rows, variant).items()):
        if Lv != level or T not in years:
            continue
        F = factors_for(rows, Lv, T, a, scheme, variant)
        l_, u, w_, e1, _ = _scored_block(a, F, tails)
        n += len(l_)
        ls += l_.sum()
        for i, c_ in enumerate((0.5, 0.8, 0.95)):
            cov[i] += (np.abs(u - 0.5) <= c_ / 2).sum()
        for w in NEAR_WINDOWS:
            win[w][0] += w_[w][0].sum()
            win[w][1] += int(w_[w][1].sum())
        for b in by_band:
            sel = a["band"] == b
            by_band[b][0] += e1[sel].sum()
            by_band[b][1] += int(a["inside"][sel].sum())
    return {"races": n, "mean_log_score": ls / n if n else None,
            "by_band": {b: {"expected": float(v[0]), "seen": v[1]} for b, v in by_band.items()},
            "coverage": list(cov / n) if n else None,
            "within": {w: {"expected": float(v[0]), "seen": v[1]} for w, v in win.items()}}


def near_tie_test(rows, variant):
    ck = ("test", variant)
    if ck in _NEAR:
        return _NEAR[ck]
    out = {"by_level": {}, "adopted": {}}
    sc = near_scored(rows, variant)
    for Lv in LEVELS:
        yrs = sorted(T for (L_, T) in sc if L_ == Lv)
        reach = [T for T in yrs if any(near_tie_factor(rows, Lv, T, 0.5 + bf + 1e-9, sch, variant)["of"]
                                       for sch in ("level", "band") for bf in (NEAR_BANDS if sch == "band" else (0.0,))
                                       if sch == "level" or (sc[(Lv, T)]["band"] == near_band(0.5 + bf + 1e-9)).any())]
        res = {"years": reach, "none": near_score(rows, Lv, None, reach, variant)}
        for sch in ("level", "band"):
            res[sch] = near_score(rows, Lv, sch, reach, variant)
        res["factors_by_year"] = {T: {"level": near_tie_factor(rows, Lv, T, 0.5, "level", variant),
                                      "band": [near_tie_factor(rows, Lv, T, 0.5 + b + 1e-9, "band", variant) for b in NEAR_BANDS]} for T in yrs}
        best = None
        if reach:
            for sch in ("level", "band"):
                r = res[sch]
                r.update(_round4(res["none"], r))
                # round 5's cells on the scheme (D2's #53, REPORT 0.2): in the 10-20 and 20+ point bands no near-even
                # count may move further from the one seen, tested where seen or expected is 5 or more
                r["round_5_cells"] = _round5_cells(rows, Lv, variant, reach, sch)
                # both again with any one scored year left out (the factors as fitted)
                loo = {}
                for y in reach:
                    yrs = [t for t in reach if t != y]
                    b0y, ry = near_score(rows, Lv, None, yrs, variant), near_score(rows, Lv, sch, yrs, variant)
                    f4 = _round4(b0y, ry)
                    c5 = _round5_cells(rows, Lv, variant, yrs, sch)
                    fails = ([] if f4["raises_log_score"] else ["the log score"]) + ([] if f4["count_nearer"] else ["the 49-51% count"]) \
                        + ([] if f4["safe_seats_supported"] else ["the safe seats' 49-51% count (|mean - 1/2| from 0.10)"]) + c5["safe_bands_further"]
                    loo[y] = {"improves": bool(f4["improves"] and c5["improves"]), "mean_log_score_gain": ry["mean_log_score"] - b0y["mean_log_score"],
                              "fails": fails}
                r["leave_one_year_out"] = loo
                r["robust"] = bool(r["improves"] and r["round_5_cells"]["improves"] and all(x["improves"] for x in loo.values()))
                if r["robust"] and (best is None or r["mean_log_score"] > res[best]["mean_log_score"]):
                    best = sch
        res["adopted"] = best
        out["by_level"][Lv] = res
        out["adopted"][Lv] = best
    _NEAR[ck] = out
    return out


def _round4(b0, r):
    """Round 4's three tests of a scheme against none on the same years (REPORT 2.6)."""
    better = r["mean_log_score"] > b0["mean_log_score"]
    nearer = abs(r["within"][NEAR_W]["expected"] - r["within"][NEAR_W]["seen"]) < abs(b0["within"][NEAR_W]["expected"] - b0["within"][NEAR_W]["seen"])
    kb = len(NEAR_BANDS) - 1
    safe = abs(r["by_band"][kb]["expected"] - r["by_band"][kb]["seen"]) <= abs(b0["by_band"][kb]["expected"] - b0["by_band"][kb]["seen"])
    return {"raises_log_score": better, "count_nearer": nearer, "safe_seats_supported": safe, "improves": bool(better and nearer and safe)}


def _round5_cells(rows, level, variant, years, sch, min_count=None):
    """Round 5's safe cells (REPORT 2.7) applied to a near-tie scheme: the scheme's near-even counts in the safe bands
    against none's (the same forecasts, so the bands are the same), tested where seen or expected is 5 or more."""
    min_count = VARIANT_MIN_COUNT if min_count is None else min_count
    r0 = variant_score(rows, level, variant, years, sch=None, use_sch=False)
    r = variant_score(rows, level, variant, years, sch=sch, use_sch=False)
    tested, failed = [], []
    for b in VARIANT_SAFE:
        for w, x0 in r0["by_band"][b]["within"].items():
            if x0["seen"] < min_count and x0["expected"] < min_count:
                continue
            x = r["by_band"][b]["within"][w]
            tested.append((b, w))
            if abs(x["expected"] - x["seen"]) > abs(x0["expected"] - x0["seen"]):
                failed.append((b, w))
    # 'improves' as chambers.py records it: round 5's whole verdict on the scheme (the log score, the 49-51% count, the cells)
    raises = r["mean_log_score"] > r0["mean_log_score"]
    nearer = abs(r["within"][NEAR_W]["expected"] - r["within"][NEAR_W]["seen"]) < abs(r0["within"][NEAR_W]["expected"] - r0["within"][NEAR_W]["seen"])
    return {"improves": bool(raises and nearer and not failed), "cells_hold": not failed, "safe_bands_tested": tested, "safe_bands_further": failed}


# ------------------------------------------------------------------------------------------- variants
def variant_score(rows, level, variant, years, sch=None, use_sch=True, bands_by_none=True):
    """The level's out-of-sample forecasts of `years` under the variant with its adopted near-tie scheme (or the one
    given): log score, coverage, near-even counts overall and by band of none's mean, the tails toward 1/2, z rms."""
    tails = VARIANTS[variant][1]
    if use_sch and sch is None:
        sch = near_tie_test(rows, variant)["adopted"].get(level)
    sc, sc0 = near_scored(rows, variant), near_scored(rows, "none")
    nb = len(VARIANT_BANDS)
    tot = {"races": 0, "ls": 0.0, "cov": np.zeros(3), "win": {w: [0.0, 0] for w in NEAR_WINDOWS}, "z2": 0.0}
    band = [{"races": 0, "ls": 0.0, "win": {w: [0.0, 0] for w in NEAR_WINDOWS}, "tail": {t_: [0.0, 0] for t_ in TAIL_LEVELS}, "z2": 0.0} for _ in range(nb)]
    for T in years:
        if (level, T) not in sc:
            continue
        a, a0 = sc[(level, T)], sc0[(level, T)]
        F = factors_for(rows, level, T, a, sch, variant)
        l_, u, w_, _, _ = _scored_block(a, F, tails)
        z2 = ((a["y"] - a["mu"]) / a["sd"]) ** 2
        b = np.array([max(i for i, x in enumerate(VARIANT_BANDS) if abs(m0 - 0.5) >= x) for m0 in (a0["mu"] if bands_by_none else a["mu"])])
        tot["races"] += len(l_)
        tot["ls"] += l_.sum()
        tot["z2"] += z2.sum()
        for i, c_ in enumerate((0.5, 0.8, 0.95)):
            tot["cov"][i] += (np.abs(u - 0.5) <= c_ / 2).sum()
        for w in NEAR_WINDOWS:
            tot["win"][w][0] += w_[w][0].sum()
            tot["win"][w][1] += int(w_[w][1].sum())
        for bi in range(nb):
            sel = b == bi
            if not sel.any():
                continue
            g = band[bi]
            g["races"] += int(sel.sum())
            g["ls"] += l_[sel].sum()
            g["z2"] += z2[sel].sum()
            for w in NEAR_WINDOWS:
                g["win"][w][0] += w_[w][0][sel].sum()
                g["win"][w][1] += int(w_[w][1][sel].sum())
            for t_ in TAIL_LEVELS:
                g["tail"][t_][0] += t_ * sel.sum()
                g["tail"][t_][1] += int(np.where(a["mu"][sel] < 0.5, u[sel] > 1 - t_, u[sel] < t_).sum())
    n = tot["races"]
    return {"variant": variant, "near_tie": sch, "races": n, "mean_log_score": tot["ls"] / n if n else None,
            "z_rms": math.sqrt(tot["z2"] / n) if n else None,
            "coverage": list(tot["cov"] / n) if n else None,
            "within": {w: {"expected": float(v[0]), "seen": v[1]} for w, v in tot["win"].items()},
            "by_band": [{"races": g["races"], "mean_log_score": g["ls"] / g["races"] if g["races"] else None,
                         "z_rms": math.sqrt(g["z2"] / g["races"]) if g["races"] else None,
                         "within": {w: {"expected": float(v[0]), "seen": v[1]} for w, v in g["win"].items()},
                         "tail": {t_: {"expected": float(v[0]), "seen": v[1]} for t_, v in g["tail"].items()}} for g in band]}


def variant_test(rows, years=None, min_count=None, strict_further=True, bands_by_none=True, with_years=True):
    """D2's variants test (REPORT 2.7): adopt the best-scoring variant that raises the log score, brings the 49-51%
    count nearer, and moves no tested safe-band count further (strictly, as written) than none's. The parameters
    vary the rule for the flip analysis (c10)."""
    years = list(VARIANT_YEARS) if years is None else list(years)
    min_count = VARIANT_MIN_COUNT if min_count is None else min_count
    out = {"by_level": {}, "adopted": {}, "shrink_by_year": {}, "k_by_year": {}}
    for Lv in LEVELS:
        res = {v: variant_score(rows, Lv, v, years, bands_by_none=bands_by_none) for v in ("none", "shrink", "t4", "both")}
        b0 = res["none"]
        best = None
        for v in ("shrink", "t4", "both"):
            r = res[v]
            if not r["races"]:
                continue
            r["raises_log_score"] = r["mean_log_score"] > b0["mean_log_score"]
            r["count_nearer"] = abs(r["within"][NEAR_W]["expected"] - r["within"][NEAR_W]["seen"]) < abs(b0["within"][NEAR_W]["expected"] - b0["within"][NEAR_W]["seen"])
            tested, failed = [], []
            for b in VARIANT_SAFE:
                for w, x0 in b0["by_band"][b]["within"].items():
                    if x0["seen"] < min_count and x0["expected"] < min_count:
                        continue
                    x = r["by_band"][b]["within"][w]
                    tested.append((b, w))
                    d, d0 = abs(x["expected"] - x["seen"]), abs(x0["expected"] - x0["seen"])
                    if (d > d0) if strict_further else (d >= d0):
                        failed.append((b, w))
            r["safe_bands_tested"], r["safe_bands_further"] = tested, failed
            r["safe_seats_supported"] = not failed
            r["improves"] = bool(r["raises_log_score"] and r["count_nearer"] and r["safe_seats_supported"])
            if r["improves"] and (best is None or r["mean_log_score"] > res[best]["mean_log_score"]):
                best = v
        res["adopted"] = best or "none"
        out["by_level"][Lv] = res
        out["adopted"][Lv] = best or "none"
        if with_years:
            out["shrink_by_year"][Lv] = {T: shrink_factor(rows, Lv, T) for T in years}
            out["k_by_year"][Lv] = {T: {"none": calibration(rows, Lv, T)["k"], "shrunk": calibration(rows, Lv, T, shrink_factor(rows, Lv, T))["k"]} for T in years}
    return out


def reset():
    _RAW.clear()
    _SC.clear()
    _NEAR.clear()
