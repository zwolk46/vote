"""C39 (seventh pass; the orchestrator's words of 20:28 UTC: "Build your input-volume check without reading D3's
local_volume.py or §29 first. Then compare your list of state-years with his. Each difference between the two lists is a
reading for me. Reason: two volume checks built separately catch what one alone misses"). Read only after c38 was built
and run: data/local/check-volume.json (D3's volume test, pipeline/local_volume.py: part 1, the year's top contest's
precinct sum against D2's count at 0.5%; part 2, MEDSL's legislative candidates against Klarner's, flagged where over 5%
sit at a ratio of 2 or 1/2 or the median is off by 3%; part 3, the structural scan) and data/local/REPORT.md section 29,
against c38's list (checks/m2/c38-state-years.json, one line per state-year with p) and its districts
(checks/m2/c38-districts.json).

  39.1 D3's flagged state-years (parts 1 and 2) and the files part 3 changed, from check-volume.json.
  39.2 c38's state-years, by the comparison that lists them.
  39.3 The two lists side by side: both, c38 alone, D3 alone; and what each check reads that the other does not.
  39.4 The methods' differences, each a reading: the unit (a contest against its record, or a state's lines summed);
       the 2024 gate (the president alone, or every federal and statewide contest); fusion lines; D2's two-party totals;
       Klarner's districts (a doubling test, or every district off by 5%); the chamber-years with no second count.
[measured] from the two files; D3's words [stated: his report].
"""
import collections
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
CHECK = os.path.join(L.ROOT, "data", "local", "check-volume.json")
MINE_SY = os.path.join(HERE, "c38-state-years.json")
MINE_D = os.path.join(HERE, "c38-districts.json")


def d3_flags(cv):
    """D3's flagged state-years: (year, st) -> [words]; and part 3's files with rule drops"""
    out = collections.defaultdict(list)
    for year, Y in cv["years"].items():
        for st, v in (Y.get("part1") or {}).items():
            if v.get("flag"):
                w = v.get("worst")
                out[(int(year), st)].append(f"part 1 {v.get('top')}: " + (f"{w:+.2%}" if isinstance(w, (int, float)) else str(w)) + f"; {v.get('reading', '')}".rstrip("; "))
        for st, v in (Y.get("part2") or {}).items():
            if v.get("flag"):
                out[(int(year), st)].append(f"part 2 legislature vs Klarner: median {v.get('median')}, {v.get('share_at_2_or_half', 0):.1%} at 2 or 1/2 of {v.get('matched')} matched")
        for st, v in (Y.get("flags") or {}).items():
            out[(int(year), st)].append(f"verdict {v.get('verdict')} ({v.get('by')})")
    drops = {}
    for year, P in cv.get("part3", {}).items():
        for fname, f in (P.get("files_with_findings") or {}).items():
            if f.get("rule_drops"):
                m = re.match(r"(\d{4})-([a-z]{2})-", fname)
                st = m.group(2).upper() if m else fname
                drops[(int(year), st, fname)] = f["rule_drops"]
    return out, drops


