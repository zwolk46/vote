# State legislatures, primaries, local races and measures: sources, method and checks

*Worker D3, `briefs/D3-data-local.md`. First written 2026-11-07 05:10 UTC. Marks: [measured] computed here from the files; [stated] as the source says; [inferred] my reading. The inventory of every source found is `data/sources/local.md`.*

**State at this writing.** The state legislatures are taken in (Klarner, 1967-2022) and the model's own forecast for them is built and back-tested. **p is not yet computed in the committed files**: the method goes to the orchestrator first (brief step 3), and the full build is larger than the repository should take without the orchestrator's word (its message of 04:38). The committed files are a sample: New Hampshire, Minnesota and Texas 2022, Montana 1974, and New Hampshire's 2014 primaries.

## 1. Sources taken in by script

| Source | Script | What it gives | Checks [measured] |
|---|---|---|---|
| Carl Klarner, *State Legislative Election Returns, 1967-2022*, Harvard Dataverse doi:10.7910/DVN/FJOGJB, v1.0 (2024-06-12), CC0 1.0 | `pipeline/intake/klarner_state_legislative.py` | 418,894 candidate rows into 189,103 contests: 158,537 regular generals, 27,359 primaries (first rounds and runoffs included), and 3,207 others (Louisiana's two rounds, specials, top-two primaries) | rows read = 418,894, as the record says; Democratic and Republican sums against Klarner's own contest file: 15 of 151,769 contests differ, most where the contest file has 0 for a party to which the candidate file gives a few votes, and one by 604 votes (Illinois House 38, 1968); all listed in the cache's `checks.json`; candidates against Klarner's candidate-contest file: 16 of 307,892 differ; winners per chamber and year against Klarner's seats-up file: 7 of 2,512 differ, each by one or two seats (vacancies and ties). Klarner's `ovote` is 0 in 9,061 contests where its candidate file lists non-major candidates with votes, so it is not used as a check |
| National Archives, Electoral College results 1964-2020 | `pipeline/intake/nara_electoral_college.py` (D2's) | the sitting president's party in each year | the winner's electoral votes reach the majority |

Klarner compiles the states' official returns (their websites when collected, and the earlier ICPSR editions) and does not name the origin of each race or say whether a count is before or after a recount, so every result is marked `stated`, with `via` the dataset, and `certified` is left out (null).

**Held back as likely incomplete in the source** [measured]: 10 contests whose count is under 5% (generals) or 2% (primaries) of the median of the chamber's like contests that year, such as Montana House 43 in 1974 (25 votes, against a median of 2,329) and Delaware House 14's 2014 Democratic primary (4 votes). They would otherwise carry the largest p of all. Their p is not computed and they are marked for a second source.

## 2. The model's own forecast, method D3-v1 (proposed; not yet approved)

No forecaster published a forecast for any race at these levels (model §4). Three routes, chosen by what is known before the election (who is on the ballot, the seat's past, incumbency), never by who finished in the first two.

**(a) Partisan**: a single-seat general with one Democrat and one Republican on the ballot. The Democrat's two-party share is

> y = ½ + a_t + b·x + g + e

- **x**, by class: **A** the seat's last result was contested (its Democratic share − ½, incumbency, the chamber's lean); **B** the last result was unopposed (which party, incumbency, lean); **C** no last result on these lines, after redistricting (incumbency, lean). Incumbency is +1, −1 or 0 (Klarner's `inc`). The chamber's lean is the mean Democratic share of the same chamber's contested seats at its previous election, minus ½.
- **a_t**, the year's swing, forecast from the kind of year (presidential, midterm, odd) and the sitting president's party, as D2-v1 does.
- **g**, the state-and-chamber's own swing that year, and **e**, the race's own error, with its sd by class and size.
- Normal with sd = √(s_a² + s_g² + s_e²); a Student-t (4 degrees of freedom, the same sd) beside it. Each year is forecast from a fit on the other years, as D2-v1 (inputs all ex ante; coefficients borrow other cycles).

Fitted on all 90,953 races [measured]:

| Class | races | last result | incumbency | lean | s_e by size (under 3k, 3-10k, 10-30k, 30k+ two-party votes) |
|---|---|---|---|---|---|
| A | 49,001 | 0.752 × (last − ½) | 0.034 | 0.038 | 0.083, 0.074, 0.067, 0.061 |
| B | 14,350 | 0.108 × (±1) | 0.049 | 0.358 | 0.109, 0.101, 0.098, 0.094 |
| C | 27,602 | none | 0.118 | 0.375 | 0.111, 0.105, 0.108, 0.109 |

Swing: the president's party loses 2.4 points of share in a midterm (−0.0242 × the president's party), 1.0 in an odd year, and +0.4 in a presidential year; s_a = 0.027; s_g = 0.027.

**(b) Like past races** (Mulligan & Hunter's route, read through the model's own lay form, model §3): for primaries, nonpartisan races and races without one D and one R, q is the share of the same class's races in other years whose leading two finished between 49% and 51% of their combined vote; then f(½) = 50 q and p = 25 q ÷ n. Classes are by kind and by facts known before the election (the number of candidates and whether an incumbent runs, for primaries). Where fewer than 10 like races fall in the window it widens to 48-52%, then 45-55%; under 100 like races, p is not computed.

**(c) Boundary**: a race that fills k seats at once, decided between the last winner and the first loser (model §7): route (b) applied to that pair, with classes by k and by whether both parties ran full slates. **Marked the model's own and not yet checked** (M2).

## 3. Back-test (`data/local/backtest.json`), each year forecast from the other years [measured]

**Route (a)**, 90,953 races, 1968-2022:

| Two-party votes | races | in 50 / 80 / 95% intervals | 49-51%: expected, seen | within 10 votes | margin 0 or 1 |
|---|---|---|---|---|---|
| under 3,000 | 3,603 | 54 / 83 / 95% | 165, 188 | 45, 37 | 6.8, 8 |
| 3,000-10,000 | 23,682 | 54 / 83 / 95% | 1,068, 1,185 | 92, 103 | 13.8, 11 |
| 10,000-30,000 | 37,406 | 54 / 83 / 95% | 1,617, 1,678 | 49, 55 | 7.4, 8 |
| 30,000 and over | 26,262 | 55 / 83 / 95% | 1,129, 1,123 | 11, 10 | 1.7, 0 |
| **all** | **90,953** | **54 / 83 / 95%** | **3,978, 4,174** | **198, 205** | **29.8, 27** |

Mean log score: normal 1.001, t4 0.994 (the normal is a little better).

**Routes (b) and (c)**, 21,841 races: margin 0 or 1, 29.3 expected and 28 seen; within 10 votes, 202 expected and 210 seen; by class in `backtest.json`.

**Against the record (brief step 5).** Model §4 gives 52 of 109,093 contests (1968-2022) tied or one vote apart. The cache reproduces it exactly: 52 of 109,093 contested generals, 30 of them single-seat and 22 multi-seat [measured]. On the races the routes cover, the forecasts expect 59.1 such margins and 55 happened.

## 4. Where p is not computed (full build, scratch) [measured]

Of 189,103 contests, 112,785 have p (route a 90,949, b 12,023, c 9,813) and 66,716 are unopposed (p = 0, said so). p is not computed for 8,266 runoffs and two-round systems; 816 primaries that nominate several at once; 173 specials; 91 top-two primaries; 121 where the source does not report every candidate's votes; 55 in classes with too few like races; 10 counts held back (§1); and 70 others (68 structures no route covers, 2 election types not handled).

## 5. Size

The full build is **144 MB** uncompressed (state-lower 100.1, state-upper 29.3, primary 14.8) and 19 MB compressed, for 189,103 contests: over the orchestrator's 100 MB line, so it is not committed until the orchestrator says how.
