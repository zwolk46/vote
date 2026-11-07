"""checks/m2/c31_statewide_filed_local.py: #82 (cbc4469, against 8b794e7): the statewide questions MEDSL files with
local offices, joined into one statewide record each from the state's own list; the rule citation chosen by who
proposed the question; the near-even note taken off a p at a threshold other than 1/2. The fourth pass (the
orchestrator, 2026-11-07 15:50: "the 35 joins (the lines add up to MEDSL's, and each is on its state's list, with a
sample of quotes); the 75 citations by proposer, checked against the rules' own texts; the 18 notes removed; the new
MT LR-130 p"; "the moves file should equal your own diff, and every moved p should be recomputed from your own pool").

  31.1 the two moves files (data/measure/moves-statewide-filed-local.json, moves-citations-notes.json) against my own
       diff of every record between 8b794e7 and cbc4469 [measured]
  31.2 the 35 joins: the joined record's votes are the sum, answer by answer, of the local lines it replaced (the
       records at 8b794e7), and, for the five states whose MEDSL files are read by git (2018 LA, AZ, WA; 2020 AL, MT),
       the lines themselves add up from MEDSL's own precinct rows [measured]; the state's printed total set beside
  31.3 each is on its state's list: the list page fetched again (checks/m2/fetch_fourth_pass.sh) and the record's
       quotes from it found word for word [measured]; quotes from other pages are counted, not checked
  31.4 the citations: pipeline/measures.py rule_for, proposer_of and _one written again here (copied, not
       imported) and run on every statewide question at cbc4469; the 75 moved citations before and after; the 28
       rules that carry a proposer against their own quoted texts, and a sample of their pages [measured]
  31.5 the 18 notes removed: a p at a threshold other than 1/2 carries no near-1/2 note; the back-test at those
       questions' own thresholds (lean_notes_statewide_own_threshold) from my pool [measured]
  31.6 MT LR-130's p and every statewide p that moved, recomputed from my own pool [measured]

Nothing in pipeline/ or model/ is imported. Run from the repository root: python3 checks/m2/c31_statewide_filed_local.py
"""
import collections
import csv
import io
import json
import os
import re
import subprocess
import sys
import zipfile

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402
import m2d3 as D  # noqa: E402
import c15_d3_refit as C15  # noqa: E402
import c16_notes as C16  # noqa: E402
import c28_governor_codes as C28  # noqa: E402
import c30_ballot_texts as C30  # noqa: E402

BEFORE = "8b794e7"   # #81 merged
AFTER = "cbc4469"    # #82 merged
FOURTH = os.path.join(L.CACHE, "fourth")
MOVES_J = "data/measure/moves-statewide-filed-local.json"
MOVES_C = "data/measure/moves-citations-notes.json"
LISTED = "data/measure/statewide-filed-local.json"
rel = C30.rel
at = C30.at


def changed_files(a, b, under="data/measure/"):
    r = subprocess.run(["git", "diff", "--name-only", a, b, "--", under], capture_output=True, text=True, cwd=L.ROOT)
    return [x for x in r.stdout.split("\n") if x]


def record_files(commit):
    r = subprocess.run(["git", "ls-tree", "-r", "--name-only", commit, "data/measure/"], capture_output=True, text=True, cwd=L.ROOT)
    return sorted(x for x in r.stdout.split("\n") if re.search(r"data/measure/\d{4}/[A-Z]{2}\.json$", x))


def deep_paths(a, b, prefix="", depth=0):
    """the dotted paths at which two JSON values differ, to depth 2 below a record's top"""
    if a == b:
        return []
    if isinstance(a, dict) and isinstance(b, dict) and depth < 2:
        out = []
        for k in sorted(set(a) | set(b)):
            out += deep_paths(a.get(k), b.get(k), f"{prefix}{k}.", depth + 1)
        return out
    return [prefix.rstrip(".")]


def load_records(commit, files):
    out = {}
    for f in files:
        d = at(commit, f)
        for c in (d or {}).get("contests", []):
            out[c["id"]] = c
    return out


def fetched(by="url"):
    """url (or key) -> path of the pages checks/m2/fetch_fourth_pass.sh fetched (HTTP 200 only)"""
    out = {}
    p = os.path.join(FOURTH, "index.txt")
    if not os.path.exists(p):
        return out
    for line in open(p):
        f = line.rstrip("\n").split("\t")
        if len(f) >= 6 and f[1] == "200" and os.path.exists(f[5]):
            out[f[4] if by == "url" else f[3]] = f[5]
    return out


# the record names some quotes' pages by a cache file only; these two are Washington's results sub-pages, fetched by key
SUB_PAGES = {"wa-results-20241105-Measures-All": "list-all:WA:2024", "wa-results-20181106-AV19": "measure:WA:2018:AV19"}


def medsl_zips():
    """year -> path of MEDSL's own file, read by git into the cache (fetch_fourth_pass.sh)"""
    out = {}
    p = os.path.join(FOURTH, "index.txt")
    if os.path.exists(p):
        for line in open(p):
            f = line.rstrip("\n").split("\t")
            if f[0] == "medsl" and len(f) >= 4 and os.path.exists(f[3]):
                m = re.search(r"/(\d{4})-", f[3])
                out.setdefault(int(m.group(1)), []).append(f[3])
    return out


