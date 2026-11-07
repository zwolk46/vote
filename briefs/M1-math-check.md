# Brief M1: The mathematics of one vote's decisiveness, derived and checked

*Written 2026-11-07 by the orchestrator. Model: **Fable 5.1**, effort **xhigh**. The project instructions' table puts "checking the mathematics the site rests on" on Fable, because an error there is carried into everything below. Read `briefs/_COMMON.md` whole first; it is part of this brief. Then read `model/MODEL-DRAFT.md` (the model as first drafted, whose claims you check) and the four research reports read at source: `research/decisiveness-models-v2.md`, `research/historical-close-races-v2.md`, `research/frameworks-benefit-cost-v2.md`, `research/electoral-systems-v2.md`.*

## Your sub-end

**One derivation of p, the probability that one ballot changes an election's outcome, that the model and the site can rest on: every step shown, every convention named, every published formula and example the model cites reconciled with it, and every number reproduced by a script.**

*Why it matters:* the maker wants to show, from p, that an individual vote's expected benefit p × B rarely exceeds its cost C. He chose to lead with the break-even stakes B* = C ÷ p, and to show what they mean for the voter alone and per person affected (`RULINGS.md`, 2026-11-07 00:24). Whatever p the site shows, the site's claim is only as true as its mathematics. The research found that the published sources disagree with each other by factors of 2 and more, and that several printed examples do not follow from their own inputs.

## Fixed by the orchestrator (do not reopen; flag if you find it incoherent)

- **The comparison is counted against not counted.** Your ballot is cast for your side and counted, against the same ballot not counted, with everyone else's behaviour the same in both worlds. This is the maker's thought experiment (brainstorm, 2026-11-06 19:32). The swing "for A against for B" is twice that. Name it whenever it appears, and never use it as p.
- **Ties follow the jurisdiction's own rule.** A fair lot where the law says lot. Where the law says a new election or a legislature decides, say what p means then.
- **The measure is ex ante:** the probability a voter could have known before the election, from a forecast. The historical frequency of near-ties (Mulligan & Hunter, Klarner) is the reality check, not the measure.

## What to do

1. **The two-way race, exactly.** Derive p for the comparison above under each tie rule from the distribution of the margin among other voters. Then give the standard approximations: the margin's density at zero, and the vote-share forecast's density at one half divided by the number of voters. Give each with its constant, and state the conditions under which it holds and how large the error is.
2. **Reconcile the published conventions** with your derivation, factor by factor: Gelman, King & Boscardin 1998; Gelman, Katz & Tuerlinckx 2002; Gelman, Katz & Bafumi 2004; Gelman, Silver & Edlin 2012; Edlin, Gelman & Kaplan 2007; Barnett 2020; Mulligan & Hunter 2003. Show what each one's p would be under ours.
3. **Settle the flagged examples.** These are Gelman, Katz & Bafumi's "1.84/n" example, which R1 recomputes as 3.316/n and R4 as 10.65/n, so they disagree with each other; Gelman, Katz & Tuerlinckx eq. 2 and eq. 5; Myatt & Fisher's two-way constant ("6n"); and Gelman, Silver & Edlin's density at zero and its scale. For each, give the formula as printed (from the reports, and from the source itself where a report leaves doubt), what follows from it, and why they differ.
4. **Two stages.** Derive p for a presidential vote (your state tied, then your state decisive in the Electoral College) and for a seat and control of a chamber. Say what independence the product form assumes and how much its failure matters.
5. **Check every mathematical claim in `model/MODEL-DRAFT.md`** sections 2, 3, 7 and 8. These include: p falls about as 1/N; p falls very steeply away from 50-50; uncertainty helps a lopsided race and hurts an even one; recounts and counting error leave p about the same; and the simple mode's "p ≈ closeness ÷ voters" and B* = C ÷ p. For each, say holds, holds under stated conditions, or wrong, with the corrected statement.
6. **The simple mode's formula.** Propose the simplest formula a lay reader can follow that stays within a stated factor of the full model over the range of real US elections (from a few hundred voters to a presidential race), and show that range numerically.
7. **Other systems.** Check the stylised calculations in `research/electoral-systems-v2.md` (plurality with three or more, runoff, IRV, STV, list PR's "about M/N", referendums with thresholds and quorums, chambers, tiny electorates). Say which are sound enough to use as the model's own, and which are not.
8. **The historical frequency.** Say exactly what quantity Mulligan & Hunter's "1 in 89,252" and Klarner's counts estimate, and how it relates to an ex ante p.

## Path and constraints

- Write `model/MATH.md` (derivations, then a findings table: claim, verdict, corrected statement, script line) and scripts under `model/math/` (Python standard library, or numpy or scipy if installed). The scripts must reproduce every number in `MATH.md`, and their output goes into `model/math/OUTPUT.txt`. *Reason:* a number that only a model checked is not checked; a script anyone can rerun is.
- Choose nothing for the site beyond what this brief fixes. Where two derivations are defensible, give both with what each implies (`_COMMON.md` 3).
- You may run subagents on Sonnet 5.5 at xhigh to re-read a formula at its source (with `_COMMON.md` rules 6, 7 and 13 and their reasons). The mathematics is yours.
- Work on your own branch from `main` and merge `main` into it if it moves. Open a pull request that adds only `model/MATH.md` and `model/math/`. Push every turn (`_COMMON.md` 8, 9).

## Done when

Every item above is answered in `MATH.md`, the scripts reproduce every number, the pull request is open, and you have reported to the orchestrator thread in at most fifteen lines. Then stop (`_COMMON.md` 14).
