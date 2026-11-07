"""pipeline/local_in.py: Indiana's certified 2024 general election (pipeline/intake/in_enr.py), gated against the
certified federal counts, compared with MEDSL's Indiana file, and put in the shape pipeline/local_medsl.py reads.

Written 2026-11-07 by worker D3 (briefs/D3-data-local.md, step 2) at the orchestrator's order of 08:08 ("For the 2024
legislatures of IN, LA and NJ, read each state's own certified results where a file is reachable by script, with a
gate against D2's federal counts on the same dates as for North Carolina") and its go-ahead of 08:32 ("Indiana's
certified archive is a good source").

Why: MEDSL's 2024 Indiana file falls short of D1's certified presidential count, so its Indiana contests are held
back (no p; data/local/REPORT.md section 6). Where two sources hold one contest the certified one wins (brief D3,
step 2). So, if the state's file passes the gate, local_medsl.load(2024) reads Indiana's legislature, local races and
questions from it in place of MEDSL's (certified_in there), with MEDSL's routes and checks; the presidency, Congress
and the governor stay D1's and D2's.

  gate()         the file's Democratic and Republican votes for president (D1's data/president/2024.json), the
                 Senate and each House district (D2's data/senate and data/house) against the certified ones:
                 (worst relative miss, words); the line is local_medsl.QUALITY_LINE, as for North Carolina.
  check()        the gate, and MEDSL's Indiana contests against the state's, by legislative district and by
                 local contest (the same names and votes): data/local/check-in.json.
  medsl_shape()  the state's contests (not federal, not the governor) in local_medsl's load() shape, or None if
                 the file is missing or fails the gate.

Run:  VOTE_CACHE=/tmp/vote-cache python3 pipeline/local_in.py check
"""
import argparse
import collections
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fetch as F  # noqa: E402
from intake import in_enr as ENR  # noqa: E402
import local as L  # noqa: E402
import local_medsl as LM  # noqa: E402

ELECTION = "2024General"
SOURCE_KEY = "in_enr"
PARTY = {"D": "DEMOCRAT", "R": "REPUBLICAN", "L": "LIBERTARIAN", "I": "INDEPENDENT", "": "NONPARTISAN"}
LEG = {"State Senator": "STATE SENATE", "State Representative": "STATE HOUSE"}
SKIP = {"Presidential Electors for US President & VP", "US Senator", "US Representative", "Governor & Lt. Governor"}
STATEWIDE_Q = {"Ratification Of State Constitutional Amendment", "Supreme Court Justice Retention",
               "Court Of Appeals Judge Retention"}
N_COUNTIES = 92


def load(election=ELECTION):
    path = os.path.join(ENR.NORM, f"{election}.jsonl")
    if not os.path.exists(path):
        raise SystemExit(f"Indiana's {election} file is not in the cache: run pipeline/intake/in_enr.py fetch and read")
    with open(path) as f:
        return [json.loads(line) for line in f]


def checks_of(election=ELECTION):
    with open(os.path.join(ENR.NORM, f"checks-{election}.json")) as f:
        return json.load(f)


def _major(party):
    p = (party or "").upper()
    return "D" if p in ("D", "DEM", "DEMOCRAT", "DEMOCRATIC") else "R" if p in ("R", "REP", "REPUBLICAN") else None


_ORD = {w: i + 1 for i, w in enumerate("First Second Third Fourth Fifth Sixth Seventh Eighth Ninth Tenth".split())}


def _dist(title):
    """The district number of a title: 'State Senator, District 001', 'United States Representative, First
    District'."""
    m = re.search(r"District\s+0*(\d+)", title or "")
    if m:
        return int(m.group(1))
    m = re.search(r"\b(" + "|".join(_ORD) + r") District\b", title or "")
    return _ORD[m.group(1)] if m else None


