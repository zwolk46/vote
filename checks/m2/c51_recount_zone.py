"""c51: D3's #115 (e3e9b921 -> f6434077), section 21: the recount zone beside p (pipeline/local_recount.py, REPORT §38,
data/local/recount-zone.json), checked with every rule copied and nothing imported from pipeline/.

The orchestrator (2026-11-13 10:34 UTC, verbatim): "D3's #115 is merged as f643407 (REPORT §38, the recount zone). Check
it in section 21, with its end at f643407. It covers pipeline/local_recount.py; the zone at 0.87% gross against n × sd
(like-race spreads from _p_like's normal device); the 1,045 notes near at 0.87%, each line equal to the old one with its
note taken out; and recount-zone.json's 15,122 near at any rate. Check also the counts at 1.06% and 2.49% (2.49% floor
0.627), the 1,838 tail races, and the figures quoted from Ansolabehere and Reeves (VTP WP11, Table 2, p. 5) and FairVote,
against their sha256. No p moves by my compare. D3 next takes Singer's 2020 results in its own PR."

Sources read apart (`fetch_eighth_pass.sh recount`, one request each, 10:35 UTC): Ansolabehere and Reeves's VTP working
paper 11 (vote.caltech.edu) and FairVote's recounts page; neither is kept in the repository. The rules copied from
pipeline/local_recount.py and marked so: the spread (route (a)'s own sd; the like-race routes' device sd = 1/(sqrt(2 pi) f)),
the zone w = rate x n, near = w >= (n sd)/3, the three rates, the note's text; MATH 5.10's gain over p is computed by my
own quadrature (scipy's quad for the table and a sample, a numpy trapezoid over the records), not D3's Simpson rule.

Sections:
  51.1  the records between the commits: what changed (the 1,045 zone notes, 156 files), each equal with its note taken out, no p moved
  51.2  MATH 5.10's gain over p, my own quadrature: MATH's table within 0.002; the listing's gain over p on a sample
  51.3  the zone on every record with p above 0: the counts at 0.87%, 1.06% and 2.49%, the tails, the listing's 15,122 rows, the 1,045 notes
  51.4  the sources read apart: hashes, the quoted figures, the licence words, the model's Minnesota figures

Run: python3 -I checks/m2/c51_recount_zone.py [1 2 3 4]
"""
import collections
import glob
import hashlib
import html as _html
import json
import math
import os
import re
import statistics
import subprocess
import sys

import numpy as np
from scipy.integrate import quad

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402
import c41_governor_refit as C41  # noqa: E402
import c48_district_checks_3 as C48  # noqa: E402
import c49_va_local_2 as C49  # noqa: E402

BEFORE, AFTER = "e3e9b921", "f6434077"
LEVELS = ("state-lower", "state-upper", "local", "primary", "measure")   # pipeline/local_recount.py LEVELS, copied
NEAR = 1.0 / 3.0   # model section 3: "a zone a third the size of the spread" (local_recount.py NEAR, copied)
NOTE_HEAD = "Recount zone [inferred]:"
RATES = (("0.87%", 0.0087), ("1.06%", 0.0106), ("2.49%", 0.0249))   # local_recount.py RATES, copied
SRC = os.path.join(L.CACHE, "eighth", "src", "recount")
# the sources as data/local/recount-zone.json `sources` states them [stated]: file, url, bytes, sha256, the quoted words
SOURCES = {
    "ansolabehere_reeves": ("vtp_wp11.pdf", 134241, "2b62faced09db789732ecdf23e2c64060929c0017692f298338499b4ac551dcf",
                            ["In the general elections in this span, 108 races had recounts",
                             "The majority of the recounts (69) occurred in races for state representative",
                             "Our analysis consists of 415 cases", "approximately 0.83 percentage point with a 95%", "from 0.61 to 1.05",
                             "Hand-Counted 92 2.49 (1.44, 3.55) 21.88", "Hand-Counted 79 0.87 (0.69, 1.06) 4.08", "(without Bradford)",
                             "Machine Counted 217 0.56 (0.42, 0.70) 8.27",
                             "The results for hand-counted paper, excluding Bradford, are nearly identical to the", "We take this as the baseline",
                             # REPORT §38's p. 8 words, quoted there but not in the file's `figures`
                             "In a US House election with 250,000 votes",
                             "any race decided by less than .5 percent of the vote will have a non-trivial probability of being reversed in a recount"]),
    "fairvote": ("fairvote-election-recounts-2024.html", 215078, "2b5dbfcfcccae32ce17da518a795b7d1c5b273696caca85716421bd1c15be7bc",
                 ["The recount shifted the margin by 390 votes", "by 239 votes, a change of 0.11 percentage points",
                  "The recount delivered a 440-vote swing to Franken", "2,746,593"]),
}
LICENCE_WORDS = ("licen", "copyright", "©", "all rights", "creative commons")
# MATH 5.10's table (model/MATH.md 5.10; local_recount.py MATH_5_10): (mu, w votes) -> gain over p at n = 100,000, sd 0.03
MATH_5_10 = {(0.50, 10): 1.000, (0.50, 100): 1.000, (0.50, 1000): 0.958, (0.50, 3000): 0.760, (0.50, 10000): 0.347,
             (0.52, 10): 1.000, (0.52, 100): 1.000, (0.52, 1000): 0.975, (0.52, 3000): 0.830, (0.52, 10000): 0.420}
