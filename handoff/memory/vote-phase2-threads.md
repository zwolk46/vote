---
name: vote-phase2-threads
description: Thread ids and briefs for the vote site's phase 2 workers (tracker, presidency data, Congress data, design), started 2026-11-07
metadata:
  type: project
  modified: 2026-11-07T03:08:49.910Z
---

Started 2026-11-07 03:08 UTC by the coordinator at the orchestrator's ask, from briefs on `main` (#13), on the networked environment:
- T1 "Keep the vote tracker current", Sonnet 5.5 xhigh, `briefs/T1-tracker.md`: cmsg_01FHkmcV6WaeZh9r5PfgnMbuByWBE5rw5LTK6xKGeqevgf. Keeps [[vote-tracker]] current.
- D1 "Gather presidential data by state", Opus 5.5 xhigh, `briefs/D1-data-president.md`: cmsg_01FHkmcV6WaeZh9r5PfgnMbuCWdWPRkhAafpzm5UUF9z22. Writes `pipeline/core.py` first (D2 imports it).
- D2 "Gather Senate, House and governor data", Opus 5.5 xhigh, `briefs/D2-data-congress.md`: cmsg_01FHkmcV6WaeZh9r5PfgnMbu4yiCuHbbX3iQD4KYFb7W48.
- X1 "Design the site's first screen", Opus 5.5 xhigh, `briefs/X1-design.md`: cmsg_01FHkmcV6WaeZh9r5PfgnMbuVvYhNiCZhk78N7b9DQjyTh.

Later (2026-11-07):
- D1 done 04:37 (#14, #23 merged); D2 done 04:31 (#18, #22), to wake once for the VP tie vote and one fetch/FEC intake.
- D3 "Gather local, legislative, primary and measure data", Opus 5.5 xhigh, `briefs/D3-data-local.md`: cmsg_01FHkmcV6WaeZh9r5PfgnMbuVThyXDPxVFHnA4YqgssTSs (started ~04:30; told to keep files compact, stop before 100 MB).
- M2 "Check every computed vote chance", Fable 5.1 xhigh, `briefs/M2-check-computed-p.md`: cmsg_01FHkmcV6WaeZh9r5PfgnMbuCEUo7XmYgNjtfLdxDRBTML (started 04:38).

- D4 "Gather voting costs and tie laws", Sonnet 5.5 xhigh, `briefs/D4-data-cost-and-ties.md`: cmsg_01FHkmcV6WaeZh9r5PfgnMbuGA4pBoUJj1By51aSAkx3E9 (started 07:09).
- D1 done 07:08 (#33); M2 done 05:56 (#26); M2 second pass started 07:42 (#47).
- D4 done 09:09 (#40, #41, #43, #50); NH tie law retry queued.
- 08:36 rule: a forecast change is adopted only if its out-of-sample gain survives leaving out any one scored year, no tested cell worse (briefs D2, D3 amended, #48).

**Why:** `plan/PLAN.md` phase 2 (data with design alongside), under law 7a.
**How to apply:** the plan and `STATE.md` on the orchestrator branch are the record; this is only a pointer. Working at 09:09: D2 (half-life k, inc 2/3), D3 (Indiana, #31 test, exact-sum fix, LA, NJ, local thresholds), M2 (item 4, end report).
