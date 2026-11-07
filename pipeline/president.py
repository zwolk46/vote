"""pipeline/president.py: every presidential contest by state (and by district where electoral votes split),
1976-2024, with its inputs, their sources, and p computed exactly in both stages.

Written 2026-11-07 by worker D1 (briefs/D1-data-president.md steps 4 and 6; plan/PLAN.md section 3).
Reads only data/president/inputs/ (written by the scripts in pipeline/intake/); writes
data/president/<year>.json, one file per election, in the layout of plan section 3 (fields added are listed
in data/README.md).

p for a voter in unit i (model section 3 and MATH section 4):
    p_i = p_state,i x W_i,
    p_state,i = f_i(1/2) / (2 n_i)   the chance the unit's count without the ballot is tied, our convention
                                     (a tie counted as half: a fair lot), in the density form, which
                                     core.p_contest's own rule chooses at these n (n >= 1000 and n sd^2 >= 6.25);
    W_i = P(the unit's electoral votes decide the College | the unit is tied), from a joint forecast,
          never the independence shortcut (pipeline/college.py).
    n_i is the other voters: the two nominees' certified votes in the unit, less one. It is ex post (a
    voter could not know it), as the model allows (section 3): the count fixes the scale, the forecast the
    closeness.

Which forecast, by year (the orchestrator's ruling of 2026-11-07 03:51, under the maker's word of 02:38):
    2020        The Economist's own joint draws (its forecast, its joint distribution), with its published
                p_decisive_vote beside as a check; 538's forecast beside it, with its own p.
    2016        538's published forecast (polls-plus first; polls-only and now-cast beside): its projected
                share as the mean, the sd its chance of winning implies (normal, marked inferred), and the
                model's own national swing for the College stage, stated.
    2008, 2012  the model's own forecast; 538's published chances of winning shown beside as the check (a
                chance alone does not fix f(1/2), so no p is computed under 538 in those years).
    538, every year (the orchestrator's rule of 04:12, the same for the presidency and Congress): the last
                forecast dated before Election Day (2008's file has Election Day only; kept as the check,
                marked); the model 538 showed by default where a source says which (none read does: polls-plus
                first); and where the implied sd breaks down, the unit's p falls back to the model's own
                forecast, marked, with the reason. It breaks down (the orchestrator's rule of 04:20): where
                other candidates hold 1% or more of 538's chance of winning (Utah 2016); where the chance is
                exactly 0 or 1; and where the implied sd's estimated relative error is 20% or more, from two
                sources: the chance's sampling error (538 printed chances as counts of runs, 20,000 in 2016
                and 40,000 in 2020, inferred from their steps), evaluated at the chance one standard error
                either side, and the rounding of the printed shares. The error is recorded on every unit.
                In the College stage under 538 the units that fall back take the model's own sd.
    1984-2004,  the model's own forecast (pipeline/own_forecast.py, approved version).
    2024
    1976, 1980  no forecast: the model's own needs the results of the two elections before, and no
                standardized source here holds 1968 or 1972 by state; no published forecast was read. The
                contests are written with their results and p null, with the reason.

Run from the repository root:  python3 pipeline/president.py [year ...]
"""
import json
import math
import os
import statistics
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import college  # noqa: E402
import core  # noqa: E402
import own_forecast  # noqa: E402

ROOT = os.path.dirname(HERE)
INPUTS = os.path.join(ROOT, "data", "president", "inputs")
OUTDIR = os.path.join(ROOT, "data", "president")
YEARS = list(range(1976, 2025, 4))
ELECTION_DAY = {1976: "1976-11-02", 1980: "1980-11-04", 1984: "1984-11-06", 1988: "1988-11-08",
                1992: "1992-11-03", 1996: "1996-11-05", 2000: "2000-11-07", 2004: "2004-11-02",
                2008: "2008-11-04", 2012: "2012-11-06", 2016: "2016-11-08", 2020: "2020-11-03",
                2024: "2024-11-05"}
NAMES = {"AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California", "CO": "Colorado",
         "CT": "Connecticut", "DE": "Delaware", "DC": "District of Columbia", "FL": "Florida", "GA": "Georgia",
         "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas",
         "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland", "MA": "Massachusetts",
         "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri", "MT": "Montana",
         "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico",
         "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma",
         "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
         "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont",
         "VA": "Virginia", "WA": "Washington", "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming"}
