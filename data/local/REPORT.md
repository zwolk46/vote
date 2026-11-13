# State legislatures, primaries, local races and measures: sources, method and checks

*Worker D3, `briefs/D3-data-local.md`. First written 2026-11-07 05:10 UTC; method and figures brought to D3-v1.1 at 05:50, and the review points of 05:17 fixed at 06:10; MEDSL's 2022 and 2024 returns added at 06:14 (§6), their 2018 and 2020 returns and local p at 06:36 (§7), measures with their thresholds and MEDSL's 2016 questions at 07:25 (§8), and North Carolina's State Board of Elections, every date from 2000, at 08:00 (§9). Marks: [measured] computed here from the files; [stated] as the source says; [inferred] my reading. The inventory of every source found is `data/sources/local.md`.*

**State at this writing.** Every state legislative contest of 1967-2022 that Klarner's dataset holds is in `data/state-upper/`, `data/state-lower/` and `data/primary/`: 189,103 contests. Each has p, p = 0 with the reason, or the reason p is not computed. The forecast method is D3-v1.1: D3-v1 as proposed, approved by the orchestrator at 05:06 with one change (each year fitted on earlier years only), and with runoffs added at its word. **MEDSL's precinct returns of 2022 and 2024** add 30,410 contests (§6): the state legislatures of 2024, 3,616 of them with p; local races and the states' other offices, 20,152; and 4,944 ballot measures. §7 adds 2018 and 2020 and p for local races; §8 adds 2016's questions and p for statewide measures: 9,768 measures, 63 of them with p. §9 adds North Carolina's own certified files: 21,002 contests from 2000 to 2026, which also take the place of MEDSL's North Carolina contests on its dates. With them, D3's files hold 265,272 contests.

## 1. Sources taken in by script

| Source | Script | What it gives | Checks [measured] |
|---|---|---|---|
| Carl Klarner, *State Legislative Election Returns, 1967-2022*, Harvard Dataverse doi:10.7910/DVN/FJOGJB, v1.0 (2024-06-12), CC0 1.0 | `pipeline/intake/klarner_state_legislative.py` | 418,894 candidate rows into 189,103 contests: 158,537 regular generals, 27,359 primaries (first rounds and runoffs included), and 3,207 others (Louisiana's two rounds, specials, top-two primaries) | rows read: 418,894, as the record says. Democratic and Republican totals against Klarner's own contest file: 15 of 151,769 contests differ. In most, the contest file has 0 for a party to which the candidate file gives a few votes; one differs by 604 votes (Illinois House 38, 1968). All are listed in the cache's `checks.json`. Candidates against Klarner's candidate-contest file: 16 of 307,892 differ. Winners per chamber and year against Klarner's seats-up file: 7 of 2,512 differ, each with one or two winners fewer than the seats up (likely ties or unfilled seats [inferred]). Klarner's `ovote` is 0 in 9,061 contests where its candidate file lists non-major candidates with votes, so it is not used as a check |
| MIT Election Data and Science Lab, *Precinct-Level Returns 2024 by Individual State*, Harvard Dataverse doi:10.7910/DVN/NYTPDU, v1.0, CC0 1.0 | `pipeline/intake/medsl_precinct.py`, then `pipeline/local_medsl.py` | 51 files, 18,383,653 rows, into 29,910 contests of every office below Congress | rows read match Dataverse's count in all 45 files it counts. The same files' presidential totals against D1's certified ones: 27 states exact, 47 within 0.2%; Indiana +5.2%, Louisiana −48.9%, New Jersey +14.4% (all three named in MEDSL's README), held back (Indiana's now replaced by the state's own file, §10); Maine −1.2%, MEDSL's first-round counts (its README), kept |
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
- 2024: the presidential totals above. New Jersey's contests are released county by county, under §13's gate. Indiana's are now the state's own certified counts (§10), and Louisiana's the state's own official ones (§12).
- 2022 state legislatures against Klarner's (`data/local/check-2022-medsl-klarner.json`), 4,130 single-member districts named alike in both: D and R votes identical in 3,426; the two-party share within 1 point in 574 more (counts scaled alike: New Hampshire's senate is exactly double in Klarner, Idaho's double in MEDSL); a major party's candidate in one source only in 94; the share more than 1 point apart in 36. The winner differs in 89. (Read again with the intake of §7, 9 Illinois districts the first reading had split now join, and Illinois falls under the line.) States where more than 10% of districts differ in share or parties (AR, IN, MI, WA, WY), and California, whose 2022 file has exactly 1,048,575 rows, a spreadsheet's limit, so it is likely cut short [inferred], are not used for last results or like races.
- The US House totals in the same files against D2's are kept in the checks file but not used: D2's state totals include blank-ballot lines in some states and its party words vary, so they do not compare line for line.

**Method**, D3-v1.1 unchanged:
- **State legislatures, 2024**: route (a) fitted on Klarner's races of 1967-2022 (earlier years only). The seat's last result is MEDSL's 2022 result where at least 80% of the district's 2024 precincts were in it in 2022; otherwise class C. Incumbency is matched by name against the 2022 winners and Klarner's of 2020-2022. Other structures take Klarner's like-race classes of earlier years (routes b and c). Alaska's races are counted by ranked choice (MEDSL's 2022 README), so p is not computed there; districts the source splits into several contests are held back (21).
- **Local races and the states' other offices** (courts, boards, statewide officers other than the governor, which plan §3 gives no level of their own: `office_scope: state`): classes by office type, partisanship, seats and candidates, from like races of earlier years in the sources taken in.
- **Measures**: see §8.

**The 2024 state legislative forecasts against what happened** (out of sample: fitted on 1967-2022) [measured], 3,032 partisan races: in the 50/80/95% intervals 60/86/96%; within 49-51%, 134.2 expected and 128 seen; within 100 votes, 42.7 expected and 42 seen. The forecasts leaned 2.3 points too Democratic on average, the year's swing. Class C carries 2,406 of them: precinct names change between the files, so the lines test finds unchanged lines for only 627 districts.

**Class C** (added 2026-11-07 at 09:28 UTC, at the orchestrator's question of 09:22: the site will need to know which p rest on a coarse forecast) [measured]. With Indiana's (§10), 2,461 of the 2024 legislative p rest on class C, against 478 on class A and 163 on class B. Class C's forecast reads the chamber's lean (the mean Democratic share of the chamber's contested seats at its previous election, minus ½), which is the same for every district of a chamber, and incumbency; so it cannot tell a safe district from a close one, and its sd is about 0.11. Indiana's House District 2 is an example: 82% Democratic, forecast at 0.47 with sd 0.115, p 9.2e-5. Out of sample in 2024, class C's 2,461 races: within 49-51%, 112.6 expected and 106 seen; in the 50/80/95% intervals 55/84/95%; the means leaned 2.6 points Democratic. In 1972-2022 (`data/local/backtest.json`, `partisan.by_class.C`), 19,619 races: 972.8 expected and 923 seen within 49-51%. Class C is right near ½ in the count, but each of its p is that of an average district of its chamber, not of its own.

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

Both years are within the line, so p is computed: 947 races in 2024 and 848 in 2020 (2020's fell to the calibration rule below until it was taken out at 09:49). The intervals hold, but the forecasts lean about 3 points too Democratic, and slightly fewer races finished near ½ than forecast (about 10% fewer within 49-51%, 15% fewer within 100 votes in 2024), so these p are, if anything, a little high. By office, the 50% interval holds 44% for councils and boards (454 races in 2024) and 66-68% for clerks and judges. 2018 and 2022 have no previous House vote by county in the sources taken in (2016 is not read; 2020's file is local only), so their 2,038 such races are not computed, with that reason.

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

**Taken out by the robustness test** (*added 2026-11-07 at 09:49 UTC*: brief D3, amended 08:36; the orchestrator, 09:31 and 09:36; `data/local/calibration-local.json`, each route's `test`, `leave_one_year_out` and `robustness_rule`) [measured].
- **The rule.** A change to a forecast stands only if it improves the out-of-sample test, and still improves it, with no tested cell made worse, when any one scored year is left out.
  - *Improves* means the count near ½ comes nearer and the deviance by office type falls.
  - A *tested cell* is an office type with 5 or more seen or expected, D2's rule (data/congress/REPORT.md §0.1), so that both builds test alike.
  - Every year with a factor fitted on earlier years is now scored, each with its own factor. For like races that is 2022 and 2024; for Democrat against Republican, 2024 only.
- **Like races: fails.**
  - Over 2022 and 2024 it improves the count (299.6 expected → 222.5, against 217 seen) and the deviance (43.7 → 16.9).
  - But three tested cells move further from what happened: other local offices (8.0 → 6.1, against 10 seen), judges (5.0 → 3.8, against 8) and sheriffs and constables (3.8 → 2.9, against 7).
  - It is the same with 2022 left out (2024 alone). With 2024 left out, 2022 alone passes (15.5 → 11.7, against 3).
- **Democrat against Republican: fails.**
  - 2024 is its only scored year. With it left out no scored year is left, so the second half of the test cannot pass (the orchestrator, 09:36: "the factor must fail. Say so in REPORT as the reason, beside the cells").
  - Its cells fail too: councils and boards go 27.4 → 24.8, against 29 seen.
- **So no local p is calibrated.** p stands uncalibrated, as before #31.
  - Each p a factor would have moved carries `calibration_not_of_record`: the factor, what it was fitted for and on, and p with it, which is the p of before to the digit.
  - 3,333 p rise, by a median of 1.235 times and at most 1.548 times. 2020's 2,666 like-race and Democrat-against-Republican p are computed again, since they no longer wait for an earlier year to fit a factor on.
  - Every moved p is in `data/local/moves-m2-item4.json`, with its id, before and after.
- **What stands is known to run high near ½.** Uncalibrated, 2024's like races expect 284.1 within their windows against 214 seen. That is the shortfall of the paragraphs above, now shown beside each p rather than taken out of it.

**The exact sum keeps the measured density** (*added 2026-11-07 at 09:49 UTC*: M2's item 4, #47; the orchestrator, 09:03 and 09:36) [measured].
- A like-race p is f/(2n), with f the class's measured density at ½. Below 1,000 voters pipeline/core.py takes the exact lattice sum instead, over a normal of mean ½ whose density at ½ is f.
- That normal is truncated to (0, 1) and renormalised. That is right for a forecast of a share, but here it raises the density above the measured f for a flat class: 1994's New Hampshire House districts had p 1.99 times f/(2n).
- The exact sum is now multiplied by the normal's mass on the sum's grid (`p.exact_mass`), which gives the unrenormalised mix (`pipeline/local.py`, `_p_like`); model/math/common.py and pipeline/core.py are unchanged.
- 4,739 exact like-race p carry the mass. 320 of them move by more than 1%, 24 by more than 10%, and at worst by 0.503 times, in five 1994 New Hampshire House districts: Cheshire 12 goes from 6.53e-4 to 3.28e-4, against f/(2n) = 3.29e-4.

**Route (a)'s rows already follow the ballot** (*added 2026-11-07 at 09:49 UTC*, M2's reading 10.8) [measured].
- `partisan_rows` keeps a contest with one Democrat and one Republican among the named candidates on the ballot. Its helper `two_leading` always returned every named candidate, not the first two; it is now called `on_ballot`, a name that says so.
- So the 400 contests where a third candidate finished ahead of the Democrat or the Republican are rows: all 400 are, counted from Klarner's own `ocand` and `ovote`.
- The rows differ from M2's in 30 contests of 90,953, and there the cause is Klarner's own file. Its contest-level counts (`dcand`, `rcand`) disagree with its candidate rows:
  - 12 have two Republicans in the rows and `rcand` 1, for example Vermont 2000, Rutland 3;
  - 11 have a Republican with a few votes in the rows and `rcand` 0, for example Washington 1968, District 24, where the Republican has 73 votes;
  - 7 others.
- The pipeline reads the candidate rows, with their names. No p moves with this.

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

**It still under-forecasts near ½.** Over the three years, 35.3 measures were expected within 5 points of ½ and 49 finished there (1.4 times); within 1 point, 6.5 and 11. Most of it is 2024 (17.7 and 26 within 5 points). The 63 measures given p finished within their own window 8 times against 3.6 expected (2022: 2 and 1.3; 2024: 6 and 2.3), so their p are likely too low, perhaps by half. Earlier years do not show it steadily: fitted on 2018 and 2022 only, the factor would be 1.18 within 1 point, 0.90 within 2 and 1.31 within 5, so a calibration like §7's would not correct 2024 in any steady way, and none is applied. At the orchestrator's word (07:25), each of the 63 p carries the shortfall in `p.note`, written by the build from its own back-test: "this route's back-test shows more near-even finishes than it forecast (49 against 35.3 within 5 points, 2018 to 2024), so p may be low". *With §9's North Carolina counts, North Carolina's 2024 amendment is one statewide measure rather than 100 county questions. That makes 64 statewide p, and the note, which the build writes from its back-test, now reads "49 against 35.5".* *With §10's Indiana file, Indiana's 2024 amendment adds a 65th, and the note reads "50 against 35.6".* *With §12's Louisiana file, Louisiana's five 2024 amendments enter the back-test (251 statewide measures), none with p, and the note reads "52 against 36.4".* Retentions: no earlier statewide retention finished within 5 points of ½, yet 2024 had 3 (2 within 1 point); none has p.

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
  - **Which lines form one contest.** The State Board names most contests with their place ("CITY OF ARCHDALE MAYOR"), so lines are joined across counties by that name. The exceptions are a county's own contests named without the county ("BOARD OF COMMISSIONERS"). In 2010 to 2013 every county contest is one per county. From 2014, a county's own contest whose name carries no place (`generic` in `pipeline/intake/ncsbe.py`: "SHERIFF (REP)", "BOARD OF EDUCATION DISTRICT 1", "COUNTYWIDE MALT BEVERAGE ELECTION") is also one per county, and says so in its `notes`. The one exception is where the counties share a county-prefixed group id, as the Town of Davidson's 2017 bonds do in Iredell and Mecklenburg.
  - *Corrected 2026-11-07 at 09:21 UTC* [measured]. Before this, from 2014 those names were joined across counties, so different counties' contests were summed. 88 written contests were affected, none with p. Examples are the 2014 primary's "Sheriff (REP)" across 34 counties, 2016's "Soil and Water Conservation District Supervisor" across 77, and 2018's "One Quarter Cent Sales Tax" across 11. They are now 500 contests, one per county, on five dates from 2014-05-06 to 2018-05-08; 80 old ids are gone and 495 are new.
  - They entered the earlier years' like races, so later p moved. 497 p change:
    - 137 are new, in classes that now reach 100 like races;
    - 360 move, by a median of 7% and at most 10% (each class's f(½) is measured again on more races);
    - none falls out.
    - The changes are in the local races of 2019-2026 (67) and the primaries of 2017-2026 (430).
    - Each p is listed, with its id, before and after, in `data/local/moves-ncsbe-own-county.json`.
  - **The number of seats.** "Vote for" is given only from 2014. Before that, a contest with several names has no seat count, so it has no winners and no p.
  - **Which round.** A party's primary carries the party in its name ("- DEM", "(REP)"). Before 2008 it is read from its candidates' party codes, and one name holding several parties is split by party. A second primary, or a first round, is the same name on another ballot that year.
  - **Winners.** The leading names for the seats are taken as won, and none at a tie.

**Checks** (`data/local/check-ncsbe.json`) [measured].
- **The gate against the certified federal counts** (D1's presidency, D2's Senate, and the House district by district in a year with neither). It covers each November general date of an even year.
  - Equal to the vote: 2004, 2006, 2008, 2012, 2014, 2016, 2018, 2022 and 2024.
  - 2020: the president's Republican count is 2 votes lower (2,758,773 against 2,758,775).
  - 2002, which D2's files do not reach (they start in 2006), against the Clerk of the House's *Statistics of the Congressional Election of November 5, 2002* (`pipeline/intake/clerk_house.py`; the orchestrator, 08:32): the Senate and all 13 House districts are equal, every candidate's votes.
  - **2000 and 2010 fall short.** In 2000 the president's count is 0.8% lower (Democratic 1,247,003 against 1,257,692). In 2010 the Senate's is 1.0% lower (1,134,001 against 1,145,074). These files were likely posted before the final count [inferred]. Their 1,109 contests carry a note that their counts are the State Board's posted ones, not the certified.
- **The legislature against Klarner** (D and R votes, single-seat districts).
  - Equal in all 170 districts in 2004, 2006, 2008, 2012, 2014, 2020 and 2022.
  - 2002: 167 of 170 in the D and R votes. Of the 3 that differ, House 118 reads 113,717 Democratic votes in Klarner's against 13,717 in the State Board's, and Senate 15 reads 34,177 Republican against 36,177; both look like typing slips in Klarner's [inferred]. A fourth, Senate 28, differs in its Libertarian (7,002 in Klarner's against 702). The State Board's 2002 file passes its gate, so its counts are written for these 4 (below).
  - 2000: 103 of 115 compared, the rest being multi-member.
  - 2010: none, since the file falls short.
  - 2016: 91 equal and 79 off, by 1 to 162 votes (median 5). The State Board is mostly higher, for example 33,456 against 33,441 in Senate 24, and its 2016 Senate and president equal the certified. So Klarner's 2016 North Carolina counts are slightly short [inferred].
  - 2018: 148 equal, and 22 off by 1 to 74 votes (median 12).
- **The legislature's 2024 generals against MEDSL's** (`legislature_medsl_2024`; named candidates' votes): 124 of 170 equal and 46 off, by up to 643 votes (Senate 32: 67,131 in the State Board's against 66,488 in MEDSL's).
- **MEDSL's North Carolina contests** (the same names and votes).
  - 2018: 810 races equal, 73 off by a few votes, and 112 not found.
  - 2020: 742 equal, 95 not found.
  - 2024: 685 equal, 165 off, 113 not found; questions 39 equal, 134 not found.
  - 2022: MEDSL's set holds only 29 North Carolina races.
  - The races not found are mostly ones MEDSL joins and the State Board keeps apart. Cherokee County's three 2018 commissioner districts are one MEDSL contest. The Court of Appeals' three 2024 seats are one MEDSL contest of four names. MEDSL also files the 2024 amendment (citizens-only voting) as 100 county questions, so §8 counted it as 100 local questions.

**The certified file wins** (brief D3, step 2: "let the certified one win"). On MEDSL's general dates (2016 to 2024), North Carolina's local races and questions are now the State Board's. `pipeline/local_medsl.py` reads them in place of MEDSL's (`certified_nc`) and gives them MEDSL's routes and checks. The governor and Congress stay MEDSL's. The legislature keeps its contests from Klarner and MEDSL, with the State Board's counts where they differ (below). The State Board's other dates are written by `pipeline/local_ncsbe.py` into the same files, and each build keeps the other's contests. Running both builds in either order gives the same files [measured]. What changed:
- North Carolina's 2024 amendment is one statewide measure with its threshold (N.C. Const. art. XIII, sec. 4) and p. Statewide measures with p go from 63 to 64. The measures' back-test reads 49 against 35.5 within 5 points (was 35.3), and so does each p's note.
- 2022 gains about 1,000 North Carolina local races, which MEDSL's 2022 set lacked. 110 of them get p by like races, calibrated on 2020.
- **Outside North Carolina**, the like-race classes and the calibration are fitted on these certified contests too. So 2,786 local p of 2024 in other states moved: by a median of −1.8%, and at most −20.5%.
  - The school board factor goes from 0.749 to 0.646.
  - The pooled like-race factor goes from 0.781 to 0.759.
  - The 2024 out-of-sample test now reads 195 finishes within 1 point against 191.9 expected after calibration. Before, it read 202 against 214.7.
  - So §7's figures for 2024 are now these.

**The legislature's counts: which source each year carries** (the orchestrator, 08:05: "Replace Klarner's 2016 North Carolina legislative counts with the certified ones too, in a later PR, marked"; 08:08: "Mark which source each year carries") [measured]. Only a State Board file that passes its gate replaces another source's count. A replaced contest keeps its Klarner or MEDSL record, takes the State Board's votes for each candidate, and is marked: `result.votes_source` is `"ncsbe"`, its first note gives both counts for each candidate that changed, and its file gains the State Board's source block. Candidates are matched by party for the Democrat and the Republican, and by name otherwise. A contest whose named candidates do not all match keeps its count. There are 8 such contests, all in Klarner's years, and in each every vote is equal: Klarner names a write-in candidate whose State Board line is marked "(Write-In)", which the match leaves out.

| Year | Counts in `data/state-*/<year>/NC.json` | Why |
|---|---|---|
| 2000 | Klarner's | the State Board's file falls short of the certified federal count |
| 2002 | Klarner's, with the State Board's in 4 of 170 | the State Board's file gated against the Clerk of the House's statistics (the orchestrator, 08:32) |
| 2004, 2006, 2008, 2012, 2014, 2020, 2022 | Klarner's, equal to the State Board's in every contest compared | |
| 2010 | Klarner's | the State Board's file falls short |
| 2016 | Klarner's, with the State Board's in 79 of 170 contests | `pipeline/local.py`, `certified_votes` |
| 2018 | Klarner's, with the State Board's in 22 of 170 | the same |
| 2024 | MEDSL's, with the State Board's in 46 of 170 | `pipeline/local_medsl.py`, `certified_legislature` |

The p of these contests are computed from the certified counts. Elsewhere, the fits that pool these contests moved p. The 2016, 2018 and 2024 counts moved them by at most 1 part in 87,000 (#46). The 2002 counts moved them more, because Klarner's 113,717 in House 118 sat in every later year's fit: 34,598 p in 981 files outside North Carolina, by a median of 0.011% and at most 0.36% (Kentucky's Senate 4 of 2022: 9.77926e-06 to 9.74402e-06) [measured]. In `data/local/backtest.json`, 2002's log score goes from 0.698 to 0.701 and 2012's share within 50 points from 0.5439 to 0.5427. The local calibration (`data/local/calibration-local.json`) moves in its first decimal, for example 2024's expected count before calibration from 59.7 to 59.8.

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
  - Local races, 2016-2026: 2,424 forecast, 288.6 expected and 304 seen.
  - Single-seat races: 142.7 against 150. Multi-seat boundaries: 196.7 against 209.
  - Primaries, 2017-2026: 613 forecast, 50.6 against 55.
  - These are the figures with the deciding rounds below (the orchestrator, 09:53). Before them (after the correction of 09:21 above) they were 2,231 forecast, 275.9 against 289; single-seat 132.8 against 138; boundaries 193.7 against 206. Before the correction: 2,191 forecast, 270.3 against 281; single-seat 115.3 against 113; and primaries 484 forecast, 38.7 against 38.
- **A single year is rougher than the pooled figure.**

  | Year | Local races: expected, seen | Primaries: expected, seen |
  |---|---|---|
  | 2016 | 0.5, 1 | |
  | 2017 | 29.7, 29 | 0.2, 0 |
  | 2018 | 8.0, 17 | 5.5, 11 |
  | 2019 | 44.2, 53 | 0.1, 0 |
  | 2020 | 11.6, 11 | 8.6, 7 |
  | 2021 | 50.0, 41 | |
  | 2022 | 17.7, 13 | 8.0, 11 |
  | 2023 | 52.0, 57 | 0.1, 0 |
  | 2024 | 16.2, 14 | 11.0, 14 |
  | 2025 | 56.1, 65 | 0.3, 1 |
  | 2026 | 2.6, 3 | 16.8, 11 |

  In 2018, twice as many local races finished in the window as were expected. In 2021, a sixth fewer.
- **No calibration: the factor fails the robustness test** (*rewritten 2026-11-07 at 10:06 UTC*; `backtest-ncsbe.json`, `calibration`).
  - **Why it is retested.** With the deciding rounds in the pool, the 06:38 rule alone, a pooled count brought nearer, would now take the factor: 284.5 expected against 274 seen in 2018-2026, against 258.5 uncalibrated. Each forecast's note said, as a fixed text, that it was not taken. So the factor now goes through the robustness test of the brief's amendment of 08:36, as MEDSL's did in §7. Each year with 30 or more expected in earlier years is scored with its own pooled factor (2018-2026: 0.99 to 1.23).
  - **Local races.** It fails. The count comes nearer, but the deviance by office type rises from 5.08 to 5.57. Two tested cells are made worse: single-seat mayors (29.0 to 32.9 against 26 seen) and school boards (16.6 to 18.1 against 13). With each year left out it fails too.
  - **Primaries.** It fails: 2025 and 2026 are scored, 17.1 expected rises to 22.1 against 12 seen, and the councils' cell is made worse.
  - **So p stays uncalibrated**, and each forecast's `note` now gives the reason from the record. The earlier figures: the factor brought 2019-2026 to 261.7 expected against 245 seen, uncalibrated 238.6 (before the correction of 09:21: 251.6, 237 and 233.0). Unlike MEDSL's national classes (0.75-0.78, §7), North Carolina's own classes are about right.
- **What it gives, on the State Board's other dates** (the State Board's contests on MEDSL's dates take MEDSL's routes, above).
  - p: 1,912 local races (734 single-seat, 1,178 at the boundary, marked not yet checked for M2) and 613 primaries. Of the local ones, 64 are deciding rounds (46 single-seat, 18 at the boundary).
  - p = 0: 5,263.
  - Out of reach, each with its reason:
    - too few like races in earlier years: 1,733 local, 1,375 primaries;
    - 2014, with no earlier year to fit on: 603;
    - no seats before 2014: 3,343;
    - first rounds, second primaries and primaries that a second primary followed: 522;
    - a second round on a date other than November's (perhaps a runoff): 30;
    - write-ins near the winner's votes: 1,162 (with the 91 on MEDSL's dates, 1,253 State Board contests carry this reason) [measured];
    - a write-in in the deciding pair: 41;
    - no votes: 1;
    - questions, waiting on step (b): 583.

**Why M2's rebuild of this route's pool holds more rows** (*added 2026-11-07 at 09:49 UTC*, M2's reading 10.5: 1 to 17 rows more in 648 of 1,742 contests) [measured].
- It is not the county split of 09:21. Rebuilt from today's files with M2's own `local_pools`, the local pool holds 5,476 rows against the route's 5,441. Every row of the route's pool is in M2's, and the 35 more are all of one kind.
- They are November contests of MEDSL's years (2018-2024) whose name was on a ballot earlier that year, a nonpartisan primary: Johnston, Moore, Wayne, Craven and Watauga counties' school boards, and Asheville's and Mount Airy's councils and mayors.
  - MEDSL's route writes them to the files as generals, with like races and p.
  - The State Board's route reads the same contest as "a contest after an earlier round this year (perhaps a runoff)". It leaves the contest out of its own pool and computes no p for it on its own dates (171 local contests, §9 above).
- So the two routes read one contest two ways. In an even year's November general, North Carolina holds no runoff, because its second primaries are party primaries in the spring [inferred; not read in the statute yet]. The State Board's route could read those as generals, as MEDSL's does. That would add the 35 rows, and the even-year November contests among the 171 would get p. This was not done in #59: it changes which contests a route takes, so it waited for the orchestrator, who ruled at 09:53 (below).

**November's deciding rounds** (*added 2026-11-07 at 10:06 UTC*; the orchestrator, 09:53) [measured].
- **The ruling.** "A November contest that follows an earlier round of the same contest that year is that contest's deciding round, whether the earlier round was a nonpartisan primary or a first round. This holds in odd and even years alike. So compute it by the route's classes (number of candidates and seats as usual), and mark it 'deciding round after an earlier round'. The earlier round stays not computed, as model §7 records." *Reason, in its words:* "the November count is the one that elects, and MEDSL already reads them that way, so both routes will agree."
- **What changed** (`pipeline/local_ncsbe.py`, `p_of`, `deciding_words`).
  - A November contest whose name was on an earlier ballot that year now takes the route's classes, and its `election` begins "deciding round after an earlier round on <date>".
  - MEDSL's route writes the State Board's contests on its own general dates (2018-2024). Those of the same kind carry the same words, 35 of them, through `medsl_shape`'s `earlier_round`. Their p is MEDSL's route's, as before (23 computed, 12 not, each with its reason), and does not move.
  - The earlier round stays not computed. So does a second round on a date other than November's, 30 contests, now in those words.
  - A question has no rounds. One whose title was on another ballot that year (21) now says only that, in place of the rounds' words it carried before.
- **What it gives.** Of the 141 November contests of 2014-2025 that were not computed as "after an earlier round", 64 get p: 46 single-seat and 18 at the boundary, all in the odd years 2017-2025. The other 77 stay out, because their class has too few like races in earlier years. Before 2014 the files give no seats, so deciding rounds there change in words only.
- **The pool.** The deciding rounds enter the route's like races, so later years' classes change. 98 contests get p for the first time, because their class now reaches 100 earlier like races; 95 of them are 2019's mayors. 1,572 p move: by a median of ×0.990, from ×0.762 to ×1.524. 907 move by more than 1% and 73 by more than 10%.
- **Every moved p** is in `data/local/moves-ncsbe-deciding-round.json`, 1,734 in all, with its id, before, after and why (`D`, `N`, `P`).
- **Words only.** 373 local `election` texts, 244 primaries' (each date now named once) and 310 `not_computed` texts (counts of like races) change without a p.

**Rounds keyed by place** (*added 2026-11-07 at 12:02 UTC*, at the orchestrator's order of 11:44, from M2's check c19 in #69: "Key the rounds on the contest's place as well (county, or the district's own id where it spans counties), rebuild, and list every contest whose mark or p changes. Also check whether any other route keys contests by name alone. Reason: a round is the same contest only in the same place, and the 09:53 ruling's reason holds only there.") [measured].
- **The fault.** `classify` keyed the rounds on (year, contest name, party), with no place. Many of the State Board's names carry no place ("BOARD OF EDUCATION DISTRICT 3"), so one county's contest was read as a round of another county's contest of the same name.
- **The fix.** A contest of the same name on another date is a round of this one only where their counties overlap. The files give no district id (the district is empty in all 24,103 contests), so the counties are the place. The rule is overlap, not equality. Of the 363 names on more than one date in a year, 327 have one set of counties, 33 have sets that do not meet (the collisions), and 3 have sets that overlap but differ. Those 3 are Hickory's aldermen in 2019, whose October primary shows Catawba County only and whose November general shows Burke and Catawba. They are one contest each [inferred: the city lies in both counties].
- **What changes.** Every change is listed in `data/local/moves-ncsbe-rounds-by-place.json`, with its id, its words and p before and after, and why.
  - **374 marks corrected.** 102 November contests (96 of 2010, 6 of 2016) were marked deciding rounds and are now generals; their p does not move. 38 contests were marked first rounds and are now elections of their own date: 19 of 2010-05-04 and 19 of 2016-03-15 (M2's 19), all school boards. 217 primaries no longer say a second primary followed (126 Republican and 91 Democratic). 17 questions no longer say a question of the same title was on another ballot.
  - **17 p newly computed.** They are among the 38 former first rounds, and all are p = 0: one name on the ballot for each seat, which the false mark had held. The other 21 stay not computed for their own reasons, such as no seats before 2014.
  - **36 p computed for the first time**, because their class now reaches 100 like races in earlier years: 32 primaries of 2026 and 4 local contests.
  - **461 p move** (394 primaries and 67 local), because the contests the false marks kept out of the like-race pool are in it now. The median move is ×1.012, from ×0.938 to ×1.028. 459 move by more than 1% and 38 by more than 5%.
  - 809 `not_computed` reasons change only in their count of like races.
- **What does not change.** No p outside North Carolina moves. The State Board's calibration test keeps its verdicts: the local route fails with the same two cells made worse, and the primary route fails with the same cell (`backtest-ncsbe.json`). M2 reported that all 87 computed deciding rounds have a true earlier round in the same county; none of them changes.
- **Other routes, checked for keys by name alone.** None found:
  - Louisiana's rounds (`local_la.rounds`) key on the parish's sheet, or on a multi-parish title, and those titles are unique on each date of 2023 and 2024.
  - Klarner's runoffs (`local.first_round_index`) key on the seat: state, chamber, district and post.
  - MEDSL's intake joins a candidate contest's precincts through their candidates' names, and splits a local question by county.
  - MEDSL's split questions (`fix_questions`) are joined only over the same counties.
  - New Jersey's gate keys on the county.

**Size** [measured]. The repository packs to 28.48 MiB with this change, against 26.60 MiB at main's 001d3f7 (scratch clones, `git gc --aggressive`). The new files are 15.9 MB unpacked.

**Still open.**
- The 1990s PDFs (left for later, 07:30).
- 2026-11-03, once certified.

## 10. Indiana's own certified 2024 general election

*Added 2026-11-07 at 09:04 UTC, at the orchestrator's order of 08:08 ("For the 2024 legislatures of IN, LA and NJ, read each state's own certified results where a file is reachable by script, with a gate against D2's federal counts on the same dates as for North Carolina") and its go-ahead of 08:32 ("Indiana's certified archive is a good source").*

**Why.** MEDSL's 2024 Indiana file adds up to 5.2% more than D1's certified presidential count (§6), so its Indiana contests were held back, with no p. Where two sources hold one contest, the certified one wins (brief D3, step 2).

**Source** [stated]. Indiana's election results site keeps each election in an archive: https://enr.indianavoters.in.gov/archive/2024General/.
- Its page says "Results for the November 2024 General Election are final, subject to pending local recounts/special elections". Its `data/settings.json` says `"Certified": "T"`, version `20241213_160047`.
- No licence for the data is printed. The page's footer reads "Copyright 1989 - <year>. Quest Information Systems, Inc. All Rights Reserved.": Quest is the site's maker.
- The files are the ones the site's own scripts fetch. There are 119 JSON files, 5.5 MB: the settings, the office list, one file per office category (24) with each race's total and its counties, and one file per county (92) with its questions' yes and no. They were fetched at 08:40 to 08:53 UTC, 4 seconds apart.
- `pipeline/intake/in_enr.py` reads them. A question on more than one county's ballot is joined by its type, title and ballot text. Each race's counties come from its regions; a title that does not name its place ("School Board Member, District") takes its district's name from the race's jurisdiction.
- The site lists no write-in lines [measured: no write-in name or code in any race]. So an unopposed race's p = 0 cannot be checked against a strong write-in, as MEDSL's can.

**The gate** (`pipeline/local_in.py`; `data/local/check-in.json`) [measured]. The file's Democratic and Republican votes equal D1's certified presidential count (1,163,603 and 1,720,347), D2's Senate count, and D2's House count in all 9 districts. It passes.

**MEDSL's Indiana against the state's** [measured].
- The legislature, 125 districts:
  - 85 are equal;
  - 39 differ: MEDSL's count is higher in 26, often by as much again, and lower in 13, by up to 76% (Senate 40: 9,378 against 38,424);
  - MEDSL splits 5 into pieces;
  - 1 is not in MEDSL's file.
- Local races: of MEDSL's 1,535, 1,165 are equal, 331 differ and 39 are not found in the state's file. The attorney general reads 1,750,318 Republican votes in MEDSL's, against 1,669,586 in the state's.
- Questions: MEDSL's file holds 33, against the state's 38. MEDSL's statewide amendment covers 42 of the 92 counties. Only 2 of MEDSL's questions equal the state's.

**The certified file wins.** `pipeline/local_medsl.py` (`certified_in`) reads Indiana's legislature, local races and questions of 2024 from the state's file in place of MEDSL's, with MEDSL's routes and checks. Indiana is then no longer held back in 2024. The presidency, Congress and the governor stay D1's and D2's. `result.source` is `in_enr`, and each file carries the source block.

**What is written** [measured].
- **The legislature**, 125 contests: the State House's 100 (64 with p, 36 with p = 0) and the State Senate's 25 (13 with p, 12 with p = 0). Each takes route (a) as class C. The 2022 result is not used, because MEDSL's 2022 Indiana is held back (§6). The lean comes from Klarner's previous election of the chamber, and incumbency from the winners of 2020-2022.
- **Local races**, 1,433: 210 with p (calibrated as §7 said until the robustness test took the factor out, §7), and 968 unopposed with p = 0. 255 are not computed, each with its reason:
  - 133 races between a Democrat and a Republican, whose forecast reads the county's 2022 House lean, which MEDSL's held-back 2022 file cannot give;
  - 122 in classes with fewer than 100 like races in earlier years.
  - The site's code N, "Non Partisan" in its settings, marks every school board candidate, and those races take the nonpartisan classes.
- **Questions**, 38:
  - **The amendment.** Public Question #1 (removing the superintendent of public instruction from the governor's line of succession) is statewide, with its ballot text and p. Its threshold is "a majority of the electors voting on the amendment" (Ind. Const. art. 16, §1(c)). That was read through WebFetch, because the legislature's site gives curl a JavaScript page and Justia's copy answered 403; it is marked `read_via` in `data/measure/thresholds.json`.
  - **The statewide retentions.** The 3 Supreme Court retentions and 1 Court of Appeals retention are statewide. They have no p: Indiana's text states no share (§8).
  - **Local questions.** The other 33 are local: 26 judges' retentions, 6 public questions, and a Court of Appeals retention on 53 counties' ballots. They wait on step (b).
- **Elsewhere.** No p outside Indiana moves: each year's fits and calibration come from earlier years only.
  - The 2024 out-of-sample test of local like races now holds 2,264 contests: 214 finished within 1 point, against 210.7 expected after calibration (before: 2,054, and 195 against 191.9). The calibration has since been taken out (§7).
  - The statewide measures with p go from 64 to 65. Their back-test reads 50 against 35.6 within 5 points, and so does each p's note (§8).

**Still open.** Indiana's other years: the archive keeps earlier elections in the same layout [inferred from its address; not read].


## 11. The boundary route (c) by size: the design, fixed before any score

*Written 2026-11-07 at 10:10 UTC, and committed before any score was run.* [inferred: a design]

**What was asked.** The orchestrator, 09:36: "as a separate step under the robustness test: size bins for the boundary route (c). M2 finds it 12% low under 3,000 votes and 20% high over 30,000. Adopt only if the test passes." At 10:09: "with the design fixed in REPORT first". M2's reading 10.10 gives, by the deciding pair's votes, 205 expected within 49-51% against 234 seen under 3,000; 562 against 625 at 3,000-10,000; 314 against 280 at 10,000-30,000; and 356 against 298 over 30,000.

**The variant: one, fixed now.**
- **What changes.** Route (c)'s class density f(½) is read off the class's earlier like races whose deciding pair falls in the same size bin as the contest's own.
- **The bins** are route (a)'s for s_e (`pipeline/local.py`, `BINS`): the two candidates' votes under 3,000, 3,000-10,000, 10,000-30,000, and 30,000 or more.
- **Which count.** The pair's votes are the n at which p is computed, so the bin comes from the same count as p. Route (a)'s s_e is read the same way (§2; M2 10.11) [inferred: the law's ex-ante rule is about who is on the ballot, and p already takes this n].
- **What stays.** The windows rule does not change: 49-51%, widening to 48-52 and then 45-55 until 10 like races fall in the window. Where the bin holds fewer than 100 earlier like races (`MIN_CLASS`), the class as a whole is used, as now. Route (b) and runoffs keep their classes.

**The pools it is tested on.** Each pool is tested separately, and each year is forecast from that pool's earlier years only, as in its back-test.
1. **State legislatures.** Klarner's multi-seat generals of 1968-2022 (`pipeline/local.py`, `backtest`). Their like races also forecast MEDSL's 2024 legislature, so 2024's outcomes are scored in this pool too, forecast from 1967-2022.
2. **MEDSL's local races at the boundary,** 2020-2024, from MEDSL's earlier years (2018 has none).
3. **North Carolina's State Board,** 2015-2026, from its own earlier years (counted from 2014).

The variant is adopted in a pool only where it passes there. A pool where it fails keeps the record's class density.

**The test** (brief D3, amended 08:36; cells as D2's, 5 or more):
- **The counts.** For every boundary contest given a forecast, three expected counts, each capped at 1, are set against what was seen, as in `backtest.json`'s class tallies:
  - within 49-51%: 0.02 f;
  - within 10 votes: 10.5 f / n;
  - a margin of 0 or 1: 1.5 f / n.
- **Improves.** Over all scored years, the 49-51% count comes nearer the count seen, and the Poisson deviance of the 49-51% counts over the cells falls.
- **The cells.** Each class and size bin, for each of the three counts. A cell is tested where its count seen or expected, as the record stands, is 5 or more. It is made worse where the variant's expected count moves further from the count seen.
- **Adopted** only if it improves with no tested cell made worse over all scored years, and again with any one scored year left out.

**What follows.**
- **If it is adopted in a pool,** the p of that pool's boundary contests change. Each forecast names the bin its density came from (`forecasts[].size_bin`, with `like_races` counted in that bin), and every moved p is listed.
- **If it is not,** nothing changes. The test is recorded in `data/local/size-bins-test.json` and here.

**The result: not adopted in any pool** (*added 2026-11-07 at 10:14 UTC*; `data/local/size-bins-test.json`; `pipeline/local_sizebins.py`, run at 3544a68) [measured]. No p changes, and the forecast stays as it was. This is a new variant, not one that stood, so it is reported here and in the test file, not on each p (as D2 reports its variants, `data/congress/REPORT.md` §0.2).

| Pool | Contests (with their own bin) | 49-51%: record, variant, seen | Deviance over the cells | Tested cells made worse | One year left out |
|---|---|---|---|---|---|
| Legislatures, 1968-2024 | 9,068 (7,188) | 1,415.6, 1,430.4, 1,419 | 105.8 → 45.0 | 8 of 33 | fails for all 55 years |
| MEDSL local, 2020-2024 | 0 | | | | |
| North Carolina, 2015-2026 | 1,257 (1,151) | 196.7, 188.3, 209 | 8.0 → 9.6 | 3 of 10 | fails for all 11 years |

- **Legislatures.** By size, the variant does what M2 asked of it. In the 49-51% counts it brings each bin near the count seen:
  - under 3,000 votes: 199.4 to 209.0, against 228 seen;
  - 3,000-10,000: 559.0 to 623.5, against 622;
  - 10,000-30,000: 309.5 to 279.9, against 279;
  - 30,000 or more: 347.7 to 318.1, against 290.

  So the deviance falls by more than half.
- **Why it still fails.** The total moves from 3.4 under the count seen to 11.4 over it. Eight tested cells of class and bin move further from their counts. For example, two seats with both parties running a full slate under 3,000 votes; three seats with full slates at 10,000-30,000; and the within-10-votes counts of three-seat and four-seat races at 3,000-10,000.
- **Without 2024.** On Klarner's years alone, the total does come nearer: 1,387.5 to 1,400.7, against 1,395. But the same eight cells are made worse, so the decision does not rest on 2024's 191 contests. With any one year left out it fails too.
- **MEDSL's local races.** None at the boundary has a forecast: every class has fewer than 100 earlier like races. The variant falls back to the class, so it could change nothing here.
- **North Carolina.** The variant moves the count away from the count seen and raises the deviance. Three council cells under 3,000 votes are made worse.
- **An observation, not part of the test** [inferred]. In North Carolina's small boundary races, the record expects 427.7 finishes within 10 votes against 327 seen, and 82.8 margins of 0 or 1 against 72. Under 3,000 votes a 10-vote window is wide in share, so f(½) × 10.5 / n overstates it where the density is not flat. p itself uses f at ½ only.
- **What would change the verdict** is the orchestrator's to say: for example, a cell rule that weighs the cells' sum, since the record's total for the legislatures is already within 3.4 of the count seen. The rule as fixed at 10:10 stands, and under it the variant fails.

## 12. Louisiana's own official 2024 results

*Added 2026-11-07 at 10:30 UTC, at the orchestrator's orders of 08:08 ("For the 2024 legislatures of IN, LA and NJ, read each state's own certified results where a file is reachable by script, with a gate against D2's federal counts on the same dates as for North Carolina") and 10:17 ("Go on with LA 2024").* Louisiana elects no legislature in 2024. Its legislature was elected in 2023, after Klarner's last year.

**Why.** MEDSL's 2024 Louisiana file counts Election Day only (its README), 48.9% short of D1's certified presidential count, so its Louisiana contests were held back (§6). It holds only 9 local contests. 7 of them are found in the state's file by their candidates' names, with MEDSL's votes at 0.53 of the state's in the median [measured].

**Source** [measured]. The Secretary of State's results site, https://voterportal.sos.la.gov/.
- **What the site says.** Its configuration names a download for each date: a workbook on the site's S3 storage, `HumanReadableElectionResults/<YYYYMMDD>/Election+Results+(<MM-DD-YYYY>).xlsx`. Its list of elections marks each date's results official (`ResultsOfficial`). All four 2024 dates are official: 2024-03-23, 2024-04-27, 2024-11-05 and 2024-12-07.
- **What a workbook holds.** One sheet of contests on several parishes' ballots, by parish, and one sheet per parish for its own contests, by precinct with early voting as its own line. The site prints no licence.
- **The reading** (`pipeline/intake/la_sos.py`): 887 contests over the four dates. In every one, the parishes' or precincts' lines add up to its total.

**The gate** (`data/local/check-la.json`) [measured]. On 2024-11-05, the file's Democratic and Republican votes match D1's certified presidential count and D2's six House districts exactly: president 766,870 and 1,208,505; House 650,836 and 1,248,101. The worst miss is 0. The other dates hold no federal contest to check.

**Rounds** (`pipeline/local_la.py`). Louisiana fills local offices at a primary open to every candidate. Where no one is elected there, a general election between the leaders follows a few weeks later. In 2024 the primaries are 2024-03-23 and 2024-11-05, and the generals 2024-04-27 and 2024-12-07 [inferred: the source's four dates and the contests it repeats from the first of each pair to the second].

*The statute, added 2026-11-07 at 11:29 UTC at the orchestrator's rulings of 10:35 and 11:16 ("cite the text you read, with its code year, and say the 2024 pairing comes from the source's repeated contests, since the statute's dates have changed").* La. R.S. 18:402 sets the election dates. Its text was read on 2026-11-07 at 10:46 UTC (https://legis.la.gov/Legis/Law.aspx?d=81545), as amended through Acts 2025, No. 386 [stated]. It pairs each season's primary with a general on a later Saturday, as the source's 2024 dates do. But its dates are not 2024's: the section was amended after the 2024 elections (Acts 2024, No. 640; Acts 2025, No. 386). So the 2024 pairing comes from the source's repeated contests. The statute is cited for the pairing's form only.
- **A contest on a primary date** is the first round of a two-round system. It is recorded with its result, and p is not computed (model section 7), as for Klarner's Louisiana legislature. Its candidates on the general's ballot are marked `"to runoff"`. Any who led them all were elected in the primary, and where no general followed, the leaders for the seats were [inferred].
- **A contest on a general date** whose parish and title (seats aside) were on that pair's primary is its deciding round. It takes the routes' classes and is marked "deciding round after an earlier round". This applies the orchestrator's ruling of 09:53 for North Carolina, "the November count is the one that elects" [inferred: the ruling's reason holds for Louisiana's generals].
- **Not rounds.** The same parish and title on two other dates are not read as rounds: Red River's Village of Martin aldermen, three seats on 2024-03-23 and one on 2024-11-05, with one candidate in common. Nor are questions: three were put to the voters again on a later date.
- **The parties' own committees** (241 contests of 2024-03-23: DSCC 84, RSCC 83, RPEC 43, DPEC 31). *Added 2026-11-07 at 11:29 UTC, at the orchestrator's ruling of 10:35: "put the party committees in. Law 5 asks for as many real US contests as true sources allow, and these are on the public ballot, counted by the Secretary of State. Mark them as party offices whose voters are the party's own, compute them where a route fits (vote-for-N only where the model has a route), and say why where not."*
  - **The law** [stated]. The state central committees (La. R.S. 18:443(B), https://legis.la.gov/Legis/Law.aspx?d=81577) and the parish executive committees (18:444(B), Law.aspx?d=81580) are elected "every four years at the same time as the presidential preference primary election". There, "the candidate who receives the greater number of votes cast shall be elected", seat by seat, with ties settled by lot. Read 2026-11-07 at 11:16 UTC. So each committee contest is decided in one round on 2024-03-23. It is not the first round of two.
  - **Their voters** are the party's own [inferred]. At that primary, La. R.S. 18:1280.21(B) (Law.aspx?d=81288) lets each elector vote only for his own party's candidates.
  - **How they are kept.** Each record carries `party_office` (the party, the committee, its law and its voters), and its `election` words say the above. Each takes the routes of its seats and ballot, like any local office. 212 have one seat and 29 have 5 to 14.
  - **Their office type.** At first it was "council, commission or board", through the word "Member" in the title, which pooled them with councils elected at general elections. *Changed 2026-11-07 at 11:53 UTC, at the orchestrator's ruling of 11:30: "give the committees their own office type, "party committee" ... Reason: a like-race class must hold like races, and a seat chosen by one party's voters on a presidential primary's turnout is unlike a council chosen at a general."* Their office type is now "party committee" (`OFFICE_TYPES` in `pipeline/local_medsl.py`, matching only a title that begins DSCC, RSCC, DPEC or RPEC Member).
  - **What they give** [measured]. None gets p. Under the first office type, each class had fewer than 100 like races in earlier years (28 to 70). Under their own, each has none. The reason is on each record. No p moves, and no back-test moves: the 241 records change only their office type and the count in that reason.
- **Left out.** The presidency, its party primaries and Congress (9 contests), which are D1's and D2's.

**What it gives** [measured]. 312 local contests and 325 questions; with the party committees above, 553 local contests.
- **Local p.**
  - First rounds, not computed: 259 (78 of the spring, 181 of the fall).
  - Deciding rounds: 52, of which 9 get p by the like-race classes. 39 have too few like races in their class in earlier years. 4 are between a Democrat and a Republican, but their parish has no lean from the 2022 House returns.
  - One contest on 2024-12-07, Franklinton's five aldermen, has no primary in the source: not computed, with that reason.
- **Questions.** 320 local questions are not computed, waiting on step (b). The five statewide amendments (one on 2024-11-05, four on 2024-12-07) are held back by La. Const. art. XIII §1(C), since the title does not show whether an amendment affects five parishes or fewer (§8). They wait on step (a).
- **What moves elsewhere.** No p outside Louisiana moves. The amendments enter the measures' back-test, so the note on each of the 65 statewide measure p now reads "52 against 36.4" (§8). The 2024 local back-tests gain Louisiana's contests: 2,270 like-race contests, against 2,264 before (`backtest-local-classes.json`). Both calibration routes still fail the robustness test, with the same cells (`calibration-local.json`).

**Still open.** The site's list of elections goes back to 1982 [measured: 319 dates, 318 of them marked official]. The workbook may not exist for the older ones [not read]. Louisiana's 2023 is in §14.

## 13. New Jersey's own certified 2024 results

*Added 2026-11-07 at 10:43 UTC, at the orchestrator's orders of 08:08 ("For the 2024 legislatures of IN, LA and NJ, read each state's own certified results where a file is reachable by script, with a gate against D2's federal counts on the same dates as for North Carolina") and 10:35 ("NJ 2024 as ordered ... its 2024 file holds local contests and any legislative specials; read what is there").*

**What the state's page holds** [measured]. The Division of Elections' 2024 page is https://www.nj.gov/state/elections/election-information-2024.shtml. Outside its HTML comments, it links:
- the official general results for president, US Senate and US House, each an "Official List" PDF by county;
- NJ-10's special primary and special general;
- the party primaries' federal offices and delegates.

It holds no legislative contest. New Jersey elects its legislature in odd years, and the page lists no legislative special. It holds no county, municipal or school board contest either. Those are not on the page; the county clerks publish them [inferred].

**The lists against D1's and D2's counts** (`pipeline/intake/nj_sos.py`, `pipeline/local_nj.py`; `data/local/check-nj.json`) [measured].
- **What was read.** 14 contests and 69 candidates (president 9, Senate 6, House 54). Each list's count matches its own last page ("Total Candidates"). Every candidate's county lines add up to the candidate's total.
- **The match.** Every candidate's votes equal D1's (president) and D2's (Senate, and all 12 House districts).
- **One quirk.** NJ-12's list repeats its last candidate's name with the contest's total. That line is read as the total.

**MEDSL's New Jersey file against the lists, county by county** [measured]. Candidates are matched by surname: MEDSL leaves the party empty in some counties' rows, and in others it files summary lines such as "CONTEST TOTAL" as candidates. The line is the state check's 0.5%.
- **16 counties add up in all three federal offices,** 12 of them to the vote: Burlington, Camden, Cape May, Cumberland, Essex, Hudson, Hunterdon, Middlesex, Monmouth, Morris, Ocean, Passaic, Salem, Somerset, Sussex, Warren.
- **Gloucester** adds up for the Senate and the House. Its presidential count is exactly double.
- **Four counties fail in all three offices:**
  - Atlantic, 0.3% to 0.8% short;
  - Union, 1.9% to 6.1% short;
  - Mercer, 23% to 32% short;
  - Bergen, three times the count.

So the state's +14.4% presidential miss (§6) comes from five counties. Gloucester shows the error can sit in one office alone. A county's federal offices adding up therefore shows its file was read whole. It does not show that every other office's rows are sound [inferred].

**What it gave at first** (PR #63). No contest was added and no p moved, since the lists hold no office below Congress. The gate by county below was put to the orchestrator then.

**The gate by county, as ruled.** *Added 2026-11-07 at 11:12 UTC, at the orchestrator's ruling of 10:45: "adopt the gate by county, with two checks added on the released rows, because your Gloucester reading is right that federal offices adding up does not show the local rows sound".* The code is `pipeline/local_nj.py` (`county_gate`, `row_checks`, `spotcheck`); its results are in `data/local/check-nj.json`, under `county_gate` [measured].
1. **By county.** A contest is released only when every county it lies in adds up in all three federal offices at the 0.5% line. Atlantic, Bergen, Gloucester, Mercer and Union stay held. Each New Jersey record carries `gate`: its counties' federal misses and what the checks found.
2. **Repeated rows** (the same precinct, office, candidate and mode twice). There are none among the file's local rows.
3. **A total line among the precincts.** Gloucester's doubled presidential count is a precinct line named "COUNTY TOTAL" beside its municipalities. So the check holds any contest with a precinct named TOTAL, or with a precinct equal, for every candidate, to all the contest's other precincts added up. There is none in the released counties. Bergen's rows have such a line in 160 contests, but Bergen is held already.
4. **A precinct over its federal votes.** A contest is held when a precinct's votes in it exceed the most votes that precinct cast for one federal office, times the contest's vote-for-N. Where MEDSL gives no vote-for-N, the number of candidates named is used. This holds 3 contests:
   - Camden's county clerk, in 6 of 429 precincts;
   - Camden's sheriff, in 8 of 429 precincts, over by 1 to 13 votes (both Camden contests released by the correction below);
   - Delanco Township's board of education, in 1 of 7 precincts (334 against 323).
5. **Against the county clerks' official results.** Five released contests in five counties were compared. In each county the contest is its board of county commissioners: the one county office on every ballot there, so it runs through every precinct the county files. The sample was fixed before any count was compared. The five counties are the released ones whose clerk's site answered with its official 2024 results.

| County | The clerk's file, in its own words | Largest miss |
|---|---|---|
| Camden | "2024 General Election Canvasser", "OFFICIAL RESULTS" | none |
| Hunterdon | results by district, "OFFICIAL RESULTS" (its "Totals" row) | none |
| Morris | summary report, "OFFICIAL RESULTS" | 6 votes (0.005%) |
| Ocean | "Ocean County Board of Canvassers Report", its 33 municipalities added up | none |
| Sussex | countywide summary, "OFFICIAL RESULTS", "Amended Summary Results" | 8 votes (0.016%) |

None misses by more than 0.5%, so the clerks' check holds no county.

The other released counties' clerks' sites, read after 10:45 UTC, are recorded, not routed round:
- Middlesex, Passaic, Somerset and Warren refused (HTTP 403). Essex's results page answered, but its results host refused (403).
- Hudson and Monmouth answered HTTP 202 with an empty body. Salem gave a bot challenge.
- Burlington's and Cape May's pages answered, but those read did not lead to the 2024 results.
- Cumberland's summary report heads itself "Unoffical" (sic), so it is not the official results.
- Within the five: Hunterdon's results by municipality reset the connection; its results by district answered. Sussex's county site gave the proxy's 502; the clerk's own site answered.

**What it gives** [measured].
- **Released:** 983 local contests and 40 questions.
- **Held:** 315 local contests and 9 questions by county, and 3 local contests by check 4 (1 after the correction below).
- **p for the released.** 52 get p for the first time: 43 by the model's route from like past races, 9 by its transferred normal route. 246 keep p = 0: one name on the ballot for each seat. The other 685 stay without p, for the model's usual reasons. The most common is that MEDSL gives no vote-for-N (397); 70 are specials, and most of the rest have too few like races.
- **No question gets p.** 38 are local measures, whose threshold is the one state law sets for their kind; 2 give one answer only.
- **The 2024 back-tests take in the released contests.** The classes back-test's 2024 has 2,313 races (from 2,270): 218 finished within their window, against 289.0 expected (from 214 against 284.5). The partisan back-test's 2024 has 977 races with a lean (from 968). The calibration file's numbers move, but no verdict does: the near-tie calibration stays out.
- **No p moves outside New Jersey.**

**Check 4's bound, corrected.** *Added 2026-11-07 at 11:22 UTC, at the orchestrator's ruling of 11:16: "Bound each contest by the precinct's ballots cast (votes + overvotes + undervotes, MEDSL's CONTEST TOTAL, taking the largest of any contest in that precinct) times vote-for-N, and keep holding contests whose vote-for-N is unknown... Reason: the bound must be one no real count can break; ballots cast is that bound, and the president's votes are not."*

Why the first bound was wrong [measured]. Both Camden contests that check 4 held equal the clerk's official counts to the vote:
- county clerk: Lampitt 149,690, Exler 84,229, write-ins 166;
- sheriff: Billingham 148,470, Williams 85,637, write-ins 217.

The file shows why. In Camden Ward 3 District 1, 319 ballots were cast. For president, 22 were overvoted and 2 left blank, so the president has 295 votes; the Senate and House have 299, and the sheriff has 302. A ballot spoiled or left blank for president still counts for sheriff.

How ballots cast are read (`pipeline/local_nj.py`, `medsl_rows`). For each vote-for-1 contest in a precinct (MEDSL's magnitude 1, which every federal office has), take its votes plus overvotes plus undervotes, or its "CONTEST TOTAL" row where that is larger. The precinct's ballots cast are the largest of these. Vote-for-N contests are left out, since there each ballot counts N times. Not every county's rows carry overvotes and undervotes [measured: 12,908 undervote and 6,979 overvote rows in the file]. Where they are missing, the contest's own votes are the bound, as before.

Where MEDSL gives no vote-for-N, the number of candidates named is used. A contest over that bound stays held, and its reason says that its vote-for-N is not given. I read "keep holding contests whose vote-for-N is unknown" as those the check holds, since the bound cannot then clear them [inferred].

What it changes [measured]. Camden's county clerk and sheriff are released and get p (6.0 in a million each). Delanco Township's board of education stays held, at 334 votes against 327 ballots, with one candidate named. So 985 local contests and 40 questions are released; 315 local contests and 9 questions are held by county, and 1 by check 4. The partisan back-test's 2024 has 979 races with a lean (from 977). No verdict moves. No p moves outside New Jersey.

## 14. Louisiana's own official 2023 results

*Added 2026-11-07 at 11:53 UTC, at the orchestrator's orders of 10:35 ("LA 2023 (Oct 14, Nov 18) by the same script") and 11:16: "the Secretary of State certifies these counts itself, and 2023's ballots carry no federal contest to gate against. So the gate is: (a) the date is marked official on the site's list, as in #62; (b) each contest's parts (parishes or precincts, whichever the workbook gives) add to its total; (c) the statewide offices of Oct 14 equal the Secretary of State's own posted statewide results for that date. A contest that fails (b) or (c) is held. Mark each record "gate: within the certifying source (no federal contest on the ballot)". Reason: #62 showed this publisher's files and your script read certified counts exactly; what is left to catch in a new year is the script's read, which (b) and (c) test."*

**Why.** Louisiana elected its legislature, its statewide officers and most of its parishes' and towns' offices in 2023. Klarner's returns end in 2022, and MEDSL holds no 2023. The state's own file is the only source taken in.

**Source** [measured]. The same site and script as §12 (`pipeline/intake/la_sos.py --year 2023`). The site's list holds seven 2023 dates, all marked official: 2023-01-14, 02-18, 03-25, 04-29, 10-14, 11-18 and 12-16. Their workbooks hold 1,024 contests: 1, 1, 62, 82, 628, 248 and 2.

**The gate** (`pipeline/local_la.py`, `source_gate`; `data/local/check-la.json`, under `2023`) [measured].
- **(a)** All seven dates are marked official on the site's list.
- **(b)** In all 1,024 contests, the parishes' or precincts' lines add up to the total.
- **(c)** The site posts its own results of each date for the contests on more than one parish's ballot (its `RacesCandidates_Multiparish` and `Votes_Multiparish` files, read 2026-11-07 at 11:34 and 11:46 UTC). The ruling names the statewide offices of 2023-10-14. I applied it to every multi-parish contest of every date, a wider read of the same check [inferred: within the ruling's reason]. All 149 equal the workbooks, choice by choice: 101 on 2023-10-14 (the governor, the four other statewide offices, the four amendments, BESE, the legislature, judges and one town's tax), 33 on 2023-11-18, 9 on 2023-04-29, 5 on 2023-03-25 and 1 on 2023-02-18. A parish's own contests are not in those files, so (b) is their check.
- **Held:** none. Every record carries `gate`, whose `by` reads "within the certifying source (no federal contest on the ballot)".

**Rounds** [inferred: the source's dates and the contests it repeats]. The spring pair is 2023-03-25 and 2023-04-29: all 9 contests of the general were on the primary. The fall pair is 2023-10-14 and 2023-11-18: all 130 contests of the general were on the primary. The House's 93rd district had a special election on 2023-02-18 and 2023-03-25. So 2023-03-25 is both a primary and a general; a contest on it is the deciding round only where it was on 2023-02-18. La. R.S. 18:402 is cited for the pairing's form only, as in §12.
- **Two exact ties.** Two generals of 2023-11-18 tied: Cameron Parish's Police Jury District 5, 178 to 178, and Opelousas's Alderman District A, 224 to 224. The source holds each again on 2023-12-16, between the same two candidates (225 to 187 and 183 to 164). The general stays its contest's deciding round, with no winner marked and a note on the record. The election of 2023-12-16 is a new election, so it is treated as a special: recorded, p not computed. *Since §16 each tied general carries `result.tie` and `result.tie_settled`, with La. R.S. 18:512(C) as `data/law/ties.json` records it. Since §15 Cameron's general gets p (0.0021), as police jurors are classed with councils; Opelousas's class still has too few like races (67).*
- **Other dates.** 2023-01-14's one contest (Turkey Creek's mayor) is on no pair's date: a special election [inferred], recorded, p not computed.

**The legislature** (`data/state-lower/2023/LA.json`, `data/state-upper/2023/LA.json`; `legislature_records`) [measured]. 98 contests: 77 House and 21 Senate.
- The 76 contests of 2023-10-14 are first rounds: recorded, p not computed (model section 7), in the words Klarner's Louisiana first rounds carry.
- The 20 of 2023-11-18 are deciding rounds. They take Klarner's runoff route (route (d), `pipeline/local.py`), as Klarner's Louisiana runoffs of 2019 do. Each is classed "runoff after an open or general first round", and by whether the first round's leader of the two led by 10 points or more, read from the 2023-10-14 count. The like past runoffs are Klarner's of 1967-2022: 181 within 10 points and 199 ahead by 10 or more. All 20 get p, from 1.4 to 7.1 in 10,000.
- The 93rd district's special (2 contests) is recorded, p not computed.
- Unopposed seats are not on Louisiana's ballot, so the source holds none [inferred].

**Local races** (`data/local/2023/LA.json`) [measured]. 618 contests, 34 of them statewide or state offices.
- First rounds, not computed: 496.
- Specials (the two new elections after ties, and Turkey Creek): 3, not computed.
- Deciding rounds: 119. 9 get p by the like-race classes, from 3.1 in 10,000 to 3.0 in 1,000. 93 have too few like races in earlier years. 17 are between a Democrat and a Republican, among them the runoffs for Secretary of State, Attorney General and Treasurer. Their route, the transferred route (a), gives p only in a year whose own back-test on that year's local races holds (the orchestrator, 06:16). 2023's local races in the sources are Louisiana's alone, too few for that back-test [inferred]. So those 17 are not computed, and the record says why.
- **Left out:** the governor. It is D2's level, now in `data/governor/2023.json` (D2's #74; this section first said `data/governor/` held even years only, true when written). The gate's check (c) compared it, and it is equal.

**Questions** (`data/measure/2023/LA.json`) [measured]. 307: 8 statewide amendments (4 on 2023-10-14, 4 on 2023-11-18) and 299 local questions. The amendments are held back, as 2024's are, by La. Const. art. XIII §1(C) (§8, §12). They join step (a)'s list. The site's posted file gives each amendment's full title, which step (a) can read. The local questions wait on step (b).

**How 2023 is forecast, and what it does not feed** [inferred: the safer default, put to the orchestrator]. *Superseded by §16: at the orchestrator's ruling of 11:56, 2023 now feeds the later years' like races and measures, the back-tests and the robustness test.* 2023's p come from earlier years only: Klarner's runoffs of 1967-2022, MEDSL's like local races of 2018-2022, and like measures of 2016-2022. 2023 is not added to any later year's like races, or to the back-tests or the calibration's robustness test (`ODD_YEARS` in `pipeline/local_medsl.py`). Adding it would change 2024's forecasts and the test's verdicts, which no ruling has weighed. For the same reason, 2023's records carry no `calibration_not_of_record`.

**What moves elsewhere** [measured]. No p outside Louisiana's 2023 moves. The back-tests and the calibration file are unchanged. In 2024, only the 241 committees change, as §12 says.

**Found, not yet changed.**
- **Police jurors.** The office type reads "Police Juror" as "sheriff or constable", through the word POLICE. A police jury is a parish's governing body [inferred: the office's name and its districts], so it belongs with "council, commission or board". This is the same kind of error as the committees': a like-race class must hold like races (the orchestrator, 11:30). It touches 246 contests of 2023, 5 of 2024 and 3 of 2020. The 3 of 2020 are like races in 2022's and 2024's classes, so the fix can move p there. It is put to the orchestrator, with the moves to be listed. *Fixed at the orchestrator's order of 11:56: §15.*
- **One question.** "Parishwide Criminal Justice Proposition, 3.16 Mills Renewal" is read as a judge's retention, through the word JUSTICE. It is local and gets no p either way.

## 15. Office types read by the office: the keyword audit

*Added 2026-11-07 at 12:32 UTC, at the orchestrator's order of 11:56: "fix police jurors as their own PR with the moves listed, classing them as the parish's governing body ("council, commission or board"). In the same PR, list for each office type the twenty most common office names it catches, and fix any other misreading of the same kind. Reason: a keyword reads words, not offices, and one misread word moved 254 contests."*

**How I looked** [measured]. For each office type I listed the office names it catches, most common first (`pipeline/office_types_audit.py`, written to `data/local/office-types-top20.json`). I also listed every name that two types' words match, every match that falls inside a longer word, and every name left as "other local office". The misreadings were of four kinds: a type's word inside a longer word or a place's name; another type's word in an office's name; a short form or a misspelling the words did not know; and lines that are not offices at all.

**Fixed** (`pipeline/local_medsl.py`: `OFFICE_TYPES`, `PLACE_NAME`, `STATE_OFFICE_TYPES`, `SEAT_DISTRICT`; `office_type` now takes the state and the district):
- **Governing bodies read by another type's word.**
  - Louisiana's police jurors: 254 contests, from "sheriff or constable" to "council, commission or board", as ruled.
  - Kentucky's magistrates and justices of the peace: 501, from "judge" to council. They sit on the county's fiscal court, its governing body: "Counties shall have a Fiscal Court, which may consist of the Judge of the County Court and the Justices of the Peace" (Ky. Const. §144, read 2026-11-07 at 12:06 UTC from the Legislative Research Commission, https://apps.legislature.ky.gov/law/constitution/constitution/viewconstitution?rsn=164) [stated]. That the ballot's "Magistrate" is the justice of the peace is [inferred].
  - New Hampshire's Executive Council (15, from mayor), Delaware's levy courts (10, from judge), Arkansas's city directors, and New Jersey's township committees (164, from "other" and "special district").
- **Officers read as judges or as a commission.** Court clerks and registers of probate: 1,493 from "judge" to "clerk, treasurer or other county officer". Georgia's tax commissioners and Alabama's revenue commissioners: 213 from council to the officers. Kentucky's county judge/executive: 109 from "judge" to "mayor or executive". The county judge sits on the fiscal court (Ky. Const. §144) [stated]; that the office is the county's executive is [inferred: its name]. Louisiana's "Constable, Justice of the Peace": 98 from "judge" to "sheriff or constable"; it is the constable of a justice of the peace's court [inferred: the sources hold separate "Justice of the Peace" contests, 88 of them].
- **A word inside another word, or a place's name.** WATER in Waterloo, Waterford, Bridgewater and Edgewater; FIRE in Foxfire; COURT in Courtland and Camden County's "Courthouse District"; WARD in Howard; PORT in Southport, Newport and Port Republic; PARK in Elk Park, Lake Park and Roselle Park; MARSHAL in Marshall. These words are now whole words. A park or a port counts only with its body's word ("Park District", "Port Authority"). A place's name is taken off before the office's words are read ("Town of Elk Park ...", "Edgewater Park Township - ...", "Park County ...", "Mayor, Town of Melville"), and only where the place's words hold no office's word ("County Commissioner Fairfield Township District" keeps its words).
- **TRUSTEE no longer means a school board.** Iowa's township trustees (2,280) go to council. Its hospital and sanitary district trustees (109) go to "special district".
- **Short forms and misspellings**, read in their own state where elsewhere they mean another thing (Texas's "ESD" is an emergency services district):
  - New Jersey: "BOE" and "Bd of Ed" (249, to "school board"), "Regional - ..." school districts, "Coun." and "Comm.".
  - Arizona: school districts (USD, ESD, UHSD, HSD, MCCCD, EVIT; 138) and "JP" (16).
  - Texas: "JP", "CDC", "DA", "Co Comm" and "Tax A-C" (70).
  - Indiana: "MSD" and "SB". Kentucky: "... Independent" school boards. Arkansas: "NWACC".
  - Everywhere: Florida's community development districts and "CDD" (369), Nebraska's natural resources districts (222), South Carolina's public service districts, Vermont's high bailiffs, "Commisioner", "Commmission", "Commissi0ner", "Tustee", "Treas", "Clrk" and "Supv".
- **Seats named by their city alone.** Arkansas's "City of Bentonville" with the district "Ward 1, Pos 2" is read by its district, as council (56) [inferred: Arkansas's councils are elected by ward and position].
- **Lines that are not offices.**
  - Straight-party tallies are left out: 6, North Carolina's four towns of 2011 and South Carolina's two of 2024.
  - Questions filed as offices under a question's name are read as questions, in `data/measure/`: 10 (Washington's advisory votes, New Jersey's public questions, Utah's form of government, North Dakota's county newspaper). 9 records are added, and Hoboken's 2024 yes is joined to its no, already there.
  - None gets p as a question. The advisory votes' answers are "Repealed" and "Maintained", not a yes and a no, and the rest are local.
- **Legislatures filed as local offices.** These are now read as the legislature (`LEG_NAMES`): Rhode Island's 2022 house and senate (113, "Representative/Senator in General Assembly"), Virginia's 2018 House of Delegates 8th district (1) and one Arizona district's 2022 representatives (1). Virginia's is a special and now sits in `data/state-lower/2018/VA.json` (see the fixes below).
  - Klarner's 2022 check now holds Rhode Island's 113 districts: all 113 have identical D and R votes, and 1 winner differs. No state's hold changes.
  - Rewriting 2018's check also shows 22 North Carolina districts as "within 1 point, counts differ". The file last written at 62123d0 read them as identical. The hold counts only differences over 1 point, so it does not change [measured].

**What moves** [measured]. Every move is listed in `data/local/moves-office-types.json`, against `ce8e7d5`.
- **Type changes.** 7,638 local and primary records change type. The largest moves:
  - school board to council: 2,455;
  - judge to the officers: 1,493;
  - "other" to special district: 547;
  - judge to council: 521;
  - council to special district: 323;
  - "other" to council: 303;
  - sheriff to council: 279;
  - "other" to school board: 266.
- **p.** 5,976 p move (5,628 local, 346 primary, 2 state senate), as the classes' like races change. The median move is by a factor of 1.12, and 90% are within 1.26. The largest is 2.46, and 8 move by more than 2.
- **Computed or not.** 136 are now computed (98 local, 38 primary). 103 are no longer computed, because their class now has fewer than 100 like races in earlier years. 72 of these are school boards: 66 of 2020 (South Carolina 24, Kentucky 19, North Carolina 16, Virginia 4, and one each in DC, Nebraska and West Virginia) and 6 of North Carolina's later years (3 of 2024, 2 of 2026, 1 of 2023). Their classes now hold 90 to 99 like races: "local school board, nonpartisan, 3 candidates" (70) and one of three seats at once (2) [measured]. *Corrected 2026-11-07 at the orchestrator's word of 13:54, from M2's count (check c24): this line said 69 of North Carolina's 2023 school boards, whose class lost the sanitary district trustees, which the moves file does not bear out.*
- **Removed and added.** 131 records leave `data/local/`. 9 are added to `data/measure/`.
- **The state senate.** Rhode Island's 2 computed state senate p of 2024 move, now that its 2022 legislature is read as the legislature.

**Verdicts** [measured]. Every back-test and the robustness test keep their verdicts.
- **Like-race classes** (`calibration-local.json`): not adopted. The test still does not pass; leaving out 2022 does not pass, and leaving out 2024 does. The cells made worse go from judge, "other local office" and sheriff or constable to judge alone.
- **The partisan route**: not adopted, as before.
- **The State Board's** (`backtest-ncsbe.json`): local and primary are not adopted, and no test's pass changes. One part moves: leaving out 2024, local's fit now improves (it did not before), but it still does not pass.
- **Measures** (`data/measure/backtest-measures.json`): unchanged.

**Fixed after M2's check of #73 (check c24)** [measured]. *Added 2026-11-07 at 14:16 UTC, at the orchestrator's order of 13:54: "1. VA 2018 HoD-8, a special, left the local file in #73 and is now in no file, because there is no VA 2018 state file. Put it back in data/state-lower/2018/VA.json, as a special, with its old fields. No contest should drop out of the record. 2. 167 school superintendents are typed 'school board'. A superintendent is one executive seat, not a board. Type them as officers and list the moves. 3. REPORT §15 says 69 of the 103 newly uncomputed are NC's 2023 school boards ... Correct the text. Reason: the record keeps every contest it has read, and a type has to describe the office."* Every move is listed in `data/local/moves-fixes-c24.json`, against `1a6d752`.
- **Virginia's 2018 House of Delegates, 8th district.** It is back in the record, in `data/state-lower/2018/VA.json`, as a special ("general, special"), with its old fields: the candidates and votes, the total, the four counties (51045, 51121, 51161, 51775), and the office as filed ("House Of Delegates"). Klarner's record holds Virginia's lower house in other years but none in 2018, so the contest fills a vacancy [inferred; MEDSL does not mark it special]. Its p is not computed, as for every special: the model's forecasts are fitted to regular elections. In `pipeline/local_medsl.py`, a legislature contest filed as a local office is now kept, as a special, wherever Klarner holds no regular race of that state, year and chamber.
- **School superintendents.** 176 contests, not M2's 167, were typed "school board" and are now "clerk, treasurer or other county officer": an office whose words name a superintendent (SUPERINTENDENT, SUPT or SUPER. OF PUBLIC INSTRUCTION) with SCHOOL, EDUCATION or INSTRUCTION. They are Alabama 61, Montana 47, Florida 30, Arizona 17, Illinois 16, Georgia 2, South Carolina 2 and North Carolina 1; 64 of 2018, 47 of 2020, 2 of 2022, 62 of 2024 and 1 of 2000. Four of them are statewide offices filed in the local files (Georgia's State School Superintendent of 2018 and 2022, South Carolina's State Superintendent of Education of 2018 and 2022), which the twenty-names list leaves out, so that list moves 172. A water superintendent stays a special district. No p becomes computed or uncomputed: the 134 computed keep their p but one, Montana's 2024 Superintendent of Schools in county 30093, which leaves the school boards' own fit and falls by a factor of 2.0 (0.000181 to 0.0000907). 866 other p move, as the like races of their class or of the fit's pool change: from ×0.9830 to ×1.0067, by a median factor of 1.003, 90% within 1.007 (867 p moved with Montana's). *Corrected 2026-11-07 after M2's check c29 §29.1:* this line first said 1,720 p moved; 854 of those 1,720 keep their p, and only their p block's not-of-record factor moved (calibration_not_of_record, 0.7951 to 0.791). The moves file now codes them 'C' [measured: p before equal to p after in `data/local/moves-fixes-c24.json`]. 165 uncomputed contests keep their reason with a changed count of like races.
- **The count above** is corrected in place.
- **Verdicts.** None changes. In `calibration-local.json` and the two local back-tests only numbers move: the like-race route's test deviance after calibration goes from 17.35 to 17.42, and 2024's seen over expected from 0.707 to 0.706. Nothing else in `data/` moves but stamps.

**The twenty names each type catches most often** (as filed; counts of contests; school board and the officers as rewritten after M2's check below) [measured]:

- **council, commission or board** (23,633 contests, 9,003 names): County Commissioner (1,651); Advisory Neighborhood Commission (568); Magistrate (481); County Commission (426); County Commission Member (317); County Council (274); Single Member District (271); City Council (262); County Board Of Supervisors (154); County Agricultural Extension Council (116); County Commissioner Term Commencing 01/02/2025 (86); County Commissioner Term Commencing 01/03/2025 (86); County Commissioner: Term Commencing 01/02/2021 (85); County Commissioner: Term Commencing 01/03/2021 (85); Member City Council (85); Board Of Commissioners (77); County Commissioner District 1 (46); Member Town Council (45); Board Of Commissioners District 2 (44); Board Of Commissioners District 3 (42)
- **school board** (8,330 contests, 3,318 names): Member Board Of Education (944); Board Of Education (578); School Board (366); School Board Member (270); County Board Of Education Member (235); Community College District Trustee (65); Member Of Board Of Education (55); Member School Board (51); Board Of Education District 1 (50); Board Of Education District 2 (49); Board Of Education District 3 (40); Board Of Education District 4 (32); Board Of Education District 5 (31); School Board Trustee (28); Board Of Education At-Large (27); School Board Of Trustees (27); School Trustee (26); Board Of Education District 6 (20); Local School Board District (20); New Hanover County Board Of Education (17)
- **clerk, treasurer or other county officer** (8,050 contests, 2,354 names): County Treasurer (412); Coroner (403); Registrar Of Voters (369); County Recorder (349); Clerk Of Superior Court (323); County Clerk (175); County Engineer (173); Register Of Deeds (173); Tax Commission (157); Superior Court Clerk (155); County Coroner (144); Assessor (131); Circuit Court Clerk (120); Clerk Of Court (118); County Auditor (112); Surveyor (99); Property Valuation Administrator (90); Clerk Of The Court Of Common Pleas (87); Circuit Clerk (75); County Surveyor (59)
- **special district** (4,182 contests, 1,319 names): Soil And Water Supervisor (427); Soil And Water Conservation District Supervisor (277); County Soil And Water Conservation District Commissioner (118); Soil And Water Conservation District Commissioner (98); Water District Director (67); Soil And Water (65); Soil And Water District Supervisor (55); Soil And Water Conservation District Supervisors (52); Soil Conservation District Supervisor (51); County Public Hospital Trustee (44); Healthcare District Director (32); Soil And Water District Commission (31); Recreation And Park District Director (28); Community Services District Director (25); Fire Protection District Director (22); Public Utility District Director (22); Irrigation District Director (17); Garrison Diversion Conservancy Director (15); Natural Resources District Board Of Directors - Central Platte (11); Natural Resources District Board Of Directors - Nemaha (11)
- **mayor or executive** (3,981 contests, 1,542 names): Mayor (165); County Judge Executive (108); City Of Charlotte Mayor (19); Parish President (19); City Of Fayetteville Mayor (15); City Of Durham Mayor (14); County Executive (13); City Of Greensboro Mayor (11); City Of Burlington Mayor (10); City Of High Point Mayor (9); Town Of Mooresville Mayor (9); City Of Archdale Mayor (8); City Of Clinton Mayor (8); City Of Elizabeth City Mayor (8); City Of Monroe Mayor (8); City Of Raleigh Mayor (8); Town Of Atlantic Beach Mayor (8); Town Of Harrellsville Mayor (8); Town Of Jamestown Mayor (8); Town Of Matthews Mayor (8)
- **sheriff or constable** (3,449 contests, 634 names): Sheriff (977); Constable (503); County Sheriff (281); County Constable (189); Jailer (107); Constable, Justice Of The Peace (89); Sheriff/Coroner (38); Mobile County Constable (25); Jefferson County Constable (16); Walker County Constable (14); Conecuh County Constable (11); Jackson County Sheriff (10); Maricopa County Constable (10); Bladen County Sheriff (9); Clay County Sheriff (9); Graham County Sheriff (9); Polk County Sheriff (9); Randolph County Sheriff (9); Union County Sheriff (9); Wilcox County Constable (9)
- **judge** (3,107 contests, 1,342 names): Justice Of The Peace (309); District Judge (146); Judge Of Probate (143); Probate Judge (140); Justice Of Peace (127); District Court Judge (93); Chancery Court (55); Circuit Judge (53); Cook Circuit Court Judge (46); Judge Of District Court Incumbent (42); Chief Magistrate (41); Magistrate Judge (41); Circuit Court Judge (27); Judge Of Circuit Court Incumbent (27); Court Of Appeals (26); Judge Of The Court Of Common Pleas - Term Commencing 01/01/2019 (24); County Court (23); Judge - Orphans Court (23); Judge Of The County Court - Term Commencing 01/01/2019 (20); Judge Of The Court Of Common Pleas Term Commencing 01/01/2025 (20)
- **prosecutor** (1,351 contests, 406 names): County Attorney (363); Prosecuting Attorney (285); District Attorney (135); Commonwealth'S Attorney (67); Solicitor General (31); Attorney (18); Solicitor (10); County Attorney/Public Administrator (9); State Attorney (7); Attorney General (5); City Attorney (4); Countywide Prosecuting Attorney (4); Prosecuting Attorney Ter (3); Santa Cruz County Attorney (3); Columbia County District Attorney (2); County District Attorney (2); County Prosecuting Attorney (2); Crawford County District Attorney (2); Dodge County District Attorney (2); Douglas County District Attorney (2)
- **party committee** (241 contests, 205 names): Rpec Member(S), At Large (12); Dpec Member(S), At Large (7); Rpec Member, District 4 (4); Rpec Member, District 5 (4); Dpec Member, District 2 (3); Rpec Member, District 3 (3); Rpec Member, District 7 (3); Dpec Member, District 1 (2); Dpec Member, District 10 (2); Dpec Member, District 3 (2); Dpec Member, District 5 (2); Rpec Member, District 1 (2); Rpec Member, District 8 (2); Rpec Member, District 9 (2); Dpec Member At Large, District 11 (1); Dpec Member At Large, Division A (1); Dpec Member(S), District A (1); Dpec Member(S), District B (1); Dpec Member(S), District C (1); Dpec Member(S), District D (1)
- **other local office** (100 contests, 71 names): Lieutenant Governor (6); Secretary Of State (5); Director Of Human Services - Glocester (2); Director Of Public Welfare - Hopkinton (2); Director Of Public Welfare - Scituate (2); Director Of Social Services - Exeter (2); Moderator - Barrington (2); Town Moderator - Charlestown (2); Town Moderator - Exeter (2); Town Moderator - Foster (2); Town Moderator - Jamestown (2); Town Moderator - Little Compton (2); Town Moderator - Scituate (2); Town Moderator - West Greenwich (2); Town Sergeant - Exeter (2); Town Sergeant - Foster (2); Town Sergeant - Glocester (2); Town Sergeant - Hopkinton (2); Town Sergeant - New Shoreham (2); Town Sergeant - Scituate (2)

**Open, not changed.**
- **Arkansas's justices of the peace** (252, judge). They sit on the county's quorum court, its governing body, under Ark. Const. amend. 55 [inferred, not read]. The law could not be read. FindLaw's page answered with a bot check (403), Justia's with 403, the Secretary of State's PDF link with 404, and the Legislature's link served an image. I did not route around these refusals; they are put to the orchestrator.
- **Indiana's township trustee** (19, council). It is the township's executive [inferred, not read].
- **The "Parishwide Criminal Justice Proposition"** (§14) is read as a retention, through the word JUSTICE. That is a measure's kind, not an office type. It is local and gets no p either way.
- **100 contests remain "other local office".** Most are Rhode Island's town moderators, sergeants and directors of welfare, which have no like type, and the statewide primaries' lieutenant governors and secretaries of state.

## 16. 2023 feeds the later years, and the two ties marked

*Added 2026-11-07 at 12:43 UTC, at the orchestrator's ruling of 11:56: "Yes, 2023 feeds later years' like races, back-tests and the robustness test, as Klarner's and the State Board's odd years already do. Reason: earlier cycles only means every earlier contest, and leaving one year out would be an exception with no reason behind it. Make it its own PR with every move listed. If any verdict changes, report it before the PR, since the tests decide as fixed." And: "The two exact ties on Nov 18 are the very event the site is about, so mark each plainly in the record (result.tie: true), with how it was settled (the new election of Dec 16) and LA's tie rule cited from data/law."*

**What changes in the code** (`pipeline/local_medsl.py`, `pipeline/local_la.py`):
- **Like races and measures.** 2023's local races and measures are added to the like races and like measures of every later year, as every other year's are. 2023's own p still come from earlier years only, so none of them moves.
- **The legislature.** Louisiana's 20 legislative runoffs of 2023 are added to the like past runoffs of later years (`local_la.class_rows`). No 2024 legislative contest takes the runoff route, so nothing there moves.
- **Back-tests and the robustness test.** 2023 is now scored in `backtest-local-classes.json`, the measures' back-test and `calibration-local.json`. So 2023's records now carry `calibration_not_of_record`, the factor the test keeps out of p.
- **The partisan route (a).** 2023 stays out of its back-test, since that route gives no forecast in 2023 to score (§14; the orchestrator, 12:42).

**The ties** [measured; the rule stated, its reach to local offices inferred]. Each tied general of 2023-11-18 (Cameron Parish's Police Jury District 5, 178 to 178, and Opelousas's Alderman District A, 224 to 224) now carries `result.tie: true` and `result.tie_settled`.
- `tie_settled` gives how the tie was settled: a new election of the same contest, between the same candidates, on 2023-12-16. That date is the fourth Saturday after the tied general, as the rule sets.
- It also gives Louisiana's rule as `data/law/ties.json` records it: La. R.S. 18:512(C), "If, as a result of a tie vote in a general election, the number of candidates who would be elected to an office exceeds the number of persons to be elected to the office, the candidates who received the same number of votes for that office in the general election are not elected. The election for officers thus not elected shall be returned to the people on the fourth Saturday after the election date at which the tie vote occurred."
- The law file marks the rule's reach to parish and municipal offices as inferred, and the record keeps that mark.

**What moves** (rebuilt at 12:39 UTC; every move in `data/local/moves-2023-feed.json`, against `bd3ae34`) [measured]. All the moves are in 2024.
- **141 local p rise by a factor of 1.42.** They share one class: "local council, commission or board, one major party against others, 2 candidates". Its like races go from 219 to 237, and its window around ½ narrows.
- **62 local races are now computed.** Their class, "local council, commission or board, two or more of one major party, 2 candidates", now has 116 like races, once Louisiana's 2023 runoffs are in. By state: Washington 23, Louisiana 21, Mississippi 8, New York 5, others 5.
- **43 statewide measures' p fall by a factor of 0.964.** Louisiana's 8 amendments of 2023 join the 215 like measures. They have no forecast of their own (§14), but their finishes are like measures. The note on these p for near-even finishes now reads 54 against 38.1, where it read 52 against 36.4.
- **Not listed as moves.** 383 not-computed reasons change only in their count of like races. 2,208 records change their `calibration_not_of_record`, 18 of them 2023's own, new. 59 North Carolina records change only their code stamp.

**Verdicts** [measured]. No route's adoption changes. One leave-one-year-out result changes, and it was reported to the orchestrator before this PR (the orchestrator's answer, 12:42: "No adoption changes, so open the PR as planned").

The like-race classes (`calibration-local.json`), before and after:

| | Before (2022 and 2024 scored) | After (2022, 2023 and 2024 scored) |
|---|---|---|
| Full test | 2,441 contests; improves; judge made worse; fails | 2,521 contests; improves; judge made worse; fails |
| Leaving 2022 out | 2,331 contests; judge made worse; fails | 2,411 contests; judge made worse; fails |
| Leaving 2023 out | (no such check) | 2,503 contests; judge made worse; fails |
| Leaving 2024 out | 110 contests (2022 only); no cell made worse; passes | 128 contests (2022 and 2023); council made worse; fails |
| Adopted | no | no |

- **Leaving 2024 out.** The check now scores 2022 and 2023: 128 contests, 18 of them 2023's. That brings council to 5 seen, so the cell is tested. Its factor moves the expected count from 4.6 to 3.7, away from the 5 seen, so the cell is made worse and the check fails.
- **The partisan route:** not adopted, as before.
- **The State Board's routes** (`backtest-ncsbe.json`): unchanged.
- **The measures' back-test** (`data/measure/backtest-measures.json`): no pass or fail changes; its expected counts move by 0.1.


## 17. Local questions' thresholds, read from state law (step (b))

*Added 2026-11-07 at 13:37 UTC, at the orchestrator's ruling of 06:16: "local thresholds read from the governing state law or p not computed (never inferred ½)". The order is from the ruling of 11:56, and the go-ahead from 12:44 ("Push (b)"). Under the ruling of 07:21, a statute may be read through Justia or Cornell LII where the state's own code site refuses; such a reading is marked as read via a compilation.*

**Which questions can take a rule.** A rule can be applied only where the source shows the question's place. That holds for North Carolina's State Board, Louisiana's Secretary of State and Indiana's own file.
- MEDSL counts a local question once per county and does not show which place holds it. Its p stays not computed, as before.
- MEDSL holds 4,346 local question titles that appear in one county only. Counting those as single places is a possible later step. It is not taken here.

**What was read** [measured]. Readers (Sonnet) read the law for each kind of question in the three states' files, and D3 checked their work. Every quote was compared word for word against the page saved when it was read, with only whitespace, quote marks and dashes normalised. The rules are in `data/measure/thresholds-local.json`.

| State | Questions | Kinds with a rule | Rules | Stated | Inferred | Not covered |
|---|---|---|---|---|---|---|
| North Carolina (ncleg.gov) | 870 | 863 | 39 | 22 | 17 | 7 |
| Louisiana (legis.la.gov) | 619 | 608 | 16 | 8 | 8 | 11 |
| Indiana | 33 | none | none | | | 33 |

- **Stated** means the law's words name the kind of question. **Inferred** means the reader joined a general rule to the question, and the rule's `match_note` says how.
- **Every threshold read is ½ of those voting on the question** [measured over the rules]. No supermajority was found for any local question in these two states.
- **Indiana is not read.** Indiana's code site (iga.in.gov) returns the same script shell for every address (4 addresses, 12:46 to 12:47 UTC). Cornell LII holds no Indiana code; it links to iga.in.gov. Justia answered 403 with a challenge page (13:32 UTC). That part stopped there, and Indiana's 33 questions carry this reason. Read or not, they would take no p yet: Indiana's own file is of 2024 only, so its class has no earlier year.

**How a rule is matched** (`pipeline/measures.py`, `local_rule_for`).
- A question takes the first rule, in the file's order, whose pattern its title matches (with `match_also` and `dates` where they are set). So one place's own act comes before the general law.
- A rule with a `hold` gives no p, and its reason says why: the source does not show which law governs the question, or the law leaves the threshold open.
- An advisory rule gives no p, because no threshold applies.
- A compound rule, a second test the counts do not show, is refused, as for statewide questions.
- A question no rule matches says so.
- A tax, bond or fee proposition whose title names a justice system is now read as a measure, not a retention. Examples are Louisiana's "Parishwide Criminal Justice Proposition, 3.16 Mills Renewal" and Washington's "City of Langley Sales and Use Tax for Criminal Justice". This fixes the keyword audit's open item (§15).

**The forecast** (D3-v1.1, like past measures). Each state's local questions form their own class, `local measure, NC` or `local measure, LA`. A class is fitted on that state's local questions of earlier years that the source counts whole, and it needs at least 100 of them.
- For North Carolina, that is the State Board's local questions on every date.
- For Louisiana, it is the Secretary of State's questions of 2023, which fit 2024. Louisiana's 2023 questions have no earlier year, so their p is not computed.
- p is model §7's threshold form, as for statewide questions.

**What moves** [measured]. The build was rerun at 13:33 UTC. Every move is listed in `data/measure/moves-local-thresholds.json`, against `de31d9b`. No p moves, and no p is lost.

*Now computed: 800.*
- **North Carolina: 496.** 190 are on MEDSL's general dates and 306 on the State Board's other dates. p runs from 1.2e-6 to 0.041, with a median of 1.9e-4.
- **Louisiana 2024: 304.** p runs from 3.2e-6 to 0.084, with a median of 7.6e-4.

*Still not computed, with a new reason: 381 in North Carolina, 315 in Louisiana, 33 in Indiana and 1 in Washington.*

North Carolina's 381:
- **216 "other" general obligation bonds are held.** G.S. 159-61(a) asks for a majority of those voting. But a bond whose proceeds may serve a service district needs a majority in the whole unit and in the districts at once (G.S. 153A-308, 160A-543), and the source does not show whether a given bond does. School, community college and county library bonds take p.
- **77 have fewer than 100 like questions in earlier years.**
- **63 are held because a local act may govern them.** The source does not show whether the question was put under the general law read or under a local act, which was not read. These are charter amendments (28), fire district taxes (16), the structure of county boards of commissioners (10), city special taxes (5), county special taxes (2), Greensboro's term lengths (1) and Leland's annexation (1).
- **7 statewide questions fall on the State Board's other dates.** They are not computed in this step.
- **7 are not covered by any rule.**
- **4 half-cent transit taxes are held.** G.S. 105-509.1 adds a majority in each county of a multicounty district.
- **3 sales or leases of city enterprises** (Salisbury, Davidson, Mooresville) are held.
- **The rest are 1 each.** Asheville's water system is held. One school tax title does not name its Article. Caswell's zoning question is advisory. Rowan-Salisbury's 2024 question is held, because S.L. 2024-2 asks for "the majority of the qualified voters of Rowan County", which may mean all qualified voters.

Louisiana's 315:
- **287 are 2023 questions with no earlier class.**
- **17 are held.** These are fire protection district parcel fees (6) and service charges (3), where the source does not show which act governs; hotel taxes (3), each on its own act; charter-section amendments whose title does not name the charter (3); a Lawrason Act adoption (1); and one gravity drainage acreage tax (1). The acreage tax is compound: R.S. 38:1783 also needs "a majority in number of acres voting".
- **11 are not covered by any rule.**

The other two states:
- **Indiana's 33** say their law is not read.
- **Washington's 1** (Langley) changes from local retention to local measure.

**The back-test, out of sample** [measured]. Local questions are scored apart from statewide ones, so the statewide counts stay as they were.
- **Statewide** (`data/measure/backtest-measures.json`, `at_threshold`): unchanged, at 65 measures. Within 2 points, 3.6 were expected and 8 seen.
- **Local, on MEDSL's general dates** (`at_threshold_local`): 494 questions.
- **Local, on North Carolina's other dates** (`data/local/backtest-ncsbe.json`, `questions_at_threshold`): 306 questions.

Expected against seen:

| | Questions | Own window | Within 1 point | Within 2 points | Within 5 points |
|---|---|---|---|---|---|
| Louisiana 2024 | 304 | 14.2 / 14 | 7.1 / 8 | 14.2 / 14 | 39.7 / 41 |
| North Carolina, general dates | 190 | 6.5 / 5 | 6.5 / 5 | 15.6 / 11 | 38.9 / 30 |
| North Carolina, other dates | 306 | 19.6 / 23 | 10.9 / 15 | 28.8 / 31 | 65.6 / 82 |

No calibration is applied, as for every route since 09:49 (§7).

**Verdicts** [measured]. The back-test files were compared with main's. The only differences are the new local keys. No pass or fail changes, and no route's adoption changes. `calibration-local.json` and `backtest-local-*.json` change only in their stamps, which were put back.

**Open readings for the orchestrator.** Each of these is a looser reading of the law, which this step does not take.
- **The 216 "other" bonds.** They could take ½ with the service-district test noted, since most county and city bonds serve no service district [inferred, not read].
- **The 63 North Carolina questions and Louisiana's fire and hotel questions.** They could take the general law, unless a local act is found.
- **Three of the 4 transit taxes** (Durham 2011, Orange 2012, Wake 2016). These were single-county referendums, which the multicounty test does not reach, by the reader's own reading. Mecklenburg's 2025 tax may rest on an act of 2025 that was not read.

## 18. The lean note: the two tests of 11:01, as amended at 13:52

*Added 2026-11-07 at 14:01 UTC, at the orchestrator's word of 13:39: "The local questions' back-test leans (NC other dates within 5 points: 82 seen against 65.6 expected). Apply the 11:01 rule to each local-question route: a note only where the share test and the vote test both count and agree. Do it in the next PR." The rule of 11:01 is in `data/congress/REPORT.md` §3.*

*The ruling of 13:52 came after a first run, which this section also reports. It was fixed before any new count was taken:*
1. *"the ladder starts lower (10, 100, 1,000, 5,000, 10,000, 20,000, 50,000 votes; still the smallest rung with 5 or more expected), and (v) doesn't count where its line holds more than half the pool's contests. Where only (s) counts, the note stands on it, as before."*
2. *"By pool, as now. A note reports the back-test of the forecasts that made that p, and each pool is its own back-test."*
3. *"retake the statewide measures' note under the amended rule with today's counts."*

*Reason for 1:* "a test that counts almost every contest measures the whole forecast, not the near-tie density that p depends on."

**The rule** (`pipeline/local_medsl.py`, `lean_note`).
- **(s)** Seen against expected within 1 point of the threshold. The statewide classes use 1 point of ½, the point every statewide p of record is taken at.
- **(v)** Seen against expected within k votes of the threshold. k is the smallest of 10, 100, 1,000, 5,000, 10,000, 20,000 and 50,000 votes at which 5 or more are expected.
  - "Within k votes" is |yes − t(yes + no)| ≤ k/2. At t = ½ that is a margin of k votes or fewer.
  - Whether a question finished within k votes is counted in whole votes, k included: with t = a/b, |2b·yes − 2a(yes + no)| ≤ b·k, in integers (since §23; the share form in floating point dropped two questions at a margin of exactly 10).
  - Each question's expected chance is its class's share of earlier questions within that many votes, taken as a share: |s − t| ≤ k / (2(yes + no)).
- **When a test counts.** A test counts only with 5 or more seen or expected. (v) does not count where its line holds more than half the pool. "Holds" is read here as the questions that finished within the line.
- **When the note stands.**
  - Where both tests count, the note stands only if they lean the same way.
  - Where only one counts, the note stands on that one.
  - Where neither counts, there is no note.
- **What the note says.** It names the counts it stands on, and says p may be low (more near-even finishes than forecast) or high (fewer).

**The pools.** Each pool is one build's own back-test of one class: the forecasts that made its p.
- **Louisiana's local questions.**
- **North Carolina's local questions on the even years' November general dates** (`pipeline/local_medsl.py`).
- **North Carolina's local questions on the State Board's other dates** (`pipeline/local_ncsbe.py`).
- **The statewide classes near ½.** This is the pool the note of 07:25 was taken on: every statewide question whose class has earlier years.

**The tests under the amended rule** [measured]. They are in `data/measure/backtest-measures.json` (`lean_notes_statewide`, `lean_notes_local`) and `data/local/backtest-ncsbe.json` (`questions_at_threshold.lean_note`). The vote lines are in `near_votes`.

| Pool | Questions | (s) within 1 point, seen / expected | (v) k, seen / expected | The note |
|---|---|---|---|---|
| Statewide measures, 2018-2024 | 259 | 11 / 6.8, more | 20,000 votes: 10 / 6.2, more | **stands**, both tests: p may be low |
| Statewide retentions, 2018-2024 | 79 | 2 / 0.0 (does not count) | under 5 expected at every line | none; no retention has p |
| Louisiana's local questions, 2024 | 304 | 8 / 7.1, more | 10 votes: 9 / 17.6, fewer | **none**: opposite ways |
| North Carolina, general dates, 2016-2024 | 190 | 5 / 6.5, fewer | 100 votes: 19 / 17.4, more | **none**: opposite ways |
| North Carolina, other dates, 2012-2026 | 306 | 15 / 10.9, more | 10 votes: 25 / 21.9, more (23 before §23) | **stands**, both tests: p may be low |

**The first run, under the rule of 11:01 as written.** In the first run the ladder started at 1,000 votes. That line held most of each local pool: 244 of Louisiana's 304, 67 of North Carolina's 190 general-date questions and 202 of its 306 other-date questions. So each pool's (v) was close to a count of all its questions. Every local note stood, and North Carolina's two pools leaned opposite ways. That was put to the orchestrator, and the ruling of 13:52 answered it.

**The other levels under the amendment** [measured: my own implementation after M2's `checks/m2/c16_notes.py`, on the files' forecasts of record (M2's set B)]. The amendment changes a verdict only where a new rung (10 or 100 votes) reaches 5 expected, or where the chosen line holds more than half the pool. Neither happens at any level:

| Level, years | Contests | Expected / seen within 10, 100, 1,000 votes | k before and after | k's line holds |
|---|---|---|---|---|
| House, 2010-2024 | 2,997 | 0.16 / 1; 1.6 / 1; 16.0 / 24 | 1,000; 1,000 | 24 of 2,997 |
| Senate, 2010-2024 | 255 | 0.01 / 0; 0.05 / 0; 0.5 / 0 | 10,000; 10,000 | 4 of 255 |
| Governors, 2006-2024 | 216 | 0.01 / 0; 0.08 / 0; 0.85 / 0 | 10,000; 10,000 | 4 of 216 |
| Governors, odd years, 1985-2021 | 29 | 0.0 / 0; 0.01 / 0; 0.08 / 0 | none of the rungs reaches 5 in these 29 | |

- So no House, Senate or governor verdict changes under the amendment.
- The odd years' note rests on D2's own back-test, of more races than the 29 with p [inferred]. Its line, 50,000 votes, holds 9 races, under half of that pool's 29 or more, and the new rungs are below 1,000 votes, where its 29 races expect 0.08.
- **The statewide measures' verdict is unchanged.** The note stood under the rule of 07:25 (54 against 38.1 within 5 points), and it stands now on both tests.

**What moves** [measured], against main (`e41dca5`).
- **No p moves.**
- **306 notes are added**, on North Carolina's local questions on the State Board's other dates.
- **65 statewide measures' notes are reworded.** They were "54 against 38.1 within 5 points". They now read "11 against 6.8 within 1 point of ½, and 10 against 6.2 within 20,000 votes". They still say p may be low.
- **Louisiana's and North Carolina's general-date local questions get no note.**
- **Nothing else in any record changes.**

## 19. Each held statewide question's own ballot text (step (a))

*Added 2026-11-07 at 14:35 UTC, at the orchestrator's order of 07:25: "each statewide measure's own ballot text, for the 85 held back by an exception and the 16 untyped". By the time they were read, 98 were held by an exception and 16 were untyped. Two later words govern parts of this section. At 14:06: "The AZ Legislative Council's analyses on azleg.gov are that body's own publication, so they are a true source. Record maine.gov's 403 and hold ME's Q1/Q5." At 14:21 the orchestrator agreed to the three calls below. On Georgia's 2018 B it said: "read its ballot text. If the text shows it exempts property from ad valorem tax, the constitution governs it and it is stated. If the text doesn't show that, hold it. Reason: the ½ must come from the law, and only the kind of act may be read from the ballot."*

**What was read** [measured]. 114 questions in 12 states. Four readers worked by group: Florida (24); Louisiana, Arkansas and Georgia (24); Colorado, Arizona and New Mexico (36); Oregon, Maine, Ohio, Idaho and Rhode Island (30). Their pages were fetched between 13:45 and 14:01 UTC.
- **What each reader recorded.** For each question, the reader recorded where its type is read (with a quote) and what the text shows on the case of the state's special rule (`fact.applies`: true, false, or null where the text read does not show it, with a quote, a why and a mark).
- **Two more questions.** I added Rhode Island's two other bond projects of the same acts, 2022's and 2024's Green Economy Bonds. They were typed by their titles and held as compound, so they were not in the list. I read them from the pages the readers saved.
- **Quotes.** All 267 quotes were checked word for word against the saved pages, bad: 0.
- **Where they are.** Everything is in `data/measure/ballot-texts.json`, with every page refused or not reached.

**How a text decides** (`pipeline/measures.py`, `rule_for`).
- **The type.** Where the title leaves the type open, or says otherwise, the type comes from the text. The `matched` line says "states" where the text states it and "shows [inferred]" where it does not. Three types are normalised to the rules' own:
  - Florida's revisions from the Constitution Revision Commission become amendments. Art. XI §5(e) sets one rule for "the proposed amendment or revision".
  - Georgia's referendums on general Acts become statutes.
  - Maine's citizen initiative and its State Referendum become statutes [inferred].
- **The special case.**
  - Where the text shows the special rule's case holds, the special rule applies. Where it shows the case does not hold, the general rule applies. Either way the mark is carried into `matched`.
  - Where the text does not show it, p is held. The reason then says the ballot text does not show it either.
- **Each record** carries what decided it, in `ballot_text` (`data/README.md`).

**The three calls, agreed at 14:21.**
- **Oregon's Measure 115 (2024).** Or. Const. art. II §23(1) reaches "any proposed requirement for more than a majority of votes cast by the electorate". 115's two-thirds is of the House and the Senate, not of the electorate. So §23(1) does not apply, and the general ½ does [inferred]. The reader had marked it true and left the reading to me.
- **Rhode Island's bonds.** The act that puts a year's bonds on the ballot sets their share in its own §3: "If a majority of the People voting on the proposition in Section 1 hereof shall vote to approve any project stated therein, said project shall be deemed to be approved by the People." That is P.L. 2022 ch. 231 and P.L. 2024 ch. 117, art. 5 [stated]. 2018's act (P.L. 2018 ch. 47, art. 5) prints its changes to the bill; with struck words dropped, it reads the same.
  - I added one rule per act to `thresholds.json`, each for its own year (`from_year`, `to_year`), at t = ½.
  - Each of the 10 projects is matched to its act's list by title and amount.
  - The act numbers 2024's projects 1 to 4, where the ballot's questions are 2 to 5. Question 1 was the convention.
- **Georgia's referendums.** I added a rule, a statute at ½, under Ga. Const. art. VII §II ¶II(a)(1): "no property shall be exempted from ad valorem taxation unless the exemption is approved by two-thirds of the members elected to each branch of the General Assembly in a roll-call vote and by a majority of the qualified electors of the state voting in a referendum thereon". It is read from the legislature's 2016 annotated edition, like Georgia's other rules. It covers only an Act exempting property from ad valorem taxation (`only_if`).
  - 2018's Referendum A (HB 820) and 2024's (HB 808) are such Acts, each stated by its own §2, which cites the paragraph. Each Act's §3 says the same in votes cast: "If more than one-half of the votes cast on ... such question are for approval of the Act".
  - **2018's Referendum B is held.** Neither its ballot text nor the Act's own text was read. The legislature's bill page is built by script and gives no text, and sos.ga.gov refused (403). The Legislative Counsel's summary of Act 25 says its Section 2 "expands the ad valorem tax exemption for nonprofit homes for the mentally disabled", but that summary is not the ballot text.

**Refused or not reached** (recorded and not tried another way; `ballot-texts.json`, `unread`):
- Georgia: sos.ga.gov (403, Cloudflare); Justia's copy of the constitution (403); and the legislature's bill page for HB 196 (script, no text). The legislature's own 2016 constitution was read instead.
- Arizona: the Secretary of State's 2024 pamphlet, apps.azsos.gov (403, Cloudflare). The Legislative Council's analyses on azleg.gov were read in its place, ruled a true source at 14:06.
- Oregon: the Secretary of State's measure search (captcha) and oregonlegislature.gov (403). The Secretary of State's own Voters' Pamphlets (county editions, each printing every statewide measure) were read.
- Maine: maine.gov, twice (403, CloudFront). This is why Q1 and Q5 are held.
- Ohio: ohiosos.gov (403). The Supreme Court of Ohio's pages were read.
- Rhode Island: vote.sos.ri.gov, sos.ri.gov and elections.ri.gov (403, Cloudflare). The General Assembly's public laws were read.

**What the texts show** [measured, as the readers marked them]. For all but three (Georgia's 2018 B, Maine's Q1 and Q5), the text settles which rule applies.
- **Florida (24).** Not "an amendment that imposes a new State tax or fee" [inferred], so 60%. No sentence says so outright, and each full text was read for tax, fee, levy and the like.
- **Colorado (19).** 2018's Amendment A and 2024's Amendment J only repeal (½); the other 17 do not (55%) [stated].
- **New Mexico (4).** None restricts the elective franchise or the education rights of art. VII and art. XII (½) [stated].
- **Arizona (13).** 133-140 are amendments and 311-315 statutes. None approves a tax (½) [inferred]. 311's $20 penalty is the closest call.
- **Louisiana (19).** None directly affects five parishes or fewer (½) [inferred].
- **Arkansas.** Issue 2 was initiated (½) [stated]. Issue 1 was referred by the General Assembly. Its rule, art. 19 §22, does not state its base, so it stays held as compound.
- **Idaho (3).** Statute initiatives (½) [stated].
- **Ohio (2).** Neither is an initiated amendment the ballot board found to conflict with art. II §1e(B)(1), which would be put as two questions (½) [inferred, weak for 2018].
- **Oregon (12).** No measure sets a supermajority of the electorate (½) [inferred].
- **Maine.** Questions 2 to 4 are bonds (½). Q1 and Q5 are held.
- **Rhode Island (10).** Bonds, under each act's §3 (½) [stated].
- **Georgia (2 of 3).** As above.

**What moves** [measured], against main (`2827d85`). Every move is in `data/measure/moves-ballot-texts.json`.
- **67 statewide measures get p.** Statewide measures with p go from 65 to 132, of 356. By state: AZ 13, LA 13, CO 10, FL 9, RI 7, OR 5, NM 3, ME 3, AR 1, GA 1, ID 1, OH 1.
- **45 more have their threshold read but no p.** They are 2016's 17 (no earlier year) and 2018's 28 (83 like measures in earlier years, under 100).
- **4 stay held by their state's law.** Arkansas's 2024 Issue 1 (compound), Georgia's 2018 B, and Maine's Q1 and Q5.
- **No other record changes.**

**The back-test** (`data/measure/backtest-measures.json`, `at_threshold`, each question at its own t, out of sample) [measured].

| | Measures | Own window, expected / seen | Within 1 point | Within 2 points | Within 5 points |
|---|---|---|---|---|---|
| Before (2022, 2024) | 65 | 3.6 / 8 | 1.8 / 4 | 3.6 / 8 | 9.9 / 24 |
| Now (2022-2024) | 132 | 7.8 / 9 | 4.0 / 4 | 8.3 / 10 | 22.7 / 37 |

- **The statewide note is unchanged.** It is taken near ½ on every statewide question whose class has earlier years, whether or not its threshold is read. It still stands on both tests (11 against 6.8 within 1 point of ½, and 10 against 6.2 within 20,000 votes). The 67 new p carry it.
- **The questions with p alone** now finish near their own threshold much as forecast, within 1 and 2 points. Within 5 points they still run high, 37 against 22.7. These are counts, not a test of the rule of 11:01.

**Open, not changed.** Where several general rules of one type set the same share, `threshold.citation` names the first in the file. For example, Oregon's 115, referred by the legislature, cites art. IV §1(4)(d), the initiative's rule, though art. XVII §1 governs a referral. The share is the same, but the cited section is not always the governing one [measured for Oregon; not checked for every state].

## 20. Two fixes from the check of #81, and the statewide questions filed as local

*Added 2026-11-07 at 15:11 UTC, at the orchestrator's word of 14:36: "Two fixes go in your next PR, with the misfiled statewide questions: 1. Citations. Cite the rule that governs each question by its kind, not the first general rule in the file that sets the same share. ... Reason: a citation has to be the law that actually governs the question, even when the share is the same. 2. The notes on supermajority p. ... a p taken at t ≠ ½ carries a note only from a back-test near its own threshold, under the 11:01 rule ... If neither test counts, the p gets no note. The note near ½ stays only on p taken at ½. Reason: a note reports the back-test at the point where its p is taken. List every note that changes." The questions themselves follow the word of 13:54: identify them "from the state's own list of that year's statewide measures where it answers, so they are marked stated ... Use your title count only where the state refuses".*

**Fix 1: the governing rule** (`pipeline/measures.py`, `proposer_of` and `_one`) [measured]. Where several rules of one type set the same share, the question's proposer chooses among them.
- **Who proposed it.** It is read from the question's ballot text where step (a) read one (`ballot_text.proposer`; Oregon's 12 from the voters' pamphlets and Ohio's 2 were added), or else from its title's own words ("INITIATIVE PETITION", "LEGISLATIVE REFERENDUM", "HJR", ...). The rules in `thresholds.json` now carry `proposer` (28 rules in 10 states).
- **One rule left.** The citation is that rule, and `matched` says "proposed by the X [mark], so C governs".
- **Several left.** Where the source does not show who proposed it, every rule that could govern is cited, "A, or B", with the others in `threshold.also_governs`. One law read two ways (Wyoming's art. 20 §1, alone and with its statute) is cited once.
- **What changed.** 75 records, every one in `data/measure/moves-citations-notes.json`, taken against `8b794e7`. No p figure moved.
  - A single, right citation now: Oregon's 5 legislative referrals (art. XVII §1, was IV §1(4)(d)); Montana's 4 initiated amendments (XIV §9(3), was §8); Ohio's two Issue 1s (II §1b, was XVI §1); Oklahoma's 4 initiative petitions (V §3, was XXIV §1); DC's Initiative 83 (unchanged, now with its proposer).
  - Every candidate cited, where the source does not show the proposer: Oklahoma 10, North Carolina 6, Alaska 5, North Dakota 5, Michigan 2, Missouri 2, Montana 2, New York 1, and Nebraska's 2022 Amendment 1 (held, compound either way).
  - North Dakota's "art. III, sec. 8 (and sec. 9)" and "art. III, sec. 9" both stand for an initiated amendment; the file reads the same law twice there, and both are cited [measured; not merged].

**Fix 2: a supermajority p's note** (`pipeline/local_medsl.py`, after the measure loop) [measured]. The near-½ note is written only on a p taken at ½. A p taken at t ≠ ½ takes its note from `lean_notes_statewide_own_threshold`: the 18 statewide questions given a forecast at a threshold other than ½, each tested within 1 point and within k votes of its own t.
- Within 1 point, 0.9 were expected and 0 seen; under 5 are expected at every vote line. Neither test counts, so these p carry no note.
- **The 18 notes removed**, each listed: Colorado's 2022 Amendments D, E, F and 2024 G, H, I, K, 79, 80 (55%), and Florida's 2022 Amendments 1-3 and 2024 1-6 (60%). The join below leaves this unchanged.

**The statewide questions filed as local** (`pipeline/local_medsl.py`, `join_statewide`; `data/measure/statewide-filed-local.json`).
- **What MEDSL did.** It files 35 statewide questions in its local files: 1,420 lines, once per county (Alabama's 2020 amendments, 67 each; Illinois's 2024 advisory questions, 102 each) or once for the whole state (Arkansas's 2016 issues, Florida's 2016 Amendment 1, Rhode Island's 2016 questions). Washington's 2018 Advisory Vote 19 is one line of 38 counties plus King County's own line, "King County Advisory Vote No. 19".
- **What was read.** Two readers read each state's own list of that year's statewide measures, 14:37 to 14:58 UTC. All 35 are on their state's list. The readers checked their 213 quotes word for word against the saved pages, and I checked again the 144 the record uses (`statewide-filed-local.json`), bad: 0.
  - Arkansas: the Secretary of State's table of initiatives and amendments. Florida: the Division of Elections' 2016 booklet. Louisiana: the Secretary of State's 2018 list. Alabama: the certified Final Canvass. Montana: the Secretary of State's 2020 ballot issues page.
  - Arizona: the Legislative Council's results memo of 4 December 2018 (azleg.gov, ruled a true source at 14:06); azsos.gov refused (403, Cloudflare). Washington: the Secretary of State's results site. Illinois: the State Board of Elections' statewide advisory questions. Minnesota: the Secretary of State's ballot questions.
  - Rhode Island's election sites refused earlier today and were not asked again. Its 7 rest on the General Assembly's own acts, which put each one to the state's electors at the November 2016 general election: P.L. 2016 ch. 142 art. 5 (the five bonds), ch. 5 (the Tiverton gaming question) and Resolution ch. 329 (the ethics amendment). No title count was needed.
- **Marks.** 31 are matched to their entry [stated]. 4 are [inferred]: Arkansas's Issue 3, whose wording differs from the list's ("Concerning" against "to Encourage"), and Illinois's three, which the State Board's document lists without numbers.
- **The join.** Each question's lines become one statewide record, its votes added answer by answer, its counties and precincts together. Whether it covers the state is still read from them (`measures.scope_of`), and all 35 do. Each record names its list in `listed_statewide`, with the type, proposer and special-rule fact the list shows (`data/README.md`).
- **Against the state's own figures**, where a page read prints them (`listed_statewide.state_total`) [measured]. Alabama's 6, Montana's LR-130 and Arizona's 127 agree to the vote. Arkansas's 4 differ by 0 to 25 votes. Washington's run below the state's by 806 to 3,322 votes a side: 2018's Advisory Vote 19 and 2024's four initiatives. The counts shown are MEDSL's, as for every other question; none of the differing ones has a p.

**What the lists settle** [as marked].
- **Types.** As the lists print them: amendments, Montana's LR-130 a statute referred by the legislature, Rhode Island's bonds, Washington's initiatives statutes, and Illinois's and Washington's 2018 advisory votes. Rhode Island's question 1 is the referendum on the Tiverton gaming act (art. VI §22), not an amendment, though its title reads "State Constitutional Approval".
- **Special rules.**
  - Arkansas: Issue 6 was initiated ("Petition"), so amendment 7 governs (½); Issues 1-3 were referred by the legislature ("Legislature"), so art. 19 §22 governs, compound [stated].
  - Florida's Amendment 1: not an amendment imposing a new State tax or fee; its full text, printed in the booklet, has no tax or fee [inferred], so 60%.
  - Louisiana's 6: none names a parish or municipality [inferred], so ½.
  - Rhode Island's bonds: each is a project of the proposition P.L. 2016 ch. 142 puts to the people, and that act's §3 sets the share: "If a majority of the people voting on the proposition provided for in section 1 hereof shall vote to approve the proposition as to any project provided for in section 1 hereof, said project shall be deemed to be approved by the people." I added that rule to `thresholds.json` for 2016 alone, as the 14:21 word did for 2018, 2022 and 2024 [stated]. Question 1 needs a majority statewide and in Tiverton (compound).

**What moves** [measured], against `6dd29ef`. Every move is in `data/measure/moves-statewide-filed-local.json`.
- **The 35.** Statewide measures go from 356 to 391, and local records from 10,447 to 9,027. 15 of the 35 have their threshold read:
  - 1 gets p: Montana's 2020 LR-130 (½), 1.24 × 10⁻⁶, which finished at 50.96%.
  - 14 have no p for want of like measures: 2016's 9 (no earlier year) and Louisiana's 2018 6 (95 like measures in 2016, under 100).
  - 9 are held by their state's law: Arkansas's Issues 1-3, Rhode Island's question 1, Washington's 2024 four (art. II §1(d)'s turnout test) and Minnesota's 2024 Amendment 1 (a majority of all voting at the election).
  - 7 have their law unread: Alabama's 6 (its code site cannot be read) and Arizona's 2018 Prop 127 (Arizona's rules are read from 2023).
  - 4 are advisory: Illinois's 3 and Washington's 2018 Advisory Vote 19.
- **Every later p.** 26 of the 35, those with a yes and a no in 2016, 2018 or 2020, enter the like-measures pool of every later year: 2022's grows from 170 to 196, 2023's from 215 to 241 and 2024's from 223 to 249. So all 132 statewide p of 2022-2024 move, by a factor of 0.93 to 1.13 (median 1.12). 2018's 59 held questions now count 95 like measures, not 83.
- **The near-½ note** still stands on both tests, and its counts change: 12 seen against 9.1 expected within 1 point of ½, and 11 against 6.9 within 20,000 votes (281 questions, was 259). The 114 p at ½ carry the new figures, and the 18 at other thresholds carry none.
- **The back-test at each question's own threshold** (`at_threshold`, all years), now with 2020's one: 133 measures; own window, 8.7 expected against 10 seen; within 1 point, 4.7 against 5; within 2 points, 9.1 against 11; within 5 points, 23.4 against 38.

**Refused or not reached** (`statewide-filed-local.json`, `unread`): Rhode Island's three election sites (not asked again); apps.azsos.gov (not asked) and azsos.gov (403, Cloudflare); Washington's 2018 voters' pamphlets and 2024 signed certification (404); Minnesota's canvass report (no content); the Illinois Secretary of State's Blue Book (curl error); and ilga.gov. **ilga.gov:** its TLS chain is incomplete at the site. The reader added the missing intermediate certificate, with verification on, and fetched three pages before being told to stop. Those pages are listed as unread and nothing from them is used, since a tool's failure is reported, not worked around.

## 21. The certified count wins (the ruling of 2026-11-07 15:16)

The ruling, verbatim: "the certified count wins. Where a state page that prints totals marks them certified or official, its totals are the statewide record's counts, shown and used in every pool. MEDSL's sum stays beside them with the difference. Where the page carries no such mark, MEDSL's counts stand and the difference is recorded, as now." Its reason: "a figure shown has to be the count of record, and the certifying source is that count."

It touches the 17 joined statewide questions (§20) whose state page prints the statewide totals. Each one's `state_total` in `data/measure/statewide-filed-local.json` now carries `certified`: whether the state marks those totals certified or official, with the words and where they stand, or a note on why not. `pipeline/local_medsl.py` (`certified_count`) takes the state's figures answer by answer where they are marked, and stops the build if an answer does not match by name.

**Marked, so the state's counts are the record's (10)** [stated]:
- **Alabama 2020, six amendments.** Every page of the Secretary of State's "Final Canvass of Results" ends "Certified by the State Canvassing Board November 23, 2020". Its totals equal MEDSL's to the vote, so only the source of the counts changes.
- **Washington 2024, four initiatives (2066, 2109, 2117, 2124).** The results page carries no mark on its totals, so I looked further on the Secretary of State's own pages. Its "2024 General Election" data page links "Official Canvass of the Returns G2024_ Certification 12 04 2024 (.pdf)", read 2026-11-07T15:21:00Z (sha256 168f9d69…8582d). Page 1 begins: "I, Steve Hobbs, Secretary of State of the State of Washington, do hereby certify that according to the provisions of RCW 29A.60.250, I have canvassed the returns of the 3,961,569 votes cast in the November 5, 2024 General Election by the registered voters of the state for all statewide measures, …". Page 10 is signed and sealed on December 4, 2024.
  - The PDF is a scan with no text layer, so its words and figures were read by eye from the page images and not checked by machine. The record says so (`certified.read`).
  - Its four measures' figures equal the results page's to the vote, and that page is text, checked word for word.
  - MEDSL's sums are short by 1,708 to 3,322 votes an answer. The counts move:

| Initiative | Yes, MEDSL → certified | No, MEDSL → certified |
|---|---|---|
| 2066 | 1,938,152 → 1,941,474 | 1,811,213 → 1,813,169 |
| 2109 | 1,362,567 → 1,364,510 | 2,435,100 → 2,437,419 |
| 2117 | 1,434,889 → 1,437,103 | 2,338,369 → 2,340,077 |
| 2124 | 1,665,224 → 1,668,435 | 2,074,571 → 2,077,216 |

**Unmarked, so MEDSL's counts stand and the difference is recorded (7):**
- **Arkansas 2016, four issues.** The Secretary of State's table "Initiatives and Amendments, 1938-2018" prints no word certified or official. It differs from MEDSL by 0 to 25 votes.
- **Arizona 2018, Proposition 127.** The Legislative Council's memo of December 4, 2018 is not a certification. It agrees with MEDSL.
- **Montana 2020, LR-130.** The Secretary of State's report is headed "2020 STATEWIDE GENERAL ELECTION CANVASS", but the words certified and official do not appear. It agrees with MEDSL to the vote, so nothing turns on it.
- **Washington 2018, Advisory Vote 19.** The results page carries no mark. The site's index says "Election results are certified by each county on November 27, 2018. The Secretary of State certifies final results by December 6, 2018." and "The results posted before certification are unofficial.", and the page was last updated "11/27/2018 4:27 PM". So its totals are likely the certified ones [inferred], but the page does not say so.
  - The Secretary of State's 2018 data download (`2018-general-data.zip`, its "FINAL 2018Gen - Cong by District.pdf") prints the same total, also unmarked.
  - No certified canvass of 2018 was found on the Secretary of State's results pages.
  - MEDSL is 1,628 short on Repealed and 806 short on Maintained.

**What moves** (`data/measure/moves-certified-count.json`, every record against the commit before):
- 17 records change. 10 take the state's counts, of which 4 (Washington's) change their figures. 7 keep MEDSL's.
- No p moves. Washington's initiatives get no p: their threshold turns on turnout as well as the yes share. Alabama's figures are unchanged.
- The four Washington questions also enter the like-measures pool of 2025 and 2026 (North Carolina's). Their yes shares move by less than 0.0002, no question crosses a window's edge, and no p of those years changes.
- Every other file is unchanged, the stamps apart.

## 22. One-county titles: counted whole where the place lies wholly in the county (item 5)

The order, verbatim: "count one whole only where the place it names lies entirely within that county, by the Census Bureau's place-to-county relationship file. Hold the rest." Its reason: "a question can sit in one county's file only because another county's file is missing it." A place that lies wholly in one county has no voters in another, so its question's count in that county is the whole count.

**Which questions.** 3,972 local questions of 2016-2024 are counted by MEDSL in one county's file only: the same state, title, subject and date in no other county. They are in `local_medsl.one_place`, run on every year's contests after the states' own files have replaced MEDSL's.

**The file.** The Census Bureau's `national_place_by_county2020.txt` (codes2020) lists each place once for each county it lies in. It was read 2026-11-07T15:32Z (sha256 9996494d…6ec6), through `pipeline/fetch.py`, into the cache.
- Only active incorporated places are read (TYPE "INCORPORATED PLACE", FUNCSTAT "A"). A census designated place has no government to put a question, and a consolidated city's balance is not a place of its own.
- The county is that of 2020. For other years it is [inferred]: an annexation across a county line would not show.

**How a title names a place** (`pipeline/places.py`):
- **[stated]:** the title says "City of X", "Town of X", "Village of X" or "Borough of X", and X is the state's one place of that kind.
- **[inferred]:** the title says one of those, but the Census calls the place another kind ("City of Highfill" is Highfill town). This fallback is not used for "Town of" in the states whose towns are county subdivisions (CT, MA, ME, NH, NY, RI, VT, WI, MN): there the Town of Poughkeepsie is not the City of Poughkeepsie.
- **[inferred]:** the title begins with an incorporated place's name ("Mesa-Question 2", "Florence Cannabis Question", "20-253 Eugene Marijuana Tax"), after an Oregon measure number is taken off.

**Guards**, each found by reading every match of the trial by hand:
- **A district, county, parish or township in the title is held.** This covers school words and Arizona's "ESD", "UHSD" and "Union #", a board of education ("BOE"), "Unified" and "College". Examples: "Stevensville Elementary School District", "Avondale Esd #44 Question", "Woodcliff Lake Boe Public Question".
- **A special body after a leading name is held** (fire, library, park, cemetery and the like). Examples: "Sequim Library Capital Facility Area", "Spangle Cemetery".
- **A name joined by a hyphen to another name is held** ("Caldwell-West Caldwell"). A question's word after the hyphen ("Mesa-Question 2") or a spaced dash ("Camilla- Sunday Sales") is not a join.
- **A leading name whose next words make a longer name, or whose kind word is not the place's, is held.** Examples: "Ogden Valley City" is not Ogden city, and "Kenai Peninsula Borough" is not Kenai city.
- **A leading name that is also a county's name, with that county as the record's, is held.** Examples: "Greenville Capital Projects Sales Tax", "Butler Cannabis Question". The county's own question is the likelier reading.
- **A leading name that is also a town's or township's in the same county is held.** This uses the Bureau's county subdivision file `national_cousub2020.txt`, read only for this, active governments only. Examples: "Chester Proposition Two" (Chester town and Chester village), "Abercrombie Home Rule Charter". It does not apply where the title states the kind ("Bordentown City", "Corning City").
- **A name that is more than one place in the state is held.**
- **A place in more than one county, or in another county than the record's, is held.** Examples: Portland, Lake Oswego, Bothell, Atlanta, Wheeling.
- **A retention is held:** a judge is retained by a court's district, not a place.

**Counts** (all years):

| | questions |
|---|---|
| counted whole, the place [stated] | 442 |
| counted whole, the place [inferred] | 280 |
| held: the title names no incorporated place | 1,345 |
| held: the title names a district, county, parish or township | 938 |
| held: a retention | 880 |
| held: the place lies in 2 or 3 counties | 50 |
| held: a county of the same name is the record's | 20 |
| held: a special body after the name | 9 |
| held: the name is also a town's or township's in the county | 5 |
| held: hyphen join, name goes on, or another county | 3 |
| total | 3,972 |

By year, the whole questions are 259 (2016), 109 (2018), 52 (2020), 6 (2022) and 296 (2024).

**What moves** (`data/measure/moves-one-county.json`, every record against the commit before):
- **The 722 whole questions.** Each gets `place_whole` and a note, and is no longer "counted by county".
  - 705 of them now say why their p is not computed in their state's own terms: "the thresholds of this state's local questions are not read". Only Louisiana's and North Carolina's local laws are read (step (b)).
  - Louisiana's 8, all of 2020, take step (b): 5 have too few like measures for a p, and 3 are of a kind whose law was not read.
  - 9 keep their reason (redacted precincts, one answer only, a county that does not add up).
  - No whole question gets a p.
- **Louisiana's like-local-measures pool.** Louisiana's 8 of 2020 now enter it.
  - All 304 of Louisiana's local p of 2024 move by ×1.0435. Their pool goes from 299 to 307 questions, and from 14 to 15 within the window of ±2 points of ½.
  - The 287 of 2023 still have no p: the pool before them grows from 0 to 8, short of 100.
- **The back-test** at each question's own threshold (`data/measure/backtest-measures.json`) moves with them. For Louisiana's local measures, all years, the own window goes from 14.2 to 14.9 expected against 14 seen, and within 1 point from 7.1 to 7.9 against 8 seen. The lean notes are unchanged.
- No candidate race and no statewide question moves.

**Not done, for a ruling if wanted:**
- Questions of a town or township (a county subdivision; New York's and New England's towns, New Jersey's townships) could be counted whole the same way by the Bureau's county subdivision file, since a county subdivision never crosses a county line. They are held now because the order names the place-to-county file.
- Questions that name a county or parish (317 of the 938 held for a district or county word) may be the county's own question when the county is the record's. They could be counted whole on that reading [inferred].

## 23. Towns, townships and counties' own questions; three readings from M2's check

*Added 2026-11-07 at 16:05 UTC, at the orchestrator's words of 15:43 and 15:50.* Every record that changed is in `data/measure/moves-towns-counties.json`, against main after #85 and M2's #69.

### 23.1 The two extensions (the orchestrator, 15:43)

The orders, verbatim:
1. "Towns and townships, from the cousub file. Count only a subdivision that is an active government (FUNCSTAT A), and hold any name that is both a place and a subdivision in that county unless the title says which ("Town of", "Village of", "Township"). Mark it stated where the title names the kind, inferred otherwise." Reason: "the Census defines county subdivisions to nest within counties, so the file itself states that the named unit lies wholly in the county."
2. "A county's or parish's own question. Count it whole only if all three hold: the title names the record's own county or parish; the title has no words of another body (district, school, hospital, fire, library, authority, board other than the county's own, and so on); the record covers that county's whole file. Mark it stated where the title names the county government ("County of X", "X County Commission", "Police Jury"), inferred otherwise." Reason: "every voter on a county's own question is in that county."

**A town or township** (`pipeline/places.py`, `_sub`). The file is the Census Bureau's `national_cousub2020.txt`, read 2026-11-07 at 15:34 UTC (§22).
- **[stated]:** the title says "Town of X", "Township of X", "Charter Township of X" or "Plantation of X", or begins "X Township", "X Twp" or "X Town".
- **[inferred]:** the title begins with the subdivision's name. This is tried only where no place matches.
- The subdivision must be an active government (FUNCSTAT A), lie in the record's county, and be the county's only subdivision of that name.

**A county's own question** (`_county`, and `local_medsl.one_place` for the third test).
- The title names the record's county as "X County", "X Parish", "County of X" or "Parish of X".
- **The third test, the whole file.** The record's precincts must equal all the county's precincts in MEDSL's file on that date. `pipeline/intake/medsl_county_precincts.py` counts them from the cached raw files, as a contest's are counted: from 2018, a precinct with a vote in any contest; in 2016, any general-election row. It writes `county-precincts-<year>.json` to the cache, and the record carries both counts (`place_whole.precincts`, `county_precincts`) [measured].
- The 20 held by this test are a county question on part of the county's ballots. Examples: Fulton County's 2016 T-SPLOST (190 of 346 precincts; Atlanta voted its own), Kittitas County's 2024 road levy (26 of 48), Latah County's 2024 recall (1 of 34), Iowa's Jefferson County Measure A (8 of 12), and Snohomish County's seven 2016 charter amendments (773 of 779).
- A county's count includes a precinct with votes for any office. A precinct that votes for federal offices only would hold back a question that was on every other ballot. This can only hold questions back [inferred].

**Guards**, each found by reading every new match of the trial by hand:
- **A leading name may go on into a longer name.** It is held where its next word, with it, begins another place's or subdivision's name in the state. "Haddon Height Proposal" is not Haddon township, since Haddon Heights is a borough. This guard is applied to places too; none of §22's 722 is lost.
- **A special body after a leading name is held**, as for places.
- **A part of the county is held:** a direction before the county's name ("South Fulton County", "Southern Sandoval County").
- **A place or town of the county also named is held** (whole word, 4 letters or more). Examples: "Jefferson County (Homewood)", "Summers County City Of Hinton Levy", "A Local Proposition For Bangor, Franklin County".
- **Something in parentheses right after the county is held** ("Delaware County (Cleora)", "Grady County (EMS)").
- **Another body's word is held**, once the county's own boards are taken off. The words are fire, hospital, library, authority, port, transit, water, sewer, sanitary, sanitation, irrigation, cemetery, drainage, levee, conservancy, conservation, airport, mosquito, city, town, township, village, borough, municipal, ward, precinct, zone, area, board, health, education and unincorporated.
  - This list also holds some questions that are the county's own. Santa Fe County's bonds for "water and wastewater projects" and "community health facilities" and McKinley County's liquor tax, partly "for ... education", are held. A question is counted whole only where its words leave no doubt [inferred].

**Counts** (all years; the build's `one-county` lines):

| | questions |
|---|---|
| whole, the place [stated] / [inferred] (§22) | 442 / 280 |
| whole, the county subdivision [stated] / [inferred] | 136 / 29 |
| whole, the county [stated] / [inferred] | 8 / 126 |
| held: the title names no incorporated place or county subdivision | 1,177 |
| held: a retention | 880 |
| held: the title names a district or a school | 620 |
| held: "Township" naming no subdivision with a government of its own | 54 |
| held: a county or parish, but not the record's | 50 |
| held: the place lies in 2 or 3 counties | 50 |
| held: another body's word in a county's question | 45 |
| held: a county of the same name is the record's (a leading place's name) | 21 |
| held: the county's own question covers fewer than all its precincts | 20 |
| held: a special body after the name | 11 |
| held: a place or town of the county also named | 8 |
| held: the name is both a place's and a town's or township's in the county | 5 |
| held: something in parentheses after the county | 4 |
| held: a part of the county | 2 |
| held: a hyphen join, a name that goes on, or another county | 4 |
| total | 3,972 |

Whole questions now total 1,021: 722 places, 165 towns and townships, and 134 counties' own questions. By year: 303 (2016), 123 (2018), 70 (2020), 6 (2022) and 519 (2024).

**What moves:**
- **299 questions are newly counted whole.** Each gets `place_whole` with its unit and a note. 290 now say why their p is not computed in their state's own terms: "the thresholds of this state's local questions are not read". 9 keep their reason. None gets a p.
- **No Louisiana or North Carolina question is newly whole.** North Carolina's come from the State Board's file, and Louisiana's MEDSL years held none that passed. So no pool of like local measures changes, and Louisiana's 304 local p of 2024 stay as they are.
- **§22's 722 are unchanged** except for `place_whole.unit` ("place").

### 23.2 Three readings from M2's check (relayed at 15:50)

1. **#80's count** (M2 c29 §29.1). "Of the 1,720 rows marked "P", 854 have p_before equal to p_after (only calibration_not_of_record moved, 0.7951 to 0.791). So 867 p moved." Reason: "a figure in the record has to say what it counts."
   - §15's line is corrected: 866 p moved, plus Montana's ×0.500.
   - `data/local/moves-fixes-c24.json` now codes the 854 rows "C" (p unchanged, the not-of-record factor moved), and its counts and `about` say so [measured: p before equal to p after in those rows].
2. **The state superintendents** (c29 §29.2). "26 of them are statewide superintendents typed as local officers... Type them as the statewide office they are." Reason: "the class decides which pool and which back-test a race falls in."
   - A superintendent's office (§15's words) in a state office's contest is now typed `statewide officer` (`office_type_in`). That means MEDSL's STATE files, or the State Board's state offices. A county's or a district's superintendent has the same words, so the words alone are not read.
   - 26 records move: 18 local and 8 North Carolina primaries. No p moves, and none becomes computed or uncomputed. Three have a p that its route does not take from the type: South Carolina's and Wyoming's of 2018 (unopposed, p 0) and North Carolina's of 2024 (a Democrat against a Republican, 3.12 × 10⁻⁷).
   - The 10 whose reason names their class now name "state statewide officer, …" (or "primary, state statewide officer, …"), with 0 or 1 like races. The other 13 keep their reason (a Democrat against a Republican with no county lean for the year, seats not in the source, a first round, a gated state).
   - 6 other North Carolina primaries keep "too few like races", with a changed count.
   - `backtest-local-partisan.json` (2024) gains a "statewide officer" row with 1 contest, and the officers' row goes from 212 to 211. In `calibration-local.json`, the partisan state officers' cell splits (deviance 11.5 to 11.75).
3. **The vote test in whole votes** (c27 §27.5). "'Within k votes' includes k. Compute it in whole votes (margin ≤ k), not in the float share form." Reason: "a test stated in votes has to be computed in votes."
   - `vote_lines` now counts |2b·yes − 2a(yes + no)| ≤ b·k in integers, with t = a/b (0.6667 read as 2/3).
   - North Carolina's other-dates pool goes from 23 to 25 within 10 votes (2016 2 to 3, 2021 2 to 3), against 21.9 expected. Its note still stands on both tests, and its 306 p's notes now read "25 against 21.9".
   - No other pool's count moved: statewide 10 against 6.2 at 20,000; Louisiana 9 against 17.6 at 10; North Carolina's general dates 19 against 17.4 at 100 [measured: `backtest-measures.json` unchanged].

**Open, for a ruling if wanted.** The same reason reaches the other statewide executive offices. Each is still typed by its words:
- state treasurers, auditors and controllers: county officer (81 records of the state files with no district or county);
- secretaries of state and lieutenant governors: "other local office" (72);
- attorneys general: prosecutor;
- commissioners of agriculture, insurance and labor: council, commission or board.

Typing them all `statewide officer` would put them in one pool. It would move more classes than item 2, so I have not done it.

## 24. Every single-seat statewide executive office typed "statewide officer" (the ruling of 16:08)

*Added 2026-11-07 at 16:18 UTC.* The ruling, verbatim: "A single-seat statewide executive office in a state office's contest is typed "statewide officer", read the way you read the superintendents. That covers treasurer, auditor or comptroller, secretary of state, lieutenant governor, attorney general, and the single commissioners (agriculture, insurance, labour, public service where one seat is elected statewide)." Reason: "the class decides a race's pool and back-test. A state treasurer's race belongs with other statewide races, not with county treasurers." Every record that changed: `data/local/moves-statewide-officers.json`, against main after #86.

**How it is read** (`pipeline/local_medsl.py`, `STATE_EXEC` and `office_type_in`):
- **The contest.** It must be a state office's contest: MEDSL's STATE files, or the State Board's state offices. It must have no district and not be one county's. A county's treasurer, auditor or superintendent has the same words, so the words alone are not read.
- **The office's whole name** must be one of these, with "State", "NC" or "Washington State -" allowed in front:
  - treasurer (State Treasurer, Treasurer of State, General Treasurer, Chief Financial Officer);
  - auditor (Auditor of State, of Accounts, of Public Accounts, Auditor General, State Auditor and Inspector);
  - comptroller or controller (Comptroller General);
  - secretary of state (of the State, of the Commonwealth);
  - lieutenant governor;
  - attorney general;
  - superintendent of public instruction (§23);
  - the single commissioners: agriculture (and Secretary of Agriculture), insurance, labor (Oregon's Commissioner of the Bureau of Labor and Industries), and public, state, or school and public lands;
  - Arizona's State Mine Inspector.

**What moves:**
- **359 records are typed `statewide officer`:** 316 local and 43 North Carolina primaries. With §23's 26 superintendents, the type holds 385. By office:

  | Office | Records |
  |---|---|
  | attorney general | 71 |
  | secretary of state | 66 |
  | treasurer or chief financial officer | 66 |
  | auditor | 43 |
  | lieutenant governor | 37 |
  | commissioners of agriculture | 19 |
  | insurance | 19 |
  | comptroller or controller | 14 |
  | labor | 14 |
  | lands | 8 |
  | mine inspector | 2 |

  Their types before were:

  | Type before | Records |
  |---|---|
  | clerk, treasurer or other county officer | 121 |
  | other local office | 108 |
  | prosecutor | 71 |
  | council, commission or board | 57 |
  | school board (South Dakota's Commissioner of School and Public Lands) | 2 |

- **No p moves.** None becomes computed or uncomputed [measured: p before and after in every row].
  - 40 of the 359 have a p, and keep it: unopposed races (p 0), and races between a Democrat and a Republican, whose partisan route does not read the type.
  - The other 319 have none before or after. 69 of them (40 local, 29 primaries) are nonpartisan or one-party races whose reasons now name the class "state statewide officer, …" (or "primary, state statewide officer, …"), too few for a p. The rest keep their reason (no county lean for the year, seats not in the source, a gated state).
- **50 records of other types** (36 prosecutors, 8 boards and 6 of §23's statewide officers) keep their type. Their reasons give a changed count of like races, since the offices that left or joined their classes count there no more or now.
- **The back-tests.** `backtest-local-partisan.json` (2024) and `calibration-local.json` show the officers' and prosecutors' rows shrinking and the statewide officers' growing. No verdict is read from these rows.

**Left as they were, counted for a ruling** (state offices with no district and not one county's):
- **Statewide boards and commissions of several seats:**
  - 13 commissioners of a commission named as such: Arizona's and Oklahoma's corporation commissioners (5), Texas's railroad commissioners (2), public service commissioners (2, and Alabama's president of the Public Service Commission, 1), and South Dakota's public utilities commissioners (3). The ruling's "public service where one seat is elected statewide" is not read for these: the size of each commission is not in the sources taken in. Each keeps "council, commission or board" [inferred: a member of a commission by its own name].
  - 10 seats on Michigan's State Board of Education and its three universities' boards, 2 seats at once.
  - 8 seats of Hawaii's Office of Hawaiian Affairs trustees.
  - New Mexico's 3 Public Education Commissioners.
  - The District of Columbia's council chairman, council member at large and State Board of Education member at large (1 each).
- **Judges:** 3,174 judge records in state offices. 145 of them name a supreme court or a court of appeals and carry no district or single county, the statewide courts by their names [inferred].
- **Others, for a reading:**
  - Montana's Clerk of the Supreme Court (2): a single statewide seat, but a court's clerk.
  - The District of Columbia's Attorney General (1) and Mayor (1): their contest is one county's, since the District is one.
  - Illinois's 2018 one-candidate "Comptroller" and "Treasurer" contests of 17 and 2 votes. Each is one name beside the statewide race, a stray write-in line filed as its own contest [inferred].

**Lieutenant governors on a joint ticket.** None is filed as its own contest [measured]. Each of the 29 general-election lieutenant governor records was set beside the same state's governor contest in `data/governor/`, party by party. 27 have a governor's contest to compare. No Democratic or Republican count equals the governor's: where both have the party's candidate, the ratios run from 0.74 to 1.35, apart from Idaho's 2022. A joint ticket's votes would be the governor's own.
- Idaho's 2022 record reads 2.96 and 2.09 times the governor's. MEDSL's 2022 Idaho file is about double: its US House count is 1,163,392 against the certified 583,628 in `checks-2022.json`. The file's own quality gate already holds those records. California's 2022 and Louisiana's 2023 had no governor's contest to compare.

## 25. Commission seats, statewide judges, Montana's clerk, New Mexico's PEC and Illinois's stray lines (the rulings of 16:19)

*Added 2026-11-07 at 16:44 UTC.* The rulings, verbatim:
1. "A statewide contest for a commission seat that elects one seat, by the source's own vote-for or seat count, is a 'statewide officer'. Where it elects more than one, it keeps the board type. Where the source does not show the count, hold it as a board and do not infer the count."
2. "A supreme court or appellate seat elected statewide in a one-seat contest is typed 'statewide judge'. Retentions stay retentions, and the other judges keep their type."
3. "MT's Clerk of the Supreme Court is a statewide officer."
4. "MI's boards, HI's OHA trustees and DC's at-large seats keep their types under rule 1. NM's PEC members are elected by district, so find the district or hold them. DC's AG and Mayor stay local."
5. "IL 2018's two stray lines: identify them from the State Board's results and fix or hold them, with the reason."

Reasons: "a race's class is set by what the contest elects"; "a statewide judicial race is not like a county bench, and the class decides the pool". Every record that changed: `data/local/moves-courts-commissions.json`, against main after #87.

**How "elected statewide" is read.** A seat's district column does not say whether the seat is elected statewide. It holds a seat's place or position as often as a district: Alabama's and Texas's "PLACE 1" and "002", Arkansas's "POSITION 2", Nevada's "SEAT C", Minnesota's "STATEWIDE, COURT 5" [measured: MEDSL's files]. So the contest's own votes are read instead (`pipeline/local_medsl.py`, `mark_whole_state`). A contest is elected statewide if it has a vote in every county where the state's contests on its date have votes, in the files taken in [measured]. County codes that are not five digits are left out. For the State Board's North Carolina contests, the contest must be in all 100 counties, the test that script already uses. "One seat" is the source's own count: MEDSL's magnitude, the State Board's vote-for. A contest with no count keeps its type.

The courts' seats split cleanly [measured, MEDSL's state files 2016-2024]:
- 117 contests are in every county.
- 155 have votes in under half the state's counties. They are district seats: Ohio's, Texas's, Kentucky's, Washington's and Mississippi's courts of appeals by district, Kentucky's and Mississippi's supreme courts by district, New York's supreme court (a trial court).
- 5 fall between, the near misses below.

**What moves:**
- **142 records are typed `statewide judge`** (135 local, 7 North Carolina primaries); all were `judge`. Of them:
  - 47 kept p 0 (unopposed);
  - 4 kept their p (North Carolina's 2024 Democrat-against-Republican races, whose partisan route does not read the type).
  - **7 lost their p:** Arkansas's 2024 Chief Justice; Michigan's 2024 Supreme Court; Minnesota's 2024 Chief Justice and Associate Justice 6; Montana's 2024 Chief Justice and Justice 3; Washington's 2024 Position 2. Their new class, "state statewide judge, nonpartisan, 2 candidates", has 8 like races in earlier years, under the method's floor of 100.
  - The other 84 had no p before and have none now.
  - By state and year, the records are Alabama's (22), North Carolina's (47), Minnesota's (15), Texas's (10), New Mexico's (10), Nevada's (11), Ohio's (7), Washington's (6), Montana's (4), Arkansas's (3), Michigan's (3), West Virginia's (2) and North Dakota's (2). `typed_by_office` in the moves file lists every office name.
- **12 other judges lost their p** with no change of type:
  - Arkansas: 4;
  - Florida: 2;
  - Indiana: 1;
  - Mississippi: 1 (a supreme court seat by district);
  - Oregon: 4 circuit judges.

  All are 2024 county or district benches in the class "state judge, nonpartisan, 2 candidates". With the statewide seats gone from that class, it has 94 like races in earlier years, under the floor of 100. This follows from the ruling's pool; it is not a choice made here.
- **16 records are typed `statewide officer`:**
  - 14 commission seats, all one seat in every county: Alabama's Public Service Commission (Places 1 and 2 of 2018, its President of 2024); Georgia's Public Service Commission (Metro-Atlanta and Western of 2018, members elected statewide from residency districts [inferred: the contests are in all 159 counties]); North Dakota's Public Service Commissioner (2018, 2024); Oklahoma's Corporation Commissioner (2018, 2022); South Dakota's Public Utilities Commissioner (2018, 2022, 2024); Texas's Railroad Commissioner (2018, 2024).
  - Montana's Clerk of the Supreme Court (2018, 2024), which `STATE_EXEC` now names.

  Their types before were `council, commission or board` (14) and `clerk, treasurer or other county officer` (2). None moved a p: Alabama's 2024 president keeps p 0 and Montana's 2024 clerk keeps its partisan p (2.97e-6). The rest are Democrat-against-Republican races with no county lean for the year, before and after.
- **Kept their type by rule 1:**
  - Arizona's corporation commissioners: 2 and 3 seats at once, and a 2024 contest split in two by MEDSL's file, 12 and 3 counties.
  - Montana's and Nebraska's public service commissioners, by district (19, 6, 8 and 4 counties).
  - Michigan's boards (2 seats at once), Hawaii's OHA trustees and the District of Columbia's at-large seats, as ruled.
- **New Mexico's Public Education Commissioners, 2022.** MEDSL's 2022 file gives the contests no district [measured: the district column is empty]. Its five candidates, each the only name in precincts of its own, had been read as five contests of no district. The Secretary of State's official results give each one's district:
  - the page is "2022 General Election Official Results", Public Education Commission, read by the new `pipeline/intake/nm_sos.py` at 16:32 UTC [stated];
  - Timothy E Beck, district 2; Alan Lee Brauer Jr, 3; Sharon Clahchischilliage, 5; Stewart Alan Ingham, 6; Patricia E Gipson, 7;
  - each was the only name, every precinct reported, and each total equals its candidate's votes.

  What changes in the records:
  - each takes its district, so its id changes (`…PUBLIC_EDUCATION_COMMISSIONER-2` and so on);
  - each takes the official votes (`result.votes_source` `nm_sos`; the ruling of 15:16, "the certified count wins") and keeps MEDSL's in `result.medsl_votes`. Gipson's official count is 35,567 against MEDSL's 35,565; the other four are equal;
  - each keeps p 0 (unopposed) and its type, `school board`.

  The 2024 file already gives the districts. The 2016 contests are read for their questions only.
- **Illinois's two stray lines of 2018.** Each is one name, Mary Arline Vann-Metcalf, with 17 votes for Comptroller and 2 for Treasurer, plus 1 for State Senate 17, which is not a local record [measured]:
  - all in one Cook County precinct, "COUNTY FLOATING";
  - no party, not marked a write-in, district STATEWIDE.

  The State Board of Elections' results page (elections.il.gov, ElectionVoteTotals.aspx) answered its own form for the 2018 general election with its error page, "An error has occurred.", at 16:20 and at 16:21 UTC, the second time with the page's own session cookie [measured]. So the lines are not identified. They are held: p not computed (before, p 0), and no winner is marked. The reason is in each record.

**The back-tests.** `backtest-local-classes.json` (2024) has 19 fewer contests, the 19 judges above, and its "class, state judge" row is gone. `backtest-local-partisan.json` and `calibration-local.json` show the judges' rows split. No verdict is read from these rows.

**For a ruling, not acted on here:** *(ruled at 16:47; each item below is resolved in §26: the near misses joined or held, the boards typed `statewide officer`, Michigan held as "seat count unread", North Dakota's 8 replaced by the state's 22 judgeships, and the officer test's misses joined or held)*
- **Near misses of "statewide":**
  - Oregon's 2024 Supreme Court positions 1 and 7 have votes in 28 and 26 of the state's 36 counties in MEDSL's file.
  - Washington's 2022 positions 1, 5 and 6 are in 38 of 39: King County's lines are filed as other contests ("STATE SUPREME COURT JUSTICE POSITION NO. 6", 558,007 votes, beside 1,360,073 for the rest of the state), and MEDSL gives each position 3 seats.
  - All five stay `judge`.
  - The same split touches Washington's 2022 statewide officers (Secretary of State, 38 of 39 counties).
- **One-seat statewide boards that are not commissions:** Colorado's at-large State Board of Education seat (64 of 64 counties) and Hawaii's resident trustees (one seat, statewide) keep their board types under rule 4.
- **Michigan's 2018 Supreme Court** is one contest of six names with MEDSL's magnitude 1, so one winner is marked. Whether it elected two seats should be checked against Michigan's results. They have not been read here.
- **North Dakota's "Justice of the Supreme Court"** with district names ("East Central Judicial District" and seven more; 8 contests) covers only those districts' counties. These are probably district court seats filed under the Supreme Court's name [inferred]. They keep `judge`.
- **The officer test of §24** ("no district and not one county") is unchanged. Read by counties, 14 of its MEDSL officers would miss a county of MEDSL's file: Washington 2022 (King), Arizona 2022 (two counties), Idaho 2022 (five offices) and others. These are gaps in those files, not districts [inferred].

## 26. Statewide contests filed in pieces, North Dakota's judgeships, Michigan's Supreme Court, one-seat boards, and M2's two readings (the ruling of 16:47)

*Added 2026-11-07 at 17:41 UTC.* The ruling, verbatim: "Your items 1 and 5 come before the legislatures. They are not class questions: a record missing counties shows the wrong count, and it can show the wrong winner. WA 2022's Secretary of State reads Anderson 1,066,770 to Hobbs 903,655 without King County, and Hobbs won. Ruled, for statewide officers and statewide judges: (a) Where a contest's lines miss counties that voted that day, find its other pieces: the same office and candidates, in counties the first piece lacks. Join them into one record where together they cover every county. (b) Check each joined total against the state's certified total where one is read. The certified count wins (15:16). (c) If it still misses counties: use the state's marked total, if one is read, as the record's count. Otherwise hold it: no p, marked incomplete, and no winner drawn from a partial count. (d) Fix MEDSL's 3 seats per position in WA 2022 from the state's results." The same PR: "One-seat statewide board seats (CO's at-large seat, HI's resident trustees) become statewide officer, by the 16:19 reason. Check every MI Supreme Court contest's seat count against the state's results. If 2018 elected two, set 2 seats and mark both winners. ND's 8: retype them from the state's results if they are district court seats. List every move. Reason: a shown figure has to be the whole contest's count of record." On Michigan, 16:53 and 16:55 (quoted in `pipeline/local_medsl.py`, `MI_SC_UNREAD`). Every record that changed: `data/local/moves-pieces.json`, against main after #89.

**How it is read** (`pipeline/local_medsl.py`, `statewide_pieces`). A state office's contest is statewide by name (a statewide executive office, no district) or as a court's, commission's or board's seat whose district is none, STATEWIDE or a seat's label, with votes in at least half the state's counties that day. It misses counties where its votes are not in every county the state's contests have votes in on its date (as `mark_whole_state` reads it). Its pieces are contests of the same state, date and stage in counties it lacks, whose candidates are within its own (or, under the same office's name, take its own in). What the rules find is written out in the script (`JOINS_EXPECTED`, `QJOINS_EXPECTED`, `HOLDS_EXPECTED`, `OVER_EXPECTED`), so a change in MEDSL's files stops the build rather than joining or holding something unseen.

**(a) Joined, 8 records** (every county covered once joined):
- **Washington 2022.** King County's lines are filed under the state's other name [measured]; the Secretary of State's own page says why: "you can download precinct results from our results exports for every county except for King County" [stated]. Joined: the Secretary of State ("Washington State - Secretary Of State", 38 counties, with "State Of Washington Secretary Of State", King), the Supreme Court's positions 1, 5 and 6, and the two advisory votes, 39 and 40. The two advisory votes are questions, not in the ruling's words; they are joined by its reason, and because the joins moved the state's largest precinct count, which had made them read as local questions.
  - **The Secretary of State now reads Hobbs 1,466,862 to Anderson 1,349,125** (MEDSL's joined counts), and Hobbs is marked the winner. Its p stays not computed, for the reason it had before: MEDSL's 2022 legislative returns for Washington differ from Klarner's in 20% of the districts compared.
- **Arizona 2024, Corporation Commission** (12 counties, with Maricopa, Pima and Santa Cruz filed apart). Its pieces give it 3 seats and 1 [measured], and the state's results were not read, so it is held: "seat count unread", no winner, seats left empty. It keeps the board type (16:19, rule 1: "Where the source does not show the count, hold it as a board").
- **Oregon 2024, Supreme Court position 7** (26 counties, with Curry's line for Bronson James filed apart). Joined, it is still in 27 of 36 counties, so it is held under (c).

**(b) The state's results** (`pipeline/intake/wa_sos.py`): the Secretary of State's results page links its exports (`20221108_StateExecutive.csv`, `_Judicial.csv`, `_Measures.csv`), read at 16:54 and 17:22 UTC. The page says "The Secretary of State certifies final results"; its link "Certified Election Results (PDF)" answered HTTP 404 at 16:51 UTC, and the exports carry no certified or official mark. So MEDSL's joined counts stand and the difference is recorded in `result.state_total` (15:16; the orchestrator, 16:53, "the joined counts standing at 4,811 under the state's, with the difference recorded, is right"):
- Secretary of State: the state's Hobbs 1,468,521, Anderson 1,351,926, write-ins 129,933; MEDSL's joined counts are 1,659, 2,801 and 351 lower, 4,811 in all.
- Supreme Court positions 1, 5 and 6, and advisory votes 39 and 40: equal to the vote.

**(d) Washington's positions take one seat each** from the state's export, which lists each as a race of its own ("SUPREME COURT - Justice Position #01") with one name and the write-ins [stated]; MEDSL's file gives each 3. Typed `statewide judge` now (one seat, every county), each with p 0 (one name for its one seat). Before, with 3 seats, p was not computed: "one name on the ballot for each seat, but write-ins received votes".

**(c) Held, still missing counties** (no p, `result.votes_incomplete` with the counties missing, no winner): 2018 New York's Comptroller (59 of 62 counties) and Attorney General (61); 2022 Arizona's Treasurer and Mine Inspector (13 of 15), Idaho's Lieutenant Governor, Secretary of State, Controller and Treasurer (43 of 44) and Superintendent of Public Instruction (41), Michigan's Secretary of State (82 of 83), New York's Comptroller (61), Oregon's Commissioner of the Bureau of Labor and Industries (34 of 36); 2024 Oregon's Supreme Court positions 1 (28 of 36) and 7 (27, joined). No state total was read for these; each is listed for a later read below.
- **North Dakota 2024, State Auditor** takes the state's marked total under (c): the Secretary of State's results site heads its page "Official 2024 General Election Results" (`<h1><span>Official</span> 2024 General Election Results</h1>`) [stated], every precinct reported (385 of 385): Gallion 241,270, Lamb 108,962, write-ins 761. MEDSL's lines miss Eddy County (38027) and read 240,424, 108,635 and 761 (`result.medsl_votes`).
- **Georgia 2022, Secretary of State:** a line with one name (Brenda Lynn Nelson-Porter, 154 votes) and no county code, beside the whole contest; held.
- Arizona's 2022 Attorney General in Cochise County is MEDSL's "GEN RECOUNT" line and stays recorded as the recount it is.

**North Dakota's 8, 2022.** MEDSL's file names North Dakota's district court judgeships "JUSTICE OF THE SUPREME COURT" with the judicial district in the district column, and adds each district's judgeships up into one contest of one seat [measured]. The Secretary of State's official results (`pipeline/intake/nd_sos.py`; the archive links "General Election - November 8, 2022" to the results site, whose pages are headed "Official 2022 General Election Results") list 22 judgeships, each "Vote For 1" with its own names, and the statewide "Justice of the Supreme Court" (Crothers, unchanged) [stated]. The 8 records are replaced by the 22, each as the state lists it ("Judge of the District Court No. 4 East Central"; office "Judge Of The District Court", district "EAST CENTRAL JUDICIAL DISTRICT, JUDGESHIP NO. 4", as MEDSL's 2024 file names them), with the state's official votes and winners (`result.votes_source` `nd_sos`; every name's count equals MEDSL's, and the write-ins add up to MEDSL's by district). MEDSL's pooled contests had read as close races (Hager 15,741 to Knudson 15,496, share 0.504), where each was unopposed for a seat of its own. Now 20 have p 0 (unopposed) and 2 are contested (Southeast No. 2, Thornton against Murphy; East Central No. 4, Cleveland against Chapman), whose class, "state judge, nonpartisan, 2 candidates", has 87 like races in earlier years, under the floor: not computed.

**Michigan's Supreme Court.** The Secretary of State's results refused and the Michigan Manual answered 403 (recorded, not tried again). The Court's own pages (courts.michigan.gov, which answers a script shell) were rendered in headless Chromium at 16:56 UTC under the ruling of 08:00, and say: Chief Justice Cavanagh, "Before joining the Michigan Supreme Court in January of 2019" and "Prior to her election to the Court"; Justice Thomas "was elected to a full term on the Michigan Supreme Court in November 2024 and took office on January 1, 2025"; Justice Bolden's page gives her appointment only [stated]. None says how many seats a contest filled, so the 2018 contest and both of 2024's are held: "seat count unread", no p, no winner, out of every pool. MEDSL's own 2018 counts add that the contest's 6,262,391 votes are 1.47 times the 4,250,585 for Governor on the same ballot [measured], so it elected more than one seat; how many is not read.

**Also held, by the same reason: one-seat contests with more votes than ballots** (`over_ballot`). A one-seat contest has at most one vote a ballot. Where the state elects a governor that day, a statewide contest of one seat by MEDSL's count with more than 1.05 times the Governor's votes on the same ballot is held, "seat count unread" [measured]: Ohio's 2018 Supreme Court (4 names, 7,086,019 votes against 4,435,462 for Governor, 1.60 times; two seats in one line [inferred]), Hawaii's 2022 at-large OHA trustee (6 names, 747,716 against 413,262, 1.81), and Michigan's 2022 Attorney General (6,153,017 against 4,432,311, 1.39; one seat, so its lines are counted more than once [inferred]). Not read for years with no governor.

**One-seat statewide board seats** (16:47; `STATE_BOARD_TYPES`). A board's or school board's seat in a state office's contest of one seat, by the source's count, with votes in every county, is typed `statewide officer`: Colorado's at-large regent of the University of Colorado (2018, 2024) and at-large member of the State Board of Education (2022, district "000"); Hawaii's OHA resident trustees (Maui and Oahu 2018, Hawaii 2022, Molokai and Kauai 2024) and at-large trustee of 2024 (2 names, one seat). Hawaii's at-large trustee of 2018 (3 seats) keeps the board type, and that of 2022 is held above. A statewide executive office is now read so also where its district column holds a code but its votes are in every county: Colorado's 2022 Secretary of State, Treasurer and Attorney General and Illinois's 2022 Secretary of State, Comptroller, Treasurer and Attorney General carry district "000" [measured], and had been typed `other local office`, `clerk, treasurer or other county officer` and `prosecutor`. These 17 move type only; no p moved (Colorado's 2024 regent keeps 5.88684e-07; the others are Democrat-against-Republican races read by the partisan route, or under the floor).

**What moves, in all** (`data/local/moves-pieces.json`, 123 records against 679f0d5, whose `data/local/` files are main's after #89) [measured]:
- 22 new records (North Dakota's judgeships) and 14 gone: MEDSL's 8 pooled North Dakota lines, and 6 pieces joined into others (Washington's 4, Arizona's 1, Oregon's 1).
- 20 typed anew: 17 `statewide officer`, 3 `statewide judge`.
- 3 new p (Washington's positions, p 0). 2 lost: Oregon's 2024 positions 1 and 7 (p 0 before, now held). No other held contest had a p, and no p value moved.
- 49 not computed before or after, their reason changed: the holds, and like races moved by the records that left or joined a class. 2024's "state judge, nonpartisan, 2 candidates" has 93 like races in earlier years (94 before); "state judge, nonpartisan, 4+ candidates" 5 (8); "state statewide officer, nonpartisan, 2 candidates" 4 (2).
- 7 notes changed.
- The 2024 partisan back-test moves Colorado's at-large regent from "school board" (74 races to 73) to "statewide officer" (25 to 26); the calibration's 2024 test reads deviance 17.58 by office type and 16.86 after (17.55 and 16.83 before this step), and still improves.
- In `data/measure/`: 2 gone (King County's advisory-vote pieces), 2 notes changed (the joined advisory votes), and the 17 statewide questions filed as local gain their page's URL in `listed_statewide.state_total` (`url`).

**M2's fourth pass, readings (a) and (b)** (relayed at 16:53):
- (a) "statewide-filed-local.json names six quote pages by cache file only. Give each one its URL." Every `quote_file` in `data/measure/statewide-filed-local.json` now has a `quote_url` beside it (163): the list's own URL for a text made from the list page, and for the nine other pages the URL the readers' fetch logs record (Alabama's Montgomery sample ballot, Louisiana's "Types of Elections" page, Montana's State Canvass Report, Minnesota's Revisor chapter 67 of 2023, Rhode Island's P.L. 2016 ch. 5 and Resolution 329, Washington's 2018 Advisory Vote 19 and 2024 Measures-All pages, and its 2024 news release on the measures certified).
- (b) "Mo. III §52(b), Okla. V §3 and Okla. V §33(C) say 'referred', but their proposer is listed as the legislature. A rule carries only the proposer its text names. Quote the words that name who refers, or carry both proposers ... and mark the rule accordingly." Each now has `proposer_quote`, checked word for word on its page fetched again at 17:07 UTC: Missouri's §52(a), "either by petitions signed by five percent of the legal voters ..., or by the general assembly, as other bills are enacted" (both carried, as before); Oklahoma's §3 with §2 on the same page, "by the initiative or referendum" and "either by petition signed by five per centum of the legal voters or by the Legislature as other bills are enacted" (the statute rule carries all three, the amendment rule the initiative only); §33(C), "Any revenue bill originating in the House of Representatives shall not become effective until it has been referred to the people", the Legislature's own bill, which the section itself sends to the people. **No citation changes**: every rule carries the proposers it carried before, now with the words that name them (the rebuild moved no `threshold`).

**For the orchestrator, not acted on here:**
- The state totals not read for the held contests: New York's State Board, Arizona's Secretary of State (azsos.gov refused earlier, 403), Idaho's, Michigan's (refused), Oregon's. Each could replace a hold under (c) if a marked page is read.
- Arizona's 2022 Attorney General reads Mayes 1,254,643 to Hamadeh 1,254,235 in MEDSL's general lines, with Cochise County's recount filed apart; the state's certified count was not read.
- The over-ballot test reads only years with a governor; 2020's and 2024's one-seat statewide contests are not tested that way.
- The District of Columbia's officers are typed by the officer test only where they are not one county's; the District is one county, so its Attorney General stays local (16:19, rule 4: "DC's AG and Mayor stay local").

## 27. New Jersey's legislatures of 2023 and 2025, from the Official Lists

*Added 2026-11-07 at 18:12 UTC, at the orchestrator's order of 10:35: "After (a), queue the odd-year legislatures after Klarner's 2022 (MS, NJ, VA 2023; NJ, VA 2025) from each state's certified files, each with a gate you propose. Reason: law 5 and Zach's 03:13 word, as much data as can be found."* With it, the ruling of 11:56: "earlier cycles only means every earlier contest". Every record that changed: `data/local/moves-nj-legislature.json`.

**Why.** New Jersey elects its legislature in odd years. Klarner's returns end with 2022 and MEDSL holds no odd year, so the state's own lists are the only source read.

**Source** [stated: the files; measured: what `pipeline/intake/nj_sos.py` reads]. The Division of Elections' page of each year links each office's "Official List" as a PDF: "Official General Election Results: State Senate" and "... General Assembly" for 2023, read at 15:43 UTC (dated 12/06/2023 on their pages); "... General Assembly", "... State Senate - 35th Legislative District" and "... Governor" for 2025, read at 16:08 UTC (dated 12/03/2025). They hold:
- 2023: the Senate's 40 districts (86 candidates) and the Assembly's 40 (160);
- 2025: the Assembly's 40 (159), the Senate in the Thirty-Fifth district only (2) and the Governor (4).

Each district's heading names its counties ("First Legislative District: ATLANTIC (part) - CAPE MAY - CUMBERLAND (part) Counties"). Each candidate has a line per county and a "Total"; the heading says "* denotes incumbent"; "(w)" follows the names of those elected [inferred: in every contest of both years it marks exactly the leading candidates for the seats].

**The reader** (`nj_sos.py`, fixed here). The Assembly lists break long names over two lines ("VERLINA REYNOLDS-" / "JACKSON (w) *"), put the marks on the line under the name, and let an address run into the name's column with one space ("GERARD SCHARFENBERGER 20 SEA GULL LANE"). The 2023 Senate list prints a Hudson County line for Pablo Olivera (29th district) with no count; his Total, 181, is Essex's, and the record says so.

The reader now takes each of these as the list prints it, numbers the districts past the Twentieth ("Thirty-First"), and reads the counties each heading names. Re-read with it, 2024's federal lists are unchanged, except that Bonnie Watson Coleman (NJ-12) now carries her "(w) *" marks; no count changed.

**Seats.** Each Senate district elects one member, each Assembly district two at once [measured: Klarner's New Jersey Assembly contests of 2017, 2019 and 2021 have 2 seats each and his Senate's 1; the lists mark 2 winners in each Assembly district and 1 in each Senate district].

**The 35th's Senate seat of 2025** is taken as an election to fill a vacancy [inferred: 2025's Senate list holds that district only, while 2023's holds all 40; no law read]. Benjie E. Wimberly, elected to the Assembly from the 35th in 2023, is on it marked "*". It is recorded as a special, p not computed.

**The gate within the certifying source** (proposed; `pipeline/local_nj_leg.py`; `data/local/check-nj-legislature.json`). 2023's ballot holds no federal or statewide contest; 2025's only statewide contest is the Governor's, which D2 read from the same list.
- (a) Each list is linked as "Official General Election Results: ...", every page is headed "Official List", and its last page counts as many candidates as are read.
- (b) Each candidate's county lines add up to its Total, and each contest's Total equals its candidates' totals added up.
- (c) Each candidate's county lines are in the counties its district's heading names.
- (d) 2025 only: the Governor's list read here equals D2's `data/governor/2025.json` for each of its 4 candidates, and is the same file (sha256 ef28c114c11de275).

A contest that fails (b) or (c) is held; a list that fails (a), or a year that fails (d), holds all its contests. **Every list and contest passes** [measured]. Recorded beside the gate, not part of it: each district's named counties are the same in 2023's Senate and Assembly lists and in 2025's Assembly list. Each record carries its `gate` in the shape of Louisiana's 2023 (`data/README.md`).

**Routes** (pipeline/local.py's, as for MEDSL's 2024 legislatures):
- **The Senate of 2023.**
  - 38 races of one Democrat against one Republican take route (a) in class C: no last result on the same lines is read, since the lists hold no precincts to compare lines by. MEDSL's 2024 legislatures take class C wherever the lines are not shown to be the same.
  - Incumbency is the list's own mark [stated]: 17 Democratic incumbents, 12 Republican, 9 open seats.
  - The chamber's lean is Klarner's New Jersey Senate of 2021, +0.0389.
  - The fit is on Klarner's races of earlier years. p runs from 1.64e-5 (16th district) to 1.08e-4 (29th); the median of the 38 is 2.61e-5.
  - Class C is the chamber's average district (`p.forecast_scope`, REPORT §6). So a seat won 85% to 15% (the 29th) gets the p of an average Senate district, not of its own.
  - The 33rd (Stack against a Socialist Workers candidate) takes route (b), "general, one major party against minor parties or independents" (6,176 like races): p 6.05e-6.
  - The 28th (Burgess alone) is unopposed: p 0.
- **The Assembly** takes route (c), "general, 2 seats at once", by slate, at the boundary between the second and third.
  - 2023: 39 computed, median p 7.29e-5, highest 4.03e-4 (the 29th, its second and third 7,409 to 1,419); the 35th is unopposed, p 0.
  - 2025: 38 computed, median 4.04e-5, highest 1.21e-4 (the 29th); the 15th and 28th are unopposed, p 0.
- **Like races are every earlier contest in the sources taken in.** For 2023: Klarner's of 1967-2022 (4,680 in the full-slate class). For 2025: those, Louisiana's 2023 deciding rounds, New Jersey's 2023 and MEDSL's 2024 legislatures (4,789).

**2023 feeds the later years** (11:56):
- **The fit.** New Jersey's 38 Democrat-against-Republican Senate races join route (a)'s fit for 2024. That moves 2024's partisan legislative p and the transferred local route's p: 702 Senate p and 2,870 lower-house p (partisan and like-race routes together), and 976 local p.
- **Like races.** New Jersey's 2023 contests join the like races of 2024's legislative class and boundary routes.
- **How far.** The ratios after/before run from ×0.9943 to ×1.0699 in the lower houses, median ×0.9999 (92 beyond 1%); ×0.9943 to ×1.0425 in the senates, median ×0.9998 (8 beyond 1%); ×0.9986 to ×1.0022 locally, median ×0.9994. The largest are partisan seats far from even, whose p sits in the forecast's tail (New York's 55th, ×1.0699).
- **No p became computed or was lost.**
- **The tests' verdicts are unchanged.** The 2024 back-test of the transferred local route holds 51.9% in its 50% interval, as before (the rule is 40% to 60%), and 81.1% in its 80% (81.0%). The calibration's 2024 test reads expected_after 54.6 (54.7), deviance by office type 17.57 (17.58) and after 16.85 (16.86). It still improves, and neither route is adopted, as before.
- **The notes** of the fit and of the like races now name every source they take in. Before, the 2024 like races' note said "like races from Klarner's 1967-2022 returns" while Louisiana's 2023 deciding rounds were already among them, a wording slip fixed here.

**For the orchestrator:**
- The gate is proposed, not yet ruled. Every record says so (`gate.ruled`).
- Class C for the 2023 Senate. The 2021 map's lines and 2023's are not compared, since no source with precincts or a statement of the lines was read. If a page stating whether the 2023 districts are 2021's is read, class A could replace C for those that are.
- The 35th's Senate seat of 2025 is a special [inferred].

## 28. Virginia's legislatures of 2023 and 2025, from the Department of Elections, as read before it refused us

*Added 2026-11-07 at 18:50 UTC, at the orchestrator's order of 10:35 (§27); with the ruling of 11:56, "earlier cycles only means every earlier contest", and the orchestrator's words of 18:30 and 18:32 on the refusal and the gate.* Every record that changed: `data/local/moves-va-legislature.json`.

**Why.** Virginia elects its legislature in odd years. Klarner's Virginia ends with the House of Delegates of 2021, and MEDSL holds no odd year, so the Department's own results are the only source.

**The refusal, told whole.**
- The Department's "Election Results" page links a directory of CSV files on apps.elections.virginia.gov. Its listing of 2005-2023 results answered at 18:21 UTC. That listing ends in April 2023, so it holds neither general.
- At 18:27:48 the same host answered HTTP 403 "Access Denied" to its "Winners List" directory. I took that for a bar on directory listings, and at 18:28:44 I asked the same host for one results file ("2023 January Senate Special.csv"). It refused too. That second request should not have been made: the rule is to stop at the first refusal. I reported both at once.
- The orchestrator (18:30): the refusal binds the whole Department, so none of its hosts is read again, rendered or not. What was read before 18:27:48 stands, and anything fetched after it is deleted. The two refusal pages are deleted; nothing else came after it.

**Source** [stated: the files; measured: what `pipeline/intake/va_elect.py` reads]. Everything below was read before the refusal. It sits in the cache with each file's url, finishing time and sha256, and the script requests nothing.
- The Department's results page (18:20:42). It links the 2025 general to its results site, enr.elections.virginia.gov. It sends results "starting with the June 2023 Primaries" to the site's directory, which, rendered at 18:22:18, lists "2023 November General and Special Elections".
- Each general's page on that site, rendered in headless Chromium, which the 08:00 ruling allows for a script shell.
  - 2023 was scrolled to its end until its contests stopped growing (183, 18:26:19).
  - 2025 was rendered once, not scrolled (18:23:53), so it shows its first 50 contests: the three statewide, then House districts 1 to 47.
  - Each page is headed "<election> <date> OFFICIAL RESULTS Last Updated ..." (2023: "Last Updated Thursday, January 2, 2025"; 2025: "Monday, December 1, 2025"). Each contest shows its candidates, with "Winner" beside the winner, their parties and votes, and "Localities reporting n/n".
- The file each page's "Media Export" link gives (18:23:02 and 18:24:08). It holds every contest's statewide count and each locality's line, option by option, with its precincts. Virginia's localities are its counties and independent cities.
- 2023: the Senate's 40 districts and the House's 100, each "Vote for only one". 2025: the House's 100, and the Governor, Lieutenant Governor and Attorney General.

**The gate within the certifying source** (proposed, from the orchestrator's list of 18:32; `pipeline/local_va_leg.py`; `data/local/check-va-legislature.json`).
- (a) The election's page is headed "OFFICIAL RESULTS". The Department's page links it, directly or through its directory. Its "Media Export" link is the file read. Where the page shows a contest, its candidates and votes are the file's.
- (b) Each contest's locality lines add up, option by option, write-ins included, to its statewide count, and name no option the statewide count lacks.
- (c) The localities are the district's own. There are as many locality lines as the page's "Localities reporting n/n", all reporting. For 2025's districts the page as read did not show, the localities are the same as the district's 2023 contest, whose count the 2023 page prints [measured: all 100 House districts have the same localities in both years].
- (d) 2025: the file's Governor equals D2's `data/governor/2025.json` to the vote, line by line (Spanberger 1,976,857, Earle-Sears 1,449,586, write-ins 6,897). D2's count is the same site's, of the same election, read at 12:46.

A contest that fails (a)'s last part, (b) or (c) is held; a year that fails the rest of (a), or (d), holds all its contests. The years pass, and every contest passes but one [measured]:
- **The 9th Senate district of 2023 is held.** Its locality lines count 76 votes for Trudy Berry, in Lunenburg County, whom its statewide count does not hold. It was Frank M. Ruff Jr. alone, with 3,354 write-ins.

Recorded beside the gate, not part of it: each locality line's precincts add up to it. They do in every locality but two, in 2023:
- In Culpeper County, every contest's precincts add up to fewer votes than the county's line. Three legislative contests are affected: the 28th Senate district (Reeves 10,176 against 10,195) and House districts 61 and 62.
- In Henrico County, the 16th Senate district's write-ins are 156 against 157.

The record is the locality lines, which add up to the statewide count the page shows, and each of those four records says so in a note. Why the precincts fall short is not read [the 2023 page was last updated in January 2025 and its file made then; nothing says what changed].

**Winners.** `won` is the page's "Winner" mark where the page showed the contest (`won_mark` `stated`): all 140 of 2023 and districts 1 to 47 of 2025. In districts 48 to 100 of 2025 it is the leading candidate for the one seat (`won_mark` `inferred`, 53 records), each with a note. Where the page showed it, the mark is always the leading candidate [measured]. The orchestrator (18:32): "a figure resting on a page we saw and one resting on a rule we applied must look different in the record."

**Routes** (pipeline/local.py's, as for MEDSL's 2024 legislatures).
- **One Democrat against one Republican: route (a).**
  - 2023 is class C. No result on 2023's lines before 2023 is in the sources: Klarner's Virginia races of 2019 and 2021 carry his district regimes of 2011 and 2019 [measured]. That makes 34 Senate races (p 8.43e-6 to 3.14e-5, median 2.47e-5) and 65 House races (2.67e-5 to 1.18e-4, median 5.04e-5).
  - 2025 takes the 2024 rule of lines: a district's 2023 contest is its last result on the same lines where at least 80% of its 2025 precincts were among its 2023 precincts. That holds in 98 of 100 districts; the 65th (68%) and 72nd (58%) stay class C. Of the 84 races, 58 are class A, 24 class B and 2 class C, with p from 3.95e-7 (51st) to 7.72e-5 (41st), median 2.55e-5.
  - **Incumbency** is matched by name, as for 2024, to the winners of the chamber's last general: Klarner's Senate of 2019 and House of Delegates of 2021 for 2023, and the House of 2023 read here for 2025. In 2023 that is 9 Democratic and 7 Republican incumbents in the Senate's 34 races, and 16 and 19 in the House's 65; in 2025, 33 and 39 in 84. No race matched both of its candidates. No special election since those generals is read (the Department refused us before any was), so a member elected in one counts as not sitting [a measured gap; `incumbency_of` says so].
  - **The lean** is the chamber's last general before: Senate 2019 −0.0491, House 2021 +0.0091, House 2023 +0.0069.
  - **The fit**, as 11:56 asks, takes every earlier race of route (a) in the sources: Klarner's for 2023. For 2025 it also takes New Jersey's and Virginia's of 2023 and MEDSL's 2024 legislatures, so 2024's own races now enter a later year's fit for the first time.
  - **The president's party in 2025** is from the National Archives' 2024 page (Trump, R). D1's `pipeline/intake/nara_electoral_college.py` was run for 1964-2024 at 18:30 UTC, since this cache had read only to 2020; no earlier year's figure changed.
- **One major party against minor parties or independents: route (b)**, like past races: the 21st Senate district and House districts 3, 13 and 43 of 2023 (6,176 like races), and the 38th of 2025 (6,515, 2024's among them).
- **One name on the ballot: p 0**, unless write-ins drew 10% of the winner's votes, in which case p is not computed:
  - 2023: Senate 3 at p 0 and 1 not computed (the 23rd); House 24 at p 0 and 8 not computed.
  - 2025: House 14 at p 0 and 1 not computed (the 25th).

**2023 feeds the later years** (11:56).
- **The fit.** Virginia's 99 Democrat-against-Republican races of 2023 join route (a)'s fit for 2024 and the transferred local route's.
- **Like races.** Its four route (b) contests join the like races of 2024 and 2025.
- **What moves, against main (67431a4):**
  - 2,736 lower-house p, ×0.9406 to ×1.0023, median ×0.9994, 83 beyond 1%;
  - 699 senate p, ×0.9629 to ×1.0018, median ×0.9994, 8 beyond 1%;
  - 976 local p, ×0.9987 to ×1.0012, median ×1.0008.
  - The largest are partisan seats far from even: New York's 55th, ×0.9406.
  - No p became computed or was lost outside Virginia.
- **The tests' verdicts are unchanged.**
  - The 2024 back-test of the transferred local route holds 51.9% in its 50% interval, as before (the rule is 40% to 60%), and 81.0% in its 80% (81.1%).
  - The calibration's 2024 test reads expected_after 54.7 (54.6) and deviance by office type 17.58 (17.57). It still improves, and neither route is adopted.
- **The notes** of the fit, the like races and the back-test now name Virginia's 2023 among their sources.
- **New Jersey's records:** `gate.ruled` now gives the orchestrator's ruling of 18:20 ("accepted as proposed").

**For the orchestrator:**
- The gate is proposed, not yet ruled. Every record says so (`gate.ruled`).
- **The 9th Senate district of 2023 is held** for 76 locality votes its statewide count lacks.
- **Incumbency** misses every member elected in a special since the last general read.
- The same 2023 file also holds Virginia's 2023 local contests (clerks, Commonwealth's attorneys, sheriffs, boards of supervisors, school boards, town councils), already in the cache from before the refusal. They are not taken in here. They could be, with nothing requested.

## 29. Doubled and missing counts: Idaho's county totals, New Hampshire's doubled legislature, Hawaii's governor, and the volume test of every MEDSL state-year

*Added 2026-11-07 at 20:25 UTC, at the orchestrator's orders of 18:54, 19:04, 19:13 and 19:49.* Every record that changed is listed in `data/local/moves-volume.json`. The whole test is in `data/local/check-volume.json`.

**Why.** The orchestrator, 18:54: "n enters p directly, so a doubled count halves a figure we show." A share test cannot see a doubled count, or a missing county, because the shares stay the same. So every MEDSL state-year we take in is now tested on its volume (parts 1 and 2), and every MEDSL file is scanned for its structure (part 3).

**Idaho 2022: what doubled it** [measured: `pipeline/intake/medsl_precinct.py`, `checks-2022.json`].
- MEDSL's 2022 Idaho file lists a precinct named "COUNTY TOTAL" in each county, beside that county's precincts. It equals their sum, so every county is counted twice.
- Power County (16077) is missing from most offices.
- The rule (19:04, "Apply the COUNTY TOTAL rule"): drop a county-total line, candidate by candidate, where the county's other precincts add up to it exactly; keep it where they do not, or where it stands alone (`drop_county_totals`). In Idaho it drops 1,137 lines of state and local contests and 107 of the federal checks, and keeps none. (Part 3 finds 2 unequal and 3 lone county-total rows in the file; they are in contests the normalizer does not read.)
- Idaho's US House then adds up to 581,696 against D2's certified 583,628. The 1,932 short is Power County's.
- **The six statewide offices** take the Secretary of State's official results (`pipeline/intake/id_sos.py`; `local_medsl.id_statewide`).
  - The state's results page links "Statewide Results" and "Canvass Files" under "General Election - November 8, 2022".
  - The results site is headed "OFFICIAL ELECTION RESULTS", all 44 counties fully reporting. A vendor host that a state page names, and that marks its count official, counts (12:40).
  - Every candidate's total there equals the canvass workbook's TOTAL row, to the vote, in all six offices. That is the gate.
  - The canvass's one write-in line (Secretary of State, Garth G Gaylord, 2,778) is not on the results page. MEDSL's count for it equals the canvass's, so it is kept, with a note.
  - `result.medsl_votes` keeps MEDSL's counts. They fall short of the state's by Power County, by up to 5,809 votes (Superintendent: Critchfield 398,740 against 404,549).
  - None of the six has a p: Idaho's 2020 House vote by county, the lean these read, is not in the sources.
- **Power County.** "Any other ID 2022 MEDSL record whose area includes Power County is held" (19:04). The six statewide offices are the only Idaho 2022 records MEDSL gives. Its local rows carry no dataverse and are not read. So the rule holds none, though it stands in `local_volume.COUNTY_HOLDS`.
- Idaho 2022 now passes part 1: the governor is −0.39% (Little 357,187 against 358,598), Power County again. Part 2's median ratio is now 1.00.

**Other files with county-total lines** (a grep of every raw file before part 3; part 3 below scans every file and finds the rest).
- Illinois 2024: 9 lines in state and local contests, and 1,062 in the federal checks. Each carries a candidate (chiefly a write-in) with no precinct line, or a county's own adjustment; none is a copy of its precincts. So the rule drops none and no record changes.
- New Jersey 2024: Gloucester's county-total line for president equals its precincts. The rule drops it, so 9 lines leave the federal check. The statewide president check stays over the line (MEDSL +9.1% after, +12.6% before). The county gate (`local_nj.py`) reads the raw file itself, so no record changes.
- New Jersey 2022: four lines in two legislative contests. The file gives no record, so it was not re-read.
- MEDSL's 2022 `STATE_precinct_general.csv` holds Idaho's county totals too, but the normalizer does not read that file.

**New Hampshire 2022** (`pipeline/local.py` nh_2022; the ruling of 19:04: "Use MEDSL's counts where every candidate matches by name, marked 'Klarner's figures are doubled; MEDSL's counts'. Hold the rest.").
- Klarner's New Hampshire 2022 legislature is doubled. Its Senate is doubled whole. Its House is doubled in part. MEDSL's counts add up to the day's governor vote. The Secretary of State refused at 19:02:32 UTC (403), so the state could not settle it.
- Each Klarner contest is matched to MEDSL's, one to one, by surname. In the House the district number and the county must match too; MEDSL's House names are often a surname alone ("PLOSZAJ") or a surname and initials ("SOUCY T"). Where a recount contest exists, it is preferred.
- Of Klarner's 227 contests, 205 take MEDSL's counts: 181 House and 24 Senate (`result.votes_source` "medsl").
- 22 House contests are held: 21 where the candidates do not all match, and Strafford 15, where one of MEDSL's counts is 63% above Klarner's rather than near 1× or ½×.
- **What moves:** 116 p, House 94 and Senate 22. They rise ×1.97 to ×2.38 (median ×2.00); one House race moves ×1.007. 22 House p are no longer computed. The other matched contests' counts were not doubled, or their p is 0.
- The 2024 fits take New Hampshire's 2022 rows from these counts and leave out the unmatched ones (19:04).

**Hawaii 2018's governor** (`pipeline/governor_hi2018.py`; `data/governor/2018.json`; the ruling of 19:13).
- D2's 137,719 for Tupola is the figure in its source, Cha, Kuriwaki and Snyder v4.1. The Office of Elections' certified summary has 131,719. Its page lists the summary under "Certified Text Files", read 19:07 UTC. The other three candidates are equal to the vote.
- The record now has 131,719, total 390,843 and n 376,653, with the summary as its source and a note. Each of its five p rises ×1.0159 (538 lite 6.463e-7 to 6.566e-7).
- **Not refit here.** D2's caches are not in this container, so two things still use 137,719:
  - the governor fits of 2020 onward, which take Hawaii 2018 as a training row;
  - Hawaii 2022's last-governor-race input, which reads 0.640094 and should be 0.650291 (first written here as 0.650298 in error; section 30).
  The orchestrator (19:49) orders a refit as its own PR, next.

**The volume test** (`pipeline/local_volume.py`).
- **Part 1** (18:54 (b)): the precinct sum of the year's top contest against our independent count, bounded at 0.5%.
  - The top contest is the governor where the state elected one (D2's `data/governor`, not a special). Otherwise it is the US House (D2's `data/house`, every line's votes together).
  - Governors are matched by surname, D2's two leading candidates against MEDSL's lines.
  - Fusion (19:04): the party lines are summed. Where D2's source reports each candidate's own line alone, that line is compared (Connecticut 2018: Lamont 676,649 and Stefanowski 624,750, equal to the vote).
- **Part 2** (18:54 (b)): MEDSL's legislative candidates against Klarner's, matched by district and name. A state-year is flagged where more than 5% of matched candidates sit at a ratio of 2 or ½ (±1%), or where the median ratio is off 1 by more than 3%.
- **Part 3** (19:49, item 5): the structural scan, below.
- **Settling** (19:04): from the state where it answers. An unsettled flag of 5% or more holds the state-year's MEDSL records. Under 5%, they are kept with a note that gives the difference and why it is unsettled.

**What each part could test** (the orchestrator, 19:49) [measured: `check-volume.json` `coverage`].
- 2016: MEDSL records in 28 states.
  - Part 1 tests 4 (Missouri, Montana, North Carolina and Washington, their governors). MEDSL's 2016 files hold no president or House contest, so 19:13's top contest for a year without a governor cannot be read.
  - Part 2 tests 23 (the four above among them).
  - Neither tests 5: Alabama, the District of Columbia, Louisiana, Mississippi and New Jersey. Part 3 scans their rows.
- 2018: all 50 state-years. Part 1 tests 35 by governor, 14 by House and DC by its mayor. Part 2 tests 40.
- 2022: all 48. Part 1 tests 35 by governor and 13 by House. Part 2 tests 42.
- 2020: none of 31. MEDSL's 2020 file holds local offices only, with no top contest and no legislature. Part 3 scans it.
- 2024: all 51, by its own gate: the president against D1's certified count (`local_medsl.quality`). Part 3 scans it too.

**The flags and what was done with each.**

| year | state | part | test | result | settled | done |
|---|---|---|---|---|---|---|
| 2016 | ME | 2 | legislature vs Klarner | median 0.934 (67 candidates) | no: no federal contest in MEDSL's 2016 files; the state refused (19:12:38, 403) | 53 records held (questions; none had p) |
| 2018 | NY | 1 | governor | −4.03% lines summed, −15.76% on own lines; votes in 57 of 62 counties | no: the State Board refused (18:49) | 2 records held (19:13, "NY 2018 held") |
| 2018 | NJ | 1 | House | −1.45% | yes: the Official List equals D2; MEDSL short in Middlesex (−18.04%) and Hunterdon (−0.78%), within 0.5% in every other county | records whose area includes either held (19:13, 19:49): none does; 528 kept with a note |
| 2018 | OR | 1 | governor | was +0.81% | yes: part 3's county-total rule ("TOTAL" rows); the governor then equals D2 to the vote | none held; its note removed |
| 2018 | IN | 1 | House | −0.70% | no: the state's 2018 results were not found | 232 records kept with a note |
| 2018 | HI | 1 | governor | was −4.36% | yes: D2's figure, fixed (above) | none held; it now passes |
| 2018 | CT | 1 | governor | +4.06% lines summed | yes: on own lines, equal | none |
| 2018 | DC | 1 | mayor | 0 | the Board's certified page (19:12) equals MEDSL | none |
| 2022 | NY | 1 | governor | +0.93% lines summed | no: the State Board refused | 2 records kept with a note |
| 2022 | MI | 1 | governor | −1.23% lines summed (−1.10% on own lines), after the county-total rule | no: the state refused earlier today | 4 records kept with a note |
| 2022 | AR | 1 | governor | −0.76% | already held by the share check | 6 noted |
| 2022 | IN | 1, 2 | House; median 0.78 | −57.4% | already held by the share check | 3 noted |
| 2022 | ID | 1, 2 | governor; median 1.73 | was doubled; now −0.39%, median 1.00 | yes: the county-total rule | the six statewide offices from the state |
| 2022 | NH | 2 | legislature | median 0.50 (74% at ½) | Klarner's doubled (19:04) | above |
| 2022 | NJ | 1 | House | 3× | the file gives no record | none |

**Part 3: a structural scan of every MEDSL file** (19:49, item 5: "Look for aggregate rows beside precinct rows ... and any row equal to the sum of the other rows for the same contest, county and candidate. Apply the ID rule where it reproduces the parts exactly; list the rest for me. Reason: Idaho's fault was structural, and a scan can find it where no second count exists.") [measured: `local_volume.py scan`; `check-volume.json` `part3`].
- **What it reads.** Every MEDSL precinct file in the cache for the five years: 156 files, 56,176,755 rows (2016: 2 files; 2018: 51; 2020: 1; 2022: 51; 2024: 51). Precincts are resolved as the normalizer resolves them (a TOTAL mode where there is one, else the modes added up), and grouped by contest and county.
- **What it looks for**, in each contest and county:
  - a row whose precinct is named as an aggregate (a word TOTAL or TOTALS, CUMULATIVE, or "ALL PRECINCTS"), and whether it equals the sum of the county's other precincts for every candidate ("equal"), does not ("unequal"), or has no precinct with votes beside it ("alone");
  - a row not so named that equals the sum of all the others for every candidate, with at least two others with votes beside it.
- Two 2016 files give some states' rows in more than one block: the state-office file Massachusetts, Michigan, Missouri and West Virginia; the local file New Jersey, Washington and West Virginia. The scan holds those states' groups to the end of the file, so a total row in one block and its precincts in another are seen together (`held_whole`). The findings are the same as block by block.
- **The ID rule, applied where it reproduces the parts exactly.**
  - Named rows: the county-total rule now reads a precinct name ending in the word TOTAL or TOTALS ("COUNTY TOTAL", "TOTAL", "Burlington Totals", "Mackinac County Michigan - Total"), not "COUNTY TOTAL" alone (`medsl_precinct.COUNTY_TOTAL`). As before, it drops such a line only where the county's other precincts add up to it, candidate by candidate.
  - Unnamed rows: a new step, `medsl_precinct.drop_sum_rows`, run after the county-total rule. In a contest and county with at least 3 precincts with votes, it drops a precinct that equals all the others together for every candidate. It needs at least 2 candidates with votes there, and drops at most one row per contest and county. *Reason for the guard:* where one candidate alone has votes, one precinct equal to the rest is one number matching another, which can happen by chance; where two or more candidates each match, the row is a copy of the sum.
- **What the rule drops, and what changes.**

| year | state | rows | lines dropped | records that change |
|---|---|---|---|---|
| 2018 | OR | precincts named "TOTAL", in 5 county groups, each equal to its county | 17, and 5 in the federal checks | the governor then equals D2's certified count to the vote (Brown 934,498, Buehler 814,988), and the House too; part 1 passes, so the note it gave 1 record is removed |
| 2022 | ID | "COUNTY TOTAL", 1,033 groups equal | 1,137, and 107 federal | above |
| 2022 | MI | "TOTALS" in 6 groups and "MACKINAC COUNTY MICHIGAN - TOTAL" in 8, equal | 44, and 9 federal | no p: the Attorney General's hold reason now counts 6,146,375 votes (6,153,017 before); 4 notes |
| 2022 | MS | "TOTAL", 7 groups equal | none read | the file gives no record |
| 2022 | NJ | county "TOTALS", "COUNTY TOTAL" and "DISTRICT TOTAL", 45 groups equal | none read | the file gives no record |
| 2024 | NJ | Gloucester's "COUNTY TOTAL" for president, equal | 9 federal | none: the county gate reads the raw file |
| 2024 | AZ | unnamed, all in Yavapai (04025): "SPURS (317.00)" in the 30th district's House and Senate contests, "AZURE (335.00)" in Camp Verde's council, "GHOST (338.00)" in Proposition 480 | 4 rows, 13 lines | the 30th district's p ×1.0137 (House) and ×1.0125 (Senate); Camp Verde's council and Proposition 480 have none |
| 2024 | MS | unnamed: Lafayette's (28071) "Yocona Community Center", Justice Court Judge, Southern district | 1 row, 7 lines | its counts; it has no p |
| 2024 | NY | unnamed: Broome's (36007) "Village of Endicott", Endicott Village Trustee | 1 row, 5 lines | its counts; it has no p |
| 2024 | NJ | unnamed: 140 rows, each a municipality's own row equal to its precincts (Bergen's "Allendale" in Allendale's council, and so on) | 140 rows, 436 lines | 138 local records' and 3 measures' counts; no p moves by it: they were held already by the county gate (Bergen, Mercer) or an unread seat count, and the 3 with p 0 keep it |
| 2024 | IN | unnamed: Hendricks's (18063) "1229-Washington 29", in 7 contests | 7 rows, 19 lines | none |

- **Listed for the orchestrator, not dropped** (the ruling: "list the rest for me").
  - *Rows equal to the rest where one candidate alone has votes* (the guard keeps them): 2016 Kentucky 1; 2018 Illinois 1 and Kentucky 1; 2020 Nebraska 2 and South Carolina 1; 2022 Kentucky 2 and Vermont 1; 2024 Alabama 1, Arizona 2 (Yavapai), Indiana 7, Mississippi 1, North Dakota 1, New Jersey 21 and South Carolina 1. `check-volume.json` gives the first 40 of each file.
  - *Named rows that do not equal their parts*, so the rule keeps them:
    - 2016, MEDSL's state-office file: "TOTAL" in 34 (unequal) groups, "CUMULATIVE" in 11 (unequal), "CUMULATIVE:" in 21 (unequal) and 4 (alone). Its local file: "TOTAL" in 4 (unequal), and "CUMULATIVE:" in 107 (alone).
    - New Jersey 2018: 433 precinct names that end in TOTAL, all in Camden County ("AUDUBON BORO DIST 1 TOTAL", "AUDUBON BORO MAIL-IN BALLOT TOTAL", "AUDUBON BORO PROVISIONAL TOTAL"): 856 groups unequal and 141 alone. They are Camden's precincts, each named as its own total. Camden's House count in MEDSL is within 0.08% of the Official List (part 1's settlement), and no row is equal, so the rule drops none.
    - New York 2018 and 2022: small rows named "Cumulative", in 13 and 16 groups, not the county's sum (Wyoming County's 2022 governor rows of that name carry 114 votes in all).
    - Michigan 2022: one "TOTAL" row, unequal.
    - New Jersey 2022: "DISTRICT n TOTALS" (12 names, 14 groups), unequal; the file gives no record.
    - Illinois 2024: "COUNTY TOTALS" in 204 groups, unequal: they carry candidates with no precinct line (above), and the normalizer keeps those lines.
    - Missouri 2024: "26_CUMULATIVE" in 16 groups, unequal.
    - Oregon 2024: "TOTAL (RESTORED)" in 3 groups, unequal.

**What moves** (against this branch's base, the merge of main at eb5948b; `data/local/moves-volume.json`). 6,168 records change, and the p of 4,859 of them moves; Hawaii's governor's 5 p move besides.
- **By a count of its own:**
  - New Hampshire 2022's legislature (MEDSL's counts): 116 p, ×1.97 to ×2.38 (median ×2.00; one ×1.007); 22 House p no longer computed; 205 notes.
  - Hawaii 2018's governor: its 5 p, ×1.0159 (the file's `governor` section).
  - Arizona's 30th district, 2024 (the sum-row rule): ×1.0137 (House) and ×1.0125 (Senate).
- **Through the fits and like-race pools**, which take New Hampshire's and Idaho's 2022 rows:
  - legislatures: 2023, 102 House and 74 Senate; 2024, 2,771 House and 701 Senate besides Arizona's 30th; 2025, 117 House. All lie within ×0.9929 and ×1.0092 save one: Idaho's 23rd Senate district of 2024, ×0.8628, whose last race (Idaho 2022's, from MEDSL) now reads a Democratic share of 0.1843 in place of 0.1887.
  - local 2024: 976 p, ×0.9994 to ×1.0014.
  - Outside New Hampshire 2022, 70 of the 4,743 moves are 0.5% or more.
- **The checks:** the partisan back-test's 80% interval covers 0.809 of outcomes (0.81 before; `backtest-local-partisan.json`). Nothing else in `data/local` moves.
- **Without a p move:** the volume test's notes (528 records in New Jersey 2018, 232 in Indiana 2018, 6 in Arkansas 2022, 4 in Michigan 2022, 3 in Indiana 2022, 2 in New York 2022) and holds (53 Maine 2016 measures, 2 New York 2018 records); the Idaho statewide offices' 5 reasons and 6 notes; counts changed by part 3 (above). 79 records' p blocks change in their inputs with the p unchanged to 6 places (78 House, 1 Senate). 134 records of 2024 (85 in New Jersey, 47 in New York, and one each in Arizona and Mississippi) only list tied candidates in another order, a side effect of the files' re-normalizing; 3 local forecasts' sd moves in the fourth place (0.1176 to 0.1174) with their p unchanged.

**Refusals and failures in this step.**
- New York's State Board refused at 18:49 UTC.
- New Hampshire's Secretary of State refused at 19:02:32 (403).
- Maine's Secretary of State refused at 19:12:38 (403, CloudFront).
- Oregon's records host failed with HTTP 500 at 19:08:00, 19:08:25 and 19:38:31 on "2018 General Election Official Results", each time cutting the file short. It is recorded as unread (19:13: "one more request per file"). Part 3 settled Oregon 2018 without it.
  - At 19:38:46 the same host gave the 2024 abstract whole. It is cached for the held-totals step. The orchestrator (19:49): a file name is not a mark; the agency's title for it on the page that links it would be. That check needs a request to the records system's page for the file, and is left to the held-totals step.
  - No 2022 file was found by search, so none was requested.
- Indiana's results archive answered 404 at two addresses. Those were wrong addresses, not refusals.

**For the orchestrator:**
- The rows part 3 lists and does not drop (above): one-candidate rows equal to the rest, and named rows unequal to their parts.
- Hawaii's refit of D2's governors (the 2020+ fits and Hawaii 2022's input) is the next step, as its own PR.
- Oregon 2024's mark: the records system's title for the abstract, in the held-totals step.

## 30. Hawaii 2018's governor refit through D2's build, and section 29's counts reconciled

*Added 2026-11-07 at 20:53 UTC, at the orchestrator's order of 19:49 (item 2).* Every move is listed in `data/local/moves-governor-hi-refit.json`.

**Why.** The orchestrator, 19:49: "The two leftovers should not stay wrong if they can be refit. After the volume PR, refetch D2's governor sources from the documented downloads D2 already used, with no new hosts. Rerun its governor build so the 2020+ fits and HI 2022's input take 131,719. Do it as its own small PR and list every move. If a source refuses, keep the notes as you have them."

**What was fetched** (20:31 to 20:33 UTC, into the cache outside the repository; D2's own intake scripts, unchanged).
- From Harvard Dataverse:
  - Cha, Kuriwaki and Snyder v4.1;
  - Algara and Amlani's county returns;
  - MEDSL's Senate v8.0 and President v10.1.
- From the other hosts D2 used:
  - The Downballot's sheets (Google Sheets export);
  - 538's checking-our-work data (GitHub);
  - the party divisions (senate.gov, history.house.gov);
  - New Jersey's 2025 governor county copies (nj.gov).
- The National Archives' pages were already in the cache. Nothing refused.
- **Virginia 2025.** The Department refused at 18:27, and a refusal binds the whole agency, so D2's reader of its API was not run. `state_governors.va_cached` reads the governor from the election's Media Export instead. That file was read at 18:24, before the refusal, and the ruling of 18:30 allows such files. It uses D2's gate: the page is headed "OFFICIAL RESULTS", the 133 localities add up, and the page shows the count. Its four figures equal D2's record to the vote.
- **The test of the refetch** [measured]. D2's code from before this change was run on these files. It writes `data/congress/backtest.json` and `backtest-governor-odd.json` byte for byte as committed. Every contest of every governor, House and Senate file comes out as committed, stamps aside. Only `history.json` differs: it had not been rewritten since #95 changed Hawaii 2018's five p.

**The change** (`pipeline/governor_hi2018.py`).
- `fix_cha` sets Hawaii 2018's governor in Cha's contests, as D2's build reads them, to the certified summary: Tupola 131,719 and the total 390,843.
  - `chambers._load` and `build_congress.cha_index` apply it, so every fit, back-test and last-race index takes it.
  - It stops if the dataset's figures are not the ones expected.
- `last_race` reads Hawaii 2022's input again. The last governor race's Democratic share moves from 0.640094 to 0.650291.
- Then `chambers.py odd`, `backtest`, `compute` for 1977 to 2025, and `history` were run.
- Hawaii 2018's note now says the fits and the input follow the certified count. Hawaii 2022 gets a note on its input.

**What moves** [measured: against d94468b, main with this change's code; stamps aside].
- **Governor p of record: 29, all the model's own.**
  - By year: 2019, 1 (Kentucky); 2020, 11; 2021, 2 (New Jersey, Virginia); 2022, 3 (Ohio, Wisconsin, Wyoming); 2024, 10; 2025, 2 (New Jersey, Virginia).
  - The range is ×0.9950 (Wyoming 2022) to ×1.0003 (Vermont 2020).
- **The p beside.** Those 29 move, and so do 30 more of 2022 whose p of record is 538's and stays. Among them is Hawaii 2022's own model, ×0.9948 (normal) and ×0.9878 (t4), from its input.
- **No House or Senate p moves.** The near-tie factor shown beside them, not of record, is fitted on a pool that takes the governors in. It moves by less than 0.002% on 107 House records of 2022 and 65 Senate records of 2022 and 2024.
- **The files' own blocks:**
  - each governor file of 2019 to 2025: the fit's terms, k and sd;
  - each odd-year file of 1985 to 2017: the odd-year test's gain for the midterm term (0.05676 to 0.05681), printed in each;
  - the House files: the near-tie switch test, shown beside.
- **The back-tests.**
  - The governors' pooled log score moves from 1.14362 to 1.14380 (calibrated, 2006 to 2024).
  - Their k for 2020, 2022 and 2024 move in the fifth place.
  - The odd-year plain route moves from 1.09708 to 1.09701.
  - No verdict changes:
    - no variant is adopted;
    - the House's near-tie factor stands alone;
    - Cha's codes of record stay;
    - the plain route stays for odd years;
    - the lean note stands.
- **`history.json`** now carries Hawaii 2018's p from #95 and these moves.

**Section 29's counts, reconciled** (the orchestrator, 20:28: "Your note says 4,859. If REPORT says the same, reconcile it with 4,860 + 24") [measured: every record of `data/`, d7eea96 against 6b24927].
- 4,860 records' p moved. They are the 4,859 records listed in `moves-volume.json`, plus Hawaii 2018's governor record. That record's five p (its own and the four beside it) are listed in the file's `governor` section.
- 22 p were lost, all in New Hampshire 2022 House contests:
  - 21 had a p above 0;
  - Strafford 15's p was 0.
- None was gained. The files show 22 lost, not 24.

**For the orchestrator:**
- D2's report (`data/congress/REPORT.md`) is not changed here. Its figures for the governors' back-test now differ by the amounts above.

## 31. Held totals: Oregon's abstract, Arizona's recount, the over-ballot test, M2's readings, the listed rows, Virginia's gate, and two of Klarner's districts (c38)

*Added 2026-11-07 at 21:50 UTC, at the orchestrator's orders of 17:44, 18:49, 20:28, 20:30, 20:55, 21:03 and 21:21.* Every record that changed is listed in `data/local/moves-held-totals.json`, by group, each group with its reason. The tests are in `data/local/check-over-ballot.json` and `data/local/check-listed-rows.json`.

**Why.** The orchestrator, 17:44: "read held contests' certified totals where the agency answers"; a statewide contest whose lines miss counties is held unless the state's own total is read, since a partial count shows the wrong n and can draw the wrong winner (16:47).

**Oregon 2024's Supreme Court** (`pipeline/intake/or_sos.py`; `local_medsl._or_state`).
- The source: the Secretary of State's abstract of votes of the 2024 general, from its records system (record 13735458), read 19:38 UTC. Every page is headed "November 5, 2024, General Election Abstract of Votes". The document prints no word "official" or "certified" [stated: the document].
- **No mark.** One request to the records system's Record Viewer, 20:56:06 UTC, found the record titled "2024 November General Election Official Results(2).PDF" [stated: the page]. That is the uploaded file's name. Ruled 21:55: "the "(2)" shows that. 15:16 excludes a file name, and 19:49 asks for the document's or the linking page's own words. So the abstract carries no mark. P7 goes back to held as before, and the abstract's figures can stay in a note, unmarked."
- So both positions stay held, as before this step. Each record's notes quote the abstract's figures, unmarked and not taken, and each hold's reason says the abstract carries no mark. The file's `sources.or_sos` names the abstract.
  - Position 7: Bronson D James 1,212,011, Misc. 23,702; each candidate's 36 county lines add up to its Total line.
  - Position 1: Stephen K Bushong 1,221,817, Misc. 26,077; its write-in line's county lines add up to 26,078, one more than its Total line.
- Oregon 2022: no abstract of the 2022 general was found (two web searches of the state's hosts, 20:57 UTC), so none was requested and its one contest held in part stays held.

**Arizona 2022's Attorney General** (`local_medsl.az_recount`).
- MEDSL's general lines are the count before the statewide recount the margin set off. The record now says so: `result.count_stage` "count before the recount, certified count unread", with a note.
- Unread: the Secretary of State (azsos.gov, 403, Cloudflare) and the Maricopa County Clerk of the Superior Court (403 at 21:02:40 UTC) refused. The court's order is found only as a copy on a third party's host. Ruled 21:03: "a third party's copy of the filing does not count here ... a count of record has to come from the body that certifies it or another body of the state."

**The over-ballot test** (`local_medsl.over_ballot`; `local_volume.py ballots`, part 4; the order of 17:44: "Hold a one-seat contest whose votes exceed ballots cast, where the source gives them. Where it doesn't, hold one that exceeds the day's highest-vote statewide contest by more than 10%, and list for me any between 1.0x and 1.1x.").
- **Ballots cast** are read from MEDSL's own lines, as in New Jersey's ruling of 11:16: a contest's votes, overvotes and undervotes, or its CONTEST TOTAL, or a line named as the ballots cast. A contest is bounded by other contests' lines only, never its own. A contest is tested against ballots where every one of its precincts has such a figure.
- **The day's top contest** otherwise: the most votes among the state's other whole one-seat candidate contests that day, its whole statewide questions, and MEDSL's president and US Senate lines. A held contest is no one's top.
  - *Questions are counted* (my reading, confirmed by the orchestrator at 21:55: "The comparator stands in for ballots cast, and a question on every ballot statewide stands in as well as an office does"). Without them, Montana 2022's Supreme Court seat 2 (440,378) is 1.11 times seat 1 (396,278); Legislative Referendum 131 (448,905) puts it at 0.98.
- **Read:** MEDSL's counts only here. A state's own count read in their place (Indiana 2024, North Carolina, Idaho's statewide offices) is not tested in this step. The orchestrator, 21:55: "Test every count shown, whatever its source"; that comes in the next step. 2016 is read for its questions only and 2020's file holds local offices only, so neither has a contest to test.
- **Found** [measured]:

| Year | Read | Against ballots cast (highest) | Against the top contest | Held | Listed, 1.0 to 1.1 times |
|---|---|---|---|---|---|
| 2018 | 191 | 31 (Florida's Attorney General, 0.978) | 160 | Michigan's Supreme Court, 1.47 times the governor's; Ohio's Supreme Court, 1.60 | Illinois's Secretary of State, 4,570,842 against the governor's 4,560,012 (1.002) |
| 2022 | 136 | 8 (Alabama's Attorney General, 0.989) | 128 | Hawaii's at-large trustee, 1.81; Michigan's Attorney General, 1.39 | Delaware's Attorney General, 319,206 against the Treasurer's 317,745 (1.005) |
| 2024 | 81 | 15 (Utah's Attorney General, 0.948) | 66 | Texas's Supreme Court, 32,783,005 votes, 2.87 times the president's | none |

- The four held before keep their holds, their reasons restated against the top contest. **Texas 2024 is new.** MEDSL files seven candidates under one office, "STATE SUPREME COURT JUSTICE", one seat: Blacklock, Devine, Bland, Weems, Jones, Goldstein and Roberson. That is three seats filed as one [inferred: 2.87 times]. It had no p before (too few like races), so no p is lost.
- The two listed carry a note.

**M2's readings** (`checks/M2-REPORT.md` §12.4; the orders of 18:13 and 20:30).
- (a) The moves file of #90's towns and counties: its codes B and Q are worded as what they mark, and an amendment sentence is added to its `about`. No record changes.
- (b) Idaho 2024's recalls (fix_questions rule 6). A recall's "AGAINST RECALLING" line, filed as a candidate's line, joins the question carrying the other answer, of the same date, office, subject and counties. It joins Latah County's recall of Judi Fuller, as M2 found, and Marsh Valley School District's recall of Kathy Egan, by the same rule. The two local records are gone; the two questions now carry both answers. Still no p: a local threshold is not read.
- (c) North Carolina's Court of Appeals of 2008 ("Martin Seat") and 2010 ("Steelman Seat") are typed judge, not statewide judge: neither title nor the State Board's file gives a seat count of one (18:13: "one seat only where the contest's own title or the State Board names one seat, otherwise typed judge"). p stays 0.
- (d) The "Town of" guard (`places.py`): a title that names another body after the town's name ("Library", "Fire", "Authority", "Sewer") is no longer counted whole by the town. It moves five 2024 questions: Poughkeepsie's library proposition (New York), and Barrington, Cumberland, Johnston and North Kingstown's questions (Rhode Island). They are counted by county; none had a p.
- **Sixth pass (a): Arizona 2024's Corporation Commission** is one contest of 3 seats. MEDSL's file gives its rows 3 seats in 13 of the 15 counties (Santa Cruz's filed under districts 001 to 003). Maricopa's and Pima's rows give 1, but there the contest's votes, overvotes and undervotes are 2.99 times the president's (Maricopa 6,213,612 against 2,078,930; Pima 1,550,565 against 518,466) [measured]. The pieces cover all 15 counties, so they are joined (16:47). It is still not computed: too few like races of its class.
- **Sixth pass (b): Michigan 2022.** M2's totals, 6,153,106 for the Attorney General and 4,432,378 for Governor, are the figures of #90 (6,153,017 and 4,432,311) plus MEDSL's "REJECTED" lines in Ottawa County (89 and 67), which fix_questions' rule 2 leaves out as not votes [measured]. After #95 dropped Michigan's total rows the record reads 6,146,375 against 4,424,918, 1.39 times, and stays held.

**The listed rows** (`local_volume.listed_rows_summary`; `local_medsl.listed_rows`; the order of 20:28: "For each one, compute the record it falls in with and without the row. Where the difference is more than 0.5% of the record's total, add a note on the record ('a possible total row in the source, not dropped'). Otherwise the list in REPORT is enough.").
- A row falls in the contest of MEDSL's counts of the same state, office, district, stage and dataverse whose counties hold the row's county; its votes are those of the contest's candidates it names. Rows of the federal dataverses are counted only.
- [measured]: 

| Year | Rows | In a record | In a contest that became no record | In no contest the build reads | Noted (records) |
|---|---|---|---|---|---|
| 2016 | 182 | 0 | 0 | 182 (candidate contests: 2016 is read for its questions only) | 0 |
| 2018 | 142 | 6 | 5 (New York's governor and legislature) | 131 (New Jersey's Assembly 5, Camden: precincts named "... TOTAL", alone in the contest) | 1 (1) |
| 2020 | 3 | 2 | 0 | 1 | 2 (2) |
| 2022 | 22 | 4 | 10 | 8 | 1 (0: New Jersey's Assembly 12, no record) |
| 2024 | 56 | 43 | 1 | 12 | 26 (24) |

- **The 27 noted records.** 23 are rows equal to the rest of their contest with one candidate alone holding votes, so the contest's count is twice its precincts' (50% of it): 20 in New Jersey 2024's Bergen County, Yavapai's Board of Supervisors 1 and Cottonwood's council (Arizona 2024), Walthall's election commissioner (Mississippi 2024), and Kentucky 2018's Magistrate 4 (Hardin, C101). The others: Nebraska 2020's Western Community College board (5.7%) and Cuming County's power district (0.7%); Illinois 2024's Bureau/Henry/Stark superintendent, whose three "COUNTY TOTALS" rows carry all 231 of its votes.
- No p rests on these counts: 6 have p 0 (one name for the seat), the 20 of Bergen are held already by New Jersey's county gate (Bergen's 2024 counts do not add up to the certified federal counts there), and Illinois's superintendent is not computed (write-ins against one name). The counts shown are the question.

**Virginia's legislatures of 2023 and 2025** (the ruling of 18:49). Each record's gate now carries the ruling's words as RULED: "accepted as proposed, with the 9th Senate district of 2023 held". The four shortfall notes add "not explained (no source read says why)".

**D2's report.** A dated line in `data/congress/REPORT.md` after its opening paragraph gives the Hawaii refit's figures (#96), D2's text left as written (20:55).

**c38: two of Klarner's districts** (`pipeline/local.py c38`; the order of 21:21).
- **Idaho 2022, Senate 1.** Klarner has Scott Herndon unopposed, 13,064, p 0. The state's canvass (cached by `intake/id_sos.py`; its legislative workbook, sheet "Leg Dist 1", DIST. TOTAL row) gives Herndon 13,064, as Klarner does, and "Steven R Johnson (W/I)" 9,025 [stated: the canvass]. MEDSL marks him a write-in too [measured]. So he was not on the ballot. He is added as a write-in, and the write-in rule applies (21:26: "Apply the existing write-in rule to it"): he has 69% of Herndon's votes, more than 10%, so p is not computed.
- **Vermont 2018, Chittenden Senate** (six seats). Klarner's figures are 2.78 to 3.83 times MEDSL's, candidate by candidate: its total is 1,096,537, MEDSL's 310,430 [measured]. MEDSL's counts are taken where all 13 named candidates match one to one by surname, with MEDSL's write-in lines as the scattering, as for New Hampshire 2022. Vermont's election archive answered one request (21:35:09 UTC) with "Not Found", so no state count is read. p moves ×3.49 (2.33e-05 to 8.14e-05).
- The district checks across every Klarner-MEDSL overlap (21:21, (a) and (b)) come next, as their own PR.

**What moves** [measured: against bcd1ce9; stamps aside; `moves-held-totals.json`].
- **p moved:** 1 (Vermont 2018 Chittenden, ×3.49).
- **p no longer computed:** 1 (Idaho 2022's Senate 1, from 0).
- **Records gone:** 2 (Idaho 2024's two recall lines, joined into their questions).
- **Typed anew:** 2 (North Carolina's two Courts of Appeals).
- **Reasons changed, p not computed before or after:** 15 (the four over-ballot holds restated, Texas's Supreme Court, Arizona's Corporation Commission, Oregon's two positions; the two recall questions; the five "Town of" questions, now counted by county).
- **Notes only:** 30 local records (the 27 listed-row notes, the two over-ballot listings, and Arizona's Attorney General).
- **Virginia:** the gate's RULED text on all 240 records of 2023 and 2025; "not explained" on the 4 with a shortfall note.
- No other p moves: the fits that take Vermont 2018 and Idaho 2022 as rows move no p.

**For the orchestrator:**
- The 23 doubled one-candidate counts are noted, as ordered, and not dropped. No p depends on them, but each shows twice its precincts' count. Ruled 21:55 (3), for the next step: such a row is dropped as a subtotal where the county shows the same pattern in its other contests in the file, or where dropping it reproduces an independent count.
- New Jersey 2018's Assembly 5 rows (131 precincts named "... TOTAL") fall in no record of MEDSL's: that year's legislature is Klarner's.

## 32. District checks: Klarner's legislatures beside MEDSL's, MEDSL's own coverage, the coarse tier, and the 21:55 items

*Added 2026-11-13 at 00:20 UTC, at the orchestrator's orders of 2026-11-07 21:21, 21:26, 21:55, 22:19, 22:26 and 22:42. The thread stopped at 23:31 that night on a usage limit and resumed on 2026-11-12 at 23:07; nothing was fetched in between.* The checks are in `data/local/check-districts.json` and `data/local/check-districts-m2.json` (`pipeline/local_districts.py`); every record that changed is in `data/local/moves-district-checks.json`.

**Why.** The orchestrator, 21:21: "(a) flag any district whose ratio is off 1 by more than 3%; (b) flag any Klarner record coded uncontested where MEDSL shows another candidate with votes beyond scattered write-ins. Settle each by the state where it answers. Where it doesn't, use the 19:04 rules." 21:26: a write-in opponent is not a ballot opponent (the write-in rule); settle from the state only where its file is cached or it answers one request; "List every flag with its outcome, and count the p moved, lost and gained by level and year"; run every overlap year.

**The check** (`local_districts.py check`). Each of Klarner's general contests of 2016, 2018 and 2022 (the years MEDSL also holds a legislature; 2020's file is local offices only) is matched to the MEDSL contest of its state and chamber that names all its candidates by surname, district number and New Hampshire's county breaking ties. Candidates are paired one to one; a candidate's fusion lines are summed; write-in totals, "ALL OTHERS", blanks and voids are not candidates, nor are New York 2016's ballot-kind lines ("Affidavit", "Absentee/Military"). Klarner's contests are read as the build reads them (North Carolina's Board counts, New Hampshire 2022, c38), so a district those fixes settled is listed as settled.

| Year | Tested | Flags | Unmatched or not paired apart (untested) |
|---|---|---|---|
| 2016 | 4,631 | 155 | 905 |
| 2018 | 4,978 | 76 | 403 |
| 2022 | 5,080 | 130 | 580 |

**MEDSL's own coverage** (the orchestrator, 22:26: "(a) in each county of the district, compare the chamber's MEDSL precinct rows with the precincts of the day's top contest; if MEDSL lacks the chamber's rows in any county of the district beyond 2% of that county's precincts, MEDSL does not cover the district. (b) There, a Klarner count above MEDSL's stays, with a note naming the counties and the share missing. (c) A Klarner count below MEDSL's partial count: the 19:04 rule. (d) Where MEDSL covers the district, the 19:04 rule. (e) A district with no MEDSL rows at all is untested, not held. List the counts under (b) to (e) by state and year in the PR.") `local_districts.coverage(year)` reads every MEDSL file of the year county by county (`COVER_VERSION` 12, cached in `$VOTE_CACHE/volume/normalized/coverage-<year>.json`).
- *The top contest* is the candidate contest with votes in the most precincts (a question only where a county has none), since MEDSL's 2018 Virginia file names a question's absentee precincts apart [measured]. A precinct's votes are its TOTAL mode's or its other modes' sum, whichever is more: a file can give both, or give one candidate a TOTAL line of 0 beside another's modes (Delaware 2018's US Senate in New Castle County) [measured].
- *Lines that are no contest* are left out: straight party, registered voters, ballots cast, turnout, voting statistics (Wayne County, Michigan, 2022 files "STRAIGHT PARTY" in 1,253 precincts, more than any contest's 1,069) [measured].
- *Precincts missed* are the set difference, but no more than the difference in counts, since a file can name one precinct apart in two contests. Names are folded for case and spacing, and a name the top contest gives once is matched under another jurisdiction code or as a '/'-joined part (Maine 2024 codes one town's precinct three ways and files an unorganized township alone in one contest and joined to a town in another) [measured].
- *A special contest's rows* count for its family, though never as the top contest: Texas 2024 files the regular TX-18 contest as special, which left 240 Harris County precincts without a US House row [measured].
- *A chamber's row with no district* is missing (22:42 item 4, Maricopa 2016); a US House row with no district is not (Santa Cruz County, Arizona, 2022, files 9 of its 35 precincts' US House rows so) [measured].
- *Staggered upper chambers* (22:42 item 3: "the other chamber's rows, or the top contest; not covered means untested"): a chamber is all up where its districts that year are at least 90% of its most on the same lines (2012-2020; 2022 against 2012-2022). Vermont's 2022 chambers have 16 and 109 districts to 13 and 81 before [measured], so they are read against their own lines. Flags read so: 2018 Illinois's Senate, 1 flag by the House's rows; no district was left untested by the top contest.

**Counts under (b) to (e), by state and year** [measured]. (b) kept with a note; (c) a Klarner count below MEDSL's partial count, by the 19:04 rule; (d) MEDSL covers the district, by the 19:04 rule (held at a gap of 5% or more, noted under it); (e) untested: no MEDSL contest of the chamber names all the district's candidates, or several do, or the candidates do not pair one to one (most are seats left off the ballot unopposed: Florida, Oklahoma, Texas, Arkansas, West Virginia 2022). The other outcomes: the write-in rule (a (b) flag whose other candidates are all write-ins, added as write-ins), settled by the state (Idaho's 2022 canvass, cached), settled earlier (New Hampshire 2022).

| Year | State | (b) kept | (c) held | (c) noted | (d) held | (d) noted | (e) untested | Write-in rule | Other |
|---|---|---|---|---|---|---|---|---|---|
| 2016 | AR |  | 2 |  |  |  | 87 |  |  |
| 2016 | AZ | 13 |  |  |  |  | 3 |  |  |
| 2016 | CT |  | 1 |  |  |  | 9 |  |  |
| 2016 | DE |  |  |  |  |  | 48 |  |  |
| 2016 | FL |  | 1 |  |  |  | 82 |  |  |
| 2016 | GA |  |  |  | 1 | 1 | 2 |  |  |
| 2016 | HI |  | 1 |  |  |  | 27 |  |  |
| 2016 | ID |  |  |  |  |  | 33 |  |  |
| 2016 | IL |  |  |  |  |  | 16 |  |  |
| 2016 | IN | 8 | 1 |  | 23 | 5 | 9 |  |  |
| 2016 | KS | 17 |  |  |  |  | 7 |  |  |
| 2016 | KY | 6 | 2 |  | 4 | 5 | 2 |  |  |
| 2016 | MA |  |  |  | 1 |  | 25 |  |  |
| 2016 | ME | 20 | 1 |  |  |  | 140 |  |  |
| 2016 | MI |  |  |  | 2 |  | 1 |  |  |
| 2016 | MT |  | 1 |  |  |  |  |  |  |
| 2016 | NC |  |  |  |  |  | 10 |  |  |
| 2016 | NE |  |  |  |  | 1 | 1 |  |  |
| 2016 | NH |  |  |  |  |  | 204 |  |  |
| 2016 | NY | 17 | 4 | 2 | 1 |  | 6 | 2 |  |
| 2016 | OK |  |  |  |  |  | 34 |  |  |
| 2016 | RI |  |  |  |  |  | 11 |  |  |
| 2016 | SC |  |  |  | 2 | 2 |  |  |  |
| 2016 | TX |  |  |  |  |  | 99 |  |  |
| 2016 | UT | 3 | 1 |  | 2 | 1 | 5 |  |  |
| 2016 | WV |  |  |  | 1 |  | 1 |  |  |
| **2016** | **all** | **84** | **15** | **2** | **37** | **15** | **905** | **2** |  |
| 2018 | AL |  |  |  |  | 1 |  |  |  |
| 2018 | AR |  |  |  |  |  | 67 |  |  |
| 2018 | CT |  |  |  | 1 | 1 | 8 |  |  |
| 2018 | DE |  |  |  |  |  | 2 | 2 |  |
| 2018 | FL |  |  |  |  |  | 50 |  |  |
| 2018 | HI |  |  |  |  |  | 37 |  |  |
| 2018 | IL |  |  | 1 |  | 1 | 3 |  |  |
| 2018 | IN | 4 |  |  | 4 | 2 | 6 |  |  |
| 2018 | KS |  |  |  | 1 |  | 2 |  |  |
| 2018 | KY |  |  |  |  | 1 | 11 |  |  |
| 2018 | MA |  |  |  |  | 1 | 2 |  |  |
| 2018 | ME |  |  |  | 5 |  | 14 |  |  |
| 2018 | NY | 3 |  | 2 | 1 |  | 77 |  |  |
| 2018 | OH |  | 1 |  | 1 |  | 2 |  |  |
| 2018 | OK |  |  |  |  |  | 35 |  |  |
| 2018 | OR |  |  |  | 1 |  | 1 |  |  |
| 2018 | SC | 1 |  |  |  |  | 1 |  |  |
| 2018 | TN |  |  |  |  |  | 1 | 3 |  |
| 2018 | TX |  |  |  |  |  | 19 |  |  |
| 2018 | UT | 1 |  | 1 | 1 |  | 7 |  |  |
| 2018 | VT |  |  |  | 4 |  | 25 | 31 |  |
| **2018** | **all** | **9** | **1** | **4** | **19** | **7** | **403** | **36** |  |
| 2022 | AR | 1 |  |  | 1 |  | 9 |  |  |
| 2022 | AZ |  |  |  |  |  | 7 | 4 |  |
| 2022 | CA |  |  |  |  |  | 21 |  |  |
| 2022 | FL |  |  |  |  |  | 72 |  |  |
| 2022 | IA | 1 |  |  |  |  | 1 |  |  |
| 2022 | ID |  |  |  |  |  | 4 |  | settled by the state 2 |
| 2022 | IN | 36 |  |  | 11 |  | 56 |  |  |
| 2022 | MA |  |  |  |  |  | 13 |  |  |
| 2022 | ME |  |  |  |  | 1 | 3 |  |  |
| 2022 | MI | 3 |  |  | 7 | 1 | 5 |  |  |
| 2022 | MO |  |  |  | 1 |  |  |  |  |
| 2022 | ND |  |  |  |  |  | 18 |  |  |
| 2022 | NH |  |  |  |  |  | 28 |  | settled earlier 2 |
| 2022 | NM |  |  |  | 1 |  | 3 |  |  |
| 2022 | NY | 1 | 2 |  | 5 | 1 | 6 | 1 |  |
| 2022 | OK |  |  |  |  |  | 93 |  |  |
| 2022 | PA |  |  |  |  | 2 | 2 |  |  |
| 2022 | TX |  | 1 |  |  |  | 80 |  |  |
| 2022 | VT |  |  |  | 1 | 14 | 8 | 29 |  |
| 2022 | WA | 1 |  |  |  |  | 2 |  |  |
| 2022 | WV |  |  |  |  |  | 100 |  |  |
| **2022** | **all** | **43** | **3** | **0** | **27** | **19** | **580** | **34** | settled by the state 2, settled earlier 2 |

Rows list each state with a flag, or with 10 or more districts untested.

- **(b): 136 districts kept** (84, 9 and 43). Arizona 2016's 13 are Maricopa's (10), Coconino's (2) and La Paz's (1): their rows give no district, so all their precincts count as missing (22:42 item 4). Indiana 2022's 36: MEDSL's 2022 Indiana file is short (§29: -57%).

**The comparison with M2's list** (22:19 item 2: "Compare these flags with M2's `checks/m2/c38-districts.json` (249 districts 5% or more off) and list each difference with its reason"; M2's list read from PR #99's head, c2f02ff, not yet merged). `check-districts-m2.json` gives each of the 249 a status and reason, and lists the flags not on M2's list by kind.
- On both lists: 108 (67, 17, 24).
- M2's alone, 141: within 3% here on the named candidates, 80 (M2 sums MEDSL's rows by D+R (55) or by every line (25), where this check sums the named candidates' lines: so New York's and Connecticut's fusion lines, Washington's same-party pairs, and write-in and scattering lines count apart [inferred from the method; each district's two sums are in the file]); unmatched here, 32 (no MEDSL contest names all the candidates; M2 matches by the district's code); settled before this check, 26 (the build's own fixes, which M2's raw read does not see: New Hampshire 2022's names and doubling, North Carolina's Board counts); not paired one to one, 2; matched to several, 1.
- Here alone, 252: (a) off 3% to 5%, under M2's 5% line, 25; (a) off 5% or more on the named candidates where M2's D+R or every-vote sum, or its match by code, is not, 128; (b) only, 99 (M2 does not test an uncontested record).

**The coarse tier** (22:42 items 1 and 2; `pipeline/local.py coarse_tier`). A district's votes (its post with the most) against its seats' share of the state's turnout that day (D1's or D2's certified count).
- *Idaho 1984-1990*: one post per district adds to 1.65 to 1.89 times the turnout. "Hold every post of a district whose votes exceed 2x its seats' share of turnout." The 2x line gives seven districts each year, not the six the ruling names: 4, 8, 13, 21, 25, 29 and 33. Their 21 posts a year are held (14 House, 7 Senate; 84 in all). The other 420 posts keep their p, each with a note giving the chamber's ratio, the districts held and its own ratio, at most 1.60. No Idaho count before 1994 was found (the Secretary of State's canvass starts in 1994, its pages in 1998), so no request was made.
- *South Carolina's Senate, 1976 and 1980*: its 46 seats are 16 districts' numbered posts, each voter voting once in each post; one post per district adds to 0.91 and 0.88 times the presidential vote. No hold; each of the 92 seats carries the note.

**MEDSL's coverage gate** (22:19 item 1: "Treat any contest whose rows are missing in part of its district as incomplete: held, no p, unless a certified count is read"; `local_medsl.coverage_gate`).
- *The county gate* (`incomplete_counties`): a county whose US House rows miss more than 2% of its precincts, holding more than 2% of its top contest's votes. It is read from the US House's rows alone, since Florida, Oklahoma, Texas and Kansas 2022 leave unopposed legislative seats off the ballot or the file; a state that left a US House seat off the ballot (D2's record: no votes) is not read. A MEDSL contest below the state whose area includes such a county is held, unless its own rows are in the county's precincts (within 2%; `whole_contests`: its district is the county, and its rows are not missing there), or it is a legislative seat whose own chamber's rows miss 2% or less of the county's precincts (22:26 (a)) [my readings].
- Monroe County, New York, 2024: the US House's rows miss 196 of its 655 precincts (28.6% of the votes), the Assembly's 181, the Senate's 1 [measured] (M2: 200 of 659 and 185, its count of precincts). Held: the Assembly's districts 130 and 133 to 139 (8 records; 134 and 139 had p 0), Irondequoit's and Pittsford's town contests and Greece's and Rush's questions (no p before). The seven local contests with one name on the ballot (the City Court Judge, Brighton, Hamlin, Parma, Rush, Sweden, Wheatland) keep p 0, as every held one-name local contest does (16 records before this step, Washington's and Wyoming's of 2022 [measured at the rebuild of section 33; a count of 127 written here first was wrong]): their p rests on the ballot's one name, not on the count (`local_medsl`, route zero). A held legislative seat loses its p 0 (districts 134 and 139), as before this step. The county's Clerk, Court Judge and Family Court (rows in all 655) and the Senate's districts 54, 55 and 56 are not held. Monroe's Board of Elections answered the one request allowed (its 2024 certification, monroecounty.gov) with "Page Not Found" at 22:30:04 UTC on 2026-11-07; Ontario's board was not asked, since no p of MEDSL's rests on Ontario (its US House rows are whole, 92 of 92).
- The other counties caught: 
  - 2018: Kennebec County, Maine (the US House's rows miss 17 of its 30 precincts, 37% of the votes): its County Commissioner 2 and District Attorney 4 are held (no p before). Dutchess, Herkimer, Montgomery, Rensselaer and Westchester Counties, New York: New York 2018 is held already (§29), so no record changes.
  - 2022: Barry County, Michigan (2 of 26 precincts, 2.9%: two precinct names misspelt in the US House's rows, 'CARLETON' and 'PRECINCNT') and Midland County (38 of 44, 89%); Ulster County, New York (69 of 164, 37%). No record changes: the records there are statewide contests, read by the statewide test, or are held already.
  - 2024: Cass County (21 of 36, 57%) and Union County (1 of 11, 2.7%: a joint-school precinct), Indiana: no record changes, since Indiana 2024's records are the state's own counts (`in_enr`).
- *Statewide contests* (`statewide_short`): a contest with rows in 90% or more of a state's counties whose rows miss more than 2% of a county's precincts. Its district is the state, so it is held where the votes missed are more than 2% of the state's (the counties' top contests summed), and noted otherwise [my reading]. Held: New York 2024's Proposal One (the rows miss 624 of Monroe County's 655 precincts, 3.81% of the state's votes; p 9.9e-08 before). Noted, at 2% of the state's votes or less: 33 records (1 in 2018, 14 in 2022, 18 in 2024: Michigan, Minnesota, Nevada, Oregon and Washington). The list's other held entries (Connecticut's registrars, one contest per town; Hawaii's, New Hampshire's and Rhode Island's US House districts; New Hampshire's commissioner district 3, one per county) reach 90% of a state's counties without being one contest, and hold no record. Delaware 2018's US Senate, Attorney General and US House were listed until the TOTAL lines of 0 were read (above); none is now.

**The 21:55 items.**
- (2) "Test every count shown, whatever its source." The over-ballot test now reads the state's own counts too (North Carolina's Board, Idaho's statewide offices, Indiana 2024, North Dakota's Auditor): 31 more contests (4 in 2018, 12 in 2022, 15 in 2024), none held. Listed between 1.0 and 1.1 times, each with a note: Idaho 2022's Attorney General (Idaho's count, 1.004 times the Lieutenant Governor's) and Indiana 2024's Attorney General (1.094 times Public Question 1). A failing state count would stop the build until re-read (`STATE_OVER_REREAD`); none failed.
- (3) Subtotal rows: 22 one-candidate rows equal to the rest of their contest in the county are dropped where the county shows the pattern in another contest of the file: Bergen County, New Jersey, 2024 (20 rows; its records are held already by New Jersey's county gate) and Yavapai County, Arizona, 2024 (2: Board of Supervisors 1 and Cottonwood's council, now counted once). A lone match stays with its note.
- (4) Oregon's 2024 Supreme Court positions 1 and 7 are typed statewide judge by the seat (`statewide_seat`); both stay held.

**22:19 item 4.** North Carolina's Board years 2000 and 2010, at -0.7% against the president's lines, keep their p; each record's note cites the 19:04 rule (1,109 records, 26 of them questions).

**What moves** [measured: against fd0af11; stamps aside; `moves-district-checks.json`].
- **p no longer computed: 197.** State legislatures: Idaho 1984-1990, 84 (the coarse tier); the district checks, 104 (2016: 45 House, 7 Senate; 2018: 15 House and 7 Senate, two of the House's Vermont's seats whose write-in candidate has 69% and 11% of the winner's votes, now added under the write-in rule; 2022: 14 and 16); Monroe County's Assembly of 2024, 8. Questions: New York 2024's Proposal One, 1.
- **p moved by more than 1%: 441** (316 House, 125 Senate; 121 by more than 3%, from x0.857 to x1.195). Those over 3% move with their chamber's lean, read from districts now held [measured: one record of each state and year]; the others by the same path [inferred]: Georgia, Indiana and Massachusetts 2018 House; Kentucky and New York 2018 Senate; Indiana 2020 Senate; Arkansas, Indiana and Vermont 2024 Senate; New York 2024 House.
- **p moved by 1% or less: 72,058** (local 1,812; House 53,952; Senate 16,294; x0.9901 to x1.0099): the fits lose the held districts. Counted by level and year in the file, not listed.
- **Not computed before or after, the reason changed: 6** (Kennebec's two, Monroe's two town contests and two questions).
- **Typed anew: 2** (Oregon's positions 1 and 7, statewide judge).
- **Notes:** 1,109 North Carolina records (19:04); 420 Idaho and 92 South Carolina seats (the coarse tier); 33 statewide notes; 22 subtotal notes; 2 over-ballot listings; the kept (b) and noted flags' notes on Klarner's records.

**For the orchestrator.**
- Idaho's 2x line gives seven districts a year, not six; built as the rule reads.
- The county gate is read from the US House's rows, with countywide contests whose own rows are whole and legislative seats whose own chamber's rows are whole released; statewide contests are held only past 2% of the state's votes. These are my readings of 22:19 item 1 and 22:26 (a).
- Name artifacts that survive the matching (Barry County, Michigan, 2022: two precincts misspelt, 2.9% of its votes; Union County, Indiana, 2024: one joint-school precinct, 2.7%) stay on the county list as the rule reads; no record rests on them.
- Ontario County was not asked; no p rests on it.
- A held legislative seat with one name loses its p 0 while a held local one keeps it: a difference between the two builds that predates this step.

## 33. Virginia's 2023 local contests and questions, from the Department's file read before the refusal; held one-name records (the ruling of 2026-11-13 00:26)

*Added 2026-11-13 at 00:51 UTC.* Nothing was requested from Virginia's Department of Elections (refused 2026-11-07 18:27:48; the orchestrator, 18:30: what was read before stands). One page was read from another agency: the Constitution of Virginia, article VII, section 4, at law.lis.virginia.gov (the General Assembly's site), 2026-11-13 00:37:39 UTC. Moves: `moves-held-one-name.json` (the ruling, against 6da2062) and `moves-va-2023-local.json` (Virginia, against 01933f2).

**Held one-name records** (the orchestrator, 2026-11-13 00:26 UTC: "A one-name record whose counts are held is not computed, at every level, with the reason that the write-in test cannot be read on held counts"; its reason: p 0 says no other name can win, and the write-in rule exists because a strong write-in can, so the test needs whole counts).
- Built in every builder of mine where held counts meet one name on the ballot (`local.HELD_ONE_NAME`): MEDSL's local records (`local_medsl`, which kept p 0 before), and the legislatures, Klarner's (`local.structure`), MEDSL's 2024, New Jersey's and Virginia's (not computed before; their reason now adds the words). The reason reads: the held reason, then "one name on the ballot for each seat, but the write-in test (whether write-ins drew 10% of the last winner's votes) cannot be read on held counts, so p 0 is not given".
- **p no longer computed: 23 local records**: Washington 2022, 13, and Wyoming 2022, 3 (both held whole, section 17); Monroe County, New York, 2024, 7 (section 32). Section 32 said 127 such records stood before its step; that was wrong, and is corrected there: 16 [measured at this rebuild].
- **Reasons changed: 61 legislative records** (45 House, 16 Senate), already not computed: Idaho 1984-1990's coarse tier (29), the district checks of 2016-2022 and New Hampshire's doubled 2022 counts (29), New York's Assembly 134 and 139 of 2024, and Virginia's 9th Senate district of 2023.
- No other p moved: a p of 0 is in no pool.

**Virginia's 2023 local contests and questions** (`pipeline/local_va.py`; `data/local/2023/VA.json`, `data/measure/2023/VA.json`; `data/local/check-va-local.json`). Section 28's note said the same file holds them, "with nothing requested".
- *What is read* [measured: the cached Media Export, read 2026-11-07 18:23]: 1,448 contests. 43 are on more than one locality's ballot and on the statewide list, which the page shows with its "Winner" marks: clerks, Commonwealth's attorneys and sheriffs a county shares with a city, James City County's and Williamsburg's treasurer, and the towns of Brodnax, Scottsville and St. Paul. 1,405 are on one locality's list alone: 1,396 for offices (374 boards of supervisors' seats, 363 school boards', 92 commissioners of the revenue, 92 treasurers, 85 sheriffs, 83 clerks, 82 Commonwealth's attorneys, 111 soil and water conservation directors, and town councils and mayors) and 9 questions.
- *Titles*: the office is the title's text before its bracket; the bracket is the district ("Cloyd District", "District 1") or the town ("Town of Windsor"), unless it names the contest's own localities. Special where the title says so (37). Seats: the file's voteFor [stated].
- *Localities*: each one's FIPS code from MEDSL's 2024 Virginia precinct file, matched by name; all 133 equal the state's 51 and the Department's own code [measured].
- *No party*: the file's party is empty for every local option, and the page prints none [measured]. So no party is shown, and route (b)'s and (c)'s class reads "party not given in the source" (`local_medsl.PARTY_NOT_GIVEN`), never "nonpartisan", which is a source's word for a ballot. No earlier year's like race is of that class, so these contests are not computed until a ruling pools them, and they enter no other year's pool [my reading].
- *Write-ins*: "Write-In" is the write-in line. An option the file keys by a name ("TakeraN.Walker-3-") rather than "cs" and a number is read as a write-in candidate counted by name: the page shows two such options (Brodnax's and Scottsville's councils), each beside an "Adjudicated Write-Ins" line of the same votes [inferred from those two; 65 contests hold such an option]. None is in the legislature's contests [measured].
- *Winners*: the page's mark for the 43; for the 1,405 the leading candidates for the seats [inferred], with a note (the 18:32 ruling: a figure resting on a rule must look different from one resting on a page).

**The gate within the certifying source** [proposed; it extends the legislature's gate, ruled at 18:49]:
- (a) The year as for the legislature (the page headed "OFFICIAL RESULTS", linked by the Department's Election Results Directory, its Media Export the file read); a contest the page shows: its figures the file's.
- (b) A shared contest's locality lines add up to its statewide count, naming no option it lacks. A one-locality contest's count is its locality's line.
- (c) All reporting: as many locality lines as the page prints; for one locality's, its precincts all reporting and its locality's every group "Fully Reported".
- (d) The over-ballot test within the locality, read as the 17:44 test for statewide contests (21:55: every count shown is tested): the file gives no ballots cast, so a contest's votes for each seat, against the highest-vote contest of the locality's whole ballot (each chamber's lines there summed, and each other one-seat contest or question put to the whole locality). Held above 1.1, listed between 1.0 and 1.1.
- Beside it, as for the legislature: precinct lines against locality lines (17 contests short: Culpeper County 15, Orange and Accomack 1 each), noted on the record.
- **Held: 5.** Brodnax's council (the page shows an "Adjudicated Write-Ins" line the file lacks) and Scottsville's special (the same, and Fluvanna County's line counts 1 vote for John Merritt Unsworth, whom the statewide count lacks); by (d), Halifax County's Sheriff (9,446 votes, 1.11 times the Treasurer's 8,505), Cumberland County's Sheriff (3,252, 1.12 times the Treasurer's 2,906) and the Norton City line of Norton's and Wise County's Clerk (434, 1.10 times the House of Delegates' 394). In those three every figure the test can read is an unopposed contest's.
- **Listed by (d): 28**, each with a note (the highest: Scott County's Treasurer, 1.094; Richmond's casino question, 1.088 times the Senate's lines; Fluvanna's Treasurer, 1.079).

**What the records get** [measured: the build]. Of 1,439 contests for offices: p 0, 774 (one name for each seat); not computed, 665: too few like races, 519 (the class "party not given in the source"); strong write-ins, 103 (60 of them with fewer names on the ballot than seats, or none, as Mecklenburg County's school board districts 4 and 5); special elections, 36; held by the gate, 5; a write-in in the deciding pair, 2. The 9 questions: not computed, Virginia's local thresholds not read.

**Virginia's commissioner of the revenue** is typed "clerk, treasurer or other county officer", not a commission: it is one of the five officers "elected by the qualified voters of each county and city" (Constitution of Virginia, art. VII, sec. 4 [stated]), as Alabama's revenue commissioner and Georgia's tax commissioner are typed. It retypes 92 of 2023's records and MEDSL's two of 2018 (Accomack and Poquoson). The 2018 contest of two candidates moves one like race from one class to the other: 100 records not computed for too few like races see their count move by one (80 of Arkansas 2024's council races 29 to 28). No p moved.

**What moves** [measured; stamps aside]: new records 1,448; typed anew 2; reasons changed 100 (this step) and 61 (the ruling); p no longer computed 23 (the ruling). No p moved anywhere.

**For the orchestrator.**
- The gate above is proposed: (d) is new for local contests; (b) reads nothing for one locality's contests, whose count is one line.
- (d) holds Halifax's and Cumberland's sheriffs and Norton's clerk line at 1.10 to 1.12, where every other contest is unopposed: an unopposed contest loses voters who skip it, so the excess may be real. Built as the 17:44 rule reads; listing them instead is a ruling's.
- 519 contests have no p for want of a party in the source. A ruling could pool "party not given" with like races of the same office type whatever their parties, or leave them.
- The name-keyed options are read as write-ins on the evidence of two contests.
- Virginia's local question thresholds are not read; the Code of Virginia at law.lis.virginia.gov would answer, with one request a section.
- The 2025 file holds 556 more local contests of one locality and 8 shared, already cached; they are not taken in, since the build's odd years are 2023 only and 2025's page as read shows its first 50 contests.

## 34. The district checks' second pass: the matcher fix, Michigan 2022, the states' and a county's results, Rutland; DC 2018's at-large seats; D2's governor totals; Virginia's notes

*Added 2026-11-13 at 04:41 UTC.* The orchestrator's orders of 2026-11-13 00:17, 00:55, 00:56, 01:04, 01:15 and 01:20, on M2's eighth pass. Moves: `moves-district-checks-2.json` (against 510b089, the code alone, whose data are main's at 78a82f2; stamps aside). The records newly tested, and every outcome that changed: `check-districts-new.json`.

**Requests made, one each** [measured: each file's `.meta.json` in the cache].
- Utah's Lieutenant Governor: the 2016 statewide canvass PDF (vote.utah.gov), 01:12:29. It prints no "official" or "certified"; it is headed "2016 General Election Results".
- Indiana's results archive of the 2016 general (enr.indianavoters.in.gov): its settings and the two legislative office files, 01:12 to 01:13. The settings print `Certified` empty.
- Vermont's Secretary of State: one request, which answered 404. No second request (01:15 (3)).
- The Census Bureau: the 2022 State Legislative Block Equivalency Files, `sldu_2022.zip` and `sldl_2022.zip`, 01:11 (the 01:04 ruling (4), one fetch).
- Wayne County's Clerk: one request, at 01:25:44, which gave an empty reply. It is read as a refusal, so nothing more is asked of that office.
- The DC Board of Elections: its certified 2018 general results PDF, 01:31:19 (00:17 (a)).
- Arenac County's Clerk: its official results of the 2022 general, 02:22:25 (01:15 (1)).

**The matcher** (00:56). Three changes, each read against the records it touches.
- A write-in line of Klarner's under the write-in rule's strong line (10% of the last winner's votes) no longer blocks a match; where MEDSL names it, it is still paired (Utah 2016's Senate 19, Seguin, 1 vote; Indiana 2016's House 54, Embry, 29).
- A compound or hyphenated surname matches on its part, the first initial agreeing ("mazzariellohooker" and "CHERYL HOOKER"). Beside a line with the whole surname, a part is taken only where it is the same name on two lines, its surnames among the whole one's, and the larger line is paired. Kentucky 2016's House 41 is the case: Klarner's "Woodson Scott", and MEDSL's "Attica Scott" with 13,257, Klarner's figure, beside "Attica Woodson SCOTT" with 434 on one row named "Cumulative:" [measured]. It was held on the 434 and now passes. A first build took any part beside a whole surname. Vermont 2016 files its whole House as one contest, so a part reached other districts' candidates there, and 101 of its districts could no longer be paired apart. The narrowed rule leaves them as they were: against the run before it, only House 41's outcome changes.
- A MEDSL contest that several of Klarner's districts match goes to the one district whose number it bears, where the others' numbers differ: they matched it by a name alone [my reading]. Hawaii 2016's House 51, unopposed, had matched House 36's contest and was held on it (flag (b), House 36's Marilyn Lee with 3,274). It is now untested, so its p 0 returns. In all, 39 records are now "matched only to another district's contest" (11 in 2016, 11 in 2018, 17 in 2022): 37 were in a shared contest not paired apart before, Hawaii's House 51 was tested, and Texas 2016's House 42 was unmatched (it now finds House 117's contest by a name alone). None is tested.
- **Newly tested: 284** (99 in 2016, 90 in 2018, 95 in 2022). Before, 229 were unmatched, 21 matched several contests and 34 were in a shared contest not paired apart. The 228 the orchestrator's 01:15 names were my first count; the first two changes give 250, and the third adds 34. Each is listed with its outcome in `check-districts-new.json`:
  - 256 pass, with no flag;
  - 16 go to the write-in rule: Vermont's House and Senate districts of 2018 and 2022, where both counts agree and MEDSL names write-ins;
  - 5 are settled by the state: Indiana's House 25, 47 and 54 and Senate 28, and Utah's Senate 19, all of 2016;
  - 3 are kept, MEDSL not covering the district: Kansas 2016's House 80, Maine 2016's Senate 11 and Indiana 2022's House 33;
  - 2 are noted: Massachusetts 2016's First Suffolk and Middlesex Senate district (4.5% off) and Vermont 2022's Lamoille Senate district (flag (b));
  - Vermont 2018's Franklin Senate district is held, and its Rutland district takes MEDSL's counts (below).
- The same file lists the outcomes of records tested before that changed. In 2016, 37 are now settled by the state: 35 of Indiana's (23 held before, 7 kept, 5 noted) and Utah's Senate 20 and 23 (kept). Kentucky's House 41 passes (held before). In 2022, 13 are kept by the Census counties: 12 held before and Michigan's Senate 36, noted before. Michigan's Senate 3 and 10 pass, and its House 99 is settled by the county; all three were held. Michigan's House 10 is held for its new reason. Hawaii 2016's House 51 is no longer tested.
- *M2's list* (`check-districts-m2.json`, rerun): 112 of M2's 249 districts are flagged here too, where 108 were. Of the others, 84 are within 3% here (80 before) and 25 unmatched (32); none now matches several contests (1).
- *Found, not changed.* MEDSL spells one candidate two ways in some districts, a spelling to a county, and the pairing takes the larger line. New York 2016's Senate 58: "Leslie Burke" 35,115 and "Leslie Danks Burke" 17,371 add up to 52,486, against Klarner's 52,488 [measured]. Indiana 2016's House 55: "Cindy Ziemke" 9,487 and "Cindy Meyer Ziemke" 8,896; "Mimi Pruett" 2,681 and "Mary L. (Mimi) Pruett" 3,125. Adding the lines of one name where their precincts are apart would make New York's Senate 58 pass (it is kept, MEDSL not covering it) and leave Indiana's House 55 flagged (settled by the state). No outcome turns on it here; it is proposed for the next step.

**The states' results** (01:15 (2): "Settling a flag needs only the state's own count agreeing with one source"; the notes say "the state's published results agree", never "certified").
- Utah 2016's Senate 19: the canvass gives Froerer 16,381, Christensen 20,994 and Seguin (write-in) 1, Klarner's figures exactly; MEDSL is +10.7%. Klarner's count stands.
- Indiana 2016: the archive agrees with Klarner, candidate by candidate within 3%, in **39 flagged districts**. These are the four the order names (House 25, 47 and 54, Senate 28) and 35 more. The rule's words cover every flag the state's count settles, so all are settled the same way. Of the 35, 23 were held and get p back; 7 were kept and 5 noted, and change only their notes. This is a large reach for one ruling, so it is listed for the orchestrator.
- The canvass also settles Utah 2016's Senate 20 and 23, which were kept; only their notes change.

**Vermont 2018** (01:15 (3)).
- *Franklin* is held under 19:04, as ruled. Its p (1.89e-04) is no longer computed.
- *Rutland*: the facts match. MEDSL's Senate rows for "RUT" are in 31 precincts, every town of Rutland County but Mount Holly, whose Senate rows carry Windsor's district (WDR) [measured]. The governor's rows hold 24,473 ballots in the county's 32 precincts and 23,875 in the district's 31. Klarner's six candidates add up to 103,751 votes, 4.35 a ballot for three seats, so 1.45 times its seats times the ballots. MEDSL's add up to 60,144 (60,206 with its write-ins), 0.84 times. All six pair one to one. So **MEDSL is taken**, marked "Klarner's count is over its seats times the ballots; MEDSL's counts", and p moves ×1.72 (1.73e-04 to 2.98e-04), listed.
- The ballots are read only from statewide contests of one seat: the president, the US Senate, and state offices MEDSL marks STATEWIDE with one seat. A first reading took Vermont's assistant judges, two a county, which MEDSL files with one seat and an empty district, and gave Rutland 31,525 ballots.
- *The rule reaches no other record.* Every other held flag has its ballots figure beside it (`over_seats`), and it stays held. A district's MEDSL precincts are its whole only where its counties are known. Before the 2022 lines, no source read gives them. Indiana 2018's Senate 47 shows the danger: Klarner's count is 1.23 times the US Senate's ballots in MEDSL's 113 precincts, and MEDSL's rows are in five counties. A county missing from the rows would explain that as well as an inflated Klarner count. So MEDSL is taken only in the record the ruling names (`OVER_SEATS_RULED`) [my reading; for the orchestrator].

**Michigan 2022** (01:04).
- *(1) Precinct names.* Before the gate's match, names are normalized: case, spacing and Excel's `_x000D_`. A name in no row of the county's top contest is joined to the one top-contest name with the same jurisdiction code and the same numbers, where their words are the same once words that name no place or unit are left out (THE, OF, CHARTER, PRECINCT and its misspellings, PCT, AND; TWP read as TOWNSHIP; Michigan's ", A MICHIGAN CITY"). Two names one word apart by one letter, both words of six letters or more, are joined too. CITY, VILLAGE, TOWNSHIP and WARD are kept, since a city and a township of one name are two places ("CITY OF MILAN" and "MILAN TOWNSHIP"). Every county of every state is recomputed. The joins are listed in `check-districts.json` (`precinct_equivalences`, by the year of MEDSL's file), 829 in all (89 in MEDSL's 2016 file, 467 in 2018's, 265 in 2022's, 8 in 2024's), 39 of them Wayne's. Wayne's "Charter Township of Brownston" is joined to "Brownstown", as M2 read it.
  - *A first rule was too loose, and was narrowed before this PR* [measured: its list]. It also joined words two letters apart and a name whose words held the other's. So it joined "CITY OF DEARBORN" to "CITY OF DEARBORN HEIGHTS", Detroit's absent voter counting boards ("AVCB 100") to its precincts, "EAST" to "WEST", "PART A" to "PART B", and "LONE ELM CITY" to "LONE ELM TOWNSHIP": 1,930 joins in all, against 829 now.
  - *The top contest, found wrong in #100's coverage and fixed here* [measured]. A contest was read as a question, and so never the top contest, wherever any of its lines bore an answer's name. MEDSL's 2022 Michigan file has "REJECTED" lines in Ottawa County's governor and Secretary of State rows. So in every Michigan county the top contest was a US House seat, and in Wayne it was the 13th district's 518 precincts, not the Secretary of State's 1,089 that M2 read. A contest is now a question only where its answer lines hold most of its votes. The top contest changed in 63 of Michigan's counties in 2022, 14 of Florida's and one of Arizona's in 2016, one of West Virginia's in 2022 and one of Indiana's in 2024.
  - What it moves. Wayne's top contest is now the Secretary of State's 1,088 precincts. With Brownstown's joined, its US House rows miss 21 of them (1.9%), holding 0.3% of its votes, so it is not short; M2 counted 22 (2.02%) holding 2.12%, before the joins. No district check's outcome changes. One gap moves by a precinct: Indiana 2022's Senate 21, in Howard County (13 of 77 precincts missing, where it was 14). Michigan's 2022 Attorney General is now held by the statewide gate, as M2 read it: its rows miss 182 of Wayne's precincts, 5.2% of the state's votes. It was held already, its seat count unread (§31). Its record keeps both reasons: a statewide contest the gate holds now keeps the reason it was held for before. Maine 2018's governor and US Senate gain a statewide-short entry (Aroostook County, 0.1% of the state's votes, noted); neither is one of D3's records. Maine 2024's five questions keep their notes, at 0.08% of the state's votes where they said 0.09%.
- *(2) Nameless party lines.* A line with a party and no name goes to the contest's one candidate of that party, other than a write-in. In 2022 these are in Michigan only. Senate 10 in Wayne: D 23,577 and R 1,228. Senate 3 in Wayne: D 38,498 and OTHER 2,685. Senate 34: OTHER 420 (Midland). With them, Senate 3 adds up to 71,490 and Senate 10 to 89,185, each equal to Klarner's. Both holds go, and p is back, with a note.
- *(3) House 10.* All of MEDSL's lines add up to 41,033 against Klarner's 41,012. Corcoran has 428 on his named line and 12,541 on the WRITE-IN line, against Klarner's 12,948. The count is confirmed, but whether he was on the ballot is not read: the Secretary of State refused, and Wayne's Clerk gave an empty reply. So the record is held, and its reason says so: "whether the candidate was on the ballot is not read". Its p does not return (01:15 (1): "Until a clerk answers, HD10 keeps your reason").
- *(4) A district's counties* are now its MEDSL rows plus the Census's 2022 block equivalency files, for 2022's lines. A listed county with no row of the district counts as missing, and the gap names the share of the district's blocks that lies in it, so that a part can be told from a sliver [measured: block counts; the files give no population]. Senate 35: Midland (17% of its blocks) has no row, so it is not covered, and Klarner's count is kept with a note. **Elsewhere this rule keeps 11 more records that were held**: Indiana's Senate 19, 26, 38, 39, 45, 47, 48 and 49 and House 60, Arkansas's Senate 9, and Michigan's Senate 12 (St. Clair, 10% of its blocks), each with a whole county that MEDSL's 2022 file lacks for the district (5% to 71% of the district's blocks). Michigan's Senate 36 moves from noted to kept. Their p return on Klarner's counts, per 22:26 (b).
- *(5) House 27, Senate 12 and House 99* (01:15 (1)).
  - Senate 12: the gap is in St. Clair County, by (4); it is kept, with no request needed.
  - House 27 lies in Wayne alone, where Howey has 14,624 against Klarner's 20,724. Its clerk did not answer, so it stays held.
  - House 99: MEDSL's lines are in six counties. In Arenac, its 2,160 (filed under Mike Hoadley) are 0.30 of the governor's votes in the same precincts, against 0.95 to 0.98 in the other five [measured], so the gap lies in Arenac. Arenac's Clerk's file is headed "Election Summary Report, General Election, Arenac County, Michigan, November 08, 2022 ... Official". It gives Kenneth A. Kish (DEM) 2,160, Mike Hoadley (REP) 4,847 and 15 unresolved write-ins [stated]. MEDSL files Kish's Arenac figure under Hoadley's name and lacks Hoadley's. With Arenac's figures in place of MEDSL's there, Kish has 13,449 and Hoadley 28,126, Klarner's figures exactly. So Klarner's count stands ("settled by the county"), with a note, and p is back.
- *(6) Wayne's Attorney General rows.* They miss 182 of the county's 1,088 precincts by this step's count (M2's: 187 of 1,094 names, and 2.35 times the Secretary of State's votes in the county), and the contest's rows statewide add up to 1.39 times the governor's votes. They are MEDSL rows not used: the 2022 Attorney General record is held, with no p, by the over-ballot test since section 31 ("seat count unread"), and now by the statewide gate too (above).

**DC 2018's at-large Council** (00:17).
- The Board's certified results (headed "District of Columbia - Board of Elections / November, 6 2018 General Election - Certified Results") give "AT-LARGE MEMBER OF THE COUNCIL": 342,188 votes for its candidates and write-ins, 90 over votes and 120,686 under votes. That is 462,964 in all, twice the Mayor's 231,482 marks and blanks, and 2.0 times the 231,700 "Ballots Cast" [measured]. So each voter had two votes. The page prints no number to vote for.
- The record now has two seats (`seats_note`; `local_medsl.SEATS_READ`), and Bonds and Silverman are marked won.
- It stays not computed. The reason: "two seats, of which the majority party may hold only one (the orchestrator, 2026-11-13 00:17), so it is not a plain race for the top two and no route of the method fits". It is in no pool.
- The over-ballot test reads it per seat: 1.477 times the 231,700 ballots, and 0.738 times its two seats times them. It is listed in `check-over-ballot.json` as a contest of two seats, explained by its seats.
- It leaves the local partisan back-test, where it stood as a race between a Democrat and a Republican. The expected count within 100 votes falls from 51.8 to 51.7, and the deviance after calibration from 16.86 to 16.85. No local p moves by more than 1%.
- *Found, for the orchestrator.* The volume test's part 4 reads a contest's votes plus over and under votes as one precinct's ballots where MEDSL gives one seat, so DC's citywide contests are bounded by the at-large's two votes a ballot (462,964 in `check-volume.json`). DC is one county, and the over-ballot test reads only states of more than one, so no verdict rests on it. A fix: divide by a seat count read (`SEATS_READ`), and read DC's citywide contests in the test.

**D2's governor totals** (22:19 item 5; M2's seventh pass, section 14.1; `pipeline/d2_labels.py`, `data/congress/check-totals.json`).
- Every governor record of 2018-2024 is set beside a second count: MEDSL's precinct file, North Carolina's State Board (2020) or Indiana's results archive (2024). 94 are read; New York 2018 has none, since MEDSL's file is held.
- 13 differ by more than 0.5% and get `result.total_votes_of` and a note naming the other count's names, write-ins and total: Connecticut, New Hampshire, New York, Rhode Island and Wyoming 2018; North Carolina 2020; Alabama, New York and Wyoming 2022; Indiana, Missouri, New Hampshire and West Virginia 2024. Their candidates, `two_party` and p are unchanged: a governor's p rests on the two leaders' votes.
- Maine's 2nd House district of 2024: the Clerk's "Continuing Ballots" (391,596) and "Exhausted Ballots" (11,340) lines are taken out of the candidates (`result.rcv_lines`). `total_votes` is now the two candidates' last-round votes, 391,596, and `two_party` pairs Golden and Theriault (it had paired the "Continuing Ballots" line). Its `ballot.others` counted those two lines; it is now null, with `others_not_read`, since the source prints the last round only. Its p stays not computed, with the reason restated.
- North Carolina 2002's House 118 and North Dakota 2024's governor: nothing to fix, as `check-totals.json` says.

**Virginia** (01:20). The three contests where a name-keyed option outpolls a ballot name now say, in their notes, that the page does not show them, so the option's being a write-in is not confirmed there:
- Charlotte County's Cullen/Red House supervisor (Carwile 304 against Reeves 227);
- Clifton's mayor (Peterson 67 against Hollaway 62);
- Clifton's council (Hess 71).

They stay not computed. The refuting count is not kept as a test. All 65 contests with a name-keyed option now carry a note that it is read as a write-in counted by name [inferred], with the two contests the page confirms it in. The source blocks of `local_va.py` and `local_va_leg.py` now print the full sha256.

**Faults in this step's own runs, fixed before the PR** [measured: each run's output against the one before].
- The Census counties: a first build counted every Census county of a district as missing (a name reused in the code), so Pennsylvania's House 186 and Michigan's House 99 showed whole counties as gaps.
- The ballots behind the over-seats test: Vermont's assistant judges, as above.
- The over-seats rule, first built for every held flag, took MEDSL's counts in Georgia 2016's House 65 and Indiana 2018's Senate 47. It is now Rutland's alone, as above.
- The build twice paired a district's candidates apart from the check, each time over a weak write-in (Indiana 2016's House 54, Utah 2018's Senate 9). The build now pairs exactly the check's pairs, and stops where they differ.
- The part-match in Vermont 2016 and the precinct joins not kept, both above.

**What moves** [measured: against 510b089; stamps aside; `moves-district-checks-2.json`].
- *p moved.*
  - Local: 1,701 records, all within 1% (0.998 to 1.000 of before). The local fits gain or lose a few races: DC 2018's at-large leaves the partisan back-test.
  - State lower chambers: 11,767 records. Of them, 11,683 moved within 1%, 74 between 1% and 10%, and 10 between 10% and 12%, all in Indiana's 2018 House (0.877 to 0.885 of before). Those are districts whose last race was unopposed (class B): they take the chamber's 2016 lean, which moves from −0.081 to −0.107 as Indiana's 2016 districts return to the fit.
  - State upper chambers: 3,271 records. Of them, 3,255 moved within 1% and 15 between 1% and 10%. One moved more: Vermont 2018's Rutland, ×1.72 on MEDSL's counts.
- *New p: 40.*
  - Indiana 2016: 22 House districts and Senate 9, settled by the archive.
  - Kentucky 2016's House 41 (p 0, unopposed).
  - Hawaii 2016's House 51 (p 0), now untested.
  - 2022, by the Census counties: Indiana's Senate 19, 26, 38, 39, 45, 47, 48 and 49 and House 60, Arkansas's Senate 9, and Michigan's Senate 12 and 35.
  - Michigan 2022: Senate 3 and 10 (nameless lines) and House 99 (Arenac).
- *p lost: 1*, Vermont 2018's Franklin (1.89e-04), held.
- *Reasons changed: 3.*
  - DC 2018's at-large: two seats, no route.
  - Michigan 2022's House 10: the ballot not read.
  - Michigan 2022's Attorney General: the statewide gate's reason is added to its earlier one, its seat count unread, and both are kept. The Secretary of State's note gives Wayne's share anew.
- *Notes changed:* 156 records.
  - 65 are Virginia 2023's contests with a name-keyed option. Each now says the option is read as a write-in [inferred], and why; the three above say also that it is not confirmed there.
  - The others are the settled, kept and noted records above.
- *Unchanged:* 347 records' p blocks changed with p the same (`f_half`, `like_races`), and 6 records changed in their forecasts alone.
- *D2:* 13 governors and Maine's 2nd district. No p moved, and they are not in the moves file: `data/congress/check-totals.json` lists them.
- Every record counted above is listed in `moves-district-checks-2.json`, apart from those whose p moved by 1% or less with nothing else, which are counted by level and year.

**For the orchestrator.**
- Indiana 2016: 39 districts are settled by the archive, not four; 23 of them were held.
- The Census counties keep 12 held 2022 records, 9 of them Indiana's.
- The over-seats rule is built for Rutland alone; Indiana 2018's Senate 47 is why.
- House 99 is settled by Arenac's official file. House 27 and House 10 wait on Wayne, which gave no answer.
- DC's volume bound, above.
- Connecticut and New York 2018: the record gives each governor candidate one party's line. Summing every line would move n (Connecticut +1.4%, New York about +3.9%), so p would move.
- Indiana 2024's governor: the state's archive, which says Certified: T, gives Braun 1,566,081 and McCormick 1,183,741, against the record's 1,561,279 and 1,179,967 (−0.3%). Under 15:16 the certified count would win, which moves p.
- (b) the unopposed comparator and (c) the Code of Virginia's offices without party come next, with Virginia's 2025 local contests, as the order of 00:55 set: they are not in this step.

## 35. Governors at the state's count and every party line; the fusion scan; the district checks' third pass (spellings, the settle test by candidate, two counts against one, the over-seats test for every record, zero-row counties); DC's ballots

*Added 2026-11-13 at 06:49 UTC; West Virginia 2012 held at 07:17 UTC.* The orchestrator's orders of 2026-11-13 04:44, 05:15 (on M2's §18), 05:26 (on the fusion scan's count), 05:38 (M2's §18, #108) and 06:52 (on #109 at 6ac10c3). Moves: `moves-governor-counts.json` (D2's files, against b285fbe, whose data are main's at 72d1d60) and `moves-district-checks-3.json` (D3's records, against 0094391, the code alone, whose data are main's). Stamps aside.

**Requests made** [measured: each file's `.meta.json` in the cache].
- Connecticut's Secretary of the State: one request to its Election History, the contest's page (electionhistory.ct.gov/contest/3781, 04:49:53), reached through one index page, the search of 2018's general governor contests (electionhistory.ct.gov/eng/contests/search/year_from:2018/year_to:2018/office_id:3/stage:General, 04:49:27), which names the contest. 06:52: "Index pages followed to reach the one file count as one request. Name them in the log."
- Missouri's Secretary of State: the official returns of 2008, 2012 and 2016, one PDF each, 05:29:14 to 05:29:43 (05:26: "one each to ... Missouri (2008, 2012, 2016)").
- West Virginia's Secretary of State: the statewide results page of the 2012 general, 05:30:03.
- Utah's Lieutenant Governor: one request, the 2008 workbook (vote.utah.gov/wp-content/uploads/2023/09/2008Gen.xls, 05:30:42), reached through two index pages, since its address was not known: vote.utah.gov/historical-election-records-and-documents (05:30:21), which links vote.utah.gov/vote/historical-election-results (05:30:35), which links the workbook (06:52, as for Connecticut).
- None to New York (its State Board refused, 2026-11-07 18:49) or Maine (its Secretary of State refused; 05:26: "Maine 2010: no request").

**The governors** (`pipeline/governor_counts.py`, then D2's refit: `d2_labels.py`, `chambers.py odd`, `backtest`, `compute` and `history`). The record's source for every one of these is Cha, Kuriwaki and Snyder (v4.1) unless it says otherwise.

| Record | The count taken | Its mark | n before → after | p's move |
|---|---|---|---|---|
| Connecticut 2018 | The Secretary of the State's Election History: Lamont 694,510 (Democratic 676,649, Working Families 17,861), Stefanowski 650,138 (Republican 624,750, Independent 25,388), and Whitnum, a write-in, 74 added | the page lists "Statement of Vote 2018" under "Official Sources" | 1,301,398 → 1,344,647 | ×0.968 |
| New York 2018 | Algara and Amlani's county returns, all 62 counties: Cuomo 3,635,340, Molinaro 2,207,602, each over every line | none (the State Board refused); the authors' figures equal Connecticut's lines summed [inferred that they are every line] | 5,350,900 → 5,842,941 | ×0.916 |
| Indiana 2024 | The results archive: Braun 1,566,081, McCormick 1,183,741, Rainwater 129,781 and Stried, a write-in, 52 added | "Certified": "T" in the archive's settings | 2,741,245 → 2,749,821 | ×0.997 |
| West Virginia 2012 | None: held under 19:04 (06:52). The record keeps Cha's count: Tomblin 297,207, Maloney 273,130, Johnson 15,179, Moran 7,934. The page gives 335,468, 303,291, 16,787 and 8,909 | the page's own words deny its heading (below) | 570,336 → 570,336 | p not computed (it was 3.77e-06) |
| Utah 2008 | The Lieutenant Governor's workbook, its Governor sheet's Total row: Huntsman 734,049, Springmeyer 186,503, Schanze 24,820 and Doughton, a write-in, 153 added | none; it stands with Algara and Amlani's, equal to it for both nominees (05:15 (3), two witnesses; 06:52: "the state's count and A&A agree, which settles it under 01:15") | 875,865 → 920,551 | ×0.951 |
| Hawaii 2018 | n at the two leaders' votes less one, as D2's build sets it (the refit of §30 had left it at their sum) | | 376,653 → 376,652 | ×1.000003 |

- Cha's figures were under the state's by 2.6% and 3.9% (Connecticut's two nominees, one line each), 5.8% and 12.7% (New York's), 0.3% (Indiana's), 9.6% to 11.4% (West Virginia's four, against the page held below) and 4.6% to 6.0% (Utah's three) [measured].
- *West Virginia 2012: held* (06:52: "WV 2012: hold it; do not take the page's count. The page says itself that its results "should not be relied on as official results until certified", and it reports 1,846 of 1,892 precincts. So its heading is not the 15:16 mark: the agency's own words deny it. Algara and Amlani equal that page exactly, so they are a copy of it, not a second witness. That leaves the record against one partial, unofficial count, about 12% apart. That gap is unsettled and 5% or more, so 19:04 holds it.").
  - The page also says "Results do not include write-in candidate information" [stated]. It is over the record by 10.6% to 12.9% for every candidate (Cha's under it by 9.6% to 11.4%) [measured].
  - The record keeps Cha, Kuriwaki and Snyder's count and its source; its p is not computed, with the hold as the reason, and its note gives the page's figures, its three sentences and the hold (`governor_counts.HELD`). It has no forecast of the model's own.
  - It is left out of the fits (`chambers.fit_rows` skips a held count) and is not read as a last governor race (`chambers.last_governor_index`). So West Virginia 2016's last governor race is the 2011 special (Tomblin's, 0.512972 of the two-party vote), where at main it was 2012's on Cha's count (0.5211); its record says why. Its p moves ×0.984 against main.
- *Missouri 2008, 2012 and 2016*: the official returns ("Official Election Returns ... As announced by the Board of State Canvassers", 2008 and 2012; "OFFICIAL RESULTS", 2016) equal the records' two nominees to the vote [measured]. No count moves; each record gains a note. Algara and Amlani's rows are the short count, by 7% for the Democrat and 2% for the Republican. In 2016 the shortfall is exactly Kansas City's own rows in the state's file (Koster 98,336, Greitens 25,284) [measured]; the 2008 and 2012 files give no rows by county. `chambers.AA_INCOMPLETE`'s words, which said the same as an inference, now say it as measured, in the Missouri records that carry them (1980-2004's reason p is not computed, and 2008's missing last race; `governor_counts.mo_text`).
- *Maine 2010: not held* (06:52: "no hold. Mitchell is not in the deciding pair, and no p rests on him"). 05:26: "Hold it if either leader's gap is 5% or more and unsettled; Mitchell's 5.5% is." Algara and Amlani give Mitchell 109,087 against the record's 103,387 (+5.5%) and LePage 217,862 against 218,065 (−0.1%), and name no other candidate. The deciding pair is LePage and Cutler: Mitchell ran third. So by the rule's words neither leader's gap is 5% (LePage's is 0.1%, and Cutler has no second count), and the record's p is not computed in any case, since its top two are not a Democrat and a Republican. Maine 2014's last governor race is 2006's, so no p reads 2010's figures. The record gains a note giving both counts. Maine 2018 (−0.6%) keeps its note.
- *What follows through the fits* (`moves-governor-counts.json`, against b285fbe: 1,156 records and 46 file blocks):
  - Each later race whose last governor race is one of these reads the new count: Connecticut and New York 2022 (538's p of record; the model's own beside it ×1.005 to ×1.014) and Utah's 2010 special (×1.002). West Virginia 2016 reads the 2011 special instead (×0.984).
  - Every governor fit, calibration and back-test after them moves a little. 187 governor p of record move, and West Virginia 2012 loses its p; 170 of the 187 are within 1%. Beyond 1% are New York 2018 (×0.916), Utah 2008 (×0.951), Utah 2016 (×0.967), Connecticut 2018 (×0.968) and 13 between ×0.983 and ×1.013: Alabama, Idaho, Oklahoma and Wyoming 2014; North Carolina, Washington and West Virginia 2016; North Dakota 2020; Indiana, Montana, North Dakota, Utah and West Virginia 2024.
  - Leaving West Virginia 2012 out of the fits moves them more than taking the page's count did: in 2014's fit, 399 races where there were 400, and the lean term 0.2893 at main, 0.2890 with the page's count, 0.2917 held [measured].
  - The House's and Senate's p of record move by 0.002% at most, through their near-tie factors, which share the governors' back-test. The factors not of record beside them (the House's by band, the Senate's taken out) move by up to 0.7%.
  - Against #109 as gated (6ac10c3), the hold moves 722 records: West Virginia 2012 loses its p, 78 governor p of record move (59 within 1%; the most, Utah 2016, ×0.964), and no House or Senate p of record moves.

**The fusion scan** (04:44: "scan every record whose source gives one candidate several party lines, at every level (NY and CT first). Send me the count before building beyond the governors"; `pipeline/check_fusion.py`, `data/local/check-fusion.json`). Run again on the refitted records:
- House and Senate (the FEC's tables, summed over every line by the intake and checked against the FEC's printed combined totals): 434 House and 42 Senate records with a candidate on several lines, all summed.
- State legislatures and local contests (MEDSL's lines, `result.candidates[].lines`): 213 lower-chamber, 86 upper-chamber and 353 local records, each candidate's votes the sum of their lines; none fails. Klarner's returns: 6,659 contests with 8,810 candidates on several lines, summed by candidate id in the intake.
- President: the FEC's tables give each nominee's votes over every line.
- Governors: the only one-line counts were Connecticut's and New York's 2018 (fixed above). Set beside Algara and Amlani's county returns, 198 governors of 2006-2020 are compared; six still differ by more than 0.5%: West Virginia 2012 (held, above: the authors' count is the page's, 12.9% and 11.0% over the record's two nominees), Missouri's three (the authors' count is the short one, above) and Maine's 2010 and 2018 (above). Utah 2008 was the seventh before.

**The district checks' third pass** (`pipeline/local_districts.py`, `data/local/check-districts.json`).
- *Spellings* (04:44: "Two spellings of one name: agreed for the next step. Sum the lines where their precincts are apart and the names share a surname and a given name, and list each pair. A name split by county is one candidate's count."). MEDSL's lines of one contest whose names share a surname and a given name or nickname are summed into one candidate's count where no precinct gives both lines votes; a row named as a total is not counted a precinct (`local_districts.merge_spellings`). Each pair is listed in `spellings`, by year, with its lines' votes, precincts and counties, and what was decided:
  - 2016: 97 pairs. 86 are summed (Kansas 36, Indiana 33, Kentucky 6, New York 6, West Virginia 3, Arizona 1, Georgia 1). 9 are not, since a line has votes only on a row named as a total, and 2 are not, since a precinct gives both lines votes.
  - 2018: 5 pairs, all summed (Vermont 4; Indiana 1, House 32's "TONY COOK" 11,330 and "ANTHONY J "TONY" COOK" 6,665).
  - 2022: 5 pairs. One is summed (Vermont). Two are not, since a precinct gives both lines votes, and two are not, since a line is not found in MEDSL's raw file.
  - New York 2016's Senate 58 now passes (Burke 52,486 against Klarner's 52,488), as §34 foresaw. Indiana 2016's House 55 is still off (ratio 0.909) and stays settled by the state.
- *What the spellings move* (against #106's outcomes):
  - 2016: 44 flags now pass. They are 24 kept before (Kansas 17, New York 5, Kentucky 2), 17 settled by the state (Indiana), 2 held (Indiana's House 75 and West Virginia's Senate 5, seat 1, whose p return) and 1 noted (Kentucky's House 36).
  - Kentucky 2016's House 33 goes from held to noted (ratio 0.900 to 1.033), and its p returns.
  - 2018: Indiana's House 32 passes. It was held, and its p returns.
- *The settle test, candidate by candidate* (05:15 (2): "Rerun every settlement candidate by candidate"). A settlement now compares each candidate within 3%, not the totals. #106 made 42 settlements: 39 of Indiana 2016's and Utah 2016's three. Of these, 25 hold candidate by candidate and 17 now pass with no flag (above). None fails. House 38 was the one settled on totals. With Vannatter's second spelling summed it is no longer flagged, and the two-counts rule below applies to it.
- *Indiana 2016's Senate 36* (05:15 (1)) is "settled by the state: MEDSL's count stands".
  - MEDSL gives Gorman 18,384 and Sandlin 26,710 (its two spellings of Sandlin summed). The archive gives 18,375 and 26,696, within 0.1% of MEDSL's. Klarner gives Gorman 23,384.
  - The record takes MEDSL's counts, with a note giving all three counts.
  - n goes from 50,093 to 45,093, Sandlin's share from 53.3% to 59.2%, and p from 5.15e-05 to 5.72e-05 (×1.111).
- *Two counts against one* (05:15 (3)). Six records of Indiana 2016 fall under this rule: Klarner's and MEDSL's counts agree within 0.4% for every candidate, and the archive, which bears no mark, differs by more than 0.4% for at least one. They are listed in `two_against_state`, and each record has `state_differs` and a note giving the archive's figures. Klarner's count stands in each.
  - House 38: the archive gives Vannatter 16,700 and Burns 8,225, against Klarner's 18,623 and 6,303 (MEDSL's 18,624 and 6,303). It keeps its p, and its reason is now this rule.
  - House 39: the archive gives Torr 22,362, against 23,591 (−5.2%). The record gains the note.
  - House 75: the archive gives Bacon 19,765, against 21,146 (−6.5%). The record was held, and no other test holds it, so its p returns (9.59e-06).
  - House 4, 25 and 77 are new to the rule. The archive is under by 0.43% to 1.36% for one candidate: Soliday −0.43%, Fuller −0.49% and Hatfield −1.36%. Before, House 25 was settled by the state within 3%, and House 4 and 77 passed. Each gains the note and nothing else. Taking "differs" as more than 0.4%, the agreement's own line, is my reading.
- *The over-seats test for every record* (05:15 (4)).
  - *The ballots first.* They are summed over the district's own precincts, those with the district's rows in MEDSL's file, not over the county's [measured]. Grand Isle's district is Colchester's two precincts and four of Grand Isle County's five towns (Alburgh's Senate rows are Franklin's), with 9,676 ballots. Windham's is 24 of the county's precincts (Wilmington's rows are Bennington's), with 17,450 ballots.
  - Klarner's counts are still over: 1.437 and 1.424 times their seats times the ballots. MEDSL's are within (0.853 and 0.833), every candidate is paired and no other name is on the ballot. So both are treated as Rutland, and MEDSL's counts are taken.
    - Grand Isle: Mazza is unopposed, with 8,253 votes (Klarner's 13,903), so p is 0. The record was held.
    - Windham: Balint 11,464, White 10,644 and four more, p 1.17e-04. The record was held.
  - *Where it runs.* The test runs on every tested record in a district that MEDSL's file covers and no other district shares: 2,882 in 2016, 4,219 in 2018 and 3,907 in 2022. Over 1.10, it flags four records, all in 2018: Rutland, Grand Isle and Windham (MEDSL taken), and Indiana's Senate 47 (below). No record that passed before is over.
  - *Indiana 2018, found and held* [measured].
    - The figures: Senate 47's count is 1.23 times the US Senate's ballots in MEDSL's 113 precincts of the district, and MEDSL's own count 0.99 times. As first built, the test would have taken MEDSL's counts.
    - What the file lacks: MEDSL's 2018 Indiana file gives Washington County (18175) 63 rows, all of them a "BALLOTS CAST" line (9,541 in its 21 precincts), and no contest's row. Klarner's count is over MEDSL's by 9,363 for the district (Siler 16,064 against 13,276; Houchin 31,853 against 25,278), within Washington's ballots. MEDSL's US House total for Indiana 2018 is 0.7% short of D2's (2,240,431 against 2,256,149; `check-volume.json`).
    - Why the test cannot read it: a county missing from the file is missing from the ballots too, so the test cannot tell a missing county from an inflated count. Before 2022's lines, a district's counties are MEDSL's rows alone, so nothing shows that a district does not take in Washington.
    - The rule: where the file has a county with no contest's votes and no Census list gives the district's counties, the test is not read. This touches Indiana 2018's 101 records (`over_seats.not_read`). Senate 47 stays held under 19:04, as in #106, and nothing else moves [my reading]. 06:52 allows one request to Indiana's 2018 archive, for the next PR.
- *Zero-row counties* (05:38 (1): "a county whose rows are all zero is missing, not covered"). Such a county is a gap of the district's coverage (`zero`), with the share of the district's blocks where the Census gives it.
  - Indiana 2022: House 23 (Cass, 56% of its blocks) and House 66 (Scott, 24%) are now "kept: MEDSL does not cover the district", where both were held. Their p return on Klarner's counts: House 23 is Manning's, unopposed, so p is 0; House 66 is 2.51e-05.
  - Six records kept before now name the zero county too: House 38 (Cass, 6%), 45 (Daviess, 7%), 63 (Daviess, 43%) and 69 (Scott, 14%), and Senate 39 (Daviess, 22%) and 43 (Scott, 17%).
  - Monroe County (18105) is zero in the 2022 file as well. The one flagged record there, House 60, was kept already: Monroe holds 6% of its blocks and has no rows of the district.
  - Kentucky 2016: MEDSL's file has Jefferson County (21111) at 0 votes in every row [measured]. House 28 (MEDSL 349, against Klarner's 16,807) moves from held to kept, and its p returns (2.98e-05).

**DC 2018's ballots** (04:44: "Divide by the seats read and read DC in the test"; 05:38 (2): "Use the Board's figure, with its source named").
- The volume test's part 4 reads a contest whose seats are read (`local_medsl.SEATS_READ`: the at-large Council, two seats) per seat. The precincts' bound for DC's citywide contests is now 231,700, where it was 462,964; the wards' are halved likewise (Ward 1's 61,188 to 30,636).
- The citywide contests take the Board's "Ballots Cast", 231,700, with its source named (`ballots_cast_source`), the precincts' bound beside it (`ballots_cast_rows`). The two agree to the vote [measured]. No verdict moves: DC is one county, and the over-ballot test reads only states of more than one.

**Moves** (`moves-district-checks-3.json`, against 0094391: 15,669 rows).
- 14,525 p move. Of these, 14,323 move by under 0.1% and 188 by under 1%.
- 13 move by 1% to 2.4%: Indiana's 2018 Senate districts (9) and 2020 House districts (3), which follow their chamber's 2016 lean (×0.976 to ×1.019), and West Virginia 2018's Senate 4, seat 2 (×1.019).
- One moves by more: Indiana 2016's Senate 36 (×1.111).
- 9 records gain a p:
  - Indiana 2016's House 75;
  - Kentucky 2016's House 28 and 33;
  - West Virginia 2016's Senate 5, seat 1;
  - Indiana 2018's House 32;
  - Vermont 2018's Grand Isle and Windham;
  - Indiana 2022's House 23 and 66.
- No record loses its p.
- Two held records' reasons change: New York 2018's Comptroller and Attorney General. Their reason now gives MEDSL's precincts as 84.53% of the record's count for governor, which is each nominee's every line; it said 95.97% of the one-line count before.
- 71 records' notes change: the spellings', two counts', zero counties' and over-seats notes. 1,070 records change only in their p block.

**For the orchestrator.**
1. *Answered at 06:52 and done here*: West Virginia 2012 held (above); Utah 2008 and Missouri stand; Maine 2010 not held; index pages count as one request, named above; Senate 36 on MEDSL's count; "differs" as more than 0.4%; Grand Isle, Windham and Rutland on MEDSL's counts; the zero counties; the spellings; DC.
2. *Next*, in their own PR: (b), the unopposed comparator; (c), the Code of Virginia's offices put on the ballot without party; Virginia 2025's local contests (the order of 00:55; 04:44: "(b) and (c) with 2025 local stand as ordered"); and one request to Indiana's 2018 results archive for Senate 47 and Washington County (06:52: "IN 2018 SD47: one request to Indiana's 2018 archive is allowed. The agency has answered before and has refused nothing. Put it in your next PR with (b), (c) and VA 2025 local."). Senate 47 stays held until then.

## 36. The unopposed comparator; nonpartisan offices by the Code of Virginia; Virginia's 2025 local contests; Indiana 2018's Senate from the state's archive

*Added 2026-11-13 at 09:25 UTC.* The orchestrator's orders of 2026-11-13 00:55 ((a), (b), (c) and (e)), 06:52 (Indiana's archive), 07:38, 07:48 (the corrected (c)) and 08:07 (the chairman; the refusals). Moves: `moves-36.json` (every file, against 89a951e, the code alone, whose data are main's at b35fede). Stamps aside.

**Requests made** [measured: each file's `.meta.json` in the cache].
- Indiana's Election Division, its 2018 general's results archive (06:52: "one request to Indiana's 2018 archive is allowed"; "Index pages followed to reach the one file count as one request. Name them in the log."): the archive's settings (`settings.json`, 07:37:47) and its list of statewide offices (`statewideElectionsC_A.json`, 07:38:04), the index pages, then the State Senator file (`OffCatC_2180_A.json`, 07:38:24), at enr.indianavoters.in.gov/archive/2018General/data/. The House file was not read.
- The Code of Virginia at law.lis.virginia.gov (the General Assembly's site): section 24.2-613 (07:42:41), then the two the orchestrator allowed at 07:48, each by its article's page, which prints the article's sections whole (08:07: "The two law.lis article pages count as one request each"): Title 22.1, chapter 5, article 7, Elected School Boards (07:50:46), and Title 10.1, chapter 5, article 3, Soil and Water Conservation Districts' directors (07:50:58).
- **Refused, and nothing from them used** (08:07: "Log all three in §36's request list as refusals of those hosts, and use nothing from them"): looking for which sections to read after 07:48, outside that allowance, which named law.lis alone, one request each to Ballotpedia (07:49:37, an answer of 202 with no content), FindLaw's copy of section 22.1-57.3 (07:50:08, 403) and vacode.org's (07:50:25, 403). None was retried. The rule from 08:07: to find a section, law.lis's own search, or ask first.

**(b) The unopposed comparator** (00:55 (b): "A refinement at every level. An unopposed comparator undercounts ballots by roll-off, often 10 to 30%. Against one, list up to 1.5 and hold only above 1.5; a two-seat race filed as one still reads near 2.0 and is caught.").
- A comparator is unopposed where no more names are on its ballot than its seats (write-in lines aside). Each test takes the single highest figure it reads, as before, and that figure's own line: 1.1 against an opposed one, 1.5 against an unopposed one. A chamber's lines summed over a locality are read as unopposed if any of its districts there is [my reading].
- *Virginia's local contests* (`local_va`, the over-ballot test within the locality): 2023: three contests held before are listed now, each note naming its unopposed comparator: Halifax County's Sheriff (9,446 votes, 1.11 times the 8,505 of its Treasurer), Cumberland County's Sheriff (3,252, 1.12 times its Treasurer's 2,906) and the Norton City line of Norton's and Wise County's Clerk (434, 1.10 times the House of Delegates' 394). Held by the gate: 5 to 2 (Brodnax's and Scottsville's, for the page's "Adjudicated Write-Ins" lines); listed: 28 to 31. The three keep no p: each is of the class "party not given in the source", with too few like races (0). 2025: no contest is over 1.0 [measured].
- *MEDSL's local contests* (`local_medsl.over_ballot`, against the highest statewide contest of the county): no verdict moves in 2018, 2022 or 2024: no top contest the test reads is unopposed (`top_unopposed` false in all 444 rows) [measured]. No US Senate contest of 2018, 2022 or 2024 has one name [measured], so a federal line is never unopposed.
- *The over-seats test of the legislatures* (`local_districts`, a district's votes against its seats times the ballots of its statewide contests): a district's ballots are read as unopposed where every statewide contest it sums has one name. 2018's ten unopposed statewide contests (Alabama's agriculture commissioner and treasurer, Idaho's controller and treasurer, Minnesota's chief justice, Nebraska's attorney general and treasurer, South Carolina's comptroller and superintendent, Wyoming's superintendent) each share a ballot with a governor's contest of more than one name [measured], so no district's ballots are those of unopposed contests alone (`over_seats.by_unopposed` false for every figure), and no verdict moves [measured].

**(c) Nonpartisan offices by the Code of Virginia** (00:55 (c); corrected at 07:48: "a contest is nonpartisan only where the Code says parties may not nominate for that office. Being unlabeled on the ballot is not enough.").
- *Why the source prints no party*: section 24.2-613 B (Form of ballot): "For elections for federal, statewide, and General Assembly offices only, each candidate who has been nominated by a political party or in a primary election shall be identified by the name of his political party." [stated]. As first built (00:55's words read as written), every local office was nonpartisan, which reached all 519 contests of the class "party not given in the source"; 07:48 narrowed it, and that build is switched off.
- *School boards: nonpartisan.* Section 22.1-57.3 E (Election of school board members): "In order to have their names placed on the ballot, all candidates shall be nominated only by petition as provided by general law pursuant to § 24.2-506." [stated]. "Only by petition" leaves no party nomination (08:07: "bars party nomination, so school boards are nonpartisan and pooled as such"). A school board's contest is classed nonpartisan and pooled with the nonpartisan like races of its office and seats; the record quotes the section, its address, the read's time and the page's sha256.
- *The chairman of the school board* (08:07: "goes with the school boards. § 22.1-57.3:3 B makes the chairman the at-large member elected under § 22.1-57.3, so subsection E's petition-only rule reaches it"): section 22.1-57.3:3 B, on the same page: "The member of the school board who is elected at large at the initial or any subsequent election shall be the chairman of the school board during his term of office" [stated]. Its subsection A confines the section to counties with the county executive form that border an urban county executive county; Prince William (2023's chairman) is one, and Page (2025's) is not [inferred]. Page's chairman is read as a member of its elected school board, elected under section 22.1-57.3, so subsection E reaches it all the same [inferred; for the orchestrator]. Both are classed with the school boards, with a note saying so.
- *Soil and water conservation directors: party not given.* Section 10.1-523 A (Nominating petitions): petitions "shall be filed with the general registrar ... to nominate candidates for elected directors of such districts" [stated]. It names petitions as the way to nominate but not the only way and says nothing of parties, so it is not read as a bar (08:07: "§ 10.1-523 A bars nothing"). 2023's 111 directors' contests stay "party not given in the source".
- *Every other local office* stays "party not given in the source", and its reason now names section 24.2-613 B as why the source prints no party.
- *What it reaches*: 
  - 2023 [measured: the build]: 388 of the 1,448 contests are school boards, the chairman's among them. 163 of them were among the 519 not computed for the class "party not given in the source". 158 now get p by the nonpartisan classes of their candidates (130 of 2 candidates, 26 of 3, 2 of 4 or more), from 2.2 in 100,000 to 1.0 in 100 (median 1.2 in 1,000); 5 elect several at once and still have too few like races (55 and 76). The other 225 keep their p or their reason (188 p 0; 33 strong write-ins, 3 special, 1 a write-in in the deciding pair) and gain the note.
  - The 364 contests of other offices not computed for too few like races (0), (b)'s three among them, now name section 24.2-613 B in their reason.
  - 2024: 2023's school boards join the like races of 2024's nonpartisan school boards: 2 candidates, 588 to 719 like races (70 to 77 in the window); 3 candidates, 179 to 205 (31 to 33); 4 or more, 156 to 158 (36 to 38). So 756 school board p of 2024 move: ×0.900 to ×0.924 (540 of 2 candidates), ×0.930 to ×0.950 (124 of 3) and ×1.021 to ×1.042 (92 of 4 or more). 207 school boards of 2024 that elect several at once count 2 or 3 more like races (55 to 58, 76 to 78), still too few.
  - The class back-test of 2023 reads 176 contests where it read 18: the 158 school boards see 11 in the window against 20.4 expected. The near-tie calibration stays out (`calibration-local.json`: the robustness test still fails, a cell made worse with any year left out, 2025 too).

**(e) Virginia's 2025 local contests** (00:55 (e): "Yes: 2025's 564 local contests from the cache, same gate and rulings, own PR. Scope is every level, and 2025's legislatures are in."; `pipeline/local_va.py`, `data/local/2025/VA.json`, `data/measure/2025/VA.json`, `data/local/check-va-local.json`).
- *What is read* [measured: the cached Media Export of the 2025 general, read 2026-11-07 18:24]: 567 contests beside the legislature's: the Governor (D2's, not taken here), the Lieutenant Governor and the Attorney General (on every locality's ballot, with their parties), 8 more contests on more than one locality's ballot (shared), and 556 on one locality's list alone: 549 for offices and 7 questions. 566 are taken in.
- *The gate*, as 2023's and the legislature's of 2025 (its year: the page headed "OFFICIAL RESULTS", its Governor equal to D2's): (b) a shared contest's locality lines add up to its statewide count; (c) all reporting; (d) the over-ballot test within the locality, with (b) above. The 2025 page as read shows its first 50 contests, among them the Lieutenant Governor and the Attorney General, whose figures equal the file's [measured], and none of the 8 other shared contests; so for a shared contest it does not show, all reporting is read from its locality lines (their precincts all reporting, each "Fully Reported"), and its winners are the leaders, with a note (no "Winner" mark seen).
- **Held: 0. Listed: 0.** All 566 pass the gate and the over-ballot test [measured].
- *Write-ins*: 25 contests hold a name-keyed option, read as a write-in counted by name, as in 2023; in none does it outpoll a name on the ballot for a seat.
- *Classes*: school boards nonpartisan under (c): 179 (the chairman's among them); "party not given in the source": 378; the Lieutenant Governor and Attorney General: a Democrat against a Republican.
- *What the records get* [measured: the build]: 559 contests for offices and 7 questions.
  - p 0: 283 (one name for each seat).
  - p by like races: 127. 61 school boards by the nonpartisan classes (52 of 2 candidates, 9 of 3) and 4 that elect several at once (the class "one major party or none" of their seats, 00:55 (c)'s multi-seat reading); and 62 councils and boards of the class "party not given in the source, 2 candidates", whose like races are 2023's Virginia contests of that class (173, 11 in the window), from 6.3 in 100,000 to 5.0 in 1,000.
  - Not computed: too few like races, 71; strong write-ins, 39; special elections, 37; a Democrat against a Republican, 2 (the Lieutenant Governor and the Attorney General, below).
  - The 7 questions: not computed, Virginia's local thresholds not read.
  - The class back-test of 2025: 127 contests, 8 in the window against 11.0 expected.
- 2025 joins the odd years (`local_medsl.ODD_YEARS`), so it is forecast from every earlier year and feeds no year (none is later). The odd-year note on a race between a Democrat and a Republican now names its year's such races: 2023's are Louisiana's alone (Virginia's local offices print no party; its words had said "local races", which Virginia's 2023 local contests made untrue), 2025's are the Lieutenant Governor and Attorney General alone, too few for the year's own back-test [inferred], so their p is not computed.

**Indiana 2018's Senate from the state's archive** (06:52).
- The archive's settings print `"Certified":"T"` [stated], the mark 15:16 asks for, as for Indiana 2024's governor in §35.
- Senate 47: Houchin 31,853 and Siler 16,064, equal to Klarner's to the vote [measured]. Klarner's count stands as the certified count (15:16), and the record moves from held to settled by the state; its p returns, 3.35 in 100,000. Senate 29 and 31, "kept: MEDSL does not cover the district" before, are settled the same way (Ford 31,974 and Delph 24,403; Merritt 30,221 and Camp 28,612, each equal to Klarner's); their p do not move, and their notes now give the archive's figures. Senate 31 pairs only once the archive's "James W. Merritt, Jr" is read as a first-name-first name with its suffix: the name readers take a comma for "LAST, FIRST", so the suffix's comma is dropped (`local_districts._first_last`; the one other such name in the 2016 archive, Rudy M. Howard, Jr., is in no flagged district).
- The over-seats test is not read in Indiana 2018 (§35: MEDSL's file has no contest's row in Washington County). The archive is read for every flagged Senate district of 2018: all 25 districts of the file equal the records' counts to the vote, candidate by candidate [measured]. The House flags of 2018 (100 and 13 held, 58 and 68 noted, 73 and 75 kept) are not read: the House file would be a second request.

**What moves** (`moves-36.json`, against 89a951e; stamps aside) [measured].
- New records: 559 local and 7 questions (Virginia 2025).
- New p: 158 (Virginia 2023's school boards) and Indiana 2018's Senate 47.
- p moved:
  - Local: 756 school boards of 2024 (above); and 1,067 races of 2020 and 2024 between a Democrat and a Republican by the transferred route (a), within 0.002%, since Indiana 2018's Senate 47 rejoins route (a)'s fit.
  - Legislatures: 7,874 p of 2019 to 2025 within 0.15%, through the same fit. Indiana 2020's 16 Senate races move most, ×0.969 to ×0.998: their chamber's lean, the mean Democratic share of Indiana 2018's contested Senate races, takes in Senate 47 again (Senate 9: −0.0699 to −0.0749).
- Reasons changed: 364 Virginia 2023 contests (§ 24.2-613 B named; (b)'s three from held to too few like races); 207 school boards of 2024 (their like-race counts); and Louisiana 2023's 17 races between a Democrat and a Republican, whose odd-year note now reads "local races between a Democrat and a Republican ... Louisiana's alone (Virginia's local offices print no party)", where it said "local races ... Louisiana's alone", which Virginia's 2023 local contests made untrue.
- Notes changed: Virginia 2023's 388 school boards (the Code's section quoted); 10 Virginia 2023 records listed by the over-ballot test against an unopposed comparator, whose note now names it and the 1.5 line (Halifax's, Cumberland's and Norton's among them); and Indiana 2018's Senate 29, 31 and 47.
- Gates: 690 Virginia 2023 local records and 9 questions (`gate.ruled` now 00:55 (a) and (b)).
- No governor, House, Senate or president record moves.

**For the orchestrator.**
- 62 councils and boards of 2025 get p from like races of the class "party not given in the source", all 173 of them Virginia's own 2023 contests. That is the class as built (§33: "like races only of each other"), but it is the first year it gives p. If "party not given" should give no p until it is pooled otherwise, that is a ruling; it would take those 62 back to not computed.
- Page County's chairman (2025) is classed with the school boards by subsection E, as a member of the elected board [inferred]; section 22.1-57.3:3, which 08:07 named, reaches Prince William's (2023), not Page's.
- Indiana 2018's House flags are not read (one more request to the same archive would read them).

## 37. Indiana 2018's House from the state's archive

*Added 2026-11-13 at 09:55 UTC.* The orchestrator's ruling of 2026-11-13 09:21 on §36's third item: "Indiana 2018's House flags: one request to the archive's 2018 House file is allowed, as for the Senate." Moves: `moves-37.json` (every file, against 802327a, the code alone, whose data are main's at 11c852d). Stamps aside.

**Request made** [measured: its `.meta.json` in the cache]: the archive's State Representative file (`OffCatC_2201_A.json`, office category 2201 in the cached `statewideElectionsC_A.json`), enr.indianavoters.in.gov/archive/2018General/data/, 2026-11-13 09:21:33 UTC, HTTP 200, 295,605 bytes, sha256 d637b3a7…a9a1682. No index page was read again.

**What it holds** [measured]: 100 districts, each candidate's total and none a write-in. Every district's ballot counts equal the records' (Klarner's) to the vote, as the Senate's 25 do (§36). The archive's settings print "Certified":"T" [stated], so it is the certified count (15:16).

**The six House flags of 2018**, each now "settled by the state: Klarner's count stands", the state's figures in its note and in `check-districts.json` (`state_count`, naming the House file):

| District | Before | Klarner (= the archive) | MEDSL | p before → after |
|---|---|---|---|---|
| 100 | held (+15.8%) | Forestal 14,070, unopposed | 16,296 | not computed → 0 (one name on the ballot; the write-in test now reads whole counts: no write-in) |
| 13 | held (−5.7%) | Negele 15,270, Barnes 6,494 | 20,524 | not computed → 1.54 in 100,000 |
| 58 | noted (−3.2%) | Burton 13,784, Reinert 7,981 | 21,072 | 2.53 in 100,000, unchanged |
| 68 | noted (+3.6%) | Lyness 17,841, Gaustad 4,834 | 23,499 | 4.46 in 1,000,000, unchanged |
| 73 | kept: MEDSL does not cover the district | Davisson 17,824, unopposed | 10,044 | 0, unchanged |
| 75 | kept: MEDSL does not cover the district | Bacon 16,118, Hurley 10,236 | 19,142 | 1.35 in 100,000, unchanged |

So no Indiana 2018 legislative flag stands open: of 2018's flags, held 17 to 15, noted 6 to 4, kept 7 to 5, settled by the state 3 to 9.

**What moves** (`moves-37.json`) [measured]:
- New p: House 100 (0) and House 13. Notes changed: the six.
- House 13 and 100 rejoin route (a)'s fit, as a held count is left out of every input (07:38) and a settled one is not. So 6,293 legislative p of 2019 to 2025 move within 0.1%, but for Indiana 2020's House: 41 of its p move by ×0.991 to ×1.0054, through the chamber's lean (the mean Democratic share of Indiana 2018's contested House races), which takes in House 13 again. 522 local p by the transferred route (a) move within 0.001%.
- No governor, House, Senate or president record moves.

## 38. The recount zone beside p (brief step 4)

*Added 2026-11-13 at 10:20 UTC.* The brief, step 4: "The recount zone in small races: check where the zone a recount can swing comes near the forecast's spread in votes, and report where p would change (model §3, the drivers table; §10)." The orchestrator's orders: 09:23 ("take your proposal 1, the recount zone ... Find candidate sources for recount shifts by search, and put them to me before you read any"), 09:58 ("Read two, one request each, and quote their figures with page or table ... Read each licence on the same request and say what it allows. The zone sits beside p: a listing and a note, not a change to p, unless the model's §3 says otherwise. Quote §3's words if it does. Build it in its own PR and list every race the zone comes near"), and the rulings of 10:06 and 10:12, quoted where they apply below. Script: `pipeline/local_recount.py` (`build` writes, `check` recomputes and writes nothing). Listing: `data/local/recount-zone.json`.

**Model §3's words** (the drivers table, "Recounts and counting error"): "leave p unchanged ... when the zone a recount can swing (hundreds to a few thousand votes) is much narrower than the forecast's spread in votes (tens of thousands in a statewide race). Your ballot shifts the *chance* your side is declared the winner by the same p. At a zone a third the size of the spread, p is still 96% of its value (MATH §5.10) ... In a small local race the two can be closer; the model checks this there when it has the data (§10)". §3 does not say to change p, so p is unchanged everywhere. The orchestrator, 10:12, 1: "p stays unchanged everywhere ... Changing p where the zone comes near would be a change of method, and the zone's rate rests on an [inferred] step."

**Requests made**, one each (09:58), with curl into `$VOTE_CACHE/recount/raw/`, each with its `.meta.json` [measured]:
- Ansolabehere and Reeves, *Using Recounts to Measure the Accuracy of Vote Tabulations: Evidence from New Hampshire Elections 1946-2002*, Caltech/MIT Voting Technology Project working paper 11, January 2004: vote.caltech.edu/documents/133/vtp_wp11.pdf, 10:00:04 UTC, HTTP 200, 134,241 bytes, sha256 2b62face…4ac551dcf, a 10-page PDF (its printed pages 1 to 8 are the PDF's 3 to 10). **Licence:** none printed [measured: no licence, copyright or rights line in its text]. So nothing is granted beyond quotation: its figures are quoted with page and table, and the file is not kept in the repository.
- Otis and Huang, *An analysis of statewide election recounts, 2000-2023*, FairVote, 28 October 2024: fairvote.org/report/election-recounts-2024/, 10:00:09 UTC, HTTP 200, 215,078 bytes, sha256 2b5dbfcf…1c15be7bc. **Licence:** none printed on the page [measured]; three figures quoted, the page not kept.
- Not read (10:06: "No further requests: neither Reeves 2012 nor FairVote's table, since the build needs neither"): Reeves's 2012 article; FairVote's 36-race list, which is an embedded Flourish table (visualisation 15880092) and a Google spreadsheet, not in the page. The page also links a newer report, 2000-2025 (27 October 2026), not read.

**Ansolabehere and Reeves's figures** [stated]. The paper has no table race by race. Its unit is "a reported ballot tabulation of a town or (district) for each candidate running in a race", and its measure is the percent difference between the first count and the recount, weighted by ballots cast (p. 3 to 4):
- p. 3: in New Hampshire's general elections of 1946 to 1962, "108 races had recounts"; "The majority of the recounts (69) occurred in races for state representative"; "Our analysis consists of 415 cases".
- p. 4: hand counts, 1946-1962, "approximately 0.83 percentage point with a 95% confidence interval from 0.61 to 1.05".
- Table 2, p. 5 (2002 general election; N cases, weighted average %, 95% interval, maximum): hand-counted 92, 2.49, (1.44, 3.55), 21.88; hand-counted without Bradford 79, 0.87, (0.69, 1.06), 4.08; machine counted 217, 0.56, (0.42, 0.70), 8.27 (Optech 21, 0.55; Accuvote 196, 0.56). P. 5: "The results for hand-counted paper, excluding Bradford, are nearly identical to the historical average. We take this as the baseline."
- P. 8: "In a US House election with 250,000 votes, the invalidation rate of .005 for scanners amounts to 1250 votes"; "any race decided by less than .5 percent of the vote will have a non-trivial probability of being reversed in a recount."

**FairVote's figures**, as an illustration only (10:06: "quote its three named races as an illustration only; none sets the rate"). FairVote is an advocacy group, so only races it names with state, year and shift are taken (09:58); its averages (551 votes, 0.03%) are left out. Each shift is FairVote's and is not yet checked against the state's own result [stated]: Washington's governor, 2004, 390 votes (Rossi ahead by 261 at first, Gregoire by 129 after, of 2,746,593 votes); Vermont's state auditor, 2006, 239 (the incumbent ahead by 137, Salmon by 102); Minnesota's US Senate, 2008, 440 (Coleman ahead by 215, Franken by 225 at the end). The model's §4 gives Minnesota's recount as 2,170 votes gross and 264 net; FairVote's 440 runs to the end of the contest that followed the recount [inferred from its words "After a months-long legal process"].

**The rate** (10:06): "The zone is 0.87%, the authors' own baseline (hand counts without Bradford, Table 2, p. 5). Show the 95% upper bound, 1.06%, beside it as a check, and list 2.49% (Bradford in) as a sensitivity". Reason: "the authors name 0.87% the baseline and set Bradford apart, and the site states one figure and shows what moves it."

**The one inferred step**, in the orchestrator's words (10:06): "The paper measures a candidate's change within one town, as a share of that candidate's votes, and you apply it to a race's whole count. Changes may add or cancel across towns and candidates, so the zone you build is a gross figure, as §3 treats Minnesota's 2,170." So a race's zone is w = rate × n votes of margin, n the count p is computed at (`p.n`), and MATH §5.10's logistic has scale w [inferred]. The rate is New Hampshire's hand counts; where a race was counted by scanner, the paper's own figure is lower (0.56%).

**Near** (10:12, 2): "a zone at or above a third of the spread, which is where gain falls to about 0.96 of p. It is the same line as the 4% effect, and it is the model's words." The spread in votes is n × sd. For route (a) the sd is the forecast's own (`forecasts[].share.sd`). For the like-race routes (`class`, `boundary`, `runoff`, like past measures) it is the sd of the normal device through which `pipeline/local.py` `_p_like` computes their p, its line `sd = 1.0 / (math.sqrt(2 * math.pi) * f)`, centred at ½ (at the threshold for a measure), with f the record's `p.f_half` (`p.f_t`) (10:12, 4). Since w ÷ (n × sd) = rate ÷ sd, whether a race is near does not depend on its size.

**gain ÷ p** is MATH §5.10's smoothed gain over the sharp p, in its continuous form: the forecast's density of the share, averaged over a logistic of scale rate ÷ 2 in the share, at the point p is taken at. `check` asserts that it reproduces MATH §5.10's table within 0.002 [measured]: 1.000, 1.000, 0.958, 0.759 (§5.10: 0.760), 0.347 at a mean of ½, and 1.000, 1.000, 0.975, 0.830, 0.420 at 0.52 (n = 100,000, sd 0.03, w = 10 to 10,000 votes). In 46 of the races near at 0.87% the zone is under 2 votes, where a count moves in whole votes and the continuous form is a reading [inferred].

**What comes near** [measured], of 107,111 records with p above 0 (every level of D3's):

| Rate | Near | By level and route | gain ÷ p of those near | Raised in the tails (not near, gain ÷ p 1.04 or more) |
|---|---|---|---|---|
| 0.87% (the zone) | 1,045 | state House boundaries 611, local like races 404, state Senate boundaries 30 | 0.909 to 0.947 | 1,838, each p 3.6 × 10⁻⁶ or less |
| 1.06% (the check) | 1,086 | the same, with local like races 445 | 0.875 to 0.957 | 3,729, each p 2.2 × 10⁻⁵ or less |
| 2.49% (the sensitivity) | 15,122 | 11,617 like-race (boundaries 7,429, classes 3,588, runoffs 600) and 3,505 route (a) (state House 2,314, Senate 1,191) | 0.627 to 4.263 | 17,055, each p 6.2 × 10⁻⁴ or less |

- At 0.87% every near race is of two classes, and the zone lowers its p. 641 are state legislative boundaries of the class "general, 4+ seats at once, both major parties running a full slate" (611 House, 30 Senate; f at ½ from 19.75 to 23.75, so a device sd of 0.0168 to 0.0202): New Hampshire 355, West Virginia 101, Wyoming 38, North Carolina 35, North Dakota 24, South Dakota 23, Alaska, Vermont and Virginia 14 each, Montana 8, South Carolina 6, Maine 3, Hawaii, Nevada and New Jersey 2 each, from 1971 to 2024. 404 are local races of the class "local council, commission or board, nonpartisan, 4+ candidates" (f 17.47 to 17.51, sd 0.0228): Kentucky 2020 232, Virginia 2020 51, Oregon 2024 17, Arkansas 2020 12, South Carolina 2020 11, and 81 more in 21 other state-years. Their n runs from 3 to 279,070 (median 5,771).
- Away from ½ the zone raises p, since the forecast's density there rises when it is smoothed. These races are counted, not listed (10:12, 5: "Their p is 3.6e-06 or less, where the choice of tails moves p far more, as §3's table shows"). At 2.49%, a route (a) race in the tails reaches 4.263 times p (New York's 2020 House 55, p 3.5 × 10⁻¹¹).
- The 2.49% floor is 0.627 (Alaska's 1978 House 20, a boundary), not 0.95 (10:12, 6).
- My first count to the orchestrator, before the 10:06 ruling, said no race came near at 0.87% or 1.06%; it covered route (a) alone. I corrected it before the 10:12 ruling.

**What is written** (10:12, 3): "Each of the 1,045 records near at 0.87% gets a note with three parts: the zone in votes, the spread it is set against, and gain/p at 0.87% marked [inferred]. Records near only at 1.06% or 2.49% appear in the listing, not in a note." Each note begins "Recount zone [inferred]:", gives those three parts and the orchestrator's words on the gross figure, and, for a like-race route, quotes the device's line. 156 files change, by one line for each noted record, and nothing else in a record moves [measured: each changed line, with its zone note taken out, equals the line it replaces]. No p moves. `data/local/recount-zone.json` lists every race near at any rate (15,122), with the zone in votes, the zone over the spread, whether it is near, and gain ÷ p at each rate; its `counts` hold the table above, and its `sources` the figures quoted here with their pages.

**Rebuild order.** The note is written by its own step, as `pipeline/governor_counts.py` writes its text. So `python3 pipeline/local_recount.py build` runs after `pipeline/local.py`, `local_medsl.py` and `local_ncsbe.py` build, since each rewrites its records without the note. The step takes out any earlier zone note first, so it can be run again. `check` fails if a record's note or the listing differs from a fresh build, and, with `$VOTE_CACHE`, checks each source's sha256 and that every figure quoted is in it.

**Not done.** Each state's own result for FairVote's three races (not requested). The lattice form of §5.10 for races whose zone is a vote or two. A rate for machine counts (the paper's 0.56% is New Hampshire's scanners of 2002 alone).

## 39. Singer's 2020 official results: 2020's second count of the state legislatures

*Added 2026-11-13 at 10:43 UTC; the flags' outcomes await the orchestrator.* The orchestrator's orders: 09:23 ("proposal 2, Singer 2020. Read only whether its file sits behind a guestbook ... If it does not, take it, under the same gates") and 10:33 ("Yes to Singer 2020 (RV80FW, CC0, no guestbook), under the same gates, with its own intake and PR. You may make the requests that reach its file: the dataset's file list and the file itself, one each. Name them in the log. Ask me before any other"). Reason: MEDSL's 2020 file holds local offices only, so 2020 is the one even year of 2016 to 2022 whose legislatures had no second count (§29's part 2 and §32 could not test it). Script: `pipeline/local_singer.py` (`normalize`, `gate`, `check`). Output: `data/local/check-2020-singer.json`. The build does not read it yet.

**The source** [stated, its Dataverse record]: Stephanie Frank Singer (Portland State University), *US 2020 General Official Election Results in Tabular Format*, Harvard Dataverse doi:10.7910/DVN/RV80FW, v1.0, released 2021-08-27, **CC0 1.0**, no guestbook. Its description: "Official 2020 General Election results for all 56 major US jurisdictions ... by county (or other major subdivision) including all federal contests and most statewide and state legislative contests ... The data in these files comes from, or is rolled up to the county level from, files or web pages published by the State, District or Territory Boards of Election." It is a third party's compilation, so it is a second count, as MEDSL's is, and settles nothing as the certified source (21:03).

**Requests made**, one each (10:33), with curl into `$VOTE_CACHE/singer2020/raw/`, each with its `.meta.json` [measured]:
- The dataset's record and file list: dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/RV80FW, 10:34:42 UTC, HTTP 200, 49,650 bytes. Still v1.0, CC0 1.0, no `guestbookId`, and the same 56 files and md5s as the record cached on 2026-11-07.
- The files themselves: the dataset holds 56 files (one per jurisdiction), so the one request is Dataverse's download of the whole dataset in the files' original format (…/api/access/dataset/:persistentId/?persistentId=doi:10.7910/DVN/RV80FW&format=original), 10:34:47 UTC, HTTP 200, a 1,532,255-byte zip. Every one of its 56 files equals the record's md5 [measured]; 23,671,970 bytes in all.

**How it is read** [measured]. Columns: Election, Contest, Selection, Party, ReportingUnit, VoteType, Count, Preliminary. Every line has a `total` vote type, which is the one used. Reporting units are counties (or the state's other subdivisions); in Maine, Rhode Island, Alaska and the Northern Marianas, 431 lines are the jurisdiction's own and are not the sum of its counties (Maine's UOCAVA ballots, Alaska's FWAB, Rhode Island's federal-only absentee ballots), so they are added. Non-votes ("Over Votes", "Under Votes", "Total Votes Cast", "None Of These Candidates") are left out; write-in totals ("Write-In", "Scattering", "All Others", Oregon's "Misc.") are write-in lines. Names: a suffix after a comma is moved before it ("Fred W. Thiele, Jr."), and Alaska's legislative names, written "Last First M." with no comma, are read with the first word as the surname. Utah's file marks 841 lines "Preliminary", all in its federal contests and governor.

**Gate 1, the federal counts** (the 0.5% line of `local_in.gate` and `local_medsl.quality`): each jurisdiction's Democrat and Republican for president, US Senate and each US House district, by candidate (by surname, else the one line of that party, for a ticket written whole or a name spelt otherwise), against D1's and D2's certified 2020 counts. 927 comparisons. **46 jurisdictions pass** (worst miss 0.27%: Connecticut, New York; Maine at 0 with its central lines added). **Five fail** and are not used: Kansas (president +7.5% and +5.2%; House 2 +32%), Missouri (its "District 7" holds the 6th district's candidates), Ohio (House 14 Republican +2.1%), Utah (−1% to −2.9%, its lines marked preliminary), Wyoming (Senate Democrat −1.4%). The five territories have no certified count here, and Klarner has none of them.

**Gate 2, §32's district checks** (`local_districts.match`, `pair` and `test`, unchanged; Klarner's 2020 general contests as the check reads them). Of Klarner's 2020 general contests, 1,464 are in no state Singer's file covers that passed gate 1 (New Hampshire 228, Massachusetts 200, Missouri 180, Kansas 165, Vermont 117, Ohio 115, New Mexico 112, Idaho 105, Utah 90, Wyoming 75, Delaware 52, Nebraska 25). **3,880 are tested**; 136 match no contest of Singer's (Oklahoma 69, Florida 23, Hawaii 22, 22 in 12 other states: mostly unopposed races, which Singer's file leaves out [inferred]); 15 share a contest with another district and cannot be paired apart; 1 is not paired.

**25 flags**, all (a) (the ratio off 1 by more than 3%); outcomes as §32's rules would give them, held at a gap of 5% or more, noted under it (21:26, 19:04), **not applied**:
- **Montana's House 3, 19 and 84** (held): Klarner's figure for one candidate is exactly 10,000 above Singer's (Powers 12,393 against 2,393; McKamey 14,288 against 4,288; Hull 12,819 against 2,819), the others' equal. These three are Montana's only House districts of 2020 over 9,740 votes in the records (15,050 to 16,075; the median district 5,649) [measured], so a keying error in Klarner is likely [inferred].
- **Maine, 17 districts** (House 111, 112, 114, 119, 120, 121, 122, 136, 137, 138, 144, 145, 148, 149 and 151; Senate 5 and 17; 15 held, 2 noted): Singer's counts are short, from 3% to 93% (House 122: 304 against 4,306; House 149: 352 against 3,672), each candidate's. Maine's federal counts in the same file are whole, so the file likely lacks some towns' rows in these contests [inferred].
- **New York's House 1, 3 and 5** (Suffolk County; 2 held, 1 noted): Singer's counts are 4% to 12% short.
- **Arizona's House 12 and Senate 16** (noted, 3.9% and 3.2%): Singer gives the write-in candidates 0 votes where Klarner gives them 7,577 and 3,124 in all.

**For the orchestrator** (put at 10:42): (a) whether §32's held and noted rules act on this third party's count as on MEDSL's, or only where the evidence is against Klarner (Montana), the short counts kept with a note; (b) one request each, to Montana's and Maine's Secretaries of State, for their 2020 legislative results, to settle the Montana and Maine flags. New York's Board refused before, so its three are not settled by the state.
