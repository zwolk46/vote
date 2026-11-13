"""pipeline/local_singer.py: Singer's US 2020 General Official Election Results (Harvard Dataverse doi:10.7910/DVN/RV80FW)
as 2020's second count of the state legislatures, beside Klarner's.

Written 2026-11-13 by worker D3 on the orchestrator's orders of 09:23 and 10:33 UTC. 09:23: "proposal 2, Singer 2020.
Read only whether its file sits behind a guestbook ... If it does not, take it, under the same gates." 10:33: "Yes to
Singer 2020 (RV80FW, CC0, no guestbook), under the same gates, with its own intake and PR. You may make the requests
that reach its file: the dataset's file list and the file itself, one each. Name them in the log. Ask me before any
other." Reason (D3's proposal, accepted): MEDSL's 2020 file holds local offices only, so 2020 is the one even year of
2016-2022 whose state legislatures had no second count: the district checks (pipeline/local_districts.py,
data/local/REPORT.md section 32) and the volume test's part 2 could not test Klarner's 2020 [stated there].

The source [stated, its Dataverse record]: Stephanie Frank Singer (Portland State University), "US 2020 General Official
Election Results in Tabular Format", v1.0, released 2021-08-27, CC0 1.0: "Official 2020 General Election results for
all 56 major US jurisdictions ... by county (or other major subdivision) including all federal contests and most
statewide and state legislative contests ... The data in these files comes from, or is rolled up to the county level
from, files or web pages published by the State, District or Territory Boards of Election." It is a compilation of the
boards' files, not a board's own: a third party's copy, so it settles nothing over Klarner's count (the ruling of
2026-11-07 21:03: third-party copies never win as the certified source); it is a second count, as MEDSL's is.

The requests (one each, 10:33), in $VOTE_CACHE/singer2020/raw/ with their .meta.json:
  the dataset's record and file list  https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/RV80FW
  the files, as Dataverse's one download of the whole dataset in the files' original format (56 tab-separated files,
  one per jurisdiction)  https://dataverse.harvard.edu/api/access/dataset/:persistentId/?persistentId=doi:10.7910/DVN/RV80FW&format=original
`normalize` checks every file's md5 against the record before reading it.

The gates, as for every second source (the orchestrator, "the same gates"):
  1. The federal gate (local_in.gate's and local_medsl.quality's line, 0.5%): each jurisdiction's Democratic and
     Republican votes for president, US Senate and each US House district, against D1's and D2's certified 2020
     counts. A state that misses by more is not used.
  2. The district checks of section 32 (pipeline/local_districts.py match, pair and test, unchanged), Klarner's 2020
     general contests against Singer's: (a) the ratio of the paired candidates' votes off 1 by more than 3%; (b) a
     Klarner contest with no more names than seats where Singer names another candidate with votes. Each flag's
     outcome by local_districts' rules where they need no further source (settled earlier; doubled; the write-in rule;
     held at a gap of 5% or more, noted under it: 21:26 and 19:04). The build does not read this file yet: the
     outcomes are put to the orchestrator first, since holding or noting a Klarner record on a third party's count is
     a step the rules of section 32 took for MEDSL alone.

Counting: each line's 'total' vote type (every line of every file has one [measured]); a contest's votes are those of
its deepest reporting units (a county, or a state's other subdivision), where a file also gives the jurisdiction's own
line for the contest; non-votes ("Over Votes", "Under Votes", "Total Votes Cast", "None Of These Candidates") are left
out, write-in totals kept as write-in lines.

Run:  VOTE_CACHE=/tmp/vote-cache python3 -I pipeline/local_singer.py normalize
      VOTE_CACHE=/tmp/vote-cache python3 -I pipeline/local_singer.py gate      (prints; check writes it)
      VOTE_CACHE=/tmp/vote-cache python3 -I pipeline/local_singer.py check     (writes data/local/check-2020-singer.json)
"""
import collections
import csv
import glob
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fetch as F  # noqa: E402

