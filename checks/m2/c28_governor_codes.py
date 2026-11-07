"""c28: D2's #78 (b782117): every governor's incumbency code checked against the record's last race, seventeen
fixed under the rulings of 13:43; and #76 (a33c065): New Jersey and Virginia 2025, Rhode Island 2010, New Jersey
2021's last race.

The orchestrator (2026-11-07 14:21 UTC): "recompute a sample of the governor moves from the new codes. Check each
fixed code against its cited source, and check the switch test's leave-one-out sets."

What this does (every figure [measured] unless marked):
  28.1 the 37 disagreements of D2's table (data/congress/governor-incumbency.json) re-derived from the files: each
       nominee (top D and R by votes), the seat's last race in the record (the state's previous governor contest in
       data/governor/, specials included, Louisiana apart) and its winner, the kind (A, B, C); the 17 fixes' inputs
       before (a33c065) and after, and that no other contest's incumbency moved.
  28.2 the ten rosters D2 cites, fetched by me (sh checks/m2/fetch_governor_rosters.sh: curl -sSL, 5 s apart, into ~/.cache/vote-m2/governor_rosters/): sha256
       against the table's, and every quote found in the page (whitespace, quotes and dashes normalised; PDFs through
       pdftotext).
  28.3 the 387 moved p: the files before and after against the table; every moved p recomputed from my own refit
       with the fixed codes (and with the sources' codes for 'before'), the ratio against the table's; the
       coefficients before and after.
  28.4 the House's switch test (level to band) under the robustness test of 08:36, on 2010-2024 and with each year
       left out, from my own scoring (m2fit, as c10 and c11 score it), against data/house/2024.json's beside block;
       the level factor of 2010 and 2012 (pooled over levels) that moved 748 House p.
  28.5 #76: the 2025 file, Rhode Island 2010, New Jersey 2021's last race (the odd years' p are c25's).
Own implementation; nothing from pipeline/ is imported (chambers._switch_test was read and its conditions re-applied
through m2fit's scoring).
"""
import collections
import copy
import hashlib
import html
import json
import os
import re
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402
import m2fit as F  # noqa: E402
import c11_k_reading as C11  # noqa: E402

BEFORE, AFTER = "a33c065", "b782117"
TABLE = os.path.join(L.DATA, "congress", "governor-incumbency.json")
ROSTERS = os.path.join(L.CACHE, "governor_rosters")
SPECIAL = "t-2"   # the House specials' lean line, as c10/c11 score the record


def rel(a, b):
    return abs(a - b) / max(abs(a), abs(b), 1e-300)


def at(commit, path):
    r = subprocess.run(["git", "show", f"{commit}:{path}"], capture_output=True, text=True, cwd=L.ROOT)
    return json.loads(r.stdout) if r.returncode == 0 and r.stdout else None


def governor_files(commit=None):
    """{year: [contests]} from data/governor/ (the working tree, or a commit)."""
    out = {}
    if commit is None:
        for p in sorted(os.listdir(os.path.join(L.DATA, "governor"))):
            if re.match(r"\d{4}\.json$", p):
                d = L.load_json(os.path.join(L.DATA, "governor", p))
                out[d["year"]] = d["contests"]
    else:
        r = subprocess.run(["git", "ls-tree", "--name-only", commit, "data/governor/"], capture_output=True, text=True, cwd=L.ROOT)
        for p in r.stdout.split():
            if re.search(r"/\d{4}\.json$", p):
                d = at(commit, p)
                if d:
                    out[d["year"]] = d["contests"]
    return out


def surname(name):
    n = (name or "").upper().replace(".", "")
    n = n.split(",")[0].strip()
    return n.split()[-1] if n else ""


def nominee(c, side):
    cands = [a for a in c["result"]["candidates"] if a.get("party") == side and (a.get("votes") or 0) > 0]
    return max(cands, key=lambda a: a["votes"]) if cands else None


def winner(c):
    cands = [a for a in c["result"]["candidates"] if (a.get("votes") or 0) > 0]
    return max(cands, key=lambda a: a["votes"]) if cands else None


