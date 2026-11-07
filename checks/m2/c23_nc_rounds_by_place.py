"""C23. #72: North Carolina's rounds keyed by place as well as name (D3's fix after c19's finding; the orchestrator's note
of 2026-11-07 12:04 UTC: "check that #72 closes your c19 and that the 234 marks beyond your count are right").
  23.1 my own reading of every State Board contest's rounds with the overlap rule, from the files' own fields: for every
       contest of data/local, data/primary and data/measure sourced from the State Board (all years), the other dates of
       the year on which a contest of the same name (and party, for a primary) sits in overlapping counties; from them
       the election words pipeline/local_ncsbe.py's rules give (classify, election_words: read, not imported), against
       the words the files carry today, contest by contest;
  23.2 the moves file (data/local/moves-ncsbe-rounds-by-place.json) against the files before #72 (main at a2433b1~1)
       and after: each row's words and p before and after; every contest whose words or p changed is in the file and
       the file holds nothing else; the counts by kind (R, C, N, P);
  23.3 the moved and new p recomputed from my own pools: local by c15's pools (MEDSL's route or the State Board's),
       primaries by a pool built here from the files' primaries of 2014 on (the class as the record names it, the
       counting mine), (N, k, h, q) and p against the record;
  23.4 c19's finding: the 19 school boards of 2016-03-15, the 96 November contests of 2010 and the 6 of 2016, and the
       234 marks beyond c19's count (primaries and questions), as they stand now.
[measured] throughout; the record's counts [stated].
"""
import collections
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402
import m2d3 as D  # noqa: E402
import c15_d3_refit as C15  # noqa: E402

BEFORE = "a2433b1~1"   # main before #72 (the moves file's before_commit, 20eedb9, is D3's branch commit of the same files)
AFTER = "a2433b1"
LEVELS = ("local", "primary", "measure")
PRIMARY_WORD = {"REP": "Republican primary", "DEM": "Democratic primary"}
MOVES = os.path.join(L.DATA, "local", "moves-ncsbe-rounds-by-place.json")


def nc_rows():
    out = []
    for lv in LEVELS:
        out += [r for r in D.rows(lv) if r["state"] == "NC" and r["src"] == "ncsbe"]
    return out


def party_of(r):
    """A primary's party from its words: 'Republican primary', 'Democratic primary', '<code> primary (the party's code in
    the source)'; None for a general, an election or a question."""
    if r["level"] != "primary":
        return None
    el = r["election"] or ""
    for code, w in PRIMARY_WORD.items():
        if el.startswith(w):
            return code
    m = re.match(r"^([A-Z]+) primary", el)
    return m.group(1) if m else "?"


_PRIMARY_ID = re.compile(r"^\d{4}-primary-NC-ncsbe-\d{4}-\d{2}-\d{2}-(.+?)-[a-z]{3}(?:-[A-Z0-9_]+)?$")


def name_of(r):
    """The contest's name: a question's title; a primary's from its id (the files give a legislative primary's office as
    'state-lower' or 'state-upper', not its district); a local contest's office."""
    if r["level"] == "measure":
        return r["question"]["title"]
    if r["level"] == "primary":
        m = _PRIMARY_ID.match(r["id"])
        return m.group(1) if m else r["office"]
    return r["office"]


def my_words(r, earlier, later):
    """pipeline/local_ncsbe.py classify + election_words, from (earlier, later): the other dates of the year on which a
    contest of the name sits in overlapping counties (read, not imported)."""
    d = r["date"]
    y = r["year"]
    gen = d[5:7] == "11"
    party = party_of(r)
    on_e = ", ".join(sorted(set(earlier)))
    on_l = ", ".join(sorted(set(later)))
    if r["level"] == "measure":
        other = (on_e if gen else (on_l or on_e))
        w = ("general" if y % 2 == 0 else "general (odd year: municipal)") if gen else f"election on {d}, not a November general (the source does not say its kind)"
        return w + (f"; a question of the same title was on the ballot on {other} too" if other else "")
    if party:
        w = PRIMARY_WORD.get(party, f"{party} primary (the party's code in the source)")
        if earlier:
            return f"{w}, second primary (the same contest was on the ballot on {on_e}) [inferred]"
        return w + (f" (a second primary followed on {on_l}) [inferred]" if later else "")
    if gen:
        if earlier:
            return f"deciding round after an earlier round on {on_e} (a nonpartisan primary or a first round that went to a runoff; the source does not say which) [inferred]"
        return "general" if y % 2 == 0 else "general (odd year: municipal)"
    if later:
        return f"first round: the same contest is on the ballot again on {on_l} (a nonpartisan primary or a first round that went to a runoff; the source does not say which) [inferred]"
    if earlier:
        return f"second round, after {on_e} (the source does not say whether a runoff or an election) [inferred]"
    return f"election on {d}, not a November general (the source does not say its kind)"


