"""c30: D3's #81 (step (a): each held statewide question's own ballot text; 67 statewide measures get p), checked
against the files, my own reading of the rules and my own pools. HEAD dc727b1; before 2827d85, after 8b794e7.

What this does (every figure [measured] unless marked):
  30.1 the moves file (data/measure/moves-ballot-texts.json, 116 rows) against my own diff of every measure file
       between 2827d85 and 8b794e7: the rows are exactly the records whose threshold or p changed (N: p appeared;
       T: threshold read, p still not computed; H: still held), t and p before and after as the commits hold them,
       and that no record changed otherwise (ballot_text added apart).
  30.2 each of the 116 questions' rule by my own reading of pipeline/measures.py's rule_for (written again here, not
       imported): the type from the title (the pipeline's patterns) or the ballot text's where it has one, the special
       rule's case from fact.applies, the rule picked among the state's rules in thresholds.json; against the record's
       threshold (t, citation, matched) and, where held, its reason.
  30.3 the four rules read in step (a) (Georgia's referendums, Rhode Island's bond acts) and a sample of the ballot
       texts' quotes (type_quote and fact.quote, two questions per state) against the pages fetched by me
       (sh checks/m2/fetch_ballot_texts.sh: curl -sSL, 5 s apart, into ~/.cache/vote-m2/ballot_texts/), word for word
       with whitespace, quotes, dashes and entities normalised; PDFs through pdftotext in both readings.
  30.4 every one of the 67 new p recomputed from my own pool of like measures (c15's measure_pool, m2d3's density_at):
       N, k, h, q, f_t, yes, no and the value; the statewide note on them; the T rows' counts of like measures
       (none before 2016, 83 before 2018) from my pool; the back-test's at-threshold counts for 2022-2024 rebuilt
       (c15 15.3 prints the full table).
Nothing in pipeline/ or model/ is imported; rules re-applied here are copied from the pipeline and say so.
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
import c28_governor_codes as C28  # noqa: E402

BEFORE = "2827d85"
AFTER = "8b794e7"
MOVES = os.path.join(L.DATA, "measure", "moves-ballot-texts.json")
TEXTS = os.path.join(L.DATA, "measure", "ballot-texts.json")
THRESH = os.path.join(L.DATA, "measure", "thresholds.json")
PAGES = os.path.join(L.CACHE, "ballot_texts")

# pipeline/measures.py's _TYPES, copied (the type a title states), and rule_for's decision, written again below
TYPES = [
    ("convention", r"\bCONVENTION\b"),
    ("bond", r"\bBONDS?\b|GENERAL OBLIGATION"),
    ("amendment", r"CONSTITUTION|\bAMEND|\bCON\.? AMEND|^CA NO\b|\bCI-\d|\bHJR\b|\bSJR\b|JOINT RESOLUTION"),
    ("statute", r"\(STATUTORY\)|REFERRED LAW|REFERRED ACT|\bAN ACT\b|LEGISLATIVE INITIATIVE|INITIATED MEASURE|"
                r"INITIATIVE MEASURE|INITIATIVE NO\b|^INITIATIVE \d|\bI-\d|REFERENDUM MEASURE"),
    ("advisory", r"\bADVISORY\b"),
]


def rel(a, b):
    return abs(a - b) / max(abs(a), abs(b), 1e-300)


def at(commit, path):
    r = subprocess.run(["git", "show", f"{commit}:{path}"], capture_output=True, text=True, cwd=L.ROOT)
    return json.loads(r.stdout) if r.returncode == 0 and r.stdout else None


def changed_files():
    r = subprocess.run(["git", "diff", "--name-only", BEFORE, AFTER, "--", "data/measure/"], capture_output=True, text=True, cwd=L.ROOT)
    return [x for x in r.stdout.split("\n") if x.endswith(".json") and re.search(r"data/measure/\d{4}/[A-Z]{2}\.json$", x)]


def pval(c):
    return (c.get("p") or {}).get("value")


def reason(c):
    return (c.get("p") or {}).get("not_computed")


def tval(c):
    return (c.get("threshold") or {}).get("t")


def title_type(title, subject=None):
    t = (title or "").upper() + " " + (subject or "").upper()
    for name, pat in TYPES:
        if re.search(pat, t):
            return name
    return None


# ---------------------------------------------------------------------------------------------- 30.1
def section_1(moves):
    print("### 30.1 the moves file against my diff of the measure files")
    rows = moves["contests"]
    cols = moves["columns"]
    print(f"  moves file: {len(rows)} rows, columns {cols}; counts {json.dumps(moves['counts'])[:300]}; before {moves['before_commit']}")
    by_id = {r[0]: dict(zip(cols, r)) for r in rows}
    code = collections.Counter(r["code"] for r in by_id.values())
    print(f"  rows by code: {dict(code)}")
    files = changed_files()
    mine = {}
    other = collections.Counter()
    texts_added = 0
    for path in files:
        b, a = at(BEFORE, path), at(AFTER, path)
        if b is None or a is None:
            print(f"  {path}: added or removed (not expected)")
            continue
        bi = {c["id"]: c for c in b["contests"]}
        ai = {c["id"]: c for c in a["contests"]}
        for cid in sorted(set(bi) | set(ai)):
            cb, ca = bi.get(cid), ai.get(cid)
            if cb is None or ca is None:
                other["record added or removed"] += 1
                continue
            if ca.get("ballot_text") and not cb.get("ballot_text"):
                texts_added += 1
            changed = (tval(cb) != tval(ca)) or (pval(cb) != pval(ca)) or (reason(cb) != reason(ca))
            if changed:
                mine[cid] = (tval(cb), tval(ca), pval(cb), pval(ca), reason(ca), (ca.get("threshold") or {}).get("citation"))
            # anything else changed?
            kb = {k: v for k, v in cb.items() if k not in ("threshold", "p", "ballot_text")}
            ka = {k: v for k, v in ca.items() if k not in ("threshold", "p", "ballot_text")}
            for k in sorted(set(kb) | set(ka)):
                if kb.get(k) != ka.get(k):
                    other[f"{k} {'added' if k not in kb else 'removed' if k not in ka else 'changed'}"] += 1
            if not changed and (ca.get("threshold") != cb.get("threshold") or ca.get("p") != cb.get("p")):
                other["threshold or p block changed without t, p or reason moving"] += 1
    print(f"  files changed under data/measure/<year>/: {len(files)}; my diff: {len(mine)} records whose threshold, p or reason changed; "
          f"ballot_text added on {texts_added}; other fields {dict(other) or 'none'} (forecasts: the class and window of a threshold now read)")
    print(f"  in both {len(set(mine) & set(by_id))}; in my diff only {sorted(set(mine) - set(by_id))[:5] or 'none'}; in the moves file only {sorted(set(by_id) - set(mine))[:5] or 'none'}")
    tal = collections.Counter()
    mycode = collections.Counter()
    for cid, (tb, ta, pb, pa, why, cit) in mine.items():
        c = "N" if pa is not None and pb is None else "T" if ta is not None and tb is None and pa is None else "H" if ta is None else "?"
        mycode[c] += 1
        r = by_id.get(cid)
        if not r:
            continue
        ok = (r["t_before"] == tb, r["t_after"] == ta, (r["p_before"] is None and pb is None) or (r["p_before"] is not None and pb is not None and rel(r["p_before"], pb) < 1e-9),
              (r["p_after"] is None and pa is None) or (r["p_after"] is not None and pa is not None and rel(r["p_after"], pa) < 1e-9),
              r["code"] == c, (r.get("citation") or None) == cit, (r.get("not_computed") or None) == why)
        tal["equal (t, p before and after, code, citation, reason)" if all(ok) else f"differs {ok}"] += 1
    print(f"  my codes {dict(mycode)}; row by row: {dict(tal)}")
    return by_id, mine


# ---------------------------------------------------------------------------------------------- 30.2
def my_rule(st, year, ty_title, text, book):
    """rule_for's decision, written again (pipeline/measures.py as #81 left it): (rule, how) or (None, why)."""
    states = book.get("states", {})
    mine = [r for r in book["rules"] if r["state"] == st and (r.get("from_year") or 0) <= year <= (r.get("to_year") or 9999) and r.get("scope") != "local"]
    ty = ty_title
    tty = (text or {}).get("type")
    how_t = None
    if tty and tty != ty:
        how_t = f"text:{tty}" + (f",not title:{ty}" if ty else "")
        ty = tty
    if ty == "advisory":
        return None, "advisory"
    pool = [r for r in mine if r["type"] != "retention"]
    if ty:
        pool = [r for r in pool if r["type"] == ty]
        if not pool:
            return None, f"the threshold of this state's {ty}s is not read"
        how = how_t or f"title:{ty}"
    else:
        if not (states.get(st) or {}).get("complete"):
            return None, "untyped, rules incomplete"
        pool = [r for r in pool if r["type"] != "convention"]
        how = "untyped, every rule the same"
    general = [r for r in pool if not r.get("only_if")]
    special = [r for r in pool if r.get("only_if")]
    form = lambda r: (r.get("t"), r.get("compound"))
    fact = (text or {}).get("fact") or {}
    if special and fact.get("applies") is not None:
        pick = special if fact["applies"] else general
        if pick and len({form(r) for r in pick}) == 1 and len({r["only_if"] for r in special}) == 1:
            r = pick[0]
            if r.get("compound") or r.get("t") is None:
                return None, "compound"
            return r, how + ("; special applies" if fact["applies"] else "; special does not apply") + f" [{fact.get('mark')}]"
    if not general:
        return None, "general not read" + ("; text does not show" if text and special and fact.get("applies") is None else "")
    if all(r.get("compound") or r.get("t") is None for r in general):
        return None, "compound"
    if len({form(r) for r in general}) > 1:
        return None, "several general forms"
    other = [r for r in special if form(r) != form(general[0])]
    if other:
        return None, "another threshold, not shown" + ("; text does not show" if text else "")
    return general[0], how


