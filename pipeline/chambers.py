"""pipeline/chambers.py: the model's own forecast for Senate, House and governor races, and control of
the Senate and the House.

Written 2026-11-07 by worker D2 (briefs/D2-data-congress.md). Every function says where its inputs come
from; the inputs are the caches the scripts in pipeline/intake/ write (CACHE below), never the network.

THE FORECAST (model section 3, "Which forecast": no forecaster's published forecast for these races is
reachable here, so the model builds one "from what was known before the election", by regression on like
past races, as Gelman, King & Boscardin did). For race i of level L in year t, with y_i the Democrat's
share of the two-party vote:

    y_i = 1/2 + a_t + b_L * lean_i + b_I * inc_i [+ b_G * (lag_i - 1/2), governors] + e_i

  lean_i  the Democrat's two-party share of the last presidential vote held BEFORE year t, in the district
          (House, on the lines in use in year t; The Downballot) or the state (Senate, governor; MEDSL),
          minus the national share in that presidential election (MEDSL);
  inc_i   +1 if a Democratic incumbent runs, -1 if a Republican incumbent runs, 0 for an open seat
          (Cha, Kuriwaki and Snyder's hand-coded incumbency; for the Senate before 2006, inferred from MEDSL);
  lag_i   governors only: the Democrat's two-party share in the state's last governor race before year t that
          a Democrat and a Republican led (Cha from 2006, Algara and Amlani's county returns before; M2's A4,
          the orchestrator 2026-11-07 05:58, item 5);
  a_t     the year's national swing, common to every race of the level that year;
  e_i     the race's own error, independent across races.

Before the election a_t is not known. Its forecast is a regression on what is known: whether t is a
midterm, and the president's party (National Archives):

    a_t = c_0 + c_mid * M_t * P_t + c_on * (1 - M_t) * P_t + d_t,    d_t ~ N(0, s_a^2)

with M_t = 1 in a midterm, P_t = +1 if the sitting president is a Democrat and -1 if a Republican.

EARLIER CYCLES ONLY (method D2-v2, the orchestrator, 2026-11-07 05:58, item 2; D2-v3 from 06:36). The forecast
for year t is fitted on the level's cycles before t and nothing later, as a forecaster then could have: the House
from 2006, the Senate from 1982 (MEDSL reaches back before Cha), governors from 1978 (Algara and Amlani's county
returns reach back before Cha; FIT_FROM). Its national sd
is the OLS prediction sd from those cycles, s_a sqrt(1 + z (Z'Z)^-1 z'). A fit needs at least K_MIN = 4
cycles (the three national terms and one degree of freedom for their spread) and presidents of both
parties among them; a year with fewer gets no forecast of its own (p not computed, unless 538's stands
first). The House of 2008-2012, with one to three earlier cycles of its own, takes the national terms (c, s_a,
(Z'Z)^-1) from the Senate's fit on the Senate's earlier cycles and fits b_lean, b_inc and s_e on its own
(06:36, item 2; raw_model). CALIBRATION (06:36, item 3): both sds are then multiplied by k, the root mean square
of z over the level's earlier years scored out of sample, once CAL_MIN = 3 such years exist (calibration). So the forecast for race i is normal with mean 1/2 + c_0 + c_.. P_t + b_L lean_i + b_I inc_i (+ b_G
(lag_i - 1/2)) and variance k^2 (sd_nat^2 + s_e^2); a Student-t with 4 degrees of freedom matched on the same sd
is computed alongside (model section 9.5). The common part sd_nat^2 is what ties races together for
control of a chamber (MATH 4.2): rho = sd_nat^2 / (sd_nat^2 + s_e^2).

Run:  python3 pipeline/chambers.py backtest      prints the fit and the back-test, writes
                                                data/congress/backtest.json
      python3 pipeline/chambers.py compute <year> ...   fills p and control in data/<level>/<year>.json
      python3 pipeline/chambers.py history      the record against the forecasts, data/congress/history.json
"""
import difflib
import json
import math
import os
import re
import sys
import unicodedata

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "intake"))
sys.path.insert(0, HERE)
import congress_common as cc  # noqa: E402

YEARS = list(range(2006, 2025, 2))
CAP = 0.25          # beyond a 25-point expected lead the error's spread is taken as constant
HETERO = os.environ.get("D2_HETERO", "0") == "1"   # tested in the back-test; not of record (REPORT.md)
LEVELS = ("house", "senate", "governor")
SQRT2 = math.sqrt(2.0)


# ----------------------------------------------------------------------------- inputs
def _load(rel):
    p = os.path.join(cc.CACHE, rel)
    if not os.path.exists(p):
        raise SystemExit(f"missing {p}: run the intake script that writes it (see pipeline/intake/)")
    with open(p) as f:
        return json.load(f)


def presidential_shares():
    """{year: {"US": share, "AL": share, ...}}: the Democrat's two-party share, from MEDSL President."""
    rows = _load("medsl/normalized/president_state.json")["rows"]
    out = {}
    for r in rows:
        if r["D"] + r["R"] > 0:
            out.setdefault(r["year"], {})[r["state"]] = r["D"] / (r["D"] + r["R"])
    for y in out:
        D = sum(r["D"] for r in rows if r["year"] == y)
        R = sum(r["R"] for r in rows if r["year"] == y)
        out[y]["US"] = D / (D + R)
    return out


def presidents():
    """{election year: row} from the National Archives' Electoral College pages."""
    return {r["year"]: r for r in _load("nara/normalized/electoral_college.json")}


def sitting_party(t, pres):
    """The party of the president in office on election day of year t (+1 Democrat, -1 Republican)."""
    y = max(k for k in pres if k < t)
    return 1 if pres[y]["party"] == "D" else -1


def last_pres_year(t):
    return t - 4 if t % 4 == 0 else t - 2


def district_key(state, dist, lean_year):
    """Cha numbers an at-large district 1; The Downballot calls it AL."""
    k = f"{state}-{dist}"
    if k not in lean_year and f"{state}-AL" in lean_year and dist == "01":
        return f"{state}-AL"
    return k


def _cls(y):
    """The Senate class of a regular election in year y: 2006, 2012, 2018, 2024 class 1; 2008, 2014, 2020 class 2;
    2010, 2016, 2022 class 3 (every six years)."""
    return {2: 1, 4: 2, 0: 3}[y % 6]


def _top_two_DR(cands):
    """(D, R) where exactly one Democrat and one Republican have votes and they are the two leading
    candidates; else None."""
    D = [a for a in cands if a["party"] == "D" and a["votes"]]
    R = [a for a in cands if a["party"] == "R" and a["votes"]]
    if len(D) != 1 or len(R) != 1:
        return None
    top2 = sorted([a for a in cands if a["votes"]], key=lambda a: -a["votes"])[:2]
    if {a["party"] for a in top2} != {"D", "R"}:
        return None
    return D[0], R[0]


# Algara and Amlani's Missouri rows fall short of Cha's totals by 7% for the Democrat and 2% for the Republican
# in each of 2008, 2012 and 2016 (pipeline/intake/algara_amlani.py's check), as they would if Kansas City, which
# reports apart from Jackson County, were missing from the county rows (inferred: the rows hold 115 jurisdictions,
# the 114 counties and St. Louis City). A count known to be incomplete is not used: no p, no fit row, no lag.
AA_INCOMPLETE = {"MO": "Algara and Amlani's Missouri rows fall short of Cha, Kuriwaki and Snyder's totals by 7% "
                       "for the Democrat and 2% for the Republican in each of 2008, 2012 and 2016, as they would "
                       "if Kansas City, which reports apart from Jackson County, were missing from the county rows "
                       "(inferred); the count is taken as incomplete"}


def aa_governors():
    """Algara and Amlani's governor elections, summed from county returns (pipeline/intake/algara_amlani.py)."""
    return _load("algara_amlani/normalized/governors.json")["elections"]


def aa_led_by_DR(r):
    """(D votes, R votes) when the Democrat and the Republican both had votes and the others' total is below the
    smaller of the two, so that no other candidate can have been among the top two; else None. The source
    gives the other candidates only as a total."""
    if not r["D"] or not r["R"] or r["others"] is None or r["others"] >= min(r["D"], r["R"]):
        return None
    return r["D"], r["R"]


def last_governor_index():
    """{state: [(year, Democrat's two-party share, special, source)]}: every governor election that a Democrat
    and a Republican led, odd years and specials included, the November round. From 2006, Cha, Kuriwaki and
    Snyder (the record); before 2006, Algara and Amlani's county returns (aa_led_by_DR), Missouri apart."""
    out = {}
    for c in _load("cha/normalized/contests.json")["contests"]:
        if c["office"] != "governor" or c["runoff"]:
            continue
        dr = _top_two_DR([a for a in c["candidates"]])
        if dr:
            out.setdefault(c["state"], []).append((c["year"], dr[0]["votes"] / (dr[0]["votes"] + dr[1]["votes"]),
                                                   bool(c["special"]), "cha"))
    for r in aa_governors():
        if r["year"] >= 2006 or r["state"] in AA_INCOMPLETE:
            continue
        dr = aa_led_by_DR(r)
        if dr:
            out.setdefault(r["state"], []).append((r["year"], dr[0] / (dr[0] + dr[1]), False, "algara_amlani"))
    return out


def last_governor_race(index, state, year):
    """The state's last governor race before year t that a Democrat and a Republican led (M2's A4, accepted by
    the orchestrator 2026-11-07 05:58, item 5): (year, the Democrat's two-party share, special, source), or None."""
    past = [x for x in index.get(state, []) if x[0] < year]
    return max(past, key=lambda x: x[0]) if past else None


# The Senate's fit reaches back before Cha, Kuriwaki and Snyder (2006) through MEDSL's U.S. Senate 1976-2024:
# from 1982, the first year whose seats' previous regular election (six years before) is in MEDSL, so that
# incumbency can be inferred (below). Reason: the forecast is fitted on earlier cycles only (the orchestrator,
# 2026-11-07 05:58, item 2: "extend the fitting data back where your sources reach (MEDSL from 1976, Cha)").
# Governors from 1978 (the orchestrator, 06:36, item 1): Algara and Amlani's county returns reach back before Cha,
# and 1978 is the first even year whose last presidential vote (1976) and sitting president are in the sources
# the inputs come from (MEDSL's U.S. President and the National Archives' pages, both from 1976). The House from
# 2006: The Downballot's district presidential vote begins on the 2006 lines, and which states kept the same
# lines in 2002-2004 is not stated in any source read here.
FIT_FROM = {"house": 2006, "senate": 1982, "governor": 1978}
GOV_FROM = 1978            # the first year of the governor contest files (data/governor/<year>.json)


def file_years(level):
    """The even years whose data/<level>/<year>.json this system builds."""
    return list(range(GOV_FROM if level == "governor" else 2006, 2025, 2))


def medsl_senate_rows(ps, pres):
    """Senate races of 1982-2004 from MEDSL (Cha begins in 2006), for the fit only. Incumbency is INFERRED: a
    candidate is the incumbent if their last name is that of the winner (most votes) of the seat's previous
    regular election (six years before) or of a special election in the state in the years between; MEDSL does
    not mark incumbents. Measured against Cha's hand-coded incumbency on 2006-2024 (incumbency_check below).
    Left out: special elections (the record does not say whose seat, and the sitting senator is often an
    appointee it does not show), and in Georgia and Louisiana a race whose leader had under half the vote (a
    runoff may have followed; MEDSL holds the November round)."""
    medsl = _load("medsl/normalized/senate.json")["contests"]
    by_state = {}
    for c in medsl:
        by_state.setdefault(c["state"], []).append(c)
    rows, skipped = [], {}

    def skip(why):
        skipped[why] = skipped.get(why, 0) + 1
    for c in medsl:
        t = c["year"]
        if not (FIT_FROM["senate"] <= t < 2006) or c["state"] not in cc.STATES_50:
            continue
        if c["special"]:
            skip("MEDSL, before 2006: a special election (whose seat, and who held it, not in the record)")
            continue
        cands = [{"name": a["name"], "party": _medsl_party(a), "votes": a["votes"]} for a in c["candidates"]]
        dr = _top_two_DR(cands)
        if not dr:
            skip("MEDSL, before 2006: not a Democrat and a Republican leading")
            continue
        lead = max(a["votes"] or 0 for a in cands)
        if c["state"] in ("GA", "LA") and lead < 0.5 * (c["totalvotes"] or 0):
            skip("MEDSL, before 2006: Georgia or Louisiana, leader under half the vote")
            continue
        py = last_pres_year(t)
        if c["state"] not in ps.get(py, {}):
            skip("no state presidential vote")
            continue
        inc = inferred_incumbency(by_state[c["state"]], t, dr)
        D, R = dr
        n2 = D["votes"] + R["votes"]
        rows.append({"year": t, "level": "senate", "state": c["state"], "district": None, "special": False,
                     "y": D["votes"] / n2, "n2": n2, "lean": ps[py][c["state"]] - ps[py]["US"], "inc": inc,
                     "inc_source": "inferred from MEDSL", "M": 0 if t % 4 == 0 else 1, "P": sitting_party(t, pres),
                     "source": "medsl_senate"})
    return rows, skipped


