"""pipeline/intake/state_law.py: every state's tie and recount law, read at the state's own code.

Written 2026-11-07 by worker D4 (briefs/D4-data-cost-and-ties.md). Statutes are not a standardized dataset,
so this script does what an intake script can do for them: it fetches each cited section once into the
cache, turns it into text, and CHECKS that every quotation recorded in the reading appears word for word
in that text. A reading is the curated file `data/law/src/<ST>.json`; `build` turns the fifty-one of them
into `data/law/ties.json` and `data/law/recounts.json`, refusing any reading whose quotation is not found.

  python3 pipeline/intake/state_law.py fetch  ST NAME URL    fetch one section into the cache and print
                                                             how much text came back (a reader's tool)
  python3 pipeline/intake/state_law.py check  [ST ...]       fetch every section of the readings and verify
                                                             every quotation; print what fails; write nothing
  python3 pipeline/intake/state_law.py build  [--allow-failures]
                                                             check, then write data/law/ties.json and
                                                             recounts.json (every quotation verified, or the
                                                             rule is marked unverified and listed)
  python3 pipeline/intake/state_law.py tables                print the counts and tables of data/law/REPORT.md,
                                                             computed from the two built files (nothing typed)

Rules kept here, with their reasons (briefs/_COMMON.md 6, 13, 15):
  - Downloads go through pipeline/fetch.py (curl's own user agent, no contact detail, a stop at the first
    refusal, a stop at a redirect to another site). *Reason:* a source that blocks us is lost; getting round
    a site's refusal is not ours to do.
  - At least FOUR seconds between two requests to one host, even across separate runs of this script, kept
    in a small file per host in the cache. *Reason:* pipeline/fetch.py keeps the interval only inside one
    process, and several readers run this script at once (_COMMON 13).
  - A refusal, an error page or a page that holds no text (a script shell) is reported and recorded as
    unread. It is never tried another way. *Reason:* _COMMON 6.
  - A quotation is verified after only these changes to both sides: Unicode compatibility form, curly
    quotation marks and long dashes made plain, runs of white space made one space. `[...]` marks a cut:
    each part must appear, in order. *Reason:* a recorded quotation is the statute's own words or it is not
    a quotation (law 8: a summary of a law is not the law).
The cache is $VOTE_CACHE/law/<ST>/, or ~/.cache/vote-intake/law/<ST>/.
"""
import datetime
import glob
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import unicodedata
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, os.pardir, os.pardir))
sys.path.insert(0, os.path.dirname(HERE))
import fetch as _fetch  # noqa: E402  (pipeline/fetch.py: the one implementation of a download)

CACHE = _fetch.CACHE
LAW_DIR = os.path.join(REPO, "data", "law")
SRC_DIR = os.path.join(LAW_DIR, "src")
MIN_INTERVAL_S = 4.0

TIE_KINDS = ["federal", "presidential-electors", "statewide", "state-legislative", "local", "primary", "measure"]
TIE_RESOLUTIONS = ["lot", "new-election", "legislature", "runoff", "recount-then-lot", "recount-then-new-election",
                   "party-committee", "court", "other", "none-found", "unread"]
RECOUNT_TYPES = ["automatic", "requested", "court", "other"]


def now_utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")


# ---------------------------------------------------------------- fetching and text

def _throttle(host):
    """Wait until MIN_INTERVAL_S has passed since the last request to this host by ANY run of this script."""
    d = os.path.join(CACHE, "law", ".last")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, re.sub(r"[^A-Za-z0-9.-]", "_", host))
    for _ in range(40):
        try:
            last = os.path.getmtime(p)
        except OSError:
            last = 0.0
        wait = MIN_INTERVAL_S - (time.time() - last)
        if wait <= 0:
            break
        time.sleep(wait + 0.05)
    with open(p, "w") as f:
        f.write(str(time.time()))
    os.utime(p, None)


def raw_name(st, name):
    return f"law/{st}/{name}.raw"


