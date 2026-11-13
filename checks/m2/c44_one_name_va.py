#!/usr/bin/env python3
"""c44: D3's #101 (4831b16; the eighth pass's section 16, its end moved from d680bd4 to 4831b16 by the orchestrator's
word of 2026-11-13 00:54 UTC): held one-name records not computed at every level (23 local p 0 lost, 61 legislative
reasons), and Virginia's 2023 local contests and questions (1,448 records, 774 p 0) from the Department's export file
read before it refused us.

The orchestrator (00:54): "For Virginia, check three things: the over-ballot gate in each locality, the name-keyed
write-in reading (the file's options keyed by name read as write-ins, inferred and confirmed by the page on two
contests), and that every p 0 has one ballot name per seat."

What this check can and cannot read [stated]: the Department's export file (export-2023-Nov-Gen.json) is in D3's own
cache, not in the repository, and Virginia's hosts are not requested (the orchestrator, 2026-11-07 18:30); so the
three things are read from the records at 4831b16 and D3's data/local/check-va-local.json alone: the gate's own
arithmetic (the recorded ratio against the record's votes and seats, and against the other contests of the same
locality in the records), the write-in reading as the records carry it, and p 0 against the records' names and seats.
A reading of the file whole waits for a copy of it (asked of the orchestrator, 01:0x UTC).

Sections:
  44.1  the two moves files (moves-held-one-name.json, moves-va-2023-local.json) against my own diff of every record,
        d680bd4 -> 4831b16: every changed record in one of the files with the same code, every row in my diff
  44.2  Virginia 2023: every p 0 has one ballot name for each seat, and the write-in test (10% of the last winner's
        votes) read from the records; the not-computed reasons by my own classification of each record
  44.3  Virginia 2023: the name-keyed write-ins as the records carry them (65 records), beside the write-in line;
        the two the page confirmed (Brodnax's and Scottsville's councils), held by the page
  44.4  Virginia 2023: the over-ballot test within the locality: the recorded ratio against the record's votes for each
        seat; the figure it implies against the other contests of the locality in the records; the verdict by the
        1.10 line; the three held and the 28 listed; the comparators of the three held (unopposed or not, for the
        orchestrator's ruling of 00:54 on an unopposed comparator)
  44.5  the held one-name records: the 23 local records' p before and reason after; the 61 legislative reasons

The rules applied are copied from the records' own words and D3's docstrings (pipeline/local_va.py, pipeline/local.py
HELD_ONE_NAME), never imported. Run:  python3 -I checks/m2/c44_one_name_va.py [1 2 3 4 5]
"""
import collections
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402
import c40_pr_checks as C40  # noqa: E402
import c43_district_checks as C43  # noqa: E402

BEFORE, AFTER = "d680bd4", "4831b16"
OVER_LINE = 1.10        # pipeline/local_va.py OVER_LINE, copied
WRITE_IN_SHARE = 0.10   # the records' words: "whether write-ins drew 10% of the last winner's votes"
HELD_WORDS = "cannot be read on held counts"
at, records_at, h1 = C43.at, C43.records_at, C43.h1


def pstate(r):
    p = r.get("p") or {}
    if p.get("value") == 0:
        return "p 0"
    if p.get("value") is not None:
        return "p > 0"
    return "not computed: " + (p.get("not_computed") or p.get("reason") or "?")


def reason_kind(r):
    s = pstate(r)
    if s in ("p 0", "p > 0"):
        return s
    for k, w in (("held by the gate", "held by the gate"), ("special", "a special election"),
                 ("write-in in the pair", "a write-in line is in the pair"),
                 ("strong write-ins (or fewer names than seats)", "but write-ins received"),
                 ("too few like races", "fewer than 100 like races"), ("held one-name", HELD_WORDS)):
        if w in s:
            return k
    return "other: " + s[14:60]


# ------------------------------------------------------------------------------------------ 44.1 the moves files

