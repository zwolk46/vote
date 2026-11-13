---
name: m2-section-21-scope
description: M2's section 21 (2026-11-13): D3's #115 (f643407, REPORT §38, the recount zone beside p) checked in c51, merged as PR #117 (30480c35, 10:46 UTC); result, readings (sent to D3 for its Singer PR); section 22 is D3's Singer 2020 PR
metadata:
  type: project
  modified: 2026-11-13T10:41:46.090Z
---

The orchestrator, 2026-11-13 10:34 UTC (verbatim): "D3's #115 is merged as f643407 (REPORT §38, the recount zone). Check it in section 21, with its end at f643407. It covers pipeline/local_recount.py; the zone at 0.87% gross against n × sd (like-race spreads from _p_like's normal device); the 1,045 notes near at 0.87%, each line equal to the old one with its note taken out; and recount-zone.json's 15,122 near at any rate. Check also the counts at 1.06% and 2.49% (2.49% floor 0.627), the 1,838 tail races, and the figures quoted from Ansolabehere and Reeves (VTP WP11, Table 2, p. 5) and FairVote, against their sha256. No p moves by my compare. D3 next takes Singer's 2020 results in its own PR."

Result (c51 §51.1–51.4, REPORT §21): everything as D3 recorded it. BEFORE e3e9b921, AFTER f6434077. 162 files changed, 156 record files; 1,045 records carry one zone note each (lower 611, upper 30, local 404), each equal with the note taken out, no p moved, 267,309 records unchanged. MATH §5.10's table reproduced within 0.0009 by scipy quad and my trapezoid. 107,111 records with p > 0; near 1,045 / 1,086 / 15,122 by level and route equal; gain ranges 0.909–0.947, 0.875–0.957, 0.627–4.263; tails 1,838 (p ≤ 3.59e-6) / 3,729 / 17,055 equal; the 15,122 rows field by field, gain within 1e-3; my note text (D3's note_text copied) equals the record's in 1,045 of 1,045. Sources: the VTP PDF's sha and bytes equal, 13 quotes found, no licence words, 10 pages; FairVote's page: quotes found, no licence words, but sha differs (3bffc3c9…, 215,159 bytes vs D3's 2b5dbfcf…, 215,078): three nonce attributes, per-request.

Readings: FairVote's hash cannot be checked across reads (only its text); D3's "46 under 2 votes" is the listing's tenth-of-a-vote rounding (48 by the exact zone, 31 under 1.5); nothing turns on it. Own run at OUTPUT.txt lines 8225-8296 (10:41 UTC, b2e445c0). PR #117 (checks at 390432ab, note commit 0c115345) merged by the orchestrator as 30480c35 at 10:46 UTC, after his #116 (3a0aa81b, state after #113 to #115); main merged into the branch (824ce0b8), note current. His words: the two readings go to D3 for its Singer PR (a hash of FairVote's text beside the page's; the exact zone's 48 under 2 votes, 31 under 1.5). Next: section 22 on D3's Singer 2020 PR when he names its commit.

Lessons: D3's listing keys its gain cache by (round(mu,6), round(sd,6), rate, at); the spread rule reads forecasts[0].share.sd first, then p.f_half, then p.f_t with p.threshold; the levels are state-lower, state-upper, local, primary, measure.

**Why:** each section checks one merged PR at its own end. **How to apply:** see [[m2-eighth-pass]]; the next section is D3's Singer 2020 PR.
