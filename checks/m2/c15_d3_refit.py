"""checks/m2/c15_d3_refit.py: D3's forecasts refitted from the sources, by my own implementation (M2's second pass,
item 4; the brief's amendment of 07:44, and the orchestrator's words of 08:35: "in item 4 report whether that factor
[the #31 local calibration] survives leave-one-year-out").

15.1  Like past races, state legislative levels: every class rebuilt from what each file says was on the ballot
      (REPORT section 2's classes), the like races of earlier years counted again (N, k in the window, the window,
      q) for every contest with such a forecast, against the record.
15.2  The same for local races (MEDSL years 2018-2024, and North Carolina's State Board years from 2014).
15.3  The same for statewide measures at their threshold, and data/measure/backtest-measures.json reproduced.
15.4  Route (a), partisan: the rows rebuilt from Klarner's contest file (Dataverse file 10273086), the fit for each
      year on earlier years only, and every contest's mean, sd, swing and inputs against the record; 2024's from the
      recorded inputs with my fit on Klarner's years.
15.5  The #31 calibration factor (the orchestrator, 06:38): recomputed from the files, the 2024 test, and
      leave-one-year-out; North Carolina's own test too.
15.6  The boundary route (c), "not yet checked": its forecasts against what happened, by class, period and size;
      routes (b) and (d) and route (a) beside it (data/local/backtest.json reproduced where the definitions are known).
15.7  D3's point 1: the race's own sd is chosen by the size bin of the count itself.

Run: python3 checks/m2/c15_d3_refit.py   (reads data/ and the Klarner file in the cache; fetches it if absent)
"""
import collections
import csv
import json
import math
import os
import re
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2d3 as D  # noqa: E402
import m2lib as M  # noqa: E402

csv.field_size_limit(1 << 26)
KLARNER_URL = "https://dataverse.harvard.edu/api/access/datafile/10273086?format=original"
KLARNER_FILE = "klarner_202slers_uoa_contest20230810.csv"
KLARNER_SHA = "21cbaeacd12e4a7b487d289157ddebd99340f056df1ce9bc4329aa1dc6ad39fc"   # [measured] 2026-11-07 08:46 UTC
# the party that won the last presidential election before year t, from the National Archives' Electoral College
# results [stated]; D3 reads the sitting president's party as that party (REPORT section 2; pipeline/local.py
# president_party: e = 4 ((t - 1) // 4)).
WON = {1964: 1, 1968: -1, 1972: -1, 1976: 1, 1980: -1, 1984: -1, 1988: -1, 1992: 1, 1996: 1, 2000: -1, 2004: -1,
       2008: 1, 2012: 1, 2016: -1, 2020: 1,
       2024: -1}  # added in the seventh pass for 2025's odd-year legislatures (#92, #93); R [stated: D3's record names the
