"""c47: the eighth pass's section 19, first part: D3's #109 (main b35fede; data/local/REPORT.md section 35) against
b350d5e, the governors' counts and D2's refit, and the fusion scan.

The orchestrator, 2026-11-13 07:38 UTC: "D3's #109 is merged as b35fede (REPORT §35, moves-governor-counts.json). Check it
in section 19, with its end at b35fede. It covers: the governor counts: CT and NY 2018 summed over fusion lines; IN 2024 on
the archive's certified count; UT 2008 settled by the state with Algara-Amlani; MO on the state; WV 2012 held and left out of
the fits and the last-race index, so WV 2016 reads 2011; Senate 36 on MEDSL; the 0.4% two-witness rule (6 IN 2016 records,
House 75 back); over-seats on every covered record ...; the zero-row counties ...; 107 spelling pairs; DC at 231,700. My
compare against main: 1 lost, 9 gained, 14,997 moved, none over 2x. D3's message counts 14,525 moved plus 187 governor;
reconcile the counts in your diff." The district checks' part is c48.

Sections (each from my own reading of the sources, fetched once more by checks/m2/fetch_eighth_pass.sh governors / aa
(Connecticut's page, Utah's 2008 workbook, West Virginia's 2012 page, Algara and Amlani's county file; Missouri's Secretary
of State answered 403 to all three PDFs, so its returns are read from the records' notes alone [stated]), and the records at
the two commits; nothing from pipeline/ imported; a rule of the build that must be applied is copied here and says so):
  47.1  moves-governor-counts.json against my own diff of every governor, House and Senate record, b350d5e -> b35fede
        (c41's coder), the files' blocks; the counts reconciled (14,997 = 14,525 + 126 + 346; D3's 187)
  47.2  the counts against the sources read apart: Connecticut's page (its Next.js data), Utah's workbook (xlrd), West
        Virginia's page, Indiana's archive, Algara and Amlani's Rdata (my own reader, checks/m2/m2rdata.py, the md5 the
        dataset lists), MEDSL's lines from my summaries; each record's candidates, lines, total, two_party, n, the p
        scaled (density: event = f_half / n, copied from governor_counts.fix_record), the last-race inputs
        (Connecticut and New York 2022, Utah's 2010 special, West Virginia 2016 -> the 2011 special)
  47.3  my own refit (m2fit's rows: the four counts applied, West Virginia 2012 out, its 2016 lag the 2011 special's)
        against the blocks before and after; the ratio of every moved governor p; the House's and Senate's p of record
  47.4  the fusion scan: every record's lines against its votes, the counts by level against check-fusion.json; Klarner's
        lines from his candidate file; the governor second count (198 compared, 6 listed) from my own A&A sums
[measured] throughout unless marked; D3's words [stated].
Run from the repository root: python3 -I checks/m2/c47_governor_counts.py [1 2 3 4]
"""
import collections
import copy
import csv
import glob
import hashlib
import html
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402
import m2fit as F  # noqa: E402
import m2medsl as M  # noqa: E402
import m2rdata  # noqa: E402
import c41_governor_refit as C41  # noqa: E402
import c42_held_totals as C42  # noqa: E402
from c9_fit2 import RECORD_VARIANT  # noqa: E402

BEFORE, AFTER = "b350d5e", "b35fede"
SRC = os.path.join(L.CACHE, "eighth", "src")
AA_FILE = os.path.join(SRC, "aa", "dataverse_shareable_gubernatorial_county_returns_1865_2020.Rdata")
AA_MD5 = "aad6adc36018578244edc77a7f520c41"   # the dataset's JSON (aa/dataset.json), file 5028535
CT_PAGE = os.path.join(SRC, "ct_sots", "contest_3781.html")
UT_XLS = os.path.join(SRC, "ut_lg", "2008Gen.xls")
WV_PAGE = os.path.join(SRC, "wv_sos", "results_2012_eid13_statewide.html")
IN_ENR = os.path.join(L.CACHE, "seventh", "in_enr")   # the 2024 archive, read in the seventh pass (index.txt there)
KLARNER_CANDS = os.path.join(SRC, "klarner", "127_slers_1967to2022_forsharing20230810.csv")
OWN = "the model's own"
TERMS = ("b_lean", "b_inc", "b_lag", "s_e", "s_a", "c0", "c1", "c2", "k")

# the counts D3 took (REPORT section 35; governor_counts.FIX), as (Democrat, Republican) of the deciding pair [stated]
NEW_COUNTS = {"2018-governor-CT": (694510, 650138), "2018-governor-NY": (3635340, 2207602),
              "2024-governor-IN": (1183741, 1566081), "2008-governor-UT": (186503, 734049)}
HELD = {"2012-governor-WV"}   # out of the fits and of the last-race index


def h1(s):
    print("\n" + "=" * 100 + f"\n{s}\n" + "=" * 100)


def at(commit, rel):
    return os.path.join(C41.worktree(commit), rel)


def records_at(commit, f):
    return C42.records_at(C41.worktree(commit), f)


def gov_record(commit, cid):
    return records_at(commit, f"data/governor/{cid[:4]}.json").get(cid)


def pv(c):
    return C41.pval(c)


def rel(a, b):
    if a is None or b is None:
        return None
    return abs(a - b) / max(abs(b), 1e-12)


# ------------------------------------------------------------------------------------------ 47.1 the moves file

def plain(code):
    return code.split(":")[0]