REPO = os.path.dirname(HERE)
BASE = os.path.join(F.CACHE, "singer2020")
RAW = os.path.join(BASE, "raw")
UNZ = os.path.join(BASE, "unzipped")
NORM = os.path.join(BASE, "normalized")
OUT = os.path.join(REPO, "data", "local", "check-2020-singer.json")
YEAR = 2020
GATE_LINE = 0.005
SOURCE = {"name": "Stephanie Frank Singer, US 2020 General Official Election Results in Tabular Format, Harvard "
                  "Dataverse doi:10.7910/DVN/RV80FW, v1.0, released 2021-08-27",
          "url": "https://doi.org/10.7910/DVN/RV80FW", "licence": "CC0 1.0", "mark": "stated",
          "via": "rolled up to the county level from the State, District or Territory Boards of Election's files or "
                 "pages (its description); a third party's compilation"}
NOT_VOTES = re.compile(r"^(OVER ?VOTES?|UNDER ?VOTES?(\.\d+)?|TOTAL VOTES CAST|NONE OF THESE CANDIDATES|BLANKS?|"
                       r"VOIDS?)$", re.I)
WRITE_IN_TOTAL = re.compile(r"^(WRITE[- ]?INS?( \(MISCELLANEOUS\))?|OTHER WRITE-INS|SCATTER(ING)?|ALL OTHERS|MISC\.?)$",
                            re.I)   # "Misc.": Oregon's write-ins, as its own results name them [inferred]
WRITE_IN = re.compile(r"\(WRITE[- ]?IN\)|\(WRITE IN\)|^WRITE-IN - ", re.I)
LEG = re.compile(r"^([A-Z]{2}) (House|Senate) District (.+?)(?: Position (\d+))?$")
DEM = re.compile(r"^DEMOCRATIC( PARTY)?$|^DEMOCRATIC-FARMER-LABOR( PARTY)?$|^DEM$", re.I)
REP = re.compile(r"^REPUBLICAN( PARTY)?$|^REP$", re.I)


# ------------------------------------------------------------------ the files

def _record():
    with open(os.path.join(RAW, "RV80FW-dataset.json")) as f:
        return json.load(f)["data"]


def _meta(name):
    with open(os.path.join(RAW, name + ".meta.json")) as f:
        return json.load(f)


