"""C19. #60, North Carolina's November deciding rounds (the orchestrator's ruling of 2026-11-07 09:53; the third pass's
item 2). The ruling: a November contest that follows an earlier round of the same contest that year is that contest's
deciding round, in odd and even years alike; it is computed by the route's classes and marked; the earlier round is not
computed. Checked here:
  19.1 every contest marked a deciding round, by route (MEDSL's route for the November dates of MEDSL's years, the State
       Board's for the other dates: c15 medsl_route), its words, its status and its reason;
  19.2 the classes: the recorded route and class of every computed deciding round against my own reading of the ballot
       by the route's own classes (c15 structure_local), and the earlier round found in the files, not computed;
  19.3 data/local/moves-ncsbe-deciding-round.json: every row's 'before' against the files at 8816d1d (the commit before
       #60), 'after' against today's, the why code against what the two files show; and no other North Carolina p moved;
  19.4 the pool: the deciding rounds' like-race forecasts (N, k, h, q) from my own pool with the deciding rounds in it;
  19.5 backtest-ncsbe.json's calibration test reproduced (the factors by year, the counts, the deviance, the cells, the
       leave-one-year-out verdicts).
[measured] throughout; the record's figures [stated].
"""
import collections
import json
import os
import re
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402
import m2d3 as D  # noqa: E402
import c15_d3_refit as C15  # noqa: E402

BEFORE = "8816d1d"
DECIDING = "deciding round after an earlier round on "


def route_of(r):
    return "MEDSL's route" if C15.medsl_route(r) else "the State Board's route"


def same(a, b):
    """Two p values equal (None with None; 0 with 0; else within 1e-9 relative)."""
    if a in (None, "absent") or b in (None, "absent"):
        return a == b
    if a == 0 or b == 0:
        return a == b
    return abs(a / b - 1) < 1e-9


