# B6a: Coate & Conlin (`coate_conlin`) and Feddersen & Sandroni (`feddersen`)

Reader: Sonnet 5.5. No network used. Scratch work only under `SCRATCH/b6a/` (page-map script, PNG renders of PDF pages 5, 12, 13 of coate_conlin and 10, 11 of feddersen). Nothing in `/home/user/vote` touched.

## Sources read

| id | what the file is | size | read in full? |
|---|---|---|---|
| `coate_conlin` | NBER Working Paper 8720, Stephen Coate and Michael Conlin (Cornell / Syracuse), **January 2002**, JEL D72. Cover title is **"Voter Turnout: Theory and Evidence from Texas Liquor Referenda"**, not the AER title (see CC-01). | 48 PDF pages; `text.txt` 17,648 words (wc). Body = printed pp. 1-24, references pp. 25-26, appendix pp. 27-37 (proofs, density derivations, estimation procedure), then Tables 1-8 and Figures 1-2 on unnumbered pages. | Yes, every line of `text.txt` (lines 1-2340), including the appendix and all tables. Formulas on PDF pp. 5, 12, 13 checked on the page image. |
| `feddersen` | "A Theory of Participation in Elections", Timothy J. Feddersen (MEDS, Kellogg, Northwestern) and Alvaro Sandroni (Economics, Rochester; also MEDS, Kellogg), dated **April 2002** on its title page. A draft; same title as the AER 2006 article. | 45 PDF pages; `text.txt` 12,234 words. Model pp. 9-12, example pp. 19-29, existence p. 29-33, appendices pp. 36-41, references pp. 42-45. | Yes, every line of `text.txt` (lines 1-1575), including the appendix proofs. Display of the rule-to-action map checked on PDF p. 11 image. |

**Page-number convention (matters for every citation below).**
- `coate_conlin`: printed page = PDF page minus 1 for PDF pp. 3-38 (printed pp. 2-37). PDF pp. 1-2 (cover, abstract) and PDF pp. 39-48 (Tables 1-8, Figures 1-2) carry no printed number. The first report's page numbers are a mix: some are printed (p. 5, 9, 10, 23, 24), one is the PDF page (p. 3), one matches neither (p. 11).
- `feddersen`: PDF page = printed page (title page unnumbered; PDF p. 2 shows "2").

**URLs.** `hdr` files carry HTTP headers only, no URL. URLs below are the first report's: coate_conlin https://www.nber.org/system/files/working_papers/w8720/w8720.pdf ; feddersen https://www.kellogg.northwestern.edu/faculty/fedderse/homepage/papers/duty4-15-02.pdf . For feddersen, `hdr` last-modified and the PDF's own creation date are both 27 Sep 2002; the date printed inside is April 2002; "4-15-02" appears only in the file name, not in the paper.

**Untrusted-data check.** Both are ordinary academic PDFs. No embedded instructions, no spam. Nothing in either was followed as an instruction.

**[M] arithmetic.** The first report attributes no [M] computation to either paper, so there is nothing to recompute for rule 9. One check I did run, because the report's transcription of the payoff is ambiguous (CC-04): footnote 15 on printed p. 12 says the expected voting cost of a supporter who votes iff c_i <= gamma_s, with c_i uniform on [0, c], is the integral from 0 to gamma_s of c_i dc_i / c plus zero for the rest, = gamma_s^2 / (2c). Check: integral of x/c from 0 to g = g^2/(2c). Agrees.

---

# Part 1: marks on the first report's claims

## Coate & Conlin

### CC-01 What the downloaded file is (title, date, relation to the AER paper)
- First pass said: line 171 gives the entry "Coate & Conlin (2004), 'A group rule-utilitarian approach to voter turnout', AER 94(5): 1476-1504 (working paper https://www.nber.org/system/files/working_papers/w8720/w8720.pdf)"; lines 328 and 335 say the AER version was unread and the NBER working paper was read.
- Mark: corrected (as to the identity of the file read). The AER citation itself is unread (see CC-01b).
- Source: coate_conlin; https://www.nber.org/system/files/working_papers/w8720/w8720.pdf ; cover, PDF p. 1 (no printed number) and PDF p. 2 (abstract page)
- Quote: "VOTER TURNOUT: THEORY AND EVIDENCE FROM TEXAS LIQUOR REFERENDA"
- Quote: "Working Paper 8720"
- Quote: "January 2002"
- Correction: the paper read is titled "Voter Turnout: Theory and Evidence from Texas Liquor Referenda" (NBER WP 8720, January 2002), not "A group rule-utilitarian approach to voter turnout". The phrase "group rule-utilitarian" does not occur in the working paper (the words "rule-utilitarianism" and "rule utilitarian" occur only when it describes Harsanyi and Feddersen-Sandroni). So every statement in this file is about the January 2002 version.
- Note: Feddersen & Sandroni's reference list names this paper by the same working-paper title (feddersen PDF p. 42: "Coate, S. and M. Conlin (2002) “Voter Turnout: Theory and Evidence from Texas Liquor Referenda,” NBER Working Paper No.w8720."). Whether the AER 2004 version changed the model, the data count, or the numbers is unread.

### CC-01b AER 94(5): 1476-1504, 2004 citation
- First pass said: line 171, "AER 94(5): 1476-1504" and the title "A group rule-utilitarian approach to voter turnout".
- Mark: unread
- Source: coate_conlin; not checkable from this file (a 2002 working paper carries no AER details).
- Note: needs the AER page, or an NBER/AEA record. Rule 1 forbids me to fetch it.

### CC-02 "Reasonable level": a cost cut-off below which members vote
- First pass said: line 171, "each group (supporters, opposers) picks a 'reasonable level' of voting cost below which members vote".
- Mark: confirmed (with one wording nuance in the note)
- Source: coate_conlin; Section 1 and Section 4; PDF p. 3 (printed p. 2) and PDF p. 12 (printed p. 11)
- Quote: "“Doing their part” is understood to mean showing up to vote if their costs of going to the polls are below some “reasonable level”."
- Quote: "Thus, individuals behave according to the rule that would be best for the group as a whole."
- Note: the paper's agent of choice is each individual, who asks what his side should do; the two groups' levels come out of "a game in which individuals from the two groups simultaneously choose their levels" (PDF p. 4, printed p. 3). The first report's "each group picks" is a fair shorthand. The paper itself says the data cannot separate its story from groups choosing collectively (CC-U).

