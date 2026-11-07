"""pipeline/intake/fec_federal_elections.py: the FEC's "Federal Elections <year>" workbooks.

Source. Federal Election Commission, "Federal Elections <year>: Election Results for the U.S. President,
the U.S. Senate and the U.S. House of Representatives", one workbook per even year, compiled "as
officially reported by individual state or territory election offices" (the FEC's results index). It
gives every general-election candidate for the Senate and the House, with party, an incumbent marker
"(I)", primary, runoff and general-election votes, the Georgia and Louisiana general-election runoffs,
fusion parties' combined totals, and a printed total per district and per state.
Licence: the FEC prints no licence or terms for election results (research/historical-close-races-v2.md
section 5; research/decisiveness-models-v2.md section 3.5); they are federal public records.

Run:  python3 pipeline/intake/fec_federal_elections.py [year ...]     (default: every year below)
Writes CACHE/fec/normalized/<year>.json (a list of contests, candidates aggregated) and prints the
checks. pipeline/intake/build_congress.py turns these into data/senate/ and data/house/.
      python3 pipeline/intake/fec_federal_elections.py president
The presidential results by state, 1996-2024 (D1's, folded in: one FEC intake; section at the end), into
data/president/inputs/fec_president.json, read by pipeline/president.py and pipeline/own_forecast.py.

Checks made, per contest: the candidates' general-election votes sum to the "District Votes" or
"Total State Votes" row the FEC prints (a fusion candidate's party lines are summed first, and must
equal the FEC's "Combined GE party totals" where printed). Any difference is listed, not hidden.
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import congress_common as cc  # noqa: E402

INDEX = "https://www.fec.gov/introduction-campaign-finance/election-results-and-voting-information/"
FILES = {
    2022: "https://www.fec.gov/documents/5676/federalelections2022.xlsx",
    2020: "https://www.fec.gov/documents/4228/federalelections2020.xlsx",
    2018: "https://www.fec.gov/documents/2706/federalelections2018.xlsx",
    2016: "https://www.fec.gov/documents/1890/federalelections2016.xlsx",
    2014: "https://www.fec.gov/documents/1700/federalelections2014.xls",
    2012: "https://www.fec.gov/documents/1682/2012congresults.xls",
    2010: "https://www.fec.gov/documents/1675/federalelections2010.xls",
    2008: "https://www.fec.gov/documents/1659/2008congresults.xls",
    2006: "https://www.fec.gov/documents/1642/federalelections2006.xls",
}
ELECTION_DAY = {2006: "2006-11-07", 2008: "2008-11-04", 2010: "2010-11-02", 2012: "2012-11-06",
                2014: "2014-11-04", 2016: "2016-11-08", 2018: "2018-11-06", 2020: "2020-11-03",
                2022: "2022-11-08", 2024: "2024-11-05"}
LICENCE = "US federal public record; the FEC prints no licence or terms for election results"


def sheets(path):
    """Yield (sheet name, list of rows) for the Senate and House results sheets of one workbook."""
    if path.endswith(".xls"):
        import xlrd
        wb = xlrd.open_workbook(path)
        for sn in wb.sheet_names():
            if "Results" in sn and ("House" in sn or "Senate" in sn):
                sh = wb.sheet_by_name(sn)
                yield sn, [sh.row_values(r) for r in range(sh.nrows)]
    else:
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        for sn in wb.sheetnames:
            if "Results" in sn and ("House" in sn or "Senate" in sn) and "Pres" not in sn:
                yield sn, [list(r) for r in wb[sn].iter_rows(values_only=True)]


def colmap(header):
    """Map the fields we need to column numbers, by the header's own words (they vary by year)."""
    m = {}
    for i, h in enumerate(header):
        u = (h or "").strip().upper()
        if u == "STATE ABBREVIATION":
            m["st"] = i
        elif u in ("D", "DISTRICT"):
            m["dist"] = i
        elif u.startswith("FEC ID"):
            m["fec"] = i
        elif u.startswith("(I)") or u.startswith("INCUMBENT"):
            m["inc"] = i
        elif u in ("CANDIDATE NAME", "LAST NAME, FIRST") or u.startswith("CANDIDATE NAME (LAST,"):
            m["name"] = i
        elif u == "TOTAL VOTES":
            m["label"] = i
        elif u == "PARTY":
            m["party"] = i
        elif u in ("GENERAL", "GENERAL VOTES"):
            m["gen"] = i
        elif u in ("GE RUNOFF", "GE RUNOFF ELECTION VOTES (GA)", "GE RUNOFF ELECTION VOTES (WHEN APPLICABLE)") \
                or (u.startswith("GE RUNOFF ELECTION VOT") or (u.startswith("GE RUNOFF") and "%" not in u)):
            m.setdefault("runoff", i)
        elif u.startswith("COMBINED GE PARTY TOTAL") or u.startswith("COMBINED GE PARTY TOTA"):
            m["combined"] = i
        elif u.startswith("GE WINNER"):
            m["winner"] = i
        elif u.startswith("FOOTNOTE") or u.startswith("NOTES"):
            m["note"] = i
    return m


