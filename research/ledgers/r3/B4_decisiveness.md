# B4 decisiveness papers: GKB 1998, GSE 2008 manuscript, GSE Economic Inquiry 2012, Mulligan & Hunter

Reader: Sonnet 5.5 subagent, batch B4. No network used. Python run as `python3 -I`; scratch work in `SCRATCH/b4work/` (not the repository).

## Sources read (all in full)

| source_id | what the file is | size | read |
|---|---|---|---|
| `gkb98` | Gelman, King & Boscardin, *JASA* 93(441), March 1998, "Applications and Case Studies", pp. 1-9. A scanned page-image PDF with an OCR text layer (Acrobat "Paper Capture"), two columns. | 9 pp, 7,619 words | all of `text.txt` (538 lines); page images of pp. 1, 2, 3, 5, 6, 7 viewed to check the OCR on every figure used |
| `gse2008` | Gelman, Silver & Edlin, dated "27 Oct 2008" (PDF created 28 Oct 2008), title "What is the probability your vote will make a difference?" Pages 1-6 text, 7-9 figures. | 9 pp, 2,816 words | all; figure pages 8-9 viewed |
| `gse_columbia` | The same title, typeset: running heads "ECONOMIC INQUIRY", "Vol. 50, No. 2, April 2012, 321-326", doi 10.1111/j.1465-7295.2010.00272.x. Pages 321-326. | 6 pp, 3,398 words | all; figure pages 4-5 viewed (Fig. 1 map not viewed; its caption text was read) |
| `mulligan_hunter` | NBER Working Paper 8590, November 2001, 38 PDF pages (3 front pages, 28 numbered text pages, 7 unnumbered figure pages). | 8,938 words | all of `text.txt`; Table 3 page (PDF p. 34) viewed; figure pages (histograms and line charts, PDF pp. 9-15, 20-22, 25-27) not viewed, no batch fact rests on them |

**Page conventions.** `gkb98` and `gse2008`: PDF page N = printed page N. `gse_columbia`: PDF pp. 1-6 = printed pp. 321-326. `mulligan_hunter`: the page number is printed at the TOP of each page ("Pivotal - N"); printed N = PDF N+3 for N = 2-5 (PDF 5-8; the first text page, PDF 4, is unnumbered = p. 1), and printed N = PDF N+10 for N >= 6 (PDF 16-38) because seven unnumbered figure pages sit at PDF 9-15. I give both.

**Quote note.** `gkb98` is two-column and `pdftotext -layout` interleaves the columns, so a sentence is usually broken across lines of `text.txt` with the other column's words between. Each `Quote:` line below is therefore one line-segment that is contiguous in `text.txt`; the sentence they make up is given in the Note. Every Quote line was checked by script against `text.txt` (whitespace collapsed, NFKC) and was found.

---

## A. Gelman, King & Boscardin (1998), `gkb98`

