"""pipeline/intake/va_elect.py: Virginia's general elections of 2023 and 2025, from the Department of Elections' results
site, as read before the Department refused us; nothing is requested from it again.

Written 2026-11-07 by worker D3 (briefs/D3-data-local.md, step 2) at the orchestrator's order of 10:35: "queue the
odd-year legislatures after Klarner's 2022 (MS, NJ, VA 2023; NJ, VA 2025) from each state's certified files, each with
a gate you propose. Reason: law 5 and Zach's 03:13 word, as much data as can be found." Klarner's Virginia ends with
the House of Delegates of 2021 and MEDSL holds no odd year, so the Department's own results are the only source.

The refusal. The Department's CSV host, apps.elections.virginia.gov, answered HTTP 403 "Access Denied" at 18:27:48 UTC
(its "Winners List" directory) and again at 18:28:44 (a results file, requested after the first refusal, which it should
not have been). The orchestrator (18:30): the refusal binds the whole Department, so none of its hosts is read again,
rendered or not; what was read before 18:27:48 stands. So this script requests nothing: it reads the files below from
the cache ($VOTE_CACHE/va_elect/raw/), each with its .meta.json (url, the time its read finished, sha256), and stops if
one is missing. A later reader may fetch them again by hand once the Department answers; a refusal is recorded, never
routed round.

The files, all read before the refusal [measured: their times]:
  election-results-page.html  https://www.elections.virginia.gov/resultsreports/election-results/ (curl, 18:20:42):
      the Department's "Election Results" page. It links the 2025 general ("November 4, 2025 General and Special
      Elections") to the results site, and says "Election Results starting with the June 2023 Primaries to the most
      recent election can be found at the Election Results Directory", linked to the site's directory.
  directory-rendered.html  https://enr.elections.virginia.gov/results/public/virginia (rendered in headless Chromium,
      18:22:18; the site serves a script shell, which the orchestrator's ruling of 08:00 lets us render): lists
      "2023 November General and Special Elections" at /results/public/virginia/2023-Nov-Gen.
  2023-Nov-Gen-page-rendered.html  the 2023 general's page, rendered and scrolled to its end until its contests
      stopped growing (183), no click (18:26:19; pipeline/intake/render_scroll.cjs's steps).
  2025-November-General-page-rendered.html  the 2025 general's page, rendered, not scrolled (18:23:53): its first 50
      contests.
  export-<election>.json  each page's "Media Export" link, /cdn/results/<jurisdiction>/export-<election>.json (curl,
      18:23:02 and 18:24:08): the election's every contest, its statewide count, and each locality's (Virginia's
      counties and independent cities) count, option by option, with its precincts.
  Each page is headed "<election> <date> OFFICIAL RESULTS Last Updated <date>" [stated: the rendered page], and each of
  its contests shows its candidates, each with "Winner" beside the winner, party, share and votes, and "Localities
  reporting n/n".

What it writes: $VOTE_CACHE/va_elect/normalized/<year>-general.json, {"year", "date", "name", "official",
"official_text", "last_updated", "linked", "files", "contests": [{"title", "vote_for", "options": [{"id", "name",
"party", "votes", "write_in", "winner_marked"}], "statewide_total", "localities": n, "parts_add_up",
"extra_in_localities", "precincts_short", "page": {"shown", "equal", "localities_reporting"}}]}.

Run:  VOTE_CACHE=/tmp/vote-cache python3 -I pipeline/intake/va_elect.py [2023 2025]
"""
import collections
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import fetch as F  # noqa: E402

RAW = "va_elect/raw"
NORM = os.path.join(F.CACHE, "va_elect", "normalized")
PAGE = "https://www.elections.virginia.gov/resultsreports/election-results/"
SITE = "https://enr.elections.virginia.gov"
DIRECTORY = SITE + "/results/public/virginia"
LICENCE = "no licence printed; the Virginia Department of Elections' official election results, public records"
ELECTION = {2023: "2023-Nov-Gen", 2025: "2025-November-General"}
REFUSED = ("the Virginia Department of Elections refused us at 2026-11-07 18:27:48 UTC (apps.elections.virginia.gov, "
           "HTTP 403 'Access Denied'); the orchestrator, 18:30: none of its hosts is read again, rendered or not")