# the note's fixed words (local_recount.py GROSS, DEVICE_LINE, note_text), copied so that my text can be set against the record's
GROSS = ("\"The paper measures a candidate's change within one town, as a share of that candidate's votes, and you "
         "apply it to a race's whole count. Changes may add or cancel across towns and candidates, so the zone you "
         "build is a gross figure, as §3 treats Minnesota's 2,170.\" (the orchestrator, 2026-11-13 10:06)")
DEVICE_LINE = "sd = 1.0 / (math.sqrt(2 * math.pi) * f)"

h1 = C48.h1
at, records_at, pval, sha256 = C49.at, C49.records_at, C49.pval, C49.sha256


def note_text(n, sd, how, g):   # local_recount.py note_text, copied
    w = RATES[0][1] * n
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


def spread(c):   # local_recount.py spread, copied: (route, centre, sd, where the sd is from, the point p is taken at)
    p = c.get("p")
    if not isinstance(p, dict) or not p.get("value") or not p.get("n"):
        return None
    fc = (c.get("forecasts") or [{}])[0]
    sh = fc.get("share") or {}
    if sh.get("sd"):
        return fc.get("route"), sh["mean"], sh["sd"], "the forecast's own sd", 0.5
    if p.get("f_half"):
        return fc.get("route"), 0.5, 1.0 / (math.sqrt(2 * math.pi) * p["f_half"]), "the normal device of pipeline/local.py _p_like", 0.5
    if p.get("f_t"):
        t = p.get("threshold", 0.5)
        return fc.get("route"), t, 1.0 / (math.sqrt(2 * math.pi) * p["f_t"]), "the normal device of pipeline/local.py _p_like, at the threshold", t
    return None


# ------------------------------------------------------------------------------------------ MATH 5.10's gain over p, my own

def npdf(x, m, s):
    return np.exp(-0.5 * ((x - m) / s) ** 2) / (s * math.sqrt(2 * math.pi))


def lpdf(u, b):
    e = np.exp(-np.abs(u) / b)
    return e / (b * (1 + e) ** 2)


def gain_quad(mu, sd, rate, at_=0.5):
    """MATH 5.10's smoothed gain over the sharp p: the forecast's normal density of the share, averaged over a logistic of
    scale rate/2 in the share and centred at the point p is taken at, over the density there; scipy's adaptive quadrature."""
    b = rate / 2.0
    val, _ = quad(lambda u: float(lpdf(u, b) * npdf(at_ + u, mu, sd)), -60 * b, 60 * b, limit=400, points=[0.0])
    return val / float(npdf(at_, mu, sd))


_U = np.linspace(-1.0, 1.0, 8001)


def gain_trap(mu, sd, rate, at_=0.5):
    """The same by a trapezoid over +-50 scales on 8,001 points (a different rule and grid from D3's Simpson over +-40 on 401)."""
    b = rate / 2.0
    u = _U * 50 * b
    y = lpdf(u, b) * npdf(at_ + u, mu, sd)
    return float(np.trapezoid(y, u) / npdf(at_, mu, sd))


# ------------------------------------------------------------------------------------------ 51.1 the records

def d3_files(commit):
    root = at(commit, "")
    out = []
    for lev in LEVELS:
        for path in sorted(glob.glob(os.path.join(root, "data", lev, "*", "*.json"))):
            out.append(os.path.relpath(path, root))
    return out