def section_1():
    h1(f"44.1 moves-held-one-name.json and moves-va-2023-local.json against my own diff of every record, {BEFORE} -> {AFTER}")
    import subprocess
    files_mv = {}
    for name in ("moves-held-one-name.json", "moves-va-2023-local.json"):
        mv = L.load_json(at(AFTER, f"data/local/{name}"))
        files_mv[name] = mv
        print(f"  {name}: {len(mv['records'])} rows, against {mv.get('against')}; summary {json.dumps(mv['summary'])}")
    rows = {}
    for name, mv in files_mv.items():
        for r in mv["records"]:
            rows.setdefault(r[0], []).append((name, r))
    files = subprocess.run(["git", "diff", "--name-only", BEFORE, AFTER, "--", "data/"], capture_output=True, text=True,
                           cwd=L.ROOT).stdout.split()
    data_files = [f for f in files if re.match(r"^data/(local|primary|measure|state-lower|state-upper)/\d{4}/[A-Z]{2}\.json$", f)
                  or re.match(r"^data/(governor|house|senate|president)/\d{4}\.json$", f)]
    print(f"  data files changed: {len(files)}; record files: {len(data_files)} {dict(collections.Counter(f.split('/')[1] for f in data_files))}; "
          f"other: {[f for f in files if f not in data_files]}")
    mine = collections.Counter()
    agree, dis, seen, worst, stamps = 0, collections.Counter(), set(), [], 0
    pdiff = 0
    for f in data_files:
        lv = f.split("/")[1]
        b, a = records_at(BEFORE, f), records_at(AFTER, f)
        for i in sorted(set(b) | set(a)):
            code = C40.my_code(b.get(i), a.get(i))
            if not code:
                continue
            d = C40.what_differs(b.get(i) or {}, a.get(i) or {})
            if tuple(d) == ("p.commit",):
                stamps += 1
                continue
            c = code[0]
            if c in ("B", "Q", "O", "R") and any((b.get(i) or {}).get(k) != (a.get(i) or {}).get(k) for k in ("type", "office_type")):
                c = "T"
            pb, pa = C40.pval(b.get(i) or {}), C40.pval(a.get(i) or {})
            mine[(lv, c)] += 1
            seen.add(i)
            hits = rows.get(i)
            if not hits:
                worst.append((i, c, "not in the moves files", d[:6]))
                continue
            theirs = set()
            for _, row in hits:
                theirs |= set(row[8])
            ok = c in theirs or (c in ("Q", "O", "B", "R") and theirs & {"Q", "O", "R"})
            if ok:
                agree += 1
            else:
                dis[(lv, c, tuple(sorted(theirs)))] += 1
                worst.append((i, c, tuple(sorted(theirs)), d[:6]))
            for _, row in hits:
                if isinstance(row[5], str) or isinstance(row[6], str):
                    continue
                if (row[6] is None) != (pa is None) or (pa is not None and abs(row[6] - pa) > 1e-9 * max(abs(pa), 1e-300)):
                    pdiff += 1
                    if pdiff <= 5:
                        print(f"    p after differs from the record: {i} row {row[6]} record {pa}")
    not_mine = [i for i in rows if i not in seen]
    print("  my diff, by level and code: " + "; ".join(f"{lv} {k} {v}" for (lv, k), v in sorted(mine.items())))
    print(f"  rows whose code I share: {agree} of {len(seen)} ids in my diff; codes differing: {sum(dis.values())}; "
          f"ids in my diff but in neither file: {len([w for w in worst if w[2] == 'not in the moves files'])}; "
          f"ids in the files but not in my diff: {len(not_mine)} {not_mine[:5]}; p after other than the record's: {pdiff}; stamps: {stamps}")
    for (lv, c, theirs), v in sorted(dis.items(), key=lambda kv: -kv[1])[:10]:
        ex = [w for w in worst if w[1] == c and w[2] == theirs][:2]
        print(f"    mine {c} theirs {theirs} {lv}: {v}; e.g. " + "; ".join(f"{e[0]} differs in {e[3]}" for e in ex))
    for w in [w for w in worst if w[2] == "not in the moves files"][:8]:
        print(f"    in neither file: {w[0]} mine {w[1]} differs in {w[3]}")
    # the L rows: p 0 before, not computed after with the held one-name words
    mv = files_mv["moves-held-one-name.json"]
    L_rows = [r for r in mv["records"] if "L" in r[8]]
    print(f"  the one-name file's L rows: {len(L_rows)} {dict(collections.Counter(r[1].split('/')[1] + ' ' + r[1].split('/')[2] for r in L_rows))}; "
          f"p before 0 in {sum(1 for r in L_rows if r[5] == 0)}; after None in {sum(1 for r in L_rows if r[6] is None)}; "
          f"reason carrying '{HELD_WORDS}': {sum(1 for r in L_rows if isinstance(r[6], str) and HELD_WORDS in r[6] or HELD_WORDS in json.dumps(r))}")
    R_rows = [r for r in mv["records"] if "R" in r[8]]
    print(f"  its R rows: {len(R_rows)} {dict(collections.Counter(r[1].split('/')[1] for r in R_rows))}")
    mv2 = files_mv["moves-va-2023-local.json"]
    print(f"  the Virginia file's rows by code: {dict(collections.Counter(c for r in mv2['records'] for c in r[8]))}; "
          f"files: {dict(collections.Counter(r[1] for r in mv2['records']))}")