def norm_district(raw):
    """FEC district cell -> (office, district, special, flag). office 'senate' or 'house'."""
    s = str(raw).strip()
    if isinstance(raw, float):
        s = str(int(raw))
    u = s.upper().replace("  ", " ")
    flag = "*" in u
    # "UNEXPIRED TERM" or "SUN" marks a special election for the rest of a term; in the 2006 workbook a
    # district number with an asterisk ("13*") is the same day's special election for that district.
    special = ("UNEXPIRED" in u) or u == "SUN" or flag
    u2 = u.replace("*", "").strip()
    if u2.startswith("S"):
        return "senate", None, special, flag
    if u2 == "H" or u2.startswith("H "):
        return "house-state-total", None, special, flag   # the state's House total row, not a district
    mnum = re.match(r"^(\d+)(\.0)?", u2)
    if mnum:
        d = int(mnum.group(1))
        return "house", ("AL" if d == 0 else f"{d:02d}"), special, flag
    return None, None, special, flag


def parse_year(year):
    rec = cc.fetch(FILES[year], f"fec/{os.path.basename(FILES[year])}")
    path = os.path.join(cc.CACHE, rec["path"])
    contests = {}
    order = []
    for sn, rows in sheets(path):
        m = None
        for row in rows:
            cells = ["" if c is None else c for c in row]
            texts = [str(c).strip() for c in cells]
            if "STATE ABBREVIATION" in [t.upper() for t in texts]:
                m = colmap(texts)
                continue
            if m is None or "st" not in m:
                continue
            st = texts[m["st"]].upper() if m["st"] < len(texts) else ""
            if st not in cc.STATE_NAMES:
                continue
            office, dist, special, flag = norm_district(cells[m["dist"]]) if "dist" in m else (None,) * 4
            if office is None or office == "house-state-total":
                continue
            key = (office, st, dist, special)
            if key not in contests:
                contests[key] = {"office": office, "state": st, "district": dist, "special": special,
                                 "flag": flag, "rows": [], "printed_total": None, "printed_runoff_total": None,
                                 "notes": set()}
                order.append(key)
            c = contests[key]
            c["flag"] = c["flag"] or flag
            label = texts[m["label"]] if "label" in m and m["label"] < len(texts) else ""
            name = texts[m["name"]] if "name" in m and m["name"] < len(texts) else ""
            note = texts[m["note"]] if "note" in m and m["note"] < len(texts) else ""
            if note:
                c["notes"].add(note)
            if label and not name:
                if label.upper().rstrip(": ") in ("DISTRICT VOTES", "TOTAL STATE VOTES", "TOTAL DISTRICT VOTES"):
                    c["printed_total"] = cc.to_int(cells[m["gen"]]) if "gen" in m else None
                    if "runoff" in m:
                        c["printed_runoff_total"] = cc.to_int(cells[m["runoff"]])
                continue
            if not name or name.upper().startswith("DISTRICT "):
                continue
            gen_raw = cells[m["gen"]] if "gen" in m else None
            party_txt = texts[m["party"]] if "party" in m else ""
            if "COMBINED" in party_txt.upper():
                # a fusion candidate's summary line (e.g. "D/WF/IDP Combined Parties"): its party lines
                # follow and are summed; the summary is kept only as the check
                c.setdefault("combined_lines", []).append((name, cc.to_int(gen_raw)))
                continue
            c["rows"].append({
                "name": re.sub(r"\s+", " ", name).strip().rstrip(","),
                "fec_id": texts[m["fec"]] if "fec" in m else "",
                "party": texts[m["party"]].strip() if "party" in m else "",
                "incumbent": "(I)" in (texts[m["inc"]] if "inc" in m else ""),
                "general": cc.to_int(gen_raw),
                # "n/a" in the November column marks a primary line (New York 2008, Texas 2006), not a November entry
                "general_text": None if cc.to_int(gen_raw) is not None or str(gen_raw).strip().lower() == "n/a"
                else (str(gen_raw).strip() or None),
                "runoff": cc.to_int(cells[m["runoff"]]) if "runoff" in m else None,
                "combined": cc.to_int(cells[m["combined"]]) if "combined" in m else None,
                "winner": (texts[m["winner"]].upper().startswith("W") if "winner" in m else None),
            })
    out = []
    for key in order:
        c = contests[key]
        cands = {}
        id_names, shared = {}, {}
        for r in c["rows"]:
            k = r["fec_id"] if r["fec_id"] and r["fec_id"].lower() not in ("n/a", "") else "name:" + r["name"]
            if r["name"].lower().startswith(("scattered", "write-in", "write in", "writein", "all others")):
                k = "scattered:" + r["name"].lower()
            elif not k.startswith("name:"):
                # The FEC's file sometimes gives two candidates of one contest the same id: 2008 NC-04, Price (D)
                # and Lawson (R) both under H6NC04037, which joined them into one "D/R" line with p = 0 (M2's
                # second pass, 2026-11-07). One id's lines are one candidate's only under one surname; a second
                # surname under the id is a second candidate, its own line, and noted.
                sn = surname(r["name"])
                first = id_names.setdefault(k, (sn, r["name"]))
                if sn != first[0]:
                    shared[k + "|" + sn] = (r["fec_id"], first[1])
                    k = k + "|" + sn
            a = cands.setdefault(k, {"name": r["name"], "fec_id": r["fec_id"], "parties": [], "incumbent": False,
                                     "votes": None, "runoff_votes": None, "combined_printed": None,
                                     "winner_marked": None, "text": None, "scattered": k.startswith("scattered:")})
            # a party counts only from a line that carries the general election (votes, a word such as
            # "Unopposed", or a runoff): the file also prints each candidate's primary lines, and a primary
            # loser who ran in November on another party's line kept the first party too (2012 NY-05, Jennings:
            # lost the Democratic primary, the Republican nominee; 2016 PA-09, Halvorson: lost the Republican
            # primary, the Democratic nominee by write-in), read as "D/R" (M2's second pass, 2026-11-07)
            general_line = r["general"] is not None or r["general_text"] or r["runoff"] is not None
            if r["party"] and general_line and r["party"] not in a["parties"]:
                a["parties"].append(r["party"])
            a["incumbent"] = a["incumbent"] or r["incumbent"]
            if r["general"] is not None:
                a["votes"] = (a["votes"] or 0) + r["general"]
            elif r["general_text"] and not a["text"]:
                a["text"] = r["general_text"]
            if r["runoff"] is not None:
                a["runoff_votes"] = (a["runoff_votes"] or 0) + r["runoff"]
            if r["combined"] is not None:
                a["combined_printed"] = r["combined"]
            if r["winner"]:
                a["winner_marked"] = True
        # A fusion candidate's party lines sometimes carry two FEC ids that differ by a digit (Connecticut 2010,
        # Blumenthal: S0CT00177 on the Democratic line, S0CT00178 on the Working Families line). Lines of one
        # contest with the same printed name are one candidate's; they are summed, and the merge is noted.
        by_name = {}
        for k in list(cands):
            a = cands[k]
            if a["scattered"]:
                continue
            nm = re.sub(r"\s+", " ", a["name"]).strip().rstrip(",").lower()
            if nm in by_name and by_name[nm] != k:
                b = cands[by_name[nm]]
                for p_ in a["parties"]:
                    if p_ not in b["parties"]:
                        b["parties"].append(p_)
                for f in ("votes", "runoff_votes"):
                    if a[f] is not None:
                        b[f] = (b[f] or 0) + a[f]
                b["incumbent"] = b["incumbent"] or a["incumbent"]
                b["winner_marked"] = b["winner_marked"] or a["winner_marked"]
                b["combined_printed"] = b["combined_printed"] if b["combined_printed"] is not None else a["combined_printed"]
                c["notes"].add(f"{a['name']}: lines under FEC ids {b['fec_id']} and {a['fec_id']} are one "
                                  f"candidate's (same name in the contest) and are summed")
                del cands[k]
            else:
                by_name[nm] = k
        cl = [a for a in cands.values() if a["votes"] is not None or a["text"]]
        for k, (fid, other) in shared.items():
            if k in cands and (cands[k]["votes"] is not None or cands[k]["text"]):
                c["notes"].add(f"{cands[k]['name']}: the FEC's file lists this candidate under {other}'s id {fid}; "
                               f"read as a separate candidate (two surnames under one id)")
        if not cl:
            # a district cell with no candidate under it (2018: a "CA" row read as an at-large district;
            # 2006: Ohio's 3rd and 18th marked with an asterisk and no special-election lines): no contest
            print(f"   {c['state']} {c['office']} {c['district'] or ''}{' special' if c['special'] else ''}: "
                  f"no candidate lines; not a contest")
            continue
        checks = []
        for nm, tot in c.get("combined_lines", []):
            for a in cl:
                if a["name"] == re.sub(r"\s+", " ", nm).strip().rstrip(",") and a["combined_printed"] is None:
                    a["combined_printed"] = tot
        for a in cl:
            if a["combined_printed"] is not None and a["votes"] is not None and a["combined_printed"] != a["votes"]:
                checks.append(f"{a['name']}: party lines sum to {a['votes']:,}, FEC combined total {a['combined_printed']:,}")
        s = sum(a["votes"] or 0 for a in cl)
        if c["printed_total"] is not None and c["printed_total"] != s:
            checks.append(f"candidates sum to {s:,}; FEC prints {c['printed_total']:,}")
        out.append({"office": c["office"], "state": c["state"], "district": c["district"],
                    "special": c["special"], "flag": c["flag"], "candidates": cl,
                    "printed_total": c["printed_total"], "printed_runoff_total": c["printed_runoff_total"],
                    "notes": sorted(c["notes"]), "checks": checks})
    return rec, out