### B4-01 When a vote is decisive (Sec. 3.1)
- First pass said: l. 87: "a vote is decisive only if 'without your vote, your state's election outcome must be exactly tied or one vote away from a tie'" (p. 3).
- Mark: confirmed
- Source: gkb98; https://gking.harvard.edu/files/estimatprob.pdf; Sec. 3.1; PDF p. 3 (printed p. 3)
- Quote: "Your presidential vote will be decisive if two conditions"
- Quote: "are satisfied. First, without your vote, your state's election"
- Quote: "outcome must be exactly tied or one vote away from a tie."
- Quote: "your state must be decisive in the national election; given"
- Quote: "that it is tied, neither party must have an electoral vote ma-"
- Quote: "(We consider the case of a person who will either vote for"
- Note: The quoted words are verbatim. The paper says "will be decisive if two conditions are satisfied"; the first pass gives only the first condition. The second is that the state decides the national electoral vote ("given that it is tied, neither party must have an electoral vote majority"). The paper's sentence in reading order: "(We consider the case of a person who will either vote for one candidate or not vote. A voter who is considering switching from the Democratic to Republican candidate will, of course, have a higher probability of being decisive.)" The OCR text layer drops the word "or" ("one candidate not vote"); the page image shows "or". So GKB's counterfactual is cast-versus-abstain (the owner's counted-versus-uncounted ballot), and they say switching would be more decisive. The intro defines the event as "(equivalent to a tie in your state and in the electoral college)" (p. 1; Quote lines in B4-F1).

### B4-02 The factor of 1/2 in eq. (3)
- First pass said: l. 87: "their eq. (3) carries a factor of ½ because 'a vote that causes the national election to be tied is only half as decisive.'"; l. 271 table: "½ for ties".
- Mark: confirmed
- Source: gkb98; https://gking.harvard.edu/files/estimatprob.pdf; Sec. 3.1, eq. (3) and the parenthesis under it; PDF p. 3 (printed p. 3)
- Quote: "(The factors of 1/2 arise because a vote that causes the"
- Quote: "national election to be tied is only half as decisive as a"
- Quote: "vote that changes the election outcome.) The conditional"
- Note: Reading order: "(The factors of 1/2 arise because a vote that causes the national election to be tied is only half as decisive as a vote that changes the election outcome.)" The first pass's quote stops before "as a vote that changes the election outcome". On the page image (p. 3) eq. (3) is: Pr(your state is decisive | your vote is decisive in your state) = Pr(E_{-i} in (.5 e_total - e_i, .5 e_total) | v_i = .5) + (1/2) Pr(E_{-i} = .5 e_total - e_i | v_i = .5) + (1/2) Pr(E_{-i} = .5 e_total | v_i = .5). So the 1/2 appears twice, and weights only the two cases in which the NATIONAL electoral-vote total ends in a tie (269-269). The state-level factor, eq. (2), has no 1/2 (see B4-04). The paper does not say how a national electoral-vote tie would be resolved. Equation numbers: (1) Pr(your vote matters) = Pr(decisive in your state) x Pr(your state decisive | your vote decisive in your state); (2) the first factor; (3) the second factor; (5), p. 5, is the normal-density version of (2).

### B4-03 Two-level structure, eq. (1) ("a conditional probability")
- First pass said: l. 112: "the chance your vote is decisive in your state times 'a conditional probability' that your state is decisive nationally (eq. 1)" (p. 3).
- Mark: confirmed
- Source: gkb98; https://gking.harvard.edu/files/estimatprob.pdf; Sec. 3.1, eq. (1); PDF p. 3 (printed p. 3)
- Quote: "Pr(your vote matters)"
- Quote: "The second factor on the right side of (1) is a conditional"
- Quote: "probability: the probability that state i will be decisive,"
- Quote: "given a popular vote tie in that state."
- Note: The words "a conditional probability" are split across two lines of `text.txt` by the column interleave; on the page image they read "...is a conditional probability: the probability that state i will be decisive, given a popular vote tie in that state."

### B4-04 Eq. (2), the state-level factor
- First pass said: l. 112: the state-level factor is "roughly the density of the vote-share forecast at .5 divided by the number of voters" (eq. 2) (p. 3).
- Mark: corrected
- Source: gkb98; https://gking.harvard.edu/files/estimatprob.pdf; Sec. 3.1, eq. (2); PDF p. 3 (printed p. 3); eq. (5) PDF p. 5
- Quote: "Pr(your vote is decisive in your state)"
- Quote: "using the discrete approximation to the continuous distribu-"
- Quote: "tion and the notation fvt for the probability density func-"
- Correction: the words in quotation marks are not in the paper (no "roughly", no "divided"; searched). Substance is right. The paper's eq. (2), from the page image: Pr(your vote is decisive in your state) = Pr(n_i v_i = .5 n_i) = Pr(v_i = .5) ≈ f_{v_i}(.5)/n_i, with f the probability density of v_i under the forecasting model, v_i the Democratic share of the two-party vote in state i "(excluding your vote)", and n_i the "number of voters in state i (excluding yourself)". For odd n_i the event is Pr(n_i v_i = .5(n_i - 1)) = Pr(v_i = .5 - .5/n_i), also ≈ f(.5)/n_i.
- Note: the OCR of the equation line in `text.txt` is garbled; the equation above is read from the image.

### B4-05 "GKB's footnote 6" on recounts
- First pass said: l. 94: "GKB's footnote 6 'addresses the recount objection but doesn't change the definition' (extractor, p. 2)"; l. 302: "recounts, courts and runoffs change it (2.2; GKB fn. 6)".
- Mark: corrected
- Source: gse2008; https://www.stat.berkeley.edu/~aldous/157/Papers/vote.pdf; footnote 6, PDF p. 2 (printed p. 2). In the published version it is footnote 3, `gse_columbia` PDF p. 1 (printed p. 321).
- Quote: "An objection sometimes arises about this sort of calculation that one vote never makes a difference, because if the election were decided by one vote, there would be a recount anyway."
- Quote: "Gelman, Katz, and Bafumi (2004, p. 674) discuss why this argument is wrong, even for real elections with disputed votes, recounts, and so forth."
- Quote: "This can be shown by setting up a more elaborate model that allows for a gray area in vote counting and then demonstrating that the simpler model of decisive votes is a reasonable approximation."
- Correction: "GKB fn. 6" → there is no footnote 6, and no footnote at all, in `gkb98` (JASA 1998), and the word "recount" does not occur in it (the 9 pages were read whole; OCR text searched; page images of pp. 1, 2, 3, 5, 6, 7 show no footnote other than the authors' affiliations on p. 1). The recount footnote is footnote 6 of the Gelman, Silver & Edlin 2008 manuscript (footnote 3 of the Economic Inquiry version; the "6" matches the manuscript's numbering, where notes 1-3 are author affiliations). Its content is not "doesn't change the definition": it says the recount objection "is wrong" and that the simple decisive-vote model is "a reasonable approximation" of a model with a gray area in counting. It points to Gelman, Katz & Bafumi (2004, p. 674), which is unread.
- Note: M&H, not GKB, discuss recounts at length (B4-M10, B4-M11). The first pass's "extractor, p. 2" matches the GSE manuscript's p. 2, so the extractor evidently mixed two papers.

### B4-06 "about 1 in 10 million for all states", 1992
- First pass said: l. 139 and l. 271: 1992 "about 1 in 10 million for all states" (pp. 5-6).
- Mark: confirmed
- Source: gkb98; https://gking.harvard.edu/files/estimatprob.pdf; Sec. 4.3; PDF p. 5 (printed p. 5)
- Quote: "The probability is about 1 in 10 million"
- Quote: "for all states. Voters in some of the smaller politically mod-"
- Quote: "about 1 in 10 million for close national elections such as 1992, varying by about a factor of 10 among states."
- Note: the third quote is the abstract (p. 1), which is a more careful statement than "for all states": the next sentences on p. 5 give Vermont 1 in 3.5 million and say Utah and Nebraska "have a lesser chance". Sec. 6.1 (p. 6): "typically of order of magnitude 1 in 10 million". The 1 in 10 million is for the 1992 election (Fig. 2a), forecast made with information available before November 1992 (p. 4, Sec. 4.1) and a model fit to 1948-1988 data. Six of the nine elections 1952-1988 (excluding 1968) also give "near 1 in 10 million" (p. 5).

### B4-07 "about 1 in 1.5 million for some small states in some close elections"
- First pass said: l. 139: "about 1 in 1.5 million for some small states in some close elections" (pp. 5-6).
- Mark: confirmed
- Source: gkb98; https://gking.harvard.edu/files/estimatprob.pdf; Sec. 6.1; PDF p. 6 (printed p. 6)
- Quote: "Like all other researchers, we estimate the (prospective)"
- Quote: "in 1.5 million for some small states in some close elections"
- Quote: "(e.g., Nevada in 1960 and Alaska in 1976)"
- Note: reading order: "...typically of order of magnitude 1 in 10 million, rising to as much as about 1 in 1.5 million for some small states in some close elections (e.g., Nevada in 1960 and Alaska in 1976) and less than 1 in 100 million for all states in landslide elections such as 1972." The first pass's quoted words are verbatim; the paper adds the two examples and the landslide clause.

### B4-08 Vermont "1 in 3.5 million"
- First pass said: l. 271: Vermont "1 in 3.5 million" (pp. 5-6).
- Mark: confirmed
- Source: gkb98; https://gking.harvard.edu/files/estimatprob.pdf; Sec. 4.3; PDF p. 5 (printed p. 5)
- Quote: "(e.g., 1 in 3.5 million in"
- Quote: "Vermont), whereas those in more extreme states (e.g., Utah"
- Note: reading order: "Voters in some of the smaller politically moderate states have a greater chance (e.g., 1 in 3.5 million in Vermont), whereas those in more extreme states (e.g., Utah and Nebraska) have a lesser chance."

### B4-09 Landslides "on the order of 1 in hundreds of millions"
- First pass said: l. 271: landslides "on the order of 1 in hundreds of millions" (pp. 5-6).
- Mark: confirmed
- Source: gkb98; https://gking.harvard.edu/files/estimatprob.pdf; Sec. 4.3; PDF p. 5 (printed p. 5)
- Quote: "three elections (1964, 1972, and 1984, corresponding to"
- Quote: "the landslide victories of Johnson, Nixon, and Reagan), the"
- Quote: "probability is much smaller, on the order of 1 in hundreds"
- Quote: "of millions for all of the states."
- Quote: "model; we trust the qualitative findings, but would rely less"
- Quote: "strongly on the exact numerical results."
- Note: the paper itself says it would "rely less strongly on the exact numerical results" for the landslide years (sensitivity to the tail of the forecasting model). Sec. 6.1 (p. 6) gives a different looser form for 1972: "less than 1 in 100 million for all states".

### B4-10 Popular-vote tie "approximately 1 in 13.3 million"
- First pass said: l. 271: popular-vote "approximately 1 in 13.3 million" (pp. 5-6).
- Mark: confirmed
- Source: gkb98; https://gking.harvard.edu/files/estimatprob.pdf; Sec. 4.3; PDF p. 5 (printed p. 5)
- Quote: "normal with mean 51.5% and standard deviation 5.6%. With"
- Quote: "about 92 million people predicted to vote, the chance that it"
- Quote: "would have been an exact tie is approximately 1 in 13.3 mil-"
- Note: this is "the chance that a single vote would be decisive if the popular vote decided the election", computed as the probability of an EXACT tie (the paper's words "an exact tie"), not tie-or-one-short and with no 1/2. [M] Recomputed from the paper's inputs: z = (.5 - .515)/.056 = -0.2679; normal density at .5 = exp(-z²/2)/(sqrt(2π)·.056) = 0.9648/2.5066/.056 = 6.873; divided by 92,000,000 = 7.47×10⁻⁸ = 1 in 13.39 million. The paper's 13.3 million matches within the rounding of the mean (51.5%) and s.d. (5.6%). This also checks eq. (2): density at .5 divided by n.

### B4-11 "varying by about a factor of 10 among states"
- First pass said: l. 271: varying "by about a factor of 10 among states" (cited to pp. 5-6).
- Mark: confirmed (location corrected)
- Source: gkb98; https://gking.harvard.edu/files/estimatprob.pdf; abstract; PDF p. 1 (printed p. 1)
- Quote: "about 1 in 10 million for close national elections such as 1992, varying by about a factor of 10 among states."
- Note: the sentence is in the abstract, p. 1, not on pp. 5-6. It describes "close national elections such as 1992", not all years. Also in the abstract: "we estimate the (prospective) probability of a single vote being decisive as".

### B4-12 State-level error s.d. about 3.5%
- First pass said: l. 271: "state-level error s.d. about 3.5% (p. 5)".
- Mark: confirmed
- Source: gkb98; https://gking.harvard.edu/files/estimatprob.pdf; Sec. 4.1 (end); PDF p. 5 (printed p. 5), top of left column
- Quote: "estimated standard deviations of about 2.5%, 2.5%, 5.0%, and 3.5%"
- Quote: "The regression coefficients and the variances of the error"
- Quote: "terms are estimated using data from the 1948 through 1988"
- Note: reading order: "estimated standard deviations of about 2.5%, 2.5%, 5.0%, and 3.5%, for the national, regional (outside the South), regional (the South), and state-level error terms." So 3.5% is the state-level error term; the others are national 2.5%, regional (non-South) 2.5%, regional (South) 5.0%. Fitted with state variance proportional to n^(-θ) (θ 95% interval [.09, .36]), so 3.5% is a typical-state value, not a constant.

### B4-13 "does not compute the expected utility of voting or a benefit-cost ratio"
- First pass said: l. 271: B for GKB is "none (the paper 'does not compute the expected utility of voting or a benefit-cost ratio')".
- Mark: corrected
- Source: gkb98; https://gking.harvard.edu/files/estimatprob.pdf; whole paper; the only mention of expected utility is Sec. 6.3, PDF p. 8 (printed p. 8)
- Quote: "Decision theorists have long noted the need for estimat-"
- Quote: "ing subjective probabilities for expected utility calculations"
- Correction: the sentence in quotation marks is not in the paper (searched; the only "expected utility" is the phrase above). Substance holds: the paper estimates only the probability and puts no value on B or on any cost. It says "The exact value of this probability is of only minor interest" (abstract, p. 1).

### B4-14 [I] "consistent with GKB's ½" (the first pass's tie algebra)
- First pass said: l. 93 and l. 314: p ≡ ½[P(tie among others) + P(A one behind)], "consistent with GKB's ½ and Barnett's ½" / "matching Gelman et al.'s and Barnett's ½".
- Mark: corrected
- Source: gkb98; https://gking.harvard.edu/files/estimatprob.pdf; Sec. 3.1, eqs. (2) and (3); PDF p. 3
- Quote: "outcome must be exactly tied or one vote away from a tie."
- Quote: "(The factors of 1/2 arise because a vote that causes the"
- Quote: "national election to be tied is only half as decisive as a"
- Correction: GKB's 1/2 is on the NATIONAL electoral-vote tie only (B4-02). At the state level, where the first pass's algebra lives, GKB give "exactly tied or one vote away from a tie" a single probability f(.5)/n_i, with no 1/2 (eq. 2). So the first pass's p is half of GKB's state-level quantity, and "GKB's 1/2" is a different 1/2 from the one in the algebra. See "Found" item 2 for the arithmetic and for GSE and M&H.

---

## B. Gelman, Silver & Edlin, 2008 manuscript, `gse2008` (each fact also checked in `gse_columbia`; see section D)

### B4-20 The formula: P(state necessary) x P(state tied | necessary)
- First pass said: l. 113: `P(state pivotal in the Electoral College) × P(state tied | pivotal)` (pp. 1, 3); l. 272 table.
- Mark: confirmed
- Source: gse2008; https://www.stat.berkeley.edu/~aldous/157/Papers/vote.pdf; abstract and Introduction; PDF p. 1 (printed p. 1)
- Quote: "the probability that your vote is decisive is equal to the probability that your state is necessary for an electoral college win, times the probability the vote in your state is tied in that event."
- Note: the paper's word is "necessary", not "pivotal". Same sentence in `gse_columbia`, PDF p. 1 (printed p. 321). The product is stated again on p. 4 of the manuscript: "The product of two probabilities above gives the probability of a decisive vote in the state."

### B4-21 10,000 simulations and "half credit for exact ties"
- First pass said: l. 113: "pivotality is the share of 10,000 simulations where the margin from all other states is less than the state's electoral votes, with half credit for exact ties" (pp. 1, 3).
- Mark: confirmed
- Source: gse2008; https://www.stat.berkeley.edu/~aldous/157/Papers/vote.pdf; Method, step 1; PDF p. 3 (printed p. 3)
- Quote: "The result of our forecasts is a 10,000 x 51 matrix representing 10,000 computer simulations of the election"
- Quote: "these are necessary for an electoral college win by computing the proportion of the"
- Quote: "than E, plus ½ the proportion of simulations for which the margin based on all other states equals E."
- Quote: "(This last part assumes implicitly that we have no idea who would win in the event of an electoral vote tie.)"
- Note: "half credit" is the first pass's phrase, not the paper's (the paper says "plus ½ the proportion"). The ½ is on the ELECTORAL-VOTE tie only, and the paper gives its rationale: no idea who wins such a tie. Published: `gse_columbia` PDF p. 2 (printed p. 322): "1/2 the proportion of simulations for which the" / "last part assumes implicitly that we have no idea" / "who would win in the event of an electoral vote".

### B4-22 Student-t with 4 d.f.
- First pass said: l. 113 and l. 272: tie density from a Student-t with 4 d.f. (pp. 1, 3).
- Mark: confirmed
- Source: gse2008; https://www.stat.berkeley.edu/~aldous/157/Papers/vote.pdf; Method, step 2; PDF p. 3 (printed p. 3)
- Quote: "compute the probability of an exact tie as the density at 0 of the Student-t distribution with 4 degrees of freedom, mean M, and scale S."
- Note: the state factor is "the probability of an exact tie" computed as the density at 0 of the vote margin (the margin in votes; the example "-.208 in Alabama" is Obama share minus McCain share, times turnout, p. 3). No 1/2 and no "one vote short" term is mentioned at the state level. See "Found" item 2 [I].

### B4-23 "1 in 10 million" in the best states
- First pass said: l. 139 and l. 272: best 2008 states "1 in 10 million".
- Mark: confirmed
- Source: gse2008; https://www.stat.berkeley.edu/~aldous/157/Papers/vote.pdf; abstract, PDF p. 1; summary, PDF p. 4 (printed pp. 1, 4)
- Quote: "most likely to matter are New Mexico, Virginia, New Hampshire, and Colorado, where your vote has an approximate 1 in 10 million chance of determining the national election outcome."
- Quote: "In summary, we estimate the probability of a single vote being decisive as, at most, about 1 in 10"
- Quote: "million in a few states near the national median."
- Note: the figure is the paper's own rounding ("approximate", "at most, about"). Published: same, `gse_columbia` PDF p. 1.

### B4-24 "1 in 60 million" for the average voter
- First pass said: l. 139 and l. 272: average voter 1 in 60 million (turnout-weighted).
- Mark: confirmed
- Source: gse2008; https://www.stat.berkeley.edu/~aldous/157/Papers/vote.pdf; abstract PDF p. 1; summary PDF p. 4 (printed pp. 1, 4)
- Quote: "On average, a voter in America has a 1 in 60 million chance of being decisive in the presidential election."
- Quote: "Averaging these probabilities over all the states and weighting by turnout yields a 1 in 60 million chance that a randomly-selected voter will be decisive."
- Note: published: "On average, a voter in America had a 1 in 60 million chance..." (`gse_columbia` PDF p. 1) and "weighting by turnout yields a 1 / in 60 million chance that a randomly selected" (PDF pp. 3-4).

### B4-25 New York, California, Texas "closer to 1 in a billion"
- First pass said: l. 139 and l. 272: NY, CA, TX "closer to 1 in a billion".
- Mark: confirmed
- Source: gse2008; https://www.stat.berkeley.edu/~aldous/157/Papers/vote.pdf; Discussion; PDF p. 4 (printed p. 4)
- Quote: "Texas where the probability of a decisive vote is closer to 1 in a billion, any reasons for voting must go beyond the any instrumental rationality.)"
- Quote: "we estimate there is a 18% chance that the electoral vote margin will be less than 55"
- Quote: "only a 1 in 100 million chance that California’s immense popular vote will be tied if that happens."
- Note: a parenthetical, loosely stated. [M] The paper's own California numbers on p. 4 give 0.18 × 10⁻⁸ = 1.8×10⁻⁹ = about 1 in 556 million, so "closer to 1 in a billion" is rounding up; the figure shows CA, NY, TX and IL near the "1 in a billion" line (Fig. 3, p. 9). The first report uses exactly 10⁻⁹ in its break-even row; the paper's own p. 4 numbers give about 1.8×10⁻⁹ for CA, and it gives no number for NY or TX. The manuscript prints "the any instrumental rationality"; the published version has "any instrumental rationality" (D1).

### B4-26 Footnote 11 values (manuscript numbering)
- First pass said: l. 272: "DC and Utah values in fn. 11 (5e-85 to 2e-12 and 9e-16 to 2e-10)".
- Mark: confirmed
- Source: gse2008; https://www.stat.berkeley.edu/~aldous/157/Papers/vote.pdf; footnote 11, starts at the foot of PDF p. 3 and ends at the foot of p. 4 (printed pp. 3-4). Published: footnote 8, `gse_columbia` PDF p. 3 (printed p. 323)
- Quote: "changing the estimated probability of decisiveness in the District of Columbia from 5e-85 to 2e-12, in Utah from 9e-16 to 2e-10, but changing the estimate in Ohio only from 3.4e-8 to 3.1e-8."
- Note: the direction is normal → Student-t (reading order: "Using the t instead of the normal has little effect on the probability of a decisive vote in close states, but it moderates the results in states farther from the national median, for example..."). The footnote also gives Ohio 3.4e-8 → 3.1e-8, which the first pass omits. Footnote number: 11 in the manuscript, 8 in the published version. Published text, same values: `gse_columbia` "Columbia from 5e-85 to 2e-12, in Utah from 9e-16 to 2e-10, but changing" / "the estimate in Ohio only from 3.4e-8 to 3.1e-8."

### B4-27 "like a lottery ticket" and the payoff
- First pass said: l. 272: a vote is "like a lottery ticket with a 1 in 10 million chance of winning"; benefit framed as the chance "to change national policy and improve (one hopes) the lives of hundreds of millions" (p. 4).
- Mark: confirmed
- Source: gse2008; https://www.stat.berkeley.edu/~aldous/157/Papers/vote.pdf; Discussion; PDF p. 4 (printed p. 4). Published: `gse_columbia` PDF p. 4 (printed p. 324), footnote 9 attached.
- Quote: "a vote is like a lottery ticket with a 1 in 10 million chance of winning, but the payoff is the chance to change national policy"
- Quote: "and improve (one hopes) the lives of hundreds of millions, compared to the alternative if the other candidate were to win."
- Note: the sentence begins "A probability of 1 in 10 million is tiny but, as discussed by Edlin, Gelman, and Kaplan (2007), can provide a rational reason for voting; in this perspective, a vote is..." (B4-F2 for what this says on B).

### B4-28 2008 election only
- First pass said: l. 272: "2008 presidential election only."
- Mark: confirmed
- Source: gse2008; https://www.stat.berkeley.edu/~aldous/157/Papers/vote.pdf; abstract PDF p. 1; Method PDF p. 2 (printed pp. 1-2)
- Quote: "We compute these probabilities for each state in the 2008 presidential election, using state-by-state election forecasts based on the latest polls."
- Quote: "We use a state-by-state election forecast computed on 24 October 2008"
- Note: published abstract: "We computed these probabilities a week before the 2008 presidential election". The paper estimates no other year.

### B4-29 "Gelman et al. leave B qualitative"
- First pass said: l. 279: "Gelman et al. leave B qualitative."
- Mark: confirmed
- Source: gse2008; https://www.stat.berkeley.edu/~aldous/157/Papers/vote.pdf; Discussion; PDF p. 4 (printed p. 4)
- Quote: "Different voters have different opinions about which candidate is desirable, but many can feel that their preference is not only better for them personally but for millions of others."
- Note: no dollar or utility value for B appears in either GSE version. For GKB the same holds (B4-13). The published version adds footnote 9 about dollar-equivalent benefits (B4-D1).

### B4-30 Is `gse_columbia` the Economic Inquiry article, and is the first pass's "unconfirmed" resolved?
- First pass said: l. 272: "the extractor could not confirm *Economic Inquiry* 50(2): 321-326, 2012, from the manuscript, and that attribution rests on a search-result title"; l. 330, l. 335: Economic Inquiry version unread.
- Mark: confirmed
- Source: gse_columbia; https://sites.stat.columbia.edu/gelman/research/published/probdecisive2.pdf; header of the first page, PDF p. 1 (printed p. 321)
- Quote: "Economic Inquiry"
- Quote: "Vol. 50, No. 2, April 2012, 321–326"
- Quote: "Online Early publication March 19, 2010"
- Quote: "doi:10.1111/j.1465-7295.2010.00272.x"
- Quote: "© 2010 Western Economic Association International"
- Note: the six PDF pages are printed pp. 321-326 with running heads "322 ECONOMIC INQUIRY" and "GELMAN, SILVER & EDLIN: WHAT IS THE PROBABILITY YOUR VOTE WILL MAKE A DIFFERENCE?", the star footnote "We thank an anonymous reviewer for helpful comments" (so post-review), a JEL code, and a typeset reference list; so this is the journal-typeset published article (Online Early March 2010; issue April 2012). Its hdr shows `Last-Modified: Tue, 14 Aug 2012` on Gelman's Columbia site; PDF metadata: title in capitals, created 1 Feb 2012, producer "PDFlib PLOP ... Acrobat Distiller". I cannot tell from the file whether it is the Wiley version of record or a typeset copy the author hosts; [I] it is the same typesetting. It differs from `gse2008` in no numerical result; every difference is listed in B4-D1.

---

## C. Mulligan & Hunter, `mulligan_hunter` (NBER WP 8590, November 2001)

### B4-M01 The publication citation (Public Choice 116: 31-54, 2003)
- First pass said: l. 273 heading: "Mulligan & Hunter (2003) *Public Choice* 116: 31-54"; l. 330/335: not discussed.
- Mark: confirmed (citation, via GSE); the M&H text itself says nothing about publication
- Source: gse2008; https://www.stat.berkeley.edu/~aldous/157/Papers/vote.pdf; reference list; PDF p. 6 (printed p. 6). Also `gse_columbia` PDF p. 6 (printed p. 326): "Mulligan, C. B., and C. G. Hunter. “The Empirical Fre-" / "quency of a Pivotal Vote.” Public Choice, 116, 2003," / "31–54."
- Quote: "Mulligan, C. B., and Hunter, C. G. (2003). The empirical frequency of a pivotal vote. Public Choice 116, 31-54."
- Note: the file I read is NBER Working Paper No. 8590, "November 2001", JEL D72, 38 PDF pages. Its text never says "Public Choice" for its own publication (the only "Public Choice" strings are other authors' references: Beck, Fischer, Margolis). It says an earlier version exists: "earlier version, Mulligan and Hunter (2000)", reference "Harris School Working Paper 00.25, October 2000." So the publication facts rest on the GSE reference lists only, and every M&H number below is the WORKING PAPER's, which may differ from the 2003 article's. [I] GSE describe M&H as using "such a model", an empirical analysis "embedded into a regression of vote differential on election-level predictors"; the working paper's estimator is the q(M)/p(M) averaging of near-tie counts (the analogue of GSE's y/(2000n)), with a fixed-effects regression only in footnote 12. The journal version may be different.

### B4-M01b What the M&H file itself is
- First pass said: l. 273: "Mulligan & Hunter (2003) *Public Choice* 116: 31-54"; URL https://www.nber.org/papers/w8590.pdf.
- Mark: corrected (a qualification: the file is the working paper, not the article)
- Source: mulligan_hunter; https://www.nber.org/papers/w8590.pdf (redirects to https://www.nber.org/system/files/working_papers/w8590/w8590.pdf, per hdr); cover and abstract pages, PDF pp. 1-2; reference list, PDF p. 38 (printed p. 28)
- Quote: "NBER Working Paper No. 8590 November 2001"
- Quote: "earlier version, Mulligan and Hunter (2000)."
- Quote: "Harris School Working Paper 00.25, October 2000."
- Correction: old → new: "Mulligan & Hunter (2003), *Public Choice* 116: 31-54" as the thing read → the text read is NBER Working Paper 8590 (November 2001; PDF metadata title "empirdecpc.wpd", created 28 Aug 2001), itself a revision of a Harris School working paper of October 2000. Its text does not mention *Public Choice* for itself. The journal article's text was not read (see "Unread").

### B4-M02 16,577 House elections, 1898-1992; one decided by a single vote
- First pass said: l. 273: "16,577 US House elections 1898-1992: one decided by a single vote".
- Mark: confirmed
- Source: mulligan_hunter; https://www.nber.org/papers/w8590.pdf (redirects to https://www.nber.org/system/files/working_papers/w8590/w8590.pdf); Sec. I and Table 1, PDF pp. 5, 7 (printed pp. 2, 4); Sec. II.C, PDF p. 16 (printed p. 6)
- Quote: "of Representatives for the election years 1898-1992 (hereafter"
- Quote: "leaving 16577 US returns for analysis."
- Quote: "years 1898-1992 (even)"
- Quote: "Of the 16577 US returns analyzed, only one (1/16577=0.00006) was decided by a single"
- Note: 16,577 are CONTESTED House elections in even years: 839 "exceptions file" elections and 3,228 more (missing, zero or uncontested) were dropped (p. 2, quote "elections where a minority candidate won, or a Democrat was not opposed by a Republican, or a Republican was"). Footnote 5: the one election is NY's 36th district, 1910, "the Democratic candidate winning 20685-20684". The paper's own Table 3 (B4-M10) records a later count of 20690-20684 for it. Reading order of the first quote: "Of the 16577 US returns analyzed, only one (1/16577=0.00006) was decided by a single vote."

### B4-M03 40,036 state legislative elections, 1968-89; two ties, seven single-vote
- First pass said: l. 273: "40,036 state legislative elections 1968-89: two ties, seven single-vote".
- Mark: confirmed
- Source: mulligan_hunter; https://www.nber.org/papers/w8590.pdf; Sec. I, PDF p. 5 (printed p. 2); Table 1, PDF p. 7 (printed p. 4); Sec. II.C, PDF p. 17 (printed p. 7)
- Quote: "state legislative election returns in the United States for the years 1968-89 (hereafter"
- Quote: "This leaves 40,036 elections included in the analysis."
- Quote: "Of the 40036 STATE elections (with almost one billion votes) analyzed, two were tied and seven were decided by a single vote (9/40036=0.0002)."
- Quote: "years 1898-1992 (even) 1968-1989"
- Note: contested general elections, single- and multi-member districts, except multi-member free-for-all districts (p. 2). Table 1: average total votes 111,370 (US) and 23,658 (STATE); "elections 16,577 40,036". 16,577 + 40,036 = 56,613 = the paper's "56,613 elections".

### B4-M04 Definition of a "pivotal vote" (Sec. II.B)
- First pass said: l. 89: a "pivotal vote" is a vote for the winner in an election the winner won "by no more than one vote", or a vote for either candidate in a tied election (Sec. II.B, p. 5).
- Mark: confirmed
- Source: mulligan_hunter; https://www.nber.org/papers/w8590.pdf; Sec. II.B; PDF p. 8 (printed p. 5)
- Quote: "vote total exceeded the loser’s official and final vote total by no more than one vote."
- Quote: "is a vote cast for the winner in a pivot election, or cast for either candidate in a tied"
- Quote: "election. In other words, a “pivotal vote” is one for which it appears an election outcome would"
- Quote: "have been different if it had been cast differently."
- Note: reading order: "To begin, we refer to a “pivot election” as one in which the winner’s official and final vote total exceeded the loser’s official and final vote total by no more than one vote. A “pivotal vote” is a vote cast for the winner in a pivot election, or cast for either candidate in a tied election. In other words, a “pivotal vote” is one for which it appears an election outcome would have been different if it had been cast differently." Two details the first pass leaves out: the definition is on "official and final" totals (the paper later shows that "final" is doubtful, B4-M10), and it says "cast differently" without saying whether that means abstaining or switching to the other candidate (GKB state the abstain-versus-switch difference, B4-01).

### B4-M05 Weight 1 or 1/2 for a one-vote margin
- First pass said: l. 89 and l. 291: M&H count a single-vote-margin vote as fully pivotal, "**without** a ½ weight".
- Mark: confirmed
- Source: mulligan_hunter; https://www.nber.org/papers/w8590.pdf; Sec. II.B PDF p. 8 (printed p. 5); Sec. II.C PDF p. 17 (printed p. 7); Sec. III.A PDF p. 30 (printed p. 20)
- Quote: "is a vote cast for the winner in a pivot election, or cast for either candidate in a tied"
- Quote: "cast,7 and that the probability of a tied election is half of that.8 Then two estimates of the"
- Quote: "The probability of a pivotal vote is just (3) because only half of the votes in a pivot election with odd total votes are pivotal."
- Note: the answer is WEIGHT 1. Each vote for the winner in a one-vote election counts as one pivotal vote, and in a tie each vote for either candidate does. No 1/2 is applied to a tie or a one-vote margin as a weight. The "half"s that do appear are not weights on decisiveness: (a) a parity count, footnote 8: with an even number of voters there is one way to tie but two ways to differ by two, so "the probability of a tied election is half of that" of a margin of any other small even value (the estimator then multiplies by 3/2 "to get 0 or 1"); (b) in a one-vote election only half the ballots (the winner's) are pivotal, so P(pivotal vote) = f(½)/(v+1), the same as P(tie | v even) (Sec. III.A). The paper defines no tie rule (coin, runoff) at all; its only treatment of a recount rule is B4-M11.

### B4-M06 "about 1 in 100,000" and "1 in 15,000" (abstract)
- First pass said: l. 273: "about 1 in 100,000 votes (House), about 1 in 15,000 (state legislature...)"; l. 285-286 break-even rows.
- Mark: confirmed
- Source: mulligan_hunter; https://www.nber.org/papers/w8590.pdf; abstract, PDF p. 2 (unnumbered page)
- Quote: "showing that one of every 100,000 votes cast in U.S. elections, and one of every 15,000"
- Quote: "in the sense that they were cast for a candidate that officially tied or won by one vote."
- Note: the words are the paper's. "U.S. elections" means the House file only. But the two figures are NOT on the same basis; see B4-R2. In short: 1 in 100,000 comes from 0.00001, the share of votes that "mattered" (winner's votes only, footnote 6); 1 in 15,000 is the share of ALL votes cast in the nine pivot STATE elections (the loser's votes included), unrounded 6.47×10⁻⁵ = 1 in 15,444. On the paper's own definition the STATE share is about 1 in 25,500 [M].

### B4-M07 The body's "0.00006"
- First pass said: l. 273: "the body's 0.00006 is about 1 in 16,700".
- Mark: confirmed
- Source: mulligan_hunter; https://www.nber.org/papers/w8590.pdf; Sec. II.C; PDF p. 17 (printed p. 7)
- Quote: "61,328 votes were cast in those nine elections, or a 0.00006 share of all of the votes in the STATE elections analyzed."
- Quote: "the losing candidate, so we are left with a 0.00001 share of all of the votes in U.S. elections"
- Note: [M] 1/0.00006 = 16,667, so "about 1 in 16,700" is correct arithmetic. The 0.00006 is the STATE vote share (all votes in the nine pivot elections). Do not confuse with another 0.00006 on p. 6: "(1/16577=0.00006)", the US per-election frequency (one election in 16,577); that 1 in 16,577 is a coincidental near-match to "1 in 16,700" and is a different quantity (elections, not votes; US, not state). Footnote 6 (PDF p. 16, ends at the foot of p. 17): "Of course, 20684 of those votes “did not matter” in the sense that they were cast for the losing candidate, so we are left with a 0.00001 share ... that mattered." The state 0.00006 has no such adjustment in the text.

### B4-M08 "Very close elections are more rare than the independent binomial model predicts"
- First pass said: l. 140, l. 273, l. 298: M&H find very close elections "more rare than the independent binomial model predicts" (abstract); "historical frequency, with the binomial over-predicting".
- Mark: confirmed
- Source: mulligan_hunter; https://www.nber.org/papers/w8590.pdf; abstract, PDF p. 2 (unnumbered); Sec. III.A, PDF p. 30 (printed p. 20); Sec. V, PDF p. 36 (printed p. 26)
- Quote: "or won by one vote. Very close elections are more rare than the independent binomial model predicts."
- Quote: "However, there are two senses in which the binomial model overpredicts the frequency of a pivotal vote."
- Quote: "Third, 2/v seems to be somewhat less than a reasonably"
- Quote: "calibrated binomial model would predict"
- Note: three qualifications the first pass omits. (1) "Somewhat less": the conclusion says the observed 2/v (v the total votes in the election) "is closely approximated by 2/v, which is broadly consistent with a binomial model" (Sec. V), and that f(½) ≈ 2 "seems sensible". (2) The paper's "independent binomial" model integrates a prior over the success probability A (their eqs. 2-4, f(½) = the density at A = ½); the same-model with A fixed gives astronomically small numbers: footnote 14 quotes "A = .61 (roughly the averages for the US sample), (1) yields an estimated" / "probability of a pivot election of 10-1108" (read as 10^-1108; the exponent is a superscript lost in the text) "Compare 10-1108 to my US sample frequency of 0.00005." So the fixed-A binomial (the source of figures like Carling's 10^-90) is not what M&H say over-predicts. (3) The two senses are: independence (they "suspect that the effective number of voters is less than the actual number") and a dip in the margin density at 0-4 votes versus 20-24 votes (Fig. 2c, 2d; Sec. IV.B), which they trace to margin-specific counting procedures.
- Quote: "we suspect that the effective number of voters is less than the actual number of voters v, so that (4) overpredicts the frequency of a"
- Quote: "probability of a pivot election of 10-1108 (here I follow Margolis 1977 and others in the liteture"

### B4-M09 The "average, historical, not forward-looking" characterization
- First pass said: l. 291: "The Mulligan-Hunter p is an average over all votes cast in those elections (a historical frequency), not a forward-looking probability for a given voter".
- Mark: confirmed (with the paper's own bridge to a subjective probability)
- Source: mulligan_hunter; https://www.nber.org/papers/w8590.pdf; Sec. II.B (end); PDF p. 16 (printed p. 6)
- Quote: "Pivot elections are interesting because those are the elections in which, at least with perfect foresight, a vote indeed had instrumental value."
- Quote: "Of course, a voter typically does not know the precise election returns before he casts his ballot, so a pivot election is only a subjective probability from his point of view"
- Quote: "and the expected instrumental value of his vote the product of that probability and the instrumental value of a vote cast in a pivot election."
- Quote: "If subjective probabilities are unbiased, this empirical frequency might be interpreted as an estimate of the average subjective probability in the population of elections with similar election and voter characteristics as those in our samples."
- Note: the paper's estimate is a retrospective frequency from official returns. It says it can be read as an estimate of the AVERAGE subjective probability only "if subjective probabilities are unbiased". The first pass's "average over all votes" is right for p (the vote-weighted frequency: Sec. II.C: "p is an estimate of the probability that a randomly chosen ballot is cast in an election decided by zero or one votes").

### B4-M10 What the paper's own Table 3 does to the one US case (not in the first pass)
- First pass said: (not stated; the first pass relies on "16,577 elections: one decided by a single vote").
- Mark: corrected (a qualification)
- Source: mulligan_hunter; https://www.nber.org/papers/w8590.pdf; Sec. IV.A and Table 3; PDF pp. 33-35 (printed pp. 23-25)
- Quote: "FED NY 10 36/H 20685-20684 20690-20684 Another recount broke the tie by one, when an arithmetic error was discovered."
- Quote: "recognize that the election was not that close."
- Quote: "rather than two ties and eight one-vote victories in the combined data set of 56,613 elections (an unweighted pivot election frequency q(1)"
- Quote: "= (10+2)/56613 = 0.0002), we have one tie and four one-vote victories (a frequency q(1)"
- Quote: "= (5+1)/56613 = 0.0001). This is a 50% reduction in the unweighted frequency and, since 76% of the"
- Quote: "76% reduction in the vote-weighted frequency."
- Correction: old → new: "16,577 US House elections: one decided by a single vote" stands as the OFFICIAL-count result, but the paper's own check of the ten tied or one-vote elections (Table 3) finds that on the "latest" counts the only US case, NY-36 in 1910, is 20690-20684, a margin of 6, and that "both parties recognize that the election was not that close". On the latest counts the ten become "one tie and four one-vote victories", all of them STATE races; the unweighted frequency halves and the vote-weighted frequency falls 76%. [M] check: votes in the ten elections = 61,328 + 41,369 = 102,697; votes in those still pivotal on the latest counts (NM 4,654 + ME 2,773 + RI 3,519 + MO 9,637 + UT 3,861) = 24,444; 24,444/102,697 = 23.8%, so 76.2% not pivotal ✓. The paper adds that it "might have increased these frequencies if we had verified official margins in some of the other 56,603 elections". So the House 1 in 100,000 rests on one race that the paper's own check says was not a one-vote race [I: on latest counts the House sample has zero].
- Note: Sec. IV.A conclusion: "In other words, even when the election is over, one cannot know for sure whether or not the outcome hinged on one vote." (PDF p. 35, printed p. 25).
- Quote: "In other words, even when the election is over, one cannot know for sure whether or not the outcome hinged on one vote."

### B4-M11 Recounts and the tie rule inside M&H (not in the first pass)
- First pass said: l. 94, l. 302: the recount point is "GKB fn. 6" (wrong source; B4-05).
- Mark: corrected (the recount material is M&H's and GSE's)
- Source: mulligan_hunter; https://www.nber.org/papers/w8590.pdf; Sec. III.B, PDF p. 32 (printed p. 22); Sec. V, PDF pp. 36-37 (printed pp. 26-27)
- Quote: "Furthermore, a vote can have (instrumental) value even the election in which it was not cast in a pivot election (as we have defined it)"
- Quote: "because a single vote can affect whether there is a recount, which in turn has some probability of changing the outcome of the election."
- Quote: "So, conditional on a recount, a pivotal vote is one cast for a candidate winning by no more than one according to the recount."
- Quote: "preliminary investigation of recounts suggest that the frequency of a pivotal ballot would only be 1/v, rather than 2/v, according to this definition."
- Correction: old → new: "GKB fn. 6 on recounts" → M&H Sec. III.B (a stylized model: a recount is held when the initially observed margin is within g_i, and the official margin is then the true margin), and Sec. V ("1/v, rather than 2/v" under a recount-based definition of a pivotal ballot; the factor is a "preliminary" result), plus GSE footnote 6 / 3 (B4-05).
- Note: this is the only place in the four papers where a decisiveness probability is recomputed under a recount rule, and it halves the frequency (2/v → 1/v) and adds a second route to value (a vote's effect on whether a recount happens). Statement by the authors, not tested by me; it rests on "preliminary investigation".

### B4-M12 Do the working paper's numbers equal the 2003 *Public Choice* article's?
- First pass said: l. 273: all M&H figures are attributed to "Mulligan & Hunter (2003) *Public Choice* 116: 31-54".
- Mark: unread
- Source: mulligan_hunter; https://www.nber.org/papers/w8590.pdf; cover, PDF p. 2 (printed: unnumbered)
- Quote: "NBER Working Paper No. 8590 November 2001"
- Note: every M&H figure in this file (16,577; 40,036; two ties and seven single-vote; 0.00006; 1 in 100,000; 1 in 15,000; Table 3) is from the November 2001 working paper. The 2003 article was not in `SRC`; whether its sample, counts, abstract rates or wording match is unread. A citation of these numbers to the *Public Choice* article would not rest on a text that was read.

---

## D. Differences between the 2008 manuscript (`gse2008`) and the published article (`gse_columbia`)

### B4-D1 Every difference
- First pass said: (not stated; batch task 3: "list every difference").
- Mark: confirmed (comparison made by word-level diff of both texts, then by reading both; figure pages 8-9 / 4-5 compared by eye)
- Source: gse_columbia; https://sites.stat.columbia.edu/gelman/research/published/probdecisive2.pdf; whole article, PDF pp. 1-6 (printed 321-326), against `gse2008` PDF pp. 1-9
- Quote: "We computed these probabilities a week before the 2008 presidential election, using state-by-state election forecasts based on the latest polls."
- Quote: "prospectively, most likely to matter in New"
- Quote: "equivalent to a charitable contribution. Fowler (2006) gives"
- Note: **Numbers: no estimate differs.** 1 in 10 million (NM, VA, NH, CO), 1 in 60 million, 10,000 × 51 simulations, t with 4 d.f., ½ credit, fn. values (5e-85 → 2e-12; 9e-16 → 2e-10; Ohio 3.4e-8 → 3.1e-8), 18% / 55 electoral votes / 1 in 100 million (CA), <1% / 1 in 70,000 (NH), 1.3% / 1.2% / 1 in 6,000 (NM), 4% + 4% turnout adjustment, and the "billion" parenthetical are identical in both (checked by a number-token comparison of the two main texts; remaining numeric differences are formatting: 2000n → 2,000 n; 1000 → 1,000; -.208 → -0.208; 6000 → 6,000; "5 electoral votes" → "five"; ½ → 1/2). Figures 1-3 are the same data redrawn (Fig. 2/3 positions look the same by eye; I did not extract plotted values).
- Note: **New numerical content in the published version only (all post-election):** (1) "After the election, we compared state-by-state forecasts to actual election outcomes and found a very close match, with a difference of less than 1 percentage point in 22 states and a difference of less than 3 percentage points in 39 of the 50 states (Gelman and Sides 2009)." (footnote 5, PDF p. 2); (2) "In retrospect, there were some differences from 2004 to 2008; for example, Indiana saw an increase in turnout of nearly 5 percentage points, while Ohio’s rate of voter turnout decreased slightly (McDonald 2009)." (footnote 6, p. 2).
- Note: **Wording changed from present to past/retrospective:** abstract "compute these probabilities for each state in the 2008 presidential election" → "computed these probabilities a week before the 2008 presidential election"; "is most likely" → "was most likely"; "has" → "had" (3 places in the abstract, in Fig. 1 and its caption, in the text); "This year, Ohio, Florida, and Pennsylvania are" → "In 2008, ... were". New in the published text: Fig. 1 paragraph says "your vote was, prospectively, most likely to matter" ("prospectively" is not in the manuscript). Footnote 7 (manuscript fn. 10): "We ignore the splitting of Nebraska’s and Maine’s electoral votes, a rule that is not expected to matter in the current election." → "We ignored the splitting of Nebraska’s and Maine’s electoral votes, which retrospectively turned out to be a mistake in 2008, when Obama won an electoral vote from one of Nebraska’s districts."
- Note: **New footnote 9 (published only), bearing on B and C:** "Hansen, Palfrey, and Rosenthal (1987) discuss the cost of voting, and Edlin, Gelman, and Kaplan (2008) estimate the dollar-equivalent benefits, considering voting as equivalent to a charitable contribution. Fowler (2006) gives experimental evidence relating altruism to voter turnout." (PDF pp. 4-5, printed pp. 324-325.) The text cites "Edlin, Gelman, and Kaplan (2008)" but the reference list has only the 2007 *Rationality and Society* item; Fowler (2006), Gelman & Sides (2009), Hansen, Palfrey & Rosenthal (1987, *Public Choice* 52: 15-33) and McDonald (2009) are new references.
- Note: **Footnote renumbering:** manuscript fns. 1-3 (author affiliations) are replaced by a star note and an affiliation block, so: manuscript fn. 4 → published fn. 1; 5 → 2; 6 (recount) → 3; 7 → 4; 8 (forecast literature) → 5; 9 (turnout) → 6; 10 → 7; 11 (t-distribution) → 8; new 9. The first pass's "fn. 11" is the manuscript's number (published: 8).
- Note: **Typo and style fixes:** "using based on the latest opinion polls" → "based on the latest opinion polls"; "Figure 2a ... Figure 2a" → "Figure 2A ... Figure 2B"; "your stat" → "your state"; "the any instrumental rationality" → "any instrumental rationality"; "how people voter to improve" → "How People Vote to Improve"; "scientists forecast that" → "forecasted that"; Fig. 3 notes "the chance that a single vote is decisive" → "is pivotal", and "The blue lines" → "The lines"; manuscript date line "27 Oct 2008" removed; headings Roman-numbered (I. INTRODUCTION, II. METHOD, III. DISCUSSION); a JEL code "(JEL H0)" and the acknowledgment star note added; Edlin's affiliation expanded to "Department of Economics and School of Law".

---

## E. Fill-in: what each paper means by "decisive", the ½, coverage, prospective versus historical

### B4-F1 GKB (1998)
- First pass said: (not stated; batch task 3).
- Mark: confirmed
- Source: gkb98; https://gking.harvard.edu/files/estimatprob.pdf; abstract and intro PDF pp. 1-2; Sec. 3.1 PDF p. 3; Sec. 4.1 PDF p. 4; Sec. 4.3 PDF p. 5; Sec. 5 and 6.1 PDF pp. 6-7 (printed same)
- Quote: "electorate, an election where one vote is decisive (equivalent"
- Quote: "to a tie in your state and in the electoral college) will almost"
- Quote: "gle vote will be decisive, for voters in each state in every"
- Quote: "postwar election. We also perform some more approximate"
- Quote: "although our model is conditional on the information"
- Quote: "ditioning on all the information available that an individual"
- Quote: "voter would have just prior to election day."
- Quote: "We estimate probabilities for the 1992"
- Quote: "each presidential election year from 1952 to 1992, exclud-"
- Quote: "(The factor of 1/2 applies because we are consid- ering the effect of casting a vote, not the effect of switching a preference from one party to the other.)"
- Note: **Decisive** = a presidential vote that (i) finds its state tied or one vote from tied among the other voters and (ii) the state then decides the national electoral vote (eq. 1-3, B4-01..03); a voter "who will either vote for one candidate or not vote" (cast versus abstain). **The 1/2**: yes, twice in eq. (3), on national electoral-vote ties only ("only half as decisive"); none in eq. (2). A different 1/2 appears in the empirical check on p. 6, "because we are considering the effect of casting a vote, not the effect of switching a preference" (and on p. 7: mobilizing N supporters is "roughly N times" the single-vote probability while switching N voters' preferences is "roughly 2 N times"). **Coverage**: the 1992 election in detail (forecast with pre-November-1992 information; model fit to 1948-1988 data); summary results for the elections 1952-1992 excluding 1968 (Fig. 2b); intro says "every postwar election"; a House check, 1900-1992, 20,597 elections: "a frequency probability of about .5/20,597 that a single vote will be decisive in a randomly chosen U.S. House election" (p. 6; the paper does not show how .5 is obtained; .5/20,597 = 2.4×10⁻⁵ = 1 in 41,194), and an upper bound 20/n for any election (1 in 10,000 for n = 200,000: 1/(sqrt(2π)×.02) = 19.95 → 19.95/200,000 = 1 in 10,027). **Forward-looking or historical?** Forward-looking: "(prospective)" in the abstract and Sec. 6.1, conditional on the pre-election forecast; the historical frequencies are offered as "a numerical check" and the authors "prefer the forecast-based estimates". The House frequency (p. 6) is per-election, not per-vote-weighted.

### B4-F2 GSE (2008 manuscript; the 2012 article is the same)
- First pass said: (not stated; batch task 3).
- Mark: confirmed
- Source: gse2008; https://www.stat.berkeley.edu/~aldous/157/Papers/vote.pdf; abstract and Method PDFs pp. 1-3; Discussion p. 4 (printed same). Published equivalents: `gse_columbia` PDF pp. 1-4.
- Quote: "This is of interest in the utility theory of voting and also for campaign strategists who must assess the costs and benefits of attempting to persuade or turn out voters in particular states."
- Quote: "Elections are very rarely tied, so one can instead use an estimate such as y/(2000n), where y is now the number of elections decided by less than 1000 votes."
- Quote: "Mulligan and Hunter (2003) use such a model for estimating the average probability of a decisive vote in legislative elections, and"
- Quote: "We convert this percentage to a numerical vote margin by multiplying by the voter turnout in the state"
- Note: **Decisive** = "your vote ... determining the national election outcome": P(state necessary for an electoral-college win) × P(exact tie in the state | necessary) (B4-20..22). "Necessary" = the electoral-vote margin among all other states is less than E (plus a ½ share where it equals E). **The ½**: yes, on the electoral-vote tie only, with the stated rationale "no idea who would win in the event of an electoral vote tie" (B4-21). At the state level they use the exact-tie density (B4-22) with no ½ and no one-short term mentioned. **Coverage**: the 2008 presidential election, 51 jurisdictions, forecast computed 24 October 2008; Nebraska/Maine splits ignored; turnout = 2004 two-party turnout +4% (population) +4% (anticipated increase). **Prospective or historical?** Prospective, forecast-based ("the third method"); the empirical y/n method is described and set aside: "the complex structure and the small number of presidential elections rule out a purely empirical approach in this case". Published: "your vote was, prospectively, most likely to matter".
- Note: **On B (see "Found" item 6):** "the payoff is the chance to change national policy and improve (one hopes) the lives of hundreds of millions" (others' welfare in B) and "many can feel that their preference is not only better for them personally but for millions of others"; the paper gives no value for B.

### B4-F3 M&H (WP, 2001)
- First pass said: (not stated; batch task 3).
- Mark: confirmed
- Source: mulligan_hunter; https://www.nber.org/papers/w8590.pdf; Sec. II.B PDF p. 8 (printed p. 5); Sec. II.C PDF pp. 16-18 (printed pp. 6-8); Sec. V PDF pp. 36-37 (printed pp. 26-27)
- Quote: "Hence, while q is an estimate of the probability that a randomly chosen election will be decided by zero or one votes,"
- Quote: "p is an estimate of the probability that a randomly chosen ballot is cast in an election decided by zero or one votes."
- Quote: "Multiplying by 3/2 yields an estimate that an election is either decided by 1 or decided by 0 votes."
- Quote: "the frequency of a pivotal ballot (ie, one cast for a winner in an election decided by one vote, or for either candidate in a tied election)"
- Quote: "is closely approximated by 2/v, which is broadly consistent with a binomial model."
- Quote: "Most economic models of voting assume that voters treat their vote as if it had instrumental value, and therefore cast for the candidate whose policies are expected to yield the voter higher income or utility."
- Note: **Decisive** = "pivotal vote" (B4-M04): on OFFICIAL, FINAL returns, a vote for the winner of an election won by no more than one vote, or for either candidate in a tie. Two statistics: q (per election: the probability an election is decided by 0 or 1 votes) and p (the same, weighted by votes cast: the share of ballots cast in such elections). **The 1/2**: no weight on ties or one-vote margins (B4-M05). **Coverage**: US House 1898-1992 (even years), 16,577 contested elections; STATE legislatures 1968-1989, 40,036 contested general elections (B4-M02, B4-M03). **Prospective or historical?** Historical, ex post frequency, from official returns (B4-M09). The paper's own summary rule for the pivotal-ballot frequency is "2/v" (v = total votes in the election, over the range 25 to 388,143 votes for STATE and 2,723 to 1,663,687 for US, Table 1); the US frequency rises with size below about 30,000-40,000 votes.

---

## F. Recomputation (task 2)

### B4-R1 1/15,000, 1/16,700, 1/100,000 against M&H's own figures
- First pass said: l. 273, 285-286, 291: "about 1 in 100,000 votes (House), about 1 in 15,000 (state legislature; the body's 0.00006 is about 1 in 16,700)"; 6.7×10⁻⁵ and 1×10⁻⁵ in the break-even table.
- Mark: confirmed (arithmetic); see Note for the bases
- Source: mulligan_hunter; https://www.nber.org/papers/w8590.pdf; abstract PDF p. 2; Sec. II.C PDF pp. 16-17 (printed pp. 6-7); Table 1 PDF p. 7 (printed p. 4); Table 3 PDF p. 34 (printed p. 24)
- Quote: "elections 16,577 40,036"
- Quote: "average 111,370 23,658"
- Quote: "41369 votes were cast in that election, or a 0.00002 share of all of the votes in the US"
- Quote: "61,328 votes were cast in those nine elections, or a 0.00006 share of all of the votes in the STATE elections analyzed."
- Note: arithmetic (python3 -I, `SCRATCH/b4work/tools/calc.py`).
  - Round-number conversions: 1/15,000 = 6.667×10⁻⁵ (first pass writes 6.7×10⁻⁵ ✓); 1/16,700 = 5.988×10⁻⁵ and 1/0.00006 = 16,666.7 (so "about 1 in 16,700" ✓); 1/100,000 = 1.000×10⁻⁵ ✓; 1/0.00001 = 100,000 ✓; 1/0.00002 = 50,000.
  - Total votes in each sample = elections × average total votes (Table 1): US 16,577 × 111,370 = 1,846,180,490; STATE 40,036 × 23,658 = 947,171,688 (the paper says "almost one billion votes" ✓).
  - US, all votes in the one pivot election: 41,369/1,846,180,490 = 2.24×10⁻⁵ = 1 in 44,627; the paper's "0.00002" ✓. US, winner's votes only (20,685): 20,685/1,846,180,490 = 1.120×10⁻⁵ = 1 in 89,252; the paper's "0.00001" is this rounded to one figure; 1/0.00001 = 100,000 is the abstract's "one of every 100,000". So the abstract's House figure is the winner-only ("mattered") share, rounded up from 1 in 89,000.
  - STATE, all votes in the nine pivot elections: 61,328/947,171,688 = 6.475×10⁻⁵ = 1 in 15,444; this is the abstract's "one of every 15,000" (the body rounds it to 0.00006 = 1 in 16,667). It counts the loser's votes in the seven one-vote races, which the paper's own fn. 6 excludes for the US figure.
  - STATE on the paper's own definition [M, from Table 3's official column and Table 1]: the nine STATE rows sum to 8,220 + 4,654 + 2,773 + 10,703 + 3,519 + 13,043 + 9,637 + 4,917 + 3,861 = 61,327 (the paper's 61,328 differs by one vote; the RI-78 text mentions a "disputed 8221st ballot"). Pivotal votes = every vote in the two ties (8,221 + 4,654 = 12,875) + the winner's votes in the seven one-vote races (1,387 + 5,352 + 1,760 + 6,522 + 4,819 + 2,459 + 1,931 = 24,230) = 37,105. 37,105/947,171,688 = 3.92×10⁻⁵ = 1 in 25,527. The all-votes basis is 1.65 times larger (61,328/37,105).
  - So the first pass's rows "1 in 15,000, state legislatures" and "1 in 100,000, House" are on different bases (all votes in pivot elections versus winner's votes only). On one basis (winner's/either-in-tie votes) they are about 1 in 25,500 and 1 in 89,000. On the other (all votes in pivot elections) about 1 in 15,400 and 1 in 44,600.
  - Per-election frequencies (different quantity): US 1/16,577 = 6.03×10⁻⁵ (paper: 0.00006 ✓); STATE 9/40,036 = 2.25×10⁻⁴ (paper: 0.0002 ✓, 1 in 4,448); 12/56,613 = 2.12×10⁻⁴ (paper: 0.0002 ✓); 6/56,613 = 1.06×10⁻⁴ (paper: 0.0001 ✓).

### B4-R2 The rest of the first pass's round-number conversions and the break-even table
- First pass said: l. 285-289: p = 6.7×10⁻⁵, 1×10⁻⁵, 1×10⁻⁷, 1.7×10⁻⁸ (1 in 60 million), 1×10⁻⁹; B* = C/p at C = $3.80 and $12.03: $57,000 / $180,500; $380,000 / $1.2 million; $38 million / $120 million; $228 million / $722 million; $3.8 billion / $12 billion.
- Mark: confirmed (arithmetic only; the inputs C are from sources outside this batch, not read by me)
- Source: gse2008; https://www.stat.berkeley.edu/~aldous/157/Papers/vote.pdf; abstract PDF p. 1 (1 in 10 million, 1 in 60 million); Discussion PDF p. 4 (1 in a billion)
- Quote: "On average, a voter in America has a 1 in 60 million chance of being decisive in the presidential election."
- Quote: "Texas where the probability of a decisive vote is closer to 1 in a billion, any reasons for voting must go beyond the any instrumental rationality.)"
- Note: [M] computed: 1/10,000,000 = 1×10⁻⁷ ✓; 1/60,000,000 = 1.667×10⁻⁸ (first pass writes 1.7×10⁻⁸); 1/1,000,000,000 = 1×10⁻⁹ ✓. C inputs: 6/60 × $38 = $3.80 ✓; 19/60 × $38 = $12.03 ✓. B* = C/p: 1/15,000 → 3.80 × 15,000 = $57,000 ✓ and 12.03 × 15,000 = $180,450 (first pass: $180,500, rounded ✓; at p = 6.7×10⁻⁵ it would be $179,552); 1/100,000 → $380,000 ✓ and $1,203,000 ✓; 1×10⁻⁷ → $38,000,000 ✓ and $120,300,000 ✓; 1/60,000,000 → 3.80 × 60,000,000 = $228,000,000 ✓ and 12.03 × 60,000,000 = $721,800,000 ✓ (at the printed 1.7×10⁻⁸ it would be $223.5 million and $707.6 million, so the first pass used 1/60 million exactly, not its printed 1.7×10⁻⁸); 1×10⁻⁹ → $3.8 billion ✓ and $12.03 billion ✓. For comparison [M]: p = 1/25,527 (the STATE share on the paper's own definition, B4-R1) gives $97,000 and $307,100.

---

## Corrections table

| Old (first pass) | New | Source |
|---|---|---|
| "GKB's footnote 6 'addresses the recount objection but doesn't change the definition' (extractor, p. 2)"; "(2.2; GKB fn. 6)" (l. 94, 302) | `gkb98` has no footnotes and no "recount". The recount footnote is GSE footnote 6 of the 2008 manuscript, p. 2 (footnote 3 of the Economic Inquiry article, p. 321); it says the "one vote never makes a difference, because ... there would be a recount" objection "is wrong" and that the simple decisive-vote model is "a reasonable approximation". M&H Sec. III.B and V are the recount treatments inside the four papers. | gse2008 PDF p. 2; gse_columbia PDF p. 1; mulligan_hunter PDF pp. 32, 36-37 |
| State factor is "roughly the density of the vote-share forecast at .5 divided by the number of voters" (in quotation marks, l. 112) | not a quotation; eq. (2) is Pr(n_i v_i = .5 n_i) = Pr(v_i = .5) ≈ f_{v_i}(.5)/n_i, with n_i the voters in state i "excluding yourself" (substance right) | gkb98 PDF p. 3 (page image) |
| the paper "does not compute the expected utility of voting or a benefit-cost ratio" (quoted, l. 271) | not in the paper; substance true (no B, no cost), the only "expected utility" is "...for expected utility calculations" (Sec. 6.3) | gkb98 PDF p. 8 |
| "varying 'by about a factor of 10 among states'" cited to pp. 5-6 (l. 271) | words are verbatim, location is the abstract, p. 1, and refers to "close national elections such as 1992" | gkb98 PDF p. 1 |
| [I] p ≡ ½[P(tie among others) + P(A one behind)] "consistent with GKB's ½" (l. 93, 314) | GKB's ½ is on the national electoral-vote tie only; the state-level eq. (2) has no ½ (so the first pass's p is half of GKB's state-level quantity); GSE's ½ is also on the electoral-vote tie only | gkb98 PDF p. 3; gse2008 PDF p. 3 |
| M&H rows: "1 in 100,000 (House)" and "1 in 15,000 (state legislature)" treated as one kind of p (l. 273, 285-286, 291) | the two are on different bases: 1 in 100,000 is the winner-only share (0.00001, unrounded 1 in 89,252); 1 in 15,000 is the share of all votes in the nine pivot elections (unrounded 1 in 15,444); on the paper's own definition the STATE share is about 1 in 25,500 [M] | mulligan_hunter PDF pp. 2, 16-17, 34 |
| "16,577 US House elections: one decided by a single vote" (l. 273) | stands for official counts; the paper's Table 3 shows the one US case (NY-36, 1910) at 20690-20684 on the latest count, "not that close"; on latest counts the paper finds 1 tie + 4 one-vote races, all STATE | mulligan_hunter PDF p. 34 |
| fn. 11 (l. 272) | fn. 11 is the manuscript's number; the published article has it as fn. 8 (same values; direction normal → t; Ohio 3.4e-8 → 3.1e-8 also given) | gse2008 PDF pp. 3-4; gse_columbia PDF p. 3 |
| 1.7×10⁻⁸ (1 in 60 million) in the break-even table | the table's $228 million / $722 million use 1/60,000,000 = 1.667×10⁻⁸ exactly; at 1.7×10⁻⁸ they would be $223.5 million / $707.6 million | calculation B4-R2 |
| M&H numbers attributed to "Mulligan & Hunter (2003) *Public Choice* 116: 31-54" (l. 273) | the numbers are from NBER Working Paper 8590, November 2001 (the file read); the journal citation is confirmed only through the GSE reference lists; the article's text was not read (B4-M01, M01b, M12) | gse2008 PDF p. 6; mulligan_hunter PDF pp. 1-2, 38 |
| "Economic Inquiry 50(2): 321-326, 2012 ... rests on a search-result title" (l. 272) | resolved: `gse_columbia` is that article (header: Vol. 50, No. 2, April 2012, 321–326; doi 10.1111/j.1465-7295.2010.00272.x); no estimate differs from the manuscript | gse_columbia PDF p. 1 |

## Unread and why

- **The Public Choice 116: 31-54 (2003) article itself.** Not in `SRC`; only the NBER working paper (November 2001) was downloaded. Every M&H number in the first report is from the working paper's text; the published article's numbers, wording and any regression were not checked. The citation "Public Choice 116, 31-54" is confirmed only through the GSE reference lists. *Reason: no network (rule 1); needs the journal page.*
- **Gelman, Katz & Bafumi (2004, *BJPS* 34: 657-674), p. 674** (the source the recount footnote cites for "why this argument is wrong"). Not read; the first pass lists it unread too.
- **Edlin, Gelman & Kaplan (2008)** cited in the published footnote 9 as estimating "dollar-equivalent benefits" (a different date from the 2007 article in the reference list). Not in this batch.
- **M&H figure pages** (Figures 1a-2d, 3a-4b, 5, 6; PDF pp. 9-15, 20-23, 25-27) were not viewed; they are histograms and fitted curves, and no first-pass fact or task item rests on them. The numbers quoted from "Figure 5" in the text (1/6000 for v = 20,000; f(½) ≈ 2) are the paper's words only.
- **GKB pages 4, 8, 9** were read from the OCR text layer only (not imaged); nothing figure-like in the batch rests on them except the sentence in B4-13 and the 1948-1988 fitting years (B4-12), both plain text. **GSE Figure 1** (the state map) not viewed.
- **GSE: the 1 in 10 million state-by-state values in Fig. 2/3** (positions only, no axis values extracted). The first pass does not cite them.
- **The C inputs in the break-even table** ($38/h, 6 and 19 minutes; SPAE 2022; a smartphone study) are outside the batch; I checked only the multiplication.

## Found that the first pass missed

1. **The recount footnote is GSE's, not GKB's** (B4-05). GKB (JASA) has no footnotes and never says "recount". What GSE say is that the objection is wrong, not that it "doesn't change the definition". M&H (not GKB) treat recounts at length (B4-M10, B4-M11).

2. **Three different tie conventions, and a possible factor of 2 between them [I; the algebra is mine, the sentences are quoted above].** (a) GKB eq. (2) takes P(your vote decisive in your state) = Pr(v_i = .5) ≈ f(.5)/n_i, "exactly tied or one vote away from a tie", with NO ½; the ½ enters only at the national electoral-vote tie (eq. 3). (b) M&H's definition counts every winner's vote in a one-vote election and every vote in a tie at weight 1, and the model's per-ballot probability is f(½)/(v+1) = P(tie | v even), again with no ½ (B4-M05). (c) The first pass's algebra, p = ½[P(M=0) + P(M=-1)], puts a ½ on the popular-vote tie. Consider X = D minus R votes among n other voters, with density g per vote of margin. X moves in steps of 2, so P(X=0 | n even) ≈ 2g(0), and for n odd P(X=-1) ≈ 2g(0) too. Then: GKB (2): f_v(.5)/n = 2g(0) (since f_X(0) = f_v(.5)/(2n) when X = n(2v-1)): the full tie probability. Fair-coin tie rule: p = ½ × 2g(0) = g(0) = f_v(.5)/(2n), half of GKB's. GSE's state factor is "the density at 0" of the vote margin, in votes (the −.208 example is a difference of shares times turnout), i.e. g(0) with no lattice factor 2; so on the same forecast it equals the coin-flip p, and is half of GKB's (2) [I]. The GSE text neither mentions the lattice nor says it is applying a ½ at the state level; its stated ½ is on the electoral-vote tie only (B4-21). If both statements hold, GKB's and GSE's "1 in 10 million" headline levels are on conventions that differ by 2 at the state tie, before any difference in model or year. A statistician should confirm before the site compares levels across these sources.

3. **M&H's two abstract rates are on different bases, and the House one rests on a case the paper's own check says was not a one-vote race** (B4-M06, B4-M10, B4-R1). 1 in 100,000 = winner's votes only (rounded from 1 in 89,252); 1 in 15,000 = all votes in the nine pivot elections (1 in 15,444); the paper's own definition applied to the state sample gives about 1 in 25,500 [M]. The single US case, NY-36 1910, is 20690-20684 on the latest count ("not that close"): on the paper's latest counts the House sample has no one-vote race and the STATE sample has one tie and four one-vote races (-50% unweighted, -76% vote-weighted).

4. **"1 in 16,700" is easily confused with a different 0.00006** (1/16,577, the US per-election frequency, p. 6). The first pass used the right one (the STATE vote share, p. 7), but a reader could cite either (B4-M07).

5. **M&H's "binomial over-predicts" is milder and different from the fixed-A binomial in other sources** (B4-M08): "somewhat less"; their binomial integrates over a prior for A; with fixed A = .61 and v = 100,000 the model gives about 10^-1108 against an observed 0.00005 (footnote 14). Figures such as Carling's 10^-90 or SEP's "millionth of a penny" are fixed-A binomial results, the kind M&H say are wildly wrong; their own p ≈ 2/v is not the binomial being rejected.

6. **Fork 1, whose welfare is in B** (quotes in B4-F1, F2, F3). GKB: the rational-choice puzzle is framed as "considering only the immediate personal costs of voting and direct personal gains from influencing the outcome" (p. 2: lines "agree it is low enough so that considering only the immedi-" / "ate personal costs of voting and direct personal gains from"), with "Many reasons for voting other than direct personal gain from the election outcome can also be given" (p. 2). GSE: B is "the chance to change national policy and improve (one hopes) the lives of hundreds of millions" and "not only better for them personally but for millions of others"; the published version adds footnote 9 ("considering voting as equivalent to a charitable contribution"; altruism and turnout). M&H: voters cast "for the candidate whose policies are expected to yield the voter higher income or utility" (own-welfare framing, p. 6). None of the four computes B.

7. **Fork 2, B as gain-if-decisive or expected gain pB.** M&H state both: "a pivot election is only a subjective probability from his point of view, and the expected instrumental value of his vote the product of that probability and the instrumental value of a vote cast in a pivot election" (B4-M09), i.e. B = the instrumental value of a vote cast in a pivot election; pB the expected value. GSE: the lottery-ticket image keeps the chance (1 in 10 million) and the payoff separate (B4-27). GKB: "The exact value of this probability is of only minor interest".

8. **Fork 3, the tie rule (the ½).** (i) GKB: ½ only for a national electoral-vote tie ("only half as decisive"); no ½ at state level; no rule for how the tie would be resolved is described. (ii) GSE: ½ for an electoral-vote tie because "we have no idea who would win"; the state-level exact-tie density (see item 2). (iii) M&H: weight 1 for tie and one-vote margin; the ½'s in their text are parity counts (footnote 8) and the winner-only-ballot fraction. (iv) GKB p. 6, a second ½: "we are considering the effect of casting a vote, not the effect of switching a preference"; p. 7: switching N voters is worth "roughly 2 N times" a single-vote probability versus "roughly N times" for mobilizing N supporters; this is the cast-versus-abstain versus switch distinction the owner's setup needs. (v) Recounts: GSE fn. 6 (objection wrong, simple model is a reasonable approximation); M&H: a recount-based definition cuts the frequency from 2/v to 1/v ("preliminary"), and a single vote can matter by affecting whether there is a recount; Table 3 shows tied/one-vote results changing on recount, a rerun election (RI 1978), and "even when the election is over, one cannot know for sure whether or not the outcome hinged on one vote."

9. **Fork 4, causal versus evidential "held fixed".** None of the four papers uses or discusses causal or evidential decision theory (searched "causal", "evidential": no hits). GKB/GSE treat the other voters' totals as uncertain draws from a forecast conditioned on pre-election information ("conditioning on all the information available that an individual voter would have just prior to election day"), not as correlated with one's own choice. M&H mention dependence across voters only as a modelling issue: "we suspect that the effective number of voters is less than the actual number of voters v" and a footnote's husbands-and-wives example (the probability would be (1.5)f(½)/(2v+1) rather than (1.5)f(½)/(v+1)); that is a probability-model statement, not a decision-theoretic one.

10. **Fork 5/6, D and C.** M&H: "the costs of voting are often small, so a precise calculation of the frequency of a pivotal vote can contribute to our understanding of how many, if any, votes might be rationally and instrumentally cast" (PDF p. 4, printed p. 1). GKB p. 7: "one must also account for the possibility that the voter may influence other, nonpresidential contests at the ballot box" (a benefit-side addition: other contests on the same ballot; Quote: "In addition, our results are of interest to rational choice theorists interested in the rationality of the decision of the individual citizen whether to vote; of course, one must also account for the possibility that the voter may influence other, nonpresidential contests at the ballot box."). GSE (2008) for NY, CA, TX: "any reasons for voting must go beyond the any instrumental rationality" (D enters); the published footnote 9 points to Hansen, Palfrey & Rosenthal (1987) for the cost of voting.

11. **GKB's own House check** (p. 6): 20,597 House elections 1900-1992 versus M&H's 16,577 (1898-1992, contested only): different samples and different quantities (GKB's ".5/20,597" is described as the probability that a single vote is decisive in a random House election; M&H's 1/16,577 is an election frequency, and its vote-weighted forms are 1.1×10⁻⁵ and 2.2×10⁻⁵). The paper does not reconcile them, and neither do I.
