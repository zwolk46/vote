"""C18. Louisiana's own 2024 results (D3's #62; the orchestrator, 2026-11-07 10:54, the third pass's item 4): the
Secretary of State's four official workbooks read by my own parser (not pipeline/intake/la_sos.py), then
  18.1 the gate: the file's Democratic and Republican votes of 2024-11-05 against D1's certified presidential count and
       D2's six House districts (data/president/2024.json, data/house/2024.json), by party and by candidate;
  18.2 the rounds: every office contest paired across the two dates of each pair (2024-03-23 to 04-27, 11-05 to 12-07)
       by its sheet and title with the seats clause stripped; the counts against data/local/check-la.json; the one
       general without a primary looked for under a near title; the 'to runoff' and 'won' marks;
  18.3 the files: every contest of data/local/2024/LA.json and data/measure/2024/LA.json against my parse (date, parish,
       seats, candidates, votes, round words, the parish FIPS by the Census's alphabetical odd-number rule);
  18.4 the nine p recomputed from my own like-race pool (c15's MEDSL route pool, earlier years only) and the recorded
       forecast (the partisan route), and the five statewide amendments' place in the measures' back-test (c16).
Needs the four workbooks in m2lib.CACHE/la_sos/ (fetched by curl from the site's own download addresses, 4 s apart).
[measured] throughout; the record's counts [stated].
"""
import collections
import glob
import json
import os
import re
import sys
import warnings

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402
import m2d3 as D  # noqa: E402
import c15_d3_refit as C15  # noqa: E402

DATES = ("2024-03-23", "2024-04-27", "2024-11-05", "2024-12-07")
PAIRS = {"2024-04-27": "2024-03-23", "2024-12-07": "2024-11-05"}
ROOT = os.path.join(L.CACHE, "la_sos")
SEATS = re.compile(r"\s*\((\d+) to be elected\)\s*$")
PARTY = re.compile(r"^(.*?)\s*\(([A-Z]+)\)\s*$")
ANSWER = re.compile(r"^(YES|NO|FOR|AGAINST)\s*(RECALL)?$", re.I)
FEDERAL = re.compile(r"^(Presidential Electors|Presidential Nominee|U\. S\. (Representative|Senator))")
COMMITTEE = re.compile(r"^(DSCC|RSCC|DPEC|RPEC) Member")
PARISHES = ["Acadia", "Allen", "Ascension", "Assumption", "Avoyelles", "Beauregard", "Bienville", "Bossier", "Caddo",
            "Calcasieu", "Caldwell", "Cameron", "Catahoula", "Claiborne", "Concordia", "De Soto", "East Baton Rouge",
            "East Carroll", "East Feliciana", "Evangeline", "Franklin", "Grant", "Iberia", "Iberville", "Jackson",
            "Jefferson", "Jefferson Davis", "Lafayette", "Lafourche", "La Salle", "Lincoln", "Livingston", "Madison",
            "Morehouse", "Natchitoches", "Orleans", "Ouachita", "Plaquemines", "Pointe Coupee", "Rapides", "Red River",
            "Richland", "Sabine", "St. Bernard", "St. Charles", "St. Helena", "St. James", "St. John the Baptist",
            "St. Landry", "St. Martin", "St. Mary", "St. Tammany", "Tangipahoa", "Tensas", "Terrebonne", "Union",
            "Vermilion", "Vernon", "Washington", "Webster", "West Baton Rouge", "West Carroll", "West Feliciana", "Winn"]
# the Census Bureau numbers Louisiana's 64 parishes in alphabetical order with the odd numbers 001-127 [inferred from
# the rule's holding on every place checked by hand: Ferriday (Concordia) 22029, Gonzales (Ascension) 22005, Benton
# (Bossier) 22015, Franklinton and Bogalusa (Washington) 22117, Amite City (Tangipahoa) 22105, Alexandria (Rapides)
# 22079, Abita Springs (St. Tammany) 22103, Plaquemine (Iberville) 22047, Colfax (Grant) 22043]
FIPS = {re.sub(r"[^a-z]", "", n.lower()): f"22{2 * i + 1:03d}" for i, n in enumerate(PARISHES)}


def _norm(s):
    return re.sub(r"[^a-z]", "", str(s).lower())


