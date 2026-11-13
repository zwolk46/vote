"""C40 (seventh pass; the orchestrator's words of 18:20, 20:28 and 20:30 UTC: "#92 merged at 67431a4: NJ's 2023 and 2025
legislatures, 121 records, and 2023 feeds 2024's fits, moving 4,548 p ... If D3's VA PR is merged by the time you start,
include it ... Check: the gate (official marks, county lines adding to Totals, lines only in the named counties, the
Governor list's sha256 against D2's file); the 120 new p from your own fit; class C for the 2023 Senate; every one of the
4,548 moves from your own refit with 2023 in"; "main is now at 6b24927 and holds #92 (NJ legislatures), #93 (VA
legislatures) and #95 (D3's volume PR ...). Take all three, with the end fixed at the main commit you start from").

The three PRs, each between the main commits before and after it (the records of each read from a detached worktree):
  #92  b9e0702 -> 67431a4  data/local/moves-nj-legislature.json
  #93  67431a4 -> d7eea96  data/local/moves-va-legislature.json
  #95  d7eea96 -> 6b24927  data/local/moves-volume.json (written against D3's merge eb5948b, not on main; the main
                           commits around #95 hold nothing else, so the diff is #95's)

  40.1 Each moves file against my own diff of every record between the two commits: the ids, the codes (A G P N L B Q O R),
       p before and after, the ratio.
  40.2 New Jersey's gate from the five Official Lists, fetched by checks/m2/fetch_seventh_pass.sh from the Division's pages
       and read here with pdftotext -layout by a reader written apart from pipeline/intake/nj_sos.py: (a) linked as
       "Official General Election Results: ...", every page headed "Official List", the last page's candidate count;
       (b) county lines adding to each Total and the Totals to the contest's; (c) lines only in the heading's counties;
       (d) the Governor's list the same file as D2's (sha256) and equal to D2's record. Then every record's candidates,
       votes, marks, totals and counties against the lists. Virginia's gate cannot be re-read: the Department refused
       D3 (REPORT section 28) and its hosts are not asked; D3's check-va-legislature.json is read as his record only.
  40.3 The new p from my own fit (c15's route (a) rows and fit; m2d3's like-race density and the exact rule): the odd-year
       records of New Jersey and Virginia, 2023 and 2025, route by route; the class-C reading of the 2023 chambers.
  40.4 Every move from my own refit: the fit for each year on the rows before and after the PR (Klarner's rows from his
       file, the added odd-year and 2024 rows from the records' inputs; for #95 New Hampshire's and Idaho's 2022 rows
       from the records at each commit), the like-race pools before and after from the records at each commit, p from
       both with each record's n; my ratio against the moves file's, record by record.
[measured] throughout; the records' own figures [stated]; D3's words [stated: his report].
"""
import collections
import csv
import glob
import hashlib
import html
import json
import math
import os
import re
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402
import m2d3 as D  # noqa: E402
import c15_d3_refit as C15  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
PRS = [("#92", "b9e0702", "67431a4", "moves-nj-legislature.json"),
       ("#93", "67431a4", "d7eea96", "moves-va-legislature.json"),
       ("#95", "d7eea96", "6b24927", "moves-volume.json")]
LEVELS = ("local", "primary", "measure", "state-lower", "state-upper", "governor")
WT = os.path.join(L.CACHE, "seventh", "wt")
NJ = os.path.join(L.CACHE, "seventh", "nj")
GOV_SHA = "ef28c114c11de275"   # D2's data/governor/2025.json, the record's note [stated]
NJ_COUNTIES = ("ATLANTIC", "BERGEN", "BURLINGTON", "CAMDEN", "CAPE MAY", "CUMBERLAND", "ESSEX", "GLOUCESTER", "HUDSON",
               "HUNTERDON", "MERCER", "MIDDLESEX", "MONMOUTH", "MORRIS", "OCEAN", "PASSAIC", "SALEM", "SOMERSET", "SUSSEX",
               "UNION", "WARREN")   # the 21 counties as the lists print them [stated: the Governor's list has a line for each]
ORD = {w: i + 1 for i, w in enumerate(["First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eighth", "Ninth",
                                        "Tenth", "Eleventh", "Twelfth", "Thirteenth", "Fourteenth", "Fifteenth", "Sixteenth",
                                        "Seventeenth", "Eighteenth", "Nineteenth", "Twentieth"])}
ORD.update({"Thirtieth": 30, "Fortieth": 40})
for _tens, _base in (("Twenty", 20), ("Thirty", 30)):
    for _w, _i in list(ORD.items())[:9]:
        ORD[f"{_tens}-{_w}"] = _base + _i
HEAD_RE = re.compile(r"^(\S[\w-]*) Legislative District: (.*?)(?: Counties)?\s*$")   # a long heading wraps, "Counties" alone on the next line
TOTAL_RE = re.compile(r"^\s{20,}Total\s+([\d,]+)\s*$")
COUNTY_RE = re.compile(r"^\s{30,}(" + "|".join(sorted(NJ_COUNTIES, key=len, reverse=True)) + r")\b\s*(.*?)\s*$")
PAGE_RE = re.compile(r"Official List\s+Page (\d+) of (\d+)")
LISTS = {("2023", "state-upper"): "2023-official-general-results-state-senate.pdf",
         ("2023", "state-lower"): "2023-official-general-results-general-assembly.pdf",
         ("2025", "state-lower"): "2025-official-general-results-general-assembly.pdf",
         ("2025", "state-upper"): "2025-official-general-results-state-senate-35ld.pdf",
         ("2025", "governor"): "2025-official-general-results-governor.pdf"}
TOL_P = 5.1e-5


def pres_2025():
    """The president's party for 2025's fits: from D1's 2024 records, the party leading the states' votes added up (the
    records carry no winner mark or electoral votes; 2024's popular and electoral winner are the same party [stated:
    D3's record names the National Archives' 2024 page, Trump, R])."""
    ev = collections.Counter()
    for c in L.load_json(os.path.join(L.DATA, "president", "2024.json"))["contests"]:
        for a in c["result"]["candidates"]:
            if (a.get("party") or "")[:1].upper() in ("D", "R") and a.get("votes"):
                ev[a["party"][:1].upper()] += a["votes"]
    return 1 if ev.most_common(1)[0][0] == "D" else -1


