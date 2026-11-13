---
name: d3-local-data
description: D3's state legislative, local and measure data: sources, PRs, rulings, queue, rebuild and traps (as of 2026-11-13 07:10 UTC)
metadata:
  type: project
  modified: 2026-11-13T06:50:32.601Z
---

D3 thread cmsg_01FHkmcV6WaeZh9r5PfgnMbuVThyXDPxVFHnA4YqgssTSs, branch `claude/project-thread-sl6m2f`, brief `briefs/D3-data-local.md`. Method and every decision: `data/local/REPORT.md` (§6-§35); resume note `handoff/workers/D3.md`.

- **Merged:** Klarner 1967-2022; MEDSL 2016-2024; NC Board; IN 2024; LA; NJ gate; #82-#90; #93 VA legislatures; #95 volume test (§29); #96 HI governor (§30); #97 held totals (§31); #100 district checks (§32); #101 VA 2023 local (§33); #106 second pass (§34, 72d1d60).
- **Open: #109** (§35): governors at the state's count (CT/NY 2018 every line, IN 2024 certified, UT 2008 unmarked + Algara-Amlani agree (settled under 01:15); MO notes, ME 2010 not held; WV 2012 held under 19:04 at 06:52, since its page says not to rely on it until certified and A&A are a copy: `governor_counts.HELD`, chambers skips `held` in fits and last races, build_congress sets not_computed) through D2's refit (`pipeline/governor_counts.py`, then d2_labels, chambers odd/backtest/compute/history); fusion scan `check-fusion.json`; spellings summed; settle by candidate; IN 2016 SD36 MEDSL's count; two counts vs unmarked state (`two_against_state`); over-seats for every record (VT GI/Windham/Rutland MEDSL taken); zero-row counties missing; DC Board ballots 231,700. Found: MEDSL's IN 2018 file has only a BALLOTS CAST line in Washington County (18175), so over-seats not read in IN 2018, SD47 held. 06:52 answered all: index pages followed to one file count as one request (name them in REPORT's list); IN 2018 archive request allowed in the next PR.
- **Next (own PR, 00:55 order):** (b) unopposed comparator up to 1.5; (c) Code-of-Virginia nonpartisan offices; (e) VA 2025 local (564 contests in `va_elect/`); one request to enr.indianavoters.in.gov/archive/2018General for SD47 (06:52).
- **Rulings:** certified source wins only with a printed mark or the agency's own words (15:16, 19:49); third-party copies never (21:03); two counts within 0.4% beat one unmarked state count (05:15). A refusal binds the whole agency. Refused: MS, VA DoE, NY Board, NH, ME SoS, AZ SoS, Maricopa, MI SoS, Wayne Clerk (empty reply); VT SoS 404 (no second request).
- **Rebuild:** `local_volume.py check`; `local_districts.py check` (~24 min) and `compare`; commit code; `bash /tmp/vote-cache/rebuild.sh` (~4 min) plus `local_la/nj/nj_leg/va_leg/va check`; revert stamp-only files (scratch `jdiff_head.py`); moves with scratch `r22_moves5.py <out> <rev>` (local) and `hi/moves_d2.py <out> <rev>` (D2 files). After a squash merge, merge main in.
- **Traps:** never `git commit -a`, `git stash` or `git checkout -- data/`. A grep for stamp-only files can catch detail lines; check the list. The refit does not rerun build_congress, so text from chambers constants reaches records only by a step of its own (`governor_counts.mo_text`). Messages to the orchestrator: 2,000 characters max.

**Why:** a later thread picking up D3 should not redo sources, tests or traps.
**How to apply:** read REPORT §29-§35 and the resume note first. See [[d2-congress-data]], [[m2-check-computed-p]], [[d2-odd-governors]], [[m2-eighth-pass]].
