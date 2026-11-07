---
name: d4-cost-and-law
description: D4's cost inputs (data/cost) and every state's tie/recount law (data/law): PRs, counts, tools, the refusals and the rulings that shaped them
metadata:
  type: project
  modified: 2026-11-07T09:07:13.597Z
---

D4 (thread "Gather voting costs and tie laws"), 2026-11-07. Cost PR #40, law PR #41 and SPAE PR #43 merged; law follow-up PR #50 open (https://github.com/zwolk46/vote/pull/50).

- Law totals after #50: 34 states read, 12 partly read, 5 unread (IL, NH, NM, PA, WI); 266 tie rules, 211 recount rules. Report `data/law/REPORT.md`; figures come from `python3 -I pipeline/intake/state_law.py tables`.
- Tools in `pipeline/intake/`: `state_law.py` (fetch/check/build/chain/tables/tree), `render_page.cjs` (one address in headless Chromium), `render_tree.cjs` (Folio NXT contents tree: expand/more/open, 5 s apart). Cache dir is `$VOTE_CACHE`.
- Refusals recorded, not worked round: IL (403 even after the TLS chain was completed with verification on), PA 403, WI reset, NM 403 (not rendered: that would get round it), TN code site 403, Justia 403. NH gave an empty reply and could be retried once.
- SPAE 2020 wait times are high because of the survey's answers, not the coding (same question and codes in all six years; MIT's report agrees). Default cost C = 14 min x $38.00/h = $8.87 (14 is the Chen median, not a SPAE figure).
- NJ: the orchestrator allowed (2026-11-07 08:41 UTC) opening the viewer's own contents tree as a reader does; no sign-in, no form, no address taken from a script, one action every few seconds.

**Why:** the maker's rule is that a source that blocks us is lost and getting round its refusal is not ours to do; rendering or clicking a public page that answers 200 is reading it.
**How to apply:** for any further state law work, start from `data/law/src/<ST>.json` and `state_law.py check ST`; read the orchestrator's rulings before using a browser on a site that has said no. Related: [[d3-local-data]], [[research-source-access]].