def _medsl_party(a):
    labels = " ".join(a["parties"]).upper()
    d, r = "DEMOCRAT" in labels, "REPUBLICAN" in labels
    return "D" if d and not r else "R" if r and not d else None


def inferred_incumbency(state_contests, t, dr):
    """+1, -1 or 0 by the rule in medsl_senate_rows, from MEDSL's own contests of the state."""
    prev = [c for c in state_contests if (c["year"] == t - 6 and not c["special"] and _cls(c["year"]) == _cls(t))
            or (c["special"] and t - 6 < c["year"] < t)]
    winners = {_last(max(c["candidates"], key=lambda a: a["votes"] or 0)["name"]) for c in prev}
    D, R = dr
    d_inc, r_inc = _last(D["name"]) in winners, _last(R["name"]) in winners
    return (1 if d_inc else 0) - (1 if r_inc else 0) if d_inc != r_inc else 0


def incumbency_check(rows):
    """The rule of inferred_incumbency applied to MEDSL's regular Senate races of 2006-2024, against Cha,
    Kuriwaki and Snyder's hand-coded incumbency for the same races (the fit rows of those years)."""
    medsl = _load("medsl/normalized/senate.json")["contests"]
    by_state = {}
    for c in medsl:
        by_state.setdefault(c["state"], []).append(c)
    agree, n, wrong = 0, 0, []
    for r in rows:
        if r["level"] != "senate" or r["year"] < 2006 or r["special"]:
            continue
        mc = [c for c in by_state.get(r["state"], []) if c["year"] == r["year"] and not c["special"]]
        if len(mc) != 1:
            continue
        cands = [{"name": a["name"], "party": _medsl_party(a), "votes": a["votes"]} for a in mc[0]["candidates"]]
        dr = _top_two_DR(cands)
        if not dr:
            continue
        n += 1
        inf = inferred_incumbency(by_state[r["state"]], r["year"], dr)
        if inf == r["inc"]:
            agree += 1
        else:
            wrong.append(f"{r['year']} {r['state']}: inferred {inf:+d}, Cha {r['inc']:+d}")
    return {"races": n, "agree": agree, "share": agree / n if n else None, "differ": wrong}


def aa_governor_rows(ps, pres, gov):
    """Governor races of 1978-2004 from Algara and Amlani (Cha begins in 2006), for the fit. Incumbency is the
    authors' seat status (an incumbent's re-election bid); a row needs the Democrat and the Republican to have
    led (aa_led_by_DR) and the state's presidential vote; it carries the state's last governor race."""
    rows, skipped = [], {}

    def skip(why):
        skipped[why] = skipped.get(why, 0) + 1
    for r in aa_governors():
        t = r["year"]
        if not (FIT_FROM["governor"] <= t < 2006) or t % 2 or r["state"] not in cc.STATES_50:
            continue
        if r["state"] in AA_INCOMPLETE:
            skip("Algara and Amlani, before 2006: Missouri, a count taken as incomplete")
            continue
        dr = aa_led_by_DR(r)
        if not dr:
            skip("Algara and Amlani, before 2006: not a Democrat and a Republican leading")
            continue
        py = last_pres_year(t)
        if r["state"] not in ps.get(py, {}):
            skip("no state presidential vote")
            continue
        lg = last_governor_race(gov, r["state"], t)
        n2 = dr[0] + dr[1]
        rows.append({"year": t, "level": "governor", "state": r["state"], "district": None, "special": False,
                     "y": dr[0] / n2, "n2": n2, "lean": ps[py][r["state"]] - ps[py]["US"], "inc": r["incumbency"],
                     "inc_source": "algara_amlani", "M": 0 if t % 4 == 0 else 1, "P": sitting_party(t, pres),
                     "source": "algara_amlani", "lag": lg[1] if lg else None, "lag_year": lg[0] if lg else None})
    return rows, skipped


def fit_rows():
    """One row per race both major parties contested in November: 2006-2024 from Cha, Kuriwaki and Snyder,
    every level; the Senate also 1982-2004 from MEDSL (medsl_senate_rows). A governor's row carries the state's
    last governor race (last_governor_race)."""
    cha = _load("cha/normalized/contests.json")["contests"]
    db = _load("downballot/normalized/pres_by_cd.json")["lean_inputs"]
    ps = presidential_shares()
    pres = presidents()
    gov = last_governor_index()
    rows, skipped = [], {}

    def skip(why):
        skipped[why] = skipped.get(why, 0) + 1
    for c in cha:
        t, L = c["year"], c["office"]
        if L not in LEVELS or t not in YEARS:
            continue
        if c["runoff"]:
            skip("runoff (the November round is not in this source)")
            continue
        cands = [a for a in c["candidates"] if a["votes"]]
        D = [a for a in cands if a["party"] == "D"]
        R = [a for a in cands if a["party"] == "R"]
        if len(D) != 1 or len(R) != 1:
            skip("not one Democrat and one Republican with votes")
            continue
        top2 = sorted(cands, key=lambda a: -a["votes"])[:2]
        if {a["party"] for a in top2} != {"D", "R"}:
            skip("a third candidate in the top two")
            continue
        py = last_pres_year(t)
        if L == "house":
            li = db.get(str(t), {})
            k = district_key(c["state"], c["district"], li)
            if k not in li or li[k]["pres_year"] != str(py):
                skip("no district presidential vote from before the election")
                continue
            lean = li[k]["two_party_D"] - ps[py]["US"]
        else:
            if c["state"] not in ps[py]:
                skip("no state presidential vote")
                continue
            lean = ps[py][c["state"]] - ps[py]["US"]
        inc = (1 if D[0]["inc"] == 1 else 0) - (1 if R[0]["inc"] == 1 else 0)
        n2 = D[0]["votes"] + R[0]["votes"]
        row = {"year": t, "level": L, "state": c["state"], "district": c["district"],
               "special": c["special"], "y": D[0]["votes"] / n2, "n2": n2, "lean": lean, "inc": inc,
               "inc_source": "cha", "M": 0 if t % 4 == 0 else 1, "P": sitting_party(t, pres), "source": "cha"}
        if L == "governor":
            lg = last_governor_race(gov, c["state"], t)
            row["lag"] = lg[1] if lg else None
            row["lag_year"] = lg[0] if lg else None
        rows.append(row)
    more, sk = medsl_senate_rows(ps, pres)
    gmore, gsk = aa_governor_rows(ps, pres, gov)
    for k, v in list(sk.items()) + list(gsk.items()):
        skipped[k] = skipped.get(k, 0) + v
    return rows + more + gmore, skipped


def fit_years(level, T):
    """The cycles a forecast for year T is fitted on: the level's even years before T, from FIT_FROM."""
    return list(range(FIT_FROM[level], T, 2))


# ----------------------------------------------------------------------------- fit
def ols(X, y):
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return beta, y - X @ beta


def fit(rows, level, years, national_from=None):
    """Stage one by OLS with a dummy per year; stage two, the year effects on the presidency terms. Governors
    carry one more term, the state's last governor race: b_lag * (lag - 1/2) (method D2-v2). With national_from
    (another level's fit on its own earlier cycles), stage two is not fitted here: the national swing's terms,
    their spread and (Z'Z)^-1 are that fit's (the House of 2008-2012 on the Senate's, the orchestrator 06:36,
    item 2), and stage one needs one cycle only."""
    lag = level == "governor"
    R = [r for r in rows if r["level"] == level and r["year"] in years and (not lag or r.get("lag") is not None)]
    ys = sorted({r["year"] for r in R})
    X = np.array([[1.0 if r["year"] == t else 0.0 for t in ys] + [r["lean"], r["inc"]]
                  + ([r["lag"] - 0.5] if lag else []) for r in R])
    y = np.array([r["y"] - 0.5 for r in R])
    beta, res = ols(X, y)
    a = dict(zip(ys, beta[:len(ys)]))
    bL, bI = beta[len(ys)], beta[len(ys) + 1]
    bG = float(beta[len(ys) + 2]) if lag else None
    s_e = float(np.sqrt((res ** 2).sum() / (len(y) - X.shape[1])))
    # the race's own error is wider where the race is expected to be close (the back-test shows it:
    # model/.. section 3 of data/congress/REPORT.md): s_e(x) = g0 + g1 * min(x, CAP), x = |fitted - 1/2|,
    # fitted by OLS of |residual| * sqrt(pi/2) on x (for a normal error, E|e| = s_e * sqrt(2/pi))
    x = np.minimum(np.abs(X @ beta), CAP)
    g, _ = ols(np.column_stack([np.ones_like(x), x]), np.abs(res) * math.sqrt(math.pi / 2))
    base = {"level": level, "years": ys, "n": len(R), "a": {t: float(a[t]) for t in ys}, "b_lean": float(bL),
            "b_inc": float(bI), "b_lag": bG, "lag": lag, "s_e": s_e, "g": [float(v) for v in g]}
    if national_from is not None:
        return dict(base, c=list(national_from["c"]), s_a=national_from["s_a"],
                    ZtZ_inv=national_from["ZtZ_inv"], national_from={"level": national_from["level"],
                                                                     "years": national_from["years"]})
    # stage two: a_t = c0 + c_mid M P + c_on (1-M) P + d
    Z = np.array([[1.0, (t % 4 != 0) * sitting_party(t, PRES), (t % 4 == 0) * sitting_party(t, PRES)]
                  for t in ys])
    av = np.array([a[t] for t in ys])
    c, d = ols(Z, av)
    dof = len(ys) - 3
    if dof < 1:
        raise ValueError(f"{len(ys)} cycles cannot fit the national swing's three terms with a residual")
    if np.linalg.matrix_rank(Z) < 3:
        raise ValueError("every one of these cycles had a president of the same party, so the national swing's "
                         "midterm and presidential-year terms cannot both be fitted")
    s_a = float(np.sqrt((d ** 2).sum() / dof))
    return dict(base, c=[float(v) for v in c], s_a=s_a, ZtZ_inv=np.linalg.inv(Z.T @ Z).tolist())


def national(m, t):
    """The forecast of year t's swing and its sd, from the fit's own cycles (all before t): the OLS prediction,
    sd = s_a sqrt(1 + z (Z'Z)^-1 z'), which counts both the swing's own spread around the national terms and
    the uncertainty of the terms fitted on few cycles. Reason: a fit on earlier cycles only (item 2 of
    2026-11-07 05:58); the sd of record before was the leave-one-cycle-out miss, which used later cycles."""
    P = sitting_party(t, PRES)
    z = np.array([1.0, (t % 4 != 0) * P, (t % 4 == 0) * P])
    a_hat = float(z @ np.array(m["c"]))
    sd = m["s_a"] * math.sqrt(1.0 + float(z @ np.array(m["ZtZ_inv"]) @ z))
    return a_hat, sd * m.get("k", 1.0)


def own_s_e(m):
    """The race's own sd as the forecast uses it: the fit's s_e times the calibration factor k (calibration)."""
    return m["s_e"] * m.get("k", 1.0)


def predict(m, r):
    a_hat, sd_a = national(m, r["year"])
    mean = 0.5 + a_hat + m["b_lean"] * r["lean"] + m["b_inc"] * r["inc"] + (m["b_lag"] * (r["lag"] - 0.5)
                                                                           if m["lag"] else 0.0)
    s_e = (m["g"][0] + m["g"][1] * min(abs(mean - 0.5), CAP)) * m.get("k", 1.0) if HETERO else own_s_e(m)
    sd = math.sqrt(sd_a ** 2 + s_e ** 2)
    return mean, sd, a_hat


# ----------------------------------------------------------------------------- distributions
def Phi(x):
    return 0.5 * (1.0 + math.erf(x / SQRT2))


def t4_cdf(x):
    """Student-t, 4 degrees of freedom, standard (scale 1)."""
    t2 = x * x
    return 0.5 + x * (t2 + 6.0) / (2.0 * (t2 + 4.0) ** 1.5)


def cdf(x, mean, sd, tails):
    z = (x - mean) / sd
    return Phi(z) if tails == "normal" else t4_cdf(z * SQRT2)        # t4 with sd matched: scale sd/sqrt2


def logpdf(x, mean, sd, tails):
    z = (x - mean) / sd
    if tails == "normal":
        return -0.5 * z * z - math.log(sd * math.sqrt(2 * math.pi))
    s = sd / SQRT2
    u = (x - mean) / s
    return math.log(3.0 / 8.0) - 2.5 * math.log(1 + u * u / 4.0) - math.log(s)


# ----------------------------------------------------------------------------- seats (MATH 4.2)
def swing_grid(sd_a, k=8.0, points=401):
    """A grid over the common swing d (deviation of a_t from its forecast), wide enough for any posterior."""
    return np.linspace(-k * sd_a, k * sd_a, points)


_erf = np.vectorize(math.erf)


def win_given_swing(mu, s_e, lam, grid):
    """P(seat won | common swing d) for y = mu + lam d + e, e ~ N(0, s_e^2)."""
    return 0.5 * (1.0 + _erf((mu + lam * grid - 0.5) / (s_e * SQRT2)))


