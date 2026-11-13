"""pipeline/local_recount.py: the recount zone beside p, for D3's levels (brief D3 step 4; model section 3, the
drivers table; MATH 5.10).

Written 2026-11-13 by worker D3 on the orchestrator's orders of 09:23, 09:58, 10:06 and 10:12 UTC. The brief (step 4):
"check where the zone a recount can swing comes near the forecast's spread in votes, and report where p would change
(model section 3, the drivers table; section 10)". Model section 3's words: "leave p unchanged ... when the zone a
recount can swing (hundreds to a few thousand votes) is much narrower than the forecast's spread in votes ... At a zone
a third the size of the spread, p is still 96% of its value (MATH 5.10) ... In a small local race the two can be
closer; the model checks this there when it has the data (section 10)". The orchestrator, 09:58: "The zone sits beside
p: a listing and a note, not a change to p, unless the model's section 3 says otherwise"; 10:12, 1: "p stays unchanged
everywhere ... Changing p where the zone comes near would be a change of method, and the zone's rate rests on an
[inferred] step."

The rate (the orchestrator, 10:06): "The zone is 0.87%, the authors' own baseline (hand counts without Bradford, Table 2,
p. 5). Show the 95% upper bound, 1.06%, beside it as a check, and list 2.49% (Bradford in) as a sensitivity". Reason:
"the authors name 0.87% the baseline and set Bradford apart, and the site states one figure and shows what moves it."
The figures are Ansolabehere and Reeves's, VTP working paper 11 (January 2004), read once at 10:00:04 UTC (SOURCES).

The one inferred step, in the orchestrator's words (10:06): "The paper measures a candidate's change within one town,
as a share of that candidate's votes, and you apply it to a race's whole count. Changes may add or cancel across towns
and candidates, so the zone you build is a gross figure, as §3 treats Minnesota's 2,170." So the zone is
w = rate x n votes of margin, n the count p is computed at (p.n), and MATH 5.10's logistic has scale w [inferred].

"Near" (the orchestrator, 10:12, 2): "a zone at or above a third of the spread, which is where gain falls to about 0.96
of p. It is the same line as the 4% effect, and it is the model's words." The spread in votes is n x sd: sd is the
forecast's own for route (a) (forecasts[0].share.sd); for the like-race routes (class, boundary, runoff, like past
measures) it is the sd of the normal device through which pipeline/local.py _p_like computes their p, its line
"sd = 1.0 / (math.sqrt(2 * math.pi) * f)", centred at 1/2 (at the threshold for a measure), with f the record's
p.f_half (p.f_t) (the orchestrator, 10:12, 4). Since w / (n sd) = rate / sd, whether a race is near does not depend on
its size.

gain / p: MATH 5.10's smoothed gain over the sharp p, in its continuous form: the forecast's density of the share
averaged over a logistic of scale rate / 2 in the share (w votes of margin) at the point p is taken at, over that
density there. `check` asserts that this reproduces MATH 5.10's table (model/math/OUTPUT.txt) within 0.002.

What it writes (`build`), p unchanged everywhere:
  - data/local/recount-zone.json: every race near at 2.49% (which holds every race near at 1.06% and 0.87%), with the
    zone, the spread and gain / p at each rate; the counts by level and route; the races the zone raises in the tails
    counted, not listed (10:12, 5).
  - one note in each record near at 0.87% (10:12, 3: "the zone in votes, the spread it is set against, and gain/p at
    0.87% marked [inferred]. Records near only at 1.06% or 2.49% appear in the listing, not in a note"). The note is
    written by this step after the builds, as pipeline/governor_counts.py writes its text: run it after
    pipeline/local.py, local_medsl.py and local_ncsbe.py build, since each rewrites its records without it. Any
    earlier zone note is taken out first, so the step can be run again.
`check` recomputes everything and writes nothing: it fails if a record's note or the listing differs, and, with
$VOTE_CACHE, checks each cached source's sha256 and that every figure quoted below is in it.

Run:  python3 pipeline/local_recount.py build
      VOTE_CACHE=/tmp/vote-cache python3 pipeline/local_recount.py check
"""
import glob
import hashlib
import html
import json
import math
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import local as L   # noqa: E402  (write_level_file: the builders' own layout, one contest per line)

LEVELS = ("state-lower", "state-upper", "local", "primary", "measure")
OUT = os.path.join(ROOT, "data", "local", "recount-zone.json")
NEAR = 1.0 / 3.0   # model section 3: "a zone a third the size of the spread"
NOTE_HEAD = "Recount zone [inferred]:"

