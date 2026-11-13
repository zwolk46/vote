# Restart: carry this project to a new account or a new project

*Written 2026-11-07 22:20 UTC by the orchestrator, at the maker's ask of 22:09 UTC (`handoff/MAKER-WORDS.md`): "I want all of my comments saved such that if maybe I purchase another account I can continue this project there by just pointing at the repo ... I want as little as I have to do as possible to be able to set that up, and I want this repo prepared for the abrupt stop." Everything a new project needs is in this repository. Nothing below depends on the old account, its memory, its threads or its files.*

## 1. What Zach does (three steps, about five minutes)

1. **Connect GitHub** in the new account as `zwolk46`: https://claude.ai/connect-github. *Reason:* the repository is the whole record, and Claude reaches it only through that link. Connecting Vercel too (the same Vercel login, team `zachs-projects-74dd78e7`) lets the orchestrator check deploys, but it is optional.
2. **Create a project** with the repository `zwolk46/vote`. In its Project settings, open Cloud environment, choose Add cloud environment, and set Network access to **Full**. *Reason:* the data work reads many public election, census and law sites, and the default environment reaches only GitHub. That cost the old project four hours on its first night (`STATE.md`, "Blocked: network access").
3. **Paste this one message** into the project chat:

   > Restart the vote project from the repo zwolk46/vote: read RESTART.md there and do what it says. Make PROJECT-INSTRUCTIONS.md the project instructions, word for word.

Nothing else is needed from you. The coordinator and the new orchestrator do the rest, and the orchestrator will put your three open picks to you again (section 5).

## 2. What the coordinator does, on that message

1. **Apply `PROJECT-INSTRUCTIONS.md` as the project instructions, verbatim.** Zach's message above is his word for it, as his message of 2026-11-06 20:03 UTC was in the first project ("Make these the project instructions"). *Reason:* they make the orchestrator the one who runs the project, and they carry his standing approval of the models and effort the orchestrator names.
2. **Start one thread** titled **"Orchestrate the vote site"**, on **Opus 5.5 at xhigh effort**, with Zach's message attached, and this opening message:

   > You are the orchestrator of the vote-importance site, restarted in a new project. Read RESTART.md in zwolk46/vote whole, then everything its section 3 names, in order, and resume as it says.

   *Reason:* the project instructions' table puts the orchestrator on Opus. Zach asked on 2026-11-06 19:39 for "effort extra, please, for all threads".
3. **Tell Zach in one line** that the orchestrator is starting in that thread. From then on, follow `PROJECT-INSTRUCTIONS.md`.

## 3. What the new orchestrator does, on its first turn

1. **Read whole, in this order:** `CLAUDE.md`, `LAW.md`, `the-law-for-agents.md`, `RULINGS.md`, `handoff/MAKER-WORDS.md` (every word Zach wrote, and his card choices), `STATE.md`, `OPERATIONS.md`, `PROJECT-INSTRUCTIONS.md`, `briefs/_COMMON.md`, `plan/PLAN.md`, then `handoff/memory/MEMORY.md` and the memory files it names. *Reason:* the law is written for a stranger, and its words alone carry its meaning. The memory files are the old project's working notes, evidence not law, and every thread id in them is dead.
2. **Find the newest state.** The old orchestrator kept `STATE.md` current on its branch, `claude/project-thread-0szt08`, and merged it to `main` from time to time. Read the newer of the two copies: `git log -1 --format=%cI origin/main -- STATE.md` against the same command for `origin/claude/project-thread-0szt08`. Then read that file's log, newest first, back to the last line that names a merge. *Reason:* the stop may be abrupt. The branch's log has a line for every turn, and `main` may lag it by hours.
3. **Make your own branch** from `main`, merge `origin/claude/project-thread-0szt08` into it, and keep `STATE.md` there, pushed every turn. Merge it to `main` through a pull request whenever a phase or a ruling changes, and at least every few hours. *Reason:* `main` is the restart point for whoever comes next.
4. **Greet Zach in your thread in under 80 words.** Say that the project is restarted from the repository, what runs next, and that the three picks of section 5 follow as cards.
5. **Put the open cards to him again, once each** (section 5), with the same options and recommendations. *Reason:* a card is tied to the old project and cannot be answered from the new one.
6. **Republish the tracker** (section 6) and give him its new link.
7. **Restart only the workers section 4 marks "restart"**, each from its brief, on the model and effort the brief names, at most three at once (`OPERATIONS.md` §4). Ask the coordinator for each one exactly as `PROJECT-INSTRUCTIONS.md` says. Add one line to its opening message: "This is a restart: read the resume note named in RESTART.md §4 first." *Reason:* the brief is the worker's law. The resume note says what it had done and left unmerged.
8. **Refresh project memory** from scratch, as pointers only: your thread id, the new tracker's link, the new environment. *Reason:* memory in the new project is blank, and the old one's facts already live in this repository.

## 4. Work in flight at the stop

*As of 2026-11-07 22:20 UTC. The newest `STATE.md` log line is the later word. Each worker keeps a resume note at `handoff/workers/<ID>.md` on its own branch, pushed at every step. A restarted worker reads that note first. Then it merges its old branch into its new one if `git log origin/main..origin/<old branch>` shows commits not on `main`.*