def text_path(st, name):
    return os.path.join(CACHE, "law", st, name + ".txt")


def html_to_text(data):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(data, "lxml")
    for t in soup(["script", "style", "noscript", "template"]):
        t.decompose()
    return soup.get_text("\n")


def extract_text(raw_path):
    with open(raw_path, "rb") as f:
        head = f.read(8)
    if head.startswith(b"%PDF"):
        out = subprocess.run(["pdftotext", "-layout", raw_path, "-"], capture_output=True)
        if out.returncode != 0:
            raise RuntimeError("pdftotext failed: " + out.stderr.decode("utf-8", "replace")[:200])
        return out.stdout.decode("utf-8", "replace")
    if head.startswith(b"PK"):
        raise RuntimeError("a zip or an Office file; read it by hand")
    with open(raw_path, "rb") as f:
        data = f.read()
    return html_to_text(data.decode("utf-8", "replace"))


def fetch_section(st, name, url, refresh=False):
    """Fetch one section's page into the cache; return (meta, text). Raises fetch.Refused on a refusal and
    ValueError if the page holds almost no text (a script shell or an error page served with status 200)."""
    rel = raw_name(st, name)
    os.makedirs(os.path.dirname(os.path.join(CACHE, rel)), exist_ok=True)
    full = os.path.join(CACHE, rel)
    if refresh or not (os.path.exists(full) and os.path.exists(full + ".meta.json")):
        _throttle(urllib.parse.urlparse(url).netloc)
        _fetch.fetch(url, rel, refresh=refresh)
    meta = _fetch.meta(rel)
    tp = text_path(st, name)
    if refresh or not os.path.exists(tp) or os.path.getmtime(tp) < os.path.getmtime(full):
        txt = extract_text(full)
        with open(tp, "w", encoding="utf-8") as f:
            f.write(txt)
    with open(tp, encoding="utf-8") as f:
        txt = f.read()
    if len(norm(txt)) < 300:
        raise ValueError(f"{url}: only {len(norm(txt))} characters of text (a script shell or an empty page)")
    return meta, txt


# ---------------------------------------------------------------- quotations

_PLAIN = {"‘": "'", "’": "'", "‚": "'", "‛": "'", "“": '"', "”": '"', "„": '"',
          "–": "-", "—": "-", "−": "-", "‐": "-", "‑": "-", " ": " ", "­": ""}


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = "".join(_PLAIN.get(c, c) for c in s)
    return re.sub(r"\s+", " ", s).strip()


def quote_found(quote, text):
    """True if every part of the quotation (cut at [...]) appears in the text, in order."""
    t = norm(text)
    pos = 0
    parts = [p for p in re.split(r"\[\.\.\.\]|…", quote) if norm(p)]
    if not parts:
        return False
    for p in parts:
        i = t.find(norm(p), pos)
        if i < 0:
            return False
        pos = i + len(norm(p))
    return True


# ---------------------------------------------------------------- readings

def load_readings(states=None):
    out = {}
    for p in sorted(glob.glob(os.path.join(SRC_DIR, "*.json"))):
        st = os.path.basename(p)[:-5]
        if states and st not in states:
            continue
        with open(p, encoding="utf-8") as f:
            out[st] = json.load(f)
    return out


