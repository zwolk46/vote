# B1 findings: `sep` (Stanford Encyclopedia of Philosophy, "The Ethics and Rationality of Voting")

**Source ids read:** `sep` only.
**Size:** `SRC/sep/text.txt` = 12,767 words, 1,711 lines, about 80 KB (`wc`). Layout: site menu lines 1-62; entry body lines 63-1273 (about 10,930 words); bibliography lines 1274-1621 (about 1,564 words); footer lines 1622-1711.
**Read in full:** yes. I read every line 1-1711 with the Read tool (seven chunks), then grepped for terms to confirm absences. I also looked at `SRC/sep/raw` (HTML) for the byline, the date metadata, the section anchors and the equation's TeX source. No network was used.
**What the page is:** a genuine SEP entry. I found no embedded instructions or spam (grep for "ignore", "assistant", "Claude", "instruction" found nothing).
**URL:** https://plato.stanford.edu/entries/voting/ (`hdr` holds only HTTP status headers, no URL; the HTML's "Author and Citation Info" link is `archinfo.cgi?entry=voting`, so it is that entry). Fetched `Date: Sat, 07 Nov 2026 00:11:05 GMT` (hdr).
**Location convention.** The web page has no PDF page numbers and no equation numbers (the one displayed equation is unnumbered). I give the SEP section number (and the HTML anchor) and the `text.txt` line numbers. "Line" below always means a line of `SRC/sep/text.txt`.

---

## Part 1. Digest of the entry

**Author, dates (from the page).** One author: Jason Brennan (Georgetown). The text shows the name only in the copyright block; the HTML metadata also says `citation_author` "Brennan, Jason".
- Quote: "First published Thu Jul 28, 2016; substantive revision Fri Feb 21, 2025"
- Quote: "Copyright © 2025 by Jason Brennan"