SOURCES = {
    "ansolabehere_reeves": {
        "name": "Stephen Ansolabehere and Andrew Reeves, Using Recounts to Measure the Accuracy of Vote Tabulations: "
                "Evidence from New Hampshire Elections 1946-2002, Caltech/MIT Voting Technology Project working paper "
                "11, January 2004",
        "url": "https://vote.caltech.edu/documents/133/vtp_wp11.pdf",
        "read_utc": "2026-11-13T10:00:04Z",
        "bytes": 134241,
        "sha256": "2b62faced09db789732ecdf23e2c64060929c0017692f298338499b4ac551dcf",
        "cache": "recount/raw/vtp_wp11.pdf",
        "licence": "none printed in the file [measured: no licence, copyright or rights line in its text]; its figures "
                   "are quoted here with page and table, and the file is not kept in the repository",
        "mark": "stated",
        "figures": [
            {"where": "p. 3", "what": "New Hampshire's general elections 1946-1962: 108 races recounted, 69 of them "
                                      "for state representative; 415 cases, a case a candidate's count in one town "
                                      "(or district)",
             "quote": ["In the general elections in this span, 108 races had recounts",
                       "The majority of the recounts (69) occurred in races for state representative",
                       "Our analysis consists of 415 cases"]},
            {"where": "p. 4", "what": "1946-1962, hand counts: the mean change from the first count to the recount, "
                                      "weighted by ballots, 0.83% (95% interval 0.61 to 1.05)",
             "quote": ["approximately 0.83 percentage point with a 95%", "from 0.61 to 1.05"]},
            {"where": "Table 2, p. 5", "what": "2002 general election: hand-counted 92 cases, 2.49% (1.44, 3.55), "
                                               "maximum 21.88; hand-counted without Bradford 79 cases, 0.87% "
                                               "(0.69, 1.06), maximum 4.08; machine counted 217 cases, 0.56% "
                                               "(0.42, 0.70), maximum 8.27",
             "quote": ["Hand-Counted 92 2.49 (1.44, 3.55) 21.88", "Hand-Counted 79 0.87 (0.69, 1.06) 4.08",
                       "(without Bradford)", "Machine Counted 217 0.56 (0.42, 0.70) 8.27"]},
            {"where": "p. 5", "what": "the authors take hand counts without Bradford as the baseline",
             "quote": ["The results for hand-counted paper, excluding Bradford, are nearly identical to the",
                       "We take this as the baseline"]},
        ],
    },
    "fairvote": {
        "name": "Deb Otis and Bryan Huang, An analysis of statewide election recounts, 2000-2023, FairVote, "
                "28 October 2024",
        "url": "https://fairvote.org/report/election-recounts-2024/",
        "read_utc": "2026-11-13T10:00:09Z",
        "bytes": 215078,
        "sha256": "2b5dbfcfcccae32ce17da518a795b7d1c5b273696caca85716421bd1c15be7bc",
        "cache": "recount/raw/fairvote-election-recounts-2024.html",
        "licence": "none printed on the page [measured: no licence or copyright line in its source]; three figures "
                   "quoted, the page not kept",
        "mark": "stated",
        "use": "an illustration only; none sets the rate (the orchestrator, 10:06). FairVote is an advocacy group, so "
               "only races it names with state, year and shift are taken (09:58); its 36-race list is an embedded "
               "table and a spreadsheet outside the page, not read, and its averages are left out",
        "figures": [
            {"race": "Washington, governor, 2004", "shift": 390,
             "what": "Rossi ahead by 261 at first; Gregoire by 129 after the recount, of 2,746,593 votes",
             "quote": ["The recount shifted the margin by 390 votes"]},
            {"race": "Vermont, state auditor, 2006", "shift": 239,
             "what": "the incumbent ahead by 137 at first; Salmon by 102 after the recount",
             "quote": ["by 239 votes, a change of 0.11 percentage points"]},
            {"race": "Minnesota, US Senate, 2008", "shift": 440,
             "what": "Coleman ahead by 215 at first; Franken by 225 at the end",
             "quote": ["The recount delivered a 440-vote swing to Franken"]},
        ],
    },
}

