# Report D4: the cost of voting, how ballots are cast, and every state's tie and recount law

*By worker D4 (brief `briefs/D4-data-cost-and-ties.md`), 2026-11-07. Marks: [measured] read here from the source's own file; [stated] as a compilation or an agency guide says; [inferred] my arithmetic or reading; [vendor claim] a supplier's claim. Every figure below is in a file in `data/cost/` or `data/law/`, with its source block; the intake scripts are in `pipeline/intake/`. Nothing was bought; nothing behind a sign-up was filled in.*

## 1. The default, and how it compares with the states

**The site's default is $8.87: 14 minutes at $38.00 an hour** (`data/cost/national-default.json`). Its two inputs:

- **$38.00 an hour**: average hourly earnings of all private employees, series CES0500000003, October 2026, seasonally adjusted. Carried here by FRED (the St. Louis Fed), by the orchestrator's ruling, because the BLS public API stopped after its first batch of the day (limit of 25 requests) and BLS's flat-file and help pages answered HTTP 403. [stated, via FRED] FRED's value equals the BLS API's in all 3,000 series-months the one BLS batch gave (25 series: the national one and 23 states, 2007 to 2016, no difference). The October 2026 figure is not in that batch; the model (§6) read $38.00 from the BLS API and FRED prints the same.
- **14 minutes**: the median time at the polling place, Election Day 2016, from the smartphone study of Chen, Haggag, Pope and Rohla (model §6). [stated] **The authors' public file reproduces it**: over their 154,489 filtered waits the median is **13.57** minutes (rounds to 14), the mean **19.13** (the model's 19), and **17.9%** are over 30 minutes (the paper's 18%) [measured: `chen-waits.json`, `national_all_filtered_waits`].

**State figures, where they are measured** (`data/cost/by-state.json`; the table in §4):

- **Time at the polling place, 2016 (Chen et al., 46 states and DC; not AK, CO, HI, OR, WA).** State medians run from 8.4 minutes (Delaware) to 21.1 (Utah); state means from 11.9 (Delaware) to 27.9 (Utah). At each state's own latest hourly earnings, the cost of the median wait runs from **$4.77 (Delaware) to $18.93 (District of Columbia)**; the middle state is **$7.69**; **32 of the 46 are below $8.87**. [inferred: median minutes x the state's wage / 60]
- **Why the default sits above most states' own figure.** The $38.00 is the national wage; 37 of the 51 states' latest wages are lower (state range **$29.36 in Mississippi to $57.86 in the District of Columbia**, middle state $34.62). The state series are not seasonally adjusted and the national one is, so the two are not exactly alike. The minutes alone say the default is about right: the national median is 13.6 and the national mean 19.1.
- **Time in line, SPAE (MIT's survey, 2008 to 2022; 2024 is gated).** State means of the answers at their category midpoints run, among states with at least 60 answers, from **2.6 to 12.1 minutes in 2022** (middle state 5.8) and **6.5 to 39.6 in 2020** (middle state 15.7). [inferred: the survey gives five categories, not minutes] SPAE asks the line only (not the time voting takes) of in-person voters, early and Election Day, from about 200 voters per state; ten states are thin in 2020 and eight in 2022. It is lower than Chen's time at the polling place, as it should be, and it moves a good deal from year to year in one state (Georgia: 33.6 minutes in 2008, 7.7 in 2014, 25.1 in 2020, 11.1 in 2022).
- **So:** the measured state figures bracket the default. At the median wait the 46 states' costs fall between $4.77 and $18.93; at the mean wait, between $6.77 and $26.51 (Chen's means, at each state's wage) [inferred]. The default is close to the national median and mean of the same study.

**What no source here measures:** travel to the polling place, registering, learning about the contest, or any cost beyond the minutes valued at the average wage. SPAE's line is stated, not timed; Chen's time is the phone's dwell time inside a 60-metre circle (it includes the time spent voting), for Election Day voters only, in one election.

**The mail case.** A mail ballot has no trip and no line. Share of ballots cast by mail (`eavs-mode.json`, `cps-voting.json`):

| | 2016 | 2018 | 2020 | 2022 | 2024 |
|---|---|---|---|---|---|
| EAVS, by mail (administrative; states with usable shares) | 19% | 26% | 43% | 32% | 31% |
| EAVS, early in person | 22% | 17% | 26% | 19% | 33% |
| EAVS, Election Day (and provisional) | 58% | 57% | 30% | 46% | 36% |
| share of the nation's ballots those states hold | 76% | 93% | 100% | 96% | 90% |
| CPS (self-reported), by mail | | | 43% | 32% | 29% |
| CPS, early in person | | | 26% | 18% | 31% |
| CPS, Election Day | | | 31% | 50% | 40% |

Four states had nearly every ballot cast by mail in 2024 (EAVS, mail 90% or more: Colorado, Hawaii, Oregon, Washington; the CPS has Utah at 83% as well). [measured; the shares are [inferred] from the survey items.]

**EAVS has gaps, and they are shown, not filled.** Some states left a mode blank (Connecticut 2024 left Election Day blank in all 169 towns; Alabama, Iowa, Utah and Vermont gave no modes in some years; Indiana's 2024 modes add to 147% of its total and Oregon's 2016 to 200%, as if ballots were counted under two modes). A jurisdiction's shares are used only if its modes add to its total within 3%; a state with less than 80% of its ballots in such jurisdictions has no shares (`shares_withheld`): 10 states in 2016, 5 in 2018, none in 2020, 2 in 2022, 7 in 2024. [inferred: my rule]

## 2. What each source gives

| Source (script) | Gives | Measured or not | Checked against |
|---|---|---|---|
| EAVS 2016 to 2024, Section F1 (`eavs.py`) | ballots counted by mode in every election jurisdiction, so by state and year | [measured] the jurisdictions' reports; gaps flagged | the EAC's printed national total of voters: equal in 2018, 2020, 2022, 2024; 3,156 ballots (0.002%) higher in the 2016 file than the 2016 report prints |
| SPAE 2008 to 2022 (`spae.py`) | for each state: share of voters who waited not at all, under 10, 10 to 30, 31 to 60, over 60 minutes; how they voted | [measured] self-reports; the minutes are [inferred] (midpoints) | Stewart's published 2012 state averages (as `spae.py` notes); 2024 is gated (the maker's call) |
| Chen et al. replication (`chen_waits.py`) | mean, median, spread and share over 30 minutes of the time at polling places, by state, 2016 | [measured] by phone location; includes voting time; Election Day only | the archive's sample size, 154,489, equal in the state, county and individual files; the paper's mean, median, and share over 30 minutes (§1) |
| CPS November Voting Supplement 2020 to 2024 (`cps_voting.py`) | whether citizens say they voted, in person or by mail, on or before Election Day, by state | [measured] self-reports (known to over-report voting); shares [inferred] | the answer counts in the technical documentation (equal for all three years); an independent recomputation of 2020's national shares |
| BLS average hourly earnings via FRED (`bls_earnings.py`) | national and 51 state series, monthly, 2007 to 2026 | [stated] second-hand (FRED); origin BLS | 3,000 series-months from the BLS API: no difference |
| `cost_assemble.py` | the above side by side; the cost of each basis as minutes x wage / 60 | [inferred] arithmetic | |

## 3. Refusals and gaps (for the orchestrator)

- **BLS**: `download.bls.gov` and the `bls.gov` help pages answered HTTP 403 to curl; the public API v1 stopped at its daily limit after one batch. The v2 key needs an email address: not done. After the limit resets, `python3 pipeline/intake/bls_earnings.py --bls` reads the next batch and extends the check, including October 2026.
- **SPAE 2024** needs a Dataverse guestbook (name and email): the maker's call. Until then the latest SPAE is 2022.
- **CPS 2016 and 2018, EAVS 2004 to 2014** are in other layouts and were not taken; **CPS replicate weights** were not used (the standard errors in `cps-voting.json` are design-naive floors).
- **Chen et al.** lack Alaska, Colorado, Hawaii, Oregon, Washington.

## 4. The tie and recount law

Every state's rule for a tie and a recount, each with the statute's own words checked by script, is in `data/law/ties.json` and `data/law/recounts.json`, and the report on it is `data/law/REPORT.md` (the pull request for the law).
