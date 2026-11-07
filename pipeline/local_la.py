"""pipeline/local_la.py: Louisiana's official 2024 results (pipeline/intake/la_sos.py), gated against the certified
federal counts, compared with MEDSL's Louisiana file, and put in the shape pipeline/local_medsl.py reads.

Written 2026-11-07 by worker D3 (briefs/D3-data-local.md, step 2) at the orchestrator's orders of 08:08 and 10:17
("Go on with LA 2024"). Why: MEDSL's 2024 Louisiana file counts Election Day only, so it falls 48.9% short of D1's
certified presidential count and its Louisiana contests are held back (no p; data/local/REPORT.md section 6). Where two
sources hold one contest the certified one wins (brief D3, step 2). So, if the state's file passes the gate,
local_medsl.load(2024) reads Louisiana's local races and questions from it in place of MEDSL's (certified_la there),
with MEDSL's routes; the presidency and Congress stay D1's and D2's. Louisiana elects no legislature in 2024.

Louisiana's rounds (each said in the contest's own words). Its local offices are filled at a primary, open to every
candidate, and, where no one is elected there, a general election between the leaders a few weeks later: in 2024 the
primaries of 2024-03-23 and 2024-11-05 and the generals of 2024-04-27 and 2024-12-07 [inferred: the four dates of the
source's 2024 list, and the contests it repeats from the first of each pair to the second]. La. R.S. 18:402, which
sets the dates, was read on 2026-11-07 at 10:46 UTC (https://legis.la.gov/Legis/Law.aspx?d=81545), as amended through
Acts 2025, No. 386: its text pairs each season's primary with a general on a later Saturday, but its dates are not
2024's, since it was amended after 2024 (Acts 2024, No. 640; Acts 2025, No. 386). So the 2024 pairing rests on the
source's repeated contests, and the statute is cited for the pairing's form only (the orchestrator, 2026-11-07 11:16).
  - A contest on a primary date is the first round of a two-round system: recorded with its result, p not computed
    (model section 7), as for Klarner's Louisiana legislature. Its candidates on the general's ballot are marked
    "to runoff"; where no general followed, the leading candidates for the seats are taken as elected [inferred].
  - A contest on a general date whose parish and title (seats aside) were on that pair's primary is its deciding
    round, and takes the routes' classes, marked "deciding round after an earlier round" (the orchestrator's ruling of
    2026-11-07 09:53 UTC for North Carolina: "the November count is the one that elects") [inferred: the ruling's
    reason holds for Louisiana's generals; the orchestrator is told].
  - A contest on a general date with no such primary in the source is recorded, p not computed, with that reason.
  - A question has no rounds. Questions are kept as the source gives them, each date its own.
  - The parties' own committees (the Democratic and Republican state central and parish executive committees, DSCC,
    RSCC, DPEC and RPEC) are elected "every four years at the same time as the presidential preference primary
    election", and "the candidate who receives the greater number of votes cast shall be elected", seat by seat, ties
    by lot (La. R.S. 18:443(B) and 18:444(B), read 2026-11-07 at 11:16 UTC, Law.aspx?d=81577 and d=81580) [stated].
    So each is decided at 2024-03-23 in one round. They are kept (the orchestrator's ruling of 2026-11-07 10:35: "put
    the party committees in ... Mark them as party offices whose voters are the party's own, compute them where a
    route fits"), with `party_office` on the record and the routes of their seats and ballot like any local office.
    Their voters are the party's own [inferred: La. R.S. 18:1280.21(B), Law.aspx?d=81288, gives each elector at that
    primary only his own party's candidates; the ruling].
Left out: the presidency, its party primaries and Congress (D1's and D2's levels).

  gate()         the file's Democratic and Republican votes for president (D1's data/president/2024.json) and each
                 House district (D2's data/house/2024.json) against the certified ones on 2024-11-05: (worst relative
                 miss, words); the line is local_medsl.QUALITY_LINE, as for North Carolina and Indiana.
  check()        the gate, and MEDSL's Louisiana contests of 2024-11-05 against the state's: data/local/check-la.json.
  medsl_shape()  the state's contests in local_medsl's load() shape, or None if a file is missing, not official on
                 the site's list, or fails the gate.

Run:  VOTE_CACHE=/tmp/vote-cache python3 pipeline/local_la.py check
"""
import argparse
import collections
import csv
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fetch as F  # noqa: E402
from intake import la_sos as SOS  # noqa: E402
import local as L  # noqa: E402
import local_medsl as LM  # noqa: E402

