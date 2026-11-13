"""c50: D3's #113 (11c852dc -> 9ad2d3d5), the second part of section 20: Indiana 2018's House flags settled on the archive's
certified State Representative file.

The orchestrator (2026-11-13 09:58 UTC, verbatim): "D3's #113 is merged as 9ad2d3d (REPORT §37, moves-37.json). It settles
Indiana 2018's six House flags on the archive's certified House file (100 of 100 districts equal to the vote). House 100
gains p 0 and House 13 gains 1.54e-05; 6,815 p move, none by more than 1%. Take it into section 20 with #111, so that
section's end is 9ad2d3d."

Sources read apart: the archive's State Representative file (`OffCatC_2201_A.json`, office category 2201 in the cached
office list), one request (`fetch_eighth_pass.sh in_2018_house`, 2026-11-13 10:01:11 UTC, 200), as D3 read it on the
orchestrator's allowance of 09:21; the settings and the office list from the in_2018 branch (c49 §49.6). D3's rules
(local_districts' in_archive and _first_last; the settle test; route (a)'s fit) are copied from c49, which copied them.

Sections:
  50.1  moves-37.json against my own diff of every D3 record between the commits; the orchestrator's counts
  50.2  the House file: hash, the certified mark, the 100 districts against the records' counts (Klarner's), the six flags
  50.3  route (a) refitted at both commits (c49 §49.7's refit): the House's lean, the 41 Indiana 2020 House moves, every P row
  50.4  the notes, reasons and other files; D2's files

Run: python3 -I checks/m2/c50_in_house_2018.py [1 2 3 4]
"""
import collections
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402
import c40_pr_checks as C40  # noqa: E402
import c41_governor_refit as C41  # noqa: E402
import c48_district_checks_3 as C48  # noqa: E402
import c49_va_local_2 as C49  # noqa: E402

BEFORE, AFTER = "11c852dc", "9ad2d3d5"
HOUSE_FILE = "OffCatC_2201_A.json"
HOUSE_SHA = "d637b3a79c2c12470bb5f7647db4b4fc641e4cc94c3031b533e29c5c6a9a1682"   # the records' notes and D3's REPORT §37 [stated]
SIX = ("100", "13", "58", "68", "73", "75")
TITLE_RE = re.compile(r"District 0*\d+$")
# D3's REPORT §37 table [stated]: district -> (before, Klarner = the archive, MEDSL's)
D3_TABLE = {"100": ("held (+15.8%)", {"forestal": 14070}, 16296), "13": ("held (-5.7%)", {"negele": 15270, "barnes": 6494}, 20524),
            "58": ("noted (-3.2%)", {"burton": 13784, "reinert": 7981}, 21072), "68": ("noted (+3.6%)", {"lyness": 17841, "gaustad": 4834}, 23499),
            "73": ("kept", {"davisson": 17824}, 10044), "75": ("kept", {"bacon": 16118, "hurley": 10236}, 19142)}
h1 = C48.h1
at, records_at, pval, sha256 = C49.at, C49.records_at, C49.pval, C49.sha256