def strip_note(c):
    cc = dict(c)
    keep = [x for x in (c.get("notes") or []) if not x.startswith(NOTE_HEAD)]
    if keep:
        cc["notes"] = keep
    else:
        cc.pop("notes", None)
    return cc


def section_1():
    h1(f"51.1 The records between the commits, {BEFORE} -> {AFTER}: what changed, each line against the old one with its note taken out, p")
    files = subprocess.run(["git", "diff", "--name-only", BEFORE, AFTER], capture_output=True, text=True, cwd=L.ROOT).stdout.split()
    data_files = [f for f in files if re.match(r"^data/(local|primary|measure|state-lower|state-upper)/\d{4}/[A-Z]{2}\.json$", f)]
    d2_files = [f for f in files if re.match(r"^data/(governor|house|senate|president)/", f)]
    other = [f for f in files if f not in data_files and f not in d2_files]
    print(f"  files changed: {len(files)}: D3's record files {len(data_files)} {dict(collections.Counter(f.split('/')[1] for f in data_files))} (D3: 156); D2's {d2_files} (none); other: {other}")
    tal = collections.Counter()
    noted, pmoved, ex = {}, [], []
    for f in d3_files(AFTER):
        b, a = records_at(BEFORE, f), records_at(AFTER, f)
        if set(b) != set(a):
            tal["ids differ"] += 1
            ex.append((f, sorted(set(b) ^ set(a))[:3]))
        for i, ra in a.items():
            rb = b.get(i)
            if rb is None:
                continue
            zn = [x for x in ra.get("notes") or [] if x.startswith(NOTE_HEAD)]
            if (pval(rb) is None) != (pval(ra) is None) or (pval(rb) is not None and pval(rb) != pval(ra)):
                pmoved.append(i)
            if zn:
                noted[i] = (f, zn, ra)
                tal[("zone notes in the record", len(zn))] += 1
                tal["equal with the note taken out" if strip_note(ra) == rb else "DIFFERS beyond the note"] += 1
                if strip_note(ra) != rb and len(ex) < 5:
                    ex.append((i, sorted(k for k in set(ra) | set(rb) if ra.get(k) != rb.get(k))))
            elif ra != rb:
                tal["changed without a zone note"] += 1
                if len(ex) < 5:
                    ex.append((i, sorted(k for k in set(ra) | set(rb) if ra.get(k) != rb.get(k))))
            else:
                tal["unchanged"] += 1
        if any(x.startswith(NOTE_HEAD) for r_ in b.values() for x in r_.get("notes") or []):
            tal["files with a zone note BEFORE"] += 1
    print(f"  records: {dict(tal)}; e.g. {ex[:5]}")
    print(f"  records with a zone note: {len(noted):,} (D3: 1,045) by level {dict(collections.Counter(v[0].split('/')[1] for v in noted.values()))}; files holding one: {len({v[0] for v in noted.values()})} (D3: 156)")
    print(f"  p moved (value before != after, or one side None): {len(pmoved)} {pmoved[:5]} (the orchestrator: no p moves)")
    return noted


# ------------------------------------------------------------------------------------------ 51.2 MATH 5.10

def section_2():
    h1("51.2 MATH 5.10's gain over p by my own quadrature: MATH's table (n 100,000, sd 0.03), and the listing's gain over p on a sample")
    worst = 0.0
    out = []
    for (mu, w), want in sorted(MATH_5_10.items()):
        g1 = gain_quad(mu, 0.03, w / 100000.0)
        g2 = gain_trap(mu, 0.03, w / 100000.0)
        worst = max(worst, abs(g1 - want), abs(g2 - want))
        out.append(f"mu {mu} w {w:,}: quad {g1:.4f}, trapezoid {g2:.4f}, MATH {want}")
    print("  " + "; ".join(out))
    print(f"  the largest difference from MATH 5.10's table: {worst:.4f} (D3's check: within 0.002)")
    lst = L.load_json(at(AFTER, "data/local/recount-zone.json"))
    cols = {c: i for i, c in enumerate(lst["columns"])}
    rows = lst["near"]
    sample = rows[::97]
    diffs = collections.Counter()
    worst = (0.0, None)
    for r in sample:
        mu, sd, at_ = r[cols["centre"]], r[cols["sd"]], 0.5
        for lab, rate in RATES:
            g = gain_quad(mu, sd, rate, at_)
            d = abs(g - r[cols[f"gain_over_p_{lab}"]])
            diffs["within 1e-3" if d <= 1e-3 else "within 1e-2" if d <= 1e-2 else "beyond 1e-2"] += 1
            if d > worst[0]:
                worst = (d, (r[0], lab, g, r[cols[f"gain_over_p_{lab}"]]))
    print(f"  the listing's gain over p on every 97th row ({len(sample)} rows x 3 rates; the row's rounded centre and sd, at 1/2) against scipy's quad: {dict(diffs)}; worst {worst}")
    print("  (the listing rounds the centre to 4 and the sd to 5 decimals, so a difference of a few 1e-4 is the rounding; section 3 uses each record's own inputs)")