def seat_dp(means, s_es, lams, grid):
    """dist[g, k] = P(the Democrats win exactly k of these seats | common swing grid[g]); seat i is won when
    mean_i + lam_i d + e_i > 1/2, e_i ~ N(0, s_e,i^2) independent given d (lam_i = 1 and s_e,i = s_e for the
    model's own seats; section 4 of data/congress/REPORT.md for 538's). Exact dynamic programming over seats."""
    dist = np.zeros((len(grid), len(means) + 1))
    dist[:, 0] = 1.0
    for mu, se, lam in zip(means, s_es, lams):
        q = win_given_swing(mu, se, lam, grid)[:, None]
        new = dist * (1 - q)
        new[:, 1:] += dist[:, :-1] * q
        dist = new
    return dist


def remove_seat(dist, q):
    """Take one seat (win chance q[g] at each grid point) back out of dist: the inverse of one DP step,
    run upward where q <= 1/2 and downward where q > 1/2 so that rounding errors shrink, not grow."""
    G, K = dist.shape
    out = np.zeros((G, K - 1))
    lo = q <= 0.5
    if lo.any():
        d, qq = dist[lo], q[lo][:, None]
        o = np.zeros((d.shape[0], K - 1))
        o[:, 0] = d[:, 0] / (1 - qq[:, 0])
        for k in range(1, K - 1):
            o[:, k] = (d[:, k] - qq[:, 0] * o[:, k - 1]) / (1 - qq[:, 0])
        out[lo] = o
    hi = ~lo
    if hi.any():
        d, qq = dist[hi], q[hi]
        o = np.zeros((d.shape[0], K - 1))
        o[:, K - 2] = d[:, K - 1] / qq
        for k in range(K - 2, 0, -1):
            o[:, k - 1] = (d[:, k] - (1 - qq) * o[:, k]) / qq
        out[hi] = o
    return np.clip(out, 0.0, 1.0)


def normal_weights(grid, mean, sd):
    w = np.exp(-0.5 * ((grid - mean) / sd) ** 2)
    return w / w.sum()


# ----------------------------------------------------------------------------- back-test
def _score(m, test, T):
    """Calibration of one fit's forecasts of year T's races: standardized residuals, coverage, log score."""
    stats = {"races": len(test)}
    zs = []
    for tails in ("normal", "t4"):
        cover = {0.5: 0, 0.8: 0, 0.95: 0}
        ls, near_pred = 0.0, 0.0
        for r in test:
            mean, sd, _ = predict(m, r)
            if tails == "normal":
                zs.append((r["y"] - mean) / sd)
            u = cdf(r["y"], mean, sd, tails)
            for q in cover:
                if abs(u - 0.5) <= q / 2:
                    cover[q] += 1
            ls += logpdf(r["y"], mean, sd, tails)
            near_pred += cdf(0.51, mean, sd, tails) - cdf(0.49, mean, sd, tails)
        stats[tails] = {"coverage": {str(q): cover[q] / len(test) for q in cover},
                        "mean_log_score": ls / len(test), "within_49_51_expected": near_pred}
    stats["z"] = zs
    stats["within_49_51_observed"] = sum(1 for r in test if abs(r["y"] - 0.5) < 0.01)
    a_hat, sd_a = national(m, T)
    fitted = FULL[m["level"]]["a"].get(T)
    # the year effect fitted in sample rests on the year's own races, so it carries their noise too, about
    # s_e^2 / races (an eleven-race governor year: as large as the national sd itself)
    noise = FULL[m["level"]]["s_e"] ** 2 / len(test)
    stats["national"] = {"forecast": a_hat, "sd": sd_a, "fitted_in_sample": fitted,
                         "z": (fitted - a_hat) / sd_a if fitted is not None else None,
                         "z_with_year_noise": (fitted - a_hat) / math.sqrt(sd_a ** 2 + noise) if fitted is not None
                         else None}
    return stats


def _test_rows(rows, L, T):
    return [r for r in rows if r["level"] == L and r["year"] == T and (L != "governor" or r.get("lag") is not None)]


def backtest(rows, window=None, calibrated=False):
    """Every year forecast from a fit on earlier cycles only: all of the level's cycles before it (window None:
    raw_model, the House of 2008-2012 on the Senate's national terms), or only the `window` cycles just before
    it. With calibrated, the forecasts of record: raw_model's sd times the calibration factor of the year's
    earlier scored years (calibration). A fit of its own national terms needs four cycles at least: the three
    terms and one degree of freedom for their spread."""
    out = {}
    for L in LEVELS:
        per_year, folds = {}, {}
        for T in range(FIT_FROM[L], 2025, 2):
            test = _test_rows(rows, L, T)
            if not test:
                continue
            if window:
                train = fit_years(L, T)
                train = train[-window:] if len(train) >= window else []
                if len(train) < K_MIN:
                    continue
                try:
                    m = fit(rows, L, train)
                except ValueError:
                    continue
            else:
                m, train = (year_model if calibrated else raw_model)(rows, L, T)
                if m is None:
                    continue
            folds[T] = {k: m[k] for k in ("b_lean", "b_inc", "b_lag", "s_e", "s_a", "c")}
            folds[T]["k"] = m.get("k", 1.0)
            if m.get("national_from"):
                folds[T]["national_from"] = m["national_from"]
            per_year[T] = _score(m, test, T)
            per_year[T]["cycles"] = len(train)
        out[L] = {"per_year": per_year, "folds": folds}
    return out


def by_cycles(bt, L, years=None):
    """The back-test pooled by the number of earlier cycles the fit had: z sd, coverage, log score, and the
    national swing's standardized misses."""
    g = {}
    for T, s in bt[L]["per_year"].items():
        if years and T not in years:
            continue
        g.setdefault(s["cycles"], []).append(s)
    out = {}
    for k, ss in sorted(g.items()):
        z = np.array([v for s in ss for v in s["z"]])
        n = len(z)
        cov = {q: sum(s["normal"]["coverage"][q] * s["races"] for s in ss) / n for q in ("0.5", "0.8", "0.95")}
        nz = [s["national"]["z"] for s in ss if s["national"]["z"] is not None]
        out[k] = {"years": sorted(T for T, s in bt[L]["per_year"].items() if s in ss), "races": n,
                  "z_sd": float(z.std()), "z_mean": float(z.mean()), "coverage": cov,
                  "mean_log_score": sum(s["normal"]["mean_log_score"] * s["races"] for s in ss) / n,
                  "national_z_rms": float(np.sqrt(np.mean(np.square(nz)))) if nz else None}
    return out


def pooled(bt, L, years=None):
    ss = [s for T, s in bt[L]["per_year"].items() if not years or T in years]
    z = np.array([v for s in ss for v in s["z"]])
    n = len(z)
    if not n:
        return None
    nz = [s["national"]["z"] for s in ss if s["national"]["z"] is not None]
    nzn = [s["national"]["z_with_year_noise"] for s in ss if s["national"].get("z_with_year_noise") is not None]
    return {"years": sorted(T for T in bt[L]["per_year"] if not years or T in years), "races": n,
            "z_sd": float(z.std()), "z_mean": float(z.mean()), "z_rms": float(np.sqrt(np.mean(z ** 2))),
            "national_z_rms_with_year_noise": float(np.sqrt(np.mean(np.square(nzn)))) if nzn else None,
            "coverage": {q: sum(s["normal"]["coverage"][q] * s["races"] for s in ss) / n for q in ("0.5", "0.8", "0.95")},
            "coverage_t4": {q: sum(s["t4"]["coverage"][q] * s["races"] for s in ss) / n for q in ("0.5", "0.8", "0.95")},
            "mean_log_score": sum(s["normal"]["mean_log_score"] * s["races"] for s in ss) / n,
            "national_z_rms": float(np.sqrt(np.mean(np.square(nz)))) if nz else None,
            "within_49_51": {"expected": sum(s["normal"]["within_49_51_expected"] for s in ss),
                             "observed": sum(s["within_49_51_observed"] for s in ss)}}


def house_on_senate_terms(rows):
    """The orchestrator's test (06:36, item 2): House 2014-2024 forecast with the national swing's terms from the
    Senate's fit on the Senate's earlier cycles, against the House's own; and with the House's own terms fitted on
    only its last 1, 2 or 3 cycles, as the House of 2008, 2010 and 2012 would be."""
    out = {}
    for scheme in ("own", "senate_terms", "senate_terms_1_cycle", "senate_terms_2_cycles", "senate_terms_3_cycles"):
        per = {}
        for T in range(2014, 2025, 2):
            test = _test_rows(rows, "house", T)
            hy = fit_years("house", T)
            if scheme.endswith("cycle") or scheme.endswith("cycles"):
                hy = hy[-int(scheme.split("_")[2]):]
            if scheme == "own":
                m = fit(rows, "house", hy)
            else:
                ms, _ = raw_model(rows, "senate", T)
                m = fit(rows, "house", hy, national_from=ms)
            per[T] = _score(m, test, T)
            per[T]["cycles"] = len(hy)
        out[scheme] = {"house": {"per_year": per}}
    return out


def backtest_seats(rows):
    """Each year from a fit on its earlier cycles: the forecast distribution of the Democrats' seats among
    the races both parties contested, against the seats they won; PIT = P(X < won) + P(X = won)/2."""
    out = {}
    for L in ("house", "senate"):
        res = {}
        for T in YEARS:
            test = [r for r in rows if r["level"] == L and r["year"] == T]
            m, _ = year_model(rows, L, T)
            if not test or m is None:
                continue
            means = [predict(m, r)[0] for r in test]
            _, sd_a = national(m, T)
            grid = swing_grid(sd_a)
            dist = (seat_dp(means, [own_s_e(m)] * len(means), [1.0] * len(means), grid)
                    * normal_weights(grid, 0.0, sd_a)[:, None]).sum(axis=0)
            won = sum(1 for r in test if r["y"] > 0.5)
            cum = np.cumsum(dist)
            k = np.arange(len(dist))
            lo, hi = int(np.searchsorted(cum, 0.1)), int(np.searchsorted(cum, 0.9))
            res[T] = {"races": len(test), "expected": float((k * dist).sum()), "interval_80": [lo, hi], "won": won,
                      "pit": float(cum[won - 1] if won > 0 else 0.0) + 0.5 * float(dist[won])}
        out[L] = res
    return out


def _fmt(x):
    if not x:
        return "none"
    return (f"{x['races']:5d} races, z sd {x['z_sd']:.3f} (mean {x['z_mean']:+.3f}), cover 50/80/95 "
            f"{x['coverage']['0.5']:.2f}/{x['coverage']['0.8']:.2f}/{x['coverage']['0.95']:.3f}, log score "
            f"{x['mean_log_score']:.3f}, national z rms {x['national_z_rms']:.2f}"
            + (f" ({x['national_z_rms_with_year_noise']:.2f} with the year effect's noise)"
               if x.get("national_z_rms_with_year_noise") is not None else "") if x["national_z_rms"] is not None
            else f"{x['races']:5d} races, z sd {x['z_sd']:.3f}")


# ----------------------------------------------------------------------------- computing p
RUN_UTC = cc.now_utc()
# the method's version: D2-v1 approved 2026-11-07 03:46 UTC; v2 (05:58, items 2 and 5) fits on earlier cycles
# only, and gives governors the state's last governor race (data/congress/REPORT.md section 2)
METHOD = {"house": "D2-v3", "senate": "D2-v3", "governor": "D2-v3 (with the last governor race)"}
# v3 (the orchestrator, 06:36): governors fitted from 1978 on Algara and Amlani's returns; the House of 2008-2012
# on the Senate's national terms; each level's sd calibrated on its earlier years (calibration)
K_MIN = 4                   # the fewest earlier cycles a fit needs (the back-test, REPORT.md section 2.3)
CAUCUS_D_LAST = {("ME", "KING"), ("VT", "SANDERS"), ("CT", "LIEBERMAN")}