def section_1():
    h1(f"50.1 moves-37.json against my own diff of every D3 record, {BEFORE} -> {AFTER}")
    mv = L.load_json(at(AFTER, "data/local/moves-37.json"))
    rows = {}
    for r in mv["records"]:
        rows.setdefault(r[0], []).append(r)
    print(f"  the file: {len(mv['records']):,} rows, {len(rows):,} ids, against {mv.get('against')} (the code alone, its data main's at 11c852d = {BEFORE}'s D3 files; my diff is main to main)")
    print(f"  its summary: {json.dumps(mv['summary'])}")
    diff, data_files, d2_files, other, stamps = C49.my_diff(BEFORE, AFTER)
    print(f"  data files changed: {len(data_files) + len(d2_files) + len(other)}; D3's record files: {len(data_files)} {dict(collections.Counter(f.split('/')[1] for f in data_files))}; D2's: {len(d2_files)} (D3: no governor, House, Senate or president record moves); other: {other}")
    mine = collections.Counter((lv, c) for c, lv, yr, b, a, d in diff.values())
    agree, dis, worst, pdiff, rdiff = 0, collections.Counter(), [], 0, 0
    for i, (c, lv, yr, b, a, d) in diff.items():
        hits = rows.get(i)
        if not hits:
            worst.append((i, c, "not in the moves file", d[:6]))
            continue
        theirs = set()
        for row in hits:
            theirs |= set(row[8])
        if c in theirs or (c in ("Q", "O", "B", "R") and theirs & {"Q", "O", "R", "B"}):
            agree += 1
        else:
            dis[(lv, c, tuple(sorted(theirs)))] += 1
            worst.append((i, c, tuple(sorted(theirs)), d[:6]))
        pb, pa = pval(b or {}), pval(a or {})
        for row in hits:
            if isinstance(row[5], str) or isinstance(row[6], str):
                continue
            if (row[5] is None) != (pb is None) or (row[6] is None) != (pa is None) \
                    or (pb is not None and abs(row[5] - pb) > 1e-9 * max(abs(pb), 1e-300)) \
                    or (pa is not None and abs(row[6] - pa) > 1e-9 * max(abs(pa), 1e-300)):
                pdiff += 1
                if pdiff <= 5:
                    print(f"    p before/after differ from the record: {i} row {row[5]} {row[6]} record {pb} {pa}")
            if pb and pa and row[7] is not None and abs(row[7] - round(pa / pb, 4)) > 1.5e-4:
                rdiff += 1
                if rdiff <= 5:
                    print(f"    ratio differs: {i} row {row[7]} mine {pa / pb:.4f}")
    not_mine = [i for i in rows if i not in diff]
    print("  my diff, by level and code: " + "; ".join(f"{lv} {k} {v}" for (lv, k), v in sorted(mine.items())))
    print(f"  rows whose code I share: {agree} of {len(diff)} ids in my diff; codes differing: {sum(dis.values())}; ids in my diff but not in the file: "
          f"{len([w for w in worst if w[2] == 'not in the moves file'])}; ids in the file but not in my diff: {len(not_mine)} {not_mine[:5]}")
    print(f"  p before/after other than the record's: {pdiff}; ratios off by more than 1.5e-4: {rdiff}; records differing in p.commit alone: {stamps}")
    for (lv, c, theirs), v in sorted(dis.items(), key=lambda kv: -kv[1])[:10]:
        ex = [w for w in worst if w[1] == c and w[2] == theirs][:2]
        print(f"    mine {c} theirs {theirs} {lv}: {v}; e.g. " + "; ".join(f"{e[0]} differs in {e[3]}" for e in ex))
    for w in [w for w in worst if w[2] == "not in the moves file"][:8]:
        print(f"    not in the file: {w[0]} mine {w[1]} differs in {w[3]}")
    new_p = [(i, lv, yr, pval(a)) for i, (c, lv, yr, b, a, d) in diff.items() if c == "N" or (c == "A" and pval(a) is not None)]
    lost = [(i, lv, yr) for i, (c, lv, yr, b, a, d) in diff.items() if c == "L" or (c == "G" and pval(b) is not None)]
    moved = [(pval(a) / pval(b), i, lv, yr) for i, (c, lv, yr, b, a, d) in diff.items() if c == "P" and pval(b)]
    zero_moves = [(i, lv) for i, (c, lv, yr, b, a, d) in diff.items() if c == "P" and not pval(b)]
    print(f"  gained (a p after, none before): {len(new_p)} {new_p} (the orchestrator: House 100 gains p 0 and House 13 gains 1.54e-05); lost: {len(lost)} {lost[:3]}; new records: {sum(1 for c, *_ in diff.values() if c == 'A')}")
    over1 = [m for m in moved if abs(m[0] - 1) > 0.01]
    print(f"  p moved (every P in my diff): {len(moved):,} = " + " + ".join(f"{lv} {n:,}" for lv, n in sorted(collections.Counter(lv for _, _, lv, _ in moved).items()))
          + f" (the orchestrator: 6,815, none by more than 1%; the file's P rows {sum(1 for r in mv['records'] if 'P' in r[8]):,}); P rows with p 0 before: {zero_moves}; "
          f"beyond 1% either way: {len(over1)} {over1[:5]}; over 2x: {len([m for m in moved if m[0] > 2 or m[0] < 0.5])}; extremes: min {min(moved)[0]:.5f} {min(moved)[1]}, max {max(moved)[0]:.5f} {max(moved)[1]}")
    bands = collections.Counter()
    for r_, i, lv, yr in moved:
        bands[(lv, "within 0.001%" if abs(r_ - 1) <= 1e-5 else "within 0.1%" if abs(r_ - 1) <= 1e-3 else "0.1-1%" if abs(r_ - 1) <= 0.01 else "beyond 1%")] += 1
    print(f"  bands by level: " + "; ".join(f"{lv} {b} {n:,}" for (lv, b), n in sorted(bands.items())))
    big = sorted([m for m in moved if abs(m[0] - 1) > 1e-3], key=lambda m: m[0])
    print(f"  beyond 0.1%: {len(big)} (D3: Indiana 2020's House, 41 of its p by x0.991 to x1.0054, through the chamber's lean): {dict(collections.Counter((yr, lv, i.split('-')[3]) for r_, i, lv, yr in big))}; "
          f"x{big[0][0]:.4f} ({big[0][1]}) to x{big[-1][0]:.4f} ({big[-1][1]})" if big else "  beyond 0.1%: 0")
    leans = collections.Counter()
    for r_, i, lv, yr in big:
        b, a = diff[i][3], diff[i][4]
        leans[((b.get("forecast_inputs") or {}).get("lean"), (a.get("forecast_inputs") or {}).get("lean"), (a.get("forecast_inputs") or {}).get("lean_year"))] += 1
    print(f"    their lean before -> after (lean_year): {dict(leans)}")
    loc = [m for m in moved if m[2] == "local"]
    print(f"  local p moved: {len(loc)} (D3: 522 by the transferred route (a), within 0.001%): largest move {max(abs(r_ - 1) for r_, *_ in loc) if loc else None:.2e}; years {dict(collections.Counter(yr for _, _, _, yr in loc))}; "
          f"routes {dict(collections.Counter((diff[i][4].get('forecasts') or [{}])[-1].get('route') for _, i, _, _ in loc))}")
    print(f"  the Q rows (a note's words changed): {sorted(i for i, (c, *_) in diff.items() if c == 'Q')} (D3: the six House flags' notes)")
    return diff


