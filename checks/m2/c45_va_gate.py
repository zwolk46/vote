#!/usr/bin/env python3
"""c45: Virginia 2023's local records read against the Department's own files, whole (the eighth pass's section 17; the
orchestrator, 2026-11-13 01:12 UTC: "Put Virginia's gate whole in section 17 … read the option keys of your four
write-in-over-ballot-name records … They are the test I set D3 under (d): a name-keyed option that beats a full ballot
means the write-in inference fails there. Say for each whether it holds").

The files [stated, D3's note of 01:10 UTC]: D3's copies of what it read on 2026-11-07 before the Department refused us
(18:27:48 UTC), placed in the project's shared folder /mnt/project-files/d3/va-2023/ and copied from there to
~/.cache/vote-m2/eighth/src/va-2023/ (outside the repository): export-2023-Nov-Gen.json (the page's 'Media Export',
sha256 95f9426e…) and 2023-Nov-Gen-page-rendered.html (the results page rendered in headless Chromium and scrolled to
its end, sha256 d311fa7b…), each with its .meta.json. Nothing is requested from Virginia's hosts (the orchestrator,
2026-11-07 18:30). The hashes are checked against D3's SHA256SUMS on each run.

The records: data/local/2023/VA.json and data/measure/2023/VA.json at 4831b16 (#101; d14645c, main's head after #104,
changes no data file, so the records are read from the 4831b16 worktree).

The gate as D3 built it (pipeline/local_va.py, docstring and code; the rules copied here, nothing imported):
  (a) the page headed "OFFICIAL RESULTS"; a contest the page shows: its candidates and votes the file's;
  (b) a shared contest's locality lines add up, option by option, to its statewide count, naming no option it lacks;
  (c) all reporting: the page's "Localities reporting n/n" for a shared contest; a one-locality contest's
      precinctsReporting equal to its precinctsParticipating and its locality's every group "Fully Reported";
  (d) the over-ballot test within the locality: a contest's votes for each seat (all its lines, write-ins too) against
      the highest-vote contest of the locality's whole ballot (_tops: each chamber's lines in the locality summed, and
      each other contest of one seat, or question, with the locality's most precincts); held over 1.10, listed over 1.0.
  Beside it: each option's precinct lines against its locality line.
  Options: "cs<n>" a name on the ballot; "wi-…" the write-in line; an id keyed by a name a write-in counted by name
  [D3's inference from two contests the page shows beside an "Adjudicated Write-Ins" line].

Sections:
  45.1  the files' hashes; the page: the heading, its 183 contests, each candidate's name, votes and Winner mark
        against the file's statewide list (gate (a))
  45.2  the 43 shared local contests: locality lines against the statewide count, option by option; the page's
        'Localities reporting' (gates (b) and (c)); the page's two 'Adjudicated Write-Ins' lines
  45.3  every record against the file: localities, office and district (D3's title rule copied), seats, every
        candidate's name and votes, the write-in flags by the option's key; the one-locality contests' reporting (c)
  45.4  the over-ballot test from the file (d): _tops per locality copied; every record's ratio and verdict against
        the record's gate; the three held and the 28 listed
  45.5  the option keys: the 65 records with a name-keyed option; the four where a named write-in outpolls a ballot
        name (Charlotte's Cullen/Red House supervisor, Clifton's mayor and council, Dillwyn's council): each option's
        key, and whether the inference holds there
  45.6  precinct lines against locality lines (17 noted)

Run:  python3 -I checks/m2/c45_va_gate.py [1 2 3 4 5 6]
"""
import collections
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402
import c43_district_checks as C43  # noqa: E402

RECORDS_AT = "4831b16"
SRC = os.path.join(L.CACHE, "eighth", "src", "va-2023")
EXPORT = os.path.join(SRC, "export-2023-Nov-Gen.json")
PAGE = os.path.join(SRC, "2023-Nov-Gen-page-rendered.html")
OVER_LINE = 1.10
BALLOT_ID = re.compile(r"cs\d+")
WRITE_IN_ID = re.compile(r"wi-")
SPECIAL = re.compile(r"\bSPECIAL\b", re.I)
LEG_TITLE = re.compile(r"Member, (Senate of Virginia|House of Delegates) \(")
at, records_at, h1 = C43.at, C43.records_at, C43.h1

_X = {}


def export():
    if "x" not in _X:
        with open(EXPORT) as f:
            _X["x"] = json.load(f)
    return _X["x"]


