# Senate, House and governor: sources, method and checks

*Worker D2 (`briefs/D2-data-congress.md`, amended 2026-11-07 03:13 UTC). Started 2026-11-07. This file grows as the work does; §2 is the forecast method proposed to the orchestrator before any p is computed with it (brief, step 2; plan §3).*

## 1. Sources taken in by script

Each is read by one script in `pipeline/intake/`, which downloads to a cache outside the repository (`VOTE_CACHE`, default `/tmp/vote-cache`), records the URL, read time, size and SHA-256 of every file, checks sums against the source's own totals, and normalizes. Rerun any of them to get the same inputs.

| Script | Source | Covers | Licence | Read |
|---|---|---|---|---|
| `fec_federal_elections.py` | FEC, *Federal Elections* workbooks | House and Senate general results with incumbent marks, 2006-2022 | none printed; federal record | 2026-11-07 |
| `clerk_statistics.py` | Clerk of the House, *Statistics of the Presidential and Congressional Election* (PDF) | House and Senate, 2024 (the FEC has no 2024 congressional workbook); the check on the FEC for other years | none printed; House publication | 2026-11-07 |
| `medsl_dataverse.py` | MIT Election Data and Science Lab, Harvard Dataverse | Senate 1976-2024; President by state 1976-2024 | CC0 1.0 | 2026-11-07 |
| `candidates_american_general_elections.py` | Cha, Kuriwaki and Snyder, *Candidates in American General Elections*, Dataverse doi:10.7910/DVN/DGDRDT, v4.1 (2026-02-15) | House, Senate, **governor** 2006-2024 (odd years too), hand-coded incumbency | CC0 1.0 | 2026-11-07 |
| `downballot_pres_by_cd.py` | The Downballot, presidential vote by congressional district (public Google Sheets, CSV export) and its statement of methodology | 2000-2024 presidential vote on the lines of each House election 2006-2024 | none printed | 2026-11-07 |
| `fec_ballot_candidates.py` | FEC, 2024 general election ballot candidates | who sat in Congress in 2024 | none printed; federal record | 2026-11-07 |
| `nara_electoral_college.py` | National Archives, Electoral College results pages | president and VP elected, 1976-2024 | federal record | 2026-11-07 |
| `census_acs_population.py` | Census Bureau, ACS 1-year, table B01003 (www2.census.gov table files; the Census API now wants a key) | population of each state and district, 2022 and 2024 | federal record | 2026-11-07 |
| `build_congress.py` | the caches above | builds `data/senate|house|governor/<year>.json` | | |

