# Brief D3: State legislatures, local races, primaries and ballot measures, by script

*Written 2026-11-07 by the orchestrator. Model: **Opus 5.5**, effort **xhigh**. Read `briefs/_COMMON.md` whole first; it is part of this brief. Opus because this is data modelling: almost no race at these levels has a published forecast, so the model's own forecast decides nearly every number (`PROJECT-INSTRUCTIONS.md`).*

## Your sub-end

**Take in, by script from standardized sources, every state legislative race, local race, primary and ballot measure the sources allow, at every level and as far back as they go; compute p for each the model can compute; and write them in the plan's layout, so the site can show where one vote matters most, with every figure's source.**

*Why it matters:*
- Law 1a: the site shows the cases against the maker's claim, and these are where p is largest and B\* smallest (model §2: a 2,000-voter town race at 52-48 has B\* of about $4,150 to $5,630).
- Law 5: "a reader sees p grow as contests shrink".
- The maker, 03:13 (`RULINGS.md`): "aggregating absolutely as much data as we can find", through "an intake flow that doesn't use as many tokens", with standardized data and no live data. The volume is itself part of what the site shows. These levels hold most of the country's contests.

## Read first, whole

- `model/MODEL.md` §3, §7, §9 and §10, and `model/MATH.md` §0, §1, §6 and §7.
- `model/math/common.py` and `pipeline/core.py` (D1's).
- `plan/PLAN.md`: §2, §3 and §3a are your layout and your method.
- The source inventories D1 and D2 have written, `data/sources/*.md`, and `research/historical-close-races-v2.md` (Klarner's state legislative data).

*Reason:* the model is approved; you compute it, you do not change it. Where it is wrong or silent, say so and do not work around it (`_COMMON.md` 2, 11).

## What to do

1. **Inventory first** (`_COMMON.md` 4). Start from `data/sources/*.md` and extend it in `data/sources/local.md`. List every standardized dataset of returns at these levels. For each, give its publisher, its coverage (levels, years, states, contest or precinct), its format, its licence, and whether this environment reaches it. These are leads to check, not facts:
   - MEDSL's precinct returns on GitHub, which include state legislative, local and measure contests for recent cycles;
   - Klarner's state legislative returns;
   - OpenElections' state repositories;
   - the Local Elections in America Project;
   - the California Elections Data Archive;
   - state election offices' bulk downloads.

   Then choose, and say why in your report. Rank the sources by contests covered per script written.
2. **One intake script per source**, `pipeline/intake/<source>.py`, as plan §3a says:
   - download to a cache outside the repository;
   - check row counts and totals against a published total where one exists;
   - convert into the layout of plan §3, with the source block filled from the file's own metadata.

   Where two sources cover one contest, read both, list the differences, and let the certified one win. *Reason:* a year, a state or a source then costs a run, not a reading.
3. **The model's own forecast** for these races (model §3, "Which forecast"). Fit it to like past races from what was known before the election: the same seat's last result, the place's presidential vote, incumbency, and the spread of past margins, as Mulligan & Hunter did. **Propose the method to the orchestrator, with its back-test, before you compute p with it**, and keep taking data in while you wait. *Reason:* the method decides nearly every number here.
4. **Compute p** with `p_contest` from `pipeline/core.py`. It gives the exact sum below 1,000 voters (model §3), and you never write a second version of it. Then:
   - **Primaries with three or more candidates:** p between the top two, which is checked and sound (model §7).
   - **Ballot measures:** the threshold formula, Yes ≈ (1 − t) f(t) ÷ n and No ≈ t f(t) ÷ n, with the threshold read from the measure's own law (model §7).
   - **Races that fill several seats** ("vote for three"): computed at the boundary between the last winner and the first loser, and marked as the model's own, not yet checked (model §7). M2 checks them.
   - **Runoffs, ranked-choice races and uncontested races:** recorded with their results, and p marked as not computed, with the reason (model §7). An uncontested race has p of zero, said so.
   - **The recount zone in small races:** check where the zone a recount can swing comes near the forecast's spread in votes, and report where p would change (model §3, the drivers table; §10).
5. **Check against the record:** how often races like these ended tied or one vote apart, against what your p implies. Klarner's 52 of 109,093 state legislative contests from 1968 to 2022 are a starting figure (model §4).
6. **Write** your data in `data/state-upper/`, `data/state-lower/`, `data/local/`, `data/primary/` and `data/measure/`, in files by year and state, and `pipeline/local.py`. Sources, method and checks go in `data/local/REPORT.md`.

## Path and constraints

- **Branch and pull requests.** Work on your own branch from `main`. Open one pull request per source or level as each is done, with the state legislatures first. Push every turn.
- **Your files.** Touch only your own directories and scripts, plus new fields in `data/README.md`. D1 owns `pipeline/core.py`; D1 and D2 own their levels.
- **Raw files.** Keep raw files out of the repository unless they are small and licensed for it. Record each URL and when you read it (law 8). A committed sample of each script's output is enough to check it.
- **Figures.** Take no figure from memory (OPERATIONS §3). Mark a figure you could not read at source, or leave it out.
- **Network.** If a host is refused, record it and tell the orchestrator. Do not route around it (`_COMMON.md` 6).
  - web.archive.org is refused.
  - Datasets behind a guestbook asking for a name and email (MEDSL's Dataverse files, perhaps others) are an outside party, so they are the maker's call (law 10). List them, and do not fill them in.

## Done when

1. Every source in your inventory that this environment reaches and its licence allows has an intake script.
2. Every contest it covers is in `data/`, with p or a marked reason for none.
3. Your checks are written and the pull requests are open.
4. You have reported to the orchestrator in at most fifteen lines, and once earlier, for the forecast method (step 3).

Then stop (`_COMMON.md` 14).

## Amended 2026-11-07 08:36 UTC: a robustness test for every change to a forecast

From now on, a change to a forecast (a factor, a class, a route) is adopted only if:
- it improves the out-of-sample test; and
- it still improves it, with no tested cell made worse, when any one scored year is left out.

Otherwise the forecast stays as it was, and the change is reported beside it.

*Reason:* M2's second pass (#47) finds three of D2's decisions turning on a single year or cell. A change adopted on a knife edge is as likely noise as signal, and the model's default is no change.

Check the one change you have adopted, the calibration factor of #31 (local races), against this test. Report whether it holds. If it does not, take it out in a PR, with the before and after.