def normalize():
    """Every file's md5 against the record, then each contest's candidates (by name and party line) with their
    votes, written to $VOTE_CACHE/singer2020/normalized/contests-2020.json."""
    rec = _record()["latestVersion"]
    want = {f["dataFile"]["originalFileName"]: f["dataFile"]["md5"] for f in rec["files"]}
    csv.field_size_limit(10 ** 8)
    out, checks = {}, {"files": {}, "both_levels": [], "rolled_up": {}, "preliminary_rows": collections.Counter()}
    for name, md5 in sorted(want.items()):
        path = os.path.join(UNZ, name)
        with open(path, "rb") as f:
            raw = f.read()
        if hashlib.md5(raw).hexdigest() != md5:
            raise SystemExit(f"{name}: md5 differs from the dataset's record")
        st = name[:2]
        lines = collections.defaultdict(lambda: collections.defaultdict(int))   # (contest, sel, party) -> unit -> n
        depth = collections.defaultdict(set)
        rows = 0
        with open(path, encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                rows += 1
                if row["VoteType"] != "total":
                    continue
                if row["Preliminary"] == "True":
                    checks["preliminary_rows"][f"{st} {row['Contest']}"] += 1
                unit = row["ReportingUnit"]
                lines[(row["Contest"], row["Selection"].strip(), row["Party"].strip())][unit] += int(row["Count"])
                depth[row["Contest"]].add(unit.count(";"))
        contests = collections.defaultdict(list)
        for (contest, sel, party), units in lines.items():
            deep = max(depth[contest])
            v = sum(n for u, n in units.items() if u.count(";") == deep)
            top = sum(n for u, n in units.items() if u.count(";") < deep)
            if top and top != v:   # a line of the jurisdiction's own (Maine's UOCAVA ballots, Alaska's FWAB,
                # Rhode Island's federal-only absentee ballots): votes counted centrally, in no county, so added
                checks["both_levels"].append([st, contest, sel, top, v])
                v += top
            elif top:              # a roll-up of the deeper units, equal to their sum: not added again
                checks["rolled_up"][st] = checks["rolled_up"].get(st, 0) + 1
            contests[contest].append({"name": sel, "party": party, "votes": v,
                                      "units": len([u for u in units if u.count(";") == deep])})
        out[st] = dict(sorted(contests.items()))
        checks["files"][name] = {"rows": rows, "contests": len(contests), "md5": md5}
    os.makedirs(NORM, exist_ok=True)
    checks["preliminary_rows"] = dict(sorted(checks["preliminary_rows"].items()))
    with open(os.path.join(NORM, "contests-2020.json"), "w") as f:
        json.dump({"contests": out, "checks": checks}, f)
    print(f"normalized {len(out)} jurisdictions, {sum(len(v) for v in out.values())} contests; "
          f"both levels differ in {len(checks['both_levels'])} lines; preliminary rows in "
          f"{len(checks['preliminary_rows'])} contests")


def load():
    with open(os.path.join(NORM, "contests-2020.json")) as f:
        return json.load(f)


SUFFIX = re.compile(r",\s*(JR|SR|II|III|IV|V)\.?$", re.I)


def person_name(st, name, leg=True):
    """A candidate's name as local_medsl.name_key reads it: a suffix after a comma ("Fred W. Thiele, Jr.") moved
    before it, as local_districts._first_last does; Alaska's file writes 'Last First M.' ("Quist Christopher",
    "Stein-Olson Monica L.") with no comma, so its first word is the surname and is moved to the end [measured]."""
    n = SUFFIX.sub(lambda m: " " + m.group(1), name.strip())
    if leg and st == "AK" and "," not in n and not WRITE_IN_TOTAL.match(n) and not NOT_VOTES.match(n):
        t = n.split()
        n = " ".join(t[1:] + t[:1])
    return n


def _surnames(st, name, leg=True):
    import local_medsl as M
    return {k[0] for k in M.name_keys(person_name(st, name, leg))}


def _side(party):
    p = (party or "").strip()
    return "D" if DEM.match(p) else "R" if REP.match(p) else None


def _person(x):
    return not NOT_VOTES.match(x["name"]) and not WRITE_IN_TOTAL.match(x["name"])


def _cert_side(cands):
    """{D: (surname, votes), R: ...}: the certified count's one Democrat and one Republican."""
    import local_in as LI
    import local_medsl as M
    out = {}
    for side in ("D", "R"):
        v = [x for x in cands if LI._major((x.get("party") or "").split("/")[-1]) == side or
             LI._major(x.get("party")) == side]
        if len(v) == 1:
            out[side] = (M.name_key(v[0]["name"])[0], v[0]["votes"])
    return out


def _by_name(st, cands, surname, side):
    """(votes, how): Singer's candidate of the certified one's surname, every line of the name added up (a fusion
    candidate's every line, as the certified counts give it), where exactly one name has it; by name first, since
    Nebraska's and South Dakota's files give no party ("none or unknown") [measured]. Else the one name on that side's
    party line: a ticket written whole ("Joseph R Biden | Kamala D Harris", South Carolina), a name spelt otherwise in
    one of the two ("Leo Valentin", D2's "Tilllis"). (None, why) where neither finds one."""
    names = {x["name"] for x in cands if _person(x) and (surname in _surnames(st, x["name"], False)
                                                         or surname in _surnames(st, x["name"], True))}
    if len(names) == 1:
        return sum(x["votes"] for x in cands if x["name"] in names), "by name"
    names = {x["name"] for x in cands if _person(x) and _side(x["party"]) == side}
    if len(names) == 1:
        return sum(x["votes"] for x in cands if x["name"] in names), f"by party line ({sorted(names)[0]})"
    return None, f"no one name {surname} in Singer's, nor one {side} line"


# ------------------------------------------------------------------ gate 1: the federal counts

def gate(data=None):
    """{state: {worst, lines}}: Singer's D and R votes for president, US Senate and each US House district against
    D1's and D2's certified 2020 counts (data/president, senate, house/2020.json), the worst relative miss."""
    data = data or load()
    cert = {}
    for level in ("president", "senate", "house"):
        with open(os.path.join(REPO, "data", level, f"{YEAR}.json")) as f:
            cert[level] = [c for c in json.load(f)["contests"] if not c.get("special")]
    out = {}
    for st, contests in sorted(data["contests"].items()):
        lines, worst = [], 0.0
        for level in ("president", "senate", "house"):
            for c in cert[level]:
                if c["place"]["state"] != st or (level == "president" and c["place"].get("district")):
                    continue   # Maine's and Nebraska's districts for president: Singer's file is statewide
                if level == "president":
                    name = [k for k in contests if re.match(r"^US President", k)]
                elif level == "senate":
                    name = [k for k in contests if re.match(rf"^US Senate {st}$", k)]
                else:
                    d = c["place"]["district"]
                    dn = "1" if d in ("AL", "0", None) else str(int(d))
                    name = [k for k in contests if re.match(rf"^US House {st} District {dn}$", k)] or \
                           ([k for k in contests if re.match(rf"^US House {st}( At-Large| District AL)?$", k)]
                            if d in ("AL", "0", None) else [])
                if len(name) != 1:
                    lines.append([level, c["place"].get("district"), "not in Singer's file" if not name else
                                  "several contests"])
                    continue
                b = _cert_side(c["result"]["candidates"])
                for side, (sur, bv) in sorted(b.items()):
                    av, how = _by_name(st, contests[name[0]], sur, side)
                    if av is None:
                        lines.append([level, c["place"].get("district"), side, how])
                    elif bv:
                        miss = abs(av - bv) / bv
                        worst = max(worst, miss)
                        lines.append([level, c["place"].get("district"), side, av, bv, round(miss, 6), how])
        tested = [x for x in lines if len(x) == 7]
        out[st] = {"worst": round(worst, 6) if tested else None, "tested": len(tested),
                   "passes": bool(tested) and worst <= GATE_LINE, "lines": lines}
    return out


# ------------------------------------------------------------------ gate 2: section 32's district checks

def legislative(data, passed):
    """Singer's state legislative contests of the states that pass gate 1, in local_districts' MEDSL shape."""
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
                ls.append({"name": nm if not WRITE_IN_TOTAL.match(x["name"]) else "WRITE-IN", "votes": x["votes"],
                           "party": x["party"], "writein": wi or bool(WRITE_IN_TOTAL.match(x["name"]))})
            import local_districts as LD
            pool[(st, 1 if m.group(2) == "Senate" else 0)].append(
                {"state": st, "sen": 1 if m.group(2) == "Senate" else 0, "district": m.group(3),
                 "counties": [], "candidates": LD._merge_lines(ls), "file": f"{st}_tabular.tsv", "stage": "GEN",
                 "post": m.group(4), "magnitude": None, "contest": name})
    return pool


def outcome(kc, t):
    """local_districts.outcome's rules that need no further source: settled earlier, doubled, the write-in rule, held
    at 5% or more, noted under it."""
    import local_districts as LD
    src = (kc.get("votes_source") or {}).get("source")
    if src:
        return {"outcome": "settled earlier", "by": src}
    if kc.get("held_reason"):
        return {"outcome": "settled earlier", "by": "held"}
    r = t["ratio"]
    ballot_others = [x for x in t["others"] if not x["write_in"]]
    voted = [p for p in t["pairs"] if p[1]]
    if t["flag_a"] and r is not None and len(voted) >= 2 and not ballot_others and \
            all(abs(p[3] / p[1] - 0.5) <= 0.5 * LD.DOUBLE_TOL for p in voted):
        return {"outcome": "Klarner's figures doubled (Singer's at half)"}
    gaps = [abs(r - 1)] if t["flag_a"] else []
    if t["flag_b"] and ballot_others:
        tot = t["medsl"] + sum(x["votes"] for x in t["others"])
        gaps.append(sum(x["votes"] for x in ballot_others) / tot if tot else 1.0)
    if not gaps:
        return {"outcome": "write-in rule"}
    g = max(gaps)
    return {"outcome": "held" if g >= LD.HOLD_GAP else "noted", "gap": round(g, 5)}


def check():
    import local as L
    import local_districts as LD
    data = load()
    g = gate(data)
    passed = {st for st, v in g.items() if v["passes"]}
    cs = L.load_klarner(raw=True)
    cs = L.c38(L.nh_2022(L.certified_votes(cs)))
    pool = legislative(data, passed)
    states = {k[0] for k in pool}
    tallies, flags, found = collections.Counter(), [], []
    untested_states, unmatched = collections.Counter(), collections.Counter()
    for kc in cs:
        if kc["year"] != YEAR or kc["etype"] != "g":
            continue
        if kc["state"] not in states:
            untested_states[kc["state"]] += 1
            continue
        hits = LD.match(kc, pool)
        if len(hits) != 1:
            tallies["unmatched" if not hits else "matched to several"] += 1
            unmatched[kc["state"]] += 1
            continue
        found.append((kc, hits[0]))
    groups = collections.defaultdict(list)
    for kc, m in found:
        groups[id(m)].append(kc)
    for kc, m in found:
        pr, b_test = None, True
        if len(groups[id(m)]) > 1:
            prs = [LD.pair(k_, m) for k_ in groups[id(m)]]
            lines = [id(x) for p_ in prs if p_ for x in p_.values()]
            if any(p_ is None for p_ in prs) or len(lines) != len(set(lines)):
                tallies["a Singer contest that several districts match, not paired apart"] += 1
                continue
            pr, b_test = prs[groups[id(m)].index(kc)], False
            tallies["shared: (a) only"] += 1
        t = LD.test(kc, m, pr, b_test)
        if not t["matched"]:
            tallies["candidates not paired"] += 1
            continue
        tallies["tested"] += 1
        if not (t["flag_a"] or t["flag_b"]):
            continue
        t["singer"] = t.pop("medsl")
        t["singer_write_ins"] = t.pop("medsl_write_ins")
        t["singer_ballot_unpaired"] = t.pop("medsl_ballot_unpaired")
        t["medsl"] = t["singer"]   # outcome() reads the second count under local_districts' key
        f = {"id": LD.klarner_id(kc), "state": kc["state"], "chamber": "state-upper" if kc["sen"] else "state-lower",
             "dname": kc["dname"] or None, "dno": kc["dno"] or None, "eseats": kc["eseats"],
             "singer_contest": m["contest"], "flags": [x for x, y in (("a", t["flag_a"]), ("b", t["flag_b"])) if y]}
        f.update(outcome(kc, t))
        del t["medsl"]
        f.update(t)
        flags.append(f)
        tallies[f"flag {'+'.join(f['flags'])}: {f['outcome']}"] += 1
    out = {"about": "Klarner's 2020 legislative districts beside Singer's 2020 official results, one by one "
                    "(pipeline/local_singer.py; the orchestrator, 2026-11-13 09:23 and 10:33; data/local/REPORT.md "
                    "section 39). The build does not read it yet: the flags' outcomes await the orchestrator.",
           "source": dict(SOURCE, read_utc=_meta("RV80FW-original.zip")["read_utc"],
                          sha256=_meta("RV80FW-original.zip")["sha256"],
                          record_read_utc=_meta("RV80FW-dataset.json")["read_utc"]),
           "rules": {"gate_line": GATE_LINE, "ratio_off_over": LD.RATIO_OFF, "held_at_or_over": LD.HOLD_GAP,
                     "doubled_within": LD.DOUBLE_TOL},
           "gate": g, "states_passed": sorted(passed),
           "states_failed": sorted(st for st, v in g.items() if v["tested"] and not v["passes"]),
           "klarner_2020_contests_not_tested_by_state": dict(sorted(untested_states.items())),
           "tallies": dict(sorted(tallies.items())),
           "unmatched_by_state": dict(sorted(unmatched.items())),
           "normalize_checks": {k: v for k, v in data["checks"].items() if k != "files"},
           "flags": sorted(flags, key=lambda f: (f["state"], f["chamber"], f["id"]))}
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    print("passed", len(passed), "failed", out["states_failed"])
    print(dict(sorted(tallies.items())))


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "normalize":
        normalize()
    elif cmd == "gate":
        for st, v in gate().items():
            print(st, v["worst"], v["tested"], v["passes"], [x for x in v["lines"] if len(x) != 7 or x[5] > GATE_LINE
                                                             or x[6] != "by name"][:5])
    elif cmd == "check":
        check()
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