def check_reading(st, r, refresh=False):
    """Fetch the reading's sections and verify its quotations. Returns (problems, section_meta, bad_rules),
    bad_rules being the set of (kind, index) of the rules with a quotation that could not be verified."""
    problems = []
    bad_rules = set()
    metas = {}
    texts = {}
    for key, sec in (r.get("sections") or {}).items():
        try:
            metas[key], texts[key] = fetch_section(st, key, sec["url"], refresh=refresh)
        except (_fetch.Refused, ValueError, RuntimeError) as e:
            problems.append(f"{st}: section {key} not readable: {e}")
    for kind in ("ties", "recounts"):
        for i, rule in enumerate(r.get(kind) or []):
            res = rule.get("resolution")
            srcs = rule.get("sources") or []
            if not srcs and res not in ("none-found", "unread") and kind == "ties":
                problems.append(f"{st}: {kind}[{i}] has no sources")
            if not srcs and kind == "recounts" and rule.get("type") != "other":
                problems.append(f"{st}: {kind}[{i}] has no sources")
            for s in srcs:
                k = s.get("section")
                if k not in (r.get("sections") or {}):
                    problems.append(f"{st}: {kind}[{i}] cites section {k!r} that is not in sections")
                    bad_rules.add((kind, i))
                    continue
                if k not in texts:
                    problems.append(f"{st}: {kind}[{i}] quote cannot be checked: section {k} unread")
                    bad_rules.add((kind, i))
                    continue
                q = s.get("quote") or ""
                if len(norm(q)) < 20:
                    problems.append(f"{st}: {kind}[{i}] {k}: no quotation (or under 20 characters)")
                    bad_rules.add((kind, i))
                elif not quote_found(q, texts[k]):
                    problems.append(f"{st}: {kind}[{i}] {k}: quotation NOT FOUND in the text: {q[:90]!r}")
                    bad_rules.add((kind, i))
            if kind == "ties":
                for kd in rule.get("kinds", []):
                    if kd not in TIE_KINDS:
                        problems.append(f"{st}: ties[{i}] kind {kd!r} not in {TIE_KINDS}")
                if res not in TIE_RESOLUTIONS:
                    problems.append(f"{st}: ties[{i}] resolution {res!r} not in {TIE_RESOLUTIONS}")
            else:
                for kd in rule.get("kinds", []):
                    if kd not in TIE_KINDS:
                        problems.append(f"{st}: recounts[{i}] kind {kd!r} not in {TIE_KINDS}")
                if rule.get("type") not in RECOUNT_TYPES:
                    problems.append(f"{st}: recounts[{i}] type {rule.get('type')!r} not in {RECOUNT_TYPES}")
    return problems, metas, bad_rules


def source_block(st, r, key, meta):
    """The source block of plan section 3 for one fetched section. A section read at a compilation (Justia,
    Cornell LII) carries `via`, the state code's own citation and url as `origin`, and the code year the
    compilation shows: the orchestrator's ruling of 2026-11-07 07:21 allows it where the state's own site
    refuses or serves only a script shell, flagged as second-hand (law 8)."""
    sec = r["sections"][key]
    at_state = sec.get("read_at", "state") == "state"
    code = r.get("code", {})
    block = {"name": f"{code.get('name', st + ' code')}, {sec.get('citation', key)}"
                     + (f" ({code['edition']})" if at_state and code.get("edition") else ""),
             "url": sec["url"], "read_utc": meta["read_utc"],
             "licence": sec.get("licence") or "state statute; no licence or terms read on the page",
             "mark": "measured" if at_state else "stated",
             "via": None if at_state else sec.get("read_at"),
             "note": sec.get("note"), "sha256": meta["sha256"]}
    if not at_state:
        block["origin"] = {"citation": sec.get("origin_citation"), "url": sec.get("origin_url")}
        block["code_year"] = sec.get("code_year")
    return block