# ---------------------------------------------------------------------------------------------- 31.1
def section_1():
    print("### 31.1 the moves files against my own diff of the records, 8b794e7 to cbc4469")
    allf = changed_files(BEFORE, AFTER)
    recf = [x for x in allf if re.search(r"data/measure/\d{4}/[A-Z]{2}\.json$", x)]
    print(f"  files changed under data/measure: {len(allf)}; record files {len(recf)}; others: "
          + ", ".join(x.rsplit('/', 1)[-1] for x in allf if x not in recf))
    before, after = load_records(BEFORE, recf), load_records(AFTER, recf)
    gone, new = set(before) - set(after), set(after) - set(before)
    changed = {}
    for cid in set(before) & set(after):
        if before[cid] != after[cid]:
            changed[cid] = deep_paths(before[cid], after[cid])
    mj = json.loads(subprocess.run(["git", "show", f"{AFTER}:{MOVES_J}"], capture_output=True, text=True, cwd=L.ROOT).stdout)
    mc = json.loads(subprocess.run(["git", "show", f"{AFTER}:{MOVES_C}"], capture_output=True, text=True, cwd=L.ROOT).stdout)
    joined = {j["id"]: j for j in mj["joined"]}
    replaced = {r for j in mj["joined"] for r in j["replaces"]}
    other = {o["id"]: o for o in mj["other_changes"]}
    cit = {r["id"]: r for r in mc["records"]}
    print(f"  my diff: {len(new)} new records, {len(gone)} gone, {len(changed)} changed; the moves file: {len(joined)} joined "
          f"(replacing {len(replaced)}), {len(other)} other changes; the citations file: {len(cit)} records "
          f"(taken against {mc.get('taken_against')}; the joins against {mj.get('taken_against')})")
    print(f"  new == joined ids: {new == set(joined)}; gone == the replaced ids: {gone == replaced}"
          + ("" if gone == replaced else f" (gone not listed {len(gone - replaced)}, listed not gone {len(replaced - gone)})"))
    # what changed, by path set
    tal = collections.Counter(tuple(v) for v in changed.values())
    print("  changed records by the paths that differ:")
    for paths, n in tal.most_common():
        print(f"    {n:4d}  {', '.join(paths)}")
    mine_p = {cid for cid, v in changed.items() if any(x.startswith("p") for x in v)}
    print(f"  records whose p block changed: {len(mine_p)}; in other_changes {len(mine_p & set(other))}, in the citations file "
          f"{len(mine_p & set(cit))}, in both {len(mine_p & set(other) & set(cit))}, in neither {len(mine_p - set(other) - set(cit))}")
    sub = lambda p, keys: {k: (p or {}).get(k) for k in keys}  # noqa: E731
    ok = sum(1 for cid, o in other.items() if cid in changed and o["p"] == [sub(before[cid].get("p"), o["p"][0]), sub(after[cid].get("p"), o["p"][1])])
    print(f"  other_changes: p [before, after] equals the records' on the keys it gives in {ok} of {len(other)}; ids not in my diff: {len(set(other) - set(changed))}")
    # the citations file, record by record
    okc = collections.Counter()
    for cid, r in cit.items():
        b, a = before.get(cid), after.get(cid)
        if b is None or a is None:
            okc["id not in both commits"] += 1
            continue
        tb, ta = b.get("threshold") or {}, a.get("threshold") or {}
        pb, pa = b.get("p") or {}, a.get("p") or {}
        good = True
        if "citation" in r:
            good &= r["citation"] == [tb.get("citation"), ta.get("citation")]
        if "matched" in r:
            good &= r["matched"] == ta.get("matched")
        if "note" in r:
            good &= r["note"] == [pb.get("note"), pa.get("note")] and r.get("t") == ta.get("t")
        if "not_computed" in r:
            good &= r["not_computed"] == [pb.get("not_computed"), pa.get("not_computed")]
        if "proposer" in r:
            bt = (a.get("ballot_text") or {})
            good &= r["proposer"] in json.dumps(bt) or r["proposer"] in json.dumps(a.get("listed_statewide") or {})
        okc["equal to the records" if good else "DIFFERS"] += 1
        if not good:
            print(f"    differs: {cid} {json.dumps(r)[:160]}")
    print(f"  the citations file's 75 against the records: {dict(okc)}")
    A = {cid for cid, v in changed.items() if any(x.startswith("threshold") or x.startswith("ballot_text") for x in v)}
    B = {cid for cid, v in changed.items() if "p.note" in v and (after[cid].get("p") or {}).get("note") is None and (before[cid].get("p") or {}).get("note")}
    Cn = {cid for cid, v in changed.items() if "p.not_computed" in v and not ((after[cid].get("p") or {}).get("not_computed") or "").startswith("fewer than")}
    cA = {cid for cid, r in cit.items() if "citation" in r or "matched" in r or "proposer" in r}
    cB = {cid for cid, r in cit.items() if "note" in r}
    cC = {cid for cid, r in cit.items() if "not_computed" in r}
    print(f"  the citations file's three kinds against my diff: threshold or ballot-text changes {len(A)} == its citation/matched/proposer records {len(cA)}: {A == cA}; "
          f"near-1/2 note taken off {len(B)} == its note records {len(cB)}: {B == cB}; a reason that cites a rule changed {len(Cn)} == its not_computed records {len(cC)}: {Cn == cC}")
    stamps = {cid for cid, v in changed.items() if v == ["p.commit"]}
    unexplained = set(changed) - set(other) - set(cit) - stamps
    print(f"  changed records in neither moves file: {len(unexplained)}" + (f": {sorted(unexplained)[:6]}" if unexplained else "")
          + f"; records whose p.commit stamp alone changed: {len(stamps)} ({dict(collections.Counter(cid[:4] + ' ' + cid.split('-')[2] for cid in stamps))})")
    return before, after, mj, mc


