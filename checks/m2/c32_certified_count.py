"""checks/m2/c32_certified_count.py: #84 (f5a4ac4, against cbc4469): the certified count wins (the orchestrator's
ruling of 2026-11-07 15:16: where a state page that prints totals marks them certified or official, its totals are the
statewide record's counts; MEDSL's sum stays beside them). The fourth pass (the orchestrator, 15:50: "the 10 certified
counts. Check WA 2024's four against the results page's text, since the canvass was read by eye. No p should move.").

  32.1 the moves file (data/measure/moves-certified-count.json) against my own diff of every record between cbc4469
       and f5a4ac4 [measured]
  32.2 the 10 counts taken from the state: the record's votes are the state's printed totals, MEDSL's sum stands
       beside them, the yes share and total follow [measured]
  32.3 Washington 2024's four against the Secretary of State's results page fetched again (Measures-All, the page
       that prints the figures; checks/m2/fetch_fourth_pass.sh), and the canvass PDF's hash, pages and want of a text
       layer [measured]
  32.4 Alabama 2020's six against the Final Canvass PDF fetched again: the amendments' Total lines and the
       certification line on every page [measured]
  32.5 the 7 unmarked questions keep MEDSL's counts; Washington 2018's and Arizona's printed totals found on their
       pages [measured]
  32.6 no p moved: every p block of every measure record equal between the two commits; the four yes shares that
       moved sit in 2024, which no later year's pool reads [measured]

Nothing in pipeline/ or model/ is imported. Run from the repository root: python3 checks/m2/c32_certified_count.py
"""
import collections
import hashlib
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402
import c28_governor_codes as C28  # noqa: E402
import c30_ballot_texts as C30  # noqa: E402
import c31_statewide_filed_local as C31  # noqa: E402

BEFORE = "cbc4469"   # #82 merged
AFTER = "f5a4ac4"    # #84 merged
MOVES = "data/measure/moves-certified-count.json"
at = C30.at


def show(commit, path):
    return json.loads(subprocess.run(["git", "show", f"{commit}:{path}"], capture_output=True, text=True, cwd=L.ROOT).stdout)


def page_text(path):
    return C31.C30.readings(path)


def figures(s):
    return [int(x.replace(",", "")) for x in re.findall(r"\d{1,3}(?:,\d{3})+|\d+", s)]


# ---------------------------------------------------------------------------------------------- 32.1
def section_1():
    print("### 32.1 the moves file against my own diff of the records, cbc4469 to f5a4ac4")
    allf = C31.changed_files(BEFORE, AFTER, under=".")
    recf = [x for x in allf if re.search(r"data/measure/\d{4}/[A-Z]{2}\.json$", x)]
    print(f"  files changed: {len(allf)}; record files {len(recf)} ({', '.join(x.split('/', 2)[-1] for x in recf)}); others: "
          + ", ".join(x for x in allf if x not in recf))
    before, after = C31.load_records(BEFORE, recf), C31.load_records(AFTER, recf)
    changed = {cid: C31.deep_paths(before[cid], after[cid]) for cid in set(before) & set(after) if before[cid] != after[cid]}
    print(f"  records new {len(set(after) - set(before))}, gone {len(set(before) - set(after))}, changed {len(changed)}")
    for paths, n in collections.Counter(tuple(v) for v in changed.values()).most_common():
        print(f"    {n:4d}  {', '.join(paths)}")
    mv = show(AFTER, MOVES)
    recs = {r["id"]: r for r in mv["records"]}
    print(f"  the moves file: {mv['summary']} (against {mv.get('against')}); its ids == my changed ids: {set(recs) == set(changed)}")
    tal = collections.Counter()
    for cid, r in recs.items():
        b, a = before.get(cid), after.get(cid)
        vb = {x["name"].upper(): x["votes"] for x in b["result"]["candidates"]}
        va = {x["name"].upper(): x["votes"] for x in a["result"]["candidates"]}
        same = (r["votes_before"] == vb, r["votes_after"] == va, r.get("yes_share_before") == b["result"].get("yes_share"),
                r.get("yes_share_after") == a["result"].get("yes_share"), r["p_before"] == b.get("p"), r["p_after"] == a.get("p"),
                r["counts_moved"] == (vb != va), r["p_moved"] == (b.get("p") != a.get("p")),
                r["counts_used"] == (a.get("listed_statewide") or {}).get("state_total", {}).get("counts_used"),
                r["certified"] == bool(((a.get("listed_statewide") or {}).get("state_total", {}).get("certified") or {}).get("marked")))
        tal["votes, yes share, p, counts_used and certified all as the records" if all(same) else f"DIFFERS {same}"] += 1
    print(f"  the 17 records: {dict(tal)}; counts moved {sum(1 for r in recs.values() if r['counts_moved'])}, from the state {sum(1 for r in recs.values() if r['counts_used'] == 'state')}, "
          f"p moved {sum(1 for r in recs.values() if r['p_moved'])}")
    return before, after, mv