RATES = (
    ("0.87%", 0.0087, "the zone: hand counts without Bradford, the authors' baseline (Table 2, p. 5)"),
    ("1.06%", 0.0106, "the check: the upper end of that row's 95% interval (Table 2, p. 5)"),
    ("2.49%", 0.0249, "the sensitivity: hand counts with Bradford in (Table 2, p. 5)"),
)
ZONE = RATES[0]

GROSS = ("\"The paper measures a candidate's change within one town, as a share of that candidate's votes, and you "
         "apply it to a race's whole count. Changes may add or cancel across towns and candidates, so the zone you "
         "build is a gross figure, as \u00a73 treats Minnesota's 2,170.\" (the orchestrator, 2026-11-13 10:06)")
DEVICE_LINE = "sd = 1.0 / (math.sqrt(2 * math.pi) * f)"
MATH_5_10 = {(0.50, 10): 1.000, (0.50, 100): 1.000, (0.50, 1000): 0.958, (0.50, 3000): 0.760, (0.50, 10000): 0.347,
             (0.52, 10): 1.000, (0.52, 100): 1.000, (0.52, 1000): 0.975, (0.52, 3000): 0.830, (0.52, 10000): 0.420}


# ------------------------------------------------------------------ MATH 5.10's smoothed gain

def _npdf(x, m, s):
    return math.exp(-0.5 * ((x - m) / s) ** 2) / (s * math.sqrt(2 * math.pi))


def _lpdf(u, b):
    e = math.exp(-abs(u) / b)
    return e / (b * (1 + e) ** 2)


def gain_over_p(mu, sd, rate, at=0.5, steps=400):
    """MATH 5.10's gain over the sharp p, continuous form: the normal (mu, sd) density of the share, averaged over a
    logistic of scale rate/2 in the share (w = rate x n votes of margin, as 5.10's pi(m) = 1/(1 + exp(-m/w))) centred
    at `at`, over the density at `at`. Simpson's rule over +-40 scales."""
    b = rate / 2.0
    half = 40 * b
    h = 2 * half / steps
    tot = 0.0
    for i in range(steps + 1):
        u = -half + i * h
        wgt = 1 if i in (0, steps) else (4 if i % 2 else 2)
        tot += wgt * _lpdf(u, b) * _npdf(at + u, mu, sd)
    return tot * h / 3 / _npdf(at, mu, sd)


def check_math():
    """MATH 5.10's table (n = 100,000, sd 0.03, w votes), reproduced within 0.002."""
    for (mu, w), want in sorted(MATH_5_10.items()):
        got = gain_over_p(mu, 0.03, w / 100000.0, steps=4000)
        if abs(got - want) > 0.002:
            raise SystemExit(f"MATH 5.10 not reproduced: mu {mu}, w {w}: {got:.4f} against {want}")
    return "MATH 5.10's table reproduced within 0.002 (mu 0.50 and 0.52; w 10, 100, 1,000, 3,000, 10,000 votes)"


# ------------------------------------------------------------------ the spread each record's p is computed under

def spread(c):
    """(route, centre, sd, where the sd is from, the point p is taken at) for a record with p above 0, else None."""
    p = c.get("p")
    if not isinstance(p, dict) or not p.get("value") or not p.get("n"):
        return None
    fc = (c.get("forecasts") or [{}])[0]
    sh = fc.get("share") or {}
    if sh.get("sd"):
        return fc.get("route"), sh["mean"], sh["sd"], "the forecast's own sd", 0.5
    if p.get("f_half"):
        return (fc.get("route"), 0.5, 1.0 / (math.sqrt(2 * math.pi) * p["f_half"]),
                "the normal device of pipeline/local.py _p_like", 0.5)
    if p.get("f_t"):
        t = p.get("threshold", 0.5)
        return (fc.get("route"), t, 1.0 / (math.sqrt(2 * math.pi) * p["f_t"]),
                "the normal device of pipeline/local.py _p_like, at the threshold", t)
    return None