# ---------------------------------------------------------------------------------------------- 31.2
def read_medsl(path, st, offices, answers, date):
    """MEDSL's own precinct rows of one zip (read in place): county fips -> answer -> votes, for the rows of the state
    whose office is one the record was filed under and whose candidate is one of its answers; one precinct's votes for
    one answer are its TOTAL row where it has one, else the sum of its modes (as pipeline/intake/medsl_precinct.py
    reads them; copied here, not imported). A redacted count ('*') is counted as missing."""
    cells = collections.defaultdict(dict)   # (office, county, jurisdiction, precinct, answer) -> mode -> votes
    missing = 0
    with zipfile.ZipFile(path) as z:
        for member in z.namelist():
            if not member.lower().endswith((".csv", ".tab", ".txt")) or member.startswith("__MACOSX"):
                continue
            with z.open(member) as raw:
                delim = "\t" if member.lower().endswith(".tab") else ","
                for row in csv.DictReader(io.TextIOWrapper(raw, encoding="utf-8", errors="replace"), delimiter=delim):
                    if row.get("state_po", "") != st or (row.get("dataverse") or "").upper() != "LOCAL":
                        continue
                    office = " ".join((row.get("office") or "").upper().split())
                    if office not in offices:
                        continue
                    cand = " ".join((row.get("candidate") or "").upper().split())
                    if cand not in answers:
                        continue
                    if row.get("date") and row["date"] != date:
                        continue
                    if row.get("stage") and row["stage"] != "GEN":
                        continue
                    v = (row.get("votes") or "").strip()
                    try:
                        votes = int(float(v))
                    except ValueError:
                        missing += 1
                        continue
                    cf = (row.get("county_fips") or "").strip()
                    if re.fullmatch(r"\d{1,5}(\.0+)?", cf):
                        cf = f"{int(float(cf)):05d}"
                    key = (office, cf, row.get("jurisdiction_fips", ""), row.get("precinct", ""), cand)
                    mode = (row.get("mode") or "TOTAL").upper()
                    cells[key][mode] = cells[key].get(mode, 0) + votes
    out = collections.defaultdict(collections.Counter)   # (office, county) -> answer -> votes
    for (office, cf, _j, _p, cand), modes in cells.items():
        out[(office, cf)][cand] += modes["TOTAL"] if "TOTAL" in modes else sum(modes.values())
    return out, missing


def section_2(before, after, mj):
    print("### 31.2 the 35 joins: the joined record's votes are the sum of the lines it replaced, and the lines add up from MEDSL's own files")
    listed = {(q["state"], q["year"], q["title"]): q for q in json.loads(subprocess.run(["git", "show", f"{AFTER}:{LISTED}"], capture_output=True, text=True, cwd=L.ROOT).stdout)["questions"]}
    zips = medsl_zips()
    tal = collections.Counter()
    src = collections.Counter()
    by_state = collections.defaultdict(list)
    for j in mj["joined"]:
        a = after[j["id"]]
        reps = [before[r] for r in j["replaces"]]
        votes = collections.Counter()
        for r in reps:
            for x in r["result"]["candidates"]:
                votes[x["name"].upper()] += x["votes"]
        mine = dict(votes)
        rec = {x["name"].upper(): x["votes"] for x in a["result"]["candidates"]}
        ls = a.get("listed_statewide") or {}
        yes, no = C27_yes_no(a)
        share = round(yes / (yes + no), 6) if yes + no else None
        same = (mine == rec, ls.get("lines_joined") == len(reps) == j["lines_joined"], share == a["result"].get("yes_share") == j.get("yes_share"),
                sum(r["result"].get("total_votes") or 0 for r in reps) == a["result"].get("total_votes"))
        tal["votes, lines, yes share and total all equal" if all(same) else f"DIFFERS {same}"] += 1
        if not all(same):
            print(f"    {j['id'][:60]}: mine {mine} share {share}; record {rec} share {a['result'].get('yes_share')} lines {ls.get('lines_joined')}")
        # the state's printed total beside MEDSL's sum
        q = listed.get((a["place"]["state"], a["year"], a["question"]["title"]))
        stt = (q or {}).get("state_total") or {}
        if stt.get("votes"):
            less = {k: rec.get(k, 0) - v for k, v in stt["votes"].items()}
            agrees = all(v == 0 for v in less.values())
            r_less, r_agrees = (ls.get("state_total") or {}).get("medsl_less_state"), (ls.get("state_total") or {}).get("agrees")
            tal["state total: my MEDSL-less-state and agrees equal the record's and the moves file's" if (less == r_less == j.get("medsl_less_state") and agrees == r_agrees == j.get("state_total_agrees")) else "state total: DIFFERS"] += 1
            if not (less == r_less):
                print(f"    {j['id'][:60]}: state total less {less}; record {r_less}; moves {j.get('medsl_less_state')}")
        else:
            tal["no state total printed on the page read"] += 1
        by_state[(a["place"]["state"], a["year"])].append((j, a, reps))
    print(f"  {len(mj['joined'])} joins: {dict(tal)}")
    # the lines themselves, from MEDSL's own files where read by git
    for (st, year), items in sorted(by_state.items(), key=lambda x: (x[0][1], x[0][0])):
        paths = [p for p in zips.get(year, []) if year == 2020 or f"-{st.lower()}-" in p]
        if not paths:
            print(f"  {st} {year}: {len(items)} joined questions, {sum(len(x[2]) for x in items)} lines; MEDSL's file not read here "
                  f"({'a Dataverse set' if year in (2016, 2022, 2024) else 'not fetched'}): the sums above stand on the records at 8b794e7")
            continue
        offices = {o.upper() for j, a, reps in items for o in (listed.get((st, year, a["question"]["title"])) or {}).get("offices_as_filed", [])}
        answers = {x["name"].upper() for j, a, reps in items for x in a["result"]["candidates"]}
        date = items[0][1].get("date")
        for p in paths:
            rows, missing = read_medsl(p, st, offices, answers, date)   # read once per state and year
            if not rows:
                continue
            line_ok = line_bad = tot_ok = tot_bad = 0
            for j, a, reps in items:
                q = listed.get((st, year, a["question"]["title"])) or {}
                offs = {" ".join(o.upper().split()) for o in q.get("offices_as_filed", [])}
                for r in reps:   # a line: one record at 8b794e7, filed under one office, over its counties
                    office = " ".join(r["question"]["title"].upper().split())
                    ctys = r["place"].get("counties") or []
                    mine = collections.Counter()
                    for (o, cf), v in rows.items():
                        if o == office and (not ctys or cf in ctys):
                            mine.update(v)
                    rec = {x["name"].upper(): x["votes"] for x in r["result"]["candidates"]}
                    if dict(mine) == rec:
                        line_ok += 1
                    else:
                        line_bad += 1
                        if line_bad <= 3:
                            print(f"    line differs: {r['id'][:70]} ({office[:30]}, {len(ctys)} counties): MEDSL's file {dict(mine)}; the record {rec}")
                total = collections.Counter()
                for (o, cf), v in rows.items():
                    if o in offs:
                        total.update(v)
                rec = {x["name"].upper(): x["votes"] for x in a["result"]["candidates"]}
                if dict(total) == rec:
                    tot_ok += 1
                else:
                    tot_bad += 1
                    print(f"    total differs: {j['id'][:70]}: MEDSL's file {dict(total)}; the joined record {rec}")
            print(f"  {st} {year} from {os.path.basename(p)}: {len(items)} questions; lines equal to MEDSL's precinct rows added up over the line's counties "
                  f"{line_ok}, differing {line_bad}; joined totals equal {tot_ok}, differing {tot_bad}; redacted counts skipped {missing}")
            src[(st, year)] += 1
    print(f"  MEDSL's own files read for {len(src)} state-years: {sorted(src)}")


