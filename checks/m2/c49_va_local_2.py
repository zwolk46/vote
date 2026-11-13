"""c49: the eighth pass's section 20: D3's #111 (main 11c852d; data/local/REPORT.md section 36) against bddef1ae (main after
my #110, whose data files are b35fede's): the unopposed comparator, Virginia's school boards nonpartisan by the Code of
Virginia, Virginia's 2025 local contests, Indiana 2018's Senate from the state's certified archive.

The orchestrator, 2026-11-13 09:21 UTC: "D3's #111 is merged as 11c852d (REPORT §36, moves-36.json). Check it in section 20,
with its end at 11c852d. It covers: the unopposed-comparator rule (VA 2023 held 5 to 2, listed 28 to 31); Virginia school
boards as nonpartisan under § 22.1-57.3 E (158 VA 2023 p, and 756 school-board p of 2024 moving ×0.900 to ×1.042 as the pools
grow); VA 2025 local (566 contests: 283 p 0, 127 by like races, 62 councils on VA 2023's "party not given" pool); Indiana
2018's certified Senate file (SD29, 31, 47 settled; 47's p back), with route (a)'s refit; the LA 2023 note. My compare: 569
gained, none lost, 9,713 moved, none over 2x."

Sources read here, each by my own reading (nothing from pipeline/ imported; a rule of the build that must be applied is
copied here and says so):
  - the records at the two commits (worktrees under ~/.cache/vote-m2/eighth/wt/);
  - Virginia's Department of Elections' 2025 Media Export and the rendered results page, D3's copies of what it read on
    2026-11-07 (before the Department refused us; nothing is requested from Virginia's hosts), placed in the project's shared
    folder /mnt/project-files/d3/va-2025/ and copied to ~/.cache/vote-m2/eighth/src/va-2025/, their sha256 checked against
    D3's SHA256SUMS on each run; 2023's as c45 holds them;
  - the three Code of Virginia pages at law.lis.virginia.gov, fetched once more by fetch_eighth_pass.sh va_code (one request
    each, six seconds apart; 2026-11-13 09:27 UTC);
  - Indiana's 2018 results archive (settings, the office list, the State Senator file), fetched once more by
    fetch_eighth_pass.sh in_2018 (six seconds apart; 09:27 UTC); the State Representative file is not read (D3 did not read
    it either: one more request, for the orchestrator);
  - MEDSL's raw precinct files of 2016, 2018 and 2022 (c48's cached pass, and a pass of my own for the names on each
    statewide contest's ballot, cached the same way);
  - Klarner's contest file and the records' rows for route (a) (c15/c40's fit, copied rules).
Sections:
  49.1  moves-36.json against my own diff of every record, bddef1ae -> 11c852dc: the codes, the counts (569 gained = new
        records with p + new p; 9,713 moved = local P + legislature P), the bands, none over 2x
  49.2  the unopposed comparator (00:55 (b), D3's rules copied): Virginia 2023 and 2025 from the export, every record's
        over-ballot verdict and ratio against its gate (held 5 -> 2, listed 28 -> 31; Halifax, Cumberland, Norton); MEDSL's
        over-ballot rows (no unopposed top contest); the over-seats figures (no district's ballots rest on unopposed
        contests alone: the ten one-name statewide contests of 2018 from the raw files)
  49.3  the Code of Virginia: the three pages read again (sha256 against D3's; the words quoted present); the school
        boards' class (388 of 2023, 179 of 2025, the chairmen), the 158 new p, the 364 reasons naming section 24.2-613 B
  49.4  the local like-race pools from the records (D3's local_structure copied): the class of every local record against
        the record's; my pool's (N, k, h, q) and p against every like-race p of 2023, 2024 and 2025 at both commits; the 756
        school boards of 2024 and the 62 councils of 2025
  49.5  Virginia 2025 from the Department's export: the 566 contests, the gate (the Governor equal to D2's; the page's 50
        contests; the shared contests' locality lines; all reporting; the over-ballot test), every record against the file,
        the write-ins by name, the p states
  49.6  Indiana 2018's Senate from the state's archive, read again: "Certified":"T", every district's count against the
        records', Senate 29, 31 and 47 (the suffix rule copied), the records' state_agrees blocks
  49.7  route (a) refitted at both commits (c40's rows and fits): Senate 47 rejoins; every partisan p's move against the
        file's; Indiana 2020's Senate lean from Indiana 2018's contested Senate races
  49.8  the reasons, notes and gates changed: Louisiana 2023's 17, Virginia 2023's 364, the 207 school boards of 2024, the
        gates; D2's files untouched
[measured] throughout unless marked; D3's words [stated].
Run from the repository root: python3 -I checks/m2/c49_va_local_2.py [1 2 3 4 5 6 7 8]
"""
import collections
import hashlib
import html as _html
import json
import math
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402
import m2medsl as M  # noqa: E402
import m2d3 as D  # noqa: E402
import c15_d3_refit as C15  # noqa: E402
import c40_pr_checks as C40  # noqa: E402
import c41_governor_refit as C41  # noqa: E402
import c42_held_totals as C42  # noqa: E402
import c43_district_checks as C43  # noqa: E402
import c44_one_name_va as C44  # noqa: E402
import c45_va_gate as C45  # noqa: E402
import c46_district_checks_2 as C46  # noqa: E402
import c48_district_checks_3 as C48  # noqa: E402

BEFORE, AFTER = "bddef1ae", "11c852dc"
SRC = os.path.join(L.CACHE, "eighth", "src")
DERIVED = os.path.join(L.CACHE, "eighth", "derived")
VA = {2023: {"dir": os.path.join(SRC, "va-2023"), "export": "export-2023-Nov-Gen.json", "page": "2023-Nov-Gen-page-rendered.html"},
      2025: {"dir": os.path.join(SRC, "va-2025"), "export": "export-2025-November-General.json", "page": "2025-November-General-page-rendered.html"}}
OVER_LINE = 1.10              # D3's OVER_LINE / OVER_TOP, copied
OVER_LINE_UNOPPOSED = 1.50    # D3's OVER_LINE_UNOPPOSED / OVER_UNOPPOSED / OVER_SEATS_UNOPPOSED, copied (the orchestrator, 00:55 (b))
BALLOT_ID = re.compile(r"cs\d+")   # D3's, copied
LEG_TITLE = re.compile(r"Member, (Senate of Virginia|House of Delegates) \(")   # D3's, copied
POSS = {"Senate of Virginia": "the Senate of Virginia's", "House of Delegates": "the House of Delegates'"}   # D3's POSS, copied
SCHOOL_BOARD = re.compile(r"\bSCHOOL BOARD\b", re.I)   # D3's CODE_NONPARTISAN['school board']['match'], copied
CHAIR_SCHOOL = re.compile(r"\bCHAIRMAN\b.*\bSCHOOL BOARD\b", re.I)   # D3's, copied
PARTY_NOT_GIVEN = "party not given in the source"   # D3's, copied
CODE = {   # D3's CODE_613, CODE_NONPARTISAN and CODE_READ_NOT_BAR, copied: the page, the words quoted
    "24.2-613 B": ("section24.2-613.html", "For elections for federal, statewide, and General Assembly offices only, each candidate who has been nominated by a political party or in a primary election shall be identified by the name of his political party."),
    "22.1-57.3 E": ("title22.1-chapter5-article7.html", "In order to have their names placed on the ballot, all candidates shall be nominated only by petition as provided by general law pursuant to § 24.2-506."),
    "22.1-57.3:3 B": ("title22.1-chapter5-article7.html", "The member of the school board who is elected at large at the initial or any subsequent election shall be the chairman of the school board during his term of office"),
    "10.1-523 A": ("title10.1-chapter5-article3.html", "to nominate candidates for elected directors of such districts")}
D3_SHA = {"section24.2-613.html": None, "title22.1-chapter5-article7.html": "4d694a3950db307a88bf71efdb6602b37ec98d825c5c77ac434dd5ff15dd70d0",
          "title10.1-chapter5-article3.html": None}   # the article 7 page's sha256 as the records quote it [stated]; the others from the records' texts
IN2018 = os.path.join(SRC, "in_enr_2018")
IN2018_SHA = "e02aab5b12cd275f5ec44f430661574d9f1463b686056a962e8f79d9167f2271"   # the records' state_agrees.sha256 [stated]
h1 = C48.h1


def at(commit, rel):
    return os.path.join(C41.worktree(commit), rel)


def records_at(commit, f):
    return C42.records_at(C41.worktree(commit), f)


def pval(c):
    return C40.pval(c)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def pstate(r):
    return C44.pstate(r)


def reason_kind(r):
    return C44.reason_kind(r)


# ------------------------------------------------------------------------------------------ 49.1 the moves file

def my_diff():
    """Every record of D3's files that differs between the commits (p.commit alone aside): {id: (code, lv, yr, before, after, differs)}."""
    files = subprocess.run(["git", "diff", "--name-only", BEFORE, AFTER, "--", "data/"], capture_output=True, text=True, cwd=L.ROOT).stdout.split()
    data_files = [f for f in files if re.match(r"^data/(local|primary|measure|state-lower|state-upper)/\d{4}/[A-Z]{2}\.json$", f)]
    d2_files = [f for f in files if re.match(r"^data/(governor|house|senate|president)/\d{4}\.json$", f)]
    other = [f for f in files if f not in data_files and f not in d2_files]
    out, stamps = {}, 0
    for f in data_files:
        lv, yr = f.split("/")[1], f.split("/")[2]
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
            out[i] = (c, lv, yr, b.get(i), a.get(i), d)
    return out, data_files, d2_files, other, stamps


