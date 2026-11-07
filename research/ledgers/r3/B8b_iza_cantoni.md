# B8b: Gibson et al. (IZA DP 5854) and Cantoni (AEJ: Applied 2020)

Reader: Sonnet 5.5, batch B8b. Network not used. Python run with `-I`. Scratch files under `SCRATCH/b8b/` (page renders) and `SCRATCH/b8b_scripts/` (arithmetic and quote checker). The repository was not touched.

## Sources read

| Source id | What it is | Size | Read in full? |
|---|---|---|---|
| `iza5854` | Gibson, Kim, Stillman & Boe-Gibson, "Time to Vote?", IZA Discussion Paper No. 5854, July 2011 (PDF metadata: Subject "IZA Discussion Paper No. 5854", created 13 July 2011). `hdr` has no request URL (only Last-Modified 22 Jul 2011), so I cannot confirm from the files that `https://docs.iza.org/dp5854.pdf` was the URL fetched; the content is DP 5854. | 26 PDF pages, 7,736 words in `text.txt` | Yes, every page of text; PDF pages 22 (Figure 1) and 23 (Table 1) also looked at as images. Tables 2-4 read from layout text (clean). |
| `cantoni` | Enrico Cantoni, "A Precinct Too Far: Turnout and Voting Costs", AEJ: Applied Economics 12(1): 61-85 (2020), plus the Online Appendix dated 11 February 2019, bound into one file downloaded from IRIS Università di Bologna. The first page says it is the final published version, not an author version (see C0). | 69 PDF pages, 22,915 words | Yes, whole text (main article PDF pp. 2-26, appendix text PDF pp. 27-41, figures PDF pp. 42-57, tables PDF pp. 58-69). Figures A2-A14 are plots whose layout text is only axis labels; I read their captions and notes, not the plotted values. PDF pages 16, 21, 42, 69 looked at as images (tables match the layout text). |

Quotes from `cantoni` keep the soft hyphens (U+00AD) and zero-width spaces (U+200B) that the PDF text layer contains inside words such as "high-minority"; they are invisible but present, so that every quote matches `text.txt` after whitespace collapse. Quotes containing a line-end hyphen are given as in the text file ("quan- tify", "frac- tion", "esti- mates"). Every `Quote:` line was machine-checked against the source text by `SCRATCH/b8b_scripts/checkquotes.py` (all found; none over 40 words).

Counts, first-pass facts only (entries G0-G13 and C0-C10): confirmed 22, corrected 3 (G7, C0, C5), unread 1 (G0b). Two further entries, X4a and X4b (how each paper summarises Brady and McNulty 2011), are third-party summaries and are also marked unread, so unread totals 3. Entries G4a, G14-G16, C11-C14, X1-X3 are fill or rule-10 entries with no first-pass claim; all are confirmed by quote.

Page conventions used in every Source line.
- Gibson: PDF pages 1-3 are cover, copyright and abstract with no printed number; printed page = PDF page - 3 from PDF p. 4 (printed p. 1) to PDF p. 26 (printed p. 23). Figure 1 is on printed p. 19 (PDF 22); Tables 1-4 on printed pp. 20-23 (PDF 23-26).
- Cantoni main article: PDF p. 1 is the repository cover sheet; printed AEJ page = PDF page + 59 (PDF 2 = printed 61, PDF 26 = printed 85).
- Cantoni Online Appendix: PDF p. 27 = appendix page 1; appendix page = PDF page - 26 (PDF 41 = appendix p. 15; Figure A1 PDF 42 = appendix p. 16; Table A12 PDF 69 = appendix p. 43).

---

## Part 1. Gibson, Kim, Stillman & Boe-Gibson (`iza5854`)

### G0 Identity, date, and "later Public Choice 2013"
- First pass said: "'Time to vote?' (IZA DP 5854, 2011; later *Public Choice* 2013)" (report line 232); URL `https://docs.iza.org/dp5854.pdf` built from memory (line 20).
- Mark: confirmed (identity, number, date); the "later Public Choice 2013" part is unread (see G0b).
- Source: iza5854; https://docs.iza.org/dp5854.pdf (as in the report; `hdr` carries no URL); title page, PDF p. 2 (unnumbered).
- Quote: "Discussion Paper No. 5854 July 2011"
- Quote: "John Gibson University of Waikato and Motu Economic Research Bonggeun Kim Seoul National University Steven Stillman University of Otago and IZA Geua Boe-Gibson University of Waikato"
- Note: the PDF is the July 2011 discussion paper, not the journal version. See G14 for the paper's own caveat that a DP is provisional.

### G0b "later Public Choice 2013"
- First pass said: "later *Public Choice* 2013" (line 232).
- Mark: unread
- Source: iza5854; https://docs.iza.org/dp5854.pdf (as in the report); the DP does not mention any later publication; the only publication statement is on the copyright page, PDF p. 2 (unnumbered).
- Quote: "A revised version may be available directly from the author."
- Note: the only publication statement in the file is that line. To settle the journal, year and whether numbers changed, someone must read the journal's own record page (not fetched by me; rule 1). From memory, unverified and not to be used: I recall the article as online-first 2013 and in a 2014 issue. If the site cites the journal version, its numbers must be re-read there, since the DP says it "may" have been revised.

### G1 New Zealand 2005 general election, NZES survey
- First pass said: "New Zealand 2005 general election, validated survey voters" (line 232).
- Mark: confirmed
- Source: iza5854; https://docs.iza.org/dp5854.pdf; Section 3 (Data), printed p. 6 (PDF p. 9).
- Quote: "In this study, we use data from the 2005 general election, for which the NZES sampled just over 3,000 respondents."
- Quote: "using self-completion postal questionnaires and telephone survey top-ups"
- Note: the survey is the New Zealand Election Study (NZES), a postal survey with telephone top-ups; it is a survey sample, not an administrative file. The respondents are people aged 18 and over.

### G2 n = 3,005 "weighted"
- First pass said: "(n = 3,005 weighted)" (line 232).
- Mark: confirmed (wording imprecise)
- Source: iza5854; https://docs.iza.org/dp5854.pdf (as in the report); footnote 11, printed p. 6 (PDF p. 9); Table 2 note, printed p. 21 (PDF p. 24); Table 1, printed p. 20 (PDF p. 23).
- Quote: "In the raw data files, there are almost 3,700 observations but with missing values for some of the covariates used in our models we have a sample of n=3,005."
- Quote: "The sample size is 3,005 and the estimates are weighted by the population sampling weights."
- Note: 3,005 is the unweighted number of observations in the estimation sample; the weights are applied to the estimates, so "3,005 weighted" is a loose phrase. Urban sub-sample n = 2,452 (Table 1: "Sample size 3,005 2,452"). The body text says "the NZES sampled just over 3,000 respondents" while footnote 11 says almost 3,700 raw observations: the paper does not reconcile the two; footnote 11 says the voting rate and average distance are the same in the full and estimation samples.

### G3 Validated voting (the dependent variable)
- First pass said: "validated survey voters" (line 232).
- Mark: confirmed
- Source: iza5854; https://docs.iza.org/dp5854.pdf (as in the report); Section 1, printed p. 2 (PDF p. 5); repeated in Section 3, printed p. 6 (PDF p. 9).
- Quote: "First, the survey data on whether each respondent voted is validated by comparing the data with the lists of votes cast that are held by the registrar of electors in each electorate."
- Quote: "Systemic overstatement of voting generates a non-random misclassification error, so when voting is the dependent variable it induces bias in all of the regression coefficients"
- Note: yes, validated against the registrar's lists of votes cast (the paper's own wording; it does not give a match rate, how unmatched respondents were treated, or the NZES response rate). Voting rate in the sample 81.5% (G4a). The paper contrasts this with surveys that "do not validate self-reports".