def C27_yes_no(c):
    import c27_local_thresholds as C27
    return C27.yes_no(c)


# ---------------------------------------------------------------------------------------------- 31.3
def stem(name):
    b = os.path.basename(name or "")
    for suf in (".raw.txt", ".flow.txt", ".txt", ".html", ".htm", ".pdf"):
        if b.endswith(suf):
            b = b[: -len(suf)]
            break
    return b


def loose(x):
    return " ".join(re.sub(r"[^A-Za-z0-9]+", " ", x).upper().split())


def find_quote(quote, readings):
    q = C28.norm(quote)
    for label, text in readings:
        if q in text:
            return label
    lq = loose(q)
    for label, text in readings:
        if lq and lq in loose(text):
            return label + ", punctuation and case aside"
    nq = q.replace(" ", "")
    for label, text in readings:
        if nq and nq in text.replace(" ", ""):
            return label + ", spaces aside"
    return None


def section_3():
    print("### 31.3 each joined question on its state's list: the list fetched again, the record's quotes found on it")
    listed = json.loads(subprocess.run(["git", "show", f"{AFTER}:{LISTED}"], capture_output=True, text=True, cwd=L.ROOT).stdout)["questions"]
    pages = fetched()
    by_key = fetched("key")
    cache = {}
    tal = collections.Counter()
    other = collections.Counter()
    by_label = collections.Counter()
    for q in listed:
        url = (q.get("list") or {}).get("url")
        path = pages.get(url)
        if not path:
            tal["list page not fetched"] += 1
            continue
        if path not in cache:
            cache[path] = C30.readings(path)
        lstem = stem((q.get("list") or {}).get("cache_file"))
        stt = q.get("state_total") or {}
        cert = stt.get("certified") or {}
        items = [("quote", q.get("quote"), q.get("quote_file")), ("type_quote", q.get("type_quote"), q.get("type_quote_file")),
                 ("statewide.quote", (q.get("statewide") or {}).get("quote"), (q.get("statewide") or {}).get("quote_file")),
                 ("proposer.quote", (q.get("proposer") or {}).get("quote"), (q.get("proposer") or {}).get("quote_file")),
                 ("fact.quote", (q.get("fact") or {}).get("quote"), (q.get("fact") or {}).get("quote_file")),
                 ("state_total.quote", stt.get("quote"), stt.get("quote_file") or stt.get("cache_file")),
                 ("certified.quote", cert.get("quote"), cert.get("quote_file") or (cert.get("source") or {}).get("cache_file"))]
        for label, quote, qf in items:
            if not quote:
                continue
            fs = stem(qf)
            if fs == lstem:
                rd = cache[path]
            elif fs in SUB_PAGES and by_key.get(SUB_PAGES[fs]):
                sp = by_key[SUB_PAGES[fs]]
                if sp not in cache:
                    cache[sp] = C30.readings(sp)
                rd = cache[sp]
                label += " (sub-page)"
            else:
                other[label] += 1
                continue
            got = find_quote(quote, rd)
            if got:
                tal[f"{label}: found"] += 1
                by_label[got] += 1
            else:
                tal[f"{label}: NOT FOUND"] += 1
                print(f"    not found: {q['state']} {q['year']} {q['title'][:40]} {label}: {quote[:90]!r}")
    print(f"  {len(listed)} listed questions; list pages fetched {len({pages.get((q.get('list') or {}).get('url')) for q in listed} - {None})} of {len({(q.get('list') or {}).get('url') for q in listed})} distinct, "
          f"and Washington's two results sub-pages")
    print(f"  quotes from the list page itself (or Washington's sub-page): {dict(sorted(tal.items()))}")
    print(f"  how found: {dict(by_label)}")
    print(f"  quotes from another page the record names by its cache file only (not fetched, not checked): {dict(other)}")


