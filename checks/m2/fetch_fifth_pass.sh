#!/bin/sh
# Fetches, for the fifth pass (c34, c35, c36) and the seventh's volume check (c38), the sources the checks read: MEDSL's precinct files for the state-years
# the three PRs changed (2022 and 2024 from Harvard Dataverse, the sets pipeline/intake/medsl_precinct.py names, in
# their original form where Dataverse ingested them; 2016's local set; 2018's per-state zips and 2020's local zip from
# MEDSL's own GitHub repositories by a blob-less git clone and `git show`, as the pipeline reads them), North
# Carolina's State Board results files for the dates of its statewide judges (dl.ncsbe.gov, pipeline/intake/ncsbe.py),
# and New Mexico's official 2022 Public Education Commission page (pipeline/intake/nm_sos.py). The Census Bureau's
# county subdivision file was fetched by fetch_fourth_pass.sh and is read from there. curl -sSL into
# ~/.cache/vote-m2/fifth/, outside the repository; one request every 5 s; a host that refuses (403, 429) is not asked
# again; a file already fetched is not fetched twice.
# Usage: sh checks/m2/fetch_fifth_pass.sh
D=${VOTE_M2_CACHE:-$HOME/.cache/vote-m2}/fifth
mkdir -p "$D/medsl" "$D/ncsbe"
python3 -I - "$D" <<'PY'
import json, os, re, sys
D = sys.argv[1]
out = []
# Dataverse's file lists of the 2024 and 2022 sets (fetched 2026-11-07 16:58 UTC into dv_<DOI>.json; kept)
need = {"NYTPDU": ["al", "az", "ga", "ia", "ky", "mi", "mn", "mt", "nd", "nm", "nv", "ny", "oh", "or", "sc", "sd", "tx", "ut", "wa", "wv", "id", "ar", "ms", "co", "hi",
                   "ak", "ca", "ct", "dc", "de", "fl", "il", "ks", "ma", "md", "me", "mo", "nc", "ne", "nh", "nj", "ok", "pa", "ri", "tn", "va", "vt", "wi", "wy", "in"],
        "UYQIEP": ["2022-ar-local", "mn22", "mt22", "2022-nd-local", "nm22", "NV-", "oh22", "ok22", "sd22", "ky22", "2022-wa-local",
                   "2022-az-local", "2022-id-local", "2022-mi-local", "ny22", "or22", "ga22", "HI-", "il22", "colorado",   # the sixth pass (#90)
                   "RI-", "WY-", "ak22", "fl22", "mo22", "ne22", "south_carolina", "nh22"]}   # the seventh pass's volume check (c38): every 2022 and 2024 file a p rests on, and 2024's Indiana
for doi, states in need.items():
    d = json.load(open(os.path.join(D, f"dv_{doi}.json")))
    for f in d["data"]["latestVersion"]["files"]:
        df = f["dataFile"]
        name = df.get("originalFileName") or df["filename"]
        year = "2024" if doi == "NYTPDU" else "2022"
        hit = any(name.startswith(f"2024-{s}-") for s in states) if year == "2024" else any(name.startswith(s) for s in states)
        if not hit:
            continue
        url = f"https://dataverse.harvard.edu/api/access/datafile/{df['id']}" + ("?format=original" if df.get("originalFileName") else "")
        out.append((f"medsl:{year}:{name}", url, os.path.join(D, "medsl", name)))
out.append(("medsl:2016:2016-precinct-local.csv", "https://dataverse.harvard.edu/api/access/datafile/3345356?format=original",
            os.path.join(D, "medsl", "2016-precinct-local.csv")))
out.append(("medsl:2016:2016-precinct-state.csv", "https://dataverse.harvard.edu/api/access/datafile/3345337?format=original",
            os.path.join(D, "medsl", "2016-precinct-state.csv")))   # the pipeline reads 2016's questions from both sets
for d in ["2008-11-04", "2010-11-02", "2014-05-06", "2014-11-04", "2016-06-07", "2016-11-08", "2018-11-06", "2020-11-03",
          "2022-05-17", "2022-11-08", "2024-03-05", "2024-11-05", "2026-03-03"]:
    n = f"results_pct_{d.replace('-', '')}.zip"
    out.append((f"ncsbe:{d}", f"https://dl.ncsbe.gov/ENRS/{d.replace('-', '_')}/{n}", os.path.join(D, "ncsbe", n)))
out.append(("nm_sos:archive:2022", "https://www.sos.nm.gov/sos-archive/election-results-archive/2022-election-results/", os.path.join(D, "nm_sos_archive_2022.html")))
out.append(("nm_sos:pec:2022", "https://electionresults.sos.nm.gov/resultsSW.aspx?type=ECX&map=CTY&eid=2838", os.path.join(D, "nm_sos_pec_2022.html")))
with open(os.path.join(D, "urls.txt"), "w") as f:
    for k, u, p in out:
        f.write(f"{k}\t{u}\t{p}\n")
print(len(out), "URLs")
PY
touch "$D/index.txt" "$D/refused_hosts.txt"
while IFS="$(printf '\t')" read -r k u p; do
  host=$(printf '%s' "$u" | sed -E 's#^https?://([^/]+).*#\1#')
  if [ -s "$p" ] && grep -q "	200	.*	$k	" "$D/index.txt" 2>/dev/null; then continue; fi
  if grep -qx "$host" "$D/refused_hosts.txt"; then
    echo "$k	skipped	$(date -u +%H:%M:%S)	$k	$u	(host refused earlier)" >> "$D/index.txt"; continue
  fi
  code=$(curl -sSL -A "vote-m2-check/1.0" --max-time 3600 -o "$p" -w "%{http_code}" "$u" 2>>"$D/curl_errors.txt")
  echo "$k	$code	$(date -u +%H:%M:%S)	$k	$u	$p	$(sha256sum "$p" | cut -c1-64)	$(wc -c < "$p")" >> "$D/index.txt"
  case "$code" in 403|429) echo "$host" >> "$D/refused_hosts.txt";; esac
  sleep 5
done < "$D/urls.txt"
# MEDSL's 2018 files by git, as pipeline/intake/medsl_precinct.py reads them (the clone fetch_fourth_pass.sh made)
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
# from ct on: the seventh pass (c38), every 2018 file a p rests on
for st in al ar ga ia il mi mn mt nd nm nv oh ok sd tx wv ny co hi ct dc de fl id ks ky md me mo ms ne nh nj ri sc va vt wy; do one MEDSL/2018-elections-official 42055b11dcd5477bc125cdec5a18fbcc60fb6bed "individual_states/2018-$st-precinct-general.zip"; done
echo "### done $(date -u +%H:%M:%S)" >> "$D/index.txt"
