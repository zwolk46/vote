"""pipeline/intake/congress_common.py: what the Senate, House and governor intake scripts share.

Written 2026-11-07 by worker D2 (briefs/D2-data-congress.md, amended 03:13 UTC). Each intake script in
this folder is named for its source and does three things (plan/PLAN.md section 3a):
  1. downloads the source's files into a cache OUTSIDE the repository (CACHE below), once;
  2. checks them (row counts, and sums against the totals the source itself prints);
  3. converts them into contest records in the layout of plan section 3.
This file holds the parts they share, so that each script carries only what is particular to its source.

Rules this code keeps, with their reasons:
  - At most one request every few seconds to one host, and a stop at the first refusal of us
    (briefs/_COMMON.md 13). Reason: a source that blocks us is lost.
  - No contact detail in any request; curl's own default user agent (briefs/_COMMON.md 15).
  - Raw files stay in the cache, not the repository (plan section 3a): anyone can fetch them again.
  - Every file read is recorded with its URL, the time it was read, its size and its SHA-256, so a
    figure can be traced to the exact bytes it came from (law 8).
"""
import datetime as _dt
import hashlib
import json
import os
import subprocess
import time

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir))
CACHE = os.environ.get("VOTE_CACHE", "/tmp/vote-cache")
DATA = os.path.join(REPO, "data")
POLITE_SECONDS = 4.0
_last_request = {}


class Refused(RuntimeError):
    """A host refused us (a 403 not explained by a wrong address, a 429, a challenge page)."""


def now_utc():
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(url, rel_path, refresh=False, min_bytes=1):
    """Download url to CACHE/rel_path with curl -sSL (once; again only if refresh). Returns a record
    {url, path, bytes, sha256, read_utc}. Raises Refused on an HTTP error, and stops: it never retries
    another way (briefs/_COMMON.md 6 and 13)."""
    path = os.path.join(CACHE, rel_path)
    meta_path = path + ".meta.json"
    if os.path.exists(path) and os.path.exists(meta_path) and not refresh:
        with open(meta_path) as f:
            return json.load(f)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    host = url.split("/")[2]
    wait = POLITE_SECONDS - (time.time() - _last_request.get(host, 0.0))
    if wait > 0:
        time.sleep(wait)
    _last_request[host] = time.time()
    tmp = path + ".part"
    out = subprocess.run(["curl", "-sSL", "--max-time", "600", "-o", tmp, "-w", "%{http_code}", url],
                         capture_output=True, text=True)
    code = out.stdout.strip()
    if out.returncode != 0 or code != "200":
        if os.path.exists(tmp):
            os.remove(tmp)
        raise Refused(f"{url}: curl exit {out.returncode}, HTTP {code}, {out.stderr.strip()[:200]}")
    size = os.path.getsize(tmp)
    if size < min_bytes:
        os.remove(tmp)
        raise Refused(f"{url}: only {size} bytes")
    os.replace(tmp, path)
    rec = {"url": url, "path": rel_path, "bytes": size, "sha256": sha256(path), "read_utc": now_utc()}
    with open(meta_path, "w") as f:
        json.dump(rec, f, indent=1)
    return rec


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


def read_json(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path) as f:
        return json.load(f)