def p_by_id_at(commit, path):
    try:
        txt = subprocess.run(["git", "show", f"{commit}:{path}"], cwd=L.ROOT, capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError:
        return None
    out = {}
    for c in json.loads(txt)["contests"]:
        out[c["id"]] = ((c.get("p") or {}).get("value"), (c.get("election") or "")[:30])
    return out


def rec_route(r):
    """The record's route for a contest: its forecast's route, or 'zero' (unopposed, p 0), or 'partisan'."""
    if r["route"]:
        return r["route"]
    if (r["reason"] or "").startswith("one name on the ballot"):
        return "zero"
    if r["cls"]:
        return "class" if "candidates" in r["cls"] else "boundary"
    return "partisan"


def overlap(a, b):
    return a is None or b is None or bool(set(a) & set(b))


def section_1_2(rows):
    print("19.1 The contests marked deciding rounds, by route, status and words")
    dec = [r for r in rows if (r["election"] or "").startswith(DECIDING)]
    t = collections.Counter((route_of(r), "odd" if r["year"] % 2 else "even", r["status"], rec_route(r)) for r in dec)
    for k, v in sorted(t.items()):
        print(f"    {k[0]:24s} {k[1]:5s} {k[2]:13s} route {k[3]:9s} {v}")
    print("  years with a computed deciding round (p 0 of an unopposed one counted apart): "
          + ", ".join(f"{y} {c}" for y, c in sorted(collections.Counter(r["year"] for r in dec if r["status"] == "value" and rec_route(r) != "zero").items()))
          + "; unopposed, p 0: " + ", ".join(f"{y} {c}" for y, c in sorted(collections.Counter(r["year"] for r in dec if r["status"] == "value" and rec_route(r) == "zero").items())))
    reasons = collections.Counter((route_of(r), re.sub(r"\(\d+\)", "(n)", (r["reason"] or ""))[:75]) for r in dec if r["status"] != "value")
    print("  not computed, by route and reason: " + "; ".join(f"{k[0]}: '{k[1]}' {v}" for k, v in sorted(reasons.items())))
    words = collections.Counter((route_of(r), re.sub(r"\d{4}-\d{2}-\d{2}", "<date>", r["election"])) for r in dec)
    print("  the words, by route: " + "; ".join(f"{k[0]}: \"{k[1]}\" {v}" for k, v in sorted(words.items())))
    print("19.2 The classes of the computed deciding rounds against my own reading, and their earlier rounds")
    by_od = collections.defaultdict(list)
    for r in rows:
        by_od[(r["year"], r["office"], r["date"])].append(r)
    agree, differ = 0, []
    for r in dec:
        if r["status"] == "value" or r["cls"]:
            st = C15.structure_local(r, nc=not C15.medsl_route(r))
            rr = rec_route(r)
            if st[0] == rr and (rr in ("partisan", "zero") or st[1] == r["cls"]):
                agree += 1
            else:
                differ.append((r["id"], rr, r["cls"], st))
    print(f"  computed or classed deciding rounds {agree + len(differ)}: my reading of the ballot by the route's classes gives the recorded route and class in {agree}; differ {len(differ)}"
          + ("; ".join(f" {i}: record {a} '{c}', mine {s}" for i, a, c, s in differ[:6]) if differ else ""))
    # the earlier round: pipeline/local_ncsbe.py keys the rounds on (year, contest name, party) with no county, so a
    # November contest is marked a deciding round when ANY county had a contest of the name earlier that year
    found = collections.Counter()
    examples = collections.defaultdict(list)
    for r in dec:
        d0 = re.search(r"\d{4}-\d{2}-\d{2}", r["election"]).group(0)
        same = [x for x in by_od[(r["year"], r["office"], d0)]]
        own = [x for x in same if overlap(x["counties"], r["counties"])]
        kind = "same counties" if own else "the name only, in other counties" if same else "no contest of the name on that date"
        found[(kind, r["year"] >= 2014, r["status"], rec_route(r) if r["status"] == "value" else "-")] += 1
        if len(examples[kind]) < 3:
            examples[kind].append(r["id"] + (f" <- {same[0]['id']}" if same and not own else ""))
    print("  the earlier round, by what the files hold on the named date (kind, 2014 on, status, route): "
          + "; ".join(f"{k[0]}, {'2014 on' if k[1] else 'before 2014'}, {k[2]}, {k[3]}: {v}" for k, v in sorted(found.items(), key=lambda kv: (kv[0][0], kv[0][1], kv[0][2]))))
    for kind, ex in examples.items():
        if kind != "same counties":
            print(f"    e.g. {kind}: " + "; ".join(ex))
    es = collections.Counter((x["status"], (x["election"] or "")[:52]) for r in dec for x in by_od[(r["year"], r["office"], re.search(r"\d{4}-\d{2}-\d{2}", r["election"]).group(0))] if overlap(x["counties"], r["counties"]))
    print("  the earlier rounds found in the same counties, their status and words: " + "; ".join(f"{k[0]} \"{k[1]}\" {v}" for k, v in sorted(es.items())))
    # the converse: contests marked first rounds whose later round is in other counties only
    FIRST = "first round: the same contest is on the ballot again on "
    fr = [r for r in rows if (r["election"] or "").startswith(FIRST)]
    ff = collections.Counter()
    fex = []
    for r in fr:
        later = re.findall(r"\d{4}-\d{2}-\d{2}", r["election"])
        same = [x for d1 in later for x in by_od[(r["year"], r["office"], d1)]]
        own = [x for x in same if overlap(x["counties"], r["counties"])]
        kind = "same counties" if own else "the name only, in other counties" if same else "no contest of the name on that date"
        ff[(kind, r["year"] >= 2014, r["status"])] += 1
        if kind != "same counties" and r["year"] >= 2014:
            fex.append(f"{r['id'][14:]} ({len(r['cands'])} names, {r['seats'] or '?'} seat(s), {r['total_votes']:,} votes, {'2 names: ' + str(r['cands'][0][1]) + ' to ' + str(r['cands'][1][1]) if len(r['cands']) == 2 else 'top two ' + str(sorted([a[1] for a in r['cands'] if a[1] is not None], reverse=True)[:2])})")
    print(f"  the converse, the {len(fr):,} contests marked first rounds (not computed), by where the later round of the name is: "
          + "; ".join(f"{k[0]}, {'2014 on' if k[1] else 'before 2014'}, {k[2]}: {v}" for k, v in sorted(ff.items())))
    if fex:
        print(f"    the {len(fex)} from 2014 on whose later 'round' is another county's contest of the name (so not computed, though nothing followed them in their own county):")
        for x in fex:
            print(f"      {x}")
    return dec


def section_3(rows, dec):
    print("19.3 The moves file against the files before #60 (8816d1d) and today")
    mv = json.load(open(os.path.join(L.DATA, "local", "moves-ncsbe-deciding-round.json")))
    print(f"  the file: before_commit {mv['before_commit']}, after_code_commit {mv['after_code_commit']}, counts {mv['counts']}")
    before = {}
    years = sorted({r["year"] for r in rows})
    for y in years:
        b = p_by_id_at(BEFORE, f"data/local/{y}/NC.json")
        if b:
            before.update(b)
    today = {r["id"]: (r["p"].get("value"), (r["election"] or "")[:30]) for r in rows}
    dec_ids = {r["id"] for r in dec}
    t = collections.Counter()
    bad = []
    ratios = []
    in_moves = set()
    for rid, b, a, why in mv["p"]:
        in_moves.add(rid)
        rb, ra = before.get(rid, ("absent", ""))[0], today.get(rid, ("absent", ""))[0]
        ok_b = same(rb, b)
        ok_a = same(ra, a)
        if why == "D":
            ok_w = b is None and a is not None and rid in dec_ids
        elif why == "N":
            ok_w = b is None and a is not None and rid not in dec_ids
        else:
            ok_w = b is not None and a is not None and b != a and rid not in dec_ids
            if b and a:
                ratios.append(a / b)
        t[(why, ok_b, ok_a, ok_w)] += 1
        if not (ok_b and ok_a and ok_w):
            bad.append((rid, why, b, rb, a, ra))
    print(f"  {len(mv['p']):,} rows: " + "; ".join(f"{k[0]} before {'ok' if k[1] else 'WRONG'} after {'ok' if k[2] else 'WRONG'} why {'ok' if k[3] else 'WRONG'}: {v:,}" for k, v in sorted(t.items())))
    for x in bad[:8]:
        print(f"    {x}")
    if ratios:
        ratios = np.array(ratios)
        print(f"  the P rows' after/before: median {np.median(ratios):.3f}, from {ratios.min():.3f} to {ratios.max():.3f} (the record: median x0.990, x0.762 to x1.524); {int((ratios < 1).sum())} fell, {int((ratios > 1).sum())} rose")
    # every other North Carolina local p: unchanged?
    other = collections.Counter()
    moved_out = []
    for rid in set(before) | set(today):
        if rid in in_moves:
            continue
        b, a = before.get(rid, ("absent", ""))[0], today.get(rid, ("absent", ""))[0]
        if b == "absent" or a == "absent":
            other["in one version only"] += 1
            moved_out.append((rid, b, a))
        elif b is None and a is None:
            other["no p in either"] += 1
        elif same(a, b):
            other["p unchanged"] += 1
        else:
            other["p CHANGED outside the moves file"] += 1
            moved_out.append((rid, b, a))
    print(f"  North Carolina local contests outside the moves file: " + "; ".join(f"{k} {v:,}" for k, v in sorted(other.items())) + (f"; e.g. {moved_out[:4]}" if moved_out else ""))
    # the primaries' files changed in #60 too
    pt = collections.Counter()
    for y in sorted({r["year"] for r in D.rows("primary") if r["state"] == "NC"}):
        b = p_by_id_at(BEFORE, f"data/primary/{y}/NC.json")
        if not b:
            pt[f"{y}: no file before"] += 1
            continue
        for r in D.rows("primary"):
            if r["state"] != "NC" or r["year"] != y:
                continue
            vb, va = b.get(r["id"], ("absent", ""))[0], r["p"].get("value")
            pt["unchanged" if same(va, vb) else "changed"] += 1
    print(f"  North Carolina primaries' p, today against {BEFORE}: {dict(pt)}")


def section_4(dec):
    print("19.4 The deciding rounds' like-race forecasts from my own pool (the deciding rounds among the like races)")
    medsl, nc, miss = C15.local_pools()
    cm = [r for r in dec if r["route"] in ("class", "boundary") and r["N"] is not None and C15.medsl_route(r)]
    cn = [r for r in dec if r["route"] in ("class", "boundary") and r["N"] is not None and not C15.medsl_route(r)]
    C15.compare_like(cm, medsl, "deciding rounds on MEDSL's route, like races from earlier MEDSL years")
    C15.compare_like(cn, [row for row in nc if row[0] >= C15.NC_FIRST], "deciding rounds on the State Board's route, like races from the State Board's 2014 on")
    print(f"  (c15 section 15.2 compares every contest of both routes the same way, with the deciding rounds now in its pools)")


def nc_pool_rows(rows):
    """c15's North Carolina pool (its local_pools NC branch) with the fields the calibration test needs: every State
    Board contest from 2014 the like-race route can take, on every date (the November dates of MEDSL's years too, as
    the record's like_rows takes them), keyed by my own reading where the files give MEDSL's class."""
    out = []
    for r in rows:
        if r["year"] < C15.NC_FIRST or r["src"] != "ncsbe":
            continue
        if r["status"] == "value" and r["route"] is None:
            continue
        reason = r["reason"] or ""
        if r["status"] == "not_computed" and not any(reason.startswith(x) for x in C15.POOL_REASONS):
            continue
        k = r["seats"] or 1
        if r["pair"]:
            v0, v1 = r["pair"]["votes"]
        else:
            b = C15.ballot_local(r)
            if len(b) <= k:
                continue
            v0, v1 = b[k - 1][1], b[k][1]
        if v0 + v1 <= 0:
            continue
        top = sorted([a for a in r["cands"] if a[1] is not None], key=lambda a: -a[1])
        if any(C15._generic(a[2]) for a in top[k - 1:k + 1]):
            continue
        if not C15.medsl_route(r) and r["cls"]:
            key = r["cls"]
        else:
            st = C15.structure_local(r, nc=True)
            if st[0] not in ("class", "boundary", "partisan"):
                continue
            key = st[1]
        route = "boundary" if "seats at once" in key else "class"
        out.append({"year": r["year"], "key": key, "s": max(v0, v1) / (v0 + v1), "n": v0 + v1, "route": route,
                    "cell": f"{route}, {r['office_scope']} {r['office_type']}", "partisan": "Democrat against a Republican" in key, "id": r["id"]})
    return out


def nc_backtest(pool, partisan):
    """The record's backtest form (pipeline/local_ncsbe.py backtest): each year forecast from the pool's earlier years;
    expected = kin / N (the class's share within h of a half), seen = s <= 1/2 + h."""
    recs = collections.defaultdict(list)
    years = sorted({r["year"] for r in pool})
    for t in years:
        train = [r for r in pool if r["year"] < t]
        dens = {}
        for r in pool:
            if r["year"] != t or (r["partisan"] and not partisan):
                continue
            if r["key"] not in dens:
                dens[r["key"]] = D.class_density([x["s"] for x in train if x["key"] == r["key"]])
            f, N, h, kin = dens[r["key"]]
            if f is None:
                continue
            recs[("local", t)].append((r, r["cell"], kin / N, r["s"] <= 0.5 + h))
    return recs


def section_5(rows):
    print("19.5 backtest-ncsbe.json's calibration test of the State Board's route reproduced")
    rec = json.load(open(os.path.join(L.DATA, "local", "backtest-ncsbe.json")))["calibration"]
    pool = nc_pool_rows(rows)
    print(f"  my State Board pool from {C15.NC_FIRST}: {len(pool):,} contests; by year " + ", ".join(f"{y} {c}" for y, c in sorted(collections.Counter(r['year'] for r in pool).items()))
          + f"; of them in the class 'a Democrat against a Republican' {sum(r['partisan'] for r in pool):,}")
    prim = collections.defaultdict(list)
    for r in D.rows("primary"):
        if r["state"] != "NC" or r["q"] is None or not r["pair"] or r["route"] not in ("class", "boundary"):
            continue
        s = r["pair"]["share_first"]
        prim[("primary", r["year"])].append((r, f"primary, {r['route']}, {r['office_scope']} {r['office_type']}", r["q"], r["win"][0] <= round(s, 6) <= r["win"][1]))
    for group, recs, label in (("local", nc_backtest(pool, partisan=False), "local, my own pool and forecasts, the Democrat-against-Republican class left out"),
                               ("local", nc_backtest(pool, partisan=True), "local, the same with that class in"),
                               ("primary", prim, "primary, the files' own forecasts (q, the window)")):
        g = rec[group]
        years = sorted(y for gg, y in recs if gg == group)
        scored = [y for y in years if str(y) in g["factors"]]
        print(f"  {label}: forecasts by year " + ", ".join(f"{y} {len(recs[(group, y)]):,}" for y in years) + f"; the record scores {g['scored_years']}")
        factors = {}
        line = []
        for t in scored:
            fy = [y for y in years if y < t]
            f = C15.factor_fit(recs, group, fy)
            factors[t] = {"pooled": f["pooled"], "own": {}}
            line.append(f"{t} {f['pooled']:.3f}/{g['factors'][str(t)]}")
        T = C15.cal_score(recs, group, scored, factors)
        tr = g["test"]
        print(f"    pooled factors, mine/record: " + ", ".join(line))
        print(f"      {T['contests']:,} contests ({tr['contests']}), seen {T['seen']} ({tr['seen_near_half']}), expected {T['before']:.1f} -> {T['after']:.1f} ({tr['expected_before']} -> {tr['expected_after']}), "
              f"deviance {T['dev_before']:.2f} -> {T['dev_after']:.2f} ({tr['deviance_by_office_type_before']} -> {tr['deviance_after']}); improves {T['improves']} ({tr['improves']}); "
              f"cells worse {T['worse']} ({tr['tested_cells_made_worse']}); passes {T['passes']} ({tr['passes']})")
        cells = collections.defaultdict(lambda: [0.0, 0.0, 0])
        for t in scored:
            for _, key, e, seen in recs.get((group, t), []):
                cells[key][0] += e
                cells[key][1] += e * factors[t]["pooled"]
                cells[key][2] += seen
        print("      by cell, mine (record): " + "; ".join(f"{k}: {v[0]:.1f} -> {v[1]:.1f} vs {v[2]} ({(tr['by_office_type'].get(k) or {}).get('expected_before')} -> {(tr['by_office_type'].get(k) or {}).get('expected_after')} vs {(tr['by_office_type'].get(k) or {}).get('seen')})" for k, v in sorted(cells.items(), key=lambda kv: -kv[1][0])))
        loo = []
        for y in scored:
            ys = [t for t in scored if t != y]
            T2 = C15.cal_score(recs, group, ys, factors)
            r2 = g["leave_one_year_out"].get(str(y), {})
            loo.append(f"{y}: {T2['before']:.1f}->{T2['after']:.1f} vs {T2['seen']} ({r2.get('expected_before')}->{r2.get('expected_after')} vs {r2.get('seen_near_half')}), passes {T2['passes']} ({r2.get('passes')})")
        print("      leave one scored year out (factors as fitted): " + "; ".join(loo))


def main():
    print("C19. #60: NORTH CAROLINA'S NOVEMBER DECIDING ROUNDS, BOTH ROUTES, THE MOVED p, THE POOL AND THE CALIBRATION TEST")
    print(f"repository HEAD {L.git_head()}")
    rows = [r for r in D.rows("local") if r["state"] == "NC"]
    dec = section_1_2(rows)
    section_3(rows, dec)
    section_4(dec)
    section_5(rows)


if __name__ == "__main__":
    main()
