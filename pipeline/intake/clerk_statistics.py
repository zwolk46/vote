"""pipeline/intake/clerk_statistics.py: the Clerk of the House's "Statistics of the Presidential and
Congressional Election", one volume per even year.

Source. Office of the Clerk, U.S. House of Representatives, "Statistics of the Presidential and
Congressional Election ... from official sources", showing "the vote cast for each nominee for United
States Senator, Representative, Resident Commissioner, and Delegate" (cover of the 2024 volume, published
March 10, 2025). PDF at https://clerk.house.gov/member_info/electionInfo/<year>/statistics<year>.pdf.
Licence: none printed; a publication of the House (research/historical-close-races-v2.md section 5).

The volume prints no incumbent marker and no district total, so this script is the primary source only
where the FEC has no workbook (2024: the FEC has published only the presidential results). For other
years it is the check on the FEC (plan section 3a: two sources, differences listed).

Run:  python3 pipeline/intake/clerk_statistics.py [year ...]      (default 2024)
Writes CACHE/clerk/normalized/<year>.json. Needs pdftotext (poppler).

How a line is read (the text of `pdftotext -layout`):
  - a state heading is a line holding only a state's name, maybe with "—Continued";
  - "FOR UNITED STATES SENATOR" or "REPRESENTATIVE" (or RESIDENT COMMISSIONER, DELEGATE) opens a section;
    "(For unexpired term ...)" inside a Senate section opens a special election;
  - "12. Name, Party ...... 123,456" opens district 12 with its first candidate; "AT LARGE" opens the
    at-large district; a later "Name, Party ..... 1,234" adds a candidate;
  - in fusion states (New York, Connecticut) a line holding only party names ("Conservative ... 25,483")
    is another party line of the candidate above, and is added to that candidate;
  - "Blank", "Void", "Scattering", "Write-in" lines are kept as non-candidate lines;
  - "Name, Party ... (1)" with the footnote "the names of those with no opposition are not printed on the
    ballot" is an unopposed candidate, with no votes;
  - the "Recapitulation of Votes Cast" table at the end of each state is skipped.
"""
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import congress_common as cc  # noqa: E402

URL = "https://clerk.house.gov/member_info/electionInfo/{y}/statistics{y}.pdf"
LICENCE = "a publication of the U.S. House of Representatives; no licence or terms printed"
NONCAND = re.compile(r"^(blank|void|scattering|scattered|write-in|write in|writein|all others|"
                     r"none of these|over ?votes?|under ?votes?|blank and void|blank/void)\b", re.I)
FUSION_PARTIES = {"conservative", "working families", "common sense", "common sense suffolk", "independence",
                  "independent", "independent party", "libertarian", "green", "griebel party", "democratic",
                  "republican", "democrat", "women's equality", "reform", "serve america movement",
                  "unaffiliated", "petitioning candidate", "democratic party", "republican party"}
STATE_LINE = re.compile(r"^([A-Z][A-Z .]+?)(—CONTINUED)?$")
DOTS = re.compile(r"\s*\.{3,}[\s.]*")


def text_of(year):
    rec = cc.fetch(URL.format(y=year), f"clerk/statistics{year}.pdf", min_bytes=10000)
    pdf = os.path.join(cc.CACHE, rec["path"])
    txt = pdf[:-4] + ".txt"
    if not os.path.exists(txt):
        subprocess.run(["pdftotext", "-layout", pdf, txt], check=True)
    with open(txt, encoding="utf-8", errors="replace") as f:
        return rec, f.read().splitlines()


