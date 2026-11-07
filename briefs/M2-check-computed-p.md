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