def _key(name):   # D3's _key, copied
    s = re.sub(r" COUNTY$", "", name.upper().replace("&", "AND"))
    return re.sub(r"[^A-Z]", "", s)


def _title(name, localities):   # D3's _title, copied
    t = " ".join(name.split()).strip()
    m = re.fullmatch(r"(.*?)\s*\(([^()]*)\)", t)
    if not m:
        return t.rstrip("."), ""
    office, inner = m.group(1).rstrip(" ."), m.group(2).strip()
    names = {_key(x) for x in inner.split(",")}
    return office, "" if names <= {_key(x) for x in localities} else inner


def option_kind(oid):   # D3's _option, copied
    return "ballot" if BALLOT_ID.fullmatch(oid) else "write-in line" if WRITE_IN_ID.match(oid) else \
        "write-in by name" if not oid.startswith("bms") else "question"


def local_contests():
    """The file's local contests (the legislature left out) in D3's shape: [(item id, title, office, district,
    localities [lid], shared, seats, question, special, options [(id, name, votes, kind)], parts [(lr, b)])]."""
    x = export()
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
        shared = iid in state_items
        lids = sorted(lr["id"] for lr, _ in parts)
        office, district = _title(b0["name"], [names[i] for i in lids])
        sb = state_items.get(iid)
        opts = [(o["id"], o["name"].strip(), o["voteCount"], option_kind(o["id"])) for o in (sb or b0)["ballotOptions"]]
        out.append({"item": iid, "title": " ".join(b0["name"].split()), "office": office, "district": district,
                    "localities": lids, "counties": sorted("51" + i for i in lids), "shared": shared,
                    "seats": b0["voteFor"], "question": b0["contestType"] == "BallotMeasure",
                    "special": bool(SPECIAL.search(b0["name"])), "options": opts, "parts": parts, "state_item": sb})
    return out


def page_contests():
    """The rendered page's 183 contests: [(title, vote-for text, [(name, votes, winner)], localities reporting)]."""
    with open(PAGE, encoding="utf-8", errors="replace") as f:
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
            opts.append((" ".join(nm.group(1).split()) if nm else None, int(vt.group(1).replace(",", "")) if vt else None,
                         ">Winner<" in blk))
        lr = re.search(r'Localities reporting</span><span class="fw-bold">\s*([\d]+/[\d]+)\s*<', art)
        out.append({"title": title, "vote_for": vf.group(1) if vf else None, "options": opts,
                    "localities_reporting": lr.group(1) if lr else None})
    return official, out


def va_records():
    rs = list(records_at(RECORDS_AT, "data/local/2023/VA.json").values())
    qs = list(records_at(RECORDS_AT, "data/measure/2023/VA.json").values())
    return rs, qs


def rec_key(r):
    office = r.get("office") or (r.get("question") or {}).get("title") or ""
    return (tuple(sorted(r["place"]["counties"])), str(office).upper(), (r["place"].get("district") or ""))


def file_index(cs):
    """key -> [contests]; a key the file repeats (Bedford's two special council contests of 2023) is told apart by the
    option names, in contest_of."""
    d = collections.defaultdict(list)
    for c in cs:
        d[file_key(c)].append(c)
    return d


def contest_of(r, index):
    cands = {x["name"].strip() for x in r["result"]["candidates"]}
    hits = index.get(rec_key(r), [])
    if len(hits) == 1:
        return hits[0]
    same = [c for c in hits if {n for _, n, _, _ in c["options"]} == cands]
    return same[0] if len(same) == 1 else None


def file_key(c):
    return (tuple(c["counties"]), c["office"].upper(), c["district"])


# ------------------------------------------------------------------------------------------ 45.1 the page

