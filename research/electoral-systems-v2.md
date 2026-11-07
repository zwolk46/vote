# How "one vote changes the outcome" works across electoral systems: re-read at source (v2)

*Brief R4 (`briefs/R4-research-electoral-systems-at-source.md`). Written 2026-11-07 UTC by the R4 worker thread (Sonnet 5.5, xhigh) with six reading subagents (Sonnet 5.5, xhigh). The first pass, `research/electoral-systems.md`, is kept as it is: this file records what was believed then and what the sources say now. Nothing here chooses anything for the model or the site (`_COMMON.md` 3); where sources disagree each is given with its source.*

## Digest: read this first

**Result.** curl reaches the sources now. Every checkable statement of the first report (lines 16-299, 288 blocks including the fill items) was re-read at source and carries one of: **confirmed**, **corrected**, **unread**. By the readers' MARK lines, counted by script: 193 confirmed, 8 confirmed with a wording, section or number correction, 44 corrected, 31 unread, and 12 blocks whose mark is a status for a fill item or a split verdict (mixed, none found, partly read). Corrections are not rare: about one fact in six needed a change, and most of the large ones are in quotations and formulas that came through extracts. **Every quote in this file was checked by script against the extracted text of the source it names** (759 quotes: 758 found by script, and the one that sits in an HTML attribute found by `grep`; none missing). Quotes copied from a page that the reader had to convert (HTML to text, docx to text) say so in the block.

**What the first pass got right.** All of its own [measured] calculations reproduce exactly (Appendix A re-run, below). Its structural findings stand: a third candidate does not change the order of the tie probability (1/N, with a three-way tie of order 1/N²); a list-PR vote moves a seat about M/N of the time; a supermajority moves the knife-edge to q; chamber control multiplies the seat probability by a second-stage factor; small electorates have large probabilities.

**What changed, in the order it touches the model.**

1. **The tie constant (first-pass open question 1) is resolved, and it shows a definition the model must fix** (A-14, A-26). The extract had Gelman, Katz & Bafumi (2004) giving "(2/√π)·(1/√n_j)". The paper prints **√(2/π)·1/√n_j** (0.798/√n_j; the radical was lost in the text layer; read on the page image, p. 662). Under the paper's own definition (Sec. 2.1: the chance A wins when the voter supports A minus the chance A wins when the voter supports B) the exact value for a 50-50 race is √(2/(πN)), so the paper agrees with the first pass's exact calculation. The first pass's Q (a vote against abstaining, ties by a fair coin) is exactly half of that, 1/√(2πN). Both are right under their own comparison; they differ by a factor of 2. Gelman, King & Boscardin (1998) use f(0.5)/n_i for "tied or one vote away from a tie", at weight 1 (A-21). So every p in this literature is relative to a comparison and a tie rule, and the figures differ by 2 across them. Which comparison the site's p uses is for the orchestrator and the maker; the maker's words of 19:32 ("the difference between voting and not voting") describe the vote-against-abstaining comparison, which is the first pass's Q.
2. **GKB 2004's worked example "1.84/n_j" does not follow from its own formula** (A-15). As printed, [1/√(2π)(0.03)]·exp(−0.5(0.05/0.03)²) = 3.32; with the distance 0.02 that a 52% forecast implies, it is 10.65 (the normal density of N(0.52, 0.03²) at 0.5, which is also what GKB 1998 Sec. 5 gives); 1.84 is reproduced only by putting 0.03 under the radical as a variance. Do not use 1.84. Appendix eq. 3 of that paper is E[π(v+1/n) − π(v)] with π the probability that A wins, not "Φ(v − 1/n) − Φ(v)" (A-13).
3. **Myatt & Fisher (2002)** (A-05, A-06): Proposition 1 prints exactly f(x/n)/n^(m−1); Lemma 1 is for m = 3 only. The printed two-way formula carries a "6n" that should be "n": a hand check with a uniform belief (every count vector equally likely) gives 1/(3n) = ∫/n where the integral is 1/3, not ∫/(6n); the reader's exact computation agrees (A-06, [measured]). The orders (1/n for a two-way near tie, 1/n² for a three-way tie) and the three-way formula are as the first pass said. Table 1 (sixteen pivotal events) and Eq. 4-5 are now transcribed from the page images.
4. **Baltz (2025) does not give levels for a real election, and the first pass's caution was both right and wrong** (E-24, E-49, RECONCILIATION in §3). The "about 10⁻⁷ (plurality) and 10⁻⁶ (IRV)" averages are for the **power-law, clear-front-runner panel only**, on a log axis, as means of log₁₀ values; the **uniform panel at the same 1,000 voters** is on a linear axis and runs 0.003 to 0.12. The plotted y-value is a **sum over every ballot a voter might cast**, not the chance that one ballot is pivotal; per ballot it is in the same decade as the 1/N values (0.006 to 0.016). The paper's printed formula, which rests on independence assumptions, gives about half the exact Poisson-game value for three equal candidates (0.0075 against 0.0155), about 5 times lower for four and 21 times lower for five (the reader's plurality analogue, [measured]). The paper's one-sentence description of the power-law electorate, taken literally, gives about 10⁻⁷⁴ at N = 1,000, so it cannot be what was plotted; the exponent, the preference orders, the plurality formula (Mebane et al. 2019, a conference talk, now found at `https://websites.umich.edu/~wmebane/pm19.pdf`) and any code are not given in the paper. arXiv v2 (31 Jul 2023) has no appendix; the "supplement" is the published appendix (4 Sep 2024): a 25-voter worked example whose printed p_direct ≈ 0.023 reproduces only with the ½ on both tie terms and whose p_indirect ≈ 0.003 only with one tie term dropped (E fill F-1; FORMULAS S-1). The journal abstract sentence the first pass quoted ("These simulations produce similar estimated pivotal probabilities in the two systems") **is** in the journal abstract (read by the orchestrating worker on the Cambridge page, `txt/baltz_journal_abs.txt`), but is not in arXiv v2's abstract. Journal reference confirmed: Political Analysis 33(4), October 2025, pp. 447-455, doi 10.1017/pan.2024.32.
5. **Germany, BSW 2025** (C-39, C-46). The final totals are readable on the Bundeswahlleiterin's results page: BSW 2,472,947 second votes (4.981%) of 49,649,512 valid. The shortfall to 5.000% is **9,529 votes** if the extra votes come from other parties' votes (total unchanged, the convention that reproduces the Stuttgarter Zeitung's 13,435 for the provisional count) and **10,031** if they are new valid votes. The first pass's 9,158 was 371 too low because the 5% line rose by 371.25 votes when the valid total rose by 7,425. 9,529 is 0.0192% of all valid second votes, about one in 5,210. I re-did the arithmetic by hand (same results).
6. **Court wording** (C-13, C-36). The BVerfG press release of 30 July 2024 does not say the 5% threshold is "in its current form unconstitutional"; it says the threshold "in the current version of § 4(2) second sentence no. 2 ... violates Art. 21(1) and Art. 38(1) first sentence of the Basic Law", and, in the operative paragraph, "in its current form is incompatible with the Basic Law" (7:1; the coverage procedure was unanimous). The three-constituency clause was removed by the 2023 law and the Court made it a condition of the rule continuing to apply; BWahlG § 4 on gesetze-im-internet.de says the same. The 2008 release does not say "may arise in certain constellations" (the wording is "may lead to a situation in which in certain constellations ..."), and says the effect is not necessary to PR and depends mainly on the set-off of first-vote against second-vote mandates. **No BVerfG, Bundeswahlleiterin or Bundestag source read says whether negative voting weight can still occur under the 2023 reform.**
7. **Lyytikäinen & Tukiainen and Luechinger et al.** (C-27, C-30, C-33, C-45; C-15 to C-19). Tables 2, 3 and A1 and footnote 1 are confirmed from page images. **No aggregation formula for the election-level pivotality is printed**: the text says only "a weighted (by respective vote shares) average" and "simply the sum of these weighted between and within pivotalities". Table 2 uses counterfactual (adjusted) turnout. The 0.006 (party-election level) and 0.028 (candidate level) are different units; 234 is the sample minimum population and "roughly 800" is the smallest mainland municipality; election-level N is 1,746 (the data set has 1,747). Luechinger et al. (open access, read on Cambridge) **give no pivot probability and no seat-change count**, only margins, and criticise resampling-based closeness (the Kotakorpi method that Lyytikäinen & Tukiainen build on) as depending on the resample size (their Fig. 5: 0.35 to 1). Every formula was transcribed from page images and the D'Hondt margin was checked on the paper's own example (15, −10, −100); the candidate margin is on p. 107, not p. 106.
8. **Bouton (2013) has closed forms** (B-08, B-10; FORMULAS in §2): the first pass said the constants were not given. Lemma 2 gives mag = −(√τ_P − √τ_Q)² for a second-round pivot and Lemma 3 (eqs. 17-19) the first-round events; all five Table 2 values were recomputed from them (ζ = 0.5: −0.0835, −0.1227, −0.0014, −0.0251, −0.0251). They are exponential rates in n, not probabilities; in the model the two rounds have separate, fully redrawn electorates. The event notation is "i/ij" (slash), not "i=ij"; eq. 4 has ten terms, only two of them differences of expected second-round utilities. France: from the Conseil constitutionnel's own proclamations, 2002 (2002-109 PDR) Le Pen 4,804,713, Jospin 4,610,113, gap 194,600 (confirmed); 2022 (2022-195 PDR) Le Pen 8,133,828, Mélenchon 7,712,520, **gap 421,308**, which fills a gap the first pass could not (B-18). Lepelley et al.: every fraction and every Table 2 cell checks; "70.1165" is an OCR slip for "≅ 0.1165" (B section).
9. **Quotations that were not in the source.** Herrera & Mattozzi do not say "does not use the classic 'pivotal voter' concept" ("pivot" and "decisive" occur zero times, checked by `grep` by the reader and again by the orchestrating worker); their P = Pr(v_R ≥ v_S, v_R + v_S ≥ q) is the party-level probability that the reform passes, printed in the paper as `(v_R ≥ v)_S`, not a vote-decisiveness formula (D-16, D-17). The "12% ... 26%" is the No share (11.97%) and turnout (25.66%) of the first question of 12-13 June 2005. The two Article 75 phrases the first pass quoted are not in the Constitutional Court's English text, which reads "approved if the majority of those eligible have participated in the vote and if it has received a majority of valid votes" (D-03). Cooper & Munger's abstract does not contain "varied widely"; Foellmi et al. regress salience on distance and never say "Swiss". The Aguiar-Conraria appendix formulas are confirmed from the docx (the opponent participation-quorum line prints ρ(v+1,v) where its other lines print ρ(v,v+1); costs are uniform on 0 to 100, not [0, c]); the paper's main text is **unread** (paywalled on Cambridge, Cloudflare on core.ac.uk).
10. **Chamber control and small electorates** (F). GKB 1998 eq. (3) has three terms (the interval probability plus ½ times each of the two exact-tie end points), not "a factor 1/2 on the whole second factor"; the symbol is E₋ᵢ. The figures at line 205 are all confirmed but cite the wrong sections (Vermont and "hundreds of millions" are in Sec. 4.3; "1 in 10,000" and .5/20,597 are in Sec. 5). The 538 page is now an ABC News redirect; its 218th-seat sentence, 40,000 simulations and 70-in-100 are confirmed only through a WebFetch extract, and the CSV with the tipping-point column was not obtained. Farber prints **no** ΔW values anywhere; "50 to 75" (Sec. 2.3, not 1.2) and "24 to 30" are different populations (all elections against the model sample of 75,300 elections with 2 to 200 voters, whose mean is 26.75, [measured]). Ballotpedia's page contradicts itself (734 against 733 rows; "496 fewer than five" against 352 in the table; its largest total is 393,922, Iowa 2, 2020, not 23,525; 267 of 733 rows are North Carolina 2019 municipal races; "0.004%" and "660" are wrong or stale; no method statement). Mulligan & Hunter's published abstract says "one of every 89,000"; the NBER working paper says 100,000.
11. **Allard (1996) is not an IRV estimate** (E-F3a, E-F3b): it is a party-level, final-stage, multi-member STV calculation (2.5 × 10⁻⁴ per constituency election, uniform prior, London poll), downward-type; Ornstein & Norman's "about once per century" compresses it, and Warren Smith's rangevoting.org page says it is about 1000 times too small. Graham-Squire & McCune: the file is **v2 (6 March 2023)**; two of the three inconsistencies the first pass flagged are in the paper as printed (52.5% against 95/182 = 52.2%; "six" against seven compromise elections), the Alaska "hypothetical shift" is not an inconsistency (every monotonicity paradox is defined by a hypothetical shift); the counts 3, 2, 1, 2/181, 3, 7 are not printed but match the paper's listed elections; the Conclusion's "0.5-1.1%" omits its own Table 7's 1.6% upward rate. All of Ornstein & Norman's numbers are confirmed.
12. **Scottish STV and Fox & Bruyns** (B-32 to B-36, B-45): Springer returns a Client Challenge, so only Crossref abstracts were read. Confirmed: 1,079 elections, 62 with an anomaly. Unread: the 30/1,049 split, the per-type counts, "lower bound", the introduction's "1-4%". The quotation "similar to prior empirical research and much lower than most theoretical research" is not in the abstract. The Fox & Bruyns DOI is a paper on Borda-count variations, not STV, so the "multiwinner version of IRV" quote is unverified. Preprints: arXiv 2305.17741 and 2501.00618 (NEED-FETCH).
13. **Droop quota** (B fill F-01): the Scottish Local Government Elections Order 2007 rule 46 and Ireland's Electoral Commission both give floor(V/(S+1)) + 1; Laird et al. print a ceiling form.

**What the model cannot yet rest on, because it is unread.** The Aguiar-Conraria main text (quorum turnout figures, the "40" against "57 to 70" boycott effect). New Zealand's rules (Cloudflare on `electionresults.govt.nz`, an Incapsula stub on `elections.nz`, an empty 202 from `legislation.govt.nz`; IDEA 2005 corroborates only "5 per cent or one single-member district seat" and that overhang is possible). Myerson 1998/2000 and Myerson & Weber 1993 (the "magnitude" theorem is stated only second-hand, in Bouton's Appendix A1; Myerson 1998 is IJGT 27(3): **375**-392, not 385-392), Cox 1994/1997, Chamberlain & Rothschild, Good & Mayer (TLS failure through the proxy at `home.uchicago.edu`, a captcha at ScienceDirect, an HTTP 500 at Kellogg; 1/n against 1/√n is now source-backed through Myatt's Oxford DP 186 fn. 43). Mulligan & Hunter's full text. The 538 tipping-point CSV and methodology page. The Electoral Commission and Commons Library pages for the 2016 referendum (the four national figures are read only on `electionpolling.co.uk`; 33,551,983 equals Leave plus Remain exactly, so what that page calls "turnout" is the valid-vote total). The outcome of *AEC v Johnston* (election void, new Senate election in Western Australia, 5 April 2014, is not on any page reached). A readable source that states a supermajority pass condition Y ≥ q(Y+X) (D-01). No source says divisor methods are monotone in votes (the C reader's own 60,000-case check found no violation; a computation, not a source). **No published decisive-vote estimate was found for a real runoff, STV, referendum under a supermajority or quorum rule, primary, chamber or small local election, nor for a real PR election other than the Finnish bootstrap**; the queries tried are in the fill blocks.

**Lower-grade facts (WebFetch, because curl got an error page or an empty reply rather than a clean refusal; each is flagged in its block).** *AEC v Johnston* judgment facts (B-41 to B-43); ACE thresholds and the ACE STV text (B-44, B-F01, B-F04); 538's sentence, date and count (F-04 to F-06) and the 538 data dictionary and Princeton Election Consortium page in F's fill F-1. B's note: the rule "WebFetch only when curl is refused" was ambiguous for an error page; it used WebFetch and flagged each fact. Three bot-checked hosts were not circumvented (rule 6): `electionresults.govt.nz` (Cloudflare), `core.ac.uk` (Cloudflare), `link.springer.com` (Client Challenge); also refused or blocked: `electoralcommission.org.uk`, `senato.it` (WAF), `info.gouv.fr`, `ssoar.info` (Anubis), `archiv.ub.uni-heidelberg.de` (Anubis). Reader D listed seven further hosts it touched for fill items (one or two requests each).

**Questions for the orchestrator (none for the maker).** (a) Which comparison does the model's p use: a vote against abstaining (the first pass's Q; the maker's 19:32 wording), or against the other side (GKB's definition, twice as large), and how are ties broken (fair coin in the first pass)? Every number in §1, §6 and §9 is in the first convention. (b) The first pass's stylised calculations for runoff, IRV/STV, quorum, primary and chamber control reproduce but have no published counterpart; whether they may be used as they are or must be marked as this project's own model is the orchestrator's call. This worker chose nothing.

**How the rest of the file is laid out.** An index of all 288 blocks with their marks; §0 how this was read; §1 to §9 the first pass's nine sections, each a register of the readers' blocks (id, the first-pass claim with its line number, MARK, SOURCE, exact quotes, correction, note); §10 the summary and the twelve open questions with their dispositions; then the fill items; **Appendix A re-run**; **the table of every correction**; the formulas as printed (collected from the readers); everything still unread and why; follow-up fetches. Block ids keep the reader's letter (A to F); in the registers a bracket shows the reader. The `QUOTE[...]` file labels name extracted text files kept outside the repository (`CLAUDE.md`: web pages go to scratch); the URL in each block's SOURCE line re-fetches the original.

## Index of every fact and its mark

*All 288 blocks, by first-pass section (fill items last): reader and id, the mark, the first-pass claim (cut at 100 characters; its line number is in the block). The mark column is the class the script read from the reader's MARK line; the block has the reader's exact words. confirmed = the source says it; corrected = the right value or wording is given; unread = with the reason in the block; other = a fill item or split verdict, see the block.*

| Block | § | Mark | First-pass claim |
|---|---|---|---|
| [A] A-01 | §1 | confirmed | "What decisive means": with 3+ candidates a vote is decisive only if, among the other voters, the le |
| [A] A-02 | §1 | confirmed | Citation: Myatt & Fisher, "Everything Is Uncertain and Uncertainty Is Everything: Strategic Voting i |
| [A] A-03 | §1 | confirmed | Pivotal event quote: "She may only influence the identity of the winner in the context of a pivotal  |
| [A] A-04 | §1 | confirmed-with-correction | Eq. 1: Pr[x] = integral Pr[x\|p] f(p) dp = (n!/prod x_j!) integral prod p_j^{x_j} f(p) dp; x_j votes  |
| [A] A-05 | §1 | confirmed | Proposition 1 (Sec. 2.2, p. 7): Pr[x] ≈ f(x/n) times 1/n^{m-1}, m = number of candidates (L24) |
| [A] A-06 | §1 | confirmed-with-correction | Lemma 1 (Sec. 2.3, pp. 8-9): two-way near-tie probability of order 1/n; three-way tie Pr[x1=x2=x3+1] |
| [A] A-07 | §1 | confirmed | Quote: "the probability of a three-way tie vanishes at rate n^-2, whereas the probability of a two-w |
| [A] A-08 | §1 | confirmed | Quote: "three-way and near three-way ties are asymptotically irrelevant to voter i = 0" (p. 9) (L25) |
| [A] A-09 | §1 | confirmed | The extractor flagged Table 1 and Eq. 4 as garbled; not reproduced (L26) |
| [A] A-10 | §1 | confirmed | Baltz uses, for SMDP, "the Mebane et al. (2019) derivation" with Skellam-based pivot probabilities u |
| [A] A-11 | §1 | confirmed | Citation: Gelman, Katz & Bafumi, "Standard Voting Power Indexes Do Not Work: An Empirical Analysis", |
| [A] A-12 | §1 | confirmed-with-correction | Two-party: Pr(decisive vote) ≈ p_{v_j}(0.5)/n_j (eq. 2 and Appendix eq. 3); p_{v_j} the density of t |
| [A] A-13 | §1 | corrected | Appendix eq. 3: "Pr = E[Phi(v - 1/n) - Phi(v)]" (L28) |
| [A] A-14 | §1 | corrected | Under random voting, an approximation "of the form (2/sqrt(pi)) * (1/sqrt(n_j))" (as extracted; cons |
| [A] A-15 | §1 | confirmed-with-correction | Sec. 2.3 forecast example: 10,000 voters, 52% forecast, 3% standard error gives decisiveness ≈ 1.84/ |
| [A] A-16 | §1 | confirmed | Sec. 2.3 cites the Good & Mayer / Chamberlain & Rothschild rule that decisiveness is proportional to |
| [A] A-17 | §1 | confirmed | M&F imply the same order, 1/n, for a two-way near-tie with a third candidate trailing, and 1/n² for  |
| [A] A-18 | §1 | other | First pass's [measured] table (L38-47): exact calculation of Q_j = P(j wins \| votes j) − P(j wins \|  |
| [A] A-19 | §1 | confirmed | First-pass line 49: "the known-shares rows show the effect of the 'only top-two votes enter the marg |
| [A] A-27 | §1 | corrected | (the first pass's Appendix equation "Pr = E[Phi(v - 1/n) - Phi(v)]" and the "random voting" constant |
| [A] A-28 | §1 | confirmed | GKB 1998 Sec. 5: probability that a single vote is decisive when the forecast is normal(μ, τ²): (√(2 |
| [E] E-19 | §1 | unread | line 27: citation, "published Political Analysis 33(4):447-455, 2025, doi 10.1017/pan.2024.32" |
| [E] E-20 | §1 | confirmed | line 27 (second part): "It uses, for single-member-district plurality (SMDP), 'the Mebane et al. (20 |
| [E] E-21 | §1 | confirmed | line 31 (first part): "100 runs per setting, 3, 4 and 5 candidates, 'a community of 1,000 voters' (c |
| [E] E-22 | §1 | confirmed | line 31 (second part): power-law preference structure "half of the population holds one preference o |
| [E] E-23 | §1 | confirmed | line 31 (third part): "No ratios printed. The paper itself calls these 'out-of-equilibrium pivotal p |
| [E] E-24 | §1 | corrected | line 31 (caution, [inferred]): "values this small, at N = 1,000, most likely arise because the styli |
| [B] B-01 | §2 | confirmed | Bouton, AER 103(4): 1248-88 (2013); version read is the author's draft, first draft March 2006, revi |
| [B] B-02 | §2 | confirmed | Setup (Sec. 2): three candidates {A,B,C}, Poisson electorate with mean n, twelve voter types (line 5 |
| [B] B-03 | §2 | confirmed | Round-1 actions {A,B,C,abstain}; if no candidate passes threshold theta a second round between the t |
| [B] B-04 | §2 | confirmed | Ties by alphabetical order (results also hold with a fair coin) (line 56) |
| [B] B-05 | §2 | confirmed | Second-round pivot event: piv^2_PQ is the event that P "trails behind Q by exactly one vote"; a tie  |
| [B] B-06 | §2 | confirmed | G_2(P\|t) = Pr(piv^2_PQ)[U(P\|t) - U(Q\|t)] (line 57) |
| [B] B-07 | §2 | confirmed-with-correction | First-round pivot events, four kinds, Table 1 (line 58) |
| [B] B-08 | §2 | corrected | First-round payoff G_1(i\|t) (eq. 4) "sums pivot probabilities times expected second-round utility di |
| [B] B-09 | §2 | confirmed | Sizes: pivot events compared by "magnitude", mag(E) = lim log Pr(E)/n (App. A1) (line 59) |
| [B] B-10 | §2 | corrected | Lemma 2 (second round): "for a ballot to be pivotal, candidates have to receive (almost) the same nu |
| [B] B-11 | §2 | confirmed | Table 2 (theta = 0.5): mag(piv^1_CA/CB) = -0.0014 is the largest listed; mag(piv^1_B/BC) = -0.1227 ( |
| [B] B-12 | §2 | confirmed | "which first-round event dominates changes with the type distribution and threshold" (Tables 2-4) (l |
| [B] B-13 | §2 | confirmed | "Published estimates of the probability. None found. Bouton gives exponents, not a probability for a |
| [B] B-14 | §2 | confirmed | France 2002: Le Pen 4,804,713 (16.86%), Jospin 4,610,113 (16.18%) (line 64) |
| [B] B-15 | §2 | confirmed | Gap 4,804,713 - 4,610,113 = 194,600 (line 64) |
| [B] B-16 | §2 | confirmed | Maire-info is a "secondary reproduction", published 25 April 2002 with president Yves Guena (line 64 |
| [B] B-17 | §2 | confirmed | France 2022: Macron 27.84, Le Pen 23.15, Melenchon 21.95, Zemmour 7.07 (LCP, Interior Ministry's def |
| [B] B-18 | §2 | corrected | Gap Le Pen minus Melenchon = 1.20 points; "The page gave no vote counts for Le Pen; the vote gap is  |
| [B] B-19 | §2 | confirmed | "The outcome she can change is 'which candidate wins', but through a longer chain: first-round vote, |
| [B] B-20 | §2 | confirmed | (a) "The second-round pivot probability is the two-candidate probability for the two finalists" (lin |
| [B] B-21 | §2 | confirmed | Lepelley, Chantreuil & Berg, "The likelihood of monotonicity paradoxes in run-off elections", Math.  |
| [B] B-22 | §2 | confirmed | "Three candidates only ('limited to the three-alternative cases'), 'impartial anonymous culture'" (l |
| [B] B-23 | §2 | confirmed | Abstract: "A monotonicity paradox occurs when a voting system reacts in a perverse way to a change i |
| [B] B-24 | §2 | confirmed | Plurality run-off, large n: M1 (more-is-less) 13/288 = 0.0451 (Cor. 1) (line 67) |
| [B] B-25 | §2 | confirmed | Plurality run-off, large n: M2 (less-is-more) 17/864 = 0.0197 (Cor. 3) (line 67) |
| [B] B-26 | §2 | confirmed | Either paradox under plurality run-off: 397/6912 = 0.0574 (Sec. 3.1) (line 67) |
| [B] B-27 | §2 | confirmed | Anti-plurality run-off, large n: 1/18 = 0.0556 (M1, Cor. 2), 7/108 = 0.0648 (M2, Cor. 4), either 151 |
| [B] B-28 | §2 | confirmed | Table 2 (plurality run-off, M1): n = 24, 0.01152; n = 60, 0.02781; n = 120, 0.03568; n = 192, 0.0390 |
| [B] B-29 | §2 | confirmed | "These are shares of random profiles in which some change of opinions would cause the paradox, not t |
| [E] E-01 | §3 | confirmed | line 73: IRV "decisive" has two ways, both defined in Baltz (2025) |
| [E] E-02 | §3 | confirmed | line 74: direct pivotality = break a first-place tie ("one vote short of winning") or create one (fa |
| [E] E-03 | §3 | confirmed | line 75: indirect pivotality = ranking c changes the drop sequence from A to A', final winner change |
| [E] E-04 | §3 | confirmed | line 76: indirect pivotality is "closely related to some well-studied phenomena (especially IRV's fa |
| [E] E-05 | §3 | corrected | line 78: notation (kappa, L, beta, S, A = [S_1..S_{kappa-1}, c], y, A' agreeing with A "up to c's po |
| [E] E-06 | §3 | confirmed | line 79: p = p_direct + p_indirect |
| [E] E-07 | §3 | confirmed | line 80: p_direct(beta) formula (sum over i, over drop sequences S consistent with the ballot, of [p |
| [E] E-08 | §3 | confirmed | line 81: p_indirect(beta) formula |
| [E] E-09 | §3 | confirmed | line 82: expected utility multiplies each by the payoff difference u(i) - u(S_{-1}) (direct), u(A'_{ |
| [E] E-10 | §3 | confirmed | line 83 (first part): modelling by Skellam probabilities under Poisson voting games, following Meban |
| [E] E-11 | §3 | confirmed | line 83 (second part): Assumptions 1 and 2 (independence of pairwise comparisons within and across r |
| [E] E-12 | §3 | confirmed | line 83 (third part): the "apparent faster decline in IRV as candidates increase" "may be attributab |
| [E] E-13 | §3 | confirmed | line 84: supplementary file of the published paper (URL listed by search but not read) |
| [E] E-14 | §3 | confirmed | line 86: published estimates: IRV "very slightly higher ... (averaging about 10^-6 compared to about |
| [E] E-15 | §3 | unread | line 86 (last sentence): Abstract: "These simulations produce similar estimated pivotal probabilitie |
| [E] E-16 | §3 | confirmed | line 94 (first sentence): size relative to a two-candidate race: "similar" in simulations of 1,000 v |
| [E] E-17 | §3 | confirmed | line 94 (rest): [inferred] "indirect pivotality has no counterpart in plurality; in Baltz's stylised |
| [E] E-18 | §3 | confirmed | line 96: [inferred] "in the indirect-pivotality term, Baltz's expected-utility rule u(A'_{-1}) - u(A |
| [E] E-25 | §3 | confirmed | line 89: citation "Ornstein & Norman, 'Frequency of monotonicity failure under Instant Runoff Voting |
| [E] E-26 | §3 | confirmed | line 89: definition: upward failure is where "the IRV winner would lose if ranked higher by some sub |
| [E] E-27 | §3 | confirmed | line 89: method: 2-D spatial model, three adaptive candidates, 1,001 voters, four voter distribution |
| [E] E-28 | §3 | confirmed | line 89: results "anywhere from 0.7 % to 51 % of all cases" |
| [E] E-29 | §3 | confirmed | line 89 and §10.3 item 2: "between 15 % and 51 % of competitive elections (excluding ties, which acc |
| [E] E-30 | §3 | confirmed | line 89: "competitive" is a vote-count condition (c > (V+2)/4), not a margin |
| [E] E-31 | §3 | confirmed | line 89: contrasts Allard (1996), who estimated failure "only about once per century" for a UK gener |
| [E] E-32 | §3 | confirmed | line 89 (end) and line 91: reports no per-ballot frequency; Burlington example moves 750 rankings; " |
| [E] E-33 | §3 | confirmed | line 90: citation and version |
| [E] E-34 | §3 | confirmed | line 90: "Database of 182 elections for political office, all without an initial majority winner" |
| [E] E-35 | §3 | confirmed | line 90: abstract quotation "rarely observed" |
| [E] E-36 | §3 | confirmed | line 90 and §10.1 and §10.3 item 2: rates "upward monotonicity failure 3 of 182 (1.6%), downward 2 o |
| [E] E-37 | §3 | confirmed | line 90: "'majoritarian failure' (winner without a majority of ballots cast, because of exhausted ba |
| [E] E-38 | §3 | confirmed | §10.3 item 3: Table 7 52.5% versus 52.2% |
| [E] E-39 | §3 | confirmed | §10.3 item 3: "the text says six compromise-voting elections but lists seven" |
| [E] E-40 | §3 | corrected | (new) Conclusion rate range for monotonicity/no-show paradoxes |
| [E] E-41 | §3 | confirmed | line 90: Burlington 2009: "450 voters who voted only for Wright and 300 voters who ranked Wright fir |
| [E] E-42 | §3 | confirmed | line 90: San Francisco: "Melgar 18,561 to Engardio 16,370; shift 800 ballots" (downward) |
| [E] E-43 | §3 | confirmed | line 90: named upward cases: Burlington 2009; Minneapolis Ward 2 2021; Alaska US House special 2022 |
| [E] E-44 | §3 | corrected | line 90 and §10.3 item 3: "the Alaska upward-monotonicity example is a hypothetical shift of 6,000 b |
| [E] E-45 | §3 | confirmed | line 91 / line 92: "McCune & Graham-Squire ... 1,079 Scottish elections" (the 1,079 figure only) |
| [B] B-30 | §3 | confirmed | McCune & Graham-Squire, "Monotonicity anomalies in Scottish local government elections", Social Choi |
| [B] B-31 | §3 | confirmed | "In 62 of the 1079 elections we found some kind of monotonicity anomaly" (30 single-winner, 1,049 mu |
| [B] B-33 | §3 | confirmed | Quote "Most STV anomalies we find are the first of their kind to be documented in real-world multiwi |
| [C] C-01 | §4 | confirmed | L&T quote "one abstaining voter could change the allocation of seats between parties by voting" (Sec |
| [C] C-02 | §4 | confirmed | Luechinger-Schelker-Schmid "closeness" is "the minimal necessary movement along both margins to gain |
| [C] C-03 | §4 | confirmed | L&T quote "one voter could change which of the party's candidates gets the last seat of the party" ( |
| [C] C-05 | §4 | confirmed | in Luechinger et al. "who gets the party's seat" is the "candidate margin" (line 103) |
| [C] C-06 | §4 | confirmed | Germany: a constituency winner whose party's second votes do not "cover" the seat is not seated: "th |
| [C] C-07 | §4 | confirmed | "A party crosses a threshold. One vote decides whether a party gets any seats at all, which moves ma |
| [C] C-08 | §4 | unread | "No source I read models [coalition formation]; it is the 'chamber control' structure of section 8 p |
| [C] C-09 | §4 | unread | New Zealand (MMP): "The 120 highest numbers (which are called quotients) determine both the number o |
| [C] C-10 | §4 | confirmed | NZ threshold and overhang as stated by another source (not in the first pass; corroboration for line |
| [C] C-11 | §4 | confirmed | Germany: 2025 final result, 5% threshold; BSW 4.981%; the new Bundestag has 630 members; "7,425 high |
| [C] C-13 | §4 | corrected | BVerfG 30 July 2024, 2 BvF 1/23 and others: second-vote coverage compatible with the Basic Law (unan |
| [C] C-14 | §4 | confirmed | citation: Luechinger, Schelker & Schmid, "Measuring Closeness in Proportional Representation Systems |
| [C] C-15 | §4 | confirmed | D'Hondt party margin, p. 104: party margin_{i,j} = votes_j - i x ( votes_{-j} / i~ )_{(n(J-1) - (n - |
| [C] C-16 | §4 | confirmed | "so that the i-th seat is decided by a coin flip" (extractor's paraphrase); Sainte-Lague, modified S |
| [C] C-17 | §4 | confirmed | largest remainder (Hare-Niemeyer), pp. 105-106: quota = (votes_j + sum of votes_{-j})/n; "formulas g |
| [C] C-18 | §4 | corrected | candidate margin (open lists), p. 106 (line 114) |
| [C] C-19 | §4 | confirmed | overall vote margin = max over i of min{party margin, candidate margin}, p. 107 (line 114) |
| [C] C-20 | §4 | confirmed | worked example (hypothetical), D'Hondt, 3 seats, parties with 45, 35, 20 votes: P2's party margins a |
| [C] C-21 | §4 | confirmed | Abstract: "In contrast to plurality systems, closeness in PR systems cannot be directly inferred fro |
| [C] C-22 | §4 | confirmed | the paper "reports no real-election figure for how many votes would change a seat, and gives no pivo |
| [C] C-23 | §4 | confirmed | L&T citation: VATT Working Papers 50/2016 (Jan 2016 version; original Sept 2013), doria.fi wp50.pdf  |
| [C] C-24 | §4 | confirmed | L&T data: 1,747 municipality-elections, five elections 1996-2012, populations 234 to 44,804 (mean 7, |
| [C] C-25 | §4 | confirmed | L&T method Sec. 4.2: resample votes with replacement at the observed shares, same number of votes as |
| [C] C-26 | §4 | confirmed | L&T pivotal event: tie "(in which case a lottery would determine who gets elected) and also when giv |
| [C] C-27 | §4 | corrected | L&T "election-level pivotality" = vote-share-weighted average of within- and between-party measures, |
| [C] C-28 | §4 | confirmed | L&T Table 2 Panel A, election level: Pivotality mean 0.063, sd 0.031, min 0.006, max 0.193 (N = 1,74 |
| [C] C-29 | §4 | confirmed | L&T Table 2 Panel B, party-election between-party pivotality mean 0.020 (sd 0.020, max 0.130; N = 10 |
| [C] C-30 | §4 | corrected | L&T within-party mean 0.006 (Table 2) versus 0.028 (Table A1, N = 146,234); paper says the gap "aris |
| [C] C-31 | §4 | confirmed | L&T Introduction: crossing the threshold raises between-party pivotality "from 1.7 times out of a hu |
| [C] C-32 | §4 | confirmed | L&T footnote 1: Mulligan & Hunter "one out of 89,000 in U.S. Congressional elections"; Gelman et al. |
| [C] C-33 | §4 | corrected | L&T "smallest mainland municipality has roughly 800 inhabitants" vs Table 3 minimum population 234 ( |
| [C] C-34 | §4 | confirmed | BVerfG press release 3 July 2008, 2 BvC 1/07: "if roughly 19,500 fewer second votes had been cast fo |
| [C] C-35 | §4 | confirmed | "it is also possible that not casting a voter's vote is beneficial to the party to be supported"; pr |
| [C] C-36 | §4 | corrected | the press release attributes negative weight to second votes for parties that win overhang mandates  |
| [C] C-37 | §4 | confirmed | BSW 2025, provisional: 2,468,670 of 49,642,087 valid second votes; lacked "exakt 13.435 Zweitstimmen |
| [C] C-38 | §4 | confirmed | the final count added 4,277 valid second votes for BSW (t-online) (line 121) |
| [C] C-39 | §4 | corrected | FINAL totals and exact final shortfall of BSW to 5% (the first pass subtracted 13,435 - 4,277 = 9,15 |
| [C] C-41 | §4 | confirmed | "The 2023 reform (second-vote coverage) was designed to remove overhang seats; I did not read a sour |
| [C] C-42 | §4 | confirmed | L&T party-election means "sit in the same range as my council-sized row ... a factor of 3 to 4 highe |
| [C] C-43 | §4 | unread | own computations: script pr.py cross-checked by pr_check.py; table rows with Q_j and M/N; "Reading"; |
| [C] C-44 | §4 | unread | "Thresholds create a second, much larger-benefit pivot ... Pr(party's share within one vote of 5%) i |
| [B] B-32 | §5 | unread | Counts by type: committee-size 9 (0.86% of multiwinner); upward 23 (2.1%); downward 17 (1.6%); no-sh |
| [B] B-34 | §5 | corrected | The authors say their results are a lower bound and "similar to prior empirical research and much lo |
| [B] B-35 | §5 | unread | the introduction states "on the order of 1-4% for each type", which does not match the committee-siz |
| [B] B-36 | §5 | other | Fox & Bruyns, Social Choice and Welfare 67 (2026) 143-166; they describe STV as "a multiwinner versi |
| [B] B-37 | §5 | confirmed | "I found no source that writes an explicit pivot-probability formula for multi-winner STV" (line 141 |
| [B] B-38 | §5 | confirmed | Laird, Malmskog, Pixler & Rodbell, "Simulating Single Transferable Voting for the Colorado House of  |
| [B] B-39 | §5 | confirmed | Laird: defines the anomaly as "decreased support for a candidate can improve their chances of gettin |
| [B] B-40 | §5 | confirmed | Laird: "the complexity of the STV algorithm makes it unlikely for any one voter to take advantage of |
| [B] B-41 | §5 | confirmed | Summary: "1,370 ballot papers had been lost between the earlier counts and the re-count"; "14 votes  |
| [B] B-42 | §5 | confirmed | "a further hearing on 20 February 2014 would 'determine the final disposition of the petitions'" (li |
| [B] B-43 | §5 | mixed | "Not read: the judgment itself, the electorate size, and what happened next" (line 148) |
| [B] B-44 | §5 | other | "I did not read a source stating the Droop quota formula, so none is given." (line 150) |
| [F] F-01 | §5 | confirmed | Ordeshook & Zeng, "Some Properties of Hare Voting with Strategic Voters", Public Choice 78(1) (1994) |
| [F] F-02 | §5 | confirmed | Ordeshook & Zeng abstract: "strategic voting does not ensure the selection of Condorcet winning cand |
| [F] F-03 | §5 | corrected | "The page shows no pivot analysis; the PDF body was not read" (line 146) |
| [D] D-01 | §6 | unread | Supermajority pass condition Y >= q(Y+X) "wherever a source states it" (task item 7; first pass l.15 |
| [D] D-02 | §6 | unread | Art. 75 English excerpt "at https://legislationline.org/taxonomy/term/12983" (l.156) |
| [D] D-03 | §6 | corrected | Art. 75 wording: "the majority of those with voting rights have voted" ... "a majority of votes vali |
| [D] D-04 | §6 | corrected | "A voter can then be pivotal for the quorum, not only the majority" and "Approval quorum: not read i |
| [D] D-05 | §6 | confirmed | Aguiar-Conraria, Magalhaes & Vanberg: title, "NIPE WP 14/2013", URL `https://core.ac.uk/download/556 |
| [D] D-06 | §6 | corrected | Lab model: 9 electors, binary choice, majority rule, voting costs c_i uniform on [0,c] (l.160) |
| [D] D-07 | §6 | unread | Sec. 2 quote: "a supporter of Change is pivotal if her vote is necessary either to reach the majorit |
| [D] D-08 | §6 | unread | Opponents' pivotal event "has two conflicting forms"; "She may be pivotal, in a desirable way ...";  |
| [D] D-09 | §6 | confirmed | Appendix 1 Supporter, participation quorum: [ sum_{v=2..4} rho(v,v)/2 + sum_{v=1..3} rho(v+1,v)/2 +  |
| [D] D-10 | §6 | confirmed | Appendix 1 Opponent, participation quorum: [ sum_{v=2..4} rho(v,v)/2 + sum_{v=2..3} rho(v+1,v)/2 - r |
| [D] D-11 | §6 | confirmed | "rho(v_o,v_s) the probability a voter attaches to the others' counts (v_o No, v_s Yes), b the suppor |
| [D] D-12 | §6 | confirmed | "These are for the experiment's quorum design, with 9 electors, not for real referendums" (l.160) |
| [D] D-13 | §6 | unread | Lab turnout 53.8% (+-4.0, 95% CI) no quorum; 39.9% (+-4.1) participation quorum; 47.0% (+-4.5) appro |
| [D] D-14 | §6 | unread | Boycott effect of a participation quorum "more than 40 percentage points" (Introduction) versus "57  |
| [D] D-15 | §6 | confirmed | Herrera & Mattozzi: title, "working paper (versions 2005-06)", URL (l.161) |
| [D] D-16 | §6 | corrected | "The paper does not use the classic 'pivotal voter' concept" (l.161): the paper's sentence or the fi |
| [D] D-17 | §6 | corrected | Herrera & Mattozzi decisive-event formula P = Pr(vR >= vS and vR + vS >= q) (l.161) |
| [D] D-18 | §6 | confirmed | Italian referendum: "the status quo party got only 12% of the votes but the total turnout was only 2 |
| [D] D-19 | §6 | confirmed | Foellmi, Heim & Schmid: title, "online appendix, 16 June 2025", URL (l.162) |
| [D] D-20 | §6 | confirmed | Foellmi et al.: quote that estimating the probability of being decisive is challenging (l.162) |
| [D] D-21 | §6 | confirmed-with-correction | Foellmi et al.: coefficient on distance -0.020 (SE 0.008) without, -0.021 (SE 0.009) with voting-day |
| [D] D-22 | §6 | confirmed | docx "The mathematics of the pivotal voter model with quorum requirements": "binary file the extract |
| [D] D-23 | §6 | confirmed | Hizen & Shinmyo (2011), "Imposing a turnout threshold in referendums", Public Choice 148(3) 491-503, |
| [D] D-24 | §6 | confirmed | "Published estimates. None found ... I did not read Mulligan & Hunter's paper itself, so I do not kn |
| [D] D-25 | §6 | confirmed | 2016 UK EU referendum: Leave 17,410,742 (51.89%), Remain 16,141,241 (48.11%), turnout 33,551,983 (72 |
| [D] D-26 | §6 | confirmed | "Margin 1,269,501 votes [17,410,742 - 16,141,241], 3.78% of the votes cast [1,269,501 / 33,551,983 = |
| [D] D-27 | §6 | confirmed | "Brexit referendum counts come from a secondary site that does not name its source; the Electoral Co |
| [D] D-28 | §6 | confirmed | l.178 arithmetic: "N about 3.4e7 ... Q roughly 7 to 8 divided by N, about 2e-7 ... 1.89 points ... f |
| [D] D-36 | §6 | confirmed | l.154: "a vote is decisive if the other votes are tied or one apart" (two-outcome contest) |
| [D] D-37 | §6 | corrected | l.180: "a quorum adds a second pivot event whose probability depends on the turnout forecast (not co |
| [D] D-29 | §7 | confirmed | "no source I read gives a formula for primaries"; "Not found: a published estimate of the probabilit |
| [D] D-30 | §7 | corrected | Gelman, King & Boscardin (1998), eq. 1: "Pr(your vote matters) = Pr(your vote is decisive in your st |
| [D] D-31 | §7 | confirmed | "the extractor's formula for the first factor, approximately f_{v_i}(.5)/n_i, is a reconstruction" ( |
| [D] D-32 | §7 | confirmed-with-correction | Cooper & Munger (2000), "The (Un)Predictability of Primaries with Many Candidates: Simulation Eviden |
| [D] D-33 | §7 | confirmed | Ballotpedia, "A look back at 2025 state primary election competitiveness", 2 July 2025: states, "51  |
| [D] D-34 | §7 | confirmed | "No margin-of-victory or close-race statistics in the article" (l.190) |
| [D] D-35 | §7 | unread | l.184 and l.193 structure claims (two-stage chain; "electability difference"; three structural diffe |
| [A] A-20 | §7 | confirmed | GKB 1998 eq. 1: "Pr(your vote matters) = Pr(your vote is decisive in your state) x Pr(your state is  |
| [A] A-21 | §8 | confirmed | GKB 1998: first factor, for even n_i, ≈ f_{v_i}(.5)/n_i (f the forecast density of the vote share);  |
| [A] A-22 | §8 | confirmed | GKB 2004: two-factor decomposition (Sec. 2.2); second factor ("Factor 1") roughly proportional to e_ |
| [A] A-23 | §8 | confirmed | Banzhaf index: probability a vote is decisive when everyone votes 50-50 (Sec. 2.1) (L201) |
| [A] A-24 | §8 | confirmed | GKB 2004 empirical result (Sec. 4, Fig. 3): fitted exponents "all closer to 0 than to" -0.5; decisiv |
| [A] A-25 | §8 | confirmed-with-correction | GKB 1998 figures (six sub-claims; the first pass gives them all as "(Sec. 6.1)") (L205) |
| [F] F-04 | §8 | confirmed | 538: "The 218th seat is the tipping-point seat because it is the House's median seat by partisanship |
| [F] F-05 | §8 | confirmed | 538 forecast "as of Oct. 14", 40,000 simulations (line 197) |
| [F] F-06 | §8 | confirmed | 538: "Republicans have a 70-in-100 chance of taking control of the House" (line 197) |
| [F] F-07 | §8 | unread | 538 tipping-point probability column is in a CSV the first pass did not open (line 197) |
| [F] F-08 | §8 | confirmed | Two stages in sequence (seat tie, then seat is the majority-maker); "The vote changes who controls t |
| [F] F-09 | §8 | confirmed | Setup of the [measured] chamber table: 435 seats, 218 is a majority (lines 207, 197) |
| [F] F-10 | §8 | confirmed | GKB 1998 two-stage decomposition: Pr(your vote matters) = Pr(decisive in your state) x Pr(your state |
| [F] F-11 | §8 | confirmed | GKB 1998: first factor "for even n_i is approximately f_{v_i}(.5)/n_i (f the forecast density of the |
| [F] F-12 | §8 | corrected | GKB 1998: second factor is "Pr(E_{P_i} in (.5 e_total - e_i, .5 e_total) \| v_i = .5), with a factor  |
| [F] F-13 | §8 | confirmed | GKB 2004: "the same two-factor decomposition (Sec. 2.2)" (line 201) |
| [F] F-14 | §8 | corrected | GKB 2004: "the second factor is, per the extract, roughly proportional to e_j" (line 201) |
| [F] F-15 | §8 | confirmed | GKB 2004: the linear approximation "has a relative error of less than 10 per cent for all states" (S |
| [F] F-16 | §8 | confirmed | GKB 2004: Banzhaf index = probability a vote is decisive when everyone votes 50-50 (Sec. 2.1) (line  |
| [F] F-17 | §8 | confirmed | GKB 2004 empirical result: Sec. 4, Fig. 3; US state lower houses and senates, US House, US Senate, E |
| [F] F-18 | §8 | confirmed | GKB 2004: fitted exponents "all closer to 0 than to" -0.5; decisive probability roughly proportional |
| [F] F-19 | §8 | confirmed | GKB 2004: random voting "overestimates the probability of close elections in larger jurisdictions" ( |
| [F] F-20 | §8 | corrected | GKT 2002: Statistical Science 17(4), Caltech working paper 1141, URL records/hpnm8-cmw66 (line 202) |
| [F] F-21 | §8 | confirmed | GKT 2002 abstract: "voting power ... is the probability that a single vote is decisive"; discusses t |
| [F] F-22 | §8 | corrected | GKT 2002: body not read - definition of voting power and treatment of two-stage elections (lines 202 |
| [F] F-23 | §8 | confirmed | Chamber (not EC): "I found no source writing the second-stage probability for a legislature in a clo |
| [F] F-24 | §8 | corrected | Line 205: GKB 1998 figures "(Sec. 6.1)": about 1 in 10 million (1992); 1 in 3.5 million in Vermont;  |
| [F] F-25 | §8 | corrected | Line 205: GKB 1998 "1 in 10,000" as upper bound for a typical 200,000-voter congressional race; empi |
| [F] F-26 | §8 | unread | [measured, stylised] stage-two factor table for a 435-seat chamber and its Reading (lines 207-221) |
| [F] F-27 | §8 | unread | "Size relative to a two-candidate plurality race ... smaller by the stage-two factor (about 0.01 to  |
| [F] F-28 | §9 | confirmed | Farber: union certification "unions lose ties" (footnote 5), decertification "the union wins ties" ( |
| [F] F-29 | §9 | confirmed | Farber, "Rational Choice and Voter Turnout: Evidence from Union Representation Elections", NBER WP 1 |
| [F] F-30 | §9 | confirmed | Farber Eq. 12: Delta W+ = Pr(n_p = n_c) as a sum over i = 0 to INT(n/2) of multinomial terms in p_p^ |
| [F] F-31 | §9 | confirmed | Farber Eq. 13: Delta W- = Pr(n_p = n_c + 1) (line 230) |
| [F] F-32 | §9 | confirmed | Farber symbols: n = N - 1 other eligible voters; p_p = mu G(b Delta W+), p_c = (1 - mu) G(b Delta W- |
| [F] F-33 | §9 | confirmed | Farber data: 75,300 on-site elections 1972-2009, 2,014,616 eligible voters in total (Table 1 note) ( |
| [F] F-34 | §9 | confirmed | Farber: "38 percent have 10 or fewer, 62 percent have 20 or fewer, and 74 percent have 30 or fewer e |
| [F] F-35 | §9 | corrected | Farber: "averaging 50 to 75 eligible voters" (Sec. 1.2) (line 230; section as cited by the first pas |
| [F] F-36 | §9 | corrected | Farber: "from 24 to 30 between 1972 and 2008" (Sec. 6.2) (line 230; §10.3 item 7, line 279) |
| [F] F-37 | §9 | confirmed | Farber prints both "50 to 75" and "24 to 30" "without reconciling them" (line 230; §10.3 item 7) |
| [F] F-38 | §9 | confirmed | Farber abstract: "most individuals (over 80 percent) vote ... independent of consideration" of pivot |
| [F] F-39 | §9 | confirmed | Farber "does not print the pivotal probabilities themselves" (line 230); task question: tables of De |
| [F] F-40 | §9 | confirmed | Lyytikainen & Tukiainen: Finnish municipalities as small as 234 residents; election-level mean pivot |
| [F] F-41 | §9 | confirmed | Gelman, Katz & Bafumi: the 1/sqrt(n) vs 1/n distinction and the Good-Mayer / Chamberlain-Rothschild  |
| [F] F-42 | §9 | confirmed | Ballotpedia "Races decided by 10 votes or fewer": the page, 2018-2026 (line 234) |
| [F] F-43 | §9 | confirmed | Ballotpedia: "out of 150,010 elections in Ballotpedia's coverage scope, 734 elections were decided b |
| [F] F-44 | §9 | corrected | Ballotpedia: "496 by fewer than five votes" (line 234) |
| [F] F-45 | §9 | confirmed | Ballotpedia: "104 decided by a single vote" (line 234) |
| [F] F-46 | §9 | confirmed | Ballotpedia: smallest total vote count 13, a 2024 Constitution Party primary in SC-4, 8 to 5 (line 2 |
| [F] F-47 | §9 | corrected | Ballotpedia: largest visible total 23,525 (a 2022 Massachusetts House race) (line 234) |
| [F] F-48 | §9 | confirmed | Ballotpedia: "most visible rows are local or school-board races" (line 234) |
| [F] F-49 | §9 | confirmed | Ballotpedia prints the share as "0.004%"; 734 / 150,010 = 0.49% (line 234; §10.3 item 6) |
| [F] F-50 | §9 | confirmed | Ballotpedia says "the 660 elections" in one place (line 234; §10.3 item 6) |
| [F] F-51 | §9 | confirmed | "The page does not define its coverage scope or its method of finding races" (line 234) |
| [F] F-52 | §9 | corrected | Ballotpedia table and text: consistency (added, not in the first pass) |
| [F] F-53 | §9 | unread | [measured] exact small-N decisiveness table (binomial 1/sqrt(2 pi N); Beta-binomial) and its Reading |
| [F] F-54 | §9 | unread | "a school-board seat decided by 5,000 voters has a probability about 2,000 times that of a national  |
| [A] A-26 | §10 | corrected | The tie constant: GKB extract "(2/sqrt(pi))*(1/sqrt(n_j))" versus my exact 1/sqrt(2 pi N) for Q (vot |
| [B] B-45 | §10 | unread | "McCune & Graham-Squire (Scottish STV): 'on the order of 1-4% for each type' in the introduction ver |
| [C] C-45 | §10 | corrected | L&T: "within-party pivotality is 0.006 in Table 2 but 0.028 in Table A1; the minimum municipal popul |
| [C] C-46 | §10 | corrected | BSW shortfall: "13,435 votes in the provisional count (Stuttgarter Zeitung) and 4,277 more votes in  |
| [E] E-46 | §10 | confirmed | line 252: "(1.6% of 182 US elections in the empirical count; 62 of 1,079 Scottish STV elections; 15% |
| [E] E-47 | §10 | confirmed | item 2: "How often non-monotonicity matters": O&N 15% to 51%; G-S&M 1.6% of 182; (McCune & GS about  |
| [E] E-48 | §10 | corrected | item 3: "Graham-Squire & McCune internal inconsistencies (extractor): Table 7 prints 52.5% ... 95 of |
| [E] E-49 | §10 | corrected | item 4: "Baltz's simulated probabilities (about 1e-7 for plurality and 1e-6 for IRV at 1,000 voters) |
| [F] F-55 | §10 | confirmed | §10.3 item 6: Ballotpedia prints "0.004%" but 734 / 150,010 = 0.49%; "the 660 elections" and "734" w |
| [F] F-56 | §10 | corrected | §10.3 item 7: Farber average election size "50 to 75 eligible voters" (Sec. 1.2) versus "from 24 to  |
| [A] F-1 | fill | confirmed | Mebane, Baltz & Vasselai (2019), "Using agent-based models to simulate strategic behavior in electio |
| [A] F-2a | fill | corrected | Myerson (1998), "Population uncertainty and Poisson games", Int. J. Game Theory 27: definition of a  |
| [A] F-2b | fill | unread | Myerson (2000), "Large Poisson Games", J. Econ. Theory: pivot event; magnitude; orders of ties |
| [A] F-2c | fill | unread | Myerson & Weber (1993), "A theory of voting equilibria", APSR |
| [A] F-3a | fill | unread | Cox (1994), APSR 88(3):608-621: the "M + 1 rule" and which candidates' votes can be pivotal |
| [A] F-3b | fill | unread | Cox (1997), Making Votes Count, ch. 7 |
| [A] F-4a | fill | confirmed | Myatt (2007), "On the theory of strategic voting", Rev. Econ. Stud. 74(1): 255-281: statements on 1/ |
| [A] F-4b | fill | unread | Chamberlain & Rothschild (1981), "A note on the probability of casting a decisive vote", J. Econ. Th |
| [A] F-4c | fill | unread | Good & Mayer (1975), "Estimating the efficacy of a vote", Behavioral Science 20: 25-33 |
| [A] F-5 | fill | confirmed | Anything else the sources cite as *the* derivation of the plurality pivot probability for 3+ candida |
| [B] F-01 | fill | confirmed | Droop quota and how an STV count is done (transfers, surplus, exclusion) |
| [B] F-02 | fill | other | Bouton (AER 2013) journal version and Bouton & Gratton: open copies; closed forms |
| [B] F-03 | fill | none-found | Any published estimate of a decisive-vote probability in a real two-round or STV election |
| [B] F-04 | fill | confirmed | ACE Electoral Knowledge Network: what a runoff is; thresholds (50%+1 etc.) |
| [C] F-1 | fill | confirmed | IDEA electoral-system design handbook: PR formulas (D'Hondt, Sainte-Laguë, modified Sainte-Laguë, Ha |
| [C] F-2 | fill | confirmed | Droop quota statement from an electoral authority (for list PR; shared with B's STV item) |
| [C] F-3 | fill | unread | Any published estimate of the probability that one vote changes a seat in a real PR election other t |
| [C] F-4 | fill | unread | Whether divisor methods are monotone in votes (a party never loses a seat from gaining votes, others |
| [D] F-1 | fill | other | The pivotal-voter condition under a participation quorum or an approval quorum (open sources) |
| [D] F-2 | fill | none-found | Published estimates of a decisive-vote probability in a real referendum (any country), under a real  |
| [D] F-3 | fill | other | Italian referendum quorum outcomes (turnout versus the 50%+1 requirement), from an official source |
| [D] F-4 | fill | other | An open, official dataset of primary margins |
| [E] F-1 | fill | confirmed | Baltz supplement (baltz_sup): what it contains, and whether it lets the 10^-6 / 10^-7 values be reco |
| [E] F-2 | fill | unread | The published (journal) version of Baltz, Political Analysis 33(4): differences visible through the  |
| [E] F-3a | fill | confirmed | Other source cited as a derivation of monotonicity-failure frequency: Allard (1996), read |
| [E] F-3b | fill | confirmed | The same Allard result is disputed on rangevoting.org (different source, an advocacy site) |
| [E] F-3c | fill | unread | Other cited derivations: not read |
| [F] FILL F-1 | fill | none-found | Any published estimate of the probability that one vote decides control of a legislative chamber (no |
| [F] FILL F-2 | fill | none-found | Any published estimate of the probability a vote is decisive in a real small local election (school  |
| [F] FILL F-3 | fill | confirmed | Mulligan & Hunter (2003) "The empirical frequency of a pivotal vote", Public Choice 116: abstract; " |

## 0. How this was read

**Access.** R4 step 1: on 2026-11-07 00:10 UTC `curl -sSL` returned HTTP 200 for `sites.stat.columbia.edu` and `plato.stanford.edu` (the first pass was refused every host it tried; the network has been opened). The orchestrating worker then fetched 34 of the first pass's source URLs into a scratch directory outside the repository and converted PDFs with `pdftotext` (layout and reading-order versions) so that six readers could work from the same copies. Results: 28 returned HTTP 200, two of those were bot-challenge pages (`link.springer.com`: Client Challenge; two papers), and six failed: `electionresults.govt.nz` (Cloudflare "Attention Required", 403), `core.ac.uk` (Cloudflare "Just a moment", 403; two papers), `mta-sts.hcourt.gov.au` (the first pass's URL now returns a 404 page), `legislationline.org` (the first pass's URL now serves an unrelated page), and the Luechinger et al. URL on `core-prod.cambridgecore.org` (proxy 502; the same open-access PDF was read at `www.cambridge.org`, DOI `10.1017/pan.2023.22`). Cambridge items the readers could not fetch were fetched by the orchestrating worker (Luechinger et al.; the quorum docx; the Baltz journal page, which has the abstract and citation but not the text; the Aguiar-Conraria page, which is paywalled: "Get access"). **No bot check was circumvented** (`_COMMON.md` 6). Where a legitimate other copy of the same text was read, the block says which copy and which version (for example the author's PDF of Gelman, King & Boscardin (1998) on `sites.stat.columbia.edu`, in place of the `core.ac.uk` copy the first pass cited).

**Who read what.** Reader A: §1, Myatt & Fisher, Gelman-Katz-Bafumi 2004, the decomposition formula of Gelman-King-Boscardin 1998, the Myerson, Cox, Mebane and Myatt 2007 leads. Reader B: §2 and §5, Bouton, France, Lepelley et al., the Scottish STV paper, Laird et al., AEC v Johnston, Droop. Reader C: §4. Reader D: §6 and §7. Reader E: §3, Baltz whole, Ornstein & Norman, Graham-Squire & McCune, Allard. Reader F: §8 and §9, Ordeshook & Zeng. The orchestrating worker: all downloads and Cambridge fetches, the Appendix A re-run, the quote checker, the table of corrections, and the independent spot checks listed below.

**Marks.** *confirmed*: the source says it (URL, location, short exact quote). *corrected*: the right value or wording is given, with the source. *unread*: with the reason. The project's grade tags: [stated] a source says it (where); [measured] computed (how shown); [inferred] a reading. A reader's own computation is [measured] and is not a source. A block whose MARK reads "confirmed with a correction" is counted as a correction in the table.

**Checks the orchestrating worker made itself, beyond the readers' own.** (1) Every `QUOTE[file]: "..."` line was checked by script against the extracted text file it names, whitespace collapsed, ellipses splitting a quote into segments that must each be found: 759 quotes, 758 found by script, one inside an HTML attribute found by `grep`, none missing. (2) The constant in Gelman-Katz-Bafumi 2004 was read on the page image (p. 662 text and p. 663, Sec. 2.3), and the "1.84" arithmetic was redone (A-15). (3) The BSW arithmetic was redone from the final totals (C-39). (4) The Myatt & Fisher Lemma 1 constant was checked by hand under a uniform belief (A-06). (5) `grep` of the sources: Herrera & Mattozzi contain no "pivot" and no "decisive"; Foellmi et al. contain no "Swiss"; the Cooper & Munger page has no "varied widely"; the Ballotpedia page prints "(0.004%)", "the 660 elections", 150,010, 734, and its table has 393,922 and 23,525 as totals. (6) The Baltz journal page was read for the abstract and the citation (Political Analysis 33(4), October 2025, pp. 447-455). (7) All seven scripts of Appendix A were re-run.

**Lower-grade facts** are those read only through WebFetch (a small model's extract; each such block says so): B-41 to B-43 (AEC v Johnston), B-44 and B fill F-01 and F-04 (ACE), F-04 to F-06 and F fill F-1 (538, a data dictionary on a mirror, Princeton Election Consortium).

**Reader notes on the reading itself** follow, verbatim from the reader files, with the headings lowered. They give what each reader could and could not reach, requests made, and problems with the instructions (collected also in the digest).

### Reader A: notes on the reading

Scope: first-pass `/home/user/vote/research/electoral-systems.md` lines 16-49 (§1), the Baltz sentence in line 27 (as to what it attributes to Mebane et al.), line 273 (§10.3 item 1), and the formula/figure checks that task A owns in lines 186, 200, 201, 205 (Gelman, King & Boscardin 1998; Gelman, Katz & Bafumi 2004).

SP = /tmp/claude-0/-home-user-vote/f871403b-c3f2-5a5c-a451-59fb99a51e77/scratchpad

How I read (all by curl-downloaded files already in SP/r4; no new requests made for these):
- Myatt & Fisher (Oxford DP 115) = `myatt_fisher` (`.raw.txt` for quotes). Equations, Proposition 1, Lemma 1, Table 1 and Eq. 4/5 were read from page images (pdftoppm, printed pages 6-9 = PDF pages 7-10; Table 1 re-rendered at 250 dpi).
- Gelman, Katz & Bafumi (BJPS 2004) = `gkb2004` (`.raw.txt`). The text layer loses radicals, pi, Greek letters and minus signs, so every formula below was read from the page images (PDF pages 6, 7, 11, 12, 18; Fig. 3 re-rendered at 300 dpi and rotated).
- Gelman, King & Boscardin (JASA 1998) = `gkb1998_columbia` (the author's PDF on sites.stat.columbia.edu, which carries the JASA running heads, "March 1998, Vol. 93, No. 441"). Its text layer interleaves the two columns, so I quote only fragments that lie inside one text line. Equations (1)-(3), (5) and the section numbers were read from page images (PDF pages 3, 5, 6).
- The first pass cited `https://core.ac.uk/download/28933611.pdf` for GKB 1998; that copy was not what I read (core.ac.uk is a different task's host and the local `gkb1998.out` is a 5 KB challenge page). What I read is the author's copy, named as such in each block.

Grade tags: [stated] a source says it (where); [measured] I computed it (how shown); [inferred] my reading.

---

### Reader B: notes on the reading

SP = /tmp/claude-0/-home-user-vote/f871403b-c3f2-5a5c-a451-59fb99a51e77/scratchpad. Local file names in QUOTE[...] are in SP/r4/txt/ unless they start with `dl/` or are marked `work-B`, in which case they are in SP/r4/work-B/ (I downloaded those myself; their URLs are given on the SOURCE line). Check script: SP/r4/work-B/checkq.py (looks in SP/r4/txt/, SP/r4/work-B/ and SP/r4/work-B/dl/).

Request log (for the orchestrator; hosts outside my task list were used only for fill items or to find an open copy): conseil-constitutionnel.fr (3 requests: 1 connection reset, 2 OK), info.gouv.fr (1: 403 Cloudflare, stopped), link.springer.com (1 extra, Client Challenge, stopped), hcourt.gov.au (3 curl attempts within a minute: HTTP/2 INTERNAL_ERROR / empty reply, then stopped; WebFetch used instead and flagged), aceproject.org (8 curl requests over 3 minutes: 404 and 503 site-error pages; then WebFetch, flagged), electoralcommission.ie (2 OK), electoralcommission.org.uk (1: 403, stopped), legislation.gov.uk (1 OK), econpapers.repec.org (4 OK), econtheory.org / econometricsociety.org (1 OK), api.crossref.org (2 OK), kops.uni-konstanz.de (1 OK), votingmatters.org.uk (2: 1 OK, 1 reset), ssoar.info (1: Anubis, stopped), data.gesis.org (1: 404), icms.org.uk (1: proxy 502, stopped). No request carried a contact detail; User-Agent "Mozilla/5.0 (research; vote-site project)" throughout. Note for the orchestrator: the common file says WebFetch only when curl is "refused"; for hcourt (empty replies) and ACE (404/503 error pages) curl was not refused in the sense of a bot check, it just failed; I used WebFetch there and say so on every fact.

Reading notes common to the Bouton blocks: the file `bouton.txt` is `pdftotext -layout` of the PDF at the Penn URL (47 pages, pdfTeX, PDF CreationDate 20 Feb 2012). The font loses minus signs, "ff" and "fi" ligatures (the file prints "runo¤" for "runoff" and "…rst" for "first") and replaces "/" in event names by "=" (the file prints `pivi=ij`; the page image prints `piv^1_{i/ij}`). Every formula below was decided from page images (pdftoppm -r 120..220, pdf page numbers given; pdf page = printed page + 1).

---

### Reader C: notes on the reading

Reader: subagent C (Sonnet 5.5). Written to SP/r4/out/C.md, SP = /tmp/claude-0/-home-user-vote/f871403b-c3f2-5a5c-a451-59fb99a51e77/scratchpad.

How to check the quotes: each QUOTE names its file. Files without a prefix are in SP/r4/txt/ (lyyt.txt, luechinger.raw.txt). Files with the prefix `work-C/` are in SP/r4/work-C/ (plain-text conversions I made of the HTML pages with SP/r4/work-C/h2t.py, and of PDFs/HTML I downloaded myself into SP/r4/work-C/dl/, with copies at the top of work-C/). Quotes were collapsed to single spaces and checked with SP/r4/work-C/qcheck.py (every QUOTE line found in its file; 0 missing at the time of writing).

Notes on my instructions (rule 11): (1) The "collapse line breaks to single spaces" rule turns a hyphen or en-dash line break such as "Hare-" / "Niemeyer" into "Hare- Niemeyer", which is not in the original; I avoided quotes that span such breaks. (2) F-3 and F-4 ask for reading papers that live on hosts outside my allowed list; I searched (URLs only) and report leads as unread. (3) The task text says the Luechinger file is "pending"; it arrived (txt/luechinger.txt, luechinger.raw.txt) and I used it. (4) Grade tags: [stated] a source says it; [measured] I computed it (script named); [inferred] my reading.

### Reader D: notes on the reading

First-pass file: `/home/user/vote/research/electoral-systems.md` (lines 152-193, 280, 283).
SP = `/tmp/claude-0/-home-user-vote/f871403b-c3f2-5a5c-a451-59fb99a51e77/scratchpad`.
Quote files: a bare name such as `herrera.txt` is in `SP/r4/txt/`; a name beginning `work-D/` is in `SP/r4/work-D/` (files I made from pages I fetched: text of an HTML page via a tag-stripping script, or `pdftotext -layout`).
WebFetch was not used for any fact below; every page was read with curl (or `pdftotext`/`pandoc`). WebSearch was used only to find URLs.

##### 0. Read this first (what I could and could not reach, and what looks wrong in my instructions)

1. **The text of Aguiar-Conraria, Magalhaes & Vanberg could not be read.** `core.ac.uk` is a Cloudflare challenge (task file). Every legitimate other copy I tried refused or failed: `wp.nipe.eeg.uminho.pt` (proxy refused: 502 on CONNECT), `repositorium.sdum.uminho.pt` and `nipe.eeg.uminho.pt` (connection reset), `www3.eeg.uminho.pt` (the "File URL" that IDEAS lists for the working paper; 503 "upstream connect error ... connection timeout"), `www.rcaap.pt` (reset), the Heidelberg repository `archiv.ub.uni-heidelberg.de` (Anubis "Making sure you're not a bot" page: not circumvented). I stopped at the first refusal on each host. What I *did* read: the IDEAS abstract pages (working paper and journal version) and, via the orchestrating thread's download, the online-resource docx `Appendix 1-3` (`quorum_docx.txt`). So Sec. 2 quotes, Sec. 4.1 turnout figures and the Introduction/Sec. 4.3/Sec. 5 boycott statements are **unread**; the Appendix 1 formulas are **read**.
2. **The task file says the published version is "Journal of Public Economics 2016". It is not, per IDEAS: Experimental Economics 19(4), pp. 886-909, December 2016, DOI 10.1007/s10683-015-9473-9** (D-05). The working paper is NIPE WP 14/2013. The docx is the online resource of the Cambridge-hosted article id `S1386415716010267`; the ISSN part (1386-4157) is Experimental Economics' [inferred]. The docx's own text and metadata (creator "Kasthuri M.", created 2015-11-02) do not name the paper; its content (9 electors, costs uniform on 0 to 100, participation quorum 4, approval quorum 3, a 48-round lab session) matches the lab design the first pass attributes to this paper.
3. **"As printed from the page image" was not possible for the Appendix 1 equations.** The docx has no page image: LibreOffice's PDF render of it leaves the equations blank (I looked at pages 1-2 of the render). I transcribed from the Word equation XML (OMML) via `pandoc -t latex` (output `work-D/docxconv/quorum_pandoc.tex`) and checked it against the orchestrating thread's flattened text `quorum_docx.txt`. The symbols are therefore from equation markup, not from a page image. The Herrera & Mattozzi formula and the Gelman-King-Boscardin equations were checked on rendered page images.
4. **Official UK and Italian sources:** `electoralcommission.org.uk`, `commonslibrary.parliament.uk` and `researchbriefings.files.parliament.uk` all answered 403 with the Cloudflare "Just a moment" page; `www.senato.it` answered 202 with an AWS WAF challenge (`x-amzn-waf-action: challenge`) on two URLs; `elezionistorico.interno.gov.it` answered 403 "Access Denied". Not circumvented. For Article 75 I used the Constitutional Court's English text (reachable); for Italian turnout the Ministry of the Interior's own dossiers on `dait.interno.gov.it` (reachable).
5. Hosts I touched that are not in my task file's list: `www.rcaap.pt`, `www3.eeg.uminho.pt` (same university as the listed ones, the URL IDEAS gives), `archiv.ub.uni-heidelberg.de`, `www.cirje.e.u-tokyo.ac.jp` (one PDF, Hizen's other paper), `dait.interno.gov.it` (Ministry of the Interior; the task names the ministry), `historical.elections.virginia.gov` and `va2.elstats.civera.com` (F-4). One or two requests each, spaced at least 3 seconds. None of them is named in another subagent's task file as far as I could see.
6. Every instruction in common.md and task-D.md carried its reason except these: task-D item 1's "Journal of Public Economics 2016" (a wrong fact, see 2) and the instruction to read Aguiar-Conraria "from the page image" for a docx (no page image exists, see 3).

---

### Reader E: notes on the reading

SP = /tmp/claude-0/-home-user-vote/f871403b-c3f2-5a5c-a451-59fb99a51e77/scratchpad. First-pass file: /home/user/vote/research/electoral-systems.md (lines 71-96, 27, 31, 274-276, §10.1).

##### How this was read (facts about the reading itself)

- Every source below was read from a file already downloaded by curl (no WebFetch used by me). Local files: `baltz_arxiv.raw.txt` / `baltz_arxiv.txt` (pdftotext of the arXiv PDF; the PDF's own first-page stamp reads "arXiv:2210.01657v2 [cs.GT] 31 Jul 2023", 28 pages, ends with the reference list; it contains NO appendix), `baltz_sup.raw.txt` / `baltz_sup.txt` (the supplement, 24 pages, headed "Appendix", dated "September 4, 2024"), `ornstein.raw.txt` (Springer-typeset PDF, Public Choice 161:1-9, copy at rangevoting.org), `gs_mccune.raw.txt` / `gs_mccune.txt` (the PDF's own stamp reads "arXiv:2301.12075v2 [econ.GN] 6 Mar 2023", 16 pages; so the file is **v2**).
- Baltz's formulas: I rendered pages 7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20 of the arXiv PDF and pages 8, 12, 18 of the supplement to PNG (`pdftoppm -r 110/130`) and looked at them. The formulas under FORMULAS AS PRINTED are transcribed from those images, not from the text extract. Figure 1 of both versions I looked at as images (arXiv page 24, supplement page 18; the embedded images were also extracted with `pdfimages`).
- Extra: one source cited by O&N (Allard 1996) turned out to be reachable at votingmatters.org.uk (one request, HTTP 200, saved to `SP/r4/work-E/allard/p1.out`, text version `allard.txt`). Nothing else was requested from any host.
- Computations (grade [measured]) are in `SP/r4/work-E/` (`skellam.py`, `ex.py`, `ex2.py`, `smdp.py`, `exact3.py`); numpy only, run with `python3 -I`.
- Where a block says "confirmed" for an attribution that the first pass put inside quotation marks but which is a paraphrase, I say so in NOTE; quotes in the QUOTE lines are exact.
- Nothing here is from memory; where I name a thing I did not read, it is in STILL UNREAD.

---

### Reader F: notes on the reading

Reader: subagent F (R4 worker thread, vote-importance project). Date read: 2026-11-07. First-pass file: /home/user/vote/research/electoral-systems.md lines 146, 195-249, 278-279.

How to read this file
- Block labels: F-01 to F-56 are the first-pass facts (regular blocks); "FILL F-1" to "FILL F-3" are the fill items of the task file (labelled so they do not collide with F-01..; FILL F-4 is Gelman, Silver & Edlin, listed under NEED-FETCH as the task file says).
- QUOTE[name]: name is a file under /tmp/claude-0/-home-user-vote/f871403b-c3f2-5a5c-a451-59fb99a51e77/scratchpad/r4/ . A bare name (farber.txt, gkb2004.raw.txt, gkb1998_columbia.raw.txt, lyyt.txt, ballotpedia10.html) is in r4/txt/ ; a name starting work-F/ is a file I made in r4/work-F/ (PDFs I downloaded and converted with pdftotext, HTML pages I downloaded, and tag-stripped text of HTML pages). Every QUOTE was copied by a script from the named file (whitespace collapsed) and the script reported zero misses.
- Two kinds of local file need care. (1) work-F/webfetch_fte.txt and work-F/webfetch_datahub.txt are WebFetch outputs (a small model's extract), saved verbatim; a quote from them proves only what WebFetch returned, not what the page says. WebFetch was used for those because curl could not reach the text (reasons in F-04, F-07, FILL F-1). (2) work-F/ballotpedia10.plain.txt is my tag-stripped copy of the saved HTML (txt/ballotpedia10.html), table cells joined by " | ".
- Page images: where a formula was needed I rendered the PDF page and looked at the image (pdftoppm; files in r4/work-F/: farber_p-17.png, farber_p-18.png, gkb98p-3.png, gkb98p6-6.png, gkb04p-06.png, gkb04p-07.png, gkt-08.png). Formulas are transcribed under FORMULAS AS PRINTED.
- Hosts requested (one to three requests each, 3-4 seconds apart, no bursts, stopped at the first refusal): authors.library.caltech.edu, nber.org, fivethirtyeight.com and projects.fivethirtyeight.com (both answered 301/302 redirects to ABC News), ballotpedia.org, github.com and raw.githubusercontent.com (403 / 404), archive.org and web.archive.org (the availability API worked, the snapshot page was refused: connection reset), econpapers.repec.org, election.princeton.edu, datahub.io (404), papers.ssrn.com (403 challenge), votehub.com (403 challenge), cesifo.org (challenge page instead of PDF). WebFetch hosts: fivethirtyeight.com, datahub.io (both worked), web.archive.org (blocked by the tool), projects.fivethirtyeight.com CSV (robots_disallowed).

## 1. Plurality, three or more candidates

*First-pass lines 16-49 of `research/electoral-systems.md`. Each block: the first-pass claim with its line number, the mark, the source and location, exact quotes, the correction if any, notes.*

#### [A] A-01 | §1 | "What decisive means": with 3+ candidates a vote is decisive only if, among the other voters, the leaders are tied or one vote apart; it is a tie/one-vote gap for first place between two candidates, rest behind; ties for lower places do not change the plurality winner (L18) [inferred from Myatt & Fisher]
MARK: confirmed (the part that M&F state), with two notes
SOURCE: https://ora.ox.ac.uk/objects/uuid:adeb8fa9-899c-4fbe-9594-5574db9c4d24/files/sv979v3563 (local: myatt_fisher.raw.txt) ; Sec. 1 p. 2 and Sec. 2.3 p. 7, Table 1 p. 8
QUOTE[myatt_fisher.raw.txt]: "The only circumstance in which a voter can influence the outcome is when the votes of all the other electors produce a tie or near-tie for the lead."
QUOTE[myatt_fisher.raw.txt]: "A near tie is a situation in which there is a winning margin of a single vote, and a single additional vote may create a tie and prevent an outright win by the leader."
NOTE: [stated] M&F define the pivotal event as a tie or near tie *for the lead* (near tie = winning margin of one vote). [inferred] "Ties for lower places do not change the winner" is the first pass's own reading; it is consistent with M&F's Table 1 (every one of its 16 pivotal events is a tie or one-vote gap for the lead), but M&F do not say it in those words. Two additions the first-pass line leaves out: (1) M&F's pivotal events for m = 3 include *three-way* ties and near three-way ties, not only "two candidates tied, rest behind" (Table 1, rows 1-4, 8, 11, 14); they are asymptotically negligible (see A-07/A-08), not impossible. (2) M&F's "near tie" for the lead also includes a one-vote lead over a *trailing-by-one* third candidate (e.g. x1 - 1 = x3 > x2, which is pivotal only for a vote for candidate 3); M&F call these events "irrelevant" for the 1-vs-2 choice (p. 8). The model in M&F has n + 1 voters with *no abstentions*, ties broken at random, so "decisive" there means a vote for 1 versus a vote for 2 (A-04 note).

#### [A] A-02 | §1 | Citation: Myatt & Fisher, "Everything Is Uncertain and Uncertainty Is Everything: Strategic Voting in Simple Plurality Elections", Oxford Dept of Economics Discussion Paper 115, July 2002, at the ORA URL (L21)
MARK: confirmed
SOURCE: https://ora.ox.ac.uk/objects/uuid:adeb8fa9-899c-4fbe-9594-5574db9c4d24/files/sv979v3563 (local: myatt_fisher.raw.txt) ; title page and p. 1
QUOTE[myatt_fisher.raw.txt]: "EVERYTHING IS UNCERTAIN AND UNCERTAINTY IS EVERYTHING: STRATEGIC VOTING IN SIMPLE PLURALITY ELECTIONS"
QUOTE[myatt_fisher.raw.txt]: "Number 115"
QUOTE[myatt_fisher.raw.txt]: "July 2002"
NOTE: Authors "David P. Myatt and Stephen D. Fisher". The file was downloaded by curl (not WebFetch). The PDF is 37 pages (pdfinfo); the paper body runs to printed p. 30+ with Appendices A-C. First pass said "read by WebFetch"; it has now been read raw.

#### [A] A-03 | §1 | Pivotal event quote: "She may only influence the identity of the winner in the context of a pivotal event" (Sec. 2.3, p. 7), concretely "a tie or near tie for the lead" (L22)
MARK: confirmed
SOURCE: https://ora.ox.ac.uk/objects/uuid:adeb8fa9-899c-4fbe-9594-5574db9c4d24/files/sv979v3563 (local: myatt_fisher.raw.txt) ; Sec. 2.3, printed p. 7
QUOTE[myatt_fisher.raw.txt]: "She may only influence the identity of the winner in the context of a pivotal event: There must be a tie or near tie for the lead."
NOTE: Section and printed page number as claimed (checked on the page image). The first-pass words "a tie or near tie for the lead" are a substring of the quoted sentence ("There must be a tie or near tie for the lead").

#### [A] A-04 | §1 | Eq. 1: Pr[x] = integral Pr[x|p] f(p) dp = (n!/prod x_j!) integral prod p_j^{x_j} f(p) dp; x_j votes for candidate j; n = number of *other* voters; p = vector of true support; f(p) the voter's density over p (L23)
MARK: confirmed (formula and definitions); one wording correction on "true support"
SOURCE: https://ora.ox.ac.uk/objects/uuid:adeb8fa9-899c-4fbe-9594-5574db9c4d24/files/sv979v3563 (local: myatt_fisher.raw.txt) ; Sec. 2.1 p. 5, Sec. 2.2 p. 6, Eq. (1), read on the page image (PDF p. 7)
QUOTE[myatt_fisher.raw.txt]: "Among these other n individuals, we use xj to denote the number of votes cast for candidate"
QUOTE[myatt_fisher.raw.txt]: "Uncertainty over p is represented by the density f (p)."
QUOTE[myatt_fisher.raw.txt]: "Conditional on p, the outcome x is multinomial with parameters p and n."
CORRECTION (wording only): "p the vector of true support" -> M&F say p "represents the constituency support for the m candidates" (Sec. 2.1) and, in Sec. 2.2's discussion, "the likely voting *intentions* of the wider electorate and not necessarily their preferences": each other voter independently votes for j with probability p_j; p is *unknown* to voter 0, who has the belief density f(p) on the simplex.
CORRECTION (what Eq. 1 is, as printed, p. 6): Pr[x] = ∫_△ Pr[x | p] f(p) dp = ∫_△ (n!/∏_{j=1}^m x_j!) ∏_{j=1}^m p_j^{x_j} f(p) dp = (n!/∏_{j=1}^m x_j!) ∫_△ ∏_{j=1}^m p_j^{x_j} f(p) dp   (1)
NOTE: Setup as printed: single-seat plurality, m candidates; n + 1 individuals, voter i = 0 is the instrumental voter, the other n are exogenous; "Each individual casts a single vote, and there are no abstentions"; ties "broken at random". x ∈ X = {x ∈ Z^m_+ | Σ x_j = n}; △ is the (m-1)-dimensional unit simplex; f is "continuous and strictly positive on the interior of △".

#### [A] A-05 | §1 | Proposition 1 (Sec. 2.2, p. 7): Pr[x] ≈ f(x/n) times 1/n^{m-1}, m = number of candidates (L24)
MARK: confirmed
SOURCE: https://ora.ox.ac.uk/objects/uuid:adeb8fa9-899c-4fbe-9594-5574db9c4d24/files/sv979v3563 (local: myatt_fisher.raw.txt) ; Sec. 2.2, printed p. 7, Proposition 1; proof of Prop. 1 in Appendix A (printed pp. 28-29); page image read (PDF p. 8)
QUOTE[myatt_fisher.raw.txt]: "Proposition 1. In a large electorate, Pr[x] is proportional to f (x/n). Formally:"
QUOTE[myatt_fisher.raw.txt]: "so that, in a large electorate, likelihood ratios are determined entirely by the density f (p)."
QUOTE[myatt_fisher.raw.txt]: "are integers. Recalling that Γ(n + 1) = n! and Γ(n + m) = (n + m − 1)!:"
NOTE: As printed (image): Pr[x] ≈_{n→∞} f(x/n) · (n!/∏_{j=1}^m x_j!) ∫_△ ∏_{j=1}^m p_j^{x_j} dp = (1/n^{m−1}) f(x/n)  ⇒  Pr[x]/Pr[x̃] ≈_{n→∞} f(x/n)/f(x̃/n). m is the number of candidates (Sec. 2.1: "A single seat plurality election is contested by m candidates"). So "approximately f(x/n) times 1/n^(m-1)" is what is printed. The "≈" is Definition 1 (p. 6): g ≈ h iff max_x g/h and min_x g/h both → 1 as n → ∞ (uniform in x ∈ X). The middle "=" is exact only up to n!/(n+m-1)! vs 1/n^{m-1}: the Appendix proof (p. 29) writes Γ(n+1)/Γ(n+m) = 1/∏_{k=1}^{m-1}(n+k) ≈ 1/n^{m-1}. [inferred] f is a density with respect to Lebesgue measure on (p_1,...,p_{m-1}) (the Dirichlet kernel step), which is what makes the constant exactly 1/n^{m-1}; checked in A-06 with a uniform f = 2.

#### [A] A-06 | §1 | Lemma 1 (Sec. 2.3, pp. 8-9): two-way near-tie probability of order 1/n; three-way tie Pr[x1=x2=x3+1] ≈ (1/n²) f(1/3,1/3,1/3) (L25)
MARK: confirmed as to orders in n and the three-way formula; **corrected as to what the exact printed statement is, and one printed constant (the "6") does not follow from Proposition 1**
SOURCE: https://ora.ox.ac.uk/objects/uuid:adeb8fa9-899c-4fbe-9594-5574db9c4d24/files/sv979v3563 (local: myatt_fisher.raw.txt) ; Lemma 1, Eqs. (2)-(3), printed pp. 8-9 (page images PDF pp. 9-10); proof in Appendix A, printed p. 29
QUOTE[myatt_fisher.raw.txt]: "Lemma 1. Two-way and near two-way ties are asymptotically equivalent; for instance:"
QUOTE[myatt_fisher.raw.txt]: "with similar expressions available for Pr[x1 = x3 > x2 ] and Pr[x2 = x3 > x1 ]. Three way and near"
QUOTE[myatt_fisher.raw.txt]: "where the first equivalence applies for (n − 1)/3 ∈ N and the second for n/3 ∈ N."
QUOTE[myatt_fisher.raw.txt]: "The sum on the right hand side has approximately n/6 elements. Multiplying and dividing by 6,"
CORRECTION (exact statement, as printed, from the image):
  Eq. (2): Pr[x1 − 1 = x2 > x3] ≈_{n→∞} ( ∫_{1/3}^{1/2} f(z, z, 1 − 2z) dz ) / (6n) ≈_{n→∞} Pr[x1 = x2 > x3 + 1]   "with similar expressions available for Pr[x1 = x3 > x2] and Pr[x2 = x3 > x1]".
  Eq. (3): Pr[x1 = x2 = x3 + 1] ≈_{n→∞} (1/n²) f(1/3, 1/3, 1/3) ≈_{n→∞} Pr[x1 = x2 = x3]   "where the first equivalence applies for (n − 1)/3 ∈ N and the second for n/3 ∈ N."
  m in Lemma 1 is not a symbol: Lemma 1 is for the three-candidate case (m = 3); the n^{-(m-1)} of Proposition 1 gives n^{-2} per outcome; the two-way tie sums n/6 outcomes (x1 = x2 = i for n/3 < i ≤ n/2), which turns n^{-2} into n^{-1}.
  So "two-way near-tie of order 1/n" and "three-way tie ≈ (1/n²) f(1/3,1/3,1/3)" are as printed. The first pass's "possibly garbled" caveat can be dropped for these.
NOTE (printed constant, [measured]): the "6" in Eq. (2) does not agree with Proposition 1 / Eq. (3). With a uniform belief (f ≡ 2 on the simplex in (p1,p2) coordinates, i.e. Dirichlet(1,1,1)), every outcome x of n voters is equally likely, so Pr[x1 = x2 > x3] = #{i : n/3 < i ≤ n/2} / C(n+2,2). Computed exactly (script SP/r4/work-A/calc2.py): n·Pr = 0.33003, 0.33300, 0.33330 at n = 300, 3000, 30000, which tends to ∫f dz = 1/3, **not** ∫f dz / 6 = 0.0556; while n²·Pr[x1=x2=x3] = 1.980, 1.998, 1.9998 → f(1/3,1/3,1/3) = 2, matching Eq. (3). The Appendix proof (printed p. 29) writes "(1/6)(1/(n/6)) Σ f(...) → (1/6) ∫_{1/3}^{1/2} f(z,z,1−2z) dz", dropping the factor 6 that turns an average over an interval of length 1/6 into the integral. [inferred] This is an arithmetic slip in the paper; it changes no order in n and no conclusion of Prop. 2 (the 6 cancels in the ratios p12, p13, p23), but a site must not copy "6n" as a constant. Also [measured]: the event x1 = x2 = x3 + 1 exists only when n ≡ 2 (mod 3), i.e. (n − 2)/3 ∈ N, not (n − 1)/3 as printed (the printed condition fits x1 = x2 = x3 − 1).

#### [A] A-07 | §1 | Quote: "the probability of a three-way tie vanishes at rate n^-2, whereas the probability of a two-way tie vanishes at rate n^-1" (Sec. 2.3, p. 9) (L25)
MARK: confirmed
SOURCE: https://ora.ox.ac.uk/objects/uuid:adeb8fa9-899c-4fbe-9594-5574db9c4d24/files/sv979v3563 (local: myatt_fisher.raw.txt) ; Sec. 2.3, printed p. 9, directly after Lemma 1
QUOTE[myatt_fisher.raw.txt]: "however, that the probability of a three-way tie vanishes at rate n−2 , whereas the probability of a two-way tie vanishes at rate n−1 , and so three-way and near three-way ties are asymptotically"
NOTE: the printed exponents are n−2 and n−1 (Unicode minus); the first pass's "n^-2" / "n^-1" is the same content. The quote is verbatim except for the superscript rendering and the space the text layer inserts after "n−2".

#### [A] A-08 | §1 | Quote: "three-way and near three-way ties are asymptotically irrelevant to voter i = 0" (p. 9) (L25)
MARK: confirmed
SOURCE: https://ora.ox.ac.uk/objects/uuid:adeb8fa9-899c-4fbe-9594-5574db9c4d24/files/sv979v3563 (local: myatt_fisher.raw.txt) ; Sec. 2.3, printed p. 9
QUOTE[myatt_fisher.raw.txt]: "irrelevant to voter i = 0. The remaining relevant pivotal events are highlighted (“∗”) in Table 1."
QUOTE[myatt_fisher.raw.txt]: "a two-way tie vanishes at rate n−1 , and so three-way and near three-way ties are asymptotically"
NOTE: the sentence is split across a line break; the two quotes together are "...and so three-way and near three-way ties are asymptotically irrelevant to voter i = 0." "Irrelevant" is relative to the choice between candidates 1 and 2 *given* the voter's relative preferences (the optimal-voting rule, Prop. 2), because three-way ties are an order n smaller than two-way ties. M&F do not say the event is impossible, and they do not give an absolute pivot probability for a 3-candidate race: their argument is explicitly about relative probabilities ("the absolute probability of being in a pivotal situation becomes irrelevant", Sec. 1 p. 2).

#### [A] A-09 | §1 | The extractor flagged Table 1 and Eq. 4 as garbled; not reproduced (L26)
MARK: confirmed that they exist as printed; now transcribed (read from page images at 130 and 250 dpi)
SOURCE: https://ora.ox.ac.uk/objects/uuid:adeb8fa9-899c-4fbe-9594-5574db9c4d24/files/sv979v3563 (local: myatt_fisher.raw.txt) ; Table 1 printed p. 8; Eq. (4)-(5) printed p. 9 (Proposition 2)
QUOTE[myatt_fisher.raw.txt]: "TABLE 1. Pivotal Events and Voter Payoffs"
QUOTE[myatt_fisher.raw.txt]: "Proposition 2. Assuming without loss of generality that an indifferent voter i = 0 casts her vote in favor"
NOTE: full transcription of Table 1 and Eqs. (4)-(5) is in FORMULAS AS PRINTED below. Points a reader of the table needs: Table 1 lists 16 pivotal events for m = 3 (4 three-way or near-three-way ties up front, 3 "Two Way Tie" rows, then near-tie rows); seven rows carry the "∗" that marks them as relevant for the 1-versus-2 decision: the three "Two Way Tie" rows (x1 = x2 > x3 + 1, x1 = x3 > x2 + 1, x2 = x3 > x1 + 1) and four "Near Two Way Tie" rows (x1 − 1 = x2 > x3, x2 − 1 = x1 > x3, x3 − 1 = x1 > x2, x3 − 1 = x2 > x1). Two near-two-way rows (x1 − 1 = x3 > x2 and x2 − 1 = x3 > x1) have payoff difference 0 and no ∗ (the text calls them "irrelevant"). Rows for x1 = x3 = x2 + 1 and x2 = x3 = x1 + 1 print the payoff (u1+u2+u3)/2 where a uniform random tie-break among three tied candidates would give (u1+u2+u3)/3 [inferred]; these are three-way rows that the paper discards asymptotically.

#### [A] A-10 | §1 | Baltz uses, for SMDP, "the Mebane et al. (2019) derivation" with Skellam-based pivot probabilities under Poisson voting games (L27; only the attribution to Mebane et al. is mine)
MARK: confirmed (attribution); the quoted phrase is not verbatim
SOURCE: https://arxiv.org/pdf/2210.01657 (local: baltz_arxiv.raw.txt) ; footnote 5 on printed p. 23 and Sec. "Modeling the probabilities" p. 19 (arXiv version; Baltz's own content is task E's)
QUOTE[baltz_arxiv.raw.txt]: "To facilitate direct comparison, I simulate SMDP pivotal probabilities using the derivation from Mebane et al. (2019) which I extended to cover IRV."
QUOTE[baltz_arxiv.raw.txt]: "Following Mebane et al. (2019), if the number of voters is drawn from a Poisson distribution, then the number of voters with a preference ordering following each possible preference"
QUOTE[baltz_arxiv.raw.txt]: "ordering will also follow a Poisson distribution with known parameter, and their difference follows the Skellam distribution."
QUOTE[baltz_arxiv.raw.txt]: "Mebane, Jr., W. R., Baltz, S., and Vasselai, F. (2019). Using agent-based models to simulate strategic behavior in elections. Presented at the 2019 meeting of the Society for Political Methodology."
CORRECTION (wording): "the Mebane et al. (2019) derivation" -> Baltz writes "the derivation from Mebane et al. (2019)" (fn. 5) and "extending a derivation of pivotal probabilities in single-vote elections by Mebane et al. (2019)" (Sec. "Modeling the probabilities").
NOTE: Mebane et al. (2019) is cited as a conference presentation (Society for Political Methodology, 2019); see F-1 for whether it could be found.

#### [A] A-11 | §1 | Citation: Gelman, Katz & Bafumi, "Standard Voting Power Indexes Do Not Work: An Empirical Analysis", BJPS 34 (2004) 657-674, at sites.stat.columbia.edu/gelman/research/published/gelmankatzbafumi.pdf (L28)
MARK: confirmed
SOURCE: https://sites.stat.columbia.edu/gelman/research/published/gelmankatzbafumi.pdf (local: gkb2004.raw.txt) ; title page / running head
QUOTE[gkb2004.raw.txt]: "B.J.Pol.S. 34, 657–674 Copyright © 2004 Cambridge University Press"
QUOTE[gkb2004.raw.txt]: "Standard Voting Power Indexes Do Not Work: An"
NOTE: the PDF is 18 pages (PDF pages = journal pp. 657-674). Downloaded by curl. Footnote 16 of the paper says the normal approximation is "most simply" used but that "other forms are possible, such as the scaled beta distribution used by" GKB 1998.

#### [A] A-12 | §1 | Two-party: Pr(decisive vote) ≈ p_{v_j}(0.5)/n_j (eq. 2 and Appendix eq. 3); p_{v_j} the density of the district's vote share v_j, n_j its number of voters (L28)
MARK: confirmed (eq. 2); Appendix eq. 3 is corrected in A-13
SOURCE: https://sites.stat.columbia.edu/gelman/research/published/gelmankatzbafumi.pdf (local: gkb2004.raw.txt) ; Sec. 2.2, eq. (2), p. 661 (page image PDF p. 5); Sec. 2.1 p. 660; Appendix p. 674
QUOTE[gkb2004.raw.txt]: "Pr (a given vote is decisive in jurisdiction j) ⫽ pvj (0.5)/nj,"
QUOTE[gkb2004.raw.txt]: "where pvj is the continuous probability density assigned to the vote for party A in"
QUOTE[gkb2004.raw.txt]: "jurisdiction j. (We are assuming that nj in any district is large enough – greater than 100,"
QUOTE[gkb2004.raw.txt]: "Next, the power of a given voter in jurisdiction j is the probability that party A wins if that voter supports A, minus the probability that A wins if that voter supports B."
NOTE: what is compared with what [stated, Sec. 2.1, p. 660]: the power of a voter is P(A wins | this voter supports A) − P(A wins | this voter supports B). So "decisive" in GKB 2004 means vote for one side versus vote for the *other* side; abstention is not the comparison. "Each jurisdiction j has nj voters" (Sec. 2.1) so n_j includes the voter. Ties "at all levels broken by coin tosses" (Sec. 2.1, p. 660). The formula is stated for two parties, and applies "(We are assuming that nj ... is large enough – greater than 100, say – so that the model for the vj's can be approximated by a continuous distribution)". See A-26 for the arithmetic that p_v(0.5)/n is exactly the vote-A-vs-vote-B swing.

#### [A] A-13 | §1 | Appendix eq. 3: "Pr = E[Phi(v - 1/n) - Phi(v)]" (L28)
MARK: corrected
SOURCE: https://sites.stat.columbia.edu/gelman/research/published/gelmankatzbafumi.pdf (local: gkb2004.raw.txt) ; Appendix, p. 674, eq. (3), read on the page image (PDF p. 18, 200 dpi)
QUOTE[gkb2004.raw.txt]: "Consider a two-party election and label v as the proportion of the n votes received by party A. We model"
QUOTE[gkb2004.raw.txt]: "Pr (decisive vote) ⫽ E[ (v ⫹ 1/n) ⫺ (v)]"
CORRECTION: "E[Phi(v − 1/n) − Phi(v)]" -> **E[π(v + 1/n) − π(v)]** (eq. 3), where π(v) (a lower-case pi, the glyph lost in the text layer) is "the probability that party A wins, given a true proportion v" (not a normal cdf), and "v" is "the proportion in favour of candidate A, excluding your potential vote" and the sign is **+ 1/n**. The text layer shows "(v ⫹ 1/n) ⫺ (v)" with the symbol missing; the page image shows π(v + 1/n) − π(v).
NOTE: as printed the Appendix goes on: with π(v) = 0 below 0.5 − ε and 1 above 0.5 + ε, and p(v) ≈ the constant p(0.5) on 0.5 ± ε, Pr(decisive vote) = p(0.5)[1/n · 1 − 1/n · 0] = p(0.5)/n. The appendix's purpose: a disputed/recounted election (π a smooth function near 0.5) gives the same p(0.5)/n as perfect counting. Footnote 48 cites Good & Meyer (sic) and Margolis, "The Banzhaf Fallacy", AJPS 27 (1983) 321-6.

#### [A] A-14 | §1 | Under random voting, an approximation "of the form (2/sqrt(pi)) * (1/sqrt(n_j))" (as extracted; constants unverifiable) (L28)
MARK: corrected
SOURCE: https://sites.stat.columbia.edu/gelman/research/published/gelmankatzbafumi.pdf (local: gkb2004.raw.txt) ; Sec. 2.2.2, p. 662, read on the page image (PDF p. 6, 130 dpi)
QUOTE[gkb2004.raw.txt]: "Under random voting, the distribution pvj of the vote share among the nj voters in"
QUOTE[gkb2004.raw.txt]: "jurisdiction j is approximately normally distributed with mean 0.5 and standard deviation"
QUOTE[gkb2004.raw.txt]: "What matters for comparing voters is not the constant factor 兹2/ but the proportionality"
CORRECTION: "(2/√π)·(1/√n_j)" -> **√(2/π) · 1/√n_j** (≈ 0.7979/√n_j). Printed: "Pr (a given vote is decisive in jurisdiction j) = p_{v_j}(0.5)/n_j = √(2/π) · 1/√n_j ." followed by "What matters for comparing voters is not the constant factor √(2/π) but the proportionality with 1/√n_j." The text layer reads "兹2/ but" because the π glyph (and the radical's extent) is lost; the extractor's "2/sqrt(pi)" = 1.128 is an extraction error. The constant √(2/π) is exactly what the paper's own stated inputs give (hand derivation in A-26).
NOTE: the paper's derivation stated in words: random voting => vote share approx. normal, mean 0.5, sd 0.5/√n_j; density at the mean is 1/(sd·√(2π)) = √(2/π)·√n_j; dividing by n_j gives √(2/π)/√n_j.

#### [A] A-15 | §1 | Sec. 2.3 forecast example: 10,000 voters, 52% forecast, 3% standard error gives decisiveness ≈ 1.84/n_j (extractor could not verify the constant) (L28)
MARK: confirmed that the paper prints "1.84/n_j"; **the printed formula does not give 1.84** (corrected as to the arithmetic)
SOURCE: https://sites.stat.columbia.edu/gelman/research/published/gelmankatzbafumi.pdf (local: gkb2004.raw.txt) ; Sec. 2.3, p. 663 (page image PDF p. 7, 300 dpi crop)
QUOTE[gkb2004.raw.txt]: "individual vote is decisive is approximate [1/兹2 (0.03)] exp( ⫺ 0.5(0.05/0.03)2)/"
QUOTE[gkb2004.raw.txt]: "nj ⫽ 1.84/nj. We discuss some other models of votes at the end of Section 5.1."
QUOTE[gkb2004.raw.txt]: "get 52 per cent of the vote with a standard error of 3 per cent, then the probability that an"
CORRECTION / NOTE ([measured], script SP/r4/work-A/calc1.py): as printed on the page image: "[1/√2π (0.03)] exp(−0.5(0.05/0.03)²)/n_j = 1.84/n_j" (the radical covers 2π only; the exponent has 0.05/0.03; the example says 52% forecast, so the distance to 0.5 is 0.02). Evaluated literally this is 1/(√(2π)·0.03) × exp(−0.5(0.05/0.03)²) = 13.298 × 0.2494 = 3.32/n_j; with the distance 0.02 it is 13.298 × 0.8007 = **10.65/n_j** (the normal density at 0.5 of N(0.52, 0.03²), i.e. what eq. (2) p_v(0.5)/n_j gives; for n = 10,000 that is 0.001065). The printed 1.84 is reproduced only by 1/√(2π · 0.03) × exp(−0.5(0.02/0.03)²) = 2.303 × 0.8007 = 1.844, that is, with 0.03 treated as a variance under the radical. So the printed number 1.84 and the printed formula disagree with each other, and with GKB 1998's own formula (A-28, which gives 10.65/n for these inputs). [inferred] a slip in the paper; the site must not use "1.84/n" for a 52%±3% forecast; the formula with the density gives 10.65/n_j. The qualitative point (decisiveness ∝ 1/n_j when the forecast does not depend on n) is unaffected.

#### [A] A-16 | §1 | Sec. 2.3 cites the Good & Mayer / Chamberlain & Rothschild rule that decisiveness is proportional to 1/n_j when vote distributions are fixed (L28)
MARK: confirmed (as GKB's statement about those papers; the papers themselves are F-4, unread)
SOURCE: https://sites.stat.columbia.edu/gelman/research/published/gelmankatzbafumi.pdf (local: gkb2004.raw.txt) ; Sec. 2.3, p. 663; footnotes 19 and 23
QUOTE[gkb2004.raw.txt]: "In particular, Good and Mayer and also Chamberlain and Rothchild derive a 1/nj rule"
QUOTE[gkb2004.raw.txt]: "number of voters.23 This model arises by assuming that votes are binomially distributed,"
QUOTE[gkb2004.raw.txt]: "but with binomial probabilities p that themselves vary over the nj voters in a jurisdiction."
QUOTE[gkb2004.raw.txt]: "vj is essentially fixed (not depending on nj), so that pvj (0.5) is a constant, and the probability"
NOTE: the sentence before the second quote reads "– that is, a model where the probability of decisiveness is inversely proportional to the" / "number of voters.23". GKB's footnote 23: "I. J. Good and L. S. Mayer, 'Estimating the Efficacy of a Vote', Behavioral Science, 20 (1975), 25–33; Chamberlain and Rothchild, 'A Note on the Probability of Casting a Decisive Vote'" (the last is J. Economic Theory 25 (1981) 152-62, footnote 19). The paper spells it "Rothchild" and (fn. 48) "Meyer". The claim is attributed, not derived, in GKB; it is "for large or even moderate values of nj".

#### [A] A-17 | §1 | M&F imply the same order, 1/n, for a two-way near-tie with a third candidate trailing, and 1/n² for a three-way tie; hence a third candidate does not change the order for a voter choosing between the top two; it matters only for a voter whose candidate is within a vote or two of the lead (close three-way race), and then by a smaller factor (L35)
MARK: confirmed as to the orders (Lemma 1); the "hence" and "smaller factor" parts are [inferred] and go beyond M&F
SOURCE: https://ora.ox.ac.uk/objects/uuid:adeb8fa9-899c-4fbe-9594-5574db9c4d24/files/sv979v3563 (local: myatt_fisher.raw.txt) ; Lemma 1 and the sentence after it, printed pp. 8-9; Sec. 2.2 p. 7 (Proposition 1 consequences)
QUOTE[myatt_fisher.raw.txt]: "Second, the likelihood ratios of different outcomes are finite. This is not the case when p is known."
NOTE: M&F's orders hold when the voter is *uncertain* of p (f continuous and strictly positive on the whole simplex). M&F say that when p is *known* (the Cox-Palfrey independence setup) "the probability of a pivotal event involving the leading two candidates is infinitely larger than the probability of a pivotal event involving any other pair of parties" (Sec. 1, p. 3). Hence the 1/n and 1/n² statements are for uncertain p only; the first pass's table (L38-47) shows both regimes. The sentence "it matters only for a voter whose candidate is within a vote or two of the lead" is not in M&F; M&F's Table 1 shows the 1-versus-3 and 2-versus-3 near-ties do enter the vote-1-versus-vote-2 payoff (rows x1 = x3 > x2 + 1 etc. with coefficient u1 − u3 over 2), at the same order 1/n as the 1-2 ties (Prop. 2, Eq. 4). So "a third candidate matters only for a voter close to the lead" is [inferred] by the first pass and is not what M&F's Prop. 2 says; in M&F a *third-placed candidate's closeness to the leaders* (p13, p23) changes the incentive at the same 1/n order.

#### [A] A-18 | §1 | First pass's [measured] table (L38-47): exact calculation of Q_j = P(j wins | votes j) − P(j wins | abstains), N other voters (L36-47)
MARK: see below (spot-checked by me; not a source claim)
SOURCE: my own recomputation, script SP/r4/work-A/calc3.py (below)
NOTE: not a sourced fact; placed in the final section "SPOT-CHECK OF THE FIRST PASS'S OWN CALCULATION".

#### [A] A-19 | §1 (also §7 L186) | First-pass line 49: "the known-shares rows show the effect of the 'only top-two votes enter the margin' factor, 1/sqrt(p1+p2): for (.4,.4,.2) that is 1/sqrt(.8) = 1.118 [measured, matches]" (L49)
MARK: confirmed (arithmetic; not a source claim)
SOURCE: my own computation, SP/r4/work-A/calc3.py and calc3b.py (see the spot-check section)
NOTE: 1/√0.8 = 1.1180 and the exact ratio Q(3 candidates, known shares .4/.4/.2)/Q(2 candidates, .5/.5) at N = 1000 is 0.014097/0.012613 = 1.1177; at N = 10,000 it is 0.004460/0.003989 = 1.118. For (.45,.45,.10): 1/√0.9 = 1.0541 versus 0.013291/0.012613 = 1.0538.

#### [A] A-27 | §1 / §10.3 | (the first pass's Appendix equation "Pr = E[Phi(v - 1/n) - Phi(v)]" and the "random voting" constant were both extraction artefacts: see A-13 and A-26)
MARK: corrected (cross-reference only)
SOURCE: see A-13, A-26
NOTE: none.

#### [A] A-28 | §1 (cross-check) | GKB 1998 Sec. 5: probability that a single vote is decisive when the forecast is normal(μ, τ²): (√(2π) τ n)^-1 exp(−(μ − .5)²/(2τ²)); 2%-standard-error upper bound 20/n (not in the first pass; needed to check A-15)
MARK: confirmed (new item, read at source)
SOURCE: https://sites.stat.columbia.edu/gelman/research/published/decisive2.pdf (local: gkb1998_columbia.raw.txt) ; Sec. 5, printed p. 6 (page image PDF p. 6)
QUOTE[gkb1998_columbia.raw.txt]: "error of less than, say, 2% of the vote. This yields 2 0 / n as"
QUOTE[gkb1998_columbia.raw.txt]: "an upper bound on the probability that your vote is decisive"
QUOTE[gkb1998_columbia.raw.txt]: "As an external check on our model, we estimate the probability that any generic election is tied using equation (2)."
NOTE: as printed (image): "Suppose that n people vote in the election, and that the forecast is a normal distribution with mean μ and standard deviation τ; then the probability that a single vote will be decisive is approximately (√(2π) τ n)^{-1} exp(−(μ − .5)²/(2τ²)), as discussed by Margolis (1977). ... The probability of a tie is clearly maximized at μ = .5. As for τ, it is hard to imagine a real election that could be forecast to within a standard error of less than, say, 2% of the vote. This yields 20/n as an upper bound on the probability that your vote is decisive in a close election." [measured] 1/(√(2π)·0.02) = 19.95. With μ = 0.52, τ = 0.03 (the GKB 2004 Sec. 2.3 example) this printed formula gives 13.298 × exp(−0.5 (0.02/0.03)²) = 10.65/n, not 1.84/n (see A-15). Margolis (1977) is "Probability of a Tie Election", Public Choice 31, 134-7 (GKB 2004 fn. 19).

---

#### [E] E-19 | §1 | line 27: citation, "published Political Analysis 33(4):447-455, 2025, doi 10.1017/pan.2024.32"
MARK: unread
SOURCE: arXiv text only (https://arxiv.org/pdf/2210.01657, local baltz_arxiv.raw.txt) and the supplement; the volume, pages and DOI are on cambridge.org (not allowed to me)
QUOTE[baltz_arxiv.txt]: "The probability of casting a pivotal vote in an Instant Runoff Voting election"
QUOTE[baltz_sup.raw.txt]: "Eggers, A. C. and Nowacki, T. (2024). Susceptibility to strategic voting: A comparison of plurality and instant-runoff elections. Journal of Politics, 86(2)."
NOTE: Title and author confirmed against the arXiv file (arXiv:2210.01657v2 [cs.GT], 31 Jul 2023, "Samuel Baltz"). Neither file prints "Political Analysis", "33(4)", pages or the DOI. [inferred] only: the supplement's URL carries the Cambridge article id S1047198724000329, which has the form of Political Analysis (ISSN 1047-1987) article 00032 of 2024, consistent with the DOI suffix pan.2024.32; this is a pattern reading, not a read. The supplement is dated 4 Sept 2024 and calls the paper "this letter", so the published paper is a short-form version of the arXiv v2.

#### [E] E-20 | §1 | line 27 (second part): "It uses, for single-member-district plurality (SMDP), 'the Mebane et al. (2019) derivation' with Skellam-based pivot probabilities under Poisson voting games, and extends it to IRV."
MARK: confirmed
SOURCE: https://arxiv.org/pdf/2210.01657 (local: baltz_arxiv.raw.txt) ; footnote 5, p. 23
QUOTE[baltz_arxiv.raw.txt]: "To facilitate direct comparison, I simulate SMDP pivotal probabilities using the derivation from Mebane et al. (2019) which I extended to cover IRV."
QUOTE[baltz_arxiv.raw.txt]: "Mebane, Jr., W. R., Baltz, S., and Vasselai, F. (2019). Using agent-based models to simulate strategic behavior in elections. Presented at the 2019 meeting of the Society for Political Methodology."
NOTE: [stated]. The first pass's quoted words "the Mebane et al. (2019) derivation" are its paraphrase. Mebane et al. is a conference presentation, not a journal article; I found no URL for it (see F-3); the SMDP formula Baltz used for Figure 1 is therefore not in anything I could read.

#### [E] E-21 | §1 | line 31 (first part): "100 runs per setting, 3, 4 and 5 candidates, 'a community of 1,000 voters' (caption)"
MARK: confirmed
SOURCE: https://arxiv.org/pdf/2210.01657 (local: baltz_arxiv.raw.txt) ; Sec. 4 p. 23 and Fig. 1 caption p. 24; supplement §9 p. 16-18
QUOTE[baltz_arxiv.raw.txt]: "I will show results from 100 runs of a model, where each run consists of one IRV contest and one SMDP contest with identical parameters, re-run for elections with 3, 4, and 5 candidates."
QUOTE[baltz_arxiv.raw.txt]: "when voters can rank every candidate, in a community of 1,000 voters."
QUOTE[baltz_sup.raw.txt]: "Each dot represents the sum of the pivotal probabilities of all ballots in one run of the simulation."
NOTE: [stated]. The arXiv caption says "in a community of 1,000 voters"; the published caption says "when 1,000 voters can rank every candidate" (baltz_sup p. 18). "100 runs" means 100 random seeds, one dot per run per system per candidate count (caption).

#### [E] E-22 | §1 | line 31 (second part): power-law preference structure "half of the population holds one preference order, and the other half has a uniformly random preference order"
MARK: confirmed
SOURCE: https://arxiv.org/pdf/2210.01657 (local: baltz_arxiv.raw.txt) ; Sec. 4, p. 23; same sentence in baltz_sup.raw.txt §9
QUOTE[baltz_arxiv.raw.txt]: "The other is a power law distribution, where half of the population holds one preference order, and the other half has a uniformly random preference order."
QUOTE[baltz_sup.raw.txt]: "The other is a power law distribution, where half of the population holds one preference order, and the other half has a uniformly random preference order."
NOTE: [stated] exact text. **But see the Reconciliation section:** taken literally with 1,000 voters and the paper's own Skellam formulas this structure gives pivot probabilities of order 10^-70 or smaller [measured], not 10^-6 to 10^-12 as plotted; so the one-sentence description cannot be the whole of what was simulated. The paper gives no exponent and calls the other structure "uniform" ("every candidate has similar numbers of people most-preferring them, second-most-preferring them, third-most-preferring them, and so on", p. 23). The published appendix adds: "the order of each voter's ballot is determined randomly, in a way that ensures that support for the candidates follows the specified distribution" (p. 17).
QUOTE[baltz_sup.raw.txt]: "the order of each voter’s ballot is determined randomly, in a way that ensures that support for the candidates follows the specified distribution."

#### [E] E-23 | §1 | line 31 (third part): "No ratios printed. The paper itself calls these 'out-of-equilibrium pivotal probabilities'."
MARK: confirmed
SOURCE: https://arxiv.org/pdf/2210.01657 (local: baltz_arxiv.raw.txt) ; footnote 6, p. 25
QUOTE[baltz_arxiv.raw.txt]: "note that these are all out-of-equilibrium pivotal probabilities."
QUOTE[baltz_arxiv.raw.txt]: "So, these should be understood as the initial pivotal probabilities of these election structures."
NOTE: [stated]. No ratio of IRV to SMDP is printed in the text of either version (searched). The footnote's reason: "Observing these pivotal probabilities would cause rational voters to update their expected vote choice, which should change the expected vote totals of each candidate, and in turn alter the pivotal probabilities."

#### [E] E-24 | §1 | line 31 (caution, [inferred]): "values this small, at N = 1,000, most likely arise because the stylised electorates have fixed preference structures that are far from a tie ... so not comparable with the 1/N-scale values"
MARK: corrected
SOURCE: https://arxiv.org/pdf/2210.01657 (local: baltz_arxiv.raw.txt; Fig. 1 page 24 as image) and baltz_sup.raw.txt §9 p. 17 and Fig. 1 p. 18
QUOTE[baltz_sup.raw.txt]: "Note that the figures have different y-axis scales so that the range of both is clearly visible; this means that they should not be directly compared to one another without taking the y-axis scales into account."
CORRECTION: "the Baltz values (1e-7, 1e-6) are the levels at N = 1,000 and are not comparable to the 1/N scale" -> the 10^-6 / 10^-7 averages belong to the **power-law (clear front-runner) panel only**, drawn on a log10 axis; in the **uniform panel** at the same 1,000 voters the plotted totals are 0.003 to 0.12 (linear axis; mean lines about 0.03 to 0.08), which is the same order of magnitude as the first pass's 0.006 to 0.016 per ballot once one allows that Baltz's y-value is a sum over all ballots. See the Reconciliation section.
NOTE: The first pass's guess (fixed structure far from a tie gives tiny values) is right for the power-law panel in kind, but it lumps in the uniform panel, which is not tiny, and it did not know the y-value is a sum over ballots.

---

### [A] SPOT-CHECK OF THE FIRST PASS'S OWN CALCULATION (L36-49; not a source claim)
I re-ran the first pass's calculation independently (SP/r4/work-A/calc3.py for N = 1,000 and calc3b.py for N = 10,000; numpy only; exact multinomial, or Dirichlet-multinomial with concentration 400; Q_j = P(j wins | this voter votes j) − P(j wins | abstains), ties split uniformly among tied leaders, N = number of other voters). Every row of the first-pass table reproduces to the digits printed:
- 2 candidates known (.5,.5): Q = 0.012613 (N = 1,000; first pass 0.01261), 0.003989 (N = 10,000; equals 1/√(2πN) = 0.0039894).
- 3 candidates known (1/3,1/3,1/3): 0.015488 (first pass 0.01549) and 0.00489 (0.004890). Known (.4,.4,.2): 0.014097 / 0.00446 (0.01410 / 0.004460); the third candidate 2e-24 / 7e-216. Known (.45,.45,.10): 0.013291 / 0.004205 (0.01329 / 0.004205).
- 2 candidates forecast (.51,.49), κ = 400: Q_A = 0.006363 (N·Q = 6.36) and 0.000724 (N·Q = 7.24) (first pass 0.006363, 6.4, 0.000724, 7.2).
- 3 candidates forecast (.40,.38,.22): Q = 0.0070664, 0.0071184, 2.9e-7 (N = 1,000) and 0.0008019, 0.0008027, 1.56e-9 (N = 10,000) (first pass 0.00707, 0.00712, 3e-7; 0.000802, 0.000803, 1.6e-9). Forecast (.36,.34,.30): 0.008013, 0.0075528, 0.0024979 and 0.0008947, 0.000846, 0.0002066 (first pass 0.00801, 0.00755, 0.00250; 0.000895, 0.000846, 0.000207). Forecast (.45,.45,.10): 0.0071041 and 0.0008244 (first pass 0.00710 and 0.000824).
So the first pass's computed values are reproduced. What the first pass's own "reading" line says ("top-two Q within about 1.05x to 1.26x of the two-candidate Q") also checks: the ratios are 1.05 and 1.12 (known shares), 1.23, and 1.11, 1.26, 1.12 (forecasts), by the numbers above. Two things to keep in mind when the table is used: (i) Q here is vote-versus-abstain with coin-toss ties; the swing for one side versus the other is 2Q (A-26); (ii) the table is the first pass's model (Dirichlet-multinomial, κ = 400), not any source's.

---


### [A] SOURCE-CHECK ANSWERS TO THE TASK FILE'S SPECIFIC QUESTIONS
1. "What is the exact statement of Lemma 1, what is m, and is 'approximately f(x/n) times 1/n^(m-1)' what Proposition 1 prints?" Lemma 1 is for m = 3: Eq. (2) two-way and near-two-way ties ≈ (∫_{1/3}^{1/2} f(z,z,1−2z)dz)/(6n) (the 6 does not survive my exact check; the order 1/n is right) and Eq. (3) three-way and near-three-way ties ≈ f(1/3,1/3,1/3)/n². m is the number of candidates (Sec. 2.1: "contested by m candidates ... we will often focus on the m = 3 case"). Proposition 1 prints Pr[x] ≈ f(x/n) · [n!/∏x_j!] ∫_△ ∏p_j^{x_j} dp = (1/n^{m−1}) f(x/n): yes, f(x/n) times 1/n^{m−1}.
2. GKB 2004 eq. 2 and Appendix eq. 3: eq. 2 is p_{v_j}(0.5)/n_j; Appendix eq. 3 is E[π(v + 1/n) − π(v)] (π = P(A wins), "+ 1/n", not Φ and not "− 1/n"). Random-voting constant: √(2/π), not 2/√π. 1.84/n_j: the printed formula gives 3.32/n_j as printed, 10.65/n_j with the 2-point distance 0.02, and 1.84 only with 0.03 under the radical. Good-Mayer / Chamberlain-Rothschild: GKB say they "derive a 1/nj rule". The empirical exponents: Fig. 1 −0.16; Fig. 3 +0.08, +0.06, −0.11, −0.23, −0.01, −0.07; simulation −0.494; "perhaps proportional to n_j^−0.1" for the vote differential, "n_j^−0.9" for the probability. "Less than 10 per cent": for the linear approximation to Factor 1 under random voting. Banzhaf: "the probability that an individual vote is decisive under the assumption that all voters are deciding their votes independently and at random, with probabilities 0.5 for each of two parties".
3. First-pass open question 1: see A-26 (the constant, read correctly, agrees with the exact calculation).
4. GKB 1998: the decomposition and the figures: A-20, A-21, A-25a-f.

---


## 2. Two-round runoffs

*First-pass lines 51-69 of `research/electoral-systems.md`. Each block: the first-pass claim with its line number, the mark, the source and location, exact quotes, the correction if any, notes.*

#### [B] B-01 | §2 | Bouton, AER 103(4): 1248-88 (2013); version read is the author's draft, first draft March 2006, revision February 2012 (line 55)
MARK: confirmed (draft dates and the journal citation separately); the AER text itself is unread
SOURCE: https://economics.sas.upenn.edu/sites/default/files/filevault/event_papers/Runoff.pdf (local: bouton.txt) ; title page. Journal citation: https://econpapers.repec.org/RePEc:aea:aecrev:v:103:y:2013:i:4:p:1248-88 (local: dl/econpapers_aer.clean.txt, fetched by me, a bibliographic record, 200 OK)
QUOTE[bouton.txt]: "First Draft: March 2006 This Revision: February 2012"
QUOTE[dl/econpapers_aer.clean.txt]: "American Economic Review , 2013, vol. 103, issue 4, 1248-88"
NOTE: Is the draft the same as the AER version? Only partly checkable. (1) The AER abstract on EconPapers is word-for-word the draft's abstract except "50%" in the draft versus "50 percent" in the AER. (2) The draft's acknowledgement thanks "the co-editor and three anonymous referees", so it is a post-review draft. (3) The AER full text is "restricted to AEA members and institutional subscribers" (EconPapers), so I could not read it. (4) The later Bouton & Gratton paper (Theoretical Economics 10 (2015), open copy, see F-02) says of its own Section 3.1: "This paragraph and Section 3.1 are based on similar sections in Bouton (2013)." and its Table 1 is the draft's Table 1 with the threshold set to 1/2. So: the draft's content is probably very close to the AER text, but I cannot say it is identical; equation and table numbers could differ in the journal. (5) [stated, EconPapers] The Boston University Department of Economics working paper WP2012-001 (https://econpapers.repec.org/RePEc:bos:wpaper:wp2012-001, local: dl/ep_bos.clean.txt) is the same title, "47 pages", dated "2012-01", and its listed download is http://people.bu.edu/lbouton/Runoff.pdf (404 on EconPapers' link check); the Penn draft I read is also 47 pages with "This Revision: February 2012", so [inferred] it is this working-paper version or a revision of it, about a year before the AER publication (AER 103(4) is the June 2013 issue; EconPapers lists the AEA data supplement .../aer/ds/june2013/20110367_ds.zip). I found no open copy of the AER text. The PDF file's metadata (ModDate 17 Apr 2012) is later than the "Feb 2012" revision date; I do not know what changed.

#### [B] B-02 | §2 | Setup (Sec. 2): three candidates {A,B,C}, Poisson electorate with mean n, twelve voter types (line 56)
MARK: confirmed
SOURCE: bouton.txt ; Sec. 2 "Setup", printed pp. 6-8 (pdf pp. 7-9)
QUOTE[bouton.txt]: "There are three candidates, fA; B; Cg ; and twelve types of voters"
QUOTE[bouton.txt]: "according to a Poisson distribution of mean n: l"
QUOTE[bouton.txt]: "Each voter is assigned a type t by i.i.d. draws."
QUOTE[bouton.txt]: "Thus, voters do not directly derive a bene…t from the ballot they cast: they are instrumental."
NOTE: [stated] The type list printed is t_AB, t'_AB, t''_AB, t_AC, t'_AC, t_BA, t''_BA, t_BC, t'_BC, t_CA, t''_CA, t_CB: twelve. The model also assumes something the first pass did not mention and that matters for any "two votes, one voter" reading: "none of the …rst-round voters participate in the second round, and vice versa. I assume that there is a (complete) new draw of voters between the two rounds." (QUOTE below). So in the model a person does not have two ballots; the two rounds have separate Poisson electorates with the same mean n and the same type probabilities. Section 5 relaxes this and says the main results survive, and that if the two electorates were exactly the same, Duverger's-law equilibria would not exist for thresholds in [1/2, 1).
QUOTE[bouton.txt]: "Therefore, in my model none of the …rst-round voters participate in the second round, and vice versa. I assume that there is a (complete) new draw of voters between the two rounds."
QUOTE[bouton.txt]: "Note that having a di¤erent electorate in each round is not necessary for the results to hold."

#### [B] B-03 | §2 | Round-1 actions {A,B,C,abstain}; if no candidate passes threshold theta a second round between the top two (line 56)
MARK: confirmed
SOURCE: bouton.txt ; Sec. 2, printed pp. 6-7
QUOTE[bouton.txt]: "In the …rst round ( = 1), each voter either casts a ballot in favor of one of the candidates or abstains."
QUOTE[bouton.txt]: "In this round, however, not all candidates participate: only the two candidates who received the most votes in the …rst round (called the top-two candidates) are included."
NOTE: [stated] The action set is printed Psi^1 = {A, B, C, ∅} (the file shows "fA; B; C; ?g", "?" standing for the empty-set symbol; I did not render that page, but the page image of pdf p. 13, footnote 24, prints the same symbol in "G^1(∅|t) = 0"). Threshold: "If the candidate who ranks …rst obtains more than a pre-de…ned fraction, ; of the votes (called the threshold for …rst-round victory), she wins outright and there is no second round." (the Greek letter, zeta, is lost in the file; the page images on pp. 12 and 19 print it as zeta). Thresholds below 1/3 are equivalent to plurality and are excluded: "a runo¤ electoral system with a threshold below 1/3 is equivalent to the plurality electoral system".
QUOTE[bouton.txt]: "If the candidate who ranks …rst obtains more than a pre-de…ned fraction, ; of the votes (called the threshold for …rst-round victory), she wins outright and there is no second round."
QUOTE[bouton.txt]: "In a three-candidate setup, a runo¤ electoral system with a threshold below 13 is equivalent to the plurality electoral system"

#### [B] B-04 | §2 | Ties by alphabetical order (results also hold with a fair coin) (line 56)
MARK: confirmed
SOURCE: bouton.txt ; Sec. 2, printed p. 7 and footnote 16
QUOTE[bouton.txt]: "ties are resolved by alphabetical order: A wins over both B and C, B wins over C."
QUOTE[bouton.txt]: "Results hold if I assume that ties are resolved by the toss of a fair coin."
NOTE: [stated]

#### [B] B-05 | §2 | Second-round pivot event: piv^2_PQ is the event that P "trails behind Q by exactly one vote"; a tie piv^2_QP also pivots because of the tie-break (line 57)
MARK: confirmed
SOURCE: bouton.txt ; Sec. 3.1.1, printed pp. 9-10
QUOTE[bouton.txt]: "happens when P trails behind Q by exactly one vote: an additional ballot in favor of P leads to a tie between P and Q and thus to the victory of the former (since ties are broken alphabetically)."
QUOTE[bouton.txt]: "happens when P and Q obtain exactly the same number of votes: an additional"
NOTE: [stated] In the text, "Suppose that P ... ranks before Q" and P wins ties, so [inferred] P is the alphabetically earlier candidate; piv^2_PQ is an extra ballot for P turning a one-vote deficit into a tie that P wins; piv^2_QP is an extra ballot for Q turning an exact tie (which P would win) into a win for Q. The page image (pdf p. 40, printed p. 39) shows the same two events in the proof of Lemma 2: "The event that candidates P and Q have exactly the same number of vote is the pivotability QP" and "The event that candidate P trails behind candidate Q by exactly one vote is the pivotability PQ". The first pass's "a tie piv^2_QP also pivots because of the tie-break" is a fair short reading.

#### [B] B-06 | §2 | G_2(P|t) = Pr(piv^2_PQ)[U(P|t) - U(Q|t)] (line 57)
MARK: confirmed
SOURCE: bouton.txt ; eq. (3), printed p. 11 (page image pdf p. 12)
QUOTE[bouton.txt]: "G2 ( jt) denote the expected gain of playing action 2 2 in the second round."
NOTE: [stated] As printed (image): G^2(P|t) = Pr(piv^2_PQ) [U(P|t) − U(Q|t)]. (3). The sentence under it: "By definition, G^2(∅|t) = 0 ∀t." The quote above is the nearest sentence in the file that survived extraction; the equation itself is in FORMULAS AS PRINTED.

#### [B] B-07 | §2 | First-round pivot events, four kinds, Table 1 (line 58)
MARK: confirmed in substance; corrected in notation
SOURCE: bouton.txt ; Sec. 3.1.2 and Table 1, printed pp. 10-11 (page image pdf p. 12, crop at 220 dpi)
QUOTE[bouton.txt]: "if candidate i lacks one vote (or less) to pass the threshold for …rst-round victory and the other candidates are all below that threshold."
QUOTE[bouton.txt]: "refers to an event in which any ballot against candidate i, i.e. in favor of either j or k, prevents an outright victory of i in the …rst round and ensures that a second round opposing i to j is held."
QUOTE[bouton.txt]: "if candidates i and j have (almost) the same number of votes and are both above the threshold."
QUOTE[bouton.txt]: "A ballot is second-rank pivotal ki=kj when candidate k ranks …rst and candidates i and j tie for second place."
CORRECTION: the first pass writes the events as "i=ij", "ij=i", "i=j", "ki=kj"; the paper prints them with a slash: threshold pivotal i/ij and ij/i, above-threshold pivotal i/j, second-rank pivotal ki/kj (the "=" is an artefact of the text extraction; the page image shows "/"). The four kinds and their wording are right. Also the paper names the one-sided versions ij/i (against i) and i/ij (for i) as two events (Table 1 has four rows: i/ij, ij/i, i/j, ki/kj), and eq. (4) uses ten of them.
NOTE: [stated] Table 1 as printed (image) is in FORMULAS AS PRINTED. The paper warns the conditions are loose: "These conditions are thus necessarily loose." (footnote 22: depending on alphabetical order the inequalities may be weak or strict and the "minus 1" may be absent). The above-threshold event is only possible for threshold below 50%: "Since two candidates cannot simultaneously obtain more than 50% of the votes, the above threshold pivotability is possible if and only if the threshold is below 50%."
QUOTE[bouton.txt]: "These conditions are thus necessarily loose."

#### [B] B-08 | §2 | First-round payoff G_1(i|t) (eq. 4) "sums pivot probabilities times expected second-round utility differences" (line 58)
MARK: corrected (partly)
SOURCE: bouton.txt ; Sec. 3.2.2, eq. (4), printed p. 12 (page image pdf p. 13)
QUOTE[bouton.txt]: "For a type t, the expected gain of playing action i in the …rst round is:"
QUOTE[bouton.txt]: "The …rst line in (4) reads as follows: if a ballot in favor of i is second-rank pivotal ki=kj; then the second round opposes k to i instead of k to j; if a ballot in favor of i is second-rank pivotal ji=jk; then the second round opposes j to i instead of j to k."
CORRECTION: "sums pivot probabilities times expected second-round utility differences" -> eq. (4) is a sum of ten terms, each a pivot probability times a utility difference, but only the two second-rank terms (display line 1) are differences of two expected second-round utilities, U(k,i|t) - U(k,j|t) and U(j,i|t) - U(j,k|t). The two above-threshold terms (line 2) are plain differences of utilities of outright winners, U(i|t) - U(j|t) and U(i|t) - U(k|t). The six threshold terms (lines 3-5) compare an outright win with an expected second round: U(i|t) - U(i,j|t), U(i|t) - U(i,k|t), U(j,i|t) - U(j|t), U(j,k|t) - U(j|t), U(k,i|t) - U(k|t), U(k,j|t) - U(k|t). Here U(i,j|t) = Pr(i|{i,j}) U(i|t) + Pr(j|{i,j}) U(j|t) is the expected utility of a second round between i and j. Exact equation in FORMULAS AS PRINTED.
NOTE: [stated]. (In the file the equation is garbled; page image read.) Eq. (4) has no probability of "no second round" term as such; the first-round outright-win events appear via the above-threshold and threshold terms.
QUOTE[bouton.txt]: "U (i; jjt) = Pr (ij fi; jg) U (ijt) + Pr (jj fi; jg) U (jjt);"

#### [B] B-09 | §2 | Sizes: pivot events compared by "magnitude", mag(E) = lim log Pr(E)/n (App. A1) (line 59)
MARK: confirmed
SOURCE: bouton.txt ; Appendix A1, Property 1, printed p. 38 (page image pdf p. 39, crop at 200 dpi)
QUOTE[bouton.txt]: "That is, the probability that event E occurs is exponentially decreasing in n: mag (E ) 2 [ 1; 0] is called the magnitude of event E . Its absolute value represents the “speed” at which the probability decreases towards 0: the more negative is the magnitude, the faster the probability goes to 0."
NOTE: [stated] The definition as printed (image), Property 1: mag(E^ρ) ≡ lim_{n→∞} log[Pr(E^ρ)]/n = max_{x^ρ∈E} Σ_ψ (x^ρ_ψ/n)(1 − log(x^ρ_ψ/(n τ^ρ_ψ))) − 1; mag ∈ [−1, 0]. The file's own line (the extract garbles the symbols but keeps the "lim ... log" structure) is in the FORMULAS section. Property 2 (Myerson 2000, Cor. 1): if mag(E) < mag(E'), Pr(E)/Pr(E') → 0 as n grows. [inferred] mag is the exponential rate only: it fixes how Pr(E) shrinks as n grows, not the level of Pr(E) at any given n (sub-exponential factors are not in it).

#### [B] B-10 | §2 | Lemma 2 (second round): "for a ballot to be pivotal, candidates have to receive (almost) the same number of votes"; magnitude is a negative function of the candidates' expected shares, zero only when equal; "extracted formula garbled; constants not given" (line 59)
MARK: corrected (a closed form IS given)
SOURCE: bouton.txt ; Lemma 2 and its proof, App. A1, printed pp. 38-39 (page images pdf pp. 39-40)
QUOTE[bouton.txt]: "Lemma 2 reformulates a known result for two-candidate elections (as is the second round): the larger the di¤erence in the expected vote shares of the two candidates, the smaller the magnitude of the pivot probability. The intuition is straightforward: for a ballot to be pivotal, candidates have to receive (almost) the same number of votes. This is more likely to happen if the second round is expected to be close."
CORRECTION: "constants not given" -> Lemma 2 states a closed form: mag(piv^2_PQ) = mag(piv^2_QP) = −(√τ²_P − √τ²_Q)², where τ²_ψ is the expected share of the electorate choosing action ψ in round 2 (eq. 2: τ^ρ(ψ) = Σ_t r(t) σ^ρ(ψ|t)). It is zero if and only if τ²_P = τ²_Q. The proof (eq. 16) maximises at x* = n √(τ²_P τ²_Q). The first-round magnitudes are also closed-form: Lemma 3, eqs. (17)-(19), printed p. 39 (page image pdf p. 40). All in FORMULAS AS PRINTED.
NOTE: [stated]. The first pass called this "Lemma 2 (second round)": correct, Lemma 2 is the second-round lemma and Lemma 3 the first-round one (the paper's Lemma 1 is about Duverger's-law equilibria, Sec. 4.3). Because τ is a share of the whole electorate (abstainers are an action), the formula uses shares of all potential voters, not shares of votes cast; [inferred] from eq. (2) and Property 1's sum over all actions ψ including abstention.

#### [B] B-11 | §2 | Table 2 (theta = 0.5): mag(piv^1_CA/CB) = -0.0014 is the largest listed; mag(piv^1_B/BC) = -0.1227 (line 59)
MARK: confirmed (signs and decimals checked on the page image; the file loses the minus signs)
SOURCE: bouton.txt ; Sec. 4.2.2, Table 2, printed p. 18 (page image pdf p. 19); parameters on printed p. 17 (page image pdf p. 18)
QUOTE[bouton.txt]: "Indeed, mag(pivCA=CB ) is the largest magnitude.27"
QUOTE[bouton.txt]: "Suppose that = 0:5; r (tAB ) = 0:3, r (tBA ) = 0:26, and r(t00CA ) = 0:44:"
NOTE: [stated] Table 2 as printed (image): mag(piv^1_{A/AC}) = −0.0835; mag(piv^1_{B/BC}) = −0.1227; mag(piv^1_{BA/BC}) = −0.0251; mag(piv^1_{CA/CB}) = −0.0014 (bold); mag(piv^1_{AB/AC}) = −0.0251. Page image on p. 17 prints ζ = 0.5, r(t_AB) = 0.3, r(t_BA) = 0.26, r(t''_CA) = 0.44, so "theta = 0.5" is right (the paper's threshold symbol is zeta, not theta). It is the three-type stylised model (t_AB, t_BA, t''_CA), not the twelve-type model. Table 2 is the "sincere voting" case. For comparison (not in the first pass): Table 3 (ζ = 0.5, r = 0.38, 0.18, 0.44; no sincere voting; image pdf p. 20): mag(piv_{A/AC}) = −0.0292 (bold), mag(piv_{B/BC}) = −0.2316, mag(piv_{BA/BC}) = −0.0668, mag(piv_{CA/CB}) = −0.0369, mag(piv_{AB/AC}) = −0.0572; Table 4 (ζ = 0.4, r = 0.30, 0.29, 0.41; the Ortega case): threshold −0.0223, −0.0273, mag(piv_{CA/C}) = −0.0002; above-threshold −0.0304, −0.0370, −0.0953; second-rank −0.0125, mag(piv_{CA/CB}) = −0.0003, −0.0125. These are not per-voter probabilities; they are exponential rates for n -> infinity.

#### [B] B-12 | §2 | "which first-round event dominates changes with the type distribution and threshold" (Tables 2-4) (line 69, inferred)
MARK: confirmed [inferred]
SOURCE: bouton.txt ; Tables 2-4 and the text before Table 3 (printed pp. 17-18, 21-22)
QUOTE[bouton.txt]: "is larger than all other magnitudes. This means that majority voters realize that, conditional on being pivotal,"
NOTE: [stated] In Table 2 the second-rank event CA/CB is largest; in the Table 3 example (more unbalanced majority) the threshold event A/AC (plus the upset risk) is largest; in the Table 4 example (ζ = 0.4) the threshold event CA/C (−0.0002) is largest by the paper's bold and CA/CB (−0.0003) next. [inferred] so the dominant event changes with the parameters, as the first pass says.

#### [B] B-13 | §2 | "Published estimates of the probability. None found. Bouton gives exponents, not a probability for any electorate size" (line 61)
MARK: confirmed
SOURCE: bouton.txt ; whole paper (searched for any numeric electorate-size probability: none; the only numbers are magnitudes in Tables 2-4 and the vote shares of examples)
QUOTE[bouton.txt]: "Their probabilities are derived in Appendix A1 (which summarizes the properties of Poisson games and applies them to runo¤ elections)."
NOTE: [stated]/[inferred]: the paper derives limiting exponents only. See F-03 for my search for any published probability estimate in a real two-round election: none found.

---

#### [B] B-14 | §2 | France 2002: Le Pen 4,804,713 (16.86%), Jospin 4,610,113 (16.18%) (line 64)
MARK: confirmed, now from the Conseil constitutionnel's own proclamation
SOURCE: https://www.conseil-constitutionnel.fr/decision/2002/2002109PDR.htm (local: dl/cc2002.clean.txt, fetched by curl, 200 OK) ; Décision n° 2002-109 PDR du 24 avril 2002, Article premier. Percentages: Maire-info (local: work-B/maire_info.clean.txt, the cleaned text of maire_info.html)
QUOTE[dl/cc2002.clean.txt]: "M. Jean-Marie Le Pen .................... 4 804 713"
QUOTE[dl/cc2002.clean.txt]: "M. Lionel Jospin .................... 4 610 113"
QUOTE[dl/cc2002.clean.txt]: "Suffrages exprimés .................... 28 498 471"
QUOTE[maire_info.clean.txt]: "Jean-Marie LE PEN - 4 804 713 (16,86%)"
QUOTE[maire_info.clean.txt]: "Lionel JOSPIN - 4 610 113 (16,18%)"
NOTE: [stated] by the Conseil constitutionnel (Article premier, "Les résultats du scrutin ... auquel il a été procédé le 21 avril 2002, sont les suivants"). [measured] percentages of suffrages exprimés from the Conseil's counts: 4,804,713 / 28,498,471 = 16.8595% (16.86), 4,610,113 / 28,498,471 = 16.1767% (16.18): both match Maire-info. Chirac 5,665,855 = 19.88%. The decision names the Conseil members including the president, Yves GUÉNA, and "Journal officiel du 25 avril 2002, page 7369". Maire-info says the percentages are the same as those the Interior Ministry published earlier and "le nombre exact des voix a été très légèrement modifié" (the exact vote counts were very slightly changed): the figures in Maire-info are the Conseil's, as the first pass said.

#### [B] B-15 | §2 | Gap 4,804,713 - 4,610,113 = 194,600 (line 64)
MARK: confirmed [measured]
SOURCE: arithmetic on the Conseil's counts (B-14)
NOTE: [measured] 4,804,713 - 4,610,113 = 194,600 (python3). As a share of suffrages exprimés: 194,600 / 28,498,471 = 0.683%. Electeurs inscrits 41,194,689; votants 29,495,733; suffrages exprimés 28,498,471 (Conseil).

#### [B] B-16 | §2 | Maire-info is a "secondary reproduction", published 25 April 2002 with president Yves Guena (line 64)
MARK: confirmed
SOURCE: https://maire-info.com/les-resultats-officiels-annonces-par-le-conseil-constitutionnel-article2-1774 (local: maire_info.html, cleaned in work-B/maire_info.clean.txt)
QUOTE[maire_info.clean.txt]: "Voici, dans l’ordre du nombre de voix obtenues au premier tour par les candidats à l’élection présidentielle, les résultats officiels annoncés mercredi par le président du Conseil constitutionnel Yves Guéna :"
QUOTE[maire_info.clean.txt]: "Édition du jeudi 25 avril 2002"
NOTE: [stated] The announcement was on Wednesday 24 April 2002; the page edition is Thursday 25 April 2002. The first pass did not read the Conseil's page ("not tried"); now read (B-14).

#### [B] B-17 | §2 | France 2022: Macron 27.84, Le Pen 23.15, Melenchon 21.95, Zemmour 7.07 (LCP, Interior Ministry's definitive results) (line 65)
MARK: confirmed as LCP prints them; and checked against the Conseil constitutionnel's final proclamation, where Macron computes to 27.85 not 27.84
SOURCE: https://lcp.fr/index%2ephp/actualites/premier-tour-decouvrez-les-resultats-definitifs-109262 (local: work-B/lcp.clean.txt, cleaned from lcp.html) ; and https://www.conseil-constitutionnel.fr/decision/2022/2022195PDR.htm (local: dl/cc2022.clean.txt) Décision n° 2022-195 PDR du 13 avril 2022, Article 1er
QUOTE[lcp.clean.txt]: "Emmanuel Macron (27,84%) et Marine Le Pen (23,15%) sont les deux qualifiés pour le second tour de l'élection présidentielle."
QUOTE[lcp.clean.txt]: "Jean-Luc Mélenchon, qui se présentait pour la troisième fois à la magistrature suprême, affiche son plus haut score, avec 21,95% des voix."
QUOTE[lcp.clean.txt]: "Éric Zemmour termine à la quatrième place avec 7,07%."
QUOTE[lcp.clean.txt]: "Selon les chiffres définitifs publiés par le ministère de l'Intérieur"
NOTE: [stated] LCP dated Monday 11 April 2022 (updated 14:46), i.e. the Interior Ministry's figures before the Conseil's proclamation of 13 April. [measured] Percentages recomputed from the Conseil's counts and suffrages exprimés 35,132,947: Macron 9,783,058 = 27.846% (27.85), Le Pen 8,133,828 = 23.152% (23.15), Mélenchon 7,712,520 = 21.952% (21.95), Zemmour 2,485,226 = 7.074% (7.07). So Macron differs in the last digit (27.84 Interior/LCP versus 27.85 from the Conseil's final counts); the others agree. The Interior's own number for Macron in LCP is 9,785,578 votes, the Conseil's 9,783,058, so the two counts differ slightly ([inferred] because of the Conseil's annulments: its decision lists communes and polling stations whose ballots it cancelled).
QUOTE[dl/cc2022.clean.txt]: "M. Emmanuel MACRON : 9 783 058"

#### [B] B-18 | §2 | Gap Le Pen minus Melenchon = 1.20 points; "The page gave no vote counts for Le Pen; the vote gap is therefore not stated" (line 65)
MARK: corrected (vote counts and gap now found)
SOURCE: https://www.conseil-constitutionnel.fr/decision/2022/2022195PDR.htm (local: dl/cc2022.clean.txt) ; Décision n° 2022-195 PDR du 13 avril 2022, Article 1er. Also LCP (quoting a deputy's tweet).
QUOTE[dl/cc2022.clean.txt]: "Mme Marine LE PEN : 8 133 828"
QUOTE[dl/cc2022.clean.txt]: "M. Jean-Luc MÉLENCHON : 7 712 520"
QUOTE[dl/cc2022.clean.txt]: "Suffrages exprimés : 35 132 947"
QUOTE[lcp.clean.txt]: "Voilà. Seulement 421 420 voix séparent Jean-Luc Mélenchon de Marine Le Pen. Rien. Aux 7 714 949 qui ont saisi l’occasion historique que fournissait le bulletin de vote Mélenchon, je dis bravo et merci !"
CORRECTION: gap "not stated" -> Conseil constitutionnel's final counts: Le Pen 8,133,828; Mélenchon 7,712,520; gap = 8,133,828 - 7,712,520 = 421,308 votes [measured]; 421,308 / 35,132,947 = 1.199% of suffrages exprimés, which matches the 1.20 points. The percentage gap 23.15 - 21.95 = 1.20 [measured] is right. Interior's earlier figures quoted in LCP (a tweet by the deputy Adrien Quatennens, as LCP says) give Mélenchon 7,714,949 and a gap of 421,420; that is a politician's tweet quoted by a news page, on the pre-proclamation count, 112 votes more than the Conseil's final gap. For the model use the Conseil's.
NOTE: Other numbers in the same decision: électeurs inscrits 48,747,876; votants 35,923,707; bulletins blancs 543,609; bulletins nuls 247,151; suffrages exprimés 35,132,947. Macron 9,783,058, Zemmour 2,485,226. Date of the decision: rendu public le 13 avril 2022, JORF n°0088 du 14 avril 2022, texte n° 1 (page footer). The Interior Ministry's own results page (info.gouv.fr) returned a Cloudflare "Just a moment..." page (HTTP 403): unread, not circumvented.
QUOTE[dl/cc2022.clean.txt]: "Rendu public le 13 avril 2022."
QUOTE[dl/cc2022.clean.txt]: "JORF n°0088 du 14 avril 2022, texte n° 1"

#### [B] B-19 | §2 | "The outcome she can change is 'which candidate wins', but through a longer chain: first-round vote, then who is in the runoff, then who wins it" (line 53)
MARK: confirmed
SOURCE: bouton.txt ; Sec. 3.1.2 opening, printed p. 10
QUOTE[bouton.txt]: "The …rst round in‡uences the …nal result either directly (if one candidate wins outright) or indirectly (through the identity of the candidates participating in the second round)."
NOTE: [stated] "In runo¤ elections, a ballot may be pivotal in both rounds." (Sec. 3, printed p. 9). Caveat already in B-02: in the model the two rounds have separate electorates, so "a voter has two votes" is the first pass's gloss, not Bouton's model.
QUOTE[bouton.txt]: "In runo¤ elections, a ballot may be pivotal in both rounds."

#### [B] B-20 | §2 | (a) "The second-round pivot probability is the two-candidate probability for the two finalists" (line 69, inferred)
MARK: confirmed [stated] for the structure
SOURCE: bouton.txt ; text after Lemma 2, printed p. 39 (page image pdf p. 40)
QUOTE[bouton.txt]: "Lemma 2 reformulates a known result for two-candidate elections (as is the second round)"
NOTE: [stated] Bouton says the second-round result is the known two-candidate result. The remainder of (a), (b) and (c) of line 69 is the first pass's reading; I found nothing in Bouton that contradicts it, and nothing that gives the ratio to a plurality race either (Bouton compares equilibria, not pivot sizes against plurality; "Not quantified in any source I read" stands).

---

#### [B] B-21 | §2 | Lepelley, Chantreuil & Berg, "The likelihood of monotonicity paradoxes in run-off elections", Math. Soc. Sci. 31 (1996) 133-146; copy at rangevoting.org (line 67)
MARK: confirmed
SOURCE: https://www.rangevoting.org/LepelleyBergRunoffMonoParadox.pdf (local: lepelley.txt) ; title page and running heads
QUOTE[lepelley.txt]: "Mathematical Social Sciences 31 (1996) 133-146"
QUOTE[lepelley.txt]: "The likelihood of monotonicity paradoxes in run-off elections"
NOTE: [stated] Authors on the title page: Dominique Lepelley, Frédéric Chantreuil, Sven Berg (OCR prints them letter-spaced); "Received February 1995; revised September 1995".

#### [B] B-22 | §2 | "Three candidates only ('limited to the three-alternative cases'), 'impartial anonymous culture'" (line 67)
MARK: confirmed
SOURCE: lepelley.txt ; Sec. 2 (p. 136) and Sec. 4 (p. 143)
QUOTE[lepelley.txt]: "Although the results given here are limited to the three-alternative cases"
QUOTE[lepelley.txt]: "Note that the underlying probabilistic assumption of this approach is the so-called 'impartial anonymous culture' condition"
NOTE: [stated] The paper's definition of vulnerability: "the proportion of voting situations in which f is vulnerable to M, i.e. the proportion of situations that can give rise to M under f." A "voting situation" is the vector (n_1..n_6) of numbers of voters holding each of the six strict preference orders on {a,b,c} with sum n. Under IAC every such vector (not every sequence of voters) is equally likely; |S| = (n+1)(n+2)(n+3)(n+4)(n+5)/120 (eq. 1) [measured: for n = 24, |S| = 118,755]. The paper ignores ties: "we ignore the problem of tied elections: we assume that one and only one alternative is eliminated in the first stage as well as in the second." The two systems are f1 = plurality with run-off (eliminate the alternative with fewest first places, then plurality between the remaining two) and f2 = anti-plurality with run-off (Coombs: eliminate the alternative with most last places). [inferred] With three alternatives f1 gives the same winner as Bouton's two-round system with a 50% threshold when voters vote sincerely; f2 is not a system used in public elections (the paper treats it as the comparison system).
QUOTE[lepelley.txt]: "we ignore the problem of tied elections"

#### [B] B-23 | §2 | Abstract: "A monotonicity paradox occurs when a voting system reacts in a perverse way to a change in individual opinions." (line 67)
MARK: confirmed
SOURCE: lepelley.txt ; Abstract
QUOTE[lepelley.txt]: "A monotonicity paradox occurs when a voting system reacts in a perverse way to a"
QUOTE[lepelley.txt]: "change in individual opinions."
NOTE: [stated] The abstract continues: "The vulnerability of a voting system to monotonicity paradoxes is defined as the proportion of voting situations that can give rise to such paradoxes." (line-broken in the file). Paradox definitions: "Paradox M1 (or the more-is-less paradox): the winner is ranked higher by one or more individuals (all else unchanged) and becomes a loser." and "Paradox 1t42 (or the less-is-more paradox): a loser is ranked lower by one or more voters (all else unchanged) and becomes a winner." (OCR "1t42" is "M2").
QUOTE[lepelley.txt]: "Paradox M1 (or the more-is-less paradox): the winner is ranked higher by one or more individuals (all else unchanged) and becomes a loser."

#### [B] B-24 | §2 | Plurality run-off, large n: M1 (more-is-less) 13/288 = 0.0451 (Cor. 1) (line 67)
MARK: confirmed
SOURCE: lepelley.txt ; Corollary 1, p. 136 (page image pdf p. 4: "lim V11(n) = 13/288 ≅ 0.0451")
QUOTE[lepelley.txt]: "and lim,,._,® Vll(n ) = 13/'288 ~ 0.0451."
NOTE: [measured] 13/288 = 0.045139 (python). The closed form for finite n, "for n in {24, 36, 48, 60, ...}" (multiples of 12): V11(n) = n(26n^4 - 325n^3 - 760n^2 + 9360n + 19584) / (576 (n+1)(n+2)(n+3)(n+4)(n+5)); its leading ratio 26/576 = 13/288. I checked it reproduces Table 2's V11 at n = 24, 48, 60, 120, 192 to five digits [measured]. Internal misprint in the paper [measured]: Corollary 1 prints the constant 19584 but the proof's eq. (4) prints |Y'| = n(26n^4 - 325n^3 - 760n^2 + 9360n + 19585)/414720; I counted the integer points of the inequality set (2) by brute force for n = 24, 36, 48 (228; 2,420; 11,666) and they equal the formula with 19584, so 19585 in eq. (4) is a misprint (page image pdf p. 5 shows 19585; pdf p. 4 shows 19584). It does not affect the quoted limits.

#### [B] B-25 | §2 | Plurality run-off, large n: M2 (less-is-more) 17/864 = 0.0197 (Cor. 3) (line 67)
MARK: confirmed
SOURCE: lepelley.txt ; Corollary 3, p. 139
QUOTE[lepelley.txt]: "and limn_,® V12(n) = 17/864 ~ 0.0197."
NOTE: [measured] 17/864 = 0.019676. Finite-n form V12(n) = n(17n^4 - 495n^3 + 4200n^2 - 6480n - 24192) / (864 (n+1)...(n+5)); it reproduces Table 2's V12 column at n = 24, 36, 48, 60, 120, 192 [measured].

#### [B] B-26 | §2 | Either paradox under plurality run-off: 397/6912 = 0.0574 (Sec. 3.1) (line 67)
MARK: confirmed; arithmetic checked
SOURCE: lepelley.txt ; Sec. 3.1 "Global vulnerability", p. 141 (page image pdf p. 9)
QUOTE[lepelley.txt]: "17~(o0)= 13/288 + 17/864 - 17/2304 = 397/6912 ~ 0.0574."
NOTE: [measured] 13/288 + 17/864 - 17/2304 = (312 + 136 - 51)/6912 = 397/6912 = 0.057436 (python Fractions). The subtracted term is the share of situations in which both paradoxes can occur: "(2 x 3 x 17)/13824 = 17/2304" (page image). So "either" is by inclusion-exclusion, as the first pass says. The paper's own summary line: "the proportion of situations in which monotonicity paradoxes are likely to occur in three-alternative elections with large electorates is at least 1.97% for f1 and at least 5.56% for f2" is a lower bound made of two cells only: M2 under f1 (17/864 = 1.97%) and M1 under f2 (1/18 = 5.56%), the cases the paper argues every paradoxical situation can be justified by strategic arguments (Sec. 3.2); that is a different quantity from the 5.74%.
QUOTE[lepelley.txt]: "at least 1.97% for fx and at least 5.56% for f2."

#### [B] B-27 | §2 | Anti-plurality run-off, large n: 1/18 = 0.0556 (M1, Cor. 2), 7/108 = 0.0648 (M2, Cor. 4), either 151/1296 = 0.1165 (line 67)
MARK: confirmed; the "70.1165" typo resolved
SOURCE: lepelley.txt ; Corollaries 2 and 4, pp. 138-139; Sec. 3.1, p. 141 (page image pdf p. 9)
QUOTE[lepelley.txt]: "a n d lim,__,® V21(n) = 1/18 --- 0.0556."
QUOTE[lepelley.txt]: "and lim,_,® V22(n) = 7/108 ~ 0.0648."
QUOTE[lepelley.txt]: "172(00) = 1/18 + 7/108 - 5/1296 = 151/1296 70.1165."
CORRECTION: the OCR's "70.1165" -> the page image prints "151/1296 ≅ 0.1165" (the "7" is the OCR's rendering of the "≅" sign; same OCR artefact appears as "~" elsewhere). So the value is 0.1165, as the first pass had it.
NOTE: [measured] 1/18 = 0.055556; 7/108 = 0.064815; 1/18 + 7/108 - 5/1296 = (72 + 84 - 5)/1296 = 151/1296 = 0.116512. Paper's comparison sentence: "the global vulnerability of f2 to monotonicity paradoxes is twice as high as the global vulnerability of f1" (0.1165 / 0.0574 = 2.03 [measured]). Table 2's limit row prints 0.04514, 0.05556, 0.01968, 0.06481 for V11, V21, V12, V22, consistent with these fractions.

#### [B] B-28 | §2 | Table 2 (plurality run-off, M1): n = 24, 0.01152; n = 60, 0.02781; n = 120, 0.03568; n = 192, 0.03903 (line 67)
MARK: confirmed (column V11(n); checked on the page image pdf p. 8)
SOURCE: lepelley.txt ; Table 2, p. 140
QUOTE[lepelley.txt]: "24 0.01152 0.02274 0.00202 0.03739"
QUOTE[lepelley.txt]: "60 0.02781 0.03848 0.00898 0.05237"
QUOTE[lepelley.txt]: "120 0.03568 0.04615 0.01347 0.05901"
QUOTE[lepelley.txt]: "192 0.03903 0.04945 0.01557 0.06119"
NOTE: [stated] The columns are V11(n), V21(n) (paradox M1, f1 and f2) and V12(n), V22(n) (paradox M2, f1 and f2); the first column in each quoted row is n and the next is V11(n), so the first pass's four values are the V11 column and right. [measured] Two other cells in the table disagree slightly with the paper's own formulas: V11(36) is printed 0.01936 but Corollary 1 gives 0.01938; V22(60) is printed 0.05237 but Corollary 4 gives 0.05327 (0.05237 would break the monotone run 0.05046, ?, 0.05516; the image prints 0.05237). The first pass did not quote these cells. The text beside the table reads "n in {24, 34, 48, ..., 192}": 34 is a misprint for 36.
QUOTE[lepelley.txt]: "n u m b e r of individuals and the paradox), and from 2% to 6.5% for the anti-"

#### [B] B-29 | §2 | "These are shares of random profiles in which some change of opinions would cause the paradox, not the chance that one ballot does" (line 67, inferred)
MARK: confirmed [stated] by the paper's own caveat
SOURCE: lepelley.txt ; Sec. 3.2, p. 142
QUOTE[lepelley.txt]: "of situations that are potentially paradoxical: paradoxes occur if and only if some"
NOTE: [stated] full sentence: "It is important to emphasize that the results given here evaluate the proportion of situations that are potentially paradoxical: paradoxes occur if and only if some individual preferences are modified in a specific way." The paper also argues the paradox M2 under f1 "involves a modification in individual preferences that can be justified by strategic arguments" (its Example 1(i): three voters switch from b-c-a to c-b-a and the winner changes from a to b). [inferred] The first pass's remark about the sign of a vote's effect is consistent with this.

---

## 3. Ranked-choice / instant-runoff voting (RCV, IRV)

*First-pass lines 71-96 of `research/electoral-systems.md`. Each block: the first-pass claim with its line number, the mark, the source and location, exact quotes, the correction if any, notes.*

#### [E] E-01 | §3 | line 73: IRV "decisive" has two ways, both defined in Baltz (2025)
MARK: confirmed
SOURCE: https://arxiv.org/pdf/2210.01657 (local: baltz_arxiv.raw.txt; arXiv v2, 31 Jul 2023) ; Sec. 2.2 "Expected vote totals", p. 9
QUOTE[baltz_arxiv.raw.txt]: "On the one hand, it could be pivotal by causing a candidate who is ranked on the ballot to win the election. I will call this direct pivotality. On the other hand, placing a candidate in a certain position on a ballot can change the winner of the election without causing that specific candidate to win, which I will call indirect pivotality."
NOTE: [stated]. The same two-way split is in the abstract ("a voter can cause one candidate to win by ranking some other candidate on their ballot"). The published appendix (baltz_sup) does not restate the definitions in words; it says "the equation in the text" / "Equation 8 in the main article" (those equation numbers refer to the journal text, which I have not seen).

#### [E] E-02 | §3 | line 74: direct pivotality = break a first-place tie ("one vote short of winning") or create one (fair tie-break, factor 1/2)
MARK: confirmed
SOURCE: https://arxiv.org/pdf/2210.01657 (local: baltz_arxiv.raw.txt) ; Sec. 2.3 "Direct pivotality", p. 10, and p. 12-13
QUOTE[baltz_arxiv.raw.txt]: "is either a) one vote short of winning (breaking a first-place tie), or b) two votes short of winning and would win a tie-breaker (making a first-place tie)."
QUOTE[baltz_arxiv.raw.txt]: "now accounting for creating a first-place tie and not just for breaking one, and assuming a fair tie-breaker:"
NOTE: [stated]. Two details worth the orchestrator's eye. (1) The prose says the creating case is "two votes short of winning", but the printed p_direct formula (p. 13) uses P(... = 1 + ...), i.e. the candidate is one vote behind the other finalist before the ballot. I report both as printed. (2) The 1/2 factors: in the prose Baltz says the factor 1/2 represents "the event that c would lose a fair tie-breaker without the pivotal vote boosting them into first place"; in the final p_direct formula both the "tie" term and the "1+" term carry a 1/2.

#### [E] E-03 | §3 | line 75: indirect pivotality = ranking c changes the drop sequence from A to A', final winner changes though c does not win; "These are the only two ways to be pivotal, and they are mutually exclusive."
MARK: confirmed
SOURCE: https://arxiv.org/pdf/2210.01657 (local: baltz_arxiv.raw.txt) ; Sec. 2.4 p. 13-14 (Constraints 1 and 2) and Sec. 2.5 p. 17
QUOTE[baltz_arxiv.raw.txt]: "Suppose that candidates will be dropped according to the sequence A, but because a voter ranks some candidate c in position i on their ballot, instead candidates are dropped according to a different sequence A′ ."
QUOTE[baltz_arxiv.raw.txt]: "Because these are the only two ways to be pivotal, and they are mutually exclusive, the full pivotal probability p is given by p = pdirect + pindirect ."
QUOTE[baltz_arxiv.raw.txt]: "Constraint 2: The winner in A is not the winner in A′ : A−1 ̸= A′−1"
NOTE: [stated]. The first pass's sentence in quotation marks ("These are the only two ways to be pivotal, and they are mutually exclusive.") is Baltz's clause with "Because" dropped and a capital T; the words are his, the sentence is not verbatim.

#### [E] E-04 | §3 | line 76: indirect pivotality is "closely related to some well-studied phenomena (especially IRV's failure of the monotonicity criterion, and also the no-show paradox), but it is not the same as either one."
MARK: confirmed
SOURCE: https://arxiv.org/pdf/2210.01657 (local: baltz_arxiv.raw.txt) ; Sec. 1 Introduction, p. 4
QUOTE[baltz_arxiv.raw.txt]: "This phenomenon is closely related to some well-studied phenomena (especially IRV’s failure of the monotonicity criterion, and also the no-show paradox), but it is not the same as either one."
NOTE: [stated]. Baltz's footnote 4 (p. 13) gives the distinction in the "no-show" case: indirect pivotality "does not necessarily cause the victory of a more-preferred candidate" (see E-18).

#### [E] E-05 | §3 | line 78: notation (kappa, L, beta, S, A = [S_1..S_{kappa-1}, c], y, A' agreeing with A "up to c's position", "V_x the cumulative expected vote total of x given earlier drops")
MARK: corrected
SOURCE: https://arxiv.org/pdf/2210.01657 (local: baltz_arxiv.raw.txt) ; Sec. 2.1 p. 6; Sec. 2.4 p. 13-14
QUOTE[baltz_arxiv.raw.txt]: "Denote by vc the expected vote total of candidate c, and use µba |S1:n to represent the number of voters expected to rank candidate a in any of the ballot positions between 1 and b, given that they assigned every higher ballot position to some candidate in the sequence S1:n"
QUOTE[baltz_arxiv.raw.txt]: "When considering a sequence of candidates dropped before some candidate c of interest, I will use A ≡ [S1 , S2 , · · · Sκ−1 , c]."
QUOTE[baltz_arxiv.raw.txt]: "Constraint 1: A and A′ are the same up to the pivotal event: for some y, A1:y−1 = A′1:y−1"
CORRECTION: "V_x, the cumulative expected vote total" -> the paper's symbols are v_c (the expected vote total of c) and mu^b_a | S_{1:n} (the number of voters expected to rank a in positions 1..b given higher positions went to candidates in S_{1:n}); a candidate's total after d drops is v_c = sum_{q=0}^{d} mu^{q+1}_c | S_{1:q} (p. 9). "A' agrees with A up to c's position" -> Constraint 1 as printed: A_{1:y-1} = A'_{1:y-1} (they agree up to position y-1, where y is the index of c in A).
NOTE: kappa = number of candidates, L = ballot length ("a voter may make L choices"), beta = the ballot, i indexes ballot positions, S = the sequence of previously dropped candidates, S_{-1} = S_{kappa-1}, "round" = each act of comparing vote totals: all as first pass says. The notation V_x is not in the paper (extractor artefact). A printed inconsistency to know about: Constraint 1 says A and A' agree up to y-1 and t = A'_y differs from c = A_y, but p. 18 defines the set of alternative sequences as formed "by pre-pending A1:y to G" (so position y would be c). I cannot say which is intended; see FORMULAS AS PRINTED.

#### [E] E-06 | §3 | line 79: p = p_direct + p_indirect
MARK: confirmed
SOURCE: https://arxiv.org/pdf/2210.01657 (local: baltz_arxiv.raw.txt) ; Sec. 2.5 p. 17 (image checked)
QUOTE[baltz_arxiv.raw.txt]: "the full pivotal probability p is given by p = pdirect + pindirect ."
NOTE: [stated]. Baltz also stresses that all probabilities and utilities "should be understood as being implicitly compared to abstention" (p. 8; and baltz_sup §2 "The counterfactual").

#### [E] E-07 | §3 | line 80: p_direct(beta) formula (sum over i, over drop sequences S consistent with the ballot, of [product of P(V_{A_l} < V_{A_r})] x [1/2 P(tie) + 1/2 P(1 + ...)])
MARK: confirmed
SOURCE: https://arxiv.org/pdf/2210.01657 (local: baltz_arxiv.raw.txt) ; Sec. 2.3, p. 13, final displayed equation (page image looked at; transcription under FORMULAS AS PRINTED, item P-1)
QUOTE[baltz_arxiv.raw.txt]: "This is the probability that a ballot cast in an IRV election is directly pivotal for any candidate."
NOTE: The structure the first pass gave is right. Differences of detail from the printed form: (a) the quantities compared are cumulative sums of mu terms, sum_{q=0}^{l-1} mu^{q+1}_{A_l}|A_{1:q} (the sum runs to l-1 on both sides) and the tie compares sum_{q=0}^{kappa-2} mu^{q+1}_{A_{kappa-1}}|A_{1:q} with sum_{q=0}^{kappa-2} mu^{q+1}_i|A_{1:q}; (b) the product index is l = 1..kappa-2, r = l+1..kappa as first pass says; (c) A is S followed by the candidate i at ballot position i (A_kappa = i), and "beta_{1:i-1} subset of S" is the printed consistency condition ("the ith ballot position can only be pivotal if all candidates ranked higher on the ballot have been dropped", p. 12). One thing the first pass could not see: the paper's own text says the "1/2" tie-break factor accompanies the P(tie) term only in the first (break-only) version, and p. 13 adds the second tie term with "1 +".

#### [E] E-08 | §3 | line 81: p_indirect(beta) formula
MARK: confirmed
SOURCE: https://arxiv.org/pdf/2210.01657 (local: baltz_arxiv.raw.txt) ; Sec. 2.4, p. 16 (in terms of v) and p. 17 (in terms of mu) (page images looked at; transcription under FORMULAS AS PRINTED, items P-2 and P-3)
QUOTE[baltz_arxiv.raw.txt]: "The result is the indirect pivotal probability of the ballot in terms of the candidates’ vote totals:"
QUOTE[baltz_arxiv.raw.txt]: "A denote the set of all A′ that, for a given A, fulfill Conditions 1 and 2"
NOTE: Structure matches the first pass. Printed oddities I found, none of which I resolved (reported, not repaired): (1) p. 16 (v-version) sums over "t in F" with F never defined in the text, whereas p. 17 (mu-version) has no sum over t (t is "the candidate in A'_y", p. 18); (2) in the p. 17 formula the first product's inner sums run to h-1 on both sides, P(sum_{q=0}^{h-1} mu_{A_l} > sum_{q=0}^{h-1} mu_{A_h}), where p_direct uses l-1; (3) the p_not-d(A -> A') display at the top of p. 16 prints the second tie term as "P(v_c^y = v_t^y = -1)" (apparently a typo for v_t^y - 1, which pp. 14, 15, the second display of p. 16, and p. 17 print); (4) the sum over A' is over the set bold-A "formed by pre-pending A_{1:y} to G" (p. 18) while Constraint 1 says agreement up to y-1 (see E-05).

#### [E] E-09 | §3 | line 82: expected utility multiplies each by the payoff difference u(i) - u(S_{-1}) (direct), u(A'_{-1}) - u(A_{-1}) (indirect)
MARK: confirmed
SOURCE: https://arxiv.org/pdf/2210.01657 (local: baltz_arxiv.raw.txt) ; Sec. 2.5 p. 17
QUOTE[baltz_arxiv.raw.txt]: "that latter factor in direct pivotality is u(c) − u(S−1 ), while in indirect pivotality it is u(A′−1 ) − u(A−1 )."
NOTE: [stated]. The displayed u(beta) (p. 18) uses u(i) - u(S_{-1}) for the direct term and u(A'_{-1}) - u(A_{-1}) for the indirect one, as first pass says. The supplement (baltz_sup §2) adds that this "omits any cost T associated with the act of voting" and that a reader who wants it "could instead compute: u(beta) = P_pivotal(beta) . u_pivotal(beta) - T" (supplement p. 2; that is Baltz's own cost term, relevant to the site).

#### [E] E-10 | §3 | line 83 (first part): modelling by Skellam probabilities under Poisson voting games, following Mebane et al. (2019)
MARK: confirmed
SOURCE: https://arxiv.org/pdf/2210.01657 (local: baltz_arxiv.raw.txt) ; Sec. 2.6, p. 19
QUOTE[baltz_arxiv.raw.txt]: "Following Mebane et al. (2019), if the number of voters is drawn from a Poisson distribution, then the number of voters with a preference ordering following each possible preference ordering will also follow a Poisson distribution with known parameter, and their difference follows the Skellam distribution."
NOTE: [stated]. The Skellam function itself (S(w, a, b)) is never written out in either version: it is used as a named function. In the supplement worked example the author defines C(a,b) = sum_{w=0}^{infinity} S(w,a,b) "which is the probability that a > b when a, b are random variables following the Poisson distribution" (supplement p. 8). So the Poisson *means* are the expected numbers of voters of each ballot type (the worked example uses first-place counts 2, 2, 3, 6, 12 as means). He also says "Dirichlet beliefs" could replace the Poisson (p. 19).

#### [E] E-11 | §3 | line 83 (second part): Assumptions 1 and 2 (independence of pairwise comparisons within and across rounds)
MARK: confirmed
SOURCE: https://arxiv.org/pdf/2210.01657 (local: baltz_arxiv.raw.txt) ; Sec. 2.1, p. 6-8 (Assumption lines: page image p. 7 looked at, see FORMULAS AS PRINTED item A-1)
QUOTE[baltz_arxiv.raw.txt]: "Assumption 1 says that any two pairwise comparisons of vote totals are independent, even conditional on any set of candidates having been dropped and any relative ordering of other vote totals. Assumption 2 says that the vote totals of two candidates in some round is unrelated to the vote totals of those or other candidates in another round."
QUOTE[baltz_arxiv.raw.txt]: "Substantively, these assumptions are not entirely reasonable; however, I will argue that a) they are at least as reasonable as any alternative assumptions, b) they are necessary for exposition, and c) their limitations do not in any way seriously limit the article’s results."
NOTE: [stated]. The first pass put "which it describes as simplifying" in quotation marks; that phrase is not in the paper. The paper's closest words: "we took Assumptions 1 and 2 specifically to simplify the exposition of the equation, even to a point that strains substantive credibility" (p. 18-19; quoted in E-12's file check below). Baltz also says Assumption 1 "is a feature of the Poisson voting games framework" while Assumption 2 "is more challenging, because it is not a familiar assumption, and it is not obvious why we should accept it" (p. 7). Footnote 2 (p. 8): without them one must "introduce a term that gives the probability of these two events occurring. This will produce results identical to the probability that I derive in this paper, up to multiplication of each term by some real number." (that is, the independence products are not innocuous: see the Reconciliation section for a measured size.)
QUOTE[baltz_arxiv.raw.txt]: "we took Assumptions 1 and 2 specifically to simplify the exposition of the equation, even to a point that strains substantive credibility."
QUOTE[baltz_arxiv.raw.txt]: "This will produce results identical to the probability that I derive in this paper, up to multiplication of each term by some real number."

#### [E] E-12 | §3 | line 83 (third part): the "apparent faster decline in IRV as candidates increase" "may be attributable to the varying quality of Assumption 2"
MARK: confirmed
SOURCE: https://arxiv.org/pdf/2210.01657 (local: baltz_arxiv.raw.txt) ; footnote 6, p. 25 (same text in the supplement, footnote 5, p. 19)
QUOTE[baltz_arxiv.raw.txt]: "However, I strongly caution against reading substantively into the appearance that pivotal probabilities in IRV fall more quickly as the number of candidates rises than pivotal probabilities in SMDP, since this result may be attributable to the varying quality of Assumption 2 as more candidates are introduced."
QUOTE[baltz_sup.raw.txt]: "However, I strongly caution against reading substantively into the appearance that pivotal probabilities in IRV fall more quickly as the number of candidates rises than pivotal probabilities in SMDP, since this result may be attributable to the varying quality of Assumption 2 as more candidates are introduced."
NOTE: [stated]. The first pass's phrase "the apparent faster decline in IRV" is its paraphrase of "the appearance that pivotal probabilities in IRV fall more quickly as the number of candidates rises". Reading Fig. 1 (published version, mean lines read off the plot, approximate): uniform panel IRV 0.083 -> 0.061 -> 0.033 for 3, 4, 5 candidates versus SMDP 0.052 -> 0.052 -> 0.043, so the "faster decline" is visible in the uniform panel; in the power-law panel the means on the log axis are IRV about -5.9, -5.9, -5.6 and SMDP about -7.6, -8.3, -8.9, which declines for SMDP and not for IRV (the opposite direction). The author's caution is the only statement on it.

#### [E] E-13 | §3 | line 84: supplementary file of the published paper (URL listed by search but not read)
MARK: confirmed
SOURCE: https://static.cambridge.org/content/id/urn%3Acambridge.org%3Aid%3Aarticle%3AS1047198724000329/resource/name/S1047198724000329sup001.pdf (local: baltz_sup.raw.txt; downloaded by the orchestrating thread, 24 pages) ; p. 1
QUOTE[baltz_sup.raw.txt]: "Appendix September 4, 2024"
NOTE: Now read whole; see F-1. It is the Appendix to the journal "letter" ("the approach that I take in this letter").

#### [E] E-14 | §3 | line 86: published estimates: IRV "very slightly higher ... (averaging about 10^-6 compared to about 10^-7 ...)" for power-law; uniform: IRV "may be slightly higher ... when there are only 3 candidates, but when there are 4 or 5 candidates neither is clearly larger"
MARK: confirmed
SOURCE: https://arxiv.org/pdf/2210.01657 (local: baltz_arxiv.raw.txt) ; Sec. 4, p. 25 (same wording in the supplement, §9, p. 19)
QUOTE[baltz_arxiv.raw.txt]: "When support for candidates resembles a power law distribution, IRV has very slightly higher pivotal probabilities than SMDP (averaging about 10−6 compared to about 10−7 with these particular preference structures). In the case of uniformly distributed support, the chances to be pivotal in IRV may be slightly higher than in SMDP when there are only 3 candidates, but when there are 4 or 5 candidates neither is clearly larger than the other."
QUOTE[baltz_sup.raw.txt]: "When support for candidates resembles a power law distribution, IRV has very slightly higher pivotal probabilities than SMDP (averaging about 10−6 compared to about 10−7 with these particular preference structures)."
NOTE: [stated]; and my reading of the Figure ([measured] off the image; see Reconciliation). The "about 10^-6 / about 10^-7" are for the **power-law panel only**, which is drawn on a log10 axis labelled "Pivotal probability (Log10)". On the published version of that panel (supplement p. 18) the plotted per-setting mean lines sit at about -7.6, -8.3, -8.9 (SMDP, 3/4/5 candidates; the first is pixel-verified at -7.56) and about -5.9, -5.9, -5.6 (IRV), so the SMDP means are about 10^-7.6, 10^-8.3 and 10^-8.9 for 3, 4, 5 candidates (about 4x, 20x and 80x below 10^-7) and the IRV means about 1.3 to 2.5 times 10^-6; the paper says "about" and does not state which average or for which candidate count. These lines sit well below the arithmetic mean of the plotted points (the highest IRV point at 3 candidates is about 10^-2.9, alone worth 10^-4.9 in a mean of 100), so they are means of log10 values (geometric means) [inferred from the picture]. The uniform panel is on a linear axis, 0 to 0.12, and its mean lines (approximate, read by eye from the supplement's figure) are SMDP about 0.052, 0.052, 0.043 and IRV about 0.083, 0.061, 0.033 for 3, 4, 5 candidates. The arXiv v2 figure has the same dots without the mean lines. The published text adds: "IRV exhibiting slightly lower variance" (supplement p. 19).
QUOTE[baltz_sup.raw.txt]: "There are differences, including IRV having a slightly higher pivotal probability overall and IRV exhibiting slightly lower variance."

#### [E] E-15 | §3 | line 86 (last sentence): Abstract: "These simulations produce similar estimated pivotal probabilities in the two systems."
MARK: unread
SOURCE: (the sentence is attributed by the first pass to the journal abstract page; that page is on cambridge.org, which my task does not allow me to request)
QUOTE[baltz_arxiv.raw.txt]: "The result is very similar to the probability of casting a pivotal vote in a Single-Member District Plurality election, which suggests that Instant Runoff Voting does not actually increase or decrease voters’ incentives to vote strategically."
NOTE: [stated] The sentence quoted by the first pass is **not in the arXiv v2 abstract** (and not anywhere in the arXiv or supplement text; searched). The arXiv v2 abstract is the quote above. The journal abstract may have been rewritten for the letter; I cannot confirm either way. So the first-pass quotation is unconfirmed, not wrong. The arXiv abstract also says "I derive the probability that a vote cast in an Instant Runoff Voting election will change the election winner" and "I estimate its magnitude for different distributions of voter preferences".

#### [E] E-16 | §3 | line 94 (first sentence): size relative to a two-candidate race: "similar" in simulations of 1,000 voters with 3-5 candidates
MARK: confirmed
SOURCE: https://arxiv.org/pdf/2210.01657 (local: baltz_arxiv.raw.txt) ; Sec. 4, p. 25; Conclusion, p. 26
QUOTE[baltz_arxiv.raw.txt]: "The striking feature of Figure 1 is that IRV and SMDP have extremely similar pivotal probabilities."
QUOTE[baltz_arxiv.raw.txt]: "The probability that some ballot in an IRV election will be pivotal is very similar to the probability that some ballot in an SMDP election will be pivotal."
NOTE: [stated]. Important for how the site reads "similar": it is similar **between IRV and SMDP on the paper's own stylised electorates**; neither version compares either with a two-candidate race. The published appendix is more cautious: "these are stylized figures meant to illustrate how my derivations could be applied in the presence of actual preference data" and that the two systems' probabilities "often coincide up to the order of magnitude or even the decimal place" (p. 19).
QUOTE[baltz_sup.raw.txt]: "However, these are stylized figures meant to illustrate how my derivations could be applied in the presence of actual preference data."

#### [E] E-17 | §3 | line 94 (rest): [inferred] "indirect pivotality has no counterpart in plurality; in Baltz's stylised cases the totals come out similar, so the extra route does not change the order of magnitude there"
MARK: confirmed
SOURCE: https://arxiv.org/pdf/2210.01657 (local: baltz_arxiv.raw.txt) Conclusion p. 25; https://static.cambridge.org/... S1047198724000329sup001.pdf (local: baltz_sup.raw.txt) §5 p. 12
QUOTE[baltz_arxiv.raw.txt]: "Indirect pivotality may be rare, but it is easy to provide examples of small-electorate contests in which the election may be decided by an indirectly pivotal vote choice."
QUOTE[baltz_sup.raw.txt]: "The probability of this particular example of indirect pivotality was found to be an order of magnitude smaller than the probability of the direct pivotality example, consistent with the fact that indirect pivotality requires a much more specific situation to occur."
NOTE: [stated] for Baltz's words; [inferred] for the first pass's sentence. Nothing in either version gives the size of p_indirect relative to p_direct in the Figure 1 simulations: Figure 1 plots only the sum. The worked example (a 25-voter, 5-candidate electorate) gives 0.023 for one direct drop sequence and 0.003 for one indirect event; my recomputation is in the FORMULAS section (the direct figure reproduces; the indirect one reproduces only under one reading).

#### [E] E-18 | §3 | line 96: [inferred] "in the indirect-pivotality term, Baltz's expected-utility rule u(A'_{-1}) - u(A_{-1}) can be negative for a given ballot"
MARK: confirmed
SOURCE: https://arxiv.org/pdf/2210.01657 (local: baltz_arxiv.raw.txt) ; footnote 4, p. 13-14; supplement p. 5
QUOTE[baltz_arxiv.raw.txt]: "and second, it does not necessarily cause the victory"
QUOTE[baltz_sup.raw.txt]: "second, it does not necessarily cause the victory of a more-preferred candidate."
NOTE: in the arXiv file the footnote runs across the page break (p. 13 ends "it does not necessarily cause the victory", p. 14 continues "of a more-preferred candidate."); the supplement has it on one page. [stated] by Baltz that an indirectly pivotal ballot need not elect a more-preferred candidate; the sign claim is then arithmetic (u(A'_{-1}) - u(A_{-1}) is a difference of the voter's utilities of two winners). "How often the sign is wrong for one ballot is not in any source I read" is also true of both Baltz versions: neither computes it.

#### [E] E-25 | §3 | line 89: citation "Ornstein & Norman, 'Frequency of monotonicity failure under Instant Runoff Voting: estimates based on a spatial model of elections', Public Choice 161 (2014) 1-9"
MARK: confirmed
SOURCE: https://www.rangevoting.org/OrnsteinNormanMonotonicityIRV.pdf (local: ornstein.raw.txt) ; p. 1
QUOTE[ornstein.raw.txt]: "Public Choice (2014) 161:1–9 DOI 10.1007/s11127-013-0118-2"
QUOTE[ornstein.raw.txt]: "Frequency of monotonicity failure under Instant Runoff Voting: estimates based on a spatial model of elections"
NOTE: [stated]. Received 5 Oct 2012, accepted 7 Sept 2013, published online 17 Oct 2013 (printed on p. 1). The first pass's "(a copy on a third-party site ... I did not check it against the journal)": the file carries Springer's typesetting, but I too have not compared it with the publisher's page.

#### [E] E-26 | §3 | line 89: definition: upward failure is where "the IRV winner would lose if ranked higher by some subset of voters"
MARK: confirmed
SOURCE: https://www.rangevoting.org/OrnsteinNormanMonotonicityIRV.pdf (local: ornstein.raw.txt) ; Sec. 1 (p. 2) and Sec. 3 (p. 3, page image looked at)
QUOTE[ornstein.raw.txt]: "is characterized as a situation in which the IRV winner would lose if ranked higher by some subset of voters."
QUOTE[ornstein.raw.txt]: "We term the former paradox an upward monotonicity failure, and the latter a downward monotonicity failure."
QUOTE[ornstein.raw.txt]: "An election profile P exhibits an upward monotonicity failure if there exists a profile"
NOTE: [stated]. The formal Sec. 3 definition (printed, page image p. 3): P exhibits an upward failure "if there exists a profile P' that is identical to P except that candidate A is ranked higher by a subset of voters, but candidate A is not the IRV winner", with P' = <a1 + lambda1 + lambda2, a2, b1 - lambda1, b2 - lambda2, c1, c2> (A the IRV winner, C the candidate with the fewest first-place votes). The first pass's "(Sec. 1/3)" is right. The definition is about *a subset of voters* moving, so it is a property of the whole profile, not of one ballot; the paper makes no per-ballot statement (as the first pass says).

#### [E] E-27 | §3 | line 89: method: 2-D spatial model, three adaptive candidates, 1,001 voters, four voter distributions, 5,000 elections each
MARK: confirmed
SOURCE: https://www.rangevoting.org/OrnsteinNormanMonotonicityIRV.pdf (local: ornstein.raw.txt) ; Sec. 4, pp. 4-5; captions of Figs. 2-5, pp. 7-8
QUOTE[ornstein.raw.txt]: "The model we develop here is a two-dimensional spatial model"
QUOTE[ornstein.raw.txt]: "We model candidates as boundedly rational adaptive agents"
QUOTE[ornstein.raw.txt]: "All three candidates begin the election at random positions in the voter distribution"
QUOTE[ornstein.raw.txt]: "Voters’ ideal points are randomly seeded across the issue space using one of four stylized distributions."
QUOTE[ornstein.raw.txt]: "Since outcomes are stochastic, we model 5,000 elections for each type of voter distribution (varying by the number of periods that candidates may move during each election, L)."
QUOTE[ornstein.raw.txt]: "Each election is parameterized with 1,001 voters, though outcomes are robust to halving or doubling this value, or setting V even or odd."
QUOTE[ornstein.raw.txt]: "Values derived from 5,000 simulated elections for each value of L (ties excluded)"
NOTE: [stated]. "5,000 elections each" needs a qualifier: 5,000 per voter distribution **and per value of the simulation length L** (figure captions 2-4: "for each value of L"); Fig. 5 uses "500,000 runs of the simulation for each distribution" (caption). The four distributions are: base case (Gaussian, sd 0.25), Balanced Polarized, Unbalanced Polarized (1.5 times as likely in one camp) and Multiparty (p. 5). The paper says "The simulation code is available from the authors on request" (not read). Voters rank by Euclidean distance, 2 issues; candidates move by 0.01 increments to maximise first-place votes using "periodic polling". The paper's own scope limit: "We restrict our attention in this paper to the three-candidate case for largely pragmatic reasons" (p. 8-9).
QUOTE[ornstein.raw.txt]: "We restrict our attention in this paper to the three-candidate case for largely pragmatic reasons"

#### [E] E-28 | §3 | line 89: results "anywhere from 0.7 % to 51 % of all cases"
MARK: confirmed
SOURCE: https://www.rangevoting.org/OrnsteinNormanMonotonicityIRV.pdf (local: ornstein.raw.txt) ; Sec. 5, p. 6
QUOTE[ornstein.raw.txt]: "the simulated elections exhibit monotonicity failure in anywhere from 0.7 % to 51 % of all cases"
NOTE: [stated]. Context: "Depending on the type of voter distribution and length of the simulation". The same paragraph breaks it down: Unbalanced Polarized about 50% at L > 40; Base Case and Balanced Polarized 9% to 12%; Multiparty "a lower bound of 0.7 %".

#### [E] E-29 | §3 | line 89 and §10.3 item 2: "between 15 % and 51 % of competitive elections (excluding ties, which account for approximately 1.1 % of simulated elections)"
MARK: confirmed
SOURCE: https://www.rangevoting.org/OrnsteinNormanMonotonicityIRV.pdf (local: ornstein.raw.txt) ; Sec. 5, p. 6; Abstract p. 1; Sec. 6 p. 8
QUOTE[ornstein.raw.txt]: "between 15 % and 51 % of competitive elections (excluding ties, which account for approximately 1.1 % of simulated elections)."
QUOTE[ornstein.raw.txt]: "results suggest a lower bound estimate of 15 % for competitive elections"
QUOTE[ornstein.raw.txt]: "Indeed, competitive simulated elections exhibited montonicity failure at least 15 % of the time for all parameterizations (Fig. 4)."
NOTE: [stated]. The first pass's §10.3 item 2 wording ("15% to 51% of simulated competitive three-candidate IRV elections have an upward failure available to some group of voters") is accurate. For the Multiparty distribution the paper says its competitive elections "exhibit monotonicity failure roughly 20 % of the time". The paper's own caveat on what the 15% is: "represents a testable prediction of the model" (Sec. 6).

#### [E] E-30 | §3 | line 89: "competitive" is a vote-count condition (c > (V+2)/4), not a margin
MARK: confirmed
SOURCE: https://www.rangevoting.org/OrnsteinNormanMonotonicityIRV.pdf (local: ornstein.txt, layout; ornstein.raw.txt) ; Sec. 3, p. 3 eq. (1) (page image looked at) and Sec. 5, p. 8
QUOTE[ornstein.txt]: "The first is that P must be a competitive election, defined as a profile in which"
QUOTE[ornstein.txt]: "2 For convenience, we define c = c + c ."
QUOTE[ornstein.raw.txt]: "competitive ratio (defined as the ratio of first-place votes received by candidate C to first-place votes received by candidate A; elections with higher ratios are more competitive)"
NOTE: [stated]. Printed equation (1), seen in the page image: c > (V + 2) / 4, with c = c1 + c2 (footnote 2), where C is the candidate with the fewest first-place votes and V the number of voters (text extracts garble the fraction). So "competitive" = the third-placed candidate has more than a quarter of the votes (plus a half vote): a three-way-race condition, not a margin; the first pass's [inferred] reading is right. The paper's separate Fig. 5 measure, "competitive ratio" = first-place votes of C divided by those of A, is a different, continuous quantity. Condition (2) printed: c + b2 > V/2 (C preferred to A by a majority).

#### [E] E-31 | §3 | line 89: contrasts Allard (1996), who estimated failure "only about once per century" for a UK general election
MARK: confirmed
SOURCE: https://www.rangevoting.org/OrnsteinNormanMonotonicityIRV.pdf (local: ornstein.raw.txt) ; Sec. 1, p. 2; and see F-3 for what Allard's paper says
QUOTE[ornstein.raw.txt]: "One study (Allard 1996) suggests that, if the United Kingdom adopted IRV for its general elections, this paradox would occur only about once per century."
NOTE: [stated] that this is what O&N write. **Allard's paper (read, F-3) is not about IRV**: it is about STV in multi-member constituencies, and it counts only failures that change a party's seat count at the final stage. See F-3 for quotes. So the first pass's "Allard (1996), who estimated failure ... for a UK general election" repeats O&N's gloss, which Allard's own page does not support as stated.

#### [E] E-32 | §3 | line 89 (end) and line 91: reports no per-ballot frequency; Burlington example moves 750 rankings; "Burlington 2009 final count 4,314 to 4,067, a margin of 247 votes"
MARK: confirmed
SOURCE: https://www.rangevoting.org/OrnsteinNormanMonotonicityIRV.pdf (local: ornstein.raw.txt) ; Sec. 2, pp. 2-3
QUOTE[ornstein.raw.txt]: "After the Democrat’s votes were redistributed to the other two candidates, the Progressive won the election 4,314 to 4,067."
QUOTE[ornstein.raw.txt]: "It was a very competitive election, as the winner’s margin of victory was 247 votes (2.8 % of the electorate)."
QUOTE[ornstein.raw.txt]: "If we shift the Progressive candidate up in 750 rankings, we can construct the following election profile"
QUOTE[ornstein.raw.txt]: "the Progressive loses to the Democrat 3,927 to 4,067."
NOTE: [stated]. [measured] check: the nine ballot-type counts in Table 1 (1513, 495, 1289, 1332, 767, 455, 2043, 371, 568) sum to 8,833, and 247/8,833 = 2.80%, which is the paper's "2.8 % of the electorate"; the first-place sums are R 1513+495+1289 = 3,297, D 1332+767+455 = 2,554, P 2043+371+568 = 2,982, as the paper states; the printed final-round totals 4,314 + 4,067 sum to 8,381 (I did not reconcile the 452 ballots between 8,833 and 8,381; the paper does not discuss it). The paper calls the Democrat the Condorcet winner, eliminated first. The paper reports rates of the phenomenon only in simulation; the 750 is a hypothetical shift (like G-S&M's examples, E-47).

---

#### [E] E-33 | §3 | line 90: citation and version
MARK: confirmed
SOURCE: https://arxiv.org/pdf/2301.12075 (local: gs_mccune.raw.txt) ; p. 1
QUOTE[gs_mccune.raw.txt]: "arXiv:2301.12075v2 [econ.GN] 6 Mar 2023"
QUOTE[gs_mccune.raw.txt]: "AN EXAMINATION OF RANKED CHOICE VOTING IN THE UNITED STATES, 2004-2022"
NOTE: The first pass said "(the version read is the arXiv text; I did not check which version)": it is v2 of 6 March 2023. Authors Adam Graham-Squire (High Point University) and David McCune (William Jewell College).

#### [E] E-34 | §3 | line 90: "Database of 182 elections for political office, all without an initial majority winner"
MARK: confirmed
SOURCE: https://arxiv.org/pdf/2301.12075 (local: gs_mccune.raw.txt) ; Abstract and Sec. 1, p. 1
QUOTE[gs_mccune.raw.txt]: "We use a database of 182 American ranked-choice elections for political office from the years 2004-2022 to investigate empirically how frequently RCV’s deficiencies manifest in practice."
QUOTE[gs_mccune.raw.txt]: "The flaws of RCV listed above can manifest only in elections without a majority candidate (i.e., elections in which RCV goes to at least a second round), and thus our database consists only of such elections."
NOTE: [stated]. Table 3 (list of jurisdictions with counts, layout file gs_mccune.txt lines 255-289) adds up to 182: 13+2+6+1+2+2+1+1+1+3+11+26+1+41+21+4+2+32+5+2+1+2+1+1 = 182 [measured, by me, from the 24 printed rows]. The authors add: "there are easily at least 100 such elections across all jurisdictions" that they did not count, i.e. elections with a first-round majority are outside the denominator, and "If we were to include these elections, the failure rates become significantly smaller." (Sec. 7).
QUOTE[gs_mccune.raw.txt]: "If we were to include these elections, the failure rates become significantly smaller."

#### [E] E-35 | §3 | line 90: abstract quotation "rarely observed"
MARK: confirmed
SOURCE: https://arxiv.org/pdf/2301.12075 (local: gs_mccune.raw.txt) ; Abstract, p. 1
QUOTE[gs_mccune.raw.txt]: "Our general finding is that RCV’s weaknesses are rarely observed in real-world elections, with the exception that ballot exhaustion frequently causes majoritarian failures."
NOTE: [stated]. The first pass's "RCV's weaknesses are rarely observed in real-world elections" is a verbatim part of this sentence; the omitted "with the exception that ballot exhaustion frequently causes majoritarian failures" belongs with it.

#### [E] E-36 | §3 | line 90 and §10.1 and §10.3 item 2: rates "upward monotonicity failure 3 of 182 (1.6%), downward 2 of 182 (1.1%), no-show 1 (0.5%), Condorcet failure 2 of 181 (1.1%), spoiler effect 3 (1.6%), compromise voting 7 (3.8%)"
MARK: confirmed
SOURCE: https://arxiv.org/pdf/2301.12075 (local: gs_mccune.txt, layout) ; Table 7, p. 12; Sec. 6, pp. 9-11
QUOTE[gs_mccune.txt]: "Flaw Condorcet Spoiler Upward Downward Truncation Compromise Majoritarian Rate 1.1% 1.6% 1.6% 1.1% 0.5% 3.8% 52.5%"
QUOTE[gs_mccune.txt]: "Table 7. The failure rate in our database of 182 elections for the six non-majoritarian flaws of RCV. For the Condorcet failure rate we use a denominator of 181 because one of the elections does not contain a Condorcet winner."
NOTE: The paper prints **percentages, not counts**. The counts (3, 2, 1, 2 of 181, 3, 7) are not printed anywhere; the first pass got them from percentages times 182. I checked them by counting the elections the paper lists in Sec. 6 ([measured]): Condorcet failure: Burlington 2009 and Alaska Aug 2022 = 2 (Minneapolis 2021 Ward 2 has no Condorcet winner, hence the denominator 181); spoiler: Burlington, Minneapolis 2021 Ward 2, Alaska = 3; upward: the same three = 3; downward: San Francisco 2020 D7 and Minneapolis 2021 Ward 2 = 2; truncation (no-show): Alaska = 1; compromise: Burlington, Pierce County, Oakland 2010, Berkeley 2016, Minneapolis 2017 Ward 3, Minneapolis 2021 Ward 2, Alaska = 7. Rates by my arithmetic: 3/182 = 1.65%, 2/182 = 1.10%, 1/182 = 0.55%, 2/181 = 1.10%, 7/182 = 3.85%; the printed 1.6%, 1.1%, 0.5%, 1.1%, 3.8% all agree with ordinary rounding to one decimal. So the counts are right but they are inferences from the table and the narrative, not printed counts. "Truncation" in Table 7 is the paper's column for the truncation (no-show) paradox; the paper says only one election (Alaska) shows it.

#### [E] E-37 | §3 | line 90: "'majoritarian failure' (winner without a majority of ballots cast, because of exhausted ballots) 95 of 182 (printed 52.5%, text count gives 52.2%)"
MARK: confirmed
SOURCE: https://arxiv.org/pdf/2301.12075 (local: gs_mccune.raw.txt) ; Sec. 6 p. 11; Sec. 7 p. 13; Table 7 p. 12
QUOTE[gs_mccune.raw.txt]: "Of the 182 elections in our database, 95 demonstrate a majoritarian failure."
QUOTE[gs_mccune.raw.txt]: "57 of the 72 truncated elections demonstrate a majoritarian failure, while 38 of the 110 non-truncated elections demonstrate this flaw."
QUOTE[gs_mccune.raw.txt]: "We say that an election demonstrates a majoritarian failure if, when the RCV algorithm is run until there are only two candidates left, the winning candidate in this final round does not achieve a majority of the total number of votes cast."
NOTE: [stated]; and [measured]: 95/182 = 52.198% (52.2%); 57 + 38 = 95 and 72 + 110 = 182 are consistent. Table 7 prints 52.5% (which would be about 95.55 of 182, i.e. 96 elections give 52.7%). So the inconsistency the first pass flagged is **in the paper as printed** (text and sums say 95 = 52.2%; Table 7 says 52.5%). Not a transcription error by the extractor.

#### [E] E-38 | §3 | §10.3 item 3: Table 7 52.5% versus 52.2%
MARK: confirmed
SOURCE: https://arxiv.org/pdf/2301.12075 (local: gs_mccune.txt) ; Table 7, p. 12, and Sec. 6, p. 11
QUOTE[gs_mccune.txt]: "Rate 1.1% 1.6% 1.6% 1.1% 0.5% 3.8% 52.5%"
NOTE: See E-37. The inconsistency is in the paper (v2) as printed.

#### [E] E-39 | §3 | §10.3 item 3: "the text says six compromise-voting elections but lists seven"
MARK: confirmed
SOURCE: https://arxiv.org/pdf/2301.12075 (local: gs_mccune.raw.txt) ; Sec. 6, p. 9-11
QUOTE[gs_mccune.raw.txt]: "Of the six elections which demonstrate a compromise voting failure, only three (Alaska, Burlington, and the 2021 Minneapolis election) demonstrate this failure in the strong sense of the definition from (Green-Armytage, 2014)."
QUOTE[gs_mccune.raw.txt]: "Four of the elections demonstrate only a compromise voting failure; we include the preference profile for only one of these elections as the dynamics of the other three are similar."
NOTE: The "six" is in the paper as printed. The paper's own list has seven elections with a compromise failure: four "only" (Pierce County 2009/2008, Oakland 2010, Berkeley 2016, Minneapolis 2017 Ward 3) plus Burlington 2009, Minneapolis 2021 Ward 2 and Alaska 2022 (each listed with a compromise bullet). Table 7's 3.8% is 7/182 (6/182 would be 3.3%) [measured]. So the "six" is the odd one out. Three further inconsistencies I found while reading and that the first pass did not list: (a) the Conclusion says monotonicity and no-show paradoxes "seem to occur on the order of 0.5-1.1%" while Table 7 prints 1.6% for upward monotonicity (below, E-40); (b) the Pierce County election is called "The 2009 County Executive Election" in Sec. 6 and Sec. 7 but "The 2008 County Executive election" in the Table 5 caption and "2008 Pierce County, WA, County Executive" in Table 9; (c) none of these affects the counts.
QUOTE[gs_mccune.raw.txt]: "2009 County Executive Election in Pierce County, WA (Table 5)."
QUOTE[gs_mccune.raw.txt]: "Table 5. The 2008 County Executive election in Pierce County, WA, after eliminating all but the final three candidates."

#### [E] E-40 | §3 | (new) Conclusion rate range for monotonicity/no-show paradoxes
MARK: corrected
SOURCE: https://arxiv.org/pdf/2301.12075 (local: gs_mccune.raw.txt) ; Sec. 8, p. 15
QUOTE[gs_mccune.raw.txt]: "Paradoxes which feature prominently in the theoretical literature such as monotonicity and no-show paradoxes seem to occur on the order of 0.5-1.1% for realworld elections without a majority candidate, and these failure rates would decrease considerably if we also included ranked-choice elections which do not advance to a second round."
CORRECTION: (not a first-pass claim; added because §10.1 and §10.3 quote "1.6% of 182") the paper's own Conclusion gives "0.5-1.1%" for these paradoxes, but its Table 7 gives upward monotonicity 1.6%, downward 1.1% and no-show 0.5%. So 1.6% (3 of 182) is the Table 7 / Sec. 6 figure for upward failure and the Conclusion's range omits it. Use Table 7 and the Sec. 6 list.
NOTE: A second statement worth keeping: the same sentence says the rates "would decrease considerably if we also included" elections that do not advance to a second round.

#### [E] E-41 | §3 | line 90: Burlington 2009: "450 voters who voted only for Wright and 300 voters who ranked Wright first and Kiss second"
MARK: confirmed
SOURCE: https://arxiv.org/pdf/2301.12075 (local: gs_mccune.raw.txt) ; Sec. 6, p. 9
QUOTE[gs_mccune.raw.txt]: "Upward monotonicity paradox: If 450 voters who voted only for Wright and 300 voters who ranked Wright first and Kiss second shift Kiss up to the first ranking on their ballots, then Kiss would no longer win the election."
NOTE: [stated]. 450 + 300 = 750, the same 750 rankings O&N shift (E-32). The paper's Table 4 for Burlington is "taken from (Ornstein & Norman, 2014)" (caption), i.e. same data. Burlington also shows (paper): Condorcet failure (Condorcet winner Montroll, RCV winner Kiss), spoiler effect (Wright) and a compromise failure.

#### [E] E-42 | §3 | line 90: San Francisco: "Melgar 18,561 to Engardio 16,370; shift 800 ballots" (downward)
MARK: confirmed
SOURCE: https://arxiv.org/pdf/2301.12075 (local: gs_mccune.raw.txt) ; Sec. 2, p. 4
QUOTE[gs_mccune.raw.txt]: "Nguyen is eliminated, and after their votes are transferred Melgar wins with 18561 votes to Engardio’s 16370."
QUOTE[gs_mccune.raw.txt]: "If Engardio were shifted down one ranking on 800 ballots of the form Engardio > Nguyen > Melgar"
NOTE: [stated]. The 2020 District 7 Board of Supervisors election, shown after four of seven candidates were eliminated; at that point Engardio has 14119 first-place votes, Melgar 11652, Nguyen 10855 (p. 4). The first pass's "downward" label is right. The same election illustrates majoritarian failure: "Melgar earns 18561/39322 = 47.2% of the total vote in the final round" (p. 5).

#### [E] E-43 | §3 | line 90: named upward cases: Burlington 2009; Minneapolis Ward 2 2021; Alaska US House special 2022
MARK: confirmed
SOURCE: https://arxiv.org/pdf/2301.12075 (local: gs_mccune.raw.txt) ; Sec. 6, pp. 9-11
QUOTE[gs_mccune.raw.txt]: "Upward monotonicity paradox: If 456 of the voters who ranked Arab first and Worlobah second shift Worlobah up one ranking, Worlobah would lose the election."
QUOTE[gs_mccune.raw.txt]: "Downward monotonicity paradox: If 80 of the voters who ranked Arab first and Gordon second shift Arab down one ranking, Arab would win the election."
NOTE: [stated]. Alaska's upward paradox is in the Sec. 2 definition and example (E-44) and the Sec. 6 list ("August 2022 Alaska Special Election for US House ... Upward monotonicity paradox", p. 11). Minneapolis Ward 2 2021 shows both an upward and a downward paradox (so downward: San Francisco and Minneapolis, as first pass says).

#### [E] E-44 | §3 | line 90 and §10.3 item 3: "the Alaska upward-monotonicity example is a hypothetical shift of 6,000 ballots" (listed among inconsistencies)
MARK: corrected
SOURCE: https://arxiv.org/pdf/2301.12075 (local: gs_mccune.raw.txt) ; Sec. 2, pp. 3-4
QUOTE[gs_mccune.raw.txt]: "An RCV election demonstrates an upward monotonicity paradox if there exists a set of ballots such that shifting the RCV winner up the rankings on those ballots but keeping the relative rankings of the other candidates the same, thereby creating a hypothetical second preference profile in which the winner has more voter support, creates an election in which the original RCV winner does not win."
QUOTE[gs_mccune.raw.txt]: "In the Alaska House election, if 6000 ballots on which Palin is ranked first and no other candidate is ranked on the ballot were changed to ballots of the form Peltola > Palin then Peltola would lose the resulting election."
CORRECTION: "an inconsistency: the Alaska example is a hypothetical shift" -> not an inconsistency. Every monotonicity paradox in this paper (and in Ornstein & Norman) is *defined* by a hypothetical shift of ballots in the observed profile; the Burlington (750) and Minneapolis (456) examples are hypothetical shifts too. The Alaska election is counted as one of the 3 upward failures. The only point the first pass could note is that the 6,000 shift is given as the worked example in Sec. 2, not in Sec. 6.
NOTE: [stated]. The same Sec. 2 example also demonstrates a no-show paradox (5,400 voters who cast Palin > Begich > Peltola) and a compromise failure.

#### [E] E-45 | §3 | line 91 / line 92: "McCune & Graham-Squire ... 1,079 Scottish elections" (the 1,079 figure only)
MARK: confirmed
SOURCE: https://arxiv.org/pdf/2301.12075 (local: gs_mccune.raw.txt) ; Sec. 4, p. 7
QUOTE[gs_mccune.raw.txt]: "(McCune & Graham-Squire, 2022) analyze 1079 ranked-choice multiwinner elections from Scotland and find low (but non-zero) rates of upward monotonicity, downward monotonicity, and no-show paradoxes."
NOTE: This corroborates the number 1,079 (and "multiwinner") from a second source. The "62" and the "30 single-winner, 1,049 multiwinner" and the "1-4% for each type" belong to the Scottish paper (task B); I did not read them. In the paper's own cross-reference, "the code found 21 elections demonstrating upward monotonicity paradoxes in Scottish local government elections which had not been previously documented" (Sec. 5, p. 8-9).

---

#### [B] B-30 | §3 line 92 / §5 line 144 | McCune & Graham-Squire, "Monotonicity anomalies in Scottish local government elections", Social Choice and Welfare 63 (2024) 69-101
MARK: confirmed for title, journal, volume and pages (metadata record); paper body unread
SOURCE: https://api.crossref.org/works/10.1007/s00355-024-01522-5 (local: dl/crossref_scot.abstract.txt, built from the JSON) ; DOI 10.1007/s00355-024-01522-5
QUOTE[dl/crossref_scot.abstract.txt]: "TITLE: Monotonicity anomalies in Scottish local government elections | JOURNAL: Social Choice and Welfare | VOLUME: 63 | ISSUE: 1 | PAGES: 69-101"
NOTE: [stated] Crossref: published online 22 April 2024; print issue August 2024; authors McCune, Graham-Squire; licence CC BY 4.0 (open access). The first pass's URL https://link.springer.com/article/10.1007/s00355-024-01522-5 is the DOI's landing page and is bot-challenged to curl.

#### [B] B-31 | §3 line 92 | "In 62 of the 1079 elections we found some kind of monotonicity anomaly" (30 single-winner, 1,049 multiwinner STV); "the authors state their results are a lower bound" (lines 92, 144)
MARK: confirmed for "1079" and "62" (abstract); unread for "30 single-winner, 1,049 multiwinner" and for "lower bound"
SOURCE: the Crossref abstract (above) ; paper body unread
QUOTE[dl/crossref_scot.abstract.txt]: "We analyze 1079 local government STV elections in Scotland to estimate the frequency of such monotonicity anomalies in real-world elections"
QUOTE[dl/crossref_scot.abstract.txt]: "In 62 of the 1079 elections we found some kind of monotonicity anomaly."
NOTE: [measured] 30 + 1,049 = 1,079 (consistent). 62 / 1079 = 5.75%. The abstract does not contain the words "lower bound", "30 single-winner" or "1,049": those first-pass facts are unread. The abstract's wording on size is "We generally find that anomaly rates are similar to prior empirical research and much lower than what most theoretical research has found."

#### [B] B-33 | §3 line 92 / §5 line 144 | Quote "Most STV anomalies we find are the first of their kind to be documented in real-world multiwinner elections." (lines 92, 144)
MARK: confirmed (abstract)
SOURCE: Crossref abstract (above)
QUOTE[dl/crossref_scot.abstract.txt]: "Most STV anomalies we find are the first of their kind to be documented in real-world multiwinner elections."
NOTE: [stated]

### [E] RECONCILIATION: Baltz's simulated magnitudes at N = 1,000 versus the 1/N scale (0.006 to 0.016) in the first pass

All steps say whether they come from the paper ([stated]), from my computation ([measured], scripts in `SP/r4/work-E/`), or from my reading ([inferred]).

**1. What Baltz's plotted number is the probability of** [stated, from arXiv Sec. 4 and the supplement §9, Figure 1 captions]. For each of 100 runs he draws a population of 1,000 ranked ballots at random "in a way that ensures that support for the candidates follows the specified distribution" (supplement) and with "an equal probability of appearing in any position on any ballot" (arXiv caption), for 3, 4 and 5 candidates and "when voters can rank every candidate" (full-length ballots, L = kappa). He then computes, for every possible ballot beta, the probability p(beta) = p_direct(beta) + p_indirect(beta) that one additional ballot of that form changes the winner (relative to abstaining; "all probabilities and utilities should be understood as being implicitly compared to abstention"), using Skellam differences of Poisson counts, with the Poisson means being the expected numbers of voters of each ballot type; the same quantity for plurality (SMDP) comes from the Mebane et al. (2019) derivation, which I could not read. The y-value is **the sum of p(beta) over every possible ballot** ("the sum of the pivotal probability of every possible ballot"), one dot per run. So it is not the probability that *a particular voter's one ballot* is pivotal: it is the total over all the ballots she might cast. The expected totals are exactly known (only Poisson noise around them; there is no forecast uncertainty about vote shares), and he calls them "out-of-equilibrium pivotal probabilities" ("the initial pivotal probabilities of these election structures"). [inferred] that the Poisson means are the realised counts of each ballot type in that run's 1,000 ballots; the paper says only that the counts "follow a Poisson distribution with known parameter".

**2. Two panels, two scales** [stated and read off the images]. Panel (b), "uniform support", is on a **linear** axis from 0 to 0.12: individual runs lie between about 0.003 and 0.12, and the published version's mean lines (read by eye, approximate) are SMDP 0.052 / 0.052 / 0.043 and IRV 0.083 / 0.061 / 0.033 for 3 / 4 / 5 candidates. Panel (a), "power law support", is on a **log10** axis ("Pivotal probability (Log10)") from 0 to -14: runs lie between about 10^-2.4 and 10^-12.5; the plotted mean lines (the 3-candidate SMDP line verified in the pixels at -7.56; the others read by eye, uncertainty about 0.2) are about 10^-7.6, 10^-8.3, 10^-8.9 (SMDP) and 10^-5.9, 10^-5.9, 10^-5.6 (IRV). The text's "averaging about 10^-6 compared to about 10^-7" is therefore about panel (a) only, and the lines are means of log10 values, not arithmetic means (the single highest 3-candidate IRV point, 10^-2.9, would alone put an arithmetic mean of 100 points near 10^-4.9). The paper warns that the two panels "should not be directly compared to one another without taking the y-axis scales into account".

**3. Are the uniform-panel values comparable with the first pass's 1/N-scale values?** Yes, in order of magnitude, with qualifications. The first pass's N = 1,000 table gives per-ballot Q of 0.0126 (two candidates, known 50-50), 0.0155 (three equal candidates, known shares) and 0.006 to 0.007 (shares uncertain), for one candidate's ballot. Baltz's uniform values are sums over all the ballots a voter might cast: for 3 candidates with full rankings there are 3! = 6 ballots, and the plotted means 0.052 (SMDP) and 0.083 (IRV) divide to about 0.009 and 0.014 per ballot, in the same decade as 0.0126 to 0.0155 [measured arithmetic on read-off values]. My own re-computation ([measured], `smdp.py`, `exact3.py`): applying the paper's printed p_direct formula, with the Skellam convention of the supplement's worked example, to plurality with 3 candidates and Poisson means 333.3 gives 0.02245 summed over the three first-choice candidates (0.00748 each); times the 2 full-ranking ballots per first choice that is 0.0449; with 100 random multinomial draws of 1,000 ballots the mean is 0.0395 (range 0.0103 to 0.0567) against the plotted SMDP mean of about 0.052 and plotted range of about 0.01 to 0.07. For 4 and 5 candidates my plurality use of the IRV-form formula does **not** reproduce the plot (0.094 and 0.26 against about 0.052 and 0.043), which is expected: his SMDP numbers come from Mebane et al., not from the formula I applied. So the uniform-panel magnitude at N = 1,000 (about 0.01 to 0.1 summed over ballots) is consistent with the 1/N scale; it is not at odds with it.

**4. How big a difference the paper's independence assumption makes** [measured, `exact3.py`, `exactk.py`]. For 3 candidates with equal Poisson means of 333.3, the exact probability from the Poisson game that a vote for candidate i changes who wins, counting a tie as a fair lottery (the same Q as the first pass), is 0.015494 (the first pass's multinomial figure was 0.01549). The paper's printed formula (Assumption 1: "any two pairwise comparisons of vote totals are independent"), applied to plurality, gives 0.00748 per candidate in the same setting, a factor 2.07 lower. The reason is visible in the formula: with i and j tied, "k below i" and "k below j" are treated as independent events (each about 0.49, product 0.24) when they are nearly the same event (about 0.49). For 4 and 5 equal candidates (Poisson means 250 and 200) the exact Q per candidate is 0.01636 and 0.01658, while the printed formula applied to plurality gives 0.00306 and 0.00078: ratios 5.4 and 21. So the independence products make the printed formula fall further below the exact value as the number of candidates grows; this is my plurality analogue, not Baltz's IRV code or his SMDP formula (Mebane et al.), but it is the same kind of product the paper's footnote 6 blames for the pattern across candidate numbers ("the varying quality of Assumption 2 as more candidates are introduced"). Baltz's footnote 2 says that without the independence assumptions the terms change "up to multiplication of each term by some real number".

**5. The power-law panel cannot be reconciled with its one-sentence description** [measured]. The paper's description is "half of the population holds one preference order, and the other half has a uniformly random preference order". With 1,000 voters, 3 candidates, that gives expected first-place counts of 667 / 167 / 167 (4 candidates: 625 / 125 / 125 / 125; 5: 600 / 100 / 100 / 100 / 100). A tie for first between the front-runner and anyone is then astronomically unlikely: applying the printed formula gives a total of about 1.7 x 10^-74 (3 candidates), 4 x 10^-85 (4) and 1 x 10^-93 (5) (`smdp.py`), many orders of magnitude below the plotted 10^-4 to 10^-12. So whatever was simulated in panel (a) had first-place shares much closer together than that sentence implies (for a tie to have a probability near 10^-7 to 10^-9 the shares must be within a few percentage points of each other), or the quantity plotted is not what I computed. The paper gives no exponent for the "power law", no list of which preference orders carry the weight, and no code. Hence the 10^-6 / 10^-7 averages describe "an electorate with a clear front-runner under Poisson noise" in a sense I cannot pin down, and they are **not** comparable with the 1/N-scale values; they are comparisons between IRV and SMDP on the same draws, which is the use the author gives them.

**6. What the paper does not let me settle** [stated absences, searched in both files]: (a) the power-law parameters; (b) whether the Poisson means are the realised ballot counts of each run (the most natural reading, not stated); (c) the SMDP formula and whether SMDP's "sum over every possible ballot" runs over kappa ballots or kappa! full rankings (it matters by a factor of (kappa-1)!); (d) whether a Figure 1 "dot" for IRV includes ties among more than two candidates (set aside by assumption) and how the ½ weights were implemented in code; (e) any value for a single voter's single ballot in a realistic election (the paper reports none; the supplement's worked example is a 25-voter electorate); (f) the effect of Assumption 2 (the author says the number-of-candidates pattern "may be attributable to the varying quality of Assumption 2"); (g) the journal text and its main-text example ("such large numbers" that the exact probabilities "become almost inexpressibly small"); (h) how the average "about 10^-6 / 10^-7" was computed, though the plotted lines suggest a mean of log10 values. In short: the uniform-panel scale agrees with the 1/N scale to within a factor of about 2 to 3 per ballot; the power-law-panel scale does not and cannot be explained from the text; and the paper's own warning is that all of it is for stylised electorates.

---


## 4. Proportional representation (PR) and mixed systems

*First-pass lines 98-137 of `research/electoral-systems.md`. Each block: the first-pass claim with its line number, the mark, the source and location, exact quotes, the correction if any, notes.*

#### [C] C-01 | §4 What "decisive" means | L&T quote "one abstaining voter could change the allocation of seats between parties by voting" (Sec. 4.2) (first pass line 101)
MARK: confirmed
SOURCE: https://www.doria.fi/bitstream/10024/148789/1/wp50.pdf (local: lyyt.txt) ; Sec. 4.2 "Step 2: Measuring pivotal probabilities", printed p. 17 (PDF p. 20)
QUOTE[lyyt.txt]: "We calculate the pivotal events both between parties, i.e., situations where one abstaining voter could change the allocation of seats between parties by voting, and within parties,"
NOTE: [stated] The first pass's quote is a correct substring. The paper's sentence defines what it counts as a "pivotal event"; it is the authors' own definition, not a general statement about PR.

#### [C] C-02 | §4 What "decisive" means | Luechinger-Schelker-Schmid "closeness" is "the minimal necessary movement along both margins to gain or lose a seat", holding "the votes of all other parties and candidates" fixed (Sec. 1, p. 102) (line 101)
MARK: confirmed
SOURCE: https://doi.org/10.1017/pan.2023.22, the Cambridge Core open-access PDF as fetched by the orchestrating thread from www.cambridge.org (exact URL not in urls.txt; file SP/r4/src/luechinger_cup.out) (Cambridge Core open-access PDF of Political Analysis 32:101-114, doi 10.1017/pan.2023.22; fetched by the orchestrating thread by curl) (local: luechinger.raw.txt; raw PDF SP/r4/src/luechinger_cup.out) ; Sec. 1 Introduction, printed p. 102
QUOTE[luechinger.raw.txt]: "We explicitly calculate these margins and then define closeness as the minimal necessary movement along both margins to gain or lose a seat."
QUOTE[luechinger.raw.txt]: "In the thought experiment underlying our approach, we assume that the votes of all other parties and candidates remain unchanged."
QUOTE[luechinger.raw.txt]: "We favor our thought experiment because of its tractability and transparency."
NOTE: [stated] Page is 102 (checked: the running page number 102 follows this text in the extraction). The paper says other thought experiments are possible (redistributing votes between parties/candidates) and says it favours this one "because of its tractability and transparency"; (so the measure is one thought experiment among possible ones, see the quote on the line above).

#### [C] C-03 | §4 What "decisive" means | L&T quote "one voter could change which of the party's candidates gets the last seat of the party" (Sec. 4.2) (line 103)
MARK: confirmed
SOURCE: https://www.doria.fi/bitstream/10024/148789/1/wp50.pdf (local: lyyt.txt) ; Sec. 4.2, printed p. 17 (PDF p. 20)
QUOTE[lyyt.txt]: "i.e., situations where one voter could change which of the party’s candidates gets the last seat of the party."
NOTE: [stated] Exact characters have a curly apostrophe (party’s); the first pass printed a straight one. Harmless typography.

#### [C] C-05 | §4 What "decisive" means | in Luechinger et al. "who gets the party's seat" is the "candidate margin" (line 103)
MARK: confirmed
SOURCE: https://doi.org/10.1017/pan.2023.22, the Cambridge Core open-access PDF as fetched by the orchestrating thread from www.cambridge.org (exact URL not in urls.txt; file SP/r4/src/luechinger_cup.out) (Political Analysis, doi 10.1017/pan.2023.22, open-access PDF) (local: luechinger.raw.txt) ; Sec. 1 p. 102 and Sec. 2.2 pp. 106-107
QUOTE[luechinger.raw.txt]: "In the following, we refer to these margins as the party and the candidate margin."
QUOTE[luechinger.raw.txt]: "We now construct the candidate margin that measures how far an individual candidate is from reaching the same position as another copartisan candidate. This variable is only relevant for open-list PR systems."
NOTE: [stated] "this margin" in the paper is a vote difference to a copartisan candidate (a margin in votes), not a probability.

#### [C] C-06 | §4 What "decisive" means (mixed systems) | Germany: a constituency winner whose party's second votes do not "cover" the seat is not seated: "those candidates with the lowest percentages of first votes are not assigned a seat" (BVerfG press release, 30 July 2024) (line 104)
MARK: confirmed
SOURCE: https://bundesverfassungsgericht.de/SharedDocs/Pressemitteilungen/EN/2024/bvg24-064.html (local: txt/bverfg24.html is the raw page; I made the plain text work-C/bverfg24.txt from it with work-C/h2t.py) ; Press Release No. 64/2024, "Facts of the case"
QUOTE[work-C/bverfg24.txt]: "If the number of successful candidates exceeds the number of seats a party’s Land list receives based on the second vote, then those candidates with the lowest percentages of first votes are not assigned a seat (§ 6(1) and (4) first and second sentence Federal Elections Act)."
QUOTE[work-C/bverfg24.txt]: "Each voter has two votes: the first vote is for a candidate in the voter’s constituency and the second vote is for a list of candidates nominated for the respective Land by a political party (hereinafter ‘Land list’)."
QUOTE[work-C/bverfg24.txt]: "The 630 seats in the Bundestag (§ 1(1) first sentence Federal Elections Act) are first distributed among the parties: Each party receives seats based on its respective share of the nationwide second vote (§ 4(2) Federal Elections Act)."
QUOTE[work-C/dl/bwahlg6.txt]: "Ein Wahlkreisbewerber einer Partei (§ 20 Absatz 2) ist dann als Abgeordneter gewählt, wenn er die meisten Erststimmen auf sich vereinigt und im Verfahren der Zweitstimmendeckung (Satz 4) einen Sitz erhält."
NOTE: [stated] Same facts in the statute itself: BWahlG § 6(1) (https://www.gesetze-im-internet.de/bwahlg/__6.html, read by curl; footnote there: "§ 6 Abs. 1: Mit dem GG vereinbar gem. BVerfGE v. 30.7.2024 I Nr. 281 - 2 BvF 1/23 u.a."). The statute says "gereiht nach fallendem Erststimmenanteil" (ranked by falling first-vote share) in each Land.

#### [C] C-07 | §4 What "decisive" means | "A party crosses a threshold. One vote decides whether a party gets any seats at all, which moves many seats at once" [inferred; German and NZ rules stated below] (line 102)
MARK: confirmed (the rule); the sentence itself is [inferred] and not checkable at a source
SOURCE: https://bundesverfassungsgericht.de/SharedDocs/Pressemitteilungen/EN/2024/bvg24-064.html (local: work-C/bverfg24.txt) ; and https://www.gesetze-im-internet.de/bwahlg/__4.html (local: work-C/dl/bwahlg4.txt) ; § 4(2)
QUOTE[work-C/bverfg24.txt]: "Pursuant to § 4(2) second sentence no. 2 of the Federal Elections Act, political parties who receive less than 5% of the second vote do not receive any seats (5% electoral threshold). Their candidates are not elected to the Bundestag."
QUOTE[work-C/dl/bwahlg4.txt]: "Parteien, die weniger als 5 Prozent der im Wahlgebiet abgegebenen gültigen Zweitstimmen erhalten haben."
NOTE: [stated] The statute says "weniger als 5 Prozent der im Wahlgebiet abgegebenen gültigen Zweitstimmen" (less than 5 percent of the valid second votes cast in the electoral area), so the denominator is valid second votes, and the party is "not considered" if below. The statute also (§ 4(2) sentence 2 no. 1) leaves out of the count "die Zweitstimmen derjenigen Wähler, die ihre Erststimme für einen Bewerber abgegeben haben, der gemäß § 6 Absatz 2 erfolgreich ist" (second votes of voters whose first vote went to a successful independent candidate), and § 4(4) adds seats when a party with more than half of the counted second votes would otherwise not have more than half of the seats. Both are rules a model of "decisive vote" would have to know. The text read is the current consolidated statute as shown by gesetze-im-internet.de on the day of reading (7 Nov 2026 per the session date); it may differ from the law in force on 23 Feb 2025.

#### [C] C-08 | §4 What "decisive" means | "No source I read models [coalition formation]; it is the 'chamber control' structure of section 8 plus coalition bargaining." (line 105)
MARK: unread
SOURCE: none; this is the first pass's own statement about the state of the literature and a pointer to section 8, not a source fact.
NOTE: Nothing to check at a source. (Task C covers only rules, formulas and numbers.)

#### [C] C-09 | §4 Rules | New Zealand (MMP): "The 120 highest numbers (which are called quotients) determine both the number of seats for each party"; party vote "divided by successive odd numbers starting with 1" (Sainte-Lague); "at least 5% of the total number of party votes" or an electorate seat; overhang: "the size of the Parliament is increased by that number of seats"; 121 seats in 2014; source electionresults.govt.nz sainte_lague.html (line 108)
MARK: unread
SOURCE: https://www.electionresults.govt.nz/sainte_lague.html (local: nz_sl.txt / nz_sl.out) ; refused
NOTE: Reason: Cloudflare block. The local nz_sl.out is the Cloudflare page ("Attention Required! | Cloudflare", "Sorry, you have been blocked", "You are unable to access electionresults.govt.nz"). I requested the page once again with curl: HTTP 403, 5,959 bytes, same block page. I then requested one different page of the same publisher (the 2020 archive copy, archive.electionresults.govt.nz/electionresults_2020/statistics/sainte-lague-formula.html): HTTP 403, the same block page. I stopped there (rule 5) and did not try other means. `elections.nz` (one request, https://elections.nz/democracy-in-nz/what-is-new-zealands-system-of-government/): HTTP 200 but a 212-byte Incapsula stub ("/_Incapsula_Resource"), a bot check; not circumvented. `www.legislation.govt.nz` (Electoral Act 1993, whole-act HTML, two requests 6 s apart): HTTP 202 with an empty body both times; not read. So the NZ quotes in line 108 stay unread, and since the first pass obtained them only by WebFetch they remain [stated via WebFetch]. See C-10 for what a different legitimate source (the IDEA Handbook, 2005) says about NZ; it does not reproduce the quoted sentences.

#### [C] C-10 | §4 Rules | NZ threshold and overhang as stated by another source (not in the first pass; corroboration for line 108 from a different legitimate source)
MARK: confirmed (for the 5%-or-one-seat rule and for "overhang possible in NZ" as of the 2005 IDEA text; the specific first-pass NZ quotes remain unread, see C-09)
SOURCE: https://www.idea.int/sites/default/files/publications/electoral-system-design-the-new-international-idea-handbook.pdf (local: work-C/idea_handbook.txt) ; printed p. 102 (PDF p. 116) "There are two thresholds for MMP in New Zealand"; printed p. 83 (PDF p. 97), paragraph 120; MMP section
QUOTE[work-C/idea_handbook.txt]: "To win a share of the seats in Parliament based on the party votes, a party must either win at least 5 per cent of all the party votes cast in a general election or win at least one single-member district seat."
QUOTE[work-C/idea_handbook.txt]: "This has occurred in most elections in Germany and is also possible in New Zealand."
QUOTE[work-C/idea_handbook.txt]: "However, in both Germany and New Zealand there exist ‘back-door’ routes for a party to be entitled to seats from the lists; in the case of New Zealand a party must win at least one constituency seat, and in the case of Germany three seats, to bypass the threshold requirements."
NOTE: [stated] This is the IDEA Handbook of 2005 (the book's own text); NZ and German rules may have changed since. Note that the German "three constituencies" back-door in 2005 was the Grundmandatsklausel, which the 2023 law removed and the BVerfG then made a condition of continued application (C-13). The IDEA text says "one single-member district seat" for NZ (this is 2005 text; the first pass says "an electorate seat").

#### [C] C-11 | §4 Rules | Germany: 2025 final result, 5% threshold; BSW 4.981%; the new Bundestag has 630 members; "7,425 higher than in the provisional result" (line 109)
MARK: confirmed
SOURCE: https://bundeswahlleiterin.de/en/info/presse/mitteilungen/bundestagswahl-2025/29_25_endgueltiges-ergebnis.html (local: work-C/bwl.txt, my plain-text conversion of txt/bwl.html) ; Press release no. 29/25 of 14 March 2025
QUOTE[work-C/bwl.txt]: "All percentages have been rounded to one decimal place for reasons of clarity. The number of valid second votes in the final result is 7,425 higher than in the provisional result."
QUOTE[work-C/bwl.txt]: "BSW Bündnis Sahra Wagenknecht - Vernunft und Gerechtigkeit 4.981 %"
QUOTE[work-C/bwl.txt]: "An exception applies if a party fell just short of the 5 percent threshold to enter the Bundestag. Then the percentage is rounded to three decimal places."
QUOTE[work-C/bwl.txt]: "Pursuant to Section 1 (1) of the Federal Elections Act, the newly elected Bundestag will have a total of 630 members (2021: 735)."
QUOTE[work-C/bwl.txt]: "Press release no. 29/25 of 14. März 2025"
NOTE: [stated] The press release says "5 percent threshold" only in the rounding sentence above; the rule itself is in BWahlG § 4(2) (C-07). It prints neither the BSW vote count nor the total of valid second votes; those are on the results page (C-36). The release adds: "Based on the final result, there are no changes in the distribution of seats compared with the provisional result." and that SSW takes part as a minority party "to which the restrictive clause does not apply".

#### [C] C-13 | §4 Rules | BVerfG 30 July 2024, 2 BvF 1/23 and others: second-vote coverage compatible with the Basic Law (unanimous); 5% threshold "in its current form unconstitutional" (7:1) but left in force until a new law; parties under 5% still take part if "their candidates win a majority of first votes in at least three constituencies" (line 109)
MARK: corrected
SOURCE: https://bundesverfassungsgericht.de/SharedDocs/Pressemitteilungen/EN/2024/bvg24-064.html (local: work-C/bverfg24.txt) ; Press release No. 64/2024 of 30 July 2024; also the full German judgment https://www.bundesverfassungsgericht.de/SharedDocs/Entscheidungen/DE/2024/07/fs20240730_2bvf000123.html (local: work-C/bverfg24_de.txt) and BWahlG § 4 footnote (work-C/dl/bwahlg4.txt)
QUOTE[work-C/bverfg24.txt]: "Judgment of 30 July 2024 - 2 BvF 1/23, 2 BvF 3/23, 2 BvE 2/23, 2 BvE 9/23, 2 BvE 10/23, 2 BvR 1523/23, 2 BvR 1547/23"
QUOTE[work-C/bverfg24.txt]: "However, the 5% electoral threshold in the current version of § 4(2) second sentence no. 2 of the Federal Elections Act violates Art. 21(1) and Art. 38(1) first sentence of the Basic Law. This provision will continue to apply until a new law is enacted, subject to the condition that political parties that receive less than 5% of the second vote will still take part in the distribution of party list seats in Parliament if their candidates win a majority of first votes in at least three constituencies."
QUOTE[work-C/bverfg24.txt]: "The decision as to the second vote basis procedure is unanimous. The decision as to the electoral threshold was taken with a vote of 7:1."
QUOTE[work-C/bverfg24.txt]: "3. The electoral threshold in § 4(2) second sentence no. 2 of the Federal Elections Act in its current form is incompatible with the Basic Law."
QUOTE[work-C/bverfg24.txt]: "Setting the electoral threshold at 5% of the second vote nationwide is adequate for this purpose."
QUOTE[work-C/bverfg24.txt]: "d) Under the present legal and factual circumstances, the design of the electoral threshold in § 4(2) second sentence no. 2 of the Federal Elections Act is nevertheless not fully necessary."
QUOTE[work-C/bverfg24.txt]: "The original draft act provided that, as an alternative, winning three constituencies would be sufficient. This corresponded to the rule in the prior law."
QUOTE[work-C/dl/bwahlg4.txt]: "Bis zu einer Neuregelung gilt § 4 Abs. 2 Satz 2 Nr. 2 des Bundeswahlgesetzes mit der Maßgabe fort, dass bei der Sitzverteilung Parteien, die weniger als 5 Prozent der im Wahlgebiet abgegebenen gültigen Zweitstimmen erhalten haben, nur dann nicht berücksichtigt werden, wenn ihre Bewerber in weniger als drei Wahlkreisen die meisten Erststimmen auf sich vereinigt haben."
CORRECTION: (1) the phrase "in its current form unconstitutional" is not in the press release; the text is "in its current form is incompatible with the Basic Law" (section C.3) and, in the lead, "violates Art. 21(1) and Art. 38(1) first sentence"; the headline says "only the 5% electoral threshold is currently unconstitutional, but it will continue to apply under certain conditions". (2) "left in force the rule that parties under 5% still take part if..." -> the three-constituency clause had been REMOVED by the 2023 law ("the removal of the minimum representation provision (Grundmandatsklausel)" in the press release; "the original draft act provided that, as an alternative, winning three constituencies would be sufficient"); the Court did not leave it in force but ordered that the threshold continue to apply "subject to the condition" of the three-constituency alternative until a new law. (3) The Court did not hold 5% itself too high: it holds a 5% threshold "adequate" for the goal of functioning of the Bundestag and holds the design "not fully necessary" because a party (the CSU) that would form a joint parliamentary group with another party need not be excluded; "Under the current legal and factual circumstances, an electoral threshold of 5% is not fully necessary in order to safeguard the proper functioning of the Bundestag" (lead). The "vote 7:1" applies to the threshold decision (confirmed) and "unanimous" to the second-vote basis procedure (confirmed).
NOTE: [stated] The statute as consolidated on gesetze-im-internet.de carries the Maßgabe in a footnote to § 4 Abs. 2 Satz 2 Nr. 2 (quote above). [inferred] The 2025 election (23 Feb 2025) took place after this judgment (30 July 2024), so the Maßgabe above is the rule under which BSW's 4.981% was measured; I did not read which parties won constituencies.

#### [C] C-14 | §4 How the literature writes it | citation: Luechinger, Schelker & Schmid, "Measuring Closeness in Proportional Representation Systems", Political Analysis 32 (2024) 101-114 (online 24 July 2023), doi 10.1017/pan.2023.22, and the cambridgecore URL (line 111)
MARK: confirmed
SOURCE: https://doi.org/10.1017/pan.2023.22, the Cambridge Core open-access PDF as fetched by the orchestrating thread from www.cambridge.org (exact URL not in urls.txt; file SP/r4/src/luechinger_cup.out) (Cambridge Core PDF) (local: luechinger.raw.txt) ; title page, p. 101
QUOTE[luechinger.raw.txt]: "Measuring Closeness in Proportional Representation Systems Simon Luechinger1 , Mark Schelker 2 and Lukas Schmid1"
QUOTE[luechinger.raw.txt]: "https://doi.org/10.1017/pan.2023.22 Published online by Cambridge University Press"
QUOTE[luechinger.raw.txt]: "Political Analysis (2024) vol. 32: 101–114 DOI: 10.1017/pan.2023.22 Published 24 July 2023"
NOTE: [stated] "This is an Open Access article, distributed under the terms of the Creative Commons Attribution licence" (CC BY 4.0), so a quote from it is licensed for re-use with attribution. Whether the first pass's `core-prod.cambridgecore.org` URL gives the same text was not tested here (not my host).

#### [C] C-15 | §4 How the literature writes it | D'Hondt party margin, p. 104: party margin_{i,j} = votes_j - i x ( votes_{-j} / i~ )_{(n(J-1) - (n - i))}, with notation (line 112)
MARK: confirmed
SOURCE: https://doi.org/10.1017/pan.2023.22, the Cambridge Core open-access PDF as fetched by the orchestrating thread from www.cambridge.org (exact URL not in urls.txt; file SP/r4/src/luechinger_cup.out) (Political Analysis PDF) (local: luechinger.raw.txt; page image of PDF p. 4 = printed p. 104 rendered at 220 dpi and read) ; Sec. 2.1 "Highest Average Methods", printed p. 104
QUOTE[luechinger.raw.txt]: "Let us consider a district with J parties Pj indexed by j ∈ P ≡ {1, 2, . . . , J }. The party index of all parties other than j is −j ∈ P\{j }. A total number of n seats are allocated. The index i ∈ {1, 2, . . . , n } denotes the potential seats of party Pj . Similarly, i˜ captures the potential seats of each of the other parties P−j . We denote a party Pj ’s total number of votes by votesj ."
QUOTE[luechinger.raw.txt]: "For each party, a total of n D’Hondt ratios, votesj /i , are calculated."
QUOTE[luechinger.raw.txt]: "The (n − i + 1)th-highest D’Hondt ratio is the one with the order statistic (n(J − 1) − (n − i ))."
NOTE: [stated] The formula as printed is in FORMULAS AS PRINTED (F-A). The first pass's transcription is right in every symbol; the two things that need saying are (1) the subscript (n(J-1)-(n-i)) is an order statistic in ASCENDING order over the n(J-1) ratios of the other parties (that is what makes it the (n-i+1)-th highest), and (2) ĩ ranges over 1..n so (votes_{-j}/ĩ) is the vector of all D'Hondt ratios of all other parties. [measured] I checked the formula by hand on the paper's own example (n = 3, J = 3, shares 45/35/20): i=1: 4th smallest of {6.67, 10, 15, 20, 22.5, 45} = 20, 35 - 1*20 = 15; i=2: 5th = 22.5, 35 - 2*22.5 = -10; i=3: 6th = 45, 35 - 3*45 = -100. Same as the printed values 15, -10, -100.

#### [C] C-16 | §4 How the literature writes it | "so that the i-th seat is decided by a coin flip" (extractor's paraphrase); Sainte-Lague, modified Sainte-Lague and Imperiali "only differ by the denominator used to calculate the ratios" (footnote 5) (line 112)
MARK: confirmed
SOURCE: https://doi.org/10.1017/pan.2023.22, the Cambridge Core open-access PDF as fetched by the orchestrating thread from www.cambridge.org (exact URL not in urls.txt; file SP/r4/src/luechinger_cup.out) (Political Analysis PDF) (local: luechinger.raw.txt) ; Sec. 2.1, printed p. 104, text and footnote 5
QUOTE[luechinger.raw.txt]: "The party margini ,j captures the necessary change in the number of votes such that party Pj is at the margin of winning exactly i seats. This happens if the ith-highest D’Hondt ratio of party Pj equals the (n − i + 1)th-highest D’Hondt ratio of all other J − 1 parties and, thus, if the ith seat for party Pj is decided by a coin flip."
QUOTE[luechinger.raw.txt]: "5 Other highest average methods, such as the Sainte-Laguë, modified Sainte-Laguë or Imperiali method, only differ by the denominator used to calculate the ratios."
NOTE: [stated] The "coin flip" phrase is in the paper (not just an extractor paraphrase). "the (n-i+1)-th highest ratio of the other parties" is also in the paper as printed. The paper's margin is signed: "negative numbers indicate vote shortfalls and positive numbers vote surpluses" (p. 104).

#### [C] C-17 | §4 How the literature writes it | largest remainder (Hare-Niemeyer), pp. 105-106: quota = (votes_j + sum of votes_{-j})/n; "formulas garbled in extraction" (line 113)
MARK: confirmed
SOURCE: https://doi.org/10.1017/pan.2023.22, the Cambridge Core open-access PDF as fetched by the orchestrating thread from www.cambridge.org (exact URL not in urls.txt; file SP/r4/src/luechinger_cup.out) (Political Analysis PDF) (local: luechinger.raw.txt; page images of PDF pp. 5 and 6 = printed pp. 105-106 rendered and read; formula crops at 220 dpi) ; Sec. 2.1 "Largest Remainder Methods", printed pp. 105-106
QUOTE[luechinger.raw.txt]: "For example, the Hare–Niemeyer method, which we employ for illustration, uses the division of the total number of party votes by a district’s number of seats as a quota."
QUOTE[luechinger.raw.txt]: "In a first round of the seat allocation, parties receive a total number of seats equalling their integer."
QUOTE[luechinger.raw.txt]: "Niemeyer quota is 33.33."
QUOTE[luechinger.raw.txt]: "we calculate the party margin for the second seat of P2 as 35 − 62.5 = −27.5."
NOTE: [stated] All formulas (quota, the equality-of-remainders condition, the closed form for votes_{i,ĩ,j,-j}, F, R, the selection conditions and the final party margin) are transcribed in FORMULAS AS PRINTED (F-B) from the page images. The party margin for the largest-remainder method is a 4-step procedure, not one closed formula: "(J - 1) x (2n + 1) possible solutions" are generated and the relevant one is selected. [measured] I checked the printed closed form by algebra: setting x*n/(S+x) - (i-1) = v*n/(S+x) - (i~-1) gives x = (v*n + (i - i~) S)/(n - (i - i~)); for n=3, i=2, i~=1, v=20 (P3), S=65 it gives 62.5, the printed value. The first pass says "pp. 105-106"; correct (Largest Remainder starts on p. 105; the F, R and margin lines are on p. 106).

#### [C] C-18 | §4 How the literature writes it | candidate margin (open lists), p. 106 (line 114)
MARK: corrected
SOURCE: https://doi.org/10.1017/pan.2023.22, the Cambridge Core open-access PDF as fetched by the orchestrating thread from www.cambridge.org (exact URL not in urls.txt; file SP/r4/src/luechinger_cup.out) (Political Analysis PDF) (local: luechinger.raw.txt; page image of PDF p. 7 = printed p. 107 read) ; Sec. 2.2, printed pp. 106-107
QUOTE[luechinger.raw.txt]: "The vote change required to be on par with the ith highest copartisan candidate, that is, the one with the order statistic (n j −i + 1), is simply the difference between the two candidates’ number of votes."
QUOTE[luechinger.raw.txt]: "The candidate margin for candidate C 2 of party P2 is −14 for i = 1, 3 for i = 2, and 8 for i = 3."
CORRECTION: "p. 106" -> the section heading "2.2 Candidate Margin" starts at the bottom of p. 106 but the definition (the displayed equation) is on p. 107 (printed). Formula is in FORMULAS AS PRINTED (F-C).
NOTE: [stated] Also on p. 107: "To be the lowest-ranked candidate (i = n j ), candidate C h could lose all her votes." (footnote 6).

#### [C] C-19 | §4 How the literature writes it | overall vote margin = max over i of min{party margin, candidate margin}, p. 107 (line 114)
MARK: confirmed
SOURCE: https://doi.org/10.1017/pan.2023.22, the Cambridge Core open-access PDF as fetched by the orchestrating thread from www.cambridge.org (exact URL not in urls.txt; file SP/r4/src/luechinger_cup.out) (Political Analysis PDF) (local: luechinger.raw.txt; page image of printed p. 107 read) ; Sec. 2.3 "Aggregation", printed p. 107
QUOTE[luechinger.raw.txt]: "The binding margin is the minimum of the party margin and the candidate margin."
QUOTE[luechinger.raw.txt]: "Among all binding margins, we choose the smallest absolute vote change that would alter the election status of candidate C h . This is the maximum among all binding margins identified in the first step."
NOTE: [stated] Formula in FORMULAS AS PRINTED (F-D): vote margin_{h,i,j} = max over i in {1,...,n} of {min{party margin_{i,j}, candidate margin_{h,i,j}}}. This overall margin is per CANDIDATE (h in party j); the party margin alone is the per-party quantity. For a model of "one vote changes a seat" the relevant part is the party margin (the number of votes a party must lose/gain to change its seat count), and the overall margin needs the within-party vote distribution as well.

#### [C] C-20 | §4 How the literature writes it | worked example (hypothetical), D'Hondt, 3 seats, parties with 45, 35, 20 votes: P2's party margins are 15 (i=1), -10 (i=2), -100 (i=3) (line 115)
MARK: confirmed
SOURCE: https://doi.org/10.1017/pan.2023.22, the Cambridge Core open-access PDF as fetched by the orchestrating thread from www.cambridge.org (exact URL not in urls.txt; file SP/r4/src/luechinger_cup.out) (Political Analysis PDF) (local: luechinger.raw.txt) ; Sec. 2.1, printed p. 105
QUOTE[luechinger.raw.txt]: "Let us illustrate the calculation of the party margin for all three potential seats of party P2 ."
QUOTE[luechinger.raw.txt]: "The party could lose 15 votes to secure their first seat (i = 1) against party P3 . Thus, its party margin is 15 for i = 1."
QUOTE[luechinger.raw.txt]: "Thus, the party margin is −100 for i = 3."
QUOTE[luechinger.raw.txt]: "To achieve this, party P2 would need 10 additional votes and thus the party margin for i = 2 is −10."
NOTE: [stated] The example is introduced on p. 102 ("a district with three seats and three parties P1 , P2 , and P3 with 45, 35, and 20 votes. We assume that the D’Hondt method is employed"). The paper also does the candidate margins (C2 of P2: 22/8/5 votes; margins -14, 3, 8), the overall margin -10 (Table 1 "Aggregation of party and candidate margins", printed p. 108), and the Hare-Niemeyer party margin for P2's second seat (-27.5). P2's D'Hondt ratios 35, 17.5, 11.7; P1's 45.0, 22.5, 15.0; P3's 20, 10, 6.7.

#### [C] C-21 | §4 How the literature writes it | Abstract: "In contrast to plurality systems, closeness in PR systems cannot be directly inferred from votes" (line 116)
MARK: confirmed
SOURCE: https://doi.org/10.1017/pan.2023.22, the Cambridge Core open-access PDF as fetched by the orchestrating thread from www.cambridge.org (exact URL not in urls.txt; file SP/r4/src/luechinger_cup.out) (Political Analysis PDF) (local: luechinger.raw.txt) ; Abstract, p. 101
QUOTE[luechinger.raw.txt]: "In contrast to plurality systems, closeness in PR systems cannot be directly inferred from votes."
NOTE: [stated] The abstract has this sentence; the first pass's quote lacks the final full stop only.

#### [C] C-22 | §4 How the literature writes it | the paper "reports no real-election figure for how many votes would change a seat, and gives no pivotal probability"; "Not treated: the Droop quota" (line 116)
MARK: confirmed
SOURCE: https://doi.org/10.1017/pan.2023.22, the Cambridge Core open-access PDF as fetched by the orchestrating thread from www.cambridge.org (exact URL not in urls.txt; file SP/r4/src/luechinger_cup.out) (Political Analysis PDF) (local: luechinger.raw.txt; I searched the whole text for "pivot", "Droop", "how many votes", mean/median) ; whole paper, pp. 101-114
QUOTE[luechinger.raw.txt]: "For illustration purposes, we implement our approach and estimate the individual incumbency advantage in three countries"
QUOTE[luechinger.raw.txt]: "A major conceptual drawback of all methods based on simulated election probabilities is that the probabilities inherently depend on arbitrary choices of the simulation setup."
QUOTE[luechinger.raw.txt]: "The probability approaches a candidate’s election status with increasing sample size, it approaches the actual vote share of a candidate’s party with decreasing sample size."
QUOTE[luechinger.raw.txt]: "Already for around 5,000 resampled votes, the simulated election probabilities of all candidates converge to 0 for nonelected candidates or to 1 for elected candidates."
QUOTE[luechinger.raw.txt]: "For 44% of the candidates, the candidate margin is not defined"
NOTE: [stated, by search] The words "pivot" and "Droop" do not occur in the paper. [measured] grep "pivot|Droop" on luechinger.raw.txt returns nothing. The empirical part (Sec. 3) gives incumbency-advantage estimates (effect "between 30 and 45 percentage points" in Switzerland) using the margin as an assignment variable, plus: "For 44% of the candidates, the candidate margin is not defined" and "For 3% of the candidates, the party margin, not the candidate, is binding" (Switzerland, Fig. 4). Those are not figures for how many votes change a seat. SURPRISE for the orchestrator: the paper criticises resampling-based closeness (the Kotakorpi et al. 2017 method that Lyytikainen & Tukiainen build on, see C-25) with the text above and says (quotes above) that the simulated probability depends on the resample size. Fig. 5 (p. 112): for the 45/35/20 example "the election probability of the first-ranked candidate of party P2 ranges from 0.35 to 1" depending on the number of resampled votes. Whether this critique applies to L&T's use (resample size equal to the votes cast; the output is the share of repetitions with a pivotal event, not an election probability) is not stated in either paper.

#### [C] C-23 | §4 Published estimates | L&T citation: VATT Working Papers 50/2016 (Jan 2016 version; original Sept 2013), doria.fi wp50.pdf (line 119)
MARK: confirmed
SOURCE: https://www.doria.fi/bitstream/10024/148789/1/wp50.pdf (local: lyyt.txt) ; title page and front matter
QUOTE[lyyt.txt]: "This version (January 19, 2016) replaces the September 27, 2013 version."
QUOTE[lyyt.txt]: "VATT Institute for Economic Research VATT Working Papers 50/2016"
NOTE: [stated] The PDF is 67 pages (pdfinfo), Acrobat Distiller, created 25 Jan 2016. Finnish municipal elections are "proportional open list, D'Hondt" -- see C-24.

#### [C] C-24 | §4 Published estimates | L&T data: 1,747 municipality-elections, five elections 1996-2012, populations 234 to 44,804 (mean 7,506), council sizes 13 to 51 (mean 27), turnout mean 0.646; open list, D'Hondt (line 119)
MARK: confirmed
SOURCE: https://www.doria.fi/bitstream/10024/148789/1/wp50.pdf (local: lyyt.txt) ; Sec. 5 text, printed p. 22 (PDF p. 25); Table 3, printed p. 23 (PDF p. 26); Sec. 3 institutional text (D'Hondt, one district), printed p. 12 (PDF p. 15); Table 1, printed p. 13 (PDF p. 16)
QUOTE[lyyt.txt]: "We limit the sample used in the analysis to five election years and to municipalities with a population below 45,000. This leaves us with 1,747 municipality- election year (i.e., election) observations."
QUOTE[lyyt.txt]: "Turnout 1747 0.646 0.060 0.420 0.895"
QUOTE[lyyt.txt]: "Population 1747 7506 7592 234 44804"
QUOTE[lyyt.txt]: "Council size 1747 27 9 13 51"
QUOTE[lyyt.txt]: "The elections in our data were held in the October of 1996, 2000, 2004, 2008 and 2012."
QUOTE[lyyt.txt]: "The seats are allocated between parties based on the D’Hondt comparison method."
QUOTE[lyyt.txt]: "Each municipality has only one electoral district."
NOTE: [stated] Table 3 title: "Summary statistics for outcome and control variables (population < 45,000)." Columns: N, Mean, Std. Dev., Min, Max. The sample is capped at population below 45,000 (Table 1 covers population groups up to 45,000: N = 274, 465, 478, 307, 168, 55 = 1,747 [measured: sum]). Each voter gives a single vote to a single candidate (open list): "Each voter gives a single vote to a single candidate."

#### [C] C-25 | §4 Published estimates | L&T method Sec. 4.2: resample votes with replacement at the observed shares, same number of votes as cast, 1,000 repetitions (line 119)
MARK: confirmed
SOURCE: https://www.doria.fi/bitstream/10024/148789/1/wp50.pdf (local: lyyt.txt) ; Sec. 4.2, printed p. 18 (PDF p. 21)
QUOTE[lyyt.txt]: "We sample votes with replacement for each candidate, so that the sampling probability of a vote for a particular candidate is the share of all votes that he or she received in the real elections. We sample as many votes as were originally given in the real elections."
QUOTE[lyyt.txt]: "We repeat this exercise 1,000 times and count the share of times a pivotal event occurred for each party-election (between parties) and each candidate-election (within parties) observation."
NOTE: [stated] The paper says the basic procedure is the bootstrap of Kotakorpi et al. (2013). The number of votes sampled in the IV measure is the counterfactual turnout ("We use this adjusted fit as the counterfactual turnout that determines the number of votes given in our counterfactual simulations."). So Table 2 pivotality is simulated at counterfactual turnout (turnout net of the council-size-threshold effect), not at the realised turnout. The first pass called it "same number of votes as cast"; that is what the paragraph says and [inferred] what Table A1 "Real" rows use, but Table 2 (the "counterfactuals based on a 6th order polynomial specification") uses the adjusted-turnout vote count. Quote for that: see C-27.

#### [C] C-26 | §4 Published estimates | L&T pivotal event: tie "(in which case a lottery would determine who gets elected) and also when giving one more vote creates a draw or a different seat allocation directly" (line 119)
MARK: confirmed
SOURCE: https://www.doria.fi/bitstream/10024/148789/1/wp50.pdf (local: lyyt.txt) ; Sec. 4.2, printed p. 17 (PDF p. 20)
QUOTE[lyyt.txt]: "A pivotal event takes place both in the case of actual draws (in which case a lottery would determine who gets elected) and also when giving one more vote creates a draw or a different seat allocation directly."
QUOTE[lyyt.txt]: "We measure the incidence of cases were a single vote would make a difference. In contrast, elections where, for example, 3 votes would make a difference to the seat allocation could be seen a close, but would not count as pivotal in our metric."
QUOTE[lyyt.txt]: "We stress that our measure of pivotality is not a measure of closeness of elections in any more general sense."
NOTE: [stated] The wording is the paper's (including "were" for "where"). The pivotal event is "giving one more vote" (adding), and a draw (tie) counts as pivotal; the paper says nothing about removing a vote in the quoted definition (the first sentence of 4.2 does say "one abstaining voter could change ... by voting"). The paper does not say how a "different seat allocation" is computed beyond D'Hondt (footnote 6).

#### [C] C-27 | §4 Published estimates | L&T "election-level pivotality" = vote-share-weighted average of within- and between-party measures, "the probability that a randomly drawn voter would be pivotal" (line 119); the first pass could not read the aggregation formula
MARK: corrected
SOURCE: https://www.doria.fi/bitstream/10024/148789/1/wp50.pdf (local: lyyt.txt) ; Sec. 4.3, printed p. 20 (PDF p. 23; I rendered the page image and read it; no displayed equation on this page or the next before Table 2)
QUOTE[lyyt.txt]: "we take a weighted (by respective vote shares) average over both the within party pivotal probability (measured at the candidate level) and the between parties pivotal probability (measured at the party level) to calculate the probability that a randomly drawn voter would be pivotal in a given election."
QUOTE[lyyt.txt]: "We use either a single measure for pivotality, which is simply the sum of these weighted between and within pivotalities, or both of them separately."
QUOTE[lyyt.txt]: "We use this adjusted fit as the counterfactual turnout that determines the number of votes given in our counterfactual simulations."
QUOTE[lyyt.txt]: "For the pivotal probabilities we report the counterfactuals based on a 6th order polynomial specification similar to Model 1."
CORRECTION: "a vote-share-weighted average of within- and between-party measures" -> the paper says both "a weighted (by respective vote shares) average" and (next sentence) the single measure "is simply the sum of these weighted between and within pivotalities". The paper prints NO formula for the weights; there is no displayed equation for the aggregation (equation (5) on the next page is the IV system). The weights are only described as "respective vote shares". Also: Table 2 reports the simulated pivotality at counterfactual (adjusted) turnout from the 6th-order-polynomial specification, not at realised turnout.
NOTE: [stated] I looked at the page image (PDF p. 23, printed p. 20): the text is in words only. The exact aggregation cannot be written from the paper; any formula would be [inferred]. The paper does not define "respective vote shares" (candidate's share of the party's votes? party's share of all votes?).

#### [C] C-28 | §4 Published estimates | L&T Table 2 Panel A, election level: Pivotality mean 0.063, sd 0.031, min 0.006, max 0.193 (N = 1,746) (line 119; also line 277)
MARK: confirmed
SOURCE: https://www.doria.fi/bitstream/10024/148789/1/wp50.pdf (local: lyyt.txt) ; Table 2, printed p. 21 (PDF p. 24); rendered page image checked
QUOTE[lyyt.txt]: "Table 2. Describing endogenous variables in IV."
QUOTE[lyyt.txt]: "Pivotality 1746 0.063 0.031 0.006 0.193"
NOTE: [stated] N = 1746 as printed in Table 2 (Panel A). Table 3 and the Sec. 5 text have 1,747 elections; the IV tables say "Notes: Sample size is 1,746." The paper does not say which municipality-election is dropped. So 1,746 is right for Table 2; 1,747 is the data set (see C-24). Table 2 also prints, Panel A: Number of candidates 84 (sd 48; 14 to 305), Share of incumbents 0.26, Proportionality 0.014.

#### [C] C-29 | §4 Published estimates | L&T Table 2 Panel B, party-election between-party pivotality mean 0.020 (sd 0.020, max 0.130; N = 10,171) (line 119)
MARK: confirmed
SOURCE: https://www.doria.fi/bitstream/10024/148789/1/wp50.pdf (local: lyyt.txt) ; Table 2 Panel B, printed p. 21 (PDF p. 24)
QUOTE[lyyt.txt]: "Pivotality, between 10171 0.020 0.020 0.000 0.130"
NOTE: [stated] Min is 0.000. The text of the Introduction also gives the "real" figure for the average party as 0.020 ("from 1.7 times out of a hundred to 2.0, see Table 2"); those two numbers (0.017 -> 0.020) are printed in Table A1 (rows "CF down between" and "Real between"), not in Table 2 (the text's "see Table 2" points at the wrong table; the numbers are in A1).

#### [C] C-30 | §4 Published estimates | L&T within-party mean 0.006 (Table 2) versus 0.028 (Table A1, N = 146,234); paper says the gap "arise[s] mainly from the weighting" (line 119; the flagged inconsistency, line 277)
MARK: corrected
SOURCE: https://www.doria.fi/bitstream/10024/148789/1/wp50.pdf (local: lyyt.txt) ; Table 2 Panel B (printed p. 21), Table A1 and its note (Online Appendix A, printed p. 46, PDF p. 49), Sec. 4.3 last sentence (printed p. 20)
QUOTE[lyyt.txt]: "Pivotality, within 10171 0.006 0.009 0.000 0.164"
QUOTE[lyyt.txt]: "Real within 146234 0.028 0.051 0 0.389"
QUOTE[lyyt.txt]: "Real between 10171 0.020 0.020 0 0.123"
QUOTE[lyyt.txt]: "Notes: The unit of observation is election-party (first three rows) or election-candidate (last three rows)."
QUOTE[lyyt.txt]: "Differences to descriptions in Table A1 arise mainly from the weighting."
CORRECTION: The "inconsistency" is partly a difference of unit, as printed: Table 2 Panel B "Pivotality, within" is at the party-election level (N = 10,171; mean 0.006, sd 0.009, max 0.164); Table A1 "Real within" is at the election-candidate level (N = 146,234; mean 0.028, sd 0.051, max 0.389). The paper itself says the differences "arise mainly from the weighting" (Sec. 4.3). The paper does not give the weights (see C-27), so the two numbers cannot be reconciled from the paper; they are two printed values for two units. Also as printed: Table 2 is "counterfactuals based on a 6th order polynomial specification", Table A1 "Real" rows are the simulations at the real council size (and real turnout).
NOTE: [stated] Table A1 also prints, for between: CF down 0.017, Real 0.020, CF up 0.024 (N = 10,171); for within: CF down 0.024, Real 0.028, CF up 0.032 (N = 146,234). The Introduction text says "from 2.4 times out of a hundred to 2.8" for within-party. Quote for those: "pivotal occurrence between parties for the average party on average by about 18% (from 1.7 times out of a hundred to 2.0, see Table 2)" is in the next block.

#### [C] C-31 | §4 Published estimates | L&T Introduction: crossing the threshold raises between-party pivotality "from 1.7 times out of a hundred to 2.0, see Table 2", within-party "from 2.4 times out of a hundred to 2.8" (not in first pass; relevant to line 119)
MARK: confirmed
SOURCE: https://www.doria.fi/bitstream/10024/148789/1/wp50.pdf (local: lyyt.txt) ; Introduction, printed p. 3 (PDF p. 6)
QUOTE[lyyt.txt]: "crossing the threshold, where council size increases, increases the probability of pivotal occurrence between parties for the average party on average by about 18% (from 1.7 times out of a hundred to 2.0, see Table 2)"
QUOTE[lyyt.txt]: "the probability of pivotal occurrence for the last seat within parties for the average candidate increases on average by about 17% (from 2.4 times out of a hundred to 2.8)."
NOTE: [stated] The 1.7/2.0 and 2.4/2.8 pairs are Table A1's CF-down/Real means (0.017, 0.020; 0.024, 0.028), not Table 2. So the "within 0.028" is the real-council-size mean over candidates, which the paper itself quotes in its introduction as "2.8 times out of a hundred".

#### [C] C-32 | §4 Published estimates | L&T footnote 1: Mulligan & Hunter "one out of 89,000 in U.S. Congressional elections"; Gelman et al. "at best one out of 1 million for close U.S. national elections" (line 119)
MARK: confirmed
SOURCE: https://www.doria.fi/bitstream/10024/148789/1/wp50.pdf (local: lyyt.txt) ; footnote 1, printed p. 2 (PDF p. 5); rendered page image checked
QUOTE[lyyt.txt]: "Mulligan and Hunter (2003) show that the simple empirical frequency of pivotal vote is one out of 89,000 in U.S. Congressional elections. Gelman et al. (1998) discuss estimating these rare events and find that the pivotal probability is at best one out of 1 million for close U.S. national elections."
QUOTE[lyyt.txt]: "Mulligan C, Hunter C (2003). The Empirical Frequency of a Pivotal Vote. Public Choice 116,"
NOTE: [stated] These are L&T's characterisations of other papers, as secondary quotes; they are not read at the original here (Mulligan & Hunter 2003 is not among our local sources; the Gelman et al. (1998) paper is handled by other readers).

#### [C] C-33 | §4 Published estimates | L&T "smallest mainland municipality has roughly 800 inhabitants" vs Table 3 minimum population 234 (line 277)
MARK: corrected
SOURCE: https://www.doria.fi/bitstream/10024/148789/1/wp50.pdf (local: lyyt.txt) ; Sec. 3, printed p. 11 (PDF p. 14); Table 3, printed p. 23 (PDF p. 26)
QUOTE[lyyt.txt]: "The largest municipality is the country’s capital, which has over half a million inhabitants, whereas the smallest mainland municipality has roughly 800 inhabitants."
QUOTE[lyyt.txt]: "Population 1747 7506 7592 234 44804"
CORRECTION: "inconsistent" -> as printed there are two different statements: the text says the smallest *mainland* municipality has roughly 800 inhabitants; Table 3's population minimum over all 1,747 election observations is 234. Table 3 is population per municipality-election, with the "mainland" qualifier absent, so a non-mainland municipality (or a population figure in a particular election year) could be the 234; the paper does not say which, and does not say that the 800 is from the sample years. Not reconciled by the paper. [inferred] that "mainland" is why the two differ; the paper does not state it.
NOTE: The Table 3 minimum is of "population" per municipality-election in the five elections 1996-2012, for population < 45,000.

#### [C] C-34 | §4 Published estimates (Germany) | BVerfG press release 3 July 2008, 2 BvC 1/07: "if roughly 19,500 fewer second votes had been cast for the SPD, this party could as a result have claimed one more seat in the Deutscher Bundestag" ("negative voting weight") (line 120)
MARK: confirmed
SOURCE: https://www.bundesverfassungsgericht.de/SharedDocs/Pressemitteilungen/EN/2008/bvg08-068.html (local: work-C/bverfg08.txt, plain text of txt/bverfg08.html made by me) ; Press Release No. 68/2008 of 3 July 2008, section IV
QUOTE[work-C/bverfg08.txt]: "In Hamburg for instance, if roughly 19,500 fewer second votes had been cast for the SPD, this party could as a result have claimed one more seat in the Deutscher Bundestag."
QUOTE[work-C/bverfg08.txt]: "Urteil vom 3. Juli 2008 - 2 BvC 1/07"
NOTE: [stated] The first pass's quote is a correct substring but omits the context "In Hamburg for instance" (the example is a Land, Hamburg). The sentence is about one example, not a general count.

#### [C] C-35 | §4 Published estimates (Germany) | "it is also possible that not casting a voter's vote is beneficial to the party to be supported"; provisions "unconstitutional insofar as the effect of negative voting weight is facilitated thereby"; deadline 30 June 2011; 16 overhang mandates in the 16th Bundestag (line 120)
MARK: confirmed
SOURCE: https://www.bundesverfassungsgericht.de/SharedDocs/Pressemitteilungen/EN/2008/bvg08-068.html (local: work-C/bverfg08.txt) ; Press Release No. 68/2008
QUOTE[work-C/bverfg08.txt]: "Conversely, it is also possible that not casting a voter's vote is beneficial to the party to be supported."
QUOTE[work-C/bverfg08.txt]: "The provision is therefore unconstitutional insofar as the effect of negative voting weight is facilitated thereby."
QUOTE[work-C/bverfg08.txt]: "The legislature was obliged to hand down a constitutional provision by 30 June 2011 at the latest."
QUOTE[work-C/bverfg08.txt]: "This also applies to the election to the 16th Deutscher Bundestag, where there were a total of 16 "overhang mandates"."
NOTE: [stated] The press release's straight apostrophes and quotation marks are as in the file. The 16 overhang mandates are the number of overhang seats in the 16th Bundestag, not the number of seats at which the effect arose.

#### [C] C-36 | §4 Non-monotonicity in PR | the press release attributes negative weight to second votes for parties that win overhang mandates in a Land (it "may arise in certain constellations"); [inferred] it is a property of the mixed system's overhang rules rather than of the divisor method (line 137)
MARK: corrected
SOURCE: https://www.bundesverfassungsgericht.de/SharedDocs/Pressemitteilungen/EN/2008/bvg08-068.html (local: work-C/bverfg08.txt) ; Press Release No. 68/2008, lead paragraph and sections II.2 and IV
QUOTE[work-C/bverfg08.txt]: "The effect of negative voting weight brought about by § 7.3 sentence 2 in conjunction with § 6.4 and 6.5 of the Federal Electoral Act (Bundeswahlgesetz - BWahlG) may lead to a situation in which in certain constellations second votes cast for parties which obtain what are known as "overhang mandates" in one Land (state) have a negative impact inasmuch as these parties lose mandates in the same or in another Land."
QUOTE[work-C/bverfg08.txt]: "The negative voting weight effect is also not a necessary consequence of a system of proportional representation combined with the personal election of candidates. The effect depends on various factors, but above all on the model of setting off the first-vote mandates with the second-vote mandates, which do not determine the electoral system as such."
QUOTE[work-C/bverfg08.txt]: "With regard to the fact that the negative voting weight effect is indivisibly linked to the "overhang mandates" and to the possibility of list combinations,"
QUOTE[work-C/bverfg08.txt]: "This effect is not a very rare exception, but as a rule has an impact on the result of elections if "overhang mandates" are created in an election to the Deutscher Bundestag."
CORRECTION: "(it 'may arise in certain constellations')" is not verbatim; the text is "may lead to a situation in which in certain constellations second votes cast for parties which obtain what are known as 'overhang mandates' in one Land (state) have a negative impact inasmuch as these parties lose mandates in the same or in another Land". The effect is on parties losing mandates "in the same or in another Land" (the Court's own wording is about Land lists). The [inferred] reading in the first pass is supported by the Court's own wording (second and third quote): the effect "depends ... above all on the model of setting off the first-vote mandates with the second-vote mandates" and is "indivisibly linked to the overhang mandates and to the possibility of list combinations". The press release does not mention divisor methods or Sainte-Laguë/D'Hondt at all (searched).
NOTE: [stated] "negative voting weight" is described at the level of a party's seat total ("an increase in the number of votes lead to a loss of mandates", section II.1: "An electoral system which is designed or at least in typical constellations permits an increase in the number of votes to lead to a loss of mandates ... leads to arbitrary results").

#### [C] C-37 | §4 Rules / Published estimates | BSW 2025, provisional: 2,468,670 of 49,642,087 valid second votes; lacked "exakt 13.435 Zweitstimmen" (Stuttgarter Zeitung, from Bundeswahlleiterin data) (line 121)
MARK: confirmed
SOURCE: https://www.stuttgarter-zeitung.de/panorama/13000-stimmen-zu-wenig-fuer-das-bsw-78867876.html (local: work-C/stuttgarter.txt, plain text of txt/stuttgarter.html made by me) ; section "BSW fehlen 13.435 Zweitstimmen"
QUOTE[work-C/stuttgarter.txt]: "Es waren nach Berechnung auf Grundlage von Daten der Bundeswahlleiterin exakt 13.435 Zweitstimmen, die der neuen Partei fehlten. 2.468.670 Stimmen holte das BSW von insgesamt 49.642.087 gültigen. Das sind 4,97293758 Prozent, bei mathematischer Rundung auf zwei Nachkommastellen also 4,97 Prozent und somit eindeutig weniger als 5,0 Prozent."
QUOTE[work-C/stuttgarter.txt]: "Das BSW hätte zum Einzug in den Bundestag mindestens 2.482.105 Stimmen benötigt, erhielt jedoch nur 2.468.670."
QUOTE[work-C/stuttgarter.txt]: "Das Wagenknecht-Ergebnis mit etwa 13.000 Stimmen zu wenig ist indes eines der knappsten und unglücklichsten in 76 Jahren Wahlgeschichte der Bundesrepublik."
NOTE: [stated] "13.435" is the newspaper's own calculation ("nach Berechnung auf Grundlage von Daten der Bundeswahlleiterin"), not a figure published by the Bundeswahlleiterin. [measured] by me (work-C/bsw.py): 0.05 x 49,642,087 = 2,482,104.35, so the least whole number of BSW votes at or above 5% of the provisional valid votes is 2,482,105 (agrees with the paper), and 2,482,105 - 2,468,670 = 13,435 (agrees). This convention holds the total of valid votes fixed (the extra BSW votes would be switched from other parties' votes). The paper's share 4.97293758% is also reproduced: 2,468,670 / 49,642,087 = 4.97293758% [measured]. The article calls the provisional share "4,97 Prozent". The page is dated "24.02.2025, 17:34 Uhr" (the day after the 23 Feb 2025 election), so it uses the provisional result; its table is headed "Vorläufiges amtliches Endergebnis der Bundestagswahl 2025".

#### [C] C-38 | §4 Published estimates (Germany) | the final count added 4,277 valid second votes for BSW (t-online) (line 121)
MARK: confirmed
SOURCE: https://www.t-online.de/nachrichten/deutschland/id_100636312/bsw-auch-nach-endgueltigem-ergebnis-nicht-im-bundestag.html (local: work-C/tonline.txt, plain text of txt/tonline.html made by me) ; article text, page stamp "Aktualisiert am 14.03.2025"
QUOTE[work-C/tonline.txt]: "Die Partei von Sahra Wagenknecht erhielt im Vergleich zum vorläufigen Ergebnis aus der Wahlnacht zwar weitere 4.277 gültige Zweitstimmen zugeschrieben, wie der Bundeswahlausschuss bei seiner Sitzung in Berlin feststellte. Mit 4,98 Prozent blieb sie aber trotzdem knapp unter der Fünf-Prozent-Hürde."
QUOTE[work-C/tonline.txt]: "Bei der CDU kamen beispielsweise 1.674 Stimmen dazu, bei der SPD 840 und bei der AfD 1.632. Dagegen wurden der FDP 121 Stimmen abgezogen."
NOTE: [stated] "weitere 4.277 gültige Zweitstimmen" is the change relative to the provisional result. [measured] it matches the official final minus provisional: 2,472,947 - 2,468,670 = 4,277 (final from C-39, provisional from C-37). The article rounds to 4.98%; the official figure printed by the Bundeswahlleiterin is 4.981% (C-11).

#### [C] C-39 | §4 Published estimates (Germany) | FINAL totals and exact final shortfall of BSW to 5% (the first pass subtracted 13,435 - 4,277 = 9,158 and admitted it did not read the final totals) (line 121; also line 282 = §10.3 item 10)
MARK: corrected
SOURCE: https://www.bundeswahlleiterin.de/en/bundestagswahlen/2025/ergebnisse/bund-99.html (local: work-C/bwl_results.txt, plain text I made from the downloaded page work-C/dl/bund99_en.html) ; "Result table Final result", Federal Returning Officer, Bundestag election 2025 (Germany as a whole)
QUOTE[work-C/bwl_results.txt]: "Valid 49,505,389 99.2 +0.2 49,649,512 99.4 +0.3"
QUOTE[work-C/bwl_results.txt]: "BSW 299,401 0.6 - 2,472,947 4.981 -"
QUOTE[work-C/bwl_results.txt]: "Persons entitled to vote 60,510,631 - - 60,510,631 - -"
QUOTE[work-C/bwl_results.txt]: "Voters 49,928,653 82.5 +6.2 49,928,653 82.5 +6.2"
CORRECTION: 9,158 ("roughly 9,000 to 10,000") -> exact figures from the final result (second votes: BSW B = 2,472,947; valid second votes V = 49,649,512; share 4.981%). Shortfall to 5.000%: (a) if the extra BSW votes are switched from other parties' votes (V unchanged, the Stuttgarter Zeitung convention): need B + x >= V/20 = 2,482,475.6, so the least whole x is 2,482,476 - 2,472,947 = **9,529** votes. (b) if the extra BSW votes are new valid votes (e.g. from invalid ballots or non-voters, so V grows with them): (B + x) / (V + x) >= 0.05, x >= (V - 20B)/19 = (49,649,512 - 49,458,940)/19 = 190,572/19 = 10,030.105..., so the least whole x is **10,031**.
NOTE: [measured] script work-C/bsw.py (output in work-C/bsw_out.txt, exact Fraction arithmetic, assertions that x and x-1 straddle 5%): final share 4.98080827% (prints as 4.981% to three decimals, as the Bundeswahlleiterin prints); final change from provisional: valid second votes 49,649,512 - 49,642,087 = 7,425 (matches "7,425 higher than in the provisional result", C-11) and BSW 2,472,947 - 2,468,670 = 4,277 (matches t-online, C-38). The first pass's 9,158 differs from the V-fixed convention's 9,529 by 371 = the rise of the 5% line (7,425 x 0.05 = 371.25) - the first pass said it ignored that; the correct subtraction is 13,435 + 371 - 4,277 = 9,529 (13,434.35 + 371.25 - 4,277 = 9,528.6, rounded up to 9,529). Also: 9,529 is 0.385% of BSW's final votes and 0.0192% of all valid second votes (about 1 in 5,210 valid second votes); and in absolute terms about 9,529 to 10,031 votes. Arithmetic for (b): 20B = 49,458,940; V - 20B = 190,572; /19 = 10,030.1 (exact 10,030.105...), so x = 10,031 (and x = 10,030 gives (B+x)/(V+x) = 2,482,977/49,659,542 = 4.99999...% < 5%; the script asserts this). The Bundeswahlleiterin's results page is for "Final result"; it also lists first votes for BSW 299,401 (0.6%).

#### [C] C-41 | §4 Published estimates (Germany) / task item 5 | "The 2023 reform (second-vote coverage) was designed to remove overhang seats; I did not read a source on whether negative weight can still occur under it." (line 120)
MARK: confirmed (that overhang seats were removed by the reform; that no source I read says whether negative voting weight can still occur) -- the question itself stays OPEN: no source found that states it either way
SOURCE: (1) https://www.bundesverfassungsgericht.de/SharedDocs/Entscheidungen/DE/2024/07/fs20240730_2bvf000123.html (local: work-C/bverfg24_de.txt, the full German judgment of 30 July 2024, read by curl, searched for "Stimmgewicht", "negativ", "Umkehrung", "Mandatsverlust", "widersinn"); (2) https://dserver.bundestag.de/btd/20/053/2005370.pdf (local: work-C/btd20_5370.txt, the bill Drucksache 20/5370 of 24 Jan 2023, searched for "negativ", "Stimmgewicht", "Monoton"); (3) https://www.bundestag.de/services/glossar/negatives-stimmengewicht-869620 (local: work-C/bt_glossar.txt); (4) https://www.gesetze-im-internet.de/bwahlg/__4.html and __5.html (local: work-C/bwahlg4.txt, bwahlg5.txt)
QUOTE[work-C/bverfg24_de.txt]: "(d) Schließlich kann das Zweistimmenwahlrecht unter bestimmten Umständen sogar zu einer Umkehrung des Stimmgewichts führen (negatives Stimmgewicht)."
QUOTE[work-C/bverfg24_de.txt]: "Nach dem Zweitstimmendeckungsverfahren werden vor dem Ausgleich keine Mandate vergeben. Zunächst erfolgt die Verteilung der 630 Sitze auf die Parteien und ihre Landeslisten."
QUOTE[work-C/bverfg24_de.txt]: "Dies führte zudem zum Auftreten von negativen Stimmgewichten"
QUOTE[work-C/btd20_5370.txt]: "Durch die Abschaffung von Überhangs- und Ausgleichsmandaten wird die Größe der"
QUOTE[work-C/bt_glossar.txt]: "durch eine Wahlrechtsreform wird der Effekt des negativen Stimmgewichts nun durch Ausgleichsmandate verhindert."
QUOTE[work-C/bwahlg4.txt]: "Zwischen den Parteien werden die Sitze im Verhältnis der Zahl der Zweitstimmen, die im Wahlgebiet für die Landeslisten der Partei abgegeben wurden, nach § 5 verteilt (Oberverteilung)."
QUOTE[work-C/bwahlg5.txt]: "Der Zuteilungsdivisor wird so bestimmt, dass alle verfügbaren Sitze verteilt werden."
NOTE: [stated] What the sources say: (a) The Court's 2024 judgment recites negative weight as a principle (para. 156: "in keinem Fall darf ein Wahlsystem darauf ausgelegt sein oder jedenfalls in typischen Konstellationen zulassen, dass ein Zuwachs an Stimmen zu Mandatsverlusten führt") and recounts that overhang seats led to it and that the 2008 and 2012 judgments struck down earlier rules; it does NOT say whether the 2023 law can produce it (the words "negatives Stimmgewicht" occur in the judgment only in the history and in para. 156; none in a finding about the new procedure). (b) The 2023 bill never uses "negativ"/"Stimmgewicht" (searched); it says the abolition of overhang and compensation seats secures equality of success value "in höherem Maße" than before. (c) The Bundestag glossary entry says the effect "wird ... nun durch Ausgleichsmandate verhindert", which describes the 2013 reform (compensation seats), not the 2023 law, which abolished compensation seats; the page is undated in my copy, so it is not evidence about the 2023 law. (d) The statute: party seat totals come from § 4(2)/§ 5 (a divisor method with standard rounding on the nationwide second votes, minus the second votes of voters whose first vote went to a successful independent candidate, and minus parties under 5%), then § 4(3) Land distribution, then § 6 coverage. [inferred, not stated by any source] Since the Court's 2008 text attributes the effect to overhang mandates and Land-list set-off (C-36) and the 2023 law has neither, the 2008 mechanism is absent; whether other routes exist (e.g. the discount of second votes of voters for successful independent candidates, the § 4(4) majority top-up, the 5% rule's effect on others' seats) is not addressed by any source I read. For the party's own total, see F-4.

#### [C] C-42 | §4 Size relative... (line 134) | L&T party-election means "sit in the same range as my council-sized row ... a factor of 3 to 4 higher"; council M = 27 on average; "roughly 4,000 voters in an average municipality if about 80% of residents are eligible [assumption] and turnout is 65%"
MARK: confirmed (the L&T inputs and the arithmetic); the comparison itself is the first pass's own [inferred] reading and not checkable at a source
SOURCE: https://www.doria.fi/bitstream/10024/148789/1/wp50.pdf (local: lyyt.txt) ; Table 3 (printed p. 23), Table 2 Panel B (printed p. 21)
QUOTE[lyyt.txt]: "Council size 1747 27 9 13 51"
QUOTE[lyyt.txt]: "Pivotality, between 10171 0.020 0.020 0.000 0.130"
NOTE: [measured] 7,506 (mean population, Table 3) x 0.8 (the first pass's assumption) x 0.646 (mean turnout, Table 3) = 3,879 votes, "roughly 4,000" as the first pass says. 0.020 / 0.0052 = 3.8 and 0.020 / 0.0067 = 3.0, so "a factor of 3 to 4" matches the first pass's own table row (council-sized, 0.0052-0.0067). The paper prints no electorate size; it prints mean population 7,506 and mean turnout 0.646 only. [stated] The paper's Table 2 simulation takes the number of votes sampled from counterfactual turnout (C-27), and its units are all parties of the municipality (mean 5.8 parties, Table 3), not the 5 parties of the first pass's example.

#### [C] C-43 | §4 Size relative to a two-candidate plurality race | own computations: script pr.py cross-checked by pr_check.py; table rows with Q_j and M/N; "Reading"; "Q_A x N = 7.0 to 7.4" (lines 124-133)
MARK: unread (not a source fact)
SOURCE: none; these are the first pass's own [measured] and [inferred] statements, not statements of any source.
NOTE: Not re-run by me; my task is to read each fact at its source. Where a source number enters them (L&T means, Table 3), see C-42. Where the text says "[measured] by me" the orchestrating thread should rely on the script, not on this file.

ORCHESTRATING WORKER: the reader marked this unread because it is the first pass's own calculation or arithmetic, not a source claim. The calculation was re-run and reproduces (see "Appendix A re-run").

#### [C] C-44 | §4 Size relative... (line 135) | "Thresholds create a second, much larger-benefit pivot ... Pr(party's share within one vote of 5%) is about (density of the party's share at 5%) divided by N. [inferred from Gelman-type density formula; I did not find a published estimate.]"
MARK: unread (inferred; no source)
SOURCE: none
NOTE: The Gelman et al. density-based formula is read by another reader. The BSW 2025 case gives one realised near-threshold number for Germany: BSW's final shortfall was 9,529 votes (V fixed) or 10,031 (new valid votes), i.e. about 0.0192% of valid second votes (C-39). That is a count of votes away, not a probability, and does not test the first pass's formula.

## 5. Single transferable vote (STV)

*First-pass lines 139-150 of `research/electoral-systems.md`. Each block: the first-pass claim with its line number, the mark, the source and location, exact quotes, the correction if any, notes.*

#### [B] B-32 | §5 line 144 | Counts by type: committee-size 9 (0.86% of multiwinner); upward 23 (2.1%); downward 17 (1.6%); no-show 39 (3.6%) (line 144)
MARK: unread (the body of the paper; the abstract has no per-type counts)
SOURCE: not read; Springer "Client Challenge". Preprint arXiv 2305.17741 (v3) listed under NEED-FETCH.
NOTE: [measured] consistency check of the first pass's numbers only: 9/1049 = 0.858% (matches 0.86% if the base is the 1,049 multiwinner elections); 23/1079 = 2.13%, 17/1079 = 1.58%, 39/1079 = 3.61% (match 2.1%, 1.6%, 3.6% if the base is all 1,079 elections; 23/1049 would be 2.19%). The four counts sum to 88 > 62, so some elections have more than one type of anomaly (26 fewer elections than counts) [measured]. [inferred] the denominators; the paper must say which. Nothing here is a confirmation.

#### [B] B-34 | §5 line 144 | The authors say their results are a lower bound and "similar to prior empirical research and much lower than most theoretical research" (line 144)
MARK: corrected (quote) / unread (lower bound)
SOURCE: Crossref abstract (above)
QUOTE[dl/crossref_scot.abstract.txt]: "We generally find that anomaly rates are similar to prior empirical research and much lower than what most theoretical research has found."
CORRECTION: the first pass's quoted words "similar to prior empirical research and much lower than most theoretical research" are not in the abstract; the abstract's words are "similar to prior empirical research and much lower than what most theoretical research has found". The first pass's string may have come from the paper's body (unread) or may be an extractor paraphrase placed in quotation marks. Do not quote the first-pass form.
NOTE: "lower bound" unread.

#### [B] B-35 | §5 line 144 / line 281 (item 9) | the introduction states "on the order of 1-4% for each type", which does not match the committee-size rate 0.86% (lines 144, 281)
MARK: unread
SOURCE: not read (body of the Springer paper)
NOTE: [inferred] The two numbers would not conflict if "on the order of 1-4%" is read as a rough order of magnitude and 0.86% as "about 1%", or if the first pass's extractor misread the sentence; I cannot decide this without the paper. The consistency check in B-32 shows the other three rates (2.1%, 1.6%, 3.6%) do fall in 1-4%, and that only the committee-size rate is below 1%. NEED-FETCH: arXiv 2305.17741 (introduction).

#### [B] B-36 | §5 line 141 | Fox & Bruyns, Social Choice and Welfare 67 (2026) 143-166; they describe STV as "a multiwinner version of IRV"; that paper analyses single-winner data only (line 141)
MARK: citation confirmed (metadata); the quote and the data claim unread
SOURCE: https://api.crossref.org/works/10.1007/s00355-025-01638-2 (local: dl/crossref_fox.abstract.txt) ; DOI 10.1007/s00355-025-01638-2
QUOTE[dl/crossref_fox.abstract.txt]: "TITLE: An evaluation of Borda count variations using ranked choice voting data | JOURNAL: Social Choice and Welfare | VOLUME: 67 | ISSUE: 1 | PAGES: 143-166"
QUOTE[dl/crossref_fox.abstract.txt]: "then empirically study 421 U.S. ranked choice elections conducted from 2004 to 2023 to determine the frequency of voting failures when using five Borda variations."
NOTE: [stated] Surprise for the orchestrator: the paper at that DOI is about Borda-count variations (published online 10 Nov 2025; print issue Aug 2026), not about STV or Scottish elections. The first pass cited it for a definitional phrase ("a multiwinner version of IRV"); the abstract does not mention STV, so the phrase is unread. The data are 421 U.S. ranked choice elections 2004-2023 (abstract), which fits "single-winner data only" for US RCV, but the abstract does not say "single-winner". Preprint: arXiv 2501.00618 (NEED-FETCH).

#### [B] B-37 | §5 line 141 | "I found no source that writes an explicit pivot-probability formula for multi-winner STV" (line 141, inferred)
MARK: confirmed as far as my searches go [inferred]
SOURCE: searches for F-03 (see there); none of the pages read gives such a formula
NOTE: see F-03.

---

#### [B] B-38 | §5 | Laird, Malmskog, Pixler & Rodbell, "Simulating Single Transferable Voting for the Colorado House of Representatives", arXiv 2607.25105v1 (27 Jul 2026) (line 145)
MARK: confirmed
SOURCE: https://arxiv.org/pdf/2607.25105 (local: laird.txt, laird.raw.txt) ; page 1
QUOTE[laird.txt]: "SIMULATING SINGLE TRANSFERABLE VOTING FOR THE"
QUOTE[laird.txt]: "COLORADO HOUSE OF REPRESENTATIVES"
QUOTE[laird.txt]: "NORA NELSON LAIRD, BETH MALMSKOG, IRIS PIXLER, AND KATHERINE RODBELL"
QUOTE[laird.txt]: "arXiv:2607.25105v1 [cs.CY] 27 Jul 2026"
NOTE: [stated] The identifier and date are printed in the PDF's left margin (the stamp reads "arXiv:2607.25105v1 [cs.CY] 27 Jul 2026"). The paper is about simulating STV with 10,000 multi-member districting plans of Colorado and ballots generated from 2022 Colorado attorney general returns; it asks how STV would change party representation in the 65-member Colorado House. It reports seat results, not pivotal probabilities. 22 pages (PDF info).
QUOTE[laird.raw.txt]: "We investigated this objective by producing 10,000"
QUOTE[laird.raw.txt]: "multi-member districting plans of Colorado, generating ranked ballots for each"

#### [B] B-39 | §5 | Laird: defines the anomaly as "decreased support for a candidate can improve their chances of getting elected"; says STV "does, in rare cases, violate the monotonicity criterion"; (line 145)
MARK: confirmed
SOURCE: laird.raw.txt ; Sec. 2.1, printed pp. 3-4 (page image pdf p. 3)
QUOTE[laird.raw.txt]: "Although STV generally results in more proportional representation, it does, in rare"
QUOTE[laird.raw.txt]: "cases, violate the monotonicity criterion of fair elections [32]."
QUOTE[laird.raw.txt]: "STV, decreased support for a candidate can improve their chances of getting elected,"
NOTE: [stated] full sentence, after the line breaks: "In other words, under STV, decreased support for a candidate can improve their chances of getting elected, while increased support can worsen their chances of getting elected." The claim is attributed to reference [32], which the bibliography gives as McCune & Graham-Squire, Monotonicity anomalies in Scottish local government elections, Social Choice and Welfare 63(1): 69-101, 2024. So Laird et al. is a secondary citation of the Scottish paper, not independent evidence.

#### [B] B-40 | §5 | Laird: "the complexity of the STV algorithm makes it unlikely for any one voter to take advantage of this anomaly" (line 145)
MARK: confirmed
SOURCE: laird.raw.txt ; Sec. 2.1, printed p. 4
QUOTE[laird.raw.txt]: "represent their actual preference order of candidates. However, the complexity of"
QUOTE[laird.raw.txt]: "the STV algorithm makes it unlikely for any one voter to take advantage of this"
NOTE: [stated] continues "anomaly [32]. Furthermore, Arrow's Impossibility Theorem states that every RCV system violates some reasonable fairness criterion, indicating that rare monotonicity violations do not provide sufficient reasoning to discount STV...". Qualitative; also cited to [32]. [measured] The words "pivot", "decisive" and "frequen..." (as a count) do not occur in the paper's text apart from one sentence in the Introduction about how frequently pathologies occur in other work ("to see how frequently pathologies like monotonicity violations occur"). So "reports no pivotality or frequency number": confirmed.
QUOTE[laird.raw.txt]: "ranked choice voting data to see how frequently pathologies like monotonicity violations occur"

---

#### [B] B-41 | §5 | Summary: "1,370 ballot papers had been lost between the earlier counts and the re-count"; "14 votes ahead of the other at the determinative point"; re-count "12 votes ahead at the determinative point" (line 148)
MARK: confirmed (via WebFetch only)
SOURCE: https://mta-sts.hcourt.gov.au/assets/publications/judgment-summaries/2014/hca5-2014-02-18.pdf (WebFetch, no local file) ; summary dated 18 February 2014. Full judgment: https://www.hcourt.gov.au/sites/default/files/eresources/2014/HCA/5.pdf (WebFetch).
WEBFETCH-EXTRACT (summary): "it emerged that 1,370 ballot papers had been lost between the earlier counts and the re-count."
WEBFETCH-EXTRACT (summary): "one of those candidates was 14 votes ahead of the other at the determinative point."
WEBFETCH-EXTRACT (summary): "the candidate who had been excluded in the earlier counts was instead 12 votes ahead at the determinative point."
WEBFETCH-EXTRACT (summary): "The number of ballot papers lost far exceeded the margin between the candidates at the determinative point in the count."
WEBFETCH-EXTRACT (judgment): "1,370 of them had been lost" (para 1); "Mr Bow had 23,515 votes and Mr van Burgel had 23,501 (a difference of 14 votes in favour of Mr Bow)" (para 42, before the fresh scrutiny); "Mr van Burgel had 23,526 votes and Mr Bow had 23,514 (a difference of 12 votes in favour of Mr van Burgel)" (para 50, after the re-count).
NOTE: [stated, via WebFetch] The two candidates are Mr Bow and Mr van Burgel at "the 50th exclusion point" (judgment); the lead reverses between the original count (Bow +14) and the re-count (van Burgel +12), which the first pass's wording ("one of the two candidates was 14 votes ahead ... the re-count result was 12 votes ahead") leaves open; the 12-vote lead belongs to the other candidate. These are votes held by the two candidates at that point of the Senate count (each about 23,500), not a gap between vote totals of the whole election.

#### [B] B-42 | §5 | "a further hearing on 20 February 2014 would 'determine the final disposition of the petitions'" (line 148)
MARK: confirmed (via WebFetch only)
SOURCE: the summary (above)
WEBFETCH-EXTRACT (summary): "The Court will hold a further hearing on Thursday, 20 February 2014 to determine the final disposition of the petitions."
NOTE: The judgment's order 3 (WebFetch): "Stand over further hearing of petitions to Thursday, 20 February 2014 at 12 noon in Melbourne." The case page https://www.hcourt.gov.au/cases/case_c17-2013 (WebFetch) lists a hearing on 20/02/2014 and the judgment (summary) of 18/02/2014 and says nothing about the outcome.

#### [B] B-43 | §5 | "Not read: the judgment itself, the electorate size, and what happened next" (line 148)
MARK: partly read now: the judgment (via WebFetch), the number of ballots; the outcome is NOT on the hcourt pages I could reach
SOURCE: judgment para 49 (WebFetch)
WEBFETCH-EXTRACT (judgment): "1,349,635 ballot papers were submitted at the election of senators for Western Australia" (para 49).
NOTE: [stated, via WebFetch] 1,349,635 ballot papers submitted at the WA Senate election (not the number of enrolled electors, which the judgment does not give). [measured] a 14-vote lead is 14 / 1,349,635 = 0.00104% of the ballot papers. The judgment (para 18, para 122 per the extract) reasons that "the only relief appropriate is for the election to be declared void", but the 18 February summary and the case page do not report the final order. The final disposition (election void; new WA Senate election on 5 April 2014) is **unread**: I did not find it on a page I may request. The AEC's media release dated 20 February 2014, "Court of Disputed Returns voids 2013 WA Senate election result" (found by search at https://emailfooter.aec.gov.au/media/media-releases/2014/02-20.htm; the AEC's own host is aec.gov.au), is the likely source: NEED-FETCH.
(The unrelated [2014] HCA 7 is Electricity Generation Corporation v Woodside Energy, 5 March 2014, so the second AEC judgment is not numbered HCA 7; I did not find its citation.)

---

#### [B] B-44 | §5 | "I did not read a source stating the Droop quota formula, so none is given." (line 150)
MARK: gap now filled: see F-01 (Ireland's Electoral Commission; Laird et al. page 3; ACE via WebFetch)
SOURCE: see F-01
NOTE: [stated] see F-01.

#### [F] F-01 | §5 | Ordeshook & Zeng, "Some Properties of Hare Voting with Strategic Voters", Public Choice 78(1) (1994) 87-101, Caltech working paper 772 (1991), URL records/ev76a-f2977 (line 146)
MARK: confirmed
SOURCE: https://authors.library.caltech.edu/records/ev76a-f2977 (local: ordeshook.html; plain-text strip work-F/ordeshook.plain.txt) ; abstract page. PDF read at https://authors.library.caltech.edu/records/ev76a-f2977/files/sswp772.pdf?download=1 (local: work-F/sswp772.txt), cover page
QUOTE[work-F/ordeshook.plain.txt]: "Published as Ordeshook, Peter C., and Langche Zeng. "Some properties of hare voting with strategic voters." Public Choice 78, no. 1 (1994): 87-101."
QUOTE[work-F/ordeshook.plain.txt]: "Published September 1991"
QUOTE[work-F/ordeshook.plain.txt]: "Series Volume or Issue Number 772"
QUOTE[work-F/sswp772.txt]: "SOCI AL SCIENCE WORKING PAPER 772 September 1991"
NOTE: The Caltech file is the 1991 working paper (Social Science Working Paper 772), not the journal text; it is a ClearScan OCR (the OCR prints "STY" for "STV"). Journal pagination 87-101 is stated on the abstract page only as the "Published as" line.

#### [F] F-02 | §5 | Ordeshook & Zeng abstract: "strategic voting does not ensure the selection of Condorcet winning candidates" (line 146)
MARK: confirmed
SOURCE: https://authors.library.caltech.edu/records/ev76a-f2977 (local: work-F/ordeshook.plain.txt) ; Abstract. Same sentence in the PDF abstract (work-F/sswp772.txt)
QUOTE[work-F/ordeshook.plain.txt]: "STY is not necessarily incentive compatible and strategic voting does not ensure the selection of Condorcet winning candidates or of Condorcet outcomes."
QUOTE[work-F/sswp772.txt]: "STY is not necessarily incentive compatible and strategic voting does not ensure the selection of Condorcet winning candidates or of Condorcet outcomes."
NOTE: The first pass wrote the phrase as a quote; the full printed sentence continues "or of Condorcet outcomes". [stated]

#### [F] F-03 | §5 | "The page shows no pivot analysis; the PDF body was not read" (line 146)
MARK: corrected
SOURCE: https://authors.library.caltech.edu/records/ev76a-f2977/files/sswp772.pdf?download=1 (local: work-F/sswp772.txt; the 18-page PDF: text layer searched for pivotal/decisive/probability/tie, and the passages around every hit, the abstract and the introduction read; the case-by-case proofs in the appendix pages were skimmed, not studied) ; Sec. 3 (Example 4 discussion), Sec. 4
QUOTE[work-F/sswp772.txt]: "First, although each voter knows that he or she is unlikely to be pivotal, each voter also knows that its vote is irrelevant unless it is pivotal. Thus, one alternative is to restrict ourselves to examining equilibria in which at least one voter is pivotal. We call such equilibria individually stable."
QUOTE[work-F/sswp772.txt]: "The particular difficulty here, though, is that no individual voter is decisive for the outcome"
QUOTE[work-F/sswp772.txt]: "these twenty four voters, although they render all other voters pivotal, do not create a situation in which any of these other voters prefers to be insincere."
CORRECTION: "PDF body not read; no pivot analysis" -> body now read (1991 working-paper version): the paper uses "pivotal" qualitatively (an equilibrium concept called "individually stable", in which at least one voter is pivotal; examples in which the voters are or are not pivotal) but prints no pivot probability, no formula for one, and no estimate. The first pass's claim that nothing quantitative about pivot probability is there stands.
NOTE: [stated] by the quotes. [inferred] For the site: nothing in this paper bears on a per-ballot probability in STV.

## 6. Referendums and ballot measures (including supermajority and quorum rules)

*First-pass lines 152-180 of `research/electoral-systems.md`. Each block: the first-pass claim with its line number, the mark, the source and location, exact quotes, the correction if any, notes.*

#### [D] D-01 | §6 | Supermajority pass condition Y >= q(Y+X) "wherever a source states it" (task item 7; first pass l.155 and l.169)
MARK: unread
SOURCE: none of the sources I could read states a supermajority pass condition of the form Y >= q(Y + X). I searched `herrera.txt`, `foellmi.txt`, `quorum_docx.txt`, `work-D/cirje_micro1204.txt`, `work-D/const_cc.txt` (grep "supermajorit", "qualified majority": no hit in any).
NOTE: What the sources do state instead, each as printed: (a) Herrera & Mattozzi Sec. 8 "Majority Quorum": the reform party needs a share of the whole electorate above a threshold m (their `P = Pr ((vR > m) ∩ (vR > vS ))`, p. 20; see FORMULAS). That is an approval-type threshold, not a share of the votes cast [inferred by me from the Sec. 8 set-up]. (b) Italian Constitution Art. 138: a constitutional law passed by two-thirds of the members of each Chamber in the second vote is not submitted to referendum (D-04). (c) Aguiar-Conraria docx: approval quorum 3 of 9 (A.2, A.3). The first pass's Gelman-type "p(threshold)/N" formula (l.155) is [inferred] by the first pass and no source I read states it for a threshold other than 50%. The orchestrating thread's re-run of Appendix A is the only thing behind the l.169-178 table.

#### [D] D-02 | §6 | Art. 75 English excerpt "at https://legislationline.org/taxonomy/term/12983" (l.156)
MARK: unread
SOURCE: https://legislationline.org/taxonomy/term/12983 (local: legislationline.html, `work-D/legislationline.txt`)
QUOTE[work-D/legislationline.txt]: "Page not found | OSCE Office for Democratic Institutions and Human Rights"
NOTE: The URL now returns an OSCE/ODIHR "Page not found" page (already noted in the task file). The first-pass quotations cannot be checked at that URL.

#### [D] D-03 | §6 | Art. 75 wording: "the majority of those with voting rights have voted" ... "a majority of votes validly cast has been reached" (l.156)
MARK: corrected
SOURCE: https://www.cortecostituzionale.it/documenti/download/pdf/Costituzione_italiana_english_version_ott2023.pdf (local: `work-D/const_cc.txt`); "CONSTITUTIONAL COURT OF THE ITALIAN REPUBLIC, Constitution of the Italian Republic", Art. 75, fourth paragraph; the file's name says Oct 2023. This is the Constitutional Court's own English text, not the senato.it text the task suggests (senato.it is WAF-challenged).
QUOTE[work-D/const_cc.txt]: "The proposal subjected to a referendum shall be approved if the majority of those eligible have participated in the vote and if it has received a majority of valid votes."
QUOTE[work-D/const_cc.txt]: "All citizens eligible to vote for the Chamber of Deputies shall have the right to participate in referendum."
CORRECTION: "the majority of those with voting rights have voted" / "a majority of votes validly cast has been reached" -> "the majority of those eligible have participated in the vote" / "a majority of valid votes" (this translation). The two phrases the first pass put in quotation marks are from another translation (legislationline's), which I could not read; they are not in the official English text I read. The meaning is the same: two conditions, a turnout over half the eligible and a majority of valid votes.
NOTE: Art. 75 covers abrogative referendums only. Constitutional referendums (Art. 138) carry no turnout condition: the Ministry's 2026 dossier says so (D-04, F-3).

#### [D] D-04 | §6 | "A voter can then be pivotal for the quorum, not only the majority" and "Approval quorum: not read in any source other than as a lab treatment" (l.156-157)
MARK: corrected
SOURCE: https://dait.interno.gov.it/documenti/dossier-referendum-2026.pdf (local: `work-D/dossier_ref2026.txt`), Ministry of the Interior (DAIT, Direzione centrale per i servizi elettorali), "marzo 2026 rev. 1.2"; Herrera & Mattozzi (`herrera.txt`, p. 2 and Sec. 8); https://ideas.repec.org/p/cor/louvrp/2666.html (`work-D/ideas_mm.txt`)
QUOTE[work-D/dossier_ref2026.txt]: "Per l’approvazione della richiesta referendaria sono necessari due quorum:"
QUOTE[work-D/dossier_ref2026.txt]: "uno, relativo alla partecipazione alla votazione della maggioranza degli aventi diritto al voto;"
QUOTE[work-D/dossier_ref2026.txt]: "Per la validità della consultazione non è necessario raggiungere il quorum della maggioranza degli aventi diritto al voto (50%+1);"
QUOTE[work-D/dossier_ref2026.txt]: "Il referendum non si svolge se la legge viene approvata con la maggioranza dei due terzi."
QUOTE[herrera.txt]: "the reform party must have the majority and at list a certain turnout in order for the referendum to pass"
QUOTE[work-D/ideas_mm.txt]: "using an approval quorum, i.e. a threshold on the number of voters expressing a ballot in favor of the reform below which the status quo is kept"
QUOTE[work-D/ideas_mm.txt]: "Note: In : Social Choice and Welfare, 45, 2015, p. 1-27"
QUOTE[work-D/dossier_ref2025.txt]: "procede alla verifica del quorum dei votanti per ogni singolo referendum"
CORRECTION: "Approval quorum ... not read in any source other than as a lab treatment" -> approval-type thresholds are described in three further places: Herrera & Mattozzi's "majority quorum" (intro p. 2 and Sec. 8), Maniquet & Morelli's definition (IDEAS abstract of "Approval quorums dominate participation quorums", whose IDEAS page notes "In : Social Choice and Welfare, 45, 2015, p. 1-27"; abstract only, formulas not read), and Aguiar-Conraria's docx (approval quorum of 3 of 9). What I did not find is a country that uses a pure approval quorum under that name: Herrera's intro lists Germany (25%), Scotland (40%), Sweden, Belarus, Latvia (50%) as "majority quorum" countries (his list, from 2006, not verified).
NOTE: The "pivotal for the quorum" idea is stated in the docx (D-10). The Italian Interior Ministry dossier gives the rule as two conditions (turnout of a majority of the electors; majority of valid votes) and says the first is checked by the central office at the Court of Cassation.

#### [D] D-05 | §6 | Aguiar-Conraria, Magalhaes & Vanberg: title, "NIPE WP 14/2013", URL `https://core.ac.uk/download/55624987.pdf` (l.160); which version
MARK: confirmed (title and working-paper number); unread (the PDF at the first-pass URL)
SOURCE: https://ideas.repec.org/p/nip/nipewp/14-2013.html (local: `work-D/ideas_nipe.txt`); https://ideas.repec.org/a/kap/expeco/v19y2016i4d10.1007_s10683-015-9473-9.html (local: `work-D/ideas_expeco.txt`)
QUOTE[work-D/ideas_nipe.txt]: "NIPE Working Papers 14/2013, NIPE - Universidade do Minho."
QUOTE[work-D/ideas_nipe.txt]: "File URL: http://www3.eeg.uminho.pt/economia/nipe/docs/2013/NIPE_WP_14_2013.pdf Download Restriction: no"
QUOTE[work-D/ideas_nipe.txt]: "Experimental Economics , Springer;Economic Science Association, vol. 19(4), pages 886-909, December."
QUOTE[work-D/ideas_expeco.txt]: "DOI: 10.1007/s10683-015-9473-9"
QUOTE[work-D/ideas_nipe.txt]: "We show that quora lead to overall decreases in participation rates, dramatically increasing the likelihood of full-fledged electoral boycotts on the part of status quo supporters."
QUOTE[work-D/ideas_expeco.txt]: "This discouraging effect is significantly larger under a participation quorum than under an approval quorum."
NOTE: Version read: neither full text. I read the working-paper abstract (IDEAS) and the journal-version abstract (IDEAS, Experimental Economics 19(4), Dec 2016). Not "Journal of Public Economics". The two abstracts differ: the 2013 abstract says "quora" decrease participation; the 2016 abstract separates a participation quorum from an approval quorum and says both lower participation, more under a participation quorum. The first pass cites the working paper (2013); the numbers it quotes (53.8, 39.9, 47.0, "more than 40", "57 to 70") may differ between the two versions: unread. A further paper by the same three authors, "What are the best quorum rules? A laboratory Investigation" (University of Heidelberg Department of Economics Working Paper 0671, 2019; https://ideas.repec.org/p/awi/wpaper/0671.html, `work-D/ideas_awi.txt`) "Guided by a pivotal voter model" tests participation, approval and a "rejection quorum"; abstract only (the PDF is behind Anubis).

#### [D] D-06 | §6 | Lab model: 9 electors, binary choice, majority rule, voting costs c_i uniform on [0,c] (l.160)
MARK: corrected (the support of the cost distribution)
SOURCE: `quorum_docx.txt` (Appendix 1 and Appendix 3 of the online resource)
QUOTE[quorum_docx.txt]: "Assume also that there are 9 electors i=1,…,9 and that each faces a cost of voting given by ci, where ci is the realization of a uniformly distributed random variable, ci ~ U0,100."
QUOTE[quorum_docx.txt]: "Your voting costs lie between 0 and 100 points."
QUOTE[quorum_docx.txt]: "In principle: The option which receives the most votes is chosen. In case of a tie, a random choice is made (50/50)."
QUOTE[quorum_docx.txt]: "The experiment consists of 48 rounds, each of which is independent of the others."
CORRECTION: "uniform on [0,c]" -> uniform on [0,100] (the docx writes "U0,100" after flattening; A.1 uses the ratio γ/c, so c = 100). Points, with 1 point = 0.05 EUR (Appendix 3, Screen 1). Also, the same electors' types are random: each draws a ball "A" or "B" with probability μ (A.1 uses μ; Appendix 3 Screen 3).
NOTE: Participation quorum = 4 votes, approval quorum = 3 votes for the favoured option, per Appendix 1 ("the participation quorum of 4", "the approval quorum of 3"). Appendix 3 Screen 6: "This rule states that one of the two options (A or B) will be automatically chosen if fewer than 4 votes are cast [fewer than 3 votes are cast for the other option]."
QUOTE[quorum_docx.txt]: "This rule states that one of the two options (A or B) will be automatically chosen if fewer than 4 votes are cast [fewer than 3 votes are cast for the other option]."

#### [D] D-07 | §6 | Sec. 2 quote: "a supporter of Change is pivotal if her vote is necessary either to reach the majority of the votes or to meet the quorum." (l.160)
MARK: unread
SOURCE: main text of the paper not reachable (see section 0 item 1).
QUOTE[quorum_docx.txt]: "Consider the case of no quorum; a Supporter is pivotal if her vote is necessary either to break or to reach the tie."
QUOTE[quorum_docx.txt]: "Namely, it could be that her vote is decisive in reaching the quorum, in addition to reaching or breaking a tie in case the quorum is met."
NOTE: The two quotes above are the appendix's own wording of the same idea; they are not the first pass's Sec. 2 sentence. The Sec. 2 sentence itself is unread.

#### [D] D-08 | §6 | Opponents' pivotal event "has two conflicting forms"; "She may be pivotal, in a desirable way ..."; "Under participation quora, Opponents may actually hurt themselves by voting." (l.160)
MARK: unread (the three quoted sentences); confirmed in substance by the appendix
SOURCE: main text unreachable. Substance: `quorum_docx.txt` Appendix 1.
QUOTE[quorum_docx.txt]: "For an Opponent, this means that she may be pivotal in an undesirable way: if her vote is decisive to meet the quorum and a majority votes in support of change, then her vote actually causes “Change” to win."
QUOTE[quorum_docx.txt]: "Thus, the AQ rule effectively eliminates the possibility to be pivotal in an undesirable way."
QUOTE[quorum_docx.txt]: "Note that in the participation quorum case, an Opponent may be pivotal in an undesirable way if her vote is decisive to meet the quorum, hence the negative signs in the second equation."

#### [D] D-09 | §6 | Appendix 1 Supporter, participation quorum: [ sum_{v=2..4} rho(v,v)/2 + sum_{v=1..3} rho(v+1,v)/2 + rho(1,2) + rho(0,3) ] b = gamma_s (l.160)
MARK: confirmed
SOURCE: `quorum_docx.txt`, eq. (A.2), second line ("if PQ=4"); structure read from the OMML and `pandoc` LaTeX (`work-D/docxconv/quorum_pandoc.tex` lines 85-87); symbols from equation markup, not a page image.
QUOTE[quorum_docx.txt]: "v=24[ρv,v/2]+v=13[ρv+1,v/2]+ρ1,2+ρ0,3b=γs, if PQ=4"
NOTE: The first pass's sum limits (v=2..4 and v=1..3) match. The whole bracket is multiplied by b. The no-quorum and approval-quorum lines of A.2 are in FORMULAS AS PRINTED.

#### [D] D-10 | §6 | Appendix 1 Opponent, participation quorum: [ sum_{v=2..4} rho(v,v)/2 + sum_{v=2..3} rho(v+1,v)/2 - rho(1,2)/2 - rho(0,3) ] x = gamma_o; "negative terms are the self-harming pivotal case" (l.160)
MARK: confirmed (as printed); an internal inconsistency in the source is flagged
SOURCE: `quorum_docx.txt`, eq. (A.3), second line; OMML/pandoc as above.
QUOTE[quorum_docx.txt]: "v=24[ρv,v/2]+v=23[ρv+1,v/2]-[ρ1,2/2]-ρ0,3x=γo, if PQ=4"
QUOTE[quorum_docx.txt]: "Note that in the participation quorum case, an Opponent may be pivotal in an undesirable way if her vote is decisive to meet the quorum, hence the negative signs in the second equation."
NOTE (source's own inconsistency, [inferred] by me, not decided): the docx defines "ρvo,vs" as the probability of vo "No" and vs "Yes" votes among the others, so rho(v_o, v_s). Under that reading the opponent's no-quorum term in A.3 is rho(v, v+1) (No = v, Yes = v+1: her vote makes a tie), and the approval-quorum term is again rho(v, v+1). But the participation-quorum line prints rho(v+1, v) for v = 2..3 (No = v+1, Yes = v), the same order the Supporter's terms use. Either the PQ line has its indices swapped, or the event is different from the other two lines. The docx does not say. Also, A.1's left side is printed rho(v_s, v_o) (order swapped relative to the sentence that introduces rho(v_o, v_s)). Both are in the source as printed; I changed nothing.

#### [D] D-11 | §6 | "rho(v_o,v_s) the probability a voter attaches to the others' counts (v_o No, v_s Yes), b the supporters' benefit, x the opponents' benefit, gamma_s and gamma_o the cut-off costs" (l.160)
MARK: confirmed
SOURCE: `quorum_docx.txt`, Appendix 1, first paragraph.
QUOTE[quorum_docx.txt]: "Assume that if ‘Yes’ wins the election, Supporters obtain a benefit b. Opponents have a benefit of x."
QUOTE[quorum_docx.txt]: "Let γs and γo be those cutoff values for supporters of Change and Opponents, respectively."
QUOTE[quorum_docx.txt]: "Taking as given the strategies of the other players, let ρvo,vs be the probability that elector i attaches that, among the other electors, vo vote ‘No’ and vs vote ‘Yes’."
NOTE: "An elector will vote if the voting cost is below some threshold" (same paragraph): the cutoffs gamma_s, gamma_o are on the cost scale 0 to 100, so gamma_s = b x P(pivotal) is the indifference condition; the docx solves the two equations numerically ("we have two equations and two unknowns. We find the equilibria numerically").

#### [D] D-12 | §6 | "These are for the experiment's quorum design, with 9 electors, not for real referendums" (l.160)
MARK: confirmed
SOURCE: `quorum_docx.txt`
QUOTE[quorum_docx.txt]: "Next, consider the participation quorum of 4."
QUOTE[quorum_docx.txt]: "Finally, consider the approval quorum of 3."
QUOTE[quorum_docx.txt]: "Existence of solutions is not a problem, but there are no general uniqueness results."

#### [D] D-13 | §6 | Lab turnout 53.8% (+-4.0, 95% CI) no quorum; 39.9% (+-4.1) participation quorum; 47.0% (+-4.5) approval quorum (Sec. 4.1) (l.160)
MARK: unread
SOURCE: not reachable (section 0 item 1). The docx's Appendix 2 tables are equilibrium predictions (QRE), not these turnout rates; I searched it for 53.8, 39.9 and 47.0 (no hit).
NOTE: Version question: working paper (2013) versus Experimental Economics (2016); see D-05.

#### [D] D-14 | §6 / §10.3 item 8 (l.280) | Boycott effect of a participation quorum "more than 40 percentage points" (Introduction) versus "57 to 70" (Sec. 4.3 and 5)
MARK: unread
SOURCE: not reachable. IDEAS abstracts give no numbers (D-05).
NOTE: Cannot confirm or refute that the inconsistency exists in either version; the first pass itself took the numbers from a WebFetch extract.

#### [D] D-15 | §6 | Herrera & Mattozzi: title, "working paper (versions 2005-06)", URL (l.161)
MARK: confirmed; published version found
SOURCE: https://igier.unibocconi.eu/sites/default/files/media/attach/HerreraPAPER.pdf (local: `herrera.txt`, `herrera.raw.txt`, `herrera.out` = PDF, 40 pages, Acrobat Distiller date 15 May 2006); https://ideas.repec.org/a/kap/pubcho/v148y2011i3p491-503.html (`work-D/ideas_hizen.txt`, reference list)
QUOTE[herrera.txt]: "QUORUM AND TURNOUT IN REFERENDA"
QUOTE[herrera.txt]: "Date: First Version: June 27th 2005, This Version: 15th May 2006."
QUOTE[work-D/ideas_hizen.txt]: "Journal of the European Economic Association , MIT Press, vol. 8(4), pages 838-871, June."
NOTE: The PDF is the May 2006 version. A published version exists: Journal of the European Economic Association 8(4), 838-871, June 2010 (the IDEAS reference list on the Hizen & Shinmyo page says so; I did not read it). The statements below are about the May 2006 version only.

#### [D] D-16 | §6 | "The paper does not use the classic 'pivotal voter' concept" (l.161): the paper's sentence or the first pass's paraphrase?
MARK: corrected
SOURCE: `herrera.txt` and `herrera.raw.txt`: the strings "pivot" and "decisive" occur **zero** times in either file (`grep -c -i pivot` gives 0 and 0; `grep -i decisiv` no hit).
QUOTE[herrera.txt]: "Abstract. We provide a positive and normative analysis of ref- erenda with a quorum limit."
QUOTE[herrera.txt]: "Parties decide simultaneously how many campaign funds or eﬀort to spend to mobilize voters in order to win the referendum."
CORRECTION: the sentence in quotation marks is not in the paper. It is the extractor's (or the first pass's) paraphrase, and quote marks around it are wrong. What the paper does: a game between two parties who choose mobilisation spending; voters are a continuum of measure 1 with random cost c uniform on [0,1]; the "decisive event" is the joint event that reform's vote share beats the status quo's and turnout meets the quorum (D-17). The paper never models a single voter's probability of being pivotal.
NOTE: The "Models party mobilisation, not the individual pivotal voter" part of the first-pass sentence is a fair description [inferred by me from the Sec. 2 model, quote above]; only the quoted words are false as a quotation.

#### [D] D-17 | §6 | Herrera & Mattozzi decisive-event formula P = Pr(vR >= vS and vR + vS >= q) (l.161)
MARK: corrected (as printed it has a typesetting error; and P is not an individual-vote probability)
SOURCE: `herrera.txt` Sec. 2, p. 4; I looked at the rendered page (`work-D/herrera_p-04.png`, 130 dpi) and transcribed what is printed.
QUOTE[herrera.txt]: "P = Pr ((vR ≥ v)S , (vR + vS ≥ q))"
QUOTE[herrera.txt]: "P is the joint probability that the vote share of r is greater than the vote share of s and that the total turnout exceeds the quorum q."
CORRECTION: first-pass "Pr(vR >= vS and vR + vS >= q)" -> printed first line is `P = Pr((v_R ≥ v)_S , (v_R + v_S ≥ q))`: the first condition's subscript S is placed outside the bracket (`(v_R ≥ v)_S`), a typesetting slip for `v_R ≥ v_S`; the second condition `(v_R + v_S ≥ q)` is as the first pass has it. The paper's second line, which restates the first in terms of r̃, the random share of voters who support reform, is `P = Pr( r̃ ≥ ρ(S)/(ρ(R)+ρ(S)) , (ρ(R) − ρ(S)) r̃ ≥ q − ρ(S) )`. Definitions (same page): `v_R = r̃ ρ(R)`, `v_S = (1 − r̃) ρ(S)`; `Pr(ρ(R) > c) = ρ(R)`; `Q = (q − ρ(S))/(ρ(R) − ρ(S))`, `K = ρ(S)/(ρ(R) + ρ(S))`.
NOTE: In the paper, P is the probability, over the random reform-supporter share r̃, that **reform is approved**; "P is the joint probability that the vote share of r is greater than the vote share of s and that the total turnout exceeds the quorum q." Here v_R and v_S are vote counts as a share of the whole electorate (measure 1) and q is a quorum on turnout in that scale (q in [0,1]); it is the party's objective-function probability (payoffs πr = BP − R, πs = B(1 − P) − S), not "the probability that my vote is decisive". The first pass calls it "decisive event with a quorum"; the paper does not.

#### [D] D-18 | §6 | Italian referendum: "the status quo party got only 12% of the votes but the total turnout was only 26%" (Sec. 1, p. 2; year not read) (l.161)
MARK: confirmed (quote, section, page); year found
SOURCE: `herrera.txt`, Sec. 1, p. 2 (the page header reads "QUORUM AND TURNOUT IN REFERENDA 2" before the sentence); Italian Ministry of the Interior dossier (`work-D/dossier_ref2026.txt`, table 10.1)
QUOTE[herrera.txt]: "the status quo party got only 12% of the votes but the total turnout was only 26%."
QUOTE[herrera.txt]: "The quote on the front page refers to a referendum on Stem Cell research in Italy in June 2005."
QUOTE[work-D/dossier_ref2026.txt]: "12 e 13 giugno 2005 (abrogativi)"
QUOTE[work-D/dossier_ref2026.txt]: "ITALIA + ESTERO 25,66 88,03 11,97"
NOTE: The year is **June 2005** (the paper says so; the front-page epigraph is The Economist, Dec. 10th 2005, which says "Only 26% of the electorate turned out to vote"). The Ministry's table (columns "% Votanti, % Si, % No") gives for question 1 of 12-13 June 2005, Italy plus abroad, turnout 25.66%, Yes 88.03%, No 11.97%: the paper's "12%" is the No share of valid votes and its "26%" the turnout, on the first of the four questions [measured: 11.97 rounds to 12, 25.66 to 26]. Note the paper calls it a referendum "on Stem Cell research"; the Ministry's headings for the four 2005 questions are "Procreazione medicalmente assistita" (assisted reproduction) with limits on research on embryos in question 1. Nothing in the paper says the 12% is of valid votes or of electors; the Ministry table shows it is of valid votes. Turnout here is the share of electors (Italy + abroad) that voted.

#### [D] D-19 | §6 | Foellmi, Heim & Schmid: title, "online appendix, 16 June 2025", URL (l.162)
MARK: confirmed
SOURCE: https://static.cambridge.org/content/id/urn%3Acambridge.org%3Aid%3Aarticle%3AS2049847025100332/resource/name/S2049847025100332sup001.pdf (local: `foellmi.txt`, `foellmi.raw.txt`)
QUOTE[foellmi.txt]: "Voter Turnout and Selective Abstention in Concurrent Votes"
QUOTE[foellmi.txt]: "Reto Foellmi, Rino Heim, Lukas Schmid"
QUOTE[foellmi.txt]: "June 16, 2025"
NOTE: The first pass says "Swiss concurrent referendums". The appendix text never contains the words "Swiss" or "Switzerland" (grep: none); what it says is "federal vote from June 13, 2021, with five concurrent propositions" and "the Federal Chancellery"; "Swiss" is the first pass's [inferred] reading.

#### [D] D-20 | §6 | Foellmi et al.: quote that estimating the probability of being decisive is challenging (l.162)
MARK: confirmed
SOURCE: `foellmi.txt`, Sec. B.2 "Probability of Being Decisive", p. 7 of the appendix (the page number printed after the section's first paragraph is 7); `foellmi.raw.txt` has the same sentence.
QUOTE[foellmi.txt]: "A key parameter in the cost-benefit calculus presented in equation (1) is the probability of being decisive, denoted as 𝑝."
QUOTE[foellmi.txt]: "Empirically, it is challenging to directly estimate this parameter because we cannot observe how individuals perceive the closeness of the referendums in advance."
NOTE: The bracket "[the probability of being decisive]" in the first pass is the first pass's gloss; the sentence before it names p.

#### [D] D-21 | §6 | Foellmi et al.: coefficient on distance -0.020 (SE 0.008) without, -0.021 (SE 0.009) with voting-day fixed effects, 228 observations; "they use ex-post distance of the Yes share from 50% as a proxy" (l.162)
MARK: confirmed (numbers); corrected (what the regression is)
SOURCE: `foellmi.txt`, Table B.1 "Association Between Salience and Ex-Post Closeness of the Referendum", Sec. B.2 (appendix p. 7-8)
QUOTE[foellmi.txt]: "Table B.1: Association Between Salience and Ex-Post Closeness of the Referendum"
QUOTE[foellmi.txt]: "Distance −0.020∗∗∗ −0.021∗∗ (0.008) (0.009)"
QUOTE[foellmi.txt]: "Voting day FE No Yes Observations 228 228"
QUOTE[foellmi.txt]: "In this analysis, the dependent variable is the average individual salience for each proposition, while the explanatory variable represents the absolute difference between a proposition’s “yes” share"
QUOTE[foellmi.txt]: "and 50%, the threshold required to obtain a majority of the votes cast."
QUOTE[foellmi.txt]: "In both models, the standard errors are one-way clustered by voting day."
CORRECTION: "they use ex-post distance of the Yes share from 50% as a proxy [for p] (coefficient on distance ...)" -> the table regresses the **average individual salience of each proposition** (dependent variable) on the ex-post distance of the Yes share from 50% (explanatory variable); its purpose is to show that "the probability of being decisive is indeed captured within the individual salience measure". Distance is not itself the proxy used in the voting model; salience is. Significance: *** (p<0.01) in column (1), ** (p<0.05) in column (2). The unit of "Distance" (share or percentage points) is not stated in the appendix text I read.
QUOTE[foellmi.txt]: "This suggests that the probability of being decisive is indeed captured within the individual salience measure of the propositions."
NOTE: "No estimate of p itself" (the first pass): confirmed by D-20's sentence.

#### [D] D-22 | §6 | docx "The mathematics of the pivotal voter model with quorum requirements": "binary file the extractor could not open" (l.163, l.290)
MARK: confirmed (now read)
SOURCE: https://static.cambridge.org/content/id/urn%3Acambridge.org%3Aid%3Aarticle%3AS1386415716010267/resource/name/S1386415716010267sup001.docx, fetched by the orchestrating thread into `SP/r4/src/quorum_docx.out`; text `quorum_docx.txt`. Read in full by me.
QUOTE[quorum_docx.txt]: "Appendix 1 ― The mathematics of the pivotal voter model with quorum requirements"
NOTE: Contents: Appendix 1 (the equations, D-06 to D-12 and FORMULAS), Appendix 2 (QRE robustness tables for different λ; not first-pass material), Appendix 3 (lab instructions, in German on screen). The first pass's "I could not obtain the 'pivotal voter model' formulas for quorum from either" is now out of date for this source. Footnote 1 of the docx (read on the LibreOffice render of p. 1; it is not in the flattened text) says: "We refer the reader to Aguiar-Conraria and Magalhães (2010b) for a rigorous derivation of the model." The docx does not say which of the authors' two 2010 papers "2010b" is. The two are, per the IDEAS reference list on the Hizen & Shinmyo page, "How quorum rules distort referendum outcomes: Evidence from a pivotal voter model", European Journal of Political Economy 26(4) 541-557, December 2010, and "Referendum design, quorum rules and turnout", Public Choice 144(1) 63-81, July 2010; the first has "pivotal voter model" in its title [inferred to be the derivation]. Neither is read (NEED-FETCH item 9). (Hizen's draft labels them the other way round: 2010a = the EJPE paper, 2010b = the Public Choice paper.)

#### [D] D-23 | §6 | Hizen & Shinmyo (2011), "Imposing a turnout threshold in referendums", Public Choice 148(3) 491-503, "abstract not shown" (l.163)
MARK: confirmed (citation); unread (abstract and the formula)
SOURCE: https://ideas.repec.org/a/kap/pubcho/v148y2011i3p491-503.html (local: `work-D/ideas_hizen.txt`)
QUOTE[work-D/ideas_hizen.txt]: "Abstract No abstract is available for this item."
QUOTE[work-D/ideas_hizen.txt]: "Public Choice , Springer, vol. 148(3), pages 491-503, September."
QUOTE[work-D/ideas_hizen.txt]: "File URL: http://hdl.handle.net/10.1007/s11127-010-9670-1 Download Restriction: Access to full text is restricted to subscribers."
NOTE: IDEAS has no abstract and the full text is subscriber-only, so neither the abstract nor the paper's own pivotal formula is read. A different paper by Hizen alone, which says its model is "closely related to the model of Hizen and Shinmyo (2011)" and uses its pivot-probability set-up, is read in F-1 (it is not Hizen & Shinmyo itself).
QUOTE[work-D/cirje_micro1204.txt]: "Our model is closely related to the model of Hizen and Shinmyo (2011)."
QUOTE[work-D/cirje_micro1204.txt]: "show that imposing such a quorum requirement can induce strategic abstention which tries to spoil the outcome rather than going to the poll to lose the referendum"

#### [D] D-24 | §6 | "Published estimates. None found ... I did not read Mulligan & Hunter's paper itself, so I do not know whether it covers ballot measures" (l.165)
MARK: confirmed (none found in the sources I read); Mulligan & Hunter's scope now known from the abstract
SOURCE: https://ideas.repec.org/p/nbr/nberwo/8590.html (local: `work-D/ideas_mh.txt`), abstract only; see F-2 for my searches.
QUOTE[work-D/ideas_mh.txt]: "Empirical distributions of election margins are computing using data on U.S. Congressional and state legislator election returns."
NOTE: The abstract mentions Congressional and state legislative election returns only; it does not mention ballot measures or primaries. The paper (Public Choice 116(1-2) 31-54, July 2003 per IDEAS) itself is unread.

#### [D] D-25 | §6 | 2016 UK EU referendum: Leave 17,410,742 (51.89%), Remain 16,141,241 (48.11%), turnout 33,551,983 (72.15%), electorate 46,500,001 (l.167)
MARK: confirmed (as shown on electionpolling.co.uk, a secondary site); unread (at the Electoral Commission and the Parliament briefing)
SOURCE: https://www.electionpolling.co.uk/results/2016eu (local: `elpolling.html`, text `work-D/elpolling.txt`, read by curl). Official sources: https://www.electoralcommission.org.uk/... (403, Cloudflare "Just a moment"), https://commonslibrary.parliament.uk/research-briefings/cbp-7639/ (403, Cloudflare), https://researchbriefings.files.parliament.uk/documents/CBP-7639/CBP-7639.pdf (403): all unread, not circumvented.
QUOTE[work-D/elpolling.txt]: "Leave 17,410,742 51.89%"
QUOTE[work-D/elpolling.txt]: "Remain 16,141,241 48.11%"
QUOTE[work-D/elpolling.txt]: "Turnout 33,551,983 72.15%"
QUOTE[work-D/elpolling.txt]: "Electorate 46,500,001"
NOTE (a surprise, [measured]): Leave + Remain = 17,410,742 + 16,141,241 = 33,551,983, **exactly the figure the page labels "Turnout"**. So that figure is the number of valid votes for the two options, not necessarily the number of ballots cast; if any ballots were rejected, the true turnout count is larger. The page does not give rejected ballots, and I did not read an official source for them. The 72.15% is 33,551,983 / 46,500,001 [measured: 72.1548%]. The percentages are shares of valid votes [measured: 17,410,742 / 33,551,983 = 51.892%; 16,141,241 / 33,551,983 = 48.108%].

#### [D] D-26 | §6 | "Margin 1,269,501 votes [17,410,742 - 16,141,241], 3.78% of the votes cast [1,269,501 / 33,551,983 = 0.03784]" (l.167)
MARK: confirmed [measured]
SOURCE: arithmetic on the D-25 figures (`python3 -I`, shown below); the figures themselves come from electionpolling.co.uk only.
NOTE: 17,410,742 − 16,141,241 = 1,269,501; 1,269,501 / 33,551,983 = 0.0378368 (3.78%). The denominator is the valid-vote total (see D-25), so "of the votes cast" is "of valid votes"; as a share of the electorate 1,269,501 / 46,500,001 = 2.730% [measured]. Output of my check: `margin 1269501`, `margin/T 0.03783683962882313`, `margin/E 2.73010961870732`.

#### [D] D-27 | §6 / §10.3 item 11 (l.283) | "Brexit referendum counts come from a secondary site that does not name its source; the Electoral Commission page was not readable"
MARK: confirmed
SOURCE: `work-D/elpolling.txt` and `elpolling.html`: the page has the heading "Here are the results of the 2016 EU Referendum." and no source line (grep for "source", "Electoral Commission" in the page text and HTML: no hit). Electoral Commission: 403 Cloudflare by curl (this task) after a "client error" by WebFetch (first pass).
QUOTE[work-D/elpolling.txt]: "Here are the results of the 2016 EU Referendum."
NOTE: The page's national figures are also unverifiable by summing its counting-area rows: it lists only some counting areas per region (e.g. five London areas), not all.

#### [D] D-28 | §6 | l.178 arithmetic: "N about 3.4e7 ... Q roughly 7 to 8 divided by N, about 2e-7 ... 1.89 points ... factor exp(-0.76^2/2) = 0.75"; "0.6/0.4 = 1.5 and (2/3)/(1/3) = 2.0, as in the table"
MARK: confirmed [measured arithmetic only]
SOURCE: `python3 -I` on the numbers quoted in the first pass; the simulated Q values and the N x Q scaling are not mine to re-run (orchestrating thread).
NOTE: 33,551,983 = 3.36e7 (≈ 3.4e7). 7/3.4e7 = 2.06e-7, 8/3.4e7 = 2.35e-7, so "about 2e-7" holds. Leave 51.89% is 1.89 points from 50%; 1.89/2.5 = 0.756, exp(−0.756²/2) = 0.7514 (0.75). 0.6/0.4 = 1.5 and (2/3)/(1/3) = 2.0 exactly. The table's printed ratios: Q_no/Q_yes = 9.6e-4/6.4e-4 = 1.500, 1.1e-3/5.5e-4 = 2.000, 1.3e-4/9.0e-5 = 1.44, 3.8e-7/2.6e-7 = 1.46, 2.7e-5/1.4e-5 = 1.93, 2.3e-5/1.5e-5 = 1.53, 1.5e-8/7.8e-9 = 1.92, 1.8e-13/9e-14 = 2.00: consistent with t/(1−t) of 1.5 and 2 within the table's two-digit rounding. 7.8e-4 x 10,000 = 7.8 ("N x Q about 7.8" ✓).

---

#### [D] D-36 | §6 | l.154: "a vote is decisive if the other votes are tied or one apart" (two-outcome contest)
MARK: confirmed (as the definition used in the sources I read; the first pass's own [inferred] statement)
SOURCE: Gelman, King & Boscardin (1998), p. 3 (`gkb1998_columbia.raw.txt`); Aguiar-Conraria docx (`quorum_docx.txt`).
QUOTE[gkb1998_columbia.raw.txt]: "First, without your vote, your state's election outcome must be exactly tied or one vote away from a tie."
QUOTE[quorum_docx.txt]: "Consider the case of no quorum; a Supporter is pivotal if her vote is necessary either to break or to reach the tie."
NOTE [inferred by me]: Aguiar-Conraria's pivot probabilities (A.2, A.3) weight both the tie event rho(v,v) and the one-apart event by 1/2, consistent with Appendix 3's "In case of a tie, a random choice is made (50/50)"; the Gelman et al. eq. (3) has factors of 1/2 for a related reason ("a vote that causes the national election to be tied is only half as decisive as a vote that changes the election outcome", p. 3).
QUOTE[gkb1998_columbia.raw.txt]: "The factors of 1/2 arise because a vote that causes the national election to be tied is only half as decisive as a vote that changes the election outcome."

#### [D] D-37 | §6 | l.180: "a quorum adds a second pivot event whose probability depends on the turnout forecast (not computed; no readable formula)"
MARK: corrected (a readable formula now exists in two sources)
SOURCE: `quorum_docx.txt` eqs. (A.2), (A.3) (n = 9; participation quorum 4) and `work-D/cirje_micro1204.txt` pp. 5-6 (general m and r): see F-1 and FORMULAS 1 and 3. Neither is for a national electorate; Hizen's p_i, q_i and t_i are multinomial sums over the other voters' types and abstentions.
QUOTE[work-D/cirje_micro1204.txt]: "A vote for alternative i can"
NOTE: the "second pivot event" the first pass describes is the pair of terms rho(1,2) + rho(0,3) (Supporter) and −rho(1,2)/2 − rho(0,3) (Opponent) in A.2/A.3, and p_i and q_i in Hizen. The docx notes the Opponent's event is self-harming. I did not compute anything.

---

## 7. Primaries and multi-stage nominations

*First-pass lines 182-193 of `research/electoral-systems.md`. Each block: the first-pass claim with its line number, the mark, the source and location, exact quotes, the correction if any, notes.*

#### [D] D-29 | §7 | "no source I read gives a formula for primaries"; "Not found: a published estimate of the probability a vote is decisive in a primary ... I did not read any dataset of primary margins" (l.184, l.191)
MARK: confirmed (none found; but see F-2 and F-4 for what I did find)
SOURCE: searches listed under F-2; nothing in the sources I read (`work-D/cooper_munger.txt`, `work-D/bp_primaries.txt`, `work-D/ideas_mh.txt`) states a pivot probability for a primary.
NOTE: A dataset of primary results that is official and downloadable exists (F-4); no margin statistics were read other than one contest's CSV.

#### [D] D-30 | §7 | Gelman, King & Boscardin (1998), eq. 1: "Pr(your vote matters) = Pr(your vote is decisive in your state) x Pr(your state is decisive | your vote is decisive in your state)" (l.186)
MARK: corrected (one word in the second factor)
SOURCE: `gkb1998_columbia.txt`/`.raw.txt` = https://sites.stat.columbia.edu/gelman/research/published/decisive2.pdf, the Columbia copy, 9 pages, running head "Gelman, King, and Boscardin: Estimating Probability of Nonoccurring Events", "Journal of the American Statistical Association, March 1998"; eq. (1) is on p. 3 and I read it on the rendered page (`work-D/gkb_p-3.png`, 130 dpi). The first-pass URL, https://core.ac.uk/download/28933611.pdf, is a Cloudflare "Just a moment..." page (`gkb1998.html`): unread.
QUOTE[gkb1998_columbia.txt]: "Pr(your vote matters)"
QUOTE[gkb1998_columbia.txt]: "= Pr(your vote is decisive in your state)"
QUOTE[gkb1998_columbia.txt]: "x Pr(your state will be decisive"
QUOTE[gkb1998_columbia.raw.txt]: "Your presidential vote will be decisive if two conditions are satisfied."
CORRECTION: printed eq. (1) second factor: "Pr(your state **will be** decisive | your vote is decisive in your state)", not "Pr(your state **is** decisive | ...)". The words "is decisive" are what eq. (3) prints for the left side of its expansion of the same factor ("Pr(your state is decisive | your vote is decisive in your state)"). Same meaning, different tense; the first-pass quotation mixes the two. The vertical bar before "your vote is decisive in your state)" is on a separate line in the print.
NOTE: the second line of eq. (1) as printed begins with "×" in the page image; in the layout text the sign appears as "x".

#### [D] D-31 | §7 | "the extractor's formula for the first factor, approximately f_{v_i}(.5)/n_i, is a reconstruction" (l.186)
MARK: confirmed (the formula is as printed, eq. 2)
SOURCE: same, p. 3 page image: `Pr(your vote is decisive in your state) = Pr(n_i v_i = .5 n_i) = Pr(v_i = .5) ≈ f_{v_i}(.5)/n_i`, eq. (2), for n_i even; for n_i odd "Pr(n_i v_i = .5(n_i − 1)) = Pr(v_i = .5 − .5/n_i) ≈ f_{v_i}(.5)/n_i also, assuming that n_i is reasonably large." Here n_i is the number of voters in state i **excluding yourself** and v_i is the Democratic share of the two-party vote excluding your vote; f_{v_i} is the density of v_i under the forecast model.
QUOTE[gkb1998_columbia.raw.txt]: "Pr(your vote is decisive in your state) = Pr(nivi = .5ni) = Pr(vi = .5)"
NOTE: this answers the first-pass open question 10.3 item 1 only in part (the constant for the "random voting" form of Gelman-Katz-Bafumi is a different paper); eq. (2) here is a density divided by n_i, with the density evaluated at 0.5.

#### [D] D-32 | §7 | Cooper & Munger (2000), "The (Un)Predictability of Primaries with Many Candidates: Simulation Evidence", Public Choice 103(3-4) 337-355 (l.189)
MARK: confirmed (citation, 10,000 voters, ten random candidates, "lottery"); corrected (the "varied widely" quote)
SOURCE: https://ideas.repec.org/a/kap/pubcho/v103y2000i3-4p337-55.html (local: `cooper_munger.html`, `work-D/cooper_munger.txt`), abstract page only (the full text is "restricted to subscribers").
QUOTE[work-D/cooper_munger.txt]: "Cooper, Alexandra & Munger, Michael C, 2000."
QUOTE[work-D/cooper_munger.txt]: "Public Choice , Springer, vol. 103(3-4), pages 337-355, June."
QUOTE[work-D/cooper_munger.txt]: "This paper uses a simulation approach, assuming 10,000 voters who vote according to a naive, deterministic proximity rule, but who choose party affiliation probabilistically."
QUOTE[work-D/cooper_munger.txt]: "The voters of each party then must choose between two sets of ten randomly chosen candidates, in "closed" primaries."
QUOTE[work-D/cooper_munger.txt]: "In fact, the way we choose candidates may amount to a lottery."
QUOTE[work-D/cooper_munger.txt]: "the winner of the primary, or the party's nominee, varied as much as two standard deviations from the median partisan voter."
CORRECTION: first-pass "outcomes 'varied widely, by as much as two standard deviations from the median partisan voter'" -> the abstract says "the winner of the primary, or the party's nominee, varied as much as two standard deviations from the median partisan voter". The words "varied widely" and "by" are not in the abstract; the first pass's quotation marks enclose a paraphrase. The abstract also says "The key result of the simulations reported here is the complete unpredictability of the outcomes of a sequence of primaries".
NOTE: "It does not study pivotal voting": the abstract says nothing about pivotal voters or about the probability of a decisive vote [inferred by me from the abstract only]; the paper is unread. The abstract's voters follow "a naive, deterministic proximity rule" and the setting is a sequence of primaries followed by a general election "in which independent voters also participate".

#### [D] D-33 | §7 | Ballotpedia, "A look back at 2025 state primary election competitiveness", 2 July 2025: states, "51 primaries out of a possible 289 for the 185 total seats", 17.6%, 19.7% (2011-2023 average), incumbents contested 22.4%, open seats 5.9% (l.190)
MARK: confirmed (all five numbers and the states); one reading flagged
SOURCE: https://news.ballotpedia.org/2025/07/02/a-look-back-at-2025-state-primary-election-competitiveness/ (local: `ballotpedia_primaries.html`, text `work-D/bp_primaries.txt`, read by curl). By Nathan Maxwell, July 2, 2025.
QUOTE[work-D/bp_primaries.txt]: "Together, the three states held 51 primaries out of a possible 289 for the 185 total seats up for election."
QUOTE[work-D/bp_primaries.txt]: "The percentage of open seats in 2025 (5.9%) was lower than in any year since 2011, and the percentage of contested primaries was 17.6%, below the average of 19.7% from 2011 to 2023."
QUOTE[work-D/bp_primaries.txt]: "The percentage of incumbents contested was 22.4%, just above the average of 21.8% in the previous seven cycles."
QUOTE[work-D/bp_primaries.txt]: "Ballotpedia’s 2025 state primary election data included competitiveness and incumbency statistics from state legislative and state executive elections in three states — New Jersey, Virginia, and Wisconsin."
NOTE (reading, [inferred]): "open seats 5.9%" is **the share of seats that were open (no incumbent running)**, not the share of open-seat primaries that were contested. The first pass lists it beside the contested-primary percentages, which invites the second reading. 51/289 = 17.65% [measured: 0.17647], which the article prints as 17.6%. The denominator 289 is "possible" primaries (party primaries that could have been held), not the 185 seats; so "contested primaries 17.6%" is a share of primaries, and the first pass's step "the decisive-vote probability is zero for the majority of seats" mixes units (primaries versus seats) [inferred; the article does not give a seat-level share]. [inferred] The 185 seats therefore include state executive offices: the article's "Wisconsin held a non-partisan primary for superintendent of public instruction" and the NJ/VA lists show the 185 seats include state executive offices. "No incumbents lost in state executive primary elections, and three lost in state legislative primaries, all in New Jersey" (same page).

#### [D] D-34 | §7 | "No margin-of-victory or close-race statistics in the article" (l.190)
MARK: confirmed
SOURCE: `work-D/bp_primaries.txt`: the article has four short paragraphs plus "Additional reading: Primary election competitiveness in state government, 2025" (link target https://ballotpedia.org/Primary_election_competitiveness_in_state_government,_2025, from the file's HTML). No margin, "decided by", or "close" statistic appears (grep "margin|close": no hit).
NOTE: that linked Ballotpedia page is on `ballotpedia.org`, which is task F's host; I did not request it. It is a lead for F-4.

#### [D] D-35 | §7 | l.184 and l.193 structure claims (two-stage chain; "electability difference"; three structural differences)
MARK: unread (these are the first pass's own reasoning; no source is claimed)
NOTE: nothing to check against a source. The one source cited for the chain, Gelman-King-Boscardin eq. (1), is D-30. Section 6's [measured] table (l.169-178) is not mine to re-run, except the arithmetic in D-28.

#### [A] A-20 | §7 L186 | GKB 1998 eq. 1: "Pr(your vote matters) = Pr(your vote is decisive in your state) x Pr(your state is decisive | your vote is decisive in your state)" (cited at core.ac.uk/download/28933611.pdf; "[stated via WebFetch]") (L186; same formula L200)
MARK: confirmed (one word differs); read at the author's copy, not at core.ac.uk
SOURCE: https://sites.stat.columbia.edu/gelman/research/published/decisive2.pdf (local: gkb1998_columbia.raw.txt) ; Sec. 3.1, eq. (1), printed p. 3 (page image PDF p. 3). Author's PDF of the JASA pages (running head "Journal of the American Statistical Association, March 1998, Vol. 93, No. 441"); journal version, not a preprint.
QUOTE[gkb1998_columbia.raw.txt]: "Pr(your vote matters)"
QUOTE[gkb1998_columbia.raw.txt]: "= Pr(your vote is decisive in your state)"
QUOTE[gkb1998_columbia.raw.txt]: "x Pr(your state will be decisive"
CORRECTION (wording): "Pr(your state is decisive | ...)" -> printed "Pr(your state **will be** decisive | your vote is decisive in your state)". As printed (image), eq. (1): Pr(your vote matters) = Pr(your vote is decisive in your state) × Pr(your state will be decisive | your vote is decisive in your state).
NOTE: Definitions as printed (Sec. 3.1, p. 3): "n_i = number of voters in state i (excluding yourself)", "v_i = Democratic share of the two-party vote in state i (excluding your vote)", e_i electoral votes, e_total = Σ e_i = 538, E_{-i} = Σ_{j≠i} e_j V_j + 3 (the 49 other states plus DC's 3 votes assumed Democratic). The text: "The second factor on the right side of (1) is a conditional probability: the probability that state i will be decisive, given a popular vote tie in that state." The two-stage structure (state tie, then state pivotal in the national total) is as the first pass says.

## 8. Chamber control (a seat, then the majority)

*First-pass lines 195-223 of `research/electoral-systems.md`. Each block: the first-pass claim with its line number, the mark, the source and location, exact quotes, the correction if any, notes.*

#### [A] A-21 | §8 L200 | GKB 1998: first factor, for even n_i, ≈ f_{v_i}(.5)/n_i (f the forecast density of the vote share); second factor Pr(E_{-i} in (.5 e_total − e_i, .5 e_total) | v_i = .5) with a factor 1/2 because a vote that ties the national election is half as decisive (L200; extractor's formula "a reconstruction" L186)
MARK: confirmed; the formulas are now read as printed
SOURCE: https://sites.stat.columbia.edu/gelman/research/published/decisive2.pdf (local: gkb1998_columbia.raw.txt) ; Sec. 3.1, eqs. (2) and (3), printed p. 3 (page image PDF p. 3)
QUOTE[gkb1998_columbia.raw.txt]: "outcome must be exactly tied or one vote away from a tie."
QUOTE[gkb1998_columbia.raw.txt]: "using the discrete approximation to the continuous distribution and the notation fvt for the probability density function"
QUOTE[gkb1998_columbia.raw.txt]: "(The factors of 1/2 arise because a vote that causes the"
QUOTE[gkb1998_columbia.raw.txt]: "national election to be tied is only half as decisive as a"
CORRECTION (exact formulas, from the image): 
  Eq. (2): Pr(your vote is decisive in your state) = Pr(n_i v_i = .5 n_i) = Pr(v_i = .5) ≈ f_{v_i}(.5)/n_i  [if n_i is even]; "Similarly, if n_i is odd, then the first factor in (1) is Pr(n_i v_i = .5(n_i − 1)) = Pr(v_i = .5 − .5/n_i) ≈ f_{v_i}(.5)/n_i also, assuming that n_i is reasonably large."
  Eq. (3): Pr(your state is decisive | your vote is decisive in your state) = Pr(E_{-i} ∈ (.5 e_total − e_i, .5 e_total) | v_i = .5) + (1/2) Pr(E_{-i} = .5 e_total − e_i | v_i = .5) + (1/2) Pr(E_{-1} = .5 e_total | v_i = .5).   (The last term is printed with subscript "-1", a typographical slip for "-i".)
  So the first-pass line "Pr(E_{P_i} in (...))" had the subscript garbled (E_{-i}); the 1/2 factors multiply the two *boundary* terms (a tie in the national electoral-vote count), not the whole expression.
NOTE: [stated, p. 3] "Your presidential vote will be decisive if two conditions are satisfied. First, without your vote, your state's election outcome must be exactly tied or one vote away from a tie. (We consider the case of a person who will either vote for one candidate or not vote. A voter who is considering switching from the Democratic to Republican candidate will, of course, have a higher probability of being decisive.)" (the text layer drops the word "or"). So GKB 1998's comparison is vote versus no vote, but its eq. (2) is the full probability f(.5)/n_i of the tie (or one-vote gap) among the others, with weight 1; see A-26 for what that implies for the constant.

#### [A] A-22 | §8 L201 | GKB 2004: two-factor decomposition (Sec. 2.2); second factor ("Factor 1") roughly proportional to e_j; the linear approximation "has a relative error of less than 10 per cent for all states" (Sec. 2.2.1) (L201)
MARK: confirmed, with a qualification the first pass omits (the 10 per cent is for random voting)
SOURCE: https://sites.stat.columbia.edu/gelman/research/published/gelmankatzbafumi.pdf (local: gkb2004.raw.txt) ; Sec. 2.2 and 2.2.1, printed pp. 661-662
QUOTE[gkb2004.raw.txt]: "individual voting power ⫽ Pr (jurisdiction j’s ej electoral votes are decisive) ⫻"
QUOTE[gkb2004.raw.txt]: "further assumption is made that ej is small compared to the uncertainty in E ⫺ j, then Pr"
QUOTE[gkb2004.raw.txt]: "(jurisdiction j’s ej electoral votes are decisive) will be approximately proportional to ej."
QUOTE[gkb2004.raw.txt]: "decisive) for each state assuming random voting and compare to the linear approximation"
QUOTE[gkb2004.raw.txt]: "we suggest. The linear fit has a relative error of less than 10 per cent for all states."
NOTE: the paper writes the decomposition as "individual voting power = Pr(jurisdiction j's e_j electoral votes are decisive) × Pr(a given vote is decisive in jurisdiction j | jurisdiction j's e_j electoral votes are decisive)" (Sec. 2.2; "Factor 1" × "Factor 2"). Proportionality to e_j holds only "if ... e_j is small compared to the uncertainty in E_{-j}". The "<10 per cent" comparison is between the linear approximation and the directly calculated Pr(jurisdiction j's e_j votes are decisive) "assuming random voting" for the Electoral College's e_j (3 to 54, total 538) and each of the 50 states plus DC. It is not a test against forecast-based probabilities, and it is only for Factor 1. Under random voting the two factors are "independent" (Sec. 2.2: "Under the random voting model, the two events, (1) and (2), are independent"). The Sec. 2.2 equation (1) as printed: Pr(j's e_j votes decisive) = Pr(E_{-j} ∈ (0.5E − e_j, 0.5E)) + (1/2)Pr(E_{-j} = 0.5E − e_j) + (1/2)Pr(E_{-j} = 0.5E).

#### [A] A-23 | §8 L201 | Banzhaf index: probability a vote is decisive when everyone votes 50-50 (Sec. 2.1) (L201)
MARK: confirmed
SOURCE: https://sites.stat.columbia.edu/gelman/research/published/gelmankatzbafumi.pdf (local: gkb2004.raw.txt) ; Sec. 2.1, printed p. 660
QUOTE[gkb2004.raw.txt]: "of campaigning efforts, and comparisons of voting power.13 Perhaps the simplest measure"
QUOTE[gkb2004.raw.txt]: "Under the random voting model, a voter is assumed to be equally likely to choose any of the"
NOTE: the full sentence (p. 660): "Perhaps the simplest measure of decisiveness is the (absolute) Banzhaf index, which is the probability that an individual vote is decisive under the assumption that all voters are deciding their votes independently and at random, with probabilities 0.5 for each of two parties." So "everyone votes 50-50" is "independently and at random, with probabilities 0.5 for each of two parties".

#### [A] A-24 | §8 L201 | GKB 2004 empirical result (Sec. 4, Fig. 3): fitted exponents "all closer to 0 than to" -0.5; decisive probability ~ n^-0.9 (signs lost in extraction); random voting "overestimates the probability of close elections in larger jurisdictions" (L201)
MARK: confirmed; signs and values now read from the figure images
SOURCE: https://sites.stat.columbia.edu/gelman/research/published/gelmankatzbafumi.pdf (local: gkb2004.raw.txt) ; abstract p. 657; Sec. 3.1 (Fig. 1) p. 666; Sec. 4 and Fig. 3, pp. 666-669 (Fig. 3 on p. 668, read from a 300 dpi render, rotated); Sec. 5.1 p. 670; Sec. 6.4 p. 673
QUOTE[gkb2004.raw.txt]: "find that the probability of a decisive vote is approximately proportional to 1/n. The random voting model (and,"
QUOTE[gkb2004.raw.txt]: "more generally, the square-root rule) overestimates the probability of close elections in larger jurisdictions."
QUOTE[gkb2004.raw.txt]: "are all closer to 0 than to ⫺ 0.5, which would correspond to"
QUOTE[gkb2004.raw.txt]: "could be said that they decline slightly with n, perhaps proportional to nj⫺ 0.1. This implies"
QUOTE[gkb2004.raw.txt]: "that the probability of a decisive vote is proportional to nj⫺ 0.9, which is far closer to 1/n"
QUOTE[gkb2004.raw.txt]: "examined in this paper are roughly consistent with a power law with an exponent of"
QUOTE[gkb2004.raw.txt]: "was ⫺ 0.494, essentially equal to a theoretical value of ⫺ 0.5."
NOTE (what is fitted, as printed): "we fit a curve of the form y = c n_j^α" (to the *proportional vote differential* |v_j − 0.5|, with n_j = total vote for the two leading candidates); α = −0.5 is the random-voting value. The probability of a decisive vote is p_v(0.5)/n, and p_v(0.5) scales as 1/(spread of v) ~ n^{−α}, so Pr(decisive) ∝ n^{−(1+α)}, which is why α ≈ −0.1 is read as n^−0.9 (Sec. 4). Values printed in the figures (read on the page images; the text layer has no values): 
  Fig. 1 (US presidential, state votes, 1960-2000): α = −0.16 (also in the text of Sec. 3.1: "the best-fitting  is ⫺ 0.16, which is much closer to 0 than to ⫺ 0.5"). 
  Fig. 3 panels: US state house elections α = 0.08; US state senate elections α = 0.06; US Congressional elections α = −0.11; US Senate elections α = −0.23; US statewide offices α = −0.01; European national elections α = −0.07. (Each panel also shows the lowess fit and the α = −0.5 curve.) The caption lists five systems (a)-(e), "lower houses of US state legislatures ... US state senates ... US House ... US Senate ... European national elections"; the figure has a sixth panel "US statewide offices" not in the caption. 
  Fig. 4 (simulation, districts permuted at random into 'states'): "the best-fit power  was ⫺ 0.494".
  So two of the six Fig. 3 exponents are printed as *positive* (0.08, 0.06) and four negative (−0.11, −0.23, −0.01, −0.07); "all closer to 0 than to −0.5" is true of each of them (the US Senate −0.23 is the farthest from 0). [inferred, using the paper's own relation Pr ∝ n^{−(1+α)}] the implied decisive-probability exponents are about −1.08, −1.06, −0.89, −0.77, −0.99, −0.93 for the six panels and −0.84 for Fig. 1; the paper itself states only "roughly n^−0.9".
  Sec. 6.4 as printed says that the empirical analyses are roughly consistent with a probability of decisive vote proportional to n_j to the power −0.1 (the Sec. 4 text says the *vote differential* goes as n^−0.1 and the decisive probability as n^−0.9; Sec. 6.4 then says this implies electoral votes in proportion to the 0.9th power of the number of voters; the "−0.1" in Sec. 6.4 is a slip in the paper, [inferred]).
  Also printed: Sec. 4 data rule: "We have excluded as uncontested any election in which the losing party received less than 10 per cent of the vote."; the empirical statements refer to the proportional vote *differential*, not directly to a measured pivot probability.

#### [A] A-25 | §8 L205 | GKB 1998 figures (six sub-claims; the first pass gives them all as "(Sec. 6.1)") (L205)
MARK: confirmed as figures; **corrected as to sections** (see each sub-block)

##### A-25a | "about 1 in 10 million for a close national election such as 1992"
MARK: confirmed
SOURCE: https://sites.stat.columbia.edu/gelman/research/published/decisive2.pdf (local: gkb1998_columbia.raw.txt) ; Abstract (p. 1); Sec. 4.3, printed p. 5 (Fig. 2 discussion); Sec. 6.1, p. 6
QUOTE[gkb1998_columbia.raw.txt]: "decisive as about 1 in 10 million for close national elections such as 1992, varying by about a factor of 10 among states. Our"
QUOTE[gkb1998_columbia.raw.txt]: "The probability is about 1 in 10 million"
QUOTE[gkb1998_columbia.raw.txt]: "of magnitude 1 in 10 million, rising to as much as about 1"
CORRECTION: section "6.1" -> abstract, Sec. 4.3 (p. 5: "Figure 2 displays for the 1992 election ... The probability is about 1 in 10 million" for all states) and Sec. 6.1 (p. 6: "typically of order of magnitude 1 in 10 million"). It is a *prospective estimate* from a forecasting model, not a frequency.

##### A-25b | "1 in 3.5 million in Vermont"
MARK: confirmed; section corrected
SOURCE: https://sites.stat.columbia.edu/gelman/research/published/decisive2.pdf (local: gkb1998_columbia.raw.txt) ; Sec. 4.3, printed p. 5 (page image PDF p. 5)
QUOTE[gkb1998_columbia.raw.txt]: "erate states have a greater chance (e.g., 1 in 3.5 million in"
NOTE: the text layer interleaves the two columns; on the page image the sentence reads "Voters in some of the smaller politically moderate states have a greater chance (e.g., 1 in 3.5 million in Vermont), whereas those in more extreme states (e.g., Utah and Nebraska) have a lesser chance." This is the 1992 election (Fig. 2a). Not Sec. 6.1.

##### A-25c | "as high as about 1 in 1.5 million for some small states in close elections"
MARK: confirmed (Sec. 6.1 as the first pass says)
SOURCE: https://sites.stat.columbia.edu/gelman/research/published/decisive2.pdf (local: gkb1998_columbia.raw.txt) ; Sec. 6.1, printed p. 6 (image PDF p. 6)
QUOTE[gkb1998_columbia.raw.txt]: "of magnitude 1 in 10 million, rising to as much as about 1"
QUOTE[gkb1998_columbia.raw.txt]: "in 1.5 million for some small states in some close elections"
NOTE: printed with the examples "(e.g., Nevada in 1960 and Alaska in 1976)" and, in the same sentence, "less than 1 in 100 million for all states in landslide elections such as 1972" (Sec. 6.1).

##### A-25d | "on the order of 1 in hundreds of millions" in landslides
MARK: confirmed; section corrected
SOURCE: https://sites.stat.columbia.edu/gelman/research/published/decisive2.pdf (local: gkb1998_columbia.raw.txt) ; Sec. 4.3, printed p. 5
QUOTE[gkb1998_columbia.raw.txt]: "probability is much smaller, on the order of 1 in hundreds"
QUOTE[gkb1998_columbia.raw.txt]: "of millions for all of the states. This strong dependence of"
CORRECTION: section "6.1" -> Sec. 4.3 (p. 5, the 1964, 1972 and 1984 landslide elections); Sec. 6.1 says "less than 1 in 100 million for all states in landslide elections such as 1972". Sec. 4.3 adds: "Of course, the probabilities of decisive votes in the landslide elections are sensitive to the tail behavior of our forecasting model; we trust the qualitative findings, but would rely less strongly on the exact numerical results."

##### A-25e | "1 in 10,000 as an upper bound for a typical 200,000-voter congressional race"
MARK: confirmed; section corrected
SOURCE: https://sites.stat.columbia.edu/gelman/research/published/decisive2.pdf (local: gkb1998_columbia.raw.txt) ; Sec. 5, printed p. 6
QUOTE[gkb1998_columbia.raw.txt]: "A typical value of n for an election to the U.S. Congress"
QUOTE[gkb1998_columbia.raw.txt]: "is 200,000, which gives an upper bound of 1 in 10,000 of"
QUOTE[gkb1998_columbia.raw.txt]: "much less than our upper bound of 1/10,000, because most"
CORRECTION: section "6.1" -> Sec. 5 ("Approximate results for U.S. congressional and other elections"). The bound comes from the paper's generic formula (A-28): with forecast standard deviation τ no smaller than 2%, the probability of a tie is at most about 20/n; with n = 200,000 that is 1 in 10,000.

##### A-25f | "an empirical House frequency of about .5/20,597 per election"
MARK: confirmed; section corrected
SOURCE: https://sites.stat.columbia.edu/gelman/research/published/decisive2.pdf (local: gkb1998_columbia.raw.txt) ; Sec. 5, printed p. 6
QUOTE[gkb1998_columbia.raw.txt]: "about .5/20,597 that a single vote will be decisive in a randomly chosen U.S. House election."
NOTE: the text: "In the period 1900-1992, there were 20,597 U.S. House elections, out of which 6 were decided by fewer than 10 votes, 49 by fewer than 100 votes, 293 by fewer than 500 votes, and 585 by fewer than 1,000 votes. This suggests a frequency probability of about .5/20,597 that a single vote will be decisive in a randomly chosen U.S. House election. This number is of course much less than our upper bound of 1/10,000, because most of the elections were not close." (The text layer reads "19001992" for "1900-1992".) The paper does not show the arithmetic that leads from the counts to ".5/20,597".

#### [F] F-04 | §8 | 538: "The 218th seat is the tipping-point seat because it is the House's median seat by partisanship" (line 197)
MARK: confirmed
SOURCE: https://fivethirtyeight.com/features/house-tipping-point-districts/ via WebFetch only (local: work-F/webfetch_fte.txt) ; article titled by WebFetch "The 10 Districts Most Likely To Decide Control Of The House" (Nathaniel Rakich, FiveThirtyEight on ABC News)
QUOTE[work-F/webfetch_fte.txt]: ""The 218th seat is the tipping-point seat because it is the House's median seat by partisanship.""
QUOTE[work-F/webfetch_fte.txt]: ""Therefore, the party that wins the tipping-point seat, and every seat that is the same color behind it, has won the House.""
NOTE: [stated via WebFetch - one grade below a curl read; the quote could not be checked against a raw page, only against the extract.] Why curl did not work: the curl read of this URL did not reach the article: https://fivethirtyeight.com/features/house-tipping-point-districts/ answers HTTP 301 to https://abcnews.com/politics (FiveThirtyEight's site now redirects to ABC News), so the saved file txt/fte.html is the ABC News politics front page (canonical https://abcnews.com/politics), not the article. The article text was obtained only through WebFetch (a small model's extract, run 2026-11-07); its output is saved verbatim in work-F/webfetch_fte.txt. A Wayback copy (archive.org availability API lists a snapshot 20250911233850) was refused to curl (connection reset on web.archive.org) and blocked for WebFetch. The first pass's attribution (the article URL) is right; its title was not given, WebFetch gives it as "The 10 Districts Most Likely To Decide Control Of The House".

#### [F] F-05 | §8 | 538 forecast "as of Oct. 14", 40,000 simulations (line 197)
MARK: confirmed
SOURCE: same article via WebFetch only (local: work-F/webfetch_fte.txt) ; footnote 1 and the methods sentence
QUOTE[work-F/webfetch_fte.txt]: ""All numbers in this article are as of Oct. 14 at 10 a.m. Eastern." (footnote 1)"
QUOTE[work-F/webfetch_fte.txt]: ""The FiveThirtyEight model simulates the election 40,000 times.""
NOTE: [stated via WebFetch.] WebFetch said the publication date is "Not stated in the page content"; "Oct. 14" has no year in the quote. The year 2022 is the first pass's reading (the 2022 forecast; the CSV names "_2022"), consistent with the WebFetch extract's own "(2022)" remark, but the year itself is not in the quoted sentence.

#### [F] F-06 | §8 | 538: "Republicans have a 70-in-100 chance of taking control of the House" (line 197)
MARK: confirmed
SOURCE: same article via WebFetch only (local: work-F/webfetch_fte.txt)
QUOTE[work-F/webfetch_fte.txt]: ""Republicans have a 70-in-100 chance of taking control of the House" (excerpt; the full sentence exceeds 125 characters)"
NOTE: [stated via WebFetch.] The extract returned only a truncated excerpt of the sentence, so the exact full sentence (and what the "70-in-100" is attached to, e.g. the model version) was not seen.

#### [F] F-07 | §8 | 538 tipping-point probability column is in a CSV the first pass did not open (line 197)
MARK: unread
SOURCE: WebFetch of the article (work-F/webfetch_fte.txt) names the files; the mirror https://datahub.io/@rufuspollock/example-fivethirtyeight/election-forecasts-2022 (WebFetch, work-F/webfetch_datahub.txt) gives the data dictionary; the CSV itself was not read
QUOTE[work-F/webfetch_fte.txt]: "It refers only to the file "house_district_toplines_2022.csv" (House) and "senate_state_toplines_2022.csv" (Senate), which are downloadable from the "Model outputs" section at the bottom of the FiveThirtyEight forecast page. The tipping-point probabilities are in the "tipping" column."
QUOTE[work-F/webfetch_datahub.txt]: "**Is "tipping" a column?** Yes. The table lists "tipping," described as "Chance that this seat is the tipping point for control of the Senate.""
NOTE: UNREAD reasons: (1) https://projects.fivethirtyeight.com/2022-general-election-forecast-data/house_district_toplines_2022.csv answers 302 to https://abcnews.go.com/politics to curl, and WebFetch reports "robots_disallowed" (the URL is my guess of the usual path, not one the article gives); (2) github.com/fivethirtyeight/data returned 403 "GitHub access to this repository is not enabled for this session" (not circumvented; raw.githubusercontent.com guess returned 404); (3) datahub.io mirror page returned 404 to curl and its WebFetch extract gave the data dictionary only, no values. The data dictionary (via WebFetch, a mirror, not 538) lists a "tipping" column in house_district_toplines_2022.csv and describes it as the chance a seat is the tipping point "for control of the Senate" (the extract suspects a documentation carry-over from the Senate file). No district values were read.

#### [F] F-08 | §8 | Two stages in sequence (seat tie, then seat is the majority-maker); "The vote changes who controls the chamber only if both hold" (line 196)
MARK: confirmed
SOURCE: structure of the two-stage decomposition as printed in GKB 1998 Sec. 3.1 (local: gkb1998_columbia.raw.txt) and GKB 2004 Sec. 2.2 (local: gkb2004.raw.txt); for a legislature the second stage is the first-pass author's extension
QUOTE[gkb1998_columbia.raw.txt]: "Your presidential vote will be decisive if two conditions are satisfied. First, without your vote, your state's election outcome must be exactly tied or one vote away from a tie."
QUOTE[gkb1998_columbia.raw.txt]: "Second, your state must be decisive in the national election; given that it is tied, neither party must have an electoral vote majority."
NOTE: [inferred] The extension from the Electoral College to a legislature is the first pass's own and is not in a source read. What the sources print is the Electoral College case. [stated] for the EC.

#### [F] F-09 | §8 | Setup of the [measured] chamber table: 435 seats, 218 is a majority (lines 207, 197)
MARK: confirmed
SOURCE: https://ballotpedia.org/United_States_House_of_Representatives (local: work-F/bp_house.txt, tag-stripped) for 435; 538 sentence (work-F/webfetch_fte.txt) for the 218th seat
QUOTE[work-F/bp_house.txt]: "There are currently 435 representatives, a number fixed by law since 1911."
QUOTE[work-F/webfetch_fte.txt]: ""The 218th seat is the tipping-point seat because it is the House's median seat by partisanship.""
NOTE: 435: [stated] by Ballotpedia. That 218 is the majority of 435: neither Ballotpedia page read (the House page; the 2022 House elections page, work-F/bp_house22.txt) prints the number 218 as the majority threshold; it follows from 435/2 = 217.5 [measured: arithmetic] and is consistent with 538 calling the 218th seat the median seat (via WebFetch). 435 is odd, so with this seat decided the other 434 seats giving 217 to the party makes 218 for it; the chamber cannot tie (with all 435 seats filled). Vacancies change this (Ballotpedia shows 2 vacancies at present); not examined.

#### [F] F-10 | §8 | GKB 1998 two-stage decomposition: Pr(your vote matters) = Pr(decisive in your state) x Pr(your state is decisive | your vote is decisive in your state) (lines 186, 200)
MARK: confirmed
SOURCE: https://sites.stat.columbia.edu/gelman/research/published/decisive2.pdf (local: gkb1998_columbia.raw.txt; page image of PDF p.3, journal p.3 viewed at 170 dpi: work-F/gkb98p-3.png) ; Sec. 3.1 "Expression in Terms of Conditional and Marginal Probability", Eq. (1)
QUOTE[gkb1998_columbia.raw.txt]: "Pr(your vote matters)"
QUOTE[gkb1998_columbia.raw.txt]: "Pr(your vote is decisive in your state)"
QUOTE[gkb1998_columbia.raw.txt]: "The second factor on the right side of (1) is a conditional probability: the probability that state i will be decisive, given a popular vote tie in that state."
NOTE: Eq. (1) as printed (page image): Pr(your vote matters) = Pr(your vote is decisive in your state) x Pr(your state will be decisive | your vote is decisive in your state). The first pass wrote "is decisive" where (1) prints "will be decisive" (the same words appear as "is decisive" on the left side of Eq. (3)); no change of meaning. Section is 3.1. The first-pass "[stated via WebFetch]" tag can now be "[stated] read at source".

#### [F] F-11 | §8 | GKB 1998: first factor "for even n_i is approximately f_{v_i}(.5)/n_i (f the forecast density of the vote share)" (line 200; also line 186 "reconstruction")
MARK: confirmed
SOURCE: https://sites.stat.columbia.edu/gelman/research/published/decisive2.pdf (page image work-F/gkb98p-3.png) ; Sec. 3.1, Eq. (2) and the sentence after it
QUOTE[gkb1998_columbia.raw.txt]: "using the discrete approximation to the continuous distribution and the notation fvt for the probability density function for the continuous variable vi under the forecasting model."
QUOTE[gkb1998_columbia.raw.txt]: "Pr(nivi = .5(ni - 1)) = Pr(vi = .5 - .5/ni) KZ fvt (.5)/ni also, assuming that ni is reasonably large."
NOTE: From the page image, Eq. (2) is printed: Pr(your vote is decisive in your state) = Pr(n_i v_i = .5 n_i) = Pr(v_i = .5) approx f_{v_i}(.5)/n_i, for n_i even; for n_i odd: Pr(n_i v_i = .5(n_i - 1)) = Pr(v_i = .5 - .5/n_i) approx f_{v_i}(.5)/n_i, "assuming that n_i is reasonably large". So the first pass's reconstruction of the first factor is right, and it holds for odd n_i too (first pass said "for even n_i" only). Definitions printed: n_i = "number of voters in state i (excluding yourself)", v_i = "Democratic share of the two-party vote in state i (excluding your vote)". The raw text file garbles the symbols ("KZ" for the approximation sign); the page image was used.

#### [F] F-12 | §8 | GKB 1998: second factor is "Pr(E_{P_i} in (.5 e_total - e_i, .5 e_total) | v_i = .5), with a factor 1/2 because a vote that ties the national election is half as decisive" (line 200)
MARK: corrected
SOURCE: https://sites.stat.columbia.edu/gelman/research/published/decisive2.pdf (page image work-F/gkb98p-3.png, Eq. (3)) ; Sec. 3.1
QUOTE[gkb1998_columbia.raw.txt]: "(The factors of 1/2 arise because a vote that causes the national election to be tied is only half as decisive as a vote that changes the election outcome.)"
QUOTE[gkb1998_columbia.raw.txt]: "Pr(your state is decisive /your vote is decisive in your state) = Pr(EPi E (.5etOtal- ei, .5etotal)lvi = .5)"
CORRECTION: first pass: one factor Pr(E in (.5 e_total - e_i, .5 e_total) | v_i = .5) "with a factor 1/2" -> Eq. (3) as printed has THREE terms: Pr(E_{-i} in (.5 e_total - e_i, .5 e_total) | v_i = .5) + (1/2) Pr(E_{-i} = .5 e_total - e_i | v_i = .5) + (1/2) Pr(E_{-i} = .5 e_total | v_i = .5). The two factors of 1/2 weight the two exact-tie end points; the interval term has no 1/2. The symbol is E_{-i} (Democratic electoral votes in the 49 states excluding i, plus the District of Columbia, 3 votes counted for the Democrats), not "E_{P_i}"; in the last term the printed subscript reads "E_{-1}" (a typographical slip for E_{-i}).
NOTE: The raw text file garbles E_{-i} as "EPi"/"E-1"; the formula was read from the page image. The "1/2" claim of the first pass is therefore half right: the factor exists, but it multiplies the two tie terms, and the explanation is as quoted. Also in Sec. 5 the paper repeats: "(The factor of 1/2 applies because we are considering the effect of casting a vote, not the effect of switching a preference from one party to the other.)" (see F-25).

#### [F] F-13 | §8 | GKB 2004: "the same two-factor decomposition (Sec. 2.2)" (line 201)
MARK: confirmed
SOURCE: https://sites.stat.columbia.edu/gelman/research/published/gelmankatzbafumi.pdf (local: gkb2004.raw.txt; page images of PDF pp.6-7 = journal pp.662-663 viewed at 150 dpi: work-F/gkb04p-06.png, work-F/gkb04p-07.png) ; Sec. 2.2 "What Does the Random Voting Model Imply about Voting Power?"
QUOTE[gkb2004.raw.txt]: "For an individual in jurisdiction j, his or her vote is decisive if (a) the ej electoral votes of jurisdiction j are decisive in the larger election, and (b) the individual’s vote is decisive in the election within the jurisdiction."
QUOTE[gkb2004.raw.txt]: "Pr (jurisdiction j’s ej electoral votes are decisive) ⫽ Pr(E ⫺ j 苸 (0.5E ⫺ ej, 0.5E)) ⫹ 1 1 Pr(E ⫺ j ⫽ 0.5E ⫺ ej) ⫹ Pr(E ⫺ j ⫽ 0.5E) 2 2"
NOTE: The paper is Gelman, Katz & Bafumi, "Standard Voting Power Indexes Do Not Work: An Empirical Analysis", British Journal of Political Science 34 (2004) 657-674 (header of the PDF). [stated] Printed Eq. (1) has the same three-term form as GKB 1998 Eq. (3): the interval term plus 1/2 times each of the two end-point tie terms (the raw text puts the "1 1 ... 2 2" fractions out of order; the page image shows (1/2)Pr(E_{-j} = 0.5E - e_j) + (1/2)Pr(E_{-j} = 0.5E)). Eq. (2): Pr(a given vote is decisive in jurisdiction j) = p_{v_j}(0.5)/n_j. The paper assumes "n_j in any district is large enough - greater than 100, say" for the continuous approximation (relevant to very small electorates, section 9). The constant: my reading of the page image is in F-41, to be compared with the reading of task A.

#### [F] F-14 | §8 | GKB 2004: "the second factor is, per the extract, roughly proportional to e_j" (line 201)
MARK: corrected
SOURCE: https://sites.stat.columbia.edu/gelman/research/published/gelmankatzbafumi.pdf (local: gkb2004.raw.txt; page images of PDF pp.6-7 = journal pp.662-663 viewed at 150 dpi: work-F/gkb04p-06.png, work-F/gkb04p-07.png) ; Sec. 2.2.1 and Sec. 2.2.3
QUOTE[gkb2004.raw.txt]: "For the rest of this article we shall assume that Factor 1 is proportional to ej."
QUOTE[gkb2004.raw.txt]: "If the number of jurisdictions is large, however, with no single jurisdiction dominating, and no unusual patterns"
CORRECTION: "second factor ... roughly proportional to e_j" -> in GKB 2004 it is "Factor 1", the probability that the jurisdiction's electoral votes are decisive (written first in the product of Sec. 2.2); "Factor 2" is the within-jurisdiction probability, p_{v_j}(0.5)/n_j. The order of the two factors is the reverse of GKB 1998 (where the in-state factor is first and the "state decisive" factor second). The proportionality to e_j holds under random voting when "the number of jurisdictions is large ... no single jurisdiction dominating" and when e_j is small compared with the uncertainty in E_{-j} (Sec. 2.2.1).
NOTE: [stated] Sec. 2.2.1 ends: the paper "shall assume" Factor 1 proportional to e_j for the rest of the article and says computing it more precisely "does not affect the main point". Its own example (e_1..e_4) = (12, 9, 6, 2) shows the relation "far from linear" when the jurisdictions are few and lumpy: the fourth has zero power and the other three have equal power 1/2 (page 661-662).

#### [F] F-15 | §8 | GKB 2004: the linear approximation "has a relative error of less than 10 per cent for all states" (Sec. 2.2.1) (line 201)
MARK: confirmed
SOURCE: https://sites.stat.columbia.edu/gelman/research/published/gelmankatzbafumi.pdf (local: gkb2004.raw.txt; page images of PDF pp.6-7 = journal pp.662-663 viewed at 150 dpi: work-F/gkb04p-06.png, work-F/gkb04p-07.png) ; Sec. 2.2.1, journal p.662 (page image work-F/gkb04p-06.png)
QUOTE[gkb2004.raw.txt]: "The linear fit has a relative error of less than 10 per cent for all states."
QUOTE[gkb2004.raw.txt]: "In this case the values of ej for the fifty states and the District of Columbia range from 3 to 54, with a total of 538."
NOTE: [stated] The 10 per cent is for the random-voting calculation of Factor 1 for the 50 states and DC against a linear fit in e_j. The same sentence appears in GKT 2002 (Sec. 3.1, as "less than 10%").

#### [F] F-16 | §8 | GKB 2004: Banzhaf index = probability a vote is decisive when everyone votes 50-50 (Sec. 2.1) (line 201)
MARK: confirmed
SOURCE: https://sites.stat.columbia.edu/gelman/research/published/gelmankatzbafumi.pdf (local: gkb2004.raw.txt; page images of PDF pp.6-7 = journal pp.662-663 viewed at 150 dpi: work-F/gkb04p-06.png, work-F/gkb04p-07.png) ; Sec. 2.1 "Defining the Power of an Individual Voter"
QUOTE[gkb2004.raw.txt]: "Perhaps the simplest measure of decisiveness is the (absolute) Banzhaf index, which is the probability that an individual vote is decisive under the assumption that all voters are deciding their votes independently and at random, with probabilities 0.5 for each of two parties."
NOTE: [stated] The printed definition is "independently and at random, with probabilities 0.5 for each of two parties", which is a little more than "everyone votes 50-50" (independence is part of it). Sec. 2.1 also defines voting power as a difference: the power of a voter is "the probability that party A wins if that voter supports A, minus the probability that A wins if that voter supports B".

#### [F] F-17 | §8 | GKB 2004 empirical result: Sec. 4, Fig. 3; US state lower houses and senates, US House, US Senate, European national elections (line 201)
MARK: confirmed
SOURCE: https://sites.stat.columbia.edu/gelman/research/published/gelmankatzbafumi.pdf (local: gkb2004.raw.txt; page images of PDF pp.6-7 = journal pp.662-663 viewed at 150 dpi: work-F/gkb04p-06.png, work-F/gkb04p-07.png) ; Sec. 4 and Fig. 3 caption (journal p.668); text pp.667-669
QUOTE[gkb2004.raw.txt]: "Fig. 3. Proportional vote differential v. number of major-party voters nj, for contested elections in the following electoral systems: (a) lower houses of US state legislatures with single-member districts, 1984–90, (b) US state senates, 1984–90, (c) US House of Representatives, 1896–1992, (d) US Senate, 1988–96, (e) European national elections, 1950–98."
QUOTE[gkb2004.raw.txt]: "We have excluded as uncontested any election in which the losing party received less than 10 per cent of the vote."
NOTE: [stated] Years: state lower houses 1984-90, state senates 1984-90, US House 1896-1992, US Senate 1988-96, European national elections 1950-98 (not in the first pass). The Electoral College is Sec. 3 (Fig. 1: presidential states 1960-2000, best-fit exponent -0.16; Fig. 2: forecast-based probabilities 1952-92), separate from Sec. 4.

#### [F] F-18 | §8 | GKB 2004: fitted exponents "all closer to 0 than to" -0.5; decisive probability roughly proportional to 1/n (fits near n^-0.9) (line 201)
MARK: confirmed
SOURCE: https://sites.stat.columbia.edu/gelman/research/published/gelmankatzbafumi.pdf (local: gkb2004.raw.txt; page images of PDF pp.6-7 = journal pp.662-663 viewed at 150 dpi: work-F/gkb04p-06.png, work-F/gkb04p-07.png) ; Sec. 4, journal p.669 (text after Fig. 3); Sec. 3.1 for the presidential -0.16
QUOTE[gkb2004.raw.txt]: "In each case, the lowess line is much closer to horizontal than to 1/兹nj, and the best-fit parameters"
QUOTE[gkb2004.raw.txt]: "are all closer to 0 than to ⫺ 0.5, which would correspond to the square-root rule."
QUOTE[gkb2004.raw.txt]: "Or it could be said that they decline slightly with n, perhaps proportional to nj⫺ 0.1. This implies that the probability of a decisive vote is proportional to nj⫺ 0.9, which is far closer to 1/n as in the election forecasting literature than to 1/兹n as in the voting power literature."
QUOTE[gkb2004.raw.txt]: "does not systematically vary with nj As shown in Figure 1, the best-fitting"
QUOTE[gkb2004.raw.txt]: "0.16, which is much closer to 0 than to ⫺ 0.5."
NOTE: [stated] The sign the first pass could not read is printed: the exponent is -0.9 in "proportional to n_j^-0.9", and the vote-differential exponent is "perhaps ... n_j^-0.1" ("perhaps" and "slightly": a rough statement, not a fitted value for the decisive probability). The individual fitted exponents for the Fig. 3 panels are in the figure (not in the text); only "all closer to 0 than to -0.5" is printed. The presidential-state fit is -0.16 (GKT 2002 adds "standard error of 0.03"). The glyph for alpha is missing from the text layer (double space before "are" and "is").

#### [F] F-19 | §8 | GKB 2004: random voting "overestimates the probability of close elections in larger jurisdictions" (line 201)
MARK: confirmed
SOURCE: https://sites.stat.columbia.edu/gelman/research/published/gelmankatzbafumi.pdf (local: gkb2004.raw.txt; page images of PDF pp.6-7 = journal pp.662-663 viewed at 150 dpi: work-F/gkb04p-06.png, work-F/gkb04p-07.png) ; Abstract
QUOTE[gkb2004.raw.txt]: "The random voting model (and, more generally, the square-root rule) overestimates the probability of close elections in larger jurisdictions."
QUOTE[gkb2004.raw.txt]: "They find that the probability of a decisive vote is approximately proportional to 1/n."
NOTE: [stated] The abstract also says the square-root rule "implies that the probability of a vote being decisive in a jurisdiction with n voters is proportional to 1/兹n" (the sqrt sign is lost in the text layer).

#### [F] F-20 | §8 | GKT 2002: Statistical Science 17(4), Caltech working paper 1141, URL records/hpnm8-cmw66 (line 202)
MARK: corrected
SOURCE: https://authors.library.caltech.edu/records/hpnm8-cmw66 (local: gktuerlinckx.html; plain strip work-F/gktuerlinckx.plain.txt); PDF https://authors.library.caltech.edu/records/hpnm8-cmw66/files/sswp1141.pdf?download=1 (local: work-F/sswp1141.txt) cover page
QUOTE[work-F/gktuerlinckx.plain.txt]: "Published as Gelman, A., Katz, J.N., & Tuerlinckx, F. (2002). The mathematics and statistics of voting power. Statistical Science, 420-435."
QUOTE[work-F/gktuerlinckx.plain.txt]: "Series Volume or Issue Number 1141"
QUOTE[work-F/sswp1141.txt]: "SOCIAL SCIENCE WORKING PAPER 1141 October, 2002"
CORRECTION: "Statistical Science 17(4)" -> volume and issue are not printed on either source read; the Caltech page gives "Statistical Science, 420-435" (2002) and a related DOI 10.1214/ss/1049993201. Working paper 1141 is confirmed (October 2002).
NOTE: "17(4)" is UNREAD (not stated in the sources read; the journal page was not requested). The Caltech page lists the PDF as "Version Submitted" (the working paper, "Published October 2002"), so the PDF text is the preprint, not the journal text; journal pagination may differ.

#### [F] F-21 | §8 | GKT 2002 abstract: "voting power ... is the probability that a single vote is decisive"; discusses two-stage elections (line 202)
MARK: confirmed
SOURCE: https://authors.library.caltech.edu/records/hpnm8-cmw66 (local: work-F/gktuerlinckx.plain.txt) ; Abstract; same sentence in the PDF (work-F/sswp1141.txt)
QUOTE[work-F/gktuerlinckx.plain.txt]: "In an election, voting power—the probability that a single vote is decisive—is affected by the rule for aggregating votes into a single outcome."
QUOTE[work-F/gktuerlinckx.plain.txt]: "This simple model has interesting implications for weighted elections, two-stage elections (such as the U.S. Electoral College) and coalition structures."
NOTE: [stated] The first pass's "voting power ... is the probability that a single vote is decisive" is the abstract with the middle elided.

#### [F] F-22 | §8 | GKT 2002: body not read - definition of voting power and treatment of two-stage elections (lines 202, 10.3 context)
MARK: corrected
SOURCE: https://authors.library.caltech.edu/records/hpnm8-cmw66/files/sswp1141.pdf?download=1 (local: work-F/sswp1141.txt; 37 pages, text layer read for Sec. 2-4) ; Sec. 2.2 (Eq. 1), Sec. 3.2 (two-stage), Sec. 4.1 (Eq. 10-12)
QUOTE[work-F/sswp1141.txt]: "Voting power can and has been defined in a variety of ways (see Saari and Sieberg, 1999, and Heard and Swartz, 1999); in this paper we shall use the definition based on the probability that a vote affects the outcome of the election."
QUOTE[work-F/sswp1141.txt]: "poweri = Power of voter i = Pr(R = +1|vi = +1) − Pr(R = +1|vi = −1). (1)"
QUOTE[work-F/sswp1141.txt]: "In two-stage voting, one must first compute the voting power of each jurisdiction j and then the power of each of the nj voters within a jurisdiction."
QUOTE[work-F/sswp1141.txt]: "Under the simulation, the probability that a voter is decisive within state j is given by (10), which we evaluate from the normal density function. We then compute in two steps the probability that the state’s electoral votes are decisive for the nation."
CORRECTION: "I did not read the body" -> read. Definition as printed: power_i = Pr(R=+1 | v_i=+1) - Pr(R=+1 | v_i=-1) (Eq. 1), i.e. the difference between the vote being cast for each side (not versus abstaining); the abstract's "probability that a single vote is decisive" is the same quantity under that definition. Two-stage: Sec. 3.2 computes, under random voting, the within-jurisdiction probability as Pr(V_{-i}=0) + (1/2)Pr(|V_{-i}|=1) = C(n_j - 1, (n_j - 1)/2) for n_j odd and C(n_j - 1, n_j/2) for n_j even as printed in the page image (without the 2^-(n_j - 1) factor that a probability needs: a typographical omission [inferred]), approximated by sqrt(2/(pi n_j)) and the whole-voter power as approx w_j / sqrt(n_j) (Eq. 6); Sec. 4.1 replaces random voting by Pr(vote decisive within district j) approx f_j(0)/n_j (Eq. 10), then computes, in two steps, the probability the state's votes are decisive nationally (conditioning the national/regional errors on V_j = 0, simulating the other states).
NOTE: Printed ties convention: "We assume that tied elections at all levels are decided by coin flips" (Sec. 2.1). Eq. (4): Pr(tie election) approx f_V(0)/n. The paper states it restricts itself to "weighted majority voting in two-party systems" and does "not discuss" "legislative elections with committees, multiple chambers, vetoes, filibusters" (see F-23). Eq. 12 of the paper is the simulation V_i^sim = V_i^obs + eps_nation + eps_region_k + eps_state_j + eps_district_i with SDs 0.06, 0.02, 0.04, 0.09 (national, regional, state, Congressional district) for the 2000 election.

#### [F] F-23 | §8 | Chamber (not EC): "I found no source writing the second-stage probability for a legislature in a closed form" (line 203)
MARK: confirmed
SOURCE: GKT 2002 Sec. 2.1 (local: work-F/sswp1141.txt); the Princeton Election Consortium page for a Senate-control formula is under FILL F-1
QUOTE[work-F/sswp1141.txt]: "Voting power has also been applied to more complicated voting schemes, which we do not discuss here, such as legislative elections with committees, multiple chambers, vetoes, filibusters, and so forth (Shapley and Shubik, 1954)."
NOTE: [stated] GKT 2002 says it does not discuss it. [inferred] The first pass's statement is about what the sources it read contain and stands; one published closed-form for a Senate-control "voter power" exists (PEC: voterpower for a state = tpdf(|statemargin-MetaMargin|/sigma,tail) / voterpop), found by me and given in FILL F-1; it is a relative measure for Senate states, not a House-seat probability.

#### [F] F-24 | §8 | Line 205: GKB 1998 figures "(Sec. 6.1)": about 1 in 10 million (1992); 1 in 3.5 million in Vermont; 1 in 1.5 million small states; "on the order of 1 in hundreds of millions" in landslides (section attribution; task A checks values)
MARK: corrected
SOURCE: https://sites.stat.columbia.edu/gelman/research/published/decisive2.pdf (local: gkb1998_columbia.raw.txt, layout twin gkb1998_columbia.txt) ; Sec. 4.3 "Numerical Results" and Sec. 6.1
QUOTE[gkb1998_columbia.raw.txt]: "Voters in some of the smaller politically mod"
QUOTE[gkb1998_columbia.raw.txt]: "erate states have a greater chance (e.g., 1 in 3.5 million in"
QUOTE[gkb1998_columbia.raw.txt]: "probability is much smaller, on the order of 1 in hundreds"
QUOTE[gkb1998_columbia.raw.txt]: "in 1.5 million for some small states in some close elections"
QUOTE[gkb1998_columbia.raw.txt]: "in 100 million for all states in landslide elections such as"
CORRECTION: section attribution: the first pass puts all of line 205's EC figures under "Sec. 6.1". As printed, "1 in 3.5 million in Vermont" (1992) and "on the order of 1 in hundreds of millions" (the landslide elections of 1964, 1972, 1984) are in Sec. 4.3 (Numerical Results); Sec. 6.1 (Concluding Remarks) prints "typically of order of magnitude 1 in 10 million, rising to as much as about 1 in 1.5 million for some small states in some close elections (e.g., Nevada in 1960 and Alaska in 1976) and less than 1 in 100 million for all states in landslide elections such as 1972". The first pass's "on the order of 1 in hundreds of millions" is Sec. 4.3 wording; the Sec. 6.1 wording is "less than 1 in 100 million".
NOTE: Values are task A's. Two column-interleaved lines of the raw text are quoted in the pieces in which they run contiguously ("mod" + "erate" = "moderate"). The abstract (Abstract page 1) also says "about 1 in 10 million for close national elections such as 1992, varying by about a factor of 10 among states".

#### [F] F-25 | §8 | Line 205: GKB 1998 "1 in 10,000" as upper bound for a typical 200,000-voter congressional race; empirical House frequency about .5/20,597 (line 205: "Sec. 6.1")
MARK: corrected
SOURCE: https://sites.stat.columbia.edu/gelman/research/published/decisive2.pdf (local: gkb1998_columbia.raw.txt) ; Sec. 5 "Approximate Results for U.S. Congressional and Other Elections"
QUOTE[gkb1998_columbia.raw.txt]: "A typical value of n for an election to the U.S. Congress"
QUOTE[gkb1998_columbia.raw.txt]: "is 200,000, which gives an upper bound of 1 in 10,000 of"
QUOTE[gkb1998_columbia.raw.txt]: "This suggests a frequency probability of about .5/20,597 that a single vote will be decisive in a randomly chosen U.S. House election."
QUOTE[gkb1998_columbia.raw.txt]: "(The factor of 1/2 applies because we are considering the effect of casting a vote, not the effect of switching"
CORRECTION: section: both are in Sec. 5 (journal p.6: Sec. 5 text, then Sec. 6.1 on the same page), not Sec. 6.1. The bound is printed as "20/n": with a forecast "normal distribution with mean mu and standard deviation tau" the single-vote decisive probability is "approximately (sqrt(2 pi) tau n)^-1 exp(-(mu - .5)^2/(2 tau^2))" (Sec. 5, "as discussed by Margolis (1977)"), maximal at mu = .5; with tau = 2% of the vote ("hard to imagine a real election that could be forecast to within a standard error of less than, say, 2% of the vote") this "yields 20/n as an upper bound"; "A typical value of n for an election to the U.S. Congress is 200,000, which gives an upper bound of 1 in 10,000".
NOTE: Sec. 5 also prints the House record behind .5/20,597: "In the period 1900-1992, there were 20,597 U.S. House elections, out of which 6 were decided by fewer than 10 votes, 49 by fewer than 100 votes, 293 by fewer than 500 votes, and 585 by fewer than 1,000 votes." (page image, journal p.6), and says .5/20,597 "is of course much less than our upper bound of 1/10,000, because most of the elections were not close". The text layer garbles the bound ("2 0 / n") and the formula; I read both from the page image. 1/(sqrt(2 pi) x 0.02) = 19.95 [measured], i.e. the 20/n.

#### [F] F-26 | §8 | [measured, stylised] stage-two factor table for a 435-seat chamber and its Reading (lines 207-221)
MARK: unread
SOURCE: no source applies (own calculation)
NOTE: not a source fact: the first pass's own calculation (script chamber.py / ref.py), re-run by the orchestrating thread per the task file; nothing here is checked at a source. The setup claims it rests on are in F-09 (435 seats, 218), F-10 to F-12 (decomposition and the 1/2 weights) and F-24 (see the note on the stage-two definition). One structural observation from the sources, not a check of the table: the printed Eq. (3) of GKB 1998 and Eq. (1) of GKB 2004 weight the two exact-tie end points by 1/2 because a tie is only half a decisive event; with 435 (odd) seats and this seat decided, there is no end-point tie, so the first pass's "P(other 434 seats give exactly 217)" has no half-weight term; I did not check the script.

ORCHESTRATING WORKER: the reader marked this unread because it is the first pass's own calculation or arithmetic, not a source claim. The calculation was re-run and reproduces (see "Appendix A re-run").

#### [F] F-27 | §8 | "Size relative to a two-candidate plurality race ... smaller by the stage-two factor (about 0.01 to 0.03)" (line 223)
MARK: unread
SOURCE: no source applies (inference from the first pass's own table)
NOTE: [inferred] in the first pass; not source-checkable.

ORCHESTRATING WORKER: the reader marked this unread because it is the first pass's own calculation or arithmetic, not a source claim. The calculation was re-run and reproduces (see "Appendix A re-run").

## 9. Very small electorates (local offices, school boards, special districts, workplace votes)

*First-pass lines 225-249 of `research/electoral-systems.md`. Each block: the first-pass claim with its line number, the mark, the source and location, exact quotes, the correction if any, notes.*

#### [F] F-28 | §9 | Farber: union certification "unions lose ties" (footnote 5), decertification "the union wins ties" (footnote 9) (line 227)
MARK: confirmed
SOURCE: https://www.nber.org/system/files/working_papers/w16160/w16160.pdf (local: farber.txt; reading-order twin farber.raw.txt) ; footnote 5 (printed p.3, in Sec. 1.2), footnote 9 (printed p.5, in Sec. 2); also Sec. 3.2 text (printed p.14)
QUOTE[farber.txt]: "The fact that the union needs more than 50 percent implies that unions lose ties. Given the large number of small elections where ties can happen with non-trivial probability, this has implications for the analysis I present below."
QUOTE[farber.txt]: "In this case, the union is decertified only if a majority of the voters vote to decertify. Thus, the union wins ties in decertification elections."
QUOTE[farber.txt]: "Thus, unions lose ties. On this basis, a pro-union worker’s vote will be pivotal only if the election would be tied without his vote."
NOTE: [stated] Footnote 5 is attached to "If the union receives more than 50 percent of the votes cast in the election, then the NLRB certifies that the union is the exclusive representative"; footnote 9 to the certification/decertification split in Sec. 2 ("213,548 ... certification elections; 23,474 ... decertification elections"). Farber's estimation applies the unions-lose-ties rule (Eq. 12-13 below); he does not model decertification separately in Sec. 3.2.

#### [F] F-29 | §9 | Farber, "Rational Choice and Voter Turnout: Evidence from Union Representation Elections", NBER WP 16160 (July 2010); PDF and abstract-page URLs (line 230)
MARK: confirmed
SOURCE: https://www.nber.org/papers/w16160 (local: work-F/w16160_abs.html, strip w16160_abs.txt) and the PDF https://www.nber.org/system/files/working_papers/w16160/w16160.pdf (local: farber.txt) ; title page
QUOTE[work-F/w16160_abs.txt]: "Working Paper 16160 DOI 10.3386/w16160 Issue Date July 2010"
QUOTE[work-F/w16160_abs.txt]: "Henry S. Farber, "Rational Choice and Voter Turnout: Evidence from Union Representation Elections," NBER Working Paper 16160 (2010), https://doi.org/10.3386/w16160."
QUOTE[farber.txt]: "Working Paper 16160 http://www.nber.org/papers/w16160"
NOTE: [stated] A working paper (not peer-reviewed, as the title page says); the abstract page shows no published version.

#### [F] F-30 | §9 | Farber Eq. 12: Delta W+ = Pr(n_p = n_c) as a sum over i = 0 to INT(n/2) of multinomial terms in p_p^i, p_c^i, p_a^(n-2i) (line 230)
MARK: confirmed
SOURCE: https://www.nber.org/system/files/working_papers/w16160/w16160.pdf (local: farber.txt; reading-order twin farber.raw.txt) ; Sec. 3.2.1 "Pivotal Pro-Union Workers", Eq. (12), printed p.15 (PDF p.17; page image work-F/farber_p-17.png viewed at 130 dpi)
QUOTE[farber.txt]: "The probability that a pro-union worker’s vote is pivotal (the probablity of a tie not including the vote of worker i), based on the multinomial distribution for the vote counts, is"
QUOTE[farber.txt]: "where n = N − 1, the number of eligible voters less one and IN T (·) returns the truncated integer value of its argument."
NOTE: Transcribed from the page image (FORMULAS AS PRINTED): Delta W+ = Pr(n_p = n_c) = sum_{i=0}^{INT(n/2)} [ n! / ( i! i! (n - 2i)! ) ] p_p^i p_c^i p_a^{n-2i}. The first pass gave only the weights; the multinomial coefficient is n!/(i! i! (n-2i)!). The text layer is garbled for the exponents but the summation limits survive in the text layer too ("IN T (n/2)"). Printed typo: "probablity" in the source sentence.

#### [F] F-31 | §9 | Farber Eq. 13: Delta W- = Pr(n_p = n_c + 1) (line 230)
MARK: confirmed
SOURCE: https://www.nber.org/system/files/working_papers/w16160/w16160.pdf (local: farber.txt; reading-order twin farber.raw.txt) ; Sec. 3.2.2 "Pivotal Anti-Union Workers", Eq. (13), printed p.16 (PDF p.18; page image work-F/farber_p-18.png)
QUOTE[farber.txt]: "A similar analysis follows for anti-union workers. The probability that an anti-union worker’s vote is pivotal is the probablity that the union wins by one not including the vote of worker i. Based on the multinomial distribution for the vote counts, this is"
NOTE: Transcribed from the page image: Delta W- = Pr(n_p = n_c + 1) = sum_{i=0}^{INT((n-1)/2)} [ n! / ( (i+1)! i! (n - 2i - 1)! ) ] p_p^{i+1} p_c^i p_a^{n-2i-1}. The first pass said only "Pr(n_p = n_c + 1) (eq. 13)": right.

#### [F] F-32 | §9 | Farber symbols: n = N - 1 other eligible voters; p_p = mu G(b Delta W+), p_c = (1 - mu) G(b Delta W-), p_a = 1 - p_v; mu the expected pro-union fraction, G the cost distribution (line 230)
MARK: confirmed
SOURCE: https://www.nber.org/system/files/working_papers/w16160/w16160.pdf (local: farber.txt; reading-order twin farber.raw.txt) ; Sec. 3.2, Eqs. (4)-(9), printed pp.13-15
QUOTE[farber.txt]: "In a given workplace, the expected fraction of workers who are pro-union is denoted by µ."
QUOTE[farber.txt]: "Ci varies across workers and is distributed with CDF G(·)."
QUOTE[farber.txt]: "pp = µG(b∆W+ )."
QUOTE[farber.txt]: "pc = (1 − µ)G(b∆W− )."
QUOTE[farber.txt]: "pa = 1 − pv = 1 − µG(b∆W+ ) − (1 − µ)G(b∆W− )."
NOTE: [stated] Eqs. (5), (7), (9). Other symbols as printed: b = the benefit (b_p = -b_c = b), C_i = "the cost of voting to worker i net of the direct benefit ... from the act of voting itself" (may be negative), p_v = p_p + p_c = turnout (Eq. 8); N = n_p + n_c + n_a eligible voters (Eq. 10); a pro-union worker votes if C_i <= b Delta W+ (Eq. 4), an anti-union worker if C_i <= b Delta W- (Eq. 6). The voting probabilities are independent across voters ("Assuming that individuals' decisions to vote are independent in a given election"). The paper does not solve for p_p and p_c in closed form ("it is not possible to derive closed form solutions for pp and pc because the expressions for the proabilities of being pivotal are complicated and depend on pp and pc").

#### [F] F-33 | §9 | Farber data: 75,300 on-site elections 1972-2009, 2,014,616 eligible voters in total (Table 1 note) (line 230)
MARK: confirmed
SOURCE: https://www.nber.org/system/files/working_papers/w16160/w16160.pdf (local: farber.txt; reading-order twin farber.raw.txt) ; Table 1 note, printed p.22; sample construction Sec. 2.3, printed pp.7-8; abstract
QUOTE[farber.txt]: "This model is estimated by maximum likelihood over the sample of 75,300 on-site elections (with a total of 2,014,616 elgibile voters) with no challenged ballots, between 2 and 200 eligible voters and at least 2 votes cast."
QUOTE[farber.txt]: "I proceed with the analysis using the 77,308 on-site elections wtih no challenges 1972- 2009."
QUOTE[farber.txt]: "I develop a rational choice model of turnout in these elections, and I implement this model empirically using data on over 75,000 of these elections held from 1972-2009."
NOTE: [stated] The 75,300 is a restricted sample: of the 77,308 on-site elections without challenged ballots (1972-2009) the Table 1 sample keeps those "between 2 and 200 eligible voters and at least 2 votes cast". "1972-2009" attaches to the 77,308 and to the abstract's "over 75,000", not to the 75,300 as such. [measured] 2,014,616 / 75,300 = 26.75 eligible voters per election on average in the Table 1 sample. Source of the elections: "237,022 individual elections involving a single union 'closed' by the NLRB between July 1962 and August 2009" (Sec. 2). Printed typo: "elgibile".

#### [F] F-34 | §9 | Farber: "38 percent have 10 or fewer, 62 percent have 20 or fewer, and 74 percent have 30 or fewer eligible voters" (line 230)
MARK: confirmed
SOURCE: https://www.nber.org/system/files/working_papers/w16160/w16160.pdf (local: farber.txt; reading-order twin farber.raw.txt) ; Sec. 1.2 (end), printed p.4, item 2 of the two numbered reasons
QUOTE[farber.txt]: "2. A substantial fraction of these elections have a small number of eligible voters; 38 percent have 10 or fewer, 62 percent have 20 or fewer, and 74 percent have 30 or fewer eligible voters."
QUOTE[farber.txt]: "My analysis sample contains data on over 75,000 elections between 1972 and 2009."
NOTE: [stated] The percentages are given for "these elections" = the analysis sample (item 1 says "My analysis sample contains data on over 75,000 elections between 1972 and 2009"); no table or figure in the paper shows the distribution behind them.

#### [F] F-35 | §9 | Farber: "averaging 50 to 75 eligible voters" (Sec. 1.2) (line 230; section as cited by the first pass and in §10.3 item 7, line 279)
MARK: corrected
SOURCE: https://www.nber.org/system/files/working_papers/w16160/w16160.pdf (local: farber.txt; reading-order twin farber.raw.txt) ; Sec. 2.3 "Voter Turnout", printed p.10 (not Sec. 1.2); Sec. 2.1 and Fig. 1 (printed p.5-6) for the data behind it
QUOTE[farber.txt]: "First, these elections are relatively small, averaging 50 to 75 eligible voters (figure 1), so that a worker’s vote has a reasonable probability of being pivotal."
QUOTE[farber.txt]: "Interestingly, at the same time the average size of elections held increased gradually from about 55 workers per election to about 70 workers per election."
CORRECTION: section "Sec. 1.2" -> Sec. 2.3 ("Voter Turnout", printed p.10); the quoted words are exact. "50 to 75" is the span of the y-axis of Fig. 1 (average number of eligible voters, 5-year moving average) for ALL elections closed by the NLRB, and Sec. 2.1 describes it as about 55 rising to about 70 workers per election.
NOTE: Sec. 1.2 contains the "38 percent ... 10 or fewer" statement but not "50 to 75". The first pass's §10.3 item 7 inherits the wrong section number.

#### [F] F-36 | §9 | Farber: "from 24 to 30 between 1972 and 2008" (Sec. 6.2) (line 230; §10.3 item 7, line 279)
MARK: corrected
SOURCE: https://www.nber.org/system/files/working_papers/w16160/w16160.pdf (local: farber.txt; reading-order twin farber.raw.txt) ; Sec. 6.2 "Can the Rational Choice Model Account for the Decline in Turnout?", printed p.39
QUOTE[farber.txt]: "The average number of eligible voters increased from 24 to 30 between 1972 and 2008."
QUOTE[farber.txt]: "Elections both increased in size and were expected to be less close over this period."
CORRECTION: "from 24 to 30 between 1972 and 2008" is exact (printed p.39); the first pass's citation to "Sec. 6.2" is right. What the first pass lacks: the sentence does not say which sample the average is over. In Sec. 6.2 the model estimated is the beta-binomial of Table 2 (sample of on-site elections with 2-200 eligible voters).
NOTE: [stated] The sentence is in a paragraph about the explanatory variables of the Table 2 model ("election size and expected closeness"); [inferred] it refers to the estimation sample, whose overall mean is 26.75 [measured, see F-33], which lies between 24 and 30. The paper does not say so in words.

#### [F] F-37 | §9 | Farber prints both "50 to 75" and "24 to 30" "without reconciling them" (line 230; §10.3 item 7)
MARK: confirmed
SOURCE: https://www.nber.org/system/files/working_papers/w16160/w16160.pdf (local: farber.txt; reading-order twin farber.raw.txt) ; Sec. 2.1 (printed p.5), Sec. 2.3 (p.10), Sec. 6.2 (p.39), Table 1 note (p.22)
QUOTE[farber.txt]: "Interestingly, at the same time the average size of elections held increased gradually from about 55 workers per election to about 70 workers per election."
QUOTE[farber.txt]: "The average number of eligible voters increased from 24 to 30 between 1972 and 2008."
QUOTE[farber.txt]: "with no challenged ballots, between 2 and 200 eligible voters and at least 2 votes cast."
NOTE: [stated] Both statements are in the paper as printed and the paper does not reconcile them in words. [inferred] They describe different populations: Sec. 2.1/2.3 and Fig. 1 are the means over all NLRB elections (certification elections, 1963-2009, including large units, which pull the mean up to 55-70), whereas the model sample (Table 1 and Table 2) is restricted to 2-200 eligible voters and at least 2 votes cast, with mean 26.75 [measured: 2,014,616 / 75,300] and, per Sec. 6.2, a time path of 24 to 30. Not "inconsistent" but not the same population; the first pass was right that the paper leaves the connection to the reader.

#### [F] F-38 | §9 | Farber abstract: "most individuals (over 80 percent) vote ... independent of consideration" of pivotality; many elections have sufficiently few eligible voters (line 230)
MARK: confirmed
SOURCE: https://www.nber.org/papers/w16160 (local: work-F/w16160_abs.txt) and the PDF abstract (local: farber.txt)
QUOTE[farber.txt]: "The results suggest that most individuals (over 80 percent) vote in these elections independent of consideration of the likelihood that they will be pivotal."
QUOTE[farber.txt]: "These elections provide a particularly good laboratory to study voter behavior because many of the elections have sufficiently few eligible voters that individuals can have a substantial probability of being pivotal."
QUOTE[farber.txt]: "Among the remainder, the probability of voting is related to variables that influence the probability of a vote being pivotal (election size and expected closeness of the election)."
NOTE: [stated] Sec. 6.1 derives the "80 percent": with the pivotal probability vanishing the predicted mean turnout is 0.791 ("about 80 percent of workers vote regardless of the likelihood of being pivotal and the remaining 20 percent ... consider whether or not their vote will be pivotal"); footnote 29 gives 0.729 using the second column of Table 2. The first pass's paraphrase of the abstract ("a single vote can have a substantial chance of being decisive") is a fair reading of "substantial probability of being pivotal".

#### [F] F-39 | §9 | Farber "does not print the pivotal probabilities themselves" (line 230); task question: tables of Delta W?
MARK: confirmed
SOURCE: https://www.nber.org/system/files/working_papers/w16160/w16160.pdf (local: farber.txt; reading-order twin farber.raw.txt) ; whole paper (50-page PDF) searched for "Delta W", "pivotal" and Tables 1-3
QUOTE[farber.txt]: "The central analytic difficulty is that the probabilities of being pivotal depend on the de- cisions of all voters."
NOTE: [measured by search of the text layer] The symbols Delta W+ and Delta W- occur only in Sec. 3.2 (Eqs. 4-13, printed pp.13-16) and nowhere else. The paper has Tables 1-3 (turnout models: Table 1 binomial and beta-binomial, Table 2 beta-binomial with election size and expected closeness, Table 3 on-site versus mail) and Figures 1-21 (by their captions, all are of election counts, win rates, vote shares, turnout and fitted densities; none is a pivot probability). No table prints Delta W+ or Delta W- for any election size; no numeric pivot probability is stated in the text. The statements on pivotality are qualitative ("The probability that a worker's vote will be pivotal is inversely related to the size of the election", Sec. 5.1). It does print: predicted turnout falls from "about 95 percent in the smallest elections to less than 89 percent in elections with 100 voters or more" (Sec. 5.1) and the 0.791 / 80 percent figure (Sec. 6.1). Properties of Delta W+ stated in words (Sec. 3.2.1): maximal at p_p = p_c, larger for odd N, falls with election size.

#### [F] F-40 | §9 | Lyytikainen & Tukiainen: Finnish municipalities as small as 234 residents; election-level mean pivotality 0.063, min 0.006, max 0.193 (line 231)
MARK: confirmed
SOURCE: https://www.doria.fi/bitstream/10024/148789/1/wp50.pdf (local: lyyt.txt, task C's file; I checked only these numbers) ; table of municipality variables (population) and Table 2 Panel A
QUOTE[lyyt.txt]: "Population 1747 7506 7592 234 44804"
QUOTE[lyyt.txt]: "Panel A: Election level Pivotality 1746 0.063 0.031 0.006 0.193"
NOTE: [stated] Task C decides this; the figures match. Reading: the 234 is the minimum of the population variable in the table with 1,747 municipality-elections and population < 45,000; the 0.063 / 0.006 / 0.193 are mean / min / max of election-level "Pivotality" (N = 1,746). The same PDF prints Panel B party-election pivotality "within" 0.006 and "between" 0.020 (mean), so the first pass's "0.006 min" at the election level coincides with the within-party mean: not a conflict, a coincidence of numbers. Note the file name lyyt.txt is in r4/txt.

#### [F] F-41 | §9 | Gelman, Katz & Bafumi: the 1/sqrt(n) vs 1/n distinction and the Good-Mayer / Chamberlain-Rothschild rule (line 232; also the §6 setup claim in the task file)
MARK: confirmed
SOURCE: https://sites.stat.columbia.edu/gelman/research/published/gelmankatzbafumi.pdf (local: gkb2004.raw.txt; page images of PDF pp.6-7 = journal pp.662-663 viewed at 150 dpi: work-F/gkb04p-06.png, work-F/gkb04p-07.png) ; Sec. 2.3 "Probability Models for Voting: Going Beyond the Square-root Rule" (journal p.663)
QUOTE[gkb2004.raw.txt]: "In particular, Good and Mayer and also Chamberlain and Rothchild derive a 1/nj rule – that is, a model where the probability of decisiveness is inversely proportional to the number of voters."
QUOTE[gkb2004.raw.txt]: "This model arises by assuming that votes are binomially distributed, but with binomial probabilities p that themselves vary over the nj voters in a jurisdiction."
QUOTE[gkb2004.raw.txt]: "Then, for large or even moderate values of nj, the distribution pvj of the vote proportion vj is essentially fixed (not depending on nj), so that pvj (0.5) is a constant, and the probability of a vote being decisive is proportional to 1/nj (from (2))."
NOTE: [stated] The footnote (23) cites "I. J. Good and L. S. Mayer, 'Estimating the Efficacy of a Vote', Behavioral Science, 20 (1975), 25-33; Chamberlain and Rothchild, 'A Note on the Probability of Casting a Decisive Vote'" and footnote 19 gives "G. Chamberlain and M. Rothchild ... Journal of Economic Theory, 25 (1981), 152-62". The paper spells the name "Rothchild" (not Rothschild). The constant (my reading, to be compared with the reading of task A; page image PDF p.6, journal p.662): the printed formula is Pr(a given vote is decisive in jurisdiction j) = p_{v_j}(0.5)/n_j = sqrt(2/pi) x 1/sqrt(n_j); "What matters for comparing voters is not the constant factor sqrt(2/pi) but the proportionality with 1/sqrt(n_j)". So the first pass's extract form "(2/sqrt(pi))(1/sqrt(n_j))" (§10.3 item 1) is wrong: the printed constant is sqrt(2/pi) = 0.7979 [measured], not 2/sqrt(pi) = 1.1284; it equals my swing value 0.798/sqrt(N) noted in §10.3 item 1, so there is no 1.41 or 2.83 discrepancy with the paper. [measured] Also: the paper's forecast example "52 per cent ... standard error of 3 per cent ... 10,000 voters ... approximate [1/sqrt(2 pi)(0.03)] exp(-0.5(0.05/0.03)^2)/n_j = 1.84/n_j" (journal p.663, page image) does not reproduce: 1/(sqrt(2 pi) x 0.03) = 13.30; times exp(-0.5 x (0.05/0.03)^2) = 0.2494 gives 3.32; with the 2-point distance from 50% that a 52% forecast implies, exp(-0.5 x (0.02/0.03)^2) = 0.8007 gives 10.65. Neither is 1.84 (I could not find the arithmetic behind it).

#### [F] F-42 | §9 | Ballotpedia "Races decided by 10 votes or fewer": the page, 2018-2026 (line 234)
MARK: confirmed
SOURCE: https://ballotpedia.org/Races_decided_by_10_votes_or_fewer (local: ballotpedia10.html, the saved page; tag-stripped text work-F/ballotpedia10.plain.txt) ; page header, lead paragraphs
QUOTE[work-F/ballotpedia10.plain.txt]: "Elections decided by 10 votes or fewer"
QUOTE[work-F/ballotpedia10.plain.txt]: "(Redirected from Races decided by 10 votes or fewer)"
QUOTE[work-F/ballotpedia10.plain.txt]: "This page analyzes trends in elections decided by 10 or fewer votes since 2018."
QUOTE[work-F/ballotpedia10.plain.txt]: "This page is updated annually. It was last updated in October 2026."
QUOTE[work-F/ballotpedia10.plain.txt]: "Close elections by margin of victory, 2018-2026"
NOTE: [stated] The saved file is a real server-rendered MediaWiki page (not a JavaScript shell): the full list of races is in an HTML table (733 data rows). The page is now titled "Elections decided by 10 votes or fewer"; the first-pass title is the redirect. Two Datawrapper charts (an overview chart and a state map) are iframes loaded from datawrapper.dwcdn.net (not read; not on my hosts); their data are not needed because the table is in the page. The page has an empty Footnotes section (no references).

#### [F] F-43 | §9 | Ballotpedia: "out of 150,010 elections in Ballotpedia's coverage scope, 734 elections were decided by 10 or fewer votes" (2018-2026) (line 234)
MARK: confirmed
SOURCE: https://ballotpedia.org/Races_decided_by_10_votes_or_fewer (local: ballotpedia10.html, the saved page; tag-stripped text work-F/ballotpedia10.plain.txt) ; lead paragraph
QUOTE[work-F/ballotpedia10.plain.txt]: "Since 2018, out of 150,010 elections in Ballotpedia's coverage scope, there were 734 elections decided by 10 or fewer votes (0.004%)."
NOTE: [stated] Counts as printed. [measured] The saved table has 733 data rows (734 <tr> elements including the header), not 734; the page text's party split (Democrats 167, Republicans 191, "nonpartisan or minor party" 376) sums to 734 and the table gives 167 / 190 / 376 [measured: the table's winners by party: Democratic 167, Republican 190, Nonpartisan 359, Independent 7, Libertarian 4, Constitution 2, Green 2, No Party Affiliation 1, Reform 1], i.e. one Republican row is missing from the saved table or the text count is one too high.

#### [F] F-44 | §9 | Ballotpedia: "496 by fewer than five votes" (line 234)
MARK: corrected
SOURCE: https://ballotpedia.org/Races_decided_by_10_votes_or_fewer (local: ballotpedia10.html, the saved page; tag-stripped text work-F/ballotpedia10.plain.txt) ; lead paragraph versus the table (margin column)
QUOTE[work-F/ballotpedia10.plain.txt]: "Of those 734 elections, 496 were determined by fewer than five votes, including 104 decided by a single vote."
CORRECTION: the page prints 496, and the page's own table does not support it: [measured, from the 733 table rows] margins: 1 vote 104, 2 votes 96, 3 votes 64, 4 votes 88, 5 votes 84, 6 votes 71, 7 votes 52, 8 votes 60, 9 votes 68, 10 votes 46. Fewer than five (margin 1-4): 352; five or fewer: 436; six or fewer: 507. No threshold reproduces 496.
NOTE: So the first pass's transcription of the page is right ("496 ... fewer than five votes") but the figure is inconsistent with the table on the same page. Which is right is not determinable from the page; treat 352 (table) and 496 (text) as conflicting, 104 as confirmed (F-45). A fuller list of the margin distribution is in my work file.

#### [F] F-45 | §9 | Ballotpedia: "104 decided by a single vote" (line 234)
MARK: confirmed
SOURCE: https://ballotpedia.org/Races_decided_by_10_votes_or_fewer (local: ballotpedia10.html, the saved page; tag-stripped text work-F/ballotpedia10.plain.txt) ; lead paragraph; table rows with margin 1
QUOTE[work-F/ballotpedia10.plain.txt]: "including 104 decided by a single vote."
NOTE: [measured] 104 table rows have a margin of victory of 1: agrees with the text.

#### [F] F-46 | §9 | Ballotpedia: smallest total vote count 13, a 2024 Constitution Party primary in SC-4, 8 to 5 (line 234)
MARK: confirmed
SOURCE: https://ballotpedia.org/Races_decided_by_10_votes_or_fewer (local: ballotpedia10.html, the saved page; tag-stripped text work-F/ballotpedia10.plain.txt) ; lead paragraph and table
QUOTE[work-F/ballotpedia10.plain.txt]: "Among these elections, the one decided with the fewest total votes was a 2024 Constitution Party primary for South Carolina's 4th Congressional District (13). Mark Hackett beat Michael Chandler 8 votes to 5."
QUOTE[work-F/ballotpedia10.plain.txt]: "2024 | SC | South Carolina District 4 | Mark Hackett | Constitution Party | 8 | Michael Chandler | Constitution Party | 5 | 3 | 13"
NOTE: [stated] and [measured]: 13 is the minimum total in the 733 rows. Its margin is 3, not 1 (the first pass did not say). The next smallest totals are 14 (AZ Wilson Elementary School District, 2022, 8-6), 16 (UT House 21, 2024, 9-7) and 17 (two rows).

#### [F] F-47 | §9 | Ballotpedia: largest visible total 23,525 (a 2022 Massachusetts House race) (line 234)
MARK: corrected
SOURCE: https://ballotpedia.org/Races_decided_by_10_votes_or_fewer (local: ballotpedia10.html, the saved page; tag-stripped text work-F/ballotpedia10.plain.txt) ; the table of all rows (sorted by margin, then total)
QUOTE[work-F/ballotpedia10.plain.txt]: "2022 | MA | Massachusetts House of Representatives 2nd Essex District | Kristin Kassner | Democratic | 11,763 | Leonard Mirra | Republican | 11,762 | 1 | 23,525"
QUOTE[work-F/ballotpedia10.plain.txt]: "2020 | IA | Iowa District 2 | Mariannette Miller-Meeks | Republican | 196,964 | Rita Hart | Democratic | 196,958 | 6 | 393,922"
CORRECTION: "largest visible total 23,525" -> 23,525 is the largest total among the 104 one-vote rows (the last of them), not in the whole table; the largest total in the full table is 393,922 (Iowa District 2, 2020, 196,964 to 196,958, margin 6). Next largest [measured]: 129,553 (AZ House 9, 2020, margin 9), 129,420 (Travis County Court at Law, TX, 2020, margin 4), 123,148 (NY Senate 50, 2022, margin 10), 80,489 (AZ House 27, 2022).
NOTE: [measured] 688 of the 733 rows have a total under 10,000 and 420 under 1,000; median total 724. So the first pass's "most visible rows are local" is a result of reading only the first screen of a table sorted by margin, whose 1-vote rows are mostly NC 2019 municipal elections.

#### [F] F-48 | §9 | Ballotpedia: "most visible rows are local or school-board races" (line 234)
MARK: confirmed
SOURCE: https://ballotpedia.org/Races_decided_by_10_votes_or_fewer (local: ballotpedia10.html, the saved page; tag-stripped text work-F/ballotpedia10.plain.txt) ; table (district name and state columns)
QUOTE[work-F/ballotpedia10.plain.txt]: "Every year, Ballotpedia covers thousands of elections at all levels of government—from the halls of Congress down to school boards in all parts of the country."
NOTE: [measured, crude keyword classification of the district-name column] of 733 rows: about 354 are state-legislative or congressional (names with House of Representatives, Senate, General Assembly, Congress/district), about 331 other local bodies (towns, councils, counties), about 48 school bodies; 359 winners are listed as "Nonpartisan". 274 rows are NC, 129 NH, 48 VT; 267 rows are NC elections in 2019 (36% of the table), 280 rows are in the year 2019 in all. So local races are about half the table, not "most", and the table is heavily concentrated in one state and year, which matters if the counts are used as a rate.

#### [F] F-49 | §9 | Ballotpedia prints the share as "0.004%"; 734 / 150,010 = 0.49% (line 234; §10.3 item 6)
MARK: confirmed
SOURCE: https://ballotpedia.org/Races_decided_by_10_votes_or_fewer (local: ballotpedia10.html, the saved page; tag-stripped text work-F/ballotpedia10.plain.txt) ; lead paragraph
QUOTE[work-F/ballotpedia10.plain.txt]: "there were 734 elections decided by 10 or fewer votes (0.004%)."
NOTE: [measured] 734 / 150,010 = 0.004893 = 0.489%; as a percentage 0.004% is wrong by a factor of about 122; as a fraction 0.004893 would round to 0.005, so even "0.004" does not match unless truncated [inferred: the page's number looks like the fraction 0.00489 truncated to three decimals and labelled with a percent sign; not stated by the page]. The page prints the same text without comment.

#### [F] F-50 | §9 | Ballotpedia says "the 660 elections" in one place (line 234; §10.3 item 6)
MARK: confirmed
SOURCE: https://ballotpedia.org/Races_decided_by_10_votes_or_fewer (local: ballotpedia10.html, the saved page; tag-stripped text work-F/ballotpedia10.plain.txt) ; section "Overview", and the embedded chart titles in the raw HTML (local: ballotpedia10.html)
QUOTE[work-F/ballotpedia10.plain.txt]: "The chart below shows how many of the 660 elections were decided by each vote margin and the winners by political party."
QUOTE[work-F/ballotpedia10.plain.txt]: "The map below highlights each state by the number of elections decided by 10 or fewer votes from 2018 to 2025."
QUOTE[ballotpedia10.html]: "title="Close races by winner party, 2018-2023""
NOTE: [stated] and [inferred]: the "660" sentence, the map sentence ("2018 to 2025") and the chart titles ("2018-2023") look like text left over from earlier annual updates, while the lead paragraph and the table caption were updated to 2018-2026 / 734 ("last updated in October 2026"). The page does not explain 660; this is my reading, not the page's statement.

#### [F] F-51 | §9 | "The page does not define its coverage scope or its method of finding races" (line 234)
MARK: confirmed
SOURCE: https://ballotpedia.org/Races_decided_by_10_votes_or_fewer (local: ballotpedia10.html, the saved page; tag-stripped text work-F/ballotpedia10.plain.txt) ; whole page (text and raw HTML searched for "scope", "coverage", "method", "footnote", "reference")
QUOTE[work-F/ballotpedia10.plain.txt]: "Every year, Ballotpedia covers thousands of elections at all levels of government—from the halls of Congress down to school boards in all parts of the country."
NOTE: [stated by absence] The only wording is "elections in Ballotpedia's coverage scope" (lead paragraph) and "Every year, Ballotpedia covers thousands of elections at all levels of government—from the halls of Congress down to school boards in all parts of the country"; the Footnotes section is empty (the page's script hides it when no reference exists); no method, no data source, no statement of whether primaries, runoffs or recount results are used for "decided by". The table does include primaries (e.g. the SC-4 Constitution Party primary), nonpartisan local races, and race-year 2026 results. A definition of "coverage scope" was not looked for on another Ballotpedia page (no link on this page leads to one).

#### [F] F-52 | §9 | Ballotpedia table and text: consistency (added, not in the first pass)
MARK: corrected
SOURCE: https://ballotpedia.org/Races_decided_by_10_votes_or_fewer (local: ballotpedia10.html, the saved page; tag-stripped text work-F/ballotpedia10.plain.txt) ; lead paragraph versus table
QUOTE[work-F/ballotpedia10.plain.txt]: "Members of the Democratic Party won 167 elections decided by 10 or fewer votes, while Republicans won 191, and nonpartisan or minor party candidates won 376."
CORRECTION: first pass assumes the page's figures are mutually consistent apart from 0.004% and 660 -> three further inconsistencies between the text and the saved table [measured]: (a) 734 stated vs 733 table rows; (b) Republicans 191 stated vs 190 in the table; (c) "496 fewer than five" stated vs 352 (margin 1-4) in the table.
NOTE: The 104 one-vote count, the Democratic 167 and "nonpartisan or minor party" 376 do match the table. Because the page was fetched 2026-11-07 and "last updated October 2026", the text and the table may come from different update steps. Which numbers are right is not decidable here.

#### [F] F-53 | §9 | [measured] exact small-N decisiveness table (binomial 1/sqrt(2 pi N); Beta-binomial) and its Reading (lines 236-247)
MARK: unread
SOURCE: no source applies (own calculation; re-run by the orchestrating thread)
NOTE: Not a source fact. One setup claim is sourced: the first pass's tie convention ("ties by fair coin") is the convention of GKT 2002 Sec. 2.1 ("We assume that tied elections at all levels are decided by coin flips", local work-F/sswp1141.txt) and of GKB 2004 Sec. 2.1 ("with ties at all levels broken by coin tosses"); Farber instead uses the unions-lose-ties rule (F-28), so for a real union election the table's tie rule is not the one that applies. GKB 2004 says its continuous approximation of the within-jurisdiction probability is for "n_j in any district ... large enough - greater than 100, say" (F-13): the first pass's N = 9, 19, 29 rows are below that, so the 1/sqrt(2 pi N) column there is outside the range the paper claims for its approximation [inferred; the first pass shows the exact binomial value alongside].

ORCHESTRATING WORKER: the reader marked this unread because it is the first pass's own calculation or arithmetic, not a source claim. The calculation was re-run and reproduces (see "Appendix A re-run").

#### [F] F-54 | §9 | "a school-board seat decided by 5,000 voters has a probability about 2,000 times that of a national election of 10 million ... a 10-voter workplace vote about 500 times higher again, about a million times" (line 249)
MARK: unread
SOURCE: no source applies (own scaling argument)
NOTE: [measured: arithmetic] 10,000,000 / 5,000 = 2,000; 10,000,000 / 10 = 10^6; 10^6 / 2,000 = 500: the ratios follow from 1/N scaling. The 1/N scaling is [stated] by GKB 2004 only as an empirical regularity of electoral districts (F-18: decisive probability roughly proportional to n^-0.9, the exponent "perhaps" -0.1 on the vote differential); the size range of the districts in its Fig. 3 is not in the text and was not read, so extending it to 10 voters is an extrapolation, which the first pass flags as [inferred].

ORCHESTRATING WORKER: the reader marked this unread because it is the first pass's own calculation or arithmetic, not a source claim. The calculation was re-run and reproduces (see "Appendix A re-run").

## 10. Summary, what each system asks of the model, disagreements, unread (re-checked)

### 10.1 The first pass's summary paragraph, sentence by sentence

- *"In every system ... the same event: the other voters leave the result within one vote of a boundary ... (a tie counts half)."* A definition; consistent with Baltz's direct pivotality (E-01 to E-03), Bouton's second-round event (B-05), Farber's Eq. 12-13 (F-30, F-31). IRV's indirect pivotality is not a first-place tie for the candidate the ballot ranks (E-03). With the ½ weight the quantity is the vote-against-abstaining Q; against the other side it is 2Q (A-26).
- *"Three or more candidates ... 1.05 to 1.26 times the two-candidate value ... three-way ties of order 1/N² (Myatt & Fisher)."* The numbers reproduce (A-18; Appendix A). The orders in N and the three-way formula are as printed; the two-way constant is misprinted in the paper (A-06).
- *"Non-monotonic outcomes (1.6% of 182 US elections; 62 of 1,079 Scottish STV; 15% or more of simulated competitive three-candidate IRV)."* 1.6% is 3 of 182 upward failures (Graham-Squire & McCune Table 7; E-36 to E-40). 62 of 1,079 confirmed from the Crossref abstract (B-31); the per-type rates are unread. "15% or more" is Ornstein & Norman's lower bound for competitive elections, their definition of competitive (E-27 to E-30). None of these is a per-ballot probability (as the first pass said). Allard (1996) is not an IRV estimate (E fill F-3a).
- *"In list PR ... about M/N, three to eighteen times the plurality figure in my cases."* Reproduced, and the two-candidate comparators are now computed rather than scaled (Appendix A). Stylised (Dirichlet κ = 400); no published counterpart (C fill F-3).
- *"A turnout quorum creates a second pivot event in which, in the only model I read, voting can harm a voter's own side."* Confirmed in the docx appendix to the Aguiar-Conraria et al. paper (eq. A.3, the negative terms for opponents under a participation quorum; D-09, D-10; note the printed inconsistency in the opponent line). The paper's main text is unread. A supermajority pass condition Y ≥ q(Y+X) is the first pass's own definition; no readable source states it (D-01).
- *"Chamber control ... about 1% to 2.5% for a near-toss-up 435-seat chamber."* Reproduced (F-26, Appendix A); stylised; see the caveat on the seeds.
- *"Very small electorates ... 10% to 12% at 9 other voters ... real-data counts of races decided by a handful of votes are consistent."* The exact small-N table reproduces (F-53). The Ballotpedia page that supplies the real-data counts contradicts itself (F-52), so it supports only that such races exist, not their frequency.
- *"I found no published single-vote pivot probability for a real election outside the two-party cases, except the Finnish municipal bootstrap."* None found by any reader in the fill searches (B F-03, C F-3, D F-2, F fill F-1 and F-2). The Finnish figure stands as an ex-post bootstrap and Luechinger et al. criticise that method (C-27 and the digest). A published figure for chamber control was not found; Princeton Election Consortium publish a relative Senate "voter power" measure (F fill F-1).

### 10.2 What each system asks of the model: evidence grades after the re-read

The table of the first pass stands; its evidence column changes in these rows. *IRV/RCV:* the formulas are now transcribed from page images (FORMULAS P-0 to P-5), with the paper's independence assumptions and with misprints noted; simulation only. *Two-round:* Bouton's magnitudes have closed forms (Lemmas 2 and 3), exponential rates, not probabilities. *PR/mixed:* Luechinger et al.'s margins transcribed (D'Hondt, largest remainder, candidate and overall margin); no probability anywhere in the paper; Lyytikäinen & Tukiainen prints no aggregation formula. *Referendum:* the quorum model is the docx appendix (n = 9, participation quorum 4, approval quorum 3). *Small electorate:* Farber's Eq. 12-13 transcribed; no ΔW values printed. *Primary, chamber control:* no source; unchanged.

### 10.3 The first pass's twelve open points, and where each stands

1. **Tie constant.** Resolved (A-14, A-26): the paper prints √(2/π); the extract lost the radical. Both constants are right for their own comparison.
2. **How often non-monotonicity matters.** The three measures are confirmed as measures (E, B-31); still not on one scale; no per-ballot probability in any source. The "1-4%" and per-type Scottish rates are unread.
3. **Graham-Squire & McCune inconsistencies.** Two are in the paper as printed; the Alaska item is not an inconsistency; file is v2 (6 March 2023); two more inconsistencies found (E-40, E-44, E-48).
4. **Baltz's 10⁻⁷ and 10⁻⁶ against the 1/N scale.** Reconciled as far as the paper allows (E-24, E-49, RECONCILIATION): power-law panel only, log-mean, a sum over ballots; the uniform panel is on the 1/N scale. What cannot be settled from the paper is listed there.
5. **Lyytikäinen & Tukiainen.** 0.006 and 0.028 are different units; 234 is the sample minimum and "roughly 800" is the smallest mainland municipality (C-30, C-33, C-45).
6. **Ballotpedia "0.004%" and "660".** Both wrong or stale; more inconsistencies found (F-49, F-50, F-52, F-55).
7. **Farber "50 to 75" and "24 to 30".** Different populations (all elections against the model sample); the first is in Sec. 2.3 (F-35 to F-37, F-56).
8. **Aguiar-Conraria "more than 40" against "57 to 70".** Unread (D-14): the main text is paywalled.
9. **McCune & Graham-Squire "1-4%" against 0.86%.** Unread (B-35, B-45): only the Crossref abstract was reachable.
10. **BSW shortfall.** Resolved: 9,529 or 10,031 votes (C-39, C-46).
11. **Brexit counts from a secondary site.** Still read only there; the Electoral Commission and Commons Library pages are behind Cloudflare; 33,551,983 equals Leave plus Remain exactly (D-25, D-26).
12. **What was not found.** Unchanged: no published single-vote decisive probability for a real multi-candidate plurality election, runoff, PR election other than the Finnish bootstrap, STV, referendum under a supermajority or quorum rule, primary, chamber, or small local election. The queries tried are in the fill blocks.

### 10.4 The unread list

Superseded by the section "Everything still unread, and why" below, which collects each reader's list.

### Register: blocks that bear on §10

#### [A] A-26 | §10.3 item 1 (L273) | The tie constant: GKB extract "(2/sqrt(pi))*(1/sqrt(n_j))" versus my exact 1/sqrt(2 pi N) for Q (vote versus abstain) and sqrt(2/(pi N)) for the full swing; "extract is 1.41x my swing and 2.83x my Q"
MARK: corrected (the extract misread the printed constant; the printed constant agrees with the exact calculation)
SOURCE: https://sites.stat.columbia.edu/gelman/research/published/gelmankatzbafumi.pdf (local: gkb2004.raw.txt) ; Sec. 2.1 p. 660, Sec. 2.2 eq. (2) p. 661, Sec. 2.2.2 p. 662, Appendix p. 674 (page images PDF pp. 6, 7, 18)
QUOTE[gkb2004.raw.txt]: "Next, the power of a given voter in jurisdiction j is the probability that party A wins if that voter supports A, minus the probability that A wins if that voter supports B."
QUOTE[gkb2004.raw.txt]: "Under random voting, the distribution pvj of the vote share among the nj voters in"
QUOTE[gkb2004.raw.txt]: "jurisdiction j is approximately normally distributed with mean 0.5 and standard deviation"
QUOTE[gkb2004.raw.txt]: "What matters for comparing voters is not the constant factor 兹2/ but the proportionality"
CORRECTION: the paper's constant is **√(2/π) ≈ 0.7979**, i.e. "Pr (a given vote is decisive in jurisdiction j) = p_{v_j}(0.5)/n_j = √(2/π) · 1/√n_j" (image, p. 662), not 2/√π = 1.128. The extract's form was a misreading of a radical lost in the text layer ("兹2/" with the π missing).
HAND DERIVATION (paper's own definitions; arithmetic shown; numbers by SP/r4/work-A/calc1.py):
 1. What is compared with what. Sec. 2.1 (quoted above): voter power = P(A wins | this voter supports A) − P(A wins | this voter supports B). The Appendix (eq. 3) uses the same convention: v is "the proportion in favour of candidate A, excluding your potential vote" with the denominator the n votes, so your vote for A moves A's share from v to v + 1/n, and your vote for B leaves it at v; the decisive probability is E[π(v + 1/n) − π(v)] = p(0.5)/n. So "decisive" = vote for A versus vote for B; abstention is not part of the comparison, and n_j = "the n_j voters in jurisdiction j" includes the voter (Sec. 2.1: "Each jurisdiction j has n_j voters"). 
 2. Exact calculation under random voting with this definition. Let the n − 1 = N other voters each vote A with probability 1/2; S = number of other votes for A, S ~ Bin(N, 1/2). Take N even (n odd, so no ties in the final count). A wins with my vote for A iff S + 1 > N − S + 0, i.e. S ≥ N/2; A wins with my vote for B iff S > N − S + 1, i.e. S ≥ N/2 + 1. Difference = P(S = N/2) = C(N, N/2)/2^N. For N odd the same difference (with coin-toss ties) equals the average of the two central probabilities, the same value to leading order. Binomial local limit: P(S = N/2) ≈ 1/√(2π · N/4) = √(2/(π N)).
 3. The paper's normal approximation (Sec. 2.2.2): v ≈ N(0.5, σ²) with σ = 0.5/√n. Density at the mean: 1/(σ√(2π)) = √n/(0.5 √(2π)) = 2√n/√(2π) = √(2/π) · √n. Divide by n (eq. 2): √(2/π) · √n / n = √(2/π)/√n = 0.7979/√n. Same as step 2 with N ≈ n.
 4. Numbers (script calc1.py, exact binomial): N = 100: P(tie among others) = 0.0795892 versus √(2/(πN)) = 0.0797885; N = 1,000: 0.025225 versus 0.0252313; N = 10,000: 0.0079786 versus 0.0079788 (ratio 0.99998); N = 100,000: 0.0025231 versus 0.0025231. The extract's "(2/√π)/√N" would be 0.0112838 at N = 10,000, i.e. 1.414 times the exact swing: it does not fit.
 5. Versus abstaining (first pass's Q, with ties broken by a fair coin): with N others and no vote from me, a tie among the others (probability P(S = N/2) for N even) gives me a coin toss; my vote for A resolves it in A's favour, a gain of 1/2: Q = (1/2) P(S = N/2) = 1/√(2πN) = 0.3989/√N = 0.0039894 at N = 10,000 (first pass: Q = 0.003989 at N = 10,000, matches; my recomputation 0.003989, calc3.py).
 6. Result: the paper's √(2/π)/√n_j (≈ 0.798/√n) equals the exact vote-for-A-versus-vote-for-B swing; the first pass's own "Q" (vote versus abstain) is exactly half of it (0.399/√N). Both are right for their own comparison; they differ by a factor 2, not by 1.41 or 2.83. The first pass's difference of "1.41x my swing and 2.83x my Q" came from reading the constant as 2/√π (1.128) instead of √(2/π) (0.798): 1.128/0.798 = 1.414 and 1.128/0.399 = 2.83 are exactly those ratios.
 7. GKB 1998 eq. (2), f_v(.5)/n_i with n_i = voters excluding yourself, also counts the tie among the others with weight 1 (A-21); it is therefore the same convention (full tie probability = A-versus-B swing) although its words say "either vote for one candidate or not vote". [inferred]
NOTE: nothing in the paper changes the constant for 3+ candidates; GKB 2004 is a two-party paper ("elections with two parties (A and B)", Sec. 2.1).

#### [B] B-45 | §10.3 item 9 | "McCune & Graham-Squire (Scottish STV): 'on the order of 1-4% for each type' in the introduction versus a committee-size rate of 0.86%." (line 281)
MARK: unread (see B-35)
SOURCE: not read
NOTE: see B-35.


---

#### [C] C-45 | §10.3 item 5 | L&T: "within-party pivotality is 0.006 in Table 2 but 0.028 in Table A1; the minimum municipal population is 234 in Table 3 but the text says the smallest mainland municipality has 'roughly 800 inhabitants'; the PDF text is scrambled in places. The election-level mean 0.063 is also a weighted average that mixes party-level and candidate-level events." (line 277)
MARK: corrected
SOURCE: https://www.doria.fi/bitstream/10024/148789/1/wp50.pdf (local: lyyt.txt) ; see C-27, C-30, C-33, C-28
CORRECTION: as printed: (i) 0.006 is Table 2 Panel B "Pivotality, within", unit = party-election (N 10,171); 0.028 is Table A1 "Real within", unit = election-candidate (N 146,234): two units, and the paper says "Differences to descriptions in Table A1 arise mainly from the weighting" (C-30); (ii) 234 is the minimum of the sample's population over 1,747 municipality-elections (Table 3), while "roughly 800" is about "the smallest mainland municipality" (the word "mainland" is in the text), so the two statements are about different sets; the paper does not say which municipality has 234 (C-33); (iii) I rendered PDF pp. 5, 23, 24 (Table 2), 26 (Table 3) and 49 (Table A1) as images and the numbers I quote agree with the text layer (lyyt.txt); (iv) the election-level 0.063 is, per the paper, "a weighted (by respective vote shares) average over both the within party pivotal probability ... and the between parties pivotal probability" and the single measure is "the sum of these weighted between and within pivotalities" (C-27): no formula is printed.
NOTE: [stated] Table 2's own Panel A mean 0.063 is larger than the sum of Panel B's party-election means (0.006 + 0.020 = 0.026), because Panel A is a different weighting and unit; the paper does not reconcile them.

#### [C] C-46 | §10.3 item 10 | BSW shortfall: "13,435 votes in the provisional count (Stuttgarter Zeitung) and 4,277 more votes in the final count (t-online); I could not read the final totals, so the final shortfall (about 9,000 to 10,000) is my subtraction ...; the English Bundeswahlleiterin release prints 4.981%, the Stuttgarter Zeitung 4.97293758% (provisional); the two are not the same count." (line 282)
MARK: corrected
SOURCE: see C-37, C-38, C-39, C-11
CORRECTION: the final totals ARE readable: Bundeswahlleiterin results page, "Final result": BSW second votes 2,472,947 (4.981%), valid second votes 49,649,512. The final shortfall is 9,529 votes if the extra votes come from other parties' votes (total of valid votes unchanged; the convention of the Stuttgarter Zeitung's 13,435) and 10,031 votes if they are new valid votes (C-39); the first pass's subtraction 9,158 is 371 too low because it ignored that the 5% line rose by 371.25 votes when the valid total rose by 7,425. 4.981% (final) and 4.97293758% (provisional) are different counts, as the first pass said; both are reproduced by my division (4.98080827% rounds to 4.981; 4.97293758% exactly) [measured].
NOTE: [stated] The Bundeswahlleiterin's final shares of CDU etc. are printed to one decimal and the BSW share to three decimals "if a party fell just short of the 5 percent threshold" (C-11).

#### [E] E-46 | §10.1 | line 252: "(1.6% of 182 US elections in the empirical count; 62 of 1,079 Scottish STV elections; 15% or more of simulated competitive three-candidate IRV elections)"
MARK: confirmed
SOURCE: Table 7 of https://arxiv.org/pdf/2301.12075 (E-36); Sec. 5 of https://www.rangevoting.org/OrnsteinNormanMonotonicityIRV.pdf (E-29); the Scottish figure is task B's
QUOTE[gs_mccune.txt]: "Rate 1.1% 1.6% 1.6% 1.1% 0.5% 3.8% 52.5%"
QUOTE[ornstein.raw.txt]: "results suggest a lower bound estimate of 15 % for competitive elections"
NOTE: 1.6% of 182 = 3 elections: the *upward* monotonicity rate in Table 7 [stated]. 15%: Ornstein & Norman's lower bound [stated]. 62 of 1,079: **unread by me** (task B holds the Scottish paper); the denominator 1,079 is corroborated by G-S&M (E-45). The same sentence in §10.1 also says "'indirect pivotality' in IRV (Baltz 2025)": confirmed (E-01). The §10.1 phrase "so the sign of a ballot's effect is not always the intuitive one" is the first pass's inference: supported for the *election-level* paradox (O&N, G-S&M) and, in Baltz's pivot setting, by his remark that an indirectly pivotal ballot need not elect a more-preferred candidate (E-18).

#### [E] E-47 | §10.3 | item 2: "How often non-monotonicity matters": O&N 15% to 51%; G-S&M 1.6% of 182; (McCune & GS about 1-4% per type); measures differ
MARK: confirmed
SOURCE: E-29 and E-36 above
QUOTE[ornstein.raw.txt]: "between 15 % and 51 % of competitive elections (excluding ties, which account for approximately 1.1 % of simulated elections)."
QUOTE[gs_mccune.raw.txt]: "Our general finding is that RCV’s weaknesses are rarely observed in real-world elections, with the exception that ballot exhaustion frequently causes majoritarian failures."
NOTE: Both figures are as the first pass says. "no source puts them on one scale, and none gives the per-ballot probability": confirmed for these two papers and for Baltz. One thing the first pass did not have: Allard's 2.5 x 10^-4 per multi-member constituency election (F-3) is a third, per-election, STV-specific frequency, from a uniform-prior area calculation; and G-S&M's counts are over elections that went to a second round only (about "at least 100" more elections with a first-round majority were left out). The "1-4% for each type" in Scotland is task B's.

#### [E] E-48 | §10.3 | item 3: "Graham-Squire & McCune internal inconsistencies (extractor): Table 7 prints 52.5% ... 95 of 182 is 52.2%; the text says six compromise-voting elections but lists seven; the Alaska upward-monotonicity example is a hypothetical shift. Which version of the paper was read is not known."
MARK: corrected
SOURCE: https://arxiv.org/pdf/2301.12075 (local: gs_mccune.raw.txt, gs_mccune.txt); E-37, E-39, E-44
QUOTE[gs_mccune.raw.txt]: "Of the 182 elections in our database, 95 demonstrate a majoritarian failure."
CORRECTION: three flagged items -> two are in the paper as printed (52.5% vs 95/182 = 52.2%; "six" vs seven listed), one is not an inconsistency (the Alaska "hypothetical shift" is how all monotonicity paradoxes are defined); version read = **v2, 6 March 2023**. Two further inconsistencies in the paper found: Conclusion "0.5-1.1%" vs Table 7 upward 1.6% (E-40); Pierce County called 2009 in the text and 2008 in the Table 5 caption and Table 9 (E-39).
NOTE: [stated] and [measured].

#### [E] E-49 | §10.3 | item 4: "Baltz's simulated probabilities (about 1e-7 for plurality and 1e-6 for IRV at 1,000 voters) versus the 1/N-scale values in this report (about 0.006 to 0.016 at N = 1,000): reconciling them needs the paper's Fig. 1 data and its Assumptions 1 and 2, which I did not see. Treat the Baltz values as comparisons between the two systems on one stylised electorate, not as levels."
MARK: corrected
SOURCE: baltz_arxiv.raw.txt, baltz_sup.raw.txt and the two Figure 1 images; see the Reconciliation section below
QUOTE[baltz_sup.raw.txt]: "The total pivotal probability on the y-axis is the sum of the pivotal probability of every possible ballot."
CORRECTION: "(about 1e-7 for plurality and 1e-6 for IRV at 1,000 voters)" -> those averages are for the power-law, clear-front-runner panel only (log axis, IRV about 10^-5.6 to 10^-5.9, SMDP about 10^-7.6 to 10^-8.9 by the plotted mean lines, individual runs from about 10^-2.4 down to 10^-12.5); for the uniform panel at the same 1,000 voters the plotted y-values are 0.003 to 0.12 (mean lines about 0.03 to 0.08), a sum over all ballots. "Fig. 1 data and Assumptions 1 and 2 ... I did not see" -> I have now seen the figure (both versions), Assumptions 1 and 2, and the supplement; the paper still does not let the two scales be compared one-for-one (below). The closing advice "Treat the Baltz values as comparisons between the two systems on one stylised electorate, not as levels" is consistent with what the paper itself says (footnote 6: "initial pivotal probabilities of these election structures"; supplement: "these are stylized figures").
NOTE: [stated] for the plot description, [measured] for my readings and computations.

---

#### [F] F-55 | §10.3-6 | §10.3 item 6: Ballotpedia prints "0.004%" but 734 / 150,010 = 0.49%; "the 660 elections" and "734" without reconciling (line 278)
MARK: confirmed
SOURCE: https://ballotpedia.org/Races_decided_by_10_votes_or_fewer (local: ballotpedia10.html, the saved page; tag-stripped text work-F/ballotpedia10.plain.txt) ; see F-49, F-50
QUOTE[work-F/ballotpedia10.plain.txt]: "Since 2018, out of 150,010 elections in Ballotpedia's coverage scope, there were 734 elections decided by 10 or fewer votes (0.004%)."
QUOTE[work-F/ballotpedia10.plain.txt]: "The chart below shows how many of the 660 elections were decided by each vote margin and the winners by political party."
NOTE: Item 6 is right as stated. Additions from F-44, F-47 and F-52: the page's "496 fewer than five" and "734" also disagree with its own table (352 and 733), and the largest total is 393,922, not 23,525.

#### [F] F-56 | §10.3-7 | §10.3 item 7: Farber average election size "50 to 75 eligible voters" (Sec. 1.2) versus "from 24 to 30" (Sec. 6.2) (line 279)
MARK: corrected
SOURCE: https://www.nber.org/system/files/working_papers/w16160/w16160.pdf (local: farber.txt) ; see F-35 to F-37
QUOTE[farber.txt]: "First, these elections are relatively small, averaging 50 to 75 eligible voters (figure 1), so that a worker’s vote has a reasonable probability of being pivotal."
QUOTE[farber.txt]: "The average number of eligible voters increased from 24 to 30 between 1972 and 2008."
CORRECTION: "(Sec. 1.2)" -> Sec. 2.3 (printed p.10) for "50 to 75"; "Sec. 6.2" for "24 to 30" is right.
NOTE: Both statements are in the paper as printed and are not reconciled in words. [inferred] They are means over different sets (all NLRB elections in Fig. 1 versus the 2-200-voter estimation sample, mean 26.75 [measured]); see F-37.

## Fill items (the first pass's unread list and open questions)

*Each reader's task file named fill items; here they are by reader. A block marked unread says why.*

### Fill items, reader A

#### [A] F-1 | Mebane, Baltz & Vasselai (2019), "Using agent-based models to simulate strategic behavior in elections": plurality pivot-probability formulas
MARK: confirmed (found and read at the author's page; formulas read on the page images)
SOURCE: https://websites.umich.edu/~wmebane/pm19.pdf (local: A_mebane2019.raw.txt, A_mebane2019.txt; downloaded by curl, saved as SP/r4/src/A_mebane2019.out) ; Sec. 2.3 "Pivotal Probabilities", eqs. (3)-(7), printed pp. 7-9; Sec. 2.4, eqs. (8)-(10), printed pp. 9-10 (page images PDF pp. 9-12)
URL found by WebSearch (for the URL only). It is Walter Mebane's page at the University of Michigan; the file is the conference paper "Prepared for presentation at the PolMeth XXXVI, Massachusetts Institute of Technology, Cambridge, MA July 18-20, 2019", dated July 10, 2019, 49 pages. This is the version Baltz cites ("Presented at the 2019 meeting of the Society for Political Methodology"), as a conference paper, not a journal article; it has not been peer-reviewed as far as the file shows.
QUOTE[A_mebane2019.raw.txt]: "Prepared for presentation at the PolMeth XXXVI, Massachusetts Institute of Technology, Cam-"
QUOTE[A_mebane2019.raw.txt]: "Elector i assumes Ne is a Poisson distributed random variable with"
QUOTE[A_mebane2019.raw.txt]: "will take certain actions: for candidate h ∈ {1, . . . , H}, it learns the proportion ph of voters"
QUOTE[A_mebane2019.raw.txt]: "where Iz (·) is a Bessel function of the first kind. S(·) is the Skellam distribution (Skellam"
QUOTE[A_mebane2019.raw.txt]: "based on an imagined electorate that does not include its own vote."
QUOTE[A_mebane2019.raw.txt]: "In words, the probability that it casts a pivotal vote is the probability that it breaks or"
QUOTE[A_mebane2019.raw.txt]: "creates a tie times the probability that party h is at least in second place.5 We can define"
QUOTE[A_mebane2019.raw.txt]: "Three-way ties are ignored."
QUOTE[A_mebane2019.raw.txt]: "To combine strategic abstention with wasted vote logic we let there be several parties—not"
NOTE: formulas are in FORMULAS AS PRINTED (F-1). What the paper says and does not say: (a) It is a *known-shares* model: each elector learns the proportion p_h of voters that are going to cast a vote for h (quoted just below; eq. 4 context); there is no uncertainty over p inside the formula (the p_h come from an iterated "poll" in the ABM). So, unlike Myatt & Fisher, there is no f(p); the Skellam probabilities S(0; μ̃_h, μ̃_j) are exponentially small in μ unless p_h = p_j. (b) The multi-party case ignores three-way ties by assumption (footnote 5, printed p. 9: "Three-way ties are ignored."), the same simplification M&F justify asymptotically. (c) Each elector evaluates pivotal probabilities "based on an imagined electorate that does not include its own vote", using μ̃_h = p_h(μ − 1). (d) The pivot event counted is "breaks a tie" (difference 0) plus "creates a tie" (difference −1), both with full weight in P_jh = α1 + α2 (eq. 9c); the expected benefit (9b) multiplies by (u_j − u_h) with no factor 1/2, whereas eqs. (8a)-(8b), which give vote-j versus abstain with random tie-breaking, imply by my algebra E_jh − E_∅jh = (α1 + α2)(u_j − u_h)/2 [measured by hand: α1[u_j − (u_j+u_h)/2] + α2[(u_j+u_h)/2 − u_h]]. That is, (9b) as printed is 2x the difference of (8a) and (8b); [inferred] it is a constant-factor slip or an unstated convention, with no effect on who is pivotal relative to whom. (e) The paper states no order in n for any pivot probability; Poisson mean μ enters only through μ̃ = p(μ − 1). (f) It cites Myerson (1998, 2000) for the Poisson framework ("number is known only to be drawn from a Poisson distribution (Myerson 1998, 2000) which simplifies computing pivotal probabilities") and Cox (1994).
QUOTE[A_mebane2019.raw.txt]: "number is known only to be drawn from a Poisson distribution (Myerson 1998, 2000) which"

#### [A] F-2a | Myerson (1998), "Population uncertainty and Poisson games", Int. J. Game Theory 27: definition of a pivot event under Poisson uncertainty; magnitude; order of two-way versus three-way ties
MARK: unread (full text); bibliographic data corrected from a record I did read
SOURCE: https://econpapers.repec.org/RePEc:spr:jogath:v:27:y:1998:i:3:p:375-392 (local: A_econpapers_spr_jogath_v_27_y_1998_i_3_p_375-392.txt) ; RePEc bibliographic record and abstract (not the paper)
QUOTE[A_econpapers_spr_jogath_v_27_y_1998_i_3_p_375-392.txt]: "International Journal of Game Theory , 1998, vol. 27, issue 3, 375-392"
QUOTE[A_econpapers_spr_jogath_v_27_y_1998_i_3_p_375-392.txt]: "An example of a large voting game is discussed, to illustrate the advantages of using a Poisson game model for large games."
QUOTE[A_econpapers_spr_jogath_v_27_y_1998_i_3_p_375-392.txt]: "Access to the full text of the articles in this series is restricted"
CORRECTION: pages "385-392" (first pass, taken from Baltz's reference list: "International Journal of Game Theory, 27:385–392") -> **375-392** per the RePEc record (issue 3). Bouton's reference list (local `bouton.raw.txt`) cites a page 377 of this paper ("see Myerson 1998, p377, for more detail"), which is inside 375-392 and outside 385-392. [inferred] Baltz's "385" is a typo for 375.
NOTE: UNREAD reason: the Springer full text is restricted (RePEc: "Access to the full text of the articles in this series is restricted"; link.springer.com is another task's host); the author's copy: Myerson's page home.uchicago.edu failed TLS verification through the sandbox proxy ("unable to get local issuer certificate"; curl exit 60; the CONNECT succeeded and the TLS alert was "unknown CA"); I did not disable verification. The Northwestern CMS-EMS discussion-paper copy (DP 1102R, Sept 1994, "Population Uncertainty and Poisson Games", http://www.kellogg.northwestern.edu/research/math/papers/1102.pdf) returned HTTP 500 ("The page cannot be displayed because an internal server error has occurred") for the same-structure DP 1189 URL; I stopped at that host after one request (DP 1102.pdf itself not requested). WebFetch of Myerson's home page was possible but listed no PDF links, and the directory page is blocked to it by robots.txt (not circumvented). See NEED-FETCH.
What the abstract (which I did read) does say: "A general class of models is developed for analyzing games with population uncertainty... a special class of Poisson games is defined. It is shown that Poisson games are uniquely characterized by properties of independent actions and environmental equivalence." (RePEc abstract of the journal article, in the local file A_econpapers_spr_jogath_v_27_y_1998_i_3_p_375-392.txt.)

#### [A] F-2b | Myerson (2000), "Large Poisson Games", J. Econ. Theory: pivot event; magnitude; orders of ties
MARK: unread at source; read second-hand through Bouton's draft (local file `bouton`), which states Myerson's results (flagged as a different source)
SOURCE: (paper itself) not read. Record: https://econpapers.repec.org/RePEc:eee:jetheo:v:94:y:2000:i:1:p:7-45 (local: A_econpapers_eee_jetheo_v_94_y_2000_i_1_p_7-45.txt). ScienceDirect full text: https://www.sciencedirect.com/science/article/pii/S002205319892453X returned HTTP 403 with a captcha page ("Are you a robot"): unread, not circumvented. Second-hand: Bouton's author draft (https://economics.sas.upenn.edu/sites/default/files/filevault/event_papers/Runoff.pdf; local: bouton.raw.txt), Appendix A1, printed p. 37-38 (page image PDF p. 39). Bouton's draft is task B's file; I read only Appendix A1 and quote it as a pointer to what Myerson (2000) proves.
QUOTE[A_econpapers_eee_jetheo_v_94_y_2000_i_1_p_7-45.txt]: "Journal of Economic Theory , 2000, vol. 94, issue 1, 7-45"
QUOTE[bouton.raw.txt]: "Together, Properties 1 and 2 have been called the magnitude theorem by Myerson (2000). The"
QUOTE[bouton.raw.txt]: "That is, the probability that event E occurs is exponentially decreasing in n: mag (E ) 2 [ 1; 0] is called"
QUOTE[bouton.raw.txt]: "Myerson (2000, Corollary 1) shows that:"
QUOTE[bouton.raw.txt]: "Theorem 2 in Myerson 2000 shows that two events that di¤er only by a small number of votes, as do pivP2 Q"
NOTE ([stated via Bouton, not by Myerson]): Bouton's Property 1 ("As shown by Myerson (2000, Theorem 1)") for a Poisson population of mean n: mag(E) ≡ lim_{n→∞} log[Pr(E)]/n = max_{x∈E} Σ_ψ (x_ψ/n)(1 − log(x_ψ/(nτ_ψ))) − 1, where x_ψ are the action counts in E and τ_ψ the rates defined in Bouton's draft (not reproduced here), and mag(E) ∈ [−1, 0] ("the probability that event E occurs is exponentially decreasing in n"). Property 2 (Myerson 2000, Corollary 1): mag(E) < mag(E') implies Pr(E)/Pr(E') → 0. Footnote 48 (Theorem 2): events differing "only by a small number of votes" (e.g. a tie and a one-vote lead) have the same magnitude. Bouton's Lemma 2: the magnitude of a two-candidate tie is −(√τ_P² − √τ_Q²)², which is 0 exactly when the two expected shares are equal. [inferred] So the magnitude notion (exponential rate) separates events by exponential speed and, by itself, does not give a polynomial order such as 1/n versus 1/n² for ties whose expected shares are equal (both have magnitude 0); in what I could read, neither Myerson nor Bouton states "two-way tie ~ 1/n, three-way tie ~ 1/n²". The definition of a pivot event under Poisson uncertainty is in Myerson's text (unread); in Bouton it is the event that P trails Q by exactly one vote (or ties, by the tie-break), within round 2 (Sec. 3.1). Mebane et al. (F-1) define it as breaking or creating a tie (eq. 6/7).

#### [A] F-2c | Myerson & Weber (1993), "A theory of voting equilibria", APSR
MARK: unread (full text); bibliographic data confirmed from RePEc
SOURCE: https://econpapers.repec.org/RePEc:cup:apsrev:v:87:y:1993:i:01:p:102-114_09 (local: A_econpapers_cup_apsrev_v_87_y_1993_i_01_p_102-114_09.txt) ; record and abstract only
QUOTE[A_econpapers_cup_apsrev_v_87_y_1993_i_01_p_102-114_09.txt]: "American Political Science Review , 1993, vol. 87, issue 1, 102-114"
QUOTE[A_econpapers_cup_apsrev_v_87_y_1993_i_01_p_102-114_09.txt]: "We compare equilibria under the plurality rule, approval voting, and the Borda system."
NOTE: UNREAD reason: full text is at cambridge.org / jstor.org, hosts held by other tasks ("not cambridge.org, not jstor.org"); not requested. The first pass gave no volume or pages: APSR 87(1): 102-114 (1993). What Myatt & Fisher (read raw) and Myatt (2004 DP) say *about* it: Myerson & Weber "describe models in which there is a probability distribution of preferences which is commonly known by voters"; M&F: "Palfrey (1989), Cox (1994) and Myerson & Weber (1993) describe models in which there is a probability distribution of preferences which is commonly known by voters, and individual voter preferences are drawn independently from that distribution." (M&F p. 2). The M&F text on this: [stated] "Statistical theory also shows us that the probability of a pivotal event involving the leading two candidates is infinitely larger than the probability of a pivotal event involving any other pair of parties." (M&F p. 3, for the known-p case).
QUOTE[myatt_fisher.raw.txt]: "Palfrey (1989), Cox (1994) and Myerson & Weber (1993) describe models in which there is a probability distribution of preferences which is commonly known by voters, and individual voter preferences are drawn independently from that distribution."
QUOTE[myatt_fisher.raw.txt]: "shows us that the probability of a pivotal event involving the leading two candidates is infinitely"

#### [A] F-3a | Cox (1994), APSR 88(3):608-621: the "M + 1 rule" and which candidates' votes can be pivotal
MARK: unread (full text); abstract read at an indexing record; M + 1 rule confirmed as stated in the abstract and by two papers that read it
SOURCE: https://econpapers.repec.org/RePEc:cup:apsrev:v:88:y:1994:i:03:p:608-621_09 (local: A_econpapers_cup_apsrev_v_88_y_1994_i_03_p_608-621_09.txt; the RePEc copy of the APSR abstract). Second-hand: Mebane, Baltz & Vasselai (2019) p. 6-7, https://websites.umich.edu/~wmebane/pm19.pdf (local: A_mebane2019.raw.txt); Myatt & Fisher (2002) p. 2-3 (local: myatt_fisher.raw.txt).
QUOTE[A_econpapers_cup_apsrev_v_88_y_1994_i_03_p_608-621_09.txt]: "What appear to be the most natural equilibria conform to the M + 1 rule, according to which strategic voting in M-seat districts produces exactly M + 1 vote-getting candidates in equilibrium, any others having their support totally undercut."
QUOTE[A_econpapers_cup_apsrev_v_88_y_1994_i_03_p_608-621_09.txt]: "Previous investigations of strategic voting equilibria in mass electorates have looked only at single-member districts. I shall investigate such equilibria in multimember districts operating under the single nontransferable vote system."
QUOTE[A_mebane2019.raw.txt]: "“Duvergerian” equilibria only the first loser (in M + 1-th place) receives a nonnegligible"
QUOTE[A_mebane2019.raw.txt]: "proportion of the votes while other losers get nothing, and with “non-Duvergerian”"
QUOTE[myatt_fisher.raw.txt]: "existence of non-Duvergerian equilibrium outcomes which involve a tie between the second and"
QUOTE[myatt_fisher.raw.txt]: "Instead of asking, “What are the chances of being pivotal?” as supposed by standard intuition,"
NOTE: The abstract says the M + 1 rule is about *equilibrium vote-getting candidates* in M-seat SNTV districts (title: "Strategic Voting Equilibria under the Single Nontransferable Vote"); the abstract does not itself say which candidates' votes are pivotal. For a single-seat plurality district (M = 1), M + 1 = 2 candidates get votes in the "Duvergerian" equilibria (Mebane et al.: "only the first loser (in M + 1-th place) receives a nonnegligible proportion of the votes while other losers get nothing"); non-Duvergerian equilibria have the losers tied at the first loser's share or at zero votes (Mebane et al., p. 7: "the losing alternatives have either the same positive proportion of votes as does the first loser or zero votes"). M&F p. 2-3 report Cox as highlighting equilibria "which involve a tie between the second and third placed candidates". Cox (1994) full text and Cox (1997) *Making Votes Count* ch. 7: unread (cambridge.org / book; not in my host list; no free full text found by search). [inferred] I do not state the pivotal-pair rule beyond what is quoted.

#### [A] F-3b | Cox (1997), Making Votes Count, ch. 7
MARK: unread
SOURCE: none. Book (Cambridge University Press); not searched beyond the title; no free copy found by the searches I ran; Myatt & Fisher quote one sentence of it ("A fourth condition necessary to generate pure local bipartism is that the identity of trailing and front-running candidates is common knowledge . . ."), which is in `myatt_fisher.raw.txt` (p. 4), second-hand.
QUOTE[myatt_fisher.raw.txt]: "“A fourth condition necessary to generate pure local bipartism is that the identity"
NOTE: no page for the Cox quote is given by M&F in the text I read (they cite "Cox (1997)" without page in the passage; Myatt DP 186 cites "Cox (1997, p. 78)" for the same condition: "Similarly, Cox (1997, p. 78) fully recognized that a 'condition necessary to generate" , local myatt2007wp).

#### [A] F-4a | Myatt (2007), "On the theory of strategic voting", Rev. Econ. Stud. 74(1): 255-281: statements on 1/n versus 1/sqrt(n)
MARK: confirmed in an earlier version (Oxford Economics Discussion Paper 186, March 2004, same title, same author); the journal article itself unread (full text restricted)
SOURCE: https://ora.ox.ac.uk/objects/uuid:00c4b09d-739b-49c8-b885-f6dfe4bfffd3/files/s12579s68h (local: A_myatt2007wp.raw.txt, A_myatt2007wp.txt; downloaded by curl, SP/r4/src/A_myatt2007wp.out). **This is a working-paper version (D. P. Myatt, "On the Theory of Strategic Voting", Oxford Dept of Economics DP No. 186, March 1, 2004), not the published RES text**; the page numbers below are the DP's printed pages. The RES record: https://econpapers.repec.org/RePEc:oup:restud:v:74:y:2007:i:1:p:255-281 (local: A_econpapers_oup_restud_v_74_y_2007_i_1_p_255-281.txt) gives "The Review of Economic Studies , 2007, vol. 74, issue 1, 255-281" and "Access to full text is restricted to subscribers."
QUOTE[A_myatt2007wp.raw.txt]: "Number 186"
QUOTE[A_myatt2007wp.raw.txt]: "March 2004"
QUOTE[A_myatt2007wp.raw.txt]: "As n → ∞, the probability q1 vanishes to zero. Its asymptotic properties are interesting,"
QUOTE[A_myatt2007wp.raw.txt]: "however; they are recorded in the following result, which represents a minor extension of"
QUOTE[A_myatt2007wp.raw.txt]: "Proposition 1 from Chamberlain and Rothschild (1981).40"
QUOTE[A_myatt2007wp.raw.txt]: "The observation that the probability of a tie, when p is unknown, is of order 1/n is due to Chamberlain"
QUOTE[A_myatt2007wp.raw.txt]: "and Rothschild (1981). When p is known, then the election"
QUOTE[A_myatt2007wp.raw.txt]: "Proposition 1 confirms that qj → 0 at a rate of"
QUOTE[A_myatt2007wp.raw.txt]: "Chamberlain and Rothschild (1981) were primarily concerned with the order of the probability of a tied"
QUOTE[A_econpapers_oup_restud_v_74_y_2007_i_1_p_255-281.txt]: "The Review of Economic Studies , 2007, vol. 74, issue 1, 255-281"
NOTE (as printed, DP 186, printed pp. 15-17; page images PDF pp. 17-18): [setting: plurality-rule election, a *disliked incumbent* and two challengers; the focal voter i = 0, n other voters; q1 = Pr[x = ⌈γn⌉] is the probability that candidate 1 ties the incumbent's fixed vote total; the binomial in the integrand is idiosyncratic uncertainty, f(p | δ) is "electoral" uncertainty about the support p.] Lemma 3: "the density f(p | δ) is continuous and strictly positive on (0, 1)", and q1 = ∫_0^1 C(n, ⌈γn⌉) [p^{γ_n}(1 − p)^{1−γ_n}]^n f(p | δ) dp. **Proposition 1** (printed p. 16; "a minor extension of Proposition 1 from Chamberlain and Rothschild (1981)"): lim_{n→∞} (n + 1) q1 = f(γ | δ), lim_{n→∞} (n + 1) q2 = f(1 − γ | δ), and lim q1/q2 = f(γ | δ)/f(1 − γ | δ). Sec. 3.5 (p. 17): "Proposition 1 confirms that q_j → 0 at a rate of 1/(n + 1) as n → ∞." Footnote 43 (p. 17), as printed: "The observation that the probability of a tie, when p is unknown, is of order 1/n is due to Chamberlain and Rothschild (1981). When p is known, then the election outcome is realization of a binomial random variable. For p = 1/2, the probability of a tie is of order 1/√n, and when p ≠ 1/2 it is of order exp(−cn) for some c > 0; see also Beck (1975) and Margolis (1977)." Footnote 40 (p. 16): "Chamberlain and Rothschild (1981) were primarily concerned with the order of the probability of a tied outcome as n → ∞; they noted that '[T]here have been to our knowledge few attempts to calculate the relevant probability. The calculations which we know of are neither general nor rigorous.' Their result was used by Mulligan and Hunter (2003) in their assessment of the empirical frequency of a pivotal vote." Footnote 41 (p. 16): Gelman, Katz and Tuerlinckx (2002, p. 429) "explained that idiosyncratic uncertainty is removed 'because the binomial variation from which it derives is minor compared to any realistic variation among the probabilities.'... They noted that this observation was also made by Good and Mayer (1975) and Margolis (1983)."
NOTE: This answers the 1/n-versus-1/√n question at one remove: (i) tie probability ~ 1/n when the share p is unknown (uncertain) with a continuous positive density, attributed to Chamberlain & Rothschild (1981); (ii) ~ 1/√n when p is known and exactly 1/2; (iii) exponentially small when p is known and ≠ 1/2. It is for a two-sided tie (candidate vs fixed incumbent total), not for the 3-way tie. The 1/n statement matches GKB 2004 A-16 and Myatt & Fisher Lemma 1 (A-06): all three agree on 1/n for a two-way tie under uncertainty about the share. [inferred] The constant is the density: Pr[tie] ≈ f(γ)/(n + 1); for two candidates with symmetric tie γ = 1/2 this is the p_v(0.5)/n of GKB 2004 (A-12), because ∫ C(n,k) p^k (1−p)^{n−k} dp = 1/(n + 1) exactly for every k.

#### [A] F-4b | Chamberlain & Rothschild (1981), "A note on the probability of casting a decisive vote", J. Econ. Theory 25(1): 152-162
MARK: unread (full text); bibliographic data confirmed; their results are known here only second-hand
SOURCE: https://econpapers.repec.org/RePEc:eee:jetheo:v:25:y:1981:i:1:p:152-162 (local: A_econpapers_eee_jetheo_v_25_y_1981_i_1_p_152-162.txt) ; record only (no abstract on the record)
QUOTE[A_econpapers_eee_jetheo_v_25_y_1981_i_1_p_152-162.txt]: "Journal of Economic Theory , 1981, vol. 25, issue 1, 152-162"
QUOTE[A_econpapers_eee_jetheo_v_25_y_1981_i_1_p_152-162.txt]: "Full text may be restricted for ScienceDirect subscribers"
NOTE: UNREAD reason: ScienceDirect is a bot check (HTTP 403, "Are you a robot", seen for a different Elsevier article on the same host; not retried for this one). Search listed `https://core.ac.uk/download/300456632.pdf` and `https://core.ac.uk/download/300459322.pdf` as results for this title; their content is unverified and core.ac.uk is another task's host: NEED-FETCH. Second-hand, read: GKB 2004 (A-16; "derive a 1/nj rule") and Myatt 2004 DP (above). The first pass's attribution "1/n versus 1/√n through Gelman et al." is confirmed as GKB's attribution: GKB 2004 Sec. 2.3 p. 663: "Good and Mayer and also Chamberlain and Rothchild derive a 1/nj rule ... This model arises by assuming that votes are binomially distributed, but with binomial probabilities p that themselves vary over the nj voters in a jurisdiction."

#### [A] F-4c | Good & Mayer (1975), "Estimating the efficacy of a vote", Behavioral Science 20: 25-33
MARK: unread
SOURCE: none read. Citation as printed in GKB 2004 fn. 23 and Myatt DP 186 reference list ("Good, I. J., and L. S. Mayer (1975): 'Estimating the Efficacy of a Vote,' Behavioral Science, 20, 25–33").
QUOTE[A_myatt2007wp.raw.txt]: "Good, I. J., and L. S. Mayer (1975): “Estimating the Efficacy of a Vote,” Behavioral"
NOTE: not searched beyond the bibliographic record (Wiley, paywalled). Myatt DP 186 fn. 41 reports that Gelman, Katz & Tuerlinckx say that the observation (idiosyncratic/binomial variation negligible) "was also made by Good and Mayer (1975) and Margolis (1983)". GKB 2004's own footnote 48 spells it "Good and Meyer".

#### [A] F-5 | Anything else the sources cite as *the* derivation of the plurality pivot probability for 3+ candidates
MARK: confirmed (what the sources I read cite); not read where marked
SOURCE: Myatt & Fisher (2002) Sec. 2.4 p. 10, Mebane et al. (2019) p. 7-9, Myatt DP 186 p. 16-17, GKB 2004 fn. 19 and 23, GKB 1998 Sec. 2.2.
QUOTE[myatt_fisher.raw.txt]: "McKelvey & Ordeshook (1972) specify a uniform distribution over X, whereas Hoffman (1982)"
QUOTE[gkb1998_columbia.raw.txt]: "Most of the literature to date on the effects of individual"
QUOTE[A_mebane2019.raw.txt]: "Demichelis and Dhillon (2010) and Cox (1994) assume that electorate sizes"
NOTE: Derivations that the sources I read point to for plurality pivot probabilities: (1) Myatt & Fisher (2002), Prop. 1 and Lemma 1 (A-05, A-06): for m ≥ 3 candidates with a continuous density f over the unknown shares, Pr[x] ≈ f(x/n)/n^{m−1}, with two-way ties of order 1/n and three-way ties of order 1/n^2; their Sec. 2.4 notes that earlier models put beliefs directly over outcomes: "McKelvey & Ordeshook (1972) specify a uniform distribution over X, whereas Hoffman (1982) considers a density with a Gaussian kernel." (both unread). (2) Chamberlain & Rothschild (1981) for the 1/n order (two-way tie, unknown p) (F-4; unread; via Myatt DP 186). (3) Myerson (1998, 2000) for Poisson-electorate pivot probabilities and the magnitude theorem (F-2; unread; via Bouton and Mebane et al.). (4) Mebane, Baltz & Vasselai (2019) eqs. (6)-(7), the Skellam formula for known shares with three-way ties ignored (F-1; read). (5) For pivot probabilities with fixed electorate size and multinomial votes: Cox (1994) and Demichelis & Dhillon (2010) per Mebane et al.: "Demichelis and Dhillon (2010) and Cox (1994) assume that electorate sizes are fixed and commonly known. This allows calculation of pivotal probabilities through exact combinatorial computation or multinomial assumptions." (unread). (6) Mulligan & Hunter (2003) NBER WP 8590 ("The Empirical Frequency of a Pivotal Vote"; cited by GKB 2004 fn. 35, and by Myatt DP 186 fn. 40): empirical frequency; nber.org is task F's host: NEED-FETCH `https://www.nber.org/papers/w8590` (URL not verified by me). (7) Margolis (1977, "Probability of a Tie Election", Public Choice 31) and Beck (1975) for the binomial/normal formula (GKB 1998 Sec. 5; unread).

---

### Fill items, reader B

#### [B] F-01 | Droop quota and how an STV count is done (transfers, surplus, exclusion)
MARK: confirmed from two electoral-authority sources read at source (Ireland's Electoral Commission; the Scottish Local Government Elections Order 2007), one academic paper, and ACE (WebFetch only)
SOURCE 1: https://www.electoralcommission.ie/irelands-voting-system/ (local: dl/eci_vs.clean.txt; curl 200) ; section "How your vote is counted" (the page is Ireland's rule, PR-STV)
QUOTE[dl/eci_vs.clean.txt]: "The quota is calculated by taking the (total number of valid ballot papers) dividing it by (the number of seats to be filled plus one) and then adding one."
QUOTE[dl/eci_vs.clean.txt]: "In the below example which is a four seat constituency, it is only possible for four candidates to reach the quota of 12,001 votes each, as this would only leave 11,996 votes left."
QUOTE[dl/eci_vs.clean.txt]: "Any candidate that reaches or exceeds the quota on the first count is deemed elected."
QUOTE[dl/eci_vs.clean.txt]: "A surplus is the number of votes a candidate has over the quota."
QUOTE[dl/eci_vs.clean.txt]: "If there is no surplus available or the distribution of a surplus is not allowed, the lowest candidate(s) is/are excluded and their votes distributed to the remaining candidates."
QUOTE[dl/eci_vs.clean.txt]: "When a candidate’s surplus is distributed or a candidate is excluded, their votes are redistributed. Any preference for candidates who have already been elected or have been excluded are ignored. The next available preference on the ballot paper is used."
SOURCE 1b: https://www.electoralcommission.ie/glossary-of-electoral-terms/ (local: dl/eci_gloss.clean.txt; curl 200)
QUOTE[dl/eci_gloss.clean.txt]: "The quota is calculated by dividing the total valid poll by 1 more than the number of available seats and then adding 1."
SOURCE 2 (the rules the Scottish data of McCune & Graham-Squire were counted under): The Scottish Local Government Elections Order 2007 (SSI 2007/42), Schedule 1, rules 46-52, as made 9 February 2007. https://www.legislation.gov.uk/ssi/2007/42/pdfs/ssi_20070042_en.pdf (local: dl/ssi2007_42.txt; curl 200, 72 pages) ; this is the Order as made; I did not check whether later Orders (e.g. SSI 2011/399, which the search also returned) changed the count rules.
QUOTE[dl/ssi2007_42.txt]: "The returning officer shall divide the total number of valid ballot papers for the electoral ward by a number exceeding by one the number of councillors to be elected at the election for that electoral ward."
QUOTE[dl/ssi2007_42.txt]: "The result of the division under paragraph (1) (ignoring any decimal places), increased by one, is the number of votes needed to secure the return of a candidate as a councillor (in these rules referred to as the “quota”)."
QUOTE[dl/ssi2007_42.txt]: "Where, at any stage of the count, the number of votes for a candidate equals or exceeds the quota, the candidate is deemed to be elected."
QUOTE[dl/ssi2007_42.txt]: "the returning officer shall exclude from the election at that stage the candidate with the then lowest number of votes."
QUOTE[dl/ssi2007_42.txt]: "Where the number of continuing candidates is equal to the number of vacancies remaining unfilled, the continuing candidates are deemed to be elected."
NOTE: [stated] Scottish rule 48(3) (transfer of a surplus): "The vote on each ballot paper transferred under paragraph (2) shall have a value (“the transfer value”) calculated as follows– A divided by B", where A = "the surplus of the transferring candidate" multiplied by "the value of the ballot paper when received by that candidate" and B = "the total number of votes credited to that candidate", "the calculation being made to five decimal places (any remainder being ignored)" (rule 48(3)); excluded candidates' papers go on at the value they had (rule 50(4)); if surpluses of two or more candidates exist, the highest is transferred first (rule 49(1)); ties are broken by the earlier count and then by lot (rules 49(2)-(3), 51). Quota formula in symbols as the Order words it: q = floor(V/(S+1)) + 1, with V valid ballot papers and S seats ("ignoring any decimal places, increased by one"); Ireland's page words it the same way without stating the rounding. A candidate "equals or exceeds" the quota is elected (rule 47).
SOURCE 3: Laird et al. (laird.raw.txt) prints a different convention: "In this paper, we will use the Droop quota, q, where q = ⌈ available" / "total votes" / "seats+1 ⌉" (the page image pdf p. 3 shows q = ⌈ total votes / (available seats + 1) ⌉, a ceiling, and the sentence above calls it "A vote threshold that a candidate needs to exceed to be elected").
QUOTE[laird.raw.txt]: "In this paper, we will use the Droop quota, q, where q = ⌈ available"
QUOTE[laird.raw.txt]: "(2) If any candidate meets the quota, they are elected, and their surplus votes"
NOTE: [measured] the two conventions differ whenever V is divisible by S+1: Ireland's example has V = 60,000 and S = 4 (12,001 = 60,000/5 + 1) where the ceiling form gives 12,000; in the Scottish form (floor + 1) any V gives a whole-number quota. Laird et al. also say surplus votes "are redistributed proportionally based on voters' next most preferred candidates" and, if no candidate meets the quota, "the candidate with the fewest first-place votes is eliminated". All three agree on the structure: quota from V and S, election at the quota, surplus transferred at a fractional value, elimination of the lowest when nobody has a quota, repeat until S are elected (Laird step (4): "This process is repeated until the required number of candidates has been elected.").
SOURCE 4 (WebFetch only; ACE, curl returned 404 for the same pages): https://aceproject.org/main/english/es/esf04.htm, a page about STV on the ACE Electoral Knowledge Network. WEBFETCH-EXTRACT: "The quota is calculated by the simple formula:" followed by a printed formula the extractor read as Quota = votes / (seats + 1) + 1 (a fraction line, "votes" over "seats + 1", then "+ 1"); "Any candidate who has more first preferences than the quota is immediately elected."; surplus: "all the candidate's ballot papers are redistributed, but each at a fractional percentage of one vote". I could not read the formula or the wording on the page itself; the extractor says the page does not mention rounding. The extractor did not find a page title.
NOTE (general): [stated] ACE has the quota as "+1"; the Irish and Scottish sources agree; Laird's ceiling differs.

#### [B] F-02 | Bouton (AER 2013) journal version and Bouton & Gratton: open copies; closed forms
MARK: Bouton AER text: unread (no open copy found); Bouton & Gratton (Theoretical Economics 2015): read in full text (open access); closed forms found in both
SOURCE A: the AER article is behind the AEA paywall: https://econpapers.repec.org/RePEc:aea:aecrev:v:103:y:2013:i:4:p:1248-88 says "Access to full text is restricted to AEA members and institutional subscribers." (local: dl/econpapers_aer.clean.txt). Open working-paper versions found by search, not read: Boston University WP2012-001 (http://people.bu.edu/lbouton/Runoff.pdf, shown as 404 by EconPapers' own link check); ULB ECARES 2013/160854 (no download). The Penn draft (bouton.txt) is the version I read.
QUOTE[dl/econpapers_aer.clean.txt]: "Access to full text is restricted to AEA members and institutional subscribers."
SOURCE B: Bouton & Gratton, "Majority runoff elections: Strategic voting and Duverger's hypothesis", Theoretical Economics 10 (2015), 283-314, DOI 10.3982/TE1642. https://econtheory.org/ojs/index.php/te/article/viewFile/20150283/13015/381 (redirects to https://www.econometricsociety.org/publications/theoretical-economics/2015/05/27/Majority-runoff-elections-strategic-voting-and-Duvergers-hypothesis/file/1642-13015-1-PB.pdf; curl 200, 32 pages) (local: dl/bg_te.txt, dl/bg_te.raw.txt). The journal is open access: "Licensed under the Creative Commons Attribution-NonCommercial License 3.0."
QUOTE[dl/bg_te.txt]: "Theoretical Economics 10 (2015), 283–314"
QUOTE[dl/bg_te.txt]: "Licensed under the Creative Commons Attribution-NonCommercial License 3.0."
QUOTE[dl/bg_te.txt]: "This paragraph and Section 3.1 are based on similar sections in Bouton (2013)."
QUOTE[dl/bg_te.txt]: "As proven in Bouton (2013), the magnitude of a pivotal event piv is larger when the expected outcome of the first round, τ, is close to the conditions necessary"
QUOTE[dl/bg_te.txt]: "Lemma 3. The magnitudes of the pivot probabilities are the following:"
NOTE: [stated] This paper is the majority-runoff (threshold 1/2) special case with general preference intensities; it relabels candidates R (front-runner), S, W. Its Appendix A restates the magnitude definition (printed p. 305: "μ(E) ≡ lim_{n→∞} log[Pr(E)]/n = max_{x∈E} Σ_i (x_i/n)(1 − log(x_i/(nτ_i))) − 1", μ in [−1, 0]) and Lemma 3 (pp. 305-306) with closed-form magnitudes (see FORMULAS AS PRINTED). So, answering the first pass's "constants not given": the exponents DO have a closed form in both papers. Neither paper gives the probability itself, only the exponent. B&G's Table 1 (first-round pivotal events) has three rows, not four: it drops the above-threshold event, because with threshold 1/2 two candidates cannot both be above it. Its threshold event reads "x_i + 1/2 > 1/2 (x_i + x_j + x_k) ≥ x_i ≥ x_j ≥ x_k", which is the draft's Table 1 with ζ = 1/2 (page image pdf p. 9 not rendered; read from the layout text, with the radicals/fractions as extracted: "xi + 12 > 12 (xi + xj + xk ) ≥ xi ≥ xj ≥ xk").
QUOTE[dl/bg_te.txt]: "Threshold pivotal i/ij piv i/ ij xi + 12 > 12 (xi + xj + xk ) ≥ xi ≥ xj ≥ xk"
[measured] I recomputed the draft's Table 2 from the draft's Lemma 3 (eqs. 17 and 19, transcribed from the page images) for ζ = 0.5, τ_A = 0.30, τ_B = 0.26, τ_C = 0.44: A/AC = −0.0835, B/BC = −0.1227, CA/CB = −0.0014, BA/BC = −0.0251, AB/AC = −0.0251, matching all five printed values of Table 2 (python3). This confirms both the transcription of Lemma 3 and the table. Also B&G Lemma 3(a) at ζ = 1/2: the draft's first case reduces to 2√((τ_j+τ_k)τ_i) − 1, which is what B&G print.

#### [B] F-03 | Any published estimate of a decisive-vote probability in a real two-round or STV election
MARK: none found
SOURCE: searches (WebSearch, URLs only), with what I read:
 (1) "estimate probability of being pivotal voter two-round runoff election empirical estimate presidential election first round second round": results were Baltz (IRV simulation, task E's), Gelman/King on US general elections (not runoff), a Konstanz paper "How to poll runoff elections" (Selb, Göbel, Lachat 2020, Public Opinion Quarterly 84(3) 776-787; I downloaded the open copy from kops.uni-konstanz.de, 10 pages, and searched the text: the words "pivot" and "decisive" do not occur: no estimate), a Kellogg page on estimating a model of large elections (not read; Japan/US elections, not runoff), others not relevant.
 (2) "probability a single vote is pivotal single transferable vote election estimate Ireland STV pivotal probability": results were Baltz again, a GESIS/SSOAR record (Anubis bot check page, 200 with a challenge: unread, not circumvented; its data.gesis.org record returned 404) and Voting Matters pages (Issue 6 P3 read: "Is STV a form of PR?" by Kestelman, not about pivot probabilities; Issue 5 P3 reset the connection: unread).
 (3) "pivotal probability estimated French presidential election two-round ... strategic voting empirical": results not about pivot-probability estimates (a Substack, conference abstracts, SIOE paper on French municipal elections not opened).
 (4) "simulation probability of a decisive ballot multiwinner STV election pivotal Scottish OR Irish OR Maltese ...": results were "Multiwinner Elections and the Spoiler Effect" (arXiv 2403.03228, about the spoiler effect, not pivot probability; arXiv is task E's host: not read) and Baltz.
NOTE: [inferred] I found no estimate for a real two-round or STV election, only Bouton's exponents (B-13) and Baltz's IRV simulation. The two France data points in B-14 to B-18 (a gap of 194,600 votes in 2002 and 421,308 in 2022 among 28.5 and 35.1 million suffrages exprimés) and the Australian Senate case (B-41) are data on margins, not probabilities. Baltz (arXiv 2210.01657, Political Analysis) is the IRV paper and belongs to task E.

#### [B] F-04 | ACE Electoral Knowledge Network: what a runoff is; thresholds (50%+1 etc.)
MARK: confirmed for thresholds from primary sources (France's Conseil constitutionnel decisions; Bouton's introduction); ACE itself read only through WebFetch (curl got site errors/404 from ACE)
SOURCE (WebFetch only): https://aceproject.org/main/english/es/esi01b.htm, an ACE page on presidential elections and the two-round system. WEBFETCH-EXTRACT: second round needed "if no one candidate wins a majority on the first round"; variants "between the top two candidates (majority-runoff)" and "between more than two candidates (majority-plurality)"; "In Costa Rica a candidate can win on the first round with only forty percent of the vote"; "in Sierra Leone a second round is only avoided if one candidate gets fifty-five percent in the first"; Argentina: "a successful candidate must poll forty-five percent" or "forty percent plus more than a ten percent lead over the second-placed candidate." The extractor says the page states no general "50% plus one" rule and gave no title. I could not read the page itself (curl: 404 "Resource not found" on the legacy path; the "ace-en" paths returned 503/404 with an error page).
SOURCE (read): Bouton draft, introduction, which says the same about thresholds from its own citations: "In practice, thresholds below 50% are far from exceptional. For instance, the threshold is 40% in Costa Rica, North Carolina State and New York City." and "in Argentina, for example, a candidate wins outright if she gains 45% of the votes or if she gains 40% of the votes as well as 10% more than the runner-up." and, in a footnote, "Thresholds above 50% are more rare: the only case I am aware of is the 1996 presidential election in Sierra Leone, for which the threshold was de…ned at 55%."
QUOTE[bouton.txt]: "In practice, thresholds below 50% are far from exceptional. For instance, the threshold is 40% in Costa Rica, North Carolina State and New York City."
QUOTE[bouton.txt]: "in Argentina, for example, a candidate wins outright if she gains 45% of the votes or if she gains 40% of the votes as well as 10% more than the runner-up."
QUOTE[bouton.txt]: "Thresholds above 50% are more rare: the only case I am aware of is the 1996 presidential election in Sierra Leone, for which the threshold was de…ned at 55%."
QUOTE[bouton.txt]: "In a runo¤ election, the candidate with the greatest number of votes wins outright in the …rst round if she obtains more than a prede…ned fraction of the votes (called the threshold for …rst-round victory)."
SOURCE (read): France: the Conseil constitutionnel's decisions 2002-109 PDR and 2022-195 PDR: absolute majority of suffrages exprimés, and a second round if none:
QUOTE[dl/cc2002.clean.txt]: "Considérant qu'aucun candidat n'a recueilli la majorité absolue des suffrages exprimés au premier tout de scrutin,"
QUOTE[dl/cc2022.clean.txt]: "Aucun candidat n'a recueilli la majorité absolue des suffrages exprimés au premier tour de scrutin."
QUOTE[dl/cc2002.clean.txt]: "Majorité absolue .................... 14 249 236"
QUOTE[dl/cc2022.clean.txt]: "Majorité absolue : 17 566 474"
NOTE: [measured] absolute majority = half of the suffrages exprimés rounded up: 28,498,471 / 2 = 14,249,235.5 -> 14,249,236; 35,132,947 / 2 = 17,566,473.5 -> 17,566,474. [stated] The 2002 decision prints "premier tout de scrutin" (a typo for "tour") in the Conseil's own text; the quote is as printed.

---

### Fill items, reader C

#### [C] F-1 | IDEA electoral-system design handbook: PR formulas (D'Hondt, Sainte-Laguë, modified Sainte-Laguë, Hare/largest remainder, Droop), thresholds in practice, list types, as printed
MARK: confirmed (for what the Handbook prints); modified Sainte-Laguë: not in this Handbook (searched for "modified" and "1.4": only "Modified Borda Count" and unrelated hits) -> unread
SOURCE: https://www.idea.int/sites/default/files/publications/electoral-system-design-the-new-international-idea-handbook.pdf (local: work-C/idea_handbook.txt (pdftotext -layout) and work-C/idea_handbook.raw.txt; downloaded by curl from the catalogue page https://www.idea.int/publications/catalogue/electoral-system-design-new-international-idea-handbook; 237 pages; "Electoral System Design: The New International IDEA Handbook" by Andrew Reynolds, Ben Reilly and Andrew Ellis, "© International Institute for Democracy and Electoral Assistance 2005, Reprinted 2008", ISBN 91-85391-18-2; the case studies stop at 2004-2005) ; Glossary, printed pp. 176-181 (PDF pp. 190-195); "The Threshold" paragraphs 119-121, printed p. 83 (PDF p. 97); "Open, Closed and Free Lists" paragraphs 122-125, printed pp. 83-84; List PR paragraph 106, printed p. 59-60; MMP threshold, printed p. 102 (PDF p. 116)
QUOTE[work-C/idea_handbook.txt]: "D’Hondt Formula – One of the options for the series of divisors used to distribute seats in List PR systems which adopt the Highest Average Method. The votes of a party or grouping are divided successively by 1, 2, 3... as seats are allocated to it."
QUOTE[work-C/idea_handbook.txt]: "Sainte-Laguë Formula – one of the options for the series of divisors used to distribute seats in List PR systems which adopt the Highest Average Method. The votes of a party or grouping are divided successively by 1, 3, 5... as seats are allocated to it."
QUOTE[work-C/idea_handbook.txt]: "Highest Average Method – A principle for converting votes into seats in List PR systems. One seat is allocated in a district at each of a series of counts to the party or grouping with the highest vote total."
QUOTE[work-C/idea_handbook.txt]: "The most common series of divisors used are D’Hondt and Sainte-Laguë. The Highest Average Method tends to be more favourable to larger parties than its alternative, the Largest Remainder Method."
QUOTE[work-C/idea_handbook.txt]: "Largest Remainder Method – A principle for converting votes into seats in List PR systems. After parties and groupings have been allocated seats in an electoral district because they have received full quotas (a) of votes, some seats will be unfilled, and some votes remain—for each party, less than a full quota (a). The remaining seats are then awarded to parties and groupings in order of the number of left-over votes they possess."
QUOTE[work-C/idea_handbook.txt]: "Hare Quota – A variant of quota used in proportional representation systems which use the Largest Remainder Method, defined as the total valid vote divided by the number of seats to be filled in the electoral district."
QUOTE[work-C/idea_handbook.txt]: "Droop Quota – A variant of quota used in proportional representation systems which use the Largest Remainder Method, defined as the total valid vote divided by the number of seats to be filled in the electoral district plus one. Also known as Hagenbach-Bischoff Quota."
QUOTE[work-C/idea_handbook.txt]: "Imperiali Quota – A variant of quota used in proportional representation systems which use the Largest Remainder Method, defined as the total valid vote divided by the number of seats to be filled in the electoral district plus two."
QUOTE[work-C/idea_handbook.txt]: "© International Institute for Democracy and Electoral Assistance 2005"
QUOTE[work-C/idea_handbook.txt]: "allocation of seats after the votes have been counted can be either a Highest Average or a Largest Remainder Method (see the glossary at annex B)."
QUOTE[work-C/idea_handbook.txt]: "The formula chosen has a small but sometimes critical effect on the outcomes of elections under PR. In Cambodia in 1998, a change in the formula a few weeks before polling day turned out to have the effect of giving the largest party 64 seats, instead of 59, in a 121-seat National Assembly."
QUOTE[work-C/idea_handbook.txt]: "119. All electoral systems have thresholds of representation: that is, the minimum level of support which a party needs to gain representation. Thresholds can be legally imposed (formal thresholds) or exist as a mathematical property of the electoral system (effective or natural thresholds)."
QUOTE[work-C/idea_handbook.txt]: "Elsewhere, legal thresholds range from 0.67 per cent in the Netherlands to 10 per cent in Turkey."
QUOTE[work-C/idea_handbook.txt]: "A striking example of this was the 2002 Turkish election, in which so many parties failed to clear the 10 per cent threshold that 46 per cent of all votes were wasted."
QUOTE[work-C/idea_handbook.txt]: "In all these cases the existence of a formal threshold tends to increase the overall level of disproportionality, because votes for those parties which would otherwise have gained representation are wasted."
QUOTE[work-C/idea_handbook.txt]: "In Poland in 1993, even with a comparatively low threshold of 5 per cent for parties and 8 per cent for coalitions, over 34 per cent of the votes were cast for parties and coalitions which did not surmount it."
QUOTE[work-C/idea_handbook.txt]: "121. An effective, hidden or natural threshold is created as a mathematical by-product of features of electoral systems, of which district magnitude is the most important."
QUOTE[work-C/idea_handbook.txt]: "123. The majority of List PR systems in the world are closed, meaning that the order of candidates elected by that list is fixed by the party itself, and voters are not able to express a preference for a particular candidate."
QUOTE[work-C/idea_handbook.txt]: "124. Many List PR systems in Western Europe use open lists, in which voters can indicate not just their favoured party but their favoured candidate within that party."
QUOTE[work-C/idea_handbook.txt]: "Finland, contrary to Brazil (see case study) where voters may either cast their vote for a candidate or for a political party, voters must vote for candidates: the number of seats received by each party is determined by the total number of votes gained by its candidates, and the order in which the party’s candidates are elected to these seats is determined by the number of individual votes they receive."
NOTE: [stated] (1) The Handbook prints the divisor series in words only ("divided successively by 1, 2, 3..." for D'Hondt; "1, 3, 5..." for Sainte-Laguë), and the quotas in words (votes / seats for Hare; / (seats + 1) for Droop in the glossary; / (seats + 2) for Imperiali), not as formulas. The only printed formula in the sections I read is the STV Droop formula in F-2/FORMULAS (image checked, printed p. 76). (2) It has no "modified Sainte-Laguë" (the 1.4 first divisor) entry and does not discuss monotonicity (grep "monoton" finds nothing). (3) The glossary's Hare quota says "Also known as Hare-Niemeyer". (4) Mexico: "uses the pure Sainte-Laguë Method" for apportioning FPTP seats among states (not for votes-to-seats in a party list). (5) "Finland ... voters must vote for candidates" agrees with L&T's description of the Finnish ballot (C-24). (6) IDEA's thresholds text (p. 83) is dated (2005): it names New Zealand "at least one constituency seat" and Germany "three seats" as bypass routes, and Poland 1993, Turkey 2002 examples; the NZ and German rules read in C-10 / C-13 are the same bypass routes but the German one was removed in 2023 and then re-imposed by the Court as a condition (C-13). (7) The IDEA online pages (idea.int answer pages, e.g. https://www.idea.int/answer/ans93801038934080 "Electoral system for national legislature") were not read; only the Handbook PDF was.

#### [C] F-2 | Droop quota statement from an electoral authority (for list PR; shared with B's STV item)
MARK: confirmed from IDEA (an intergovernmental organisation, NOT an electoral authority); from an electoral authority: unread (not searched on a host in my list)
SOURCE: https://www.idea.int/sites/default/files/publications/electoral-system-design-the-new-international-idea-handbook.pdf (local: work-C/idea_handbook.txt) ; Glossary "Droop Quota", printed p. 176 (PDF p. 190); STV "Counting", printed p. 76 (PDF p. 90, formula rendered and read); South Africa case study, printed p. 62
QUOTE[work-C/idea_handbook.txt]: "Droop Quota – A variant of quota used in proportional representation systems which use the Largest Remainder Method, defined as the total valid vote divided by the number of seats to be filled in the electoral district plus one."
QUOTE[work-C/idea_handbook.txt]: "used is normally the Droop quota, calculated by the simple formula:"
QUOTE[work-C/idea_handbook.txt]: "The Droop Quota was used to allocate seats, and surplus seats were awarded by an adaptation of the Largest Remainder Method."
QUOTE[work-C/idea_handbook.txt]: "Quota – May have one of two distinct meanings: a. The number of votes which guarantees a party or candidate to win one seat in a particular electoral district in a proportional representation system."
NOTE: [stated] Two printed forms in one book: the glossary words say "the total valid vote divided by the number of seats ... plus one" (ambiguous: [inferred] it reads as votes/(seats + 1)); the STV counting text prints the formula as Quota = votes/(seats + 1), then "+ 1" outside the fraction (image checked, printed p. 76; text layer shows "Quota = votes +1 seats +1"). Those two differ by the final +1 (in the usual STV rule a candidate needs more than votes/(seats+1), i.e. that quotient plus one in whole numbers). The South Africa sentence is IDEA's case-study author's statement about the 1994 law (List PR, "no formal threshold"), not an electoral authority's. Electoral authorities of list-PR countries that use the Droop quota in law (not read by me): none requested on my host list. Task B reads ACE for STV.

#### [C] F-3 | Any published estimate of the probability that one vote changes a seat in a real PR election other than Lyytikainen & Tukiainen
MARK: unread (none found on the hosts I was allowed to read)
SOURCE: WebSearch (standard mode) queries tried, each returning URLs only: (1) "probability that a single vote is pivotal proportional representation election seat allocation estimate D'Hondt pivotal probability party seat"; (2) "\"pivotal\" vote \"proportional representation\" empirical frequency one vote changes seat allocation probability Israel OR Netherlands OR Brazil OR Switzerland"; (3) "\"decisive vote\" OR \"pivotal vote\" \"list proportional representation\" probability estimated real elections turnout \"one vote\" seat parliament bootstrap OR simulation"; (4) "Kotakorpi Poutvaara Terviö \"Returns to office in national and local politics\" bootstrap approach proportional elections lucky unlucky candidates"
NOTE: Reasons: the only results that were on-topic are off my allowed hosts (task rule: stay within the listed hosts), so they are LEADS, not read: (a) Kotakorpi, Poutvaara & Terviö (2017), "Returns to office in national and local politics: A bootstrap method and evidence from Finland" (Journal of Law, Economics, and Organization; the method L&T cite as their basis, which computes a candidate's election probability by resampling, not the chance that one vote changes a seat), found at https://docs.iza.org/dp10003.pdf and https://www.cesifo.org/DocDL/cesifo1_wp4542.pdf; (b) Mulligan & Hunter (2003), "The Empirical Frequency of a Pivotal Vote" (US Congress and state legislatures, not PR), https://www.nber.org/papers/w8590; (c) "An experimental test of the pivotal voter model under plurality and PR elections" (a laboratory experiment, not a real election), indexed at https://katalog.lib.cas.cz/KNAV/EdsRecord/edsair,edsair.doi...........12f117377cd2753a2ffce398322aeb19; (d) Gelman, King & Boscardin (1998) and Gelman, Katz & Bafumi (2004) (plurality), read by other readers. [stated, from the Luechinger paper I read] Luechinger et al. cite resampling-based closeness (Kotakorpi et al. 2017) only as a drawback (C-22), and their own paper gives margins, not probabilities. So: none found; the Finnish bootstrap of L&T (this file, C-25 to C-30) remains the only published per-vote seat-change frequency for a real PR system that I could read.

#### [C] F-4 | Whether divisor methods are monotone in votes (a party never loses a seat from gaining votes, others fixed)
MARK: unread (no source on the allowed hosts states or proves it); my own check is [measured], not a source
SOURCE: WebSearch (query: "divisor methods apportionment \"vote monotonicity\" OR \"monotone in votes\" party never loses seat when it gains votes Sainte-Laguë D'Hondt Balinski Young") returned URLs on hosts outside my list (arxiv.org/pdf/1504.06475, arxiv.org/pdf/1701.02396, en.wikipedia.org "Vote-ratio monotonicity" and others), not read. The statutory text of the German divisor rule is at https://www.gesetze-im-internet.de/bwahlg/__5.html (local: work-C/bwahlg5.txt)
QUOTE[work-C/bwahlg5.txt]: "Zur Ermittlung der Oberverteilung wird die Zahl der zu berücksichtigenden Zweitstimmen im Wahlgebiet durch den nach Absatz 2 zu bestimmenden Zuteilungsdivisor geteilt und das Teilungsergebnis gemäß Absatz 3 gerundet."
QUOTE[work-C/bwahlg5.txt]: "Die Teilungsergebnisse bei der Berechnung nach Absatz 1 werden gerundet, indem Zahlenbruchteile unter 0,5 zur darunterliegenden ganzen Zahl abgerundet und solche über 0,5 zur darüber liegenden ganzen Zahl aufgerundet werden."
QUOTE[work-C/bverfg08.txt]: "The negative voting weight effect is also not a necessary consequence of a system of proportional representation combined with the personal election of candidates."
NOTE: [stated] § 5 BWahlG states the German rule as a divisor method with standard rounding (equivalent to the Sainte-Laguë series 1, 3, 5, ...; see F-1 for IDEA's series); it does not state monotonicity. The BVerfG 2008 sentence says negative voting weight is "not a necessary consequence" of PR with personal election, i.e. that a PR system without it is possible; it does not say that divisor methods are monotone. [measured] My own brute-force check (work-C/mono.py, exact fractions): 59,994 random cases (2 to 6 parties, 1 to 25 seats, 0 to 60 votes each, one party's votes raised by 1 to 5, others fixed, ties by party index): the raised party's own seats fell in 0 cases for D'Hondt, 0 for Sainte-Laguë (1, 3, 5, ...), and 0 for Hare largest-remainder (also zero). This is a random test, not a proof and not a source; the usual highest-average argument is [inferred] simple: a party's quotients v/d(s) all rise when its votes rise and other parties' quotients are unchanged, so the number of its quotients among the M largest cannot fall. For a source, Balinski & Young "Fair Representation" or Pukelsheim's "Proportional Representation" are the standard texts [lead from my training, NOT read]; they are on non-listed hosts.

### Fill items, reader D

#### [D] F-1 | The pivotal-voter condition under a participation quorum or an approval quorum (open sources)
MARK: done as far as the sources allow (three sources found; two read)
SOURCE 1 (read): Aguiar-Conraria, Magalhaes & Vanberg online resource, Appendix 1, eqs. (A.1)-(A.3): see D-09 to D-12 and FORMULAS. It covers n = 9, participation quorum 4 and approval quorum 3 (a Supporter's no-quorum pivot probability is `sum_{v=0..4} rho(v,v)/2 + sum_{v=0..3} rho(v+1,v)/2`).
SOURCE 2 (read; a **different** paper): Yoichi Hizen, "A Referendum Experiment with Participation Quorums", First Draft May 2008, This Draft November 2012, Hokkaido University, https://www.cirje.e.u-tokyo.ac.jp/research/workshops/micro/micropaper12/micro1204.pdf (local: `work-D/cirje_micro1204.txt`, PDF 39 pages; I looked at pp. 5 and 6 as rendered images, `work-D/hizen_p-05.png`, `hizen_p-06.png`). This is a working paper by Hizen alone, **not** Hizen & Shinmyo (2011) (D-23), but it says its pivot-probability set-up follows Hizen and Shinmyo's.
QUOTE[work-D/cirje_micro1204.txt]: "Our model is closely related to the model of Hizen and Shinmyo (2011)."
QUOTE[work-D/cirje_micro1204.txt]: "In other words, the outcome is valid if my + mn ≥ [rm], and is invalid otherwise, where r ∈ [0, 1] is the turnout rate that must be achieved for the validity of the outcome"
QUOTE[work-D/cirje_micro1204.txt]: "For the computational ease of pivot probabilities, as in Hizen and Shinmyo’s (2011) analysis, we impose the following two assumptions on the values of m and r:"
QUOTE[work-D/cirje_micro1204.txt]: "The ﬁrst is to validate the outcome with alternative i being selected."
QUOTE[work-D/cirje_micro1204.txt]: "The second is to validate the outcome with alternative j being selected."
QUOTE[work-D/cirje_micro1204.txt]: "The third is for a vote for i to change the winner from alternative j to alternative i when the outcome is valid even without that vote."
QUOTE[work-D/cirje_micro1204.txt]: "Given these probabilities, voters with preference i vote for i only if (1 − v)pi + ti ≥ vqi. (1)"
NOTE: The model: m voters, each has preference "yes" with probability s; vote for the preferred option or abstain at zero cost; benefit 1 for the preferred outcome, 0 for the other, and v in (0,1) if the outcome is invalid (turnout below [rm]). Three ways one vote matters: p_i (validates the outcome with i winning), q_i (validates it with j winning: the "self-harming" event), t_i (changes the winner when the outcome is valid anyway). Assumptions: m odd, [rm] odd. Formulas in FORMULAS. The condition (1) is a per-vote expected-benefit inequality of the kind the site needs; it assumes no cost of voting and no population uncertainty.
SOURCE 3 (abstract only): Maniquet & Morelli, "Approval quorums dominate participation quorums", Social Choice and Welfare 2015 (IDEAS: https://ideas.repec.org/p/cor/louvrp/2666.html, `work-D/ideas_mm.txt`): "We study direct democracy with population uncertainty." Formulas unread (open PDF candidates in NEED-FETCH).
QUOTE[work-D/ideas_mm.txt]: "We study direct democracy with population uncertainty."
QUOTE[work-D/ideas_mm.txt]: "We show that with a participation quorum, i.e. a threshold on the fraction of participating voters below which the status quo is kept, the status quo may be kept in situations where the planner would prefer the reform, or the reform is passed when the planner prefers the status quo."
NOTE: Herrera & Mattozzi (D-16, D-17) give the party-level probability that reform passes under a turnout quorum, not an individual pivot condition.

#### [D] F-2 | Published estimates of a decisive-vote probability in a real referendum (any country), under a real supermajority/quorum rule, or in a real primary
MARK: none found (for all three); two nearby results read
SOURCE: queries tried (WebSearch, URL finding only): (1) "estimated probability a single vote is decisive in a referendum or ballot measure empirical estimate"; (2) "probability of being pivotal in a primary election estimate close primary margins decisive vote"; (3) `Swiss referendum "probability of being decisive" OR "pivotal" estimate vote closeness turnout direct democracy empirical`; (4) `pivotal voter supermajority rule probability decisive vote formula "supermajority" turnout quorum pivot probability large electorate`; (5) the Aguiar/Hizen/Maniquet searches of F-1. Result lists were dominated by the U.S. presidential Electoral College (Gelman et al.), turnout-and-closeness studies (e.g. a "Using prediction market data for measuring the expected closeness in electoral research" record at serval.unil.ch, an econbiz record "Expected closeness or mobilisation: why do voters go to the polls? Empirical results for Switzerland, 1981-1999", a CESifo paper `cesifo1_wp1387.pdf`, Bursztyn et al. on election closeness and turnout) and theory papers. I did not open those turnout-and-closeness items: they study turnout versus closeness, not a decisive-vote probability, from their titles [inferred].
SOURCE (read): https://ideas.repec.org/p/nbr/nberwo/8590.html (Mulligan & Hunter; local `work-D/ideas_mh.txt`), abstract only.
QUOTE[work-D/ideas_mh.txt]: "showing that one of every 100,000 votes cast in U.S. elections, and one of every 15,000 votes cast in state elections, 'mattered' in the sense that they were cast for a candidate that officially tied or won by one vote."
QUOTE[gkb1998_columbia.txt]: "we estimate the (prospective) probability of a single vote being decisive as about 1 in 10 million for close national elections such as 1992"
NOTE: Mulligan & Hunter's data are "U.S. Congressional and state legislator election returns" (D-24); no ballot measures, no primaries mentioned in the abstract. Gelman-King-Boscardin is a U.S. presidential-election estimate (abstract on the Columbia copy, p. 1). Neither is a referendum, a supermajority/quorum rule or a primary. So the first pass's "none found" stands for those three cases from what I read, with the caveat that the full text of Mulligan & Hunter is unread.

#### [D] F-3 | Italian referendum quorum outcomes (turnout versus the 50%+1 requirement), from an official source
MARK: done (official source reached)
SOURCE: Ministero dell'Interno, Dipartimento per gli affari interni e territoriali, Direzione centrale per i servizi elettorali, "Il Dossier - Referendum 2026", marzo 2026 rev. 1.2, https://dait.interno.gov.it/documenti/dossier-referendum-2026.pdf (102 pages; local `work-D/dossier_ref2026.txt`), tables 10.1 "I risultati dei referendum dal 1946 al 2025" (pp. 81-86) and 10.2 "Percentuali dei votanti dei referendum abrogativi dal 1974 al 2025" (p. 87); and the Ministry's "Il Dossier - Referendum 2025", giugno 2025 rev. 1.3, https://dait.interno.gov.it/documenti/dossier-referendum2025.pdf (`work-D/dossier_ref2025.txt`). The columns are "% Votanti" (voters as a share of electors), "% Si" and "% No" (shares of valid votes), with rows "ITALIA", "ESTERO" and "ITALIA + ESTERO". These are Ministry documents; the final proclamation is by the Court of Cassation's central referendum office, which I did not read.
QUOTE[work-D/dossier_ref2026.txt]: "8 e 9 giugno 2025 (abrogativi)"
QUOTE[work-D/dossier_ref2026.txt]: "ITALIA 30,58 89,06 10,94"
QUOTE[work-D/dossier_ref2026.txt]: "ITALIA + ESTERO 29,83 87,57 12,43"
QUOTE[work-D/dossier_ref2026.txt]: "ITALIA + ESTERO 29,85 65,34 34,66"
QUOTE[work-D/dossier_ref2025.txt]: "Domenica 8 e lunedì 9 giugno 2025 si terranno cinque referendum popolari abrogativi ai quali potranno partecipare 51.303.216 elettori, di cui 5.302.299 all’estero."
QUOTE[work-D/dossier_ref2026.txt]: "12 giugno 2022 (abrogativi)"
QUOTE[work-D/dossier_ref2026.txt]: "ITALIA + ESTERO 20,49 53,08 46,92"
QUOTE[work-D/dossier_ref2026.txt]: "Elezione Camera dei deputati (abolizione del voto di lista) 49,58 91,52 8,48"
QUOTE[work-D/dossier_ref2026.txt]: "ITALIA + ESTERO 54,82 95,35 4,65"
RESULT: (a) **8-9 June 2025** (five abrogative questions): turnout 29.83% to 29.85% of electors, Italy plus abroad (30.58% to 30.59% in Italy alone), against the 50%+1 needed; the pre-vote elector count was 51,303,216 (5,302,299 abroad). [measured, approximate] 29.83% of 51,303,216 is about 15.30 million voters and half the electors is 25,651,608, so the shortfall was roughly 10.3 million votes (uses the pre-vote elector count and the rounded percentage; the final elector count is not in what I read). Yes shares on the five questions: 87.57%, 86.02%, 87.53%, 85.78% and 65.34% (Italy plus abroad): large Yes majorities with the quorum unmet. (b) **12 June 2022** (five questions): 20.47% to 20.49% (Italy plus abroad; 20.49% on Q1). (c) **1999** (18 April 1999, abolition of the proportional list vote for the Chamber): 49.58% turnout with 91.52% Yes: short of 50% by 0.42 points [measured: 50 − 49.58]. (d) 2011 (12-13 June): 54.82% to 54.83% (Italy plus abroad), quorum met, Yes 94% to 95%.
RESULT, all years: taking the highest-turnout question of each of the 19 abrogative referendum days from 1974 to 2025 (my parse of table 10.1; it reproduces the dossier's chart 10.2 exactly), the turnout was **below 50% on 10 of the 19 days** [measured by comparison with the 50% rule; the dossier does not label the failures]: 1990 (43.36), 1997 (30.29), 1999 (49.58), 2000 (32.51), 2003 (25.75), 2005 (25.66), 2009 (24.02), 2016 (31.19), 2022 (20.49), 2025 (29.85). Above 50%: 1974 (87.72), 1978 (81.19), 1981 (79.43), 1985 (77.85), 1987 (65.12), 1991 (62.50), 1993 (77.01), 1995 (58.12), 2011 (54.83). The 2005 June referendum is the one Herrera & Mattozzi describe (D-18).
QUOTE[work-D/dossier_ref2026.txt]: "Per la validità della consultazione non è necessario raggiungere il quorum della maggioranza degli aventi diritto al voto (50%+1);"
NOTE: constitutional referendums (Art. 138) have no turnout requirement; the table lists 2001 (34.05%), 2006 (52.46%), 2016 (65.48%), 2020 (51.12%) with no quorum consequence. The 22-23 March 2026 constitutional referendum on the justice reform is announced in the 2026 dossier (51,424,729 electors, 5,477,619 abroad); its result is not in that dossier and I did not look for it. Whether the quorum is checked on Italy-plus-abroad or Italy-only electors does not matter for any case above except possibly 1999 (the 1999 row has one line only; Italy-only figure not given there).

#### [D] F-4 | An open, official dataset of primary margins
MARK: identified and one file read
SOURCE: Virginia Department of Elections, "Historical Elections Database", contest page https://historical.elections.virginia.gov/contest/160943 ("2025 Jun 17 • Democratic Primary Election • Lieutenant Governor • State of Virginia"; local `va_contest.html`), which links "Download the data from this contest: Results CSV", https://va2.elstats.civera.com/api/download_contest/160943_table.csv?split_party=false (served from a vendor host, `civera.com`; local `work-D/va_lg.csv`, 2,802 lines: State, then each locality, then each precinct). Each contest has its own CSV. This is a state election authority's open, free, per-contest file; I did not build a dataset.
QUOTE[work-D/va_lg.csv]: ",,Ghazala F. Hashmi,Levar Marcus Stoney,Aaron R. Rouse,Babur B. Lateef,Alexander J. Bastani,Victor R. Salgado,Total Votes Cast"
QUOTE[work-D/va_lg.csv]: "State,Virginia,136717,131765,130485,42099,28476,27593,497135"
NOTE: For this one contest the CSV gives a six-candidate Democratic primary: 136,717 / 131,765 / 130,485 / 42,099 / 28,476 / 27,593, total 497,135 (the six sum to 497,135 [measured]). Margins [measured]: first minus second 4,952; second minus third 1,280. The CSV is precinct-level, so margins by district are computable for legislative contests the same way. Leads not read (hosts are task F's or not mine): Ballotpedia's "Primary election competitiveness in state government, 2025" (https://ballotpedia.org/Primary_election_competitiveness_in_state_government,_2025, link found in the file `ballotpedia_primaries.html`) and Ballotpedia's "Virginia state legislative election results, 2025" (from a search result); the Virginia site's coverage of earlier years and the other states (New Jersey, Wisconsin) were not checked.

---

### Fill items, reader E

#### [E] F-1 | Baltz supplement (baltz_sup): what it contains, and whether it lets the 10^-6 / 10^-7 values be reconciled
MARK: confirmed (read whole, 24 pages; text extract and page images of pp. 8, 12, 18)
SOURCE: https://static.cambridge.org/content/id/urn%3Acambridge.org%3Aid%3Aarticle%3AS1047198724000329/resource/name/S1047198724000329sup001.pdf (local: baltz_sup.raw.txt, baltz_sup.txt; fetched by the orchestrating thread, not by me)
QUOTE[baltz_sup.raw.txt]: "There is one crucial distinction that must be noted between the approach that I take in this letter and the closest approach that I build on in the literature, that of Eggers and Nowacki (2024)."
QUOTE[baltz_sup.raw.txt]: "I will use different numbers from the example in the main text because with such large numbers, exact pivotal probabilities become almost inexpressibly small."
QUOTE[baltz_sup.txt]: "pdirect (S) ≈ 0.023"
QUOTE[baltz_sup.raw.txt]: "In the article I implement the IRV pivotal probability algorithm in Python and simulate the magnitude of pivotal probabilities for identical election setups in IRV and SMDP."
NOTE: **Contents** (section titles as printed): Appendix, dated 4 September 2024, for a journal "letter". §1 Further context (contrasts with Eggers & Nowacki, who count the probability of causing a drop in some round whether or not it changes the winner, and with the "margin of victory" literature; defines IRV); §2 The counterfactual (abstention; the cost term T; what changes if the counterfactual is another ballot beta'); §3 Simplifying assumptions (Assumptions 1 and 2 again; tie-breakers, "I assume a fair tie-breaker"); §4 Indirect pivotality from switching sequences; §5 Example pivotal probability calculation (5 candidates, 25 voters, ballots of length 3: Gross, Claus, Begich, Peltola, Palin; one direct drop sequence p_direct(S) ≈ 0.023 and one indirect event p_not-d(E) ≈ 0.003); §6 Pseudocode (the same two algorithms as arXiv Sec. 3); §7 Equal utility ballots; §8 Modeling the probabilities (the Skellam-form u(beta), same as arXiv p. 20); §9 Simulated pivotal probabilities (the Figure 1 text, with a longer discussion, and Figure 1 with plotted mean lines); §10 Translation to existing notation (derives Eggers & Nowacki's second-round pivot event pi_{xy,2} from Baltz's p_direct and says "the two papers agree when applied to the same situation"); references. **No code, no data, no repository link, no replication archive, no proofs beyond the algebra, and no extra simulations.** It is not the main text: its references to "Equation 6 in the article" and "Equation 8 in the main article" point to the journal text, which I have not seen.
NOTE (reconciliation): the supplement does help, in four ways, and does not settle two things. It helps: (1) it says what the y-axis sums ("the sum of the pivotal probability of every possible ballot", "Each dot represents the sum of the pivotal probabilities of all ballots in one run of the simulation"); (2) it adds plotted means and the warning that the two panels have different y-scales "so ... they should not be directly compared to one another without taking the y-axis scales into account"; (3) it says IRV is "slightly higher ... overall" with "slightly lower variance"; (4) it gives a worked numeric example with its Skellam convention, which I can recompute (below). It does not give: the power-law parameters beyond one sentence; how ballots are drawn beyond "determined randomly, in a way that ensures that support for the candidates follows the specified distribution"; the SMDP formula (only "the derivation from Mebane et al. (2019)", a 2019 conference presentation); or the code. So the 10^-6 / 10^-7 values cannot be reproduced from the paper and supplement alone.

#### [E] F-2 | The published (journal) version of Baltz, Political Analysis 33(4): differences visible through the supplement and the arXiv text
MARK: unread (journal page not allowed to me); partial comparison confirmed from the two files I have
SOURCE: arXiv v2 (https://arxiv.org/pdf/2210.01657, local baltz_arxiv.raw.txt, dated 31 Jul 2023) against the published Appendix (baltz_sup.raw.txt, dated 4 Sep 2024)
QUOTE[baltz_arxiv.raw.txt]: "In the Appendix I also apply the pivotal probability equation to a simple example of an IRV election, and I show step-by-step how to use it to compute numerically specific probabilities of both direct and indirect pivotality for a full IRV ballot."
QUOTE[baltz_sup.raw.txt]: "Figure 1 shows the total pivotal probability for two stylized preference distributions in either IRV and SMDP: one where support for 3, 4, or 5 candidates is roughly uniform, and another where it follows a power law."
NOTE: Differences I can see (all [stated] by the two files): (1) **the arXiv v2 PDF has no appendix** (28 pages: text, pseudocode, references), though its text promises one three times ("In the appendix I illustrate and explain the abstract derivation by providing simple numerical examples"); the published Appendix is what the arXiv text refers to. (2) The arXiv abstract differs from the sentence the first pass attributes to the journal abstract page (E-15), so the journal abstract was rewritten or the first-pass sentence is an extractor paraphrase; unresolved. (3) The arXiv v2 simulation text says "I conclude by implementing" and has one paragraph on Figure 1; the published appendix §9 has more (IRV "slightly lower variance"; "these are stylized figures meant to illustrate how my derivations could be applied in the presence of actual preference data"; the caution that the Assumption 2-driven decline is not substantive is kept). (4) Figure 1: the dots appear to be the same (I compared the extreme points by eye, not by pixel); the published version shifts the two systems side by side and adds mean lines; the caption changes from "in a community of 1,000 voters ... Candidates have an equal probability of appearing in any position on any ballot" to "when 1,000 voters can rank every candidate"; the arXiv caption sentence about equal probability of appearing in any position is dropped. (5) Eggers & Nowacki: cited as an unpublished 2021 paper in arXiv v2 and as Journal of Politics 86(2) (2024) in the published Appendix. (6) The published Appendix says "this letter", so the journal paper is the short form. The numerical claims in the text (100 runs; 3-5 candidates; 1,000 voters; "about 10^-6 ... about 10^-7"; "neither is clearly larger") are word-for-word the same in both files. I could not check volume, pages or abstract of the journal version.

#### [E] F-3a | Other source cited as a derivation of monotonicity-failure frequency: Allard (1996), read
MARK: confirmed (the paper exists and says what O&N cite it for, with qualifications that change its meaning; it is not about IRV)
SOURCE: https://www.votingmatters.org.uk/ISSUE5/P1.HTM (local: allard.txt in SP/r4/work-E/allard/; HTML page, Voting matters Issue 5, January 1996, pp. 1-5; the area formulas are images and are not in my text)
QUOTE[allard.txt]: "In this paper I attempt to estimate the probability of a monotonicity failure which affects the number of seats won by a party."
QUOTE[allard.txt]: "I estimate the probability of this occurring in a multi-member constituency in one election as: 2.5 × 10**(-4), equivalent to less than once every century across the whole UK."
QUOTE[allard.txt]: "So, if the UK is divided into 138 multi-member constituencies, as proposed in Reference 4, and assuming an average of one General Election every four years, we would expect one instance of final-stage monotonicity failure affecting party standing under STV roughly every 115 years."
QUOTE[allard.txt]: "Thus, if we assume a uniform distribution, the probability of this type of monotonicity failure is the ratio of the area of the small triangle (either PQR or STR, whichever is the smaller) to the area of the large one (ABC)."
QUOTE[allard.txt]: "It is almost certainly true that the probability of affecting individual candidates within a party is much greater."
NOTE: [stated]. What it is: an area-ratio calculation (a probability that a randomly drawn three-party vote split, uniform over the triangle, satisfies the failure conditions M1-M3 printed in the paper, with transfer rates alpha and beta estimated from an ERS/MORI exit poll of 3,983 London voters in the 1994 European Parliament elections: "840 data sets (sadly not independent!)"), for the **final stage of an n-member STV constituency** and for failures that change a party's seat count. Not IRV, not single-winner, per **constituency-election** (2.5 x 10^-4), not per ballot. The conditions as printed (text form): "a > b > c", "a < b + alpha x c", and that some x exists with "a - x > b", "c + x > b", "a > c + 2x + beta x b": the failure has B elected, and A elected after voters move from A to C, which in G-S&M's terms is the *downward* kind (a loser wins by losing support), while O&N's measure is the *upward* kind [inferred from the printed conditions]. So O&N's gloss ("if the United Kingdom adopted IRV for its general elections ... about once per century") compresses Allard's STV, party-level, final-stage, uniform-prior figure. Allard's own caveats include "The method assumes a Uniform (prior) distribution of votes between the three parties" and "The results are based on an opinion poll conducted only in London".
QUOTE[allard.txt]: "The results are based on an opinion poll conducted only in London."

#### [E] F-3b | The same Allard result is disputed on rangevoting.org (different source, an advocacy site)
MARK: confirmed that the page says this; [stated by the page's author, Warren D. Smith; not peer-reviewed; I have not checked his claims]
SOURCE: https://www.rangevoting.org/Monotone (local: monotone.txt in SP/r4/work-E/rv/; one request, HTTP 200; "heavily revised March 2009")
QUOTE[monotone.txt]: "One reason was a published paper by Crispin Allard in which he made an incorrect calculation of these numbers."
QUOTE[monotone.txt]: "As a result of these errors, Allard got a number about 1000 times smaller than the truth."
QUOTE[monotone.txt]: "In total, monotonicity failure occurs once every 6.9 elections, i.e. 14.5% of the time."
QUOTE[monotone.txt]: "Allard only examined type-II nonmonotonicity and apparently was unaware that type-I also existed."
NOTE: The page's own model is the "random elections model" ("Impartial Culture"), i.e. six random ballot-type counts for three candidates, Monte Carlo, for any three-candidate IRV election; it gives type-I (a winner stops winning when given votes) 12.2% and type-II 2.3%. Inside the page the summary paragraph says "type (I) occur about once per 45 elections and of type (II) occur once per 8.2 elections", which is the reverse of its own program output (type-I 12.18% = 1 in 8.2; type-II 2.312%): an internal inconsistency in the page as printed. Different model, different scope (any three-candidate IRV election with uniform random preference counts, not a forecasted close race) from both Allard and O&N. This is where two sources disagree about Allard: O&N cite it as a UK estimate without comment; Smith calls it wrong by about a factor of 1000. I give each with its source and do not choose.

#### [E] F-3c | Other cited derivations: not read
MARK: unread
SOURCE: (none read)
NOTE: Named by Baltz as the prior derivations of IRV pivot probabilities: "Eggers and Nowacki (2021)" (published as Journal of Politics 86(2), 2024; Baltz's supplement says they consider "pivotal events in IRV", restricted to three or four candidates, with beliefs over a continuous vote share, and that the two papers agree on the one event Baltz translates: pi_{xy,2} = [P(v_y + v_{zy} = v_x + v_{zx}) + P(v_y + v_{zy} = 1 + v_x + v_{zx})] x P(v_z < v_x) x P(v_z < v_y) as printed in supplement p. 22) and Bouton (2013) (taken by another task). Not read, reason: Journal of Politics page is on journals.uchicago.edu (not a host my task allows; found by search: https://www.journals.uchicago.edu/doi/10.1086/726943 -> NEED-FETCH, and likely a paywall); Mebane, Baltz & Vasselai (2019), "Presented at the 2019 meeting of the Society for Political Methodology": a conference presentation, no URL found by my one search; Myerson (1998), Vasselai (2022, AAAI), Cox (1994), Cox & Shugart (1996): not searched (not about IRV). Named by O&N for monotonicity frequency: Lepelley, Chantreuil & Berg (1996) (first-pass §2; another task), Norman (2006, 2012), Miller (2012) (Miller 2017, "Closeness matters: Monotonicity failure in IRV elections with three candidates", Public Choice 173, is G-S&M's reference [19]; springer host, not mine): not read. Margin of victory (Baltz supplement): Atsusaka, Valeva & Vallejo (2024), Blom et al. (2016), Magrino et al. (2011): not read; the supplement says these concern "the fewest number of ballots that could upset an election result", which is not a pivot probability.

---

### Fill items, reader F

#### [F] FILL F-1 | Any published estimate of the probability that one vote decides control of a legislative chamber (not just the seat); include 538's "tipping point" methodology page
MARK: none found (for an absolute single-vote probability of deciding chamber control); two published seat-level / relative measures found and read, one methodology page not read
SOURCE: (a) 538 article via WebFetch (work-F/webfetch_fte.txt) and the 538 data dictionary on a mirror via WebFetch (work-F/webfetch_datahub.txt); (b) Princeton Election Consortium, "Democracy Moneyball, 2022. Part 1: the Senate", October 2, 2022 by Sam Wang, https://election.princeton.edu/?p=2221 (curl, local: work-F/pec2221.html, strip work-F/pec2221.txt); (c) GKT 2002 (work-F/sswp1141.txt)
QUOTE[work-F/webfetch_fte.txt]: "- "...the odds that each district will be the "tipping-point seat" in the House" (excerpt; the full sentence exceeds 125 characters)"
QUOTE[work-F/webfetch_datahub.txt]: "- "vpi""
QUOTE[work-F/pec2221.txt]: "I defined a jerseyvote as the amount by which one New Jersey vote changed the probability of Senate control."
QUOTE[work-F/pec2221.txt]: "voterpower for a state = tpdf(|statemargin-MetaMargin|/sigma,tail) / voterpop,"
QUOTE[work-F/pec2221.txt]: "Relative voter power then looks like this:"
QUOTE[work-F/sswp1141.txt]: "Voting power has also been applied to more complicated voting schemes, which we do not discuss here, such as legislative elections with committees, multiple chambers, vetoes, filibusters, and so forth (Shapley and Shubik, 1954)."
NOTE: (1) 538: publishes, per House district and per Senate state, the probability that the seat is "the tipping-point seat" (the 218th seat in the House ordering by partisanship; WebFetch quotes in F-04) in its CSV "tipping" column; this is the seat-level stage-two quantity of section 8, not a per-vote probability; the values were not read (F-07). The CSV also has a "vpi" column (only its name is known; the data dictionary text on the mirror was not read in full and the extract gives no definition of vpi, so it is NOT known whether "vpi" is a per-vote measure). 538's methodology page https://fivethirtyeight.com/methodology/how-fivethirtyeights-house-and-senate-models-work/ answers 301 to https://abcnews.com/politics to curl; WebFetch returned an extract that said it contained none of "tipping point", "tipping-point", "value of a vote", "VPI" or "voter power index" and one related line, "Democrats' chances of winning the House were about 7 in 10" (dated versions June 30, 2022 and Sept. 18, 2020, per the extract); the page is long and the WebFetch read may not have covered all of it, so "538 methodology page defines tipping point": NOT FOUND, not shown absent. (2) Princeton Election Consortium (Sam Wang) publishes a relative per-voter measure for Senate control: a "jerseyvote" is "the amount by which one New Jersey vote changed the probability of Senate control", and the formula as printed is voterpower for a state = tpdf(|statemargin - MetaMargin| / sigma, tail) / voterpop, with tpdf a "long-tailed" density ("see MATLAB documentation"; tail = 1), statemargin = median recent-poll margin, sigma = 4 points, voterpop = estimated voters (2020 turnout); it is a relative index across Senate states (charts, not read, show it), with no absolute probability stated in the text. A Part 2 on the House was announced ("In the next installment ... I'll write more about the House") but not found. (3) GKT 2002 explicitly leaves multi-chamber / legislative voting schemes aside. Queries tried (WebSearch, URLs only): "FiveThirtyEight tipping-point seat median seat by partisanship House forecast 2022 tipping point districts"; "The 10 Districts Most Likely To Decide Control Of The House Rakich FiveThirtyEight"; "house_district_toplines_2022.csv fivethirtyeight data tipping column"; "FiveThirtyEight How our 2022 House and Senate models work methodology tipping-point value of a vote VPI"; "FiveThirtyEight voter power index Senate House seat tipping point chance one vote decides control of the chamber relative"; "Princeton Election Consortium Democracy Moneyball, 2022. Part 2 House voter power"; "probability a single vote decides control of the U.S. Senate estimate one in million vote pivotal chamber control paper". Not readable: VoteHub, "VoteHub's Voter Power Index: Finding 2026's Most Impactful Ballots" (Sept 10, 2026, https://votehub.com/2026/09/10/votehubs-voter-power-index-finding-2026s-most-impactful-ballots/): curl returned HTTP 403 with a Cloudflare "Just a moment..." page; not circumvented; its title suggests it estimates a per-ballot measure for 2026 (content unread; a lead only). Gelman, Silver & Edlin (2012) is task A's host (see NEED-FETCH).

#### [F] FILL F-2 | Any published estimate of the probability a vote is decisive in a real small local election (school board, municipal, union), beyond Farber and Lyytikainen & Tukiainen
MARK: none found (as a probability); one frequency source and one model paper read
SOURCE: Coate, Conlin & Moro, NBER WP 10797 (September 2004), https://www.nber.org/system/files/working_papers/w10797/w10797.pdf (curl; local: work-F/w10797.raw.txt); Ballotpedia table (F-42 to F-52); Mulligan & Hunter (FILL F-3)
QUOTE[work-F/w10797.raw.txt]: "With a relative small number of voters (e.g., less than 5,000), the equilibrium probability of being pivotal is large enough to motivate voters with positive costs of voting to participate."
QUOTE[work-F/w10797.raw.txt]: "Evaluating the expected benefit of voting requires computing the equilibrium probability that a voter will be pivotal."
NOTE: Coate, Conlin & Moro (the Journal of Public Economics 92 (2008) version is the published form per the search results; I read only the NBER working paper) estimate a pivotal-voter model on Texas liquor referenda (small jurisdictions, within-sample under 900 eligible voters per their text, out-of-sample 906 to 81,904) and report turnout and closeness distributions; a search of the text for "pivotal" finds the model and the statement quoted but no table or sentence giving a numeric pivot probability, and the main finding is that the model "predicts much closer elections than are seen in the data" ("tends, on average, to predict closer electoral outcomes than are observed", abstract). So it is a source on the model, not an estimate. Frequencies, not probabilities, from real local elections: Ballotpedia counts (F-43 to F-45, F-52): 104 of 150,010 elections in its coverage scope decided by one vote since 2018 [measured: 104 / 150,010 = 0.069%, about 1 in 1,442] and 734 (or 733 in the table) by 10 or fewer, but the page does not say whether uncontested elections are in the 150,010, and its counts of "decided by" rows are concentrated in North Carolina 2019 municipal elections (267 of 733 rows), so this ratio is not a rate for a typical local race. Queries tried: "Coate Conlin Moro Texas liquor referenda pivotal probability"; "probability of being pivotal school board election OR municipal election empirical estimate ..."; "frequency of close elections local government elections tie probability estimate decided by one vote city council school board ...". One search hit (CESifo working paper 7786, https://www.cesifo.org/DocDL/cesifo1_wp7786.pdf) was not read: curl returned a 3,038-byte HTML page (a bot-check/challenge page, same size as other challenge pages in src) instead of the PDF; no workaround attempted. Task C holds Lyytikainen & Tukiainen.

#### [F] FILL F-3 | Mulligan & Hunter (2003) "The empirical frequency of a pivotal vote", Public Choice 116: abstract; "one out of 89,000" and what it is the frequency of
MARK: confirmed (abstract, published version, via EconPapers/RePEc; body of the published version unread); the NBER working-paper version body was read and gives a different headline number (100,000)
SOURCE: https://econpapers.repec.org/RePEc:kap:pubcho:v:116:y:2003:i:1-2:p:31-54 (curl; local: work-F/ep_mh.txt) for the Public Choice abstract; https://www.nber.org/papers/w8590 and https://www.nber.org/system/files/working_papers/w8590/w8590.pdf (curl; local: work-F/w8590_abs.txt, work-F/w8590.txt) for the working paper, NBER WP 8590, November 2001
QUOTE[work-F/ep_mh.txt]: "One of every 89,000 votes cast in U.S. Congressional elections, and one of 15,000 in state legislator elections, "mattered" in the sense that they were cast for a candidate that tied or won by one vote."
QUOTE[work-F/ep_mh.txt]: "Public Choice, 2003, vol. 116, issue 1-2, 54 pages"
QUOTE[work-F/w8590.txt]: "showing that one of every 100,000 votes cast in U.S. elections, and one of every 15,000 votes cast in state elections, “mattered” in the sense that they were cast for a candidate that officially tied or won by one vote."
QUOTE[work-F/w8590.txt]: "A “pivotal vote” is a vote cast for the winner in a pivot election, or cast for either candidate in a tied election."
QUOTE[work-F/w8590.txt]: "Of the 16577 US returns analyzed, only one (1/16577=0.00006) was decided by a single vote."
QUOTE[work-F/w8590.txt]: "Of the 40036 STATE elections (with almost one billion votes) analyzed, two were tied and seven were decided by a single vote (9/40036=0.0002)."
QUOTE[work-F/w8590_abs.txt]: "Mulligan, Casey B and Charles G. Hunter. "The Empirical Frequency Of A Pivotal Vote," Public Choice, 2003, v116(1-2,Jul), 31-54."
NOTE: What "one in 89,000" is the frequency of: the share of all votes cast in US Congressional (House) elections that were "pivotal" in the authors' sense: cast for the winner of an election the winner won by one vote, or for either candidate in an election that ended in a tie, by the official final count (not a probability that a random voter would be decisive in a forecast; an empirical share of votes). The headline in the Public Choice abstract is 89,000 (US Congressional) and 15,000 (state legislators); the NBER working paper (Nov. 2001) abstract says 100,000 (US) and 15,000 (state), so the published figure differs from the working paper's (the text layer of the working paper contains no "89,000"; its US data are 16,577 House elections 1898-1992 with one decided by a single vote, 20,685-20,684, with 41,369 votes cast, footnote 6: "a 0.00001 share" once the 20,684 losing votes are removed; state data 40,036 elections, 1968-89, two ties and seven one-vote margins, 61,328 votes in those nine elections, "a 0.00006 share"). The reason for the change from 100,000 to 89,000 (new data, a corrected count) is not stated in anything I read; the body of the published version is paywalled (EconPapers: "Access to full text is restricted to subscribers") and unread. Task A's GKT/GKB sources cite the 2001 working paper (GKT 2002: "see Mulligan and Hunter, 2001"), which would match the 100,000 version. The 2001 abstract also says "Very close elections are more rare than the independent binomial model predicts" and that "recounts, and other margin-specific election procedures, are quite relevant determinants of the frequency of a pivotal vote". SSRN (https://papers.ssrn.com/abstract=290394) answered HTTP 403 with a Cloudflare "Just a moment..." page: unread, not circumvented. Date caution: the working-paper authors say it is a revision of "Mulligan and Hunter (2000)" (a still earlier version).

## Appendix A re-run (by the orchestrating worker; the readers ran no code except where a block says so)

All seven scripts of the first report's Appendix A were extracted unchanged from `research/electoral-systems.md`, with only the placeholder path replaced, and run on 2026-11-07 (Python 3, numpy 2.5.3, `python3 -I`; seeds as in the scripts). They use no data from the web.

| Script | First-pass result | Re-run | Stands? |
|---|---|---|---|
| `plur.py` | N = 1,000: Q = 0.01261; N = 10,000: 0.003989 (= 1/√(2πN) to 5 digits); forecast (.51,.49), kappa 400: 0.006363 at N = 1,000, 0.000724 at N = 10,000 | 0.0126125; 0.00398932 against 1/√(2πN) = 0.00398942; 0.00636319; 0.000723861 | yes, identical |
| `plur3.py` | the §1 table (e.g. (.4,.4,.2) known: 0.01410 and 0.004460; (.40,.38,.22) forecast: 0.00707, 0.00712, 3e-7 at N = 1,000) | 0.0140973 and 0.00446007; 0.00706638, 0.00711841, 2.94e-7 | yes, identical (reader A also reproduced every row, A-18) |
| `pr.py` | council-sized 0.0052, 0.0056, 0.0059, 0.0062, 0.0067; M = 5: 2.4e-5, 4.7e-5, 4.5e-6, 2.1e-5; M = 10: 5.8e-5, 6.2e-5, 4.4e-5, 9.1e-5, 9.8e-6; national 2.1e-5 to 2.7e-5 | 0.00515, 0.00558, 0.00588, 0.00624, 0.00665; 2.36e-5, 4.69e-5, 4.46e-6, 2.11e-5; 5.8e-5, 6.2e-5, 4.39e-5, 9.1e-5, 9.83e-6; 2.1e-5, 2.36e-5, 2.52e-5, 2.59e-5, 2.69e-5 | yes (Monte Carlo, 20,000 or 6,000 draws; differences in the last digit) |
| `pr_check.py` | analytic 0.00626 / 0.01035 / 0.00862; brute force 0.00623 / 0.0112 / 0.00893 | the same figures | yes; the second party differs by about 1.3 combined Monte Carlo standard errors |
| `ref.py`, `ref2.py` | §6 table and §9 table | identical to the digits printed in the first report | yes |
| `chamber.py` | §8 table, "mean of three random draws" | identical | yes, with the caveat below |

**Comparators the first pass extrapolated and did not compute, now [measured].** Two-candidate Q for forecast (.51,.49), kappa 400: N = 4,000: 0.0017670 (first pass 0.00177); N = 50,000: 1.4669e-4 (1.47e-4); N = 100,000: 7.347e-5 (7.3e-5); N = 1,000,000: 7.3581e-6; N = 5,000,000: 1.4718e-6 (first pass 1.47e-6, scaled from N × Q = 7.36). N × Q converges to f(1/2)/2 = 7.3593, where f is the Beta(204, 196) density of the vote share at 1/2, as Q ≈ f(1/2)/(2N) predicts. The N × Q scaling the first pass used for the 2016-referendum remark (§6 reading (d)) holds to four digits at N = 5 million; the factor exp(−0.76²/2) = 0.75 is arithmetic.

**Against the corrected formulas.** (a) *The definition of Q.* Every table in §1, §6 and §9 is Q = P(wins | one more vote for it) − P(wins | the voter abstains), ties by a fair coin. Gelman, Katz & Bafumi's Sec. 2.1 compares a vote for A with a vote for B, which is 2Q (A-26); the constant they print, √(2/π), is the swing, so the first pass's exact numbers are consistent with the paper's formula once the comparison is named. None of the first pass's calculations uses the misread constant 2/√π; they are exact sums, so the correction does not reach them. (b) *D'Hondt.* `pr.py` uses ratios votes_j/i and a coin flip when the voter's ratio equals the (M − i + 1)-th highest ratio of the others, which is Luechinger et al.'s party margin (p. 104, transcribed in FORMULAS); the paper's example (shares 45/35/20, three seats) gives P2's margins 15, −10, −100, which I reproduced by hand, and `pr_check.py`'s brute force agrees with `pr.py`. (c) *The supermajority pass rule* in `ref.py` (Y ≥ q(Y+X) for q > ½) is the first pass's definition; no readable source states it (D-01). (d) *Myatt & Fisher's printed two-way constant* (the "6n") is not used by any calculation. (e) *Baltz's formulas* are not used by any calculation; reader E applied them separately (RECONCILIATION).

**A caveat on `chamber.py` (§8).** The baseline margins of the other 434 seats are random draws (seeds 0, 1, 2), so each row is a function of those draws as well as of the parameters: the row m0 = 0 has an expected 209 Democratic seats among the other 434, not 217, which is why the first pass calls the 209 rows "near" a toss-up. The seat-count standard deviations are 13 to 36; by a normal approximation [inferred] an 8-seat offset changes P(exactly 217) by about 5% when the standard deviation is 24 and by about a fifth when it is 13, so the σ = 1 rows are the more affected. The table is a stylised illustration, as the first pass said, and has no published counterpart (F fill F-1).

## Table of every correction (old, new, source)

*One row per block whose mark is corrected or confirmed with a correction (52 blocks). The text is the reader's CORRECTION line (or, where there is none, the MARK line), cut at about 460 characters; the block has the full text and the quotes. A correction to the first pass's wording or section reference is listed with the same weight as one to a figure, so a reader can see which are which.*

| Block | Section | First-pass claim | Old → new (reader's words) | Source |
|---|---|---|---|---|
| [A] A-04 | §1 | Eq. 1: Pr[x] = integral Pr[x\|p] f(p) dp = (n!/prod x_j!) integral prod p_j^{x_j} f(p) dp; x_j votes for candid | (wording) "p the vector of true support" -> M&F say p "represents the constituency support for the m candidates" (Sec. 2.1) and, in Sec. 2.2's discussion, "the likely voting *intentions* of the wider electorate and not necessarily their preferences": each other voter independently votes for j with probability p_j; p is *unknown* to voter 0, who has the belief density f(p) on the simplex. | https://ora.ox.ac.uk/objects/uuid:adeb8fa9-899c-4fbe-9594-5574db9c4d24/files/sv979v3563 |
| [A] A-06 | §1 | Lemma 1 (Sec. 2.3, pp. 8-9): two-way near-tie probability of order 1/n; three-way tie Pr[x1=x2=x3+1] ≈ (1/n²)  | (wording) Eq. (2): Pr[x1 − 1 = x2 > x3] ≈_{n→∞} ( ∫_{1/3}^{1/2} f(z, z, 1 − 2z) dz ) / (6n) ≈_{n→∞} Pr[x1 = x2 > x3 + 1] "with similar expressions available for Pr[x1 = x3 > x2] and Pr[x2 = x3 > x1]". Eq. (3): Pr[x1 = x2 = x3 + 1] ≈_{n→∞} (1/n²) f(1/3, 1/3, 1/3) ≈_{n→∞} Pr[x1 = x2 = x3] "where the first equivalence applies for (n − 1)/3 ∈ N and the second for n/3 ∈ N." m in Lemma 1 is not a symbol: Lemma 1 is for the three-candidate case (m = 3); the n^{-(m-1)} of … (full text in the block) | https://ora.ox.ac.uk/objects/uuid:adeb8fa9-899c-4fbe-9594-5574db9c4d24/files/sv979v3563 |
| [A] A-12 | §1 | Two-party: Pr(decisive vote) ≈ p_{v_j}(0.5)/n_j (eq. 2 and Appendix eq. 3); p_{v_j} the density of the distric | (wording) confirmed (eq. 2); Appendix eq. 3 is corrected in A-13 | https://sites.stat.columbia.edu/gelman/research/published/gelmankatzbafumi.pdf |
| [A] A-13 | §1 | Appendix eq. 3: "Pr = E[Phi(v - 1/n) - Phi(v)]" (L28) | "E[Phi(v − 1/n) − Phi(v)]" -> **E[π(v + 1/n) − π(v)]** (eq. 3), where π(v) (a lower-case pi, the glyph lost in the text layer) is "the probability that party A wins, given a true proportion v" (not a normal cdf), and "v" is "the proportion in favour of candidate A, excluding your potential vote" and the sign is **+ 1/n**. The text layer shows "(v ⫹ 1/n) ⫺ (v)" with the symbol missing; the page image shows π(v + 1/n) − π(v). | https://sites.stat.columbia.edu/gelman/research/published/gelmankatzbafumi.pdf |
| [A] A-14 | §1 | Under random voting, an approximation "of the form (2/sqrt(pi)) * (1/sqrt(n_j))" (as extracted; constants unve | "(2/√π)·(1/√n_j)" -> **√(2/π) · 1/√n_j** (≈ 0.7979/√n_j). Printed: "Pr (a given vote is decisive in jurisdiction j) = p_{v_j}(0.5)/n_j = √(2/π) · 1/√n_j ." followed by "What matters for comparing voters is not the constant factor √(2/π) but the proportionality with 1/√n_j." The text layer reads "兹2/ but" because the π glyph (and the radical's extent) is lost; the extractor's "2/sqrt(pi)" = 1.128 is an extraction error. The constant √(2/π) is exactly what … (full text in the block) | https://sites.stat.columbia.edu/gelman/research/published/gelmankatzbafumi.pdf |
| [A] A-15 | §1 | Sec. 2.3 forecast example: 10,000 voters, 52% forecast, 3% standard error gives decisiveness ≈ 1.84/n_j (extra | (wording) as printed on the page image: "[1/√2π (0.03)] exp(−0.5(0.05/0.03)²)/n_j = 1.84/n_j" (the radical covers 2π only; the exponent has 0.05/0.03; the example says 52% forecast, so the distance to 0.5 is 0.02). Evaluated literally this is 1/(√(2π)·0.03) × exp(−0.5(0.05/0.03)²) = 13.298 × 0.2494 = 3.32/n_j; with the distance 0.02 it is 13.298 × 0.8007 = **10.65/n_j** (the normal density at 0.5 of N(0.52, 0.03²), i.e. what eq. (2) p_v(0.5)/n_j gives; for n = … (full text in the block) | https://sites.stat.columbia.edu/gelman/research/published/gelmankatzbafumi.pdf |
| [A] A-25 | §8 | GKB 1998 figures (six sub-claims; the first pass gives them all as "(Sec. 6.1)") (L205) | (wording) section "6.1" -> abstract, Sec. 4.3 (p. 5: "Figure 2 displays for the 1992 election ... The probability is about 1 in 10 million" for all states) and Sec. 6.1 (p. 6: "typically of order of magnitude 1 in 10 million"). It is a *prospective estimate* from a forecasting model, not a frequency. | https://sites.stat.columbia.edu/gelman/research/published/decisive2.pdf |
| [A] A-26 | §10 | The tie constant: GKB extract "(2/sqrt(pi))*(1/sqrt(n_j))" versus my exact 1/sqrt(2 pi N) for Q (vote versus a | the paper's constant is **√(2/π) ≈ 0.7979**, i.e. "Pr (a given vote is decisive in jurisdiction j) = p_{v_j}(0.5)/n_j = √(2/π) · 1/√n_j" (image, p. 662), not 2/√π = 1.128. The extract's form was a misreading of a radical lost in the text layer ("兹2/" with the π missing). HAND DERIVATION (paper's own definitions; arithmetic shown; numbers by SP/r4/work-A/calc1.py): 1. What is compared with what. Sec. 2.1 (quoted above): voter power = P(A wins \| this voter … (full text in the block) | https://sites.stat.columbia.edu/gelman/research/published/gelmankatzbafumi.pdf |
| [A] A-27 | §1 | (the first pass's Appendix equation "Pr = E[Phi(v - 1/n) - Phi(v)]" and the "random voting" constant were both | corrected (cross-reference only) | see A-13, A-26 |
| [A] F-2a | fill | Myerson (1998), "Population uncertainty and Poisson games", Int. J. Game Theory 27: definition of a pivot even | pages "385-392" (first pass, taken from Baltz's reference list: "International Journal of Game Theory, 27:385–392") -> **375-392** per the RePEc record (issue 3). Bouton's reference list (local `bouton.raw.txt`) cites a page 377 of this paper ("see Myerson 1998, p377, for more detail"), which is inside 375-392 and outside 385-392. [inferred] Baltz's "385" is a typo for 375. | https://econpapers.repec.org/RePEc:spr:jogath:v:27:y:1998:i:3:p:375-392 |
| [B] B-07 | §2 | First-round pivot events, four kinds, Table 1 (line 58) | (wording) the first pass writes the events as "i=ij", "ij=i", "i=j", "ki=kj"; the paper prints them with a slash: threshold pivotal i/ij and ij/i, above-threshold pivotal i/j, second-rank pivotal ki/kj (the "=" is an artefact of the text extraction; the page image shows "/"). The four kinds and their wording are right. Also the paper names the one-sided versions ij/i (against i) and i/ij (for i) as two events (Table 1 has four rows: i/ij, ij/i, i/j, ki/kj), and eq. … (full text in the block) | bouton.txt ; Sec. 3.1.2 and Table 1, printed pp. 10-11 (page image pdf p. 12, crop at 220 dpi) |
| [B] B-08 | §2 | First-round payoff G_1(i\|t) (eq. 4) "sums pivot probabilities times expected second-round utility differences" | "sums pivot probabilities times expected second-round utility differences" -> eq. (4) is a sum of ten terms, each a pivot probability times a utility difference, but only the two second-rank terms (display line 1) are differences of two expected second-round utilities, U(k,i\|t) - U(k,j\|t) and U(j,i\|t) - U(j,k\|t). The two above-threshold terms (line 2) are plain differences of utilities of outright winners, U(i\|t) - U(j\|t) and U(i\|t) - U(k\|t). The six … (full text in the block) | bouton.txt ; Sec. 3.2.2, eq. (4), printed p. 12 (page image pdf p. 13) |
| [B] B-10 | §2 | Lemma 2 (second round): "for a ballot to be pivotal, candidates have to receive (almost) the same number of vo | "constants not given" -> Lemma 2 states a closed form: mag(piv^2_PQ) = mag(piv^2_QP) = −(√τ²_P − √τ²_Q)², where τ²_ψ is the expected share of the electorate choosing action ψ in round 2 (eq. 2: τ^ρ(ψ) = Σ_t r(t) σ^ρ(ψ\|t)). It is zero if and only if τ²_P = τ²_Q. The proof (eq. 16) maximises at x* = n √(τ²_P τ²_Q). The first-round magnitudes are also closed-form: Lemma 3, eqs. (17)-(19), printed p. 39 (page image pdf p. 40). All in FORMULAS AS PRINTED. | bouton.txt ; Lemma 2 and its proof, App. A1, printed pp. 38-39 (page images pdf pp. 39-40) |
| [B] B-18 | §2 | Gap Le Pen minus Melenchon = 1.20 points; "The page gave no vote counts for Le Pen; the vote gap is therefore  | gap "not stated" -> Conseil constitutionnel's final counts: Le Pen 8,133,828; Mélenchon 7,712,520; gap = 8,133,828 - 7,712,520 = 421,308 votes [measured]; 421,308 / 35,132,947 = 1.199% of suffrages exprimés, which matches the 1.20 points. The percentage gap 23.15 - 21.95 = 1.20 [measured] is right. Interior's earlier figures quoted in LCP (a tweet by the deputy Adrien Quatennens, as LCP says) give Mélenchon 7,714,949 and a gap of 421,420; that is a … (full text in the block) | https://www.conseil-constitutionnel.fr/decision/2022/2022195PDR.htm |
| [B] B-34 | §5 | The authors say their results are a lower bound and "similar to prior empirical research and much lower than m | the first pass's quoted words "similar to prior empirical research and much lower than most theoretical research" are not in the abstract; the abstract's words are "similar to prior empirical research and much lower than what most theoretical research has found". The first pass's string may have come from the paper's body (unread) or may be an extractor paraphrase placed in quotation marks. Do not quote the first-pass form. | Crossref abstract (above) |
| [C] C-13 | §4 | BVerfG 30 July 2024, 2 BvF 1/23 and others: second-vote coverage compatible with the Basic Law (unanimous); 5% | (1) the phrase "in its current form unconstitutional" is not in the press release; the text is "in its current form is incompatible with the Basic Law" (section C.3) and, in the lead, "violates Art. 21(1) and Art. 38(1) first sentence"; the headline says "only the 5% electoral threshold is currently unconstitutional, but it will continue to apply under certain conditions". (2) "left in force the rule that parties under 5% still take part if..." -> the … (full text in the block) | https://bundesverfassungsgericht.de/SharedDocs/Pressemitteilungen/EN/2024/bvg24-064.html |
| [C] C-18 | §4 | candidate margin (open lists), p. 106 (line 114) | "p. 106" -> the section heading "2.2 Candidate Margin" starts at the bottom of p. 106 but the definition (the displayed equation) is on p. 107 (printed). Formula is in FORMULAS AS PRINTED (F-C). | https://doi.org/10.1017/pan.2023.22 |
| [C] C-27 | §4 | L&T "election-level pivotality" = vote-share-weighted average of within- and between-party measures, "the prob | "a vote-share-weighted average of within- and between-party measures" -> the paper says both "a weighted (by respective vote shares) average" and (next sentence) the single measure "is simply the sum of these weighted between and within pivotalities". The paper prints NO formula for the weights; there is no displayed equation for the aggregation (equation (5) on the next page is the IV system). The weights are only described as "respective vote shares". … (full text in the block) | https://www.doria.fi/bitstream/10024/148789/1/wp50.pdf |
| [C] C-30 | §4 | L&T within-party mean 0.006 (Table 2) versus 0.028 (Table A1, N = 146,234); paper says the gap "arise[s] mainl | The "inconsistency" is partly a difference of unit, as printed: Table 2 Panel B "Pivotality, within" is at the party-election level (N = 10,171; mean 0.006, sd 0.009, max 0.164); Table A1 "Real within" is at the election-candidate level (N = 146,234; mean 0.028, sd 0.051, max 0.389). The paper itself says the differences "arise mainly from the weighting" (Sec. 4.3). The paper does not give the weights (see C-27), so the two numbers cannot be reconciled … (full text in the block) | https://www.doria.fi/bitstream/10024/148789/1/wp50.pdf |
| [C] C-33 | §4 | L&T "smallest mainland municipality has roughly 800 inhabitants" vs Table 3 minimum population 234 (line 277) | "inconsistent" -> as printed there are two different statements: the text says the smallest *mainland* municipality has roughly 800 inhabitants; Table 3's population minimum over all 1,747 election observations is 234. Table 3 is population per municipality-election, with the "mainland" qualifier absent, so a non-mainland municipality (or a population figure in a particular election year) could be the 234; the paper does not say which, and does not say … (full text in the block) | https://www.doria.fi/bitstream/10024/148789/1/wp50.pdf |
| [C] C-36 | §4 | the press release attributes negative weight to second votes for parties that win overhang mandates in a Land  | "(it 'may arise in certain constellations')" is not verbatim; the text is "may lead to a situation in which in certain constellations second votes cast for parties which obtain what are known as 'overhang mandates' in one Land (state) have a negative impact inasmuch as these parties lose mandates in the same or in another Land". The effect is on parties losing mandates "in the same or in another Land" (the Court's own wording is about Land lists). The … (full text in the block) | https://www.bundesverfassungsgericht.de/SharedDocs/Pressemitteilungen/EN/2008/bvg08-068.html |
| [C] C-39 | §4 | FINAL totals and exact final shortfall of BSW to 5% (the first pass subtracted 13,435 - 4,277 = 9,158 and admi | 9,158 ("roughly 9,000 to 10,000") -> exact figures from the final result (second votes: BSW B = 2,472,947; valid second votes V = 49,649,512; share 4.981%). Shortfall to 5.000%: (a) if the extra BSW votes are switched from other parties' votes (V unchanged, the Stuttgarter Zeitung convention): need B + x >= V/20 = 2,482,475.6, so the least whole x is 2,482,476 - 2,472,947 = **9,529** votes. (b) if the extra BSW votes are new valid votes (e.g. from invalid … (full text in the block) | https://www.bundeswahlleiterin.de/en/bundestagswahlen/2025/ergebnisse/bund-99.html |
| [C] C-45 | §10 | L&T: "within-party pivotality is 0.006 in Table 2 but 0.028 in Table A1; the minimum municipal population is 2 | as printed: (i) 0.006 is Table 2 Panel B "Pivotality, within", unit = party-election (N 10,171); 0.028 is Table A1 "Real within", unit = election-candidate (N 146,234): two units, and the paper says "Differences to descriptions in Table A1 arise mainly from the weighting" (C-30); (ii) 234 is the minimum of the sample's population over 1,747 municipality-elections (Table 3), while "roughly 800" is about "the smallest mainland municipality" (the word … (full text in the block) | https://www.doria.fi/bitstream/10024/148789/1/wp50.pdf |
| [C] C-46 | §10 | BSW shortfall: "13,435 votes in the provisional count (Stuttgarter Zeitung) and 4,277 more votes in the final  | the final totals ARE readable: Bundeswahlleiterin results page, "Final result": BSW second votes 2,472,947 (4.981%), valid second votes 49,649,512. The final shortfall is 9,529 votes if the extra votes come from other parties' votes (total of valid votes unchanged; the convention of the Stuttgarter Zeitung's 13,435) and 10,031 votes if they are new valid votes (C-39); the first pass's subtraction 9,158 is 371 too low because it ignored that the 5% line … (full text in the block) | see C-37, C-38, C-39, C-11 |
| [D] D-03 | §6 | Art. 75 wording: "the majority of those with voting rights have voted" ... "a majority of votes validly cast h | "the majority of those with voting rights have voted" / "a majority of votes validly cast has been reached" -> "the majority of those eligible have participated in the vote" / "a majority of valid votes" (this translation). The two phrases the first pass put in quotation marks are from another translation (legislationline's), which I could not read; they are not in the official English text I read. The meaning is the same: two conditions, a turnout over … (full text in the block) | https://www.cortecostituzionale.it/documenti/download/pdf/Costituzione_italiana_english_version_ott2023.pdf |
| [D] D-04 | §6 | "A voter can then be pivotal for the quorum, not only the majority" and "Approval quorum: not read in any sour | "Approval quorum ... not read in any source other than as a lab treatment" -> approval-type thresholds are described in three further places: Herrera & Mattozzi's "majority quorum" (intro p. 2 and Sec. 8), Maniquet & Morelli's definition (IDEAS abstract of "Approval quorums dominate participation quorums", whose IDEAS page notes "In : Social Choice and Welfare, 45, 2015, p. 1-27"; abstract only, formulas not read), and Aguiar-Conraria's docx (approval … (full text in the block) | https://dait.interno.gov.it/documenti/dossier-referendum-2026.pdf |
| [D] D-06 | §6 | Lab model: 9 electors, binary choice, majority rule, voting costs c_i uniform on [0,c] (l.160) | "uniform on [0,c]" -> uniform on [0,100] (the docx writes "U0,100" after flattening; A.1 uses the ratio γ/c, so c = 100). Points, with 1 point = 0.05 EUR (Appendix 3, Screen 1). Also, the same electors' types are random: each draws a ball "A" or "B" with probability μ (A.1 uses μ; Appendix 3 Screen 3). | `quorum_docx.txt` (Appendix 1 and Appendix 3 of the online resource) |
| [D] D-16 | §6 | "The paper does not use the classic 'pivotal voter' concept" (l.161): the paper's sentence or the first pass's | the sentence in quotation marks is not in the paper. It is the extractor's (or the first pass's) paraphrase, and quote marks around it are wrong. What the paper does: a game between two parties who choose mobilisation spending; voters are a continuum of measure 1 with random cost c uniform on [0,1]; the "decisive event" is the joint event that reform's vote share beats the status quo's and turnout meets the quorum (D-17). The paper never models a single … (full text in the block) | `herrera.txt` and `herrera.raw.txt`: the strings "pivot" and "decisive" occur **zero** times in either file (`grep -c -i |
| [D] D-17 | §6 | Herrera & Mattozzi decisive-event formula P = Pr(vR >= vS and vR + vS >= q) (l.161) | first-pass "Pr(vR >= vS and vR + vS >= q)" -> printed first line is `P = Pr((v_R ≥ v)_S , (v_R + v_S ≥ q))`: the first condition's subscript S is placed outside the bracket (`(v_R ≥ v)_S`), a typesetting slip for `v_R ≥ v_S`; the second condition `(v_R + v_S ≥ q)` is as the first pass has it. The paper's second line, which restates the first in terms of r̃, the random share of voters who support reform, is `P = Pr( r̃ ≥ ρ(S)/(ρ(R)+ρ(S)) , (ρ(R) − ρ(S)) r̃ … (full text in the block) | `herrera.txt` Sec. 2, p. 4; I looked at the rendered page (`work-D/herrera_p-04.png`, 130 dpi) and transcribed what is p |
| [D] D-21 | §6 | Foellmi et al.: coefficient on distance -0.020 (SE 0.008) without, -0.021 (SE 0.009) with voting-day fixed eff | (wording) "they use ex-post distance of the Yes share from 50% as a proxy [for p] (coefficient on distance ...)" -> the table regresses the **average individual salience of each proposition** (dependent variable) on the ex-post distance of the Yes share from 50% (explanatory variable); its purpose is to show that "the probability of being decisive is indeed captured within the individual salience measure". Distance is not itself the proxy used in the voting model; … (full text in the block) | `foellmi.txt`, Table B.1 "Association Between Salience and Ex-Post Closeness of the Referendum", Sec. B.2 (appendix p. 7 |
| [D] D-30 | §7 | Gelman, King & Boscardin (1998), eq. 1: "Pr(your vote matters) = Pr(your vote is decisive in your state) x Pr( | printed eq. (1) second factor: "Pr(your state **will be** decisive \| your vote is decisive in your state)", not "Pr(your state **is** decisive \| ...)". The words "is decisive" are what eq. (3) prints for the left side of its expansion of the same factor ("Pr(your state is decisive \| your vote is decisive in your state)"). Same meaning, different tense; the first-pass quotation mixes the two. The vertical bar before "your vote is decisive in your state)" … (full text in the block) | https://sites.stat.columbia.edu/gelman/research/published/decisive2.pdf |
| [D] D-32 | §7 | Cooper & Munger (2000), "The (Un)Predictability of Primaries with Many Candidates: Simulation Evidence", Publi | (wording) first-pass "outcomes 'varied widely, by as much as two standard deviations from the median partisan voter'" -> the abstract says "the winner of the primary, or the party's nominee, varied as much as two standard deviations from the median partisan voter". The words "varied widely" and "by" are not in the abstract; the first pass's quotation marks enclose a paraphrase. The abstract also says "The key result of the simulations reported here is the complete … (full text in the block) | https://ideas.repec.org/a/kap/pubcho/v103y2000i3-4p337-55.html |
| [D] D-37 | §6 | l.180: "a quorum adds a second pivot event whose probability depends on the turnout forecast (not computed; no | corrected (a readable formula now exists in two sources) | `quorum_docx.txt` eqs. (A.2), (A.3) (n = 9; participation quorum 4) and `work-D/cirje_micro1204.txt` pp. 5-6 (general m  |
| [E] E-05 | §3 | line 78: notation (kappa, L, beta, S, A = [S_1..S_{kappa-1}, c], y, A' agreeing with A "up to c's position", " | "V_x, the cumulative expected vote total" -> the paper's symbols are v_c (the expected vote total of c) and mu^b_a \| S_{1:n} (the number of voters expected to rank a in positions 1..b given higher positions went to candidates in S_{1:n}); a candidate's total after d drops is v_c = sum_{q=0}^{d} mu^{q+1}_c \| S_{1:q} (p. 9). "A' agrees with A up to c's position" -> Constraint 1 as printed: A_{1:y-1} = A'_{1:y-1} (they agree up to position y-1, where y is … (full text in the block) | https://arxiv.org/pdf/2210.01657 |
| [E] E-24 | §1 | line 31 (caution, [inferred]): "values this small, at N = 1,000, most likely arise because the stylised electo | "the Baltz values (1e-7, 1e-6) are the levels at N = 1,000 and are not comparable to the 1/N scale" -> the 10^-6 / 10^-7 averages belong to the **power-law (clear front-runner) panel only**, drawn on a log10 axis; in the **uniform panel** at the same 1,000 voters the plotted totals are 0.003 to 0.12 (linear axis; mean lines about 0.03 to 0.08), which is the same order of magnitude as the first pass's 0.006 to 0.016 per ballot once one allows that Baltz's … (full text in the block) | https://arxiv.org/pdf/2210.01657 |
| [E] E-40 | §3 | (new) Conclusion rate range for monotonicity/no-show paradoxes | (not a first-pass claim; added because §10.1 and §10.3 quote "1.6% of 182") the paper's own Conclusion gives "0.5-1.1%" for these paradoxes, but its Table 7 gives upward monotonicity 1.6%, downward 1.1% and no-show 0.5%. So 1.6% (3 of 182) is the Table 7 / Sec. 6 figure for upward failure and the Conclusion's range omits it. Use Table 7 and the Sec. 6 list. | https://arxiv.org/pdf/2301.12075 |
| [E] E-44 | §3 | line 90 and §10.3 item 3: "the Alaska upward-monotonicity example is a hypothetical shift of 6,000 ballots" (l | "an inconsistency: the Alaska example is a hypothetical shift" -> not an inconsistency. Every monotonicity paradox in this paper (and in Ornstein & Norman) is *defined* by a hypothetical shift of ballots in the observed profile; the Burlington (750) and Minneapolis (456) examples are hypothetical shifts too. The Alaska election is counted as one of the 3 upward failures. The only point the first pass could note is that the 6,000 shift is given as the … (full text in the block) | https://arxiv.org/pdf/2301.12075 |
| [E] E-48 | §10 | item 3: "Graham-Squire & McCune internal inconsistencies (extractor): Table 7 prints 52.5% ... 95 of 182 is 52 | three flagged items -> two are in the paper as printed (52.5% vs 95/182 = 52.2%; "six" vs seven listed), one is not an inconsistency (the Alaska "hypothetical shift" is how all monotonicity paradoxes are defined); version read = **v2, 6 March 2023**. Two further inconsistencies in the paper found: Conclusion "0.5-1.1%" vs Table 7 upward 1.6% (E-40); Pierce County called 2009 in the text and 2008 in the Table 5 caption and Table 9 (E-39). | https://arxiv.org/pdf/2301.12075 |
| [E] E-49 | §10 | item 4: "Baltz's simulated probabilities (about 1e-7 for plurality and 1e-6 for IRV at 1,000 voters) versus th | "(about 1e-7 for plurality and 1e-6 for IRV at 1,000 voters)" -> those averages are for the power-law, clear-front-runner panel only (log axis, IRV about 10^-5.6 to 10^-5.9, SMDP about 10^-7.6 to 10^-8.9 by the plotted mean lines, individual runs from about 10^-2.4 down to 10^-12.5); for the uniform panel at the same 1,000 voters the plotted y-values are 0.003 to 0.12 (mean lines about 0.03 to 0.08), a sum over all ballots. "Fig. 1 data and Assumptions 1 … (full text in the block) | baltz_arxiv.raw.txt, baltz_sup.raw.txt and the two Figure 1 images; see the Reconciliation section below |
| [F] F-03 | §5 | "The page shows no pivot analysis; the PDF body was not read" (line 146) | "PDF body not read; no pivot analysis" -> body now read (1991 working-paper version): the paper uses "pivotal" qualitatively (an equilibrium concept called "individually stable", in which at least one voter is pivotal; examples in which the voters are or are not pivotal) but prints no pivot probability, no formula for one, and no estimate. The first pass's claim that nothing quantitative about pivot probability is there stands. | https://authors.library.caltech.edu/records/ev76a-f2977/files/sswp772.pdf?download=1 |
| [F] F-12 | §8 | GKB 1998: second factor is "Pr(E_{P_i} in (.5 e_total - e_i, .5 e_total) \| v_i = .5), with a factor 1/2 becaus | first pass: one factor Pr(E in (.5 e_total - e_i, .5 e_total) \| v_i = .5) "with a factor 1/2" -> Eq. (3) as printed has THREE terms: Pr(E_{-i} in (.5 e_total - e_i, .5 e_total) \| v_i = .5) + (1/2) Pr(E_{-i} = .5 e_total - e_i \| v_i = .5) + (1/2) Pr(E_{-i} = .5 e_total \| v_i = .5). The two factors of 1/2 weight the two exact-tie end points; the interval term has no 1/2. The symbol is E_{-i} (Democratic electoral votes in the 49 states excluding i, plus the … (full text in the block) | https://sites.stat.columbia.edu/gelman/research/published/decisive2.pdf |
| [F] F-14 | §8 | GKB 2004: "the second factor is, per the extract, roughly proportional to e_j" (line 201) | "second factor ... roughly proportional to e_j" -> in GKB 2004 it is "Factor 1", the probability that the jurisdiction's electoral votes are decisive (written first in the product of Sec. 2.2); "Factor 2" is the within-jurisdiction probability, p_{v_j}(0.5)/n_j. The order of the two factors is the reverse of GKB 1998 (where the in-state factor is first and the "state decisive" factor second). The proportionality to e_j holds under random voting when "the … (full text in the block) | https://sites.stat.columbia.edu/gelman/research/published/gelmankatzbafumi.pdf |
| [F] F-20 | §8 | GKT 2002: Statistical Science 17(4), Caltech working paper 1141, URL records/hpnm8-cmw66 (line 202) | "Statistical Science 17(4)" -> volume and issue are not printed on either source read; the Caltech page gives "Statistical Science, 420-435" (2002) and a related DOI 10.1214/ss/1049993201. Working paper 1141 is confirmed (October 2002). | https://authors.library.caltech.edu/records/hpnm8-cmw66 |
| [F] F-22 | §8 | GKT 2002: body not read - definition of voting power and treatment of two-stage elections (lines 202, 10.3 con | "I did not read the body" -> read. Definition as printed: power_i = Pr(R=+1 \| v_i=+1) - Pr(R=+1 \| v_i=-1) (Eq. 1), i.e. the difference between the vote being cast for each side (not versus abstaining); the abstract's "probability that a single vote is decisive" is the same quantity under that definition. Two-stage: Sec. 3.2 computes, under random voting, the within-jurisdiction probability as Pr(V_{-i}=0) + (1/2)Pr(\|V_{-i}\|=1) = C(n_j - 1, (n_j - 1)/2) … (full text in the block) | https://authors.library.caltech.edu/records/hpnm8-cmw66/files/sswp1141.pdf?download=1 |
| [F] F-24 | §8 | Line 205: GKB 1998 figures "(Sec. 6.1)": about 1 in 10 million (1992); 1 in 3.5 million in Vermont; 1 in 1.5 m | section attribution: the first pass puts all of line 205's EC figures under "Sec. 6.1". As printed, "1 in 3.5 million in Vermont" (1992) and "on the order of 1 in hundreds of millions" (the landslide elections of 1964, 1972, 1984) are in Sec. 4.3 (Numerical Results); Sec. 6.1 (Concluding Remarks) prints "typically of order of magnitude 1 in 10 million, rising to as much as about 1 in 1.5 million for some small states in some close elections (e.g., Nevada … (full text in the block) | https://sites.stat.columbia.edu/gelman/research/published/decisive2.pdf |
| [F] F-25 | §8 | Line 205: GKB 1998 "1 in 10,000" as upper bound for a typical 200,000-voter congressional race; empirical Hous | section: both are in Sec. 5 (journal p.6: Sec. 5 text, then Sec. 6.1 on the same page), not Sec. 6.1. The bound is printed as "20/n": with a forecast "normal distribution with mean mu and standard deviation tau" the single-vote decisive probability is "approximately (sqrt(2 pi) tau n)^-1 exp(-(mu - .5)^2/(2 tau^2))" (Sec. 5, "as discussed by Margolis (1977)"), maximal at mu = .5; with tau = 2% of the vote ("hard to imagine a real election that could be … (full text in the block) | https://sites.stat.columbia.edu/gelman/research/published/decisive2.pdf |
| [F] F-35 | §9 | Farber: "averaging 50 to 75 eligible voters" (Sec. 1.2) (line 230; section as cited by the first pass and in § | section "Sec. 1.2" -> Sec. 2.3 ("Voter Turnout", printed p.10); the quoted words are exact. "50 to 75" is the span of the y-axis of Fig. 1 (average number of eligible voters, 5-year moving average) for ALL elections closed by the NLRB, and Sec. 2.1 describes it as about 55 rising to about 70 workers per election. | https://www.nber.org/system/files/working_papers/w16160/w16160.pdf |
| [F] F-36 | §9 | Farber: "from 24 to 30 between 1972 and 2008" (Sec. 6.2) (line 230; §10.3 item 7, line 279) | "from 24 to 30 between 1972 and 2008" is exact (printed p.39); the first pass's citation to "Sec. 6.2" is right. What the first pass lacks: the sentence does not say which sample the average is over. In Sec. 6.2 the model estimated is the beta-binomial of Table 2 (sample of on-site elections with 2-200 eligible voters). | https://www.nber.org/system/files/working_papers/w16160/w16160.pdf |
| [F] F-44 | §9 | Ballotpedia: "496 by fewer than five votes" (line 234) | the page prints 496, and the page's own table does not support it: [measured, from the 733 table rows] margins: 1 vote 104, 2 votes 96, 3 votes 64, 4 votes 88, 5 votes 84, 6 votes 71, 7 votes 52, 8 votes 60, 9 votes 68, 10 votes 46. Fewer than five (margin 1-4): 352; five or fewer: 436; six or fewer: 507. No threshold reproduces 496. | https://ballotpedia.org/Races_decided_by_10_votes_or_fewer |
| [F] F-47 | §9 | Ballotpedia: largest visible total 23,525 (a 2022 Massachusetts House race) (line 234) | "largest visible total 23,525" -> 23,525 is the largest total among the 104 one-vote rows (the last of them), not in the whole table; the largest total in the full table is 393,922 (Iowa District 2, 2020, 196,964 to 196,958, margin 6). Next largest [measured]: 129,553 (AZ House 9, 2020, margin 9), 129,420 (Travis County Court at Law, TX, 2020, margin 4), 123,148 (NY Senate 50, 2022, margin 10), 80,489 (AZ House 27, 2022). | https://ballotpedia.org/Races_decided_by_10_votes_or_fewer |
| [F] F-52 | §9 | Ballotpedia table and text: consistency (added, not in the first pass) | first pass assumes the page's figures are mutually consistent apart from 0.004% and 660 -> three further inconsistencies between the text and the saved table [measured]: (a) 734 stated vs 733 table rows; (b) Republicans 191 stated vs 190 in the table; (c) "496 fewer than five" stated vs 352 (margin 1-4) in the table. | https://ballotpedia.org/Races_decided_by_10_votes_or_fewer |
| [F] F-56 | §10 | §10.3 item 7: Farber average election size "50 to 75 eligible voters" (Sec. 1.2) versus "from 24 to 30" (Sec.  | "(Sec. 1.2)" -> Sec. 2.3 (printed p.10) for "50 to 75"; "Sec. 6.2" for "24 to 30" is right. | https://www.nber.org/system/files/working_papers/w16160/w16160.pdf |

## Formulas as printed (collected from the readers)

*Each reader transcribed the formulas that bear on its sections from the source, exactly as printed, from page images where the text layer garbles. The notation is the paper's; nothing was simplified or repaired, and misprints in the sources are noted where the reader found them.*

### Reader A
(Each was read from a page image; the text layers garble the Greek letters, radicals, fractions and minus signs. Notation: ≈_{n→∞} is the paper's "asymptotically equivalent" symbol.)

###### Myatt & Fisher (2002), Oxford DP 115 (local: myatt_fisher; page images PDF pp. 7-10 = printed pp. 6-9)
- Setup (Sec. 2.1, p. 5): m candidates j ∈ {1,…,m}; n + 1 individuals, voter i = 0 instrumental, the other n voters produce x = [x_j]_{j=1}^m ∈ X = {x ∈ Z^m_+ | Σ_{j=1}^m x_j = n}; "Each individual casts a single vote, and there are no abstentions"; ties "broken at random". p ∈ △ = {p ∈ R^m_+ | Σ p_j = 1}; given p, x is multinomial(p, n); the voter's belief is the density f(p), "continuous and strictly positive on the interior of △".
- Definition 1 (p. 6): g(x,n) ≈_{n→∞} h(x,n) iff lim_{n→∞} max_{x∈X} {g(x,n)/h(x,n)} = lim_{n→∞} min_{x∈X} {g(x,n)/h(x,n)} = 1.
- Eq. (1) (p. 6): Pr[x] = ∫_△ Pr[x | p] f(p) dp = ∫_△ (n!/∏_{j=1}^m x_j!) ∏_{j=1}^m p_j^{x_j} f(p) dp = (n!/∏_{j=1}^m x_j!) ∫_△ ∏_{j=1}^m p_j^{x_j} f(p) dp.
- Proposition 1 (p. 7): "In a large electorate, Pr[x] is proportional to f(x/n). Formally: Pr[x] ≈_{n→∞} f(x/n) · (n!/∏_{j=1}^m x_j!) ∫_△ ∏_{j=1}^m p_j^{x_j} dp = (1/n^{m−1}) f(x/n) ⇒ Pr[x]/Pr[x̃] ≈_{n→∞} f(x/n)/f(x̃/n)". (So the printed statement is "f(x/n) times 1/n^{m−1}"; m is the number of candidates.)
- Lemma 1 (pp. 8-9), m = 3 only: "Two-way and near two-way ties are asymptotically equivalent; for instance: Pr[x1 − 1 = x2 > x3] ≈_{n→∞} (∫_{1/3}^{1/2} f(z, z, 1 − 2z) dz)/(6n) ≈_{n→∞} Pr[x1 = x2 > x3 + 1]   (2), with similar expressions available for Pr[x1 = x3 > x2] and Pr[x2 = x3 > x1]. Three way and near three-way ties are asymptotically equivalent, and satisfy: Pr[x1 = x2 = x3 + 1] ≈_{n→∞} (1/n²) f(1/3, 1/3, 1/3) ≈_{n→∞} Pr[x1 = x2 = x3]   (3), where the first equivalence applies for (n − 1)/3 ∈ N and the second for n/3 ∈ N." [measured: the "6" in (2) should be 1 for f a density in (p1,p2) coordinates, and the first n-condition should be (n − 2)/3 ∈ N: A-06]
- Sentence after Lemma 1 (p. 9): "Notice, however, that the probability of a three-way tie vanishes at rate n^{−2}, whereas the probability of a two-way tie vanishes at rate n^{−1}, and so three-way and near three-way ties are asymptotically irrelevant to voter i = 0."
- Table 1 (p. 8), "Pivotal Events and Voter Payoffs". Columns: Event | u(Vote 1) | u(Vote 2) | u(Vote 1) − u(Vote 2) | Description | ∗ (the last column's mark means "relevant"). Rows, in print order:
   1. x1 = x2 = x3 | u1 | u2 | (u1 − u3) − (u2 − u3) | Three Way Tie
   2. x1 = x2 = x3 + 1 | u1 | u2 | (u1 − u3) − (u2 − u3) | Near Three Way Tie
   3. x1 = x3 = x2 + 1 | u1 | (u1 + u2 + u3)/2 | (u1 − u2 − u3)/2 | Near Three Way Tie
   4. x2 = x3 = x1 + 1 | (u1 + u2 + u3)/2 | u2 | (u1 + u3 − u2)/2 | Near Three Way Tie
   5. x1 = x2 > x3 + 1 | u1 | u2 | (u1 − u3) − (u2 − u3) | Two Way Tie | ∗
   6. x1 = x3 > x2 + 1 | u1 | (u1 + u3)/2 | (u1 − u3)/2 | Two Way Tie | ∗
   7. x2 = x3 > x1 + 1 | (u2 + u3)/2 | u2 | −(u2 − u3)/2 | Two Way Tie | ∗
   8. x1 − 1 = x2 = x3 | u1 | (u1 + u2)/2 | [(u1 − u3) − (u2 − u3)]/2 | Near Three Way Tie
   9. x1 − 1 = x2 > x3 | u1 | (u1 + u2)/2 | [(u1 − u3) − (u2 − u3)]/2 | Near Two Way Tie | ∗
  10. x1 − 1 = x3 > x2 | u1 | u1 | 0 | Near Two Way Tie
  11. x2 − 1 = x1 = x3 | (u1 + u2)/2 | u2 | [(u1 − u3) − (u2 − u3)]/2 | Near Three Way Tie
  12. x2 − 1 = x1 > x3 | (u1 + u2)/2 | u2 | [(u1 − u3) − (u2 − u3)]/2 | Near Two Way Tie | ∗
  13. x2 − 1 = x3 > x1 | u2 | u2 | 0 | Near Two Way Tie
  14. x3 − 1 = x1 = x2 | (u1 + u3)/2 | (u2 + u3)/2 | [(u1 − u3) − (u2 − u3)]/2 | Near Three Way Tie
  15. x3 − 1 = x1 > x2 | (u1 + u3)/2 | u3 | (u1 − u3)/2 | Near Two Way Tie | ∗
  16. x3 − 1 = x2 > x1 | u3 | (u2 + u3)/2 | −(u2 − u3)/2 | Near Two Way Tie | ∗
  (u1 > u2 > u3 "without loss of generality", p. 7. Rows 3 and 4 are printed with denominator 2 in the three-way payoff; a uniform random tie-break among three would give 3: [inferred].)
- Proposition 2, Eqs. (4)-(5) (p. 9): "Assuming without loss of generality that an indifferent voter i = 0 casts her vote in favor of candidate 1, the optimal voting rule is asymptotically equivalent to: Vote 1 ⇔ log[(u1 − u3)/(u2 − u3)] (labelled "Relative Preference") ≥ log[(2 Pr[x1 = x2 > x3] + Pr[x2 = x3 > x1]) / (2 Pr[x1 = x2 > x3] + Pr[x1 = x3 > x2])]   (4)   ≈_{n→∞} log[(p23 + 2 p12)/(p13 + 2 p12)] ≡ λ ("Strategic Incentive")   (5), where p12 = ∫_{1/3}^{1/2} f(z, z, 1 − 2z) dz, p13 = ∫_{1/3}^{1/2} f(z, 1 − 2z, z) dz and p23 = ∫_{1/3}^{1/2} f(1 − 2z, z, z) dz."
- Definition 2 (p. 10): "When λ ≥ 0, define the intensity of the strategic incentive as Λ = 1 − e^{−λ}."
- Proof of Lemma 1 (Appendix A, p. 29), the line that drops the 6: "n Pr[x1 = x2 > x3] = Σ_{n/3<i≤n/2} (1/n) n² Pr[i, i, n − 2i] ≈ (1/n) Σ f(i/n, i/n, (n − 2i)/n) … The sum on the right hand side has approximately n/6 elements. Multiplying and dividing by 6, this summation defines a Riemann integral over the set [1/3, 1/2]. Indeed: n Pr[x1 = x2 > x3] ≈ (1/6)(1/(n/6)) Σ_{n/3<i≤n/2} f(i/n, i/n, (n − 2i)/n) → (1/6) ∫_{1/3}^{1/2} f(z, z, 1 − 2z) dz." (Reading from the image of the Appendix is not done: this is from the text layer of Appendix A, printed p. 29; the equation signs are the text layer's. I did not render the Appendix page.)

###### Gelman, Katz & Bafumi (2004) (local: gkb2004; page images PDF pp. 5, 6, 7, 18)
- Sec. 2.2, eq. (1) (p. 661): Pr(jurisdiction j's e_j electoral votes are decisive) = Pr(E_{−j} ∈ (0.5E − e_j, 0.5E)) + (1/2) Pr(E_{−j} = 0.5E − e_j) + (1/2) Pr(E_{−j} = 0.5E)   (1).
- eq. (2) (p. 661): Pr(a given vote is decisive in jurisdiction j) = p_{v_j}(0.5)/n_j   (2).
- Sec. 2.2.1 (p. 661): probability 1/2^{J−1} to each configuration of the other J − 1 jurisdictions; (p. 662) "the linear fit has a relative error of less than 10 per cent for all states".
- Sec. 2.2.2 (p. 662): "Pr (a given vote is decisive in jurisdiction j) = p_{v_j}(0.5)/n_j = √(2/π) · 1/√n_j ." and "What matters for comparing voters is not the constant factor √(2/π) but the proportionality with 1/√n_j."
- Sec. 2.3 (p. 663): "[1/√2π (0.03)] exp(−0.5(0.05/0.03)²)/n_j = 1.84/n_j" (radical over 2π only, as printed; see A-15 for the arithmetic).
- Sec. 3.1 (p. 666): "we fit a curve of the form y = c/√n_j ... Thirdly, we find the best-fitting curve of the form y = c n_j^α", Fig. 1 α = −0.16; Sec. 5.2: α = −0.494 on permuted districts.
- Appendix, eq. (3) (p. 674): Pr(decisive vote) = E[π(v + 1/n) − π(v)] = Σ_v [π(v + 1/n) − π(v)] p(v)   (3); then = ∫_{0.5−ε}^{0.5+ε} [π(v + 1/n) − π(v)] p(0.5) dv = p(0.5)[1/n · 1 − 1/n · 0] = p(0.5)/n. π(v) = probability that A wins given true proportion v; v = proportion in favour of A excluding your potential vote.

###### Gelman, King & Boscardin (1998) (local: gkb1998_columbia; page images PDF pp. 3, 5, 6)
- Eq. (1) (p. 3): Pr(your vote matters) = Pr(your vote is decisive in your state) × Pr(your state will be decisive | your vote is decisive in your state).
- Eq. (2) (p. 3): Pr(your vote is decisive in your state) = Pr(n_i v_i = .5 n_i) = Pr(v_i = .5) ≈ f_{v_i}(.5)/n_i; if n_i odd: Pr(n_i v_i = .5(n_i − 1)) = Pr(v_i = .5 − .5/n_i) ≈ f_{v_i}(.5)/n_i.
- Eq. (3) (p. 3): Pr(your state is decisive | your vote is decisive in your state) = Pr(E_{−i} ∈ (.5 e_total − e_i, .5 e_total) | v_i = .5) + (1/2) Pr(E_{−i} = .5 e_total − e_i | v_i = .5) + (1/2) Pr(E_{−1} = .5 e_total | v_i = .5)   (subscript "−1" as printed in the last term).
- Eq. (5) (p. 5): Pr(n_i v_i = .5 n_i | β, γ, δ, θ, σ²) [n_i even] or Pr(n_i v_i = .5(n_i − 1) | …) [n_i odd] ≈ (1/n_i) N(.5 | (Xβ)_i + γ_{r_i} + δ, n_i^{−θ} σ²), N(x | μ, τ²) the normal density.
- Sec. 5 (p. 6): approximately (√(2π) τ n)^{−1} exp(−(μ − .5)²/(2τ²)); upper bound 20/n for τ = 2%; presidential frequency calculation: .18/(.04 n_i) per state; ".008 e_i/n_i" combined.

###### Mebane, Baltz & Vasselai (2019) (local: A_mebane2019; page images PDF pp. 10-12 = printed pp. 8-10)
- (3): N_e ∼ Pois(μ).  (4): n_h ∼ Pois(p_h μ).
- (5): P(X − Y = z) = S(z; μ_x, μ_y) = exp(−(μ_x + μ_y)) (μ_x/μ_y)^{z/2} I_z(2√(μ_x μ_y)), "where I_z(·) is a Bessel function of the first kind. S(·) is the Skellam distribution".
- μ̃_h = p_h(μ − 1) ("an imagined electorate that does not include its own vote").
- (6): pv_h = Σ_{j≠h} [ P(μ̃_h − μ̃_j = 0 | μ̃_h, μ̃_j ≥ μ̃_m ∀ m ≠ j, h) + P(μ̃_h − μ̃_j = −1 | μ̃_h, μ̃_j ≥ μ̃_m ∀ m ≠ j, h) ] ∏_{m≠j,h} P(μ̃_h − μ̃_m > 0).
- (7): pv_h = Σ_{j≠h} [ S(0; μ̃_h, μ̃_j) + S(−1; μ̃_h, μ̃_j) ] ∏_{m≠j,h} ( Σ_{w=1}^{∞} S(w; μ̃_h, μ̃_m) ).  Footnote 5: "Three-way ties are ignored."
- (8a) E^i_jh = α^i_{1jh} u^i_j + α^i_{2jh} (u^i_j + u^i_h)/2 + α^i_{3jh} u^i_j + α^i_{4jh} u^i_h;  (8b) E^i_{∅jh} = α^i_{1jh} (u^i_j + u^i_h)/2 + α^i_{2jh} u^i_h + α^i_{3jh} u^i_j + α^i_{4jh} u^i_h.
- (9a) R^i_j = Σ_{h≠j} [E^i_jh − E^i_{∅jh}] − c^i;  (9b) = Σ_{h≠j} (α^i_{1jh} + α^i_{2jh})(u^i_j − u^i_h) − c^i;  (9c) = Σ_h P^i_jh B^i_jh − c^i, P^i_jh = α^i_{1jh} + α^i_{2jh}, B^i_jh = u^i_j − u^i_h.
- (10): P^i_jh = [S(0; μ̃_j, μ̃_h) + S(−1; μ̃_j, μ̃_h)] ∏_{m≠j,h} ( Σ_{w=1}^{∞} S(w; μ̃_h, μ̃_m) ).  [My algebra: E_jh − E_∅jh from (8a)-(8b) = (α1 + α2)(u_j − u_h)/2, so (9b) as printed lacks a factor 1/2 (F-1 NOTE d).]

###### Myatt (2004 DP 186; RES 2007 version unread) (local: A_myatt2007wp; page image PDF pp. 17-18 = printed pp. 16-17)
- Proposition 1 (p. 16), under Lemma 3 (f(p | δ) continuous, strictly positive on (0,1)): lim_{n→∞} (n + 1) q1 = f(γ | δ), lim_{n→∞} (n + 1) q2 = f(1 − γ | δ), and lim_{n→∞} q1/q2 = f(γ | δ)/f(1 − γ | δ). q1 = Pr[x = ⌈γn⌉] = ∫_0^1 C(n, ⌈γ n⌉) [p^{γ_n}(1 − p)^{1−γ_n}]^n f(p | δ) dp.

###### Bouton (author's draft; second-hand for Myerson 2000) (local: bouton; page image PDF p. 39 = printed p. 38)
- Property 1: mag(E^ρ) ≡ lim_{n→∞} log[Pr(E^ρ)]/n = max_{x^ρ∈E} Σ_ψ (x^ρ_ψ/n)(1 − log(x^ρ_ψ/(n τ^ρ_ψ))) − 1, mag ∈ [−1, 0]. Property 2: mag(E^ρ) < mag(E^ρ′) ⇒ Pr(E^ρ)/Pr(E^ρ′) → 0. Lemma 2: mag(piv²_PQ) = mag(piv²_QP) = −(√τ²_P − √τ²_Q)².

---


### Reader B

All from page images, transcribed as printed. "pdf p." is the PDF page; printed page = pdf page - 1 for the Bouton draft.

**Bouton draft (bouton.txt), page images viewed: pdf pp. 12, 13, 18, 19, 20 (top, Table 3), 23, 39, 40 (Table 1 also at 220 dpi; Lemma 2 and Lemma 3 at 200 dpi).**

Eq. (2) (Sec. 2, printed p. 8; the file shows it garbled, read from the layout text and the sentence beside it): τ^ρ(ψ) = Σ_t r(t) σ^ρ(ψ|t), "the expected share of voters who choose action ψ in round ρ"; E[x^ρ_ψ | σ] = τ^ρ(ψ) n.

Table 1 (printed p. 11; pdf p. 12; "first-round pivotal events"; ζ is the threshold; i, j, k distinct candidates):
- Threshold pivotal i/ij; piv^1_{i/ij}: x^1_i + 1 − ζ > ζ(x^1_i + x^1_j + x^1_k) ≥ x^1_i ≥ x^1_j ≥ x^1_k
- Threshold pivotal ij/i; piv^1_{ij/i}: ζ(x^1_i + x^1_j + x^1_k + 1) ≥ x^1_i > ζ(x^1_i + x^1_j + x^1_k) > x^1_j ; and x^1_i ≥ x^1_j ≥ x^1_k
- Above-threshold pivotal i/j; piv^1_{i/j}: x^1_i = x^1_j − 1 ≥ ζ(x^1_i + x^1_j + x^1_k) ≥ x^1_k
- Second-rank pivotal ki/kj; piv^1_{ki/kj}: x^1_i = x^1_j − 1 ; and ζ(x^1_i + x^1_j + x^1_k) ≥ x^1_k > x^1_j
(The first row's left part, "x^1_i + 1 − ζ > ζ(…)", is printed exactly so in Table 1, in the footnotes to Tables 2-4 and in the proof of Lemma 3. The paper warns the conditions are "necessarily loose" (footnote 22).)

Eq. (3) (printed p. 11): G²(P|t) = Pr(piv²_PQ) [U(P|t) − U(Q|t)].  By definition G²(∅|t) = 0 ∀t.

Definition of the second-round expected utility (printed p. 12): U(i,j|t) = Pr(i|{i,j}) U(i|t) + Pr(j|{i,j}) U(j|t), with Pr(j|{i,j}) = 1 − Pr(i|{i,j}).

Eq. (4) (printed p. 12; pdf p. 13), i, j, k ∈ {A,B,C}, i ≠ j ≠ k:
G¹(i|t) = Pr(piv¹_{ki/kj}) [U(k,i|t) − U(k,j|t)] + Pr(piv¹_{ji/jk}) [U(j,i|t) − U(j,k|t)] +
 Pr(piv¹_{i/j}) [U(i|t) − U(j|t)] + Pr(piv¹_{i/k}) [U(i|t) − U(k|t)] +
 Pr(piv¹_{i/ij}) [U(i|t) − U(i,j|t)] + Pr(piv¹_{i/ik}) [U(i|t) − U(i,k|t)] +
 Pr(piv¹_{ji/j}) [U(j,i|t) − U(j|t)] + Pr(piv¹_{jk/j}) [U(j,k|t) − U(j|t)] +
 Pr(piv¹_{ki/k}) [U(k,i|t) − U(k|t)] + Pr(piv¹_{kj/k}) [U(k,j|t) − U(k|t)],
and G¹(∅|t) = 0 ∀t (footnote 24). The paper's sentence under it: display line 1 = second-rank pivotal events; line 2 = above-threshold; "the three last lines refer to the gains when the ballot is threshold pivotal" (lines 3-5): ten terms in all, two on each of five display lines.

Poisson probabilities (App. A1, printed p. 37): Pr(x^ρ_ψ) = exp(−nτ^ρ_ψ)(nτ^ρ_ψ)^{x^ρ_ψ}/x^ρ_ψ!  (14), and the product over ψ for an action profile (15).

Property 1 (App. A1, printed p. 38; pdf p. 39): mag(E^ρ) ≡ lim_{n→∞} log[Pr(E^ρ)]/n = max_{x^ρ∈E} Σ_ψ (x^ρ_ψ/n) (1 − log(x^ρ_ψ/(nτ^ρ_ψ))) − 1.  "mag(E^ρ) ∈ [−1, 0]".
Property 2: mag(E^ρ) < mag(E^ρ') ⇒ Pr(E^ρ)/Pr(E^ρ') → 0 as n → ∞.

Lemma 2 (printed p. 38; pdf p. 39): mag(piv²_PQ) = mag(piv²_QP) = −(√τ²_P − √τ²_Q)².
Eq. (16): lim log[Pr(x²_P = x²_Q)]/n = max_{x²} Σ_ψ (x²_ψ/n)(1 − log(x²_ψ/(nτ²_ψ))) − 1  s.t. x²_P = x²_Q; maximised at x* = n√(τ²_P τ²_Q); value −(√τ²_P − √τ²_Q)².

Lemma 3 (printed p. 39; pdf p. 40), eqs. (17)-(19):
(a) Threshold pivot probability i/ij and ij/i (17): mag(piv¹_{i/ij}) = mag(piv¹_{ij/i}) =
 ((τ¹_j + τ¹_k)/(1−ζ))^{1−ζ} (τ¹_i/ζ)^ζ − 1   if ζ/(1−ζ) ≥ τ¹_j/(τ¹_j+τ¹_k) ≥ 1/2;
 (√(τ¹_iτ¹_j)/ζ)^{2ζ} (τ¹_k/(1−2ζ))^{1−2ζ} − 1   if τ¹_j/(τ¹_j+τ¹_k) > ζ/(1−ζ) ≥ 1/2;
 (2√(τ¹_jτ¹_k)/(1−ζ))^{1−ζ} (τ¹_i/ζ)^ζ − 1   if ζ/(1−ζ) ≥ 1/2 > τ¹_j/(τ¹_j+τ¹_k).
(b) Above-threshold pivot probability i/j and j/i, for ζ < 1/2 (18): mag(piv¹_{i/j}) = mag(piv¹_{j/i}) =
 −(√τ¹_i − √τ¹_j)²   if √(τ¹_iτ¹_j) ≥ τ¹_k ζ/(1−2ζ);
 (√(τ¹_iτ¹_j)/ζ)^{2ζ} (τ¹_k/(1−2ζ))^{1−2ζ} − 1   if τ¹_k ζ/(1−2ζ) > √(τ¹_iτ¹_j).
(c) Second-rank pivot probability ki/kj and kj/ki (19): mag(piv¹_{ki/kj}) = mag(piv¹_{kj/ki}) =
 −(√τ¹_i − √τ¹_j)²   if 2ζ/(1−ζ) √(τ¹_iτ¹_j) > τ¹_k > √(τ¹_iτ¹_j);
 (2√(τ¹_iτ¹_j)/(1−ζ))^{1−ζ} (τ¹_k/ζ)^ζ − 1   if τ¹_k ≥ 2ζ/(1−ζ) √(τ¹_iτ¹_j) > √(τ¹_iτ¹_j);
 3(τ¹_iτ¹_jτ¹_k)^{1/3} − 1   if 2ζ/(1−ζ) √(τ¹_iτ¹_j) > √(τ¹_iτ¹_j) ≥ τ¹_k.
(Page image pdf p. 40, crop at 200 dpi, and verified numerically against Table 2: see F-02.)

Table 2 (printed p. 18; pdf p. 19): ζ = 0.5, r(t_AB) = 0.3, r(t_BA) = 0.26, r(t''_CA) = 0.44: mag(piv¹_{A/AC}) = −0.0835; mag(piv¹_{B/BC}) = −0.1227; mag(piv¹_{BA/BC}) = −0.0251; mag(piv¹_{CA/CB}) = −0.0014 (bold); mag(piv¹_{AB/AC}) = −0.0251.
Table 4 (printed p. 22; pdf p. 23): ζ = 0.4 (printed on p. 21: "ζ = 0.4; r(t_AB) = 0.30, r(t_BA) = 0.29, and r(t''_CA) = 0.41"): threshold −0.0223 (A/AC), −0.0273 (B/BC), −0.0002 (CA/C, bold), −0.0003 (CB/C); above-threshold −0.0304 (A/C), −0.0370 (B/C), −0.0953 (A/B); second-rank −0.0125 (BA/BC), −0.0003 (CA/CB, bold), −0.0125 (AB/AC).

**Bouton & Gratton (2015) (bg_te.txt; page images viewed: pdf pp. 23 and 24):** μ(E) ≡ lim log[Pr(E)]/n = max_{x∈E} Σ_i (x_i/n)(1 − log(x_i/(nτ_i))) − 1 (printed p. 305); Lemma 3 (printed pp. 305-306), threshold 1/2: μ(piv_{i/ij}) = μ(piv_{ij/i}) = 2√((τ_j + τ_k)τ_i) − 1 if τ_j/(τ_j+τ_k) ≥ 1/2, and 2√(2τ_i √(τ_jτ_k)) − 1 otherwise; μ(piv_{ki/kj}) = μ(piv_{kj/ki}) = −(√τ_i − √τ_j)² if 2√(τ_iτ_j) > τ_k > √(τ_iτ_j); 2√(2τ_k √(τ_iτ_j)) − 1 if τ_k > 2√(τ_iτ_j); 3(τ_iτ_jτ_k)^{1/3} − 1 if √(τ_iτ_j) > τ_k.

**Lepelley, Chantreuil & Berg (1996) (page images viewed: pdf pp. 4, 5, 6, 7, 8, 9):**
Eq. (1): |S| = (n+1)(n+2)(n+3)(n+4)(n+5)/120 (the OCR prints "(n+5)5 − ..." for the binomial C(n+5, 5)).
Cor. 1: V11(n) = n(26n⁴ − 325n³ − 760n² + 9360n + 19584) / [576 (n+1)(n+2)(n+3)(n+4)(n+5)] for n ∈ {24, 36, 48, 60, ...}; lim V11 = 13/288 ≅ 0.0451.
Cor. 2: V21(n) = n(2n⁴ − 15n³ + 60n² − 180n − 432) / [36 (n+1)...(n+5)]; lim V21 = 1/18 ≅ 0.0556.
Cor. 3: V12(n) = n(17n⁴ − 495n³ + 4200n² − 6480n − 24192) / [864 (n+1)...(n+5)]; lim V12 = 17/864 ≅ 0.0197.
Cor. 4: V22(n) = n(7n⁴ + 30n³ − 600n² + 6048) / [108 (n+1)...(n+5)]; lim V22 = 7/108 ≅ 0.0648.
(Cor. 2-4 were checked on the page images pdf pp. 6-7 and by recomputation against Table 2: they reproduce the table to five digits except the two cells named in B-28.)
Sec. 3.1: Ṽ1(∞) = 13/288 + 17/864 − 17/2304 = 397/6912 ≅ 0.0574; Ṽ2(∞) = 1/18 + 7/108 − 5/1296 = 151/1296 ≅ 0.1165.

**STV quota:** Scottish Local Government Elections Order 2007, rule 46: quota = (valid ballot papers ÷ (councillors + 1), "ignoring any decimal places") + 1. Ireland's Electoral Commission: "(total number of valid ballot papers) dividing it by (the number of seats to be filled plus one) and then adding one". Laird et al. (page 3): q = ⌈ total votes / (available seats + 1) ⌉.

---


### Reader C

Source for F-A to F-D: Luechinger, Schelker & Schmid, Political Analysis 32 (2024) 101-114, https://doi.org/10.1017/pan.2023.22, Cambridge Core PDF (local SP/r4/src/luechinger_cup.out; text SP/r4/txt/luechinger.raw.txt). I rendered PDF pp. 4, 5, 6, 7 (= printed pp. 104, 105, 106, 107) as images (130 dpi; crops at 220 dpi for the equations on pp. 104-105) and transcribed the equations from the images; none of these equations carries an equation number in the paper. Notation (p. 104): "a district with J parties Pj indexed by j ∈ P ≡ {1, 2, . . . , J}. The party index of all parties other than j is −j ∈ P\{j}. A total number of n seats are allocated. The index i ∈ {1, 2, . . . , n} denotes the potential seats of party Pj. Similarly, ĩ captures the potential seats of each of the other parties P−j. We denote a party Pj's total number of votes by votes_j." Negative margins are shortfalls, positive are surpluses (p. 104).

**F-A. D'Hondt (highest average) party margin, printed p. 104 (image):**

    party margin_{i,j} = votes_j − i ( votes_{−j} / ĩ )_{(n(J−1)−(n−i))}.

The subscript "(n(J−1)−(n−i))" is an order statistic over the n(J−1) ratios votes_{−j}/ĩ of the other parties (ĩ = 1..n); the paper does not say ascending or descending, but the paper's numbers (C-15) only come out if it is counted from the smallest ratio [measured by hand]; the paper says it is "the one with the order statistic (n(J − 1) − (n − i ))" for the (n − i + 1)th-highest D'Hondt ratio. The sentence before: the party margin is the vote change at which "the ith-highest D'Hondt ratio of party Pj equals the (n − i + 1)th-highest D'Hondt ratio of all other J − 1 parties". The first pass's transcription "votes_j - i x (votes_{-j}/i~)_{(n(J-1)-(n-i))}" is symbol-for-symbol the same. [measured, by hand] On the paper's example (n = 3, J = 3, votes 45/35/20) it gives 15, -10, -100 for P2 (C-15, C-20).

**F-B. Largest remainder (Hare-Niemeyer), printed pp. 105-106 (images):**

    Hare-Niemeyer quota = ( votes_j + Σ_{−j} votes_{−j} ) / n          (p. 105, in text)
    floor( votes_j / quota ) and mod( votes_j / quota )                  (p. 105, in text)

    Condition (equal remainders after i−1 and ĩ−1 first-round seats), p. 105:
    votes_{i,ĩ,j,−j} × n / ( Σ_{−j} votes_{−j} + votes_{i,ĩ,j,−j} ) − (i − 1)  =  votes_{−j} × n / ( Σ_{−j} votes_{−j} + votes_{i,ĩ,j,−j} ) − (ĩ − 1).

    Rewritten, p. 105:
    votes_{i,ĩ,j,−j} = ( votes_{−j} × n + (i − ĩ) Σ_{−j} votes_{−j} ) / ( n − (i − ĩ) ),   where 1 ≤ ĩ ≤ n − i + 1.

    Second step, pp. 105-106 (ratios with the new index −j̃ = same values as −j):
    ratio = votes_{−j̃} × n / ( Σ_{−j̃} votes_{−j̃} + votes_{i,ĩ,j,−j} )
    F_{i,ĩ,j,−j} = n − (i − 1) − Σ_{−j̃} floor( votes_{−j̃} × n / ( Σ_{−j̃} votes_{−j̃} + votes_{i,ĩ,j,−j} ) )
    R_{i,ĩ,j,−j,−j̃} = rank( mod( votes_{−j̃} × n / ( Σ_{−j̃} votes_{−j̃} + votes_{i,ĩ,j,−j} ) ) )

    Third step, p. 106: "(J − 1) × (2n + 1) possible solutions"; the relevant solution votes*_{i,ĩ,j,−j} satisfies
    F_{i,ĩ,j,−j} = R_{i,ĩ,j,−j,−j̃},
    −j̃ = −j, and
    (i − 1) = floor( votes_{i,ĩ,j,−j} × n / ( Σ_{−j̃} votes_{−j̃} + votes_{i,ĩ,j,−j} ) ).

    Fourth step, p. 106:
    party margin_{i,j} = votes_{i,j} − votes*_{i,ĩ,j,−j}.

[measured, by algebra] the closed form follows from the condition (x n − v n)/(S + x) = i − ĩ with x = votes_{i,ĩ,j,−j}, v = votes_{−j}, S = Σ_{−j} votes_{−j}; for the paper's example (n = 3, i = 2, ĩ = 1, v = 20, S = 65) it gives 62.5, the paper's value; the paper's margin for P2's second seat is 35 − 62.5 = −27.5. Note a notational oddity as printed: the first formula uses the subscripts "i,ĩ,j,−j" on the votes, while the final line uses "votes_{i,j}" for the actual votes.

**F-C. Candidate margin, printed p. 107 (image):**

    candidate margin_{h,i,j} = votes_{h,j} − (votes_{−h,j})_{(n_j − i + 1)}   if i < n_j,
                               votes_{h,j}                                    if i = n_j.

with h ∈ H ≡ {1, ..., n_j} the candidates of party Pj, n_j the number of candidates, −h ∈ H\{h}; "the one with the order statistic (n_j − i + 1)" (p. 107). Footnote 6: "To be the lowest-ranked candidate (i = n_j), candidate C_h could lose all her votes."

**F-D. Overall vote margin, printed p. 107 (image):**

    vote margin_{h,i,j} = max_{i ∈ {1,...,n}} { min{ party margin_{i,j}, candidate margin_{h,i,j} } }.

(As printed, the left side carries the subscript i although the maximum is over i.)

**F-E. L&T "election-level pivotality" aggregation: NO FORMULA IS PRINTED.** Source: https://www.doria.fi/bitstream/10024/148789/1/wp50.pdf, printed p. 20 (PDF p. 23; image read), in words only: "we take a weighted (by respective vote shares) average over both the within party pivotal probability (measured at the candidate level) and the between parties pivotal probability (measured at the party level) to calculate the probability that a randomly drawn voter would be pivotal in a given election. We use either a single measure for pivotality, which is simply the sum of these weighted between and within pivotalities, or both of them separately." (Text-layer file lyyt.txt.) The displayed equations of that section are the IV system (5) on printed p. 21 (Pivotality_it = β1 + β2 Group2_it + ... + β3 Group6_it + f(Pop_it) + u_it, etc.), which is a regression, not the aggregation. L&T's pivotal-event definition (Sec. 4.2, printed p. 17): a draw (lottery) or "giving one more vote creates a draw or a different seat allocation directly".

**F-F. IDEA Handbook, STV Droop quota, printed p. 76 (image read):**

    Quota = ( votes / (seats + 1) ) + 1

(as printed: the fraction votes over "seats +1", then "+1" after the fraction.) The Handbook's glossary words for Droop (list-PR use) are "the total valid vote divided by the number of seats to be filled in the electoral district plus one" (F-1, F-2).

**F-G. German divisor rule (statute, in words), BWahlG § 5(1)-(3):** the number of second votes is divided by a "Zuteilungsdivisor" and rounded (fractions under 0.5 down, over 0.5 up; ties by lot, constrained so that the number of available seats is met); the divisor is "so bestimmt, dass alle verfügbaren Sitze verteilt werden" (start from the sum of votes divided by seats, then raised or lowered). No formula is printed; quotes in C-41 and F-4.

**F-H. Threshold arithmetic (mine, [measured]; not from a source).** With B = BSW's votes, V = valid second votes: V fixed, need x_fixed = ceil(V/20) − B; new valid votes, need x_new = ceil((V − 20B)/19) (from (B + x)/(V + x) ≥ 1/20). Final: B = 2,472,947, V = 49,649,512: x_fixed = 2,482,476 − 2,472,947 = 9,529; x_new = ceil(190,572/19) = ceil(10,030.105...) = 10,031 (work-C/bsw.py).


### Reader D

###### 1. Aguiar-Conraria, Magalhaes & Vanberg, online resource "Appendix 1 ― The mathematics of the pivotal voter model with quorum requirements" (Experimental Economics 19(4) 2016 [inferred from the article id and IDEAS], source `quorum_docx.txt`)
Not a page image: transcribed from the Word equation XML (OMML) through `pandoc -t latex` (`work-D/docxconv/quorum_pandoc.tex`, lines 18-96), with the orchestrating thread's flattened text as a cross-check. Fractions printed as a fraction, sums with their limits, brackets as printed. n = 9 electors; c = 100.
Definitions in the text: "Let γs and γo be those cutoff values for supporters of Change and Opponents, respectively." "let ρvo,vs be the probability that elector i attaches that, among the other electors, vo vote ‘No’ and vs vote ‘Yes’." Footnote 1: "This is an obvious abuse of notation, as ρ(.) depends on the strategies of the other players, which also depend on the existing quorum requirement." (read on the LibreOffice render, p. 1; the text file may not carry it).
(A.1), as printed:
`ρ(v_s, v_o) = Σ_{s = v_s}^{n−1−v_o} C(s, v_s) (γ_s/c)^{v_s} (1 − γ_s/c)^{s − v_s} C(n−1−s, v_o) (γ_o/c)^{v_o} (1 − γ_o/c)^{n−1−s−v_o} C(n−1, s) μ^s (1 − μ)^{n−1−s}`   (C(a,b) is the binomial coefficient, printed as a 2-row bracket)
with, in the text before it, `P(s; i) = C(n−1, s) μ^s (1−μ)^{n−1−s}`, `V(v_s) = C(s, v_s) (γ_s/c)^{v_s} (1 − γ_s/c)^{s−v_s}`, `V(v_o) = C(n−1−s, v_o) (γ_o/c)^{v_o} (1 − γ_o/c)^{n−1−s−v_o}`. Note A.1's left side is ρ(v_s, v_o), while the sentence defining the symbol writes ρ(v_o, v_s).
No-quorum pivot probabilities (text, no equation number): Supporter `[ Σ_{v=0}^{4} ρ(v,v)/2 + Σ_{v=0}^{3} ρ(v+1,v)/2 ]`; Opponent `Σ_{v=0}^{4} ρ(v,v)/2 + Σ_{v=0}^{3} ρ(v,v+1)/2`.
(A.2), Supporter (b = benefit if "Yes" wins), three lines:
- NQ: `[ Σ_{v=0}^{4} ρ(v,v)/2 + Σ_{v=0}^{3} ρ(v+1,v)/2 ] b = γ_s`
- PQ = 4: `[ Σ_{v=2}^{4} ρ(v,v)/2 + Σ_{v=1}^{3} ρ(v+1,v)/2 + ρ(1,2) + ρ(0,3) ] b = γ_s`
- AQ = 3: `[ Σ_{v=3}^{4} ρ(v,v)/2 + Σ_{v=2}^{3} ρ(v+1,v)/2 + Σ_{v=0}^{2} ρ(v,2) ] b = γ_s`
(A.3), Opponent (x = benefit if "Yes" loses), three lines:
- NQ: `[ Σ_{v=0}^{4} ρ(v,v)/2 + Σ_{v=0}^{3} ρ(v,v+1)/2 ] x = γ_o`
- PQ = 4: `[ Σ_{v=2}^{4} ρ(v,v)/2 + Σ_{v=2}^{3} ρ(v+1,v)/2 − ρ(1,2)/2 − ρ(0,3) ] x = γ_o`
- AQ = 3: `[ Σ_{v=3}^{4} ρ(v,v)/2 + Σ_{v=2}^{3} ρ(v,v+1)/2 ] x = γ_o`
Flag (D-10): the Opponent's PQ line uses ρ(v+1,v) where its NQ and AQ lines use ρ(v,v+1). The first-pass transcription (l.160) copies the PQ lines as printed.

###### 2. Herrera & Mattozzi, "Quorum and Turnout in Referenda", This Version 15 May 2006 (`herrera.txt`), p. 4 (looked at the rendered page `work-D/herrera_p-04.png`)
`v_R = r̃ ρ(R),   v_S = (1 − r̃) ρ(S).`
`P = Pr((v_R ≥ v)_S , (v_R + v_S ≥ q))`   (as printed: the subscript S sits outside the bracket; read `v_R ≥ v_S`)
`  = Pr( r̃ ≥ ρ(S)/(ρ(R)+ρ(S)) , (ρ(R) − ρ(S)) r̃ ≥ q − ρ(S) ).`
`Q = (q − ρ(S))/(ρ(R) − ρ(S)),   K = ρ(S)/(ρ(R) + ρ(S)).`
Objectives (p. 3): `π_r = B P − R`, `π_s = B(1 − P) − S`; `Pr(ρ(R) > c) = ρ(R)`.
Sec. 8 "Majority Quorum", p. 20 (text-layout copy `herrera.txt` line 1020; not looked at as an image): `P = Pr((v_R > m) ∩ (v_R > v_S))`, where the reform party needs a share above m of the whole electorate, m in [0, 1/2].

###### 3. Hizen, "A Referendum Experiment with Participation Quorums" (draft Nov 2012; looked at rendered pp. 5-6)
`p_i = Σ_{k=0}^{([rm]−1)/2} (m−1)! / ( k! ([rm]−1−k)! (m−[rm])! ) · π_i^{[rm]−1−k} π_j^{k} π_a^{m−[rm]}`, with `π_y = s σ_y`, `π_n = (1−s) σ_n`, `π_a = 1 − π_y − π_n`.
`q_i = Σ_{k=0}^{([rm]−1)/2 − 1} (m−1)! / ( k! ([rm]−1−k)! (m−[rm])! ) · π_i^{k} π_j^{[rm]−1−k} π_a^{m−[rm]}`.
`t_i = ½ Σ_{k=([rm]−1)/2}^{(m−1)/2 − 1} (m−1)! / ( k! (k+1)! (m−2k−2)! ) π_i^{k} π_j^{k+1} π_a^{m−2k−2}  +  ½ Σ_{k=([rm]−1)/2 + 1}^{(m−1)/2} (m−1)! / ( k! k! (m−2k−1)! ) π_y^{k} π_n^{k} π_a^{m−2k−1}`.
Condition (1): `(1 − v) p_i + t_i ≥ v q_i`.
(i, j in {y, n}, j ≠ i; m voters; [rm] the smallest integer ≥ rm; σ_i the probability that a voter with preference i votes.)

###### 4. Gelman, King & Boscardin (1998), p. 3 (looked at the rendered page)
(1) `Pr(your vote matters) = Pr(your vote is decisive in your state) × Pr(your state will be decisive | your vote is decisive in your state).`
(2) `Pr(your vote is decisive in your state) = Pr(n_i v_i = .5 n_i) = Pr(v_i = .5) ≈ f_{v_i}(.5)/n_i`.
(3) `Pr(your state is decisive | your vote is decisive in your state) = Pr(E_{−i} ∈ (.5 e_total − e_i, .5 e_total) | v_i = .5) + ½ Pr(E_{−i} = .5 e_total − e_i | v_i = .5) + ½ Pr(E_{−1} = .5 e_total | v_i = .5).` The third term reads "E_{−1}" in the image (the line is cut at the bottom of my crop); it is probably a typo for E_{−i}, not changed. Definitions: `n_i` = voters in state i excluding yourself; `v_i` = Democratic share of the two-party vote in state i excluding your vote; `E_{−i} = Σ_{j≠i} e_j V_j + 3`.

---


### Reader E

All Baltz arXiv page numbers are the PDF's printed page numbers (v2, 31 Jul 2023). I looked at the page image for each equation (pp. 7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20; supplement pp. 8, 12). Ornstein & Norman pp. 3-4 also by image.

**V-1** Expected vote total after d drops (p. 9, image):
  v_c = mu^1_c | S_{1:0} + mu^2_c | S_{1:1} + ... + mu^{d+1}_c | S_{1:d}      (with labels: "c first, vacuous condition", "c second, any dropped candidate first", "c ranked in d+1, all candidates ranked 1 to d dropped")
  v_c = sum_{q=0}^{d} mu^{d+1}_c | S_{1:q}      [as printed: the superscript is d+1 in this second line, q+1 in the rest of the paper]
  P(v_c - v_j = k)   (the probability that c has k more votes than j; no formula given for it)

**A-1** Assumptions (p. 7, image; "E1 perp E2 perp E3 means that events E1, E2 and E3 are pairwise independent"):
  Assumption 1: [ v^r_A >= v^r_B ] perp [ v^r_A >= v^r_C ] perp [ v^r_C >= v^r_D ]
  Assumption 2: [ v^r_A >= v^r_B ] perp [ v^{r'}_A >= v^{r'}_B ] perp [ v^{r'}_A >= v^{r'}_C ] perp [ v^{r'}_C >= v^{r'}_D ]
  "where A != C, A != D, B != C, and B != D."

**P-0** Direct pivotality given a drop sequence S (p. 10, image):
  p_d | S = P(v_c = v_{S_{-1}}) . [ ( P(mu^1_c > mu^1_{S_1}) ) ( P(mu^2_c | S_1 > mu^2_{S_2} | S_1) ) ... ( P(mu^{kappa-2}_c | S_{1:kappa-3} > mu^{kappa-2}_{S_{kappa-2}} | S_{1:kappa-3}) ) ]
  p_d | S = P( mu^{kappa-1}_c | S_{1:-1} = mu^{kappa-1}_{S_{-1}} | S_{1:-1} ) . prod_{h=1}^{kappa-2} P( mu^h_c | S_{1:h-1} > mu_{S_h} | S_{1:h-1} )

**P-0b** (p. 11, image; the version for the drop list A, with the tie-break factor):
  p_d(A) = P(v^1_{S_1} < v^1_{S_2}) P(v^1_{S_1} < v^1_{S_3}) ... P(v^1_{S_1} < v^1_{S_{-1}}) P(v^1_{S_1} < v^1_c) . P(v^2_{S_2} < v^2_{S_3}) ... P(v^2_{S_2} < v^2_{S_{-1}}) P(v^2_{S_2} < v^2_c) . ... . P(v^{kappa-2}_{S_{kappa-2}} < v^{kappa-2}_{S_{-1}}) P(v^{kappa-2}_{S_{kappa-2}} < v^{kappa-2}_c) . P(v^{kappa-1}_{S_{-1}} = v^{kappa-1}_c) . 1/2
  p_d(A) = [ prod_{l=1}^{kappa-2} prod_{r=l+1}^{kappa} P(v^l_{A_l} < v^l_{A_r}) ] P(v^{kappa-1}_{A_{kappa-1}} = v^{kappa-1}_c) . 1/2      (labels: "Probability the candidates are dropped in order A", "Probability that c is in a first-place tie given the drop order A", "Probability after tying c loses")
  (p. 12, image) p_d(A) = [ prod_{l=1}^{kappa-2} prod_{r=l+1}^{kappa} P( sum_{q=0}^{l-1} mu^{q+1}_{A_l} | A_{1:q} < sum_{q=0}^{l-1} mu^{q+1}_{A_r} | A_{1:q} ) ] P( sum_{q=0}^{kappa-2} mu^{q+1}_{A_{kappa-1}} | A_{1:q} = sum_{q=0}^{kappa-2} mu^{q+1}_c | A_{1:q} ) . 1/2

**P-1** p_direct (the quantity the first pass reconstructs), final form (p. 13, image; "assuming a fair tie-breaker"):
  p_direct(beta) = sum_{i=1}^{L} ( sum_{S in Sym(C\i), beta_{1:i-1} subset of S} { [ prod_{l=1}^{kappa-2} prod_{r=l+1}^{kappa} P( sum_{q=0}^{l-1} mu^{q+1}_{A_l} | A_{1:q} < sum_{q=0}^{l-1} mu^{q+1}_{A_r} | A_{1:q} ) ] .
      [ 1/2 . P( sum_{q=0}^{kappa-2} mu^{q+1}_{A_{kappa-1}} | A_{1:q} = sum_{q=0}^{kappa-2} mu^{q+1}_i | A_{1:q} ) + 1/2 . P( sum_{q=0}^{kappa-2} mu^{q+1}_{A_{kappa-1}} | A_{1:q} = 1 + sum_{q=0}^{kappa-2} mu^{q+1}_i | A_{1:q} ) ] } )
  (p. 12 has the break-only version: the same without the second tie term and with the single factor 1/2 . P( ... = ... ) after the product.)

**P-2a** Tie probability and A -> A' switch (pp. 14-16, images):
  p_tie | A' = sum_{t in A_{y+1:kappa}} [ 1/2 . P( v^y_c = v^y_t ) + 1/2 . P( v^y_c = v^y_t - 1 ) ]                                  (p. 14)
  p_tie(A' | A) = prod_{d=1}^{|G|} [ prod_{h=1}^{d-1} P( v_{G_d} > v_{G_h} ) ] . [ 1/2 . P( v^y_c = v^y_t ) + 1/2 . P( v^y_c = v^y_t - 1 ) ]      (p. 15, image)
  p_tie | A = sum_{A' in bold-A} { prod_{d=1}^{|G|} [ prod_{h=1}^{d-1} P( v_{G_d} > v_{G_h} ) ] . [ 1/2 . P( v^y_c = v^y_t ) + 1/2 . P( v^y_c = v^y_t - 1 ) ] }      (p. 15, image; "Let bold-A denote the set of all A' that, for a given A, fulfill Conditions 1 and 2")
  p_{not d}(A -> A') = prod_{l=2}^{kappa} [ prod_{h=1}^{l-1} P( v_{A_l} > v_{A_h} ) ] . sum_{A' in bold-A} { [ prod_{d=1}^{|G|} prod_{h=1}^{d-1} P( v_{G_d} > v_{G_h} ) ] . [ 1/2 . P( v^y_c = v^y_t ) + 1/2 . P( v^y_c = v^y_t = -1 ) ] }      (p. 16, image: note the printed "= -1" in the last term; pp. 14, 15 and 16 (second display) print "- 1")

**P-2b** p_indirect(beta), in terms of vote totals v (p. 16, image):
  p_indirect(beta) = sum_{i=1}^{L} ( sum_{A in Sym(C), beta_{1:i} subset of A_{1:y}} [ prod_{l=2}^{kappa} prod_{h=1}^{l-1} P( v_{A_l} > v_{A_h} ) ] . sum_{A' in bold-A} { [ prod_{d=1}^{|G|} prod_{h=1}^{d-1} P( v_{G_d} > v_{G_h} ) ] . sum_{t in F} [ 1/2 . P( v^y_c = v^y_t ) + 1/2 . P( v^y_c = v^y_t - 1 ) ] } )
  ("F" is not defined anywhere in the text.)

**P-3** p_indirect(beta), in terms of the mu's (p. 17, image):
  p_indirect(beta) = sum_{i=1}^{L} ( sum_{A in Sym(C), beta_{1:i} subset of A_{1:y}} [ prod_{l=2}^{kappa} prod_{h=1}^{l-1} P( sum_{q=0}^{h-1} mu^{q+1}_{A_l} | A_{1:q} > sum_{q=0}^{h-1} mu^{q+1}_{A_h} | A_{1:q} ) ] .
      sum_{A' in bold-A} { [ prod_{d=1}^{|G|} prod_{h=1}^{d-1} P( sum_{q=0}^{y+d} mu^{q+1}_{G_d} | A_{1:q} > sum_{q=0}^{y+d} mu^{q+1}_{G_h} | A_{1:q} ) ] .
      [ 1/2 . P( sum_{q=0}^{y} mu^{q+1}_c | A_{1:q} = sum_{q=0}^{y} mu^{q+1}_t | A_{1:q} ) + 1/2 . P( sum_{q=0}^{y} mu^{q+1}_c | A_{1:q} = sum_{q=0}^{y} mu^{q+1}_t | A_{1:q} - 1 ) ] } ) )
  Definitions (p. 18, below the u(beta) display): "bold-A is the set of all ordered lists A' formed by pre-pending A_{1:y} to G, for every G in the symmetric group of the set C \ A_{1:y}", y = "the index in the list A of the candidate ranked at position i", t = "the candidate in A'_y".

**P-4** Expected utility of a ballot (pp. 17-18, images; the display is on p. 18): u(beta) = [the p_direct(beta) of P-1 with each term multiplied by ( u(i) - u(S_{-1}) )] + [the p_indirect(beta) of P-3 with each term multiplied by ( u(A'_{-1}) - u(A_{-1}) )]; "where Sym(C) is the symmetric group of the set C, L is the length of the ballot beta such that L <= kappa".

**P-5** Skellam form (p. 20, image), S(w, a, b) being a named function (the Skellam pmf of the difference of two Poissons with means a and b; it is not written out):
  u(beta) = sum_{i=1}^{L} ( sum_{S in Sym(C\i), beta_{1:i-1} subset of S} { [ prod_{l=1}^{kappa-2} prod_{r=l+1}^{kappa} sum_{w=0}^{infinity} S( w, sum_{q=0}^{l-1} mu^{q+1}_{A_r} | A_{1:q}, sum_{q=0}^{l-1} mu^{q+1}_{A_l} | A_{1:q} ) ] . [ 1/2 . S( 0, sum_{q=0}^{kappa-2} mu^{q+1}_{A_{kappa-1}} | A_{1:q}, sum_{q=0}^{kappa-2} mu^{q+1}_i | A_{1:q} ) + 1/2 . S( 1, sum_{q=0}^{kappa-2} mu^{q+1}_{A_{kappa-1}} | A_{1:q}, sum_{q=0}^{kappa-2} mu^{q+1}_i | A_{1:q} ) ] } . ( u(i) - u(S_{-1}) )
        + sum_{A in Sym(C), beta_{1:i} subset of A_{1:y}} [ prod_{l=2}^{kappa} prod_{h=1}^{l-1} sum_{w=0}^{infinity} S( w, sum_{q=0}^{h-1} mu^{q+1}_{A_l} | A_{1:q}, sum_{q=0}^{h-1} mu^{q+1}_{A_h} | A_{1:q} ) ] . sum_{A' in bold-A} { [ prod_{d=1}^{|G|} prod_{h=1}^{d-1} sum_{w=0}^{infinity} S( w, sum_{q=0}^{y+d} mu^{q+1}_{G_d} | A_{1:q}, sum_{q=0}^{y+d} mu^{q+1}_{G_h} | A_{1:q} ) ] . [ 1/2 . S( 0, sum_{q=0}^{y} mu^{q+1}_c | A_{1:q}, sum_{q=0}^{y} mu^{q+1}_t | A_{1:q} ) + 1/2 . S( 1, sum_{q=0}^{y} mu^{q+1}_c | A_{1:q}, sum_{q=0}^{y} mu^{q+1}_t | A_{1:q} ) ] } . ( u(A'_{-1}) - u(A_{-1}) ) )
  Here the direct "break/make" terms use S(0, ., .) and S(1, ., .) (the main-text form), whereas the pseudocode and the worked example in the supplement use S(0, ., .) and S(-1, ., .) or "S(0, a, 1 + b)". The pseudocode (p. 21-22; identical in the supplement p. 13-14) prints "breakTieProb <- S(0, v_i, v_{S_{-1}})" and "makeTieProb <- S(-1, v_i, v_{S_{-1}})" for direct pivotality and "makeProb <- S(0, v_i, v_t - 1)" for indirect, with chain probabilities "sum_{w=1}^{infinity} S(w, ., .)" (w from 1 there, from 0 in the displayed formulas).

**S-1** Supplement worked example conventions (p. 8, image): "C = sum_{w=0}^{infinity} S(w, a, b), which is the probability that a > b when a, b are random variables following the Poisson distribution".
  p_direct(S) = C(2,2) . C(3,2) . C(6,2) . C(12,2) . C(3+0,2+0) . C(6+2,2+0) . C(12+0,2+0) . C(6+2+2,3+0+0) . C(12+0+0,3+0+0) . ( S(0, 6+2+2+0, 12+0+0+0) + 1/2 . S(0, 6+2+2+0, 1+12+0+0+0) )     [printed: the 1/2 multiplies only the second S]; "p_direct(S) ≈ 0.023"
  p_{not d}(E) = C(2,2) . C(3,2) . C(3+0,2+0) . C(6,2) . C(6+2,2+0) . C(6+2+2,3+0+0) . C(12,2) . C(12+0,2+0) . C(12+0+0,3+0+0) . C(6+2+2+3,12+0+0+0) . C(3,2) . C(6,2) . C(6+0,3+0) . C(2,2) . C(2+2,3+0) . C(2+2+3,6+0+0) . C(12,2) . C(12+0,3+0) . C(12+0+0,6+0+0) . C(12+0+0+6,2+2+3+0) . ( S(0,2,2) + 1/2 . S(0,2,2-1) )     (p. 12; "p_{not d}(E) ≈ 0.003")
  **My recomputation of both** ([measured], `ex.py`, `ex2.py`; Skellam pmf by direct summation, C(a,b) = P(Poisson(a) >= Poisson(b))): the product of the C factors in p_direct(S) is 0.31375, S(0,10,12) = 0.07827, S(0,10,13) = 0.06903. As literally printed, p_direct(S) = 0.0354. With the 1/2 on **both** tie terms (as in the main-text formula, P-1) it is 0.0231, which matches the printed "≈ 0.023". For p_{not d}(E): the C product is 0.03255, S(0,2,2) = 0.2070, S(0,2,1) = 0.2117; as printed it is 0.0102; with the 1/2 on both terms 0.00681; with only the first tie term (1/2 . S(0,2,2)) 0.00337, which is the only variant near the printed "≈ 0.003". So the printed direct example is reproduced only if the 1/2 multiplies both tie terms, and the printed indirect example is reproduced (to one digit) only if the second tie term is dropped or the printed 0.003 has a slip; I cannot tell which. These are illustrations in the supplement, not inputs to Figure 1.

**E-1** Eggers & Nowacki's second-round pivot event as translated by Baltz (supplement p. 20-22, text extract; images not looked at): pi_{ij,2} = Pr( v_j + v_{kj} - 1/2 in (0, N^{-1}) and v_k < v_i and v_k < v_j ), which Baltz rewrites for counts as pi_{xy,2} = P(v_y + v_{zy} = v_x + v_{zx}) + P(v_y + v_{zy} = 1 + v_x + v_{zx})) . P(v_z < v_x) . P(v_z < v_y), and then says it "exactly matches" his p_direct with L = 2, kappa = 3 and the identity pi_{xy,2} = 2 . p_direct (the factor 2 undoes the tie-break halves, the sum over ballot positions omitted).

**O-1** Ornstein & Norman (p. 3-4, images): P' = <a1 + lambda1 + lambda2, a2, b1 - lambda1, b2 - lambda2, c1, c2>; (1) c > (V + 2)/4 with c = c1 + c2; (2) c + b2 > V/2; (3) (b1 - lambda1) + (b2 - lambda2) + c > V/2; (4) (b1 - lambda1) + (b2 - lambda2) <= c - 1; (5) c + b2 - lambda2 > V/2. Utility (eq. 6, p. 5, text): u_j(y) = ( sum_{i=1}^{n} (x_{ji} - y_i)^2 )^{-1/2} (n = 2); voters rank candidates in decreasing utility ("in increasing order of utility" is what the text extract prints; I did not look at the image of p. 5).

**AL-1** Allard (1996), conditions as printed in the HTML text (the area formulas P1 are images, not in my extract): a > b > c; a < b + alpha x c; exists x with a - x > b, c + x > b, a > c + 2x + beta x b; equivalently M1. b > c, M2. a < b + alpha x c, M3. a > max{2b - c, (2 + beta) b - c}; alpha = T_CB - T_CA, beta = T_BC - T_BA, T_ij = "the proportion of i's votes which transfer to j if i is eliminated".

---


### Reader F

Notation: plain text; "sum_{a}^{b}" is a sum with limits a and b; subscripts with underscores; transcribed from page images unless the source line says "text layer".

**Farber (NBER WP 16160, July 2010)** (https://www.nber.org/system/files/working_papers/w16160/w16160.pdf). Eqs. (12) and (13) read from page images (PDF pp.17 and 18 = printed pp.15 and 16, work-F/farber_p-17.png and farber_p-18.png); the rest from the text layer (farber.txt) and checked against the images of (9)-(11).
- (4)  C_i <= b dW+   [pro-union worker votes if]
- (5)  p_p = mu G(b dW+)
- (6)  C_i <= b dW-   [anti-union worker votes if]
- (7)  p_c = (1 - mu) G(b dW-)
- (8)  p_v = p_p + p_c = mu G(b dW+) + (1 - mu) G(b dW-)
- (9)  p_a = 1 - p_v = 1 - mu G(b dW+) - (1 - mu) G(b dW-)
- (10) Pr(n_p, n_c, n_a) = [ N! / ( n_p! n_c! n_a! ) ] p_p^{n_p} p_c^{n_c} p_a^{n_a}
- (11) theta = sum_{n_p=1}^{N} sum_{n_c=0}^{Min[n_p - 1, N - n_p]} Pr(n_p, n_c, n_a)      [theta = probability of a union victory]
- (12) dW+ = Pr(n_p = n_c) = sum_{i=0}^{INT(n/2)} [ n! / ( i! i! (n - 2i)! ) ] p_p^i p_c^i p_a^{n-2i},   where n = N - 1, "the number of eligible voters less one and INT(.) returns the truncated integer value of its argument".
- (13) dW- = Pr(n_p = n_c + 1) = sum_{i=0}^{INT((n-1)/2)} [ n! / ( (i+1)! i! (n - 2i - 1)! ) ] p_p^{i+1} p_c^i p_a^{n-2i-1}.
Symbols: mu = expected fraction of pro-union workers; G = CDF of the net cost of voting C_i; b = benefit (b_p = -b_c = b); N = number of eligible voters; n_p, n_c, n_a = pro, anti, non-votes; dW+ (Delta W+) = probability a tie arises without the pro-union worker's vote; dW- = probability the union would win by exactly one vote without the anti-union worker's vote. Tie rule: unions lose ties (footnote 5), so a pro-union vote is pivotal at a tie and an anti-union vote is pivotal when the union leads by one. Printed typo: Eq. (11) as shown has sums to N and the upper limit Min[n_p - 1, N - n_p].

**Gelman, King & Boscardin (JASA, March 1998)** (https://sites.stat.columbia.edu/gelman/research/published/decisive2.pdf; page image of journal p.3: work-F/gkb98p-3.png; p.6: work-F/gkb98p6-6.png). A checks the numbers; the forms:
- (1) Pr(your vote matters) = Pr(your vote is decisive in your state) x Pr(your state will be decisive | your vote is decisive in your state).
- (2) Pr(your vote is decisive in your state) = Pr(n_i v_i = .5 n_i) = Pr(v_i = .5) approx f_{v_i}(.5)/n_i   [n_i even]; for n_i odd: Pr(n_i v_i = .5(n_i - 1)) = Pr(v_i = .5 - .5/n_i) approx f_{v_i}(.5)/n_i, "assuming that n_i is reasonably large". n_i = number of voters in state i (excluding yourself); v_i = Democratic share of the two-party vote in state i (excluding your vote).
- (3) Pr(your state is decisive | your vote is decisive in your state) = Pr(E_{-i} in (.5 e_total - e_i, .5 e_total) | v_i = .5) + (1/2) Pr(E_{-i} = .5 e_total - e_i | v_i = .5) + (1/2) Pr(E_{-1} = .5 e_total | v_i = .5)   [the subscript "-1" in the last term is as printed]. E_{-i} = sum_{j != i} e_j V_j + 3 = Democratic electoral votes in the 49 other states plus DC; V_j = 1 if v_j > .5, 0 otherwise; e_total = sum_i e_i = 538.
- Sec. 5: probability that a single vote is decisive approx (sqrt(2 pi) tau n)^-1 exp( -(mu - .5)^2 / (2 tau^2) ) for a normal forecast with mean mu and sd tau "as discussed by Margolis (1977)"; with tau = 2% this "yields 20/n as an upper bound"; n = 200,000 gives "1 in 10,000".
- Sec. 5: probability a vote swings the national election approx 1/2 (2/11) (e_i/50); combined .008 e_i/n_i (A's figures).

**Gelman, Katz & Bafumi (Br. J. Pol. Sci. 34 (2004) 657-674)** (page images work-F/gkb04p-06.png, work-F/gkb04p-07.png = journal pp.662-663):
- individual voting power = Pr(jurisdiction j's e_j electoral votes are decisive) x Pr(a given vote is decisive in jurisdiction j | jurisdiction j's e_j electoral votes are decisive)   [Sec. 2.2]
- (1) Pr(jurisdiction j's e_j electoral votes are decisive) = Pr(E_{-j} in (0.5E - e_j, 0.5E)) + (1/2) Pr(E_{-j} = 0.5E - e_j) + (1/2) Pr(E_{-j} = 0.5E)
- (2) Pr(a given vote is decisive in jurisdiction j) = p_{v_j}(0.5)/n_j, p_{v_j} the continuous density of party A's vote share in j (assuming n_j > 100, say).
- Sec. 2.2.2: under random voting p_{v_j}(0.5)/n_j = sqrt(2/pi) x 1/sqrt(n_j); "What matters for comparing voters is not the constant factor sqrt(2/pi) but the proportionality with 1/sqrt(n_j)". (NOT 2/sqrt(pi).)
- Sec. 2.2.3: voting power approx proportional to e_j / sqrt(n_j); with e_j proportional to n_j, power proportional to sqrt(n_j).
- Sec. 2.3 example: [1/(sqrt(2 pi)(0.03))] exp(-0.5 (0.05/0.03)^2) / n_j = 1.84/n_j (as printed; arithmetic does not reproduce it: 3.32/n_j with the printed inputs, see F-41).

**Gelman, Katz & Tuerlinckx (Caltech SSWP 1141, October 2002)** (PDF https://authors.library.caltech.edu/records/hpnm8-cmw66/files/sswp1141.pdf?download=1; page image of printed p.7: work-F/gkt-08.png):
- (1) power_i = Power of voter i = Pr(R = +1 | v_i = +1) - Pr(R = +1 | v_i = -1), v_i = +/-1, R = R(v) = +/-1 the aggregation rule.
- (3) power_i = Pr(R = +1 | v_i = +1) + Pr(R = -1 | v_i = -1) - 1 = 2 Pr(satisfied) - 1 (if Pr(v_i = +1) = 1/2) (text layer).
- (4) Pr(tie election) approx f_V(0)/n, f_V the density of the difference V in vote proportions between the two leading candidates (text layer).
- (5) weighted voting: power_i = Pr(|V_{-i}| < w_i) + (1/2) Pr(|V_{-i}| = w_i).
- Linear approximation (Sec. 3.1): power_i approx sqrt(2/pi) w_i / W, "relative error of less than 10% for all states" (page image).
- Sec. 3.2 (page image): Pr(V_{-i} = 0) + (1/2) Pr(|V_{-i}| = 1) = C(n_j - 1, (n_j - 1)/2) if n_j is odd, C(n_j - 1, n_j/2) if n_j is even, "under the random voting model" (printed without the factor 2^-(n_j - 1)); "Unless n is very small, this can be approximated as sqrt(2/(pi n_j)), which is a special case of (4)".
- (6) two-stage random voting: power_i approx w_j / sqrt(n_j).
- (10) Pr(a vote is decisive within district j) approx f_j(0)/n_j; (11) approx 1/(n_j sd(V_j)) if f_j has mean 0 and fixed form (text layer).
- (12) V_i^sim = V_i^obs + eps^nation + eps_k^region + eps_j^state + eps_i^district (text layer), SDs 0.06, 0.02, 0.04, 0.09 for the 2000 election.

**Princeton Election Consortium, October 2, 2022**: voterpower for a state = tpdf(|statemargin - MetaMargin| / sigma, tail) / voterpop (text, work-F/pec2221.txt), sigma = 4, tail = 1.

**Mulligan & Hunter**: no formula transcribed (definitions in words; FILL F-3).


## Everything still unread, and why

*Each reader's list, verbatim. The digest names the ones that matter for the model.*

### Reader A
1. Myerson (1998), IJGT 27(3): 375-392, full text: Springer restricted (RePEc: "Access to the full text of the articles in this series is restricted"; the Springer host belongs to task B); the author's page home.uchicago.edu fails TLS verification through the sandbox proxy ("unable to get local issuer certificate", curl exit 60; the proxy CONNECT succeeded); not bypassed. Northwestern DP copy (kellogg.northwestern.edu): HTTP 500 for DP 1189 on one request; stopped at that host.
2. Myerson (2000), JET 94(1): 7-45, full text: ScienceDirect HTTP 403 with a captcha page ("Are you a robot"); not circumvented. Read only second-hand through Bouton (F-2b).
3. Myerson & Weber (1993), APSR 87(1): 102-114: cambridge.org / jstor.org are other tasks' hosts; record and abstract only (RePEc).
4. Cox (1994), APSR 88(3): 608-621: full text at cambridge.org/jstor (other tasks' hosts); abstract read (RePEc). Cox (1997), Making Votes Count ch. 7: a book; not searched beyond the title.
5. Chamberlain & Rothschild (1981), JET 25(1): 152-162: ScienceDirect (captcha seen for the sibling article); two core.ac.uk search hits not read (core.ac.uk is another task's host).
6. Good & Mayer (1975), Behavioral Science 20: 25-33: not searched beyond the citation; Wiley/paywalled.
7. Myatt (2007), RES 74(1): 255-281 journal text: OUP/Wiley restricted; the DP 186 working paper (March 2004) was read in its place and is a different version.
8. Hoffman (1982), McKelvey & Ordeshook (1972), Palfrey (1989), Demichelis & Dhillon (2010), Margolis (1977, 1983), Beck (1975), Mulligan & Hunter (2003): named by the sources I read as places where pivot probabilities are derived; none read (no search made).
9. Myatt & Fisher Appendix A page image (Lemma 1 proof, printed p. 29) was read in the text layer only; I did not render the page (the Lemma 1 correction in A-06 rests on my exact calculation, not on the Appendix image).

###### NEED-FETCH (URLs for hosts that are not mine, or that I could not reach legitimately; not fetched)
- Chamberlain & Rothschild (1981): candidates from a search listing, unverified: `https://core.ac.uk/download/300456632.pdf`, `https://core.ac.uk/download/300459322.pdf` (core.ac.uk: another task's host); publisher: `http://www.sciencedirect.com/science/article/pii/0022-0531(81)90022-3` (from the RePEc record; bot check expected).
- Myerson (2000) JET: `http://www.sciencedirect.com/science/article/pii/S0022-0531(98)92453-X` (RePEc record; bot check seen at sciencedirect); the 1997 working paper "Large Poisson Games", Northwestern CMS-EMS DP 1189: `http://www.kellogg.northwestern.edu/research/math/papers/1189.pdf` (HTTP 500 on one request); Myerson's page `https://home.uchicago.edu/rmyerson/` (TLS verification fails through the proxy; the paper PDFs' file names are not known to me).
- Myerson (1998) IJGT: `http://link.springer.de/link/service/journals/00182/papers/8027003/80270375.pdf` (RePEc download link; link.springer.* is task B's host; restricted); Northwestern DP 1102R: `http://www.kellogg.northwestern.edu/research/math/papers/1102.pdf` (not requested; same host as the 500).
- Cox (1994) and Myerson & Weber (1993): `https://www.cambridge.org/core/product/identifier/S0003055400093680/type/journal_article` (the search listing's Cambridge link for Cox 1994 (identifier from the listing; not verified by me)); cambridge.org is another task's host.
- Mulligan & Hunter (2003) NBER WP 8590: `https://www.nber.org/papers/w8590` (a URL pattern, not verified; nber.org is task F's host).
- Gelman, Silver & Edlin (2012) "What is the probability your vote will make a difference?" (task F's F-4 says list under NEED-FETCH, A's host): I did not search for or fetch it; it is not in the first-pass lines I own.

---


### Reader B

- **McCune & Graham-Squire (Scottish STV), paper body** (counts by type, "30 single-winner, 1,049 multiwinner", "lower bound", the introduction's "1-4%"): Springer "Client Challenge" (also for the PDF link); not circumvented. Only the Crossref abstract was read. Preprint arXiv 2305.17741 is a different, legitimate copy: NEED-FETCH.
- **Fox & Bruyns (2026)** body, including the quote "a multiwinner version of IRV": same Springer challenge. The DOI is a paper on Borda-count variations (see B-36), not STV. Preprint arXiv 2501.00618: NEED-FETCH.
- **Bouton, AER 2013 text**: behind the AEA paywall; no open copy found. Only the Penn draft was read.
- **AEC v Johnston, final disposition (election void; new election 5 April 2014)**: not on the hcourt pages I could reach; hcourt.gov.au refused curl (empty replies / HTTP/2 INTERNAL_ERROR), all hcourt facts via WebFetch (a small model's extract).
- **Electorate size of WA (enrolled electors)**: not in the judgment per the extract; AEC pages NEED-FETCH.
- **info.gouv.fr 2022 results page** (Interior Ministry): Cloudflare "Just a moment..." (403), not circumvented. The Conseil constitutionnel's proclamations were read instead.
- **ACE pages**: curl returned 404/503 site-error pages for every ACE path; the two ACE pages above are via WebFetch only.
- **Electoral Commission (UK) Scotland page**: 403 "Just a moment..." Cloudflare check; not circumvented.
- **ssoar.info (Quinlan record)**: Anubis bot check; not circumvented; I do not know what the record contains.
- **icms.org.uk** (Graham-Squire slides): the proxy refused the CONNECT (502); not retried.
- **conseil-constitutionnel.fr/maire-info/lcp**: read (no problem).


### Reader C

- **New Zealand rules (C-09):** www.electionresults.govt.nz/sainte_lague.html: Cloudflare 403 (twice: the orchestrator's download and mine), archive.electionresults.govt.nz (one request): 403 same block page; elections.nz: Incapsula stub (one request); legislation.govt.nz Electoral Act 1993 whole-act URL: HTTP 202 with empty body (two requests, 6 s apart). Not circumvented; stopped on each host. Unread: the "120 highest numbers (quotients)", "successive odd numbers starting with 1", "size of the Parliament is increased by that number of seats", "121 seats in 2014" statements. Only the 5%-or-one-seat rule and "overhang is also possible in New Zealand" were read, from the IDEA Handbook 2005 (C-10).
- **Task item 5 (C-41):** no BVerfG, Bundeswahlleiterin or Bundestag source found that states whether negative voting weight can occur under the 2023 law; the 2023 bill and the 2024 judgment were searched and do not say.
- **Modified Sainte-Laguë formula (F-1):** not in the IDEA Handbook.
- **Droop quota from an electoral authority (F-2):** not read; IDEA is not an electoral authority.
- **F-3:** no published estimate found on allowed hosts; leads (Kotakorpi et al.; Mulligan & Hunter; the lab experiment) unread.
- **F-4:** no source stating or proving vote-monotonicity of divisor methods on allowed hosts; leads are on arxiv.org and wikipedia (not read).
- **L&T footnote 1's sources (C-32):** Mulligan & Hunter (2003) and Gelman et al. (1998) were not read at source here (other readers cover Gelman et al.).
- **First pass's own computations, lines 124-135 (C-43, C-44):** not source facts; not re-run.
- **IDEA online pages (idea.int/answer/...):** not read (F-1).


### Reader D

- Aguiar-Conraria, Magalhaes & Vanberg full text (either version): core.ac.uk (Cloudflare), uminho hosts (refused/reset/timeout), rcaap.pt (reset), Heidelberg archive (Anubis). Consequently unread: the Sec. 2 quotes (D-07, D-08), the turnout figures 53.8/39.9/47.0 and CIs (D-13), the "40" versus "57 to 70" boycott statements (D-14), Tables 1 and 4.
- Hizen & Shinmyo (2011): abstract (not on IDEAS), full text (subscribers only).
- Electoral Commission and House of Commons Library pages for the 2016 referendum: Cloudflare 403 (D-25). Rejected-ballot count unread.
- Italian Constitution at senato.it: AWS WAF challenge (the Constitutional Court's English text was read instead, D-03). `elezionistorico.interno.gov.it`: 403 Access Denied.
- Herrera & Mattozzi, JEEA 2010 version (the first pass and I read the May 2006 working paper).
- Maniquet & Morelli (2015) full text; Mulligan & Hunter (2003) full text; Gelman, King & Boscardin via core.ac.uk (the Columbia copy was read instead).
- Outcome of the 22-23 March 2026 Italian constitutional referendum (not needed).


### Reader E

- Baltz, journal version (Political Analysis 33(4):447-455, doi 10.1017/pan.2024.32): volume, pages, DOI, journal abstract, main-text equation numbers, main-text example. Reason: cambridge.org is held by the orchestrating thread; I had only the arXiv v2 text and the supplement (E-15, E-19, F-2).
- Mebane, Baltz & Vasselai (2019), the SMDP derivation Baltz extends: a conference presentation; no URL found; the SMDP formula behind Figure 1 is therefore unseen.
- Eggers & Nowacki (2024), Journal of Politics 86(2): not an allowed host (journals.uchicago.edu), probably a paywall. NEED-FETCH: https://www.journals.uchicago.edu/doi/10.1086/726943 (URL from a web search, not opened).
- Bouton (2013); Lepelley, Chantreuil & Berg (1996); Miller (2012, 2017); Norman (2006, 2012); Atsusaka et al. (2024); Magrino et al. (2011); Blom et al. (2016): not read (other tasks or not searched).
- McCune & Graham-Squire, Scottish STV (the "62 of 1,079", "30 single-winner, 1,049 multiwinner", "1-4%" figures): task B.
- Ornstein & Norman's simulation code ("available from the authors on request") and Figures 1-5 data: not obtained; I read only the text and tables.
- The Allard area formulas (images in the HTML) and the ERS/MORI poll data.
- Image of O&N p. 5 (utility equation 6) not looked at; the sign/direction there is from the text extract.
- Warren D. Smith's other pages (e.g. the "IrvParadoxProbabilities" page the Monotone page points to): not requested.


### Reader F

- FiveThirtyEight article text by curl: https://fivethirtyeight.com/features/house-tipping-point-districts/ answers 301 to https://abcnews.com/politics (checked: curl -I at 2026-11-07), so the saved fte.html (txt/fte.html, 1.9 MB) is the ABC News politics front page, not the article (its canonical link is https://abcnews.com/politics, its title is not the article's; it contains no "tipping-point" text). The four facts (218th seat sentence, Oct. 14, 40,000 simulations, 70-in-100) rest on one WebFetch extract (F-04 to F-06).
- Wayback copy of the article: https://web.archive.org/web/20250911233850/https://fivethirtyeight.com/features/house-tipping-point-districts/ (snapshot listed by https://archive.org/wayback/available): curl reset the connection twice (proxy log: tunnel closed mid-exchange), WebFetch said "SITE_BLOCKED". Not circumvented.
- 538 CSVs (house_district_toplines_2022.csv, "tipping" and "vpi" columns): see F-07. Values unread.
- 538 methodology page (how-fivethirtyeights-house-and-senate-models-work): WebFetch only, no match for tipping point / VPI; may be incomplete (FILL F-1).
- Public Choice text of Mulligan & Hunter (2003): Springer (paywalled; EconPapers says access restricted to subscribers); SSRN (Cloudflare 403 challenge). Only the abstract (EconPapers) and the NBER working paper were read.
- VoteHub "Voter Power Index" (Sept. 10, 2026): Cloudflare 403 challenge; lead only.
- CESifo working paper 7786: bot-check page returned instead of the PDF; content unknown.
- GKT 2002 volume and issue ("Statistical Science 17(4)") and the journal text: not on the sources read (F-20). Page range 420-435 and DOI 10.1214/ss/1049993201 are on the Caltech page.
- Datawrapper chart data (Ballotpedia overview chart https://datawrapper.dwcdn.net/xYKPX/5/ and map https://datawrapper.dwcdn.net/FIOBI/5/): host not named for task F; the list table on the page is the full data, so not needed.
- Ballotpedia definition of "coverage scope": no page found or looked for beyond the page itself (F-51).
- Sources not in my assignment and not read: Gelman, Silver & Edlin (2012), Economic Inquiry (A's host, FILL F-4); the "1.84/n_j" arithmetic in GKB 2004 (cannot be reproduced; no explanation found).
- Charts: the Princeton Election Consortium page's charts (relative voter power by state) are images, not read.


## Follow-up fetches (URLs the readers could not take legitimately; none was fetched by them)

*Items on `cambridge.org` that were the orchestrating worker's were fetched (Luechinger et al.; the quorum docx; the Baltz and Aguiar-Conraria pages). Those that remain below are from the readers' lists; each may sit behind a bot check or paywall, which is not to be circumvented.*

### Reader A
- Chamberlain & Rothschild (1981): candidates from a search listing, unverified: `https://core.ac.uk/download/300456632.pdf`, `https://core.ac.uk/download/300459322.pdf` (core.ac.uk: another task's host); publisher: `http://www.sciencedirect.com/science/article/pii/0022-0531(81)90022-3` (from the RePEc record; bot check expected).
- Myerson (2000) JET: `http://www.sciencedirect.com/science/article/pii/S0022-0531(98)92453-X` (RePEc record; bot check seen at sciencedirect); the 1997 working paper "Large Poisson Games", Northwestern CMS-EMS DP 1189: `http://www.kellogg.northwestern.edu/research/math/papers/1189.pdf` (HTTP 500 on one request); Myerson's page `https://home.uchicago.edu/rmyerson/` (TLS verification fails through the proxy; the paper PDFs' file names are not known to me).
- Myerson (1998) IJGT: `http://link.springer.de/link/service/journals/00182/papers/8027003/80270375.pdf` (RePEc download link; link.springer.* is task B's host; restricted); Northwestern DP 1102R: `http://www.kellogg.northwestern.edu/research/math/papers/1102.pdf` (not requested; same host as the 500).
- Cox (1994) and Myerson & Weber (1993): `https://www.cambridge.org/core/product/identifier/S0003055400093680/type/journal_article` (the search listing's Cambridge link for Cox 1994 (identifier from the listing; not verified by me)); cambridge.org is another task's host.
- Mulligan & Hunter (2003) NBER WP 8590: `https://www.nber.org/papers/w8590` (a URL pattern, not verified; nber.org is task F's host).
- Gelman, Silver & Edlin (2012) "What is the probability your vote will make a difference?" (task F's F-4 says list under NEED-FETCH, A's host): I did not search for or fetch it; it is not in the first-pass lines I own.

---

### Reader D
1. Cambridge Core page of the Experimental Economics article (held by the orchestrating thread): https://www.cambridge.org/core/journals/experimental-economics/article/experimental-evidence-that-quorum-rules-discourage-turnout-and-promote-election-boycotts/CC55C56A35BFBA78389B0747C1B54D53 (from a search result; its PDF would give Sec. 2, Sec. 4.1, Sec. 4.3, Sec. 5, Tables 1 and 4). The `core-reader` link in the same search result: https://www.cambridge.org/core/product/CC55C56A35BFBA78389B0747C1B54D53/core-reader.
2. NIPE WP 14/2013 PDF at the host IDEAS gives: http://www3.eeg.uminho.pt/economia/nipe/docs/2013/NIPE_WP_14_2013.pdf (the sandbox cannot reach any uminho.pt host).
3. Heidelberg working paper 0671 (a different paper by the same authors, pivotal-voter model with participation, approval and rejection quorums): https://archiv.ub.uni-heidelberg.de/volltextserver/27268/5/Aguiar_2019.pdf (Anubis).
4. Electoral Commission: https://www.electoralcommission.org.uk/research-reports-and-data/our-reports-and-data-past-elections-and-referendums/results-and-turnout-eu-referendum and the report PDF https://www.electoralcommission.org.uk/sites/default/files/pdf_file/2016-EU-referendum-report.pdf (both from search results; Cloudflare). House of Commons Library CBP-7639: https://commonslibrary.parliament.uk/research-briefings/cbp-7639/.
5. Italian Constitution Art. 75 at the Senate: https://www.senato.it/documenti/repository/istituzione/costituzione_inglese.pdf (WAF challenge).
6. Hizen & Shinmyo (2011) abstract: publisher page via the DOI 10.1007/s11127-010-9670-1 (Springer: bot-challenged for other tasks). A working-paper version may exist as Kochi University of Technology SDES-2015-6 (https://www.souken.kochi-tech.ac.jp/seido/wp/SDES-2015-6.pdf; from a search result; IDEAS lists "SDES-2015-6" under Hizen's papers, but I did not check that it is this paper).
7. Maniquet & Morelli open versions: https://research.dial.uclouvain.be/bitstreams/d37e9eed-ab08-4a9f-9882-9fd2854180f1/download and the EUI working paper (https://cadmus.eui.eu/handle/1814/13664) (search results; not opened).
8. Ballotpedia: https://ballotpedia.org/Primary_election_competitiveness_in_state_government,_2025 (task F's host).
9. Aguiar-Conraria & Magalhaes (2010), "How quorum rules distort referendum outcomes: Evidence from a pivotal voter model", European Journal of Political Economy 26(4) 541-557 (doi:10.1016/j.ejpoleco.2010.03.004 per Hizen's reference list; NIPE WP 17/2009 per IDEAS): the "rigorous derivation" the docx points to; and "Referendum design, quorum rules and turnout", Public Choice 144(1) 63-81 (NIPE WP 05/2008). Not searched for open copies.

---

### Reader F
1. Gelman, Silver & Edlin (2012), "What is the probability your vote will make a difference?", Economic Inquiry: on sites.stat.columbia.edu (task A's host); I did not look the URL up.
2. 538 article and its data: the ABC News republication of "The 10 Districts Most Likely To Decide Control Of The House" (URL not found by search; fivethirtyeight.com redirects to abcnews.com/politics); the Wayback snapshot above; the model-output CSVs (github.com/fivethirtyeight/data returned 403 "GitHub access to this repository is not enabled for this session" - enabling it needs the add_repo tool, which is not mine to use).
3. Mulligan & Hunter (2003) full text and the explanation of 89,000 versus 100,000 (Springer / SSRN / the author's page).
4. Statistical Science 17(4) 2002 page for GKT (projecteuclid.org or the DOI 10.1214/ss/1049993201).
5. VoteHub's Voter Power Index (2026) and Princeton Election Consortium Part 2/3 of "Democracy Moneyball, 2022" (House), for F-1.
6. Coate, Conlin & Moro (Journal of Public Economics 92 (2008) 582-596, the published version): for whether a numerical pivot probability is printed.
7. Ballotpedia: a methodological page defining "coverage scope" and the "decided by 10 votes or fewer" list.