def section_1():
    h1(f"49.1 moves-36.json against my own diff of every D3 record, {BEFORE} -> {AFTER}")
    mv = L.load_json(at(AFTER, "data/local/moves-36.json"))
    rows = {}
    for r in mv["records"]:
        rows.setdefault(r[0], []).append(r)
    print(f"  the file: {len(mv['records']):,} rows, {len(rows):,} ids, against {mv.get('against')} (the code alone, its data main's at b35fede, which equal {BEFORE}'s D3 files; my diff is main to main)")
    print(f"  its summary: {json.dumps(mv['summary'])}")
    diff, data_files, d2_files, other, stamps = my_diff()
    print(f"  data files changed: {len(data_files) + len(d2_files) + len(other)}; D3's record files: {len(data_files)} {dict(collections.Counter(f.split('/')[1] for f in data_files))}; D2's: {len(d2_files)}; other: {other}")
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
        ok = c in theirs or (c in ("Q", "O", "B", "R") and theirs & {"Q", "O", "R", "B"})
        if ok:
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
    # the orchestrator's counts: gained = a p after and none before (a new record with p, or a new p); lost; moved = P
    new_with_p = [(i, lv, yr) for i, (c, lv, yr, b, a, d) in diff.items() if c == "A" and pval(a) is not None]
    new_p = [(i, lv, yr) for i, (c, lv, yr, b, a, d) in diff.items() if c == "N"]
    lost = [(i, lv, yr) for i, (c, lv, yr, b, a, d) in diff.items() if c == "L" or (c == "G" and pval(b) is not None)]
    moved = [(pval(a) / pval(b), i, lv, yr) for i, (c, lv, yr, b, a, d) in diff.items() if c == "P" and pval(b)]
    print(f"  gained (a p after, none before): {len(new_with_p) + len(new_p)} = {len(new_with_p)} new records with p {dict(collections.Counter((lv, yr) for _, lv, yr in new_with_p))} "
          f"(p 0: {sum(1 for i, lv, yr in new_with_p if pval(diff[i][4]) == 0)}, p > 0: {sum(1 for i, lv, yr in new_with_p if pval(diff[i][4]))}) + {len(new_p)} new p "
          f"{dict(collections.Counter((lv, yr) for _, lv, yr in new_p))} (the orchestrator: 569 gained); lost: {len(lost)} {lost[:3]} (none)")
    print(f"  new records in all: {sum(1 for c, *_ in diff.values() if c == 'A')} {dict(collections.Counter((lv, yr) for c, lv, yr, *_ in diff.values() if c == 'A'))} (D3: 559 local and 7 questions)")
    over2 = [m for m in moved if m[0] > 2 or m[0] < 0.5]
    print(f"  p moved (every P in my diff): {len(moved):,} = " + " + ".join(f"{lv} {n:,}" for lv, n in sorted(collections.Counter(lv for _, _, lv, _ in moved).items()))
          + f" (the orchestrator: 9,713; the file's P rows {sum(1 for r in mv['records'] if 'P' in r[8]):,}); over 2x either way: {len(over2)} {over2[:5]}; "
          f"extremes: min {min(moved)[0]:.4f} {min(moved)[1]}, max {max(moved)[0]:.4f} {max(moved)[1]}")
    bands = collections.Counter()
    for r_, i, lv, yr in moved:
        bands[(lv, "within 0.002%" if abs(r_ - 1) <= 2e-5 else "within 0.15%" if abs(r_ - 1) <= 1.5e-3 else "0.15-1%" if abs(r_ - 1) <= 0.01 else "1-10%" if abs(r_ - 1) <= 0.1 else "beyond 10%")] += 1
    print(f"  bands by level: " + "; ".join(f"{lv} {b} {n:,}" for (lv, b), n in sorted(bands.items())))
    # D3's three groups: the school boards of 2024, the local D-R races of 2020 and 2024 (route (a)), the legislatures
    sb = [(r_, i) for r_, i, lv, yr in moved if lv == "local" and (diff[i][4].get("office_type") == "school board")]
    sbr = collections.Counter()
    for r_, i in sb:
        f = (diff[i][4].get("forecasts") or [{}])[-1]
        sbr[f.get("class", "?")[-13:]] += 1
    byc = collections.defaultdict(list)
    for r_, i in sb:
        byc[(diff[i][4].get("forecasts") or [{}])[-1].get("class", "?")].append(r_)
    print(f"  the school boards of 2024 moved: {len(sb)} (D3: 756): " + "; ".join(f"'{k[-30:]}' {len(v)} x{min(v):.3f}-{max(v):.3f}" for k, v in sorted(byc.items())))
    dr = [(r_, i) for r_, i, lv, yr in moved if lv == "local" and diff[i][4].get("office_type") != "school board"]
    print(f"  other local p moved: {len(dr)} (D3: 1,067 races between a Democrat and a Republican by route (a), within 0.002%): routes {dict(collections.Counter((diff[i][4].get('forecasts') or [{}])[-1].get('route') for _, i in dr))}; "
          f"largest move {max(abs(r_ - 1) for r_, i in dr) if dr else None:.2e}; years {dict(collections.Counter(diff[i][2] for _, i in dr))}")
    leg = [(r_, i, lv, yr) for r_, i, lv, yr in moved if lv.startswith("state-")]
    big = sorted([m for m in leg if abs(m[0] - 1) > 1.5e-3], key=lambda m: m[0])
    print(f"  legislature p moved: {len(leg):,} (D3: 7,874 within 0.15% and Indiana 2020's 16 Senate races x0.969 to x0.998); beyond 0.15%: {len(big)}: "
          + "; ".join(f"{i} x{r_:.4f}" for r_, i, lv, yr in big))
    for r_, i, lv, yr in big[:16]:
        b, a = diff[i][3], diff[i][4]
        fb, fa = b.get("forecast_inputs") or {}, a.get("forecast_inputs") or {}
        print(f"    {i}: x{r_:.4f}; lean {fb.get('lean')} -> {fa.get('lean')} (lean_year {fa.get('lean_year')}); swing {fb.get('swing')} -> {fa.get('swing')}; class {fa.get('class')}")
    return diff


# ------------------------------------------------------------------------------------------ 49.2 the unopposed comparator

_X = {}


def export(year):
    if year not in _X:
        with open(os.path.join(VA[year]["dir"], VA[year]["export"])) as f:
            _X[year] = json.load(f)
    return _X[year]


def check_hashes(year):
    d = VA[year]["dir"]
    sums = {}
    with open(os.path.join(d, "SHA256SUMS")) as f:
        for line in f:
            h, _, n = line.strip().partition("  ")
            sums[n] = h
    out = {}
    for n, h in sums.items():
        out[n] = (sha256(os.path.join(d, n)) == h, h[:12])
    return out


def local_contests(year):
    """The export's contests beside the legislature's (and, in 2025, beside the Governor, D2's), in D3's shape (c45's reading,
    with D3's 2025 additions copied: the Governor skipped; 'statewide' where a shared contest is on every locality's list)."""
    x = export(year)
    state_items = {b["id"]: b for b in x["results"]["ballotItems"]}
    names = {lr["id"]: lr["name"].title() for lr in x["localResults"]}
    by_item = collections.defaultdict(list)
    for lr in x["localResults"]:
        for b in lr["ballotItems"]:
            by_item[b["id"]].append((lr, b))
    out = []
    for iid, parts in by_item.items():
        b0 = parts[0][1]
        if iid in state_items and b0["name"].startswith("Member, "):
            continue
        if iid in state_items and " ".join(b0["name"].split()).upper() == "GOVERNOR":
            continue
        shared = iid in state_items
        lids = sorted(lr["id"] for lr, _ in parts)
        office, district = C45._title(b0["name"], [names[i] for i in lids])
        sb = state_items.get(iid)
        opts = [(o["id"], o["name"].strip(), o["voteCount"], C45.option_kind(o["id"]), o.get("politicalParty")) for o in (sb or b0)["ballotOptions"]]
        out.append({"item": iid, "title": " ".join(b0["name"].split()), "office": office, "district": district,
                    "localities": lids, "counties": sorted("51" + i for i in lids), "shared": shared,
                    "seats": b0["voteFor"], "question": b0["contestType"] == "BallotMeasure",
                    "special": bool(C45.SPECIAL.search(b0["name"])), "options": opts, "parts": parts, "state_item": sb,
                    "statewide": shared and len(parts) == len(x["localResults"])})
    return out


def tops(lr):   # D3's _tops, copied (with (b)'s unopposed mark): [(votes, name, item id, unopposed)]
    n = max(b["precinctsParticipating"] or 0 for b in lr["ballotItems"])
    out, cham, cham_un = [], collections.Counter(), set()
    for b in lr["ballotItems"]:
        v = sum(o["voteCount"] for o in b["ballotOptions"])
        names = sum(1 for o in b["ballotOptions"] if BALLOT_ID.fullmatch(o["id"]))
        unopposed = b["contestType"] != "BallotMeasure" and names <= (b["voteFor"] or 1)
        m = LEG_TITLE.match(b["name"])
        if m:
            cham[m.group(1)] += v
            if unopposed:
                cham_un.add(m.group(1))
        elif (b["voteFor"] == 1 or b["contestType"] == "BallotMeasure") and b["precinctsParticipating"] == n:
            out.append((v, " ".join(b["name"].split()), b["id"], unopposed))
    out += [(v, f"{POSS[ch]} lines in {lr['name'].title()}, summed", None, ch in cham_un) for ch, v in cham.items()]
    return out


def over_ballot(c, tops_by):
    """D3's over-ballot test within the locality, copied: per locality line, votes for each seat against the highest-vote other
    contest; the line shown is one over its line if any (the furthest over), else the highest ratio."""
    over = []
    for lr, b in c["parts"]:
        v = sum(o["voteCount"] for o in b["ballotOptions"])
        mine = v / (b["voteFor"] or 1) if not c["question"] else v
        others = [t for t in tops_by[lr["id"]] if t[2] != c["item"]]
        top, name, _, un = max(others) if others else (None, None, None, False)
        r = mine / top if top else None
        over.append({"locality": lr["name"].title(), "votes_per_seat": round(mine, 1), "top": top, "top_name": name,
                     "top_unopposed": un, "line": OVER_LINE_UNOPPOSED if un else OVER_LINE, "ratio": None if r is None else round(r, 4)})
    read_ = [o for o in over if o["ratio"] is not None]
    worst = max(read_, key=lambda o: (o["ratio"] > o["line"], o["ratio"] / o["line"] if o["ratio"] > o["line"] else o["ratio"]), default=None)
    verdict = "untested" if worst is None else "held" if worst["ratio"] > worst["line"] else "listed" if worst["ratio"] > 1 else "passes"
    return worst, verdict


def file_index(cs):   # c45's file_index, on this script's options (five fields)
    d = collections.defaultdict(list)
    for c in cs:
        d[(tuple(c["counties"]), c["office"].upper(), c["district"])].append(c)
    return d


def contest_of(r, index):   # c45's contest_of, on this script's options
    cands = {x["name"].strip() for x in r["result"]["candidates"]}
    hits = index.get(C45.rec_key(r), [])
    if len(hits) == 1:
        return hits[0]
    same = [c for c in hits if {o[1] for o in c["options"]} == cands]
    return same[0] if len(same) == 1 else None


