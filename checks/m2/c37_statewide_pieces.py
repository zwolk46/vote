"""c37: D3's #90 (6119f98): the orchestrator's ruling of 2026-11-07 16:47 applied: statewide contests whose lines miss
counties joined from their pieces in MEDSL's file (8 joins), checked against Washington's own export where one is
read, or held with the counties missing (15 holds); North Dakota's 2022 district judgeships from the state's results
(22 records for MEDSL's 8); one-seat contests with more votes than ballots held (3, with Michigan's Supreme Court);
one-seat statewide board seats typed statewide officer (17) and Washington's three positions statewide judge (3);
every quote_file of data/measure/statewide-filed-local.json given its quote_url (163); three proposer quotes.

The orchestrator (2026-11-07 18:13 UTC): "Sixth pass: check #90, with main at b9e0702 as its fixed end. - The 8 joins:
the pieces add up from MEDSL's raw rows and together cover every county. - WA's export figures against the record. -
The 15 held contests, by your own county coverage. - ND's 22 district judgeships against the state's page. - The three
over-ballot holds, by your own ratios. - The one-seat boards now typed statewide officer. - The 163 quote URLs: a
sample opens and holds its quote. - The p moves: 3 gained, 2 lost, none moved."

What this does (every figure [measured] unless marked):
  37.1 the moves file (data/local/moves-pieces.json) against my own diff of every record file between a2a4b0a
       (before: #89) and 6119f98 (after: #90): new and gone ids, the codes, and the p moves (3 new, 2 lost, 0 moved).
  37.2 the 8 joins: each piece found in MEDSL's file by my own reading (my summaries of the raw files,
       checks/m2/m2medsl.py; and the raw rows themselves, grouped by county, where the pieces share one office name):
       the piece's counties and votes, the pieces apart, their union against every county the state's contests have
       votes in that day, and the joined record's counts as the pieces' sums.
  37.3 Washington's 2022 export (results.vote.wa.gov, fetched by fetch_sixth_pass.sh) against each record's
       result.state_total and its MEDSL counts; the page's words on certification; the certification PDF's answer.
  37.4 the 15 held contests: the 14 held "incomplete" by my own county coverage from the files (the counties missing,
       the state's count); Arizona's 2024 Corporation Commission by the seat counts of its pieces in the raw rows;
       Georgia's 2022 stray line; North Dakota's 2024 State Auditor (MEDSL's missing county, the state's total).
  37.5 North Dakota's pages (the archive, the 2022 and 2024 front pages, the statewide and judicial pages), read with
       my own copy of pipeline/intake/nd_sos.py's patterns (said so): the 22 judgeships against the 22 records
       (title, Vote For, precincts, names, votes, winners, totals); MEDSL's 8 district contests against the page;
       the 2024 State Auditor.
  37.6 the over-ballot rule re-applied from my summaries over every file fetched for 2018, 2022 and 2024: every whole
       one-seat state contest's votes against the Governor's on the same ballot; those above 1.05 against D3's.
  37.7 the 20 T rows (17 statewide officer, 3 statewide judge): each record's seat count and counties from the files;
       the rule re-applied over every state-scope board, commission or school-board record of the files read.
  37.8 the 163 quote URLs: every quote beside a quote_url found on the page the URL answers (all 20 distinct pages
       fetched), with c31's find_quote; the three proposer quotes of data/measure/thresholds.json on their pages.
  37.9 the 49 R rows: each reason's count of like races against my own count from the records' classes
       (c35.pools_at) at 6119f98, and the count before at a2a4b0a.
Nothing from pipeline/ is imported; the patterns and rules copied are marked.
"""
import collections
import csv
import glob
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402
import m2medsl as M  # noqa: E402

import c30_ballot_texts as C30  # noqa: E402
import c31_statewide_filed_local as C31  # noqa: E402
import c34_towns_counties as C34  # noqa: E402
import c35_statewide_officers as C35  # noqa: E402
import c36_courts_commissions as C36  # noqa: E402

BEFORE = "a2a4b0a"   # #89 merged
AFTER = "6119f98"    # #90 merged
MOVES = "data/local/moves-pieces.json"
LISTED = "data/measure/statewide-filed-local.json"
THRESH = "data/measure/thresholds.json"
LEVELS = ("local", "primary", "measure")
SIXTH = os.path.join(L.CACHE, "sixth")
FIFTH = os.path.join(L.CACHE, "fifth")
FOURTH = os.path.join(L.CACHE, "fourth")
# copied from pipeline/local_medsl.py at 6119f98 (#90), so that the rules are applied here as the pipeline words them;
# nothing is imported
GOVERNOR = re.compile(r"^GOVERNOR\b(?! *'S COUNCIL)")
OVER_BALLOT = 1.05
STATE_BOARD_TYPES = ("council, commission or board", "school board")
OVER_EXPECTED = {2018: {("MI", "JUSTICE OF THE SUPREME COURT"), ("OH", "JUSTICE OF THE SUPREME COURT")},
                 2022: {("HI", "AT-LARGE TRUSTEE"), ("MI", "ATTORNEY GENERAL")}}
REASON_N = C36.REASON_N
ANSWERS = {"YES", "NO", "FOR", "AGAINST", "REPEALED", "MAINTAINED", "APPROVE", "REJECT", "RETAIN", "DO NOT RETAIN"}


def st_of(c):
    return (c.get("place") or {}).get("state") or c["id"].split("-")[2]


def sixth_fetched():
    """url -> path of what fetch_sixth_pass.sh fetched (HTTP 200), and key -> (code, path) for every line"""
    by_url, by_key = {}, {}
    p = os.path.join(SIXTH, "index.txt")
    if not os.path.exists(p):
        return by_url, by_key
    for line in open(p):
        f = line.rstrip("\n").split("\t")
        if len(f) >= 6 and f[1] == "200" and os.path.exists(f[5]):
            by_url[f[4]] = f[5]
        if len(f) >= 5:
            by_key[f[0]] = (f[1], f[5] if len(f) >= 6 else None)
    return by_url, by_key


def nkey(name):
    return " ".join(re.sub(r"[^A-Z0-9 ]+", " ", (name or "").upper()).split())


def nkey2(name):
    """nkey with a middle initial (a one-letter word) set aside"""
    return " ".join(w for w in nkey(name).split() if len(w) > 1)


# ---------------------------------------------------------------------------------------------- 37.1
def my_codes(b, a):
    codes = set()
    pb, pa = b.get("p") or {}, a.get("p") or {}
    if b.get("office_type") != a.get("office_type"):
        codes.add("T")
    if "value" in pa and "value" not in pb:
        codes.add("N")
    if "value" in pb and "value" not in pa:
        codes.add("L")
    if "value" in pa and "value" in pb:
        if pa["value"] != pb["value"]:
            codes.add("P")
        elif {k for k in set(pa) | set(pb) if pa.get(k) != pb.get(k)} - {"note"}:
            codes.add("B")
    if "not_computed" in pa and "not_computed" in pb and pa["not_computed"] != pb["not_computed"]:
        codes.add("R")
    if b.get("notes") != a.get("notes"):
        codes.add("Q")
    if b.get("listed_statewide") != a.get("listed_statewide"):
        codes.add("O")
    return codes


