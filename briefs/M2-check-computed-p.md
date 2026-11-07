# Brief M2: Check every computed p, and the model's own forecasts, against the model

*Written 2026-11-07 04:36 UTC by the orchestrator. Model: **Fable 5.1**, effort **xhigh**. Read `briefs/_COMMON.md` whole first; it is part of this brief. Fable because the project instructions put breaking and math checks on Fable, and every number the site shows rests on these. xhigh because every thread runs at xhigh, and max only on the maker's word.*

## Your sub-end

**Say, with a script that shows it, whether each p in `data/` is what the model says it is, from the contest's own inputs, and whether the forecasts it rests on are honest, so that nothing goes on the site that the model does not support.**

*Why it matters:* law 8 (true things from true sources) and law 4 (the exact computation sits behind every number). The site does not compute p for real contests; it reads it from `data/` (plan §3). So an error here goes straight to a reader. Two workers built these files, each checking its own work. An independent check is the one the model's own figures had from M1 and B1, and plan §4 calls for it before anything is shown.

## Read first, whole

- `model/MODEL.md` and `model/MATH.md`. They are the standard; you check against them, you do not change them. Where the model itself is wrong or silent, say so (`_COMMON.md` 2, 11).
- `plan/PLAN.md` §3 (the layout), and `data/README.md` (every field).
- `data/president/REPORT.md` (D1) and `data/congress/REPORT.md` (D2), whole. They list their own open findings; start from those.
- `pipeline/` to see what was done. Do not import it for your check (below).

## What to do