if 2025 not in C15.PRES:
    C15.PRES[2025] = pres_2025()   # c15's table carries 2025 since the run of record; kept for a c15 without it


def h1(s):
    print("\n" + "=" * 100 + f"\n{s}\n" + "=" * 100)


def h2(s):
    print("\n" + s)


# ------------------------------------------------------------------------------------------ the records at a commit
def worktree(commit):
    """A detached worktree of the commit under the cache (git worktree add --detach), made once."""
    path = os.path.join(WT, commit)
    if not os.path.isdir(os.path.join(path, "data")):
        os.makedirs(WT, exist_ok=True)
        r = subprocess.run(["git", "worktree", "add", "--detach", path, commit], capture_output=True, text=True, cwd=L.ROOT)
        if r.returncode != 0:
            raise SystemExit(f"git worktree add {commit}: {r.stderr.strip()}")
    return path


_ROWS = {}


def rows_at(root, level):
    """Every contest of a level at a commit's worktree as m2d3's slim row."""
    key = (root, level)
    if key not in _ROWS:
        out = []
        for path in sorted(glob.glob(os.path.join(root, "data", level, "[0-9]*", "*.json"))):
            with open(path) as fh:
                d = json.load(fh)
            for c in d["contests"]:
                out.append(D.slim(level, d, c))
        _ROWS[key] = out
    return _ROWS[key]


def forget(root):
    """Drop a commit's rows and pools once no later PR needs them (the records of five commits do not fit in memory at once)."""
    for k in [k for k in _ROWS if k[0] == root]:
        del _ROWS[k]
    _POOL.pop(root, None)
    for k in [k for k in _DENS if k[0] == root]:
        del _DENS[k]


def pval(c):
    p = c.get("p") or {}
    return p.get("value") if "value" in p else None


def what_differs(b, a):
    keys = set()
    for k in set(b) | set(a):
        if k == "p":
            pb, pa = b.get("p") or {}, a.get("p") or {}
            for kk in set(pb) | set(pa):
                if pb.get(kk) != pa.get(kk):
                    keys.add("p." + kk)
        elif k == "forecasts":
            fb, fa = b.get(k) or [], a.get(k) or []
            if json.dumps(fb, sort_keys=True) != json.dumps(fa, sort_keys=True):
                sub = set()
                for x, y in zip(fb, fa):
                    for kk in set(x) | set(y):
                        if x.get(kk) != y.get(kk):
                            sub.add(kk)
                if len(fb) != len(fa):
                    sub.add("count")
                keys.add("forecasts." + ",".join(sorted(sub)))
        elif isinstance(b.get(k), dict) and isinstance(a.get(k), dict) and b.get(k) != a.get(k):
            keys.add(k + "." + ",".join(sorted(kk for kk in set(b[k]) | set(a[k]) if b[k].get(kk) != a[k].get(kk))))
        elif b.get(k) != a.get(k):
            keys.add(k)
    return tuple(sorted(keys))


def my_code(b, a):
    """D3's letters from my own diff: A new, G gone; P p moved, N new p, L p lost; else B (p's block), Q (notes only),
    R (the not-computed reason), O (other fields)."""
    if b is None:
        return ("A",)
    if a is None:
        return ("G",)
    pb, pa = pval(b), pval(a)
    if pb is None and pa is not None:
        return ("N",)
    if pb is not None and pa is None:
        return ("L",)
    if pb is not None and pa is not None and abs(pb - pa) > 1e-12 * max(abs(pb), abs(pa), 1e-300):
        return ("P",)
    d = what_differs(b, a)
    if not d:
        return ()
    if pb is None and pa is None and any(x in ("p.not_computed", "p.reason") for x in d):
        return ("R",)
    if any(x.startswith("p.") for x in d):
        return ("B",)
    if all(x in ("forecasts.note", "note", "notes", "forecasts.note,source", "result.note") or x.startswith("forecasts.note") for x in d):
        return ("Q",)
    return ("O",)