def gate(cs=None):
    """(worst relative miss, words) of the file's D and R votes against D1's and D2's certified 2024 counts."""
    cs = cs or load()
    worst, what = 0.0, []
    for cat, level in (("Presidential Electors for US President & VP", "president"), ("US Senator", "senate"),
                       ("US Representative", "house")):
        mine = [c for c in cs if c.get("category") == cat]
        with open(os.path.join(L.REPO, "data", level, "2024.json")) as f:
            cert = [x for x in json.load(f)["contests"] if x["place"]["state"] == "IN" and not x.get("special")]
        if level == "house":
            byd = {int(x["place"]["district"]): x for x in cert}
            pairs = [([c], [byd[_dist(c["title"])]]) for c in mine if _dist(c["title"]) in byd]
        else:
            pairs = [(mine, cert)]
        for side in ("D", "R"):
            a = sum(x["votes"] for m_, _ in pairs for c in m_ for x in c["candidates"] if _major(x["party"]) == side)
            b = sum(x["votes"] for _, c_ in pairs for c in c_ for x in c["result"]["candidates"]
                    if _major(x.get("party")) == side)
            if not b:
                continue
            what.append(f"{level} {side} {a:,} against {b:,}" + (f" ({len(pairs)} districts)" if level == "house" else ""))
            for m_, c_ in pairs:
                aa = sum(x["votes"] for c in m_ for x in c["candidates"] if _major(x["party"]) == side)
                bb = sum(x["votes"] for c in c_ for x in c["result"]["candidates"] if _major(x.get("party")) == side)
                if bb:
                    worst = max(worst, abs(aa - bb) / bb)
    return worst, "; ".join(what)


def medsl_shape(year=2024):
    """Indiana's 2024 contests, not federal and not the governor, in local_medsl's load() shape; None if the file is
    missing, not marked certified, or fails the gate."""
    if year != 2024 or not os.path.exists(os.path.join(ENR.NORM, f"{ELECTION}.jsonl")):
        return None
    cs = load()
    meta = checks_of()
    if meta.get("certified") != "T" or gate(cs)[0] > LM.QUALITY_LINE:
        return None
    out = []
    for c in cs:
        base = {"state": "IN", "date": c["date"], "stage": "GEN", "special": False, "subject": None, "precincts": None,
                "counties": c["counties"], "source": SOURCE_KEY,
                "file": {"name": c.get("file") or "JurR_<FIPS>_A.json", "url": meta["source"]["url"],
                         "read_utc": meta["source"]["read_utc"]}}
        if c["kind"] == "question":
            statewide = c["type"] in STATEWIDE_Q and len(c["counties"]) == N_COUNTIES
            out.append(dict(base, dataverse="STATE" if statewide else "LOCAL", office=c["title"].upper(),
                            district="STATEWIDE" if statewide else "", subject=c["text"], magnitude=None,
                            question=True, question_type=c["type"],
                            candidates=[{"name": "YES", "votes": c["yes"]}, {"name": "NO", "votes": c["no"]}]))
            continue
        if c["category"] in SKIP:
            continue
        cands = [{"name": x["name"], "votes": x["votes"], "as_named": True,
                  "party": PARTY.get(x["party"], x["party"])} for x in c["candidates"]]
        if c["category"] in LEG:
            d = _dist(c["title"])
            out.append(dict(base, dataverse="STATE", office=LEG[c["category"]], district=f"{d:02d}" if d else "",
                            magnitude=c["seats"], question=False, candidates=cands))
        else:
            statewide = c["heading"] == "State" and len(c["counties"]) == N_COUNTIES
            office = c["title"].upper()
            for pl in c.get("places") or []:   # a title that does not name its place ("School Board Member,
                if pl.upper() not in office:   # District") takes the district's name from its jurisdiction
                    office += f" - {pl.upper()}"
            out.append(dict(base, dataverse="STATE" if c["heading"] == "State" else "LOCAL", office=office,
                            district="STATEWIDE" if statewide else "", magnitude=c["seats"], question=False,
                            candidates=cands))
    return out


def source_block():
    meta = checks_of()
    return F.source("Indiana Election Division, Indiana Election Results, November 2024 General Election (the "
                    "results site's archive)", meta["source"]["url"], meta["source"]["read_utc"], ENR.LICENCE,
                    mark="stated",
                    note=f"the state's results files, marked certified in its settings ('Certified': "
                         f"'{meta['certified']}'); {meta['files']} JSON files, {meta['bytes']:,} bytes besides the "
                         f"three index files, read by pipeline/intake/in_enr.py; the site lists no write-in totals")


def _sig(cands):
    return tuple(sorted((x["votes"] for x in cands if not LM._is_generic(x["name"]) and not x.get("writein")),
                        reverse=True))