### CC-03 "maximize the payoff of a representative member of my group"
- First pass said: line 171, chosen to "maximize the payoff of a representative member of my group" (p. 3).
- Mark: confirmed. Page: the first report's "p. 3" is the PDF page; the printed page is 2. The phrase appears twice: Section 1 (PDF p. 3, printed p. 2, hyphenated across a line as "max-imize") and Section 4 (PDF p. 12, printed p. 11).
- Source: coate_conlin; Section 1 and Section 4; PDF p. 3 (printed p. 2); PDF p. 12 (printed p. 11)
- Quote: "What would be the level of voting costs below which those on my side of the issue should vote that would max-"
- Quote: "imize the payoff of a representative member of my group?"
- Quote: "what would be the critical level of voting costs below which those on my side of the issue should vote that would maximize the payoff of a representative member of my group?"
- Note: the words are the question each individual asks himself, not the paper's description of an optimiser. The Section 1 version omits "critical".

### CC-04 Supporter's expected payoff
- First pass said: line 171, "a supporter's expected payoff `π(γs, γo)b − γs²/2c` (p. 11; the extractor warned formulas were garbled in places, so I rely on the prose)".
- Mark: corrected (formula content confirmed on the PDF page image; page and notation corrected)
- Source: coate_conlin; Section 4, display after "Prior to the realization of his voting cost"; PDF p. 13 (printed p. 12); footnote 15 on the same page
- Quote: "Prior to the realization of his voting cost, a supporter’s expected payoff from the critical level"
- Quote: "and the second term represent expected voting costs, given that a supporter will vote only if"
- Correction: page "p. 11" → PDF p. 13 / printed p. 12 (printed p. 11 is the page where Section 4 begins). Notation: the display (seen on the page image) is π(γs, γo; ν, ω)·b − γs² / (2c), with the whole 2c in the denominator; the opposer's is −π(γs, γo; ν, ω)·x − γo² / (2c). Written "γs²/2c" it can be misread as (γs²/2)·c.
- Note: π is the probability that the referendum passes, ∫ from γo/(γs+γo) to 1 of the Beta density h(μ; ν, ω) dμ (PDF p. 12, printed p. 11, display seen on the image); it is not the probability that one ballot is pivotal (CC-P). The "c" is the upper end of the uniform support of voting costs, not an individual's cost. b is a willingness to pay (CC-B). The paper's own gloss: the first term is "expected policy benefits", the second "expected voting costs".

### CC-05 363 local liquor elections in Texas, 1976-96
- First pass said: line 171, "data: 363 local liquor elections in Texas, 1976-96 (p. 9)".
- Mark: confirmed (printed p. 9; PDF p. 10)
- Source: coate_conlin; Section 3.2; PDF p. 10 (printed p. 9); Appendix 9.1 on PDF p. 28 (printed p. 27)
- Quote: "We assembled data on 363 local liquor elections in Texas between 1976 and 1996 where prior to the election the voting jurisdictions prohibited the retail sale of all alcohol"
- Quote: "A total of 526 local liquor elections are identified in the annual reports of the Texas Alcoholic Beverage Commission between 1976 and 1996. We use 363 of these in our estimation."
- Note: the 363 are only the elections that proposed to move out of a completely "dry" status (the other 163 dropped for missing data, other items on the ballot, or a not-dry starting point). The introduction says "over 500 elections between 1976 and 1996" (printed p. 2). Table 1 (PDF p. 39): 147 beer/wine, 144 off-premise, 72 off- and on-premise (sum 363); 2 county, 133 justice precinct, 228 city (sum 363).

### CC-06 The paper does not test its model against the pivotal-voter model
- First pass said: line 171, the paper "does not test the model against the pivotal-voter model; it says that comparison 'has yet to be demonstrated' (p. 24)".
- Mark: confirmed (printed p. 24; PDF p. 25)
- Source: coate_conlin; Section 8 (Conclusion); PDF p. 25 (printed p. 24)
- Quote: "From an empirical perspective, it would be worth comparing the performance of the model presented here with that of the pivotal-voter model."
- Quote: "Thus, it should only be rejected if it can be shown to be outperformed by some coherent alternative. This has yet to be demonstrated."
- Quote: "It remains to structurally estimate the pivotal-voter model and compare its performance."
- Note: "has yet to be demonstrated" says that the pivotal-voter model has not been shown to be outperformed by a coherent alternative; "it" is the pivotal-voter model, and the paper treats its own model as a candidate for that role without having done the test. The same paragraph says "there are good reasons to be sceptical about its abilities to explain turnout" (quoted in CC-P). The paper also notes an earlier attempt to estimate the pivotal-voter model by others (Hansen, Palfrey and Rosenthal 1987, quoted in CC-P).

### CC-07 Two ad hoc alternatives and the three log-likelihoods
- First pass said: line 171, "compares against two ad hoc alternatives (the basic model fits best: log-likelihoods 749.20, 704.05, 692.26, p. 23)".
- Mark: confirmed (printed p. 23; PDF p. 24)
- Source: coate_conlin; Section 7.3; PDF p. 24 (printed p. 23); Tables 2, 4, 6, 8 on PDF pp. 42, 44, 46, 48 (unnumbered)
- Quote: "The maximum log-likelihood values for the basic, intensity, and popularity models are 749.20, 704.05, and 692.26 respectively."
- Quote: "Thus, the basic model appears the best, with the intensity model the runner up."
- Quote: "They are ad hoc, in the sense that they do not provide an account of why people behave in the postulated way"
- Quote: "N=363 , Log Likelihood=749.20"
- Quote: "N=363 , Log Likelihood=704.05"
- Quote: "N=363 , Log Likelihood=692.26"
- Quote: "Basic Model = Intensity Model 2.18"
- Quote: "Basic Model = Popularity Model 2.81"
- Quote: "Intensity Model = Popularity Model 2.08"
- Note: assignment (the first report did not give it): basic 749.20 (Table 2), intensity 704.05 (Table 4), popularity 692.26 (Table 6). The formal comparison is Vuong's non-nested test (Table 8): the basic model beats each rival at the 5 percent level; the intensity model beats the popularity model. The two rivals are the intensity hypothesis (supporters vote if cost < αb, opposers if < αx; printed pp. 19-20) and the popularity hypothesis (cut-off α·ν/(ν+ω) for supporters, α·ω/(ν+ω) for opposers; printed p. 21). Neither rival is the pivotal-voter model.

