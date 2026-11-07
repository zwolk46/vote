"""C26 (third pass, item 5: D3's #75, 2023 feeds the later years; the orchestrator's relay of 12:44 UTC). Louisiana's
2023 rows now join every later year's like races and like measures, the back-tests and the robustness test (the
orchestrator's ruling of 11:56). Checked: the moves file (data/local/moves-2023-feed.json) against my own diff of every
contest between main before #75 (5a22ade) and #75 (de31d9b); the one class whose 141 p of 2024 rise by a factor 1.42,
recomputed from my pools with and without 2023, with the window rule shown step by step (the orchestrator: "a rise that
large from 219 to 237 like races needs its 'window narrows' explained"); the 62 p newly computed; the 43 statewide
measure p (x0.964) and the measures' note under the 11:01 rule at its new counts (c16's test); the two ties as marked.
Own implementation (m2d3.py, c15, c16); nothing from pipeline/ is imported. [measured] throughout; the record's own
figures [stated].
"""
import collections
import json
import math
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402
import m2d3 as D  # noqa: E402
import c15_d3_refit as C15  # noqa: E402
import c16_notes as C16  # noqa: E402

BEFORE, AFTER = "5a22ade", "de31d9b"
LEVELS = ("local", "primary", "measure", "state-lower", "state-upper")
CLS_UP = "local council, commission or board, one major party against others, 2 candidates"
CLS_NEW = "local council, commission or board, two or more of one major party, 2 candidates"


def h1(s):
    print("\n" + s)


def at(commit, path):
    r = subprocess.run(["git", "show", f"{commit}:{path}"], capture_output=True, text=True, cwd=L.ROOT)
    return json.loads(r.stdout) if r.returncode == 0 else None


def changed_files():
    out = subprocess.run(["git", "diff", "--name-only", BEFORE, AFTER, "--", "data/"], capture_output=True, text=True, cwd=L.ROOT).stdout.split()
    return [f for f in out if f.endswith(".json") and len(f.split("/")) == 4 and f.split("/")[1] in LEVELS]


def what_differs(b, a):
    """Which parts of a contest's record differ, p's value aside."""
    keys = set()
    for k in set(b) | set(a):
        if k == "p":
            pb, pa = b.get("p") or {}, a.get("p") or {}
            for kk in set(pb) | set(pa):
                if pb.get(kk) != pa.get(kk):
                    keys.add("p." + kk)
        elif k == "forecasts":
            fb, fa = json.dumps(b.get(k), sort_keys=True), json.dumps(a.get(k), sort_keys=True)
            if fb != fa:
                keys.add("forecasts" + (".calibration_not_of_record" if "calibration_not_of_record" in fa + fb else ""))
        elif b.get(k) != a.get(k):
            keys.add(k if k != "result" else "result." + ",".join(sorted(kk for kk in set(b[k]) | set(a[k]) if b[k].get(kk) != a[k].get(kk))))
    return tuple(sorted(keys))