# ---------------------------------------------------------------------------------------------- 31.4
# pipeline/measures.py's proposer words, copied (the orchestrator, 14:36: cite the rule that governs each question by
# its kind)
_PROPOSER_WORDS = (("initiative", r"INITIATIVE PETITION|PROPOSED BY INITIATIVE|CONSTITUTIONAL INITIATIVE|\bCI-\d|"
                                  r"\bINITIATIVE (MEASURE )?(NO\.? ?)?\d|LEGISLATIVE INITIATIVE|\bINITIATED\b"),
                   ("legislature", r"LEGISLATIVE REFERENDUM|\bLR-?\d|REFERRED BY THE (LEGISLATURE|LEGISLATIVE ASSEMBLY|"
                                   r"GENERAL ASSEMBLY)|\b[HS]JR ?\d|\(ACT (NO\. )?\d+[^)]*\b[HS]B ?\d+"))


def proposer_of(title, subject, text):
    pr = (text or {}).get("proposer")
    if pr:
        return pr["who"], (f"[{pr['mark']}: {text.get('said_by', 'the ballot text read')}, "
                           f"{text.get('file', 'data/measure/ballot-texts.json')}]")
    t = " ".join((title + " " + (subject or "")).upper().split())
    hits = {who for who, pat in _PROPOSER_WORDS if re.search(pat, t)}
    return (hits.pop(), "[stated: the title's words]") if len(hits) == 1 else (None, None)


def one(rs, how, who=None):
    """pipeline/measures.py _one, written again: (rule with citation and also_governs, how, None) or (None, None, why)"""
    seen, cands = set(), []
    for r in rs:
        if r["citation"] not in seen:
            seen.add(r["citation"]); cands.append(r)
    parts = [set(x["citation"].split("; ")) for x in cands]
    cands = [x for i, x in enumerate(cands) if not any(j != i and parts[i] < parts[j] for j in range(len(cands)))]
    whom, narrowed = (who[0] if who else None), False
    if whom and len(cands) > 1:
        fit = [r for r in cands if whom in (r.get("proposer") or [])]
        if fit:
            n0 = len(cands)
            cands = fit + [r for r in cands if not r.get("proposer")]
            narrowed = len(cands) < n0
    r = cands[0]
    cite = r["citation"] if len(cands) == 1 else ", or ".join(x["citation"] for x in cands)
    if r.get("compound") or r.get("t") is None:
        return None, None, (f"{cite}" + (" (the source does not show which of these governs it)" if len(cands) > 1 else "")
                            + f": {r.get('compound') or r.get('rule')}: the threshold turns on more than the yes share of "
                            f"those voting on the question, and the model forecasts that share only")
    if narrowed and len(cands) == 1:
        how += f"; proposed by the {whom} {who[1]}, so {r['citation']} governs ({r['applies_to']})"
    elif len(cands) > 1:
        how += ("; the source does not show which of these governs it (" + "; ".join(
            f"{x['citation']}: {x['applies_to']}" for x in cands) + "), and each sets this share")
        r = dict(r, citation=cite, also_governs=[x["citation"] for x in cands[1:]])
    return r, how, None