Work in this order. The presidency is first because it is final on `main` (#23). Senate control is last, because D2 has one change still to make there (the Vice President's tie vote, now set at one half, is to become the presidential chance).

1. **Recompute every p from its contest's own inputs**, by your own implementation of the model's formulas, with numpy or scipy. Do not import `pipeline/` or `model/math/common.py`. *Reason:* a check that runs the same code finds nothing that code gets wrong. For each contest, take n, the forecast's mean, sd and tails as recorded, compute p and the event, and compare. Do this for every contest in `data/`, not a sample. List every mismatch beyond a tolerance you state and justify. Check too that:
   - the event is exactly twice p;
   - the exact sum and the density agree where the code switches between them (below 1,000 voters, or n·sd² under 6.25);
   - every contest without p gives a reason, and every p names its forecast, script and commit.
2. **The second stage.**
   - The Electoral College, W given a tie in the unit: recompute it independently for at least 1984, 2000, 2016 and 2024, including Maine's and Nebraska's districts, by a method other than D1's.
   - Control of each chamber, P(decides given the seat is tied): check the exact form (MATH §4.2) for a sample of chamber-years, the House and the Senate.
   - Under 538, control is 538's seat p times our P(decides given a tie). Say whether that mixing of two forecasts is coherent, and what it does to the figure.
3. **The forecasts the p rest on.** The model's own forecast decides most numbers. Check each worker's method and back-test, as written in the reports, and say what is wrong or overstated:
   - **The governors.** D2 finds no governor race of 2006–2024 within 5,000 votes against 4.4 expected (a chance of 1.3%), and 61% of races inside the 50% interval. Find the cause, and give the orchestrator the options for a fix, with what each does to the governor p. Do not apply one.
   - **Leave one cycle out** (D2). Its coefficients come partly from later cycles, which no voter knew before the election. Refit on earlier cycles only, and report how much p changes, by level and cycle.
   - **The presidency** (D1). The national and state errors are fitted on earlier cycles only. 2024 uses 538's average of 12 September, the last one reachable, with errors fitted to the 9 September averages of earlier cycles. Check that the horizon matches, and that the t4 scale is the sd ÷ √2.
   - **538's implied sd**, (mean − ½) ÷ Φ⁻¹(chance), is kept only where its estimated error is under 20%. Check the error calculation, including the run counts inferred from the step.
4. **The checks against published figures.** Try to explain what the reports leave unexplained:
   - The Economist's ratio of our p to its `p_decisive_vote`, 2020, runs from 0.14 (Ohio) to 1.32 (Arizona), with several gaps larger than their sampling error.
   - Gelman, King and Boscardin, 1992: ours averages 1 in 45.6 million against about 1 in 20 million.
   - Gelman, Silver and Edlin, 2008: ours is lower in the close states and higher in California.

   Say for each one which is likelier right and why. Where you cannot tell, say what would settle it.
5. **The record against the forecasts** (MATH §8.2): for the presidency as D2 did for Congress, the number of contests decided by k votes or fewer, expected against seen.
6. **The figures a reader will see first.** Recompute by hand, in your report, the closest states of 2024, 2020, 2016 and 2008, the average voter's p in each year D1 reports, and the closest House and Senate races. These are the ones the first screen is likeliest to use.

## Path and constraints

- **Write** `checks/M2-REPORT.md`: a findings table (the claim or figure, your verdict, the correct value, the script line), then your reasoning. Put your scripts in `checks/m2/`, with their output in `checks/m2/OUTPUT.txt`, so that every number in the report is reproduced by a run. Touch nothing else.
- **You change no data and no pipeline.** Say what is wrong and what the right value is; the orchestrator decides the fix and a data worker applies it. *Reason:* one owner for each file (`_COMMON.md` 9). A checker that fixes what it checks leaves nothing checked.
- **Choose nothing for the site** (`_COMMON.md` 3). Where two readings are defensible, give both with what each implies.
- **Subagents:** Sonnet 5.5 at xhigh to re-read a published figure at its source, with `_COMMON.md` 6, 7 and 13. The checking is yours.
- **Branch.** Work on your own branch from `main`. Merge `main` into it when it moves, since D2's Senate change will land while you work. Open one pull request when the presidency is checked, and update it as you go. Push every turn (`_COMMON.md` 8, 9).
- **Escalate** to the orchestrator, never the maker (`_COMMON.md` 11). If you find a p that is wrong by more than a factor of two, tell the orchestrator at once, before you finish the rest.

## Done when

Items 1 to 6 are answered in `checks/M2-REPORT.md` for every level now on `main`, the scripts reproduce every number, the pull request is open, and you have reported to the orchestrator in at most fifteen lines. Then stop (`_COMMON.md` 14). The levels D3 brings (state legislatures, local races, primaries, measures, and races that fill several seats) are a second pass, on the orchestrator's word.

## Amended 2026-11-07 07:44 UTC: the second pass

*The orchestrator's word for the second pass, which the "Done when" above leaves to it. Reason: since #26, D2 has rebuilt Congress and the governors four times (#29, #32, #35, #38: earlier cycles only, the governors' last race, the near-tie factor F, the mean shrunk toward ½, t4 tails for the governors), and D3 has brought every other level (#25, #28, #30, #31, #36, #37). None of it has had a check by a script that does not share its code, and every figure on the site is read from these files.*

Work on a new branch from `main`, extending `checks/m2/` and adding a section to `checks/M2-REPORT.md`. In this order:

1. **Congress and the governors, as they stand after #38.**
   - Recompute every p from its recorded inputs, as before: `value_uncalibrated` from the forecast's mean, sd and tails, then `value` with the near-tie factor in D2's form (the density within 1 point of ½ multiplied by F and renormalized; `data/congress/REPORT.md` §2.6). Check that each F is the one its year's earlier-only fit gives.
   - The shrinkage: check that each shrunk mean is ½ + λ(mean_unshrunk − ½) with the λ D2 reports for its year, fitted on earlier years only.
   - Control: `c3_chambers.py` must read `stage_two.inputs.own_sd`, `common_swing_sd` and `swing_loading`, which the files now carry. Recompute P(decides given a tie) for a sample of House and Senate years, under the model's own forecast and under 538's reading (c), including the 23 marked seats, and the Senate with the Vice President's tie vote at the presidential chance.
   - Re-run your governor test of #26 (no race within 5,000 votes against 4.4 expected): did adding the last governor race and t4 cure it?
2. **The back-tests D2 used to adopt or reject each change** (REPORT §0.1, §2.6, §2.7): are the log scores and cells reproduced, is each fit on earlier years only, and was the rule "adopt only if the out-of-sample test improves" applied as written? Say where a decision would flip.
3. **The spread factor k.** D2 finds the House's sd wider than its results in every year 2010–24 (rms z 0.75–0.92) and suspects that k, averaged over all earlier years, lags shrinking errors. Give the reading, with what a recent-years k would do to p; choose nothing (`_COMMON.md` 3).
4. **D3's levels**, every p in `data/state-upper/`, `data/state-lower/`, `data/local/` and `data/measure/`: the like-race forecast (D3-v1.1), the calibration of #31, and the measures' threshold form, Yes ≈ (1 − t)·f(t)/n (MODEL §7), each by your own implementation. Every contest, not a sample, since a script makes them cheap.

Report to the orchestrator in at most fifteen lines when items 1 and 2 are done, and again at the end. Open one pull request and update it as you go. A p wrong by more than a factor of two goes to the orchestrator at once, as before.

## Amended 2026-11-07 10:54 UTC: the third pass

*The orchestrator's word for a third pass, which your report of 10:54 leaves to it. Reason: since the second pass's last recheck (#59), D3 has computed or released new p (#60, #62) and changed which contests a route takes (#60), and every p the site shows is to be checked by you before it is shown (this brief, items 1 to 6). A check that cannot run on today's files checks nothing of today's.*

Work on a new branch from `main`, extending `checks/m2/` and adding a section to `checks/M2-REPORT.md`. In this order:

1. **Make the first pass run on today's files.** `run_all.sh` should run c1 to c15 on current `main`; fix c1 to c7's reads (c3's renamed input key and any others), changing what they read, never what they test. Report any number that differs from the run of record at d11cae2.
2. **#60, the deciding rounds.** Your item 4 asked which reading the State Board's route should take for the 35 November contests after a nonpartisan primary: the orchestrator ruled at 09:53 (a November contest after an earlier round of the same contest that year is its deciding round, odd or even year; computed by the route's classes, marked; the earlier round not computed), and #60 applies it. Check that the two routes now agree on every such contest, and recompute their p.
3. **#61, route (c)'s size bins.** Reproduce the robustness test's numbers (legislatures' deviance 105.8 to 45.0; the 49 to 51% total 3.4 under to 11.4 over; 8 of 33 cells further; fails with each year left out) and confirm no p of record changed.
4. **#62, Louisiana 2024.** Check the gate of the Secretary of State's workbooks against D1 and D2, the deciding-round pairing (March to April, November to December), and recompute the 9 new p and the measures' note (52 against 36.4).
5. **As they land:** D3's NJ county gate (the orchestrator's ruling of 10:45: 0.5% by county, a duplicate-row scan, a precinct ceiling, 5 contests against the clerks' own results) and the Louisiana follow-up (2023, party committees). Check each gate's numbers and recompute a sample of each one's p.

Report in at most fifteen lines when 1 to 4 are done, and again at the end. One pull request, updated as you go. A p wrong by more than a factor of two goes to the orchestrator at once.