# ---------------------------------------------------------------------------------------------- 28.1
def section_1(table, files):
    print("### 28.1 the 37 disagreements re-derived from the files, and the 17 fixes' inputs")
    by_state = collections.defaultdict(list)
    for y, cs in files.items():
        for c in cs:
            c.setdefault("state", c["id"].split("-")[2])
            if c["state"] != "LA":
                by_state[c["state"]].append((y, c))
    for st in by_state:
        by_state[st].sort(key=lambda yc: yc[0])
    checks = table["checks"]
    print(f"  table: {len(checks)} checks ({dict(collections.Counter(x['verdict'] for x in checks))}; kinds "
          f"{dict(collections.Counter(x['kind'] for x in checks))}); contests read {table.get('contests_read')} "
          f"(mine: {sum(len(v) for v in by_state.values())} apart from Louisiana's {sum(1 for cs in files.values() for c in cs if c.get('state', c['id'].split('-')[2]) == 'LA')})")
    tal = collections.Counter()
    for x in checks:
        cid, side = x["contest"], x["side"]
        y = int(cid[:4])
        c = next((c for yy, c in by_state[x["contest"].split("-")[2]] if c["id"] == cid), None)
        if c is None:
            tal["contest not found"] += 1
            print(f"    {cid}: not in the files")
            continue
        nom = nominee(c, side)
        same_nom = nom is not None and nom["name"] == x["nominee"]
        earlier = [(yy, cc) for yy, cc in by_state[c["state"]] if yy < y]
        if earlier:
            ly, lc = earlier[-1]
            w = winner(lc)
            last = (ly, w["name"] if w else None, bool(lc.get("special")))
        else:
            last = None   # the state's first contest in the files: Algara and Amlani's last race before 1977
        code = x["code_in_source"]
        coded_inc = (code == 1) if isinstance(code, int) else str(code).endswith("Incumbent")
        coded_any = (code in (1, 2, 3)) if isinstance(code, int) else str(code).endswith("Incumbent")
        if last is None:
            tl = x.get("last_race") or {}
            won = surname(x["nominee"]) == surname(tl.get("winner"))
            same_last = "first contest (AA's last race, not re-derived)"
            special = False
        else:
            won = surname(nom["name"] if nom else x["nominee"]) == surname(last[1])
            tl = x.get("last_race") or {}
            same_last = (tl.get("year") == last[0] and surname(tl.get("winner")) == surname(last[1]))
            special = last[2]
        kind = ("C" if coded_inc and won and special else "A" if won and not coded_inc else
                "B" if coded_any and not won else "-")
        ok = same_nom and (same_last is True or isinstance(same_last, str)) and kind == x["kind"]
        tal["agree" if ok else "differ"] += 1
        if not ok:
            print(f"    {cid} {side}: nominee {x['nominee']!r} mine {(nom or {}).get('name')!r}; last race table "
                  f"{tl.get('year')} {tl.get('winner')!r} mine {last}; kind table {x['kind']} mine {kind}")
    print(f"  nominee, last race and kind re-derived: {dict(tal)} (the state's first contest in the files takes "
          f"the table's Algara and Amlani last race: "
          f"{sum(1 for x in checks if not [1 for yy, c in by_state[x['contest'].split('-')[2]] if yy < int(x['contest'][:4])])})")
    # the 17 fixes: from, to and the files' incumbency before and after
    moved = {m["contest"]: m for m in table["p_moved"]["incumbency_moved"]}
    fixed = [x for x in checks if x["verdict"] == "fixed"]
    before = governor_files(BEFORE)
    ok = 0
    others = []
    for y, cs in files.items():
        bcs = {c["id"]: c for c in before.get(y, [])}
        for c in cs:
            fa = (c.get("forecast_inputs") or {}).get("incumbency")
            fb = ((bcs.get(c["id"]) or {}).get("forecast_inputs") or {}).get("incumbency")
            if c["id"] in moved:
                m = moved[c["id"]]
                if fb == m["before"] and fa == m["after"]:
                    ok += 1
                else:
                    print(f"    {c['id']}: file before {fb} after {fa}; table {m['before']} -> {m['after']}")
            elif fb != fa and c["id"] in bcs:
                others.append((c["id"], fb, fa))
    print(f"  fixes: {len(fixed)} in the table, {len(moved)} in incumbency_moved; the files' incumbency before "
          f"({BEFORE}) and after equal the table's in {ok}; moved elsewhere: {others or 'none'}")
    # the after value follows the rule: the fixed side's new code (1 -> +-1, else 0) with the other side's unchanged
    rule_ok = 0
    for x in fixed:
        m = moved[x["contest"]]
        sign = 1 if x["side"] == "D" else -1
        to = x["fix"]["to"]
        was_inc = (x["code_in_source"] == 1) if isinstance(x["code_in_source"], int) else str(x["code_in_source"]).endswith("Incumbent")
        now_inc = (to == 1) if isinstance(to, int) else str(to).endswith("Incumbent")
        other = m["before"] - (sign if was_inc else 0)
        if other + (sign if now_inc else 0) == m["after"]:
            rule_ok += 1
        else:
            print(f"    {x['contest']}: from {x['fix']['from']} to {to}, before {m['before']} after {m['after']}: not the rule's arithmetic")
    print(f"  the after value equals the other side's code plus the fixed side's new one in {rule_ok} of {len(fixed)}")
    by_src = collections.Counter((x["source"], x["verdict"]) for x in checks)
    print(f"  by source and verdict: {dict(by_src)}; the inferred six: "
          f"{[x['contest'] for x in checks if x['verdict'] == 'inferred']}")


