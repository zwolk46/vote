#!/bin/sh
# Fetches every page the local-threshold rules cite (data/measure/thresholds-local.json: the rules' own URLs and
# their also_cited and supporting ones) into ~/.cache/vote-m2/law_local/, for c27's quote check. curl -sSL into
# files outside the repository; one request every 5 s to a host; stops that host at the first refusal.
# Usage: sh checks/m2/fetch_law_pages.sh [host-substring]   (default: both hosts, one after the other)
D=${VOTE_M2_CACHE:-$HOME/.cache/vote-m2}/law_local
mkdir -p "$D"
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
python3 -I - "$ROOT/data/measure/thresholds-local.json" "$D/law_urls.txt" <<'PY'
import json, sys
book = json.load(open(sys.argv[1]))
seen = {}
for r in book["rules"]:
    seen.setdefault(r["url"], None)
    for k in ("also_cited", "supporting"):
        for a in r.get(k) or []:
            seen.setdefault(a["url"], None)
with open(sys.argv[2], "w") as f:
    for i, u in enumerate(seen):
        f.write(f"{i:02d}\t{u}\n")
print(len(seen), "distinct URLs")
PY
for host in ${1:-ncleg legis.la}; do
  : > "$D/index_$host.txt"
  grep "$host" "$D/law_urls.txt" | while IFS="$(printf '\t')" read -r n u; do
    code=$(curl -sSL -A "vote-m2-check/1.0" --max-time 60 -o "$D/$n.html" -w "%{http_code}" "$u" 2>>"$D/curl_errors_$host.txt")
    echo "$n	$code	$(date -u +%H:%M:%S)	$u" >> "$D/index_$host.txt"
    if [ "$code" != "200" ]; then echo "$n	STOP after $code" >> "$D/index_$host.txt"; break; fi
    sleep 5
  done
  echo "### done $host $(date -u +%H:%M:%S)" >> "$D/index_$host.txt"
done