Not reachable or not taken: 538's forecast files (they redirect to ABC News and archive.org is refused, so no published Senate, House or governor forecast has been read); MEDSL's House file (behind a Dataverse guestbook asking a name and email, the maker's call, law 10). The full inventory is `data/sources/congress.md`.

## 2. The model's own forecast (method D2-v1, approved by the orchestrator 2026-11-07 03:46 UTC)

**Why one is needed.** No forecaster's published forecast for these races is reachable here (§1), so the model builds its own "from what was known before the election" by regression on like past races (model §3, "Which forecast"), as Gelman, King and Boscardin did.

**The forecast.** For a race in year t, with y the Democrat's share of the two-party vote:

> y = ½ + a_t + b_lean × lean + b_inc × inc + e

- **lean**: the Democrat's two-party share of the last presidential vote held before year t, in the district on the lines in use in year t (House; The Downballot) or in the state (Senate, governor; MEDSL), minus the national share of that election (MEDSL).
- **inc**: +1 if a Democratic incumbent runs, −1 if a Republican one does, 0 for an open seat (Cha, Kuriwaki and Snyder).
- **a_t**: the year's national swing, shared by every race of that level that year. Before the election it is forecast from two facts known then, whether t is a midterm and the sitting president's party (National Archives): a_t = c₀ + c_mid·M·P + c_on·(1−M)·P + d, with P = +1 for a Democratic president.
- **e**: the race's own error, normal, independent across races given a_t.

The forecast for a race is normal with mean ½ + â_t + b_lean·lean + b_inc·inc and sd √(s_a² + s_e²), with a Student-t (4 degrees of freedom, same sd) alongside (model §9.5). s_a is the national forecast's root-mean-square miss over the ten cycles, each forecast from a fit on the other nine.

**Fitted** to every race both major parties contested in November 2006-2024 (`pipeline/chambers.py`; figures in `backtest.json`):

| Level | Races | b_lean | b_inc | s_e | s_a | sd | ρ = s_a²/sd² |
|---|---|---|---|---|---|---|---|
| House | 3,805 | 0.814 | 0.053 | 0.049 | 0.019 | 0.053 | 0.13 |
| Senate | 319 | 0.746 | 0.056 | 0.058 | 0.021 | 0.061 | 0.12 |
| Governor | 232 | 0.411 | 0.076 | 0.077 | 0.040 | 0.086 | 0.21 |

The national terms (House): c₀ = +0.016, c_mid = −0.031, c_on = −0.010. A midterm under a Democratic president is forecast at −1.5 points, under a Republican at +4.7.

**Back-test** (each cycle forecast from a fit on the other nine; normal forecast):

| Level | Coverage of the 50 / 80 / 95% intervals | Races finishing within 49-51%: expected, observed | Mean log score, normal / t4 |
|---|---|---|---|
| House | 53 / 82 / 94% | 124.8, 128 | 1.49 / 1.51 |
| Senate | 57 / 84 / 95% | 16.9, 21 | 1.35 / 1.39 |
| Governor | 61 / 80 / 96% | 14.9, 17 | 1.08 / 1.09 |

The count of races finishing within a point of even is the check that matters most for p, since p is about 25 × (chance of finishing within 49-51%) ÷ n (model §3). It is within Poisson noise at every level (House 125 expected, 128 seen). The t4 scores better on log score and worse on central coverage (43% inside its 50% interval for the House), so the truth lies between the two tails, as the model expects to show both.

**Seats.** The forecast distribution of the Democrats' seats among contested races, by exact dynamic programming over seats with the common swing, against the seats won: the House result falls outside the 80% interval in 2 of 10 cycles (2008, more Democratic; 2020, less), the Senate's in 2 of 10 (2008, 2012), as an 80% interval should about twice in ten.

**Tested and not adopted.** An error spread that grows as a race is expected to be closer (the residuals are wider there: 0.066 for House races forecast within 3 points, against 0.045 for those 15-25 points out). It improved central coverage but lowered the expected count within 49-51% to 118 against 128 seen, and scored worse for the Senate and governors, so the simpler constant spread is proposed. A forecast from the earlier cycles only (an expanding window, possible from 2014) gives intervals too wide in its early years, because three or four cycles cannot pin down the national terms.

**Marked, at the orchestrator's word of 03:46.**
- *Leaving one cycle out is an orchestrator choice the maker may correct.* The inputs of a year's forecast are all from before the election; its coefficients come partly from later cycles that no voter then had. Every forecast block says "the model's own" and names the method's version (`D2-v1`).
- *No polls are used*, so the forecast carries less than forecasters then knew. A lead for a later version: fivethirtyeight/data's `pollster-ratings` folder holds a raw polls file.
- *A reachable published forecast comes first* (model §3), with ours beside it as the check. Checked once, 2026-11-07 03:48 UTC: fivethirtyeight/data's `house-forecast-2018`, `senate-forecast-2018` and `governors-forecast-2018` folders hold only READMEs. Their data files are at projects.fivethirtyeight.com, which now redirects to abcnews.com (HTTP 200, an ABC page), and `election-forecasts-2018` does not exist (404). fivethirtyeight/data's `forecast-review` file (raw.githubusercontent.com, CC BY 4.0) gives 538's final 2018 win probabilities by race but no vote-share distribution, so it cannot give p. It will be the check beside our 2018 forecasts.

## 3. Structures, and where p is not computed

- **Uncontested** (one candidate on the ballot): p = 0, said so.
- **No Democrat or no Republican among the top two** (an independent or a minor party second, as Utah's Senate race of 2022, Nebraska's of 2024, Maine and Vermont's independents): not computed, since the forecast is fitted to Democrat-against-Republican races. Two candidates of one party (California and Washington top-two): not computed.
- **Georgia** (a majority is required, else a runoff): a race with three or more candidates is not computed; with two candidates the November count decides as a two-way race. **Louisiana**'s open primary on Election Day (2022 and 2024): not computed. **Maine and Alaska ranked-choice**: not computed. **Vermont governor** (the legislature chooses if no one has a majority): not computed when a third candidate is on the ballot. The result is recorded in every case.
- **Missing district input**: no 2020 presidential vote on the 2024 lines in Alabama, Louisiana and North Carolina (27 districts); 2008 on California's 2012 lines (53); 2012 on Florida's 2016 lines (27). Not computed for those seats until a source is found.

## 4. Control of the chamber (exact form, MATH §4.2)

**How each seat enters control** (`stage_two.inputs.entered_as`):
- *model*: the seat's own forecast, sharing the common swing.
- *inferred*: a structure whose p is not computed, entered as the model's two-way forecast of the Democrat (or the independent who caucuses with them) against the Republican. Marked. This covers Georgia with three or more candidates, Louisiana's open primary (party lean and incumbency), ranked-choice races in Maine and Alaska, and King and Sanders. It also covers the seats with no earlier presidential vote on their lines (AL, LA and NC in 2024), which use the same day's presidential vote on those lines minus that day's national share, stated as same-day.
- *fixed*: settled by who was on the ballot, which was known before the election. A seat with only Democrats (or a caucusing independent) is fixed D. A seat with no Democrat and no caucusing independent is fixed not-D: same-party top-two races, a Republican against minor parties, Osborn (Nebraska 2024) and McMullin (Utah 2022), who said they would join neither caucus. Only the Democrats' count matters for control. No seat is ever fixed at its result.

**Seats not up** (Senate): each held by the winner of its latest election before the year (Cha, Kuriwaki and Snyder, runoffs included), counted by caucus. 2022: 36 D, 29 R. 2024: 28 D, 38 R. Both match the Senate's party divisions before the election less the seats up (117th: 50-50; 118th: 51 D-caucus, 49 R).

**The Vice President.** In 2022 the VP was Harris (D), so the Democrats needed 50. In 2024 the VP was elected the same day: P(D VP) = 0.5, marked provisional, until D1's published presidential win probability is in. Then it is used assumed independent of the Senate swing, marked inferred. How far it moves control: for Montana, the seat with the largest control p, P(decides | tie) is 0.084 at 0.5, 0.114 with a Democratic VP and 0.054 with a Republican one.

p(control) = p(seat) × P(the other seats leave control to this one | this seat tied), with the common swing conditioned on the tie: d | tie ~ N((½ − μ)·s_a²/sd², s_a²·s_e²/sd²). The distribution of the other seats is computed exactly by dynamic programming over seats on a grid of the swing. What decides control: the House at 218 of 435; the Senate at 51 seats, or 50 with the Vice President's vote, counting the seats not up that year and the independents who caucus with a party. The stage-two step uses the normal forecast for both tails.

## 5. Results so far (2024 and 2022)

| Year, level | Contests | p computed | p = 0 (one candidate) | not computed | largest p | largest p for control |
|---|---|---|---|---|---|---|
| 2024 Senate | 35 | 32 | 0 | 3 | Montana, 1 in 193,000 | Montana, 1 in 2.3 million |
| 2024 House | 435 | 373 | 13 | 49 | CA-22, 1 in 46,000 | CA-22, 1 in 1.2 million |
| 2024 governor | 11 | 10 | 0 | 1 | Delaware, 1 in 220,000 | none |
| 2022 Senate | 36 | 32 | 0 | 4 | New Hampshire, 1 in 275,000 | New Hampshire, 1 in 1.9 million |
| 2022 House | 436 | 390 | 13 | 33 | CA-13, 1 in 36,000 | CA-22, 1 in 1.5 million |
| 2022 governor | 36 | 33 | 0 | 3 | Rhode Island, 1 in 152,000 | none |

p is under the normal forecast; the t4 figure sits beside it in `p.alongside`.

**Historical check** (MATH §8.2 iv). The sum of the event probabilities over a set of contests is the expected number of contests decided by a tie or one vote. For the 2024 House it is 0.0012 and for the 2022 House 0.0021, with no such contest seen in either. The Senate and governors' sums are smaller still. That is inside the Poisson interval of a count of zero, and it says little alone. The sharper check is the back-test's count of finishes within 49-51% (§2), which matches.

**Two sources, differences listed** (plan §3a). Every House and Senate contest is checked against Cha, Kuriwaki and Snyder, and the differences are kept in `checks`. Most are small candidates (under ten votes) or blank and write-in lines, which the check source leaves out by design. A few are real: 2022 IL-03, where the FEC has Delia Ramirez at 177,759 and the check source has 121,764; 2024 Missouri Senate, where W. C. Young has 35,671 in the Clerk's volume and 21,111 in the check source; and Indiana 2022, where the counts differ by a few hundred votes. The source of record (the FEC through 2022, the Clerk for 2024) wins. Governors have one standardized source here, so they are not checked.

**2026.** Not built: no standardized source holds its count yet (held 2026-11-03). Once one does, the files carry it marked as an unofficial count with its date, until it is certified.
