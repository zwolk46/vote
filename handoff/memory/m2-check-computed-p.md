---
name: m2-check-computed-p
description: M2's independent check of every computed p (president, Congress, governors, local, measures): scripts checks/m2/c1-c40, report checks/M2-REPORT.md (§10 third pass ... §13 sixth, §14 seventh), PRs #69, #89, #91, #94 merged, seventh pass PR #NNN (c38 volume check, c39 comparison, c40 PR checks); eighth pass next (#96, #97)
metadata:
  type: project
---

M2 (thread cmsg_01FHkmcV6WaeZh9r5PfgnMbuCEUo7XmYgNjtfLdxDRBTML, branch `claude/project-thread-pbr8zl`) re-derives every p from its own pools and formulas; nothing in `pipeline/` or `model/` is imported (a pipeline rule that must be applied is copied into the script, which says so). `sh checks/m2/run_all.sh` writes `checks/m2/OUTPUT.txt` (c1–c40, ~60 min once the raw-file summaries exist; c40 makes four git worktrees under the cache). Report `checks/M2-REPORT.md`: §10 third pass (#60–#81, PR #69 merged as bdac161), §11 fourth (#82/#84/#85, PR #89 merged as a2a4b0a), §12 fifth (#86/#87/#88, fixed end a2a4b0a; PR #91). Each pass checks the PRs merged since the last fixed end; "anything later goes to the next pass".

Tools, fetch scripts and gotchas: [[m2-fifth-pass-tools]].

Sixth pass (c37, #90): all of it reproduces (123 moves, 8 joins from the raw rows, WA's export, 14 holds by coverage + AZ CC, ND's 22 judgeships, over-ballot holds OH/MI 2018, HI/MI 2022, 20 retypes, 163 quotes, 49 reasons' counts). Readings: AZ 2024 CC's 1-seat piece takes in Santa Cruz's rows filed under districts 001-003 at magnitude 3; MI 2022 AG/Governor totals 89/67 votes apart from D3's (write-in lines), ratio 1.39 either way.

Results so far: every moves file (#82–#88) equals my diff; no p off beyond rounding; fourth pass: 133 statewide p and 304 LA p reproduce; fifth pass: D3's 1,021 whole questions, the 165 towns/townships (Census tests), 134 county questions' precinct counts and 20 partial ones reproduce; #87's 409 rows and 119 like-race counts reproduce; #88's 244 rows, the 142 statewide judges (every-county test from the raw files, 2 unopposed 2008/2010 seats a reading), 16 officers, 21 lost p (pools 8 and 94) and NM's PEC page reproduce (c36).

**Open readings for the orchestrator (nothing chosen by M2):** Hoboken 2024 question recorded as an unopposed office; D3 REPORT §15 "69 of 103 are NC 2023 school boards" wrong; #75's ×1.42 is the window rule switching at exactly 10 rows; LA statute pages do not say ties are by lot; governors' note reads "stands, fewer"; local_sizebins.py docstring says 2015 where FIRST_FIT_YEAR is 2014; moves-towns-counties.json code B's words ("only in its note") fit its Q rows better; D3's §23 example "Latah 1 of 34" is right but the recall's other answer is found under "JUDI FULLER - FOR RECALLING…" (D3 holds it as one answer only). Ruled at 16:53 (closed): the six quote-page URLs, the "referred" proposers, Perry.

Passes: fifth merged #91 (b9e0702); sixth (brief 18:13): #90, fixed end b9e0702, c37 + REPORT §13, PR #94 merged as 46825da; seventh (fixed end 46825da): #92, #93, #95 + the volume check, c38–c40 + REPORT §14, PR #NNN; brief and findings in [[m2-seventh-pass-brief]] and [[m2-input-volume-check]]. Seventh-pass results: the three moves files equal my diffs; NJ's gate holds from the lists (my own pdftotext reader; 3 texts cut short in D3's records); the 120 new p and the #92/#93 moves reproduce (within 5e-4 of D3's ratios); like-race pools must leave out the held records and recounts (held_out) to match D3's.

**Why:** the orchestrator decides every reading; M2 reports and chooses nothing. **How to apply:** a later M2 thread starts from `checks/M2-REPORT.md` §13 and these readings; rerun c28 (and c8/c9/c13/c16) if governor codes change, c29/c24/c35 for office types, c27/c33/c34 for local thresholds and whole questions, c36 for statewide judges and commissions, c31 for statewide joins, c32 for certified counts.
