---
name: d3-local-data
description: D3's state legislative, local and measure data: sources, PRs, rulings, queue, rebuild and traps (as of 2026-11-07 21:55 UTC)
metadata:
  type: project
  modified: 2026-11-13T00:23:38.099Z
---

D3 thread cmsg_01FHkmcV6WaeZh9r5PfgnMbuVThyXDPxVFHnA4YqgssTSs, branch `claude/project-thread-sl6m2f`, brief `briefs/D3-data-local.md`. Method and every decision: `data/local/REPORT.md` (§6-§31).

- **Merged:** Klarner 1967-2022; MEDSL 2016-2024; NC State Board; IN 2024; LA 2023-24; NJ county gate; #82-#90; #93 VA legislatures (pre-refusal cache); #95 volume test (§29); #96 HI governor refit (§30).
- **#97 merged 2ea7c2e: held totals** (§31, `moves-held-totals.json`): OR 2024 abstract read (`intake/or_sos.py`) but unmarked (title is a file name), so both SC positions held; AZ 2022 AG `count_stage`; over-ballot test (`check-over-ballot.json`, holds TX 2024 SC); listed rows (`check-listed-rows.json`); M2 (a)-(d); c38: ID 2022 SD1 write-in (not computed), VT 2018 Chittenden from MEDSL. Next PR: district checks (ratio >3%, uncontested vs MEDSL) + 21:55 rulings (questions count; test every source; subtotal rows; type by seat).
- **Rulings:** certified source wins, only with a printed mark or the agency's own words on the linking page/records title (19:49). Third-party copies never count (21:03). A refusal binds the whole agency. Refused: MS SoS, VA DoE (18:27), NY Board (18:49), NH SoS (19:02), ME SoS (19:12), AZ SoS, Maricopa Clerk (21:02).
- **Queue (2026-11-12):** (1) District-checks PR #100 merged 2026-11-13 as d680bd4 (REPORT §32; coverage v12; 197 p no longer computed; moves-district-checks.json lists >1% moves, counts the rest). Resume note `handoff/workers/D3.md` has the rulings (21:21-22:42) and next steps. Thread paused 2026-11-07 23:31 on a usage limit, resumed 11-12 23:07. (2) PR #101 opened 2026-11-13 00:52: VA 2023 local (pipeline/local_va.py, REPORT §33; no party in the source, class 'party not given'; name-keyed options = write-ins; gate (a)-(d) proposed) + one-name ruling (23 p 0 lost). (3) 22:19 item 5 (D2 checks, no p), with DC 2018 at-large Council: seat count 2 from DC BOE (one request) or DC Code, keep not computed (one-seat-per-majority-party rule), over-ballot per seat (orchestrator 11-13 00:17; details in the resume note).
- **Rebuild:** `local_volume.py check` first (the build reads it); commit code; `bash /tmp/vote-cache/rebuild.sh` (~3.5 min, nohup + ALLDONE) plus `local_la/nj/nj_leg/va_leg check`; revert stamp-only files (scratch `jdiff_head.py`); moves with scratch `r22_moves5.py <out> HEAD`. After a squash merge, merge main in.
- **Traps:** never `git commit -a`, `git stash` or `git checkout -- data/`. MEDSL total/sum rows; WA legislature filed LOCAL; local_medsl encodes expected joins/holds/over-ballot (OVER_EXPECTED), so a change stops the build. Messages to the orchestrator: 2,000 characters max. Don't print MEDSL write-in lists (VT has hundreds).

**Why:** a later thread picking up D3 should not redo sources, tests or traps.
**How to apply:** read REPORT §6-§13, §29-§31 and this file first. See [[d2-congress-data]], [[vote-president-data]], [[m2-check-computed-p]], [[d2-odd-governors]].
- **Ruled 2026-11-13:** a one-name record whose counts are held is not computed at every level (write-in test unreadable); held one-name local records lose p 0 in D3's next PR.
- **#101 merged 4831b16 (2026-11-13):** held one-name rule built; VA 2023 local (1,448). Ruled after: unopposed comparator lists up to 1.5; VA no-party contests stay without p except Code-nonpartisan offices; name-keyed write-ins [inferred] + refuting count; 2025 local (564) next, own PR.
