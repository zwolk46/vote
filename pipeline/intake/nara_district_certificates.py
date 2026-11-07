"""Intake: Maine's and Nebraska's presidential votes by congressional district, 2012-2024, from the states'
Certificates of Ascertainment as published by the National Archives.

Written 2026-11-07 by worker D1 (briefs/D1-data-president.md: "per district where EVs split").

Why: Maine and Nebraska give one elector to the winner of each congressional district and two to the
statewide winner, so each district is a contest of its own for one electoral vote. No standardized dataset
reached here has the presidential vote by district (MEDSL's state file and the FEC have state totals only);
the certificate each governor sends to the Archivist does.

Source: https://www.archives.gov/files/electoral-college/<year>/[<year>-]ascertainment-<state>.pdf, linked
from https://www.archives.gov/electoral-college/<year> (NARA; the certificates are the states' official
acts, public records). The PDFs from 2012 to 2020 are scans with a text layer recognised by machine, which
drops or garbles some figures; 2024's are clean. Text is read with pdftotext (poppler), never by eye.

What it writes: data/president/inputs/nara_district_certificates.json: for each year and state, the
Democratic and Republican tickets' votes in each district and statewide (at large), where the text layer
gives every one of them legibly. A state-year is kept only if all its figures parse as whole numbers with
thousands separators and pass the checks; otherwise it is listed under "unread" with the reason.

Checks: Nebraska's districts sum to its statewide total for each ticket (its certificate prints both);
Maine's districts sum to no more than its at-large total (Maine's certificate says some votes are "included
in the At-Large totals, but not in the separate totals by Congressional District"); the statewide figures
equal the FEC's (data/president/inputs/fec_president.json).

Run from the repository root:  python3 pipeline/intake/nara_district_certificates.py
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import fetch  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "data", "president", "inputs", "nara_district_certificates.json")
FEC = os.path.join(ROOT, "data", "president", "inputs", "fec_president.json")
YEARS = (2012, 2016, 2020, 2024)
NOMINEES = {2012: ("Obama", "Romney"), 2016: ("Clinton", "Trump"), 2020: ("Biden", "Trump"),
            2024: ("Harris", "Trump")}
ORD = {"First": 1, "Second": 2, "Third": 3}
NUM = r"(\d{1,3}(?:,\d{3})+|\d{1,3})"


def url(year, state):
    pre = "2012-" if year == 2012 else ""
    return f"https://www.archives.gov/files/electoral-college/{year}/{pre}ascertainment-{state}.pdf"


def text(year, state):
    path = fetch.fetch(url(year, state), f"nara_ascertainment_{year}_{state}.pdf")
    out = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True, check=True)
    return out.stdout


def sections(t, names):
    """Split the text at each ticket's heading; return {party: section text} for the two nominees."""
    found = {}
    for party, name in zip(("dem", "rep"), names):
        m = [x.start() for x in re.finditer(name, t)]
        if not m:
            raise ValueError(f"no heading names {name}")
        found[party] = m[0]
    starts = sorted(found.values())
    # a section runs to the next ticket's heading: any line naming a party's electors or "President"
    heads = [x.start() for x in re.finditer(r"(?im)^.*(party|petition|electors supporting).*$", t)]
    out = {}
    for party, s in found.items():
        nxt = [h for h in heads if h > s + 10]
        out[party] = t[s:(nxt[0] if nxt else len(t))]
    return out


def as_int(s):
    return int(s.replace(",", ""))


def parse_ne(sec):
    st = re.search(r"Statewide Total Votes Received:\s*" + NUM + r"\s*$", sec, re.M)
    d = {k: re.search(rf"{k} Congressional District Total Votes Received:\s*" + NUM + r"\s*$", sec, re.M)
         for k in ORD}
    if not st or not all(d.values()):
        raise ValueError("a figure is missing or garbled in the text layer")
    return as_int(st.group(1)), {ORD[k]: as_int(m.group(1)) for k, m in d.items()}


def parse_me(sec):
    def after(label):
        m = re.search(label + r"[^\n]*\n[^\n]*?\s{3,}" + NUM + r"\s*$", sec, re.M)
        return as_int(m.group(1)) if m else None
    d = {1: after(r"First Congressional District"), 2: after(r"Second Congressional District")}
    al = after(r"At-Large")
    if None in d.values():
        raise ValueError("a district figure is missing or garbled in the text layer")
    return al, d          # al None: the at-large figure is illegible; the FEC's statewide total stands in


def main():
    fec = json.load(open(FEC))["years"]
    doc = {"about": "Maine's and Nebraska's presidential votes by congressional district, from the states' "
                    "Certificates of Ascertainment (NARA), by pipeline/intake/nara_district_certificates.py.",
           "years": {}, "unread": {}, "sources": {}}
    for y in YEARS:
        for state, code, parse in (("maine", "ME", parse_me), ("nebraska", "NE", parse_ne)):
            key = f"{y} {code}"
            try:
                secs = sections(text(y, state), NOMINEES[y])
                res = {party: parse(sec) for party, sec in secs.items()}
                filled = []
                for party, (statewide, dists) in list(res.items()):
                    want = fec[str(y)][code][party]
                    if statewide is None:
                        res[party] = (want, dists)
                        statewide = want
                        filled.append(party)
                    if statewide != want:
                        raise ValueError(f"{party} statewide {statewide:,} differs from the FEC's {want:,}")
                    if code == "NE" and sum(dists.values()) != statewide:
                        raise ValueError(f"{party} districts sum to {sum(dists.values()):,}, not {statewide:,}")
                    if code == "ME" and sum(dists.values()) > statewide:
                        raise ValueError(f"{party} districts sum above the at-large total")
            except (ValueError, KeyError) as e:
                doc["unread"][key] = str(e)
                print(f"{key}: unread ({e})")
                continue
            doc["years"].setdefault(str(y), {})[code] = {
                "statewide": {p: r[0] for p, r in res.items()},
                "districts": {f"{code}-{k}": {"dem": res["dem"][1][k], "rep": res["rep"][1][k]}
                              for k in sorted(res["dem"][1])}}
            m = fetch.meta(f"nara_ascertainment_{y}_{state}.pdf")
            doc["sources"][key] = fetch.source(
                f"State of {state.title()}, Certificate of Ascertainment of Electors, {y} (National Archives)",
                m["url"], m["read_utc"], "public record", "stated",
                note="read from the PDF's text layer with pdftotext; checked against the FEC's statewide totals"
                     + (f"; the at-large figure for {', '.join(filled)} is illegible there and the FEC's "
                        "statewide total is used" if filled else ""),
                sha256=m["sha256"])
            print(f"{key}: " + ", ".join(f"{u} D {v['dem']:,} R {v['rep']:,}"
                                         for u, v in doc["years"][str(y)][code]["districts"].items()))
    with open(OUT, "w") as f:
        json.dump(doc, f, indent=1)
        f.write("\n")
    print(f"wrote {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
