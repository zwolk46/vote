# Senate, House and governor: sources, method and checks

*Worker D2 (`briefs/D2-data-congress.md`, amended 2026-11-07 03:13 UTC). Written 2026-11-07. It covers every Senate, House and governor race of the even years 2006 to 2024 that the sources hold, with p, and control of the Senate and the House.*

## 1. Sources taken in by script

Each source is read by one script in `pipeline/intake/`. The script downloads to a cache outside the repository (`VOTE_CACHE`, default `/tmp/vote-cache`). It records the URL, read time, size and SHA-256 of every file, checks sums against the source's own totals, and normalizes. Rerunning any of them gives the same inputs.

| Script | Source | Covers | Licence | Read |
|---|---|---|---|---|
| `fec_federal_elections.py` | FEC, *Federal Elections* workbooks | House and Senate general results with incumbent marks, 2006-2022 | none printed; federal record | 2026-11-07 |
| `clerk_statistics.py` | Clerk of the House, *Statistics of the Presidential and Congressional Election* (PDF) | House and Senate, 2024 (the FEC has no 2024 congressional volume yet) | none printed; House publication | 2026-11-07 |
| `medsl_dataverse.py` | MIT Election Data and Science Lab, Harvard Dataverse | Senate 1976-2024; President by state 1976-2024 | CC0 1.0 | 2026-11-07 |
| `candidates_american_general_elections.py` | Cha, Kuriwaki and Snyder, *Candidates in American General Elections*, doi:10.7910/DVN/DGDRDT, v4.1 | House, Senate, **governor** 2006-2024 (odd years too), hand-coded incumbency | CC0 1.0 | 2026-11-07 |
| `downballot_pres_by_cd.py` | The Downballot, presidential vote by congressional district (public Google Sheets) | 2000-2024 presidential vote on the lines of each House election 2006-2024 | none printed | 2026-11-07 |
| `fec_ballot_candidates.py` | FEC, 2024 general election ballot candidates | who sat in Congress in 2024 | none printed; federal record | 2026-11-07 |
| `nara_electoral_college.py` | National Archives, Electoral College pages | president and VP elected, 1976-2024 | federal record | 2026-11-07 |
| `census_acs_population.py` | Census Bureau, ACS 1-year, table B01003 (www2.census.gov table files) | population of each state and district, 2022 and 2024 | federal record | 2026-11-07 |
| `party_divisions.py` | U.S. Senate, *Party Division*; House History, *Party Divisions of the House* | seats by party at the opening of each Congress, with the chambers' notes | none printed; chamber publications | 2026-11-07 |
| `fivethirtyeight_checking_our_work.py` | FiveThirtyEight, `checking-our-work-data` (raw.githubusercontent.com, commit f6d5b2e) | 538's published forecasts by race and day: Senate 2008-2022, House 2010 and 2018-2022, governors 2010, 2018, 2022 | CC BY 4.0 | 2026-11-07 |
| `build_congress.py` | the caches above | builds `data/senate|house|governor/<year>.json` | | |

**Source of record and check.** For 2006-2022 the FEC's volume is the record; for 2024 it is the Clerk's. Cha, Kuriwaki and Snyder check every House and Senate contest, and the differences are kept in `checks` (§6). Governors have one standardized source here (Cha), so they are not checked yet. MEDSL's state-office precinct files for 2022 and 2024 (CC0, no guestbook) are the lead for a check.

**Not taken.** MEDSL's House file sits behind a Dataverse guestbook that asks for a name and email; filling it is the maker's call (law 10). 538's own forecast pages redirect to abcnews.com. The full inventory is `data/sources/congress.md`.

## 2. The forecasts

### 2.1 538's published forecast, first where it can be used

The orchestrator's words of 03:46 put "a reachable published forecast" first, with ours as the check; the rules below are his of 04:12 and 04:20. 538's `checking-our-work-data` keeps every race it forecast, each day and each version, with the projected vote share and the chance of winning.

