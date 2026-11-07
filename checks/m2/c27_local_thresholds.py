"""c27: D3's #77 (e41dca5): local questions' thresholds read from state law (step (b)); 800 local questions of
North Carolina and Louisiana take p by the threshold form, 55 rules (NC 39, LA 16).

The orchestrator (2026-11-07 13:39 UTC): "check a sample of the rules' quotes against their saved pages,
recompute a sample of the p, and check the out-of-sample counts in REPORT §17."

What this does (every figure [measured] unless marked):
  27.1 the rules file and the moves file: the 55 rules' counts; the moves file against my own diff of the measure
       files between de31d9b (before) and e41dca5 (after); no p moved or lost; p_after equals the file.
  27.2 every quote of the rules file (the rule's own, and those of also_cited and supporting) against the page at
       its URL as fetched by checks/m2/fetch_law_pages.sh into ~/.cache/vote-m2/law_local/ (D3's saved pages are
       in D3's cache, not in the repository); whitespace, quote marks, dashes and HTML entities normalised.
  27.3 every NC and LA local question in the files, counted whole (the State Board's and the Secretary of State's
       own counts): the rule matched by my own reading of the rules file (first rule in file order whose
       `match`, `match_also` and `dates` the title fits), the pool of like questions of earlier years, f at t,
       p = f / (2 n); against the records and the moves file's reasons.
  27.4 the out-of-sample counts (own window, within 1, 2 and 5 points) rebuilt from 27.3, against
       data/measure/backtest-measures.json (at_threshold_local) and data/local/backtest-ncsbe.json
       (questions_at_threshold) and REPORT §17's table.
  27.5 the 11:01 rule's two tests (c16's form) on the local classes: none of the 800 p carries a near-1/2 note;
       whether one would stand is a reading for the orchestrator.
Own implementation; nothing from pipeline/ is imported (pipeline/measures.py's local_rule_for and density_at
were read and their rules re-applied here).
"""
import collections
import glob
import html
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402
import c16_notes as C16  # noqa: E402

BEFORE, AFTER = "de31d9b", "e41dca5"
BOOK = os.path.join(L.DATA, "measure", "thresholds-local.json")
MOVES = os.path.join(L.DATA, "measure", "moves-local-thresholds.json")
PAGES = os.path.join(L.CACHE, "law_local")
WINDOWS, MIN_IN_WINDOW, MIN_CLASS = (0.01, 0.02, 0.05), 10, 100
MEDSL_GENERAL = {"2016-11-08", "2018-11-06", "2020-11-03", "2022-11-08", "2024-11-05"}   # MEDSL's general dates
YES_WORDS = {"YES", "FOR", "APPROVE", "APPROVED", "ACCEPT", "RETAIN", "BONDS YES", "YES ON", "FOR THE MEASURE",
             "IN FAVOR", "IN FAVOR OF", "YES FOR APPROVAL"}
NO_WORDS = {"NO", "AGAINST", "REJECT", "REJECTED", "NOT RETAIN", "DO NOT RETAIN", "BONDS NO", "NO ON",
            "AGAINST THE MEASURE", "OPPOSED", "NO FOR REJECTION"}
_POS = re.compile(r"^(YES|FOR|IN FAVOR)\b")
_NEG = re.compile(r"^(NO|AGAINST|OPPOSED)\b(?! (NAME|CANDIDATE))")


def side(name):
    n = (name or "").upper().strip()
    if n in YES_WORDS:
        return "yes"
    if n in NO_WORDS:
        return "no"
    if _POS.match(n):
        return "yes"
    if _NEG.match(n):
        return "no"
    return None


def rel(a, b):
    return abs(a - b) / max(abs(a), abs(b), 1e-300)


def at(commit, path):
    r = subprocess.run(["git", "show", f"{commit}:{path}"], capture_output=True, text=True, cwd=L.ROOT)
    return json.loads(r.stdout) if r.returncode == 0 and r.stdout else None


def changed_files():
    r = subprocess.run(["git", "diff", "--name-only", BEFORE, AFTER, "--", "data/measure", "data/local"],
                       capture_output=True, text=True, cwd=L.ROOT)
    return [x for x in r.stdout.split("\n") if x]


