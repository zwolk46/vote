---
name: sld-population
description: State legislative district populations (2024, 2022) for B* per person: Census CD119/CD118 source, script, matching rules, gaps (PR #71, 2026-11-07)
metadata:
  type: project
  modified: 2026-11-07T12:00:58.242Z
---

D2 built data/population/state-legislative-2024.json and -2022.json (PR #71, 2026-11-07), keyed by D3's contest ids, on the orchestrator's ask of 11:39 UTC (X1's "to each person" row needs it).

- Source: Census Bureau 2020 Census 119th (2024 SLDs) and 118th (2022 SLDs) Congressional District Summary Files on www2.census.gov, per-state zips (~2.5 GB each product); only the geo header's POP100 at summary levels 610/620 is read. api.census.gov needs a key, so it is not used. Some geo headers are Latin-1, not UTF-8.
- Scripts: pipeline/intake/census_sld_population.py (cache ~/.cache/vote-intake/census/), then pipeline/population_sld.py.
- Matching: names as words+numbers; multi-member seats get the district figure; seats that may be lettered subdistricts (MN 2022, MD, SD/ND 26A-style), NH floterials (39), and D3 records without a district (all RI 2024, some NY/AZ) get none. Never apportion.
- 2024: 5,143/5,310 (96.9%); 2022: 5,645/5,869 (96.2%).
- Bureau lines changed 2022 to 2024: GA, MT, NC, ND, OH, WA, WI, NY Assembly, MI House, bits of MN and SC House. No state known to differ from the Bureau's 2024 lines.

**Why:** a later thread adding populations for other years or levels should reuse these sources and rules.
**How to apply:** extend the same two scripts; D3's 2022 MN House names lack A/B, a D3 fix would let them match. [[d3-local-data]] [[d2-congress-data]]