def rule_for(c, book, texts, listed):
    """pipeline/measures.py rule_for, written again on a record: (citation, also_governs, matched, None) or
    (None, None, None, the reason)"""
    q = c["question"]
    title, subject, st, year = q["title"], q.get("subject"), c["place"]["state"], c["year"]
    kind = q.get("kind") or "measure"
    text = texts.get(c["id"])
    if text is None and c.get("listed_statewide") is not None:
        lq = listed.get((st, year, title)) or {}
        text = {"type": lq.get("type"), "type_mark": lq.get("type_mark"), "proposer": lq.get("proposer"),
                "fact": lq.get("fact"), "said_by": "the state's list of its statewide measures",
                "file": "data/measure/statewide-filed-local.json"}
    who = proposer_of(title, subject, text)
    who = who if who[0] else None
    states = book.get("states", {})
    in_year = lambda r: (r.get("from_year") or 0) <= year <= (r.get("to_year") or 9999)  # noqa: E731
    mine = [r for r in book["rules"] if r["state"] == st and in_year(r) and r.get("scope") != "local"]
    if not mine:
        why = (states.get(st) or {}).get("not_read")
        return None, None, None, (f"the thresholds of this state's {kind}s are not read: {why}" if why else
                                  f"the thresholds of this state's {kind}s are not read from its constitution or statute for {year}")
    if kind == "retention":
        rs = [r for r in mine if r["type"] == "retention"]
        if not rs:
            return None, None, None, "the threshold of this state's judicial retentions is not read"
        r, how, why = one(rs, "retention")
        return (r["citation"], r.get("also_governs", []), how, None) if r else (None, None, None, why)
    ty = C30.title_type(title, subject)
    tty = (text or {}).get("type")
    if tty and tty != ty:
        said = "states" if text.get("type_mark") == "stated" else f"shows [{text.get('type_mark')}]"
        how_t = (f"by the type {text.get('said_by', 'the ballot text')} {said} ({tty}; "
                 f"{text.get('file', 'data/measure/ballot-texts.json')})" + (f", not the title's ({ty})" if ty is not None else ""))
        ty = tty
    else:
        how_t = None
    if ty == "advisory":
        return None, None, None, "an advisory question: the law read sets no threshold for it"
    pool = [r for r in mine if r["type"] != "retention"]
    if not pool:
        return None, None, None, f"the thresholds of this state's measures are not read for {year}"
    if ty is not None:
        pool = [r for r in pool if r["type"] == ty]
        if not pool:
            return None, None, None, f"the threshold of this state's {ty}s is not read"
        how = how_t or f"by the type the source's title states ({ty})"
    else:
        if not (states.get(st) or {}).get("complete"):
            return None, None, None, ("the source's title does not give the measure's type, and the rules read for this "
                                      "state do not cover every kind of statewide question it puts to voters")
        pool = [r for r in pool if r["type"] != "convention"]
        how = ("the source's title does not give the type; every rule read for the state's measures (but its "
               "convention question) sets this threshold")
    general = [r for r in pool if not r.get("only_if")]
    special = [r for r in pool if r.get("only_if")]
    form = lambda r: (r.get("t"), r.get("compound"))  # noqa: E731
    fact = (text or {}).get("fact") or {}
    if special and fact.get("applies") is not None:
        pick = special if fact["applies"] else general
        if pick and len({form(r) for r in pick}) == 1 and len({r["only_if"] for r in special}) == 1:
            r, how2, why = one(pick, f"{how}; {text.get('said_by', 'the ballot text')} shows it is "
                                     f"{'' if fact['applies'] else 'not '}{special[0]['only_if']} [{fact['mark']}] "
                                     f"({text.get('file', 'data/measure/ballot-texts.json')})", who)
            return (r["citation"], r.get("also_governs", []), how2, None) if r else (None, None, None, why)
    unshown = ("; its ballot text, read in step (a), does not show it either (data/measure/ballot-texts.json)"
               if text and not text.get("said_by") else "")
    if not general:
        return None, None, None, (f"the general threshold is not read; {special[0]['citation']} covers only "
                                  f"{special[0]['only_if']}" + (unshown if special and fact.get("applies") is None else ""))
    if all(r.get("compound") or r.get("t") is None for r in general):
        r, how2, why = one(general, how, who)
        return (r["citation"], r.get("also_governs", []), how2, None) if r else (None, None, None, why)
    if len({form(r) for r in general}) > 1:
        return None, None, None, ("the state's law sets different thresholds for different kinds of measure, and the "
                                  "source's title does not show which kind this is")
    other = [r for r in special if form(r) != form(general[0])]
    if other:
        return None, None, None, (f"{other[0]['citation']} sets another threshold for {other[0]['only_if']}, and the "
                                  f"source does not show whether this measure is one" + unshown)
    r, how2, why = one(general, how, who)
    return (r["citation"], r.get("also_governs", []), how2, None) if r else (None, None, None, why)


FIRST_REASONS = ("fewer than", "no yes or no", "the source", "not computed in this step", "a local measure", "the model")
PROPOSER_WORDS_IN_LAW = {"initiative": r"initiat|petition", "legislature": r"legislat|general assembly|each house|both houses|council",
                         "referendum": r"referend|referred|refer", "revision": r"revis"}