def section_1():
    h1("40.1 The three moves files against my own diff of every record between the main commits before and after each PR")
    out = {}
    for pr, before, after, mvname in PRS:
        wb, wa = worktree(before), worktree(after)
        mv = L.load_json(os.path.join(L.DATA, "local", mvname))
        rows = {}
        for r in mv["records"]:
            rows[r[0]] = r
        h2(f"  {pr}: {before} -> {after}; {mvname} (against {mv.get('against')}): {len(mv['records']):,} rows, "
           f"{len(rows):,} ids; summary {json.dumps(mv['summary'])[:300]}...")
        files = subprocess.run(["git", "diff", "--name-only", before, after, "--", "data/"], capture_output=True, text=True, cwd=L.ROOT).stdout.split()
        files = [f for f in files if re.match(r"^data/(local|primary|measure|state-lower|state-upper)/\d{4}/[A-Z]{2}\.json$", f) or re.match(r"^data/governor/\d{4}\.json$", f)]
        print(f"  data files changed: {len(files)} " + str(dict(collections.Counter(f.split('/')[1] for f in files))))
        mine, agree, dis, pdiff, rdiff, unlisted, worst = collections.Counter(), 0, collections.Counter(), 0, 0, collections.Counter(), []
        seen = set()
        gov_rows = []
        for f in files:
            lv = f.split("/")[1]
            fb = os.path.join(wb, f)
            fa = os.path.join(wa, f)
            b = {c["id"]: c for c in (json.load(open(fb))["contests"] if os.path.exists(fb) else [])}
            a = {c["id"]: c for c in (json.load(open(fa))["contests"] if os.path.exists(fa) else [])}
            for i in sorted(set(b) | set(a)):
                code = my_code(b.get(i), a.get(i))
                if not code:
                    continue
                if lv == "governor":
                    gov_rows.append((i, code, b.get(i), a.get(i)))
                    continue
                mine[(lv, code[0])] += 1
                seen.add(i)
                row = rows.get(i)
                if row is None:
                    unlisted[(lv, code[0])] += 1
                    if code[0] in ("P", "N", "L", "A", "G"):
                        worst.append((i, code, "not in the moves file", what_differs(b.get(i) or {}, a.get(i) or {})[:4]))
                    continue
                theirs = tuple(row[8])
                if code[0] in theirs or (code[0] == "Q" and "O" in theirs) or (code[0] == "O" and "Q" in theirs) or (code[0] == "R" and ("Q" in theirs or "O" in theirs)):
                    agree += 1
                else:
                    dis[(lv, code[0], theirs)] += 1
                    if len(worst) < 400:
                        worst.append((i, code, theirs, what_differs(b.get(i) or {}, a.get(i) or {})[:4]))
                pb, pa = pval(b.get(i) or {}), pval(a.get(i) or {})
                if isinstance(row[5], str) or isinstance(row[6], str):
                    # the file writes the not-computed reason in p's columns
                    continue
                if (row[5] is None) != (pb is None) or (row[6] is None) != (pa is None) \
                        or (pb is not None and abs(row[5] - pb) > 1e-9 * max(abs(pb), 1e-300)) \
                        or (pa is not None and abs(row[6] - pa) > 1e-9 * max(abs(pa), 1e-300)):
                    pdiff += 1
                    if pdiff <= 3:
                        print(f"    p before/after differ from the record: {i} row {row[5]} {row[6]} record {pb} {pa}")
                if pb and pa and row[7] is not None and abs(row[7] - round(pa / pb, 4)) > 1.5e-4:
                    rdiff += 1
        listed_not_mine = [i for i in rows if i not in seen and not rows[i][1].startswith("data/governor")]
        print("  my diff, by level and code: " + "; ".join(f"{lv} {k} {v}" for (lv, k), v in sorted(mine.items())))
        print(f"  rows whose code I share: {agree:,} of {len(seen):,} ids in my diff; codes differing: {sum(dis.values())}; "
              f"ids in my diff but not in the file: {sum(unlisted.values())} {dict(unlisted) if unlisted else ''}; "
              f"ids in the file but not in my diff: {len(listed_not_mine)} {listed_not_mine[:5]}")
        print(f"  p before/after other than the record's: {pdiff}; ratios off the record's by more than 1.5e-4: {rdiff}")
        for (lv, mine_c, theirs), v in sorted(dis.items(), key=lambda kv: -kv[1])[:10]:
            ex = [w for w in worst if w[1][0] == mine_c and w[2] == theirs][:2]
            print(f"    mine {mine_c} theirs {theirs} {lv}: {v}; e.g. " + "; ".join(f"{e[0]} differs in {e[3]}" for e in ex))
        for w in [w for w in worst if w[2] == "not in the moves file"][:6]:
            print(f"    not in the file: {w[0]} mine {w[1]} differs in {w[3]}")
        if unlisted:
            ex = []
            for f in files:
                lv = f.split("/")[1]
                if lv == "governor":
                    continue
                fb_, fa_ = os.path.join(wb, f), os.path.join(wa, f)
                b = {c["id"]: c for c in (json.load(open(fb_))["contests"] if os.path.exists(fb_) else [])}
                a = {c["id"]: c for c in (json.load(open(fa_))["contests"] if os.path.exists(fa_) else [])}
                for i in a:
                    if i in b and i not in rows and my_code(b[i], a[i]):
                        ex.append((i, my_code(b[i], a[i]), what_differs(b[i], a[i])[:5]))
                if len(ex) >= 3:
                    break
            kinds = collections.Counter(tuple(e[2]) for e in ex)
            print(f"    the ids not in the file, what differs (first examples): " + "; ".join(f"{i} {c} {d}" for i, c, d in ex[:3]))
        if gov_rows:
            g = mv.get("governor", {})
            print(f"  governor records in my diff: {[(i, c) for i, c, _, _ in gov_rows]}; the file's governor section: {len(g.get('records', []))} rows "
                  f"({g.get('about', '')[:120]}...)")
            for i, code, b, a in gov_rows:
                pb_all = [(x.get("by") or x.get("method"), (x.get("p") or {}).get("value")) for x in (b.get("forecasts") or [])] if b else []
                pa_all = [(x.get("by") or x.get("method"), (x.get("p") or {}).get("value")) for x in (a.get("forecasts") or [])] if a else []
                print(f"    {i}: p {pval(b)} -> {pval(a)}; result total {b['result'].get('total_votes')} -> {a['result'].get('total_votes')}; "
                      f"differs in {what_differs(b, a)[:6]}")
                file_rows = [(r[5], r[6], r[7]) for r in g.get("records", []) if r[0] == i]
                rec_pairs = []
                for fb_, fa_ in zip(b.get("forecasts") or [], a.get("forecasts") or []):
                    vb, va = (fb_.get("p") or {}).get("value"), (fa_.get("p") or {}).get("value")
                    if vb is not None and va is not None:
                        rec_pairs.append((vb, va, round(va / vb, 6) if vb else None))
                top = (pval(b), pval(a), round(pval(a) / pval(b), 6) if pval(b) else None)
                print(f"      file rows (before, after, ratio): {file_rows}")
                print(f"      the record's own: published {top}; forecasts' p: {rec_pairs}")
        out[pr] = {"mine": dict(mine), "agree": agree, "dis": sum(dis.values()), "unlisted": sum(unlisted.values()), "listed_not_mine": len(listed_not_mine), "pdiff": pdiff, "rdiff": rdiff}
    return out