### G4a Voting rate in the sample
- First pass said: (not stated in the report; needed for the "seven points below the mean" in G11).
- Mark: confirmed
- Source: iza5854; https://docs.iza.org/dp5854.pdf (as in the report); Section 4.1, printed p. 8 (PDF p. 11); Table 1, printed p. 20 (PDF p. 23).
- Quote: "The voting rate was 81.5 percent in both the national sample and the urban sub-sample (all estimates use population sampling weights)."
- Quote: "Dependent variable = 1 if voted, 0 if not 0.815 0.389 0.815 0.389"
- Note: this is the survey voting rate after validation and weighting; the paper does not compare it with the official turnout.

### G4 National mean distance about 1.5 km
- First pass said: "national mean distance to the polling place about 1.5 km" (line 232).
- Mark: confirmed
- Source: iza5854; https://docs.iza.org/dp5854.pdf (as in the report); Section 4.1, printed p. 8 (PDF p. 11); Table 1, printed p. 20 (PDF p. 23).
- Quote: "The average distance by road to the nearest polling place is 1.5 kilometres, or just under one mile, while in urban areas it is one kilometre (0.6 miles)."
- Quote: "Road distance (km) to closest polling booth 1.530 2.500 1.017 1.183"
- Note: it is the road distance (Google Maps shortest road) from the population-weighted centroid of the respondent's census meshblock to the nearest polling place, not the distance to the place the person actually voted. Mean 1.530 km, s.d. 2.500 (national); urban mean 1.017, s.d. 1.183.

### G5 Mean travel time 5.1 minutes
- First pass said: "mean travel time 5.1 minutes" (line 232).
- Mark: confirmed (the text calls it the return trip)
- Source: iza5854; https://docs.iza.org/dp5854.pdf (as in the report); Table 1, printed p. 20 (PDF p. 23); Section 4.1, printed pp. 8-9 (PDF pp. 11-12).
- Quote: "Travel time (mins) to closest polling booth 5.105 6.216 3.908 3.641"
- Quote: "the average return trip by car to the nearest polling place would take just five minutes of travelling time"
- Note: Table 1 does not say whether the minutes are one-way or return; the text says "return trip". [M] arithmetic with an [I] inference: 2 x 1.530 km in 5.105 minutes is 36 km/h (one-way would be 18 km/h), which fits a return trip by car; the paper does not state a speed. The paper assumes travel "by motor vehicle" (G14).

### G6 Imputed mean wage just under NZ$28 per hour (about US$19.50)
- First pass said: "imputed mean wage just under NZ$28/hour (about US$19.50)" (line 232).
- Mark: confirmed
- Source: iza5854; https://docs.iza.org/dp5854.pdf (as in the report); Section 4.1, printed p. 9 (PDF p. 12); Table 1, printed p. 20 (PDF p. 23).
- Quote: "Using the imputed wages, which average just under $28 per hour (US$19.50 at the time of the election), this is equivalent to a time cost of $2.30 (US$1.60) nationally and $1.80 (US$1.25) in urban areas."
- Quote: "Imputed wage ($ per hour) 27.759 17.358 27.968 17.377"
- Note: the paper itself gives the US$ conversions (see G13). Table 1 mean imputed wage 27.759 (s.d. 17.358) national, 27.968 urban. The wage is imputed, not observed (G12).

### G7 Time cost about NZ$2.30 per trip (US$1.60) national; NZ$1.80 (US$1.25) urban
- First pass said: "estimated cost about NZ$2.30 per trip (US$1.60) nationally, NZ$1.80 (US$1.25) urban" (line 232); "NZ$2.30, about US$1.60 per trip, a different country and year" (line 262).
- Mark: corrected (small): "per trip" should read "per return trip"; the "NZ" prefix is the report's inference, and the US$ figures are the paper's own at the 2005 exchange rate.
- Source: iza5854; https://docs.iza.org/dp5854.pdf (as in the report); Section 4.1, printed p. 9 (PDF p. 12); Table 1, printed p. 20 (PDF p. 23).
- Quote: "this is equivalent to a time cost of $2.30 (US$1.60) nationally and $1.80 (US$1.25) in urban areas."
- Quote: "Time cost ($) of reaching polling booth 2.322 3.406 1.837 2.190"
- Correction: "per trip" → "per average return trip by car to the nearest polling place (the paper's phrase), valued at the imputed wage, in 2005 NZ dollars; US$ values at the 2005 rate as the paper gives them".
- Note: Table 1 gives the unrounded means 2.322 (s.d. 3.406) national and 1.837 (s.d. 2.190) urban. This is a mean of individual-level time x wage, not the product of the two means (see recomputation R1).

### G8 Parking and waiting excluded
- First pass said: "parking and waiting excluded" (line 232).
- Mark: confirmed
- Source: iza5854; https://docs.iza.org/dp5854.pdf (as in the report); Section 4.1, printed p. 9 (PDF p. 12); Section 1, printed p. 3 (PDF p. 6).
- Quote: "Obviously, allowing for parking (albeit, often free on Saturdays) and any waiting at the polls would increase this slightly, but there is no information to estimate these costs, unlike the time costs of travel."
- Quote: "Third, we can assume that little time is spent waiting at the polling booth due to congestion;"
- Note: the paper says it has "no information" on parking and waiting, and argues waiting is little in New Zealand (average about 600 votes per polling place in 10 hours, about 50 polling places per electorate). It does not measure them.

### G9 Effects, national sample: 0.5 points per minute, 0.8 points per $1
- First pass said: "each minute of travel time reduces turnout by 0.5 percentage points and each $1 of opportunity cost by 0.8 points (national sample...)" (line 232).
- Mark: confirmed
- Source: iza5854; https://docs.iza.org/dp5854.pdf (as in the report); Section 4.3, printed p. 10 (PDF p. 13); Table 2, printed p. 21 (PDF p. 24).
- Quote: "each minute of travelling time reduces turnout by one-half of a percentage point, and each one-dollar of opportunity cost reduces it by 0.8 percentage points."
- Quote: "Time cost ($) of reaching polling booth -0.008 (2.25)*"
- Quote: "The coefficients give the change in the probability of voting for a one-unit change in each explanatory variable."
- Note: the dollar is the paper's "$" (New Zealand dollars, see G13) of the wage-weighted travel-time cost, not a price paid. The three measures are never in one equation, so the effects are not additive: "The reason for not including distance, time and cost in the same equation is because of the high correlation between these variables". Table 2 marginal effects (probit, evaluated at the mean): distance -0.010 per km (z 2.09), time -0.005 per minute (z 2.37), cost -0.008 per $1 (z 2.25). One standard deviation of any of them: "A standard deviation increase in any of these three variables would reduce turnout by three percentage points." My check: 2.5, 3.1, 2.7 points (R2).

### G10 Effects, urban sample: 0.8 per minute, 2.0 per $1
- First pass said: "(national sample; urban: 0.8 and 2.0)" (line 232).
- Mark: confirmed
- Source: iza5854; https://docs.iza.org/dp5854.pdf (as in the report); Section 4.3, printed p. 12 (PDF p. 15); Table 4, printed p. 23 (PDF p. 26).
- Quote: "each minute of travelling time reduces turnout by 0.8 of a percentage point, and each one-dollar of opportunity cost reduces it by two percentage points."
- Quote: "Time cost ($) of reaching polling booth -0.020 (3.47)**"
- Note: urban distance effect -0.019 per km (text: "two percentage points"). The urban cost effect has p = 0.001 (text, printed p. 12).

### G11 At a $10 cost, predicted national turnout 75%, seven points below the mean
- First pass said: "At a $10 cost, predicted national turnout 75%, seven points below the mean." (line 232).
- Mark: confirmed
- Source: iza5854; https://docs.iza.org/dp5854.pdf (as in the report); Section 4.3, printed p. 12 (PDF p. 15); repeated Section 5, printed p. 15 (PDF p. 18); Figure 1, printed p. 19 (PDF p. 22).
- Quote: "For example, at an opportunity cost of $10 (two standard deviations above the national mean, and equivalent to US$7), the predicted national turnout would be just 75 percent, which is down seven percentage points from the mean."
- Quote: "In urban areas, the decline is even larger, with a predicted turnout of just 62 percent when opportunity costs are $10."
- Quote: "In these simulations all of the other variables are held at their mean, so the confidence intervals quickly expand as the simulations approach the extremes of the observed costs (Figure 1)."
- Note: the "$10" is NZ$ 10 (US$7 by the paper); it is a simulated value of the wage-weighted travel cost, not a cost anyone is reported to face. [M] "two standard deviations above the national mean" is loose: mean 2.322 + 2 x 3.406 = 9.13; $10 is 2.25 s.d. above (R2). Mean voting rate 81.5% minus 75% is 6.5, which the paper calls seven. Reading Figure 1 [I]: the national line is about 0.75 at $10; its 95% band at $10 runs from about 0.68 to about 0.82, and the urban line is about 0.62 with a band of about 0.49 to 0.82. I read these off a plot; they are approximate. The simulation holds the other variables at their means, so it is a prediction at the average person, not a population turnout.

