# Senate, House and governor: sources, method and checks

Worker D2 (`briefs/D2-data-congress.md`, amended 2026-11-07 03:13, 05:58, 06:36, 07:04, 07:19, 08:06 and 08:36 UTC, and the orchestrator's words of 08:54, 09:03, 09:08, 09:26, 11:16, 12:01, 12:11, 12:35, 12:40 and 13:06). Written 2026-11-07 and revised thirteen times the same day (last at 13:45 UTC):
- for the follow-ups from M2 (§0.9);
- for the orchestrator's third round (§0.8);
- for its fourth, the near-ties (§0.7);
- for its fifth, the means and the tails (§0.6);
- for the incumbency fix after M2's second pass (§0.5);
- for the rest of that pass, with round 5 taken again under the robustness test (§0.4);
- for round 4's near-tie factor taken again under that test, with the governors' near-even note (§0.3);
- for the next round, a half-life k and Cha's incumbency codes 2 and 3, neither adopted (§0.2);
- for the near-even note on the House's and the Senate's p, with the FEC's 2004 file (§0.1);
- for the note's two tests, which take it off the Senate's and the governors' p (§0.1, item 3);
- for the odd-year governors of Kentucky, Louisiana, Mississippi, New Jersey and Virginia (§8);
- for New Jersey's and Virginia's governors of 2025 from the states' own certified results, Kentucky's and Mississippi's 2023 refused, and Rhode Island 2010 (§9);
- and for the check of every governor's incumbency code against the record's last race: five codes fixed, and what moves with them, the House's near-tie scheme included (§10).

It covers every Senate and House race of the even years 2006 to 2024, every governor race of the even years 1978 to 2024 and of the odd years 1977 to 2025, that the sources hold, with p, and control of the Senate and the House.

## 0. What each round changed

### 0.1 The near-even note at every level, the FEC's 2004 file, and the note's two tests (the orchestrator, 2026-11-07 09:26 and 11:16 UTC)

**What was asked.** The orchestrator, 09:26: "Stop the search for a better forecast here. Six variants have now failed the same way, and more searching on the same years would fit noise." It asked for two things, then a stop:
- **The note.** "Write the House's and the Senate's near-even shortfall onto each of their model's own p, built from your back-test with its counts, as for the governors." *Reason:* "the same disclosure at every level, whichever way the forecast leans."
- **FEC 2004.** "FEC 2004 by script, so that House 2006 gets its lagged inputs and its p, if the FEC's 2004 file is reachable and token-light. Otherwise record why and leave it."

**1. The note** (`chambers.near_even_note`, written by `compute`). *Since 11:16 the note stands on the House's p only; the Senate's is taken off (item 3).* Each p of the model's own normal forecast now carries a `note`, whether it stands first or beside 538's. That is the forecast the back-test scores. There are 3,369 such p in the House (2,514 first, 855 beside) and 317 in the Senate (170 first, 147 beside):

> House: this route's back-test shows more near-even finishes than it forecast (105 against 87.5 within 1 point, 2010 to 2024), so p may be low
>
> Senate: this route's back-test shows more near-even finishes than it forecast (17 against 11.1 within 1 point, 2010 to 2024), so p may be low

- **Where the counts come from.** They are the back-test's: 49-51% of the two-party vote, 2010-2024, out of sample, under the forecast of record. The House's count includes its near-tie factor; the Senate has none since §0.3. The sentence turns "more … may be low" into "fewer … may be high" when the count leans the other way.
- **p is not corrected.**
- **538's p carry no note**, since the back-test does not score them. The governors' note (§0.3) stayed on every governor p, from the history by votes, until item 3 took it off.

**2. FEC 2004: the file is taken in; House 2006 is left as it is.**
- **The file is reachable and light.** It is `https://www.fec.gov/documents/1625/2004congresults.xls`, 908,800 bytes. `fec_federal_elections.py 2004` now reads it into the cache. Two changes to the reader were needed, both fixed:
  - its sheet is named in capitals;
  - it prints "Combined Parties:" in the column before the November votes, with no party.

  So it gives 34 Senate and 440 House contests, and each of the 433 printed district totals agrees. Every other year's output is unchanged, byte for byte.
- **Why House 2006 still has no p.** A House row of 2004 needs its lean: the 2000 presidential vote on the lines of 2004, as each row's lean is the last presidential vote before the election on the lines it was held on (§2.2). The Downballot gives the 2000 vote on the 2006-2010 lines only. So it serves 2004 only in the states whose lines did not change from 2004 to 2006, and no source read here states which those are.
  - The FEC's 2006 endnotes state that Texas's districts 15, 21, 23, 25 and 28 were redrawn by court order for 2006.
  - They do not state the others. Georgia's map of 2005 is a known case that no source read here states.
  - Wikipedia's API refused the request ("You are making too many requests to the API"). By the rules that route was stopped, not worked around.
- **What it would take.** A source listing every state whose lines changed between 2004 and 2006, such as the Census Bureau's notes on the 110th Congress's districts. With it, the 2004 rows would enter every later House fit. So every House p of 2008-2024 would move, as well as the 2006 p being computed, and all of it would need to be scored again under the robustness test. It is left for the orchestrator (§7).

**3. The note's two tests (the orchestrator, 11:16).** The orchestrator's ruling of 11:01 UTC, fixed before the numbers were seen: a back-test lean note stands only where two tests of the same back-test lean the same way.
- **(s)** Seen against expected within the note's share line, 1 point of ½ (49-51%).
- **(v)** Seen against expected within k votes. k is the smallest of 1,000, 5,000, 10,000, 20,000 and 50,000 at which 5 or more are expected.
- A test counts only with 5 or more seen or expected.

*Reason* (11:16): "a note that one reading of the record contradicts tells the reader a direction the record doesn't give, and X1's first screen draws these notes as arrows."

**The counts are M2's** (`checks/m2/c16_notes.py`, M2's third pass, on its branch; the orchestrator relayed them at 11:16). The chance is M2's one-sided chance of a count that far off.

| Level, years | (s) seen against expected, within 1 point | (v) k, seen against expected | Leans | The note |
|---|---|---|---|---|
| House, 2010-2024 | 105 against 87.5: more (chance 0.030) | 1,000 votes: 24 against 16.9, more (0.057) | the same way | **stands** |
| Senate, 2010-2024 | 17 against 11.1: more (0.053) | 10,000 votes: 4 against 5.1, fewer (0.42) | opposite ways | **goes** |
| Governors, 2006-2024 | 17 against 15.8: more | 10,000 votes: 6 against 9.7, fewer | opposite ways | **goes** |

- **The governors' own line does not count.** Their note's 5,000-vote line expected under 5 (4.5), so it is not a test under the ruling.
- **This route's own (s) is the same count at every level.** Its back-test gives 105 against 87.47, 17 against 11.10 and 17 against 15.78 (governors, 2006-2024, under the variant of record).
- **(v) is not recomputed here.** This route's back-test does not keep each race's vote total. `history.json` counts by votes under the p the files show, which is 538's forecast where it stands first. So its counts differ from M2's, but they lean the same way at each level's k:
  - House: 24 against 18.6 at 1,000 votes;
  - Senate: 4 against 7.1 at 10,000;
  - governors: 4 against 9.0 at 10,000.
- **One reading differs, and no level reaches it.** M2's script lets a note stand on one test where only one counts. The ruling as relayed here says "two tests". Both tests count at all three levels, so the two readings agree here.

**What changed** (`chambers.lean_note_test`, with the counts in `LEAN_TESTS`; `history.json`, `lean_note`):
- The note is taken off each Senate p: 170 that stand first and 147 beside 538's.
- It is taken off each of the 420 governor p.
- The House's 3,369 stay (2,514 first, 855 beside).
- Only notes change. Every p, control and other figure is as it was, and so is every other field of each p. The House's files and the governors' of 1978-1984 are unchanged.

### 0.2 A half-life k, and Cha's incumbency codes 2 and 3, under the robustness test (the orchestrator, 2026-11-07 09:03 and 09:08 UTC)

**What was asked.** The orchestrator, 09:03: "run only your half-life k, since M2 has already tested last-3; then the incumbency variants (a) and (b); all under the robustness test." *Reason:* "last-3 has been tested independently, and the tokens are better spent on the untested variants." M2 found that the last one, two and three years, and a trend k, each fail the rule; its reading is that "the near-tie shortfall sits in the mean, not the spread". At 09:08 the orchestrator added: "on the D2-v3 record". Both variants were fixed before any score (`/mnt/project-files/d2/recent-k-design.md`).

**The rule** is round 5's (`variant_test`) with the robustness test. Each variant is scored against the record on 2010-2024, out of sample, banded by the record's means. It is adopted only if it does all of these, on all years and again with any one year left out:
- raises the mean log score;
- brings the 49-51% count nearer the count seen;
- moves no tested count in the 10-20 or 20+ point bands further from the count seen.

**Nothing is adopted.** Every p, control and file stays as it was, and the variants' scores are in `backtest.json` (`variants.halflife`, `incumbency_test`).

**1. The half-life k** (`calibration(..., rule="halflife")`; variant `halflife`). Each earlier scored year T′ has weight 0.5^((T − T′)/4) in the RMS of z, a half-life of two cycles. The near-tie factor and its rule are refitted under it.

| Level | Log score, record | half-life | 49-51%, expected against seen | 50 / 80% coverage | Tested safe cells | One year left out |
|---|---|---|---|---|---|---|
| House | 1.5785 | 1.5867 (+0.0081) | 86.2 against 105 (record 87.5): further | 55.0 / 84.9 (record 56.9 / 86.9) | all three in the 10-20 point band further | fails for every year |
| Senate | 1.2984 | 1.3193 (+0.0208) | 10.9 against 17 (record 11.1): further | 49.6 / 84.8 (record 54.3 / 91.0) | 45-55% in the 10-20 point band further | fails for every year |
| Governors | 1.1780 | 1.1725 (−0.0055) | 12.9 against 16 (record 12.8) | 58.6 / 84.9 (record 59.1 / 86.0) | none further | fails for every year |

- **k by year, record then half-life:**
  - House 2014-2024: 0.982 and 0.950, 0.930 and 0.876, 0.903 and 0.844, 0.895 and 0.848, 0.891 and 0.855, 0.871 and 0.816.
  - Senate 2024: 0.911 and 0.791.
  - Governors 2024: 0.936 and 0.874.
- **What it shows.** M2 read the same in the last-years k.
  - A narrower spread fits the results better on the whole, so the log score rises in the House and the Senate.
  - It also lowers the density at ½ of every race beyond about one sd from even, so the near-even counts fall further short. That happens most in the 10-20 point band, where the House's results land nearer ½ than its means (§7).
  - The coverage moves toward nominal but stays above it (House 50%: 55.0 from 56.9; Senate 80%: 84.8 from 91.0). So the spread is better calibrated overall, and still the near-even counts fall further short.
  - So the shortfall at ½ is not a spread that is too wide, and k stays as it is.

**2. Cha's incumbency codes** (`fit_rows(inc_codes)`, `inc_test`). The two definitions were fixed before any score: (a) codes 1 and 2 count as an incumbent; (b) 1, 2 and 3. They apply to the fit rows of 2006-2024, which come from Cha. The Senate's rows of 1982-2004 and the governors' before 2006 keep their own definitions. Under each, everything is refitted on earlier years only: the coefficients, k, and the near-tie factor and its rule. The half-life k was not adopted, so there is no second setting to score.

- **Rows that change** (of the Cha rows):
  - House: 59 of 3,805 under both (a) and (b), since no House nominee is coded 3.
  - Senate: 9 of 319 under (a), 22 under (b).
  - Governors: 3 of 232 under (a), 14 under (b).

| Level | Variant | Log score (record) | 49-51%, expected against seen (record) | Tested safe cells | One year left out | Decision |
|---|---|---|---|---|---|---|
| House | (a) | 1.5862 (1.5785), +0.0076 | 86.9 against 105 (87.5): further | all three in the 10-20 point band further | fails for every year | not adopted |
| House | (b) | 1.5839, +0.0053 | 87.1 (87.5): further | all three in the 10-20 point band further | fails for every year | not adopted |
| Senate | (a) | 1.2980 (1.2984), −0.0004 | 10.8 against 17 (11.1): further | 48-52% in the 10-20 point band further | fails for every year | not adopted |
| Senate | (b) | 1.2977, −0.0007 | 10.3 (11.1): further | the same | fails for every year | not adopted |
| Governors | (a) | 1.1817 (1.1780), +0.0038 | 12.7 against 16 (12.8): further | none further | passes only without 2010 | not adopted |
| Governors | (b) | 1.1819, +0.0039 | 12.4 (12.8): further | 45-55% in the 10-20 point band further | fails for every year | not adopted |

- **b_inc barely moves.** Here it is record / (a) / (b), with the record's standard error:
  - House: 2010 0.0944 / 0.0943 / 0.0943 ± 0.0031; 2024 0.0560 / 0.0568 / 0.0568 ± 0.0013.
  - Senate: 2010 0.1045 / 0.1045 / 0.1046 ± 0.0045; 2024 0.0908 / 0.0903 / 0.0904 ± 0.0037.
  - Governors: 2010 0.0814 / 0.0816 / 0.0815 ± 0.0067; 2024 0.0724 / 0.0727 / 0.0717 ± 0.0053.
  - Every year is in `incumbency_test.b_inc_by_year`.
- **The House under (a).** Counting its 59 nominees elected in specials as incumbents raises the log score. But the near-even counts move further from the counts seen, so the rule does not adopt it.
- **No contest's `forecast_inputs.incumbency` changes.**

**Code.** These changes to `chambers.py` leave the record as it was; a recompute gives the same files, apart from the commit and the read time:
- the variant `halflife` and `K_HALF_LIFE`;
- `INC_CODES`, with `fit_rows(inc_codes)`;
- `inc_test`;
- `b_inc_se` in each fit;
- caches keyed by the fit rows, so that two definitions of the rows can be scored in one run;
- `_variant_score(..., band_rows)`, which bands a variant by the record's means.

### 0.3 Round 4's near-tie factor taken again under the robustness test, and the governors' near-even note (the orchestrator, 2026-11-07 08:54 UTC)

