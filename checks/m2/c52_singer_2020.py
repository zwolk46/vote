"""checks/m2/c52_singer_2020.py: M2's eighth pass, section 22: D3's #118 (4debd7e5), Singer's 2020 official results as
2020's second count of the state legislatures (data/local/REPORT.md section 39; pipeline/local_singer.py; pipeline/local.py
singer_checks; data/local/check-2020-singer.json; data/local/moves-39.json).

The orchestrator's brief (2026-11-13 11:05 UTC, verbatim): "D3's Singer 2020 PR #118 is merged as 4debd7e. Please check it
in §22, ending at 4debd7e. It covers the following, all in REPORT §39 and pipeline/local_singer.py: Singer's RV80FW intake:
CC0, 56 files against the record's md5. The gate against D1/D2's 2020 by candidate at 0.5%: 46 pass; KS, MO, OH, UT and WY
fail and are untested, not held; Maine passes with its UOCAVA lines. The district checks of 3,880 Klarner 2020 contests
(136 unmatched). The 25 flags. MT House 3, 19 and 84 take Singer's count, which Montana's canvass agrees with (sha256
3e6f8ba1…). Held: ME 15, NY House 3 and 5. Noted: ME House 144, Senate 17, NY House 1, AZ House 12, Senate 16. Maine's rows
being counties only, so 22:26 (b) does not apply. The moves: 7,546 moved, 17 lost, 0 gained; my compare agrees. Your two
readings: FairVote's text hash, and §38's 48 and 31. The rulings: §32's rules act on Singer's count as on MEDSL's, and an
inferred error settles nothing."

Nothing from pipeline/ is imported; a rule of D3's that must be applied is copied here and says so. BEFORE is main after
#117 (30480c35, whose D3 records are those of f6434077), AFTER is 4debd7e5; both read from worktrees.
  52.1  The sources, read apart (fetch_eighth_pass.sh singer_record, singer_files, mt_sos; one request each): the dataset's
        record (CC0, no guestbook, no access request, 56 files), every file's md5 against the record, the files read by
        D3's counting rule copied (each line's 'total' vote type; a contest's votes are its deepest reporting units', plus
        the jurisdiction's own line where it is not their sum; non-votes out) against D3's normalize_checks.
  52.2  Gate 1: each jurisdiction's Democrat and Republican for president, US Senate and each US House district against
        D1's and D2's certified 2020 counts (the rule copied), line by line against D3's gate.
  52.3  Gate 2: section 32's district checks (local_districts' match, pair and test copied, on Singer's legislative
        contests of the states that pass) on every Klarner 2020 general record at BEFORE: the untested, the unmatched, the
        shared, the tested, and the 25 flags with their outcomes by the rules copied.
  52.4  Montana's canvass (sha256; my own reading of its 125 districts) against Singer's and Klarner's, House 3, 19 and 84
        and every other district; Maine's legislative rows by reporting unit.
  52.5  The records at AFTER: every flag's outcome as built (the notes' words by D3's formats copied; p by the density
        formula from the record's own forecast); the moves file against my own diff of every D3 record.
  52.6  My two readings taken: FairVote's text sha256 from my own copy of the page; the recount listing at AFTER against
        my scan (c51's rules).
Run: python3 -I checks/m2/c52_singer_2020.py [1 2 3 4 5 6]
"""
import collections
import csv
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
import c40_pr_checks as C40  # noqa: E402
import c43_district_checks as C43  # noqa: E402
import c46_district_checks_2 as C46  # noqa: E402
import c49_va_local_2 as C49  # noqa: E402
import c51_recount_zone as C51  # noqa: E402

BEFORE, AFTER = "30480c35", "4debd7e5"
SRC = os.path.expanduser("~/.cache/vote-m2/eighth/src")
SINGER = os.path.join(SRC, "singer")
UNZ = os.path.join(SINGER, "unzipped")
MT_PDF = os.path.join(SRC, "mt_sos", "State_Canvass_Legislative.pdf")
MT_SHA = "3e6f8ba183389121a1c7e3a118b5b01869d9f0e30145ad8724ceabfd22c1947a"   # the note's, the orchestrator's 3e6f8ba1…
DERIVED = os.path.join(L.CACHE, "eighth", "derived")
NORM = os.path.join(DERIVED, "singer-2020.json")
YEAR = 2020
# D3's constants, copied (pipeline/local_singer.py, pipeline/local_districts.py)
GATE_LINE = 0.005
RATIO_OFF, HOLD_GAP, DOUBLE_TOL = 0.03, 0.05, 0.02
NOT_VOTES = re.compile(r"^(OVER ?VOTES?|UNDER ?VOTES?(\.\d+)?|TOTAL VOTES CAST|NONE OF THESE CANDIDATES|BLANKS?|VOIDS?)$", re.I)
WRITE_IN_TOTAL = re.compile(r"^(WRITE[- ]?INS?( \(MISCELLANEOUS\))?|OTHER WRITE-INS|SCATTER(ING)?|ALL OTHERS|MISC\.?)$", re.I)
WRITE_IN = re.compile(r"\(WRITE[- ]?IN\)|\(WRITE IN\)|^WRITE-IN - ", re.I)
WRITE_IN_MARK = re.compile(r"\(W/I\)|\bWRITE[- ]?IN\b", re.I)
LD_NOT_VOTES = re.compile(r"OVER ?VOTES?|UNDER ?VOTES?|\bBLANKS?\b|\bVOIDS?\b|\bTOTALS?\b|FEDERAL BALLOTS", re.I)
LEG = re.compile(r"^([A-Z]{2}) (House|Senate) District (.+?)(?: Position (\d+))?$")
SUFFIX = re.compile(r",\s*(JR|SR|II|III|IV|V)\.?$", re.I)
DEM = re.compile(r"^DEMOCRATIC( PARTY)?$|^DEMOCRATIC-FARMER-LABOR( PARTY)?$|^DEM$", re.I)
REP = re.compile(r"^REPUBLICAN( PARTY)?$|^REP$", re.I)
# pipeline/local.py's note formats, copied, so that each record's note can be rebuilt from the check file and compared
S_SRC = ("Singer's 2020 official results ({file} of Harvard Dataverse doi:10.7910/DVN/RV80FW, CC0 1.0, a third party's "
         "compilation of the states' files)")
S_RULE = ("the orchestrator, 2026-11-13 10:44: \"§32's rules act on Singer's count exactly as on MEDSL's\"; 2026-11-07 "
          "21:26: \"a gap of 5% or more is held, and a gap under 5% is kept with a note\"")
S_RATIO = ("{src} give this district's {n} named candidate{s} {m:,} votes against Klarner's {k:,}, {pct:+.1f}% ({diff}) "
           "[measured: pipeline/local_singer.py, data/local/check-2020-singer.json], and no state count is read; which "
           "count errs is [inferred]: {why} (the orchestrator, 2026-11-13 10:44: \"an inference settles nothing\")")
S_HELD = "{what}; so neither count is relied on ({rule}): p is not computed, and the contest is left out of the fits"
S_NOTED = "{what}; under 5%, so Klarner's count is kept ({rule})"
S_AGREE_SINGER = ("{src} give this district's {n} named candidate{s} {m:,} votes against Klarner's {k:,}, {pct:+.1f}% "
                  "[measured: pipeline/local_singer.py]; the state's canvass agrees with Singer's, candidate by "
                  "candidate, and not with Klarner's ({ssrc}, {url}, read {read}, sha256 {sha}: {pairs}), so Singer's "
                  "count stands (the orchestrator, 2026-11-13 10:44: \"If it agrees with Singer on House 3, 19 and 84, "
                  "they take that count with Klarner's figures in a note, as Indiana Senate 36 took MEDSL's\"): {diff}")
FAIRVOTE = os.path.join(SRC, "recount", "fairvote-election-recounts-2024.html")
# pipeline/local.py's HELD_ONE_NAME, copied (the orchestrator, 2026-11-13 00:26: a one-name record whose counts are held is not
# computed, with the reason that the write-in test cannot be read on held counts); the build appends it to a held reason
HELD_ONE_NAME = ("one name on the ballot for each seat, but the write-in test (whether write-ins drew 10% of the last winner's "
                 "votes) cannot be read on held counts, so p 0 is not given")


def h1(s):
    print("\n" + "=" * 100 + f"\n{s}\n" + "=" * 100)


def at(commit, rel):
    return C49.at(commit, rel)


def records_at(commit, f):
    return C49.records_at(commit, f)


def pval(c):
    return C49.pval(c)


def index_lines(prefix):
    out = []
    with open(os.path.join(SRC, "index.txt")) as f:
        for line in f:
            if line.startswith(prefix):
                out.append(line.rstrip("\n").split("\t"))
    return out