def section_1():
    h1("45.1 The files; the page against the file's statewide list (gate (a))")
    sums = {}
    with open(os.path.join(SRC, "SHA256SUMS")) as f:
        for line in f:
            if line.strip():
                hsh, name = line.split()
                sums[name.strip("*")] = hsh
    for name in ("export-2023-Nov-Gen.json", "2023-Nov-Gen-page-rendered.html"):
        with open(os.path.join(SRC, name), "rb") as f:
            got = hashlib.sha256(f.read()).hexdigest()
        meta = L.load_json(os.path.join(SRC, name + ".meta.json"))
        print(f"  {name}: sha256 {got[:16]}… equal to D3's SHA256SUMS: {sums.get(name) == got}; to its .meta.json: {meta.get('sha256') == got}; "
              f"url {meta.get('url')}; read {meta.get('read_utc')}; how: {meta.get('how', '')[:90]}")
    x = export()
    print(f"  the file: electionName {x['electionName']!r}, electionDate {x['electionDate']}, createdAt {x['createdAt']}; statewide contests {len(x['results']['ballotItems'])}; "
          f"localities {len(x['localResults'])}")
    official, pcs = page_contests()
    print(f"  the page: headed 'OFFICIAL RESULTS': {official}; contests parsed: {len(pcs)}; with a title {sum(1 for p in pcs if p['title'])}; "
          f"options parsed {sum(len(p['options']) for p in pcs)}; Winner marks {sum(1 for p in pcs for o in p['options'] if o[2])}")
    by_title = collections.defaultdict(list)
    for b in x["results"]["ballotItems"]:
        by_title[" ".join(b["name"].split())].append(b)
    matched = eq = neq = 0
    extra_page = extra_file = 0
    ex = []
    winners = collections.Counter()
    for p in pcs:
        items = by_title.get(p["title"])
        if not items or len(items) != 1:
            ex.append(("page title not once in the file", p["title"]))
            continue
        b = items[0]
        matched += 1
        fo = {o["name"].strip(): o["voteCount"] for o in b["ballotOptions"]}
        po = {n: v for n, v, _ in p["options"] if n}
        same = {n: v for n, v in po.items() if n in fo and fo[n] == v}
        if len(same) == len(fo) and len(same) == len(po):
            eq += 1
        else:
            neq += 1
            extra_page += len([n for n in po if n not in fo])
            extra_file += len([n for n in fo if n not in po])
            if len(ex) < 12:
                ex.append(("differ", p["title"], {n: v for n, v in po.items() if fo.get(n) != v}, {n: v for n, v in fo.items() if po.get(n) != v}))
        for n, v, w in p["options"]:
            if w:
                winners[("legislature" if b["name"].startswith("Member, ") else "local")] += 1
    print(f"  page contests matched to the file's by title: {matched} of {len(pcs)}; candidates and votes equal: {eq}; differing: {neq} "
          f"(page lines not in the file: {extra_page}; file lines not on the page: {extra_file})")
    for e in ex[:12]:
        print(f"    {e}")
    print(f"  Winner marks by kind: {dict(winners)}")


# ------------------------------------------------------------------------------------------ 45.2 the shared contests

def section_2():
    h1("45.2 The 43 shared local contests: locality lines against the statewide count; the page's 'Localities reporting'; the Adjudicated Write-Ins lines")
    cs = [c for c in local_contests() if c["shared"]]
    official, pcs = page_contests()
    page = {p["title"]: p for p in pcs}
    print(f"  shared local contests in the file: {len(cs)} (D3: 43)")
    add_ok = add_bad = rep_ok = rep_bad = extra = 0
    for c in cs:
        sb = c["state_item"]
        state = {o["id"]: o["voteCount"] for o in sb["ballotOptions"]}
        parts = collections.Counter()
        names = {}
        for lr, b in c["parts"]:
            for o in b["ballotOptions"]:
                parts[o["id"]] += o["voteCount"]
                names[o["id"]] = o["name"].strip()
        missing = [names[i] for i in parts if i not in state]
        if missing:
            extra += 1
        if all(parts.get(i, 0) == v for i, v in state.items()) and not missing:
            add_ok += 1
        else:
            add_bad += 1
            print(f"    lines do not add up: {c['title']}: statewide {[(names.get(i, i), v) for i, v in state.items()]}; localities' sums "
                  f"{[(names[i], v) for i, v in parts.items()]}")
        p = page.get(c["title"])
        rep = p["localities_reporting"] if p else None
        a, _, t = (rep or "/").partition("/")
        if a == t == str(len(c["localities"])):
            rep_ok += 1
        else:
            rep_bad += 1
            print(f"    reporting: {c['title']}: page {rep!r}, localities {len(c['localities'])}")
    print(f"  locality lines adding up to the statewide count, option by option, no option extra: {add_ok}; not: {add_bad} (contests with a locality option the statewide count lacks: {extra})")
    print(f"  the page's 'Localities reporting n/n' with n the file's localities: {rep_ok}; not: {rep_bad}")
    # the page's Adjudicated Write-Ins lines beside name-keyed options
    for p in pcs:
        adj = [(n, v) for n, v, _ in p["options"] if n == "Adjudicated Write-Ins"]
        if adj:
            c = next((c for c in cs if c["title"] == p["title"]), None)
            named = [(o[1], o[2], o[0]) for o in (c["options"] if c else []) if o[3] == "write-in by name"]
            print(f"  page: {p['title']}: 'Adjudicated Write-Ins' {adj}; the file's name-keyed options {named}; the page's lines {[(n, v) for n, v, _ in p['options']]}")