def parse(path, date):
    """My own reading of one workbook: every contest found from its 'Total Votes' line upward (the title two rows
    above, the choices one row above), its parish or precinct lines below until a blank row."""
    import openpyxl
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    out, bad = [], []
    for sheet in wb.sheetnames:
        if sheet == "Multi-Parish(Precinct)":
            continue
        rows = [tuple(x for x in r if x is not None) for r in wb[sheet].iter_rows(values_only=True)]
        for i, r in enumerate(rows):
            if not r or r[0] != "Total Votes" or i < 2:
                continue
            names, title = rows[i - 1], rows[i - 2]
            if len(title) != 1 or not isinstance(title[0], str):
                bad.append((sheet, i, "no title line"))
                continue
            totals = list(r[1:])
            if len(totals) != len(names):
                bad.append((sheet, i, f"{len(names)} choices, {len(totals)} totals"))
                continue
            lines = []
            j = i + 1
            while j < len(rows) and rows[j]:
                lines.append(rows[j])
                j += 1
            t = " ".join(title[0].split())
            m = SEATS.search(t)
            cands = []
            for k, x in enumerate(names):
                x = " ".join(str(x).split())
                pm = PARTY.match(x)
                cands.append({"name": pm.group(1) if pm else x, "party": pm.group(2) if pm else "", "votes": int(totals[k] or 0)})
            sums = [sum(int(ln[k + 1] or 0) for ln in lines if len(ln) == len(names) + 1) for k in range(len(names))]
            out.append({"date": date, "sheet": sheet, "multi": sheet == "Multi-Parish(Parish)", "title": t,
                        "base": SEATS.sub("", t), "seats": int(m.group(1)) if m else 1,
                        "question": all(ANSWER.match(c["name"]) for c in cands), "cands": cands,
                        "parishes": [str(ln[0]).strip() for ln in lines] if sheet == "Multi-Parish(Parish)" else [sheet],
                        "adds_up": sums == [c["votes"] for c in cands], "n_lines": len(lines),
                        "short_line": any(len(ln) != len(names) + 1 for ln in lines)})
    return out, bad


def load_all():
    cs, bad = [], []
    for d in DATES:
        path = os.path.join(ROOT, d.replace("-", "") + ".xlsx")
        if not os.path.exists(path):
            print(f"  {d}: workbook not in {ROOT}; c18 cannot run")
            return None, None
        c, b = parse(path, d)
        cs += c
        bad += b
    return cs, bad


def key(c):
    return (c["date"], "multi" if c["multi"] else c["sheet"], c["base"])


def rounds(cs):
    on = collections.defaultdict(dict)
    for c in cs:
        if not c["question"]:
            on[("multi" if c["multi"] else c["sheet"], c["base"])][c["date"]] = c
    out = {}
    for c in cs:
        if c["question"]:
            out[id(c)] = ("question", None, None)
            continue
        k = ("multi" if c["multi"] else c["sheet"], c["base"])
        if c["date"] in PAIRS.values():
            g = next((d for d, p in PAIRS.items() if p == c["date"] and d in on[k]), None)
            out[id(c)] = ("first", g, on[k].get(g))
        else:
            p = PAIRS[c["date"]]
            out[id(c)] = ("deciding", p, on[k][p]) if p in on[k] else ("general, no primary", None, None)
    return out


def major(party):
    p = (party or "").upper()
    return "D" if p in ("DEM", "D", "DEMOCRAT", "DEMOCRATIC") else "R" if p in ("REP", "R", "REPUBLICAN") else None