def pair_votes(rk, ak):
    """The record's {surname: votes} against the archive's: equal by surname; else paired where one surname is the tail or the head
    of the other (Klarner's 'candelariareardon' against the archive's 'Reardon'; his 'harrisjr' against 'Harris' with the suffix
    moved), the votes equal; else DIFFER. Returns (equal, how)."""
    if rk == ak:
        return True, "by surname"
    if len(rk) != len(ak):
        return False, "counts differ"
    left = dict(ak)
    for k, v in rk.items():
        hit = k if k in left else next((a for a in left if (a.endswith(k) or k.endswith(a) or a.startswith(k) or k.startswith(a)) and left[a] == v), None)
        if hit is None or left[hit] != v:
            return False, "a name or a vote differs"
        del left[hit]
    return True, "by the surname's tail"


def section_2():
    h1("50.2 Indiana 2018's House from the state's archive, read apart (fetch_eighth_pass.sh in_2018_house), against the records and D3's six flags")
    path = os.path.join(C49.IN2018, HOUSE_FILE)
    mine_sha = sha256(path)
    print(f"  the State Representative file: {os.path.getsize(path):,} bytes (D3: 295,605), my sha256 {mine_sha[:16]}... {'equal to' if mine_sha == HOUSE_SHA else 'DIFFERS from'} the one the records' notes and REPORT §37 quote ({HOUSE_SHA[:16]}...)")
    with open(os.path.join(C49.IN2018, "settings.json"), encoding="utf-8-sig") as f:
        st = json.load(f)
    root = st.get("Root", st)
    print(f"  settings.json: Root.Certified = {root.get('Certified')!r} (the certified mark, 15:16); WriteTime {root.get('WriteTime')}")
    with open(os.path.join(C49.IN2018, "statewideElectionsC_A.json"), encoding="utf-8-sig") as f:
        cats = json.load(f)
    acc = []

    def walk(o):
        if isinstance(o, dict):
            if any(str(v) == "2201" for v in o.values() if not isinstance(v, (dict, list))):
                acc.append({k: v for k, v in o.items() if k in ("OFFICECATEGORYID", "OFFICE_CATEGORY_NAME")})
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(cats)
    print(f"  the office list's entry for 2201: {acc[:1]} (D3: office category 2201, 'State Representative')")
    house, raw = C49.in_archive_file(HOUSE_FILE)
    rows = (raw.get("Root", raw).get("StatewideSummary") or {}).get("Race") or []
    seats = collections.Counter(r.get("NumofSeats") for r in rows)
    print(f"  districts in the file: {len(house)} (D3: 100); OFFICE_TITLE every one 'State Representative, District NNN': {all(TITLE_RE.search(r['OFFICE_TITLE'].strip()) is not None for r in rows)}; NumofSeats {dict(seats)}; "
          f"write-in lines ('(W/I)'): {sum(1 for cs in house.values() for n, v, wi in cs if wi)} (D3: none a write-in)")
    commas = [x["NAME_ON_BALLOT"] for row in rows for cs_ in [(row.get("Candidates") or {}).get("Candidate") or []] for x in (cs_ if isinstance(cs_, list) else [cs_]) if "," in x["NAME_ON_BALLOT"]]
    print(f"  names holding a comma in the raw file (D3's _first_last moves the suffix): {commas} -> {[C49.first_last(n) for n in commas]}")
    recs = records_at(AFTER, "data/state-lower/2018/IN.json")
    recs_b = records_at(BEFORE, "data/state-lower/2018/IN.json")
    by_d = {str(int(r["place"]["district"])): r for r in recs.values() if str(r["place"]["district"]).isdigit()}
    tal = collections.Counter()
    for dno, cands in sorted(house.items(), key=lambda kv: int(kv[0])):
        r = by_d.get(dno)
        if r is None:
            tal["no record"] += 1
            continue
        rk = {C49.name_key(c["name"]): c["votes"] for c in r["result"]["candidates"] if c.get("party") != "write-in"}
        ak = {C49.name_key(n): v for n, v, wi in cands if not wi}
        eq, how = pair_votes(rk, ak)
        tal["every named candidate equal to the vote" if eq else "DIFFERS"] += 1
        tal[("paired", how)] += 1
        tal[("names on the ballot", len(rk), "=", len(ak))] += 1
        if not eq or how != "by surname":
            print(f"    district {dno}: archive {[(n, v) for n, v, wi in cands]}; record {[(c['name'], c['votes']) for c in r['result']['candidates']]}; {'equal' if eq else 'DIFFER'} ({how}): {(rk, ak)}")
    print(f"  the archive's 100 districts against the records' counts (Klarner's), candidate by candidate (by surname; where Klarner joins a two-word surname or carries the suffix in it, by the surname's tail): {dict(tal)} (D3: 100 of 100 equal to the vote)")
    chk_b = L.load_json(at(BEFORE, "data/local/check-districts.json"))
    chk_a = L.load_json(at(AFTER, "data/local/check-districts.json"))
    fl_b = {f["id"]: f for f in chk_b["years"]["2018"]["flags"]}
    fl_a = {f["id"]: f for f in chk_a["years"]["2018"]["flags"]}
    print("\n  the six House flags (D3's REPORT §37 table against the file, the records and check-districts.json):")
    for dno in SIX:
        r, rb = by_d[dno], recs_b.get(by_d[dno]["id"], {})
        fid = f"2018-IN-lower--{dno}--"
        fa, fb = fl_a.get(fid, {}), fl_b.get(fid, {})
        ak = {C49.name_key(n): v for n, v, wi in house[dno] if not wi}
        d3 = D3_TABLE[dno]
        sc = fa.get("state_count") or {}
        notes = r.get("notes") or []
        hn = [n for n in notes if HOUSE_FILE in n]
        m = re.search(r"(https://enr\.indianavoters\.in\.gov/\S+), read (\S+), sha256 ([0-9a-f]{64}): (.*?)\), so Klarner's count stands", hn[0]) if hn else None
        print(f"    House {dno}: archive {ak} = D3's table {d3[1]}: {ak == {k.upper(): v for k, v in d3[1].items()}}; MEDSL's {fa.get('medsl')} (D3: {d3[2]}); outcome before '{fb.get('outcome')}' (D3: {d3[0]}) -> after '{fa.get('outcome')}'; "
              f"state_count: by {sc.get('source', '')[-30:]!r}, read {sc.get('read_utc')}, sha {'mine' if sc.get('sha256') == mine_sha else 'DIFFERS'}, marked {sc.get('marked')}, ratio {sc.get('ratio')}; "
              f"p before {pval(rb)} ({str((rb.get('p') or {}).get('not_computed'))[:50]}) -> after {pval(r)} ({str((r.get('p') or {}).get('not_computed') or (r.get('p') or {}).get('reason'))[:60]}); "
              f"the note: url {'the file' if m and m.group(1).endswith(HOUSE_FILE) else None}, read {m.group(2) if m else None}, sha {'mine' if m and m.group(3) == mine_sha else 'DIFFERS'}, certified words {'present' if any('certified' in n for n in hn) else 'ABSENT'}; notes before {len(rb.get('notes') or [])}, after {len(notes)}")
    for lab, fl in (("before", fl_b), ("after", fl_a)):
        out = collections.Counter((f.get("outcome") or "")[:40] for f in fl.values())
        print(f"  2018's flags, every state, outcomes {lab}: {dict(out)}")
    noted_b = sorted(i for i, f in fl_b.items() if f.get("outcome") == "noted")
    noted_a = sorted(i for i, f in fl_a.items() if f.get("outcome") == "noted")
    print(f"  (D3: held 17 to 15, noted 6 to 4, kept 7 to 5, settled by the state 3 to 9) noted flags before: {noted_b}; after: {noted_a}")
    in_a = collections.Counter((f["id"].split("-")[2], f.get("outcome")) for f in fl_a.values() if f["id"].startswith("2018-IN-"))
    print(f"  Indiana's 2018 flags after: {dict(in_a)} (D3: no Indiana 2018 legislative flag stands open)")


