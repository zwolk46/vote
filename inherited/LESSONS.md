# What the midterms system learned (11-02 to 11-06 2026)

*Written by the midterms orchestrator for the next project. Each lesson has its date and its evidence in zwolk46/midterms (`STATE.md`'s log on branch claude/project-thread-ik9nd7, `RULINGS.md`). Evidence, not law.*

## Working with the maker

1. **He is away for hours and skims when he returns.** Lead with the answer; under 80 words when he has been away; one ask at a time, with a decision card when the choice is his. Do reversible things and say so; wait only for what cannot be undone. (Whole record.)
2. **His words go into `RULINGS.md` verbatim, the same turn.** A paraphrase drifted twice into a rule he did not make. (11-03.)
3. **"Ignore time limits"** (11-05 15:48) and **"don't sacrifice components or his review for time"** held throughout: quality was never cut for a deadline.
4. **Usage.** 11-06 11:30 to 11:32: a quarter of his weekly limit in about 12 hours with up to ten workers on Opus at high or max effort. He asked to wind down or lower effort. Start with fewer workers; stand each down when its brief is done; ask before max effort.
5. **He may change his mind about anything he said earlier**, including designs he asked for (11-05 21:03: his earlier instructions, "even the glass intro", are optional). Keep earlier work on branches; delete nothing.

## Running the system

6. **One orchestrator, workers from briefs, every instruction with its reason.** This let workers continue after their context was summarised, and let a worker refuse an instruction with no reason rather than misapply it (11-06: W24 asked for the reason of "merge main, never rebase").
7. **The orchestrator gates every PR itself:** `git merge-tree` against `main` for conflicts, then `npm test` and `npm run build` on the merge, then a squash merge with a plain title. Several PRs ready at once are gated together on one merged tree. (Gate loop in `STATE.md`, 11-05 and 11-06.)
8. **Merge `main` into branches; never rebase or force-push a pushed branch; never amend.** Two workers tried a force push on 11-05; it would have rewritten what others had read. (`briefs/_COMMON.md`, added 22:40 UTC 11-05.)
9. **Thread messages are limited:** about 120 a day from one thread to other threads and the coordinator. The orchestrator hit it at 10:44 UTC 11-06 by sending three notes per merge. Batch: one board update per several changes; no "merged, thanks" notes when the merge itself tells the worker. A message from the maker in the thread lifted it.
10. **A stacked PR** (based on another PR's branch) must be retargeted to `main` after its base merges, or it merges into a dead branch. (11-06, #233 and #234.)
11. **Do not route around another session's permission check.** When a worker's session refused to push, the orchestrator did not push its bundle for it; another worker wrote the fix fresh. (11-06, W18 and #222.) Likewise the orchestrator's own check refused sending a passcode in a command line (11-06 15:20); it stopped and told the maker.
12. **Secrets:** never in the repository, memory or a file. A passcode the maker gave in a message was read by workers from that message by id, used as an environment variable, and the cookie jar deleted after. (11-05 onward.)
13. **A worker loses what is not pushed** when its context is summarised or its container ends. Push every turn; write `STATE.md` every turn.
14. **Records the code cites must be on `main`.** Briefs kept only on the orchestrator's branch were cited by code on `main`; a stranger reading `main` could not find them. (11-06, #244.)
15. **Subagents for cold readings and bulk checks only**, on Sonnet or Haiku. They know only their prompt; give them the curl rule and the money rule with reasons.

## Vercel, GitHub and the web

16. **Vercel's Git hook can miss a push.** Check that the deployment of the pushed commit exists; if not, create it with the connector from the Git source. (11-06 03:46.)
17. **`vercel.json` `functions.*.includeFiles` is limited to 256 characters**; a longer one fails the deploy at schema check. Use a glob. (11-06 01:54, probe/og-cinematic.)
18. **A build that downloads from the web fails when that site is down.** #251 fetches three Wikimedia photos at build, pinned by SHA-1. Prefer committing small assets. (11-06.)
19. **Vercel does not compress a middleware's answer** and undoes a gzip the middleware applies; size pages served from middleware accordingly. (11-05, W18.)
20. **A site behind a login shows no link previews**: preview bots get the login's 401. Decide early whether share cards must work. (11-06 15:20.)
21. **Read pages with `curl -sSL`**; WebFetch returns a summary and raises approval prompts. Some sites refuse Claude's agents by robots.txt (apnews.com, 11-04); a refusal aimed at Claude is not ours to work around.
22. **No bursts:** Clarity blocked a sandbox after about 40 requests in a minute (11-02). One request every few seconds per host; stop at the first refusal.
23. **Local `vite preview` serves no `/api/`**; components that fetch it fail locally while fixtures work. (11-05.)

## Building pages

24. **Measure the case that does not fit** (the maker, 11-03 12:50: "These are all things you should catch yourself"): every page at phone widths 320 to 430 and text 1× to 2×, desktop at the narrowest width of each layout, with real data, not only fixtures. Fixtures missed faults that real data had (11-06, #239, #240, #242).
25. **One bad field must not blank a page:** wrap each card in an error boundary that draws a plain fallback and logs (11-06, #241 and #246: a null party in one row blanked two states and 26 race pages).
26. **A view that subscribes after it draws can miss its first answer;** redraw on subscribe if woken in between (11-06, #248).
27. **No jumping while loading:** reserve space for what is coming; measure layout shift on arrival (11-05, W19; 11-06, #250).
28. **Timing checks on a cloud machine are noisy:** compare against `main` interleaved on the same machine, never against a fixed budget alone (11-06).