# ------------------------------------------------------------------------------------------ 51.3 the zone on every record

def scan(commit):
    """Every record of D3's levels with p above 0 at the commit: (id, lev, year, state, route, n, mu, sd, how, at, p, class, f) [measured]."""
    out = []
    for f in d3_files(commit):
        lev = f.split("/")[1]
        for i, c in records_at(commit, f).items():
            s = spread(c)
            if s is None:
                continue
            route, mu, sd, how, at_ = s
            fc = (c.get("forecasts") or [{}])[0]
            out.append((i, lev, c.get("year"), (c.get("place") or {}).get("state"), route, c["p"]["n"], mu, sd, how, at_, c["p"]["value"],
                        fc.get("class"), c["p"].get("f_half") or c["p"].get("f_t"), [x for x in c.get("notes") or [] if x.startswith(NOTE_HEAD)]))
    return out


def section_3():
    h1("51.3 The zone on every record with p above 0 (the spread, the zone and the near line copied; gain over p by my own trapezoid): the counts, the tails, the listing, the 1,045 notes")
    recs = scan(AFTER)
    print(f"  records with p above 0 and a spread: {len(recs):,} (the listing's records_with_p_above_0: {L.load_json(at(AFTER, 'data/local/recount-zone.json'))['records_with_p_above_0']:,}); by level {dict(collections.Counter(r[1] for r in recs))}; "
          f"sd from {dict(collections.Counter('own' if 'device' not in r[8] else 'device' for r in recs))}")
    cache = {}
    counts = {lab: {"near": 0, "by": collections.Counter(), "g": [], "tails": 0, "tails_p": 0.0, "tails_ids": []} for lab, _ in RATES}
    mine = {}
    for (i, lev, yr, st, route, n, mu, sd, how, at_, p, cls, f, zn) in recs:
        per = []
        for lab, rate in RATES:
            k = (round(mu, 6), round(sd, 6), rate, at_)   # D3's cache key, copied, so that the same inputs give one g
            if k not in cache:
                cache[k] = gain_trap(mu, sd, rate, at_)
            g = cache[k]
            near = rate * n >= NEAR * n * sd
            per.append((lab, rate, near, g))
            cn = counts[lab]
            if near:
                cn["near"] += 1
                cn["by"][f"{lev}, {route}"] += 1
                cn["g"].append(g)
            elif g >= 1.04:
                cn["tails"] += 1
                if p > cn["tails_p"]:
                    cn["tails_p"], cn["tails_ids"] = p, [i]
        if any(x[2] for x in per):
            mine[i] = (lev, yr, st, route, n, mu, sd, how, at_, p, cls, f, zn, per)
    lst = L.load_json(at(AFTER, "data/local/recount-zone.json"))
    for lab, _ in RATES:
        cn, theirs = counts[lab], lst["counts"][lab]
        print(f"  {lab}: near {cn['near']:,} (the listing: {theirs['near']:,}); by level and route mine {dict(cn['by'])} = the listing's: {dict(cn['by']) == theirs['by_level_and_route']}; "
              f"gain over p of those near {min(cn['g']):.3f} to {max(cn['g']):.3f} (the listing: {theirs['gain_over_p']}); raised in the tails (not near, gain over p 1.04 or more) {cn['tails']:,} "
              f"with p at most {cn['tails_p']:.4g} {cn['tails_ids']} (the listing: {theirs['raised_in_the_tails']})")
    cols = {c: j for j, c in enumerate(lst["columns"])}
    rows = {r[0]: r for r in lst["near"]}
    print(f"\n  the listing's rows: {len(rows):,} ids (D3: 15,122); mine near at any rate: {len(mine):,}; in both: {len(set(rows) & set(mine)):,}; the listing's only: {sorted(set(rows) - set(mine))[:5]}; mine only: {sorted(set(mine) - set(rows))[:5]}")
    tal = collections.Counter()
    worst = []
    for i, (lev, yr, st, route, n, mu, sd, how, at_, p, cls, f, zn, per) in mine.items():
        r = rows.get(i)
        if r is None:
            continue
        ok = (r[cols["level"]] == lev and r[cols["route"]] == route and r[cols["n"]] == n and abs(r[cols["centre"]] - mu) <= 5e-5 and abs(r[cols["sd"]] - sd) <= 5e-6
              and r[cols["sd_from"]] == ("own" if "device" not in how else "device") and r[cols["p"]] == p)
        tal["id, level, route, n, centre, sd, sd_from, p equal" if ok else "a field differs"] += 1
        for lab, rate, near, g in per:
            z_ok = abs(r[cols[f"zone_votes_{lab}"]] - round(rate * n, 1)) <= 0.051
            q_ok = abs(r[cols[f"zone_over_spread_{lab}"]] - round(rate / sd, 4)) <= 5.1e-5
            n_ok = r[cols[f"near_{lab}"]] == near
            dg = abs(r[cols[f"gain_over_p_{lab}"]] - g)
            tal[(lab, "zone, ratio, near equal" if z_ok and q_ok and n_ok else "zone/ratio/near DIFFER", "gain within 1e-3" if dg <= 1e-3 else "gain within 1e-2" if dg <= 1e-2 else "gain beyond 1e-2")] += 1
            if dg > 1e-3 or not (z_ok and q_ok and n_ok):
                worst.append((dg, i, lab, g, r[cols[f"gain_over_p_{lab}"]], near, r[cols[f"near_{lab}"]]))
    print("  the listing's 15,122 rows against mine, field by field: " + "; ".join(f"{k}: {v:,}" for k, v in sorted(tal.items(), key=str)))
    worst.sort(reverse=True)
    for w in worst[:5]:
        print(f"    {w}")
    # the notes
    near87 = {i: v for i, v in mine.items() if v[13][0][2]}
    noted = {i: v for i, v in mine.items() if v[12]}
    print(f"\n  near at 0.87%, mine: {len(near87):,} (D3: 1,045); records carrying a zone note: {len(noted):,}; the two sets equal: {set(near87) == set(noted)}")
    eq = collections.Counter()
    ex = []
    for i, (lev, yr, st, route, n, mu, sd, how, at_, p, cls, f, zn, per) in near87.items():
        g = per[0][3]
        mine_note = note_text(n, sd, how, g)
        if zn and zn[0] == mine_note:
            eq["my note = the record's, word for word"] += 1
        elif zn and re.sub(r"then \d\.\d{3} of", "then G of", zn[0]) == re.sub(r"then \d\.\d{3} of", "then G of", mine_note):
            eq["equal but for gain's third decimal"] += 1
            if len(ex) < 3:
                ex.append((i, re.search(r"then (\d\.\d{3}) of", zn[0]).group(1), f"{g:.4f}"))
        else:
            eq["DIFFERS"] += 1
            if len(ex) < 3:
                ex.append((i, (zn[0] if zn else None)[:200], mine_note[:200]))
    print(f"  my note text (D3's note_text copied, my gain over p) against the record's: {dict(eq)}; e.g. {ex}")
    # the classes, the f range, the states, n, the tiny zones, the floor and the top
    byc = collections.defaultdict(list)
    for i, v in near87.items():
        byc[(v[0], v[3], v[10])].append(v)
    for (lev, route, cls), vs in sorted(byc.items(), key=lambda kv: -len(kv[1])):
        fs = [v[11] for v in vs if v[11]]
        sds = [v[6] for v in vs]
        sts = collections.Counter(f"{v[2]} {v[1]}" if lev == "local" else v[2] for v in vs)
        print(f"    {lev} {route} '{cls}': {len(vs)}; f {min(fs):.2f} to {max(fs):.2f} (sd {min(sds):.4f} to {max(sds):.4f}); years {min(v[1] for v in vs)}-{max(v[1] for v in vs)}; "
              f"by state{' and year' if lev == 'local' else ''}: {dict(sts.most_common(8))}... ({len(sts)} keys)")
    ns = sorted(v[4] for v in near87.values())
    tiny = sorted((round(RATES[0][1] * v[4], 2), i) for i, v in near87.items() if RATES[0][1] * v[4] < 2)
    print(f"  n of the near races: {ns[0]:,} to {ns[-1]:,}, median {statistics.median(ns):,.0f} (D3: 3 to 279,070, median 5,771); zone at 0.87% under 2 votes: {len(tiny)}, "
          f"under 1.95 (the listing's tenth rounds below 2): {sum(1 for w, i in tiny if w < 1.95)}, under 1.5 (the note's whole vote reads 1 or 0): {sum(1 for w, i in tiny if w < 1.5)} (D3: 46 'under 2 votes'); the largest of them {tiny[-3:]}")
    g249 = sorted((v[13][2][3], i, v[9]) for i, v in mine.items() if v[13][2][2])
    print(f"  at 2.49%: the floor {g249[0]} (D3: 0.627, Alaska's 1978 House 20); the top {g249[-1]} (D3: 4.263, New York's 2020 House 55, p 3.5e-11)")
    return mine


