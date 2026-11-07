# State legislatures, primaries, local races and measures: sources, method and checks

*Worker D3, `briefs/D3-data-local.md`. First written 2026-11-07 05:10 UTC; method and figures brought to D3-v1.1 at 05:50, and the review points of 05:17 fixed at 06:10; MEDSL's 2022 and 2024 returns added at 07:10 (§6). Marks: [measured] computed here from the files; [stated] as the source says; [inferred] my reading. The inventory of every source found is `data/sources/local.md`.*

**State at this writing.** Every state legislative contest of 1967-2022 that Klarner's dataset holds is in `data/state-upper/`, `data/state-lower/` and `data/primary/`: 189,103 contests. Each has p, p = 0 with the reason, or the reason p is not computed. The forecast method is D3-v1.1: D3-v1 as proposed, approved by the orchestrator at 05:06 with one change (each year fitted on earlier years only), and with runoffs added at its word. **MEDSL's precinct returns of 2022 and 2024** add 30,410 contests (§6): the state legislatures of 2024, 3,616 of them with p; local races and the states' other offices, 20,152; and 4,944 ballot measures, recorded with p not yet computed.

## 1. Sources taken in by script

| Source | Script | What it gives | Checks [measured] |
|---|---|---|---|
| Carl Klarner, *State Legislative Election Returns, 1967-2022*, Harvard Dataverse doi:10.7910/DVN/FJOGJB, v1.0 (2024-06-12), CC0 1.0 | `pipeline/intake/klarner_state_legislative.py` | 418,894 candidate rows into 189,103 contests: 158,537 regular generals, 27,359 primaries (first rounds and runoffs included), and 3,207 others (Louisiana's two rounds, specials, top-two primaries) | rows read: 418,894, as the record says. Democratic and Republican totals against Klarner's own contest file: 15 of 151,769 contests differ. In most, the contest file has 0 for a party to which the candidate file gives a few votes; one differs by 604 votes (Illinois House 38, 1968). All are listed in the cache's `checks.json`. Candidates against Klarner's candidate-contest file: 16 of 307,892 differ. Winners per chamber and year against Klarner's seats-up file: 7 of 2,512 differ, each with one or two winners fewer than the seats up (likely ties or unfilled seats [inferred]). Klarner's `ovote` is 0 in 9,061 contests where its candidate file lists non-major candidates with votes, so it is not used as a check |
| MIT Election Data and Science Lab, *Precinct-Level Returns 2024 by Individual State*, Harvard Dataverse doi:10.7910/DVN/NYTPDU, v1.0, CC0 1.0 | `pipeline/intake/medsl_precinct.py`, then `pipeline/local_medsl.py` | 51 files, 18,383,653 rows, into 29,910 contests of every office below Congress | rows read match Dataverse's count in all 45 files it counts. The same files' presidential totals against D1's certified ones: 27 states exact, 47 within 0.2%; Indiana +5.2%, Louisiana −48.9%, New Jersey +14.4% (all three named in MEDSL's README), held back; Maine −1.2%, MEDSL's first-round counts (its README), kept |
| MEDSL, *Precinct-Level Returns 2022 by Individual State*, doi:10.7910/DVN/UYQIEP, v5.0, CC0 1.0 | the same scripts | 51 files, 12,310,863 rows, into 5,782 contests. For AR, AZ, ID, IN, MD, MI, ND and WA it holds only a local file; their state offices are in MEDSL's OAARCY set, not yet taken | rows match Dataverse's count in all 46 files it counts. State legislatures against Klarner's 2022 returns: §6 |
| National Archives, Electoral College results 1964-2020 | `pipeline/intake/nara_electoral_college.py` (D2's) | the sitting president's party in each year | the winner's electoral votes reach the majority |

Klarner compiles the states' official returns, from their websites when collected and from the earlier ICPSR editions. It does not name the origin of each race, or say whether a count is before or after a recount. So every result is marked `stated`, with `via` the dataset, and `certified` is left out (null).

**Held back as likely incomplete in the source** [measured]: 10 contests whose count is under 5% (generals) or 2% (primaries) of the median of the chamber's like contests that year. Examples are Montana House 43 in 1974 (25 votes, against a median of 2,329) and Delaware House 14's 2014 Democratic primary (4 votes). They would otherwise carry the largest p of all. Their p is not computed, and they are marked for a second source.

## 2. The model's own forecast, method D3-v1.1

No forecaster published a forecast for any race at these levels (model §4). Each route is chosen by what is known before the election: who is on the ballot, the seat's past and incumbency. It is never chosen by who finished in the first two. **Every year is forecast from a fit on earlier years only**: a coefficient fitted partly on later years is something no voter knew (the orchestrator, 05:06; MODEL §3, "Which forecast").

**(a) Partisan**: a single-seat general with one Democrat and one Republican on the ballot. The Democrat's two-party share is

> y = ½ + a_t + b·x + g + e

- **x**, by class:
  - **A**: the seat's last result was contested. Inputs: its Democratic share − ½, incumbency and the chamber's lean.
  - **B**: the last result was unopposed. Inputs: which party won it, incumbency and lean.
  - **C**: there is no last result on these lines, after redistricting. Inputs: incumbency and lean.
  - Incumbency is +1, −1 or 0 (Klarner's `inc`). The chamber's lean is the mean Democratic share of the same chamber's contested seats at its previous election, minus ½.
- **a_t**, the year's swing, is forecast from the kind of year (presidential, midterm, odd) and the sitting president's party, as D2-v1 does.
- **g** is the state-and-chamber's own swing that year. **e** is the race's own error, with its sd by class and size.
- The forecast is normal with sd = √(s_a² + s_g² + s_e²). A Student-t with 4 degrees of freedom and the same sd sits beside it.
- **The fewest earlier years: 3 of the same kind** (presidential, midterm, odd). This is read off the back-test below: with 2, the 95% interval held only 92%. So route (a) starts in 1980 for presidential years, 1982 for midterms and 1975 for odd years. Earlier years are not computed, with that reason.

For reference, the fit on all years [measured]. Each year's own fit, on its earlier years, differs.

| Class | races | last result | incumbency | lean | s_e by size (under 3k, 3-10k, 10-30k, 30k+ two-party votes) |
|---|---|---|---|---|---|
| A | 49,001 | 0.752 × (last − ½) | 0.034 | 0.038 | 0.083, 0.074, 0.067, 0.061 |
| B | 14,350 | 0.108 × (±1) | 0.049 | 0.358 | 0.109, 0.101, 0.098, 0.094 |
| C | 27,602 | none | 0.118 | 0.375 | 0.111, 0.105, 0.108, 0.109 |

Swing [measured], as a change in the president's party's share: −2.4 points in a midterm, −1.0 in an odd year and +0.4 in a presidential year; s_a = 0.027 and s_g = 0.027.

**(b) Like past races** (Mulligan & Hunter's route, read through the model's own lay form, model §3). This route covers primaries, nonpartisan races and races without one D and one R.
- q is the share of the same class's races in earlier years whose leading two finished between 49% and 51% of their combined vote. Then f(½) = 50 q and p = 25 q ÷ n.
- Classes use facts known before the election: the kind of race, and for primaries the number of candidates and whether an incumbent runs.
- Where fewer than 10 like races fall in the window, it widens to 48-52%, then 45-55%. With fewer than 100 like races in earlier years, p is not computed.

**(c) Boundary**: a race that fills k seats at once is decided between the last winner and the first loser (model §7). Route (b) is applied to that pair, with classes by k and by whether both parties ran full slates. **Marked as the model's own and not yet checked**, for M2's second pass.

**(d) Runoffs** (the orchestrator, 05:06): a runoff's second round is its own two-way race. Route (b) is applied to like past runoffs, in four classes:
- kind: after a party primary, or after an open or general first round (Louisiana; Georgia's general runoffs);
- crossed with how far ahead the first round's leader of the two finished in the first round: within 10 points, or 10 points or more. This is known before the second round.

The first round stays not computed, since a vote there works through who advances (model §7).

**p is computed only between the pair that decided** (model §7; the orchestrator's review of 05:17). Where the two leading candidates of a route-(a) race are not the Democrat and the Republican, the forecast is not of the deciding pair, so p is not computed there, with that reason. The same holds where a write-in candidate, or the source's "scattering" (write-in votes counted together), is in the deciding pair of any route. A race with one name on the ballot for each seat has p = 0, unless a write-in candidate received at least 10% of the last winner's votes; then p is not computed, since no route covers write-in contests.

## 3. Back-test (`data/local/backtest.json`): each year forecast from earlier years only [measured]

**Route (a), by the number of earlier years of the same kind the fit had.** The minimum of 3 is chosen from this table.

| Earlier years | races | in 50 / 80 / 95% intervals | 49-51%: expected, seen | within 100 votes: expected, seen | margin 0 or 1: expected, seen |
|---|---|---|---|---|---|
| 1 | 6,118 | 51 / 80 / 94% | 319, 316 | 183, 175 | 2.9, 0 |
| 2 | 6,129 | 47 / 76 / 92% | 275, 282 | 152, 172 | 2.3, 2 |
| 3 | 6,325 | 52 / 81 / 95% | 294, 312 | 148, 167 | 2.3, 4 |
| 4 | 6,284 | 52 / 82 / 96% | 263, 270 | 137, 161 | 2.1, 0 |
| 5 | 6,384 | 55 / 83 / 95% | 239, 291 | 130, 166 | 2.0, 0 |
| 6-9 | 26,379 | 55 / 84 / 96% | 1,166, 1,180 | 589, 661 | 8.9, 8 |
| 10 or more | 27,184 | 58 / 86 / 96% | 1,199, 1,210 | 478, 518 | 7.2, 10 |

**Route (a), the years computed (3 or more earlier years)**: 72,556 races, 1975-2022.

| Two-party votes | races | in 50 / 80 / 95% intervals | 49-51%: expected, seen | within 10 votes | margin 0 or 1 |
|---|---|---|---|---|---|
| under 3,000 | 2,566 | 55 / 85 / 96% | 118, 141 | 31.6, 26 | 4.8, 8 |
| 3,000-10,000 | 17,505 | 54 / 83 / 96% | 785, 861 | 68.3, 78 | 10.3, 7 |
| 10,000-30,000 | 30,421 | 56 / 84 / 96% | 1,306, 1,337 | 39.5, 45 | 5.9, 7 |
| 30,000 and over | 22,064 | 57 / 85 / 96% | 952, 924 | 9.8, 8 | 1.5, 0 |
| **all** | **72,556** | **56 / 84 / 96%** | **3,161, 3,263** | **149, 157** | **22.4, 22** |

- The intervals are a little wide (56/84/96% against 50/80/95%), so the forecast is a little under-confident.
- Close finishes are a little under-forecast: 3% fewer expected than seen within 49-51%, and 11% fewer within 100 votes (1,483 expected, 1,673 seen).
- Within 10 votes and at a margin of 0 or 1, the forecast matches what happened.
- Mean log score: normal 1.010, t4 1.009. The normal is kept, with t4 beside it.

**Routes (b), (c) and (d), from like races of earlier years**: 21,030 races. Within 49-51%: 1,853 expected, 1,807 seen. Within 10 votes: 192 expected, 193 seen. Margin 0 or 1: 27.9 expected, 26 seen. Of these, the 1,144 runoffs: within 49-51%, 126 expected and 125 seen; within 10 votes, 10.0 expected and 8 seen; margin 0 or 1, 1.4 expected and 1 seen. By class in `backtest.json`.

**Against the record (brief step 5).** Model §4 gives 52 of 109,093 contests (1968-2022) tied or one vote apart. The cache reproduces it exactly: 52 of 109,093 contested generals, 30 of them single-seat and 22 multi-seat [measured]. On the races the routes compute, the forecasts expect 50.3 margins of 0 or 1 and 48 happened.

**Points for M2.**
1. The race's own sd is chosen by the size bin of the count itself. The count is not known before the election, though the bins are coarse.
2. The boundary route (c) is not yet checked.
3. The back-test of route (a) includes the 278 races whose deciding pair was not D and R: it tests the forecast of the Democrat's two-party share, which they have too.
4. In route (b), very small primaries reach the largest p, for example about 1 in 25 in a 2014 New Hampshire House primary whose two leading candidates had 21 votes between them. This is the exact sum of pipeline/core.py at a density read off races of every size.

## 4. Where p is computed and where it is not [measured]

Of 189,103 contests:

- **p computed: 93,285**, in four routes:
  - (a) 72,273
  - (b) 10,993
  - (c) 8,875
  - (d) 1,144
- **p = 0: 66,534** with one name on the ballot for each seat, said so.
- **p not computed, with the reason in each contest:**
  - 18,395 partisan races in years with fewer than 3 earlier years of their kind;
  - 6,480 first rounds of two-round systems;
  - 2,594 races in classes with fewer than 100 like races in earlier years;
  - 816 primaries that nominate several at once;
  - 278 partisan races where the Democrat and the Republican were not the top two;
  - 182 unopposed races where a write-in candidate received at least 10% of the last winner's votes;
  - 173 specials and 47 special runoffs;
  - 121 races where the source does not report every candidate's votes;
  - 91 top-two primaries;
  - 12 races with a write-in candidate in the deciding pair, and 5 with the source's scattering there;
  - 10 runoffs for several seats;
  - 10 counts held back (§1);
  - 68 structures no route covers, and 2 election types not handled.

**Party codes.** Where Klarner gives a candidate's party only as a code, the code is put in words from its codebook (Appendix C): 1,282 candidates, 792 of them under 99997, "assumed non-major party because the election is fully contested". The code is kept in `party_code`, and each file lists the codebook's words for the codes it uses. Two codes, 1776 and 50005, are not in the codebook; those two candidates show `unknown`.

## 5. Size

The full build is 137.3 MB as plain compact JSON in 2,821 files [measured]: state-lower 94.4 MB, state-upper 27.5 MB, primary 15.4 MB. The largest file is 0.35 MB (New York's 2014 primaries).

The orchestrator ruled at 05:06: commit plain JSON if the pack grows under about 50 MB and no file is over 20 MB. Its reason: git compresses objects and stores a rerun as a delta. Measured in a scratch clone with `git gc` before and after committing the full build, `git count-objects -vH` showed size-pack going from 6.99 MiB to 21.94 MiB. The pack grows by 15.0 MiB, so the build is committed.

## 6. MEDSL's precinct returns, 2022 and 2024

**Reading the files** (`pipeline/intake/medsl_precinct.py`). Each file is read in place from the cache; a precinct's votes for a line are its TOTAL row where it has one, else the sum of its modes. Precincts join into contests on the candidates they share. What had to be fixed, each found in the output [measured]:
- **Lines that are not candidates**: CONTEST TOTAL, CAST VOTES, VOID, blank and invalid ballots, and New York City's ballot-count lines (PUBLIC COUNTER, ABSENTEE / MILITARY, AFFIDAVIT, FEDERAL), which had made New York's 2022 counts 32% too high. Write-in totals (WRITE-IN, SCATTER, ALL OTHERS) are kept but never ranked as candidates on the ballot.
- **One person, several lines**: New York's and Oregon's fusion candidates appear once per party line, and counties spell names differently (T O'Mara, Thomas Fellers O'Mara). A candidate's lines are added up, and kept in `lines`; a numbered legislative district also joins on surname and party, and New York's pieces filed without a district number join their district (18 in 2024).
- **Washington** files its legislature as local offices ("Legislative District 9 - State Representative Pos. 1"); they are read as the state house or senate, with the position.
- **Minnesota's DFL and North Dakota's Democratic-NPL** are filed as "other" in 2022; they are read as Democrats.
- Some files list every precinct of the state under an office with 0 votes; a contest is placed by the precincts that voted in it, and 35 contests with no vote anywhere are left out.

**Checks** [measured]:
- 2024: the presidential totals above. Indiana's, Louisiana's and New Jersey's contests are recorded with p not computed and the reason.
- 2022 state legislatures against Klarner's (`data/local/check-2022-medsl-klarner.json`), 4,130 single-member districts named alike in both: D and R votes identical in 3,426; the two-party share within 1 point in 574 more (counts scaled alike: New Hampshire's senate is exactly double in Klarner, Idaho's double in MEDSL); a major party's candidate in one source only in 94; the share more than 1 point apart in 36. The winner differs in 89. (Read again with the intake of §7, 9 Illinois districts the first reading had split now join, and Illinois falls under the line.) States where more than 10% of districts differ in share or parties (AR, IN, MI, WA, WY), and California, whose 2022 file has exactly 1,048,575 rows, a spreadsheet's limit, so it is likely cut short [inferred], are not used for last results or like races.
- The US House totals in the same files against D2's are kept in the checks file but not used: D2's state totals include blank-ballot lines in some states and its party words vary, so they do not compare line for line.

**Method**, D3-v1.1 unchanged:
- **State legislatures, 2024**: route (a) fitted on Klarner's races of 1967-2022 (earlier years only). The seat's last result is MEDSL's 2022 result where at least 80% of the district's 2024 precincts were in it in 2022; otherwise class C. Incumbency is matched by name against the 2022 winners and Klarner's of 2020-2022. Other structures take Klarner's like-race classes of earlier years (routes b and c). Alaska's races are counted by ranked choice (MEDSL's 2022 README), so p is not computed there; districts the source splits into several contests are held back (21).
- **Local races and the states' other offices** (courts, boards, statewide officers other than the governor, which plan §3 gives no level of their own: `office_scope: state`): classes by office type, partisanship, seats and candidates, from like races of earlier years in the sources taken in.
- **Measures**: recorded, with the yes share; p waits for the thresholds and a forecast route.

**The 2024 state legislative forecasts against what happened** (out of sample: fitted on 1967-2022) [measured], 3,032 partisan races: in the 50/80/95% intervals 60/86/96%; within 49-51%, 134.2 expected and 128 seen; within 100 votes, 42.7 expected and 42 seen. The forecasts leaned 2.3 points too Democratic on average, the year's swing. Class C carries 2,406 of them: precinct names change between the files, so the lines test finds unchanged lines for only 627 districts.

**Where p is computed**, and what would compute the rest: superseded by §7, which adds 2018 and 2020.

## 7. MEDSL's 2018 and 2020 returns, and p for local races

**Sources** [measured] (the orchestrator, 06:16: "check GitHub first... compare their files to the Dataverse sets"):
- **2018**: MEDSL's GitHub repository `MEDSL/2018-elections-official` at commit 42055b1, one zip per state (51). Each CSV inside is byte-identical, by MD5, to the file of the same name in the Dataverse set Precinct-Level Returns 2018 by Individual State (doi:10.7910/DVN/NVQYMG, CC0 1.0, behind guestbook 458): `medsl_precinct.py 2018 --compare-dataverse` reads the Dataverse's public file list (names, sizes, MD5) and downloads nothing from it. So the guestbook is not needed for 2018. Wisconsin's file is in MEDSL's older layout (no county codes, party groups or seat counts) and holds state offices only, which Klarner records; it is not read.
- **2020**: `MEDSL/2020-elections-official` at commit a450bb4, the commit before its files were deleted (2023-10-24) with a note that the official data are now on the Dataverse. Its local returns are read (one file, 33 states). No file of the Dataverse collection 2020_precincts has its name or MD5; the by-state set there (NT66Z3, version 8, 2026-03-02) may hold a later version of the same races, behind the guestbook. So 2020's local races are MEDSL's earlier release, and nothing in the file can check them: it holds no federal or legislative contest.
- Neither repository has a licence file; the Dataverse sets of the same years are CC0 1.0.
- **Intake fixes**: county codes are now always five digits (Alabama's 2022 file wrote 1001 for 01001). The US House vote is kept by county for the lean below.

**2018 legislatures against Klarner's** (`data/local/check-2018-medsl-klarner.json`) [measured], 4,130 single-member districts named alike: D and R votes identical in 3,785; the share within 1 point in 305 more; a major party's candidate in one source only in 27; the share more than 1 point apart in 13; the winner differs in 53. No state passes the 10% line, so none is held back. Klarner stays the record for 2018's legislatures; MEDSL's 2018 legislative contests are its check and are not written again.

**Local races between one Democrat and one Republican** (the orchestrator, 06:16: route (a)'s class-C terms "with the county's 2022 House share, marked 'transferred, not yet checked'... If its 50% interval holds under 40% or over 60%, do not compute"). The lean is the Democrats' two-party share of the US House vote in the race's counties at the previous general, minus ½, from MEDSL's own precincts. Missing, with the reason, where a county had a precinct whose ballot lacked a Democrat or a Republican, or the previous year's state is held back. Incumbency is not matched (0). The back-test (`data/local/backtest-local-partisan.json`), each year fitted on Klarner's races of earlier years only [measured]:

| year (lean from) | races with a lean | in 50 / 80 / 95% intervals | within 49-51%: expected, seen | within 100 votes: expected, seen | mean forecast minus outcome |
|---|---|---|---|---|---|
| 2024 (2022 House) | 953 of 1,401 | 51 / 81 / 96% | 58.8, 53 | 50.7, 43 | +3.0 points D |
| 2020 (2018 House) | 856 of 979 | 52 / 83 / 96% | 53.8, 49 | 46.1, 43 | +2.8 points D |

Both years are within the line, so p is computed: 947 races in 2024 and 848 in 2020 (2020's then fall to the calibration rule below). The intervals hold, but the forecasts lean about 3 points too Democratic, and slightly fewer races finished near ½ than forecast (about 10% fewer within 49-51%, 15% fewer within 100 votes in 2024), so these p are, if anything, a little high. By office, the 50% interval holds 44% for councils and boards (454 races in 2024) and 66-68% for clerks and judges. 2018 and 2022 have no previous House vote by county in the sources taken in (2016 is not read; 2020's file is local only), so their 2,038 such races are not computed, with that reason.

**Local like-race classes, now with earlier years** (`data/local/backtest-local-classes.json`) [measured]. Each year's classes come from the local races of earlier years only (2018 from none, 2020 from 2018, 2022 from 2018 and 2020, 2024 from 2018 to 2022). Out of sample, the classes forecast more close races than happened:

| year | contests with p | expected within the window | seen | seen over expected |
|---|---|---|---|---|
| 2024 | 2,066 | 270.6 | 202 | 0.75 |
| 2020 | 1,817 | 317.8 | 248 | 0.78 |

So an uncalibrated like-race p for a local race is about a third too high on average [measured, these two years]. Councils and boards (961 in 2024: 141.3 expected, 107 seen) and school boards (511: 77.5, 50) carry most of it. The same direction as the legislatures' recount zone (§4).

**Calibrated to earlier years' near-ties** (the orchestrator, 07:37: "(b), calibrated, fitted on earlier years only... Adopt it only if it improves that test"; `data/local/calibration-local.json`) [measured]. The factor is seen over expected near ½ in the fitting years' own out-of-sample forecasts: by office type where those years expected 30 or more near-½ races, else pooled over their races. p is multiplied by it (for like races, the class density at ½ is). A year with no earlier year to fit on has these p not computed, with that reason.

| route | factor for 2024 (fitted on 2020) | 2024 near ½: expected before, after, seen | deviance by office type, before → after | adopted |
|---|---|---|---|---|
| like races | councils and boards 0.82, school boards 0.74, the rest pooled 0.78 | 270.6, 213.8, 202 | 38.1 → 19.2 | yes |
| Democrat against Republican (transferred) | pooled 0.91 (no type had 30 expected) | 58.8, 53.5, 53 | 13.2 → 12.6 | yes |

Both improve the 2024 test, so both are adopted: 2024's 2,066 like-race p and 947 Democrat-against-Republican p are calibrated, with the factor and its fitting year on the forecast. 2020's have no earlier year with these forecasts (2018's races have none: no year before it is taken in), so its 1,817 like-race p and 848 Democrat-against-Republican p are now not computed, with that reason; their forecasts stay in the records, since they are what fits 2024's factor. The calibrated like-race count is still 6% above what happened (213.8 against 202), most of it in special districts (19.0 against 13).

**Where p is computed** [measured], 56,908 contests:
- State legislatures 2024, 5,314: unchanged from §6 (p for 3,616, 0 for 1,470, not computed for 228).
- Local races and state offices, 43,301:
  - 2024, 19,711: p computed for 3,013, all calibrated (2,066 like-race, 947 Democrat against Republican); p = 0 for 10,158 unopposed. Not computed: 2,036 seats not given, 2,027 in states held back, 1,239 classes with fewer than 100 like races, 499 specials, 357 lean missing, 280 unopposed with strong write-ins, 84 redacted, 18 others.
  - 2020, 8,965: p = 0 for 3,617. Not computed: 2,665 with forecasts but no earlier year to calibrate them on (1,817 like-race, 848 Democrat against Republican), 1,470 seats not given, 901 too few like races, 123 lean missing, 88 specials, 84 strong write-ins, 17 others.
  - 2022, 441: p = 0 for 135. Not computed: 192 Democrat against Republican with no lean, 74 too few like races, 24 held back, 16 others.
  - 2018, 14,184: p = 0 for 7,180. Not computed: 4,364 too few like races (no earlier year), 1,846 Democrat against Republican with no lean, 290 specials, 218 seats not given, 172 strong write-ins, 114 others.
- Measures, 8,293 (2018: 1,581; 2020: 1,768; 2022: 95; 2024: 4,849): p not computed yet (next).

**Size**: the data grow the repository's pack from 21.3 to 23.3 MiB (scratch clone, `git gc --aggressive`, `git count-objects -vH`); no file is over 20 MB.

**Still open**: measures (thresholds from state law, the like-past-measures route, MEDSL's 2016 measures); OAARCY for the 2022 legislatures of the eight states UYQIEP holds only as local files; 2020's state offices and legislatures (Klarner covers the legislatures; the rest sit behind the guestbook).