# ------------------------------------------------------------------------------------------ 44.2 p 0: one name a seat

def va_records():
    return [r for r in records_at(AFTER, "data/local/2023/VA.json").values()]


def names_and_writeins(r):
    cands = r["result"]["candidates"]
    ballot = [c for c in cands if c.get("party") != "write-in"]
    wi_line = sum(c["votes"] for c in cands if c.get("party") == "write-in" and c["name"].strip().upper() == "WRITE-IN")
    wi_named = [(c["name"], c["votes"]) for c in cands if c.get("party") == "write-in" and c["name"].strip().upper() != "WRITE-IN"]
    return ballot, wi_line, wi_named


def my_class(r):
    """My own reading of the record: p 0 where one ballot name for each seat, not special, not held, and the
    write-ins (the line and the named, together) under 10% of the last winner's votes; else the reason."""
    seats = r.get("seats", 1)
    ballot, wi_line, wi_named = names_and_writeins(r)
    wi = wi_line + sum(v for _, v in wi_named)
    gate_held = (r.get("gate") or {}).get("over_ballot") == "held" or (r.get("gate") or {}).get("page_equal") is False \
        or (r.get("gate") or {}).get("parts_add_up") is False or (r.get("gate") or {}).get("all_reporting") is False
    if gate_held:
        return "held by the gate"
    if r.get("election") == "special" or "special" in json.dumps(r.get("notes", [])).lower() and False:
        return "special"
    votes = sorted((c["votes"] for c in ballot), reverse=True)
    last = votes[seats - 1] if len(votes) >= seats else None
    if len(ballot) < seats:
        return "fewer names than seats"
    if len(ballot) == seats:
        if last and wi >= WRITE_IN_SHARE * last:
            return "one name a seat, strong write-ins"
        return "one name a seat, p 0"
    # contested
    if last is not None and wi > (votes[seats] if len(votes) > seats else 0) and wi >= votes[seats]:
        pass
    return "contested"