def section_2(by_id):
    print("### 30.2 each question's rule by my own reading of the ballot text and the state's rules")
    book = L.load_json(THRESH)
    texts = L.load_json(TEXTS)["questions"]
    rec = {}
    for path in changed_files():
        a = at(AFTER, path)
        for c in a["contests"]:
            if c["id"] in by_id:
                rec[c["id"]] = c
    tal = collections.Counter()
    bad = []
    type_src = collections.Counter()
    marks = collections.Counter()
    for cid, row in sorted(by_id.items()):
        c = rec[cid]
        text = texts.get(cid)
        if text is None:
            tal["no ballot text for the row"] += 1
            bad.append((cid, "no ballot text"))
            continue
        tt = title_type((c.get("question") or {}).get("title"), (c.get("question") or {}).get("subject"))
        r, how = my_rule(c["place"]["state"], c["year"], tt, text, book)
        th = c.get("threshold") or {}
        if r is not None:
            type_src[how.split(";")[0].split(":")[0]] += 1
            marks[(text.get("type_mark"), (text.get("fact") or {}).get("mark") if "special" in how else None)] += 1
            ok = (th.get("t") == r["t"], th.get("citation") == r["citation"], row["t_after"] == r["t"], row["code"] in ("N", "T"))
            # the record's matched line names the same reading
            m = th.get("matched") or ""
            if how.startswith("text:"):
                ok += ("ballot text" in m and f"({r['type']}" in m,)
            if "special applies" in how:
                ok += ("shows it is " in m and "shows it is not" not in m,)
            elif "special does not apply" in how:
                ok += ("shows it is not" in m,)
            tal["rule as the record's" if all(ok) else "DIFFERS"] += 1
            if not all(ok):
                bad.append((cid, f"mine t {r['t']} {r['citation']} ({how}); record t {th.get('t')} {th.get('citation')} matched {m[:120]!r}; row {row['code']} {row['t_after']}"))
        else:
            why = reason(c) or ""
            ok = (th.get("t") is None, row["code"] == "H",
                  ("does not show it either" in why) if "text does not show" in how else ("turns on more than" in why) if how == "compound" else True)
            tal["held as the record's" if all(ok) else "DIFFERS (held)"] += 1
            if not all(ok):
                bad.append((cid, f"mine held ({how}); record t {th.get('t')} code {row['code']} reason {why[:140]!r}"))
    print(f"  {len(by_id)} questions: {dict(tal)}; the type from {dict(type_src)} (text = the ballot text's type, title = the pipeline's title patterns); "
          f"marks (type, special case) {dict((str(k), v) for k, v in marks.items())}")
    for cid, s in bad[:12]:
        print(f"    {cid}: {s}")
    # the three calls of 14:21 and the four held
    held = [cid for cid, row in by_id.items() if row["code"] == "H"]
    print(f"  held (H): {held}")
    for cid in ("2024-measure-OR-MEASURE_115", "2024-measure-OR-115"):
        if cid in rec:
            print(f"  Oregon 115: t {tval(rec[cid])}, {(rec[cid].get('threshold') or {}).get('citation')}, matched {(rec[cid].get('threshold') or {}).get('matched', '')[:160]!r}")
    for cid, row in sorted(by_id.items()):
        if cid.startswith("2024-measure-OR") and "115" in cid:
            print(f"  Oregon 115 ({cid}): t {row['t_after']}, {row.get('citation')}, code {row['code']}")
    ga = [(cid, row["code"], row["t_after"], row.get("citation")) for cid, row in sorted(by_id.items()) if "-GA-" in cid]
    ri = [(cid[:40], row["code"], row["t_after"], row.get("citation")) for cid, row in sorted(by_id.items()) if "-RI-" in cid]
    print(f"  Georgia: {ga}")
    print(f"  Rhode Island: {ri}")


