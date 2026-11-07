# Standardized election datasets: an inventory

*Kept by worker D2 (Senate, House, governor), 2026-11-07, for every level, so that the next worker (D3: state legislatures, local races, primaries, measures) starts from what is known (plan §3a). "Reached" means this environment fetched it on the date given; "refused" names what refused. Licences are as each publisher prints them. Datasets marked "taken" have an intake script in `pipeline/intake/`.*

## Federal and statewide results

| Dataset | Publisher | Covers | Format | Licence | Reached | Taken |
|---|---|---|---|---|---|---|
| *Federal Elections* (yearly volumes) | Federal Election Commission | House and Senate general (and primary) results by candidate, with incumbent marks and party labels; President in presidential years; 2006-2022 workbooks (fec.gov/documents/NNNN/…) | xls, xlsx | none printed; federal record | yes, 2026-11-07 | `fec_federal_elections.py` |
| 2024 General Election Ballot Candidates | FEC | candidates on the 2024 general ballot for Senate and House; "(I)" marks a sitting member | xlsx | none printed | yes | `fec_ballot_candidates.py` |
| *Statistics of the Presidential and Congressional Election* | Clerk of the House | every nominee's vote for Senate, House, delegates, by state; 1920 on (older volumes are scans) | PDF | none printed; House publication | yes (2024) | `clerk_statistics.py` (2024) |
| U.S. Senate statewide 1976-2024 (doi:10.7910/DVN/PEJ5QU) | MIT Election Data and Science Lab (MEDSL) | Senate general and special results by candidate, 1976-2024 | tab | CC0 1.0 | yes | `medsl_dataverse.py` |
| U.S. President 1976-2024 (doi:10.7910/DVN/42MVDX) | MEDSL | President by state | csv | CC0 1.0 | yes | `medsl_dataverse.py` (D1 has its own) |
| U.S. House 1976-2024 (doi:10.7910/DVN/IG0UN2) | MEDSL | House by district, 1976-2024 | tab | CC0 1.0 | behind a Dataverse guestbook asking a name and email: not filled (the maker's call, law 10) | no |
| House / Senate / President constituency returns 1976-2020 (QUUABJ, 3CNSWO, VDDKN5) | MEDSL (older versions) | as above, to 2020 | tab | CC0 1.0 | guestbook, as above | no |
| Candidates in American General Elections (doi:10.7910/DVN/DGDRDT), v4.1 | Cha, Kuriwaki and Snyder | every candidate for President (by state), House, Senate and **governor**, 2006-2024 (odd years too); hand-coded incumbency; standardized names | Stata (dta) | CC0 1.0 | yes | `candidates_american_general_elections.py` |
| Partisanship & Nationalization replication data (doi:10.7910/DVN/DGUMFI) | Algara and Amlani | county-level returns: President 1868-2020, Senate 1908-2020, **governor 1865-2020** | Rdata | CC0 1.0 | record read; files not yet taken (needs an R reader) | no |
| Governors Dataset (doi:10.7910/DVN/PQ0Y1N) | Carl Klarner | governors and gubernatorial election variables, mostly 1961-2010 | xlsx | CC0 1.0 | record read | no |
| United States Governors 1775-2020 (doi:10.7910/DVN/RYY3OW) | Jacob Kaplan (from the National Governors Association) | every governor and party | tab | CC BY 4.0 | record read | no |
| State Office-Level Returns 2016 (doi:10.7910/DVN/XSOFHD) | MEDSL | statewide offices, 2016 | tab | CC0 1.0 | guestbook | no |
| State Offices Precinct-Level Returns 2022 (doi:10.7910/DVN/OAARCY) | MEDSL | precinct returns for **governor and every state office**, 2022, one file per state | csv | CC0 1.0 | record read, no guestbook | no (the check for 2022 governors) |
| State Precinct-Level Returns 2024 (doi:10.7910/DVN/DODOBJ) | MEDSL | precinct returns for state offices, 2024 | csv | CC0 1.0 | record read, no guestbook | no (the check for 2024 governors) |
| State Precinct-Level Returns 2016 (doi:10.7910/DVN/GSZG1O) | MEDSL | precinct returns, 2016 | tab | CC0 1.0 | record read, no guestbook | no |
| Precinct-Level Election Results 2012, 2015, 2017, 2019 (B3NTZR, KTXHEW, VNJAB1, 2AJUII) | MEDSL | precinct returns for those years | tab | (records not read) | found by search | no |
| Election Night Returns 2024 (doi:10.7910/DVN/2CKSIK) | MEDSL | unofficial election-night President counts | csv, tab | CC0 1.0 | record read | no (unofficial; not a result) |
| US 2020 General Official Election Results, tabular / NIST CDF (RV80FW, PBFRQM, 2KJK8U, 0GKBGT) | Stephanie Frank Singer | 2020 official results by state, many offices, one file per state | tab, xml, json | CC0 1.0 | record read | no |
| Virginia Election Data 1969-2026 (doi:10.7910/DVN/BAQ69D) | Joseph Jones | Virginia elections of every level, primaries included | zip | CC BY-SA 4.0 | record read | no |
| Electoral College results | National Archives | President and VP elected, electoral votes, 1789 on | HTML, one page a year | federal record | yes | `nara_electoral_college.py` (D1 has its own) |
| Party Divisions of the House, 1789 to present | House History, Art & Archives | seats by party at the start of each Congress | HTML | none printed | yes | no (used as a check) |
| Party Division (Senate) | U.S. Senate | seats by party by Congress, with changes | HTML | none printed | yes (at /about/parties-leadership/party-division.htm) | no (used as a check) |

## District-level inputs

| Dataset | Publisher | Covers | Format | Licence | Reached | Taken |
|---|---|---|---|---|---|---|
| Presidential results by congressional district | The Downballot (formerly Daily Kos Elections) | 2000-2024 presidential vote on the lines of each House election 2006-2024. Gaps: 2020 on AL/LA/NC 2024 lines, 2008 on CA 2012 lines, 2012 on FL 2016 lines | Google Sheets (CSV export) | none printed | yes | `downballot_pres_by_cd.py` |
| The Downballot's data guide (the-downballot.com/data) | The Downballot | index of its sheets: statewide results by **legislative district** (2012-2020), special elections 2017-2026, open and uncontested seats 2006-2026, primary calendars, redistricting tables, district demographics | Google Sheets | none printed | yes | no (leads for D3) |
| ACS 1-year, table B01003 (table-based summary file) | U.S. Census Bureau | population of every state and congressional district, 2021 on in this format | pipe-delimited | federal record | yes (www2.census.gov). The Census API itself now refuses requests without a key | `census_acs_population.py` |

## Forecasts

| Dataset | Publisher | Covers | Reached |
|---|---|---|---|
| House, Senate and governor forecasts 2018 (`house-forecast-2018` etc. in fivethirtyeight/data) | FiveThirtyEight | daily forecasts with vote-share ranges | READMEs only; the data files sit at projects.fivethirtyeight.com, which redirects to abcnews.com. Refused in effect |
| `forecast-review` (fivethirtyeight/data) | FiveThirtyEight | final 2018 win probabilities by race, no vote share | yes (raw.githubusercontent.com); CC BY 4.0; to be the check beside 2018 |
| `pollster-ratings` raw polls (fivethirtyeight/data) | FiveThirtyEight | polls of many races | not yet read; a lead for a polls-based version of the model's own forecast |
| 538 forecast pages for past years | FiveThirtyEight | every published forecast | need web.archive.org, which this environment refuses |

## Other levels (for D3)

| Dataset | Publisher | Covers | Licence | Reached |
|---|---|---|---|---|
| State Legislative Election Returns, 1967-2022 (doi:10.7910/DVN/FJOGJB) | Carl Klarner | every state legislative general election, candidate by candidate, 1967-2022 | CC0 1.0 | record read, no guestbook |
| MEDSL precinct files (above) | MEDSL | state legislative and local offices and ballot measures where on the ballot | CC0 1.0 | records read |
| OpenElections (github.com/openelections) | OpenElections | certified results by state, precinct and county, many offices and primaries | varies by state repo | not yet read (raw.githubusercontent.com allowed, orchestrator 03:46) |
| Ballotpedia | Ballotpedia | every level | not standardized for download | not read |