YEAR = 2024
SOURCE_KEY = "la_sos"
PAIRS = {"2024-04-27": "2024-03-23", "2024-12-07": "2024-11-05"}   # general date -> its primary (docstring)
PRIMARIES = set(PAIRS.values())
PARTY = {"DEM": "DEMOCRAT", "REP": "REPUBLICAN", "LBT": "LIBERTARIAN", "GRN": "GREEN", "IND": "INDEPENDENT",
         "NOPTY": "NO PARTY", "OTHER": "OTHER", "": "NONPARTISAN"}
FEDERAL = re.compile(r"^(Presidential Electors|Presidential Nominee|U\. S\. (Representative|Senator))")
PARTY_COMMITTEE = re.compile(r"^(DSCC|RSCC|DPEC|RPEC) Member")
COMMITTEES = {"DSCC": ("D", "the Democratic Party's state central committee", "18:443"),
              "RSCC": ("R", "the Republican Party's state central committee", "18:443"),
              "DPEC": ("D", "the Democratic Party's parish executive committee", "18:444"),
              "RPEC": ("R", "the Republican Party's parish executive committee", "18:444")}
LAW_URL = {"18:443": "https://legis.la.gov/Legis/Law.aspx?d=81577", "18:444": "https://legis.la.gov/Legis/Law.aspx?d=81580",
           "18:1280.21": "https://legis.la.gov/Legis/Law.aspx?d=81288", "18:402": "https://legis.la.gov/Legis/Law.aspx?d=81545"}
STATE_OFFICE = re.compile(r"^(District Judge|Judge, Court of Appeal|Justice, Supreme Court|PSC|District Attorney|"
                          r"BESE|Judge)")
N_PARISHES = 64
MEDSL_FIPS_FILE = os.path.join("medsl", "raw", "2024-13731147-2024-la-precinct-general.csv")


def load():
    path = os.path.join(SOS.NORM, f"{YEAR}.jsonl")
    if not os.path.exists(path):
        raise SystemExit(f"Louisiana's {YEAR} file is not in the cache: run pipeline/intake/la_sos.py fetch and read")
    with open(path) as f:
        return [json.loads(line) for line in f]


def checks_of():
    with open(os.path.join(SOS.NORM, f"checks-{YEAR}.json")) as f:
        return json.load(f)


def _key(s):
    return re.sub(r"[^A-Z]", "", s.upper())


def parish_fips():
    """Parish names to FIPS codes, from the county_name and county_fips columns of MEDSL's 2024 Louisiana file."""
    m = {}
    with open(os.path.join(F.CACHE, MEDSL_FIPS_FILE), newline="") as f:
        for row in csv.DictReader(f):
            m[_key(row["county_name"])] = row["county_fips"]
    return m, F.meta(MEDSL_FIPS_FILE)


def fips_source():
    _, fm = parish_fips()
    return F.source("parish FIPS codes: the county_name and county_fips columns of MEDSL's 2024 Louisiana precinct "
                    "file", fm["url"], fm["read_utc"], "CC0 1.0", mark="stated")


def _major(party):
    return {"DEM": "D", "REP": "R"}.get(party)


def _cert_major(party):
    """D1's and D2's party words ('Democratic', 'D', ...), as local_in's _major reads them."""
    p = (party or "").upper()
    return "D" if p in ("D", "DEM", "DEMOCRAT", "DEMOCRATIC") else "R" if p in ("R", "REP", "REPUBLICAN") else None


