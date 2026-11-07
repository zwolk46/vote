"""pipeline/population_sld.py: the population each state legislative contest's district holds, by D3's contest id.

Written 2026-11-07 by worker D2, on the orchestrator's word of 11:39 UTC. The site divides B* among the people a seat
serves ("to each person"), and D3's state legislative contests carry no population. Reason for a separate file (the
orchestrator): law 8 says every figure comes from a named true source, and a separate file keeps clear of D3's builds.
D3's files are read, never written.

The figures are the Census Bureau's own: the 2020 Census count (POP100) of each state legislative district, as the
Bureau tabulates it to the lines of the election cycle (pipeline/intake/census_sld_population.py: the CD119 summary
file for the 2024 cycle, CD118 for 2022). Nothing is apportioned. A contest gets a figure only where its district is
one the Bureau tabulates, matched by name:
  - a district's name is read as its words and its numbers: "BELKNAP 001" and "Belknap 01" are one district,
    "1ST BRISTOL AND PLYMOUTH" and "Bristolplymouth 1" another ("and", "&" and ordinal endings are dropped, case and
    punctuation ignored). A name that two of the Bureau's districts share is matched to neither;
  - a seat or position of a multi-member district ("DISTRICT 1 SEAT A", "9, position 2", Washington's positions) is
    given its district's figure: every seat of it is elected by the whole district. But where the Bureau tabulates
    lettered subdistricts under that number (South Dakota's 26A and 26B, Minnesota's 10A and 10B, North Dakota's 4A
    and 4B), the seat may be one of them, and no figure is given;
  - a district the Bureau does not tabulate (New Hampshire's floterial districts overlap its base districts, and
    the Bureau's districts cover each block once) gets none, nor a contest whose record names no district.

Lines. The Bureau's 2024 districts are the "2024 election cycle boundaries" every state provided in Phase 4 of its
Redistricting Data Program (CD119 technical documentation, A-21). Where a state's 2024 lines differ from them, its
districts are marked as not given, with the reason (NOT_THE_LINES below). None is known. As a check, each state and
chamber's districts are compared with the Bureau's 2022 districts (CD118), and the file says which changed: on
2026-11-07 they were Georgia, Montana, North Carolina, North Dakota, Ohio, Washington and Wisconsin (both chambers),
New York's Assembly and Michigan's House, and a few districts of Minnesota (both) and South Carolina's House. Every district name in D3's 2024 records is among the Bureau's 2024 districts, but for New Hampshire's 39
highest-numbered districts in their counties, and the contests whose record names no district.

Run from the repository root, after the intake script:  python3 pipeline/population_sld.py [2024] [2022]
Writes data/population/state-legislative-<year>.json.
"""
import collections
import glob
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "intake"))
import congress_common as cc  # noqa: E402
from census_sld_population import STATES  # noqa: E402

ROOT = os.path.dirname(HERE)
PRODUCT = {2024: "cd119", 2022: "cd118"}
CHAMBERS = {"state-upper": "upper", "state-lower": "lower"}
# states whose lines at the year's election differ from the Bureau's districts of that cycle, by year and chamber,
# each with its reason and source; their contests get no figure. None is known (data/README.md, data/population/).
NOT_THE_LINES = {}
# the words around a district's name in the Bureau's names ("Missouri State Senate District 1", "Legislative
# (House) District 9", "Orleans Senatorial District"), dropped with the state's own name before matching
FRAME = {"STATE", "SENATE", "SENATORIAL", "HOUSE", "DISTRICT", "LEGISLATIVE", "ASSEMBLY", "REPRESENTATIVE",
         "DELEGATE", "GENERAL"}
ORDINAL = {"FIRST": "1ST", "SECOND": "2ND", "THIRD": "3RD", "FOURTH": "4TH", "FIFTH": "5TH", "SIXTH": "6TH",
           "SEVENTH": "7TH", "EIGHTH": "8TH", "NINTH": "9TH", "TENTH": "10TH", "ELEVENTH": "11TH", "TWELFTH": "12TH"}