def density_at(s, t):
    """pipeline/measures.py density_at, re-applied: (f, N, h, k); None where the class is under MIN_CLASS."""
    N = len(s)
    if N < MIN_CLASS:
        return None, N, None, None
    for h in WINDOWS:
        k = sum(1 for x in s if abs(x - t) <= h)
        if k >= MIN_IN_WINDOW or h == WINDOWS[-1]:
            return k / N / (2.0 * h), N, h, k


def yes_no(c):
    cands = (c.get("result") or {}).get("candidates") or []
    yes = sum(x["votes"] for x in cands if side(x["name"]) == "yes")
    no = sum(x["votes"] for x in cands if side(x["name"]) == "no")
    return yes, no


def local_rows(st):
    """The state's local questions in data/measure, counted whole (its own file's counts), with my yes/no."""
    out = []
    for p in sorted(glob.glob(os.path.join(L.DATA, "measure", "*", f"{st}.json"))):
        d = L.load_json(p)
        for c in d["contests"]:
            q, res = c.get("question") or {}, c.get("result") or {}
            if res.get("source") not in ("ncsbe", "la_sos"):
                continue
            yes, no = yes_no(c)
            out.append(dict(c=c, year=c["year"], date=c.get("date"), scope=q.get("scope"), kind=q.get("kind"),
                            title=q.get("title") or "", yes=yes, no=no, st=st))
    return out


# ---------------------------------------------------------------------------------------------- 27.1
def section_1(book, moves):
    print("### 27.1 the rules file and the moves file")
    rules = book["rules"]
    by_st = collections.Counter(r["state"] for r in rules)
    print(f"  {len(rules)} rules: {dict(by_st)}; t: {dict(collections.Counter(str(r.get('t')) for r in rules))}; "
          f"hold {sum(1 for r in rules if r.get('hold'))}, advisory {sum(1 for r in rules if r.get('advisory'))}, "
          f"compound {sum(1 for r in rules if r.get('compound'))}; mark: "
          f"{dict(collections.Counter((r['state'], r.get('mark')) for r in rules))}")
    print(f"  scope: {dict(collections.Counter(r.get('scope') for r in rules))}; with dates "
          f"{sum(1 for r in rules if r.get('dates'))}, with match_also {sum(1 for r in rules if r.get('match_also'))}"
          f"; every rule has match: {all(r.get('match') for r in rules)}; every rule compiles: "
          f"{all(re.compile(r['match']) is not None for r in rules)}")
    bad_t = [r['kind'][:40] for r in rules if r.get('t') not in (0.5, None)]
    print(f"  thresholds other than 1/2: {bad_t or 'none'} (D3: every threshold read is 1/2)")
    print(f"  states block: {list((book.get('states') or {}).keys())} (not read): "
          f"{ {k: v.get('questions') for k, v in (book.get('states') or {}).items()} }")
    # the moves file against my own diff
    recs = moves["records"]
    print(f"  moves file: {len(recs)} records; counts {moves['counts']}")
    mine = {}   # id -> (p_before, p_after, reason_before, reason_after)
    for path in changed_files():
        if not re.search(r"data/measure/\d{4}/[A-Z]{2}\.json$", path):
            continue
        b, a = at(BEFORE, path), at(AFTER, path)
        bb = {c["id"]: c for c in (b or {}).get("contests", [])}
        aa = {c["id"]: c for c in (a or {}).get("contests", [])}
        for i in set(bb) | set(aa):
            pb, pa = (bb.get(i) or {}).get("p") or {}, (aa.get(i) or {}).get("p") or {}
            if pb != pa:
                mine[i] = (pb.get("value"), pa.get("value"), pb.get("not_computed"), pa.get("not_computed"))
    ids = {r[0] for r in recs}
    print(f"  my diff {BEFORE}..{AFTER}: {len(mine)} records whose p block changed; in the moves file "
          f"{len(set(mine) & ids)}, not in it {len(set(mine) - ids)}; moves rows not in my diff {len(ids - set(mine))}")
    for i in sorted(set(mine) - ids)[:5]:
        print(f"    not in the moves file: {i} {mine[i]}")
    kinds = collections.Counter()
    for i, (vb, va, rb, ra) in mine.items():
        kinds[("p appeared" if vb is None and va is not None else "p gone" if vb is not None and va is None else
               "p moved" if vb is not None and va is not None else "reason changed")] += 1
    print(f"  what changed: {dict(kinds)} (D3: no p moves, no p lost)")
    # p_after equals the file's p; N rows' p_before None
    n_rows = [r for r in recs if r[3] == "N"]
    r_rows = [r for r in recs if r[3] == "R"]
    ok = sum(1 for r in n_rows if r[1] is None and r[2] is not None and r[0] in mine
             and mine[r[0]][1] is not None and rel(r[2], mine[r[0]][1]) <= 1e-9)
    print(f"  N rows {len(n_rows)}: p_before None and p_after equals the file's p in {ok}; "
          f"R rows {len(r_rows)}: reason changed and p still None in "
          f"{sum(1 for r in r_rows if r[0] in mine and mine[r[0]][1] is None and mine[r[0]][0] is None)}")
    print(f"  N by state: {dict(collections.Counter(r[0].split('-')[2] for r in n_rows))}; "
          f"R by state: {dict(collections.Counter(r[0].split('-')[2] for r in r_rows))}")
    return mine