def section_1():
    h1(f"47.1 moves-governor-counts.json against my own diff of every governor, House and Senate record, {BEFORE} -> {AFTER}")
    mv = L.load_json(at(AFTER, "data/local/moves-governor-counts.json"))
    rows = {r[0]: r for r in mv["records"]}
    print(f"  the file: {len(mv['records']):,} rows ({len(rows):,} ids), against {mv['against']} (the code alone; its data main's at 72d1d60, which equal "
          f"{BEFORE}'s D2 files: my diff is main to main); stamp_only {mv.get('stamp_only')}; columns {mv['columns']}")
    print(f"  its codes: {json.dumps(mv['codes'])}")
    files = subprocess.run(["git", "diff", "--name-only", BEFORE, AFTER, "--", "data/governor", "data/house", "data/senate", "data/president"],
                           capture_output=True, text=True, cwd=L.ROOT).stdout.split()
    print(f"  D2 data files changed: {len(files)} " + str(dict(collections.Counter(f.split('/')[1] for f in files))))
    mine, agree, dis, unlisted, examples = collections.Counter(), 0, collections.Counter(), collections.Counter(), []
    pdiff, rdiff, bdiff, seen, stamp_only = 0, 0, 0, set(), 0
    blocks_mine = {}
    lv_codes = collections.Counter()
    for f in files:
        lv = f.split("/")[1]
        db = json.load(open(at(BEFORE, f)))
        da = json.load(open(at(AFTER, f)))
        b = {c["id"]: c for c in db["contests"]}
        a = {c["id"]: c for c in da["contests"]}
        hb = {k: v for k, v in db.items() if k != "contests"}
        ha = {k: v for k, v in da.items() if k != "contests"}
        dl = C41.diff_leaves(hb, ha)
        if dl:
            blocks_mine[f] = dl
        for i in sorted(set(b) | set(a)):
            code = C41.my_codes(b.get(i), a.get(i))
            if not code:
                if C41.diff_leaves(b.get(i), a.get(i)) == [] and json.dumps(b.get(i), sort_keys=True) != json.dumps(a.get(i), sort_keys=True):
                    stamp_only += 1
                continue
            seen.add(i)
            mine[(lv, ",".join(code))] += 1
            for c_ in code:
                lv_codes[(lv, c_)] += 1
            row = rows.get(i)
            if row is None:
                unlisted[(lv, ",".join(code))] += 1
                if len(examples) < 6:
                    examples.append((i, code, "not in the file", [k for k, _, _ in C41.diff_leaves(b.get(i), a.get(i))][:5]))
                continue
            theirs = [plain(x) for x in row[7]]
            same = set(code) == set(theirs) or (set(code) - {"B", "F", "O"}) == (set(theirs) - {"B", "F", "O"})
            if same:
                agree += 1
            else:
                dis[(lv, ",".join(code), ",".join(theirs))] += 1
                if len(examples) < 12:
                    examples.append((i, code, theirs, [k for k, _, _ in C41.diff_leaves(b.get(i), a.get(i))][:6]))
            pb, pa = pv(b.get(i)), pv(a.get(i))
            if (row[3] is None) != (pb is None) or (row[4] is None) != (pa is None) \
                    or (pb is not None and abs(row[3] - pb) > 1e-9 * max(abs(pb), 1e-300)) \
                    or (pa is not None and abs(row[4] - pa) > 1e-9 * max(abs(pa), 1e-300)):
                pdiff += 1
                if pdiff <= 3:
                    print(f"    p before/after differ from the record: {i} row {row[3]} {row[4]} record {pb} {pa}")
            if pb and pa and row[5] is not None and abs(row[5] - pa / pb) > 1.5e-6 * max(1.0, abs(row[5])) + 6e-7:
                rdiff += 1
                if rdiff <= 3:
                    print(f"    ratio off the record's: {i} row {row[5]} record {pa / pb:.6f}")
            bb, ba = C41.beside(b.get(i)), C41.beside(a.get(i))
            mine_r = [round(y / x, 6) if x else None for x, y in zip(bb, ba)]
            if len(row[6]) != len(mine_r) or any(m_ is None or t_ is None or abs(m_ - t_) > 1.5e-6 for m_, t_ in zip(mine_r, row[6])):
                bdiff += 1
                if bdiff <= 3:
                    print(f"    the p beside's ratios differ: {i} row {row[6]} mine {mine_r}")
    listed_not_mine = [i for i in rows if i not in seen]
    print("  my diff, by level and codes: " + "; ".join(f"{lv} {k} {v}" for (lv, k), v in sorted(mine.items())))
    print(f"  records whose only difference is a stamp (commit, read_utc), left out as the file does: {stamp_only:,} (the file's stamp_only {mv.get('stamp_only')})")
    print(f"  rows whose codes I share (B, F and O read as one kind): {agree:,} of {len(seen):,} ids in my diff; differing: {sum(dis.values())}; "
          f"ids in my diff but not in the file: {sum(unlisted.values())} {dict(unlisted) if unlisted else ''}; in the file but not in my diff: "
          f"{len(listed_not_mine)} {listed_not_mine[:5]}")
    print(f"  p before/after other than the record's: {pdiff}; ratios off the record's: {rdiff}; the p beside's ratios off: {bdiff}")
    for (lv, mc, tc), v in sorted(dis.items(), key=lambda kv: -kv[1])[:8]:
        print(f"    mine {mc} theirs {tc} {lv}: {v}")
    for e in examples[:8]:
        print(f"    e.g. {e[0]}: mine {e[1]}, theirs {e[2]}; differs in {e[3]}")
    # the counts, reconciled
    theirs_lv = collections.Counter()
    for r in mv["records"]:
        lv = r[1].split("/")[1]
        for c_ in r[7]:
            theirs_lv[(lv, plain(c_))] += 1
    print("\n  the counts (the orchestrator, 07:38: 'My compare against main: 1 lost, 9 gained, 14,997 moved'; D3's message: '14,525 moved plus 187 governor'):")
    print(f"    the file's P (p of record moved), by level: {dict((lv, theirs_lv[(lv, 'P')]) for lv in ('governor', 'house', 'senate') if theirs_lv[(lv, 'P')])}; "
          f"mine: {dict((lv, lv_codes[(lv, 'P')]) for lv in ('governor', 'house', 'senate') if lv_codes[(lv, 'P')])}")
    print(f"    the file's L: {dict((lv, theirs_lv[(lv, 'L')]) for lv in ('governor', 'house', 'senate') if theirs_lv[(lv, 'L')])} (mine X/L {dict((lv, lv_codes[(lv, 'X')]) for lv in ('governor', 'house', 'senate') if lv_codes[(lv, 'X')])}); "
          f"the file's A (a p beside moved) without P: {dict((lv, len([r for r in mv['records'] if r[1].split('/')[1] == lv and 'A' in r[7] and 'P' not in r[7]])) for lv in ('governor', 'house', 'senate'))}")
    gov_p = theirs_lv[("governor", "P")]
    gov_pa = len([r for r in mv["records"] if r[1].startswith("data/governor") and ("P" in r[7] or "A" in r[7]) and "L" not in r[7]])
    mv3 = L.load_json(at(AFTER, "data/local/moves-district-checks-3.json"))
    p3 = collections.Counter(r[1].split("/")[1] for r in mv3["records"] if "P" in r[8])
    n3 = collections.Counter(r[1].split("/")[1] for r in mv3["records"] if "N" in r[8])
    l3 = collections.Counter(r[1].split("/")[1] for r in mv3["records"] if "L" in r[8])
    print(f"    moves-district-checks-3.json: P by level {dict(p3)} = {sum(p3.values()):,}; N {dict(n3)} = {sum(n3.values())}; L {dict(l3)}")
    print(f"    so: D3's 14,525 = the district file's P; the orchestrator's 14,997 = {sum(p3.values()):,} + governor P {gov_p} + House P {theirs_lv[('house', 'P')]} = "
          f"{sum(p3.values()) + gov_p + theirs_lv[('house', 'P')]:,}; his 1 lost = West Virginia 2012 (L); his 9 gained = the district file's N ({sum(n3.values())})")
    print(f"    D3's '187 governor p of record move' (REPORT section 35) = the governor rows with P or A, the L row (West Virginia 2012, which carries A too) aside: {gov_pa} = P {gov_p} + A without P "
          f"{gov_pa - gov_p} (the 2018 and 2022 records whose p of record is 538's, unchanged, and whose model's-own p beside moved); "
          f"the p of record that moved are {gov_p}, so the section's '187' counts the p beside too [measured]")
    moved = [r for r in mv["records"] if "P" in r[7] and r[1].startswith("data/governor")]
    rs = sorted((r[5], r[0]) for r in moved if r[5] is not None)
    over1 = [(r[0], r[5]) for r in moved if r[5] is not None and abs(r[5] - 1) > 0.01]
    print(f"    the governor P rows' ratios: from {rs[0][0]} ({rs[0][1]}) to {rs[-1][0]} ({rs[-1][1]}); beyond 1%: {len(over1)} {sorted(over1, key=lambda x: x[1])}; "
          f"within 1%: {len(moved) - len(over1)} (D3: '170 of the 187 are within 1%': 170 = {len(moved) - len(over1)} P within 1% + the {gov_pa - gov_p} A-only rows: "
          f"{len(moved) - len(over1) + gov_pa - gov_p == 170}); over 2x either way: {[r[0] for r in moved if r[5] is not None and (r[5] > 2 or r[5] < 0.5)]}")
    hs = [r for r in mv["records"] if "P" in r[7] and not r[1].startswith("data/governor")]
    worst = max((abs(r[5] - 1), r[0]) for r in hs) if hs else None
    print(f"    the House's and Senate's P rows: {len(hs)} ({dict(collections.Counter(r[1] for r in hs))}); the largest move {worst[0]:.2e} ({worst[1]}) "
          f"(D3: 'by 0.002% at most'): {'holds' if worst and worst[0] <= 2e-5 else 'the largest is 0.0021%, D3 rounded'}")
    # the files' own blocks
    fb = mv.get("file_blocks") or {}
    print(f"\n  the files' own blocks: the file lists {len(fb)}; my diff finds {len(blocks_mine)} files with a block leaf changed; "
          f"same set: {set(fb) == set(blocks_mine)}; mine not theirs {sorted(set(blocks_mine) - set(fb))[:5]}; theirs not mine {sorted(set(fb) - set(blocks_mine))[:5]}")
    kinds = collections.Counter()
    for f, dl in sorted(blocks_mine.items()):
        kinds[(f.split("/")[1], tuple(sorted({re.sub(r"\[\d+\]", "[]", k.split(".")[0] + ("." + k.split(".")[1] if "." in k else "")) for k, _, _ in dl})))] += 1
    for (lv, ks), v in sorted(kinds.items()):
        print(f"    {lv}: {v} file(s) differ in {list(ks)[:8]}")
    for f in ("data/governor/2014.json", "data/governor/2020.json", "data/governor/2024.json"):
        if f in blocks_mine:
            print(f"    {f}: " + "; ".join(f"{k} {vb!s:.10} -> {va!s:.10}" for k, vb, va in blocks_mine[f] if k.startswith("model.") and not k.startswith("model.ZtZ"))[:700])
    return mv


# ------------------------------------------------------------------------------------------ 47.2 the counts

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetched(key):
    idx = os.path.join(SRC, "index.txt")
    for line in open(idx):
        p = line.rstrip("\n").split("\t")
        if p and p[0] == key:
            return p
    return None


