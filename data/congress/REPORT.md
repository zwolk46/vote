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

Not reachable or not taken: 538's forecast files (they redirect to ABC News and archive.org is refused, so no published Senate, House or governor forecast has been read); MEDSL's House file (behind a Dataverse guestbook asking a name and email, the maker's call, law 10). The full inventory is `data/sources/congress.md`.

## 2. The model's own forecast (proposed; not yet used for any p)

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

**Tested and not adopted.** An error spread that grows as a race is expected to be closer (the residuals are wider there: 0.066 for House races forecast within 3 points, against 0.045 for those 15-25 points out). It improved central coverage but lowered the expected count within 49-51% to 118 against 128 seen, and scored worse for the Senate and governors, so the simpler constant spread is proposed. A forecast from the earlier cycles only (an expanding window, possible from 2014) gives intervals too wide in its early years, because three or four cycles cannot pin down the national terms; leaving one cycle out is proposed instead. Its coefficients for year t come partly from later cycles that no voter then had; its inputs are all from before the election.

## 3. Structures, and where p is not computed

- **Uncontested** (one candidate on the ballot): p = 0, said so.
- **No Democrat or no Republican among the top two** (an independent or a minor party second, as Utah's Senate race of 2022, Nebraska's of 2024, Maine and Vermont's independents): not computed, since the forecast is fitted to Democrat-against-Republican races. Two candidates of one party (California and Washington top-two): not computed.
- **Georgia** (a majority is required, else a runoff): a race with three or more candidates is not computed; with two candidates the November count decides as a two-way race. **Louisiana**'s open primary on Election Day (2022 and 2024): not computed. **Maine and Alaska ranked-choice**: not computed. **Vermont governor** (the legislature chooses if no one has a majority): not computed when a third candidate is on the ballot. The result is recorded in every case.
- **Missing district input**: no 2020 presidential vote on the 2024 lines in Alabama, Louisiana and North Carolina (27 districts); 2008 on California's 2012 lines (53); 2012 on Florida's 2016 lines (27). Not computed for those seats until a source is found.

## 4. Control of the chamber (exact form, MATH §4.2)

p(control) = p(seat) × P(the other seats leave control to this one | this seat tied), with the common swing conditioned on the tie: d | tie ~ N((½ − μ)·s_a²/sd², s_a²·s_e²/sd²). The distribution of the other seats is computed exactly by dynamic programming over seats on a grid of the swing. What decides control: the House at 218 of 435; the Senate at 51 seats, or 50 with the Vice President's vote, counting the seats not up that year and the independents who caucus with a party. The stage-two step uses the normal forecast for both tails.