def section_1():
    h1("26.1 The moves file against my own diff of every contest between main before #75 and #75")
    mv = L.load_json(os.path.join(L.DATA, "local", "moves-2023-feed.json"))
    print(f"  the file: before {mv['before_commit']}, after code {mv['after_code_commit']}; counts {mv['counts']}; columns {mv['columns']}")
    rows = {r[0]: r for r in mv["contests"]}
    print(f"  rows {len(rows)} ({len(mv['contests'])} listed); kinds {dict(collections.Counter(r[4] for r in mv['contests']))}")
    files = changed_files()
    print(f"  data files changed: {len(files)} " + str(dict(collections.Counter(f.split('/')[1] for f in files))))
    kinds, other, bad = collections.Counter(), collections.Counter(), []
    ratios = collections.defaultdict(list)
    cls_of = collections.defaultdict(collections.Counter)
    for f in files:
        b = {c["id"]: c for c in (at(BEFORE, f) or {"contests": []})["contests"]}
        a = {c["id"]: c for c in (at(AFTER, f) or {"contests": []})["contests"]}
        lv = f.split("/")[1]
        for i in set(b) | set(a):
            if i not in b or i not in a:
                kinds[(lv, "removed" if i not in a else "added")] += 1
                bad.append((i, "removed/added", rows.get(i)))
                continue
            pb, pa = (b[i].get("p") or {}).get("value"), (a[i].get("p") or {}).get("value")
            if pb is None and pa is None:
                k = None
            elif pb is None:
                k = "N"
            elif pa is None:
                k = "X"
            elif abs(pb - pa) > 1e-12 * max(abs(pb), abs(pa)):
                k = "P"
            else:
                k = None
            if k:
                kinds[(lv, k)] += 1
                row = rows.get(i)
                if row is None or row[4] != k or (row[2] is None) != (pb is None) or (row[3] is None) != (pa is None) \
                        or (pb is not None and row[2] is not None and abs(row[2] - pb) > 1e-9 * max(abs(pb), 1e-300)) \
                        or (pa is not None and row[3] is not None and abs(row[3] - pa) > 1e-9 * max(abs(pa), 1e-300)):
                    bad.append((i, k, row))
                if k == "P" and pb:
                    ratios[lv].append(pa / pb)
                    cls_of[(lv, "P")][(a[i].get("p") or {}).get("class") or re.sub(r".*for the class '([^']*)'.*", r"\1", (a[i].get("p") or {}).get("not_computed") or "") or ((a[i].get("forecasts") or [{}])[0].get("class") if lv == "measure" else None)] += 1
                if k == "N":
                    cls_of[(lv, "N")][(a[i].get("p") or {}).get("class")] += 1
            else:
                d = what_differs(b[i], a[i])
                if d:
                    other[(lv, d)] += 1
                    if "result.tie,tie_settled" in d or any(x.startswith("result.") and "tie" in x for x in d):
                        row = rows.get(i)
                        if row is None or row[4] != "tie":
                            bad.append((i, "tie", row))
    print("  my diff, p changed: " + "; ".join(f"{lv} {k} {v}" for (lv, k), v in sorted(kinds.items())))
    listed_not_found = [i for i, r in rows.items() if r[4] in ("P", "N") and not any(True for _ in [0])]
    print(f"  rows of the moves file not matched by my diff (id, kind, p before, p after): {len(bad)} {bad[:5]}")
    ids_mine = sum(kinds.values())
    n_pn = sum(1 for r in rows.values() if r[4] in ("P", "N"))
    print(f"  every p that changed is listed, and every P or N row is a change: {'yes' if not bad and ids_mine == n_pn else 'NO'} ({ids_mine} in my diff, {n_pn} P or N rows, {len(rows) - n_pn} tie rows)")
    for lv, rs in ratios.items():
        rs = sorted(rs)
        print(f"  {lv} P ratios after/before: n {len(rs)}, min {rs[0]:.4f}, median {rs[len(rs) // 2]:.4f}, max {rs[-1]:.4f}")
    print("  other differences, p's value unchanged (not listed as moves), by level and what differs: "
          + "; ".join(f"{lv} {'+'.join(d)} {v}" for (lv, d), v in sorted(other.items(), key=lambda kv: -kv[1])[:12]))
    return rows


def window_steps(sh, label):
    """D3-v1.1's window rule step by step (m2d3.class_density): the narrowest window of WINDOWS holding MIN_IN_WINDOW or
    more of the class's earlier shares; f = count / (N 2h); p = f / (2n) ... through sd_eq."""
    N = len(sh)
    parts = []
    for h in D.WINDOWS:
        k = sum(1 for s in sh if abs(s - 0.5) <= h + 1e-12)
        parts.append(f"h {h}: {k} in window" + (" (reaches 10)" if k >= D.MIN_IN_WINDOW else ""))
    f, N2, h, k = D.class_density(sh)
    print(f"    {label}: N {N}; " + "; ".join(parts) + f" -> chosen h {h}, k {k}, q = k/N {k / N:.5f}, f = k/(N 2h) {f:.4f}")
    return f, N, h, k