# National Archives' 2024 page; c40 derives the same sign from D1's 2024 state votes added up]
PRES = {t: WON[4 * ((t - 1) // 4)] for t in range(1965, 2026) if 4 * ((t - 1) // 4) in WON}
COLS = ["B", "C", "A_last", "A_inc", "A_lean", "B_unopposed", "B_inc", "B_lean", "C_inc", "C_lean", "lean_missing"]
MIN_EARLIER = 3
MEDSL_YEARS = (2018, 2020, 2022, 2024)
MEASURE_YEARS = (2016, 2018, 2020, 2022, 2024)
NC_FIRST = 2014
CAL_MIN_EXPECTED = 30
Z = {"50": 0.6744897501960817, "80": 1.2815515655446004, "95": 1.959963984540054}


def h1(s):
    print("\n" + "=" * 100 + f"\n{s}\n" + "=" * 100)


def cycle(t):
    return "presidential" if t % 4 == 0 else "midterm" if t % 4 == 2 else "odd"


# ------------------------------------------------------------------------------------------ like races, state levels
def state_like_pool():
    """Rows for routes (b), (c) and (d) from the state files' Klarner-sourced contests: (year, key, s). The class
    from my own reading of the ballot (m2d3.structure_state); runoffs by the recorded class (their class needs the
    first round, which the file names only in words)."""
    pool, mine_vs_rec, no_class = [], collections.Counter(), collections.Counter()
    for level in ("state-upper", "state-lower"):
        for r in D.rows(level):
            if r["src"] != "klarner":
                continue
            el = r["election"] or ""
            if "runoff" in el and el != "srunoff" and not el.startswith("lasrunoff"):
                key = r["cls"] if r["cls"] and r["cls"].startswith("runoff") else None
                if key is None:
                    no_class[el] += 1
                    continue
                pr = D.deciding_pair(r, 1)
                if pr and pr[0] + pr[1] > 0:
                    pool.append((r["year"], key, max(pr) / (pr[0] + pr[1])))
                continue
            st = D.structure_state(r)
            if st is None or st[0] not in ("class", "boundary"):
                continue
            k = r["seats"] if st[0] == "boundary" else 1
            pr = D.deciding_pair(r, k)
            if pr is None or pr[0] + pr[1] <= 0:
                continue
            pool.append((r["year"], st[1], max(pr) / (pr[0] + pr[1])))
            if r["cls"] and r["route"] in ("class", "boundary"):
                mine_vs_rec[(st[1] == r["cls"], st[0] == r["route"])] += 1
    return pool, mine_vs_rec, no_class


def compare_like(contests, pool, label, by_year_src=None):
    """For every contest with a like-race forecast: my (N, k, h, q) from the pool's earlier years against the record.
    pool: (year, key, s). Prints the tallies; returns the mismatches."""
    by_key = collections.defaultdict(list)
    for y, key, s in pool:
        by_key[key].append((y, s))
    cache, tal, bad, dq = {}, collections.Counter(), [], []
    for r in contests:
        t, key = r["year"], r["cls"]
        if (t, key) not in cache:
            sh = [s for y, s in by_key.get(key, []) if y < t]
            cache[(t, key)] = D.class_density(sh)
        f, N, h, k = cache[(t, key)]
        if f is None:
            tal["mine: too few like races"] += 1
            bad.append((r["id"], f"mine N {N} < 100; record N {r['N']}"))
            continue
        same = (N == r["N"], k == r["kin"], abs(h - D.window_h(r["win"])) < 1e-9, abs(round(k / N, 5) - r["q"]) < 1e-9)
        tal[same] += 1
        if not all(same):
            bad.append((r["id"], f"mine N {N} k {k} h {h} q {k / N:.5f}; record N {r['N']} k {r['kin']} h {D.window_h(r['win'])} q {r['q']}"))
            if r["q"]:
                dq.append((abs((k / N) / r["q"] - 1), N - r["N"], k - r["kin"], r["id"]))
    n = sum(tal.values())
    print(f"\n  {label}: {n:,} contests with a like-race forecast; (N, k, h, q) all equal in {tal[(True, True, True, True)]:,}")
    for k_, v in sorted(tal.items(), key=str):
        if k_ != (True, True, True, True):
            print(f"    {str(k_):40s} {v:,}")
    if dq:
        dq.sort(reverse=True)
        print(f"    where they differ: N mine - record from {min(x[1] for x in dq)} to {max(x[1] for x in dq)}, k from {min(x[2] for x in dq)} to "
              f"{max(x[2] for x in dq)}; |q mine / record - 1| largest {dq[0][0]:.4f} ({dq[0][3]}), median {sorted(x[0] for x in dq)[len(dq) // 2]:.4f}; "
              f"p moves with q (f = q/(2h)), so by the same share")
    if bad:
        dn = collections.Counter()
        for rid, s in bad:
            dn[rid.split("-")[0]] += 1
        print("    differing, by year: " + ", ".join(f"{y} {c}" for y, c in sorted(dn.items())))
        for rid, s in bad[:12]:
            print(f"    {rid}: {s}")
    return bad


def like_state():
    h1("15.1 Like past races, state legislative levels: classes rebuilt and like races counted again [measured]")
    pool, mine_vs_rec, no_class = state_like_pool()
    print(f"  pool: {len(pool):,} rows (year, class, the leading candidate's share of the deciding pair) from the Klarner-"
          f"sourced contests of both chambers, {min(y for y, _, _ in pool)}-{max(y for y, _, _ in pool)}; "
          f"runoffs without a recorded class (left out): {dict(no_class)}")
    print(f"  my class against the recorded class, contests with a (b)/(c) forecast: (class equal, route equal) -> "
          + ", ".join(f"{k} {v:,}" for k, v in sorted(mine_vs_rec.items(), key=str)))
    kc = collections.Counter(key for _, key, _ in pool)
    print("  rows by class: " + "; ".join(f"{k}: {v:,}" for k, v in sorted(kc.items())))
    contests = [r for level in ("state-upper", "state-lower") for r in D.rows(level)
                if r["route"] in ("class", "boundary", "runoff") and r["N"] is not None]
    kl = [r for r in contests if r["src"] == "klarner"]
    md = [r for r in contests if r["src"] in ("medsl", "in_enr", "la_sos")]
    compare_like(kl, pool, "Klarner-built years (1968-2023), like races from earlier years of the same pool")
    compare_like(md, pool, "2024 (MEDSL-built, with Indiana's own file), like races from Klarner's years before 2024")
    # the window's widening as written: k < 10 at every narrower window
    return pool


# ------------------------------------------------------------------------------------------ like races, local
GENERIC = ("WRITE-IN", "WRITEIN", "WRITE IN", "SCATTERING", "WRITE-INS")


def _generic(name):
    n = (name or "").strip().upper()
    return n in GENERIC or n.startswith("*") or "WRITE" in n


def ballot_local(r):
    """Candidates on the ballot of a local contest (not write-ins, not write-in totals), by votes."""
    b = [a for a in r["cands"] if a[0] != "write-in" and not _generic(a[2]) and a[1] is not None]
    return sorted(b, key=lambda a: -a[1])


def structure_local(r, nc=False):
    """(route, class) for a local contest from what the file says was on the ballot, in REPORT section 7's classes
    (pipeline/local_medsl.py local_structure) or, nc=True, section 9's (local_ncsbe.py nc_key: 'a Democrat against a
    Republican' is a class there, since the State Board's dates have no county lean)."""
    b = ballot_local(r)
    k = r["seats"] or 1
    if len(b) <= k:
        return ("zero", None)
    nd = sum(1 for a in b if a[0] == "D")
    nr = sum(1 for a in b if a[0] == "R")
    lead = f"{r['office_scope']} {r['office_type']}"
    n = len(b)
    if k > 1:
        slate = "both major parties on the ballot" if nd and nr else "one major party or none"
        return ("boundary", f"{lead}, {k if k < 4 else '4+'} seats at once, {slate}")
    if nd == 1 and nr == 1 and (not nc or n == 2):
        return ("partisan", f"{lead}, a Democrat against a Republican") if nc else ("partisan", None)
    nonpartisan = all((a[0] or "nonpartisan") in ("nonpartisan", "") for a in b)
    kind = ("nonpartisan" if nonpartisan else "one major party against others" if nd + nr == 1 else
            "two or more of one major party" if nd + nr >= 2 else "no Democrat or Republican")
    return ("class", f"{lead}, {kind}, {n if n < 4 else '4+'} candidates")


POOL_REASONS = ("fewer than 100 like races", "no earlier year to fit on", "a write-in line is in the pair",
                "a race between a Democrat and a Republican", "this route's p is calibrated")


def medsl_route(r):
    """Whether a local contest is one pipeline/local_medsl.py's routes forecast: MEDSL's own contests, and the State
    Board's North Carolina contests of MEDSL's general dates, which stand in place of MEDSL's (certified_nc). North
    Carolina's other dates are local_ncsbe.py's, whatever file holds them."""
    if r["src"] in ("medsl", "in_enr", "la_sos"):   # Indiana's own certified 2024 file stands in place of MEDSL's (#54, certified_in)
        return True
    return r["state"] == "NC" and r["src"] == "ncsbe" and (r["date"] or "")[5:7] == "11" and r["year"] in MEDSL_YEARS


def measure_route(r):
    """The same for a question: MEDSL's, or the State Board's of MEDSL's general dates in the measure years."""
    if r["src"] in ("medsl", "in_enr", "la_sos"):
        return True
    return r["state"] == "NC" and r["src"] == "ncsbe" and (r["date"] or "")[5:7] == "11" and r["year"] in MEASURE_YEARS


ODD_LA_YEARS = (2023,)   # Louisiana's odd year (#70). #75 feeds it into every later year's like races and measures (the default here); odd_la=False gives the rule between #70 and #75


def local_pools(odd_la=True):
    """(MEDSL pool, North Carolina pool): (year, key, s) rows from the local files. odd_la=True takes Louisiana's 2023
    rows (#70) into the MEDSL pool too; the record keeps them out of later years' like races (c22 measures both).
    MEDSL (pipeline/local_medsl.py local_rows): every contest of MEDSL's route (medsl_route) that local_structure
    sends to routes (b) or (c), with the recorded class and deciding pair, or both rebuilt from the ballot where the
    file records neither (a write-in in the deciding pair: the contest's own p is not computed, but it is a like race).
    North Carolina (local_ncsbe.py like_rows): the State Board's contests from 2014, on every date, including the
    November dates local_medsl.py builds; 'a Democrat against a Republican' is a class; a contest with a write-in in
    the deciding pair is left out. The files' 'built by' line names the build that wrote the year's file, so a State
    Board contest of May 2018 sits in a file local_medsl.py wrote: the route is read from the source and the date."""
    medsl, nc = [], []
    miss = collections.Counter()
    # since #60 (the orchestrator's ruling of 09:53) a November contest that follows an earlier round the same year is
    # that contest's deciding round: it takes the route's classes and enters the pool of like races; the earlier round
    # (its election 'first round: the same contest is on the ballot again on <date>') is not computed and, its reason
    # not being a pool reason, is not a pool row. Before #60 the State Board's route left the November contest out too.
    after_first = set()
    for r in D.rows("local"):
        if r["status"] == "value" and r["route"] is None:
            continue
        reason = r["reason"] or ""
        if r["status"] == "not_computed" and not any(reason.startswith(x) for x in POOL_REASONS):
            continue
        k = r["seats"] or 1
        pair = r["pair"]
        if pair:
            v0, v1 = pair["votes"]
        else:
            b = ballot_local(r)
            if len(b) <= k:
                miss["no pair on the ballot"] += 1
                continue
            v0, v1 = b[k - 1][1], b[k][1]
        if v0 + v1 <= 0:
            continue
        s = max(v0, v1) / (v0 + v1)
        if medsl_route(r):
            if r["src"] == "la_sos" and r["year"] in ODD_LA_YEARS and not odd_la:
                miss["Louisiana's odd year, kept out of later years' like races (#70)"] += 1
                continue
            if r["route"] in ("class", "boundary") or (r["cls"] and not r["route"]):
                medsl.append((r["year"], r["cls"], s))
            elif reason.startswith("a write-in line is in the pair"):
                st = structure_local(r)
                if st[0] in ("class", "boundary"):
                    medsl.append((r["year"], st[1], s))
                else:
                    miss[("write-in pair contest, my structure", st[0])] += 1
        if r["state"] == "NC" and r["year"] >= NC_FIRST:
            top = sorted([a for a in r["cands"] if a[1] is not None], key=lambda a: -a[1])
            if any(_generic(a[2]) for a in top[k - 1:k + 1]):
                continue
            if not medsl_route(r) and r["cls"]:
                nc.append((r["year"], r["cls"], s))
            else:
                st = structure_local(r, nc=True)
                if st[0] in ("class", "boundary", "partisan"):
                    nc.append((r["year"], st[1], s))
                else:
                    miss[("NC, my structure", st[0])] += 1
    return medsl, nc, miss


def like_local():
    h1("15.2 Like past races, local: like races counted again from the files [measured]")
    medsl, nc, miss = local_pools()
    print(f"  MEDSL pool {len(medsl):,} rows, years {sorted({y for y, _, _ in medsl})}; North Carolina State Board pool "
          f"{len(nc):,} rows, years {min(y for y, _, _ in nc)}-{max(y for y, _, _ in nc)}")
    print("  contests left out of the pools: " + ("; ".join(f"{k} {v}" for k, v in sorted(miss.items(), key=str)) or "none"))
    loc = D.rows("local")
    cm = [r for r in loc if r["route"] in ("class", "boundary") and r["N"] is not None and medsl_route(r)]
    cn = [r for r in loc if r["route"] in ("class", "boundary") and r["N"] is not None and not medsl_route(r)]
    compare_like(cm, medsl, "MEDSL's route (MEDSL years 2018-2024, all states, North Carolina's November contests from the State Board), like races from earlier MEDSL years")
    nc_pool = [row for row in nc if row[0] >= NC_FIRST]
    compare_like(cn, nc_pool, "North Carolina's route (the State Board's other dates), like races from the State Board's 2014 on")
    return medsl, nc


# ------------------------------------------------------------------------------------------ measures
YES_WORDS = {"YES", "FOR", "APPROVE", "APPROVED", "ACCEPT", "RETAIN", "BONDS YES", "YES ON", "FOR THE MEASURE",
             "IN FAVOR", "IN FAVOR OF", "YES FOR APPROVAL"}
NO_WORDS = {"NO", "AGAINST", "REJECT", "REJECTED", "NOT RETAIN", "DO NOT RETAIN", "BONDS NO", "NO ON",
            "AGAINST THE MEASURE", "OPPOSED", "NO FOR REJECTION"}
_POS = re.compile(r"^(YES|FOR|IN FAVOR)\b")
_NEG = re.compile(r"^(NO|AGAINST|OPPOSED)\b(?! (NAME|CANDIDATE))")


def side(name):
    """'yes', 'no' or None for an answer line, by the answer words the pipeline reads (local_medsl.py side: the words,
    or a line that begins with one, 'FOR BONDS', 'AGAINST PROPOSED TAXATION')."""
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


# a state whose year's source fails its check is left out of that year's pools (local_medsl.py build: bad[year]); the
# files carry the fault as each contest's reason ("the source's 2022 file for this state ...", "the source's 2024
# counts for this state do not add up ...", "the source's 2022 state legislative returns for this state differ ...")
_STATE_FAULT = re.compile(r"^the source's \d{4} .*this state")


def measure_pool(odd_la=True):
    """(year, key, yes share) rows of the measure files on MEDSL's route (measure_route): every question of the measure
    years with yes or no votes, statewide or local (partial left out; a question the source gives one answer of, and a
    state whose counts do not add up that year, left out), as pipeline/measures.py rows counts them. Louisiana's 2023
    questions (#70) only with odd_la=True: the record keeps them out of later years' like measures."""
    pool = []
    for r in D.rows("measure"):
        if not measure_route(r) or not r["question"]:
            continue
        if r["src"] == "la_sos" and r["year"] in ODD_LA_YEARS and not odd_la:
            continue
        q = r["question"]
        reason = r["reason"] or ""
        if q.get("scope") == "partial" or reason.startswith("the source gives one answer only") or _STATE_FAULT.match(reason):
            continue
        yes = sum(a[1] or 0 for a in r["cands"] if side(a[2]) == "yes")
        no = sum(a[1] or 0 for a in r["cands"] if side(a[2]) == "no")
        if yes + no <= 0:
            continue
        pool.append((r["year"], f"{q.get('scope')} {q.get('kind')}", yes / (yes + no), r["id"]))
    return pool


def measures():
    h1("15.3 Statewide measures: like past measures at the threshold, and backtest-measures.json reproduced [measured]")
    pool = measure_pool()
    yk = collections.Counter((y, k) for y, k, _, _ in pool)
    print("  pool rows by year and class: " + "; ".join(f"{y} {k} {v}" for (y, k), v in sorted(yk.items())))
    by_key = collections.defaultdict(list)
    for y, k, s, _ in pool:
        by_key[k].append((y, s))
    ms = [r for r in D.rows("measure") if r["route"] == "like past measures" and r["status"] == "value"]
    tal, bad = collections.Counter(), []
    for r in ms:
        t, key = r["year"], r["cls"]
        if key.startswith("local "):   # #77's local classes (local measure, NC / LA): their pools and p are c27's
            tal["local class (c27's)"] += 1
            continue
        sh = [s for y, s in by_key[key] if y < t]
        f, N, h, k = D.density_at(sh, r["t"])
        if f is None:
            tal["too few"] += 1
            continue
        same = (N == r["N"], k == r["kin"], abs(h - D.window_h(r["win"])) < 1e-9, abs(round(k / N, 5) - r["q"]) < 1e-9,
                D.rel(f, r["p"]["f_t"]) <= 1e-5)
        tal[same] += 1
        if not all(same):
            bad.append((r["id"], f"mine N {N} k {k} h {h} q {k / N:.5f} f {f:.6g}; record N {r['N']} k {r['kin']} h {D.window_h(r['win'])} q {r['q']} f_t {r['p']['f_t']}"))
    print(f"  {len(ms)} measures with p: (N, k, h, q, f_t) all equal in {tal[(True,) * 5]}; other outcomes {dict((str(k), v) for k, v in tal.items() if k != (True,) * 5)}")
    for rid, s in bad[:10]:
        print(f"    {rid}: {s}")
    # backtest-measures.json: near 1/2 for every statewide question with a trained class; at the threshold for those with p
    rec = json.load(open(os.path.join(M.DATA, "measure", "backtest-measures.json")))
    half = {}
    for y, key, s, rid in pool:
        if not key.startswith("statewide") or y not in MEASURE_YEARS:
            continue
        tr = [x for yy, x in by_key[key] if yy < y]
        if not tr:
            continue
        g = half.setdefault(f"{y} {key} (trained on {len(tr)})", {"measures": 0, "near": {str(hh): [0.0, 0] for hh in D.WINDOWS}})
        g["measures"] += 1
        for hh in D.WINDOWS:
            g["near"][str(hh)][0] += sum(1 for x in tr if abs(x - 0.5) <= hh) / len(tr)
            g["near"][str(hh)][1] += int(abs(s - 0.5) <= hh)
    print("  near 1/2 (every statewide question whose class has earlier years): mine | record")
    for k in sorted(half):
        mine = half[k]
        got = rec["near_half"].get(k)
        mstr = ", ".join(f"within {float(hh):.0%} {v[0]:.1f}/{v[1]}" for hh, v in mine["near"].items())
        rstr = (", ".join(f"within {hh} {v['expected']}/{v['seen']}" for hh, v in got["near"].items()) + f" ({got['measures']})") if got else "absent"
        print(f"    {k:48s} {mine['measures']:4d}: {mstr} | {rstr}")
    at = {}
    for r in ms:
        y, key, t = r["year"], r["cls"], r["t"]
        if key.startswith("local "):   # c27's
            continue
        tr = [x for yy, x in by_key[key] if yy < y]
        if not tr:
            continue
        v0, v1 = r["pair"]["votes"]
        s = v0 / (v0 + v1)
        h = D.window_h(r["win"])
        for grp in (str(y), "all years"):
            g = at.setdefault(grp, {"measures": 0, "own": [0.0, 0], "near": {str(hh): [0.0, 0] for hh in D.WINDOWS}})
            g["measures"] += 1
            g["own"][0] += r["q"]
            g["own"][1] += int(abs(s - t) <= h + 1e-12)
            for hh in D.WINDOWS:
                g["near"][str(hh)][0] += sum(1 for x in tr if abs(x - t) <= hh) / len(tr)
                g["near"][str(hh)][1] += int(abs(s - t) <= hh)
    print("  at the threshold (measures given p): mine | record")
    for grp in sorted(at):
        g, got = at[grp], rec["at_threshold"].get(grp)
        mstr = f"own window {g['own'][0]:.1f}/{g['own'][1]}, " + ", ".join(f"within {float(hh):.0%} {v[0]:.1f}/{v[1]}" for hh, v in g["near"].items())
        rstr = (f"own window {got['own_window']['expected']}/{got['own_window']['seen']}, " + ", ".join(f"within {hh} {v['expected']}/{v['seen']}" for hh, v in got["near_threshold"].items())) if got else "absent"
        print(f"    {grp:10s} {g['measures']:3d}: {mstr} | {rstr}")
    # the threshold form against a plain near-1/2 count (MODEL section 7): what the form does at t away from 1/2
    ts = collections.Counter(r["t"] for r in ms)
    print(f"  thresholds among the measures with p: {dict(sorted(ts.items()))}; at t = 0.5 yes = no = f/(2n) (the two-way form); "
          f"at t = 0.6 a Yes ballot's p is 0.4 f/n and a No ballot's 0.6 f/n, which is MODEL section 7's form.")


# ------------------------------------------------------------------------------------------ route (a) from Klarner
def klarner_rows():
    """Route (a)'s rows from Klarner's contest file, as REPORT section 2 defines them: single-seat generals (g, gs,
    ssg) with one Democrat and one Republican on the ballot, both with votes, every candidate's votes reported."""
    path, _ = M.fetch(KLARNER_URL, KLARNER_FILE, KLARNER_SHA)
    rows = []
    with open(path, newline="") as fh:
        for row in csv.DictReader(fh):
            if row["etype"] not in ("g", "gs", "ssg") or row["eseats"] != "1" or row["vmiss"] == "1":
                continue
            if row["dcand"] != "1" or row["rcand"] != "1":
                continue
            d, r = int(row["dvote"] or 0), int(row["rvote"] or 0)
            if d <= 0 or r <= 0:
                continue
            lag = float(row["dperlag"]) if row["dperlag"] != "" else None
            ul = row["uncontlag"]
            if lag is None:
                cls, xl, ulag = "C", 0.0, 0
            elif ul == "1":
                cls, xl, ulag = "B", 0.0, (1 if lag > 50 else -1)
            else:
                cls, xl, ulag = "A", lag / 100.0 - 0.5, 0
            rows.append({"year": int(row["year"]), "state": row["sab"], "sen": int(row["sen"]), "y": d / (d + r), "N": d + r,
                         "d": d, "r": r, "cls": cls, "xl": xl, "ulag": ulag, "inc": int(row["inc"] or 0), "lag": lag,
                         "last_year": int(row["yearmaxlag"]) if row["yearmaxlag"] else None,
                         "N_lag": (int(row["dvotelag"] or 0) + int(row["rvotelag"] or 0)) if row["dvotelag"] and row["rvotelag"] else None,
                         "ocand": int(row["ocand"] or 0), "ovote": int(row["ovote"] or 0),
                         "dist": (row["dname"], row["dno"], row["geopost"], row["mmdpost"])})
    by = collections.defaultdict(list)
    for r_ in rows:
        by[(r_["state"], r_["sen"], r_["year"])].append(r_["y"])
    years = collections.defaultdict(list)
    for (s, sen, t) in by:
        years[(s, sen)].append(t)
    prev = {}
    for k, ts in years.items():
        ts.sort()
        for a, b in zip(ts, ts[1:]):
            prev[(k[0], k[1], b)] = (float(np.mean(by[(k[0], k[1], a)])) - 0.5, a)
    for r_ in rows:
        L = prev.get((r_["state"], r_["sen"], r_["year"]))
        r_["L"], r_["L_year"], r_["Lmiss"] = (L[0], L[1], 0) if L else (0.0, None, 1)
    return rows, by


def ballot_rows_by_chamber_year():
    """Route (a)'s rows counted from the state files' candidate rows as pipeline/local.py partisan_rows selects them
    (on_ballot: every named candidate but a write-in; exactly one Democrat and one Republican; single-seat general-type
    contests, every candidate's votes reported), by (year, state, chamber)."""
    out = collections.Counter()
    for level, sen in (("state-lower", 0), ("state-upper", 1)):
        for r in D.rows(level):
            if r["src"] != "klarner" or (r["seats"] or 1) != 1:
                continue
            if r["election"] not in ("general", "special general of the whole chamber", "general, for the rest of a term"):
                continue
            named = [a for a in r["cands"] if a[0] != "write-in"]
            if any(a[1] is None for a in named):
                continue
            ds = [a for a in named if a[0] == "D"]
            rs = [a for a in named if a[0] == "R"]
            if len(ds) != 1 or len(rs) != 1 or (ds[0][1] or 0) <= 0 or (rs[0][1] or 0) <= 0:
                continue
            out[(r["year"], r["state"], sen)] += 1
    return out


def design(rows, ys):
    yi = {t: i for i, t in enumerate(ys)}
    k = len(ys)
    j = {c: k + i for i, c in enumerate(COLS)}
    X = np.zeros((len(rows), k + len(COLS)))
    for i, r_ in enumerate(rows):
        X[i, yi[r_["year"]]] = 1
        c = r_["cls"]
        if c == "A":
            X[i, j["A_last"]], X[i, j["A_inc"]], X[i, j["A_lean"]] = r_["xl"], r_["inc"], r_["L"]
        elif c == "B":
            X[i, j["B"]], X[i, j["B_unopposed"]], X[i, j["B_inc"]], X[i, j["B_lean"]] = 1, r_["ulag"], r_["inc"], r_["L"]
        else:
            X[i, j["C"]], X[i, j["C_inc"]], X[i, j["C_lean"]] = 1, r_["inc"], r_["L"]
        X[i, j["lean_missing"]] = r_["Lmiss"]
    return X, yi, j


def fit_partisan(rows):
    """REPORT section 2's fit: OLS with a dummy per year; the swing per kind of year on the president's party; s_a
    from the swing's residuals; s_g from the state-chamber-year group means; s_e by class and size bin."""
    ys = sorted({r_["year"] for r_ in rows})
    X, yi, j = design(rows, ys)
    y = np.array([r_["y"] - 0.5 for r_ in rows])
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ b
    coef = {c: float(b[j[c]]) for c in COLS}
    ye = {t: float(b[yi[t]]) for t in ys}
    swing, resid, df, n_kind = {}, [], 0, {}
    for cy in ("presidential", "midterm", "odd"):
        ts = [t for t in ys if cycle(t) == cy and t in PRES]
        n_kind[cy] = len(ts)
        if not ts:
            continue
        v = np.array([ye[t] for t in ts])
        if len(ts) >= 2 and len({PRES[t] for t in ts}) > 1:
            A, npar = np.array([[1.0, PRES[t]] for t in ts]), 2
        else:
            A, npar = np.ones((len(ts), 1)), 1
        s, *_ = np.linalg.lstsq(A, v, rcond=None)
        swing[cy] = (float(s[0]), float(s[1]) if npar == 2 else 0.0)
        resid += list(v - A @ s)
        df += len(ts) - npar
    s_a = math.sqrt(sum(e * e for e in resid) / df) if df > 0 else None
    groups = collections.defaultdict(list)
    for i, r_ in enumerate(rows):
        groups[(r_["state"], r_["sen"], r_["year"])].append(i)
    within = [float(res[ix].var(ddof=1)) for ix in groups.values() if len(ix) > 1]
    se2 = float(np.mean(within))
    gm = np.array([res[ix].mean() for ix in groups.values()])
    gn = np.array([len(ix) for ix in groups.values()])
    s_g = math.sqrt(max(float(np.mean(gm ** 2 - se2 / gn)), 0.0))
    w = collections.defaultdict(list)
    for ix in groups.values():
        if len(ix) < 2:
            continue
        mu, f = res[ix].mean(), len(ix) / (len(ix) - 1)
        for i in ix:
            w[(rows[i]["cls"], D.size_bin(rows[i]["N"]))].append((res[i] - mu) ** 2 * f)
    s_e = {f"{c}{b_}": math.sqrt(float(np.mean(v))) for (c, b_), v in w.items()}
    return {"coef": coef, "swing": swing, "s_a": s_a, "s_g": s_g, "s_e": s_e, "n_kind": n_kind, "years": ys, "races": len(rows)}


def predict(Mfit, r_):
    c, t = Mfit["coef"], r_["year"]
    sw = Mfit["swing"][cycle(t)]
    a = sw[0] + sw[1] * PRES[t]
    m = 0.5 + a + c["lean_missing"] * r_["Lmiss"]
    if r_["cls"] == "A":
        m += c["A_last"] * r_["xl"] + c["A_inc"] * r_["inc"] + c["A_lean"] * r_["L"]
    elif r_["cls"] == "B":
        m += c["B"] + c["B_unopposed"] * r_["ulag"] + c["B_inc"] * r_["inc"] + c["B_lean"] * r_["L"]
    else:
        m += c["C"] + c["C_inc"] * r_["inc"] + c["C_lean"] * r_["L"]
    se = Mfit["s_e"].get(f"{r_['cls']}{D.size_bin(r_['N'])}") or max(Mfit["s_e"].values())
    sd = math.sqrt(Mfit["s_a"] ** 2 + Mfit["s_g"] ** 2 + se ** 2)
    return min(max(m, 0.001), 0.999), sd, a


def partisan():
    h1("15.4 Route (a), partisan: rows from Klarner's contest file, the fit per year on earlier years only, every contest against the record [measured]")
    rows, by = klarner_rows()
    cc = collections.Counter(r_["cls"] for r_ in rows)
    print(f"  Klarner file 10273086 ({KLARNER_FILE}, sha256 {KLARNER_SHA[:12]}...): {len(rows):,} route-(a) rows "
          f"{min(r_['year'] for r_ in rows)}-{max(r_['year'] for r_ in rows)}; by class A {cc['A']:,} B {cc['B']:,} C {cc['C']:,} "
          f"(REPORT section 2: A 49,001, B 14,350, C 27,602)")
    Mall = fit_partisan(rows)
    c = Mall["coef"]
    print(f"  the fit on all years: A last {c['A_last']:.3f}, inc {c['A_inc']:.3f}, lean {c['A_lean']:.3f}; B unopposed {c['B_unopposed']:.3f}, "
          f"inc {c['B_inc']:.3f}, lean {c['B_lean']:.3f}; C inc {c['C_inc']:.3f}, lean {c['C_lean']:.3f}; lean missing {c['lean_missing']:.4f}")
    print("  s_e by class and size: " + ", ".join(f"{k} {v:.3f}" for k, v in sorted(Mall["s_e"].items())))
    sw = Mall["swing"]
    print(f"  swing, as the president's party's change: presidential {sw['presidential'][1] * 2 * 100:+.1f} points? no: the fit's terms are "
          f"(mean, x president's party): presidential ({sw['presidential'][0]:+.4f}, {sw['presidential'][1]:+.4f}), midterm "
          f"({sw['midterm'][0]:+.4f}, {sw['midterm'][1]:+.4f}), odd ({sw['odd'][0]:+.4f}, {sw['odd'][1]:+.4f}); s_a {Mall['s_a']:.4f}, s_g {Mall['s_g']:.4f} "
          f"(REPORT section 2: A 0.752/0.034/0.038, B 0.108/0.049/0.358, C 0.118/0.375; s_a 0.027, s_g 0.027)")
    # the fit per year, on earlier years only
    fits = {}
    for t in range(1969, 2025):
        train = [r_ for r_ in rows if r_["year"] < t]
        if not train or t not in PRES:
            continue
        Mf = fit_partisan(train)
        k = Mf["n_kind"].get(cycle(t), 0)
        fits[t] = (Mf if (Mf["s_a"] is not None and cycle(t) in Mf["swing"]) else None, k)
    # every contest with a partisan forecast: Klarner years by (year, state, chamber, D votes, R votes)
    index = collections.defaultdict(list)
    for r_ in rows:
        index[(r_["year"], r_["state"], r_["sen"], r_["d"], r_["r"])].append(r_)
    tal = collections.Counter()
    worst = []
    for level in ("state-upper", "state-lower"):
        sen = 1 if level == "state-upper" else 0
        for r in D.rows(level):
            if r["route"] != "partisan" or not r["share"]:
                continue
            v = r["pair"]["votes"]
            inp = r["inputs"] or {}
            if r["src"] == "klarner":
                cands = index.get((r["year"], r["state"], sen, v[0], v[1]), [])
                if len(cands) != 1:
                    tal[f"klarner: matched {len(cands)} rows"] += 1
                    continue
                r_ = cands[0]
                fit, k = fits.get(r["year"], (None, 0))
                if fit is None or k < MIN_EARLIER:
                    tal["klarner: no fit for the year (mine)"] += 1
                    continue
                same_in = (r_["cls"] == inp.get("class"), r_["inc"] == inp.get("incumbency"), abs(r_["L"] - inp.get("lean", 9)) <= 5.1e-5,
                           r_["L_year"] == inp.get("lean_year"),
                           (r_["cls"] != "A") or abs(r_["xl"] + 0.5 - inp.get("last_D", 9)) <= 5.1e-5,
                           (r_["cls"] == "C") or r_["last_year"] == inp.get("last_year"),
                           (r_["cls"] != "B") or inp.get("last_unopposed") == ("D" if r_["ulag"] > 0 else "R"))
                tal[("klarner inputs", same_in)] += 1
            else:
                fit, k = fits.get(2024, (None, 0))
                cls = inp.get("class")
                r_ = {"year": r["year"], "cls": cls, "inc": inp.get("incumbency", 0), "L": inp.get("lean", 0.0),
                      "Lmiss": 0 if inp.get("lean_year") else 1, "N": v[0] + v[1],
                      "xl": (inp.get("last_D", 0.5) - 0.5) if cls == "A" else 0.0,
                      "ulag": (1 if inp.get("last_unopposed") == "D" else -1) if cls == "B" else 0}
                Lk = by.get((r["state"], sen, 2022))
                lean22 = (float(np.mean(Lk)) - 0.5) if Lk else None
                tal[("2024 lean = Klarner 2022 chamber mean", lean22 is not None and abs(lean22 - inp.get("lean", 9)) <= 5.1e-5 and inp.get("lean_year") == 2022)] += 1
            mean, sd, a = predict(fit, r_)
            dm, ds, da = abs(mean - r["share"]["mean"]), abs(sd - r["share"]["sd"]), abs(a - inp.get("swing", 9))
            worst_d = max(dm, ds, da)
            band = ("within rounding (5e-5)" if worst_d <= 5.1e-5 else "within 5e-4" if worst_d <= 5e-4 else
                    "within 5e-3" if worst_d <= 5e-3 else "beyond 5e-3")
            lean_same = (r["src"] != "klarner") or abs(r_["L"] - inp.get("lean", 9)) <= 5.1e-5
            tal[(r["src"], "mean, sd, swing", band, "lean equal" if lean_same else "lean differs")] += 1
            if band == "beyond 5e-3" or (band == "within 5e-3" and lean_same):
                worst.append((worst_d, r["id"], f"mine mean {mean:.5f} sd {sd:.5f} swing {a:.5f}; record {r['share']['mean']} {r['share']['sd']} {inp.get('swing')}; lean mine {r_['L']:.4f} record {inp.get('lean')}"))
    print("  contests with a partisan forecast against my refit (the record's mean and sd carry 4 decimals; a fit on rows that differ by")
    print("  a few of 90,000 moves every mean by about 1e-4, so 'within 5e-4' is the same fit within the rows' difference):")
    for k_, v in sorted(tal.items(), key=str):
        print(f"    {str(k_):90s} {v:,}")
    worst.sort(key=lambda x: -x[0])
    for _, rid, s in worst[:12]:
        print(f"    {rid}: {s}")
    # the rows (D3's #59; REPORT section 2): pipeline/local.py on_ballot returns every named candidate but a write-in,
    # and partisan_rows keeps the contests with exactly one Democrat and one Republican among them; mine keep Klarner's
    # contest-level dcand = rcand = 1. The two differ where Klarner's dcand/rcand disagree with its own candidate rows
    # (D3: 30 contests). Counted by chamber and year from the state files' candidate rows:
    files_cnt = ballot_rows_by_chamber_year()
    mine_cnt = collections.Counter((r_["year"], r_["state"], r_["sen"]) for r_ in rows)
    diff = {k: (mine_cnt.get(k, 0), files_cnt.get(k, 0)) for k in set(mine_cnt) | set(files_cnt) if mine_cnt.get(k, 0) != files_cnt.get(k, 0)}
    print(f"  the rows: mine {sum(mine_cnt.values()):,} (Klarner's contest-level dcand = rcand = 1); from the files' candidate rows as pipeline/local.py")
    print(f"  on_ballot reads them (every named candidate but a write-in; exactly one Democrat and one Republican; single-seat generals; every vote")
    print(f"  reported) {sum(files_cnt.values()):,}; chamber-years where the two counts differ: {len(diff)}, rows {sum(abs(a - b) for a, b in diff.values())}: "
          + "; ".join(f"{st} {'upper' if sen else 'lower'} {y} {a}/{b}" for (y, st, sen), (a, b) in sorted(diff.items())[:40]))
    print("  (D3's #59: the pipeline's rows follow the ballot, as REPORT section 2 says; 30 contests differ from mine where Klarner's dcand/rcand")
    print("   disagree with its candidate rows: 12 with two Republicans in the rows and rcand 1, 11 with a Republican of a few votes and rcand 0,")
    print("   7 others. The chamber lean differs where those rows sit, which is the tally above; my reading 10.8 of 09:34 was wrong on the rule.)")
    # the back-test by earlier years of the kind (REPORT section 3's table), from my fits
    bt = collections.defaultdict(lambda: [0, 0, 0.0, 0, 0.0, 0])
    for r_ in rows:
        fit, k = fits.get(r_["year"], (None, 0))
        if fit is None or k < 1:
            continue
        mean, sd, a = predict(fit, r_)
        key = str(k) if k <= 5 else "6-9" if k <= 9 else "10 or more"
        b = bt[key]
        b[0] += 1
        b[1] += int(abs(r_["y"] - mean) <= Z["50"] * sd)
        b[2] += stats.norm.cdf(0.51, mean, sd) - stats.norm.cdf(0.49, mean, sd)
        b[3] += int(abs(r_["y"] - 0.5) <= 0.01)
        N = r_["N"]
        b[4] += stats.norm.cdf(0.5 + 50 / N, mean, sd) - stats.norm.cdf(0.5 - 50 / N, mean, sd)
        b[5] += int(abs(r_["d"] - r_["r"]) <= 100)
    print("  back-test by earlier years of the kind (mine; REPORT section 3: 1: 6,118 51% 319/316 183/175; 2: 6,129 47% 275/282 152/172; "
          "3: 6,325 52% 294/312 148/167; 4: 6,284 52% 263/270 137/161; 5: 6,384 55% 239/291 130/166; 6-9: 26,379 55% 1,166/1,180 589/661; "
          "10+: 27,184 58% 1,199/1,210 478/518):")
    for key in ("1", "2", "3", "4", "5", "6-9", "10 or more"):
        b = bt[key]
        if b[0]:
            print(f"    {key:11s} {b[0]:6,} in 50% {100 * b[1] / b[0]:.0f}%; 49-51% {b[2]:.0f}/{b[3]}; within 100 votes {b[4]:.0f}/{b[5]}")
    return rows, fits, Mall


# ------------------------------------------------------------------------------------------ the #31 factor
def near_half_local():
    """(group, year, office key, expected near 1/2, seen) for every MEDSL-built local record with a forecast
    (pipeline/local_medsl.py _near_half: the class's window for like races, 49-51% for the partisan route)."""
    out = collections.defaultdict(list)
    for r in D.rows("local"):
        if r["by"] != "pipeline/local_medsl.py" or not r["route"] or not r["pair"] or not medsl_route(r):
            continue   # local_ncsbe.py's contests on North Carolina's other dates sit in the same files; not that build's
        v0, v1 = r["pair"]["votes"]
        if r["route"] in ("class", "boundary") and r["N"] is not None:
            s = v0 / (v0 + v1)
            out[("like races", r["year"])].append((r, f"{r['route']}, {r['office_scope']} {r['office_type']}", r["q"],
                                                   r["win"][0] <= round(s, 6) <= r["win"][1]))
        elif r["route"] == "partisan" and r["share"]:
            m, sd = r["share"]["mean"], r["share"]["sd"]
            e = stats.norm.cdf(0.51, m, sd) - stats.norm.cdf(0.49, m, sd)
            out[("partisan", r["year"])].append((r, f"partisan, {r['office_scope']} {r['office_type']}", e, abs(v0 / (v0 + v1) - 0.5) <= 0.01))
    return out


def deviance(pairs):
    d = 0.0
    for e, s_ in pairs:
        if e <= 0:
            continue
        d += 2 * ((s_ * math.log(s_ / e) if s_ > 0 else 0.0) - (s_ - e))
    return d


def factor_fit(recs, group, fit_years):
    by = collections.defaultdict(lambda: [0.0, 0])
    for y in fit_years:
        for _, key, e, seen in recs.get((group, y), []):
            by[key][0] += e
            by[key][1] += seen
    pe, ps = sum(v[0] for v in by.values()), sum(v[1] for v in by.values())
    own = {k: v[1] / v[0] for k, v in by.items() if v[0] >= CAL_MIN_EXPECTED}
    return {"pooled": ps / pe if pe else 1.0, "own": own, "counts": dict(by)}


def factor_test(recs, group, test_year, f):
    by_b = collections.defaultdict(lambda: [0.0, 0.0, 0])
    for _, key, e, seen in recs.get((group, test_year), []):
        k = f["own"].get(key, f["pooled"])
        by_b[key][0] += e
        by_b[key][1] += e * k
        by_b[key][2] += seen
    eb, ea, sn = (sum(v[i] for v in by_b.values()) for i in range(3))
    db, da = deviance([(v[0], v[2]) for v in by_b.values()]), deviance([(v[1], v[2]) for v in by_b.values()])
    adopt = abs(ea - sn) < abs(eb - sn) and da < db
    worse = {k: (round(v[0], 1), round(v[1], 1), v[2]) for k, v in by_b.items() if abs(v[1] - v[2]) > abs(v[0] - v[2]) + 1e-9}
    return {"contests": sum(1 for _ in recs.get((group, test_year), [])), "seen": sn, "before": eb, "after": ea, "dev_before": db,
            "dev_after": da, "adopt": adopt, "cells_worse": worse, "cells": len(by_b)}


def cal_score(recs, group, years, factors):
    """pipeline/local_medsl.py _cal_score (#59): the factors' out-of-sample test over the scored years, each year with its
    own factor; a tested cell is an office type with 5 or more seen or expected."""
    by_b = collections.defaultdict(lambda: [0.0, 0.0, 0])
    n = 0
    for t in years:
        f_t = factors[t]
        for _, key, e, seen in recs.get((group, t), []):
            k = f_t["own"].get(key, f_t["pooled"])
            by_b[key][0] += e
            by_b[key][1] += e * k
            by_b[key][2] += seen
            n += 1
    eb, ea, sn = (sum(v[i] for v in by_b.values()) for i in range(3))
    db, da = deviance([(v[0], v[2]) for v in by_b.values()]), deviance([(v[1], v[2]) for v in by_b.values()])
    worse = sorted(k for k, v in by_b.items() if max(v[0], v[2]) >= 5 and abs(v[1] - v[2]) > abs(v[0] - v[2]))
    improves = abs(ea - sn) < abs(eb - sn) and da < db
    return {"contests": n, "seen": sn, "before": eb, "after": ea, "dev_before": db, "dev_after": da, "improves": improves,
            "worse": worse, "passes": bool(improves and not worse)}


def calibration():
    h1("15.5 The #31 calibration factor (the orchestrator, 06:38): recomputed, the 2024 test, leave-one-year-out [measured]")
    recs = near_half_local()
    rec = json.load(open(os.path.join(M.DATA, "local", "calibration-local.json")))["routes"]
    for group in ("like races", "partisan"):
        years = sorted(y for g, y in recs if g == group)
        print(f"\n  {group}: forecasts by year " + ", ".join(f"{y} {len(recs[(group, y)]):,} (expected {sum(x[2] for x in recs[(group, y)]):.1f}, seen {sum(x[3] for x in recs[(group, y)])})" for y in years))
        for t in years:
            fy = [y for y in years if y < t]
            if not fy:
                continue
            f = factor_fit(recs, group, fy)
            got = rec[group]["factors"].get(str(t)) or {}
            print(f"    factor for {t}, fitted on {fy}: pooled {f['pooled']:.3f} (record {got.get('pooled')}); own "
                  + ", ".join(f"{k.split(', ', 1)[1]} {v:.3f}" for k, v in sorted(f["own"].items())) + f" (record {got.get('own')})")
        if 2024 in years:
            fy = [y for y in years if y < 2024]
            f = factor_fit(recs, group, fy)
            T = factor_test(recs, group, 2024, f)
            got = rec[group].get("test", {})
            print(f"    the 2024 test: {T['contests']:,} contests, seen {T['seen']}, expected before {T['before']:.1f} after {T['after']:.1f}; "
                  f"deviance {T['dev_before']:.2f} -> {T['dev_after']:.2f}; adopt {T['adopt']} (the record's test is over every scored year since #59: below)")
            print(f"    cells (office types) the factor moves further from what was seen: {len(T['cells_worse'])} of {T['cells']}: "
                  + "; ".join(f"{k.split(', ', 1)[1]}: {v[0]} -> {v[1]} vs {v[2]}" for k, v in T["cells_worse"].items()))
            # leave one scored year out (the orchestrator, 08:35)
            print("    leave-one-year-out (the orchestrator's robustness test of 08:35):")
            for left in years:
                if left == 2024:
                    # the test year itself left out: the latest earlier year becomes the test, fitted on the years before it
                    tests = [y for y in years if y < 2024]
                    ty = tests[-1]
                    fy2 = [y for y in years if y < ty]
                    if not fy2:
                        print(f"      leave out 2024: no earlier year has both a fitting year and a test year (years {years}); the test cannot run")
                        continue
                    f2 = factor_fit(recs, group, fy2)
                    T2 = factor_test(recs, group, ty, f2)
                    print(f"      leave out 2024 -> test {ty} with the factor fitted on {fy2} (pooled {f2['pooled']:.3f}): {T2['contests']:,} contests, "
                          f"seen {T2['seen']}, expected {T2['before']:.1f} -> {T2['after']:.1f}, deviance {T2['dev_before']:.2f} -> {T2['dev_after']:.2f}; "
                          f"adopt {T2['adopt']}; cells worse {len(T2['cells_worse'])} of {T2['cells']}")
                else:
                    fy2 = [y for y in fy if y != left]
                    if not fy2:
                        print(f"      leave out {left}: no fitting year remains ({fy}); the factor cannot be fitted")
                        continue
                    f2 = factor_fit(recs, group, fy2)
                    T2 = factor_test(recs, group, 2024, f2)
                    print(f"      leave out {left} -> fitted on {fy2} (pooled {f2['pooled']:.3f}, own "
                          + ", ".join(f"{k.split(', ', 1)[1]} {v:.3f}" for k, v in sorted(f2["own"].items()))
                          + f"): test 2024 seen {T2['seen']}, expected {T2['before']:.1f} -> {T2['after']:.1f}, deviance {T2['dev_before']:.2f} -> {T2['dev_after']:.2f}; "
                          f"adopt {T2['adopt']}; cells worse {len(T2['cells_worse'])} of {T2['cells']}: "
                          + "; ".join(f"{k.split(', ', 1)[1]} {v[0]}->{v[1]} vs {v[2]}" for k, v in T2["cells_worse"].items()))
        # D3's robustness test as calibration-local.json records it since #59 (each route's test and leave_one_year_out): every
        # year with a factor is scored with its own factor (fitted on the years before it); it improves where the count near 1/2
        # comes nearer and the deviance falls; a tested cell (5 or more seen or expected) may not move further; and again with
        # any one scored year left out (a route with one scored year fails)
        factors = {}
        for t in years:
            fy = [y for y in years if y < t]
            if fy and recs.get((group, t)):
                factors[t] = factor_fit(recs, group, fy)
        scored = sorted(factors)
        got = rec[group].get("test") or {}
        if scored:
            T3 = cal_score(recs, group, scored, factors)
            print(f"    the robustness test (#59; every scored year with its own factor; a tested cell has 5 or more seen or expected): years {scored} (record {got.get('years')});")
            print(f"      {T3['contests']:,} contests (record {got.get('contests')}), seen {T3['seen']} ({got.get('seen_near_half')}), expected {T3['before']:.1f} -> {T3['after']:.1f} "
                  f"({got.get('expected_before')} -> {got.get('expected_after')}), deviance {T3['dev_before']:.2f} -> {T3['dev_after']:.2f} "
                  f"({got.get('deviance_by_office_type_before')} -> {got.get('deviance_after')}); improves {T3['improves']} ({got.get('improves')}); "
                  f"tested cells made worse {[k.split(', ', 1)[1] for k in T3['worse']]} ({[k.split(', ', 1)[1] for k in got.get('tested_cells_made_worse') or []]}); "
                  f"passes {T3['passes']} ({got.get('passes')})")
            lo_rec = rec[group].get("leave_one_year_out") or {}
            loo_pass = []
            for t in scored:
                rest = [y for y in scored if y != t]
                g2 = lo_rec.get(str(t)) or {}
                if not rest:
                    loo_pass.append(False)
                    print(f"      without {t}: no scored year is left, so it fails (record: passes {g2.get('passes')}; {g2.get('why')})")
                    continue
                T4 = cal_score(recs, group, rest, factors)
                loo_pass.append(T4["passes"])
                print(f"      without {t}: {T4['contests']:,} contests ({g2.get('contests')}), seen {T4['seen']} ({g2.get('seen_near_half')}), expected "
                      f"{T4['before']:.1f} -> {T4['after']:.1f} ({g2.get('expected_before')} -> {g2.get('expected_after')}); tested cells made worse "
                      f"{[k.split(', ', 1)[1] for k in T4['worse']]} ({[k.split(', ', 1)[1] for k in g2.get('tested_cells_made_worse') or []]}); passes {T4['passes']} ({g2.get('passes')})")
            print(f"      adopted under the rule: mine {bool(T3['passes'] and all(loo_pass))}; the record: no factor of record for this route (each p the "
                  f"factor would move carries calibration_not_of_record)")
        for t in scored:
            got_f = (rec[group]["factors"].get(str(t)) or {}).get("fit_counts_expected_seen") or {}
            mine_c = factors[t]["counts"]
            diffs = [(k, round(v[0], 1), v[1], got_f.get(k)) for k, v in sorted(mine_c.items())
                     if got_f.get(k) is None or abs(got_f[k][0] - v[0]) > 0.051 or got_f[k][1] != v[1]]
            print(f"    the fitting counts (expected, seen) by office type behind {t}'s factor: {len(mine_c)} types, {len(diffs)} differ from the record's "
                  f"fit_counts_expected_seen" + (": " + "; ".join(f"{k.split(', ', 1)[1]} mine {e}/{s_} record {g}" for k, e, s_, g in diffs[:6]) if diffs else ""))
    # North Carolina's own: data/local/backtest-ncsbe.json 'calibration' (local: each year with 30 or more expected in earlier years)
    nc = collections.defaultdict(list)
    for r in D.rows("local"):
        if r["by"] != "pipeline/local_ncsbe.py" or r["route"] not in ("class", "boundary") or r["N"] is None or not r["pair"]:
            continue
        v0, v1 = r["pair"]["votes"]
        s = v0 / (v0 + v1)
        nc[r["year"]].append((r["q"], int(r["win"][0] <= round(s, 6) <= r["win"][1])))
    seen = e_raw = e_cal = 0.0
    for y in sorted(nc):
        ee = sum(q for q, _ in (x for yy in nc if yy < y for x in nc[yy]))
        ss = sum(s_ for _, s_ in (x for yy in nc if yy < y for x in nc[yy]))
        if ee < CAL_MIN_EXPECTED:
            continue
        k = ss / ee
        seen += sum(s_ for _, s_ in nc[y])
        e_raw += sum(q for q, _ in nc[y])
        e_cal += k * sum(q for q, _ in nc[y])
    got = json.load(open(os.path.join(M.DATA, "local", "backtest-ncsbe.json")))["calibration"]["local"]
    print(f"\n  North Carolina (local_ncsbe.py), the factor pooled over earlier years, each year with 30 or more expected: seen {seen:.0f}, "
          f"expected uncalibrated {e_raw:.1f}, calibrated {e_cal:.1f} (record: seen {got.get('seen', got.get('seen_near_half'))}, "
          f"{got.get('expected_uncalibrated', got.get('expected_before'))}, {got.get('expected_calibrated', got.get('expected_after'))}, "
          f"adopted {got.get('adopted', got.get('passes'))}; the record's keys {sorted(got)[:8]})")


# ------------------------------------------------------------------------------------------ the boundary route's first check
def route_tables():
    h1("15.6 The boundary route (c), not yet checked: forecasts against outcomes; routes (b), (d) and (a) beside it [measured]")
    print("  expected counts sum each forecast's chance: in the class's own window (q); within 49-51% (0.02 f, capped at 1); within 100 and 10 "
          "votes of a tie (f m / N for a margin within m of the pair's N votes, capped); a margin of 0 or 1 (f/N for N even, 2f/N for N odd); "
          "the recount zone, within 0.5% of the pair's votes (0.005 f). Seen counts what happened. [measured]")
    rec = json.load(open(os.path.join(M.DATA, "local", "backtest.json")))

    def tally(rs, label, show_rec=None):
        t = [0, 0.0, 0, 0.0, 0, 0.0, 0, 0.0, 0, 0.0, 0, 0.0, 0]
        for r in rs:
            v0, v1 = r["pair"]["votes"]
            N = v0 + v1
            if N <= 0:
                continue
            s = v0 / N
            marg = abs(v0 - v1)
            f = r["p"]["f_half"] if r["route"] != "partisan" else M.f_half(r["share"]["mean"], r["share"]["sd"])
            t[0] += 1
            if r["route"] != "partisan":
                h = D.window_h(r["win"])
                t[1] += r["q"]
                t[2] += int(s <= 0.5 + h + 1e-12)
                t[3] += min(1.0, 0.02 * f)
                t[7] += min(1.0, 100 * f / N)
                t[9] += min(1.0, 10 * f / N)
                t[11] += min(1.0, (1 if N % 2 == 0 else 2) * f / N)
                t[5] += min(1.0, 0.005 * f)
            else:
                m, sd = r["share"]["mean"], r["share"]["sd"]
                cdf = lambda x: stats.norm.cdf(x, m, sd)  # noqa: E731
                t[3] += cdf(0.51) - cdf(0.49)
                t[7] += cdf(0.5 + 50 / N) - cdf(0.5 - 50 / N)
                t[9] += cdf(0.5 + 5 / N) - cdf(0.5 - 5 / N)
                t[11] += min(1.0, (1 if N % 2 == 0 else 2) * f / N)
                t[5] += cdf(0.5025) - cdf(0.4975)
            t[4] += int(abs(s - 0.5) <= 0.01)
            t[8] += int(marg <= 100)
            t[10] += int(marg <= 10)
            t[12] += int(marg <= 1)
            t[6] += int(marg <= 0.005 * N)
        if not t[0]:
            return
        own = f"own window {t[1]:.1f}/{t[2]}; " if t[1] else ""
        line = (f"    {label:70s} {t[0]:7,}: {own}49-51% {t[3]:.1f}/{t[4]}; recount zone {t[5]:.1f}/{t[6]}; within 100 votes {t[7]:.1f}/{t[8]}; "
                f"within 10 {t[9]:.2f}/{t[10]}; margin 0 or 1 {t[11]:.2f}/{t[12]}")
        if show_rec:
            line += (f"  | record: {show_rec.get('races')}: 49-51% {show_rec.get('expected_49_51')}/{show_rec.get('seen_49_51')}; recount {show_rec.get('expected_recount_zone')}/"
                     f"{show_rec.get('seen_recount_zone')}; within 10 {show_rec.get('expected_within_10_votes')}/{show_rec.get('seen_within_10_votes')}; "
                     f"margin 0 or 1 {show_rec.get('expected_margin_0_or_1')}/{show_rec.get('seen_margin_0_or_1')}")
        print(line)

    state = [r for level in ("state-upper", "state-lower") for r in D.rows(level) if r["status"] == "value" and r["route"] and r["pair"] and r["p"].get("f_half")]
    bnd = [r for r in state if r["route"] == "boundary"]
    print(f"\n  boundary (c), {len(bnd):,} contests with p, by class (record: data/local/backtest.json class.by_class, Klarner years):")
    for key in sorted({r["cls"] for r in bnd}):
        tally([r for r in bnd if r["cls"] == key and r["src"] == "klarner"], key, rec["class"]["by_class"].get(key))
    print("  boundary (c), by period:")
    for a, b in ((1968, 1979), (1980, 1989), (1990, 1999), (2000, 2009), (2010, 2019), (2020, 2024)):
        tally([r for r in bnd if a <= r["year"] <= b], f"{a}-{b}")
    print("  boundary (c), by the size of the deciding pair's votes:")
    for i in range(4):
        tally([r for r in bnd if D.size_bin(r["pair"]["votes"][0] + r["pair"]["votes"][1]) == i], f"bin {D.BINS[i]}-{D.BINS[i + 1]}")
    print("  boundary (c), by seats at once:")
    for k in (2, 3, 4):
        tally([r for r in bnd if (r["seats"] if k < 4 else 99) == k or (k == 4 and r["seats"] >= 4)], f"{k if k < 4 else '4+'} seats")
    print("\n  class (b) and runoff (d), state levels, by class:")
    for route in ("class", "runoff"):
        for key in sorted({r["cls"] for r in state if r["route"] == route}):
            tally([r for r in state if r["route"] == route and r["cls"] == key and r["src"] == "klarner"], key, rec["class"]["by_class"].get(key))
    print("\n  partisan (a), state levels, by period (record: backtest.json partisan.all over 1975-2022):")
    pa = [r for r in state if r["route"] == "partisan"]
    for a, b in ((1975, 1979), (1980, 1989), (1990, 1999), (2000, 2009), (2010, 2019), (2020, 2024)):
        tally([r for r in pa if a <= r["year"] <= b], f"{a}-{b}")
    tally([r for r in pa if r["src"] == "klarner"], "all Klarner years", rec["partisan"]["all"])
    print("\n  local, boundary and class, MEDSL years (after calibration where applied) and North Carolina:")
    loc = [r for r in D.rows("local") if r["status"] == "value" and r["route"] in ("class", "boundary") and r["pair"] and r["p"].get("f_half")]
    for by in ("pipeline/local_medsl.py", "pipeline/local_ncsbe.py"):
        for route in ("boundary", "class"):
            for y in sorted({r["year"] for r in loc if r["by"] == by and r["route"] == route}):
                tally([r for r in loc if r["by"] == by and r["route"] == route and r["year"] == y], f"{by.split('/')[-1]} {route} {y}")


def size_bin_point(rows, Mall):
    h1("15.7 D3's point 1: the race's own sd by the size bin of the count itself [measured]")
    have = [r_ for r_ in rows if r_["N_lag"]]
    same = sum(1 for r_ in have if D.size_bin(r_["N"]) == D.size_bin(r_["N_lag"]))
    print(f"  of {len(rows):,} route-(a) rows, {len(have):,} have the seat's last two-party count (Klarner's dvotelag + rvotelag); "
          f"the size bin of the count itself equals the last count's bin in {same:,} ({100 * same / len(have):.1f}%).")
    ratio = []
    for r_ in have:
        a, b = Mall["s_e"].get(f"{r_['cls']}{D.size_bin(r_['N'])}"), Mall["s_e"].get(f"{r_['cls']}{D.size_bin(r_['N_lag'])}")
        if a and b and a != b:
            ratio.append(b / a)
    if ratio:
        ratio = np.array(ratio)
        print(f"  where the bins differ ({len(ratio):,} rows), s_e from the last count's bin over s_e from the count's own bin (the all-years fit): "
              f"median {np.median(ratio):.3f}, 10th-90th percentile {np.percentile(ratio, 10):.3f}-{np.percentile(ratio, 90):.3f}; "
              f"the whole sd moves less, since s_a and s_g do not change.")
    print("  REPORT section 2's s_e by class and size differ by at most 0.02 between neighbouring bins, so a bin read from the last count would "
          "move sd by a few percent in the rows that change bin; the count itself is not known before the election (D3's own point).")


if __name__ == "__main__":
    print(f"c15: D3's forecasts refitted from the sources; repository HEAD {M.git_head()}")
    like_state()
    like_local()
    measures()
    rows, fits, Mall = partisan()
    calibration()
    route_tables()
    size_bin_point(rows, Mall)