# ---------------------------------------------------------------------------------------------- 28.2
def norm(s):
    s = html.unescape(s or "")
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'), ("–", "-"), ("—", "-"),
                 (" ", " "), ("‑", "-")):
        s = s.replace(a, b)
    return " ".join(s.split())


def page_text(path):
    if path.endswith(".pdf"):
        # both readings of a two-column page: -layout keeps the columns side by side (a footnote wrapped onto
        # two lines gets the other column's words between its halves), -raw keeps each column's reading order
        r = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True)
        r2 = subprocess.run(["pdftotext", "-raw", path, "-"], capture_output=True, text=True)
        return norm(r.stdout) + " \n " + norm(r2.stdout)
    raw = open(path, "rb").read()
    try:
        s = raw.decode("utf-8")
    except UnicodeDecodeError:
        s = raw.decode("cp1252", errors="replace")
    s = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", s)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    return norm(s)


def loose(s):
    return re.sub(r"[^A-Z0-9]", "", s.upper())


def section_2(table):
    print("### 28.2 the ten rosters, fetched by me, against the table (sha256 and the quotes)")
    idx = {}
    p = os.path.join(ROSTERS, "index.txt")
    if os.path.exists(p):
        for line in open(p):
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 5:
                idx[parts[0]] = (parts[1], parts[3], parts[4])
    if not idx:
        print("  no rosters fetched (see the script's header): nothing compared")
        return
    tal = collections.Counter()
    for st, r in table["rosters"].items():
        got = idx.get(st)
        if not got or got[0] != "200" or not os.path.exists(got[2]):
            print(f"  {st}: not fetched ({got})")
            tal["not fetched"] += 1
            continue
        same_url = got[1] == r["url"]
        sha = hashlib.sha256(open(got[2], "rb").read()).hexdigest()
        text = page_text(got[2])
        found = []
        for q in r.get("quotes") or []:
            nq = norm(q)
            if nq in text:
                found.append("word for word")
            elif loose(nq) in loose(text):
                found.append("letters and digits")
            else:
                lo, hi = 0, len(nq)
                while lo < hi:
                    mid = (lo + hi + 1) // 2
                    if nq[:mid] in text:
                        lo = mid
                    else:
                        hi = mid - 1
                found.append(f"NOT FOUND (longest prefix {lo} of {len(nq)}: {nq[:60]!r})")
        tal.update(f.split(" (")[0] for f in found)
        print(f"  {st}: url {'same' if same_url else 'DIFFERS'}; sha256 {'equal' if sha == r.get('sha256') else 'differs (' + sha[:12] + ' vs ' + str(r.get('sha256'))[:12] + ')'}; "
              f"{len(text):,} chars; quotes {found}")
    print(f"  quotes: {dict(tal)}; the rosters not read by D2: {list(table.get('rosters_not_read', {}).keys())} (not tried here)")


