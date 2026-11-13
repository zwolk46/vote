#!/bin/sh
# M2, eighth pass, section 18: the state and county files D3's #106 read, fetched once more for my own reading
# (one request every six seconds to a host; the first refusal stops that host; nothing from Virginia's or Michigan's
# Secretary of State is asked). Writes ~/.cache/vote-m2/eighth/src/index.txt: key, HTTP code, time, URL, path, sha256, bytes.
D=${HOME}/.cache/vote-m2/eighth/src
mkdir -p "$D/in_enr_2016" "$D/ut_lg" "$D/dc_boe" "$D/arenac" "$D/census_sld"
IDX="$D/index.txt"
fetch() {  # key url path
  code=$(curl -sSL -o "$3" -w '%{http_code}' --max-time 300 "$2" 2>>"$D/curl_errors.txt") || code=000
  sha=$(sha256sum "$3" 2>/dev/null | cut -d' ' -f1); bytes=$(stat -c %s "$3" 2>/dev/null)
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$1" "$code" "$(date -u +%H:%M:%S)" "$2" "$3" "$sha" "$bytes" >> "$IDX"
  case "$code" in 200) return 0;; *) echo "$1 refused: $code" >> "$D/refused_hosts.txt"; return 1;; esac
}
case "$1" in
  indiana)
    B=https://enr.indianavoters.in.gov/archive/2016General/data
    fetch in2016:settings "$B/settings.json" "$D/in_enr_2016/settings.json" || exit 1; sleep 6
    fetch in2016:categories "$B/statewideElectionsC_A.json" "$D/in_enr_2016/statewideElectionsC_A.json" || exit 1; sleep 6
    fetch in2016:OffCatC_1766 "$B/OffCatC_1766_A.json" "$D/in_enr_2016/OffCatC_1766_A.json" || exit 1; sleep 6
    fetch in2016:OffCatC_1787 "$B/OffCatC_1787_A.json" "$D/in_enr_2016/OffCatC_1787_A.json" || exit 1;;
  utah) fetch ut:canvass2016 "https://vote.utah.gov/wp-content/uploads/2023/09/2016-General-Election-Statewide-Canvass-3.pdf" "$D/ut_lg/2016-General-Election-Statewide-Canvass-3.pdf";;
  dc) fetch dc:certified2018 "https://electionresults.dcboe.org/Downloads/Reports/November_6_2018_General_Election_Certified_Results.pdf" "$D/dc_boe/November_6_2018_General_Election_Certified_Results.pdf";;
  arenac) fetch arenac:official2022 "https://arenaccountymi.gov/docs/Clerk/Election%20Results/2022/Official%20Nov%208,%202022%20ElectionSummaryReportRPT.pdf" "$D/arenac/Official_Nov_8_2022_ElectionSummaryReportRPT.pdf";;
  census) # $2 $3: the two zips' URLs, found on the Census page first
    fetch census:sldu_2022 "$2" "$D/census_sld/sldu_2022.zip" || exit 1; sleep 6
    fetch census:sldl_2022 "$3" "$D/census_sld/sldl_2022.zip";;
  census-page) fetch census:page "$2" "$D/census_sld/page.html";;
esac
echo "### done $1"