def note_text(n, sd, how, g):
    w = ZONE[1] * n
    dev = (f" The spread of a like-race route is the sd of the normal device through which pipeline/local.py _p_like "
           f"computes its p, \"{DEVICE_LINE}\" (the orchestrator, 10:12)." if "device" in how else "")
    return (f"{NOTE_HEAD} at 0.87%, Ansolabehere and Reeves's baseline for the change a recount makes in a hand count "
            f"(VTP working paper 11, Table 2, p. 5: per candidate per town, New Hampshire 2002, without Bradford), "
            f"this race's zone is about {w:,.0f} votes, against the forecast's spread of {n * sd:,.0f} votes "
            f"({n:,} x sd {sd:.4f}, {how}), at or above the third of the spread at which model section 3 says p is "
            f"still 96% of its value; by MATH 5.10 the chance a ballot changes who is declared the winner is then {g:.3f} of "
            f"p [inferred]. {GROSS}{dev} p is unchanged (model section 3; the orchestrator, 10:12: \"p stays unchanged "
            f"everywhere\"); data/local/recount-zone.json lists this race with the 1.06% check and the 2.49% "
            f"sensitivity.")


# ------------------------------------------------------------------ the scan

def files():
    for lev in LEVELS:
        for path in sorted(glob.glob(os.path.join(ROOT, "data", lev, "*", "*.json"))):
            yield lev, path


def compute():
    """Every record with p above 0: the listing of those near at any rate, the notes for those near at 0.87%, and the
    counts."""
    rows, notes, counts, cache = [], {}, {}, {}
    for lab, _r, _w in RATES:
        counts[lab] = {"near": 0, "by_level_and_route": {}, "gain_over_p": None,
                     "raised_in_the_tails": {"races": 0, "p_at_most": 0.0}}
    seen = 0
    for lev, path in files():
        with open(path) as f:
            d = json.load(f)
        for c in d.get("contests", []):
            s = spread(c)
            if s is None:
                continue
            seen += 1
            route, mu, sd, how, at = s
            n = c["p"]["n"]
            per = []
            for lab, rate, _ in RATES:
                k = (round(mu, 6), round(sd, 6), rate, at)
                if k not in cache:
                    cache[k] = gain_over_p(mu, sd, rate, at)
                g = cache[k]
                near = rate * n >= NEAR * n * sd
                per.append((lab, rate, near, g))
                cn = counts[lab]
                if near:
                    cn["near"] += 1
                    key = f"{lev}, {route}"
                    cn["by_level_and_route"][key] = cn["by_level_and_route"].get(key, 0) + 1
                    lo_hi = cn["gain_over_p"] or [g, g]
                    cn["gain_over_p"] = [min(lo_hi[0], g), max(lo_hi[1], g)]
                elif g >= 1.04:   # the 4% the line stands for, crossed upward away from 1/2 (10:12, 5)
                    cn["raised_in_the_tails"]["races"] += 1
                    cn["raised_in_the_tails"]["p_at_most"] = max(cn["raised_in_the_tails"]["p_at_most"],
                                                                 c["p"]["value"])
            if any(x[2] for x in per):
                row = [c["id"], lev, c["year"], (c.get("place") or {}).get("state"), route, n, round(mu, 4),
                       round(sd, 5), "own" if "device" not in how else "device", c["p"]["value"]]
                for lab, rate, near, g in per:
                    row += [round(rate * n, 1), round(rate / sd, 4), near, round(g, 4)]
                rows.append(row)
                if per[0][2]:
                    notes[c["id"]] = note_text(n, sd, how, per[0][3])
    for cn in counts.values():
        cn["by_level_and_route"] = dict(sorted(cn["by_level_and_route"].items(), key=lambda kv: (-kv[1], kv[0])))
        if cn["gain_over_p"]:
            cn["gain_over_p"] = [round(x, 3) for x in cn["gain_over_p"]]
    rows.sort(key=lambda r: (r[13], r[0]))
    return rows, notes, counts, seen


def listing(rows, counts, seen):
    cols = ["id", "level", "year", "state", "route", "n", "centre", "sd", "sd_from", "p"]
    for lab, _, _ in RATES:
        cols += [f"zone_votes_{lab}", f"zone_over_spread_{lab}", f"near_{lab}", f"gain_over_p_{lab}"]
    return {
        "about": "the recount zone beside p for every record of D3's levels with p above 0 (brief D3 step 4; model "
                 "section 3; MATH 5.10): each race whose zone, at any of the three rates, is at or above a third of "
                 "the forecast's spread in votes, with the zone, the ratio and MATH 5.10's gain over p at each. p is "
                 "unchanged everywhere (the orchestrator, 2026-11-13 10:12). Built by pipeline/local_recount.py; "
                 "method in data/local/REPORT.md section 38.",
        "rule": {"zone_votes": "rate x n, n the count p is computed at (p.n) [inferred]", "gross": GROSS,
                 "near": "zone at or above a third of n x sd (model section 3: \"At a zone a third the size of the "
                         "spread, p is still 96% of its value\"; the orchestrator, 10:12, 2)",
                 "sd_from": {"own": "route (a): the forecast's own sd (forecasts[0].share.sd)",
                             "device": f"the like-race routes: the normal device of pipeline/local.py _p_like, "
                                       f"\"{DEVICE_LINE}\", centred at 1/2 (a measure's threshold), f = p.f_half "
                                       f"(p.f_t)"},
                 "gain_over_p": "MATH 5.10's smoothed gain over the sharp p, its continuous form; " + check_math(),
                 "notes": "each record near at 0.87% carries a note (the orchestrator, 10:12, 3); the others are "
                          "listed here only"},
        "rates": {lab: {"rate": r, "what": what} for lab, r, what in RATES},
        "sources": SOURCES,
        "records_with_p_above_0": seen,
        "counts": counts,
        "columns": cols,
        "near": rows,
    }