def ct_page():
    """The contest's data as the page serves it (its Next.js __NEXT_DATA__ JSON): each candidate's votes and lines."""
    s = open(CT_PAGE, encoding="utf-8", errors="replace").read()
    m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', s, re.S)
    d = json.loads(m.group(1))
    contest = d["props"]["pageProps"]["contest"]
    cands, totals = [], []
    for c in contest["candidates"]:
        if (c.get("candidate") or {}).get("pseudocandidate"):   # the page's own total rows ('Total Votes Cast', 'Total Ballots Cast')
            totals.append((c["displayName"], c["nVotes"]))
            continue
        lines = []
        for k in ("party", "party2", "party3", "party4"):
            if c.get(k):
                n = int(k[5:] or 1)
                v = c.get(f"nVotesParty{n}")
                lines.append((c[k]["name"], v if v is not None else (c["nVotes"] if n == 1 and not c.get("party2") else None)))
        cands.append({"name": c["displayName"], "votes": c["nVotes"], "lines": lines, "write_in": c.get("isWriteIn"), "winner": c.get("isWinner"),
                      "pseudo": (c.get("candidate") or {}).get("pseudocandidate")})
    text = re.sub(r"<[^>]+>", " ", s)
    text = html.unescape(re.sub(r"\s+", " ", text))
    words = {w: (w in s or w in text) for w in ("Statement of Vote 2018", "Official Sources", "data entry errors that have been preserved",
                                               "discrepancies in precinct reporting in the Town of Woodstock")}
    # the total the page carries
    totals_int = {k: v for k, v in contest.items() if isinstance(v, int) and v > 1000}
    nested = re.findall(r'"(\w*[Tt]otal\w*)":(\d+)', m.group(1))
    return {"contest": {k: contest.get(k) for k in ("id", "nSeats", "verifiedAt", "eventTypeDisplayName", "hasWinners")},
            "office": contest["office"]["name"], "event_date": contest["event"]["startDate"], "division": contest["division"]["displayName"],
            "candidates": cands, "words": words, "totals": totals, "ints": totals_int, "totals_named": nested[:10], "sum": sum(c["votes"] for c in cands)}


def ut_xls():
    import xlrd
    wb = xlrd.open_workbook(UT_XLS)
    sh = next(s for s in wb.sheets() if s.name.strip().lower() == "governor")
    head = None
    for i in range(sh.nrows):
        row = [sh.cell_value(i, j) for j in range(sh.ncols)]
        if any(isinstance(c, str) and c.strip().upper() == "COUNTY" for c in row):
            head = row
        if any(isinstance(c, str) and c.strip().lower() == "total" for c in row):
            total = row
    cols = {str(h).strip(): total[j] for j, h in enumerate(head) if str(h).strip()}
    marks = collections.Counter()
    for s in wb.sheets():
        for i in range(s.nrows):
            for j in range(s.ncols):
                v = s.cell_value(i, j)
                if isinstance(v, str):
                    for w in ("certif", "official", "canvass", "abstract"):
                        if w in v.lower():
                            marks[(s.name, w)] += 1
    counties = sum(1 for i in range(sh.nrows) if isinstance(sh.cell_value(i, 0), str) and sh.cell_value(i, 0).strip() and sh.cell_value(i, 0).strip().lower() not in ("county", "total"))
    return {"sheets": [s.name for s in wb.sheets()], "sheet": sh.name, "header": [str(h) for h in head], "total_row": cols, "county_rows": counties,
            "marks": dict(marks)}


