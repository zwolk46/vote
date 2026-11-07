"""C22. Louisiana's own 2023 results (D3's #70; the orchestrator's note of 2026-11-07 12:04 UTC, the third pass's item 5):
the Secretary of State's seven official 2023 workbooks read by c18's parser (not pipeline/intake/la_sos.py), then
  22.1 the gate within the certifying source (the orchestrator, 11:16): (a) each date marked official on the site's
       list, (b) each contest's parishes' or precincts' lines add up to its total, (c) each contest on more than one
       parish's ballot equal, choice by choice, to the site's own posted results of its date (the posted files
       fetched by curl); the workbooks' hashes against the record's;
  22.2 the rounds: the pairs 2023-02-18 -> 03-25 (the 93rd district's special), 03-25 -> 04-29 and 10-14 -> 11-18, and
       the two contests held again on 12-16 after exact ties; the counts against data/local/check-la.json's 2023;
  22.3 the four files (local, measure, state-lower, state-upper) against my parse: candidates, votes, seats, parish
       FIPS or district, round words, won marks, the ties' notes, yes_share and scope;
  22.4 the 29 p: the 9 local p from my own like-race pool (c15's MEDSL route, earlier years only), the 20 legislative
       runoffs by Klarner's runoff route (the class from my parse of the first round, the like races from c15's state
       pool), the rounds not computed by reason, and whether 2023's rows feed 2024's p (the record says they do not).
Needs the seven workbooks (m2lib.CACHE/la_sos/2023MMDD.xlsx) and the posted multi-parish files of each date
(la_sos/posted/2023MMDD-RacesCandidates_Multiparish.json and -Votes_Multiparish.json), fetched by curl 4 s apart.
[measured] throughout; the record's counts [stated].
"""
import collections
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402
import m2d3 as D  # noqa: E402
import c15_d3_refit as C15  # noqa: E402
import c18_louisiana as C18  # noqa: E402

DATES = ("2023-01-14", "2023-02-18", "2023-03-25", "2023-04-29", "2023-10-14", "2023-11-18", "2023-12-16")
PAIRS = {"2023-03-25": "2023-02-18", "2023-04-29": "2023-03-25", "2023-11-18": "2023-10-14"}   # a general -> its primary
AGAIN = {"2023-12-16": "2023-11-18"}   # a new election after an exact tie -> the general that tied
LEG = re.compile(r"^State (Representative|Senator) -- (\d+)(?:st|nd|rd|th) (?:Representative|Senatorial) District$")
ROOT = C18.ROOT
YEAR = 2023


def load_all():
    cs, bad = [], []
    for d in DATES:
        path = os.path.join(ROOT, d.replace("-", "") + ".xlsx")
        if not os.path.exists(path):
            print(f"  {d}: workbook not in {ROOT}; c22 cannot run")
            return None, None
        c, b = C18.parse(path, d)
        cs += c
        bad += b
    return cs, bad


def official():
    """{date: ResultsOfficial} from the site's list of elections (ElectionDates.json, fetched by curl for c18)."""
    d = L.load_json(os.path.join(ROOT, "ElectionDates.json"))
    out = {}
    for e in d["Dates"]["Date"]:
        m, dd, y = e["ElectionDate"].split("/")
        out[f"{y}-{m}-{dd}"] = e.get("ResultsOfficial")
    return out


def tkey(s):
    """A title's key: letters and digits (c18's _norm drops digits, which tells 'Proposition No. 1 of 6' from 'No. 2 of 6')."""
    return re.sub(r"[^a-z0-9]", "", str(s).lower())


def lone(x):
    return x if isinstance(x, list) else [x]


