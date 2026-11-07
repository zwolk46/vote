# B8a: Chen et al. (smartphone wait times), Brady & McNulty (Cambridge Core page), Froomkin (Discourse.net)

Reader: Sonnet 5.5. No network used. All quotes below were copied from `SRC/<id>/text.txt`; page numbers for Chen et al. are PDF pages, which equal the printed page numbers (checked on pp. 14, 24, 32: the footer number is the PDF page index).

## Sources read

| source_id | what it is | size | read in full? |
|---|---|---|---|
| chen_haggag | arXiv 1909.00024v2 [econ.GN], 31 Oct 2020, "Racial Disparities in Voting Wait Times: Evidence from Smartphone Data", M. Keith Chen, Kareem Haggag, Devin G. Pope, Ryne Rohla (paper dated October 30, 2020). Header: `content-disposition: inline; filename="1909.00024v2.pdf"`, `last-modified: Mon, 23 Jan 2023`. | PDF 61 pages; text.txt 2,410 lines, 22,889 words (`wc`) | Text and tables of pp. 1-48 read whole, line by line (main text pp. 1-18, references pp. 19-21, Appendix A pp. 22-33, Appendix B pp. 34-47, Table C.1 p. 48). Pp. 49-61 (Tables C.2 and C.3: 435 districts and 100 counties) were filtered for any non-table line (only table headers and notes found); their cells were not read one by one. Rendered pages 14 (Table 1), 24 (Table A.1) and 32 (Table A.4) as images to check the layout text: columns match. Figures (1-4, A.1-A.8, B.1-B.4) are images; I read their captions and notes, not the plots. |
| cup_bm2011 | Cambridge Core "abs" page for Brady & McNulty, APSR 105(1) (HTML, cached render dated 2026-11-06T08:16Z) | text.txt 466 lines, 2,446 words | Yes, whole. Also grepped the raw HTML for citation meta tags, footnote arrays and any hidden full text. |
| discourse | Discourse.net post by Michael Froomkin, 2012-11-06 (WordPress HTML) | text.txt 292 lines, 1,330 words | Yes, whole (the post is lines 26-79; the rest is site furniture). I also read the raw HTML to list the post's hyperlinks (the text file drops them). |

Redirect chain for `cup_bm2011` (from `hdr`): the URL the first report cites (`.../content/view/6CB07495AFC81E3251CC01A60A10B8FB/S0003055410000596a.pdf`) answers 301, then 302 to `/core/product/6CB07495AFC81E3251CC01A60A10B8FB`, 301, 302 to `/core/journals/american-political-science-review/article/abs/turning-out-to-vote-the-costs-of-finding-and-getting-to-the-polling-place/6CB07495AFC81E3251CC01A60A10B8FB`, which returns 200 HTML. So the cited "PDF" URL is not a PDF; it lands on the abstract page.

The three sources are what they say they are; none contained instruction-like text.

---

# Part 1. Chen, Haggag, Pope & Rohla (chen_haggag)

### C1 Authors and identity of the paper
- First pass said: "Authors per the extractor: Chen, Haggag, Pope and Rohla (my query had the fourth name wrong)" (report line 226).
- Mark: confirmed
- Source: chen_haggag; https://arxiv.org/pdf/1909.00024 (hdr: canonical link; file 1909.00024v2.pdf); title page, PDF p. 1 (printed p. 1)
- Quote: "M. Keith Chen, Kareem Haggag, Devin G. Pope, and Ryne Rohla∗"
- Quote: "Racial Disparities in Voting Wait Times: Evidence from Smartphone Data"
- Note: The version read is v2 dated October 30, 2020 (arXiv stamp 31 Oct 2020). The PDF does not say whether or where it was published; the first report does not claim a journal, so nothing to check.

### C2 The year, and the election date
- First pass said: "year 2016 per the NBER Digest title only" (line 226).
- Mark: confirmed (now from the paper itself)
- Source: chen_haggag; abstract, PDF p. 1; Section 1 Data, PDF p. 5; Figure 1 notes, PDF p. 8
- Quote: "we quantify a racial disparity in voting wait times across a nationwide sample of polling places during the 2016 U.S."
- Quote: "These data cover the days between November 1st and 15th, 2016, and consist of “pings”, which record a phone’s location at a series of points in time."
- Quote: "The initial sample of smartphones that recorded at least one ping on Election Day(November 8, 2016) consisted of 5.2 million unique devices."
- Note: One election: the 2016 US general election, Tuesday November 8, 2016. Pings from Nov 1-15, 2016 are used (the other days serve as placebo days, Figure A.2 and A.8). The voters in the sample are people seen at a polling place on Election Day itself. [I] Anyone who voted early at a different place or on another day, or by mail, is not in the measure; the paper does not say this in one sentence, but the sample filters (below) are all built on Election Day pings at a polling place.

### C3 Data source (first pass named only "pings")
- First pass said: "midpoint of lower and upper bounds from pings" (line 226); no data source named.
- Mark: confirmed (new detail)
- Source: chen_haggag; Section 1 Data, PDF pp. 5-6
- Quote: "We use anonymized location data for smartphones provided by SafeGraph, a firm that aggregates location data across a number of smartphone applications"
- Quote: "The median time between pings in our sample for a given device is 48 seconds (with a mode of 5 minutes)."
- Quote: "Of the 116,990 national polling places reported in 2016 by the U.S. Election Assistance Commission, 93,658 polling places (80.1%) were identified and geocoded"
- Note: Polling-place addresses were collected from state and county authorities and geocoded (p. 6). Racial composition comes from the 2017 ACS five-year estimates at the Census block group of the polling place (p. 6; Table A.1 notes, p. 24). The quote "Pings are recorded anytime an application on a phone requests information about the phone’s location." (p. 5) means ping timing depends on app use.