def main(years):
    for y in years:
        rec, contests = parse_year(y)
        dst = os.path.join(cc.CACHE, "fec", "normalized", f"{y}.json")
        cc.write_json(dst, {"year": y, "date": ELECTION_DAY[y], "file": rec, "index": INDEX, "contests": contests})
        n_s = sum(1 for c in contests if c["office"] == "senate")
        n_h = sum(1 for c in contests if c["office"] == "house")
        bad = [c for c in contests if c["checks"]]
        with_total = sum(1 for c in contests if c["printed_total"] is not None)
        print(f"{y}: {n_s} Senate and {n_h} House contests; {with_total} with a printed total; "
              f"{len(bad)} with a difference")
        for c in bad[:12]:
            print(f"   {c['state']} {c['office']} {c['district'] or ''}{' special' if c['special'] else ''}: "
                  + "; ".join(c["checks"]))


# ======================================================================================== the presidency
# Folded in from D1's pipeline/intake/fec_president.py (written 2026-11-07 by worker D1, briefs/D1-data-president.md),
# 2026-11-07 by worker D2 on the orchestrator's word of 05:58 UTC (item 7: "one implementation of each thing").
# Its parsers are D1's, unchanged. What it writes: data/president/inputs/fec_president.json, for every year and
# state, the Democratic and Republican nominees' votes (summed over the party lines they ran on), the FEC's
# total votes, and the nominees' names as the FEC prints them. Why both this and MEDSL: plan section 3a says
# where two sources cover a contest both are read, the differences listed, and the certified source wins; the
# FEC's compilation is the federal record of each state's official count, so it is the count of record for
# 1996-2024 and MEDSL the check (pipeline/president.py lists every difference). Checks: 51 jurisdictions each
# year; the 2024 national sums equal the FEC's printed totals (Harris 75,017,613, Trump 77,302,580, all
# 155,238,302; research/decisiveness-models-v2.md section 3.5); each year's sums printed.
PRES_OUT = os.path.join(cc.REPO, "data", "president", "inputs", "fec_president.json")
FEC = "https://www.fec.gov"
PAGE = FEC + "/introduction-campaign-finance/election-results-and-voting-information/federal-elections-{y}/"
PRES_FILES = {
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


def pres_workbook(year):
    rel, sheet = PRES_FILES[year]
    name = f"fec/{rel.split('/')[-1]}"
    path = os.path.join(cc.CACHE, cc.fetch(FEC + rel, name)["path"])
    if path.endswith(".xls"):
        # D1's route, kept: LibreOffice (headless) converts the old binary workbook, in the cache, so that
        # openpyxl reads it with the cell types the parsers below were written for; never committed
        conv = os.path.join(cc.CACHE, "converted")
        out = os.path.join(conv, os.path.basename(path) + "x")
        if not os.path.exists(out):
            os.makedirs(conv, exist_ok=True)
            subprocess.run(["libreoffice", "--headless", "--convert-to", "xlsx", "--outdir", conv, path],
                           check=True, capture_output=True)
        path = out
    import openpyxl
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


def president():
    """The presidential part (D1's fec_president.py, folded in here 2026-11-07: one FEC intake)."""
    out = {}
    sources = {}
    for year in sorted(PRES_FILES):
        name, rows = pres_workbook(year)
        if year in (1996, 2000):
            res = parse_candidate_rows(year, rows)
        elif year == 2024:
            res = parse_2024(rows)
        else:
            res = parse_table2(year, rows)
        assert len(res) == 51 and set(res) == CODES, (year, sorted(CODES - set(res)))
        assert all(v["dem"] > 0 and v["rep"] > 0 for v in res.values()), year
        out[str(year)] = res
        m = cc.fetch(FEC + PRES_FILES[year][0], name)
        sources[str(year)] = dict(cc.source_block(
            f"Federal Election Commission, Federal Elections {year}: presidential general election results"
            f" by state ({PRES_FILES[year][1]})", m["url"], m["read_utc"],
            "public record (no reuse terms printed by the FEC)", "stated",
            via="the FEC's compilation of results as officially reported by state election offices",
            note=f"listed on {PAGE.format(y=year)}"), sha256=m["sha256"])
        d = sum(v["dem"] for v in res.values())
        r = sum(v["rep"] for v in res.values())
        t = sum(v["total"] for v in res.values())
        print(f"{year}: 51 jurisdictions; {NOMINEES[year][0]} {d:,}, {NOMINEES[year][1]} {r:,}, total {t:,}")
        if year == 2024:
            assert (d, r, t) == (75017613, 77302580, 155238302), (d, r, t)
    doc = {"about": "FEC official presidential results by state, normalised by pipeline/intake/fec_federal_elections.py president."
                    " dem and rep are the two nominees' votes summed over their party lines; total is the FEC's.",
           "sources": sources, "years": out}
    os.makedirs(os.path.dirname(PRES_OUT), exist_ok=True)
    with open(PRES_OUT, "w") as f:
        json.dump(doc, f, indent=1)
        f.write("\n")
    print(f"wrote {os.path.relpath(PRES_OUT, cc.REPO)}")


if __name__ == "__main__":
    if sys.argv[1:2] == ["president"]:
        president()
    else:
        main([int(a) for a in sys.argv[1:]] or sorted(FILES))