def section_2(rows):
    h1("26.2 The class whose 141 p of 2024 rise by a factor of 1.42, recomputed, and the window rule shown")
    print(f"  the window rule (m2d3.class_density, D3-v1.1): windows {D.WINDOWS} around 1/2, the narrowest holding {D.MIN_IN_WINDOW} or more like races is used; a class needs {D.MIN_CLASS} like races")
    with_, _, _ = C15.local_pools(odd_la=True)
    without, _, _ = C15.local_pools(odd_la=False)
    s_with = [s for y, k, s in with_ if k == CLS_UP and y < 2024]
    s_without = [s for y, k, s in without if k == CLS_UP and y < 2024]
    f0, N0, h0, k0 = window_steps(s_without, "without 2023 (the rule between #70 and #75)")
    f1, N1, h1_, k1 = window_steps(s_with, "with 2023 (#75)")
    new = sorted(s for y, k, s in with_ if k == CLS_UP and y == 2023)
    print(f"    2023's rows of the class: {len(new)}; their shares of the deciding pair " + ", ".join(f"{s:.3f}" for s in new)
          + f"; within 0.01 of 1/2: {sum(1 for s in new if abs(s - 0.5) <= 0.01 + 1e-12)}, within 0.02: {sum(1 for s in new if abs(s - 0.5) <= 0.02 + 1e-12)}, within 0.05: {sum(1 for s in new if abs(s - 0.5) <= 0.05 + 1e-12)}")
    print(f"    the ratio of the densities f with / without: {f1 / f0:.4f} (the record's p move x1.42); with the same window {h0} the ratio would be {(sum(1 for s in s_with if abs(s - 0.5) <= h0 + 1e-12) / (N1 * 2 * h0)) / f0:.4f}")
    mv = [r for r in rows.values() if r[4] == "P" and r[0].split("-")[1] == "local"]
    rs = sorted(r[3] / r[2] for r in mv if r[2])
    print(f"    the moves file's 141 ratios: min {rs[0]:.4f} max {rs[-1]:.4f}")
    ids = {r[0] for r in mv}
    todays = [r for r in D.rows("local") if r["id"] in ids and r["status"] == "value" and r["route"] in ("class", "boundary")]
    print(f"    their classes today: {dict(collections.Counter(r['cls'] for r in todays))}")
    C15.compare_like(todays, with_, f"the 141 moved p, like races from my pool with 2023")
    C15.compare_like(todays, without, f"the same without 2023 (expected to differ)")


def section_3(rows):
    h1("26.3 The 62 p newly computed")
    with_, _, _ = C15.local_pools(odd_la=True)
    without, _, _ = C15.local_pools(odd_la=False)
    for label, pool in (("without 2023", without), ("with 2023", with_)):
        sh = [s for y, k, s in pool if k == CLS_NEW and y < 2024]
        la = sum(1 for y, k, s in pool if k == CLS_NEW and y == 2023)
        print(f"  '{CLS_NEW}', {label}: {len(sh)} like races before 2024 ({la} of 2023)" + ("" if len(sh) >= D.MIN_CLASS else " (under 100: no p)"))
    ids = {r[0] for r in rows.values() if r[4] == "N"}
    todays = [r for r in D.rows("local") if r["id"] in ids]
    print(f"  the 62 today: status {dict(collections.Counter(r['status'] for r in todays))}; classes {dict(collections.Counter(r['cls'] for r in todays))}; by state {dict(collections.Counter(r['state'] for r in todays).most_common())}")
    C15.compare_like([r for r in todays if r["status"] == "value"], with_, "the 62 new p, like races from my pool with 2023")


def section_4(rows):
    h1("26.4 The 43 statewide measure p (x0.964) and the measures' note at its new counts")
    pw = C15.measure_pool(odd_la=True)
    po = C15.measure_pool(odd_la=False)
    for label, pool in (("without 2023", po), ("with 2023", pw)):
        sh = [s for y, k, s, rid in pool if k == "statewide measure" and y < 2024]
        print(f"  statewide measures before 2024, {label}: {len(sh)} like measures ({sum(1 for y, k, s, rid in pool if k == 'statewide measure' and y == 2023)} of 2023)")
    ids = {r[0] for r in rows.values() if r[0].split("-")[1] == "measure"}
    ms = [r for r in D.rows("measure") if r["id"] in ids]
    print(f"  the 43 today: status {dict(collections.Counter(r['status'] for r in ms))}, routes {dict(collections.Counter(r['route'] for r in ms))}, classes {dict(collections.Counter(r['cls'] for r in ms))}")
    rs = sorted(r[3] / r[2] for r in rows.values() if r[0] in ids and r[2])
    print(f"  the moves file's ratios: min {rs[0]:.4f} max {rs[-1]:.4f}")
    for label, pool in (("with 2023", pw), ("without 2023 (expected to differ)", po)):
        by_k = collections.defaultdict(list)
        for y, k, s, rid in pool:
            by_k[k].append((y, s))
        tal = collections.Counter()
        worst = 0.0
        for r in ms:
            if r["status"] != "value":
                continue
            sh = [s for y, s in by_k[r["cls"]] if y < r["year"]]
            f, N, h, k = D.density_at(sh, r["t"])
            if f is None:
                tal["too few"] += 1
                continue
            same = (N == r["N"], k == r["kin"], abs(h - D.window_h(r["win"])) < 1e-9, abs(round(k / N, 5) - r["q"]) < 1e-9)
            tal["(N, k, h, q) equal" if all(same) else "differ"] += 1
            worst = max(worst, D.rel(f, r["p"]["f_t"]))
        print(f"  {label}: {dict(tal)}; worst relative difference of the density at the threshold {worst:.1e}")
    print("  the note's two tests (c16's measures test on today's files, the ruling of 11:01):")
    out = C16.measures()
    ls, lv, stands, s, v = out
    print(f"  (s) {s[1]} against {s[0]:.1f} ({ls}); (v) at {v[0]:,} votes {v[2]} against {v[1]:.1f} ({lv}); the note stands {stands}")
    note = next((((r.get("p") or {}).get("note") or "") for r in ms if (r.get("p") or {}).get("note")), "")
    print(f"  the note as written on the 43: '{note[:150]}'")


