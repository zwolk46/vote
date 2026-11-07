"""pipeline/intake/cps_voting.py: how citizens say they voted (in person on Election Day, in person before it, by
mail), by state, from the Current Population Survey November Voting and Registration Supplement, 2020 to 2024.

Source. U.S. Census Bureau and Bureau of Labor Statistics, Current Population Survey, November 2020, 2022 and 2024
Voting and Registration Supplement, public-use microdata (CSV) and technical documentation (PDF), from
https://www2.census.gov/programs-surveys/cps/ (the links of the Census page
https://www.census.gov/data/datasets/time-series/demo/cps/cps-supp_cps-repwgt/cps-voting.html). A publication of a U.S.
Government agency; the pages print no licence or terms [measured, 2026-11-07].
November 2016 and 2018 are published only as fixed-width files (nov16pub.dat.gz, nov18pub.dat.gz) with other column
positions; they are listed in data/sources/cost.md and not taken in this run.

Items (the technical documentation's own wording):
  PES1  "Did (you/name) vote in the election held on Tuesday, November [date]?"      1 Yes  2 No  (-2 don't know, -3 refused)
  PES5  "Did (you/he/she) vote in person or did (you/he/she) vote by mail?"             1 In person  2 By mail
  PES6  "Was that on election day or before election day?"                              1 On election day  2 Before election day
Universe: citizens aged 18 or more (PRTAGE >= 18 and PRCITSHP 1 to 4). Weight: PWSSWGT, the basic CPS weight, which the
documentation says to use "for tallying the supplement items" (there is no supplement weight). State: GESTFIPS.

What is computed, per state and year (weighted by PWSSWGT; shares are [inferred] from the items, the answers are
[measured] self-reports):
  voted_share        PES1 = 1 over PES1 = 1 or 2 (don't know, refused and no response left out of the denominator);
  mail_share         PES5 = 2 over voters with a valid PES5;
  early_in_person    PES5 = 1 and PES6 = 2, over voters with a valid PES5 (and, for in-person voters, a valid PES6);
  election_day       PES5 = 1 and PES6 = 1, same denominator.
The unweighted answer counts of PES1, PES5 and PES6 are checked against the tallies the technical documentation prints;
the run fails if one differs. A Kish effective sample size, (sum w)^2 / sum w^2, and a design-naive standard error
sqrt(p (1 - p) / n_eff) are recorded; the CPS design clusters households, so the true error is larger (the replicate
weights, which would give it, are in the "rep" files and are not read here).

Run: python3 pipeline/intake/cps_voting.py        (about 450 MB of downloads into the cache, once; writes data/cost/cps-voting.json)
"""
import csv
import json
import os
import re
import subprocess
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import congress_common as cc  # noqa: E402
from bls_earnings import STATES  # noqa: E402

B = "https://www2.census.gov/programs-surveys/cps/"
YEARS = {2024: "24", 2022: "22", 2020: "20"}
PAGE = "https://www.census.gov/data/datasets/time-series/demo/cps/cps-supp_cps-repwgt/cps-voting.html"


def tallies(text, var):
    """The value -> count lines of the documentation's tallies for var (its last, frequency-table, appearance).
    Layouts differ by year: the variable name stands alone above the values (2022, 2024), or on the line of the first
    value (2020)."""
    out = {}
    lines = text.splitlines()
    starts = [i for i, ln in enumerate(lines)
              if re.match(rf"^\s*{var}\s+-?\d+\s+\S.*[\d,]+\s*$", ln)
              or (re.match(rf"^\s*{var}\s{{2,}}\S", ln) and not re.search(r"\d{4}-\d{4}\s*$", ln) and i > 0
                  and "TALLIES" in " ".join(lines[max(0, i - 8):i]))]
    if not starts:
        return out
    i = starts[-1]
    for ln in lines[i:i + 40]:
        ln2 = re.sub(rf"^\s*{var}\b", "", ln)
        m = re.match(r"^\s+(-?\d+)\s+.*?\s([\d,]{2,})\s*$", ln2)
        if m:
            out[int(m.group(1))] = int(m.group(2).replace(",", ""))
        elif ln is not lines[i] and re.match(r"^\s*(PE|PR|PU|HU|GE|HR|PW|PT)[A-Z0-9]+\s", ln):
            break
    return out


