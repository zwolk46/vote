"""pipeline/intake/downballot_pres_by_cd.py: presidential results by congressional district, from
The Downballot (formerly Daily Kos Elections).

Source. The Downballot, "Calculating Statewide Election Results by Congressional and Legislative District:
Statement of Methodology" (first published March 2021, last updated April 2025), Google Doc
1efGEHGAQGaDGnIrdedwxVg1uUrjZYz06IPLTHRCg9zM, and the public Google Sheets it links, read through
Google's documented CSV export (docs.google.com/spreadsheets/d/<id>/export?format=csv). The figures
are The Downballot's calculations from official precinct results; the methodology names the state
office each state's figures come from. No licence is printed on the sheets.

Why this source. The model's own House forecast needs, for each district and election, the presidential
vote in that district on the lines in use at that election, from before the election (model section 3:
"variables known before the election"). The Downballot is the only standardized source of that series
reachable here from 2006 to 2024. (Census and state offices publish lines, not the vote on them.)

Which sheet serves which House election ("lines" = the district map in use at that election):

  House year  lines sheet         presidential vote used before the election
  2024        2024 lines          2020 (counts); for states still on 2022 lines, the 2022-lines sheet
  2022        2022 lines          2020 (one decimal)
  2020        2020 lines          2016
  2018        2018 lines          2016
  2016        2016 lines          2012
  2014        2012-14 lines       2012
  2012        2012-14 lines       2008
  2010        2006-10 lines       2008 (whole percent)
  2008        2006-10 lines       2004 (whole percent)
  2006        2006-10 lines       2004 (whole percent)

The 2024-lines sheet leaves 2020 blank in nine states. The methodology's per-state list says which
lines each state used in 2024 ("The year listed before 'districts' indicates the year of the first
election in which the given districts were first used"): CA, FL, OH, TN, TX and UT used their 2022
districts, so their 2020 figure is read from the 2022-lines sheet, the same map. AL, LA and NC used new
2024 districts; the methodology says 2020 was calculated on them, but not in a sheet this script has
found, so those 28 districts carry no 2020 figure and say so (`missing`).

Run:  python3 pipeline/intake/downballot_pres_by_cd.py
Writes CACHE/downballot/normalized/pres_by_cd.json:
  {"sheets": {key: {...source...}}, "districts": {key: {"AL-01": {"2020": {"D":..,"R":..,"two_party_D":..,
   "unit": "votes|percent"}}}}, "lean_inputs": {house_year: {district: {...}}}, "missing": {...}, "checks": [...]}
Checks: 435 districts per sheet; seats per state equal across the sheets of one decade; two-party
shares inside (0, 1); where two sheets give the same year on the same lines, the difference.
"""
import csv
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import congress_common as cc  # noqa: E402

EXPORT = "https://docs.google.com/spreadsheets/d/{id}/export?format=csv{gid}"
METHOD_DOC = "https://docs.google.com/document/d/1efGEHGAQGaDGnIrdedwxVg1uUrjZYz06IPLTHRCg9zM"
LICENCE = "none printed on the sheets; The Downballot's own calculations from official precinct results"

# key: (sheet id, gid or None, label, {pres year: column of the Democrat; the Republican is the next})
#   columns None -> read from the sheet's year row
SHEETS = {
    "2024": ("1eZfaFI-c-PFOoKx1-zZA2MP0_dxRq_LVK0re3BOQqy0", "1491069057",
             "2024 presidential results by congressional district, 2024 lines (with 2020)", None),
    "2022": ("1CKngqOp8fzU22JOlypoxNsxL6KSAH920Whc-rd7ebuM", None,
             "2020 presidential results by congressional district, 2022 lines", {"2020": 3}),
    "2020": ("1XbUXnI9OyfAuhP5P3vWtMuGc5UJlrhXbzZo3AwMuHtk", None,
             "Presidential results by congressional district, 2020 lines (2020, 2016, 2012, 2008)", None),
    "2018": ("1zLNAuRqPauss00HDz4XbTH2HqsCzMe0pR8QmD1K8jk8", None,
             "Presidential results by congressional district, 2018 lines (2016, 2012, 2008)", None),
    "2016": ("1VfkHtzBTP5gf4jAu8tcVQgsBJ1IDvXEHjuMqYlOgYbA", None,
             "Presidential results by congressional district, 2016 lines (2016, 2012, 2008)", None),
    "2012": ("1xn6nCNM97oFDZ4M-HQgoUT3X4paOiSDsRMSuxbaOBdg", None,
             "Presidential results by congressional district, 2012-2014 lines (2012, 2008)", None),
    "2006": ("1l7W130tPRF6dQ4JoqlQJSJexnEg4rZct-7kwDXqgoLE", "429358610",
             "Presidential results by congressional district, 2006-2010 lines (2008, 2004, 2000)", None),
}
# House year -> (lines sheet, presidential year known before that election)
LEAN_INPUT = {2024: ("2024", "2020"), 2022: ("2022", "2020"), 2020: ("2020", "2016"), 2018: ("2018", "2016"),
              2016: ("2016", "2012"), 2014: ("2012", "2012"), 2012: ("2012", "2008"), 2010: ("2006", "2008"),
              2008: ("2006", "2004"), 2006: ("2006", "2004")}