def section_1():
    print("### 37.1 the moves file against my own diff of the record files")
    mv = C34.show(AFTER, MOVES)
    print(f"  {MOVES} at {AFTER}: {len(mv['records'])} records, against {mv['against']}; codes {sorted(mv['codes'])}; summary {json.dumps(mv['summary'])}")
    files = [f for f in C31.changed_files(BEFORE, AFTER, "data/") if re.search(r"data/(" + "|".join(LEVELS) + r")/\d{4}/[A-Z]{2}\.json$", f)]
    before = C31.load_records(BEFORE, files)
    after = C31.load_records(AFTER, files)
    print(f"  record files changed between {BEFORE} and {AFTER} (local, primary, measure): {len(files)}: {', '.join(f.split('data/')[1] for f in files)}")
    print(f"  records in them: before {len(before)}, after {len(after)}")
    new = sorted(set(after) - set(before))
    gone = sorted(set(before) - set(after))
    changed = sorted(cid for cid in set(before) & set(after) if before[cid] != after[cid])
    print(f"  new ids {len(new)}, gone ids {len(gone)}, changed records {len(changed)}")
    d3 = {r[0]: r for r in mv["records"]}
    mine = {}
    for cid in new:
        mine[cid] = {"A"}
    for cid in gone:
        mine[cid] = {"G"}
    keysets = collections.Counter()
    for cid in changed:
        b, a = before[cid], after[cid]
        mine[cid] = my_codes(b, a)
        diff = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
        keysets[(tuple(sorted(mine[cid])), tuple(diff))] += 1
    # compare
    same = sum(1 for cid, cs in mine.items() if cid in d3 and set(d3[cid][8]) == cs)
    print(f"  my codes equal D3's: {same} of {len(mine)} records of mine; D3's rows without a record of mine: {len(set(d3) - set(mine))}; mine not in D3's: {len(set(mine) - set(d3))}")
    for cid in sorted(set(mine) | set(d3)):
        if cid not in d3 or cid not in mine or set(d3[cid][8]) != mine[cid]:
            print(f"    DIFFERS: {cid[:80]}: D3 {d3[cid][8] if cid in d3 else '-'}, mine {sorted(mine.get(cid, []))}")
    print("  my code sets with the top-level keys that differ (count):")
    for (cs, diff), n in sorted(keysets.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"    {n:4d}  {''.join(cs) or '-':6s} {', '.join(diff)}")
    by_code = collections.Counter()
    for cid, cs in mine.items():
        lvl = cid.split("-")[1]
        for c in cs:
            by_code[f"{lvl} {c}"] += 1
    print(f"  my counts by level and code: {dict(sorted(by_code.items()))}")
    print(f"  D3's: {json.dumps(mv['summary'])}")
    # the p moves
    for code, words in (("N", "new p"), ("L", "p no longer computed"), ("P", "p moved"), ("B", "p unchanged, its block changed")):
        rows = sorted(cid for cid, cs in mine.items() if code in cs)
        print(f"  {code} ({words}): {len(rows)}")
        for cid in rows:
            print(f"    {cid[:80]}: {C34.pval(before[cid])!s:.70} -> {C34.pval(after[cid])!s:.70}")
    return before, after, mv


# ---------------------------------------------------------------------------------------------- 37.2
def raw_contests(path, year, offices):
    """the rows of the named offices (office keys; dataverse STATE, stage GEN) grouped by county: {(office, district):
    {county: {"mags": set, "cands": {cand: votes}, "precincts": n}}}; county '' for a row with no county code"""
    cells = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(dict)))
    mags = collections.defaultdict(lambda: collections.defaultdict(set))
    for r in M.rows(path):
        office = M.office_key(r.get("office"))
        if office not in offices or (r.get("dataverse") or "") != "STATE" or (r.get("stage") or "").upper() != "GEN":
            continue
        cand = (r.get("candidate") or "").strip().upper()
        if M.is_meta(cand):
            continue
        try:
            votes = int(float(r.get("votes") or ""))
        except ValueError:
            continue
        county = M.fips5(r.get("county_fips", ""))
        if not re.fullmatch(r"\d{5}", county):
            county = ""
        pk = (county, r.get("jurisdiction_fips", ""), r.get("precinct", ""))
        key = (office, (r.get("district") or "").strip().upper())
        mode = (r.get("mode") or "TOTAL").upper()
        cell = cells[key][county][(pk, cand)]
        cell[mode] = cell.get(mode, 0) + votes
        mags[key][county].add((r.get("magnitude") or "").strip())
    out = {}
    for key, bycounty in cells.items():
        out[key] = {}
        for county, pkc in bycounty.items():
            tot = collections.Counter()
            voted = set()
            for (pk, cand), modes in pkc.items():
                v = M._resolve(modes)
                if v is not None:
                    tot[cand] += v
                    if v > 0:
                        voted.add(pk)
            out[key][county] = {"mags": mags[key][county], "cands": dict(tot), "precincts": len(voted)}
    return out