# ------------------------------------------------------------------------------------------ the New Jersey lists
def list_text(name):
    pdf = os.path.join(NJ, name)
    txt = os.path.join(NJ, "txt", name[:-4] + ".txt")
    if not os.path.exists(txt):
        os.makedirs(os.path.dirname(txt), exist_ok=True)
        subprocess.run(["pdftotext", "-layout", pdf, txt], check=True)
    with open(txt, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def parse_list(text):
    """The list as printed: pages (headed 'Official List' or not), the last page's candidate count, and the contests:
    {district, heading, counties, cands: [{name, w, star, party, lines: [(county, slogan, votes)], total}], total}.
    The Governor's list has no district heading: one contest, district None."""
    pages, contests, warn = [], [], []
    cur = cand = None
    cols = None
    tail = False
    in_bracket = False
    count = None
    for pg in text.split("\f"):
        lines = pg.split("\n")
        if not any(ln.strip() for ln in lines):
            continue
        first = next(ln for ln in lines if ln.strip())
        pages.append("Official List" in first)
        for ln in lines:
            s = ln.rstrip()
            if not s.strip():
                continue
            st = s.strip()
            if PAGE_RE.search(s) or st.startswith(("Candidates for ", "For GENERAL ELECTION")):
                continue
            m = re.match(r"^Name\s+(Address)\s+(Party)\s+(County)\s+(Slogan)\s+(Tally)", s)
            if m:
                cols = {k: m.start(i + 1) for i, k in enumerate(("addr", "party", "county", "slogan", "tally"))}
                continue
            if st.startswith("Candidate Totals for Party"):
                tail = True
                continue
            if tail:
                m = re.match(r"^Total Candidates\s+(\d+)$", st)
                if m:
                    count = int(m.group(1))
                continue
            if st == "Counties":
                continue
            m = HEAD_RE.match(s)
            if m:
                n = ORD.get(m.group(1))
                if n is None:
                    warn.append(f"ordinal not read: {m.group(1)}")
                if cur is not None and cur["district"] == n and cur["total"] is None:
                    continue   # the heading repeated at the top of a page, the contest going on
                cur = {"district": n, "heading": st, "counties": [c.strip() for c in m.group(2).split(" - ")], "cands": [], "total": None}
                contests.append(cur)
                cand = None
                continue
            m = TOTAL_RE.match(s)
            if m:
                v = int(m.group(1).replace(",", ""))
                if cand is not None and cand["total"] is None:
                    cand["total"] = v
                elif cur is not None:
                    if cur["total"] is not None:
                        warn.append(f"two contest totals in district {cur['district']}")
                    cur["total"] = v
                    cand = None
                else:
                    warn.append(f"a Total with no contest: {st}")
                continue
            m = COUNTY_RE.match(s)
            if m and cand is not None and not m.group(2).startswith(",") and m.start(1) >= (cols["county"] - 6 if cols else 60):
                # (an address line "UNION, NJ 07083" under a name is indented too, but at the Address column)
                rest = m.group(2)
                mv = re.search(r"([\d,]+)\s*$", rest)
                votes = int(mv.group(1).replace(",", "")) if mv else None
                slogan = rest[:mv.start()].strip() if mv else rest.strip()
                cand["lines"].append((m.group(1), slogan, votes))
                continue
            if s[0] != " ":
                if st.startswith("(bracketed"):
                    in_bracket = ")" not in st
                    continue
                if in_bracket:
                    in_bracket = ")" not in st
                    continue
                name_part = re.split(r"\s(?=\d|P\.O\.)", re.split(r"\s{2,}", st)[0])[0].rstrip()   # the name ends at a gap, or where an address runs into its column
                if cand is not None and cand["total"] is None and not cand["lines"]:
                    cand["raw"] += " " + name_part
                    continue
                if cand is not None and cand["total"] is None and norm_name(re.sub(r"\(w\)|\*", " ", name_part)) == norm_name(re.sub(r"\(w\)|\*", " ", cand["raw"])):
                    continue   # the candidate's block goes on past a page break, the name printed again
                if cur is None or (cur["district"] is None and cur["total"] is not None):
                    cur = {"district": None, "heading": None, "counties": list(NJ_COUNTIES), "cands": [], "total": None}
                    contests.append(cur)
                cand = {"raw": name_part, "party": party_text(st), "lines": [], "total": None}
                cur["cands"].append(cand)
                continue
            # an address line (indented, under the name) or anything else indented: not read
    for c in contests:
        for a in c["cands"]:
            raw = a.pop("raw")
            a["w"] = "(w)" in raw
            a["star"] = "*" in raw
            nm = re.sub(r"\(w\)|\*", " ", raw)
            nm = re.sub(r"-\s+", "-", nm)
            a["name"] = re.sub(r"\s+", " ", nm).strip()
    return {"pages": pages, "count": count, "contests": contests, "warnings": warn}


PARTIES = ("Democratic", "Republican", "Libertarian Party", "Socialist Workers Party", "Green Party", "Conservative Party")


def party_text(line):
    """The Party column of a candidate's first line: the text after the line's last gap of two or more spaces; where the
    address runs into it with one space, a known party's name at the end, else the words after the address's last
    numbered or 'Apt' token."""
    tail = re.split(r"\s{2,}", line.strip())[-1]
    for pn in PARTIES:
        if tail.lower().endswith(pn.lower()):
            return pn
    toks = tail.split()
    cut = 0
    for i, t in enumerate(toks):
        if re.search(r"\d", t) or t.startswith("Apt"):
            cut = i + 1
    return " ".join(toks[cut:])


def norm_name(s):
    return re.sub(r"[^A-Z0-9]", "", (s or "").upper())


def party_code(p):
    p = (p or "").strip().lower()
    return "D" if p == "democratic" else "R" if p == "republican" else p


def section_2():
    h1("40.2 New Jersey's gate from the five Official Lists, and every record against them")
    # (a) the pages: the links' text, from the Division's pages as fetched
    links = {}
    for y in ("2023", "2025"):
        with open(os.path.join(NJ, f"page-{y}.html"), encoding="utf-8", errors="replace") as fh:
            h = fh.read()
        for m in re.finditer(r'<a[^>]*href="([^"]*' + y + r'-official-general-results-[^"]*\.pdf)"[^>]*>(.*?)</a>', h, re.S | re.I):
            links[os.path.basename(m.group(1))] = html.unescape(re.sub(r"<[^>]+>|\s+", " ", m.group(2))).strip()
    idx = {}
    with open(os.path.join(NJ, "..", "index.txt")) as fh:
        for ln in fh:
            f = ln.rstrip("\n").split("\t")
            if len(f) >= 8 and f[0].startswith("nj:") and f[1] == "200":
                idx[os.path.basename(f[5])] = (f[6][:16], int(f[7]), f[4])
    parsed = {}
    for (y, level), name in sorted(LISTS.items()):
        P = parse_list(list_text(name))
        parsed[(y, level)] = P
        sha = hashlib.sha256(open(os.path.join(NJ, name), "rb").read()).hexdigest()[:16]
        n_c = sum(len(c["cands"]) for c in P["contests"])
        print(f"  {name}: linked as '{links.get(name)}' from election-information-{y}.shtml; fetched {idx.get(name, ('?',))[0]}... "
              f"({idx.get(name, (0, 0))[1]:,} bytes), sha256 {sha}...; pages {len(P['pages'])}, headed 'Official List' {sum(P['pages'])}; "
              f"contests {len(P['contests'])}, candidates read {n_c}, the last page's 'Total Candidates' {P['count']}"
              + (f"; warnings {P['warnings'][:3]}" if P["warnings"] else ""))
    # (b), (c) on the lists themselves
    h2("  (b) each candidate's county lines add to its Total, and the candidates' Totals to the contest's; (c) lines in the heading's counties")
    gate = {}
    for (y, level), P in sorted(parsed.items()):
        bad_b, bad_c, no_count, n_lines = [], [], [], 0
        for c in P["contests"]:
            heads = {re.sub(r"\s*\(part\)", "", x).strip().upper() for x in c["counties"]}
            tot = 0
            for a in c["cands"]:
                s = sum(v for _, _, v in a["lines"] if v is not None)
                n_lines += len(a["lines"])
                for cty, _, v in a["lines"]:
                    if v is None:
                        no_count.append((c["district"], a["name"], cty))
                    if cty not in heads:
                        bad_c.append((c["district"], a["name"], cty))
                if a["total"] is None or s != a["total"]:
                    bad_b.append((c["district"], a["name"], s, a["total"]))
                tot += a["total"] or 0
            if c["total"] is not None and c["total"] != tot:
                bad_b.append((c["district"], "contest", tot, c["total"]))
            if c["total"] is None and c["district"] is not None:
                bad_b.append((c["district"], "contest total missing", tot, None))
        gate[(y, level)] = (not bad_b, not bad_c)
        print(f"    {y} {level}: {n_lines:,} county lines over {len(P['contests'])} contests; (b) fails {len(bad_b)} {bad_b[:4]}; (c) lines outside the "
              f"heading's counties {len(bad_c)} {bad_c[:4]}; lines printed with no count {len(no_count)} {no_count[:3]}")
    # (d) the Governor's list against D2
    h2("  (d) the Governor's list of 2025: the same file as D2's, and equal to D2's record")
    gov = parsed[("2025", "governor")]["contests"]
    sha = hashlib.sha256(open(os.path.join(NJ, LISTS[("2025", "governor")]), "rb").read()).hexdigest()[:16]
    d2 = [c for c in L.load_json(os.path.join(L.DATA, "governor", "2025.json"))["contests"] if c["place"]["state"] == "NJ"][0]
    d2c = {norm_name(a["name"]): a for a in d2["result"]["candidates"]}
    print(f"    sha256 {sha} against D2's note {GOV_SHA}: {'equal' if sha == GOV_SHA else 'DIFFERENT'}; D2's note: {str(d2['result']['source'].get('note'))[:90]}")
    eq = []
    for a in gov[0]["cands"]:
        b = d2c.get(norm_name(a["name"]))
        eq.append((a["name"], a["party"], a["total"], (b or {}).get("votes"), (b or {}).get("party"), b is not None and b["votes"] == a["total"]))
    print(f"    the list's {len(gov[0]['cands'])} candidates against D2's {len(d2c)}: " + "; ".join(f"{n} ({p}) {t:,} = D2 {v} ({pp}) {'yes' if ok else 'NO'}" for n, p, t, v, pp, ok in eq))
    print(f"    totals: list {sum(a['total'] for a in gov[0]['cands']):,}; D2 total_votes {d2['result']['total_votes']:,}; D2's two-party votes {d2['two_party']['votes']}")
    # the records against the lists
    h2("  every record of data/state-upper and state-lower 2023 and 2025 NJ against the lists")
    out_lists = {}
    for (y, level), P in sorted(parsed.items()):
        if level == "governor":
            continue
        recs = {c["place"]["district"]: c for c in L.load_json(os.path.join(L.DATA, level, y, "NJ.json"))["contests"]}
        by_d = {str(c["district"]): c for c in P["contests"] if c["district"] is not None}
        tal = collections.Counter()
        bad = []
        for dn, rec in sorted(recs.items(), key=lambda kv: int(kv[0])):
            c = by_d.get(dn)
            if c is None:
                bad.append((rec["id"], "no contest in the list"))
                continue
            rc = rec["result"]["candidates"]
            lc = c["cands"]
            tal["contests"] += 1
            if len(rc) != len(lc):
                bad.append((rec["id"], f"candidates {len(rc)} record vs {len(lc)} list"))
            # match by votes and party, then the name and the marks
            used = set()
            for a in rc:
                hit = None
                for j, b in enumerate(lc):
                    if j in used:
                        continue
                    if b["total"] == a["votes"] and (party_code(b["party"]) == a["party"] if a["party"] in ("D", "R") else party_code(b["party"]) not in ("D", "R")):
                        hit = j
                        break
                if hit is None:
                    bad.append((rec["id"], f"{a['name']} {a['party']} {a['votes']}: no list candidate with that party and total"))
                    tal["candidates not matched"] += 1
                    continue
                used.add(hit)
                b = lc[hit]
                tal["candidates matched by party and total"] += 1
                if a["party"] not in ("D", "R") and party_code(b["party"]) != (a["party"] or "").lower():
                    tal["party text differs (minor)"] += 1
                    bad.append((rec["id"], f"party: record '{a['party']}' list '{b['party']}' ({b['name']})"))
                if norm_name(b["name"]) != norm_name(a["name"]):
                    tal["name differs"] += 1
                    bad.append((rec["id"], f"name: record '{a['name']}' list '{b['name']}'"))
                if bool(a.get("won")) != b["w"]:
                    tal["won mark differs"] += 1
                    bad.append((rec["id"], f"won: record {a.get('won')} list (w) {b['w']} {b['name']}"))
                if bool(a.get("incumbent")) != b["star"]:
                    tal["incumbent mark differs"] += 1
                    bad.append((rec["id"], f"incumbent: record {a.get('incumbent')} list * {b['star']} {b['name']}"))
            if rec["result"]["total_votes"] != (c["total"] if c["total"] is not None else sum(b["total"] for b in lc)):
                tal["total_votes differs"] += 1
                bad.append((rec["id"], f"total_votes record {rec['result']['total_votes']} list {c['total']}"))
            rn = [re.sub(r"\s+", " ", x).strip().upper() for x in rec["place"].get("counties_named") or []]
            if rn != [x.upper() for x in c["counties"]]:
                tal["counties_named differs"] += 1
                bad.append((rec["id"], f"counties record {rn} list {c['counties']}"))
            g = rec.get("gate") or {}
            tal[("gate fields", g.get("official"), g.get("parts_add_up"), g.get("counties_named"))] += 1
            inp = rec.get("forecast_inputs") or {}
            if inp.get("class"):
                inc = sum((1 if a["party"] == "D" else -1) for a in rc if a.get("incumbent") and a["party"] in ("D", "R"))
                tal[("inputs.incumbency = the list's marks", inc == inp.get("incumbency"))] += 1
        print(f"    {y} {level}: " + "; ".join(f"{k} {v}" for k, v in sorted(tal.items(), key=str)))
        if bad:
            print(f"      differences {len(bad)}: " + " | ".join(f"{i}: {s}" for i, s in bad[:8]))
        out_lists[f"{y}-{level}"] = [{"district": c["district"], "counties": c["counties"], "total": c["total"],
                                      "cands": [{"name": a["name"], "party": a["party"], "total": a["total"], "w": a["w"], "star": a["star"], "lines": a["lines"]} for a in c["cands"]]}
                                     for c in P["contests"]]
    with open(os.path.join(HERE, "c40-nj-lists.json"), "w") as fh:
        json.dump({"what": "New Jersey's Official Lists of 2023 and 2025 (State Senate, General Assembly; 2025's Senate 35th district), as c40_pr_checks.py reads them with pdftotext -layout: each contest's heading counties, each candidate's county lines (county, slogan, votes), Total, (w) and * marks, the contest Total",
                   "lists": out_lists}, fh, indent=0)
    print(f"  the lists as read: checks/m2/c40-nj-lists.json")
    # Virginia: the gate as D3 recorded it, not re-read
    cv = L.load_json(os.path.join(L.DATA, "local", "check-va-legislature.json"))
    print(f"\n  Virginia (REPORT section 28): the Department refused D3 at 18:27 UTC and its hosts are not asked again; the gate cannot be re-read here. "
          f"D3's check-va-legislature.json [stated]: keys {list(cv)[:8]}")
    for k, v in list(cv.items())[:6]:
        print(f"    {k}: {json.dumps(v)[:300]}")
    return gate


# ------------------------------------------------------------------------------------------ rows and pools at a commit
row_from_record = C15.row_from_record   # the eighth pass: shared with c15


_KROWS = None


def klarner_rows():
    global _KROWS
    if _KROWS is None:
        _KROWS = C15.klarner_rows()
    return _KROWS


def fit_rows_at(root, override=()):
    """Route (a)'s rows at a commit (c15.fit_rows on the records at the commit's worktree): Klarner's from his file, the
    records' where the source is not Klarner, and, for the state-years in override, the records' Klarner-sourced rows in
    place of the file's (for #95: New Hampshire and Idaho 2022)."""
    base, _ = klarner_rows()
    return C15.fit_rows(base, {lv: rows_at(root, lv) for lv in ("state-upper", "state-lower")}, override)


def fits_for(rows, years):
    out = {}
    for t in years:
        train = [r_ for r_ in rows if r_["year"] < t]
        M = C15.fit_partisan(train)
        out[t] = M if (M["s_a"] is not None and C15.cycle(t) in M["swing"]) else None
    return out


def p_partisan(M, r_, n):
    mean, sd, a = C15.predict(M, r_)
    p, use, f = D.p_auto(n, mean, sd)
    return p, mean, sd, a, use


_POOL = {}
HELD_OUT = C15.HELD_OUT   # the eighth pass: shared with c15
held_out = C15.held_out


def pool_at(root):
    """Like-race rows at a commit (c15.like_pool on the records at the commit's worktree), by class key -> [(year, s)]."""
    if root not in _POOL:
        pool, _, _ = C15.like_pool([r for level in ("state-upper", "state-lower") for r in rows_at(root, level)])
        by = collections.defaultdict(list)
        for y, key, s in pool:
            by[key].append((y, s))
        _POOL[root] = by
    return _POOL[root]


_DENS = {}


def density_at(root, t, key):
    k_ = (root, t, key)
    if k_ not in _DENS:
        sh = [s for y, s in pool_at(root).get(key, []) if y < t]
        _DENS[k_] = D.class_density(sh)
    return _DENS[k_]


def p_like(f, n):
    sd = D.sd_eq(f)
    use = D.method_rule(n, sd)
    if use == "exact":
        p = L.p_exact(n, 0.5, sd)
        if not (p > 0.0) or not math.isfinite(p):
            return f / (2.0 * n), "density (the exact sum underflowed)"
        return p, "exact"
    return f / (2.0 * n), "density"


def record_n(r):
    pr = r["pair"] or {}
    return pr.get("n_other_voters")


def p_of_record(root, r, fits):
    """My p for a record at a commit: route (a) from the fit of its year on the rows at that commit, routes (b)-(d) from
    the pool at that commit. (p, how) or (None, why)."""
    n = record_n(r)
    if r["route"] == "partisan":
        x = row_from_record(r)
        M = fits.get(r["year"])
        if x is None or M is None or n is None:
            return None, "no row, fit or n"
        p, mean, sd, a, use = p_partisan(M, x, n)
        return p, ("partisan", mean, sd, a, use)
    if r["route"] in ("class", "boundary", "runoff") and r["cls"]:
        f, N, h, k = density_at(root, r["year"], r["cls"])
        if f is None or n is None:
            return None, f"pool {N} < 100 or no n"
        p, use = p_like(f, n)
        return p, ("like", N, k, h, use)
    return None, f"route {r['route']}"


def section_3():
    h1("40.3 The new p of New Jersey's and Virginia's 2023 and 2025 legislatures from my own fit and pools (at HEAD)")
    root = L.ROOT
    rows, added = fit_rows_at(root)
    print(f"  fit rows at HEAD: {len(rows):,} (Klarner's file {len(klarner_rows()[0]):,}; added from the records: "
          + ", ".join(f"{y} {st} {src} {n}" for (y, st, src), n in sorted(added.items())) + ")")
    fits = fits_for(rows, (2023, 2024, 2025))
    _, by = klarner_rows()
    leans = {("NJ", 1, 2021): 0.0389, ("VA", 1, 2019): -0.0491, ("VA", 0, 2021): 0.0091}
    print("  the chambers' leans from Klarner's rows (mean D share of the chamber's route-(a) races at its last general, minus one half) against the records' inputs,")
    print("  and the same from the records of that chamber-year with a route-(a) forecast (the pipeline's rows follow the ballot; mine Klarner's dcand = rcand = 1, c15):")
    for (st, sen, y), rec in leans.items():
        v = by.get((st, sen, y))
        rr = [row_from_record(r) for r in rows_at(root, "state-upper" if sen else "state-lower") if r["year"] == y and r["state"] == st and r["route"] == "partisan"]
        rr = [x for x in rr if x]
        print(f"    {st} {'Senate' if sen else 'House'} {y}: mine {float(np.mean(v)) - 0.5:+.4f} over {len(v)} races; from the records {float(np.mean([x['y'] for x in rr])) - 0.5:+.4f} over {len(rr)}; record {rec:+.4f}")
    va23 = [row_from_record(r) for r in rows_at(root, "state-lower") if r["year"] == 2023 and r["state"] == "VA" and r["route"] == "partisan"]
    va23 = [x for x in va23 if x]
    print(f"    VA House 2023 (the lean of 2025's House): mine {float(np.mean([x['y'] for x in va23])) - 0.5:+.4f} over {len(va23)} races; record +0.0069")
    tal = collections.Counter()
    worst = []
    counts = collections.Counter()
    for level in ("state-upper", "state-lower"):
        for r in rows_at(root, level):
            if r["year"] not in (2023, 2025) or r["state"] not in ("NJ", "VA"):
                continue
            key = (r["year"], r["state"], level)
            counts[(key, r["route"] or r["status"], r["cls"] if r["route"] != "partisan" else (r["inputs"] or {}).get("class"))] += 1
            if r["status"] != "value":
                continue
            pr = r["p"]["value"]
            if pr == 0.0:
                named = [a for a in r["cands"] if a[0] != "write-in"]
                tal[(key, "p 0: one name per seat", len(named) <= (r["seats"] or 1))] += 1
                continue
            p, how = p_of_record(root, r, fits)
            if p is None:
                tal[(key, "mine none", how)] += 1
                continue
            ratio = p / pr
            band = ("within 1e-4" if abs(ratio - 1) <= 1e-4 else "within 1e-3" if abs(ratio - 1) <= 1e-3 else "within 1e-2" if abs(ratio - 1) <= 1e-2 else "beyond 1e-2")
            if how[0] == "partisan":
                _, mean, sd, a, use = how
                inp = r["inputs"] or {}
                sh = r["share"] or {}
                d_in = max(abs(mean - sh.get("mean", 9)), abs(sd - sh.get("sd", 9)), abs(a - inp.get("swing", 9)))
                b2 = ("inputs within 5e-5" if d_in <= TOL_P else "within 5e-4" if d_in <= 5e-4 else "within 5e-3" if d_in <= 5e-3 else "beyond 5e-3")
                tal[(key, "route (a)", (r["inputs"] or {}).get("class"), band, b2)] += 1
                if band in ("within 1e-2", "beyond 1e-2"):
                    worst.append((abs(ratio - 1), r["id"], f"mine p {p:.5g} mean {mean:.4f} sd {sd:.4f} swing {a:+.4f}; record {pr:.5g} {sh.get('mean')} {sh.get('sd')} {inp.get('swing')}"))
            else:
                _, N, k, h, use = how
                same = (N == r["N"], k == r["kin"], abs(h - D.window_h(r["win"])) < 1e-9)
                tal[(key, "like races", r["cls"][:40], band, f"N,k,h equal {same}")] += 1
                if not all(same) or band in ("within 1e-2", "beyond 1e-2"):
                    worst.append((abs(ratio - 1), r["id"], f"mine N {N} k {k} h {h} p {p:.5g}; record N {r['N']} k {r['kin']} h {D.window_h(r['win'])} p {pr:.5g}"))
    # the like-race pools: my N (rows before the year, by class) against the records' like_races
    seenN = {}
    for level in ("state-upper", "state-lower"):
        for r in rows_at(root, level):
            if r["year"] in (2023, 2025) and r["state"] in ("NJ", "VA") and r["route"] in ("class", "boundary") and r["N"]:
                f, N, h, k = density_at(root, r["year"], r["cls"])
                seenN.setdefault((r["year"], r["cls"]), collections.Counter())[(N, r["N"])] += 1
    print("  like-race pools, my rows before the year by class against the records' like_races (mine, record): count")
    for (y, cls), c in sorted(seenN.items()):
        print(f"    {y} '{cls[:70]}': " + ", ".join(f"({a}, {b}) {n}" for (a, b), n in sorted(c.items())))
    # Virginia's Senate of 2019: my 21 rows against the records' 20
    recs19 = {tuple(sorted((r["pair"] or {}).get("votes") or [])) for r in rows_at(root, "state-upper") if r["year"] == 2019 and r["state"] == "VA" and r["route"] == "partisan"}
    mine19 = [r_ for r_ in klarner_rows()[0] if r_["year"] == 2019 and r_["state"] == "VA" and r_["sen"] == 1]
    odd = [r_ for r_ in mine19 if tuple(sorted((r_["d"], r_["r"]))) not in recs19]
    print("  Virginia's Senate of 2019, my rows not among the records' route-(a) rows (by the D and R votes): "
          + "; ".join(f"district {r_['dist'][1]} D {r_['d']:,} R {r_['r']:,} others {r_['ocand']} with {r_['ovote']:,}" for r_ in odd))
    print("  the records by year, state, chamber, route and class:")
    for (key, route, cls), n in sorted(counts.items(), key=str):
        print(f"    {key[0]} {key[1]} {key[2]:12s} {str(route):14s} {str(cls)[:60]:60s} {n}")
    print("  my p against the record's (ratio bands; for route (a) the inputs' agreement: mean, sd, swing against the record's 4 decimals):")
    for k_, v in sorted(tal.items(), key=str):
        print(f"    {str(k_):150s} {v}")
    worst.sort(key=lambda x: -x[0])
    for _, rid, s in worst[:16]:
        print(f"    {rid}: {s}")
    print("  class C for the 2023 chambers [not read from a source]: the records say no last result on the same lines is read (New Jersey's 2021")
    print("  map against 2023's; Virginia's 2019 and 2021 regimes against 2023's). No page stating whether the lines are the same was read here")
    print("  either; the reading stands as D3 put it to the orchestrator (REPORT sections 27 and 28).")
    return fits


# ------------------------------------------------------------------------------------------ the moves from my refit
def section_4():
    h1("40.4 Every move from my own refit: the fit and the pools on the rows before and after each PR, p with each record's n, my ratio against the moves file's")
    specs = {"#92": ((), "New Jersey's 2023 Senate rows join the fit for 2024 (and 2025); its 2023 contests join the like races"),
             "#93": ((), "Virginia's 2023 rows join the fits; its contests join the like races"),
             "#95": (((2022, "NH"), (2022, "ID")), "New Hampshire's 2022 rows from the records (MEDSL's votes; the held ones left out), Idaho's 2022 from the records (county-total rows dropped)")}
    for pr, before, after, mvname in PRS:
        override, words = specs[pr]
        wb, wa = worktree(before), worktree(after)
        mv = L.load_json(os.path.join(L.DATA, "local", mvname))
        prow = {r[0]: r for r in mv["records"] if "P" in r[8]}
        h2(f"  {pr} ({words}): {len(prow):,} P rows in the file")
        rb, ab = fit_rows_at(wb, override)
        ra, aa = fit_rows_at(wa, override)
        years = sorted({r["year"] for lv in ("state-upper", "state-lower", "local") for r in rows_at(wa, lv) if r["status"] == "value" and r["route"] in ("partisan", "class", "boundary", "runoff")} & {2022, 2023, 2024, 2025})
        print(f"    fit rows before {len(rb):,} (added from records: {sum(ab.values())}), after {len(ra):,} (added {sum(aa.values())}); rows that differ by (year, state, source): "
              + ", ".join(f"{k} {aa.get(k, 0) - ab.get(k, 0):+d}" for k in sorted(set(ab) | set(aa)) if aa.get(k, 0) != ab.get(k, 0)) + "; fits for " + str(years))
        fb, fa = fits_for(rb, years), fits_for(ra, years)
        pb_, pa_ = pool_at(wb), pool_at(wa)
        dpool = {k: (sum(1 for _ in pb_.get(k, [])), sum(1 for _ in pa_.get(k, []))) for k in set(pb_) | set(pa_)}
        dpool = {k: v for k, v in dpool.items() if v[0] != v[1]}
        print(f"    like-race pool rows that differ, by class: " + "; ".join(f"'{k[:50]}' {a}->{b}" for k, (a, b) in sorted(dpool.items(), key=lambda kv: -abs(kv[1][1] - kv[1][0]))[:8]))
        before_by = {}
        for lv in ("state-upper", "state-lower", "local"):
            for r in rows_at(wb, lv):
                before_by[r["id"]] = r
        tal = collections.Counter()
        unreached = collections.Counter()
        diffs = []
        moved_unlisted = []
        n_mine_moved = 0
        for lv in ("state-upper", "state-lower", "local"):
            for r in rows_at(wa, lv):
                if r["status"] != "value" or r["route"] not in ("partisan", "class", "boundary", "runoff"):
                    continue
                r0 = before_by.get(r["id"])
                if r0 is None or r0["status"] != "value":
                    continue
                row = prow.get(r["id"])
                p0, how0 = p_of_record(wb, r0, fb)
                p1, how1 = p_of_record(wa, r, fa)
                if p0 is None or p1 is None or not p0:
                    if row:
                        tal[(lv, "P row, mine none", str(how0 if p0 is None else how1)[:40])] += 1
                    else:
                        unreached[(lv, r["route"])] += 1
                    continue
                mine = p1 / p0
                if row is None:
                    if abs(mine - 1) > 5e-4:
                        moved_unlisted.append((abs(mine - 1), r["id"], mine, r["route"]))
                    tal[(lv, "not a P row", "mine within 5e-4 of 1" if abs(mine - 1) <= 5e-4 else "mine moves")] += 1
                    continue
                theirs = row[7]
                if theirs is None:
                    theirs = row[6] / row[5] if row[5] else None
                if theirs is None:
                    tal[(lv, "P row with no ratio")] += 1
                    continue
                d = abs(mine - theirs)
                band = ("within 5e-4" if d <= 5e-4 else "within 5e-3" if d <= 5e-3 else "within 5e-2" if d <= 5e-2 else "beyond 5e-2")
                same_dir = (mine - 1) * (theirs - 1) > 0 or abs(mine - 1) <= 5e-4 or abs(theirs - 1) <= 5e-4
                tal[(lv, r["route"], band, "same direction" if same_dir else "opposite")] += 1
                n_mine_moved += 1
                if band in ("within 5e-2", "beyond 5e-2") or not same_dir:
                    diffs.append((d, r["id"], mine, theirs, r["route"], str(how1)[:60]))
        print(f"    P rows of the file with a p of mine before and after: {n_mine_moved:,} of {len(prow):,}; records not listed as P and not refitted here "
              f"(the local like-race routes' pools are local, not built in this check): " + ", ".join(f"{lv} {rt} {n:,}" for (lv, rt), n in sorted(unreached.items(), key=str)))
        for k_, v in sorted(tal.items(), key=str):
            print(f"      {str(k_):110s} {v:,}")
        diffs.sort(key=lambda x: -x[0])
        if diffs:
            print(f"    the largest differences between my ratio and the file's ({len(diffs)} beyond 5e-3 or in the other direction):")
            for d, rid, mine, theirs, route, how in diffs[:14]:
                print(f"      {rid}: mine x{mine:.4f}, file x{theirs:.4f} ({route}; {how})")
        moved_unlisted.sort(key=lambda x: -x[0])
        if moved_unlisted:
            print(f"    records my refit moves beyond 5e-4 that the file does not list as P: {len(moved_unlisted)}: "
                  + "; ".join(f"{rid} x{m:.4f} ({rt})" for _, rid, m, rt in moved_unlisted[:10]))
        # the P rows my refit did not reach, by level and year
        missing = collections.Counter()
        reached = set()
        for lv in ("state-upper", "state-lower", "local"):
            for r in rows_at(wa, lv):
                if r["id"] in prow:
                    reached.add(r["id"])
        for i, row in prow.items():
            if i not in reached:
                missing[row[1].split("/")[1]] += 1
        if missing:
            print(f"    P rows in levels my refit does not read: {dict(missing)}")
        forget(wb)


def main():
    print(f"C40 PR checks (#92, #93, #95); {L.git_head()}")
    for pr, b, a, _ in PRS:
        print(f"  {pr}: {b} -> {a}; worktree {worktree(a)}")
    section_1()
    section_2()
    section_3()
    section_4()


if __name__ == "__main__":
    main()