def section_1(rows):
    print("23.1 Every State Board contest's round words regenerated by the overlap rule from the files' own fields")
    seen = collections.defaultdict(list)
    for r in rows:
        seen[(r["year"], name_of(r), party_of(r))].append((r["date"], frozenset(r["counties"] or [])))
    t = collections.Counter()
    bad = []
    kinds = collections.Counter()
    for r in rows:
        here = set(r["counties"] or [])
        # a contest with no counties in the file is statewide (the State Board's file lists every county for it), so it overlaps every contest of the name
        ds = [x for x, where in seen[(r["year"], name_of(r), party_of(r))] if (where & here) or not where or not here]
        earlier, later = [x for x in ds if x < r["date"]], [x for x in ds if x > r["date"]]
        mine = my_words(r, earlier, later)
        if r["level"] == "measure" and not r["election"]:
            t[(r["level"], "no words in the file (a November question of a MEDSL year, built by local_medsl.py)")] += 1
            continue
        same = mine == (r["election"] or "")
        t[(r["level"], same)] += 1
        kinds[(r["level"], re.sub(r"\d{4}-\d{2}-\d{2}(, \d{4}-\d{2}-\d{2})*", "<date>", mine)[:60])] += 1
        if not same and len(bad) < 10:
            bad.append((r["id"], r["election"], mine))
    print("  by level, my words equal to the file's: " + "; ".join(f"{lv} {t[(lv, True)]:,} of {t[(lv, True)] + t[(lv, False)]:,}" for lv in LEVELS)
          + f"; questions with no words in the file (local_medsl.py's November builds, not compared) {t[('measure', 'no words in the file (a November question of a MEDSL year, built by local_medsl.py)')]:,}"
          + f"; contests with no counties in the file (statewide: taken to overlap every contest of the name) {sum(1 for r in rows if not r['counties']):,}")
    print("  the kinds, by my reading: " + "; ".join(f"{lv}: \"{w}\" {n:,}" for (lv, w), n in sorted(kinds.items(), key=lambda kv: (kv[0][0], -kv[1]))))
    for rid, el, mine in bad:
        print(f"    {rid}: file \"{el[:80]}\" mine \"{mine[:80]}\"")
    if bad:
        by_name = collections.defaultdict(list)
        for r in rows:
            by_name[(r["year"], name_of(r), party_of(r))].append(r)
        for rid, el, mine in bad[:3]:
            r = next(x for x in rows if x["id"] == rid)
            print(f"      the files' contests of that name, party and year: " + "; ".join(f"{x['id'][14:]} ({x['date']}, {len(x['counties'] or [])} counties, p {x['p'].get('value')})" for x in by_name[(r["year"], name_of(r), party_of(r))]))
    return t


def at_commit(commit, path):
    """{id: (election, p value or None, reason)} of a file at a commit; None if the file is not there."""
    r = subprocess.run(["git", "show", f"{commit}:{path}"], capture_output=True, text=True, cwd=L.ROOT)
    if r.returncode:
        return None
    out = {}
    for c in json.loads(r.stdout)["contests"]:
        p = c.get("p") or {}
        out[c["id"]] = (c.get("election") or "", p.get("value"), p.get("not_computed"))
    return out


def nc_paths():
    out = []
    for lv in LEVELS:
        for path in D.level_files(lv):
            if path.endswith("NC.json"):
                out.append(os.path.relpath(path, L.ROOT))
    return out


