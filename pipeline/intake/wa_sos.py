"""pipeline/intake/wa_sos.py: Washington's own results of a general election, its statewide and judicial races.

Written 2026-11-07 by worker D3 on the orchestrator's ruling of 16:47: "(a) Where a contest's lines miss counties that
voted that day, find its other pieces ... (b) Check each joined total against the state's certified total where one is
read. The certified count wins (15:16). ... (d) Fix MEDSL's 3 seats per position in WA 2022 from the state's results."
Reason (the orchestrator): "a shown figure has to be the whole contest's count of record". MEDSL's 2022 Washington file
holds King County's lines as contests of other names [measured], and the Secretary of State's own page says why: "you
can download precinct results from our results exports for every county except for King County" [stated].
Plan section 3a: data comes in by script; raw files stay in a cache outside the repository.

Source: the Secretary of State's results page, https://results.vote.wa.gov/results/<date>/, whose "Export Results" page
(Export.html) links each export as a CSV, export/<date>_StateExecutive.csv, export/<date>_Judicial.csv and
export/<date>_Measures.csv: one row per race and candidate (or answer), "Race","Candidate","Party","Votes",
"PercentageOfTotalVotes","JurisdictionName" [stated: the files].
The page says that "Election results are certified by each county" and that "The Secretary of State certifies final
results"; its link "Certified Election Results (PDF)" (SignedCertification.pdf) answered HTTP 404 on 2026-11-07 at 16:51
UTC [measured], and the exports themselves carry no certified or official mark, so they are read as the state's results,
not its certified totals (the ruling of 15:30: only a printed certified or official mark counts). The site prints no
licence; these are the state's public election returns.

What it does:
  read   fetches the results page, the Export page and the two exports through pipeline/fetch.py (4 s between requests;
         a refusal stops it), checks that the Export page links both files, and writes
         $VOTE_CACHE/wa_sos/normalized/<date>-statewide.json: {"races": {race: [{candidate, party, votes}]}, ...}.

Run:  VOTE_CACHE=/tmp/vote-cache python3 pipeline/intake/wa_sos.py read --date 20221108
"""
import argparse
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import fetch as F  # noqa: E402

BASE = "https://results.vote.wa.gov/results/{date}/"
FILES = ("StateExecutive", "Judicial", "Measures")
ROOT = os.path.join(F.CACHE, "wa_sos")
NORM = os.path.join(ROOT, "normalized")
for _d in ("raw", "normalized"):   # fetch.py makes the cache itself, not folders inside it
    os.makedirs(os.path.join(ROOT, _d), exist_ok=True)
LICENCE = "no licence printed; the Washington Secretary of State's election returns, public records"
CERT_404 = ("the page's link 'Certified Election Results (PDF)' (SignedCertification.pdf) answered HTTP 404 on "
            "2026-11-07 at 16:51 UTC; the exports carry no certified or official mark")


def read(date):
    base = BASE.format(date=date)
    page = F.fetch(base, f"wa_sos/raw/{date}-results.html")
    exp = F.fetch(base + "Export.html", f"wa_sos/raw/{date}-export.html")
    with open(exp, encoding="utf-8", errors="replace") as f:
        e = f.read()
    races, files = {}, {}
    for name in FILES:
        rel = f"export/{date}_{name}.csv"
        if rel not in e:
            raise SystemExit(f"wa_sos: the Export page does not link {rel}")
        cache = f"wa_sos/raw/{date}_{name}.csv"
        path = F.fetch(base + rel, cache)
        files[name] = F.meta(cache)
        with open(path, encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                races.setdefault(row["Race"].strip(), []).append(
                    {"candidate": row["Candidate"].strip(), "party": row["Party"].strip(), "votes": int(row["Votes"])})
    res = {"date": date, "page": dict(F.meta(f"wa_sos/raw/{date}-results.html")),
           "export_page": dict(F.meta(f"wa_sos/raw/{date}-export.html")), "files": files, "licence": LICENCE,
           "certified": {"marked": False, "note": CERT_404}, "races": races}
    with open(os.path.join(NORM, f"{date}-statewide.json"), "w") as f:
        json.dump(res, f, indent=1)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("what", choices=["read"])
    ap.add_argument("--date", default="20221108")
    a = ap.parse_args()
    res = read(a.date)
    for r, cs in res["races"].items():
        if "Supreme" in r or "SUPREME" in r or "Secretary" in r:
            print(r, cs)


if __name__ == "__main__":
    main()