def section_2():
    h1("44.2 Virginia 2023: every p 0 has one ballot name for each seat; the write-in test and the reasons, from the records")
    rs = va_records()
    print(f"  records: {len(rs)}; by the record's p: {dict(collections.Counter(reason_kind(r) for r in rs))}")
    tab = collections.Counter()
    bad = []
    for r in rs:
        k = reason_kind(r)
        m = my_class(r)
        tab[(k, m)] += 1
        if k == "p 0" and m != "one name a seat, p 0":
            bad.append((r["id"], m, r.get("seats", 1), [(c["name"], c["votes"], c.get("party")) for c in r["result"]["candidates"]][:5]))
        if m == "one name a seat, p 0" and k != "p 0" and k not in ("special",):
            bad.append((r["id"], k[:50], r.get("seats", 1), [(c["name"], c["votes"], c.get("party")) for c in r["result"]["candidates"]][:5]))
    print("  the record's reason x my own class:")
    for (k, m), v in sorted(tab.items(), key=lambda kv: -kv[1]):
        print(f"    {v:5}  record: {k[:60]:60}  mine: {m}")
    print(f"  p 0 records not one name a seat by my reading, or one name a seat (not special) without p 0: {len(bad)}")
    for b in bad[:12]:
        print(f"    {b}")
    # every p 0: seats, ballot names equal
    p0 = [r for r in rs if pstate(r) == "p 0"]
    eq = sum(1 for r in p0 if len(names_and_writeins(r)[0]) == r.get("seats", 1))
    print(f"  p 0 records: {len(p0)}; ballot names equal to seats in {eq}; the specials among them: {sum(1 for r in p0 if r.get('election') == 'special')}")
    # the strong write-in records: fewer names than seats vs one name a seat
    sw = [r for r in rs if reason_kind(r) == "strong write-ins (or fewer names than seats)"]
    print(f"  strong write-in (or fewer names) records: {len(sw)}; fewer names than seats: {sum(1 for r in sw if len(names_and_writeins(r)[0]) < r.get('seats', 1))}; "
          f"one name a seat with write-ins at 10% or more of the last winner: {sum(1 for r in sw if my_class(r) == 'one name a seat, strong write-ins')} (D3: 103, 60 with fewer names)")
    # the write-in share where p 0: the highest
    shares = []
    for r in p0:
        ballot, wl, wn = names_and_writeins(r)
        votes = sorted((c["votes"] for c in ballot), reverse=True)
        last = votes[r.get("seats", 1) - 1]
        shares.append(((wl + sum(v for _, v in wn)) / last if last else None, r["id"]))
    shares = [s for s in shares if s[0] is not None]
    print(f"  the write-ins' share of the last winner where p 0: highest {sorted(shares, reverse=True)[:3]}; all under 10%: {all(s < WRITE_IN_SHARE for s, _ in shares)}")
    # a p 0 record whose winner is not the ballot name (a named write-in ahead)?
    ahead = [r["id"] for r in rs if names_and_writeins(r)[2] and names_and_writeins(r)[0]
             and max(v for _, v in names_and_writeins(r)[2]) > min(c["votes"] for c in names_and_writeins(r)[0])]
    print(f"  records where a named write-in outpolls a ballot name: {len(ahead)} (a reading: the page would say whether the name was on the ballot)")
    byid = {r["id"]: r for r in rs}
    for i in ahead[:8]:
        r = byid[i]
        print(f"    {i}: seats {r.get('seats', 1)}; {[(c['name'], c['votes'], c.get('party')) for c in r['result']['candidates']]}; {pstate(r)[:90]}")


# ------------------------------------------------------------------------------------------ 44.3 the named write-ins

def section_3():
    h1("44.3 Virginia 2023: the name-keyed write-ins as the records carry them")
    rs = va_records()
    named = [r for r in rs if names_and_writeins(r)[2]]
    print(f"  records with a write-in candidate counted by name: {len(named)} (D3: 65); with the write-in line beside it: "
          f"{sum(1 for r in named if any(c.get('party') == 'write-in' and c['name'].strip().upper() == 'WRITE-IN' for c in r['result']['candidates']))}")
    print(f"  by the record's reason: {dict(collections.Counter(reason_kind(r) for r in named))}")
    more = [(r['id'], names_and_writeins(r)[2], names_and_writeins(r)[1]) for r in named if sum(v for _, v in names_and_writeins(r)[2]) > names_and_writeins(r)[1]]
    print(f"  the named write-ins' votes over the line's: {len(more)} records, e.g. {more[:4]}")
    won = [r["id"] for r in named if any(c.get("won") and c.get("party") == "write-in" for c in r["result"]["candidates"])]
    print(f"  a named write-in marked won: {len(won)} {won[:5]}")
    for key in ("Brodnax", "Scottsville"):
        for r in rs:
            if key in r["id"] and "COUNCIL" in r["id"]:
                g = r.get("gate") or {}
                print(f"  {r['id']}: candidates {[(c['name'], c['votes'], c.get('party')) for c in r['result']['candidates']]}; page_equal {g.get('page_equal')}; "
                      f"parts_add_up {g.get('parts_add_up')}; {pstate(r)[:160]}")
    # the legislature: none
    leg = 0
    for lv in ("state-lower", "state-upper"):
        for r in records_at(AFTER, f"data/{lv}/2023/VA.json").values():
            if any(c.get("party") == "write-in" and c["name"].strip().upper() != "WRITE-IN" for c in r["result"]["candidates"]):
                leg += 1
    print(f"  named write-ins in the 2023 legislature's records: {leg} (D3: none)")