DISTRICTS = {"ME": ["ME-1", "ME-2"], "NE": ["NE-1", "NE-2", "NE-3"]}
SPLIT_FROM = {"ME": 1972, "NE": 1992}       # the first year each state gave electors by district
WINDOW_INDEX = 2                            # the Economist draws: the window of +-100 steps (+-0.01)
MIN_WINDOW_WEIGHT_VALUE = 10   # decisive draws in the window below which the Economist's draws give a bound only
MVN_DRAWS = 100000
THIRD_CHANCE = 0.01   # other candidates' combined chance of winning from which 538's two-way spread is not read
SD_REL_ERROR_MAX = 0.20   # 538's implied sd is kept where its estimated relative error is under this (rule of 04:20)
EX_POST = "n is the two nominees' certified votes less one: ex post, which no voter knew; the model allows it (section 3)"


def load(name):
    with open(os.path.join(INPUTS, name)) as f:
        return json.load(f)


def git_commit():
    out = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True)
    return out.stdout.strip() or None


def Phi_inv(p):
    return statistics.NormalDist().inv_cdf(p)


def poisson_upper(k, level=0.95):
    """The 95% upper bound on a Poisson mean when k events were seen (k = 0 gives 2.996)."""
    lo, hi = 0.0, k + 10 + 10 * math.sqrt(k + 1)
    for _ in range(100):
        mid = (lo + hi) / 2
        cdf = sum(math.exp(-mid) * mid ** j / math.factorial(j) for j in range(k + 1))
        lo, hi = (mid, hi) if cdf > 1 - level else (lo, mid)
    return hi


def p_block(p_state, W, under, method, n, commit, extra=None):
    if p_state is None or W is None:
        return None
    p = p_state * W
    b = {"value": p, "event": 2 * p, "under": under, "computed_by": "pipeline/president.py", "commit": commit,
         "one_in": (round(1 / p) if p > 0 else None), "p_state": p_state, "W": W, "n_other_voters": n,
         "method": method}
    if extra:
        b.update(extra)
    return b


class Inputs:
    def __init__(self):
        self.fec = load("fec_president.json")
        self.medsl = load("medsl_president.json")
        self.nara = load("nara_electoral_votes.json")
        self.census = load("census_population.json")
        self.fte = load("fte_president_forecasts.json")
        self.econ = load("economist_2020.json")
        self.cert = load("nara_district_certificates.json")


# ----------------------------------------------------------------------------------------------- results
def state_result(I, y, s):
    """The count of record for state s in year y, with every candidate and the check against the other source."""
    md = I.medsl["years"][str(y)][s]
    others = [c for c in md["candidates"]
              if c["name"] not in (md["dem"]["name"], md["rep"]["name"])]
    medsl_src = I.medsl["source"]
    if str(y) in I.fec["years"]:
        f = I.fec["years"][str(y)][s]
        dem, rep, total = f["dem"], f["rep"], f["total"]
        src = I.fec["sources"][str(y)]
        check = {"by": "MEDSL", "dem": md["dem"]["votes"], "rep": md["rep"]["votes"], "total": md["totalvotes"],
                 "dem_diff": md["dem"]["votes"] - dem, "rep_diff": md["rep"]["votes"] - rep,
                 "total_diff": md["totalvotes"] - total, "source": medsl_src}
        dname, rname = md["dem"]["name"], md["rep"]["name"]
    else:
        dem, rep, total = md["dem"]["votes"], md["rep"]["votes"], md["totalvotes"]
        src, check = medsl_src, None
        dname, rname = md["dem"]["name"], md["rep"]["name"]
    cands = [{"name": dname, "party": "Democratic", "votes": dem},
             {"name": rname, "party": "Republican", "votes": rep}]
    cands += [{"name": c["name"], "party": "/".join(c["parties"]) or None, "votes": c["votes"], "from": "MEDSL",
               **({"writein": True} if c["writein"] else {})} for c in others]
    top_two = [c["name"] for c in md["top_two"]]
    return {"certified": True, "candidates": cands, "total_votes": total, "source": src,
            "check": check, "two_party": dem + rep, "dem": dem, "rep": rep,
            "leading_two_not_nominees": (sorted(top_two) != sorted([dname, rname])), "not_candidates":
            md["not_candidates"] or None}


