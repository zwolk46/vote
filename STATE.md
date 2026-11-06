# STATE: the orchestrator's hand-off

*Current every turn, so a stranger can continue. The orchestrator alone writes it.*

## Where things stand

- Initialized on 2026-11-06 from `handoff/vote-importance/` in zwolk46/midterms (its PR #252), by the midterms orchestrator: system files, templates, `inherited/`, the starter site with Plex. `npm run build` and `npm test` (1 pass) clean.
- Vercel: linked. Project `vote` (prj_C78MKoz1D80kgE2Bfz9mMmET3Ndo, team zachs-projects-74dd78e7), imported by the maker. Production deployment dpl_5azt1qjLZELKy2tUsxjUHhD9Sotx of `main` 80e6705 is READY [measured 2026-11-06 17:36 UTC]. Address: https://vote-rho-pearl.vercel.app. Vercel Authentication is on ("all_except_custom_domains"), so the vercel.app addresses ask visitors to sign in to Vercel; to settle before launch (midterms lesson 20: no link previews behind a login).
- Orchestrator: thread "Orchestrate the vote site" (cmsg_01FHkmcV6WaeZh9r5PfgnMbuGmNcLgzp1vbf5yXQkbDeFE), branch `claude/project-thread-0szt08`; this file is kept current on that branch.
- Law: not yet drafted. Brainstorm under way; its verbatim record is `brainstorm/2026-11-06-transcript.md`. Settled so far (his words, 19:32): importance is the chance one vote decides the outcome, all else held fixed; the site exists to show the individual vote's expected benefit against its cost. The site itself is "way later". 19:39: he asked the orchestrator to flesh out the full model itself (the site is a visual demonstration, so not too complex, perhaps two modes), to foreclose nothing, and to ask only material questions; B, in his words, is the marginal difference between the outcome voted for and the expected outcome. Under way: breadth-first research (frameworks, decisiveness models and estimates, historical close races) in `research/`. Open: whether B counts benefit to others (he called the question premature until the framework is set); how a margin of one is treated (recounts, courts); which elections.

## Project instructions

In force since 2026-11-06 20:04 UTC: `PROJECT-INSTRUCTIONS.md`, approved by the maker (20:03, project chat) and applied verbatim by the coordinator.

## Blocked: network access (asked of the maker 2026-11-06 ~20:10 UTC)

The session's egress policy refuses every scholarly, archive, data and news host tried (43+ hosts, 403 at CONNECT; list in `research/decisiveness-models.md` section 1.2); only GitHub is reachable. The project has no cloud environment selected (built-in, no settings). Asked the maker to add one with Full network access (Project settings, Cloud environment, Add cloud environment). Threads started after that run on it; this thread may be moved with `switch_environment`. Fallback: WebFetch works (tested on Gelman, Silver & Edlin 2012 at sites.stat.columbia.edu) but returns quotes capped at 125 characters and saves no PDF; too thin to rest the model on, usable for spot checks, and always said so (CLAUDE.md).

## The research plan (his ask of 19:50: parallel where it can be, sequential where it must, no loss of accuracy)

- **Wave 1, running now in parallel** (Sonnet subagents in the orchestrator's thread, xhigh): `research/decisiveness-models.md`, `research/historical-close-races.md`, `research/frameworks-benefit-cost.md`, `research/electoral-systems.md`. Subagents, not threads, because bounded reading reports straight back and costs less.
- **Wave 2, needs wave 1:** fresh-reader check, at source, of every formula and figure the model rests on; then the orchestrator writes the full model (with a simple mode for the site); Fable tries to break it; then it goes to the maker.
- **Wave 3, after the maker has seen the model** (he put the standard of review before the historical data, 19:32): worker threads through the coordinator, from briefs in `briefs/`, to compute p for real past elections, split by election set. At most three at once.

## Threads

| Thread | Id | Brief | Status |
|---|---|---|---|

## Accounts and keys opened (no secrets here)

## Log (newest first; one line per turn)

- 2026-11-06 20:20: research C (frameworks, benefit, cost) back, read only through WebFetch extracts (curl refused); every fact to be re-read at source in wave 2. Its key point: the altruistic reading of B is the one choice the maker's conclusion turns on; and his "marginal difference" fits B or pB.

- 2026-11-06 20:05: project instructions approved and applied; checked identical to the draft.

- 2026-11-06 20:05: he ruled the orchestrator controls the project; drafted project instructions with a model and effort table; put to him.

- 2026-11-06 20:10: research subagent A back, blocked by network policy (others likewise); asked the maker for network access; research to move into threads once granted.

- 2026-11-06 19:52: he asked for parallel delegation; plan in waves recorded; a fourth subagent (electoral systems) started; told the coordinator no threads are needed yet.

- 2026-11-06 19:41: brainstorm turn 2; ruling on models and effort recorded; research started (three Sonnet subagents).

- 2026-11-06 19:34: brainstorm turn 1; proposed p×B against C as the standard of review; asked whether B counts others.

- 2026-11-06 17:37: orchestrator started; read the record; deploy checked READY; greeted the maker; brainstorm opens, the formula first.

- 2026-11-06: initialized by the midterms orchestrator; first push of main.
