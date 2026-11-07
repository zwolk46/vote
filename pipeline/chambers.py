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
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "intake"))
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


PRES = None
FULL = None
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


def main(argv):
    rows, skipped = setup()
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