# ---------------------------------------------------------------------------------------------- 30.3
def readings(path):
    """[(label, normalised text)] of a fetched page: a PDF (by its first bytes, whatever the URL's ending) through
    pdftotext in both readings (-layout and -raw), and once more with the line numbers a bill or an analysis prints at
    the start of each line dropped; an HTML page as its text, and once more with struck words (text-decoration:
    line-through, the marks of an act's changes to its bill) dropped, as D3's read_via says they were read."""
    raw = open(path, "rb").read()
    if raw[:4] == b"%PDF" or path.endswith(".pdf"):
        lay = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout
        rw = subprocess.run(["pdftotext", "-raw", path, "-"], capture_output=True, text=True).stdout
        def nonum(x):   # a line number alone on its line, or at the start of a line of text
            x = re.sub(r"(?m)^[ \t]*\d{1,3}[ \t]*\n", "", x)
            return re.sub(r"(?m)^[ \t]*\d{1,3}[ \t]+(?=\S)", "", x)
        dehyph = re.sub(r"(\w)-[ \t]*\n[ \t]*(\w)", r"\1\2", rw)   # a word hyphenated at a line's end, joined
        return [("word for word", C28.norm(lay) + " \n " + C28.norm(rw)),
                ("word for word, the page's line numbers dropped", C28.norm(nonum(lay)) + " \n " + C28.norm(nonum(rw))),
                ("word for word, line-end hyphens joined", C28.norm(dehyph))]
    try:
        s = raw.decode("utf-8")
    except UnicodeDecodeError:
        s = raw.decode("cp1252", errors="replace")
    s = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", s)
    struck = re.sub(r"(?is)<span style=['\"]text-decoration:\s*line-through;?['\"]>.*?</span>", "", s)
    plain = lambda x: C28.norm(re.sub(r"(?s)<[^>]+>", " ", x))
    tight = lambda x: re.sub(r"\s+([.,;:])", r"\1", x)   # the space a dropped tag leaves before a stop
    return [("word for word", plain(s)), ("word for word, struck words dropped", tight(plain(struck)))]


