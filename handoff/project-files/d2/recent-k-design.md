# D2: the next round, a recent-years k and Cha's incumbency codes (run 09:30 UTC; nothing adopted)

*Result, 2026-11-07 09:40 UTC (PR #55; `data/congress/REPORT.md` §0.1).* On the orchestrator's word of 09:03, only the half-life k of Part 1 was run, since M2 had already tested the last three years. The record is D2-v3, not round 5's, which no longer stands. Then (a) and (b) of Part 2 were run. All were scored under the robustness test of 08:36. None is adopted at any level. They raise the House's log score, but they move its near-even counts further from the counts seen.

*Worker D2, 2026-11-07 07:45 UTC. Written on the orchestrator's word of 07:43: "Write up the design now if you like; don't run it." It runs only when the orchestrator says so, after M2's second pass.*

*Amended 08:25 UTC on the orchestrator's word of 08:20: test Cha's inc 2 and 3 in the same round, beside the recent-years k, with two variants fixed before any score (Part 2). Hold until M2's report.*

# Part 1. A recent-years k

## Why

After round 5 the House's forecast sd is wider than its results in every year 2010-2024: z rms 0.92, 0.86, 0.75, 0.83, 0.92, 0.89, 0.82 and 0.76 (REPORT §7). The Senate shows the same (0.57 to 0.93). Governors do not (0.72 to 1.36).

k is the RMS of z over all of a level's earlier scored years, so the noisier early years hold it up after the errors have shrunk. A spread that is too wide puts too little density at ½, which matches the near-even shortfall (House 49-51%: 88.8 expected against 105 seen).

## What would be tested

Everything stays on the variant of record: the House shrunk, the governors with t4 first, the Senate as it is. λ is not changed. Each k_T below is fitted on years before T only.

1. **Last three.** The RMS of z over the last 3 scored years before T. 3 is CAL_MIN, so no new constant is introduced.
2. **Weighted.** The RMS of z with weight 0.5^((T − T′)/4) for year T′, a half-life of two cycles, over every earlier scored year.

Both are fixed now, before any score is seen, so the choice is not tuned on the test years. No third variant is added after seeing results.

For the House, z is taken on the shrunk means. Under each candidate the near-tie factor and its rule are refitted, as in round 5, since F rests on the earlier years' forecasts of record.

## How it would be scored

The years are 2010-2024, out of sample, against the record of round 5 (`variant_test`'s machinery, with k as one more variant). The scores are:

- mean log score;
- 50/80/95% coverage;
- expected against seen at 49-51%, 48-52% and 45-55%;
- the same counts by band of |mean − ½| (0-5, 5-10, 10-20 and 20+ points, banded on the record's mean);
- the results beyond the 5% and 1% quantiles toward ½, in each band.

## Adoption

A candidate is adopted for a level only if it does three things:

- raises the mean log score;
- brings the 49-51% count nearer the count seen;
- moves no near-even count further from the count seen, in either safe-seat band (10-20 and 20+ points). A count is tested where the count seen, or the record's expected count, is 5 or more.

If both candidates pass, the one with the better log score is adopted.

The far seats are the case to watch. A narrower sd lowers their p, which the near-even counts there cannot test (1 of 789 House results within 45-55%). The tail counts toward ½ will be reported beside the test, as in round 5.

## What it would report

- k by year, before and after.
- z rms by year, after.
- The sums of p and control before and after, by level and year, and by band.
- The largest p.

# Part 2. Cha's incumbency codes 2 and 3

## Why

Cha's guide codes `inc` 0 (not an incumbent), 1 (an incumbent), 2 (an incumbent elected in a special election) and 3 (a senator appointed by the governor). The fit (`chambers.fit_rows`) and, since #45, each contest's `forecast_inputs.incumbency` count only 1. Among the fit's rows, 2006-2024, that reads as not incumbents:

- 59 House nominees coded 2;
- 9 Senate nominees coded 2 and 13 coded 3;
- 14 governor nominees coded 2 or 3 (Cha uses 3 for governors too; its guide does not say what it means there).

The orchestrator (08:20): "an incumbent elected in a special is an incumbent by any plain reading, and an appointed senator holds the seat too. So test it rather than assume it." Counting them changes every p through the refit, so it goes through the same out-of-sample test as any other change to the forecast.

## The two variants, fixed now

- **(a)** inc 1 and 2 count as an incumbent.
- **(b)** inc 1, 2 and 3 count.

Each applies the same definition in both places: the fit's rows, and each contest's `forecast_inputs.incumbency` (the nominee's Cha code, as since #45). Nothing else changes. The Senate's rows of 1982-2004 (MEDSL, incumbency inferred) and the governors' before 2006 (Algara and Amlani's `seat_status`) keep their own definitions; Cha does not hold them.

Under each variant everything is refitted on earlier years only, as the record is: the coefficients (b_inc among them), k, λ (House) and the near-tie factor and its rule.

## How it is scored and adopted

The same scores as Part 1 (log score, coverage, near-even counts overall and by band, tails toward ½), years 2010-2024, out of sample, by level.

1. **Alone.** Each of (a) and (b) on the round-5 record with the k of record, against that record.
2. **With the chosen k.** If Part 1 adopts a k for a level, each of (a) and (b) with that k, against the record with that k.

The adoption rule is Part 1's: raise the log score; bring the 49-51% count nearer the count seen; move no tested safe-band count (10-20 and 20+ points, tested where seen or expected is 5 or more) further from the count seen. If both pass, the better log score is adopted.

The decision is taken in the setting the site will use: step 2 where a k was adopted for that level, step 1 otherwise. The other setting's scores are reported beside it. Where the two settings disagree on whether a variant passes, both are reported and the round stops for the orchestrator.

## What it reports

- b_inc by year and level, before and after, with its standard error.
- Which contests' `forecast_inputs.incumbency` change, and their p before and after.
- The scores of every variant in both settings.
- The sums of p and control, by level and year, and the largest p.

# Then

The round stops for M2.
