"""C25 (third pass, item 5: D2's #74, the odd-year governors; the orchestrator's relay of 12:35 UTC). The 60 governor
contests of the odd years 1977-2023 (data/governor/<odd year>.json): the sources checked (Cha, Kuriwaki and Snyder's
file for 2007-2021, the Secretary of State's workbook for Louisiana 2023; Algara and Amlani's county file is not
refetched here, as in the second pass), the fit shown to use the even years before each odd year only (the model block
of every odd year rebuilt from my own even-year fit rows, which hold no odd year), every odd p recomputed from its
inputs and the inputs themselves (lean, president, incumbency, the last governor race) rebuilt, and the odd years'
back-test (data/congress/backtest-governor-odd.json) reproduced: the plain route against the midterm term under the
robustness test of 08:36, and the lean note's two tests under the ruling of 11:01 as D2 recorded it (data/congress/
REPORT.md section 0, item 3). Own implementation (m2fit.py); nothing from pipeline/ is imported.
[measured] throughout; the record's own figures quoted from the files [stated].
"""
import collections
import json
import math
import os
import re
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402
import m2fit as F  # noqa: E402

C74, C74_PARENT = "5a22ade", "7fd4565"   # #74 and the main it followed
ODD_YEARS = list(range(1977, 2024, 2))
ODD_STATES = ("KY", "LA", "MS", "NJ", "VA")
LEAN_KS = (1000, 5000, 10000, 20000, 50000)
LEAN_MIN = 5
WINDOWS = (0.01, 0.02, 0.05)
BANDS = (0.0, 0.05, 0.10, 0.20)
MIN_COUNT = 5
SQ2PI = math.sqrt(2 * math.pi)


def h1(s):
    print("\n" + s)