# ---------------------------------------------------------------------------------------------- 27.2
def norm(s):
    s = html.unescape(s or "")
    s = (s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
         .replace("–", "-").replace("—", "-").replace(" ", " ").replace("‑", "-"))
    return " ".join(s.split())


def page_text(path):
    raw = open(path, "rb").read()
    try:
        s = raw.decode("utf-8")
    except UnicodeDecodeError:
        s = raw.decode("cp1252", errors="replace")
    s = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", s)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    return norm(s)


def citations(book):
    out = []
    for i, r in enumerate(book["rules"]):
        out.append((i, "rule", r["url"], r.get("quote"), r["citation"]))
        for k in ("also_cited", "supporting"):
            for a in r.get(k) or []:
                out.append((i, k, a["url"], a.get("quote"), a.get("citation")))
    return out


def url_index():
    """url -> (file, http code) from fetch_law_pages.sh's index files."""
    idx = {}
    for p in glob.glob(os.path.join(PAGES, "index_*.txt")):
        for line in open(p):
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 4:
                idx[parts[3]] = (os.path.join(PAGES, f"{parts[0]}.html"), parts[1])
    return idx


def section_2(book):
    print("### 27.2 the quotes against their pages (fetched by me with curl -sSL, one request per 5 s per host)")
    cites = citations(book)
    idx = url_index()
    urls = collections.OrderedDict((u, None) for _, _, u, _, _ in cites)
    print(f"  {len(cites)} citations ({dict(collections.Counter(k for _, k, _, _, _ in cites))}) on {len(urls)} "
          f"distinct URLs ({dict(collections.Counter(u.split('/')[2] for u in urls))}); fetched {len(set(urls) & set(idx))}"
          f", http codes {dict(collections.Counter(idx[u][1] for u in urls if u in idx))}")
    if not idx:
        print("  no pages fetched (run checks/m2/fetch_law_pages.sh first): nothing compared")
        return
    texts = {}
    tal = collections.Counter()
    misses = []
    for i, kind, u, q, cit in cites:
        if u not in idx or idx[u][1] != "200" or not os.path.exists(idx[u][0]):
            tal["page not fetched"] += 1
            continue
        if u not in texts:
            texts[u] = page_text(idx[u][0])
        t = texts[u]
        nq = norm(q)
        if not nq:
            tal["no quote"] += 1
        elif nq in t:
            tal["found, word for word"] += 1
        elif nq.lower() in t.lower():
            tal["found, case aside"] += 1
        else:
            # how much of it is there: the longest prefix found
            lo, hi = 0, len(nq)
            while lo < hi:
                mid = (lo + hi + 1) // 2
                if nq[:mid] in t:
                    lo = mid
                else:
                    hi = mid - 1
            tal["not found"] += 1
            misses.append((i, kind, cit, len(nq), lo, nq[max(0, lo - 30):lo + 40]))
    print(f"  {dict(tal)}")
    for i, kind, cit, n, lo, ctx in misses:
        print(f"    rule {i} ({kind}) {cit[:60]}: quote {n} chars, longest prefix found {lo}; around the break: "
              f"...{ctx}...")
    # pages that are shells (no law text): size and whether the citation's section number appears
    small = [(u, len(texts[u])) for u in texts if len(texts[u]) < 500]
    print(f"  pages under 500 characters of text: {len(small)}")
    for u, n in small:
        who = [(i, k, (cit or '')[:40], norm(q)[:60]) for i, k, uu, q, cit in cites if uu == u]
        print(f"    {u} ({n} chars): {texts[u][:160]!r}; cited by {who}")