def posted(date):
    """The site's posted results of `date` for the contests on more than one parish's ballot:
    {normalized title: {"seats", "votes": {normalized choice: votes}}}; {} where the files hold no race; None if absent."""
    ymd = date.replace("-", "")
    paths = {w: os.path.join(ROOT, "posted", f"{ymd}-{w}_Multiparish.json") for w in ("RacesCandidates", "Votes")}
    if not all(os.path.exists(p) for p in paths.values()):
        return None
    with open(paths["RacesCandidates"], encoding="utf-8-sig") as f:
        rc = json.load(f)["Races"]
    with open(paths["Votes"], encoding="utf-8-sig") as f:
        vt = json.load(f)["Races"]
    if "Race" not in rc:
        return {}
    votes = {x["ID"]: {ch["ID"]: int(ch["VoteTotal"]) for ch in lone(x["Choice"])} for x in lone(vt["Race"])}
    out = {}
    for x in lone(rc["Race"]):
        v = votes.get(x["ID"], {})
        choices = {}
        for ch in lone(x["Choice"]):
            desc = " ".join(str(ch["Desc"]).split())
            pm = C18.PARTY.match(desc)
            choices[C18._norm(pm.group(1) if pm else desc)] = v.get(ch["ID"])
        out[tkey(C18.SEATS.sub("", " ".join(x["SpecificTitle"].split())))] = {"seats": int(x["NumberToBeElected"] or 1), "votes": choices}
    return out


def level_of(c):
    if c["question"]:
        return "question"
    m = LEG.match(c["base"])
    if m:
        return "state-lower" if m.group(1) == "Representative" else "state-upper"
    if c["base"] == "Governor":
        return "governor"
    return "local"


def rounds(cs):
    """{id(contest): (kind, the other round's date, that contest)}: deciding (its primary), first (its general or
    None), again (the general that tied), other date, general with no primary; question."""
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
        d = c["date"]
        earlier = PAIRS.get(d)
        later = next((g for g, p in PAIRS.items() if p == d), None)
        if earlier and earlier in on[k]:
            out[id(c)] = ("deciding", earlier, on[k][earlier])
        elif d in PAIRS.values():
            out[id(c)] = ("first", later if later in on[k] else None, on[k].get(later))
        elif d in AGAIN:
            out[id(c)] = ("again", AGAIN[d], on[k].get(AGAIN[d]))
        elif d in PAIRS:
            out[id(c)] = ("general, no primary", None, None)
        else:
            out[id(c)] = ("other date", None, None)
    return out


def gate(cs):
    print("22.1 The gate within the certifying source: official dates, lines that add up, the posted multi-parish results")
    rec = L.load_json(os.path.join(L.DATA, "local", "check-la.json"))["2023"]
    off = official()
    print(f"  the site's list: " + ", ".join(f"{d} {'official' if off.get(d) == '1' else off.get(d)}" for d in DATES)
          + f"; the record's 'official': {rec['official']}; equal {all((off.get(d) == '1') == rec['official'].get(d) for d in DATES)}")
    adds = sum(c["adds_up"] for c in cs)
    print(f"  contests parsed {len(cs):,} (by date " + ", ".join(f"{d} {sum(1 for c in cs if c['date'] == d)}" for d in DATES)
          + f"); lines add up to the total in {adds:,} (the record's 'parts add up' {rec['gate']['tallies'].get('parts add up')}); with a short line {sum(c['short_line'] for c in cs)}")
    # the workbooks' hashes against the record's sources note
    note = L.load_json(os.path.join(L.DATA, "local", "2023", "LA.json"))["sources"]["la_sos"]["note"]
    rec_sha = dict(re.findall(r"(\d{4}-\d{2}-\d{2}) \(Election\+Results\+\([\d-]+\)\.xlsx, sha256 ([0-9a-f]+)", note))
    same = 0
    for d in DATES:
        with open(os.path.join(ROOT, d.replace("-", "") + ".xlsx"), "rb") as f:
            h = hashlib.sha256(f.read()).hexdigest()
        same += h.startswith(rec_sha.get(d, "x"))
    print(f"  the seven workbooks' sha256 against the record's sources note: {same} of 7 begin with the recorded digits")
    t = collections.Counter()
    bad = []
    for d in DATES:
        multi = [c for c in cs if c["date"] == d and c["multi"]]
        post = posted(d)
        if post is None:
            print(f"  {d}: the posted files are not in {ROOT}/posted; not compared")
            continue
        if not multi:
            t[(d, f"no multi-parish contest in the workbook; the posted files hold {len(post)} race(s)")] += 1
            continue
        for c in multi:
            hit = post.get(tkey(c["base"]))
            mine = {C18._norm(x["name"]): x["votes"] for x in c["cands"]}
            if hit is None:
                t[(d, "not found in the posted results")] += 1
                bad.append((d, c["base"], "not found"))
            elif hit["votes"] == mine and hit["seats"] == c["seats"]:
                t[(d, "posted results equal")] += 1
            else:
                t[(d, "posted results differ")] += 1
                bad.append((d, c["base"], mine, hit))
        extra = len(post) - len(multi)
        if extra:
            t[(d, f"races in the posted files beyond the workbook's multi-parish contests: {extra}")] += 1
    rt = rec["gate"]["tallies"]
    print("  multi-parish contests against the posted results, by date: " + "; ".join(f"{k[0]} {k[1]} {v}" + (f" (record {rt.get(k[0] + ' multi-parish: ' + k[1])})" if "equal" in k[1] else "") for k, v in sorted(t.items())))
    eq = {k[0]: v for k, v in t.items() if k[1] == "posted results equal"}
    rec_eq = {k.split(" ")[0]: v for k, v in rt.items() if k.endswith("posted results equal")}
    print(f"  equal counts as the record's: {eq == rec_eq} (mine {sum(eq.values())}, record {sum(rec_eq.values())})")
    for b in bad[:6]:
        print(f"    {b}")


