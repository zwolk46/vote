#!/bin/sh
# The sources M2's sixth pass (c37: D3's #90) reads, fetched once into ~/.cache/vote-m2/sixth/ (outside the repository):
# Washington's 2022 results page, its Export page and the three exports (pipeline/intake/wa_sos.py reads them), and the
# page's "Certified Election Results (PDF)" link (which D3 found answering 404); North Dakota's election-results archive,
# the 2022 and 2024 front pages of its results site and their statewide and judicial pages (pipeline/intake/nd_sos.py);
# every distinct quote_url of data/measure/statewide-filed-local.json (20) and the two rule pages whose proposer_quote
# data/measure/thresholds.json carries (Missouri's revisor, sections 52(b) and 52(a); Oklahoma's Senate PDF). MEDSL's files the pass needs are
# fetched by fetch_fifth_pass.sh into the fifth cache (its lists were extended). curl -sSL; one request every 5 s; a
# host that refuses (403, 429) is not asked again; a file already fetched (HTTP 200) is not fetched twice.
# Usage: sh checks/m2/fetch_sixth_pass.sh   (from the repository root)
D=${VOTE_M2_CACHE:-$HOME/.cache/vote-m2}/sixth
mkdir -p "$D"
python3 -I - "$D" "$(pwd)" <<'PY'
import json, os, re, sys
D, R = sys.argv[1], sys.argv[2]
out = []
wa = "https://results.vote.wa.gov/results/20221108/"
out += [("wa_sos:results", wa, "wa_20221108_results.html"), ("wa_sos:export_page", wa + "Export.html", "wa_20221108_export.html")]
for n in ("StateExecutive", "Judicial", "Measures"):
    out.append((f"wa_sos:{n}", f"{wa}export/20221108_{n}.csv", f"wa_20221108_{n}.csv"))
out.append(("wa_sos:certified_pdf", wa + "SignedCertification.pdf", "wa_20221108_SignedCertification.pdf"))
nd = "https://results.sos.nd.gov/"
out.append(("nd_sos:archive", "https://www.sos.nd.gov/elections/election-results", "nd_election_results.html"))
out.append(("nd_sos:2022:front", nd + "Default.aspx?map=Cty&eid=vxUYQ0lrpP4.", "nd_2022_front.html"))
out.append(("nd_sos:2022:statewide", nd + "ResultsSW.aspx?text=All&type=SW&map=CTY&eid=vxUYQ0lrpP4.", "nd_2022_statewide.html"))
out.append(("nd_sos:2022:judicial", nd + "ResultsSW.aspx?text=Race&type=JD&map=CTY&area=District&eid=vxUYQ0lrpP4.", "nd_2022_judicial.html"))
out.append(("nd_sos:2024:front", nd + "Default.aspx?map=Cty", "nd_2024_front.html"))
out.append(("nd_sos:2024:statewide", nd + "ResultsSW.aspx?text=All&type=SW&map=CTY", "nd_2024_statewide.html"))
urls = {}
def walk(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "quote_url" and isinstance(v, str):
                urls.setdefault(v, len(urls))
            walk(v)
    elif isinstance(o, list):
        for v in o:
            walk(v)
walk(json.load(open(os.path.join(R, "data/measure/statewide-filed-local.json"))))
for u, i in urls.items():
    ext = ".pdf" if u.lower().endswith(".pdf") else ".html"
    out.append((f"quote:{i:02d}", u, f"quote_{i:02d}{ext}"))
t = json.load(open(os.path.join(R, "data/measure/thresholds.json")))
rules = {}
def walk2(o):
    if isinstance(o, dict):
        if "proposer_quote" in o and o.get("url"):
            rules.setdefault(o["url"], len(rules))
        if "proposer_quote" in o and isinstance(o["proposer_quote"], dict) and o["proposer_quote"].get("url"):
            rules.setdefault(o["proposer_quote"]["url"], len(rules))   # a quote taken from a section of its own (Missouri's 52(a))
        for v in o.values():
            walk2(v)
    elif isinstance(o, list):
        for v in o:
            walk2(v)
walk2(t)
for u, i in rules.items():
    ext = ".pdf" if u.lower().endswith(".pdf") else ".html"
    out.append((f"rule:{i}", u, f"rule_{i}{ext}"))
with open(os.path.join(D, "urls.txt"), "w") as f:
    for k, u, p in out:
        f.write(f"{k}\t{u}\t{os.path.join(D, p)}\n")
print(len(out), "URLs")
PY
touch "$D/index.txt" "$D/refused_hosts.txt"
while IFS="$(printf '\t')" read -r k u p; do
  host=$(printf '%s' "$u" | sed -E 's#^https?://([^/]+).*#\1#')
  if [ -s "$p" ] && grep -q "	200	.*	$k	" "$D/index.txt" 2>/dev/null; then continue; fi
  if grep -qx "$host" "$D/refused_hosts.txt"; then
    echo "$k	skipped	$(date -u +%H:%M:%S)	$k	$u	(host refused earlier)" >> "$D/index.txt"; continue
  fi
  code=$(curl -sSL -A "vote-m2-check/1.0" --max-time 600 -o "$p" -w "%{http_code}" "$u" 2>>"$D/curl_errors.txt")
  echo "$k	$code	$(date -u +%H:%M:%S)	$k	$u	$p	$(sha256sum "$p" | cut -c1-64)	$(wc -c < "$p")" >> "$D/index.txt"
  case "$code" in 403|429) echo "$host" >> "$D/refused_hosts.txt";; esac
  sleep 5
done < "$D/urls.txt"
echo "### done $(date -u +%H:%M:%S)" >> "$D/index.txt"
