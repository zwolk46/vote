#!/bin/sh
# Fetches, for the fourth pass (c31, c32, c33), the pages the checks read: the Census Bureau's two 2020 files
# (pipeline/places.py), the states' lists of their statewide measures and the two results pages that print totals
# (data/measure/statewide-filed-local.json: one list per state, the hosts D3 records as refusing left out), the
# Washington canvass PDF, and a sample of the pages of the threshold rules that carry a `proposer`
# (data/measure/thresholds.json). curl -sSL into ~/.cache/vote-m2/fourth/, outside the repository; one request every
# 5 s; a host that refuses (403, 429) is not asked again. Then MEDSL's own 2018 and 2020 files (GitHub,
# MEDSL/2018-elections-official and MEDSL/2020-elections-official at the commits pipeline/intake/medsl_precinct.py
# names) by a blob-less git clone and `git show`, as the pipeline reads them, into ~/.cache/vote-m2/fourth/medsl/.
# Usage: sh checks/m2/fetch_fourth_pass.sh
D=${VOTE_M2_CACHE:-$HOME/.cache/vote-m2}/fourth
mkdir -p "$D/medsl"
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
python3 -I - "$ROOT/data/measure/statewide-filed-local.json" "$ROOT/data/measure/thresholds.json" "$D/urls.txt" <<'PY'
import json, sys
sw = json.load(open(sys.argv[1]))["questions"]
rules = json.load(open(sys.argv[2]))["rules"]
refused = ("sos.ga.gov", "law.justia.com", "apps.azsos.gov", "azsos.gov", "maine.gov", "ohiosos.gov", "sos.ri.gov",
           "elections.ri.gov", "oregonlegislature.gov", "sos.oregon.gov/elections/Pages/measure")
out = [("census:places", "https://www2.census.gov/geo/docs/reference/codes2020/national_place_by_county2020.txt"),
       ("census:cousub", "https://www2.census.gov/geo/docs/reference/codes2020/national_cousub2020.txt")]
seen = set()
for q in sw:   # one list per state and year, and the certified canvass where the record names one
    u = (q.get("list") or {}).get("url")
    if u and u not in seen and not any(h in u for h in refused):
        seen.add(u); out.append((f"list:{q['state']}:{q['year']}", u))
    cu = (((q.get("state_total") or {}).get("certified") or {}).get("source") or {}).get("url")
    if cu and cu not in seen and not any(h in cu for h in refused):
        seen.add(cu); out.append((f"canvass:{q['state']}:{q['year']}", cu))
# Washington's results site prints its figures on sub-pages ('Measures-All.html'; the advisory vote's own page); the
# Measures tab names the measures only
out.append(("list-all:WA:2024", "https://results.vote.wa.gov/results/20241105/Measures-All.html"))
out.append(("measure:WA:2018:AV19", "https://results.vote.wa.gov/results/20181106/Advisory-Votes-Advisory-Vote-No-19-Engrossed-Second-Substitute-Senate-Bill-6269.html"))
n = 0
for r in rules:   # the rules with a proposer: their pages, at most ten, hosts that refuse left out
    u = r.get("url")
    if r.get("proposer") and u and u not in seen and not any(h in u for h in refused) and n < 10:
        seen.add(u); out.append((f"rule:{r['state']}:{r['citation']}", u)); n += 1
import re
with open(sys.argv[3], "w") as f:
    for k, u in out:   # the file is named by its key, so a later run adds pages without renumbering the earlier ones
        f.write(f"{re.sub(r'[^A-Za-z0-9]+', '_', k).strip('_')}\t{k}\t{u}\n")
print(len(out), "URLs")
PY
touch "$D/index.txt" "$D/refused_hosts.txt"
while IFS="$(printf '\t')" read -r n k u; do
  host=$(printf '%s' "$u" | sed -E 's#^https?://([^/]+).*#\1#')
  if grep -q "	200	.*	$u	" "$D/index.txt" 2>/dev/null; then continue; fi   # fetched already (a second run adds only new pages)
  if grep -qx "$host" "$D/refused_hosts.txt"; then
    echo "$n	skipped	$(date -u +%H:%M:%S)	$k	$u	(host refused earlier)" >> "$D/index.txt"; continue
  fi
  ext=html; case "$u" in *.pdf|*.PDF) ext=pdf;; *.txt) ext=txt;; esac
  code=$(curl -sSL -A "vote-m2-check/1.0" --max-time 300 -o "$D/$n.$ext" -w "%{http_code}" "$u" 2>>"$D/curl_errors.txt")
  echo "$n	$code	$(date -u +%H:%M:%S)	$k	$u	$D/$n.$ext" >> "$D/index.txt"
  case "$code" in 403|429) echo "$host" >> "$D/refused_hosts.txt";; esac
  sleep 5
done < "$D/urls.txt"
# MEDSL's files by git, as pipeline/intake/medsl_precinct.py reads them (blob-less clone, one blob fetched per file)
G="$D/../medsl_git"
mkdir -p "$G"
one() {   # repo commit path
  d="$G/$(printf '%s' "$1" | cut -d/ -f2)"
  [ -d "$d/.git" ] || git clone -q --filter=blob:none --no-checkout "https://github.com/$1" "$d"
  git -C "$d" cat-file -e "$2" 2>/dev/null || git -C "$d" fetch -q --filter=blob:none origin "$2"
  [ -s "$D/medsl/$(basename "$3")" ] && return
  git -C "$d" show "$2:$3" > "$D/medsl/$(basename "$3")" && echo "medsl	$(date -u +%H:%M:%S)	https://github.com/$1/blob/$2/$3	$D/medsl/$(basename "$3")	$(sha256sum "$D/medsl/$(basename "$3")" | cut -c1-64)" >> "$D/index.txt"
  sleep 5
}
for st in la az wa; do one MEDSL/2018-elections-official 42055b11dcd5477bc125cdec5a18fbcc60fb6bed "individual_states/2018-$st-precinct-general.zip"; done
one MEDSL/2020-elections-official a450bb45da90cda13a8e8ce2556c3a1d90dce324 all_states/2020-all-states-local-precinct-general.zip
echo "### done $(date -u +%H:%M:%S)" >> "$D/index.txt"
