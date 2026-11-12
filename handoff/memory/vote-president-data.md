---
name: vote-president-data
description: Facts about the presidential data (D1) that a later thread would otherwise rediscover: rules applied, 538 file quirks, PR, cache
metadata:
  type: project
  modified: 2026-11-07T04:30:45.628Z
---

D1 (thread "Gather presidential data by state") wrote data/president/<year>.json 1976–2024, pipeline/president.py, college.py, own_forecast.py. Data PR zwolk46/vote#23 merged 2026-11-07 04:34 UTC; the core PR #14 merged earlier.

- The orchestrator's 538 rules (2026-11-07 04:12 and 04:20), which also apply to Congress (D2):
  - Use the last forecast dated before Election Day. 538's 2008 file has Election Day only; it is kept as the check, marked.
  - Keep 538's implied sd only where its estimated relative error is under 20%. Otherwise fall back to the model's own forecast, marked.
  - Units where other candidates hold at least 1% of the chance, or where the chance is exactly 0 or 1, always fall back.
- 538's checking-our-work chances are counts of runs: 2016 steps by 0.00005 (20,000 runs) and 2020 by 0.000025 (40,000 runs). Both were measured; the run counts are inferred.
- No source read says which 2016 model 538 showed by default; polls-plus is used first and marked so.
- The own forecast uses 538's last national poll average before Election Day (2024: 12 Sept, the last available). The eve version beats 9 September in the back-test, Brier 0.073 against 0.081.
- Raw-file caches live outside the repo: D1's at ~/.cache/vote-intake (pipeline/fetch.py); D2's at /tmp/vote-cache (congress_common.fetch). Both are lost when the container ends. Merging the two fetch helpers is a follow-up.

**Why:** the orchestrator ruled these to make the presidency and Congress match. The run-count facts set the error rule.
**How to apply:** reuse the same rules for any 538 forecast intake; see data/president/REPORT.md for checks and follow-ups. Related: [[vote-project]]

Orchestrator's settlements (2026-11-07 04:38), after the brief closed:
- The 2024 forecast is accepted as marked: 538's average of 12 Sept, with errors fitted to the 9 Sept averages of earlier cycles.
- The PS 2024 forecast stays unused: it has no licence and is dated 1 Sept.
- pipeline/fetch.py, which refuses cross-site redirects, becomes the one fetch helper. fec_president.py folds into D2's fec_federal_elections.py. D2 does both, later.
- Queued as follow-ups: the Clerk's PDFs for 1920–1972, the Downballot district data, and the FEC's PDFs for 1984–1992.
- M2 (Fable) checks D1's p independently.

After M2 (amendment of 2026-11-07 05:58):
- The 538 rule now keys on p's error, not the sd's. p's error is |z²−1| × the sd's error from the chance, combined with the mean's rounding at factor 1, and must be under 20%. This is the same rule as D2's chambers.py.
- The Economist's W is marked thin below 30 weighted draws (OH, IA, CO).
- Both changes are in PR #33, merged 2026-11-07 07:08 UTC. The brief is done.