# ------------------------------------------------------------------------------------------ 45.3 every record

def section_3():
    h1(f"45.3 Every record at {RECORDS_AT} against the file: localities, office, district, seats, candidates, votes, write-in flags; reporting")
    rs, qs = va_records()
    cs = local_contests()
    index = file_index(cs)
    dup = sum(len(v) - 1 for v in index.values())
    for k, v in index.items():
        if len(v) > 1:
            print(f"    key repeated in the file: {k}: {[c['title'] for c in v]} (told apart by the option names)")
    print(f"  the file's local contests: {len(cs)} (offices {sum(1 for c in cs if not c['question'])}, questions {sum(1 for c in cs if c['question'])}); "
          f"keys (localities, office, district) repeated: {dup}; records: offices {len(rs)}, questions {len(qs)}")
    matched = unmatched = 0
    eq = collections.Counter()
    bad = []
    seen = set()
    for r in rs + qs:
        k = rec_key(r)
        c = contest_of(r, index)
        if c is None:
            unmatched += 1
            if unmatched <= 6:
                print(f"    record without a file contest of its key: {r['id']} {k}")
            continue
        matched += 1
        seen.add(c["item"])
        q = r.get("question", False) or "candidates" not in r["result"] or r["level"] == "measure"
        rc = {x["name"].strip().upper(): x for x in r["result"]["candidates"]}   # a question's YES/NO are the file's Yes/No, upper-cased by the build
        fo = {n.upper(): (v, kind) for _, n, v, kind in c["options"]}
        ok_names = set(rc) == set(fo)
        ok_votes = ok_names and all(rc[n]["votes"] == fo[n][0] for n in rc)
        ok_wi = ok_names and all((rc[n].get("party") == "write-in") == (fo[n][1] in ("write-in line", "write-in by name")) for n in rc)
        ok_seats = (r.get("seats", 1) == c["seats"]) if not q else True
        ok_total = r["result"]["total_votes"] == sum(v for _, _, v, _ in c["options"])
        ok_special = ("a special election" in ((r.get("p") or {}).get("not_computed") or "")) == c["special"] if not q else True   # the records carry the special in p's reason alone
        if not ok_special and len(bad) < 10:
            bad.append((r["id"], "special differs", c["title"], ((r.get("p") or {}).get("not_computed") or "")[:80]))
        eq["names"] += ok_names
        eq["votes"] += ok_votes
        eq["write-in flags by the option's key"] += ok_wi
        eq["seats"] += ok_seats
        eq["total_votes"] += ok_total
        eq["special"] += ok_special
        if not (ok_names and ok_votes and ok_wi and ok_seats and ok_total and ok_special):
            bad.append((r["id"], {"names": ok_names, "votes": ok_votes, "wi": ok_wi, "seats": ok_seats, "total": ok_total, "special": ok_special},
                        [(n, x["votes"], x.get("party")) for n, x in rc.items()][:4], c["options"][:4]))
    print(f"  records matched to a file contest by key: {matched} of {len(rs) + len(qs)}; unmatched: {unmatched}; file contests no record claims: {len(cs) - len(seen)}")
    print(f"  equal in: {dict(eq)}")
    for b in bad[:10]:
        print(f"    {b}")
    # (c) one-locality contests all reporting
    x = export()
    full = {lr["id"]: all(s["status"] == "Fully Reported" for s in lr["reportingStatuses"]) for lr in x["localResults"]}
    one = [c for c in cs if not c["shared"]]
    rep = sum(1 for c in one for lr, b in c["parts"] if b["precinctsReporting"] == b["precinctsParticipating"] and full[lr["id"]])
    print(f"  one-locality contests: {len(one)}; precincts all reporting and the locality's groups all 'Fully Reported': {rep}; "
          f"localities with every group 'Fully Reported': {sum(full.values())} of {len(full)}")
    # the record's gate fields
    g = collections.Counter()
    for r in rs + qs:
        gt = r.get("gate") or {}
        g[(gt.get("shared"), gt.get("all_reporting"), gt.get("page_equal"), gt.get("parts_add_up"), gt.get("precincts_add_up"))] += 1
    print(f"  the records' gate fields (shared, all_reporting, page_equal, parts_add_up, precincts_add_up): {dict(g)}")