def section_2():
    print(f"23.2 The moves file against the files before ({BEFORE}) and after ({AFTER}) #72")
    mv = L.load_json(MOVES)
    rows = {row[0]: row for row in mv["contests"]}
    print(f"  the file: {len(rows):,} rows ({mv['counts']}); before_commit {mv['before_commit']}, after_code_commit {mv['after_code_commit']}")
    before, after = {}, {}
    for path in nc_paths():
        b = at_commit(BEFORE, path)
        a = at_commit(AFTER, path)
        if b:
            before.update(b)
        if a:
            after.update(a)
    print(f"  contests in the State Board's files: before {len(before):,}, after {len(after):,}; ids in one only: {len(set(before) ^ set(after))}")
    changed = {}
    reasons_only = 0
    for i in set(before) & set(after):
        eb, pb, rb = before[i]
        ea, pa, ra = after[i]
        pchg = (pb is None) != (pa is None) or (pb is not None and pa is not None and abs(pb - pa) > 1e-12 * max(abs(pb), abs(pa), 1e-300))
        if eb != ea or pchg:
            changed[i] = (eb, ea, pb, pa)
        elif rb != ra:
            reasons_only += 1
    print(f"  contests whose words or p changed between the two commits: {len(changed):,}; in the moves file {sum(1 for i in changed if i in rows):,}; "
          f"moves rows not among them {sum(1 for i in rows if i not in changed)}; words and p the same but the reason's words changed {reasons_only:,} (the record: 809)")
    ok = collections.Counter()
    bad = []
    for i, row in rows.items():
        _, eb, ea, pb, pa, why = row
        if i not in before or i not in after:
            bad.append((i, "not in both commits"))
            continue
        b, a = before[i], after[i]
        same = (eb == b[0], ea == a[0], (pb is None and b[1] is None) or (pb is not None and b[1] is not None and abs(pb - b[1]) <= 1e-9 * max(abs(pb), 1e-300)),
                (pa is None and a[1] is None) or (pa is not None and a[1] is not None and abs(pa - a[1]) <= 1e-9 * max(abs(pa), 1e-300)))
        kind_ok = {"R": eb != ea and ((pb is None and pa is None) or (pb is not None and pa is not None and pb == pa)),
                   "C": pb is None and pa == 0.0, "N": pb is None and pa is not None and pa > 0,
                   "P": pb is not None and pa is not None and pb != pa}.get(why, False)
        ok[(all(same), kind_ok, why)] += 1
        if not all(same) or not kind_ok:
            if len(bad) < 8:
                bad.append((i, same, why, (eb[:40], b[0][:40]), (pb, b[1]), (pa, a[1])))
    print("  each row's words and p before and after as the commits hold them, and its kind as its columns say: "
          + "; ".join(f"{why}: {'all as recorded' if a and k else 'DIFFER'} {n}" for (a, k, why), n in sorted(ok.items(), key=lambda kv: kv[0][2])))
    for b in bad:
        print(f"    {b}")
    ratios = sorted(row[4] / row[3] for row in rows.values() if row[5] == "P" and row[3])
    print(f"  the P rows' p after / before: median {ratios[len(ratios) // 2]:.3f}, from {ratios[0]:.3f} to {ratios[-1]:.3f}; over 1% {sum(1 for x in ratios if abs(x - 1) > 0.01)}, over 5% {sum(1 for x in ratios if abs(x - 1) > 0.05)}, over a factor of two {sum(1 for x in ratios if x > 2 or x < 0.5)} (the record: ×1.012, ×0.938 to ×1.028, 459, 38)")
    by_level = collections.Counter((row[5], row[0].split("-")[1]) for row in rows.values())
    print("  rows by kind and level: " + "; ".join(f"{k[0]} {k[1]} {v}" for k, v in sorted(by_level.items())))
    return rows


def primary_class(r):
    """local_ncsbe.nc_key's class for a primary (read, not imported): 'primary, <scope> <office type>, <n> candidates[, <seats> seats]',
    n the named candidates on the ballot, 4+ from four."""
    leg = r["office"] in ("state-lower", "state-upper") or r["office_scope"] == "state legislature"
    lead = "state legislature" if leg else f"{r['office_scope']} {r['office_type']}"   # the legislature's primaries carry no office_scope or office_type in the files
    n = len(C15.ballot_local(r))
    k = r["seats"] or 1
    return f"primary, {lead}, {n if n < 4 else '4+'} candidates" + (f", {k} seats" if k > 1 else "")