def gate(cs):
    print("18.1 The gate: the state's file on 2024-11-05 against D1's and D2's certified federal counts")
    nov = [c for c in cs if c["date"] == "2024-11-05"]
    pres = [c for c in nov if c["title"].startswith("Presidential Electors")]
    cert = next(c for c in L.load_json(os.path.join(L.DATA, "president", "2024.json"))["contests"] if c["place"]["state"] == "LA")
    worst = 0.0
    for side in ("D", "R"):
        a = sum(x["votes"] for c in pres for x in c["cands"] if major(x["party"]) == side)
        b = sum(x["votes"] for x in cert["result"]["candidates"] if major(x.get("party")) == side)
        worst = max(worst, abs(a - b) / b)
        print(f"  president {side}: the state's file {a:,} ({len(pres)} contest, {sum(c['n_lines'] for c in pres)} parish lines, adds up {all(c['adds_up'] for c in pres)}), D1 {b:,}: {'equal' if a == b else f'differ by {a - b:+,}'}")
    house = {}
    for c in nov:
        m = re.match(r"^U\. S\. Representative -- (\d+)(st|nd|rd|th) Congressional District", c["title"])
        if m:
            house[int(m.group(1))] = c
    certh = {int(x["place"]["district"]): x for x in L.load_json(os.path.join(L.DATA, "house", "2024.json"))["contests"]
             if x["place"]["state"] == "LA" and not x.get("special")}
    print(f"  House: the state's file has {len(house)} districts ({sorted(house)}), D2's file {len(certh)} ({sorted(certh)})")
    tot = {"D": [0, 0], "R": [0, 0]}
    for d in sorted(set(house) | set(certh)):
        if d not in house or d not in certh:
            print(f"    district {d}: in one file only")
            continue
        a_votes = sorted(x["votes"] for x in house[d]["cands"])
        b_votes = sorted(x["votes"] for x in certh[d]["result"]["candidates"] if x.get("party") not in ("W",) and x["votes"])
        parts = []
        for side in ("D", "R"):
            a = sum(x["votes"] for x in house[d]["cands"] if major(x["party"]) == side)
            b = sum(x["votes"] for x in certh[d]["result"]["candidates"] if major(x.get("party")) == side)
            tot[side][0] += a
            tot[side][1] += b
            if b:
                worst = max(worst, abs(a - b) / b)
            parts.append(f"{side} {a:,}/{b:,}")
        print(f"    district {d}: " + ", ".join(parts) + f"; candidates' vote counts {'the same multiset' if a_votes == b_votes else 'differ: ' + str(a_votes) + ' vs ' + str(b_votes)} ({len(a_votes)} in the state's file, {len(b_votes)} in D2's)")
    print(f"  House D {tot['D'][0]:,} against {tot['D'][1]:,}; R {tot['R'][0]:,} against {tot['R'][1]:,}; worst relative miss over the eight party counts {worst:.2e} "
          f"(check-la.json: worst_miss {json.load(open(os.path.join(L.DATA, 'local', 'check-la.json')))['gate']['worst_miss']})")


