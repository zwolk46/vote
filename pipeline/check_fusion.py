"""The fusion scan: every record whose source gives one candidate several party lines, at every level, and whether
the record counts the candidate over every line. Writes data/local/check-fusion.json; changes no record.

Why (the orchestrator, 2026-11-13 04:44): "A fusion candidate's votes are the sum of his lines in the official count,
so one line understates both the candidate and n. ... scan every record whose source gives one candidate several
party lines, at every level (NY and CT first). Send me the count before building beyond the governors."

What is read, by level:
  house, senate      the records (FEC): a party label with "/" is a candidate on several lines, which
                     pipeline/intake/fec_federal_elections.py sums and checks against the FEC's printed
                     "Combined GE party totals".
  governor           the records, with Cha, Kuriwaki and Snyder's party_formal (several parties named) and Algara and
                     Amlani's county returns as a second count of every governor 2006-2020 both hold: a count of one
                     line shows as the record under the second count (as CT and NY 2018 did before
                     pipeline/governor_counts.py).
  state legislatures, local
                     the records from MEDSL's precinct files: result.candidates[].lines holds each line's votes, and
                     the candidate's votes are their sum (checked here); Klarner's returns, one row a candidate and
                     line, summed by candidate id in pipeline/intake/klarner_state_legislative.py (counted here from its
                     cache).
  president          the FEC's tables, which give each nominee's votes over every line (the intake's own words:
                     "summed over the party lines they ran on"); not re-read here.

Run: VOTE_CACHE=... python3 -I pipeline/check_fusion.py
"""
import collections
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch as F  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(REPO, "data")
OUT = os.path.join(DATA, "local", "check-fusion.json")
CHA = os.path.join(F.CACHE, "cha", "normalized", "contests.json")
AA = os.path.join(F.CACHE, "algara_amlani", "normalized", "governors.json")
KLARNER = os.path.join(F.CACHE, "klarner", "normalized", "contests.jsonl")
LINE = 0.005     # the totals check's line (data/congress/check-totals.json): a second count off by more is listed


def _src(r):
    s = (r.get("result") or {}).get("source")
    return (s.get("name") if isinstance(s, dict) else str(s or ""))


def _tally(out, level, source, r, summed):
    t = out.setdefault(level, {}).setdefault(source, {"records": 0, "summed": 0, "one_line": [],
                                                      "by_state": collections.Counter()})
    t["records"] += 1
    t["by_state"][r["place"]["state"]] += 1
    if summed:
        t["summed"] += 1
    else:
        t["one_line"].append(r["id"])


def federal(out):
    for level in ("house", "senate"):
        for p in sorted(glob.glob(os.path.join(DATA, level, "*.json"))):
            with open(p) as f:
                d = json.load(f)
            for r in d.get("contests", []):
                cs = r["result"]["candidates"]
                if any("/" in (c.get("party") or "") for c in cs):
                    # the FEC reader sums the lines and stops where they differ from the printed combined total
                    _tally(out, level, "FEC", r, True)


def legislatures_and_local(out):
    bad = []
    for level in ("state-lower", "state-upper", "local"):
        for p in sorted(glob.glob(os.path.join(DATA, level, "*", "*.json"))):
            with open(p) as f:
                d = json.load(f)
            for r in d.get("contests", []):
                cs = (r.get("result") or {}).get("candidates") or []
                multi = [c for c in cs if isinstance(c.get("lines"), list)
                         and len([x for x in c["lines"] if isinstance(x, dict) and x.get("party")]) > 1]
                if not multi:
                    continue
                ok = all(sum(x.get("votes") or 0 for x in c["lines"]) == c["votes"] for c in multi)
                if not ok:
                    bad.append(r["id"])
                _tally(out, level, "MEDSL", r, ok)
    return bad


def klarner():
    n_c, n_k, by = 0, 0, collections.Counter()
    with open(KLARNER) as f:
        for line in f:
            c = json.loads(line)
            k = sum(1 for a in c["cands"] if len(a.get("lines") or []) > 1)
            if k:
                n_c += 1
                n_k += k
                by[c["state"]] += 1
    return {"source": "Klarner's state legislative returns (pipeline/intake/klarner_state_legislative.py)",
            "how": ("one row a candidate and line in the source; the intake adds a candidate's rows by candidate id "
                    "(a['votes'] += v) and keeps the lines' names in lines, so every record built from them counts "
                    "every line"),
            "contests": n_c, "candidates": n_k, "by_state": dict(by.most_common())}