def section_3():
    h1("50.3 Route (a) refitted at both commits (c49 §49.7's refit; Indiana 2018's rows from the records, so that House 13 joins as the records have it)")
    wb, wa = C41.worktree(BEFORE), C41.worktree(AFTER)
    override = ((2022, "NH"), (2022, "ID"), (2018, "IN"))
    rb, ab = C40.fit_rows_at(wb, override)
    ra, aa = C40.fit_rows_at(wa, override)
    print(f"  fit rows before {len(rb):,} (from the records: {sum(ab.values())}), after {len(ra):,} (from the records: {sum(aa.values())}); rows that differ by (year, state, source): "
          + ", ".join(f"{k} {aa.get(k, 0) - ab.get(k, 0):+d}" for k in sorted(set(ab) | set(aa)) if aa.get(k, 0) != ab.get(k, 0)))
    in18 = {c: sorted((r_["id"], r_["y"]) for r_ in rows if r_["year"] == 2018 and r_["state"] == "IN" and r_["sen"] == 0 and r_.get("from_record")) for c, rows in (("before", rb), ("after", ra))}
    print(f"  Indiana 2018's House rows from the records: before {len(in18['before'])}, after {len(in18['after'])}; added: {[i for i in in18['after'] if i not in in18['before']]}")
    for c, rows in (("before", in18["before"]), ("after", in18["after"])):
        ys = [y for _, y in rows]
        print(f"    the chamber's lean from them (mean Democratic share - 0.5): {c} {sum(ys) / len(ys) - 0.5:+.4f} over {len(ys)} contested races")
    in20 = {i: (r.get("forecast_inputs") or {}).get("lean") for i, r in records_at(AFTER, "data/state-lower/2020/IN.json").items()}
    in20b = {i: (r.get("forecast_inputs") or {}).get("lean") for i, r in records_at(BEFORE, "data/state-lower/2020/IN.json").items()}
    print(f"    the Indiana 2020 House records' lean: before {set(in20b.values())}, after {set(in20.values())}")
    years = sorted({r["year"] for lv in ("state-upper", "state-lower", "local") for r in C40.rows_at(wa, lv) if r["status"] == "value" and r["route"] == "partisan"} & set(range(2019, 2026)))
    years = sorted(set(years) | {2018})
    fb, fa = C40.fits_for(rb, years), C40.fits_for(ra, years)
    print(f"  fits for {years}; the fit's coefficients after against before: " + ", ".join(f"{k} {fa[2024]['coef'][k] - fb[2024]['coef'][k]:+.2e}" for k in fa[2024]["coef"]) if fa.get(2024) and fb.get(2024) else "")
    mv = L.load_json(at(AFTER, "data/local/moves-37.json"))
    prow = {r[0]: r for r in mv["records"] if "P" in r[8]}
    before_by = {}
    for lv in ("state-upper", "state-lower", "local"):
        for r in C40.rows_at(wb, lv):
            before_by[r["id"]] = r
    tal = collections.Counter()
    diffs, unlisted, n_mine = [], [], 0
    for lv in ("state-upper", "state-lower", "local"):
        for r in C40.rows_at(wa, lv):
            if r["status"] != "value" or r["route"] != "partisan":
                continue
            r0 = before_by.get(r["id"])
            if r0 is None or r0["status"] != "value":
                if r["id"] in prow or r["id"] in ("2018-state-lower-IN-13", "2018-state-lower-IN-100"):
                    p1, how1 = C40.p_of_record(wa, r, fa)
                    print(f"    {r['id']}: no p before; mine after {p1} ({str(how1)[:60]}); the record's {r['p'].get('value')}")
                continue
            row = prow.get(r["id"])
            p0, how0 = C40.p_of_record(wb, r0, fb)
            p1, how1 = C40.p_of_record(wa, r, fa)
            if not p0 or not p1:
                tal[(lv, "mine none")] += 1
                continue
            mine = p1 / p0
            if row is None:
                tal[(lv, "not a P row", "mine within 2e-5 of 1" if abs(mine - 1) <= 2e-5 else "mine within 5e-4" if abs(mine - 1) <= 5e-4 else "mine moves")] += 1
                if abs(mine - 1) > 5e-4:
                    unlisted.append((r["id"], round(mine, 5)))
                continue
            theirs = row[7] if row[7] is not None else (row[6] / row[5] if row[5] else None)
            if theirs is None:
                tal[(lv, "P row with no ratio")] += 1
                continue
            d = abs(mine - theirs)
            band = "within 5e-4" if d <= 5e-4 else "within 5e-3" if d <= 5e-3 else "within 5e-2" if d <= 5e-2 else "beyond 5e-2"
            same_dir = (mine - 1) * (theirs - 1) > 0 or abs(mine - 1) <= 5e-4 or abs(theirs - 1) <= 5e-4
            tal[(lv, band, "same direction" if same_dir else "opposite")] += 1
            n_mine += 1
            if band in ("within 5e-2", "beyond 5e-2") or not same_dir:
                diffs.append((d, r["id"], mine, theirs))
    print(f"  the file's partisan P rows with a p of mine before and after: {n_mine:,}; my ratio against the file's:")
    for k_, v in sorted(tal.items(), key=str):
        print(f"    {str(k_):70s} {v:,}")
    diffs.sort(key=lambda x: -x[0])
    for d, rid, mine, theirs in diffs[:10]:
        print(f"    {rid}: mine x{mine:.4f}, file x{theirs:.4f}")
    if unlisted:
        print(f"  records my refit moves beyond 5e-4 that the file does not list as P: {len(unlisted)} {unlisted[:8]}")
    big = []
    for i in sorted(in20):
        r = next((x for x in C40.rows_at(wa, "state-lower") if x["id"] == i), None)
        r0 = before_by.get(i)
        if r and r0 and r["status"] == "value" and r0["status"] == "value" and r["route"] == "partisan":
            p0, _ = C40.p_of_record(wb, r0, fb)
            p1, _ = C40.p_of_record(wa, r, fa)
            row = prow.get(i)
            if p0 and p1:
                big.append((i, round(p1 / p0, 4), row[7] if row else None))
    moved = [b for b in big if b[2] is not None and abs(b[2] - 1) > 1e-3]
    exact = [(i, pval(r_a) / pval(r_b)) for i in sorted(in20) for r_b, r_a in [(records_at(BEFORE, "data/state-lower/2020/IN.json").get(i), records_at(AFTER, "data/state-lower/2020/IN.json").get(i))] if r_b and r_a and pval(r_b) and pval(r_a)]
    print(f"  the Indiana 2020 House's partisan p, mine against the file: {len(big)} with a p both sides; the file's rounded ratio beyond 0.1%: {len(moved)}, the records' exact ratio beyond 0.1%: {sum(1 for i, x in exact if abs(x - 1) > 1e-3)} (D3: 41, x0.991 to x1.0054); "
          f"the largest difference between my ratio and the file's: {max(abs(m - t) for i, m, t in big if t is not None):.1e}; e.g. {moved[:4]}")