# ---------------------------------------------------------------------------------------------- 27.3
def in_year(r, year):
    return (r.get("from_year") or 0) <= year <= (r.get("to_year") or 9999)


def rule_for(book, st, words, date, year):
    """pipeline/measures.py local_rule_for, re-applied: (rule index, reason)."""
    mine = [(i, r) for i, r in enumerate(book["rules"]) if r["state"] == st and r.get("scope") == "local"
            and in_year(r, year)]
    if not mine:
        return None, "the thresholds of this state's local questions are not read"
    for i, r in mine:
        if (re.search(r["match"], words) and (not r.get("match_also") or re.search(r["match_also"], words))
                and (not r.get("dates") or (date or "") in r["dates"])):
            break
    else:
        return None, "the source's words do not show which kind of local question this is"
    if r.get("hold"):
        return i, f"{r['kind']}: {r['hold']}"
    if r.get("advisory"):
        return i, "an advisory question: the law read sets no threshold for it"
    if r.get("compound") or r.get("t") is None:
        return i, f"{r['citation']}: compound"
    return i, None


def section_3(book, moves):
    print("### 27.3 the rule matched and p recomputed for every NC and LA local question counted whole")
    reasons = moves["reasons"]
    by_id = {r[0]: r for r in moves["records"]}
    out = []   # rows for 27.4
    for st in ("NC", "LA"):
        rows = local_rows(st)
        loc = [r for r in rows if r["scope"] == "local"]
        # the pool: the state's local questions counted whole, with a yes and a no side, by year (kind measure)
        pool = collections.defaultdict(list)
        for r in loc:
            if r["yes"] + r["no"] > 0 and r["kind"] == "measure" and not r["c"].get("one_answer_only"):
                pool[r["year"]].append(r["yes"] / (r["yes"] + r["no"]))
        print(f"  {st}: {len(rows)} questions in its own files' counts, {len(loc)} local; the pool by year "
              f"{ {y: len(v) for y, v in sorted(pool.items())} }")
        tal = collections.Counter()
        diffs = []
        n_p = 0
        for r in loc:
            c = r["c"]
            words = " ".join((r["title"] + " " + ((c.get("question") or {}).get("subject") or "")).upper().split())
            ri, why = rule_for(book, st, words, r["date"], r["year"])
            rec_p = c.get("p") or {}
            th = c.get("threshold") or {}
            mv = by_id.get(c["id"])
            if why is not None or ri is None:
                # the record should have no p and a reason that begins the same way
                rec_why = rec_p.get("not_computed") or ""
                if "value" in rec_p:
                    tal["mine: no p; record: p"] += 1
                    diffs.append((c["id"], "mine no p: " + why, "record p"))
                elif rec_why[:40] == why[:40] or (why.startswith("the source's words") and
                                                  rec_why.startswith("the source's words")):
                    tal["no p, same reason"] += 1
                else:
                    tal["no p, other reason"] += 1
                    diffs.append((c["id"], why[:70], rec_why[:70]))
                continue
            rule = book["rules"][ri]
            t = rule["t"]
            train = [s for y, ss in pool.items() if y < r["year"] for s in ss]
            f, N, h, k = density_at(train, t)
            if r["yes"] + r["no"] <= 0:
                tal["no yes/no votes"] += 1
                continue
            n = r["yes"] + r["no"] - 1
            if f is None:
                rec_why = rec_p.get("not_computed") or ""
                if rec_why.startswith(f"fewer than {MIN_CLASS} like measures") and f"({N})" in rec_why:
                    tal[f"fewer than {MIN_CLASS}: same, same N"] += 1
                else:
                    tal[f"fewer than {MIN_CLASS}: differs"] += 1
                    diffs.append((c["id"], f"mine: fewer than 100 ({N})", rec_why[:70] or "record p"))
                continue
            p = f / (2 * n) if t == 0.5 else max((1 - t) * f / n, t * f / n)
            fc = (c.get("forecasts") or [{}])[-1]
            same_rule = th.get("citation") == rule["citation"]
            same_fit = (fc.get("like_measures") == N and fc.get("in_window") == k
                        and fc.get("window") == [round(t - h, 4), round(t + h, 4)])
            same_p = "value" in rec_p and rel(rec_p["value"], p) <= 1e-5 and rel(rec_p["f_t"], f) <= 1e-5 \
                and rec_p["n"] == n
            same_mv = mv is not None and mv[3] == "N" and rel(mv[2], p) <= 1e-5
            if same_rule and same_fit and same_p and same_mv:
                tal["p equal (rule, N, k, h, f_t, n, p; moves row)"] += 1
                n_p += 1
            else:
                tal["p differs"] += 1
                diffs.append((c["id"], f"mine rule {ri} N {N} k {k} h {h} f {f:.5g} n {n} p {p:.4g}",
                              f"record {th.get('citation', '')[:30]} N {fc.get('like_measures')} k {fc.get('in_window')}"
                              f" win {fc.get('window')} f_t {rec_p.get('f_t')} n {rec_p.get('n')} p {rec_p.get('value')}"
                              f" moves {mv[3] if mv else None} {mv[2] if mv else None}"))
            out.append(dict(st=st, year=r["year"], date=r["date"], key=f"local measure, {st}", t=t,
                            s=r["yes"] / (r["yes"] + r["no"]), q_own=f * 2 * h, in_own=abs(r["yes"] / (r["yes"] + r["no"]) - t) <= h,
                            near={hh: (sum(1 for x in train if abs(x - t) <= hh) / len(train),
                                       abs(r["yes"] / (r["yes"] + r["no"]) - t) <= hh) for hh in WINDOWS},
                            general=r["date"] in MEDSL_GENERAL, equal=same_rule and same_fit and same_p and same_mv,
                            tr=train, n=r["yes"] + r["no"], margin=abs(r["yes"] - r["no"]),
                            note=(rec_p.get("note") or "")))
        print(f"    {st}: {dict(tal)}")
        for d in diffs[:12]:
            print(f"      {d[0][:70]} | {d[1]} | {d[2]}")
        if len(diffs) > 12:
            print(f"      ... {len(diffs) - 12} more")
        # the p's range as D3 states it
        ps = [(c.get("p") or {}).get("value") for r in loc for c in [r["c"]] if "value" in (c.get("p") or {})]
        ps.sort()
        if ps:
            print(f"    {st}: {len(ps)} p in the files: {ps[0]:.2g} to {ps[-1]:.2g}, median {ps[len(ps) // 2]:.2g} "
                  f"(D3: NC 496, 1.2e-6 to 0.041, median 1.9e-4; LA 304, 3.2e-6 to 0.084, median 7.6e-4)")
        # which rules the p'd questions took, against the rules' n_questions
        took = collections.Counter()
        for r in loc:
            words = " ".join(r["title"].upper().split())
            ri, why = rule_for(book, st, words, r["date"], r["year"])
            if ri is not None:
                took[ri] += 1
        off = [(i, took.get(i, 0), book["rules"][i].get("n_questions")) for i in range(len(book["rules"]))
               if book["rules"][i]["state"] == st and took.get(i, 0) != book["rules"][i].get("n_questions")]
        print(f"    {st}: questions per rule (the rule taken, any p state) equal the rules' n_questions for "
              f"{sum(1 for i in range(len(book['rules'])) if book['rules'][i]['state'] == st) - len(off)} rules; "
              f"differing (rule, mine, file): {off[:10] or 'none'}")
        # where two rules share a pattern (17/18 bonds, 33/34 school tax), n_questions counts the pattern's matches
        pats = collections.defaultdict(list)
        for i, r in enumerate(book["rules"]):
            if r["state"] == st:
                pats[(r["match"], r.get("dates") and tuple(r["dates"]))].append(i)
        for key, ii in pats.items():
            if len(ii) > 1:
                print(f"      rules {ii} share the pattern {key[0][:30]!r}: taken {[took.get(i, 0) for i in ii]}, "
                      f"sum {sum(took.get(i, 0) for i in ii)}, file's n_questions {[book['rules'][i].get('n_questions') for i in ii]}")
        # my reasons for the questions without p, against D3's REPORT §17 breakdown
        whys = collections.Counter()
        for r in loc:
            words = " ".join(r["title"].upper().split())
            ri, why = rule_for(book, st, words, r["date"], r["year"])
            if why is None and ri is not None:
                train = [s for y, ss in pool.items() if y < r["year"] for s in ss]
                if len(train) < MIN_CLASS:
                    why = f"fewer than {MIN_CLASS} like questions in earlier years"
            if why:
                whys[why[:60]] += 1
        print(f"    {st}: my reasons for no p ({sum(whys.values())} questions):")
        for w, n in whys.most_common():
            print(f"      {n:4d} {w}")
    # the moves file's reasons for R rows, against mine, by state
    print(f"  moves file R reasons (28 listed): {len(reasons)}; rules cited by N rows: {len(moves['rules_cited'])}")
    return out