### G12 "The full imputed wage as the value of time"
- First pass said: "The extractor said the paper uses the full imputed wage as the value of time, without stating a fraction." (line 232); "Gibson et al. charge the full imputed wage" (line 235).
- Mark: confirmed in substance (the paper states no fraction; the quoted phrase "the full imputed wage" is not in the paper)
- Source: iza5854; https://docs.iza.org/dp5854.pdf (as in the report); Section 3, printed p. 8 (PDF p. 11) and footnote 16 on the same page; Table 1, printed p. 20 (PDF p. 23).
- Quote: "we estimate a wage regression using the NZIS controlling for all variables common to both surveys and the coefficients from this regression are then used to predict hourly wage rates for all respondents in the NZES."
- Quote: "Hence, we obtain an estimated value of time for everyone, regardless of whether they are wage workers;"
- Quote: "leisure and other non-market time uses also have an implicit price that must be accounted for when studying the decision of whether to vote."
- Note: how time is valued: the predicted hourly wage (from a regression on the 2005 New Zealand Income Survey, n = 13,182 working people, using variables common to both surveys: age, gender, income brackets, employment status, industry, occupation, education, ethnicity, urbanity, region; R-squared 0.386, footnote 16) is applied to everybody, workers or not, with no discount fraction stated. The paper never writes the formula "time x wage". [M] Table 1 means are consistent with cost = travel minutes x imputed wage / 60 (R1), so fraction 1.0 is implied, but that is my reconstruction [I]. The paper's justification is that leisure and non-market time "have an implicit price"; it gives no evidence that the price equals the wage. Footnote 8 (G14) shows that for workers voting on a Saturday the employer may not deduct pay.

### G13 Currency: who gave the US$ values, and what "$" means in the effects
- First pass said: "(about US$19.50)", "(US$1.60)", "(US$1.25)", and "$1 of opportunity cost" / "$10 cost" (line 232). The task asks: did the paper give the US$ conversions, and which currency is "$" in the turnout effect?
- Mark: confirmed. The paper gives the US$ conversions itself, in its own text; the paper never writes "NZ$" anywhere, so "$" in the effects is New Zealand dollars by inference [I].
- Source: iza5854; https://docs.iza.org/dp5854.pdf (as in the report); Section 4.1, printed p. 9 (PDF p. 12); Section 4.3, printed p. 12 (PDF p. 15).
- Quote: "were used to simulate turnout probability as the opportunity cost increased from $1 to $20 (US$0.70 to US$14)."
- Quote: "(US$19.50 at the time of the election)"
- Note: the plain "$" in the text, in Table 1 ("Time cost ($)", "Imputed wage ($ per hour)") and in Tables 2-4 ("Time cost ($) of reaching polling booth") is the unmarked New Zealand dollar; US dollars are always written "US$". The household income brackets ("< $16,000", "> $59,000") in Table 1 are also plain "$". [I] The inference that plain "$" = NZ$ rests on (a) the NZ data, (b) US$ being marked every time it is meant. The paper's own conversions imply a rate of about 0.70 US$ per NZ$ (R1): 19.50/27.759 = 0.7025 and exactly 0.70 for $10 to US$7, $1 to US$0.70, $20 to US$14. The paper gives no rate and no source for the rate; "at the time of the election" means 2005. So the "NZ$" and "US$" labels in the report are right in substance, and the US$ values in the report are the paper's own, not the extractor's.

### G14 What Gibson et al. say about their own limits (task 3, caveats)
- First pass said: (not stated; fill requested).
- Mark: confirmed (each item quoted)
- Source: iza5854; https://docs.iza.org/dp5854.pdf (as in the report); page for each item below.
- Quote: "Citation of such a paper should account for its provisional character."
- Quote: "When calculating these travel times, we assume that the mode of transport is by motor vehicle."
- Quote: "the exact addresses of respondents are not included in the public use data, so as to maintain confidentiality."
- Quote: "examining a general election in a country with ample polling places per voter, weekend voting, and little road congestion,"
- Quote: "their employer cannot make deductions from the employee’s remuneration for the time taken off."
- Quote: "To implement the Pesaran non-nested test, the models in columns (1) and (3) of Table 4 were re-run, using Ordinary Least Squares (OLS)"
- Note: locations: provisional character, PDF p. 2 (unnumbered, copyright page); motor vehicle, printed p. 7 (PDF p. 10); address is a meshblock centroid, printed p. 6 (PDF p. 9; the paper says meshblocks average "just 110 residents", printed p. 7); external-validity sentence ("Given that we are examining a general election in a country with ample polling places per voter, weekend voting, and little road congestion, it is perhaps surprising that we find that small increases in the opportunity cost of time can discourage individuals from voting"), conclusion, printed pp. 15-16 (PDF pp. 18-19; the quote above is on printed p. 16, PDF p. 19, a page break and page number fall in the middle of the sentence); employer cannot deduct pay, footnote 8, printed p. 3 (PDF p. 6; it cites "Section 162 of the Electoral Act, 1993"); non-nested test, printed p. 14 (PDF p. 17). Other stated limits, all in the text: parking and waiting excluded (G8); travel assumed by car because New Zealand "has the second highest car ownership rate in the world"; voters are assumed to go to the nearest polling place from home (Election Day is always a Saturday and special votes were 6.7% of votes cast, printed p. 3, PDF p. 6); wage regression R-squared 0.386; confidence bands widen at high costs (G11). [I] My reading of the design, not the paper's words: it is a covariate-adjusted probit (16 controls; electorate fixed effects in Table 3 with "no effect at all on the magnitude"), with no instrument or natural experiment and no discussion of where people choose to live relative to polling places; the paper uses "reduces" for its coefficients but the design supports a conditional association. The paper does not claim a causal design.

### G15 Wage-weighting versus distance: what the paper tested (bears on C)
- First pass said: (not stated; fill requested).
- Mark: confirmed
- Source: iza5854; https://docs.iza.org/dp5854.pdf; Section 4.4, printed p. 14 (PDF p. 17); Tables 2 and 4, printed pp. 21 and 23 (PDF pp. 24 and 26).
- Quote: "When the distance-based model is H0 it is soundly rejected against H1, the cost-based model."
- Quote: "there is no rejection of the cost-based model in favour of the distance-based model."
- Note: the non-nested test compares road distance against wage-weighted travel time, on the urban sample only (columns (1) and (3) of Table 4, re-run as a linear probability model). It shows the wage-weighted measure fits the urban sample at least as well as distance; it does not test whether the right weight on time is 100% of the wage, nor time without wages. In the national sample (Table 2) the pseudo-R2 values are 0.061 (distance), 0.063 (time), 0.061 (cost): essentially equal. Urban (Table 4): 0.074, 0.076, 0.083. This is from the paper's tables, my reading [I].

### G16 What Gibson et al. count in C
- First pass said: "(NZ, travel only)" (line 248); "travel (Gibson et al.: NZ$2.30...)" (line 262).
- Mark: confirmed
- Source: iza5854; https://docs.iza.org/dp5854.pdf (as in the report); Section 1, printed pp. 2-3 (PDF pp. 5-6).
- Quote: "Second, voter registration is compulsory in New Zealand so variation in individual turnout is not driven by differences in voter registration, as happens in the US."
- Quote: "Thus, the cognitive costs of voting should nor vary between precincts, unlike in the United States where some voters face many more choices than others."
- Note: C in this paper = round-trip road travel time by car to the nearest polling place, valued at the imputed hourly wage. Not in C, and why: registration (compulsory in New Zealand, so not measured), information or "cognitive" costs (assumed equal across precincts because every voter has two votes; not measured), waiting and parking (no data; G8), early or postal voting (less than 7% of resident votes cast early, footnote 7). The typo "nor" is in the source.