def section_4():
    h1("50.4 The notes, reasons and other files changed; D2's files")
    diff, data_files, d2_files, other, stamps = C49.my_diff(BEFORE, AFTER)
    print(f"  D2's files changed: {d2_files} (D3: none); other files: {other}")
    q = {i: v for i, v in diff.items() if v[0] == "Q"}
    print(f"  Q rows: {len(q)}: " + "; ".join(f"{i} notes {len(v[3].get('notes') or [])} -> {len(v[4].get('notes') or [])}" for i, v in sorted(q.items())))
    n = {i: v for i, v in diff.items() if v[0] == "N"}
    for i, v in sorted(n.items()):
        print(f"  N: {i}: before p {pval(v[3])} '{str((v[3].get('p') or {}).get('not_computed'))[:100]}' -> after p {pval(v[4])} '{str((v[4].get('p') or {}).get('not_computed'))[:100]}'; notes {len(v[3].get('notes') or [])} -> {len(v[4].get('notes') or [])}; fields differing: {v[5][:8]}")
    b = collections.Counter((lv, tuple(sorted(set(k.split('.')[0] for k in d)))) for i, (c, lv, yr, bb, a, d) in diff.items() if c == "B")
    print(f"  B rows (p unchanged, its block changed), by level and the fields: {dict(b)}")


def main():
    print(f"C50 (section 20, D3's #113): {BEFORE} -> {AFTER}; {L.git_head()}")
    section_1()
    section_2()
    section_3()
    section_4()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(f"C50 (section 20, D3's #113): {BEFORE} -> {AFTER}; {L.git_head()}")
        for a in sys.argv[1:]:
            globals()[f"section_{a}"]()
    else:
        main()