def section_5(rows):
    h1("26.5 The two ties as marked")
    la = [r for r in D.rows("local") if r["state"] == "LA" and r["year"] == 2023]
    tied = [r for r in la if r["date"] == "2023-11-18" and len({a[1] for a in r["cands"][:2]}) == 1 and len(r["cands"]) >= 2 and r["cands"][0][1] == r["cands"][1][1]]
    d = L.load_json(os.path.join(L.DATA, "local", "2023", "LA.json"))
    marked = [c for c in d["contests"] if c["result"].get("tie")]
    print(f"  exact ties of 2023-11-18 by the votes (top two equal): {len(tied)} {[r['id'] for r in tied]}; marked result.tie: {len(marked)} {[c['id'] for c in marked]}; "
          f"the moves file's tie rows: {[r[0] for r in rows.values() if r[4] == 'tie']}")
    for c in marked:
        ts = c["result"].get("tie_settled") or {}
        rule = ts.get("rule") or {}
        again = [r for r in la if r["date"] == ts.get("date") and r["office"] == next(x["office"] for x in la if x["id"] == c["id"]) and (r["counties"] or []) == next(x["counties"] for x in la if x["id"] == c["id"])]
        names = {a[2] for a in next(x for x in la if x["id"] == c["id"])["cands"]}
        names2 = {a[2] for r in again for a in r["cands"]}
        print(f"    {c['id']}: votes {[a['votes'] for a in c['result']['candidates']]}; settled by '{ts.get('settled_by')}' on {ts.get('date')} ({rule.get('law')}, {rule.get('resolution')}); "
              f"the quote names the fourth Saturday {'fourth Saturday' in (rule.get('quote') or '')}; the Dec 16 contest in the file: {len(again)} with the same candidates {names == names2}; "
              f"the tied contest's p {c.get('p', {}).get('value')} ({(c.get('p') or {}).get('not_computed') or (c.get('p') or {}).get('reason') or ''})")
    law = L.load_json(os.path.join(L.DATA, "law", "ties.json"))["states"]["LA"]
    print(f"  data/law/ties.json LA: status {law.get('status')}; rules {[(r.get('law') or r.get('cite'), r.get('resolution')) for r in (law.get('rules') or [])][:4]}")


def section_6():
    h1("26.6 The robustness test's leave-one-year-out as the record now has it (calibration-local.json; c15 15.5 reproduces it)")
    rec = L.load_json(os.path.join(L.DATA, "local", "calibration-local.json"))["routes"]
    for g, v in rec.items():
        t = v.get("test") or {}
        print(f"  {g}: adopted {v.get('adopted')}; test years {t.get('years')}, contests {t.get('contests')}, improves {t.get('improves')}, cells made worse {t.get('tested_cells_made_worse')}, passes {t.get('passes')}")
        for y, x in (v.get("leave_one_year_out") or {}).items():
            print(f"    without {y}: years {x.get('years')}, contests {x.get('contests')}, seen {x.get('seen_near_half')}, expected {x.get('expected_before')} -> {x.get('expected_after')}, worse {x.get('tested_cells_made_worse')}, passes {x.get('passes')}"
                  + (f"; council: {x['by_office_type'].get('class, local council, commission or board')}" if (x.get('by_office_type') or {}).get('class, local council, commission or board') and y == '2024' else ""))


def main():
    print("C26. D3's #75: 2023 FEEDS THE LATER YEARS: THE MOVES, THE x1.42 CLASS AND ITS WINDOW, THE 62 NEW p, THE MEASURES AND THEIR NOTE, THE TWO TIES")
    print(f"repository HEAD {L.git_head()}")
    rows = section_1()
    section_2(rows)
    section_3(rows)
    section_4(rows)
    section_5(rows)
    section_6()


if __name__ == "__main__":
    main()