def build(allow_failures=False):
    readings = load_readings()
    all_problems = []
    ties = {}
    recounts = {}
    for st, r in readings.items():
        problems, metas, bad_rules = check_reading(st, r)
        all_problems += problems
        head = {"name": r.get("name"), "status": r.get("status"), "code": r.get("code"),
                "unread": r.get("unread") or [], "notes": r.get("notes") or []}

        def with_sources(rule, kind, i):
            rule = dict(rule)
            blocks = {}
            for s in rule.get("sources") or []:
                k = s["section"]
                if k in metas and k in (r.get("sections") or {}):
                    blocks[k] = source_block(st, r, k, metas[k])
            rule["source_blocks"] = blocks
            rule["quotations_verified"] = bool(rule.get("sources")) and (kind, i) not in bad_rules
            return rule

        if r.get("held"):
            # A reading made by a route that may be a way round a host's refusal is kept in data/law/src/ but not
            # published as a rule until the orchestrator rules (briefs/_COMMON.md 6 and 13): the state shows as held.
            head = dict(head, status="held", held=r["held"],
                        held_rules={"ties": len(r.get("ties") or []), "recounts": len(r.get("recounts") or [])})
            ties[st] = dict(head, rules=[])
            recounts[st] = dict(head, rules=[])
        else:
            ties[st] = dict(head, rules=[with_sources(x, "ties", i) for i, x in enumerate(r.get("ties") or [])])
            recounts[st] = dict(head, rules=[with_sources(x, "recounts", i) for i, x in enumerate(r.get("recounts") or [])])
        ties[st]["sections"] = r.get("sections")
        recounts[st]["sections"] = r.get("sections")
    if all_problems:
        print("\n".join(all_problems))
        if not allow_failures:
            print(f"\n{len(all_problems)} problem(s); nothing written. Fix the readings, or run with --allow-failures.")
            return 1
    stamp = now_utc()
    about_t = ("Every state's and the District of Columbia's rule for a tied election, by kind of office, each read "
              "at the state's own code (or marked otherwise). A rule's quotation was verified word for word against "
              "the fetched text by pipeline/intake/state_law.py. Written " + stamp + ".")
    about_r = about_t.replace("rule for a tied election", "recount rules (automatic and requested)")
    for fn, obj, about in (("ties.json", ties, about_t), ("recounts.json", recounts, about_r)):
        with open(os.path.join(LAW_DIR, fn), "w", encoding="utf-8") as f:
            json.dump({"about": about, "written_utc": stamp, "tie_kinds": TIE_KINDS,
                       "tie_resolutions": TIE_RESOLUTIONS, "states": obj}, f, indent=1, ensure_ascii=False)
            f.write("\n")
    print(f"wrote data/law/ties.json and recounts.json for {len(readings)} readings; {len(all_problems)} problem(s)")
    return 0 if not all_problems else 2

LOT = {"lot", "recount-then-lot"}
ABBR = {"lot": "lot", "new-election": "new election", "legislature": "legislature", "runoff": "runoff",
        "recount-then-lot": "recount, then lot", "recount-then-new-election": "recount, then new election",
        "party-committee": "party committee", "court": "court", "other": "other", "none-found": "none found",
        "unread": "unread"}


def _load_built():
    with open(os.path.join(LAW_DIR, "ties.json"), encoding="utf-8") as f:
        t = json.load(f)
    with open(os.path.join(LAW_DIR, "recounts.json"), encoding="utf-8") as f:
        r = json.load(f)
    return t["states"], r["states"]


def _has_quote(rule):
    return any(s.get("quote") for s in rule.get("sources", []))