def rounds_check(cs):
    print("18.2 The rounds: first rounds paired to their deciding rounds by sheet and title (the seats clause stripped)")
    rd = rounds(cs)
    t = collections.Counter()
    for c in cs:
        if FEDERAL.match(c["title"]):
            t["left out: the presidency, its primaries and Congress"] += 1
        elif COMMITTEE.match(c["title"]):
            t["left out: the parties' committees"] += 1
        else:
            t[f"{c['date']}: {rd[id(c)][0]}"] += 1
    rec = json.load(open(os.path.join(L.DATA, "local", "check-la.json")))["contests"]
    same = all(rec.get(k) == v for k, v in t.items()) and set(rec) == set(t)
    print(f"  my counts {'equal' if same else 'DIFFER FROM'} check-la.json's: " + "; ".join(f"{k} {v}" + ("" if rec.get(k) == v else f" (record {rec.get(k)})") for k, v in sorted(t.items())))
    print(f"  contests parsed {len(cs):,}; lines that add up to the total in {sum(c['adds_up'] for c in cs):,}; with a short line {sum(c['short_line'] for c in cs)}")
    # the pairing: a deciding round's primary has the same choices' names among its candidates?
    paired = [(c, rd[id(c)][2]) for c in cs if rd[id(c)][0] == "deciding"]
    names_ok = sum(1 for c, p in paired if {x["name"] for x in c["cands"]} <= {x["name"] for x in p["cands"]})
    print(f"  deciding rounds {len(paired)}: every candidate's name also on the primary's ballot in {names_ok}; "
          + ("; ".join(f"{c['date']} {c['sheet']} '{c['base'][:50]}': {sorted({x['name'] for x in c['cands']} - {x['name'] for x in p['cands']})}" for c, p in paired if not {x["name"] for x in c["cands"]} <= {x["name"] for x in p["cands"]}) or "none differ"))
    two = sum(1 for c, p in paired if len(c["cands"]) == 2 * c["seats"])
    print(f"  deciding rounds with exactly twice the seats on the ballot {two} of {len(paired)}; the others: "
          + ("; ".join(f"'{c['base'][:40]}' {len(c['cands'])} for {c['seats']}" for c, p in paired if len(c["cands"]) != 2 * c["seats"]) or "none"))
    # the general without a primary: a near title on the primary's date?
    for c in cs:
        if rd[id(c)][0] == "general, no primary":
            near = [x for x in cs if x["date"] == PAIRS[c["date"]] and x["sheet"] == c["sheet"] and not x["question"]
                    and _norm(x["base"].split("--")[-1]) == _norm(c["base"].split("--")[-1])]
            print(f"  general without a primary: {c['date']} {c['sheet']} '{c['title']}', {len(c['cands'])} candidates for {c['seats']} seats; "
                  f"contests of the same place on {PAIRS[c['date']]}: " + ("; ".join(f"'{x['title']}'" for x in near) or "none") + "; names of its candidates on that date's ballot of the same sheet: "
                  + str(sorted({x["name"] for x in c["cands"]} & {y["name"] for x in cs if x["date"] == PAIRS[c["date"]] and x["sheet"] == c["sheet"] for y in x["cands"]})))
    # majority in the first round: how many first rounds were decided outright (no later round)
    first = [c for c in cs if rd[id(c)][0] == "first" and not FEDERAL.match(c["title"]) and not COMMITTEE.match(c["title"])]
    decided = [c for c in first if rd[id(c)][1] is None]
    lead = [max(x["votes"] for x in c["cands"]) / max(1, sum(x["votes"] for x in c["cands"])) for c in decided if c["seats"] == 1]
    under = [c for c in decided if c["seats"] == 1 and max(x["votes"] for x in c["cands"]) < 0.5 * sum(x["votes"] for x in c["cands"])]
    print(f"  first rounds {len(first)}: {len(decided)} with no later round of the contest (decided in the primary), {len(first) - len(decided)} followed by one; "
          f"of the single-seat ones decided in the primary ({len(lead)}), the leader's share of all votes was under 50% in {len(under)} "
          f"(a majority elects in Louisiana's primary; under 50% with no later round is a runoff the source does not hold, a withdrawal, or a pairing miss): "
          + "; ".join(f"{c['date']} {c['sheet']} '{c['base'][:45]}' " + ", ".join(f"{x['name']} {x['votes']:,}" for x in sorted(c['cands'], key=lambda x: -x['votes'])[:3]) for c in under))
    return rd