def va_records(commit, year):
    rs = list(records_at(commit, f"data/local/{year}/VA.json").values())
    qs = list(records_at(commit, f"data/measure/{year}/VA.json").values())
    return rs, qs


def section_2():
    h1("49.2 The unopposed comparator (the orchestrator, 00:55 (b)): D3's rules copied at every level")
    # (a) Virginia's local contests from the export
    for year in (2023, 2025):
        hs = check_hashes(year)
        print(f"\n  Virginia {year}: the files' sha256 against D3's SHA256SUMS: {hs}")
        cs = local_contests(year)
        x = export(year)
        tops_by = {lr["id"]: tops(lr) for lr in x["localResults"]}
        index = file_index(cs)
        n_un = sum(1 for ts in tops_by.values() for t in ts if t[3])
        print(f"    contests beside the legislature's{' and the Governor' if year == 2025 else ''}: {len(cs)}; top figures per locality {sum(len(v) for v in tops_by.values())}, unopposed {n_un} "
              f"(a figure is unopposed where its contest has no more names on the ballot than seats, write-in lines aside; a chamber's lines summed, where any of its contests there is)")
        for commit in ((BEFORE, AFTER) if year == 2023 else (AFTER,)):
            rs, qs = va_records(commit, year)
            g = collections.Counter((r.get("gate") or {}).get("over_ballot") for r in rs + qs)
            print(f"    the records' gate verdicts at {commit}: {dict(g)}")
        rs, qs = va_records(AFTER, year)
        same_r = diff_r = same_v = diff_v = 0
        held, listed, worst_ex = [], [], []
        noted = 0
        for r in rs + qs:
            c = contest_of(r, index)
            if c is None:
                continue
            w, verdict = over_ballot(c, tops_by)
            g = r.get("gate") or {}
            if w is not None and g.get("over_ballot_ratio") is not None and abs(w["ratio"] - g["over_ballot_ratio"]) <= 1e-4:
                same_r += 1
            else:
                diff_r += 1
                worst_ex.append((r["id"], None if w is None else w["ratio"], g.get("over_ballot_ratio")))
            if verdict == g.get("over_ballot"):
                same_v += 1
            else:
                diff_v += 1
                worst_ex.append((r["id"], verdict, g.get("over_ballot")))
            if verdict == "held":
                held.append((c["title"], w))
            if verdict == "listed":
                listed.append((c["title"], w))
            if any("unopposed (an unopposed contest loses its voters who skip it" in n for n in (r.get("notes") or [])):
                noted += 1
        print(f"    records with a file contest: {same_r + diff_r}; ratio equal to the record's gate (4 decimals): {same_r}; differing: {diff_r}; verdict equal: {same_v}; differing: {diff_v} {worst_ex[:6]}")
        print(f"    held by the over-ballot test, mine: {len(held)}: " + "; ".join(f"{t} {w['ratio']} in {w['locality']} against {w['top_name']} {w['top']:,}{' (unopposed)' if w['top_unopposed'] else ''}" for t, w in held))
        un_listed = [(t, w) for t, w in listed if w["top_unopposed"]]
        print(f"    listed, mine: {len(listed)} (D3: {'31' if year == 2023 else '0'}); against an unopposed comparator: {len(un_listed)}; records whose note names an unopposed comparator: {noted} (D3: {'10' if year == 2023 else '0'})")
        for t, w in sorted(un_listed, key=lambda z: -z[1]["ratio"]):
            print(f"      {t}: {w['votes_per_seat']:,.0f} for each seat in {w['locality']}, {w['ratio']:.4f} times the {w['top']:,} of {w['top_name']} (line {w['line']})")
        if year == 2023:
            for t, w in un_listed:
                comp = next((c for c in cs if c["title"] == w["top_name"]), None)
                if comp and any(k in t for k in ("Halifax", "Cumberland", "Norton")):
                    print(f"      the comparator {w['top_name']}: options {[(o[1], o[2], o[3]) for o in comp['options']]}; ballot names {sum(1 for o in comp['options'] if o[3] == 'ballot')} for {comp['seats']} seat(s)")
            # the three D3 names, held before and listed now: their p before and after
            for key in ("SHERIFF-county_51083", "SHERIFF-county_51049", "CLERK_OF_COURT"):
                for r in rs:
                    if key in r["id"] and (key != "CLERK_OF_COURT" or "51720" in r["id"]):
                        b = records_at(BEFORE, "data/local/2023/VA.json").get(r["id"])
                        print(f"      {r['id']}: before {str((b or {}).get('p'))[:90]}; after {str(r.get('p'))[:120]}")
        mx = max((w["ratio"] for r in rs + qs for c in [contest_of(r, index)] if c for w, _ in [over_ballot(c, tops_by)] if w), default=None)
        print(f"    the highest ratio of any record, mine: {mx} (D3 2025: no contest over 1.0)")
    # (b) MEDSL's over-ballot rows: no unopposed top contest
    chk = L.load_json(at(AFTER, "data/local/check-over-ballot.json"))
    print(f"\n  MEDSL's over-ballot test (check-over-ballot.json): about: {chk['about'][:160]}...")
    for yr in ("2018", "2022", "2024"):
        rows = chk[yr]
        print(f"    {yr}: rows {len(rows)}; against 'top' {sum(1 for r in rows if r['against'] == 'top')}; top_unopposed true {sum(1 for r in rows if r.get('top_unopposed'))}; verdicts {dict(collections.Counter(r['verdict'][:6] for r in rows))}")
    # from the records: the statewide one-seat contests of the local files with one name on the ballot, and the day's top by votes
    for year in (2018, 2022, 2024):
        one, tops_rec = [], {}
        d = at(AFTER, f"data/local/{year}")
        for n in sorted(os.listdir(d)):
            if not re.fullmatch(r"[A-Z]{2}\.json", n):
                continue
            for r in records_at(AFTER, f"data/local/{year}/{n}").values():
                if r.get("office_scope") != "state" or (r.get("seats") or 1) != 1 or r.get("question"):
                    continue
                cands = r["result"]["candidates"]
                names = [c for c in cands if c.get("party") != "write-in" and "WRITE" not in c["name"].upper()]
                v = sum(c["votes"] for c in cands)
                k = (r["place"]["state"], r["date"])
                if k not in tops_rec or v > tops_rec[k][0]:
                    tops_rec[k] = (v, r["office"], len(names))
                if len(names) <= 1:
                    one.append((r["place"]["state"], r["office"], v, len(names)))
        # MEDSL's federal lines (the president's and the US Senate's) are in D3's tops too: D2's records of the year
        fed_one = []
        for lv in ("president", "senate"):
            f = at(AFTER, f"data/{lv}/{year}.json")
            if not os.path.exists(f):
                continue
            for r in L.load_json(f)["contests"]:
                st_, dt = r["place"]["state"], r.get("date")
                cands = r["result"]["candidates"]
                v = sum(c["votes"] for c in cands)
                names = [c for c in cands if (c.get("party") or "").lower() not in ("write-in",) and "WRITE" not in (c.get("name") or "").upper()]
                if lv == "senate" and len(names) <= 1:
                    fed_one.append((st_, r.get("office"), v, len(names)))
                k = (st_, dt)
                if k not in tops_rec or v > tops_rec[k][0]:
                    tops_rec[k] = (v, f"{lv}: {r.get('office', lv)}", len(names))
        top_one = [(k, v) for k, v in tops_rec.items() if v[2] <= 1]
        print(f"    {year} from the records (office_scope state, one seat, with D2's president and US Senate records as the federal lines): one-name statewide contests {len(one)}: {sorted(one)[:8]}...; "
              f"US Senate contests with one name: {fed_one} (D3: none); state-days whose top contest by votes has one name: {top_one} (D3: none)")
    # (c) the over-seats figures: the names on every statewide contest's ballot from the raw files
    print("\n  the over-seats test (local_districts): a district's ballots rest on unopposed contests alone where every wide contest giving them has one name")
    chk = L.load_json(at(AFTER, "data/local/check-districts.json"))
    for year in (2016, 2018, 2022):
        yv = chk["years"][str(year)]
        fl = [f for f in yv["flags"] if isinstance(f.get("over_seats"), dict) and f["over_seats"].get("read")]
        bu = collections.Counter(str(f["over_seats"].get("by_unopposed")) for f in fl)
        lines = collections.Counter(f["over_seats"].get("line") for f in fl)
        nm = names_by_year(year)
        one = sorted((st, k, sorted(v)) for st, d in nm.items() for k, v in d.items() if len(v) <= 1)
        print(f"    {year}: D3's flags with over_seats read {len(fl)}: by_unopposed {dict(bu)}, line {dict(lines)}; my raw-file pass: statewide one-seat contests with one name: {len(one)}: "
              + "; ".join(f"{st} {k.split('|')[0][:40]} {v}" for st, k, v in one))
        if year == 2018:
            govs = {st: sorted(nm[st].get(k, set())) for st, k, v in one for st_ in [st] for k in nm[st] if k.startswith("GOVERNOR")}
            print(f"      the governor's names in those states: " + "; ".join(f"{st} {len(v)}" for st, v in sorted(govs.items())))
        # my by_unopposed on D3's read flags
        mine = collections.Counter()
        ps = C48.passes(year)
        by_state_file = {}
        for p, d in ps.items():
            for st in d["seen"]:
                by_state_file.setdefault(st, []).append(p)
        for f in fl:
            y_, st, lv, key = C46.kid_norm(f["id"])
            files = by_state_file.get(st, [])
            if not files:
                mine["no raw file"] += 1
                continue
            d = ps[files[0]]
            sen = 1 if lv == "state-upper" else 0
            k = f"{st}|{sen}|{C48.dkey(f['medsl_district'])}"
            got = ballots_keys(d, st, [k])
            if k not in got:
                mine["no ballots in my pass"] += 1
                continue
            keys = got[k][2]
            un = all(len(nm.get(st, {}).get(c, set())) <= 1 for c in keys)
            mine[("mine", un, "D3", bool(f["over_seats"].get("by_unopposed")))] += 1
        print(f"      my by_unopposed on D3's read flags against his: {dict(mine)}")