def rounds_check(cs):
    print("22.2 The rounds: the pairs of dates, the contests held again, the counts against check-la.json's 2023")
    rd = rounds(cs)
    t = collections.Counter()
    for c in cs:
        lv = level_of(c)
        if lv == "governor":
            t["left out: the governor (D2's level; data/governor/ holds even years only)"] += 1
        else:
            t[f"{c['date']} {lv}: {rd[id(c)][0]}"] += 1
    rec = L.load_json(os.path.join(L.DATA, "local", "check-la.json"))["2023"]["contests"]
    same = dict(t) == dict(rec)
    print(f"  my counts {'equal' if same else 'DIFFER FROM'} check-la.json's: " + "; ".join(f"{k} {v}" + ("" if rec.get(k) == v else f" (record {rec.get(k)})") for k, v in sorted(t.items()))
          + ("" if same else "; in the record only: " + str({k: v for k, v in rec.items() if k not in t})))
    paired = [(c, rd[id(c)][2]) for c in cs if rd[id(c)][0] == "deciding"]
    names_ok = sum(1 for c, p in paired if {x["name"] for x in c["cands"]} <= {x["name"] for x in p["cands"]})
    two = sum(1 for c, p in paired if len(c["cands"]) == 2 * c["seats"])
    print(f"  deciding rounds {len(paired)}: every candidate's name also on the primary's ballot in {names_ok}; exactly twice the seats on the ballot in {two}; the others: "
          + ("; ".join(f"'{c['base'][:40]}' {len(c['cands'])} for {c['seats']}" for c, p in paired if len(c["cands"]) != 2 * c["seats"]) or "none"))
    for c in cs:
        if rd[id(c)][0] == "deciding" and c["date"] == "2023-03-25":
            print(f"  2023-03-25 as a general: '{c['title']}' after 2023-02-18 ({len(c['cands'])} candidates: " + ", ".join(f"{x['name']} {x['votes']:,}" for x in c["cands"]) + ")")
    again = [(c, rd[id(c)][2]) for c in cs if rd[id(c)][0] == "again"]
    for c, g in again:
        gv = sorted((x["votes"] for x in g["cands"]), reverse=True) if g else None
        print(f"  held again on {c['date']}: {c['sheet']} '{c['base']}': the general of {AGAIN[c['date']]} " + (f"{gv} ({'an exact tie' if gv and gv[0] == gv[1] else 'NOT a tie'})" if g else "NOT FOUND")
              + f"; again " + ", ".join(f"{x['name']} {x['votes']:,}" for x in c["cands"]) + f"; the same names {g is not None and {x['name'] for x in c['cands']} == {x['name'] for x in g['cands']}}")
    rec_again = L.load_json(os.path.join(L.DATA, "local", "check-la.json"))["2023"].get("held_again")
    print(f"  the record's held_again: {rec_again}")
    ties = [c for c in cs if rd[id(c)][0] == "deciding" and len(c["cands"]) > c["seats"]
            and sorted((x["votes"] for x in c["cands"]), reverse=True)[c["seats"] - 1] == sorted((x["votes"] for x in c["cands"]), reverse=True)[c["seats"]]]
    print(f"  deciding rounds that ended in an exact tie at the last seat: {len(ties)}: " + "; ".join(f"{c['date']} {c['sheet']} '{c['base'][:40]}'" for c in ties))
    for c in cs:
        if rd[id(c)][0] == "general, no primary":
            print(f"  general without a primary: {c['date']} {c['sheet']} '{c['title']}'")
    first = [c for c in cs if rd[id(c)][0] == "first" and level_of(c) != "governor"]
    decided = [c for c in first if rd[id(c)][1] is None]
    under = [c for c in decided if c["seats"] == 1 and max(x["votes"] for x in c["cands"]) < 0.5 * sum(x["votes"] for x in c["cands"])]
    print(f"  first rounds {len(first)}: {len(decided)} with no later round (decided in the primary), {len(first) - len(decided)} followed by one; single-seat ones decided with the leader under 50%: {len(under)}"
          + ("; " + "; ".join(f"{c['date']} {c['sheet']} '{c['base'][:40]}'" for c in under[:5]) if under else ""))
    return rd


