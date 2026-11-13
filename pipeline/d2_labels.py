"""pipeline/d2_labels.py: the labels of D2's records that M2's seventh pass found untrue, where no p moves.

Written 2026-11-13 by worker D3 on the orchestrator's order of 2026-11-07 22:19, item 5: "No p is touched by these;
queue them after VA 2023: D2's governor totals holding two parties only (RI 2018, WV 2024, WY 2022, IN 2024, MO and NH
2024, NH 2018, NC 2020, and the D line in CT and NY 2018); ME-02 2024's RCV lines in the total; NC 2002 House 118; ND
2024 governor rows missing in 2 counties. Reason: n enters p directly, and a count that is short or doubled moves p by
the same factor." (M2's report, checks/M2-REPORT.md section 14.1, items 7, 10, 11 and 14.) D2 is stopped; its records
are fixed in place, one line each, as pipeline/governor_hi2018.py fixes Hawaii 2018 (its file keeps one contest a line).

What it does (run again, it changes nothing):
  governors   every regular governor record of 2018-2024 against a second count of the same contest: MEDSL's precinct
              files (normalized by pipeline/intake/medsl_precinct.py) for 2018, 2022 and 2024; North Carolina's State
              Board for 2020 (pipeline/intake/ncsbe.py); Indiana's results archive for 2024 (pipeline/intake/in_enr.py),
              since MEDSL's 2024 Indiana file is held back (data/local/REPORT.md section 6); none for New York 2018
              (MEDSL's file is held, data/local/check-volume.json, and the State Board refused us, 2026-11-07 18:49) or
              for the other 2020 contests (MEDSL's 2020 file holds local offices only). Where the record's total_votes
              is off the second count by more than 0.5% (M2's line), the record says what its total adds up
              (result.total_votes_of) and a note gives the second count. The candidates' figures, the two-party votes
              and n are left as they are: a governor's p rests on the two leaders' votes (two_party.n_other_voters,
              pipeline/chambers.py), not on total_votes, so no p moves.
  me02        ME-02 2024: the Clerk's statistics print the ranked-choice count's last round, with "Continuing Ballots"
              (the two candidates' votes added up) and "Exhausted Ballots" as lines; they are taken out of the
              candidates into result.rcv_lines, total_votes is the two candidates' last-round votes, and two_party pairs
              Golden with Theriault. p stays not computed (ranked choice, model section 7).
  Since pipeline/governor_counts.py (the orchestrator, 2026-11-13 04:44), Connecticut's and New York's 2018 nominees
  are at every party line and Indiana 2024 at its archive's certified count; a label a record no longer needs (its
  total within the line, or no second count) is taken off with its note.
  The two items with nothing to fix are listed in data/congress/check-totals.json: North Carolina 2002's House 118
  (the record already holds the State Board's certified counts; Klarner's contest file total, 125,193, carries its
  candidate file's 113,717 for Rapp, whom the Board counts at 13,717) and North Dakota 2024's governor (MEDSL's file
  lacks the governor's rows in Burleigh and Divide Counties; the record's count is the dataset's, 361,421, and no p of
  D3's rests on those rows).

Run:  VOTE_CACHE=/tmp/vote-cache python3 -I pipeline/d2_labels.py
"""
import collections
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fetch as F  # noqa: E402

REPO = os.path.dirname(HERE)
LINE = 0.005
YEARS = (2018, 2020, 2022, 2024)
CHECK = os.path.join(REPO, "data", "congress", "check-totals.json")
TAG = "the record's total (pipeline/d2_labels.py): "
MEDSL = os.path.join(F.CACHE, "medsl", "normalized")
NCSBE = os.path.join(F.CACHE, "ncsbe", "normalized", "2020_11_03.jsonl")
IN_ENR = os.path.join(F.CACHE, "in_enr", "normalized", "2024General.jsonl")
NOT_NAMES = re.compile(r"^(STATE BALLOTS|ELIGIBLE|OVER ?VOTES?|UNDER ?VOTES?|BLANKS?|VOID)$", re.I)
NY_2018 = ("no second count: MEDSL's 2018 New York file is held (data/local/check-volume.json) and New York's State "
           "Board refused us (2026-11-07 18:49); the record's nominees are each at every party line, from Algara and "
           "Amlani's county returns (pipeline/governor_counts.py; the orchestrator, 2026-11-13 04:44), where Cha, "
           "Kuriwaki and Snyder give the party's line alone (M2's reading, checks/M2-REPORT.md section 14.1 item 10)")