# ---------------------------------------------------------------------------------------------- 28.3
def model_own(c):
    """The model's own p value of a governor contest: p.value where it stands first, else the alongside entry."""
    p = c.get("p") or {}
    if "value" in p and str(p.get("under", "")).startswith("the model's own"):
        return p["value"], "first"
    for a in p.get("alongside") or []:
        if str(a.get("under", "")).startswith("the model's own") and "t4" not in str(a.get("under", "")):
            return a.get("value"), "beside"
    return None, None


def section_3(table, files):
    print("### 28.3 the 387 moved p: the files before and after, and every moved p recomputed from my refit")
    before = governor_files(BEFORE)
    pm = table["p_moved"]
    tab = {x["contest"]: x for x in pm["p"]}
    beside = {x["contest"]: x for x in pm.get("model_own_beside_538") or []}
    moved, unmoved, missing = {}, 0, 0
    for y, cs in files.items():
        bcs = {c["id"]: c for c in before.get(y, [])}
        for c in cs:
            if c["id"] not in bcs:
                missing += 1
                continue
            va, wa = model_own(c)
            vb, wb = model_own(bcs[c["id"]])
            if va is None or vb is None:
                continue
            if rel(va, vb) > 1e-12:
                moved[c["id"]] = (vb, va, va / vb, wa)
            else:
                unmoved += 1
    first = {k: v for k, v in moved.items() if v[3] == "first"}
    print(f"  my diff {BEFORE}..HEAD of the model's own p: {len(moved)} moved ({len(first)} standing first, "
          f"{len(moved) - len(first)} beside 538's), {unmoved} unmoved, {missing} contests new since {BEFORE} (#76's 2025)")
    print(f"  the table: p {len(tab)} (ratio n {pm['p_ratio']['n']}, {pm['p_ratio']['min']:.3f} to {pm['p_ratio']['max']:.3f}, median {pm['p_ratio']['median']:.3f}), "
          f"model_own_beside_538 {len(beside)}")
    same = sum(1 for k, v in first.items() if k in tab and rel(v[1], tab[k]["after"]) <= 1e-9 and rel(v[0], tab[k]["before"]) <= 1e-9)
    same_b = sum(1 for k, v in moved.items() if v[3] == "beside" and k in beside and rel(v[1], beside[k]["after"]) <= 1e-9)
    rs = sorted(v[2] for v in first.values())
    print(f"  table rows equal to my diff: p {same} of {len(first)} (not in the table: {sorted(set(first) - set(tab))[:5] or 'none'}; "
          f"in the table, not moved in my diff: {sorted(set(tab) - set(first))[:5] or 'none'}); beside {same_b} of {len(moved) - len(first)}")
    if rs:
        print(f"  my ratios: {rs[0]:.3f} to {rs[-1]:.3f}, median {rs[len(rs) // 2]:.3f}; under 5% {sum(1 for x in rs if abs(x - 1) < 0.05)}, under 1% {sum(1 for x in rs if abs(x - 1) < 0.01)}")
    # recompute: my refit with the fixed codes (after) and with the sources' codes (before)
    ar = F.all_rows()
    rows_after = ar["rows"]
    rows_before = copy.deepcopy(rows_after)
    reverted = 0
    for r in rows_before:
        if "inc_source_code" in r:
            r["inc"] = r["inc_source_code"]
            reverted += 1
    print(f"  fit rows: {len(rows_after)}; fixed codes changed on the rows {len(ar.get('fixed_codes_applied') or [])} (Cha's even-year rows; "
          f"Algara and Amlani's rows take the files' codes, fixed already), reverted to the sources' codes for 'before' {reverted} "
          f"(the 17 less the odd years' 2)")
    by_id = {r["id"]: r for r in rows_after if r["level"] == "governor" and r.get("id")}
    by_id_b = {r["id"]: r for r in rows_before if r["level"] == "governor" and r.get("id")}
    tails = F.VARIANTS["none"][1]
    # m2fit caches its fits by (level, year) only, so the 'before' fits run with the caches emptied and the
    # 'after' caches are put back afterwards (section 4's switch test reads the fixed rows)
    years = sorted({int(cid[:4]) for cid in moved if int(cid[:4]) % 2 == 0 and cid in by_id}
                   | {int(y) for y in (pm.get("models") or {}) if int(y) % 2 == 0})
    models = {}
    saved = (F._RAW, F._SC, F._NEAR)
    F._RAW, F._SC, F._NEAR = {}, {}, {}
    for y in years:
        models[y] = [F.variant_model(rows_before, "governor", y, "none")[0], None]
    F._RAW, F._SC, F._NEAR = saved
    for y in years:
        models[y][1] = F.variant_model(rows_after, "governor", y, "none")[0]
    tal = collections.Counter()
    worst = (0.0, None)
    worst_ratio = (0.0, None)
    for cid, (vb, va, ratio, where) in sorted(moved.items()):
        y = int(cid[:4])
        if y % 2:
            tal["odd year (c25's)"] += 1
            continue
        if cid not in by_id:
            tal["no fit row (no refit here)"] += 1
            continue
        mb, ma = models[y]
        if ma is None or mb is None:
            tal["no model for the year"] += 1
            continue
        c = next(c for c in files[y] if c["id"] == cid)
        n = (c.get("p") or {}).get("n")
        if n is None:
            n = next((a.get("n") for a in (c.get("p") or {}).get("alongside") or [] if a.get("n")), None)
        mean_a, sd_a, _ = F.predict(ma, by_id[cid])
        mean_b, sd_b, _ = F.predict(mb, by_id_b[cid])
        pa = L.p_density(n, L.f_half(mean_a, sd_a, tails))
        pb = L.p_density(n, L.f_half(mean_b, sd_b, tails))
        d_after = rel(pa, va)
        d_ratio = rel(pa / pb, ratio)
        if d_after > worst[0]:
            worst = (d_after, cid)
        if d_ratio > worst_ratio[0]:
            worst_ratio = (d_ratio, cid)
        tal["recomputed, after within 1e-4 and the ratio within 1e-3" if d_after <= 1e-4 and d_ratio <= 1e-3 else "recomputed, DIFFERS"] += 1
        if d_after > 1e-4 or d_ratio > 1e-3:
            print(f"    {cid}: file before {vb:.4g} after {va:.4g} (x{ratio:.4f}); mine before {pb:.4g} after {pa:.4g} (x{pa / pb:.4f})")
    print(f"  {dict(tal)}; worst relative difference on p after {worst[0]:.2e} ({worst[1]}), on the ratio {worst_ratio[0]:.2e} ({worst_ratio[1]})")
    # the twelve whose own input moved, as D2 lists them
    print("  the contests whose own input moved (file before -> after, 1 in n):")
    for cid in [m["contest"] for m in pm["incumbency_moved"]]:
        if cid in moved:
            vb, va, ratio, where = moved[cid]
            print(f"    {cid}: 1 in {1 / vb:,.0f} -> 1 in {1 / va:,.0f} (x{ratio:.3f}, {where})")
        else:
            print(f"    {cid}: no model's own p moved (no p, or 538's stands first and the own one is unchanged)")
    # coefficients before and after
    tm = pm.get("models") or {}
    print("  coefficients (table before/after | mine before/after), the years D2 names:")
    for y in (1986, 1990, 2006, 2024):
        if y in models and str(y) in tm:
            mb, ma = models[y]
            t = tm[str(y)]
            print(f"    {y}: b_inc {t['b_inc'][0]:.4f}/{t['b_inc'][1]:.4f} | {mb['b_inc']:.4f}/{ma['b_inc']:.4f}; b_lean {t['b_lean'][0]:.3f}/{t['b_lean'][1]:.3f} | {mb['b_lean']:.3f}/{ma['b_lean']:.3f}; "
                  f"b_lag {t['b_lag'][0]:.3f}/{t['b_lag'][1]:.3f} | {mb['b_lag']:.3f}/{ma['b_lag']:.3f}; k mine {mb['k']:.3f}/{ma['k']:.3f}")
    nd = 0
    for y_s, t in tm.items():
        y = int(y_s)
        if y in models and models[y][0] is not None:
            mb, ma = models[y]
            for k in ("b_lean", "b_inc", "b_lag"):
                if rel(t[k][0], mb[k]) > 1e-4 or rel(t[k][1], ma[k]) > 1e-4:
                    nd += 1
    print(f"  the table's coefficients differ from mine beyond 1e-4 in {nd} cells of {3 * sum(1 for y_s in tm if int(y_s) in models)}")