def ballots_keys(d, st, keys):
    """c48's district_ballots with the wide contests' keys kept: {key: [precincts, ballots, [contest keys giving them]]}."""
    tot, oth = d["tot"].get(st, {}), d["oth"].get(st, {})
    ks = set(tot) | set(oth)
    votes = {k: {q: max(tot.get(k, {}).get(q, 0), oth.get(k, {}).get(q, 0)) for q in set(tot.get(k, {})) | set(oth.get(k, {}))} for k in ks}
    allp = set().union(*[set(v) for v in votes.values()]) if votes else set()
    wide = [k for k in ks if allp and len(votes[k]) >= C48.STATEWIDE_SPREAD * len(allp)]
    out = {}
    for k in keys:
        ps = d["leg"].get(k)
        if not ps or not wide:
            continue
        b = [max(votes[c].get(q, 0) for c in wide) for q in ps]
        if all(b):
            out[k] = [len(ps), sum(b), sorted(c for c in wide if any(votes[c].get(q) for q in ps))]
    return out


def names_pass(path, year):
    """One pass over a raw MEDSL file for the names on each statewide one-seat contest's ballot (D3's district_ballots'
    names, copied: stage GEN, not special; meta names, total rows and NOT_A_CONTEST offices skipped as c48's pass skips
    them; a name counts where writein is not TRUE and 'WRITE' is not in it). Cached in DERIVED by size and mtime."""
    os.makedirs(DERIVED, exist_ok=True)
    stt = os.stat(path)
    cache = os.path.join(DERIVED, f"p20-{os.path.basename(path)}.json")
    stamp = {"size": stt.st_size, "mtime": int(stt.st_mtime), "version": 1}
    if os.path.exists(cache):
        d = L.load_json(cache)
        if d.get("stamp") == stamp:
            return d
    names = collections.defaultdict(lambda: collections.defaultdict(set))
    for r in M.rows(path):
        st = r.get("state_po") or r.get("state_postal") or ""
        if (r.get("stage") or "").upper() != "GEN" or (r.get("special") or "").strip().upper() == "TRUE":
            continue
        office = (r.get("office") or "").strip().upper()
        cand = (r.get("candidate") or "").strip()
        prec = r.get("precinct") or ""
        if M.is_meta(cand) or C43.AGG_NAME.search(prec) or C43.COUNTY_TOTAL.search(prec.strip().upper()):
            continue
        if C43.NOT_A_CONTEST.search(office) or C48.leg_office(office, r.get("district") or "") is not None:
            continue
        if cand.upper() in C43.ANSWERS or not C48.statewide_one_seat(r, office):
            continue
        if (r.get("writein") or "").strip().upper() != "TRUE" and "WRITE" not in cand.upper():
            names[st][f"{office}|{(r.get('district') or '').strip()}"].add(cand.upper())
    out = {"stamp": stamp, "names": {st: {k: sorted(v) for k, v in d.items()} for st, d in names.items()}}
    with open(cache, "w") as f:
        json.dump(out, f)
    return out


_NAMES = {}


def names_by_year(year):
    """{st: {contest key: set of names}} over every raw file of the year."""
    if year not in _NAMES:
        out = collections.defaultdict(dict)
        for p in C48.raw_files(year):
            d = names_pass(p, year)
            for st, m in d["names"].items():
                for k, v in m.items():
                    out[st].setdefault(k, set()).update(v)
        _NAMES[year] = out
    return _NAMES[year]


# ------------------------------------------------------------------------------------------ 49.3 the Code of Virginia

def code_text(name):
    """D3's _code_text, copied: the page's text, tags and whitespace aside, a linked section number's space before its stop closed."""
    with open(os.path.join(SRC, "va_code", name), encoding="utf-8") as f:
        text = " ".join(_html.unescape(re.sub(r"<[^>]+>", " ", f.read())).split())
    return re.sub(r" ([.,;:])", r"\1", text)


def section_3():
    h1("49.3 The Code of Virginia's pages read again, and the school boards' class (the orchestrator, 00:55 (c), 07:48, 08:07)")
    idx = {}
    with open(os.path.join(SRC, "index.txt")) as f:
        for line in f:
            p = line.rstrip("\n").split("\t")
            if p[0].startswith("vacode:") or p[0].startswith("in2018:"):
                idx[p[0]] = p
    print("  my requests (fetch_eighth_pass.sh va_code, in_2018; index.txt): " + "; ".join(f"{k} {v[1]} at {v[2]} UTC, {v[6]} bytes" for k, v in idx.items()))
    # the sha256 the records quote
    rs23, _ = va_records(AFTER, 2023)
    quoted = collections.Counter()
    for r in rs23:
        for n in r.get("notes") or []:
            m = re.search(r"(https://law\.lis\.virginia\.gov/\S+), read (\S+), sha256 ([0-9a-f]{64})", n)
            if m:
                quoted[(m.group(1), m.group(2), m.group(3)[:16])] += 1
        p = r.get("p") or {}
        m = re.search(r"(https://law\.lis\.virginia\.gov/\S+), read (\S+), sha256 ([0-9a-f]{64})", p.get("not_computed") or "")
        if m:
            quoted[(m.group(1), m.group(2), m.group(3)[:16])] += 1
    print("  pages the 2023 records quote (url, read, sha256): " + "; ".join(f"{k} in {v} records" for k, v in sorted(quoted.items())))
    for name in ("section24.2-613.html", "title22.1-chapter5-article7.html", "title10.1-chapter5-article3.html"):
        mine = sha256(os.path.join(SRC, "va_code", name))
        theirs = next((k[2] for k in quoted if k[2] == mine[:16]), None)
        print(f"  {name}: my sha256 {mine[:16]}...; {'equal to the records'' quoted' if theirs else 'not quoted by the records (D3 recorded no sha for it)' if name.startswith('title10') else 'DIFFERS from the records'' quoted'}")
    for sec, (name, words) in CODE.items():
        t = code_text(name)
        print(f"  section {sec}: the words quoted {'are' if words in t else 'are NOT'} in my copy of {name}" + (f"; the page has {t.count('§ ')} section marks" if words in t else ""))
    t7 = code_text("title22.1-chapter5-article7.html")
    a = re.search(r"§ 22\.1-57\.3:3\. (.{0,400})", t7)
    print(f"  section 22.1-57.3:3's head as my copy reads: {a.group(1)[:330] if a else None}...")
    e = re.search(r"§ 22\.1-57\.3\. Election of school board members; election of tie breaker\.(.{0,120})", t7)
    print(f"  section 22.1-57.3's heading: {'found' if e else 'NOT found'}; subsection E's words follow 'E. ': {'E. In order to have their names placed on the ballot' in t7}")
    t3 = code_text("title10.1-chapter5-article3.html")
    s = re.search(r"§ 10\.1-523\. Nominating petitions; posting of notice\. A\. (.{0,300})", t3)
    print(f"  section 10.1-523 A as my copy reads: {s.group(1)[:300] if s else None}")
    t6 = code_text("section24.2-613.html")
    b = re.search(r"B\. (For elections for federal.{0,200})", t6)
    print(f"  section 24.2-613 B as my copy reads: {b.group(1)[:220] if b else None}")
    # the class in the records
    for year in (2023, 2025):
        rs, qs = va_records(AFTER, year)
        sb = [r for r in rs if SCHOOL_BOARD.search(r.get("office") or "")]
        ch = [r for r in rs if CHAIR_SCHOOL.search(r.get("office") or "")]
        nonp_note = [r for r in rs if any(n.startswith("nonpartisan: the Code of Virginia, section 22.1-57.3") for n in r.get("notes") or [])]
        chair_note = [r for r in rs if any(n.startswith("the chairman of the school board is a member") for n in r.get("notes") or [])]
        why = [r for r in rs if "section 24.2-613 B" in ((r.get("p") or {}).get("not_computed") or "")]
        print(f"\n  Virginia {year}: records {len(rs)}; office matching D3's SCHOOL BOARD regex: {len(sb)}; with the nonpartisan note: {len(nonp_note)} (equal sets: {set(r['id'] for r in sb) == set(r['id'] for r in nonp_note)}); "
              f"chairman: {[(r['office'], r['place']['counties']) for r in ch]}, with the chairman's note: {len(chair_note)}; reasons naming section 24.2-613 B: {len(why)}")
        print(f"    school boards by office_type: {dict(collections.Counter(r.get('office_type') for r in sb))}; by p state: {dict(collections.Counter(reason_kind(r) for r in sb))}")
        if year == 2023:
            b_all = records_at(BEFORE, "data/local/2023/VA.json")
            png_before = [i for i, r in b_all.items() if "party not given in the source" in ((r.get("p") or {}).get("not_computed") or "") and "fewer than" in ((r.get("p") or {}).get("not_computed") or "")]
            sb_ids = {r["id"] for r in sb}
            print(f"    before: 'party not given' not computed for too few like races: {len(png_before)} (D3: 519); school boards among them: {len([i for i in png_before if i in sb_ids])} (D3: 163)")
            new_p = [r for r in sb if (r.get("p") or {}).get("value") and (b_all.get(r["id"], {}).get("p") or {}).get("value") is None]
            cls = collections.Counter((r["forecasts"][-1]["class"], r["forecasts"][-1]["like_races"], r["forecasts"][-1]["in_window"]) for r in new_p)
            print(f"    school boards with p now and none before: {len(new_p)} (D3: 158): " + "; ".join(f"'{k[0][-30:]}' N {k[1]} k {k[2]}: {v}" for k, v in sorted(cls.items())))
            ps = [r["p"]["value"] for r in new_p]
            print(f"      their p: from {min(ps):.3g} to {max(ps):.3g}, median {sorted(ps)[len(ps) // 2]:.3g} (D3: 2.2 in 100,000 to 1.0 in 100, median 1.2 in 1,000)")
            few = [(r["id"][-40:], re.search(r"\((\d+)\) for the class '(.+?)'", r["p"].get("not_computed", "")).groups()) for r in sb if "fewer than" in (r.get("p") or {}).get("not_computed", "")]
            print(f"      school boards still too few like races: {len(few)} (D3: 5, with 55 and 76): {few}")
            kept = [r for r in sb if r["id"] not in {x["id"] for x in new_p}]
            print(f"      the other school boards: {len(kept)} (D3: 225): {dict(collections.Counter(reason_kind(r) for r in kept))}")
            others_few = [r for r in rs if not SCHOOL_BOARD.search(r.get('office') or '') and "fewer than" in ((r.get("p") or {}).get("not_computed") or "")]
            print(f"      other offices too few like races: {len(others_few)} (D3: 364), naming section 24.2-613 B: {sum(1 for r in others_few if 'section 24.2-613 B' in r['p']['not_computed'])}")
            # the notes' read time and sha
            times = collections.Counter(re.search(r"read (\S+), sha256 (\S{12})", n).groups() for r in nonp_note for n in r["notes"] if n.startswith("nonpartisan: the Code"))
            print(f"      the nonpartisan notes' (read time, sha256) : {dict(times)} (D3's meta: 2026-11-13T07:50:46Z)")
        else:
            sw = [r for r in rs if r.get("office_scope") == "state"]
            rest = [r for r in rs if not SCHOOL_BOARD.search(r.get("office") or "") and r.get("office_scope") != "state"]
            png = [r for r in rest if (r.get("forecasts") or [{}])[-1].get("class", "").find(PARTY_NOT_GIVEN) >= 0 or PARTY_NOT_GIVEN in ((r.get("p") or {}).get("not_computed") or "")]
            print(f"    every other local office: {len(rest)} (D3: 378 'party not given in the source'), of which a class or reason naming it {len(png)} (the rest p 0, special or strong write-ins: {dict(collections.Counter(reason_kind(r) for r in rest if r not in png))}); "
                  f"statewide: {[(r['office'], [(c['name'], c.get('party')) for c in r['result']['candidates']]) for r in sw]}")
            print(f"    the chairman's record: {[(r['id'], r['place'], (r.get('forecasts') or [{}])[-1].get('class'), str(r.get('p'))[:80]) for r in ch]}")