def files_check(cs, rd):
    print("18.3 The files against my parse: data/local/2024/LA.json and data/measure/2024/LA.json")
    mine = {}
    for c in cs:
        if FEDERAL.match(c["title"]) or COMMITTEE.match(c["title"]):
            continue
        mine.setdefault((c["date"], c["multi"], c["sheet"], _norm(c["base"])), []).append(c)
    loc = L.load_json(os.path.join(L.DATA, "local", "2024", "LA.json"))["contests"]
    mea = L.load_json(os.path.join(L.DATA, "measure", "2024", "LA.json"))["contests"]
    sheet_fips = {}
    for c in cs:
        if not c["multi"]:
            sheet_fips[c["sheet"]] = FIPS.get(_norm(c["sheet"]))
    unknown = sorted(s for s, f in sheet_fips.items() if f is None)
    print(f"  parish sheets {len(sheet_fips)}; sheet names not among the 64 parishes: {unknown or 'none'}")
    t = collections.Counter()
    bad = []
    used = set()
    for f in loc + mea:
        q = "question" in f
        if f.get("party_office"):
            t["local: a party committee (18.5)"] += 1
            continue
        title = (f["question"]["title"] if q else f["office"])
        cands = [(_norm(x["name"]), x["votes"]) for x in f["result"]["candidates"]]
        hits = [c for k, v in mine.items() if k[0] == f["date"] for c in v
                if c["question"] == q and sorted(x["votes"] for x in c["cands"]) == sorted(v_ for _, v_ in cands)
                and {_norm(x["name"]) for x in c["cands"]} == {n for n, _ in cands}]
        if len(hits) != 1:
            t[f"{'measure' if q else 'local'}: {len(hits)} parses with these candidates and votes"] += 1
            bad.append((f["id"], len(hits)))
            continue
        c = hits[0]
        used.add(id(c))
        t[f"{'measure' if q else 'local'}: matched"] += 1
        # seats, parishes, round words, won marks
        if not q:
            if (f.get("seats") or 1) != c["seats"]:
                bad.append((f["id"], f"seats {f.get('seats')} vs {c['seats']}"))
                t["seats differ"] += 1
            r = rd[id(c)]
            el = f["election"]
            want = {"first": "first round", "deciding": "deciding round after an earlier round on " + str(r[1]),
                    "general, no primary": "Louisiana's general election date, with no primary"}[r[0]]
            if not el.startswith(want):
                bad.append((f["id"], f"election '{el[:60]}' vs my round {r[0]} {r[1]}"))
                t["round words differ"] += 1
            if r[0] == "first":
                if r[1] and "followed on " + r[1] not in el:
                    bad.append((f["id"], f"'{el[:70]}': my later round {r[1]}"))
                    t["first round's later date differs"] += 1
                if not r[1] and "decided in it" not in el:
                    bad.append((f["id"], f"'{el[:70]}': I find no later round"))
                    t["first round's later date differs"] += 1
            # won marks
            order = sorted(c["cands"], key=lambda x: -x["votes"])
            k = c["seats"]
            if r[0] == "first" and r[2] is not None:
                later = {x["name"] for x in r[2]["cands"]}
                top = max((x["votes"] for x in order if x["name"] in later), default=0)
                want_won = {_norm(x["name"]): ("to runoff" if x["name"] in later else True if x["votes"] > top else None) for x in order}
            else:
                tie = len(order) > k and order[k - 1]["votes"] == order[k]["votes"]
                winners = set() if tie else {x["name"] for x in order[:k]}
                want_won = {_norm(x["name"]): (True if x["name"] in winners else None) for x in order}
            got = {_norm(x["name"]): x.get("won") for x in f["result"]["candidates"]}
            if got != want_won:
                bad.append((f["id"], f"won marks {got} vs {want_won}"))
                t["won marks differ"] += 1
        fips = sorted({FIPS.get(_norm(p)) for p in c["parishes"]} - {None}) if c["multi"] else [sheet_fips[c["sheet"]]]
        if len(fips) == 64 and not f["place"].get("counties"):
            t["statewide (all 64 parishes; the file names no parish)"] += 1
        elif sorted(f["place"].get("counties") or []) != sorted(x for x in fips if x):
            bad.append((f["id"], f"counties {f['place'].get('counties')} vs {fips}"))
            t["parish FIPS differ"] += 1
        if q:
            yes = next((x["votes"] for x in f["result"]["candidates"] if x["name"].upper().startswith(("YES", "FOR"))), None)
            tot = sum(x["votes"] for x in f["result"]["candidates"])
            if yes is not None and tot and abs(f["result"].get("yes_share", -1) - yes / tot) > 1e-6:
                bad.append((f["id"], "yes_share"))
                t["yes_share differs"] += 1
            scope = "statewide" if (c["multi"] and len({FIPS.get(_norm(p)) for p in c["parishes"]} - {None}) == 64) else "local"
            if f["question"].get("scope") != scope:
                bad.append((f["id"], f"scope {f['question'].get('scope')} vs {scope}"))
                t["scope differs"] += 1
    notin = [c for v in mine.values() for c in v if id(c) not in used]
    print(f"  files: {len(loc)} local contests, {len(mea)} questions; " + "; ".join(f"{k} {v}" for k, v in sorted(t.items())))
    print(f"  my parse's contests (federal and committees aside) not matched by any file contest: {len(notin)}" + (": " + "; ".join(f"{c['date']} {c['sheet']} '{c['base'][:40]}'" for c in notin[:6]) if notin else ""))
    for rid, what in bad[:12]:
        print(f"    {rid[:80]}: {what}")
    return loc, mea