def wv_page():
    s = open(WV_PAGE, encoding="utf-8", errors="replace").read()
    text = re.sub(r"[\s\xa0]+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s)))
    i = text.find("Governor Contest Code")
    if i < 0:
        i = text.find("EARL RAY TOMBLIN") - 100
    seg = text[i:i + 800]
    cands = re.findall(r"([A-Z][A-Z .']+?) (Democrat|Republican|Mountain|Libertarian|Independent|Constitution) ([\d,]+) ([\d.]+)%", seg)
    tot = re.search(r"Official Total Votes: ([\d,]+)", seg)
    words = {w: (w in text) for w in ("should not be relied on as official results until certified", "Results do not include write-in candidate information",
                                      "Official Results")}
    prec = re.search(r"Number of Precincts (\d+) Number of Precincts Reporting (\d+)", text)
    return {"candidates": [(n.strip(), p, int(v.replace(",", "")), float(pc)) for n, p, v, pc in cands], "official_total": int(tot.group(1).replace(",", "")) if tot else None,
            "words": words, "precincts": (int(prec.group(1)), int(prec.group(2))) if prec else None, "heading_stars": "★★★ Official Results ★★★" in text or "Official Results" in text,
            "segment": seg[:400]}


def in_archive_2024():
    d = json.load(open(os.path.join(IN_ENR, "OffCatC_1007_A.json"), encoding="utf-8-sig"))
    d = d.get("Root", d)
    races = (d.get("StatewideSummary") or {}).get("Race") or []
    races = races if isinstance(races, list) else [races]
    r = next(r for r in races if "Governor" in r.get("OFFICE_TITLE", ""))
    cs = (r.get("Candidates") or {}).get("Candidate") or []
    st = json.load(open(os.path.join(IN_ENR, "settings.json"), encoding="utf-8-sig"))
    st = st.get("Root", st)
    return {"office": r["OFFICE_TITLE"], "candidates": [(x["NAME_ON_BALLOT"].strip(), x.get("PARTY"), int(x.get("TOTAL") or 0), "(W/I)" in x["NAME_ON_BALLOT"]) for x in (cs if isinstance(cs, list) else [cs])],
            "settings": {k: st.get(k) for k in ("Certified", "CurrentElection", "WriteTime")}, "write_time": d.get("WriteTime")}


_AA = {}


def aa():
    """Algara and Amlani's data frame, read by my own reader; cached in the process."""
    if not _AA:
        md5 = hashlib.md5(open(AA_FILE, "rb").read()).hexdigest()
        d = m2rdata.load(AA_FILE)
        df = d["gov_elections_release"]
        _AA["md5"] = md5
        _AA["df"] = df
        _AA["objects"] = list(d)
        cols = df["data"]
        idx = collections.defaultdict(list)
        for i in range(df["nrow"]):
            idx[(int(cols["election_year"][i]), cols["state"][i], cols["election_type"][i])].append(i)
        _AA["idx"] = idx
    return _AA


def aa_sums(year, st, etype="G"):
    """(D, R, counties, dem nominee, rep nominee, total of the county totals) summed over the state's county rows."""
    a = aa()
    cols = a["df"]["data"]
    rows = a["idx"].get((year, st, etype), [])
    if not rows:
        return None
    D = sum(cols["democratic_raw_votes"][i] or 0 for i in rows)
    R = sum(cols["republican_raw_votes"][i] or 0 for i in rows)
    T = sum(cols["raw_county_vote_totals"][i] or 0 for i in rows)
    return {"D": int(D), "R": int(R), "counties": len(rows), "dem": collections.Counter(cols["dem_nominee"][i] for i in rows).most_common(1)[0][0],
            "rep": collections.Counter(cols["rep_nominee"][i] for i in rows).most_common(1)[0][0], "total": int(T),
            "missing_D": sum(1 for i in rows if cols["democratic_raw_votes"][i] is None), "missing_R": sum(1 for i in rows if cols["republican_raw_votes"][i] is None)}


def medsl_governor(year, st):
    """MEDSL's governor lines from my volume summary (every line of a candidate summed under the name): {name: votes}, counties."""
    for y, path in M.all_raw_files():
        if y != year or not os.path.basename(path).lower().startswith(f"{year}-{st.lower()}-"):
            continue
        p = os.path.join(L.CACHE, "fifth", "derived", os.path.basename(path) + ".volume.json")
        if not os.path.exists(p):
            continue
        d = L.load_json(p)
        for key, c in d["contests"].items():
            parts = key.split("|")
            if parts[2] == "GOVERNOR" and parts[3] in ("", "STATEWIDE"):
                return {"cands": c["no_total"] or c["cands"], "counties": len(c.get("counties") or {}) if isinstance(c.get("counties"), dict) else c.get("counties"), "key": key}
    return None


def p_scaled(rec_b, rec_a):
    """D3's scaling, copied from governor_counts.fix_record: each density p's event = f_half / n, value = event / 2; here applied
    to the record before, at the record after's n, against the record after's p (and the p beside)."""
    pb, pa = rec_b["p"], rec_a["p"]
    n_a = pa.get("n")
    out = []
    for xb, xa in zip([pb] + list(pb.get("alongside") or []), [pa] + list(pa.get("alongside") or [])):
        if xb.get("method") != "density" or xa.get("method") != "density":
            out.append((xb.get("under"), "not a density p"))
            continue
        want = xb["f_half"] / n_a / 2
        out.append((xb.get("under", "")[:40], xb["value"], xa["value"], want, abs(want - xa["value"]) <= 1e-9 * max(abs(xa["value"]), 1e-300),
                    xb["f_half"] == xa["f_half"]))
    return out


def section_2():
    h1("47.2 The counts against the sources, read apart: Connecticut's page, Utah's workbook, West Virginia's page, Indiana's archive, Algara and Amlani, MEDSL")
    for k in ("ct:contest3781", "ut:2008gen", "wv:2012statewide", "mo:2008", "mo:2012", "mo:2016", "aa:dataset", "aa:rdata"):
        p = fetched(k)
        print(f"  {k}: http {p[1]} at {p[2]} UTC, {p[6] or '-'} bytes, sha256 {p[5][:16] if p[5] else '-'}..." if p else f"  {k}: not fetched")
    print("  Missouri's Secretary of State answered 403 to each of the three PDFs (one request each, six seconds apart; not asked again): its returns "
          "are read here from the records' notes and D3's REPORT alone [stated]; New York's State Board and Maine's Secretary of State are not asked (refused earlier)")
    a = aa()
    print(f"\n  Algara and Amlani's file: md5 {a['md5']} ({'equals' if a['md5'] == AA_MD5 else 'DIFFERS FROM'} the dataset's listing {AA_MD5}); objects {a['objects']}; "
          f"{a['df']['nrow']:,} rows, columns {a['df']['columns'][:16]}...; election types {dict(collections.Counter(a['df']['data']['election_type']))}; "
          f"years {int(min(a['df']['data']['election_year']))}-{int(max(a['df']['data']['election_year']))}")
    # the records
    recs = {}
    for cid in ("2018-governor-CT", "2018-governor-NY", "2024-governor-IN", "2008-governor-UT", "2012-governor-WV", "2018-governor-HI",
                "2008-governor-MO", "2012-governor-MO", "2016-governor-MO", "2010-governor-ME", "2016-governor-WV", "2022-governor-CT", "2022-governor-NY",
                "2010-governor-UT-special"):
        recs[cid] = (gov_record(BEFORE, cid), gov_record(AFTER, cid))

    def show(cid, src_figs, extra=""):
        b, r = recs[cid]
        print(f"\n  {cid}: {extra}")
        print(f"    before: {[(c['name'], c['party'], c['votes']) for c in b['result']['candidates']]} total {b['result']['total_votes']:,}; source {b['result']['source']['name'][:60]}... mark {b['result']['source'].get('mark')}")
        print(f"    after:  {[(c['name'], c['party'], c['votes'], [(l_['party'], l_['votes']) for l_ in c['lines']] if c.get('lines') else '') for c in r['result']['candidates']]} total {r['result']['total_votes']:,}")
        print(f"            source {r['result']['source']['name'][:90]}...; url {r['result']['source'].get('url')}; mark {str(r['result']['source'].get('mark'))[:120]}")
        print(f"            total = sum of candidates: {r['result']['total_votes'] == sum(c['votes'] for c in r['result']['candidates'])}; lines sum to votes: "
              f"{all(sum(l_['votes'] for l_ in c['lines']) == c['votes'] for c in r['result']['candidates'] if c.get('lines'))}")
        votes_a = {c["name"]: c["votes"] for c in r["result"]["candidates"]}
        agree = {n: (votes_a.get(n), v, votes_a.get(n) == v) for n, v in src_figs.items()}
        print(f"    the source's figures against the record after: {agree}; all equal: {all(x[2] for x in agree.values())}")
        tb, ta = b["two_party"], r["two_party"]
        print(f"    two_party before {tb['votes']} n {tb['n_other_voters']:,} share {tb['share_first']}; after {ta['votes']} n {ta['n_other_voters']:,} share {ta['share_first']}; "
              f"n = sum - 1: {ta['n_other_voters'] == sum(ta['votes']) - 1}; share = first/sum: {abs(ta['share_first'] - ta['votes'][0] / sum(ta['votes'])) < 1e-6}")
        if r["p"].get("value") is not None and b["p"].get("value") is not None:
            sc = p_scaled(b, r)
            print(f"    p: before {b['p']['value']:.6e} (n {b['p'].get('n')}) -> after {r['p']['value']:.6e} (n {r['p'].get('n')}); ratio {r['p']['value'] / b['p']['value']:.6f}; "
                  f"n before/after {b['p'].get('n') / r['p'].get('n'):.6f}; p.n = two_party's n: {r['p'].get('n') == ta['n_other_voters']}")
            for x in sc:
                if len(x) == 2:
                    print(f"      {x}")
                else:
                    print(f"      {x[0]:40s} before {x[1]:.6e} after {x[2]:.6e}; before's f_half at after's n {x[3]:.6e} {'= after' if x[4] else '!= after (the forecast moved too)'}; f_half unchanged: {x[5]}")
        else:
            print(f"    p before {b['p'].get('value')} after {r['p'].get('value')}; after's reason: {str(r['p'].get('not_computed'))[:300]}")
        if "ballot" in r:
            print(f"    ballot.others: before {b.get('ballot', {}).get('others')} after {r['ballot'].get('others')} (candidates after neither D, R nor W-I: {len([c for c in r['result']['candidates'] if c['party'] not in ('D', 'R') and not c['party'].startswith('W-I')])})")
        notes = [n for n in r.get("notes", []) if n.startswith("the count (pipeline/governor_counts.py)")]
        figs_in_note = {v: any(f"{v:,}" in n for n in notes) for v in src_figs.values() if v}
        print(f"    the count note: {len(notes)}; the source's figures in it: {figs_in_note}; Cha's note kept: {any('leave out candidates under ten votes' in n for n in r.get('notes', []))}")

    # Connecticut
    ct = ct_page()
    print(f"\n  Connecticut's page (electionhistory.ct.gov/contest/3781), its data as served: office {ct['office']}, {ct['division']}, event {ct['event_date'][:10]}, "
          f"contest {ct['contest']}; words on the page: {ct['words']}")
    for c in ct["candidates"]:
        print(f"    {c['name']}: {c['votes']:,} = lines {c['lines']} ({'sum ok' if sum(v or 0 for _, v in c['lines']) == c['votes'] else 'LINES DO NOT SUM'}); write-in {c['write_in']}; winner {c['winner']}")
    print(f"    the candidates' sum {ct['sum']:,}; the page's total rows (pseudocandidates) {ct['totals']}; equal: {all(v == ct['sum'] for _, v in ct['totals'])}; "
          f"the page's other integers {ct['ints']}; named totals in the JSON {ct['totals_named']}")
    show("2018-governor-CT", {"LAMONT, EDWARD M. (NED)": next(c["votes"] for c in ct["candidates"] if "Lamont" in c["name"]),
                              "STEFANOWSKI, BOB": next(c["votes"] for c in ct["candidates"] if "Stefanowski" in c["name"]),
                              "GRIEBEL, R. NELSON (OZ)": next(c["votes"] for c in ct["candidates"] if "Griebel" in c["name"]),
                              "WHITNUM, LEE": next(c["votes"] for c in ct["candidates"] if "Whitnum" in c["name"])},
         "the Secretary of the State's count, every line [stated: the page]")
    s_ct = aa_sums(2018, "CT")
    m_ct = medsl_governor(2018, "CT")
    print(f"    Algara and Amlani, Connecticut 2018 over {s_ct['counties']} counties: D {s_ct['D']:,} R {s_ct['R']:,} ({s_ct['dem']} / {s_ct['rep']}); equal to the page's lines summed: "
          f"{(s_ct['D'], s_ct['R']) == (694510, 650138)}")
    print(f"    MEDSL's 2018 Connecticut file, my summary (lines summed under the name): {dict(sorted(m_ct['cands'].items(), key=lambda nv: -nv[1])[:3])}; counties {m_ct['counties']} "
          f"(D3: 694,509 and 650,132 every line summed)")
    # New York
    s_ny = aa_sums(2018, "NY")
    m_ny = medsl_governor(2018, "NY")
    print(f"\n  Algara and Amlani, New York 2018 over {s_ny['counties']} counties ({s_ny['missing_D']} D / {s_ny['missing_R']} R rows missing): D {s_ny['D']:,} R {s_ny['R']:,} "
          f"({s_ny['dem']} / {s_ny['rep']}); county totals {s_ny['total']:,}")
    show("2018-governor-NY", {"CUOMO, ANDREW M.": s_ny["D"], "MOLINARO, MARCUS J. (MARC)": s_ny["R"]}, "Algara and Amlani's county returns, every line [measured: my sums]")
    named = {n: v for n, v in m_ny["cands"].items() if not re.search(r"BALLOTS|VOIDS|SCATTER|UNDER|ELIGIBLE|VOTES|WRITE", n)}
    print(f"    MEDSL's 2018 New York file, my summary: {dict(sorted(named.items(), key=lambda nv: -nv[1])[:3])}; counties {m_ny['counties']} of 62; Cuomo's lines summed "
          f"{m_ny['cands'].get('ANDREW M CUOMO', 0) / s_ny['D']:.4f} of Algara and Amlani's; Cha's own-line figures 3,424,416 and 1,926,485 [stated: the note] are "
          f"{3424416 / s_ny['D']:.4f} and {1926485 / s_ny['R']:.4f} of them")
    # Indiana 2024
    ia = in_archive_2024()
    print(f"\n  Indiana's 2024 archive (my copy of the seventh pass, enr.indianavoters.in.gov/archive/2024General): {ia['office']}; settings {ia['settings']}; written {ia['write_time']}")
    for c in ia["candidates"]:
        print(f"    {c}")
    show("2024-governor-IN", {"BRAUN, MIKE": next(c[2] for c in ia["candidates"] if "Braun" in c[0]), "MCCORMICK, JENIFFER": next(c[2] for c in ia["candidates"] if "McCormick" in c[0]),
                              "RAINWATER, DONALD": next(c[2] for c in ia["candidates"] if "Rainwater" in c[0]), "STRIED, CHRISTOPHER RYAN": next(c[2] for c in ia["candidates"] if "Stried" in c[0])},
         "the archive's certified count (settings 'Certified': 'T') [stated]")
    # Utah 2008
    ut = ut_xls()
    print(f"\n  Utah's 2008 workbook (vote.utah.gov .../2008Gen.xls): sheets {ut['sheets']}; the {ut['sheet']} sheet's header {ut['header']}; its Total row {ut['total_row']}; "
          f"{ut['county_rows']} county rows; words 'certif'/'official'/'canvass'/'abstract' anywhere in the workbook: {ut['marks'] or 'none'}")
    tr = ut["total_row"]
    hunts = next(v for k, v in tr.items() if k.startswith("Huntsman"))
    spring = next(v for k, v in tr.items() if k.startswith("Springmeyer"))
    schanze = next(v for k, v in tr.items() if k.startswith("Schanze"))
    dough = next(v for k, v in tr.items() if k.startswith("Doughton"))
    show("2008-governor-UT", {"HUNTSMAN, JON M., JR.": int(hunts), "SPRINGMEYER, BOB": int(spring), "SCHANZE, DELL (SUPERDELL)": int(schanze), "DOUGHTON": int(dough)},
         "the Lieutenant Governor's workbook, Total row; no mark [stated]; Algara and Amlani agree (two witnesses)")
    b_ut, a_ut = recs["2008-governor-UT"]
    names_a = [c["name"] for c in a_ut["result"]["candidates"]]
    print(f"    the record's names: {names_a} (the figures above are matched by surname below)")
    by_sur = {re.split(r"[ ,]", n)[0]: c["votes"] for n, c in ((c["name"], c) for c in a_ut["result"]["candidates"])}
    print(f"    by surname: Huntsman {by_sur.get('HUNTSMAN')} = {int(hunts)}: {by_sur.get('HUNTSMAN') == int(hunts)}; Springmeyer {by_sur.get('SPRINGMEYER')} = {int(spring)}: {by_sur.get('SPRINGMEYER') == int(spring)}; "
          f"Schanze {by_sur.get('SCHANZE')} = {int(schanze)}: {by_sur.get('SCHANZE') == int(schanze)}; Doughton {by_sur.get('DOUGHTON')} = {int(dough)}: {by_sur.get('DOUGHTON') == int(dough)}")
    s_ut = aa_sums(2008, "UT")
    print(f"    Algara and Amlani, Utah 2008 over {s_ut['counties']} counties: D {s_ut['D']:,} R {s_ut['R']:,} ({s_ut['dem']} / {s_ut['rep']}); equal to the workbook's Total row: "
          f"{(s_ut['R'], s_ut['D']) == (int(hunts), int(spring))}; within 0.4% by candidate (the two-witness rule): "
          f"{abs(s_ut['R'] / hunts - 1) <= 0.004 and abs(s_ut['D'] / spring - 1) <= 0.004}; Cha's 700,565 / 175,301 [stated] under the workbook by "
          f"{1 - 700565 / hunts:.4f} / {1 - 175301 / spring:.4f}")
    # West Virginia 2012
    wv = wv_page()
    print(f"\n  West Virginia's 2012 page (apps.sos.wv.gov, statewide, eid 13): governor {wv['candidates']}; 'Official Total Votes' {wv['official_total']}; precincts (number, reporting) {wv['precincts']}; "
          f"words {wv['words']}; heading 'Official Results' {wv['heading_stars']}; the segment: {wv['segment'][:300]}")
    s_wv = aa_sums(2012, "WV")
    print(f"    Algara and Amlani, West Virginia 2012 over {s_wv['counties']} counties: D {s_wv['D']:,} R {s_wv['R']:,}; equal to the page: "
          f"{(s_wv['D'], s_wv['R']) == (next(c[2] for c in wv['candidates'] if 'TOMBLIN' in c[0]), next(c[2] for c in wv['candidates'] if 'MALONEY' in c[0]))} (so a copy of it, not a second witness: D3's reading [stated])")
    b_wv, a_wv = recs["2012-governor-WV"]
    show("2012-governor-WV", {"TOMBLIN, EARL RAY": 297207, "MALONEY, WILLIAM (BILL)": 273130, "JOHNSON, JESSE CLARENCE, JR.": 15179, "MORAN, DAVID D. (DAVE)": 7934},
         "held: the record keeps Cha's count [stated: the figures are Cha's as the record before carries them]")
    print(f"    Cha's figures under the page's: " + ", ".join(f"{c['name'].split(',')[0]} {1 - c['votes'] / next(x[2] for x in wv['candidates'] if c['name'].split(',')[0] in x[0]):.4f}" for c in b_wv["result"]["candidates"]))
    own_a = len([f_ for f_ in a_wv["forecasts"] if f_.get("by") == OWN])
    own_b = len([f_ for f_ in b_wv["forecasts"] if f_.get("by") == OWN])
    print(f"    after: model's-own forecasts {own_a} (before {own_b}); "
          f"p.not_computed begins '{str(a_wv['p'].get('not_computed'))[:90]}...'; the page's figures in the note: "
          f"{all(f'{c[2]:,}' in ' '.join(a_wv['notes']) for c in wv['candidates'])}; the three sentences quoted: "
          f"{[w for w in wv['words'] if w in ' '.join(a_wv['notes'])]}")
    # the last-race inputs
    print("\n  the last-race inputs that read these counts:")
    cha = F.cha_contests()
    wv11 = [c for c in cha if c["office"] == "governor" and c["state"] == "WV" and c["year"] == 2011]
    dr = F.top_two_DR(wv11[0]["candidates"]) if wv11 else None
    y11 = dr[0]["votes"] / (dr[0]["votes"] + dr[1]["votes"]) if dr else None
    print(f"    West Virginia 2011 (Cha: {len(wv11)} contest, special {wv11[0]['special'] if wv11 else None}): {[(c['name'], c['party'], c['votes']) for c in (wv11[0]['candidates'] if wv11 else [])][:3]}; D's two-party share {y11}")
    for cid, (lag_y, lag_new) in (("2022-governor-CT", (2018, 694510 / (694510 + 650138))), ("2022-governor-NY", (2018, 3635340 / (3635340 + 2207602))),
                                  ("2010-governor-UT-special", (2008, 186503 / (186503 + 734049))), ("2016-governor-WV", (2011, y11))):
        b, r = recs[cid]
        lb, la = b["forecast_inputs"]["last_governor_race"], r["forecast_inputs"]["last_governor_race"]
        print(f"    {cid}: before {lb}; after {la}; expected year {lag_y} share {lag_new:.6f}: {la['year'] == lag_y and abs(la['share_D'] - lag_new) < 1e-6}; "
              f"p {pv(b):.6e} -> {pv(r):.6e} (x{pv(r) / pv(b):.6f}); the model's own beside: {[round(y / x, 6) for x, y in zip(C41.beside(b), C41.beside(r)) if x]}")
    # Hawaii 2018's n
    b, r = recs["2018-governor-HI"]
    print(f"\n  Hawaii 2018: two_party n before {b['two_party']['n_other_voters']:,} after {r['two_party']['n_other_voters']:,} (= sum - 1: {r['two_party']['n_other_voters'] == sum(r['two_party']['votes']) - 1}); "
          f"p {pv(b):.6e} -> {pv(r):.6e} (x{pv(r) / pv(b):.8f}; n ratio {b['p']['n'] / r['p']['n']:.8f})")
    # Missouri and Maine
    print("\n  Missouri 2008, 2012, 2016 (the Secretary of State's PDFs refused to me; the records' notes and A&A read):")
    for cid in ("2008-governor-MO", "2012-governor-MO", "2016-governor-MO"):
        b, r = recs[cid]
        s_mo = aa_sums(int(cid[:4]), "MO")
        two = {c["party"]: c["votes"] for c in r["result"]["candidates"] if c["party"] in ("D", "R")}
        notes = [n for n in r.get("notes", []) if "Missouri's official returns" in n or "official returns" in n.lower()]
        print(f"    {cid}: record D {two['D']:,} R {two['R']:,} (before the same: {[c['votes'] for c in b['result']['candidates']] == [c['votes'] for c in r['result']['candidates']]}); "
              f"A&A over {s_mo['counties']} counties D {s_mo['D']:,} ({s_mo['D'] / two['D'] - 1:+.4f}) R {s_mo['R']:,} ({s_mo['R'] / two['R'] - 1:+.4f}); "
              f"p {pv(b)} -> {pv(r)}; note added: {len(notes)} {notes[0][:160] + '...' if notes else ''}")
    kc = [i for i in aa()["idx"].get((2016, "MO", "G"), []) if "KANSAS" in (aa()["df"]["data"]["county_name"][i] or "").upper()]
    cols = aa()["df"]["data"]
    print(f"    A&A's Missouri 2016 rows named Kansas City: {[(cols['county_name'][i], cols['fips'][i], cols['democratic_raw_votes'][i], cols['republican_raw_votes'][i]) for i in kc]} "
          f"(D3: the shortfall is Kansas City's own rows, Koster 98,336 / Greitens 25,284: Koster's gap {two['D'] - aa_sums(2016, 'MO')['D']:,}, Greitens's {two['R'] - aa_sums(2016, 'MO')['R']:,})")
    b, r = recs["2010-governor-ME"]
    s_me = aa_sums(2010, "ME")
    mitch = next(c["votes"] for c in r["result"]["candidates"] if c["party"] == "D")
    lep = next(c["votes"] for c in r["result"]["candidates"] if c["party"] == "R")
    print(f"\n  Maine 2010: A&A over {s_me['counties']} counties D {s_me['D']:,} ({s_me['D'] / mitch - 1:+.4f} of the record's Mitchell {mitch:,}) R {s_me['R']:,} ({s_me['R'] / lep - 1:+.4f} of LePage {lep:,}); "
          f"the deciding pair {r['two_party']['candidates']}; p before {pv(b)} after {pv(r)}; note: {[n[:200] for n in r.get('notes', []) if 'Algara' in n][:1]}")


# ------------------------------------------------------------------------------------------ 47.3 the refit

def apply_counts(rows):
    """The four counts on my fit rows (y, n2; the later rows' lag that carried the old share), West Virginia 2012 dropped and
    West Virginia 2016's lag set to the 2011 special's share (Cha's), as governor_counts and chambers do [stated]; returns the
    rows and what changed."""
    changed = []
    out = []
    for r in rows:
        if r.get("id") in HELD:
            changed.append((r["id"], "dropped from the fit", r["y"], None))
            continue
        out.append(r)
    for cid, (D, R) in NEW_COUNTS.items():
        r0 = next((r for r in out if r.get("id") == cid), None)
        if r0 is None:
            changed.append((cid, "no row", None, None))
            continue
        y_old, y_new = r0["y"], D / (D + R)
        changed.append((cid, "y, n2", (r0["y"], r0["n2"]), (y_new, D + R)))
        r0["y"], r0["n2"] = y_new, D + R
        for r in out:
            if r is r0 or r["level"] != "governor" or r["state"] != r0["state"] or r["year"] <= r0["year"] or r.get("lag") is None:
                continue
            if abs(r["lag"] - y_old) < 1e-9 and r.get("lag_year") == r0["year"]:
                changed.append((r.get("id"), "lag", r["lag"], y_new))
                r["lag"] = y_new
    cha = F.cha_contests()
    wv11 = next(c for c in cha if c["office"] == "governor" and c["state"] == "WV" and c["year"] == 2011)
    dr = F.top_two_DR(wv11["candidates"])
    y11 = dr[0]["votes"] / (dr[0]["votes"] + dr[1]["votes"])
    for r in out:
        if r["level"] == "governor" and r["state"] == "WV" and r.get("lag_year") == 2012:
            changed.append((r.get("id"), "lag (2012 held -> 2011 special)", r["lag"], y11))
            r["lag"], r["lag_year"] = y11, 2011
    return out, changed


def section_3(mv):
    h1("47.3 My own refit with the four counts and West Virginia 2012 out, against the model blocks before and after")
    d = F.all_rows()
    rows = d["rows"]
    print(f"  rows {len(rows):,} (c9's; Hawaii 2018's certified figures applied on load: {d.get('certified_applied')})")
    rows_before = copy.deepcopy(rows)
    rows_after, changed = apply_counts(copy.deepcopy(rows))
    for c in changed:
        print(f"    {c}")
    g_b = [r for r in rows_before if r["level"] == "governor"]
    g_a = [r for r in rows_after if r["level"] == "governor"]
    print(f"  governor rows before {len(g_b)}, after {len(g_a)}; the 2014 fit's rows (year < 2014, D2's fit window from 1978): before {len([r for r in g_b if 1978 <= r['year'] < 2014])} after "
          f"{len([r for r in g_a if 1978 <= r['year'] < 2014])} (D3: '399 races where there were 400')")
    wb, wa = C41.worktree(BEFORE), C41.worktree(AFTER)
    years = sorted({int(f[:4]) for f in os.listdir(os.path.join(wa, "data", "governor")) if f.endswith(".json")})
    even = [t for t in years if t % 2 == 0 and t >= 2010]
    print(f"\n  {'year':6s} {'terms':10s} " + " ".join(f"{k:>10s}" for k in TERMS))
    fits = {}
    for label, rr, wt in (("before", rows_before, wb), ("after", rows_after, wa)):
        F._RAW.clear()
        F._SC.clear()
        for t in even:
            m, fy = F.variant_model(rr, "governor", t, RECORD_VARIANT["governor"])
            blk = json.load(open(os.path.join(wt, "data", "governor", f"{t}.json")))["model"]
            fits[(label, t)] = (m, blk)
            mt, bt = C41.my_terms(m), C41.block_terms(blk)
            print(f"  {t:<6d} {label + ', mine':10s} " + " ".join(f"{mt[k]:10.6f}" if mt.get(k) is not None else f"{'-':>10s}" for k in TERMS))
            print(f"  {'':6s} {'block':10s} " + " ".join(f"{bt[k]:10.6f}" if bt.get(k) is not None else f"{'-':>10s}" for k in TERMS))
            worst = max((rel(mt[k], bt[k]), k) for k in TERMS if bt.get(k) is not None and mt.get(k) is not None)
            print(f"  {'':6s} {'rel diff':10s} largest {worst[0]:.1e} ({worst[1]}); fit races mine {m.get('n') or m.get('races')} / the block's {blk.get('races')}")
    print("\n  the change before -> after, the blocks' against my fits' (a sign and size test of the refit):")
    tal = collections.Counter()
    for t in even:
        mb, bb = fits[("before", t)]
        ma, ba = fits[("after", t)]
        mt_b, mt_a, bt_b, bt_a = C41.my_terms(mb), C41.my_terms(ma), C41.block_terms(bb), C41.block_terms(ba)
        parts = []
        for k in ("b_lean", "b_inc", "b_lag", "s_e", "s_a", "c0", "c1", "k"):
            if bt_a.get(k) is None or mt_a.get(k) is None:
                continue
            db, dm = bt_a[k] - bt_b[k], mt_a[k] - mt_b[k]
            same = (db == 0 and abs(dm) < 1e-9) or db * dm > 0
            tal["same sign" if same else "opposite or one zero"] += 1
            parts.append(f"{k} block {db:+.2e} mine {dm:+.2e}")
        print(f"    {t}: " + "; ".join(parts))
    print(f"    signs: {dict(tal)}")
    # every moved governor p from my fits
    print("\n  the moved governor p of the even years, the ratio after/before from my fits (the forecast's f_half and the record's n) against the file's:")
    moved = [r for r in mv["records"] if "P" in r[7] and r[1].startswith("data/governor")]
    tal = collections.Counter()
    worst = []
    for row in sorted(moved):
        cid = row[0]
        t = int(cid[:4])
        if t % 2:
            tal["odd year (c25's route; below)"] += 1
            continue
        rb = next((x for x in rows_before if x.get("id") == cid), None)
        ra = next((x for x in rows_after if x.get("id") == cid), None)
        if rb is None or ra is None:
            tal["no row of mine (or held)"] += 1
            continue
        if t < 2010:
            tal["before 2010 (no fit of mine; the record's own forecast below)"] += 1
            continue
        mb, _ = fits[("before", t)]
        ma, _ = fits[("after", t)]
        mean_b, sd_b, _ = F.predict(mb, rb)
        mean_a, sd_a, _ = F.predict(ma, ra)
        tails = "normal" if "normal" in row[2] else "t4"
        fb_, fa_ = L.f_half(mean_b, sd_b, tails), L.f_half(mean_a, sd_a, tails)
        recb, reca = gov_record(BEFORE, cid), gov_record(AFTER, cid)
        n_ratio = recb["p"]["n"] / reca["p"]["n"]
        if row[2].startswith("538"):   # 538's forecast of record (not 'the model's own ...; 538 beside'): the n alone moves it
            ratio = n_ratio
            kind = "538 of record: n alone"
        else:
            ratio = fa_ / fb_ * n_ratio
            kind = "the model's own"
        d_ = abs(ratio - row[5])
        band = "within 1e-4" if d_ <= 1e-4 else "within 1e-3" if d_ <= 1e-3 else "within 1e-2" if d_ <= 1e-2 else "beyond 1e-2"
        same_dir = (ratio - 1) * (row[5] - 1) > 0 or abs(ratio - 1) < 1e-5 or abs(row[5] - 1) < 1e-5
        tal[(kind, band, "same direction" if same_dir else "OPPOSITE")] += 1
        worst.append((d_, cid, row[5], round(ratio, 6), round(n_ratio, 6)))
    for k_, v in sorted(tal.items(), key=str):
        print(f"    {str(k_):75s} {v}")
    worst.sort(reverse=True)
    for d_, cid, theirs, mine_, nr in worst[:8]:
        print(f"    {cid}: file x{theirs:.6f}, mine x{mine_:.6f} (n alone x{nr:.6f})")
    # the odd years and 2008
    print("\n  the odd years' and 2008's moved p: p recomputed from each record's own forecast (density: f(1/2)/(2n)) before and after:")
    for row in sorted(moved):
        cid = row[0]
        t = int(cid[:4])
        if t % 2 == 0 and t >= 2010:
            continue
        out = []
        for c in (gov_record(BEFORE, cid), gov_record(AFTER, cid)):
            p = c["p"]
            fc = c["forecasts"][p["of_forecast"]]
            pm = L.p_density(p["n"], L.f_half(fc["share"]["mean"], fc["share"]["sd"], fc["share"]["tails"]))
            out.append((p["value"], pm, fc["share"]["mean"], fc["share"]["sd"], p["n"]))
        print(f"    {cid}: before p {out[0][0]:.6e} (from its forecast {out[0][1]:.6e}; mean {out[0][2]:.6f} sd {out[0][3]:.6f}; n {out[0][4]:,}) -> after {out[1][0]:.6e} "
              f"(from its forecast {out[1][1]:.6e}; mean {out[1][2]:.6f} sd {out[1][3]:.6f}; n {out[1][4]:,}); ratio {row[5]}")
    for f_ in sorted(f for f in os.listdir(os.path.join(wa, "data", "governor")) if int(f[:4]) % 2 and f.endswith(".json")):
        hb = {k: v for k, v in json.load(open(os.path.join(wb, "data", "governor", f_))).items() if k != "contests"}
        ha = {k: v for k, v in json.load(open(os.path.join(wa, "data", "governor", f_))).items() if k != "contests"}
        dl = C41.diff_leaves(hb, ha)
        if dl:
            print(f"    {f_}: " + "; ".join(f"{k} {vb!s:.9} -> {va!s:.9}" for k, vb, va in dl[:5]) + (f" ... ({len(dl)} leaves)" if len(dl) > 5 else ""))
    # the House's and Senate's p of record
    hs = [r for r in mv["records"] if "P" in r[7] and not r[1].startswith("data/governor")]
    print(f"\n  the House's and Senate's p of record moved: {len(hs)} rows {dict(collections.Counter(r[1] for r in hs))}; ratios from {min(r[5] for r in hs):.6f} to {max(r[5] for r in hs):.6f}; "
          f"all within 0.002%: {all(abs(r[5] - 1) <= 2e-5 for r in hs)}; the p beside's ratios (not of record), the farthest from 1: "
          f"{max((abs(x - 1), r[0]) for r in mv['records'] if not r[1].startswith('data/governor') for x in r[6] if x is not None)}")
    b2012 = json.load(open(at(BEFORE, "data/house/2012.json")))
    a2012 = json.load(open(at(AFTER, "data/house/2012.json")))
    dl = C41.diff_leaves({k: v for k, v in b2012.items() if k != "contests"}, {k: v for k, v in a2012.items() if k != "contests"})
    print(f"  data/house/2012.json's block: {len(dl)} leaves changed: " + "; ".join(f"{k} {vb!s:.9} -> {va!s:.9}" for k, vb, va in dl[:6]))


# ------------------------------------------------------------------------------------------ 47.4 the fusion scan

def all_record_files(commit, levels):
    wt = C41.worktree(commit)
    out = []
    for lv in levels:
        d = os.path.join(wt, "data", lv)
        if not os.path.isdir(d):
            continue
        for root, _, files in os.walk(d):
            for n in files:
                if n.endswith(".json") and (re.fullmatch(r"\d{4}\.json", n) or re.fullmatch(r"[A-Z]{2}\.json", n)):
                    out.append((lv, os.path.relpath(os.path.join(root, n), wt)))
    return sorted(out)


CONTEST_KEY = ("year", "month", "day", "etype", "sid", "sen", "dname", "dno", "geopost", "mmdpost", "regime")   # the intake's, copied


def klarner_lines():
    """Klarner's candidate file read as the intake reads it (pipeline/intake/klarner_state_legislative.normalize, copied): a
    contest is CONTEST_KEY; a candidate is candid (or the name), 'scattering' apart; a line is the row's party, or partyz where
    party is empty, each distinct value once. A candidate on several lines has more than one; the counts by contest, for every
    contest and for the general-type ones (etype not a primary: the intake's deter rule, 'not startswith dp, rp, ttp')."""
    if not os.path.exists(KLARNER_CANDS):
        return None
    lines = {}
    etypes = collections.Counter()
    n = 0
    with open(KLARNER_CANDS, newline="", encoding="utf-8", errors="replace") as f:
        rd = csv.DictReader(f)
        for r in rd:
            n += 1
            key = tuple(r[k] for k in CONTEST_KEY)
            scat = r["last"].strip().lower() == "scattering" or r["cand"].strip().lower() == "scattering"
            ck = "scattering" if scat else (r["candid"] or r["cand"])
            line = r["party"] or r["partyz"]
            ls = lines.setdefault((key, ck), [])
            if line and line not in ls:
                ls.append(line)
            etypes[r["etype"]] += 1
    out = {"rows": n, "etypes": dict(etypes.most_common(8))}
    for label, keep in (("every contest", lambda et: True), ("general type (etype not dp*, rp*, ttp*)", lambda et: not et.startswith(("dp", "rp", "ttp")))):
        multi = [(k, c) for (k, c), ls in lines.items() if len(ls) > 1 and keep(k[3])]
        contests = {k for k, _ in multi}
        by_state = collections.Counter(k[4] for k in contests)   # sid: the state's id; the intake carries sab as state
        out[label] = {"contests": len(contests), "candidates": len(multi), "by_sid": dict(by_state.most_common(6))}
    # the states' names for the by-state count (sab by sid, from the rows)
    return out


def section_4():
    h1("47.4 The fusion scan: every record's lines against its votes; check-fusion.json's counts; Klarner's lines; the governor second count")
    cf = L.load_json(at(AFTER, "data/local/check-fusion.json"))
    print(f"  check-fusion.json: {cf['about'][:300]}...")
    # D2's files: a candidate on several lines is one whose party names several ('R/CRV/IDP/REF'), the FEC's combined figure
    for lv in ("house", "senate", "president", "governor"):
        recs = {}
        for _, f in all_record_files(AFTER, (lv,)):
            recs.update(records_at(AFTER, f))
        slash = collections.Counter()
        lines = collections.Counter()
        comma = collections.Counter()
        bad = []
        for r in recs.values():
            st = r["place"]["state"]
            cs = (r.get("result") or {}).get("candidates") or []
            if any("/" in (c.get("party") or "") for c in cs):
                slash[st] += 1
            if lv == "governor" and any("," in (c.get("party") or "") for c in cs) and str((r["result"].get("source") or {}).get("name", "")).startswith("Cha, Kuriwaki"):
                comma[st] += 1   # Cha's party_formal names several lines ('D,Indep,WF'); the record carries it as the party
            if any(isinstance(c.get("lines"), list) for c in cs):
                lines[st] += 1
                for c in cs:
                    if isinstance(c.get("lines"), list) and sum(l_["votes"] for l_ in c["lines"]) != c["votes"]:
                        bad.append((r["id"], c["name"]))
        theirs = cf["levels"].get(lv)
        print(f"  {lv}: records {len(recs):,}; with a candidate's party naming several lines ('/', the FEC's): {sum(slash.values())} {dict(slash.most_common(6))}"
              + (f"; (',', Cha's party_formal, the source Cha's): {sum(comma.values())} {dict(comma)}" if lv == "governor" else "")
              + f"; with `lines`: {sum(lines.values())} {dict(lines)}; lines not summing to the votes: {bad}")
        if theirs:
            for src, v in theirs.items():
                print(f"    the file: {src[:70]}: records {v['records']}, summed {v['summed']}, one_line {v['one_line']}, by_state {dict(list(v['by_state'].items())[:6])}")
        elif lv == "president":
            print(f"    the file: {str(cf.get('president'))[:200]}")
    # D3's files
    for lv in ("state-lower", "state-upper", "local", "measure", "primary"):
        n_rec, with_lines, by_state, bad, n_cands, lines_n = 0, 0, collections.Counter(), [], 0, 0
        any_lines, bad_any = 0, []
        for _, f in all_record_files(AFTER, (lv,)):
            for r in records_at(AFTER, f).values():
                n_rec += 1
                hit = False
                for c in (r.get("result") or {}).get("candidates") or []:
                    ls = c.get("lines")
                    if not isinstance(ls, list):
                        continue
                    if len(ls) > 1:
                        any_lines += 1
                        if sum(l_.get("votes") or 0 for l_ in ls) != (c.get("votes") or 0):
                            bad_any.append((r["id"], c["name"], c.get("votes"), sum(l_.get("votes") or 0 for l_ in ls), [l_.get("party") for l_ in ls]))
                    # D3's rule, copied (check_fusion.legislatures_and_local): more than one line with a party
                    if len([x for x in ls if isinstance(x, dict) and x.get("party")]) > 1:
                        hit = True
                        n_cands += 1
                        lines_n += len(ls)
                        if sum(l_.get("votes") or 0 for l_ in ls) != (c.get("votes") or 0):
                            bad.append((r["id"], c["name"], c.get("votes"), sum(l_.get("votes") or 0 for l_ in ls)))
                if hit:
                    with_lines += 1
                    by_state[r["place"]["state"]] += 1
        theirs = cf["levels"].get(lv, {})
        tv = next(iter(theirs.values())) if theirs else {}
        print(f"  {lv}: records {n_rec:,}; with a candidate on several party lines (D3's rule copied: more than one line with a party): {with_lines} ({n_cands} candidates, {lines_n} lines) {dict(by_state.most_common(8))}; "
              f"not summing: {len(bad)} {bad[:3]}; the file: records {tv.get('records')}, summed {tv.get('summed')}, one_line {tv.get('one_line')}, by_state {dict(list((tv.get('by_state') or {}).items())[:6])}; "
              f"equal: {tv.get('records') == with_lines and dict(tv.get('by_state') or {}) == dict(by_state)}")
        if any_lines:
            print(f"    candidates with any `lines` list of two or more (a line without a party, or a second spelling, too): {any_lines}; of them not summing to the votes: {len(bad_any)} "
                  f"{bad_any[:4]}{' ...' if len(bad_any) > 4 else ''} (outside D3's rule, which counts party lines)")
    # Klarner's lines
    kl = klarner_lines()
    print(f"\n  Klarner's candidate file: {kl if kl else 'not fetched (the fetch failed or is still running); the intake counts 6,659 contests / 8,810 candidates on several lines [stated]'}")
    print(f"    the file's klarner block: {json.dumps(cf['klarner'])[:400]}")
    # the governor second count
    print("\n  the governor second count (the file: 'the record's two nominees against Algara and Amlani's county returns summed; listed where either differs by more than the line' 0.005):")
    g = cf["governor_second_count"]
    print(f"    the file: compared {g['compared']}, line {g['line']}, listed {[(x['id'], [(n_['party'], n_['record'], n_['algara_amlani'], n_['off']) for n_ in x['nominees']]) for x in g['listed']]}")
    compared, listed, skipped = 0, [], collections.Counter()
    cmp_rows, cmp_parties = [], []
    for _, f in all_record_files(AFTER, ("governor",)):
        for r in records_at(AFTER, f).values():
            t, st = r["year"], r["place"]["state"]
            if t < 2006 or t > 2020:
                skipped["outside 2006-2020"] += 1
                continue
            # the record's Democrat and Republican: the leading candidate whose party is D (DFL in Minnesota) or R, a party
            # naming several lines by its first ('D,Indep,WF' is Cha's party_formal) [D3's 'the record's two nominees', read so]
            def lead(ps):
                xs = [c for c in r["result"]["candidates"] if (c.get("party") or "").split(",")[0].strip() in ps]
                return max(xs, key=lambda c: c["votes"] or 0)["votes"] if xs else None
            two = {"D": lead(("D", "DFL")), "R": lead(("R",))}
            if two["D"] is None or two["R"] is None:
                skipped["no D and R"] += 1
                continue
            s = aa_sums(t, st, "S" if r.get("special") else "G") or aa_sums(t, st)
            if s is None:
                skipped["no A&A rows"] += 1
                continue
            compared += 1
            cmp_parties.append((r["id"], tuple(next((c.get("party") or "") for c in r["result"]["candidates"] if (c.get("party") or "").split(",")[0].strip() in ps and (c["votes"] or 0) == two[k]) for k, ps in (("D", ("D", "DFL")), ("R", ("R",))))))
            offs = {"D": s["D"] / two["D"] - 1 if two["D"] else None, "R": s["R"] / two["R"] - 1 if two["R"] else None}
            cmp_rows.append((r["id"], offs))
            if any(o is not None and abs(o) > 0.005 for o in offs.values()):
                listed.append((r["id"], two["D"], s["D"], round(offs["D"], 5), two["R"], s["R"], round(offs["R"], 5), s["counties"]))
    odd_party = [(i_, ps) for i_, ps in cmp_parties if ps != ("D", "R")]
    print(f"    mine: compared {compared} (skipped {dict(skipped)}); of them with a nominee's party other than plain D or R (DFL, or Cha's party_formal naming lines): "
          f"{len(odd_party)} {odd_party} (D3's 198 compared against my {compared}: the difference lies among these, his reader of A&A's normalized file matching the nominees its own way [inferred])")
    print(f"    listed {len(listed)}:")
    for x in sorted(listed):
        print(f"      {x}")
    mine_ids = {x[0] for x in listed}
    theirs_ids = {x["id"] for x in g["listed"]}
    print(f"    the same set as the file's: {mine_ids == theirs_ids}; mine not the file's {sorted(mine_ids - theirs_ids)}; the file's not mine {sorted(theirs_ids - mine_ids)}")
    within = [max(abs(o) for o in offs.values() if o is not None) for _, offs in cmp_rows]
    print(f"    of the {compared} compared, within 0.1%: {sum(1 for w in within if w <= 0.001)}, 0.1-0.5%: {sum(1 for w in within if 0.001 < w <= 0.005)}; "
          f"the four records whose counts #109 took now equal A&A: {[(cid, dict(next(o for i_, o in cmp_rows if i_ == cid))) for cid in NEW_COUNTS if any(i_ == cid for i_, _ in cmp_rows)]}")


def main():
    which = [int(a) for a in sys.argv[1:]] or [1, 2, 3, 4]
    print(f"c47: section 19, part one; {BEFORE} -> {AFTER}; sections {which}")
    mv = None
    if 1 in which or 3 in which:
        mv = section_1() if 1 in which else L.load_json(at(AFTER, "data/local/moves-governor-counts.json"))
    if 2 in which:
        section_2()
    if 3 in which:
        section_3(mv)
    if 4 in which:
        section_4()


if __name__ == "__main__":
    main()