# ------------------------------------------------------------------------------------------ 49.4 the local like-race pools

def generic(name):   # D3's _is_generic, copied
    n = name.strip().upper()
    return n in {"WRITE-IN", "WRITEIN", "WRITE IN", "SCATTERING", "WRITE-INS"} or n.startswith("*") or "WRITE" in n


def ballot_of(r):
    return [c for c in r["result"]["candidates"] if c.get("party") != "write-in" and not generic(c["name"])]


IN_POOL_REASONS = ("fewer than", "a write-in line is in the", "write-in", "a race between a Democrat and a Republican")


def my_local_structure(r):
    """D3's local_structure, copied onto a record (its ballot: the candidates but the write-ins; its seats; its party words as
    the record writes them: None for a blank party in MEDSL's file, which D3's rule reads as nonpartisan, 'nonpartisan',
    'D', 'R'; Virginia's 'party not given' where the source is the Department's and the record has no nonpartisan note):
    (route, class key or why). A record whose p is not computed for a reason the pool does not take (special, held, a
    recount, redacted, seats unverified, a round) is out, as D3's held() and local_structure put it out."""
    p = r.get("p") or {}
    nc = p.get("not_computed") or ""
    el = r.get("election") or ""
    if "special" in el:
        return ("not computed", "special")
    if "recount" in el.lower():
        return ("not computed", "a recount")
    if not (el == "general" or el.startswith("deciding round")):   # D3's stage GEN: a November general or its deciding round; the
        return ("not computed", el[:40])                            # State Board's contests on other dates are built apart (local_ncsbe)
    if nc and not any(nc.startswith(w) or w in nc[:60] for w in IN_POOL_REASONS):
        return ("not computed", nc[:50])
    b = ballot_of(r)
    k = r.get("seats") or 1
    if len(b) <= k:
        return ("zero", "one name a seat")
    if any(c.get("votes_incomplete") for c in b):
        return ("not computed", "redacted")
    nd = sum(1 for c in b if c.get("party") == "D")
    nr = sum(1 for c in b if c.get("party") == "R")
    scope = "state" if r.get("office_scope") == "state" else "local"
    ot = r.get("office_type")
    png = r["result"].get("source") == "va_elect" and scope == "local" and not any(n.startswith("nonpartisan: the Code of Virginia") for n in r.get("notes") or [])
    if k > 1:
        slate = PARTY_NOT_GIVEN if png else "both major parties on the ballot" if nd and nr else "one major party or none"
        return ("boundary", f"{scope} {ot}, {k if k < 4 else '4+'} seats at once, {slate}")
    if nd == 1 and nr == 1:
        return ("partisan", f"a {scope} race between a Democrat and a Republican")
    nonpartisan = all(c.get("party") in (None, "nonpartisan") for c in b)
    kind = (PARTY_NOT_GIVEN if png else "nonpartisan" if nonpartisan else "one major party against others" if nd + nr == 1
            else "two or more of one major party" if nd + nr >= 2 else "no Democrat or Republican")
    n = len(b)
    return ("class", f"{scope} {ot}, {kind}, {n if n < 4 else '4+'} candidates")


def rec_class(r):
    fc = r.get("forecasts") or []
    if fc and fc[-1].get("class"):
        return fc[-1]["route"], fc[-1]["class"]
    m = re.search(r"for the class '(.+?)'\s*(?:;|$)", (r.get("p") or {}).get("not_computed") or "")
    return (None, m.group(1)) if m else (None, None)


_LPOOL = {}


def local_pool(commit):
    """{class key: [(year, share)]} from every local record at the commit (D3's local_rows copied: the k-th and (k+1)-th ballot
    names' votes), and the tally of my class against the record's."""
    if commit in _LPOOL:
        return _LPOOL[commit]
    pool = collections.defaultdict(list)
    tal = collections.Counter()
    ex = []
    root = at(commit, "data/local")
    for yr in sorted(os.listdir(root)):
        # D3's pool years (local_medsl.build: lrows for YEARS + ODD_YEARS): MEDSL's 2018, 2020, 2022 and 2024 (with the State Board's
        # November contests in place of MEDSL's for North Carolina), and 2023 and 2025 from Louisiana's and Virginia's own files; MEDSL's 2016
        # sets are read for their questions alone, and the State Board's odd-year municipal contests are built and pooled apart (local_ncsbe)
        if not yr.isdigit() or int(yr) not in (2018, 2020, 2022, 2023, 2024, 2025):
            continue
        for n in sorted(os.listdir(os.path.join(root, yr))):
            if not re.fullmatch(r"[A-Z]{2}\.json", n):
                continue
            for r in records_at(commit, f"data/local/{yr}/{n}").values():
                if int(yr) % 2 == 1 and n[:2] == "NC":   # the State Board's odd-year contests: their own pool (local_ncsbe), not D3's
                    continue
                route, key = my_local_structure(r)
                rr, rk = rec_class(r)
                if route in ("class", "boundary"):
                    b = sorted(ballot_of(r), key=lambda c: -c["votes"])
                    kk = (r.get("seats") or 1) if route == "boundary" else 1
                    x1, x2 = b[kk - 1]["votes"], b[kk]["votes"]
                    if x1 + x2 > 0:
                        pool[key].append((int(yr), max(x1, x2) / (x1 + x2)))
                    if rk is not None:
                        tal[("my class = the record's", key == rk)] += 1
                        if key != rk and len(ex) < 6:
                            ex.append((r["id"], key, rk))
                    else:
                        tal[("my class; the record has none", (r.get("p") or {}).get("not_computed", "p " + str((r.get("p") or {}).get("value")))[:40])] += 1
                elif rk is not None and (r.get("p") or {}).get("value") is not None and rr in ("class", "boundary"):
                    if state_board_route(r):   # the State Board's other-date contests: its own pool (c15 §10.4-10.6), not D3's
                        tal[("the State Board's own pool (local_ncsbe), mine no class", route)] += 1
                        continue
                    tal[("the record has a like-race p, mine no class", route, str(key)[:30])] += 1
                    if len(ex) < 6:
                        ex.append((r["id"], route, key, rk))
    _LPOOL[commit] = (pool, tal, ex)
    return _LPOOL[commit]


def state_board_route(r):
    """True where the record's like-race p is fitted on the State Board's own pool (pipeline/local_ncsbe.py: North Carolina's
    odd-year municipal contests and its other dates), which c15 §10.4-10.6 reproduced and #111 does not touch."""
    fc = r.get("forecasts") or []
    return bool(fc) and str(fc[-1].get("fitted_on", "")).startswith("North Carolina's State Board")


def my_like_p(pool, r):
    """My (f, N, h, k) for a record's class from the pool's earlier years, and my p with the record's n: the deciding pair's
    n_other_voters (two_party for one seat; the record's boundary block, the k-th and (k+1)-th names, for the boundary route)."""
    rr, key = rec_class(r)
    t = r["year"]
    sh = [s for y, s in pool.get(key, []) if y < t]
    f, N, h, k = D.class_density(sh)
    n = ((r.get("boundary") if rr == "boundary" else r.get("two_party")) or {}).get("n_other_voters")
    if f is None or not n:
        return None, N, h, k, None
    p, use = C40.p_like(f, n)
    return p, N, h, k, use


