"""pipeline/governor_counts.py: three governors' counts, a fusion candidate's every party line and a certified count.

Written 2026-11-13 by worker D3 on the orchestrator's message of 04:44 UTC:
  "CT and NY 2018 governors: sum every line. A fusion candidate's votes are the sum of his lines in the official
  count, so one line understates both the candidate and n. List the moves."
  "IN 2024 governor: the certified count wins. "Certified: T" is the agency's own word in its own data, which 15:16
  accepts. A file name or URL is what it refuses. Take Braun 1,566,081 and McCormick 1,183,741, name the archive in the
  source, and list the move. D2 is done, so it is yours."
Reason (the orchestrator, 2026-11-07 18:54): "n enters p directly", so a count that is short moves p by the same
factor. M2 found all three (checks/M2-REPORT.md section 14.1, item 10); data/local/REPORT.md section 35 lists the moves.

The record's source, Cha, Kuriwaki and Snyder (Harvard Dataverse doi:10.7910/DVN/DGDRDT, v4.1), gives these three
contests as follows [measured]: Connecticut's and New York's 2018 nominees on their own party's line alone, and
Indiana's 2024 two nominees alone, at figures under the state's archive.

The sources (each read once, kept in $VOTE_CACHE with its .meta.json):
  Connecticut 2018  the Secretary of the State's Election History, the 2018 general's governor contest
                    (https://electionhistory.ct.gov/contest/3781, read 2026-11-13 04:49 UTC): each candidate's votes on
                    each line, the page's data as served. Lamont 694,510 (Democratic 676,649, Working Families 17,861);
                    Stefanowski 650,138 (Republican 624,750, Independent 25,388); Griebel 54,741; Hanscomb 6,086;
                    Greenstein 1,254; Whitnum, a write-in, 74; "Total Votes Cast" 1,406,803 [stated]. The page lists
                    the count under "Official Sources": "Statement of Vote 2018", page 7 [stated]. That is the mark
                    taken, the page's own words under 15:16 ("marks them certified or official"). It also says: "The
                    election from the original source document contained data entry errors that have been preserved"
                    and "There are discrepancies in precinct reporting in the Town of Woodstock" [stated]. Algara and
                    Amlani's county returns give Lamont 694,510 and Stefanowski 650,138, and MEDSL's precinct file
                    694,509 and 650,132, every line summed [measured].
  New York 2018     Algara and Amlani's county returns (Harvard Dataverse doi:10.7910/DVN/DGUMFI; the file D2's build
                    reads, pipeline/intake/algara_amlani.py), summed over the 62 counties, none missing: Cuomo 3,635,340
                    and Molinaro 2,207,602, each nominee's lines together [measured]. New York's State Board refused us
                    (2026-11-07 18:49), so its own count is not read, and MEDSL's 2018 file holds the governor in 57 of
                    the 62 counties (data/local/check-volume.json). That the authors' figures are every line is read
                    from Connecticut, where they equal the Secretary of the State's lines summed to the vote [inferred].
                    The other three candidates ran on one line each, and keep the dataset's figures.
  Indiana 2024      Indiana's results archive of the 2024 general (https://enr.indianavoters.in.gov/archive/2024General/,
                    read 2026-11-07 08:40 UTC by pipeline/intake/in_enr.py), whose settings say "Certified": "T":
                    Braun 1,566,081, McCormick 1,183,741, Rainwater 129,781 and Stried, a write-in, 52.

What it does (run again, it changes nothing):
  fix_cha(contests)   the same counts in Cha's contests as D2's build reads them (pipeline/chambers.py _load,
                      pipeline/intake/build_congress.py cha_index): the nominees' votes and the contest's total, so that
                      every fit, back-test and last-race index takes them. It stops where a contest's figures are
                      neither the dataset's nor the fixed ones.
  main()              each record: its candidates' votes (Connecticut's with their lines, in `lines`), the candidates
                      the source names and the dataset leaves out (Connecticut's write-in; Indiana's Rainwater and
                      write-in), total_votes, the source, two_party, n (the two leaders' votes less one, as D2's build
                      sets it) and each p scaled to the new n (method "density": event = f_half / n), a note; and the
                      file's sources block. Then the last-race input of each later record whose last race is one of
                      these (Connecticut and New York 2022), read again from chambers.last_governor_index().
Then pipeline/d2_labels.py, and pipeline/chambers.py odd, backtest, compute and history, as for Hawaii 2018
(pipeline/governor_hi2018.py; data/local/REPORT.md section 30).

Run:  VOTE_CACHE=/tmp/vote-cache python3 -I pipeline/governor_counts.py
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fetch as F  # noqa: E402

REPO = os.path.dirname(HERE)
CT_PAGE = os.path.join(F.CACHE, "ct_sots", "contest-3781.html")
CT_URL = "https://electionhistory.ct.gov/contest/3781"
AA = os.path.join(F.CACHE, "algara_amlani", "normalized", "governors.json")
AA_FILE = os.path.join(F.CACHE, "algara_amlani", "dataverse_shareable_gubernatorial_county_returns_1865_2020.Rdata")
IN_ENR = os.path.join(F.CACHE, "in_enr", "normalized", "2024General.jsonl")
IN_CHECKS = os.path.join(F.CACHE, "in_enr", "normalized", "checks-2024General.json")
TAG = "the count (pipeline/governor_counts.py): "
CHA_NOTE = "governors' totals here leave out candidates under ten votes"
NOTE_LAST = ("the last governor race's Democratic share ({state} 2018) reads each nominee's every party line "
             "(pipeline/governor_counts.py; the orchestrator, 2026-11-13 04:44; data/local/REPORT.md section 35)")

# the record's candidates (Cha's names) and their figures: the dataset's, and the count taken here [measured]
FIX = {
    "2018-governor-CT": {
        "key": (2018, "CT"), "source_key": "ct_sots",
        "was": {"LAMONT, EDWARD M. (NED)": 676649, "STEFANOWSKI, BOB": 624750, "GRIEBEL, R. NELSON (OZ)": 54741,
                "HANSCOMB, RODNEY": 6086, "GREENSTEIN, MARK STEWART": 1254},
        "names": {"LAMONT, EDWARD M. (NED)": "Ned Lamont and Susan Bysiewicz",
                  "STEFANOWSKI, BOB": "Bob Stefanowski and Joe Markley",
                  "GRIEBEL, R. NELSON (OZ)": "Oz Griebel and Monty E. Frank",
                  "HANSCOMB, RODNEY": "Rodney Hanscomb and Jeffrey Thibeault",
                  "GREENSTEIN, MARK STEWART": "Mark Stewart Greenstein and John Demitrus"},
        "add": [("WHITNUM, LEE", "W-I", "Lee Whitnum and Jacey Wyatt")],
        "expect": {"Ned Lamont and Susan Bysiewicz": (694510, [("Democratic", 676649), ("Working Families", 17861)]),
                   "Bob Stefanowski and Joe Markley": (650138, [("Republican", 624750), ("Independent", 25388)]),
                   "Oz Griebel and Monty E. Frank": (54741, None), "Rodney Hanscomb and Jeffrey Thibeault": (6086, None),
                   "Mark Stewart Greenstein and John Demitrus": (1254, None),
                   "Lee Whitnum and Jacey Wyatt": (74, None)},
        "total": 1406803,
    },
    "2018-governor-NY": {
        "key": (2018, "NY"), "source_key": "algara_amlani",
        "was": {"CUOMO, ANDREW M.": 3424416, "MOLINARO, MARCUS J. (MARC)": 1926485, "HAWKINS, HOWIE": 103946,
                "SHARPE, LARRY": 95033, "MINER, STEPHANIE A.": 55441},
        "now": {"CUOMO, ANDREW M.": 3635340, "MOLINARO, MARCUS J. (MARC)": 2207602},
        "add": [],
    },
    "2024-governor-IN": {
        "key": (2024, "IN"), "source_key": "in_enr",
        "was": {"BRAUN, MIKE": 1561279, "MCCORMICK, JENIFFER": 1179967},
        "names": {"BRAUN, MIKE": "Mike Braun & Micah Beckwith", "MCCORMICK, JENIFFER": "Jennifer G. McCormick & Terry Goodin"},
        "add": [("RAINWATER, DONALD", "Lbt", "Donald Rainwater & Tonya Hudson"),
                ("STRIED, CHRISTOPHER RYAN", "W-I", "Christopher Ryan Stried (W/I)")],
        "expect": {"Mike Braun & Micah Beckwith": 1566081, "Jennifer G. McCormick & Terry Goodin": 1183741,
                   "Donald Rainwater & Tonya Hudson": 129781, "Christopher Ryan Stried (W/I)": 52},
    },
}

NOTES = {
    "2018-governor-CT": (
        "the candidates' votes are the Connecticut Secretary of the State's count (its Election History, which lists "
        "the Statement of Vote 2018 under 'Official Sources'), each candidate's lines summed (in `lines`): Lamont "
        "694,510 (Democratic 676,649, Working Families 17,861), Stefanowski 650,138 (Republican 624,750, Independent "
        "25,388); the write-in Whitnum's 74 are added, so the total is the page's 'Total Votes Cast', 1,406,803. Cha, "
        "Kuriwaki and Snyder give each nominee's own party line alone (676,649 and 624,750). n and each p follow the "
        "lines summed, and so do D2's fits of later years and Connecticut 2022's last-governor-race input (the "
        "orchestrator, 2026-11-13 04:44: \"A fusion candidate's votes are the sum of his lines in the official "
        "count\"; data/local/REPORT.md section 35)"),
    "2018-governor-NY": (
        "Cuomo's and Molinaro's votes are each nominee's every party line, 3,635,340 and 2,207,602: Algara and "
        "Amlani's county returns summed over the 62 counties, none missing. Cha, Kuriwaki and Snyder give each "
        "nominee's own party line alone (3,424,416 and 1,926,485); the other three ran on one line each and keep "
        "their figures. New York's State Board refused us (2026-11-07 18:49), so its own count is not read; that "
        "the authors' figures are every line is read from Connecticut 2018, where they equal the Secretary of the "
        "State's lines summed to the vote [inferred]. n and each p follow the lines summed, and so do D2's fits of "
        "later years and New York 2022's last-governor-race input (the orchestrator, 2026-11-13 04:44; "
        "data/local/REPORT.md section 35)"),
    "2024-governor-IN": (
        "the candidates' votes are Indiana's results archive of the 2024 general, whose data says Certified: T "
        "(the orchestrator, 2026-11-13 04:44: \"the certified count wins\"): Braun 1,566,081, McCormick 1,183,741, "
        "Rainwater 129,781 and the write-in Stried's 52. Cha, Kuriwaki and Snyder list the two nominees alone, at "
        "1,561,279 and 1,179,967. n and each p follow the certified count (data/local/REPORT.md section 35)"),
}


def _meta(path):
    if not (os.path.exists(path) and os.path.exists(path + ".meta.json")):
        raise SystemExit(f"governor_counts: {path} (and its .meta.json) is not in the cache")
    with open(path + ".meta.json") as f:
        return json.load(f)


def ct_2018():
    """The Secretary of the State's 2018 governor contest, from the page's own data: ({name: (votes, lines)}, total,
    source). Stops where the page is not that contest, does not list the Statement of Vote under 'Official Sources',
    or its figures are not the ones expected."""
    meta = _meta(CT_PAGE)
    with open(CT_PAGE, encoding="utf-8", errors="replace") as f:
        s = f.read()
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', s, re.S)
    if not m or "Official Sources" not in s:
        raise SystemExit("governor_counts: Connecticut's page has no data, or does not say 'Official Sources'")
    c = json.loads(m.group(1))["props"]["pageProps"]["contest"]
    if (c["office"]["name"], c["division"]["displayName"], c["event"]["startDate"][:10], c["event"]["type"]["name"],
            c["isSpecial"]) != ("Governor", "State of Connecticut", "2018-11-06", "General", False):
        raise SystemExit("governor_counts: Connecticut's page is not the 2018 general's governor contest")
    files = [x["file"]["title"] for x in c.get("files") or []]
    if files != ["Statement of Vote 2018"]:
        raise SystemExit(f"governor_counts: Connecticut's page names its sources {files}")
    got, total = {}, None
    for x in c["candidates"]:
        if x["displayName"] == "Total Votes Cast":
            total = x["nVotes"]
            continue
        if x["displayName"] == "Total Ballots Cast":
            continue
        lines = None
        if (x.get("party2") or {}).get("name"):
            lines = [(x["party"]["name"], x["nVotesParty1"]), (x["party2"]["name"], x["nVotesParty2"])]
            if x.get("party3") or sum(v for _, v in lines) != x["nVotes"]:
                raise SystemExit(f"governor_counts: Connecticut's lines for {x['displayName']} do not add up")
        got[x["displayName"]] = (x["nVotes"], lines)
    fx = FIX["2018-governor-CT"]
    want = {k: (v, [tuple(t) for t in ln] if ln else None) for k, (v, ln) in fx["expect"].items()}
    if {k: (v, [tuple(t) for t in ln] if ln else None) for k, (v, ln) in got.items()} != want or total != fx["total"]:
        raise SystemExit(f"governor_counts: Connecticut's page reads {got}, total {total}")
    src = {"name": "Connecticut Secretary of the State, Election History: 2018 Nov 6, General Election, Governor "
                   "(the page's data, each candidate's votes by line)",
           "url": CT_URL, "read_utc": meta["read_utc"],
           "licence": "no licence printed; the State of Connecticut's public election returns",
           "mark": "official (the page lists the count under 'Official Sources': 'Statement of Vote 2018', page 7)",
           "via": CT_URL,
           "note": ("sha256 " + meta["sha256"][:16] + "; the page also says 'The election from the original source "
                    "document contained data entry errors that have been preserved' and 'There are discrepancies in "
                    "precinct reporting in the Town of Woodstock'")}
    return got, total, src


def ny_2018():
    """Algara and Amlani's New York 2018 governor, summed over its counties: ({record name: votes}, the record's
    source, the file's source block as D2's build writes it)."""
    with open(AA) as f:
        d = json.load(f)
    hit = [e for e in d["elections"] if e["year"] == 2018 and e["state"] == "NY" and e["type"] == "G"]
    if len(hit) != 1:
        raise SystemExit(f"governor_counts: {len(hit)} New York 2018 elections in Algara and Amlani's file")
    e = hit[0]
    if (e["counties"], e["counties_missing"], e["D"], e["R"]) != (62, 0, 3635340, 2207602):
        raise SystemExit(f"governor_counts: Algara and Amlani's New York 2018 reads {e}")
    if not ("Cuomo" in e["dem_nominee"] and "Molinaro" in e["rep_nominee"]):
        raise SystemExit(f"governor_counts: Algara and Amlani's New York 2018 nominees are {e['dem_nominee']}, "
                         f"{e['rep_nominee']}")
    meta = _meta(AA_FILE)
    src = {"name": d["source"]["name"], "url": meta["url"], "read_utc": meta["read_utc"], "licence": "CC0 1.0", "mark": "stated",
           "via": "https://doi.org/10.7910/DVN/DGUMFI",
           "note": ("the two nominees' votes, county returns summed to the state over 62 counties, none missing, by "
                    "pipeline/intake/algara_amlani.py: the authors' compilation, not a state's certified total; the "
                    "other three candidates' votes are Cha, Kuriwaki and Snyder's (v4.1), since the authors give the "
                    "others only as the county total less the two nominees")}
    return {"CUOMO, ANDREW M.": e["D"], "MOLINARO, MARCUS J. (MARC)": e["R"]}, src, d["source"]


def in_2024():
    """Indiana's archive's 2024 governor: ({archive name: votes}, source). Stops where the archive is not certified."""
    with open(IN_CHECKS) as f:
        chk = json.load(f)
    if chk.get("certified") != "T" or (chk.get("settings") or {}).get("Certified") != "T":
        raise SystemExit("governor_counts: Indiana's 2024 archive does not say Certified: T")
    hit = []
    with open(IN_ENR) as f:
        for line in f:
            c = json.loads(line)
            if c.get("title") == "Governor & Lt. Governor":
                hit.append(c)
    if len(hit) != 1:
        raise SystemExit(f"governor_counts: {len(hit)} governor contests in Indiana's 2024 archive")
    got = {" ".join(x["name"].split()): x["votes"] for x in hit[0]["candidates"]}
    if got != FIX["2024-governor-IN"]["expect"]:
        raise SystemExit(f"governor_counts: Indiana's archive reads {got}")
    src = {"name": "Indiana Election Division, results archive of the 2024 General Election (Governor & Lt. Governor)",
           "url": chk["source"]["url"], "read_utc": chk["source"]["read_utc"],
           "licence": "no licence printed; the State of Indiana's public election returns",
           "mark": "certified (the archive's settings say \"Certified\": \"T\", version 20241213_160047)",
           "via": chk["source"]["url"], "note": f"sha256 {chk['source']['sha256'][:16]}; {hit[0]['file']}"}
    return got, src


def counts():
    """{record id: ({record name: votes}, {record name: lines or None}, added [(name, party, votes)], the record's
    source, the file's source block)}."""
    out = {}
    got, total, src = ct_2018()
    fx = FIX["2018-governor-CT"]
    out["2018-governor-CT"] = ({n: got[s][0] for n, s in fx["names"].items()},
                               {n: got[s][1] for n, s in fx["names"].items()},
                               [(n, p, got[s][0]) for n, p, s in fx["add"]], src, src)
    got, src, file_src = ny_2018()
    out["2018-governor-NY"] = ({**FIX["2018-governor-NY"]["was"], **got}, {}, [], src, file_src)
    got, src = in_2024()
    fx = FIX["2024-governor-IN"]
    out["2024-governor-IN"] = ({n: got[s] for n, s in fx["names"].items()}, {},
                               [(n, p, got[s]) for n, p, s in fx["add"]], src, src)
    return out


def fix_cha(contests):
    """Cha, Kuriwaki and Snyder's normalized contests with the three governors' nominees at the counts taken here and
    the contest's total; the dataset's other candidates stand. In place; returns the list. Stops where a contest is not
    found once, or its figures are neither the dataset's nor these."""
    for rid, (now, _, added, _, _) in counts().items():
        year, st = FIX[rid]["key"]
        hit = [c for c in contests if c["year"] == year and c["office"] == "governor" and c["state"] == st
               and not c["special"]]
        if len(hit) != 1:
            raise SystemExit(f"governor_counts.fix_cha: {len(hit)} {st} {year} governor contests in Cha's file")
        c = hit[0]
        old = {a["name"]: a["votes"] for a in c["candidates"]}
        if old != FIX[rid]["was"] and old != {**FIX[rid]["was"], **now}:
            raise SystemExit(f"governor_counts.fix_cha: Cha's {st} {year} votes are not the dataset's as expected: {old}")
        for a in c["candidates"]:
            a["votes"] = now.get(a["name"], a["votes"])
        c["totalvotes"] = sum(now.get(n, v) for n, v in old.items()) + sum(v for _, _, v in added)
        c["count_fixed"] = f"pipeline/governor_counts.py: {rid}"
    return contests


def _sources_block(lines, key, src):
    """The file's top-level sources block with `key` added before "model" (as pipeline/governor_hi2018.py does)."""
    text = "\n".join(lines)
    if f'"{key}": {{' in text.split(' "model": {')[0]:
        return lines
    block = [" " + b for b in json.dumps({key: src}, indent=1, ensure_ascii=False).split("\n")[1:-1]]
    k = lines.index(' "model": {')
    if lines[k - 1] != " }," or lines[k - 2] != "  }":
        raise SystemExit("governor_counts: the file's sources block does not end where expected")
    lines[k - 2] = lines[k - 2] + ","
    lines[k - 1:k - 1] = block
    return lines


def fix_record(rid, rec, now, lines_of, added, src):
    """The record with the counts taken here; returns [(p under, was, now)]."""
    res = rec["result"]
    cands = res["candidates"]
    old = {c["name"]: c["votes"] for c in cands}
    have = {c["name"] for c in cands}
    base = {n: v for n, v in old.items() if n not in {a for a, _, _ in added}}
    if base != FIX[rid]["was"] and base != {**FIX[rid]["was"], **now}:
        raise SystemExit(f"governor_counts: {rid}'s votes are not the dataset's as expected: {old}")
    for c in cands:
        if c["name"] in now:
            c["votes"] = now[c["name"]]
        if lines_of.get(c["name"]):
            c["lines"] = [{"party": p, "votes": v} for p, v in lines_of[c["name"]]]
    for n, p, v in added:
        if n not in have:
            cands.append({"name": n, "party": p, "votes": v})
    cands.sort(key=lambda c: -c["votes"])
    res["total_votes"] = sum(c["votes"] for c in cands)
    res["source"] = src
    tp = rec["two_party"]
    tp["votes"] = [next(c["votes"] for c in cands if c["name"] == n) for n in tp["candidates"]]
    n_old, n = tp["n_other_voters"], sum(tp["votes"]) - 1
    tp["n_other_voters"] = n
    tp["share_first"] = round(tp["votes"][0] / sum(tp["votes"]), 6)
    b = rec.get("ballot") or {}
    on = [c for c in cands if c["party"] not in ("D", "R") and not c["party"].startswith("W-I")]
    if b.get("others") is not None:
        b["others"] = len(on)
    moves = []
    p = rec["p"]
    if p.get("method") != "density" or p.get("n") not in (n_old, n):
        raise SystemExit(f"governor_counts: {rid}'s p is not a density p on n {n_old}: {p.get('method')}, {p.get('n')}")
    for x in [p] + list(p.get("alongside") or []):
        if x.get("method") != "density":
            raise SystemExit(f"governor_counts: a p of {rid} under {x['under']} is not a density p")
        was = x["value"]
        x["event"] = x["f_half"] / n
        x["value"] = x["event"] / 2
        moves.append((x["under"], was, x["value"]))
    p["n"] = n
    note = TAG + NOTES[rid]
    # the dataset's note on its totals (candidates under ten votes left out) is not the state's, whose count is taken
    # whole where the state gives every candidate (Connecticut, Indiana); New York keeps it for its other candidates
    drop = (CHA_NOTE,) if rid != "2018-governor-NY" else ()
    rec["notes"] = [x for x in rec["notes"] if not x.startswith(TAG) and not x.startswith(drop or ("\0",))] + [note]
    return moves


def last_race(fixed):
    """Every governor record of 2019-2025 whose forecast input "last_governor_race" is one of the fixed contests, read
    again from chambers.last_governor_index() (with fix_cha); returns [(id, was, now)]."""
    import chambers as CH
    idx = CH.last_governor_index()
    moves = []
    for year in range(2019, 2026):
        path = os.path.join(REPO, "data", "governor", f"{year}.json")
        if not os.path.exists(path):
            continue
        with open(path) as f:
            lines = f.read().split("\n")
        hit = False
        for i, l in enumerate(lines):
            if not l.startswith('  {"id":"') or '"last_governor_race":{"year":' not in l:
                continue
            comma = l.endswith(",")
            rec = json.loads(l.strip().rstrip(","))
            st = rec["place"]["state"]
            lg = rec["forecast_inputs"]["last_governor_race"]
            if (lg["year"], st) not in fixed or rec.get("special"):
                continue
            now = CH.last_governor_race(idx, st, year)
            if now is None or now[0] != lg["year"]:
                raise SystemExit(f"governor_counts.last_race: {rec['id']}'s last race now reads {now}")
            new = {"year": now[0], "share_D": now[1], "special": now[2], "source": now[3]}
            note = NOTE_LAST.format(state=rec["place"]["name"])
            if new != lg or note not in rec["notes"]:
                if new != lg:
                    moves.append((rec["id"], lg["share_D"], now[1]))
                rec["forecast_inputs"]["last_governor_race"] = new
                if note not in rec["notes"]:
                    rec["notes"].append(note)
                lines[i] = "  " + json.dumps(rec, separators=(",", ":"), ensure_ascii=False) + ("," if comma else "")
                hit = True
        if hit:
            with open(path, "w") as f:
                f.write("\n".join(lines))
    return moves


def main():
    cs = counts()
    for year in sorted({FIX[r]["key"][0] for r in FIX}):
        path = os.path.join(REPO, "data", "governor", f"{year}.json")
        with open(path) as f:
            lines = f.read().split("\n")
        for rid in [r for r in FIX if FIX[r]["key"][0] == year]:
            now, lines_of, added, src, file_src = cs[rid]
            at = [i for i, l in enumerate(lines) if l.startswith('  {"id":"' + rid + '"')]
            if len(at) != 1:
                raise SystemExit(f"governor_counts: {rid} is found {len(at)} times in {path}")
            line = lines[at[0]]
            comma = line.endswith(",")
            rec = json.loads(line.strip().rstrip(","))
            n_old = rec["two_party"]["n_other_voters"]
            moves = fix_record(rid, rec, now, lines_of, added, src)
            lines[at[0]] = "  " + json.dumps(rec, separators=(",", ":"), ensure_ascii=False) + ("," if comma else "")
            lines = _sources_block(lines, FIX[rid]["source_key"], file_src)
            print(f"{rid}: n {n_old:,} -> {rec['two_party']['n_other_voters']:,}; total {rec['result']['total_votes']:,}")
            for under, a, b in moves:
                print(f"  p under {under[:60]}: {a:.6g} -> {b:.6g} ({b / a:.5f}x)")
        with open(path, "w") as f:
            f.write("\n".join(lines))
    for rid, a, b in last_race({FIX[r]["key"] for r in FIX}):
        print(f"{rid}: last governor race, the Democrat's two-party share {a:.6f} -> {b:.6f}")


if __name__ == "__main__":
    main()