def governors(out):
    with open(CHA) as f:
        cha = json.load(f)["contests"]
    with open(AA) as f:
        aa = json.load(f)
    recs = {}
    for p in sorted(glob.glob(os.path.join(DATA, "governor", "*.json"))):
        with open(p) as f:
            for r in json.load(f)["contests"]:
                recs[r["id"]] = r
    pf = {}
    for c in cha:
        if c["office"] == "governor":
            pf.setdefault((c["year"], c["state"], bool(c.get("special"))), []).append(c)
    listed = []
    for rid, r in sorted(recs.items()):
        k = (r["year"], r["place"]["state"], bool(r.get("special")))
        cs = pf.get(k) or []
        if len(cs) == 1 and any("," in (a.get("party_formal") or "") for a in cs[0]["candidates"]) \
                and _src(r).startswith("Cha, Kuriwaki and Snyder"):
            _tally(out, "governor", "Cha, Kuriwaki and Snyder (party_formal names the lines, votes summed)", r, True)
        if any(len(c.get("lines") or []) > 1 for c in r["result"]["candidates"]):
            _tally(out, "governor", "the state's count by line (pipeline/governor_counts.py)", r,
                   all(sum(x["votes"] for x in c["lines"]) == c["votes"] for c in r["result"]["candidates"]
                       if c.get("lines")))
    # the second count: Algara and Amlani's two nominees against the record's, every governor both hold
    compared = 0
    for e in aa["elections"]:
        if e["type"] != "G":
            continue
        rid = f"{e['year']}-governor-{e['state']}"
        r = recs.get(rid)
        if r is None or _src(r).startswith("Algara and Amlani") or len(pf.get((e["year"], e["state"], False)) or []) != 1:
            continue
        compared += 1
        rows, worst = [], 0.0
        for p, v in (("D", e["D"]), ("R", e["R"])):
            xs = [c["votes"] for c in r["result"]["candidates"] if (c.get("party") or "")[:1] == p]
            if xs and v:
                off = v / max(xs) - 1
                rows.append({"party": p, "record": max(xs), "algara_amlani": v, "off": round(off, 5)})
                worst = max(worst, abs(off))
        if worst > LINE:
            listed.append({"id": rid, "source": _src(r), "nominees": rows,
                           "algara_amlani_counties_missing": e["counties_missing"]})
    listed.sort(key=lambda t: -max(abs(x["off"]) for x in t["nominees"]))
    return compared, listed


def main():
    out = collections.OrderedDict()
    federal(out)
    gov_compared, gov_listed = governors(out)
    bad = legislatures_and_local(out)
    for lv in out.values():
        for t in lv.values():
            t["by_state"] = dict(t["by_state"].most_common())
    doc = {
        "about": ("the fusion scan (pipeline/check_fusion.py; the orchestrator, 2026-11-13 04:44): by level and "
                  "source, the records with a candidate on several party lines, how many count the candidate over "
                  "every line (summed) and which count one line (one_line); then a second count of every governor "
                  "2006-2020 that Algara and Amlani also hold, since a source that prints one line names one party "
                  "and is found only by a second count (CT and NY 2018, now every line by pipeline/governor_counts.py)"),
        "levels": out,
        "klarner": klarner(),
        "president": ("the FEC's tables give each nominee's votes over every line (pipeline/intake/"
                      "fec_federal_elections.py: 'summed over the party lines they ran on'); the 2024 check of "
                      "MEDSL's precincts against them (local_medsl.quality) is within 0.01% in NY and exact in CT"),
        "lines_not_summing": bad,
        "governor_second_count": {"compared": gov_compared, "line": LINE,
                                  "rule": ("the record's two nominees against Algara and Amlani's county returns "
                                           "summed; listed where either differs by more than the line"),
                                  "listed": gov_listed},
    }
    with open(OUT, "w") as f:
        json.dump(doc, f, indent=1)
        f.write("\n")
    for lvl, v in out.items():
        for s, t in v.items():
            print(f"{lvl} | {s}: {t['records']} records, {t['summed']} summed, one line {t['one_line']}; "
                  f"{list(t['by_state'].items())[:6]}")
    k = doc["klarner"]
    print(f"klarner: {k['contests']} contests, {k['candidates']} candidates; {list(k['by_state'].items())[:6]}")
    print("lines not summing:", bad)
    print(f"governors compared with Algara and Amlani: {gov_compared}, over {LINE:.1%}: {len(gov_listed)}")
    for t in gov_listed:
        print(" ", t["id"], [(x["party"], x["record"], x["algara_amlani"], x["off"]) for x in t["nominees"]])


if __name__ == "__main__":
    main()