def files_check(cs, rd):
    print("22.3 The four files against my parse: data/{local,measure,state-lower,state-upper}/2023/LA.json")
    mine = collections.defaultdict(list)
    for c in cs:
        mine[c["date"]].append(c)
    files = {lv: L.load_json(os.path.join(L.DATA, lv, "2023", "LA.json"))["contests"] for lv in ("local", "measure", "state-lower", "state-upper")}
    sheet_fips = {c["sheet"]: C18.FIPS.get(C18._norm(c["sheet"])) for c in cs if not c["multi"]}
    t = collections.Counter()
    bad = []
    used = set()
    for lv, recs in files.items():
        for f in recs:
            q = lv == "measure"
            cands = [(C18._norm(x["name"]), x["votes"]) for x in f["result"]["candidates"]]
            hits = [c for c in mine[f["date"]] if c["question"] == q and sorted(x["votes"] for x in c["cands"]) == sorted(v for _, v in cands)
                    and {C18._norm(x["name"]) for x in c["cands"]} == {n for n, _ in cands}]
            if lv.startswith("state"):
                hits = [c for c in hits if level_of(c) == lv and LEG.match(c["base"]).group(2) == str(f["place"].get("district"))]
            if len(hits) != 1:
                t[f"{lv}: {len(hits)} parses with these candidates and votes"] += 1
                bad.append((f["id"], f"{len(hits)} parses"))
                continue
            c = hits[0]
            used.add(id(c))
            t[f"{lv}: matched"] += 1
            if not q and (f.get("seats") or 1) != c["seats"]:
                bad.append((f["id"], f"seats {f.get('seats')} vs {c['seats']}"))
                t["seats differ"] += 1
            if not q:
                r = rd[id(c)]
                el = f["election"] or ""
                core = el[len("special election: "):] if el.startswith("special election: ") else el
                ok = {"first": core.startswith("first round: Louisiana's primary") and ((f"followed on {r[1]}" in core) if r[1] else ("decided in it" in core)),
                      "deciding": core.startswith(f"deciding round after an earlier round on {r[1]}"),
                      "again": core.startswith(f"a new election of this contest, after its general election on {r[1]} ended in an exact tie"),
                      "other date": core.startswith("a date that is neither a primary nor a general"),
                      "general, no primary": False}[r[0]]
                if not ok:
                    bad.append((f["id"], f"election '{el[:70]}' vs my round {r[0]} {r[1]}"))
                    t["round words differ"] += 1
                if (c["date"] in ("2023-02-18",) or (c["date"] == "2023-03-25" and r[0] == "deciding")) != el.startswith("special election: "):
                    bad.append((f["id"], f"'special election' prefix: '{el[:50]}'"))
                    t["special prefix differs"] += 1
                order = sorted(c["cands"], key=lambda x: -x["votes"])
                k = c["seats"]
                if r[0] == "first" and r[2] is not None:
                    later = {x["name"] for x in r[2]["cands"]}
                    top = max((x["votes"] for x in order if x["name"] in later), default=0)
                    want_won = {C18._norm(x["name"]): ("to runoff" if x["name"] in later else True if x["votes"] > top else None) for x in order}
                else:
                    tie = len(order) > k and order[k - 1]["votes"] == order[k]["votes"]
                    winners = set() if tie else {x["name"] for x in order[:k]}
                    want_won = {C18._norm(x["name"]): (True if x["name"] in winners else None) for x in order}
                got = {C18._norm(x["name"]): x.get("won") for x in f["result"]["candidates"]}
                if got != want_won:
                    bad.append((f["id"], f"won marks {got} vs {want_won}"))
                    t["won marks differ"] += 1
                tie_here = len(order) > k and order[k - 1]["votes"] == order[k]["votes"] and r[0] == "deciding"
                has_note = any("exact tie" in n for n in (f.get("notes") or []))
                if tie_here != has_note:
                    bad.append((f["id"], f"tie note {has_note} vs a tie {tie_here}"))
                    t["tie notes differ"] += 1
                elif tie_here:
                    t["an exact tie, noted"] += 1
            if lv.startswith("state"):
                if f["place"].get("counties"):
                    t["legislature: counties named"] += 1
            else:
                fips = sorted({C18.FIPS.get(C18._norm(p)) for p in c["parishes"]} - {None}) if c["multi"] else [sheet_fips[c["sheet"]]]
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
                scope = "statewide" if (c["multi"] and len({C18.FIPS.get(C18._norm(p)) for p in c["parishes"]} - {None}) == 64) else "local"
                if f["question"].get("scope") != scope:
                    bad.append((f["id"], f"scope {f['question'].get('scope')} vs {scope}"))
                    t["scope differs"] += 1
    notin = [c for c in cs if id(c) not in used]
    print("  files: " + ", ".join(f"{lv} {len(recs)}" for lv, recs in files.items()) + "; " + "; ".join(f"{k} {v}" for k, v in sorted(t.items())))
    print(f"  my parse's contests not matched by any file contest: {len(notin)}: " + "; ".join(f"{c['date']} {c['sheet'][:14]} '{c['base'][:40]}' ({level_of(c)})" for c in notin[:6]))
    for rid, what in bad[:12]:
        print(f"    {rid[:80]}: {what}")
    pj = [f for f in files["local"] if "police juror" in f["office"].lower()]
    print(f"  local contests whose office names a police juror: {len(pj)}, office_type " + ", ".join(f"'{k}' {v}" for k, v in collections.Counter(f['office_type'] for f in pj).items())
          + " (the record's 'found, not yet changed': a police jury is a parish's governing body)")
    return files


