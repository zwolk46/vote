# Decisiveness models and published estimates, re-read at source (v2)

*Brief R1, written 2026-11-07 by a Sonnet 5.5 worker thread (xhigh), from the brief `briefs/R1-research-decisiveness-models-at-source.md`. It re-reads at source every fact of `research/decisiveness-models.md` (the first report, kept unchanged) and fills what that report left unread. Marks on facts: [measured] (I ran or computed it; how is shown), [stated] (a source says it: where, with the exact words), [inferred]. Verdict on each fact of the first report: **confirmed**, **corrected** or **unread**. I choose nothing for the model or the site; where sources disagree or print something that does not agree with itself, both are given with their sources (`_COMMON.md` 3).*

## 0. Summary

Read on 2026-11-07. Most hosts the first report found refused are now reachable (section 1), so the formulas and published numbers it could not read are read here, from the papers' own pages.

1. **The model, as the sources print it.** A vote is decisive if (stage one) the state's vote is tied without it and (stage two) the state's electoral votes decide the Electoral College: Pr(decisive) = Pr(state necessary) × Pr(state tied | that event) (Gelman, Silver and Edlin 2012, abstract; Gelman, King and Boscardin 1998, eq. 1 to 3; section 3.1). The within-state factor is p_v(0.5)/n, the forecast density of the state's Democratic two-party share at one half, divided by the other voters (GKB eq. 2; Gelman, Katz and Bafumi 2004, eq. 2 and Appendix). Ties at the electoral-vote level get half credit.
2. **The old "random voting" index and the empirical record.** Banzhaf and Penrose give sqrt(2/π)/sqrt(n) (the constant is **sqrt(2/π) = 0.798, not 2/sqrt(π)**, GKBafumi p. 662). The same authors find that the spread of the vote share shrinks far more slowly than 1/sqrt(n): the best-fit exponent is −0.16 for presidential state results 1960 to 2000 (p. 666) and the curves "perhaps" decline as n^−0.1 across their data sets, which "implies that the probability of a decisive vote is proportional to n^−0.9, which is far closer to 1/n ... than to 1/sqrt(n)" (p. 669). The directive's "exponentially when the share is known" holds only for a known share other than one half (Mulligan and Hunter).
3. **Published estimates, all as printed** (section 3.3): about 1 in 10 million for all states in 1992 and less than 1 in 100 million for all states in landslide years such as 1972 (GKB 1998); in 2008, "on average ... 1 in 60 million", 1 in 10 million in the closest states, 1 in a billion in New York, California and Texas (GSE 2012); for 2020 the Economist page holds 51 values (Pennsylvania 1.14e-7, California 6.4e-11); for the House and state legislatures, one pivotal ballot in 89,000 to 100,000 and in 15,000 (Mulligan and Hunter, the first number differs between the working and the published abstract). 538's "Voter Power Index" is a relative measure whose definition and baseline I could not read.
4. **The first report's facts:** S1 to S5 all re-read; its two appendices (56 and 156 rows) have 0 differences from their sources. Twenty corrections are tabulated in section 4; the ones that matter most: the Economist's `se` is `(high − mean)/1.68`, not a standard deviation; BuzzFeed's power ratio is a per-demographic registered-voter ratio; the FEC **has** published 2024; MEDSL's county file is CC0 but gated behind a guestbook; the 2/sqrt(π) constant in `research/electoral-systems.md` was an extraction error.
5. **Where sources print something that does not agree with itself** (section 5): the worked example at GKBafumi p. 663 ("1.84/n") does not follow from its own inputs (they give 3.316/n); GKT's eq. (2) and (5) use a density that is half the exact tie probability, and its binomial expression omits a factor 2^−(n−1); the papers differ on whether the comparison is voting versus abstaining or one candidate versus the other (a factor of 2); GSE's "density at 0 of the margin" and "scale" may differ from the exact tie probability by small factors. For the mathematics check.
6. **Data inputs** (section 3.5): MEDSL state returns 1976 to 2024 (free CSV, CC0); MEDSL county 2000 to 2024 (CC0, gated); Algara and Amlani county returns 1868 to 2020 (CC0; Alaska absent; shares only in the state file); FEC official results back to 1982 (free, **no reuse terms printed**); National Archives electoral-vote tables 1789 to 2024 (CC0 notice for its own works); Census CPS voting supplement (free, no terms printed). MEDSL and the FEC differ in `totalvotes` for 14 to 21 states in each of 2016, 2020, 2024.
7. **Still unread** (section 6): 538's definitions and every Wayback copy (`web.archive.org` resets the connection); the 1975 to 1981 papers (Cloudflare or paywall); Gelman's 2016 blog post (Cloudflare); how the Economist computes `p_decisive_vote`; the MEDSL county rows; Dave Leip's Atlas (Cloudflare). What would open each is in section 6.

## 1. Access: the first report's section 1, re-checked [measured]

