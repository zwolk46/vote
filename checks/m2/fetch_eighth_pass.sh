#!/bin/sh
# M2, eighth pass, section 18: the state and county files D3's #106 read, fetched once more for my own reading
# (one request every six seconds to a host; the first refusal stops that host; nothing from Virginia's or Michigan's
# Secretary of State is asked). Writes ~/.cache/vote-m2/eighth/src/index.txt: key, HTTP code, time, URL, path, sha256, bytes.
D=${HOME}/.cache/vote-m2/eighth/src
mkdir -p "$D/in_enr_2016" "$D/ut_lg" "$D/dc_boe" "$D/arenac" "$D/census_sld" "$D/ct_sots" "$D/mo_sos" "$D/wv_sos" "$D/aa" "$D/klarner"
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
  governors)  # section 19: the governor counts D3's #109 read (data/local/REPORT.md section 35), one request to each host; Missouri's three six seconds apart
    fetch ct:contest3781 "https://electionhistory.ct.gov/contest/3781" "$D/ct_sots/contest_3781.html"
    fetch ut:2008gen "https://vote.utah.gov/wp-content/uploads/2023/09/2008Gen.xls" "$D/ut_lg/2008Gen.xls"
    fetch wv:2012statewide "https://apps.sos.wv.gov/elections/results/results.aspx?year=2012&eid=13&county=Statewide" "$D/wv_sos/results_2012_eid13_statewide.html"
    fetch mo:2008 "https://www.sos.mo.gov/CMSImages/ElectionResultsStatistics/AllRacesGeneralNovember2008.pdf" "$D/mo_sos/AllRacesGeneralNovember2008.pdf" && sleep 6
    fetch mo:2012 "https://www.sos.mo.gov/CMSImages/ElectionResultsStatistics/2012GeneralElection.pdf" "$D/mo_sos/2012GeneralElection.pdf" && sleep 6
    fetch mo:2016 "https://www.sos.mo.gov/CMSImages/ElectionResultsStatistics/ActualResults-November82016-GeneralElection.pdf" "$D/mo_sos/ActualResults-November82016-GeneralElection.pdf";;
  aa)  # Algara and Amlani's county returns (Harvard Dataverse doi:10.7910/DVN/DGUMFI, CC0 1.0, no guestbook: the dataset's JSON, fetched first, says fileAccessRequest false and restricted false)
    fetch aa:rdata "https://dataverse.harvard.edu/api/access/datafile/5028535" "$D/aa/dataverse_shareable_gubernatorial_county_returns_1865_2020.Rdata";;
  klarner)  # section 19: Klarner's candidate-level file (Harvard Dataverse doi:10.7910/DVN/FJOGJB, CC0 1.0, the dataset whose contest file I hold; one request; the intake sums a candidate's lines by candidate id, which the fusion scan counts)
    fetch klarner:candidates "https://dataverse.harvard.edu/api/access/datafile/10273085?format=original" "$D/klarner/127_slers_1967to2022_forsharing20230810.csv";;
  va_code)  # section 20: the three Code of Virginia pages D3's #111 read (data/local/REPORT.md section 36), one request each, six seconds apart, to law.lis.virginia.gov (the General Assembly's site); Ballotpedia, FindLaw and vacode.org are not asked (D3's refusals, 08:07)
    mkdir -p "$D/va_code"
    fetch vacode:24.2-613 "https://law.lis.virginia.gov/vacode/title24.2/chapter6/section24.2-613/" "$D/va_code/section24.2-613.html" || exit 1; sleep 6
    fetch vacode:t22.1c5a7 "https://law.lis.virginia.gov/vacodefull/title22.1/chapter5/article7/" "$D/va_code/title22.1-chapter5-article7.html" || exit 1; sleep 6
    fetch vacode:t10.1c5a3 "https://law.lis.virginia.gov/vacodefull/title10.1/chapter5/article3/" "$D/va_code/title10.1-chapter5-article3.html";;
  in_2018)  # section 20: Indiana's 2018 archive as D3's #111 read it (settings, the office list, the State Senator file), six seconds apart; the House file is the in_2018_house branch
    mkdir -p "$D/in_enr_2018"
    B=https://enr.indianavoters.in.gov/archive/2018General/data
    fetch in2018:settings "$B/settings.json" "$D/in_enr_2018/settings.json" || exit 1; sleep 6
    fetch in2018:categories "$B/statewideElectionsC_A.json" "$D/in_enr_2018/statewideElectionsC_A.json" || exit 1; sleep 6
    fetch in2018:OffCatC_2180 "$B/OffCatC_2180_A.json" "$D/in_enr_2018/OffCatC_2180_A.json";;
  in_2018_house)  # section 20, D3's #113: the archive's State Representative file (office category 2201 in the cached office list), one request, as D3 read it on the orchestrator's allowance of 09:21 ("one request to the archive's 2018 House file is allowed, as for the Senate")
    B=https://enr.indianavoters.in.gov/archive/2018General/data
    fetch in2018:OffCatC_2201 "$B/OffCatC_2201_A.json" "$D/in_enr_2018/OffCatC_2201_A.json";;
  recount)  # section 21, D3's #115: the two recount sources D3 read once each (data/local/REPORT.md section 38), one request each, six seconds apart; neither file is kept in the repository
    mkdir -p "$D/recount"
    fetch recount:vtp_wp11 "https://vote.caltech.edu/documents/133/vtp_wp11.pdf" "$D/recount/vtp_wp11.pdf" || exit 1; sleep 6
    fetch recount:fairvote "https://fairvote.org/report/election-recounts-2024/" "$D/recount/fairvote-election-recounts-2024.html";;
  singer_record)  # section 22, D3's #118: Singer's dataset record (Harvard Dataverse doi:10.7910/DVN/RV80FW), one request; read for its licence, guestbook and file md5s before the files are asked for
    mkdir -p "$D/singer"
    fetch singer:record "https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/RV80FW" "$D/singer/RV80FW-dataset.json";;
  singer_files)  # section 22: the dataset's 56 files as Dataverse's one download in their original format (as D3 read them, 10:34), one request, after the record showed no guestbook and CC0
    mkdir -p "$D/singer"
    fetch singer:original "https://dataverse.harvard.edu/api/access/dataset/:persistentId/?persistentId=doi:10.7910/DVN/RV80FW&format=original" "$D/singer/RV80FW-original.zip";;
  mt_sos)  # section 22: Montana's 2020 legislative general canvass as D3's #118 read it (data/local/REPORT.md section 39; the file its results page's "2020 General ... Legislative" link names), one request
    mkdir -p "$D/mt_sos"
    fetch mt:canvass2020 "https://sosmt.gov/wp-content/uploads/State_Canvass_Legislative.pdf" "$D/mt_sos/State_Canvass_Legislative.pdf";;
esac
echo "### done $1"