def p_check(cs, rd, files):
    print("22.4 The 29 p from my own pools and my reading of the first rounds; the rounds not computed; 2023 in 2024's pool")
    medsl, nc, miss = C15.local_pools(odd_la=True)   # 2023's rows in: they are earlier years for no 2023 p, and #75 feeds them into 2024's
    by_key = collections.defaultdict(list)
    for y, k, s in medsl:
        by_key[k].append((y, s))
    la23 = [r for r in D.rows("local") if r["state"] == "LA" and r["year"] == YEAR]
    n_pool = sum(1 for y, _, _ in medsl if y == YEAR)
    print(f"  the local file's {len(la23)} contests: status " + ", ".join(f"{k} {v}" for k, v in collections.Counter(r['status'] for r in la23).items())
          + f"; routes of the computed: {dict(collections.Counter(r['route'] for r in la23 if r['status'] == 'value'))}; 2023 rows in my MEDSL-route pool {n_pool}")
    worst = 0.0
    eq = 0
    for r in la23:
        if r["status"] != "value":
            continue
        n = r["p"]["n"]
        if r["route"] in ("class", "boundary"):
            sh = [s for y, s in by_key.get(r["cls"], []) if y < r["year"]]
            f, N, h, k = D.class_density(sh)
            if f is None:
                print(f"    {r['id'][:70]}: my pool has {N} like races < 100; record N {r['N']}")
                continue
            pm, meth, fh = D.p_auto(n, 0.5, D.sd_eq(f))
            same = (N == r["N"], k == r["kin"], abs(h - D.window_h(r["win"])) < 1e-9, abs(round(k / N, 5) - r["q"]) < 1e-9)
            eq += all(same)
            worst = max(worst, D.rel(pm, r["p"]["value"]))
            print(f"    {r['id'][14:72]}: {r['route']}; (N, k, h, q) mine ({N}, {k}, {h}, {k / N:.5f}) record ({r['N']}, {r['kin']}, {D.window_h(r['win'])}, {r['q']}) {'equal' if all(same) else 'DIFFER'}; "
                  f"p mine {pm:.6g} ({meth}) record {r['p']['value']:.6g} ({r['p']['method']}); rel {D.rel(pm, r['p']['value']):.1e}")
        else:
            print(f"    {r['id'][14:72]}: route {r['route']} (not expected in 2023)")
    print(f"  local p: (N, k, h, q) equal in {eq} of {sum(1 for r in la23 if r['status'] == 'value')}; worst relative difference of p {worst:.1e}")
    reasons = collections.Counter(re.sub(r"\(\d+\)", "(n)", r["reason"] or "")[:95] for r in la23 if r["status"] != "value")
    print("  local, not computed, by reason: " + "; ".join(f"'{k}' {v}" for k, v in reasons.most_common()))
    dr = [r for r in la23 if r["status"] != "value" and (r["reason"] or "").startswith("a race between a Democrat and a Republican")]
    print(f"  Democrat-against-Republican deciding rounds not computed: {len(dr)} (the record: 17); among them " + ", ".join(sorted({r['office'][:28] for r in dr if r['office_scope'] != 'local'})))
    # 2024's p with and without 2023's rows
    la24 = [r for r in D.rows("local") if r["state"] == "LA" and r["year"] == 2024 and r["status"] == "value" and r["route"] in ("class", "boundary")]
    C15.compare_like(la24, medsl, "2024's Louisiana p, with 2023's rows in my pool (the record's rule since #75)")
    C15.compare_like(la24, C15.local_pools(odd_la=False)[0], "2024's Louisiana p, 2023's rows left out (the rule between #70 and #75: expected to differ now)")
    # the legislature
    pool, _, _ = C15.state_like_pool()
    bk = collections.defaultdict(list)
    for y, k, s in pool:
        bk[k].append((y, s))
    leg = {}
    for c in cs:
        m = LEG.match(c["base"])
        if m:
            leg[("state-lower" if m.group(1) == "Representative" else "state-upper", m.group(2), c["date"])] = c
    eq = tot = 0
    cls_same = 0
    worst = 0.0
    for lv in ("state-lower", "state-upper"):
        rows = [r for r in D.rows(lv) if r["state"] == "LA" and r["year"] == YEAR]
        print(f"  {lv}: {len(rows)} contests; status " + ", ".join(f"{k} {v}" for k, v in collections.Counter(r['status'] for r in rows).items())
              + "; not computed by reason: " + "; ".join(f"'{k}' {v}" for k, v in collections.Counter((r['reason'] or '')[:70] for r in rows if r['status'] != 'value').most_common()))
        for r in rows:
            if r["status"] != "value":
                continue
            tot += 1
            dist = r["id"].split("-")[4]
            c = leg.get((lv, dist, r["date"]))
            first = rd[id(c)][2] if c else None
            two = sorted(c["cands"], key=lambda x: -x["votes"])[:2] if c else []
            fv = {x["name"]: x["votes"] for x in first["cands"]} if first else {}
            got = [fv.get(x["name"]) for x in two]
            if len(two) == 2 and all(g is not None for g in got) and sum(got) > 0:
                s = max(got) / sum(got)
                my_cls = "runoff after an open or general first round, first-round leader of the two " + ("within 10 points" if s < 0.55 else "ahead by 10 points or more")
            else:
                my_cls = "runoff after an open or general first round, first round not found in the source"
            cls_same += my_cls == r["cls"]
            sh = [s_ for y, s_ in bk.get(r["cls"], []) if y < r["year"]]
            f, N, h, k = D.class_density(sh)
            if f is None:
                print(f"    {r['id']}: my state pool has {N} like races < 100; record N {r['N']}")
                continue
            pm, meth, fh = D.p_auto(r["p"]["n"], 0.5, D.sd_eq(f))
            same = (N == r["N"], k == r["kin"], abs(h - D.window_h(r["win"])) < 1e-9, abs(round(k / N, 5) - r["q"]) < 1e-9)
            eq += all(same)
            worst = max(worst, D.rel(pm, r["p"]["value"]))
            if not all(same) or my_cls != r["cls"] or tot <= 3:
                print(f"    {r['id']}: route {r['route']}; first-round leader's share of the two {s:.4f} -> my class '{my_cls[-32:]}' {'as' if my_cls == r['cls'] else 'NOT as'} the record's; "
                      f"(N, k, h, q) mine ({N}, {k}, {h}, {k / N:.5f}) record ({r['N']}, {r['kin']}, {D.window_h(r['win'])}, {r['q']}) {'equal' if all(same) else 'DIFFER'}; p mine {pm:.6g} record {r['p']['value']:.6g}; rel {D.rel(pm, r['p']['value']):.1e}")
    print(f"  legislative runoffs with p: {tot} (the record: 20); my class from the first round as the record's in {cls_same}; (N, k, h, q) equal in {eq}; worst relative difference of p {worst:.1e}")
    mea = [r for r in D.rows("measure") if r["state"] == "LA" and r["year"] == YEAR]
    print(f"  questions {len(mea)}: status " + ", ".join(f"{k} {v}" for k, v in collections.Counter(r['status'] for r in mea).items())
          + "; by reason: " + "; ".join(f"'{k}' {v}" for k, v in collections.Counter((r['reason'] or '')[:60] for r in mea).most_common()))
    pool_m = C15.measure_pool(odd_la=True)
    print(f"  Louisiana's 2023 questions in my measure pool: {sum(1 for y, k, s, rid in pool_m if '-LA-' in rid and y == YEAR)} (#75: 2023 feeds the later years)")
    ms = [r for r in D.rows("measure") if r["year"] == 2024 and r["route"] == "like past measures" and r["status"] == "value"]
    for label, pool_rows in (("with 2023's questions in my pool", pool_m), ("2023's questions left out (the rule between #70 and #75: expected to differ now)", C15.measure_pool(odd_la=False))):
        by_k = collections.defaultdict(list)
        for y, k, s, rid in pool_rows:
            by_k[k].append((y, s))
        tal = collections.Counter()
        for r in ms:
            sh = [s for y, s in by_k[r["cls"]] if y < r["year"]]
            f, N, h, k = D.density_at(sh, r["t"])
            tal["too few"] += f is None
            if f is not None:
                tal[(N == r["N"], k == r["kin"], abs(h - D.window_h(r["win"])) < 1e-9, abs(round(k / N, 5) - r["q"]) < 1e-9, D.rel(f, r["p"]["f_t"]) <= 1e-5)] += 1
        print(f"  2024's like-past-measures p ({len(ms)}, every state), {label}: (N, k, h, q, f_t) all equal in {tal[(True,) * 5]}; other outcomes {dict((str(k), v) for k, v in tal.items() if k != (True,) * 5)}"
              + f"; 2023 rows by class {dict(collections.Counter(k for y, k, s, rid in pool_rows if y == YEAR))}")


def main():
    print("C22. #70: LOUISIANA'S OWN 2023 RESULTS: THE GATE WITHIN THE SOURCE, THE ROUNDS, THE FOUR FILES AND THE 29 p")
    print(f"repository HEAD {L.git_head()}")
    cs, bad = load_all()
    if cs is None:
        return
    print(f"  parsed {len(cs):,} contests from the seven workbooks by c18's reader; blocks I could not read: {bad or 'none'}")
    gate(cs)
    rd = rounds_check(cs)
    files = files_check(cs, rd)
    p_check(cs, rd, files)


if __name__ == "__main__":
    main()