def check():
    cs = load()
    w, words = gate(cs)
    out = {"about": "Indiana's certified 2024 general election (pipeline/intake/in_enr.py), compared with the "
                    "sources already in data/. Built by pipeline/local_in.py check.",
           "certified_flag": checks_of().get("certified"),
           "gate": {"worst_miss": round(w, 6), "fails": w > LM.QUALITY_LINE, "counts": words},
           "contests": collections.Counter(), "legislature_medsl": {}, "local_medsl": {}, "questions_medsl": {}}
    for c in cs:
        out["contests"][c["kind"] + ": " + (c.get("category") or c.get("type"))] += 1
    med = []
    for p in glob.glob(os.path.join(LM.NORM, "2024", "IN-*.jsonl")):
        with open(p) as f:
            med += [x for x in (json.loads(ln) for ln in f) if "state" in x]
    # the legislature, district by district (MEDSL splits some districts into pieces)
    mine = {(LEG[c["category"]], _dist(c["title"])): c for c in cs if c.get("category") in LEG}
    t, diffs = collections.Counter(), []
    pieces = collections.defaultdict(list)
    for m in med:
        if m["office"] in LM.LEG and not m["question"] and m["stage"] == "GEN" and not m["special"]:
            pieces[(m["office"], int(LM.district_no(m["district"]) or 0))].append(m)
    for key, c in sorted(mine.items()):
        ms = pieces.get(key)
        if not ms:
            t["not in MEDSL's file"] += 1
            continue
        if len(ms) > 1:
            t["MEDSL splits the district into pieces"] += 1
        a = _sig(c["candidates"])
        tot = collections.Counter()
        for m in ms:
            for x in m["candidates"]:
                if not LM._is_generic(x["name"]) and not x.get("writein"):
                    tot[LM.name_key(x["name"])] += x["votes"]
        b = tuple(sorted(tot.values(), reverse=True))
        if a == b:
            t["equal"] += 1
        else:
            t["differ"] += 1
            diffs.append({"district": f"{key[0].lower()} {key[1]}", "state": list(a), "medsl": list(b),
                          "largest_difference": max((abs(x - y) for x, y in zip(a, b)), default=None),
                          "share_short": round(1 - sum(b) / sum(a), 4) if sum(a) else None})
    out["legislature_medsl"] = {"tally": dict(t), "differences": sorted(diffs, key=lambda x: -(x["share_short"] or 0))}
    # local races: MEDSL's contest found in the state's by its candidates' names
    st_by_name = collections.defaultdict(list)
    for c in cs:
        if c["kind"] == "office" and c["category"] not in SKIP and c["category"] not in LEG:
            st_by_name[frozenset(LM.name_key(x["name"]) for x in c["candidates"])].append(c)
    t, diffs = collections.Counter(), []
    for m in med:
        if m["question"] or m["office"] in LM.LEG or LM.GOVERNOR.match(m["office"]) or m["dataverse"] == "FEDERAL" \
                or m["office"] in ("US PRESIDENT", "US SENATE", "US HOUSE", "PRESIDENT"):
            continue
        names = frozenset(LM.name_key(x["name"]) for x in m["candidates"] if not LM._is_generic(x["name"])
                          and not x.get("writein"))
        hit = [c for k, v in st_by_name.items() if names and names <= k for c in v]
        if not hit:
            t["not found in the state's file"] += 1
            continue
        if any(_sig(c["candidates"]) == _sig(m["candidates"]) for c in hit):
            t["equal"] += 1
        else:
            t["differ"] += 1
            if len(diffs) < 60:
                diffs.append({"office": m["office"], "medsl": list(_sig(m["candidates"]))[:4],
                              "state": list(_sig(hit[0]["candidates"]))[:4], "state_title": hit[0]["title"]})
    out["local_medsl"] = {"medsl_contests": sum(t.values()),
                          "state_contests": sum(len(v) for v in st_by_name.values()), "tally": dict(t),
                          "examples": diffs}
    # questions: the statewide amendment and retentions by their totals
    t = collections.Counter()
    ex = []
    sq = [c for c in cs if c["kind"] == "question"]
    for m in med:
        if not m["question"]:
            continue
        y, n = LM.yes_no(m)
        hit = [c for c in sq if (c["yes"], c["no"]) == (y, n)]
        t["equal" if hit else "not equal to any of the state's"] += 1
        if not hit and len(ex) < 40:
            ex.append({"office": m["office"], "medsl": [y, n], "counties_in_medsl": len(m["counties"])})
    out["questions_medsl"] = {"medsl_questions": sum(t.values()), "state_questions": len(sq), "tally": dict(t),
                              "examples": ex}
    out["contests"] = dict(sorted(out["contests"].items()))
    path = os.path.join(L.REPO, "data", "local", "check-in.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
        f.write("\n")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("what", choices=["check"])
    ap.parse_args()
    out = check()
    print(json.dumps({k: v for k, v in out.items() if k not in ("legislature_medsl", "local_medsl", "questions_medsl")},
                     indent=1))
    for k in ("legislature_medsl", "local_medsl", "questions_medsl"):
        print(k, json.dumps(out[k].get("tally")))


if __name__ == "__main__":
    main()
