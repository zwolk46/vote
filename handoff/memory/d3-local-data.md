---
name: d3-local-data
description: D3's state legislative, local and measure data: sources, PRs, rulings, queue, rebuild and traps (as of 2026-11-07 21:55 UTC)
metadata:
  type: project
  modified: 2026-11-07T21:53:31.058Z
---

D3 thread cmsg_01FHkmcV6WaeZh9r5PfgnMbuVThyXDPxVFHnA4YqgssTSs, branch `claude/project-thread-sl6m2f`, brief `briefs/D3-data-local.md`. Method and every decision: `data/local/REPORT.md` (§6-§31).

- **Merged:** Klarner 1967-2022; MEDSL 2016-2024; NC State Board; IN 2024; LA 2023-24; NJ county gate; #82-#90; #93 VA legislatures (pre-refusal cache); #95 volume test (§29); #96 HI governor refit (§30).
- **#97 merged 2ea7c2e: held totals** (§31, `moves-held-totals.json`): OR 2024 abstract read (`intake/or_sos.py`) but unmarked (title is a file name), so both SC positions held; AZ 2022 AG `count_stage`; over-ballot test (`check-over-ballot.json`, holds TX 2024 SC); listed rows (`check-listed-rows.json`); M2 (a)-(d); c38: ID 2022 SD1 write-in (not computed), VT 2018 Chittenden from MEDSL. Next PR: district checks (ratio >3%, uncontested vs MEDSL) + 21:55 rulings (questions count; test every source; subtotal rows; type by seat).
- **Rulings:** certified source wins, only with a printed mark or the agency's own words on the linking page/records title (19:49). Third-party copies never count (21:03). A refusal binds the whole agency. Refused: MS SoS, VA DoE (18:27), NY Board (18:49), NH SoS (19:02), ME SoS (19:12), AZ SoS, Maricopa Clerk (21:02).
- **Queue:** (1) District-checks PR (orchestrator 21:26): across every Klarner-MEDSL overlap year, flag (a) district ratio off 1 by >3%, (b) Klarner uncontested where MEDSL has another candidate beyond scattered write-ins. A write-in (MEDSL mark or state's W/I) is not a ballot opponent: apply the write-in rule. Settle from the state only if cached or it answers one request; else 19:04 rules (gap >=5% held, <5% kept with note). List every flag with outcome; count p moved/lost/gained by level and year. M2 compares in its 7th pass. Known: VT 2018 Bennington off. M2 will send NJ 2024 Bergen, ND 2024, NY-25, WA-08, NH House. (2) VA 2023 local from the cache (own PR).
- **Rebuild:** `local_volume.py check` first (the build reads it); commit code; `bash /tmp/vote-cache/rebuild.sh` (~3.5 min, nohup + ALLDONE) plus `local_la/nj/nj_leg/va_leg check`; revert stamp-only files (scratch `jdiff_head.py`); moves with scratch `r22_moves5.py <out> HEAD`. After a squash merge, merge main in.
- **Traps:** never `git commit -a`, `git stash` or `git checkout -- data/`. MEDSL total/sum rows; WA legislature filed LOCAL; local_medsl encodes expected joins/holds/over-ballot (OVER_EXPECTED), so a change stops the build. Messages to the orchestrator: 2,000 characters max. Don't print MEDSL write-in lists (VT has hundreds).

**Why:** a later thread picking up D3 should not redo sources, tests or traps.
**How to apply:** read REPORT §6-§13, §29-§31 and this file first. See [[d2-congress-data]], [[vote-president-data]], [[m2-check-computed-p]], [[d2-odd-governors]].