def section_4():
    h1("49.4 The local like-race pools from the records at both commits (D3's local_structure and local_rows copied), every like-race p of 2023 to 2025")
    for commit in (BEFORE, AFTER):
        pool, tal, ex = local_pool(commit)
        print(f"\n  {commit}: pool rows {sum(len(v) for v in pool.values()):,} in {len(pool)} classes; my class against the record's: {dict(tal)}; e.g. {ex[:4]}")
        for key in ("local school board, nonpartisan, 2 candidates", "local school board, nonpartisan, 3 candidates", "local school board, nonpartisan, 4+ candidates",
                    "local council, commission or board, party not given in the source, 2 candidates", "local school board, 2 seats at once, one major party or none", "local school board, 3 seats at once, one major party or none"):
            by = collections.Counter(y for y, s in pool.get(key, []))
            print(f"    '{key}': by year {dict(sorted(by.items()))}")
    pb_, _, _ = local_pool(BEFORE)
    pa_, _, _ = local_pool(AFTER)
    diff = my_diff()[0]
    for commit, pool in ((BEFORE, pb_), (AFTER, pa_)):
        tal = collections.Counter()
        bad = []
        for yr in (2023, 2024, 2025):
            d = at(commit, f"data/local/{yr}")
            if not os.path.isdir(d):
                continue
            for n in sorted(os.listdir(d)):
                if not re.fullmatch(r"[A-Z]{2}\.json", n):
                    continue
                for r in records_at(commit, f"data/local/{yr}/{n}").values():
                    rr, key = rec_class(r)
                    if rr not in ("class", "boundary") or (r.get("p") or {}).get("value") is None:
                        continue
                    if state_board_route(r):
                        tal[(yr, "the State Board's own pool (pipeline/local_ncsbe.py; c15 §10.4-10.6), not tested here")] += 1
                        continue
                    f = r["forecasts"][-1]
                    p, N, h, k, use = my_like_p(pool, r)
                    same = (N == f.get("like_races"), k == f.get("in_window"), h is not None and abs(h - D.window_h(f.get("window"))) < 1e-9)
                    if p is None:
                        tal[(yr, n[:2], "mine: too few" if N < D.MIN_CLASS else "mine: no n", N)] += 1
                        bad.append((r["id"], f"mine N {N}; record N {f.get('like_races')}"))
                        continue
                    ratio = p / r["p"]["value"]
                    band = "within 1e-4" if abs(ratio - 1) <= 1e-4 else "within 1e-3" if abs(ratio - 1) <= 1e-3 else "within 1e-2" if abs(ratio - 1) <= 1e-2 else "beyond 1e-2"
                    tal[(yr, n[:2], "N,k,h equal" if all(same) else f"N,k,h {same}", band)] += 1
                    if not all(same) or band != "within 1e-4":
                        bad.append((r["id"], f"mine N {N} k {k} h {h} p {p:.4g} ({use}); record N {f.get('like_races')} k {f.get('in_window')} p {r['p']['value']}"))
        print(f"\n  every like-race p of 2023-2025 at {commit} against my pool's: ")
        for k_, v in sorted(tal.items(), key=str):
            print(f"    {str(k_):90s} {v:,}")
        for rid, s in bad[:10]:
            print(f"    {rid}: {s}")
    # the moves: my ratio after/before against the file's, for the school boards of 2024 and every other local like-race P row
    mv = L.load_json(at(AFTER, "data/local/moves-36.json"))
    prow = {r[0]: r for r in mv["records"] if "P" in r[8] and r[1].startswith("data/local/")}
    tal = collections.Counter()
    ex = []
    for i, row in prow.items():
        if i not in diff:
            tal["not in my diff"] += 1
            continue
        b, a = diff[i][3], diff[i][4]
        rr, key = rec_class(a)
        if rr not in ("class", "boundary"):
            tal[("route", rr)] += 1
            continue
        p0, *_ = my_like_p(pb_, b)
        p1, *_ = my_like_p(pa_, a)
        if not p0 or not p1:
            tal["mine: no p at one commit"] += 1
            continue
        mine, theirs = p1 / p0, row[7] if row[7] is not None else row[6] / row[5]
        dlt = abs(mine - theirs)
        tal[(a.get("office_type"), "within 5e-4" if dlt <= 5e-4 else "within 5e-3" if dlt <= 5e-3 else "beyond 5e-3")] += 1
        if dlt > 5e-4 and len(ex) < 8:
            ex.append((i, round(mine, 4), theirs))
    print(f"\n  the file's local P rows with a like-race route: my ratio (pool after / pool before) against the file's: {dict(tal)}; e.g. {ex}")
    # the 158 new p of 2023 and 2025's 127 from my pool
    for yr, want in ((2023, 158), (2025, 127)):
        rs, _ = va_records(AFTER, yr)
        got = collections.Counter()
        for r in rs:
            rr, key = rec_class(r)
            if rr not in ("class", "boundary") or (r.get("p") or {}).get("value") is None:
                continue
            p, N, h, k, use = my_like_p(pa_, r)
            got[(key[-34:], "mine = record within 1e-4" if p and abs(p / r["p"]["value"] - 1) <= 1e-4 else f"differs: mine {p} record {r['p']['value']}")] += 1
        print(f"  Virginia {yr}'s like-race p (D3: {want}): {sum(got.values())}: " + "; ".join(f"'{k}' {w}: {v}" for (k, w), v in sorted(got.items())))


# ------------------------------------------------------------------------------------------ 49.5 Virginia 2025 from the export

def page_contests(year):
    """c45's page_contests, on the year's rendered page."""
    with open(os.path.join(VA[year]["dir"], VA[year]["page"]), encoding="utf-8", errors="replace") as f:
        h = f.read()
    official = "OFFICIAL RESULTS" in h
    out = []
    for art in h.split("<article>")[1:]:
        m = re.search(r'class="panel-header h3"[^>]*>(?:<!---->)*<span>([^<]*)</span>', art)
        title = " ".join(m.group(1).split()) if m else None
        vf = re.search(r"<span>(Vote for [^<]*)</span>", art)
        opts = []
        for blk in re.split(r'class="ballot-option"', art)[1:]:
            nm = re.search(r'class="me-2">(?:<a [^>]*>)?(?:<span[^>]*>)?([^<]+)<', blk)
            vt = re.search(r'>Votes</span><span[^>]*>\s*([\d,]+)\s*<', blk)
            opts.append((" ".join(nm.group(1).split()) if nm else None, int(vt.group(1).replace(",", "")) if vt else None, ">Winner<" in blk))
        lr = re.search(r'Localities reporting</span><span class="fw-bold">\s*([\d]+/[\d]+)\s*<', art)
        out.append({"title": title, "vote_for": vf.group(1) if vf else None, "options": opts, "localities_reporting": lr.group(1) if lr else None})
    i = h.find("OFFICIAL RESULTS")
    heading = " ".join(re.sub(r"<[^>]+>", " ", h[max(0, i - 400):i + 120]).split()) if i >= 0 else None
    return official, out, heading


def section_5():
    h1("49.5 Virginia 2025 from the Department's export (D3's copy; the 566 contests, the gate, every record against the file)")
    x = export(2025)
    print(f"  the export: electionName {x.get('electionName')!r}, electionDate {x.get('electionDate')}, createdAt {x.get('createdAt')}; statewide items {len(x['results']['ballotItems'])}, localities {len(x['localResults'])}")
    cs = local_contests(2025)
    kinds = collections.Counter(("statewide" if c["statewide"] else "shared" if c["shared"] else "one locality") + (", question" if c["question"] else "") for c in cs)
    print(f"  contests beside the legislature's and the Governor: {len(cs)} {dict(kinds)} (D3: 567 beside the legislature's: the Governor, LG, AG, 8 shared, 556 on one list (549 offices, 7 questions); 566 taken in)")
    # the Governor against D2's
    gov = next(b for b in x["results"]["ballotItems"] if " ".join(b["name"].split()).upper() == "GOVERNOR")
    d2 = next(r for r in L.load_json(at(AFTER, "data/governor/2025.json"))["contests"] if r["place"]["state"] == "VA")
    fg = [(o["name"], o["voteCount"]) for o in gov["ballotOptions"]]
    dg = [(c["name"], c["votes"]) for c in d2["result"]["candidates"]]
    print(f"  the Governor: the file's statewide lines {fg}; D2's data/governor/2025.json {dg}; equal line by line: {fg == dg} (the year's gate, D3)")
    # the page
    official, page, heading = page_contests(2025)
    print(f"  the page as rendered: 'OFFICIAL RESULTS' {official}; heading {heading!r}; contests shown {len(page)} (D3: its first 50); the shared contests the page shows: "
          + "; ".join(f"{p['title']}" for p in page if not p["title"].startswith("Member,") and p["title"] != "Governor"))
    state_items = {" ".join(b["name"].split()): b for b in x["results"]["ballotItems"]}
    for p in page:
        if p["title"] in ("Lieutenant Governor", "Attorney General"):
            fo = [(o["name"].strip(), o["voteCount"]) for o in state_items[p["title"]]["ballotOptions"]]
            po = [(n, v) for n, v, w in p["options"]]
            print(f"    {p['title']}: page {po} winner marked {[n for n, v, w in p['options'] if w]}; file {fo}; equal: {sorted(fo) == sorted(po)}")
    titles_page = {p["title"] for p in page}
    shown = [c["title"] for c in cs if c["shared"] and c["title"] in titles_page]
    print(f"    shared local contests the page shows: {shown} (D3: none of the 8)")
    # the shared contests: locality lines add up option by option
    adds = []
    for c in cs:
        if not c["shared"]:
            continue
        state_opts = {o["id"]: o["voteCount"] for o in c["state_item"]["ballotOptions"]}
        summed = collections.Counter()
        for lr, b in c["parts"]:
            for o in b["ballotOptions"]:
                summed[o["id"]] += o["voteCount"]
        ok = all(summed.get(k, 0) == v for k, v in state_opts.items()) and set(summed) <= set(state_opts)
        adds.append((c["title"], len(c["parts"]), ok))
    print(f"  the shared contests ({len(adds)}): locality lines adding up to the statewide count, option by option: {sum(1 for _, _, ok in adds if ok)} of {len(adds)}: " + "; ".join(f"{t} ({n} localities){'' if ok else ' NOT'}" for t, n, ok in adds))
    # all reporting, per locality line
    full = {lr["id"]: all(s["status"] == "Fully Reported" for s in lr["reportingStatuses"]) for lr in x["localResults"]}
    statuses = collections.Counter(s["status"] for lr in x["localResults"] for s in lr["reportingStatuses"])
    not_all = [c["title"] for c in cs if not all(b["precinctsReporting"] == b["precinctsParticipating"] and full[lr["id"]] for lr, b in c["parts"])]
    print(f"  reporting statuses over the localities' groups: {dict(statuses)}; contests with a locality line not all reporting: {len(not_all)} {not_all[:5]}")
    # every record against the file
    rs, qs = va_records(AFTER, 2025)
    index = file_index(cs)
    tal = collections.Counter()
    bad = []
    for r in rs + qs:
        c = contest_of(r, index)
        if c is None:
            tal["no file contest found"] += 1
            bad.append((r["id"], "no contest"))
            continue
        tal["matched"] += 1
        rc = r["result"]["candidates"]
        q = c["question"]
        fo = sorted((n.upper() if q else n, v) for _, n, v, k, _ in c["options"])   # a question's answers are written in capitals
        ro = sorted((a["name"].strip(), a["votes"]) for a in rc)
        tal[("names and votes equal", fo == ro)] += 1
        if fo != ro and len(bad) < 8:
            bad.append((r["id"], f"file {fo[:4]} record {ro[:4]}"))
        if not q:
            wi_f = sorted(n for _, n, v, k, _ in c["options"] if k != "ballot")
            wi_r = sorted(a["name"].strip() for a in rc if a.get("party") == "write-in")
            tal[("write-in flags equal (by the option's key)", wi_f == wi_r)] += 1
        tal[("seats equal", (r.get("seats") or 1) == (c["seats"] or 1))] += 1
        tal[("special equal", ("special" in (r.get("election") or "")) == c["special"])] += 1
        tal[("counties equal", sorted(r["place"]["counties"]) == c["counties"])] += 1
        g = r.get("gate") or {}
        tal[("gate: shared", g.get("shared") == c["shared"], "page_equal", g.get("page_equal"), "parts_add_up", g.get("parts_add_up"), "all_reporting", g.get("all_reporting"), "over_ballot", g.get("over_ballot"), "precincts_add_up", g.get("precincts_add_up"))] += 1
        if c["statewide"]:
            tal[("statewide parties", tuple((a["name"], a.get("party")) for a in rc))] += 1
    print(f"  the records ({len(rs)} local + {len(qs)} questions) against the file: ")
    for k_, v in sorted(tal.items(), key=str):
        print(f"    {str(k_):120s} {v}")
    for b in bad[:6]:
        print(f"    {b}")
    # the write-ins by name
    named = [(c, [(n, v) for _, n, v, k, _ in c["options"] if k == "write-in by name"]) for c in cs if any(k == "write-in by name" for _, _, _, k, _ in c["options"])]
    outpoll, no_ballot, kinds = [], [], collections.Counter()
    for c, wi in named:
        ballot = sorted((v for _, n, v, k, _ in c["options"] if k == "ballot"), reverse=True)
        seats = c["seats"] or 1
        kinds[("ballot names", len(ballot), "seats", seats)] += 1
        if not ballot:
            no_ballot.append((c["title"], wi, seats))
        elif any(v > min(ballot) for n, v in wi):
            outpoll.append((c["title"], wi, ballot, seats))
    print(f"  contests with a name-keyed option (a write-in counted by name): {len(named)} (D3: 25) {dict(kinds)}; where such an option outpolls a name on the ballot: {len(outpoll)} {outpoll[:3]}; "
          f"with no name on the ballot at all (write-ins alone): {len(no_ballot)} {no_ballot[:3]}")
    # the p states, and my own class
    print(f"  the records' p states: {dict(collections.Counter(reason_kind(r) for r in rs))} (D3: p 0 283; by like races 127; too few 71; strong write-ins 39; special 37; D against R 2); questions: {dict(collections.Counter(reason_kind(r)[:50] for r in qs))}")
    agree = collections.Counter()
    for r in rs:
        mine = C44.my_class(r)
        agree[(reason_kind(r)[:30], mine)] += 1
    print("  my class (c44's rule: p 0 where one name a seat and write-ins under 10% of the last winner's; strong write-ins else) against the record's reason:")
    for k_, v in sorted(agree.items(), key=str):
        print(f"    {str(k_):90s} {v}")
    print(f"  the odd-year route (a) reason on the two statewide offices: " + "; ".join(f"{r['office']}: {(r.get('p') or {}).get('not_computed', '')[-200:]}" for r in rs if r.get("office_scope") == "state"))