def Phi(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def within(mu, sd, w):
    return Phi((0.5 + w - mu) / sd) - Phi((0.5 - w - mu) / sd)


def major(p):
    p = (p or "").upper()
    if p in ("D", "DEM", "DEMOCRAT", "DEMOCRATIC"):
        return "D"
    if p in ("R", "REP", "REPUBLICAN"):
        return "R"
    return None


def rel(a, b):
    return abs(a - b) / max(abs(a), abs(b), 1e-300)


def git_names(a, b, path):
    return subprocess.run(["git", "diff", "--name-only", a, b, "--", path], capture_output=True, text=True,
                          cwd=L.ROOT).stdout.split()


def odd_files():
    out = {}
    for y in ODD_YEARS:
        p = os.path.join(L.DATA, "governor", f"{y}.json")
        if os.path.exists(p):
            out[y] = L.load_json(p)
    return out


def dr_votes(c):
    """(D votes, R votes) of the leading Democrat and Republican, or None where the two leaders are not one of each."""
    cands = [a for a in c["result"]["candidates"] if a.get("votes")]
    top = sorted(cands, key=lambda a: -a["votes"])[:2]
    if {major(a.get("party")) for a in top} != {"D", "R"}:
        return None
    D = [a for a in cands if major(a.get("party")) == "D"]
    R = [a for a in cands if major(a.get("party")) == "R"]
    if len(D) != 1 or len(R) != 1:
        return None
    return D[0]["votes"], R[0]["votes"]


# ---------------------------------------------------------------------------------------------- 25.1 the files
def section_1(files):
    h1("25.1 The odd years' files and their sources")
    n = sum(len(d["contests"]) for d in files.values())
    by_state = collections.Counter(c["place"]["state"] for d in files.values() for c in d["contests"])
    withp = [c for d in files.values() for c in d["contests"] if (c.get("p") or {}).get("value") is not None]
    print(f"  {len(files)} files {min(files)}-{max(files)}, {n} contests: " + ", ".join(f"{s} {v}" for s, v in sorted(by_state.items()))
          + f"; p computed {len(withp)} (" + ", ".join(f"{s} {v}" for s, v in sorted(collections.Counter(c['place']['state'] for c in withp).items())) + ")")
    reasons = collections.Counter()
    for d in files.values():
        for c in d["contests"]:
            p = c.get("p") or {}
            if p.get("value") is None:
                reasons[(c["place"]["state"], (p.get("not_computed") or p.get("reason") or "no reason")[:60])] += 1
    print("  not computed, by state and reason: " + "; ".join(f"{s} {v}: '{r}'" for (s, r), v in sorted(reasons.items())))
    # dates
    def nov_date(y):
        import datetime
        d = datetime.date(y, 11, 1)
        d += datetime.timedelta(days=(1 - d.weekday()) % 7)   # the first Tuesday
        if d.day == 1:
            d += datetime.timedelta(days=7)   # after the first Monday
        return d.isoformat()
    dd = collections.Counter()
    for y, d in files.items():
        for c in d["contests"]:
            st = c["place"]["state"]
            if st in ("KY", "MS", "NJ", "VA"):
                dd["general day" if c.get("date") == nov_date(y) else f"other: {st} {y} {c.get('date')}"] += 1
            else:
                dd[f"{st}: " + ("null" if c.get("date") is None else c["date"] if y == 2023 else "given")] += 1
    print(f"  dates: {dict(dd)}")
    # Cha: 2007-2021
    cha = [c for c in F.cha_contests() if c["office"] == "governor" and c["year"] % 2]
    chak = {(c["year"], c["state"], bool(c["special"])): c for c in cha}
    eq = bad = 0
    srcs = collections.Counter()
    for y, d in files.items():
        for c in d["contests"]:
            src = c["result"].get("source")
            name = src if isinstance(src, str) else (src or {}).get("name", "")
            key = ("cha" if "Cha" in name else "algara_amlani" if "Algara" in name else "la_sos" if "Louisiana" in name else name[:30])
            srcs[(key, c["result"].get("certified"))] += 1
            if key == "cha":
                k = (y, c["place"]["state"], bool(c.get("special")))
                x = chak.get(k)
                if x is None:
                    bad += 1
                    print(f"    not in my read of Cha: {c['id']}")
                    continue
                mine = sorted((a["votes"] or 0) for a in x["candidates"] if a.get("votes"))
                theirs = sorted((a["votes"] or 0) for a in c["result"]["candidates"] if a.get("votes"))
                tot = sum(theirs) == c["result"].get("total_votes")
                if mine == theirs and tot:
                    eq += 1
                else:
                    bad += 1
                    print(f"    differs from Cha: {c['id']}: mine {mine[-3:]}, file {theirs[-3:]}, total adds up {tot}")
    print(f"  sources (certified flag): {dict(srcs)}; Cha's contests: {eq} equal candidate by candidate and in total, {bad} differ")
    # Algara and Amlani: internal only
    aa_ok = aa_bad = 0
    for y, d in files.items():
        for c in d["contests"]:
            src = c["result"].get("source")
            name = src if isinstance(src, str) else (src or {}).get("name", "")
            if "Algara" in name:
                if sum(a["votes"] or 0 for a in c["result"]["candidates"]) == c["result"].get("total_votes"):
                    aa_ok += 1
                else:
                    aa_bad += 1
    print(f"  Algara and Amlani's contests: {aa_ok} add up to their total, {aa_bad} do not (the county file itself is not refetched here)")
    # Louisiana 2023 against my parse of the workbook (c18/c22's cache)
    try:
        import c18_louisiana as C18
        path = os.path.join(C18.ROOT, "20231014.xlsx")
        cs, _bad = C18.parse(path, "2023-10-14")
        gov = [c for c in cs if re.match(r"^governor$", (c.get("base") or c.get("title") or "").strip(), re.I)]
        la = next(c for c in files[2023]["contests"] if c["place"]["state"] == "LA")
        if gov:
            g = gov[0]
            mine = sorted(x["votes"] for x in g["cands"])
            theirs = sorted(a["votes"] for a in la["result"]["candidates"])
            print(f"  Louisiana 2023: the workbook's '{g.get('title')}' ({g['sheet']}): {len(g['cands'])} candidates, votes "
                  f"{'equal' if mine == theirs else 'DIFFER'} to the file's {len(la['result']['candidates'])} (sum {sum(mine):,} vs the file's total {la['result']['total_votes']:,}; "
                  f"leader {max(g['cands'], key=lambda x: x['votes'])['name']} {max(mine):,}); the file's certified flag {la['result'].get('certified')}")
        else:
            print(f"  Louisiana 2023: no contest titled Governor in my parse of the workbook ({len(cs)} contests)")
    except Exception as e:   # noqa: BLE001
        print(f"  Louisiana 2023: the workbook could not be read here ({e})")


# ------------------------------------------------------------------------------- 25.2 the fit on even years only
def section_2(files, rows):
    h1("25.2 The fit: the even years before each odd year only, and the model blocks reproduced")
    odd_in_rows = sum(1 for r in rows if r["year"] % 2)
    gov_years = sorted({r["year"] for r in rows if r["level"] == "governor"})
    print(f"  my fit rows (c8/c9's, rebuilt from Cha, MEDSL and the files): {len(rows)}, odd-year rows {odd_in_rows}; governor years {gov_years[0]}-{gov_years[-1]}, {len(gov_years)} even cycles")
    changed = git_names(C74_PARENT, C74, "data/governor/")
    even_changed = [f for f in changed if int(re.search(r"(\d{4})\.json", f).group(1)) % 2 == 0]
    print(f"  files #74 changed under data/governor/: {len(changed)}, even years among them {len(even_changed)} {even_changed}")
    other = [f for f in git_names(C74_PARENT, C74, "data/") if not f.startswith("data/governor/")]
    print(f"  other data files #74 changed: {other}")
    worst = collections.defaultdict(float)
    nm = 0
    for y, d in sorted(files.items()):
        m = d.get("model") or {}
        if "c" not in m:
            print(f"    {y}: no fitted model ({(m.get('note') or m.get('method') or '')[:90]})")
            continue
        nm += 1
        mm, fy = F.variant_model(rows, "governor", y, "none")
        if mm is None:
            print(f"    {y}: my fit has too few cycles ({len(fy)})")
            continue
        exp_fy = list(range(1978, y, 2))
        ok_years = (m["fit_years"] == fy == exp_fy)
        cal_ok = all(t < y and t % 2 == 0 for t in m["calibration"]["years"]) and m["calibration"]["years"] == mm["calibration"]["years"]
        if not (ok_years and cal_ok):
            print(f"    {y}: fit years {m['fit_years'][0]}-{m['fit_years'][-1]} ({len(m['fit_years'])}) vs mine {fy[0]}-{fy[-1]} ({len(fy)}); calibration years ok {cal_ok}")
        for k, a, b in (("b_lean", m["b_lean"], mm["b_lean"]), ("b_inc", m["b_inc"], mm["b_inc"]), ("b_lag", m["b_lag"], mm["b_lag"]),
                        ("s_e_fitted", m["s_e_fitted"], mm["s_e"]), ("s_a", m["s_a"], mm["s_a"]), ("k", m["k"], mm["k"])):
            worst[k] = max(worst[k], rel(a, b))
        for i in range(3):
            worst["c"] = max(worst["c"], rel(m["c"][i], mm["c"][i]))
            for j in range(3):
                worst["ZtZ_inv"] = max(worst["ZtZ_inv"], rel(m["ZtZ_inv"][i][j], mm["ZtZ_inv"][i][j]))
        oy = m.get("odd_year") or {}
        z = np.array(oy.get("z") or [1.0, 0.0, 0.0])
        nat = float(z @ np.array(m["c"]))
        nat_sd = m["k"] * m["s_a"] * math.sqrt(1.0 + float(z @ np.array(m["ZtZ_inv"]) @ z))
        s_e = m["k"] * m["s_e_fitted"]
        sd = math.sqrt(nat_sd ** 2 + s_e ** 2)
        worst["national_forecast"] = max(worst["national_forecast"], rel(m["national_forecast"], nat))
        worst["national_sd"] = max(worst["national_sd"], rel(m["national_sd"], nat_sd))
        worst["s_e"] = max(worst["s_e"], rel(m["s_e"], s_e))
        worst["sd"] = max(worst["sd"], rel(m["sd"], sd))
        if oy.get("term") != "plain" or [abs(v) for v in oy.get("z", [])] != [1.0, 0.0, 0.0]:
            print(f"    {y}: odd_year block {json.dumps(oy)[:200]}")
    print(f"  {nm} odd years with a fitted model, each rebuilt from the even years 1978 to the year before (fit years and calibration years as the file's, all even and earlier): "
          "worst relative differences " + ", ".join(f"{k} {v:.1e}" for k, v in worst.items()))
    print("  z = (1, 0, 0) and the plain term in every odd year's model block" if not any(((d.get('model') or {}).get('odd_year') or {}).get('term') not in (None, 'plain') for d in files.values()) else "  SOME odd year's term is not plain")


# ------------------------------------------------------------------------- 25.3 every p from its inputs; the inputs
def governor_index(files_all, cha):
    """{state: [(year, D share, special, source)]}: every governor race a Democrat and a Republican led, from every
    governor file (even and odd years) and from Cha (2006 on, runoffs out)."""
    idx = collections.defaultdict(dict)
    for y, d in files_all.items():
        for c in d["contests"]:
            dr = dr_votes(c)
            if dr:
                idx[c["place"]["state"]][(y, bool(c.get("special")))] = (dr[0] / (dr[0] + dr[1]), "file")
    for c in cha:
        if c["office"] != "governor" or c["runoff"]:
            continue
        dr = F.top_two_DR(c["candidates"])
        if dr:
            idx[c["state"]].setdefault((c["year"], bool(c["special"])), (dr[0]["votes"] / (dr[0]["votes"] + dr[1]["votes"]), "cha"))
    return idx


def last_race(idx, st, y):
    past = [(k[0], v[0], k[1], v[1]) for k, v in idx[st].items() if k[0] < y]
    return max(past, key=lambda x: x[0]) if past else None


def section_3(files, rows):
    h1("25.3 Every odd-year p from its recorded inputs, and the inputs rebuilt")
    ps = F.pres_shares()
    ps = {int(k): v for k, v in ps.items()}
    cha = [c for c in F.cha_contests() if c["office"] == "governor"]
    chak = {(c["year"], c["state"], bool(c["special"])): c for c in cha}
    files_all = {}
    for path in sorted(os.listdir(os.path.join(L.DATA, "governor"))):
        if path.endswith(".json"):
            d = L.load_json(os.path.join(L.DATA, "governor", path))
            files_all[d["year"]] = d
    idx = governor_index(files_all, cha)
    worst = collections.defaultdict(float)
    n = 0
    lag_diff, inc_diff, lean_diff, pres_diff, n_diff = [], [], [], [], []
    notes = collections.Counter()
    for y, d in sorted(files.items()):
        m = d.get("model") or {}
        for c in d["contests"]:
            p = c.get("p") or {}
            fi = c.get("forecast_inputs") or {}
            st = c["place"]["state"]
            # the inputs, rebuilt
            py = y - (y % 4 or 4)
            if fi:
                if st in ps.get(py, {}):
                    mine = ps[py][st] - ps[py]["US"]
                    if abs(mine - fi["lean"]) > 2e-6:
                        lean_diff.append((c["id"], fi["lean"], mine))
                if fi.get("president_party") != F.SITTING.get(y + 1):
                    pres_diff.append((c["id"], fi.get("president_party"), F.SITTING.get(y + 1)))
                x = chak.get((y, st, bool(c.get("special"))))
                if x is not None and fi.get("incumbency_source") == "cha":
                    dr = F.top_two_DR(x["candidates"])
                    if dr:
                        inc = (1 if dr[0]["inc"] == 1 else 0) - (1 if dr[1]["inc"] == 1 else 0)
                        if inc != fi.get("incumbency"):
                            inc_diff.append((c["id"], fi.get("incumbency"), inc))
                lg = fi.get("last_governor_race")
                mine_lg = last_race(idx, st, y)
                if mine_lg and (lg is None or lg["year"] != mine_lg[0] or abs(lg["share_D"] - mine_lg[1]) > 1e-9):
                    lag_diff.append((c["id"], (lg or {}).get("year"), round((lg or {}).get("share_D", 0), 4), mine_lg[0], round(mine_lg[1], 4), mine_lg[3]))
            if p.get("value") is None:
                continue
            n += 1
            dr = dr_votes(c)
            if dr and p["n"] != dr[0] + dr[1] - 1:
                n_diff.append((c["id"], p["n"], dr[0] + dr[1]))
            f0 = c["forecasts"][p["of_forecast"]]
            mean = 0.5 + m["national_forecast"] + m["b_lean"] * fi["lean"] + m["b_inc"] * fi["incumbency"] + m["b_lag"] * (fi["last_governor_race"]["share_D"] - 0.5)
            sd = m["sd"]
            worst["mean"] = max(worst["mean"], rel(mean, f0["share"]["mean"]))
            worst["sd"] = max(worst["sd"], rel(sd, f0["share"]["sd"]))
            fh = L.f_half(mean, sd, "normal")
            worst["f_half"] = max(worst["f_half"], rel(fh, p["f_half"]))
            worst["value"] = max(worst["value"], rel(L.p_density(p["n"], fh), p["value"]))
            worst["event"] = max(worst["event"], rel(2 * L.p_density(p["n"], fh), p["event"]))
            for b in p.get("alongside") or []:
                if "t4" in b["under"]:
                    worst["t4 value"] = max(worst["t4 value"], rel(L.p_density(p["n"], L.f_half(mean, sd, "t4")), b["value"]))
            notes[(p.get("note") or "none")[:120]] += 1
    print(f"  {n} p recomputed from the file's inputs and model block (mean = 1/2 + national + b_lean lean + b_inc inc + b_lag (last race - 1/2); sd the model's; p = f(1/2)/(2n), t4 alongside): "
          "worst relative differences " + ", ".join(f"{k} {v:.1e}" for k, v in worst.items()))
    print(f"  n = the two nominees' votes less one: {'every p' if not n_diff else 'NOT ' + str(n_diff[:5])}")
    print(f"  the inputs rebuilt: lean from the last presidential vote (year t - (t mod 4 or 4)) differs in {len(lean_diff)} {lean_diff[:3]}; "
          f"president's party vs the even year after differs in {len(pres_diff)} {pres_diff[:3]}; incumbency vs Cha's code 1 differs in {len(inc_diff)} {inc_diff[:4]}")
    print(f"  the last governor race (my index: every governor file, even and odd, and Cha 2006 on): differs in {len(lag_diff)} contest(s):")
    for x in lag_diff:
        print(f"    {x[0]}: the file's last race {x[1]} (share {x[2]}); mine {x[3]} (share {x[4]}, from the {x[5]})")
    for x in lag_diff:
        y = int(x[0][:4])
        d = files[y]
        m = d["model"]
        c = next(cc for cc in d["contests"] if cc["id"] == x[0])
        p = c.get("p") or {}
        if p.get("value") is None:
            continue
        fi = c["forecast_inputs"]
        mean = 0.5 + m["national_forecast"] + m["b_lean"] * fi["lean"] + m["b_inc"] * fi["incumbency"] + m["b_lag"] * (x[4] - 0.5)
        pm = L.p_density(p["n"], L.f_half(mean, m["sd"], "normal"))
        print(f"    with my last race, {x[0]}'s mean would be {mean:.4f} (file {c['forecasts'][p['of_forecast']]['share']['mean']:.4f}) and p {pm:.4e} (file {p['value']:.4e}), x{pm / p['value']:.3f}")
    print("  the note on the p: " + "; ".join(f"{v}: '{k}'" for k, v in notes.items()))
    # the even years' p carry no such note
    en = collections.Counter()
    for y, d in files_all.items():
        if y % 2 == 0:
            for c in d["contests"]:
                p = c.get("p") or {}
                if p.get("value") is not None:
                    en["note" if p.get("note") else "no note"] += 1
    print(f"  the even years' governor p: {dict(en)}")
    return idx


# ------------------------------------------------------------- 25.4 the odd years' back-test and the lean note
def odd_rows(files, idx):
    """The odd-year races the route is scored on, by D2's rules (odd_governor_rows): Kentucky, Mississippi, New Jersey
    and Virginia, not special, one Democrat and one Republican leading; lean, incumbency and the last race as the
    file records them (D2's own inputs, so the test is reproduced as run)."""
    rows, skipped = [], collections.Counter()
    for y, d in sorted(files.items()):
        for c in d["contests"]:
            st = c["place"]["state"]
            if st not in ODD_STATES or c.get("special"):
                skipped["a special election, or a state that elects its governor in even years"] += 1
                continue
            if st == "LA":
                skipped["Louisiana"] += 1
                continue
            dr = dr_votes(c)
            fi = c.get("forecast_inputs") or {}
            if not dr:
                skipped["not one Democrat and one Republican leading"] += 1
                continue
            if not fi or fi.get("last_governor_race") is None:
                skipped["no inputs"] += 1
                continue
            rows.append({"year": y, "state": st, "y": dr[0] / (dr[0] + dr[1]), "n2": dr[0] + dr[1], "lean": fi["lean"],
                         "inc": fi["incumbency"], "lag": fi["last_governor_race"]["share_D"],
                         "P": 1 if F.SITTING[y + 1] == "D" else -1, "id": c["id"]})
    return rows, skipped


def score(rows_even, odd, term, years, bands_by=None):
    tot = {"n": 0, "ls": 0.0, "z": [], "cov": [0, 0, 0], "win": {w: [0.0, 0] for w in WINDOWS},
           "lean_v": {k: [0.0, 0] for k in LEAN_KS}}
    band = [{"n": 0, "win": {w: [0.0, 0] for w in WINDOWS}} for _ in BANDS]
    means, per_year = {}, {}
    for T in years:
        test = [r for r in odd if r["year"] == T]
        m, fy = F.variant_model(rows_even, "governor", T, "none")
        if m is None or not test:
            continue
        py = per_year.setdefault(T, [0, 0.0, len(fy), m["k"]])
        for r in test:
            z = np.array([1.0, (1.0 if term == "midterm" else 0.0) * r["P"], 0.0])
            a = float(z @ np.array(m["c"]))
            sd_a = m["k"] * m["s_a"] * math.sqrt(1.0 + float(z @ np.array(m["ZtZ_inv"]) @ z))
            mu = 0.5 + a + m["b_lean"] * r["lean"] + m["b_inc"] * r["inc"] + m["b_lag"] * (r["lag"] - 0.5)
            sd = math.sqrt(sd_a ** 2 + (m["k"] * m["s_e"]) ** 2)
            means[(T, r["state"])] = mu
            mu0 = bands_by[(T, r["state"])] if bands_by else mu
            b = max(i for i, x in enumerate(BANDS) if abs(mu0 - 0.5) >= x)
            zz = (r["y"] - mu) / sd
            ls = -0.5 * zz * zz - math.log(sd * SQ2PI)
            u = Phi(zz)
            for g in (tot, band[b]):
                g["n"] += 1
                for w in WINDOWS:
                    g["win"][w][0] += within(mu, sd, w)
                    g["win"][w][1] += abs(r["y"] - 0.5) < w
            tot["ls"] += ls
            tot["z"].append(zz)
            for i, q in enumerate((0.5, 0.8, 0.95)):
                tot["cov"][i] += abs(u - 0.5) <= q / 2
            margin = abs(2 * r["y"] - 1) * r["n2"]
            for k in LEAN_KS:
                h = k / (2 * r["n2"])
                tot["lean_v"][k][0] += within(mu, sd, h)
                tot["lean_v"][k][1] += margin < k
            py[0] += 1
            py[1] += ls
    n = tot["n"]
    cells = {"all races": {w: tuple(v) for w, v in tot["win"].items()}}
    for i, g in enumerate(band):
        cells[f"band {BANDS[i]:.2f}" + (f"-{BANDS[i + 1]:.2f}" if i + 1 < len(BANDS) else " up")] = {w: tuple(v) for w, v in g["win"].items()}
    zs = np.array(tot["z"]) if n else np.array([0.0])
    return {"term": term, "n": n, "ls": tot["ls"] / n if n else None, "z_rms": float(np.sqrt(np.mean(zs ** 2))),
            "z_mean": float(zs.mean()), "cov": [c / n for c in tot["cov"]] if n else None, "cells": cells,
            "lean_s": cells["all races"][0.01], "lean_v": {k: tuple(v) for k, v in tot["lean_v"].items()},
            "per_year": per_year, "means": means, "years": sorted(per_year)}


def verdict(r, b0):
    tested, further = [], []
    for cell, ws in b0["cells"].items():
        for w, (e0, s0) in ws.items():
            if s0 < MIN_COUNT and e0 < MIN_COUNT:
                continue
            e, s = r["cells"][cell][w]
            tested.append(f"{cell} {w}")
            if abs(e - s) > abs(e0 - s0):
                further.append(f"{cell} {w}")
    raises = r["ls"] > b0["ls"]
    return {"raises": raises, "gain": r["ls"] - b0["ls"], "tested": tested, "further": further, "improves": raises and not further}


def tail_chance(ps, seen):
    """One-sided chance of `seen` or more successes among independent Bernoullis with chances ps (exact)."""
    dist = np.zeros(len(ps) + 1)
    dist[0] = 1.0
    for q in ps:
        dist[1:] = dist[1:] * (1 - q) + dist[:-1] * q
        dist[0] *= (1 - q)
    return float(dist[seen:].sum())


def section_4(files, rows_even, idx):
    h1("25.4 The odd years' back-test reproduced: the plain route against the midterm term (the robustness test of 08:36), and the lean note's two tests (the ruling of 11:01)")
    rec = L.load_json(os.path.join(L.DATA, "congress", "backtest-governor-odd.json"))
    odd, skipped = odd_rows(files, idx)
    years = sorted({r["year"] for r in odd})
    print(f"  my odd rows {len(odd)} (the record's {rec['rows']}); skipped {dict(skipped)} (the record's {rec['skipped']})")
    b0 = score(rows_even, odd, "plain", years)
    r1 = score(rows_even, odd, "midterm", years, bands_by=b0["means"])
    vd = verdict(r1, b0)
    rp, rm = rec["plain"], rec["midterm"]
    print(f"  plain: {b0['n']} races in {b0['years'][0]}-{b0['years'][-1]} ({len(b0['years'])} years; the record {rp['races']} races, {len(rp['years_scored'])} years); "
          f"mean log score {b0['ls']:.4f} (record {rp['mean_log_score']:.4f}); z rms {b0['z_rms']:.3f} (record {rp['z_rms']:.3f}), z mean {b0['z_mean']:+.3f} ({rp['z_mean']:+.3f}); "
          f"coverage 50/80/95% {b0['cov'][0]:.3f}/{b0['cov'][1]:.3f}/{b0['cov'][2]:.3f} (record {rp['coverage']['0.5']:.3f}/{rp['coverage']['0.8']:.3f}/{rp['coverage']['0.95']:.3f})")
    print(f"  midterm term: mean log score {r1['ls']:.4f} (record {rm['mean_log_score']:.4f}), gain {vd['gain']:+.4f} (record {rm['mean_log_score_gain']:+.4f}); z rms {r1['z_rms']:.3f} ({rm['z_rms']:.3f})")
    # cells
    worst = 0.0
    seen_ok = True
    rkeys = {"all races": "all races", "band 0.00-0.05": "|mean - 1/2| 0.00-0.05", "band 0.05-0.10": "|mean - 1/2| 0.05-0.10",
             "band 0.10-0.20": "|mean - 1/2| 0.10-0.20", "band 0.20 up": "|mean - 1/2| 0.20 up"}
    wk = {0.01: "49-51%", 0.02: "48-52%", 0.05: "45-55%"}
    for mine_r, rec_r in ((b0, rp), (r1, rm)):
        for cell, ws in mine_r["cells"].items():
            for w, (e, s) in ws.items():
                x = rec_r["cells"][rkeys[cell]][wk[w]]
                worst = max(worst, abs(e - x["expected"]))
                seen_ok &= (s == x["seen"])
    print(f"  the near-even cells (3 windows x all races and 4 bands, both terms): counts seen {'all equal' if seen_ok else 'DIFFER'}; expected counts within {worst:.1e} of the record's")
    print("  plain, all races: " + "; ".join(f"{wk[w]} expected {e:.2f} seen {s}" for w, (e, s) in b0["cells"]["all races"].items())
          + " | midterm: " + "; ".join(f"{wk[w]} {e:.2f}" for w, (e, s) in r1["cells"]["all races"].items()))
    print(f"  the test: cells tested (5 or more seen or expected under the plain route) {len(vd['tested'])} (record {len(rm['cells_tested'])}); further from the count seen {len(vd['further'])} (record {len(rm['cells_further'])}): {vd['further']}; "
          f"raises the log score {vd['raises']}; improves {vd['improves']} (record {rm['improves']})")
    loo_fail = 0
    loo_bad = []
    for Y in years:
        if Y not in b0["years"]:
            continue
        ys = [t for t in years if t != Y]
        x0 = score(rows_even, odd, "plain", ys)
        x1 = score(rows_even, odd, "midterm", ys, bands_by=b0["means"])
        v = verdict(x1, x0)
        loo_fail += not v["improves"]
        rl = rm["leave_one_year_out"].get(str(Y), {})
        if rl.get("improves") != v["improves"] or abs(rl.get("mean_log_score_gain", 0) - v["gain"]) > 1e-6:
            loo_bad.append((Y, v["improves"], rl.get("improves"), round(v["gain"], 5), rl.get("mean_log_score_gain")))
    robust = loo_fail == 0 and len(b0["years"]) > 1
    print(f"  leaving one scored year out ({len(b0['years'])} sets): the term fails to improve on {loo_fail}; robust {robust} (record {rm['robust']}); "
          f"sets differing from the record: {loo_bad if loo_bad else 'none'}")
    adopted = "midterm" if vd["improves"] and robust else "plain"
    print(f"  adopted: {adopted} (record {rec['adopted']})")
    # the lean note, by the rule as D2 recorded it
    e_s, s_s = b0["lean_s"]
    k = next((k for k in LEAN_KS if b0["lean_v"][k][0] >= LEAN_MIN), LEAN_KS[-1])
    e_v, s_v = b0["lean_v"][k]
    way = lambda s, e: "more" if s > e else "fewer" if s < e else "as many"
    counts = max(s_s, e_s) >= LEAN_MIN and max(s_v, e_v) >= LEAN_MIN
    stands = counts and way(s_s, e_s) == way(s_v, e_v) != "as many"
    ln = rec["lean_note"]
    print(f"  the lean note's two tests on the plain route's back-test: (s) within 1 point: seen {s_s} against {e_s:.2f} expected ({way(s_s, e_s)}; record {ln['s']['seen']} against {ln['s']['expected']:.2f}); "
          f"(v) k = {k:,} votes, the smallest at which 5 or more are expected (the ladder: " + ", ".join(f"{kk // 1000}k {b0['lean_v'][kk][0]:.2f}/{b0['lean_v'][kk][1]}" for kk in LEAN_KS)
          + f"): seen {s_v} against {e_v:.2f} ({way(s_v, e_v)}; record {ln['v']['seen']} against {ln['v']['expected']:.2f} within {ln['v']['within_votes']:,})")
    print(f"  both count (5 or more seen or expected) {counts}, lean the same way {way(s_s, e_s) == way(s_v, e_v)}: the note stands {stands} (record {ln['stands']}), and reads 'p may be {'low' if way(s_s, e_s) == 'more' else 'high'}'")
    # the chance of the count seen
    ps_s, ps_v = [], []
    for T in b0["years"]:
        m, _ = F.variant_model(rows_even, "governor", T, "none")
        for r in odd:
            if r["year"] != T:
                continue
            a = m["c"][0]
            sd = math.sqrt((m["k"] * m["s_a"] * math.sqrt(1.0 + m["ZtZ_inv"][0][0])) ** 2 + (m["k"] * m["s_e"]) ** 2)
            mu = 0.5 + a + m["b_lean"] * r["lean"] + m["b_inc"] * r["inc"] + m["b_lag"] * (r["lag"] - 0.5)
            ps_s.append(within(mu, sd, 0.01))
            ps_v.append(within(mu, sd, k / (2 * r["n2"])))
    print(f"  the one-sided chance of a count that far off: (s) {tail_chance(ps_s, s_s):.3f} for {s_s} or more of {len(ps_s)}; (v) {tail_chance(ps_v, s_v):.3f} for {s_v} or more")
    # the note's words
    note = next((c["p"]["note"] for d in files.values() for c in d["contests"] if (c.get("p") or {}).get("note")), "")
    want = f"({s_s} against {e_s:.1f} within 1 point, {b0['years'][0]} to {b0['years'][-1]})"
    print(f"  the note's figures {want} {'appear' if want in note else 'DO NOT appear'} in the note as written: '{note[:160]}'")
    # the same test with my last-race index (the one input that differs)
    odd2 = []
    for r in odd:
        lg = last_race(idx, r["state"], r["year"])
        odd2.append(dict(r, lag=lg[1] if lg else r["lag"]))
    b2 = score(rows_even, odd2, "plain", years)
    e2, s2 = b2["lean_s"]
    k2 = next((k for k in LEAN_KS if b2["lean_v"][k][0] >= LEAN_MIN), LEAN_KS[-1])
    print(f"  the same with my last-race index for every row: (s) {s2} against {e2:.2f}; (v) k {k2:,}: {b2['lean_v'][k2][1]} against {b2['lean_v'][k2][0]:.2f}; mean log score {b2['ls']:.4f}")


def main():
    print("C25. D2's #74: THE ODD-YEAR GOVERNORS, 1977-2023 (KY, LA, MS, NJ, VA): SOURCES, THE FIT ON EVEN YEARS ONLY, EVERY p, THE ODD YEARS' BACK-TEST AND THE LEAN NOTE")
    print(f"repository HEAD {L.git_head()}")
    files = odd_files()
    rows = F.all_rows()["rows"]
    section_1(files)
    section_2(files, rows)
    idx = section_3(files, rows)
    section_4(files, rows, idx)


if __name__ == "__main__":
    main()