# ---------------------------------------------------------------------------------------------- 27.4
def summarise(rows):
    out = {"measures": len(rows), "own": [round(sum(r["q_own"] for r in rows), 1), sum(r["in_own"] for r in rows)]}
    for hh in WINDOWS:
        out[f"{hh:.0%}"] = [round(sum(r["near"][hh][0] for r in rows), 1), sum(r["near"][hh][1] for r in rows)]
    return out


def section_4(rows):
    print("### 27.4 the out-of-sample counts, rebuilt, against the two back-test files and REPORT §17")
    bt = L.load_json(os.path.join(L.DATA, "measure", "backtest-measures.json")).get("at_threshold_local") or {}
    bn = (L.load_json(os.path.join(L.DATA, "local", "backtest-ncsbe.json")).get("questions_at_threshold") or {}).get("years") or {}

    def rec_fmt(v):
        if not v:
            return None
        return {"measures": v.get("measures"), "own": [v["own_window"]["expected"], v["own_window"]["seen"]],
                **{k.replace("within ", ""): [x["expected"], x["seen"]] for k, x in v.get("near_threshold", {}).items()}}
    groups = {
        "LA 2024 (general dates file: all years local measure, LA)": ([r for r in rows if r["st"] == "LA"],
                                                                      rec_fmt(bt.get("all years local measure, LA"))),
        "NC general dates (all years local measure, NC)": ([r for r in rows if r["st"] == "NC" and r["general"]],
                                                           rec_fmt(bt.get("all years local measure, NC"))),
        "NC other dates (backtest-ncsbe questions_at_threshold, all years)":
            ([r for r in rows if r["st"] == "NC" and not r["general"]],
             rec_fmt(bn.get("all years"))),
    }
    for name, (rs, rec) in groups.items():
        mine = summarise(rs)
        print(f"  {name}:\n    mine   {mine}\n    record {rec}")
    # by year, both files
    print("  by year (mine | file), general dates (at_threshold_local) and NC other dates (questions_at_threshold):")
    for y in sorted({r["year"] for r in rows}):
        g = [r for r in rows if r["year"] == y and (r["general"] or r["st"] == "LA")]
        o = [r for r in rows if r["year"] == y and r["st"] == "NC" and not r["general"]]
        if g:
            print(f"    {y} general: {summarise(g)} | {rec_fmt(bt.get(str(y)))}")
        if o:
            print(f"    {y} other:   {summarise(o)} | {rec_fmt(bn.get(str(y)))}")
    print("  REPORT §17's table: LA 2024 304: 14.2/14, 7.1/8, 14.2/14, 39.7/41; NC general 190: 6.5/5, 6.5/5, "
          "15.6/11, 38.9/30; NC other 306: 19.6/23, 10.9/15, 28.8/31, 65.6/82")
    # the sums' meaning: within 1% expected = sum over questions of the share of the class within 1 point
    for name, rs in (("LA 2024", [r for r in rows if r["st"] == "LA"]),
                     ("NC general dates", [r for r in rows if r["st"] == "NC" and r["general"]]),
                     ("NC other dates", [r for r in rows if r["st"] == "NC" and not r["general"]])):
        hs = collections.Counter(next((f"{hh:.0%}" for hh in WINDOWS if abs(r["q_own"] - r["near"][hh][0]) < 1e-12),
                                      "?") for r in rs)
        print(f"  the window each question's class took ({name}): {dict(hs)} (own window = within that width: "
              f"q = f·2h, h the first of 1, 2, 5 points holding 10 like questions)")