# ------------------------------------------------------------------------------------------ 49.6 Indiana 2018

def first_last(name):   # D3's _first_last, copied
    return re.sub(r",\s*(JR|SR|II|III|IV|V)\.?$", r" \1", name, flags=re.I)


def in_archive_senate():
    """D3's in_archive, copied, on my copy of the State Senator file: {district: [(name, votes, write_in)]}."""
    with open(os.path.join(IN2018, "OffCatC_2180_A.json"), encoding="utf-8-sig") as f:
        d = json.load(f)
    out = {}
    root = d.get("Root", d)   # D3's in_archive, copied: Root -> StatewideSummary -> Race
    rows = (root.get("StatewideSummary") or {}).get("Race") or []
    rows = rows if isinstance(rows, list) else [rows]
    for r in rows:
        mt = re.search(r"District 0*(\d+)$", r["OFFICE_TITLE"].strip())
        cs = (r.get("Candidates") or {}).get("Candidate") or []
        if mt:
            out[mt.group(1)] = [(first_last(x["NAME_ON_BALLOT"].replace("(W/I)", "").strip()), int(x.get("TOTAL") or 0), "(W/I)" in x["NAME_ON_BALLOT"]) for x in (cs if isinstance(cs, list) else [cs])]
    return out, d


def name_key(n):
    """The surname, from 'last, first m (nick)' (Klarner) or 'First M. Last' (the archive, after first_last; a suffix dropped).
    The archive prints nicknames where Klarner prints given names (Tim/Timothy, Jim/James, J.d./James), so the pairing here is
    by surname within the district, where every surname is single [measured]."""
    s = re.sub(r"\(.*?\)|\"[^\"]*\"", " ", n.upper())
    s = re.sub(r"[^A-Z, ]", " ", s)
    if "," in s:
        last = s.split(",", 1)[0]
        last = last.split()[-1] if last.split() else ""
    else:
        toks = [t for t in s.split() if t not in C48.NOT_GIVEN]
        last = toks[-1] if toks else ""
    return last.strip()


def section_6():
    h1("49.6 Indiana 2018's Senate from the state's archive, read again (fetch_eighth_pass.sh in_2018), against the records")
    with open(os.path.join(IN2018, "settings.json"), encoding="utf-8-sig") as f:
        st = json.load(f)
    root = st.get("Root", st)
    cert = root.get("Certified")
    print(f"  settings.json: Root.Certified = {cert!r} (D3: \"Certified\":\"T\", the mark 15:16 asks for); WriteTime {root.get('WriteTime')}, CurrentElection {root.get('CurrentElection')}, ElectionType {root.get('ElectionType')}; keys {[k for k in root if not isinstance(root[k], (dict, list))][:14]}")
    with open(os.path.join(IN2018, "statewideElectionsC_A.json"), encoding="utf-8-sig") as f:
        cats = json.load(f)
    def walk(o, acc):
        if isinstance(o, dict):
            if str(o.get("OFFICE_CATEGORY_ID", o.get("OfficeCategoryID", ""))) == "2180" or any(str(v) == "2180" for v in o.values() if not isinstance(v, (dict, list))):
                acc.append({k: v for k, v in o.items() if not isinstance(v, (dict, list))})
            for v in o.values():
                walk(v, acc)
        elif isinstance(o, list):
            for v in o:
                walk(v, acc)
    acc = []
    walk(cats, acc)
    print(f"  the office list: entries naming 2180: {acc[:2]} (D3: office category 2180, 'State Senator')")
    sen, raw = in_archive_senate()
    mine_sha = sha256(os.path.join(IN2018, "OffCatC_2180_A.json"))
    print(f"  the State Senator file: {len(sen)} districts (D3: 25); my sha256 {mine_sha[:16]}... {'equal to' if mine_sha == IN2018_SHA else 'DIFFERS from'} the records' state_agrees.sha256 {IN2018_SHA[:16]}...")
    recs = records_at(AFTER, "data/state-upper/2018/IN.json")
    recs_b = records_at(BEFORE, "data/state-upper/2018/IN.json")
    by_d = {str(int(r["place"]["district"])): r for r in recs.values() if str(r["place"]["district"]).isdigit()}
    tal = collections.Counter()
    for dno, cands in sorted(sen.items(), key=lambda kv: int(kv[0])):
        r = by_d.get(dno)
        if r is None:
            tal["no record"] += 1
            continue
        rk = {name_key(c["name"]): c["votes"] for c in r["result"]["candidates"] if c.get("party") != "write-in"}
        ak = {name_key(n): v for n, v, wi in cands if not wi}
        eq = rk == ak
        tal["every named candidate equal to the vote" if eq else "DIFFERS"] += 1
        tal[("names on the ballot", len(rk), "=", len(ak))] += 1
        if not eq or dno in ("29", "31", "47"):
            print(f"    district {dno}: archive {[(n, v) for n, v, wi in cands]}; record {[(c['name'], c['votes']) for c in r['result']['candidates']]}; "
                  f"{'equal' if eq else 'DIFFER: ' + str((rk, ak))}; p before {pval(recs_b.get(r['id'], {}))} after {pval(r)}")
    print(f"  the archive's districts against the records' counts (Klarner's), candidate by candidate by surname and given name: {dict(tal)}")
    suffix = [n for cands in sen.values() for n, v, wi in cands if re.search(r"\b(JR|SR|II|III|IV)\b", n, re.I)]
    raw_rows = ((raw.get("Root", raw).get("StatewideSummary") or {}).get("Race") or [])
    raw_suffix = [x["NAME_ON_BALLOT"] for row in raw_rows for cs_ in [(row.get("Candidates") or {}).get("Candidate") or []]
                  for x in (cs_ if isinstance(cs_, list) else [cs_]) if "," in x["NAME_ON_BALLOT"]]
    print(f"  names with a suffix after first_last (D3's rule copied): {suffix}; names holding a comma in the raw file: {raw_suffix}")
    for dno in ("29", "31", "47"):
        r = by_d[dno]
        notes = r.get("notes") or []
        m = next((re.search(r"\((https://enr\.indianavoters\.in\.gov/\S+), read (\S+), sha256 ([0-9a-f]{64}): (.*?)\), so Klarner's count stands", n) for n in notes if "OffCatC_2180" in n), None)
        print(f"  Senate {dno}: the note's url {m.group(1) if m else None}, read {m.group(2) if m else None}, sha256 {'mine' if m and m.group(3) == mine_sha else 'DIFFERS'}; pairs: {m.group(4)[:160] if m else None}; "
              f"certified words {'present' if any('bear a certified mark' in n for n in notes) else 'ABSENT'}; before: p {pval(recs_b.get(r['id'], {}))}, {str((recs_b.get(r['id'], {}).get('p') or {}).get('not_computed'))[:60]}; "
              f"notes before {len(recs_b.get(r['id'], {}).get('notes') or [])}, after {len(notes)}")
    chk = L.load_json(at(AFTER, "data/local/check-districts.json"))
    fl = [f for f in chk["years"]["2018"]["flags"] if f["id"].startswith("2018-IN-")]
    print(f"  D3's Indiana 2018 flags: {len(fl)}: outcomes {dict(collections.Counter((f['id'].split('-')[2], f.get('outcome', '')[:50]) for f in fl))}")
    print(f"  the House file (OffCatC for State Representative) is not read here: D3 did not read it (a second request), and the orchestrator's allowance named one file")


# ------------------------------------------------------------------------------------------ 49.7 route (a)