# ------------------------------------------------------------------------------------------ 45.4 the over-ballot test

def _tops(lr):   # D3's _tops, copied
    n = max(b["precinctsParticipating"] or 0 for b in lr["ballotItems"])
    out, cham = [], collections.Counter()
    for b in lr["ballotItems"]:
        v = sum(o["voteCount"] for o in b["ballotOptions"])
        m = LEG_TITLE.match(b["name"])
        if m:
            cham[m.group(1)] += v
        elif (b["voteFor"] == 1 or b["contestType"] == "BallotMeasure") and b["precinctsParticipating"] == n:
            out.append((v, " ".join(b["name"].split()), b["id"]))
    out += [(v, f"{ch}'s lines in {lr['name'].title()}, summed", None) for ch, v in cham.items()]
    return out


def section_4():
    h1("45.4 The over-ballot test within the locality, from the file (gate (d)), against every record's gate")
    rs, qs = va_records()
    cs = local_contests()
    x = export()
    tops = {lr["id"]: _tops(lr) for lr in x["localResults"]}
    index = file_index(cs)
    same_r = diff_r = same_v = diff_v = 0
    worst = []
    held, listed = [], []
    for r in rs + qs:
        c = contest_of(r, index)
        if c is None:
            continue
        over = []
        for lr, b in c["parts"]:
            v = sum(o["voteCount"] for o in b["ballotOptions"])
            mine = v / (b["voteFor"] or 1) if not c["question"] else v
            others = [t for t in tops[lr["id"]] if t[2] != c["item"]]
            top, name, _ = max(others) if others else (None, None, None)
            over.append((mine / top if top else None, lr["name"].title(), name, top, mine))
        w = max((o for o in over if o[0] is not None), key=lambda o: o[0], default=None)
        verdict = "untested" if w is None else "held" if w[0] > OVER_LINE else "listed" if w[0] > 1 else "passes"
        g = r.get("gate") or {}
        if w is not None and g.get("over_ballot_ratio") is not None and abs(round(w[0], 4) - g["over_ballot_ratio"]) <= 1e-4:
            same_r += 1
        else:
            diff_r += 1
            worst.append((r["id"], None if w is None else round(w[0], 4), g.get("over_ballot_ratio")))
        if verdict == g.get("over_ballot"):
            same_v += 1
        else:
            diff_v += 1
        if verdict == "held":
            held.append((c["title"], round(w[0], 4), w[1], w[2], w[3]))
        if verdict == "listed":
            listed.append((c["title"], round(w[0], 4), w[2]))
    print(f"  records with a file contest: {same_r + diff_r}; ratio equal to the record's (4 decimals): {same_r}; differing: {diff_r} {worst[:6]}")
    print(f"  verdict equal to the record's: {same_v}; differing: {diff_v}")
    print(f"  held by (d), mine: {len(held)}: " + "; ".join(f"{t} {r} in {l} against {n} {v:,}" for t, r, l, n, v in held))
    print(f"  listed, mine: {len(listed)} (D3: 28): " + "; ".join(f"{t} {r}" for t, r, _ in sorted(listed, key=lambda z: -z[1])[:10]) + " …")
    # the comparators of the held: unopposed?
    for t, r, l, n, v in held:
        comp = next((c for c in cs if c["title"] == n), None)
        if comp:
            print(f"    comparator {n}: options {[(o[1], o[2], o[3]) for o in comp['options']]}; ballot names {sum(1 for o in comp['options'] if o[3] == 'ballot')} for {comp['seats']} seat(s)")
        else:
            print(f"    comparator {n}: a chamber's lines summed (no single contest)")


# ------------------------------------------------------------------------------------------ 45.5 the option keys

FOUR = ["2023-local-VA-MEMBER_BOARD_OF_SUPERVISORS-Cullen_red_House_District_county_51037",
        "2023-local-VA-MAYOR-Town_of_Clifton_county_51059",
        "2023-local-VA-MEMBER_TOWN_COUNCIL-Town_of_Clifton_county_51059",
        "2023-local-VA-MEMBER_TOWN_COUNCIL-Dillwyn_county_51029"]