def district_result(I, y, d):
    st = d[:2]
    rec = I.cert["years"].get(str(y), {}).get(st)
    if not rec:
        return None, I.cert["unread"].get(f"{y} {st}", "no certificate read for this year")
    v = rec["districts"][d]
    return ({"certified": True, "candidates": [{"name": None, "party": "Democratic", "votes": v["dem"]},
                                               {"name": None, "party": "Republican", "votes": v["rep"]}],
             "total_votes": None, "source": I.cert["sources"][f"{y} {st}"], "check": None,
             "two_party": v["dem"] + v["rep"], "dem": v["dem"], "rep": v["rep"],
             "note": "the certificate's district totals for the two tickets; other tickets' district votes "
                     "are not read here"}, None)


# --------------------------------------------------------------------------------------------- forecasts
def units_for(y, with_districts):
    """The College's units in year y: 51 jurisdictions, and Maine's and Nebraska's districts when modelled."""
    us = list(NAMES)
    if with_districts:
        for st, ds in DISTRICTS.items():
            if y >= SPLIT_FROM[st]:
                us += ds
    return us


def unit_ev(I, y, u, with_districts):
    if "-" in u:
        return 1
    ev = I.nara["years"][str(y)]["states"][u]["ev"]
    if with_districts and u in DISTRICTS and y >= SPLIT_FROM[u]:
        return 2                                  # the two at-large electors
    return ev


def fte_unit(I, y, model, u):
    rows = I.fte["years"][str(y)][model]["units"][u]
    cs = {c["party"]: c for c in rows}
    pD, pR = cs["D"]["probwin"], cs["R"]["probwin"]
    win = pD / (pD + pR)
    other = sum(c["probwin"] or 0 for c in rows if c["party"] not in ("D", "R"))
    if cs["D"]["projected_voteshare"] is None:
        return {"win_prob": win, "mean": None, "probwin_other": other}
    m = cs["D"]["projected_voteshare"] / (cs["D"]["projected_voteshare"] + cs["R"]["projected_voteshare"])
    return {"win_prob": win, "mean": m, "probwin_D": pD, "probwin_R": pR, "probwin_other": other,
            "share_D": cs["D"]["projected_voteshare"], "share_R": cs["R"]["projected_voteshare"],
            "half_step_D": half_step(cs["D"]["projected_voteshare_printed"]),
            "half_step_R": half_step(cs["R"]["projected_voteshare_printed"])}


def half_step(printed):
    """Half a unit in the last printed digit of a share in percent ('48.11232' -> 0.000005). Where 538's printer
    dropped trailing zeros this overstates the rounding, which errs toward falling back."""
    decimals = len(printed.split(".")[1]) if "." in printed else 0
    return 0.5 * 10 ** (-decimals)


def sd_rel_error(r, runs, step):
    """The estimated relative error of the sd that 538's mean m and chance P imply, sd = (m - 1/2) / z with
    z = Phi^-1(P) (the rule of 04:20). Two sources, combined in quadrature:
      the chance's sampling error: P is a count out of `runs` simulation runs (inferred from the step its
        printed chances take), so its standard error is sqrt(P (1 - P) / runs); the error in z is taken at P
        one standard error either side, not linearised, so a chance of one or two runs counts as unreadable;
      the rounding of the mean: each printed share is exact to half its last digit, which moves the two-party
        mean m = D / (D + R) by at most (R hD + D hR) / (D + R)^2."""
    P, m = r["win_prob"], r["mean"]
    se = math.sqrt(P * (1 - P) / runs)
    z = Phi_inv(P)
    lo, hi = P - se, P + se
    if z == 0 or lo <= 0 or hi >= 1:
        from_chance = math.inf
    else:
        from_chance = max(abs(Phi_inv(lo) - z), abs(Phi_inv(hi) - z)) / abs(z)
    D, R_ = r["share_D"], r["share_R"]
    dm = (R_ * r["half_step_D"] + D * r["half_step_R"]) / (D + R_) ** 2
    from_mean = dm / abs(m - 0.5) if m != 0.5 else math.inf
    value = math.hypot(from_chance, from_mean)
    fin = lambda x: (x if math.isfinite(x) else None)  # noqa: E731
    return {"value": fin(value), "from_chance": fin(from_chance), "from_mean_rounding": fin(from_mean),
            "runs": runs, "runs_mark": f"inferred: every chance 538 printed for this model and year is a whole "
                                       f"multiple of {step:g}",
            "chance_se": se, "mean_rounding": dm}


