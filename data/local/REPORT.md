# State legislatures, primaries, local races and measures: sources, method and checks

*Worker D3, `briefs/D3-data-local.md`. First written 2026-11-07 05:10 UTC; method and figures brought to D3-v1.1 at 05:50, and the review points of 05:17 fixed at 06:10; MEDSL's 2022 and 2024 returns added at 06:14 (§6), their 2018 and 2020 returns and local p at 06:36 (§7), measures with their thresholds and MEDSL's 2016 questions at 07:25 (§8), and North Carolina's State Board of Elections, every date from 2000, at 08:00 (§9). Marks: [measured] computed here from the files; [stated] as the source says; [inferred] my reading. The inventory of every source found is `data/sources/local.md`.*

**State at this writing.** Every state legislative contest of 1967-2022 that Klarner's dataset holds is in `data/state-upper/`, `data/state-lower/` and `data/primary/`: 189,103 contests. Each has p, p = 0 with the reason, or the reason p is not computed. The forecast method is D3-v1.1: D3-v1 as proposed, approved by the orchestrator at 05:06 with one change (each year fitted on earlier years only), and with runoffs added at its word. **MEDSL's precinct returns of 2022 and 2024** add 30,410 contests (§6): the state legislatures of 2024, 3,616 of them with p; local races and the states' other offices, 20,152; and 4,944 ballot measures. §7 adds 2018 and 2020 and p for local races; §8 adds 2016's questions and p for statewide measures: 9,768 measures, 63 of them with p. §9 adds North Carolina's own certified files: 21,002 contests from 2000 to 2026, which also take the place of MEDSL's North Carolina contests on its dates. With them, D3's files hold 265,272 contests.

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
- **Measures**: see §8.

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
| 2024 | 2,066 | 271.1 | 202 | 0.75 |
| 2020 | 1,809 | 317.4 | 248 | 0.78 |

So an uncalibrated like-race p for a local race is about a third too high on average [measured, these two years]. Councils and boards (961 in 2024: 141.3 expected, 107 seen) and school boards (511: 77.7, 50) carry most of it. The same direction as the legislatures' recount zone (§4).

**Calibrated to earlier years' near-ties** (the orchestrator, 06:38: "(b), calibrated, fitted on earlier years only... Adopt it only if it improves that test"; `data/local/calibration-local.json`) [measured]. The factor is seen over expected near ½ in the fitting years' own out-of-sample forecasts: by office type where those years expected 30 or more near-½ races, else pooled over their races. p is multiplied by it (for like races, the class density at ½ is). A year with no earlier year to fit on has these p not computed, with that reason.

| route | factor for 2024 (fitted on 2020) | 2024 near ½: expected before, after, seen | deviance by office type, before → after | adopted |
|---|---|---|---|---|
| like races | councils and boards 0.82, school boards 0.75, the rest pooled 0.78 | 271.1, 214.7, 202 | 38.2 → 19.1 | yes |
| Democrat against Republican (transferred) | pooled 0.91 (no type had 30 expected) | 58.8, 53.5, 53 | 13.2 → 12.6 | yes |