def _surname(name):
    n = re.sub(r"\([^)]*\)|\"[^\"]*\"", " ", name.upper())
    if "," in n:
        return re.sub(r"[^A-Z]", "", n.split(",")[0])
    n = n.split(" AND ")[0].split(" & ")[0]
    toks = [re.sub(r"[^A-Z]", "", t) for t in n.split()]
    toks = [t for t in toks if t and t not in ("JR", "SR", "II", "III", "IV")]
    return toks[-1] if toks else ""


def second(year, st):
    """The second count of a state's governor contest: (source, [(name, votes, write_in)]) or None."""
    if year == 2020:
        if st != "NC" or not os.path.exists(NCSBE):
            return None
        for line in open(NCSBE):
            c = json.loads(line)
            if c.get("contest") == "NC GOVERNOR":
                return ("North Carolina's State Board of Elections (results_pct_20201103.zip)",
                        [(x["name"], x["votes"], False) for x in c["choices"]])
        return None
    if year == 2024 and st == "IN":
        for line in open(IN_ENR):
            c = json.loads(line)
            if c.get("title", "").startswith("Governor"):
                return ("Indiana's results archive of the 2024 general (its data says Certified: T)",
                        [(x["name"].replace("(W/I)", "").strip(), x["votes"], "(W/I)" in x["name"])
                         for x in c["candidates"]])
        return None
    if year == 2018 and st == "NY":
        return None
    ms = []
    for p_ in glob.glob(os.path.join(MEDSL, str(year), f"{st}-*.jsonl")):
        for line in open(p_):
            m = json.loads(line)
            if m["office"] == "GOVERNOR" and m["stage"] == "GEN" and not m["special"]:
                ms.append((os.path.basename(p_), m))
    if len(ms) != 1:
        return None
    name, m = ms[0]
    return (f"MEDSL's precinct file ({m['file']['name'] if isinstance(m.get('file'), dict) else name})",
            [(x["name"], x["votes"] or 0, bool(x.get("writein")) or x["name"].strip().upper() in
              ("WRITEIN", "WRITE-IN", "SCATTERING", "UNQUALIFIED WRITE-IN"))
             for x in m["candidates"] if not NOT_NAMES.match(x["name"].strip())])


def governors(out):
    edits = {}
    for year in YEARS:
        path = os.path.join(REPO, "data", "governor", f"{year}.json")
        with open(path) as f:
            d = json.load(f)
        for r in d["contests"]:
            if r.get("special") or not r["result"].get("total_votes"):
                continue
            st, res = r["place"]["state"], r["result"]
            s = second(year, st)
            row = {"id": r["id"], "total_votes": res["total_votes"], "candidates": len(res["candidates"])}
            if s is None:
                row["second"] = None
                if (year, st) == (2018, "NY"):
                    row["note"] = NY_2018
                out.append(row)
                continue
            src, cs = s
            tot = sum(v for _, v, _ in cs)
            ballot = [(n, v) for n, v, w in cs if not w]
            wi = sum(v for _, v, w in cs if w)
            mine = {_surname(c["name"]) for c in res["candidates"]}
            others = [(n, v) for n, v in ballot if _surname(n) not in mine and v]
            pairs = []
            for c in res["candidates"]:
                hit = [(n, v) for n, v in ballot if _surname(n) == _surname(c["name"])]
                pairs.append([c["name"], c["votes"], hit[0][1] if len(hit) == 1 else None])
            x = tot / res["total_votes"] - 1
            row.update({"second": src, "second_total": tot, "off": round(x, 5), "ballot_names_second": len(ballot),
                        "others_second": others, "write_ins_second": wi, "pairs": pairs})
            out.append(row)
            if abs(x) <= LINE:
                continue
            what = []
            if others:
                of = f"the {len(res['candidates'])} candidates the source lists"
                what.append(f"total_votes adds up only the {len(res['candidates'])} candidates the source lists "
                            f"({', '.join(c['name'] for c in res['candidates'])}); {src} names "
                            f"{len(ballot)} on the ballot, the others " + ", ".join(f"{n} {v:,}" for n, v in others))
            else:
                of = "the names on the ballot"
                what.append("total_votes adds up the names on the ballot")
            if wi:
                what.append(f"{src} counts {wi:,} write-in votes, which the source leaves out")
            diff = [f"{n}: {a:,} in the source, {b:,} there" for n, a, b in pairs if b is not None and a != b]
            if diff:
                what.append("the candidates' own figures differ: " + "; ".join(diff))
            note = (TAG + "; ".join(what) + f"; there the contest's votes add up to {tot:,}, {100 * x:+.1f}% "
                    "[measured]. The candidates' figures, the two-party votes and n are the source's; a governor's p "
                    "rests on the two leaders' votes, not on total_votes (the orchestrator, 2026-11-07 22:19, item 5; "
                    "M2's seventh pass, section 14.1 item 10)")
            edits[r["id"]] = (of, note)
    return edits