def main():
    out = {"about": "How citizens say they voted, by state, from the CPS November Voting and Registration Supplement (see pipeline/intake/cps_voting.py).",
           "years": {}, "unread": [{"what": "November 2016 and 2018 supplements", "reason": "fixed-width files with other column positions; not taken in this run"},
                                    {"what": "CPS replicate weights (nov20rep, nov22rep, nov24rep)", "reason": "the standard errors here are design-naive; the replicate files would give design-based ones"}]}
    for y, yy in sorted(YEARS.items()):
        rec = cc.fetch(f"{B}datasets/{y}/supp/nov{yy}pub.csv", f"cost/cps/nov{yy}pub.csv", min_bytes=10_000_000)
        doc = cc.fetch(f"{B}techdocs/cpsnov{yy}.pdf", f"cost/cps/cpsnov{yy}.pdf", min_bytes=100000)
        txt = os.path.join(cc.CACHE, doc["path"][:-4] + ".txt")
        if not os.path.exists(txt):
            subprocess.run(["pdftotext", "-layout", os.path.join(cc.CACHE, doc["path"]), txt], check=False, stderr=subprocess.DEVNULL)
        doc_text = open(txt, encoding="utf-8", errors="replace").read()
        want = {v: tallies(doc_text, v) for v in ("PES1", "PES5", "PES6")}
        got = {v: defaultdict(int) for v in want}
        acc = defaultdict(lambda: defaultdict(float))
        nn = defaultdict(lambda: defaultdict(int))
        with open(os.path.join(cc.CACHE, rec["path"]), encoding="utf-8", errors="replace", newline="") as fh:
            rd = csv.DictReader(fh)
            cols = {c.upper(): c for c in rd.fieldnames}
            need = ["PES1", "PES5", "PES6", "GESTFIPS", "PWSSWGT", "PRTAGE", "PRCITSHP"]
            missing = [c for c in need if c not in cols]
            if missing:
                raise ValueError(f"{y}: columns not in the file: {missing}")
            ci = {c: cols[c] for c in need}
            nrows = 0
            for r in rd:
                nrows += 1
                for v in got:
                    try:
                        got[v][int(r[ci[v]])] += 1
                    except ValueError:
                        pass
                try:
                    p1, p5, p6 = int(r[ci["PES1"]]), int(r[ci["PES5"]]), int(r[ci["PES6"]])
                    fips = f"{int(r[ci['GESTFIPS']]):02d}"
                    w = float(r[ci["PWSSWGT"]])
                except ValueError:
                    continue
                st = STATES.get(fips)
                if st is None or p1 not in (1, 2):
                    continue
                a, n = acc[st], nn[st]
                a["w1"] += w; a["w1sq"] += w * w; n["n1"] += 1
                if p1 == 1:
                    a["wv"] += w; n["nv"] += 1
                    if p5 in (1, 2) and (p5 == 2 or p6 in (1, 2)):
                        a["wm_den"] += w; a["wm_den_sq"] += w * w; n["n_mode"] += 1
                        if p5 == 2:
                            a["wmail"] += w
                        elif p6 == 2:
                            a["wearly"] += w
                        else:
                            a["wday"] += w
        mism = {v: {"documentation": want[v], "file": dict(sorted(got[v].items()))} for v in want
                if any(got[v].get(k, 0) != c for k, c in want[v].items()) or not want[v]}
        states = {}
        for st in sorted(acc):
            a, n = acc[st], nn[st]
            neff1 = a["w1"] ** 2 / a["w1sq"]
            pv = a["wv"] / a["w1"]
            rec_st = {"n_citizens_asked": n["n1"], "voted_share": round(pv, 4), "voted_share_se_naive": round((pv * (1 - pv) / neff1) ** 0.5, 4),
                      "n_voters_with_mode": n["n_mode"]}
            if a["wm_den"] > 0:
                neff = a["wm_den"] ** 2 / a["wm_den_sq"]
                for key, num in (("mail_share", "wmail"), ("early_in_person_share", "wearly"), ("election_day_share", "wday")):
                    p = a[num] / a["wm_den"]
                    rec_st[key] = round(p, 4)
                    rec_st[key + "_se_naive"] = round((p * (1 - p) / neff) ** 0.5, 4)
            states[st] = rec_st
        nat_w = sum(a["wm_den"] for a in acc.values())
        natmode = {k: round(sum(a[w] for a in acc.values()) / nat_w, 4) for k, w in (("mail_share", "wmail"), ("early_in_person_share", "wearly"), ("election_day_share", "wday"))}
        src = cc.source_block(f"U.S. Census Bureau, Current Population Survey, November {y} Voting and Registration Supplement, public-use file nov{yy}pub.csv",
                              f"{B}datasets/{y}/supp/nov{yy}pub.csv", rec["read_utc"], "a U.S. Government publication; no licence or terms printed on the page",
                              mark="measured", via=PAGE,
                              note=f"{rec['bytes']} bytes, sha256 {rec['sha256']}; documentation {B}techdocs/cpsnov{yy}.pdf sha256 {doc['sha256']}")
        out["years"][str(y)] = {"source": src, "rows_in_file": nrows,
                                "check_against_documentation_tallies": {"matches": not mism, "differences": mism, "documentation_tallies_read": want},
                                "national_weighted_mode_shares_in_states_and_dc": natmode, "states": states}
        print(y, nrows, "rows; tallies match:", not mism, "; national", natmode)
        if mism:
            print("  DIFFERENCES", json.dumps(mism)[:600])
    dest = os.path.join(cc.DATA, "cost")
    os.makedirs(dest, exist_ok=True)
    with open(os.path.join(dest, "cps-voting.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")


if __name__ == "__main__":
    main()