# ------------------------------------------------------------------------------------------ 52.1 the sources, the files

def record():
    with open(os.path.join(SINGER, "RV80FW-dataset.json")) as f:
        return json.load(f)["data"]


def normalize():
    """D3's normalize, copied (its counting rule) on my own copy of the 56 files, with my own counts beside: every file's
    md5 against the record first."""
    rec = record()["latestVersion"]
    want = {f["dataFile"]["originalFileName"]: f["dataFile"]["md5"] for f in rec["files"]}
    csv.field_size_limit(10 ** 8)
    out = {}
    checks = {"files": {}, "both_levels": [], "rolled_up": {}, "preliminary_rows": collections.Counter(), "md5_equal": 0,
              "vote_types": collections.Counter(), "me_leg_units": collections.Counter(), "rows": 0, "bytes": 0}
    for name, md5 in sorted(want.items()):
        path = os.path.join(UNZ, name)
        with open(path, "rb") as f:
            raw = f.read()
        ok = hashlib.md5(raw).hexdigest() == md5
        checks["md5_equal"] += ok
        checks["bytes"] += len(raw)
        st = name[:2]
        lines = collections.defaultdict(lambda: collections.defaultdict(int))
        depth = collections.defaultdict(set)
        rows = 0
        with open(path, encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                rows += 1
                checks["vote_types"][row["VoteType"]] += 1
                if row["VoteType"] != "total":
                    continue
                if row["Preliminary"] == "True":
                    checks["preliminary_rows"][f"{st} {row['Contest']}"] += 1
                unit = row["ReportingUnit"]
                lines[(row["Contest"], row["Selection"].strip(), row["Party"].strip())][unit] += int(row["Count"])
                depth[row["Contest"]].add(unit.count(";"))
                if st == "ME" and LEG.match(row["Contest"]):
                    checks["me_leg_units"][unit] += 1
        contests = collections.defaultdict(list)
        for (contest, sel, party), units in lines.items():
            deep = max(depth[contest])
            v = sum(n for u, n in units.items() if u.count(";") == deep)
            top = sum(n for u, n in units.items() if u.count(";") < deep)
            if top and top != v:   # the jurisdiction's own line, not the sum of its units: added (D3's rule)
                checks["both_levels"].append([st, contest, sel, top, v])
                v += top
            elif top:
                checks["rolled_up"][st] = checks["rolled_up"].get(st, 0) + 1
            contests[contest].append({"name": sel, "party": party, "votes": v,
                                      "units": len([u for u in units if u.count(";") == deep])})
        out[st] = dict(sorted(contests.items()))
        checks["files"][name] = {"rows": rows, "contests": len(contests), "md5": md5, "md5_equal": ok}
        checks["rows"] += rows
    checks["preliminary_rows"] = dict(sorted(checks["preliminary_rows"].items()))
    checks["vote_types"] = dict(checks["vote_types"])
    checks["me_leg_units"] = dict(checks["me_leg_units"])
    os.makedirs(DERIVED, exist_ok=True)
    with open(NORM, "w") as f:
        json.dump({"contests": out, "checks": checks}, f)
    return {"contests": out, "checks": checks}


def load_singer():
    if os.path.exists(NORM):
        with open(NORM) as f:
            return json.load(f)
    return normalize()


def section_1():
    h1("52.1 Singer's dataset, read apart: the record, the 56 files against its md5s, the files as read (D3's counting rule copied) against D3's normalize_checks")
    d = record()
    v = d["latestVersion"]
    fields = {x["typeName"]: x["value"] for x in v["metadataBlocks"]["citation"]["fields"]}
    idx = {r[0]: r for r in index_lines("singer:") + index_lines("mt:")}
    print(f"  the record [measured: {idx['singer:record'][3]}, {idx['singer:record'][2]} UTC, HTTP {idx['singer:record'][1]}, {idx['singer:record'][6]} bytes]: "
          f"'{fields.get('title')}', {[a.get('authorName', {}).get('value') for a in fields.get('author', [])]} ({[a.get('authorAffiliation', {}).get('value') for a in fields.get('author', [])]}); "
          f"version {v.get('versionNumber')}.{v.get('versionMinorNumber')} {v.get('versionState')}, released {v.get('releaseTime')}; licence {v.get('license', {}).get('name')} ({v.get('license', {}).get('uri')}); "
          f"termsOfUse {v.get('termsOfUse')}; guestbook keys {[k for k in v if 'guest' in k.lower()]}; fileAccessRequest {v.get('fileAccessRequest')}; files {len(v['files'])}, any restricted {any(f.get('restricted') for f in v['files'])}; "
          f"the record's filesize sum {sum(f['dataFile']['filesize'] for f in v['files']):,} (Dataverse's ingested tabular sizes [inferred]); persistent {d.get('persistentUrl')}")
    desc = " ".join(x.get("dsDescriptionValue", {}).get("value", "") for x in fields.get("dsDescription", []))
    for q in ("Official 2020 General Election results for all 56 major US jurisdictions", "by county (or other major subdivision)",
              "including all federal contests and most statewide and state legislative contests",
              "comes from, or is rolled up to the county level from, files or web pages published by the State, District or Territory Boards of Election"):
        print(f"    description holds {q!r}: {q in desc}")
    print(f"  the files [measured: {idx['singer:original'][3]}, {idx['singer:original'][2]} UTC, HTTP {idx['singer:original'][1]}, {idx['singer:original'][6]} bytes, sha256 {idx['singer:original'][5][:16]}…]: "
          f"D3's zip 1,532,255 bytes, sha256 e0f1dc5c…: the bytes equal, the sha256 {'equal' if idx['singer:original'][5].startswith('e0f1dc5c') else 'differs (Dataverse builds the zip at each request [inferred]; the files within are what the record names, by md5)'}")
    d_ = normalize()
    ck = d_["checks"]
    print(f"  unzipped: {len(ck['files'])} files, {ck['bytes']:,} bytes (D3: 23,671,970), md5 equal to the record's: {ck['md5_equal']} of {len(ck['files'])}; rows {ck['rows']:,}; vote types {ck['vote_types']}")
    chk = L.load_json(at(AFTER, "data/local/check-2020-singer.json"))
    nc = chk["normalize_checks"]
    bl = ck["both_levels"]
    print(f"  lines where the jurisdiction's own line is not its units' sum (added): mine {len(bl)} (D3: {len(nc['both_levels'])}; equal as lists: {bl == nc['both_levels']}); by jurisdiction {dict(collections.Counter(x[0] for x in bl))}; "
          f"the own lines' votes {sum(x[3] for x in bl):,} against the units' {sum(x[4] for x in bl):,}")
    print(f"  roll-ups equal to their units' sum (not added): mine {ck['rolled_up']} (D3: {nc['rolled_up']}); preliminary rows: mine {sum(ck['preliminary_rows'].values())} in {len(ck['preliminary_rows'])} contests, "
          f"equal to D3's: {ck['preliminary_rows'] == nc['preliminary_rows']} {ck['preliminary_rows']}")
    print(f"  contests by jurisdiction: {sum(len(c) for c in d_['contests'].values()):,} in {len(d_['contests'])} files; legislative contests {sum(1 for st, cs in d_['contests'].items() for k in cs if LEG.match(k) and LEG.match(k).group(1) == st):,}")
    print(f"  the check file's source: read_utc {chk['source']['read_utc']}, record_read_utc {chk['source']['record_read_utc']}, licence {chk['source']['licence']}, mark {chk['source']['mark']}; rules {chk['rules']} (copied here: {GATE_LINE}, {RATIO_OFF}, {HOLD_GAP}, {DOUBLE_TOL})")
    mt = idx.get("mt:canvass2020")
    sha = C49.sha256(MT_PDF)
    pages = subprocess.run(["pdfinfo", MT_PDF], capture_output=True, text=True).stdout
    pg = re.search(r"Pages:\s+(\d+)", pages)
    print(f"  Montana's canvass [measured: {mt[3]}, {mt[2]} UTC, HTTP {mt[1]}, {mt[6]} bytes]: sha256 {sha[:8]}…{sha[-8:]} = the note's {MT_SHA[:8]}…{MT_SHA[-8:]}: {sha == MT_SHA}; {pg.group(1) if pg else '?'} pages (D3: 24, 129,117 bytes)")


# ------------------------------------------------------------------------------------------ 52.2 gate 1

def major(party):   # pipeline/local_in._major, copied
    p = (party or "").upper()
    return "D" if p in ("D", "DEM", "DEMOCRAT", "DEMOCRATIC") else "R" if p in ("R", "REP", "REPUBLICAN") else None


def person_name(st, name, leg=True):   # D3's person_name, copied
    n = SUFFIX.sub(lambda m: " " + m.group(1), name.strip())
    if leg and st == "AK" and "," not in n and not WRITE_IN_TOTAL.match(n) and not NOT_VOTES.match(n):
        t = n.split()
        n = " ".join(t[1:] + t[:1])
    return n


def surnames(st, name, leg=True):
    return {k[0] for k in C46.name_keys(person_name(st, name, leg))}


def side(party):
    p = (party or "").strip()
    return "D" if DEM.match(p) else "R" if REP.match(p) else None


def person(x):
    return not NOT_VOTES.match(x["name"]) and not WRITE_IN_TOTAL.match(x["name"])


def cert_side(cands):   # D3's _cert_side, copied
    out = {}
    for s in ("D", "R"):
        v = [x for x in cands if major((x.get("party") or "").split("/")[-1]) == s or major(x.get("party")) == s]
        if len(v) == 1:
            out[s] = (C46.name_key(v[0]["name"])[0], v[0]["votes"])
    return out


def by_name(st, cands, surname, s):   # D3's _by_name, copied
    names = {x["name"] for x in cands if person(x) and (surname in surnames(st, x["name"], False) or surname in surnames(st, x["name"], True))}
    if len(names) == 1:
        return sum(x["votes"] for x in cands if x["name"] in names), "by name"
    names = {x["name"] for x in cands if person(x) and side(x["party"]) == s}
    if len(names) == 1:
        return sum(x["votes"] for x in cands if x["name"] in names), f"by party line ({sorted(names)[0]})"
    return None, f"no one name {surname} in Singer's, nor one {s} line"


def gate(data):   # D3's gate, copied
    cert = {}
    for level in ("president", "senate", "house"):
        cert[level] = [c for c in L.load_json(at(AFTER, f"data/{level}/{YEAR}.json"))["contests"] if not c.get("special")]
    out = {}
    for st, contests in sorted(data["contests"].items()):
        lines, worst = [], 0.0
        for level in ("president", "senate", "house"):
            for c in cert[level]:
                if c["place"]["state"] != st or (level == "president" and c["place"].get("district")):
                    continue
                if level == "president":
                    name = [k for k in contests if re.match(r"^US President", k)]
                elif level == "senate":
                    name = [k for k in contests if re.match(rf"^US Senate {st}$", k)]
                else:
                    d = c["place"]["district"]
                    dn = "1" if d in ("AL", "0", None) else str(int(d))
                    name = [k for k in contests if re.match(rf"^US House {st} District {dn}$", k)] or \
                           ([k for k in contests if re.match(rf"^US House {st}( At-Large| District AL)?$", k)] if d in ("AL", "0", None) else [])
                if len(name) != 1:
                    lines.append([level, c["place"].get("district"), "not in Singer's file" if not name else "several contests"])
                    continue
                b = cert_side(c["result"]["candidates"])
                for s, (sur, bv) in sorted(b.items()):
                    av, how = by_name(st, contests[name[0]], sur, s)
                    if av is None:
                        lines.append([level, c["place"].get("district"), s, how])
                    elif bv:
                        miss = abs(av - bv) / bv
                        worst = max(worst, miss)
                        lines.append([level, c["place"].get("district"), s, av, bv, round(miss, 6), how])
        tested = [x for x in lines if len(x) == 7]
        out[st] = {"worst": round(worst, 6) if tested else None, "tested": len(tested), "passes": bool(tested) and worst <= GATE_LINE, "lines": lines}
    return out


def section_2():
    h1("52.2 Gate 1: Singer's Democrat and Republican for president, US Senate and each US House district against D1's and D2's certified 2020 counts (the rule copied), line by line against D3's")
    data = load_singer()
    g = gate(data)
    chk = L.load_json(at(AFTER, "data/local/check-2020-singer.json"))
    gd = chk["gate"]
    passed = sorted(st for st, v in g.items() if v["passes"])
    failed = sorted(st for st, v in g.items() if v["tested"] and not v["passes"])
    untested = sorted(st for st, v in g.items() if not v["tested"])
    print(f"  comparisons: {sum(v['tested'] for v in g.values())} (D3: 927, {sum(v['tested'] for v in gd.values())}); pass {len(passed)} (D3 {len(chk['states_passed'])}; the same states: {passed == chk['states_passed']}); "
          f"fail {failed} (D3 {chk['states_failed']}); no certified count to test {untested} (D3's untested {[st for st, v in gd.items() if not v['tested']]})")
    same = [st for st in g if g[st] == gd.get(st)]
    print(f"  states whose gate block (worst, tested, passes, every line) equals D3's: {len(same)} of {len(g)}; differing: {[st for st in g if st not in same]}")
    for st in [st for st in g if st not in same][:5]:
        mine_l, d3_l = g[st]["lines"], gd[st]["lines"]
        print(f"    {st}: mine worst {g[st]['worst']} tested {g[st]['tested']} passes {g[st]['passes']}; D3 {gd[st]['worst']} {gd[st]['tested']} {gd[st]['passes']}; lines in mine only {[x for x in mine_l if x not in d3_l][:3]}; in D3's only {[x for x in d3_l if x not in mine_l][:3]}")
    worst = sorted(((v["worst"], st) for st, v in g.items() if v["passes"]), reverse=True)[:4]
    print(f"  the passing states' worst misses: {[(st, w) for w, st in worst]} (D3: Connecticut, New York at 0.27%); Maine: worst {g['ME']['worst']} on {g['ME']['tested']} lines (its central UOCAVA lines added, 52.1)")
    for st in failed:
        bad = [x for x in g[st]["lines"] if len(x) == 7 and x[5] > GATE_LINE]
        print(f"    {st} fails: worst {g[st]['worst']:.4f} on {g[st]['tested']} lines; over the line: " + "; ".join(f"{x[0]} {x[1] or ''} {x[2]} {x[3]:,} vs {x[4]:,} ({100 * x[5]:+.1f}%, {x[6]})" for x in bad[:4]))
    short = collections.Counter((x[0], x[2] if len(x) == 4 else x[2]) for v in g.values() for x in v["lines"] if len(x) != 7)
    print(f"  lines not compared (no contest, or no one name): {sum(short.values())}: {dict(short)}")
    how = collections.Counter(x[6] for v in g.values() for x in v["lines"] if len(x) == 7)
    print(f"  how the pair was found: by name {how['by name']}; by party line {sum(v for k, v in how.items() if k.startswith('by party'))} ({[k for k in how if k.startswith('by party')][:6]}…)")
    # Missouri's District 7: the orchestrator's note (D3: its "District 7" holds the 6th district's candidates)
    mo = data["contests"]["MO"]
    for k in sorted(mo):
        if re.match(r"^US House MO District [67]$", k):
            print(f"    Missouri's {k}: {[(x['name'], x['votes']) for x in mo[k] if person(x)][:4]}")
    for c in L.load_json(at(AFTER, "data/house/2020.json"))["contests"]:
        if c["place"]["state"] == "MO" and c["place"]["district"] in ("06", "07", "6", "7"):
            print(f"    D2's Missouri {c['place']['district']}: {[(x['name'], x['votes']) for x in c['result']['candidates'][:3]]}")
    return g


# ------------------------------------------------------------------------------------------ 52.3 gate 2

def merge_lines(cands):   # local_districts._merge_lines, copied
    out = {}
    for x in cands:
        k = " ".join(x["name"].upper().split())
        if k in out:
            out[k]["votes"] = (out[k]["votes"] or 0) + (x["votes"] or 0)
            out[k]["writein"] = out[k]["writein"] and bool(x.get("writein"))
            out[k]["lines"] += 1
        else:
            out[k] = {"name": x["name"], "votes": x["votes"] or 0, "party": x.get("party"), "writein": bool(x.get("writein")), "lines": 1}
    return list(out.values())


def legislative(data, passed):   # D3's legislative, copied: Singer's legislative contests in local_districts' shape
    pool = collections.defaultdict(list)
    for st, contests in data["contests"].items():
        if st not in passed:
            continue
        for name, cands in contests.items():
            m = LEG.match(name)
            if not m or m.group(1) != st:
                continue
            ls = []
            for x in cands:
                if NOT_VOTES.match(x["name"]):
                    continue
                wi = bool(WRITE_IN.search(x["name"])) or x["party"].upper().startswith("WRITE")
                nm = re.sub(r"\s*\((?:WRITE[- ]?IN|write in)\)\s*$", "", x["name"], flags=re.I)
                nm = re.sub(r"^WRITE-IN - ", "", nm, flags=re.I)
                nm = person_name(st, nm)
                ls.append({"name": nm if not WRITE_IN_TOTAL.match(x["name"]) else "WRITE-IN", "votes": x["votes"], "party": x["party"],
                           "writein": wi or bool(WRITE_IN_TOTAL.match(x["name"]))})
            sen = 1 if m.group(2) == "Senate" else 0
            pool[(st, sen)].append({"state": st, "sen": sen, "district": m.group(3), "counties": [], "candidates": merge_lines(ls),
                                    "file": f"{st}_tabular.tsv", "stage": "GEN", "post": m.group(4), "contest": name})
    return pool


def kc_of(rec, level):
    """Klarner's contest as D3's check reads it, from the record at BEFORE: its candidates (c46's rec_cands: party 'w' for
    a write-in line, scattering flagged), seats, district number and name."""
    head = rec["place"]["district"].split(",")[0].strip()
    m = re.search(r"(\d+)$", head)
    dno = m.group(1) if m else None
    dname = (re.sub(r"[\s\d]+$", "", head).strip().lower() if m else head.strip().lower()) or None
    return {"id": rec["id"], "state": rec["place"]["state"], "sen": 1 if level == "state-upper" else 0, "dno": dno, "dname": dname,
            "eseats": rec.get("seats") or 1, "cands": C46.rec_cands(rec), "rec": rec, "year": rec["year"]}


def klarner_2020(commit=BEFORE):
    out = []
    for level in ("state-lower", "state-upper"):
        for f in sorted(subprocess.run(["ls", at(commit, f"data/{level}/{YEAR}")], capture_output=True, text=True).stdout.split()):
            for i, rec in records_at(commit, f"data/{level}/{YEAR}/{f}").items():
                if rec.get("election") == "general":   # D3: etype 'g' (the 8 'for the rest of a term' are not)
                    out.append(kc_of(rec, level))
    return out


def generic(x):
    return C46.generic(x)


def is_write_in(x):   # local_districts._is_write_in, copied
    return bool(x.get("writein")) or bool(WRITE_IN_MARK.search(x["name"]))


def keys_of(m):   # local_districts._keys_of, copied
    if "_keys" not in m:
        ms = set()
        for x in m["candidates"]:
            ms |= C46.name_keys(x["name"])
        m["_keys"] = ({t for t, _ in ms}, ms)
    return m["_keys"]


def last_line(m, seats):   # local_districts._last_line, copied
    lines = sorted((x["votes"] or 0 for x in m["candidates"] if not generic(x)), reverse=True)
    return lines[seats - 1] if len(lines) >= seats else 0


def ballot_sized(kc, m):   # local_districts._ballot_sized, copied
    pr = pair(kc, m)
    if pr is None:
        return False
    k = kc["eseats"] or 1
    ballot = C46.on_ballot(kc["cands"])
    kl = (ballot[k - 1]["votes"] or 0) if len(ballot) >= k else 0
    ml = last_line(m, k)
    return all((pr[id(a)]["votes"] or 0) >= C46.WRITE_IN_STRONG * ml for a in ballot if id(a) in pr and (a["votes"] or 0) >= C46.WRITE_IN_STRONG * kl)


def match(kc, pool):
    """local_districts.match, copied (its New Hampshire county step and its GEN RECOUNT step cannot apply: New Hampshire is
    not in Singer's file, and Singer's contests have one stage)."""
    named = C46.named_of(kc["cands"], kc["eseats"])
    ks = [C46.name_key(a["name"]) for a in named]
    if not ks or not all(k[0] for k in ks):
        return []
    hits = []
    for m in pool.get((kc["state"], kc["sen"]), []):
        surs, ms = keys_of(m)
        if all(k[0] in surs or C46.finds(k, ms) for k in ks):
            hits.append(m)
    if len(hits) > 1 and str(kc["dno"]).isdigit():
        h = [m for m in hits if C43.dno_of(re.sub(r"\D", "", m["district"] or "") or None) == str(int(kc["dno"]))]
        hits = h or hits
    if len(hits) > 1:
        h = [m for m in hits if ballot_sized(kc, m)]
        hits = h or hits
    return hits


def pair(kc, m):   # local_districts.pair, copied
    named = [a for a in kc["cands"] if not a["scattering"]]
    must = {id(a) for a in C46.named_of(kc["cands"], kc["eseats"])}
    left = [x for x in m["candidates"] if not generic(x)]
    out = {}
    for a in sorted(named, key=lambda a: -(a["votes"] or 0)):
        s, i = C46.name_key(a["name"])
        hit = [x for x in left if s in C46.surs(x["name"])]
        if not hit:
            hit = [x for x in left if C46.finds((s, i), C46.name_keys(x["name"]))]
        else:
            whole = set().union(*(C46.surs(x["name"]) for x in hit))
            hit += [x for x in left if x not in hit and C46.finds((s, i), C46.name_keys(x["name"])) and C46.surs(x["name"]) <= whole]
        if len(hit) > 1:
            hit = [x for x in hit if C46.name_key(x["name"])[1] == i] or hit
        if len(hit) > 1:
            hit = [max(hit, key=lambda x: x["votes"] or 0)]
        if not hit:
            if id(a) in must:
                return None
            continue
        out[id(a)] = hit[0]
        left.remove(hit[0])
    return out


def test(kc, m, pr=None, b_test=True):   # local_districts.test, copied
    pr = pr if pr is not None else pair(kc, m)
    if pr is None:
        return {"matched": False}
    allnamed = [a for a in kc["cands"] if not a["scattering"]]
    named = [a for a in allnamed if id(a) in pr]
    kv = sum(a["votes"] or 0 for a in named if a["votes"])
    mv = sum(pr[id(a)]["votes"] or 0 for a in named if a["votes"])
    used = {id(x) for x in pr.values()}
    others = [x for x in m["candidates"] if id(x) not in used and not generic(x) and (x["votes"] or 0) > 0]
    kkeys = {C46.name_key(a["name"]) for a in allnamed}
    others = [x for x in others if not any(C46.finds(k, C46.name_keys(x["name"])) for k in kkeys)]
    unopposed = len(C46.on_ballot(kc["cands"])) <= (kc["eseats"] or 1)
    ratio = mv / kv if kv else None
    rest = [x for x in m["candidates"] if id(x) not in used and (is_write_in(x) or re.search(r"SCATTER|WRITE[- ]?IN|^OTHERS?$|\bALL OTHERS\b", x["name"], re.I))
            and not LD_NOT_VOTES.search(x["name"])]
    return {"matched": True, "pairs": [[a["name"], a["votes"], pr[id(a)]["name"], pr[id(a)]["votes"]] for a in named],
            "klarner": kv, "singer": mv, "ratio": None if ratio is None else round(ratio, 5),
            "flag_a": ratio is not None and abs(ratio - 1) > RATIO_OFF, "unopposed": unopposed,
            "others": [{"name": x["name"], "votes": x["votes"], "party": x.get("party"), "write_in": is_write_in(x)} for x in others],
            "flag_b": b_test and unopposed and bool(others), "b_tested": b_test,
            "singer_ballot_unpaired": len([x for x in others if not is_write_in(x)]), "singer_write_ins": sum(x["votes"] or 0 for x in rest)}


def outcome(kc, t):   # D3's outcome (local_singer), copied: the rules that need no further source
    rec = kc["rec"]
    if rec["result"].get("votes_source"):
        return {"outcome": "settled earlier", "by": rec["result"]["votes_source"]}
    if rec.get("held_reason"):
        return {"outcome": "settled earlier", "by": "held"}
    r = t["ratio"]
    ballot_others = [x for x in t["others"] if not x["write_in"]]
    voted = [p for p in t["pairs"] if p[1]]
    if t["flag_a"] and r is not None and len(voted) >= 2 and not ballot_others and all(abs(p[3] / p[1] - 0.5) <= 0.5 * DOUBLE_TOL for p in voted):
        return {"outcome": "Klarner's figures doubled (Singer's at half)"}
    gaps = [abs(r - 1)] if t["flag_a"] else []
    if t["flag_b"] and ballot_others:
        tot = t["singer"] + sum(x["votes"] for x in t["others"])
        gaps.append(sum(x["votes"] for x in ballot_others) / tot if tot else 1.0)
    if not gaps:
        return {"outcome": "write-in rule"}
    g = max(gaps)
    return {"outcome": "held" if g >= HOLD_GAP else "noted", "gap": round(g, 5)}


def district_checks(data, passed):
    """D3's check, copied in its course: every Klarner 2020 general record at BEFORE against Singer's pool."""
    pool = legislative(data, passed)
    states = {k[0] for k in pool}
    cs = klarner_2020()
    tallies, flags, found = collections.Counter(), [], []
    untested, unmatched, unmatched_ids = collections.Counter(), collections.Counter(), []
    for kc in cs:
        if kc["state"] not in states:
            untested[kc["state"]] += 1
            continue
        hits = match(kc, pool)
        if len(hits) != 1:
            tallies["unmatched" if not hits else "matched to several"] += 1
            unmatched[kc["state"]] += 1
            unmatched_ids.append((kc["id"], len(hits), len(C46.on_ballot(kc["cands"])), kc["eseats"]))
            continue
        found.append((kc, hits[0]))
    groups = collections.defaultdict(list)
    for kc, m in found:
        groups[id(m)].append(kc)
    tests = {}
    for kc, m in found:
        pr, b_test = None, True
        if len(groups[id(m)]) > 1:
            prs = [pair(k_, m) for k_ in groups[id(m)]]
            lines = [id(x) for p_ in prs if p_ for x in p_.values()]
            if any(p_ is None for p_ in prs) or len(lines) != len(set(lines)):
                tallies["a Singer contest that several districts match, not paired apart"] += 1
                continue
            pr, b_test = prs[groups[id(m)].index(kc)], False
            tallies["shared: (a) only"] += 1
        t = test(kc, m, pr, b_test)
        if not t["matched"]:
            tallies["candidates not paired"] += 1
            continue
        tallies["tested"] += 1
        tests[kc["id"]] = (kc, m, t)
        if not (t["flag_a"] or t["flag_b"]):
            continue
        f = {"id": kc["id"], "state": kc["state"], "chamber": "state-upper" if kc["sen"] else "state-lower", "dno": kc["dno"], "eseats": kc["eseats"],
             "singer_contest": m["contest"], "flags": [x for x, y in (("a", t["flag_a"]), ("b", t["flag_b"])) if y]}
        f.update(outcome(kc, t))
        f.update(t)
        flags.append(f)
    for f in flags:
        tallies[f"flag {'+'.join(f['flags'])}: {f['outcome']}"] += 1
    return {"tallies": dict(sorted(tallies.items())), "untested": dict(sorted(untested.items())), "unmatched": dict(sorted(unmatched.items())),
            "unmatched_ids": unmatched_ids, "flags": sorted(flags, key=lambda f: (f["state"], f["chamber"], f["id"])), "tests": tests, "pool": pool, "records": len(cs)}


def flag_key(f):
    return (f["state"], f["chamber"], str(int(f["dno"])) if f.get("dno") and str(f["dno"]).isdigit() else f.get("dno"))


def section_3():
    h1("52.3 Gate 2: section 32's district checks (match, pair, test and the outcome rules copied) on every Klarner 2020 general record at BEFORE, against Singer's contests of the states that pass gate 1")
    data = load_singer()
    chk = L.load_json(at(AFTER, "data/local/check-2020-singer.json"))
    passed = set(chk["states_passed"])
    g = gate(data)
    assert passed == {st for st, v in g.items() if v["passes"]}, "the passing states differ from 52.2's"
    r = district_checks(data, passed)
    print(f"  Klarner's 2020 general records at {BEFORE}: {r['records']:,} (D3: 1,464 untested by state + 3,880 tested + 136 unmatched + 15 shared + 1 not paired = 5,496); Singer's legislative contests in the pool: {sum(len(v) for v in r['pool'].values()):,} in {len({k[0] for k in r['pool']})} states")
    print(f"  untested, their state not in the pool: {sum(r['untested'].values()):,} (D3: 1,464) {r['untested']}; equal to D3's by state: {r['untested'] == chk['klarner_2020_contests_not_tested_by_state']}")
    print(f"  my tallies: {r['tallies']}")
    print(f"  D3's tallies: {chk['tallies']}")
    mine_t = {k: v for k, v in r["tallies"].items() if not k.startswith("flag ") and k != "shared: (a) only"}
    print(f"  equal (tested, unmatched, shared not paired apart, candidates not paired): {mine_t == {k: v for k, v in chk['tallies'].items() if not k.startswith('flag ')}}; unmatched by state mine {r['unmatched']} = D3's: {r['unmatched'] == chk['unmatched_by_state']}")
    un = collections.Counter((x[2] <= x[3]) for x in r["unmatched_ids"])
    print(f"  the unmatched {len(r['unmatched_ids'])}: with no more names on the ballot than seats (unopposed, which Singer's file leaves out [D3's inference]) {un[True]}; contested {un[False]}: {[x[0] for x in r['unmatched_ids'] if x[2] > x[3]][:12]}")
    mine = {flag_key(f): f for f in r["flags"]}
    theirs = {flag_key(f): f for f in chk["flags"]}
    print(f"\n  flags: mine {len(mine)}, D3's {len(theirs)}; the same districts: {set(mine) == set(theirs)}; mine only {sorted(set(mine) - set(theirs))}; D3's only {sorted(set(theirs) - set(mine))}")
    eq = collections.Counter()
    for k in sorted(set(mine) & set(theirs)):
        a, b = mine[k], theirs[k]
        rule_b = b.get("outcome_by_rule") or b["outcome"]
        same = {"pairs": sorted(map(tuple, a["pairs"])) == sorted(map(tuple, b["pairs"])), "ratio": a["ratio"] == b["ratio"], "klarner": a["klarner"] == b["klarner"], "singer": a["singer"] == b["singer"],
                "flags": a["flags"] == b["flags"], "outcome by rule": a["outcome"] == rule_b, "gap": a.get("gap") == b.get("gap"), "eseats": a["eseats"] == b["eseats"],
                "unopposed": a["unopposed"] == b["unopposed"], "write-ins": a["singer_write_ins"] == b["singer_write_ins"] and a["singer_ballot_unpaired"] == b["singer_ballot_unpaired"],
                "contest": a["singer_contest"] == b["singer_contest"], "b_tested": a["b_tested"] == b["b_tested"]}
        for kk, v in same.items():
            eq[kk] += v
        if not all(same.values()):
            print(f"    DIFFERS {k}: {[kk for kk, v in same.items() if not v]}; mine {a['outcome']} {a.get('gap')} {a['ratio']} {a['pairs']}; D3 {rule_b} {b.get('gap')} {b['ratio']} {b['pairs']}")
    print(f"  field by field over the {len(set(mine) & set(theirs))} flags shared: {dict(eq)} (the pairs as sets: D3 lists them in Klarner's file order, I in the record's)")
    byo = collections.Counter((f["state"], f.get("outcome_by_rule") or f["outcome"]) for f in chk["flags"])
    print(f"  D3's outcomes by the rule (before the state's canvass): {dict(sorted(byo.items()))}; after settle_mt: {dict(collections.Counter(f['outcome'] for f in chk['flags']))}")
    for f in r["flags"]:
        print(f"    {f['id']}: {f['outcome']} gap {f.get('gap')}, ratio {f['ratio']}, Klarner {f['klarner']:,} Singer {f['singer']:,}; " + "; ".join(f"{p[0]} {p[1]:,} / {p[2]} {p[3]:,}" for p in f["pairs"]))
    # the flagged tests among all tests: how many ratios lie within 3%; the distribution
    rs = [t["ratio"] for _, _, t in r["tests"].values() if t["ratio"] is not None]
    bands = collections.Counter("equal" if x == 1 else "within 0.5%" if abs(x - 1) <= 0.005 else "0.5-3%" if abs(x - 1) <= 0.03 else "over 3%" for x in rs)
    print(f"  the {len(rs):,} tested ratios: {dict(bands)}")
    return r


# ------------------------------------------------------------------------------------------ 52.4 Montana's canvass, Maine's rows

def mt_canvass():
    """My own reading of the canvass: each district's block ('HD 03 Total' or 'SD 01 Total', the counties' names, then for
    each candidate a party line with the counties' votes and the total, and the name's words on the lines below)."""
    if C49.sha256(MT_PDF) != MT_SHA:
        raise SystemExit("Montana's canvass: not the file the note names")
    txt = subprocess.run(["pdftotext", "-layout", MT_PDF, "-"], capture_output=True, check=True).stdout.decode("utf-8")
    out, cur, cand, sums_ok, n_cands = {}, None, None, 0, 0
    head = re.compile(r"^(HD|SD) (\d+)\s+Total$")
    line = re.compile(r"^([A-Za-z][A-Za-z ]*?)\s+((?:\d+\s+)*\d+)$")
    for raw in txt.splitlines():
        s = re.sub(r"\s+", " ", raw.replace("\f", "")).strip()
        if not s or s.startswith("MONTANA SECRETARY OF STATE") or s.startswith("2020 LEGISLATIVE GENERAL"):
            continue
        m = head.match(s)
        if m:
            cur, cand = (m.group(1), int(m.group(2))), None
            assert cur not in out, f"{cur} twice"
            out[cur] = []
            continue
        m = line.match(s)
        if m and cur:
            nums = [int(x) for x in m.group(2).split()]
            cand = {"party": m.group(1), "counties": nums[:-1], "total": nums[-1], "name": ""}
            sums_ok += (len(nums) == 1) or sum(nums[:-1]) == nums[-1]
            n_cands += 1
            out[cur].append(cand)
            continue
        if cand is not None and re.match(r"^[A-Z][A-Z .'&-]*$", s):
            cand["name"] = (cand["name"] + " " + s).strip()
    return out, sums_ok, n_cands


def section_4():
    h1("52.4 Montana's 2020 legislative canvass (my own reading) against Singer's and Klarner's counts; Maine's legislative rows by reporting unit")
    cv, sums_ok, n_cands = mt_canvass()
    hd, sd = [k for k in cv if k[0] == "HD"], [k for k in cv if k[0] == "SD"]
    print(f"  the canvass: {len(hd)} House and {len(sd)} Senate districts (D3: 100 and 25), {n_cands} candidate lines, counties adding up to the total in {sums_ok} of {n_cands}; "
          f"parties {dict(collections.Counter(x['party'] for v in cv.values() for x in v))}; any nameless line: {any(not x['name'] for v in cv.values() for x in v)}")
    data = load_singer()
    mt = data["contests"]["MT"]
    chk = L.load_json(at(AFTER, "data/local/check-2020-singer.json"))
    # the three flags
    for f in [f for f in chk["flags"] if f["state"] == "MT"]:
        k = ("SD" if f["chamber"] == "state-upper" else "HD", int(f["dno"]))
        lines = cv[k]
        sc = f["state_count"]
        rows = []
        for kname, kv, sname, sv in f["pairs"]:
            hit = [x for x in lines if C46.name_key(x["name"])[0] == C46.name_key(kname)[0]]
            rows.append((kname, kv, sv, hit[0]["name"] if len(hit) == 1 else None, hit[0]["total"] if len(hit) == 1 else None))
        agrees_s = all(x[4] == x[2] for x in rows) and len(lines) == len(f["pairs"])
        agrees_k = all(x[4] == x[1] for x in rows)
        d3_rows = [(p[0], p[1], p[2], p[3], p[4]) for p in sc["pairs"]]
        print(f"  {f['id']} ({f['singer_contest']}): the canvass {[(x['name'], x['party'], x['total']) for x in lines]}; Klarner / Singer / the state: {[(x[0], x[1], x[2], x[4]) for x in rows]}; "
              f"the state agrees with Singer's on every candidate: {agrees_s}; with Klarner's: {agrees_k}; D3's state_count pairs equal mine: {d3_rows == [(x[0], x[1], x[2], x[3], x[4]) for x in rows]}; "
              f"its sha256 {sc['sha256'][:8]}… = the file's: {sc['sha256'] == MT_SHA}; read {sc['read_utc']}; outcome {f['outcome']} (by the rule: {f.get('outcome_by_rule')})")
    # every district: the canvass against Singer's MT file and against Klarner's records at BEFORE
    recs = {}
    for level, ch in (("state-lower", "HD"), ("state-upper", "SD")):
        for i, rec in records_at(BEFORE, f"data/{level}/{YEAR}/MT.json").items():
            if rec.get("election") == "general":
                recs[(ch, int(rec["place"]["district"]))] = rec
    tal = collections.Counter()
    diffs, name_off = [], collections.Counter()
    for k in sorted(cv):
        name = f"MT {'House' if k[0] == 'HD' else 'Senate'} District {k[1]}"
        s_cands = [x for x in mt.get(name, []) if person(x)]
        st_v = sorted(x["total"] for x in cv[k])   # by the votes: the canvass wraps a long surname over two lines ("WEATHERW" / "AX"), so a name key is not the test
        s_v = sorted(x["votes"] for x in s_cands)
        st_keys = {C46.name_key(x["name"])[0] for x in cv[k]}
        if name not in mt:
            tal["not in Singer's file"] += 1
        elif st_v == s_v:
            tal["Singer's = the canvass, every candidate's votes"] += 1
            name_off["Singer"] += st_keys != {C46.name_key(x["name"])[0] for x in s_cands}
        else:
            tal["Singer's differs"] += 1
            diffs.append(("Singer", k, [(x["name"], x["total"]) for x in cv[k]], [(x["name"], x["votes"]) for x in s_cands]))
        rec = recs.get(k)
        if rec is None:
            tal["no record"] += 1
            continue
        kc = [c for c in rec["result"]["candidates"] if (c.get("party") or "") != "write-in" and (c.get("name") or "").lower() != "scattering"]
        if sorted(c["votes"] for c in kc) == st_v:
            tal["Klarner's = the canvass, every candidate's votes"] += 1
            name_off["Klarner"] += st_keys != {C46.name_key(c["name"])[0] for c in kc}
        else:
            tal["Klarner's differs"] += 1
            diffs.append(("Klarner", k, [(x["name"], x["total"]) for x in cv[k]], [(c["name"], c["votes"]) for c in kc]))
    print(f"  all {len(cv)} districts, each candidate's votes: {dict(tal)}; districts whose surname keys differ from the canvass's while the votes agree (compound surnames joined or wrapped): {dict(name_off)}")
    for d in diffs:
        print(f"    {d[0]} differs at {d[1]}: the canvass {d[2]}; {d[0]}'s {d[3]}")
    # Maine's rows
    units = data["checks"]["me_leg_units"]
    kinds = collections.Counter("the state's own line" if u == "Maine" else "a county" if re.fullmatch(r"Maine;[A-Za-z ]+ County", u) else "below the county" for u in units)
    print(f"\n  Maine's legislative rows (ME House and Senate contests, 'total' lines): reporting units {len(units)}: {dict(kinds)}; the counties {sorted(u.split(';')[1] for u in units if ';' in u)}; "
          f"rows on the state's own line {units.get('Maine', 0):,}, on counties {sum(v for u, v in units.items() if ';' in u):,} (D3: no row lies below the county, so 22:26 (b) has nothing to measure)")
    me = data["contests"]["ME"]
    bl = [x for x in data["checks"]["both_levels"] if x[0] == "ME"]
    print(f"  Maine's own-line (UOCAVA) additions: {len(bl)} lines, {sum(x[3] for x in bl):,} votes over the counties' {sum(x[4] for x in bl):,}; in the legislature {len([x for x in bl if LEG.match(x[1])])} lines, "
          f"in the federal contests {len([x for x in bl if x[1].startswith('US ')])}; House 122's lines: {[(x['name'], x['votes'], x['units']) for x in me.get('ME House District 122', [])]}")


# ------------------------------------------------------------------------------------------ 52.5 the records, the moves

def note_for(fl):
    """The record's note or held reason as pipeline/local.py's singer_checks writes it (its formats copied), from the
    check file's flag."""
    n = len(fl["pairs"])
    s_ = "" if n == 1 else "s"
    src = S_SRC.format(file=fl["file"])
    diff = "; ".join(f"{p_[0]}: {p_[1]:,} in Klarner's, {p_[3]:,} in Singer's" for p_ in fl["pairs"])
    o = fl["outcome"]
    if o in ("held", "noted"):
        what = S_RATIO.format(src=src, n=n, s=s_, m=fl["singer"], k=fl["klarner"], pct=100 * (fl["ratio"] - 1), diff=diff, why=fl["why"])
        return S_HELD.format(what=what, rule=S_RULE) if o == "held" else S_NOTED.format(what=what, rule=S_RULE)
    sc = fl["state_count"]
    return S_AGREE_SINGER.format(src=src, n=n, s=s_, m=fl["singer"], k=fl["klarner"], pct=100 * (fl["ratio"] - 1), ssrc=sc["source"], url=sc["url"], read=sc["read_utc"], sha=sc["sha256"],
                                 pairs="; ".join(f"{d_}: {v_:,} in the state's, {s__:,} in Singer's, {k__:,} in Klarner's" for _, k__, s__, d_, v_ in sc["pairs"]), diff=diff)


def density_p(mean, sd, n):
    """p by the density method as the records carry it: f at one half of the normal forecast, event = f / n, p = event / 2
    (the records' own fields f_half, event, value, read on every partisan record of these files)."""
    f = math.exp(-0.5 * ((0.5 - mean) / sd) ** 2) / (sd * math.sqrt(2 * math.pi))
    return f, f / n, f / n / 2


def d3_files(commit_a, commit_b):
    files = subprocess.run(["git", "diff", "--name-only", commit_a, commit_b, "--", "data/"], capture_output=True, text=True, cwd=L.ROOT).stdout.split()
    rec = [f for f in files if re.match(r"^data/(local|primary|measure|state-lower|state-upper)/\d{4}/[A-Z]{2}\.json$", f)]
    d2 = [f for f in files if re.match(r"^data/(governor|house|senate|president)/\d{4}\.json$", f)]
    other = [f for f in files if f not in rec and f not in d2]
    return rec, d2, other


def section_5():
    h1("52.5 The records at AFTER: every flag's outcome as built; the moves file against my own diff of every D3 record")
    chk = L.load_json(at(AFTER, "data/local/check-2020-singer.json"))
    tal = collections.Counter()
    for fl in chk["flags"]:
        st, lv = fl["state"], fl["chamber"]
        b = records_at(BEFORE, f"data/{lv}/{YEAR}/{st}.json")
        a = records_at(AFTER, f"data/{lv}/{YEAR}/{st}.json")
        rid = f"{YEAR}-{lv}-{st}-{int(fl['dno'])}"
        rb, ra = b[rid], a[rid]
        d = C40.what_differs(rb, ra)
        text = note_for(fl)
        o = fl["outcome"]
        if o == "held":
            got = ra.get("p", {}).get("not_computed")
            one_name = len(C46.on_ballot(C46.rec_cands(rb))) <= (rb.get("seats") or 1)   # p was 0 before (unopposed)
            ok = (got == text or (one_name and got == text + "; " + HELD_ONE_NAME)) and "value" not in ra.get("p", {}) and not ra.get("forecasts") and "two_party" not in ra and ra["result"] == rb["result"]
            tal[("held", ("p not computed, its reason the held text word for word" + (" then HELD_ONE_NAME (one name on the ballot: p was 0 before)" if one_name else "") + ", no forecast, the counts unchanged") if ok else "DIFFERS")] += 1
            if not ok:
                got = ra.get("p", {}).get("not_computed") or ""
                j = next((j for j in range(min(len(got), len(text))) if got[j] != text[j]), min(len(got), len(text)))
                print(f"    {rid} DIFFERS: text equal {got == text} (first difference at {j}: record {got[max(0, j - 40):j + 60]!r} / mine {text[max(0, j - 40):j + 60]!r}); value absent {'value' not in ra.get('p', {})}; forecasts {ra.get('forecasts')}; two_party absent {'two_party' not in ra}; result unchanged {ra['result'] == rb['result']}")
            tal[("held", "fields differing", d)] += 1
        elif o == "noted":
            ok = text in (ra.get("notes") or []) and pval(ra) == pval(rb) and ra["result"] == rb["result"] and [x for x in d if x not in ("notes", "p.commit")] == []
            tal[("noted", "the note's words in the record, p and the counts unchanged, nothing else differs" if ok else f"DIFFERS {d}")] += 1
        else:
            votes_ok = [[c["name"], c["votes"]] for c in ra["result"]["candidates"]] == sorted([[p_[0], p_[3]] for p_ in fl["pairs"]], key=lambda x: -x[1]) or \
                       {c["name"]: c["votes"] for c in ra["result"]["candidates"]} == {p_[0]: p_[3] for p_ in fl["pairs"]}
            total_ok = ra["result"]["total_votes"] == sum(p_[3] for p_ in fl["pairs"])
            src_ok = ra["result"].get("votes_source") == "singer" and ra["result"].get("source") == "klarner"
            note_ok = text in (ra.get("notes") or [])
            fc = (ra.get("forecasts") or [{}])[0]
            n = ra["p"]["n"]
            if fc.get("route") == "partisan":
                f, ev, p = density_p(fc["share"]["mean"], fc["share"]["sd"], n)
                p_ok = abs(p / ra["p"]["value"] - 1) <= 2e-4 and abs(f / ra["p"]["f_half"] - 1) <= 2e-4
                how = f"partisan: mean {fc['share']['mean']} sd {fc['share']['sd']} (before: sd {rb['forecasts'][0]['share']['sd']}) n {n:,} (before {rb['p']['n']:,}): f {f:.5f} (record {ra['p']['f_half']}), p {p:.6g} (record {ra['p']['value']})"
            else:
                f = ra["p"]["f_half"]
                p = f / n / 2
                p_ok = abs(p / ra["p"]["value"] - 1) <= 2e-4 and f == rb["p"]["f_half"]
                how = f"class route: f_half {f} (before {rb['p']['f_half']}, the like races' device) n {n:,} (before {rb['p']['n']:,}): p {p:.6g} (record {ra['p']['value']})"
            tp = ra.get("two_party") or {}
            tp_ok = (not tp) or (tp["n_other_voters"] == sum(tp["votes"]) - 1 and n == tp["n_other_voters"])
            tal[("Singer's count", "votes, total, votes_source, the note, two_party and p by the density formula all as the flag and the formats give" if votes_ok and total_ok and src_ok and note_ok and p_ok and tp_ok else
                 f"DIFFERS votes {votes_ok} total {total_ok} source {src_ok} note {note_ok} p {p_ok} two_party {tp_ok}")] += 1
            print(f"    {rid}: p {pval(rb):.4g} -> {pval(ra):.4g} (x{pval(ra) / pval(rb):.3f}); {how}; state_agrees in the record: {'state_agrees' in ra}; fields differing {d}")
    for k, v in sorted(tal.items(), key=str):
        print(f"  {k}: {v}")
    # the sd of the partisan route against the chamber's other records of the class (the sd moved with n on House 3 and 84)
    for lv in ("state-lower",):
        a = records_at(AFTER, f"data/{lv}/{YEAR}/MT.json")
        by = collections.defaultdict(list)
        for i, r in a.items():
            fc = (r.get("forecasts") or [{}])[0]
            if fc.get("route") == "partisan" and r.get("p", {}).get("n"):
                by[((r.get("forecast_inputs") or {}).get("class"), fc["share"]["sd"])].append(r["p"]["n"])
        print("  Montana's 2020 House partisan records at AFTER, by class and the forecast's sd: " + "; ".join(f"class {c} sd {s}: {len(ns)} records, n {min(ns):,} to {max(ns):,}" for (c, s), ns in sorted(by.items(), key=lambda kv: (str(kv[0][0]), kv[0][1]))))
    # the files' sources.singer
    with_src = []
    for lv in ("state-lower", "state-upper"):
        for f in subprocess.run(["ls", at(AFTER, f"data/{lv}/{YEAR}")], capture_output=True, text=True).stdout.split():
            hdr = L.load_json(at(AFTER, f"data/{lv}/{YEAR}/{f}"))
            if "singer" in (hdr.get("sources") or {}):
                with_src.append((f"{lv}/{YEAR}/{f}", hdr["sources"]["singer"] == chk["source"], any((c["result"].get("votes_source") == "singer") for c in hdr["contests"])))
    print(f"  files whose sources name Singer's dataset: {with_src} (D3: the files with a record at Singer's count; the source block equal to the check file's)")
    # the moves
    print("\n  the moves file against my own diff")
    mv = L.load_json(at(AFTER, "data/local/moves-39.json"))
    rows = collections.defaultdict(list)
    for r in mv["records"]:
        rows[r[0]].append(r)
    rec_files, d2_files, other = d3_files(BEFORE, AFTER)
    print(f"  moves-39.json: {len(mv['records']):,} rows, {len(rows):,} ids, against {mv['against']} (the code commit whose records are main's f6434077's, which equal {BEFORE}'s D3 records: my diff is main to main); its summary: {json.dumps(mv['summary'])}")
    print(f"  files changed between {BEFORE} and {AFTER} under data/: D3's record files {len(rec_files)} {dict(collections.Counter(f.split('/')[1] for f in rec_files))}; D2's {d2_files}; other {other}")
    mine = collections.Counter()
    seen, agree, dis, pdiff, rdiff, stamps = set(), 0, collections.Counter(), 0, 0, 0
    moved, lost, gained = [], [], []
    notes_changed = collections.Counter()
    for f in rec_files:
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
            pb, pa = pval(b.get(i) or {}), pval(a.get(i) or {})
            if c == "P":
                moved.append((pa / pb if pb else None, i, lv, yr, (a.get(i) or {}).get("place", {}).get("state")))
            if c == "L":
                lost.append((i, pb, str((a.get(i) or {}).get("p", {}).get("not_computed"))[:60]))
            if c == "N":
                gained.append((i, pa))
            if "notes" in d:
                notes_changed[lv] += 1
            mine[(lv, c)] += 1
            seen.add(i)
            hits = rows.get(i)
            if not hits:
                dis[(lv, c, "not in the file")] += 1
                continue
            theirs = set()
            for row in hits:
                theirs |= set(row[8])
            if c in theirs or (c in ("Q", "O", "B", "R") and theirs & {"Q", "O", "R", "B"}):
                agree += 1
            else:
                dis[(lv, c, tuple(sorted(theirs)))] += 1
            for row in hits:
                if isinstance(row[5], str) or isinstance(row[6], str):
                    continue
                if (row[5] is None) != (pb is None) or (row[6] is None) != (pa is None) or (pb is not None and abs(row[5] - pb) > 1e-9 * max(abs(pb), 1e-300)) or (pa is not None and abs(row[6] - pa) > 1e-9 * max(abs(pa), 1e-300)):
                    pdiff += 1
                if pb and pa and row[7] is not None and abs(row[7] - round(pa / pb, 4)) > 1.5e-4:
                    rdiff += 1
    not_mine = [i for i in rows if i not in seen]
    print(f"  my diff, by level and code: " + "; ".join(f"{lv} {k} {v}" for (lv, k), v in sorted(mine.items())) + f"; records differing in p.commit alone: {stamps}")
    print(f"  ids whose code I share with the file: {agree} of {len(seen)}; differing or missing: {dict(dis)}; ids in the file but not in my diff: {len(not_mine)} {not_mine[:5]}; p before/after other than the record's: {pdiff}; ratios off by more than 1.5e-4: {rdiff}")
    mv_all = [m for m in moved if m[0] is not None]
    print(f"  p moved: {len(mv_all):,} (D3: 7,546; the file's P rows {len([r for r in mv['records'] if 'P' in r[8]]):,}); p lost: {len(lost)} (D3: 17); p gained: {len(gained)} (D3: 0) {gained[:3]}")
    print(f"  lost: {[(i, f'{p:.3g}', w) for i, p, w in lost]}")
    over2 = [m for m in mv_all if m[0] > 2 or m[0] < 0.5]
    print(f"  over 2x either way: {len(over2)}: {[(i, round(r_, 3)) for r_, i, lv, yr, st in over2]}")
    byly = collections.defaultdict(list)
    for r_, i, lv, yr, st in mv_all:
        byly[(lv, yr)].append((r_, st))
    print("  by level and year (D3's table): " + "; ".join(f"{lv} {yr}: {len(v)}, x{min(x[0] for x in v):.4f} to x{max(x[0] for x in v):.4f}" for (lv, yr), v in sorted(byly.items())))
    over1 = [(lv, yr, st) for r_, i, lv, yr, st in mv_all if abs(r_ - 1) > 0.01 and not (r_ > 2 or r_ < 0.5)]
    print(f"  moved by more than 1% (short of 2x): {len(over1)} {dict(collections.Counter(over1))} (D3: 139 in state-lower 2022, Maine 61, New York 78)")
    print(f"  records whose notes changed, by level: {dict(notes_changed)} (D3: 8, the 5 noted and Montana's 3)")
    # the lean's move (New York's 2022 lower chamber: D3 0.0968 -> 0.1008)
    for st in ("NY", "ME"):
        b, a = records_at(BEFORE, f"data/state-lower/2022/{st}.json"), records_at(AFTER, f"data/state-lower/2022/{st}.json")
        lb = {(r.get("forecast_inputs") or {}).get("lean") for r in b.values()} - {None}
        la = {(r.get("forecast_inputs") or {}).get("lean") for r in a.values()} - {None}
        print(f"  {st} 2022 lower: the lean in the records' forecast inputs {sorted(lb)} -> {sorted(la)} (D3: New York's 0.0968 -> 0.1008)")


# ------------------------------------------------------------------------------------------ 52.6 my two readings taken

def page_text(raw):   # pipeline/local_recount.page_text, copied (D3's text_method)
    t = re.sub(r"(?is)<(script|style|noscript)\b.*?</\1\s*>", " ", raw.decode("utf-8", "replace"))
    t = re.sub(r"(?s)<!--.*?-->", " ", t)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", _html.unescape(t)).strip()


def section_6():
    h1("52.6 My two readings taken: FairVote's text sha256 from my own copy of the page; the recount listing at AFTER against my scan (c51's rules)")
    lst_a = L.load_json(at(AFTER, "data/local/recount-zone.json"))
    lst_b = L.load_json(at(BEFORE, "data/local/recount-zone.json"))
    fv = lst_a["sources"]["fairvote"]
    with open(FAIRVOTE, "rb") as f:
        raw = f.read()
    t = page_text(raw)
    h = hashlib.sha256(t.encode("utf-8")).hexdigest()
    chars = re.search(r"\(([0-9,]+) characters\)", fv["text_method"])
    print(f"  FairVote: my copy (read 10:35:39, {len(raw):,} bytes, sha256 {hashlib.sha256(raw).hexdigest()[:8]}…; the listing's page sha256 {fv['sha256'][:8]}…, {fv['bytes']:,} bytes) -> text by D3's page_text copied: {len(t):,} characters, "
          f"sha256 {h[:16]}…; the listing's text_sha256 {fv['text_sha256'][:16]}…: equal {h == fv['text_sha256']} (the method text names {chars.group(1) if chars else '?'} characters)")
    print(f"  the listing's rule.near_with_zone_under: {'near_with_zone_under' in lst_a['rule']}; counts.near_with_zone_under at 0.87%: {lst_a['counts']['0.87%'].get('near_with_zone_under')} (my section 21: 48 under 2 votes, 31 under 1.5)")
    recs_a = C51.scan(AFTER)
    recs_b = C51.scan(BEFORE)
    ids_a, ids_b = {r[0] for r in recs_a}, {r[0] for r in recs_b}
    print(f"  records with p above 0 and a spread: {len(recs_a):,} at AFTER (the listing: {lst_a['records_with_p_above_0']:,}), {len(recs_b):,} at BEFORE (the listing then: {lst_b['records_with_p_above_0']:,}); "
          f"lost {len(ids_b - ids_a)} {sorted(ids_b - ids_a)[:3]}…; gained {len(ids_a - ids_b)} {sorted(ids_a - ids_b)}")
    for i in sorted(ids_a - ids_b):
        lv = i.split("-")[1] if not i.startswith("20") else i.split("-")[1]
        print(f"    gained: {i}: {[r for r in recs_a if r[0] == i][0][1:13]}")
    cache = {}
    counts = {lab: {"near": 0, "by": collections.Counter(), "g": [], "tails": 0, "tails_p": 0.0, "under2": 0, "under15": 0, "near_ids": set()} for lab, _ in C51.RATES}
    for (i, lev, yr, st, route, n, mu, sd, how, at_, p, cls, f, zn) in recs_a:
        for lab, rate in C51.RATES:
            k = (round(mu, 6), round(sd, 6), rate, at_)
            if k not in cache:
                cache[k] = C51.gain_trap(mu, sd, rate, at_)
            g = cache[k]
            near = rate * n >= C51.NEAR * n * sd
            cn = counts[lab]
            if near:
                cn["near"] += 1
                cn["by"][f"{lev}, {route}"] += 1
                cn["g"].append(g)
                cn["under2"] += rate * n < 2
                cn["under15"] += rate * n < 1.5
                cn["near_ids"].add(i)
            elif g >= 1.04:
                cn["tails"] += 1
                cn["tails_p"] = max(cn["tails_p"], p)
    noted = {r[0] for r in recs_a if r[13]}
    noted_b = {r[0] for r in recs_b if r[13]}
    for lab, _ in C51.RATES:
        cn, th = counts[lab], lst_a["counts"][lab]
        print(f"  {lab}: near {cn['near']:,} (the listing: {th['near']:,}); by level and route equal: {dict(cn['by']) == th['by_level_and_route']}; gain over p {min(cn['g']):.3f} to {max(cn['g']):.3f} (the listing {th['gain_over_p']}); "
              f"zone under 2 votes {cn['under2']}, under 1.5 {cn['under15']} (the listing {th['near_with_zone_under']}); raised in the tails {cn['tails']:,} with p at most {cn['tails_p']:.4g} (the listing {th['raised_in_the_tails']})")
    print(f"  the 0.87% notes: records carrying one at AFTER {len(noted):,}, at BEFORE {len(noted_b):,}, the same records: {noted == noted_b}; equal to my near set at 0.87%: {noted == counts['0.87%']['near_ids']}")
    row_ids = {r[0] for r in lst_a["near"]}
    any_near = set().union(*(counts[lab]["near_ids"] for lab, _ in C51.RATES))
    print(f"  the listing's rows: {len(lst_a['near']):,} at AFTER (D3: 15,120; 15,122 before); the rows' ids equal my near-at-any-rate set: {row_ids == any_near} (in both {len(row_ids & any_near):,})")


def main():
    want = [int(x) for x in sys.argv[1:]] or [1, 2, 3, 4, 5, 6]
    print(f"c52_singer_2020.py: section 22 (D3's #118, {AFTER}); run at {L.git_head()}; sections {want}")
    for s in want:
        globals()[f"section_{s}"]()


if __name__ == "__main__":
    main()
