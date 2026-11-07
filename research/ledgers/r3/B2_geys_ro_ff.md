# B2: Geys (2006), arXiv 2510.24344, Riker & Ordeshook (1968) and Ferejohn & Fiorina (1974) Cambridge pages, Wikipedia "Paradox of voting"; and the trail of who said what about `R = PB − C + D`

Reader: Sonnet 5.5 research reader, batch B2. No network used. Repository not touched. Scratch copies with page markers: `SCRATCH/b2/` (geys.txt, arxiv2510.txt, cup_ro1968.txt, cup_ff1974.txt).

## Sources read

| source_id | what it is | size | read in full? |
|---|---|---|---|
| `geys` | Geys (2006), PSR 4: 16-35, the journal's typeset PDF ("© 2006 The Author / Journal compilation © 2006 Political Studies Association"; PDF metadata title `psr_34`), hosted by uh.edu lecture materials | 10,944 words; 20 PDF pages (the extractor's text.txt has a 21st empty page after the last form feed) | Yes: every page including notes 1-23 and the reference list |
| `arxiv2510` | arXiv 2510.24344v1 [econ.GN], 28 Oct 2025, Mostafa Raeisi Sarkandiz (Univ. of Palermo), "Are They Willing to Participate? A Review on Behavioral Economics Approach to Voters Turnout"; the arXiv-served PDF | 6,391 words; 12 PDF pages (printed 1-12) | Yes: every page including references |
| `cup_ro1968` | Cambridge Core landing page (HTML), R&O 1968, APSR 62(1): 25-42, DOI 10.2307/1953324; page render date 2026-11-05. Shows the opening paragraph (labelled "Extract") and the 24 numbered notes (listed under the page's "References" heading). Body is paywalled: "Article purchase / Temporarily unavailable" | 3,066 words (most is page boilerplate) | Yes: whole page text |
| `cup_ff1974` | Cambridge Core landing page (HTML), F&F 1974, APSR 68(2): 525-536, DOI 10.2307/1959502; render date 2026-11-06. The URL in the report redirected to this page. Abstract and 21 notes; body paywalled | 2,175 words | Yes: whole page text |
| `wiki_paradox` | Wikipedia "Paradox of voting", oldid=1368673256, last edited 2026-08-10. A pointer, not a true source | 1,841 words | Yes (most is navigation boilerplate) |

For task 2 I also grepped `-i "riker\|ordeshook"`, `Downs`, `calculus of voting`, `civic duty|citizen duty`, and formula shapes over every `SRC/*/text.txt` and read each hit in context (sources outside my batch are cited only for what they say about this trail).

**Page convention.** Geys: PDF page k = printed page k + 15 (PDF p. 1 = printed p. 16). arXiv: PDF page = printed page. Cambridge pages are HTML: no pages; I give the note number (fn.).

**Two global notes on the first report's quotes.** (a) The report prints straight quotes and apostrophes where the sources have curly ones (’ ‘); a character-exact check will fail on those unless normalised. (b) Where the PDF text breaks a word at a line end, text.txt keeps a hyphen and a space ("util- ities"); my quotes copy that as it is.

**Reasons.** Tasks 1-3 of the batch brief come without a reason of their own; I took common.md's (the site's model rests on facts actually read; the fork points). Said here as CLAUDE.md asks.

**Short answer to task 2 (details in Part 2).**
1. Geys's eq. (2) is printed `R = PB − C + D`, and Geys says R&O "reformulated the original equation into" it (Geys PDF p. 4, printed p. 19). Yes.
2. That D is R&O's symbol and is tied to citizen duty is established as an attribution (not as R&O's printed formula), supported by R&O's own notes 15 and 16 (a quantity D with "high and medium D" categories, and the SRC "sense of citizen duty scale"; the two notes together tie D to that scale, though no single sentence says "D is measured by the scale" [I]) and by six later texts (Geys, arXiv, Coate & Conlin, Gibson et al., Feddersen & Sandroni, Hamlin & Jennings; I cannot tell whether they copy one another), which describe it with different words (expressing oneself; civic duty; consumption benefit; "duty" payoff; doing one's duty).
3. R&O's own equation was NOT seen. The page gives only the opening paragraph and the 24 notes. The notes show symbols P, B, C, D and equation numbers (1), (5), (7), (21), but no equation. Whether R&O wrote `R = PB − C + D` (letters, order, an R at all) is unverified. Among the downloaded texts the order `PB − C + D` is printed only by Geys; Gibson et al. print `C < PB + D`, Coate & Conlin `pB + d` against `c`. The report's sources for `PB + D − C` (Sanders) and `(PB) − C + D` (Salka) were not downloaded (HTTP 404 for both), nor was Dowding (HTTP 403).
4. No downloaded text prints Downs's own formula. Later texts credit Downs with originating the calculus of voting (Geys eq. 1; Kselman et al.; Goldman fn 1; Wikipedia; Coate & Conlin credit it to Downs and R&O jointly), and R&O's note 7 says Downs "cannot include 'non-political' benefits (i.e. those calculated in (7) but not in (1))".

---

# Part 1. Facts the first report states about these sources

### G01 Geys eq. (1)
- First pass said: Geys eq. (1) `R = PB − C > 0` (report line 32).
- Mark: confirmed
- Source: geys; https://www.uh.edu/hobby/eitm/_docs/past-lectures/2014-Lectures/Jeremy-Gilmore/Rational-Theories-of-Voter-Turnout.pdf; section "Foundations: Instrumental Voting", eq. (1); PDF p. 2 (printed p. 17)
- Quote: "the ‘expected utility’ model of voter turnout (Downs, 1957) states that a voter, in deciding whether to vote or abstain, calculates the expected utility of either action"
- Quote: "R = PB − C > 0 (1)"
- Note: Geys credits the model to Downs (1957) but does not say Downs printed it in these letters; the letters R, P, B, C are Geys's text. Geys calls PB "the benefits from voting": "The benefits from voting (PB) have two elements." So in Geys B is the difference in expected utilities (the gain if decisive) and PB is the expected benefit; this bears on the B-versus-pB fork.

### G02 Geys definitions of R, P, B, C (page)
- First pass said: R "represents the net expected utility of voting"; P "the probability (P) that one's vote influences the outcome"; B "stands for the difference in expected utilities from the policies of the two candidates"; C "refers to the costs of voting"; D "stands for the benefit from expressing oneself" (p. 19) (report line 32).
- Mark: corrected
- Source: geys; same URL; "Foundations: Instrumental Voting"; PDF p. 2 (printed p. 17); D is on PDF p. 4 (printed p. 19)
- Quote: "In this equation, R represents the net expected utility of voting."
- Quote: "B stands for the difference in expected util- ities from the policies of the two candidates."
- Quote: "These benefits have to be weighed with the probability (P) that one’s vote influences the outcome."
- Quote: "Finally, C refers to the costs of voting."
- Correction: "(p. 19)" for all five terms → R, P, B, C are defined on printed p. 17 (PDF p. 2); only D is on printed p. 19 (PDF p. 4). The wording of the report's quotes is verbatim (apart from straight apostrophes; "util- ities" is a line-end hyphen).
- Note: Geys's footnote 3 (PDF p. 14, printed p. 29), attached to the B sentence, limits the model: see S2.

### G03 Geys eq. (2) and D
- First pass said: eq. (2) `R = PB − C + D`; D "stands for the benefit from expressing oneself" (p. 19); "The brief's `R = PB − C + D` is Geys's eq. (2)" (report lines 32, 45, 314).
- Mark: confirmed
- Source: geys; same URL; section "Consumption Benefits of Voting", eq. (2); PDF p. 4 (printed p. 19)
- Quote: "Riker and Ordeshook (1968), for instance, reformulated the original equation into:"
- Quote: "R = PB − C + D (2)"
- Quote: "where D stands for the benefit from expressing oneself."
- Note: Geys attributes the reformulation to R&O (1968) and gives the gloss of D in his own voice; he does not say R&O printed the letters R, P, B, C, D or this order. The "original equation" is Geys's eq. (1), which he attributes to Downs. This confirms "Geys's eq. (2) is `R = PB − C + D`" and nothing about R&O's page.

### G04 D is added after PB − C and not multiplied by P
- First pass said: "the D term is added after it and is not multiplied by p" (report line 44, naming Geys among four sources).
- Mark: confirmed
- Source: geys; same URL; PDF p. 4 (printed p. 19)
- Quote: "First, because it still holds that P, and thus PB, is close to zero, equation (2) can be reduced to R = D − C."
- Note: for Geys, D enters additively and PB is dropped as near zero. The same passage says what this implies for the model: it is the first of the two reasons quoted in G19.

