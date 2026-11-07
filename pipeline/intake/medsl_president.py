"""Intake: MIT Election Data and Science Lab, "U.S. President 1976-2024", state returns (CC0 1.0).

Written 2026-11-07 by worker D1 (briefs/D1-data-president.md; plan/PLAN.md section 3a).

Source: Harvard Dataverse doi:10.7910/DVN/42MVDX, file 1976-2024-president.csv (datafile 13887042),
read through Dataverse's documented access API. Licence CC0 1.0 (the dataset's licence field). MEDSL's
own list of where each state's figures came from, sources-president.tab (datafile 4304791), is fetched
beside it. MEDSL compiles state election offices' returns; its codebook names the Clerk of the House's
Statistics as a source (research/decisiveness-models-v2.md section 3.5).

What it writes: data/president/inputs/medsl_president.json, for every year and state: each named
candidate's votes summed over the party lines the candidate ran on (New York's fusion lines, for
example), the Democratic and Republican nominees, the leading two candidates, and MEDSL's totalvotes.
Rows that are not a candidate (blank, void, over- and undervotes, scattering, "other", none of these)
are kept apart under "not_candidates" and never ranked.

Checks (the script stops if one fails):
  - the file's MD5 equals the one Dataverse publishes for it;
  - 13 elections, 51 jurisdictions (50 states and DC) in each;
  - in every state-year the rows sum to totalvotes, except where MEDSL's totalvotes is known to be
    defined otherwise (listed in KNOWN_TOTAL_GAPS with the size of the gap, so a change is caught);
  - national sums of the two nominees' votes against MEDSL's own national totals as computed here
    (printed, for comparison with the FEC in pipeline/intake/fec_president.py).

Run from the repository root:  python3 pipeline/intake/medsl_president.py
"""
import collections
import csv
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import fetch  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "data", "president", "inputs", "medsl_president.json")

DATA_URL = "https://dataverse.harvard.edu/api/access/datafile/13887042"
DATA_NAME = "medsl_42MVDX_1976-2024-president.csv"
DATA_MD5 = "405af83db7625cb35d8c19a5ebe029ff"       # Dataverse's published checksum for datafile 13887042
SOURCES_URL = "https://dataverse.harvard.edu/api/access/datafile/4304791?format=original"
SOURCES_NAME = "medsl_42MVDX_sources-president.csv"

NOT_CANDIDATES = {"", "SCATTERING", "OTHER", "OTHERS", "BLANK VOTE/SCATTERING", "NONE OF THE ABOVE",
                  "BLANK VOTE", "NONE OF THESE CANDIDATES", "OVER VOTE", "BLANK VOTE/VOID VOTE/SCATTERING",
                  "VOID VOTE", "BLANK VOTES", "OVERVOTES", "UNDERVOTES", "VOID", "WRITE-IN", "SPOILED"}