### CC-08 "This all depends on how we measure closeness"
- First pass said: line 171, "On closeness the paper says 'this all depends on how we measure closeness' (p. 10)".
- Mark: confirmed (the paper has a capital T; printed p. 10; PDF p. 11)
- Source: coate_conlin; Section 3.3; PDF p. 11 (printed p. 10)
- Quote: "It is natural to ask whether the data support the familiar idea that turnout is higher in close elections. This all depends on how we measure closeness."
- Quote: "When closeness is defined as the difference between votes for and against divided by total votes, the average closeness is 0.25."
- Quote: "This positive relationship is stronger if closeness is defined as the difference between votes for and against divided by the voting age population (correlation coefficient of 0.58)."
- Quote: "tween turnout and closeness when closeness is defined as the difference between votes for and against (correlation coefficient of -0.11)."
- Note [I]: all three "closeness" measures the paper uses are differences (margins), for which a larger number is a less close election. The paper reports correlations of 0.12 (margin over total votes, "a slight positive relationship"), 0.58 (margin over voting-age population) and -0.11 (raw vote difference) and does not state a sign convention for what "positive" means for "turnout is higher in close elections". Read literally, a positive correlation with a margin is higher turnout in less close races. Do not cite 0.12, 0.58 or -0.11 as support for or against "turnout rises when the race is close" without the lead resolving this. The first report quotes only the sentence, not the numbers.