### G05 Downs known through Geys (p. 17)
- First pass said: Downs (1957) "Known only through Geys (p. 17), Dowding, Sanders, Salka" (report line 39).
- Mark: confirmed
- Source: geys; same URL; PDF p. 1 (printed p. 16) and PDF p. 2 (printed p. 17)
- Quote: "the instrumental voter axiom predicts large-scale abstention because no individ- ual is likely to have an influence on the election outcome (Downs, 1957)."
- Quote: "the ‘expected utility’ model of voter turnout (Downs, 1957) states that a voter, in deciding whether to vote or abstain, calculates the expected utility of either action"
- Quote: "Downs (1957) argued that if no one votes, the democratic system fails."
- Quote: "Note, finally, that Downs’ (1957) model predicts that ‘voters will be dispropor- tionately drawn from the extremes of the political distribution’ (Brennan and Hamlin, 1998, p. 154)."
- Note: besides eq. (1) Geys gives Downs: that information costs are minor (G13, G14); a "consumption" benefit of voting in the survival of democracy (the sentence quoted above on printed p. 18 goes on, on printed p. 19, to "value of the increased chance of the survival of democracy", and footnote 7 says it does not rescue the model, S4); and the extremes prediction. All are Geys's account; Downs's text is unread. The "consumption" benefit Geys credits to Downs is a different thing from the D he credits to R&O as "expressing oneself" (G03), though he lists both under "Consumption Benefits of Voting".