def implied_sd_breaks(r, runs, step):
    """Why the sd that 538's mean and chance imply is not kept here, or None; and its estimated error (the
    orchestrator's rules of 04:12 and 04:20)."""
    P, m = r["win_prob"], r["mean"]
    if P in (0.0, 1.0):
        return f"538's chance here is exactly {P:g}, which fixes no spread", None
    err = sd_rel_error(r, runs, step)
    if r["probwin_other"] >= THIRD_CHANCE:
        return (f"other candidates hold {r['probwin_other']:.1%} of 538's chance of winning here, so its two-party "
                "chance does not fix a two-way spread"), err
    if err["value"] is None or err["value"] >= SD_REL_ERROR_MAX:
        v = "unbounded" if err["value"] is None else f"{err['value']:.0%}"
        return (f"the implied sd's estimated relative error is {v}, not under {SD_REL_ERROR_MAX:.0%} (538's chance "
                f"{P:.5f} out of {runs:,} runs, its two-party mean {m:.4f})"), err
    if (m - 0.5) / Phi_inv(P) <= 0:
        return "538's mean and chance point to different winners", err
    return None, err


def fte_forecast(I, y, model, units, own):
    """538's marginals with the model's swing. Returns {unit: forecast dict} and the College parameters.
    Where the implied sd breaks down, the unit takes the model's own sd in the College stage, and has no p
    under 538 (the rules of 04:12 and 04:20)."""
    raw = {u: fte_unit(I, y, model, u) for u in units}
    tau_own = math.sqrt(own["s_nat"] ** 2 + own["s_state"] ** 2)
    m = I.fte["years"][str(y)][model]
    for u, r in raw.items():
        why, err = implied_sd_breaks(r, m["runs_inferred"], m["probwin_step"])
        r["fallback"], r["sd_rel_error"] = why, err
        if why is None:
            r["sd"] = (r["mean"] - 0.5) / Phi_inv(r["win_prob"])
            r["sd_how"] = "implied by 538's projected share and chance of winning (normal)"
        else:
            r["sd"] = tau_own
            r["sd_how"] = (f"not read from 538: {why}; the College stage under 538 takes the model's own sd for {y} "
                           f"here ({tau_own:.4f}, inferred)")
    tau = np.array([raw[u]["sd"] for u in units])
    s_d = own["s_nat"]
    capped = False
    if s_d > 0.95 * tau.min():
        s_d, capped = 0.95 * tau.min(), True
    return raw, {"s_d": s_d, "capped": capped, "s_nat_own": own["s_nat"], "tau_own": tau_own}


def own_means(I, y, a, with_districts):
    """The own forecast's means per unit: states from own_forecast; districts by the same uniform swing from
    their own last result (the certificates), when that result is read."""
    means = dict(a["means"])
    if with_districts:
        prev = I.cert["years"].get(str(y - 4), {})
        swing = a["national_mean"] - own_forecast.shares(own_forecast.results())[1][y - 4]
        for st, ds in DISTRICTS.items():
            for d in ds:
                if st in prev:
                    v = prev[st]["districts"][d]
                    means[d] = v["dem"] / (v["dem"] + v["rep"]) + swing
    return means