def section_3():
    print("### 30.3 the four rules read in step (a) and a sample of the ballot texts' quotes, against the pages fetched by me")
    p = os.path.join(PAGES, "index.txt")
    if not os.path.exists(p):
        print("  no pages fetched (see the script's header): nothing compared")
        return
    idx = []
    for line in open(p):
        parts = line.rstrip("\n").split("\t")
        if len(parts) >= 6:
            idx.append(parts)
    book = L.load_json(THRESH)
    texts = L.load_json(TEXTS)["questions"]
    tal = collections.Counter()
    codes = collections.Counter(x[1] for x in idx)
    print(f"  pages: {len(idx)} fetched, HTTP codes {dict(codes)}")
    for n, code, when, key, url, path in idx:
        if code != "200" or not os.path.exists(path):
            print(f"  {key[:60]}: not fetched ({code})")
            tal["not fetched"] += 1
            continue
        reads = readings(path)
        text = reads[0][1]
        checks = []
        if key.startswith("rule:"):
            _, st, cit = key.split(":", 2)
            rs = [r for r in book["rules"] if r["state"] == st and r["citation"] == cit]
            for r in rs:
                checks.append(("the rule's quote", r["quote"]))
                if r.get("url") != url:
                    checks.append(("URL", None))
        else:
            kind, cid = key.split(":", 1)
            q = texts[cid]
            if kind == "q":
                if q.get("type_quote"):
                    checks.append(("type_quote", q["type_quote"]))
                fs = (q.get("fact") or {}).get("source")
                fu = fs.get("url") if isinstance(fs, dict) else None
                if (q.get("fact") or {}).get("quote") and (fu is None or fu == url):
                    checks.append(("fact.quote", q["fact"]["quote"]))
            else:
                if (q.get("fact") or {}).get("quote"):
                    checks.append(("fact.quote", q["fact"]["quote"]))
        found = []
        for name, quote in checks:
            if quote is None:
                found.append(f"{name} DIFFERS")
                continue
            nq = C28.norm(quote)
            hit = next((lab for lab, tx in reads if nq in tx), None)
            if hit:
                found.append(f"{name}: {hit}")
                tal[hit] += 1
            elif C28.loose(nq) in C28.loose(text):
                found.append(f"{name}: letters and digits")
                tal["letters and digits"] += 1
            else:
                lo, hi = 0, len(nq)
                while lo < hi:
                    mid = (lo + hi + 1) // 2
                    if nq[:mid] in text:
                        lo = mid
                    else:
                        hi = mid - 1
                found.append(f"{name}: NOT FOUND (longest prefix {lo} of {len(nq)})")
                tal["NOT FOUND"] += 1
        print(f"  {key[:70]}: {len(text):,} chars; {found}")
    print(f"  quotes: {dict(tal)}")
    unread = L.load_json(TEXTS).get("unread") or []
    print(f"  pages D3 could not read ({len(unread)}, in ballot-texts.json 'unread'): not tried here; the sample above keeps off those hosts")