### CC-09 "the only citizens who vote in equilibrium are those for whom d is no smaller than c" (Palfrey and Rosenthal)
- First pass said: line 201, "Coate & Conlin cite Palfrey & Rosenthal for 'the only citizens who vote in equilibrium are those for whom d is no smaller than c' in large electorates (p. 5)" (the line's heading says "Palfrey & Rosenthal 1983, 1985").
- Mark: confirmed (printed p. 5; PDF p. 6; the sentence starts at the foot of printed p. 4, PDF p. 5), with a restriction the first report omits
- Source: coate_conlin; Section 2; PDF p. 5 (printed p. 4) and PDF p. 6 (printed p. 5); footnote 2 on PDF p. 6 (printed p. 5)
- Quote: "Formal support for this concern is provided by Palfrey"
- Quote: "and Rosenthal’s well known result that in a sufficiently large electorate the only citizens who vote in equilibrium are those for whom d is no smaller than c"
- Quote: "Accordingly, significant variations in turnout in large elections must arise from variations in the fraction of the population for whom d is no smaller than c."
- Quote: "Palfrey and Rosenthal’s result is for symmetric equilibria in a model where voters are imperfectly informed about each others’ voting costs and preferences."
- Note: footnote 2 limits the result to symmetric equilibria with imperfect information about others' costs and preferences. The paper's reference list has only Palfrey and Rosenthal 1985, "Voter Participation and Strategic Uncertainty", APSR 79, 62-78 (PDF p. 27, printed p. 26); the 1983 paper is not in C&C's list. The original theorem is unread (rule 1).

### CC-10 Geys on Coate & Conlin: warm glow "restricted to behaving like as should towards people on one's own side of the issue"
- First pass said: line 173, Geys "notes Coate & Conlin's warm glow is 'restricted to behaving like as should towards people on one's own side of the issue' (p. 20)".
- Mark: unread (the quoted words are Geys's, in another reader's source)
- Source: coate_conlin; PDF p. 7 (printed p. 6), the nearest sentence in C&C
- Quote: "They are therefore motivated only to help those on their side of the issue."
- Note: C&C's own text supports the substance. C&C never use the words "warm glow" (grep over `text.txt`: none). Feddersen & Sandroni do (FS-D).

## Feddersen & Sandroni

### FS-01 What the downloaded file is (title, date, authors)
- First pass said: line 172, "draft read (...duty4-15-02.pdf, an earlier draft titled differently; the extractor labelled it 'duty')"; the report's brief calls it dated 4-15-02.
- Mark: corrected
- Source: feddersen; https://www.kellogg.northwestern.edu/faculty/fedderse/homepage/papers/duty4-15-02.pdf ; title page, PDF p. 1
- Quote: "A Theory of Participation in Elections"
- Quote: "Timothy J. Feddersen"
- Quote: "Alvaro Sandroni"
- Quote: "April 2002"
- Correction: "an earlier draft titled differently" → the draft carries the same title as the AER 2006 article, "A Theory of Participation in Elections", authors Timothy J. Feddersen and Alvaro Sandroni, dated April 2002 on the title page. "duty" is only part of the file name. "4-15-02" is in the file name, not in the paper.
- Note: three versions are in play: the 2001 mimeo that Coate & Conlin cite (their reference [7]: Feddersen and Sandroni, 2001, under the same title, "mimeo, University of Rochester"; coate_conlin PDF p. 26, printed p. 25; the title is hyphenated across a line there), this April 2002 draft (read), and the AER 2006 article (unread). Feddersen & Sandroni's own reference list cites Coate & Conlin (2002) (PDF p. 42). Differences between the versions are not checkable here; one possible difference is flagged in FS-W.

### FS-02 Ethical agents "receive a payoff D>cl for doing their part"
- First pass said: line 172, ethical agents "receive a payoff D>cl for doing their part" (p. 11).
- Mark: confirmed (PDF p. 11 = printed p. 11; the "l" in "cl" is a superscript on the page image: the lower end of the cost support)
- Source: feddersen; Section 2; PDF p. 11 (printed p. 11)
- Quote: "(called ethical agents) receive a payoff D > cl for doing their part."
- Quote: "(called abstainers) receive zero payoff for doing their part."
- Quote: "That is, ethical agents will do their part if and only if the cost of the required action is sufficiently small."
- Note: D must exceed only the lowest possible cost c^l, not every cost. "Doing their part" means taking the action the (endogenously chosen) rule says one should take, which can be to abstain: "it may be (and often is) the case that some agents receive an additional payoff for voting while others receive a payoff for not voting" (PDF p. 4; quoted in FS-D). On the page image the display defining the actual action reads "abstain if d ≤ c; e_i(c) if c > d". The second inequality looks like a misprint for c < d, since the prose and Proposition 1 (cut-offs c*_i in (c^l, D], PDF p. 16) say ethical agents act only when the cost is low. Cite the prose, not the display. [I]

### FS-03 "Agents with voting costs below this threshold should (and will) vote"
- First pass said: line 172, "consistent behaviour is a cost cut-off ('Agents with voting costs below this threshold should (and will) vote', p. 5)".
- Mark: confirmed (PDF p. 5 = printed p. 5). The first report capitalised "Agents" and cut the clause; in the paper it sits inside a longer sentence.
- Source: feddersen; Section 1; PDF p. 5 (printed p. 5); the formal version is Proposition 1, PDF p. 16 (printed p. 16)
- Quote: "We show that if agents’ behavior is consistent then there exists a cut-off point for each type such that agents with voting costs below this threshold should (and will) vote for their favored candidate."
- Quote: "Agents with voting costs above the threshold abstain."
- Quote: "As noted above, it is possible that agents with voting costs below D will abstain because they reason they should."
- Note: the cut-off is a result of the model for ethical agents under the "consistency" requirement; non-ethical agents abstain. Proposition 1: "There is a pair of cut-off points c*_i in (c^l, D]" (PDF p. 16).

### FS-04 "a single vote is never pivotal"
- First pass said: line 172, "'a single vote is never pivotal' (p. 4) in the large-population model".
- Mark: confirmed (PDF p. 4 = printed p. 4)
- Source: feddersen; Section 1, PDF p. 4; also Abstract (PDF p. 1); Section 2 (PDF p. 9)
- Quote: "Voting costs vary within the population and a single vote is never pivotal."
- Quote: "We model a two-candidate election in which a large population of agents may vote for candidate 1, vote for candidate 2 or abstain."
- Quote: "in which voting is costly and no vote is ever pivotal."
- Quote: "There is a continuum of agents who must choose one of three actions: vote for candidate 1, vote for 2 or abstain."
- Note: "never pivotal" is true by construction of a continuum-of-agents model (PDF p. 9), not a computed small probability. The first report's "in the large-population model" is right; the precise setting is a continuum.

### FS-05 Minority turnout exceeds majority turnout
- First pass said: line 172, "minority turnout exceeds majority turnout (p. 5)".
- Mark: corrected (the wording is the paper's, but unqualified it misleads: it is the share of each group that votes)
- Source: feddersen; Section 1, PDF p. 5 (printed p. 5); Property 1, PDF p. 23 (printed p. 23); Section 6, PDF p. 33 (printed p. 33), footnote 12; Proposition 4, PDF p. 37 (printed p. 37)
- Quote: "In contrast, our model predicts that turnout will be higher among the minority than the majority, yet the majority’s preferred candidate wins with probability greater than a half."
- Quote: "The expected fraction of agents in the majority group who vote"
- Quote: "is smaller than the expected fraction of agents in the minority group who vote"
- Quote: "However, the total expected turnout of the majority"
- Quote: "is greater than the total expected turnout of the minority"
- Quote: "Note that this result depends on several assumptions. First, the importance of the election is equal for both groups."
- Correction: "minority turnout exceeds majority turnout" → the fraction of the minority that votes exceeds the fraction of the majority that votes, but the majority's total expected turnout is larger than the minority's, and the majority's candidate wins with probability above one half (Property 1, PDF p. 23; Propositions 4 and 5, PDF p. 37). It holds in the worked example (uniform costs, uniform ethical fractions, equal importance w) and, in Appendix B, with the same cost density in both groups and equal average ethical fractions.
- Note: footnote 12 (PDF p. 33) lists the assumptions: equal importance for both groups, and that "agents in both groups care about aggregate voting costs as opposed to only caring about the voting cost of the members of their group" (full quote in FS-B). If the minority cared more or had more ethicals, its candidate could win with probability above a half (PDF p. 24).

### FS-06 AER 96(4): 1271-82 citation and the published version
- First pass said: line 172, "Feddersen & Sandroni (2006), 'A theory of participation in elections', AER 96(4): 1271-82... Published version unread."
- Mark: unread
- Source: feddersen; not checkable from a 2002 draft.
- Note: the first report's own flag stands: nothing here says what the AER version contains.

---

# Part 2: the fill (unit, pivotal-voter model, benefit, calculus of voting, fork points)

## Coate & Conlin

### CC-U Unit of evaluation: a cut-off rule applied by a group, not one ballot
- First pass said: line 174, "the unit of evaluation is the *rule* 'vote if your cost is below a cut-off' applied by everyone on your side, and the group's welfare under that rule"; line 175 [I] a group can gain more from the rule than it costs while a member's marginal ballot still has tiny p; table row 3.5 (line 129).
- Mark: confirmed for the first half (the unit and the group's payoff); the [I] half carries qualifications, listed in the note
- Source: coate_conlin; PDF p. 3 (printed p. 2); PDF p. 4 (printed p. 3); PDF p. 7 (printed p. 6); PDF p. 8 (printed p. 7); PDF p. 12 (printed p. 11); PDF p. 14 (printed p. 13)
- Quote: "Thus, individuals behave according to the rule that would be best for the group as a whole."
- Quote: "In equilibrium, individuals in each group must be satisfied with their reasonable level, given the level they expect the opposing group to choose."
- Quote: "For analytical tractability, we adopt the fiction that the community has a continuum of citizens."
- Quote: "Each group collectively and simultaneously decides how many of its members should vote in order to maximize the group’s aggregate benefit."
- Quote: "the empirical work to distinguish it from a story where supporters and opposers collectively determine which of their members should vote"
- Quote: "This is typically because it would be better for that group not to vote at all than to vote for cost levels below the reasonable level identified in the proposition."
- Note: (1) The object chosen is the cut-off γ (vote iff c_i ≤ γ), judged by the expected payoff of a representative member of one's group, π·b − γ²/(2c). The Morton quotation (printed p. 6) describes Morton's model, of which C&C say their approach "may be considered as a special case"; the "collectively determine" sentence (printed p. 7) says the data cannot tell their story from a group-collective one. (2) The opposing group's cut-off is held fixed in each best response (Nash across groups), so "contradicts fixity of others" in row 3.5 holds only inside one's own group: a group's rule changes all its members' behaviour and not the other group's [I]. (3) On the first report's [I] "any one member's marginal ballot still has tiny p": in this model there is no such p, because the community is a continuum, so one ballot has no effect by construction; the paper never computes the effect of one ballot. (4) "A group can gain more from the rule than the rule costs it" is a condition, not a given: Proposition 2(iii), the "better than staying home" conditions (PDF p. 14), and the passage quoted above say a group may do better by not voting at all, and an equilibrium may not exist.

### CC-P What the paper says about the pivotal-voter model and the probability of being pivotal
- First pass said: line 171 only that the paper does not test against it (CC-06). The probability side is not stated.
- Mark: confirmed (new facts, not in the first report)
- Source: coate_conlin; Section 2, PDF p. 5 (printed p. 4); PDF p. 8 (printed p. 7); Section 8, PDF p. 25 (printed p. 24)
- Quote: "The pivotal-voter model of Ledyard (1984) and Palfrey and Rosenthal (1985) provides a natural way of endogenizing the probability that a voter will swing the election."
- Quote: "However, the obvious problem with this approach would seem to be that p is sufficiently small in any large election that changes in pB are likely to be minuscule across elections."
- Quote: "Thus, many have questioned the fruitfulness of a theory of turnout based on minuscule changes in a minuscule number"
- Quote: "While there are good reasons to be sceptical about its abilities to explain turnout, the pivotal voter model represents in many respects the simplest way of thinking about voting behavior."
- Quote: "Rosenthal (1987) use data on school budget referenda to try to structurally esti-"
- Quote: "mate the pivotal-voter model."
- Quote: "The probability that the referendum passes is therefore:"
- Note: the paper's own model has one probability, π(γs, γo; ν, ω), the chance the referendum passes given both groups' cut-offs (the display on PDF p. 12 shows the referendum passes when μγs/c > (1−μ)γo/c, a strict inequality, with μ the random share of supporters). It never defines a probability that one ballot decides the result. The paper states p is "sufficiently small in any large election" as the standard objection, and then does not engage it with a test (CC-06). Hansen, Palfrey and Rosenthal (1987) attempted a structural estimate of the pivotal-voter model on school-budget referenda (printed p. 7), which the first report does not mention.

### CC-B What the paper calls the voter's benefit, and whose welfare
- First pass said: no statement beyond the payoff (CC-04) and [I] "the group's welfare" (line 174).
- Mark: confirmed (new facts)
- Source: coate_conlin; PDF p. 4 (printed p. 3); PDF p. 7 (printed p. 6); Section 4, PDF p. 12 (printed p. 11); footnote 17, PDF p. 13 (printed p. 12); Section 6, PDF p. 19 (printed p. 18); PDF p. 20 (printed p. 19)
- Quote: "Each supporter is willing to pay b for the relaxation, while each opposer is willing to pay x to avoid it."
- Quote: "The specific model developed in the paper assumes that all supporters enjoy the same benefit and all opposers incur the same cost if the referendum passes."
- Quote: "They are therefore motivated only to help those on their side of the issue."
- Quote: "The reasonable level for each group is increasing in the gains or losses to that group caused by the referendum passing"
- Quote: "would be the fraction of the population who believed that the change would be good for society,"
- Quote: "b would be their estimate of the average net benefit of the change, and x would be the estimate of the average net cost of the change of those who thought it was a bad idea."
- Quote: "The change passes a standard cost-benefit test if and only if this average net benefit is positive."
- Quote: "Only 39 referenda had a positive net benefit when voting costs are included"
- Note: in the voter's own objective, the benefit is b (a supporter's willingness to pay for the change) or x (an opposer's willingness to pay to avoid it), uniform across a group, received if the referendum passes, weighted by π = P(passes). It is the voter's own group's welfare only ("motivated only to help those on their side"). Footnote 17 (printed p. 12) gives an alternative reading in the manner of Feddersen & Sandroni (2001), where b and x are beliefs about the change's average net benefit or cost to society; the paper says (continuing on PDF p. 14, printed p. 13) that the two interpretations have different implications for the equilibrium reasonable costs, so in principle one could ask which fits the data better, but that empirically it is not clear what ν and ω should depend on under the Feddersen & Sandroni reading; it does not test the two. Separately, the paper's own welfare accounting is aggregate: net benefit = μb − (1−μ)x, positive in 110 of the 363 jurisdictions, and with voting costs included positive in only 39 (printed pp. 18-19). Units: b, x, c are identified only up to a normalisation (printed p. 18, fn 24: "we can only infer relative benefits and relative costs"), so the paper's numbers (e.g. mean b 0.59, x 0.92, c 2.45 in Table 3) carry no dollar meaning.

### CC-D Where the paper states the calculus of voting is pB + d
- First pass said: not stated; the first report's calculus table (lines 28-46) has no Coate & Conlin row; line 45 and line 326 treat Riker & Ordeshook's form as unconfirmed.
- Mark: confirmed (new)
- Source: coate_conlin; Section 2 ("Relationship to the turnout literature"); PDF p. 5 (printed p. 4); text lines 188-194; formula verified on the page image
- Quote: "The well-known calculus of voting model of turnout (Downs (1957), Riker and Ordeshook (1968)) defines the benefits of voting as pB + d where p is the probability of swinging the election,"
- Quote: "B is the gain from having one’s preferred candidate win, and d is the benefit a citizen feels from doing his civic duty or expressing his preference."
- Quote: "A voter votes if these benefits exceed the direct cost of voting, denoted c, which includes the time taken to get to the polls and so on."
- Note: this is the sentence the lead asked about. It credits the whole form pB + d to "Downs (1957), Riker and Ordeshook (1968)" jointly and in passing; it is a secondary, compressed attribution (neither original read). The first report's table has Downs's own form as PB − C and the d term added by Riker & Ordeshook (via Sanders and Salka). The decision rule here is pB + d > c, the same as the first report's Dowding row (`pB + D > C`). B is "the gain from having one's preferred candidate win" (a gain if the candidate wins, not an expected gain: the probability sits in p). d is given two meanings in one clause, "civic duty or expressing his preference", which fits the first report's "sources disagree on what D is" (item 6.1) and adds the paper as another source. The next paragraph then sets d aside: "Since the benefits from doing one’s duty seem rather nebulous" (PDF p. 5).

### CC-F1 Tie rule
- First pass said: not stated for this paper (the report's open point 6.6 is about the ½ factor in general).
- Mark: confirmed (new)
- Source: coate_conlin; Section 3.1; PDF p. 9 (printed p. 8)
- Quote: "All registered voters can vote and if the proposed change receives at least as many affirmative as negative votes, it is approved."
- Note: Texas rule: a tied referendum passes (no coin toss, no ½). In the model the community is a continuum and the referendum passes iff μγs/c > (1−μ)γo/c, so a tie has probability zero and no tie rule is used. There is no ½ factor anywhere in the paper.

### CC-F2 Whether "held fixed" is causal or evidential
- First pass said: row 3.5 "contradicts fixity of others"; item 6.9 (causal or evidential) is open.
- Mark: confirmed (the paper's wording); the causal/evidential question itself is not addressed by the paper
- Source: coate_conlin; PDF p. 4 (printed p. 3); PDF p. 7 (printed p. 6); Section 2, PDF p. 6 (printed p. 5)
- Quote: "In equilibrium, individuals in each group must be satisfied with their reasonable level, given the level they expect the opposing group to choose."
- Quote: "A rule-utilitarian takes the action that, if taken by all rule-utilitarians, would maximize aggregate utility."
- Note: the other group's behaviour is taken as given ("given the level they expect the opposing group to choose"); the member's own group is treated as acting together under the rule (the rule-utilitarian's test is what happens "if taken by all"). The paper never says whether the link between one person's rule and the group's behaviour is causal or evidential; it simply posits that individuals follow the rule. [I] that this is the structure the first report's table calls "contradicts fixity of others", but only for the own group.

### CC-F3 What d is
- First pass said: items 6.1 and 3.6: d is the open fork; 3.5 [I] "close to D (3.6) with a consequentialist justification".
- Mark: confirmed (new, and supports the [I])
- Source: coate_conlin; PDF p. 3 (printed p. 2); PDF p. 6 (printed p. 5); footnote 5, PDF p. 7 (printed p. 6); Section 8, PDF p. 25 (printed p. 24)
- Quote: "This is not because they receive a transfer from other group members for doing so - they simply adhere to the belief that this is how a citizen should behave in a democracy."
- Quote: "In terms of the calculus of voting model, Harsanyi is effectively assuming that d is large enough so that everyone does their duty but rejects the implicit assumption that doing one’s duty always involves voting."
- Quote: "As in Harsanyi (1980), the model of this paper implicitly assumes that d is sufficiently large that individuals always do their part."
- Quote: "Finally, more thought should be given to the justification of the behavior postulated here. Why should citizens believe that this is how they should behave in elections?"
- Note: in C&C, duty is not an extra payoff in the vote decision: d is assumed large enough that the rule is always followed, and the content of "duty" is the cut-off rule. The paper itself says the justification is open: "what forces compel them to do their part?" (printed p. 24).

### CC-F4 What counts in C
- First pass said: item 6.8 open (trip, time, information, registration).
- Mark: confirmed (new)
- Source: coate_conlin; Section 2, PDF p. 5 (printed p. 4); Section 1, PDF p. 3 (printed p. 2); Section 3.2, PDF p. 11 (printed p. 10); Section 4, PDF p. 12 (printed p. 11)
- Quote: "Voting is costly, with each citizen i facing a cost of voting ci where ci is the realization of a random variable uniformly distributed on [0, c]."
- Quote: "In an attempt to get information about the costs of voting, daily weather conditions at 44 weather stations in Texas was obtained"
- Quote: "Third, the referenda are typically held separately from other elections, so that the only reason to go to the polls is to vote on the proposed change in liquor law."
- Note: c is the time and effort of going to the polls (the calculus-of-voting sentence, CC-D). Empirically it is proxied by weekend, weather and summer indicators (Table 2: weekend 0.282, significant; weather, summer not). Voting costs also enter the paper's welfare accounting (CC-B).

## Feddersen & Sandroni

### FS-U Unit of evaluation: a rule for a whole type, never one ballot
- First pass said: line 174 row 3.5, as for Coate & Conlin; the Feddersen & Sandroni entry (line 172) does not say.
- Mark: confirmed (new)
- Source: feddersen; PDF p. 5 (printed p. 5); PDF p. 10 (printed p. 10); PDF p. 12 (printed p. 12); PDF p. 14 (printed p. 14); PDF p. 15 (printed p. 15)
- Quote: "agents with preference type i evaluate each rule by the social outcome they produce."
- Quote: "No single agent decides who will be elected or the social cost of voting. Each agent’s preferences reflect the choices he would make if he was a social planner."
- Quote: "Assume that a rule e defines the actions that all type i agents should take."
- Quote: "In our model with a continuum of agents the act of an individual agent does not have any impact on either the probability a candidate wins or on the social cost of voting."
- Quote: "In suitably redefined model with countably many agents this agent would abstain."
- Quote: "Part 2 ensures that the behavior of all agents of the same type is determined by the same maximally ranked rule."
- Note: the authors themselves say that judged one agent at a time, taking everyone else as given, the agent would abstain in a model with countably many agents; the rule-ranking is how they avoid that. They also reject ranking rules as if everyone, including the other type, followed one's rule (PDF pp. 15-16).

### FS-P What the paper says about the pivotal-voter model and the probability of being pivotal
- First pass said: line 172 only that "a single vote is never pivotal" (p. 4) (FS-04).
- Mark: confirmed (new)
- Source: feddersen; Section 1, PDF p. 2 (printed p. 2) and PDF p. 6 (printed p. 6); Section 1.1, PDF p. 8 (printed p. 8, footnote 2); Section 4, PDF p. 24 (printed p. 24); Section 2, PDF p. 10 (printed p. 10)
- Quote: "If voting is costly then, since the likelihood of a vote being pivotal is very small,"
- Quote: "theoretic models predict low levels of turnout (e.g., Palfrey and Rosenthal (1985))."
- Quote: "Their result follows from the fact that the probability of a pivotal vote increases as the margin of victory decreases."
- Quote: "However, this correlation is not related to changes in the probability a vote is pivotal."
- Quote: "Since a vote is never pivotal in our setting, the relationship between turnout and margin of victory is unrelated to changes in the likelihood a vote is pivotal."
- Quote: "It is known that in voting games, as above, with a continuum of agents and costly voting there are generically no equilibria in which a positive fraction of the population participates."
- Quote: "in a large election, any result can be reproduced, at lower social cost, by taking a sufficiently representative sample."
- Note: the paper treats the small pivot probability as the reason standard models predict low turnout, and builds a model in which pivotality plays no role. It does not test or reject the pivotal-voter model empirically; it cites Coate & Conlin (2002) for a structural estimate of "our model" (PDF p. 35).

### FS-B What the paper calls the benefit, and whose welfare
- First pass said: line 172 only the payoff D.
- Mark: confirmed (new)
- Source: feddersen; Section 1, PDF p. 4 (printed p. 4); Section 2, PDF p. 9 (printed p. 9), PDF p. 10 (printed p. 10, footnote 4); Section 2.1, PDF p. 13 (printed p. 13); Section 6, PDF p. 33 (printed p. 33, footnote 12)
- Quote: "ences over the candidates and the cost of the election, but these preferences are not necessarily related to social welfare."
- Quote: "Let a social outcome be a probability that candidate 1 is elected and an expected cost of the election."
- Quote: "All agents prefer the social cost of voting to be minimized"
- Quote: "Thus, w parameterizes the importance of the difference between the two candidates relative to the social cost of voting."
- Quote: "Informally, we have in mind that agents’ preferences reflect not only their self-interest but also their religious, ethical or philosophical perspectives."
- Quote: "For example, these preferences might be associated with a notion of social welfare (utilitarianism), a concern for distributive justice or support for human rights"
- Quote: "agents in both groups care about aggregate voting costs as opposed to only caring about the voting cost of the members of their group."
- Note: the first Quote starts mid-word because the source breaks "prefer-" / "ences" across a line (PDF p. 4); the sentence is "We assume that agents have preferences over the candidates and the cost of the election, but these preferences are not necessarily related to social welfare." A type-1 agent's objective is w·p − ϑ(φ) (display (2.1), PDF p. 9; type 2: w(1−p) − ϑ(φ), PDF p. 10), where p is the probability that candidate 1 wins, φ the expected social (aggregate) cost of voting, ϑ a strictly increasing convex function, and w "the importance of the election". So the benefit is w times the probability that the voter's candidate wins, given the group's rule (not the probability one ballot decides); the cost term is everyone's voting cost, not only the voter's own. The paper does not define the benefit as the voter's own welfare or as society's: preferences are "not necessarily related to social welfare" yet may be utilitarian, distributive or rights-based (PDF p. 13). The paper's own assumption is that "fixing the probability candidate 1 wins the election, all agents prefer lower turnout" (PDF p. 13). See also FS-W below.

### FS-D Where the paper treats the calculus of voting, and what D is
- First pass said: nothing about Feddersen & Sandroni in the calculus table (lines 28-46).
- Mark: confirmed (new): the paper never writes pB + D; it describes Riker & Ordeshook's model as a duty payoff that depends on voting, and turnout in "such a model" as depending only on cost against D. `grep -i "calculus\|pB"` finds "calculus" only in two reference titles (Palfrey & Rosenthal 1983, "A Strategic Calculus of Voting"; Riker & Ordeshook 1968, "A Theory of the Calculus of Voting").
- Source: feddersen; Section 1, PDF p. 4 (printed p. 4); Section 1.1, PDF p. 8 (printed p. 8); Section 4, PDF p. 25 (printed p. 25); Section 7, PDF p. 34 (printed p. 34)
- Quote: "Riker and Ordershook (1968) analyze a model of participation in which agents receive a “duty” payoff D > 0 when they vote for their preferred candidate."
- Quote: "In contrast, the action an agent should take is determined endogenously in our model."
- Quote: "In particular, it may be (and often is) the case that some agents receive an additional payoff for voting while others receive a payoff for not voting."
- Quote: "In such a model turnout is determined by the fraction of the electorate with cost to vote less than D."
- Quote: "In that case, just as in Riker and Ordeshook, agents will vote for their preferred candidate if and only if the payoff for doing their part is greater than their cost to vote."
- Quote: "As in the Riker and Ordeshook (1968) paper, the warm glow effect is exogenous."
- Quote: "There is a warm glow aspect to our model."
- Quote: "Blais (2000) reports that a sense of duty plays an important role in the decision to vote for a large fraction of voters."
- Note: so for this paper D is a payoff for doing one's part (taking the action the rule requires), received by "ethical" agents only, and it is endogenous in what counts as the part. In Riker & Ordeshook, as the paper reads them, D is a duty payoff for voting for one's preferred candidate, exogenous, with no pB term in the decision (the decision is c versus D). Both are secondary readings (original unread). The paper calls the R&O D a "warm glow" and its own "a warm glow aspect". The model reduces to Riker & Ordeshook when ϑ is constant or increasing (PDF p. 34).

### FS-F1 Tie rule
- First pass said: not stated.
- Mark: confirmed (new)
- Source: feddersen; Section 5, PDF p. 29 (printed p. 29)
- Quote: "Then, each candidate wins the election with equal probability"
- Note: stated in the discussion of why a pure-strategy equilibrium may not exist when the election is exactly tied (σ1·k·q1 = σ2·(1−k)·q2): a fair coin. It is a knife-edge case in a continuum model, not used elsewhere.

### FS-F2 Whether "held fixed" is causal or evidential
- First pass said: not stated.
- Mark: confirmed (new)
- Source: feddersen; Section 2.1.1, PDF p. 15 (printed p. 15); PDF p. 12 (printed p. 12)
- Quote: "We also assume that when agents rank rules they take as given the behavior of agents with preferences different from their own."
- Quote: "At one extreme, we might have assumed an agent ranks rules taking as given the behavior of all other agents."
- Quote: "In a note available upon request from the authors, we provide a formal foundation for this assumption."
- Note: others of the other type are taken as given; one's own type is assumed to follow the same rule (consistency, part 2). The paper does not discuss causal versus evidential reasoning. The justification for "taking as given the other type" is in a separate note not in this draft.

### FS-F3 What counts in C
- First pass said: not stated.
- Mark: confirmed (new)
- Source: feddersen; Section 2, PDF p. 9 (printed p. 9)
- Quote: "The cost of voting can be thought of as, for example, the time spent in the process of voting."
- Quote: "We assume that the disutility from voting is equal to the cost"
- Quote: "Each agent knows her own realized voting costs, but not the realization of other agents’ voting costs."
- Note: the cost that enters the rule ranking is the aggregate expected social cost of voting (ϑ(φ)); a voter's own cost c enters only whether she does her part (c against D). See FS-B.

### FS-W Possible difference from Coate & Conlin's description of the 2001 mimeo
- First pass said: not stated.
- Mark: confirmed (the two statements, each from its own source; whether they describe different versions is [I])
- Source: coate_conlin; PDF p. 7 (printed p. 6), footnote 5 on the same page; and feddersen; PDF p. 4 (printed p. 4)
- Quote: "In Feddersen and Sandroni’s model, all individuals who vote follow the voting rule that they believe maximizes aggregate utility."
- Quote: "The key difference between the two approaches is thus one of interpretation."
- Quote: "First, in Feddersen and Sandroni’s model, the payoff of each group member depends on the expected voting costs of the average citizen in the community as a whole as opposed to the average citizen in his group."
- Note: Coate & Conlin (January 2002) describe the 2001 mimeo as aggregate-utility rule-utilitarianism. The April 2002 draft read here says the preferences "are not necessarily related to social welfare" (FS-B) while still making the cost term aggregate. Whether that is a difference between versions or only emphasis is [I]; the published AER 2006 text is unread. Also: Feddersen & Sandroni say Coate & Conlin "have structurally estimated our model" (PDF p. 35), while Coate & Conlin call the difference between the approaches one of interpretation, with four differences listed in their footnote 5.

---

# Corrections table

| Old (first report) | New | Source |
|---|---|---|
| Coate & Conlin entry carries the AER title and the NBER URL (line 171) | The file at that NBER URL is WP 8720, January 2002, titled "Voter Turnout: Theory and Evidence from Texas Liquor Referenda"; "group rule-utilitarian" is not in it | coate_conlin, PDF p. 1-2 (CC-01) |
| Supporter's payoff "π(γs, γo)b − γs²/2c" at "p. 11" | π(γs, γo; ν, ω)·b − γs²/(2c), at PDF p. 13 / printed p. 12 (denominator is 2c) | coate_conlin, PDF p. 13 (CC-04) |
| "maximize the payoff of a representative member of my group" at "p. 3" | PDF p. 3 = printed p. 2 (Section 1); the same question again at PDF p. 12 = printed p. 11 (Section 4) | coate_conlin (CC-03) |
| Feddersen & Sandroni draft is "an earlier draft titled differently" | Same title as the AER article, "A Theory of Participation in Elections", April 2002; "duty" is part of the file name | feddersen, PDF p. 1 (FS-01) |
| "minority turnout exceeds majority turnout (p. 5)" | the fraction of the minority that votes exceeds the fraction of the majority; the majority's total expected turnout is greater; the majority's candidate wins with probability above one half | feddersen, PDF pp. 5, 23, 37 (FS-05) |
| Palfrey & Rosenthal result "in large electorates" (line 201) | add: the result is for symmetric equilibria with imperfect information about others' costs and preferences (footnote 2); C&C cite only the 1985 paper | coate_conlin, PDF p. 6 (CC-09) |
| "this all depends on how we measure closeness" (lowercase) | "This all depends on how we measure closeness." (capital T; printed p. 10) | coate_conlin, PDF p. 11 (CC-08) |
| Feddersen & Sandroni quote "Agents with voting costs below this threshold should (and will) vote" | in the paper the clause is lowercase and continues "for their favored candidate." | feddersen, PDF p. 5 (FS-03) |

# Unread and why

- Coate & Conlin, AER 94(5): 1476-1504 (2004): the published version and its citation details; only the January 2002 working paper was read (CC-01b). Rule 1 forbids fetching it.
- Feddersen & Sandroni, AER 96(4): 1271-82 (2006): the published version; only the April 2002 draft was read (FS-06). The 2001 mimeo that Coate & Conlin cite is also unread.
- Geys's wording about Coate & Conlin's "warm glow" (line 173): Geys is another reader's source (CC-10).
- Harsanyi (1977, 1980, 1992), Palfrey & Rosenthal (1983, 1985), Ledyard (1984), Hansen-Palfrey-Rosenthal (1987), Morton (1987, 1991), Downs (1957), Riker & Ordeshook (1968): not read. Everything this file says about them is what Coate & Conlin or Feddersen & Sandroni say about them, quoted as such.
- Whether the AER versions of either paper keep the same model, numbers and wording as these two drafts.

# Found that the first pass missed

Fork points from rule 10, where these two papers speak (each points to the entry with the quotes):

| Fork | Coate & Conlin (Jan 2002 WP) | Feddersen & Sandroni (Apr 2002 draft) |
|---|---|---|
| Whose welfare is in B | The voter's own group only: b = a supporter's willingness to pay for the change, x = an opposer's to avoid it, same across a group; the paper's welfare check is aggregate (CC-B). A footnote reading in the F&S manner makes b and x beliefs about average net benefit to society | The objective is w × P(own candidate wins) minus a convex function of the aggregate expected voting cost of everyone; preferences "not necessarily related to social welfare" but may be utilitarian (FS-B) |
| B as gain-if-decisive or expected gain pB | b is the gain if the referendum passes; the expected gain is π·b with π = P(passes), a group-level probability (CC-04, CC-B); in the calculus sentence "B is the gain from having one's preferred candidate win" and p is the probability of swinging (CC-D) | w is the importance of the election; the expected benefit is w × P(win); no pivot probability exists (FS-B, FS-P) |
| Tie rule (the ½) | Ties pass under the Texas rule; no ½ in the model (CC-F1) | A tie gives each candidate "equal probability" (FS-F1); a knife-edge case |
| "Held fixed": causal or evidential | Other group's cut-off taken as given; own group acts under the rule; no causal/evidential discussion (CC-F2) | Other type's behaviour taken as given; own type acts under the same rule; a separate note, not in the draft, gives the foundation (FS-F2) |
| What D is | d: civic duty or expressing a preference (CC-D); assumed large enough that the rule is always followed (CC-F3) | D: payoff for "doing one's part", for ethical agents only, endogenous in what the part is; R&O's D called an exogenous warm glow (FS-D, FS-02) |
| What counts in C | Time and effort of going to the polls; uniform on [0, c]; weather and weekend as proxies; voting costs also in welfare accounting (CC-F4) | Time spent voting; the ranking uses the aggregate social cost (FS-F3, FS-B) |

Items in neither report's list, with sources:

### M1 Units are not identified in Coate & Conlin
- First pass said: not stated.
- Mark: confirmed (new)
- Source: coate_conlin; Section 6, footnote 24; PDF p. 19 (printed p. 18)
- Quote: "The normalization is required because we cannot infer benefits and costs from the number of people who vote for and against the referendum."
- Quote: "Instead, we can only infer relative benefits and relative costs."
- Note: no dollar value of B or C can be read from the paper's estimates (Table 3, PDF p. 43: b 0.59, x 0.92, c 2.45 are in unidentified units).

### M2 Coate & Conlin's model equilibrium need not exist
- First pass said: not stated.
- Mark: confirmed (new)
- Source: coate_conlin; Section 4; PDF p. 14 (printed p. 13)
- Quote: "There is no general guarantee that an equilibrium will exist - the payoff functions of supporters and opposers are not quasi-concave functions of their own reasonable cost levels."
- Note: the paper checks Proposition 2's conditions after estimation and says they hold for every jurisdiction ("Remarkably, this is the case for every jurisdiction", PDF p. 17, printed p. 16).

### M3 Equilibrium cut-offs rise with the stakes (bears on "importance")
- First pass said: not stated.
- Mark: confirmed (new)
- Source: coate_conlin; PDF p. 4 (printed p. 3); PDF p. 13 (printed p. 12); PDF p. 19 (printed p. 18)
- Quote: "The equilibrium reasonable levels depend on election specific characteristics like the relative sizes of the two competing groups, the importance of the issue decided by the referendum to the groups, and expected voting costs."
- Quote: "The reasonable level for each group is increasing in the gains or losses to that group caused by the referendum passing"
- Quote: "opposers feel much more intensely about the issue than do supporters"
- Note: in Feddersen & Sandroni the analogous prediction is that turnout rises with the importance w (PDF p. 26, Property 4): "The property that expected turnout increases with the important of the election is consistent with the evidence that turnout is higher for presidential elections than state elections" (source typo "important" as printed). Both are about turnout across elections, not the value of one ballot.

### M4 Internal inconsistency in Coate & Conlin on mean voting-age population
- First pass said: not stated (not a first-report claim).
- Mark: confirmed (new, a flaw in the source)
- Source: coate_conlin; Section 3.2 text, PDF p. 10 (printed p. 9), against Table 1, PDF p. 39
- Quote: "Table 1 indicates that the mean voting age population in the 363 jurisdictions is 4,415 at the time of the elections."
- Quote: "Mean = 4145"
- Note: the text says 4,415; Table 1 says 4145. Probably a transposition; unresolved. Not used by the first report.

### M5 Feddersen & Sandroni: the socially best turnout is small
- First pass said: not stated.
- Mark: confirmed (new)
- Source: feddersen; Section 1.1, footnote 2; PDF p. 8 (printed p. 8)
- Quote: "whereas the social optimal level of turnout is necessarily small."
- Note: this is the authors' stated reason that a public-goods analogy to voluntary contribution fails for elections; the first report's row 3.5 "group benefit can exceed group cost" should be read with it: in this paper the group's benefit comes from a cost-minimising cut-off, and the social optimum for a large election is small turnout.
