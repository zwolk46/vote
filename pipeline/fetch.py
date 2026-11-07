"""pipeline/fetch.py: download a published file once, into a cache outside the repository, and record it.

Written 2026-11-07 by worker D1 for the intake scripts in pipeline/intake/ (plan/PLAN.md section 3a: data
comes in by script; raw files stay out of the repository; anyone can fetch the same file again, law 8).

  fetch(url, name)   returns the local path of the file, downloading it only if it is not cached yet.
                     Beside it, <name>.meta.json records the url, when it was read (UTC), its size and
                     sha256, so a source block can say exactly which file a figure came from.
  source(...)        a source block in the layout of plan section 3.

Rules kept here, with their reasons (briefs/_COMMON.md 6, 13, 15):
  - curl's own default User-Agent, nothing else: a browser-like header was refused as bot-check
    circumvention (research/decisiveness-models-v2.md section 1), and the maker's email is never sent.
  - at least 4 seconds between two requests to one host, and a refusal (HTTP 403, 429, or a challenge) is
    raised, never retried another way: a source that blocks us is lost.
  - HTTP status 400 or above stops the script with the status and url, so an error page is never parsed
    as data; so does a redirect to another site (fivethirtyeight.com now sends every address to ABC News).
The cache directory is $VOTE_CACHE, or ~/.cache/vote-intake if that is unset.
"""
import datetime
import hashlib
import json
import os
import subprocess
import time
import urllib.parse

CACHE = os.environ.get("VOTE_CACHE") or os.path.join(os.path.expanduser("~"), ".cache", "vote-intake")
MIN_INTERVAL_S = 4.0
_last_request = {}


class Refused(RuntimeError):
    """The source answered with an error or a refusal. Record it as unread; do not route around it."""


def _now_utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _site(netloc):
    """The registered site of a host, crudely: its last two labels (www.fec.gov -> fec.gov)."""
    return ".".join(netloc.lower().split(":")[0].split(".")[-2:])


def meta(name):
    with open(os.path.join(CACHE, name + ".meta.json")) as f:
        return json.load(f)


def fetch(url, name, refresh=False, timeout_s=600, storage_sites=()):
    """Download url to $CACHE/name (once) and return the path. Raises Refused on HTTP >= 400, or on a
    redirect to another site than the url's own or one of storage_sites (for example "amazonaws.com",
    where Harvard Dataverse keeps its files)."""
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, name)
    meta_path = path + ".meta.json"
    if os.path.exists(path) and os.path.exists(meta_path) and not refresh:
        return path
    host = urllib.parse.urlparse(url).netloc
    wait = MIN_INTERVAL_S - (time.time() - _last_request.get(host, 0.0))
    if wait > 0:
        time.sleep(wait)
    tmp = path + ".part"
    out = subprocess.run(["curl", "-sS", "-L", "--max-time", str(timeout_s), "-o", tmp,
                          "-w", "%{http_code} %{url_effective}", url],
                         capture_output=True, text=True)
    _last_request[host] = time.time()
    if out.returncode != 0:
        raise Refused(f"curl failed for {url}: {out.stderr.strip()}")
    code, _, effective = out.stdout.strip().partition(" ")
    if int(code) >= 400:
        os.remove(tmp)
        raise Refused(f"HTTP {code} for {url}")
    eff_host = urllib.parse.urlparse(effective).netloc
    if _site(eff_host) != _site(host) and _site(eff_host) not in storage_sites:
        # e.g. every fivethirtyeight.com address now redirects to abcnews.go.com: the file is gone
        # from its publisher, and what came back is another site's page, not the data
        os.remove(tmp)
        raise Refused(f"{url} redirected to another site, {effective}")
    os.replace(tmp, path)
    # the effective host only: a signed storage address carries a credential id and an expiry
    record = {"url": url, "served_from": eff_host, "read_utc": _now_utc(),
              "bytes": os.path.getsize(path), "sha256": _sha256(path)}
    with open(meta_path, "w") as f:
        json.dump(record, f, indent=1)
    return path


def source(name, url, read_utc, licence, mark="measured", via=None, note=None, sha256=None):
    """A source block in the layout of plan/PLAN.md section 3 (sha256 added: which file exactly)."""
    block = {"name": name, "url": url, "read_utc": read_utc, "licence": licence, "mark": mark,
             "via": via, "note": note}
    if sha256:
        block["sha256"] = sha256
    return block


def source_for(name_in_cache, title, licence, mark="measured", via=None, note=None):
    """The source block for a cached file, filled from its meta record."""
    m = meta(name_in_cache)
    return source(title, m["url"], m["read_utc"], licence, mark, via, note, m["sha256"])
