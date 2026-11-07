#!/bin/sh
# Fetches, for c30's quote check, the four statewide rules read in step (a) (data/measure/thresholds.json, read_in)
# and a sample of the ballot texts' sources (data/measure/ballot-texts.json: per state, the first two questions'
# source pages and the fact's own page where it is another), keeping off the hosts D3 records as refusing, into
# ~/.cache/vote-m2/ballot_texts/. curl -sSL into files outside the repository; one request every 5 s.
# Usage: sh checks/m2/fetch_ballot_texts.sh
D=${VOTE_M2_CACHE:-$HOME/.cache/vote-m2}/ballot_texts
mkdir -p "$D"
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
python3 -I - "$ROOT/data/measure/ballot-texts.json" "$ROOT/data/measure/thresholds.json" "$D/urls.txt" <<'PY'
import collections, json, sys
b = json.load(open(sys.argv[1]))["questions"]
t = json.load(open(sys.argv[2]))["rules"]
refused = ("sos.ga.gov", "law.justia.com", "apps.azsos.gov", "maine.gov", "ohiosos.gov", "sos.ri.gov", "elections.ri.gov",
           "oregonlegislature.gov", "sos.oregon.gov/elections/Pages/measure")
out = []
for r in t:
    if r.get("read_in"):
        out.append(("rule:" + r["state"] + ":" + r["citation"], r["url"]))
by_state = collections.defaultdict(list)
for qid, q in sorted(b.items()):
    by_state[q["state"]].append((qid, q))
for st, qs in sorted(by_state.items()):
    n = 0
    for qid, q in qs:
        u = (q.get("source") or {}).get("url")
        if not u or any(h in u for h in refused):
            continue
        out.append(("q:" + qid, u))
        n += 1
        fs = (q.get("fact") or {}).get("source")
        fu = fs.get("url") if isinstance(fs, dict) else None
        if fu and fu != u and not any(h in fu for h in refused):
            out.append(("f:" + qid, fu))
            n += 1
        if n >= 2:
            break
seen, rows = set(), []
for k, u in out:
    if u not in seen:
        seen.add(u)
        rows.append((k, u))
with open(sys.argv[3], "w") as f:
    for i, (k, u) in enumerate(rows):
        f.write(f"{i:02d}\t{k}\t{u}\n")
print(len(rows), "URLs")
PY
: > "$D/index.txt"
while IFS="$(printf '\t')" read -r n k u; do
  ext=html; case "$u" in *.pdf|*.PDF) ext=pdf;; esac
  code=$(curl -sSL -A "vote-m2-check/1.0" --max-time 90 -o "$D/$n.$ext" -w "%{http_code}" "$u" 2>>"$D/curl_errors.txt")
  echo "$n	$code	$(date -u +%H:%M:%S)	$k	$u	$D/$n.$ext" >> "$D/index.txt"
  sleep 5
done < "$D/urls.txt"
echo "### done $(date -u +%H:%M:%S)" >> "$D/index.txt"