def name_key(s, state=None):
    """A district name as (its letters, its numbers): case, punctuation, "and", "&", ordinal endings, the words of
    FRAME and the state's own name dropped."""
    s = s.upper().replace("&", " AND ").replace("(", " ").replace(")", " ")
    if state:
        s = s.replace(STATES[state].replace("_", " ").upper(), " ")
    s = " ".join(ORDINAL.get(w, w) for w in re.split(r"[\s,]+", s) if w and w not in FRAME)
    s = re.sub(r"\bAND\b", " ", s)
    s = re.sub(r"(?<=\d)(ST|ND|RD|TH)\b", "", s)
    nums = tuple(int(x) for x in re.findall(r"\d+", s))
    letters = re.sub(r"[^A-Z]", "", re.sub(r"\d+", " ", s))
    return letters, nums


SEAT = [re.compile(r"^DISTRICT (\d+) SEAT [A-Z0-9]+$", re.I),        # Idaho, 2024: "DISTRICT 1 SEAT A"
        re.compile(r"^(\d+), (?:seat|position) \d+$", re.I)]         # 2022: "1, seat 2", "26, position 1"


def git_head():
    return subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True,
                          cwd=ROOT).stdout.strip()


def bureau_index(districts, state):
    """{name key: district} over the Bureau's districts of a chamber, leaving out keys two districts share, and
    the set of numbers under which it tabulates lettered subdistricts (26A, 26B -> 26)."""
    by = collections.defaultdict(list)
    lettered = set()
    for d in districts:
        if d["code"] == "ZZZ":
            continue
        k = name_key(d["basename"], state)
        by[k].append(d)
        if len(k[1]) == 1 and len(k[0]) == 1 and re.fullmatch(r"0*\d+[A-Z]", d["code"].strip(), re.I):
            lettered.add(k[1][0])
    return {k: v[0] for k, v in by.items() if len(v) == 1}, {k for k, v in by.items() if len(v) > 1}, lettered


WHY = {"no district": "D3's record names no district",
       "seat": "a seat of a district the Bureau tabulates only as lettered subdistricts",
       "shared": "a name two of the Bureau's districts share",
       "no such district": "no district of that name among the Bureau's",
       "lines": "the state's lines at the election are not the Bureau's"}


def match(c, idx, shared, lettered):
    """(the Bureau's district, note, None) for D3's contest c, or (None, reason, the reason's WHY key)."""
    pl = c["place"]
    dist = pl.get("district")
    if dist is None:
        return None, "D3's record of this contest names no district", "no district"
    seat = None
    for rx in SEAT:
        m = rx.match(dist.strip())
        if m:
            seat, dist = dist, m.group(1)
            break
    if pl.get("position"):
        seat = f"position {pl['position']}"
    k = name_key(dist)
    if seat is not None and k[1] and k[1][0] in lettered and not k[0]:
        return None, (f"a seat ({seat}) of district {dist}, under which the Bureau tabulates lettered subdistricts: "
                      "the seat may be one of them, so no figure is given"), "seat"
    if k in shared:
        return None, f"two of the Bureau's districts share the name {dist!r}", "shared"
    d = idx.get(k)
    if d is None:
        return None, f"the Bureau tabulates no district named {dist!r} in this chamber on these lines", \
            "no such district"
    note = (f"one of the seats of district {d['basename']} ({seat}), every seat of which the whole district elects: "
            "the figure is the district's") if seat else None
    return d, note, None


