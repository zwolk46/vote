"""pipeline/intake/party_divisions.py: seats by party at the start of each Congress, for the Senate and the
House, as the two chambers' own historians print them. Used only as a check on control of the chamber:
the seats not up plus the seats won must give the division the new Congress opened with.

Sources.
  Senate: U.S. Senate, "Party Division", https://www.senate.gov/about/parties-leadership/party-division.htm
          (one block per Congress: the opening division, the changes within it, and numbered footnotes).
  House:  History, Art & Archives, U.S. House of Representatives, "Party Divisions of the House of
          Representatives, 1789 to Present", https://history.house.gov/Institution/Party-Divisions/Party-Divisions/
          (one row per Congress: seats, Democrats, Republicans, other, and footnotes).
Both are publications of the chambers; no licence printed.

Run:  python3 pipeline/intake/party_divisions.py
Writes CACHE/divisions/normalized/divisions.json:
  {"senate": {"110": {"D", "R", "other", "vacant", "years", "footnotes"}}, "house": {"110": {"seats", "D",
   "R", "other", "footnote"}}, "sources": {...}}
"""
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import congress_common as cc  # noqa: E402

SENATE_URL = "https://www.senate.gov/about/parties-leadership/party-division.htm"
HOUSE_URL = "https://history.house.gov/Institution/Party-Divisions/Party-Divisions/"
LICENCE = "a publication of the U.S. {}; no licence printed"


def text_of(path):
    with open(os.path.join(cc.CACHE, path), errors="ignore") as f:
        s = f.read()
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", s, flags=re.S | re.I)
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " | ", s)))


def senate():
    rec = cc.fetch(SENATE_URL, "divisions/senate_party_division.html", min_bytes=100000)
    t = text_of(rec["path"])
    t = re.sub(r"(\| )+", "| ", t)
    flat = re.sub(r"\s*\|\s*", " ", t)
    out = {}
    heads = list(re.finditer(r"(\d{2,3})(?:st|nd|rd|th) Congress \((\d+)/(\d+)/(\d{4}) to (\d+)/(\d+)/(\d{4})\)", flat))
    for i, h in enumerate(heads):
        n = int(h.group(1))
        if n < 100:
            continue
        body = flat[h.end(): heads[i + 1].start() if i + 1 < len(heads) else len(flat)].strip()
        m = re.match(r"\s*(\d+) (Democrats|Republicans) (\d+) (Democrats|Republicans) (\d+) (\d+) (\d+)", body)
        if not m:
            continue
        a, pa, b, pb, other, vacant, total = m.groups()
        d = {"D": int(a) if pa == "Democrats" else int(b), "R": int(b) if pb == "Republicans" else int(a),
             "other": int(other), "vacant": int(vacant), "total": int(total),
             "from": f"{h.group(4)}-{int(h.group(2)):02d}-{int(h.group(3)):02d}"}
        notes = re.findall(r" (\d)\. ([A-Z][^|]*?\.)(?= \d\. | \d{2,3}(?:st|nd|rd|th) Congress|$)", body)
        d["footnotes"] = [f"{k}. {v.strip()}" for k, v in notes]
        out[str(n)] = d
    src = cc.source_block("U.S. Senate, Party Division", rec["url"], rec["read_utc"], LICENCE.format("Senate"),
                          mark="stated", note=f"sha256 {rec['sha256'][:16]}")
    return out, src


def house():
    rec = cc.fetch(HOUSE_URL, "divisions/house_party_divisions.html", min_bytes=50000)
    t = text_of(rec["path"])
    t = re.sub(r"(\| )+", "| ", t)
    out = {}
    for m in re.finditer(r"\| (\d{2,3})(?:st|nd|rd|th) \((\d{4})[–-](\d{4})\) \| (\d+) \|(?: (\d) \|)? (\d+) \| (\d+) \| ([^|]*?) \|", t):
        n = int(m.group(1))
        if n < 100:
            continue
        other = m.group(8).strip()
        out[str(n)] = {"seats": int(m.group(4)), "D": int(m.group(6)), "R": int(m.group(7)),
                       "other": other, "footnote": int(m.group(5)) if m.group(5) else None,
                       "years": [int(m.group(2)), int(m.group(3))]}
    feet = dict(re.findall(r"\| (\d) \| ([A-Z][^|]+?) (?=\|)", t[t.find("Footnotes"):]))
    for v in out.values():
        if v["footnote"]:
            v["footnote"] = feet.get(str(v["footnote"]), v["footnote"])
    src = cc.source_block("History, Art & Archives, U.S. House of Representatives, Party Divisions of the House "
                          "of Representatives, 1789 to Present", rec["url"], rec["read_utc"],
                          LICENCE.format("House"), mark="stated", note=f"sha256 {rec['sha256'][:16]}")
    return out, src


def main():
    s, s_src = senate()
    h, h_src = house()
    checks = []
    for n in range(110, 120):
        if str(n) not in s:
            checks.append(f"Senate: the {n}th Congress not parsed")
        if str(n) not in h:
            checks.append(f"House: the {n}th Congress not parsed")
    for n, v in s.items():
        if v["D"] + v["R"] + v["other"] + v["vacant"] != v["total"]:
            checks.append(f"Senate {n}: parties sum to {v['D'] + v['R'] + v['other'] + v['vacant']}, not {v['total']}")
    out = {"senate": s, "house": h, "sources": {"senate_gov": s_src, "house_history": h_src}, "checks": checks}
    cc.write_json(os.path.join(cc.CACHE, "divisions", "normalized", "divisions.json"), out)
    print(f"Senate: {len(s)} Congresses; House: {len(h)}; checks: {checks or 'all pass'}")
    for n in range(110, 120):
        print(n, s.get(str(n), {}).get("D"), s.get(str(n), {}).get("R"), s.get(str(n), {}).get("other"),
              s.get(str(n), {}).get("vacant"), "|", h.get(str(n), {}).get("D"), h.get(str(n), {}).get("R"),
              h.get(str(n), {}).get("footnote"))


if __name__ == "__main__":
    main()