def _house_district(title):
    m = re.search(r"(\d+)(st|nd|rd|th) Congressional District", title)
    return int(m.group(1)) if m else None


def gate(cs=None):
    """(worst relative miss, words) of the file's D and R votes on 2024-11-05 against D1's and D2's certified
    counts."""
    cs = [c for c in (cs or load()) if c["date"] == "2024-11-05"]
    worst, what = 0.0, []
    for pat, level in (("Presidential Electors", "president"), ("U. S. Representative", "house")):
        mine = [c for c in cs if c["office"].startswith(pat)]
        with open(os.path.join(L.REPO, "data", level, f"{YEAR}.json")) as f:
            cert = [x for x in json.load(f)["contests"] if x["place"]["state"] == "LA" and not x.get("special")]
        if level == "house":
            byd = {int(x["place"]["district"]): x for x in cert}
            pairs = [([c], [byd[_house_district(c["title"])]]) for c in mine if _house_district(c["title"]) in byd]
        else:
            pairs = [(mine, cert)]
        for side in ("D", "R"):
            a = sum(x["votes"] for m_, _ in pairs for c in m_ for x in c["candidates"] if _major(x["party"]) == side)
            b = sum(x["votes"] for _, c_ in pairs for c in c_ for x in c["result"]["candidates"]
                    if _cert_major(x.get("party")) == side)
            if not b:
                continue
            what.append(f"{level} {side} {a:,} against {b:,}" + (f" ({len(pairs)} districts)" if level == "house" else ""))
            for m_, c_ in pairs:
                aa = sum(x["votes"] for c in m_ for x in c["candidates"] if _major(x["party"]) == side)
                bb = sum(x["votes"] for c in c_ for x in c["result"]["candidates"] if _cert_major(x.get("party")) == side)
                if bb:
                    worst = max(worst, abs(aa - bb) / bb)
    return worst, "; ".join(what)


def _base(title):
    return SOS.SEATS.sub("", title)


def rounds(cs):
    """For each contest (by id()), its round: ("first", the general's date or None), ("deciding", the primary's date),
    ("general, no primary", None), or None for a question."""
    on = collections.defaultdict(dict)
    for c in cs:
        if c["kind"] == "office":
            on[("multi" if c["multi_parish"] else c["sheet"], _base(c["title"]))][c["date"]] = c
    out = {}
    for c in cs:
        if c["kind"] != "office":
            out[id(c)] = None
            continue
        if PARTY_COMMITTEE.match(c["office"]):   # one round, the most votes elected (La. R.S. 18:443, 18:444)
            out[id(c)] = ("party committee", None, None)
            continue
        k = ("multi" if c["multi_parish"] else c["sheet"], _base(c["title"]))
        if c["date"] in PRIMARIES:
            g = next((d for d, p in PAIRS.items() if p == c["date"] and d in on[k]), None)
            out[id(c)] = ("first", g, on[k].get(g))
        elif c["date"] in PAIRS:
            p = PAIRS[c["date"]]
            out[id(c)] = ("deciding", p, on[k][p]) if p in on[k] else ("general, no primary", None, None)
        else:
            out[id(c)] = ("general, no primary", None, None)
    return out


def _won(c, r):
    """The source marks no winners. A first round's candidates on the general's ballot go "to runoff"; any who led
    them all were elected in it; where no general followed, the leaders for the seats were [inferred]. Elsewhere, the
    leaders for the seats, none at a tie for the last (local_medsl's rule)."""
    order = sorted(c["candidates"], key=lambda x: -x["votes"])
    k = c["seats"]
    tie = len(order) > k and order[k - 1]["votes"] == order[k]["votes"]
    if r and r[0] == "first" and r[2] is not None:
        later = {x["name"] for x in r[2]["candidates"]}
        top = max((x["votes"] for x in order if x["name"] in later), default=0)
        return {x["name"]: ("to runoff" if x["name"] in later else True if x["votes"] > top else None) for x in order}
    winners = set() if tie else {x["name"] for x in order[:k]}
    return {x["name"]: (True if x["name"] in winners else None) for x in order}


