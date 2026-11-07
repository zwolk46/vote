"""pipeline/governor_hi2018.py: Hawaii's 2018 governor, the Republican's votes set to the Office of Elections' certified count.

Written 2026-11-07 by worker D3 on the orchestrator's ruling of 19:13: "HI 2018: fix D2's file in your PR. Set
data/governor/2018.json's Tupola to 131,719 with the Office of Elections' certified summary as its source, and list any
p that moves. D2 is stopped, and the fix is one figure from a certified page. Note where D2's 137,719 came from."
Reason (the orchestrator, 18:54): "n enters p directly", so a wrong count moves a figure we show.

The source, read 2026-11-07 at 19:07 UTC and kept in $VOTE_CACHE/volume/raw (each with a .meta.json):
  hi-election-results.html       the Office of Elections' results page (https://elections.hawaii.gov/election-results/).
                                 Under "General Election", "November 6, 2018" it lists "Certified Reports (PDF format)"
                                 and "Certified Text Files", whose "Statewide Summary" links the file below [stated].
  hi-2018-general-summary.txt    https://files.hawaii.gov/elections/files/results/2018/general/summary.txt: one line per
                                 candidate; "Governor and Lieutenant Governor": "(D) IGE / GREEN" 244,934, "(R) TUPOLA /
                                 KERNS" 131,719, "(G) BREWER / ING" 10,123, "(N) TERUYA / ROBOTTI" 4,067 [stated].
D2's 137,719 is the figure in its source, Cha, Kuriwaki and Snyder's Candidates in American General Elections (Harvard
Dataverse doi:10.7910/DVN/DGDRDT, v4.1), as built by pipeline/chambers.py [measured: the record's result.source]; the
other three candidates there equal the certified summary to the vote [measured]. 131,719 and 137,719 differ in one digit.

What it does: checks that the page links the summary as a certified text file of the 2018 general and that the
summary's four governor lines are as above; sets the record's candidates' votes to the summary's, its total, its
two-party votes, n and share, and its source to the summary; scales each p of the record (method "density": event =
f_half / n, value = event / 2, f_half the forecast's density at an even split, which does not depend on the count) to
the new n; adds a note. Run again it changes nothing.

The refit (the orchestrator's ruling of 19:49, item 2: "refetch D2's governor sources from the documented downloads D2
already used, with no new hosts. Rerun its governor build so the 2020+ fits and HI 2022's input take 131,719. Do it
as its own small PR and list every move"). Reason (19:49): "The two leftovers should not stay wrong if they can be
refit." Two more steps:
  fix_cha(contests)   the same count in Cha, Kuriwaki and Snyder's contests as D2's build reads them (pipeline/chambers.py
                      _load, pipeline/intake/build_congress.py cha_index): Tupola's votes and the total, so that every
                      fit, back-test and last-race index the build makes takes Hawaii 2018 at 131,719. The dataset's
                      other figures stand.
  last_race()         Hawaii 2022's forecast input "last_governor_race" (data/governor/2022.json), the Democrat's
                      two-party share of Hawaii 2018, read again from chambers.last_governor_index() with the fix, as
                      build_congress.forecast_inputs writes it.
Then pipeline/chambers.py is run (odd, backtest, compute, history), and data/local/REPORT.md section 30 lists every
move.

Run:  VOTE_CACHE=/tmp/vote-cache python3 pipeline/governor_hi2018.py        (the record, then Hawaii 2022's input)
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fetch as F  # noqa: E402

FILE = os.path.join(os.path.dirname(HERE), "data", "governor", "2018.json")
RAW = os.path.join(F.CACHE, "volume", "raw")
PAGE = "hi-election-results.html"
SUMMARY = "hi-2018-general-summary.txt"
SUMMARY_URL = "https://files.hawaii.gov/elections/files/results/2018/general/summary.txt"
ID = "2018-governor-HI"
CONTEST = "Governor and Lieutenant Governor"
# the record's candidate name: the summary's line for it
NAMES = {"IGE, DAVID YUTAKA": "(D) IGE / GREEN", "TUPOLA, ANDRIA": "(R) TUPOLA / KERNS",
         "BREWER, JIM": "(G) BREWER / ING", "TERUYA, TERRENCE": "(N) TERUYA / ROBOTTI"}
EXPECT = {"(D) IGE / GREEN": 244934, "(R) TUPOLA / KERNS": 131719, "(G) BREWER / ING": 10123,
          "(N) TERUYA / ROBOTTI": 4067}
WAS = 137719
NOTE = ("TUPOLA, ANDRIA's votes are the Office of Elections' certified count, 131,719 (its Statewide Summary, a "
        "certified text file); the dataset reads 137,719, which differs in one digit (the orchestrator's ruling of "
        "2026-11-07 19:13; data/local/REPORT.md section 29). n and each p follow the certified count, and so do D2's "
        "fits of later years and Hawaii 2022's last-governor-race input (the ruling of 19:49; section 30)")
OLD_NOTE = "TUPOLA, ANDRIA's votes are the Office of Elections' certified count, 131,719"   # an earlier wording
NOTE_LAST = ("the last governor race's Democratic share (Hawaii 2018) reads Tupola at the Office of Elections' "
             "certified 131,719 in place of the dataset's 137,719 (pipeline/governor_hi2018.py; the orchestrator, "
             "2026-11-07 19:49; data/local/REPORT.md section 30)")


def _meta(name):
    p = os.path.join(RAW, name)
    if not (os.path.exists(p) and os.path.exists(p + ".meta.json")):
        raise SystemExit(f"{p} (and its .meta.json) is not in the cache")
    with open(p + ".meta.json") as f:
        return p, json.load(f)


def summary():
    page, page_meta = _meta(PAGE)
    path, meta = _meta(SUMMARY)
    with open(page, encoding="utf-8", errors="replace") as f:
        s = f.read()
    i = s.find('href="' + SUMMARY_URL + '"')
    if i < 0:
        raise SystemExit("governor_hi2018: the Office of Elections' page does not link the 2018 summary")
    j = s.find("</a>", i)
    seg = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s[max(0, i - 3000):j]))
    if not re.search(r"General Election November 6, 2018 .*Certified Text Files Statewide Summary\s*$", seg):
        raise SystemExit("governor_hi2018: the link is not the 2018 general's certified text file 'Statewide Summary'")
    import csv
    with open(path, newline="", encoding="utf-8", errors="replace") as f:
        rows = [r for r in csv.DictReader(f) if r["Contest Title"] == CONTEST]
    got = {r["Candidate Name"]: int(r["Total Votes"]) for r in rows}
    if got != EXPECT:
        raise SystemExit(f"governor_hi2018: the summary's governor lines read {got}")
    return got, {"name": "State of Hawaii Office of Elections, 2018 General Election, Certified Text Files: Statewide "
                         "Summary", "url": SUMMARY_URL, "read_utc": meta["read_utc"],
                 "licence": "no licence printed; the State of Hawaii's public election returns",
                 "mark": "certified (the Office of Elections' page lists the file under 'Certified Text Files')",
                 "via": page_meta["url"], "note": "sha256 " + meta["sha256"][:16]}


def fix_cha(contests):
    """Cha, Kuriwaki and Snyder's normalized contests (pipeline/intake/candidates_american_general_elections.py), with
    Hawaii 2018's governor at the certified count: each candidate's votes from the summary, and the contest's total.
    In place; returns the list. Stops where the contest is not found once, or where it differs from the dataset's
    figures other than Tupola's 137,719 (so a new version of the dataset is read again, not overwritten)."""
    got, _ = summary()
    hit = [c for c in contests if c["year"] == 2018 and c["office"] == "governor" and c["state"] == "HI"
           and not c["special"]]
    if len(hit) != 1:
        raise SystemExit(f"governor_hi2018.fix_cha: {len(hit)} Hawaii 2018 governor contests in Cha's file")
    c = hit[0]
    old = {a["name"]: a["votes"] for a in c["candidates"]}
    if set(old) != set(NAMES):
        raise SystemExit(f"governor_hi2018.fix_cha: Cha's contest names {sorted(old)}")
    want = {n: got[NAMES[n]] for n in NAMES}
    if old != want and old != {**want, "TUPOLA, ANDRIA": WAS}:
        raise SystemExit(f"governor_hi2018.fix_cha: Cha's votes are not the dataset's as expected: {old}")
    for a in c["candidates"]:
        a["votes"] = want[a["name"]]
    c["totalvotes"] = sum(want.values())
    c["certified_count"] = ("TUPOLA, ANDRIA's votes set to 131,719 from the dataset's 137,719: the State of Hawaii "
                            "Office of Elections' certified Statewide Summary (pipeline/governor_hi2018.py)")
    return contests


