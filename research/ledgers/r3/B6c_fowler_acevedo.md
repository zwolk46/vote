# B6c: Fowler working paper (fowler_wp) and Acevedo & Krueger 2004 (scispace)

## Sources read

- **fowler_wp**: `SRC/fowler_wp/text.txt`, 9,891 words (wc), 28 PDF pages (form-feed count), **read in full** with Read in four chunks (lines 1-1429). PDF pages 8, 18 and 20 also looked at as images (footnote 1 formula, Table 6, Table 7). Numbering: PDF p. 1 is the unnumbered title/abstract page; PDF p. N (N >= 2) carries printed page N-1, so **printed = PDF - 1**. URL: `https://econwpa.ub.uni-muenchen.de/econ-wp/exp/removed/0504001.pdf` (from the lead's `list2.txt`; the `hdr` file carries no URL; `hdr` says Last-Modified 11 Jul 2018). The PDF metadata says Title "Microsoft Word - Altruism and Political Participation MPSA.doc", Author jhfowler, created 2005-04-01.
- **scispace**: `SRC/scispace/text.txt`, 9,258 words, 20 PDF pages, **read in full** with Read in four chunks (lines 1-907). PDF pages 8 and 15 also looked at as images. Numbering: printed journal pages 115-134 on PDF pp. 1-20, so **printed = PDF + 114**. URL (canonical per `hdr`): `https://scispace.com/pdf/two-egocentric-sources-of-the-decision-to-vote-the-voter-s-x8k3uughbj.pdf`.
- Neither file contains text addressed to a reader or any instruction; both are what they claim to be (a conference working paper; a journal article's typeset pages).
- Verification: every quoted passage listed under a quote line below was run through the lead's `qcheck.py` logic against the right `text.txt` (whitespace collapsed) and found, each at most 40 words. Where `text.txt` has a line-break hyphen (e.g. "deci-/sions") the quote stops short of it, and the Note says so.
- Citations of the form "p. N" in the text of a Note mean the printed page of that source unless "PDF" is said.
- First-report line numbers refer to `/home/user/vote/research/frameworks-benefit-cost.md` (337 lines).
- Section order: A1-A22 Acevedo & Krueger; F1-F22 Fowler working paper. Entries A1-A10 and F1-F6 are the first report's own statements; the rest are new facts filled from the sources.

---

# Part A. Acevedo & Krueger (2004), scispace

### A1 Quattrone & Tversky title and citation
- First pass said: Quattrone & Tversky (1984), "Causal versus diagnostic contingencies: on self-deception and on the voter's illusion", **unread**, described by Acevedo & Krueger (line 161).
- Mark: confirmed
- Source: scispace; https://scispace.com/pdf/two-egocentric-sources-of-the-decision-to-vote-the-voter-s-x8k3uughbj.pdf; References list; PDF p. 20 (printed p. 134)
- Quote: "Quattrone, G. A., & Tversky, A. (1984). Causal versus diagnostic contingencies: On self-deception and on the voter’s illusion. Journal of Personality and Social Psychology, 46, 237–248."
- Note: The journal is *Journal of Personality and Social Psychology* 46, 237-248 (the first report gave no journal). I did not read Quattrone & Tversky; everything about them in A11-A12 is Acevedo & Krueger's description. A&K give no Quattrone & Tversky sample size, correlation or p-value anywhere (all eleven mentions of the name were checked), so no Quattrone & Tversky number is available from this source.

### A2 "voters regard their own decisions as being diagnostic ... millions of other voters" (p. 117)
- First pass said: "voters regard their own decisions as being diagnostic of the decisions of millions of other voters" who share their preferences (p. 117, extractor) (line 161).
- Mark: confirmed
- Source: scispace; same URL; section "The Voter's Illusion", first sentence; PDF p. 3 (printed p. 117)
- Quote: "Quattrone and Tversky (1984) suggested that voters regard their own"
- Quote: "as being diagnostic of the decisions of millions of other voters who share their political preferences."
- Note: In `text.txt` the word "decisions" is split across the line break ("deci-" / "sions"), hence two Quote lines; read together they are the sentence the first report quotes. The page number (printed 117) is right. The words are A&K's report of what Quattrone & Tversky "suggested"; "millions" is A&K's phrase, not a figure from an experiment.

### A3 The "weaker reading" (p. 118)
- First pass said: weaker reading: they "may merely believe that their own actions are diagnostic of collective behavior" (p. 118) (line 161).
- Mark: confirmed
- Source: scispace; same URL; section "The Voter's Illusion", second paragraph; PDF p. 4 (printed p. 118)
- Quote: "Alternatively, people may merely believe that their own actions are diagnostic of collective behavior, in which case they can read their own voting as a sign that many like-minded others will vote too."
- Note: Quote and page are right. Attribution to be careful with: this "weaker reading" is **A&K's own alternative** to Quattrone & Tversky's attribution, which A&K give in the sentence before it (see A12: Quattrone & Tversky "attributed the voter's illusion to the belief that the decision to vote might induce others to do likewise", a causal belief A&K call "magical thinking"). So the diagnostic (evidential) reading is A&K's proposal, and A&K's Study 1 data are said to support it (A18).

### A4 Study 1: 110 undergraduates
- First pass said: Study 1, 110 undergraduates (line 161).
- Mark: confirmed
- Source: scispace; same URL; Study 1, Method, Participants; PDF p. 6 (printed p. 120)
- Quote: "Undergraduates (N = 110) participated in this study. Half of them completed the study to fulfill a course requirement; the other half completed the study as part of a class activity."
- Note: Nothing is said about the university, age or sex of the participants. The Limitations section says students "may differ from the general population" (printed p. 131).

### A5 Study 1 uses the nation "Delta"
- First pass said: hypothetical nation "Delta" (line 161).
- Mark: confirmed
- Source: scispace; same URL; Study 1 heading and Design and procedures; PDF p. 5 (printed p. 119) for the heading, PDF p. 6 (printed p. 120) for the quote
- Quote: "Study 1: Voting in Nation “Delta”"
- Quote: "Participants read a description of nation “Delta,” which was about to hold an election (see Quattrone & Tversky, 1984, study 2)."
- Note: "Hypothetical" is the first report's word; the paper says participants were asked to "imagine" themselves as supporters of the Peace Party and that the studies "used scenarios to elicit judgments" (printed p. 131; Quote in A21). Study 1 follows Quattrone & Tversky's study 2. Full design in A14.

### A6 r(108) = .19, one-tailed p = .027 (p. 122)
- First pass said: the illusion measured as a correlation of r(108) = .19, one-tailed p = .027 (p. 122) (line 161).
- Mark: confirmed
- Source: scispace; same URL; Study 1, Results, "The voter's illusion"; PDF p. 8 (printed p. 122)
- Quote: "between the projection scores and the voting scores [r(108) = .19, p = .027, one-tailed]."
- Note: "correla-/tion" is split across a line in `text.txt`, so the Quote starts at "between". The full sentence is "The voter's illusion was then captured by the correlation between the projection scores and the voting scores [r(108) = .19, p = .027, one-tailed]." Page 122 is right (checked on the PDF image). [M] recomputation, mine: for N = 110 (df = 108), r = .19 gives t = 2.011 and one-tailed p = .0234, not .027. A one-tailed p of .027 corresponds to r of about .184 (r = .185 gives .0265). So the paper's r and p agree only at the bottom edge of rounding for r; I report the paper's figures as printed. Both are in the same range and the difference does not change the reading.

### A7 "modest"
- First pass said: the extractor calls the effect modest (line 161).
- Mark: confirmed
- Source: scispace; same URL; Study 1 Results (PDF p. 8, printed p. 122); General Discussion, Limitations (PDF p. 18, printed p. 132)
- Quote: "The size of the voter’s illusion was relatively modest, in part, because the social desirability of voting"
- Quote: "the observed effect sizes may not have been large, but according to the convention proposed by Cohen (1988), they fell between the small (r = .10) and medium benchmarks (r = .30)."
- Quote: "Thus, these effects were not negligible."
- Note: "Modest" is the authors' word. They also say the effects are "not negligible", that voting intentions were high (ceiling), and that the result is probably conservative: "If so, the obtained findings are rather conservative estimates of egocentric components of the decision to vote." (printed p. 132; Quote in A15). They also say it was "more modest than it was in Quattrone and Tversky's (1984) original study" (printed p. 124; A12). The site should not quote only "modest".

### A8 Study 2: N = 86, 2000 US presidential election
- First pass said: Study 2 (N = 86, 2000 US presidential election) (line 161).
- Mark: confirmed
- Source: scispace; same URL; Study 2 heading and Method; PDF p. 11 (printed p. 125)
- Quote: "Study 2: Beliefs in Personal Relevance in the 2000 Presidential Election"
- Quote: "Undergraduates (N = 86) completed the study as an in-class activity."
- Quote: "election at a time when that election was 18 months in the future."
- Note: It is a scenario about a future election: participants were asked to consider the 2000 presidential election when it was 18 months away (the sentence begins "Participants were asked to consider the 2000 presiden-/tial election ..." with a line-break hyphen, so the Quote starts at "election"). Design and numbers in A17.

### A9 Study 2 had no measure of the illusion
- First pass said: Study 2 "found no measure of the illusion" (line 161).
- Mark: confirmed
- Source: scispace; same URL; Study 2; PDF p. 11 (printed p. 125); General Discussion; PDF p. 18 (printed p. 132)
- Quote: "Our second study was designed to examine beliefs in personal relevance in a more realistic context."
- Quote: "the voter’s illusion first demonstrated by Quattrone and Tversky (1984), and Study 2 replicated the belief in personal relevance first demonstrated in Study 1."
- Quote: "The first three questions were intended to raise awareness about this election and to ascertain the anticipated level of involvement"
- Note: Study 2 contains no projection or conditional-turnout items (its questions are certainty of preference, likelihood of voting, and then regret, satisfaction, waste and confidence for four win/lose x vote/abstain scenarios). So the first report's wording "found no measure" should read "**had no measure**": Study 2 neither tested nor failed to find the illusion. Only Study 1 bears on the illusion.

### A10 [I] r = .19 measures a belief, not a correlation among real voters
- First pass said: "the only number is r = .19 in a hypothetical-nation experiment, which measures a belief, not a correlation among real voters" (line 166, an [I]).
- Mark: confirmed (the inference is supported by the source)
- Source: scispace; same URL; Study 1 Results; PDF p. 8 (printed p. 122); Limitations; PDF p. 17 (printed p. 131)
- Quote: "For each participant, a projection score was computed as the average of two differences (voter turnout if voting minus voter turnout if abstaining, victory if voting minus victory if abstaining)"
- Quote: "voting intentions were computed as the average of two ratings (likelihood of voting and voting intention, which were highly correlated: r = .68)"
- Quote: "Nonetheless, the predictive value of voting intentions for actual voting behavior needs to be examined further."
- Note: The r = .19 is **across participants** between (a) each person's own stated difference in expectation of others' turnout and the party's victory if they vote versus abstain, and (b) the same person's stated intention to vote. Both are self-ratings on 9-point scales about an imagined election. It is not a correlation between real voters' choices, and the authors say intentions-to-behaviour is itself untested. There are other numbers in the paper that bear on the evidential question (see A15, A18): the mean difference in the expected outcome (5.06 vs 4.48 on a 9-point scale) is the closest thing to a perceived conditional probability shift, but it too is a belief.

### A11 [new] What A&K say Quattrone & Tversky's design was
- First pass said: not stated (line 161 only says "described by Acevedo & Krueger").
- Mark: confirmed
- Source: scispace; same URL; "The Voter's Illusion", PDF p. 3 (printed p. 117) and PDF p. 4 (printed p. 118); Study 1 intro, PDF p. 5 (printed p. 119) and p. 6 (printed p. 120)
- Quote: "Participants in their study were asked to identify with one of two parties seeking to govern the country of “Delta.”"
- Quote: "Some participants learned that the electoral outcome depended on each party’s ability to mobilize its supporters. Others learned that the election depended on the ultimate behavior of unaligned voters."
- Quote: "Thus, only participants in the party-supporters condition could use their own intentions (vote or abstain) to predict the outcome."
- Quote: "participants predicted the electoral outcome under the assumption that they had voted, and under the assumption that they had abstained."
- Quote: "We adopted Quattrone and Tversky’s (1984) paradigm and added a"
- Quote: "Participants answered six questions drawn from Quattrone and Tversky (1984)."
- Note: Two conditions (outcome depends on the party supporters' turnout, or on unaligned voters); each participant forecasts the outcome under "I vote" and under "I abstain". A&K's Study 1 follows Quattrone & Tversky's study 2, keeps six of their questions, and adds the morning/evening timing manipulation (A14). No sample size for Quattrone & Tversky is given in A&K.

### A12 [new] What A&K say Quattrone & Tversky found and claimed
- First pass said: only the p. 117 and p. 118 sentences (line 161).
- Mark: confirmed
- Source: scispace; same URL; PDF p. 4 (printed p. 118), PDF p. 10 (printed p. 124), PDF p. 14 (printed p. 128), PDF p. 18 (printed p. 132)
- Quote: "As expected, participants in the party-supporters condition thought that victory was more likely if they themselves voted."
- Quote: "The voter’s illusion was revealed by the correlation between the degree to which the expected electoral outcome was associated with"
- Quote: "(i.e., estimated likelihood of victory if voting minus estimated likelihood of victory if abstaining) and the strength of their expressed intentions to vote."
- Quote: "Quattrone and Tversky (1984) attributed the voter’s illusion to the belief that the decision to vote might induce others to do likewise."
- Quote: "magical thinking because individual decisions can have no causal effect on the behavior of the aggregate."
- Quote: "Quattrone and Tversky (1984) assumed that people should realize that their individual decisions to vote play no causal role in turnout."
- Quote: "People should recognize abstention as the dominating choice."
- Quote: "The size of the voter’s illusion was more modest than it was in Quattrone and Tversky’s (1984) original study"
- Note: Per A&K: (1) **Finding**: in the party-supporters condition, victory was judged more likely if the participant voted; the illusion is the correlation, across participants, between that difference (expected outcome if voting minus if abstaining) and intention to vote (printed p. 118; this is one sentence in the paper: the second Quote stops at "associated with", the words "individuals' own hypothetical behavior" fall across a line-break hyphen and are not quoted, and the third Quote starts at the parenthesis). (2) **Claim about cause**: the illusion comes from the belief that one's vote might induce others to vote (printed p. 118), which A&K call magical thinking. (3) **Normative claim**: Quattrone & Tversky treated the illusion as an error because individual decisions "play no causal role in turnout" and abstention dominates (printed p. 128). (4) A&K's Study 1 effect is smaller than the original (printed p. 124); they report no number for the original. A&K also say Study 1 "replicated the voter's illusion first demonstrated by Quattrone and Tversky" (printed p. 132, A9).

### A13 [new] Definition of the "voter's illusion"
- First pass said: not stated beyond the p. 117 quotation (line 161).
- Mark: confirmed
- Source: scispace; same URL; Abstract, PDF p. 1 (printed p. 115); Introduction, PDF p. 3 (printed p. 117)
- Quote: "the voter’s illusion (the projection of one’s own choice between voting and abstention to supporters of the same party or candidate)"
- Quote: "The first phenomenon is the voter’s illusion, which occurs when people project their own intentions, either to vote or to abstain, more strongly to similar others (i.e., supporters of the same party) than to"
- Quote: "Because this projection differential inspires greater optimism regarding the election outcome when voting rather than abstention is being"
- Quote: "many people may choose to vote (Quattrone & Tversky, 1984)."
- Quote: "the belief in personal relevance (the belief that one’s own vote matters regardless of its predictive value for the behavior of others)"
- Quote: "The rationality of these two egocentric mechanisms depends on the normative framework invoked."
- Note: Definition: **projecting one's own voting/abstaining intention more strongly onto like-minded others than onto others, which makes the expected outcome look better if one votes** (the full sentence continues "dissimilar others", split by a line-break hyphen). It is a belief (projection), not a measured correlation among real voters. The second mechanism, the "belief in personal relevance", is the belief that one's own vote matters "regardless of its predictive value for the behavior of others", i.e. the causal/counterfactual belief (the one that "negates the moral certainty argument", printed p. 117). A&K separate the two and find them "largely independent" (r = -.05 and -.03; A15). The authors stress the rationality of both "depends on the normative framework invoked".

### A14 [new] Study 1 design
- First pass said: Study 1 = 110 undergraduates, nation "Delta" (line 161).
- Mark: confirmed
- Source: scispace; same URL; Study 1 Method; PDF pp. 5-7 (printed pp. 119-121)
- Quote: "Participants were asked to imagine themselves as supporters of the Peace Party (which opposed the War Party)."
- Quote: "They learned that political analysts predicted that the electoral outcome would depend on which party’s supporters turned out in greater numbers"
- Quote: "The party that was better able to mobilize its supporters was expected to win by a margin of 200,000 to 400,000 votes."
- Quote: "Participants also learned that voting in Delta involved time and effort, and that citizens do not typically share information about their voting intentions with others because it is improper etiquette in Delta to do so."
- Quote: "Half of the participants were placed in the morning condition, and half were placed in the evening condition."
- Quote: "A manipulation check performed on a separate sample (N = 38) showed that 84% of respondents correctly recalled the timing of their voting behavior at the end of the procedure."
- Quote: "The first two ratings referred to the expected turnout as a function of the participant’s own behavior"
- Quote: "“If you vote, how likely is it that Party A will defeat Party B?” and “If you abstain, how likely is it that Party A will defeat Party B?”"
- Quote: "“How likely are you to vote if the theory of the political analysts about the outcome of the election is true?” and “Would you vote if the political theory were true and voting in Delta were costly?”"
- Quote: "All ratings were made on 9-point scales (1 = very unlikely, 9 = very likely; for the last rating, 1 = not at all, 9 = most definitely)."
- Quote: "to explore the possibility that the voter’s illusion is stronger among earlier voters than among late voters."
- Note: Within-subject factor: Behavior (vote vs abstain); between-subject factor: Time of Voting (morning 7-8 a.m. vs evening 7-8 p.m. voting window; the timing was A&K's addition). Four of the six ratings (two on others' turnout if I vote/abstain, two on victory if I vote/abstain) form the projection score; two give voting intentions (A15). Participants then rated four mishap scenarios (win/lose x voted/abstained) on waste, confidence, regret and satisfaction (A16). **The Delta scenario stipulates that voting intentions are not shared**, yet the illusion still appeared (see "Found that the first pass missed", item 4).

### A15 [new] Study 1 statistics for the illusion
- First pass said: only r(108) = .19, p = .027 (line 161).
- Mark: confirmed
- Source: scispace; same URL; Study 1 Results; PDF p. 7 (printed p. 121), PDF p. 8 (printed p. 122), PDF p. 10 (printed p. 124); General Discussion PDF p. 18 (printed p. 132)
- Quote: "Indeed, ratings of the likelihood of voting [M = 7.15, t(109) = 17.02, d = 1.62]"
- Quote: "and of voting intentions [M = 6.26, t(109) = 8.58, d = .82] were both above the scale midpoint."
- Quote: "A favorable outcome appeared more likely if participants expected to vote (M = 5.06) rather than abstain (M = 4.48) [F(1, 108) = 31.75, d = .49]."
- Quote: "Moreover, there was no evidence for magical causation (r = .19 and .18 for the morning and the evening condition, respectively)."
- Quote: "Even among participants who did not show any tendency to project their own decisions to similar others (i.e., 54% of the sample), voting intentions were above the midpoint of the scale"
- Quote: "The low correlations suggested that the two egocentric sources of voting operated largely independently of one another."
- Quote: "the voter’s illusion (r = .19) means that the rate of above-median voting intentions is 19 percentage points greater among above-median projectors than among below-median projectors"
- Quote: "If so, the obtained findings are rather conservative estimates of egocentric components of the decision to vote."
- Note: Illusion: r(108) = .19, one-tailed p = .027 (A6); with the timing split r = .19 (morning) and .18 (evening). Conditional expectation: M = 5.06 if voting vs 4.48 if abstaining on a 9-point scale, F(1,108) = 31.75, d = .49 (a MANOVA on turnout and victory ratings; the only significant effect was Behavior). Voting intention was high (7.15 and 6.26 on a 9-point scale); A&K say social desirability limited the range, and that 54% of the sample showed no projection. Correlation of the illusion with perceived waste is r = -.05 and with confidence in future voting r = -.03 (the text splits those two numbers across a hyphenated line, so there is no Quote for them). [M] binomial effect size display: .5 + .19/2 = 59.5% vs 40.5%, a 19-point gap, matching the sentence quoted. [M] 54% of 110 = 59.4, consistent with t(58) (59 participants).

### A16 [new] Study 1 "personal relevance" and anticipated emotions
- First pass said: not stated (line 161 mentions only the illusion).
- Mark: confirmed
- Source: scispace; same URL; Study 1 Results, Table 1; PDF p. 8 (printed p. 122) and PDF p. 9 (printed p. 123)
- Quote: "Perceptions of waste showed the predicted interaction [F(1, 108) = 50.31]."
- Quote: "Confidence in future voting showed an interaction [F(1, 108) = 48.76]"
- Quote: "Waste Vote 2.80 (1.85) 4.08 (2.51) Abstain 4.42 (2.42) 3.35 (2.13)"
- Quote: "Confidence Vote 7.18 (1.54) 6.52 (1.84) Abstain 6.15 (1.93) 7.02 (1.83)"
- Quote: "Regret Vote 1.40 (0.74) 3.30 (2.32) Abstain 2.87 (1.89) 6.48 (2.29)"
- Quote: "Satisfaction Vote 7.47 (1.70) 5.04 (2.29) Abstain 2.42 (1.65) 2.00 (1.44)"
- Quote: "Conversely, satisfaction was greater after victory than after defeat [F(1, 108) = 104.78], and it was greater after voting than after abstaining [F(1, 108) = 350.15]."
- Note: Table 1 columns are Victory then Defeat (means with SD; 1-9 scales; N = 110). Perceived waste is lowest after victory-and-voting (2.80) and after defeat-and-abstaining (3.35), as the counterfactual-reasoning idea predicts; the paper reads that as the "belief in personal relevance". Satisfaction is much higher after voting than abstaining even after defeat (5.04 vs 2.00): [M] differences 7.47 - 2.42 = 5.05 (victory) and 5.04 - 2.00 = 3.04 (defeat). These are hypothetical self-ratings, not dollars (see D in "Found that the first pass missed", item 8).

### A17 [new] Study 2 design and statistics
- First pass said: Study 2 (N = 86, 2000 US presidential election) (line 161).
- Mark: confirmed
- Source: scispace; same URL; Study 2, Table 3; PDF pp. 11-13 (printed pp. 125-127)
- Quote: "participants read the four scenarios. They were asked to assume that their preferred candidate had either won or lost the election, and that they had either cast a vote or abstained."
- Quote: "Participants were quite certain of having a preference [M = 6.19, t(84) = 6.87, d = .69]"
- Quote: "They also expressed strong intentions to vote [M = 6.35, t(84) = 6.23, d = .63]."
- Quote: "The expected interactions between Outcome and Behavior were significant for perceptions of both waste [F(1, 85) = 23.56] and confidence [F(1, 85) = 19.56]."
- Quote: "Assuming victory, perceptions of waste were lower after voting than after abstaining [F(1, 85) = 40.59, d = .69] but did not vary assuming defeat (F < 1)."
- Quote: "Waste Vote 2.67 (2.18) 3.48 (2.41) Abstain 4.35 (2.37) 3.38 (2.20)"
- Quote: "Confidence Vote 7.14 (2.14) 6.48 (2.39) Abstain 6.15 (2.41) 6.85 (2.33)"
- Quote: "Regret Vote 1.24 (0.61) 2.23 (1.81) Abstain 3.57 (2.20) 6.05 (2.60)"
- Quote: "Satisfaction Vote 7.21 (2.12) 5.12 (2.46) Abstain 2.34 (1.58) 1.85 (1.43)"
- Note: N = 86 undergraduates, in-class. The scenario said (my paraphrase) that the next US presidential election would be held in November 2000, most likely with one Democrat and one Republican candidate, and that analysts expected the candidate whose party best mobilized its supporters to win; it was given when that election was 18 months away. Three opening ratings (preference certainty, knowing the preference, likelihood of voting), then the four win/lose x vote/abstain scenarios with four ratings each. All ratings 1-9. Table 3 columns are Victory then Defeat. The authors say three of four simple effects matched Study 1 and only the waste difference between voting and abstaining after defeat became significantly smaller (printed p. 127; my paraphrase, the sentence is hyphen-split). **No illusion measure** (A9).

### A18 [new] What A&K say about whether voters' choices are correlated (the evidential question)
- First pass said: the evidential reading "is not excluded by 'no one knows'"; "the only number is r = .19 ... which measures a belief" (lines 165-166, 305; table line 128).
- Mark: confirmed
- Source: scispace; same URL; PDF p. 4 (printed p. 118); PDF p. 11 (printed p. 125); PDF p. 14 (printed p. 128); PDF p. 15 (printed p. 129)
- Quote: "Alternatively, people may merely believe that their own actions are diagnostic of collective behavior, in which case they can read their own voting as a sign that many like-minded others will vote too."
- Quote: "If magical thinking occurs, the voter’s illusion should be limited to those who act before instead of after most others."
- Quote: "Instead, the voter’s illusion simply appeared to capitalize on the perceived diagnosticity of one’s own decision."
- Quote: "People should recognize abstention as the dominating choice."
- Quote: "The evidential or inductive argument recognizes the relevance of the demon’s record of accurate predictions."
- Quote: "a person can expect the probability of box B being loaded to be higher if he or she takes only this box (Nozick, 1993)."
- Quote: "In voting and in other forms of cooperative dilemmas, social projection serves the same predictive purpose. Individuals can project their own intended choices to others."
- Quote: "In short, both the voter’s illusion and the belief in personal relevance are potentially rational, but not in the way envisioned by the traditional public-choice model."
- Quote: "Supposing that projection extends to the entire electorate, a citizen who intends to abstain might conclude that everyone will abstain."
- Note: What A&K say: (1) They test **causal vs evidential** accounts of the illusion by the timing manipulation: if people believed they *cause* others to vote, the illusion should be limited to early voters; it was not (r = .19 and .18), so "magical causation" is not supported and the illusion "appeared to capitalize on the perceived diagnosticity" (printed p. 125). (2) They frame the rationality of the projection as a choice between two normative frameworks (printed p. 128): dominance/causal (Quattrone & Tversky: abstention dominates because one's decision has "no causal role") and evidential/inductive (Nozick's Newcomb problem: "the demon's predictions and individual choices are conditionally dependent"; the sentence continues across a hyphen, hence the Quote starts at "a person can expect"). Voting "serves the same predictive purpose": projecting your choice is a prediction about others' (printed p. 128). (3) They conclude both mechanisms are "potentially rational, but not in the way envisioned by the traditional public-choice model" (printed p. 129). (4) **They never assert that real voters' choices are in fact correlated** and give no data on it: the evidential argument holds "accepting the view that" choices are conditionally dependent, and the only measured thing is participants' beliefs about it (A10). (5) Footnote 1 (printed p. 118) notes a "loop": if projection extends to the whole electorate, an intending abstainer expects everyone to abstain and so expects to break a 0-0 tie, then expects others to vote again, and so on.

### A19 [new] A&K on whose welfare counts (altruism, Parfit, Dovidio) and on rules
- First pass said: not stated for A&K (line 195, 303 cover Edlin et al., Barnett, Fowler).
- Mark: confirmed
- Source: scispace; same URL; PDF p. 15 (printed p. 129); PDF p. 16 (printed p. 130, footnote 3); PDF p. 17 (printed p. 131)
- Quote: "Dissenting, Parfit (1984) suggested that voters act rationally if they care about the benefits reaped by others as much (or nearly as much) as they care about their own."
- Quote: "True altruists would vote because the total number of people benefiting from victory of the presumed superior candidate is so large that it more than offsets the costs incurred by the individual voter."
- Quote: "This seems unlikely in light of the finding that altruistic motives tend to weaken as electorates become larger and their members more anonymous (Dovidio, 1984)."
- Quote: "a sociotropic orientation is ethical in the Kantian sense because it does not require the perception of a differential probability for one’s own action (Meehl, 1977)."
- Quote: "To preserve the system, voting, but not abstaining, could be a rule imposed on all."
- Quote: "Conversely, partisan politicians tend to appeal to significant outcomes being at stake, which can be construed as an appeal to altruism."
- Note: A&K state the altruistic argument (Parfit: others' welfare counted at near-equal weight makes voting pay because "the total number of people benefiting" is large), then doubt it: Parfit's conclusion hinges on altruism being strong, and altruism "tend[s] to weaken as electorates become larger" (Dovidio 1984; Dovidio unread, A&K's claim only). [I] This is a tension with the cancellation in Fowler and Edlin et al. (P about 1/N with others' benefit about N, requiring a constant weight alpha): if alpha shrinks as N grows, the product no longer stays flat. Footnote 3: a "sociotropic" (rule/community) orientation avoids needing a differential probability, and "voting, but not abstaining, could be a rule imposed on all" (the rule/group fork, report 3.5). A&K do not give any number for alpha.

### A20 [new] A&K on p and B: "perceived probability", Meehl's number, closeness
- First pass said: not stated for A&K.
- Mark: confirmed
- Source: scispace; same URL; PDF p. 2 (printed p. 116); PDF p. 15 (printed p. 129); PDF p. 16 (printed p. 130)
- Quote: "For an investment to be rational, the perceived probability of the desired outcome must be greater than zero."
- Quote: "My rough calculations indicate that my chances of determining who becomes President are about of the same order of magnitude (i.e., p = 10-8) as my chances of being killed driving to the polls"
- Quote: "Third, voter turnout increases with the expected closeness of the race (Aldrich, 1993)."
- Quote: "(although the voter’s illusion does not)"
- Quote: "all four elections occurred in the 19th century, they all involved seats in the House of Representatives, and the numbers of voters were below 10,000."
- Quote: "The implication is that since 1900, no election in the United States has turned on a single vote."
- Note: A&K use a **perceived** probability of the desired outcome (they describe the classic model, printed p. 116, as an investment by a citizen who weighs the expected benefits of winning against the costs of voting; that sentence has line-break hyphens, so it is my paraphrase, not a Quote). The Meehl number is quoted from Meehl 1977, p. 11; the image of PDF p. 15 shows the exponent as a superscript, p = 10 to the power -8 (the text file flattens it to "10-8"). A&K say closeness raises turnout via the belief in personal relevance, but "the voter's illusion does not" explain that (printed p. 130). The FEC sentences are A&K's reading of a federal agency web page as of about 2000; "since 1900, no election ... has turned on a single vote" is their implication, unverified, and should not be used as a fact. No tie rule (no 1/2) is mentioned anywhere in A&K; their counterfactual is "the election could have been lost / won" with one's vote.

### A21 [new] A&K on C and D
- First pass said: not stated for A&K (D discussed via Geys, Dowding, Sanders etc.).
- Mark: confirmed
- Source: scispace; same URL; PDF p. 2 (printed p. 116); PDF p. 17 (printed p. 131)
- Quote: "Moreover, casting a vote requires some time and effort."
- Quote: "which creates opportunity costs and possibly regrets."
- Quote: "voters can reap non-instrumental rewards regardless of the electoral outcome (Brennan & Lomasky, 1993)."
- Quote: "Some feel gratified by being able to act on their political attitudes and allegiances, whereas others seek to foster reputations as responsible citizens"
- Quote: "Like earlier research in this vein—most notably that of Quattrone and Tversky (1984)—our studies relied on university students as respondents, used scenarios to elicit judgments, and found relatively modest effect sizes."
- Note: C = "time and effort", cancelled or postponed activities ("opportunity costs and possibly regrets"), no dollar figure. D = "non-instrumental rewards regardless of the electoral outcome" (Brennan & Lomasky 1993): gratification from acting on attitudes and allegiances, and reputation as a responsible citizen; A&K label these "the expressive function of voting" (printed p. 116, hyphenated so no Quote). A&K do not estimate D. The anticipated satisfaction/regret ratings in A16-A17 are the only D-like measures and are hypothetical.

### A22 Provenance of the aggregator copy
- First pass said: "Acevedo & Krueger (an aggregator copy)" used with low confidence (line 337); "https://scispace.com/pdf/... [S] (an aggregator copy)" (line 161).
- Mark: confirmed
- Source: scispace; same URL; page headers and footer, PDF p. 1 and p. 2
- Quote: "Political Psychology, Vol. 25, No. 1, 2004"
- Quote: "Two Egocentric Sources of the Decision to Vote: The Voter’s Illusion and the Belief in Personal Relevance"
- Note: The file is a 20-page PDF with the journal's own running heads ("116 Acevedo and Krueger", "Egocentric Sources of the Decision to Vote 117"), the Blackwell copyright footer, and the 115-134 pagination, so the **page numbers above are the journal's printed pages** and the report's "p. 117 / 118 / 122" are correct as journal pages. PDF metadata names Political Psychology and the authors (Producer PyPDF2). I cannot check it against the publisher's own copy (no network), so it is an aggregator copy of the typeset article.

---

# Part B. Fowler, "Altruism and Political Participation" (working paper, March 31, 2005), fowler_wp

### F1 Claims about Fowler (2006), "Altruism and turnout", J. of Politics (not this source)
- First pass said: "Fowler (2006), 'Altruism and turnout', *J. of Politics*: via a Greater Good (Berkeley) article, not the paper ... The paper itself is unread." (lines 192, 327)
- Mark: unread
- Source: fowler_wp (not the same document); https://econwpa.ub.uni-muenchen.de/econ-wp/exp/removed/0504001.pdf; title page, PDF p. 1 (unnumbered) and voting result PDF p. 21 (printed p. 20)
- Quote: "March 31, 2005"
- Quote: "This paper is prepared for delivery at the Midwest Political Science Association annual meeting in Chicago, 2005."
- Quote: "I extend this model in two ways. First, I generalize it for all acts of political participation."
- Quote: "Finally, it is interesting to note that neither altruism nor discrimination in altruism affects voting."
- Note: This source is the **working paper**, an earlier and different document. **Title**: "Altruism and Political Participation" (journal version per the first report: "Altruism and Turnout", J. Politics 2006; I did not read it). **Scope**: the WP covers seven acts of participation (vote, contribute to a candidate, join a political organization, donate to one, attend local board meetings, volunteer for a local board, protest), builds an equally-weighted index, and says it generalises the model "for all acts of political participation". **Its voting result is null**: neither altruism nor discriminating altruism affects voting in the WP's Table 7 (F17). That is the opposite of the Greater Good sentence the first report quotes for the 2006 article. So the WP's numbers cannot stand in for the journal's, and the journal paper must be read before the site cites any Fowler result on turnout. [I] the shorter journal title suggests a narrower focus on turnout.

### F2 Greater Good quote: dictator-game givers "were significantly more likely to have voted in the most recent election"
- First pass said: people who gave more in a dictator game "were significantly more likely to have voted in the most recent election" (line 192).
- Mark: unread
- Source: fowler_wp; the words are the Greater Good article's about the 2006 journal paper; not in the WP
- Quote: "Finally, it is interesting to note that neither altruism nor discrimination in altruism affects voting."
- Note: Not in this source. In the WP the only voting measure is "Did you happen to vote in the 2004 general election in November?" (appendix, printed p. 25; 73.4% of subjects said yes) and altruism was **not** retained in the voting model. I cannot say whether the 2006 article used a different sample, measure or model; I did not read it.

### F3 Greater Good quote: "Altruism only mattered among people who were politically partisan"
- First pass said: "Altruism only mattered among people who were politically partisan" (line 192).
- Mark: unread
- Source: fowler_wp; not in the WP
- Quote: "Strong partisans give 9.4% less than others to the anonymous recipient, a difference equivalent to about one third of the mean allocation."
- Note: The WP has no test of altruism interacting with partisanship in the participation models. What it does say: strong partisans give **less** to the anonymous recipient (24.4% vs 33.8%, Table 2; "strong partisans give 22% less ... than independents" in the Tobit, printed p. 13), partisan strength is a separate positive predictor of participation (Table 6, best model coefficient 1.31, SE 0.38), and "partisan strength" and "selfish partisan bias" are WP terms. So the sentence about partisans is either about a different analysis or the 2006 version; unread.

### F4 Fowler's reading, "altruism combined with the belief that politics matters"
- First pass said: "altruism combined with the belief that politics matters" (line 192).
- Mark: unread
- Source: fowler_wp; not in the WP (searched "belief", "matters": no hit)
- Quote: "I rework the traditional calculus of participation model by adding a term for benefits to others."
- Note: The WP never uses that phrase. Its mechanism is only the multiplication of a small P by a large number of beneficiaries (F8). Whether the 2006 article adds a "belief that politics matters" is unread.

### F5 Geys p. 20: "only those with different preferences ... ('discriminating altruists') are motivated to vote by altruism"
- First pass said: Geys p. 20: Fowler argues this (line 192).
- Mark: unread
- Source: fowler_wp (Geys's text is another source's)
- Quote: "if politics involves transfers from one group to another, then unconditional altruists gain nothing from participating."
- Quote: "It is important to realize that the altruism hypothesis and the discriminating altruism hypothesis may not be mutually exclusive."
- Note: In the WP, discriminating altruism is **one of two channels**. Pure altruism (the "altruism hypothesis") works when an activity gives "a positive average benefit to the whole population"; discriminating altruism matters only when politics is distributive (transfers). The WP does not say "only". If Geys's sentence is about elections as transfer contests it is consistent with the WP's distributive case; if it summarises the journal version it may differ. [I]. See F8-F10.

### F6 Geys: altruism-weight utility function (eq. 3), alpha "the weight we attach to other's happiness"
- First pass said: Fowler "gives an altruism-weight utility function (eq. 3, alpha 'the weight we attach to other's happiness')" (line 192, via Geys).
- Mark: unread
- Source: fowler_wp; the quoted words and the equation number are Geys's; the WP has no numbered equations
- Quote: "weight a player attaches to the other player’s payoff, α"
- Quote: "cares about benefits to others, which is labeled α for altruism. These assumptions transform the calculus of political participation to P(BS + αNBO) > C."
- Note: The WP defines alpha twice: in the participation calculus, "how much the citizen cares about benefits to others, which is labeled α for altruism"; and in dictator-game footnote 1, "the weight a player attaches to the other player's payoff". Neither uses the words "the weight we attach to other's happiness". The calculus is `P(BS + αNBO) > C` (F8). Whether Geys's eq. 3 is the same expression is unread (Geys is another reader's source).

### F7 Identity, date and provenance of the working paper
- First pass said: not stated (the report treats only the 2006 paper).
- Mark: confirmed
- Source: fowler_wp; https://econwpa.ub.uni-muenchen.de/econ-wp/exp/removed/0504001.pdf; title page, PDF p. 1
- Quote: "Altruism and Political Participation"
- Quote: "March 31, 2005"
- Quote: "This paper is prepared for delivery at the Midwest Political Science Association annual meeting in Chicago, 2005."
- Note: James H. Fowler, UC Davis (affiliation on p. 1); a conference paper for the 2005 Midwest Political Science Association meeting; 28 PDF pages (27 numbered plus the title page). It says "A copy of the most recent version can be found at http://jhfowler.ucdavis.edu", i.e. it expected revision. The URL path contains `/exp/removed/`: the file sits in an "exp/removed" directory of the EconWPA archive. I cannot say why (withdrawn, superseded, or moved), and I did not use the network to find out. The PDF's own creation date is 2005-04-01.

### F8 The model: how benefits to others enter, what multiplies what
- First pass said: Edlin et al. eq. 2 `B = B_self + alpha N B_soc`; "p proportional to 1/n and the social part of B proportional to N, so ... their product is roughly flat in electorate size" (lines 191, 195-196); Fowler's alpha function via Geys (line 192).
- Mark: confirmed (same structure stated in the WP)
- Source: fowler_wp; Altruism and Political Participation section; PDF pp. 3-5 (printed pp. 2-4)
- Quote: "For simplicity, a citizen receives a benefit B > 0 if her preferred outcome occurs, and 0 otherwise."
- Quote: "Participation in the political activity has a cost C > 0 because it takes time, money, and other"
- Quote: "resources to contribute to a collective endeavor to secure the outcome."
- Quote: "However, participation also increases the probability that the preferred outcome will prevail by P. Thus, the citizen will participate if PB > C."
- Quote: "In general, the probability that a single person’s decision to participate will affect a political outcome is decreasing in the size of the relevant population, N."
- Quote: "that P is approximately proportional to 1/N for voting. Thus, PB is probably less than C for most acts of political participation,"
- Quote: "Scholars incorporate altruism into the traditional calculus of participation model by assuming that each citizen also cares about the benefits that others secure from the preferred outcome"
- Quote: "Under this assumption, B is a function not only of direct benefits to oneself BS, but to the N other people affected by the outcome who would gain an average benefit BO if the citizen’s preferred alternative occurs."
- Quote: "cares about benefits to others, which is labeled α for altruism. These assumptions transform the calculus of political participation to P(BS + αNBO) > C."
- Quote: "If P is proportional to 1/N and N is large, then the decision to participate reduces approximately to whether or not αBO > C."
- Quote: "those who exhibit a sufficient degree of concern for the welfare of others will be willing to engage in costly political participation. I call this the altruism hypothesis."
- Quote: "although the probability that a single act of participation affects the outcome of a political activity in large populations is quite small, the number of people who enjoy the benefit is large."
- Note: **The model** (inline, no equation numbers; the formulas below read B_S and B_O as subscripts, as on the PDF): participate iff `P (B_S + α N B_O) > C`. B_S = the citizen's own gain if her preferred outcome occurs; N = the number of *other* people affected ("the N other people affected by the outcome"); B_O = their **average** gain; alpha = one scalar weight on others' welfare (the text does not bound it; [I] alpha = 0 reduces the formula to the pure self-interest model PB_S > C). P = the increase in the probability that the preferred outcome prevails. So **P multiplies the whole bracket; alpha multiplies N x B_O; B is the gain conditional on the preferred outcome occurring (not "gain if decisive"), and P x B is the expected gain.** With P about 1/N the bracket's second term is N-independent: [M] P(B_S + alpha N B_O) = B_S/N + alpha B_O when P = 1/N, so for N large the rule is alpha B_O > C, as the paper says. **Role of the number who enjoy the benefit**: it is N, the same symbol as "the size of the relevant population" in P about 1/N; the WP does not distinguish the number of participants (which sets P) from the number affected (which sets the benefit), so the cancellation holds exactly when those two scale together. This is the same cancellation the first report credits to Edlin et al.; the WP cites Edlin, Gelman and Kaplan (2003) and Jankowski (2002, 2004) as the origin: "Scholars have recently reworked the traditional calculus of voting model by adding a term for benefits to others". No numerical value of alpha, B_O, N or P is given anywhere in the WP.

### F9 The discriminating-altruism model
- First pass said: Geys p. 20 on "discriminating altruists" (line 192).
- Mark: confirmed
- Source: fowler_wp; Discriminating Altruism and Political Participation section; PDF pp. 5-6 (printed pp. 4-5)
- Quote: "One wrinkle in this story is the fact that it assumes that the political activity in question yields a positive average benefit to the whole population."
- Quote: "Another wrinkle is the assumption that individuals exhibit the same degree of altruism to all members of the population."
- Quote: "suppose that there are two possible outcomes to a political activity and there are two equally sized groups X and Y in the population such that NX = NY = N / 2."
- Quote: "the individual deciding whether or not to participate receives a benefit BS > 0, each person in group X receives a benefit BO > 0, while each person in group Y must pay a cost –BO."
- Quote: "This changes the calculus of participation to P(BS + αX NX BO – αY NY BO) > C. Again, under the assumption that P is approximately 1/N, this equation reduces to (αX – αY) BO > 2C."
- Quote: "What the equation suggests is that people who do not discriminate between the two groups ( αX = αY ) will not be motivated to participate since the left hand side reduces to zero."
- Quote: "Regardless of how much one values benefits to others, the participatory act would not be an act of altruism because it would not be providing a net gain for others"
- Quote: "it would merely transfer resources between two groups about which the individual cares equally."
- Quote: "On the other hand, discriminating altruists, who value benefits to group X more than to group Y ( αX > αY ) will have an incentive to participate"
- Quote: "this incentive will be increasing in the amount with which they discriminate between the two groups. I call this the discriminating altruism hypothesis."
- Note: **Model** (distributive politics): two equal groups of N/2; the other outcome gives nothing to anyone; the preferred outcome gives the citizen B_S, each X member +B_O and each Y member -B_O; separate weights alpha_X, alpha_Y. Participate iff `P (B_S + alpha_X (N/2) B_O - alpha_Y (N/2) B_O) > C`. **Here others' welfare enters with sign**: Y members *lose*. [M] with P = 1/N: (1/N)[B_S + (alpha_X - alpha_Y)(N/2) B_O] = B_S/N + (alpha_X - alpha_Y) B_O / 2 > C, so for N large (alpha_X - alpha_Y) B_O > 2C, matching the paper. [M] The "2C" depends on P = 1/N exactly (proportionality constant 1); with P = K/N (Edlin et al.'s K) it would be (alpha_X - alpha_Y) B_O > 2C/K, and the pure-altruism rule alpha B_O > C/K. The WP drops the constant ("approximately 1/N"), so it does not carry a measure of how close races are.

### F10 The two hypotheses as the WP states them
- First pass said: not stated.
- Mark: confirmed
- Source: fowler_wp; Abstract, PDF p. 1; PDF pp. 5-6 (printed pp. 4-5)
- Quote: "if politics involves transfers from one group to another, then unconditional altruists gain nothing from participating."
- Quote: "However, discriminating altruists who care more about some groups than others will have a significant incentive to participate in activities that make members of their preferred groups better off."
- Quote: "It is important to realize that the altruism hypothesis and the discriminating altruism hypothesis may not be mutually exclusive."
- Note: **Unconditional altruist** = alpha_X = alpha_Y (cares equally about the two groups); **discriminating altruist** = alpha_X differs from alpha_Y. The WP calls them "unconditional" in the abstract and "do not discriminate" in the text. The altruism hypothesis (any concern for others raises participation when the activity benefits the whole population) and the discriminating one (concern that differs by group raises participation in redistributive activities) are meant to hold together ("Politics is usually about both how to make the pie larger and how to split it").

### F11 Sample
- First pass said: "Sample size and effect size not seen" (line 192).
- Mark: confirmed
- Source: fowler_wp; Research Design and Subject Profile; PDF pp. 8-9 (printed pp. 7-8)
- Quote: "In December 2004, about 350 subjects were recruited from undergraduate political science and sociology courses to participate in a study administered by computer."
- Quote: "Subjects were offered credit towards their course grade to show up for the study, and 306 (about 85%) of them chose to participate."
- Quote: "Subjects range in age from 18 to 43 years, but the average age is 21. The sample is weighted somewhat towards women (56%) and a substantial number (43%) identify themselves as minorities."
- Quote: "The median family income is about $80,000 a year."
- Quote: "herself at 3.45 on the seven point liberal conservative scale and 3.14 on the seven point party identification scale."
- Quote: "One might argue that these results are of limited value because they are based on the behavior of college students who are not representative of the population as a whole."
- Quote: "Even if future work suggests that the altruism and discriminating altruism theories cannot explain the habits of older adults, it might still help to explain how these habits are formed."
- Note: **N = 306** undergraduates, December 2004 (the WP's own N; the 306 appears as the total in Tables 1 and 2; 173 women, 133 men). [M] 306/350 = 87.4%, the paper says "about 85%". The university is not named (the author is at UC Davis and the paper compares reported turnout with "the city of Davis", so Davis is likely; [I]). Subjects got course credit for showing up and played for lottery tickets (F12), not cash. The author's own caveat: college students, "not representative" (printed p. 21), with the argument that early adulthood forms habits (printed p. 22). These are the WP's N and results; **they are not the journal paper's** (F1).

### F12 Dictator-game design and which recipients
- First pass said: not stated (the report knows only "dictator game" from the Greater Good article).
- Mark: confirmed
- Source: fowler_wp; Dictator Game Method; PDF pp. 9-10 (printed pp. 8-9); Appendix PDF p. 24 (printed p. 23)
- Quote: "Subjects are given ten lottery tickets that each have an equal chance of winning a prize of $100."
- Quote: "They are then given two identical and opaque envelopes and asked to place the tickets they wish to keep for themselves in one envelope and the tickets they wish to share with an anonymous individual in another envelope."
- Quote: "They seal both envelopes, place the envelope designated for the anonymous individual in a locked mailbox under their computer, and then keep the other envelope for themselves."
- Quote: "I ask each individual to play three dictator games with different information about the anonymous recipient."
- Quote: "In one game, subjects are told “you know nothing about this anonymous individual.”"
- Quote: "In the other two games subjects are told “The only thing you know about this individual is that he or she is a registered Republican [Democrat].”"
- Quote: "The order of these treatments is randomized and a variable indicating the order is included in the analysis below."
- Quote: "since the expected value of the prize is only $100 / N ≈ $0.33"
- Quote: "You may keep one of these envelopes, but we will give the other envelope to a randomly chosen anonymous individual."
- Quote: "Altruism is coded as the fraction of tickets given to the anonymous player."
- Quote: "Discriminator is a dummy variable that equals 1 if the amount given to the Democrat, Republican, and anonymous recipient are not equal, and 0 otherwise."
- Quote: "The recipient is completely anonymous in all three games, but in two of the games subjects are informed that the recipient is a registered Democrat or a registered Republican."
- Note: **Design**: each subject divides 10 lottery tickets (each ticket an equal chance at $100) between self and a randomly chosen anonymous recipient, three times in random order: (1) a recipient about whom they "know nothing", (2) a "registered Republican", (3) a "registered Democrat". **Altruism = fraction of tickets given to the anonymous (nothing-known) recipient; Discriminator = 1 if the three allocations are not all equal.** The stake is low: the expected value is "$100 / N ≈ $0.33" (N is not defined at that point in the text; [M] 100/306 = $0.327 if N is the 306 subjects, [I]). Whether the recipients really were registered Democrats or Republicans, and who received the envelopes, is not stated. The WP defends the low stakes by citing Camerer and Hogarth (1999), Forsythe et al. (1994), Carpenter et al. (2004) (printed p. 9).

### F13 Participation measure (the dependent variable)
- First pass said: not stated.
- Mark: confirmed
- Source: fowler_wp; PDF p. 9 (printed p. 8); Appendix PDF p. 26 (printed p. 25)
- Quote: "About 73.4% said they voted in the 2004 general election (compared to official turnout of 81.4% for the city of Davis) while 20.6% said they had given money to a candidate."
- Quote: "A participation index was created using a simple equally-weighted sum of responses to each of these seven questions."
- Quote: "The average subject participated in 2.41 of these activities, with 12.5% of them never participating in any activity and 2.3% participating in all of them."
- Quote: "Did you happen to vote in the 2004 general election in November?"
- Quote: "Contribute to a Candidate - “Have you ever contributed money – to an individual candidate, a party group, a political action committee, or any other organization that supports candidates in elections?”"
- Note: Seven yes/no items summed (index mean 2.41, 12.5% with none). Only the vote item is tied to a specific election (2004); the other six are not tied to a date (four of them begin "Have you ever ..."; "join" and "donate" ask about membership and giving without a date), so for 18-43-year-old students the index is mostly lifetime participation. Self-reported 2004 turnout was 73.4%, the paper notes the Davis official figure of 81.4%.

### F14 Dictator-game allocations (all subjects)
- First pass said: not stated.
- Mark: confirmed
- Source: fowler_wp; Table 1 and text; PDF pp. 10-11 (printed pp. 9-10); Table 2, PDF p. 13 (printed p. 12)
- Quote: "subjects in this experiment were even more likely (38.0%) to keep everything for themselves than those in both treatments."
- Quote: "the mean allocation (29.9%) falls between the two treatments"
- Quote: "All 29.9% 30.1 27.3 306"
- Quote: "Low Income 34.2 32.1 28.0 132 High Income 26.8 27.9 26.3 145"
- Quote: "Female 32.6 32.2 27.3 173 Male 26.5 27.4 27.3 133"
- Quote: "those with low incomes (below the median) give 6.4% more than those with high incomes to the anonymous recipient, while women give 6.1% more than men."
- Note: Mean share of the 10 tickets given: **29.9% to the anonymous recipient, 30.1% to the registered Democrat, 27.3% to the registered Republican** (columns: anonymous, Democrat, Republican; N = 306); 38.0% kept everything (in the anonymous game, as the paper's comparison with Forsythe et al. implies [I]). Table 1 p-values are one-sided t-tests ("probability that true relationship is opposite to the sign of the difference"): low vs high income 7.4 points, p = .02 (anonymous); women vs men 6.1, p = .04. [M] 34.2 - 26.8 = 7.4, so the sentence quoted (6.4%) disagrees with the Table 1 figure (7.4); income N 132 + 145 = 277, not 306 (29 not shown). These matter only if the site cites the table.

### F15 Partisanship in giving
- First pass said: not stated.
- Mark: confirmed
- Source: fowler_wp; Table 2 and Tables 3-5; PDF pp. 13-16 (printed pp. 12-15)
- Quote: "Democrat 29.6 31.5 26.0 173 Republican 29.2 29.6 32.7 78"
- Quote: "Strong Partisan 24.4 29.5 25.4 127"
- Quote: "Strong partisans give 9.4% less than others to the anonymous recipient, a difference equivalent to about one third of the mean allocation."
- Quote: "Notice that the Republican recipient inspires the largest divergence, receiving 6.7% more from Republican donors than Democratic donors, or about a fifth of the mean allocation."
- Quote: "after controlling for income and gender, strong partisans give 22% less to the anonymous recipient than independents."
- Quote: "About 61.7% of the subjects gave exactly the same amount to the registered Democrat and registered Republican that they gave to the anonymous recipient."
- Quote: "I will refer to the remaining 38.3% of the subjects as discriminators"
- Quote: "First, Republicans receive lower allocations from all donors except strong Republicans, suggesting that there is a partisan bias against sharing with them."
- Note: Four findings: partisan bias (Republican recipient gets 2.8 points less than the Democrat, p = .03, Table 4), own-party bias, "selfish partisan bias" (strong partisans give less to everyone), "partisan strength bias". Table 2 columns: anonymous, Democrat, Republican; Democratic donors 29.6/31.5/26.0 (N = 173), Republican donors 29.2/29.6/32.7 (N = 78); strong partisans 24.4/29.5/25.4 (N = 127). **Discriminators = 38.3% of subjects** (not all three allocations equal); 61.7% gave the same to all. Internal inconsistency in the WP: the introduction says the Republican recipient gets less "even when the donor is a Republican" (PDF p. 3), but Table 2 has Republican donors giving more to the Republican (32.7) than the Democrat (29.6), and the conclusion says "except strong Republicans". I do not use these for anything below.

### F16 Key results: altruism and discriminating altruism raise the participation index
- First pass said: "Sample size and effect size not seen" (line 192).
- Mark: confirmed
- Source: fowler_wp; Altruism, Discriminators, and Participation; Table 6; PDF pp. 17-19 (printed pp. 16-18); Table 6 checked on the PDF image (PDF p. 18)
- Quote: "Those who gave more than 30% (the median allocation) to the anonymous recipient participated in 2.64 of 7 activities compared to 2.24 activities for those who gave 30% or less."
- Quote: "Discriminators (those who gave different amounts depending on the partisanship of the recipient) participated in 2.74 activities compared to 2.21 for those who gave the same amount to all three recipients."
- Quote: "One-sided t-tests suggest that both of these differences are significant (p=0.03, p=0.01, respectively)."
- Quote: "Altruism 0.72 0.39 0.51 0.34 0.80 0.32 0.01"
- Quote: "Discriminator 0.58 0.25 0.52 0.21 0.40 0.20 0.05"
- Quote: "Note: Tobit regression. Best model selected using stepwise AIC."
- Quote: "To make these results more concrete, subjects who allocate an equal share to themselves and the anonymous recipient in the dictator game participate in 0.40 more activities than subjects who keep everything for themselves."
- Quote: "Moreover, subjects who change the amount they give based on the partisanship of the recipient also participate in 0.40 more activities than those who give the same amount to each recipient."
- Note: **Raw**: split at the median allocation (30%): 2.64 vs 2.24 activities (diff 0.40, one-sided p = .03); discriminators 2.74 vs 2.21 (diff 0.53, p = .01) [M, differences]. **Tobit on the 0-7 index** (Table 6, columns coefficient, SE for simple / full / best model, then the best model's p): Altruism 0.72 (0.39), 0.51 (0.34), **0.80 (0.32), p = .01**; Discriminator 0.58 (0.25), 0.52 (0.21), **0.40 (0.20), p = .05**. The "best" model is picked by stepwise AIC from the full model; the full model has no p column, and [M] 0.51/0.34 = 1.50 for altruism in the full model, so the stated effect holds in the stepwise-selected model and is weaker in the all-controls model. Controls in the best model: partisan identification, partisan strength, political interest (3.28), sex, citizen, write letter, make decisions. The "0.40 more activities" is [M] 0.80 x 0.5 = 0.40 (altruism is a fraction from 0 to 1, so giving half of 10 tickets vs none), as the paper does it; Tobit coefficients are on the latent index and the paper reads them as the index [I].

### F17 Individual acts (Table 7): altruism effects on voting
- First pass said: not stated; line 192 reports the Greater Good claim about voting.
- Mark: confirmed
- Source: fowler_wp; Table 7 and text; PDF pp. 20-21 (printed pp. 19-20); Table 7 checked on the PDF image (PDF p. 20)
- Quote: "Best fitting logit models for each dependent variable using stepwise AIC model selection."
- Quote: "altruism is retained in the models for contribution to a candidate, donation to a political organization, attendance at local board meetings, and volunteering for a local government board."
- Quote: "The discriminator dummy is retained only in the models for contributing to a candidate and participating in a protest."
- Quote: "Finally, it is interesting to note that neither altruism nor discrimination in altruism affects voting."
- Quote: "This may be due to the uniquely low costs of this form of political participation."
- Quote: "If C is very close to zero, then other factors important to voter turnout may be sufficient to push individuals over the cost-benefit threshold, making it less likely that variation in altruism will have an impact on voting."
- Quote: "Although it is not immediately obvious what these two forms of participation have in common, the discriminating altruism theory suggests that they may be those forms of participation with the greatest impact on distributional conflicts."
- Note: Logit coefficients (SE in brackets), from the image: Altruism: contribute to a candidate 0.75 (0.52), donate to a political organization 0.68 (0.45), attend local board meetings 0.84 (0.53), volunteer for a local board 1.27 (0.48); Discriminator: contribute to a candidate 1.01 (0.33), protest 0.39 (0.27). [M] coefficient/SE: 1.44, 1.51, 1.58, 2.65 (altruism); 3.06, 1.44 (discriminator); only volunteering and contributing-with-discriminator exceed about 2. **Table 7 gives SEs and AIC only, no p-values.** The **Vote** column contains no altruism or discriminator coefficient: both were dropped by stepwise AIC, so the WP reports **no estimate, SE or interval for altruism on voting**, only the exclusion. Its explanation (low cost of voting; Aldrich 1993; Verba et al. 1995) is a conjecture. "Join a political organization" retained neither altruism variable.

### F18 The "unconditional versus discriminating altruists" result
- First pass said: Geys: "discriminating altruists" are the ones motivated to vote by altruism (line 192).
- Mark: confirmed (what the WP says; Geys's sentence itself unread, F5)
- Source: fowler_wp; PDF p. 19 (printed p. 18), Table 6 and text; PDF p. 21 (printed p. 20)
- Quote: "Thus, discriminating altruists appear to be more motivated to participate in politics than altruists who weigh benefits to all groups equally."
- Quote: "Note that even though there are numerous controls, both altruism and the discriminator dummy continue to have a positive influence on participation."
- Quote: "People who share with an anonymous individual in the dictator game participate in politics more than those who do not share."
- Quote: "People who vary the amount they give depending on the partisan affiliation of the recipient also participate more than those who give the same amount to everyone."
- Note: **Theory**: unconditional altruists (alpha_X = alpha_Y) gain nothing from participating in transfer politics; discriminators do (F9). **Data**: both altruism and the discriminator dummy have **positive** coefficients on the 0-7 participation index (0.80, p = .01; 0.40, p = .05), so the data do not show that unconditional altruists do *not* participate; the WP reads this as support for both hypotheses (they are "not mutually exclusive"). For individual acts the discriminator effect shows only for contributing to a candidate and protest, the altruism effect for four other acts (F17). **Neither** shows for voting. Caveats [I]: the comparison group for "discriminator" is everyone who gave the same to all three recipients, which includes people who gave 0 to all (i.e. egoists), though altruism is a control; and the index mixes distributive and non-distributive acts, so it does not separate the two hypotheses; the WP itself concedes it is "not immediately obvious" what the two acts retained for the discriminator "have in common".

### F19 Dictator allocation as a measure of the weight alpha (footnote 1)
- First pass said: Geys's alpha "the weight we attach to other's happiness" (line 192).
- Mark: confirmed (the WP's own treatment)
- Source: fowler_wp; footnote 1; PDF p. 8 (printed p. 7); the formula read from the PDF image
- Quote: "there is a monotonic relationship between the equilibrium allocation in the dictator game and the weight a player places on the other player’s utility"
- Quote: "weight a player attaches to the other player’s payoff, α"
- Quote: "where ρ < 1 represents the convexity of preferences and the budget constraint is π s + π o = 1"
- Quote: "The well-being of others is probably more important to a person who chooses to allocate 20% than one who allocates 0%."
- Note: Footnote 1 (from the image): utility `U(pi_s, pi_o) = (pi_s^rho + alpha pi_o^rho)^(1/rho)`, rho < 1, budget pi_s + pi_o = 1, optimum `pi_o* = 1 - (1 + alpha^(1/(1-rho)))^(-1)`, increasing in alpha (the text file scrambles the formula, so I have no Quote for it). [M] check: the first-order condition gives pi_o/pi_s = alpha^(1/(1-rho)) and so pi_o = x/(1+x) with x = alpha^(1/(1-rho)), which equals the footnote. **The WP never estimates alpha or rho**: the "Altruism" regressor is the raw fraction of tickets given. The 29.9% mean allocation is not a value of alpha, and converting it needs a value of rho the paper does not supply.

### F20 What the WP says about whether voters' (participants') choices are correlated
- First pass said: the evidential reading "is not excluded by 'no one knows'" (lines 165, 305); nothing from Fowler.
- Mark: confirmed
- Source: fowler_wp; PDF p. 2 (printed p. 1) and PDF p. 4 (printed p. 3); a text search for "correl" (outside regression/variable use), "diagnos", "conditional" and "belief" found nothing bearing on this
- Quote: "This gives individuals an incentive to avoid the costs of participation and free ride on the efforts of others"
- Quote: "In general, the probability that a single person’s decision to participate will affect a political outcome is decreasing in the size of the relevant population, N."
- Quote: "it may be just one of thousands or even millions of other contributions."
- Quote: "For example, if the participatory act is voting, then the outcome can only be changed when there is an exact tie, or when the vote can create a tie."
- Note: **The WP is silent on correlated choice.** Its P is the "probability that a single person's decision to participate will affect a political outcome", a counterfactual probability treating others' acts as given ("one of thousands or even millions of other contributions"; "free ride on the efforts of others"); no sentence says one's own choice is evidence about others'. So under the WP's model the evidential reading is neither used nor excluded; it is simply not discussed. The WP's reference list contains neither Quattrone & Tversky nor Grafstein.

### F21 Fork points in the WP's model (rule 10)
- First pass said: fork points in lines 301-305, 125-131 (table rows 3.1-3.7).
- Mark: confirmed
- Source: fowler_wp; PDF pp. 3-5, 19, 21 (printed pp. 2-4, 18, 20)
- Quote: "Scholars incorporate altruism into the traditional calculus of participation model by assuming that each citizen also cares about the benefits that others secure from the preferred outcome"
- Quote: "For example, if the participatory act is voting, then the outcome can only be changed when there is an exact tie, or when the vote can create a tie."
- Quote: "they tend to correlate with the costs of acquiring information about politics"
- Quote: "people without skills may experience greater initial costs to participation since they would have to learn new skills in order to contribute to the collective activity."
- Quote: "Aldrich (1993) observes that voting is probably a very low cost activity, and Verba, et al. (1995) argue that voting is the least costly of the main ways to participate in politics."
- Note: Fork by fork. (1) **Whose welfare in B**: the voter's own B_S plus the N others' average B_O, weighted by one scalar alpha; in the distributive version others can lose and alpha is group-specific (F8, F9). (2) **B as gain-if-decisive vs pB**: B is the gain if the preferred outcome occurs; P is the probability increase; PB is the expected gain. For voting P is the chance of an exact tie or of creating a tie. (3) **Tie rule 1/2**: not mentioned; the WP says only "an exact tie, or ... create a tie". (4) **Held fixed, causal vs evidential**: P is the single act's probability of affecting the outcome (F20). (5) **D**: the WP has **no D term** (no duty, expressive or consumption term; the word "duty" appears only in the title of a cited paper, Jankowski 2002); the sole nod to other motives is "other factors important to voter turnout" in the voting discussion (F17), unspecified. (6) **C**: "time, money, and other resources"; and the WP counts **information costs and skills in C** by interpretation: SES variables "correlate with the costs of acquiring information about politics" and "people without skills may experience greater initial costs"; the WP asserts but does not measure that voting is "a very low cost activity" (Aldrich, Verba et al., both cited as authority). The first report said it found no measured information cost; the WP gives none either, only the classification.

### F22 Limits and internal inconsistencies in the WP (for anyone citing its numbers)
- First pass said: not stated.
- Mark: confirmed
- Source: fowler_wp; PDF pp. 10-11, 13, 20 (printed pp. 9-10, 12, 19)
- Quote: "since the expected value of the prize is only $100 / N ≈ $0.33"
- Quote: "those with low incomes (below the median) give 6.4% more than those with high incomes to the anonymous recipient, while women give 6.1% more than men."
- Quote: "The Republican recipient tends to receive less than the Democrat or the unidentified anonymous recipient, even when the donor is a Republican."
- Quote: "Note: p-values reflect probability that true relationship is opposite to the sign of the difference (one-sided t-test)."
- Note: (a) Table 1 gives 7.4 points for low vs high income where the text says 6.4 [M 34.2 - 26.8 = 7.4]. (b) Table 2 contradicts the introduction on Republican donors (F15). (c) Table 7 has no p-values (F17). (d) Tables 1, 2, 4 use one-sided p-values; the paper says so. (e) N = 306 undergraduates, low stakes, recipients identified only by a one-line partisanship label. (f) The quote about the prize uses an undefined N. (g) The only voting outcome is a self-reported 2004 vote. The first report's table row for 3.7 ("pB roughly independent of electorate size") is a statement about the model, which the WP supports as a derivation; its **empirical** support in the WP is nil for voting.

---

## Corrections table

No fact in the first report's statements about these two sources was found wrong. Wording to tighten, none a change of fact:

| Old (first report) | New | Source |
|---|---|---|
| "Study 2 ... found no measure of the illusion" (line 161) | "Study 2 had no measure of the illusion" (it was designed to test the belief in personal relevance only) | scispace, PDF p. 11 (printed p. 125); A9 |
| "weaker reading: they 'may merely believe ...'" read as Quattrone & Tversky's own weaker reading (line 161) | A&K's own alternative to Quattrone & Tversky's attribution (belief that one's vote might induce others, "magical thinking") | scispace, PDF p. 4 (printed p. 118); A3, A12 |
| Study 1 effect called "modest" with no qualification (line 161) | Authors' own words: "relatively modest" but "not negligible"; "rather conservative estimates"; "more modest than ... Quattrone and Tversky's original study" | scispace, PDF pp. 8, 10, 18 (printed pp. 122, 124, 132); A7 |
| "Sample size and effect size not seen" for Fowler (line 192) | **This working paper**: N = 306; Table 6 best model altruism 0.80 (SE 0.32, p = .01), discriminator 0.40 (SE 0.20, p = .05). These are the WP's, not the 2006 article's | fowler_wp, PDF pp. 8, 18 (printed pp. 7, 17); F11, F16 |
| (Greater Good) altruists "were significantly more likely to have voted" (line 192) | In the **working paper** "neither altruism nor discrimination in altruism affects voting" (not a correction of the 2006 article, which is unread, but the two sources conflict) | fowler_wp, PDF p. 21 (printed p. 20); F1, F2, F17 |
| [M] A&K p-value | r(108) = .19 gives one-tailed p = .023 by my computation, paper prints .027 (consistent only at the edge of r's rounding) | scispace, PDF p. 8 (printed p. 122); A6 |

## Unread and why

- **Quattrone & Tversky (1984) itself**: not one of my sources; A&K give no sample size, r or p for it (A1, A12). Needs its own read.
- **Fowler (2006), "Altruism and Turnout", *J. of Politics***: not my source; the working paper is an earlier, differently titled and broader paper whose voting result is null. The three Greater Good quotations (F2-F4) cannot be checked here. Needs its own read before any Fowler figure is cited.
- **Geys p. 20** (F5, F6): Geys's wording ("only those with different preferences", "eq. 3", "the weight we attach to other's happiness") is in another reader's source.
- **Why the EconWPA file sits under `/exp/removed/`** (F7): unknown; no network use.
- **Dovidio (1984), Parfit (1984), Nozick (1993), Meehl (1977)**: cited by A&K, unread; I report only what A&K say they say.
- **Fowler WP Table 5 and Figure 1**: not used; the text layout of Table 5 is dense, and I used only its prose conclusion ("strong partisans give 14% more than Independents to either of the partisan recipients" was seen but is not needed).
- **Whether the WP's recipients really were registered partisans, and who received the envelopes**: not stated in the paper.

## Found that the first pass missed

1. **Fowler's working paper finds no altruism effect on voting.** Table 7 (Vote column) has no altruism or discriminator term, and the text says "neither altruism nor discrimination in altruism affects voting" (printed p. 20), conjecturing that voting's low cost explains it. The first report's Greater Good quote ("significantly more likely to have voted") is about a different, later paper. The model (alpha B_O > C) is stated in the WP, but the WP does not support it for voting; it supports altruism for contributing, donating, local board attendance and volunteering. [I] The site should not cite "Fowler found altruists vote more" until the 2006 article is read.
2. **Precise Fowler model (fork points)**: `P (B_S + alpha N B_O) > C`; B is the gain *if the preferred outcome occurs*; P is a probability *increment*; one scalar alpha; N is both "relevant population" (for P about 1/N) and "other people affected", so the cancellation needs the two to scale together; in the distributive version others can lose (-B_O) and alpha is group-specific; the proportionality constant of P is dropped (P about 1/N), so the "2C" in the distributive condition and the "C" in the pure rule carry an implicit K = 1; no D term; no tie rule or 1/2; C counts "time, money, and other resources" and, by interpretation, information and skill costs. The WP gives no number for alpha, B_O, N or P.
3. **The WP never discusses correlated choices**; P is a single act's counterfactual probability (F20). The only evidential material in my two sources is Acevedo & Krueger.
4. **The Delta scenario makes voting intentions private** ("improper etiquette in Delta" to share them, printed p. 120) and the illusion still appeared (r = .19); the timing test found the same r for morning and evening voters (.19, .18), so the authors conclude the illusion reflects "perceived diagnosticity", not a belief in causing others to vote (printed p. 125). This supports the first report's [I] (lines 165, 305) that "no one knows" closes the causal channel but not correlated dispositions, **as a belief**; but A&K show nothing about actual correlation among real voters.
5. **A&K call the evidential-vs-causal issue normative**: "The rationality of these two egocentric mechanisms depends on the normative framework invoked" (abstract) and "both ... are potentially rational, but not in the way envisioned by the traditional public-choice model" (printed p. 129). "Illusion" is the dominance/causal framework's label (Quattrone & Tversky assumed "no causal role" and that abstention dominates, printed p. 128). The first report's section 3.4 treats them as evidential theory plus a measured belief; A&K add that the same behaviour is irrational under dominance and potentially rational under the evidential principle (Newcomb's problem).
6. **Size of the measured belief**: mean expected outcome 5.06 if voting vs 4.48 if abstaining on a 9-point scale, F(1,108) = 31.75, d = .49 (printed p. 122). This is a rating of "how likely" on 1-9 scales mixing turnout and victory, not a probability or a count of voters; it is the nearest thing in these sources to a perceived conditional probability shift.
7. **A&K and Fowler/Edlin pull against each other on alpha**: A&K cite Dovidio (1984, unread) that "altruistic motives tend to weaken as electorates become larger and their members more anonymous" (printed p. 129). The cancellation "P about 1/N, benefit about N" needs alpha not to shrink with N. [I] flagged: this is an input the site's model would need a source for.
8. **D-like measure**: A&K's anticipated satisfaction is far higher after voting than after abstaining even after defeat (Study 1: 5.04 vs 2.00; after victory 7.47 vs 2.42; Study 2: 5.12 vs 1.85 and 7.21 vs 2.34; 1-9 scales). Hypothetical self-ratings, not dollars.
9. **A&K footnote 3**: a rule/community orientation "does not require the perception of a differential probability for one's own action" (printed p. 130), bearing on the rule fork (report 3.5) and on altruistic voting without p.
10. **Meehl's p = 10^-8** (A&K printed p. 129; the exponent is a superscript in the PDF; the text file flattens it) is a 1977 rough calculation for determining the Presidency, quoted by A&K, not an estimate the site can reuse.
11. **FEC claims in A&K** (printed p. 116): four FEC-cited elections, all nineteenth-century House seats with under 10,000 voters; A&K's "implication" that no US election since 1900 turned on one vote is theirs, drawn from a web page as of the 2000s; not for use as a fact.
12. **A&K p-value arithmetic**: r(108) = .19 gives one-tailed p = .023 (my computation); the paper prints .027 (A6).
13. **The Fowler WP's URL is under `/exp/removed/`** (F7), and the PDF's text has small internal inconsistencies (F14, F15, F22). If the site cites it, cite it as a 2005 conference working paper, with its N and with the caveat that its voting result is null.