- **Which forecast.** The last one dated before Election Day, recorded as `as_of`. In 2008 and 2010 the file holds one forecast per race, dated Election Day, and it is marked so.
- **Which version.** 538 showed one version by default. No source read here names it: its pages redirect, and its data READMEs do not say. So the version listed first in the repository's rows comes first, and the others stand beside it in `forecasts`. That is *lite* in 2018-2022, *polls-plus* in 2016 and the only version in 2014. This is an orchestrator choice the maker may correct.
- **Mean and sd.** The mean is the Democrat's projected share of the two leading parties' projected vote. The sd is the one a normal needs to give 538's chance: sd = (mean − ½) ÷ Φ⁻¹(chance), marked inferred. 538's own distribution is not normal, so this sd is "the normal that agrees with 538's mean and chance", not 538's.
- **When it is used.** 538 comes first when the implied sd's estimated error is under 20%, no chance is exactly 0 or 1, and other candidates hold under 1% of the chance.
  - The error comes from two places. One is the chance's sampling error, √(q(1−q)/N). N is the number of simulation runs the chances step by: 50,000 in 2018, 40,000 in 2020 and 2022, 20,000 in 2016, marked inferred; 2014's chances have no step and are taken as exact. The other is the rounding of the printed shares.
  - The chance is moved one standard error either side and carried through Φ⁻¹ at both ends, not linearized. A chance one run from 0 or 1 is unbounded and falls back. D1 uses the same rule.
- **Otherwise** ours comes first, with 538's forecast beside it and the reason in `unusable` (a sentence) and `unusable_kind` (a short class).
- **Control of the chamber** stays the model's own, because 538's file gives no joint distribution. A seat whose p is 538's has control p = 538's seat p × the model's own P(the others leave control to it | it ties). Both parts are named in `p.control.under`.

| Level | Races with a 538 forecast | 538 first | Ours first: no share in the file (2008-2012 Senate; 2010) | chance 0 or 1 | sd error 20% or more | other |
|---|---|---|---|---|---|---|
| House | 1,566 | 1,008 | 400 | 111 | 45 | 2 |
| Senate | 251 | 154 | 94 | 0 | 2 | 1 |
| Governor | 99 | 66 | 32 | 0 | 1 | 0 |

The two "other" House cases are a 538 Democrat not on our ballot (South Carolina 5th, 2018, where 538 names April Freeman and the record has Archie Parnell) and one race with no Democrat or Republican in 538's rows.

### 2.2 The model's own forecast (method D2-v1, approved by the orchestrator 2026-11-07 03:46 UTC)

Used where no published forecast can be: every race of 2006, 2008, 2010 (House and governor), 2012, 2014 (House, governors), 2016 (House, governors), 2020 governors and 2024, and the fallbacks above. It is always kept beside 538's as the check. For a race in year t, with y the Democrat's share of the two-party vote:

> y = ½ + a_t + b_lean × lean + b_inc × inc + e

- **lean**: the Democrat's two-party share of the last presidential vote before year t, minus that election's national share (MEDSL). For the House it is taken on the lines in use in year t (The Downballot); for the Senate and governors, in the state (MEDSL). A House special is held on the old Congress's lines, so its lean is taken on the lines of t − 2. Pennsylvania's 7th and 15th specials of 2018 are the cases where this matters.
- **inc**: +1 if a Democratic incumbent runs, −1 if a Republican one does, 0 for an open seat (Cha, Kuriwaki and Snyder).
- **a_t**: the year's national swing. It is forecast from whether t is a midterm and from the sitting president's party (National Archives): a_t = c₀ + c_mid·M·P + c_on·(1−M)·P + d.
- **e**: the race's own error, independent across races given a_t.

The forecast is normal with sd √(s_a² + s_e²), with a Student-t (4 degrees of freedom, same sd) beside it. s_a is the national forecast's root-mean-square miss, each cycle forecast from a fit on the other nine.

| Level | Races fitted | b_lean | b_inc | s_e | s_a | sd | ρ = s_a²/sd² |
|---|---|---|---|---|---|---|---|
| House | 3,805 | 0.814 | 0.053 | 0.049 | 0.019 | 0.053 | 0.13 |
| Senate | 319 | 0.746 | 0.056 | 0.058 | 0.021 | 0.061 | 0.12 |
| Governor | 232 | 0.411 | 0.076 | 0.077 | 0.040 | 0.086 | 0.21 |

**Back-test**, each cycle forecast from a fit on the other nine (`backtest.json`):

| Level | 50 / 80 / 95% interval coverage | Races within 49-51%: expected, seen | Mean log score, normal / t4 |
|---|---|---|---|
| House | 53 / 82 / 94% | 124.8, 128 | 1.49 / 1.51 |
| Senate | 57 / 84 / 95% | 16.9, 21 | 1.35 / 1.39 |
| Governor | 61 / 80 / 96% | 14.9, 17 | 1.08 / 1.09 |