def last_race():
    """Every governor record of 2019-2025 whose forecast input "last_governor_race" is Hawaii's 2018 race, read again
    from chambers.last_governor_index() (with fix_cha); returns [(id, was, now)]."""
    import chambers as CH
    idx = CH.last_governor_index()
    moves = []
    for year in range(2019, 2026):
        path = os.path.join(os.path.dirname(HERE), "data", "governor", f"{year}.json")
        if not os.path.exists(path):
            continue
        with open(path) as f:
            lines = f.read().split("\n")
        hit = False
        for i, l in enumerate(lines):
            if not l.startswith('  {"id":"') or '"last_governor_race":{"year":2018' not in l:
                continue
            comma = l.endswith(",")
            rec = json.loads(l.strip().rstrip(","))
            st = rec["place"]["state"]
            lg = rec["forecast_inputs"]["last_governor_race"]
            if st != "HI" or lg["year"] != 2018:
                continue
            now = CH.last_governor_race(idx, st, year)
            if now is None or now[0] != 2018:
                raise SystemExit(f"governor_hi2018.last_race: {rec['id']}'s last race now reads {now}")
            new = {"year": now[0], "share_D": now[1], "special": now[2], "source": now[3]}
            if new != lg or NOTE_LAST not in rec["notes"]:
                if new != lg:
                    moves.append((rec["id"], lg["share_D"], now[1]))
                rec["forecast_inputs"]["last_governor_race"] = new
                if NOTE_LAST not in rec["notes"]:
                    rec["notes"].append(NOTE_LAST)
                lines[i] = "  " + json.dumps(rec, separators=(",", ":"), ensure_ascii=False) + ("," if comma else "")
                hit = True
        if hit:
            with open(path, "w") as f:
                f.write("\n".join(lines))
    return moves