# from the methodology's per-state list: states whose 2024 election used their 2022 districts
ON_2022_LINES_IN_2024 = {"CA", "FL", "OH", "TN", "TX", "UT"}
NEW_LINES_IN_2024 = {"AL", "GA", "LA", "NY", "NC"}
DIST = re.compile(r"^([A-Z]{2})-(AL|\d{2})$")


def num(s):
    s = (s or "").strip().replace(",", "").replace("%", "")
    if not s or s in ("-", "—", "N/A", "n/a"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def load(key):
    sid, gid, label, cols = SHEETS[key]
    url = EXPORT.format(id=sid, gid=f"&gid={gid}" if gid else "")
    # Google serves a sheet's CSV export from googleusercontent.com, its own storage host (checked 2026-11-07)
    rec = cc.fetch(url, f"downballot/sheet_{key}.csv", min_bytes=5000, storage_sites=("googleusercontent.com",))
    path = os.path.join(cc.CACHE, rec["path"])
    with open(path, encoding="utf-8") as f:
        head = f.read(200)
    if head.lstrip().startswith("<"):
        raise cc.Refused(f"{url}: an HTML page, not CSV")
    with open(path, encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))
    hdr = next(i for i, r in enumerate(rows) if r and r[0].strip() in ("District", "CD"))
    names = rows[hdr]
    if cols is None:
        def years(r):
            return {c.strip(): j for j, c in enumerate(r) if re.fullmatch(r"(19|20)\d\d", c.strip())}
        cols = years(rows[hdr])
        if cols:      # the years sit in the "District" row and the candidates in the row below it
            names = rows[hdr + 1]
        else:         # the years sit in the row above the "District" row
            cols = years(rows[hdr - 1])
    out = {}
    for r in rows[hdr + 1:]:
        if not r or not DIST.match(r[0].strip()):
            continue
        d = r[0].strip()
        rec_d = {}
        for y, j in cols.items():
            D, R = num(r[j]), num(r[j + 1])
            if D is None or R is None:
                continue
            unit = "votes" if ("," in r[j] or D > 100 or R > 100) else "percent"
            rec_d[y] = {"D": D if unit == "percent" else int(D), "R": R if unit == "percent" else int(R),
                        "two_party_D": D / (D + R), "unit": unit,
                        "candidates": [names[j].strip(), names[j + 1].strip()]}
        out[d] = rec_d
    source = cc.source_block(f"The Downballot, {label}", url, rec["read_utc"], LICENCE, mark="stated",
                             note=f"calculated by The Downballot from official precinct results; methodology "
                                  f"{METHOD_DOC}; sha256 {rec['sha256'][:16]}")
    return source, cols, out


def main():
    sheets, districts, checks = {}, {}, []
    for key in SHEETS:
        src, cols, out = load(key)
        sheets[key] = dict(src, years=sorted(cols))
        districts[key] = out
        n = len(out)
        if n != 435:
            checks.append(f"sheet {key}: {n} districts, not 435")
        bad = [(d, y) for d, v in out.items() for y, x in v.items() if not 0 < x["two_party_D"] < 1]
        if bad:
            checks.append(f"sheet {key}: share outside (0,1) at {bad[:5]}")
    # the same decade's sheets must agree on seats per state
    def seats(key):
        c = {}
        for d in districts[key]:
            c[d[:2]] = c.get(d[:2], 0) + 1
        return c
    for a, b in (("2012", "2016"), ("2016", "2018"), ("2018", "2020"), ("2022", "2024")):
        if seats(a) != seats(b):
            checks.append(f"seats per state differ between the {a} and {b} sheets")
    lean_inputs, missing = {}, {}
    for hy, (key, py) in sorted(LEAN_INPUT.items()):
        li, miss = {}, []
        for d, v in districts[key].items():
            x = v.get(py)
            via = key
            if x is None and hy == 2024 and d[:2] in ON_2022_LINES_IN_2024:
                x = districts["2022"].get(d, {}).get(py)
                via = "2022"
            if x is None:
                miss.append(d)
                continue
            li[d] = {"pres_year": py, "two_party_D": round(x["two_party_D"], 6), "D": x["D"], "R": x["R"],
                     "unit": x["unit"], "sheet": via}
        lean_inputs[str(hy)] = li
        if miss:
            missing[str(hy)] = sorted(miss)
    # where the 2024 sheet and the 2022 sheet both give 2020 on the same (2022) lines, they must agree
    agree = []
    for d, v in districts["2024"].items():
        if d[:2] in NEW_LINES_IN_2024 or "2020" not in v or "2020" not in districts["2022"].get(d, {}):
            continue
        agree.append(abs(v["2020"]["two_party_D"] - districts["2022"][d]["2020"]["two_party_D"]))
    if agree:
        checks.append(f"2020 on 2022 lines, 2024 sheet vs 2022 sheet: {len(agree)} districts, largest "
                      f"difference in two-party share {max(agree):.4f} (the 2022 sheet rounds to 0.1 point)")
    cc.write_json(os.path.join(cc.CACHE, "downballot", "normalized", "pres_by_cd.json"),
                  {"sheets": sheets, "districts": districts, "lean_inputs": lean_inputs, "missing": missing,
                   "checks": checks})
    for hy in sorted(lean_inputs):
        print(f"House {hy}: {len(lean_inputs[hy])} districts with a presidential figure from before the "
              f"election; missing {len(missing.get(hy, []))}")
    for c in checks:
        print("check:", c)


if __name__ == "__main__":
    main()
