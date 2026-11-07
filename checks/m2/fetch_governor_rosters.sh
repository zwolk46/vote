#!/bin/sh
# Fetches the ten governor rosters D2's incumbency table cites (data/congress/governor-incumbency.json: rosters)
# into ~/.cache/vote-m2/governor_rosters/, for c28's sha256 and quote check. curl -sSL into files outside the
# repository; one request every 5 s; the six pages D2 could not read (rosters_not_read) are not tried.
# Usage: sh checks/m2/fetch_governor_rosters.sh
D=${VOTE_M2_CACHE:-$HOME/.cache/vote-m2}/governor_rosters
mkdir -p "$D"
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
python3 -I - "$ROOT/data/congress/governor-incumbency.json" "$D/roster_urls.txt" <<'PY'
import json, sys
table = json.load(open(sys.argv[1]))
with open(sys.argv[2], "w") as f:
    for st, r in table["rosters"].items():
        f.write(f"{st}\t{r['url']}\n")
print(len(table["rosters"]), "rosters")
PY
: > "$D/index.txt"
while IFS="$(printf '\t')" read -r st u; do
  ext=html; case "$u" in *.pdf) ext=pdf;; esac
  code=$(curl -sSL -A "vote-m2-check/1.0" --max-time 90 -o "$D/$st.$ext" -w "%{http_code}" "$u" 2>>"$D/curl_errors.txt")
  echo "$st	$code	$(date -u +%H:%M:%S)	$u	$D/$st.$ext" >> "$D/index.txt"
  sleep 5
done < "$D/roster_urls.txt"
echo "### done $(date -u +%H:%M:%S)" >> "$D/index.txt"