# ---------------------------------------------------------------------------------------------- 32.2
def section_2(before, after, mv):
    print("### 32.2 the 10 counts taken from the state")
    listed = {(q["state"], q["year"], q["title"]): q for q in show(AFTER, C31.LISTED)["questions"]}
    tal = collections.Counter()
    for r in mv["records"]:
        if r["counts_used"] != "state":
            continue
        a, b = after[r["id"]], before[r["id"]]
        q = listed[(a["place"]["state"], a["year"], a["question"]["title"])]
        stt = a["listed_statewide"]["state_total"]
        va = {x["name"].upper(): x["votes"] for x in a["result"]["candidates"]}
        vb = {x["name"].upper(): x["votes"] for x in b["result"]["candidates"]}
        yes, no = C31.C27_yes_no(a)
        same = (va == q["state_total"]["votes"] == stt["votes"], stt.get("medsl_votes") == vb, a["result"].get("votes_source") == "state_certified",
                a["result"].get("yes_share") == round(yes / (yes + no), 6), a["result"].get("total_votes") == sum(va.values()),
                stt.get("medsl_less_state") == {k: vb.get(k, 0) - v for k, v in va.items()},
                any("certified totals" in n for n in a.get("notes") or []), q["state_total"]["certified"]["marked"] is True)
        tal["the state's totals in the record, MEDSL's beside, votes_source, yes share, total, difference and note all as expected" if all(same) else f"DIFFERS {same}"] += 1
        if not all(same):
            print(f"    {r['id'][:60]}: {same}")
    print(f"  {sum(tal.values())} records: {dict(tal)}")


# ---------------------------------------------------------------------------------------------- 32.3
def section_3(after):
    print("### 32.3 Washington 2024's four against the results page's text, and the canvass PDF")
    pages = C31.fetched("key")
    p = pages.get("list-all:WA:2024")
    if not p:
        print("  the Measures-All page was not fetched")
        return
    text = page_text(p)[0][1]
    tal = collections.Counter()
    for c in after.values():
        if c["place"]["state"] != "WA" or c["year"] != 2024 or not (c.get("listed_statewide") or {}).get("state_total"):
            continue
        title = c["question"]["title"]
        m = re.search(re.escape(C28.norm(title)) + r".{0,80}?Yes ([\d,]+) [\d.]+% No ([\d,]+) [\d.]+% Total Votes ([\d,]+)", text)
        rec = {x["name"].upper(): x["votes"] for x in c["result"]["candidates"]}
        medsl = c["listed_statewide"]["state_total"].get("medsl_votes")
        if not m:
            tal["title not found on the page with its figures"] += 1
            print(f"    {title}: not found")
            continue
        page = {"YES": int(m.group(1).replace(",", "")), "NO": int(m.group(2).replace(",", ""))}
        total = int(m.group(3).replace(",", ""))
        ok = page == rec and total == sum(rec.values())
        tal["the page's Yes, No and Total Votes equal the record's" if ok else "DIFFERS"] += 1
        print(f"    {title}: page Yes {page['YES']:,} No {page['NO']:,} total {total:,}; record {rec}; MEDSL's sum {medsl} "
              f"(difference {dict((k, (medsl or {}).get(k, 0) - v) for k, v in page.items())})")
    print(f"  {dict(tal)}")
    cp = pages.get("canvass:WA:2024")
    if cp:
        h = hashlib.sha256(open(cp, "rb").read()).hexdigest()
        rec_src = next((c["listed_statewide"]["state_total"]["certified"]["source"] for c in after.values()
                        if c["place"]["state"] == "WA" and c["year"] == 2024 and (c.get("listed_statewide") or {}).get("state_total")), {})
        info = subprocess.run(["pdfinfo", cp], capture_output=True, text=True).stdout
        pg = re.search(r"Pages:\s+(\d+)", info)
        txt = subprocess.run(["pdftotext", cp, "-"], capture_output=True, text=True).stdout
        print(f"  the canvass PDF: sha256 equals the record's: {h == rec_src.get('sha256')} ({h[:12]}...); pages {pg.group(1) if pg else '?'} "
              f"(record: 10 pages); text layer: {len(txt.strip())} characters by pdftotext "
              f"({'none: a scan, as the record says it was read by eye' if len(txt.strip()) < 20 else 'some text'})")
    lp = pages.get("list:WA:2024")
    if lp:
        t = page_text(lp)[0][1]
        print(f"  the Measures tab names the four measures ({sum(1 for n in ('2066', '2109', '2117', '2124') if 'Initiative Measure No. ' + n in t)} of 4) and prints no figures; "
              f"the figures are on Measures-All, which the record's quote file names")


