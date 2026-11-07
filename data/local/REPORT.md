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
- **School superintendents.** 176 contests, not M2's 167, were typed "school board" and are now "clerk, treasurer or other county officer": an office whose words name a superintendent (SUPERINTENDENT, SUPT or SUPER. OF PUBLIC INSTRUCTION) with SCHOOL, EDUCATION or INSTRUCTION. They are Alabama 61, Montana 47, Florida 30, Arizona 17, Illinois 16, Georgia 2, South Carolina 2 and North Carolina 1; 64 of 2018, 47 of 2020, 2 of 2022, 62 of 2024 and 1 of 2000. Four of them are statewide offices filed in the local files (Georgia's State School Superintendent of 2018 and 2022, South Carolina's State Superintendent of Education of 2018 and 2022), which the twenty-names list leaves out, so that list moves 172. A water superintendent stays a special district. No p becomes computed or uncomputed: the 134 computed keep their p but one, Montana's 2024 Superintendent of Schools in county 30093, which leaves the school boards' own fit and falls by a factor of 2.0 (0.000181 to 0.0000907). 1,720 other p move, as the like races of their class or of the fit's pool change: by a median factor of 1.003, 90% within 1.007, the largest 1.017. 165 uncomputed contests keep their reason with a changed count of like races.
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
| North Carolina, other dates, 2012-2026 | 306 | 15 / 10.9, more | 10 votes: 23 / 21.9, more | **stands**, both tests: p may be low |

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