# ---------------------------------------------------------------------------------------------- 30.4
def section_4(by_id):
    print("### 30.4 the 67 new p recomputed from my own pool of like measures, their note, and the back-test's counts")
    pool = C15.measure_pool()
    by_key = collections.defaultdict(list)
    for y, k, s, _ in pool:
        by_key[k].append((y, s))
    rows = {r["id"]: r for r in D.rows("measure")}
    new = [cid for cid, row in by_id.items() if row["code"] == "N"]
    tal = collections.Counter()
    worst = 0.0
    bad = []
    noted = 0
    by_state = collections.Counter()
    ts = collections.Counter()
    for cid in sorted(new):
        r = rows.get(cid)
        if r is None or r["status"] != "value":
            tal["no row with p"] += 1
            continue
        by_state[r["state"]] += 1
        t = r["t"]
        ts[t] += 1
        sh = [s for y, s in by_key[r["cls"]] if y < r["year"]]
        f, N, h, k = D.density_at(sh, t)
        if f is None:
            tal["too few in my pool"] += 1
            continue
        yes = sum(a[1] or 0 for a in r["cands"] if C15.side(a[2]) == "yes")
        no = sum(a[1] or 0 for a in r["cands"] if C15.side(a[2]) == "no")
        n = yes + no - 1
        p = r["p"]
        y_, n_ = (1 - t) * f / n, t * f / n
        same = (N == r["N"], k == r["kin"], abs(h - D.window_h(r["win"])) < 1e-9, abs(round(k / N, 5) - r["q"]) < 1e-9,
                rel(f, p["f_t"]) <= 1e-5, n == p.get("n"), rel(y_, p["yes"]) <= 1e-5, rel(n_, p["no"]) <= 1e-5, rel(max(y_, n_), p["value"]) <= 1e-5)
        worst = max(worst, rel(max(y_, n_), p["value"]))
        tal["(N, k, h, q, f_t, n, yes, no, value) all equal" if all(same) else "DIFFERS"] += 1
        if not all(same):
            bad.append((cid, f"mine N {N} k {k} h {h} f {f:.6g} n {n} value {max(y_, n_):.6g}; record N {r['N']} k {r['kin']} win {r['win']} f_t {p['f_t']} n {p.get('n')} value {p['value']}"))
        if "11 against 6.8" in (p.get("note") or "") and "10 against 6.2" in (p.get("note") or ""):
            noted += 1
    print(f"  {len(new)} new p: {dict(tal)}; worst relative difference on the value {worst:.2e}; by state {dict(sorted(by_state.items(), key=lambda x: -x[1]))}; thresholds {dict(sorted(ts.items()))}")
    print(f"  D3: AZ 13, LA 13, CO 10, FL 9, RI 7, OR 5, NM 3, ME 3, AR 1, GA 1, ID 1, OH 1")
    for cid, s in bad[:8]:
        print(f"    {cid}: {s}")
    print(f"  the statewide note (11 against 6.8 within 1 point of ½, 10 against 6.2 within 20,000 votes) on {noted} of the {len(new)}")
    allp = [r for r in rows.values() if r["route"] == "like past measures" and r["status"] == "value" and r["cls"] == "statewide measure"]
    print(f"  statewide measures with p now: {len(allp)} (D3: 132, from 65); with the note {sum(1 for r in allp if '11 against 6.8' in (r['p'].get('note') or ''))}")
    # the T rows: like measures in earlier years from my pool
    sh16 = [s for y, s in by_key["statewide measure"] if y < 2016]
    sh18 = [s for y, s in by_key["statewide measure"] if y < 2018]
    tro = collections.Counter(int(cid[:4]) for cid, row in by_id.items() if row["code"] == "T")
    print(f"  the T rows by year {dict(sorted(tro.items()))}; my pool's like statewide measures before 2016: {len(sh16)}, before 2018: {len(sh18)} (D3: none, 83; under {D.MIN_CLASS})")
    # the back-test's at-threshold counts (2022-2024), rebuilt for the 132
    rec = L.load_json(os.path.join(L.DATA, "measure", "backtest-measures.json"))["at_threshold"]
    g = {"measures": 0, "own": [0.0, 0], "near": {str(hh): [0.0, 0] for hh in D.WINDOWS}}
    for r in allp:
        tr = [x for yy, x in by_key[r["cls"]] if yy < r["year"]]
        v0, v1 = r["pair"]["votes"]
        s = v0 / (v0 + v1)
        h = D.window_h(r["win"])
        g["measures"] += 1
        g["own"][0] += r["q"]
        g["own"][1] += int(abs(s - r["t"]) <= h + 1e-12)
        for hh in D.WINDOWS:
            g["near"][str(hh)][0] += sum(1 for x in tr if abs(x - r["t"]) <= hh) / len(tr)
            g["near"][str(hh)][1] += int(abs(s - r["t"]) <= hh)
    got = rec.get("all years")
    mstr = f"own window {g['own'][0]:.1f}/{g['own'][1]}, " + ", ".join(f"within {float(hh):.0%} {v[0]:.1f}/{v[1]}" for hh, v in g["near"].items())
    rstr = (f"own window {got['own_window']['expected']}/{got['own_window']['seen']}, " + ", ".join(f"within {hh} {v['expected']}/{v['seen']}" for hh, v in got["near_threshold"].items())) if got else "absent"
    print(f"  at the threshold, all years ({g['measures']} measures): mine {mstr} | record {rstr} ({got['measures'] if got else '-'})")


def main():
    print(f"c30: #81 (step (a): each held statewide question's own ballot text); HEAD {L.git_head()}; before {BEFORE}, after {AFTER}")
    moves = L.load_json(MOVES)
    by_id, mine = section_1(moves)
    section_2(by_id)
    section_3()
    section_4(by_id)


if __name__ == "__main__":
    main()