Both improve the 2024 test, so both are adopted: 2024's 2,066 like-race p and 947 Democrat-against-Republican p are calibrated, with the factor and its fitting year on the forecast. 2020's have no earlier year with these forecasts (2018's races have none: no year before it is taken in), so its 1,809 like-race p and 848 Democrat-against-Republican p are now not computed, with that reason; their forecasts stay in the records, since they are what fits 2024's factor. The calibrated like-race count is still 6% above what happened (214.7 against 202), most of it in special districts (19.1 against 13).

*The figures of this section are from the rebuild of §8 (07:25), which moved 23 yes-or-no contests that MEDSL files as candidate races out of the local races (they are questions, §8) and dropped Michigan's 2022 rejected-ballot lines; against the build of 06:41 the like-race figures moved by under 1%.*

**Where p is computed** [measured], 58,360 contests with §8's measures:
- State legislatures 2024, 5,314: unchanged from §6 (p for 3,616, 0 for 1,470, not computed for 228).
- Local races and state offices, 43,278:
  - 2024, 19,704: p computed for 3,013, all calibrated (2,066 like-race, 947 Democrat against Republican); p = 0 for 10,158 unopposed. Not computed: 2,031 seats not given, 2,027 in states held back, 1,237 classes with fewer than 100 like races, 499 specials, 357 lean missing, 280 unopposed with strong write-ins, 84 redacted, 18 others.
  - 2020, 8,956: p = 0 for 3,617. Not computed: 2,657 with forecasts but no earlier year to calibrate them on (1,809 like-race, 848 Democrat against Republican), 1,470 seats not given, 901 too few like races, 123 lean missing, 88 specials, 84 strong write-ins, 17 others.
  - 2022, 441: p = 0 for 135. Not computed: 192 Democrat against Republican with no lean, 74 too few like races, 24 held back, 16 others.
  - 2018, 14,177: p = 0 for 7,180. Not computed: 4,357 too few like races (no earlier year), 1,846 Democrat against Republican with no lean, 290 specials, 218 seats not given, 172 strong write-ins, 114 others.
- Measures, 9,768 (2016: 1,513; 2018: 1,584; 2020: 1,777; 2022: 83; 2024: 4,811): p for 63 statewide measures (§8).

**Size**: the data grow the repository's pack from 21.3 to 23.3 MiB (scratch clone, `git gc --aggressive`, `git count-objects -vH`); no file is over 20 MB.

**Still open**: see §8 for measures. OAARCY is a check only (§8). 2020's state offices and legislatures (Klarner covers the legislatures; the rest sit behind the guestbook).

## 8. Ballot measures and retentions: thresholds from state law, and p for statewide measures

*Added 2026-11-07 07:25 UTC, at the orchestrator's ruling of 06:16: "Measures: approved, except local thresholds are never inferred. Read statewide thresholds from each constitution or statute, with URLs... Where it cannot be read, p is not computed, with that reason... The like-past-measures route is approved, marked as the model's own... Refit with 2016 added, report the calibration again, and say in REPORT.md if it still under-forecasts near ½."*

**Sources** [measured]. MEDSL's precinct returns as in §6 and §7, and for 2016 its older sets, read for their questions only (`pipeline/intake/medsl_precinct.py 2016`): State Precinct-Level Returns 2016 (doi:10.7910/DVN/GSZG1O), 335 questions, and Local Precinct-Level Returns 2016 (doi:10.7910/DVN/Q8OHRS), 1,178. Their offices are spelled differently from county to county; spellings at least 0.95 alike (difflib) over disjoint counties are joined (4 and 13). OAARCY, the 2022 set the plan named for the eight states UYQIEP holds only as local files, holds only ID, IN, ND and WA, with the same 363 contests and votes as UYQIEP (`data/local/check-2022-oaarcy.json`), so it is a check and adds nothing.

**Fixes found in the output** [measured]:
- MEDSL files some yes-or-no questions as candidate races, with a yes and a no line ('Yes-Local Amendment No 1'): read as questions (7 in 2018, 9 in 2020, 7 in 2024; they leave the local races, §7).
- It files some questions' yes and no under different wordings in the same counties: joined where the words agree by token Jaccard 0.5 or more (4 in 2018, 45 in 2024); the 21 left with one answer have p not computed, with that reason.
- Michigan's 2022 local file has a 'REJECTED' line under candidate offices (rejected ballots), which made questions of them; left out (12). Michigan's 2022 legislatures now pass the Klarner line (§6), and its stale measure file is gone.
- Alaska's files before 2024 name no county, so its statewide questions read as local. A question is now statewide when it is filed with the state's offices and carries at least 90% of the most precincts any of the state's contests carries that year; where the source names counties and the year's file holds under 90% of the state's counties (South Dakota's 2016 file holds Yankton County only), the question is `partial` and p is not computed (19).
- Titles that name a court ('Statewide Amendment No. 2 - Statewide Business Court') were read as retentions; a title that reads as an amendment, statute, bond or convention question is now a measure. A dollar figure no longer reads as a bond (Oregon's 2016 Measure 97 is a tax).

**Thresholds** (`data/measure/thresholds.json`). Four readers read the constitutions and statutes of the states with statewide questions in the sources, on 2026-11-07 between 06:53 and 07:03 UTC, by curl from the states' own official sites (legislatures, courts, secretaries of state), and returned each rule with its URL, the law's words and the time read: 131 rules in 37 states and DC. Every quote was checked here against the page saved when it was read [measured]: all are found word for word (Colorado's session law with the PDF's spacing), except Indiana's retention fragment, which came through WebFetch (marked `read_via`), and Montana's MCA 13-27-503, which was not in the saved pages and was fetched again and checked at 07:05. What each rule needs is the share of Yes among those voting on the question (`t`); a rule that turns on more (a share of all ballots cast at the election, a turnout floor, a vote of the legislature afterwards, a majority in each affected parish) is recorded as `compound`, and p is not computed for it, since the model forecasts the share only.

Not read, because the sites refused and the readers stopped there (never routed around): **Alabama** (alison.legislature.state.al.us is a JavaScript page, and its robots.txt refused WebFetch), **California** (leginfo.legislature.ca.gov gave curl a Cloudflare check, HTTP 403), **New Hampshire** (nh.gov, sos.nh.gov and courts.nh.gov refused with HTTP 403; gc.nh.gov returned an empty reply) and **Illinois's** general rule (ilga.gov failed TLS verification; art. XIV §3 is read as the Illinois Supreme Court quotes it). Also not read: Colorado's retention rule and its constitution's own sections (its rules come from the 2017 session law amending C.R.S. 1-40-123, applied from 2017), and the shares South Dakota's constitution leaves unstated for initiated laws and retentions.

**Matching a rule to a question.** The type is read from the source's title in the words states use (`question.type`: 'Constitutional Amendment', '(Statutory)', 'Initiated Measure', 'Bond'). Where the title does not say, a rule is used only if every rule read for the state (but its convention question, whose title names it) sets the same threshold, and the readers covered every kind of question the state puts to voters (`complete` in the file). An exception that turns on what a measure does holds p back where the source does not show whether the measure is one: Florida's new State tax (two-thirds of those voting in the election, art. XI §7), Colorado's repeal-only amendments, Arizona's tax measures, New Mexico's amendments restricting the franchise or education rights (three-fourths), Louisiana's amendments affecting five parishes or fewer, Oregon's measures that themselves require a supermajority, Maine's competing measures, Ohio's two-question amendments [the matching rules are mine; inferred]. The texts read are those in force on 2026-11-07, applied to 2016-2024 on my reading that each section was in force then [inferred]; Arizona's tax clauses are applied from 2023 only, since the reader dates them to Proposition 132 of 2022 and the page does not, and the earlier text is not read.

**The forecast**, like past measures (the model's own, D3-v1.1, approved at 06:16): the density of the yes share at t among the statewide questions of the same kind (measures, retentions) of earlier years in the sources, by the like-race route's lay form (at least 100 earlier questions; the window widens 1, 2, 5 points until 10 fall in it). p is model §7's threshold form: a Yes ballot decides with chance about (1 − t) f(t) / n and a No ballot t f(t) / n, n the other voters on the question. Local questions are not computed: the state law that sets their threshold depends on the kind of measure and the place, which MEDSL's wording does not show (the orchestrator, 06:16: "local thresholds are never inferred").

**Where p is computed** [measured], 9,768 questions of 2016-2024: 9,314 local, 435 statewide (333 measures, 102 retentions) and 19 partial.
- p computed: 63 statewide measures, all at t = ½ (22 in 2022, 41 in 2024), from 9.2 × 10⁻⁸ to 2.9 × 10⁻⁶.
- Too few like questions in earlier years: 130 (every retention whose threshold is read, since the sources hold 27, 52 and 63 earlier statewide retentions; and 2016's and 2018's measures, with 0 and 83 earlier).
- An exception the source does not settle: 85 (Florida 24, Colorado 19, Arizona 13, Oregon 12, Louisiana 6, Maine 5, New Mexico 4, Ohio 2).
- Not read: 78 (Alabama 19, California 11, New Hampshire 3, Illinois 2, and 43 where a state's rule for that kind or year is not read).
- A compound rule: 34 (Washington's one-third turnout floor 9, Nebraska's 35% 4, Tennessee's majority of those voting for governor 4, Hawaii 3, and 14 more).
- The title does not show which of the state's thresholds applies: 16. The source redacts precincts: 22. Partial source: 19. The state's counts held back (§6, §7): 6. Advisory: 1.
- Local: 9,314, with the reason above.

**The like-past-measures route out of sample, with 2016 added** (`data/measure/backtest-measures.json`) [measured]. Each year's class comes from earlier years only. Near ½, over every statewide measure (threshold read or not):

| year | earlier measures | measures | within 1 point of ½: expected, seen | within 2 | within 5 |
|---|---|---|---|---|---|
| 2018 | 83 | 87 | 2.1, 3 | 5.2, 5 | 11.5, 12 |
| 2022 | 170 | 45 | 1.3, 1 | 2.6, 2 | 6.1, 11 |
| 2024 | 215 | 112 | 3.1, 7 | 6.3, 12 | 17.7, 26 |
| all | | 244 | 6.5, 11 | 14.1, 19 | 35.3, 49 |

**It still under-forecasts near ½.** Over the three years, 35.3 measures were expected within 5 points of ½ and 49 finished there (1.4 times); within 1 point, 6.5 and 11. Most of it is 2024 (17.7 and 26 within 5 points). The 63 measures given p finished within their own window 8 times against 3.6 expected (2022: 2 and 1.3; 2024: 6 and 2.3), so their p are likely too low, perhaps by half. Earlier years do not show it steadily: fitted on 2018 and 2022 only, the factor would be 1.18 within 1 point, 0.90 within 2 and 1.31 within 5, so a calibration like §7's would not correct 2024 in any steady way, and none is applied. At the orchestrator's word (07:25), each of the 63 p carries the shortfall in `p.note`, written by the build from its own back-test: "this route's back-test shows more near-even finishes than it forecast (49 against 35.3 within 5 points, 2018 to 2024), so p may be low". *With §9's North Carolina counts, North Carolina's 2024 amendment is one statewide measure rather than 100 county questions. That makes 64 statewide p, and the note, which the build writes from its back-test, now reads "49 against 35.5".* Retentions: no earlier statewide retention finished within 5 points of ½, yet 2024 had 3 (2 within 1 point); none has p.

**Size**: the rebuild grows the repository's pack from 27.43 to 27.83 MiB (scratch clone, `git gc --aggressive`, `git count-objects -vH`) [measured]; no file is over 20 MB.

**Still open**, in the orchestrator's order of 07:25: OpenElections and North Carolina's State Board for the local races MEDSL lacks; local thresholds, state by state, from the state law that governs each kind of local measure; each statewide measure's own ballot text, for the 85 held back by an exception and the 16 untyped. Where a state's own code refuses (AL, CA, NH, IL), its statute may be read from Justia or Cornell LII, marked "via compilation", with the official citation and the code year (the orchestrator's ruling of 07:21 for D4, which holds for D3).

## 9. North Carolina's State Board of Elections: every contest from 2000

*Added 2026-11-07 at 08:00 UTC, at the orchestrator's order of 07:25 ("OpenElections and NC SBE first: by script, the most contests for the fewest tokens") and its go-ahead of 07:30 (the results_pct files by script; the 1990s PDFs left for later).*

**Source** [measured]. The State Board's public download site, https://dl.ncsbe.gov/, is an S3 bucket whose `ENRS/` folder holds one folder per election date.
- The listing was read at 07:31 UTC: 87 dates from 1990 to 2026.
- 70 dates have a `results_pct_<date>` file (2000-11-07 to 2026-11-03): every contest on the ballots, by county, precinct and choice. 9 of these files are empty. The 1990s have PDFs only.
- The files were fetched at 07:37 to 07:42 (60 MB).
- The site's `ReadMe_PUBLIC_DATA.txt` says its files "are considered public information per NC General Statutes" and cites G.S. 132-1 [stated]. No licence is printed.
- 2026-11-03 is left out. Its count was four days old at reading and is not yet certified [inferred], and the brief takes no live data.

**Scripts.**
- `pipeline/intake/ncsbe.py` runs `list`, `fetch` and `read`. It handles the six layouts of the site's `layout_results_pct.txt`; three files have no header line, and their layout is read from their columns.
- `pipeline/local_ncsbe.py` runs `check` and `build`.
- What the files do not say, and how each is read [inferred]:
  - **Which lines form one contest.** The State Board names each contest with its place ("CITY OF ARCHDALE MAYOR"), so lines are joined across counties by that name. The exception is 2010 to 2013, whose county contests are named without the county ("BOARD OF COMMISSIONERS"); those are joined within a county.
  - **The number of seats.** "Vote for" is given only from 2014. Before that, a contest with several names has no seat count, so it has no winners and no p.
  - **Which round.** A party's primary carries the party in its name ("- DEM", "(REP)"). Before 2008 it is read from its candidates' party codes, and one name holding several parties is split by party. A second primary, or a first round, is the same name on another ballot that year.
  - **Winners.** The leading names for the seats are taken as won, and none at a tie.

**Checks** (`data/local/check-ncsbe.json`) [measured].
- **The gate against the certified federal counts** (D1's presidency, D2's Senate, and the House district by district in a year with neither). It covers each November general date of an even year.
  - Equal to the vote: 2004, 2006, 2008, 2012, 2014, 2016, 2018, 2022 and 2024.
  - 2020: the president's Republican count is 2 votes lower (2,758,773 against 2,758,775).
  - 2002 is not checked, because D2's files start in 2006.
  - **2000 and 2010 fall short.** In 2000 the president's count is 0.8% lower (Democratic 1,247,003 against 1,257,692). In 2010 the Senate's is 1.0% lower (1,134,001 against 1,145,074). These files were likely posted before the final count [inferred]. Their 1,109 contests carry a note that their counts are the State Board's posted ones, not the certified.
- **The legislature against Klarner** (D and R votes, single-seat districts).
  - Equal in all 170 districts in 2004, 2006, 2008, 2012, 2014, 2020 and 2022.
  - 2002: 167 of 170.
  - 2000: 103 of 115 compared, the rest being multi-member.
  - 2010: none, since the file falls short.
  - 2016: 91 equal and 79 off by a few votes. The State Board is higher, for example 33,456 against 33,441 in Senate 24, and its 2016 Senate and president equal the certified. So Klarner's 2016 North Carolina counts are slightly short [inferred]. They stay in `data/state-*/` as Klarner's, and the orchestrator may want the certified ones there.
  - 2018: 148 equal, and 22 off by about one vote.
- **MEDSL's North Carolina contests** (the same names and votes).
  - 2018: 810 races equal, 73 off by a few votes, and 112 not found.
  - 2020: 742 equal, 95 not found.
  - 2024: 685 equal, 165 off, 113 not found; questions 39 equal, 134 not found.
  - 2022: MEDSL's set holds only 29 North Carolina races.
  - The races not found are mostly ones MEDSL joins and the State Board keeps apart. Cherokee County's three 2018 commissioner districts are one MEDSL contest. The Court of Appeals' three 2024 seats are one MEDSL contest of four names. MEDSL also files the 2024 amendment (citizens-only voting) as 100 county questions, so §8 counted it as 100 local questions.

**The certified file wins** (brief D3, step 2: "let the certified one win"). On MEDSL's general dates (2016 to 2024), North Carolina's local races and questions are now the State Board's. `pipeline/local_medsl.py` reads them in place of MEDSL's (`certified_nc`) and gives them MEDSL's routes and checks. The legislature, the governor and Congress stay MEDSL's. The State Board's other dates are written by `pipeline/local_ncsbe.py` into the same files, and each build keeps the other's contests. Running both builds in either order gives the same files [measured]. What changed:
- North Carolina's 2024 amendment is one statewide measure with its threshold (N.C. Const. art. XIII, sec. 4) and p. Statewide measures with p go from 63 to 64. The measures' back-test reads 49 against 35.5 within 5 points (was 35.3), and so does each p's note.
- 2022 gains about 1,000 North Carolina local races, which MEDSL's 2022 set lacked. 110 of them get p by like races, calibrated on 2020.
- **Outside North Carolina**, the like-race classes and the calibration are fitted on these certified contests too. So 2,786 local p of 2024 in other states moved: by a median of −1.8%, and at most −20.5%.
  - The school board factor goes from 0.749 to 0.646.
  - The pooled like-race factor goes from 0.781 to 0.759.
  - The 2024 out-of-sample test now reads 195 finishes within 1 point against 191.9 expected after calibration. Before, it read 202 against 214.7.
  - So §7's figures for 2024 are now these.

**What is written** [measured]: 21,002 North Carolina contests from 2000 to 2026.
- By level: 17,078 local (with the state's courts, district attorneys and Council of State), 3,057 primaries and 867 questions.
- 4,230 of them are on MEDSL's general dates. 354 of these have p, 2,334 have p = 0 and 1,542 are not computed, each with its reason.
- The other 16,772 are written by `pipeline/local_ncsbe.py`, with p by North Carolina's own like races (below).
- Left out:
  - the legislature's generals, which are Klarner's and MEDSL's and are compared above;
  - 54 legislative primaries of 2014, which Klarner's file holds;
  - Congress, the presidency, the governor and the straight-party lines.

**p for the State Board's other dates** (approved by the orchestrator at 08:08 with this back-test; `data/local/backtest-ncsbe.json`) [measured].
- **The route.** D3-v1.1's like races, fitted on North Carolina's own State Board contests of earlier years only, counted from 2014, when the files begin to give seats. The classes are §7's: scope, office type, the kind of field and the number of candidates, with seats at once at the boundary. Two more were fixed before any score:
  - "a Democrat against a Republican", since these dates have no county lean;
  - primaries by office type and number of candidates, with p between the top two (model section 7).
- **The back-test.** Each year is forecast from earlier years only. For each class, the expected count is the chance its like races gave of finishing in the class's window around ½; the seen count is how many did.
  - Local races, 2016-2026: 2,191 forecast, 270.3 expected and 281 seen.
  - Single-seat races: 115.3 against 113. Multi-seat boundaries: 193.7 against 206.
  - Primaries, 2019-2026: 484 forecast, 38.7 against 38.
- **A single year is rougher than the pooled figure.**

  | Year | Local races: expected, seen | Primaries: expected, seen |
  |---|---|---|
  | 2017 | 29.4, 28 | |
  | 2018 | 7.4, 15 | |
  | 2019 | 32.7, 41 | 0.2, 0 |
  | 2020 | 7.2, 6 | 12.3, 10 |
  | 2021 | 49.4, 41 | |
  | 2022 | 16.8, 13 | 7.6, 11 |
  | 2023 | 51.1, 54 | 0.1, 0 |
  | 2024 | 15.3, 13 | 5.8, 7 |
  | 2025 | 58.5, 67 | 0.3, 1 |
  | 2026 | 2.0, 2 | 12.4, 9 |

  In 2018, twice as many local races finished in the window as were expected. In 2021, a sixth fewer.
- **No calibration.** A factor fitted on earlier years only (the 06:38 rule) brings 2019-2026 to 251.6 expected against 237 seen; uncalibrated gives 233.0. It makes the later years worse, so it is not applied, and each forecast says so in its `note`. Unlike MEDSL's national classes (0.75-0.78, §7), North Carolina's own classes are about right.
- **What it gives, on the State Board's other dates** (the State Board's contests on MEDSL's dates take MEDSL's routes, above).
  - p: 1,742 local races (584 single-seat, 1,158 at the boundary, marked not yet checked for M2) and 484 primaries.
  - p = 0: 5,177.
  - Out of reach, each with its reason:
    - too few like races in earlier years: 1,746 local, 1,453 primaries;
    - 2014, with no earlier year to fit on: 504;
    - no seats before 2014: 3,343;
    - first rounds, second primaries and primaries that a second primary followed: 380;
    - after an earlier round: 171;
    - write-ins near the winner's votes: 1,158;
    - a write-in in the deciding pair: 41;
    - no votes: 1;
    - questions, waiting on step (b): 572.

**Size** [measured]. The repository packs to 28.48 MiB with this change, against 26.60 MiB at main's 001d3f7 (scratch clones, `git gc --aggressive`). The new files are 15.9 MB unpacked.

**Still open.**
- Klarner's 2016 North Carolina counts, against the certified ones.
- The 1990s PDFs (left for later, 07:30).
- 2026-11-03, once certified.

