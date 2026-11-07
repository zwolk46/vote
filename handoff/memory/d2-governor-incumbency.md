---
name: d2-governor-incumbency
description: D2's check of every governor nominee's incumbency code against the record's last race (PR #78, 2026-11-07): 17 fixes under the 13:43 rulings, roster sources and refusals, the House near-tie switch test
metadata:
  type: project
  modified: 2026-11-07T14:21:21.700Z
---

PR #78 (merged 2026-11-07 14:20 UTC) implements the orchestrator's ask of 13:06 UTC and its two rulings of 13:43. Code: `pipeline/governor_incumbency.py` (check / moves / fetch). Table: `data/congress/governor-incumbency.json`. Write-up: REPORT §10.

- **Survey.** 613 governor contests, Louisiana apart: 37 disagree (kinds A 4, B 32, C 1). The join (#45 `cha_entry`) agrees with Cha's codes by exact name on 254 of 254, so every disagreement is the source's own.
- **Successor rule (13:43, fixed before any score).** "A successor who was not elected to the seat is not the incumbent, and this holds in every year." Cha's 2 and 3 read as 0 (§0.2). No new variant is to be added.
- **Fixed (17).**
  - NJ 2021 Murphy 0→1 and AR 2018 Hutchinson 0→1.
  - KY 2019 Beshear and VT 2020 Zuckerman 1→0.
  - MN 1982 Perpich AA → Republican Open Seat.
  - Ten AA successors confirmed by rosters → Open Seat: AL94, AR94, AR98, AZ78, AZ98, CT82, MN78, NV90, TX02, VT92.
  - Brewer AZ 2010, Cha 1→3.
  - Tomblin WV 2012, Cha 1→2. This is kind C: he won the 2011 special, and Cha codes Brown OR 2018 and Herbert UT 2012 as 2. This was D2's reading. The orchestrator confirmed it at 14:21: "keep the definition of record" means the record's own coding (Cha's 2 for a special-election winner), which is narrower than "not elected to the seat".
- **Kept (14):** Cha 2/3. **Inferred (6), codes kept:** FL98, NH88, WI78, WI02, ID78, MA98.
- **Near-tie scheme (13:43).** A switch from the scheme of record (`chambers.NEAR_TIE_OF_RECORD`, House = level) must pass the 08:36 robustness test against it, with each year left out (`_switch_test`).
  - Band fails: the 49-51% count is further away (85.8 vs 87.5 against 105 seen), and the 0.10-0.20 safe-band cells are worse.
  - So level stays. Band is shown beside: `model.near_tie.beside` and each House p's `near_tie_not_of_record`.
  - Only House 2010/2012 p move against main, by ×1.002-1.004, through the pooled factor.
- **Rosters that answered:** AL archives, AR SoS, azgovernor.gov, CA State Library, CT State Library, MN LRL, NV State Library, SC Legislative Manual, TX LRL, VT Legislature. They are cached in ~/.cache/vote-intake/rosters/.
- **Rosters that did not answer:** dos.fl.gov, sos.mo.gov and www.nh.gov gave 403. docs.legis.wisconsin.gov reset the connection twice. sos.idaho.gov gave 404. No MA roster was found. Do not use other hosts of a refusing agency (e.g. floridamemory.com).
- **Rebuild order:** build_congress.py $(seq 1977 2025), then chambers.py odd, then compute $(seq 1977 2025), then history, then backtest. This takes about 12-20 min. Afterwards, revert Senate and House files that come out equal.

**Why:** a later thread should not re-hit the refused hosts or redo the survey, and the two rules of 13:43 bind every later change.
**How to apply:** add states to `ROSTERS` and `CHECKS` in governor_incumbency.py; `check` fails if the survey and CHECKS differ. A new near-tie scheme for a level must pass `_switch_test` against its scheme of record. See [[d2-odd-governors]], [[d2-congress-data]] and [[m2-check-computed-p]].
