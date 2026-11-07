# B5: Barnett, Kagan, JESP reply, Goldman (Cambridge page)

Reader: Sonnet 5.5 (batch B5). First report checked: `/home/user/vote/research/frameworks-benefit-cost.md` (line numbers below are its lines). No network used. Python run with `python3 -I`; scratch only under SCRATCH.

## Sources read, and how

| id | what it is | size | read in full? |
|---|---|---|---|
| `barnett` | Zach Barnett, "Why You Should Vote to Change the Outcome", *Philosophy & Public Affairs* 48(4), 2020, printed pp. 422-446 (PDF metadata Subject: "Philosophy & Public Affairs 2020.48:422-446"; the page footer says "© 2020 Wiley Periodicals LLC"). The file fetched from philosophersannual.org is the P&PA typeset text. | 25 PDF pages, 9,916 words, 1,129 text lines | Yes: every line of `text.txt` read with Read in 4 chunks. I also rendered PDF pp. 9, 11, 12, 16, 21 to images to check the tables, the superscripts and the Appendix A formulas that `pdftotext` scrambled. |
| `kagan` | Shelly Kagan, "Do I Make a Difference?", *Philosophy & Public Affairs* 39(2), 2011, printed pp. 105-141 (page head: "papa_1203 105..141") | 37 PDF pages, 16,081 words, 1,567 text lines | Yes: every line read in 5 chunks. |
| `jesp` | An HTML abstract page at jesp.org (a Discussion article that replies to Barnett; see J5-01) | 1 page, 387 words | Yes (whole text, plus the raw page's `<meta>` tags). Abstract only; the PDF of the article is not in SRC. |
| `cup_goldman` | Cambridge Core abstract page for Goldman 1999 | 1 page, 2,785 words (the first paragraph of the article, 39 footnotes, site boilerplate) | Yes (whole text, plus the raw page's `<meta>` tags). The body of the paper is not on the page. |

**Page arithmetic used throughout.** Barnett: PDF page N has printed page N + 421 (PDF p. 1 = printed 422). Kagan: printed page = PDF page + 104 (PDF p. 1 = printed 105). Every page given below is checked by searching the quote in `text.txt` page by page (form feeds), not read off the first report.

**URLs.** `SRC/<id>/hdr` records no request URL; the URLs below are from the lead's `list1.txt`: barnett https://philosophersannual.org/40articles/barnett-why.pdf ; kagan https://pdf.stafforini.com/kagan-2011-make-difference.pdf ; jesp https://jesp.org/index.php/jesp/article/view/2915 (307 to https://www.jesp.org/index.php/jesp/article/view/2915, then 301 to https://www.jesp.org/paper/36346f73-90e0-81d0-86e6-d03e516d0052, then 200); cup_goldman https://www.cambridge.org/core/journals/social-philosophy-and-policy/article/abs/why-citizens-should-vote-a-causal-responsibility-approach/6628D3915B2973208BBD49C15C90394B (the page's own canonical link, 200 with no redirect).

**Mark rule used.** "corrected" = something the first report states (a number, a quoted wording, a page) differs from the source. A page-only error is labelled `[page only]` in the Correction line so the lead can tell it from an error of substance.

---

# Part 1. Barnett (2020)

### B5-01 Identity and edition
- First pass said: "Barnett (2020)", URL philosophersannual.org/40articles/barnett-why.pdf (lines 76, 79, 140, 275).
- Mark: confirmed
- Source: barnett; https://philosophersannual.org/40articles/barnett-why.pdf; PDF p. 1 (printed p. 422), bottom of page
- Quote: "© 2020 Wiley Periodicals LLC Philosophy & Public Affairs 48, no. 4"
- Note: the PDF has 25 pages = printed 422-446 (the P&PA article; the report's URL gives the P&PA typeset text, not a different Philosophers' Annual text). Barnett is at the National University of Singapore (p. 422 footnote).

### B5-02 B and b defined (first pass: B = b × N, "the net social benefit of having Daisy rather than Donald in charge")
- First pass said: `B = b × N`, "the net social benefit of having Daisy rather than Donald in charge", b the average benefit per person (line 76).
- Mark: corrected
- Source: barnett; https://philosophersannual.org/40articles/barnett-why.pdf; Section II; B first defined PDF p. 5 (printed p. 426); b = B/N completed on PDF p. 6 (printed p. 427)
- Quote: "First, there’s the net social beneﬁt associated with having Daisy rather than Donald in charge, which we can call B."
- Quote: "In contrast, the net social beneﬁt, B, is proportional to N."
- Quote: "we will rewrite B as b × N, where b stands for the average"
- Quote: "social beneﬁt—that is, the average beneﬁt, per person—of having Daisy rather than Donald in charge."
- Correction: [quote wording] the report's quoted string "the net social benefit of having Daisy rather than Donald in charge" is not in the source; the source has "the net social benefit associated with having Daisy rather than Donald in charge". The b definition ("of having Daisy rather than Donald in charge") is right. Substance confirmed.
- Note: B is the benefit of Daisy rather than Donald being in charge, i.e. the gain IF the better candidate wins; it is not multiplied by any probability. The expected gain is EB = ½·B·d (B5-04). So in Barnett B is the "gain if decisive" reading (fork point 5 of the first report's list), not pB. N is "the number of citizens in the community" (p. 426) and the justification for B ∝ N is "an election that affects eight million is, other things equal, twice as important to the consequentialist voter, as an election that affects four million" (p. 426, lines 219-221 of text.txt). Barnett treats N as both the number of citizens affected and the number of voters (see B5-F3, items 6-7). [I] The paper does not discuss a case where the number affected differs from the number who vote.

### B5-03 Whose welfare is in B (and in the cost): the whole public, equal weights, the voter included
- First pass said: the voter is a consequentialist for whom "everyone's interests are given equal weight, including your own" (p. 425) (line 76; also lines 193, 275, 303).
- Mark: confirmed
- Source: barnett; Section II; PDF p. 4 (printed p. 425)
- Quote: "your voting decisions (whether to vote, whom to vote for) will be based solely on what is best for the public, where everyone’s interests are given equal weight, including your own."
- Quote: "costs and beneﬁts to whom—you, the voter? No. If you were wholly self-interested, voting would hardly ever be rational."
- Note: the page is exactly p. 425 (PDF p. 4). Barnett's rationale: the question is whether voting is rational "for a consequentialist voter" (fn 7, same page) and "some citizens may be public-spirited voters" (fn 8). Costs are also social: "we’ll be thinking about the social costs and the social beneﬁts" (p. 425). The cost c is the cost of the person's own voting, counted as a social cost; no number is given for c anywhere in the paper (grep: the only dollar figures are $33 billion, $4.77×10^-2650, $1.4-3.5 trillion, $4000, $3 trillion, $10,000, $500, $1,190,480.60 and $134.92).

### B5-04 EB = ½·B·d, "decisive", and the tie rule
- First pass said: "Barnett, pp. 426-7: a decisive vote 'breaks a tie' or 'causes a tie'; ties are settled by coin flip, so the expected benefit of a decisive vote is half of B: EB = ½ × B × d." (line 88; also lines 93, 275).
- Mark: confirmed
- Source: barnett; Section II; PDF p. 5 (printed p. 426); also footnote 10 on the same page
- Quote: "a vote that breaks a tie (when the number of voters is odd) or causes a tie (when the number of voters is even)."
- Quote: "For simplicity, we’ll assume that, in the event of an exact tie, both candidates are equally likely to be awarded victory—perhaps a coin is ﬂipped to determine a winner."
- Quote: "It follows that the expected beneﬁt of a decisive vote for Daisy, one which causes Daisy to win when she otherwise would have tied, is B – ½ × B, or simply ½ × B."
- Quote: "So the expected beneﬁt of a vote for Daisy, then, is ½ × B × d."
- Note: all of this is on printed p. 426 (PDF p. 5), not 426-7. The tie rule is an assumption "for simplicity": equal chance for each candidate in an exact tie, with a coin flip given as one example ("perhaps"). It is not a claim about real tie-breaking (recounts, courts, runoffs are not discussed). Footnote 10 (p. 426): "When N is even, a decisive vote causes Daisy to tie when she otherwise would have lost. Here too, the expected beneﬁt of a decisive vote works out to ½ × B." Barnett's own wording is counterfactual: "If you had abstained, there would have been a tie" (p. 426). The paper's only stated option set is vote for Daisy or abstain (fn 9, p. 425).

### B5-05 d ≥ 1/N when both candidates have at least a 10% chance
- First pass said: "d ≥ 1/N whenever both candidates have at least a 10% chance (p. 432)" (lines 140, 275).
- Mark: corrected
- Source: barnett; Section IV; the thesis sentence is on PDF p. 12 (printed p. 433), italicised, and begins at the foot of PDF p. 11 (printed p. 432); first stated PDF p. 8 (printed p. 429); the worked argument is PDF pp. 15-16 (printed pp. 436-437); the general form is Appendix A, PDF pp. 20-21 (printed pp. 441-442)
- Quote: "plausible model should make—the probability of casting a decisive vote, d, can be shown to be greater than 1/N as long as both candidates have at least a 10 percent chance of winning."
- Quote: "the chances condition follows from two weak modeling assumptions, together with the claim that both candidates have at least a 10 percent chance of winning"
- Quote: "So the probability of your casting a decisive vote is (at least 5 percent) × (at least 1/50,000), which is at least 1/1,000,000, which is greater than 1/N."
- Quote: "all of whom are certain to vote"
- Quote: "The usual assumptions are in effect: There are N citizens, all of whom will vote for one of the two candidates."
- Correction: [page, and conditions omitted] p. 432 → the sentence straddles pp. 432-433 (thesis italicised on p. 433); first stated p. 429; proved in the worked case pp. 436-437. Substance confirmed, but the claim is conditional on three things the report omits: (a) Partial Unimodality and Narrow Upsets (B5-07); (b) every other citizen votes ("no one will abstain, except maybe you", p. 433, text.txt line 525; "all of whom will vote for one of the two candidates", Appendix A, p. 441); (c) a large electorate (p. 442: "when N ≤ 20, generalized Narrow Upsets is automatically false, for S is empty").
- Note: in the worked argument the underdog has "at least a 10 percent chance of achieving an upset victory" (p. 436, N = 1,000,001); the proof there is: at least a 5% chance the leader gets between 45 and 50% of the others' votes (10% × ½ from Narrow Upsets), over 50,000 possible counts, with the exact-tie count at least as likely as any other (Partial Unimodality) → d ≥ 5% × 1/50,000 = 1/1,000,000. I checked the list-figure on PDF p. 16 (image): 50,000 possibilities, bottom row "500,000 / 500,000 / 50.0000% / Your vote is decisive". The general bound is B5-06. Barnett calls the conclusion conditional: "it can be argued that the value of d is often going to exceed 1/N, so long as the election is reasonably competitive" (p. 436, text.txt lines 651-653).

### B5-06 d ≥ 10u/N, u the upset probability
- First pass said: "d ≥ 10u/N with u the upset probability (p. 437)" (line 275).
- Mark: confirmed
- Source: barnett; Section IV.D, statement and table on PDF p. 16 (printed p. 437), reading of the table and the 90% sentence on PDF p. 17 (printed p. 438); Appendix A, the formula restated on PDF p. 20 (printed p. 441), the definition of u and the proof on PDF p. 21 (printed p. 442)
- Quote: "Probability of upset (percent) d is at least . . . 50 5/N 40 4/N 30 3/N 20 2/N 10 1/N"
- Quote: "d ≥ 10u/N, which implies that d ≥ 1/N in a wide class of cases."
- Quote: "Let u stand for the ex ante probability that the leading candidate earns the triggering amount or fewer votes from your fellow citizens."
- Quote: "even for quite one-sided elections where one candidate has a 90 percent chance of winning, d can still be shown to be at least 1/N."
- Note: p. 437 text: "for large N, d ≥ 10u/N" (the "N." is followed by footnote mark 30). The proof chain ends "= 10u/N⁻ > 10u/N" with N⁻ = N − 1 (the others), so the strict inequality d > 10u/N holds (PDF p. 21 image, printed p. 442). The table value "50 → 5/N" is the maximum, "approximately 5/N for the most competitive elections" (p. 438). Since EB = ½·b·N·d, the table says EB ≥ 0.5b (u = 10%), b (20%), 1.5b (30%), 2b (40%), 2.5b (50%) [M: ½·10u = 5u times b]. u is defined in the Appendix as the ex ante probability that the leader gets the triggering number of votes or fewer from the others (it includes the exact-tie count); the body text calls it "the probability of an upset".

### B5-07 "Partial Unimodality" and "Narrow Upsets"
- First pass said: his chances argument rests on two assumptions he names, "Partial Unimodality" and "Narrow Upsets" (pp. 434, 437) (line 140).
- Mark: confirmed
- Source: barnett; Section IV.C; stated PDF p. 13 (printed p. 434); defended PDF pp. 13-15 (printed pp. 434-436); used PDF pp. 15-16 (printed pp. 436-437); generalised PDF p. 21 (printed p. 442)
- Quote: "Partial Unimodality: The leading candidate is at least as likely to earn exactly half of the vote as she is to earn any precise share of the vote smaller than this."
- Quote: "Narrow Upsets: If the leading candidate fails to earn a majority, then the likelihood that she comes within ten percentage points of her"
- Quote: "Both assumptions are true of every election model with which I am familiar, including the binomial model favored by Brennan."
- Quote: "Looking back on U.S. Senate races from the last ten years, one ﬁnds that in cases where the leading candidate lost, he/she still came within ten points of winning about 92 percent of the time."
- Note: both assumptions concern the proportion of votes the leading candidate earns "when we count up everyone’s votes except for your own" (p. 434). Narrow Upsets completes "... of her opponent is at least ½" (the word is broken "oppo- nent" at a line end in text.txt, hence the truncated quote). The 92% figure is from five Senate cycles (2010-2018) with RealClearPolitics averages used to pick leaders; Barnett's fn 28 (p. 436) lists the 12 upsets and says only Kansas 2014 was won by more than ten points. Partial Unimodality is defended by a unimodality argument on Bayesian grounds (p. 435) and he concedes "one can cook up cases where unimodal expectations would not be appropriate" (fn 27, p. 435). The "narrow" in Narrow Upsets means within ten percentage points of the opponent, which in the Appendix becomes a count window S of N⁻/20 votes below the triggering number (the leader at about 45 to 50% of the others' votes).

### B5-08 The binomial model, "a very poor way to model real-world elections"
- First pass said: Barnett "calls the binomial model 'a very poor way to model real-world elections' (p. 441)" (line 140; line 51 for the "led us astray" part: B5-13).
- Mark: confirmed
- Source: barnett; Section V; PDF p. 20 (printed p. 441); an earlier "a poor way" on PDF p. 19 (printed p. 440)
- Quote: "it is a consequence of the example’s use of the binomial model, which is a very poor way to model real-world elections."
- Quote: "this tight clustering renders the binomial model a poor way to model real-world elections."
- Quote: "the chance that Donald wins or ties is less than 8.84 × 10—2653."
- Note: his stated reason is that the model's tight clustering makes upsets absurdly improbable (with Daisy at 50.5% of 122,293,322 voters), and it "vastly underestimates the probability of an upset" (fn 22, p. 431). He also says which model should replace it "will require detailed work by economists, political scientists, and statisticians" (p. 441). [M] I recomputed the upset bound with log-gamma: t = 61,146,661, log10(t · C(N,t) · 0.505^t · 0.495^(N−t)) = −2652.054, i.e. 8.83 × 10^-2653 (Barnett: 8.84 × 10^-2653), agrees to rounding.

### B5-09 Stakes condition: b > 2c, "more than twice"
- First pass said: stakes condition b > 2c; "sets the threshold at 'more than twice' the cost" (lines 76, 140, 193, 275, 279).
- Mark: confirmed
- Source: barnett; Section II; PDF p. 6 (printed p. 427)
- Quote: "First, there is the stakes condition, which requires the average social beneﬁt of electing the better candidate to be more than twice as great as the individual voting cost."
- Quote: "Given these two conditions, the expected beneﬁt of voting can be proven to be greater than the cost."
- Quote: "Not always, to be sure. There isn’t always very much at stake."
- Note: the derivation is EB = ½·B·d = ½·b·N·d ≥ ½·b·1 = ½·b > c, the first ≥ from d ≥ 1/N and the second > from b > 2c (p. 427; the printed line has the labels i and ii, which pdftotext garbled; I checked the PDF text). The third quote is on PDF p. 7 (printed p. 428): Section III is titled "THE STAKES CONDITION: A QUALIFIED DEFENSE" and Barnett concedes the condition fails when platforms are similar or "the differences may wash out" (p. 428); he argues only that it is "comfortably met" in "at least some fairly ordinary electoral circumstances" (p. 429). The stakes condition compares an average per-person benefit b with one person's cost c; no value of c is given.

### B5-10 The +$134.92 example
- First pass said: in his example "at least +$134.92, and probably much greater" (p. 441) (line 275).
- Mark: confirmed
- Source: barnett; Section V and footnote 36, PDF p. 20 (printed p. 441); Brennan's $33 billion stipulation as quoted from Maring, PDF p. 3 (printed p. 424)
- Quote: "the expected contribution to the public good of a vote for Daisy is nothing like a millionth of a penny—it’s at least +$134.92, and probably much greater."
- Quote: "EBvote = (½)(B)(d) = (½)(+ $33 bil.)(1 / N) = (½)(+ $33 bil.)(1/122,293,322) ≈ +$134.92."
- Quote: "a particular candidate’s victory is worth $33 billion to the common good"
- Note: [M] recomputed: ½ × 33,000,000,000 / 122,293,322 = 134.9215 (python). Because d is set to its lower bound 1/N, this number equals ½·b exactly, with b = $33 bn / 122,293,322 = $269.84 per voter. It is an expected social benefit of one vote (not net of the voting cost c). The $33 billion is Brennan's stipulation (quoted by Barnett p. 424 from Maring), not an estimate of any real election; the 122,293,322 is the 2004 US presidential-election electorate used by Brennan. The paper does not state the underdog's chance in Brennan's example, so that d ≥ 1/N holds there needs the 10% condition, which Barnett does not check for that example. [I] The "$134.92" is therefore "½b at d = 1/N", conditional on B5-05's conditions and on the $33 bn.

### B5-11 Stakes examples: tax relief, Iraq/Afghanistan
- First pass said: Barnett argues the stakes condition from examples (tax relief for below-median earners; the cost of the Iraq and Afghanistan wars, pp. 427-8) (line 279).
- Mark: confirmed
- Source: barnett; Section III; PDF p. 7 (printed p. 428) for both examples; a third example on PDF pp. 7-8 (printed pp. 428-429)
- Quote: "a simple referendum on a policy substantially reducing the tax burden on every household earning less than the median income"
- Quote: "This is more than $4000 per U.S. citizen."
- Quote: "Even if these wars delivered signiﬁcant beneﬁts to the public (a proposition which would be emphatically denied by some),"
- Quote: "Presumably, an average social beneﬁt of $500 would dwarf the individual cost of voting for most Americans."
- Note: both named examples are on printed p. 428 (inside "pp. 427-8", which also covers the section heading on p. 427). The first report omits the third example: a presidential candidate whose spending is "5 percent more efficient" than another's would amount to $500 per citizen on about $10,000 of tax revenue per citizen (pp. 428-429). The Iraq/Afghanistan figure ($1.4 to $3.5 trillion, "more than $4000 per U.S. citizen") is a COST of the wars, used only to show "how much can ride on political decisions"; Barnett does not say it is b for any candidate pair ("Even if these wars delivered significant benefits to the public (a proposition which would be emphatically denied by some)", p. 428). The tax example has no number: "plausibly much higher than the typical cost of voting" (p. 428). Fn 13 (p. 429) adds that voters' ignorance of the benefits is a separate objection, set aside by assuming "a well-informed citizen".

### B5-12 Parfit: "no chance, however small, should be ignored"
- First pass said: "Barnett cites Parfit against ignoring tiny chances: 'When the stakes are very high, no chance, however small, should be ignored' (p. 439, extractor). Parfit's own text is unread." (line 156).
- Mark: confirmed
- Source: barnett; Section IV.E; PDF p. 18 (printed p. 439), quoted from Parfit, *Reasons and Persons* p. 74 (Barnett's fn 32)
- Quote: "When the stakes are very high, no chance, however small, should be ignored."
- Quote: "Parﬁt’s argument, of course, should not necessarily be regarded as the ﬁnal word on the matter."
- Note: the sentence is the last line of a block quotation from Parfit (with "[. . .]" elisions), about nuclear-reactor risk at "one-in-a-million", not about voting; Barnett uses it against the view that tiny chances can be ignored "regardless of the stakes". Parfit's text is still unread (second-hand via Barnett). Barnett's first, independent response is on the same page (PDF p. 18, printed p. 439): even if sufficiently tiny probabilities were ignored in all cases, "the argument presented in this article still shows that, contrary to popular opinion, voting to change the outcome often has positive expected value" (p. 439).

### B5-13 Brennan's example "led us astray"
- First pass said: "Barnett calls the standard binomial argument Brennan's example, which 'led us astray'" (line 51).
- Mark: confirmed
- Source: barnett; Section I, PDF p. 3 (printed p. 424); Section V title "WHAT’S WRONG WITH BRENNAN’S EXAMPLE?" on PDF p. 18 (printed p. 439); the "employs the binomial model" sentence on PDF p. 19 (printed p. 440)
- Quote: "After examining the argument, we will conclude with a discussion of why Brennan’s example led us astray."
- Quote: "As we discussed earlier, this example employs the binomial model."
- Note: the phrase is at the end of the Introduction (p. 424), where he promises what Section V does. What he says "led us astray" is Brennan's single example (a stipulated 50.5% per-voter probability under the binomial model), not "the standard binomial argument" in general; the report's wording widens it. The "(3.1)" in line 51 is the report's own cross-reference.

### B5-14 With both conditions, EB exceeds cost (the report's summary of the argument)
- First pass said: "Barnett (2020) argues d ≥ 1/N (N citizens) and, with b > 2c, that EB exceeds cost" (line 140; line 193).
- Mark: confirmed
- Source: barnett; Section II; PDF p. 6 (printed p. 427)
- Quote: "Given these two conditions, the expected beneﬁt of voting can be proven to be greater than the cost."
- Note: "N" in "d ≥ 1/N" is the number of citizens, and Barnett's N is also the number of voters (all citizens vote in the argument; see B5-05 (b) and B5-F3 items 6-7). Barnett presents the combination as sufficient, not necessary: "two substantive conditions, which happen to be together sufﬁcient for the rationality of voting" (p. 427).

### B5-15 The first report's tie algebra versus Barnett's ½ (line 93)
- First pass said: p ≡ ½·[P(tie among others) + P(A one behind)], "consistent with GKB's ½ and Barnett's ½" (line 93; the open point at line 94 and fork 6 at line 305).
- Mark: confirmed
- Source: barnett; PDF p. 5 (printed p. 426), including footnote 10
- Quote: "When N is even, a decisive vote causes Daisy to tie when she otherwise would have lost. Here too, the expected beneﬁt of a decisive vote works out to ½ × B."
- Note: confirmed for the factor ½ and its source; the equivalence needs this qualification. Barnett's d is ONE event, whichever of the two is possible: with N odd (N − 1 others, even) it is "the others tie"; with N even it is "the others have Daisy exactly one vote short". In his model every other citizen votes (B5-05 (b)), so exactly one of the two events can occur, and the report's ½·[P(M=0) + P(M=−1)] reduces to ½·d with Barnett's d. So the report's p equals ½ × Barnett's d (the ½ is outside Barnett's d, as in EB = ½·B·d). With partial or random turnout both events are possible and Barnett's d would not be the sum; the paper does not treat that case. [I] (my algebra, not stated by Barnett).

### B5-16 The SEP/Brennan quotation as reproduced by Barnett (bears on report line 139)
- First pass said: SEP: the expected benefit under binomial models is "worth far less than a millionth of a penny" (extractor's quote) (line 139; also line 51).
- Mark: confirmed
- Source: barnett; Section I; PDF p. 2 (printed p. 423), Barnett quoting Brennan's SEP entry "The Ethics and Rationality of Voting"
- Quote: "so small that the expected beneﬁt . . . of the modal vote for a good candidate is worth far less than a millionth of a penny."
- Quote: "Thus . . . for most voters in most elections, voting for the purpose of trying to change the outcome is irrational."
- Note: confirmed as to the phrase, as Barnett reproduces it; the qualifier "under binomial models" is not in the reproduced passage. Barnett's version has editorial ellipses. The passage as quoted does not mention the binomial model; Barnett links the binomial model to Brennan's separate example (*Ethics of Voting* pp. 18-20, via Maring p. 245). I have not seen the SEP page, so "under binomial models" is neither confirmed nor refuted by this source.

---

## Barnett: the fill, stated precisely (each point carries its quotes)

### B5-F1 The claim, and what "the outcome" is
- First pass said: (nothing stated in this form; the lead asked for the fill)
- Mark: confirmed
- Source: barnett; Sections I-II; PDF pp. 1-5 (printed pp. 422-426)
- Quote: "A simple yet powerful consequentialist case for voting can be made."
- Quote: "the rationality of voting can be proven to hold given two conditions: a stakes condition and a chances condition."
- Quote: "Suppose you’re eligible to vote in a large, upcoming election. On the ballot are two candidates: Daisy and Donald."
- Quote: "a vote that breaks a tie (when the number of voters is odd) or causes a tie (when the number of voters is even)."
- Note: the claim is that, for a voter who cares only about the public good (B5-03), voting for the better of two candidates has an expected social benefit greater than the cost whenever (i) the stakes condition b > 2c and (ii) the chances condition d ≥ 1/N hold; and that both are "often satisﬁed in typical electoral circumstances" (p. 424, lines 113-114 of text.txt, on PDF p. 3). "The outcome" is which of the two candidates is awarded the single election, with an exact tie counted as an outcome whose value is the average of the two ("½ × B", B5-04). "A vote that changes the outcome" is one that breaks a tie (N odd) or causes a tie (N even). The title phrase is not defined further. Both steps are expected-value reasoning: "we will make the standard decision-theoretic assumption that an act is rational if its expected beneﬁts exceed its costs" (p. 425).

### B5-F2 How d is defined and bounded
- First pass said: (partly at lines 88, 140, 275)
- Mark: confirmed
- Source: barnett; PDF p. 5 (printed p. 426) for the definition; PDF p. 6 (printed p. 427) for the chances condition; Appendix A PDF pp. 20-21 (printed pp. 441-442) for the formal definition
- Quote: "Second, there’s the probability that your vote for Daisy is decisive, which we can call d."
- Quote: "Chances condition: The probability of casting the deciding vote is at least one divided by the number of citizens (in short: d ≥ 1/N)."
- Quote: "Let t stand for what might be called a triggering number—that is, the number of votes the leading candidate would have to earn, from your fel- low citizens, in order for your vote to be decisive."
- Quote: "Let L stand for the number of votes, from that group of N− citizens, earned by the leading candidate."
- Note: formally (Appendix A, PDF p. 21, checked on the image) d = P(L = t), where L is the number of the other N⁻ = N − 1 citizens' votes that go to the leading candidate and t = ⌊N⁻/2⌋ (voting for the leader) or ⌈N⁻/2⌉ (voting against the leader); the probability is an ex ante probability over the others' votes (u is called "the ex ante probability", fn 21 speaks of "our credence"), never conditioned on your own act. d is a lower bound, not an estimate: d ≥ 1/N, or d > 10u/N for large N, derived only from Partial Unimodality + Narrow Upsets + the underdog having at least a 10% chance + full turnout of the others (B5-05 to B5-07). Barnett gives no point estimate of d for any real election. The only point values he reports for d under the binomial model are in Appendix B: random voting with 500,000 others, "about 1 in 1,250" (pp. 430 and 444; see "Found" item 6 for a recomputation), and the Brennan-example figures (B5-08).

### B5-F3 The assumptions he names
- First pass said: (partly: line 140 "two assumptions he names")
- Mark: confirmed
- Source: barnett; Section II PDF pp. 4-5 (printed pp. 425-426); Section IV PDF pp. 12-16 (printed pp. 433-437); footnote 13 PDF p. 8 (printed p. 429)
- Quote: "In thinking through your predicament, we will make two simplifying assumptions, which will inform our discussion."
- Quote: "To make the problem tractable, we will make the standard decision- theoretic assumption that an act is rational if its expected beneﬁts exceed its costs."
- Quote: "Strictly speaking, for voting to be rational, it must have a higher expected value than all possible alternative courses of action. For simplicity, the only options we will consider are voting and abstaining"
- Quote: "To the extent that we are interested in (2), we are entitled to leave aside worries about voters’ actual beliefs and simply assume that our imagined voter is a well-informed citizen."
- Note: the full list as the paper states it. (1) Rationality = expected benefit exceeds cost (p. 425). (2) The voter is a consequentialist who weighs everyone's interests equally including their own (p. 425). (3) Only two options, vote or abstain (fn 9, p. 425); the voter will vote for Daisy "provided that you vote at all" (p. 425). (4) Two candidates, one election (p. 424: "On the ballot are two candidates: Daisy and Donald"), an electorate of N citizens (p. 427). (5) An exact tie goes to each candidate with equal probability (p. 426). (6) B = b × N, b the same average for everyone affected, N the number of citizens (pp. 426-427). (7) Everyone else votes, for one of the two candidates (pp. 433, 436, 441). (8) The two modelling assumptions, Partial Unimodality and Narrow Upsets (p. 434). (9) The underdog has at least a 10% chance of winning, with N large (pp. 429, 433, 436, 442). (10) The voter is well-informed: fn 13 (p. 429) separates "(1) Is it rational to vote, given voters’ actual beliefs?" from "(2) Is it rational to vote, given the beliefs voters ought, epistemically, to have?", and Barnett takes (2) (quote above).

### B5-F4 What the paper does not treat (absence claims; each checked by grep of text.txt)
- First pass said: (nothing)
- Mark: confirmed
- Source: barnett; whole text
- No quote (absence claim). Evidence: `grep -n -i "electoral college\|swing\|recount\|correl\|evidential\|turnout\|abstain"` shows "Electoral College" only in two bibliographic notes (fn 15-16, p. 430, about Banzhaf; the main text on p. 430 mentions that "residents of different states" have unequal power in presidential elections only as an example of the voting-power literature), "turnout" only in fn 7 (Downs's paradox of voter turnout), "abstain/abstained" only in the vote-or-abstain option set (pp. 425-426) and in "no one will abstain, except maybe you" (p. 433), and no hits for recount, evidential or correlat*; "causal" appears only in cited titles.
- Note: so the paper has: no Electoral College or state-level model (Brennan's example is a single national popular vote of 122,293,322); no more than two candidates; no recount, runoff or court rule beyond the equal-chance tie; no partial turnout in the argument; no correlation between voters (independence appears only in the binomial model he criticises: "independent coin toss", pp. 430-431, 440, 444); no evidential-decision-theory discussion; no value of the voting cost c; no measured b. The "held fixed" question (fork 9) is therefore not addressed: his wording is counterfactual (B5-04) and his assumptions are on the distribution of the others' votes alone.

---

# Part 2. Kagan (2011)

### K5-01 Identity and pages
- First pass said: Kagan (2011), "Do I make a difference?", *Philosophy & Public Affairs* (line 155); "pp. 119, 140"
- Mark: confirmed
- Source: kagan; https://pdf.stafforini.com/kagan-2011-make-difference.pdf; PDF p. 1 (printed p. 105)
- Quote: "SHELLY KAGAN Do I Make a Difference? papa_1203 105..141"
- Quote: "© 2011 Wiley Periodicals, Inc. Philosophy & Public Affairs 39, no. 2"
- Note: 37 PDF pages = printed 105-141. The title is "Do I Make a Difference?" (title case in the print); the first report's sentence-case title is cosmetic.

### K5-02 "In triggering cases there is a small chance that the act makes a big (morally relevant) difference"
- First pass said: Kagan: "In triggering cases there is a small chance that the act makes a big (morally relevant) difference" (pp. 119, 140) (line 155).
- Mark: corrected
- Source: kagan; Section VII; PDF p. 16 (printed p. 120)
- Quote: "In triggering cases there is a small chance that the act makes a big (morally relevant) difference."
- Quote: "And while the chance is only a small one, the difference it makes, if it does make a difference, is sufficiently great to guarantee that the expected utility of the given act is negative."
- Correction: [page only] "pp. 119, 140" → this quote is on printed p. 120 (PDF p. 16). Printed p. 119 (PDF p. 15) is where Section VII begins ("Let us start by considering the (pure) triggering cases", with the answer "It is unlikely, but possible, that it did make a difference—that my own act was the triggering act"); the first statement of "triggering" is printed p. 118 (PDF p. 14).
- Note: the "guarantee" in the second quote rests on Kagan's stipulation that the total bad result exceeds the total good result: "In the kinds of cases that concern us, it is always true that B > g" (fn 4, p. 114), so the act's expected utility g/n + B/n is negative. [I] The structure (a small chance times the whole total) parallels Barnett's EB = ½·b·N·d with d ≥ 1/N, where b·N is the whole total and the chance is about 1/N.

### K5-03 The chicken example: a 1 in T chance of triggering T chickens; "has a negative expected utility"
- First pass said: with a 1-in-T chance of triggering an order of T chickens, the act "has a negative expected utility" (line 155).
- Mark: corrected
- Source: kagan; Section VIII; PDF p. 20 (printed p. 124) for the T result; PDF p. 16 (printed p. 120) for the phrase "has a negative expected utility" (general triggering cases)
- Quote: "I do know that whatever it is, I have a 1 in T chance (more or less) of triggering the suffering of another T chickens (more or less)."
- Quote: "my act of purchasing a chicken still has an expected disutility equivalent to one chicken’s suffering."
- Quote: "That is, my act has a negative expected utility."
- Quote: "the expected utility of my act is (1/n)(B + g/n) + ([n–1]/n)(0 + g/n), where B stands for the"
- Correction: [page and wording] the phrase "has a negative expected utility" is printed p. 120 (general triggering argument, formula in the 4th quote, which the text then reduces to g/n + B/n). The chicken-T passage is printed p. 124 and says the "net expected utility of my purchase remains negative" (after subtracting the pleasure of eating the chicken). So the pages are 120 and 124, not "119, 140".
- Note: in Kagan's notation B means the total (additional) bad results and g the total good results (p. 120: "B stands for the (total) additional bad results, and g stands for the (total) additional good results"), not a per-person or "benefit" B. As printed the expression "g/n + B/n" is negative only if B is read as a negative quantity larger in size than g; the text calls this "B is greater than g". The chicken case's arithmetic is (1/T) × T chickens = one chicken's suffering (p. 124).

### K5-04 "Collective action cases are all triggering cases"
- First pass said: "Collective action cases are all triggering cases" (pp. 119, 140) (line 155).
- Mark: confirmed
- Source: kagan; Section XVI; PDF p. 36 (printed p. 140)
- Quote: "Collective action cases are all triggering cases, though they differ, of course, in their details."
- Quote: "although it may not be very likely that my act will make a difference, there is a great enough chance that it will, so that—given the difference that it might make—my act will have negative expected utility."
- Note: the conclusion depends on Sections XI-XV (pp. 129-140), where Kagan argues that "imperceptible difference" cases cannot exist: "we should deny their existence" (p. 130). That argument concerns perceptible pain and is not about elections.

### K5-05 "Do I make a difference? I might."
- First pass said: "Do I make a difference? I might." (pp. 119, 140) (line 155).
- Mark: corrected
- Source: kagan; Section XVI, last line of the paper; PDF p. 37 (printed p. 141)
- Quote: "Do I make a difference? I might."
- Correction: [page only] "pp. 119, 140" → printed p. 141 (PDF p. 37), the last line of the paper.
- Note: fn 15 on the same page limits the conclusion: "the consequentialist’s appeal to expected utility might itself be questioned (see note 8)." Note 8 (p. 120): "For the purposes of the present paper I will simply take for granted the familiar assumption that consequentialism does indeed condemn acts with negative (incremental) expected utility."

### K5-06 Voting is not discussed in the text
- First pass said: "Voting is not discussed in the text (extractor)" (line 155).
- Mark: confirmed
- Source: kagan; whole text, PDF pp. 1-37 (printed pp. 105-141)
- No quote (absence claim). Evidence, run on `SRC/kagan/text.txt` (1,567 lines): `grep -n -i "vot\|election\|ballot"` returns **no lines** (exit status 1). A wider check of whole words and stems (vote*, voter*, voting, election*, elect*, ballot*, poll*, politic*, democra*, referend*, candidate*, pivot*, decisive, swing, tie) gives only: "pollut-" words (38 lines: the factory and sky pollution examples), and one "decisive" at printed p. 128 (PDF p. 24, text.txt line 1011), in a parenthesis about the effect a purchase may have in encouraging other people to eat chicken: "These effects are, of course, often significant, and may be decisive."
- Note: so every hit for the report's patterns is either "pollute/pollution" or that one "decisive" about encouraging others. The paper mentions no election, no vote, no ballot, no tie. Kagan's own examples are factory pollution, a fishing village, buying chickens, and a torture machine with a thousand switches. The paper does cite Parfit's *Reasons and Persons* (Chapter 3 is the debt: fn 1, p. 105; Sections 25, 26, 29 in fns 3, 5, 6, 7), but Barnett's fn 1 (p. 423) puts Parfit's voting remarks at pp. 73-4 of that book, and Kagan never connects the two. Any link from Kagan to voting is the first report's inference [I] (line 157).

### K5-07 The first report's inference (line 157): "3.1's maths read morally"
- First pass said: [I] "the expected effect of your act equals (chance you trigger) × (size of what the trigger changes)... the tiny p can be matched by a large B" (line 157).
- Mark: confirmed
- Source: kagan; PDF p. 19 (printed p. 123) for the two quotes; PDF pp. 15-16 and 20-24 (printed pp. 119-120 and 124-128) for the rest
- Quote: "Thus, you have a 1/25th chance of affecting the suffering of 25 chickens."
- Quote: "In terms of chicken suffering, then, the expected disutility of your act is one chicken’s worth of suffering."
- Note: the factual base (chance × size) is confirmed; the inference goes beyond the source in two ways. (a) where Kagan's chance 1/T comes from: not from a distribution of other people's behaviour but from indifference over the size of the buyers' "cohort" modulo T: "in the absence of any special information about the situation, I must assume that a cohort that is an exact multiple of 25 is no more likely or less likely than any of the other twenty-four possibilities" (p. 126, quoted in K5-F1). The thresholds recur every T purchases, so the chance of being at one is 1/T. An election has a single threshold (a tie or a one-vote deficit), so no 1/T chance is available from Kagan's reasoning, and he says nothing about how to get one. (b) Kagan's reasoning is counterfactual with the others' acts fixed ("each one of us can correctly say that had he acted differently, the results would have been better", p. 125, PDF p. 21) and, when you do know the others' total, the chance goes to zero or one (p. 128, K5-F1). [I] The report's "does not contradict the owner's setup" reading is consistent with both points but is not stated by Kagan.

## Kagan: what he argues about triggering (the fill)

### K5-F1 Kagan's argument, in his words, with pages
- First pass said: (the lead asked for the fill)
- Mark: confirmed
- Source: kagan; whole paper; PDF and printed pages given in the Note
- Quote: "The problem, in effect, is this: consequentialism condemns my act only when my act makes a difference."
- Quote: "it seems more accurate to suggest that most acts make no difference, but some single act makes a great deal of difference."
- Quote: "The real question, therefore, is not whether I will be the 25th (or 50th, or 75th . . .) person to buy a chicken,"
- Quote: "but rather whether I will be part of a cohort of exactly 25 (or 50, or 75 . . .) chicken purchasers."
- Quote: "But in the absence of any special information about the situation, I must assume that a cohort that is an exact multiple of 25 is no more likely or less likely than any of the other twenty-four possibilities"
- Quote: "In such a case I know that my act makes no difference, and results will not be any better if I refrain from buying a chicken."
- Note: the structure, with printed (PDF) pages. (1) Problem (pp. 107-108; PDF 3-4): "collective action" cases, where enough people doing an act produces bad results although no individual act seems to make a difference; since "consequentialism condemns my act only when my act makes a difference" (p. 108), consequentialism seems to fail. (2) Four proposed fixes he will not use (pp. 111-114; PDF 7-10): universalizability, rule consequentialism, group duties, and "bookkeeping" shares of 1/n. (3) A fifth, imperceptible harms, is rejected as incomplete (pp. 114-117; PDF 10-13). (4) Two types of case (pp. 117-119; PDF 13-15): imperceptible-difference cases, and triggering cases where "some single act works as a trigger" (p. 118). (5) Triggering cases: the chance that my act is the trigger is small but the difference it makes is large, so its expected utility is negative; formula on p. 120; fn 8 (p. 120) notes the assumption that consequentialism condemns acts with negative incremental expected utility, and that "condemns" is chosen over "prohibits". More complicated cases with several triggers are covered in a parenthesis: "there is, of course, a correspondingly greater chance that your act will be one of the triggering acts" (p. 121). (6) The chicken example (pp. 121-124; PDF 17-20): the butcher orders 25 chickens when 25 have been sold, you have a 1 in 25 chance, expected disutility is one chicken, T unknown but "more or less" a 1 in T chance of T chickens. (7) The refinement (pp. 125-128; PDF 21-24): whether your act matters depends on whether the total number of buyers is an exact multiple of T, not on your place in line (p. 127: the important question concerns the size of your cohort rather than your place in the butcher's line); with no special information, equal chance over the T residues, so 1/T (p. 126); fn 10 (p. 127) allows cases where each person "objectively has a 1/n chance of triggering ... regardless of what others do". (8) The exception (p. 128; PDF 24): if you know that the others will total 66 buyers and that orders trigger at multiples of 25, "the expected disutility of my purchasing a chicken is actually zero" and consequentialism cannot condemn the purchase. (9) Effects on others (e.g. encouraging other buyers) are "not our concern here, so I leave them aside" (p. 128). (10) Imperceptible-difference cases cannot exist (Sections XI-XV, pp. 129-140; PDF 25-36), by a reductio about a torture victim's pain reports; so "Collective action cases are all triggering cases" (p. 140) and "I conclude, therefore, that there is no need to go beyond familiar consequentialist theory" (p. 141). The question in the title gets "I might" (p. 141).
- Note: Kagan's argument is about when an act is condemned for the harm it risks, not about benefits to oneself or others from voting. His "chance" is the chance that the act falls on the triggering side, given that the agent does not know the others' total (pp. 126, 128); where the agent knows the others' total the chance is 0 or 1 (p. 128). [I] That makes it an epistemic chance, which is my reading, not his label (he does not use the term).

---

# Part 3. The JESP page

### J5-01 What the page is: title, authors, date
- First pass said: "A published reply (JESP)", "Barnett's reply authors (JESP page shows none)", URL https://jesp.org/index.php/jesp/article/view/2915 (lines 140, 330).
- Mark: corrected
- Source: jesp; https://jesp.org/index.php/jesp/article/view/2915 (redirects, see header of this file); top of the page
- Quote: "The Case for Voting to Change the Outcomes Is Weaker Than It May Seem: A Reply to Zach Barnett"
- Quote: "Amir Liron and David Enoch Volume 26, Number 1, November 2023, Pages 204–216"
- Correction: "(JESP page shows none)" → the page names two authors, Amir Liron and David Enoch (the page's heading reads "Amir Liron and David Enoch", then the volume line).
- Note: the page is a DISCUSSION article in the *Journal of Ethics and Social Philosophy* (JESP) vol. 26, no. 1, November 2023, pp. 204-216 (the page's meta tags: citation_firstpage 204, citation_lastpage 216, citation_publication_date 2023/11/01, DOI https://doi.org/10.26556/jesp.v26i1.2915, ISSN 1559-3061, journal "Journal of Ethics and Social Philosophy"). It is an abstract page: "Abstract" plus lists of unrelated articles ("Related Articles"), no body text; the footer "© 2026" is the site's, the paper's copyright line reads "Copyright © 2023 Amir Liron and David Enoch". The PDF address given in the page's own meta tag is https://www.jesp.org/pdf/36346f73-90e0-81d0-86e6-d03e516d0052 (not fetched; the lead's call). The page also says "This paper has not yet been cited." and states a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 licence.

### J5-02 "may apply to significantly less real-life scenarios than he suggests"
- First pass said: the reply says his reasoning "may apply to significantly less real-life scenarios than he suggests" (line 140).
- Mark: confirmed
- Source: jesp; abstract paragraph, last sentence
- Quote: "Barnett’s reasoning, we conclude, may apply to significantly less real-life scenarios than he suggests."
- Note: the full sentence is in the authors' words, the abstract's last sentence.

### J5-03 "too quick on one key premise"
- First pass said: he is "too quick on one key premise" (the extractor could not see which) (lines 140, 298).
- Mark: confirmed
- Source: jesp; abstract paragraph
- Quote: "However, Barnett is—we argue in this paper—too quick on one key premise, and once this is noticed, it becomes unclear how often Barnett’s reasoning can point to a justification of voting to change the outcomes."
- Note: the phrase is confirmed; which premise is not said (see J5-04). The sentence says the effect of the flaw is that "it becomes unclear how often" the reasoning supports voting, i.e. a claim about frequency, not an invalidity claim. See J5-04 and J5-05.

### J5-04 Which premise (the extractor could not see)
- First pass said: the extractor could not see which premise (line 140); "The JESP reply disputes Barnett on 'one key premise' the extractor could not identify." (line 298)
- Mark: unread
- Source: jesp; abstract only
- No quote (nothing to quote: the abstract does not identify the premise).
- Note: to settle it the lead needs the reply's PDF (address in J5-01's note). Do not infer it from the abstract: candidates are the chances condition (d ≥ 1/N, i.e. Partial Unimodality, Narrow Upsets or the 10% condition), the stakes condition (b > 2c) or the full-turnout assumption; the abstract names none.

### J5-05 What the abstract says about Barnett, beyond the two quotes the extractor gave
- First pass said: (line 140: "A published reply (JESP) says his reasoning ... "; line 298 sets it against Barnett on "how large p is")
- Mark: corrected
- Source: jesp; abstract paragraph, sentences 1 to 4
- Quote: "Because you are highly unlikely to cast the deciding vote in the next elections, it is often said that you don’t have a reason to vote in order to change the outcomes."
- Quote: "He shows how it follows, from rather conservative assumptions, that in many real-life cases the expected social value of voting is higher than its cost."
- Quote: "Barnett is successful, we believe, in showing that the commonly held belief—that voters do not have a reason to vote in order to change the outcomes—is way too hasty."
- Correction: [omission and classification] the first report presents the reply as a dispute that sits under "how large p is" (line 298, item 2). The abstract (a) agrees with Barnett's main claim in part ("Barnett is successful ... in showing that the commonly held belief ... is way too hasty") and states his result as "the expected social value of voting is higher than its cost" in "many real-life cases"; (b) does not say the disputed premise concerns p. [I] The classification under p is the first report's, not the page's.
- Note: Liron and Enoch use "the expected social value of voting" as their summary of Barnett (consistent with B5-F1).

---

# Part 4. Goldman 1999, Cambridge page

### G5-01 Identity, date, pages
- First pass said: Goldman 1999, *Social Philosophy and Policy*, "Why citizens should vote: a causal responsibility approach" (lines 126, 146, 324, 335).
- Mark: confirmed
- Source: cup_goldman; the page's canonical URL (see header); the "Information" block and the head of the page
- Quote: "Social Philosophy and Policy , Volume 16 , Issue 2 , Summer 1999 , pp. 201 - 217"
- Quote: "Why Citizens Should Vote: A Causal Responsibility Approach* | Social Philosophy and Policy | Cambridge Core"
- Quote: "Published online by Cambridge University Press: 13 January 2009"
- Note: author "Alvin I. Goldman", affiliation "Philosophy, University of Arizona"; DOI 10.1017/S0265052500002442; "Copyright © Social Philosophy and Policy Foundation 1999"; page type "abs" (abstract page). Barnett's fn 6 (p. 424) cites the same paper as "Social Philosophy and Policy 16 (2001): 201–17" and calls it "A Causal Responsibility Account": see G5-F3. The Cambridge page, not Barnett, is the source for year 1999.

### G5-02 The "abstract wording" (an Extract that is the paper's first paragraph)
- First pass said: Goldman's own abstract: two readings of "why should citizens vote?", "in a prudential sense, and in a moral (or quasi-moral) sense", "mainly try to answer the moral version" (line 146).
- Mark: confirmed
- Source: cup_goldman; the section labelled "Extract" (also the page's `citation_abstract` meta tag)
- Quote: "Why should a citizen vote? There are two ways to interpret this question: in a prudential sense, and in a moral (or quasi-moral) sense."
- Quote: "I shall mainly try to answer the moral version of the question, but my answer may also, in some circumstances, bear on the prudential question."
- Quote: "Under the first interpretation, the question asks why—or under what circumstances—it is in a citizen's self-interest to vote."
- Note: the page's label is "Extract", and its last sentence ("Before proceeding to my own approach, let me briefly survey alternatives in the field.") shows it is the opening paragraph of the article's body, not a separately written abstract. So "Goldman's own abstract" is, more exactly, "the first paragraph of Goldman's article". The first interpretation is "self-interest", which the page explicitly ties to prudence.

### G5-03 Footnote 39: causal credit and the swing-voter probability
- First pass said: footnote 39: a non-swing voter can still raise the probability of earning "causal credit", which is "no longer linked to the probability of being a swing voter" (extractor) (line 146).
- Mark: confirmed
- Source: cup_goldman; "References" list, note 39
- Quote: "Strictly, the causal responsibility approach I propose could be subsumed under the expected-consequences, or rational-choice, perspective."
- Quote: "In addition to the outcomes being different, the probability of getting a more preferred outcome from voting than from abstaining is no longer linked to the probability of being a swing voter."
- Quote: "Even if one is not a swing voter, one's act of voting can raise the probability of one's earning more causal credit for a superior candidate's victory and of avoiding causal discredit for such a candidate's loss."
- Quote: "Since the outcomes have a moral nature, however, it may be controversial whether the choices should be considered a matter of “prudence” or “self-interest.” I do not try to address this issue here."
- Note: the report's wording attaches "no longer linked..." to the probability of earning causal credit; the footnote attaches it to "the probability of getting a more preferred outcome from voting than from abstaining" in a choice matrix whose outcomes include the states of being "a partial cause of a good electoral result" and "deserving moral credit (or discredit)". The report missed the first sentence: Goldman himself says "the approach I favor may just be a special case of the rational-choice framework", with the outcomes changed, and he declines to say whether this makes it prudential.

### G5-04 Footnote 25: the scalar treatment fails with more than two candidates
- First pass said: Goldman's footnote 25 (a scalar "force" treatment "doesn't work with three or more candidates", extractor) (line 107).
- Mark: corrected
- Source: cup_goldman; "References" list, note 25
- Quote: "In election cases, however, at least in races where there are more than two candidates, the scalar approach will not work."
- Quote: "John Staddon points out that these forces can be treated as scalars rather than vectors, because there is just one dimension of movement, and forces can be treated as either positive or negative along this dimension."
- Correction: [quote wording] "doesn't work with three or more candidates" → "at least in races where there are more than two candidates, the scalar approach will not work"; "more than two candidates" is the same set as "three or more", and the source hedges with "at least". The "force" is the footnote's own term ("these forces"; "the term 'vector' is here used loosely to depict an interplay of conflicting forces").
- Note: the footnote credits the scalar/vector remark to John Staddon, not to Goldman. Footnote 5 quotes Meehl on an "obligation vector"; together they support the report's second-hand "vectoral model" (Ridge) as a term in the paper, but the body is not visible, so I have not confirmed how the model works.

### G5-05 Footnote 1: Riker and Ordeshook's p = 10⁻⁸
- First pass said: (the lead's batch note: "footnote 1 on Riker & Ordeshook's 10⁻⁸"; the report has Dowding's "made it 10⁻⁸" at line 274 but nothing from Goldman)
- Mark: confirmed
- Source: cup_goldman; "References" list, note 1
- Quote: "William Riker and Peter Ordeshook have estimated the probability of an individual voter being decisive to the outcome of a U.S. presidential election as p = 10–8–that is, a 1 in 100,000,000 chance."
- Quote: "Downs formulates matters in terms of the “party differential” rather than the differential between the two individual candidates, but this difference is incidental."
- Note: this is Goldman's description of Riker & Ordeshook (APSR 62, 1968, p. 25 as cited), not R&O's text. The exponent is printed "10–8" with an en dash (the minus sign), and the gloss "a 1 in 100,000,000 chance" fixes it as 10⁻⁸. It matches Dowding's note quoted at line 274 and Edlin et al.'s fn 3 range ("10⁻⁷ or 10⁻⁸") at line 270. Downs's "party differential" (line 74) is also confirmed by the second quote as Goldman describes it.

### G5-06 The body of the paper is paywalled
- First pass said: "Body paywalled" (line 146); "Goldman (1999) body ... Cambridge abstract page only" (line 324).
- Mark: confirmed
- Source: cup_goldman; "Access options"
- Quote: "Get access to the full version of this content by using one of the access options below."
- Quote: "Article purchase Temporarily unavailable"
- Note: also on the page, "Cited by ... No CrossRef data available." The page's `citation_pdf_url` (a Cambridge PDF address ending S0265052500002442a.pdf) is in the raw HTML; it is not fetched and would presumably be behind the same access control.

### G5-07 [I] "Goldman's 'prudential' reading is the one that coincides with 3.1"
- First pass said: Goldman's "prudential" reading is the one that coincides with 3.1 (the pivotality framework) (line 150).
- Mark: unread
- Source: cup_goldman; the visible text (extract + footnotes) only
- No quote (nothing visible states it).
- Note: the visible text neither confirms nor refutes this. What is visible: the first paragraph says the prudential question asks "under what circumstances—it is in a citizen's self-interest to vote" (G5-02); footnote 1 (G5-05) describes "the economic approach" with p = 10⁻⁸; footnote 39 (G5-03) calls the "standard analysis" the expected-consequences one in which the probability is "linked to the probability of being a swing voter", and says his own approach differs in the outcomes but could be fitted into the same framework. [I] That is consistent with the report's reading but it is not stated in the visible text.

## Goldman: what text of the paper is on the Cambridge page, and what is not (the fill)

### G5-F1 Visible and not visible
- First pass said: (the lead asked for the list)
- Mark: confirmed
- Source: cup_goldman; the whole page
- Quote: "Why should a citizen vote? There are two ways to interpret this question: in a prudential sense, and in a moral (or quasi-moral) sense."
- Quote: "Get access to the full version of this content by using one of the access options below."
- Note: **Visible (all verbatim on the page):** (1) title, author, affiliation, journal, volume 16 issue 2, "Summer 1999", pp. 201-217, DOI, online date 13 January 2009 (G5-01); (2) one paragraph labelled "Extract", the article's first paragraph, 6 sentences (G5-02); (3) the "References" block: footnotes **numbered 1 to 39, all present with no gap** (a count of 39 on the page; whether the printed paper has more is not shown), with the full text of each note, many with only a bibliographic citation. Those footnotes are the only part of the argument visible. **Not visible:** the article body after its first paragraph (the page has no section headings, no argument, no examples, no conclusion); the paper's own bibliography apart from the notes; the page numbers inside the paper (the notes carry no page markers); the body references that the notes number.
- Note: what the 39 footnotes disclose about the body (not the body itself): note 1 Riker-Ordeshook p = 10⁻⁸, Downs's party differential; note 2 Parfit pp. 73-75; notes 4-5 Meehl's "prima facie obligation or obligation vector"; notes 8, 11-16, 28 Lewis on causation and overdetermination (the example: "If the ten pushings had not occurred, would no pushings have occurred? Not obviously. Perhaps five pushings would still have occurred, which would have been sufficient to free the car", note 16); notes 17-20 Mackie's INUS; note 21 "I assume an election with a single race"; note 22-24 political information; note 25 vectors and scalars; note 26 influence by persuading others is set aside; note 30 the electoral college "involves a two-step system"; note 33 team spirit; note 38 Holocaust bystanders; note 39 rational-choice reading (G5-03). None of the 39 notes states a formula for the value of a vote.

### G5-F2 Other footnotes that bear on the fork points
- First pass said: (not covered)
- Mark: confirmed
- Source: cup_goldman; "References" list, notes 9, 20, 26
- Quote: "And a decision to abstain rather than vote could change the outcome from a victory for one candidate to a tie—perhaps requiring a run-off election."
- Quote: "In the context of voting, however, we do not need to worry about probabilistic causation. Wherever an electoral outcome occurs, some set of votes is sufficient for the outcome."
- Quote: "There may be ways to influence the outcome above and beyond one's personal vote, for example, by persuading other voters. But this goes beyond the present subject."
- Note: note 9 treats a tie as a different outcome (possibly a run-off) and notes that "even switching a vote from one candidate to another can result in a tie, when the number of votes is even" (the same page), which bears on the tie-rule fork (the report's lines 94, 305): Goldman does not use a coin; he allows a run-off. Note 20 says causation is non-probabilistic in an election. Note 26 matches the owner's "all other contexts the same" in setting persuasion of others aside.

### G5-F3 What Barnett says about Goldman, and a disagreement on the year
- First pass said: (not covered)
- Mark: confirmed
- Source: barnett; fn 6; PDF p. 3 (printed p. 424); and cup_goldman G5-01
- Quote: "to share in a winning effort"
- Quote: "Social Philosophy and Policy 16 (2001): 201–17"
- Note: Barnett's fn 6 lists Goldman (with Tuck) among those who "have sought to defend voting in other ways" and describes the aim as "to share in a winning effort"; it cites volume 16 as 2001, pages 201-17. Cambridge's page says Summer 1999 for the same volume and pages. The year the site shows for Goldman should be 1999 (the Cambridge page and the first report agree) unless a reader of the printed volume finds otherwise; Barnett's 2001 is a conflict between two sources, noted, not resolved.

---

# Corrections table

| # | Old (first pass) | New | Source and location |
|---|---|---|---|
| 1 | Barnett: "d ≥ 1/N when both candidates have at least a 10% chance (p. 432)" [page; conditions omitted] | The italic thesis sentence is on printed p. 433 (PDF p. 12), beginning at the foot of p. 432; first stated printed p. 429 (PDF p. 8); proved for N = 1,000,001 on pp. 436-437 (PDF pp. 15-16); general form in Appendix A, pp. 441-442. Also missing from the report: full turnout of the others (pp. 433, 436, 441), large N (p. 442), and the two modelling assumptions | barnett B5-05 |
| 2 | Barnett's B: "the net social benefit of having Daisy rather than Donald in charge" (as a quote) [quote wording] | "the net social benefit associated with having Daisy rather than Donald in charge" (printed p. 426, PDF p. 5) | barnett B5-02 |
| 3 | Kagan: "In triggering cases there is a small chance that the act makes a big (morally relevant) difference" at p. 119 [page only] | printed p. 120 (PDF p. 16) | kagan K5-02 |
| 4 | Kagan: with a 1-in-T chance of T chickens the act "has a negative expected utility" (pp. 119, 140) [page and wording] | the phrase "has a negative expected utility" is printed p. 120; the chicken-T passage is printed p. 124 (PDF p. 20) and says "net expected utility of my purchase remains negative" | kagan K5-03 |
| 5 | Kagan: "Do I make a difference? I might." (pp. 119, 140) [page only] | printed p. 141 (PDF p. 37), the paper's last line. ("Collective action cases are all triggering cases" is on p. 140, PDF p. 36: confirmed) | kagan K5-05, K5-04 |
| 6 | Goldman fn 25 as "doesn't work with three or more candidates" [quote wording] | "at least in races where there are more than two candidates, the scalar approach will not work"; the scalar/vector remark is credited in the note to John Staddon | cup_goldman G5-04 |
| 7 | JESP: "Barnett's reply authors (JESP page shows none)" | Amir Liron and David Enoch; JESP vol. 26 no. 1, November 2023, pp. 204-216; DOI 10.26556/jesp.v26i1.2915 | jesp J5-01 |
| 8 | The reply is a dispute about "how large p is" (line 298) | The abstract agrees with Barnett in part ("way too hasty"), names no premise, and does not say the premise concerns p | jesp J5-05 |

---

# Unread and why

- **Which premise the JESP reply says Barnett is "too quick" on** (and everything else in the reply): the page has the abstract only; the reply's PDF is at https://www.jesp.org/pdf/36346f73-90e0-81d0-86e6-d03e516d0052 (the page's own `citation_pdf_url`). Needs the lead's fetch.
- **Goldman 1999, body of the paper** (including how the "vectoral model", "efficacious set" and any statement about the prudential reading work): paywalled on the Cambridge page; only the first paragraph and footnotes 1-39 are visible. G5-07 stays unread.
- **Ridge's quotations of Goldman** (line 145: "Non-swing voters in a massive election make causal contributions" etc.) and **Tuck / Amadae** (line 147): not in my sources; not checked.
- **Parfit, *Reasons and Persons*, pp. 73-75 and the reactor passage**: read only as quoted in Barnett (p. 439) and as cited by Barnett (fn 1, 32), Kagan (fns 1, 3, 5-7) and Goldman (fn 2). The quotation has "[. . .]" elisions, so the original is not checked.
- **Brennan's *Ethics of Voting* pp. 18-20 and Maring p. 245** (the $33 billion example and the $4.77 × 10^-2650 figure): read only as quoted in Barnett (pp. 423-424).
- **The SEP page** (Brennan's quoted passage): read only through Barnett's quotation (B5-16); the qualifier "under binomial models" at the report's line 139 is not checked here.
- **Mulligan & Hunter's direction of the binomial comparison** (line 140: they find close elections "more rare than the independent binomial model predicts"): Barnett's p. 432 says the empirical estimates he lists, which include Mulligan & Hunter and Gelman, King & Boscardin (his fn 25), "all turn out to be considerably greater than the binomial model predicts". Both are about "the binomial model" but the baselines may differ (a fair coin versus Brennan's 50.5% case). I could not settle it: the Mulligan-Hunter text is not in my batch.

# Found that the first pass missed

1. **The JESP page is a named, dated, partly agreeing reply** (Liron and Enoch, Nov 2023). It says "Barnett is successful, we believe, in showing that the commonly held belief ... is way too hasty" and that his result is that "in many real-life cases the expected social value of voting is higher than its cost" (J5-05). The first report says no authors were shown and files the reply under "how large p is".
2. **Barnett's ½ sits outside his d, and his d is a single event.** B is the gain if the better candidate wins; EB = ½·B·d; d = P(the others stand exactly at the triggering number); with everyone else voting, only one of "others tied" and "others one short" is possible. The first report's p = ½[P(tie) + P(one behind)] equals ½·d only under that fixed-turnout condition (B5-15). The tie rule is an equal-chance assumption "for simplicity" ("perhaps a coin"), not a claim about real tie-breaking; Goldman's note 9 allows a run-off instead (G5-F2).
3. **Barnett's bound has conditions the first report leaves out**: full turnout of the other citizens (p. 433, p. 441), a large electorate (p. 442: false for N ≤ 20), Partial Unimodality and Narrow Upsets (p. 434), and the underdog's 10% chance. The $134.92 is ½b at d = 1/N with Brennan's stipulated $33 billion; the paper does not say the underdog has 10% in Brennan's example (B5-10). [M] b = $269.84, ½b = $134.92.
4. **Barnett never fixes the voting cost c** and never measures b; "b > 2c" is a condition, with illustrations that are either costs (Iraq and Afghanistan) or unnumbered (tax relief). His third example ($500 per citizen from a 5% more efficient budget, pp. 428-429) is omitted by the report (B5-11).
5. **Barnett's objector concedes the national probability is tiny**: "(maybe 1/100,000,000 for a national election in the United States)" (PDF p. 17, printed p. 438; text.txt line 745-746), and Barnett does not deny it. [M] For N = 122,293,322, 1/N = 8.18 × 10⁻⁹. So his bound is about the same size as Riker & Ordeshook's 10⁻⁸ (Goldman fn 1, G5-05) and below the forecast-based national figures the first report cites (1 in 10 million, 1 in 60 million; those are other batches' sources). [I] The report's "tension" is therefore not about the size of d for a national election but about whether the benefit B scales with N (Barnett) or not (self-only B). Barnett's bound is for one national popular vote; he has no state-level model, so the "closer to 1 in a billion" state values the report cites are not tested by it.
6. **Internal inconsistencies in Barnett's appendix** [M]: (a) pp. 430 and 444 say random voting with 500,000 others gives "about 1 in 1,250", but the printed value 0.0011284 (which I recompute as 0.00112838) is 1 in 886, not 1 in 1,250; (b) fn 38 gives N = 122,293,222 where the text and fn 36 use 122,293,322; (c) the quoted Maring/Brennan figure $4.77 × 10^-2650 equals B × P(exact tie of 122,293,322 binomial voters) with no factor ½ (my recompute: B × P = 4.77 × 10^-2650; ½·B·P = 2.38 × 10^-2650), whereas Barnett's own EB has the ½. None of these affects the 2,650-order-of-magnitude point or the d ≥ 1/N argument. [M] I also recomputed Barnett's "$1,190,480.60" (r = 0.5): ½ × $33 bn × P(L = N/2) = $1,190,481 (difference is floating-point rounding).
7. **Barnett's d is an ex ante credence over the others' votes** ("ex ante probability", "credence", p. 442 and fn 21), the votes "not counting you"; his wording is counterfactual ("If you had abstained, there would have been a tie"); he never raises evidential decision theory or correlation among voters (B5-F4). The "held fixed: causal or evidential" fork (the report's item 9) is therefore not settled by this source.
8. **Kagan never mentions voting** (confirmed by grep with zero hits for "vot|election|ballot"), and his 1/T chance comes from indifference over the size of the buyers' cohort modulo T, with a rule that known totals make the chance zero (pp. 126, 128). He also sets aside influence on others (p. 128) and takes the expected-utility rule for granted (fn 8, p. 120; fn 15, p. 141). The report's pages for his quotes are off (p. 120, p. 124, p. 140, p. 141).
9. **Goldman's page offers more than the first report used**: the "Extract" is the first paragraph of the article, not an abstract; footnote 39 begins "Strictly, the causal responsibility approach I propose could be subsumed under the expected-consequences, or rational-choice, perspective"; footnote 1 gives Riker and Ordeshook's p = 10⁻⁸; notes 9, 20, 21, 26, 30 on ties, sufficiency, a single race, persuasion and the electoral college (G5-02, G5-03, G5-05, G5-F2). **Barnett cites the paper as 2001; Cambridge says Summer 1999** (G5-F3).
10. **Barnett's source identity**: the philosophersannual.org PDF is the P&PA typeset article (pp. 422-446), so its printed page numbers can be cited as P&PA 48(4) pages.

# Machine-check note

I ran my own check (script `SCRATCH/tools/verify.py`) on every `Quote:` line against the `text.txt` of the source named on that entry's Source line, after collapsing whitespace. Result: 106 quotes checked, 106 found, 0 not found. All 106 are also found with only whitespace collapsed (no Unicode normalisation needed), so the Barnett quotes keep the ﬁ/ﬂ ligature characters exactly as `text.txt` has them and the Kagan, JESP and Goldman quotes use the plain letters those texts have. No quote exceeds 40 words. Where a source breaks a word across lines with a hyphen, the quote keeps the hyphen and the space ("decision- theoretic", "fel- low") because that is what the whitespace-collapsed text contains. The same script reports, for each quote, the PDF page on which it was found; the PDF and printed pages given in the Source lines come from that report.