def tables():
    """Print, as markdown, every count and table in data/law/REPORT.md, computed from the built files."""
    ts, rs = _load_built()
    out = []
    p = out.append
    st_counts = {}
    for s in ts.values():
        st_counts[s["status"]] = st_counts.get(s["status"], 0) + 1
    p("STATUS " + ", ".join(f"{k} {v}" for k, v in sorted(st_counts.items())))
    p(f"RULES {sum(len(s['rules']) for s in ts.values())} tie, {sum(len(s['rules']) for s in rs.values())} recount")
    for name, d in (("tie", ts), ("recount", rs)):
        c = {}
        for s in d.values():
            for x in s["rules"]:
                k = (x.get("mark") or "none", "quoted" if _has_quote(x) else "no quotation")
                c[k] = c.get(k, 0) + 1
        p(f"MARKS {name}: " + "; ".join(f"{m} {q} {n}" for (m, q), n in sorted(c.items())))
        bad = sum(1 for s in d.values() for x in s["rules"] if _has_quote(x) and x.get("quotations_verified") is not True)
        p(f"QUOTED RULES NOT VERIFIED {name}: {bad}")
    stated = sorted(st for st in ts if any(x.get("mark") == "stated" for x in ts[st]["rules"])
                    or any(x.get("mark") == "stated" for x in rs[st]["rules"]))
    p("STATED-GRADE STATES (" + str(len(stated)) + "): " + " ".join(stated))
    p("")
    p("### Resolution by kind of office (states with at least one rule of that resolution)")
    p("")
    p("| Resolution | " + " | ".join(TIE_KINDS) + " |")
    p("|---|" + "---|" * len(TIE_KINDS))
    for res in TIE_RESOLUTIONS:
        cells = []
        for k in TIE_KINDS:
            n = len({st for st, s in ts.items() for x in s["rules"] if x["resolution"] == res and k in x["kinds"]})
            cells.append(str(n) if n else "")
        p(f"| {ABBR[res]} | " + " | ".join(cells) + " |")
    p("")
    p("### States by kind of office: what the rules found say")
    p("")
    p("| Kind | Only a lot (or recount, then lot) | Another rule for some office or condition | Lot and a part unread | "
      "Searched, none found | Not read | No rule recorded |")
    p("|---|---|---|---|---|---|---|")
    for k in TIE_KINDS:
        cat = {"only": [], "other": [], "mixed": [], "none": [], "unread": [], "absent": []}
        for st, s in ts.items():
            res = {x["resolution"] for x in s["rules"] if k in x["kinds"]}
            real = res - {"none-found", "unread"}
            if not res:
                cat["absent"].append(st)
            elif real and real <= LOT:
                cat["mixed" if res & {"unread", "none-found"} else "only"].append(st)
            elif real:
                cat["other"].append(st)
            elif "unread" in res:
                cat["unread"].append(st)
            else:
                cat["none"].append(st)
        p(f"| {k} | {len(cat['only'])} | {len(cat['other'])} | {len(cat['mixed'])} | {len(cat['none'])} | "
          f"{len(cat['unread'])} | {len(cat['absent'])} |")
    p("")
    p("### Automatic recounts (a recount with no one's request), as each reading records them")
    p("")
    auto = sorted({st for st, s in rs.items() for x in s["rules"] if x["type"] == "automatic"})
    p(f"{len(auto)} states: " + " ".join(auto))
    p("")
    p("| State | Offices | Trigger, in the reading's words | Mark |")
    p("|---|---|---|---|")
    for st in auto:
        for x in rs[st]["rules"]:
            if x["type"] == "automatic":
                w = ((x.get("threshold") or {}).get("in_words") or "").replace("|", "/")
                kinds = ", ".join(k for k in x["kinds"])
                p(f"| {st} | {kinds} | {w} | {x.get('mark')} |")
    p("")
    p("### Not fully read")
    p("")
    for st, s in ts.items():
        if s["status"] != "read":
            p(f"- {st}: {s['status']}")
    print("\n".join(out))
    return 0


def main(argv):
    if len(argv) >= 2 and argv[1] == "fetch" and len(argv) == 5:
        st, name, url = argv[2:5]
        try:
            meta, txt = fetch_section(st, name, url)
        except (_fetch.Refused, ValueError, RuntimeError) as e:
            print("NOT READ:", e)
            return 1
        print(f"read {meta['bytes']} bytes at {meta['read_utc']} sha256 {meta['sha256'][:16]}; "
              f"{len(norm(txt))} characters of text -> {text_path(st, name)}")
        print(norm(txt)[:400])
        return 0
    if len(argv) >= 2 and argv[1] == "check":
        states = set(argv[2:]) or None
        bad = 0
        for st, r in load_readings(states).items():
            problems, _, _ = check_reading(st, r)
            for p in problems:
                print(p)
            bad += len(problems)
            if not problems:
                print(f"{st}: ok")
        return 1 if bad else 0
    if len(argv) >= 2 and argv[1] == "tables":
        return tables()
    if len(argv) >= 2 and argv[1] == "build":
        return build(allow_failures="--allow-failures" in argv)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