# ---------------------------------------------------------------------------------------------- 27.5
def section_5(rows):
    print("### 27.5 the lean note's two tests on the local pools, under the rule of 11:01 as amended at 13:52 (#79)")
    print("  (s) the class's share within 1 point of the threshold, summed, against the questions that finished there; "
          "(v) the same within k votes (k/(2n) of the threshold, n = yes + no), k the smallest of 10/100/1,000/5,000/"
          "10,000/20,000/50,000 with 5 or more expected, not counting where its line holds more than half the pool; "
          "a test counts with 5 or more seen or expected; the note stands where both count and lean the same way, or "
          "on the one that counts (c16's two_tests). Each pool is one build's own back-test (the ruling's item 2).")
    bt = L.load_json(os.path.join(L.DATA, "measure", "backtest-measures.json")).get("lean_notes_local") or {}
    bn = (L.load_json(os.path.join(L.DATA, "local", "backtest-ncsbe.json")).get("questions_at_threshold") or {}).get("lean_note")
    recs = {"LA 2024": bt.get("local measure, LA"), "NC general dates": bt.get("local measure, NC"), "NC other dates": bn}

    def emp(r, x):
        return sum(1 for v in r["tr"] if abs(v - 0.5) <= x) / len(r["tr"])
    groups = (("LA 2024", [r for r in rows if r["st"] == "LA"]),
              ("NC general dates", [r for r in rows if r["st"] == "NC" and r["general"]]),
              ("NC other dates", [r for r in rows if r["st"] == "NC" and not r["general"]]),
              ("NC, all 496", [r for r in rows if r["st"] == "NC"]),
              ("all 800", rows))
    for name, rs in groups:
        print(f"  {name} ({len(rs)} questions):")
        ps_s = [emp(r, 0.01) for r in rs]
        seen_s = [int(abs(r["s"] - 0.5) <= 0.01 + 1e-12) for r in rs]
        years = collections.defaultdict(lambda: [0.0, 0])
        for r, p_, s_ in zip(rs, ps_s, seen_s):
            years[r["year"]][0] += p_
            years[r["year"]][1] += s_
        ladder = {k: ([emp(r, k / (2.0 * r["n"])) for r in rs], [int(r["margin"] <= k) for r in rs]) for k in C16.KS}
        C16.two_tests(name, ps_s, seen_s, 0.01, ladder, {y: tuple(v) for y, v in years.items()})
        # D3 reads 'within k votes' as |s - t| <= k / (2(yes + no)) in floating point; a margin of exactly k can fall
        # outside it by rounding
        for k in (10, 100):
            fl = sum(1 for r in rs if abs(r["s"] - 0.5) <= k / (2.0 * r["n"]))
            ex = sum(1 for r in rs if r["margin"] == k)
            print(f"    within {k} votes: margin <= {k} in {sum(1 for r in rs if r['margin'] <= k)}; D3's share form in floats {fl}; margin exactly {k} in {ex}")
        rec = recs.get(name)
        if rec:
            st_, vt = rec.get("share_test") or {}, rec.get("vote_test") or {}
            print(f"    the record: (s) {st_.get('seen')} against {st_.get('expected')} ({st_.get('line')}, counts {st_.get('counts')}), "
                  f"(v) {vt.get('seen')} against {vt.get('expected')} ({vt.get('line') or vt.get('why')}, counts {vt.get('counts')}); "
                  f"note {'stands on ' + str(rec.get('stands_on')) if rec.get('note') else 'none: ' + str(rec.get('why_none'))}")
        # the counts of the p themselves: how many of this pool's p carry the note
        noted = collections.Counter()
        for r in rs:
            noted["note" if r.get("note") else "no note"] += 1
        print(f"    p blocks of this pool by note: {dict(noted)}")


def main():
    print(f"c27: #77 local thresholds; HEAD {L.git_head()}; before {BEFORE}, after {AFTER}")
    book = L.load_json(BOOK)
    moves = L.load_json(MOVES)
    section_1(book, moves)
    section_2(book)
    rows = section_3(book, moves)
    section_4(rows)
    section_5(rows)


if __name__ == "__main__":
    main()
