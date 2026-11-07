# Brief B1: Try to break the model before it goes to the maker

*Written 2026-11-07 by the orchestrator. Model: **Fable 5.1**, effort **xhigh**. The project instructions' table puts "breaking the law and the model before they go to Zach" on Fable, because an error there is carried into everything below. Read `briefs/_COMMON.md` whole first; it is part of this brief.*

## Your sub-end

**Find every way in which `model/MODEL-DRAFT-2.md` is wrong, misleading, or narrower than the maker's intention, before he reads it.**

*Why it matters:* the maker will decide, from this draft, what the law of the site says (the general law, `the-law-for-agents.md` 16b: "Before the law is ratified, the chat tries to break it"). A break caught now costs a sentence. Caught after ratification, it is carried into every page.

## What the draft rests on

- **The maker's words:** `brainstorm/2026-11-06-transcript.md` and `brainstorm/2026-11-07-transcript.md`, and `RULINGS.md`. Read them to know what he intends. They are the standard the draft is held to.
- **The facts:** `research/*-v2.md`, read at source.
- **The mathematics:** `model/MATH.md` and `model/math/`, derived and checked by script.

## What to do

1. **Breaks of intention** (general law 16b). Move one variable the draft bears on, holding the rest still, and ask whether the draft still says what the maker means. Look in particular at:
   - the counterfactual and its reading of "everything else fixed";
   - the break-even framing and the two readings of B;
   - how C enters;
   - "ex ante" as the measure;
   - each choice in its §9.

   Report each break as: the variable, the case, what the draft says, what the maker's words suggest, and a proposed fix in one sentence.
2. **Breaks of fact.** Check every figure and quotation in the draft against the v2 reports and, where a report leaves doubt, against the source. For anything you re-read, curl and the other rules of `_COMMON.md` apply.
3. **Breaks of mathematics.** Check every formula and every mathematical claim in the draft against `MATH.md`, and re-run `model/math/run_all.sh`. Say where the draft states MATH more strongly than MATH does, or drops one of its conditions.
4. **Breaks of reading.** Where would a stranger with a broad education, but no statistics, misread the draft? Give each such place and a plainer wording.
5. **What is missing.** Is there a factor, framework or case that bears on whether one vote's expected benefit exceeds its cost, and that the draft forecloses without saying so?

## Path and constraints

- Write `model/BREAKS-draft-2.md`. Give each break a number, a kind (intention, fact, mathematics, reading, missing), a severity (changes what gets made / changes a number / wording) and a proposed fix. Then list what you checked and found sound.
- Do not edit the draft. The orchestrator decides what changes (`_COMMON.md` 3).
- You may run subagents on Sonnet 5.5 at xhigh to re-check facts at source, each with `_COMMON.md` rules 6, 7 and 13 and their reasons.
- Work on your own branch from `main`, and open a pull request that adds only `model/BREAKS-draft-2.md`. Push every turn.

## Done when

Every item above has been worked, the file is in a pull request, and you have reported to the orchestrator thread in at most fifteen lines, the most severe breaks first. Then stop (`_COMMON.md` 14).