def put_notes(notes, write):
    """Take out every zone note, then add each record's own; with write, rewrite the files that change in the
    builders' layout. Returns the files that would change and how many notes each record set holds."""
    changed, have = [], {}
    for lev, path in files():
        with open(path) as f:
            d = json.load(f)
        cs = d.get("contests", [])
        before = json.dumps(cs, ensure_ascii=False, sort_keys=True)
        for c in cs:
            old = [x for x in (c.get("notes") or []) if x.startswith(NOTE_HEAD)]
            if old:
                have[c["id"]] = old
            keep = [x for x in (c.get("notes") or []) if not x.startswith(NOTE_HEAD)]
            if c.get("id") in notes:
                keep.append(notes[c["id"]])
            if keep:
                c["notes"] = keep
            elif "notes" in c:
                del c["notes"]
        if json.dumps(cs, ensure_ascii=False, sort_keys=True) != before:
            changed.append(os.path.relpath(path, ROOT))
            if write:
                L.write_level_file(path, {k: v for k, v in d.items() if k != "contests"}, cs)
    return changed, have


def check_sources():
    cache = os.environ.get("VOTE_CACHE")
    if not cache:
        return "sources not checked: VOTE_CACHE not set"
    for key, s in SOURCES.items():
        path = os.path.join(cache, s["cache"])
        with open(path, "rb") as f:
            raw = f.read()
        if hashlib.sha256(raw).hexdigest() != s["sha256"] or len(raw) != s["bytes"]:
            raise SystemExit(f"{key}: the cached file is not the one read at {s['read_utc']}")
        if path.endswith(".pdf"):
            text = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, check=True).stdout
            text = text.decode("utf-8", "replace")
        else:
            text = re.sub(r"<[^>]+>", " ", html.unescape(raw.decode("utf-8", "replace")))
        text = re.sub(r"\s+", " ", text)
        for fig in s["figures"]:
            for q in fig["quote"]:
                if re.sub(r"\s+", " ", q) not in text:
                    raise SystemExit(f"{key}: not found in the source: {q!r}")
    return "both sources' sha256 and every quoted figure checked in the cache"


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("build", "check"):
        raise SystemExit(__doc__)
    write = sys.argv[1] == "build"
    print(check_math())
    if not write:
        print(check_sources())
    rows, notes, counts, seen = compute()
    out = listing(rows, counts, seen)
    body = json.dumps(out, indent=1, ensure_ascii=False)
    body = re.sub(r"\[\n\s+([^\[\]{}]*?)\n\s+\]", lambda m: "[" + re.sub(r",\n\s+", ", ", m.group(1)) + "]", body)
    changed, have = put_notes(notes, write)
    if write:
        with open(OUT, "w") as f:
            f.write(body + "\n")
    else:
        with open(OUT) as f:
            if f.read() != body + "\n":
                raise SystemExit("data/local/recount-zone.json differs from a fresh build")
        if changed:
            raise SystemExit(f"{len(changed)} files' zone notes differ from a fresh build, e.g. {changed[:3]}")
    print(f"records with p above 0: {seen}")
    for lab, _, _ in RATES:
        cn = counts[lab]
        print(f"{lab}: near {cn['near']} {cn['by_level_and_route']}; gain/p {cn['gain_over_p']}; raised in the "
              f"tails {cn['raised_in_the_tails']}")
    print(f"notes: {len(notes)}; files {'rewritten' if write else 'to change'}: {len(changed)}")


if __name__ == "__main__":
    main()