def main():
    print(f"C39 volume comparison; {L.git_head()}")
    cv = L.load_json(CHECK)
    mine = {(x["year"], x["state"]): x["reasons"] for x in L.load_json(MINE_SY)["state_years"]}
    dists = L.load_json(MINE_D)["districts"]
    d3, drops = d3_flags(cv)
    print(f"  D3's test ({cv['about'][:120]}...): line {cv['line']}; part 2 rule {cv['part2_rule']}")
    print("\n39.1 D3's flagged state-years (check-volume.json parts 1 and 2, and the verdicts)")
    for (y, st), ws in sorted(d3.items()):
        print(f"  {y} {st}: " + " | ".join(ws))
    print(f"  part 3's files where the rules dropped rows: {len(drops)}")
    for (y, st, fname), rd in sorted(drops.items()):
        print(f"    {y} {st} {fname}: {json.dumps(rd)[:160]}")
    cov = cv.get("coverage", {})
    for y, c in sorted(cov.items()):
        print(f"  coverage {y}: {c.get('states')} states; part 1 {len(c.get('part1', []))}, part 2 {len(c.get('part2', []))}, neither {len(c.get('neither', []))} {c.get('neither')}")
    print(f"  untested: {cv.get('untested')}")

    print("\n39.2 c38's state-years (c38-state-years.json), by the comparison that lists them")
    kinds = collections.Counter()
    for (y, st), rs in sorted(mine.items()):
        for r in rs:
            kinds[r.split(" ")[0] + (" " + r.split(" ")[1] if r.startswith(("MEDSL", "Klarner", "NC", "D1/D2")) else "")] += 1
    print("  by kind: " + "; ".join(f"{k} {v}" for k, v in sorted(kinds.items())))
    print(f"  state-years: {len(mine)}")

    print("\n39.3 Side by side")
    both = sorted(set(mine) & set(d3))
    mine_only = sorted(set(mine) - set(d3))
    d3_only = sorted(set(d3) - set(mine))
    print(f"  both: {len(both)}; c38 alone: {len(mine_only)}; D3 alone: {len(d3_only)}")
    print("  both:")
    for k in both:
        print(f"    {k[0]} {k[1]}: D3 {' | '.join(d3[k])}")
        print(f"      {'':8s}c38 {' | '.join(mine[k])[:400]}")
    print("  D3 alone (what c38 says of the state-year, if anything):")
    for k in d3_only:
        print(f"    {k[0]} {k[1]}: {' | '.join(d3[k])}")
    # c38 alone, grouped by the kind of comparison, the Klarner-only coarse tier last
    groups = collections.defaultdict(list)
    for k in mine_only:
        rs = mine[k]
        if all(r.startswith("Klarner state-") and "coarse" in r for r in rs):
            groups["coarse tier only (Klarner chamber-years with no MEDSL file; a state count would settle them)"].append(k)
        elif any(r.startswith("MEDSL file") for r in rs):
            groups["a MEDSL precinct file's contest against D1 or D2"].append(k)
        elif any(r.startswith("Klarner vs MEDSL") for r in rs):
            groups["Klarner's districts against MEDSL's"].append(k)
        elif any(r.startswith("NC Board") or r.startswith("Indiana") or r.startswith("Louisiana") for r in rs):
            groups["a state's own file against D1, D2 or Klarner"].append(k)
        else:
            groups["D1's or D2's record against MEDSL's state-level file (no p of D3's)"].append(k)
    for g, ks in groups.items():
        print(f"  c38 alone, {g}: {len(ks)}")
        for k in ks:
            print(f"    {k[0]} {k[1]}: {' | '.join(mine[k])[:420]}")

    print("\n39.4 The methods, each difference a reading")
    print("  1. The unit. D3's part 1 adds a state's House lines together (or reads the governor); c38 reads each federal and statewide")
    print("     contest against its own D1 or D2 record. A district short by 8% inside a state within 0.1% passes his (Washington 2022's")
    print("     eighth district, where 13 local p rest on the file) and is listed by mine.")
    print("  2. 2024. D3's gate for 2024 is the president against D1's count; c38 reads the president, the Senate, every House seat and the")
    print("     governor. North Dakota 2024's governor rows are absent in Burleigh and Divide counties (-14%) with the president whole;")
    print("     New York 2024's Monroe County lacks US House rows for 200 of 659 precincts and Assembly rows for 185 (29% of its presidential")
    print("     vote), Ontario County Assembly rows for 54 of 92 (53%), with the president and the Senate whole: the Assembly p of those")
    print("     counties rest on short counts, which the president's gate cannot see.")
    print("  3. Fusion. D3 sums a candidate's lines (Connecticut, New York) and, where D2's record holds the party line alone, compares that")
    print("     line; c38 compares the record's total and leader with the file's and lists the difference. The record's figure is the")
    print("     reading either way: Connecticut 2018's Lamont 676,649 is the Democratic line; the file's lines summed give 694,509.")
    print("  4. D2's governors. D2's total_votes is its two leading candidates' sum where its source gives no more (Rhode Island 2018,")
    print("     West Virginia 2024, Wyoming 2022, Missouri 2024, New Hampshire 2018 and 2024, Indiana 2024, North Carolina 2020); D3's")
    print("     part 1 matches the two leaders, so it sees no gap; c38 lists the totals apart from the leaders. p's n is the two-party")
    print("     n by design, so no p moves; the label does.")
    print("  5. Klarner. D3's part 2 flags a state-year where over 5% of candidates sit at 2x or 1/2 or the median is off by 3%: a test")
    print("     for doubling. c38 lists every district off by more than 5% by the two parties' lines (or every vote), on either side:")
    print(f"     {len(dists)} districts in c38-districts.json (Idaho 2022's first Senate district filed unopposed, Vermont 2018's Chittenden at")
    print("     3.7x, Michigan 2022's 63rd House and 3rd Senate districts, New York 2022's 56th Senate district, and MEDSL's partial districts")
    print("     in the 2016 state file and the 2022 'local' files). Neither side is right by default; each is a reading for a state count.")
    print("  6. No second count. D3 lists 2020 as untested; c38 lists with it DC 2018, the odd-year legislatures of 2023 and 2025, Louisiana")
    print("     2023, North Carolina's odd years and primaries, and reads Klarner's chamber-years without a MEDSL file against the")
    print("     chamber's own history (the coarse tier), which neither check can settle without a state count.")
    print("  7. Subtotal rows. Both checks found the county-total rows (Idaho 2022, Oregon 2018, Michigan 2022) and New Jersey 2024's")
    print("     municipality rows under mode TOTAL (D3's part 3: 140 rows; c38: 1,478,257 votes over 14 federal and statewide contests,")
    print("     Bergen's fifth district at +79% raw and +0.02% once dropped), by rules written apart: D3 drops a row equal to the rest of")
    print("     its county for every candidate; c38 drops a named total equal to the county's other rows, or a row whose name the")
    print("     county's other rows extend and equal, within 0.5% or 10 votes. New Jersey 2018's Camden precincts, every one named")
    print("     '... TOTAL', are kept by both.")


if __name__ == "__main__":
    main()