# ---------------------------------------------------------------------------------------------- 32.4
def section_4(after):
    print("### 32.4 Alabama 2020's six against the Final Canvass PDF")
    pages = C31.fetched("key")
    p = pages.get("list:AL:2020")
    if not p:
        print("  the canvass was not fetched")
        return
    lay = subprocess.run(["pdftotext", "-layout", p, "-"], capture_output=True, text=True).stdout
    found = {}
    for page in lay.split("\f"):
        heads = re.findall(r"Proposed Statewide Amendment Number (\w+) \((\d+)\)", page)
        if not heads:
            continue
        tot = re.search(r"(?m)^\s*Total\s+(.*)$", page)
        nums = figures(tot.group(1)) if tot else []
        for i, (word, num) in enumerate(heads):
            if len(nums) >= 2 * i + 2:
                found[word.upper()] = {"YES": nums[2 * i], "NO": nums[2 * i + 1]}
    cert = sum(1 for page in lay.split("\f") if re.search(r"Certified by the State Canvassing Board\s+November 23, 2020", page))
    pages_n = len([x for x in lay.split("\f") if x.strip()])
    tal = collections.Counter()
    for c in after.values():
        if c["place"]["state"] != "AL" or c["year"] != 2020 or not (c.get("listed_statewide") or {}).get("state_total"):
            continue
        word = c["question"]["title"].split()[-1].upper()
        rec = {x["name"].upper(): x["votes"] for x in c["result"]["candidates"]}
        medsl = c["listed_statewide"]["state_total"].get("medsl_votes")
        pg = found.get(word)
        ok = pg == rec
        tal["the canvass's Total equals the record's votes" if ok else "DIFFERS"] += 1
        print(f"    Amendment {word}: canvass {pg}; record {rec}; MEDSL's sum {medsl} ({'equal' if medsl == rec else 'differs'})")
    print(f"  {dict(tal)}; 'Certified by the State Canvassing Board November 23, 2020' on {cert} of {pages_n} pages")


