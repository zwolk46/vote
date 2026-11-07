# W22: the home page, uncluttered (a table of sections, researched)

Read first, whole: `LAW.md`, `the-law-for-agents.md`, `RULINGS.md` (from 2026-11-05 16:44 on; in particular 19:04), `STATE.md`, `briefs/_COMMON.md`, research/plan/2026-11-05-A-maker-principles.md (the visual hierarchy principles).

**The maker, 19:04 UTC 11-05, verbatim in RULINGS.md:** "the main page, the home page, the country page, all names for the same page, have gotten a little bit cluttered. So maybe, I don't know, somewhere there could be like a table of sections or something like that, but really nicely and beautifully implemented with nice motion and things. And you could do some research to find out the best way to do that."

**1. Research first.**
- Inventory the home page as it is today: each section, its job, its height at 390 and 1280, and what a reader does there.
- Look at how the best long pages organise themselves: news live pages and election-night pages (the survey of election sites in inherited/ and research/), Mobbin (sections, tables of contents, scrollspy, anchored chips), 21st.dev (table-of-contents and scrollspy components; the key is API_KEY_21st; retrieve code, no AI generation) and Details.
- Write what you found and your recommendation, with reasons, to research/design/2026-11-05-W22-home-sections.md.
- Bring the recommendation to the orchestrator before building. *Reason:* the maker asked for research to find the best way.

**2. Then build.**
- A table of sections that shows where you are and takes you anywhere: for example a sticky chip row on the phone and a side rail on desktop, with the current section marked as you scroll. Use motion (src/lib/motion.js and the motion spec), not glows or pulses (principles 2b).
- Decluttering may also mean merging, reordering or folding sections. Propose it; do not drop content without the orchestrator's word.
- Reduced motion; 44 px targets; no layout jump. W19 owns jumps site-wide; tell it what you change.
- *Reason:* the maker's words, and the principles.

Branch build/home-sections from origin/main. Preview on probe/home-sections; if no deployment appears, use create_deployment with forceNew. If the connector fails, stop and tell.

Shots and a short recording at 390 and 1280, light and dark, in /mnt/project-files/design/home-sections/.

Do not touch lib/gate/ (W18) or the search (W21).

Report to the orchestrator thread. Do not merge.

Model: Opus 5.5, effort high.

**Added at 19:06 (RULINGS):**
- Decide deliberately what information matters most and comes first. The broad order is right, but the pinned races sit too far down.
- Separately, redesign the pinned race card for a called race: it is "not as beautiful as it could be".
