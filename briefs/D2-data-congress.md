# Brief D2: Senate, governor and House races, and control of each chamber

*Written 2026-11-07 by the orchestrator. Model: **Opus 5.5**, effort **xhigh**. Read `briefs/_COMMON.md` whole first; it is part of this brief. Opus because this is data modelling: almost none of these races has a published p, so the model's own forecast decides most numbers (`PROJECT-INSTRUCTIONS.md`).*

## Your sub-end

**For every Senate, governor and House race of 2024 and 2022, then of earlier cycles as far as sources allow, gather from true sources every input the model needs, compute p for the race and for control of its chamber, and write it in the plan's layout, so the site can show each race's p and B\* with every figure's source.** 2026 comes after 2024 and 2022: its counts are not yet certified, so until they are, a 2026 race is marked as an unofficial count with its date and source.

*Why it matters:* these are the races on most readers' ballots beside the presidency, and the step down from the presidency is where p starts to grow (law 5: "a reader sees p grow as contests shrink"). Law 8: every figure has its source and date, and is checked by another agent.

## Read first, whole

`model/MODEL.md` (§3, §4, §7, §9, §10), `model/MATH.md` §0, §1, §4.2 and §6, `model/math/common.py`, `model/math/s4_two_stage.py`, `plan/PLAN.md` (§2 and §3 are your layout), `research/historical-close-races-v2.md` and `research/electoral-systems-v2.md`. *Reason:* the model is approved; you compute it, you do not change it. Where you find it wrong or silent, say so and do not work around it (`_COMMON.md` 2, 11).

## What to do

1. **Breadth first, then choose** (`_COMMON.md` 3, 4). For each input list every candidate source, with what it gives, its licence, its reach from this environment and its evidence:
   - certified results by race (state election offices, the Clerk of the House's statistics, the FEC's federal elections reports, compilations that name their origins);
   - published forecasts a voter could have seen before the election, by race and for chamber control, ideally the forecaster's simulations or seat distributions. Leads, not facts: 538's data on GitHub (`fivethirtyeight/data`); record every licence;
   - population of each state and district (Census Bureau), for the per-person reading of B\* (model §5).
