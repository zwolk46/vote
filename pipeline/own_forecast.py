"""pipeline/own_forecast.py: the model's own presidential forecast, for years with no published forecast.

Written 2026-11-07 by worker D1 (briefs/D1-data-president.md step 3; model/MODEL.md section 3, "Which
forecast"; plan/PLAN.md section 3). Reported to the orchestrator at 03:48 with its back-test; approved
at 03:51 in structure, with one change: the polls are the last national average before the election, not
the one of 9 September, because the voter decides on Election Day with what was known then (law 2a). Both
versions are back-tested below; the eve version scores better and is the one used (APPROVED below).

The method, in the manner of Gelman, King and Boscardin (1998), from "variables known before the election
such as the polls two months out" (model section 3), kept as small as the data allow:

  The Democrat's share of the two-party vote in state i in year t is forecast as
      v_it = v_i,t-4 + (N_t - V_t-4) + delta_t + eps_it,
  the state's last result moved by the national swing the polls showed two months out (uniform swing), where
      v_i,t-4, V_t-4  the certified two-party shares of the last election, in the state and the nation;
      N_t             538's national polling average on 9 September of year t, as a two-party share;
      delta_t         the national error of that average, common to every state:  N(b_t, s_nat^2);
      eps_it          the state's own deviation from uniform swing, independent:  N(0, s_state^2).
  b_t, s_nat and s_state are fitted to the past cycles only (every year before t, from 1976 for the national
  error and 1980 for the state deviations), so each year's forecast uses only what was known before it.
  The common swing is part of the model, so the College stage needs no further assumption: its national
  swing sd is s_nat.

  Two variants are reported in the back-test: "uniform", b_t = 0; and "shrunk", where the September lead
  is shrunk toward even by the factor fitted on past years (N_t - 1/2 multiplied by k_t, least squares
  through one half), the regression to the mean that September leads have shown.

Inputs (all committed under data/president/inputs/): FEC results 1996-2024 (the count of record), MEDSL
results 1976-1992, 538's polling averages (fte_poll_averages.json).

The approved version (APPROVED): the last average, uniform swing, t4 state errors. 2024 is the exception
the files force: 538's 2024 averages end on 12 September 2024 in every file this environment reaches (the
later ones are at projects.fivethirtyeight.com, which redirects to ABC News), so 2024 uses the average of
12 September with the errors fitted to the 9 September averages of earlier cycles, and is marked so.

Run:  python3 pipeline/own_forecast.py   (prints the back-test; writes nothing)
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
INPUTS = os.path.join(ROOT, "data", "president", "inputs")
YEARS = list(range(1976, 2025, 4))


def load(name):
    with open(os.path.join(INPUTS, name)) as f:
        return json.load(f)


def results():
    """{year: {state: (dem, rep)}} from the FEC (1996-2024) and MEDSL (1976-1992)."""
    fec = load("fec_president.json")["years"]
    medsl = load("medsl_president.json")["years"]
    out = {}
    for y in YEARS:
        if str(y) in fec:
            out[y] = {s: (v["dem"], v["rep"]) for s, v in fec[str(y)].items()}
        else:
            out[y] = {s: (v["dem"]["votes"], v["rep"]["votes"]) for s, v in medsl[str(y)].items()}
    return out


def shares(res):
    v = {y: {s: d / (d + r) for s, (d, r) in st.items()} for y, st in res.items()}
    V = {y: sum(d for d, _ in st.values()) / sum(d + r for d, r in st.values()) for y, st in res.items()}
    return v, V


def polls(when):
    """{year: (538's national two-party share for the Democrat, the date)} on `when`: "two_months_out"
    (9 September) or "last" (the last date in 538's file: election day, or the eve, in every year but
    2024, whose file ends on 12 September; see fte_poll_averages.py)."""
    doc = load("fte_poll_averages.json")["years"]
    out = {}
    for y, d in doc.items():
        us = d[when]["units"]["US"]
        dem = us["dem"] if us["dem"] is not None else us["dem_trend_adjusted"]
        rep = us["rep"] if us["rep"] is not None else us["rep_trend_adjusted"]
        out[int(y)] = (dem / (dem + rep), d[when]["date"])
    return out


def polls_two_months_out():
    return {y: v for y, (v, _) in polls("two_months_out").items()}


def polls_eve():
    """The last average before the election (the orchestrator's change of 03:51: the voter decides on
    Election Day with what was known then, law 2a). 2024 has no average after 12 September in any file
    this environment reaches, so 2024 is left out of this version and marked."""
    out = {}
    for y, (v, date) in polls("last").items():
        if date[5:] >= "11-01":
            out[y] = v
    return out


def fit(t, v, V, N, variant):
    """Parameters for year t from the years before t only."""
    nat_years = [y for y in YEARS if y < t and y in N]
    if variant == "shrunk":
        x = [N[y] - 0.5 for y in nat_years]
        z = [V[y] - 0.5 for y in nat_years]
        k = sum(a * b for a, b in zip(x, z)) / sum(a * a for a in x)
    else:
        k = 1.0
    nat_res = [V[y] - (0.5 + k * (N[y] - 0.5)) for y in nat_years]
    s_nat = math.sqrt(sum(r * r for r in nat_res) / len(nat_res))
    st_res = []
    for y in YEARS:
        if 1980 <= y < t:
            sw = V[y] - V[y - 4]
            st_res += [(v[y][s] - v[y - 4][s]) - sw for s in v[y]]
    s_state = math.sqrt(sum(r * r for r in st_res) / len(st_res))
    return {"k": k, "s_nat": s_nat, "s_state": s_state, "n_nat": len(nat_years), "n_state": len(st_res)}


def forecast(t, v, V, N, variant="uniform"):
    """{state: (mean, sd)}, the national mean, and the parameters, for year t (1980 on)."""
    f = fit(t, v, V, N, variant)
    nat_mean = 0.5 + f["k"] * (N[t] - 0.5)
    swing = nat_mean - V[t - 4]
    tau = math.sqrt(f["s_nat"] ** 2 + f["s_state"] ** 2)
    return {s: (v[t - 4][s] + swing, tau) for s in v[t - 4]}, nat_mean, f


APPROVED = {"polls": "last", "variant": "uniform", "tails": "t4",
            "approved": "orchestrator, 2026-11-07 03:51 UTC, under the maker's word of 02:38"}


def approved(t):
    """The model's own forecast for year t (1984 on), in the approved version. Returns the state means,
    the national and state error sds, the tails and the poll it rests on."""
    res = results()
    v, V = shares(res)
    last = polls("last")
    value, date = last[t]
    eve = date[5:] >= "11-01"
    N = polls_eve() if eve else polls_two_months_out()
    N = dict(N)
    N[t] = value
    fc, nat_mean, f = forecast(t, v, V, N, APPROVED["variant"])
    note = (f"538's national average of {date}, the last before the election" if eve else
            f"538's national average of {date}, the last in any file reachable here (its later 2024 averages "
            "are unreadable); errors fitted to the 9 September averages of earlier cycles; the file is 538's "
            "uncorrected copy, whose bug 538 says overstated Harris's margin by 0.1 points")
    return {"means": {s: m for s, (m, _) in fc.items()}, "national_mean": nat_mean, "s_nat": f["s_nat"],
            "s_state": f["s_state"], "tails": APPROVED["tails"], "poll_date": date, "poll_value": value,
            "last_result_year": t - 4, "fit": f, "note": note, "eve": eve}


def Phi(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def T4(x):
    """Student-t cdf with 4 degrees of freedom: 1/2 + (1/2) sin(a) (1 + cos(a)^2 / 2), a = atan(x/2)."""
    a = math.atan(x / 2.0)
    return 0.5 + 0.5 * math.sin(a) * (1 + 0.5 * math.cos(a) ** 2)


GRID = [(-6 + 12 * j / 200) for j in range(201)]
GW = [math.exp(-0.5 * z * z) for z in GRID]
GW = [w / sum(GW) for w in GW]


def cdf(x, m, s_nat, s_state, tails):
    """P(v <= x) for v = m + delta + eps, delta ~ N(0, s_nat^2), eps normal or t4 matched on sd s_state
    (scale s_state / sqrt 2, model section 9.5)."""
    if tails == "normal":
        return Phi((x - m) / math.sqrt(s_nat ** 2 + s_state ** 2))
    sc = s_state / math.sqrt(2.0)
    return sum(w * T4((x - m - z * s_nat) / sc) for z, w in zip(GRID, GW))


def college_prob(fc, ev, s_nat, s_state, tails, majority=270, total=538):
    """P(the Democrat wins a majority of the College), by DP over states given the national error."""
    p = 0.0
    for z, w in zip(GRID, GW):
        dist = [1.0] + [0.0] * total
        for s, (m, _) in fc.items():
            q = 1 - (Phi((0.5 - m - z * s_nat) / s_state) if tails == "normal"
                     else T4((0.5 - m - z * s_nat) / (s_state / math.sqrt(2.0))))
            e = ev[s]
            new = [d * (1 - q) for d in dist]
            for k in range(total + 1 - e):
                new[k + e] += dist[k] * q
            dist = new
        p += w * (sum(dist[majority:]) + (0.5 * dist[total // 2] if total % 2 == 0 else 0.0))
    return p


def backtest():
    res = results()
    v, V = shares(res)
    fte = load("fte_president_forecasts.json")["years"]
    nara = load("nara_electoral_votes.json")["years"]
    print("Back-test of the model's own forecast: every year forecast from the years before it only.")
    print("Brier: the Brier score of the 51 state win probabilities (lower is better; 0.25 is a coin toss).")
    print("in50, in90: the share of states whose result fell inside the forecast's central 50% and 90%")
    print("intervals (a calibrated forecast: 0.50 and 0.90). MAE: mean absolute error of the state means.")
    print("P(D): the forecast's chance that the Democrat wins the College (a 269 tie counted half); won: 1 if")
    print("the Democrat won. 538 columns: 538's published forecast of election day (polls-plus where it ran")
    print("several), which had two more months of polls than this forecast.\n")
    runs = [("two_months_out", "uniform", "normal"), ("two_months_out", "uniform", "t4"),
            ("two_months_out", "shrunk", "t4"), ("eve", "uniform", "normal"), ("eve", "uniform", "t4"),
            ("eve", "shrunk", "t4")]
    for when, variant, tails in runs:
        N = polls_two_months_out() if when == "two_months_out" else polls_eve()
        print(f"polls: {when}; variant: {variant}, state errors {tails}")
        print(f"{'year':>5} {'k':>5} {'s_nat':>6} {'s_st':>6} {'nat mean':>8} {'nat res':>8} {'Brier':>6} "
              f"{'in50':>5} {'in90':>5} {'MAE':>6} {'P(D)':>5} {'won':>3} {'538 Brier':>9} {'538 MAE':>8} {'538 P(D)':>8}")
        tot = []
        for t in [y for y in YEARS if y >= 1984 and y in N]:
            fc, nat_mean, f = forecast(t, v, V, N, variant)
            brier, in50, in90, mae = [], 0, 0, []
            for s, (m, _) in fc.items():
                F = cdf(v[t][s], m, f["s_nat"], f["s_state"], tails)
                pD = 1 - cdf(0.5, m, f["s_nat"], f["s_state"], tails)
                out = 1.0 if v[t][s] > 0.5 else 0.0
                brier.append((pD - out) ** 2)
                in50 += 0.25 < F < 0.75
                in90 += 0.05 < F < 0.95
                mae.append(abs(v[t][s] - m))
            ev = {s: d["ev"] for s, d in nara[str(t)]["states"].items()}
            pc = college_prob(fc, ev, f["s_nat"], f["s_state"], tails)
            won = 1 if sum(ev[s] for s in v[t] if v[t][s] > 0.5) >= 270 else 0   # by states carried
            fb = fm = fp = ""
            if str(t) in fte:
                model = "polls-plus" if "polls-plus" in fte[str(t)] else "published"
                u = fte[str(t)][model]["units"]
                bs, ms = [], []
                for s in v[t]:
                    cs = {c["party"]: c for c in u[s]}
                    pD = cs["D"]["probwin"] / (cs["D"]["probwin"] + cs["R"]["probwin"])
                    out = 1.0 if v[t][s] > 0.5 else 0.0
                    bs.append((pD - out) ** 2)
                    if cs["D"]["projected_voteshare"] is not None:
                        m = cs["D"]["projected_voteshare"] / (cs["D"]["projected_voteshare"] + cs["R"]["projected_voteshare"])
                        ms.append(abs(v[t][s] - m))
                fb = f"{sum(bs) / len(bs):.4f}"
                fm = f"{sum(ms) / len(ms):.4f}" if ms else "n/a"
                us = {c["party"]: c for c in u["US"]}
                fp = f"{us['D']['probwin']:.3f}"
            n = len(fc)
            tot.append((sum(brier) / n, in50 / n, in90 / n, sum(mae) / n))
            print(f"{t:>5} {f['k']:>5.2f} {f['s_nat']:>6.3f} {f['s_state']:>6.3f} {nat_mean:>8.3f} "
                  f"{V[t] - nat_mean:>+8.3f} {sum(brier) / n:>6.3f} {in50 / n:>5.2f} {in90 / n:>5.2f} "
                  f"{sum(mae) / n:>6.3f} {pc:>5.2f} {won:>3} {fb:>9} {fm:>8} {fp:>8}")
        a = [sum(x[j] for x in tot) / len(tot) for j in range(4)]
        print(f"{'all':>5} {'':>5} {'':>6} {'':>6} {'':>8} {'':>8} {a[0]:>6.3f} {a[1]:>5.2f} {a[2]:>5.2f} {a[3]:>6.3f}\n")


if __name__ == "__main__":
    backtest()