def build(year):
    product = PRODUCT[year]
    B = cc.read_json(os.path.join(cc.CACHE, "census", "normalized", f"sld_population_{product}.json"))
    prev = cc.read_json(os.path.join(cc.CACHE, "census", "normalized", "sld_population_cd118.json")) \
        if year == 2024 else None
    if not B:
        raise SystemExit(f"run pipeline/intake/census_sld_population.py {product} first")
    reads = sorted(f["read_utc"] for f in B["files"].values())
    src_key = f"census_{product}"
    out = {"about": f"The 2020 Census population of the district each state legislative contest of {year} is held "
                    f"in, by D3's contest id (data/state-upper/{year}, data/state-lower/{year}), as the Census Bureau "
                    f"tabulates it to the state legislative districts of the {year} election cycle. Nothing is "
                    "apportioned: a contest whose district the Bureau does not tabulate gets no figure, with the "
                    "reason. The fields are described in data/README.md (data/population/).",
           "year": year, "written_by": "pipeline/population_sld.py", "commit": git_head(),
           "sources": {src_key: cc.source_block(
               B["title"], "https://www2.census.gov/programs-surveys/decennial/2020/data/" +
               ("119th" if product == "cd119" else "118th") + "-congressional-district-summary-file/",
               reads[-1], B["licence"], mark="stated",
               note=f"one zip per state, its geographic header file read by pipeline/intake/census_sld_population.py "
                    f"(read {reads[0]} to {reads[-1]}); POP100 is the 2020 Census count of 1 April 2020 "
                    f"(\"Population Count (100%)\"); each file's url and sha256 under files. Technical "
                    f"documentation: {B['techdoc']}")},
           "files": {st: {k: f[k] for k in ("url", "sha256", "bytes", "read_utc")} for st, f in B["files"].items()},
           "match_rate": {}, "lines_against_2022": {} if prev else None, "contests": {}}
    for level, ch in CHAMBERS.items():
        for path in sorted(glob.glob(os.path.join(ROOT, "data", level, str(year), "*.json"))):
            d = cc.read_json(path)
            st = d.get("state") or os.path.basename(path)[:2]
            bd = B["states"][st][ch]
            idx, shared, lettered = bureau_index(bd, st)
            mr = out["match_rate"].setdefault(st, {}).setdefault(ch, {"contests": 0, "given": 0,
                                                                        "bureau_districts": len(idx) + len(shared)})
            why_not = collections.Counter()
            for c in d["contests"]:
                mr["contests"] += 1
                bad = NOT_THE_LINES.get((year, st, ch))
                if bad:
                    out["contests"][c["id"]] = {"population": None, "not_given": bad}
                    why_not[WHY["lines"]] += 1
                    continue
                dist, note, why = match(c, idx, shared, lettered)
                if dist is None:
                    out["contests"][c["id"]] = {"population": None, "not_given": note}
                    why_not[WHY[why]] += 1
                    continue
                mr["given"] += 1
                e = {"population": {"value": dist["population"], "of": "district", "as_of": "2020-04-01",
                                    "source": src_key},
                     "district": {"chamber": ch, "code": dist["code"], "geoid": dist["geoid"], "name": dist["name"]}}
                if note:
                    e["note"] = note
                out["contests"][c["id"]] = e
            mr["share"] = round(mr["given"] / mr["contests"], 4) if mr["contests"] else None
            mr["not_given"] = dict(why_not)
            if prev:
                a = sorted((x["code"], x["population"]) for x in prev["states"][st][ch])
                b = sorted((x["code"], x["population"]) for x in bd)
                out["lines_against_2022"].setdefault(st, {})[ch] = "the same districts and counts as the Bureau's " \
                    "2022 districts" if a == b else f"changed from the Bureau's 2022 districts ({len(prev['states'][st][ch])} " \
                    f"then, {len(bd)} now, ZZZ included)"
    n = len(out["contests"])
    g = sum(1 for e in out["contests"].values() if e["population"])
    out["totals"] = {"contests": n, "given": g, "share": round(g / n, 4) if n else None}
    cc.write_json(os.path.join(ROOT, "data", "population", f"state-legislative-{year}.json"), out)
    print(f"{year}: {g} of {n} contests given a population ({g / n:.1%})")
    for st, v in out["match_rate"].items():
        print("  " + st + ": " + "; ".join(f"{ch} {x['given']}/{x['contests']}" +
                                           (f" (not given: {x['not_given']})" if x["not_given"] else "")
                                           for ch, x in v.items()))
    return out


def main(argv):
    for y in [int(a) for a in argv] or [2024, 2022]:
        build(y)


if __name__ == "__main__":
    main(sys.argv[1:])