| Worker | Brief | Model, effort | Old branch | At the stop | On restart |
|---|---|---|---|---|---|
| D3, local, legislative and measure data | `briefs/D3-data-local.md` | Opus 5.5, xhigh | `claude/project-thread-sl6m2f` | #100 to #118 merged by 2026-11-13 (#115: the recount zone beside p; #118: Singer's 2020 results). Final report given 11:07 UTC (STATE log); the brief is done and the thread rests. Not done, for a later brief: §5.10's lattice form for zones under 2 votes (48 races), a recount rate for machine counts, MT's write-in report. | **done**: restart only for new work |
| M2, independent check of every p | `briefs/M2-check-computed-p.md` | Fable 5.1, xhigh | `claude/project-thread-pbr8zl` | Eighth pass merged as #102, #104, #105, #108, #110 and #114 (2026-11-13: #96 to #113 checked). §21 on #115 merged as #117, §22 on #118 as #119: every data PR through #118 checked. Final report asked 2026-11-13 11:30. | **restart only for new work** |
| X1, design | `briefs/X1-design.md` | Opus 5.5, xhigh | `claude/project-thread-ozfwbq-options`, `claude/project-thread-ozfwbq-explainer` | Holding for Zach's two picks, with both options carrying real data. Told him 2026-11-13 11:30 UTC: unless he picks by 2026-11-14 12:00 UTC, the pages start on the recommended pair (A the Ruler, B Steps). | **restart once he picks, or at that deadline** |
| T1, tracker | `briefs/T1-tracker.md` | Sonnet 5.5, xhigh | none | Kept the old tracker's rows. | **restart** after section 6, pointing the brief at the new tracker's link |
| D1, D2, D4, R1 to R4, B1, B2, M1 | their briefs | as named | as in `handoff/memory/` | Done, merged and stopped. | no |

**The previews** of the two picks are Vercel deployments in Zach's own Vercel account, so a move of the Claude account leaves them as they are: first screen [A](https://vote-git-claude-project-thread-o-6fbb1a-zachs-projects-74dd78e7.vercel.app/?v=a) and [B](https://vote-git-claude-project-thread-o-6fbb1a-zachs-projects-74dd78e7.vercel.app/?v=b), explainer [A](https://vote-git-claude-project-thread-o-f3f92e-zachs-projects-74dd78e7.vercel.app/?page=how&v=a) and [B](https://vote-git-claude-project-thread-o-f3f92e-zachs-projects-74dd78e7.vercel.app/?page=how&v=b). They ask for a Vercel sign-in.

## 5. Zach's open picks (re-put as cards)

The exact questions, options and recommendations are in `handoff/MAKER-WORDS.md`, "Cards still open":

1. **First screen: A, the Ruler, or B, the Ballot** (A recommended). Building the site waits on this.
2. **Explainer: A, Scroll, or B, Steps** (B recommended). Building the explainer waits on this.
3. **Design workers at max effort, or xhigh like everything else** (max for design only, recommended). Until he answers, design runs at xhigh.

One older ask also stands, and a Full-network environment settles it: web.archive.org, for 538's past forecasts (`plan/PLAN.md` §5).

Two source questions wait for him, to be put together when he next writes, not as urgent cards (2026-11-13): MEDSL's 2020 by-state Dataverse set (NT66Z3) sits behind a guestbook form (2018 came from MEDSL's GitHub instead; Singer's CC0 2020 set now gives 2020 a second count, except KS, MO, OH, UT and WY), an outsider's ask that only he can answer; and Jones's Virginia Election Data 1969–2026 (Dataverse BAQ69D) is CC BY-SA, whose share-alike term would bind the site's licence. *Reason:* both bind the site to an outsider's terms (CLAUDE.md, "Money and outsiders only on the maker's word").

## 6. The tracker

Zach watched the work in the artifact "Vote Work" (old link https://claude.ai/artifact/DzVTr4wvWE92sNxxEx6wKH, which belongs to the old account). To bring it back:

1. Publish `tracker/vote-work.html` as a new artifact with the capability `{db: {}}`. *Reason:* the page reads its rows from the artifact's database, collection `tasks`.
2. Write every row of `tracker/tasks-export.json` (73 rows at 22:20 UTC, keyed by document id) into `tasks` with one batch write, then add rows for anything newer in `STATE.md`.
3. Give Zach the link, and put it in memory and `STATE.md`.

## 7. What did not carry over, and what stands in for it

| In the old account | In this repository |
|---|---|
| Project memory (22 files) | `handoff/memory/`, a snapshot of every file |
| The project's shared files folder | `handoff/project-files/`, holding only the files not already in the repository |
| The tracker artifact and its rows | `tracker/vote-work.html` and `tracker/tasks-export.json` |
| Zach's messages and card choices | `handoff/MAKER-WORDS.md` (all 25 messages, verbatim) and `RULINGS.md` |
| Project instructions | `PROJECT-INSTRUCTIONS.md`, identical byte for byte to the file he attached at 20:03 |
| Threads and their ids | the briefs in `briefs/` and the resume notes of section 4 |
| The cloud environment with network access | Zach's step 2 |

## 8. Keeping this file true until the stop

The orchestrator updates `handoff/MAKER-WORDS.md` whenever Zach writes or answers a card. It refreshes the memory snapshot and the tracker export whenever they change materially, and it updates section 4 whenever a worker starts, stops or changes course. All of it is pushed with `STATE.md` every turn, and merged to `main` often. *Reason:* the stop may come at any moment, and only what is pushed survives it.