### C4 Unit of observation; 154,489 people at 43,413 polling places
- First pass said: "154,489 people at 43,413 polling places" (line 226).
- Mark: confirmed (wording note)
- Source: chen_haggag; Section 2 Methods, PDF p. 9 (printed p. 9); Table 1 notes, PDF p. 14
- Quote: "our final sample consists of 154,489 individuals whom we identify as likely voters across 43,413 polling locations."
- Quote: "Unit of observation is a cellphone identifier on Election Day."
- Note: The unit is a cellphone identifier classed as a likely voter, not a verified voter; the paper's word is "likely voters". Other counts in the paper, so the lead does not mix them: regressions use N = 154,411 (Table 1, p. 14; the 78 fewer lack Census race data, [I]); Figure 2 notes say "154,495 cell phones" (p. 10); Table B.2 has 43,385 polling places (p. 45); the filters take 5.2 million devices to 1.5 million (100 m), 1.0 million (60 m), 406k (building), 307k (hourly pings), 155k (final) (Figure 1 notes, p. 8). The abstract says "hundreds of thousands of smartphone users" while the analysed sample is about 155 thousand. Table C.1 N values sum to exactly 154,489 [M: sum of the 46 rows]. 43,413 is 37.1% of the 116,990 national polling places [M].
- Note: "46 different states" (Section 1, p. 2): Table C.1 (p. 48) has 46 rows = 45 states plus DC. Absent: Alaska, Colorado, Hawaii, Oregon, Washington [M: set difference]. The paper does not say why in what I read.

### C5 How waiting time is inferred
- First pass said: "midpoint of lower and upper bounds from pings" (line 226).
- Mark: confirmed
- Source: chen_haggag; Section 2 Methods, PDF p. 7 (printed p. 7)
- Quote: "Thus, we create upper and lower bounds for the amount of time spent voting by measuring the time between the last ping before entering and the first ping after exiting a polling-place circle"
- Quote: "We use the midpoint of these bounds as our best guess of a voter’s time at a polling place"
- Note: The circle is 60 metres around the building centroid (radius chosen from Figure 1, pp. 7-8). Lower bound = first to last ping inside the circle; upper bound = last ping before entering to first ping after leaving. Worked example in the paper (p. 7): lower 14 min, upper 20 min, midpoint 17 min. Table A.1 (p. 24): mean lower bound 11.26, mean upper bound 27.00, mean midpoint 19.13. [M] (11.26 + 27.00) / 2 = 19.13. So the measurement bracket on the mean is 11 to 27 minutes, and the headline is the middle.
- Quote: "Specifically, these individuals entered and spent at least one minute within a 60-meter radius of a polling location on Election Day"
- Quote: "and spent no more than 2 hours at the polling location (to eliminate, for example, poll workers who spend all day at a polling place)."
- Note: Sample filters (pp. 2, 8-9): at least one minute in the circle on Election Day, at only one polling place that day, no visit in the weeks before/after, at least one ping inside the building outline, hourly pings for 12 hours, and not more than 2 hours (upper bound under 2 hours). The 2-hour cap and the radius move the mean a lot (see C11).

### C6 Mean 19 minutes (19.13, Table A.1)
- First pass said: "mean 19 min (19.13, Table A.1)" (line 226); reused as "19" in 4.6 table (line 259), break-even (lines 281-283) and summary (line 314).
- Mark: confirmed
- Source: chen_haggag; Table A.1, PDF p. 24 (printed p. 24); text of Sections 1 and 3, PDF pp. 2 and 9-10
- Quote: "Primary Wait Time Measure (Midpoint) 154,489 19.13 16.89 0.51 5.02 13.57 40.83 119.50"
- Quote: "We estimate that the median and average times spent at polling locations are 14 and 19 minutes, respectively, and 18% of individuals spent more than 30 minutes voting."
- Note: Columns of Table A.1 are N, Mean, SD, Min, p10, Median, p90, Max (checked on the rendered page). So mean 19.13, SD 16.89, p10 5.02, p90 40.83, max 119.50 (cap from the 2-hour filter). The Section 2 text says "average voting wait times of just over 19 minutes" (p. 9). Table 1 DepVarMean is also 19.13 (N = 154,411).
- Note: [M] 4.6 arithmetic: 19/60 × 38.00 = 12.033 → $12.03 ✓; 19/60 × 32.75 = 10.371 → $10.37 ✓. With the unrounded 19.13: $12.12 and $10.44; with the median 13.57: $8.59 at $38.00. The wage inputs ($38.00, $32.75) belong to another batch and were not checked here.

### C7 Median 14 minutes
- First pass said: "median 14 min" (line 226).
- Mark: confirmed
- Source: chen_haggag; Table A.1, PDF p. 24 (printed p. 24); Section 3, PDF p. 9 (printed p. 9; the same sentence is on p. 2)
- Quote: "The median and average times spent at polling locations are 14 and 19 minutes, respectively, and 18% of individuals spent more than 30 minutes voting."
- Note: The unrounded median of the midpoint measure is 13.57 (Table A.1, column "Median"); 14 is the paper's rounding. Medians of the bounds: lower 5.52, upper 20.30.

### C8 18% over 30 minutes
- First pass said: "18% over 30 min" (line 226).
- Mark: confirmed
- Source: chen_haggag; Table A.1, PDF p. 24 (printed p. 24); Section 2, PDF p. 9 (printed p. 9)
- Quote: "Wait Time Is Over 30min 154,489 0.18 0.38 0.00 0.00 0.00 1.00 1.00"
- Quote: "and 18% of our sample waited more than 30 minutes to vote."
- Note: The 30-minute threshold is the Presidential Commission's (p. 15): "as a general rule, no voter should have to wait more than half an hour in order to have an opportunity to vote." The 18% is a share of the midpoint measure, so it inherits the casting time (see C9).