def section_2(after):
    print("### 37.2 the 8 joins: the pieces from MEDSL's raw rows, apart and together")
    joined = sorted((c for c in after.values() if c.get("pieces_joined")), key=lambda c: c["id"])
    print(f"  records at {AFTER} with pieces_joined: {len(joined)} (D3: 8 = 6 local + 2 measure)")
    summaries, raws = {}, {}
    tal = collections.Counter()
    for c in joined:
        cid, st, year, date = c["id"], st_of(c), c["year"], c["date"]
        paths = M.medsl_files(year, st)
        if not paths:
            print(f"    {cid}: MEDSL file not fetched")
            tal["file not fetched"] += 1
            continue
        path = paths[0]
        if path not in summaries:
            summaries[path] = M.summary(path, year)
        s = summaries[path]
        allc = set(s["counties_all"].get(f"{st}|{date}", []))
        offices = {M.office_key(p["office"]) for p in c["pieces_joined"]}
        dist = ((c.get("place") or {}).get("district") or "").strip().upper()
        same_name = len(offices) < len(c["pieces_joined"])
        if same_name:   # the pieces share one office name: my summary merges them, so the raw rows are read by county
            if (path, tuple(sorted(offices))) not in raws:
                raws[(path, tuple(sorted(offices)))] = raw_contests(path, year, offices)
            raw = raws[(path, tuple(sorted(offices)))]
            keys = [k for k in raw if k[0] in offices and (k[1] == dist or (not dist and k[1] in ("", "STATEWIDE")))]
            mine_c = set().union(*[set(raw[k]) for k in keys]) if keys else set()
            # the office's rows under another district code, in counties the record's district has none in (Santa Cruz's
            # Corporation Commission rows under 001, 002, 003); another seat's district (Oregon's position 1) is not that
            others = [k for k in raw if k[0] in offices and k not in keys and not (set(raw[k]) & mine_c)]
            bycounty, bycounty_all = {}, {}
            def add(into, k):
                for county, v in raw[k].items():
                    cell = into.setdefault(county, {"mags": set(), "cands": collections.Counter(), "precincts": 0})
                    cell["mags"] |= v["mags"]
                    cell["cands"].update(v["cands"])
                    cell["precincts"] += v["precincts"]
            for k in keys:
                add(bycounty, k)
            for k in keys + others:
                add(bycounty_all, k)
            if others:
                print(f"  {cid}: the office's rows under other district codes: " + "; ".join(
                    f"district {k[1]!r}: counties {sorted(raw[k])}, magnitude {sorted(set().union(*[v['mags'] for v in raw[k].values()]))}, votes {sum(sum(v['cands'].values()) for v in raw[k].values()):,}" for k in others))
            # the pieces: counties grouped by (magnitude, the names with votes)
            groups = collections.defaultdict(list)
            for county, v in bycounty.items():
                groups[(tuple(sorted(v["mags"])), tuple(sorted(k for k, n in v["cands"].items() if n > 0)))].append(county)
            print(f"  {cid}: one office name {sorted(offices)} district {dist!r}: {len(bycounty)} counties in the raw rows; groups by (magnitude, names with votes):")
            for (mg, names), cs in sorted(groups.items(), key=lambda kv: -len(kv[1])):
                votes = collections.Counter()
                for county in cs:
                    votes.update(bycounty[county]["cands"])
                print(f"      magnitude {list(mg)}, {len(cs)} counties {sorted(cs) if len(cs) <= 4 else ''}: {len(names)} names, votes {sum(votes.values()):,}: {dict(votes.most_common(4))}")
            my_pieces, my_pieces_all = {}, {}
            for p in c["pieces_joined"]:
                pcs = set(p["counties"])
                for src, into in ((bycounty, my_pieces), (bycounty_all, my_pieces_all)):
                    votes = collections.Counter()
                    mg = set()
                    for county in pcs:
                        votes.update(src.get(county, {}).get("cands", {}))
                        mg |= src.get(county, {}).get("mags", set())
                    into[tuple(sorted(pcs))] = (dict(votes), mg, sum(src.get(x, {}).get("precincts", 0) for x in pcs))
            allsum = collections.Counter()
            for county, v in bycounty_all.items():
                allsum.update(v["cands"])
            rc0 = {nkey(x["name"]): x["votes"] for x in c["result"]["candidates"]}
            a1 = {nkey(k): v for k, v in allsum.items() if v}
            a2 = collections.Counter()
            for k, v in a1.items():
                a2[nkey2(k)] += v
            eq = rc0 == a1 or ({nkey2(k): v for k, v in rc0.items()} == dict(a2) and "equal, a middle initial aside")
            print(f"    the record's counts == my sums over the office's rows in every county ({len(bycounty_all)} counties, the other district codes above counted in): {eq}")
        else:
            my_pieces, my_pieces_all = {}, {}
            for p in c["pieces_joined"]:
                office = M.office_key(p["office"])
                hits = {k: v for k, v in s["state_contests"].items()
                        if k.split("|")[0] == st and k.split("|")[1] == date and "|".join(k.split("|")[2:-1]) == office
                        and (k.split("|")[-1].strip().upper() == dist or (not dist and k.split("|")[-1].strip().upper() in ("", "STATEWIDE")))}
                if len(hits) != 1:
                    print(f"    {cid}: piece {p['office']!r}: {len(hits)} contests in my summary")
                    tal["piece not found once"] += 1
                    continue
                v = next(iter(hits.values()))
                my_pieces[tuple(sorted(v["counties"]))] = (v["cands"], set(v["magnitudes"]), v["precincts"])
        # each piece against the record's
        union = set()
        total = collections.Counter()
        ok_votes = ok_counties = True
        for p in c["pieces_joined"]:
            pcs = tuple(sorted(p["counties"]))
            mine = my_pieces.get(pcs)
            if mine is None:
                near = [k for k in my_pieces if set(k) & set(pcs)]
                print(f"    {cid}: piece {p['office']!r} in {len(pcs)} counties: no contest of mine with these counties (mine: {[len(k) for k in near]} counties)")
                ok_counties = False
                continue
            votes, mg, prec = mine
            pv = {nkey(k): v for k, v in p["votes"].items()}
            mv_ = {nkey(k): v for k, v in votes.items() if v}
            same = pv == mv_
            how = "equal"
            if not same and pcs in my_pieces_all:
                votes2, mg2, prec2 = my_pieces_all[pcs]
                mv2 = {nkey(k): v for k, v in votes2.items() if v}
                if pv == mv2:
                    same, how = True, f"equal once the office's rows under the other district codes are counted in (magnitude then {sorted(mg2)}, precincts {prec2})"
            ok_votes &= same
            seats = C36.seats_of(mg)
            print(f"    piece {p['office']!r}: {len(pcs)} counties, precincts {p.get('precincts')} (mine {prec}), seats {p.get('seats')} (my magnitude {sorted(mg)}), "
                  f"votes {sum(p['votes'].values()):,} (mine {sum(mv_.values()):,}): {how if same else 'DIFFERS ' + json.dumps(mv_)[:200]}")
            if union & set(pcs):
                print(f"      DIFFERS: pieces share counties {sorted(union & set(pcs))}")
            union |= set(pcs)
            total.update(pv)
        rc = {nkey(x["name"]): x["votes"] for x in c["result"]["candidates"]}
        rc_ok = rc == dict(total)
        if not rc_ok:
            t2 = collections.Counter()
            for k, v in total.items():
                t2[nkey2(k)] += v
            if {nkey2(k): v for k, v in rc.items()} == dict(t2):
                rc_ok = "equal once a middle initial is set aside (the pipeline's name key joins the two spellings)"
        cover = "every county" if allc <= union else f"{len(union & allc)} of {len(allc)} counties (missing {sorted(allc - union)})"
        vi = (c.get("result") or {}).get("votes_incomplete") or {}
        print(f"    together: {cover}; the record's counts == the pieces' sums: {rc_ok}" + ("" if rc_ok else f" (record {rc}, pieces {dict(total)})")
              + f"; total_votes {c['result'].get('total_votes'):,} == {sum(total.values()):,}: {c['result'].get('total_votes') == sum(total.values())}"
              + (f"; the record's votes_incomplete: {len(vi.get('counties_missing', []))} of {vi.get('counties_of_state')} missing" if vi else ""))
        tal[f"pieces' votes equal: {ok_votes and ok_counties}; record == sums: {rc_ok if rc_ok in (True, False) else 'True (a middle initial aside)'}; {'every county' if allc <= union else 'not every county'}"] += 1
    print(f"  the joins: {dict(tal)}")
    print("  files read: " + "; ".join(f"{os.path.basename(p)} ({s['rows']:,} rows, sha256 {s['sha256'][:12]})" for p, s in sorted(summaries.items())))
    return summaries, raws