# ------------------------------------------------------------------------------------------ 44.4 the over-ballot test

def section_4():
    h1("44.4 Virginia 2023: the over-ballot test within the locality, from the records and check-va-local.json")
    rs = va_records()
    qs = list(records_at(AFTER, "data/measure/2023/VA.json").values())
    chk = L.load_json(at(AFTER, "data/local/check-va-local.json"))["years"]["2023"]
    print(f"  the check's tallies: {json.dumps(chk['tallies'])}")
    # the figures I can see in each locality: one-seat contests of the whole locality (no district) and questions
    by_loc = collections.defaultdict(list)
    for r in rs:
        if len(r["place"]["counties"]) == 1 and not r["place"].get("district") and r.get("seats", 1) == 1:
            by_loc[r["place"]["counties"][0]].append((r["result"]["total_votes"], r["id"]))
    for q in qs:
        if len(q["place"]["counties"]) == 1:
            by_loc[q["place"]["counties"][0]].append((q["result"]["total_votes"], q["id"]))
    verdict_tab = collections.Counter()
    arith_ok = arith_bad = 0
    implied = collections.Counter()
    worst_lines = []
    for r in rs + qs:
        g = r.get("gate") or {}
        v = g.get("over_ballot")
        ratio = g.get("over_ballot_ratio")
        verdict_tab[v] += 1
        if ratio is None:
            continue
        my_v = "held" if ratio > OVER_LINE else "listed" if ratio > 1 else "passes"
        if my_v != v:
            arith_bad += 1
            worst_lines.append(("verdict", r["id"], ratio, v))
        else:
            arith_ok += 1
        if len(r["place"]["counties"]) == 1:
            seats = r.get("seats", 1) if "candidates" in r["result"] and not r.get("question") else 1
            vps = r["result"]["total_votes"] / (seats or 1)
            top = vps / ratio
            loc = r["place"]["counties"][0]
            others = [(t, i) for t, i in by_loc[loc] if i != r["id"]]
            mx = max((t for t, _ in others), default=None)
            hit = [i for t, i in others if abs(t - top) <= max(1, 0.0006 * top)]
            if hit:
                implied["a local contest in the records"] += 1
            elif mx is not None and top > mx * 1.0006:
                implied["beyond every local one-seat contest (a chamber's lines summed)"] += 1
            elif mx is not None and top < mx * 0.9994:
                implied["UNDER a local one-seat contest of the locality"] += 1
                big = max(others)
                worst_lines.append(("top under a local contest", r["id"], round(top), big[0], big[1].split("-VA-")[1][:40], round(ratio, 4),
                                    f"under by {100 * (1 - top / big[0]):.2f}%"))
            else:
                implied["no other figure in the records"] += 1
    print(f"  verdicts on the records: {dict(verdict_tab)}; the ratio's verdict by the 1.10 line equal to the record's: {arith_ok}, differing: {arith_bad}")
    print(f"  the figure each one-locality ratio implies (votes a seat / ratio), against the locality's other one-seat whole-locality contests and questions in the records: {dict(implied)}")
    for w in worst_lines[:8]:
        print(f"    {w}")
    print(f"  the check's held: {len(chk['held'])}; listed: {len(chk['listed'])}; highest ratios: "
          + "; ".join(f"{h['title']} {h['ratio']}" for h in chk["over_ballot_highest"][:6]))
    # the records held by the gate and listed: as the check
    held = [r for r in rs if "held by the gate" in pstate(r)]
    listed = [r for r in rs + qs if "between 1.0 and" in json.dumps(r.get("notes", []))]
    print(f"  records held by the gate: {len(held)} {[r['id'] for r in held]}; records carrying the listed note: {len(listed)} (the check: 28)")
    # the comparators of the three held by (d): unopposed?
    byid = {r["id"]: r for r in rs}
    for h in chk["held"]:
        if "times the" not in (h["why"] or ""):
            continue
        m = re.search(r"times the ([\d,]+) of (.+?), the highest", h["why"])
        comp = m.group(2) if m else None
        cands = None
        for r in rs:
            if comp and r["office"].upper() == comp.split(" (")[0].upper() and any(("51" + l) in r["place"]["counties"] for l in h["localities"]):
                cands = [(c["name"], c["votes"], c.get("party")) for c in r["result"]["candidates"]]
                break
        print(f"  held: {h['title']} | {h['why'][:90]}... | the comparator's record: {cands}")
    for l in chk["listed"][:28]:
        pass
    print(f"  listed (the 28): " + "; ".join(f"{l['title']} {l['ratio']} vs {l['top_name'][:40]}" for l in chk["listed"][:10]) + " ...")