# ---------------------------------------------------------------------------------------------- 28.4
def cell_names(further):
    """c11's cell names ('|mean - 1/2| 0.10-0.20 49-51%' forms) into D2's: '|mean - 1/2| 0.10-0.20, 49-51%'."""
    out = []
    for x in further:
        m = re.match(r"(.+?) (\d\d-\d\d%)$", x)
        out.append(f"|mean - 1/2| {m.group(1)}, {m.group(2)}" if m else x)
    return out


def fails_of(ref, alt):
    better, nearer, further = C11.three_tests(ref, alt)
    return ([] if better else ["the log score"]) + ([] if nearer else ["the 49-51% count"]) + cell_names(further)


def section_4():
    print("### 28.4 the House's switch test (level -> band) and its leave-one-year-out sets, from my own scoring")
    rows = F.all_rows()["rows"]
    F.set_special_lines(rows, SPECIAL)
    years = list(F.VARIANT_YEARS)
    ref = F.variant_score(rows, "house", "none", years, sch="level")
    alt = F.variant_score(rows, "house", "none", years, sch="band")
    fails = fails_of(ref, alt)
    beside = L.load_json(os.path.join(L.DATA, "house", "2024.json"))["model"]["near_tie"]["beside"]
    sw = beside["switch_test"]
    print(f"  on {years[0]}-{years[-1]}: log score level {ref['mean_log_score']:.6f}, band {alt['mean_log_score']:.6f}, gain {alt['mean_log_score'] - ref['mean_log_score']:.3e} "
          f"(record {sw['mean_log_score_gain']:.3e}); 49-51% expected level {ref['within'][0.01]['expected']:.2f}, band {alt['within'][0.01]['expected']:.2f}, seen {ref['within'][0.01]['seen']} "
          f"(record {sw['count_49_51']['record_expected']:.2f}, {sw['count_49_51']['expected']:.2f}, {sw['count_49_51']['seen']})")
    print(f"  fails: mine {fails}; record {sw['fails']}; {'the same' if fails == sw['fails'] else 'DIFFER'}; passes: mine {not fails}, record {sw['passes']}")
    print("  the safe-band cells (expected level / band vs seen):")
    for b in F.VARIANT_SAFE:
        print("    " + C11.BANDL[b] + ": " + ", ".join(f"{C11.WIN[w]} {ref['by_band'][b]['within'][w]['expected']:.1f}/{alt['by_band'][b]['within'][w]['expected']:.1f} vs {ref['by_band'][b]['within'][w]['seen']}" for w in C11.WIN))
    same = 0
    for Y in years:
        ys = [t for t in years if t != Y]
        r_, a_ = F.variant_score(rows, "house", "none", ys, sch="level"), F.variant_score(rows, "house", "none", ys, sch="band")
        f_ = fails_of(r_, a_)
        rec = beside["fails_without"].get(str(Y))
        ok = f_ == rec
        same += ok
        print(f"    without {Y}: gain {a_['mean_log_score'] - r_['mean_log_score']:+.2e}; fails {f_}{'' if ok else ' | record ' + str(rec)}")
    print(f"  leave-one-year-out: {same} of {len(years)} sets fail the same way as the record's; band passes in none: "
          f"{all(beside['fails_without'].get(str(Y)) for Y in years)} (record), {all(fails_of(F.variant_score(rows, 'house', 'none', [t for t in years if t != Y], sch='level'), F.variant_score(rows, 'house', 'none', [t for t in years if t != Y], sch='band')) for Y in years)} (mine)")
    # the level factor of 2010 and 2012, pooled over levels (governors included), that moved 748 House p
    for y in (2010, 2012, 2014):
        fy = F.near_tie_factor(rows, "house", y, 0.5, "level", "none")
        rec = L.load_json(os.path.join(L.DATA, "house", f"{y}.json"))["model"]["near_tie"]
        print(f"  {y} House level factor: mine {fy['factor']:.5f} ({fy.get('of')}), record {rec.get('factor'):.5f} ({rec.get('of')}); "
              f"{'equal' if rel(fy['factor'], rec['factor']) <= 1e-4 else 'DIFFERS'}")
    bf = governor_files  # noqa: F841 (kept for symmetry)
    # the 748 House p moved: my diff
    n_m, ratios = 0, []
    for y in (2010, 2012):
        b = at(BEFORE, f"data/house/{y}.json")
        a = L.load_json(os.path.join(L.DATA, "house", f"{y}.json"))
        bb = {c["id"]: (c.get("p") or {}).get("value") for c in b["contests"]}
        for c in a["contests"]:
            va = (c.get("p") or {}).get("value")
            vb = bb.get(c["id"])
            if va and vb and rel(va, vb) > 1e-12:
                n_m += 1
                ratios.append(va / vb)
    print(f"  House p moved {BEFORE}..HEAD in 2010 and 2012: {n_m} (D2: 748), ratios {min(ratios):.4f} to {max(ratios):.4f}" if ratios else "  no House p moved")