Seat totals fall outside their 80% interval in 2 of 10 cycles for the House (2008, 2020) and the Senate (2008, 2012). An error spread that grows as a race is closer was tested and not adopted. So was an expanding window, which runs too wide in its early years.

**Marked, at the orchestrator's word of 03:46.**
- *Leaving one cycle out is an orchestrator choice the maker may correct.* Every input is from before the election, but the coefficients come partly from later cycles.
- *No polls are used*, so the model's own forecast carries less than forecasters then knew. Where 538's forecast stands first, the polls are in.

**Found since the approval, not changed.**
- The fit takes 44 House specials with the year's own lines, not the old Congress's. Refitting without them moves b_lean from 0.814 to 0.812 and b_inc from 0.053 to 0.053, so D2-v1 is left as approved. The forecasts in the files use the old lines (above).
- The governors' forecast runs wide: see §5.

## 3. Structures, and where p is not computed

- **Uncontested** (one candidate on the ballot): p = 0, said so.
- **No Democrat or no Republican among the top two**: not computed, since both forecasts are of a Democrat against a Republican. This covers an independent or minor party second, and two candidates of one party (California and Washington top-two; Connecticut 2006, where Lieberman ran on a Democratic and a third-party line). An independent who caucuses with the Democrats (Sanders, King) stands as the Democrat, as in 538's rows.
- **Georgia** (a majority is required, else a runoff): not computed with three or more candidates. **Louisiana**'s open primary: not computed. **Ranked choice** in Maine (2018 on) and Alaska (2022 on): not computed. **Vermont governor**, which the legislature chooses if no one has a majority: not computed with a third candidate on the ballot. The result is recorded in every case, and 538's forecast is kept where it has one.
- **Missing district input**: no 2020 presidential vote on the 2024 lines in Alabama, Louisiana and North Carolina; none for 2008 on California's 2012 lines; none for 2012 on Florida's 2016 lines.
- **Specials held apart from November.** The November record leaves out specials held on other dates. Cha, Kuriwaki and Snyder hold 42 such House contests and Massachusetts's Senate special of January 2010. They are added with Cha as their record (`certified` null, with no second source) and p not computed, since both forecasts are of November's general election. Their dates are not in the sources read here, except Massachusetts's: 19 January 2010, from Senate.gov. Eight of 2024's are among them (CA-20, CO-04, NJ-10, NY-03, NY-26, OH-06, TX-18, WI-08). The FEC has no 2024 volume, so they come from Cha, as the orchestrator agreed for want of the FEC.

## 4. Control of the chamber (exact form, MATH §4.2)

p(control) = p(seat) × P(the other seats leave control to this one | this seat tied). The common swing is conditioned on the tie: d | tie ~ N((½ − μ)·s_a²/sd², s_a²·s_e²/sd²). The other seats' distribution is computed exactly, by dynamic programming over seats on a grid of the swing.