def section_4(before, after, mc):
    print("### 31.4 the citations: rule_for written again on every statewide question at cbc4469; the 75 moved; the proposer rules' own texts")
    book = json.loads(subprocess.run(["git", "show", f"{AFTER}:data/measure/thresholds.json"], capture_output=True, text=True, cwd=L.ROOT).stdout)
    texts = json.loads(subprocess.run(["git", "show", f"{AFTER}:data/measure/ballot-texts.json"], capture_output=True, text=True, cwd=L.ROOT).stdout)["questions"]
    listed = {(q["state"], q["year"], q["title"]): q for q in json.loads(subprocess.run(["git", "show", f"{AFTER}:{LISTED}"], capture_output=True, text=True, cwd=L.ROOT).stdout)["questions"]}
    recs = load_records(AFTER, record_files(AFTER))
    sw = [c for c in recs.values() if c.get("question") and c["question"].get("scope") == "statewide"]
    tal = collections.Counter()
    bad = []
    narrowed = collections.Counter()
    first = collections.Counter()
    for c in sw:
        cite, also, how, why = rule_for(c, book, texts, listed)
        th = c.get("threshold") or {}
        p = c.get("p") or {}
        if cite is not None and not th.get("citation") and (p.get("not_computed") or "").startswith(FIRST_REASONS):
            tal["a rule by me; the record's reason comes before the rule in the pipeline (a source, count or step reason), no threshold block"] += 1
            first[(p.get("not_computed") or "")[:45]] += 1
            continue
        if cite is not None:
            rec_also = [x.get("citation") for x in th.get("also_governs") or []]
            same = (th.get("citation") == cite, rec_also == also, th.get("matched") == how)
            tal["rule: citation, also_governs and matched text equal" if all(same) else f"rule: DIFFERS {same}"] += 1
            if not all(same):
                bad.append((c["id"], cite, th.get("citation"), how[:80], (th.get("matched") or "")[:80]))
            if "proposed by the" in how:
                narrowed[c["place"]["state"]] += 1
        else:
            rec_why = p.get("not_computed") or ""
            if th.get("citation"):
                tal["mine: no rule; record: a citation"] += 1
                bad.append((c["id"], why[:60], th.get("citation"), "", ""))
            elif rec_why == why:
                tal["no rule, the same reason word for word"] += 1
            elif rec_why.startswith(FIRST_REASONS):
                tal["no rule by me; the record's reason comes before the rule in the pipeline (a source, count or step reason)"] += 1
            else:
                tal["no rule, reason DIFFERS"] += 1
                bad.append((c["id"], why[:70], rec_why[:70], "", ""))
    print(f"  {len(sw)} statewide questions and retentions: {dict(tal)}")
    print(f"    the reasons that come before the rule: {dict(first)}")
    for b in bad[:40]:
        print(f"    {b[0][:60]} | mine {b[1]} | record {b[2]} | {b[3]} | {b[4]}")
    print(f"  citations narrowed by the proposer ('proposed by the ...' in matched), by state: {dict(sorted(narrowed.items()))}; total {sum(narrowed.values())}")
    also_n = sum(1 for c in sw if (c.get("threshold") or {}).get("also_governs"))
    print(f"  records citing every rule that could govern (also_governs): {also_n}")
    # the 75: before and after
    okb = 0
    for r in mc["records"]:
        if "citation" in r and r["id"] in before:
            okb += (before[r["id"]].get("threshold") or {}).get("citation") == r["citation"][0]
    print(f"  the citations file's 'before' citation equals the record's at 8b794e7 in {okb} of {sum(1 for r in mc['records'] if 'citation' in r)}")
    # the rules with a proposer: their own quoted texts, and their pages where fetched
    pages = fetched()
    cache = {}
    rows = []
    for r in book["rules"]:
        if not r.get("proposer"):
            continue
        txt = (r.get("quote") or "") + " " + (r.get("applies_to") or "") + " " + (r.get("rule") or "")
        words = {who: bool(re.search(PROPOSER_WORDS_IN_LAW[who], txt, re.I)) for who in r["proposer"]}
        in_quote = {who: bool(re.search(PROPOSER_WORDS_IN_LAW[who], r.get("quote") or "", re.I)) for who in r["proposer"]}
        path = pages.get(r.get("url"))
        found = None
        if path:
            if path not in cache:
                cache[path] = C30.readings(path)
            found = find_quote(r.get("quote") or "", cache[path]) or "NOT FOUND"
        rows.append((r["state"], r["citation"], r["type"], r["proposer"], words, in_quote, found))
    print(f"  {len(rows)} rules carry a proposer (states {sorted({x[0] for x in rows})}):")
    print("    state | citation | type | proposer | a word for each proposer in the rule's quote | ... in quote, applies_to or rule | quote on the page fetched")
    for st, cite, ty, pr, words, inq, found in rows:
        print(f"    {st} | {cite[:48]} | {ty} | {','.join(pr)} | {'yes' if all(inq.values()) else 'no: ' + ','.join(k for k, v in inq.items() if not v)} | "
              f"{'yes' if all(words.values()) else 'NO: ' + ','.join(k for k, v in words.items() if not v)} | {found or 'page not fetched'}")
    print(f"  every proposer named in the rule's own quote: {sum(1 for x in rows if all(x[5].values()))}; in its quote, applies_to or rule: "
          f"{sum(1 for x in rows if all(x[4].values()))}; quote found on the page: {sum(1 for x in rows if x[6] and x[6] != 'NOT FOUND')} of {sum(1 for x in rows if x[6])} fetched")
    for r in book["rules"]:
        if r.get("proposer") and not all(re.search(PROPOSER_WORDS_IN_LAW[w], (r.get("quote") or "") + " " + (r.get("applies_to") or "") + " " + (r.get("rule") or ""), re.I) for w in r["proposer"]):
            print(f"    {r['state']} {r['citation']} proposer {r['proposer']}: quote {r.get('quote')!r}; applies_to {r.get('applies_to')!r}")


