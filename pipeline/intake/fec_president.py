"""Intake: Federal Election Commission, official presidential general-election results by state, 1996-2024.

Written 2026-11-07 by worker D1 (briefs/D1-data-president.md; plan/PLAN.md section 3a).

Source: the FEC's "Federal Elections" compilations, "election results from past federal elections, as
officially reported by individual state or territory election offices" (fec.gov, stated). One workbook
per year, linked from each year's page under fec.gov/introduction-campaign-finance/election-results-and-
voting-information/. No reuse terms are printed (research/decisiveness-models-v2.md section 3.5); the
figures are official vote counts, a public record. The old binary .xls files are converted to .xlsx with
LibreOffice (headless) in the cache; the converted copy is never committed.

Why both this and MEDSL: plan section 3a says where two sources cover a contest both are read, the
differences listed, and the certified source wins. The FEC's compilation is the federal government's
record of each state's official count, so it is taken as the count of record for 1996-2024, and MEDSL
(pipeline/intake/medsl_dataverse.py president_detail) as the check; pipeline/president.py lists every difference.

What it writes: data/president/inputs/fec_president.json, for every year and state, the Democratic and
Republican nominees' votes (summed over the party lines they ran on), the FEC's total votes, and the
nominees' names as the FEC prints them.

Checks: 51 jurisdictions each year; the 2024 national sums equal the FEC's printed totals (Harris
75,017,613, Trump 77,302,580, all 155,238,302; research/decisiveness-models-v2.md section 3.5); each
year's sums printed.

Run from the repository root:  python3 pipeline/intake/fec_president.py
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import fetch  # noqa: E402

import openpyxl  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "data", "president", "inputs", "fec_president.json")
FEC = "https://www.fec.gov"
PAGE = FEC + "/introduction-campaign-finance/election-results-and-voting-information/federal-elections-{y}/"
FILES = {
    1996: ("/documents/1721/FederalElections96_PresidentialGeneralElectionResults.xlsx", "Table 1"),
    2000: ("/documents/1612/2000presge.xls", "Master By State"),
    2004: ("/documents/1631/2004tables.xls", "Table 2. Pres Elec & Pop Vote"),
    2008: ("/documents/1670/tables2008.xls", "Table 2. Electoral &  Pop Vote"),
    2012: ("/documents/1695/tables2012.xls", "Table 2. Electoral &  Pop Vote"),
    2016: ("/documents/1890/federalelections2016.xlsx", "Table 2. Electoral &  Pop Vote"),
    2020: ("/documents/4228/federalelections2020.xlsx", "3. Table 2 Electoral & Pop Vote"),
    2024: ("/documents/5645/2024presgeresults.xlsx", "OFFICIAL 2024 PRES GE RESULTS"),
}
NOMINEES = {1996: ("Clinton", "Dole"), 2000: ("Gore", "Bush"), 2004: ("Kerry", "Bush"), 2008: ("Obama", "McCain"),
            2012: ("Obama", "Romney"), 2016: ("Clinton", "Trump"), 2020: ("Biden", "Trump"), 2024: ("Harris", "Trump")}
STATES = {"ALABAMA": "AL", "ALASKA": "AK", "ARIZONA": "AZ", "ARKANSAS": "AR", "CALIFORNIA": "CA", "COLORADO": "CO",
          "CONNECTICUT": "CT", "DELAWARE": "DE", "DISTRICT OF COLUMBIA": "DC", "D.C.": "DC", "FLORIDA": "FL",
          "GEORGIA": "GA", "HAWAII": "HI", "IDAHO": "ID", "ILLINOIS": "IL", "INDIANA": "IN", "IOWA": "IA",
          "KANSAS": "KS", "KENTUCKY": "KY", "LOUISIANA": "LA", "MAINE": "ME", "MARYLAND": "MD",
          "MASSACHUSETTS": "MA", "MICHIGAN": "MI", "MINNESOTA": "MN", "MISSISSIPPI": "MS", "MISSOURI": "MO",
          "MONTANA": "MT", "NEBRASKA": "NE", "NEVADA": "NV", "NEW HAMPSHIRE": "NH", "NEW JERSEY": "NJ",
          "NEW MEXICO": "NM", "NEW YORK": "NY", "NORTH CAROLINA": "NC", "NORTH DAKOTA": "ND", "OHIO": "OH",
          "OKLAHOMA": "OK", "OREGON": "OR", "PENNSYLVANIA": "PA", "RHODE ISLAND": "RI", "SOUTH CAROLINA": "SC",
          "SOUTH DAKOTA": "SD", "TENNESSEE": "TN", "TEXAS": "TX", "UTAH": "UT", "VERMONT": "VT", "VIRGINIA": "VA",
          "WASHINGTON": "WA", "WEST VIRGINIA": "WV", "WISCONSIN": "WI", "WYOMING": "WY"}
CODES = set(STATES.values())


def workbook(year):
    rel, sheet = FILES[year]
    name = f"fec_{year}_{rel.split('/')[-1]}"
    path = fetch.fetch(FEC + rel, name)
    if path.endswith(".xls"):
        conv = os.path.join(fetch.CACHE, "converted")
        out = os.path.join(conv, os.path.basename(path) + "x")
        if not os.path.exists(out):
            os.makedirs(conv, exist_ok=True)
            subprocess.run(["libreoffice", "--headless", "--convert-to", "xlsx", "--outdir", conv, path],
                           check=True, capture_output=True)
        path = out
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    return name, list(wb[sheet].iter_rows(values_only=True))


def surname(s):
    return str(s).split(",")[0].strip().lower()


def parse_candidate_rows(year, rows):
    """1996 and 2000: one row per candidate and party line, grouped by state."""
    dname, rname = (n.lower() for n in NOMINEES[year])
    res = {}
    st = None
    for r in rows:
        cells = [c for c in r if c is not None and c != ""]
        if not cells:
            continue
        if year == 2000:
            code, cand, party, votes = r[0], r[1], r[2], r[3]
            if code not in CODES:
                continue
            st = code
            if party is None:
                continue
            d = res.setdefault(st, {"dem": 0, "rep": 0, "total": 0, "dem_name": None, "rep_name": None})
            d["total"] += int(votes)
        else:
            first = str(cells[0]).strip()
            joined = " ".join(str(c).strip() for c in cells).upper().rstrip("*")   # "NEW YORK*"
            if all(isinstance(c, str) for c in cells) and joined in STATES:   # "NORTH", "DAKOTA" in two cells
                st = STATES[joined]
                continue
            if st is None:
                continue
            nums = [c for c in cells[1:] if isinstance(c, (int, float))]
            if first.startswith("Total"):
                if not nums:                         # "Total Votes:   1,392,614" in one cell
                    nums = [int(re.sub(r"[^0-9]", "", first))]
                res[st]["total_printed"] = int(nums[0])
                continue
            if "Combined" in first:                  # New York: "Clinton, Bill  Combined" "Parties:" 3756177
                first = first.split("Combined")[0].strip()
            elif any(isinstance(c, str) and c.startswith("[") for c in cells[1:]):
                continue                             # a "[3,649,630]" party-line part of a combined row
            one = re.match(r"^(.*?,.*?)\s{2,}(\S+)\s+([\d,]+)\s+[\d.]+$", first)
            if one and not nums:                     # "Dole, Bob     R     1,138,350   47.10" in one cell
                first, nums = one.group(1).strip(), [int(one.group(3).replace(",", ""))]
            if not nums:
                continue
            cand = first
            votes = nums[0]
            d = res.setdefault(st, {"dem": 0, "rep": 0, "total": 0, "dem_name": None, "rep_name": None})
            d["total"] += int(votes)
        if surname(cand) == dname:
            d["dem"] += int(votes)
            d["dem_name"] = str(cand)
        elif surname(cand) == rname:
            d["rep"] += int(votes)
            d["rep_name"] = str(cand)
    for st, d in res.items():
        if "total_printed" in d:
            if d["total_printed"] != d["total"]:      # the FEC's own rows and its printed total differ
                d["rows_sum"] = d["total"]
                print(f"  {year} {st}: the FEC prints total {d['total_printed']:,}; its candidate rows sum"
                      f" to {d['total']:,}. The printed total is kept.")
            d["total"] = d.pop("total_printed")
    return res


def parse_table2(year, rows):
    """2004-2020: Table 2, one row per state; the column order differs by year, so it is read from the header."""
    dname, rname = NOMINEES[year]
    hdr_i = next(i for i, r in enumerate(rows) if r[0] == "STATE")
    h = [str(c or "") for c in rows[hdr_i]]
    if not any(dname in c for c in h):          # two header rows (2008 on): names are on the next row
        h = [f"{a} {b or ''}".strip() for a, b in zip(h, rows[hdr_i + 1])]
    pop = [i for i, c in enumerate(h) if "Popular" in c or "POPULAR" in c] or list(range(len(h)))
    # the popular-vote columns: the last ones whose header names each nominee
    di = max(i for i, c in enumerate(h) if dname in c)
    ri = max(i for i, c in enumerate(h) if rname in c or rname.replace("Trump", "Trunp") in c)
    ti = max(i for i, c in enumerate(h) if "Total" in c or "TOTAL" in c)
    assert min(di, ri, ti) >= min(pop), (year, h)
    res = {}
    for r in rows[hdr_i + 1:]:
        code = str(r[0] or "").rstrip("*")           # 2020 prints "ME*" and "NE*" (split electoral votes)
        if code in CODES:
            res[code] = {"dem": int(r[di]), "rep": int(r[ri]), "total": int(r[ti]),
                         "dem_name": dname, "rep_name": rname}
    return res


def parse_2024(rows):
    h = [str(c or "") for c in rows[0]]
    di, ri, ti = h.index("HARRIS"), h.index("TRUMP"), h.index("TOTAL VOTES")
    res = {}
    for r in rows[1:]:
        if r[0] in CODES:
            res[r[0]] = {"dem": int(r[di] or 0), "rep": int(r[ri] or 0), "total": int(r[ti]),
                         "dem_name": "Harris", "rep_name": "Trump"}
    return res


def main():
    out = {}
    sources = {}
    for year in sorted(FILES):
        name, rows = workbook(year)
        if year in (1996, 2000):
            res = parse_candidate_rows(year, rows)
        elif year == 2024:
            res = parse_2024(rows)
        else:
            res = parse_table2(year, rows)
        assert len(res) == 51 and set(res) == CODES, (year, sorted(CODES - set(res)))
        assert all(v["dem"] > 0 and v["rep"] > 0 for v in res.values()), year
        out[str(year)] = res
        m = fetch.meta(name)
        sources[str(year)] = fetch.source(
            f"Federal Election Commission, Federal Elections {year}: presidential general election results"
            f" by state ({FILES[year][1]})", m["url"], m["read_utc"],
            "public record (no reuse terms printed by the FEC)", "stated",
            via="the FEC's compilation of results as officially reported by state election offices",
            note=f"listed on {PAGE.format(y=year)}", sha256=m["sha256"])
        d = sum(v["dem"] for v in res.values())
        r = sum(v["rep"] for v in res.values())
        t = sum(v["total"] for v in res.values())
        print(f"{year}: 51 jurisdictions; {NOMINEES[year][0]} {d:,}, {NOMINEES[year][1]} {r:,}, total {t:,}")
        if year == 2024:
            assert (d, r, t) == (75017613, 77302580, 155238302), (d, r, t)
    doc = {"about": "FEC official presidential results by state, normalised by pipeline/intake/fec_president.py."
                    " dem and rep are the two nominees' votes summed over their party lines; total is the FEC's.",
           "sources": sources, "years": out}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(doc, f, indent=1)
        f.write("\n")
    print(f"wrote {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
