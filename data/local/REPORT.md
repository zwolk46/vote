# State legislatures, primaries, local races and measures: sources, method and checks

*Worker D3, `briefs/D3-data-local.md`. First written 2026-11-07 05:10 UTC; method and figures brought to D3-v1.1 at 05:50, and the review points of 05:17 fixed at 06:10. Marks: [measured] computed here from the files; [stated] as the source says; [inferred] my reading. The inventory of every source found is `data/sources/local.md`.*

**State at this writing.** Every state legislative contest of 1967-2022 that Klarner's dataset holds is in `data/state-upper/`, `data/state-lower/` and `data/primary/`: 189,103 contests. Each has p, p = 0 with the reason, or the reason p is not computed. The forecast method is D3-v1.1: D3-v1 as proposed, approved by the orchestrator at 05:06 with one change (each year fitted on earlier years only), and with runoffs added at its word. Local races and ballot measures come next, from the precinct sources.

## 1. Sources taken in by script

| Source | Script | What it gives | Checks [measured] |
|---|---|---|---|
| Carl Klarner, *State Legislative Election Returns, 1967-2022*, Harvard Dataverse doi:10.7910/DVN/FJOGJB, v1.0 (2024-06-12), CC0 1.0 | `pipeline/intake/klarner_state_legislative.py` | 418,894 candidate rows into 189,103 contests: 158,537 regular generals, 27,359 primaries (first rounds and runoffs included), and 3,207 others (Louisiana's two rounds, specials, top-two primaries) | rows read: 418,894, as the record says. Democratic and Republican totals against Klarner's own contest file: 15 of 151,769 contests differ. In most, the contest file has 0 for a party to which the candidate file gives a few votes; one differs by 604 votes (Illinois House 38, 1968). All are listed in the cache's `checks.json`. Candidates against Klarner's candidate-contest file: 16 of 307,892 differ. Winners per chamber and year against Klarner's seats-up file: 7 of 2,512 differ, each with one or two winners fewer than the seats up (likely ties or unfilled seats [inferred]). Klarner's `ovote` is 0 in 9,061 contests where its candidate file lists non-major candidates with votes, so it is not used as a check |
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
