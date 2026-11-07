"""pipeline/intake/nara_electoral_college.py: who won each presidential election, from the National
Archives' Electoral College results pages.

Source. National Archives and Records Administration, Office of the Federal Register, "Electoral College
Results", one page per election (https://www.archives.gov/electoral-college/<year>), each printing the
President and Vice President elected, their party, and the electoral votes. A federal public record; no
licence printed.

Why. The model's own forecast for Senate, House and governor races uses one fact about each year known
before the election: which party held the presidency (the president's party tends to lose ground at a
midterm). Control of the Senate at 50-50 turns on the Vice President's vote, so the Vice President in
office when the new Senate meets is needed too: after a presidential election, the one just elected;
after a midterm, the one in office.

Run:  python3 pipeline/intake/nara_electoral_college.py [first_year last_year]   (default 1976 2024)
Writes CACHE/nara/normalized/electoral_college.json: [{"year", "president", "party", "vice_president",
"electoral_votes", "opponent", "opponent_party", "source"}].
Checks: the winner's electoral votes reach the printed majority.
"""
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import congress_common as cc  # noqa: E402

URL = "https://www.archives.gov/electoral-college/{y}"
LICENCE = "US federal public record (National Archives); no licence printed"


def text(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        t = f.read()
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S)
    t = html.unescape(re.sub(r"<[^>]+>", "\n", t))
    return [x.strip() for x in t.splitlines() if x.strip()]


def parse(year):
    rec = cc.fetch(URL.format(y=year), f"nara/electoral_college_{year}.html", min_bytes=5000)
    L = text(os.path.join(cc.CACHE, rec["path"]))
    i = L.index(f"{year} Electoral College Results")
    block = L[i:i + 40]

    def after(label):
        j = block.index(label)
        return block[j + 1]
    pres = after("President")
    opp = after("Main Opponent")
    m, mo = re.match(r"(.+?)\s*\[(\w+)\]", pres), re.match(r"(.+?)\s*\[(\w+)\]", opp)
    win_ev = int(re.search(r"Winner:\s*(\d+)", " ".join(block)).group(1))
    total, majority = map(int, re.search(r"Total/Majority:\s*(\d+)/(\d+)", " ".join(block)).groups())
    # "Richard B. Cheney (286)" in older pages, "Kamala D. Harris [D]" in 2020 and 2024
    vp = re.match(r"(.+?)\s*[\(\[]", after("Vice President") + " (")
    out = {"year": year, "president": m.group(1), "party": m.group(2), "electoral_votes": win_ev,
           "total": total, "majority": majority, "opponent": mo.group(1), "opponent_party": mo.group(2),
           "vice_president": vp.group(1) if vp else None,
           "source": cc.source_block(f"National Archives, {year} Electoral College Results", rec["url"],
                                     rec["read_utc"], LICENCE, mark="stated")}
    if win_ev < majority:
        out["check"] = f"winner's {win_ev} electoral votes are under the majority {majority}"
    return out


def main(first, last):
    rows = [parse(y) for y in range(first, last + 1, 4)]
    cc.write_json(os.path.join(cc.CACHE, "nara", "normalized", "electoral_college.json"), rows)
    for r in rows:
        print(f"{r['year']}: {r['president']} [{r['party']}] {r['electoral_votes']}/{r['total']}, "
              f"VP {r['vice_president']}{'; ' + r['check'] if r.get('check') else ''}")


if __name__ == "__main__":
    a = [int(x) for x in sys.argv[1:3]]
    main(*(a if len(a) == 2 else (1976, 2024)))
