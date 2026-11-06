# Decisiveness models and published estimates: research report

*Written 2026-11-06 (about 19:55 UTC) by a Sonnet 5.5 research subagent of the orchestrator, from the directive "survey the models and published estimates of the probability that one vote is decisive". Every fact is marked [measured] (I ran it or computed it, shown how), [stated] (a source says it, with where), or [inferred]. Sources I could not read are listed as unread, with the reason.*

## 0. Read this first: the directive could not be carried out as written

**The substance of the directive (the formulas, the published numbers for real elections) is almost entirely UNREAD.** The session's outbound network policy refuses every scholarly, news, data-archive and encyclopedia host I tried. Only GitHub's raw-file host and a few GitHub paths are reachable. I did not write any formula or any decisiveness estimate from memory, because the directive and `CLAUDE.md` forbid it and because a formula "from memory" is exactly what the site must not show.

What I did instead: (a) measured and recorded exactly what is blocked (section 1), so the block can be lifted by the maker in one settings change; (b) read the few things that *are* reachable and that bear on the directive (section 2: a 2016 snapshot of FiveThirtyEight's published "Voter Power Index" by state, scraped by BuzzFeed News; the Economist's open model repository with its per-state forecast means and standard errors for 2008, 2012 and 2016, which are exactly the kind of input a forecast-based decisiveness calculation needs; and three data-licence statements); (c) wrote a read plan for each of the five parts of the directive, so the next pass, once the hosts are open, can go straight to the sources (section 3).

**What the orchestrator needs to decide** (the reason for each is in section 1):
1. Ask the maker to widen the environment's network access (the documentation tool says this is done in *Project settings, Cloud environment menu, Add cloud environment*, by choosing a broader access level or adding hosts under *Allowed domains*; the project "has no cloud environment selected, so it runs on a built-in one that has no settings" [stated, `read_documentation` topic `environment.network`]). The hosts I need are listed in section 1.3. The three sibling research subagents are blocked the same way: the section 0 of each of `research/electoral-systems.md`, `research/frameworks-benefit-cost.md` and `research/historical-close-races.md` says curl was refused for the academic and data hosts it tried [stated, those files as they stood at about 19:58 UTC].
2. Or say explicitly that WebFetch may be used despite the policy. I did **not** use it (section 1.4 gives my reasons).

---

## 1. Access: what is and is not reachable [measured]

### 1.1 Method
`curl -sSL` through the session's proxy (HTTPS_PROXY, CA bundle `/root/.ccr/ca-bundle.crt`), generic User-Agent `Mozilla/5.0 (X11; Linux x86_64) research-fetch`, no email address anywhere, at least 3 to 4 seconds between requests, one request per host except the two GitHub hosts, which got several requests, each at least 4 seconds apart (search requests 7 seconds apart). All files saved under `/tmp/claude-0/research-a/`, outside the repository. A refusal here is a `403` answered by the **egress proxy to the CONNECT request** (`curl: (56) CONNECT tunnel failed, response 403`), not by the website. The proxy's own status page records them as `connect_rejected`, and its README says: "Most often the destination host is not allowed for this session. Do not retry or route around it — report the blocked host." [stated, `/root/.ccr/README.md`, section "403 / 407 from the proxy"]. I did not retry any refused host.

### 1.2 Hosts refused (43 hosts, one request each, all on 2026-11-06 between about 19:42 and 19:52 UTC)
- Gelman's pages: `sites.stat.columbia.edu`, `www.stat.columbia.edu`, `statmodeling.stat.columbia.edu` (plain `http://www.stat.columbia.edu` did not resolve: only HTTPS goes through the proxy).
- Preprints and indexes: `arxiv.org`, `export.arxiv.org`, `papers.ssrn.com`, `projecteuclid.org`, `core.ac.uk`, `citeseerx.ist.psu.edu`, `www.researchgate.net`, `www.semanticscholar.org`, `api.semanticscholar.org`, `api.openalex.org`, `api.crossref.org`, `doi.org`, `zenodo.org`, `osf.io`.
- Publishers: `www.jstor.org`, `www.cambridge.org`, `onlinelibrary.wiley.com`, `academic.oup.com`, `www.sciencedirect.com`, `journals.sagepub.com`, `www.tandfonline.com`, `www.pnas.org`.
- Archives and encyclopedia: `web.archive.org`, `archive.org`, `scholar.archive.org`, `en.wikipedia.org`, `cran.r-project.org`.
- Forecasters and press: `projects.fivethirtyeight.com`, `fivethirtyeight.com`, `www.economist.com`, `www.washingtonpost.com`, `www.nytimes.com`, `abcnews.go.com`.
- Data and government: `dataverse.harvard.edu`, `electionlab.mit.edu`, `www.census.gov`, `www.fec.gov`, `www.archives.gov`, `www.eac.gov`, `www.nationalpopularvote.com`.