def parse(year):
    rec, lines = text_of(year)
    state = None
    section = None          # 'senate' | 'house' | None
    special = False
    district = None
    contests = []
    cur = None
    in_recap = False
    footnotes = {}

    def open_contest(office, dist, spec):
        nonlocal cur
        cur = {"office": office, "state": state, "district": dist, "special": spec, "candidates": [],
               "other_lines": [], "notes": []}
        contests.append(cur)

    for raw in lines:
        line = raw.replace("\f", "").strip()
        if not line:
            continue
        compact = re.sub(r"\s+", " ", DOTS.sub(" … ", line)).strip()
        up = compact.upper()
        msta = STATE_LINE.match(up)
        if msta and msta.group(1).strip() in cc.ABBR:
            new_state = cc.ABBR[msta.group(1).strip()]
            if new_state != state or not msta.group(2):
                state, section, cur, district, special, in_recap = new_state, None, None, None, False, False
            else:
                in_recap = False
            continue
        if up.startswith("RECAPITULATION OF VOTES CAST"):
            in_recap, section, cur = True, None, None
            continue
        if state is not None and "no opposition" in compact.lower():
            # e.g. "According to Florida law, the names of those with no opposition are not printed on the
            # ballot." (printed under the recapitulation; the marker "(1)" sits on its own line above it)
            footnotes[(state, "1")] = compact
            continue
        if in_recap or state is None:
            continue
        if up.startswith("FOR PRESIDENTIAL ELECTORS"):
            section, cur = None, None
            continue
        if up.startswith("FOR UNITED STATES SENATOR"):
            if "CONTINUED" not in up:
                section, special, cur = "senate", False, None
                open_contest("senate", None, False)
            continue
        if up.startswith(("FOR UNITED STATES REPRESENTATIVE", "FOR RESIDENT COMMISSIONER", "FOR DELEGATE")):
            if "CONTINUED" not in up:
                section, cur = "house", None
            continue
        if section == "senate" and up.startswith("(FOR UNEXPIRED TERM"):
            if cur is not None and not cur["candidates"]:
                contests.remove(cur)
            open_contest("senate", None, True)
            continue
        if section == "senate" and up.startswith("(FOR FULL TERM"):
            if cur is not None and not cur["candidates"]:
                contests.remove(cur)
            open_contest("senate", None, False)
            continue
        if section == "house" and up in ("AT LARGE", "AT-LARGE"):
            open_contest("house", "AL", False)
            continue
        mfoot = re.match(r"^\((\d)\)\s+(According to .*|.*no opposition.*)$", compact)
        if mfoot:
            footnotes[(state, mfoot.group(1))] = mfoot.group(2)
            continue
        if section is None:
            continue
        m = re.match(r"^(?:(\d{1,2})\.\s+)?(.+?)\s+…\s+([\d,]+|\(\d\))$", compact)
        if not m:
            continue
        dnum, label, val = m.group(1), m.group(2).strip(), m.group(3)
        if section == "house" and dnum:
            open_contest("house", f"{int(dnum):02d}", False)
        if cur is None:
            continue
        votes = None if val.startswith("(") else int(val.replace(",", ""))
        if NONCAND.match(label):
            cur["other_lines"].append({"label": label, "votes": votes})
            continue
        parts = [p.strip() for p in label.split(",")]
        if all(p.lower().rstrip(".") in FUSION_PARTIES for p in parts) and cur["candidates"]:
            cur["candidates"][-1]["votes"] = (cur["candidates"][-1]["votes"] or 0) + (votes or 0)
            cur["candidates"][-1]["parties"].append(label)
            continue
        # "Rock Aboujaoude, Jr., Democrat": the party follows the last comma
        name, party = (label.rsplit(",", 1) + [""])[:2] if "," in label else (label, "")
        name, party = name.strip(), party.strip()
        cur["candidates"].append({"name": name, "parties": [party] if party else [], "votes": votes,
                                  "unopposed_marker": val if votes is None else None})
    out = []
    for c in contests:
        if not c["candidates"]:
            continue
        for a in c["candidates"]:
            if a["unopposed_marker"]:
                note = footnotes.get((c["state"], a["unopposed_marker"].strip("()")))
                a["text"] = "Unopposed" if note and "no opposition" in note else note
                c["notes"].append(note or f"footnote {a['unopposed_marker']} unread")
        out.append(c)
    return rec, out


def main(years):
    for y in years:
        rec, contests = parse(y)
        cc.write_json(os.path.join(cc.CACHE, "clerk", "normalized", f"{y}.json"),
                      {"year": y, "file": rec, "contests": contests})
        n_s = sum(c["office"] == "senate" for c in contests)
        n_h = sum(c["office"] == "house" for c in contests)
        print(f"{y}: {n_s} Senate and {n_h} House contests (delegates included) from the Clerk's volume")


if __name__ == "__main__":
    main([int(a) for a in sys.argv[1:]] or [2024])