def section_7():
    h1("49.7 Route (a) refitted at both commits (c40's rows and fits; Indiana 2018's rows from the records, so that Senate 47 joins as the records have it)")
    wb, wa = C41.worktree(BEFORE), C41.worktree(AFTER)
    override = ((2022, "NH"), (2022, "ID"), (2018, "IN"))
    rb, ab = C40.fit_rows_at(wb, override)
    ra, aa = C40.fit_rows_at(wa, override)
    print(f"  fit rows before {len(rb):,} (from the records: {sum(ab.values())}), after {len(ra):,} (from the records: {sum(aa.values())}); rows that differ by (year, state, source): "
          + ", ".join(f"{k} {aa.get(k, 0) - ab.get(k, 0):+d}" for k in sorted(set(ab) | set(aa)) if aa.get(k, 0) != ab.get(k, 0)))
    in18 = {c: sorted((r_["id"], r_["y"]) for r_ in rows if r_["year"] == 2018 and r_["state"] == "IN" and r_["sen"] == 1 and r_.get("from_record")) for c, rows in (("before", rb), ("after", ra))}
    print(f"  Indiana 2018's Senate rows from the records: before {len(in18['before'])}, after {len(in18['after'])}; added: {[i for i in in18['after'] if i not in in18['before']]}")
    for c, rows in (("before", in18["before"]), ("after", in18["after"])):
        ys = [y for _, y in rows]
        print(f"    the chamber's lean from them (mean Democratic share - 0.5): {c} {sum(ys) / len(ys) - 0.5:+.4f} over {len(ys)} races (D3: Senate 9's lean -0.0699 -> -0.0749)")
    in20 = {i: (r.get("forecast_inputs") or {}).get("lean") for i, r in records_at(AFTER, "data/state-upper/2020/IN.json").items()}
    in20b = {i: (r.get("forecast_inputs") or {}).get("lean") for i, r in records_at(BEFORE, "data/state-upper/2020/IN.json").items()}
    print(f"    the Indiana 2020 Senate records' lean: before {set(in20b.values())}, after {set(in20.values())}")
    years = sorted({r["year"] for lv in ("state-upper", "state-lower", "local") for r in C40.rows_at(wa, lv) if r["status"] == "value" and r["route"] == "partisan"} & set(range(2019, 2026)))
    years = sorted(set(years) | {2018})   # 2018's fit (on the years before it) for Senate 47's own p
    fb, fa = C40.fits_for(rb, years), C40.fits_for(ra, years)
    print(f"  fits for {years}; the fit's coefficients after against before: " + ", ".join(f"{k} {fa[2024]['coef'][k] - fb[2024]['coef'][k]:+.2e}" for k in fa[2024]["coef"]) if fa.get(2024) and fb.get(2024) else "")
    mv = L.load_json(at(AFTER, "data/local/moves-36.json"))
    prow = {r[0]: r for r in mv["records"] if "P" in r[8]}
    before_by = {}
    for lv in ("state-upper", "state-lower", "local"):
        for r in C40.rows_at(wb, lv):
            before_by[r["id"]] = r
    tal = collections.Counter()
    diffs = []
    n_mine = 0
    unlisted = []
    for lv in ("state-upper", "state-lower", "local"):
        for r in C40.rows_at(wa, lv):
            if r["status"] != "value" or r["route"] != "partisan":
                continue
            r0 = before_by.get(r["id"])
            if r0 is None or r0["status"] != "value":
                if r["id"] in prow or r["id"] == "2018-state-upper-IN-47":
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
            tal[(lv, str(r["year"]) if lv == "local" else "", band, "same direction" if same_dir else "opposite")] += 1
            n_mine += 1
            if band in ("within 5e-2", "beyond 5e-2") or not same_dir:
                diffs.append((d, r["id"], mine, theirs))
    print(f"  the file's partisan P rows with a p of mine before and after: {n_mine:,}; my ratio against the file's:")
    for k_, v in sorted(tal.items(), key=str):
        print(f"    {str(k_):90s} {v:,}")
    diffs.sort(key=lambda x: -x[0])
    for d, rid, mine, theirs in diffs[:10]:
        print(f"    {rid}: mine x{mine:.4f}, file x{theirs:.4f}")
    if unlisted:
        print(f"  records my refit moves beyond 5e-4 that the file does not list as P: {len(unlisted)} {unlisted[:8]}")
    # the Indiana 2020 Senate moves, mine
    for i in sorted(in20):
        r = next((x for x in C40.rows_at(wa, "state-upper") if x["id"] == i), None)
        r0 = before_by.get(i)
        if r and r0 and r["status"] == "value" and r0["status"] == "value" and r["route"] == "partisan":
            p0, _ = C40.p_of_record(wb, r0, fb)
            p1, _ = C40.p_of_record(wa, r, fa)
            row = prow.get(i)
            if p0 and p1:
                print(f"    {i}: lean {in20b.get(i)} -> {in20.get(i)}; mine x{p1 / p0:.4f}; the file x{row[7] if row else None}")


# ------------------------------------------------------------------------------------------ 49.8 the reasons, notes and gates

def section_8():
    h1("49.8 The reasons, notes and gates changed (R, Q, O rows), and D2's files")
    diff, data_files, d2_files, other, stamps = my_diff()
    print(f"  D2's files (governor, house, senate, president) in the diff: {d2_files} (D3: no governor, House, Senate or president record moves)")
    # the fields themselves, whatever the record's first code (D3's rows carry several codes; mine one): Virginia 2023's gates and notes
    gates, notes_k, reasons = collections.Counter(), collections.Counter(), collections.Counter()
    for i, (c, lv, yr, b, a, d) in diff.items():
        if not b or not a:
            continue
        if (b.get("gate") or {}) != (a.get("gate") or {}):
            gates[(lv, yr, tuple(sorted(k for k in set(b.get("gate") or {}) | set(a.get("gate") or {}) if (b.get("gate") or {}).get(k) != (a.get("gate") or {}).get(k))))] += 1
        na = [n for n in (a.get("notes") or []) if n not in (b.get("notes") or [])]
        for n in na:
            notes_k[(lv, yr, "nonpartisan note (the Code quoted)" if n.startswith("nonpartisan: the Code") else "unopposed comparator named" if "unopposed (an unopposed contest loses" in n
                     else "Indiana 2018's archive" if "OffCatC_2180" in n else "other: " + n[:50])] += 1
        if (b.get("p") or {}).get("not_computed") != (a.get("p") or {}).get("not_computed") and (b.get("p") or {}).get("not_computed") and (a.get("p") or {}).get("not_computed"):
            reasons[(lv, yr)] += 1
    print(f"  records whose gate changed, by (level, year, fields): {dict(gates)} (D3: 690 Virginia 2023 local records and 9 questions, gate.ruled now 00:55 (a) and (b); every Virginia 2023 record carries the gate)")
    print(f"  notes added, by kind: {dict(notes_k)} (D3: 388 nonpartisan, 10 unopposed comparators, Indiana's Senate 29, 31 and 47)")
    print(f"  reasons changed (not computed before and after): {dict(reasons)} (D3: 364 + 207 + 17 = 588)")
    for code in ("R", "Q", "O", "B", "T", "G", "I"):
        rows = [(i, lv, yr, b, a, d) for i, (c, lv, yr, b, a, d) in diff.items() if c == code]
        if not rows:
            continue
        print(f"\n  {code}: {len(rows):,} by (level, year, state): {dict(collections.Counter((lv, yr, i.split('-')[3] if lv.startswith('state') else i.split('-')[2]) for i, lv, yr, b, a, d in rows))}")
        if code == "R":
            kinds = collections.Counter()
            for i, lv, yr, b, a, d in rows:
                nb, na = (b.get("p") or {}).get("not_computed", ""), (a.get("p") or {}).get("not_computed", "")
                k = ("LA 2023: the odd-year note names Louisiana's alone and Virginia's no party" if "Louisiana's alone (Virginia's local offices print no party" in na
                     else "VA 2023: section 24.2-613 B named" if "section 24.2-613 B" in na and "section 24.2-613 B" not in nb
                     else "VA 2023: held before, too few like races now" if "held" in nb and "fewer than" in na
                     else "2024 school boards: the like-race count changed" if "fewer than" in nb and "fewer than" in na
                     else f"other: {nb[:40]} -> {na[:40]}")
                kinds[(yr, k)] += 1
            for k_, v in sorted(kinds.items()):
                print(f"    {k_}: {v}")
            ex = [(i, (b.get("p") or {}).get("not_computed", "")[-120:], (a.get("p") or {}).get("not_computed", "")[-160:]) for i, lv, yr, b, a, d in rows if "2024" in yr and "school" in i.lower()][:2]
            print(f"    e.g. 2024 school boards: {ex}")
            la = [(i, (a.get('p') or {}).get('not_computed', '')[-170:]) for i, lv, yr, b, a, d in rows if yr == "2023" and "-LA-" in i][:1]
            print(f"    e.g. Louisiana: {la}")
        if code == "Q":
            kinds = collections.Counter()
            for i, lv, yr, b, a, d in rows:
                na = [n for n in (a.get("notes") or []) if n not in (b.get("notes") or [])]
                k = "nonpartisan note (the Code quoted)" if any(n.startswith("nonpartisan: the Code") for n in na) else \
                    "unopposed comparator named" if any("unopposed (an unopposed contest loses" in n for n in na) else \
                    "Indiana 2018's archive" if any("OffCatC_2180" in n for n in na) else "other: " + str(na)[:60]
                kinds[(yr, k)] += 1
            print(f"    kinds: {dict(kinds)}")
        if code == "O":
            kinds = collections.Counter((yr, tuple(sorted({x.split('.')[0] for x in d}))) for i, lv, yr, b, a, d in rows)
            print(f"    fields: {dict(kinds)}")
            g = [(i, d) for i, lv, yr, b, a, d in rows if any(x.startswith("gate") for x in d)][:1]
            print(f"    e.g. gate: {g}; before {str((diff[g[0][0]][3] or {}).get('gate', {}).get('ruled'))[:120] if g else None}")
        if code == "B":
            kinds = collections.Counter((yr, tuple(sorted({x for x in d if not x.startswith('p.commit')}))[:3]) for i, lv, yr, b, a, d in rows)
            print(f"    what differs: {dict(list(kinds.items())[:8])}")


def main():
    print(f"C49 (section 20): D3's #111, {BEFORE} -> {AFTER}; {L.git_head()}")
    for s in (section_1, section_2, section_3, section_4, section_5, section_6, section_7, section_8):
        s()


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        main()
    else:
        print(f"C49 (section 20): D3's #111, {BEFORE} -> {AFTER}; {L.git_head()}")
        for a in args:
            globals()[f"section_{a}"]()