def me02():
    rid = "2024-house-ME-02"
    note = (TAG + "the Clerk's statistics print the ranked-choice count's last round, Golden 197,151 and Theriault "
            "194,445, with 'Continuing Ballots' 391,596 (their votes added up) and 'Exhausted Ballots' 11,340 as lines; "
            "these two are kept as result.rcv_lines, not candidates, total_votes is the two candidates' last-round "
            "votes, and the two-party pair is Golden and Theriault (M2's seventh pass, section 14.1 item 14; the "
            "orchestrator, 2026-11-07 22:19, item 5). The first round is not in the Clerk's statistics")

    def fix(rec):
        res = rec["result"]
        lines = [c for c in res["candidates"] if c["name"] in ("Continuing Ballots", "Exhausted Ballots")]
        if lines:
            res["candidates"] = [c for c in res["candidates"] if c not in lines]
            res["rcv_lines"] = lines
        cands = sorted(res["candidates"], key=lambda c: -c["votes"])
        if len(cands) != 2 or sum(c["votes"] for c in cands) != 391596:
            raise SystemExit(f"d2_labels: {rid}: the candidates are not the two of the last round: {cands}")
        res["total_votes"] = sum(c["votes"] for c in cands)
        res["total_votes_of"] = "the two candidates' votes in the ranked-choice count's last round"
        rec["two_party"] = {"candidates": [c["name"] for c in cands], "votes": [c["votes"] for c in cands],
                            "n_other_voters": sum(c["votes"] for c in cands) - 1,
                            "share_first": round(cands[0]["votes"] / sum(c["votes"] for c in cands), 6)}
        for ch in rec.get("checks") or []:
            ch["differences"] = [x for x in ch.get("differences") or []
                                 if not x.startswith(("Continuing Ballots", "Exhausted Ballots"))]
        # the ballot's count of others and the reason p is not computed were read from the two lines taken out: the
        # Clerk's statistics print the last round only, so who else was on the first round's ballot is not read
        b = rec.get("ballot") or {}
        if b.get("others") == 2 or b.get("others_not_read"):
            b["others"] = None
            b["others_not_read"] = ("the Clerk's statistics print the ranked-choice count's last round only; the 2 "
                                    "others counted before were its 'Continuing Ballots' and 'Exhausted Ballots' lines")
        if rec["p"].get("not_computed", "").startswith("counted by ranked choice"):
            rec["p"]["not_computed"] = ("counted by ranked choice (Maine from 2018): the Clerk's statistics print the "
                                        "count's last round only, so its first round, and who else was on the "
                                        "ballot, are not read (model section 7)")
        rec["notes"] = [x for x in rec["notes"] if not x.startswith(TAG)] + [note]
        return rec
    return rid, fix