What decides control:
- **House:** 218 of 435.
- **Senate:** 51, or 50 with the Vice President, with the seats not up and the independents counted by caucus. A Senate special whose term ends when the new Senate meets (California 2022 and 2024; Illinois 2010, in Senate.gov's words) is not part of control.

**How each seat enters** (`stage_two.inputs.entered_as`):
- *model*: the model's own forecast, sharing the common swing.
- *inferred*: a structure whose p is not computed, entered as the model's two-way forecast. This covers Georgia's runoffs, Louisiana, and ranked choice (King in Maine from 2018 among them). Seats with no earlier presidential vote on their lines use the same day's presidential vote, stated as same-day.
- *fixed*: settled by who was on the ballot, known before the election. Only Democrats on the ballot is fixed D. No Democrat and no caucusing independent is fixed not-D: same-party top two, a Republican against minor parties, and Osborn and McMullin, who said they would join neither caucus. No seat is ever fixed at its result.

**Seats not up** (Senate): each is held by the winner of its latest election before the year, counted by caucus. Winners come from Cha, Kuriwaki and Snyder from 2006 on, runoffs included, and from MEDSL's Senate returns for seats last elected in 2002 and 2004. Each is listed in `chamber.seats_not_up_list`.

**The check on every chamber-year** (`chamber.check`): the seats not up plus the seats won, against the division the new Congress opened with (Senate.gov; House History). All 20 agree but two, and each of the two is a seat vacant at the opening:
- Minnesota's Senate seat in January 2009, contested; Franken (D) was seated in July. We count 59 against 56 + 2 independents + 1 vacant.
- New York's 22nd in January 2021, uncertified; Tenney (R) was seated in February. We count 213 R against 212.

**The Vice President.** In midterms it is the sitting one (Cheney R in 2006, Biden D in 2010 and 2014, Pence R in 2018, Harris D in 2022). In presidential years the VP is elected the same day:
- 2008, 2012, 2016 and 2020: 0.5, marked provisional.
- 2024: still 0.5 until D1's published presidential win probability is in. It will then be used, assumed independent of the Senate swing and marked inferred.

How far 0.5 moves control is shown in each seat's `P_decides_given_tie_if_VP_D` and `_if_VP_R`. For Montana 2024, P(decides | tie) is 0.084 at 0.5, 0.114 with a Democratic VP and 0.054 with a Republican.

## 5. Results

| Year, level | Contests | p computed | 538 first | p = 0 | not computed | largest p | largest p for control |
|---|---|---|---|---|---|---|---|
| 2006 Senate | 33 | 31 | 0 | 0 | 2 | North Dakota, 1 in 61,867 | North Dakota, 1 in 531,679 |
| 2006 House | 438 | 368 | 0 | 30 | 40 | New York 13, 1 in 31,970 | Texas 27, 1 in 2,959,652 |
| 2006 governor | 36 | 34 | 0 | 0 | 2 | Wyoming, 1 in 82,437 | |
| 2008 Senate | 35 | 31 | 0 | 0 | 4 | South Dakota, 1 in 112,640 | South Dakota, 1 in 1,802,442 |
| 2008 House | 443 | 370 | 0 | 24 | 49 | New York 13, 1 in 47,211 | Texas 27, 1 in 1,988,640 |
| 2008 governor | 11 | 10 | 0 | 0 | 1 | Delaware, 1 in 166,637 | |
| 2010 Senate | 39 | 32 | 0 | 1 | 6 | North Dakota, 1 in 124,645 | Delaware special, 1 in 7,690,243 |
| 2010 House | 441 | 402 | 0 | 10 | 29 | New York 13, 1 in 32,972 | New York 13, 1 in 1,203,963 |
| 2010 governor | 36 | 32 | 0 | 0 | 4 | Wyoming, 1 in 158,976 | |
| 2012 Senate | 33 | 33 | 0 | 0 | 0 | Montana, 1 in 144,641 | Montana, 1 in 1,016,834 |
| 2012 House | 441 | 344 | 0 | 10 | 87 | Illinois 8, 1 in 62,384 | West Virginia 3, 1 in 17,058,348 |
| 2012 governor | 11 | 10 | 0 | 0 | 1 | North Dakota, 1 in 163,273 | |
| 2014 Senate | 36 | 32 | 32 | 1 | 3 | Alaska, 1 in 29,075 | Alaska, 1 in 184,226 |
| 2014 House | 440 | 358 | 0 | 27 | 55 | California 21, 1 in 27,166 | California 21, 1 in 24,885,306 |
| 2014 governor | 35 | 33 | 0 | 0 | 2 | Rhode Island, 1 in 111,200 | |
| 2016 Senate | 34 | 30 | 29 | 0 | 4 | Nevada, 1 in 116,767 | Nevada, 1 in 1,877,279 |
| 2016 House | 439 | 344 | 0 | 22 | 73 | California 21, 1 in 36,709 | California 21, 1 in 5,287,726 |
| 2016 governor | 12 | 11 | 0 | 0 | 1 | Delaware, 1 in 178,840 | |
| 2018 Senate | 35 | 32 | 32 | 0 | 3 | Montana, 1 in 95,378 | North Dakota, 1 in 1,093,472 |
| 2018 House | 442 | 383 | 318 | 15 | 44 | New Mexico 2, 1 in 33,197 | California 21, 1 in 1,019,350 |
| 2018 governor | 36 | 34 | 34 | 0 | 2 | South Dakota, 1 in 59,093 | |
| 2020 Senate | 35 | 30 | 29 | 0 | 5 | Alaska, 1 in 87,769 | Alaska, 1 in 552,027 |
| 2020 House | 440 | 398 | 332 | 10 | 32 | Oklahoma 5, 1 in 49,402 | California 21, 1 in 4,823,776 |
| 2020 governor | 11 | 11 | 0 | 0 | 0 | Montana, 1 in 258,029 | |
| 2022 Senate | 36 | 32 | 32 | 0 | 4 | New Hampshire, 1 in 95,630 | New Hampshire, 1 in 662,445 |
| 2022 House | 444 | 390 | 358 | 15 | 39 | New Hampshire 1, 1 in 20,079 | California 22, 1 in 974,126 |
| 2022 governor | 36 | 33 | 32 | 0 | 3 | Nevada, 1 in 134,250 | |
| 2024 Senate | 35 | 33 | 0 | 0 | 2 | Montana, 1 in 193,072 | Montana, 1 in 2,294,762 |
| 2024 House | 443 | 373 | 0 | 13 | 57 | California 22, 1 in 46,024 | California 22, 1 in 1,164,456 |
| 2024 governor | 11 | 10 | 0 | 0 | 1 | Delaware, 1 in 219,725 | |

In all: 4,997 contests, 4,264 with p computed (1,228 of them under 538's forecast), 178 with p = 0, and 555 not computed, each with its reason. p is under the normal forecast. The t4 figure and the other forecasts' figures sit beside it in `p.alongside`, each with its own `control`.

### Historical check (MATH §8.2 iv), 2006-2024

Over all contests with p, the expected number decided by k votes or fewer is computed under the forecast each p used, and set against the number seen (`chambers.py history`, `history.json`). k = 1 is the event itself. Larger k test the same forecasts where there are cases to count.

| Level | Contests | within 1 vote | within 10 | within 100 | within 1,000 | within 5,000 |
|---|---|---|---|---|---|---|
| House | 3,730 | 0.027 vs 0 | 0.27 vs 1 | 2.7 vs 2 | 27.3 vs 30 | 136.7 vs 126 |
| Senate | 316 | 0.001 vs 0 | 0.009 vs 0 | 0.09 vs 0 | 0.93 vs 1 | 4.7 vs 5 |
| Governor | 218 | 0.001 vs 0 | 0.009 vs 0 | 0.09 vs 0 | 0.88 vs 0 | 4.4 vs 0 |

- **House and Senate.** The forecasts pass at every k. The one House race within ten votes is Iowa's 2nd of 2020, at 6 votes. The Senate race within 1,000 is Minnesota 2008, at 312.
- **Governors.** No race in 2006-2024 finished within 5,000 votes, against 4.4 expected. A count of 0 has a chance of 1.3% under the forecasts, so the governors' p are likely too high. The governor back-test points the same way: 61% of races fell inside the 50% interval.
  - The likely cause is the model's own forecast (sd 0.086) running too wide in the middle, since 538 is first in only 66 of 218 governor races.
  - The method is approved, so it is not changed here. A governor-only fix, such as a separate national term or the heteroskedastic spread, is for the orchestrator to weigh.

## 6. Two sources, differences listed (plan §3a)

Every House and Senate contest in the record is checked against Cha, Kuriwaki and Snyder, and the differences are kept in `checks`. The source of record wins.
- **Most differences** are small candidates (under ten votes) and blank or write-in lines, which the check source leaves out by design.
- **Real ones**: 2022 IL-03 (Ramirez 177,759 at the FEC, 121,764 in the check), 2024 Missouri Senate (W. C. Young 35,671 at the Clerk, 21,111 in the check), and 2012 AL-03 (Harris 98,141 at the FEC, 91,141 in the check).
- **Fixed in the record's reading**:
  - A fusion candidate's lines filed under two FEC ids are one candidate's. Connecticut's Senate race of 2010 is the case: Blumenthal's Democratic and Working Families lines now sum to 636,040, as the check has. Each merge is noted in the contest.
  - FEC rows with no candidate are not contests: a "California" row in 2018, and two Ohio rows in 2006.

## 7. Not yet

- **Population before 2022.** The ACS table-based files on www2.census.gov begin with 2021. The older sequence-based summary files there hold the same table and are the next step. The Census API wants a key, which needs an email, so it is not used.
- **A second source for governors** (MEDSL precinct files, 2016, 2022 and 2024).
- **Odd-year governors** (Virginia, New Jersey, Kentucky, Louisiana, Mississippi), which are in Cha.
- **Earlier than 2006.** For the Senate this needs MEDSL from 1976 (`medsl_dataverse.py` already reads it). For governors it needs Algara and Amlani, Klarner or Kaplan. The Downballot's district presidential vote reaches back to 2000 on the lines of 2002.
- **2026.** Not built: no standardized source holds its count yet (held 2026-11-03). Once one does, the files carry it marked as an unofficial count with its date, until it is certified.