# ---------------------------------------------------------------------------------------------- 31.5
def section_5(before, after):
    print("### 31.5 the 18 notes: a p at a threshold other than 1/2 carries no near-1/2 note; the back-test at its own threshold")
    recs = load_records(AFTER, record_files(AFTER))
    half = [c for c in recs.values() if "value" in (c.get("p") or {}) and (c.get("question") or {}).get("scope") == "statewide" and (c.get("threshold") or {}).get("t") not in (None, 0.5)]
    noted = [c for c in half if (c.get("p") or {}).get("note")]
    had = [c for c in half if c["id"] in before and (before[c["id"]].get("p") or {}).get("note")]
    print(f"  statewide p at a threshold other than 1/2 at cbc4469: {len(half)} (thresholds {dict(collections.Counter((c['threshold']['t']) for c in half))}); "
          f"with a note now {len(noted)}; with the near-1/2 note at 8b794e7 {len(had)}")
    at_half = [c for c in recs.values() if "value" in (c.get("p") or {}) and (c.get("question") or {}).get("scope") == "statewide" and (c.get("threshold") or {}).get("t") == 0.5]
    print(f"  statewide p at 1/2: {len(at_half)}, with the near-1/2 note {sum(1 for c in at_half if (c['p'].get('note') or '').startswith('this route'))}")
    # the back-test at their own thresholds, from my pool (2018-2024, the class with earlier years), c16's two tests
    pool = C15.measure_pool()
    by_key = collections.defaultdict(list)
    for y, k, s, rid in pool:
        by_key[k].append((y, s))
    rows = []
    for c in half:
        y, t = c["year"], c["threshold"]["t"]
        if not (C16.MEASURE_YEARS[0] <= y <= C16.MEASURE_YEARS[1]):
            continue
        tr = np.array([s for yy, s in by_key["statewide measure"] if yy < y])
        yes, no = C27_yes_no(c)
        rows.append({"id": c["id"], "t": t, "s": yes / (yes + no), "n": yes + no, "tr": tr})
    emp = lambda r, x: float(np.mean(np.abs(r["tr"] - r["t"]) <= x + 1e-12))  # noqa: E731
    e_s = sum(emp(r, C16.MEASURE_LINE) for r in rows)
    s_s = sum(int(abs(r["s"] - r["t"]) <= C16.MEASURE_LINE + 1e-12) for r in rows)
    ladder = {k: (sum(emp(r, k / (2.0 * r["n"])) for r in rows), sum(int(abs(r["s"] - r["t"]) * 2 * r["n"] <= k + 0.5) for r in rows)) for k in C16.KS}
    rec = (L.load_json(os.path.join(L.DATA, "measure", "backtest-measures.json")).get("lean_notes_statewide_own_threshold") or {}).get("statewide measure") or {}
    counts_s = e_s >= C16.MIN_COUNT or s_s >= C16.MIN_COUNT
    vk = next((k for k in C16.KS if ladder[k][0] >= C16.MIN_COUNT), None)
    print(f"  {len(rows)} such questions {C16.MEASURE_YEARS[0]}-{C16.MEASURE_YEARS[1]} (record: {rec.get('questions')}): (s) within 1 point of its own threshold "
          f"expected {e_s:.1f}, seen {s_s} (record {rec.get('share_test', {}).get('expected')}, {rec.get('share_test', {}).get('seen')}); counts: {counts_s} (record {rec.get('share_test', {}).get('counts')})")
    print("    (v) ladder expected/seen: " + "; ".join(f"{k:,} votes {e:.2f}/{s}" for k, (e, s) in ladder.items())
          + f"; first line with 5 expected: {vk if vk else 'none up to 50,000'} (record: {rec.get('vote_test', {}).get('why') or rec.get('vote_test')})")
    print(f"  note by the rule of 13:52: {'none, neither test counts' if not counts_s and vk is None else 'a test counts'} (record note: {rec.get('note')!r}, why_none {rec.get('why_none')!r})")


# ---------------------------------------------------------------------------------------------- 31.6
def section_6(before, after):
    print("### 31.6 MT LR-130's p and every statewide p that moved, recomputed from my own pool")
    moved = [cid for cid in set(before) & set(after) if "value" in (after[cid].get("p") or {}) and (before[cid].get("p") or {}).get("value") != after[cid]["p"]["value"]]
    new = [cid for cid in set(after) - set(before) if "value" in (after[cid].get("p") or {})]
    ratios = [after[cid]["p"]["value"] / before[cid]["p"]["value"] for cid in moved if (before[cid].get("p") or {}).get("value")]
    print(f"  p values moved {len(moved)} (ratios {min(ratios):.3f} to {max(ratios):.3f}), new p {len(new)}: {new}")
    pool = C15.measure_pool()
    by_key = collections.defaultdict(list)
    for y, k, s, _ in pool:
        by_key[k].append((y, s))
    rows = {r["id"]: r for r in D.rows("measure")}
    tal = collections.Counter()
    worst = 0.0
    dN = collections.Counter()
    for cid in sorted(moved + new):
        r = rows.get(cid)
        a = after[cid]
        if r is None or r["status"] != "value" or r["p"]["value"] != a["p"]["value"]:
            tal["HEAD's record is not cbc4469's"] += 1
            continue
        t = r["t"]
        sh = [s for y, s in by_key[r["cls"]] if y < r["year"]]
        f, N, h, k = D.density_at(sh, t)
        if f is None:
            tal["too few in my pool"] += 1
            continue
        yes, no = C27_yes_no(a)
        n = yes + no - 1
        p = r["p"]
        y_, n_ = (1 - t) * f / n, t * f / n
        same = (N == r["N"], k == r["kin"], abs(h - D.window_h(r["win"])) < 1e-9, abs(round(k / N, 5) - r["q"]) < 1e-9,
                rel(f, p["f_t"]) <= 1e-5, n == p.get("n"), rel(max(y_, n_), p["value"]) <= 1e-5)
        worst = max(worst, rel(max(y_, n_), p["value"]))
        tal["(N, k, h, q, f_t, n, value) all equal" if all(same) else "DIFFERS"] += 1
        if not all(same):
            print(f"    {cid}: mine N {N} k {k} h {h} f {f:.6g} n {n} value {max(y_, n_):.6g}; record N {r['N']} k {r['kin']} win {r['win']} f_t {p['f_t']} n {p.get('n')} value {p['value']}")
        if cid in moved:
            fb = (before[cid].get("forecasts") or [{}])[-1]
            dN[(r["year"], (r["N"] or 0) - (fb.get("like_measures") or 0))] += 1
    print(f"  {len(moved) + len(new)} p: {dict(tal)}; worst relative difference on the value {worst:.2e}")
    print(f"  like measures added to the pool by the joins, (year of the p, N after - N before): {dict(sorted(dN.items()))}")
    lr = rows.get("2020-measure-MT-LEGISLATIVE_REFERENDUM_NO_130")
    if lr:
        print(f"  LR-130: p {lr['p']['value']:.6g} at t {lr['t']}, N {lr['N']}, in window {lr['kin']}, window {lr['win']}, n {lr['p']['n']}; yes share {lr['yes_share']}")


def main():
    print(f"##### c31 statewide questions filed local, citations by proposer, notes (#82): HEAD {L.git_head()}")
    before, after, mj, mc = section_1()
    section_2(before, after, mj)
    section_3()
    section_4(before, after, mc)
    section_5(before, after)
    section_6(before, after)


if __name__ == "__main__":
    main()