# state-years where the rows do not sum to totalvotes, measured 2026-11-07 (rows minus totalvotes)
KNOWN_TOTAL_GAPS = {("2024", "DC"): 2535, ("2024", "NY"): -874}
YEARS = [str(y) for y in range(1976, 2025, 4)]


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    path = fetch.fetch(DATA_URL, DATA_NAME, storage_sites=("amazonaws.com",))
    fetch.fetch(SOURCES_URL, SOURCES_NAME, storage_sites=("amazonaws.com",))
    assert md5(path) == DATA_MD5, "the file is not the one Dataverse publishes as datafile 13887042"
    rows = list(csv.DictReader(open(path, encoding="utf-8-sig")))

    by = collections.defaultdict(list)
    for r in rows:
        by[(r["year"], r["state_po"])].append(r)
    years = sorted({y for y, _ in by})
    assert years == YEARS, years
    for y in years:
        assert len([1 for (yy, _) in by if yy == y]) == 51, y

    out = {}
    for (y, st), rs in sorted(by.items()):
        total = int(rs[0]["totalvotes"])
        assert all(int(r["totalvotes"]) == total for r in rs), (y, st)
        gap = sum(int(r["candidatevotes"]) for r in rs) - total
        assert gap == KNOWN_TOTAL_GAPS.get((y, st), 0), (y, st, gap)
        cands = collections.OrderedDict()
        others = collections.Counter()
        for r in rs:
            name = r["candidate"].strip()
            v = int(r["candidatevotes"])
            if name.upper() in NOT_CANDIDATES:
                others[name or "(blank name)"] += v
                continue
            c = cands.setdefault(name, {"name": name, "votes": 0, "lines": [], "parties": set(),
                                        "writein": True})
            c["votes"] += v
            c["lines"].append({"party_detailed": r["party_detailed"], "votes": v})
            c["parties"].add(r["party_simplified"])
            c["writein"] = c["writein"] and r["writein"] == "True"   # write-in only if every line is
        ranked = sorted(cands.values(), key=lambda c: -c["votes"])
        for c in ranked:
            c["parties"] = sorted(p for p in c["parties"] if p)

        def nominee(party):
            # the party's leading candidate (MEDSL marks every 2020 DC row a write-in, so the flag is not used)
            m = [c for c in ranked if party in c["parties"]]
            return {"name": m[0]["name"], "votes": m[0]["votes"]} if m else None

        out.setdefault(y, {})[st] = {
            "state": rs[0]["state"].title(), "totalvotes": total,
            "dem": nominee("DEMOCRAT"), "rep": nominee("REPUBLICAN"),
            "top_two": [{"name": c["name"], "votes": c["votes"], "parties": c["parties"]} for c in ranked[:2]],
            # the party lines are kept only where a candidate ran on more than one (fusion), to keep the file small
            "candidates": [dict({"name": c["name"], "votes": c["votes"], "parties": c["parties"],
                                 "writein": c["writein"]}, **({"lines": c["lines"]} if len(c["lines"]) > 1 else {}))
                           for c in ranked],
            "not_candidates": dict(others),
            "medsl_version": rs[0]["version"],
        }

    m = fetch.meta(DATA_NAME)
    ms = fetch.meta(SOURCES_NAME)
    doc = {
        "about": "MEDSL state presidential returns, normalised by pipeline/intake/medsl_president.py. "
                 "Votes per candidate are summed over the party lines the candidate ran on.",
        "source": fetch.source("MIT Election Data and Science Lab, U.S. President 1976-2024, "
                               "Harvard Dataverse doi:10.7910/DVN/42MVDX, file 1976-2024-president.csv",
                               DATA_URL, m["read_utc"], "CC0 1.0", "stated",
                               via="MEDSL's compilation of state election offices' returns",
                               note="checked against Dataverse's MD5 " + DATA_MD5, sha256=m["sha256"]),
        "state_sources": fetch.source("MEDSL, sources-president.tab: where MEDSL took each state's figures",
                                      SOURCES_URL, ms["read_utc"], "CC0 1.0", "stated", sha256=ms["sha256"]),
        "known_total_gaps": {f"{y} {s}": g for (y, s), g in KNOWN_TOTAL_GAPS.items()},
        "years": out,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(doc, f, indent=1, sort_keys=False)
        f.write("\n")
    for y in years:
        d = sum(out[y][s]["dem"]["votes"] for s in out[y])
        r = sum(out[y][s]["rep"]["votes"] for s in out[y])
        t = sum(out[y][s]["totalvotes"] for s in out[y])
        odd = [s for s in out[y] if {c["name"] for c in out[y][s]["top_two"]} != {out[y][s]["dem"]["name"], out[y][s]["rep"]["name"]}]
        print(f"{y}: 51 jurisdictions; Democratic {d:,}, Republican {r:,}, totalvotes {t:,};"
              f" leading two not the two nominees in: {', '.join(odd) or 'none'}")
    print(f"wrote {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