### C9 Is "mean time at a polling place" the same as "time waiting in line"? What the paper measures, exactly
- First pass said: row label "Smartphone data, mean time at a polling place" (line 226); "Smartphone mean time at polls, 2016" (line 259); sits in the table "Measured waiting and time-at-polls" next to SPAE "waited before voting" figures (lines 215-226).
- Mark: confirmed (the first pass's label is the right one; it must not be read as a line-waiting time)
- Source: chen_haggag; Section 1 intro footnote 1, PDF pp. 2-3 (the footnote runs across the page break); Section 3, PDF p. 12
- Quote: "The time measure that we estimate in our paper is a combination of wait time in addition to the time"
- Quote: "it took to cast a ballot. We typically refer to this as just “wait time” in the paper."
- Quote: "Second, our wait time measures are a combination of waiting in line and casting a ballot, whereas the survey only asks about wait times."
- Quote: "Our wait-time estimates are, on average, slightly longer than those in the survey, which is likely a reflection of the fact that our measure includes both wait time and ballot-casting time."
- Note: Answer: No. The paper measures dwell time inside a 60-metre circle around a polling-place building, bracketed from sparse GPS pings, and calls it "wait time". By the authors' own statement it is waiting plus casting a ballot, and the authors expect it to run longer than a survey wait. Not separated anywhere in the paper. The paper's defence is a correlation with the CCES wait question: "we find incredibly strong correlations between our wait time measures and survey responses that ask only about wait times as opposed to total voting time" (fn. 1, p. 3), 0.86 at state level and 0.73 at congressional-district level (Section 3, p. 12); the CCES answer is coarse ("not at all", "less than 10 minutes", "10 to 30 minutes", "31 minutes to an hour", "more than an hour"; fn. 6, p. 12). Other things that sit inside the measure: time in a queue outside the building but inside 60 m; time walking from parking within the circle [I]; voters who gave up: "These observations might be voters who abandoned after dis-" (p. 10; hyphenated across the line in the text, so not a Quote line). [I] For the site: this number is "time at the polling place of people who voted", not "time in line" and not a cost of the whole trip (no travel, no parking outside 60 m, no registration or information time).
- Quote: "Among other important factors (e.g. barriers to registration, purges from voter rolls, travel times to polling places),"
- Note: the paper itself names those other cost items as outside its measure (p. 2).

### C10 Racial disparity, headline numbers: 5.23 minutes, 29%
- First pass said: "entirely-Black block groups waited about 5 min (5.23) longer, 29% longer" (line 226).
- Mark: confirmed (the 29% appears only in the abstract; see note)
- Source: chen_haggag; abstract, PDF p. 1; intro, PDF p. 3; Section 4 and Table 1 (Panel A, column 1), PDF pp. 14-15
- Quote: "Relative to entirely-white neighborhoods, residents of entirely-black neighborhoods waited 29% longer to vote and were 74% more likely to spend more than 30 minutes at their polling place."
- Quote: "moving from a census block group with no black residents to one that is entirely composed of black residents is associated with a 5.23 minute longer wait time."
- Quote: "We find that the average wait time in a Census block group composed entirely of black residents is approximately 5 minutes longer than average wait time in a block group that has no black residents."
- Quote: "We find that entirely black areas are 12 percentage points more likely to wait more than 30 minutes than entirely white areas, a 74% increase in that likelihood."
- Note: What the number is. It is the coefficient on "Fraction Black" (a 0-to-1 share of the Census block group of the polling place) in a regression of the voter's wait time, so it is a line extended from 0% to 100% Black; the sample is mostly far from 100%: mean fraction Black 0.11, p90 0.31, max 1.00 (Table A.1). The race is the area's, "as a proxy for its catchment area" (p. 3), not the voter's: "We use Census data to characterize the racial composition of each polling place’s corresponding Census block group (as a proxy for its catchment area)." The paper words it as an association, "is associated with". The comparator is "no black residents" in column 1 and "entirely white neighborhoods" once other races enter (column 2 onward, p. 15).
- Note: [M] I cannot reproduce 29% from printed numbers: the intercept is not printed. With mean fraction Black 0.11 and mean wait 19.13, intercept ≈ 19.13 − 5.23 × 0.11 = 18.55 and 5.23 / 18.55 = 28.2%; the abstract says 29%. Likewise 0.12 / (0.18 − 0.12 × 0.11) = 71.9% against the paper's 74% (with the coefficients rounded to two places, 74% is inside the range). Treat 29% and 74% as the authors' figures from unrounded numbers; the 5.23 and 12 percentage points are the ones with a printed table.
- Quote: "Voters from areas in the top decile spent 19% more time at their polling locations than those in the bottom decile."
- Quote: "Further, voters from the top decile were 49% more likely to spend over 30 minutes at their polling locations."
- Note: The top-versus-bottom-decile comparison (Figure 3, p. 13): the top decile is 15,439 voters at 5,262 polling places with mean 58% Black; the bottom decile is 34,420 voters at 10,319 places with mean 0% Black.

### C11 Disparity: uncertainty, and how it moves with the specification (the first pass gave none)
- First pass said: nothing on standard errors, controls or robustness (line 226 gives 5.23 and 29% only).
- Mark: confirmed (new, from Table 1 and Table A.4)
- Source: chen_haggag; Table 1, PDF p. 14 (rendered and checked); Table A.2, p. 30; Table A.4 and Figure 4 notes, pp. 17 and 32; Section 4.1, pp. 16-17
- Quote: "Robust standard errors, clustered at the polling place level, are in parentheses."
- Quote: "In column 5, we present the results within county. We find that the disparity is mitigated, but it continues to be large and statistically significant."
- Quote: "Column 4 adds state fixed effects and the coefficient on fraction black only slightly decreases"
- Note: Table 1, Panel A (dependent variable: wait time in minutes), coefficient on Fraction Black (standard error), all p < 0.01: col 1 5.23 (0.39); col 2 5.22 (0.39) [adds other races]; col 3 4.96 (0.42) [adds population, density, poverty]; col 4 4.84 (0.42) [state fixed effects]; col 5 3.27 (0.45) [county fixed effects]; Table A.2 col 6 3.10 (0.44) [adds hour-of-arrival fixed effects and Android dummy]. Panel B (share over 30 minutes): 0.12 (0.01), 0.12 (0.01), 0.11 (0.01), 0.10 (0.01), 0.07 (0.01). Fraction Hispanic in col 2: 1.15 (0.37), p < 0.01, smaller than the Black coefficient (the paper says the same, p. 3).
- Note: [M] 95% interval for 5.23, ±1.96 × 0.39: 4.47 to 5.99 minutes (Figure 4 itself plots ±1.96 robust standard errors). For the county-fixed-effects coefficient 3.27 (0.45): 2.39 to 4.15. These are sampling errors only; they do not include measurement choices.
- Note: Measurement choices move the coefficient more than sampling error does (Table A.4, p. 32): by splitting the bounds, lower bound 4.71 (0.35) to upper bound 5.75 (0.45) (Panel A); by the cap on the upper bound (Panel B), 5.78 (0.54) with the cap at 5 hours, 5.23 at 2 hours (the baseline), and 3.26 (0.23) to 3.56 (0.23) with the cap at 1 hour (RV7-RV10, which also drop stays of 2 to 4 minutes or less); by radius, 1.43 (0.39) at 10 m, 5.23 (0.39) at 60 m (baseline), 6.99 (0.48) at 100 m (Panel C). The same choices move the mean wait too (Figure 4 notes, p. 17): "Panel C varies the bounding radius around the polling station centroid from 10 meters (N = 60,821; Mean = 12.09) up to 100 meters (N = 113,797; Mean = 21.81)." and "[RV7] Upper Bound under 1 hour and over 2 minutes (N = 141,170; Mean = 15.64)" and "[RV1] Upper Bound under 5 hours (N = 159,046; Mean = 22.92)". So the 19.13 mean is a point on a range of about 12 to 23 minutes depending on radius and trimming, and 11 to 27 depending on the bounds.
- Quote: "We find that none of these alternative dates produces a positive coefficient, suggesting that our approach likely identifies a lower bound on the racial gap in wait times."
- Note: Placebo days (Figure A.8, p. 29; text p. 16). Stricter likely-voter filter (68,812 voters): coefficient 4.97 (0.53) (Table A.5, p. 33).
- Note: State by state the sign is not uniform. Table C.1 (p. 48), unadjusted state coefficients on Fraction Black run from −117.11 (Montana, s.e. 92.15, N = 307) to +35.78 (Rhode Island, s.e. 15.56); among the better-measured states, Indiana −15.93 (2.73; N = 4,286) and South Carolina −11.68 (3.03) are negative while Missouri +15.00 (2.40) and Michigan +11.48 (1.42) are positive. Empirical-Bayes adjusted, the range is −13.07 (Indiana) to +13.63 (Missouri). The paper's summary words are "persistent" and "widespread" (pp. 18, 3); read the state table before saying every state shows a gap.
- Quote: "the black-white disparity in wait times for individuals who vote at a low-volume polling location (10th percentile = 1,150 registered voters) is 3.7 minutes"
- Note: p. 42: the disparity is about 3.7 minutes at the 10th percentile of registered voters per polling place and "almost twice as large at 7 minutes" at the 90th (5,242 registered voters).

### C12 "The paper gives no dollar value of time or count of deterred voters"
- First pass said: "The paper gives **no dollar value** of time or count of deterred voters." (line 226; again "Chen et al. dollar values (the paper gives none)" line 329).
- Mark: confirmed
- Source: chen_haggag; whole text (searched: the character "$" occurs 0 times; "dollar" and "wage" 0 times; "turnout" appears only in a CCES-overreporting remark, p. 12, in reference titles, and in a hypothetical on p. 34)
- Quote: "Long wait times have large opportunity costs"
- Quote: "may lead to line abandonment by discouraged voters (Stein et al. 2019),"
- Note: These two phrases (p. 2) are the whole of what the paper says about the cost of waiting or about deterrence, each with a citation (Stewart and Ansolabehere 2015; Stein et al. 2019) and no figure. The paper estimates no effect of waiting on turnout and says its estimates are conditional on a person having voted (C13).

### C13 The paper's own caveats
- First pass said: not covered.
- Mark: confirmed (new)
- Source: chen_haggag; Section 1 Data, PDF p. 5; Section 2, p. 9; Appendix B intro, p. 34 and B.5, p. 43
- Quote: "While Chen and Pope (2019) show that the data are generally representative of the U.S. along several observable dimensions (with the exception of skewing more wealthy), they may differ on unobservables."
- Quote: "However, our goal is to estimate a property of places rather than individuals."
- Quote: "Thus, to the degree that we can not completely eliminate false positives in our voter sample, we expect our overall voter wait times to be biased upward."
- Quote: "We also would expect the noise introduced by non-voters to bias us towards not finding systematic disparities in wait times by race."
- Quote: "First, as noted in Section 3, our wait time measure may include voters who abandon the line after discovering a long wait time."
- Quote: "Second, our estimates are conditional on a voter turning out."
- Quote: "The nature of our data does not lend itself to a deep exploration of mechanism."
- Quote: "Our analysis is correlational and thus does not allow us to make conclusive statements about the exact underlying mechanism."
- Quote: "This is not to dismiss the potential issue of missing polling places or times of day."
- Note: Smartphone ownership was "approximately 77% of U.S. adults ... in 2016" (p. 5). Missing polling places: 80.1% geocoded, and "In twelve states, not all county election authorities responded to inquiries" (p. 6). On mechanism, the paper "do[es] not find conclusive evidence in favor of arrival bunching, partisan bias, early voting, or strict ID laws" and finds "suggestive evidence that the effects could be driven by fewer resources that leads to congestion especially in high-volume polling places" (Section 5, p. 18; the second phrase is also available as a Quote: "We find suggestive evidence that the effects could be driven by fewer resources that leads to congestion especially in high-volume polling places."). The authors expect upward bias in the level (false positives) and downward bias in the disparity (noise).

---

# Part 2. Brady & McNulty (2011), Cambridge Core page (cup_bm2011)

### B1 Bibliographic details
- First pass said: "*APSR* 105(1): 115-134" and title "Turning out to vote" (line 234); the batch brief gives the title "Turning Out to Vote: The Costs of Finding and Getting to the Polling Place".
- Mark: confirmed
- Source: cup_bm2011; https://www.cambridge.org/core/journals/american-political-science-review/article/abs/turning-out-to-vote-the-costs-of-finding-and-getting-to-the-polling-place/6CB07495AFC81E3251CC01A60A10B8FB (final URL of the redirect chain in hdr); page header and "Information" block (page-text lines 63-118)
- Quote: "Turning Out to Vote: The Costs of Finding and Getting to the Polling Place"
- Quote: "Volume 105 , Issue 1 , February 2011 , pp. 115 - 134"
- Quote: "Published online by Cambridge University Press: 15 March 2011"
- Note: Authors HENRY E. BRADY (UC Berkeley) and JOHN E. MCNULTY (Binghamton University). DOI https://doi.org/10.1017/S0003055410000596 (page text lines 113 and 308).

### B2 What is visible on the page and what is not
- First pass said: "(abstract only; ...)" and "Distances, counts and costs are in the paywalled body." (line 234); "Brady & McNulty (2011) body (paywall)" (line 329).
- Mark: confirmed
- Source: cup_bm2011; the whole page
- Quote: "Get access to the full version of this content by using one of the access options below."
- Quote: "Article purchase Temporarily unavailable"
- Note: Visible: (1) title, authors, affiliations and the author-note (the "*" footnote giving each author's title and postal and e-mail address); (2) the full abstract (also in the page's `citation_abstract` meta tag); (3) volume, issue, month, pages, DOI, copyright "© American Political Science Association 2011"; (4) the reference list, 50 entries (Abadie et al. 2001 through Wolfinger & Rosenstone 1980), each with only the citation text and "Google Scholar" or "CrossRef" link labels; (5) "200 Cited by" count, with the list itself loading blank. NOT visible: the body of the paper (introduction, argument, data, design, tables, figures, appendix, conclusion), any in-text footnotes (the page's embedded data shows `footnotes:[]` and `fulltextNotes:[]`, i.e. none), the data on distances, counts of voters or precincts, the costs, and the method (matching). The "footnotes" the brief mentions are the author-note only; I found no article footnotes on the page. The first report's claim "abstract only" is right; its URL (see Sources read) redirects to this abstract page and is not a PDF.
- Note: Reference list entries bearing on the calculus of voting (titles only, nothing said about what the body does with them): "Downs, Anthony. 1957. An Economic Theory of Democracy", "Riker, William H., and Ordeshook, Peter C.. 1973. An Introduction to Positive Political Theory", "Niemi, Richard G. 1976. “Costs of Voting and Nonvoting.” Public Choice 27: 115–19", "Sanders, Elizabeth. 1980. “On the Costs, Utilities and Simple Joys of Voting.”", "Aldrich, John H. 1993. “Rational Choice and Turnout.”", and "Mulligan, Casey B., and Hunter, Charles G.. 2003. “The Empirical Frequency of a Pivotal Vote.”". Verbatim: Quote below.
- Quote: "Mulligan, Casey B., and Hunter, Charles G.. 2003. “The Empirical Frequency of a Pivotal Vote.” Public Choice 116: 31–54."

### B3 The natural experiment
- First pass said: "2003 California recall election, Los Angeles County precinct consolidation" (line 234).
- Mark: confirmed
- Source: cup_bm2011; abstract (page-text line 97)
- Quote: "The consolidation of voting precincts in Los Angeles County during California's 2003 gubernatorial recall election provides a natural experiment for studying how changing polling places influences voter turnout."
- Note: The question the abstract opens with is "Could changing the locations of polling places affect the outcome of an election by increasing the costs of voting for some and decreasing them for others?"

### B4 "Overall turnout decreased by a substantial 1.85 percentage points"
- First pass said: "Overall turnout decreased by a substantial 1.85 percentage points" (line 234).
- Mark: confirmed
- Source: cup_bm2011; abstract (page-text line 97)
- Quote: "Overall turnout decreased by a substantial 1.85 percentage points: A drop in polling place turnout of 3.03 percentage points was partially offset by an increase in absentee voting of 1.18 percentage points."
- Note: [M] 3.03 − 1.18 = 1.85 ✓ (the three abstract figures are consistent). The abstract does not say who the 1.85 is a percentage of or which voters it covers (all voters in the county, or those whose polling place changed): unread, the body would say. The first pass gives the figures without that base; the site should not state the base without the body.

### B5 Polling-place turnout fell 3.03; absentee rose "about 1.18"
- First pass said: "polling-place turnout fell 3.03 points, absentee voting rose about 1.18 points" (line 234).
- Mark: confirmed (wording: the abstract gives 1.18 exactly, not "about")
- Source: cup_bm2011; abstract (page-text line 97)
- Quote: "A drop in polling place turnout of 3.03 percentage points was partially offset by an increase in absentee voting of 1.18 percentage points."
- Note: The unit is percentage points. "partially offset" is the abstract's word.

### B6 "Both transportation and search costs caused these changes."
- First pass said: quoted in 4.1 (line 212) and 4.3 (line 234) as "Both transportation and search costs caused these changes".
- Mark: confirmed
- Source: cup_bm2011; abstract (page-text line 97)
- Quote: "Both transportation and search costs caused these changes."
- Note: The abstract gives the claim, not the size of each cost or any dollar or minute value; the body is paywalled. The first pass's 4.1 sentence lists "search for the polling place" as a cost component citing this line; that is the abstract's own title ("The Costs of Finding and Getting to the Polling Place") and sentence, so it is supported.

### B7 Found in the abstract and not in the first pass
- First pass said: nothing.
- Mark: confirmed (new, abstract only)
- Source: cup_bm2011; abstract (page-text line 97)
- Quote: "those registered as Democrats were more sensitive to changes in costs than those registered as Republicans."
- Quote: "the partisan effect might be decisive in only about one in two hundred contested House elections"
- Quote: "increasing the costs of voting for some and decreasing them for others"
- Note: Bears on the fork points. (a) Cost differs by voter and group, and the response to a cost change differs by registered party (abstract). (b) "decisive ... in only about one in two hundred contested House elections" is the authors' statement about whether the polling-place effect could flip an election, not a probability that a single vote is decisive; the abstract gives no inputs. (c) The abstract says changes in cost moved turnout, so it is evidence that voters respond to cost at the margin; the size of any cost in minutes or dollars is not in the abstract. [I] Nothing here is a value for C or B.

---

# Part 3. Froomkin, Discourse.net (discourse)

### F1 Identity, date and form of the post
- First pass said: "A Discourse.net post (Michael Froomkin, 2012-11-06)" (line 236); URL https://www.discourse.net/2012/11/wasted-time-in-line-for-early-voting-cost-floridians-up-to-190-million/
- Mark: confirmed
- Source: discourse; https://www.discourse.net/2012/11/wasted-time-in-line-for-early-voting-cost-floridians-up-to-190-million/ (permalink in the page); post header (page-text lines 26-28); author block (line 90-93)
- Quote: "Wasted Time in Line for Early Voting Cost Floridians up to $190 Million"
- Quote: "Posted on November 6, 2012 by Michael Froomkin"
- Quote: "Laurie Silvers & Mitchell Rubenstein Distinguished Professor of Law"
- Note: A personal blog ("A Personal Blog by Michael Froomkin", University of Miami School of Law). The page's own metadata gives `article:published_time` 2012-11-07T00:37:44+00:00, which is the evening of November 6 in Florida [I: time zone arithmetic]. The post is openly partisan: "delays due to misfeasance or malfeasance by Rick Scott, the Governor of Florida, and the state legislature (proprietor, Republican Party, State of Florida)" and "All because Rick Scott and his gang foisted this giant ballot on us". It is not a neutral source.
- Quote: "delays due to misfeasance or malfeasance by Rick Scott, the Governor of Florida, and the state legislature (proprietor, Republican Party, State of Florida)?"

### F2 "up to $190 million"
- First pass said: puts "up to $190 million" of lost time on Florida early voting (line 236).
- Mark: confirmed
- Source: discourse; post lead and "Cost" section (page-text lines 32, 70, 72)
- Quote: "My rough estimates makes it up to $190 million worth of lost time waiting in line"
- Quote: "Cost = $94,559,833 – $189,119,665"
- Quote: "Rounding, to two significant figures (this is just the back of an envelope, remember) gives us a final cost range of $95 million to $190 million."
- Note: The headline figure is the top of a range, $95 million to $190 million; the first pass gives only the top. The range comes from the average-wait assumption alone (2 or 4 hours); the other two inputs are single values.

### F3 Inputs and formula (Froomkin's own)
- First pass said: "assuming 2-4 hour waits, 2,413,472 in-person early voters and a BLS Florida wage of $19.59" (line 236).
- Mark: confirmed
- Source: discourse; page-text lines 34-68
- Quote: "The basic shape of the calculation is pretty easy: we just have to multiply the following three numbers:"
- Quote: "Cost = V * N * A"
- Quote: "V = Value of an hour of the average Floridian adult’s time"
- Quote: "N = Number of early voters"
- Quote: "A = Average wait time"
- Quote: "According to the federal Bureau of Labor Statistics, the mean hourly wage in Florida is $19.59"
- Quote: "There were 4,469,393 early voters of whom 54% voted early in-person making 2,413,472 persons (approx) who had to wait in lines (the rest voted absentee)."
- Quote: "Cost = 19.59 * 2,413,472 * [2 to 4]"
- Note: The three inputs are V = $19.59 per hour, N = 2,413,472, A = 2 to 4 hours.

### F4 The number 2,413,472 is a derived figure, not a count
- First pass said: "2,413,472 in-person early voters" (line 236).
- Mark: confirmed (with a qualification the first pass did not give)
- Source: discourse; page-text line 56; hyperlink in the raw HTML to http://elections.gmu.edu/early_vote_2012.html on the phrase "4,469,393 early voters of whom 54% voted early in-person" (the link is not in text.txt; I read it from `raw`)
- Quote: "making 2,413,472 persons (approx) who had to wait in lines"
- Note: [M] 4,469,393 × 0.54 = 2,413,472.22 ✓. So N is the product of a total early-voter count and a 54% in-person share, labelled "(approx)"; the post's source for both is the George Mason page (unread, no network). [I] It is presumably all of Florida's in-person early voters; the post does not state the period or the county breakdown.

### F5 The wage input: "mean" in the text, "median" in a footnote
- First pass said: "a BLS Florida wage of $19.59" (line 236); "a blogger's Florida estimate" (line 235).
- Mark: confirmed (with an inconsistency in the post)
- Source: discourse; page-text lines 50 and 77 (footnote 2); hyperlink in raw HTML: http://www.bls.gov/oes/current/oes_fl.htm#00-0000 on the phrase "mean hourly wage in Florida is $19.59"
- Quote: "This $19.59 figure is the median rate."
- Note: The body says "mean hourly wage", footnote 2 says "median rate". The link points to the Bureau of Labor Statistics occupational employment (OES) page for Florida, all occupations; it was not read here, so which data year and whether $19.59 is its mean or its median is unread. [I] "00-0000" in the URL is the all-occupations row. The value is an average of all Floridian workers' hourly pay, applied to every waiting voter.

### F6 Value-of-time convention (first pass line 235 quote)
- First pass said: a blogger's Florida estimate "value[s] an hour of leisure at the same rate as work" (line 235).
- Mark: corrected (substance confirmed; the quoted wording is altered)
- Source: discourse; footnote 1 and footnote 2, page-text lines 76-77
- Quote: "But in a hypothetical perfect market, workers will value the marginal hour of leisure at the same value as the forgone wages."
- Quote: "Hence, for these purposes, we can value an hour of leisure at the same rate as work."
- Correction: "value[s] an hour of leisure at the same rate as work" → the post's words are "we can value an hour of leisure at the same rate as work."
- Quote: "I don’t know how to estimate that, or even what the sign is, so I’m going to ignore it."
- Quote: "feel free to knock off 8.7% from the estimate."
- Note: Footnote 2 (page-text line 77) says the marginal rate "is surely different?" from the $19.59, which it calls "the median rate", and that he ignores the difference (the first Quote above). Footnote 3 (line 78) offers an adjustment he does not make, for unemployed people (second Quote). [M] 8.7% off $189.1 million = $172.7 million.

### F7 The 2-to-4-hour average wait: where it comes from
- First pass said: "[I] Its 2-4 hour assumption comes from some Miami-Dade polling places" (line 236).
- Mark: confirmed (the first pass's [I] is in fact stated in the post)
- Source: discourse; "Average wait time" section, page-text lines 60-64, 79
- Quote: "This is actually the hard one."
- Quote: "I know people who voted in an hour; I know people who waited over four hours."
- Quote: "When I happened to look, data from Miami-Dade Elections showed various wait time at different polling places ranging from 20 minutes to six hours."
- Quote: "Much of the cluster was in the 2-4 hour range though, so I think we should use those as our range."
- Quote: "Yes, I’m assuming the rest of the state was the same as here."
- Note: So the 2 to 4 hours is Froomkin's reading of "much of the cluster" in Miami-Dade polling-place data he happened to look at (no link or date given for it), extended to the whole state by an explicit assumption (footnote 4), and used as the average wait for every in-person early voter. He also writes "wait times varied enormously by date, time of day, and geography". The post's range for the data he looked at is 20 minutes to six hours.

### F8 "own back-of-the-envelope estimate, not a published study"
- First pass said: it is the author's "own back-of-the-envelope estimate, not a published study" (line 236, in quotation marks).
- Mark: corrected
- Source: discourse; page-text lines 32, 46, 72
- Quote: "We won’t require precision – this is back-of-the-envelope stuff, we’re just trying to get the answer right well within an order of magnitude."
- Quote: "Please check my math — corrections welcomed."
- Correction: the phrase "own back-of-the-envelope estimate, not a published study" does not occur in the post (searched `text.txt`: "back-of-the-envelope" appears once, line 46, in the sentence quoted; "published study" and "own back" do not occur) → the post says "this is back-of-the-envelope stuff", "My rough estimates", and "this is just the back of an envelope, remember".
- Note: The substance (a rough personal estimate by the blogger) is supported; the quotation marks are not. "Not a published study" is a reasonable description of a blog post but is not his wording.

### F9 Recompute Froomkin's product from his inputs
- First pass said: no recomputation in the first report; the post's $94,559,833 to $189,119,665 and $95 to $190 million were taken from the extract.
- Mark: confirmed
- Source: discourse; page-text lines 66-72
- Quote: "Cost = $94,559,833 – $189,119,665"
- Note: [M] V × N = 19.59 × 2,413,472 = $47,279,916.48 (per hour of average wait). × 2 hours = $94,559,832.96, which the post rounds to $94,559,833 ✓. × 4 hours = $189,119,665.92; the post prints $189,119,665 (truncated, not rounded to $189,119,666: a $1 difference, immaterial). Two significant figures: $95 million and $190 million ✓. Also [M]: implied cost per in-person early voter 19.59 × 2 = $39.18 to 19.59 × 4 = $78.36; implied total hours 2,413,472 × 2 = 4,826,944 to 2,413,472 × 4 = 9,653,888. And if N is recomputed from his components (4,469,393 × 0.54 = 2,413,472.2), the product is unchanged to the dollar. The arithmetic is right; every dollar of the result rests on the 2-to-4-hour assumption (F7).

### F10 First report's [I] comparison with Pew (line 236)
- First pass said: "[I] ... far above the 20-minute early-vote average Pew found statewide in the same year" (line 236).
- Mark: unread (Pew is not one of my sources); an inconsistency inside the first report is flagged
- Source: discourse; page-text lines 62 (for what Froomkin used); the first report's own line 224 (for the Pew figures, not a source I could check)
- Quote: "When I happened to look, data from Miami-Dade Elections showed various wait time at different polling places ranging from 20 minutes to six hours."
- Note: The first report's table (line 224) gives Pew 2012 as "early voting lines averaged 20 min vs 13 min on Election Day ... Florida nearly 50 min", i.e. 20 minutes is the national early-vote average and Florida's figure was "nearly 50 min", not 20. The sentence at line 236 calls 20 minutes a "statewide" Florida figure. One of the two lines is wrong; the Pew page (a different batch) decides which. The comparison that is safe from my sources: Froomkin's 2 to 4 hours is an average he asserts for all of Florida's in-person early voters; his data covered some Miami-Dade polling places at some moment he looked.

---

## Corrections table

| Old (first pass) | New | Source |
|---|---|---|
| Froomkin "own back-of-the-envelope estimate, not a published study" (line 236, as a quotation) | Not the post's wording. The post says "this is back-of-the-envelope stuff" (line 46), "My rough estimates" (line 32), "this is just the back of an envelope, remember" (line 72). Substance right, quotation marks wrong. | discourse |
| Froomkin "value[s] an hour of leisure at the same rate as work" (line 235) | "we can value an hour of leisure at the same rate as work." (footnote 1) | discourse |
| "up to $190 million" given alone (line 236) | the post's range is $95 million to $190 million ($94,559,833 to $189,119,665); $190 million is the 4-hour end | discourse |
| "absentee voting rose about 1.18 points" (line 234) | the abstract gives 1.18 exactly (no "about") | cup_bm2011 |
| Smartphone row: "year 2016 per the NBER Digest title only" (line 226) | the paper itself says the 2016 US presidential election, Election Day November 8, 2016, pings Nov 1-15, 2016 | chen_haggag p. 1, p. 5, p. 8 |
| Line 236 [I]: "the 20-minute early-vote average Pew found statewide" | outside my sources; conflicts with the first report's own line 224 (20 min national early; Florida nearly 50 min) | first report; Pew page not mine |
| Brady & McNulty URL (line 234) | the cited `.../S0003055410000596a.pdf` URL redirects to the abstract page `.../article/abs/turning-out-to-vote-.../6CB07495AFC81E3251CC01A60A10B8FB`; it is not a PDF | cup_bm2011 hdr |

Nothing in the numeric claims about Chen et al. (19.13, 14, 18%, 154,489, 43,413, 5.23, 29%) needed correcting.

## Unread and why

- Brady & McNulty body (all of it but the abstract and references): paywalled; page shows "Article purchase Temporarily unavailable". Unread therefore: which voters the 1.85 / 3.03 / 1.18 points describe (all voters or the affected voters); distances; how many precincts were consolidated; any minutes or dollars; the method; what the body says about Mulligan & Hunter, Niemi, Sanders, Aldrich.
- Froomkin's upstream sources, not read (no network): the BLS OES Florida page (http://www.bls.gov/oes/current/oes_fl.htm#00-0000), the George Mason early-vote page (http://elections.gmu.edu/early_vote_2012.html), the Google public-data unemployment link behind "8.7%", and the Miami-Dade Elections wait-time data he refers to (no link given). So $19.59 (mean or median, which year), 4,469,393 and 54%, and 8.7% are his statements, not checked.
- Pew's 20-minute figure and its geography (first report line 236): not my source.
- Chen et al.: the cited works (Stewart & Ansolabehere 2015; Stein et al. 2019; Pettigrew 2017; Chen & Pope 2019) are unread; the plots in Figures 1-4, A.1-A.8, B.1-B.4 were not inspected (captions and notes only); cell-by-cell content of Tables C.2 and C.3 (pp. 49-61) not read.

## Found that the first pass missed

1. What the 19-minute figure is (C9). The paper's "wait time" is dwell time in a 60-metre circle around a polling-place building, bracketed from pings, and it is waiting plus casting the ballot (footnote 1, p. 2-3). The first report's labels are right, but the 4.6 table sets it beside SPAE figures that are waiting only. Fork point "what counts in C": the paper's measure is time at the polling place of people who voted, conditional on having voted ("our estimates are conditional on a voter turning out", p. 34); it excludes travel, registration and information time, which the authors list as other factors (p. 2). It excludes early voters and mail voters by construction [I].
2. The 19.13 mean is a range, not a point (C5, C11): 11.26 to 27.00 by the bounds; about 12 to 23 by radius and trimming choices (Figure 4 notes, p. 17); and the authors expect it to be biased upward by non-voters caught in the filter (p. 9).
3. The racial disparity is an extension of a line to 100% Black block groups, measured by the polling place's block group, not the voter's race, with 95% interval about 4.5 to 6.0 minutes on sampling error alone, a coefficient that falls to 3.27 within county and to 3.10 with hour-of-day controls, and a sign that differs by state (C10, C11). The 29% (abstract only) is not reproducible from printed numbers (about 28% by my arithmetic).
4. Chen et al.'s state mean for Florida in 2016 is 17.99 minutes (Table C.1, PDF p. 48: N = 7,172, unadjusted mean 17.99, adjusted 17.99). It is Election Day 2016, smartphone dwell time; Froomkin's figure is average wait for in-person early voters in 2012, asserted for the whole state. Different year and different voting mode, so not a test of his number, but it is the only Florida minutes figure in my three sources.
5. Brady & McNulty's abstract carries two items bearing on fork points the first pass did not record (B7): group differences in sensitivity to cost, and "decisive in only about one in two hundred contested House elections" (an election-level statement, not a per-vote probability).
6. Froomkin's post is a partisan blog post whose product depends wholly on an asserted 2-to-4-hour statewide average (F7), a full-wage value of time (F6), and a total (N) derived from a 54% share; his own footnotes show where he chose not to adjust (marginal wage, unemployed). The $190 million is the top of a $95 million to $190 million range. Implied cost per in-person early voter: $39.18 to $78.36 [M]. This is an aggregate cost to everyone waiting, with no benefit side and no link to any decision to vote.
7. A mean-versus-median inconsistency inside Froomkin's post ($19.59 called "mean" in the text and "median" in footnote 2) is not in the first report.
8. The Cambridge URL cited in the first report is not a PDF and redirects to the abstract page; the page shows no article footnotes.
