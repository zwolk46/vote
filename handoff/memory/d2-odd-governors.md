---
name: d2-odd-governors
description: D2's odd-year governors (KY, LA, MS, NJ, VA, 1977-2025; PRs #74, #76): sources, gates, refusals (KY/MS 2023), which get p, the plain route and its test, the lean note, open gaps
metadata:
  type: project
  modified: 2026-11-07T14:19:27.702Z
---

D2 built `data/governor/<odd year>.json` for 1977-2023 in PR #74 (merged 5a22ade), and 2025 plus RI 2010 in PR #76 (merged 2026-11-07 13:06 UTC). The write-up is in data/congress/REPORT.md §8 and §9.

- **Contests.** The record is Cha 2007-2021 and Algara-Amlani 1977-2005. Algara-Amlani also stands for NJ 2017, LA 2007 and RI 2010 (#76), where Cha lacks the race.
  - LA 2023 comes from the SoS through D3's gate (la_sos_governor.py).
  - NJ and VA 2025 come from the states' certified results via pipeline/intake/state_governors.py:
    - NJ: the Official List, read with D3's nj_sos, plus 21 county copies;
    - VA: enr.elections.virginia.gov, the API /results/public/api/elections/Virginia/2025-November-General/data plus /data/ballot-item/<id>, and the report CSV at /cdn/results/<jurisdiction id>/<blob>.
- **Refused at 12:39 UTC; nothing else tried.**
  - KY 2023: elect.ky.gov answered 403 "The request is blocked."
  - MS 2023: the sos.ms.gov results frame answered 403, a Cloudflare challenge.
  - The orchestrator's vendor rule (12:40): a vendor host counts only if a state page that answers names it and the vendor marks the count official or certified.
- **p.** Given for KY, NJ and VA from 1985 (31 races). Not computed for:
  - LA, because of its two rounds;
  - MS 1979-2019 (two majorities, HC 47 of 2020); MS 2023+ with 3 or more names is a first round;
  - AZ 1991 and the WV 2011 special;
  - 1977-1983 (too few cycles);
  - RI 2010, where the others' total is at least the second nominee's.
- **Route.** Fitted on the even years before each odd year; plain z=(1,0,0).
  - The midterm term fails the robustness test (40 races, 1985-2025: 5 of 7 cells further).
  - The lean note stands: 6 vs 3.2 within 1 point, and 9 vs 6.2 within 50,000 votes (after PR #78's fixes; plain log score 1.0971).
  - 2025 incumbency is inferred (chambers.state_gov_incumbency): neither nominee is the Cha 2021 winner.
- **Rebuild:** run la_sos_governor.py 2023, ms_governor_rule.py and state_governors.py, then build_congress.py $(seq 1977 2 2025) 2010, then chambers.py odd, then chambers.py compute.
- **Open.**
  - Cha's codes for KY 2019 and NJ 2021 are fixed in PR #78, with 15 more under the 13:43 successor rule (see [[d2-governor-incumbency]]).
  - AZ's 1990 cycle is filed under 1991.
  - LA's dates before 2023 are missing.

**Why:** a later thread adding odd-year races should reuse these rules, not retest them, and should not re-hit the refused hosts.
**How to apply:** extend state_governors.py READERS or build_odd_governors, and keep odd years out of fit_rows. See [[d2-congress-data]], [[d3-local-data]] and [[d4-cost-and-law]].