# ---------------------------------------------------------------------------------------------- 37.3
def wa_export():
    by_url, by_key = sixth_fetched()
    races = {}
    files = {}
    for name in ("StateExecutive", "Judicial", "Measures"):
        code, path = by_key.get(f"wa_sos:{name}", (None, None))
        if code != "200" or not path:
            continue
        files[name] = (path, L.sha256(path))
        with open(path, encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                races.setdefault(row["Race"].strip(), {})[row["Candidate"].strip()] = int(row["Votes"])
    return races, files, by_key


def section_3(after):
    print("### 37.3 Washington's 2022 export against the records' state_total and MEDSL counts")
    races, files, by_key = wa_export()
    if not races:
        print("  the export files are not fetched: nothing compared")
        return
    print(f"  export files: " + "; ".join(f"{n} ({os.path.basename(p)}, sha256 {h[:12]})" for n, (p, h) in sorted(files.items())) + f"; races {len(races)}")
    code, path = by_key.get("wa_sos:results", (None, None))
    if path:
        t = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", open(path, encoding="utf-8", errors="replace").read())).split())
        for w in ("certified by each county", "certifies final results", "before certification are unofficial", "except for King County"):
            m = re.search(re.escape(w), t)
            print(f"    the results page: {'says' if m else 'does not say'} {w!r}" + (f": '...{t[max(0, m.start() - 60):m.end() + 40]}...'" if m else ""))
    code, path = by_key.get("wa_sos:export_page", (None, None))
    if path:
        e = open(path, encoding="utf-8", errors="replace").read()
        print(f"    the Export page links the three files: {all(f'export/20221108_{n}.csv' in e for n in ('StateExecutive', 'Judicial', 'Measures'))}")
    print(f"    SignedCertification.pdf: HTTP {by_key.get('wa_sos:certified_pdf', ('not fetched',))[0]} (D3: 404 at 16:51 UTC)")
    recs = sorted((c for c in after.values() if (c.get("result") or {}).get("state_total")), key=lambda c: c["id"])
    print(f"  records at {AFTER} with result.state_total: {len(recs)} (D3: 6: the Secretary of State, positions 1, 5 and 6, advisory votes 39 and 40)")
    tal = collections.Counter()
    for c in recs:
        stt = c["result"]["state_total"]
        race = stt.get("race")
        ex = races.get(race)
        if ex is None:
            print(f"    {c['id']}: race {race!r} not in the export")
            tal["race not in the export"] += 1
            continue
        exn = {nkey(k): v for k, v in ex.items()}
        stn = {nkey(k): v for k, v in (stt.get("votes") or {}).items()}
        rec = {nkey(x["name"]): x["votes"] for x in c["result"]["candidates"]}
        less = {nkey(k): v for k, v in (stt.get("medsl_less_state") or {}).items()}
        my_less = {k: rec.get(k, 0) - exn[k] for k in exn}
        ok = exn == stn
        ok2 = less == my_less
        print(f"    {c['id'][:70]}: export {ex}; state_total.votes == export: {ok}; medsl_less_state {less} == record - export: {ok2}; counts_used {stt.get('counts_used')}; "
              f"certified.marked {(stt.get('certified') or {}).get('marked')}; export names {len(ex)} (one name + WRITE-IN: {len(ex) == 2 and 'WRITE-IN' in ex})")
        tal[f"state_total == export {ok}, medsl_less_state right {ok2}"] += 1
    print(f"  {dict(tal)}")
    # the positions: the export's seat reading
    for cid in ("2022-local-WA-SUPREME_COURT___JUSTICE_POSITION__01", "2022-local-WA-SUPREME_COURT___JUSTICE_POSITION__05", "2022-local-WA-SUPREME_COURT___JUSTICE_POSITION__06"):
        c = after.get(cid)
        if c:
            print(f"    {cid}: type {c.get('office_type')}, p {C34.pval(c)!s:.60}, seats_note {str(c.get('seats_note'))[:120]!r}")


# ---------------------------------------------------------------------------------------------- 37.4
def section_4(after, summaries, raws):
    print("### 37.4 the 15 held contests, by my own county coverage")
    held = sorted((c for c in after.values() if (c.get("result") or {}).get("votes_incomplete")), key=lambda c: c["id"])
    print(f"  records at {AFTER} with result.votes_incomplete: {len(held)} (D3: 14 held 'incomplete'; the 15th is Arizona's 2024 Corporation Commission, 'seats differ')")
    tal = collections.Counter()
    for c in held:
        cid, st, year, date = c["id"], st_of(c), c["year"], c["date"]
        paths = M.medsl_files(year, st)
        if not paths:
            print(f"    {cid}: MEDSL file not fetched")
            tal["file not fetched"] += 1
            continue
        path = paths[0]
        if path not in summaries:
            summaries[path] = M.summary(path, year)
        s = summaries[path]
        con, how = C36.medsl_contest(c, s)
        allc = set(s["counties_all"].get(f"{st}|{date}", []))
        got = set()
        for v in con.values():
            got.update(v["counties"])
        miss = sorted(allc - got)
        vi = c["result"]["votes_incomplete"]
        ok = miss == vi.get("counties_missing") and len(allc) == vi.get("counties_of_state")
        reason = (c.get("p") or {}).get("not_computed", "")
        print(f"    {cid[:70]}: mine {len(got & allc)} of {len(allc)} counties, missing {miss}; the record's {len(vi.get('counties_missing', []))} of {vi.get('counties_of_state')}: {'equal' if ok else 'DIFFERS'}; "
              f"contests matched {len(con)} ({how}); p: {reason[:60]!r}; winner marked: {any(x.get('won') for x in c['result']['candidates'])}")
        tal[f"equal {ok}"] += 1
    print(f"  the 14: {dict(tal)}")
    # Arizona's 2024 Corporation Commission
    c = after.get("2024-local-AZ-CORPORATION_COMMISSIONER")
    if c:
        key = [k for k in raws if "2024-az" in k[0]]
        if key:
            raw = raws[key[0]]
            k = next((k for k in raw if k[0] == "CORPORATION COMMISSIONER"), None)
            mg = collections.Counter()
            for county, v in raw.get(k, {}).items():
                mg[tuple(sorted(v["mags"]))] += 1
            print(f"  Arizona 2024 Corporation Commissioner: magnitudes by county in the raw rows {dict(mg)}; the record: type {c.get('office_type')}, p {C34.pval(c)!s:.120}; winner marked: {any(x.get('won') for x in c['result']['candidates'])}")
        else:
            print("  Arizona 2024: raw rows not read")
    # Georgia's 2022 stray line
    paths = M.medsl_files(2022, "GA")
    if paths:
        raw = raw_contests(paths[0], 2022, {"SECRETARY OF STATE"})
        k = next((k for k in raw if k[0] == "SECRETARY OF STATE"), None)
        bc = raw.get(k, {})
        nocounty = bc.get("", {})
        s = M.summary(paths[0], 2022)
        allc = set(s["counties_all"].get("GA|2022-11-08", []))
        print(f"  Georgia 2022 Secretary of State ({os.path.basename(paths[0])}): counties with a code {len([x for x in bc if x])} of the state's {len(allc)}; rows with no county code: "
              f"{len(nocounty.get('cands', {}))} name(s), votes {nocounty.get('cands')}")
        for cid in ("2022-local-GA-SECRETARY_OF_STATE", "2022-local-GA-SECRETARY_OF_STATE~2"):
            c = after.get(cid)
            if c:
                print(f"    {cid}: type {c.get('office_type')}, candidates {[(x['name'], x['votes']) for x in c['result']['candidates']][:4]}, p {C34.pval(c)!s:.100}; winner marked: {any(x.get('won') for x in c['result']['candidates'])}")
    else:
        print("  Georgia 2022: file not fetched")
    # North Dakota's 2024 State Auditor
    c = after.get("2024-local-ND-STATE_AUDITOR")
    paths = M.medsl_files(2024, "ND")
    if c and paths:
        s = M.summary(paths[0], 2024)
        con, how = C36.medsl_contest(c, s)
        allc = set(s["counties_all"].get("ND|2024-11-05", []))
        got = set()
        cands = collections.Counter()
        for v in con.values():
            got.update(v["counties"])
            cands.update(v["cands"])
        mv_ = {nkey(k): v for k, v in cands.items()}
        rm = {nkey(k): v for k, v in (c["result"].get("medsl_votes") or {}).items()}
        print(f"  North Dakota 2024 State Auditor: MEDSL's lines in {len(got & allc)} of {len(allc)} counties, missing {sorted(allc - got)}; MEDSL's votes {dict(cands)} == result.medsl_votes: {mv_ == rm}; "
              f"the record's votes {[(x['name'], x['votes']) for x in c['result']['candidates']]} (votes_source {c['result'].get('votes_source')}), p {C34.pval(c)!s:.80}")


# ---------------------------------------------------------------------------------------------- 37.5
def _text(s):
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", s)).split())


def _num(s):
    return int(s.replace(",", "").strip())


def nd_parse(path):
    """copied from pipeline/intake/nd_sos.py parse() at 6119f98 (the patterns of the state's page), so that the page is
    read here as the pipeline reads it; nothing is imported"""
    with open(path, encoding="utf-8", errors="replace") as f:
        s = f.read()
    out = []
    for b in re.split(r'<div class="display-results-box-a">', s)[1:]:
        title = _text(re.search(r"<h1>(.*?)</h1>", b, re.S).group(1))
        vote_for = re.search(r"<h2>\s*Vote For (\d+)\s*</h2>", b)
        prec = re.search(r"Precincts Fully:\s*([\d,]+)\s*/\s*([\d,]+)", b)
        body = b[b.index("candidate-rows"):b.index("display-results-box-totalvotes")]
        cands = []
        for row in re.split(r'<div class="section group', body)[1:]:
            name = re.search(r'display-results-box-d"[^>]*>\s*<h2>(.*?)</h2>', row, re.S)
            votes = re.search(r'display-results-box-g"[^>]*>([\d,]+)</h2>', row)
            party = re.search(r'display-results-box-e">\s*<div[^>]*>([^<]*)</div>', row)
            if not (name and votes):
                continue
            n = _text(name.group(1))
            if n.split() == ["write-in", "write-in"]:
                n = "write-in"
            cands.append({"name": n, "party": party.group(1).strip() if party else None, "votes": _num(votes.group(1)),
                          "won": row.lstrip().startswith("winner") or ' winner"' in row[:40]})
        total = re.search(r'display-results-box-total">([\d,]+)</h2>', b)
        out.append({"office": title, "vote_for": int(vote_for.group(1)) if vote_for else None,
                    "precincts": [_num(prec.group(1)), _num(prec.group(2))] if prec else None,
                    "candidates": cands, "total": _num(total.group(1)) if total else None})
    return out


def section_5(after):
    print("### 37.5 North Dakota's pages: the 22 judgeships, MEDSL's 8 district contests, the 2024 State Auditor")
    by_url, by_key = sixth_fetched()
    code, arch = by_key.get("nd_sos:archive", (None, None))
    if arch:
        a = open(arch, encoding="utf-8", errors="replace").read()
        links = [(html.unescape(h), _text(t)) for h, t in re.findall(r'href="([^"]+)"[^>]*>(.*?)</a>', a, re.S)]
        for words, front in (("General Election - November 8, 2022", "https://results.sos.nd.gov/Default.aspx?map=Cty&eid=vxUYQ0lrpP4."),
                             ("General Election - November 5, 2024", "https://results.sos.nd.gov/Default.aspx?map=Cty")):
            print(f"  the archive links {words!r} to {front}: {(front, words) in links}")
    for year in (2022, 2024):
        code, fp = by_key.get(f"nd_sos:{year}:front", (None, None))
        if fp:
            fs = open(fp, encoding="utf-8", errors="replace").read()
            heading = f"<h1><span>Official</span> {year} General Election Results</h1>"
            print(f"  the {year} front page carries {heading!r}: {heading in fs}; links the statewide page: {'ResultsSW.aspx?text=All&type=SW&map=CTY' in fs or 'ResultsSW.aspx?text=All&amp;type=SW&amp;map=CTY' in fs}; "
                  f"the judicial page: {'ResultsSW.aspx?text=Race&type=JD&map=CTY&area=District' in fs or 'ResultsSW.aspx?text=Race&amp;type=JD&amp;map=CTY&amp;area=District' in fs}")
            for k in ("statewide", "judicial"):
                code2, pp = by_key.get(f"nd_sos:{year}:{k}", (None, None))
                if pp:
                    print(f"    the {year} {k} page carries the heading: {heading in open(pp, encoding='utf-8', errors='replace').read()} (sha256 {L.sha256(pp)[:12]})")
    # the 22 judgeships
    code, jp = by_key.get("nd_sos:2022:judicial", (None, None))
    recs = sorted((c for c in after.values() if c["id"].startswith("2022-local-ND-JUDGE_OF_THE_DISTRICT_COURT")), key=lambda c: c["id"])
    print(f"  records at {AFTER} 'Judge Of The District Court' 2022: {len(recs)} (D3: 22)")
    if not jp:
        print("  the 2022 judicial page is not fetched: nothing compared")
    else:
        page = nd_parse(jp)
        judges = [b for b in page if b["office"].startswith("Judge of the District Court")]
        print(f"  the judicial page: {len(page)} contests, {len(judges)} 'Judge of the District Court ...'; Vote For {dict(collections.Counter(b['vote_for'] for b in judges))}; "
              f"every precinct reported {sum(1 for b in judges if b['precincts'] and b['precincts'][0] == b['precincts'][1])} of {len(judges)}; "
              f"candidates add to the total {sum(1 for b in judges if b['total'] == sum(x['votes'] for x in b['candidates']))} of {len(judges)}")
        bytitle = {b["office"]: b for b in page}
        tal = collections.Counter()
        for c in recs:
            title = c["result"].get("office_as_listed")
            b = bytitle.get(title)
            if not b:
                print(f"    {c['id'][:80]}: {title!r} not on the page")
                tal["not on the page"] += 1
                continue
            pv = {nkey(x["name"]): (x["votes"], x["won"]) for x in b["candidates"]}
            rv = {nkey(x["name"]): (x["votes"], bool(x.get("won"))) for x in c["result"]["candidates"]}
            ok = pv == rv and c["result"].get("total_votes") == b["total"]
            tal[f"names, votes, winners and total equal: {ok}; Vote For {b['vote_for']}"] += 1
            if not ok:
                print(f"    DIFFERS: {c['id'][:80]}: page {pv}, total {b['total']}; record {rv}, total {c['result'].get('total_votes')}")
        print(f"  the 22 against the page: {dict(tal)}; the page's judgeships not in the records: {sorted(set(b['office'] for b in judges) - {c['result'].get('office_as_listed') for c in recs})}")
        # MEDSL's 8 district contests against the page
        paths = M.medsl_files(2022, "ND")
        if paths:
            s = M.summary(paths[0], 2022)
            districts = collections.defaultdict(list)
            for c in recs:
                districts[c["place"]["district"].split(", JUDGESHIP")[0]].append(c)
            print(f"  MEDSL's 2022 file ({os.path.basename(paths[0])}, sha256 {s['sha256'][:12]}): 'JUSTICE OF THE SUPREME COURT' contests {len([k for k in s['state_contests'] if k.split('|')[2] == 'JUSTICE OF THE SUPREME COURT'])} (one statewide, 8 by district)")
            for dist, cs in sorted(districts.items()):
                k = f"ND|2022-11-08|JUSTICE OF THE SUPREME COURT|{dist}"
                v = s["state_contests"].get(k)
                if not v:
                    print(f"    {dist}: not in my summary")
                    continue
                med = {nkey(a): b for a, b in v["cands"].items()}
                page_names = {}
                wi = 0
                for c in cs:
                    b = bytitle.get(c["result"].get("office_as_listed"), {})
                    for x in b.get("candidates", []):
                        if x["name"] == "write-in":
                            wi += x["votes"]
                        else:
                            page_names[nkey(x["name"])] = x["votes"]
                same = all(med.get(n) == pv for n, pv in page_names.items() if n in med)
                missing = sorted(set(page_names) - set(med))
                print(f"    {dist}: {len(cs)} judgeships; MEDSL {len(med) - ('WRITE IN' in med)} names, magnitude {v['magnitudes']}, {len(v['counties'])} counties; the page's {len(page_names)} names: "
                      f"MEDSL's votes equal the page's for the names it holds: {same}; names on the page not in MEDSL: {missing}; write-ins: page {wi:,}, MEDSL {med.get('WRITE IN', 0):,}")
    # the 2022 statewide Supreme Court and the 2024 State Auditor
    for year, office, cid in ((2022, "Justice of the Supreme Court", "2022-local-ND-JUSTICE_OF_THE_SUPREME_COURT"), (2024, "State Auditor", "2024-local-ND-STATE_AUDITOR")):
        code, sp = by_key.get(f"nd_sos:{year}:statewide", (None, None))
        c = after.get(cid) or C31.load_records(AFTER, [f"data/local/{year}/ND.json"]).get(cid)
        if sp and c:
            hits = [b for b in nd_parse(sp) if b["office"] == office]
            for b in hits:
                pv = {nkey(x["name"]): x["votes"] for x in b["candidates"]}
                rv = {nkey(x["name"]): x["votes"] for x in c["result"]["candidates"]}
                print(f"  {year} statewide page {office!r}: Vote For {b['vote_for']}, precincts {b['precincts']}, {pv}, total {b['total']:,}; the record's {rv} (votes_source {c['result'].get('votes_source', 'medsl')}): "
                      f"{'equal' if pv == rv else 'DIFFERS'}; winners on the page {[x['name'] for x in b['candidates'] if x['won']]}, in the record {[x['name'] for x in c['result']['candidates'] if x.get('won')]}")


# ---------------------------------------------------------------------------------------------- 37.6
def all_medsl_files():
    """(year, path) of every MEDSL raw file in the caches (2018 zips by git, 2022 and 2024 by Dataverse)"""
    out = []
    for d in (os.path.join(FIFTH, "medsl"), os.path.join(FOURTH, "medsl")):
        for p in sorted(glob.glob(os.path.join(d, "*"))):
            n = os.path.basename(p)
            if n.startswith("2016") or n.startswith("2020"):
                continue
            year = 2018 if n.startswith("2018") else 2024 if n.startswith("2024") else 2022
            if n not in {os.path.basename(x) for _, x in out}:
                out.append((year, p))
    return out


def is_question(cands):
    """every name an answer (YES, NO, FOR, ..., or 'NAME - YES'), a retention's blank-vote lines aside: the pipeline's
    question flag as I read it"""
    names = [k for k in cands if nkey(k) not in ("WRITE IN", "WRITEIN") and not re.search(r"BLANK VOTED|OVER ?VOTE|UNDER ?VOTE", k.upper())]
    return bool(names) and all(nkey(n) in ANSWERS or M.answer_of(n) for n in names)


def section_6():
    print("### 37.6 the over-ballot rule re-applied from my summaries: every whole one-seat state contest against the Governor's votes")
    found = collections.defaultdict(set)
    near = []
    n_files = n_contests = 0
    govs = {}
    read = []
    for year, path in all_medsl_files():
        s = M.summary(path, year)
        n_files += 1
        read.append((os.path.basename(path), s["rows"], s["sha256"][:12]))
        allc = {k: set(v) for k, v in s["counties_all"].items()}
        gov = {}
        for k, v in s["state_contests"].items():
            st, date, office = k.split("|")[0], k.split("|")[1], k.split("|")[2]
            a = allc.get(f"{st}|{date}", set())
            if GOVERNOR.match(office) and len(a) > 1 and a <= set(v["counties"]):
                gov[(st, date)] = max(gov.get((st, date), 0), sum(x for x in v["cands"].values() if x))
        govs.update(gov)
        for k, v in s["state_contests"].items():
            st, date, office = k.split("|")[0], k.split("|")[1], k.split("|")[2]
            t = gov.get((st, date))
            a = allc.get(f"{st}|{date}", set())
            if not t or C36.seats_of(set(v["magnitudes"])) != 1 or not (len(a) > 1 and a <= set(v["counties"])):
                continue
            if GOVERNOR.match(office) or office in ("STATE HOUSE", "STATE SENATE") or is_question(v["cands"]):
                continue
            n_contests += 1
            vv = sum(x for x in v["cands"].values() if x)
            if vv > OVER_BALLOT * t:
                found[year].add((st, office))
                print(f"    over: {year} {st} {office!r} district {k.split('|')[-1]!r}: {vv:,} votes, {vv / t:.2f} times the Governor's {t:,}")
            elif vv > 0.95 * t:
                near.append((year, st, office, vv, t, vv / t))
    print(f"  files read {n_files}; states and dates with a whole Governor contest {len(govs)}; whole one-seat state contests (not the Governor, the legislature or a question) under them {n_contests}")
    for year in sorted(set(found) | set(OVER_EXPECTED)):
        print(f"  {year}: over 1.05 by my ratios {sorted(found.get(year, set()))}; D3's OVER_EXPECTED {sorted(OVER_EXPECTED.get(year, set()))}: {'equal' if found.get(year, set()) == OVER_EXPECTED.get(year, set()) else 'DIFFERS'}")
    print(f"  within 5% below the Governor's votes but not over (not held): {len(near)}")
    for year, st, office, vv, t, r in sorted(near):
        print(f"    {year} {st} {office!r}: {vv:,} = {r:.3f} x {t:,}")
    print("  files read: " + "; ".join(f"{n} ({r:,} rows, {h})" for n, r, h in read))


# ---------------------------------------------------------------------------------------------- 37.7
def my_type(office, before_type, whole, seats, district, scope):
    """the rulings of 16:19 and 16:47 as I read them, from the source's own seat count and counties (c36.my_type, with
    the one-seat board seat and the state executive office with a district code added)"""
    o = " ".join(str(office or "").upper().split())
    if scope == "state" and district in ("", "STATEWIDE", "000", None) and C35.my_office(o):
        return "statewide officer"
    if scope == "state" and whole and seats == 1 and not C36.RETENTION.search(o) and "CLERK" not in o:
        if C36.STATE_COURT.search(o):
            return "statewide judge"
        if C36.STATE_COMMISSION.search(o) and before_type == "council, commission or board":
            return "statewide officer"
        if before_type in STATE_BOARD_TYPES:
            return "statewide officer"
    return before_type


def section_7(before, after, mv, summaries):
    print("### 37.7 the 20 T rows and the one-seat board rule re-applied")
    T = [r for r in mv["records"] if "T" in r[8]]
    print(f"  T rows: {len(T)} (D3: 17 typed statewide officer, 3 statewide judge); before -> after: {dict(collections.Counter((r[3], r[4]) for r in T))}")
    races, _, _ = wa_export()
    tal = collections.Counter()
    for r in sorted(T, key=lambda r: r[0]):
        c = after[r[0]]
        st, year, date = st_of(c), c["year"], c["date"]
        paths = M.medsl_files(year, st)
        if not paths:
            print(f"    {r[0]}: file not fetched")
            tal["file not fetched"] += 1
            continue
        path = paths[0]
        if path not in summaries:
            summaries[path] = M.summary(path, year)
        s = summaries[path]
        con, how = C36.medsl_contest(c, s)
        allc = set(s["counties_all"].get(f"{st}|{date}", []))
        got, mags = set(), set()
        for v in con.values():
            got.update(v["counties"])
            mags.update(v["magnitudes"])
        note = ""
        if c.get("pieces_joined"):   # a joined contest: its counties are its pieces' together, its seat count the state's export's
            got = set()
            for p in c["pieces_joined"]:
                got.update(p["counties"])
                mags.add(str(p.get("seats")))
            note = f"; joined from {len(c['pieces_joined'])} pieces (MEDSL's magnitude {sorted(mags)})"
            race = ((c.get("result") or {}).get("state_total") or {}).get("race")
            ex = races.get(race) if races else None
            if ex is not None:
                mags = {"1"} if len([k for k in ex if nkey(k) != "WRITE IN"]) == 1 else mags
                note += f", the state's export lists {race!r} as a race of its own with {len([k for k in ex if nkey(k) != 'WRITE IN'])} name: one seat"
        whole = len(allc) > 1 and allc <= got
        seats = C36.seats_of(mags)
        dist = ((c.get("place") or {}).get("district") or "").strip().upper()
        mine = my_type(c["office"], r[3], whole, seats, dist, c.get("office_scope"))
        ok = mine == c.get("office_type")
        names = len([x for x in c["result"]["candidates"] if x.get("party") != "write-in"])
        print(f"    {r[0][:72]}: {r[3]} -> {r[4]}; mine {mine} ({'equal' if ok else 'DIFFERS'}); {'every county' if whole else f'{len(got & allc)} of {len(allc)} counties'}, magnitude {sorted(mags)}, district {dist!r}, {names} names{note}; p {C34.pval(c)!s:.50}")
        tal[f"mine == the record's: {ok}"] += 1
    print(f"  {dict(tal)}")
    # the rule over every state-scope board record of the changed files and the files of the T rows
    pool = dict(after)
    for f in sorted({r[1] for r in T}):
        for cid, c in C31.load_records(AFTER, [f]).items():
            pool.setdefault(cid, c)
            before.setdefault(cid, C31.load_records(BEFORE, [f]).get(cid) or c)
    recs = [c for c in pool.values() if c.get("office_scope") == "state" and c.get("level") == "local"
            and (c.get("office_type") in STATE_BOARD_TYPES + ("statewide officer",)) and (before.get(c["id"]) or {}).get("office_type", c.get("office_type")) in STATE_BOARD_TYPES
            and (c.get("result") or {}).get("source") == "medsl"]
    tal2 = collections.Counter()
    for c in sorted(recs, key=lambda c: c["id"]):
        st, year, date = st_of(c), c["year"], c["date"]
        paths = M.medsl_files(year, st)
        if not paths:
            tal2["file not fetched"] += 1
            continue
        path = paths[0]
        if path not in summaries:
            summaries[path] = M.summary(path, year)
        s = summaries[path]
        con, how = C36.medsl_contest(c, s)
        if not con:
            tal2["contest not found"] += 1
            continue
        allc = set(s["counties_all"].get(f"{st}|{date}", []))
        got, mags = set(), set()
        for v in con.values():
            got.update(v["counties"])
            mags.update(v["magnitudes"])
        whole = len(allc) > 1 and allc <= got
        seats = C36.seats_of(mags)
        bt = (before.get(c["id"]) or {}).get("office_type", c.get("office_type"))
        mine = my_type(c["office"], bt, whole, seats, ((c.get("place") or {}).get("district") or "").strip().upper(), "state")
        ok = mine == c.get("office_type")
        tal2[f"{bt} -> {c.get('office_type')}: mine {mine} ({'equal' if ok else 'DIFFERS'}); {'every county' if whole else 'not every county'}, seats {seats}"] += 1
        if not ok:
            print(f"    DIFFERS: {c['id'][:80]}: record {c.get('office_type')}, mine {mine} ({len(got & allc)} of {len(allc)} counties, magnitude {sorted(mags)})")
    print(f"  state-scope board or school-board records (by their type before) in the changed files and the T rows' files, MEDSL's: {len(recs)}:")
    for k, n in sorted(tal2.items(), key=lambda kv: -kv[1]):
        print(f"    {n:4d}  {k}")


# ---------------------------------------------------------------------------------------------- 37.8
def section_8():
    print("### 37.8 the 163 quote URLs: each quote on the page its URL answers; the three proposer quotes")
    by_url, by_key = sixth_fetched()
    listed = C34.show(AFTER, LISTED)
    items = []
    def walk(o, path):
        if isinstance(o, dict):
            for k in list(o):
                if k.endswith("quote_url"):
                    qk = k[:-4]   # quote_url -> quote; type_quote_url -> type_quote
                    items.append((path + "." + k, o.get(qk), o[k], o.get(qk + "_file")))
            for k, v in o.items():
                walk(v, path + "." + k)
        elif isinstance(o, list):
            for v in o:
                walk(v, path + "[]")
    walk(listed, "")
    urls = collections.Counter(u for _, _, u, _ in items)
    print(f"  quote_url fields in {LISTED} at {AFTER}: {len(items)} (D3: 163), by field {dict(collections.Counter(p.split('.')[-1] for p, _, _, _ in items))}; distinct URLs {len(urls)}; fetched (HTTP 200) {sum(1 for u in urls if u in by_url)} of {len(urls)}")
    codes = collections.Counter(v[0] for k, v in by_key.items() if k.startswith("quote:"))
    print(f"  HTTP codes of the 20 quote fetches: {dict(codes)}")
    cache = {}
    tal = collections.Counter()
    how = collections.Counter()
    perurl = collections.Counter()
    for path, quote, url, qfile in items:
        p = by_url.get(url)
        if not p:
            tal["page not fetched"] += 1
            continue
        if not quote:
            tal["no quote beside the URL"] += 1
            continue
        if p not in cache:
            cache[p] = C30.readings(p)
        got = C31.find_quote(quote, cache[p])
        field = path.split(".")[-1]
        if got:
            tal[f"{field}: found"] += 1
            how[got] += 1
            perurl[(url, True)] += 1
        else:
            tal[f"{field}: NOT FOUND"] += 1
            perurl[(url, False)] += 1
            print(f"    not found: {path[:60]} on {url[:70]}: {quote[:100]!r} (quote_file {qfile})")
    print(f"  {dict(sorted(tal.items()))}")
    print(f"  how found: {dict(how)}")
    print("  by URL (found, not found):")
    for u in sorted(urls):
        print(f"    {perurl[(u, True)]:3d} {perurl[(u, False)]:3d}  {u}")
    # the list's own URL
    same = sum(1 for p, q, u, f in items if u == ((listed.get("questions") or [{}])[0].get("list") or {}).get("url")) if False else None
    # the three proposer quotes
    book = C34.show(AFTER, THRESH)
    rules = book.get("rules") if isinstance(book, dict) else book
    n = 0
    for i, r in enumerate(rules or []):
        pq = (r or {}).get("proposer_quote")
        if not pq:
            continue
        n += 1
        url = (pq.get("url") if isinstance(pq, dict) else None) or r.get("url")   # the quote's own section where it names one
        p = by_url.get(url)
        words = pq.get("words") if isinstance(pq, dict) else pq
        if isinstance(words, str):
            words = [words]
        cite = str((pq.get("citation") if isinstance(pq, dict) else None) or r.get("cite") or r.get("citation") or "")
        if not p:
            print(f"    rules[{i}] {r.get('state')} {cite[:40]}: page {url} not fetched")
            continue
        if p not in cache:
            cache[p] = C30.readings(p)
        for w in words or []:
            got = C31.find_quote(w, cache[p])
            print(f"    rules[{i}] {r.get('state')} {cite[:50]!r}: proposer_quote {'found (' + got + ')' if got else 'NOT FOUND'} on {url[:60]}: {w[:80]!r}")
    print(f"  rules with a proposer_quote: {n} (D3: rules[59], [95], [96], [97])")


# ---------------------------------------------------------------------------------------------- 37.9
def section_9(before, after, mv):
    print("### 37.9 the 49 R rows: each reason's count of like races against my own pool counts")
    R = [r for r in mv["records"] if "R" in r[8]]
    print(f"  rows with R: {len(R)} (D3: 49: 41 R alone, 7 T and R, 1 R and Q)")
    pa_m, pa_nc = C35.pools_at(AFTER)
    pb_m, pb_nc = C35.pools_at(BEFORE)
    tal = collections.Counter()
    for r in sorted(R, key=lambda r: r[0]):
        cid = r[0]
        a, b = after[cid], before[cid]
        ma = REASON_N.search((a.get("p") or {}).get("not_computed") or "")
        mb = REASON_N.search((b.get("p") or {}).get("not_computed") or "")
        year = a["year"]
        if not ma or not mb:
            tal["not of the 'fewer than 100 like races' shape"] += 1
            print(f"    {cid[:70]}: {(b.get('p') or {}).get('not_computed', '')[:60]!r} -> {(a.get('p') or {}).get('not_computed', '')[:60]!r}")
            continue
        na, ca = int(ma.group(1)), ma.group(2)
        nb, cb = int(mb.group(1)), mb.group(2)
        mine_a = C35.count_like(pa_m, ca, year)
        mine_b = C35.count_like(pb_m, cb, year)
        tal[f"{year} '{ca}': after {na} (mine {mine_a}, {'equal' if na == mine_a else 'DIFFERS'}); before '{cb}' {nb} (mine {mine_b}, {'equal' if nb == mine_b else 'DIFFERS'})"] += 1
    for k, n in sorted(tal.items(), key=lambda kv: -kv[1]):
        print(f"    {n:4d}  {k}")


def main():
    print(f"### c37: D3's #90 ({AFTER}) against {BEFORE}: statewide pieces, holds, North Dakota's judgeships, over-ballot holds, one-seat boards, quote URLs; HEAD {L.git_head()}")
    before, after, mv = section_1()
    summaries, raws = section_2(after)
    section_3(after)
    section_4(after, summaries, raws)
    section_5(after)
    section_6()
    section_7(before, after, mv, summaries)
    section_8()
    section_9(before, after, mv)
    print("### c37 done")


if __name__ == "__main__":
    main()