**Headings and numbers** (anchors from the HTML): intro (six questions, lines 66-88); 1 The Rationality of Voting (#RatiVoti); 1.1 Voting to Change the Outcome (#VotiChanOutc); 1.2 Voting to Change the "Mandate" (#VotiChanMand); 1.3 Other Reasons to Vote (#OtheReasVote); 2 The Moral Obligation to Vote (#MoraObliVote); 2.1 A General Moral Obligation Not to Vote? (#GeneMoraObliNotVote); 3 Moral Obligations Regarding How One Votes (#MoraObliRegaHowOneVote); 3.1 The Expressivist Ethics of Voting; 3.2 The Epistemic Ethics of Voting; 4 The Justice of Compulsory Voting; 5 The Ethics of Vote Buying; 6 Who Should Be Allowed to Vote? Should Everyone Receive Equal Voting Rights?; 6.1 Democratic Challenges to One Person, One Vote; 6.2 Non-Democratic Challenges to One Person, One Vote; Bibliography; Academic Tools; Other Internet Resources; Related Entries.

**Section by section (what each says, in one or two lines; the facts that matter are quoted in Part 2).**
- *Intro (66-88).* Six questions: is it rational to vote; is there a moral duty to vote; are there obligations on how to vote; may governments compel voting; may votes be bought and sold; who should vote and should votes be equal. Question 6 is sent to Christiano (2006), Pacuit (2011), Gosseries (2005).
- *1 Rationality, opening (128-160).* Voting has an opportunity cost; for nearly every citizen it does not maximise expected utility, hence Downs's "paradox of voting". Rationality depends on what voters are trying to do: instrumental (change the outcome or the "mandate"), expressive, consumption, or discharge a moral obligation.
- *1.1 Voting to change the outcome (162-290).* Sally and candidates D and R; the one formula `U_v = p[V(D) - V(R)] - C`; the equation's stated simplifications and what it omits; doubts about monetising and about voter information; the lottery analogy; p: binomial models ("far less than a millionth of a penny"), Edlin-Gelman-Kaplan's statistical estimate ("on the order of a 1 in 10 million" in very close states), Barnett's "at least 1/N", the Liron-Enoch critique; further worries (courts, "double-edged sword").
- *1.2 Mandate (292-365).* The mandate hypothesis; two "major problems"; Guerrero's delegate-to-trustee variant, continuum and threshold versions; conclusion: expected benefit "still less than a penny".
- *1.3 Other reasons (367-429).* Causal-responsibility theories (Tuck 2008; Goldman 1999); the expressive theory (G. Brennan and Lomasky 1993); the perceived-duty reason (Mackie 2010).
- *2 Moral obligation (431-616).* Most citizens and most philosophers think there is a duty to vote; arguments that rely on a vote making a difference fail on "vanishingly small instrumental value"; the insurance/collapse hypothesis (Downs 1957: 257); complicity (Beerbohm 2012); the "Generalization Argument" and its parody; free-riding / fairness analogies; four arguments that do not rely on efficacy; the "particularity problem"; Maskivker's "easy aid".
- *2.1 Obligation not to vote (618-648).* Sheehy 2002 (voting while indifferent); Freiman 2020 (voting as ineffective altruism).
- *3 How to vote (650-707).* Three families of questions including "The Intended Beneficiary of the Vote".
- *3.1 Expressivist ethics (709-747).* If voting is expression, its ethics is the ethics of expression (G. Brennan and Lomasky 1993: 186, the "Klan ballot").
- *3.2 Epistemic ethics (749-814).* Voters as fiduciaries; the disanalogy of the vanishing p; the "clean-hands principle" and the 100-member firing squad, "causally overdetermined".
- *4 Compulsory voting (816-891).* Demographic argument; "assurance problem" (Hill 2006); empirical effects.
- *5 Vote buying (893-988).* Equality, efficiency and inalienability arguments; case-by-case view; secret-ballot problem; social-meaning objection.
- *6, 6.1, 6.2 (990-1272).* Boundary problem and "all affected interests"; stake-weighted votes; epistocracy; Hong-Page theorem; Condorcet's Jury Theorem; the enfranchisement lottery; public-reason objection.
- *Bibliography (1274-1621).* Note: it lists Barnett as 2023 (the text says 2020 three times) and prints the Edlin-Gelman-Kaplan pages as "219-314"; see Part 4.

---

## Part 2. The first report's statements attributed to SEP

I grepped "SEP", "Stanford", "plato" in `/home/user/vote/research/frameworks-benefit-cost.md`. SEP statements are at lines 31, 44, 51, 72, 137, 139, 148, 180, 203, 276 and 314. Lines 11 and 333 only say curl to plato.stanford.edu was refused (no claim about content). Lines 50, 52, 53 (which the brief named) are about Downs/Dowding, Geys and Dowding, not SEP; the only SEP statement in lines 50-53 is line 51.

### F1 The formula and its three term definitions (line 31; repeated in line 314)
- First pass said: sec. 1.1 gives `U_v = p[V(D) − V(R)] − C`; p "the probability that Sally's vote is decisive"; V(D) − V(R) "the difference in the expected value of the two candidates"; C "the opportunity cost of voting".
- Mark: confirmed
- Source: sep; https://plato.stanford.edu/entries/voting/ ; §1.1 (#VotiChanOutc), the single unnumbered display equation, lines 201-215; no PDF/print page exists.
- Quote: "In that case, the expected value of her vote (\(U_v\)) is:"
- Quote: "U_v = p[V(D) - V(R)] - C"
- Quote: "where p represents the probability that Sally’s vote is decisive, \([V(D) - V(R)]\) represents (in monetary terms) the difference in the expected value of the two candidates, and C represents the opportunity cost of voting."
- Note: The page prints the equation as TeX (rendered by MathJax); the minus signs in the source are ASCII hyphens, the first report wrote U+2212. Same equation. Two qualifiers the first report dropped: "(in monetary terms)", and the premise just before it, "Suppose Sally’s only goal, in voting, is to change the outcome of the election between two major candidates." In this equation D and R are the two candidates (F2b). U_v is net of cost: it is the "expected value of her vote" including −C.

### F2a The structure "p × differential − cost" is written by SEP (line 44, first half)
- First pass said: "The structure probability of decisiveness × benefit differential − cost is written by SEP, Geys, Edlin et al. and Dowding."
- Mark: confirmed (for SEP)
- Source: sep; §1.1; lines 210-215.
- Quote: "In short, the value of her vote is the value of the difference between the two candidates discounted by her chance of being decisive, minus the opportunity cost of voting."
- Quote: "Unless \(p[V(D) - V(R)] > C\), then it is (given Sally’s stated goals) irrational for her to vote."
- Note: The "[S2, in fact S4]" independence tag is the first report's. For the probability figures SEP is a relay of other sources (Brennan and Lomasky 1993; Edlin, Gelman and Kaplan 2007), not an independent measurement (see N5, N6).

### F2b "The D term is added after it" does not apply to SEP (line 44, second half; line 314)
- First pass said: the structure is written by SEP et al. "and the D term is added after it and is not multiplied by p"; the summary (line 314) says every source writes the calculus "with an outcome-independent term D added (SEP `U_v = p[V(D)−V(R)] − C`; ...)".
- Mark: corrected
- Source: sep; §1.1 (lines 162-221) and the opening of §1 (lines 144-160).
- Quote: "The equation above models the rationality of Sally’s choice to vote under the assumption that she is simply trying to change the outcome of the election, and gets no further benefit from voting."
- Quote: "Suppose there are two candidates, D and R."
- Quote: "In contrast, the expressive theory of voting holds that voters vote in order to express themselves and their fidelity to certain groups or ideas."
- Correction: "SEP's equation has an outcome-independent term D added" → "SEP's equation has no outcome-independent term. `D` inside `V(D)` is the name of a candidate (the other is `R`). SEP never writes Riker and Ordeshook's D, `PB + D − C`, or any added term; expressive, consumption and duty reasons are separate theories of what the voter is trying to do, described in prose (§1 opening; §1.3)."
- Note: This is a notation trap for the site: in SEP `D` is a candidate, in Geys/Riker-Ordeshook/Dowding `D` is the non-outcome benefit. SEP does not name Riker, Ordeshook or the calculus of voting at all (grep: no "Riker", no "Ordeshook").

### F3 The paradox of voting and the opportunity-cost sentence (line 51)
- First pass said: SEP sec. 1: voting "has opportunity costs", for most people "voting does not maximize expected utility, which gives rise to the 'paradox of voting' (Downs 1957)" (flagged there as the extractor's paraphrase).
- Mark: corrected (wording only; substance right)
- Source: sep; §1, opening paragraph (before 1.1), lines 128-142.
- Quote: "The act of voting has an opportunity cost."
- Quote: "economists have long worried that, that for nearly every individual citizen, voting does not maximize expected utility."
- Quote: "This leads to the “paradox of voting”(Downs 1957): Since the expected costs (including opportunity costs) of voting appear to exceed the expected benefits,"
- Correction: "'has opportunity costs'" → "The act of voting has an opportunity cost."; "for most people" → "for nearly every individual citizen"; "which gives rise to" → "This leads to". The quoted fragments in the first report are not on the page as written.
- Note: SEP also gives the reason it is a paradox: "and since voters could always instead perform some action with positive overall utility, it’s surprising that anyone votes" (lines 140-142). The parenthesis "(including opportunity costs)" in the third Quote suggests SEP's "costs" may be wider than opportunity costs alone, although the formula labels C only "the opportunity cost of voting" (see N15).

### F4a B's definition (line 72, first cell)
- First pass said: SEP defines B as "the difference in the expected value of the two candidates" (V(D) − V(R)).
- Mark: confirmed
- Source: sep; §1.1; lines 207-210.
- Quote: "represents (in monetary terms) the difference in the expected value of the two candidates"
- Note: see F1 for the full sentence. SEP's wording is "(in monetary terms)"; see N4 on its caveats about monetising.

### F4b Whose welfare counts in SEP's B (line 72, "Who is counted": "not stated in the extract")
- First pass said: not stated in the extract.
- Mark: corrected
- Source: sep; §1.1; lines 164-170 and 220-221.
- Quote: "Suppose she correctly believes that D would do a trillion dollars more overall good than R would do."
- Quote: "Further, the equation assumes her vote confers no other benefit to others than having some chance of changing which candidate wins."
- Quote: "if two candidates were identical except that one would save one more life than another"
- Correction: "not stated" → the page states it: in SEP's worked example the quantity V(D) − V(R) is the difference in "overall good" the two candidates would do, and the sentence about others speaks of "benefit to others" through the outcome. It is not the voter's own private gain. SEP gives no self/other split and no weight on others (no α).
- Note: [I] "overall good" is SEP's phrase; it does not say "social welfare" or "everyone affected". The equation is also stated for a voter whose "only goal" is to change the outcome. Whether the site's B should be overall good or the voter's own is not settled by SEP; SEP simply uses overall good in its example.

### F5 SEP §1.1 listed as a source for the pivotality framework (line 137)
- First pass said: "Sources: SEP sec. 1.1; Edlin et al.; ..." for "3.1 Pivotality / counterfactual (CDT, others fixed)".
- Mark: confirmed (with a limit)
- Source: sep; §1.1; lines 232-236.
- Quote: "the vote depends on the expected difference in value between the chosen candidate and the next best alternative, discounted by the probability of the vote breaking a tie"
- Note: SEP treats the instrumental value of a vote as p (probability of breaking a tie) times the value difference. The labels "counterfactual", "CDT", "others fixed" are the first report's [I]; SEP uses none of them (no "decision theory", "causal", "counterfactual" for this; "counterfactuals" appears only about estimating candidates' effects, line 190).

### F6 "worth far less than a millionth of a penny" (line 139; also line 276)
- First pass said: SEP: the expected benefit under binomial models is "worth far less than a millionth of a penny" (extractor's quote).
- Mark: confirmed
- Source: sep; §1.1; lines 247-255.
- Quote: "the expected benefit of voting (i.e., \(p[V(D) - V(R)]\)) for a good candidate is worth far less than a millionth of a penny (G. Brennan and Lomasky 1993: 56–7, 119)."
- Quote: "These models generally imply that the probability of being decisive, if any candidate has a lead, is vanishingly small"
- Note: Three things the first report did not have: (1) SEP attributes the claim to G. Brennan and Lomasky 1993, pp. 56-7 and 119, not to its own computation; (2) the qualifier "for a good candidate"; (3) SEP gives no numeric p for the binomial model, so the first report's "not stated" in the p column of line 276 is right. I did not read Brennan and Lomasky (not in my batch), so whether they say it is unread.

### F7 Causal-contribution theories (line 148)
- First pass said: SEP (sec. 1.3): these theories hold "voting is rational provided the voter sufficiently cares about being a cause or among the joint causes of the outcome."
- Mark: confirmed
- Source: sep; §1.3 (#OtheReasVote), second paragraph; lines 375-381.
- Quote: "These causal theories of voting claim that voting is rational provided the voter sufficiently cares about being a cause or among the joint causes of the outcome."
- Note: SEP names Tuck 2008 and Goldman 1999 here, in that order. SEP does not use "overdetermination" for these theories (it uses the word in §3.2 about the ethics of voting, see N11).

### F8 Expressive theory (line 180)
- First pass said: SEP (sec. 1.3): "The expressive theory of voting (G. Brennan and Lomasky 1993) holds that voters vote in order to express themselves"; voting is "a consumption activity rather than a productive activity"; compared to sports fans' displays of loyalty.
- Mark: confirmed
- Source: sep; §1.3; lines 390-402.
- Quote: "The expressive theory of voting (G. Brennan and Lomasky 1993) holds that voters vote in order to express themselves."
- Quote: "On the expressive theory, voting is a consumption activity rather than a productive activity;"
- Quote: "Sports fans who paint their faces the team colors do not generally believe that they, as individuals, will change the outcome of the game,"
- Note: the first report's fragments are verbatim. Sentence continues "...but instead wish to demonstrate their commitment to their team."

### F9 The "mandate" argument (line 203)
- First pass said: SEP 1.2: votes might change how effective a winner is; "the extractor reports (paraphrase) that SEP rejects it for two reasons, one being that political scientists largely reject the claim that mandates affect effectiveness."
- Mark: confirmed (incomplete; see N14 for the second reason and the Guerrero variant)
- Source: sep; §1.2 (#VotiChanMand); lines 292-325.
- Quote: "However, the mandate argument faces two major problems."
- Quote: "Political scientists have done extensive empirical work trying to test whether electoral mandates exist, and they now roundly reject the mandate hypothesis (Dahl 1990b; Noel 2010)."
- Note: "roundly reject" (SEP) versus "largely reject" (first report): same sense. The first of the two problems is a marginal-size problem, not an empirical one (N14). The sentence "A vote's effect on a winner's mandate is a consequence the owner's setup ... leaves unspecified" is the first report's [I], not SEP's.

### F10 Row "SEP sec. 1.1 | binomial models" in the p × B table (line 276)
- First pass said: p not stated; B not stated; result: expected benefit "worth far less than a millionth of a penny"; "a 1 in 10 million chance of breaking a tie" in close states (Edlin et al.).
- Mark: confirmed
- Source: sep; §1.1; lines 254-263.
- Quote: "suggests that that a vote in very close states could have on the order of a 1 in 10 million chance of breaking a tie (Edlin, Gelman, and Kaplan 2007)."
- Quote: "the expected benefit of voting (i.e., \(p[V(D) - V(R)]\)) for a good candidate is worth far less than a millionth of a penny (G. Brennan and Lomasky 1993: 56–7, 119)."
- Note: Two models, two cites. The "millionth of a penny" belongs to the binomial model (Brennan and Lomasky); the "1 in 10 million" belongs to the statistical model (Edlin, Gelman and Kaplan 2007) and the first report's row mixes them in one line; both are SEP's own words. "B: not stated" is right: SEP gives no dollar B except the illustrative "a trillion dollars" (F4b). SEP's figure is "on the order of" 1 in 10 million for "very close states", not "close states".

### F11 No other SEP statements in the first report
- First pass said: nothing further.
- Mark: confirmed (checked; no further SEP claims in the report)
- Source: sep; grep of the report for "SEP", "Stanford", "plato".
- Note: Line 126 ("Causal contribution / overdetermination (Goldman, Tuck)") and line 130 ("Expressive / consumption (D)") are the first report's framework labels, not SEP statements.

---

## Part 3. What the entry says on topics (a)-(i) (new findings; the first pass was silent or thin)

Marks here are "confirmed (new)": the page says it; the first report made no claim.

### N1 Authors and dates (task 2 header)
- First pass said: not stated.
- Mark: confirmed (new)
- Source: sep; page header line 64; copyright block lines 1648-1651; HTML metadata (`citation_author`, `DCTERMS.issued` 2016-07-28, `DCTERMS.modified` 2025-02-21).
- Quote: "First published Thu Jul 28, 2016; substantive revision Fri Feb 21, 2025"
- Quote: "Copyright © 2025 by Jason Brennan"
- Note: Cite as Brennan, Jason (first published 2016, substantive revision 21 Feb 2025). The author's own work is cited in the entry ("J. Brennan 2011a; Freiman 2020", line 288; "Brennan and Freiman 2023", line 290) and Barnett's critique of "Brennan's example" in the first report (line 51) may concern this author [I; unread]. For the site: SEP is a secondary relay of other authors' numbers.

### N2 (a) What the equation assumes and omits
- First pass said: not stated.
- Mark: confirmed (new)
- Source: sep; §1.1; lines 217-227.
- Quote: "The equation above models the rationality of Sally’s choice to vote under the assumption that she is simply trying to change the outcome of the election, and gets no further benefit from voting."
- Quote: "It is possible that the choice to cast a vote may induce others to vote, might improve the quality of the ground decision by adding cognitive diversity,"
- Quote: "might have some marginal influence on which candidates or platforms parties run, or might have some other effect not modeled in the equation above."
- Note: SEP calls these "controversial simplifying assumptions". The inducing-others channel is explicitly outside U_v. The equation as printed therefore has only the tie-breaking channel, which fits a set-up where nobody is persuaded.

### N3 (a) SEP's own reading of the formula: "expected benefit" is p × the value difference
- First pass said: not stated (the report's fork "B = gain if decisive versus expected gain pB", lines 98-101, 301).
- Mark: confirmed (new)
- Source: sep; §1.1; lines 210-213, 232-236, 252-255; §1.2 line 311-315.
- Quote: "the expected benefit of voting (i.e., \(p[V(D) - V(R)]\))"
- Quote: "the general point is that the vote depends on the expected difference in value between the chosen candidate and the next best alternative, discounted by the probability of the vote breaking a tie"
- Note: In SEP the bracket V(D) − V(R) is the value difference if the preferred candidate wins (the gain if decisive, expected over uncertainty about what the candidates would do), and "expected benefit of voting" is p times that bracket. So SEP's "benefit" language is attached to p·[V(D) − V(R)], and the bracket itself is the "difference in the expected value of the two candidates". SEP also uses "expected value of her vote" for U_v, which is net of C. The decision rule is "p[V(D) - V(R)] > C" (F2a).

### N4 (b) Whose welfare, monetising, and what the voter knows
- First pass said: "not stated in the extract" (line 72); Edlin et al. and Barnett count others (lines 75-76).
- Mark: confirmed (new)
- Source: sep; §1.1 lines 172-192, 284-290; §3 lines 687-693; §4 lines 865-867.
- Quote: "Whether political outcomes can be described in monetary terms as such is not without controversy."
- Quote: "Even if the expected value difference between two candidates could be expressed on some common value scale, such as in monetary terms, this leaves open whether the typical voter is aware of or can generally estimate that difference."
- Quote: "Beyond that, estimating the value difference between candidates requires evaluating complex counterfactuals, estimating what various candidates are likely to achieve, and determining what the outcomes of these actions would be (Freiman 2020)."
- Quote: "After all, showing that individual votes matter is a double-edged sword; the more expected good an individual vote can do, the more expected harm it can do (J. Brennan 2011a; Freiman 2020)."
- Quote: "The Intended Beneficiary of the Vote: Whose interests should the voter take into account when casting a vote? May the voter vote selfishly, or should she vote sociotropically?"
- Quote: "political scientists overwhelmingly find that voters do not vote their self-interest, but instead vote for what they perceive to be the national interest."
- Note: In §1.1 B is "overall good" (F4b). The "Intended Beneficiary" passage (§3) is about what voters ought to do (ethics), not about the rationality formula. The "double-edged sword" sentence means B can be negative for a voter who picks the worse candidate; SEP's V(D) − V(R) is what the voter correctly or incorrectly believes. SEP never mentions Edlin et al.'s altruism parameter or "social preferences" in the text; their paper appears in the text only for the 1-in-10-million figure, although the bibliography title reads "Why and How People Vote to Improve the Well-Being of Others".

### N5 (c) The probability a vote is decisive: general statement and the binomial model
- First pass said: line 139/276 (millionth of a penny only).
- Mark: confirmed (new)
- Source: sep; §1.1; lines 243-255.
- Quote: "There is some debate among economists, political scientists, and philosophers over the precise way to calculate the probability that a vote will be decisive."
- Quote: "Nevertheless, they generally agree that the probability that the modal individual voter in a typical election will break a tie is small."
- Quote: "Binomial models of voting estimate the probability of a vote being decisive by modeling voters as if they were weighted coins"
- Quote: "and then asking what the probability is that a weighted coin will come up heads exactly 50% of the time."
- Note: SEP's one-sentence description of the binomial model ("a weighted coin will come up heads exactly 50% of the time") is loose; the standard statement is that the other voters' votes split exactly evenly. [I] SEP gives no number for p from this model, only the dollar figure in F6. SEP cites no empirical frequency of ties (no Mulligan and Hunter, no Gelman-King-Boscardin 1998, no Gelman-Silver-Edlin 2008).

### N6 (c) The statistical (forecast-based) estimate
- First pass said: line 276 (1 in 10 million, Edlin et al.).
- Mark: confirmed (new detail)
- Source: sep; §1.1; lines 255-270.
- Quote: "A more optimistic estimate in the literature, which uses statistical estimate techniques based on past elections,"
- Quote: "American voters have widely varying chances of being decisive depending on which state they vote in."
- Quote: "This model still predicts that a typical vote in a “safe” states, like California, has a vanishingly small chance of making a difference"
- Quote: "The binomial model suggests it will almost never be rational to vote, while the statistical model suggests it will be rational for voters to vote in sufficiently close elections or in swing states."
- Quote: "whether voting for the purpose of changing the outcome is rational depends upon the facts on the ground, including how close the election is and how significant the value difference is between the candidates."
- Note: SEP's conclusion is conditional, not "voting is irrational": it depends on closeness and on the size of the value difference. SEP's only citation for the statistical model is Edlin, Gelman, and Kaplan 2007 (line 263). The bibliography prints that paper as "Rationality and Society, 19: 219–314" (the first report has 293-314, from the NBER page); SEP's page range looks like a typo [I].

### N7 (c) Barnett's 1/N, and the critique SEP cites
- First pass said: line 140 (Barnett d ≥ 1/N; "a published reply (JESP)... the extractor could not see which premise").
- Mark: confirmed (new; identifies the JESP reply)
- Source: sep; §1.1 lines 270-278, 288-290; Bibliography lines 1289-1291, 1482-1484.
- Quote: "Barnett (2020) offers an alternative model of the expected value of a vote which implies voting is rational, in the sense of having a high enough expected utility (or disutility) in even more common conditions."
- Quote: "Barnett defends the view that the probability of casting a deciding vote is at least \(1/N\), where \(N\) is the number of voting citizens"
- Quote: "(For a critique of the realism of Barnett’s model, see Liron and Enoch 2023.)"
- Quote: "Liron, A. and D. Enoch, 2023, “The Case for Voting to Change the Outcomes Is Weaker than It May Seem,” Journal of Ethics and Social Philosophy, 26: 204–216."
- Quote: "Barnett, Z., 2023, “Why You Should Vote to Change the Outcome,” Philosophy & Public Affairs, 48: 442–446."
- Note: The first report's "JESP reply" is Liron and Enoch 2023 (SEP's bibliography identifies it; I have not read it). SEP's text cites Barnett as "(2020)" three times (lines 270, 288, 289) but its bibliography prints "2023" and pages "442–446"; the first report uses 2020 (from the Philosophers' Annual PDF). The disagreement is inside SEP. SEP does not mention Barnett's b > 2c condition or his "Partial Unimodality" and "Narrow Upsets" assumptions.

### N8 (c, h) Courts and tie-breaking (the only thing SEP says besides "break a tie")
- First pass said: line 302 ("recounts, courts and runoffs change it", the owner's ½ question).
- Mark: confirmed (new)
- Source: sep; §1.1; lines 280-283.
- Quote: "One worry is that if a major election in most places came down to a single vote, the issue might be decided in the courts after extensive lawsuits (Somin 2013)."
- Note: This is the one place SEP bears on the tie rule: it says a one-vote election would go to the courts, so the nominal p is, in effect, optimistic. SEP does not discuss recounts, runoffs, coin-flip rules, or a factor ½; it equates "decisive" with "breaking a tie" throughout (F5, N5, N16).

### N9 (c) Illustrative numbers in the entry that are not estimates
- First pass said: not stated.
- Mark: confirmed (new)
- Source: sep; §1.1 lines 197-199, 237-241.
- Quote: "In much the same way, it might be worth $200 million to win the lottery, but that does not imply it is rational to buy a lottery ticket."
- Quote: "but one had a 1 in 1 billion chance of being decisive, and instead of voting one could save a drowning toddler,"
- Quote: "then it seems voting is not worthwhile, even if we cannot assign an exact monetary value to thee consequences."
- Note: "1 in 1 billion", "$200 million" and "a trillion dollars" are SEP's illustrations; none is presented as an estimate for a real election, and no source is given.

### N10 (d) Causal-contribution / causal-responsibility theories (Goldman, Tuck)
- First pass said: line 148 only (via SEP); the rest via Ridge and Amadae.
- Mark: confirmed (new detail)
- Source: sep; §1.3; lines 369-388.
- Quote: "Perhaps by voting, a voter has a significant chance of being among the “causally efficacious set” of votes, or is in some way causally responsible for the outcome (Tuck 2008; Goldman 1999)."
- Quote: "On these theories, what voters value is not changing the outcome, but being agents who have participated in causing various outcomes."
- Quote: "Voters vote because they wish to bear the right kind of causal responsibility for outcomes, even if their individual influence is small."
- Quote: "What these alternative theories make clear is that whether voting is rational depends in part upon what the voters’ goals are."
- Quote: "If their goal is to in some way change the outcome of the election, or to change which policies are implemented, then voting is indeed irrational, or rational only in unusual circumstances or for a small subset of voters."
- Note: SEP casts these as theories of what the voter values (a goal, "sufficiently cares"), which makes them goal-based reasons like the expressive and duty reasons, not an extra expected-benefit term. SEP says the voter has "a significant chance" of being in the efficacious set, in contrast with the vanishing chance of being decisive. Parfit and Kagan are not named anywhere in the entry (grep: no "Parfit", no "Kagan").

### N11 (d) "Causally overdetermined", and an internal tension with "vanishingly small"
- First pass said: line 126 labels Goldman/Tuck "overdetermination"; not attributed to SEP.
- Mark: confirmed (new)
- Source: sep; §3.2 (#EpisEthiVoti); lines 775-777, 805-814.
- Quote: "Adding or subtracting a shooter to the firing squad makes no difference—the girl will die anyway."
- Quote: "Similarly, with elections, individual votes make no difference. In both cases, the outcome is causally overdetermined."
- Quote: "individual voters have only a vanishingly small chance of making a difference."
- Note: In §3.2 SEP says "individual votes make no difference" (for an election) and calls the outcome "causally overdetermined"; in §1.1 and §3.2 line 777 it says the chance is "vanishingly small" (not zero). The word "overdetermined" is used for J. Brennan's "clean-hands" ethics of voting well (2011a: 68-94), not for Goldman/Tuck. Both statements are in the entry; the entry does not reconcile them.

### N12 (e) The expressive theory in more detail, and "no one knows"
- First pass said: line 180 and line 186 ([I]: "the owner's isolation ('no one knows') also removes the social part of D").
- Mark: confirmed (new detail)
- Source: sep; §1.3 lines 390-422; §3.1 lines 711-716.
- Quote: "On this theory, though the act of voting is private, voters regard voting as an apt way to demonstrate and express their commitment to their political team."
- Quote: "They vote to signal to themselves and to others that they are loyal to certain ideas, ideals, or groups."
- Quote: "Bob can afford to indulge irrational and misinformed beliefs about public policy and express those beliefs at the polls."
- Note: Per SEP the expressive voter's audience includes the voter ("to themselves"), and the act is "private"; so secrecy does not remove the expressive benefit as SEP describes it. The first report's [I] (line 186) that "no one knows" removes the social part holds only for the show-others part; SEP lists "being able to show others that they voted" under consumption (N13). SEP's Bob passage says the low cost of an outcome-irrelevant ballot lets the voter hold false beliefs; it does not put a number on the expressive benefit.

### N13 (e) Consumption value and perceived duty (what SEP offers in place of a D term)
- First pass said: not attributed to SEP.
- Mark: confirmed (new)
- Source: sep; §1 opening lines 154-160; §1.3 lines 424-429.
- Quote: "Alternatively, one might hold that voting is rational because it is has consumption value; many people enjoy political participation for its own sake or for being able to show others that they voted."
- Quote: "Finally, if one believes, as most democratic citizens say they do (Mackie 2010), that voting is a substantial moral obligation, then voting could be rational because it is necessary to discharge one’s obligation."
- Quote: "Another simple and plausible argument is that it can be rational to vote in order to discharge a perceived duty to vote (Mackie 2010)."
- Quote: "If there are such duties, and these duties are sufficiently weighty, then it would be rational for most voters to vote."
- Note: SEP offers four non-outcome reasons: expressive, consumption, perceived duty (Mackie 2010, an unpublished manuscript per the bibliography), causal responsibility (N10). It does not call any of them D and does not say how they would be added to U_v. On what D "is": SEP keeps expression, consumption and duty distinct.

### N14 (f) The "mandate" argument: what exactly SEP concludes, and why
- First pass said: line 203 (F9).
- Mark: confirmed (new detail)
- Source: sep; §1.2; lines 294-365.
- Quote: "The assumption here is that an elected official’s efficacy—i.e., her ability to get things done in office—depends in part on how large of a majority vote she received."
- Quote: "we would need to know how much the nth voter’s vote increases the marginal effectiveness of her preferred candidate, or reduces the marginal effectiveness of her dispreferred candidate."
- Quote: "It would be rational for me to vote only if I believed my individual vote would give the winning candidate at least $15 worth of electoral efficacy"
- Quote: "A winning candidate’s ability to get things done is generally not affected by how small or large of a margin she wins by."
- Quote: "Perhaps voting is rational not as a way of trying to change how effective the elected politician will be, but instead as a way of trying to change the kind of mandate the winning politician enjoys (Guerrero 2010)."
- Quote: "just as the probability that her vote will decide the election is vanishingly small, so the probability that her vote will decisively transform a representative from a delegate into a trustee would be vanishingly small."
- Quote: "Indeed, the formula for determining decisiveness in transforming a candidate into a trustee would be roughly the same as determining whether the voter would break a tie."
- Quote: "suppose it’s a billion or even a trillion dollars better for a representative to be a trustee rather than a candidate."
- Quote: "Even if so, the expected benefit of an individual vote is still less than a penny, which is lower than the opportunity cost of voting."
- Note: SEP's two "major problems" with the efficacy mandate: (1) even if mandates exist, one must show that the nth vote adds at least the vote's cost in marginal effectiveness (SEP's example cost: $15 of time); (2) political scientists "roundly reject the mandate hypothesis". SEP then considers Guerrero's delegate/trustee version: on a continuum the marginal increment must be worth at least $15 (Guerrero 2010: 295-297); with a threshold, the chance of crossing it is as small as the chance of a tie, so even a billion-or-trillion-dollar gain gives "less than a penny". SEP's conclusion: the mandate route does not rescue the rationality of voting. For the "less than a penny" figure see N19 (the p it requires).

### N15 (g) The cost of voting (C)
- First pass said: Part 4 of the report, nothing from SEP.
- Mark: confirmed (new)
- Source: sep; §1 opening lines 128-142; §1.2 lines 311-315; §2 line 614-615.
- Quote: "The act of voting has an opportunity cost. It takes time and effort that could be used for other valuable things, such as working for pay, volunteering at a soup kitchen, or playing video games."
- Quote: "Further, identifying issues, gathering political information, thinking or deliberating about that information, and so on, also take time and effort which could be spent doing other valuable things."
- Quote: "Suppose voting for the expected winning candidate costs me $15 worth of my time."
- Quote: "and since voters could always instead perform some action with positive overall utility"
- Quote: "if one can provide aid to others at very low cost to oneself, then one should do so."
- Note: In SEP C is an opportunity cost: time and effort of the act, plus the time and effort of getting informed and deliberating (so SEP does count information-gathering in cost; compare the first report's "information" component, line 212). The $15 is a hypothetical, not a measurement. Maskivker's "easy aid" (a duty that assumes a very low cost) is quoted from SEP's account of her argument; SEP does not give a value of C. SEP's formula uses a single C; it has no separate cost-of-information term.

### N16 (h) Ties, recounts, tie-breaking, the factor ½
- First pass said: lines 302 and 314 (the ½, the owner's "margin of one" point).
- Mark: confirmed (new; mostly an absence)
- Source: sep; whole entry; §1.1 lines 233-236, 247-263, 280-283; §1.2 lines 357-360.
- Quote: "discounted by the probability of the vote breaking a tie"
- Quote: "a weighted coin will come up heads exactly 50% of the time"
- Quote: "the issue might be decided in the courts after extensive lawsuits (Somin 2013)"
- Note: SEP identifies "decisive" with "breaking a tie". It has no factor ½ for a coin-flip tie, no "one short of a tie" case, no recount rule, no runoff, no multi-candidate pivot event. A whole-word grep for tie, ties, tied, recount, court, courts, lawsuits, runoff returns only lines 235, 247, 263, 282 and 360, all cited above. Whether a ½ belongs in p is therefore not addressed by SEP.

### N17 (i) Evidential decision theory; group or rule consequentialism
- First pass said: sections 3.4 and 3.5 (sources other than SEP).
- Mark: confirmed (new; absence plus nearest passages)
- Source: sep; whole entry; §2 lines 487-507; §4 lines 851-861.
- Quote: "What if everyone were to stay home and not vote? The results would be disastrous! Therefore, I (you/she) should vote. (Lomasky and G. Brennan 2000: 75)"
- Quote: "The problem with this argument, as stated, is that even if it would be disastrous if no one or too few performed some activity, it does not follow that everyone ought to perform it."
- Quote: "What’s important is that enough other voters like her vote. However, she cannot easily coordinate with other voters and ensure they will vote with her."
- Note: The words "evidential", "Jeffrey", "Newcomb", "decision theory", "Harsanyi", "utilitarian", "rule" (as in rule consequentialism) occur nowhere in the entry (grep returned nothing; "consequential" appears only at lines 597, 915, 982 in other senses). The nearest material is the "Generalization Argument" (§2, 'what if everyone stayed home'), which SEP says is "unsound, as stated" and replaces with fairness/free-riding arguments, and the "assurance problem" in §4 (Hill 2006): a voter needs assurance that enough like-minded others vote, which compulsory voting supplies. SEP therefore gives no evidential or correlated-choice treatment of p.

### N18 (d, i) Threshold arguments in §2 (the "tiny chance of a big difference" structure)
- First pass said: section 3.3 (Kagan, Parfit), not from SEP.
- Mark: confirmed (new)
- Source: sep; §2; lines 453-467.
- Quote: "one early hypothesis was that voting might be a form of insurance, meant to to prevent democracy from collapsing (Downs 1957: 257)."
- Quote: "just as there is a vanishingly small probability that any individual’s vote would decide the election, so there is a vanishingly small chance that any vote would decisively put the number of votes above that threshold."
- Quote: "one would first need to show that the marginal expected benefits of the nth vote, in reducing the chance of democratic collapse, exceed the expected costs (including opportunity costs)."
- Note: SEP treats a threshold effect (democracy collapses below a vote count) the same way as a tie: probability of being the vote that crosses the threshold is "vanishingly small", and the continuous version needs marginal expected benefit above expected cost. It does not cite Kagan or Parfit and does not discuss whether a tiny p should be ignored; it multiplies p by the stakes (see N19).

### N19 [M] What p the entry's "less than a penny" statements require (my arithmetic, not SEP's)
- First pass said: no [M] arithmetic is attributed to SEP in the report.
- Mark: confirmed (new; calculation of my own, from SEP's inputs)
- Source: sep; §1.2 lines 360-363 (B = $1 billion or $1 trillion, "less than a penny"); §1.1 lines 262-263 (1 in 10 million).
- Quote: "Thus, suppose it’s a billion or even a trillion dollars better for a representative to be a trustee rather than a candidate."
- Quote: "Even if so, the expected benefit of an individual vote is still less than a penny, which is lower than the opportunity cost of voting."
- Note: [M] p × B < $0.01 requires p < 0.01 / B: for B = $10^9, p < 10^-11; for B = $10^12, p < 10^-14. At SEP's own "on the order of a 1 in 10 million" (p = 10^-7) the same B gives p × B = $100 (B = $10^9) and $100,000 (B = $10^12); at p = 1 in 1 billion (10^-9) it gives $1 and $1,000. So SEP's "less than a penny" sentence holds only for p far below the statistical model's best case (the binomial-model or safe-state regime); SEP states no p for that sentence. This is a tension inside the entry that the site's model should not inherit silently. (Computed with `python3 -I`; inputs are the dollar figures and probabilities quoted above.)

---

## Part 4. Corrections table

| Old (first report) | New (this page) | Source |
|---|---|---|
| Line 44, 314: the D term is "added after" the SEP structure, "not multiplied by p"; line 314 lists SEP among formulas "with an outcome-independent term D added" | SEP's equation has no D term; `D` in `V(D)` is a candidate; expressive/consumption/duty reasons are separate prose theories | sep §1.1 lines 166, 217-219; §1 opening 152-160 |
| Line 51: SEP says voting "has opportunity costs"; for "most people" it "does not maximize expected utility, which gives rise to the 'paradox of voting'" (paraphrase) | "The act of voting has an opportunity cost."; "for nearly every individual citizen, voting does not maximize expected utility"; "This leads to the “paradox of voting”(Downs 1957)" | sep §1 opening, lines 128, 136-138 |
| Line 72: who is counted in SEP's B: "not stated in the extract" | The page states it: "overall good" (D "would do a trillion dollars more overall good than R") | sep §1.1, lines 166-169 |

Other points of detail (not corrections of statements the report attributed to SEP): the formula uses ASCII "-" in the page source (the first report used U+2212); SEP bibliography prints Barnett as 2023 and Edlin et al. pages as "219–314" (N6, N7).

## Part 5. Unread and why

- Whether Brennan and Lomasky (1993), pp. 56-7 and 119, say anything like "a millionth of a penny": SEP cites it; the book is not in my batch. SEP's claim is confirmed as SEP's claim only.
- Whether Edlin, Gelman and Kaplan (2007) give "on the order of a 1 in 10 million" in the form SEP states it (the first report quotes their fn. 3 as "10⁻⁷ or 10⁻⁸"): not my source; unread here.
- Liron and Enoch (2023): that it is the reply the first report calls "a published reply (JESP)" is inferred from the title/journal in SEP's bibliography and SEP's text ("a critique of the realism of Barnett’s model"). I did not read it.
- Whether the first report's extractor read this same revision (21 Feb 2025). Every first-report quote I could test matches this revision's wording (F6-F8), but I cannot see what version the extractor had. An earlier revision of the entry would need the Wayback or SEP archive, which I may not request.
- The rendered page (MathJax output) was not viewed; I read the TeX source of the equation in the HTML.
- Whether SEP's "Mackie 2010" (unpublished manuscript per the bibliography) supports the survey claims; not read.

## Part 6. Found that the first pass missed

Each item bears on the fork points in common.md rule 10.

1. **Whose welfare is in B (fork 1).** SEP's worked case defines V(D) − V(R) as the "overall good" the candidates would do, so B in SEP is not the voter's own gain (F4b). SEP also says the voter may not know the difference and may pick the worse candidate ("double-edged sword", N4). SEP uses no altruism weight; it never discusses the Edlin et al. α.
2. **B is the gain if decisive; the benefit is pB (fork 2).** SEP calls p[V(D) − V(R)] "the expected benefit of voting" and V(D) − V(R) "the difference in the expected value of the two candidates"; U_v is p times the bracket minus C (N3, F2a). So SEP's bracket is the "if decisive" quantity and the product is the expected benefit. SEP also says "the expected value of her vote" for the net U_v.
3. **Tie rule / factor ½ (fork 3).** No ½ anywhere; "decisive" = "breaking a tie"; the only comment is that a one-vote election might be decided in the courts (Somin 2013) (N8, N16).
4. **"Held fixed": causal or evidential (fork 4).** SEP is silent: no evidential or correlated-choice treatment, no mention of EDT or Jeffrey. The closest passages are the Generalization Argument and the assurance problem (N17); SEP's p is "the probability that Sally’s vote is decisive" with no mention of what is held fixed. SEP's equation also explicitly omits the channel "induce others to vote" (N2), which is the channel the owner's set-up shuts.
5. **What D is (fork 5).** SEP has no D term; it separates expression, consumption, perceived duty and causal responsibility (N10, N12, N13). The letter D in SEP's formula is a candidate (F2b). The first report's statement that SEP is one of the sources that writes the D term is wrong.
6. **What counts in C (fork 6).** SEP's C is opportunity cost of time and effort and includes the effort of getting informed and deliberating ("identifying issues, gathering political information, thinking or deliberating"); SEP's paradox sentence says "expected costs (including opportunity costs)" (F3, N15). The $15 figure is a hypothetical.
7. **SEP relays numbers, it does not measure them.** "Far less than a millionth of a penny" is Brennan and Lomasky 1993 pp. 56-7, 119; "on the order of a 1 in 10 million" is Edlin, Gelman and Kaplan 2007; "at least 1/N" is Barnett. The first report counts SEP as a separate source for p alongside Edlin et al. (line 276, line 139); on the 1-in-10-million figure they are the same source (F10, N6).
8. **Internal tension on the "less than a penny" sentence** (N19) and on "no difference" versus "vanishingly small" (N11).
9. **Citation discrepancies inside SEP**: Barnett "2020" in the text, "2023, Philosophy & Public Affairs 48: 442-446" in the bibliography; Edlin et al. pages "219–314" (N6, N7). A site that cites SEP's Barnett or Edlin entries should cite the originals.
10. **Identification of the JESP reply**: Liron and Enoch (2023), *Journal of Ethics and Social Philosophy* 26: 204-216 (N7).
