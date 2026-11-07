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
checks. pipeline/intake/congress_build.py turns these into data/senate/ and data/house/.

Checks made, per contest: the candidates' general-election votes sum to the "District Votes" or
"Total State Votes" row the FEC prints (a fusion candidate's party lines are summed first, and must
equal the FEC's "Combined GE party totals" where printed). Any difference is listed, not hidden.
"""
import json
import os
import re
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
                "general_text": None if cc.to_int(gen_raw) is not None else (str(gen_raw).strip() or None),
                "runoff": cc.to_int(cells[m["runoff"]]) if "runoff" in m else None,
                "combined": cc.to_int(cells[m["combined"]]) if "combined" in m else None,
                "winner": (texts[m["winner"]].upper().startswith("W") if "winner" in m else None),
            })
    out = []
    for key in order:
        c = contests[key]
        cands = {}
        for r in c["rows"]:
            k = r["fec_id"] if r["fec_id"] and r["fec_id"].lower() not in ("n/a", "") else "name:" + r["name"]
            if r["name"].lower().startswith(("scattered", "write-in", "write in", "writein", "all others")):
                k = "scattered:" + r["name"].lower()
            a = cands.setdefault(k, {"name": r["name"], "fec_id": r["fec_id"], "parties": [], "incumbent": False,
                                     "votes": None, "runoff_votes": None, "combined_printed": None,
                                     "winner_marked": None, "text": None, "scattered": k.startswith("scattered:")})
            if r["party"] and r["party"] not in a["parties"]:
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


if __name__ == "__main__":
    ys = [int(a) for a in sys.argv[1:]] or sorted(FILES)
    main(ys)