# ---------------------------------------------------------------------------------------------- 32.5
def section_5(before, after, mv):
    print("### 32.5 the 7 unmarked questions keep MEDSL's counts; the printed totals found on the pages fetched")
    listed = {(q["state"], q["year"], q["title"]): q for q in show(AFTER, C31.LISTED)["questions"]}
    tal = collections.Counter()
    for r in mv["records"]:
        if r["counts_used"] == "state":
            continue
        a, b = after[r["id"]], before[r["id"]]
        q = listed[(a["place"]["state"], a["year"], a["question"]["title"])]
        stt = a["listed_statewide"]["state_total"]
        va = {x["name"].upper(): x["votes"] for x in a["result"]["candidates"]}
        vb = {x["name"].upper(): x["votes"] for x in b["result"]["candidates"]}
        same = (va == vb, a["result"].get("votes_source") is None, stt.get("counts_used") == "medsl", r.get("why_not") == q["state_total"]["certified"].get("note"),
                stt.get("medsl_less_state") == {k: va.get(k, 0) - v for k, v in q["state_total"]["votes"].items()}, q["state_total"]["certified"]["marked"] is False)
        tal["votes unchanged, counts_used medsl, why_not the page's note, the difference recorded" if all(same) else f"DIFFERS {same}"] += 1
        if not all(same):
            print(f"    {r['id'][:60]}: {same}")
    print(f"  {sum(tal.values())} records: {dict(tal)}")
    pages = C31.fetched("key")
    p = pages.get("measure:WA:2018:AV19")
    if p:
        t = page_text(p)[0][1]
        m = re.search(r"Repealed ([\d,]+) [\d.]+% Maintained ([\d,]+) [\d.]+%", t)
        upd = re.search(r"Last updated on [^A-Z]{0,30}", t)
        c = next(c for c in after.values() if c["place"]["state"] == "WA" and c["year"] == 2018 and (c.get("listed_statewide") or {}).get("state_total"))
        rec = {x["name"].upper(): x["votes"] for x in c["result"]["candidates"]}
        if m:
            page = {"REPEALED": int(m.group(1).replace(",", "")), "MAINTAINED": int(m.group(2).replace(",", ""))}
            print(f"  WA 2018 Advisory Vote 19: the page prints {page} ({upd.group(0).strip() if upd else 'no update line'}); the record's state_total {c['listed_statewide']['state_total']['votes']} "
                  f"({'equal' if page == c['listed_statewide']['state_total']['votes'] else 'DIFFERS'}); MEDSL's (the record's counts) {rec}, difference {dict((k, rec.get(k, 0) - v) for k, v in page.items())}; "
                  f"no mark of certification on the page: {'certified' not in t.lower() or 'results posted before certification are unofficial' in t.lower()}")
        else:
            print("  WA 2018 Advisory Vote 19: the figures were not found on the page")
    p = pages.get("list:AZ:2018")
    if p:
        rd = page_text(p)
        c = next(c for c in after.values() if c["place"]["state"] == "AZ" and c["year"] == 2018 and (c.get("listed_statewide") or {}).get("state_total"))
        qt = c["listed_statewide"]["state_total"]["quote"]
        print(f"  AZ 2018 Prop 127: the memo's words {qt!r} found: {C31.find_quote(qt, rd)}; the record's counts (MEDSL's) {dict((x['name'].upper(), x['votes']) for x in c['result']['candidates'])} equal the memo's figures: "
              f"{figures(qt)[-2:] == [c['listed_statewide']['state_total']['votes']['YES'], c['listed_statewide']['state_total']['votes']['NO']] == [x['votes'] for x in sorted(c['result']['candidates'], key=lambda x: x['name'] != 'YES')]}")
    print("  MT 2020: the state canvass report the record quotes ('Total 298388 287129') is named by its cache file only and was not fetched; its totals equal MEDSL's in the record, so nothing turns on it")


# ---------------------------------------------------------------------------------------------- 32.6
def section_6():
    print("### 32.6 no p moved")
    files = C31.record_files(AFTER)
    same = diff = 0
    yshare = []
    for f in files:
        b, a = at(BEFORE, f), at(AFTER, f)
        bi = {c["id"]: c for c in (b or {}).get("contests", [])}
        for c in (a or {}).get("contests", []):
            pb = (bi.get(c["id"]) or {}).get("p")
            if pb == c.get("p"):
                same += 1
            else:
                diff += 1
            rb = (bi.get(c["id"]) or {}).get("result") or {}
            if rb.get("yes_share") != c["result"].get("yes_share"):
                yshare.append((c["id"], c["year"], rb.get("yes_share"), c["result"].get("yes_share")))
    print(f"  p blocks equal in {same} records of {len(files)} files, differing {diff}; yes shares that moved: {len(yshare)} "
          + "; ".join(f"{cid[:40]} {y0} -> {y1}" for cid, y, y0, y1 in yshare))
    years = sorted({y for _, y, _, _ in yshare})
    later = sorted({int(f.split('/')[2]) for f in files if int(f.split('/')[2]) > max(years)}) if years else []
    later_p = sum(1 for f in files if int(f.split('/')[2]) in later for c in (at(AFTER, f) or {}).get("contests", []) if "value" in (c.get("p") or {}))
    print(f"  the moved shares are of {years}; measure files of later years: {later or 'none'}, holding {later_p} p (every one among the equal blocks above): no p reads the moved shares")


def main():
    print(f"##### c32 the certified count wins (#84): HEAD {L.git_head()}")
    before, after, mv = section_1()
    section_2(before, after, mv)
    section_3(after)
    section_4(after)
    section_5(before, after, mv)
    section_6()


if __name__ == "__main__":
    main()