def primary_pool(rows):
    """(year, class, s) for every State Board primary of 2014 on the route can take (local_ncsbe.like_rows: p computed,
    or not computed for a pool reason, 2014's 'no earlier year to fit on' rows among them), the class by my own reading
    of the ballot (primary_class) and s the share of the deciding pair's votes its leader won, from the ballot."""
    out = []
    agree = collections.Counter()
    for r in rows:
        if r["level"] != "primary" or r["year"] < C15.NC_FIRST:
            continue
        reason = r["reason"] or ""
        if r["status"] != "value" and not any(reason.startswith(x) for x in C15.POOL_REASONS):
            continue
        k = r["seats"] or 1
        b = C15.ballot_local(r)
        if len(b) <= k:
            continue
        top = sorted([a for a in r["cands"] if a[1] is not None], key=lambda a: -a[1])
        if any(C15._generic(a[2]) for a in top[k - 1:k + 1]):
            continue
        v0, v1 = b[k - 1][1], b[k][1]
        if v0 + v1 <= 0:
            continue
        cls = primary_class(r)
        if r["cls"]:
            agree[cls == r["cls"]] += 1
        out.append((r["year"], cls, max(v0, v1) / (v0 + v1)))
    print(f"  my class for a primary against the record's where it names one: equal {agree[True]:,}, differ {agree[False]:,}")
    return out


def section_3(rows, moves):
    print("23.3 The moved (P) and new (N) p from my own pools")
    ids = {i for i, row in moves.items() if row[5] in ("P", "N")}
    medsl, nc, miss = C15.local_pools()
    nc_pool = [row for row in nc if row[0] >= C15.NC_FIRST]
    loc = [r for r in rows if r["level"] == "local" and r["id"] in ids and r["status"] == "value" and r["route"] in ("class", "boundary")]
    cm = [r for r in loc if C15.medsl_route(r)]
    cn = [r for r in loc if not C15.medsl_route(r)]
    C15.compare_like(cm, medsl, f"local, MEDSL's route (the November contests), {len(cm)} moved or new p, like races from my MEDSL pool")
    C15.compare_like(cn, nc_pool, f"local, the State Board's route, {len(cn)} moved or new p, like races from my State Board pool")
    pool = primary_pool(rows)
    print(f"\n  my primary pool: {len(pool):,} rows of {C15.NC_FIRST} on, by year " + ", ".join(f"{y} {c}" for y, c in sorted(collections.Counter(y for y, _, _ in pool).items())))
    pr = [r for r in rows if r["level"] == "primary" and r["id"] in ids and r["status"] == "value" and r["route"] == "class"]
    C15.compare_like(pr, pool, f"primaries, {len(pr)} moved or new p, like races from my primary pool (the class as the record names it)")
    allp = [r for r in rows if r["level"] == "primary" and r["status"] == "value" and r["route"] == "class"]
    bad = C15.compare_like(allp, pool, f"every primary with a like-race forecast today ({len(allp)}), the same pool")
    if bad:
        dn = collections.Counter()
        for rid, what in bad:
            m = re.search(r"mine N (\d+).*record N (\d+)", what)
            r = next(x for x in allp if x["id"] == rid)
            dn[(r["cls"], int(m.group(2)) - int(m.group(1)) if m else None)] += 1
        kl = [r for r in D.rows("primary") if r["state"] == "NC" and r["src"] == "klarner"]
        print("    the differing ones by class and the record's N less mine: " + "; ".join(f"'{k[0]}' +{k[1]}: {v}" for k, v in dn.most_common())
              + f" (a reading: the files hold 2014's legislative primaries from Klarner, {len(kl)} rows of {sorted({r['year'] for r in kl})} with no votes, where the record's pool reads the State Board's own 2014 file; the moved and new p above are not among these)")
    worst = 0.0
    n = 0
    for r in loc + pr:
        f, N, h, k = D.class_density([s for y, key, s in (medsl if C15.medsl_route(r) and r["level"] == "local" else nc_pool if r["level"] == "local" else pool) if key == r["cls"] and y < r["year"]])
        if f is None:
            continue
        pm, meth, fh = D.p_auto(r["p"]["n"], 0.5, D.sd_eq(f))
        worst = max(worst, D.rel(pm, r["p"]["value"]))
        n += 1
    print(f"  p recomputed from my (N, k, h) for {n} of them: worst relative difference {worst:.1e}")
    zero = [r for r in rows if r["id"] in {i for i, row in moves.items() if row[5] == "C"}]
    print(f"  the C rows ({len(zero)}): p today " + ", ".join(f"{k} {v}" for k, v in collections.Counter(r['p'].get('value') for r in zero).items())
          + "; names on the ballot <= seats in " + str(sum(1 for r in zero if len([a for a in r['cands'] if not C15._generic(a[2])]) <= (r['seats'] or 1))) + f"; words today: {dict(collections.Counter(re.sub(r'\d{4}-\d{2}-\d{2}', '<date>', r['election'])[:50] for r in zero))}")