# ------------------------------------------------------------------------------------------------- years
def build(I, y, commit):
    nara = I.nara["years"][str(y)]
    total_ev, majority = nara["total_ev"], nara["majority"]
    ev_src = I.nara["sources"][str(y)]
    pop = I.census["years"].get(str(y))
    pop_src = I.census["sources"].get(str(y))
    contests = {}

    # every unit's contest shell: result, population, stage two's static inputs
    district_units = [d for st, ds in DISTRICTS.items() if y >= SPLIT_FROM[st] and y >= 2008 for d in ds]
    for u in list(NAMES) + district_units:
        st = u[:2]
        if "-" in u:
            res, why = district_result(I, y, u)
        else:
            res, why = state_result(I, y, u), None
        c = {"id": f"{y}-president-{u}", "year": y, "date": ELECTION_DAY[y], "level": "president",
             "place": {"state": st, "district": (u.split("-")[1] if "-" in u else None),
                       "name": NAMES[st] + (f", congressional district {u.split('-')[1]}" if "-" in u else "")},
             "result": res, "forecasts": [],
             "population": ({"value": pop[st], "of": "state", "source": pop_src} if pop and "-" not in u else
                            {"value": None, "of": "district", "source": None,
                             "note": "district populations are not gathered yet"}),
             "population_nation": ({"value": pop["US"], "of": "nation", "source": pop_src} if pop else None),
             "stage_two": {"of": "Electoral College",
                           "inputs": {"ev": (1 if "-" in u else (2 if st in DISTRICTS and y >= SPLIT_FROM[st]
                                                                 else nara["states"][u]["ev"])),
                                      "ev_state": nara["states"][st]["ev"], "total_ev": total_ev,
                                      "majority": majority, "pi_house": college.PI_HOUSE},
                           "source": ev_src},
             "p": None, "notes": []}
        if "-" not in u and st in DISTRICTS and y >= SPLIT_FROM[st]:
            c["notes"].append(f"{NAMES[st]} gives two electors to the statewide winner and one to each district's; "
                              "this contest is the statewide count, which decides the two at-large electors. A voter "
                              "here also votes in a district contest.")
        if res is None:
            c["notes"].append(f"No district count was read: {why}.")
        elif res.get("leading_two_not_nominees"):
            c["notes"].append("The leading two candidates here were not the two major-party nominees; the forecast "
                              "and n are of the Democratic and Republican nominees.")
        if res is not None:
            c["notes"].append(EX_POST)
        contests[u] = c

    def n_of(u):
        r = contests[u]["result"]
        return r["two_party"] - 1 if r else None

    own_stage = {}      # the model's own stage-two inputs per unit, for the years it is primary or a fallback
    own_whole_note = {}

    def use_own(u, why):
        """The rules of 04:12 and 04:20: where the published forecast's sd breaks down, the model's own p, marked."""
        own = next((f for f in contests[u]["forecasts"] if f["by"] == "the model's own"), None)
        if own is None or own.get("p") is None or u not in own_stage:
            contests[u]["notes"].append(f"No p: {why}, and the model's own forecast does not model this unit in {y}.")
            return
        contests[u]["p"] = own["p"]
        contests[u]["stage_two"]["inputs"].update(own_stage[u])
        contests[u]["notes"].append(f"p is the model's own forecast's: {why} (the orchestrator's rules of 2026-11-07 "
                                    "04:12 and 04:20: where a published forecast's implied sd breaks down, fall back to the "
                                    "model's own forecast, marked).")
        if u in own_whole_note:
            contests[u]["notes"].append(own_whole_note[u])

    # ------------------------------------------------------------------ the model's own forecast
    if y >= 1984:
        a = own_forecast.approved(y)
        with_d = y >= 2016 and str(y - 4) in I.cert["years"] and all(
            st in I.cert["years"][str(y - 4)] for st in DISTRICTS)
        units = units_for(y, with_d)
        means = own_means(I, y, a, with_d)
        units = [u for u in units if u in means]
        mu = np.array([means[u] for u in units])
        ev = np.array([unit_ev(I, y, u, with_d) for u in units])
        assert ev.sum() == total_ev, (y, ev.sum())
        s_unit = np.full(len(units), a["s_state"])
        primary = y not in (2016, 2020)
        src = {"name": "the model's own forecast (pipeline/own_forecast.py, approved version)",
               "url": None, "read_utc": None, "licence": None, "mark": "inferred",
               "via": "538's national polling average (CC BY 4.0) and the certified results of the election before",
               "note": a["note"]}
        for i, u in enumerate(units):
            if u not in contests:
                continue
            r = college.swing_model(i, mu, s_unit, ev, a["s_nat"], total_ev, majority, tails="t4")
            n = n_of(u)
            p_state = core.common.p_density_approx(n, r["f_half"]) if n else None
            tau = math.sqrt(a["s_nat"] ** 2 + a["s_state"] ** 2)
            fc = {"by": "the model's own", "published": False,
                  "share": {"mean": float(mu[i]), "sd": tau, "tails": "normal national error + t4 state error",
                            "national_sd": a["s_nat"], "state_sd": a["s_state"]},
                  "p_published": None, "convention": None, "as_of": a["poll_date"], "source": src,
                  "unit_ev": int(ev[i]),
                  "p": p_block(p_state, r["W"], "the model's own", "density form at f(1/2) of the forecast; "
                               "W by the swing model given the tie", n, commit,
                               {"W_unconditional": r["W_unconditional"], "f_half": r["f_half"]})}
            contests[u]["forecasts"].append(fc)
            own_stage[u] = {"W": r["W"], "W_unconditional": r["W_unconditional"], "unit_ev": int(ev[i]),
                            "method": "the model's own joint forecast: a common national error (normal, sd "
                                      f"{a['s_nat']:.4f}) and independent state errors (t4, sd {a['s_state']:.4f}); "
                                      "W given the tie, by dynamic programming over the other units",
                            "national_swing_sd": a["s_nat"],
                            "districts_modelled": with_d}
            if primary:
                contests[u]["p"] = fc["p"]
                contests[u]["stage_two"]["inputs"].update(own_stage[u])
        if not with_d:
            for st in DISTRICTS:
                if y >= SPLIT_FROM[st] and st in contests:
                    own_whole_note[st] = (
                        f"In the model's own forecast for {y} the districts are not modelled (no district count of "
                        f"{y - 4} was read), so {NAMES[st]} is one unit with all {nara['states'][st]['ev']} electoral "
                        "votes; this p is for the state's whole vote.")
                    if primary:
                        contests[st]["notes"].append(own_whole_note[st])
            for d in district_units:
                if d in contests and primary:
                    contests[d]["notes"].append("No p: the model's own forecast does not model the districts this year.")

    # ------------------------------------------------------------------ 538
    if str(y) in I.fte["years"]:
        models = I.fte["years"][str(y)]
        order = [m for m in ("polls-plus", "polls-only", "now-cast", "published") if m in models]
        fte_src = I.fte["source"]
        own_a = own_forecast.approved(y)
        for model in order:
            first = model == order[0]
            fdate = models[model]["forecast_date"]
            dated_note = models[model].get("note")
            units = units_for(y, y >= 2012)
            have_mean = fte_unit(I, y, model, "PA")["mean"] is not None
            if not have_mean:
                for u in units:
                    if u not in contests:
                        continue
                    r = fte_unit(I, y, model, u)
                    contests[u]["forecasts"].append({
                        "by": "538", "model": None, "published": True, "share": None, "win_prob": r["win_prob"],
                        "p_published": None, "convention": None, "as_of": fdate, "source": fte_src,
                        "p": None, "note": "538's chance of winning only (no projected share in the file): a chance "
                                           "alone does not fix f(1/2), so no p is computed under 538 this year"
                                           + (f". Dated Election Day: {dated_note}" if dated_note else "")})
                continue
            raw, par = fte_forecast(I, y, model, units, own_a)
            mu = np.array([raw[u]["mean"] for u in units])
            tau = np.array([raw[u]["sd"] for u in units])
            ev = np.array([unit_ev(I, y, u, True) for u in units])
            assert ev.sum() == total_ev, (y, ev.sum())
            s_unit = np.sqrt(np.maximum(tau ** 2 - par["s_d"] ** 2, 1e-12))
            for i, u in enumerate(units):
                if u not in contests:
                    continue
                why = raw[u]["fallback"]
                n = n_of(u)
                if why is None:
                    r = college.swing_model(i, mu, s_unit, ev, par["s_d"], total_ev, majority, tails="normal")
                    p_state = core.p_contest(n, float(mu[i]), float(tau[i]), "normal")["p"] if n else None
                    pb = p_block(p_state, r["W"], f"538 ({model})",
                                 "core.p_contest at 538's mean and implied sd; W by the model's swing model "
                                 f"(national swing sd {par['s_d']:.4f}{', capped at 0.95 of the smallest sd' if par['capped'] else ''}) "
                                 "given the tie", n, commit, {"W_unconditional": r["W_unconditional"]})
                else:
                    pb = None
                fc = {"by": "538", "model": model, "published": True,
                      "share": {"mean": float(mu[i]), "sd": (float(tau[i]) if why is None else None), "tails": "normal",
                                "mean_mark": "stated (538's projected shares, made two-party here)",
                                "sd_mark": ("inferred" if why is None else None), "sd_how": raw[u]["sd_how"],
                                "sd_rel_error": raw[u]["sd_rel_error"]},
                      "win_prob": raw[u]["win_prob"], "p_published": None, "convention": None,
                      "as_of": fdate, "source": fte_src, "unit_ev": int(ev[i]), "p": pb}
                if why is not None:
                    fc["note"] = (f"No p under 538 here: {why}. The orchestrator's rules of 2026-11-07 04:12 and 04:20: "
                                  "where the implied sd breaks down, the contest's p falls back to the model's own forecast.")
                contests[u]["forecasts"].append(fc)
                primary_538 = first and (y == 2016 or (y == 2020 and "-" in u))
                if primary_538 and why is not None:
                    use_own(u, f"538's implied sd breaks down here ({why})")
                    continue
                if y == 2016 and first:
                    contests[u]["p"] = fc["p"]
                    contests[u]["stage_two"]["inputs"].update(
                        {"W": r["W"], "W_unconditional": r["W_unconditional"], "unit_ev": int(ev[i]),
                         "method": "538's marginals (mean, implied sd, normal) with the model's own national "
                                   f"swing, sd {par['s_d']:.4f} (the own forecast's national error for {y}); W given "
                                   "the tie, by dynamic programming over the units including the five districts",
                         "national_swing_sd": par["s_d"], "districts_modelled": True})
                if y == 2020 and "-" in u and first:
                    contests[u]["p"] = fc["p"]          # the Economist does not model the districts
                    contests[u]["stage_two"]["inputs"].update(
                        {"W": r["W"], "W_unconditional": r["W_unconditional"], "unit_ev": 1,
                         "method": "538's marginals with the model's own national swing (the Economist's draws "
                                   "have no districts)", "national_swing_sd": par["s_d"], "districts_modelled": True})

    # ------------------------------------------------------------------ the Economist, 2020
    if y == 2020:
        E = I.econ
        states = list(E["states"])
        means = np.array([E["states"][s]["sims"]["mean"] for s in states])
        sds = np.array([E["states"][s]["sims"]["sd"] for s in states])
        cs = E["correlation"]["states"]
        idx = [cs.index(s) for s in states]
        corr = np.array(E["correlation"]["matrix"])[np.ix_(idx, idx)]
        ev = np.array([E["states"][s]["ev"] for s in states])
        for i, s in enumerate(states):
            es = E["states"][s]
            w = es["sims"]["windows"][WINDOW_INDEX]
            n = n_of(s)
            K, width = w["draws"], w["width"]
            mv = college.mvn_stage_two(i, means, sds, corr, ev, 538, 270, draws=MVN_DRAWS)
            half = (width - 1e-4) / 2
            check = {"W_mvn": mv["W"], "W_mvn_se": mv["W_se"], "W_mvn_note": (
                "a check: W from the Economist's means, sds and correlation matrix read as a multivariate normal, "
                f"{MVN_DRAWS:,} seeded draws of the other states given the tie")}
            pub = es["published"]
            if w["weighted"] >= MIN_WINDOW_WEIGHT_VALUE:
                p_state = w["in_window"] / (K * width) / (2 * n)
                W = w["weighted"] / w["in_window"]
                method = (f"the Economist's own 80,000 joint draws: the {w['in_window']:,} draws within {half:.2f} of "
                          "one half, each weighted by whether the state's electoral votes decide the College in that "
                          "draw (a 269 tie counted half)")
                extra = {"window_draws": w["in_window"], "window_weighted": w["weighted"], "window_width": width,
                         "relative_error": 1 / math.sqrt(w["weighted"]), **check}
                pb = p_block(p_state, W, "The Economist", method, n, commit, extra)
                pb["ratio_to_published"] = pb["value"] / pub["p_decisive_vote"]
            else:
                upper = poisson_upper(int(round(w["weighted"]))) / (K * width) / (2 * n)
                pb = None
                bound = {"p_upper": upper, "one_in_at_least": round(1 / upper), "window_draws": w["in_window"],
                         "window_weighted": w["weighted"], **check,
                         "note": (f"The Economist's 80,000 draws hold {w['in_window']:,} within {half:.2f} of one half "
                                  f"and {w['weighted']:g} in which the state's votes decide, too few to fix p; under "
                                  f"its forecast p is at most {upper:.2g} (95% bound). Its own figure, beside, rests "
                                  "on a method it does not state.")}
            fc = {"by": "The Economist", "published": True,
                  "share": {"mean": pub["mean"], "sd": float(sds[i]), "tails": "published",
                            "low": pub["low"], "high": pub["high"], "sd_mark": "measured from its draws"},
                  "win_prob": pub["win_prob"], "p_published": pub["p_decisive_vote"],
                  "convention": "unread: the Economist's method for p_decisive_vote is not stated in its files "
                                "(model section 4)",
                  "as_of": E["model_date"], "source": E["source"], "unit_ev": int(ev[i]), "p": pb}
            if pb is None:
                fc["p_bound"] = bound
            contests[s]["forecasts"].append(fc)
            fte = next((f for f in contests[s]["forecasts"] if f["by"] == "538" and f.get("p")), None)
            if pb is not None:
                contests[s]["p"] = pb
                contests[s]["stage_two"]["inputs"].update(
                    {"W": pb["W"], "unit_ev": int(ev[i]), "method": method, "districts_modelled": False})
            elif fte is None:
                use_own(s, "the Economist's draws cannot fix p here (see its forecast's p_bound), and 538's implied "
                           "sd breaks down here (see its forecast's note)")
            else:
                contests[s]["p"] = fte["p"]
                contests[s]["notes"].append(
                    "The Economist's draws cannot fix p here (see its forecast's p_bound), so p is 538's, the other "
                    "forecast published for 2020.")
                contests[s]["stage_two"]["inputs"].update(
                    {"W": fte["p"]["W"], "W_unconditional": fte["p"].get("W_unconditional"), "unit_ev": fte["unit_ev"],
                     "method": "538's marginals with the model's own national swing", "districts_modelled": True})
            if s in DISTRICTS:
                contests[s]["notes"].append("The Economist's draws give Maine and Nebraska whole (winner-take-all, "
                                            f"{int(ev[i])} electoral votes); 538's forecast beside it models the districts.")

    for u, c in contests.items():
        if c["p"] is None and y < 1984:
            c["notes"].append("No p: no published forecast was read for this year, and the model's own forecast "
                              "needs the two elections before (1968 and 1972 by state are not in the sources read).")
    return contests


