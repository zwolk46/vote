#!/bin/sh
# Fetches, for the seventh pass's input-volume check (c38_input_volume.py), the second counts that are not in the
# caches of the earlier passes: MEDSL's state-level U.S. President 1976-2024 and U.S. House 1976-2024 files from
# Harvard Dataverse (doi:10.7910/DVN/42MVDX file 13887042, as D1's source block names it; doi:10.7910/DVN/IG0UN2
# file 13592823, from the dataset's record fetched 2026-11-07 into dv_IG0UN2.json), and Indiana's 2024 certified
# results files for the federal and state offices (the site's own data files, as pipeline/intake/in_enr.py names
# them: settings.json, statewideElectionsC_A.json, OffCatC_<category>_A.json), and North Carolina's State Board results
# files of five general elections (dl.ncsbe.gov, as pipeline/intake/ncsbe.py names them). MEDSL's precinct files and the git-shown
# 2018 zips come from checks/m2/fetch_fifth_pass.sh (its lists extended for this pass). curl -sSL into
# ~/.cache/vote-m2/seventh/, outside the repository; one request every 5 s; a host that refuses (403, 429) is not asked
# again; a file already fetched is not fetched twice.
# Usage: sh checks/m2/fetch_seventh_pass.sh
D=${VOTE_M2_CACHE:-$HOME/.cache/vote-m2}/seventh
mkdir -p "$D/in_enr" "$D/medsl_state" "$D/ncsbe"
{
  printf 'medsl_state:president\thttps://dataverse.harvard.edu/api/access/datafile/13887042?format=original\t%s/medsl_state/1976-2024-president.csv\n' "$D"
  printf 'medsl_state:house\thttps://dataverse.harvard.edu/api/access/datafile/13592823\t%s/medsl_state/1976-2024-house.tab\n' "$D"
  printf 'in_enr:settings\thttps://enr.indianavoters.in.gov/archive/2024General/data/settings.json\t%s/in_enr/settings.json\n' "$D"
  printf 'in_enr:categories\thttps://enr.indianavoters.in.gov/archive/2024General/data/statewideElectionsC_A.json\t%s/in_enr/statewideElectionsC_A.json\n' "$D"
  # the Federal and State headings' categories (statewideElectionsC_A.json, read 2026-11-07): President, US Senator,
  # US Representative, Governor, Attorney General, State Senator, State Representative
  for c in 1019 1006 1005 1007 1022 1018 1039; do
    printf 'in_enr:OffCatC_%s\thttps://enr.indianavoters.in.gov/archive/2024General/data/OffCatC_%s_A.json\t%s/in_enr/OffCatC_%s_A.json\n' "$c" "$c" "$D" "$c"
  done
  # North Carolina's State Board results files of the general elections not in the fifth pass's cache, for the
  # NCSBE-sourced p (the file's federal and statewide contests against D1 and D2)
  for d in 2000-11-07 2002-11-05 2004-11-02 2006-11-07 2012-11-06; do
    n="results_pct_$(printf '%s' "$d" | tr -d -)".zip
    printf 'ncsbe:%s\thttps://dl.ncsbe.gov/ENRS/%s/%s\t%s/ncsbe/%s\n' "$d" "$(printf '%s' "$d" | tr - _)" "$n" "$D" "$n"
  done
} > "$D/urls.txt"
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
echo "### done $(date -u +%H:%M:%S)" >> "$D/index.txt"

# New Jersey's Official Lists for the #92 check (c40): the Division of Elections' pages for 2023 and 2025, then every
# Official List PDF they link for the State Senate, the General Assembly and the Governor, the whole-state lists only
# (the pages are read first, so the lists are fetched by the addresses the pages give, not by addresses guessed). The
# same host rule as above: one request every 5 s, a refusal stops the rest. (A first run of this block matched the
# pages' other PDFs too, the unofficial and primary lists and the per-county and per-district results, and fetched 22
# of them before it was stopped; they sit in the cache unread, logged in index.txt.)
mkdir -p "$D/nj"
: > "$D/nj_urls.txt"
for y in 2023 2025; do
  u="https://www.nj.gov/state/elections/election-information-$y.shtml"
  p="$D/nj/page-$y.html"
  if grep -qx "www.nj.gov" "$D/refused_hosts.txt"; then echo "nj:page-$y	skipped	$(date -u +%H:%M:%S)	nj:page-$y	$u	(host refused earlier)" >> "$D/index.txt"; continue; fi
  if ! grep -q "	200	.*	nj:page-$y	" "$D/index.txt" 2>/dev/null; then
    code=$(curl -sSL -A "vote-m2-check/1.0" --max-time 600 -o "$p" -w "%{http_code}" "$u" 2>>"$D/curl_errors.txt")
    echo "nj:page-$y	$code	$(date -u +%H:%M:%S)	nj:page-$y	$u	$p	$(sha256sum "$p" | cut -c1-64)	$(wc -c < "$p")" >> "$D/index.txt"
    case "$code" in 403|429) echo "www.nj.gov" >> "$D/refused_hosts.txt";; esac
    sleep 5
  fi
  # the five lists D3's records rest on, and no other file of the page: the whole-state Official General Election
  # Results of the State Senate, the General Assembly and the Governor (2025: the Senate's 35th district alone)
  grep -oE 'href="[^"]*election-results/'"$y"'/[^"]*\.pdf"' "$p" | sed -E 's/^href="//; s/"$//' | sort -u \
    | grep -E '/'"$y"'-official-general-results-(state-senate|general-assembly|governor|state-senate-35ld)\.pdf$' | while read -r href; do
      case "$href" in http*) full="$href";; /*) full="https://www.nj.gov$href";; *) full="https://www.nj.gov/state/elections/$href";; esac
      printf 'nj:%s\t%s\t%s/nj/%s\n' "$(basename "$href" .pdf)" "$full" "$D" "$(basename "$href")" >> "$D/nj_urls.txt"
    done
done
while IFS="$(printf '\t')" read -r k u p; do
  if [ -s "$p" ] && grep -q "	200	.*	$k	" "$D/index.txt" 2>/dev/null; then continue; fi
  if grep -qx "www.nj.gov" "$D/refused_hosts.txt"; then echo "$k	skipped	$(date -u +%H:%M:%S)	$k	$u	(host refused earlier)" >> "$D/index.txt"; continue; fi
  code=$(curl -sSL -A "vote-m2-check/1.0" --max-time 600 -o "$p" -w "%{http_code}" "$u" 2>>"$D/curl_errors.txt")
  echo "$k	$code	$(date -u +%H:%M:%S)	$k	$u	$p	$(sha256sum "$p" | cut -c1-64)	$(wc -c < "$p")" >> "$D/index.txt"
  case "$code" in 403|429) echo "www.nj.gov" >> "$D/refused_hosts.txt";; esac
  sleep 5
done < "$D/nj_urls.txt"
echo "### done nj $(date -u +%H:%M:%S)" >> "$D/index.txt"