def section_4(rows):
    print("23.4 c19's finding as it stands now, and the marks beyond its count")
    by_od = collections.defaultdict(list)
    for r in rows:
        by_od[(r["year"], r["level"], name_of(r), r["date"])].append(r)
    sb = [r for r in rows if r["level"] == "local" and r["date"] == "2016-03-15" and "school board" in (r["office_type"] or "")]
    fr = [r for r in sb if (r["election"] or "").startswith("first round")]
    print(f"  the school boards of 2016-03-15: {len(sb)}; marked first rounds today {len(fr)} (c19: 19); words today {dict(collections.Counter(re.sub(r'\d{4}-\d{2}-\d{2}', '<date>', r['election'])[:45] for r in sb))}; p today "
          + ", ".join(f"{k} {v}" for k, v in collections.Counter('value ' + ('0' if r['p'].get('value') == 0 else '>0') if r['status'] == 'value' else (r['reason'] or '')[:40] for r in sb).most_common()))
    nov10 = [r for r in rows if r["level"] == "local" and r["date"] == "2010-11-02" and (r["election"] or "").startswith("deciding round")]
    nov16 = [r for r in rows if r["level"] == "local" and r["date"] == "2016-11-08" and (r["election"] or "").startswith("deciding round")]
    print(f"  November deciding rounds today: 2010 {len(nov10)} (c19: 96 on a name collision), 2016 {len(nov16)} (c19: 6 of them on a collision)")
    dec = [r for r in rows if r["level"] == "local" and (r["election"] or "").startswith("deciding round")]
    own = 0
    for r in dec:
        d0 = re.findall(r"\d{4}-\d{2}-\d{2}", r["election"])
        same = [x for d in d0 for x in by_od[(r["year"], "local", name_of(r), d)] if set(x["counties"] or []) & set(r["counties"] or [])]
        own += bool(same)
    print(f"  deciding rounds today {len(dec)}: with an earlier round of the name in overlapping counties on the named date {own}")
    sp = collections.Counter()
    for r in rows:
        if r["level"] == "primary":
            el = r["election"] or ""
            if "second primary" in el:
                d0 = re.findall(r"\d{4}-\d{2}-\d{2}", el)
                same = [x for d in d0 for x in by_od[(r["year"], "primary", name_of(r), d)] if party_of(x) == party_of(r) and set(x["counties"] or []) & set(r["counties"] or [])]
                sp[("second primary followed" if "followed" in el else "second primary", "overlapping counties" if same else "NOT")] += 1
    print(f"  primaries marked with a second primary today: {dict(sp)} (the record: 217 such marks removed by #72)")
    mq = collections.Counter()
    for r in rows:
        if r["level"] == "measure" and "same title" in (r["election"] or ""):
            d0 = re.findall(r"\d{4}-\d{2}-\d{2}", r["election"])
            same = [x for d in d0 for x in by_od[(r["year"], "measure", name_of(r), d)] if set(x["counties"] or []) & set(r["counties"] or [])]
            mq["overlapping counties" if same else "NOT"] += 1
    print(f"  questions marked with one of the same title on another date today: {dict(mq)} (the record: 17 such marks removed)")


def main():
    print("C23. #72: NORTH CAROLINA'S ROUNDS KEYED BY PLACE: EVERY MARK REGENERATED, THE MOVES FILE, THE MOVED AND NEW p")
    print(f"repository HEAD {L.git_head()}")
    rows = nc_rows()
    print(f"  State Board contests in the files: " + ", ".join(f"{lv} {sum(1 for r in rows if r['level'] == lv):,}" for lv in LEVELS))
    section_1(rows)
    moves = section_2()
    section_3(rows, moves)
    section_4(rows)


if __name__ == "__main__":
    main()