The first report said the egress proxy refused (403 at CONNECT) 43 scholarly, news, archive and data hosts on 2026-11-06, and only `raw.githubusercontent.com` answered. **That is no longer true.** On 2026-11-07, between about 00:10 and 00:40 UTC, plain `curl -sSL` (curl's default User-Agent, no other headers, no email address anywhere, at least 4 seconds between requests to one host, one host at a time per reader) got:

| Host | Result |
|---|---|
| `sites.stat.columbia.edu` | 200; the index page and all PDFs asked for (10 requests) |
| `plato.stanford.edu` | 200 (the brief's first test; no content used) |
| `raw.githubusercontent.com`; `github.com` | 200 for 16 files; `git clone --depth 1 https://github.com/TheEconomist/us-potus-model` worked (the first report found github.com refused: "GitHub access to this repository is not enabled for this session") |
| `projects.economist.com` | 200 for three pages (3 requests). `www.economist.com` was not requested (the first report was refused there) |
| `www.nber.org` | 200 for `w8590.pdf` |
| `www.politifact.com`, `www.jezebel.com` (a 2016 Fusion article), `www.natesilver.net` | 200 |
| `projects.fivethirtyeight.com`, `fivethirtyeight.com` | **every URL answers 301/302 to `abcnews.com`** (the site redirects; the proxy does not refuse): no 538 page, feed or data file can be read at the origin |
| `web.archive.org` | **refused**: CONNECT accepted, then the connection is reset after the TLS hello (`curl: (35) Recv failure: Connection reset by peer`; the proxy logs `ws_closed_mid_exchange ... tunnel closed (code 1006) after 10s`), three requests in a row; not retried. One `WebFetch` call on a Wayback URL after those failures returned `SITE_BLOCKED`; I count it as the "WebFetch when curl is refused" fallback (`CLAUDE.md`) and report it here so the orchestrator can judge |
| `andrewgelman.com` (Gelman's blog) | HTTP 403, a "Just a moment..." Cloudflare challenge; not circumvented |
| `www.sciencedirect.com`, `onlinelibrary.wiley.com`, `core.ac.uk`, `scilit.com`, the Villanova digital-commons PDF endpoint | HTTP 403 (Cloudflare challenge or error page); not circumvented |
| `link.springer.com`, the AER | paywall or login, no free text |

The data-source hosts (`dataverse.harvard.edu`, `www.fec.gov`, `www.archives.gov`, `www.census.gov`, `uselectionatlas.org`) are in section 3.5.

**Two things to know about method.** (1) My first request carried a browser-like `User-Agent` header, copied from the first report's method (`Mozilla/5.0 (X11; Linux x86_64) research-fetch`). The environment's safety monitor denied it as "Bot Check Circumvention". I repeated the request with curl's default header, which worked, and every later request by me and by the readers used the default. The first report's method line is therefore not to be copied. (2) One reader's first request to a 538 URL used `-L` and so followed the redirect and downloaded one ABC News page from `abcnews.go.com` and `abcnews.com`, outside its host list; it was never read and was deleted.

## 2. What the first report read (S1 to S5), re-read

Re-read from the GitHub files and cloned repository by a reader (notes `/tmp/r1/notes/B-github-economist.md`, not in the repository); I re-ran the checks that decide something (the `se` formula, the 24 zero rows, the 51 Economist page values) on its saved files.

### S1. FiveThirtyEight "Voter Power Index", 2016 snapshot, as scraped by BuzzFeed News

Source: `https://raw.githubusercontent.com/BuzzFeedNews/2016-11-voter-power-by-demographic/master/` (README.md, notebooks/scrape-voter-power-index.ipynb, data/fivethirtyeight/voter-power-index.csv, notebooks/demographic-analysis.ipynb; all read whole; branch master).
- README sentence: **corrected (where it ends).** [stated, README line 11] `This analysis uses FiveThirtyEight's "Voter Power Index" estimates for the 2016 election. BuzzFeed News downloaded the data on November 5, 2016; you can find it in the data/fivethirtyeight directory.` The first report ended the quote at "2016." where the source has a semicolon and goes on. The link on "Voter Power Index" is `https://projects.fivethirtyeight.com/2016-election-forecast/#tipping-point`.
- CSS class `tippingpointroi`, second table: **confirmed.** [stated, scrape notebook line 81] `table = dom.cssselect("table.tippingpointroi")[1]`, from `URL = "http://projects.fivethirtyeight.com/2016-election-forecast/"`.
- "<0.1" set to 0: **confirmed.** [stated, notebook lines 98 to 99] `# Set any value less than 0.1 to 0`, then `if power == "<0.1": power = 0`. [inferred] The code sends the page text "<0.1" to 0 and any other text to `float(text)`, so a 0.0 in the CSV means the page showed "<0.1" (or "0"); the page itself is unread.
- CSV: **confirmed, no differences.** [measured, script] 56 data rows; 24 rows have power 0.0; a cell-by-cell diff (abbreviation, power, state name, order) of the CSV against Appendix A of the first report gives 0 differences. The smallest nonzero values are HI 0.1, WA 0.2, UT 0.2. The CSV has a fourth column (`state`, upper case, empty for the five Maine and Nebraska district rows) that Appendix A omitted; Appendix A below is the first report's, unchanged.
- "power ratio" quote: **confirmed** [stated, demographic notebook line 785]: `# The "power ratio" is the total power for a demographic divided by the number of registered voters`. **The first report's description of the method is corrected.** [stated, notebook cells 13, 15, 17] BuzzFeed joins the index to Census 2012 registered-voter counts by state and demographic (`Table4b_2012.csv`, the Census report "Voting and Registration in the Election of November 2012"), computes `demo_power = total_registered * power` for each state row, sums it over states within each demographic, divides by that demographic's own registered voters (`power_ratio`), and then divides by the "Total" row's ratio (`power_ratio_norm`). It does not divide by the whole electorate's "total voters". That BuzzFeed treats the index as a per-voter weight is [inferred] from this arithmetic.
- What the index is: **still unread at 538.** Neither the README nor any notebook defines the index (searched for tipping, probab, decisive, pivot, defin): the only words are "Voter Power Index" in quotation marks, the anchor `#tipping-point` and the class name. **New, second-hand:** a 2016-09-20 article by Fusion (Daniel McLaughlin and Kate Stohr), "How we calculated how much your vote counts...", now at `https://www.jezebel.com/how-we-calculated-how-much-your-vote-counts-1793862047`, says: "As part of their election model, Fivethirtyeight.com calculates a Voter Power Index, which they define as 'the relative likelihood that an individual voter in a state will determine the Electoral College winner.' The index is based on polling data and fluctuates as the race heats up. The actual probabilities that a single vote will decide the election are vanishingly small." [stated by a third party quoting 538; I could not read 538's page (section 1) to confirm the wording, or to learn what the index is relative to: the baseline, the unit, whether 1.0 is the national average.] The first report's caution therefore stands in part: the index is a **relative** measure, "relative to" something not yet read; it is not a probability.
- Value of S1 to the site, as the first report said: a published, forecaster-computed relative measure for the 2016 presidential race, a comparison for any model of ours; **not usable as a number until its baseline is read.**

### S2. The Economist's open presidential model (`TheEconomist/us-potus-model`)

Source: `README.md` and a shallow clone (157 files, branch `master` only, HEAD `b89e602ec03e81c797c66cf2743af6fdae4aa526`, committed 2020-10-15 12:41 -0400, "removing unsued parameters from stan model.").
- Date line and licence: **confirmed.** [stated, README lines 3 and 346 to 358] "Last update on Thursday October 15, 2020 at 12:29 PM EDT"; "This software is published by The Economist under the MIT licence. The data generated by The Economist are available under the Creative Commons Attribution 4.0 International License." followed by "The licences include only the data and the software authored by The Economist, and do not cover any Economist content or third-party data or content made available using the software." The `LICENCE` file reads "MIT License ... Copyright (c) 2020 The Economist Newspaper, Andrew Gelman and Merlin Heidemanns (Columbia University)".
- Tables: **confirmed, no differences.** [measured, script] the three tables headed "Predictions for each state" (2008, 2012, 2016; columns `state | mean | low | high | prob | se`; 52 rows each; the national row is labelled with U+2013 "–") give 156 rows by 5 values and 0 differences against Appendix B of the first report. The performance tables are labelled "economist (backtest)" [stated, README lines 75, 169, 260].
- Layout: **corrected.** The README names `final_model_2008.R`, `final_model_2012.R`, `final_model_2016.R` [stated, README lines 29 to 31], but the files are `scripts/model/final_2008.R`, `final_2012.R`, `final_2016.R` [measured: the first report's path returns 404, `.../master/scripts/model/final_2016.R` returns 200 and is identical to the clone's file]. There is no branch `main`. Also: `scripts/model/poll_model_2020.stan` (141 lines). The fitted-model files the README tables are built from are **not in the repository** (`models/` holds only `.gitkeep`; the README.Rmd loads `models/backtest_2008/stan_model_%s_normal_final.rds`, line 63), so which Stan file produced the 2008, 2012 and 2016 tables is not stated.
- Wording: "survey mode and population" in the first report is "survey mode and survey population" in the README (lines 8 to 15), minor.
- **What the columns mean: corrected, where the first report inferred.** The README does not define them; `README.Rmd` produces them. [stated, README.Rmd lines 550 to 564 for 2008, 1068 to 1082 for 2012, 1589 to 1603 for 2016; the posterior draws `pct_obama` come from the Stan output `predicted_score`, built at lines 208 to 248, 719 to 759, 1243 to 1283]:
  - `mean`: the average over posterior draws, on the last day (`filter(t == max(t))`), of the Democratic candidate's two-party vote share in that state (Obama in 2008 and 2012, Clinton in 2016; third parties excluded). The run date is `min(election day, Sys.Date())`, so these tables are back-tests with polls up to election day [stated, lines 55, 571, 1089].
  - `low`, `high`: the 2.5% and 97.5% quantiles of the same draws (README.Rmd lines 214 to 215), a central 95% interval.
  - `prob`: `mean(x > 0.5)` over the draws (line 217): the model's probability that the Democrat carries the state.
  - `se`: **not a standard deviation computed from the draws.** The code is `mutate(se = (high - mean)/1.68)` (README.Rmd lines 555, 1073, 1594; [measured by me] the same expression occurs 9 times in the file, and a 1.96 variant, `(high - mean)/1.96`, occurs three times, in the plots of the "ex_states" rows at lines 257, 768 and 1292). [measured, script, by the reader] all 156 table rows fit (high − mean)/1.68 within rounding (0.0011), and 50, 51 and 52 of the 52 rows (2008, 2012, 2016) do not fit (high − mean)/1.96. No comment explains 1.68. [measured by the reader] for a normal curve with that 95% interval the standard deviation would be (high − mean)/1.96, so `se` is about 1.17 times that. **The first report's reading, "se the forecast standard deviation of the share", is therefore wrong in its definition and only roughly right in size.**
  - Row `–` (`'--'` in the code): the vote-weighted average over states of each draw's state shares (README.Rmd line 237), so its `prob` is the probability of winning the national two-party popular vote, not the Electoral College (lines 244 to 247). Rows are sorted by |mean − 0.5|, values rounded to 3 decimals (line 562).
- "Tipping", "pivot", "voter power", "decisive": **confirmed: the repository holds no decisiveness output.** [measured, grep over every text file] "pivot" 0, "voter power" 0, "decisive" 0, "Banzhaf" 0, "voting power" 0, "one vote" 0; "tipping" 10 lines, all in `final_2008.R` (lines 813 to 843) and `final_2012.R` (lines 809 to 839), which print to the console the share of draws in which each state is the 270th-electoral-vote state; none in `final_2016.R`, the README or the Stan files.
- **New: the Economist's 2020 forecast pages.** `https://projects.economist.com/us-2020-forecast/president/how-this-works` (read; the README links to it) describes the 2020 model and defines no voter-power or tipping measure; it says "The resulting probabilities of victory are simply the fraction of these simulations that a given candidate wins" and "The ultimate result is a list of 20,000 hypothetical paths that the election could take." The main page `https://projects.economist.com/us-2020-forecast/president`, section "Key states", says [stated, page text and its embedded JSON `pageProps.text.tipping_point.description`]: "We use two metrics to measure states' importance. One is the 'tipping-point probability': the chance that a state will cast the decisive 270th electoral vote for the victor. The other is the chance that any single voter in a state will cast the decisive ballot that wins the tipping-point state for the next president." Its embedded data (timestamp 1604404963 = 2020-11-03T12:02:43Z [measured]) holds 51 values (50 states and DC) of `p_decisive_vote`, with a label and `p_tipping_point`; they are tabulated in section 3.3. **Not stated anywhere I read:** how `p_decisive_vote` is computed (formula, electorate size, tie definition) (the repository has no code for it); and the Economist's terms for the page numbers (they carry "Copyright © The Economist Newspaper Limited 2026. All rights reserved."; the repository's CC BY grant is for "the data generated by The Economist" and excludes "any Economist content", so the page numbers are not shown to be CC BY).

### S3. "What's my vote worth?" (smrfeld)

**Confirmed.** [stated, `https://raw.githubusercontent.com/smrfeld/whats-my-vote-worth/master/README.md`, 4,783 bytes, read whole] "With the 2020 census populations, California has the lowest fraction: 0.84, while Wyoming has the highest fraction: 3.2." and "every vote cast in California is worth c.a. 0.3 the vote of a voter in Wyoming, or equivalently every voter in Wyoming has the power of 3.8 Californians in deciding the U.S. presidential race." [measured: 3.2/0.84 = 3.81]. MIT licence, "Copyright 2020 Oliver K. Ernst". The formula for the "vote fraction" is in an image (`static/vote_frac.png`), which the reader looked at: f_state = (electoral votes of state / electoral votes total) × (total U.S. population / state population). [inferred, as the first report said] This is electoral votes per person, not the probability of decisiveness; it ignores closeness.

### S4. MIT Election Data and Science Lab repository note

**Confirmed.** [stated] `https://raw.githubusercontent.com/MEDSL/2020-elections-official/master/README.md` (226 bytes): heading "# This repository is deprecated"; then "We are no longer maintaing 2020 precinct data in this repository. Our official 2020 precinct data are now available on the Dataverse here: https://dataverse.harvard.edu/dataverse/2020_precincts" ("maintaing" is the source's spelling; the first report joined heading and sentence into one quote, the words are exact).

### S5. Third-party compilation of election-data sources and licences (`pmheideman/us-county-election-results`)

**Every statement confirmed against the three files** (README.md, LICENSE-DATA.md, docs/DECISIONS.md, branch `main`, read whole), still a third party's account: version "v1.0.0" released 2026-09-26; scope "U.S. House 1990-2024, President 1992-2024, U.S. Senate 1990-2024; regular general elections; 48 contiguous states"; data CC BY 4.0, code MIT; "Verified CC0 1.0 on Dataverse: MEDSL (House and Senate precinct files 2016-2024, county President 2000-2024) and Algara & Amlani" (DECISIONS.md section 9, "License check (2026-09-23)"); Algara & Amlani "Harvard Dataverse doi:10.7910/DVN/DGUMFI", "Historical President 1868-2020, Senate 1908-2020", "CC0 1.0 as deposited. It is compiled from CQ Press / ICPSR historical returns, so the upstream provenance should be cited"; `countypres_2000-2024.tab`; "We do not use CQ Press or Leip's Atlas data directly."; "State sites: none grants CC0/CC BY." with Colorado, Florida, Indiana and Wisconsin restrictive and North Carolina and Utah "Conditional (non-commercial/unmodified)"; the defect list "MEDSL 2016 totals inflated in AL, SC, AR and IN" (section 8b item 3); "8 states of the 2024 President (367 county-years) had been silently dropped (blank MEDSL vote mode)" (line 211; a defect in their build, fixed there); "the FEC has not published 2024" (line 225: "FEC 'Federal Elections' workbooks for 2004-2020"; line 227 "the FEC has no 2024 book").
- One statement needs a clarification, not a correction: MEDSL's 2004 county rows were "incomplete in nearly every county (Maine 7.3% and Mississippi 3.2% below the certified totals)"; in their release those two state-years are not MEDSL rows but come from Wikipedia-derived county tables tied to the FEC statewide totals (line 229).
- Left out of the first report [stated by the third party]: "Maine 2024 totals doubled; New Jersey Bergen County 2024 total; Indiana 2018-2022 coverage; Indiana and Alabama pre-2016 gaps" are still flagged in their corrections log; "Terms pages unreadable (HTTP 403): GA, MD, NH, AZ."; "Open question for the release license: vote counts are factual public records, but the restrictive/conditional/unreachable states may warrant a written permission request or a reliance-on-facts note before publishing under CC BY 4.0."; their own reconciliation of the presidential rows, 2000 to 2024, 336 state-years: "658 nominee checks, 600 within 0.05%, 648 within 0.5%; state totals within 0.5% in 316 of 336".
- The primary check of these claims, at MEDSL, the FEC and Dataverse: section 3.5.

### Other reads of the first report

- `https://raw.githubusercontent.com/fivethirtyeight/data/master/README.md` (761 bytes) and the 19 GitHub repository searches: **not re-read** (no bearing on the model); the first report's statement of them stands unverified.

## 3. The five parts of the directive

### 3.1 Theoretical models and formulas

The first report read none of them. Every formula below is copied from the printed page. Where text extraction garbles an equation I read the page image (marked "page image"). Papers fetched with `curl -sSL` from `https://sites.stat.columbia.edu/gelman/research/published/` on 2026-11-07: `probdecisive2.pdf` (6 pp), `decisive2.pdf` (8 pp), `STS027.pdf` (10 pp), `gelmankatzbafumi.pdf` (18 pp), all read whole. [measured: HTTP 200, sizes 495,420 / 2,110,416 / 357,081 / 274,015 bytes; `pdftotext`, and `pdftoppm` page images for equations.]

**Locators from the first report: confirmed.** The titles, venues and years the first report gave "from memory" are right, as printed on the papers and in the reference lists of GSE, GKB and GKBafumi: Gelman, Silver and Edlin, "What is the probability your vote will make a difference?", *Economic Inquiry* 50(2), April 2012, 321 to 326, doi 10.1111/j.1465-7295.2010.00272.x, online early 19 March 2010; Gelman, King and Boscardin, "Estimating the Probability of Events That Have Never Occurred: When Is Your Vote Decisive?", *JASA* 93(441), March 1998, 1 to 9; Gelman, Katz and Tuerlinckx, "The Mathematics and Statistics of Voting Power", *Statistical Science* 17(4), 2002, 420 to 435; Gelman, Katz and Bafumi, "Standard Voting Power Indexes Do Not Work: An Empirical Analysis", *British Journal of Political Science* 34(4), 2004, 657 to 674, doi 10.1017/S0007123404000237; Mulligan and Hunter, "The Empirical Frequency of a Pivotal Vote", *Public Choice* 116, 2003, 31 to 54 (GSE's reference list); Edlin, Gelman and Kaplan, *Rationality and Society* 19, 2007, 293 to 314 (GSE's reference list); Good and Mayer, *Behavioral Science* 20, 1975, 25 to 33; Beck, *Public Choice* 23, 1975, 75 to 79; Chamberlain and Rothschild (printed "Rothchild" in GSE and GKB), *Journal of Economic Theory* 25, 1981, 152 to 162; Banzhaf (1965), *Rutgers Law Review* 19, 317 to 343; Penrose (1946), *JRSS* 109, 53 to 57. One discrepancy among the sources themselves: Banzhaf (1968), "One Man, 3,312 Votes", *Villanova Law Review*, pages 304 to 332, is volume 13 in GKB (1998) and GKT (2002) and volume 16 in a footnote of GKBafumi (2004). [stated, reference lists]

#### A. Gelman, King and Boscardin (1998), the base formulas

[stated, JASA 93, p. 3, section 3.1, page image] Definition: "Your presidential vote will be decisive if two conditions are satisfied. First, without your vote, your state's election outcome must be exactly tied or one vote away from a tie. (We consider the case of a person who will either vote for one candidate or not vote. A voter who is considering switching from the Democratic to Republican candidate will, of course, have a higher probability of being decisive.) Second, your state must be decisive in the national election; given that it is tied, neither party must have an electoral vote majority."

Notation as printed: e_i electoral votes of state i; e_total = sum of e_i = 538; n_i = "number of voters in state i (excluding yourself)"; v_i = "Democratic share of the two-party vote in state i (excluding your vote)"; V_i = 1 if v_i > .5 and 0 otherwise; E_-i = (sum over j not equal i of e_j V_j) + 3 = "Democratic electoral vote in the 49 states excluding i, plus the District of Columbia" (DC's 3 electoral votes are assumed certain for the Democrats).

- Eq. (1): Pr(your vote matters) = Pr(your vote is decisive in your state) × Pr(your state will be decisive | your vote is decisive in your state).
- Eq. (2): "if n_i is even, ... Pr(n_i v_i = .5 n_i) = Pr(v_i = .5) ≈ f_vi(.5)/n_i" and "if n_i is odd ... Pr(n_i v_i = .5(n_i − 1)) = Pr(v_i = .5 − .5/n_i) ≈ f_vi(.5)/n_i also, assuming that n_i is reasonably large", where f_vi is the density of the continuous variable v_i under the forecast model.
- Eq. (3): Pr(your state is decisive | your vote is decisive in your state) = Pr(E_-i in (.5 e_total − e_i, .5 e_total) | v_i = .5) + (1/2) Pr(E_-i = .5 e_total − e_i | v_i = .5) + (1/2) Pr(E_-i = .5 e_total | v_i = .5). "The factors of 1/2 arise because a vote that causes the national election to be tied is only half as decisive as a vote that changes the election outcome."
- Eq. (4), the forecast model: v_it = (Xβ)_it + δ_t + γ_{r,it} + ε_it, with a national error δ_t, independent regional errors γ, independent state errors ε; var(ε_it) = n_it^(−θ) σ², "θ is a parameter that varies between 0 (as in the forecasting models) and 1 (as in the theoretical models)"; fitted "95% interval for θ of [.09, .36]", with "estimated standard deviations of about 2.5%, 2.5%, 5.0%, and 3.5%, for the national, regional (outside the South), regional (the South), and state-level error terms" (p. 5).
- Eq. (5): the within-state probability ≈ (1/n_i) N(.5 | (Xβ)_i + γ_ri + δ, n_i^(−θ) σ²), "where N(x|μ, τ²) is the normal density function"; averaged over 1,250 posterior simulations of the parameters (p. 5). The second factor (3) is found by adding "the observation" v_it = .5 to the data, refitting, simulating the other 49 states, and fitting a beta distribution to (E_-i − 3)/(e_total − 3 − e_i) on the first two moments (p. 4 and p. 5, and Figure 1: beta fit versus simulation frequency).
- Stated scaling (p. 7, section 6.2): "The probability of a tie in a state is on the order of 1/n_i, and the probability that a state will be decisive given that a tie occurs is (crudely) proportional to e_i, which is roughly proportional to n_i. Therefore, we expect the product of these two factors to be approximately constant, with a slight advantage to the smallest states."
- Binomial versus forecast variance (p. 7): "in practice, the turnout in U.S. elections is so large that the binomial variability is negligible compared to the forecast uncertainty in the model. For example, in 1992, turnout in all states was greater than 160,000, and sqrt((.5)(.5)/160,000) = .00125, as compared to statewide error terms of about .03." [measured: sqrt(.25/160000) = 0.00125]

**Two scope statements in the paper.** (1) p. 2: "We ignore minor exceptions such as Maine's rule that allows their electoral college delegates to be split, delegates deciding to vote for candidates other than for whom they were chosen, and complications caused by third-party candidates who get large fractions of the vote." (2) p. 6, section 6.1: "In general, the probability of influencing the election outcome by mobilizing N supporters to vote in a single state is roughly N times the probability that a single vote in that state will be decisive ... the probability of swinging the election by changing the preferences of N voters in a single state is roughly 2N times the probability that a single vote in that state will be decisive."

#### B. Gelman, Silver and Edlin (2012), the forecast-simulation method

[stated, Economic Inquiry 50(2), p. 321] "Broadly speaking, there are three ways of estimating the probability of a decisive vote. The first approach, and the oldest in the literature, is to set up a theoretical model for the joint distribution of the popular vote margin in the separate jurisdictions ... The second approach is purely empirical, an estimate of the form y/n, where n is the number of elections in some large historical sample and y is the number that were tied. Elections are very rarely tied, so one can instead use an estimate such as y/(2,000 n), where y is now the number of elections decided by less than 1,000 votes. ... The third method, which we use here, is to set up a forecasting model for the current election." The paper names Good and Mayer (1975) and Chamberlain and Rothchild (1981) as examples of the first approach, and Mulligan and Hunter (2003) and Gelman, Katz and Bafumi (2004) of the second (p. 321 and footnote 2).

Definition (abstract and p. 321): "In a presidential election, the probability that your vote is decisive is equal to the probability that your state is necessary for an electoral college win, times the probability the vote in your state is tied in that event."

Method (p. 322, section II): forecast of 24 October 2008 from polls (Silver 2008), "a 10,000 × 51 matrix representing 10,000 computer simulations of the election, with each simulation including the vote margin for Obama" (51 = 50 states and DC). The margin is converted to votes "by multiplying by the voter turnout in the state (which we estimate by taking the two-party turnout from 2004 and adding 4% corresponding to population increase and another 4% to account for an anticipated increase in turnout this year)". Then, for each state:
1. "Let E be the number of electoral votes in your state. We estimate the probability that these are necessary for an electoral college win by computing the proportion of the 10,000 simulations for which the electoral vote margin based on all the other states is less than E, plus 1/2 the proportion of simulations for which the margin based on all other states equals E. (This last part assumes implicitly that we have no idea who would win in the event of an electoral vote tie.)"
2. "We estimate the probability that your vote is decisive, if your state's electoral votes are necessary, by working with the subset of the 10,000 simulations for which the electoral vote margin based on all the other states is less than or equal to E. We compute the mean M and standard deviation S of the vote margin among that subset of simulations and then compute the probability of an exact tie as the density at 0 of the Student-t distribution with 4 degrees of freedom (df), mean M, and scale S." Footnote 8: the t with 4 df is "a robust alternative to the normal ... to allow for the possibility of unanticipated shocks. Using the t instead of the normal has little effect on the probability of a decisive vote in close states, but it moderates the results in states farther from the national median, for example, changing the estimated probability of decisiveness in the District of Columbia from 5e-85 to 2e-12, in Utah from 9e-16 to 2e-10, but changing the estimate in Ohio only from 3.4e-8 to 3.1e-8." Footnote 7: Nebraska's and Maine's split electoral votes "retrospectively turned out to be a mistake in 2008, when Obama won an electoral vote from one of Nebraska's districts."
3. "The product of two probabilities above gives the probability of a decisive vote in the state."

The paper's own checks on its inputs (p. 322, footnote 5): after the election the state forecasts "found a very close match, with a difference of less than 1 percentage point in 22 states and a difference of less than 3 percentage points in 39 of the 50 states (Gelman and Sides 2009)".

Footnote 4: betting-market prices as the source of the distribution are rejected: "www.intrade.com assigned McCain a ridiculously high 3% chance of winning the District of Columbia".

Footnote 3 on recounts: "An objection sometimes arises ... that one vote never makes a difference, because if the election were decided by one vote, there would be a recount anyway. Gelman, Katz, and Bafumi (2004, p. 674) discuss why this argument is wrong ... This can be shown by setting up a more elaborate model that allows for a gray area in vote counting and then demonstrating that the simpler model of decisive votes is a reasonable approximation." (See D below for that model.)

#### C. Gelman, Katz and Bafumi (2004) and Gelman, Katz and Tuerlinckx (2002), the voting-power literature and its critique

**Definition of voting power.** GKBafumi p. 660: "the voting power of jurisdiction j is the probability that party A wins if jurisdiction j goes for party A, minus the probability that party A wins if jurisdiction j goes for party B. Next, the power of a given voter in jurisdiction j is the probability that party A wins if that voter supports A, minus the probability that A wins if that voter supports B." Ties "at all levels are broken by coin tosses". GKT p. 422, eq. (1): power_i = Pr(R = +1 if v_i = +1) − Pr(R = +1 if v_i = −1); "We assume that ties at all levels are decided by coin flips." GKT p. 424: under random voting "power_i = 2 Pr(voter i is satisfied) − 1".

**Banzhaf (and Penrose) index.** GKBafumi p. 660: "Perhaps the simplest measure of decisiveness is the (absolute) Banzhaf index, which is the probability that an individual vote is decisive under the assumption that all voters are deciding their votes independently and at random, with probabilities 0.5 for each of two parties" (footnote 14 credits Banzhaf 1965 and Penrose 1946). "The random voting model": "a voter is assumed to be equally likely to choose any of the alternatives on the ballot" (p. 659); equivalently all 2^n vote configurations equally likely (GKT p. 423).

**Two-stage formula.** GKBafumi p. 661 (page image): individual voting power = Pr(jurisdiction j's e_j electoral votes are decisive) × Pr(a given vote is decisive in jurisdiction j | jurisdiction j's e_j electoral votes are decisive), with
- eq. (1): Pr(j's e_j electoral votes are decisive) = Pr(E_-j in (0.5E − e_j, 0.5E)) + (1/2) Pr(E_-j = 0.5E − e_j) + (1/2) Pr(E_-j = 0.5E), E = sum of e_j, E_-j the votes for party A outside j;
- eq. (2): Pr(a given vote is decisive in jurisdiction j) = p_vj(0.5)/n_j, "where p_vj is the continuous probability density assigned to the vote for party A in jurisdiction j. (We are assuming that n_j in any district is large enough, greater than 100, say, so that the model for the v_j's can be approximated by a continuous distribution. A derivation of this approximation, under general conditions, appears in the Appendix.)"
Same structure in GKT section 3.2 and footnote 11 of GKBafumi ("The voting power of an individual citizen has the same two-stage mathematical structure ... whether the aggregation is by representatives as in the Council of Ministers or (nearly) automatic as in the Electoral College").

**The square-root formula, exactly as printed.** GKBafumi p. 662 (page image), section 2.2.2: "Under random voting, the distribution p_vj of the vote share among the n_j voters in jurisdiction j is approximately normally distributed with mean 0.5 and standard deviation 0.5/sqrt(n_j), hence the approximation, Pr (a given vote is decisive in jurisdiction j) = p_vj(0.5)/n_j = sqrt(2/π) · 1/sqrt(n_j). What matters for comparing voters is not the constant factor sqrt(2/π) but the proportionality with 1/sqrt(n_j)." **The tie constant is sqrt(2/π) = 0.7979, not 2/sqrt(π).** [measured: with density 1/(sqrt(2π) · 0.5/sqrt(n)) at the mean, divided by n, = sqrt(2/π)/sqrt(n); numerically sqrt(2/π) = 0.79788 and 2/sqrt(π) = 1.12838.] This settles `research/electoral-systems.md` section 10.3 item 1, whose WebFetch extract read "(2/sqrt(pi)) * (1/sqrt(n_j))": that was an extraction error (see the table of corrections). [measured, exact enumeration] the same constant for the exact count: for 1,001 voters, Pr(the other 1,000 split 500 to 500) = C(1000,500)/2^1000 = 0.025225, sqrt(2/(π · 1001)) = 0.025219.

GKT p. 423 (page image), section 3.2: the exact random-voting probability, "Pr(V_-i = 0) + 1/2 Pr(|V_-i| = 1)", is printed as the binomial coefficient C(n_j − 1, (n_j − 1)/2) for n_j odd and C(n_j − 1, n_j/2) for n_j even, "under the random voting model. Unless n is very small, this can be approximated as sqrt(2/(π n_j)), which is a special case of (2)." [measured] As printed the two binomial coefficients omit the factor 2^−(n_j − 1) that turns a count into a probability (with it, n_j = 1001 gives 0.025225, matching sqrt(2/(π n_j)) = 0.025219). GKT eq. (4): "power_i ≈ w_j / sqrt(n_j)", the origin of Penrose's square-root rule (weights proportional to the square root of the jurisdiction's voters, GKT p. 423 to 424, attributed to Penrose 1946) and of the claim that the Electoral College favours large states (Banzhaf 1968, GKT p. 426). GKBafumi 2.2.3: "voting power approximately proportional to e_j/sqrt(n_j) ... Under the natural weighting system in which the electoral votes e_j are set proportional to n_j, an individual's voting power is then proportional to sqrt(n_j)".

**The first factor under random voting.** GKBafumi p. 662 and GKT p. 423: with many jurisdictions and none dominant, Pr(j's electoral votes are decisive) is approximately proportional to e_j; GKT eq. (3) power_i = Pr(|V_-i| < w_i) + (1/2) Pr(|V_-i| = w_i) with the linear approximation power_i ≈ sqrt(2/π)(w_i/W), W² = sum of squares of weights, "relative error of less than 10% for all states" (the same sentence, "less than 10 per cent for all states", GKBafumi p. 662; the Electoral College's e_j "range from 3 to 54, with a total of 538").

**The critique, and what replaces it.** GKBafumi abstract: "Voting power indexes such as that of Banzhaf are derived, explicitly or implicitly, from the assumption that all votes are equally likely (i.e., random voting). That assumption implies that the probability of a vote being decisive in a jurisdiction with n voters is proportional to 1/sqrt(n). ... They find that the probability of a decisive vote is approximately proportional to 1/n. The random voting model (and, more generally, the square-root rule) overestimates the probability of close elections in larger jurisdictions."
- Test (sections 3.1 and 4): fit |v_j − 0.5| = c n_j^β. For presidential state results 1960 to 2000 the best-fitting β is −0.16 (GKBafumi p. 666; "with a standard error of 0.03", GKT p. 427), "much closer to 0 than to −0.5". For lower houses and senates of US states 1984 to 90, the US House 1896 to 1992, the US Senate 1988 to 96, and European national elections 1950 to 98 the lowess lines are "much closer to horizontal than to 1/sqrt(n_j), and the best-fit parameters β are all closer to 0 than to −0.5" (p. 669; the exponents themselves are in Figure 3, not printed in text). Then (p. 669): "the lowess and best-fit power-law curves ... are essentially flat. Or it could be said that they decline slightly with n, perhaps proportional to n_j^−0.1. This implies that the probability of a decisive vote is proportional to n_j^−0.9, which is far closer to 1/n as in the election forecasting literature than to 1/sqrt(n) as in the voting power literature."
- Control (p. 670 to 671): permuting the 435 congressional districts at random into "states" removes state, regional and national swings; the best-fit exponent is then −0.494, "essentially equal to a theoretical value of −0.5".
- Why (section 5.1, p. 669 to 670): "elections are affected by local, state, regional and national swings"; "The result of this multilevel or fractal variation is that the standard deviation v_j will be expected to decline as a function of n_j, but at a slower rate than 1/sqrt(n_j)"; "the 1/sqrt(n) rule in general holding only for independent or weakly-correlated random variables".
- The Good and Mayer / Chamberlain and Rothschild rule (GKBafumi p. 663, section 2.3, page image): "Good and Mayer and also Chamberlain and Rothchild derive a 1/n_j rule, that is, a model where the probability of decisiveness is inversely proportional to the number of voters. This model arises by assuming that votes are binomially distributed, but with binomial probabilities p that themselves vary over the n_j voters in a jurisdiction. Then, for large or even moderate values of n_j, the distribution p_vj of the vote proportion v_j is essentially fixed (not depending on n_j), so that p_vj(0.5) is a constant, and the probability of a vote being decisive is proportional to 1/n_j (from (2))." GKT p. 428 to 429 says the same in section 5: independent votes with probability p other than 1/2 "is not a useful model; although it corrects the mean vote, it still predicts a standard deviation that is extremely small for large elections (Beck, 1975)"; if the voters' probabilities p_i "are given any fixed distribution not depending on n, then the distribution of the average vote, for large n, will converge to the distribution of the p_i's. The empirically falsified 1/sqrt(n) rule then goes away ... because the binomial variation ... is minor compared to any realistic variation among the probabilities p_i. (This was noted by Good and Mayer, 1975; Margolis, 1977, 1983; and Chamberlain and Rothschild, 1981.)"
- Replacement models in GKT (sections 5.1 and 5.2, read at the level of their stated results): votes as an Ising model on a tree give sd(V̄) proportional to n^−α with α below 1/2, fitted at α = 0.16 for the presidential data (best-fitting flip probabilities π = 0.05, 0.08, 0.15, 0.26 for k = 2, 3, 10, 100 branches; the fitted coefficient c is 1.74); a latent random-walk model gives a variance of the form a − b log n. GKT p. 433 says plainly that "Further work is needed to develop models of individual voters in a way consistent with available data". The authors' empirical-model alternative for the Electoral College is a forecast-based simulation (GKT section 4.4 and Figure 2b: normal errors with standard deviations 0.06 national, 0.02 regional, 0.04 state, 0.09 congressional district on the vote proportions, 500 simulations of the 2000 election; the plotted values are in the figure only).

**Recounts and courts: the printed model (GKBafumi Appendix, p. 674).** "Consider a two-party election and label v as the proportion of the n votes received by party A. We model vote-count errors, disputes, etc., by defining π(v) (the paper's symbol for this probability, not the constant 3.14159) as the probability that party A wins, given a true proportion v. With perfect voting, π(v) = 0 if v < 0.5, 1 if v > 0.5, or 0.5 if v = 0.5. ... the probability that your vote determines the outcome of the election, conditional on v (defined now as the proportion in favour of candidate A, excluding your potential vote), is π(v + 1/n) − π(v)." Eq. (3): Pr(decisive vote) = E[π(v + 1/n) − π(v)] = sum over v of [π(v + 1/n) − π(v)] p(v). Two approximations: the election is contested "only for a small range of vote proportions, which will lie near 0.5" (π(v) = 0 for v < 0.5 − ε and 1 for v > 0.5 + ε), and "the probability density p(v) for the election outcome has an uncertainty that is greater than ε (for example, perhaps ε = 0.005 and v can be anticipated to an accuracy of 2 per cent, or 0.02)", so p(v) is treated as the constant p(0.5) on 0.5 ± ε. The integral then telescopes to p(0.5)[1/n · 1 − 1/n · 0] = p(0.5)/n, "which is the same probability of decisiveness as calculated assuming all votes are recorded correctly." GKT p. 422 to 423 repeats it: with disputed votes and recounts, "the probability of affecting the outcome of the election can still be identified with the probability of a tie to a very close approximation". The model assumes a smooth, fixed disputed zone; it does not itself say what π is for any real election.

#### D. The directive's premises, checked

1. **"p is approximately the density of the vote-share forecast at 50% divided by the number of voters": confirmed**, with the exact notation above: GKB eq. (2), GKBafumi eq. (2) and Appendix, GKT eq. (2) and (5). Qualifications printed in the sources: n_j is large (GKBafumi: "greater than 100, say"); GKB's n_i excludes the voter, GKBafumi's n_j is the number of voters in the jurisdiction; the density is of the vote share v (GKB, GKBafumi) but GKT's printed (2) and (5) use the density of the "difference in vote proportions" (see the open points, section 5).
2. **"p shrinks like 1/N when the vote share is uncertain but exponentially when it is known": the 1/N half is confirmed in the sources above** (GKBafumi p. 663 and p. 664: "in contrast, it is usual in forecasting elections to model the vote proportion v_j directly, with no dependence on n_j, in which case p_vj(0.5) does not depend on n_j and so the probability of decisiveness is proportional to 1/n_j"). **The "exponentially when known" half is not stated in these four papers.** What they print is the normal formula in GKB p. 6, section 5 (attributed to Margolis 1977): "Suppose that n people vote in the election, and that the forecast is a normal distribution with mean μ and standard deviation τ; then the probability that a single vote will be decisive is approximately (sqrt(2π) τ n)^−1 exp(−(μ − .5)²/(2τ²))", page image. [inferred] If the share is known exactly, with each voter independently choosing A with probability p other than 1/2, the standard deviation of the share is sqrt(p(1 − p)/n), which shrinks with n, so the exponent −(μ − .5)²/(2τ²) = −n(p − .5)²/(2p(1 − p)) grows in n and the probability falls exponentially; I derive that from the printed formula and do not find it printed. See section 3.1 E for the early papers.

#### E. Beck (1975), Good and Mayer (1975), Chamberlain and Rothschild (1981), Mulligan and Hunter (2003) and the rest

**Only Mulligan and Hunter could be read, and only as the free working paper.** Everything else in this list is **unread**: each publisher or archive refused a plain `curl` (Cloudflare challenge or error page, a paywall or a login), and I did not get round any of them (`_COMMON.md` 6). A reader ran 39 fetches, one host at a time (notes `/tmp/r1/notes/C-early-papers.md`, not in the repository).

| Paper | Status | Why |
|---|---|---|
| Chamberlain and Rothschild 1981, *J. Econ. Theory* 25, 152 to 162 | **unread** | ScienceDirect HTTP 403 (Cloudflare error page); the CORE copies a search returned were behind a Cloudflare challenge (403); no free abstract reached |
| Beck 1975, *Public Choice* 23, 75 to 79 | **unread** | Springer paywall, no free abstract |
| Good and Mayer 1975, *Behavioral Science* 20, 25 to 33 | **unread** | Wiley Cloudflare challenge (403); only mentions of it found |
| Margolis 1977, *Public Choice* 31 | **unread** | Springer paywall. GKB (1998) and GKBafumi (2004) print pages 134 to 137; a reader reports 135 to 138 from Springer's listing (not checked by me) |
| Banzhaf 1965 (*Rutgers L. Rev.* 19); Banzhaf 1968 (*Villanova L. Rev.* 13) | **unread** | Banzhaf 1968 has a free copy at `https://digitalcommons.law.villanova.edu/vlr/vol13/iss2/3` (landing page answers; its PDF endpoint returned a Cloudflare challenge to `curl`); 1965 not found free |
| Penrose 1946, *JRSS* 109, 53 to 57 | **unread** | no free text found |
| Stromberg 2008, *AER* 98(3), 769 to 807 | **unread** (abstract read) | AER behind a login; a 2001 conference draft marked "Preliminary and incomplete. Please do not quote." covers the probability that a state is pivotal and close, with no single-voter formula |
| Riker and Ordeshook 1968; Ferejohn and Fiorina 1974; Myerson 2000 "Large Poisson Games" | **unread** | free extracts or abstracts only, no formulas; Kellogg's working-paper server returned 500 |
| Mulligan and Hunter 2003, *Public Choice* 116, 31 to 54 | **read as NBER Working Paper 8590 (November 2001)**, `http://www.nber.org/papers/w8590.pdf`; the 2003 text is paywalled | the working paper and the published version differ (see below) |

**What was not established from a primary source:** the sentence quoted in GKBafumi that "Good and Mayer and also Chamberlain and Rothchild derive a 1/n_j rule" (read in GKBafumi, section C above, but not in the two papers themselves); and which alternative the voter faces (abstaining, or voting for the other side) in Beck, Good and Mayer, Chamberlain and Rothschild and Margolis. Secondary descriptions a reader met, all marked third-party: Usher (Queen's University working paper 1238, p. 8) says Chamberlain and Rothschild let the vote share p "itself be drawn from a distribution" and that "if the distribution of p is uniform (and in some other cases as well), the probability of a tie is proportional to 1/N"; Xia (arXiv 2011.03791) says Beck's model is "two groups of agents, whose votes are i.i.d. within each group"; Zyczkowski and Slomczynski (arXiv 1104.5213, pp. 5 to 6) write the Penrose result as the probability of a tie among 2j other equal-probability voters, C(2j, j)/4^j ≈ sqrt(2/(πN)), and Banzhaf's index for weights w_k as (2w_k − w)/2^(M−1) [stated by third parties; I did not re-derive them].

**Mulligan and Hunter (NBER WP 8590)**, read by a reader and re-checked by me on the printed text (`pdftotext`); page numbers are the paper's own "Pivotal – N".
- Definitions (p. 5): "we refer to a 'pivot election' as one in which the winner's official and final vote total exceeded the loser's official and final vote total by no more than one vote. A 'pivotal vote' is a vote cast for the winner in a pivot election, or cast for either candidate in a tied election. In other words, a 'pivotal vote' is one for which it appears an election outcome would have been different if it had been cast differently." The voter's alternative is the other candidate, not abstention.
- The binomial model (p. 18 to 19, section III.A): z_j = 1 for a Democratic vote, v voters, success probability A. Eq. (1), known A, v even: Pr(Σ z_j = v/2) = C(v, v/2) A^(v/2) (1 − A)^(v/2). Eq. (2), a prior F on A: Pr(Σ z_j = v/2) = ∫ C(v, v/2) A^(v/2) (1 − A)^(v/2) dF(A). "Interestingly, not much has to be known about F to compute the unconditional probability of a pivotal vote, because (2)'s integrand can be neglected everywhere except in the neighborhood of A = ½. So (2) simplifies to (3)": Pr(Σ z_j = v/2) ≈ f(1/2)/(v + 1), "where f is the density function corresponding to F". Eq. (4): the probability of a pivot election, tie or one-vote margin, "heuristically" 1.5 times (3), because with v odd (3) gives "half of the probability that the election margin is exactly one"; "The probability of a pivotal vote is just (3) because only half of the votes in a pivot election with odd total votes are pivotal." Footnote 13: with v even a pivot election is "approximately twice (3)"; if even and odd v are equally likely, "approximately the average of (3) and twice (3)". [measured by a reader, exact computation] (3) matches the exact integral to four decimals for A uniform on [0.25, 0.75] at v from 100 to 100,000.
- f(1/2): "The estimates reported in Figure 5 suggest that f(½) ≈ 2. For example, Figure 5 shows the frequency of a pivot election, for elections of size v = 20,000, to be 1/6000, so f(½) = (1/6000)(2/3)(20001) ≈ 2. The model seems sensible in this regard, since f(½) = 2 if, say, A were uniformly distributed on [0.25, 0.75]." (p. 20) [measured: (1/6000)(2/3)(20001) = 2.22.]
- Known A is exponentially small unless A = 1/2 (footnote 14, p. 20): "setting v = 100,000 and A = .61 (roughly the averages for the US sample), (1) yields an estimated probability of a pivot election of 10^−1108 (here I follow Margolis 1977 and others in the literature using the normal density to compute (1)). Compare 10^−1108 to my US sample frequency of 0.00005." [measured by a reader and by me] The normal-density value is 10^−1107.0 (the paper's printed exponent is 1 off) and the exact binomial value is 10^−1079.9; both are astronomically small either way. [measured by a reader] For A = 0.49 and v = 100,000 the exact tie probability is about 5.2e−12.
- Empirical (p. 6 to 7, 14 to 16, 24 to 26): 16,577 contested US House elections 1898 to 1992 (ICPSR 6311) and 40,036 state legislative elections 1968 to 89 (ICPSR 8907). Abstract: "one of every 100,000 votes cast in U.S. elections, and one of every 15,000 votes cast in state elections, 'mattered' in the sense that they were cast for a candidate that officially tied or won by one vote. Very close elections are more rare than the independent binomial model predicts. The evidence also suggests that recounts, and other margin-specific election procedures, are quite relevant determinants of the frequency of a pivotal vote." Of the US returns, only one in 16,577 was decided by a single vote (New York's 36th district, 1910, officially 20,685 to 20,684). In the state data, "two were tied and seven were decided by a single vote (9/40036=0.0002)". **The published version's abstract (Public Choice 116, free abstract at EconPapers) says "One of every 89,000 votes ... in U.S. Congressional elections", not 100,000; a number from the working paper must not be shown as the published one.**
- Scaling (p. 15 and 26): in 50 equal-sized groups of state elections the pivot frequency against election size is "apparently linear with slope equal to −1" on log-log axes, "so the probability of pivotal vote appears to vary with 1/v rather than e^−v"; the conclusion (p. 26) says the frequency of a pivotal ballot "is closely approximated by 2/v, which is broadly consistent with a binomial model". But the paper also says (p. 14) that three size groups "do not appear to be 1/v" exactly (q(4) in units of 10^−4: 4.5, 2.7, 0.2 for average sizes 5,570, 14,236 and 51,169 votes) and (p. 16) that for US House elections below about 30,000 to 40,000 votes the frequency rises with size.
- Recounts (p. 24 to 26): of the ten general elections coded as decided by 0 or 1 vote, in five the later or recounted totals differ from the official ones and determined the winner; "using the 'latest' column" the frequency falls by about half, to "one tie and four one-vote victories (a frequency q(1) = (5+1)/56613 = 0.0001)"; p. 26: "Some preliminary investigation of recounts suggest that the frequency of a pivotal ballot would only be 1/v, rather than 2/v, according to this definition."

**The directive's premise, "p shrinks like 1/N when the vote share is uncertain but exponentially when it is known":**
- *Uncertain share:* confirmed in a primary source: Mulligan and Hunter eq. (3), f(1/2)/(v + 1), for a fixed prior f, and GKBafumi (section C).
- *Known share, not 1/2:* exponentially small in v is confirmed by Mulligan and Hunter eq. (1) and footnote 14 (a binomial coefficient times [A(1 − A)]^(v/2)). A secondary source writes it T = sqrt(2/(πN)) [4p(1 − p)]^(N/2) (Usher, eq. (3); [measured by a reader] this equals the exact binomial to four figures for N = 100,000 and p = 0.49).
- *Known share exactly 1/2:* **not exponential**: the tie probability is C(v, v/2)/2^v ≈ sqrt(2/(πv)), falling as 1/sqrt(v) (the Penrose and Banzhaf square-root case in GKT and GKBafumi). **So the premise as the directive states it is incomplete: it holds for a known share different from 1/2, and the rate depends on how far from 1/2 the share is.**

### 3.2 Two-stage structure of the Electoral College

The first report had only the directive's statement of it; the sources now give it in four printed forms (formulas in section 3.1 A to C).

- **The structure.** Your vote decides the national outcome only if (stage one) your state's vote is exactly tied, or one vote from a tie, without your vote, and (stage two) your state's electoral votes are the ones that decide the Electoral College: GSE abstract, "the probability that your vote is decisive is equal to the probability that your state is necessary for an electoral college win, times the probability the vote in your state is tied in that event"; GKB eq. (1); GKBafumi eq. (1) and (2) and footnote 11; GKT section 3.2. The order of the factors is as GKB writes it: Pr(tied in state) × Pr(state decisive | tied in state).
- **Stage one:** p_v(0.5)/n (GKB eq. (2); GKBafumi eq. (2)), with n the other voters of the state and p_v the forecast density of the Democratic share of the two-party vote.
- **Stage two:** GKB eq. (3): the probability that the electoral votes of the other states, E_-i, fall in the interval (0.5 e_total − e_i, 0.5 e_total) given the state is tied, plus 1/2 the probability they equal either end. GKBafumi eq. (1) is the same with E in place of e_total. Under random voting this is approximately proportional to e_j (error under 10% for all states, GKBafumi p. 662, GKT p. 423); under a forecast it must be computed from a joint forecast of all states, because "separate forecasts for all the states are not enough; it must be a joint forecast" (GKB p. 3), so that, for example, "the probability that Utah ... will be decisive in the unlikely event that it is tied" can be found.
- **Two ways the sources compute stage two (given as printed, no choice made).** GKB: refit the forecast model with the state's share fixed at 0.5, simulate the other 49 states (1,250 posterior draws), and fit a beta distribution to the other states' electoral votes (pp. 4 to 5). GSE: use 10,000 joint simulations of all 51 contests; stage two is the share of simulations in which the other states' electoral-vote margin is less than E, plus half the share in which it equals E; stage one is the t4 density at 0 of the margin among the simulations with others' margin at most E (p. 322). [inferred] These differ in how the "state is tied" condition is imposed.
- **What the sources leave out, in their own words.** Maine's and Nebraska's split electoral votes, faithless electors and third-party winners (GKB p. 2: "We ignore minor exceptions such as Maine's rule ..."; GSE footnote 7: ignoring the splits "retrospectively turned out to be a mistake in 2008"). DC: GKB assumes its 3 electoral votes certain for the Democrats. A 269 to 269 electoral tie: both papers give half credit ("a vote that causes the national election to be tied is only half as decisive as a vote that changes the election outcome", GKB p. 3; GSE: "we have no idea who would win in the event of an electoral vote tie"). What the law then does in that tie (the contingent election in the House) is **not in any source I have read**; see section 3.5 for the National Archives page.
- **Beyond the Electoral College.** The same two-stage structure is stated to hold for any weighted aggregation, such as the Council of the European Union (GKBafumi footnote 11), and for chamber control (the other briefs). The sources read here do not give a decisiveness figure for the House, the Senate or a parliament.
- **The Economist's page names the same two quantities** (section 2, S2): the "tipping-point probability" of a state and "the chance that any single voter in a state will cast the decisive ballot that wins the tipping-point state"; the formula behind its `p_decisive_vote` is unread.

### 3.3 Published numerical estimates of p for real elections

Each row says what was estimated, for which election, how, and where it is printed. All are per voter, and the first four are probabilities that a single vote decides the presidency. Different papers use different tie and alternative conventions (section 5, open points 3 to 5), so rows are not strictly comparable.

| Election | Estimate | How computed | Source | Mark |
|---|---|---|---|---|
| Presidential 1952 to 1992 (1968 excluded), by state | "about 1 in 10 million for all states" in 1992 (Figure 2a); Vermont "1 in 3.5 million"; Utah and Nebraska lower; "as much as about 1 in 1.5 million for some small states in some close elections (e.g., Nevada in 1960 and Alaska in 1976)"; "less than 1 in 100 million for all states in landslide elections such as 1972"; 1964, 1972, 1984 "on the order of 1 in hundreds of millions" | prospective: hierarchical regression forecast from economic and political variables available before the election (poll standing two months out), 1,250 posterior draws; eqs. (1) to (5) of section 3.1 A | GKB 1998, pp. 5 to 7 and Figure 2 | [stated] |
| Presidential 1992, if the popular vote decided | exact tie "approximately 1 in 13.3 million" | popular vote forecast "roughly normal with mean 51.5% and standard deviation 5.6%", about 92 million voters | GKB 1998, p. 5 | [stated] |
| Presidential, generic (not a forecast) | .008 e_i/n_i; e.g. 10 electoral votes and 2 million turnout, "1 in 25 million" | 18% of state results between .48 and .52, 2 of 11 elections (1948 to 1988) within 50 electoral votes, times 1/2 | GKB 1998, p. 6 | [stated]; [measured] .008 × 10/2,000,000 = 4e-8 |
| Presidential 2008 (forecast of 24 Oct 2008), by state | New Mexico, Virginia, New Hampshire and Colorado "approximate 1 in 10 million"; "On average, a voter in America had a 1 in 60 million chance"; New York, California and Texas "closer to 1 in a billion"; Ohio 3.1e-8; Utah 2e-10; DC 2e-12 (t4; with the normal, DC 5e-85, Utah 9e-16, Ohio 3.4e-8); Nevada, Pennsylvania, Florida higher than most (Figures 1 to 3; plotted values are not printed) | poll-based simulation; section 3.1 B | GSE 2012, abstract and pp. 323 to 325, footnote 8 | [stated] |
| Presidential 2000, by state | plotted only (Figure 2b of GKT); numbers not printed | perturbing observed district results with normal errors, SDs 0.06, 0.02, 0.04, 0.09; 500 simulations | GKT 2002, section 4.4 | **unread** (figure) |
| Presidential 2016, by state | the "Voter Power Index", relative: NH 5.6, NV 4.9, NM 4.7, MI 3.1, CO 3.1, AK 3.1, PA 2.7, NC 2.7, FL 2.5, VA 2.3, IA 1.0, "<0.1" in 24 of 56 rows including CA, NY, TX | 538's forecast; definition second-hand only ("the relative likelihood that an individual voter in a state will determine the Electoral College winner"), baseline unread | BuzzFeed scrape (Appendix A); Fusion quoting 538 | [stated, third party]; not a probability |
| Presidential 2020 (Economist page of 2020-11-03 12:02 UTC), by state | `p_decisive_vote`: PA 1.1426e-7 ("1 in 9 million"), WI 6.82e-8 (1 in 15 million), NV 6.46e-8, NH 5.79e-8 (1 in 17 million), MI 4.85e-8 (1 in 21 million), MN 3.49e-8, AZ 3.45e-8, FL 2.69e-8 (1 in 37 million), NM 2.62e-8, GA 2.12e-8, NC 2.02e-8, VA 1.28e-8 (1 in 78 million); TX 9.64e-9 (1 in 104 million), OH 4.98e-9 (1 in 201 million), IA 4.34e-9, NY 1.65e-10 (1 in 6 billion), UT 8.97e-11, CA 6.38e-11 (1 in 16 billion), WY 6.44e-12, DC 4.14e-15 (1 in 242 trillion); with `p_tipping_point` (sums to 1.0 [measured]; PA 0.4089, WI 0.0946) | The Economist's forecast; method for `p_decisive_vote` **unread** | `https://projects.economist.com/us-2020-forecast/president`, embedded data | [stated]; terms unread |
| Congressional elections (U.S. House 1900 to 1992) | 6 of 20,597 decided by under 10 votes, 49 by under 100, 293 by under 500, 585 by under 1,000; "a frequency probability of about .5/20,597" per random election; upper bound 1 in 10,000 for n = 200,000 | counting; 2τ-bound with a 2% forecast SD | GKB 1998, p. 6 | [stated] |
| US House 1898 to 1992 and state legislatures 1968 to 89, retrospective | "one of every 100,000 votes cast in U.S. elections, and one of every 15,000 votes cast in state elections" were cast for a candidate who "officially tied or won by one vote" (working paper; the published abstract says 89,000, not 100,000); about 2/v per ballot | counts of official margins 0 and 1, 16,577 and 40,036 elections; recounts roughly halve the frequency | Mulligan and Hunter, NBER WP 8590, abstract and pp. 6, 7, 24 to 26 | [stated] |
| Presidential 2012, 2016, 2020, 2024; any year after 2008 by Gelman or Silver | a Gelman blog post of 2016-11-07 ("chance vote will decide election") was found by search | `andrewgelman.com` answers a Cloudflare challenge | | **unread** |
| 538 in other years, 538's 2008 FAQ figure, Katz, Gelman and King (2002), Stromberg (2008) | | 538 redirects to ABC; Wayback refused; the others paywalled or text unreadable (the Oxford chapter's text layer is garbled) | | **unread** |

### 3.4 Simple, explainable forms and the inputs they need

The sources give these simple forms. Which, if any, the site uses is not mine to choose; the facts the maker's model would need are the printed formulas, their stated conditions and the inputs.

1. **A state's tie probability from a forecast** (GKB eq. (2), GKBafumi eq. (2)): p_v(0.5)/n. Inputs: the forecast density of the state's Democratic two-party share at 0.5, and n. Condition: n "greater than 100, say"; a vote-share forecast that does not itself depend on n.
2. **With a normal forecast of the share, mean μ and standard deviation τ** (GKB p. 6, attributed to Margolis 1977): (sqrt(2π) τ n)^−1 exp(−(μ − .5)²/(2τ²)). Inputs: μ, τ and n. GKBafumi's worked example (p. 663): 10,000 voters, forecast 52% with standard error 3%: printed as "[1/sqrt(2π)(0.03)] exp(−0.5(0.05/0.03)²)/n_j = 1.84/n_j". **The printed arithmetic does not agree with its own inputs: see section 5, point 2.** GKB's bound (p. 6): with τ = 2% and μ = .5 the factor is "20/n" ([measured] 19.95/n); with n = 200,000 "an upper bound of 1 in 10,000".
3. **Random voting**: sqrt(2/π)/sqrt(n) (GKBafumi p. 662); Banzhaf and Penrose; the square-root rule. For comparison only; the papers say it is empirically falsified for real elections.
4. **Scaling rules**: p ∝ 1/n for a fixed forecast (GKBafumi p. 663 to 664), empirically n^−0.9 (GKBafumi p. 669); Mulligan and Hunter's per-ballot frequency 2/v (WP p. 26); the unweighted state-by-size result does not fit 1/v exactly (WP p. 14).
5. **Two-stage product**: GSE's "probability your state is necessary" times "probability the vote in your state is tied in that event", with the electoral-vote margin among the other states and the state's electoral votes as the inputs to the first factor. GSE's Figure 3 reads it by quantity: "a 18% chance that the electoral vote margin will be less than 55 (so that California's 55 electoral votes will be crucial), but only a 1 in 100 million chance that California's immense popular vote will be tied if that happens"; for New Hampshire "a less than 1% chance that the electoral college will be so close that New Hampshire's five electoral votes will be necessary—but, if they are, ... a relatively high 1 in 70,000 of a tie vote in the state."
6. **A rule of thumb for the first factor with e electoral votes** (GKB p. 6): about 1/2 (2/11)(e/50), from 2 of 11 elections within 50 electoral votes.
7. **Mulligan and Hunter's closed form for a prior on the vote share** (eq. (3)): f(1/2)/(v + 1), with f(1/2) about 2 if the share is uniform on [0.25, 0.75].
8. **Inputs named across the papers:** the number of voters (turnout: GSE uses the 2004 two-party turnout plus 4% population growth plus 4% turnout rise; GKB scales the previous election's turnout by the growth of the voting-age population, "errors in the turnout have simple and relatively minor effects"); the forecast mean and uncertainty of each state's two-party share and their joint (national, regional, state) error structure; the electoral votes of each state; and for a lay explanation the numerical examples above that reproduce by hand: GKB's 10 electoral votes with 2 million turnout, "1 in 25 million"; the printed `.008 e_i/n_i`; and the `20/n` bound.

### 3.5 Where the input data come from

Read on 2026-11-07 by a reader (notes `/tmp/r1/notes/D-data-sources.md`, not in the repository), with the points that decide something re-checked by me: the Dataverse records (licence field, version, file list) of the MEDSL county and state files, the FEC results page and its 2024 links, and the National Archives allocation page. All requests were plain `curl -sSL` with the default header, at least 4 seconds apart per host. No account was opened, no form filled, nothing bought, no message sent.

**Verdict on each statement of the first report's section 3.5**

| First report said | Verdict | What the source says |
|---|---|---|
| Forecast inputs: the Economist repository gives mean and standard deviation of the state vote share for 2008, 2012, 2016 under CC BY 4.0, "subject to the column definitions being confirmed" | **corrected** | The licence statement is confirmed (section 2, S2) and covers "the data generated by The Economist". The columns are now defined from the code: `mean`, `low`, `high`, `prob` as in section 2; **`se` is not a standard deviation of the draws but `(high − mean)/1.68`**. 538's archived forecasts: **unread** (538 redirects to ABC; Wayback refused) |
| MEDSL county presidential returns 2000 to 2024, `countypres_2000-2024.tab`, "said by a third party to be CC0" | **confirmed for the record, unread for the data** | [stated, Dataverse API field] doi:10.7910/DVN/VOQCHQ, v20.0 released 2026-02-25 (20 versions since 2018-10-11), licence `CC0 1.0`, every other terms field null, file `countypres_2000-2024.tab` (9,845,506 bytes; the original CSV is 10,222,208). **The file and its codebook are behind a guestbook** that requires name, email, institution and position (the API answers 400, "You may not download this file without the required Guestbook response for guestbookID 458"), which I did not fill in (it asks for an email address). The landing page itself answered HTTP 202 with an empty body and was not retried |
| MEDSL's 2020 repository is deprecated in favour of Dataverse | **confirmed** | S4 above |
| Dave Leip's Atlas: access and licence unread | **still unread** | `uselectionatlas.org` answers HTTP 403, `cf-mitigated: challenge`, "Just a moment..." on the first request; not retried, no WebFetch |
| State election offices: terms vary, some restrict reuse (third party) | **unread** | no state site was visited; the third party's list (S5) stands as a claim |
| FEC "Federal Elections" workbooks exist for 2004 to 2020 (third party) | **confirmed and extended** | see below; **the FEC has published 2024 official presidential results** |
| Algara and Amlani, President 1868 to 2020, Senate 1908 to 2020, CC0 (third party) | **confirmed, with two corrections** | see below |

**MEDSL on Harvard Dataverse (`dataverse.harvard.edu`; the JSON API answered every call, the HTML landing page did not).**
- Records for US President ([measured] from `/api/search`): county 2000 to 2024 (VOQCHQ, above); state ("constituency") 1976 to 2024, **doi:10.7910/DVN/42MVDX "U.S. President 1976–2024", v10.1 released 2026-09-04 (12 versions since 2017-11-01), CC0 1.0 [I re-read the licence field and file list]**; older 2000 to 2020 county and 1976 to 2020 state files (8RFBRF, VDDKN5, both v1.0 of 2022-01-24, one with a template description left unfilled: "election returns gathered for the office of xxx at the county/constituency/precinct level"); precinct files for 2016 (11.2), 2020 (5.0), 2024 (1.0; `PRESIDENT_precinct_general.csv` 399,528,254 bytes, not downloaded); and Edison/CNN election-night returns 2024 (1.5 GB county file, not downloaded). MEDSL's own site (`electionlab.mit.edu/data`) still labels the state file "U.S. President 1976–2020" (dated Jul 17, 2023); the Dataverse record is the newer statement. Nothing earlier than 1976 for President turned up in the search. Every version of VOQCHQ and 42MVDX has `versionNote: null` (no changelog or errata in the record).
- The county file's structure is known only from the public DDI [measured by the reader]: 94,151 rows, 12 variables (`state, county_name, year, state_po, county_fips, office, candidate, party, candidatevotes, totalvotes, version, mode`), years 2000 to 2024, `county_fips` with 52 invalid values and a maximum of 2938000 (so non-county codes exist), `version` 20260225 in every row. The rows and the `mode` values are unread.
- **The state file is free (CSV, 514,108 bytes) and was read whole** [measured by the reader; the row counts below re-run on the saved file]: 4,822 rows, 13 elections 1976 to 2024, 51 jurisdictions in every year, columns `year, state, state_po, state_fips, state_cen, state_ic, office, candidate, party_detailed, writein, candidatevotes, totalvotes, version, notes, party_simplified`; `notes` empty in all rows; `version` is `20210113` for 4,287 rows and `2025-11-20` for the 535 rows of 2024 (two date formats in one column). Its codebook (3,176 bytes) is stale [stated and measured]: titled "Codebook for U.S. President Returns 1976–2016" though the file is 1976 to 2024; names "Statistics of the Congressional Election", published by the Clerk of the House, as the source; documents a `mode` column the CSV does not have; does not document `notes`. It warns that for Massachusetts and New York the rows include "blank", "other/blank", "scattering/blank" entries ("consult state returns" for a count of votes cast for candidates), and that where candidates appear on several party lines "separate vote totals are indicated for each party", to be aggregated.
- `totalvotes` is not defined the same way in every state-year [measured by the reader]: in 2024 the file has UNDERVOTES rows in nine jurisdictions and OVERVOTES in five; in Maine the rows sum to `totalvotes` with 11,072 undervotes included, in DC `totalvotes` excludes them. Against the FEC's official workbook (below), `totalvotes` differs in 14 of 51 jurisdictions for 2024 (examples NY +118,934, PA −24,526, MA +39,262, ME +11,072), 21 for 2020 and 18 for 2016, while the Democratic and Republican candidate votes are identical in all 51 for 2024; for 2020 they differ in seven states (CA, IN, NC, ND, NH, NJ, NY, mostly by a few hundred votes; New York by −13,901 and −7,199 because MEDSL has one line per candidate and the FEC sums party lines) and for 2016 in five (AZ, CA, MD, MN, UT, by up to 259 votes; my reader's New York difference is an artefact of its own sum). National 2024 sum of `totalvotes`: 155,410,204 (MEDSL) against 155,238,302 (FEC). Which side is right is not decided here; both say they come from state offices.
- MEDSL's own list of where the president data came from, `sources-president.tab` (5,038 bytes, 51 rows; the same file is attached to the county and the state datasets, and its URLs are 2020 election pages, so it does not cover 2024): "Is certified?" is "official" 24, "yes" 19, "YES" 1, "official recount" 1, "unofficial" 1 (SD), "doesnt say" 1 (MD), "does not say" 1 (TN), blank 3 (MA, MN, WA); "missing votes?" is TRUE for 16 states (AR, CO, IL, KS, KY, LA, MI, MS, NJ, NM, OK, PA, SD, TN, TX, WV), with notes such as "missing scatter" and "says official but no statement of votes" (CT) [stated].
- **MEDSL's own statements of defects** [stated, `README.md` of the 2024 precinct dataset XDJYKC, 42,513 bytes, downloaded freely]: "**Note: These aggregation checks are representative of the data as it stands upon the initial release and may not be reflective as we improve the data over time.**"; for Vermont, "County-level presidential data for VT is incomplete (missing several counties); our data matches official VT Secretary of State results (~119K Trump, ~235K Harris)"; its table of the county dataset's 2024 presidential totals gives Indiana 1,808,892 (Trump) and 1,220,554 (Harris), against 1,720,347 and 1,163,603 in the FEC workbook and in MEDSL's own state file [measured], i.e. about 5% high; Maine, Rhode Island and Virginia differ by a few thousand (Maine's note: "Harris and King gaps are RCV redistribution artifacts"). [inferred] That table is "upon the initial release"; the current county file is unread, so I do not know whether it still holds. The same README warns of "fictitious zero-vote rows", of modes that double-count if a `TOTAL` mode is added to split modes, and that in some small jurisdictions of California, Kansas, Nevada and New Mexico "vote counts are not published due to privacy concerns" (`votes = "*"`), for the precinct file.
- **The third party's MEDSL defect claims (S5), one by one.** "Verified CC0 1.0 on Dataverse": confirmed for the county President record and for the state file (above). "House and Senate precinct files 2016-2024" CC0: **unread** (their licence fields were not fetched). File name `countypres_2000-2024.tab`: confirmed. "MEDSL 2016 totals inflated in AL, SC, AR and IN": **unread for the county file; not seen in the state file**: [measured] the state file's 2016 values equal the FEC's for AL, SC and IN (Democratic, Republican and total) and in AR the candidate votes are equal and the total is 41 lower. "8 states of the 2024 President (367 county-years) silently dropped (blank MEDSL vote mode)": **unread** (the `mode` values are in the gated file); the only gap MEDSL states itself is Vermont's. "2004 county rows incomplete (Maine 7.3%, Mississippi 3.2% below certified)": **unread for the county rows**; [measured] in MEDSL's state file Maine 2004 equals the FEC total (740,752) and Mississippi 2004 is 1.07% below the FEC (1,139,824 against 1,152,145; Bush 672,660 against 684,981).

**Algara and Amlani, doi:10.7910/DVN/DGUMFI** (the HTML landing page was not fetched; API read).
- [stated] Title (exact): "Replication Data for: Partisanship & Nationalization in American Elections: Evidence from Presidential, Senatorial, & Gubernatorial Elections in the U.S. Counties, 1872-2020" (Carlos Algara, Claremont Graduate University; Sharif Amlani, UC Davis); deposited 2021-08-30, published 2021-09-07, version 1.1 of 2022-09-04. **The phrase "Historical President 1868-2020" in the first report is the third party's label, not the title.** Licence field `CC0 1.0`; other terms null; no guestbook.
- Contents [stated, depositor's descriptions; sizes measured]: county-level presidential returns 1868 to 2020, Senate 1908 to 2020 and governor 1865 to 2020 as R binaries (about 1.5 to 1.9 MB each; **not opened**), a state-level presidential file `1868_2020_presvote.tab` (59,528 bytes), a 266,932-byte manual, county shapes (2.3 GB, not downloaded) and replication code. In the president county frame the vote variables are `democratic_raw_votes`, `republican_raw_votes`, `pres_raw_county_vote_totals_two_party` and `raw_county_vote_totals`: only the Democratic and Republican nominees' counts and the county total are held.
- [stated, manual dated August 30, 2021] "these datasets do not contain data on elections in Alaska given the lack of consistent county-level geographic units in the state"; 113,756 presidential county-election rows of which 88 have missing votes (56 are Texas counties in 1904 and 1908); no 1868 rows for Florida, Mississippi, Texas, Virginia; Colorado 1876 omitted; Democratic votes coded missing in CO, ID, KS, ND, WY for 1892.
- [measured by the reader] The state file `1868_2020_presvote.tab` has 2,028 rows (39 elections by 52 codes); `dvote, rvote, ovote` are **vote shares** with one decimal, not counts (so it cannot give turnout); `dev, rev, oev, totev` are electoral votes. Two defects: 2020 Nebraska has Democratic 1, Republican 5 and total 5 (the parts exceed the total), and 1968 North Carolina `totev` is 14 where the National Archives page lists 13. Its `totev` matches the National Archives table for every state in all 15 presidential years 1960 to 2020 compared, except NC 1968.
- **"Compiled from CQ Press / ICPSR historical returns" (S5): not confirmed.** The manual names Congressional Quarterly only for identifying gubernatorial elections, and the Newberry Library's Atlas of Historical County Boundaries for county dates; it does not say where the county vote counts came from, and refers to the *Electoral Studies* paper ("Forthcoming" in the manual), which is unread.

**FEC (`www.fec.gov`).**
- [stated] "As a public service, the FEC compiles election results from past federal elections, as officially reported by individual state or territory election offices." and "Election results are not available immediately from the FEC. Instead, state election offices are responsible for certifying results."
- **2024: corrected.** [stated and re-checked by me] The page links "Official 2024 Presidential General Election Results, compiled from state election offices ( PDF ) ( Excel )" (`/documents/5644/2024presgeresults.pdf`, `/documents/5645/2024presgeresults.xlsx`). [measured by the reader] The workbook (21,376 bytes, Last-Modified 17 Jan 2025) has one sheet, 51 jurisdiction rows, electoral votes (Trump 312, Harris 226, total 538), 26 candidate columns, a none-of-these and a write-ins column, and TOTAL VOTES; totals Harris 75,017,613, Trump 77,302,580, all 155,238,302; it prints "Popular Vote: State Elections Offices", "Electoral Vote: State Certificates of Vote, U.S. National Archives and Records Administration", "Total Electoral Vote Needed to Win = 270" and a compilation date of "January 16, 2025". What the FEC has **not** posted is a biennial "Federal Elections 2024" compilation (the newest linked is 2022).
- Formats by year [measured from each year's page]: whole-publication workbooks for 2022, 2020 and 2016 (xlsx) and 2012, 2008, 2004 (xls); president-only xls for 2012, 2008, 2004 and 2000, and xlsx or PDF for 1996; PDFs only for 1994 back to 1982. The 2020 workbook (6,251,110 bytes, 19 sheets) has "Table 2 Electoral & Pop Vote" and "2020 Pres General Results"; the 2016 workbook has the same structure. The old binary `.xls` files were not parsed (no reader without installing software).
- **Terms on reuse of results: nothing printed.** [measured] No licence or copyright statement on the results index, on the year pages, inside the 2024, 2020 and 2016 workbooks, on `/about/privacy-and-security-policy/` or `/open/`. The only boilerplate is "This information is produced and disseminated at U.S. taxpayer expense." and a disclaimer that it creates no rights. A reuse restriction exists for contributor data (donor names and addresses may not be used to solicit or for commercial purposes, `/updates/sale-or-use-contributor-information/`); [inferred] it concerns donors, not results. Small defects [measured]: the 2020 table header prints "Trunp (R)".

**National Archives (`www.archives.gov/electoral-college`).**
- [stated] "The Electoral College consists of 538 electors. A majority of 270 electoral votes is required to elect the President." "The District of Columbia is allocated 3 electors and treated like a State for purposes of the Electoral College under the 23rd Amendment." Maine and Nebraska "appoint individual electors based on the winner of the popular vote within each Congressional district and then 2 'at-large' electors". Allocation page (reviewed November 4, 2024), re-read by me: "The allocations below are based on the 2020 Census. They are effective for the 2024 and 2028 presidential elections. Total Electoral Votes: 538*; Majority Needed to Elect: 270*", then 51 jurisdictions (California 54, Texas 40, Florida 30, New York 28, Pennsylvania 19, Illinois 19, ...); [measured by the reader] the list sums to 538 and equals the FEC 2024 workbook's column.
- Per-year tables at `/electoral-college/<year>` (1789 to 2024 linked from `/results`): [measured by the reader] the HTML tables for 1960, 1964, ... 2024 (17 pages) give 51 jurisdictions each year from 1964 (50 in 1960, before DC voted), 537 electoral votes in 1960 (majority 269) and 538 (270) in every year from 1964; the 2020 and 2024 tables equal the FEC's. HTML only for the tables; each state's Certificate of Ascertainment and of Vote is a PDF for recent years. Defects: the 2024 page still says "Check back for the Certificates of Vote from the 2024 election. They will be posted as they become available." although its table links a certificate for every state [measured]. The 2000 page records that a District of Columbia elector "cast a blank ballot", so DC cast 2 of its 3 votes (Bush 271, Gore 266) [stated].
- **The 269 to 269 case.** [stated, FAQ reviewed January 13, 2026] "Assuming that all 538 electoral votes are available, if no candidate receives a majority of electoral votes, the Presidential election leaves the Electoral College process and moves to Congress." The `/provisions` page lists the Twelfth Amendment and 3 U.S.C. §§ 1 to 18 and onward; I have not read the text of the Twelfth Amendment or of the statute, so what each chamber does and how it votes is **unread** here.
- Terms [stated, `/global-pages/privacy.html`]: "Works of the U.S. Government that have been produced by the National Archives and Records Administration are in the public domain and may be copied and distributed without permission. These works are available for worldwide use and reuse under the terms of the Creative Commons CC0 1.0 Universal license." and "However, not all materials appearing on this website are in the public domain." [inferred] The electoral-vote tables are NARA's own; the Certificates are state documents.

**Census Bureau (`www.census.gov`, `www2.census.gov`).**
- Current Population Survey Voting and Registration Supplement [stated]: "Voting and Registration | November of even years | Provide demographic information on persons who did and did not register to vote ... Periodicity: Biennial"; publication P20-590 (August 2026): "For every national election since 1964, we collected data on the characteristics of American voters." [measured] A survey sample, self-reported, with 90-percent margins of error in every table; the 2024 national "Total voted" is 154,308 thousand against the FEC's 155,238,302 votes for President.
- Free xlsx tables: Table 4a "Reported Voting and Registration of the Total Voting-Age Population, for States: November 2024" (`.../tables/p20/587/vote04a_2024.xlsx`, 15,882 bytes; the file path says `587`, the report is P20-590): per state the 18-plus population and the citizen 18-plus population in thousands, registered and voted counts, percentages and margins (US 260,363 and citizens 236,138). Historical Table A-5a/A-5b "Reported Voting and Registration for Total and Citizen Voting-Age Population, by State for Presidential Elections: 1972-2024" (`a5a.xlsx`, 19,336 bytes): percentages only, 1980 to 2024 for all states and DC, 1976 for the 25 largest states and 1972 for the 15 largest; [stated] "Prior to 1996, the CPS did not collect information on citizenship in a uniform way. Estimates for the citizenship population presented in this table prior to 1996 should be interpreted with caution". Public-use microdata exist (not downloaded). A second voting-age source: the Citizen Voting Age Population special tabulation from the ACS 5-year estimates, yearly 2009 to 2024, CSV at state level and below (not downloaded).
- **Terms: nothing printed** for the tables (no licence on the topic page, the table pages, the workbooks, the privacy or policy pages); the only terms found are the Census Data API's, which cover the API (a notice that the product "is not endorsed or certified by the Census Bureau") and not downloaded tables. The citation page says "The Census Bureau has no specific style recommendation".
- [measured] The topic page's teaser "73.6% of the voting-age population was registered to vote and 65.3% voted" quotes the **citizen** percentages of Table 4a (total-population percentages in the same table: 66.8 and 59.3).

**Dave Leip's Atlas of U.S. Presidential Elections: unread** (Cloudflare challenge, above). The only thing read about it is MEDSL's one-line description on its data page ("a resource for U.S. Presidential Election results and other types of election data"), which also lists the United States Election Project as a source of turnout time series (not visited). What is free or paid, its prices and its terms are unknown from the source.

## 4. Table of corrections (old, new, source)

"Old" is the first report (`research/decisiveness-models.md`) unless another file is named. Each "new" is a fact I measured or a source states; none is a choice.

| # | Old | New | Source |
|---|---|---|---|
| 1 | 43 scholarly, news, archive and data hosts refused (403 at CONNECT) on 2026-11-06; only `raw.githubusercontent.com` reachable (sections 0, 1.2, 1.3) | On 2026-11-07 `sites.stat.columbia.edu`, `plato.stanford.edu`, `www.nber.org`, `projects.economist.com`, `github.com` (clone), `dataverse.harvard.edu`, `www.fec.gov`, `www.archives.gov`, `www.census.gov` and others answered 200. Still unreadable: `web.archive.org` (connection reset), 538 (redirects to ABC), `andrewgelman.com`, ScienceDirect, Wiley, CORE, the Villanova PDF and `uselectionatlas.org` (Cloudflare challenge), Springer and the AER (paywall or login) | section 1 (measured) |
| 2 | Method: generic User-Agent `Mozilla/5.0 (X11; Linux x86_64) research-fetch` (1.1) | The environment's safety monitor denied that header as "Bot Check Circumvention"; curl's default header works. Do not copy the first report's method line | section 1 (measured) |
| 3 | WebFetch not used (1.4) | One WebFetch call was made by a reader on a Wayback URL after curl was reset; it returned SITE_BLOCKED. Also one reader request with `-L` followed a 538 redirect and downloaded one ABC News page outside its host list (deleted, never read). Disclosed so the orchestrator can judge | section 1 |
| 4 | Directive could not be carried out; "no source I read states a decisiveness model" (0, 5) | The four Gelman papers and Mulligan and Hunter are read; formulas in section 3.1 | section 3.1 |
| 5 | S1: README quote ends "...for the 2016 election. BuzzFeed News downloaded the data on November 5, 2016." | The source has a semicolon and continues: "; you can find it in the data/fivethirtyeight directory." | BuzzFeed README line 11 (stated) |
| 6 | S1: BuzzFeed's "power ratio" divides total power by the number of voters (as understood) | It sums `registered voters × power` over states within a demographic, divides by that demographic's own registered voters, then divides by the "Total" row's ratio; the voters are Census 2012 registered-voter counts | demographic notebook cells 13, 15, 17 (stated) |
| 7 | Appendix A: the CSV's columns (abbreviation, power) | The CSV has a fourth column `state` (upper case; empty for the five Maine and Nebraska district rows). Appendix A is unchanged: its 56 rows have 0 differences from the CSV | BuzzFeed CSV (measured) |
| 8 | S2: model scripts `final_model_2008.R` etc.; path returned 404; the repository tree could not be listed | The README names those, but the files are `scripts/model/final_2008.R`, `final_2012.R`, `final_2016.R`; the default branch is `master` (no `main`); the fitted-model files behind the README tables are not in the repository | README lines 29 to 31; clone (measured) |
| 9 | S2: `se` read as the forecast standard deviation of the share (inferred) | `se = (high − mean)/1.68` in `README.Rmd` (lines 555, 1073, 1594), fits all 156 table rows; not computed from the draws; a normal 95% interval would give (high − mean)/1.96, so `se` is about 1.17 times that. No comment explains 1.68 | README.Rmd (stated); script (measured) |
| 10 | S2: `mean`, `low`, `high`, `prob` inferred | Stated by the code: mean of the posterior draws of the Democratic two-party share on the last day; 2.5% and 97.5% quantiles; `prob = mean(x > 0.5)`; the national row is the vote-weighted average of the state shares (popular vote, not Electoral College) | README.Rmd (stated) |
| 11 | S2: "survey mode and population" | "survey mode and survey population" | README lines 8 to 15 (stated) |
| 12 | S5 (third party), repeated in 3.5: "the FEC has not published 2024" | The FEC publishes "Official 2024 Presidential General Election Results" (PDF and Excel), compiled January 16, 2025; only the biennial "Federal Elections 2024" compilation is absent | `fec.gov` results page; workbook (stated, measured) |
| 13 | S5 and 3.5: Algara and Amlani "compiled from CQ Press / ICPSR historical returns" | Not stated in the depositor's manual or record; the source of the county vote counts is in the unread *Electoral Studies* paper. Title is not "Historical President 1868-2020" but "Replication Data for: Partisanship & Nationalization ... 1872-2020"; Alaska is absent from the county files; the state file holds shares, not counts | manual; Dataverse record (stated, measured) |
| 14 | 3.5: MEDSL county file: Dataverse unreachable, licence unread | Licence field `CC0 1.0` (v20.0, 2026-02-25); file and codebook behind a guestbook requiring an email; the state-level file 1976 to 2024 is free and CC0 | Dataverse API (stated, re-checked) |
| 15 | S5 (third party): "MEDSL 2016 totals inflated in AL, SC, AR and IN" | Not seen in MEDSL's state file (equal to the FEC in AL, SC, IN; AR total 41 lower); county file unread. MEDSL's own 2024 README shows its county dataset about 5% high for Indiana and Vermont incomplete | section 3.5 (measured, stated) |
| 16 | Directive premise: p falls like 1/N under an uncertain share and exponentially when the share is known | Confirmed only for a known share different from 1/2 (exponentially small); for a known share of exactly 1/2 the tie probability is about sqrt(2/(πv)), falling as 1/sqrt(v) | M&H eq. (1) and fn. 14; GKBafumi, GKT (section 3.1 D) |
| 17 | `research/electoral-systems.md` line 28 and section 10.3 item 1: random-voting probability "of the form (2/sqrt(pi)) * (1/sqrt(n_j))" (WebFetch extract; constants unverifiable) | `p_vj(0.5)/n_j = sqrt(2/π) · 1/sqrt(n_j)` (0.7979/sqrt(n)), page image of GKBafumi p. 662. 2/sqrt(π) = 1.128 is not what is printed | GKBafumi (stated, page image; checked by exact enumeration) |
| 18 | `research/electoral-systems.md` line 28: "Appendix eq. 3: Pr = E[Phi(v − 1/n) − Phi(v)]" | `E[π(v + 1/n) − π(v)]`, with π(v) the probability that party A wins given true share v (a symbol the paper takes for a probability, not the normal distribution function) | GKBafumi p. 674 (stated, page image) |
| 19 | `research/frameworks-benefit-cost.md` line 273: Mulligan and Hunter (2003) "about 1 in 100,000 votes (House)", source the NBER PDF | 1 in 100,000 is the **working paper's** abstract ("U.S. elections"); the published (2003) abstract at EconPapers says 1 in 89,000 "in U.S. Congressional elections". The published body is unread (Springer paywall); label which version a figure comes from | NBER WP 8590 (stated); `research/historical-close-races.md` line 18 |
| 20 | Banzhaf (1968) "One Man, 3,312 Votes" cited as *Villanova Law Review* 13 | The sources disagree: volume 13 in GKB (1998) and GKT (2002), volume 16 in a footnote of GKBafumi (2004). Unresolved (the paper itself is unread) | reference lists (stated) |

## 5. Open points where sources disagree or print something that does not agree with itself

I choose none of these. For each, both readings and where they come from.

1. **The tie constant.** Settled for GKBafumi: `sqrt(2/π)/sqrt(n_j)`, printed at p. 662, exact enumeration agrees (1,001 voters: 0.025225 exact, 0.025219 by the formula). `research/electoral-systems.md` section 10.3 reads 2/sqrt(π); that was an extraction error (correction 17). Remaining: which *quantity* the constant measures depends on the convention in point 4.
2. **GKBafumi's worked example does not agree with itself.** [stated, p. 663, section 2.3] 10,000 voters, forecast 52%, standard error 3%: "[1/sqrt(2π)(0.03)] exp(−0.5(0.05/0.03)²)/n_j = 1.84/n_j" [measured]: the printed expression equals 3.316/n_j (13.298 × 0.2494). A 2-point distance from 50% (the 52% forecast) would give 10.648/n_j; a 6-point distance 1.80/n_j; none gives 1.84. The text, the arithmetic and the result are three different statements. I have not decided which is intended.
3. **GKT eq. (2) and (5), a factor of 2.** [stated, printed with the density of the "difference in vote proportions"] If that density is the density of (share for A) − (share for B) = 2v − 1, it is half the density of v at the tie, and the probability would be half the one GKB and GKBafumi print. And [measured] GKT's exact random-voting expression C(n_j − 1, (n_j − 1)/2) omits the factor 2^−(n_j − 1) (section 3.1 C); the approximation next to it, sqrt(2/(π n_j)), is right.
4. **What the "decisive vote" is compared with.** GKB p. 3 says it considers "a person who will either vote for one candidate or not vote" (voting versus abstaining) but prints f_v(.5)/n; GKBafumi and GKT define voting power as P(A wins | the voter supports A) − P(A wins | supports B) with ties broken by coin flips. [measured, exact binomial computation, here and in `research/electoral-systems.md` section 10.3] Under coin-flip ties, the A-versus-B swing is the exact-tie probability, f_v(.5)/n; the effect of voting for A versus abstaining is half of that. So the same printed expression f/n answers the second question only if the half is ignored. Mulligan and Hunter's "pivotal vote" is a third definition (a vote for the winner in a one-vote election, or any vote in a tie), which their eq. (3) and (4) turn into f(1/2)/(v + 1) and 1.5 times that for the pivot election. These are conventions; the sources state them differently.
5. **GSE's two stated steps.** (a) The "density at 0 of the Student-t distribution" is of the popular-vote margin **in votes**; with a fixed number of voters the margin A − B takes only every second integer, so a density in votes is half the exact-tie probability. Whether the paper means the tie probability or the vote-versus-abstain effect is not stated. (b) "Scale S" is the standard deviation of the simulated margins; for a Student-t with 4 degrees of freedom the scale parameter and the standard deviation differ by sqrt(2), and the density at the centre is 0.375/scale (normal: 0.399/sd). The paper does not say which it uses. Both are [inferred] from the text; the code is not published with it.
6. **Banzhaf (1968) volume** (correction 20).
7. **538's index.** Defined only second-hand ("the relative likelihood that an individual voter in a state will determine the Electoral College winner", Fusion 2016-09-20); the baseline (relative to what), the unit and whether the "tipping-point probability" feeds it are not read.
8. **Mulligan and Hunter.** (a) Working paper (1 in 100,000) against published abstract (1 in 89,000) for the same headline (correction 19). (b) The conclusion "2/v" and the figure "slope −1" sit beside the paper's own statement that three size groups "do not appear to be 1/v" exactly (4.5, 2.7, 0.2 in units of 10^-4 for average sizes 5,570, 14,236, 51,169) and that for US House elections below about 30,000 to 40,000 votes the frequency rises with size.
9. **The Economist's `se`.** The README's `se` is (high − mean)/1.68 with no stated reason, while the plots in the same file use /1.96 (three places).
10. **MEDSL against the FEC.** `totalvotes` differs in 14, 21 and 18 states (2024, 2020, 2016); candidate counts differ by up to about 14,000 (New York 2020). MEDSL's codebook is stale (title, source, `mode`). Whether the county file has the third party's defects is unknown (gated).
11. **Maine and Nebraska, faithless electors, 269 to 269.** The sources ignore the first two (GKB p. 2) or call ignoring them a mistake in 2008 (GSE footnote 7); the National Archives states the allocation rules and that a failure of any candidate to reach 270 "moves to Congress". What follows is not read here.
12. **A recount "gray area".** GKBafumi's appendix assumes a smooth, fixed disputed zone and two approximations and concludes the decisive probability is unchanged, p(0.5)/n; Mulligan and Hunter find, in their data, that recounts roughly halve the frequency of a pivotal ballot and say a preliminary look suggests "1/v, rather than 2/v". The two statements are about different things (a model's disputed zone against a count of official margins); both are printed.

## 6. Still unread, and why

| What | Why | What would open it |
|---|---|---|
| 538's index definition and baseline; 538's 2008 FAQ figure; 538's tipping-point article; the 2016 forecast page and any archived 538 copy | `fivethirtyeight.com` and `projects.fivethirtyeight.com` redirect every URL to `abcnews.com`; `web.archive.org` resets the connection after the TLS hello | Allow `web.archive.org` in the environment's network policy (the maker's setting); the first targets: `web.archive.org/web/20161106id_/http://projects.fivethirtyeight.com/2016-election-forecast/` and the 538 URLs in the brief |
| Chamberlain and Rothschild 1981; Good and Mayer 1975; Beck 1975; Margolis 1977; Banzhaf 1965 and 1968; Penrose 1946; Stromberg 2008; Riker and Ordeshook 1968; Ferejohn and Fiorina 1974; Myerson 2000; Katz, Gelman and King 2002 | ScienceDirect, Wiley, CORE and the Villanova PDF endpoint answer a Cloudflare challenge; Springer and the AER are behind a paywall or login; the others have no free text I could reach. Not circumvented (`_COMMON.md` 6) | Copies supplied by the maker (a library login or a download by hand); or a free copy at a host not yet tried |
| Gelman's blog post of 2016-11-07 on the chance a vote decides the election, and any blog post by Gelman or Silver on later years | `andrewgelman.com` answers a Cloudflare challenge. I did not look for the same post on another host | Allow `web.archive.org`; or the maker saves the page by hand |
| Economist's `p_decisive_vote` method (formula, electorate size, tie definition); terms for its page numbers | not stated on the pages read; the repository has no code for it | An Economist methodology page if one exists; none in the three pages read |
| MEDSL county file `countypres_2000-2024.tab` and its codebook (the `mode` values, the third party's defect claims) | Dataverse guestbook 458 requires name, email, institution and position | The maker answers the guestbook (a form, no account, no cost) and saves the file, or says to answer it with a stated identity |
| Dave Leip's Atlas (coverage, price, terms) | Cloudflare challenge on the first request | The maker, or a source other than the site |
| Algara and Amlani county Rdata (R binaries), the *Electoral Studies* paper | R binaries, not opened; the paper is behind a publisher | R in the environment, kept in a sandbox; or the maker's download |
| FEC 2004 to 2012 `.xls` and 2022, 2018 workbooks; 2000 PDF; per-state election-office pages and their terms | old binary format not parsed; not requested | a converter in the environment; later passes |
| Census CPS microdata, CVAP CSVs | not downloaded | later passes |
| Text of the Twelfth Amendment and 3 U.S.C. §§ 1 to 18 (contingent election) | pages listed on the National Archives site but not read | a later pass, at archives.gov or congress.gov |
| GKT Figure 2b plotted values; GSE Figures 1 to 3 values; GKBafumi Figure 3 exponents | printed only as plots | digitising is a measurement of a figure and would be marked as such |
| The published (2003) text of Mulligan and Hunter | Springer paywall | a copy supplied |
| The first report's own unchecked items (`fivethirtyeight/data` README; the 19 repository searches; Wikipedia pages) | no bearing on the model | not pursued |

---

## Appendices

Appendix A and Appendix B are the first report's, **copied unchanged**. They were diffed against their sources on 2026-11-07: Appendix A (56 rows) against `voter-power-index.csv` and Appendix B (3 tables, 156 rows) against the Economist README: **0 differences** each (sections 2, S1 and S2). They are inputs for any forecast-based calculation; the `se` column of Appendix B is `(high − mean)/1.68`, not a standard deviation (correction 9).

## Appendix A. FiveThirtyEight "Voter Power Index", 2016, as scraped by BuzzFeed News on 2016-11-05 (S1)
*Generated mechanically from `data/fivethirtyeight/voter-power-index.csv` [measured: script read the file and printed it]. "<0.1" on the 538 page appears here as 0.0 (BuzzFeed's rule). Rows are in 538's page order. Congressional-district rows (Maine and Nebraska) are separate electoral votes.*

| abbrev | power | state_raw |
|---|---|---|
| NH | 5.6 | New Hampshire |
| NV | 4.9 | Nevada |
| NM | 4.7 | New Mexico |
| MI | 3.1 | Michigan |
| CO | 3.1 | Colorado |
| AK | 3.1 | Alaska |
| PA | 2.7 | Pennsylvania |
| NC | 2.7 | North Carolina |
| FL | 2.5 | Florida |
| VA | 2.3 | Virginia |
| NE2 | 1.9 | Nebraska 2nd District |
| WI | 1.7 | Wisconsin |
| AZ | 1.6 | Arizona |
| ME2 | 1.5 | Maine 2nd District |
| MN | 1.5 | Minnesota |
| OH | 1.4 | Ohio |
| DE | 1.2 | Delaware |
| ME | 1.2 | Maine - statewide |
| IA | 1.0 | Iowa |
| RI | 0.9 | Rhode Island |
| ME1 | 0.6 | Maine 1st District |
| GA | 0.6 | Georgia |
| OR | 0.6 | Oregon |
| NE1 | 0.6 | Nebraska 1st District |
| SD | 0.6 | South Dakota |
| CT | 0.5 | Connecticut |
| SC | 0.5 | South Carolina |
| MT | 0.3 | Montana |
| NJ | 0.3 | New Jersey |
| WA | 0.2 | Washington |
| UT | 0.2 | Utah |
| HI | 0.1 | Hawaii |
| IL | 0.0 | Illinois |
| VT | 0.0 | Vermont |
| NE3 | 0.0 | Nebraska 3rd District |
| MO | 0.0 | Missouri |
| LA | 0.0 | Louisiana |
| MD | 0.0 | Maryland |
| WY | 0.0 | Wyoming |
| TX | 0.0 | Texas |
| KS | 0.0 | Kansas |
| IN | 0.0 | Indiana |
| TN | 0.0 | Tennessee |
| MS | 0.0 | Mississippi |
| KY | 0.0 | Kentucky |
| NY | 0.0 | New York |
| NE | 0.0 | Nebraska - statewide |
| AR | 0.0 | Arkansas |
| ID | 0.0 | Idaho |
| AL | 0.0 | Alabama |
| CA | 0.0 | California |
| MA | 0.0 | Massachusetts |
| ND | 0.0 | North Dakota |
| OK | 0.0 | Oklahoma |
| WV | 0.0 | West Virginia |
| DC | 0.0 | District of Columbia |

## Appendix B. The Economist's per-state forecasts, 2008, 2012, 2016 (S2)
*Generated mechanically from the tables in the README under "Predictions for each state" [measured: parsed by script]. Column meanings are NOT defined in the README (see S2). Rows in the README's order. The row `–` is as printed.*

**2008** (52 rows)

| state | mean | low | high | prob | se |
|---|---|---|---|---|---|
| NC | 0.502 | 0.466 | 0.538 | 0.545 | 0.021 |
| MO | 0.509 | 0.474 | 0.543 | 0.704 | 0.020 |
| FL | 0.514 | 0.479 | 0.548 | 0.788 | 0.020 |
| IN | 0.484 | 0.448 | 0.519 | 0.179 | 0.021 |
| AR | 0.477 | 0.439 | 0.516 | 0.124 | 0.023 |
| OH | 0.524 | 0.489 | 0.559 | 0.917 | 0.021 |
| MT | 0.475 | 0.437 | 0.512 | 0.094 | 0.022 |
| VA | 0.527 | 0.491 | 0.564 | 0.917 | 0.022 |
| GA | 0.473 | 0.437 | 0.511 | 0.083 | 0.022 |
| WV | 0.470 | 0.434 | 0.507 | 0.058 | 0.022 |
| AZ | 0.468 | 0.429 | 0.507 | 0.055 | 0.023 |
| NV | 0.532 | 0.494 | 0.568 | 0.952 | 0.022 |
| CO | 0.533 | 0.496 | 0.571 | 0.961 | 0.022 |
| – | 0.539 | 0.517 | 0.562 | 1.000 | 0.013 |
| LA | 0.460 | 0.421 | 0.500 | 0.025 | 0.024 |
| MS | 0.457 | 0.418 | 0.497 | 0.019 | 0.024 |
| TX | 0.454 | 0.413 | 0.495 | 0.015 | 0.024 |
| SD | 0.453 | 0.413 | 0.492 | 0.008 | 0.023 |
| SC | 0.450 | 0.412 | 0.488 | 0.003 | 0.023 |
| NH | 0.550 | 0.514 | 0.587 | 0.998 | 0.022 |
| ND | 0.449 | 0.409 | 0.487 | 0.006 | 0.023 |
| PA | 0.554 | 0.518 | 0.588 | 0.999 | 0.020 |
| TN | 0.445 | 0.406 | 0.484 | 0.003 | 0.023 |
| WI | 0.557 | 0.521 | 0.592 | 0.999 | 0.021 |
| KY | 0.442 | 0.405 | 0.478 | 0.001 | 0.021 |
| MN | 0.559 | 0.523 | 0.595 | 1.000 | 0.021 |
| NM | 0.561 | 0.522 | 0.599 | 0.998 | 0.023 |
| IA | 0.562 | 0.526 | 0.597 | 1.000 | 0.021 |
| MI | 0.565 | 0.530 | 0.598 | 1.000 | 0.020 |
| OR | 0.572 | 0.535 | 0.608 | 1.000 | 0.021 |
| KS | 0.424 | 0.387 | 0.460 | 0.000 | 0.022 |
| AK | 0.417 | 0.377 | 0.458 | 0.000 | 0.024 |
| WA | 0.584 | 0.548 | 0.620 | 1.000 | 0.021 |
| ME | 0.584 | 0.545 | 0.620 | 1.000 | 0.021 |
| NJ | 0.590 | 0.552 | 0.627 | 1.000 | 0.022 |
| AL | 0.405 | 0.368 | 0.444 | 0.000 | 0.023 |
| NE | 0.402 | 0.365 | 0.440 | 0.000 | 0.023 |
| DE | 0.616 | 0.577 | 0.652 | 1.000 | 0.022 |
| CA | 0.617 | 0.578 | 0.653 | 1.000 | 0.022 |
| MD | 0.618 | 0.572 | 0.664 | 1.000 | 0.027 |
| CT | 0.619 | 0.579 | 0.655 | 1.000 | 0.022 |
| OK | 0.378 | 0.340 | 0.417 | 0.000 | 0.023 |
| IL | 0.629 | 0.591 | 0.663 | 1.000 | 0.020 |
| WY | 0.366 | 0.331 | 0.404 | 0.000 | 0.022 |
| MA | 0.642 | 0.603 | 0.680 | 1.000 | 0.023 |
| ID | 0.354 | 0.318 | 0.392 | 0.000 | 0.022 |
| NY | 0.647 | 0.610 | 0.683 | 1.000 | 0.021 |
| VT | 0.654 | 0.615 | 0.693 | 1.000 | 0.023 |
| UT | 0.343 | 0.306 | 0.381 | 0.000 | 0.023 |
| HI | 0.663 | 0.622 | 0.703 | 1.000 | 0.024 |
| RI | 0.670 | 0.633 | 0.706 | 1.000 | 0.021 |
| DC | 0.933 | 0.917 | 0.946 | 1.000 | 0.008 |

**2012** (52 rows)

| state | mean | low | high | prob | se |
|---|---|---|---|---|---|
| VA | 0.504 | 0.467 | 0.539 | 0.586 | 0.021 |
| CO | 0.505 | 0.471 | 0.541 | 0.617 | 0.021 |
| FL | 0.495 | 0.457 | 0.531 | 0.394 | 0.021 |
| OH | 0.510 | 0.474 | 0.545 | 0.704 | 0.021 |
| – | 0.510 | 0.489 | 0.533 | 0.773 | 0.014 |
| NH | 0.513 | 0.478 | 0.548 | 0.758 | 0.021 |
| IA | 0.514 | 0.480 | 0.550 | 0.785 | 0.021 |
| NC | 0.485 | 0.451 | 0.521 | 0.212 | 0.022 |
| NV | 0.516 | 0.478 | 0.554 | 0.797 | 0.022 |
| WI | 0.521 | 0.486 | 0.556 | 0.876 | 0.021 |
| PA | 0.528 | 0.492 | 0.563 | 0.937 | 0.021 |
| MN | 0.534 | 0.500 | 0.568 | 0.974 | 0.021 |
| MI | 0.537 | 0.502 | 0.572 | 0.979 | 0.021 |
| OR | 0.538 | 0.499 | 0.575 | 0.971 | 0.022 |
| MO | 0.460 | 0.424 | 0.496 | 0.015 | 0.022 |
| NM | 0.540 | 0.500 | 0.580 | 0.976 | 0.023 |
| IN | 0.455 | 0.420 | 0.492 | 0.006 | 0.022 |
| MT | 0.453 | 0.417 | 0.489 | 0.006 | 0.022 |
| GA | 0.452 | 0.413 | 0.492 | 0.009 | 0.024 |
| AZ | 0.452 | 0.414 | 0.491 | 0.009 | 0.023 |
| NJ | 0.556 | 0.518 | 0.593 | 0.999 | 0.022 |
| ME | 0.557 | 0.520 | 0.593 | 0.999 | 0.021 |
| WA | 0.561 | 0.526 | 0.596 | 1.000 | 0.021 |
| SC | 0.438 | 0.395 | 0.483 | 0.004 | 0.026 |
| CT | 0.567 | 0.529 | 0.603 | 1.000 | 0.022 |
| SD | 0.431 | 0.392 | 0.470 | 0.000 | 0.023 |
| ND | 0.422 | 0.385 | 0.461 | 0.000 | 0.023 |
| MS | 0.421 | 0.375 | 0.468 | 0.000 | 0.028 |
| TN | 0.419 | 0.383 | 0.458 | 0.000 | 0.023 |
| WV | 0.416 | 0.378 | 0.456 | 0.000 | 0.024 |
| CA | 0.585 | 0.549 | 0.622 | 1.000 | 0.022 |
| MA | 0.588 | 0.552 | 0.623 | 1.000 | 0.021 |
| TX | 0.409 | 0.372 | 0.448 | 0.000 | 0.023 |
| NE | 0.407 | 0.370 | 0.444 | 0.000 | 0.022 |
| IL | 0.599 | 0.562 | 0.635 | 1.000 | 0.021 |
| LA | 0.401 | 0.363 | 0.442 | 0.000 | 0.024 |
| DE | 0.602 | 0.555 | 0.646 | 1.000 | 0.026 |
| KY | 0.398 | 0.360 | 0.438 | 0.000 | 0.024 |
| KS | 0.395 | 0.355 | 0.435 | 0.000 | 0.024 |
| MD | 0.607 | 0.565 | 0.646 | 1.000 | 0.023 |
| RI | 0.616 | 0.575 | 0.654 | 1.000 | 0.023 |
| AR | 0.384 | 0.346 | 0.423 | 0.000 | 0.023 |
| AL | 0.383 | 0.342 | 0.423 | 0.000 | 0.024 |
| NY | 0.620 | 0.584 | 0.655 | 1.000 | 0.021 |
| AK | 0.363 | 0.320 | 0.407 | 0.000 | 0.026 |
| VT | 0.660 | 0.620 | 0.697 | 1.000 | 0.022 |
| HI | 0.661 | 0.620 | 0.699 | 1.000 | 0.023 |
| ID | 0.331 | 0.295 | 0.369 | 0.000 | 0.022 |
| OK | 0.330 | 0.293 | 0.369 | 0.000 | 0.023 |
| WY | 0.313 | 0.277 | 0.350 | 0.000 | 0.022 |
| UT | 0.291 | 0.257 | 0.326 | 0.000 | 0.021 |
| DC | 0.903 | 0.880 | 0.924 | 1.000 | 0.012 |

**2016** (52 rows)

| state | mean | low | high | prob | se |
|---|---|---|---|---|---|
| FL | 0.496 | 0.457 | 0.536 | 0.435 | 0.024 |
| NV | 0.508 | 0.467 | 0.548 | 0.652 | 0.024 |
| NC | 0.492 | 0.451 | 0.532 | 0.340 | 0.024 |
| – | 0.512 | 0.485 | 0.540 | 0.791 | 0.017 |
| NH | 0.514 | 0.475 | 0.554 | 0.736 | 0.024 |
| PA | 0.514 | 0.475 | 0.553 | 0.745 | 0.024 |
| CO | 0.516 | 0.476 | 0.555 | 0.774 | 0.023 |
| OH | 0.484 | 0.445 | 0.523 | 0.217 | 0.023 |
| MI | 0.518 | 0.479 | 0.558 | 0.816 | 0.024 |
| WI | 0.521 | 0.483 | 0.561 | 0.844 | 0.024 |
| IA | 0.478 | 0.439 | 0.517 | 0.148 | 0.023 |
| VA | 0.523 | 0.482 | 0.562 | 0.863 | 0.023 |
| MN | 0.527 | 0.489 | 0.568 | 0.909 | 0.024 |
| AZ | 0.471 | 0.430 | 0.510 | 0.077 | 0.024 |
| GA | 0.470 | 0.430 | 0.508 | 0.069 | 0.023 |
| NM | 0.532 | 0.489 | 0.575 | 0.926 | 0.025 |
| ME | 0.542 | 0.503 | 0.582 | 0.985 | 0.024 |
| SC | 0.452 | 0.411 | 0.493 | 0.011 | 0.024 |
| OR | 0.549 | 0.509 | 0.590 | 0.992 | 0.025 |
| TX | 0.443 | 0.403 | 0.483 | 0.002 | 0.024 |
| MO | 0.439 | 0.401 | 0.478 | 0.001 | 0.023 |
| MS | 0.436 | 0.397 | 0.476 | 0.001 | 0.024 |
| CT | 0.565 | 0.525 | 0.607 | 1.000 | 0.024 |
| WA | 0.567 | 0.528 | 0.607 | 1.000 | 0.024 |
| DE | 0.568 | 0.525 | 0.609 | 1.000 | 0.025 |
| AK | 0.425 | 0.384 | 0.468 | 0.000 | 0.026 |
| NJ | 0.578 | 0.537 | 0.619 | 1.000 | 0.024 |
| IN | 0.419 | 0.380 | 0.458 | 0.000 | 0.023 |
| IL | 0.583 | 0.543 | 0.623 | 0.999 | 0.024 |
| LA | 0.410 | 0.371 | 0.449 | 0.000 | 0.024 |
| MT | 0.406 | 0.368 | 0.446 | 0.000 | 0.024 |
| RI | 0.595 | 0.555 | 0.636 | 1.000 | 0.024 |
| KS | 0.403 | 0.368 | 0.441 | 0.000 | 0.022 |
| TN | 0.403 | 0.365 | 0.442 | 0.000 | 0.023 |
| SD | 0.398 | 0.361 | 0.438 | 0.000 | 0.023 |
| NY | 0.611 | 0.571 | 0.649 | 1.000 | 0.023 |
| ND | 0.389 | 0.352 | 0.429 | 0.000 | 0.024 |
| NE | 0.388 | 0.351 | 0.428 | 0.000 | 0.023 |
| AL | 0.384 | 0.346 | 0.423 | 0.000 | 0.023 |
| AR | 0.382 | 0.345 | 0.421 | 0.000 | 0.023 |
| CA | 0.620 | 0.581 | 0.658 | 1.000 | 0.023 |
| UT | 0.375 | 0.337 | 0.412 | 0.000 | 0.022 |
| KY | 0.373 | 0.336 | 0.411 | 0.000 | 0.023 |
| MA | 0.629 | 0.591 | 0.668 | 1.000 | 0.023 |
| MD | 0.639 | 0.598 | 0.677 | 1.000 | 0.023 |
| WV | 0.353 | 0.316 | 0.390 | 0.000 | 0.022 |
| ID | 0.349 | 0.313 | 0.386 | 0.000 | 0.022 |
| OK | 0.342 | 0.305 | 0.378 | 0.000 | 0.022 |
| VT | 0.658 | 0.619 | 0.696 | 1.000 | 0.023 |
| HI | 0.661 | 0.620 | 0.699 | 1.000 | 0.023 |
| WY | 0.289 | 0.255 | 0.324 | 0.000 | 0.021 |
| DC | 0.908 | 0.885 | 0.928 | 1.000 | 0.012 |

