# B3: Edlin, Gelman & Kaplan (NBER WP 13562) and Kselman, Niou & Wang (2020), re-read from the sources

First report checked: `/home/user/vote/research/frameworks-benefit-cost.md` (cited below as "L<n>" for its line numbers).

## Sources read

| source_id | what it is | size | read in full? |
|---|---|---|---|
| `edlin_nber` | NBER Working Paper 13562, PDF, 22 pages (`https://www.nber.org/papers/w13562.pdf`, which hdr shows is a 301 to `https://www.nber.org/system/files/working_papers/w13562/w13562.pdf`) | text.txt 8,820 words, 815 lines | Yes. Every line of text.txt read (4 chunks). I also viewed PDF pp. 5, 6, 7, 8, 9, 21, 22 as page images to check equations, superscripts and folios. |
| `edlin_nberpage` | NBER landing page `https://www.nber.org/papers/w13562` (HTML) | text.txt 845 words | Yes, whole page. I also read its raw-HTML `<meta>` tags (they are not in text.txt). |
| `edlin_stafforini` | Catalogue page `https://stafforini.com/works/edlin-2007-voting-rational-choice/` (canonical link in raw HTML) | text.txt 355 words | Yes, whole page. |
| `kselman` | Kselman, Niou & Wang, *Electoral Studies* 68 (2020) 102220, PDF, 11 pages (a DukeSpace copy; hdr gives `content-disposition: inline; filename="Measuring closeness.pdf"`, `last-modified: Wed, 09 Aug 2023`; the report's URL is not in hdr) | text.txt 12,059 words (two-column layout, columns interleaved line by line) | Yes. I read the whole paper, references included, in a reading-order re-extraction I made in scratch (12,047 words), and checked every quoted passage against the layout text.txt. PDF p. 5 viewed as an image. **Not read:** the paper's Supporting Information file (a separate download, not in SRC) and the cell values of Tables 1-3 and Figs. 1-4 (the first report uses none of them). |

**Page keys (so the site can cite them).**
- Edlin et al.: PDF p. 1 is the NBER cover, PDF p. 2 the NBER abstract page (no folio). The body starts on PDF p. 3, whose printed folio is "2". From PDF p. 3 on, **printed folio = PDF page - 1** (checked on the images of PDF pp. 5-9 and 21-22). The first report's "p. 4", "p. 5", "p. 6", "Appendix p. 20" are these printed folios of the NBER working-paper version. They are not pages of the journal article (293-314); see entry A5.
- Kselman et al.: pages are numbered 1-11 and **printed page = PDF page**.

**Quote checking.** Every `Quote:` line below was run by me against the entry's own `text.txt` (NFKC, whitespace collapsed) with `SCRATCH/b3work/qcheck.py`; all were found. For `kselman` the layout text interleaves the two columns, so each quote is kept inside one column-line; where the first report's longer string crosses lines I give two Quote lines and say so. In Edlin's text.txt, superscripts are flattened ("10−7" is 10^-7 on the page image) and "∆" is U+2206.

---

## A. Publication facts (edlin_nberpage, edlin_stafforini, edlin_nber front matter)

### A1 NBER landing page: working-paper number, DOI, issue date
- First pass said: not stated beyond the journal citation "from https://www.nber.org/papers/w13562" (L34). The brief asks for these facts.
- Mark: confirmed
- Source: edlin_nberpage; https://www.nber.org/papers/w13562; header block under the title and authors
- Quote: "Working Paper 13562"
- Quote: "DOI 10.3386/w13562"
- Quote: "Issue Date October 2007"
- Note: Raw HTML meta (not in text.txt, so not machine-checkable): `citation_publication_date` and `dcterms.date` are both "2007/10/26", `citation_technical_report_number` "w13562", `citation_pdf_url` the `system/files/working_papers/w13562/w13562.pdf` address. The PDF cover (edlin_nber, PDF p. 1) says "October 2007" and its p. 2 adds "JEL No. H0,K21". Authors: Aaron Edlin (Berkeley, Economics and School of Law, and NBER), Andrew Gelman (Columbia, Statistics and Political Science), Noah Kaplan (Univ. of Houston, Political Science). NBER lists topic "Public Economics" and programs "Law and Economics", "Political Economy".

### A2 NBER landing page: the published version
- First pass said: "Edlin, Gelman & Kaplan (2007), *Rationality and Society* 19(3): 293-314" (L34); "the NBER page lists *Rationality and Society* 19(3): 293-314, **2007** (resolved)" (L307).
- Mark: confirmed
- Source: edlin_nberpage; https://www.nber.org/papers/w13562; block headed "Published Versions"
- Quote: "Rationality and Society, vol 19(3), pages 293-314."
- Quote: "Published Versions"
- Note: The listing gives the year 2007 in the entry "A. Edlin & A. Gelman & N. Kaplan, 2007." (its text includes straight double quotes around the title, so I quote only the journal part). The page gives only volume(issue) and pages; it gives no month or DOI for the journal article. L307's "one Wikipedia extract said 2008" is not checkable from my sources (see Unread).

### A3 Stafforini catalogue page: journal facts
- First pass said: nothing (not cited).
- Mark: confirmed
- Source: edlin_stafforini; https://stafforini.com/works/edlin-2007-voting-rational-choice/; entry under the title
- Quote: "Rationality and Society, vol. 19, no. 3, 2007, pp. 293–314"
- Note: A personal-site catalogue entry (type "article"), not the journal. It gives the same journal, volume, issue, year and pages as the NBER page. Its abstract is the same text as NBER's except that it writes "socially motivated" without the hyphen in contributions (2) and (3) and has HTML-entity quote marks around "social", which suggests it was copied from a publisher or index record rather than from the NBER page [I]. I did not find any other fact on it.

### A4 Revision dates for the NBER paper
- First pass said: nothing. The brief asks for "revision dates".
- Mark: unread
- Source: edlin_nberpage and edlin_nber; none
- Quote: "Issue Date October 2007"
- Note: Neither the landing page nor the PDF gives any revision or version date (searched for "revis", "version", "updated", "draft", "forthcoming" in all three texts). The only date is the issue date, October 2007 (cover and p. 2 of the PDF) / 2007-10-26 (raw HTML meta). The PDF's own metadata (pdfinfo, not page text) has CreationDate Wed Sep 21 20:35:23 2005 UTC and ModDate Wed Oct 24 16:13:27 2007 UTC; I report it as a clue only [I], not as a publication fact.

### A5 Which text this is: NBER working paper, not the journal article
- First pass said: the table row at L34 pairs the journal citation "*Rationality and Society* 19(3): 293-314" with page labels "(p. 4)"; other rows cite "p. 5", "p. 6", "Appendix p. 20", "fn. 3".
- Mark: corrected
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; PDF p. 1 (cover), PDF p. 3 (body title page, printed folio 2)
- Quote: "NBER WORKING PAPER SERIES"
- Quote: "Voting as a rational choice: the effect of preferences regarding the"
- Quote: "Working Paper 13562"
- Correction: "p. 4 / p. 5 / p. 6 / Appendix p. 20, cited alongside Rationality and Society 19(3): 293-314" -> these are printed folios of NBER Working Paper 13562 (PDF pp. 5 / 6 / 7 / 21); the journal's own page numbers for these passages are unknown to me.
- Note: I did not read the journal text, so I cannot say whether its equation numbers, footnotes or wording match. Evidence that the NBER file is an older draft wrapped in a 2007 cover [I]: the body title page (PDF p. 3) carries a different title ("Voting as a rational choice: the effect of preferences regarding the well-being of others") from the NBER and journal title; the reference list marks several items "to appear" (Coate & Colin 2005 AER; Fowler 2005b; Mulligan & Hunter 2002); the PDF CreationDate is 2005 (see A4). The site should cite it as "NBER Working Paper 13562 (October 2007), p. N" and not as the journal.

---

## B. Statements the first report attributes to Edlin, Gelman & Kaplan

### E01 Equation 1: ΔU = pB − c, and what ΔU is
- First pass said: eq. 1 `ΔU = pB − c`; ΔU "relative utility of voting" (L34); eq. 1 again at L191, L314.
- Mark: confirmed
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Sect. 2.1, eq. (1); PDF p. 5 (printed p. 4)
- Quote: "the relative utility of voting, for a particular eligible voter, is"
- Quote: "∆U = pB − c,"
- Note: The paper calls this "the basic rational-choice model of voting and political participation". It is stated for "a particular eligible voter". The first report writes "Δ" (U+0394); the text has "∆" (U+2206); same symbol on the page.

### E02 p defined as the probability a single vote is decisive
- First pass said: "p probability a single vote is decisive" (L34).
- Mark: confirmed
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Sect. 2.1 under eq. (1); PDF p. 5 (printed p. 4)
- Quote: "where p is the probability that a single vote will be decisive, B is the relative benefit associated with your desired candidate winning the election,"
- Quote: "and c is the net cost of voting—that is, the costs, minus the direct benefit of voting (whether or not your candidate wins)."
- Note: The sentence is one sentence of 48 words in the paper (over the 40-word limit), so it is split in two Quote lines; E03 and E05 check B and c separately. See S6 and S7 for what "decisive" means in the paper (a coin-flip tie rule is built into p).

### E03 B defined (the first report's quotation of it is not the paper's wording)
- First pass said: B "relative benefit of the voter's preferred candidate winning" (L34).
- Mark: corrected
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Sect. 2.1 under eq. (1); PDF p. 5 (printed p. 4)
- Quote: "the relative benefit associated with your desired candidate winning the election"
- Quote: "Traditionally, B is understood to refer to direct benefits to"
- Quote: "the voter. This is the assumption of self-interest."
- Correction: B "relative benefit of the voter's preferred candidate winning" -> B "is the relative benefit associated with your desired candidate winning the election" (the meaning is the same; the quoted words in the report are not the paper's).
- Note: The last two Quote lines are one sentence pair split by a page break: the first is at the foot of PDF p. 5, the second at the top of PDF p. 6 (the footnotes sit between them). They say the usual reading of B is the voter's own direct benefit, which the paper then widens in eq. (2).

### E04 Equation 2: B = B_self + αN·B_soc
- First pass said: eq. 2 `B = B_self + αN·B_soc` "(eq. 2, p. 5)"; B_self "the individual's own benefit"; N "the affected population"; α "a discount on others' benefit" (L75, L191).
- Mark: confirmed
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Sect. 2.1, eq. (2); PDF p. 6 (printed p. 5)
- Quote: "B = Bself + αN Bsoc"
- Quote: "individual benefits Bself and social benefits Bsoc for an affected population of size N"
- Quote: "Here, Bsoc is the average benefit per person if the preferred candidate wins, and α is a discounting"
- Note: The full sentence continues "factor to reflect that benefits to others are less important than benefits to self" (see E06). So N multiplies B_soc: the social term is the total over the N people, B_soc being "the average benefit per person". The paper later writes b = B/N = αB_soc + B_self/N (eq. 4, PDF p. 8).

### E05 c defined as net cost: "the costs, minus the direct benefit of voting"
- First pass said: c "net cost, defined as 'the costs, minus the direct benefit of voting' (p. 4)" (L34); the same at L186 and L213.
- Mark: confirmed
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Sect. 2.1 under eq. (1) and footnote 4; PDF p. 5 (printed p. 4)
- Quote: "the costs, minus the direct benefit of voting"
- Quote: "This last term is often written in two parts, separating the direct costs C and direct benefits D, but we shall only need to work with the difference or net cost, c = C − D."
- Note: The paper's full phrase is "the costs, minus the direct benefit of voting (whether or not your candidate wins)". The parenthesis says the direct benefit is outcome-independent. Footnote 4 is the only place the paper names C and D: c = C − D.

### E06 α: selfish if α = 0, social if α > 0; α < 1 expected
- First pass said: "α = 0 is a selfish voter, α > 0 a social one" (L75); "the paper expects α < 1 for most people" (L196).
- Mark: confirmed
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Sect. 2.1, text after eq. (2) and the "Definition"; PDF p. 6 (printed p. 5)
- Quote: "factor to reflect that benefits to others are less important than benefits to self; thus, we would expect α < 1 for most people."
- Quote: "Definition. A voter is selfish if α = 0 and social if α > 0 in (2)."
- Note: The page-5 passage is the only definition of α. No value of α is derived from data; the paper's worked value is 0.1 (E15).

### E07 B_soc is "as perceived by the person making the decision" (the first report's quoted words are not the paper's)
- First pass said: B_soc "the average benefit per person if the preferred candidate wins 'as perceived by the voter'" (L75); "B_soc is 'perceived', not measured (p. 5)" (L196).
- Mark: corrected
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Sect. 2.1, after eq. (2); PDF p. 6 (printed p. 5)
- Quote: "The factor Bsoc represents the benefit to others as perceived by the person making the decision whether to vote;"
- Correction: "as perceived by the voter" -> "as perceived by the person making the decision whether to vote" (italicised in the paper). The substance (perceived, not measured) is confirmed.
- Note: In the Introduction the paper also says "we model the voter's subjective social benefits as proportional to the number of citizens, and independent of the way other citizens vote" (PDF p. 4, printed p. 3; see S3).

### E08 B_soc "is not an averaging of the actual utilities or preferences of the N persons"
- First pass said: B_soc "is not an averaging of the actual utilities or preferences of the N persons" (p. 5) (L75).
- Mark: confirmed
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Sect. 2.1, after eq. (2); PDF p. 6 (printed p. 5)
- Quote: "it is not an averaging of the actual utilities or preferences of the N persons in the population affected by the election."
- Note: The sentence continues with a footnote mark (5) on "election"; the first report's quotation is word-for-word correct as far as it goes.

### E09 Equation 3: p = K/n; K is the "competitiveness"
- First pass said: eq. 3 `p = K/n` (n voters, K "competitiveness") (L191); p = K/n (L270).
- Mark: confirmed
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Sect. 2.1, eq. (3); PDF p. 6 (printed p. 5)
- Quote: "p = K/n,"
- Quote: "where K represents the competitiveness of the election."
- Note: The Assumption just above eq. (3) reads "The probability of a pivotal vote is inversely proportional to the number of voters, n." (PDF p. 6). In the paper n is "persons vote[ing]" (Sect. 2.1 opening) and later n = n_elig·T (eq. 5 text, PDF p. 8).

### E10 K = 10 for close elections ("10/n", Appendix p. 20)
- First pass said: "K = 10 for close elections ('10/n', Appendix p. 20)" (L270).
- Mark: confirmed
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Sect. 2.1 after eq. (3), PDF p. 6 (printed p. 5); Appendix, PDF p. 21 (printed p. 20)
- Quote: "where K represents the competitiveness of the election. As discussed in the Appendix, K = 10 is a reasonable value for close elections, with smaller values in elections that are not expected to be close."
- Quote: "In practice, we see 10/n as a reasonable approximate probability of decisiveness in close elections"
- Note: The Appendix text continues "with lower probabilities for elections not anticipated to be close." My arithmetic [M]: with a uniform forecast density on the vote differential, K = f(0) = 1/(2h) for half-width h, so K = 10 corresponds to h = ±5%. The main-text ±6% example gives K = 8.33 (see M1), and the Appendix's ±10% gives 5 and ±2% gives 25 (M5).

### E11 The ±6% differential gives p ≈ 1/(0.12n)
- First pass said: "±6% differential gives p ≈ 1/(0.12n) (p. 6)" (L270); "with ±6% vote differential, p ≈ 1/(0.12n)" (L139).
- Mark: confirmed
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Sect. 2.1 after Proposition 1; PDF p. 7 (printed p. 6)
- Quote: "the vote differential is expected to be in the range ±6%). The probability that a single vote is decisive is then about 1/(0.12n)."
- Quote: "This assumes that the probability distribution for the vote differential is approximately uniform in the range of uncertainty."
- Note: The paper's set-up is "each candidate is expected to get between 47 and 53 percent of the vote". The "." in the first quote is followed by a footnote mark (6) in the PDF. The second quote is footnote 6, which adds "Using a different distributional form would change the coefficient but not the proportionality to 1/n." The 1/(0.12n) already includes the coin-flip halving; see S7 and M6.

### E12 n = 1 million, B_self = $10,000: expected gain "less than 10 cents"
- First pass said: "n = 1 million: self-interest gain 'less than 10 cents'" (L270); "with n = 1 million and a self-benefit worth $10,000 the expected gain is 'less than 10 cents' ([M] check: p = 8.3×10⁻⁶, pB = $0.083)" (L139).
- Mark: confirmed
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Sect. 2.1 after Proposition 1; PDF p. 7 (printed p. 6)
- Quote: "even if the outcome of the election is worth $10,000 to a particular voter, the expected utility gain is less than 10 cents."
- Quote: "So for a selfish voter, the expected utility gain from potentially swinging the outcome of the election is about Bself /(0.12n)"
- Note: Recomputed in M1 and M2. The paper's "$10,000" is "the outcome of the election" to the voter, i.e. B_self itself, not pB (see S6).

### E13 The $250 figure (Sect. 2.1, Proposition 2 example)
- First pass said: "B_soc = $10 per citizen, ... n/N = 1/3 → expected social value of the vote ≈ $250 (p. 6)" (L191); "$250 expected value" (L270).
- Mark: confirmed
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Sect. 2.1 after Proposition 2; PDF p. 7 (printed p. 6)
- Quote: "Further suppose that 1/3 of the population are voters; that is, n/N = 1/3."
- Quote: "then you are effectively giving them a total of $10N/(0.12n) = $10N/(0.12(N/3)) = $250 in expected value by voting."
- Note: Recomputed in M3. The $250 is computed with **no α**: it is $10N/(0.12n), i.e. B_soc times N times p. See E15 for the α.

### E14 The $25 threshold: α = 0.1 gives c < $25
- First pass said: "voting worthwhile if c < $25 (p. 6)" (L191); "voting pays if c < $25" (L270).
- Mark: confirmed
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Sect. 2.1 after Proposition 2; PDF p. 7 (printed p. 6)
- Quote: "if your discounting factor for benefits to others is α = 0.1, then your net utility gain from voting is positive as long as your cost of voting c is less than $25."
- Note: Recomputed in M4: 0.1 × $250 = $25.

### E15 The first report ties $250 to α = 0.1 and sets "$250 vs c < $25"; the paper's $250 is undiscounted
- First pass said: "worked example: B_soc = $10 per citizen, α = 0.1, n/N = 1/3 → expected social value of the vote ≈ $250 and voting worthwhile if c < $25 (p. 6)" (L191); "with α = 0.1 and $10 per person it fails in the Edlin et al. example ($250 vs c < $25)" (L196); "with social preferences, $250 expected value, so voting pays if c < $25" (L270).
- Mark: corrected
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Sect. 2.1 after Proposition 2; PDF p. 7 (printed p. 6)
- Quote: "then you are effectively giving them a total of $10N/(0.12n) = $10N/(0.12(N/3)) = $250 in expected value by voting."
- Quote: "if your discounting factor for benefits to others is α = 0.1, then your net utility gain from voting is positive as long as your cost of voting c is less than $25."
- Correction: "α = 0.1 ... ≈ $250" and "$250 vs c < $25" -> $250 is the expected social value with no discount (α = 1 implicit); the α = 0.1 value is $25 (= 0.1 × $250), and that is what c is compared with. Voting pays at α = 0.1 if c < $25, not "$250 vs c < $25"; the paper's "$250 ... equivalent in some ways to giving $250 to a national charity" is the undiscounted gift.
- Note: Both numbers are in the paper; only the pairing in the report is off. The paper also says "In many elections with issues such as national security, global climate change, and nuclear weapons proliferation, a rational citizen could think that the superiority of his or her candidate might deliver an expected value per citizen far in excess of $10" (same page); B_soc = $10 is a hypothetical ("consider the same hypothetical election as above"), see E21.

### E16 Footnote 3: "10⁻⁷ or 10⁻⁸ are more reasonable values for U.S. Presidential elections"
- First pass said: "fn. 3: '10⁻⁷ or 10⁻⁸ are more reasonable values for U.S. Presidential elections'" (L270).
- Mark: confirmed
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; footnote 3 (attached to the last sentence of the opening of Sect. 2.1); PDF p. 5 (printed p. 4)
- Quote: "In fact, 10−7 or 10−8 are more reasonable values for U.S. Presidential elections"
- Quote: "The probability of a decisive vote is low but is clearly distinct from zero, if multiplied by a benefit term that is proportional to the size of the electorate."
- Note: Footnote 3 gives the figure as the value in Gelman, King & Boscardin (1998) ("(Gelman, King, and Boscardin, 1998) with much higher probabilities for many Congressional races (Mulligan and Hunter, 2002)"); it is not an estimate by Edlin et al. In the PDF image the exponents are superscripts (10^-7, 10^-8). The same footnote rebuts Dowding (2005), whom it says believed p "is as low as 10−90".

### E17 The abstract's two sentences
- First pass said: abstract: "For voters with 'social' preferences, the expected utility of voting is approximately independent of the size of the electorate", and "a feedback mechanism keeps turnout at a reasonable level under a wide range of conditions." (L191)
- Mark: confirmed
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; abstract, PDF p. 2 (NBER abstract page, no folio) and PDF p. 3 (body abstract, printed folio 2); also edlin_nberpage (same text)
- Quote: "the expected utility of voting is approximately independent of the size of the electorate, suggesting that rational voter turnouts can be substantial even in large elections."
- Quote: "Less important elections are predicted to have lower turnout, but a feedback mechanism keeps turnout at a reasonable level under a wide range of conditions."
- Note: PDF p. 2 writes "social" with straight quotes; PDF p. 3 with curly quotes. The first report's single quotes are its own, which is why I quote from "the expected utility" onward. The abstract goes on to list three "main contributions" ((1) social preferences dominate; (2) feedback "stabilizes turnout at reasonable levels (e.g., 50% of the electorate)"; (3) a link to survey findings on socially-motivated vote choice).

### E18 "gives no empirical estimate of c": the words are not the paper's; the substance holds
- First pass said: The paper "gives no empirical estimate of c" (L191, in quotation marks).
- Mark: corrected
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Sect. 3, opening, PDF p. 11 (printed p. 10); Sect. 5.4, PDF p. 17 (printed p. 16)
- Quote: "Though a rigorous empirical test of our claim is beyond the scope of the current project, we do provide some suggestive evidence."
- Quote: "We hope that our model inspires researchers to do empirical tests of its implications and estimates of its parameters."
- Correction: the string "gives no empirical estimate of c" does not occur in the paper -> the paper estimates no parameter (not c, not α, not B_soc): it assumes a noncentral-Cauchy distribution for c/b (E19) and invites others to estimate "its parameters".
- Note: The only numbers for c are hypothetical thresholds (c < $25, E14) and the share of people with c < 0 implied by the assumed distribution (S5, M7).

### E19 The turnout simulations (K = 10, n_elig/N = 1/3, noncentral Cauchy c/b, Fig. 1); "to illustrate" is not the paper's phrase
- First pass said: "Simulations of turnout use K = 10, n_elig/N = 1/3 and an assumed noncentral-Cauchy c/b distribution (Fig. 1), 'to illustrate', not to estimate." (L270)
- Mark: corrected
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Sect. 2.2, PDF pp. 9-10 (printed pp. 8-9), footnote 9 (PDF p. 9), Fig. 1 caption (PDF p. 10); Sect. 5.3, PDF p. 16 (printed p. 15)
- Quote: "In an election anticipated to be close, it is reasonable to set K = 10 (see the Appendix)."
- Quote: "with nelig /N , the fraction of the population who are eligible voters, set to 1/3."
- Quote: "We use the noncentral Cauchy distribution (that is, the noncentral t with 1 degree of freedom)"
- Quote: "Our key point is not that the curves in Figure 1, for example, exactly fit turnout behavior in specific U.S. elections, but that the model is consistent with such behavior."
- Correction: the quoted words "to illustrate" -> not in the paper in this context (the only "to illustrate" in the paper is about Aldrich, PDF p. 16, unrelated). The inputs (K = 10, n_elig/N = 1/3, noncentral Cauchy, Fig. 1) are confirmed. The paper's own framing is the Sect. 5.3 quote above.
- Note: Fig. 1 plots equilibrium turnout against election "importance" s for δ = 0.5, 1.0, 1.5. Its caption says "the equilibrium turnout remains in a plausible range (between 20% and 80%), even as the importance of the election varies by two orders of magnitude." I have not re-derived the curves.

### E20 The B inputs ($10,000, $10, α = 0.1) are "hypothetical" round numbers; "suggestive" is the paper's word for its evidence, not for these
- First pass said: "Edlin et al. set it by assumption with stated round numbers ($10,000 own stake; $10 per citizen; α = 0.1), which they call suggestive." (L279)
- Mark: corrected
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Sect. 2.1, PDF p. 7 (printed p. 6) and Sect. 3, PDF p. 11 (printed p. 10)
- Quote: "For example, consider the same hypothetical election as above, in which the n voters represent a jurisdiction with population N ."
- Quote: "Though a rigorous empirical test of our claim is beyond the scope of the current project, we do provide some suggestive evidence."
- Correction: "which they call suggestive" -> the paper presents the three inputs as a hypothetical example; "suggestive" is its description of the supporting evidence in Sects. 3-4 (political participation, vote choice). "Set by assumption with stated round numbers" is right.
- Note: Another word for the same status is in the Fig. 1 caption ("hypothetical population", PDF p. 10).

### E21 L44: the D term is added after pB and is not multiplied by p (as read for Edlin et al.)
- First pass said: "The structure probability of decisiveness × benefit differential − cost is written by SEP, Geys, Edlin et al. and Dowding, and the D term is added after it and is not multiplied by p." (L44); and, for the isolation setup, "Edlin et al. fold it into c ('the costs, minus the direct benefit of voting', so c can be negative)" (L186).
- Mark: confirmed
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Sect. 2.1 (PDF p. 5, printed p. 4, with footnote 4), Proposition 1 (PDF p. 6, printed p. 5), Sect. 2.2 (PDF p. 9, printed p. 8), Sect. 3.4 (PDF p. 13, printed p. 12)
- Quote: "voting in large elections only makes sense for selfish voters if they enjoy the act of voting itself (that is, if c < 0 in (1))."
- Quote: "In general, b should be positive, but c can be either positive or negative."
- Quote: "The natural way to empirically distinguish our social preference, Bsoc , from civic duty is that Bsoc is multiplied by Pr(election is tied), and civic duty is not."
- Note: In Edlin et al. D is not a separate term. It sits inside c as c = C − D (footnote 4), is not multiplied by p, and is not given a separate symbol after the first mention. The third quote says civic duty is a direct (outcome-independent) benefit that is not multiplied by the probability of a tie.

### E22 "p ∝ 1/n and the social part of B ∝ N, so their product is roughly flat in electorate size"
- First pass said: "p ∝ 1/n and the social part of B ∝ N, so (as Edlin et al. show) their product is roughly flat in electorate size" (L195).
- Mark: confirmed
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Sect. 2.1 opening, PDF p. 5 (printed p. 4)
- Quote: "suppose n persons vote in an election that affects a jurisdiction with a population of N ; then the benefit of having the preferred candidate win the election is proportional to N ."
- Quote: "and thus the expected utility of voting is proportional to N/n, which is approximately independent of the size of the electorate."
- Note: Precisely, what the paper shows is that the expected benefit is proportional to **N/n**; it is independent of "the size of the electorate" only if the ratio N/n (turnout as a share of the affected population) is held fixed. The worked example fixes n/N = 1/3; Sect. 2.2 argues the ratio settles by feedback (S5).

### E23 L303: "Edlin et al. ... count others"
- First pass said: "Whose welfare is in B (3.7). Edlin et al. and Barnett count others" (L303); "the voter, **plus** others at weight α" (L75).
- Mark: confirmed
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Sect. 2.1, PDF pp. 6-7 (printed pp. 5-6)
- Quote: "If you, as a potential voter, think that the net benefit to your fellow citizens of candidate A winning the election is the equivalent of Bsoc = $10 per citizen"
- Quote: "individual benefits Bself and social benefits Bsoc for an affected population of size N"
- Note: Detail in S3.

### E24 L276: a quotation attributed to Edlin et al. at SEP sec. 1.1
- First pass said: SEP: expected benefit "worth far less than a millionth of a penny"; "a 1 in 10 million chance of breaking a tie" in close states (Edlin et al.). (L276)
- Mark: unread
- Source: edlin_nber; (SEP is not one of my sources); footnote 3, PDF p. 5 (printed p. 4)
- Quote: "In fact, 10−7 or 10−8 are more reasonable values for U.S. Presidential elections"
- Note: I cannot check what SEP says. The phrase "1 in 10 million" does not occur in the Edlin et al. working paper (searched "million": only "n = 1 million" and "millions of people"). The nearest statement in the paper is the footnote 3 quotation above, which it attributes to Gelman, King & Boscardin (1998). L288 and L139 also mention "Gelman, Silver & Edlin" (a different paper, 2008) which is outside my batch.

---

## C. Recomputation of every [M] number the first report gives for Edlin et al. (python3 -I, script `SCRATCH/b3work/recompute.py`)

### M1 p at n = 1,000,000 with a ±6% differential
- First pass said: "[M] check: p = 8.3×10⁻⁶" (L139)
- Mark: confirmed
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Sect. 2.1; PDF p. 7 (printed p. 6)
- Quote: "the vote differential is expected to be in the range ±6%). The probability that a single vote is decisive is then about 1/(0.12n)."
- Note: Inputs from the paper: range ±6% means a range of width 0.12; n = 1,000,000. Calculation: p = 1/(0.12 × 1,000,000) = 1/120,000 = 8.333×10⁻⁶. Matches the first report's 8.3×10⁻⁶. (With the paper's K = 10 in place of 1/0.12: p = 10/1,000,000 = 1.0×10⁻⁵.)

### M2 pB with B = $10,000
- First pass said: "pB = $0.083" and the paper's "less than 10 cents" (L139)
- Mark: confirmed
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Sect. 2.1; PDF p. 7 (printed p. 6)
- Quote: "even if the outcome of the election is worth $10,000 to a particular voter, the expected utility gain is less than 10 cents."
- Note: Calculation: pB = $10,000 × 8.333×10⁻⁶ = $10,000/120,000 = $0.08333 = 8.3 cents, which is less than 10 cents, as the paper says. With K = 10 instead: $10,000 × 10/1,000,000 = $0.10 exactly (not "less than"), so the paper's wording is for the ±6% case.

### M3 The $250
- First pass said: "$250 expected value" for B_soc = $10, n/N = 1/3 (L191, L270)
- Mark: confirmed
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Sect. 2.1 after Proposition 2; PDF p. 7 (printed p. 6)
- Quote: "then you are effectively giving them a total of $10N/(0.12n) = $10N/(0.12(N/3)) = $250 in expected value by voting."
- Note: Calculation: $10·N/(0.12·n) with n = N/3 gives $10 × 3/0.12 = $30/0.12 = $250. N cancels (tried N = 30,000; 3,000,000; 300,000,000: all $250). The paper's formula is p × (N × B_soc) with p = 1/(0.12n) and **no α**.

### M4 The $25
- First pass said: "voting worthwhile if c < $25" (L191)
- Mark: confirmed
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Sect. 2.1; PDF p. 7 (printed p. 6)
- Quote: "if your discounting factor for benefits to others is α = 0.1, then your net utility gain from voting is positive as long as your cost of voting c is less than $25."
- Note: Calculation: ΔU = pB − c with B = αN·B_soc (B_self ignored): pB = 0.1 × $250 = $25, so ΔU > 0 iff c < $25. If B_self = $10,000 is added (N = 300,000,000, n = 100,000,000) the self term is $10,000/(0.12 × 10⁸) = $0.0008, so pB = $25.0008: the self term does not change the threshold at the paper's precision.

### M5 Arithmetic the first report did not give but the paper's other numbers allow
- First pass said: nothing (K = 10 and "10/n" are quoted, L270).
- Mark: confirmed
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Appendix; PDF p. 21 (printed p. 20)
- Quote: "then the probability is about 1/(0.2n) = 5/n that a single added vote could create or break a tie."
- Quote: "In practice, we see 10/n as a reasonable approximate probability of decisiveness in close elections"
- Note: Calculation with a uniform density of half-width h on the differential: f(0) = 1/(2h). h = 0.10 gives 5/n (the paper's "1/(0.2n) = 5/n"); h = 0.02 gives 25/n (the paper's "1/(0.04n) = 25/n"); h = 0.06 gives 8.33/n; h = 0.05 gives exactly 10/n. So the paper's K = 10 sits between its ±10% and ±2% examples and equals the ±5% case [M]; it is a rounded judgement ("we see 10/n as a reasonable approximate probability").

### M6 Does 1/(0.12n) already contain the coin-flip half? (reader's check, not in the first report)
- First pass said: nothing (the report writes p = ½[P(tie) + P(one short)] in its own algebra, L314).
- Mark: confirmed
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Appendix and footnote 12; PDF p. 21 (printed p. 20)
- Quote: "The probability of a decisive vote is then half the probability that a single vote can make or break an exact tie, or f (0)/n."
- Quote: "The assumption here is that an exact tie vote will be decided by a coin flip."
- Note: Check by exact binomial arithmetic (script `SCRATCH/b3work/tiecheck.py`): other voters' votes X ~ Binomial(n−1, s) with s uniform on [0.47, 0.53] (differential uniform on ±6%); one vote for the preferred candidate changes the winning probability by 1 (breaking a tie), ½ (creating a tie), or 0, with exact ties decided by a coin flip. The expected change is 1.6666×10⁻³ at n = 5,000 versus 1/(0.12n) = 1.6667×10⁻³ (ratio 1.0000); at n = 1,000 the ratio is 0.94 (edge effect). So 1/(0.12n) = f(0)/n **already includes the ½**; "make or break an exact tie" would be twice that, 2f(0)/n = 2/(0.12n). The Appendix's own example then calls f(0)/n = 5/n "the probability ... that a single added vote could create or break a tie", which by its preceding sentence is the halved quantity; the wording there is loose [I].

### M7 Section 2.2's noncentrality-parameter percentages (not in the first report; they bear on c < 0)
- First pass said: nothing (the report does not use these numbers).
- Mark: confirmed (the passage is quoted; but it is internally inconsistent, see Note)
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Sect. 2.2, PDF p. 10 (printed p. 9)
- Quote: "If δ = 1, then Pr(c > 0) = 0.16, which means that 60% of the eligible voters would vote, even in an election with no importance."
- Quote: "We consider values of δ from 0.5 (in which case 31% of the people would vote under any circumstances) to 1.5 (6.7% would always vote)."
- Note: [M, python3 -I] The first report is not affected; this is a flaw in the paper's text. Footnote 9 defines the distribution as a normal with mean δ and sd 1 divided by a positive scale, so the share with c < 0 is Φ(−δ): Φ(−0.5) = 0.3085 (the paper: 31%), Φ(−1.0) = 0.1587 (the paper writes 0.16, but as "Pr(c > 0)", and then "60%"), Φ(−1.5) = 0.0668 (the paper: 6.7%). So the 0.16 is Pr(c < 0), the sign in "Pr(c > 0)" is reversed, and the "60%" does not follow (16% would). If the site quotes these shares it should use Φ(−δ) and flag the text. The journal version may have fixed this; not read.

---

## D. Kselman, Niou & Wang (2020), *Electoral Studies* 68: 102220 (the first report's only statements: L106)

### K01 Identity and citation
- First pass said: "Kselman, Niou & Wang (2020, *Electoral Studies* 68: 102220)" (L106)
- Mark: confirmed
- Source: kselman; DukeSpace copy (URL as in the report: https://dukespace.lib.duke.edu/server/api/core/bitstreams/672a2c09-26d4-4f6b-923a-7b2da6ccdd60/content); PDF p. 1 (printed p. 1)
- Quote: "Electoral Studies 68 (2020) 102220"
- Quote: "Measuring ‘closeness’ in 3-candidate elections: Methodology and an"
- Quote: "Received 17 October 2019; Received in revised form 21 August 2020; Accepted 30 August 2020"
- Quote: "Available online 15 October 2020"
- Note: Title continues "application to strategic voting". Authors Daniel Kselman (IE University, Spain), Emerson Niou (Duke), Austin Horng-En Wang (UNLV). This is a methods-and-application paper on measuring closeness in three-candidate plurality elections and testing strategic voting in the 2010 British Election Study (robustness check: 1988 Canadian National Election Study). It has no cost-of-voting term, no turnout model and no estimate of the size of a pivot probability.

### K02 "pivotal in creating or breaking 1st-place ties" (the quotation marks are the first report's, not the paper's)
- First pass said: voters are "pivotal in creating or breaking 1st-place ties" between two candidates (L106).
- Mark: confirmed
- Source: kselman; as K01; Sect. 1 (PDF p. 1, printed p. 1) and Sect. 1.1 (PDF p. 2, printed p. 2)
- Quote: "are ‘pivotal’ in creating or breaking 1st-place ties between candidates"
- Quote: "‘pivotal’ for creating or breaking a 1st-place tie between two candidates."
- Note: The paper puts only the word ‘pivotal’ in single quotation marks, so the first report's string "pivotal in creating or breaking 1st-place ties" is not a verbatim substring (the closing ’ after "pivotal" is missing); the wording and meaning are the paper's. Sect. 1 says "between candidates"; the "two candidates" version is in Sect. 1.1 (p. 2), where it describes how the explicit measures of other authors are built (by integrating a belief density over the outcomes in which a voter is pivotal), and adds "Although very small, these values are greater than ‘0’."

### K03 The three-candidate condition (eq. 4)
- First pass said: three-candidate condition (as extracted) `p23·(U2 − U3) > 2·p12·(U1 − U2) > p13·(U1 − U3)` (L106)
- Mark: confirmed
- Source: kselman; as K01; Sect. 3, eq. (4), with eq. (5) below it; PDF p. 5 (printed p. 5); footnote 14 same page
- Quote: "p23 ⋅(U2 − U3 ) > 2p12 ⋅(U1 − U2 ) > p13 ⋅(U1 − U3 )"
- Quote: "E2 > E1 if and only if"
- Quote: "σ p23 − 2(1 − σ)p12 − p13 > 0."
- Quote: "From past formal research (Black, 1978; Hoffman,"
- Quote: "following condition for strategically choosing their second-preference14:"
- Note: The report's string is the printed equation (4) (it adds a "·" after the 2; the paper has "2p12"), and its "(as extracted)" was apt. **The printed (4) shows ">" twice, but eq. (5) only follows if the second ">" is "+".** [I] Algebra: with the paper's normalisation U1 = 1, U3 = 0, U2 = σ (so U2−U3 = σ, U1−U2 = 1−σ, U1−U3 = 1), "p23(U2−U3) > 2p12(U1−U2) + p13(U1−U3)" becomes σp23 > 2(1−σ)p12 + p13, i.e. eq. (5) "σ p23 − 2(1 − σ)p12 − p13 > 0". A literal chain "a > b > c" would instead say two separate things and cannot give (5). The text after (4) also speaks of "the left-hand side" and "the right-hand side" as two sides: "When the left-hand side is greater than the right-hand side, the". I viewed the printed page (PDF p. 5): it shows ">" in both places. The paper says it "reproduce[s]" the condition from Black 1978, Hoffman 1982, Fisher 2004 and Kselman & Niou 2010, none of which I have. The factor 2 on p12 is not explained in this paper (see N14). Meaning of the symbols: p_jk is the closeness index between the voter's jth and kth preferences (p12, p13, p23); U_j is "a voter's utility for having their jth preference win the election", with U1 ≥ U2 ≥ U3; E_j the expected utility of choosing candidate j. The condition is for voting for the 2nd preference rather than the 1st in a three-candidate plurality election. Footnote 14 (attached to the sentence introducing (4), though it speaks of inequality (5)) states an assumption that adjacent probabilities in comparable outcome spaces are equal, citing McKelvey and Ordeshook (1972, p. 51); the quote is in N7.

### K04 Strategic voting is "driven almost entirely by viability comparisons involving one's least-preferred candidate"
- First pass said: they find strategic voting "driven almost entirely by viability comparisons involving one's least-preferred candidate" (L106).
- Mark: confirmed
- Source: kselman; as K01; Sect. 1, PDF p. 2 (printed p. 2); repeated in Sect. 4, PDF p. 8, and Sect. 5, PDF p. 9
- Quote: "candidates, our results suggest that strategic voting is driven almost"
- Quote: "entirely by viability comparisons involving one’s least-preferred"
- Quote: "only on viability comparisons which include their least-preferred"
- Quote: "to cast a strategic vote is driven by viability comparisons involving one’s"
- Quote: "least-preferred candidate, and not by comparing one’s top two prefer­"
- Note: The Sect. 1 sentence is one sentence, "...our results suggest that strategic voting is driven almost entirely by viability comparisons involving one’s least-preferred candidate", but in the two-column text.txt the first half ends one line and the second half starts the next with the other column's text between them (and a soft hyphen in "candi­date"), so a search for the whole string will fail; hence the two Quote lines. The Sect. 5 sentence (PDF p. 9, the same way split over two lines) reads "The choice to cast a strategic vote is driven by viability comparisons involving one’s least-preferred candidate, and not by comparing one’s top two preferences." Hedge: the Introduction says "our results suggest"; the finding is an empirical result for British (2010 BES) and Canadian (1988 CNES) three-party contests and is about choosing the 2nd preference over the 1st, not about turnout. On PDF p. 8 the authors read the near-zero effect of p12 as a heuristic short-cut: voters simplify the calculus in (5) by looking only at viability comparisons that include their least-preferred candidate.

### K05 Extending to more candidates "will require careful proofs"
- First pass said: The paper says extending to more candidates "will require careful proofs" (L106).
- Mark: confirmed
- Source: kselman; as K01; Sect. 3.1 (measurement and operationalization), PDF p. 5 (printed p. 5); see also Sect. 5, PDF p. 9
- Quote: "approach to measuring closeness can be extended to party systems with"
- Quote: "more than three parties. However, these extensions are not trivial, and"
- Quote: "will require careful proofs which are beyond the scope of the current"
- Note: The sentence (continuing on the next line with "paper.") says both the Calculus of Voting and the paper's axiomatic closeness approach "can be extended to party systems with more than three parties", but that the extensions "are not trivial". Sect. 5 (PDF p. 9) adds: "paper has yet derived the full conditions for strategic voting in" 4-candidate elections, "i.e. the equivalent to (5) above" (quoted in N15).

---

## E. Fill: what Edlin, Gelman & Kaplan's paper says, for the model (NBER WP version, October 2007; printed folios given, PDF page = folio + 1)

### S1 The model in the paper's own summary
- First pass said: eq. 1 to 3 and the $250 / $25 example are summarised at L191; the argument "p ∝ 1/n, B_soc part ∝ N" at L195.
- Mark: confirmed
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Sect. 1 (PDF p. 3, printed p. 2) and Sect. 2.1 (PDF p. 5, printed p. 4)
- Quote: "In a large election, the probability that a vote is decisive is small, but the social benefits at stake in the election is large,"
- Quote: "and so the expected utility benefit of voting to an individual with social preferences can be significant."
- Quote: "What is perhaps surprising is that the expected value of the social benefit does not approach zero or even diminish as the number of voters grows large."
- Note: Structure: a rational voter with ΔU = pB − c (eq. 1); B = B_self + αN·B_soc (eq. 2); p = K/n (eq. 3). Proposition 1: for a selfish voter (α = 0) "the expected benefits from being pivotal and swinging the election vanish as n grows", so voting in a large election pays only if c < 0. Proposition 2: for a social voter (α > 0) "the expected benefits ... have a nonzero asymptote proportional to αBsoc". Section 2.2 then lets turnout adjust (S5). Sections 3-4 give "suggestive evidence" (small campaign contributions, falling poll response rates, higher turnout in large and close elections, strategic voting, issue voting, surveys); Sect. 5 discusses implications (people should vote for the social good), psychological explanations, generalisations to groups and "empirical tests".

### S2 What each symbol means, as the paper defines it
- First pass said: partial definitions at L34, L75, L191.
- Mark: confirmed
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Sect. 2.1-2.2, PDF pp. 5-8 (printed pp. 4-7)
- Quote: "where p is the probability that a single vote will be decisive, B is the relative benefit associated with your desired candidate winning the election,"
- Quote: "and c is the net cost of voting—that is, the costs, minus the direct benefit of voting (whether or not your candidate wins)."
- Quote: "Here, Bsoc is the average benefit per person if the preferred candidate wins, and α is a discounting"
- Quote: "where K represents the competitiveness of the election."
- Quote: "Finally, we define nelig as the number of eligible voters and T as the proportional voter turnout, so"
- Note (the paper's definitions, in its words or very close):
  - **ΔU**: "the relative utility of voting, for a particular eligible voter".
  - **p**: "the probability that a single vote will be decisive"; modelled as p = K/n (eq. 3); the Assumption: "The probability of a pivotal vote is inversely proportional to the number of voters, n."
  - **B**: "the relative benefit associated with your desired candidate winning the election"; B = B_self + αN·B_soc.
  - **B_self**: "individual benefits"; **B_soc**: "the average benefit per person if the preferred candidate wins", "as perceived by the person making the decision whether to vote".
  - **α**: "a discounting factor to reflect that benefits to others are less important than benefits to self"; "we would expect α < 1 for most people".
  - **N**: "a jurisdiction with a population of N" / "an affected population of size N".
  - **n**: "n persons vote in an election" (the number of voters); with n_elig the number of eligible voters and T turnout, n = n_elig·T.
  - **K**: "the competitiveness of the election"; "K = 10 is a reasonable value for close elections, with smaller values in elections that are not expected to be close".
  - **c**: "the net cost of voting—that is, the costs, minus the direct benefit of voting (whether or not your candidate wins)"; c = C − D (fn. 4); "c can be either positive or negative".
  - **b = B/N**: "the expected benefit, per affected person in the population, of changing the election outcome", b = αB_soc + B_self/N (eq. 4); eq. 5: ΔU = (KN/n)b − c = (KN/(n_elig T))b − c; eq. 6: vote iff c/b < KN/(n_elig T).

### S3 Whose welfare counts in B (a fork point)
- First pass said: "the voter, **plus** others at weight α" (L75); "Whose welfare is in B (3.7). Edlin et al. and Barnett count others" (L303); the group version is not mentioned.
- Mark: confirmed
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Sect. 1 (PDF p. 4, printed p. 3); Sect. 2.1 (PDF pp. 6-8, printed pp. 5-7); Sect. 5.3 (PDF p. 17, printed p. 16); Sect. 5.4 (PDF p. 17, printed p. 16)
- Quote: "Instead, we model the voter’s subjective social benefits as proportional to the number of citizens, and independent of the way other citizens vote."
- Quote: "or at the least the good of a large affinity group, but not for direct individual gain."
- Quote: "The social-benefit model (applied now to groups rather than all persons in the population)"
- Quote: "California voters have two different α’s—a high one for benefits to Californians and a lower one for benefits to other U.S. citizens."
- Quote: "Hence a shareholder in a privately held company with four shareholders might vote for his own interest."
- Note: In eq. 2 the voter's own benefit B_self counts once; each of the N affected persons counts at weight α. "Others" are "fellow citizens" in "the population affected by the election"; the paper does not say whether the voter is inside N. The Intro's "the voter's subjective social benefits ... independent of the way other citizens vote" (and footnote 1: the two groups of voters "do not represent competing interests but rather competing perspectives about what is best for the country") sets B_soc as the voter's own perception, not a poll of others. Sect. 5.3 generalises to groups ("applied now to groups rather than all persons in the population"); Sect. 5.4 allows different α's for different groups. The paper's selfish/social test is α = 0 versus α > 0 (E06).

### S4 How p depends on electorate size
- First pass said: "p ∝ 1/n" (L195); "p = K/n" (L270); fn. 3, Appendix (L270).
- Mark: confirmed
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Sect. 2.1 "Assumption" (PDF p. 6, printed p. 5); Appendix (PDF pp. 21-22, printed pp. 20-21)
- Quote: "(This assumption is reasonable because the closeness of elections, in percentage terms, does not depend strongly on the number of voters, n."
- Quote: "Hence the probability that an individual vote is decisive—which essentially is the probability that an election is exactly tied—is of order 1/n."
- Quote: "but this model once again implies elections that are much closer than actually occur"
- Note: The reason for 1/n is that the forecast uncertainty about the vote **differential** (a proportion) does not shrink with n, so the density of an exact tie in votes is f(0)/n. The paper contrasts this with "Under a coin-flipping model of voting, the probability of decisiveness is proportional to 1/√n", which it rejects because it "implies elections that are much closer than actually occur" (Appendix, PDF p. 22, printed p. 21), and with game-theoretic models that "imply that large elections will be extremely close". It says p "is of order 1/n" but does not give a formula for p at a given n beyond f(0)/n; its numeric values are K = 10 for close elections and the fn. 3 range for U.S. presidential elections (E16). The Section 3.3 prediction: small elections can have a visible self-interest term (the 1/N B_self term), otherwise "election size will not substantially influence turnout rates" (PDF p. 5, printed p. 4: "Finally, our model predicts that holding constant these other factors, election size will not substantially influence turnout rates,").

### S5 The "feedback mechanism" for turnout
- First pass said: abstract quotation only: "a feedback mechanism keeps turnout at a reasonable level under a wide range of conditions" (L191).
- Mark: confirmed
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Sect. 2.2, PDF pp. 8-10 (printed pp. 7-9), eqs. (5)-(7), footnote 8, Fig. 1
- Quote: "If turnout becomes very low, then n decreases, and thus the factor N/n increases, and it becomes more reasonable to vote."
- Quote: "The equilibrium point of turnout is defined where the probability of voting in (6) is consistent with the turnout rate T in that expression; thus,"
- Quote: "our feedback mechanism works because, as turnout declines, the probability of a vote being decisive increases, causing the expected benefit of voting to increase."
- Quote: "Because of the feedback mechanism (when turnout decreases, the probability of a decisive vote increases), the equilibrium turnout remains in a plausible range"
- Note: Mechanism: from ΔU = (K/n)B − c, a person votes iff c/b < KN/(n_elig T) (eq. 6), so the fraction who find it worth voting falls as T rises; T_equilib = Pr(c/b < K·(N/n_elig)·(1/T_equilib)) (eq. 7), solved numerically for an assumed distribution of c/b (noncentral Cauchy with noncentrality δ, which sets the share with c < 0, and scale s, "the average importance of the election"). Fig. 1: δ = 0.5, 1.0, 1.5; K = 10; n_elig/N = 1/3; the caption's claim is turnout between 20% and 80% as importance s varies by two orders of magnitude. Footnote 8 says the same feedback exists for the instrumental (selfish) model "but there the expected utility of voting is so low that voter turnout will stabilize at less then 1% in large elections (Ledyard, 1984)", and says Bendor, Diermeier & Ting (2003) and Fowler (2005b) differ from the paper by "relying on “satisficing” rather than utility maximization". The feedback is an equilibrium condition in the aggregate turnout T; the paper does not ask whether one's own vote changes others' (see S8).

### S6 Fork: is B the gain if decisive, or the expected gain pB?
- First pass said: Two readings (a) B = U(outcome you vote for) − U(alternative), the gain **if decisive**, which "the sources call B"; (b) E[U|vote] − E[U|abstain] = pB (L98-101); "B is a perceived utility difference between two outcomes" (L314).
- Mark: confirmed
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Sect. 2.1 (PDF pp. 5, 7; printed pp. 4, 6); Sect. 2.2 (PDF p. 8, printed p. 7)
- Quote: "B is the relative benefit associated with your desired candidate winning the election"
- Quote: "So for a selfish voter, the expected utility gain from potentially swinging the outcome of the election is about Bself /(0.12n)"
- Quote: "For a social voter, the expected benefits of being pivotal and swinging the election have a nonzero asymptote proportional to αBsoc , which does not vanish as n increases."
- Quote: "It is useful to express this in terms of b = B/N , the expected benefit, per affected person in the population, of changing the election outcome,"
- Note: In this paper B is reading (a): the benefit "associated with your desired candidate winning", and the "expected" gain is **pB** (the paper says "expected utility gain ... is about Bself /(0.12n)", i.e. p·B_self, and "even if the outcome of the election is worth $10,000 to a particular voter", i.e. B_self = $10,000, then p·B_self "less than 10 cents"). One wording to watch: b = B/N is called "the expected benefit, per affected person in the population, of changing the election outcome", yet b = B/N has **no p in it**; "expected" there seems to mean "anticipated/perceived" [I], so the word "expected" in the paper does not always mean "multiplied by p".

### S7 Fork: the tie rule (the factor ½)
- First pass said: p = ½[P(others tied) + P(your side one short)] "(my algebra, matching Gelman et al.'s and Barnett's ½)" (L314). No statement about Edlin et al.'s tie rule.
- Mark: confirmed
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Appendix and footnote 12, PDF p. 21 (printed p. 20)
- Quote: "The probability of a decisive vote is then half the probability that a single vote can make or break an exact tie, or f (0)/n."
- Quote: "The assumption here is that an exact tie vote will be decided by a coin flip."
- Quote: "1/(0.2n) = 5/n that a single added vote could create or break a tie."
- Note: **Edlin et al. do build the ½ in.** Their p ("decisive") is half the probability of making or breaking an exact tie, on a coin-flip tie rule, and p = K/n, p = 1/(0.12n) and 10/n are all that halved quantity (my check in M6). Footnote 12 continues that with recounts "this result is still valid and can be obtained by integrating over the range of votes for which a recount is possible" (citing Gelman, Katz & Bafumi 2004). The Appendix example's gloss ("the probability is about 1/(0.2n) = 5/n that a single added vote could create or break a tie") fits f(0)/n, not 2f(0)/n, so it is loosely worded [I]. The main-text Assumption says p "essentially is the probability that an election is exactly tied" (S4).

### S8 Fork: is "held fixed" causal or evidential?
- First pass said: nothing about Edlin et al. (L162-165 treat it for other sources).
- Mark: unread (the paper has no statement to confirm or correct; absence established by reading the whole paper and searching it for "evidential", "causal", "counterfactual")
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Sect. 2.1 footnote 5 (PDF p. 6, printed p. 5); Sect. 2.2 (PDF p. 8); Sect. 5.3 (PDF p. 16, printed p. 15)
- Quote: "In contrast, we embed our individual and social benefits within a decision theoretic framework."
- Quote: "a “cascading” effect that motivates others nearby in the social network also to vote."
- Quote: "Fowler (2005a) examines evidence that an individual’s decision to vote can have a"
- Note: The paper does not address causal versus evidential decision theory (the words "evidential", "counterfactual" and "causal decision" do not occur; "causal correlation" in Sect. 5.4, PDF p. 17, is about separating a voter's perceived personal and social gains). Everything is a standard "decision theoretic framework" with p and n as given quantities for the individual: p = K/n, n = n_elig·T, with T pinned by an equilibrium in which each person's decision uses the common T. The only mention of one voter's act influencing other voters is Fowler's (2005a) "cascading" effect, cited as a possible extension (Sect. 5.3). "Held constant" in the paper is a ceteris-paribus comparison across elections ("holding constant these other factors", PDF p. 5, printed p. 4; "only if all other factors in the election were held constant", PDF p. 12, printed p. 11), not the owner's counterfactual. Marked unread only because there is no statement to quote.

### S9 Fork: what D is
- First pass said: "D term is added after [pB] and is not multiplied by p" (L44); "Edlin et al. fold it into c ... so c can be negative" (L186).
- Mark: confirmed
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; footnote 4 (PDF p. 5, printed p. 4); Sect. 2.1 (PDF p. 7, printed p. 6); Sect. 2.2 (PDF p. 9, printed p. 8)
- Quote: "the direct gratifications of voting (including the performance of a civic duty); that is, a negative net cost c of the act of voting."
- Quote: "(these are the people for which the direct benefits of voting exceed its costs, irrespective of who wins)."
- Quote: "the relative benefit associated with your desired candidate winning the election"
- Note: D is the "direct benefit of voting (whether or not your candidate wins)": "the direct gratifications of voting (including the performance of a civic duty)", i.e. "irrespective of who wins". The paper never separates D after footnote 4 (c = C − D). It also claims a way to tell B_soc from civic duty: B_soc is "multiplied by Pr(election is tied), and civic duty is not" (E21). The paper says turnout "is thus usually attributed to some mix of irrationality, confusion, and the direct gratifications of voting" (PDF p. 7), which it treats as the standard way of explaining why people vote at all, and then argues these motives "do not explain observed variations in voter turnout between elections".

### S10 Fork: what counts in C
- First pass said: c is net cost, may be negative (L34, L213); no list of components for Edlin et al.
- Mark: confirmed
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Sect. 2.1 (PDF pp. 5, 7; printed pp. 4, 6); Sect. 1 (PDF p. 4, printed p. 3); Sect. 5.1 (PDF p. 15, printed p. 14)
- Quote: "Given that the act of voting has a nonzero cost, voter turnout is thus usually attributed to some mix of irrationality, confusion, and"
- Quote: "a small effort yields a substantial expected social gain, equivalent in some ways to giving $250 to a national charity."
- Quote: "as the cost of voting declines, more people, and importantly more people who are poorly informed, will find it rational"
- Quote: "actions such as the decision to gather information in order to make an informed vote) is rational in large elections only to the extent that voters are not selfish."
- Note: The paper never itemises C (no time, travel, registration or information costs, and no dollar figures other than the hypothetical $25 threshold). It treats "cost of voting" as a single net number c that can be positive or negative; "a small effort" is its description of voting; it counts "the decision to gather information in order to make an informed vote" among the "related actions" whose rationality in large elections also depends on non-selfishness (PDF pp. 14-15), which is a statement about information as a decision, not a measured cost.

### S11 Statement bearing on strategic voting and more than two candidates (cross-reference to Kselman)
- First pass said: nothing about Edlin et al. on this (L102-105 use other sources).
- Mark: confirmed
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Sect. 4.1, PDF p. 13 (printed p. 12)
- Quote: "supporters of the third candidate to vote for one of the leaders"
- Quote: "Strategic voting behavior is consistent with our model because it suggests that at least some voters are acting based on the anticipated consequences if"
- Note: The paper's model is two-candidate ("a two-candidate election with n voters", PDF p. 7); it mentions three-candidate U.K. races only as evidence that votes are seen as consequential. It has no multi-candidate pivot calculus. The second quote is cut at the line end; it continues "their vote is decisive."

---

## F. Found that the first pass missed (new items, with their quotes in entries above or below)

### N1 The tie rule is stated by Edlin et al. (S7, M6)
- First pass said: no statement about it for Edlin et al.
- Mark: confirmed
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Appendix and footnote 12; PDF p. 21 (printed p. 20)
- Quote: "The assumption here is that an exact tie vote will be decided by a coin flip."
- Note: p = f(0)/n is half of the probability of making or breaking an exact tie. If the site's p includes the factor ½ already, the Edlin et al. K and the 1/(0.12n) are on that footing; if it does not, the ½ must be applied to them (or K doubled) before using them. See M6.

### N2 "Approximately independent of the size of the electorate" holds at fixed N/n
- First pass said: "their product is roughly flat in electorate size" (L195).
- Mark: confirmed
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Sect. 2.1 opening, PDF p. 5 (printed p. 4)
- Quote: "and thus the expected utility of voting is proportional to N/n, which is approximately independent of the size of the electorate."
- Note: Spelled out in E22. If turnout as a share of the affected population differed, the $250 would change in inverse proportion (for example $125 if n/N were 2/3 rather than 1/3: $250 × (1/3)/(2/3)).

### N3 K = 10 corresponds to ±5% (uniform density), not the main text's ±6%
- First pass said: both K = 10 and ±6% / 1/(0.12n) are given as inputs (L270), without noting they differ.
- Mark: confirmed
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; PDF pp. 6, 7, 21 (printed pp. 5, 6, 20)
- Quote: "In practice, we see 10/n as a reasonable approximate probability of decisiveness in close elections"
- Note: M5. The main example gives 8.33/n; "less than 10 cents" at n = 1 million is for 8.33/n; with 10/n it is exactly 10 cents.

### N4 Section 2.2's percentages with δ contradict themselves (M7)
- First pass said: nothing.
- Mark: confirmed (as a statement of what the paper says; the inconsistency is the paper's)
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Sect. 2.2, PDF p. 10 (printed p. 9)
- Quote: "If δ = 1, then Pr(c > 0) = 0.16, which means that 60% of the eligible voters would vote, even in an election with no importance."
- Note: The paper's "Pr(c > 0) = 0.16" is Pr(c < 0) = Φ(−1) = 0.159, and "60%" does not follow; see M7. Relevant if the site ever quotes the share of people who vote "even in an election with no importance".

### N5 Footnote 13's cross-reference does not match this text (further sign of a different draft; see A5)
- First pass said: nothing.
- Mark: confirmed (the footnote says this; the mismatch is my observation)
- Source: edlin_nber; https://www.nber.org/papers/w13562.pdf; Appendix, footnote 13; PDF p. 21 (printed p. 20)
- Quote: "See footnote 5 on page 5."
- Note: Footnote 13 is attached to the Appendix's "±10%" example. In this file footnote 5 on printed p. 5 is about the dual-utility literature and Jankowski (2002), not about adding a vote to make or break a tie, so the cross-reference does not match this text [I]; another sign that the body comes from a different draft.

### N6 Kselman: p_jk is a proxy index, not the pivot probability
- First pass said: three-candidate condition and "pivotal ... 1st-place ties" (L106), with no statement that the p_jk used are not probabilities of being pivotal.
- Mark: confirmed
- Source: kselman; as K01; Sect. 1.1, PDF p. 2 (printed p. 2); Sect. 2, PDF p. 3 (printed p. 3); Sect. 3, PDF p. 4 (printed p. 4)
- Quote: "that it aims to create a reliable empirical proxy for the probability of"
- Quote: "casting a pivotal vote in a plurality election."
- Quote: "ranges from 0 to 1, is of course not a direct measure of pjk , which will be small in large electorates."
- Quote: "Section 2 developed a new strategy for measuring pjk , the probability"
- Note: The paper's p_jk is a closeness **index** built from the voter's perceived winning probabilities p_j (ratios such as p_j/p_k with p_j < p_k, so that p_jk ≤ 1), not the probability that one vote is pivotal. The Section 2 text is explicit for the two-candidate difference proxy (the quote above says it "is of course not a direct measure of pjk , which will be small in large electorates"). The Section 3 sentence nevertheless calls p_jk "the probability of creating or breaking a tie between one's jth and kth preferences" (the rest of that sentence continues on the next layout line with the other column's text between, so I quote the first half only). A reader citing eq. (4) for p-times-B should know the p_jk in the regressions are proxies on a 0-1 scale.

### N7 Kselman: U_j are the voter's own utilities, measured by "attraction"; no tie rule is stated; the factor 2 is not explained
- First pass said: nothing.
- Mark: confirmed
- Source: kselman; as K01; Sect. 3, PDF p. 4 (printed p. 4); Sect. 3.1, PDF p. 5 (printed p. 5)
- Quote: "the expected utility of choosing their second-preference is higher than"
- Quote: "that of choosing their first-preference. Define Uj as a voter’s utility for"
- Quote: "having their jth preference win the election, such that by construction"
- Quote: "We use Feeling Thermometers, which ask survey respondents to report"
- Quote: "their general ‘attraction’ to a party or candidate, to measure a voter’s"
- Quote: "Inequality (5) employs the assumption that adjacent probabilities in"
- Note: For the fork points: (i) welfare: U_j is the voter's own utility for candidate j winning; the data measure is a feeling thermometer of "attraction" to a party or candidate, not welfare, and others' welfare does not appear. (ii) B versus pB: each term in (4) is a closeness (a probability proxy) times a utility gap, so the utility gap is the gain if that pivot event occurs, like Edlin's B. (iii) tie rule: the paper does not state one; the factor 2 on p12 is not explained here, and footnote 14's assumption (adjacent probabilities in comparable outcome spaces are equal; it cites McKelvey and Ordeshook 1972, p. 51) is its only related statement. It plausibly belongs to how ties are counted in the cited prior work [I], which I have not read. (iv) D and C: there are none; eq. (4) is a choice between candidates for a voter who votes. The paper says of turnout only: "the COV was originally applied to the question of turnout" (PDF p. 4) and, in footnote 1, notes Green & Shapiro's criticism that it fails to explain turnout.

### N8 Kselman: "No paper has yet derived the full conditions for strategic voting in 4-candidate elections"
- First pass said: "with three or more candidates B is not one number: each pivot pair has its own utility gap and its own probability" [I] (L105), citing other sources.
- Mark: confirmed
- Source: kselman; as K01; Sect. 5, PDF p. 9 (printed p. 9)
- Quote: "paper has yet derived the full conditions for strategic voting in"
- Quote: "date elections, i.e. the equivalent to (5) above, which will be necessary"
- Quote: "the parameters p12 , p13 , and"
- Note: The Conclusion (the sentence begins "No" on the line before the first quote) says no paper has derived the 4-candidate analogue of (5), and that in a 4-candidate analysis p12, p13 and p23 would be joined by p14, p24 and p34. This supports the report's [I] that more candidates add pairwise terms, but it also says the formal condition is unknown beyond three candidates, so a sum of pairwise terms for n > 3 is the paper's expectation, not a proven result.

---

## Corrections table

| old (first report) | new | source |
|---|---|---|
| L34: B "relative benefit of the voter's preferred candidate winning" | B "is the relative benefit associated with your desired candidate winning the election" | edlin_nber, PDF p. 5 (printed p. 4), under eq. 1 |
| L75: B_soc "as perceived by the voter" | "as perceived by the person making the decision whether to vote" | edlin_nber, PDF p. 6 (printed p. 5) |
| L191: the paper "gives no empirical estimate of c" (as a quotation) | not the paper's words; the paper estimates no parameter and assumes a noncentral-Cauchy c/b; it hopes others will estimate "its parameters" (Sect. 5.4) | edlin_nber, PDF pp. 11, 17 (printed pp. 10, 16) |
| L191, L196, L270: α = 0.1 ... ≈ $250; "$250 vs c < $25" | $250 is undiscounted (no α); with α = 0.1 the value compared with c is $25 | edlin_nber, PDF p. 7 (printed p. 6) |
| L270: simulations "to illustrate" | "to illustrate" is not the paper's phrase here; inputs confirmed; the paper's framing is "Our key point is not that the curves in Figure 1 ... exactly fit turnout behavior" | edlin_nber, PDF p. 16 (printed p. 15) |
| L279: the round numbers "which they call suggestive" | the numbers are a "hypothetical election"; "suggestive" describes its supporting evidence | edlin_nber, PDF pp. 7, 11 |
| L34 etc.: page labels "p. 4 / 5 / 6 / Appendix p. 20" with the journal citation | they are printed folios of NBER WP 13562 (PDF pp. 5 / 6 / 7 / 21), not journal pages | edlin_nber (A5) |
| L106: Kselman "pivotal in creating or breaking 1st-place ties" (as a verbatim quotation) | the paper has ‘pivotal’ in single quotes: "are ‘pivotal’ in creating or breaking 1st-place ties between candidates"; the meaning is the same | kselman, PDF p. 1 |
| L106: three-candidate condition `... > 2·p12·(U1 − U2) > p13·(U1 − U3)` | transcription of printed eq. (4) is right, but eq. (5) shows the second ">" must be read as "+" (printed (4) is internally inconsistent with (5)) [I] | kselman, PDF p. 5 (printed p. 5) |
| L276: "a 1 in 10 million chance of breaking a tie" attributed to Edlin et al. | not in the Edlin et al. working paper; its figure is "10−7 or 10−8 ... (Gelman, King, and Boscardin, 1998)" | edlin_nber, PDF p. 5 (printed p. 4) |

Entry counts in this file: 60 entries = 50 confirmed, 7 corrected (E03, E07, E15, E18, E19, E20, A5), 3 unread (A4, E24, S8). Two further first-report strings are flagged as typographic only and marked confirmed: K02 (quote marks around "pivotal") and K03 (the ">" versus "+" point is a property of the printed equation).

## Unread and why

- **Revision dates of the NBER paper (A4):** neither the landing page nor the PDF gives any; only "October 2007" (and 2007-10-26 in raw meta).
- **The journal article's text** (*Rationality and Society* 19(3): 293-314): not among my sources; so I cannot say whether its equation numbers, footnotes, K = 10, the ±6% example, the $250/$25 example, or the Section 2.2 percentages match.
- **L276 (SEP quotation attributed to Edlin et al.)** and **L288 (Gelman, Silver & Edlin, 2008)**: SEP and the 2008 manuscript are not my sources.
- **L307's "one Wikipedia extract said 2008"**: Wikipedia is not my source; the NBER page and Stafforini both give 2007.
- **Kselman Supporting Information** (Parts I-VI: the proof of Proposition 1, the axioms' extensions, the argument in footnote 1 that expected utility is viable for voter choice even if not for turnout): not downloaded.
- **Kselman & Niou (2010), Hoffman (1982), Black (1978), Fisher (2004), McKelvey & Ordeshook (1972):** the sources the paper says it reproduces eq. (4) from; not read, so the factor 2 on p12 and the tie rule behind it are unexplained here.
- **Kselman Tables 1-3 and Figs. 1-4:** read only as text; the first report uses none of their numbers.
- **S8 (causal versus evidential "held fixed")**: the paper has no statement on it.

## Found that the first pass missed

1. **Tie rule (N1, S7, M6):** Edlin et al. build in the ½ (coin-flip tie rule; Appendix, fn. 12), and their K = 10, 1/(0.12n) are that halved quantity. The Appendix's gloss "could create or break a tie" for 5/n is loosely worded.
2. **B versus pB (S6):** B is the benefit "associated with your desired candidate winning"; "expected utility gain" is pB; but the paper also calls b = B/N "the expected benefit ... of changing the election outcome" with no p in it.
3. **$250 is undiscounted; $25 is the α = 0.1 value (E15, M3, M4).** The first report pairs them wrongly at L191, L196 and L270.
4. **The N/n condition (N2):** the "independent of the size of the electorate" result holds at fixed N/n; the example fixes n/N = 1/3.
5. **K = 10 versus ±6% (N3, M5):** K = 10 corresponds to ±5% under a uniform density; the main example (±6%) gives 8.33.
6. **Section 2.2 percentages contradict themselves (N4, M7).**
7. **D and C (S9, S10):** D is only the direct outcome-independent benefit folded into c = C − D (fn. 4), includes civic duty, and the paper never itemises C or gives costs other than the hypothetical $25 threshold; information-gathering is called a "related action" whose rationality depends on non-selfishness.
8. **Group version of B (S3):** Sect. 5.3-5.4 let B_soc be for a group and allow two α's (Californians versus other U.S. citizens).
9. **Causal versus evidential (S8):** not discussed; the only influence-on-others mention is Fowler's "cascading" effect (Sect. 5.3).
10. **Version (A5, N5):** NBER file is an older draft with a different body title; "to appear" references; fn. 13 cross-reference points to a footnote that does not match.
11. **Kselman (N6, N7, N8, K03):** p_jk is a proxy index (0-1), not the pivot probability; printed eq. (4) has ">" where eq. (5) needs "+"; U_j are own utilities proxied by feeling thermometers of "attraction"; no tie rule or cost/turnout term; the paper itself says the four-candidate conditions have not been derived.
