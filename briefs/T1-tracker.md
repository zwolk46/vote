# Brief T1: Keep the maker's tracker current

*Written 2026-11-07 by the orchestrator. Model: **Sonnet 5.5**, effort **xhigh**. Read `briefs/_COMMON.md` whole first; it is part of this brief. Sonnet because the work has a clear directive and no judgment about the site (`PROJECT-INSTRUCTIONS.md`: Opus for "anything that turns on judgment"); every thread runs at xhigh (Zach, 2026-11-06 19:39).*

## Your sub-end

**Keep "Vote Work" (https://claude.ai/artifact/DzVTr4wvWE92sNxxEx6wKH) showing, at every moment, what is being built on the vote site and what is next, with a link to open every preview as soon as it exists.**

*Why:* the maker's words, 2026-11-07 02:58 UTC (`RULINGS.md`): "I want to be able to watch what's going on as it happens in at least some detail [...] what pages are being worked on, what features are being worked on [...] it'll be the place where I can open previews, where links will be put, and there should be probably a dedicated thread analogous to the thread run in the midterms project [...] I basically want to be able to just watch that until I have a comment that I need to make." A row that is wrong or late shows him a site that is not the one being built.

## The page and its rows

- The page is fixed; you never republish it. You change only its rows, with the `ArtifactData` tool (load it with ToolSearch), in the collection `tasks`. *Reason:* republishing would replace the page's code, which is the orchestrator's (source: `tracker/vote-work.html`).
- One document per row: `{ s: "doing" | "todo" | "done", t: text, o: order number, link?: an https URL, linkLabel?: a short word }`. The page sorts doing, then todo, then done, each by `o`.
- Rows already there (ids): `model`, `law`, `plan`, `data-president`, `data-congress`, `design-first-screen`, `data-local`, `data-cost`. Keep the ids; add new ones in the same kebab-case. *Reason:* a stable id lets you update a row in place instead of adding a duplicate.
- **Every write is pinned**: read the row first, then pass its `version` as `if_version`. Use one `batch` for several rows. *Reason:* the tool refuses an unpinned write to an existing row, and a pin keeps you from overwriting the orchestrator's own edit.

**What a row says.** One page, feature or piece of data the maker would recognise, in plain words, at most about ten words: "Data: Senate races, 2024 and 2022", "First screen, version B", "The calculator: your own race". Never a thread id, a branch, a PR number, a file path or a code name. *Reason:* he skims it; names from the code are not his words (the project's rule for titles and replies).

**When a row is doing.** When a worker thread is working on it. Split a row when a worker's report shows its parts move separately (for example "Data: the presidency, 2024" done while "2000 to 2020" is doing). Mark it done when its pull request is merged, not when it is opened. *Reason:* the maker's site changes only when `main` changes (law 7b).

**Links.**
1. A **preview** of the site gets `linkLabel: "Preview"`. Use the branch's stable Vercel address (the alias that follows the branch, of the form `vote-git-<branch>-<team>.vercel.app`), not a single deployment's address, so the link stays current as the worker pushes. For design options on one branch, one row per option, each linking `?v=a`, `?v=b` or `?v=c` on that address (the design guidance, process step 2).
2. A **document** he may want to read (the law, the model, the plan, a design spec) gets `linkLabel: "Read"`, linking the file on GitHub: on `main` once it is there, otherwise on its branch.
3. When the work is merged, a site row links the production address, https://vote-rho-pearl.vercel.app, with `linkLabel: "Open"`.
4. Check each new link once before you write it: a GitHub link with the GitHub tools, a Vercel address with the Vercel tools (`get_deployment`, `list_deployment_aliases`; project `prj_C78MKoz1D80kgE2Bfz9mMmET3Ndo`; find the team id with `list_teams`, team slug `zachs-projects-74dd78e7`). The vercel.app addresses ask for a Vercel sign-in; the maker is signed in, so that is expected, not a fault. *Reason:* a dead link on his tracker is a false row.

## Where you read what is happening

Read in this order each time you wake, and change only what has changed:
1. `STATE.md` and `plan/PLAN.md` on the orchestrator's branch `claude/project-thread-0szt08` in zwolk46/vote (`git fetch origin claude/project-thread-0szt08` and read with `git show`). The threads table and the newest log lines say what runs and what has ended. *Reason:* the orchestrator holds the state and pushes it every turn (CLAUDE.md).
2. The project's threads, with `list_threads` and, where a thread's state or output is unclear, `read_thread`. Read; never write in another thread.
3. Open and recently merged pull requests in zwolk46/vote (GitHub tools).
4. Vercel deployments of project `vote`, for new preview addresses.

## When you wake

- **Amended 2026-11-13 12:45 UTC: schedule nothing.** The maker, 12:36: "Stop any processes that run on a schedule in the background" (`RULINGS.md`). Update the tracker only when a message wakes you, then end the turn; the struck line below stands suspended until he allows schedules again. *Reason:* his word.
- ~~After each pass, schedule your next wake with `send_later` (load it with ToolSearch): **15 minutes** while any worker thread is working; after three passes in a row with nothing to change, **30**, then **60**. Go back to 15 as soon as something changes. *Reason:* he watches while work runs; a pass that finds nothing still spends his usage (OPERATIONS §4).~~
- When no worker thread is working and nothing is waiting to be shown, schedule nothing and stop. The orchestrator messages you when work starts again. *Reason:* no scheduled checks without an end (OPERATIONS §4).
- A pass that changes nothing writes nothing.

## Who you speak to

- **Nothing to the maker.** If he writes in your thread, answer him there, briefly, and tell the orchestrator. *Reason:* the orchestrator speaks for the project (`PROJECT-INSTRUCTIONS.md`, every thread, 2).
- **The orchestrator**, by message, only for a fault: a link that does not open, a row you cannot place, a tool that refuses you (and then stop that part, `_COMMON.md` 11; `PROJECT-INSTRUCTIONS.md`, every thread, 5). Batch faults into one message per pass at most. *Reason:* a thread can send about 120 messages a day to other threads (OPERATIONS §4).
- You choose nothing for the site, write no file in the repository, and open no pull request. *Reason:* your sub-end is the tracker alone (`_COMMON.md` 3).

## Done when

This brief has no end of its own while the site is being built. You stop each time nothing is running (above), and for good when the orchestrator says so.