### G06 Geys on tautology, as the report words it
- First pass said: Geys adds that D "can be tautological unless its sources are specified" (extractor's paraphrase, p. 19) (report line 45).
- Mark: corrected
- Source: geys; same URL; PDF p. 4 (printed p. 19); the broader statement PDF p. 13 (printed p. 28)
- Quote: "Importantly, the ‘expressive’ voter hypothesis will necessarily be tautological unless we can identify the reasons why some people wish to express a preference and others do not."
- Quote: "The first approach – assuming that people derive benefits from voting itself – removes all predictive capacities from the model and makes it tautological."
- Correction: the words in quotation marks ("can be tautological unless its sources are specified") are not in Geys. The p. 19 sentence is about the "expressive" voter hypothesis, says "necessarily", and the condition is identifying "the reasons why some people wish to express a preference and others do not". Page is right (p. 19).
- Note: see S4 for the rest of Geys on this.

### G07 Do sources disagree on what D is: Geys versus "citizen duty"
- First pass said: sources disagree: "Citizen duty" (Sanders; the arXiv review) versus "benefit from expressing oneself" (Geys) (report line 45; line 297).
- Mark: corrected
- Source: geys; same URL; PDF p. 4 (printed p. 19)
- Quote: "where D stands for the benefit from expressing oneself."
- Quote: "In the former case, a voter turns out because he or she feels morally obliged to do so (that is, ‘civic duty’)."
- Quote: "Whereas the utility one derives from compliance with the ethics of voting is independent of the candidate one votes for, the utility from expressing a preference amongst the candidates is choice specific"
- Correction: Geys's D is not set against citizen duty. His one gloss has two readings, "compliance with the ethics of voting" (which he equates with "civic duty") and "expressing a preference amongst the candidates" ("cheer"/"boo"). The report lists Geys as one rival of "citizen duty"; in Geys the civic-duty reading is inside D.
- Note: the report's own disagreement (the arXiv review says "civic duty"; Coate & Conlin: "civic duty or expressing his preference") is partly one of emphasis; see Part 2.

### G08 Geys on the level and the margin
- First pass said: Geys: "it appears highly implausible that the level of real turnout rates can be explained on instrumental grounds" (p. 18); but it fits differences in turnout better than levels (report line 52).
- Mark: confirmed
- Source: geys; same URL; PDF p. 3 (printed p. 18)
- Quote: "it appears highly implausible that the level of real turnout rates can be explained on instrumental grounds"
- Quote: "Although Downs’ (1957) model is unsuccessful at explaining turnout levels, it performs much better in explaining differences in turnout at the margin"
- Note: [I] "at the margin" here seems to mean differences in turnout between groups or elections (the next sentence gives costs and closeness), not a marginal vote.

### G09 Geys on minimax regret: the rule
- First pass said: "The rule here is to choose the action that yields a minimal regret in a worst-case scenario" (p. 21) (report line 59).
- Mark: confirmed
- Source: geys; same URL; section "Minimax Regret"; PDF p. 6 (printed p. 21)
- Quote: "The rule here is to choose the action that yields a minimal regret in a worst-case scenario."

### G10 Geys on F&F: risk versus uncertainty
- First pass said: "the decision to vote is not made under risk, but under uncertainty" (p. 21) (report line 59).
- Mark: confirmed
- Source: geys; same URL; PDF p. 6 (printed p. 21)
- Quote: "assert that the decision to vote is not made under risk, but under uncertainty"

### G11 Geys on F&F: turnout prediction and "(much) less satisfactory"
- First pass said: it predicts higher turnout than expected utility, but "several other predictions are (much) less satisfactory", p. 21 (report line 59).
- Mark: confirmed
- Source: geys; same URL; PDF p. 6 (printed p. 21)
- Quote: "model predicts higher levels of voter turnout than the expected utility model; several other predictions are (much) less satisfactory."
- Quote: "and that turnout is indepen- dent of the closeness of the election, are in contrast to the results from empirical analyses (see above)."
- Note: the second quote is one of Geys's listed failures (turnout independent of closeness).

### G12 Geys gives the regret rule in words only, no formula
- First pass said: "Geys describes the rule in words only, no formula" (report line 59).
- Mark: confirmed
- Source: geys; same URL; PDF p. 6 (printed p. 21)
- Quote: "can be defined as ‘the difference between what the decision maker could have attained had he known the true state of the world before he chose his action and what he actually gets by choosing ai’"
- Quote: "(Ferejohn and Fiorina, 1974, p. 928)"
- Note: this is the only definition of regret in Geys, with symbols R_i,j, a_i, S_j and no formula for the decision rule. [Anomaly] Geys cites F&F p. 928, but his own reference list gives F&F as "68, 525–36" and the Cambridge page says pp. 525-536; p. 928 is outside the article, so it is a misprint in Geys (probably 528). Do not copy it.

### G13 Geys on Downs and Aldrich on costs (the quoted sentence)
- First pass said: Geys p. 18: "Downs (1957) and Aldrich (1993) argue that these costs are only minor." (report line 61)
- Mark: confirmed
- Source: geys; same URL; PDF p. 3 (printed p. 18)
- Quote: "Although Downs (1957) and Aldrich (1993) argue that these costs are only minor"
- Note: the report's words are a verbatim part of a longer sentence; "these costs" refers to the pre-election-day costs (see G14). The sentence continues with a contrary claim: "Converse (1964, 1970, 2000) has repeatedly argued that citizens’ limited capabilities to accomplish political tasks may cause these costs to be significant" (quoted in S3).

### G14 "Downs and Aldrich treat costs as small"
- First pass said: "Downs and Aldrich treat costs as small ('these costs are only minor', Geys p. 18)" (report line 211).
- Mark: corrected
- Source: geys; same URL; PDF p. 3 (printed p. 18)
- Quote: "there are costs that a voter makes before the election day (and which are sunk at the time of the elec- tion) for, say, gathering information about the candidates, their policy proposals and so on."
- Quote: "Several authors have claimed these costs to be small (Niemi, 1976; Palfrey and Rosenthal, 1985; Aldrich, 1993)."
- Correction: in Geys, Downs and Aldrich are cited as calling the information-gathering costs (the first group, "sunk at the time of the election") minor. For the election-day costs ("shoe leather", time) Geys cites "Several authors" (Niemi 1976; Palfrey and Rosenthal 1985; Aldrich 1993); Downs is not cited there. So "Downs and Aldrich treat costs as small" holds for information costs only; Aldrich also appears for election-day costs.

### G15 Geys among the sources for a tiny P
- First pass said: Geys is a source for pivotality, "estimates of p" (report line 137, list "SEP; Edlin; Gelman; Mulligan & Hunter; Dowding; Geys").
- Mark: confirmed
- Source: geys; same URL; PDF p. 2 (printed p. 17), continuing on PDF p. 3
- Quote: "Because the probability of affecting the outcome (P) is low to non-existent"
- Quote: "Crucially, it does not take much for the costs of turning out to exceed the ben- efits of that action."
- Note: Geys gives no estimate or formula for P himself; he cites Owen and Grofman 1984, Gelman et al. 1998 and Mulligan and Hunter 2003 for it, and in his footnote 4 notes that "Voters may not perceive their influence on the election result to be negligible" (PDF p. 14, printed p. 29).

### G16 Harsanyi quoted in Geys
- First pass said: "Harsanyi (1980): quoted by Geys, 'a rule that would maximize social utility if it were followed by everybody' (pp. 20-21)" (report line 170).
- Mark: corrected
- Source: geys; same URL; PDF p. 6 (printed p. 21); reference list PDF p. 18 (printed p. 33)
- Quote: "assume that people are ‘rule utilitarians’ who receive a warm-glow pay-off from following ‘a rule that would maximize social utility if it were followed by every- body’ (Harsanyi, 1977, p. 626)."
- Quote: "Harsanyi, J. C. (1977) ‘Morality and the Theory of Rational Behavior’, Social Research, 44 (3), 623–56."
- Correction: Harsanyi (1980) → Harsanyi (1977), p. 626, "Morality and the Theory of Rational Behavior", Social Research 44(3): 623-56; "pp. 20-21" → p. 21 (PDF p. 6). The sentence describes Feddersen and Sandroni (2002), not Harsanyi's own argument.
- Note: Coate & Conlin's reference list has a different paper, "[13] Harsanyi, John C., [1980], 'Rule Utilitarianism, Rights, Obligations and ...'" (coate_conlin, reference [13]); the first report's 1980 may come from there. The quote in the report is verbatim ("every- body" is a line-end hyphen).

### G17 Geys on Coate and Conlin's warm glow
- First pass said: Coate & Conlin's warm glow is "restricted to behaving like as should towards people on one's own side of the issue" (p. 20) (report line 173).
- Mark: corrected
- Source: geys; same URL; PDF p. 6 (printed p. 21)
- Quote: "assume that this warm glow from ‘doing one’s part’ towards the common good is restricted to behaving like as should towards people on one’s own side of the issue."
- Correction: p. 20 → p. 21 (PDF p. 6). The quoted words are verbatim.

### G18 Geys on group-based models and the stylised facts
- First pass said: "group-based models of turnout go a long way towards explaining our 'stylised facts'" (p. 24) (report line 173).
- Mark: confirmed
- Source: geys; same URL; section "Group-based Models"; PDF p. 9 (printed p. 24)
- Quote: "Finally, group-based models of turnout go a long way towards explaining our ‘stylised facts’ on voter turnout."

### G19 Geys on D: "a severe price"
- First pass said: D "does so at a severe price", because "the model loses all predictive value" (p. 19) (report line 183).
- Mark: confirmed
- Source: geys; same URL; PDF p. 4 (printed p. 19)
- Quote: "does so at a severe price."
- Quote: "Moreover, as any action can be explained by making the appropriate assumptions post hoc, the model loses all pre- dictive value (Grossman and Helpman, 2001; Mueller, 2003)."
- Quote: "reasons unrelated to the central element of the democra- tic process, namely electing a government."
- Note: "because" in the report merges two separate reasons. Geys gives (First) that eq. (2) reduces to R = D − C so turnout is driven by reasons unrelated to electing a government, and (Moreover) the post-hoc point.

### G20 Fowler as Geys describes him
- First pass said: Geys p. 20: Fowler argues "only those with different preferences... ('discriminating altruists') are motivated to vote by altruism" and gives an altruism-weight utility function (eq. 3, α "the weight we attach to other's happiness"); the report heads the item "Fowler (2006), 'Altruism and turnout', J. of Politics" (report lines 192, 327).
- Mark: corrected
- Source: geys; same URL; PDF p. 5 (printed p. 20); reference list PDF p. 17 (printed p. 32)
- Quote: "only those with different preferences with regard to the ben- efits of some groups within the population (‘discriminating altruists’) are motivated to vote by altruism."
- Quote: "where α is the weight we attach to other’s happiness"
- Quote: "Fowler, J. H. (2005) ‘Altruism and Political Participation’, unpublished manuscript."
- Quote: "Fowler, J. H. (2006) ‘Habitual Voting and Behavioral Turnout’, Journal of Politics, forthcoming."
- Correction: (a) the report's quotation contains an ellipsis inside it, so it is not one verbatim passage; the full wording is above. (b) Geys cites Fowler (2005), an unpublished manuscript "Altruism and Political Participation"; his Fowler (2006) is a different paper ("Habitual Voting and Behavioral Turnout", J. Politics, forthcoming), used for learning models. "Fowler (2006), 'Altruism and turnout'" is not a reference Geys gives. (c) Eq. (3) `W_i = U_i + α Σ U_j` (0 < α < 1) is Geys's own device for ethical preferences in general ("Hence, we could write a given individual’s utility function as:", PDF p. 5, line before eq. 3); it comes before Goodin and Roberts and before Fowler and Geys does not attribute it to Fowler.
- Note: `fowler_wp` in SRC is titled "Altruism and Political Participation" by James H. Fowler (UC Davis); that is probably the manuscript Geys cites (not read by me; another batch's).

### G21 Geys: game theory (pp. 22 and 28)
- First pass said: Geys p. 22: "by resorting to game theory does not succeed" (quoting Mueller), and positive turnout "disappears under realistic assumptions" (p. 28) (report line 201).
- Mark: confirmed
- Source: geys; same URL; PDF p. 7 (printed p. 22) and PDF p. 13 (printed p. 28)
- Quote: "attempt to explain voter turnout ‘by resorting to game theory does not succeed’ (Mueller, 2003, p. 307)."
- Quote: "turnout in game theoretic models disappears under realistic assumptions con- cerning voter information levels"
- Note: the first is Mueller (2003, p. 307) as quoted by Geys. The p. 22 text also says the positive-turnout finding "rests critically upon the assumption that all voters are certain about the voting costs and preferences of other voters".

### G22 Geys: learning (p. 27)
- First pass said: Geys p. 27: "Introducing 'learning' into the voter calculus appears highly promising" but with no empirical evidence yet; "a much-needed avenue of future (experimental) research" (report line 202).
- Mark: confirmed
- Source: geys; same URL; PDF p. 12 (printed p. 27)
- Quote: "Introducing ‘learning’ into the voter calculus appears highly promising with respect to the predictions that flow from the model."
- Quote: "to the best of our knowledge no empirical evidence has as yet been brought forward to substantiate the presence of adaptive reasoning"
- Quote: "avenue of future (experimental) research in this field."
- Note: the source has "much- needed" with a line-end hyphen; the report's "much-needed" is the same word.

### G23 "Turnout falls with increasing costs" (Geys p. 18)
- First pass said: Geys (p. 18): the prediction that "turnout falls with increasing costs" is described as generally supported empirically (extractor's paraphrase) (report line 211).
- Mark: confirmed
- Source: geys; same URL; PDF p. 3 (printed p. 18)
- Quote: "Predictions that turnout falls with increasing costs or rises when elections are more important (that is, with a closer contest or in ‘first-order’ elec- tions) are generally supported in the empirical literature (see above)."
- Quote: "Fourth, voters are more likely to show up under pro- portional electoral systems and when the candidates are in a neck-and-neck race"
- Note: the "(see above)" points to the introduction's list of "stylised facts" (PDF p. 1, printed p. 16: first- versus second-order elections; income, education, partisanship, sex and age; alienation; proportional systems and close races; strategic voting). That list has no cost item. The cost-related citations on p. 18 are for registration only (Rosenstone and Wolfinger 1978; Brians and Carter 1999; Highton 2004). So Geys states the cost-turnout prediction without a citation or data of its own in that sentence.

### G24 Geys on B: "who is counted: the voter"
- First pass said: Geys's B: "the difference in expected utilities from the policies of the two candidates"; who is counted: "the voter" (report line 73).
- Mark: corrected
- Source: geys; same URL; PDF p. 2 (printed p. 17), PDF p. 3 (printed p. 18) and PDF p. 5 (printed p. 20)
- Quote: "B stands for the difference in expected util- ities from the policies of the two candidates."
- Quote: "and the benefits of political action (B) are collective goods"
- Quote: "This is not the case with pure altruism because the benefits derived from this form of altruism work to inflate the B-term in equation (1)."
- Correction: "the voter" (as stated) → Geys does not say whose utilities B counts. The model is a voter's calculus ("a voter ... calculates the expected utility of either action"), so the voter's own is implied for eq. (1) [I]. But Geys states that B is "a collective good" (p. 18) and that pure altruism "work[s] to inflate the B-term in equation (1)" (p. 20), i.e. he lets others' welfare enter B.
- Note: this bears on the "whose welfare is in B" fork. Geys's warm-glow altruism, by contrast, is "very similar to introducing ‘consumption’ benefits" (PDF p. 5): "It, therefore, stands open to all criticisms associated with this approach (see above)."

### G25 What the Geys copy is
- First pass said: Geys (a UH-hosted copy), used with low confidence; "Page numbers are the journal's, per the extractor" (report lines 32, 337).
- Mark: confirmed
- Source: geys; same URL; PDF p. 1 (printed p. 16) and PDF p. 13 (printed p. 28)
- Quote: "POLITICAL STUDIES REVIEW: 2006 VOL 4, 16–35"
- Quote: "© 2006 The Author"
- Quote: "(Accepted: 19 September 2005)"
- Note: the page numbers in the report are the journal's printed numbers (16-35) and I checked each one against the PDF (corrections: G02, G16, G17). It is the journal's typeset PDF, hosted by a university course page, not the publisher's site; the content reads as the published article. Geys's reference list gives the "Geys (2006) Explaining Voter Turnout: A Review of Aggregate-Level Research" as forthcoming, and Dowding (2005) as BJPIR 7(3): 442-59.

### X01 arXiv review: eq. (1) and R&O's D "as a civic duty"
- First pass said: arXiv 2510.24344, sec. 3.1: `ΔU = PB − C`; D added "as a civic duty"; P "the probability that a vote can be decisive"; B "the gain of the individual candidate's victory"; C "the net cost incurred by the individual in the voting process" (report line 36).
- Mark: confirmed
- Source: arxiv2510; https://arxiv.org/pdf/2510.24344; section 3.1 "Voter as a Consumer", eq. (1); PDF p. 3 (printed p. 3)
- Quote: "∆U = P B − C (1)"
- Quote: "Which P represents the probability that a vote can be decisive, B represents the gain of the individual candidate’s victory, and C represents the net cost incurred by the individual in the voting process."
- Quote: "To overcome this impasse, Riker & Ordeshook (1968), in their study, tried to resolve this problem by adding the parameter D as a civic duty."
- Note: no formula containing D is printed anywhere in the review (I read all 12 pages). The sentence before eq. (1) credits Downs with "defining the voters as rational consumers" and ends "(Downs, 1957)"; it does not say Downs wrote ΔU = PB − C. The review is a single-author arXiv v1 preprint (the PDF names no journal and carries no peer-review statement); most of it is about economic voting and a government game, and its eq. (2) is misprinted (see "Found").

### X02 arXiv review: "citizen duty" versus "civic duty"
- First pass said: "Citizen duty" (Sanders; the arXiv review) (report line 45).
- Mark: confirmed
- Source: arxiv2510; same URL; section 3.1; PDF p. 3 (printed p. 3)
- Quote: "Furthermore, Uhlaner (1989), besides the civic duty, added the willing of supporting charismatic leaders or politicians in D."
- Note: the review's words are "civic duty", not "citizen duty" (the latter is R&O's own scale name, fn 15 below). It attributes to R&O the adding of D "as a civic duty", and to Uhlaner (1989) a further content for D.

### X03 What the arXiv review counts in C
- First pass said: C is "the net cost incurred by the individual in the voting process" (report line 36).
- Mark: confirmed
- Source: arxiv2510; same URL; PDF p. 4 (printed p. 4) and PDF p. 7 (printed p. 7), section 4.1 "Direct Costs Reduction"
- Quote: "The cost factor here is severely limited and covers some of the costs, including the cost of being in the voting queue, the cost of gathering information to select an ideal candidate, etc."
- Quote: "Direct election costs include the cost of getting off of home or work to the polls, the cost of the stand in the voting queue (time cost), as well as the cost of gathering information"
- Quote: "Although decreasing these costs can lead to more people’s willingness to participate in the elections, but eliminating all the direct costs cannot lead to full turnout."
- Note: the third is the review's version of "turnout falls with increasing costs" (with postal voting in Switzerland said to raise participation "by about four percent (Luechinger et al., 2007)", PDF p. 8).

### R01 R&O 1968: not read; paywall
- First pass said: R&O: "Not read. Cambridge shows abstract and footnote fragments only; the full text is paywalled" (Cambridge paywall "Temporarily unavailable") (report lines 38, 321).
- Mark: confirmed
- Source: cup_ro1968; https://www.cambridge.org/core/journals/american-political-science-review/article/abs/theory-of-the-calculus-of-voting/F32A6F556750C8207E920CE9D0850A2E; "Access options"
- Quote: "Article purchase Temporarily unavailable"
- Note: what the page shows is the opening paragraph (the page labels it "Extract", not "Abstract") and 24 numbered notes. The original equation(s) are not on the page. The report's statement that `R = PB − C + D` is unconfirmed as R&O's stands.

### R02 R&O's opening paragraph
- First pass said: R&O abstract: "voting is an irrational act in that it usually costs more to vote than one can expect to get in return"; "we present empirical evidence that citizens actually behave as if they employed this calculus."; the abstract goes on to say the reinterpreted calculus makes voting reasonable for those who vote and abstaining reasonable for those who abstain (report line 49).
- Mark: confirmed
- Source: cup_ro1968; same URL; "Extract" (opening paragraph); no page numbers on the HTML page (the article is pp. 25-42)
- Quote: "Much recent theorizing about the utility of voting concludes that voting is an irrational act in that it usually costs more to vote than one can expect to get in return."
- Quote: "We describe a calculus of voting from which one infers that it is reasonable for those who vote to do so and also that it is equally reasonable for those who do not vote not to do so."
- Quote: "Furthermore we present empirical evidence that citizens actually behave as if they employed this calculus."
- Note: the report marked the "reasonable for those who vote ... not to vote" sentence as the extractor's paraphrase; the second quote confirms it in the authors' words. The paragraph also says the paper "is, therefore, an effort to reinterpret the voting calculus so that it can fit comfortably into a rationalistic theory of political behavior".

### R03 R&O notes: "worth B utiles", "constancy of D", "citizen duty scale"
- First pass said: footnote fragments: a favourable outcome is "worth B utiles"; "constancy of D"; a "sense of citizen duty scale" (report line 38).
- Mark: confirmed
- Source: cup_ro1968; same URL; fn. 19, fn. 16, fn. 15
- Quote: "If the vote for the citizen's preferred party is V/2, v even, before he votes, then this outcome is worth B utiles since his vote gives his party v/2 + 1 votes, or enough to win."
- Quote: "The constancy of D is open to some technical question."
- Quote: "The sense of citizen duty scale is fully described in Campbell, A., Gurin, G. and Miller, W. E., The Voter Decides (Evanston, 1954), pp. 194–199"
- Note: in fn. 19 "B utiles" is the worth of the outcome in which the citizen's vote gives his party enough to win. The note does not say whose utility is counted beyond the citizen it describes; "preferred party" is the citizen's. The report's "a favourable outcome" is a paraphrase of this.

### R04 R&O notes: "C and V appear as cost and value"
- First pass said: C and V appear as cost and value (report line 38).
- Mark: corrected
- Source: cup_ro1968; same URL; fn. 9, fn. 13, fn. 14, fn. 19
- Quote: "the party label reduces the cost of decision in the general election to zero."
- Quote: "It is conceivable that some people who have a high P by this operationalization actually view the probability density as continuous so that for them P = 0 rather than P = ½ pr [1; V/2]."
- Correction: "C and V ... cost and value" → C is "the cost of decision in the general election" (fn. 9, where it appears as C 1 < C 2). V is not defined in the notes: in fn. 9 it appears only as "V 1 to be greater than V 2" (undefined), and in fn. 13, 14 and 19 as "V/2", a vote threshold ("If the vote for the citizen's preferred party is V/2"). Nothing on the page says V is "value".
- Note: P appears in fn. 13, 14 and 18 as the quantity "high P" / "low P" and as `P = ½ pr [1; V/2]` (fn. 14). So the page shows R&O's letters P, B, C, D (and V) but not an R.

### R05 R&O fn. 7: what Downs could and could not include
- First pass said: (not in the report; the lead asks for footnote 7 verbatim: "(7) but not in (1)")
- Mark: confirmed
- Source: cup_ro1968; same URL; fn. 7
- Quote: "Downs, of course, recognizes that his is an incomplete analysis of the act of voting."
- Quote: "As a result Downs cannot include “non-political” benefits (i.e. those calculated in (7) but not in (1)) in his analysis, although many of the benefits he cannot include are clearly political."
- Quote: "It seems to us that he is unduly bothered by the tautology, which after all does affirm something, namely that people calculate about their actions and that their calculations can be understood by others."
- Quote: "we will adopt here the broader interpretation of rationality, recognizing its tautological character, in order to develop a theory that may more adequately describe behavior."
- Note: R&O's own words say (i) the analysis they attribute to Downs is incomplete; (ii) R&O's equation (7) calculates "non-political" benefits that equation (1) does not; (iii) R&O adopt a broad, "tautological" sense of rationality knowingly. They do not name D in this note, so that (7) contains D is an inference [I], though fn. 15-16 (R06) tie D to a measured non-outcome quantity. "Non-political" is the note's word for the benefits Downs excludes; it does not say "citizen duty" or "consumption".

### R06 R&O fn. 15 and 16: D and the citizen-duty scale
- First pass said: the extractor flagged "D is citizen duty" as its inference (report line 38).
- Mark: confirmed
- Source: cup_ro1968; same URL; fn. 15 and fn. 16
- Quote: "The constancy of D is open to some technical question."
- Quote: "The SRC ceased in 1964 to collect the necessary information, first, because the scale of citizen duty turned out to be very similar to the scale of the sense of political efficacy"
- Quote: "Suppose some persons with an actually low D are included (by reason of response set) in our categories I and II of high and medium D."
- Quote: "And if low D is associated with not caring about the outcome of the election so that these low D's add disproportionately to the non-carers"
- Note: this is now stronger than "the extractor's inference". R&O's own notes speak of "high and medium D" and "low D" categories and of the "constancy of D", and the same note 16 explains that the SRC stopped collecting "the necessary information" because of the citizen-duty scale (fn. 15 names that scale). Read together they tie D to the SRC sense-of-citizen-duty scale [I: no single sentence says "D is measured by the scale"]. What the notes do not give is D's role in the voting equation or its sign. [I] The inference that D enters their calculus as an outcome-independent term (the sense in which later authors use it) rests on the later authors, not on this page.

### R07 R&O fn. 14, 19, 23, 24: the factor ½ and ties
- First pass said: (not in the report; the lead asks for the notes on the factor ½ verbatim)
- Mark: confirmed
- Source: cup_ro1968; same URL; fn. 14, 19, 23, 24
- Quote: "If, however, v is odd, then, assuming the voter does not value a tie, only until an outcome of (v + 1) /2 + 1 votes is assured"
- Quote: "This result differs by a factor of ½ from our original formulation in equation (21) because we have implicitly assumed v even."
- Quote: "Our original analysis showed however that when v is odd the voter cannot affect the outcome so as to bring about the victory of his preferred candidate."
- Quote: "The gain associated with increasing his favored candidate's chance of winning is offset by increasing the chance of a tie"
- Quote: "Given an equal likelihood for even and odd v we would once again let P = ½pr v [1; v/2]."
- Quote: "If we assumed the voter equally valued creating a tie to having his preferred candidate win then we would drop the ½ once again."
- Quote: "Or if one wishes ½pr v [1; v/2]."
- Note: as the notes read [I], R&O's ½ comes from averaging over whether the number v of voters (before the citizen votes) is even or odd, with a tie not valued ("assuming the voter does not value a tie"): for v even his vote wins, for v odd it can at most create a tie; with equal likelihood of the two, P = ½ pr_v[1; v/2]; and the ½ is dropped if creating a tie is valued as much as winning. That is a different route to a ½ from the coin-flip route of Gelman-King-Boscardin and Barnett (report 2.2), reaching the same factor under a symmetric assumption; the notes do not mention a coin or a recount. The notes also show that R&O's P is a subjective probability: "since we are dealing with subjective probabilities" (fn. 10, quoted in "Found"). Their equation (21) is not on the page.

### R08 What R&O say Downs contributed
- First pass said: (not in the report; the lead asks what the texts say Downs contributed)
- Mark: confirmed
- Source: cup_ro1968; same URL; fn. 1, fn. 2, fn. 4, fn. 6
- Quote: "The two most interesting presentations of this analysis are"
- Quote: "Downs, Anthony, An Economic Theory of Democracy (New York: Harper, 1957), pp. 36–50, 260–276"
- Quote: "Downs refines (5) considerably and we refer the reader to his work cited, pp. 38–47, for the full presentation."
- Quote: "In Downs' theory, which he characterizes as “positive, but not descriptive,” there is no reason to expect descriptive accuracy"
- Note: "this analysis" in fn. 1 is the "customary" analysis in the text (fn. 4 says "customarily" refers to "not only ... the work of Downs and Tullock, but also ... numerous unpublished analyses"); Downs's and Tullock's (1968, ch. 7) are the "two most interesting presentations". Fn. 6 says Downs "refines (5) considerably" on pp. 38-47, so (5) is R&O's presentation of the analysis they take from him [I]. Whether (5) is `PB − C` is not stated on the page [I: likely, not shown].

### F01 F&F: formula not read; paywall
- First pass said: F&F: "Formula not read. Abstract and some footnotes only" (report lines 40, 322).
- Mark: confirmed
- Source: cup_ff1974; https://www.cambridge.org/core/journals/american-political-science-review/article/abs/paradox-of-not-voting-a-decision-theoretic-analysis/0F89DD7019DEC0A1D8B0F4F33CB69CBE (the URL in the report redirects here); "Access options"
- Quote: "Article purchase Temporarily unavailable"

### F02 F&F abstract: voting under quite general conditions; two and three candidates
- First pass said: minimax regret "specifies voting under quite general conditions", for two- and three-candidate plurality elections (report line 57).
- Mark: confirmed
- Source: cup_ff1974; same URL; Abstract (no pages on the HTML page; the article is pp. 525-536)
- Quote: "In this paper we show that an alternative criterion for decision making under uncertainty, minimax regret, specifies voting under quite general conditions."
- Quote: "Both two and three candidate plurality elections are considered."
- Note: the abstract also states the paradox F&F start from: "Put simply, the probability that a citizen's vote will affect the outcome is so small that the expected gains from voting are outweighed by the costs in time and effort."

### F03 F&F abstract: second choice in a three-candidate election
- First pass said: a minimax-regret voter "never votes for their second choice in a three-candidate election", while expected-utility maximisers sometimes do (report line 57).
- Mark: corrected
- Source: cup_ff1974; same URL; Abstract
- Quote: "Interestingly, a minimax regret decision maker never votes for his second choice in a three candidate election, whereas expected utility maximizers clearly may."
- Correction: "never votes for their second choice in a three-candidate election" → "never votes for his second choice in a three candidate election" (his; no hyphen in "three candidate"). The report's quoted words are not verbatim.

### F04 F&F fn. 12: c < ½
- First pass said: the authors assume the cost is below half the utility gap between one's preferred candidate winning and losing ("c < ½") (report line 58).
- Mark: confirmed
- Source: cup_ff1974; same URL; fn. 12
- Quote: "In computing regrets we assume c < ½, i.e., the utility cost of voting is less than ½ the utility difference between having one's preferred candidate in office rather than his opponent."
- Quote: "Essentially we are analyzing average voters, those who have a preference for C 1 or C 2, and for whom the costs of voting are the typical costs in time and effort."
- Note: this ½ is a bound on the cost relative to the utility difference; it is not a tie factor. Do not mix it with the ½ of R&O fn. 23.

### F05 F&F fn. 12: "abstaining would dominate voting"
- First pass said: without it "abstaining would dominate voting" (report line 58, in quotation marks).
- Mark: corrected
- Source: cup_ff1974; same URL; fn. 12
- Quote: "The assumption is necessary, of course, because from Table 2 one sees that unless it is satisfied one never votes: A would dominate V 1 as well as V 2."
- Correction: "abstaining would dominate voting" → "unless it is satisfied one never votes: A would dominate V 1 as well as V 2". The phrase in quotation marks is not in the source; "A" is the abstain strategy by fn. 19 below, "V 1" and "V 2" are voting for candidate 1 or 2 [I: from fn. 19, where A has worst outcome 0 and V's have −c].

### F06 F&F: regret tables and voting condition not visible
- First pass said: the regret tables and the exact voting condition were not visible (report line 58).
- Mark: confirmed
- Source: cup_ff1974; same URL; fn. 19
- Quote: "In Table 2, the worst outcomes for V 1, V 2, and A are —c, —c, and 0, respectively."
- Note: tables 2 and 4 are referred to in fn. 12 and fn. 19 but are not on the page. Fn. 19 shows the payoffs: voting costs −c in its worst case, abstaining 0.

### F07 F&F on more than two candidates
- First pass said: F&F's abstract (1.3) treats the multi-candidate case as different (report line 107).
- Mark: confirmed
- Source: cup_ff1974; same URL; fn. 13 and fn. 12
- Quote: "For a more extensive analysis of the voting behavior of expected utility maximizers in multicandidate contests see"
- Quote: "Analogous considerations lead us to make the same assumption in the three-candidate case."
- Note: fn. 13 sends the reader to McKelvey and Ordeshook (1972), "A General Theory of the Calculus of Voting" and says F&F's conclusions "seem consonant with theirs"; that paper is also what Geys fn. 3 cites (S2).

### W01 Wikipedia "Paradox of voting" (pointer only)
- First pass said: Wikipedia (pointer only), URL fetched and returned the intended document (report lines 20, 337); no fact in the report is cited to this page.
- Mark: confirmed
- Source: wiki_paradox; https://en.wikipedia.org/wiki/Paradox_of_voting; sections "History of scholarship" and "Civic duty"
- Quote: "This problem in modern public choice theory was analysed by Anthony Downs in 1957.[4]"
- Quote: "U = B ⋅ p − C"
- Quote: "is the benefit of a pivotal vote,"
- Quote: "Civic duty can be represented in the rational voter model as an additional benefit to voting independent of casting a pivotal vote.[5]"
- Note: the page never mentions Riker or Ordeshook (grep finds no hit) and prints no D; it prints `U = B ⋅ p − C` with B "the benefit of a pivotal vote" (the gain-if-decisive reading of B), citing [5] François & Gergaud (2019), "Is civic duty the solution to the paradox of voting?", Public Choice 180: 257-283. Not a true source; its only use is to show how a popular source words B.

---

# Part 2. Who is the formula and who is D? Every attribution in the downloaded texts

Each entry is a text that says something about Downs, Riker & Ordeshook, the formula, the terms P, B, C, D or citizen duty. Geys, the arXiv review, the R&O page and the F&F page are in Part 1 (G03, G05, X01, X02, R03-R08). Entries here: T01 Coate & Conlin, T02 Gibson et al., T03 Feddersen & Sandroni, T04 Kselman et al., T05 Hamlin & Jennings, T06 Goldman, T07 Edlin et al., T08 SEP, T09 minor mentions, T10 the three sources that were not downloaded.

### T01 Coate & Conlin: pB + d, credited to Downs and R&O together
- First pass said: (not in the report for this point; the report cites Coate & Conlin on p. 5 for "d no smaller than c", line 201, and for the rule-utilitarian model, line 171)
- Mark: confirmed
- Source: coate_conlin; https://www.nber.org/system/files/working_papers/w8720/w8720.pdf (the NBER working paper); introduction; PDF p. 5 (printed p. 4)
- Quote: "The well-known calculus of voting model of turnout (Downs (1957), Riker and Ordeshook (1968)) defines the benefits of voting as pB + d where p is the probability of swinging the election"
- Quote: "B is the gain from having one’s preferred candidate win, and d is the benefit a citizen feels from doing his civic duty or expressing his preference."
- Quote: "A voter votes if these benefits exceed the direct cost of voting, denoted c, which includes the time taken to get to the polls and so on."
- Note: the formula as printed is the inline `pB + d` against a separate `c`; no equation number. The authors do not split Downs's contribution from R&O's. D here is "civic duty or expressing his preference" (lower-case d), the same two readings as Geys. B is "the gain from having one’s preferred candidate win", a gain if decisive, not pB. C (c) is "the direct cost of voting ... the time taken to get to the polls and so on".

### T02 Gibson, Kim, Stillman & Boe-Gibson (IZA DP 5854): C < PB + D, "at least since R&O"
- First pass said: (not in the report for this point; the report uses this paper for NZ travel cost, line 232)
- Mark: confirmed
- Source: iza5854; https://docs.iza.org/dp5854.pdf; Introduction; PDF p. 4 (printed p. 1)
- Quote: "One solution to this paradox of voting, used at least since Riker and Ordeshook (1968), is to assume some additional (consumption) benefit from voting."
- Quote: "and allowing for the consumption benefit (D) that results from the feeling of satisfaction in performing one’s civic duty: C < PB + D."
- Note: the display is unnumbered and is an inequality, not an equation for R. Here D is the "consumption benefit" from "performing one's civic duty", credited to R&O only as "used at least since"; it does not say R&O wrote this formula.

### T03 Feddersen & Sandroni (April 2002 draft): R&O's "duty" payoff D > 0
- First pass said: (not in the report for this point; the report uses this draft at line 172)
- Mark: confirmed
- Source: feddersen; https://www.kellogg.northwestern.edu/faculty/fedderse/homepage/papers/duty4-15-02.pdf; PDF p. 4 (printed p. 4); also PDF p. 3, 5 and 25 (printed pages equal PDF pages)
- Quote: "Riker and Ordershook (1968) analyze a model of participation in which agents receive a “duty”"
- Quote: "D > 0 when they vote for their preferred candidate."
- Quote: "In their model the action an agent should take is de- termined exogenously."
- Quote: "levels are fixed and independent of the relative size of the minority."
- Quote: "increases in costs to vote can have significant impact on turnout levels (Riker and Ordeshook (1968))"
- Quote: "In such a model turnout is determined by the fraction of the electorate with cost to vote less than D."
- Note: the word between the first two quotes is "payoff" (printed with the ligature ﬀ in text.txt, left out of the quotes so a ligature-normalising check cannot trip on it). Here R&O's D is a "duty" payoff, positive, received when voting for one's preferred candidate; with no P and no B in the description. The draft then says that, in such a decision-theoretic model "along the lines of Riker and Ordeshook (1968)", turnout is set by the fraction of the electorate with cost below D (PDF p. 25), i.e. D is compared with the cost alone. The last quote (PDF p. 3) is an attribution to R&O of an empirical cost-to-turnout effect, relevant to the "turnout falls with increasing costs" item; the R&O page's own paragraph reports "empirical evidence" (R02) but the page does not show this finding.

### T04 Kselman, Niou & Wang (2020): "first proposed by Downs and formalized by R&O"
- First pass said: (the report cites Kselman for the three-candidate pivot condition, line 106, not for this attribution)
- Mark: confirmed
- Source: kselman; https://dukespace.lib.duke.edu/server/api/core/bitstreams/672a2c09-26d4-4f6b-923a-7b2da6ccdd60/content; section 3; PDF p. 4 (printed p. 4). The text is in two columns, so the sentence is split across interleaved lines in text.txt; I give it as two quotes.
- Quote: "The Calculus of Voting (COV) is an expected utility model of voting behavior applicable to winner-take-all elections, and was first proposed by Downs (1957) and formalized by Riker and"
- Quote: "Ordeshook (1968) and McKelvey and Ordeshook (1972)."
- Note: no D is mentioned; the paper uses the COV for strategic choice among three candidates (its inequality (4), with a factor 2 on p12), not for turnout.

### T05 Hamlin & Jennings (2011): "expressive choice as doing one's duty", developed by R&O
- First pass said: (not in the report for this point; the report uses this paper for expressive voting, lines 182, 186)
- Mark: confirmed
- Source: hj_pdf; https://strathprints.strath.ac.uk/27852/1/Hamlin_and_Jennings_final.pdf; section 3; PDF p. 15 (printed p. 15); note 6 on PDF p. 33
- Quote: "This is the idea of ‘expressive choice as doing one’s duty’ developed by Riker and Ordeshook.20"
- Quote: "This approach proposes that voters express their respect for duty through voting."
- Quote: "(1968), 25-42, who focus on duty"
- Note: this is the only text that calls R&O's D "expressive" (duty-expression); the text says it "provides a reason for voting, but carries no implications for how to vote". In the same note 6 the other strands are assigned to others: "ethical voting" to Tullock and to Goodin and Roberts, party allegiance to Fiorina (1976), and a general account to Brennan and Buchanan (1984).

### T06 Goldman (Cambridge page): Downs's "party differential"; R&O's p = 10^-8
- First pass said: Riker & Ordeshook "made it 10⁻⁸" (n. 6), via Dowding (report line 274)
- Mark: confirmed
- Source: cup_goldman; https://www.cambridge.org/core/journals/social-philosophy-and-policy/article/abs/why-citizens-should-vote-a-causal-responsibility-approach/6628D3915B2973208BBD49C15C90394B; fn. 1 (HTML page, no page numbers)
- Quote: "William Riker and Peter Ordeshook have estimated the probability of an individual voter being decisive to the outcome of a U.S. presidential election as p = 10–8–that is, a 1 in 100,000,000 chance."
- Quote: "Perhaps the earliest formulation of the economic approach is due to Downs"
- Quote: "Downs formulates matters in terms of the “party differential” rather than the differential between the two individual candidates, but this difference is incidental."
- Note: an independent attribution, in a second text, of the 10^-8 to R&O (the report had it only through Dowding, which was not downloaded). It also credits Downs, not R&O, with "the earliest formulation of the economic approach" (Downs ch. 14) and says Downs's B is a party differential.

### T07 Edlin, Gelman & Kaplan (NBER w13562): R&O listed; C and D "often written in two parts"
- First pass said: Edlin et al. eq. 1 `ΔU = pB − c`, c net cost "the costs, minus the direct benefit of voting" (p. 4) (report line 34)
- Mark: confirmed
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; PDF p. 4 (printed p. 3) and PDF p. 5 (printed p. 4), fn. 4
- Quote: "the probability that a vote is decisive is too low for voting to be “worth it” in an expected utility sense (see Downs, 1957, Riker and Ordeshook, 1968, Ferejohn and Fiorina, 1974,"
- Quote: "This last term is often written in two parts, separating the direct costs C and direct benefits D, but we shall only need to work with the difference or net cost, c = C − D."
- Note: Edlin et al. attribute the "too low" finding to a list of authors (Downs, R&O, F&F, others) and attribute the C/D split to no one ("often written"). They fold D into c = C − D. They do not credit D to R&O.

### T08 SEP: no R&O; paradox of voting from Downs; insurance against collapse from Downs
- First pass said: SEP sec. 1.1 `U_v = p[V(D) − V(R)] − C` (report line 31)
- Mark: confirmed
- Source: sep; https://plato.stanford.edu/entries/voting/; sections 1 and 1.1 (no R&O anywhere in the text)
- Quote: "U_v = p[V(D) - V(R)] - C"
- Quote: "one early hypothesis was that voting might be a form of insurance, meant to to prevent democracy from collapsing (Downs 1957: 257)"
- Note: in SEP "D" and "R" are the two candidates (Democrat, Republican), not the D term; do not confuse. SEP credits Downs (1957: 257) with the democracy-insurance hypothesis, the same consumption-type benefit Geys credits to Downs (PDF p. 3-4).

### T09 Minor mentions (no formula, no D)
- First pass said: (not in the report)
- Mark: confirmed
- Source: scispace; https://scispace.com/pdf/two-egocentric-sources-of-the-decision-to-vote-the-voter-s-x8k3uughbj.pdf; PDF p. 3
- Quote: "Other theorists have suggested that people, perhaps mistakenly, believe that their individual votes are relevant (Riker & Ordeshook, 1968)."
- Note: Acevedo and Krueger attribute to R&O a different thing, that voters may mistakenly believe their votes are relevant. `barnett` (note 24, PDF p. 11) lists R&O 1968 among works on modelling the probability of being decisive ("Some authors have proposed alternative ways to model large elections"); `gkb98` (PDF p. 2) cites R&O in a string of sources for "irrational" to vote (two-column layout, no clean quote); `cup_bm2011` lists only R&O's 1973 book in its references. None gives a formula.

### T10 Sanders, Salka and Dowding were not downloaded
- First pass said: Sanders (1980) writes "R = PB + D − C will usually be positive" (p. 855) and "'D' (for 'citizen duty')" (report line 33); Salka (2017): R&O revised `u(V) = (PB) − C + D` (line 37); Dowding `pB + D > C` (line 35)
- Mark: unread
- Source: sanders (https://newschoolhistories.org/wp-content/uploads/2018/04/sanders_onvoting.pdf: HTTP 404, page "Page not found"), salka (https://www.wpsanet.org/papers/docs/WPSA%20-%20Salka%202017.pdf: HTTP 404), dowding (https://core.ac.uk/download/156636542.pdf: HTTP 403 "Just a moment...")
- Note: no text for these is in SRC. The report's most explicit attribution of "D (for 'citizen duty')" to R&O (Sanders) and of `(PB) − C + D` to R&O's revision (Salka) therefore cannot be checked in this corpus; they rest on WebFetch extracts only. The lead may want them re-fetched (another host or a different route for Sanders).

---

# Part 3. What Geys says on the points asked

### S1 The factor ½ and tie treatment in Geys
- First pass said: (not in the report; the lead asks)
- Mark: confirmed
- Source: geys; same URL; all 20 PDF pages (printed pp. 16-35)
- Quote: "he or she is forced to the polls to avoid the unlikely event that this party wins the race by a single vote"
- Quote: "counterbalance the small proba- bility of tipping the balance toward the preferred candidate"
- Note: Geys has no factor ½, no tie, no tie-breaking rule and no treatment of a one-vote margin. A search of the full text for tie, ties, half, ½, pivot, decisive, margin, single vote, one vote and coin finds only: the "single vote" passage above (p. 21); "tipping the balance" (p. 20); the game-theory paragraph (p. 22: "in which case one vote becomes decisive", "the probability of being decisive is not fixed"); the reference-list titles "The Empirical Frequency of the Pivotal Vote" and "When Is Your Vote Decisive?"; and "at the margin" in the senses of G08, the group and learning sections and footnote 5. In Geys, P is "the probability (P) that one’s vote influences the outcome" and is taken from other authors (G15). Nothing here helps with the tie rule; for the ½ see R07 (R&O) and the report's 2.2 (Gelman-King-Boscardin, Barnett).

### S2 Geys on more than two candidates
- First pass said: (the report's 2.4 relies on Rivière, Kselman et al., and F&F; Geys is not cited for it)
- Mark: confirmed
- Source: geys; same URL; fn. 3 on PDF p. 14 (printed p. 29); PDF p. 3 (printed p. 18); PDF p. 6 (printed p. 21)
- Quote: "The model was developed for two candidate plurality elections."
- Quote: "However, McKelvey and Ordeshook (1972) and Geys and Heyndels (2005) argue that a similar model would apply to multi-candidate elections."
- Quote: "Moving to multiparty elections, nothing in the model prevents voters from making strategic choices."
- Note: Geys says eq. (1) is a two-candidate plurality model and that the extension to several candidates exists in the literature (McKelvey and Ordeshook 1972, the paper F&F fn. 13 also cites), but he gives no formula for it and does not discuss pairwise pivot events. He says the model "does not take into account the possible effects from coalition formations that frequently arise in multi-candidate elections" (same note). The only multi-candidate example he gives is the regret-model case of a small disliked third party (S1 first quote).

### S3 What counts as C in Geys
- First pass said: Downs and Aldrich treat costs as small; components of cost (report lines 211-212)
- Mark: confirmed
- Source: geys; same URL; PDF p. 2 (printed p. 17), PDF p. 3 (printed p. 18), PDF p. 7 (printed p. 22)
- Quote: "Hence, any positive cost (C) renders voting an unprofitable venture."
- Quote: "On the other hand, there are costs that the voter incurs on election day. These comprise ‘shoe leather’ costs to get to the polling station and opportunity costs from the time spent in casting a vote."
- Quote: "Moreover, registration procedures, if fulfilled by voters, also involve possibly significant costs"
- Quote: "Converse (1964, 1970, 2000) has repeatedly argued that citizens’ limited capabilities to accomplish political tasks may cause these costs to be significant"
- Quote: "the rational individual once again abstains when he or she has positive net voting costs"
- Note: Geys splits C into (1) costs before election day, "sunk at the time of the election" (G14: information about candidates and policies; registration), and (2) election-day costs (travel, "shoe leather", time spent voting). He does not define C more exactly than "the costs of voting" (G02). He calls the information costs "sunk at the time of the election", which bears on whether they belong in the cost of the marginal decision; he does not draw that conclusion. "Net voting costs" on p. 22 is used without defining "net".

### S4 Is D tautological, in Geys
- First pass said: Geys adds that D "can be tautological unless its sources are specified" (report line 45; corrected in G06)
- Mark: confirmed
- Source: geys; same URL; PDF p. 4 (printed p. 19), PDF p. 11 (printed p. 26), PDF p. 13 (printed p. 28)
- Quote: "Importantly, the ‘expressive’ voter hypothesis will necessarily be tautological unless we can identify the reasons why some people wish to express a preference and others do not."
- Quote: "provide a means to identify the reasons why some people have a preference for voting such that the consumption benefit of voting is made endogenous to the model."
- Quote: "The first approach – assuming that people derive benefits from voting itself – removes all predictive capacities from the model and makes it tautological."
- Quote: "It has been argued that learning mainly affects the D-term from the calculus of voting model (Kanazawa, 2000)."
- Note: Geys's position: a bare D (consumption or expressive benefit with no account of who has it and why) is tautological; the charge is lifted if the model explains the source of D (he names group models, Schuessler's "being" account, and learning models as doing so). R&O's own note 7 accepts a tautology at the level of rationality (R05). Geys's p. 19 also says Downs's own consumption benefit (survival of democracy) does not rescue the model: "This is not the case when adding the benefits of rescuing democracy, proposed by Downs (1957). The reason is that the probability of influencing the survival of the democratic system is infinitesimally small" (fn. 7, PDF p. 14, printed p. 29).

### S5 "Turnout falls with increasing costs"
- First pass said: see G23
- Mark: confirmed
- Source: geys; same URL; PDF p. 3 (printed p. 18)
- Quote: "Predictions that turnout falls with increasing costs or rises when elections are more important (that is, with a closer contest or in ‘first-order’ elec- tions) are generally supported in the empirical literature (see above)."
- Note: the only statement of this form in Geys. It is a stated prediction of the Downsian model, described as "generally supported", with "(see above)" and no data or citation of its own (see G23). The arXiv review states a version in X03 (third quote), and Feddersen and Sandroni attribute a cost effect to R&O (T03).

---

# Corrections table

| Old (first report) | New | Source |
|---|---|---|
| L32: Geys defines R, P, B, C at "(p. 19)" | R, P, B, C: printed p. 17 (PDF p. 2); only D is on printed p. 19 (PDF p. 4) | geys |
| L45: Geys: D "can be tautological unless its sources are specified" (p. 19) | not Geys's words; he says the "‘expressive’ voter hypothesis will necessarily be tautological unless we can identify the reasons why some people wish to express a preference and others do not" (p. 19) | geys |
| L45, L297: Geys's D ("expressing oneself") is a rival of "citizen duty" | Geys's one gloss of D has two readings, compliance with the ethics of voting ("civic duty") and expressing a preference among candidates | geys p. 19 |
| L73: Geys's B counts "the voter" | Geys does not say whose utilities; the voter's is implied for eq. (1); pure altruism "work[s] to inflate the B-term" (p. 20); B is "collective goods" (p. 18) | geys pp. 17, 18, 20 |
| L170: Harsanyi (1980), pp. 20-21 | Harsanyi (1977), p. 626, "Morality and the Theory of Rational Behavior", Social Research 44(3); quote on printed p. 21 | geys p. 21 and reference list |
| L173: Coate & Conlin's warm glow, Geys p. 20 | Geys p. 21 | geys |
| L192: "Fowler (2006), 'Altruism and turnout', J. of Politics"; quoted with an ellipsis; eq. (3) credited to Fowler | Geys cites Fowler (2005) "Altruism and Political Participation" (unpublished manuscript); Fowler (2006) in Geys is "Habitual Voting and Behavioral Turnout"; the full sentence has no ellipsis; eq. (3) is Geys's own | geys pp. 20, 32 |
| L211: "Downs and Aldrich treat costs as small ('these costs are only minor')" | Downs and Aldrich: the pre-election-day information costs; election-day costs "small" per Niemi, Palfrey and Rosenthal, Aldrich | geys p. 18 |
| L38: "C and V appear as cost and value" (R&O notes) | C = "cost of decision" (fn. 9); V undefined, and in fn. 13, 14, 19 "V/2" is a vote threshold | cup_ro1968 |
| L57: F&F "never votes for their second choice in a three-candidate election" | "never votes for his second choice in a three candidate election" | cup_ff1974 abstract |
| L58: without c < ½ "abstaining would dominate voting" (in quotes) | "unless it is satisfied one never votes: A would dominate V 1 as well as V 2" | cup_ff1974 fn. 12 |

Not corrections but flags: the report's quotes use straight quotes where the sources use curly ones; the first pass's "inference" that D is citizen duty (R&O) is now supported by R&O's own notes 15-16 (R06).

# Unread and why

- **R&O 1968 body, including its equations (1), (5), (7), (21) and the definition of D**: paywalled ("Article purchase Temporarily unavailable"); the page gives only the opening paragraph and 24 notes. Needed to settle: whether R&O wrote `R = PB − C + D`, in what order, whether R is their letter, and what D is in their own words.
- **F&F 1974 body** (regret tables 2 and 4, the voting condition): paywalled; the page gives the abstract and 21 notes.
- **Downs (1957)**: not downloaded; the form and order of his calculus and his own treatment of "consumption" benefits are known only through the texts quoted in Part 2.
- **Sanders (1980)** (`PB + D − C`, "citizen duty"), **Salka (2017)** (`(PB) − C + D`), **Dowding (2005)** (`pB + D > C`; costs low "for most people most of the time"): not downloaded (404, 404, 403). The report's lines 33, 35, 37 and 211 (Dowding quote) are unchecked here.
- **Harsanyi (1977)** and other works Geys cites, **McKelvey & Ordeshook (1972)**, **Mueller (2003)**: not downloaded; what they say is known only as Geys reports it. The Fowler manuscript Geys cites is probably `fowler_wp` (another batch).
- **Whether Wikipedia's [5] (François & Gergaud 2019) prints the model in the form Wikipedia gives**: not downloaded.

# Found that the first pass missed

1. **Geys calls PB "the benefits from voting" and B "the difference in expected utilities"** ("The benefits from voting (PB) have two elements"), so Geys's B is the gain if decisive; Wikipedia's B is likewise "the benefit of a pivotal vote"; Coate & Conlin's B is "the gain from having one’s preferred candidate win"; the arXiv review's B is "the gain of the individual candidate’s victory". No downloaded text defines B as the expected gain pB. (Fork: B versus pB.)
2. **Whose welfare**: Geys's B has no stated owner; he says B is "collective goods" (p. 18) and that pure altruism "work[s] to inflate the B-term in equation (1)" (p. 20) (G24). Coate & Conlin's d is "civic duty or expressing his preference". (Fork: whose welfare in B.)
3. **The tie rule**: Geys has none (S1). R&O's notes 19, 23, 24 give a parity-and-tie-valuation route to ½ (R07): ½ for a tie valued at nothing, dropped "if we assumed the voter equally valued creating a tie to having his preferred candidate win". R&O's P is a subjective probability: fn. 10, "In the general case, since we are dealing with subjective probabilities, we may write pr [1; x] = A where A is any positive number." (cup_ro1968, fn. 10; quote below.) (Fork: tie rule.)
4. **Held fixed, causal or evidential**: Geys footnote 21 (PDF p. 15, printed p. 30) calls the evidential models "magical thinking" and describes them as perceiving "an illusory correlation" with others' behaviour: "The difference is that in these models, voters perceive an illusory cor- relation between their present behaviour and the concomitant behaviour of other voters" and "(‘if I vote, others like me will also vote’) – thereby echoing Jeffrey’s (1983) evidential decision theory." (geys). Footnote 4 (PDF p. 14, printed p. 29): "Voters may not perceive their influence on the election result to be negligible". Geys treats the evidential reading as a perception error in a model of what voters believe, not as a coherent alternative reading of "held fixed". (Fork: causal or evidential.)
5. **What D is**: Geys's D has two readings (G07); Coate & Conlin: "civic duty or expressing his preference"; Gibson et al.: "consumption benefit ... civic duty"; Feddersen & Sandroni: "duty" payoff D > 0 when voting for the preferred candidate; Hamlin & Jennings: "expressive choice as doing one's duty"; arXiv: "civic duty" (Uhlaner added "supporting charismatic leaders"); R&O's own notes: measured by the SRC citizen-duty scale (R06). R&O call their own treatment of rationality "tautological" and accept it (R05). (Fork: what D is.)
6. **What counts in C**: Geys's two groups, pre-election (information, registration) and election day (travel, time) (S3); Coate & Conlin: "the direct cost of voting ... the time taken to get to the polls"; F&F: "the typical costs in time and effort"; arXiv: queue time, travel, information. R&O fn. 9: "the party label reduces the cost of decision in the general election to zero" (a cost of deciding how to vote). (Fork: what counts in C.)
7. **Geys footnote 5** on the "mandate": the paradox is said to follow from treating the policy outcome as all-or-nothing (Stigler 1972; Castanheira 2002, 2003), with a larger vote share possibly mattering; Geys's reply is that "the probability of affecting the implemented platform at the margin is positive, it is likely to be very small" and empirical work on whether mandate matters is "inconclusive" (geys, PDF p. 14, printed p. 29). The report's 3.8 has the SEP version of the mandate point; Geys's is a related point about the policy effect of the margin [I].
8. **Geys's citation error** F&F "p. 928" (G12); the F&F article is pp. 525-536.
9. **The arXiv review's eq. (2) is misprinted**: it prints `B = Bsoc + αN Bself` where the text beside it says α discounts benefit to other people and where Edlin et al. (NBER w13562, PDF p. 5) print `B = Bself + αN Bsoc`. Quote (arxiv2510, PDF p. 3): "By dividing Factor B into the personal income Bself , and the social income Bsoc , and N be the effective population size, then the term B is redefined as follows:" with `B = Bsoc + αN Bself (2)`. Its eq. (4), `b = αBsoc + (1/N)Bself`, matches Edlin et al., so the review is internally inconsistent. If the site cites the review for Edlin et al.'s eq. (2), cite Edlin et al. instead.
10. **R&O notes bearing on the paper's own stance** (cup_ro1968, fn. 3): "This essay may be taken as supporting the position of Riker and Key on the procedural level, i.e., that voters are rational in deciding whether or not to cast a substantive ballot." And fn. 10 (subjective probabilities, above).
11. **Cambridge page label**: the R&O opening paragraph is labelled "Extract", the F&F paragraph "Abstract" (R02, F02).
12. **A second source for R&O's 10^-8** (Goldman fn. 1, T06) in addition to Dowding.
13. **Feddersen and Sandroni (T03)** attribute to R&O 1968 that "increases in costs to vote can have significant impact on turnout levels"; the R&O page itself does not show this result, and none of the other R&O hits in the downloaded texts states it.
14. **R&O's equation numbers in the notes**: (1) and (5) are the "customary" analysis Downs refines (fn. 6: "Downs refines (5) considerably"); (7) is the fuller calculation that includes "non-political" benefits (fn. 7); (21) is the original formulation of P (fn. 23). Later authors' equation numbers (Geys's (1) and (2); the arXiv review's (1)) are their own, not R&O's.

## Quote support for items 3, 4, 7 and 9 above

### Q1 R&O fn. 10 and fn. 3 (quotes for items 3 and 10)
- First pass said: (not in the report)
- Mark: confirmed
- Source: cup_ro1968; same URL; fn. 10 and fn. 3
- Quote: "In the general case, since we are dealing with subjective probabilities, we may write pr [1; x] = A where A is any positive number."
- Quote: "This essay may be taken as supporting the position of Riker and Key on the procedural level, i.e., that voters are rational in deciding whether or not to cast a substantive ballot."
- Note: fn. 10 shows R&O treat P as a subjective probability; fn. 3 states R&O's own claim about what the paper supports.

### Q2 Geys on the evidential models (quotes for item 4)
- First pass said: (report 3.4 cites Geys only for nothing; Geys is not cited for the evidential view)
- Mark: confirmed
- Source: geys; same URL; fn. 21 and fn. 4 on PDF p. 15 (printed p. 30) and PDF p. 14 (printed p. 29)
- Quote: "The difference is that in these models, voters perceive an illusory cor- relation between their present behaviour and the concomitant behaviour of other voters"
- Quote: "will also vote’) – thereby echoing Jeffrey’s (1983) evidential decision theory."
- Quote: "Voters may not perceive their influence on the election result to be negligible"
- Note: the models listed in fn. 21 are Cyr (1975), Quattrone and Tversky (1986), Grafstein (1991) and Güth and Weck-Hannemann (1997); Geys's wording is "magical thinking" and "illusory correlation".

### Q3 Geys fn. 5 on the mandate (quotes for item 7)
- First pass said: (report 3.8 cites SEP for the mandate; Geys is not cited)
- Mark: confirmed
- Source: geys; same URL; fn. 5 on PDF p. 14 (printed p. 29)
- Quote: "all-or-nothing issue (Stigler, 1972; Castanheira, 2002, 2003)."
- Quote: "the probability of affecting the implemented platform at the margin is positive, it is likely to be very small"
- Note: Geys's source for the idea that the margin of victory matters to the policy is Castanheira (2003, "Victory Margins and the Paradox of Voting", EJPE 19: 817-41, listed in his references); not read.

### Q4 arXiv eq. (2) (quote for item 9)
- First pass said: (not in the report)
- Mark: confirmed
- Source: arxiv2510; same URL; PDF p. 3 (printed p. 3); Edlin et al. in edlin_nber, PDF p. 5 (printed p. 4)
- Quote: "B = Bsoc + αN Bself (2)"
- Quote: "Thus, α as a moderating factor indicates that the benefits to other people is less important than the gain to the individual"
- Note: the first quote is the arXiv review's printed eq. (2); the second is its own explanation, which contradicts it (α should multiply the social term). Edlin et al. print `B = Bself + αN Bsoc` (their eq. (2)).