def section_5():
    h1("45.5 The option keys: the name-keyed options, and the four records where a named write-in outpolls a ballot name")
    rs, qs = va_records()
    cs = local_contests()
    index = file_index(cs)
    kinds = collections.Counter(o[3] for c in cs for o in c["options"])
    print(f"  option kinds in the file's local contests: {dict(kinds)}; contests with a name-keyed option: {sum(1 for c in cs if any(o[3] == 'write-in by name' for o in c['options']))} (D3: 65)")
    # every name-keyed option's id looks like a name
    nk = [(c["title"], o[0], o[1], o[2]) for c in cs for o in c["options"] if o[3] == "write-in by name"]
    print(f"  name-keyed options: {len(nk)}; ids e.g. {[o[1] for o in nk[:6]]}")
    # in the name-keyed contests: the 'wi-' line beside; the named ahead of a ballot name
    for i in FOUR:
        r = next((r for r in rs if r["id"] == i), None)
        c = contest_of(r, index) if r else None
        if not c:
            print(f"  {i}: no file contest"); continue
        b = c["parts"][0][1]
        opts = [(o["id"], o["name"].strip(), o["voteCount"], option_kind(o["id"]), o.get("politicalParty"), o.get("ballotOrder")) for o in b["ballotOptions"]]
        ballot = [o for o in opts if o[3] == "ballot"]
        named = [o for o in opts if o[3] == "write-in by name"]
        full = c["seats"] <= len(ballot)
        beats = [o for o in named if ballot and o[2] > min(x[2] for x in ballot)]
        print(f"  {i}: seats {c['seats']}, precincts {b['precinctsParticipating']}; options (id, name, votes, kind, party, ballotOrder): {opts}")
        print(f"    a 'wi-' write-in line in the contest: {any(o[3] == 'write-in line' for o in opts)} {[(o[1], o[2]) for o in opts if o[3] == 'write-in line']}; "
              f"ballot ids: {[o[0] for o in ballot]}")
        print(f"    ballot names {len(ballot)} for {c['seats']} seat(s) (a full ballot: {full}); name-keyed options beating a ballot name: "
              f"{[(o[1], o[2]) for o in beats]}; the inference (a name-keyed option is a write-in) {'FAILS the test here' if full and beats else 'holds (no full ballot beaten)' if not beats else 'holds (the ballot is not full)'}")
        # precinct lines of the named option: spread or one precinct?
        for o in b["ballotOptions"]:
            if option_kind(o["id"]) == "write-in by name":
                pr = [(p["name"], p["voteCount"]) for p in (o["precinctResults"] or []) if p["voteCount"]]
                print(f"    {o['name'].strip()}: precinct lines with votes {len(pr)} of {len(o['precinctResults'] or [])}: {pr[:6]}")


# ------------------------------------------------------------------------------------------ 45.6 precinct lines

def section_6():
    h1("45.6 Each option's precinct lines against its locality line (recorded beside the gate)")
    cs = local_contests()
    rs, qs = va_records()
    short = []
    for c in cs:
        for lr, b in c["parts"]:
            for o in b["ballotOptions"]:
                if o["precinctResults"] is None:
                    continue
                s = sum(p["voteCount"] for p in o["precinctResults"])
                if s != o["voteCount"]:
                    short.append((c["title"], lr["name"].title(), o["name"].strip(), o["voteCount"], s))
    by_c = collections.Counter((t, l) for t, l, _, _, _ in short)
    print(f"  option lines whose precinct lines do not add up: {len(short)} in {len({t for t, _, _, _, _ in short})} contests (D3: 17 contests); by locality: "
          f"{dict(collections.Counter(l for (t, l) in by_c))}")
    for s in short[:6]:
        print(f"    {s}")
    noted = sum(1 for r in rs + qs if "precinct lines do not add up" in json.dumps(r.get("notes", [])))
    print(f"  records carrying the note: {noted}")


def main():
    which = [int(a) for a in sys.argv[1:]] or [1, 2, 3, 4, 5, 6]
    print(f"C45 Virginia 2023's gate whole from the Department's files (D3's copies in {SRC}); records at {RECORDS_AT}")
    for n in which:
        globals()[f"section_{n}"]()
    print("\n### done c45")


if __name__ == "__main__":
    main()