**What was asked** (the orchestrator, 08:54, after #51):
- **The near-tie factor.** "The test applies to every change that stands, not only to round 5's. Retake round 4's near-tie factor for the House and the Senate. Where it fails, take it out and report it beside the forecast." *Reason, in its words:* "a rule kept for new changes only would leave older knife-edge changes standing on less evidence than new ones need."
- **The governors' note.** "Write the note on each governor p, built from your back-test with its own counts (4.5 against 0, 2006–2024)." *Reason:* "a known lean of the forecast should be visible to a reader, whichever forecast stands."

**1. The test** (`near_tie_test`; each scheme's `round_5_cells`, `leave_one_year_out` and `robust` in `backtest.json`, `near_tie`). A scheme is adopted for a level only if it passes all three of these, on 2010-2024, the years it reaches:
- **Round 4's test, as before** (§2.6). It must raise the log score, bring the 49-51% count nearer the count seen, and not move the safe seats' 49-51% count further from it.
- **Round 5's cells.** In the 10-20 and 20+ point bands, no near-even count (49-51, 48-52 and 45-55%) may move further from the count seen. A cell is tested where its count seen or expected is 5 or more. *Reason:* by the orchestrator's reason above, an old change must meet what a new one needs, and a new one needs these cells.
- **Both again with any one scored year left out.**

| Level | Scheme | All years: round 4's test | All years: round 5's cells | One year left out | Decision |
|---|---|---|---|---|---|
| House | one factor | passes (log score +0.0007) | passes (three cells tested, all 10-20 points) | passes for every year | **stands** |
| House | by band | passes (+0.0007, a little lower) | passes | passes for every year | passes, but scores lower |
| Senate | one factor | passes (+0.0033) | **fails**: 48-52% in the 10-20 point band, 5.8 expected against 5 seen, from 5.5 without it | fails without 2012, 2014 or 2024 (that cell), and without 2020 (the safe seats' 49-51% count) | **taken out** |
| Senate | by band | passes (+0.0007) | passes | fails without 2024 (log score −0.0016) | not adopted |
| Governors | either | fails (log score lower) | | | none, as before |

- **The House keeps its factor.** It passes everywhere, so its p and control are unchanged.
- **The Senate loses its factor.** Its p of record is now the model's own forecast as it stands, with no near-tie factor.
  - Each of the model's own Senate p (the one standing first, or one beside it) carries `near_tie_not_of_record`. That gives the factor, the multiplier and what p would be with it, which is the p of before, to the digit.
  - Each Senate file's `model.near_tie.taken_out` gives the year's factor, its fitting years, and where the test fails.
  - The factors taken out are 0.886 in 2010, then 1.079, 1.100, 1.120, 1.128, 1.177, 1.198 and 1.229 in 2024, every one pooled over the levels.
  - 538's p is unchanged; it was never calibrated.

**2. Round 5's variants on the new Senate record.** Each variant is scored against the record, and the Senate's record no longer has the factor. No variant passes at any level (`backtest.json`, `variants`), so nothing changes:

| Level | Variant | All years | One year left out | Decision |
|---|---|---|---|---|
| House | shrink | log score +0.0259, but 49-51% in the 10-20 point band further | fails for every year | not adopted |
| House | t4 | log score −0.0028 | fails for every year | not adopted |
| House | both | log score +0.0342, but three counts in the 10-20 point band further | fails for every year | not adopted |
| Senate | shrink | log score +0.0220, but 48-52% in the 10-20 point band further (6.3 expected against 5 seen, from 5.5) | fails without 2010, 2012, 2014, 2016 or 2024 | not adopted |
| Senate | t4 | log score −0.0043 | fails for every year | not adopted |
| Senate | both | log score +0.0305, but 48-52% and 45-55% in the 10-20 point band further | fails for every year | not adopted |
| Governor | shrink | log score −0.0031 | fails for every year | not adopted |
| Governor | t4 | passes: log score +0.0265 | fails without 2010, 2018 or 2020 | not adopted |
| Governor | both | passes: log score +0.0177 | fails without 2010, 2012, 2018, 2020 or 2024 | not adopted |

The House's shrink scores differ from §0.4 (+0.0266 there). Under shrinkage the near-tie factor is refitted, and it now fails the robustness test too.

**3. The governors' near-even note.** *Since 11:16 it is taken off again: its two tests lean opposite ways (§0.1, item 3).* `chambers.py history` now writes a `note` onto each of the 420 governor p of 1986-2024. Its words are the brief's:

> this route's back-test shows fewer near-even finishes than it forecast (0 against 4.5 within 5,000 votes, 2006 to 2024), so p may be high

- **Where the counts come from.** They are read from `history.json` (`by_level.governor.by_year`, and the summary in `governor_note`): 4.52 expected against 0 seen. The expected count uses each p's own forecast, which is 538's where it stands first.
  - By year: 0.72 in 2006, 0.19, 0.74, 0.26, 0.53, 0.27, 0.89, 0.20, 0.54 and 0.18 in 2024.
- **The order of the counts.** Seen comes first, then forecast. That follows the sentence's own order, "fewer near-even finishes than it forecast", and D3's note on the measures (#37).
- **p is not corrected**, as the brief says.
- **History runs after compute.** compute rewrites p, and history writes the note.

**Sums, before and after** (before is `main` at 00961e4, #51):

| Level | Sum of p, before | after | Control, before | after |
|---|---|---|---|---|
| House, 2008-2024 | 1.0157e-2 | unchanged | 1.4159e-4 | unchanged |
| Senate, 2006-2024 | 4.4685e-4 | 4.4426e-4 | 4.8432e-5 | 4.7655e-5 |
| Governors, 1986-2024 | 9.8925e-4 | unchanged | | |

- **The Senate by year.**
  - 2010 rises ×1.119, since its factor was below one.
  - 2012 falls ×0.932.
  - 2024 falls ×0.827. Delaware is still its largest p, now 1 in 214,130 (from 1 in 177,747).
  - 2014 is unchanged, since 538 stands first in every race. 2016-2022 move under 1%, since 538 stands first in most races.
  - 108 Senate p change in all, from ×0.814 (Wyoming 2024) to ×1.128 (Oklahoma 2010).
- **History.** Within 5,000 votes the Senate now expects 4.43 against 5 seen (from 4.46). Within 20,000 it expects 17.44 against 17 (from 17.54).

### 0.4 M2's second pass: three fixes, and round 5 taken again under the robustness test (the orchestrator, 2026-11-07 08:36 UTC)

**What was asked** (brief, amended 08:36). M2's second pass reproduced every p, fit and back-test cell, and found three faults. Fix them in one pull request, then take each of round 5's decisions again under a new test, fixed before any score:
- a change is adopted only if it improves the out-of-sample test, as before;
- and it still improves it, with no tested cell made worse, when any one scored year is left out.

*Reason, in its words:* "A change adopted on a knife edge is as likely noise as signal, and the model's default is no change." The test applies from now on, to every change to a forecast at every level.

**1. The House specials' lean in the fit rows** (`chambers.fit_rows`).
- **The fault.** A special fills the old Congress's term and is held on the old Congress's lines. The files took its lean that way (the lines of t − 2), but the fit rows took the sheet of the special's own year. Pennsylvania's 18th of 2018 was +0.13 in the rows against −0.11 in the file.
- **The fix.** The rows now read as the files do. 17 rows move: 2012 AZ-08, KY-04, MI-11, OR-01 and WA-01; 2018 PA-18; 2022 CA-22, FL-20, IN-02, MN-01, NE-01, NY-19 and NY-23; 2024 CO-04, NJ-10, NY-03 and NY-26. Each now equals its file's `forecast_inputs.lean` to 1e-6.
- *Reason:* the fit must be fitted on the inputs it is applied to.
- **The effect.** Only the House's fits move, by about 1e-3. Its out-of-sample log score of record rises from 1.5743 to 1.5785.

**2. The FEC's joined lines** (`fec_federal_elections.py`). Two faults in the reading of the FEC's file joined candidates into one line marked "D/R".
- **One id for two candidates.** The file sometimes gives two candidates of one contest the same FEC id, and the reader summed lines by id. For example, Price (D, 265,751) and Lawson (R, 153,947) in North Carolina's 4th of 2008 both carry H6NC04037. Now one id's lines are one candidate's only under one surname; a second surname is a second candidate, and the contest notes it.
- **A party from a primary line.** The file prints each candidate's primary lines beside the November ones, and the reader took a party from either. So a primary loser who ran in November on another line was given both parties. Jennings (New York's 5th of 2012) lost the Democratic primary and was the Republican nominee; Schley (New York's 13th) the same; Halvorson (Pennsylvania's 9th of 2016) lost the Republican primary and won the Democratic nomination by write-in. Now a party counts only from a line that carries the November vote.
- **The split** comes from the FEC's own per-candidate rows in every case, so Cha was not needed. Each split matches Cha's count (Price 265,751; Ramirez 121,764).
- **Vermont at large, 2008 and 2016, is not a joined line.** Welch won both parties' nominations, and the FEC's line "D/R" is one candidate's: "Democrat in Primary; Democrat and Republican in General", in its words of 2008. No Republican ran against him, so p is not computed, as before.

The contests whose p changed state:

| Contest | Before | After | p |
|---|---|---|---|
| House 2008, North Carolina 4 | Price "D/R", 419,698; p = 0 | Price 265,751, Lawson 153,947 | 5.34e-7 |
| House 2022, Illinois 3 | Ramirez "D/R", 177,759; p = 0 | Ramirez 121,764, Burau 55,995 | 2.72e-7 |
| House 2008, New Jersey 5 | Garrett "R/D", 303,686; not computed | Garrett 172,653, Shulman 131,033 | 1.55e-6 |
| House 2020, Tennessee 7 | Green "R/D", 341,027; not computed | Green 245,188, Sreepada 95,839 | 9.13e-8 |
| Senate 2010, New Hampshire | Ayotte "R/D", 440,763; not computed | Ayotte 273,218, Hodes 167,545 | 4.71e-6 |
| House 2016, Pennsylvania 9 | two Republicans; not computed | Shuster (R) against Halvorson (D) | 8.84e-8 |
| House 2012, New York 5 | two Democrats; not computed | Meeks (D) against Jennings (R) | 6.40e-11 |
| House 2012, New York 13 | two Democrats; not computed | Rangel (D) against Schley (R) | 4.53e-13 |

- **Two-party counts that changed**, where a minor candidate's votes had been added to a nominee's:
  - Senate 2012, New Mexico: Wilson 379,459 → 351,260, without Barrie's 28,199. p 3.127e-6 → 3.246e-6.
  - Senate 2010, Oregon: Huffman 582,227 → 566,199. p 5.72e-7 → 5.79e-7.
  - House 2012, Tennessee 1: Roe 185,124 → 182,252. House 2014, Connecticut 4: Himes 106,878 → 106,873. Senate 2020, Michigan: Peters 2,734,573 → 2,734,568.
- **Who was on the ballot.** The counts of Democratic and Republican nominees (`ballot`) fall in 72 Senate and House contests, where primary losers had been counted. "n/a" in the file's November column marks a primary line too (New York 2008, Texas 2006), and is read so. Sanders, in Vermont's Senate races of 2006 and 2018, is now counted as the independent who caucuses with the Democrats, as he ran; his p is unchanged in 2006 and moves under 0.1% in 2018.
- **The minor candidates** with a borrowed id (a write-in under a nominee's id, for example) are now their own lines, and each is noted.
- **§6**: Illinois's 3rd of 2022 is no longer a real difference against Cha; it was this fault.

**3. The Vice President's tie vote** (`vice_president_chance`). The presidential chance now takes the College's units as the record holds them: Maine and Nebraska statewide (2 electoral votes each) and by district (1 each).
- *Reason:* that is how the College is chosen.
- 2024: 0.5295, from 0.5286.
- 2008 and 2012 are unchanged: D1's record forecasts no district in those years, so the states stand whole there as before. 2016 and 2020 take 538's national chance, which counts the districts already.
- The Senate of 2024's control sum moves 2.8121e-6 → 2.8147e-6.

**4. Round 5 taken again** (`variant_test`, with `leave_one_year_out` and `robust` for each variant in `backtest.json`). After 1 to 3, scored on 2010-2024, out of sample:

| Level | Variant | All years | With one year left out | Decision |
|---|---|---|---|---|
| House | shrink | log score +0.0266, but 49-51% in the 10-20 point band further from the count seen | fails without 2010, 2020, 2022 or 2024 | not adopted (was adopted) |
| House | t4 | log score −0.0028 | fails every year | not adopted |
| House | both | log score +0.0342, but three counts in the 10-20 point band further | fails every year | not adopted |
| Senate | shrink | log score +0.0190, but 48-52% in the 10-20 point band further | fails every year but 2020 | not adopted, as before |
| Senate | t4 | log score −0.0072 | fails every year | not adopted |
| Senate | both | log score +0.0315, but 45-55% in the 10-20 point band further | fails every year | not adopted |
| Governor | shrink | log score −0.0031 | fails every year | not adopted |
| Governor | t4 | passes: log score +0.0265, 49-51% 13.8 against 16 seen, from 12.8 | fails without 2010 (the 49-51% count, and 45-55% in the 10-20 point band), 2018 or 2020 (45-55% in the 10-20 point band) | not adopted (was adopted) |
| Governor | both | passes: log score +0.0177 | fails without 2010, 2012, 2018, 2020 or 2024 | not adopted |

- **Every level returns to round 4's forecast:** D2-v3, the mean as fitted, normal first, k on all earlier years, and round 4's near-tie factor for the House and the Senate. The governors' sums return exactly to round 4's (9.8925e-4 over 1986-2024).
- **The Senate's rejection** still rests on one cell (48-52% in the 10-20 point band), but no longer on a knife edge: the same cell fails on all years and with every year left out but 2020.
- **Round 4's near-tie rule** is not round 5's decision, so it is not taken again here. It is checked under the same test and reported beside:
  - the House's scheme (`level`) passes with every year left out;
  - the Senate's `level` scheme fails without 2020, where the 49-51% count beyond 10 points from even moves further from the count seen; its `band` scheme fails without 2024, on the log score.
  - So under the new test the Senate would take no near-tie factor. On the orchestrator's word it was taken out (§0.3).

**5. The governors' near-even note** is not written. The brief asks for it if round 5's governor forecast stands, and it does not. Under the normal forecast that stands now, the governors still show the shortfall: 4.5 expected within 5,000 votes in 2006-2024 against none seen (Poisson chance 0.011); 9.9 against 5 over 1986-2024 (§5). On the orchestrator's word it is written onto each governor p (§0.3), and taken off again since its two tests lean opposite ways (§0.1, item 3).

**Sums, before and after** (before is `main` at f22bf6b, after #45):

| Level | Sum of p, before | after | Control, before | after |
|---|---|---|---|---|
| House, 2008-2024 | 1.0184e-2 | 1.0157e-2 | 1.4465e-4 | 1.4159e-4 |
| Senate, 2006-2024 | 4.4200e-4 | 4.4685e-4 | 4.8468e-5 | 4.8432e-5 |
| Governors, 1986-2024 | 1.0439e-3 | 9.8925e-4 | | |

- **The House by year.**
  - 2010 and 2012 take round 4's factors again (×0.888, ×1.078).
  - 2014 rises 7.5% and 2024 falls 4.7%, as the shrinkage comes off. The far seats' p falls back to the normal's: as low as ×0.037 (New York's 13th of 2020, at 1.5e-21).
  - 2016-2022 move under 2.3%: 538 stands first in most of the close races of 2018-2022.
  - 2008 rises 0.2%, with North Carolina's 4th and New Jersey's 5th.
- **The Senate** rises 1.1%, mostly with New Hampshire's race of 2010 (4.7e-6).
- **The governors** of 1986-2024 return to round 4's p, apart from 2018 and most of 2022, where 538 stands first and nothing changed.

### 0.5 The incumbency fix (M2's second pass; the orchestrator, 2026-11-07 08:06 UTC)

**What was wrong.** M2 found p wrong by more than a factor of two in four contests, all from `forecast_inputs.incumbency`. `build_congress.py` had two faults, and it is fixed there.
- **It looked up Cha's candidates by last name alone.** A second candidate of the same name overwrote the first. South Dakota at large, 2024, has two Johnsons, and Utah's Senate race of 2006 has Orrin and Julian Hatch. So the incumbent was read as not running.
- **It took the FEC's incumbent mark from any candidate on a major-party line,** including one who was not the nominee. In New York's 14th of 2018, Crowley had lost the primary and stayed on the ballot; in Michigan's 11th of 2014, Bentivolio ran as a write-in.

The fit rows read Cha directly, so the fits were never affected.

**The fix** (`incumbency`, `cha_entry`). Change nothing else, and not k: the orchestrator's words.
- **The definition is now the fit's** (§2.2): Cha's hand coding of the race's two nominees. Those are the candidate with the most votes on a Democratic line (or the independent who caucuses with the Democrats) and the candidate with the most votes on a Republican line. Where Cha does not hold the nominee, the source of record's own mark on that same nominee is used.
- **Cha's entry is found within the contest matched on year, office, state, district and special.** It is the candidate of the same last name; among several of one name, the one with the same votes, else the same first name. The source lists some candidates twice under two spellings with the same votes, and those count as one.
- **The same lookup now serves the check against Cha** (§6).

**What changed.** Thirteen contests' incumbency changed:

| Contest | Incumbency, before → after | Why | p, before → after |
|---|---|---|---|
| Senate 2006, Utah | 0 → −1 | Hatch read as Julian Hatch | 2.798e-6 → 4.192e-7 (×0.150) |
| House 2014, Michigan 11 | −1 → 0 | Bentivolio's write-in | 1.838e-6 → 8.729e-6 (×4.75) |
| House 2018, New York 14 | +1 → 0 | Crowley not the nominee | 1.139e-14 → 2.360e-11 (×2,071) |
| House 2024, South Dakota at large | 0 → −1 | Dusty Johnson read as Sheryl Johnson | 6.374e-7 → 2.249e-8 (×0.0353) |
| House 2014, Louisiana 5 | −1 → 0 | McAllister was not the Republican with the most votes | not computed (open primary); its control mean 0.297 → 0.375 |
| House 2006, Arkansas 4 | 0 → +1 | Mike Ross read as Joe Ross | not computed (House 2006) |
| House 2006, Michigan 7 | −1 → 0 | Schwarz not the nominee | not computed (House 2006) |
| House 2018, Washington 9 | 0 → +1 | Adam Smith read as Sarah Smith | not computed (two Democrats) |
| House 2012, California 15 and 35; 2016, California 17 | +1 → 0 | the incumbent Democrat was not the Democrat with the most votes | not computed (two Democrats) |
| House 2012, California 44 | +1 → 0 | Hahn, the Democrat with the most votes, is coded 2 in Cha (an incumbent elected in a special election), and the fit counts only 1 as an incumbent; Richardson, coded 1, had fewer votes | not computed (two Democrats) |
| House 2016, Kansas 1 | −1 → 0 | Huelskamp not the nominee | not computed (no Democrat) |

- **Control.** The four contests with p change their own control. Through P(decides | tie), the other seats of the same chambers move too:
  - Senate 2006: control sum 1.155e-6 → 8.613e-7, with expected Democratic seats 45.56 → 45.40.
  - House 2014: 6.590e-6 → 6.884e-6, with Michigan 11 and Louisiana 5 moving.
  - House 2018 and House 2024 move under 0.4%.
- **Sums of p.** Senate 2006: 5.134e-5 → 4.896e-5. House 2014: 1.1115e-3 → 1.1183e-3. House 2024: 7.0208e-4 → 7.0146e-4. Nothing else moves.
- **In §5.** The results table and the historical check are brought up to date: Senate 2006's largest p for control (Rhode Island) is now 1 in 9,343,171, from 7,285,814; House 2014's (California 21) 1 in 4,061,804, from 4,273,353; House 2024's 1 in 711,488, from 711,626. The historical check moves by under 0.6% (House within 20,000 votes: 410.3 expected, from 410.0; Senate: 17.3, from 17.4), and every count seen is the same. The sums tables of rounds 4 and 5 stand as those rounds left them; this fix's sums are above.
- **The check against Cha** loses nine false differences, each from the same name clash, and gains none (§6).
- **Unchanged.** Every other contest's incumbency, mean and p, the fits, k, λ and the near-tie factors. Before the fix, the rebuilt files reproduced `main` exactly, apart from read times and commits.
- **A source note, not changed.** Cha codes Angus King as an incumbent in 2012, when the seat was open, and as not one in 2018, when he was. The fix takes Cha's coding as it stands, as the fit does. Maine 2018 has no p (ranked choice); Maine 2012's p rests on +1. It is open (§7).
- **A definition note, not changed.** Cha's guide codes `inc` 0 (not an incumbent), 1 (an incumbent), 2 (an incumbent elected in a special election) and 3 (a senator appointed by the governor). The fit counts only 1, so it reads 2 and 3 as not incumbents. The fix keeps that, since it takes the fit's definition. It is open (§7).

### 0.6 Round 5 (the orchestrator, 2026-11-07 07:19 UTC): the means and the tails

*No longer of record:* neither of round 5's adoptions survives the robustness test of §0.4. This section records round 5 as it stood.

**What was asked.** Round 4 left one point open: the House's results land about 1.5 points nearer ½ than its means in races 5 to 20 points from even. The orchestrator asked for three variants, each fitted on earlier years only and scored out of sample on 2010-2024: (i) the mean shrunk toward ½ by a factor fitted on earlier years; (ii) t4 tails standing first in place of normal; (iii) both. The near-tie factor is refitted after each. Adoption is by round 4's three conditions, with the safe-seat bands (10 to 20 points from even, and beyond 20) added where the record's counts allow a test. *Reason, in its words:* "the far seats are most of the House, and a forecast too sure of them puts their p orders of magnitude too low, which no reader would see."

**What was done** (§2.7).
- **Shrinkage.** mean′ = ½ + λ·(mean − ½). λ is the slope, through ½, of the result on the mean over the level's earlier years' raw out-of-sample forecasts, weighted by 1/sd². It needs three such years, as k does. k is then refitted on the shrunk means.
- **Adopted for the House: shrinkage.** The log score rises from 1.5743 to 1.6008, the largest gain of any change so far. The 49-51% count moves nearer the one seen (88.8 against 105, from 87.5), and so does every count in the 10-20 point band. λ is 1.001 in 2014, falling to 0.93 by 2022 and 2024.
- **Adopted for governors: t4 first.** The log score rises from 1.1780 to 1.2045, and the 49-51% count moves nearer (13.8 against 16, from 12.8). The one safe-band count that can be tested moves nearer too.
- **Nothing adopted for the Senate.** Shrinkage raises its log score (1.3017 to 1.3208) but moves one safe-band count further from the one seen: 48-52% in the 10-20 point band, 6.3 expected against 5 seen, from 5.8. Both together fail the same way at 45-55%. The rule rejects both, so the Senate is unchanged.
- **t4 is not supported in the House.** It lowers the House's log score (1.5743 to 1.5728). It also moves every near-even count in the 10-20 point band further from the one seen; at 45-55% it expects 67.9 against 105 seen, where normal expects 92.7.
- **The far seats.** Beyond 20 points from even, the record cannot test p at ½: 1 of 789 House results finished within 45-55%, against 1.24 expected under normal and 3.21 under t4. What the record does show argues against heavier tails there. Under normal, 42 of those results finished beyond the forecast's 5% quantile toward ½, against 39.4 expected, and 5 beyond the 1% quantile, against 7.9. So the evidence does not support the roughly ×500 that t4 would give a seat like Arkansas's 1st of 2024 (mean 0.266: normal 8.7e-11, t4 4.3e-8). Under shrinkage their p rises by a median ×1.39, at most ×16.
- **The near-tie factor, refitted.** Under shrinkage the House's rule turns to the band scheme: a factor in the two bands nearest ½ and none from 0.10 up. So the House's safe seats no longer take round 4's factor of 1.12 to 1.30; they take the shrinkage instead. The Senate keeps round 4's factor.

**Sums, before and after** (§5):

| Level | Sum of p, before | after | Control, before | after |
|---|---|---|---|---|
| House | 1.0158e-2 | 1.0178e-2 (+0.2%) | 1.4184e-4 | 1.4438e-4 (+1.8%) |
| Senate | 4.4438e-4 | unchanged | 4.8762e-5 | unchanged |
| Governors | 9.8925e-4 | 1.0439e-3 (+5.5%) | | |

- **The House by year.** 2010 rises 12% and 2012 falls 7%: λ cannot be fitted yet for those years, and the band scheme has no factor for them, where round 4 applied 0.886 and 1.079. 2014 falls 7% and 2024 rises 5%. 2016-2022 move under 3%, since 538 stands first in most of the close races of 2018-2022.
- **The governors.** p rises in close races (a median ×1.26 within 5 points of even, where t4's density at its centre is 1.33 times the normal's) and falls further out (×0.86 at 5-10 points, ×0.66 at 10-20). This applies to every year with the model's own forecast first, 1986-2024: 356 contests.
- **The largest House p.** California's 22nd of 2024, from 1 in 32,693 to 1 in 29,944.
- **What is left.** The House's forecast sd is wider than its results in every year 2010-2024: z rms 0.75 to 0.92 after shrinkage. k is fitted on all earlier years, and the errors have shrunk since. A too-wide sd near ½ gives exactly the near-even shortfall, so this is the likely root of it. It is open (§7).

### 0.7 Round 4 (the orchestrator, 2026-11-07 07:04 UTC): the near-even shortfall

*Since §0.3 the House's factor stands and the Senate's is taken out: it fails the robustness test. The figures below are round 4's as it stood.*

**What was asked.** Round 3's back-test found more races finishing within 49-51% than the forecasts expected: 113 against 89.3 in the House, 30 against 21.6 in the Senate. The orchestrator asked for D3's rule of #31: a near-tie calibration fitted on earlier years only, adopted only if it improves the out-of-sample test. *Reason, in its words:* "about 20% too few near-even finishes means p near even is about 20% low. That understates exactly the races law 1a says the site must show, and k cannot reach it because it moves the spread, not the shape."

**What was done** (§2.6).
- **The rule.** The forecast's density within one point of ½ is multiplied by a factor fitted on earlier years' out-of-sample near-ties, and the forecast renormalized. So the model's own p is multiplied by that factor over the renormalization.
- **The two schemes tested.** One factor per level, and a factor by band of |mean − ½|. Both were scored on 2010-2024 at 49-51, 48-52 and 45-55%, with coverage and log score.
- **Adopted: one factor per level, for the House and the Senate.** It raises the log score (House 1.5736 to 1.5743, Senate 1.2984 to 1.3017) and brings every count nearer the one seen. In the safe seats' band it stays below the count seen, so no safe seat's p is raised beyond what the record at its distance shows.
- **Not adopted for governors.** Both schemes lower their log score.
- **Where it applies.** 2,246 contests: the model's own p for the House and the Senate of 2010-2024. Each forecast records its `calibration` (factor, multiplier, fitting years), and p's `under` ends "calibrated to earlier years' near-ties".
- **538's forecasts are not calibrated.** They show no shortfall: where 538 stands first, 40 House races finished within 49-51% against 50.6 expected.

**Sums, before and after** (§5):

| Level | Sum of p, before | after | Control, before | after |
|---|---|---|---|---|
| House | 9.903e-3 | 1.0158e-2 | 1.371e-4 | 1.418e-4 |
| Senate | 4.413e-4 | 4.444e-4 | 4.799e-5 | 4.876e-5 |
| Governors | 9.893e-4 | 9.893e-4 | | |

- **Where p rises and falls.** The House of 2024 rises 26% (factor 1.295) and the Senate of 2024 21% (1.229). The House and Senate of 2010 fall 11%: the factor fitted on the years before 2010 is 0.886, since those years had fewer near-ties than expected.
- **What it does not reach.** The counts at 48-52% and 45-55% stay short (House 166.6 against 209, and 422.6 against 521). The House's results land about 1.5 points nearer ½ than its means in races 5 to 20 points from even. That is a question for the means, and it is left open (§7).

### 0.8 Round 3 (the orchestrator, 2026-11-07 06:36 UTC), each item with its reason

1. **Governors from 1978, from Algara and Amlani's county returns.** *Reason, in the orchestrator's words:* "the maker wants as much data as can be found, and this both adds races and restores p."
   - **The source.** Algara and Amlani's county returns for governor, 1865-2020 (Harvard Dataverse, CC0 1.0, no guestbook). They are taken by script (`algara_amlani.py`), and the file's MD5 is checked against the one Dataverse publishes. The file is R's own format, and this environment has no R, so `rdata_reader.py` reads it from R's published description of the format, with no package added.
   - **What is built from it.** The county returns are summed to the state, and the 327 governor races of the even years 1978-2004 are added as contests (`data/governor/1978.json` to `2004.json`).
   - **What it restores.** The governors' fit now reaches back to 1978, so 2006-2016 are fitted on earlier cycles: 2006 on the 14 cycles of 1978-2004. Governors with p go from 88 to 420.
   - **The last-race term is kept.** Before 2006 the last race comes from Algara and Amlani, odd years included.
   - **Why 1978.** It is the first even year whose earlier presidential vote (MEDSL, 1976 on) and sitting president (National Archives, 1976 on) are in the sources.
   - **Checked against Cha, Kuriwaki and Snyder** over 2006-2020 (§6). Missouri's rows fall short, so Missouri before 2006 is left out of every use (§3).
2. **House 2006-2012: the Senate's national terms, back-tested first.** *Reason:* the orchestrator's test. If the House on the Senate's terms keeps z sd and coverage within a few points of the House's own over 2014-2024, use it for the early years.
   - **It does** (§2.3). Over 2014-2024 (2,286 races) the result is:
     - z sd 0.748, against 0.770 on the House's own terms;
     - coverage 64 / 92 / 98.8%, against 61 / 91 / 98.5%;
     - log score 1.633, against 1.603.
   - So the House of 2008-2012 takes the Senate's national terms, fitted on the Senate's own earlier cycles. Its lean, incumbency and race-error terms are fitted on its own earlier cycles. Each such file's `model.national_from` marks it "national terms from the Senate's earlier cycles".
   - **The House of 2006 has no earlier House cycle** to fit those terms on, so it stays not computed. FEC 2004 would be needed (§7).
   - The House gains p for 1,116 contests, and its control is now computed for 2008-2012.
3. **The spread, calibrated on earlier cycles only.** *Reason, in the orchestrator's words:* "a forecast wider than the record supports understates p, which tilts the site toward the maker's own claim (law 1a). The forecast should be as sharp as the record allows and no sharper."
   - **What is done.** Each level's sd, both the national part and the race's own, is multiplied by k. k is the root mean square of the standardized errors of that level's earlier years, each year forecast out of sample from its own earlier cycles. It applies once three such years exist.
   - **What it improved.** The log score at every level, and z sd moved nearer 1 (§2.4).
   - **Two factors, no better.** A separate factor for the national part was tested. It improved nothing that matters, and it made the national misses worse.
   - **Narrowing does not raise every p.** It raises p in races within one sd of even and lowers it in the rest. So the House sum of 2024 fell 11% (§2.4).
   - **The governors' national z rms of 2.45 was the small sample** (§2.5). Over 1986-2024 it is 1.29. Counting the noise in an eleven-race year's own swing, it is 0.91. 2020 stands as the one real miss, at 2.6 sd.

**What changed, in totals** (round 2, on `main` at b00c55e, against now):

| | Contests | p computed | 538 first | p = 0 | Not computed |
|---|---|---|---|---|---|
| Round 2 | 4,997 | 2,650 | 1,064 | 178 | 2,169 |
| Now | 5,324 | 4,098 | 1,064 | 178 | 1,048 |

- **The House.** p for 3,362 contests (2,246 before). 873 are not computed, 368 of them for too few cycles (2006).
- **The Senate.** Unchanged at 316.
- **Governors.** 562 contests (235 before); p for 420 (88 before); 142 not computed. Of these 142:
  - 89 for too few cycles (1978-1984);
  - 7 for Missouri's count;
  - 9 where the others' total could hide a top-two candidate;
  - 2 with no last race;
  - 35 for the structures of §3.

The sums of p by level and year are in §5.

### 0.9 Round 2: the follow-ups from M2 (brief, amended 2026-11-07 05:58 UTC), each with its reason

M2 checked every p (`checks/M2-REPORT.md`) and the orchestrator decided its readings. These stand. Where round 3 changed a figure, it says so in brackets.

1. **The Vice President's tie vote in presidential years is the presidential chance**, not one half (§4). *Reason:* the Senate's control in a presidential year turns on who becomes Vice President.
   - It is 538's where 538's forecast stands first in D1's record of the year. In 2016 and 2020 that is its polls-plus chance that the Democratic ticket wins, 0.7137 and 0.8932.
   - Otherwise it is the model's own chance that the Democrat wins the College: 0.954 in 2008, 0.552 in 2012 and 0.529 in 2024.
2. **The model's own forecast is fitted on earlier cycles only.** It never leaves one cycle out, and its national sd comes from those cycles too. The Senate's fit reaches back to 1982 through MEDSL. A fit needs four cycles, with presidents of both parties among them (§2.3).
   - [Round 3: governors are fitted from 1978, and the House of 2008-2012 is on the Senate's national terms. So only the House of 2006 and the governors of 1978-1984 lack a forecast of the model's own.]

   *Reason:* the model's own forecast is fitted to like past races, from what was known before the election (MODEL §3). A coefficient fitted partly on later years is something no voter knew.
3. **538 is kept on p's error, not the sd's.** It stands first where p's estimated relative error is under 20% (§2.1). *Reason:* the reader sees p, and at z = 3.94 a 7% error in the sd is a 105% error in p (M2 3.9).
4. **Control under 538, reading (c).** A seat whose p is 538's enters the chamber stage with 538's mean and sd as its marginal (§4). *Reason:* one forecast of the seat throughout its figure (M2 2.6).
5. **Governors carry the state's last governor race** as a predictor. It took the log score from 1.064 to 1.143 (M2's A4).
   - [Round 3: the back-test now covers 1986-2024, 448 races (§2.3).]
6. **The files reproduce themselves.** Mean and sd are at full precision. Every p block holds f(½) and names the forecast it is computed from (`of_forecast`). The p = 0 blocks name their script and commit. *Reason:* law 4: a reader recomputing p from the file gets the file's p.
7. **One fetch and one FEC intake.**
   - Every D2 intake script downloads through `pipeline/fetch.py`.
   - D1's `fec_president.py` is now `fec_federal_elections.py president`, with output identical to before.

   *Reason:* one implementation of each thing.
8. **Senate 2014's chances stand as exact**, because they have no step at any plausible run count (M2 3.7).

## 1. Sources taken in by script

Each source is read by one script in `pipeline/intake/`.
- Every download goes through `pipeline/fetch.py`, into a cache outside the repository: `$VOTE_CACHE`, else `~/.cache/vote-intake`. These files were built with `VOTE_CACHE=/tmp/vote-cache`.
- It records the URL, read time, size and SHA-256 of every file. It stops at an HTTP error, or at a redirect to a site other than the URL's own or a storage host named at the call.
- Each script checks sums against the source's own totals and normalizes.
- Rerunning any of them gives the same inputs.

| Script | Source | Covers | Licence | Read |
|---|---|---|---|---|
| `fec_federal_elections.py` | FEC, *Federal Elections* workbooks | House and Senate general results with incumbent marks, 2006-2022. With `president`, the presidential results by state, 1996-2024 (D1's, folded in) | none printed; federal record | 2026-11-07 |
| `clerk_statistics.py` | Clerk of the House, *Statistics of the Presidential and Congressional Election* (PDF) | House and Senate, 2024 (the FEC has no 2024 congressional volume yet) | none printed; House publication | 2026-11-07 |
| `medsl_dataverse.py` | MIT Election Data and Science Lab, Harvard Dataverse | Senate 1976-2024 (the seats not up, and the Senate's fit from 1982); President by state 1976-2024 | CC0 1.0 | 2026-11-07 |
| `candidates_american_general_elections.py` | Cha, Kuriwaki and Snyder, *Candidates in American General Elections*, doi:10.7910/DVN/DGDRDT, v4.1 | House, Senate, governor 2006-2024 (odd years too), hand-coded incumbency | CC0 1.0 | 2026-11-07 |
| `algara_amlani.py governors` (with `rdata_reader.py`) | Algara and Amlani, *Replication Data for: Partisanship & Nationalization in American Elections*, doi:10.7910/DVN/DGUMFI, v1.1: county returns for governor, 1865-2020 | **governors 1978-2004** (the record), the odd years 1977-2005 and two contests Cha lacks (§8), the last governor race before 2006, and the check on Cha's governors of 2006-2020 | CC0 1.0 | 2026-11-07 |
| `downballot_pres_by_cd.py` | The Downballot, presidential vote by congressional district (public Google Sheets) | 2000-2024 presidential vote on the lines of each House election 2006-2024 | none printed | 2026-11-07 |
| `fec_ballot_candidates.py` | FEC, 2024 general election ballot candidates | who sat in Congress in 2024 | none printed; federal record | 2026-11-07 |
| `nara_electoral_college.py` | National Archives, Electoral College pages | president and VP elected, 1976-2024 | federal record | 2026-11-07 |
| `census_acs_population.py` | Census Bureau, ACS 1-year, table B01003 (www2.census.gov table files) | population of each state and district, 2022 and 2024 | federal record | 2026-11-07 |
| `party_divisions.py` | U.S. Senate, *Party Division*; House History, *Party Divisions of the House* | seats by party at the opening of each Congress, with the chambers' notes | none printed; chamber publications | 2026-11-07 |
| `fivethirtyeight_checking_our_work.py` | FiveThirtyEight, `checking-our-work-data` (raw.githubusercontent.com, commit f6d5b2e) | 538's published forecasts by race and day: Senate 2008-2022, House 2010 and 2018-2022, governors 2010, 2018, 2022 | CC BY 4.0 | 2026-11-07 |
| `la_sos_governor.py` (with D3's `la_sos.py` and `local_la.py`, unchanged) | Louisiana Secretary of State, official election results: the workbook of 2023-10-14 and the posted multi-parish results of each 2023 date | **Louisiana's governor of 2023** (the record), gated as D3 gates that year (§8.1) | none printed; public records | 2026-11-07 |
| `ms_governor_rule.py` (with D4's `state_law.py`, unchanged) | Mississippi Legislature, House Concurrent Resolution 47 of 2020 (billstatus.ls.state.ms.us) | Mississippi's rule for electing its governor before 2020 (§8.2) | none printed; a public record | 2026-11-07 |
| `state_governors.py` (with D3's `nj_sos.py`, unchanged) | New Jersey Division of Elections, the Official List for governor, 2025, and its 21 county copies; Virginia Department of Elections, its results site's statewide count, locality breakdown and precinct report, 2025 | **New Jersey's and Virginia's governors of 2025** (the record), gated within the certifying source (§9.1); Kentucky's and Mississippi's 2023 results refused (§9.2) | none printed; public records | 2026-11-07 |
| `build_congress.py` | the caches above | builds `data/senate|house|governor/<year>.json` | | |

**Source of record and check.**
- **The House and Senate.** For 2006-2022 the FEC's volume is the record; for 2024 it is the Clerk's. Cha, Kuriwaki and Snyder check every contest, and the differences are kept in `checks` (§6).
- **Governors of 2006-2024.** Cha is the record.
- **Governors of 1978-2004.** Algara and Amlani's county sums are the record, with `certified` null and no second source. Their `checks` say so.
- **The cross-check.** The two governor sources are compared over 2006-2020 (§6). MEDSL's state-office precinct files for 2022 and 2024 (CC0, no guestbook) remain the lead for a third.

**Algara and Amlani, what the record is.**
- **What it holds.** One row per county and election, with the Democratic and Republican nominees' votes, the county's total vote, and the seat's status: an incumbent's party and re-election bid, or an open seat. The authors coded the status from Congressional Quarterly (the dataset's manual, 2021-08-30).
- **What the files show.** The two nominees by name and votes. The rest appear as one line, "others (not named in the source)", which is the county total less the two nominees, so `ballot.others` is null.
- **What it lacks.** Alaska is not in it, since it has no consistent counties. Seven of the 327 races have a county with no count, marked `votes_incomplete`.
- **The date** is the general election day, inferred; the source gives the year.

**Not taken.**
- MEDSL's House file sits behind a Dataverse guestbook that asks for a name and email. Filling it is the maker's call (law 10).
- 538's own forecast pages redirect to abcnews.com.

The full inventory is `data/sources/congress.md`.

## 2. The forecasts

### 2.1 538's published forecast, first where it can be used

The orchestrator's words of 03:46 put "a reachable published forecast" first, with ours as the check; the rules below are his of 04:12 and 04:20. 538's `checking-our-work-data` keeps every race it forecast, each day and each version, with the projected vote share and the chance of winning.

- **Which forecast.** The last one dated before Election Day, recorded as `as_of`. In 2008 and 2010 the file holds one forecast per race, dated Election Day, and it is marked so.
- **Which version.** 538 showed one version by default. No source read here names it: its pages redirect, and its data READMEs do not say. So the version listed first in the repository's rows comes first, and the others stand beside it in `forecasts`. That is *lite* in 2018-2022, *polls-plus* in 2016 and the only version in 2014. This is an orchestrator choice the maker may correct.
- **Mean and sd.** The mean is the Democrat's projected share of the two leading parties' projected vote. The sd is the one a normal needs to give 538's chance: sd = (mean − ½) ÷ Φ⁻¹(chance), marked inferred. 538's own distribution is not normal, so this sd is "the normal that agrees with 538's mean and chance", not 538's.
- **When it is used.** 538 comes first when three things hold:
  - p's estimated relative error is under 20%;
  - no chance is exactly 0 or 1;
  - other candidates hold under 1% of the chance.
- **Where the error comes from.**
  - *The chance's sampling error*, √(q(1−q)/N). N is the number of simulation runs the chances step by: 50,000 in 2018, 40,000 in 2020 and 2022, and 20,000 in 2016, marked inferred. 2014's chances have no step at any plausible run count and are taken as exact (M2 3.7). The chance is moved one standard error either side and carried through Φ⁻¹ at both ends, not linearized. A chance one run from 0 or 1 is unbounded and falls back.
  - *The rounding of the printed shares.*
- **How each error reaches p.** p = φ(z) ÷ (2n·sd), with z = Φ⁻¹(chance) and sd = (mean − ½) ÷ z.
  - An error in the chance moves z. It moves p by |z² − 1| times its relative error in z, which is the sd's.
  - The mean's rounding moves only the sd, so it moves p by its own relative size.
  - The two are added in quadrature, as `p_relative_error`, beside `sd_relative_error` and `z`.
- **Otherwise** ours comes first, with 538's forecast beside it and the reason in `unusable` (a sentence) and `unusable_kind` (a short class).
- **Control of the chamber.** 538's file gives no joint distribution, so the chamber stage is the model's: its common swing and the other seats. A seat whose p is 538's enters it with 538's mean and sd as its marginal (reading (c), §4).

| Level | Races with a 538 forecast | 538 first | Ours first: no share in the file (2008-2012 Senate; 2010) | chance 0 or 1 | p's error 20% or more | other |
|---|---|---|---|---|---|---|
| House | 1,566 | 853 | 400 | 111 | 200 | 2 |
| Senate | 251 | 147 | 94 | 0 | 9 | 1 |
| Governor | 99 | 64 | 32 | 0 | 3 | 0 |

The table is unchanged by round 3. The 2010 House and governor races that 538 forecast without a share now have p under the model's own forecast (governors on their own earlier cycles, the House on the Senate's terms), with 538's chance beside it.

The two "other" House cases are a 538 Democrat not on our ballot (South Carolina 5th, 2018, where 538 names April Freeman and the record has Archie Parnell) and one race with no Democrat or Republican in 538's rows.

### 2.2 The model's own forecast (method D2-v3)

D2-v3 is D2-v2 (round 2, §0.9) with governors fitted from 1978, the House of 2008-2012 on the Senate's national terms, and each level's sd calibrated on its earlier years (round 3, §0.8). D2-v4 (round 5, §2.7) was D2-v3 with the House's mean shrunk toward ½ and the governors' t4 forecast standing first. Neither survives the robustness test (§0.4), so every level is D2-v3 again. It is used where no published forecast can be, and it is always kept beside 538's as the check. For a race in year t, with y the Democrat's share of the two-party vote:

> y = ½ + a_t + b_lean × lean + b_inc × inc [+ b_lag × (lag − ½), governors only] + e

- **lean**: the Democrat's two-party share of the last presidential vote before year t, minus that election's national share (MEDSL).
  - For the House it is taken on the lines in use in year t (The Downballot); for the Senate and governors, in the state (MEDSL).
  - A House special is held on the old Congress's lines, so its lean is taken on the lines of t − 2.
- **inc**: +1 if a Democratic incumbent runs, −1 if a Republican one does, 0 for an open seat.
  - From 2006 it comes from Cha, Kuriwaki and Snyder's hand coding of the Democratic and Republican nominees. Each contest's `forecast_inputs.incumbency` uses the same definition since the fix of §0.5.
  - For the Senate before 2006 it is inferred from MEDSL (below).
  - For governors before 2006 it is Algara and Amlani's seat status: "Democratic Incumbent" +1, "Republican Incumbent" −1, else 0. It is recorded in `forecast_inputs.seat_status`.
- **lag** (governors only): the Democrat's two-party share in the state's last governor race before year t that a Democrat and a Republican led. Odd years and specials are included. It comes from Cha from 2006 and from Algara and Amlani before, and is recorded in `forecast_inputs.last_governor_race`, with its `source`.
- **a_t**: the year's national swing. It is forecast from whether t is a midterm and from the sitting president's party (National Archives): a_t = c₀ + c_mid·M·P + c_on·(1−M)·P + d.
- **e**: the race's own error, independent across races given a_t.

**Earlier cycles only.** The forecast for year t is fitted on the level's cycles before t and nothing later.
- Its national sd is the regression's own prediction sd from those cycles, s_a·√(1 + z(Z′Z)⁻¹z′). This counts both the swing's spread about the national terms and the terms' own uncertainty when few cycles fit them.
- The forecast is normal, with sd k·√(national sd² + s_e²), where k is the calibration factor (§2.4). A Student-t with 4 degrees of freedom and the same sd stands beside it.
- Every year's fitted terms are in the file's `model`, with the formulas for the mean and the sd (`mean_is`, `sd_is`), so a reader can rebuild each forecast.
  - `s_e_fitted` is the fit's race error and `s_e` the one used (k × `s_e_fitted`).
  - `calibration` gives k's years, races and rule.

**How far back each fit reaches.**
- **Senate, from 1982.**
  - MEDSL's U.S. Senate 1976-2024 adds 380 races of 1982-2004 to Cha's 319 of 2006-2024.
  - 1982 is the first year whose seats' previous regular election, six years before, is in MEDSL. A candidate is the incumbent if their last name is that of the winner of the seat's previous regular election, or of a special in the state in the years between.
  - MEDSL marks no incumbents, so this is **inferred**. On the 295 Senate races of 2006-2024 where both exist, it agrees with Cha's hand coding in 286 (96.9%). The nine that differ are listed in `backtest.json`.
  - Left out before 2006: specials, since whose seat it was, and who held it, is not in the record; and Georgia and Louisiana races whose leader had under half the vote.
- **Governors, from 1978.**
  - Algara and Amlani's county returns add 327 races of 1978-2004, of which 311 enter the fit, to Cha's 230 of 2006-2024 that have a last race.
  - A race enters only where both nominees had votes and the others' total is below the smaller nominee's, so no unnamed candidate can have been in the top two. 9 such races are left out of the fit.
  - Missouri is left out before 2006 (§3).
- **House, from 2006.** The Downballot's district presidential vote begins on the 2006 lines. Its 2006-2010 sheet also gives the 2000 vote on those lines. But which states kept the same lines in 2002 and 2004 is not stated in any source read here, so 2002 and 2004 are not added.
  - **The House of 2008-2012 on the Senate's national terms** (round 3, item 2). It has one to three earlier cycles of its own, fewer than the four a fit of the national terms needs.
    - c₀, c_mid, c_on, s_a and (Z′Z)⁻¹ are the Senate's raw fit on its cycles before t (1982 on).
    - b_lean, b_inc and s_e are fitted on the House's cycles before t.
    - The file's `model.national_from` names the Senate's years.
  - The House of 2006 has no earlier House cycle for the second stage, so it is not computed.

**What each year's fit gives** (2024's, on every earlier cycle; and the House of 2008, the first year on the Senate's terms):

| Level, year | Cycles | Races fitted | b_lean | b_inc | b_lag | s_e fitted | k | s_e used | national sd | sd | ρ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| House 2024 | 2006-2022 (9) | 3,424 | 0.807 | 0.056 | | 0.0504 | 0.873 | 0.0440 | 0.0164 | 0.047 | 0.12 |
| Senate 2024 | 1982-2022 (21) | 667 | 0.574 | 0.091 | | 0.0745 | 0.911 | 0.0679 | 0.0213 | 0.071 | 0.09 |
| Governor 2024 | 1978-2022 (23) | 530 | 0.298 | 0.072 | 0.118 | 0.0790 | 0.936 | 0.0739 | 0.0247 | 0.078 | 0.10 |
| House 2008 | 2006 (1), national terms the Senate's of 1982-2006 | 373 | 0.631 | 0.097 | | 0.0600 | 1 | 0.0600 | 0.0245 | 0.065 | 0.14 |

- **The governors' b_lean** is 0.298 on 1978-2022, against 0.393 on 2010-2022 in round 2, and b_lag is 0.118 against 0.206. Governor races of the 1980s and 1990s followed the presidential vote less closely, as the Senate's did.
- **The House of 2008's b_inc** (0.097) is larger than the House's on more cycles (0.056). It is fitted on 2006 alone.

### 2.3 The back-test, and the fewest cycles a fit needs

Every year is forecast from a fit on its earlier cycles only, with the calibration of §2.4. This is the method of record (`chambers.py backtest`; `backtest.json`, scheme `earlier_calibrated`; `earlier` is the same before calibration). Each forecast is scored against the result:

| Level | Years | Races | z sd | 50 / 80 / 95% coverage | Mean log score | National swing's misses, z rms (with the year's own noise) | Within 49-51%: expected, seen |
|---|---|---|---|---|---|---|---|
| House | 2008-2024 | 3,432 | 0.90 | 56 / 86 / 96.9% | 1.53 | 0.96 (0.95) | 89.3, 113 |
| Senate | 1996-2024 | 474 | 0.91 | 53 / 86 / 97.3% | 1.18 | 1.00 (0.88) | 21.6, 30 |
| Governor | 1986-2024 | 448 | 0.95 | 55 / 82 / 95.5% | 1.09 | 1.29 (0.91) | 30.9, 30 |

On 2006-2024 alone, the Senate's z sd is 0.85 (319 races) and the governors' 0.94 (230 races).

**The House on the Senate's terms** (round 3, item 2). The test asks whether the Senate's national terms serve the House where both can be scored: 2014-2024, where the House has four cycles of its own. Stage one is on the House's cycles in every scheme. The table is from `backtest.json`, `house_on_senate_terms`, before calibration.

| House 2014-2024, 2,286 races | z sd | 50 / 80 / 95% coverage | Log score | National z rms |
|---|---|---|---|---|
| the House's own terms | 0.770 | 61 / 91 / 98.5% | 1.603 | 0.76 |
| the Senate's terms | 0.748 | 64 / 92 / 98.8% | 1.633 | 0.28 |
| the Senate's terms, stage one on the last cycle only | 0.836 | 62 / 88 / 97.4% | 1.836 | 0.28 |
| the Senate's terms, stage one on the last 2 cycles | 0.797 | 65 / 90 / 97.8% | 1.820 | 0.28 |
| the Senate's terms, stage one on the last 3 cycles | 0.765 | 65 / 91 / 98.3% | 1.790 | 0.28 |

- **The result.** z sd and coverage stay within three points of the House's own, and the log score is higher. So the Senate's terms are used for 2008-2012.
- **Fewer cycles for stage one** (the last three rows) match 2008-2012, which have one to three earlier House cycles. Those rows score better still, because a fit on few recent cycles carries the recent race error.
- **Scored directly on 2008-2012** (1,146 races): z sd 0.97, coverage 53 / 82 / 95.2%, log score 1.32, national z rms 1.14. 2008's national swing missed by 1.7 sd.
- **Found, not changed.** The Senate's terms also score better than the House's own over 2014-2024. The House's own terms are kept there, since the orchestrator's item asked only about the early years.

**The fewest cycles.**
- **Why at least four.** A fit of the national terms cannot have fewer than four cycles: three for the terms and one degree of freedom for their spread.
- **Why both parties.** Its cycles must hold presidents of both parties, or the midterm and presidential-year terms cannot both be fitted. A Republican was in office in every Senate cycle of 1982-1992.
  - So the Senate is first forecast in 1996, after 1994 brings a Democratic president into its cycles.
  - Governors are first forecast in 1986, the first year with four earlier cycles (1978-1984, under Carter and Reagan).
- **What the back-test shows.** It was run with fits on only the k cycles before each year, for k = 4 to 12. `backtest.json` keeps the windows of 4, 5, 6, 8 and 10 cycles.
  - *Race forecasts.* No k from four up gives race forecasts that are too narrow.
  - *The national swing* is less well judged on few cycles. Its z rms is 1.1 to 2.8 on four to seven cycles, and about 1 from eight. That matters more to control than to a seat's p.
- **The choice.** Four cycles, with presidents of both parties, is the fewest a fit needs (`K_MIN`). Each year uses every earlier cycle, as D1 and D3 do.

**What the back-test says of the forecasts.**
- **More races finish within 49-51% than the forecast expects.**
  - The House: 113 against 89.3, 2.5 Poisson sds above.
  - The Senate: 30 against 21.6, 1.8 above.
  - Governors: 30 against 30.9.

  The expected count is the forecasts' density near even, summed. So this says that, in aggregate, the model's own p of the House and the Senate is low by up to a quarter where races are close. The history by votes (§5) shows a smaller excess for the House, 108 against 99 within 5,000 votes.
  - A single calibration factor cannot fix this. It narrows every race alike, and most races are far from even, so it lowered the expected count (91.9 to 89.3).
  - Why, is open. The close races' means may be better than the model knows, or the error may not be normal in shape. Round 4 calibrates p for it (§2.6).
- **Seats.** Among contested races, the Democrats' seats fell outside their 80% interval five times in 19 chamber-years:
  - the House in 2008 (219 won, 196.6 expected), 2010 (190 won, 226.6 expected) and 2020 (203 won, 221.5 expected);
  - the Senate in 2006 and 2008 (22 and 19 won, 16.6 and 13.6 expected).

  2008 and 2010 are on the Senate's terms, with stage one fitted on one and two cycles. The reading, not tested: an incumbency term fitted on 2006 and 2008 alone (0.097, 0.094) overstated the Democrats' newly won seats in 2010.

**Marked.** *No polls are used*, so the model's own forecast carries less than forecasters then knew. Where 538's forecast stands first, the polls are in.

### 2.4 Calibration of the spread (round 3, item 3)

**The rule.** For year t, k(t) is the root mean square of z = (y − mean) ÷ sd over the level's earlier years. Each of those years is forecast from its own earlier cycles, before calibration (`chambers.py`, `calibration`).
- It applies when at least three such years exist (`CAL_MIN`); otherwise k = 1.
- It multiplies both the national sd and s_e, so the correlation ρ between races is unchanged.
- *Reason:* the orchestrator's: "the forecast should be as sharp as the record allows and no sharper", and the record used is only what came before t.

**k by year:**
- **House:** 2014 0.984, 2016 0.931, 2018 0.904, 2020 0.897, 2022 0.892, 2024 0.873.
- **Senate:** from 1.049 in 2002 to 0.911 in 2024.
- **Governors:** from 0.965 in 1992 to 0.936 in 2024.

Each year's k is in its file's `model.calibration`.

**Before and after,** on the years calibrated:

| Level | Years | Races | z sd | 50 / 80 / 95% coverage | Log score | National z rms |
|---|---|---|---|---|---|---|
| House | 2014-2024 | 2,286 | 0.770 → 0.846 | 61 / 91 / 98.5 → 57 / 87 / 97.7% | 1.603 → 1.632 | 0.76 → 0.85 |
| Senate | 2002-2024 | 378 | 0.856 → 0.865 | 56 / 89 / 97.4 → 55 / 88 / 98.1% | 1.212 → 1.223 | 0.98 → 0.99 |
| Governor | 1992-2024 | 371 | 0.919 → 0.948 | 57 / 83 / 96.0 → 55 / 82 / 95.4% | 1.099 → 1.101 | 1.33 → 1.39 |

- **Adopted at every level.** Each moves z sd nearer 1, coverage nearer 50 / 80 / 95, and raises the log score.
- **Why z sd stays below 1** (a reading). k is fitted on earlier years, and the race error has kept falling, so each year's k is a little larger than the next year's would want.
- **Two factors**, one for the national part and one for the race's own, were tested (scratch script; the same years):
  - log score 1.627, 1.224 and 1.102 for the House, Senate and governors;
  - national z rms 0.84, 1.10 and 2.60.

  The national factor, fitted on a few years' national misses, went to its floor of 0.5 for governors. So one factor is kept.
- **What calibration does to p.** For a normal forecast, d ln p ÷ d ln sd = z² − 1 at the race's z = (½ − mean) ÷ sd.
  - So narrowing raises p in races within one sd of even and lowers it in safer ones.
  - Most House races are safe, so the House's 2024 sum fell 11% at k = 0.873 (5.97 → 5.32 × 10⁻⁴).
  - Its largest p rose: California 22 went from 1 in 45,994 to 1 in 40,376.

### 2.5 The governors' national swing: the small sample, and one real miss

Round 2's back-test gave the governors' national misses a z rms of 2.45 over 2020-2024, on fits of five to seven cycles (2010 on). Two things made it large:
- **The small sample.** Three years, on fits whose s_a had two to four degrees of freedom. With 1978 on, the national sd of 2020 is 0.020 (calibrated 0.019), against 0.012 before.
- **The yardstick's own noise.** The miss is measured against the year's swing as a fit on every cycle estimates it. In an eleven-race presidential year that estimate has noise of about s_e ÷ √11 ≈ 0.024, as large as the national sd itself. `z_with_year_noise` divides by √(national sd² + s_e²/n_races) instead.

Over 1986-2024 (20 years, 448 races) the z rms is 1.29 with calibration, and 0.91 with the year's noise.

**2020 is a real miss.** The model forecast a Democratic year of +1.7 points among the eleven governors, and the year came out −6.4.
- That is −3.9 national sds, or −2.6 counting the year's noise.
- At least one year in twenty beyond 2.6 sd has a chance of about one in five (P(|z| > 2.56) ≈ 1% a year).
- So the record does not show the governors' national term too narrow overall. 2020 is its one large miss.

### 2.6 Near-tie calibration of p (round 4)

*Since §0.3 a scheme must also pass round 5's cells and the robustness test, which leaves out one scored year at a time. The House's one factor does; the Senate's does not, so the Senate takes no factor and each of its p shows the factor beside it (`near_tie_not_of_record`). The test below is round 4's as it stood.*

*Reason:* the orchestrator's of 07:04, quoted in §0.7.

**The rule.** It is D3's of #31, for the model's own forecast (`chambers.py`, `near_tie_test` and `near_tie`).
- **What it does to the forecast.** The density within one point of ½ (49-51%) is multiplied by a factor F, and the forecast renormalized: Z = 1 + (F − 1)·q, where q is the forecast's own chance of that window.
  - p, the density at ½, is then multiplied by F ÷ Z, recorded as the forecast's `calibration.multiplier`.
  - The forecast's mean and sd are unchanged. So a reader recomputing p from them gets the file's `p.value_uncalibrated`, and that times the multiplier is `p.value`.
- **How F is fitted.** On earlier years only: F makes the expected count in the window equal the count seen, over the earlier years' out-of-sample forecasts. Each of those forecasts is from its own earlier cycles, with k.
- **Whose F.** A level takes its own F where those years expected 30 or more near-ties (D3's minimum, the orchestrator's of 07:37). Otherwise it takes the F of every level's earlier years pooled, again with 30 or more expected. Otherwise no factor applies.
- **The band scheme.** Bands of |mean − ½| are 0-0.05, 0.05-0.10, and 0.10 up. A band takes its own F by level, else pooled over levels, else none. So no safe seat's p is raised on support from closer races.
- **When a scheme is adopted for a level.** It must meet three tests, on the years it reaches:
  - it raises the mean log score;
  - it brings the count within 49-51% nearer the count seen;
  - it does not move the safe seats' count (|mean − ½| of 0.10 or more) further from the one seen.

  Of two schemes that pass, the better log score is adopted.

**The test**, 2010-2024, the years either scheme reaches (`backtest.json`, `near_tie`). Each window cell is expected against seen:

| Level, races | Scheme | Log score | 50 / 80 / 95% coverage | 49-51% | 48-52% | 45-55% | Safe seats, 49-51% |
|---|---|---|---|---|---|---|---|
| House, 3,047 | none | 1.5736 | 56.8 / 86.6 / 97.5 | 78.7 vs 105 | 158.7 vs 209 | 417.1 vs 521 | 13.4 vs 17 |
| | one factor | **1.5743** | 57.0 / 86.9 / 97.5 | 87.5 | 166.6 | 422.6 | 14.5 |
| | by band | 1.5743 | 56.9 / 86.8 / 97.5 | 85.3 | 164.5 | 420.8 | 13.4 |
| Senate, 256 | none | 1.2984 | 54.3 / 91.0 / 98.8 | 11.1 vs 17 | 22.2 vs 34 | 55.9 vs 69 | 2.8 vs 4 |
| | one factor | **1.3017** | 54.3 / 90.2 / 98.8 | 12.1 | 23.2 | 56.6 | 3.1 |
| | by band | 1.2992 | 53.9 / 90.6 / 98.8 | 11.8 | 22.8 | 56.3 | 2.8 |
| Governors, 186 | none | **1.1780** | 59.1 / 86.0 / 96.8 | 12.8 vs 16 | 25.5 vs 31 | 62.1 vs 70 | 1.2 vs 2 |
| | one factor | 1.1752 | 59.1 / 86.0 / 96.8 | 13.7 | 26.3 | 62.8 | 1.3 |
| | by band | 1.1768 | 59.1 / 86.0 / 96.8 | 13.7 | 26.3 | 62.7 | 1.2 |

**What the test shows.**
- **The House and the Senate.** One factor per level passes all three tests and is adopted. The band scheme passes too but scores no better: the same log score for the House to four places with a count further from the one seen, and a lower one for the Senate.
  - In the safe seats' band the one factor moves the House's count from 13.4 to 14.5 against 17 seen, and the Senate's from 2.8 to 3.1 against 4. So the record at their distance supports the raise.
- **Governors.** Both schemes lower the log score, so neither is adopted.
  - In most years their factor would be the pooled one, fitted mostly on House races.
  - Their own earlier years give 0.996 by 2024: 30 near-ties seen against 30.1 expected over 1986-2022.

**The factors.**
- **House.** 2010: 0.886 and 2012: 1.079, both pooled. Then its own: 1.128 in 2014, 1.126, 1.120, 1.220, 1.253 and 1.295 in 2024.
- **Senate.** Pooled throughout, since its own years never expect 30 near-ties: 0.886 in 2010, 1.079, 1.100, 1.120, 1.127, 1.178, 1.199 and 1.229 in 2024.
- **2008 and before.** No factor: the fitting years expected fewer than 30.
- **2010's factor is below one.** The years before 2010 had fewer near-ties than expected, so the rule lowers p in 2010 by about 11%. It is kept, since the rule takes earlier years only.

**What it does not reach.**
- **The wider windows.** The counts at 48-52% and 45-55% stay short, so the excess is not only at the centre.
- **The House's means.** Its results land about 1.5 points nearer ½ than its means, in races 5 to 20 points from even (a reading from the back-test's residuals). Their p may be understated more than any factor at ½ can show. It is open (§7).

**Control.** p for control is the calibrated p times P(decides | tie), which the calibration does not change. The other seats enter the chamber stage under their uncalibrated forecasts. The change is under half a percentage point in a close seat's chance of winning.

### 2.7 Shrinkage of the mean and t4 tails (round 5)

*No longer of record.* After M2's second pass, neither variant survives the robustness test of §0.4, which leaves out one scored year at a time. The figures below are round 5's as it stood. The test's results now are in §0.4 and in `backtest.json` (`variants`, each with `leave_one_year_out` and `robust`).

*Reason:* the orchestrator's of 07:19, quoted in §0.6.

**The variants** (`chambers.py`, `shrink_factor`, `variant_model` and `variant_test`). Each is fitted on earlier years only.
- **none.** The record of round 4: the mean as fitted, normal first, k, and the near-tie factor where adopted.
- **shrink.** mean′ = ½ + λ·(mean − ½).
  - λ is the slope through ½ of the result on the raw mean, over the level's earlier years' raw out-of-sample forecasts (`raw_model`), weighted by 1/sd². That is the normal likelihood's estimate.
  - It needs three such years scored, as k does (`CAL_MIN`); before that λ = 1. So the House has none until 2014.
  - k is refitted on the shrunk means: the RMS of z = (y − mean′)/sd over the same years.
- **t4.** The t4 forecast with the same sd stands first in place of the normal. The normal stands beside it, as the t4 did.
- **both.** Shrinkage and t4 together.

Under each variant the near-tie factor of round 4 is refitted, and its rule re-run (`near_tie_test` with the variant). The pool for a pooled factor is every level's forecasts under the same variant.

**When a variant is adopted for a level.** It must meet three tests against none, on 2010-2024:
- it raises the mean log score;
- it brings the count within 49-51% nearer the count seen;
- in each safe-seat band (|mean − ½| from 0.10 to 0.20, and from 0.20 up), it moves no near-even count (49-51%, 48-52%, 45-55%) further from the count seen. A count is tested where the count seen, or none's expected, is 5 or more.

The bands are by none's mean, so that each band holds the same races under every variant. Of the variants that pass, the better log score is adopted.

**The test**, 2010-2024 (`backtest.json`, `variants`). Each window cell is expected against seen; "near-tie" is the scheme the refitted rule adopts.

| Level, races | Variant | Near-tie | Log score | 50 / 80 / 95% coverage | 49-51% | 48-52% | 45-55% | Passes |
|---|---|---|---|---|---|---|---|---|
| House, 3,047 | none | one factor | 1.5743 | 57.0 / 86.9 / 97.5 | 87.5 vs 105 | 166.6 vs 209 | 422.6 vs 521 | |
| | shrink | by band | **1.6008** | 58.6 / 87.6 / 97.6 | 88.8 | 171.2 | 438.4 | all three |
| | t4 | one factor | 1.5728 | 46.5 / 79.3 / 97.6 | 86.5 | 158.2 | 396.1 | none |
| | both | one factor | 1.6097 | 47.9 / 80.8 / 97.6 | 89.6 | 164.2 | 412.9 | not the safe band |
| Senate, 256 | none | one factor | **1.3017** | 54.3 / 90.2 / 98.8 | 12.1 vs 17 | 23.2 vs 34 | 56.6 vs 69 | |
| | shrink | by band | 1.3208 | 55.9 / 89.8 / 98.8 | 12.4 | 24.0 | 59.3 | not the safe band |
| | t4 | by band | 1.2945 | 41.8 / 81.6 / 98.8 | 10.6 | 21.2 | 53.6 | none |
| | both | one factor | 1.3332 | 46.5 / 84.0 / 98.8 | 12.5 | 23.5 | 57.4 | not the safe band |
| Governors, 186 | none | none | 1.1780 | 59.1 / 86.0 / 96.8 | 12.8 vs 16 | 25.5 vs 31 | 62.1 vs 70 | |
| | shrink | none | 1.1748 | 58.6 / 85.5 / 97.3 | 12.4 | 24.7 | 60.4 | the safe band only |
| | t4 | none | **1.2045** | 50.5 / 78.0 / 97.3 | 13.8 | 27.4 | 66.3 | all three |
| | both | none | 1.1957 | 48.9 / 77.4 / 97.3 | 13.3 | 26.5 | 64.2 | all three |

**The House's safe-seat bands**, expected against seen, with the results beyond the forecast's 5% and 1% quantiles toward ½ (expected 5% and 1% of the races):

| Band | Variant | 49-51% | 48-52% | 45-55% | Beyond 5% toward ½ | Beyond 1% |
|---|---|---|---|---|---|---|
| 0.10-0.20, 1,428 races | none | 14.4 vs 17 | 28.9 vs 37 | 92.7 vs 105 | 57 vs 71.4 | 12 vs 14.3 |
| | shrink | 14.4 | 30.1 | 99.7 | 47 | 12 |
| | t4 | 11.6 | 22.1 | 67.9 | 84 | 6 |
| | both | 12.4 | 23.7 | 73.4 | 70 | 5 |
| 0.20 up, 789 races | none | 0.13 vs 0 | 0.27 vs 0 | 1.24 vs 1 | 42 vs 39.4 | 5 vs 7.9 |
| | shrink | 0.13 | 0.28 | 1.34 | 28 | 4 |
| | t4 | 0.62 | 1.17 | 3.21 | 49 | 2 |
| | both | 0.67 | 1.26 | 3.48 | 34 | 0 |

**What the test shows.**
- **The House: shrinkage.** It passes all three tests, and its log score gain (0.027) is many times the near-tie factor's (0.0007).
  - λ: 1.001 in 2014, 0.979 in 2016, 0.981, 0.947, 0.928, and 0.930 in 2024. So the earlier cycles' fit overstates how far a district's lean carries its result from ½, and more so lately.
  - k refitted on the shrunk means: 0.929 in 2016 down to 0.851 in 2024 (from 0.931 and 0.873).
  - By band, the results land nearer ½ than none's means by 0.4, 1.7, 1.7 and 1.4 points (0-5, 5-10, 10-20 and 20+ points from even). Under shrinkage that is 0.3, 1.5, 1.2 and 0.6: most of the gap remains in the 5-20 point bands, since λ is fitted over every race.
  - "Both" scores better still (1.6097), but in the 10-20 point band all three near-even counts move further from the counts seen. So it fails.
- **The House: t4.** It lowers the log score and moves every near-even count in the 10-20 point band further from the one seen. Its 50% intervals hold 46.5% of the results.
- **The far seats.** The record cannot test p at ½ there: one result within 45-55% of 789. The tails toward ½ are no heavier than normal says: 42 results beyond the 5% quantile against 39.4, 5 beyond the 1% against 7.9. Their spread is wider than the results: z rms 0.85 under none, 0.81 under shrinkage. So nothing here supports t4's much higher p for them. Shrinkage raises them by a median ×1.39 (at most ×16, New York's 13th of 2020 at mean 0.939, 2.5e-21 to 3.9e-20). Its centre is supported (the results land 1.4 points nearer ½ than none's mean), its effect at ½ is not tested.
- **The Senate.** Shrinkage raises the log score (λ 0.98 in 2010 to 0.90 in 2024), but in the 10-20 point band it moves 48-52% from 5.8 to 6.3 expected against 5 seen. "Both" moves 45-55% there from 15.4 to 12.4 against 18. Each fails one tested count, so none is adopted.
- **The governors: t4.** It passes all three tests, and "both" passes too with a lower log score. In the 10-20 point band only 45-55% can be tested (5 seen, 6.48 expected under normal); t4 brings it to 4.6. There are no governors 20 points or more from even in 2010-2024.
  - λ for governors is above 1 (1.025 to 1.098): their results land further from ½ than the means. Shrinkage lowers their log score.
  - t4 first applies to every governor year with the model's own forecast first, 1986-2024. It was chosen on 2010-2024, so for 1986-2008 the choice of tails rests on later years. That is the same kind of choice as the normal before it, which no year tested.

**The near-tie factor, refitted.**
- **The House under shrinkage** adopts the band scheme: log score 1.6008, against 1.6005 for one factor. Its factors are:
  - nearest ½ (0-0.05): 1.164 in 2014, 1.136, 1.098 and 1.204 in 2020, pooled over levels; then the House's own, 1.368 in 2022 and 1.400 in 2024;
  - 0.05-0.10: 1.108 in 2018, 1.073 and 1.093 in 2022, pooled; the House's own, 1.072, in 2024;
  - 0.10 up: none in any year, as those years expect fewer than 30 near-ties;
  - 2010 and 2012: no factor in any band.
- **The Senate** keeps one factor (round 4).
- **Governors**: still none under t4. The rule lowers their log score again (1.2045 to 1.2017).

**Control.** Unchanged in form: calibrated p × P(decides | tie). The House's seats enter the chamber stage at their shrunk means, with the refitted k. Where the governors' p is t4, there is no chamber.

## 3. Structures, and where p is not computed

- **Uncontested** (one candidate on the ballot): p = 0, said so.
- **No Democrat or no Republican among the top two**: not computed, since both forecasts are of a Democrat against a Republican.
  - This covers an independent or minor party second, and two candidates of one party (California and Washington top-two; Connecticut 2006, where Lieberman ran on a Democratic and a third-party line).
  - An independent who caucuses with the Democrats (Sanders, King) stands as the Democrat, as in 538's rows.
- **Runoffs and the legislature.**
  - **Georgia** (a majority is required, else a runoff): not computed with three or more candidates.
  - **Louisiana**'s open primary: not computed.
  - **Ranked choice** in Maine (2018 on) and Alaska (2022 on): not computed.
  - **Vermont governor**, which the legislature chooses if no one has a majority: not computed with a third candidate on the ballot.

  The result is recorded in every case, and 538's forecast is kept where it has one.
- **Algara and Amlani's races (1978-2004).** The source names only the two nominees.
  - Where the others' total is at least the smaller nominee's, an unnamed candidate may have been in the top two, so p is not computed (8 races).
  - Where a nominee had no votes, who the top two were is not known (1 race).
  - Georgia and Vermont with any other votes are not computed, as above.
- **Missouri before 2006.** Algara and Amlani's Missouri rows fall short of Cha's totals by 7% for the Democrat and 2% for the Republican in each of 2008, 2012 and 2016.
  - That is what a missing Kansas City would do: it reports apart from Jackson County. This is inferred, since the rows hold 115 jurisdictions, the 114 counties and St. Louis City.
  - The count is taken as incomplete. Missouri's seven races of 1980-2004 have no p, no fit row and no last-race value.
  - So Missouri 2008, whose last race is 2004's, has no forecast of the model's own either.
- **Missing district input**: no 2020 presidential vote on the 2024 lines in Alabama, Louisiana and North Carolina; none for 2008 on California's 2012 lines; none for 2012 on Florida's 2016 lines.
- **Too few earlier cycles** (§2.3): the House of 2006 (368 contests) and the governors of 1978-1984 (89). 538's files hold neither, so p is not computed, with that reason.
  - Control of the House in 2006 is not computed either, since the chamber stage needs the model's common swing.
  - The chamber check (§4) is still made.
- **No last governor race.** Two races get no forecast of the model's own: Alaska 2006, since Alaska is not in Algara and Amlani, and Missouri 2008.
- **Specials held apart from November.** The November record leaves out specials held on other dates.
  - Cha, Kuriwaki and Snyder hold 42 such House contests and Massachusetts's Senate special of January 2010. They are added with Cha as their record (`certified` null, with no second source) and p not computed, since both forecasts are of November's general election.
  - Their dates are not in the sources read here, except Massachusetts's: 19 January 2010, from Senate.gov.
  - Eight of 2024's are among them (CA-20, CO-04, NJ-10, NY-03, NY-26, OH-06, TX-18, WI-08). The FEC has no 2024 volume, so they come from Cha, as the orchestrator agreed for want of the FEC.

## 4. Control of the chamber (exact form, MATH §4.2)

p(control) = p(seat) × P(the other seats leave control to this one | this seat tied).
- **Each seat** is y_i = μ_i + λ_i·d + e_i. Here d ~ N(0, s_a²) is the common swing (s_a here is the year's calibrated national sd), and e_i ~ N(0, s_e,i²) is the seat's own error. `stage_two.inputs` gives μ_i (`mean`), s_e,i (`own_sd`) and λ_i (`swing_loading`).
- **The common swing is conditioned on the tie**: d | tie ~ N(λ·s_a²·(½ − μ)/sd², s_a²·s_e,i²/sd²), with sd² = λ²s_a² + s_e,i².
- **The other seats' distribution** is computed exactly, by dynamic programming over seats on a grid of the swing. Where the swing given a tie is narrower than three grid steps, the other seats are counted afresh on a fine grid around it. No seat needed it.

**Whose forecast of the seat** (reading (c); *reason:* one forecast of the seat throughout its figure, M2 2.6):
- **The model's own**: its mean, s_e,i = the model's calibrated s_e, and λ = 1.
- **538's**, where 538's p stands first: 538's mean and implied sd are the seat's marginal, with s_e,i = √(sd₅₃₈² − s_a²) and λ = 1, as the presidency treats 538's marginals.
- **Where 538's sd is not above s_a**, no seat can carry the whole swing and keep 538's sd.
  - Such a seat carries λ = sd₅₃₈·√ρ ÷ s_a of the swing, with s_e,i = sd₅₃₈·√(1 − ρ) and ρ the model's own s_a² ÷ (s_a² + s_e²).
  - Its sd stays 538's, and its correlation with the swing is the model's.
  - These seats are marked in `marginal_note`.
- **Each forecast in `p.alongside`** has its own `control`, with P(decides | tie) conditioned on that forecast's mean and sd. The t4 figure uses the normal with the same mean and sd. The other seats are the same for all of them.

What decides control:
- **House:** 218 of 435.
- **Senate:** 51, or 50 with the Vice President, with the seats not up and the independents counted by caucus. A Senate special whose term ends when the new Senate meets (California 2022 and 2024; Illinois 2010, in Senate.gov's words) is not part of control.

**How each seat enters** (`stage_two.inputs.entered_as`):
- *model*: the model's own forecast, sharing the common swing.
- *inferred*: a structure whose p is not computed, entered as the model's two-way forecast.
  - This covers Georgia's runoffs, Louisiana, and ranked choice (King in Maine from 2018 among them).
  - Seats with no earlier presidential vote on their lines use the same day's presidential vote, stated as same-day.
- *fixed*: settled by who was on the ballot, known before the election.
  - Only Democrats on the ballot is fixed D.
  - No Democrat and no caucusing independent is fixed not-D: a same-party top two, a Republican against minor parties, and Osborn and McMullin, who said they would join neither caucus.
  - No seat is ever fixed at its result.

**Seats not up** (Senate): each is held by the winner of its latest election before the year, counted by caucus. Winners come from Cha, Kuriwaki and Snyder from 2006 on, runoffs included, and from MEDSL's Senate returns for seats last elected in 2002 and 2004. Each is listed in `chamber.seats_not_up_list`.

**The check on every chamber-year** (`chamber.check`): the seats not up plus the seats won, against the division the new Congress opened with (Senate.gov; House History). All 20 agree but two, and each of the two is a seat vacant at the opening. The House of 2006 is checked although its control is not computed.
- Minnesota's Senate seat in January 2009, contested; Franken (D) was seated in July. We count 59 against 56 + 2 independents + 1 vacant.
- New York's 22nd in January 2021, uncertified; Tenney (R) was seated in February. We count 213 R against 212.

**The Vice President.** In midterms it is the sitting one: Cheney (R) in 2006, Biden (D) in 2010 and 2014, Pence (R) in 2018, Harris (D) in 2022. In presidential years the VP is elected the same day, and P(the VP is a Democrat) is the presidential chance (§0.9, item 1). It comes from D1's record of the year, in `chamber.vice_president`, with `by`, `as_of` and `note`:

| Year | P(VP Democrat) | Whose |
|---|---|---|
| 2008 | 0.954 | the model's own, on 538's national average of 3 November |
| 2012 | 0.552 | the model's own, on 538's national average of 5 November |
| 2016 | 0.7137 | 538, polls-plus, 7 November; any other ticket counts as not Democratic |
| 2020 | 0.8932 | 538, polls-plus, 2 November |
| 2024 | 0.5295 | the model's own, on the 12 September average (D1's horizon for 2024, M2 3.5), Maine and Nebraska by district (§0.4; 0.5286 with the states whole) |

- **Whose chance.** It is 538's where 538's forecast stands first in D1's record of the year. Otherwise it is the model's own chance that the Democrat wins the College (`pipeline/own_forecast.py`, `college_prob` on the record's unit forecasts): Maine and Nebraska by district as well as statewide where the record forecasts the districts (2024; not 2008 or 2012), as the College is chosen, and a 269 tie counts half.
- **Independence.** It is taken as independent of the Senate's common swing.
- **How far it moves control** is shown in each seat's `P_decides_given_tie_if_VP_D` and `_if_VP_R`.

## 5. Results

| Year, level | Contests | p computed | 538 first | near-tie calibrated | p = 0 | not computed | largest p | largest p for control |
|---|---|---|---|---|---|---|---|---|
| 1978 Governor | 35 | 0 | 0 | 0 | 0 | 35 |  |  |
| 1980 Governor | 13 | 0 | 0 | 0 | 0 | 13 |  |  |
| 1982 Governor | 35 | 0 | 0 | 0 | 0 | 35 |  |  |
| 1984 Governor | 13 | 0 | 0 | 0 | 0 | 13 |  |  |
| 1986 Governor | 35 | 33 | 0 | 0 | 0 | 2 | Wyoming, 1 in 80,892 |  |
| 1988 Governor | 12 | 10 | 0 | 0 | 0 | 2 | Delaware, 1 in 124,851 |  |
| 1990 Governor | 34 | 30 | 0 | 0 | 0 | 4 | Wyoming, 1 in 101,750 |  |
| 1992 Governor | 12 | 9 | 0 | 0 | 0 | 3 | Delaware, 1 in 114,679 |  |
| 1994 Governor | 35 | 31 | 0 | 0 | 0 | 4 | Wyoming, 1 in 86,111 |  |
| 1996 Governor | 11 | 9 | 0 | 0 | 0 | 2 | Delaware, 1 in 170,487 |  |
| 1998 Governor | 35 | 31 | 0 | 0 | 0 | 4 | Rhode Island, 1 in 171,812 |  |
| 2000 Governor | 11 | 9 | 0 | 0 | 0 | 2 | Delaware, 1 in 141,467 |  |
| 2002 Governor | 35 | 33 | 0 | 0 | 0 | 2 | Wyoming, 1 in 79,672 |  |
| 2004 Governor | 11 | 9 | 0 | 0 | 0 | 2 | Montana, 1 in 180,231 |  |
| 2006 Senate | 33 | 31 | 0 | 0 | 0 | 2 | North Dakota, 1 in 131,113 | Rhode Island, 1 in 9,343,171 |
| 2006 House | 438 | 0 | 0 | 0 | 30 | 408 |  |  |
| 2006 Governor | 36 | 33 | 0 | 0 | 0 | 3 | Wyoming, 1 in 104,980 |  |
| 2008 Senate | 35 | 31 | 0 | 0 | 0 | 4 | Wyoming special, 1 in 165,466 | South Dakota, 1 in 3,186,288 |
| 2008 House | 443 | 372 | 0 | 0 | 23 | 48 | New York 13, 1 in 59,057 | Texas 27, 1 in 6,629,139 |
| 2008 Governor | 11 | 9 | 0 | 0 | 0 | 2 | Delaware, 1 in 172,157 |  |
| 2010 Senate | 39 | 33 | 0 | 0 | 1 | 5 | North Dakota, 1 in 118,658 | Delaware special, 1 in 9,341,565 |
| 2010 House | 441 | 402 | 0 | 402 | 10 | 29 | West Virginia 3, 1 in 57,259 | New York 13, 1 in 3,003,249 |
| 2010 Governor | 36 | 32 | 0 | 0 | 0 | 4 | Wyoming, 1 in 82,327 |  |
| 2012 Senate | 33 | 33 | 0 | 0 | 0 | 0 | North Dakota, 1 in 149,911 | North Dakota, 1 in 1,743,852 |
| 2012 House | 441 | 346 | 0 | 346 | 10 | 85 | Texas 34, 1 in 61,244 | Arizona 1, 1 in 13,139,317 |
| 2012 Governor | 11 | 10 | 0 | 0 | 0 | 1 | North Dakota, 1 in 147,500 |  |
| 2014 Senate | 36 | 32 | 32 | 0 | 1 | 3 | Alaska, 1 in 29,076 | Alaska, 1 in 119,757 |
| 2014 House | 440 | 358 | 0 | 358 | 27 | 55 | California 31, 1 in 33,992 | California 21, 1 in 3,706,176 |
| 2014 Governor | 35 | 33 | 0 | 0 | 0 | 2 | Rhode Island, 1 in 105,001 |  |
| 2016 Senate | 34 | 30 | 26 | 0 | 0 | 4 | Nevada, 1 in 116,765 | Nevada, 1 in 556,042 |
| 2016 House | 439 | 345 | 0 | 345 | 22 | 72 | California 21, 1 in 40,292 | California 21, 1 in 4,267,878 |
| 2016 Governor | 12 | 11 | 0 | 0 | 0 | 1 | North Dakota, 1 in 163,506 |  |
| 2018 Senate | 35 | 32 | 30 | 0 | 0 | 3 | Montana, 1 in 95,378 | North Dakota, 1 in 596,519 |
| 2018 House | 442 | 383 | 273 | 110 | 15 | 44 | New Mexico 2, 1 in 33,196 | California 10, 1 in 2,009,316 |
| 2018 Governor | 36 | 34 | 34 | 0 | 0 | 2 | South Dakota, 1 in 59,094 |  |
| 2020 Senate | 35 | 30 | 28 | 0 | 0 | 5 | Alaska, 1 in 87,769 | Alaska, 1 in 707,427 |
| 2020 House | 440 | 399 | 289 | 110 | 10 | 31 | Oklahoma 5, 1 in 49,401 | California 21, 1 in 12,208,000 |
| 2020 Governor | 11 | 11 | 0 | 0 | 0 | 0 | Vermont, 1 in 164,734 |  |
| 2022 Senate | 36 | 32 | 31 | 0 | 0 | 4 | New Hampshire, 1 in 95,632 | Nevada, 1 in 453,746 |
| 2022 House | 444 | 391 | 293 | 98 | 14 | 39 | New Hampshire 1, 1 in 20,079 | New Hampshire 1, 1 in 1,003,563 |
| 2022 Governor | 36 | 33 | 30 | 0 | 0 | 3 | Nevada, 1 in 134,249 |  |
| 2024 Senate | 35 | 33 | 0 | 0 | 0 | 2 | Delaware, 1 in 214,130 | Delaware, 1 in 2,453,710 |
| 2024 House | 443 | 373 | 0 | 373 | 13 | 57 | California 22, 1 in 32,501 | California 22, 1 in 760,344 |
| 2024 Governor | 11 | 10 | 0 | 0 | 0 | 1 | Delaware, 1 in 207,174 |  |

**In all.**
- 5,324 contests.
- 4,106 with p computed, 1,066 of them under 538's forecast.
- 176 with p = 0.
- 1,042 not computed, each with its reason. 457 of them are for too few earlier cycles: the House of 2006 and the governors of 1978-1984.
- 2,142 of the p computed are calibrated to earlier years' near-ties (§2.6): the model's own for the House of 2010-2024. The Senate's 108 were calibrated until round 4's factor failed the robustness test (§0.3). Each now shows beside it what p would be with the factor.
- The near-even note stands on the House's 3,369 p of the model's own forecast. It is taken off the Senate's and the governors' p, since their two tests lean opposite ways (§0.1, item 3).
- Nothing of round 5 is of record (§0.4).

p is under the normal forecast. The other tails and the other forecasts' figures sit beside it in `p.alongside`, each with its own `control`.

**Sums of p, before and after round 5** (round 5's record; §0.4 has this round's). Before is round 4, on `main` at ab34bd0 (#35). Each cell sums p over a level and year's contests; control likewise. The Senate is unchanged (4.4438e-04, control 4.8762e-05).

| Year | House: p before | now | control before | now | Governor: p before | now |
|---|---|---|---|---|---|---|
| 1986 |  |  |  |  | 9.4230e-05 | 1.0712e-04 |
| 1988 |  |  |  |  | 3.4647e-05 | 3.4675e-05 |
| 1990 |  |  |  |  | 7.9517e-05 | 8.0154e-05 |
| 1992 |  |  |  |  | 3.2597e-05 | 3.9282e-05 |
| 1994 |  |  |  |  | 7.9194e-05 | 9.0772e-05 |
| 1996 |  |  |  |  | 2.4488e-05 | 2.3868e-05 |
| 1998 |  |  |  |  | 5.9534e-05 | 5.5222e-05 |
| 2000 |  |  |  |  | 2.7069e-05 | 2.9643e-05 |
| 2002 |  |  |  |  | 8.2682e-05 | 9.3008e-05 |
| 2004 |  |  |  |  | 2.2970e-05 | 2.4350e-05 |
| 2006 | 0 | 0 | 0 | 0 | 7.1799e-05 | 7.4562e-05 |
| 2008 | 8.5538e-04 | 8.5538e-04 | 9.8365e-06 | 9.8365e-06 | 1.8754e-05 | 1.7050e-05 |
| 2010 | 1.3307e-03 | 1.4899e-03 | 2.3063e-05 | 2.5821e-05 | 7.3832e-05 | 8.2316e-05 |
| 2012 | 9.5199e-04 | 8.8720e-04 | 6.0463e-06 | 5.6291e-06 | 2.6378e-05 | 2.9787e-05 |
| 2014 | 1.2003e-03 | 1.1115e-03 | 7.2900e-06 | 6.5897e-06 | 5.2825e-05 | 5.0218e-05 |
| 2016 | 6.8323e-04 | 6.6552e-04 | 7.2812e-06 | 7.3288e-06 | 2.6920e-05 | 3.0543e-05 |
| 2018 | 1.6759e-03 | 1.6755e-03 | 2.5407e-05 | 2.5393e-05 | 8.9209e-05 | 8.9209e-05 |
| 2020 | 1.0768e-03 | 1.0773e-03 | 3.9121e-06 | 3.7915e-06 | 2.0400e-05 | 2.0088e-05 |
| 2022 | 1.7129e-03 | 1.7133e-03 | 3.2612e-05 | 3.2913e-05 | 5.4290e-05 | 5.4053e-05 |
| 2024 | 6.7123e-04 | 7.0208e-04 | 2.6393e-05 | 2.7074e-05 | 1.7919e-05 | 1.7964e-05 |
| **All** | 1.0158e-02 | 1.0178e-02 | 1.4184e-04 | 1.4438e-04 | 9.8925e-04 | 1.0439e-03 |

- **House 2010 and 2012** return to round 3's sums: λ is not yet fitted there, and the refitted near-tie rule has no factor for them.
- **House 2014-2024** take the shrunk mean, with the near-tie factor only within 10 points of even. The far seats' p rises (a median ×1.39 beyond 20 points), the 10-20 point band's moves both ways (×0.88 to ×1.77), and the safe seats lose round 4's factor of 1.12-1.30.
- **Governors** rise where close and fall where safer, as t4 with the same sd does: ×1.26 median within 5 points of even, ×0.86 at 5-10, ×0.66 at 10-20.

**Sums of p, before and after the near-tie calibration (round 4).** Before is round 3, on `main` at c301d58 (#32). Each cell sums p over a level and year's contests; control likewise. "Calibrated" counts the contests whose p is. The governors are unchanged (9.8925e-04 in all).

| Year | House: p before | now | control before | now | calibrated | Senate: p before | now | control before | now | calibrated |
|---|---|---|---|---|---|---|---|---|---|---|
| 2006 | 0 | 0 | 0 | 0 | 0 | 5.1336e-05 | 5.1336e-05 | 1.1552e-06 | 1.1552e-06 | 0 |
| 2008 | 8.5538e-04 | 8.5538e-04 | 9.8365e-06 | 9.8365e-06 | 0 | 3.9762e-05 | 3.9762e-05 | 1.7761e-06 | 1.7761e-06 | 0 |
| 2010 | 1.4899e-03 | 1.3307e-03 | 2.5821e-05 | 2.3063e-05 | 402 | 4.4674e-05 | 3.9908e-05 | 6.6501e-07 | 5.9349e-07 | 32 |
| 2012 | 8.8720e-04 | 9.5199e-04 | 5.6291e-06 | 6.0463e-06 | 344 | 3.8608e-05 | 4.1446e-05 | 3.9862e-06 | 4.2798e-06 | 33 |
| 2014 | 1.0720e-03 | 1.2003e-03 | 6.4949e-06 | 7.2900e-06 | 358 | 8.5495e-05 | 8.5495e-05 | 1.7498e-05 | 1.7498e-05 | 0 |
| 2016 | 6.1260e-04 | 6.8323e-04 | 6.5180e-06 | 7.2812e-06 | 344 | 2.6886e-05 | 2.7120e-05 | 5.3246e-06 | 5.3709e-06 | 4 |
| 2018 | 1.6702e-03 | 1.6759e-03 | 2.5351e-05 | 2.5407e-05 | 110 | 5.1473e-05 | 5.1511e-05 | 4.8993e-06 | 4.9006e-06 | 2 |
| 2020 | 1.0717e-03 | 1.0768e-03 | 3.8916e-06 | 3.9121e-06 | 110 | 4.4368e-05 | 4.4457e-05 | 5.2345e-06 | 5.2429e-06 | 2 |
| 2022 | 1.7124e-03 | 1.7129e-03 | 3.2611e-05 | 3.2612e-05 | 98 | 3.6458e-05 | 3.6504e-05 | 5.1294e-06 | 5.1333e-06 | 1 |
| 2024 | 5.3186e-04 | 6.7123e-04 | 2.0931e-05 | 2.6393e-05 | 373 | 2.2199e-05 | 2.6842e-05 | 2.3260e-06 | 2.8121e-06 | 33 |
| **All** | 9.9032e-03 | 1.0158e-02 | 1.3708e-04 | 1.4184e-04 | 2139 | 4.4126e-04 | 4.4438e-04 | 4.7994e-05 | 4.8762e-05 | 107 |

**Sums of p, round 2 and round 3.** Round 2 is D2-v2, on `main` at b00c55e (#29); round 3 is before the near-tie calibration. The governors of 1978-2004 had no file in round 2.

| Year | House: round 2 | round 3 | control, round 2 | round 3 | Senate: round 2 | round 3 | control, round 2 | round 3 | Governor: round 2 | round 3 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1978-1984 |  |  |  |  |  |  |  |  | (no file) | 0 |
| 1986 |  |  |  |  |  |  |  |  | (no file) | 9.4230e-05 |
| 1988 |  |  |  |  |  |  |  |  | (no file) | 3.4647e-05 |
| 1990 |  |  |  |  |  |  |  |  | (no file) | 7.9517e-05 |
| 1992 |  |  |  |  |  |  |  |  | (no file) | 3.2597e-05 |
| 1994 |  |  |  |  |  |  |  |  | (no file) | 7.9194e-05 |
| 1996 |  |  |  |  |  |  |  |  | (no file) | 2.4488e-05 |
| 1998 |  |  |  |  |  |  |  |  | (no file) | 5.9534e-05 |
| 2000 |  |  |  |  |  |  |  |  | (no file) | 2.7069e-05 |
| 2002 |  |  |  |  |  |  |  |  | (no file) | 8.2682e-05 |
| 2004 |  |  |  |  |  |  |  |  | (no file) | 2.2970e-05 |
| 2006 | 0 | 0 | 0 | 0 | 5.1168e-05 | 5.1336e-05 | 1.0845e-06 | 1.1552e-06 | 0 | 7.1799e-05 |
| 2008 | 0 | 8.5538e-04 | 0 | 9.8365e-06 | 3.9609e-05 | 3.9762e-05 | 1.7509e-06 | 1.7761e-06 | 0 | 1.8754e-05 |
| 2010 | 0 | 1.4899e-03 | 0 | 2.5821e-05 | 4.4840e-05 | 4.4674e-05 | 6.4503e-07 | 6.6501e-07 | 0 | 7.3832e-05 |
| 2012 | 0 | 8.8720e-04 | 0 | 5.6291e-06 | 3.8629e-05 | 3.8608e-05 | 3.9831e-06 | 3.9862e-06 | 0 | 2.6378e-05 |
| 2014 | 1.0883e-03 | 1.0720e-03 | 6.8564e-06 | 6.4949e-06 | 8.5495e-05 | 8.5495e-05 | 1.7482e-05 | 1.7498e-05 | 0 | 5.2825e-05 |
| 2016 | 6.4762e-04 | 6.1260e-04 | 8.0010e-06 | 6.5180e-06 | 2.6970e-05 | 2.6886e-05 | 5.2616e-06 | 5.3246e-06 | 0 | 2.6920e-05 |
| 2018 | 1.6685e-03 | 1.6702e-03 | 2.4589e-05 | 2.5351e-05 | 5.1602e-05 | 5.1473e-05 | 4.8308e-06 | 4.8993e-06 | 8.9209e-05 | 8.9209e-05 |
| 2020 | 1.0702e-03 | 1.0717e-03 | 5.0971e-06 | 3.8916e-06 | 4.4422e-05 | 4.4368e-05 | 4.9942e-06 | 5.2345e-06 | 2.0575e-05 | 2.0400e-05 |
| 2022 | 1.7145e-03 | 1.7124e-03 | 3.1041e-05 | 3.2611e-05 | 3.6584e-05 | 3.6458e-05 | 6.5364e-06 | 5.1294e-06 | 5.3741e-05 | 5.4290e-05 |
| 2024 | 5.9743e-04 | 5.3186e-04 | 2.1313e-05 | 2.0931e-05 | 2.2805e-05 | 2.2199e-05 | 2.2460e-06 | 2.3260e-06 | 1.4931e-05 | 1.7919e-05 |
| **All** | 6.7866e-03 | 9.9032e-03 | 9.6897e-05 | 1.3708e-04 | 4.4212e-04 | 4.4126e-04 | 4.8815e-05 | 4.7994e-05 | 1.7846e-04 | 9.8925e-04 |
| contests with p | 2,246 | 3,362 |  |  | 316 | 316 |  |  | 88 | 420 |

- **Where p is regained.** The House of 2008-2012 (1,116 contests) and the governors of 2006-2016 (128). The governors of 1986-2004 are new (204 contests with p).
- **Where p moves.**
  - Calibration narrows every level's forecast after the first scored years. So the sums fall a little where most races are safe: the House of 2024 by 11%, of 2016 by 5%; the Senate of 2024 by 3%.
  - The governors of 2020-2024 move with the fit from 1978: 2024 is 20% higher.
  - 538's seats are unchanged, but their control moves with the model's calibrated common swing: Senate 2022 falls from 6.54 to 5.13 × 10⁻⁶.

### Historical check (MATH §8.2 iv)

Over all contests with p, the expected number decided by k votes or fewer is computed under the forecast each p used (with its near-tie calibration, where it has one), and set against the number seen (`chambers.py history`, `history.json`). k = 1 is the event itself. Larger k test the same forecasts where there are cases to count.

| Level | Contests | within 1 vote | within 10 | within 100 | within 1,000 | within 5,000 | within 10,000 | within 20,000 |
|---|---|---|---|---|---|---|---|---|
| House, 2008-2024 | 3,369 | 0.020 vs 0 | 0.20 vs 1 | 2.0 vs 1 | 20.3 vs 25 | 101.6 vs 108 | 202.3 vs 192 | 407.4 vs 422 |
| Senate, 2006-2024 | 317 | 0.001 vs 0 | 0.009 vs 0 | 0.09 vs 0 | 0.89 vs 1 | 4.5 vs 5 | 8.9 vs 8 | 17.5 vs 17 |
| Governor, 1986-2024 | 420 | 0.002 vs 0 | 0.02 vs 0 | 0.20 vs 0 | 1.98 vs 1 | 9.9 vs 5 | 19.7 vs 14 | 39.3 vs 39 |

- **House and Senate.** The forecasts pass at every k.
  - The one House race within ten votes is Iowa's 2nd of 2020, at 6 votes.
  - The Senate race within 1,000 is Minnesota 2008, at 312. Within 20,000 the Senate now counts 17, from 18: New Mexico's race of 2012 was 16,258 apart with Barrie's votes added to Wilson's, and is 44,457 apart without them (§0.4).
- **Governors.**
  - The race within 1,000 is Washington 2004, at 129 votes in Algara and Amlani's county sums.
  - Within 5,000 votes, 5 finished against 9.9 expected (a Poisson chance of 7% for 5 or fewer). Within 10,000, 14 against 19.7 (12%). Within 20,000, 39 against 39.3. Over 2006-2024 alone, none finished within 5,000 votes against 4.5 expected (0.011); M2 found the same under round 5's t4 (4.7, P 0.009).
  - Measured by share, the governors are not short: in the back-test, 30 finished within 49-51% against 30.9 expected (§2.3); over 2010-2024, 16 against 12.8 (§2.7).
  - So the shortfall is at fixed vote margins, which weight the small states. Since §0.3 it is written onto each governor p, uncorrected.

## 6. Two sources, differences listed (plan §3a)

**House and Senate.** Every contest in the record is checked against Cha, Kuriwaki and Snyder, and the differences are kept in `checks`. The source of record wins.
- **Most differences** are small candidates (under ten votes) and blank or write-in lines, which the check source leaves out by design.
- **Real ones**: 2024 Missouri Senate (W. C. Young 35,671 at the Clerk, 21,111 in the check), and 2012 AL-03 (Harris 98,141 at the FEC, 91,141 in the check).
- **Matched by name within the contest** since §0.5: a candidate of the record is paired with Cha's candidate of the same last name, and among several of one name with the same votes or else the same first name. The old lookup by last name alone made nine false differences (Utah's Senate race of 2006, Pennsylvania's of 2012 and Missouri's of 2024; House 2006 AR-04, 2008 MI-02, 2010 TX-16, 2012 MS-02, 2018 WA-09 and 2024 SD-AL), and they are gone.
- **Fixed in the record's reading**:
  - A fusion candidate's lines filed under two FEC ids are one candidate's. Connecticut's Senate race of 2010 is the case: Blumenthal's Democratic and Working Families lines now sum to 636,040, as the check has. Each merge is noted in the contest.
  - FEC rows with no candidate are not contests: a "California" row in 2018, and two Ohio rows in 2006.
  - One FEC id under two surnames is two candidates, and a party counts only from a November line (§0.4). Illinois's 3rd of 2022 (Ramirez 177,759 at the FEC) was such a joined line, and now agrees with the check (121,764).

**Governors, Algara and Amlani against Cha, Kuriwaki and Snyder, 2006-2020.** This is the check `algara_amlani.py` writes into its cache, nominee by nominee, on the even and odd years both hold.
- **The count.** 203 elections, with 61 differences, of which 27 are over 0.1%. Two elections are in Algara and Amlani only: Rhode Island 2010 and New Jersey 2017.
- **The large ones:**

| Election | Party | Algara and Amlani | Cha | Difference | Reading |
|---|---|---|---|---|---|
| Missouri 2008, 2012, 2016 | D | 1,560,588; 1,386,582; 1,179,024 | 1,680,611; 1,494,056; 1,277,360 | −7% each | a missing jurisdiction, inferred; Missouri left out before 2006 (§3) |
| Missouri 2008, 2012, 2016 | R | | | −2% each | the same |
| New York 2018 | R; D | 2,207,602; 3,635,340 | 1,926,485; 3,424,416 | +15%; +6% | fusion: Algara and Amlani sum the nominee's lines, Cha counts the party's line |
| Connecticut 2018 | R; D | 650,138; 694,510 | 624,750; 676,649 | +4%; +3% | fusion, the same |
| West Virginia 2012 | D; R | 335,468; 303,291 | 297,207; 273,130 | +13%; +11% | Cha appears low, not settled here |
| Utah 2008 | D; R | 186,503; 734,049 | 175,301; 700,565 | +6%; +5% | Cha appears low, not settled here |
| Maine 2010 | D | 109,087 | 103,387 | +5.5% | not settled here |
| Hawaii 2018 | R | 131,719 | 137,719 | −4.4% | not settled here |
| Louisiana 2011 | D | 182,925 | 288,161 | −37% | the open primary: several Democrats ran, and the check sums Cha's Democrats |

- **The rest** are under 0.7%.
- **The governor files of 2006-2024 keep Cha as the record.** Where the two differ beyond fusion, a third source (MEDSL's precinct files, or the states' own canvasses) is needed to settle which is right (§7).

## 7. Not yet

- **The House of 2006.** It needs an earlier House cycle for stage one. The FEC's 2004 volume is now taken in (§0.1). With The Downballot's 2000 vote on the 2006-2010 lines it would give one, if a source states which states kept their lines from 2004 to 2006. The FEC states Texas's five redrawn districts only, and Wikipedia's API refused the request. Adding 2004 would move every later House p, so it waits for the orchestrator.
- **The House's spread, out of sample.** The House's forecast sd is wider than its results in every year 2010-2024: z rms 0.92, 0.85, 0.75, 0.84, 0.95, 0.97, 0.81 and 0.80 (§0.4's forecasts). k is the RMS of z over all earlier years, and the errors have shrunk since, so k lags. The Senate shows the same (0.57 to 0.93); governors do not (0.72 to 1.36). A k weighted toward recent years narrows the spread and raises the log score, but moves the near-even counts further from the counts seen (§0.2; M2 found the same for the last one to three years). So the near-even shortfall of round 4 (49-51%: 87.5 expected against 105) is not the spread's: as M2 reads it, it sits in the mean (the next item).
- **The House's safer means.** Results in races 5-20 points from even land about 1.5 points nearer ½ than the means. Shrinkage closed part of that gap but does not survive the robustness test (§0.4). A spread that depends on the expected margin (`D2_HETERO`) is another way to test it.
- **The far seats' p.** Beyond 20 points from even the record cannot test p at ½ (§2.7). Shrinkage would raise it (a median ×1.39) and t4 hundreds of times; neither is of record. If the site shows those seats, it should show that their p rests on the normal tail, untested there.
- **The Senate's shrinkage.** On the record without the near-tie factor it raises the log score by 0.022, and fails one tested count by about a race (48-52% in the 10-20 point band: 6.3 expected against 5 seen, from 5.5). It fails on all years, and with 2010, 2012, 2014, 2016 or 2024 left out (§0.3). It is recorded here.
- **Marks in the FEC's November column** other than votes, "Unopposed" and "n/a": "#", "##" and "??" (for example Chad Taylor, Kansas's Senate race of 2014, who withdrew). They are kept as the file prints them, so such a candidate stays on the ballot's count.
- **The Senate's national terms for every House year.** They score better over 2014-2024 too (§2.3). This is a finding only, not adopted.
- **Earlier still.**
  - Algara and Amlani also hold county returns for President (1872 on) and the Senate (1908 on). Their presidential returns would let governor contests reach before 1978. Their Senate returns would extend the Senate's fit, with incumbency from their seat status rather than inferred.
  - Their Missouri rows would need the missing jurisdiction found first.
- **Cha's incumbency codes 2 and 3.** Cha's guide codes an incumbent elected in a special election 2, and a senator appointed by the governor 3. The fit (§2.2), and since §0.5 each contest's `forecast_inputs.incumbency`, count only 1. Among the fit's rows, 2006-2024, that reads as not incumbents 59 House nominees coded 2, 9 Senate nominees coded 2 and 13 coded 3, and 14 governor nominees coded 2 or 3 (Cha uses 3 for governors too; its guide does not say what it means there). Counting them, as (a) codes 1 and 2 or (b) 1 to 3, was tested in §0.2 and is not adopted: the House's log score rises, but at every level the near-even counts move further from the counts seen.
- **Angus King's coding in Cha.** Cha codes King an incumbent (1) in Maine's Senate race of 2012, when the seat was open, and not one (0) in 2018, when he was. Maine 2012's p rests on +1. Maine 2018 has no p (ranked choice).
- **A third source for the governor disputes** of §6: MEDSL's precinct files (2016, 2022 and 2024), or the states' canvasses.
- **Population before 2022.** The ACS table-based files on www2.census.gov begin with 2021. The older sequence-based summary files there hold the same table and are the next step. The Census API wants a key, which needs an email, so it is not used.
- **Odd-year governors**: done since §8, back to 1977; what remains is in §8.6.
- **2026.** Not built: no standardized source holds its count yet (held 2026-11-03). Once one does, the files carry it marked as an unofficial count with its date, until it is certified.

## 8. The odd-year governors (the orchestrator, 2026-11-07 12:01 UTC)

The ask, in the orchestrator's words: "data/governor holds even years only, so KY, LA, MS, NJ and VA are missing, and law 5 asks for as many real contests as true sources allow." *Reason:* "the governor is the most prominent office on those ballots, and the record now skips it every odd year."

### 8.1 Results

`data/governor/1977.json` to `2023.json` (the odd years) hold **60 contests**. They are Kentucky, Louisiana and Mississippi in the years before a presidential election, New Jersey and Virginia in the years after one, and the two other governor contests the sources hold in an odd year (Arizona 1991 and West Virginia's special of 2011).

| Years | The record | Gate |
|---|---|---|
| 2007-2021 | Cha, Kuriwaki and Snyder, as for the even years from 2006 (`certified` true) | Cha's own checks, as before: candidates sum to the total, one winner. All pass. |
| 1977-2005 | Algara and Amlani's county returns summed to the state, as for the even years before 2006 (`certified` null) | No second source, as before. |
| New Jersey 2017 | Algara and Amlani: Cha does not hold it | The same, with a note. |
| Louisiana 2007 | Algara and Amlani: Cha holds only the winner (Jindal, 699,275, the count Algara and Amlani give him too) | The same, with a note. |
| Louisiana 2023 | The Secretary of State's workbook of 2023-10-14, read with D3's `la_sos.py` (`pipeline/intake/la_sos_governor.py`) | D3's gate within the certifying source (11:16). The date is official on the site's list, the 64 parishes add up, and the counts equal the Secretary of State's posted results choice by choice. |

- **Louisiana 2023 is the SoS count.** Landry has 547,827 of 1,062,498 votes over 15 candidates. The posted files it was compared with are byte for byte the ones D3's `data/local/check-la.json` compared (sha256 `099dee9c…` and `5e4134f0…`). No later date of 2023 holds a contest titled Governor, since a candidate had a majority.
- **The cross-check.** On the odd years both sources hold (2007-2019), Algara and Amlani agree with Cha within 0.1% for every nominee, with two exceptions. One is Louisiana 2007 above. The other is Louisiana 2011's open primary, where several Democrats ran (§6).
- **Where the record starts.** Algara and Amlani reach back to 1865. The odd years here begin in 1977, the first odd year whose last presidential vote (1976) and sitting president are in the sources the inputs come from. That is the rule that makes 1978 the governors' first even year (§0.8, item 1).
- **Not in any source read here:** Kentucky and Mississippi 2023 (the file's `not_in_sources`). Cha ends in 2021 and Algara and Amlani in 2019, and both states' own results refused (§9.2). New Jersey and Virginia 2025 are now read from the states' own files (§9.1).
- **Dates.**
  - Kentucky, Mississippi, New Jersey and Virginia vote on the general election day, inferred. The source gives the year.
  - Louisiana's dates before 2023, Arizona 1991's and West Virginia 2011's are not given by the sources, so `date` is null with a note.

### 8.2 Where p is not computed

- **Louisiana, every year.** It elects its governor in an open primary, then a runoff between the two leaders where no one has a majority. The record is the deciding round, either a first round or a runoff. Model §7 computes neither, as for its congressional races.
- **Mississippi, 1979-2019.** Until the amendment of 2020 a governor needed two majorities: "a majority of all the electoral votes, and also a majority of the popular vote". An electoral vote was each county's or House district's, won by the most votes there. Failing both, "the House of Representatives shall proceed to choose a Governor". So one vote can also decide by crossing the popular majority line or by changing a district's electoral vote, and the tie form measures neither (the orchestrator, 12:11).
  - The words are sections 140 and 141 of the Constitution of 1890, as the Legislature's House Concurrent Resolution 47 of 2020 prints them, struck and repealed (`pipeline/intake/ms_governor_rule.py`; source `ms_hc47_2020`).
  - It was read at billstatus.ls.state.ms.us, through D4's `state_law.py` with the certificate chain completed (ruling 08:00). Justia's pages refused curl and WebFetch, and the Secretary of State's page refused curl. The orchestrator was told at once.
  - Under the amended section 140 (a majority, or else a runoff), a race of 2023 or later with three or more names drawing votes would be a first round. Mississippi 2023 is not in the sources.
- **Arizona 1991 and West Virginia's special of 2011.** These are odd-year elections in states that elect their governors in even years. Arizona 1991 is the deciding round of the 1990 cycle: Algara and Amlani hold no Arizona row for 1990 [inferred]. The sources give neither date, and the forecasts are fitted to regular general elections.
- **1977-1983.** These years have too few earlier cycles: the fit needs four even ones.

So p is computed for 29 contests, Kentucky (1987-2019), New Jersey and Virginia (1985-2021). It is not computed for 31.

### 8.3 The forecast: how the route treats an odd year

The route is the governors' D2-v3, as it stands.
- It is fitted on the even years before the odd year: 1978 to the year before, the variant of record (normal), k from the even years' out-of-sample scores before it, and the last governor race as for every governor.
- No odd-year race is a fit row of any year, so no even-year p moves.

The national swing's stage two has two presidency terms: the president's party in a midterm, and in a presidential year. An odd year is neither.
- **The plain route** gives it neither: z = (1, 0, 0). Its swing is the intercept c0, with sd s_a √(1 + z (Z'Z)⁻¹ z′), the even years' spread around their terms, times k.
- **The one odd-year term tested** was fixed in the code before any score (`chambers.ODD_TERMS`, commit 208b810c). It carries the midterm's term to the odd year, z = (1, P, 0), since an odd year is held under the same president.

**The test** is the robustness test of 08:36, on the odd years from 1985 (the first with four even cycles before it) to 2021. That is 38 races in 19 years: Kentucky, Mississippi, New Jersey and Virginia, by the fit rows' rules (`odd_governor_rows`).
- Louisiana is left out (11 races, two rounds), as are the two contests held apart from their state's cycle.
- Mississippi is scored: its share is a forecast like the others, though its p is not computed.
- The term must raise the mean log score with no tested cell further from the count seen, on every scored year and on every set with one year left out.
- A cell is a near-even window (49-51%, 48-52%, 45-55%), over all races and in each band of |mean − ½| by the plain route's means. It is tested where 5 or more are seen or expected.

| | Plain route | The midterm term |
|---|---|---|
| Mean log score | 1.1276 | 1.1627 (+0.0351) |
| z rms (mean) | 0.930 (+0.081) | 0.885 (+0.087) |
| 50 / 80 / 95% coverage | 58 / 82 / 97% | 58 / 82 / 95% |
| 49-51%, all races: expected against 6 seen | 3.12 | 3.03: further |
| 48-52%: expected against 11 | 6.21 | 6.04: further |
| 45-55%: expected against 18 | 14.96 | 14.59: further |
| Verdict | | **fails**: 5 of 7 tested cells further, on every year and with each year left out |

**The plain route stands** (`data/congress/backtest-governor-odd.json`, written by `python3 pipeline/chambers.py odd`).
- The midterm term raises the log score, but it pulls the forecasts further from even, where the record already shows more close finishes than forecast. With so few races, the plain route is what the record supports, as the orchestrator expected.
- On the plain route the odd years' forecasts are about as wide as their results: z rms 0.93.

### 8.4 Control and the lean note

- **Control.** There is none: a governor is one seat (`stage_two` null), as for the even years.
- **The lean note.** It is taken on the odd years' own back-test under the ruling of 11:01, and **both tests count and agree**:
  - (s) within 1 point of ½: 6 seen against 3.1 expected;
  - (v) within 50,000 votes, the smallest of the five lines at which 5 or more are expected: 9 seen against 6.2.
  So each of the 29 odd-year p carries the note, on the model's own normal p: "this route's back-test of the odd-year governor races shows more near-even finishes than it forecast (6 against 3.1 within 1 point, 1985 to 2021), so p may be low."
- **The even-year governors' note stays off** (§0.1, item 3). Their tests are of their own back-test.

### 8.5 What did not change

No file of an even year is rewritten.
- The code's changes for even years are none in effect. `last_pres_year` now also serves odd years and gives the same year for even ones. `national` takes a new branch for odd years only.
- As a check, 1986, 1994 and 2002 were recomputed. Their files differ from the record only in `commit` and the time of the run, and were put back.

### 8.6 Open

*Since 12:35 (§9): Rhode Island 2010 is added; New Jersey and Virginia 2025 are read from the states' own files; Kentucky and Mississippi 2023 were refused. The test above and the note are taken again with 2025's two races (§9.3).*

- ~~**Kentucky 2019.** Cha codes both nominees incumbents (Bevin, and Andy Beshear, whose father was governor until 2015), so `incumbency` is 0 there. Algara and Amlani's seat status says a Republican incumbent. The fit's rule takes Cha's code, and Kentucky 2019's p rests on 0.~~ Fixed: Beshear is not the incumbent (§10.3).
- ~~**Rhode Island 2010** is in Algara and Amlani only, and is not in `data/governor/2010.json`.~~ Added (§9.4).
- **Arizona's 1990 cycle.** It is under 1991 in Algara and Amlani, so `data/governor/1990.json` has no Arizona.
- **Louisiana's dates before 2023**, and its rounds before 2023 against the Secretary of State, would come from the site's own list of elections, which D3's reader takes.
- ~~**Kentucky and Mississippi 2023, and New Jersey and Virginia 2025**, would come from the states' certified files.~~ New Jersey and Virginia 2025 are read (§9.1); Kentucky's and Mississippi's sites refused (§9.2).

## 9. The most recent governors, and Rhode Island 2010 (the orchestrator, 2026-11-07 12:35 and 12:40 UTC)

The ask, in the orchestrator's words: "add the governors no source you read reaches: KY and MS 2023, and NJ and VA 2025. Take each from the state's own certified results (KY State Board of Elections, MS Secretary of State, NJ Division of Elections, VA Department of Elections), by script." The gate is "the one I set for LA 2023, within the certifying source: the result is marked official or certified, its parts (counties or cities) add to its total, and it equals the state's own posted statewide result." And: "Yes to RI 2010." *Reason:* "these are the most recent governor races on the record, and law 5 asks for every one true sources allow."

### 9.1 New Jersey and Virginia 2025: read, and the gate passes

Both are read by `pipeline/intake/state_governors.py` into the cache, and `data/governor/2025.json` is built from it. Each contest carries `gate` and `checks`.

| | New Jersey | Virginia |
|---|---|---|
| The record | The Division of Elections' Official List, "Candidates for Governor For GENERAL ELECTION 11/04/2025", linked from its 2025 page as "Official General Election Results: Governor"; read with D3's `nj_sos.py`, unchanged | The Department of Elections' results site, enr.elections.virginia.gov, which the Department's own results page names for "November 4, 2025 General and Special Elections"; its statewide count for Governor |
| (a) Official | The Official List, dated 12/03/2025 on every page | The election is marked `"isOfficialResults": true` (published 2025-12-01 18:15 UTC; 133 of 133 localities reporting) |
| (b) Parts add up | Each candidate's 21 county lines add up to its Total line | The contest's 133 localities (its counties and independent cities) add up, option by option and write-ins included, to the statewide count |
| (c) The statewide result | The record is the list's own Total lines | The record is the site's own statewide count |
| A further check | The 21 county copies on the same page: each one's lines (its municipalities, and a "Federal Overseas" line in some) add up to its Total line, and that line equals the list's four figures for the county. All 21 agree. | The site's "Election Results" report, precinct by precinct (2,533 precincts): each named candidate's rows add up to the statewide count. They do; the report's write-in cells are empty, so the write-ins are checked on (b) only. |
| Result | Sherrill (Democratic) 1,896,610, Ciattarelli (Republican) 1,417,705, Kaplan 11,880, Kuniansky 8,164; 3,334,359 in all. The list gives no write-in votes. | Spanberger (Democratic) 1,976,857, Earle-Sears (Republican) 1,449,586, write-ins 6,897; 3,433,340 in all |

- **How the Virginia site's files were found.** The site is a script-driven page. Its own scripts (`main-*.js` and the chunks it loads) name the API (`/results/public/api/elections/<jurisdiction>/<election>/data`, and `/data/ballot-item/<id>` for one contest's breakdown) and the reports' address (`/cdn/results/<jurisdiction id>/<file>`) [stated: the site's scripts, read 2026-11-07]. Nothing was guessed, and every file is on the state's own host.
- **Incumbency.** No source read here codes it for 2025. Both seats were open by the rule `chambers.state_gov_incumbency` applies: the winner of each state's last governor contest in Cha (2021: Murphy in New Jersey, Youngkin in Virginia) is neither nominee [inferred: it assumes the 2021 winner still held the office on election day]. So `incumbency` is 0, with `incumbency_source` "inferred" and the rule's words in `incumbency_how`.
- **p.**
  - New Jersey: 1 in 1,308,367 (7.64 × 10⁻⁷). The model's mean is 0.511 for Sherrill and the sd 0.078; she had 57.2% of the two-party vote.
  - Virginia: 1 in 1,344,794 (7.44 × 10⁻⁷). The mean is 0.508 for Spanberger; she had 57.7%.
  - Both carry the lean note (§9.3).

### 9.2 Kentucky and Mississippi 2023: refused, recorded, nothing else tried

- **Kentucky.** The State Board of Elections' 2023 results page, `https://elect.ky.gov/results/2020-2029/Pages/2023.aspx`, answered curl with HTTP 403 and "The request is blocked." at 12:39 UTC. That is the site's own firewall, not this system's proxy.
- **Mississippi.** The Secretary of State's page for the 2023 general election loads. Its results, though, sit in a frame on sos.ms.gov itself (`elections_results_2023_generalG.aspx`), and that page answered curl with HTTP 403 (Cloudflare's "Attention Required!") at 12:39 UTC.
- The orchestrator was told at 12:39, and answered at 12:40: "Right on both: record them and try nothing else." It also said: "MS's frame sits on sos.ms.gov itself, so it stays refused."
  - Neither page was tried again, by WebFetch or another host. A WebFetch would give a summary, not the file, so it could not meet "by script" anyway.
  - On a vendor's host, the orchestrator's rule (12:40): it counts as the state's own result only where a state page that answers names it as where the official results are published, and the vendor's page marks the count official or certified.
- **In the file.** `data/governor/2023.json`'s `not_in_sources` gives each refusal: the page, the time, the answer, and what was tried. `state_governors.py` keeps them as `REFUSED` and does not request them again.

### 9.3 The forecast and the lean note, as in §8

The route is §8.3's, unchanged: the governors' D2-v3 fitted on the even years before the odd year, the plain route z = (1, 0, 0), and the midterm term tested under the robustness test of 08:36.
- New Jersey's and Virginia's 2025 races enter the odd years' back-test by `odd_governor_rows`' rules: one Democrat and one Republican, the two leading. That makes **40 races in 20 years (1985-2025)**, from 38 in 19.
- **New Jersey 2021's last race is now 2017**, not 2013. The index of last races (`last_governor_index`) took Algara and Amlani before 2006 only, so New Jersey 2017, which is in the record from Algara and Amlani (§8.1), was skipped. That was a slip of §8, fixed here. The index now takes Algara and Amlani wherever Cha does not hold a contest. No even year moves: Rhode Island 2010, the only other such contest, was not led by a Democrat and a Republican.
  - New Jersey 2021's p moves from 1 in 1,032,625 to 1 in 1,075,208.
  - Its forecast mean moves from 0.503 to 0.523 for Murphy, who had 51.6%.

| | Plain route | The midterm term |
|---|---|---|
| Mean log score | 1.1356 | 1.1802 (+0.0446) |
| z rms (mean) | 0.926 (+0.113) | 0.869 (+0.104) |
| 50 / 80 / 95% coverage | 55 / 82.5 / 97.5% | 60 / 82.5 / 95% |
| 49-51%, all races: expected against 6 seen | 3.32 | 3.23: further |
| 48-52%: expected against 11 | 6.60 | 6.42: further |
| 45-55%: expected against 18 | 15.90 | 15.49: further |
| Verdict | | **fails**: 5 of 7 tested cells further, on every year and with each year left out |

- **The plain route stands**, as in §8 (`data/congress/backtest-governor-odd.json`).
- **The lean note stands.** Under the ruling of 11:01, both tests count and agree:
  - (s) 6 seen against 3.3 expected within 1 point;
  - (v) 9 against 6.4 within 50,000 votes.

  So each of the 31 odd-year p now carries: "this route's back-test of the odd-year governor races shows more near-even finishes than it forecast (6 against 3.3 within 1 point, 1985 to 2025), so p may be low." The 29 p of §8 are otherwise unchanged, save New Jersey 2021's above.
- **Control.** None: a governor is one seat.
- **A wording fix.** The odd years' forecast source said "an odd year, an odd year: …"; it now says it once.

### 9.4 Rhode Island 2010

- Cha does not hold it, so Algara and Amlani's county sums stand as the record, as for New Jersey 2017. That gives Caprio (D) 78,872, Robitaille (R) 114,879, and the others 148,450 (not named in the source).
- p is not computed. The others' total is above both nominees', so one of the others may be among the top two (`aa_structure`).
- `data/governor/2010.json` gains this contest and the Algara and Amlani source block. Its other 36 contests are unchanged, save `commit`.

### 9.5 What else changed, and what did not

- **A source block now in the 2006 and 2008 files.** `data/governor/2006.json` and `2008.json` name Algara and Amlani as the source of 35 and 8 races' `last_governor_race`, but the files' `sources` left out its block, since the builder rebuilt `sources` level by level from the forecast inputs' other fields. The builder now keeps it. The two files gain the block and nothing else: compared with the record without `commit` and the time of the run, every contest is equal.
- **The Senate and House files of 2006, 2008 and 2010** were rebuilt and recomputed as a by-product. They were equal to the record once `commit` and the time of the run were set aside, and were put back.

### 9.6 Open

- **Kentucky and Mississippi 2023** stay out unless the orchestrator finds a source by the rule of §9.2.
- ~~**New Jersey 2021 in Cha.** Cha codes Murphy as not an incumbent (0), though he won the state's 2017 contest (`data/governor/2017.json`, from Algara and Amlani). It is a slip like the one in Kentucky 2019, where Cha codes both nominees as incumbents (§8.6). The fit's rule takes Cha's code, so New Jersey 2021's `incumbency` is 0. By the record's own 2017 winner it would be +1.~~ Fixed: +1 (§10.3).

## 10. Every governor's incumbency code, against the record's last race (the orchestrator, 2026-11-07 13:06 UTC)

The ask, in the orchestrator's words: "Compare every governor nominee's incumbency code, as your files carry it, with the record's own last race for that seat." Where a nominee won the seat's last regular race and is coded as not incumbent, or the reverse, "find out first whether it is Cha's coding or your join (#45 was a join on last names)", and "fix each one where the record proves it." For a governor who took office mid-term: "Take those from the state's own roster of governors where it answers, or else mark them inferred and leave the code alone." And: "List every code you change and every p that moves." *Reason:* "incumbency is an input to every governor's forecast. One miscode found by chance means we need to know how many others there are."

### 10.1 The check

`pipeline/governor_incumbency.py check` writes `data/congress/governor-incumbency.json`.
- **What is read.** Every governor contest in `data/governor/`, 1977-2025: 613 contests, Louisiana apart. Louisiana has no p, because of its two rounds, and is not in the fit.
- **The nominees.** A nominee is the candidate with the most votes on a Democratic or a Republican line, by the files' own rule (`build_congress.major`). Fusion lines such as New York's "D,WF,Indep" and Minnesota's DFL count; a write-in does not.
- **The codes.** Each nominee's code is taken as the source gives it:
  - Cha, Kuriwaki and Snyder's `inc`, found by the nominee's exact name in Cha's own contest;
  - or, before 2006 and where Cha lacks the contest, Algara and Amlani's seat status.
- **The test.** Each code is set against whether the nominee won the state's previous governor contest in the files. For a state's first contest, that is Algara and Amlani's last race before 1977.
- **Two kinds of disagreement:**
  - A: the nominee won the last race and is not coded 1;
  - B: the nominee is coded 1 (or Cha's 2 or 3) and did not win it.
- **Every name settles.** No case has an unknown last winner, and none matches by surname alone.

**36 disagree: 4 of kind A and 32 of kind B. None is the join's.** For each of the 254 contests whose code is Cha's, the `incumbency` the files carried equals the one Cha's codes give the two nominees found by exact name (`join_check`). So #45's last-name join, `cha_entry`, changes no code. Every disagreement is in the sources' own codes.

**What counts as an incumbent is unchanged.**
- The record counts Cha's code 1 only, and Algara and Amlani's "Incumbent" seat status (§2.2).
- Cha's 2 (an incumbent elected in a special election) and 3 (appointed, in the guide; Cha uses it for governors who succeeded too) read as not incumbents. Counting them was tested in §0.2 and not adopted.
- So a nominee coded 2 or 3 who did sit is coded right by Cha's own guide, and the code is kept. Only codes that are wrong by their own meaning are fixed.

### 10.2 The verdicts

| Verdict | Count | Contests |
|---|---|---|
| **Fixed**: wrong by its own meaning, proven by the record or the state's roster | 5 | §10.3 |
| **Confirmed**: coded the incumbent; the state's roster shows the nominee took office mid-term, before the election | 11 | AL 1994 Folsom; AR 1994 Tucker, 1998 Huckabee; AZ 1978 Babbitt, 1998 Hull, 2010 Brewer; CT 1982 O'Neill; MN 1978 Perpich; NV 1990 Miller; TX 2002 Perry; VT 1992 Dean |
| **Kept**: Cha's 2 or 3, right by Cha's guide, read as not an incumbent (§0.2) | 14 | Code 2: CA 2006 Schwarzenegger (elected in the 2003 recall, which the record does not hold); OR 2018 Brown and UT 2012 Herbert, who each won the special before. Code 3, the roster confirming the nominee sat: AL 2018 Ivey, CT 2006 Rell, SC 2018 McMaster. Code 3, roster refused: MO 2020 Parson. Code 3, no roster read: IA 2018 Reynolds, IL 2010 Quinn, MA 2006 Healey, NY 2022 Hochul, OR 2016 Brown (the special), UT 2010 Herbert (the special), AK 2010 Parnell |
| **Inferred**: coded the incumbent, did not win the last race, and the state's roster did not answer; the code is kept, unproven | 6 | FL 1998 MacKay, NH 1988 McEachern (rosters refused, HTTP 403); WI 1978 Schreiber, WI 2002 McCallum (the connection was reset twice); ID 1978 Evans (Idaho's Blue Book not found, HTTP 404); MA 1998 Cellucci (no roster of the Commonwealth's own found) |

- **The rosters.** Ten answered, read by `pipeline/fetch.py` into the cache:
  - Alabama's Department of Archives and History; Arkansas's Secretary of State; the Arizona Governor's office; the California State Library; the Connecticut State Library;
  - the Minnesota and Texas Legislative Reference Libraries; Nevada's State Library and Archives; South Carolina's Legislative Manual; the Vermont Legislature's list.
  - The words each verdict rests on are in the table, and `gate()` finds every quote in the file as read before the table is written.
- **The rosters that did not answer** (`rosters_not_read`):
  - Florida's Department of State, Missouri's Secretary of State and New Hampshire's almanac on www.nh.gov each answered HTTP 403 at 13:11 UTC.
  - Wisconsin's Blue Book list reset the connection at 13:11, and again on the one retry at 13:16.
  - Idaho's Blue Book was at none of the three addresses a search gave (HTTP 404).
  - The orchestrator was told at 13:14. Nothing else was tried: no other host of a refusing agency (so not floridamemory.com, which is the Florida Department of State's too), and no copy elsewhere.
- **Years only.** Three rosters give years, not days: AZ 1978 (Bolin 1977 to 1978, Babbitt from 1978), AR 1994 (Tucker from 1991) and CT 1982 (O'Neill from 1980). Only Babbitt's could have begun after the election; that he sat in November 1978 is inferred.
- **Not read for code 3.** For the seven nominees coded 3 with no roster read, a roster could not move a p: the record reads 3 as not an incumbent either way.

### 10.3 The five codes changed

| Contest | Nominee | Code in the source | Code of record | `incumbency` | Proof |
|---|---|---|---|---|---|
| NJ 2021 | Murphy (D) | Cha 0 | 1 | 0 → +1 | won the seat's last race, 2017 (`data/governor/2017.json`, from Algara and Amlani) |
| AR 2018 | Hutchinson (R) | Cha 0 | 1 | 0 → −1 | won the last race, 2014 (`2014.json`); Arkansas's roster: served 2015-2023 |
| KY 2019 | Beshear (D) | Cha 1 | 0 | 0 → −1 | Cha codes both nominees 1; Bevin, the Republican, won the last race, 2015 (`2015.json`) |
| VT 2020 | Zuckerman (D) | Cha 1 | 0 | 0 → −1 | Cha codes both nominees 1; Scott, the Republican, won the last race, 2018 (`2018.json`) |
| MN 1982 | Perpich (D) | Algara and Amlani "Democratic Incumbent" | "Republican Open Seat" | +1 → 0 | Minnesota's roster: Al Quie from 1/4/1979, Perpich from 1/3/1983 (his first term from 12/29/1976). In November 1982 the governor was Quie, who did not run. |

- **How they apply.** The fixes apply where the sources are read: `fix_cha` in `chambers.fit_rows`, `chambers.odd_governor_rows` and `build_congress.cha_index`, and `fix_aa` in `chambers.aa_governors` and `build_congress.AA_SOURCE`. Each fix must find its nominee with the code it corrects, or the run stops.
- **In the files.** Each of the 36 contests carries `forecast_inputs.incumbency_check`: the nominee, the code in the source, the verdict, why, and the roster. Minnesota 1982 also keeps the authors' status as `seat_status_in_source`.
- **The rows.** Three of the five are fit rows of the even years (AR 2018, VT 2020, MN 1982), so the coefficients of every later governor fit move. Two are odd-year rows (KY 2019, NJ 2021), scored in the odd years' back-test.

### 10.4 What moved

`pipeline/governor_incumbency.py moves a33c0650` writes `p_moved` in the table: every governor p and model term that differs from the files on main before this change.

**The governors.**
- **Inputs.** `incumbency` moved in the five contests of §10.3, and nowhere else.
- **p.** It moved in 387 of the 451 governor p that are not 0. Every one of them is the model's own; 538's p stand where they stood. Of the model's own p shown beside 538's, 64 moved.
  - The ratios run from ×0.335 to ×1.173, with a median of ×0.9988.
  - Most move by under 1%, through the refitted terms.
- **The contests whose own input moved:**

| Contest | Result (the Democrat's two-party share) | The model's mean for the Democrat | p |
|---|---|---|---|
| KY 2019 | Beshear 50.2% | 0.450 → 0.376 | 1 in 675,441 → 1 in 2,014,771 |
| NJ 2021 | Murphy 51.6% | 0.523 → 0.598 | 1 in 1,075,208 → 1 in 2,221,632 |
| VT 2020 | Zuckerman 28.5% | 0.549 → 0.476 | 1 in 164,734 → 1 in 140,419 |
| AR 2018 | 32.7% | 0.477 → 0.403 | 538's p stands first, unchanged (1 in 23,153,470); the model's own beside it, 1 in 364,115 → 1 in 726,827 |
| MN 1982 | | | no p (too few earlier cycles); a fit row from 1985 on |

- **The next largest moves:** Wyoming 2022 ×0.891, Utah 2024 ×0.944, Montana 2024 ×0.950 and Ohio 2022 ×0.957.
- **The coefficients.** Each year's fit is on its earlier cycles only (`models` in the table).
  - b_inc rises a little in every fit: 1986's from 0.0597 to 0.0604, 2024's from 0.0724 to 0.0735.
  - b_lean rises: 1986's from 0.170 to 0.184, 2024's from 0.298 to 0.302.
  - b_lag falls: 2024's from 0.118 to 0.112.
  - k falls a little: 2024's from 0.936 to 0.926.
- **The even years' back-test** (`data/congress/backtest.json`).
  - The governors' log score of record, 2006-2024 calibrated, rises from 1.1295 to 1.1475.
  - In the incumbency test of §0.2, the record's rises from 1.1780 to 1.2002 (2010-2024). Variants (a) and (b) score 1.2043 each and still fail: the 49-51% count is no nearer (12.7 and 12.4 expected against 16 seen, 12.7 under the record). So the record's reading of Cha's codes stands.
  - No variant, near-tie factor or tails is adopted for governors, as before.
- **The odd years' back-test** (`data/congress/backtest-governor-odd.json`).
  - The plain route's log score falls from 1.1356 to 1.0973. Its two corrected races are close ones that the sitting governor's party did worse in than an incumbent's bid forecasts: Bevin lost by less than a point, and Murphy won by 3.
  - The midterm term still fails: log score 1.1562, a gain of +0.0589, but its tested cells move further. So the plain route stands.
  - The lean note stands, with new counts: 6 against 3.2 expected within 1 point, and 9 against 6.2 within 50,000 votes. The 31 odd-year p carry it.
- **The even years' near-even counts** (`data/congress/history.json`, 2006-2024): 9.05 expected against 4 seen within 10,000 votes, from 9.03. The note's tests are M2's counts (§0.1), not recomputed here, and the governors' note stays off.

**The House: its near-tie scheme changes, and 2,142 House p move.** This was not foreseen when the work was asked.
- **How.** The near-tie factor is fitted on the level's own earlier years. Where those have too few expected near-ties (30), it is fitted on every level's earlier years pooled (§2.6). The governors' forecasts are in that pool, so they reach the House's first years and its safest band.
- **The margin.** Both schemes pass the robustness test for the House, and the one with the higher log score stands (§0.3).
  - Before: one factor 1.578535, by band 1.578513.
  - After: one factor 1.578538, by band 1.578556.
  - So the scheme of record moves from one factor to the band scheme, on a margin of 0.00002.
- **What moves.** 2,142 of the House's 3,369 p move, all of them the model's own; 538's p, where they stand first, do not.
  - The medians by year: ×1.13 in 2010, ×0.93 in 2012, ×0.89 in 2014, 2016 and 2018, ×0.82 in 2020, ×0.80 in 2022 and ×0.77 in 2024.
  - The seats with |mean − ½| of 0.10 or more now take no factor in the years where that band has too few expected near-ties. Before, every seat took the one factor.
  - The House's near-even note now reads 85.7 expected against 105 seen within 1 point, from 87.5.
  - The chambers' control figures (`chamber`) do not change in any year.
- **The Senate.** No Senate p moves. The factor that is taken out and shown beside each p (`near_tie_not_of_record`) moves a little through its pooled years (2018: 1.1280 to 1.1287).
- **Unchanged files.** The Senate's files of 2006 and 2008 and the House's of 2006 came out equal, apart from `commit` and the time of the run, and were put back.
- This is the rule as it stands, applied. Whether a scheme of record should change on so small a margin is open (§10.5).

### 10.5 Open

- **The successors.** Cha codes one successor 1 (Brewer, Arizona 2010) and ten 3 (Ivey, Rell, McMaster, Parson, Reynolds, Quinn, Hochul, Brown 2016, Herbert 2010, Parnell). It also codes Healey 3, who did not win the last race; no roster was read for her.
  - Under the record's reading, Brewer counts as an incumbent and the other ten do not.
  - Algara and Amlani count a successor as the incumbent (Perpich 1978, Perry 2002, Dean 1992 and the rest of §10.2's confirmed).
  - So the fit reads a successor as the incumbent before 2006 and, Brewer apart, not after. Counting Cha's 3 was tested in §0.2 as variant (b) and not adopted; a variant that counts only the successors the rosters confirm was not tested. That is the orchestrator's call.
- **The inferred six** would be settled by Florida's, New Hampshire's, Wisconsin's, Idaho's and Massachusetts's rosters. MacKay and McEachern are coded incumbents though the last race's winner, who did not run, may still have sat; no source read here says.
- **The House's near-tie scheme** moved from one factor to the band scheme, on a log-score margin of 0.00002 that the governors' corrected codes tipped (§10.4). Both schemes pass. The rule takes the higher score, and that moves 2,142 House p by ×0.77 to ×1.13. Whether a scheme of record should change on so small a margin, or stay until another wins by more, is for the orchestrator.
- **What the check cannot see.** A successor whom the source codes as not an incumbent can be found only from every state's roster, since the last race shows who won it, not who sat after.