def summary(y, contests):
    ps = [(u, c["p"]["value"], c["result"]["two_party"]) for u, c in contests.items()
          if c["p"] and c["result"] and "-" not in u]
    if not ps:
        return None
    nv = sum(n for _, _, n in ps)
    avg = sum(p * n for _, p, n in ps) / nv
    top = sorted(ps, key=lambda x: -x[1])[:5]
    return {"vote_weighted_mean_p": avg, "one_in": round(1 / avg), "top": [(u, p) for u, p, _ in top],
            "states_with_p": len(ps)}


def main():
    years = [int(a) for a in sys.argv[1:]] or YEARS
    I = Inputs()
    commit = git_commit()
    for y in years:
        contests = build(I, y, commit)
        doc = {"about": f"Every presidential contest of {y} by state (and by district where electoral votes "
                        "split), with inputs, sources and p. Layout: plan/PLAN.md section 3, fields added in "
                        "data/README.md. Written by pipeline/president.py; do not edit by hand.",
               "year": y, "computed_by": "pipeline/president.py", "commit": commit,
               "summary": summary(y, contests), "contests": list(contests.values())}
        path = os.path.join(OUTDIR, f"{y}.json")
        with open(path, "w") as f:
            json.dump(doc, f, indent=1)
            f.write("\n")
        s = doc["summary"]
        print(f"{y}: {len(contests)} contests; " + (
            f"average voter's p {s['vote_weighted_mean_p']:.3g} (1 in {s['one_in']:,}); highest "
            + ", ".join(f"{u} 1 in {1 / p:,.0f}" for u, p in s["top"]) if s else "no p"))


if __name__ == "__main__":
    main()
