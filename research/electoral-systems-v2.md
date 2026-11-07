# How "one vote changes the outcome" works across electoral systems: re-read at source (v2)

*Work in progress, 2026-11-07 UTC. Brief R4 (`briefs/R4-research-electoral-systems-at-source.md`), worker thread on Sonnet 5.5. The first pass, `research/electoral-systems.md`, is kept as it is. This file will carry, for every fact in the first pass, a mark (confirmed, corrected, unread), then a table of corrections, then what is still unread. The sections below are filled as the reading comes back.*

## 0. How this was read

- **curl reaches the sources now.** On 2026-11-07 00:10 UTC `curl -sSL` returned HTTP 200 for `sites.stat.columbia.edu` and `plato.stanford.edu`, and then for 31 of the 35 URLs the first pass used. The first pass was refused every one of these hosts at CONNECT; the network has been opened (R4 step 1 passed).
- **Pages that curl could not read:** `www.electionresults.govt.nz` (Cloudflare "Attention Required", HTTP 403), `core.ac.uk` (Cloudflare "Just a moment", HTTP 403, two papers), `link.springer.com` (a "Client Challenge" page, two papers), `mta-sts.hcourt.gov.au` (the first pass's URL now returns a 404 page), `legislationline.org` (the first pass's URL now serves an unrelated page). None of these was circumvented (`_COMMON.md` 6); where a legitimate other copy of the same text was read, the section says which copy and which version.

## Appendix A re-run (by the orchestrating worker; the readers do not run code)

All seven scripts of the first report's Appendix A were extracted unchanged from `research/electoral-systems.md`, with only the placeholder path replaced, and run on 2026-11-07 (Python 3, numpy 2.5.3, `python3 -I`; seeds as in the scripts).

| Script | First-pass result | Re-run | Stands? |
|---|---|---|---|
| `plur.py` | N = 1,000: Q = 0.01261; N = 10,000: 0.003989 (= 1/sqrt(2 pi N) to 5 digits); forecast (.51,.49), kappa 400: 0.006363 at N = 1,000, 0.000724 at N = 10,000 | 0.0126125; 0.00398932 against 1/sqrt(2 pi N) = 0.00398942; 0.00636319; 0.000723861 | yes, identical |
| `plur3.py` | the §1 table (e.g. (.4,.4,.2) known: 0.01410 and 0.004460; (.40,.38,.22) forecast: 0.00707, 0.00712, 3e-7 at N = 1,000) | 0.0140973 and 0.00446007; 0.00706638, 0.00711841, 2.94e-7 | yes, identical |
| `pr.py` | council-sized 0.0052, 0.0056, 0.0059, 0.0062, 0.0067; M = 5: 2.4e-5, 4.7e-5, 4.5e-6, 2.1e-5; M = 10: 5.8e-5, 6.2e-5, 4.4e-5, 9.1e-5, 9.8e-6; national 2.1e-5 to 2.7e-5 | 0.00515, 0.00558, 0.00588, 0.00624, 0.00665; 2.36e-5, 4.69e-5, 4.46e-6, 2.11e-5; 5.8e-5, 6.2e-5, 4.39e-5, 9.1e-5, 9.83e-6; 2.1e-5, 2.36e-5, 2.52e-5, 2.59e-5, 2.69e-5 | yes (Monte Carlo, 20,000 or 6,000 draws; differences in the last digit) |
| `pr_check.py` | analytic 0.00626 / 0.01035 / 0.00862; brute force 0.00623 / 0.0112 / 0.00893 | the same figures | yes; the second party differs by about 1.3 combined Monte Carlo standard errors |
| `ref.py`, `ref2.py` | §6 table and §9 table | identical to the digits printed in the first report | yes |
| `chamber.py` | §8 table, "mean of three random draws" | identical | yes, with the caveat in §8 below |

**Comparators the first pass extrapolated and did not compute [measured now].** Two-candidate Q for forecast (.51,.49), kappa 400: N = 4,000: 0.0017670 (first pass 0.00177); N = 50,000: 1.4669e-4 (1.47e-4); N = 100,000: 7.347e-5 (7.3e-5); N = 1,000,000: 7.3581e-6; N = 5,000,000: 1.4718e-6 (first pass 1.47e-6, from scaling N x Q = 7.36). N x Q converges to f(1/2)/2 = 7.3593, where f is the Beta(204, 196) density of the vote share at 1/2, as the formula Q = f(1/2)/(2N) predicts. The scaling the first pass used for the 2016-referendum remark (§6 reading (d)) therefore holds to four digits at N = 5 million.

*(Sections 1 to 9 follow when the readers' results are in.)*
