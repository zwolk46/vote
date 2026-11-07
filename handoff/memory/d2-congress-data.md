---
name: d2-congress-data
description: What D2 built for Senate/House 2006-2024 and governors 1978-2024 (sources, method D2-v3, 538 rule, calibrations, robustness test, open findings), as of 2026-11-07 11:30 UTC
metadata:
  type: project
  modified: 2026-11-07T07:03:16.589Z
---

D2 (thread cmsg_01FHkmcV6WaeZh9r5PfgnMbu4yiCuHbbX3iQD4KYFb7W48) built data/senate|house/<even year>.json 2006-2024 and data/governor/<even year>.json 1978-2024: 5,324 contests, p for 4,106 (1,066 under 538), 176 p = 0, 1,042 not computed. Method and checks: data/congress/REPORT.md (§0.1 M2 second-pass fixes, §0.2 incumbency, §0.3 round 5, §0.4 round 4).

PRs: #18, #22 (D2-v1), #29 (D2-v2), #32 (D2-v3, round 3), #35 (round 4) merged. #38 (round 5, D2-v4) merged 2026-11-07 07:41; #45 (incumbency fix) merged 08:20. #51 (M2 second pass #47: specials' lean, FEC joined D/R lines, VP pi with ME/NE districts, round 5 retaken) merged 08:54. #53 (near-tie retaken: House stands, Senate out, p.near_tie_not_of_record; governor p.note via history) merged 09:08.

D2-v3 (pipeline/chambers.py):
- Fit on earlier cycles only; K_MIN 4 with both parties' presidents. FIT_FROM: Senate 1982 (MEDSL, incumbency inferred), House 2006, governors 1978.
- Governors before 2006 from Algara and Amlani county returns (doi:10.7910/DVN/DGUMFI, CC0, Rdata) via pipeline/intake/algara_amlani.py + rdata_reader.py (pure-Python R reader). Incumbency = authors' seat_status. Missouri before 2006 excluded everywhere (rows 7% D / 2% R short of Cha; Kansas City inferred missing).
- House 2008-2012 takes the Senate's national terms (c, s_a, ZtZ_inv) from the Senate's earlier cycles (model.national_from); stage one on House cycles. House 2006 still not computed (needs FEC 2004).
- Calibration: sd × k, k = RMS of z over the level's earlier out-of-sample years, CAL_MIN 3. Lowers p in safe races (House 2024 sum −11%).

- Near-tie calibration (round 4, D3's rule): model's own p × F/(1+(F−1)q), F = seen/expected at 49-51% on earlier years (own level if ≥30 expected, else pooled). Not governors; 538 not calibrated. Of record since #53: House one factor; Senate none (fails robustness).
- Robustness test (orchestrator 08:35, fixed from then on): a variant is adopted only if it raises log score, moves the 49-51% count nearer, worsens no tested safe-band cell, AND the same holds leaving out any one scored year. Under it (#51) round 5's House shrink and governor t4 fail; no variant of record, every level D2-v3. Applies to old changes too (08:54).
- The intake cache (~/.cache/vote-intake) is lost on restart; rebuild with the pipeline/intake scripts (xlrd via pip --target /usr/local/lib/python3.13/site-packages so -I sees it) before build_congress.py and chambers.py compute; reproduces every p exactly.

Open findings for the orchestrator:
- #58 (09:26 ask, last): near-even note on House/Senate model's-own normal p (105 vs 87.5; 17 vs 11.1, 2010-2024); FEC 2004 intake works, but House 2006 not computed: no source says which states kept 2004 lines to 2006 (FEC names TX 15/21/23/25/28 only; Wikipedia API refused). Merged 09:38. #67 (11:16 ruling): lean note stands only where share-line and votes-line tests agree; M2's counts keep House note, drop Senate+governor.
- Round 6 (#55, merged 09:26): half-life k and Cha inc (a) 1-2 / (b) 1-3 tested on D2-v3 under the robustness test; none adopted (near-even counts further). M2: shortfall sits in the mean. Design fixed in /mnt/project-files/d2/recent-k-design.md.
- The Senate's terms also beat the House's own over 2014-2024 (not adopted).
- Cha inc 2 (special-elected) and 3 (appointed): the fit counts only 1; tested in round 6, not adopted.
- Cha vs Algara-Amlani disputes (WV/UT/ME/HI) need a third source.

**Why:** a later data thread needs these sources, rules and open options without asking again.
**How to apply:** extend the existing intake scripts rather than writing new ones (one script per source, plan §3a). [[research-source-access]] [[vote-system-pointers]] [[m2-check-computed-p]] [[d3-local-data]]