---

## Part 2. Cantoni (`cantoni`)

### C0 Version and identity of the file
- First pass said: "*AEJ: Applied* 12(1) (author version, https://cris.unibo.it/bitstream/11585/801478/9/app.20180306_copyright.pdf [S])" (line 233).
- Mark: corrected
- Source: cantoni; https://cris.unibo.it/bitstream/11585/801478/9/app.20180306_copyright.pdf (as in the report; `hdr` has no URL, only `content-disposition: inline;filename="app.20180306_copyright.pdf"`); cover sheet, PDF p. 1.
- Quote: "This is the final published version of:"
- Quote: "Copyright American Economic Association; reproduced with permission"
- Correction: "author version" → final published version (AEA copyright, repository copy with a cover sheet), journal pages 61-85, with the Online Appendix dated 11 February 2019 appended.
- Note: page numbers for the site can therefore cite the AEJ printed pages (61-85) and the appendix page numbers given in this file. The cover sheet also says "When citing, please refer to the published version."

### C1 Nine urban municipalities in Massachusetts and Minnesota
- First pass said: "nine urban municipalities in Massachusetts and Minnesota" (line 233).
- Mark: confirmed
- Source: cantoni; https://cris.unibo.it/bitstream/11585/801478/9/app.20180306_copyright.pdf; Abstract, printed p. 61 (PDF p. 2); Introduction and footnote 1, printed p. 62 (PDF p. 3); Appendix B, appendix p. 2 (PDF p. 28).
- Quote: "In nine municipalities in Massachusetts and Minnesota, a 1 standard deviation (0.245 mile) increase in distance reduces ballots cast by 2 to 5 percent across four elections."
- Quote: "I focus on a sample of urban municipalities in Massachusetts and Minnesota because of their ready availability of extremely detailed GIS data for"
- Note: the nine are Boston, Cambridge, Fall River, Lowell, Newton, Quincy, Somerville, Brookline (eight in Massachusetts) and Minneapolis (footnote 1). "As of the 2010 census, these nine municipalities encompassed a total population of more than 1.5 million residents" (appendix p. 2).

### C2 Elections 2012, 2013, 2014, 2016
- First pass said: "elections 2012, 2013, 2014, 2016" (line 233).
- Mark: confirmed, with a coverage correction in the note
- Source: cantoni; https://cris.unibo.it/bitstream/11585/801478/9/app.20180306_copyright.pdf (as in the report); Section IV, printed p. 74 (PDF p. 15); Appendix B, appendix p. 2 (PDF p. 28).
- Quote: "I start by examining the effect on the number of ballots cast by parcel residents in the 2012 presidential, 2013 municipal, 2014 midterm, and 2016 primary elections."
- Quote: "The sample for the November 4, 2013, municipal elections only includes the cities of Boston, Fall River, Lowell, and Minneapolis."
- Quote: "the sample for the March 1, 2016, presidential primary is limited to the eight Massachusetts"
- Note: the four elections are the November 2012 presidential, November 2013 municipal (four cities only), November 2014 midterm, and the March 1, 2016 presidential primary (eight Massachusetts municipalities only, because Minnesota held caucuses and the state collected no voter-level data). So "nine municipalities, four elections" overstates coverage, and the fourth election is a primary, not a general election. The introduction (printed p. 62, PDF p. 3) says "2012, 2013, 2014, and 2016 voter records from nine municipalities" without this qualification.

### C3 Mean parcel distance 0.365 mile (s.d. 0.245)
- First pass said: "mean parcel distance 0.365 mile (s.d. 0.245)" (line 233).
- Mark: confirmed
- Source: cantoni; https://cris.unibo.it/bitstream/11585/801478/9/app.20180306_copyright.pdf (as in the report); Online Appendix C, appendix p. 5 (PDF p. 31); Figure A1, appendix p. 16 (PDF p. 42).
- Quote: "The average residential parcel has a distance of 0.365 mile to its polling place, with a standard deviation of 0.245."
- Quote: "Figure A1: Distance to the Polling Place 16 12 Parcel counts (1,000) Mean = 0.365 Std. Dev. = 0.245"
- Note: Figure A1 gives N = 262,420 parcels (the full residential parcel sample, Table 1). The same 0.245 mile is the "1 standard deviation" of the headline effect. [I] It is the total s.d. of distance, not the variation that identifies the effect: the paper's own footnote 13 gives a residual s.d. of distance after boundary fixed effects of 0.17 mile, and 0.12 mile after adding latitude-longitude terms. Distance is the straight-line (Euclidean) distance between centroids, to the assigned polling place (C11). In kilometres, 0.365 mile = 0.587 km; 0.245 mile = 0.394 km (R4). Census-block mean distance in the 2012 simulation is 0.360 mile (Table A12).

