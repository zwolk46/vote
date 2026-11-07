# Brief X1: The site's design, and options for its first screen

*Written 2026-11-07 by the orchestrator. Model: **Opus 5.5**, effort **xhigh**. Read `briefs/_COMMON.md` whole first; it is part of this brief (rule 16 above all). Opus because design turns on judgment (`PROJECT-INSTRUCTIONS.md`). xhigh because every thread runs at xhigh (Zach, 2026-11-06 19:39) and max only on his word; whether design work runs at max is an open question to him, and if he says so, the orchestrator tells you.*

## Your sub-end

**Decide, within the design guidance, how this site looks, reads and moves, and put two or three whole options for its first screen in front of the maker, each on one preview link, so he can pick one.**

*Why it matters:* law 6, "a really nice visualization", made as the design guidance says; law 9b, a surface that matters goes to him as two or three whole options; the design guidance, process step 2, options side by side, never one, each a whole build he can try. The first screen is where a stranger meets the claim, so it carries the end (law 1, 1a).

## Read first, whole, in this order

1. `inherited/design/README.md`, and everything it names, in its order: `TASTE.md`; `specs/DESIGN-SPEC.md` §0 and §1, then the sections for the surfaces you draw (12 and 26 for page states, 15 light and dark, 17 switches, 19 icons, 20 components, 23 the case that does not fit); `specs/MOTION-SPEC.md` §1, 2, 4, 5, 6; `inherited/DESIGN.md`. *Reason:* `_COMMON.md` 16 and CLAUDE.md: his midterms corrections apply here by default.
2. `LAW.md` whole, above all 1 (the end), 1a (the cases against his claim are shown), 1b (one question), 2 to 2c (B\* leads, both readings, the ballot summed), 3 to 6 (plain, full, broad, beautiful) and 11 (the midterms look). *Reason:* the first screen states the end; a design that misses 1a or 2b fails the law however it looks.
3. `model/MODEL.md` §1, §2, §4 and §8 (the two modes), and `plan/PLAN.md`.
4. The midterms site itself, https://midterms.zwolk.com, and its code where useful (zwolk46/midterms is readable with `git clone --depth 1`). The starter in `src/` already carries its tokens and Plex.

## What to do

1. **A design spec for this site**, `design/DESIGN-SPEC.md`: what carries over from the midterms spec as it stands, what this site needs that midterms did not, and the pages the site needs, as a proposal. Things this site has that midterms did not, as starting points, not a list to keep to:
   - B\* runs over about eight orders of magnitude, from thousands of dollars in a town race to hundreds of billions in a safe state (model §2, §4). How a reader feels that scale is the site's central visual problem.
   - The ballot: one trip, many races, shares of the trip adding toward 100% (law 2c).
   - Two modes: simple (three facts in, two numbers out) and full (every input and its source behind every number) (law 3, 4; model §8).
   - Every figure carries its source and date where a reader would ask (law 8), without burying the page.
   - The tie counted as half, and the event at twice p, always named (law 2b, open points).
   *Reason:* the build workers will work from this spec; the orchestrator decides the pages from your proposal.
2. **Two or three whole first-screen options**, on one branch, switched by `?v=a`, `?v=b`, `?v=c`, with a picker shown only on previews and never in production (design guidance, process step 2). Each is a whole build he can use on a phone and a desktop, not a mock-up, and each takes a different idea of how to show the end, not a different colour. Design within the principles; you may use real examples from Details, 21st.dev or Mobbin where one fits the page as a whole, and cite it; never 21st.dev's `generate` (it costs) (process step 1).
3. **Real figures only.** Use the figures already sourced in `model/MODEL.md` (§2 and §4: for example 1 in 10 million for the closest states in 2008, 1 in 16 billion for California in 2020 as The Economist published it, the 2,000-voter town race marked as stylised), each with its source on the page. The Economist's figures are its copyright and not yet cleared for showing (model §4), so an option that uses one marks it in your report. Where you need a figure that is not in the model, mark it plainly as a sample, or wait for D1 and D2's data. *Reason:* law 8; the midterms rule that nothing reads as a real figure unless it is one (`TASTE.md`).
4. **Check each option before it goes to him** (process steps 3 to 6): phone widths 320 to 430 at text 1× to 2×, desktop at the narrowest width of each layout, light and dark, motion measured with the `code/motion.js` tokens, nothing jumping while loading, `code/Boundary.jsx` around each part. Adapt `code/fitcheck.cjs` and `code/checks.cjs`; Chromium and Playwright are installed in your container. *Reason:* the maker, midterms 11-03 12:50: "These are all things you should catch yourself".
5. **Report** to the orchestrator: the preview link for each option (Vercel builds every pushed branch; the stable branch address is of the form `vote-git-<branch>-zachs-projects-74dd78e7.vercel.app`, behind a Vercel sign-in the maker has), what each gives toward the end, what it costs, and the checks' results. The orchestrator sends them to the maker. Then wait for his pick, and stop if the orchestrator says so.

## Path and constraints

- Work on your own branch from `main`; push every turn. Open a pull request with `design/DESIGN-SPEC.md` alone as soon as it is written. The options stay on the preview branch until he picks; after his pick, the chosen one goes to `main` in its own PR, without the picker. *Reason:* the site changes only through `main` (law 7b), and an option he did not pick never reaches it.
- Touch only `design/`, `src/` and `public/` on your branch. Data workers (D1, D2) write `data/` and `pipeline/` beside you.
- Nothing bought, no outside party contacted (law 10). No new dependency without its licence and size in your report; the starter is Preact and Vite (law 7b: what the site is built with beyond the starter is chosen once the design work has learned enough to choose).

## Done when

The spec is in a PR, two or three options are on one preview branch with the checks passed, and you have reported to the orchestrator in at most fifteen lines. Then wait for the maker's pick through the orchestrator; when he has picked, the brief continues with step 2's merge, then stops (`_COMMON.md` 14).
