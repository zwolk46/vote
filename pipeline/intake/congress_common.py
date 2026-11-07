"""pipeline/intake/congress_common.py: what the Senate, House and governor intake scripts share.

Written 2026-11-07 by worker D2 (briefs/D2-data-congress.md, amended 03:13 UTC). Each intake script in
this folder is named for its source and does three things (plan/PLAN.md section 3a):
  1. downloads the source's files into a cache OUTSIDE the repository (CACHE below), once;
  2. checks them (row counts, and sums against the totals the source itself prints);
  3. converts them into contest records in the layout of plan section 3.
This file holds the parts they share, so that each script carries only what is particular to its source.

Rules this code keeps, with their reasons:
  - Every download goes through pipeline/fetch.py: at most one request every few seconds to one host, a
    stop at the first refusal of us or at a redirect to another site (briefs/_COMMON.md 13; reason: a
    source that blocks us is lost), and no contact detail in any request (briefs/_COMMON.md 15).
  - Raw files stay in the cache, not the repository (plan section 3a): anyone can fetch them again.
  - Every file read is recorded with its URL, the time it was read, its size and its SHA-256, so a
    figure can be traced to the exact bytes it came from (law 8).
"""
import datetime as _dt
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import fetch as _fetch  # noqa: E402  (pipeline/fetch.py, D1's: the one implementation of a download)

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir))
CACHE = _fetch.CACHE          # one cache for every intake script: $VOTE_CACHE, or ~/.cache/vote-intake
DATA = os.path.join(REPO, "data")
Refused = _fetch.Refused


def now_utc():
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")


def fetch(url, rel_path, refresh=False, min_bytes=1, storage_sites=()):
    """Download url to CACHE/rel_path through pipeline/fetch.py (once; again only if refresh), and return the
    record these scripts read, {url, path, bytes, sha256, read_utc}. pipeline/fetch.py keeps the rules: curl's
    own user agent, 4 seconds between requests to a host, a stop (Refused) on HTTP 400 or above and on a
    redirect to another site than the url's own or one of storage_sites; it never retries another way
    (briefs/_COMMON.md 6 and 13). Reason for one implementation: the orchestrator, 2026-11-07 05:58 (item 7)."""
    os.makedirs(os.path.dirname(os.path.join(CACHE, rel_path)), exist_ok=True)
    path = _fetch.fetch(url, rel_path, refresh=refresh, storage_sites=storage_sites)
    m = _fetch.meta(rel_path)
    if m["bytes"] < min_bytes:
        os.remove(path)
        os.remove(path + ".meta.json")
        raise Refused(f"{url}: only {m['bytes']} bytes")
    return {"url": m["url"], "path": rel_path, "bytes": m["bytes"], "sha256": m["sha256"], "read_utc": m["read_utc"]}


def source_block(name, url, read_utc, licence, mark="stated", via=None, note=None):
    """The source block of plan section 3, field for field."""
    return {"name": name, "url": url, "read_utc": read_utc, "licence": licence, "mark": mark,
            "via": via, "note": note}


def to_int(x):
    """A vote count from a spreadsheet cell: 12345, 12345.0, '12,345' -> 12345; anything else -> None."""
    if x is None or isinstance(x, bool):
        return None
    if isinstance(x, (int,)):
        return int(x)
    if isinstance(x, float):
        return int(round(x)) if x == x else None
    s = str(x).strip().replace(",", "")
    if not s:
        return None
    try:
        v = float(s)
    except ValueError:
        return None
    return int(round(v))


def contest_id(year, level, state, district=None, special=False, stage=None):
    parts = [str(year), level, state]
    if district is not None:
        parts.append(district)
    if special:
        parts.append("special")
    if stage:
        parts.append(stage)
    return "-".join(parts)


STATE_NAMES = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California",
    "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "DC": "District of Columbia",
    "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana",
    "IA": "Iowa", "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri",
    "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey",
    "NM": "New Mexico", "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio",
    "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont",
    "VA": "Virginia", "WA": "Washington", "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming",
    "AS": "American Samoa", "GU": "Guam", "MP": "Northern Mariana Islands", "PR": "Puerto Rico",
    "VI": "U.S. Virgin Islands",
}
STATES_50 = [s for s in STATE_NAMES if s not in ("DC", "AS", "GU", "MP", "PR", "VI")]
ABBR = {v.upper(): k for k, v in STATE_NAMES.items()}


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, path)


def write_contest_file(path, obj):
    """A contest file with one contest per line: small enough to ship, and a diff shows which contests
    changed. Every key but "contests" is written as indented JSON."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    head = {k: v for k, v in obj.items() if k != "contests"}
    with open(tmp, "w") as f:
        body = json.dumps(head, indent=1, ensure_ascii=False)
        f.write(body[:-2] + ',\n "contests": [\n')
        cs = obj.get("contests", [])
        for i, c in enumerate(cs):
            f.write("  " + json.dumps(c, ensure_ascii=False, separators=(",", ":")) + (",\n" if i < len(cs) - 1 else "\n"))
        f.write(" ]\n}\n")
    with open(tmp) as f:
        json.load(f)          # the file must read back as JSON
    os.replace(tmp, path)


def read_json(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path) as f:
        return json.load(f)
