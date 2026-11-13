---
name: x1-design-thread
description: Where X1's first-screen options and X2's explainer work live (branches, preview URLs, real-data build, what waits on Zach)
metadata:
  type: project
  modified: 2026-11-07T12:50:00.000Z
---

X1 design thread (cmsg_01FHkmcV6WaeZh9r5PfgnMbuVvYhNiCZhk78N7b9DQjyTh), as of 2026-11-07 12:50 UTC:
- Spec: design/DESIGN-SPEC.md; v1 merged (#16), v2 merged (#19).
- First-screen options: branch claude/project-thread-ozfwbq-options (head 01a2762, real data); preview alias
  https://vote-git-claude-project-thread-o-6fbb1a-zachs-projects-74dd78e7.vercel.app (?v=a Ruler, ?v=b Ballot; behind Vercel sign-in).
- Explainer: branch claude/project-thread-ozfwbq-explainer (head 8f0ee05, options merged in); preview alias
  https://vote-git-claude-project-thread-o-f3f92e-zachs-projects-74dd78e7.vercel.app/?page=how&v=a (A scroll) and &v=b (B steps).
  Code in src/explainer/. /how approved as the address (orchestrator 06:35): the post-pick PR may touch vercel.json for that rewrite.
- Real data (orchestrator 09:26, 09:31): src/data/build-field.mjs reads data/ and writes src/data/field.json (run from repo root
  after data/ changes). Every contest 1969-2024 with a p, as dots of 10. Lead = the state with the highest chance in 2024
  (NV), never "closest" (orchestrator 11:05; same for GSE 2008 in the explainer); WV = lowest chance. Named lows = 2024's,
  only from p that are the contest's own (state legislatures: forecast_scope "district (class A/B)"); class C and
  like-race routes are lighter dots. Lean (p.note "so p may be low") = dashed arrow, House only: governor and Senate notes
  ruled out (LEAN_OUT in the build) until D2 removes them. A dot or figure with no population fades per person, without
  words (no "No figure yet", no "no population in the data yet": orchestrator 11:05, 12:01).
  Local races and measures wait for M2's last item.
- Resume note: handoff/workers/X1.md on the options branch (b6e9660, 22:20). field.json built from main as of #71; rebuild before any PR.
- Waiting on Zach's picks (A/B first screen; A/B explainer); then one PR to main per pick without the picker; then stop.
  Holding (orchestrator 11:40, again after 12:01). State legislative populations now read from data/population/ (#71).
  Explainer's first step made lighter (orchestrator 12:35): worlds scene copies its 4,000 ballots from cached grids
  (scenes.js grids(); dot-by-dot fallback when no room), Measure no longer re-renders; motion 16.8 ms worst at CPU x4.
- Option C dropped (Zach 04:09: awful on a phone); its idea is in the explainer.
- Checks: design/checks/fit.cjs, motion.cjs, settle.cjs. Never run motion alongside another browser job (CPU contention).
  Dense piles are thinned (Field.jsx thinStep) so 9,000+ dots move within a frame at 390 px CPU x4.
- Picker guard is hostname-only (VITE_VERCEL_ENV not exposed in this project's Vercel builds).
- Cold readings: design/FIRST-SCREEN-READINGS.md, design/EXPLAINER-READINGS.md. Text ledger: design/TEXT-LEDGER.md.

**Why:** a later thread picking up X1/X2 would otherwise have to rediscover the branches, the build script and the rules for which p may be named.
**How to apply:** after Zach picks, rerun build-field.mjs on the latest main, then the chosen option goes to main in its own PR without the picker. Related: [[vote-project]], [[m2-check-computed-p]], [[d3-local-data]]