def election_words(r, date):
    if r is None:
        return "election" + (" (Louisiana's primary date)" if date in PRIMARIES else
                             " (Louisiana's general election date)" if date in PAIRS else "")
    if r[0] == "first":
        return (f"first round: Louisiana's primary, its general election followed on {r[1]}" if r[1] else
                "first round: Louisiana's primary, decided in it (no general election of this contest followed)") + \
            " [inferred]"
    if r[0] == "party committee":
        return ("the party's own election of its committee's members, held with the presidential preference primary "
                "and decided in it: the most votes are elected (La. R.S. 18:443, 18:444) [stated]")
    if r[0] == "deciding":
        return f"deciding round after an earlier round on {r[1]} (Louisiana's general election after its primary) " \
               f"[inferred]"
    return "Louisiana's general election date, with no primary of this contest in the source [inferred]"


def medsl_shape(year=YEAR):
    """Louisiana's 2024 contests, not federal, in local_medsl's load() shape; None if the file is missing, a date is
    not official, or the file fails the gate."""
    if year != YEAR or not os.path.exists(os.path.join(SOS.NORM, f"{YEAR}.jsonl")):
        return None
    cs = load()
    meta = checks_of()
    if any(f.get("official") != "1" for f in meta["files"].values()) or gate(cs)[0] > LM.QUALITY_LINE:
        return None
    fips, _ = parish_fips()
    rd = rounds(cs)
    out = []
    for c in cs:
        if FEDERAL.match(c["office"]):
            continue
        fm = meta["files"][c["date"]]
        parishes = sorted({fips[_key(p)] for p in c["parishes"] if _key(p) in fips})
        statewide = len(parishes) == N_PARISHES
        r = rd[id(c)]
        title = ", ".join(x for x in (c["office"], c["place"]) if x).upper()   # "MAYOR, TOWN OF MELVILLE"
        base = {"state": "LA", "date": c["date"], "stage": "GEN", "special": False, "subject": None,
                "precincts": None, "counties": parishes, "source": SOURCE_KEY, "id_date": True,
                "election_words": election_words(r, c["date"]),
                "file": {"name": fm["url"].rsplit("/", 1)[1], "url": fm["url"], "read_utc": fm["read_utc"],
                         "sha256": fm["sha256"]}}
        if c["kind"] == "question":
            amendment = c["office"].startswith("CA No.")
            out.append(dict(base, dataverse="STATE" if statewide else "LOCAL", office=title,
                            district="STATEWIDE" if statewide else "", magnitude=None, question=True,
                            question_type="Constitutional Amendment" if amendment and statewide else None,
                            candidates=[{"name": re.sub(r"^(FOR|AGAINST)\s*RECALL$", r"\1 RECALL", x["name"].upper()),
                                         "votes": x["votes"]} for x in c["candidates"]]))   # "ForRecall": a recall
            continue
        won = _won(c, r)
        cands = [{"name": x["name"], "votes": x["votes"], "as_named": True, "won_marked": won[x["name"]],
                  "party": PARTY.get(x["party"], x["party"])} for x in c["candidates"]]
        held = None
        if r and r[0] == "first":
            held = ("the first round of Louisiana's two-round system: a vote there works through who is elected "
                    "outright or advances (model section 7); recorded, p not computed")
        elif r and r[0] == "general, no primary":
            held = ("on Louisiana's general election date, with no primary of this contest in the source, so which "
                    "round it is cannot be read: p not computed")
        rec = dict(base, dataverse="STATE" if (statewide or STATE_OFFICE.match(c["office"])) else "LOCAL",
                   office=title, district="STATEWIDE" if statewide else "", magnitude=c["seats"],
                   question=False, candidates=cands, held_round=held,
                   earlier_round=[r[1]] if r and r[0] == "deciding" else None)
        if r and r[0] == "party committee":
            side, body, sec = COMMITTEES[c["office"].split()[0]]
            rec["party_office"] = {"party": side, "body": body, "law": f"La. R.S. {sec}", "law_url": LAW_URL[sec],
                                   "voters": "the party's own [inferred: La. R.S. 18:1280.21(B); the orchestrator's "
                                             "ruling of 2026-11-07 10:35]"}
        out.append(rec)
    return out