def p_check(loc):
    print("18.4 The nine p from my own pool and the recorded inputs; the amendments in the measures' back-test")
    medsl, nc, miss = C15.local_pools()
    by_key = collections.defaultdict(list)
    for y, k, s in medsl:
        by_key[k].append((y, s))
    la_pool = [r for r in D.rows("local") if r["state"] == "LA" and r["src"] == "la_sos"]
    in_pool = sum(1 for r in la_pool if r["route"] in ("class", "boundary") or (r["cls"] and not r["route"]))
    print(f"  Louisiana's contests in my MEDSL-route pool (like races for later years): {in_pool} (deciding rounds with a class)")
    for r in la_pool:
        if r["status"] != "value":
            continue
        n = r["p"]["n"]
        if r["route"] in ("class", "boundary"):
            sh = [s for y, s in by_key.get(r["cls"], []) if y < r["year"]]
            f, N, h, k = D.class_density(sh)
            if f is None:
                print(f"    {r['id'][:70]}: my pool has {N} like races < 100; record N {r['N']}")
                continue
            sd = D.sd_eq(f)
            pm, meth, fh = D.p_auto(n, 0.5, sd)
            same = (N == r["N"], k == r["kin"], abs(h - D.window_h(r["win"])) < 1e-9, abs(round(k / N, 5) - r["q"]) < 1e-9)
            print(f"    {r['id'][:70]}: {r['route']}; (N, k, h, q) mine ({N}, {k}, {h}, {k / N:.5f}) record ({r['N']}, {r['kin']}, {D.window_h(r['win'])}, {r['q']}) {'equal' if all(same) else 'DIFFER'}; "
                  f"p mine {pm:.6g} ({meth}) record {r['p']['value']:.6g} ({r['p']['method']}); rel {D.rel(pm, r['p']['value']):.1e}")
        else:
            sh = r["share"]
            pm, meth, fh = D.p_auto(n, sh["mean"], sh["sd"], sh.get("tails", "normal"))
            print(f"    {r['id'][:70]}: partisan, mean {sh['mean']:.4f} sd {sh['sd']:.4f}; p mine {pm:.6g} ({meth}) record {r['p']['value']:.6g} ({r['p']['method']}); rel {D.rel(pm, r['p']['value']):.1e}"
                  + (" (the record's partisan exact sum keeps common.py's cut at mean +- 0.5; c14 allows it)" if meth == "exact" else ""))
    pool = C15.measure_pool()
    la = [(y, k, s, rid) for y, k, s, rid in pool if "-LA-" in rid and y == 2024]
    sw = [x for x in la if x[1] == "statewide measure"]
    print(f"  Louisiana's 2024 questions in my measure pool: {len(la)} ({dict(collections.Counter(k for _, k, _, _ in la))}); the five statewide amendments: "
          + "; ".join(f"{rid.split('-LA-')[1][:22]} yes {s:.3f}" for _, _, s, rid in sw))
    n24 = sum(1 for y, k, _, _ in pool if y == 2024 and k == "statewide measure")
    print(f"  2024 statewide measures in the pool: {n24} (the record's near-half table: 119, of which Louisiana's 5); c16 reproduces the note's 52 against 36.4 from this pool")


def main():
    print("C18. LOUISIANA'S OWN 2024 RESULTS: THE GATE, THE ROUNDS, THE FILES AND THE NINE p")
    print(f"repository HEAD {L.git_head()}")
    cs, bad = load_all()
    if cs is None:
        return
    print(f"  parsed {len(cs):,} contests from the four workbooks by my own reader: " + "; ".join(f"{d} {sum(1 for c in cs if c['date'] == d)}" for d in DATES)
          + f"; blocks I could not read: {bad or 'none'}")
    gate(cs)
    rd = rounds_check(cs)
    loc, mea = files_check(cs, rd)
    p_check(loc)
    committees_check(cs, rd, loc)


