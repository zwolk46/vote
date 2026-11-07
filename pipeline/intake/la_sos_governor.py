"""pipeline/intake/la_sos_governor.py: Louisiana's governor contest of an odd year from the Secretary of State's own
results, gated as D3 gates the same year's other contests.

Written 2026-11-07 by worker D2, on the orchestrator's word of 12:01 UTC: "the odd-year governors ... LA 2023 should
equal what D3's check-la.json compared (equal to the SoS)". Reason (the orchestrator): the governor is the most
prominent office on those ballots, and the record skipped it every odd year. Cha, Kuriwaki and Snyder end in 2021, so
Louisiana's 2023 governor comes from the state's own file, the source D3 reads for the rest of that year's ballots.

Source: the Secretary of State's results site, read with D3's own code, unchanged (pipeline/intake/la_sos.py: the
site's list of elections, and each date's workbook; pipeline/local_la.py: the site's posted results of the contests on
more than one parish's ballot). Nothing of D3's is written: the files go into this system's cache under the same
names D3's scripts give them, so either reads the other's.

The gate is D3's for 2023 (the orchestrator, 2026-11-07 11:16: a ballot with no federal contest is gated within the
certifying source): (a) the date is marked official on the site's list ("ResultsOfficial": "1"); (b) the contest's
parishes add up to its total in the workbook; (c) its counts equal, choice by choice, the Secretary of State's own
posted results of that date. A contest that fails any is written with the failure and no result is used.

Which dates: each official date of the year whose posted multi-parish results hold a contest titled "Governor". In
2023 that is 2023-10-14 alone (a candidate had a majority there, so no later round was held for it).

Run from the repository root:  python3 -I pipeline/intake/la_sos_governor.py [2023]
Writes CACHE/la_sos/normalized/governor-<year>.json: {"year", "source", "dates_list", "contests": [{"date", "title",
"candidates": [{"name", "party", "votes"}], "total_votes", "parishes", "gate": {...}, "held"}]}.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import fetch as F  # noqa: E402
from intake import la_sos as SOS  # noqa: E402
import local_la as LA  # noqa: E402

TITLE = "Governor"


def governor(year):
    out = {"year": year, "contests": [], "dates_without": []}
    for dt, pk, official in SOS.elections(year):
        d = str(dt)
        if official != "1":
            out["dates_without"].append(f"{d}: not marked official on the site's list (not read: no live data)")
            continue
        try:
            post, files = LA.posted(d)
        except KeyError:
            # a date whose posted multi-parish file lists no race (D3's reader expects one at least)
            out["dates_without"].append(f"{d}: the posted multi-parish results list no race")
            continue
        if TITLE not in post:
            out["dates_without"].append(f"{d}: no contest titled {TITLE!r} in the posted multi-parish results")
            continue
        name = SOS._xlsx_name(dt)
        F.fetch(SOS.XLSX.format(ymd=f"{dt:%Y%m%d}", mdy=f"{dt:%m-%d-%Y}"), name)
        cs = [c for c in SOS.parse(os.path.join(F.CACHE, name), dt) if c["multi_parish"] and c["title"] == TITLE]
        if len(cs) != 1:
            raise SystemExit(f"{d}: {len(cs)} contests titled {TITLE!r} on the workbook's multi-parish sheet")
        c = cs[0]
        mine = {x["name"]: x["votes"] for x in c["candidates"]}
        hit = post[TITLE]
        equal = hit["votes"] == mine and hit["seats"] == c["seats"]
        why = []
        if not c["lines_add_up"]:
            why.append("its parishes' lines do not add up to its total in the workbook")
        if not equal:
            miss = sum(abs((hit["votes"].get(n) or 0) - v) for n, v in mine.items())
            why.append(f"its counts differ from the Secretary of State's posted results of its date by {miss:,} votes")
        wm = F.meta(name)
        out["contests"].append({
            "date": d, "title": c["title"], "seats": c["seats"], "candidates": c["candidates"],
            "total_votes": sum(x["votes"] for x in c["candidates"]), "parishes": len(c["parishes"]),
            "workbook": {"url": wm["url"], "read_utc": wm["read_utc"], "sha256": wm["sha256"], "bytes": wm["bytes"]},
            "gate": {"by": "within the certifying source (no federal contest on the ballot)",
                     "ruled": "the orchestrator, 2026-11-07 11:16 UTC (D3's gate for Louisiana's 2023 ballots)",
                     "official": True, "parts_add_up": c["lines_add_up"],
                     "posted_results": "equal, choice by choice" if equal else "differ",
                     "posted_files": {w: {"url": m["url"], "read_utc": m["read_utc"], "sha256": m["sha256"]}
                                      for w, m in files.items()}},
            "held": "; ".join(why) or None})
    dm = F.meta(SOS._dates_name())
    out["dates_list"] = {"url": dm["url"], "read_utc": dm["read_utc"], "sha256": dm["sha256"]}
    out["source"] = {"name": "Louisiana Secretary of State, official election results (the results site's workbook of "
                             "each date, and its posted results of the contests on more than one parish's ballot)",
                     "url": SOS.SITE, "licence": SOS.LICENCE}
    os.makedirs(SOS.NORM, exist_ok=True)
    path = os.path.join(SOS.NORM, f"governor-{year}.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    return out


def main(argv):
    for y in [int(a) for a in argv] or [2023]:
        o = governor(y)
        for c in o["contests"]:
            print(f"{y} {c['date']} {c['title']}: {len(c['candidates'])} candidates, {c['total_votes']:,} votes over "
                  f"{c['parishes']} parishes; parts add up {c['gate']['parts_add_up']}; posted results "
                  f"{c['gate']['posted_results']}; held {c['held']}")
        for x in o["dates_without"]:
            print("  " + x)


if __name__ == "__main__":
    main(sys.argv[1:])
