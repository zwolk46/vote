"""pipeline/chambers.py: the model's own forecast for Senate, House and governor races, and control of
the Senate and the House.

Written 2026-11-07 by worker D2 (briefs/D2-data-congress.md). Every function says where its inputs come
from; the inputs are the caches the scripts in pipeline/intake/ write (CACHE below), never the network.

THE FORECAST (model section 3, "Which forecast": no forecaster's published forecast for these races is
reachable here, so the model builds one "from what was known before the election", by regression on like
past races, as Gelman, King & Boscardin did). For race i of level L in year t, with y_i the Democrat's
share of the two-party vote:

    y_i = 1/2 + a_t + b_L * lean_i + b_I * inc_i + e_i

  lean_i  the Democrat's two-party share of the last presidential vote held BEFORE year t, in the district
          (House, on the lines in use in year t; The Downballot) or the state (Senate, governor; MEDSL),
          minus the national share in that presidential election (MEDSL);
  inc_i   +1 if a Democratic incumbent runs, -1 if a Republican incumbent runs, 0 for an open seat
          (Cha, Kuriwaki and Snyder's hand-coded incumbency);
  a_t     the year's national swing, common to every race of the level that year;
  e_i     the race's own error, independent across races.

Before the election a_t is not known. Its forecast is a regression on what is known: whether t is a
midterm, and the president's party (National Archives):

    a_t = c_0 + c_mid * M_t * P_t + c_on * (1 - M_t) * P_t + d_t,    d_t ~ N(0, s_a^2)

with M_t = 1 in a midterm, P_t = +1 if the sitting president is a Democrat and -1 if a Republican. s_a is
taken as the root-mean-square miss of this national forecast over the ten cycles, each cycle forecast
from a fit on the other nine (leave one cycle out). So the forecast for race i is normal with mean
1/2 + c_0 + c_.. P_t + b_L lean_i + b_I inc_i and variance s_a^2 + s_e^2; a Student-t with 4 degrees of freedom matched on the same sd is computed alongside (model
section 9.5). The common part s_a^2 is what ties races together for control of a chamber (MATH 4.2):
rho = s_a^2 / (s_a^2 + s_e^2).

The fit uses the races both major parties contested, decided in November (not a runoff), 2006-2024,
from "Candidates in American General Elections" (pipeline/intake/candidates_american_general_elections.py).

Run:  python3 pipeline/chambers.py backtest      prints the fit and the back-test, writes
                                                data/congress/backtest.json
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


def fit_rows():
    """One row per race both major parties contested in November, 2006-2024, every level."""
    cha = _load("cha/normalized/contests.json")["contests"]
    db = _load("downballot/normalized/pres_by_cd.json")["lean_inputs"]
    ps = presidential_shares()
    pres = presidents()
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
        rows.append({"year": t, "level": L, "state": c["state"], "district": c["district"],
                     "special": c["special"], "y": D[0]["votes"] / n2, "n2": n2, "lean": lean, "inc": inc,
                     "M": 0 if t % 4 == 0 else 1, "P": sitting_party(t, pres)})
    return rows, skipped


# ----------------------------------------------------------------------------- fit
def ols(X, y):
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return beta, y - X @ beta


def fit(rows, level, years):
    """Stage one by OLS with a dummy per year; stage two, the year effects on the presidency terms."""
    R = [r for r in rows if r["level"] == level and r["year"] in years]
    ys = sorted({r["year"] for r in R})
    X = np.array([[1.0 if r["year"] == t else 0.0 for t in ys] + [r["lean"], r["inc"]] for r in R])
    y = np.array([r["y"] - 0.5 for r in R])
    beta, res = ols(X, y)
    a = dict(zip(ys, beta[:len(ys)]))
    bL, bI = beta[len(ys)], beta[len(ys) + 1]
    s_e = float(np.sqrt((res ** 2).sum() / (len(y) - X.shape[1])))
    # the race's own error is wider where the race is expected to be close (the back-test shows it:
    # model/.. section 3 of data/congress/REPORT.md): s_e(x) = g0 + g1 * min(x, CAP), x = |fitted - 1/2|,
    # fitted by OLS of |residual| * sqrt(pi/2) on x (for a normal error, E|e| = s_e * sqrt(2/pi))
    x = np.minimum(np.abs(X @ beta), CAP)
    g, _ = ols(np.column_stack([np.ones_like(x), x]), np.abs(res) * math.sqrt(math.pi / 2))
    # stage two: a_t = c0 + c_mid M P + c_on (1-M) P + d
    Z = np.array([[1.0, (t % 4 != 0) * sitting_party(t, PRES), (t % 4 == 0) * sitting_party(t, PRES)]
                  for t in ys])
    av = np.array([a[t] for t in ys])
    c, d = ols(Z, av)
    dof = len(ys) - 3
    if dof < 1:
        raise ValueError(f"{level}: {len(ys)} years cannot fit the national swing's three terms with a residual")
    s_a = float(np.sqrt((d ** 2).sum() / dof))
    return {"level": level, "years": ys, "n": len(R), "a": {t: float(a[t]) for t in ys}, "b_lean": float(bL),
            "b_inc": float(bI), "s_e": s_e, "g": [float(v) for v in g], "c": [float(v) for v in c], "s_a": s_a,
            "ZtZ_inv": np.linalg.inv(Z.T @ Z).tolist()}


def national(m, t):
    """The forecast of year t's swing, and its sd. The sd of record is how far the national forecast
    missed, root-mean-square, over the ten cycles 2006-2024, each forecast from a fit on the other nine
    (NAT_RMSE, set in main); before that is known, the OLS prediction sd s_a^2 (1 + z (Z'Z)^-1 z')."""
    P = sitting_party(t, PRES)
    z = np.array([1.0, (t % 4 != 0) * P, (t % 4 == 0) * P])
    a_hat = float(z @ np.array(m["c"]))
    if NAT_RMSE.get(m["level"]):
        return a_hat, NAT_RMSE[m["level"]]
    sd = m["s_a"] * math.sqrt(1.0 + float(z @ np.array(m["ZtZ_inv"]) @ z))
    return a_hat, sd


def national_rmse(rows, level):
    """Leave-one-cycle-out misses of the national-swing forecast: [(year, forecast, fitted, miss)], RMSE."""
    miss = []
    for T in YEARS:
        if not any(r["level"] == level and r["year"] == T for r in rows):
            continue
        m = fit(rows, level, [t for t in YEARS if t != T])
        a_hat, _ = national(m, T)
        miss.append((T, a_hat, FULL[level]["a"][T], FULL[level]["a"][T] - a_hat))
    return miss, math.sqrt(sum(x[3] ** 2 for x in miss) / len(miss))


def predict(m, r):
    a_hat, sd_a = national(m, r["year"])
    mean = 0.5 + a_hat + m["b_lean"] * r["lean"] + m["b_inc"] * r["inc"]
    s_e = m["g"][0] + m["g"][1] * min(abs(mean - 0.5), CAP) if HETERO else m["s_e"]
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


def seat_dp(means, s_e, grid):
    """dist[g, k] = P(the Democrats win exactly k of these seats | common swing grid[g]); seat i is won when
    mean_i + d + e_i > 1/2, e_i ~ N(0, s_e^2) independent given d. Exact dynamic programming over seats."""
    erf = np.vectorize(math.erf)
    dist = np.zeros((len(grid), len(means) + 1))
    dist[:, 0] = 1.0
    for j, mu in enumerate(means):
        q = 0.5 * (1.0 + erf((mu + grid - 0.5) / (s_e * SQRT2)))[:, None]
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
def backtest(rows, scheme="loco"):
    """loco: each year forecast from a fit on every other year; expanding: from the years before it only
    (possible from 2014, the first year with four earlier ones for the national swing's three terms)."""
    out = {}
    for L in LEVELS:
        per_year, pits, folds = {}, {"normal": [], "t4": []}, {}
        for T in YEARS:
            test = [r for r in rows if r["level"] == L and r["year"] == T]
            train = [t for t in YEARS if (t != T if scheme == "loco" else t < T)]
            if not test or len(train) < 4:
                continue
            m = fit(rows, L, train)
            folds[T] = {k: m[k] for k in ("b_lean", "b_inc", "s_e", "s_a", "c")}
            stats = {"races": len(test)}
            for tails in ("normal", "t4"):
                cover = {0.5: 0, 0.8: 0, 0.95: 0}
                ls, near_pred = 0.0, 0.0
                for r in test:
                    mean, sd, _ = predict(m, r)
                    u = cdf(r["y"], mean, sd, tails)
                    pits[tails].append(u)
                    for q in cover:
                        if abs(u - 0.5) <= q / 2:
                            cover[q] += 1
                    ls += logpdf(r["y"], mean, sd, tails)
                    near_pred += cdf(0.51, mean, sd, tails) - cdf(0.49, mean, sd, tails)
                stats[tails] = {"coverage": {str(q): cover[q] / len(test) for q in cover},
                                "mean_log_score": ls / len(test), "within_49_51_expected": near_pred}
            stats["within_49_51_observed"] = sum(1 for r in test if abs(r["y"] - 0.5) < 0.01)
            a_hat, sd_a = national(m, T)
            stats["national"] = {"forecast": a_hat, "sd": sd_a, "fitted_in_sample": FULL[L]["a"].get(T)}
            per_year[T] = stats
        pit_hist = {t: np.histogram(pits[t], bins=10, range=(0, 1))[0].tolist() for t in pits}
        out[L] = {"per_year": per_year, "pit_deciles": pit_hist, "folds": folds}
    return out


def backtest_seats(rows):
    """Leave-one-cycle-out: the forecast distribution of the Democrats' seats among the races both
    parties contested, against the seats they won; PIT = P(X < won) + P(X = won)/2."""
    out = {}
    for L in ("house", "senate"):
        res = {}
        for T in YEARS:
            test = [r for r in rows if r["level"] == L and r["year"] == T]
            if not test:
                continue
            m = fit(rows, L, [t for t in YEARS if t != T])
            means = [predict(m, r)[0] for r in test]
            _, sd_a = national(m, T)
            grid = swing_grid(sd_a)
            dist = (seat_dp(means, m["s_e"], grid) * normal_weights(grid, 0.0, sd_a)[:, None]).sum(axis=0)
            won = sum(1 for r in test if r["y"] > 0.5)
            cum = np.cumsum(dist)
            k = np.arange(len(dist))
            lo, hi = int(np.searchsorted(cum, 0.1)), int(np.searchsorted(cum, 0.9))
            res[T] = {"races": len(test), "expected": float((k * dist).sum()), "interval_80": [lo, hi], "won": won,
                      "pit": float(cum[won - 1] if won > 0 else 0.0) + 0.5 * float(dist[won])}
        out[L] = res
    return out


def summarize(bt, full):
    lines = []
    for L in LEVELS:
        f = full[L]
        lines.append(f"\n{L.upper()}: {f['n']} races; b_lean {f['b_lean']:.3f}, b_inc {f['b_inc']:.4f}, s_e {f['s_e']:.4f}, "
                     f"s_a {f['s_a']:.4f}, rho {f['s_a']**2/(f['s_a']**2+f['s_e']**2):.2f}; "
                     f"c0 {f['c'][0]:+.4f}, c_mid {f['c'][1]:+.4f}, c_on {f['c'][2]:+.4f}")
        lines.append("  year effects a_t: " + ", ".join(f"{t} {v:+.3f}" for t, v in f["a"].items()))
        tot = {"normal": {"0.5": 0, "0.8": 0, "0.95": 0, "ls": 0.0, "near": 0.0}, "t4": {"0.5": 0, "0.8": 0, "0.95": 0, "ls": 0.0, "near": 0.0}}
        nobs, near_obs = 0, 0
        for T, s in bt[L]["per_year"].items():
            n = s["races"]
            nobs += n
            near_obs += s["within_49_51_observed"]
            for tails in ("normal", "t4"):
                for q in ("0.5", "0.8", "0.95"):
                    tot[tails][q] += s[tails]["coverage"][q] * n
                tot[tails]["ls"] += s[tails]["mean_log_score"] * n
                tot[tails]["near"] += s[tails]["within_49_51_expected"]
            lines.append(f"  {T}: {n:3d} races; national swing forecast {s['national']['forecast']:+.3f} "
                         f"(sd {s['national']['sd']:.3f}) "
                         f"vs fitted {s['national']['fitted_in_sample']:+.3f}; cover 50/80/95 normal "
                         f"{s['normal']['coverage']['0.5']:.2f}/{s['normal']['coverage']['0.8']:.2f}/{s['normal']['coverage']['0.95']:.2f}; "
                         f"within 49-51: expected {s['normal']['within_49_51_expected']:.1f} (t4 {s['t4']['within_49_51_expected']:.1f}), "
                         f"observed {s['within_49_51_observed']}")
        for tails in ("normal", "t4"):
            t_ = tot[tails]
            lines.append(f"  ALL {tails}: cover 50/80/95 {t_['0.5']/nobs:.3f}/{t_['0.8']/nobs:.3f}/{t_['0.95']/nobs:.3f}; "
                         f"mean log score {t_['ls']/nobs:.3f}; within 49-51 expected {t_['near']:.1f}, observed {near_obs}; "
                         f"PIT deciles {bt[L]['pit_deciles'][tails]}")
    return "\n".join(lines)


# ----------------------------------------------------------------------------- computing p
RUN_UTC = cc.now_utc()
METHOD = "D2-v1"            # the version of the method approved 2026-11-07 03:46 UTC (data/congress/REPORT.md)
PI_VP_D_PROVISIONAL = 0.5   # P(the Vice President elected in 2024 is a Democrat), until D1's figure is in
CAUCUS_D_LAST = {("ME", "KING"), ("VT", "SANDERS"), ("CT", "LIEBERMAN")}


def git_head():
    import subprocess
    out = subprocess.run(["git", "-C", REPO, "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
    return out.stdout.strip() or None


def model_source(year, level, m):
    return cc.source_block(f"the model's own forecast, method {METHOD}, fitted to the {level} races of 2006-2024 "
                           f"other than {year}", "https://github.com/zwolk46/vote/blob/main/data/congress/REPORT.md",
                           RUN_UTC, None, mark="inferred",
                           note="the file's top-level \"model\" holds the fitted terms; no polls are used")


def model_mean(m, year, lean, inc):
    a_hat, sd_a = national(m, year)
    return 0.5 + a_hat + m["b_lean"] * lean + m["b_inc"] * inc, sd_a


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


def stage_two(entries, s_e, sd_a, pivotal_weights, grid_points=401):
    """For each modelled seat i: P(the other seats leave control to seat i | seat i tied), MATH 4.2.
    entries: [(index, kind, mean or fixed party)]; pivotal_weights: {k: w}, the weight on the other
    seats' Democratic count k (k counts fixed seats too) at which seat i decides control."""
    grid = swing_grid(sd_a, points=grid_points)
    means = [e[2] for e in entries if e[1] in ("model", "inferred")]
    fixed_D = sum(1 for e in entries if e[1] == "fixed" and e[2] == "D")
    dist = seat_dp(means, s_e, grid)
    erf = np.vectorize(math.erf)
    sd = math.sqrt(sd_a ** 2 + s_e ** 2)
    out = {}
    j = 0
    for idx, kind, mu in entries:
        if kind not in ("model", "inferred"):
            continue
        if kind == "model":
            q = 0.5 * (1.0 + erf((mu + grid - 0.5) / (s_e * SQRT2)))
            others = remove_seat(dist, q)
            # the swing given this seat tied: d | y_i = 1/2 ~ N((1/2 - mu) sd_a^2/sd^2, sd_a^2 s_e^2/sd^2)
            w = normal_weights(grid, (0.5 - mu) * sd_a ** 2 / sd ** 2, sd_a * s_e / sd)
            prob = 0.0
            for k, wt in pivotal_weights.items():
                kk = k - fixed_D
                if 0 <= kk < others.shape[1]:
                    prob += wt * float((others[:, kk] * w).sum())
            # and the unconditional chance, to show what conditioning on the tie changes (MATH 4.2)
            w0 = normal_weights(grid, 0.0, sd_a)
            prob0 = sum(wt * float((others[:, k - fixed_D] * w0).sum()) for k, wt in pivotal_weights.items()
                        if 0 <= k - fixed_D < others.shape[1])
            out[idx] = (prob, prob0)
        j += 1
    seats = (dist * normal_weights(grid, 0.0, sd_a)[:, None]).sum(axis=0)
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
# sd = (mean - 1/2) / Phi^-1(chance), marked inferred. It is kept where the sd's estimated relative error is
# under 20%, no chance is exactly 0 or 1, and other candidates hold under 1% of the chance; otherwise ours comes
# first and 538's forecast stays beside it as the check, with the reason.
FTE_MAX_REL_ERROR = 0.20  # the implied sd is kept where its estimated relative error is under 20%
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
    entry["share"] = {"mean": round(mean, 6), "sd": None, "tails": "normal", "of": "Democrat, two-party",
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
    entry["sd_relative_error"] = None if math.isinf(rel) else round(rel, 4)
    entry["share"]["sd"] = round(sd, 6)
    if rel >= FTE_MAX_REL_ERROR:
        entry["unusable"] = (f"the implied sd's estimated error is {'beyond measure' if math.isinf(rel) else f'{rel:.0%}'} "
                             f"(538's chance rests on too few of its {N:,} simulation runs, or its mean is too near even), "
                             f"at or above the 20% allowed" if N else
                             f"the implied sd's estimated error is {rel:.0%}, at or above the 20% allowed")
        entry["unusable_kind"] = "implied sd's error 20% or more"
    return entry


def compute(year):
    """Fill forecasts, p and control for data/<level>/<year>.json, in place."""
    from core import p_contest
    commit = git_head()
    rows, _ = fit_rows()
    for level in LEVELS:
        path = os.path.join(REPO, "data", level, f"{year}.json")
        d = cc.read_json(path)
        m = fit(rows, level, [t for t in YEARS if t != year])
        sd_a = NAT_RMSE[level]
        a_hat, _ = national(m, year)
        sd = math.sqrt(sd_a ** 2 + m["s_e"] ** 2)
        for c in d["contests"]:
            fi = c.get("forecast_inputs")
            pending = c["p"]["value"] is None and (c["p"]["not_computed"] or "").startswith("pending")
            if not pending:
                if c["p"]["value"] is None and not c["forecasts"]:
                    # p is not computed here (a runoff, ranked choice, a missing input), but 538's forecast
                    # is kept in the record all the same
                    c["forecasts"] = [fte_forecast(c, level, year, v, f) for v, f in (fte_versions(c, level, year) or [])]
                continue
            mean, _ = model_mean(m, year, fi["lean"], fi["incumbency"])
            src = model_source(year, level, m)
            own = [{"by": "the model's own", "published": False, "method": METHOD,
                    "share": {"mean": round(mean, 6), "sd": round(sd, 6), "tails": t, "of": "Democrat, two-party"},
                    "p_published": None, "convention": None, "as_of": c["date"], "source": src}
                   for t in ("normal", "t4")]
            n = c["two_party"]["n_other_voters"]
            rn = p_contest(n, mean, sd, tails="normal")
            rt = p_contest(n, mean, sd, tails="t4")
            own_p = [{"under": f"the model's own ({METHOD}), normal", "value": rn["p"], "event": rn["event"],
                      "method": rn["method"], "f_half": rn["f_half"]},
                     {"under": f"the model's own ({METHOD}), t4 with the same sd", "value": rt["p"],
                      "event": rt["event"], "method": rt["method"], "f_half": rt["f_half"]}]
            fte = [fte_forecast(c, level, year, v, f) for v, f in (fte_versions(c, level, year) or [])]
            for e in fte:
                e["source"] = level + "_538"
                FTE_USED.setdefault((year, level), {"races": 0, "first": 0, "fallback": {}})
            if fte:
                tally = FTE_USED[(year, level)]
                tally["races"] += 1
            first = fte[0] if fte and fte[0]["unusable"] is None else None
            fte_p = []
            for e in fte:
                if e["unusable"] is None:
                    r5 = p_contest(n, e["share"]["mean"], e["share"]["sd"], tails="normal")
                    fte_p.append({"under": f"538 ({e['version']}), normal with the implied sd", "value": r5["p"],
                                  "event": r5["event"], "method": r5["method"], "f_half": r5["f_half"],
                                  "sd": e["share"]["sd"]})
            if fte:
                if first:
                    tally["first"] += 1
                else:
                    kd = fte[0].get("unusable_kind") or fte[0]["unusable"]
                    tally["fallback"][kd] = tally["fallback"].get(kd, 0) + 1
            if first:
                c["forecasts"] = fte + own
                head, rest = fte_p[0], fte_p[1:] + own_p
                head["under"] = (f"538 ({first['version']}), normal with the sd implied by its chance (inferred); "
                                 f"538 published first, the model's own beside it as the check")
            else:
                c["forecasts"] = own + fte
                head, rest = own_p[0], own_p[1:] + fte_p
                if fte:
                    head["under"] += f"; 538's forecast stands beside it as the check ({fte[0]['unusable']})"
            c["p"] = {"value": head["value"], "event": head["event"], "under": head["under"],
                      "computed_by": "pipeline/chambers.py", "commit": commit, "not_computed": None, "reason": None,
                      "method": head["method"], "f_half": head["f_half"], "n": n, "alongside": rest}
        if any(f.get("by") == "538" for c in d["contests"] for f in c.get("forecasts") or []):
            d["sources"][f"{level}_538"] = FTE["source"][level]
        if level in ("house", "senate"):
            control(d, level, year, m, sd_a, commit)
        d["model"] = {"method": METHOD, "what": "the model's own forecast (data/congress/REPORT.md section 2): leaving "
                      "one cycle out, an orchestrator choice the maker may correct, so the inputs are from before the "
                      "election and the coefficients partly from later cycles; no polls are used, so it carries less "
                      "than forecasters then knew", "fit_years": [t for t in YEARS if t != year], "b_lean": m["b_lean"],
                      "b_inc": m["b_inc"], "s_e": m["s_e"], "national_forecast": a_hat, "national_sd": sd_a,
                      "rho": sd_a ** 2 / (sd_a ** 2 + m["s_e"] ** 2), "c": m["c"], "commit": commit}
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
        print(f"{year} {level}: p computed for {len(ps)} contests; largest {max(ps):.3g} "
              f"({max(d['contests'], key=lambda c: c['p']['value'] or 0)['id']})" if ps else f"{year} {level}: none")


def control(d, level, year, m, sd_a, commit):
    s_e = m["s_e"]
    entries = []
    for i, c in enumerate(d["contests"]):
        if level == "house" and c["special"]:
            c["stage_two"] = {"of": None, "inputs": {}, "source": None,
                              "note": "a special election fills the old Congress's term; not part of control"}
            continue
        if level == "senate" and c["special"] and (year, c["place"]["state"]) in OFF_DATE_SPECIALS:
            c["stage_two"] = {"of": None, "inputs": {}, "source": None,
                              "note": "held before November; its winner holds the seat in November and is "
                                      "counted among the seats not up. " + OFF_DATE_SPECIALS[(year, c["place"]["state"])]}
            continue
        if level == "senate" and c["special"]:
            nu = [x for x in _load("cha/normalized/contests.json")["contests"] if x["year"] == year and
                  x["office"] == "senate" and x["state"] == c["place"]["state"] and x["special"]]
            if nu and nu[0].get("next_up") and nu[0]["next_up"] <= year:
                c["stage_two"] = {"of": None, "inputs": {}, "source": None,
                                  "note": "the term ends when the new Senate meets; not part of control"}
                continue
            if (year, c["place"]["state"]) in SAME_SEAT_SPECIALS:
                c["stage_two"] = {"of": None, "inputs": {}, "source": None,
                                  "note": "the term ends when the new Senate meets; not part of control. "
                                          + SAME_SEAT_SPECIALS[(year, c["place"]["state"])]}
                continue
        kind, val, note = seat_entry(c, m, year)
        if kind == "model":
            val = next(f for f in c["forecasts"] if f["by"] == "the model's own")["share"]["mean"]
        entries.append((i, kind, val, note))
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
            pi = PI_VP_D_PROVISIONAL
            vp = {"P_democrat": pi, "mark": "provisional",
                  "note": "the Vice President is elected the same day; until D1's published presidential win "
                          "probability is in, 0.5, assumed independent of the Senate swing"}
        else:
            sitting = pres[max(y for y in pres if y < year)]
            pi = 1.0 if sitting["party"] == "D" else 0.0
            vp = {"P_democrat": pi, "who": sitting["vice_president"], "source": sitting["source"]}
        # with a Democratic VP the Democrats control at 50; with a Republican at 51. Seat i decides when
        # the others (seats not up included) give the Democrats 49 (D VP) or 50 (R VP).
        piv = {k: w for k, w in ((49, pi), (50, 1 - pi)) if w > 0}
        piv = {k - notup_D: w for k, w in piv.items()}
        rule = "51 of 100 seats, or 50 with the Vice President's vote; seats not up and independents counted by caucus"
    probs, seats, fixed_D = stage_two([(i, k, v) for i, k, v, _ in entries], s_e, sd_a, piv)
    split = {}
    if level == "senate" and year % 4 == 0:
        # how far the provisional VP figure moves control: the same with the VP's party known
        for party, k in (("D", 49), ("R", 50)):
            split[party], _, _ = stage_two([(i, kk, v) for i, kk, v, _ in entries], s_e, sd_a, {k - notup_D: 1.0})
    for i, kind, val, note in entries:
        c = d["contests"][i]
        st2 = {"of": "House control" if level == "house" else "Senate control",
               "inputs": {"entered_as": kind, "mean": val if kind in ("model", "inferred") else None,
                          "fixed": val if kind == "fixed" else None, "note": note,
                          "rule": rule, "common_swing_sd": sd_a, "own_sd": s_e},
               "source": model_source(year, level, m)}
        if i in probs:
            w_tie, w_uncond = probs[i]
            st2["inputs"]["P_decides_given_tie"] = w_tie
            st2["inputs"]["P_decides_unconditional"] = w_uncond
            if split:
                st2["inputs"]["P_decides_given_tie_if_VP_D"] = split["D"][i][0]
                st2["inputs"]["P_decides_given_tie_if_VP_R"] = split["R"][i][0]
            pv = c["p"]
            pv["control"] = {"value": pv["value"] * w_tie, "event": pv["event"] * w_tie,
                             "under": pv["under"] + "; stage two: the model's own, normal",
                             "computed_by": "pipeline/chambers.py",
                             "commit": commit}
            for a in pv.get("alongside", []):
                a["control"] = {"value": a["value"] * w_tie, "event": a["event"] * w_tie,
                                "note": "stage two: the model's own, normal"}
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


PRES = None
FULL = None
FTE_USED = {}
NAT_RMSE = {}
NAT_MISSES = {}


def setup():
    """Fit every level on 2006-2024 and measure the national forecast's misses; returns the fit rows."""
    global PRES, FULL
    PRES = presidents()
    rows, skipped = fit_rows()
    FULL = {L: fit(rows, L, YEARS) for L in LEVELS}
    NAT_RMSE.clear()
    for L in LEVELS:
        NAT_MISSES[L], NAT_RMSE[L] = national_rmse(rows, L)
    return rows, skipped


def history(years=YEARS):
    """MATH 8.2 (iv), the check the model can pass: over a population of contests, the expected number
    decided by k votes or fewer, under the forecast each p used, against the number seen. For contest i
    with two-party total N and forecast share ~ normal(mean, sd), P(|margin| <= k) = P(|share - 1/2| <=
    k / 2N). k = 1 is the event (2p); larger k test the same forecasts where there are cases to count."""
    ks = (1, 10, 100, 1000, 5000)
    out = {"written_by": "pipeline/chambers.py history", "k_votes": list(ks), "by_level": {}, "cases": {}}
    for level in LEVELS:
        exp = {k: 0.0 for k in ks}
        seen = {k: 0 for k in ks}
        n_c = 0
        for y in years:
            d = cc.read_json(os.path.join(REPO, "data", level, f"{y}.json"))
            if not d:
                continue
            for c in d["contests"]:
                p = c.get("p") or {}
                if not p.get("value"):
                    continue
                f = next((f for f in c["forecasts"] if f.get("share") and f["share"].get("sd") and
                          (p["under"].startswith("538") and f["by"] == "538" and f.get("unusable") is None or
                           not p["under"].startswith("538") and f["by"] == "the model's own")), None)
                tp = c["two_party"]
                N = sum(tp["votes"])
                margin = abs(tp["votes"][0] - tp["votes"][1])
                n_c += 1
                for k in ks:
                    h = k / (2 * N)
                    mu, sd = f["share"]["mean"], f["share"]["sd"]
                    exp[k] += Phi((0.5 + h - mu) / sd) - Phi((0.5 - h - mu) / sd)
                    if margin <= k:
                        seen[k] += 1
                        if k <= 1000:
                            out["cases"].setdefault(level, []).append([c["id"], margin]) if k == 1000 else None
        out["by_level"][level] = {"contests": n_c, "expected": exp, "seen": seen}
    for level, v in out["by_level"].items():
        print(f"{level}: {v['contests']} contests with p, 2006-2024")
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
        print(f"fit rows: {len(rows)}; skipped: {skipped}")
        for L in LEVELS:
            print(f"national swing sd of record, {L}: {NAT_RMSE[L]:.4f} (leave-one-cycle-out RMSE); misses "
                  + ", ".join(f"{T} {x:+.3f}" for T, _, _, x in NAT_MISSES[L]))
        res = {}
        for scheme in ("loco", "expanding"):
            res[scheme] = backtest(rows, scheme)
            print(f"\n======== back-test: {scheme}")
            print(summarize(res[scheme], FULL))
        seats = backtest_seats(rows)
        print("\n======== seats won by the Democrats among contested races (leave-one-cycle-out)")
        for L, by_year in seats.items():
            for T, x in by_year.items():
                print(f"  {L} {T}: {x['races']} races, expected {x['expected']:.1f}, 80% {x['interval_80']}, "
                      f"won {x['won']}, PIT {x['pit']:.2f}")
        res["seats"] = seats
        os.makedirs(os.path.join(REPO, "data", "congress"), exist_ok=True)
        cc.write_json(os.path.join(REPO, "data", "congress", "backtest.json"),
                      {"written_by": "pipeline/chambers.py backtest", "fit": FULL, "backtest": res,
                       "national_sd": NAT_RMSE, "national_misses": NAT_MISSES,
                       "skipped": skipped, "rows": len(rows)})


if __name__ == "__main__":
    main(sys.argv[1:])