# ---------------------------------------------------------------------------------------------- 28.5
def section_5(files):
    print("### 28.5 #76: the 2025 file, Rhode Island 2010, New Jersey 2021's last race (the odd years' p are c25's)")
    f25 = files.get(2025) or []
    for c in f25:
        p = c.get("p") or {}
        fi = c.get("forecast_inputs") or {}
        src = (c.get("result") or {}).get("source")
        print(f"  {c['id']}: p {p.get('value')} (1 in {1 / p['value']:,.0f})" if p.get("value") else f"  {c['id']}: no p ({p.get('not_computed')})",
              f"| incumbency {fi.get('incumbency')} ({fi.get('incumbency_source')}), president {fi.get('president_party')}, last race {(fi.get('last_governor_race') or {}).get('year')}; source {src}")
    ri = next((c for c in files.get(2010, []) if c.get("state", c["id"].split("-")[2]) == "RI"), None)
    if ri:
        p = ri.get("p") or {}
        print(f"  RI 2010: in the file; p {'value ' + str(p.get('value')) if 'value' in p else 'not computed: ' + str(p.get('not_computed'))[:160]}; "
              f"candidates {[(a['name'], a.get('party'), a['votes']) for a in ri['result']['candidates'][:4]]}")
    else:
        print("  RI 2010: not in data/governor/2010.json")
    nj = next((c for c in files.get(2021, []) if c.get("state", c["id"].split("-")[2]) == "NJ"), None)
    if nj:
        lg = (nj.get("forecast_inputs") or {}).get("last_governor_race") or {}
        print(f"  NJ 2021: last race {lg.get('year')} share_D {lg.get('share_D')}; incumbency {(nj.get('forecast_inputs') or {}).get('incumbency')}; p {(nj.get('p') or {}).get('value')}")


def main():
    print(f"c28: #78 (governor incumbency codes) and #76; HEAD {L.git_head()}; before {BEFORE}, after {AFTER}")
    table = L.load_json(TABLE)
    files = governor_files()
    section_1(table, files)
    section_2(table)
    section_3(table, files)
    section_4()
    section_5(files)


if __name__ == "__main__":
    main()