The proxy's failure log also shows refusals at 19:41 to 19:42 UTC for `link.springer.com`, `www.nber.org`, `plato.stanford.edu`, `econpapers.repec.org`, `www.ncsl.org` and `ballotpedia.org`. I did not request those; the sibling reports list them among the hosts they were refused [stated, section 0 of `research/historical-close-races.md` and `research/frameworks-benefit-cost.md`].

### 1.3 Hosts reachable
- `raw.githubusercontent.com`: returned `200` for a file in each of six public repositories I asked for (the ones in section 2), and `404` for paths that do not exist. Note that without a directory listing I can only fetch a path I can name.
- `api.github.com`: the repository *search* endpoint returned `200` without credentials. Everything repository-specific outside this session's configured repositories was refused: `orgs/MEDSL/repos` gave `403 "This GitHub API path is not available: sessions are bound to their configured repositories..."`, and `repos/fivethirtyeight/data/contents` gave `403 "GitHub access to this repository is not enabled for this session. Use add_repo to request access..."`. The `github.com` HTML page of that repository gave the same message. I did **not** call `add_repo`: it changes what this session may reach, which is the maker's or orchestrator's decision.
- `gh` (the GitHub CLI): `gh auth status` reports "Failed to log in to github.com using token (GH_TOKEN) ... The token in GH_TOKEN is invalid." [measured]. I did not need it. Reported because `CLAUDE.md` says to tell the orchestrator at once when GitHub fails.
- Package registries (`pypi.org`, `registry.npmjs.org`, and so on) are on the proxy's no-proxy list [stated, proxy status JSON `noProxy`]; they are not sources for the papers, so I did not use them.

