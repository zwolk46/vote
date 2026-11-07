# Brief D1: The presidency, state by state, and the shared computation

*Written 2026-11-07 by the orchestrator. Model: **Opus 5.5**, effort **xhigh**. Read `briefs/_COMMON.md` whole first; it is part of this brief. Opus because this is data modelling: which forecast stands for a state, and how the College stage is computed, turn on judgment (`PROJECT-INSTRUCTIONS.md`).*

## Your sub-end

**For every state in every presidential election from 2024 back to 2000, gather from true sources every input the model needs, compute p exactly in both stages, and write it in the plan's layout, so the site can show each state's p and B\* with every figure's source.** Also write the shared computation, `pipeline/core.py`, that every data worker uses.

*Why it matters:* the presidency is the one level with published estimates of p (model §4), so it is where our computation is checked against others'; and it is the contest most readers bring. Law 8: every figure shown has its source and date, and is checked by another agent. Law 5: the site shows "as much historical data as we possibly can".

## Read first, whole

`model/MODEL.md` (the method; §3, §4, §7, §9, §10), `model/MATH.md` §0, §1, §2, §3.4, §4.1 and §6, `model/math/common.py` and `model/math/s4_two_stage.py`, `plan/PLAN.md` (§2 and §3 are your layout), and `research/decisiveness-models-v2.md` and `research/historical-close-races-v2.md`. *Reason:* the model is approved; you compute it, you do not change it. Where you find it wrong or silent, say so in your report and do not work around it (`_COMMON.md` 2, 11).

## What to do

1. **`pipeline/core.py` first, in its own pull request.** One function, at least: `p_contest(n, mean, sd, tails="normal")` returning `{"p": ..., "event": ...}` for a two-way race, with `tails` `"normal"` or `"t4"` (model §9.5), the exact sum below 1,000 voters and the density form above (model §3), all built on `model/math/common.py` by import, not by copying. Add a test, `pipeline/test_core.py`, runnable with `python3 -m pytest pipeline` or plain `python3 pipeline/test_core.py`, that reproduces figures already in `model/math/OUTPUT.txt` (for example the 2,000-voter race at 52-48 with a 4-point spread, p = 1 in 468, MATH §6.2). *Reason:* D2 imports this function while you work (plan §3), so it must exist early, and its figures must match the ones the model was checked with.
2. **Breadth first, then choose** (`_COMMON.md` 3, 4). For each input list every candidate source you can find, with what it gives, its licence, its reach from this environment, and its evidence:
   - certified results by state (and by district in Maine and Nebraska, which award electoral votes by district), with two-way shares as the model defines them;
   - electoral votes by state for each year;
   - published forecasts a voter could have seen before each election: state means and spreads, or simulations giving the joint distribution of states, or a published p. Leads to check, not facts: 538's data on GitHub (`fivethirtyeight/data`, under CC BY 4.0 by its README), The Economist's repositories, academic replications. Record each one's licence; The Economist's published p figures are its copyright and not settled for showing (model §4), so collect them as checks, not as figures to show;
   - population by state (Census Bureau), for the per-person reading of B\* (model §5).
3. **The model's own forecast**, for years with no published forecast a voter could have seen (model §3, "Which forecast"; §10: 538's archived pages need web.archive.org, which is refused here). Propose a method fitted to past cycles from variables known before the election, with its back-test on the years that do have published forecasts. **Report it to the orchestrator before you compute p with it**, and keep gathering data while you wait. *Reason:* the method decides every number for those years, so it is approved before it is used (plan §3).
4. **The College stage, exactly** (model §3, "Two stages"; MATH §4.1): p = (chance the state is tied) × (chance its electoral votes then decide, given that tie), from a joint forecast of the states. Use the forecaster's own joint distribution where published; otherwise the model's, with its common national swing stated. Never the independence shortcut. Maine's and Nebraska's districts are a further stage (model §7).
5. **Check against the published estimates** (model §4): Gelman, Silver & Edlin for 2008, The Economist for 2020, Gelman, King & Boscardin for 1992 if in range. For each, your p beside theirs, the convention of each (MATH §2), and why they differ. *Reason:* the one outside check of the whole computation; M2 (Fable) checks it again after you.
6. **Write** `data/president/<year>.json` in the layout of plan §3, one contest per state (and per district where electoral votes are split), each with its sources, and `pipeline/president.py`, which computes every `p` from `data/` and `pipeline/core.py`. Start `data/README.md` with the layout and every field you add (plan §3). Write your sources, method and checks in `data/president/REPORT.md`.

## Path and constraints

- Work on your own branch from `main`. Two pull requests at least: `pipeline/core.py` with its test first; then the data, one year or several per PR as they are done, 2024 first. Push every turn. *Reason:* the orchestrator gates as you go and the tracker shows each year as it lands.
- Touch only `pipeline/`, `data/president/` and `data/README.md`. D2 works in `data/` beside you (Senate, governor, House) and imports `pipeline/core.py`; change `p_contest`'s signature only by telling the orchestrator first. *Reason:* two workers fill one layout at once.
- Raw downloads stay out of the repository unless they are small and their licence allows it; record each one's URL and when you read it. *Reason:* the record must let anyone fetch the same file again (law 8), and a large or unlicensed file does not belong in a public repository.
- No figure from memory (OPERATIONS §3). A figure you could not read at source is marked so, or left out.
- Network: if a host you need is refused by this environment, record it and tell the orchestrator in your next report; do not route around it (`_COMMON.md` 6). Hosts already known to be refused: web.archive.org; MEDSL's Dataverse files ask for a name and email (a guestbook), which is an outside party and the maker's call (law 10), so do not fill it.

## Done when

Every state and every year from 2024 to 2000 has its contest with inputs, sources and p (or a marked reason it has none), your checks against the published estimates are written, the PRs are open, and you have reported to the orchestrator in at most fifteen lines. Report earlier, once, when `pipeline/core.py` is up, and once for the model's own forecast method (step 3). Then stop (`_COMMON.md` 14).