def committees_check(cs, rd, loc):
    """18.5 #68: the parties' committees (La. R.S. 18:443, 18:444), 241 contests of 2024-03-23 with no p."""
    import html
    print("18.5 #68: the parties' committees against my parse, their words, and the statutes' text")
    mine = [c for c in cs if COMMITTEE.match(c["title"])]
    by_kind = collections.Counter(c["title"][:4] for c in mine)
    print(f"  my parse: {len(mine)} committee contests on {sorted({c['date'] for c in mine})}, by committee {dict(sorted(by_kind.items()))} (the record: 241 of 2024-03-23: DSCC 84, RSCC 83, RPEC 43, DPEC 31)")
    later = sum(1 for c in mine if rd[id(c)][0] != "first" or rd[id(c)][1])
    print(f"  committee contests with a later round of the name in the source: {later} (so each is decided in one round, as the statute says)")
    fc = [f for f in loc if f.get("party_office")]
    t = collections.Counter()
    bad = []
    used = set()
    for f in fc:
        cands = [(_norm(x["name"]), x["votes"]) for x in f["result"]["candidates"]]
        hits = [c for c in mine if c["date"] == f["date"] and sorted(x["votes"] for x in c["cands"]) == sorted(v for _, v in cands)
                and {_norm(x["name"]) for x in c["cands"]} == {n for n, _ in cands} and _norm(c["base"]) == _norm(f["office"])]
        if len(hits) != 1:
            t[f"{len(hits)} parses with these candidates and votes"] += 1
            bad.append((f["id"], len(hits)))
            continue
        c = hits[0]
        used.add(id(c))
        t["matched"] += 1
        po = f["party_office"]
        want_party = "D" if c["title"][0] == "D" else "R"
        if po.get("party") != want_party:
            bad.append((f["id"], f"party {po.get('party')} vs {want_party}"))
            t["party differs"] += 1
        want_law = "18:443" if c["title"][1:4] == "SCC" else "18:444"
        if want_law not in (po.get("law") or ""):
            bad.append((f["id"], f"law {po.get('law')} vs {want_law}"))
            t["law differs"] += 1
        if (f.get("seats") or 1) != c["seats"]:
            bad.append((f["id"], f"seats {f.get('seats')} vs {c['seats']}"))
            t["seats differ"] += 1
        if "value" in f["p"]:
            bad.append((f["id"], "has p"))
            t["HAS p"] += 1
        if not (f["p"].get("not_computed") or "").startswith("fewer than 100 like races"):
            t["another reason"] += 1
        if "decided in it" not in f["election"] or "18:443, 18:444" not in f["election"]:
            t["election words differ"] += 1
        if f.get("office_type") != "council, commission or board":
            t["office type not 'council, commission or board'"] += 1
    seats = collections.Counter(min(f.get("seats") or 1, 2) for f in fc)
    print(f"  the file's {len(fc)} party-committee contests: " + "; ".join(f"{k} {v}" for k, v in sorted(t.items()))
          + f"; my parse's committee contests not matched: {len(mine) - len(used)}; seats: one {seats.get(1, 0)}, several {seats.get(2, 0)} (the record: 212 one, 29 with 5 to 14; max here {max((f.get('seats') or 1) for f in fc)})")
    for rid, what in bad[:6]:
        print(f"    {rid[:80]}: {what}")
    # the statutes' text, read from the pages fetched by curl into the cache (legis.la.gov Law.aspx?d=81577, 81580)
    for d, sec in (("81577", "18:443"), ("81580", "18:444")):
        path = os.path.join(L.CACHE, "la_sos", "law", f"law_{d}.html")
        if not os.path.exists(path):
            print(f"  {sec}: the page is not in the cache ({path}); fetched by curl -sSL from https://legis.la.gov/Legis/Law.aspx?d={d}")
            continue
        txt = open(path, encoding="utf-8", errors="replace").read()
        txt = re.sub(r"<script.*?</script>", " ", txt, flags=re.S)
        txt = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", txt)).split())
        phrases = ["every four years at the same time as the presidential preference primary election",
                   "the candidate who receives the greater number of votes cast shall be elected"]
        found = {ph[:40] + "...": ph in txt for ph in phrases}
        i = txt.find("tie")
        lot = bool(re.search(r"\btie\b.{0,200}\blot\b|\blot\b.{0,200}\btie\b", txt))
        print(f"  La. R.S. {sec} (the page's text): {found}; a tie decided by lot: {lot}; section heading: '{txt[txt.find('§4'):txt.find('§4') + 40]}'")


if __name__ == "__main__":
    main()