def _need(name):
    path = os.path.join(F.CACHE, name)
    if not (os.path.exists(path) and os.path.exists(path + ".meta.json")):
        raise SystemExit(f"va_elect: {name} is not in the cache, and it is not requested: {REFUSED}")
    return path


def _tokens(path):
    """The rendered page's text, one token per element, scripts and styles left out."""
    with open(path, encoding="utf-8", errors="replace") as f:
        s = re.sub(r"<(script|style)\b.*?</\1>", "", f.read(), flags=re.S | re.I)
    return [re.sub(r"\s+", " ", t).strip() for t in html.unescape(re.sub(r"<[^>]+>", "\x00", s)).split("\x00")
            if t.strip()]


def _links(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        s = f.read()
    return [(html.unescape(h), re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t))).strip())
            for h, t in re.findall(r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>', s, re.S | re.I)]


def page_contests(toks):
    """Each contest the rendered page shows: {title: {"vote_for", "candidates": [{name, winner, party, votes}],
    "localities_reporting"}}. A contest's block runs from its title (the token before "Vote for ...") to "View
    results by locality"."""
    out = {}
    i = 0
    while i < len(toks):
        if toks[i].lower().startswith("vote for "):
            title, vote_for, cands, rep = toks[i - 1], toks[i], [], None
            i += 1
            while i < len(toks) and toks[i] != "View results by locality":
                if toks[i] == "Candidate" and i + 1 < len(toks) and toks[i + 1] != "Percentage":
                    j, seg = i + 2, []
                    while toks[j] != "Percentage":
                        seg.append(toks[j])
                        j += 1
                    if toks[j + 2] != "Votes":
                        raise SystemExit(f"va_elect: the page's contest {title!r} is not laid out as read")
                    cands.append({"name": toks[i + 1], "winner": "Winner" in seg,
                                  "party": " ".join(x for x in seg if x != "Winner") or None,
                                  "votes": int(toks[j + 3].replace(",", ""))})
                    i = j + 4
                    continue
                if toks[i] == "Localities reporting":
                    rep = toks[i + 1]
                i += 1
            if title in out:
                raise SystemExit(f"va_elect: the page shows {title!r} twice")
            out[title] = {"vote_for": vote_for, "candidates": cands, "localities_reporting": rep}
        i += 1
    return out


def read(year):
    eid = ELECTION[year]
    names = {"page": f"{RAW}/election-results-page.html", "directory": f"{RAW}/directory-rendered.html",
             "election": f"{RAW}/{eid}-page-rendered.html", "export": f"{RAW}/export-{eid}.json"}
    paths = {k: _need(v) for k, v in names.items()}
    # linked from the Department's page: directly (2025), or by its Election Results Directory (2023)
    dept = _links(paths["page"])
    target = f"{DIRECTORY}/{eid}".lower()
    direct = [t for h, t in dept if h.lower().rstrip("/") == target]
    if direct:
        linked = f"the Department's results page links it as {direct[0]!r}"
    else:
        to_dir = [t for h, t in dept if h.lower().rstrip("/") == DIRECTORY.lower()]
        listed = [t for h, t in _links(paths["directory"]) if h.lower().rstrip("/") == f"/results/public/virginia/{eid}"
                  .lower()]
        with open(paths["page"], encoding="utf-8", errors="replace") as f:
            said = "can be found at the" in re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", f.read()))
        if not (to_dir and listed and said):
            raise SystemExit(f"va_elect {year}: the Department's page links neither the election nor a directory "
                             f"listing it")
        linked = (f"the Department's results page says results from the June 2023 primaries on are at its "
                  f"{to_dir[0]!r}, which lists it as {listed[0]!r}")
    toks = _tokens(paths["election"])
    official = "OFFICIAL RESULTS" in toks
    k = toks.index("OFFICIAL RESULTS") if official else None
    heading = toks[k - 2:k + 3] if official else []
    last_updated = toks[k + 2] if official and toks[k + 1] == "Last Updated" else None
    export_links = [h for h, t in _links(paths["election"]) if t == "Media Export"]
    meta_x = F.meta(names["export"])
    if len(export_links) != 1 or SITE + export_links[0] != meta_x["url"]:
        raise SystemExit(f"va_elect {year}: the page's Media Export link {export_links} is not the file read, "
                         f"{meta_x['url']}")
    shown = page_contests(toks)
    with open(paths["export"]) as f:
        x = json.load(f)
    # each locality's line of each contest, option by option, and its precincts
    loc = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    short = collections.defaultdict(list)
    seen_in = collections.defaultdict(dict)   # an option's name and localities, as the locality lines name it
    for lr in x["localResults"]:
        for b in lr["ballotItems"]:
            for o in b["ballotOptions"]:
                loc[b["id"]][lr["id"]][o["id"]] += o["voteCount"]
                seen_in[o["id"]].setdefault("name", o["name"].strip())
                seen_in[o["id"]].setdefault("localities", []).append(lr["name"].title())
                if o["precinctResults"] is not None:
                    ps = sum(p["voteCount"] for p in o["precinctResults"])
                    if ps != o["voteCount"]:
                        short[b["id"]].append({"locality": lr["name"].title(), "option": o["name"].strip(),
                                               "locality_line": o["voteCount"], "precincts": ps})
    contests = []
    for b in x["results"]["ballotItems"]:
        opts = [{"id": o["id"], "name": o["name"].strip(), "party": o["politicalParty"], "votes": o["voteCount"],
                 "write_in": o["id"].startswith("wi-")} for o in b["ballotOptions"]]
        state = {o["id"]: o["votes"] for o in opts}
        added = collections.Counter()
        for lid, cnt in loc[b["id"]].items():
            added.update(cnt)
        extra = [{"option": oid, "name": seen_in[oid]["name"], "localities": seen_in[oid]["localities"], "votes": v}
                 for oid, v in sorted(added.items()) if oid not in state]
        parts_add_up = all(added[oid] == v for oid, v in state.items()) and not extra
        pg = shown.get(b["name"])
        page = {"shown": pg is not None}
        if pg:
            page["equal"] = sorted((c["name"].strip(), c["votes"]) for c in pg["candidates"]) == \
                sorted((o["name"], o["votes"]) for o in opts)
            page["localities_reporting"] = pg["localities_reporting"]
            won = {c["name"].strip() for c in pg["candidates"] if c["winner"]}
            for o in opts:
                o["winner_marked"] = o["name"] in won
        contests.append({"title": b["name"].strip(), "vote_for": b["voteFor"], "options": opts,
                         "statewide_total": sum(state.values()), "localities": len(loc[b["id"]]),
                         "locality_ids": sorted(loc[b["id"]]),
                         "precinct_ids": sorted(f"{lr['id']}|{p['id']}" for lr in x["localResults"]
                                                for bb in lr["ballotItems"] if bb["id"] == b["id"]
                                                for p in (bb["ballotOptions"][0]["precinctResults"] or [])
                                                if not p["isVirtual"]),
                         "parts_add_up": parts_add_up, "extra_in_localities": extra,
                         "precincts_short": short.get(b["id"], []), "page": page})
    files = {k: dict(F.meta(v), cache=v) for k, v in names.items()}
    out = {"year": year, "date": x["electionDate"], "name": x["electionName"], "official": official,
           "official_text": " ".join(heading), "last_updated": last_updated, "linked": linked,
           "export_created_utc": x.get("createdAt"), "files": files, "page_contests_shown": len(shown),
           "contests": contests}
    os.makedirs(NORM, exist_ok=True)
    with open(os.path.join(NORM, f"{year}-general.json"), "w") as f:
        json.dump(out, f, indent=1)
    return out


def main(argv):
    years = [int(a) for a in argv] or sorted(ELECTION)
    for y in years:
        r = read(y)
        n_leg = sum(1 for c in r["contests"] if c["title"].startswith(("Member, House of Delegates",
                                                                         "Member, Senate of Virginia")))
        print(f"{y}: {r['name']!r}, {r['official_text']!r}; {len(r['contests'])} contests ({n_leg} of the legislature), "
              f"{r['page_contests_shown']} shown on the page; localities add up in "
              f"{sum(c['parts_add_up'] for c in r['contests'])}; page equal in "
              f"{sum(1 for c in r['contests'] if c['page'].get('equal'))}")


if __name__ == "__main__":
    main(sys.argv[1:])
