---
name: vote-no-schedules
description: Zach 2026-11-13 12:36: no scheduled tasks in the vote project, and Vercel must not email him (branch previews and bot comments off)
metadata:
  type: feedback
---
Zach (project chat, 2026-11-13 12:36 UTC): "Stop any processes that run on a schedule in the background, whatever makes Vercel send me emails".

Done that turn: deleted the project's two scheduled tasks (T1's tracker pass, the orchestrator's phase-3 deadline); T1 told to schedule nothing. The emails were GitHub notices of vercel[bot]'s comment on each PR (one per branch preview). vercel.json on main (#121, b85f960): git.deploymentEnabled {"claude/**": false}, github.silent true. The Vercel connector cannot change project settings (403).

**Why:** the reminders and the per-PR bot comments filled his inbox and ran without him.
**How to apply:** no send_later, create_trigger or polling loops in this project until he allows it; threads act only when woken. Before X1 or a build worker needs a preview, ask him, then re-enable previews in vercel.json through a PR. Ruling in RULINGS.md (2026-11-13 12:36). The account's other projects' routines (morning brief, heartbeat, design-system watches) were left as they are. See [[vote-tracker]], [[vote-restart]].