def rewrite(path, fixes):
    """Each record of `fixes` ({id: function}) rewritten on its own line, the file otherwise as it is."""
    with open(path) as f:
        lines = f.read().split("\n")
    done = []
    for rid, fn in fixes.items():
        at = [i for i, l in enumerate(lines) if l.startswith('  {"id":"' + rid + '"')]
        if len(at) != 1:
            raise SystemExit(f"d2_labels: {rid} is found {len(at)} times in {path}")
        line = lines[at[0]]
        comma = line.endswith(",")
        rec = fn(json.loads(line.strip().rstrip(",")))
        new = "  " + json.dumps(rec, separators=(",", ":"), ensure_ascii=False) + ("," if comma else "")
        if new != line:
            lines[at[0]] = new
            done.append(rid)
    with open(path, "w") as f:
        f.write("\n".join(lines))
    return done


def main():
    rows = []
    edits = governors(rows)
    changed = []
    for year in YEARS:
        path = os.path.join(REPO, "data", "governor", f"{year}.json")
        mine = {rid: e for rid, e in edits.items() if rid.startswith(f"{year}-")}

        def fixer(of, note):
            def fn(rec):
                rec["result"]["total_votes_of"] = of
                rec["notes"] = [x for x in rec["notes"] if not x.startswith(TAG)] + [
                    note if note.startswith(TAG) else TAG + note]
                return rec
            return fn

        def unlabel(rec):
            # a record labelled before whose total now agrees with the second count, or that has none (Connecticut
            # and New York 2018, Indiana 2024 since pipeline/governor_counts.py): the label and its note are taken off
            rec["result"].pop("total_votes_of", None)
            rec["notes"] = [x for x in rec["notes"] if not x.startswith(TAG)]
            return rec
        with open(path) as f:
            stale = [c["id"] for c in json.load(f)["contests"]
                     if c["id"] not in mine and any(x.startswith(TAG) for x in c.get("notes") or [])]
        changed += rewrite(path, {**{rid: fixer(of, note) for rid, (of, note) in mine.items()},
                                  **{rid: unlabel for rid in stale}})
    rid, fn = me02()
    changed += rewrite(os.path.join(REPO, "data", "house", "2024.json"), {rid: fn})
    with open(os.path.join(REPO, "data", "state-lower", "2002", "NC.json")) as f:
        nc = next(c for c in json.load(f)["contests"] if c["id"] == "2002-state-lower-NC-118")
    out = {"about": ("D2's governor totals of 2018-2024 against a second count of each contest, and the two items with "
                     "nothing to fix (pipeline/d2_labels.py; the orchestrator, 2026-11-07 22:19, item 5; M2's seventh "
                     "pass, checks/M2-REPORT.md section 14.1). off: the second count's total over the record's, less "
                     "1; a record off by more than 0.5% says what its total adds up (result.total_votes_of) and "
                     "carries a note"),
           "line": LINE, "governors": rows, "relabelled": sorted(edits),
           "me02": {"id": rid, "fixed": "the ranked-choice lines out of the candidates (result.rcv_lines)"},
           "nc_2002_house_118": {"id": nc["id"], "total_votes": nc["result"]["total_votes"],
                                 "candidates": [[c["name"], c["votes"]] for c in nc["result"]["candidates"]],
                                 "reading": ("nothing to fix: the record holds the State Board's certified counts "
                                             "(its note); Klarner's contest file total, 125,193, adds its candidate "
                                             "file's 113,717 for Rapp, whom the Board counts at 13,717 [measured]")},
           "nd_2024_governor": {"reading": ("nothing to fix: MEDSL's 2024 North Dakota file lacks the governor's rows "
                                            "in Burleigh and Divide Counties with the president whole (M2's seventh "
                                            "pass, item 7); the record's count is the dataset's, and no p of D3's "
                                            "rests on those rows (the legislature's rows are present)")}}
    with open(CHECK, "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"relabelled {len(edits)}: {sorted(edits)}; lines rewritten {len(changed)}")
    for r in rows:
        if r.get("off") is not None and abs(r["off"]) > LINE:
            print(f"  {r['id']}: {r['total_votes']:,} vs {r['second_total']:,} ({100 * r['off']:+.1f}%), "
                  f"others {r['others_second']}, write-ins {r['write_ins_second']:,}")


if __name__ == "__main__":
    main()
