---
name: d3-local-data
description: D3's state legislative, local and measure data: sources, PRs, rulings, queue, rebuild and traps (as of 2026-11-13 03:45 UTC)
metadata:
  type: project
  modified: 2026-11-13T00:23:38.099Z
---

D3 thread cmsg_01FHkmcV6WaeZh9r5PfgnMbuVThyXDPxVFHnA4YqgssTSs, branch `claude/project-thread-sl6m2f`, brief `briefs/D3-data-local.md`. Method and every decision: `data/local/REPORT.md` (§6-§34).

- **Merged:** Klarner 1967-2022; MEDSL 2016-2024; NC State Board; IN 2024; LA 2023-24; NJ county gate; #82-#90; #93 VA legislatures (pre-refusal cache); #95 volume test (§29); #96 HI governor refit (§30).
- **#97 merged 2ea7c2e: held totals** (§31, `moves-held-totals.json`): OR 2024 abstract read (`intake/or_sos.py`) but unmarked (title is a file name), so both SC positions held; AZ 2022 AG `count_stage`; over-ballot test (`check-over-ballot.json`, holds TX 2024 SC); listed rows (`check-listed-rows.json`); M2 (a)-(d); c38: ID 2022 SD1 write-in (not computed), VT 2018 Chittenden from MEDSL. Next PR: district checks (ratio >3%, uncontested vs MEDSL) + 21:55 rulings (questions count; test every source; subtotal rows; type by seat).
- **Rulings:** certified source wins, only with a printed mark or the agency's own words on the linking page/records title (19:49). Third-party copies never count (21:03). A refusal binds the whole agency. Refused: MS SoS, VA DoE (18:27), NY Board (18:49), NH SoS (19:02), ME SoS (19:12), AZ SoS, Maricopa Clerk (21:02), MI SoS (11-07), Wayne County Clerk (empty reply 11-13 01:25); VT SoS 404 (no second request).
- **Merged since:** #100 district checks (d680bd4, §32), #101 VA 2023 local + held one-name rule (4831b16, §33). Resume note `handoff/workers/D3.md` holds the rulings and next steps.
- **Rebuild:** `local_volume.py check` first (the build reads it); commit code; `bash /tmp/vote-cache/rebuild.sh` (~3.5 min, nohup + ALLDONE) plus `local_la/nj/nj_leg/va_leg check`; revert stamp-only files (scratch `jdiff_head.py`); moves with scratch `r22_moves5.py <out> HEAD`. After a squash merge, merge main in.
- **Traps:** never `git commit -a`, `git stash` or `git checkout -- data/`. MEDSL total/sum rows; WA legislature filed LOCAL; local_medsl encodes expected joins/holds/over-ballot (OVER_EXPECTED), so a change stops the build. Messages to the orchestrator: 2,000 characters max. Don't print MEDSL write-in lists (VT has hundreds).

**Why:** a later thread picking up D3 should not redo sources, tests or traps.
**How to apply:** read REPORT §6-§13, §29-§34 and this file first. See [[d2-congress-data]], [[vote-president-data]], [[m2-check-computed-p]], [[d2-odd-governors]].
- **Ruled after #101:** unopposed comparator lists up to 1.5; VA no-party contests stay without p except Code-nonpartisan offices; name-keyed write-ins [inferred].
- **§34, district checks' second pass (2026-11-13, PR #106):** matcher fix (weak write-ins, compound surnames, a part beside a whole one only for the same name on two lines; shared contest to the district of its number): 284 newly tested (`check-districts-new.json`); Michigan 2022 rules (precinct joins kept in coverage v14, nameless party lines, Census 2022 BEF counties); Utah canvass and Indiana 2016 archive settle 42 flags (39 IN); Arenac clerk settles MI HD99; Rutland MEDSL taken (`OVER_SEATS_RULED` only), Franklin held; HD10/HD27 held (Wayne gave an empty reply = refusal); DC 2018 at-large 2 seats, no route; ME-02 RCV lines out. Next: (b) unopposed comparator, (c) Code-nonpartisan VA offices, (e) VA 2025 local, own PR (00:55 order). District check takes ~10 min; coverage v14 ~5 min (4 years in parallel).