# ------------------------------------------------------------------------------------------ 51.4 the sources

def section_4():
    h1("51.4 The sources read apart (fetch_eighth_pass.sh recount, one request each): hashes, the quoted figures, the licence words, the model's Minnesota figures")
    for key, (fname, nbytes, sha, quotes) in SOURCES.items():
        path = os.path.join(SRC, fname)
        raw = open(path, "rb").read()
        mine = hashlib.sha256(raw).hexdigest()
        print(f"  {key}: my copy {len(raw):,} bytes, sha256 {mine[:12]}... {'EQUAL to' if mine == sha and len(raw) == nbytes else 'DIFFERS from'} the listing's ({nbytes:,} bytes, {sha[:12]}...)")
        if path.endswith(".pdf"):
            info = subprocess.run(["pdfinfo", path], capture_output=True, text=True).stdout
            pages = re.search(r"Pages:\s+(\d+)", info)
            text = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout
            print(f"    pdfinfo pages: {pages.group(1) if pages else None} (D3: a 10-page PDF); title line: {[l.strip() for l in text.splitlines() if l.strip()][:2]}")
        else:
            text = re.sub(r"<[^>]+>", " ", _html.unescape(raw.decode("utf-8", "replace")))
            print(f"    the page: 'nonce' attributes {raw.decode('utf-8', 'replace').lower().count('nonce')} (a value set per request [inferred]), 'flourish' {raw.decode('utf-8', 'replace').lower().count('flourish')}, title {re.search(r'<title>(.*?)</title>', raw.decode('utf-8', 'replace'), re.S).group(1).strip()[:80]!r}")
        t1 = re.sub(r"\s+", " ", text)
        found = [q for q in quotes if re.sub(r"\s+", " ", q) in t1]
        print(f"    quoted words found: {len(found)} of {len(quotes)}; missing: {[q for q in quotes if q not in found]}")
        lic = {w: len(re.findall(re.escape(w), t1, re.I)) for w in LICENCE_WORDS}
        print(f"    licence words in the text: {lic} (D3: none printed)")
        if key == "ansolabehere_reeves":
            m = re.search(r"Table 2.{0,400}", t1)
            print(f"    Table 2's words: {m.group(0)[:420] if m else None}")
            for q in ("108 races", "(69)", "415 cases", "0.83 percentage", "0.61 to 1.05"):
                print(f"      '{q}' on PDF page(s) {[k + 1 for k, pg in enumerate(text.split(chr(12))) if q in re.sub(r'\s+', ' ', pg)]}")
        else:
            for q in ("390 votes", "239 votes", "440-vote", "551", "0.03%"):
                m = re.search(r".{0,80}" + re.escape(q) + r".{0,80}", t1)
                print(f"      '{q}': {m.group(0) if m else None}")
    for f in ("model/MODEL-DRAFT-3.md", "model/MATH.md"):
        p = os.path.join(L.ROOT, f)
        if os.path.exists(p):
            t = open(p).read()
            for q in ("2,170", "264", "48,000 to 73,000", "a third the size of the spread", "96% of its value"):
                ls = [k + 1 for k, line in enumerate(t.splitlines()) if q in line]
                print(f"  {f}: '{q}' on lines {ls[:6]}")


def main():
    print(f"C51 (section 21): D3's #115, {BEFORE} -> {AFTER}; {L.git_head()}")
    section_1()
    section_2()
    section_3()
    section_4()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(f"C51 (section 21): D3's #115, {BEFORE} -> {AFTER}; {L.git_head()}")
        for a in sys.argv[1:]:
            globals()[f"section_{a}"]()
    else:
        main()