# ------------------------------------------------------------------------------------------ 44.5 the held one-name

def section_5():
    h1(f"44.5 The held one-name records: p before and the reason after, {BEFORE} -> {AFTER}")
    mv = L.load_json(at(AFTER, "data/local/moves-held-one-name.json"))
    ok = bad = 0
    tally = collections.Counter()
    for r in mv["records"]:
        f, i = r[1], r[0]
        b, a = records_at(BEFORE, f).get(i), records_at(AFTER, f).get(i)
        pb, pa = C40.pval(b or {}), C40.pval(a or {})
        ra = (a.get("p") or {}).get("not_computed") or ""
        rb = (b.get("p") or {}).get("not_computed") or (b.get("p") or {}).get("reason") or ""
        lv = f.split("/")[1]
        if "L" in r[8]:
            good = pb == 0 and pa is None and HELD_WORDS in ra and "one name on the ballot" in ra
            tally[(lv, "L", good)] += 1
        else:
            good = pb is None and pa is None and HELD_WORDS in ra and HELD_WORDS not in rb and ra.startswith(rb.split(" (the orchestrator")[0][:40])
            tally[(lv, "R", good)] += 1
        ok += good
        bad += not good
        if not good and bad <= 4:
            print(f"    not as the file says: {i} p {pb} -> {pa}; before: {rb[:100]}; after: {ra[:160]}")
    print(f"  rows as the file says (L: p 0 before, not computed after with the one-name words; R: not computed before and after, the words added): {ok}; not: {bad}")
    print(f"  by level and code: {dict(sorted(tally.items()))}")
    # any other record at AFTER carrying the words, not in the file?
    carry = []
    for lv in ("local", "state-lower", "state-upper", "measure"):
        for f in sorted(os.listdir(at(AFTER, f"data/{lv}"))):
            if not os.path.isdir(at(AFTER, f"data/{lv}/{f}")):
                continue
            for st in sorted(os.listdir(at(AFTER, f"data/{lv}/{f}"))):
                if not st.endswith(".json"):
                    continue
                for i, r in records_at(AFTER, f"data/{lv}/{f}/{st}").items():
                    if HELD_WORDS in ((r.get("p") or {}).get("not_computed") or ""):
                        carry.append(i)
    ids = {r[0] for r in mv["records"]}
    print(f"  records at {AFTER} carrying the words: {len(carry)}; in the file: {len([i for i in carry if i in ids])}; not: {[i for i in carry if i not in ids][:6]}")


def main():
    which = [int(a) for a in sys.argv[1:]] or [1, 2, 3, 4, 5]
    print(f"C44 #101 (held one-name records, Virginia 2023 local); records at {BEFORE} and {AFTER} under {L.CACHE}/eighth/wt/")
    for n in which:
        globals()[f"section_{n}"]()
    print("\n### done c44")


if __name__ == "__main__":
    main()