2. **The model's own forecast** for races with no published forecast (model §3, "Which forecast"): propose a method fitted to past races from variables known before the election (the district's past presidential vote, incumbency, the national environment, as Gelman, King & Boscardin and Mulligan & Hunter did, R1 §3.1 E and §3.3), with a back-test on past cycles. **Report it to the orchestrator before you compute p with it**, and keep gathering data while you wait. *Reason:* the method decides almost every number here, so it is approved before it is used (plan §3).
3. **Compute p** for each race with `p_contest` from `pipeline/core.py`, which D1 writes first in its own pull request. Until it is on `main`, gather data; if you must compute before then, write against its signature, `p_contest(n, mean, sd, tails)` returning `{"p", "event"}`, and do not write a second version of it. *Reason:* one implementation of each formula (plan §3).
4. **Control of the chamber, exactly** (model §3 "Two stages", §7; MATH §4.2): p = (chance the seat is tied) × (chance that seat then decides control, given that tie), from a joint forecast of all seats with its common swing stated. The shortcut fails badly for a leaning seat, so never use it. State what decides control in each case (the Vice President's tie vote in the Senate, 218 in the House, seats not up).
5. **Races the model does not yet compute.** Runoffs (Georgia), ranked-choice races (Maine, Alaska), Louisiana's open primary system, and uncontested races: record the race with its result and sources, and mark p as not computed with the reason (model §7: no calculation checked is good enough to show yet). An uncontested race has p of zero, said so. Never invent a number for these. *Reason:* law 8; a number the model cannot stand behind is not a true thing.
6. **Write** `data/senate/<year>.json`, `data/governor/<year>.json` and `data/house/<year>.json` in the layout of plan §3, and `pipeline/chambers.py`, which computes every `p` from `data/` and `pipeline/core.py`. Add any field you need to `data/README.md` (D1 starts it), never renaming one. Sources, method and checks go in `data/congress/REPORT.md`.
7. **Check** your p against the historical record (model §4; MATH §8): how often races like these ended within one vote, against what your p implies.

## Path and constraints

- Work on your own branch from `main`; a pull request per level and year as each is done, 2024 Senate first. Push every turn. *Reason:* the orchestrator gates as you go, and the tracker shows each set as it lands.
- Touch only `data/senate/`, `data/governor/`, `data/house/`, `data/congress/`, `pipeline/chambers.py` and new fields in `data/README.md`. D1 owns `pipeline/core.py` and `data/president/`. *Reason:* two workers fill one layout at once.
- Raw downloads stay out of the repository unless small and licensed for it; record each URL and when you read it (law 8).
- No figure from memory (OPERATIONS §3). A figure you could not read at source is marked so, or left out.
- Network: if a host you need is refused, record it and tell the orchestrator in your next report; do not route around it (`_COMMON.md` 6). Known: web.archive.org is refused; MEDSL's Dataverse files ask for a name and email, which is the maker's call (law 10), so do not fill it.

## Done when

2024 and 2022 are complete for all three levels with chamber control, earlier cycles as far as sources allow, 2026 marked as it stands, the PRs open, and you have reported to the orchestrator in at most fifteen lines. Report earlier, once, for the forecast method (step 2). Then stop (`_COMMON.md` 14).

## Amended 2026-11-07 03:13 UTC: as much data as can be found, by script

The maker's ruling of 03:13 (`RULINGS.md`; `plan/PLAN.md` §3a) amends this brief:
- **Breadth is a goal of its own.** Go back as far as standardized sources go, not only to the years named above. *Reason:* "aggregating absolutely as much data as we can find".
- **Intake by script.** For each standardized source, write `pipeline/intake/<source>.py` once: download to a cache outside the repository, check row counts and totals, convert into the layout of plan §3 with the source block filled. *Reason:* "an intake flow that doesn't use as many tokens"; a year or a state then costs a run, not a reading.
- **An inventory.** List every standardized dataset you find, for your level and any other, in `data/sources/<your level>.md`: publisher, coverage, format, licence, and whether this environment reaches it. *Reason:* the next worker starts from what is known.
- **No live data.** Everything is a published dataset taken in by script.


## Amended 2026-11-07 05:58 UTC: follow-ups from M2 (`checks/M2-REPORT.md`, #26), and the Vice President

M2 checked every p independently. Every one reproduces from its inputs, and no p is off by a factor of two. The forecasts are honest, with the points below, which the orchestrator has decided. Do them in one pull request, each with its reason in `data/congress/REPORT.md`, then report the changed totals and sums.
1. **The Vice President's tie vote** in presidential years is the presidential chance, not one half: 538's where it stands first, else the model's own. *Reason:* the Senate's control in a presidential year turns on who becomes Vice President.
2. **Fit on earlier cycles only**, as D1 and D3 do; never leave one cycle out. Choose the fewest earlier cycles a fit needs from your back-test. Extend the fitting data back where your sources reach (MEDSL from 1976, Cha) and the predictors exist. A year that still has too few earlier cycles gets p not computed, with that reason, unless a published forecast stands first. *Reason:* the model's own forecast is fitted to like past races, from what was known before the election (MODEL §3); a coefficient fitted partly on later years is something no voter knew. M2 measured the effect (3.4): the sum of p × 0.81 (House 2014) to × 1.04.
3. **538 kept on p's error, not the sd's.** Keep 538's implied sd only where p's relative error, |z² − 1| × the sd's, is under 20%; otherwise the model's own stands first. *Reason:* the reader sees p, and at z = 3.94 a 7% error in the sd is a 105% error in p (M2 3.9: 164 Congress entries move).
4. **Control under 538, reading (c):** take 538's mean and sd as the seat's marginal in the chamber stage, with s_e,i = √(sd₅₃₈² − s_a²), as the presidency already treats 538's marginals. Where sd₅₃₈ < s_a, say what you do and mark it. *Reason:* one forecast of the seat throughout its figure; the record's mix conditions what a tie tells the chamber on the model's mean while the tie's chance is 538's (M2 2.6).
5. **Governors: add the state's last governor race** as a predictor (M2's A4: log score 1.064 → 1.143), then report the back-test's z sd and coverage. The governors' p may be shown: M2 found the 0 of 4.4 specific to the 5,000-vote line, and the forecast slightly too wide, so p is if anything a little low (3.1, 3.2).
6. **The files reproduce themselves.** Record f(½) in each p block, and mean and sd at full precision. Give the p = 0 blocks their script and commit (M2 1.4, 1.5). *Reason:* law 4, a reader recomputing p from the file gets the file's p.
7. **One fetch and one FEC intake:** `pipeline/fetch.py` (D1's, which refuses cross-site redirects) replaces `congress_common.fetch`, and `fec_president.py` folds into `fec_federal_elections.py`. *Reason:* one implementation of each thing.
8. Senate 2014's chances stand as exact, as recorded: no step at any plausible run count.

After it merges, the orchestrator reruns `checks/m2/c3_chambers.py`.