**Hosts to open for this research (minimum useful set), most important first:** `sites.stat.columbia.edu` (Gelman's own page, where I expect copies of his papers; unverified), `projecteuclid.org` (where I believe *Statistical Science* is hosted; unverified), `www.nber.org`, `arxiv.org`, `papers.ssrn.com`, `ideas.repec.org` and `econpapers.repec.org`, `web.archive.org` (the forecasters' old pages), `projects.fivethirtyeight.com` and `fivethirtyeight.com`, `www.economist.com` and `projects.economist.com`, `dataverse.harvard.edu` and `electionlab.mit.edu` (MIT Election Data and Science Lab), `www.census.gov`, `www.fec.gov`, `www.archives.gov`, `uselectionatlas.org` (Dave Leip's Atlas; not probed, it is a different host), `en.wikipedia.org` (secondary, for cross-checks only). Publisher hosts (`link.springer.com`, `onlinelibrary.wiley.com`, `www.tandfonline.com`, `journals.sagepub.com`, `www.cambridge.org`, `academic.oup.com`, `www.jstor.org`) are only worth opening to read free abstracts and see whether a free copy is linked; the directive says paywalled papers are recorded as unread.

### 1.4 Why I did not use WebFetch
The directive and `CLAUDE.md` allow WebFetch "only when curl is refused, and say so". Curl was refused, but by the sandbox's egress policy, not by a website, and the environment's own documentation says: "Do not retry or route around it — report the blocked host" [stated, `/root/.ccr/README.md`]. Separately, WebFetch returns a small model's summary; a summary cannot give "each formula exactly as written in the source", which is the point of the directive. If the orchestrator judges the first reason does not apply, I can be re-dispatched with WebFetch authorised, but the second reason stands: its output would be [summary, unverified] and could not carry the model.

---

## 2. What I could read

### S1. FiveThirtyEight "Voter Power Index", 2016 snapshot, as scraped by BuzzFeed News
- **Where:** `https://raw.githubusercontent.com/BuzzFeedNews/2016-11-voter-power-by-demographic/master/README.md`, `.../notebooks/scrape-voter-power-index.ipynb`, `.../data/fivethirtyeight/voter-power-index.csv`, `.../notebooks/demographic-analysis.ipynb` (all read whole; copies in `/tmp/claude-0/research-a/gh/`).
- [stated, README] "This analysis uses FiveThirtyEight's "Voter Power Index" estimates for the 2016 election. BuzzFeed News downloaded the data on November 5, 2016." The README links the source as `https://projects.fivethirtyeight.com/2016-election-forecast/#tipping-point`.
- [stated, scrape notebook] The values came from the HTML table of CSS class `tippingpointroi` (the second such table) on `http://projects.fivethirtyeight.com/2016-election-forecast/`; columns kept: state, power, abbreviation. Rule in BuzzFeed's code: "Set any value less than 0.1 to 0" for the page's text `<0.1`. **So every 0.0 in the CSV below means "<0.1 on the page", not zero** [stated, notebook code `if power == "<0.1": power = 0`]. The index is shown to one decimal.
- [stated, notebook output and CSV] Top of the table: NH 5.6, NV 4.9, NM 4.7, MI 3.1, CO 3.1, AK 3.1, PA 2.7, NC 2.7, FL 2.5, VA 2.3. Iowa is 1.0. The full table is in appendix A.
- [stated, demographic notebook] BuzzFeed multiplies the index by a state's registered voters and divides by total voters, "The 'power ratio' is the total power for a demographic divided by the number of registered voters". That is, BuzzFeed treats the index as a **per-voter weight**, comparable across states.
- **What I could not establish:** what 538 *defined* the index to be (relative to what baseline; whether 1.0 is the national average; how the "tipping-point" quantity was computed; the page's wording). The only 538 text I have is the class name `tippingpointroi` and the anchor `#tipping-point` [stated, in the code]. 538's own page is unread (blocked). Do **not** describe the number as a probability, nor as "relative to the average voter", until the definition is read at 538 (or its archived copy).
- **Value for the site:** it is a published, forecaster-computed *relative* measure of decisiveness for the 2016 presidential race, showing the order of magnitude by which state matters (NH 5.6 against about 0 for CA, NY, TX, which the page rounded to "<0.1"). It is a second source to compare any model of ours against, once its definition is read.

### S2. The Economist's open presidential forecast model (code and data) with per-state forecasts for 2008, 2012, 2016
- **Where:** `https://raw.githubusercontent.com/TheEconomist/us-potus-model/master/README.md` (read whole; "Last update on Thursday October 15, 2020 at 12:29 PM EDT").
- [stated] "Code for a dynamic multilevel Bayesian model to predict US presidential elections. Written in R and Stan." It builds on Pierre Kremp's implementation of Drew Linzer's dynamic linear model (Linzer 2013), adds corrections for partisan non-response, survey mode and population, uses informative state-level priors, and "specify[ies] empirical state-level correlations from political and demographic variables".
- [stated] Per-state "Predictions for each state" tables for **2008, 2012 and 2016** (labelled "economist (backtest)" in the performance tables), with columns `state, mean, low, high, prob, se`. 52 rows each: 50 states, DC, and one row labelled `–` [measured, parsed by script]. The README does **not** define the columns. [inferred] `mean` is the forecast Democratic share of the two-party vote (NH 2008 0.550, AK 2008 0.417), `low` and `high` an interval around it, `prob` the probability the Democrat carries the state, `se` the forecast standard deviation of the share; the `–` row is the national figure (mean 0.539, se 0.013 in 2008). These inferences must be checked against the Economist's R scripts or "how this works" page before use.
- **Why it matters here:** a forecast mean and a forecast standard deviation for each state's vote share are the inputs the forecast-based approach needs (probability density of the state's vote share at 50%, scaled by the number of voters). If the columns are what I infer, the README alone holds those inputs for three elections. Full tables are in appendix B. For example, for 2016 the README lists FL mean 0.496, se 0.024, prob 0.435.
- [stated] Licence: "This software is published by The Economist under the MIT licence. The data generated by The Economist are available under the Creative Commons Attribution 4.0 International License. The licences include only the data and the software authored by The Economist, and do not cover any Economist content or third-party data."
- [measured] A case-insensitive search of the README for `power`, `decisive`, `tipping`, `pivot` finds nothing: the repository documents a forecast, not a voter-power index. I tried the R script path named in the README (`scripts/model/final_model_2016.R`) on `master` and `main`; both returned `404` and I cannot list the repository (API refused, section 1.3), so the scripts are unread.

### S3. "What's my vote worth?" (a hobby app, relative Electoral College weight, not decisiveness)
- **Where:** `https://raw.githubusercontent.com/smrfeld/whats-my-vote-worth/master/README.md` (read whole). MIT licence, Oliver K. Ernst, 2020.
- [stated] Defines a state's "vote fraction" as its share of Electoral College votes relative to its share of population, using 2020 census populations. "California has the lowest fraction: 0.84, while Wyoming has the highest fraction: 3.2 ... every voter in Wyoming has the power of 3.8 Californians in deciding the U.S. presidential race."
- [inferred] This is a measure of **electoral votes per person**, not the probability that a vote is decisive, and it ignores closeness. It does not match this project's definition of importance. Useful only as an example of the lay "relative weight" visual that the site should *not* confuse with decisiveness. The author's phrase "power ... in deciding" shows how readily the two are conflated.

### S4. MIT Election Data and Science Lab, repository note
- **Where:** `https://raw.githubusercontent.com/MEDSL/2020-elections-official/master/README.md`.
- [stated] "This repository is deprecated. We are no longer maintaing 2020 precinct data in this repository. Our official 2020 precinct data are now available on the Dataverse here: https://dataverse.harvard.edu/dataverse/2020_precincts". The Dataverse host is refused (section 1.2), so the data itself is unread.

### S5. A third party's account of election-data sources and licences (secondary; useful for part 5 only)
- **Where:** `https://raw.githubusercontent.com/pmheideman/us-county-election-results/main/README.md`, `.../LICENSE-DATA.md`, `.../docs/DECISIONS.md` (read whole; Paul Heideman, v1.0.0, 2026-09-26). This is a third party's compilation and its statements are [stated by a third party], not primary.
- It compiles county results (President 1992 to 2024, House and Senate 1990 to 2024, 48 contiguous states), data CC BY 4.0, code MIT.
- [stated by the third party, `DECISIONS.md` section 9 and `LICENSE-DATA.md`] "Verified CC0 1.0 on Dataverse: MEDSL (House and Senate precinct files 2016-2024, county President 2000-2024) and Algara & Amlani." Algara & Amlani is "Harvard Dataverse doi:10.7910/DVN/DGUMFI" with "Historical President 1868-2020, Senate 1908-2020", "CC0 1.0 as deposited", "compiled from CQ Press / ICPSR historical returns, so the upstream provenance should be cited". The file name for MEDSL's county presidential returns is `countypres_2000-2024.tab`. "We do not use CQ Press or Leip's Atlas data directly." State election offices: "none grants CC0/CC BY"; terms vary (Florida, Indiana, Colorado, Wisconsin restrictive; North Carolina and Utah non-commercial).
- [stated by the third party] Known defects in MEDSL: "MEDSL 2016 totals inflated in AL, SC, AR and IN"; "8 states of the 2024 President (367 county-years) had been silently dropped (blank MEDSL vote mode)" in their build; MEDSL's 2004 county rows for Maine were 7.3% and Mississippi 3.2% below certified totals; "the FEC has not published 2024" official results (so, as of their note, no official FEC 2024 workbook). The same note says the FEC "Federal Elections" workbooks exist for 2004 to 2020.
- These claims need confirming at MEDSL and the FEC before any figure from those datasets is used. Directly relevant to the site's rule that every figure comes from a true source: MEDSL's own data is the intended primary source for county and state results, and its documented gaps matter for close-margin computations.

### Other reads, no content bearing on the directive
- `https://raw.githubusercontent.com/fivethirtyeight/data/master/README.md` (761 bytes): only notes that sports forecasts stopped being updated; no election files named. The repository tree is not listable from here.
- GitHub repository searches (19 queries, `api.github.com/search/repositories`) for pivotal vote, decisive vote, Banzhaf, voter power, tipping point, Gelman: no repository holding the target papers; the results were small hobby projects. Not read further.

---

## 3. The five parts of the directive: status and read plan

For each part: what the directive asks, what I could read, and what the next pass must capture. Titles and authors in the lists below come from the directive or from my memory and are **locators only, unverified**: a title, year or venue may be wrong until read at the source.

### 3.1 Theoretical models and formulas. **UNREAD.**
Nothing read. Sources to read, in this order:
1. Gelman, Silver and Edlin, "What is the probability your vote will make a difference?", *Economic Inquiry* (2012) (directive's citation). Capture: the definition of "decisive", the formula with its equation number, the two-stage Electoral College formula, the stated approximation, every numerical result with the election and the method. I expect a free copy on Gelman's page or as a working paper (unverified); those hosts are blocked.
2. Gelman, King and Boscardin, *JASA* (1998) (directive's citation). Capture: the model of the vote share forecast and the formula for the probability of a tie or a one-vote margin, stated assumptions.
3. Gelman, Katz and Tuerlinckx (2002), "The mathematics and statistics of voting power", and Gelman, Katz and Bafumi (2004), "Standard voting power indexes do not work" (the directive names the two without confirming titles). Capture: the Banzhaf/Penrose square-root formula as written, the critique, and what the authors say replaces it.
4. Beck (1975), Good and Mayer (1975), Chamberlain and Rothschild (1981) (directive's citations). Capture: the binomial model formula; the statement of the 1/N result when the vote share is uncertain, and the exponential result when it is known. **Premise from the directive, unverified by me:** "p shrinks like 1/N when the vote share is uncertain but exponentially when it is known."
5. Others I recall that the next pass should check exist and read if free: Mulligan and Hunter (2003, *Public Choice*) on the empirical frequency of pivotal votes; Edlin, Gelman and Kaplan (2007, *Rationality and Society*) on why voting can be rational when others' well-being counts; Banzhaf (1965 and 1968) and Penrose (1946) for the original power indices; Riker and Ordeshook (1968); Ferejohn and Fiorina (1974); Myerson on Poisson games; Gelman's blog posts. [from memory, locators only]
6. **Directive's standard approximation, unverified by me:** "p ≈ density of the vote-share forecast at 50% divided by the number of voters." To be confirmed in source 1 or 2, with its exact notation and its assumptions.

### 3.2 Two-stage structures. **UNREAD.**
The Electoral College structure (probability the vote flips the state times probability the state flips the college) is the directive's statement; the exact formula, and whether the sources treat the House majority, Senate control or parliamentary systems, is unread. Part of the answer should be in Gelman, Silver and Edlin (2012). `STATE.md` says a sibling subagent writes `research/electoral-systems.md`; compare when both are in.

### 3.3 Published numerical estimates of p for real elections. **Only one published index read, and it is a relative index (S1).**
- Read: the 2016 FiveThirtyEight Voter Power Index by state (S1, appendix A), definition unread.
- Not read: any published *probability* of decisiveness for 2008, 2012, 2016, 2020 or 2024; any state, local or foreign estimate; 538's indices for other years; The Economist's voter-power figures if any (S2 shows none in the repository README). Where to find them: Gelman, Silver and Edlin (2012) (which elections it covers, and its numbers, are unread); 538's and The Economist's election pages and the Wayback Machine copies; Gelman's blog.
- Nothing here may be quoted as a number for the site until read at its source.

### 3.4 Simple, explainable forms and the inputs they need. **UNREAD as to sources; inputs can be named from the directive.**
The directive names the inputs: number of voters, expected margin, forecast uncertainty. I have no source that states a simple form, so I offer none. What the next pass should capture: which simplified formulas the authors themselves give (for example a closed-form for a normal forecast), the stated conditions under which each is valid, and any numerical example the authors give that a lay visual could reproduce, so every number on the site traces to a page.

### 3.5 Where the input data comes from. **Partly read, all secondary.**
- Forecast inputs (mean and standard deviation of the state vote share): the Economist repository README gives them for 2008, 2012, 2016 under CC BY 4.0 (S2, appendix B), subject to the column definitions being confirmed in their code. 538's archived forecasts: unread.
- Results data: MIT Election Data and Science Lab, county presidential returns 2000 to 2024, `countypres_2000-2024.tab` on Harvard Dataverse, said by a third party to be CC0 (S5); I could not reach Dataverse (blocked) and so have not read the licence, the codebook, or the data. MEDSL's GitHub repository for 2020 precinct data is deprecated in favour of Dataverse (S4, stated by MEDSL itself).
- Dave Leip's Atlas (`uselectionatlas.org`): not probed; a third party says it does not use Leip data (S5). Access and licence unread.
- State election offices: a third party reports terms vary and some restrict reuse (S5). Official federal results: the FEC "Federal Elections" workbooks exist for 2004 to 2020 per the same third party; unread at the FEC.
- Historical results (President 1868 to 2020, Senate 1908 to 2020): Algara and Amlani on Dataverse, CC0 per the third party; unread.

---

## 4. Summary

I could not read the papers. Outbound access from this session is limited to GitHub's raw-file host; 43 scholarly, news, archive and data hosts returned a policy refusal from the egress proxy, so the formulas of Beck, Good and Mayer, Chamberlain and Rothschild, Banzhaf and Penrose, Gelman and co-authors, and every published numerical estimate of the probability of decisiveness are unread and are not given here. What the session could reach and I read: a BuzzFeed News scrape of FiveThirtyEight's 2016 state "Voter Power Index" (a relative, one-decimal index: NH 5.6, NV 4.9, NM 4.7, MI 3.1, CO 3.1, AK 3.1, PA 2.7, NC 2.7, FL 2.5, VA 2.3, IA 1.0, "<0.1" (printed as 0.0 in the scrape) in 24 of its 56 rows, including CA, NY and TX; 538's definition unread); The Economist's open model repository, whose README tabulates per-state forecast means, intervals, win probabilities and standard errors for 2008, 2012 and 2016 (a usable forecast-input source under CC BY 4.0, column definitions to be confirmed); a hobby app showing that "electoral votes per person" is a different quantity from decisiveness; and a third party's account that MEDSL county presidential returns 2000 to 2024 and the Algara and Amlani historical returns are CC0 on Harvard Dataverse, with documented MEDSL defects. The remedy is one settings change by the maker (section 1.3's host list) followed by a second pass using section 3 as its checklist.

## 5. Open questions where the sources disagree
No two sources I read disagree about decisiveness, because none states a decisiveness model. Points to settle once the sources are open:
1. What 538's "Voter Power Index" is (baseline, unit, and how "tippingpointroi" was computed). BuzzFeed uses it as a per-voter weight (S1); the page's own definition is unread.
2. What the Economist README's `mean`, `low`, `high`, `prob`, `se` columns are (S2); my reading is inferred only.
3. Whether the "p shrinks as 1/N when the share is uncertain, exponentially when known" premise (directive) and the "density at 50% over N" approximation (directive) are stated that way in the papers, and what Gelman and co-authors report as the failure of the square-root (Penrose/Banzhaf) model.
4. Whether MEDSL's known defects (S5, third party) are acknowledged by MEDSL, and whether its 2024 presidential file is complete.

## 6. Unread sources (with reason)
All of the following are **unread: blocked by the session's network policy (403 at the proxy), or not reachable by name without a listing**, except where noted.
- Gelman, King, Boscardin (1998, JASA); Gelman, Katz, Tuerlinckx (2002); Gelman, Katz, Bafumi (2004); Gelman, Silver, Edlin (2012, *Economic Inquiry*), and the NBER or Columbia working-paper copies.
- Beck (1975); Good and Mayer (1975); Chamberlain and Rothschild (1981); Mulligan and Hunter (2003); Edlin, Gelman, Kaplan (2007); Banzhaf (1965, 1968); Penrose (1946); Riker and Ordeshook (1968); Ferejohn and Fiorina (1974); Myerson (Poisson games). Paywalled or on blocked hosts.
- FiveThirtyEight's own pages for 2008, 2012, 2016, 2020 voter-power and tipping-point figures, and their archived copies (`projects.fivethirtyeight.com`, `web.archive.org`: blocked). The Economist's forecast pages (`projects.economist.com`, `www.economist.com`: blocked) and "how this works" page.
- The Economist repository's R and Stan scripts (path from the README returned 404; the repository tree cannot be listed).
- MEDSL data and codebooks, Algara and Amlani data (Dataverse, blocked); Dave Leip's Atlas (not probed); state election offices, FEC, National Archives (Electoral College), Census Bureau voting supplement (blocked).
- Wikipedia articles on the Penrose method and Banzhaf index (blocked; secondary in any case).

---

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