def source_block():
    meta = checks_of()
    files = "; ".join(f"{d} ({f['url'].rsplit('/', 1)[1]}, sha256 {f['sha256'][:12]}, {f['contests']} contests)"
                      for d, f in sorted(meta["files"].items()))
    read = max(f["read_utc"] for f in meta["files"].values())
    return F.source("Louisiana Secretary of State, official election results (the results site's workbook of each "
                    "date)", SOS.SITE, read, SOS.LICENCE, mark="stated",
                    note=f"each date marked official on the site's list of elections ('ResultsOfficial': '1'); "
                         f"files read by pipeline/intake/la_sos.py: {files}")


def _sig(cands):
    return tuple(sorted((x["votes"] for x in cands if not LM._is_generic(x["name"]) and not x.get("writein")),
                        reverse=True))


def check():
    cs = load()
    w, words = gate(cs)
    rd = rounds(cs)
    t = collections.Counter()
    for c in cs:
        if FEDERAL.match(c["office"]):
            t["left out: the presidency, its primaries and Congress"] += 1
        else:
            r = rd[id(c)]
            t[f"{c['date']}: " + ("question" if r is None else r[0])] += 1
    # MEDSL's Louisiana contests of 2024-11-05, held back: the same names, and how far their votes fall short
    med = []
    for p in sorted(os.listdir(os.path.join(LM.NORM, str(YEAR)))):
        if p.startswith("LA-"):
            with open(os.path.join(LM.NORM, str(YEAR), p)) as f:
                med += [json.loads(ln) for ln in f]
    mine = {}
    for c in cs:
        if c["date"] == "2024-11-05":
            mine.setdefault(frozenset(LM.name_key(x["name"]) for x in c["candidates"]), []).append(c)
    m_t, ratios = collections.Counter(), []
    for m in med:
        if "state" not in m or m.get("dataverse") not in ("STATE", "LOCAL") or m["office"] in LM.LEG:
            continue
        names = frozenset(LM.name_key(x["name"]) for x in m["candidates"] if not LM._is_generic(x["name"])
                          and not x.get("writein"))
        hit = mine.get(names)
        if not hit:
            m_t["MEDSL: not found by its candidates' names in the state's file"] += 1
            continue
        a, b = sum(x["votes"] for x in m["candidates"]), sum(x["votes"] for x in hit[0]["candidates"])
        m_t["MEDSL: found"] += 1
        if b:
            ratios.append(a / b)
    ratios.sort()
    out = {"about": "Louisiana's official 2024 results (pipeline/intake/la_sos.py) against the certified federal "
                    "counts, and MEDSL's 2024 Louisiana contests against them. Built by pipeline/local_la.py check.",
           "gate": {"worst_miss": round(w, 6), "fails": w > LM.QUALITY_LINE, "counts": words},
           "contests": dict(sorted(t.items())),
           "medsl_2024_11_05": dict(m_t, medsl_votes_over_the_states_median=round(ratios[len(ratios) // 2], 4)
                                    if ratios else None)}
    with open(os.path.join(L.REPO, "data", "local", "check-la.json"), "w") as f:
        json.dump(out, f, indent=1)
        f.write("\n")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("what", choices=["check"])
    ap.parse_args()
    print(json.dumps(check(), indent=1))


if __name__ == "__main__":
    main()