def main():
    got, src = summary()
    with open(FILE) as f:
        lines = f.read().split("\n")
    at = [i for i, l in enumerate(lines) if l.startswith('  {"id":"' + ID + '"')]
    if len(at) != 1:
        raise SystemExit(f"governor_hi2018: {ID} is found {len(at)} times in {FILE}")
    line = lines[at[0]]
    comma = line.endswith(",")
    rec = json.loads(line.strip().rstrip(","))
    cands = rec["result"]["candidates"]
    old = {c["name"]: c["votes"] for c in cands}
    if set(old) != set(NAMES):
        raise SystemExit(f"governor_hi2018: the record names {sorted(old)}")
    for c in cands:
        c["votes"] = got[NAMES[c["name"]]]
    changed = old != {c["name"]: c["votes"] for c in cands}
    if changed and old != {**{c["name"]: c["votes"] for c in cands}, "TUPOLA, ANDRIA": WAS}:
        raise SystemExit(f"governor_hi2018: the record's votes are not the dataset's as expected: {old}")
    rec["result"]["total_votes"] = sum(c["votes"] for c in cands)
    rec["result"]["source"] = src
    tp = rec["two_party"]
    tp["votes"] = [next(c["votes"] for c in cands if c["name"] == n) for n in tp["candidates"]]
    n_old, n = tp["n_other_voters"], sum(tp["votes"])
    tp["n_other_voters"] = n
    tp["share_first"] = round(tp["votes"][0] / n, 6)
    moves = []
    p = rec["p"]
    if p.get("method") != "density" or p.get("n") not in (n_old, n):
        raise SystemExit(f"governor_hi2018: the record's p is not a density p on n {n_old}: {p.get('method')}, {p.get('n')}")
    for x in [p] + list(p.get("alongside") or []):
        if x.get("method") != "density":
            raise SystemExit(f"governor_hi2018: a p under {x['under']} is not a density p")
        was = x["value"]
        x["event"] = x["f_half"] / n
        x["value"] = x["event"] / 2
        moves.append((x["under"], was, x["value"]))
    p["n"] = n
    if NOTE not in rec["notes"]:
        rec["notes"] = [x for x in rec["notes"] if not x.startswith(OLD_NOTE)] + [NOTE]
    lines[at[0]] = "  " + json.dumps(rec, separators=(",", ":"), ensure_ascii=False) + ("," if comma else "")
    text = "\n".join(lines)
    if '"hi_oe": {' not in text:
        block = json.dumps({"hi_oe": src}, indent=1, ensure_ascii=False).split("\n")[1:-1]
        block = [" " + b for b in block]
        k = lines.index(' "model": {')
        if lines[k - 1] != " }," or lines[k - 2] != "  }":
            raise SystemExit("governor_hi2018: the file's sources block does not end where expected")
        lines[k - 2] = lines[k - 2] + ","
        lines[k - 1:k - 1] = block
        text = "\n".join(lines)
    with open(FILE, "w") as f:
        f.write(text)
    print(f"{ID}: n {n_old:,} -> {n:,}; total {sum(old.values()):,} -> {rec['result']['total_votes']:,}")
    for under, a, b in moves:
        print(f"  p under {under}: {a:.6g} -> {b:.6g} ({b / a:.5f}x)")
    for rid, a, b in last_race():
        print(f"{rid}: last governor race (Hawaii 2018), the Democrat's two-party share {a:.6f} -> {b:.6f}")


if __name__ == "__main__":
    main()
