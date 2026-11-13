---
name: d3-local-data
description: D3's state legislative, local and measure data: sources, PRs, rulings, queue, rebuild and traps (as of 2026-11-13 10:56 UTC)
metadata:
  type: project
  modified: 2026-11-13T06:50:32.601Z
---

D3 thread cmsg_01FHkmcV6WaeZh9r5PfgnMbuVThyXDPxVFHnA4YqgssTSs, branch `claude/project-thread-sl6m2f`, brief `briefs/D3-data-local.md`. Method and every decision: `data/local/REPORT.md` (§6-§39); resume note `handoff/workers/D3.md`.

- **Merged:** Klarner 1967-2022; MEDSL 2016-2024; NC Board; IN 2024; LA; NJ gate; #82-#90; #93 VA legislatures; #95 volume test (§29); #96 HI governor (§30); #97 held totals (§31); #100 district checks (§32); #101 VA 2023 local (§33); #106 second pass (§34, 72d1d60); #109 governors' counts and third pass (§35, b35fede); #111 (§36, 11c852d).
- **#109** (§35, merged 07:38): governors at the state's count (CT/NY 2018 every line, IN 2024 certified, UT 2008 two witnesses; WV 2012 held, out of every input); fusion scan; spellings summed; settle by candidate; two counts vs unmarked state; over-seats on every record; zero-row counties missing; DC ballots 231,700. M2 checked it in #110 (§19).
- **#111 merged** (§36, 11c852d): VA 2023 comparators listed; VA local offices' party by Code (school boards 22.1-57.3 E, soil and water 10.1-523 A, others "party not given", 24.2-613 B); VA 2025 in (`ODD_YEARS`); IN 2018 Senate file settles SD29/31/47. Refused once each, never retry: Ballotpedia, FindLaw, vacode.org (find sections by law.lis search or ask first).
- **#113 merged** (§37, 9ad2d3d): IN 2018 House settled. **Recount zone** (§38, own PR; 09:58/10:06/10:12): VTP WP11 and FairVote read once at 10:00, no more requests; zone 0.87% x p.n (gross [inferred]), check 1.06%, sensitivity 2.49%; near = zone >= n*sd/3 (like-race sd from _p_like's device); p unchanged; 1,045 notes (`local_recount.py build` after the builders), `data/local/recount-zone.json`. #115 merged (f643407). **Singer 2020** (§39, `local_singer.py`, `check-2020-singer.json`, `local.py singer_checks`): 10:44 ruling: §32's rules act on Singer's count as on MEDSL's; notes give both counts and D3's reason [inferred]; ME rows county-only so holds stand; MT canvass (sosmt.gov, one request) agrees with Singer on HD 3/19/84, which take Singer's count. 17 held, 5 noted. Jones waits on the maker (licence).
- **Rulings:** certified source wins only with a printed mark or the agency's own words (15:16, 19:49); third-party copies never (21:03); two counts within 0.4% beat one unmarked state count (05:15). A refusal binds the whole agency. Refused: MS, VA DoE, NY Board, NH, ME SoS, AZ SoS, Maricopa, MI SoS, Wayne Clerk (empty reply); VT SoS 404 (no second request).
- **Rebuild:** `local_volume.py check`; `local_districts.py check` (~24 min) and `compare`; commit code; `bash /tmp/vote-cache/rebuild.sh` (~4 min; ends with `local_recount.py build`) plus `local_la/nj/nj_leg/va_leg/va check`; revert stamp-only files (scratch `jdiff_head.py`); moves with scratch `r22_moves5.py <out> <rev>` (local) and `hi/moves_d2.py <out> <rev>` (D2 files). After a squash merge, merge main in.
- **Traps:** never `git commit -a`, `git stash` or `git checkout -- data/`. A grep for stamp-only files can catch detail lines; check the list. The refit does not rerun build_congress, so text from chambers constants reaches records only by a step of its own (`governor_counts.mo_text`). Messages to the orchestrator: 2,000 characters max.

**Why:** a later thread picking up D3 should not redo sources, tests or traps.
**How to apply:** read REPORT §29-§36 and the resume note first. See [[d2-congress-data]], [[m2-check-computed-p]], [[d2-odd-governors]], [[m2-eighth-pass]].