### C4 One s.d. increase reduces ballots cast by 2 to 5 percent
- First pass said: "a one-s.d. increase in distance reduces ballots cast by 2 to 5 percent" (line 233).
- Mark: confirmed (rounded; my recomputation 1.75% to 5.46%)
- Source: cantoni; https://cris.unibo.it/bitstream/11585/801478/9/app.20180306_copyright.pdf (as in the report); Abstract, printed p. 61 (PDF p. 2); Introduction, printed p. 63 (PDF p. 4); Section IV and Table 3, printed pp. 74-75 (PDF pp. 15-16); Conclusion, printed p. 83 (PDF p. 24).
- Quote: "reduces the number of ballots cast by parcel residents by 2–5 percent"
- Quote: "This compares to an average of around two ballots cast per parcel,"
- Quote: "so a ­1 standard deviation increase in distance to the polling place reduces counts of votes cast in 2012 by 4–5 percent."
- Quote: "increase in distance to the polling place reduces average turnout by approximately 2–5 percent"
- Note: this is a relative change in the count of ballots cast by residents of a parcel (mean about 1 to 2.3 ballots per parcel, Table 3), not a percentage-point change in turnout. The conclusion's "reduces average turnout by approximately 2–5 percent" is also relative (percent, not points). [M] R3 below divides each Table 3 coefficient x 0.245 by that column's mean: the 16 cells run from 1.75% (2016, matching, <0.05 mile) to 5.46% (2013, matching, <0.10 mile); 2012 alone 3.8% to 4.4% (the paper's own 4-5% uses 0.08 and 0.098 per s.d. over a mean of 2.04). So "2 to 5" is a rounding of 1.75 to 5.5.

### C5 "1 to 3 percentage points" of turnout
- First pass said: "'1 to 3 percentage points' of turnout" (in quotation marks, line 233); "a distance effect of 1 to 3 points of turnout per 0.245 mile in two states" (line 314).
- Mark: corrected (wording only: the substance is confirmed, but the report put quotation marks around words the paper does not use)
- Source: cantoni; https://cris.unibo.it/bitstream/11585/801478/9/app.20180306_copyright.pdf (as in the report); Introduction, printed p. 63 (PDF p. 4).
- Quote: "which translates to a 1­ –3 ­percentage point decrease in turnout."
- Correction: "1 to 3 percentage points" (in quotation marks) → the paper's words, "1–3 percentage point decrease in turnout" (per 1 s.d. = 0.245 mile).
- Note: the paper writes "1–3 percentage point decrease", not "1 to 3 percentage points"; the report's quotation marks should be dropped or the paper's words used. The paper does not show how 2-5 percent becomes 1-3 points. [M] consistency checks (R3): block-level Table 4 turnout coefficients x 0.245 span 0.42 to 3.55 points across its 16 cells (2012 alone 2.1 to 3.6); the Table A12 simulations imply 1.1 to 2.7 points per s.d. (R3). So 1-3 is a rounding consistent with the tables; 2012 is the top. The block coefficients in Table 4 are per mile (the text: "a 1 mile increase in distance to the polling place reduces turnout by 8.6–14.5 percentage points in the 2012 presidential", printed p. 77).

### C6 Effect about three times larger in high-minority areas in non-presidential elections
- First pass said: "the effect is about three times larger in high-minority areas in non-presidential elections" (line 233).
- Mark: confirmed (specification-dependent; see note)
- Source: cantoni; https://cris.unibo.it/bitstream/11585/801478/9/app.20180306_copyright.pdf (as in the report); Abstract, printed p. 61 (PDF p. 2); Introduction, printed p. 63 (PDF p. 4); Section V and Table 5, printed pp. 79-81 (PDF pp. 20-22).
- Quote: "During ­­non-presidential elections, effects are three times larger in ­high-minority areas than in ­low-minority areas."
- Quote: "Corresponding proportional effects in ­low-minority areas are one-third as large (i.e., 11, 6, and 5 log points) and mostly insignificant."
- Quote: "Percent minority 2.17 −0.165 0.98 −0.333 1.43 −0.269 1.45 −0.193"
- Note: the high-minority Poisson effects are -16.5, -33.3, -26.9, -19.3 log points per mile in 2012, 2013, 2014, 2016; the low-minority ones -15.9, -11, -6.4, -5 (Table 5 Panel A; "the median" split of block minority share is 0.186, footnote 20). Ratios high/low from the table: 1.04 (2012), 3.03 (2013), 4.20 (2014), 3.86 (2016) (R3), so the ratio is 3.0 in 2013 and about 4 in 2014 and 2016, and about 1 in 2012; the paper rounds to "three times" and "one-third". Within-year tests: 2013 F = 8.34, 2014 F = 13.0, 2016 F = 5.47. Other specifications are weaker [I] (my reading of the appendix tables): block-level OLS (Table A6) gives ratios 2.6, 2.5, 2.8 with p = 0.09, 0.03, 0.09; the matching specification at parcel level (Table A5) gives -0.266 versus -0.236 in 2013 (p = 0.84, no gap) and gaps in 2014 (-0.058 vs -0.261) and 2016 (-0.052 vs -0.143). The author's own caveat: the minority, income and car-availability splits are correlated and "I lack statistical power" to separate them (see C13).

### C7 The 2012 presidential election shows no minority heterogeneity
- First pass said: "the 2012 presidential election shows no minority heterogeneity" (line 233).
- Mark: confirmed
- Source: cantoni; https://cris.unibo.it/bitstream/11585/801478/9/app.20180306_copyright.pdf (as in the report); Introduction, printed p. 63 (PDF p. 4); Section V, printed pp. 80-81 (PDF pp. 21-22); Table 5, printed p. 80 (PDF p. 21).
- Quote: "while no heterogeneity emerges in the 2012 presidential election."
- Quote: "F-test (within year) 0.01 8.34 13.0 5.47"
- Quote: "p-value 0.93 0.00 0.00 0.02"
- Note: 2012: high-minority -0.165 versus low-minority -0.159; within-year F = 0.01, p = 0.93. The author's gloss: "Differential effects vanish in the higher-salience 2012 election" (printed p. 81). The OLS version (Table A4) gives -0.384 versus -0.267 with p = 0.38, also not significant.

### C8 Eliminating the distance effect would raise turnout 1.6 to 4 points
- First pass said: "eliminating the distance effect would raise turnout 1.6 to 4 points" (line 233).
- Mark: confirmed
- Source: cantoni; https://cris.unibo.it/bitstream/11585/801478/9/app.20180306_copyright.pdf (as in the report); Introduction, printed p. 64 (PDF p. 5); Conclusion, printed pp. 83-84 (PDF pp. 24-25); Table A12, appendix p. 43 (PDF p. 69).
- Quote: "policy that erased the impact of distance to the polling place would increase turnout by 1.6–4 percentage points (i.e., between 4.2 and 7.3 percent)"
- Quote: "Efficiently re-drawing precinct lines reduces distance to the polling place by 0.035 miles, on average (from its 2012 mean of 0.36 miles)."
- Quote: "The simulated turnout effects of the two policies are computed using census block point esti- mates from Table A6 times the average distances shown in columns 1 and 2 of Table A12."
- Note: Table A12 Panel A (average census block): 2012 61.2 to 65.2 (+4.0), 2013 30.0 to 32.2 (+2.2), 2014 45.0 to 47.6 (+2.6), 2016 38.4 to 40.0 (+1.6). So the 1.6 is 2016 and the 4.0 is 2012; relative gains 4.2% to 7.3% (R3). Appendix footnote 18 (appendix p. 13, PDF p. 39) states the method in the last quote: a linear extrapolation to zero distance, a policy "benchmark" that no precinct redrawing can deliver. The efficient redrawing itself lifts turnout only 0.2-0.4 points. The author warns that the redrawing setup uses fixed polling places and capacities.

### C9 "No monetisation"
- First pass said: "**No monetisation.**" (line 233).
- Mark: confirmed
- Source: cantoni; https://cris.unibo.it/bitstream/11585/801478/9/app.20180306_copyright.pdf (as in the report); Abstract, printed p. 61 (PDF p. 2); appendix footnote 6, appendix p. 3 (PDF p. 29); whole text searched for "wage", "dollar", "opportunity", "value of time", "monet", "travel time": the only dollar uses are covariates and donations.
- Quote: "Results are substantively unchanged when outcomes are defined as the corresponding dollar amounts donated by parcel residents."
- Quote: "I study the effects of voting costs—specifically, distance to polling location—using geographic discontinuities."
- Note: "wage" appears only in the title of a reference (minimum wages). The paper values neither time nor distance in money. The word "dollar" occurs for the income covariate (median household income about $71,000 in 2013 dollars) and for political donations (appendix footnote 6). There is no travel-time measure at all: the cost variable is distance in miles.

### C10 The extractor's per-0.1-mile conversion (0.4 to 1.2 points)
- First pass said: "(The extractor's per-0.1-mile conversion, 0.4 to 1.2 points, is its arithmetic and not the paper's.)" (line 233).
- Mark: confirmed (the paper does not contain it; arithmetic recomputed)
- Source: cantoni; https://cris.unibo.it/bitstream/11585/801478/9/app.20180306_copyright.pdf (as in the report); whole text searched for "0.1 mile" and "tenth": the only "0.1 mile" strings are bandwidth and distance-bin labels (0.10 mile from a boundary; 0-0.1, 0.1-0.2 mile bins); non-linearity, Appendix G, appendix p. 9 (PDF p. 35).
- Quote: "In Figure A13, the estimated effects appear to grow linearly with distance to the polling place."
- Quote: "The only possible exception is the seemingly “exponential” drop in participation going from 0.3-0.5mi to 0.5-0.75mi, which is particularly visible in census block regressions."
- Note: [M] 1 point x 0.1/0.245 = 0.41 and 3 points x 0.1/0.245 = 1.22 (R3), so "0.4 to 1.2" is right arithmetic. It assumes linearity in distance. The paper's own non-linearity result: "the estimated effects appear to grow linearly with distance to the polling place" up to 0.3-0.5 mile, then an "exponential" drop from 0.3-0.5 to 0.5-0.75 mile (appendix p. 9, PDF p. 35), and the estimates come from parcels within 0.05 or 0.10 mile of a precinct boundary, where the identifying variation is the difference in distance to the polling place across the boundary. The conversion is therefore an extrapolation of the paper's mean slope, not a paper result.

### C11 What Cantoni measures as "cost of voting", dependent variable, validation (task 3)
- First pass said: (not stated; fill requested).
- Mark: confirmed
- Source: cantoni; https://cris.unibo.it/bitstream/11585/801478/9/app.20180306_copyright.pdf (as in the report); Section II.A, printed p. 67 (PDF p. 8); Section I.B, printed p. 66 (PDF p. 7); Appendix B-C, appendix pp. 2-4 (PDF pp. 28-30); Appendix A, appendix p. 1 (PDF p. 27).
- Quote: "Distances between polygons (e.g., a parcel and a polling place) are computed as the Euclidean, straight-line distance between the polygon centroids."
- Quote: "For these reasons, I use the number of votes cast by parcel residents as my main dependent variable, rather than turnout as a percentage of registered voters."
- Quote: "This produces a perfect match for more than 96 percent of voter addresses."
- Quote: "Thus, the only legitimate way most voters had to cast their ballots was by traveling to their assigned polling places on Election Day."
- Quote: "Unfortunately, this implies that the 2012 voter lists were already purged of inactive voters who failed to vote in the 2010 and 2012 statewide elections"
- Note: cost of voting = distance to the assigned polling place, straight line between centroids (no road network, no travel time, no mode, no waiting, no parking, no money). Dependent variable = count of ballots cast by residents of each parcel, from official registered-voter lists and turnout files supplied by municipal election offices and the Minnesota Secretary of State, matched to parcels through address points (96% perfect match, the rest geocoded and checked by hand using Google StreetView). It is not a survey, so no survey validation applies; it is a count of recorded ballots, and it misses residents who are not on the file (that is why the author chose counts over turnout rates, to be robust to registration). A second dependent variable: census-block turnout = votes cast by block residents / 2010 voting-age population (Table 4), with blocks whose ballots exceed the VAP dropped. The paper treats "voting costs" as the cost of getting to the polls on Election Day; early voting did not exist in either state in 2012 and absentee required an excuse (appendix A, appendix p. 1); Minnesota dropped the excuse requirement in 2014, which the paper dates both to "June 2014" (appendix p. 2, PDF p. 28) and to "August 2014" (appendix p. 10, PDF p. 36), without reconciling the two.

### C12 Cantoni on how a vote counts (bears on B, p and D)
- First pass said: (not stated; fill requested under rule 10).
- Mark: confirmed
- Source: cantoni; https://cris.unibo.it/bitstream/11585/801478/9/app.20180306_copyright.pdf (as in the report); Introduction, printed p. 61 (PDF p. 2); Appendix E, appendix pp. 6-7 (PDF pp. 32-33).
- Quote: "However, a single vote is rarely, if ever, consequential for electoral outcomes, raising the possibility that even small changes in voting costs can have a sizable impact on voter participation."
- Quote: "Overall, I find no evidence that my estimates are spuriously driven by unobservable correlates of living close to schools or polling places"
- Note: the paper contains no calculus-of-voting formula, no B, no p, no tie rule and no "held fixed" language. It uses the inconsequentiality of one vote only as the reason small costs may matter. In the placebo appendix the author considers that people living near schools or city halls may have a "higher sense of civic duty" (a D-type taste) and finds no evidence that this drives the result.

### C13 Cantoni's own stated limits (task 3, caveats)
- First pass said: (not stated; fill requested).
- Mark: confirmed
- Source: cantoni; https://cris.unibo.it/bitstream/11585/801478/9/app.20180306_copyright.pdf (as in the report); page for each below.
- Quote: "Though large, registration effects should be taken with caution because only one out of four estimates reaches conventional levels of significance."
- Quote: "I lack statistical power to quan- tify the extent to which heterogeneous effects are due to differential sensitivities to voting costs by white versus minority, rich versus poor,"
- Quote: "Second, there may be a fixed cost associated with driving to the polls (e.g., the time necessary to find parking)."
- Quote: "Overall, I reckon my problem setup to be conservative, in the sense that it privileges realistic assumptions over the achievement of larger, but perhaps infeasible, efficiency gains."
- Quote: "I find inconclusive evidence of the short-run turnout-enhancing potential of this form of convenience voting."
- Note: locations: registration, printed p. 78 (PDF p. 19); heterogeneity cannot be split, printed p. 81 (PDF p. 22); fixed driving cost including time to find parking, appendix p. 9 (PDF p. 35; speculative explanation of a drop in turnout between 0.3-0.5 and 0.5-0.75 mile); re-precincting setup "quite restrictive" (appendix p. 12, PDF p. 38) and "conservative" (appendix p. 13, PDF p. 39); no-excuse absentee, appendix p. 11 (PDF p. 37). Other stated limits: the information and donation outcomes (Table 6) "does not disprove theories of endogenous information", printed p. 82; parcel-level counts may be sensitive to outliers and parcel population "I cannot test directly", printed p. 76; the 2012 and 2013 voter lists were obtained between November 2013 and August 2014 and already purged (C11); the Republican estimates in Massachusetts are "much noisier" (appendix p. 10). The effects are estimated on parcels within 0.05 or 0.10 mile of a precinct boundary in dense urban areas, mean distance 0.365 mile. [I] Everything is reduced form: the paper cannot say which part of the distance effect is time, effort, search or transport cost.

### C14 Cantoni on registration as an outcome of distance (bears on C)
- First pass said: (not stated; fill requested under rule 10).
- Mark: confirmed
- Source: cantoni; https://cris.unibo.it/bitstream/11585/801478/9/app.20180306_copyright.pdf (as in the report); Section I.B, printed p. 65 (PDF p. 6); Section IV.B, printed p. 78 (PDF p. 19); Table 4 Panel E, printed p. 77 (PDF p. 18).
- Quote: "Distance to the polling place may affect voter registration through two channels."
- Quote: "reduce the frac- tion of VAP registered to the November 2014 voter rolls by"
- Quote: "Distance to polling place −0.049 −0.022 −0.045 −0.032"
- Note: In Minnesota, which allows registration at the polling place, a longer distance may deter would-be Election Day registrants; in both states inactive voters are purged. Estimated effect on the registered share of the voting-age population: 2.2 to 4.9 points per mile in 2014, only one of four estimates significant (Table 4 Panel E: -0.049, -0.022, -0.045, -0.032 on a mean of about 0.82). So what the site counts in C is wider than the trip if registration status itself responds to distance; the author reports it as imprecise.

---

## Part 3. Cross-cutting entries (rule 10: fork points)

### X1 Gibson et al.: the calculus they write (whose welfare, B or pB, D)
- First pass said: (not addressed for this source; line 314 lists other sources' formulas).
- Mark: confirmed
- Source: iza5854; https://docs.iza.org/dp5854.pdf (as in the report); Section 1 and footnote 1, printed p. 1 (PDF p. 4); Section 4.1, printed p. 9 (PDF p. 12); Section 5, printed p. 15 (PDF p. 18).
- Quote: "For a rational, self-interested voter, the cost of voting normally exceeds any plausible value of expected benefits from the preferred candidate winning."
- Quote: "Thus, a person will choose to vote if the costs (C) are outweighed by the benefits (B) that flow from the preferred candidate winning, discounted by the probability of casting the deciding vote (P),"
- Quote: "and allowing for the consumption benefit (D) that results from the feeling of satisfaction in performing one’s civic duty:"
- Quote: "typical stakes in an election (in terms of the amount of compensation needed for indifference between who wins) of only a few thousand dollars (Tollison and Willett, 1973)."
- Quote: "if the B (benefits) or PB (benefits weighted by the probability that a person’s vote matters) term is indeed quite small"
- Quote: "there is an indicator for whether respondents had voted in the local government elections from the previous year, to proxy for their attitude towards the civic duty of voting."
- Quote: "This responsiveness of turnout to small costs is also suggestive that the consumption benefits of voting need not be very large in order for it to be rational for many people to vote."
- Note: the displayed inequality is "C < PB + D". Whose welfare in B: the voter's own ("rational, self-interested voter"; benefits "that flow from the preferred candidate winning"); no altruistic term. B versus pB: the paper writes PB with P "the probability of casting the deciding vote" and B discounted by it; it does not estimate P or B. Tie rule: none stated (no 1/2 factor; the words tie, pivotal and decisive do not occur except "deciding vote"). "Held fixed": the paper's only "held" is statistical (other regressors "held at their mean", G11), not causal or evidential. What D is: a "consumption benefit" from "the feeling of satisfaction in performing one's civic duty"; the empirical proxy for D is prior local-election voting (printed p. 9, PDF p. 12; the quoted sentence). Size of stakes, footnote 1 (a secondary citation, Tollison and Willett 1973; the same footnote reports Feddersen's five-million-voter example in which the benefit "must be more than eight billion times greater than the cost of voting"). The Niemi quotation is the paper quoting Niemi (1976, p. 117) in its conclusion (printed p. 15, PDF p. 18); the last quote is the authors' own inference, not a measurement of B, p or D.

### X2 Gibson et al.: pivotality varies little in New Zealand by design
- First pass said: (not addressed).
- Mark: confirmed
- Source: iza5854; https://docs.iza.org/dp5854.pdf (as in the report); Section 1, printed p. 2 (PDF p. 5), footnote 6, printed p. 3 (PDF p. 6).
- Quote: "each voter has the same weight in determining overall proportionality of parties in the Parliament, irrespective of the marginality of the"
- Note: the authors use the Mixed Member Proportional system to argue that the chance a vote matters does not vary with local marginality, so that variation in distance, not in p, drives the differences in turnout. They note one exception, a party below the 5% threshold that wins an electorate seat, which "only rarely occurs" (footnote 6). This bears on B and p only as a design remark; no p is computed.

### X3 What counts in C: side by side (rule 10)
- First pass said: "Add travel ... and any information or registration time, none of which has a US figure in what I read." (line 262).
- Mark: confirmed
- Source: iza5854 and cantoni; https://docs.iza.org/dp5854.pdf and https://cris.unibo.it/bitstream/11585/801478/9/app.20180306_copyright.pdf (as in the report); see G16, C11, C14 for pages; the quote is cantoni Section I.B, printed p. 65 (PDF p. 6).
- Quote: "Distance to the polling place may affect voter registration through two channels."
- Note: Gibson et al.: C = return car trip time x imputed wage; registration and information costs held out by the New Zealand setting; waiting and parking excluded for want of data; a worker voting on Saturday cannot have pay deducted (footnote 8). Cantoni: C = straight-line distance in miles; no time or money value; effects may include registration and purge channels; early voting absent in 2012; walking range 0.3-0.5 mile and a possible fixed driving cost (finding parking) suggested for the non-linearity. Neither paper values waiting at the polls, ballot-completion time, or information. Neither offers a US dollar figure for a person's C. Gibson's NZ$2.32 is the 2005 mean of individuals' travel times (mean 5.1 minutes) times their imputed wages.

### X4a Gibson et al.'s summary of Brady and McNulty (2011) (secondary; for whoever reads that paper)
- First pass said: Brady & McNulty: "Overall turnout decreased by a substantial 1.85 percentage points", polling-place turnout fell 3.03 points, "Both transportation and search costs caused these changes." (abstract only; report line 234).
- Mark: unread (this is a third party's summary; it is not evidence about what Brady and McNulty wrote)
- Source: iza5854; https://docs.iza.org/dp5854.pdf (as in the report); Section 2, printed p. 5 (PDF p. 8).
- Quote: "Brady and McNulty (2011) show that this increased the average distance to the nearest polling place from 0.35 to 0.50 miles,"
- Quote: "and resulted in a three percentage point decline in in- person voting in consolidated voting precincts compared to unconsolidated ones."
- Quote: "Most of this decline is attributed to search costs of finding a new polling place rather than to the transportation cost of increased distance"
- Note: consistent with the report's 3.03 points for polling-place turnout. Gibson et al. weight the decline to search costs; the abstract the report quotes says "Both transportation and search costs caused these changes." These are different statements; the report should settle it from the paper itself, not from either summary. Gibson et al. also report Los Angeles County cut polling places from 5,231 to 1,885 (same page).

### X4b Cantoni's summary of Brady and McNulty (2011) (secondary)
- First pass said: same as X4a.
- Mark: unread (a third party's summary)
- Source: cantoni; https://cris.unibo.it/bitstream/11585/801478/9/app.20180306_copyright.pdf (as in the report); Section I.C, printed p. 66 (PDF p. 7).
- Quote: "find that a 1 mile increase in distance to the polling place reduced ­in-person voting by as much as 4 percentage points"
- Note: Cantoni's wording is "as much as 4 percentage points" per mile, for in-person voting; the report has not read the body of that paper. Do not use either summary as a figure for Brady and McNulty.

---

## Recomputation (python3 -I; script `SCRATCH/b8b_scripts/calc.py`)

Task 2. No [M]-tagged derivation in report section 4.3 uses these papers' numbers (the only [M] in 4.3 is the Census 99.9% sum; section 4.6's table uses BLS wages and wait minutes from other sources). The conversions that do use them are recomputed below: the paper's own US$ conversions, the extractor's per-0.1-mile conversion, and the paper's own derived numbers.

R1. Gibson Table 1 inputs, travel time x wage / 60.
- National: 5.105 x 27.759 / 60 = 2.362 NZ$ versus Table 1 mean time cost 2.322; ratio 0.983. Urban: 3.908 x 27.968 / 60 = 1.822 versus 1.837; ratio 1.008. The means differ slightly because a mean of products is not the product of means. Fraction of wage implied: about 1.0.
- Implied speed, if Table-1 minutes are the return trip: 2 x 1.530 km / (5.105/60 h) = 36.0 km/h national; 31.2 km/h urban. If one-way: 18.0 and 15.6 km/h.
- The paper's own US$ conversions: 19.50 / 27.759 = 0.7025; 19.50 / 27.9 = 0.699; 1.60 / 2.30 = 0.696; 1.25 / 1.80 = 0.694; 7 / 10 = 0.700; 0.70 / 1 = 0.700; 14 / 20 = 0.700. So about 0.70 US$ per NZ$ in 2005. Table 1 means x 0.70: 2.322 → 1.63; 1.837 → 1.29 (the paper rounds to 1.60 and 1.25).

R2. Gibson effect sizes.
- One s.d. (marginal effect x s.d.), national: distance 0.010 x 2.500 = 2.5 points; time 0.005 x 6.216 = 3.1; cost 0.008 x 3.406 = 2.7. Paper: "three percentage points". Urban: 0.019 x 1.183 = 2.2; 0.008 x 3.641 = 2.9; 0.020 x 2.190 = 4.4.
- $10 scenario: national z = (10 - 2.322) / 3.406 = 2.25 s.d. (paper: "two standard deviations"; mean + 2 s.d. = 9.13). Linear extrapolation of the marginal effect: 0.008 x 7.678 = 6.1 points national; urban 0.020 x 8.163 = 16.3 points.
- Consistency check, my reconstruction [I]: a probit with mean probability 0.815 (z = 0.8965, density 0.2669) and marginal effect 0.008 gives beta = 0.0300 per NZ$; predicted turnout at $10 = Phi(0.8965 - 0.0300 x 7.678) = 0.747 (paper: 75%). Urban: beta = 0.0749; Phi(0.8965 - 0.0749 x 8.163) = 0.612 (paper: 62%). Starting at 0.83 (Figure 1's start) gives 0.762 and 0.621. So the paper's 75% and 62% are reproducible from Tables 1, 2 and 4 within a point or two; this is my arithmetic, not the paper's.

R3. Cantoni.
- Table 3 coefficients x 0.245 / own-column mean dependent variable, in percent, by election: 2012: 3.90, 3.82, 4.22, 4.39; 2013: 5.07, 4.46, 5.46, 3.67; 2014: 3.97, 3.23, 4.46, 3.39; 2016: 2.56, 2.52, 2.72, 1.75. Range 1.75 to 5.46. The paper's text for 2012: 0.325 x 0.245 = 0.080, 0.401 x 0.245 = 0.098; 0.080/2.04 = 3.9%, 0.098/2.04 = 4.8% ("4-5 percent").
- Table 4 coefficients x 0.245 in points: 2012: 2.77, 2.89, 2.11, 3.55; 2013: 1.52, 1.57, 0.76, 0.69; 2014: 1.76, 1.32, 1.15, 1.94; 2016: 1.10, 1.10, 0.42, 2.43. Range 0.42 to 3.55.
- Table A12 Panel A: gain from zero distance and implied slope (gain / 0.360 mile): 2012 4.0 points (6.5%), 11.1 per mile, 2.72 per s.d.; 2013 2.2 (7.3%), 6.1, 1.50; 2014 2.6 (5.8%), 7.2, 1.77; 2016 1.6 (4.2%), 4.4, 1.09. Redrawing gains 0.4, 0.2, 0.3, 0.2 points. Gap reductions: 13.3 - 11.6 = 1.7, 17.9 - 15.9 = 2.0, 12.7 - 11.2 = 1.5; shares 12.8%, 11.2%, 11.8% (paper: "between 11 and 13 percent"). Panel B 2012 check: 0.126 x 0.382 = 4.81 and 0.097 x 0.342 = 3.32 (A12: +4.8 and +3.3), confirming footnote 18's method.
- Table 5 Panel A high/low ratios: 2012 1.04; 2013 3.03; 2014 4.20; 2016 3.86. Table A6 (block OLS) ratios: 0.77, 2.56, 2.47, 2.81. exp(-0.333) - 1 = -28.3% for 33 log points per mile; per s.d. 8.2 log points.
- Per-0.1-mile conversion: 1 x 0.1 / 0.245 = 0.408; 3 x 0.1 / 0.245 = 1.224.

R4. Units and a side-by-side of the two papers' distance slopes, no choice made.
- Gibson national: 1.0 point per km = 1.61 points per mile (1 / 0.621); urban: 1.9 points per km = 3.06 per mile (national mean distance 1.53 km = 0.95 mile; urban 1.017 km = 0.63 mile).
- Cantoni block turnout: 1.7 to 14.5 points per mile (range of the four per-mile ranges quoted on printed pp. 77-78); the four-election per-mile means from A12 are 4.4 to 11.1 points per mile.
- The designs differ (cross-sectional probit on survey voters in New Zealand, versus boundary discontinuity on administrative ballot counts in US cities, mean distance 0.365 mile), so I do not combine them.

---

## Corrections table

Rows marked (C) change a first-pass statement and are counted as corrected; rows marked (R) are refinements where the first-pass statement stands and is counted as confirmed; (U) is unread.

| Old (first report) | New | Source |
|---|---|---|
| (C) Cantoni file is an "author version" (line 233) | It is the final published version (AEA copyright, repository copy), AEJ: Applied 12(1): 61-85, with the Online Appendix (11 Feb 2019) appended | cantoni PDF p. 1 |
| (C) Gibson "NZ$2.30 per trip (US$1.60)" (lines 232, 262) | per average return trip by car to the nearest polling place, 2005 NZ dollars valued at the imputed wage; the US$ figures are the paper's own at about 0.70 US$ per NZ$ (the paper writes plain "$" and "US$", never "NZ$") | iza5854 printed p. 9 (PDF p. 12); p. 12 (PDF p. 15) |
| (R) "(n = 3,005 weighted)" (line 232) | n = 3,005 unweighted observations in the estimation sample (from almost 3,700 raw); the estimates are weighted by population sampling weights | iza5854 footnote 11, printed p. 6 (PDF p. 9); Table 2 note |
| (C) Cantoni "'1 to 3 percentage points' of turnout" (in quotation marks, line 233) | the paper's words are "1–3 percentage point decrease in turnout"; the quotation marks are not verbatim | cantoni printed p. 63 (PDF p. 4) |
| (R) Cantoni "nine ... municipalities ... elections 2012, 2013, 2014, 2016" (line 233) | the 2013 sample has four cities (Boston, Fall River, Lowell, Minneapolis); the 2016 election is the 1 March 2016 presidential primary in the eight Massachusetts municipalities only | cantoni appendix p. 2 (PDF p. 28) |
| (R) Cantoni "2 to 5 percent" (line 233) | confirmed as the paper's words; my recomputation from Table 3 gives 1.75% to 5.46%; it is a relative change in ballot counts, not points | cantoni Table 3, printed p. 75 (PDF p. 16) |
| (R) Cantoni "about three times larger" (line 233) | the paper's words; the table ratios are 3.0, 4.2, 3.9 (2013, 2014, 2016) in the Poisson boundary specification only; weaker or absent in the matching and block-level specifications | cantoni Table 5, printed p. 80 (PDF p. 21); Tables A5, A6 |
| (U) "later *Public Choice* 2013" (line 232) | not in the file; unread | iza5854 |

## Unread and why

- Public Choice journal version of Gibson et al. ("later *Public Choice* 2013", line 232): the file read is the July 2011 discussion paper, which says only that a revised version "may be available"; the journal page was not fetched (rule 1). The lead should decide whether to read it, since the numbers in the journal version could differ.
- Request URLs: `hdr` for both sources records no URL, so I cannot confirm from the files that the first report's `docs.iza.org/dp5854.pdf` and `cris.unibo.it/...` addresses were the ones fetched; the contents are the intended papers.
- Cantoni Figures A2-A14: plots; I read captions and notes only. No claim of the first report depends on them.
- Gibson Figure 1: read as an image (PDF p. 22); the 0.75, 0.62 and band values in G11 are approximate readings of a plot, not printed numbers.
- Brady and McNulty (2011) itself (report line 234): not one of my sources. X4a and X4b record how Gibson et al. and Cantoni summarise it; those are third-party summaries and I mark them unread.
- Whether the plain "$" in Gibson et al. is New Zealand dollars: the paper never says "NZ$"; it is an inference from context (G13).

## Found that the first pass missed

1. Gibson et al.'s cost is a return car trip, valued at the imputed wage, and in New Zealand an employer "cannot make deductions from the employee’s remuneration for the time taken off" (footnote 8). For the site's C (rule 10: what counts): the paper's wage-weighting of time is a modelling choice with no test of the fraction; the only test (non-nested, urban sample) compares wage-weighted time with plain distance.
2. Gibson et al. hold registration (compulsory in New Zealand) and information costs ("cognitive costs") out of C by design, and say parking and waiting are excluded for want of data; so the NZ$2.32 mean is travel only, as the report said, but the paper explains why the other parts are absent.
3. Gibson et al. write the calculus as "C < PB + D" with the voter's own benefit B and a consumption benefit D for civic duty (rule 10: B as self-interested, pB, D); they estimate none of B, P or D, use prior local-election voting as a proxy for D, and give no tie rule. Their footnote 1 quotes "a few thousand dollars" of typical stakes (Tollison and Willett, secondary) and Feddersen's eight-billion ratio.
4. Both papers' headline effects are in different units: Gibson per km and per NZ$ of wage-weighted time (probit marginal effects at the mean, 81.5% base voting rate); Cantoni per mile on ballot counts (percent) and on block turnout (points). Slopes side by side (R4): Gibson 1.6 to 3.1 points per mile; Cantoni 1.7 to 14.5 points per mile for blocks (4.4 to 11.1 implied by Table A12). No choice made.
5. Cantoni's coverage is narrower than the report's "nine municipalities, four elections": 2013 has four cities and 2016 is a Massachusetts-only March presidential primary.
6. Cantoni's "per s.d." scaling uses the total s.d. of distance (0.245 mile); the variation that identifies the effect is within-boundary (residual s.d. 0.12 to 0.17 mile, appendix footnote 13). The per-0.1-mile conversion in the report is a linear extrapolation; the paper finds a sharp drop beyond 0.5 mile and suggests a fixed driving cost including time to find parking.
7. Cantoni's "three times larger" claim is not stable across his own specifications and cannot be tied to minority status alone: minority share, income and car availability are correlated (block-level correlations -0.414, 0.379, -0.473, footnote 3) and with all three interactions entered, the estimates are, in the author's words, imprecise and mostly insignificant (main text printed p. 81, PDF p. 22; Tables A8, A9).
8. Cantoni treats registration as an outcome of distance (Election Day registration in Minnesota; purging of inactive voters), imprecisely estimated, and chooses counts of ballots over turnout rates to avoid selection. This bears on whether C should include registration status (rule 10: what counts in C).
9. Secondary statements about Brady and McNulty (2011) appear in both papers; see X4a and X4b. They bear on the report's abstract-only Brady & McNulty bullet and are another author's summary, not a check of that paper.
