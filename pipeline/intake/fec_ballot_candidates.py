"""pipeline/intake/fec_ballot_candidates.py: the FEC's list of general-election ballot candidates for
Congress, used here for who was the incumbent in a year the FEC has not yet published results for.

Source. Federal Election Commission, "2024 General Election Ballot Candidates for U.S. Senate and House"
(https://www.fec.gov/documents/5548/2024congressgecands.xlsx), one sheet per state, columns
STATE ABBREVIATION, STATE, DISTRICT, FEC ID#, (I), CANDIDATE NAME, PARTY. Licence: none printed; a
federal public record.

What "(I)" means here. In this file "(I)" marks a sitting Member of Congress, not the holder of the seat
on the ballot: Ruben Gallego (a House member) is marked "(I)" on the 2024 Arizona Senate line, and Lisa
Blunt Rochester on Delaware's. The FEC's results workbooks (2006-2022) mark the seat's incumbent instead
(Val Demings, a House member running for the Senate in 2022, is unmarked there). So a Senate line's
"(I)" is read as the seat's incumbent only when the candidate did not win a House seat at the previous
election (the Clerk's or the FEC's results for that year), and the reading is checked against the
previous election for the seat; both checks are made where the contests are built (pipeline/intake/build_congress.py).

Run:  python3 pipeline/intake/fec_ballot_candidates.py [year ...]   (default 2024)
Writes CACHE/fec/ballot/normalized/<year>.json: {"file": ..., "contests": [{"office", "state", "district",
"special", "candidates": [{"name", "fec_id", "party", "member_marked"}]}]}.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import congress_common as cc  # noqa: E402

FILES = {2024: "https://www.fec.gov/documents/5548/2024congressgecands.xlsx"}
LICENCE = "US federal public record; the FEC prints no licence or terms"


def parse(year):
    import openpyxl
    rec = cc.fetch(FILES[year], f"fec/ballot/{year}congressgecands.xlsx", min_bytes=10000)
    wb = openpyxl.load_workbook(os.path.join(cc.CACHE, rec["path"]), read_only=True)
    contests = {}
    rows = 0
    for ws in wb.worksheets:
        head = None
        for r in ws.iter_rows(values_only=True):
            if head is None:
                head = [str(x).strip() if x is not None else "" for x in r]
                continue
            st = (r[0] or "").strip() if isinstance(r[0], str) else r[0]
            if not st or st not in cc.STATE_NAMES or not r[7]:
                continue
            rows += 1
            dist = str(r[2] or "").strip()
            special = "UNEXPIRED" in dist.upper()
            base = dist.split("-")[0].strip()
            if base.upper() == "S":
                office, d = "senate", None
            else:
                office, d = "house", ("AL" if base in ("00", "0") else f"{int(base):02d}")
            k = (office, st, d, special)
            c = contests.setdefault(k, {"office": office, "state": st, "district": d, "special": special,
                                        "candidates": []})
            c["candidates"].append({"name": " ".join(str(r[7]).split()), "fec_id": (r[3] or "").strip() or None,
                                    "party": " ".join(str(r[8] or "").split()),
                                    "member_marked": bool(r[4] and "I" in str(r[4]))})
    out = sorted(contests.values(), key=lambda c: (c["office"], c["state"], c["district"] or "", c["special"]))
    cc.write_json(os.path.join(cc.CACHE, "fec", "ballot", "normalized", f"{year}.json"),
                  {"year": year, "file": rec, "licence": LICENCE, "rows": rows, "contests": out})
    n_s = sum(c["office"] == "senate" for c in out)
    n_h = sum(c["office"] == "house" for c in out)
    print(f"{year}: {rows} candidate rows; {n_s} Senate and {n_h} House contests (delegates included)")
    return rec, out


if __name__ == "__main__":
    for y in [int(a) for a in sys.argv[1:]] or [2024]:
        parse(y)