def git_head():
    import subprocess
    out = subprocess.run(["git", "-C", REPO, "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
    return out.stdout.strip() or None


def model_source(year, level, m):
    yrs = m["years"]
    nf = m.get("national_from")
    return cc.source_block(f"the model's own forecast, method {METHOD[level]}, fitted to the {level} races of "
                           f"{yrs[0]}-{yrs[-1]} ({len(yrs)} cycle{'s' if len(yrs) > 1 else ''}, all before {year})"
                           + (f", with national terms from the Senate's earlier cycles ({nf['years'][0]}-"
                              f"{nf['years'][-1]})" if nf else ""),
                           "https://github.com/zwolk46/vote/blob/main/data/congress/REPORT.md",
                           RUN_UTC, None, mark="inferred",
                           note="the file's top-level \"model\" holds the fitted terms; no polls are used")


def model_mean(m, year, lean, inc, lag=None):
    a_hat, sd_a = national(m, year)
    mean = 0.5 + a_hat + m["b_lean"] * lean + m["b_inc"] * inc
    if m["lag"]:
        mean += m["b_lag"] * (lag - 0.5)
    return mean, sd_a


def seat_entry(c, m, year):
    """How a seat enters the control calculation. Returns (kind, value, note):
       ("model", mean, ...)    the model's forecast, with the common swing;
       ("inferred", mean, ...) the model's forecast for a structure it does not compute p for, marked;
       ("fixed", "D"|"R"|"non-D", ...) settled by who was on the ballot, known before the election."""
    b = c.get("ballot") or {}
    fi = c.get("forecast_inputs") or {}
    p = c["p"]
    st = c["place"]["state"]
    dcount = b.get("D", 0) + len(b.get("caucus_D", []))
    if p["value"] == 0.0 or (dcount == 0 and b.get("R", 0) == 0):
        party = None
        if dcount and not b.get("R"):
            return ("fixed", "D", "only Democratic candidates or an independent who caucuses with them on the ballot")
        if b.get("R") and not dcount:
            return ("fixed", "R", "no Democrat on the ballot")
        return ("fixed", party or "non-D", "one candidate on the ballot")
    if dcount == 0:
        return ("fixed", "non-D", "no Democrat on the ballot, nor an independent who caucuses with the Democrats "
                "(Nebraska's Osborn in 2024 and Utah's McMullin in 2022 said they would join neither party's "
                "caucus); for control only the Democrats' count matters, so the seat is not theirs whoever wins")
    if b.get("R", 0) == 0:
        return ("fixed", "D", "no Republican on the ballot")
    if p["value"] is None and not (p["not_computed"] or "").startswith("pending"):
        lean = fi.get("lean")
        why = p["not_computed"]
        if lean is None and fi.get("lean_same_day"):
            lean = fi["lean_same_day"]["value"]
            why = "the same day's presidential vote on these lines stands in for the missing earlier one"
        if lean is None:
            return ("fixed", None, "no input")
        mean, _ = model_mean(m, year, lean, fi.get("incumbency", 0))
        return ("inferred", mean, f"the model's two-way forecast, Democrat (or the caucusing independent) against "
                                  f"Republican, used for control only: {why}")
    return ("model", None, None)


def tie_swing(mu, se, lam, sd_a):
    """The common swing given the seat tied, y = 1/2, for y = mu + lam d + e: normal, with
    mean lam sd_a^2 (1/2 - mu) / sd^2 and sd sd_a s_e / sd, sd^2 = lam^2 sd_a^2 + s_e^2 (MATH 4.2)."""
    sd2 = lam ** 2 * sd_a ** 2 + se ** 2
    return lam * sd_a ** 2 * (0.5 - mu) / sd2, sd_a * se / math.sqrt(sd2)


def stage_two(entries, sd_a, pivots, grid_points=401):
    """For each modelled seat i: P(the other seats leave the Democrats exactly k | seat i tied), for each k in
    pivots (k counts fixed seats too), MATH 4.2. entries: [(index, kind, mean or fixed party, s_e,i, lam_i,
    alts)], alts the marginals [(mean, s_e, lam)] of each forecast whose p the seat records (the first is the
    seat's own entry): the other seats are the same for all of them, and only what a tie tells about the swing
    differs. Returns ({index: {"given_tie": [{k: P} per alt], "unconditional": {k: P}}}, seats, fixed_D)."""
    grid = swing_grid(sd_a, points=grid_points)
    h = grid[1] - grid[0]
    mod = [e for e in entries if e[1] in ("model", "inferred")]
    fixed_D = sum(1 for e in entries if e[1] == "fixed" and e[2] == "D")
    dist = seat_dp([e[2] for e in mod], [e[3] for e in mod], [e[4] for e in mod], grid)
    w0 = normal_weights(grid, 0.0, sd_a)
    out = {}
    for j, (idx, kind, mu, se, lam, alts) in enumerate(mod):
        if kind != "model":
            continue
        others = remove_seat(dist, win_given_swing(mu, se, lam, grid))
        res = {"given_tie": [], "unconditional": {k: float((others[:, k - fixed_D] * w0).sum())
                                                  if 0 <= k - fixed_D < others.shape[1] else 0.0 for k in pivots}}
        for (m_, s_, l_) in alts:
            cm, cs = tie_swing(m_, s_, l_, sd_a)
            if cs >= 3 * h:
                g, oth = grid, others
            else:
                # the swing given the tie is narrower than three grid steps: the other seats are counted afresh
                # on a fine grid around it (161 points over 8 sd either side)
                g = np.linspace(cm - 8 * cs, cm + 8 * cs, 161)
                rest = [e for i2, e in enumerate(mod) if i2 != j]
                oth = seat_dp([e[2] for e in rest], [e[3] for e in rest], [e[4] for e in rest], g)
            w = normal_weights(g, cm, cs)
            res["given_tie"].append({k: float((oth[:, k - fixed_D] * w).sum()) if 0 <= k - fixed_D < oth.shape[1]
                                     else 0.0 for k in pivots})
        out[idx] = res
    seats = (dist * w0[:, None]).sum(axis=0)
    return out, seats, fixed_D


# Two Senate specials of 2006-2024 that the November record and Cha, Kuriwaki and Snyder do not settle by
# themselves, each with the U.S. Senate's own words (pipeline/intake/party_divisions.py, 111th Congress):
OFF_DATE_SPECIALS = {
    # held before November: its winner holds the seat in November, which is not up
    (2010, "MA"): "U.S. Senate, Party Division, 111th Congress, note 4: \"Scott Brown (R) of Massachusetts, "
                  "elected January 19, 2010, was seated, replacing appointed Senator Paul Kirk (D).\"",
}
SAME_SEAT_SPECIALS = {
    # held the same day as the regular election for the same seat: it fills the weeks before the new Senate
    # meets, and only the regular election counts for control
    (2010, "IL"): "U.S. Senate, Party Division, 111th Congress, note 5: \"Mark Kirk (R) of Illinois, elected "
                  "November 2, 2010, was seated, replacing appointed Senator Roland Burris (D).\" The seat is "
                  "Illinois's class 3 seat, whose regular election was the same day (FEC, Federal Elections 2010: "
                  "\"Unexpired term\")",
}


def senate_not_up(year):
    """The seats not up in year t, each held by the winner of its latest election before t, counted by
    caucus. Winners from Cha, Kuriwaki and Snyder (2006 on; the deciding round, runoffs included); for a
    seat last elected before 2006, from MEDSL's U.S. Senate 1976-2024 (the most votes in that election).
    Class from the year: a regular election in 2006, 2012, 2018, 2024 is class 1; 2008, 2014, 2020 class 2;
    2010, 2016, 2022 class 3; a special's class is that of the year its term ends (next_up). Specials whose
    term ends at the new Congress (next_up = t) do not count; a special held earlier in year t
    (OFF_DATE_SPECIALS) holds its seat in November. Returns ({(state, class): (year, caucus, name, source
    key)}, the set of seats up)."""
    cha = _load("cha/normalized/contests.json")["contests"]

    def cls(y):
        return {2: 1, 4: 2, 0: 3}[y % 6]
    latest = {}
    up = set()
    classes = {}
    for c in cha:
        if c["office"] == "senate" and not c["special"] and c["year"] % 2 == 0:
            classes.setdefault(c["state"], set()).add(cls(c["year"]))
    for c in cha:
        if c["office"] != "senate" or c["state"] not in cc.STATES_50:
            continue
        if c["special"]:
            if not c.get("next_up") or c["next_up"] <= c["year"]:
                continue
            k = (c["state"], cls(c["next_up"]) if c["next_up"] % 2 == 0 else None)
            if k[1] not in classes.get(c["state"], ()):
                # a next_up that names a class the state does not have (Alabama's 2017 special says 2018):
                # the seat is the state's class whose regular election comes first after the special
                nxt = {cl: min(y for y in range(c["year"] + 1, c["year"] + 7) if y % 2 == 0 and cls(y) == cl)
                       for cl in classes.get(c["state"], ())}
                k = (c["state"], min(nxt, key=nxt.get))
        else:
            k = (c["state"], cls(c["year"]))
        before = c["year"] < year or (c["year"] == year and c["special"] and (year, c["state"]) in OFF_DATE_SPECIALS)
        if c["year"] == year and not before:
            up.add(k)
            continue
        if not before:
            continue
        w = [a for a in c["candidates"] if a["won"] == 1]
        if not w:
            continue
        if k not in latest or c["year"] >= latest[k][0]:
            last = w[0]["name"].split(",")[0].split()[-1]
            party = "D" if w[0]["party"] == "D" or (c["state"], last) in CAUCUS_D_LAST else \
                "R" if w[0]["party"] == "R" else "non-D"
            latest[k] = (c["year"], party, w[0]["name"], "cha")
    # seats last elected before Cha begins (2006): MEDSL's regular elections of the six years before t
    medsl = _load("medsl/normalized/senate.json")["contests"]
    for st, cl_set in classes.items():
        for cl in cl_set:
            k = (st, cl)
            if k in up or k in latest:
                continue
            past = [c for c in medsl if c["state"] == st and not c["special"] and year - 6 <= c["year"] < year
                    and cls(c["year"]) == cl]
            if not past:
                continue
            c = max(past, key=lambda c: c["year"])
            w = max(c["candidates"], key=lambda a: a["votes"] or 0)
            labels = " ".join(w["parties"]).upper()
            party = "D" if "DEMOCRAT" in labels else "R" if "REPUBLICAN" in labels else "non-D"
            latest[k] = (c["year"], party, w["name"], "medsl_senate")
    held = {k: v for k, v in latest.items() if k not in up}
    return held, up


def division_check(d, level, year, held):
    """Seats the Democrats (with the independents who caucus with them) and the Republicans won, counted
    from Cha, Kuriwaki and Snyder's winners (the deciding round), plus the seats not up, against the
    division the new Congress opened with (pipeline/intake/party_divisions.py)."""
    div = _load("divisions/normalized/divisions.json")
    n = str((year - 1788) // 2 + 1)
    cha = _load("cha/normalized/contests.json")["contests"]
    won = {"D": 0, "R": 0, "other": 0, "no winner in the check source": 0}
    for c in d["contests"]:
        st2 = c.get("stage_two") or {}
        if not st2.get("of"):
            continue
        st, dist = c["place"]["state"], c["place"]["district"]
        cs = [x for x in cha if x["year"] == year and x["office"] == level and x["state"] == st
              and bool(x["special"]) == bool(c["special"])
              and (level == "senate" or (x["district"] or "") in (dist, "01" if dist == "AL" else dist))]
        if level == "senate" and not cs:
            # one source calls it a special and the other does not (Arizona 2020): the state's only contest
            alt = [x for x in cha if x["year"] == year and x["office"] == level and x["state"] == st]
            cs = alt if len(alt) == 1 else cs
        w = [a for x in cs for a in x["candidates"] if a["won"] == 1]
        if not w:
            won["no winner in the check source"] += 1
            continue
        last = w[-1]["name"].split(",")[0].split()[-1]
        won["D" if w[-1]["party"] == "D" or (st, last) in CAUCUS_D_LAST else "R" if w[-1]["party"] == "R"
            else "other"] += 1
    out = {"of": f"the {n}th Congress at its opening", "won_in_this_file": won}
    if level == "senate":
        nu = {"D": sum(1 for v in held.values() if v[1] == "D"), "R": sum(1 for v in held.values() if v[1] == "R"),
              "other": sum(1 for v in held.values() if v[1] == "non-D")}
        out["not_up"] = nu
        out["counted"] = {"D_caucus": won["D"] + nu["D"], "R": won["R"] + nu["R"], "other": won["other"] + nu["other"]}
        x = div["senate"].get(n)
        out["division"] = ({"D": x["D"], "R": x["R"], "other": x["other"], "vacant": x["vacant"], "from": x["from"],
                            "notes": x["footnotes"]} if x else None)
        if x:
            # the page's "other" senators of 2007-2025 are independents who caucused with the Democrats (its
            # notes say so); a winner counted "other" here is one who did not run as a Democrat or a
            # Republican and does not caucus with the Democrats (Murkowski, a write-in in 2010)
            out["agrees"] = (out["counted"]["D_caucus"] == x["D"] + x["other"]
                             and out["counted"]["R"] + out["counted"]["other"] == x["R"])
        out["source"] = "senate_gov"
    else:
        out["counted"] = {"D": won["D"], "R": won["R"], "other": won["other"]}
        x = div["house"].get(n)
        out["division"] = {"D": x["D"], "R": x["R"], "other": x["other"], "note": x["footnote"]} if x else None
        if x:
            out["agrees"] = out["counted"]["D"] == x["D"] and out["counted"]["R"] == x["R"]
        out["source"] = "house_history"
    return out


# FiveThirtyEight's published forecasts (pipeline/intake/fivethirtyeight_checking_our_work.py) come first
# where the race has one (the orchestrator, 2026-11-07 03:46: "a reachable published forecast comes first,
# with ours as the check"; 04:12, and 04:20 for the rule below). Its mean is the Democrat's projected share of
# the two leading parties' projected vote; its sd is the one a normal needs to give its chance,
# sd = (mean - 1/2) / Phi^-1(chance), marked inferred. It is kept where p's estimated relative error is
# under 20%, no chance is exactly 0 or 1, and other candidates hold under 1% of the chance; otherwise ours comes
# first and 538's forecast stays beside it as the check, with the reason.
FTE_MAX_REL_ERROR = 0.20  # 538's forecast is kept where p's estimated relative error is under 20% (05:58, item 3)
FTE_OTHERS = 0.01         # and where other candidates hold under 1% of the chance (the orchestrator, 04:20)
FTE = None


def Phi_inv(q):
    lo, hi = -12.0, 12.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if Phi(mid) < q:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def _last(name):
    """A candidate's last name, for matching across sources: "Cardin, Ben" and "Benjamin L. Cardin" give
    "cardin"; accents dropped, and text decoded twice by mistake (538's "LujÃ¡n") put right."""
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


def fte_versions(c, level, year):
    """538's versions for contest c, in the repository's order, or (None, why)."""
    global FTE
    if FTE is None:
        FTE = _load("fivethirtyeight/normalized/checking_our_work_congress.json") or {"races": {}}
    st, dist = c["place"]["state"], c["place"]["district"]
    if level == "house":
        dist = "01" if dist == "AL" else dist
    k = f"{level}|{year}|{st}|{dist or '-'}|{1 if c['special'] else 0}"
    r = FTE["races"].get(k)
    if r is None and level != "house":
        alt = [v for kk, v in FTE["races"].items() if kk.startswith(f"{level}|{year}|{st}|")]
        r = alt[0] if len(alt) == 1 else None
    if r is None:
        return None
    order = FTE["versions_order"][level][str(year)]
    return [(v, r["versions"][v]) for v in order if v in r["versions"]]


def fte_forecast(c, level, year, version, f):
    """One 538 version as a forecast entry, with the implied sd, or the reason it cannot be used."""
    by = {a["party"]: a for a in f["candidates"]}
    D, R = by.get("D"), by.get("R")
    if D is None and by.get("I") and (c["place"]["state"], _last(by["I"]["name"] or "").upper()) in CAUCUS_D_LAST:
        D = by["I"]     # Sanders, King: the independent who caucuses with the Democrats takes the Democrat's place
    entry = {"by": "538", "published": True, "version": version, "method": None,
             "share": None, "chance": {a["party"]: a["chance"] for a in f["candidates"]},
             "p_published": None, "convention": None, "as_of": f["as_of"], "source": level + "_538",
             "unusable": None, "unusable_kind": None}
    if f["dated_election_day"]:
        entry["note"] = "the file's only forecast for the race is dated Election Day"
    tp = c.get("two_party") or {}
    names = [_last(x) for x in tp.get("candidates", [])]
    for a in (D, R):
        if a and a.get("name"):
            ln = _last(a["name"])
            if names and not any(difflib.SequenceMatcher(None, ln, n).ratio() >= 0.8 or ln in n or n in ln
                                 for n in names):
                entry["unusable"] = f"538's {a['party']} candidate ({a['name']}) is not one of the two leading candidates here"
                entry["unusable_kind"] = "candidate not matched"
                return entry
    if not D or not R:
        entry["unusable"], entry["unusable_kind"] = "538's forecast has no Democrat or no Republican", "no D or R"
        return entry
    if D["share"] is None or R["share"] is None:
        entry["unusable"], entry["unusable_kind"] = ("538's file gives its chance but not its projected share",
                                                     "chance only, no share")
        return entry
    mean = D["share"] / (D["share"] + R["share"])
    others = 1 - D["chance"] - R["chance"]
    q = D["chance"] / (D["chance"] + R["chance"]) if (D["chance"] + R["chance"]) > 0 else None
    entry["share"] = {"mean": mean, "sd": None, "tails": "normal", "of": "Democrat, two-party",
                      "sd_from": "implied by 538's chance under a normal: sd = (mean - 1/2) / Phi^-1(chance); inferred"}
    if D["chance"] in (0.0, 1.0) or R["chance"] in (0.0, 1.0):
        entry["unusable"], entry["unusable_kind"] = "538's chance is exactly 0 or 1, which no sd gives", "chance 0 or 1"
        return entry
    if others >= FTE_OTHERS:
        entry["unusable"] = (f"538's chance gives {others:.1%} to someone else (a third candidate or a runoff), "
                             "so the two-way sd cannot be read from it")
        entry["unusable_kind"] = "others hold 1% or more of the chance"
        return entry
    if (mean - 0.5) * (q - 0.5) <= 0:
        entry["unusable"], entry["unusable_kind"] = ("538's mean and chance fall on different sides of even, which no "
                                                     "normal gives", "mean and chance on different sides")
        return entry
    z = Phi_inv(q)
    sd = (mean - 0.5) / z
    # the implied sd's relative error (the orchestrator, 04:20): from the chance's sampling error, sqrt(q(1-q)/N)
    # with N the simulation runs its steps imply, carried through Phi^-1 at both ends rather than linearized
    # (an end at 0 or 1 is an infinite error); and from the rounding of the printed shares
    N = FTE["simulations"][level][str(year)].get(version)
    if N:
        dq = math.sqrt(q * (1 - q) / N)
        ends = [q - dq, q + dq]
        rel_q = (math.inf if min(ends) <= 0 or max(ends) >= 1 else
                 max(abs(Phi_inv(e) - z) for e in ends) / abs(z))
        entry["simulations"] = N
        entry["simulations_mark"] = "inferred: the step its chances move in"
    else:
        rel_q = 0.0
        entry["simulations"] = None
        entry["simulations_mark"] = "no fixed step in the chances: taken as exact"
    dec = FTE["share_decimals"][level][str(year)].get(version, 5)
    d_share = 0.5 * 10 ** -(dec + 2)        # half the last printed digit, in share
    rel_m = d_share / abs(mean - 0.5)
    rel = math.sqrt(rel_q ** 2 + rel_m ** 2)
    # p's relative error (the orchestrator, 05:58, item 3: the reader sees p). p = phi(z) / (2n sd) with
    # z = Phi^-1(chance) and sd = (mean - 1/2) / z, so an error in the chance moves p by |z^2 - 1| times its
    # relative error in z (= the sd's), while the mean's rounding moves sd alone, with z fixed, and p by its own
    # relative size (M2 3.9)
    rel_p = math.sqrt(((z * z - 1) * rel_q) ** 2 + rel_m ** 2) if not math.isinf(rel_q) else math.inf
    entry["sd_relative_error"] = None if math.isinf(rel) else rel
    entry["p_relative_error"] = None if math.isinf(rel_p) else rel_p
    entry["z"] = z
    entry["share"]["sd"] = sd
    if rel_p >= FTE_MAX_REL_ERROR:
        entry["unusable"] = (f"p's estimated error under 538's implied sd is {'beyond measure' if math.isinf(rel_p) else f'{rel_p:.0%}'} "
                             f"(z = {z:.2f}; 538's chance rests on {N:,} simulation runs, and its mean is "
                             f"{abs(mean - 0.5):.3f} from even), at or above the 20% allowed" if N else
                             f"p's estimated error under 538's implied sd is {rel_p:.0%}, at or above the 20% allowed")
        entry["unusable_kind"] = "p's error 20% or more"
    return entry


def is_pending(c):
    """A contest whose p this script sets: pending from pipeline/intake/build_congress.py, or set here before."""
    p = c.get("p") or {}
    return (p.get("not_computed") or "").startswith("pending") or p.get("computed_by") == "pipeline/chambers.py"


def raw_model(rows, level, year):
    """The model's own fit for year t, on its earlier cycles only, before calibration; (None, cycles) when there
    are too few. The House with fewer than K_MIN earlier cycles of its own (2008-2012) but at least one takes the
    national swing's terms from the Senate's fit on the Senate's earlier cycles (the orchestrator, 06:36, item 2:
    the back-test on 2014-2024 keeps z sd and coverage within a few points of the House's own; REPORT 2.3)."""
    fy = [t for t in fit_years(level, year) if any(r["level"] == level and r["year"] == t for r in rows)]
    try:
        if len(fy) >= K_MIN:
            return fit(rows, level, fy), fy
        if level == "house" and fy:
            ms, _ = raw_model(rows, "senate", year)
            if ms is not None:
                return fit(rows, level, fy, national_from=ms), fy
    except ValueError:
        pass
    return None, fy


# CALIBRATION (the orchestrator, 06:36, item 3): each level's forecast sd is multiplied by k, the root mean square
# of the standardized errors z = (y - mean) / sd of the level's earlier years, each year forecast from its own
# earlier cycles (raw_model), once at least CAL_MIN such years are scored. Reason: a forecast wider than the record
# supports understates p (law 1a); the back-test (REPORT 2.4) shows k improves the log score at every level, and
# a separate factor for the national term does not. A year with fewer scored years before it keeps k = 1.
CAL_MIN = 3
_CAL = {}


def _scored(rows, level):
    """{year: [z of each race]} for every year the level's raw_model forecasts, cached."""
    if level not in _CAL:
        out = {}
        for T in range(FIT_FROM[level], 2025, 2):
            test = _test_rows(rows, level, T)
            m, _ = raw_model(rows, level, T)
            if m is None or not test:
                continue
            out[T] = [(r["y"] - mu) / sd for r in test for mu, sd, _ in [predict(m, r)]]
        _CAL[level] = out
    return _CAL[level]


def calibration(rows, level, year):
    sc = _scored(rows, level)
    yrs = [t for t in sorted(sc) if t < year]
    if len(yrs) < CAL_MIN:
        return {"k": 1.0, "years": yrs, "races": sum(len(sc[t]) for t in yrs),
                "note": f"not calibrated: {len(yrs)} earlier year(s) scored out of sample, {CAL_MIN} needed"}
    zs = [z for t in yrs for z in sc[t]]
    return {"k": math.sqrt(sum(z * z for z in zs) / len(zs)), "years": yrs, "races": len(zs),
            "note": "k = the root mean square of z = (y - mean) / sd over these earlier years' races, each year "
                    "forecast from its own earlier cycles"}


def year_model(rows, level, year):
    """The model's own forecast for year t, of record: raw_model, its sd calibrated (calibration)."""
    m, fy = raw_model(rows, level, year)
    if m is None:
        return None, fy
    cal = calibration(rows, level, year)
    m = dict(m, k=cal["k"], calibration=cal)
    return m, fy


# NEAR-TIE CALIBRATION (the orchestrator, 2026-11-07 07:04, round 4; D3's rule of #31). The back-test found more
# races finishing within 49-51% than the forecasts expected (House 113 against 89.3, Senate 30 against 21.6), which
# k cannot reach: it moves the spread, not the shape. So the forecast's density within NEAR_W of 1/2 is multiplied
# by a factor F and the forecast renormalized, f_cal(y) = f(y) h(y) / Z with h = F within the window, 1 outside,
# and Z = 1 + (F - 1) q, q the forecast's own chance of the window. p, the density at 1/2, is then multiplied by
# F / Z. F is fitted on earlier years only: seen over expected within the window in the level's earlier years'
# out-of-sample forecasts (year_model), solved exactly (the sum of F q / Z equals the count seen). A level takes its
# own F when those years expected NEAR_MIN_EXPECTED or more near-ties, else the F of every level's earlier years
# pooled, else none (D3's rule, the orchestrator 07:37). The second scheme the orchestrator named, a factor by band
# of |mean - 1/2|, takes the band's own F (by level, else pooled over levels) and none where the band has too few
# expected, so that no safe seat's p is raised without support at its distance. A scheme is adopted for a level only
# if, on the years it reaches, it raises the mean log score and brings the count within 49-51% nearer the count
# seen (near_tie_test, backtest.json "near_tie"); of two that do, the better log score.
# Reason: about 20% too few near-even finishes means p near even is about 20% low, which understates exactly the
# races law 1a says the site must show.
NEAR_W = 0.01
NEAR_MIN_EXPECTED = 30
NEAR_BANDS = (0.0, 0.05, 0.10)
NEAR_NOTE = "calibrated to earlier years' near-ties"
NEAR_WINDOWS = (0.01, 0.02, 0.05)
_NEAR = {}


def near_q(mean, sd, tails="normal", w=NEAR_W):
    """The forecast's chance of finishing within w of one half."""
    return cdf(0.5 + w, mean, sd, tails) - cdf(0.5 - w, mean, sd, tails)


def near_band(mean):
    d = abs(mean - 0.5)
    return max(i for i, b in enumerate(NEAR_BANDS) if d >= b)


def _near_scored(rows):
    """{(level, year): [(mean, sd, y)]}: every year's out-of-sample forecasts of record (year_model), cached."""
    if "scored" not in _NEAR:
        out = {}
        for L in LEVELS:
            for T in range(FIT_FROM[L], 2025, 2):
                test = _test_rows(rows, L, T)
                m, _ = year_model(rows, L, T)
                if m is None or not test:
                    continue
                out[(L, T)] = [(mu, sd, r["y"]) for r in test for mu, sd, _ in [predict(m, r)]]
        _NEAR["scored"] = out
    return _NEAR["scored"]


def _solve_factor(qs, seen):
    """F with sum(F q / (1 + (F - 1) q)) = seen: the factor that makes the window's expected count the seen one."""
    lo, hi = 1e-3, 50.0
    for _ in range(200):
        F = (lo + hi) / 2
        lo, hi = (F, hi) if sum(F * q / (1 + (F - 1) * q) for q in qs) < seen else (lo, F)
    return (lo + hi) / 2


def _near_counts(rows, year, key):
    """{group: [window chances, seen, {level: years}]} over every level's scored years before `year`."""
    g = {}
    for (L, T), rs in _near_scored(rows).items():
        if T >= year:
            continue
        for mu, sd, y in rs:
            k = key(L, mu)
            if k is None:
                continue
            e = g.setdefault(k, [[], 0, {}])
            e[0].append(near_q(mu, sd))
            e[1] += abs(y - 0.5) < NEAR_W
            e[2].setdefault(L, set()).add(T)
    return g


def near_tie_factor(rows, level, year, mean, scheme):
    """The near-tie factor for a forecast of `level` in `year` with this mean, under scheme "level" or "band":
    {"factor", "of", "fitted_on", "expected", "seen"}; factor 1 with "of" null where the fitting years have too
    few expected near-ties."""
    b = near_band(mean) if scheme == "band" else None
    ck = ("factor", scheme, year, level, b)
    if ck in _NEAR:
        return _NEAR[ck]
    cc_ = ("counts", scheme, year)
    if cc_ not in _NEAR:
        if scheme == "level":
            _NEAR[cc_] = (_near_counts(rows, year, lambda L, mu: L), _near_counts(rows, year, lambda L, mu: "all"))
        else:
            _NEAR[cc_] = (_near_counts(rows, year, lambda L, mu: (L, near_band(mu))),
                          _near_counts(rows, year, lambda L, mu: near_band(mu)))
    own, pool = _NEAR[cc_]
    band_txt = ""
    if scheme == "band":
        band_txt = f", |mean - 1/2| from {NEAR_BANDS[b]:.2f}" + (f" to {NEAR_BANDS[b + 1]:.2f}"
                                                                  if b + 1 < len(NEAR_BANDS) else " up")
    out = {"factor": 1.0, "of": None, "fitted_on": {}, "expected": None, "seen": None}
    for groups, k, of in ((own, level if scheme == "level" else (level, b), f"the {level}'s own earlier years{band_txt}"),
                          (pool, "all" if scheme == "level" else b, f"every level's earlier years pooled{band_txt}")):
        e = groups.get(k)
        if e and sum(e[0]) >= NEAR_MIN_EXPECTED:
            out = {"factor": _solve_factor(e[0], e[1]), "of": of,
                   "fitted_on": {L_: sorted(ys) for L_, ys in sorted(e[2].items())}, "expected": sum(e[0]),
                   "seen": e[1]}
            break
    _NEAR[ck] = out
    return out


def _near_score(rows, level, scheme, years):
    """The level's out-of-sample forecasts of `years`, scored with the near-tie scheme (or none): mean log score,
    coverage, and expected against seen within 1, 2 and 5 points of one half."""
    n, ls, cov = 0, 0.0, [0, 0, 0]
    win = {w: [0.0, 0] for w in NEAR_WINDOWS}
    for (L, T), rs in sorted(_near_scored(rows).items()):
        if L != level or T not in years:
            continue
        for mu, sd, y in rs:
            F = 1.0 if scheme is None else near_tie_factor(rows, L, T, mu, scheme)["factor"]
            q1 = near_q(mu, sd)
            Z = 1 + (F - 1) * q1
            inside = abs(y - 0.5) < NEAR_W
            n += 1
            ls += logpdf(y, mu, sd, "normal") + (math.log(F) if inside else 0.0) - math.log(Z)
            base = Phi((y - mu) / sd)
            extra = (F - 1) * max(0.0, Phi((min(y, 0.5 + NEAR_W) - mu) / sd) - Phi((0.5 - NEAR_W - mu) / sd))
            u = (base + extra) / Z
            for i, c_ in enumerate((0.5, 0.8, 0.95)):
                cov[i] += abs(u - 0.5) <= c_ / 2
            for w in NEAR_WINDOWS:
                win[w][0] += (near_q(mu, sd, w=w) + (F - 1) * q1) / Z
                win[w][1] += abs(y - 0.5) < w
    return {"races": n, "mean_log_score": ls / n if n else None,
            "coverage": {q: c_ / n for q, c_ in zip(("0.5", "0.8", "0.95"), cov)} if n else None,
            "within": {f"{50 - round(w * 100)}-{50 + round(w * 100)}%": {"expected": v[0], "seen": v[1]}
                       for w, v in win.items()}}


def near_tie_test(rows):
    """The orchestrator's test (07:04): both schemes against none, on the years either reaches, by level; and the
    rule of record, {level: scheme or None}."""
    if "test" in _NEAR:
        return _NEAR["test"]
    out = {"window": f"{50 - round(NEAR_W * 100)}-{50 + round(NEAR_W * 100)}%", "min_expected": NEAR_MIN_EXPECTED,
           "bands": list(NEAR_BANDS), "by_level": {}, "adopted": {}}
    for L in LEVELS:
        yrs = sorted(T for (L_, T) in _near_scored(rows) if L_ == L)
        reach = [T for T in yrs if any(near_tie_factor(rows, L, T, mu, sch)["of"]
                                       for sch in ("level", "band") for mu, _, _ in _near_scored(rows)[(L, T)])]
        res = {"years": reach, "none": _near_score(rows, L, None, reach)}
        for sch in ("level", "band"):
            res[sch] = _near_score(rows, L, sch, reach)
        res["factors_by_year"] = {str(T): {"level": near_tie_factor(rows, L, T, 0.5, "level"),
                                           "band": [near_tie_factor(rows, L, T, 0.5 + b + 1e-9, "band")
                                                    for b in NEAR_BANDS]} for T in yrs}
        best = None
        k49 = f"{50 - round(NEAR_W * 100)}-{50 + round(NEAR_W * 100)}%"
        if reach:
            b0 = res["none"]
            for sch in ("level", "band"):
                r = res[sch]
                better_ls = r["mean_log_score"] > b0["mean_log_score"]
                nearer = abs(r["within"][k49]["expected"] - r["within"][k49]["seen"]) < \
                    abs(b0["within"][k49]["expected"] - b0["within"][k49]["seen"])
                r["improves"] = bool(better_ls and nearer)
                if r["improves"] and (best is None or r["mean_log_score"] > res[best]["mean_log_score"]):
                    best = sch
        res["adopted"] = best
        out["by_level"][L] = res
        out["adopted"][L] = best
    _NEAR["test"] = out
    return out


def near_tie(rows, level, year, mean, sd, tails):
    """The near-tie calibration of record for one forecast: None where the level has none adopted, or its factor
    is 1; else {"factor", "multiplier" (F / Z, what p is multiplied by), "window", "of", "fitted_on", "what"}."""
    sch = near_tie_test(rows)["adopted"].get(level)
    if not sch:
        return None
    f = near_tie_factor(rows, level, year, mean, sch)
    if not f["of"]:
        return None
    F = f["factor"]
    return {"factor": F, "multiplier": F / (1 + (F - 1) * near_q(mean, sd, tails)),
            "window": f"{50 - round(NEAR_W * 100)}-{50 + round(NEAR_W * 100)}%", "scheme": sch, "of": f["of"],
            "fitted_on": f["fitted_on"], "expected": f["expected"], "seen": f["seen"],
            "what": "seen over expected within the window in the fitting years' out-of-sample forecasts: the "
                    "forecast's density there is multiplied by factor and the forecast renormalized, so p is "
                    "multiplied by multiplier = factor / (1 + (factor - 1) q), q the forecast's chance of the window"}


def too_few(level, year, fy):
    if len(fy) >= K_MIN:
        return (f"the model's own forecast is fitted on earlier cycles only; its sources hold {len(fy)} {level} cycles "
                f"before {year} ({fy[0]}-{fy[-1]}), but every one had a president of the same party, so the national "
                f"swing's midterm and presidential-year terms cannot both be fitted")
    first = {"house": "the House's from 2006 (The Downballot's district presidential vote begins on the 2006 lines)",
             "senate": "the Senate's from 1982 (MEDSL)",
             "governor": "the governors' from 1978 (Algara and Amlani's county returns before 2006, with the "
                         "presidential vote from MEDSL and the president from the National Archives, both from 1976)"}[level]
    if level == "house":
        return (f"the model's own forecast is fitted on earlier cycles only: {K_MIN} of the House's own, or at least "
                f"one with the national swing's terms from the Senate's earlier cycles; its sources hold {len(fy)} "
                f"before {year} ({first})")
    return (f"the model's own forecast is fitted on earlier cycles only and needs {K_MIN} of them; its sources hold "
            f"{len(fy)} before {year} ({first})")


def compute(year):
    """Fill forecasts, p and control for data/<level>/<year>.json, in place."""
    from core import p_contest
    commit = git_head()
    rows, _ = fit_rows()
    for level in LEVELS:
        path = os.path.join(REPO, "data", level, f"{year}.json")
        if year not in file_years(level):
            continue
        d = cc.read_json(path)
        m, fy = year_model(rows, level, year)
        if m:
            a_hat, sd_a = national(m, year)
            sd = math.sqrt(sd_a ** 2 + own_s_e(m) ** 2)
        for c in d["contests"]:
            fi = c.get("forecast_inputs")
            if not is_pending(c):
                if c["p"]["value"] is None and not c["forecasts"]:
                    # p is not computed here (a runoff, ranked choice, a missing input), but 538's forecast
                    # is kept in the record all the same
                    c["forecasts"] = [fte_forecast(c, level, year, v, f) for v, f in (fte_versions(c, level, year) or [])]
                continue
            n = c["two_party"]["n_other_voters"]
            own, own_p, own_missing = [], [], None
            lag = None
            if level == "governor":
                lg = fi.get("last_governor_race")
                lag = lg["share_D"] if lg else None
            if m is None:
                own_missing = too_few(level, year, fy)
            elif level == "governor" and lag is None:
                own_missing = fi.get("last_governor_race_missing") or "no earlier governor race in the state"
            else:
                mean, _ = model_mean(m, year, fi["lean"], fi["incumbency"], lag)
                src = model_source(year, level, m)
                own = [{"by": "the model's own", "published": False, "method": METHOD[level],
                        "share": {"mean": mean, "sd": sd, "tails": t, "of": "Democrat, two-party"},
                        "p_published": None, "convention": None, "as_of": c["date"], "source": src}
                       for t in ("normal", "t4")]
                for t_, f in zip(("normal", "t4"), own):
                    r_ = p_contest(n, mean, sd, tails=t_)
                    e_ = {"under": f"the model's own ({METHOD[level]}), " +
                          ("normal" if t_ == "normal" else "t4 with the same sd"),
                          "value": r_["p"], "event": r_["event"], "method": r_["method"], "f_half": r_["f_half"],
                          "_f": f}
                    nt = near_tie(rows, level, year, mean, sd, t_)
                    if nt:
                        # the near-tie calibration (round 4): p, its event and f(1/2) times the multiplier
                        f["calibration"] = nt
                        e_["value_uncalibrated"] = r_["p"]
                        e_["value"], e_["event"], e_["f_half"] = (r_["p"] * nt["multiplier"],
                                                                  r_["event"] * nt["multiplier"],
                                                                  r_["f_half"] * nt["multiplier"])
                        e_["under"] += f", {NEAR_NOTE}"
                    own_p.append(e_)
            fte = [fte_forecast(c, level, year, v, f) for v, f in (fte_versions(c, level, year) or [])]
            tally = None
            if fte:
                tally = FTE_USED.setdefault((year, level), {"races": 0, "first": 0, "fallback": {}})
                tally["races"] += 1
            first = fte[0] if fte and fte[0]["unusable"] is None else None
            fte_p = []
            for e in fte:
                if e["unusable"] is None:
                    r5 = p_contest(n, e["share"]["mean"], e["share"]["sd"], tails="normal")
                    fte_p.append({"under": f"538 ({e['version']}), normal with the implied sd", "value": r5["p"],
                                  "event": r5["event"], "method": r5["method"], "f_half": r5["f_half"],
                                  "sd": e["share"]["sd"], "_f": e})
            if tally:
                if first:
                    tally["first"] += 1
                else:
                    kd = fte[0].get("unusable_kind") or fte[0]["unusable"]
                    tally["fallback"][kd] = tally["fallback"].get(kd, 0) + 1
            if first:
                c["forecasts"] = fte + own
                head, rest = fte_p[0], fte_p[1:] + own_p
                head["under"] = (f"538 ({first['version']}), normal with the sd implied by its chance (inferred); "
                                 f"538 published first" + (", the model's own beside it as the check" if own else
                                                           f"; the model's own is not computed ({own_missing})"))
            elif own:
                c["forecasts"] = own + fte
                head, rest = own_p[0], own_p[1:] + fte_p
                if fte:
                    head["under"] += f"; 538's forecast stands beside it as the check ({fte[0]['unusable']})"
            else:
                c["forecasts"] = fte
                c["p"] = {"value": None, "event": None, "under": None, "computed_by": "pipeline/chambers.py",
                          "commit": commit, "not_computed": own_missing + (
                              f"; 538's forecast stands beside it but cannot give p ({fte[0]['unusable']})" if fte
                              else "; no published forecast for the race is reachable"), "reason": None}
                continue
            for e in [head] + rest:
                e["of_forecast"] = c["forecasts"].index(e.pop("_f"))
            c["p"] = {"value": head["value"], "event": head["event"], "under": head["under"],
                      "computed_by": "pipeline/chambers.py", "commit": commit, "not_computed": None, "reason": None,
                      "method": head["method"], "f_half": head["f_half"], "n": n,
                      "of_forecast": head["of_forecast"], "alongside": rest}
            if "sd" in head:
                c["p"]["sd"] = head["sd"]
            if "value_uncalibrated" in head:
                c["p"]["value_uncalibrated"] = head["value_uncalibrated"]
        if any(f.get("by") == "538" for c in d["contests"] for f in c.get("forecasts") or []):
            d["sources"][f"{level}_538"] = FTE["source"][level]
        if m and level in ("house", "senate"):
            control(d, level, year, m, sd_a, commit)
        elif level in ("house", "senate"):
            for c in d["contests"]:
                why = not_in_control(c, level, year)
                c["stage_two"] = ({"of": None, "inputs": {}, "source": None, "note": why} if why else
                                  {"of": "House control" if level == "house" else "Senate control", "inputs": {},
                                   "source": None, "note": "control not computed: the chamber stage needs the "
                                   "model's common swing, and " + too_few(level, year, fy)})
            d["chamber"] = {"of": "House control" if level == "house" else "Senate control", "not_computed":
                            "the chamber stage needs the model's common swing, and " + too_few(level, year, fy),
                            "commit": commit}
            d["chamber"]["check"] = division_check(d, level, year, senate_not_up(year)[0] if level == "senate" else {})
            divs = _load("divisions/normalized/divisions.json")["sources"]
            d["sources"][d["chamber"]["check"]["source"]] = divs[d["chamber"]["check"]["source"]]
        if m:
            d["model"] = {"method": METHOD[level],
                          "what": "the model's own forecast (data/congress/REPORT.md section 2), fitted on earlier "
                                  "cycles only, from what was known before the election (the orchestrator, "
                                  "2026-11-07 05:58); no polls are used, so it carries less than forecasters then knew",
                          "fit_years": m["years"], "cycles": len(m["years"]), "races": m["n"],
                          "b_lean": m["b_lean"], "b_inc": m["b_inc"], "b_lag": m["b_lag"], "s_e_fitted": m["s_e"],
                          "k": m["k"], "calibration": m["calibration"], "s_e": own_s_e(m),
                          "s_a": m["s_a"], "c": m["c"], "ZtZ_inv": m["ZtZ_inv"],
                          "national_forecast": a_hat, "national_sd": sd_a, "sd": sd,
                          "rho": sd_a ** 2 / (sd_a ** 2 + own_s_e(m) ** 2), "commit": commit,
                          "mean_is": "1/2 + national_forecast + b_lean * lean + b_inc * incumbency"
                                     + (" + b_lag * (last governor race's Democratic share - 1/2)" if m["lag"] else ""),
                          "sd_is": "sqrt(national_sd^2 + s_e^2); national_sd = k s_a sqrt(1 + z (Z'Z)^-1 z'), "
                                   "s_e = k s_e_fitted, z = (1, midterm * P, (1 - midterm) * P), P = +1 Democratic "
                                   "president, -1 Republican; k the calibration factor"}
            nt_rule = near_tie_test(rows)["adopted"].get(level)
            nt_f = near_tie_factor(rows, level, year, 0.5, nt_rule) if nt_rule == "level" else None
            d["model"]["near_tie"] = (
                {"scheme": nt_rule, "window": f"{50 - round(NEAR_W * 100)}-{50 + round(NEAR_W * 100)}%",
                 "factor": nt_f["factor"], "of": nt_f["of"], "fitted_on": nt_f["fitted_on"],
                 "expected": nt_f["expected"], "seen": nt_f["seen"],
                 "note": "each forecast's own calibration gives its multiplier of p (REPORT 2.6)" if nt_f["of"] else
                         "no factor: the fitting years expected fewer than "
                         f"{NEAR_MIN_EXPECTED} near-ties"} if nt_f else
                {"scheme": nt_rule, "note": "not adopted for this level: on the years it reaches it does not both "
                                            "raise the log score and bring the near-even count nearer (REPORT 2.6)"})
            if m.get("national_from"):
                d["model"]["national_from"] = dict(m["national_from"], note=(
                    "national terms from the Senate's earlier cycles: c, s_a and (Z'Z)^-1 are the Senate's fit on "
                    "its own cycles before this year, since the House has fewer than four earlier cycles of its own "
                    "(the orchestrator, 2026-11-07 06:36, item 2)"))
        else:
            d["model"] = {"method": METHOD[level], "not_fitted": too_few(level, year, fy), "fit_years": fy,
                          "commit": commit}
        t = FTE_USED.get((year, level))
        if t:
            d["fte_538"] = {"races_with_a_538_forecast": t["races"], "538_first": t["first"],
                            "fell_back_to_the_model's_own": t["fallback"],
                            "version_first": FTE["versions_order"][level][str(year)][0],
                            "version_note": "538 showed one version by default; no source read here names it, "
                                            "so the version listed first in its repository's rows comes first and "
                                            "the others stand beside it (the orchestrator, 04:12)"}
            print(f"   538: {t['races']} races, first in {t['first']}, fell back in "
                  f"{sum(t['fallback'].values())}: {t['fallback']}")
        cc.write_contest_file(path, d)
        ps = [c["p"]["value"] for c in d["contests"] if c["p"]["value"]]
        print(f"{year} {level}: p computed for {len(ps)} contests, sum {sum(ps):.6g}; largest {max(ps):.3g} "
              f"({max(d['contests'], key=lambda c: c['p']['value'] or 0)['id']})" if ps else f"{year} {level}: none")


def chamber_marginal(f, sd_a, s_e):
    """How a forecast of one seat enters the chamber stage: (mean, s_e,i, lam_i, mark). The model's own: its
    mean, the model's s_e, the whole common swing. 538's (reading (c), the orchestrator 05:58, item 4): its mean
    and implied sd as the seat's marginal, with s_e,i = sqrt(sd_538^2 - s_a^2), as the presidency treats 538's
    marginals. Where 538's sd is not above the common swing's, the seat cannot carry the whole swing and keep
    538's sd: it carries lam = sd_538 sqrt(rho) / s_a of it with s_e,i = sd_538 sqrt(1 - rho), rho the model's
    s_a^2 / (s_a^2 + s_e^2), so that its sd is still 538's and its correlation with the swing the model's."""
    mean, sd = f["share"]["mean"], f["share"]["sd"]
    if f["by"] != "538":
        return mean, s_e, 1.0, None
    if sd > sd_a * (1 + 1e-9):
        return mean, math.sqrt(sd ** 2 - sd_a ** 2), 1.0, None
    rho = sd_a ** 2 / (sd_a ** 2 + s_e ** 2)
    return (mean, sd * math.sqrt(1 - rho), sd * math.sqrt(rho) / sd_a,
            f"538's implied sd ({sd:.4f}) is not above the common swing's ({sd_a:.4f}): the seat carries "
            f"{sd * math.sqrt(rho) / sd_a:.3f} of the swing, at the model's own correlation, so that its sd stays 538's")


def not_in_control(c, level, year):
    """Why a contest is not one of the seats that decide control of the new chamber, or None."""
    if level == "house" and c["special"]:
        return "a special election fills the old Congress's term; not part of control"
    if level == "senate" and c["special"] and (year, c["place"]["state"]) in OFF_DATE_SPECIALS:
        return ("held before November; its winner holds the seat in November and is counted among the seats not "
                "up. " + OFF_DATE_SPECIALS[(year, c["place"]["state"])])
    if level == "senate" and c["special"]:
        nu = [x for x in _load("cha/normalized/contests.json")["contests"] if x["year"] == year and
              x["office"] == "senate" and x["state"] == c["place"]["state"] and x["special"]]
        if nu and nu[0].get("next_up") and nu[0]["next_up"] <= year:
            return "the term ends when the new Senate meets; not part of control"
        if (year, c["place"]["state"]) in SAME_SEAT_SPECIALS:
            return ("the term ends when the new Senate meets; not part of control. "
                    + SAME_SEAT_SPECIALS[(year, c["place"]["state"])])
    return None


def control(d, level, year, m, sd_a, commit):
    s_e = own_s_e(m)
    entries = []
    for i, c in enumerate(d["contests"]):
        why = not_in_control(c, level, year)
        if why:
            c["stage_two"] = {"of": None, "inputs": {}, "source": None, "note": why}
            continue
        kind, val, note = seat_entry(c, m, year)
        se, lam, alts, mark = s_e, 1.0, [], None
        if kind == "model":
            blocks = [c["p"]] + c["p"]["alongside"]
            margs = [chamber_marginal(c["forecasts"][b["of_forecast"]], sd_a, s_e) for b in blocks]
            val, se, lam, mark = margs[0]
            alts = [x[:3] for x in margs]
        entries.append((i, kind, val, se, lam, alts, note, mark))
    held = {}
    if level == "house":
        total = len(entries)
        # the Democrats control with 218 of 435: seat i decides when the others give them exactly 217
        piv = {{435: 217}.get(total, total // 2): 1.0}
        rule = "218 of 435 seats (a majority of the whole House)"
        vp = None
    else:
        held, up = senate_not_up(year)
        notup_D = sum(1 for v in held.values() if v[1] == "D")
        total = len(entries) + len(held)
        pres = presidents()
        if year % 4 == 0:
            vp = vice_president_chance(year)
            pi = vp["P_democrat"]
        else:
            sitting = pres[max(y for y in pres if y < year)]
            pi = 1.0 if sitting["party"] == "D" else 0.0
            vp = {"P_democrat": pi, "who": sitting["vice_president"], "source": sitting["source"]}
        # with a Democratic VP the Democrats control at 50; with a Republican at 51. Seat i decides when
        # the others (seats not up included) give the Democrats 49 (D VP) or 50 (R VP).
        piv = {k - notup_D: w for k, w in ((49, pi), (50, 1 - pi))}
        rule = "51 of 100 seats, or 50 with the Vice President's vote; seats not up and independents counted by caucus"
    probs, seats, fixed_D = stage_two([e[:6] for e in entries], sd_a, list(piv))
    for i, kind, val, se, lam, alts, note, mark in entries:
        c = d["contests"][i]
        st2 = {"of": "House control" if level == "house" else "Senate control",
               "inputs": {"entered_as": kind, "mean": val if kind in ("model", "inferred") else None,
                          "fixed": val if kind == "fixed" else None, "note": note,
                          "rule": rule, "common_swing_sd": sd_a,
                          "own_sd": se if kind in ("model", "inferred") else None,
                          "swing_loading": lam if kind in ("model", "inferred") else None,
                          "marginal": (None if kind != "model" else
                                       "538's mean and implied sd (reading (c))" if c["forecasts"][c["p"]["of_forecast"]]["by"] == "538"
                                       else "the model's own")},
               "source": model_source(year, level, m)}
        if mark:
            st2["inputs"]["marginal_note"] = mark
        if i in probs:
            r = probs[i]
            given = [sum(piv[k] * g[k] for k in piv) for g in r["given_tie"]]
            st2["inputs"]["P_decides_given_tie"] = given[0]
            st2["inputs"]["P_decides_unconditional"] = sum(piv[k] * r["unconditional"][k] for k in piv)
            if level == "senate" and year % 4 == 0:
                st2["inputs"]["P_decides_given_tie_if_VP_D"] = r["given_tie"][0][49 - notup_D]
                st2["inputs"]["P_decides_given_tie_if_VP_R"] = r["given_tie"][0][50 - notup_D]
            pv = c["p"]
            how = ("538's mean and sd as the seat's marginal, the model's common swing (reading (c))"
                   if c["forecasts"][pv["of_forecast"]]["by"] == "538" else "the model's own, normal")
            pv["control"] = {"value": pv["value"] * given[0], "event": pv["event"] * given[0],
                             "P_decides_given_tie": given[0], "under": pv["under"] + "; stage two: " + how,
                             "computed_by": "pipeline/chambers.py", "commit": commit}
            for a_, g_ in zip(pv.get("alongside", []), given[1:]):
                f = c["forecasts"][a_["of_forecast"]]
                a_["control"] = {"value": a_["value"] * g_, "event": a_["event"] * g_, "P_decides_given_tie": g_,
                                 "note": "stage two: " + ("this 538 version's mean and sd as the seat's marginal"
                                                          if f["by"] == "538" else
                                                          "the model's own, normal" if f["share"]["tails"] == "normal"
                                                          else "the model's own, normal with the same sd")}
        c["stage_two"] = st2
    k = np.arange(len(seats))
    d["chamber"] = {"of": "House control" if level == "house" else "Senate control", "rule": rule,
                    "seats_in_play_modelled": int(sum(1 for e in entries if e[1] in ("model", "inferred"))),
                    "seats_fixed_D": fixed_D, "seats_fixed_other": int(sum(1 for e in entries if e[1] == "fixed") - fixed_D),
                    "seats_not_up": ({"D": int(sum(1 for v in held.values() if v[1] == "D")),
                                      "R": int(sum(1 for v in held.values() if v[1] == "R")),
                                      "non-D": int(sum(1 for v in held.values() if v[1] == "non-D"))} if held else None),
                    "vice_president": vp,
                    "expected_D_seats": float((k * seats).sum()) + fixed_D + (sum(1 for v in held.values() if v[1] == "D") if held else 0),
                    "common_swing_sd": sd_a, "own_sd": s_e, "commit": commit,
                    "seat_model": "y_i = mean_i + swing_loading_i * d + e_i, d ~ N(0, common_swing_sd^2), e_i ~ "
                                  "N(0, own_sd_i^2), each seat's stage_two.inputs giving mean, own_sd, swing_loading",
                    "not_up_source": ("the winner of each seat's latest election before "
                                      f"{year}: Cha, Kuriwaki and Snyder from 2006, MEDSL's U.S. Senate 1976-2024 "
                                      "before" + "".join(f"; {v}" for (y, st), v in OFF_DATE_SPECIALS.items()
                                                          if y == year)) if held else None,
                    "seats_not_up_list": ({f"{k[0]} class {k[1]}": {"elected": v[0], "caucus": v[1], "name": v[2],
                                                                    "source": v[3]} for k, v in sorted(held.items())}
                                          if held else None)}
    d["chamber"]["check"] = division_check(d, level, year, held)
    divs = _load("divisions/normalized/divisions.json")["sources"]
    d["sources"][d["chamber"]["check"]["source"]] = divs[d["chamber"]["check"]["source"]]
    if held and any(v[3] == "medsl_senate" for v in held.values()):
        i = _load("medsl/normalized/senate.json")["source"]
        d["sources"]["medsl_senate"] = cc.source_block(
            "MIT Election Data and Science Lab, U.S. Senate statewide 1976-2024, Harvard Dataverse "
            "doi:10.7910/DVN/PEJ5QU, " + str(i.get("version")), i["file"]["url"], i["file"]["read_utc"],
            i.get("licence"), mark="stated", via="https://doi.org/10.7910/DVN/PEJ5QU",
            note="the winner of a seat last elected before 2006 is the candidate with the most votes")
    if level == "senate" and year % 4 == 0 and vp.get("source_block"):
        d["sources"][vp["source"]] = vp.pop("source_block")


def vice_president_chance(year):
    """P(the Vice President elected in year t is a Democrat): the presidential chance, from D1's record
    (data/president/<year>.json): 538's national chance where 538's forecast stands first there (the same model,
    its "US" row, the last forecast before Election Day), else the model's own chance that the Democrat wins the
    College (pipeline/own_forecast.py college_prob on the approved forecast, a 269 tie counted half, states
    whole). Reason: the Senate's control in a presidential year turns on who becomes Vice President (the
    orchestrator, 2026-11-07 05:58, item 1). Assumed independent of the Senate's common swing, as before."""
    import own_forecast
    pres = cc.read_json(os.path.join(REPO, "data", "president", f"{year}.json"))
    unders = [c["p"]["under"] for c in pres["contests"] if (c.get("p") or {}).get("under")]
    top = max(set(unders), key=unders.count)
    if top.startswith("538"):
        model = re.search(r"538 \(([^)]+)\)", top).group(1)
        fte = cc.read_json(os.path.join(REPO, "data", "president", "inputs", "fte_president_forecasts.json"))
        f = fte["years"][str(year)][model]
        us = {a["party"]: a for a in f["units"]["US"]}
        return {"P_democrat": us["D"]["probwin"], "by": f"538 ({model})", "as_of": f["forecast_date"],
                "source": "fte_president", "source_block": fte["source"],
                "note": f"538's chance that the Democratic ticket wins, its {model} forecast of {f['forecast_date']} "
                        f"(the presidency's p in data/president/{year}.json stands under 538 ({model})); any other "
                        f"ticket counts as not Democratic; assumed independent of the Senate's common swing"}
    a = own_forecast.approved(year)
    nara = cc.read_json(os.path.join(REPO, "data", "president", "inputs", "nara_electoral_votes.json"))["years"]
    ev = {s: x["ev"] for s, x in nara[str(year)]["states"].items()}
    fc = {s: (mu, None) for s, mu in a["means"].items()}
    pD = own_forecast.college_prob(fc, ev, a["s_nat"], a["s_state"], a["tails"])
    return {"P_democrat": pD, "by": "the model's own (pipeline/own_forecast.py, approved version)",
            "as_of": a["poll_date"], "source": "data/president",
            "note": f"the model's own chance that the Democrat wins the College, from its forecast on 538's national "
                    f"average of {a['poll_date']} (the presidency's p in data/president/{year}.json stands under the "
                    f"model's own): states whole, a 269 tie counted half; assumed independent of the Senate's common swing"}


PRES = None
FULL = None
FTE_USED = {}


def setup():
    """The fit rows, and a fit on every cycle of each level (FULL), used only to show the year effects and to
    score the national forecasts' misses in the back-test; no forecast uses it."""
    global PRES, FULL
    PRES = presidents()
    rows, skipped = fit_rows()
    FULL = {L: fit(rows, L, list(range(FIT_FROM[L], 2025, 2))) for L in LEVELS}
    return rows, skipped


def history():
    """MATH 8.2 (iv), the check the model can pass: over a population of contests, the expected number
    decided by k votes or fewer, under the forecast each p used, against the number seen. For contest i
    with two-party total N and forecast share ~ normal(mean, sd), P(|margin| <= k) = P(|share - 1/2| <=
    k / 2N). k = 1 is the event (2p); larger k test the same forecasts where there are cases to count."""
    ks = (1, 10, 100, 1000, 5000, 10000, 20000)
    out = {"written_by": "pipeline/chambers.py history", "k_votes": list(ks), "by_level": {}, "cases": {}}
    for level in LEVELS:
        exp = {k: 0.0 for k in ks}
        seen = {k: 0 for k in ks}
        n_c = 0
        for y in file_years(level):
            d = cc.read_json(os.path.join(REPO, "data", level, f"{y}.json"))
            if not d:
                continue
            for c in d["contests"]:
                p = c.get("p") or {}
                if not p.get("value"):
                    continue
                f = c["forecasts"][p["of_forecast"]]
                tp = c["two_party"]
                N = sum(tp["votes"])
                margin = abs(tp["votes"][0] - tp["votes"][1])
                n_c += 1
                cal = f.get("calibration")
                for k in ks:
                    h = k / (2 * N)
                    mu, sd = f["share"]["mean"], f["share"]["sd"]
                    e_ = Phi((0.5 + h - mu) / sd) - Phi((0.5 - h - mu) / sd)
                    if cal:
                        # under the near-tie calibration (round 4): the density within NEAR_W of 1/2 times the
                        # factor, renormalized
                        F = cal["factor"]
                        hw = min(h, NEAR_W)
                        e_ = (e_ + (F - 1) * (Phi((0.5 + hw - mu) / sd) - Phi((0.5 - hw - mu) / sd))) / \
                            (1 + (F - 1) * near_q(mu, sd))
                    exp[k] += e_
                    if margin <= k:
                        seen[k] += 1
                        if k <= 1000:
                            out["cases"].setdefault(level, []).append([c["id"], margin]) if k == 1000 else None
        out["by_level"][level] = {"contests": n_c, "expected": exp, "seen": seen}
    for level, v in out["by_level"].items():
        print(f"{level}: {v['contests']} contests with p, {file_years(level)[0]}-2024")
        for k in ks:
            print(f"   within {k:>5} votes: expected {v['expected'][k]:8.3f}, seen {v['seen'][k]}")
    cc.write_json(os.path.join(REPO, "data", "congress", "history.json"), out)


def main(argv):
    if argv[:1] == ["history"]:
        history()
        return
    rows, skipped = setup()
    if argv[:1] == ["compute"]:
        for y in [int(a) for a in argv[1:]]:
            compute(y)
        return
    if argv[:1] == ["backtest"]:
        print(f"fit rows: {len(rows)} ({sum(1 for r in rows if r['source'] == 'medsl_senate')} Senate rows of "
              f"1982-2004 from MEDSL); skipped: {skipped}")
        chk = incumbency_check(rows)
        print(f"inferred incumbency (MEDSL rule) against Cha's hand coding, Senate 2006-2024: {chk['agree']} of "
              f"{chk['races']} agree ({chk['share']:.3f}); differ: {chk['differ']}")
        for L in LEVELS:
            f = FULL[L]
            print(f"\n{L.upper()} fit on every cycle {f['years'][0]}-{f['years'][-1]} (shown, not used): {f['n']} races; "
                  f"b_lean {f['b_lean']:.3f}, b_inc {f['b_inc']:.4f}" + (f", b_lag {f['b_lag']:.3f}" if f["lag"] else "")
                  + f", s_e {f['s_e']:.4f}, s_a {f['s_a']:.4f}; c {', '.join(f'{v:+.4f}' for v in f['c'])}")
        res = {"earlier": backtest(rows), "earlier_calibrated": backtest(rows, calibrated=True)}
        print("\n======== back-test: each year from a fit on all of its earlier cycles (the House of 2008-2012 on the "
              "Senate's national terms), before calibration")
        for L in LEVELS:
            bt = res["earlier"][L]["per_year"]
            for T, x in bt.items():
                print(f"  {L} {T}: {x['cycles']:2d} cycles, {x['races']:3d} races; national {x['national']['forecast']:+.3f} "
                      f"(sd {x['national']['sd']:.3f}) vs {x['national']['fitted_in_sample']:+.3f}, z {x['national']['z']:+.2f}; "
                      f"cover 50/80/95 {x['normal']['coverage']['0.5']:.2f}/{x['normal']['coverage']['0.8']:.2f}/"
                      f"{x['normal']['coverage']['0.95']:.2f}; z sd {np.std(x['z']):.3f}")
            print(f"  {L} by the number of earlier cycles:")
            for k, x in by_cycles(res["earlier"], L).items():
                print(f"     {k:2d} cycles ({', '.join(map(str, x['years']))}): {_fmt(x)}")
            print(f"  {L} 2006-2024: {_fmt(pooled(res['earlier'], L, YEARS))}")
        print("\n======== calibration: each year's sd times k from its earlier scored years (CAL_MIN years at least);"
              " the forecasts of record")
        for L in LEVELS:
            cal_years = [T for T, x in res["earlier_calibrated"][L]["folds"].items() if x["k"] != 1.0]
            print(f"  {L} k by year: " + ", ".join(f"{T} {res['earlier_calibrated'][L]['folds'][T]['k']:.3f}"
                                                   for T in cal_years))
            print(f"  {L}, the calibrated years ({cal_years[0]}-{cal_years[-1]}), before: "
                  f"{_fmt(pooled(res['earlier'], L, cal_years))}")
            print(f"  {L}, the calibrated years, after:  {_fmt(pooled(res['earlier_calibrated'], L, cal_years))}")
            print(f"  {L} 2006-2024, of record: {_fmt(pooled(res['earlier_calibrated'], L, YEARS))}")
        hs = house_on_senate_terms(rows)
        print("\n======== the House of 2014-2024 on the Senate's national terms (item 2)")
        for k, bt in hs.items():
            print(f"  {k:24s} {_fmt(pooled(bt, 'house'))}")
        print("\n======== the fewest cycles a fit needs: each year from a fit on only the k cycles before it")
        windows = (4, 5, 6, 8, 10)
        for k in windows:
            res[f"window_{k}"] = backtest(rows, window=k)
        common = {"senate": list(range(2002, 2025, 2)), "house": list(range(2016, 2025, 2)),
                  "governor": list(range(1998, 2025, 2))}
        for L in LEVELS:
            print(f"  {L}, the same years for every k ({common[L][0]}-{common[L][-1]}):")
            for k in windows:
                x = pooled(res[f"window_{k}"], L, common[L])
                if x and x["years"] == common[L]:
                    print(f"     k = {k:2d}: {_fmt(x)}")
        seats = backtest_seats(rows)
        print("\n======== seats won by the Democrats among contested races (each year from its earlier cycles)")
        for L, by_year in seats.items():
            for T, x in by_year.items():
                print(f"  {L} {T}: {x['races']} races, expected {x['expected']:.1f}, 80% {x['interval_80']}, "
                      f"won {x['won']}, PIT {x['pit']:.2f}")
        out = {"written_by": "pipeline/chambers.py backtest", "fit_from": FIT_FROM, "k_min": K_MIN,
               "cal_min": CAL_MIN, "full_fit_shown_not_used": FULL, "incumbency_check": chk, "seats": seats,
               "skipped": skipped, "rows": len(rows), "schemes": {},
               "house_on_senate_terms": {k: {"per_year": {T: {kk: v for kk, v in x.items() if kk != "z"}
                                                          for T, x in bt["house"]["per_year"].items()},
                                             "pooled_2014_2024": pooled(bt, "house")} for k, bt in hs.items()}}
        for name, bt in res.items():
            out["schemes"][name] = {L: {"per_year": {T: {k: v for k, v in x.items() if k != "z"}
                                                     for T, x in bt[L]["per_year"].items()},
                                        "folds": bt[L]["folds"], "by_cycles": by_cycles(bt, L),
                                        "pooled_2006_2024": pooled(bt, L, YEARS),
                                        "pooled_all": pooled(bt, L)} for L in LEVELS}
        nt = near_tie_test(rows)
        out["near_tie"] = nt
        print("\nNear-tie calibration (round 4): adopted", nt["adopted"])
        for L, v in nt["by_level"].items():
            for sch in ("none", "level", "band"):
                x = v[sch]
                if x["races"]:
                    print(f"  {L} {v['years'][0]}-{v['years'][-1]} {sch:5s}: {x['races']} races, log score "
                          f"{x['mean_log_score']:.4f}, coverage " + "/".join(f"{c_:.3f}" for c_ in x["coverage"].values())
                          + "; " + ", ".join(f"{k} {w['expected']:.1f} vs {w['seen']}" for k, w in x["within"].items()))
        os.makedirs(os.path.join(REPO, "data", "congress"), exist_ok=True)
        cc.write_json(os.path.join(REPO, "data", "congress", "backtest.json"), out)


if __name__ == "__main__":
    main(sys.argv[1:])
