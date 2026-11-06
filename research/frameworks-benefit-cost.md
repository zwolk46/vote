# Frameworks for "does one vote matter": the benefit term and the cost term

*Researcher: Sonnet 5.5 subagent, 2026-11-06. Brief: map the frameworks, the benefit term B and the cost term C, so that nothing is assumed or foreclosed. Nothing here chooses a model for the site; that is the orchestrator's.*

**Read section 0 first.** It says how every fact below was obtained, and that no source was read as a whole page.

---

## 0. How this was read, and what that means for every fact

1. **curl was refused for every academic host, by the sandbox's network policy.** `curl -sSL` to plato.stanford.edu, sites.stat.columbia.edu, arxiv.org, en.wikipedia.org, archive.org, www.jstor.org, papers.ssrn.com, core.ac.uk, electionlab.mit.edu, ideas.repec.org, api.crossref.org and api.openalex.org each ended in `curl: (56) CONNECT tunnel failed, response 403` (my own requests, one per host). The proxy's status log also showed 403s on CONNECT to www.nber.org and link.springer.com from other sessions' requests; I did not request those two myself, and took the log as enough. The proxy status endpoint names the cause: `gateway answered 403 to CONNECT (policy denial or upstream failure)`. This is the environment's egress allowlist, not the sites refusing a client. I did not retry and did not route around it. Only github.com and raw.githubusercontent.com answered, and they hold none of these sources. (`read_documentation environment.network` says the person can widen "Allowed domains" in the project's cloud-environment settings; the hosts that mattered are the ones listed above.)
2. **WebFetch was therefore used for every source below, which the brief allows when curl is refused.** WebFetch returns a small model's reading of the page, not the page. Consequences, which apply to every line of this report:
   - Every fact is **[S] stated, via a WebFetch extract**. None is a whole-page read, so the brief's "decide a fact at its source, whole" has **not** been met for any of them. Wave 2's fresh-reader check should re-read each at the URL given, in a session that can reach the host.
   - The extractor would not reproduce long passages, so "exact quotes" are short fragments (under about 25 words) **as the extractor returned them**. I could not check them against the page. Where an extractor corrected my own assumption about a source, I followed the extractor and say so.
   - Page numbers are the extractor's. Several were flagged by it as approximate.
   - Where the extractor said the text was paywalled or garbled, I say so and give no formula.
3. **Tags.** [S] = stated in one extract (URL given). [S2] = two independent extracts agree. [M] = I computed it (script `/tmp/claude-0/research-c/calc/arith.py`, inputs from the named sources; output shown). [I] = my inference across sources, not stated by any of them.
4. **WebSearch** was used to find URLs only. Result lists included mirrors and proxies (a Chinese university web-VPN copy of a Sage article, `remotevs.com` copies of Gelman's site, a Hungarian "virtual library" PDF of the Downs book, `adambrown.info` notes); I used none of those. A few facts rest on a search-result **title** alone (marked "title only").
5. **One bot challenge, not circumvented.** `https://is.muni.cz/el/fss/podzim2023/POLn6001/um/DOWNS_-_Economic_Theory_of_Political_Action.txt` returned, per the extractor, an empty page whose script runs a SHA-256 loop and reloads (a proof-of-work check). I stopped at the first refusal and made no further request to that host. Downs's own text is therefore unread.
6. **URLs built from memory, disclosed.** WebFetch prefers URLs that came from a search. Most of mine did. These did not: an AEA address for Feddersen 2004 (it returned a different article, Fama and French; I discarded it and put Feddersen 2004 in the unread list), and, because they follow the host's standard pattern, `https://docs.iza.org/dp5854.pdf`, `https://www.bls.gov/news.release/empsit.nr0.htm`, `https://en.wikipedia.org/wiki/Paradox_of_voting` and `https://en.wikipedia.org/wiki/Cost_of_Voting_Index`. Each of the last four returned the intended document (the extractor named it from the page's own header), but a fresh reader should re-check them first.
7. **No emails, purchases or messages were used or sent.** No git commands were run. Only this file was written in the repository.

---

## 1. The calculus of voting and its paradox

### 1.1 The formulas, as each source writes them

| Source | Formula as written | Terms as defined | URL, location |
|---|---|---|---|
| Stanford Encyclopedia of Philosophy, "The Ethics and Rationality of Voting", sec. 1.1 | `U_v = p[V(D) − V(R)] − C` | p "the probability that Sally's vote is decisive"; V(D) − V(R) "the difference in the expected value of the two candidates"; C "the opportunity cost of voting" | https://plato.stanford.edu/entries/voting/ [S] |
| Geys (2006), "'Rational' theories of voter turnout: a review", *Political Studies Review* 4: 16-35 | eq. (1) `R = PB − C > 0`; eq. (2) `R = PB − C + D` | R "represents the net expected utility of voting"; P "the probability (P) that one's vote influences the outcome"; B "stands for the difference in expected utilities from the policies of the two candidates"; C "refers to the costs of voting"; D "stands for the benefit from expressing oneself" (p. 19) | https://www.uh.edu/hobby/eitm/_docs/past-lectures/2014-Lectures/Jeremy-Gilmore/Rational-Theories-of-Voter-Turnout.pdf [S]. This is a university lecture-materials copy; the extractor identified it as Geys's article from its own header. Page numbers are the journal's, per the extractor. |
| Sanders (1980), "On the costs, utilities and simple joys of voting", *J. of Politics* 42(3): 854-863 | Downsian form, then Riker & Ordeshook's "R = PB + D − C will usually be positive" (p. 855) | B "the perceived differential in benefits offered the voter by the two parties"; P "the probability that his vote will bring about the favored party's victory"; C "the costs incurred in the voting decision"; D added by Riker & Ordeshook, "'D' (for 'citizen duty')" | https://newschoolhistories.org/wp-content/uploads/2018/04/sanders_onvoting.pdf [S] (a copy hosted on a third-party site) |
| Edlin, Gelman & Kaplan (2007), *Rationality and Society* 19(3): 293-314, eq. 1 | `ΔU = pB − c` | ΔU "relative utility of voting"; p probability a single vote is decisive; B "relative benefit of the voter's preferred candidate winning"; c net cost, defined as "the costs, minus the direct benefit of voting" (p. 4) | https://www.nber.org/papers/w13562.pdf [S]; journal citation from https://www.nber.org/papers/w13562 [S] |
| Dowding (2005), "Is it rational to vote? Five types of answer and a suggestion", *BJPIR* 7: 442-459 | `pB > C` (p. 442); `pB + D > C` (p. 443); `pB − C > 0` (p. 445) | p "the probability of someone's vote being decisive"; B "the benefit gained through the voter's favoured party winning"; C "the cost of voting"; D "can cover all sorts of private motivations" and is "an 'expressive benefit'" | https://core.ac.uk/download/156636542.pdf [S] |
| arXiv 2510.24344 (2025 review of behavioural approaches to turnout), sec. 3.1 | `ΔU = PB − C`; D added "as a civic duty" | P "the probability that a vote can be decisive"; B "the gain of the individual candidate's victory"; C "the net cost incurred by the individual in the voting process" | https://arxiv.org/pdf/2510.24344 [S] (secondary) |
| Salka (2017), conference paper, WPSA | Downs: `u(V) = (PB) − C`; Riker & Ordeshook revised: `u(V) = (PB) − C + D` | B = "the party differential" (credited to Downs 1957); PB = what "Downs called the vote value"; D "the private, consumptive reward an individual receives from voting that is independent of that individual's contribution to the outcome" (citing Riker & Ordeshook 1973, 63) | https://www.wpsanet.org/papers/docs/WPSA%20-%20Salka%202017.pdf [S] (weak: a conference paper, itself secondary) |
| **Riker & Ordeshook (1968)**, *APSR* 62(1): 25-42 | **Not read.** Cambridge shows abstract and footnote fragments only; the full text is paywalled. | Footnote fragments the extractor saw: a favourable outcome is "worth B utiles"; C and V appear as cost and value; "constancy of D" and a "sense of citizen duty scale" (the extractor flagged "D is citizen duty" as its inference). | https://www.cambridge.org/core/journals/american-political-science-review/article/abs/theory-of-the-calculus-of-voting/F32A6F556750C8207E920CE9D0850A2E [S: abstract only] |
| **Downs (1957)**, *An Economic Theory of Democracy* | **Not read** (book; one open text attempt hit a bot challenge, section 0). Known only through Geys (p. 17), Dowding, Sanders, Salka. | Downs's own terms: "vote value", "party differential" (via Salka); "the vote value, which is nearly infinitesimal under most circumstances" (via Dowding) | see rows above |
| **Ferejohn & Fiorina (1974)**, *APSR* 68(2): 525-536 | **Formula not read.** Abstract and some footnotes only. | see 1.3 | https://www.cambridge.org/core/services/aop-cambridge-core/content/view/0F89DD7019DEC0A1D8B0F4F33CB69CBE/S0003055400117368a.pdf/ [S: abstract] |

**Two things the table shows.**

- [S2, in fact S4] The structure **probability of decisiveness × benefit differential − cost** is written by SEP, Geys, Edlin et al. and Dowding, and the D term is **added after** it and is **not multiplied by p**. That is the owner's p × B against C.
- **Sources disagree on what D is.** "Citizen duty" (Sanders; the arXiv review), "benefit from expressing oneself" (Geys), "expressive benefit" (Dowding), "private, consumptive reward... independent of the contribution to the outcome" (Salka). Geys adds that D "can be tautological unless its sources are specified" (extractor's paraphrase, p. 19). The brief's `R = PB − C + D` is Geys's eq. (2); I could not confirm it as Riker & Ordeshook wrote it in 1968, and Sanders writes the order `PB + D − C`. Whether D is a duty, an expression, or a consumption benefit decides how the owner's "civic duty" objection is classified (see 3.6).

### 1.2 The paradox, as the sources state it

- Riker & Ordeshook abstract: "voting is an irrational act in that it usually costs more to vote than one can expect to get in return"; and "we present empirical evidence that citizens actually behave as if they employed this calculus." The abstract goes on to say the reinterpreted calculus makes voting reasonable for those who vote and abstaining reasonable for those who abstain (extractor's paraphrase). [S] Cambridge page above.
- Downs, via Dowding: "the party which eventually wins will probably be elected no matter how he casts his ballot" and "the vote value, which is nearly infinitesimal under most circumstances." [S] (Downs's own text unread.)
- SEP sec. 1: voting "has opportunity costs", for most people "voting does not maximize expected utility, which gives rise to the 'paradox of voting' (Downs 1957)" (extractor's paraphrase). [S] Barnett calls the standard binomial argument Brennan's example, which "led us astray" (3.1).
- Geys on the instrumental model: "it appears highly implausible that the level of real turnout rates can be explained on instrumental grounds" (p. 18); but it fits **differences** in turnout better than levels. [S]
- **A ready map of the escapes.** Dowding sorts the replies into five types, in his words: "the marginalist solution" ("rational choice is good at predicting at the margin"); "the C-term solution" ("people simply do not factor them into their decisions to vote"); "the B-term solution" ("By making the B term massive"); "the p-term solutions" ("the p term is defective and needs to be replaced"); "D-term solutions" ("the work in utility terms is done by 'D'") (p. 443). [S] URL as above. [I] The owner's claim fixes p as measured and C as real, so the replies that remain open to a critic are exactly B (counts others), D (non-outcome benefits), and a different decision rule or a different p; section 3 is organised around that.

### 1.3 Ferejohn & Fiorina (minimax regret), and Aldrich

- F&F abstract: minimax regret "specifies voting under quite general conditions", for two- and three-candidate plurality elections; a minimax-regret voter "never votes for their second choice in a three-candidate election", while expected-utility maximisers sometimes do. [S]
- Footnote fragment (extractor): the authors assume the cost is below half the utility gap between one's preferred candidate winning and losing ("c < ½"); without it "abstaining would dominate voting". The regret tables and the exact voting condition were **not visible**. [S]
- Geys describes the rule in words only, no formula: "The rule here is to choose the action that yields a minimal regret in a worst-case scenario" (p. 21); "the decision to vote is not made under risk, but under uncertainty" (p. 21); the extractor's paraphrase is that it predicts higher turnout than expected utility but several of its other predictions fit the stylised facts poorly (Geys's own words there: "several other predictions are (much) less satisfactory", p. 21). [S]
- Dowding's objection: "elections are not that uncertain" and it "cannot explain higher turnout in close elections" (p. 449). [S]
- **Aldrich (1993)**, "Rational choice and turnout", *AJPS* 37(1): 246-278. Abstract read (an extract of a library catalogue record; the page did not name the author, citation from the extractor): the paper "compares the calculus of voting and minimax regret models" and argues turnout is not an especially problematic collective-action problem because for many people it is "a low cost, low (expected) benefit decision." [S] https://opact.sdu.edu.tr/vufind/SummonRecord/FETCH-LOGICAL-c363t-c3fb87c8733304e3ad34740cc19e8f1eb9e39340c982f7d4367bd90485cc21743. Geys p. 18: "Downs (1957) and Aldrich (1993) argue that these costs are only minor." [S] Full text unread.
- [I] Minimax regret ignores p, so it does not measure the owner's "importance". It is a competing **decision rule**, not a competing definition of mattering.

---

## 2. What B is

### 2.1 Definitions the sources use

| Source | Definition of B | Who is counted |
|---|---|---|
| SEP | "the difference in the expected value of the two candidates" (V(D) − V(R)) | not stated in the extract |
| Geys | "the difference in expected utilities from the policies of the two candidates" | the voter |
| Sanders / Downs | "the perceived differential in benefits offered the voter by the two parties" ("party differential") | the voter |
| Edlin, Gelman & Kaplan | `B = B_self + αN·B_soc` (eq. 2, p. 5): B_self the individual's own benefit; B_soc the average benefit per person if the preferred candidate wins "as perceived by the voter"; N the affected population; α a discount on others' benefit. B_soc "is not an averaging of the actual utilities or preferences of the N persons" (p. 5). α = 0 is a selfish voter, α > 0 a social one. | the voter, **plus** others at weight α |
| Barnett (2020) | `B = b × N`, "the net social benefit of having Daisy rather than Donald in charge", b the average benefit per person; the voter is a consequentialist for whom "everyone's interests are given equal weight, including your own" (p. 425) | the whole public |
| Dowding | "the benefit gained through the voter's favoured party winning" | the voter (the B-term reply is "making the B term massive") |

[S] throughout; URLs in 1.1 and https://philosophersannual.org/40articles/barnett-why.pdf for Barnett.

**What is common:** every source defines B as a **difference between two outcomes, valued by the voter** (a perceived or expected value, not a measured one). They differ on **whose welfare is in the value** (section 3.7).

### 2.2 From B to the expected value of one vote: the tie algebra

The brief asks how the expected value is written as the change in the probability your side wins times the differential. Sources:

- Gelman, King & Boscardin (1998), p. 3: a vote is decisive only if "without your vote, your state's election outcome must be exactly tied or one vote away from a tie"; their eq. (3) carries a factor of ½ because "a vote that causes the national election to be tied is only half as decisive." [S] https://gking.harvard.edu/files/estimatprob.pdf
- Barnett, pp. 426-7: a decisive vote "breaks a tie" or "causes a tie"; ties are settled by coin flip, so the expected benefit of a decisive vote is half of B: `EB = ½ × B × d`. [S]
- Mulligan & Hunter (2003) count a "pivotal vote" as a vote for the winner in an election the winner won "by no more than one vote", or a vote for either candidate in a tied election (Sec. II.B, p. 5), **without** a ½ weight. [S] https://www.nber.org/papers/w8590.pdf

**[M]/[I] derivation (my algebra, checked by simulation in the script).** Let M be the margin among **others** (A's votes minus B's), and let ties be broken by a fair coin. Then:
- P(A wins | you vote A) − P(A wins | you abstain) = ½·[P(M = 0) + P(M = −1)].
- So the expected value of the vote is `½·[P(M=0) + P(M=−1)] × (U_A − U_B)`. This is p × B with **p ≡ ½·[P(tie among others) + P(A one behind)]** and **B ≡ U_A − U_B**, consistent with GKB's ½ and Barnett's ½. Script output: the difference equals ½(P0 + P₋₁) for three random distributions.
- The ½ is a **tie-rule choice**. If a tie is resolved by a recount, a court or a runoff, the weight changes; GKB's footnote 6 "addresses the recount objection but doesn't change the definition" (extractor, p. 2). The owner's open point on "a margin of one" is exactly this. [I]

### 2.3 The owner's wording of B versus the sources'

His words (brainstorm, 19:39): "the marginal difference between the outcome voted for and the outcome or the expected outcome." [I] Two readings, and they are different quantities:
- (a) **B = U(outcome you vote for) − U(the alternative outcome)**, the quantity the sources call B, which is the gain **if decisive**.
- (b) **E[U | you vote] − E[U | you abstain]**, which already contains the probability: it equals p × B from 2.2. "The expected outcome" without your vote is what the abstaining arm gives.
Both are in the literature; they differ by the factor p. Which he means decides whether "the magnitude" he wants to isolate is B or pB. The orchestrator holds the transcript; I flag it only.

### 2.4 More than two candidates

- **Pivot events are pairwise ties for first place.** Rivière (2003, Royal Holloway DP 2003-06, a geometric analysis of electoral systems), https://repository.royalholloway.ac.uk/items/60802168-c229-3784-da90-256e3b2f72a9/1/dpe0306.pdf [S]: with three candidates the "prospective rating" is `PR_i = p_ij[u_i − u_j] + p_ik[u_i − u_k]`; with four or more, `PR_i = Σ_j p_ij[u_i − u_j]`, where p_ij is the probability of a close race between i and j. The extractor noted a typo in the source's printed formula.
- Kselman, Niou & Wang (2020, *Electoral Studies* 68: 102220), https://dukespace.lib.duke.edu/server/api/core/bitstreams/672a2c09-26d4-4f6b-923a-7b2da6ccdd60/content [S]: voters are "pivotal in creating or breaking 1st-place ties" between two candidates; three-candidate condition (as extracted) `p23·(U2 − U3) > 2·p12·(U1 − U2) > p13·(U1 − U3)`; they find strategic voting "driven almost entirely by viability comparisons involving one's least-preferred candidate". The paper says extending to more candidates "will require careful proofs".
- F&F's abstract (1.3) and Goldman's footnote 25 (a scalar "force" treatment "doesn't work with three or more candidates", extractor) also treat the multi-candidate case as different.
- [I] So with three or more candidates B is not one number: each pivot pair has its own utility gap and its own probability. A sum of pairwise terms is what the literature writes. Myerson & Weber (1993) and Palfrey & Rosenthal (1983, 1985) are the standard sources for these and are **unread** (Palfrey & Rosenthal 1983 abstract only: "Presents a game-theoretic model of voter turnout"; https://authors.library.caltech.edu/65012/ [S]).

### 2.5 An office that decides control of a body (a seat in a chamber, an Electoral College)

- GKB's presidential structure is two-level: the chance your vote is decisive in your state times "a conditional probability" that your state is decisive nationally (eq. 1), with the state-level factor "roughly the density of the vote-share forecast at .5 divided by the number of voters" (eq. 2) (p. 3). [S]
- Gelman, Silver & Edlin (2008 manuscript): `P(state pivotal in the Electoral College) × P(state tied | pivotal)`; pivotality is the share of 10,000 simulations where the margin from all other states is less than the state's electoral votes, with half credit for exact ties; tie density from a Student-t with 4 d.f. (pp. 1, 3). [S] https://www.stat.berkeley.edu/~aldous/157/Papers/vote.pdf
- VoteHub "Voter Power Index" (page path dated 2026/09/10; the page shows no date): the index grades each federal race by "how much influence a single ballot cast in it has over the broader outcome in Congress"; it is "not a literal probability that a vote is decisive"; method in words: the seat's tie likelihood from daily forecast simulations, divided by expected turnout, combined with how often the seat is the one that decides the chamber ("the rest of the chamber sits exactly one seat from a majority"); a district's number is "the state's Senate score plus the seat's House score." Headline: Texas has the highest Senate tipping-point probability, 19%. No per-ballot probability and no dollar B. [S] https://votehub.com/2026/09/10/votehubs-voter-power-index-finding-2026s-most-impactful-ballots/
- [I] **For a seat, B is not "who holds the seat"; it is the difference the seat makes to the body's outcome**, so B = (value of the difference in control, or in policy, when this seat flips) and p has the same two-level shape: P(tie in seat) × P(seat is the tipping point for the body). No source I read states B for a chamber seat as a dollar or utility quantity; VoteHub gives only the probability side.

---

## 3. Frameworks under which "your vote mattered" is evaluated

**The owner's setup** (brainstorm 19:32, [I] my reading): compare the world where your ballot is counted with the world where it is not, *"all other contexts"* the same, nobody persuaded, nobody knowing; the count is "exactly as it would had you not gone to the polls." Two features decide how each framework fits: (i) **others' behaviour is fixed across the two arms** (a counterfactual fixity), and (ii) **nothing but the counted ballot differs**. One reading detail bears on the cost term: his thought experiment has you *go to the polls and put the ballot in* in both arms, so the trip is common to both and the experiment isolates B; the real choice (go or not) is where C bites. Whether C is part of his isolated comparison is a question for him (section 6).

| # | Framework | Counts as "the vote mattered" | Fit with the owner's setup | Implication for E[benefit] vs cost |
|---|---|---|---|---|
| 3.1 | Pivotality / counterfactual (CDT, others fixed) | the vote creates or breaks a tie | exact | tiny p; for self-only B, pB ≪ C in large electorates |
| 3.2 | Causal contribution / overdetermination (Goldman, Tuck) | the vote is among the causes (members of an "efficacious set") even if not pivotal | different question | no expected-benefit number; a moral or participation reason |
| 3.3 | Triggering / threshold expected effect (Kagan, Parfit) | small chance of a big difference | same maths as 3.1 | tiny p is not discounted if the whole B is large |
| 3.4 | Evidential / correlated choice | your choice is evidence of what similar others do | excluded only if "fixed" is read causally | replaces p by a conditional probability over correlated voters |
| 3.5 | Rule / group consequentialism | the rule "vote" followed by like-minded people matters | contradicts fixity of others | group benefit can exceed group cost; individual pB unchanged |
| 3.6 | Expressive / consumption (D) | the act itself is the benefit | outside "importance" by definition | if D ≥ C voting pays regardless of p |
| 3.7 | Altruistic / social-welfare B | decisive vote × benefit to everyone affected | not excluded; changes B, not the counterfactual | pB roughly independent of electorate size |
| 3.8 | Minimax regret | worst-case regret of abstaining | ignores p | predicts voting under conditions; not a measure of importance |

### 3.1 Pivotality / counterfactual (causal decision theory with others' votes fixed)

- **What it says counts:** the vote matters iff the others' votes leave the outcome tied, or one short of a tie (2.2). The "evidence, causality" paper writes CDT as maximising `∑_W V(W)·P(A □→ W)` (counterfactual probability of each world W given act A), and EDT as `∑_W V(W)·P(W|A)` (p. 4). [S] https://philarchive.org/archive/FULECA (author and year not shown in the extract; its latest citations are 2021).
- **Sources:** SEP sec. 1.1; Edlin et al.; Gelman et al.; Mulligan & Hunter; Dowding; Geys.
- **Fit:** exact. The owner's counted-versus-uncounted ballot with others fixed *is* this counterfactual.
- **Implication:** estimates of p cluster around 10⁻⁷ for the best-placed US presidential voters (Gelman et al. 1998: "about 1 in 10 million for all states" in 1992, "about 1 in 1.5 million for some small states in some close elections"; Gelman, Silver & Edlin 2008: "1 in 10 million" in the best 2008 states, "1 in 60 million" for the average voter, "closer to 1 in a billion" in New York, California and Texas); SEP: the expected benefit under binomial models is "worth far less than a millionth of a penny" (extractor's quote). Edlin et al. (p. 6): with ±6% vote differential, p ≈ 1/(0.12n), and with n = 1 million and a self-benefit worth $10,000 the expected gain is "less than 10 cents" ([M] check: p = 8.3×10⁻⁶, pB = $0.083). So **under 3.1 with self-only B, pB < C except in small or very close elections**; whether it is below C depends on C (section 4) and on p's source (section 5).
- **Contested premise: how large p is.** Barnett (2020) argues d ≥ 1/N (N citizens) and, with b > 2c, that EB exceeds cost; his chances argument rests on two assumptions he names, "Partial Unimodality" and "Narrow Upsets" (pp. 434, 437), and he calls the binomial model "a very poor way to model real-world elections" (p. 441). A published reply (JESP) says his reasoning "may apply to significantly less real-life scenarios than he suggests" and that he is "too quick on one key premise" (the extractor could not see which); https://jesp.org/index.php/jesp/article/view/2915 [S: abstract only]. Mulligan & Hunter find very close elections are "more rare than the independent binomial model predicts" (abstract). [S] These are in tension and the sources do not reconcile them.

### 3.2 Causal contribution / overdetermination (Goldman 1999; Tuck 2008)

- **What it says counts:** a vote is among the causes of the winner's victory even when the outcome would not have differed without it.
  - Goldman, via Ridge (2021, *J. Political Philosophy*, https://core.ac.uk/download/391332717.pdf): "Non-swing voters in a massive election make causal contributions"; "it is not true that if they had not voted as they did that the outcome would have differed"; on the "vectoral model" the causes of victory "are the votes he receives." Ridge says Goldman's account "does not rely on the delusional idea that voting in massive elections is likely enough to determine the outcome." [S, secondary]
  - Goldman's own abstract (Cambridge): two readings of "why should citizens vote?", "in a prudential sense, and in a moral (or quasi-moral) sense", and he says he will "mainly try to answer the moral version"; footnote 39: a non-swing voter can still raise the probability of earning "causal credit", which is "no longer linked to the probability of being a swing voter" (extractor). Body paywalled. https://www.cambridge.org/core/journals/social-philosophy-and-policy/article/abs/why-citizens-should-vote-a-causal-responsibility-approach/6628D3915B2973208BBD49C15C90394B [S]
  - Tuck, via S. M. Amadae's review (*Ethics*, Oct. 2008, 198-202, https://philarchive.org/archive/AMABRR-2): "the existence of a threshold within a practice such as an election gives us reason to participate"; "each ballot could be a member of the efficacious set"; to deny voting's rationality is "to deny the causal efficacy that each vote has"; and "if there were a recount, one's ballot could move from the inefficacious set to the efficacious set." [S, via a review]
  - SEP (sec. 1.3, extractor): these theories hold "voting is rational provided the voter sufficiently cares about being a cause or among the joint causes of the outcome."
- **Fit:** not the owner's question. He defines importance as the chance the vote itself flips the outcome. These views *accept* that p is tiny and claim p is the wrong test of mattering. [I]
- **Implication:** they give no expected-benefit number: what a vote contributes is credit, responsibility or a reason to participate (Goldman's "prudential" reading is the one that coincides with 3.1). So they do not say pB > C; they say the question is not only pB vs C. [I]
- Tuck's and Goldman's own texts are unread; the above is through a reviewer and a commentator.

### 3.3 Triggering / threshold arguments (Kagan; Parfit)

- Kagan (2011), "Do I make a difference?", *Philosophy & Public Affairs*: "In triggering cases there is a small chance that the act makes a big (morally relevant) difference"; with a 1-in-T chance of triggering an order of T chickens, the act "has a negative expected utility"; "Collective action cases are all triggering cases"; "Do I make a difference? I might." (pp. 119, 140). **Voting is not discussed in the text** (extractor). https://pdf.stafforini.com/kagan-2011-make-difference.pdf [S]
- Barnett cites Parfit against ignoring tiny chances: "When the stakes are very high, no chance, however small, should be ignored" (p. 439, extractor). Parfit's own text is unread.
- [I] This is 3.1's maths read morally: the expected effect of your act equals (chance you trigger) × (size of what the trigger changes). It does not contradict the owner's setup; it says the tiny p can be matched by a large B, which is a statement about B (3.7) and about whether tiny probabilities count (Barnett's and Parfit's point), not a different definition of mattering.

### 3.4 Evidential / correlated-decision views

- **Sources:** Quattrone & Tversky (1984), "Causal versus diagnostic contingencies: on self-deception and on the voter's illusion" (**unread**; described by Acevedo & Krueger): "voters regard their own decisions as being diagnostic of the decisions of millions of other voters" who share their preferences (p. 117, extractor); weaker reading: they "may merely believe that their own actions are diagnostic of collective behavior" (p. 118). Acevedo & Krueger (2004, *Political Psychology*): Study 1, 110 undergraduates, hypothetical nation "Delta", the illusion measured as a correlation of r(108) = .19, one-tailed p = .027 (p. 122), which the extractor calls a modest effect; Study 2 (N = 86, 2000 US presidential election) found no measure of the illusion. https://scispace.com/pdf/two-egocentric-sources-of-the-decision-to-vote-the-voter-s-x8k3uughbj.pdf [S] (an aggregator copy).
- Grafstein's "An evidential decision theory of turnout" (1991, *AJPS*; **unread**), via Dowding pp. 449-450: it replaces "the causal decision theory component by Richard Jeffrey's (1983) evidential decision theory"; Dowding argues (extractor's paraphrase) that the smoking analogy shows evidential links do not make voting rational, and that a colleague analogy "fails" (p. 450). [S]
- "Evidence, Causality, and Collective Action" (philarchive FULECA, author not shown): "Evidential decision theory can require us to do our part even when causal decision theory does not"; "When individuals are similar to one another, their actions are non-causally correlated" (p. 3); "You should do your part, provided that enough others will likely do as you do" (p. 18); objections discussed: "too much other evidence" (p. 14) and the tickle defense (p. 14, fn. 17); it uses Edlin et al.'s "one in ten million" (p. 12). [S] https://philarchive.org/archive/FULECA
- **What counts as mattering:** your choice is evidence of what like-minded voters do, so the relevant probability is conditional on your act, `P(W|A)`, not counterfactual.
- **Fit:** [I] this is the framework most sensitive to *how* "everything else held fixed" is read. If it means *others' choices are causally independent of mine* (no persuasion, no one knowing), then CDT applies and the evidential link survives untouched, because it needs no causal path: it works through shared dispositions. If it means *others' choices are the same in both worlds as a stipulation*, the evidential reading is excluded by stipulation, not refuted. The owner's own words ("as many people as you would have convinced... you do in either case") fix the causal channel; they say nothing of correlated dispositions. This is a place where the owner's setup is silent, not clearly closed.
- **Implication:** if EDT is admitted, the expected benefit scales with the number of voters whose choice tracks yours; the sources give no measured correlation for real elections (the only number is r = .19 in a hypothetical-nation experiment, which measures a belief, not a correlation among real voters).

### 3.5 Rule- or group-consequentialist views

- **Harsanyi (1980)**: quoted by Geys, "a rule that would maximize social utility if it were followed by everybody" (pp. 20-21). [S] Harsanyi's text unread.
- **Coate & Conlin (2004)**, "A group rule-utilitarian approach to voter turnout", *AER* 94(5): 1476-1504 (working paper https://www.nber.org/system/files/working_papers/w8720/w8720.pdf [S]): each group (supporters, opposers) picks a "reasonable level" of voting cost below which members vote, chosen to "maximize the payoff of a representative member of my group" (p. 3); a supporter's expected payoff `π(γs, γo)b − γs²/2c` (p. 11; the extractor warned formulas were garbled in places, so I rely on the prose); data: 363 local liquor elections in Texas, 1976-96 (p. 9). The extractor corrected my assumption: the paper **does not test the model against the pivotal-voter model**; it says that comparison "has yet to be demonstrated" (p. 24), and compares against two ad hoc alternatives (the basic model fits best: log-likelihoods 749.20, 704.05, 692.26, p. 23). On closeness the paper says "this all depends on how we measure closeness" (p. 10).
- **Feddersen & Sandroni (2006)**, "A theory of participation in elections", *AER* 96(4): 1271-82: draft read (https://www.kellogg.northwestern.edu/faculty/fedderse/homepage/papers/duty4-15-02.pdf, an earlier draft titled differently; the extractor labelled it "duty"): ethical agents "receive a payoff D>cl for doing their part" (p. 11); consistent behaviour is a cost cut-off ("Agents with voting costs below this threshold should (and will) vote", p. 5); "a single vote is never pivotal" (p. 4) in the large-population model; minority turnout exceeds majority turnout (p. 5). [S] Published version unread.
- Geys on group-based models: "group-based models of turnout go a long way towards explaining our 'stylised facts'" (p. 24); he also notes Coate & Conlin's warm glow is "restricted to behaving like as should towards people on one's own side of the issue" (p. 20). [S]
- **What it says counts:** the unit of evaluation is the *rule* "vote if your cost is below a cut-off" applied by everyone on your side, and the group's welfare under that rule.
- **Fit:** [I] opposite to the owner's setup. His setup varies one ballot and holds others fixed; a rule-consequentialist varies the *policy* of a group. A group can gain more from the rule than the rule costs it while any one member's marginal ballot still has tiny p.
- **Implication:** these models explain turnout; they do not claim a single vote's p × B beats C. They reclassify the reason to vote as compliance with a beneficial rule, i.e. close to D (3.6) with a consequentialist justification.

### 3.6 Expressive and consumption voting (Brennan & Lomasky; Brennan & Hamlin; the D term)

- SEP (sec. 1.3, extractor): "The expressive theory of voting (G. Brennan and Lomasky 1993) holds that voters vote in order to express themselves"; voting is "a consumption activity rather than a productive activity"; compared to sports fans' displays of loyalty. [S]
- Brennan & Hamlin (1998), "Expressive voting and electoral equilibrium", *Public Choice* 95: 149-175, abstract only (https://eprints.soton.ac.uk/32947 [S]): the instrumental account treats the vote as "a revelation of preference over possible electoral outcomes", the expressive as "expressing support for one or other electoral options", with the football-cheering analogy. Full text not visible; **I could not confirm the payoff structure**.
- Hamlin & Jennings (2011), "Expressive political behaviour: foundations, scope and implications", *BJPolS* 41: 645-670 (https://core.ac.uk/download/9030083.pdf [S]): "voting may be motivated by concerns other than a concern for the eventual outcome of the election" (p. 2); "their individual vote is extremely unlikely to determine the electoral outcomes" (p. 2); "the price of expressive behaviour is low, and we should expect it to dominate" (p. 8, placing voting in an "economics of low-cost decisions"); they state "we do not pursue the specification of a formal utility function" (p. 3). So **no explicit formula** of the form p·B + expressive − c is given in that paper.
- Geys on the D term: it "does so at a severe price", because "the model loses all predictive value" (p. 19). [S]
- Gerber, Huber, Doherty & Dowling (2016), "Why people vote: estimating the social returns to voting", *BJPolS* 46(2) (abstract only): "information about whether a person votes directly affects how favorably that person is viewed"; people "are willing to take costly action in a dictator game to reward political participation". https://www.cambridge.org/core/journals/british-journal-of-political-science/article/why-people-vote-estimating-the-social-returns-to-voting/5C6F75024BD0A621729DB16F5FCBACC9 [S]. No number for the size of the social return was visible.
- **What counts as mattering:** the act itself (expressing, belonging, being seen to vote), independent of the outcome.
- **Fit:** [I] outside "importance" by the owner's definition (it is independent of the chance the vote decides). The owner's isolation ("no one knows") also removes the *social* part of D (Gerber et al.'s reputational returns). But D is not removed from the person's *own* cost-benefit: Edlin et al. fold it into c ("the costs, minus the direct benefit of voting", so c can be negative).
- **Implication:** if D ≥ C then voting pays whatever p is. Whether the owner's claim "the expected benefit cannot outweigh the cost" is about the *outcome-benefit only* (pB) or about *all benefit* is a classification the sources make both ways; it is the owner's to settle (section 6).

### 3.7 Altruistic / social-welfare voting (Edlin, Gelman & Kaplan; Fowler; Barnett)

- **Edlin, Gelman & Kaplan (2007):** abstract: "For voters with 'social' preferences, the expected utility of voting is approximately independent of the size of the electorate", and "a feedback mechanism keeps turnout at a reasonable level under a wide range of conditions." Model: eq. 1 ΔU = pB − c; eq. 2 B = B_self + αN·B_soc; eq. 3 p = K/n (n voters, K "competitiveness"); worked example: B_soc = $10 per citizen, α = 0.1, n/N = 1/3 → expected social value of the vote ≈ $250 and voting worthwhile if c < $25 (p. 6). The paper "gives no empirical estimate of c". [S] https://www.nber.org/papers/w13562.pdf
- **Fowler (2006)**, "Altruism and turnout", *J. of Politics*: via a Greater Good (Berkeley) article, not the paper: people who gave more in a dictator game "were significantly more likely to have voted in the most recent election"; "Altruism only mattered among people who were politically partisan"; Fowler's reading: "altruism combined with the belief that politics matters". https://greatergood.berkeley.edu/article/item/altruistic_electorate [S, secondary]. Geys p. 20: Fowler argues "only those with different preferences... ('discriminating altruists') are motivated to vote by altruism" and gives an altruism-weight utility function (eq. 3, α "the weight we attach to other's happiness"). [S] Sample size and effect size not seen. The paper itself is unread.
- **Barnett (2020):** counts the whole public with equal weight; b > 2c; d ≥ 1/N (3.1). [S]
- **What counts as mattering:** the decisive vote × the benefit to everyone affected, discounted by α (or not discounted).
- **Fit:** [I] not excluded by "all else equal": it does not change the counterfactual (p) at all, only *whose welfare is in B*. The owner called this question premature until the framework is set; the framework table shows it is a B-term choice that interacts with p: p ∝ 1/n and the social part of B ∝ N, so (as Edlin et al. show) their product is roughly flat in electorate size.
- **Implication:** the claim "expected benefit rarely outweighs cost" is **sensitive to this choice**: with self-only B it follows from the p estimates (3.1); with α = 0.1 and $10 per person it fails in the Edlin et al. example ($250 vs c < $25). It is also sensitive to the perceived-benefit input: B_soc is "perceived", not measured (p. 5), and the paper expects α < 1 for most people.

### 3.8 Others the sources mention (not in the brief's list)

- **Minimax regret** (1.3).
- **Strategic / game-theoretic turnout** (Palfrey & Rosenthal 1983, 1985): Geys p. 22: "by resorting to game theory does not succeed" (quoting Mueller), and positive turnout "disappears under realistic assumptions" (p. 28); Coate & Conlin cite Palfrey & Rosenthal for "the only citizens who vote in equilibrium are those for whom d is no smaller than c" in large electorates (p. 5). [S, via Geys and Coate-Conlin] Originals unread.
- **Adaptive learning**: Geys p. 27: "Introducing 'learning' into the voter calculus appears highly promising" but with no empirical evidence yet; also "a much-needed avenue of future (experimental) research". [S]
- **"Mandate"** (SEP 1.2): votes might change how effective a winner is; the extractor reports (paraphrase) that SEP rejects it for two reasons, one being that political scientists largely reject the claim that mandates affect effectiveness. A vote's effect on a winner's mandate is a consequence the owner's setup (a one-vote change in the count) leaves unspecified. [S]

---

## 4. The cost term C

### 4.1 What the literature counts as cost

- Downs and Aldrich treat costs as small ("these costs are only minor", Geys p. 18, [S]); Dowding: "The costs are low for most people most of the time" (extractor, no source number given). Geys (p. 18): the prediction that "turnout falls with increasing costs" is described as generally supported empirically (extractor's paraphrase). [S]
- Components in the literature I read: time voting; waiting; travel to the polling place; search for the polling place (Brady & McNulty: "Both transportation and search costs caused these changes"); registration (the Cost of Voting Index's central items; the CPS reason "registration problems"); information (Downs's cost; no measured figure found, section 4.5).
- Edlin et al. define c as net: "the costs, minus the direct benefit of voting" (p. 4); it can be negative.

### 4.2 Measured waiting and time-at-polls

| Measure | Figure | Source (all [S], via extract; a search was one pass) |
|---|---|---|
| SPAE 2022 average wait | "The average Election Day voter waited six minutes before voting; the average early voter waited four minutes." (p. 20). The report does not say whether these are means or medians. | MIT Election Data & Science Lab, *How We Voted in 2022* (Charles Stewart III, as the extractor read it): https://electionlab.mit.edu/sites/default/files/2023-05/HowWeVotedIn2022.pdf |
| SPAE 2022 waits over 30 min | Election Day 6%, early 4% (p. 3); African Americans 8.2% vs Whites 3.4% (p. 21); Florida, Tennessee and DC over 10% of in-person voters (p. 21) | same |
| SPAE 2022 "line too long" as a non-voter reason | 2.2% of non-voters in 2022, down from 5.0% in 2020 (p. 24) | same |
| SPAE 2024 waits over 30 min | Election Day 11% (2020: 14%), early 15% (2020: 21%) (pp. 3, 18); average waits "decreased" (p. 3), no minutes given; non-voter reasons: "did not like the candidates" 20.9%, "sick or disabled" 12.1%, "other" 11.6% (p. 24); 77% found their polling place "very easy" to find (p. 15) | https://electionlab.mit.edu/sites/default/files/2025-07/HowWeVotedIn2024.pdf |
| SPAE 2020 waits over 30 min | early 22%, Election Day 14% (p. 19); question: "Approximately, how long did you have to wait in line to vote?"; 18,200 registered voters, administered by YouGov (p. iii). No average given. | https://electionlab.mit.edu/sites/default/files/2021-03/HowWeVotedIn2020-March2021.pdf |
| Pew / SPAE 2012 | early voting lines averaged 20 min vs 13 min on Election Day; 13% waited more than 30 min; Florida nearly 50 min, Maryland over 30, South Carolina and Virginia over 25; 10,200 people (about 200 per state and DC). "Final, comprehensive data will be released later." | https://www.pewtrusts.org/en/research-and-analysis/articles/2012/12/10/new-data-on-lines-at-the-polls |
| Stewart on 2016 vs 2012 | Florida "from an average of 45 minutes to less than 10 minutes"; "More than 10% of voters waited longer than 30 minutes in roughly half the states" (the extract does not make the year clear); the Black-white early-voting disparity "narrowed only slightly" | https://electionacademy.lib.umn.edu/2016/12/15/charles-stewart-this-just-in-lines-at-the-polls-shorter-in-2016-than-in-2012 |
| Smartphone data, mean time at a polling place | mean 19 min (19.13, Table A.1), median 14 min, 18% over 30 min; 154,489 people at 43,413 polling places; midpoint of lower and upper bounds from pings; entirely-Black block groups waited about 5 min (5.23) longer, 29% longer; year 2016 per the NBER Digest title only. The paper gives **no dollar value** of time or count of deterred voters. Authors per the extractor: Chen, Haggag, Pope and Rohla (my query had the fourth name wrong). | https://arxiv.org/pdf/1909.00024 |

**Discrepancy to resolve (wave 2).** The 2022 report's extract gives the 2020 share waiting over 30 minutes as 5% (Election Day) and 7% (early) (p. 3); the 2020 report gives 14% and 22%, and the 2024 report gives 14% and 21% for 2020. The extractor said all of these refer to "more than 30 minutes". They cannot all be right; I could not tell whether the extractor misread the 2022 page or the 2022 report uses another measure. Do not use the 2022 report's comparison until checked at source. Also: the 2022 report lists its sample as 10,200 in one place and 10,100 in another (p. 38), and the 2024 report likewise (p. 41).

### 4.3 Travel, distance and the value of time

- **Gibson, Kim, Stillman & Boe-Gibson**, "Time to vote?" (IZA DP 5854, 2011; later *Public Choice* 2013): New Zealand 2005 general election, validated survey voters (n = 3,005 weighted); national mean distance to the polling place about 1.5 km, mean travel time 5.1 minutes; imputed mean wage just under NZ$28/hour (about US$19.50); estimated cost about **NZ$2.30 per trip (US$1.60)** nationally, NZ$1.80 (US$1.25) urban; parking and waiting excluded; each minute of travel time reduces turnout by 0.5 percentage points and each $1 of opportunity cost by 0.8 points (national sample; urban: 0.8 and 2.0). At a $10 cost, predicted national turnout 75%, seven points below the mean. The extractor said the paper uses the full imputed wage as the value of time, without stating a fraction. https://docs.iza.org/dp5854.pdf [S]
- **Cantoni (2020)**, "A precinct too far", *AEJ: Applied* 12(1) (author version, https://cris.unibo.it/bitstream/11585/801478/9/app.20180306_copyright.pdf [S]): nine urban municipalities in Massachusetts and Minnesota, elections 2012, 2013, 2014, 2016; mean parcel distance 0.365 mile (s.d. 0.245); a one-s.d. increase in distance reduces ballots cast by 2 to 5 percent, "1 to 3 percentage points" of turnout; the effect is about three times larger in high-minority areas in non-presidential elections; the 2012 presidential election shows no minority heterogeneity; eliminating the distance effect would raise turnout 1.6 to 4 points. **No monetisation.** (The extractor's per-0.1-mile conversion, 0.4 to 1.2 points, is its arithmetic and not the paper's.)
- **Brady & McNulty (2011)**, "Turning out to vote", *APSR* 105(1): 115-134 (abstract only; https://www.cambridge.org/core/services/aop-cambridge-core/content/view/6CB07495AFC81E3251CC01A60A10B8FB/S0003055410000596a.pdf/ [S]): 2003 California recall election, Los Angeles County precinct consolidation: "Overall turnout decreased by a substantial 1.85 percentage points", polling-place turnout fell 3.03 points, absentee voting rose about 1.18 points; "Both transportation and search costs caused these changes." Distances, counts and costs are in the paywalled body.
- **Value of an hour.** BLS Employment Situation, October 2026 (released 2026-11-06, 8:30 ET per the extractor): average hourly earnings, all private nonfarm employees **$38.00**; production and nonsupervisory **$32.75**. https://www.bls.gov/news.release/empsit.nr0.htm [S] (the quote the extractor gave was only the "increased by 14 cents" sentence; the level was reported alongside it, so re-read it at source). Which fraction of the wage to charge for non-work time is a convention: Gibson et al. charge the full imputed wage; a blogger's Florida estimate "value[s] an hour of leisure at the same rate as work". Other conventions exist in the time-valuation literature; I read none.
- **A cautionary example.** A Discourse.net post (Michael Froomkin, 2012-11-06) puts "up to $190 million" of lost time on Florida early voting by assuming 2-4 hour waits, 2,413,472 in-person early voters and a BLS Florida wage of $19.59; it is the author's "own back-of-the-envelope estimate, not a published study". https://www.discourse.net/2012/11/wasted-time-in-line-for-early-voting-cost-floridians-up-to-190-million/ [S] [I] Its 2-4 hour assumption comes from some Miami-Dade polling places and is far above the 20-minute early-vote average Pew found statewide in the same year; I would not cite it as a figure.

### 4.4 The Cost of Voting Index (CoVI) and non-voters' reasons

- **CoVI** (Li, Pomante & Schraufnagel, *Election Law Journal* 17(3), 2018, and updates): a **policy** index that ranks states by how hard their laws make voting; it does **not** give minutes or dollars. Described as: 33 variables on registration and voting laws, with registration deadlines carrying the most weight (Phys.org 2018 article, https://phys.org/news/2018-10-scrutinizes-effort-vote-state.pdf [S]); "ranks each state by the time and effort it takes to vote" (NIU newsroom, 2022-10-05, https://newsroom.niu.edu/?p=12676 [S]); ten categories under registration and voting, "rankings for every two years since 1996" (Wikipedia, https://en.wikipedia.org/wiki/Cost_of_Voting_Index [S], a pointer only). Rankings: 2016, Oregon easiest, Mississippi hardest (Phys.org). 2022, *Election Law Journal* 21(3): 220-228: Oregon "maintains the first position as the easiest state", Mississippi and New Hampshire "stay at the bottom of the rankings" (abstract via https://search.bvsalud.org/global-literature-on-novel-coronavirus-2019-ncov/resource/en/covidwho-2070074 [S]); the NIU piece lists the top eight as Oregon, Washington, Vermont, Hawaii, Colorado, California, Nevada, Utah, with New Hampshire 50th and Mississippi 49th. The extracts gave **ranks, not index values**, and no scale direction was stated in the Wikipedia extract (Phys.org says higher means costlier). The NIU extract says "the original index dates to 2020"; the Phys.org and Wikipedia pieces date it to 2018 (rankings back to 1996). Unreconciled.
  - [I] CoVI is useful for *which states have higher legal cost*, not for converting C to a figure; the conversion would need an additional source linking index to time or money, and I found none.
- **Registered non-voters' stated reasons, 2020** (Census Bureau P20-585, Table 3; 12.8 million registered non-voters; https://www.census.gov/content/dam/Census/library/publications/2022/demo/p20-585.pdf [S]): not interested 17.6%; did not like candidates or campaign issues 14.6%; other 14.5%; **too busy, conflicting schedule 13.1%**; illness or disability 13.0%; out of town 6.1%; **registration problems 4.9%**; COVID-19 concerns 4.3%; forgot 3.7%; don't know/refused 3.2%; **inconvenient polling place 2.6%**; **transportation problems 2.4%**; bad weather 0.1%. These sum to 99.9% [M]. They are self-reports of why a *registered* person did not vote, not measures of cost.

### 4.5 What I did not find

- A measured figure for the cost of becoming informed (one search, only textbook pages returned).
- A measured time to cast a ballot once at the booth, or a measured time to register.
- Any study that values voting time in money **and** reports a per-voter dollar figure besides Gibson et al. (NZ, travel only).

### 4.6 Illustrative conversions [M]

Arithmetic only (script output above); wage inputs are the BLS figures in 4.3, minutes are the figures in 4.2. **Not an estimate of C** (a person's C is not the national average; the wage convention is a choice).

| Minutes | Source of minutes | at $38.00/h | at $32.75/h |
|---|---|---|---|
| 4 | SPAE 2022, early | $2.53 | $2.18 |
| 6 | SPAE 2022, Election Day | $3.80 | $3.28 |
| 13 | Pew 2012, Election Day | $8.23 | $7.10 |
| 19 | Smartphone mean time at polls, 2016 | $12.03 | $10.37 |
| 20 | Pew 2012, early | $12.67 | $10.92 |

Add travel (Gibson et al.: NZ$2.30, about US$1.60 per trip, a different country and year) and any information or registration time, none of which has a US figure in what I read.

---

## 5. Published p × B calculations, and how each chooses B

| Study | p | B | Result |
|---|---|---|---|
| Edlin, Gelman & Kaplan (2007) | p = K/n; K = 10 for close elections ("10/n", Appendix p. 20); ±6% differential gives p ≈ 1/(0.12n) (p. 6); fn. 3: "10⁻⁷ or 10⁻⁸ are more reasonable values for U.S. Presidential elections" | B = B_self + αN·B_soc; B_self $10,000; B_soc $10 per citizen; α = 0.1 | n = 1 million: self-interest gain "less than 10 cents"; with social preferences, $250 expected value, so voting pays if c < $25 (p. 6). Simulations of turnout use K = 10, n_elig/N = 1/3 and an assumed noncentral-Cauchy c/b distribution (Fig. 1), "to illustrate", not to estimate. [S] |
| Gelman, King & Boscardin (1998) *JASA* | state tie density from a forecast model × conditional probability the state is pivotal; ½ for ties; state-level error s.d. about 3.5% (p. 5) | none (the paper "does not compute the expected utility of voting or a benefit-cost ratio") | 1992: "about 1 in 10 million for all states"; varying "by about a factor of 10 among states"; Vermont "1 in 3.5 million"; some small states in some close elections "1 in 1.5 million"; landslides "on the order of 1 in hundreds of millions"; popular-vote "approximately 1 in 13.3 million" (pp. 5-6). [S] https://gking.harvard.edu/files/estimatprob.pdf |
| Gelman, Silver & Edlin (2008 manuscript; the extractor could not confirm *Economic Inquiry* 50(2): 321-326, 2012, from the manuscript, and that attribution rests on a search-result title) | `P(state pivotal) × P(tie | pivotal)`; Student-t(4) tie density | none in dollars: a vote is "like a lottery ticket with a 1 in 10 million chance of winning"; benefit framed as the chance "to change national policy and improve (one hopes) the lives of hundreds of millions" (p. 4) | 2008: best states 1 in 10 million; average voter 1 in 60 million (turnout-weighted); New York, California, Texas "closer to 1 in a billion"; DC and Utah values in fn. 11 (5e-85 to 2e-12 and 9e-16 to 2e-10). 2008 presidential election only. [S] |
| Mulligan & Hunter (2003) *Public Choice* 116: 31-54 | empirical frequency: 16,577 US House elections 1898-1992: one decided by a single vote; 40,036 state legislative elections 1968-89: two ties, seven single-vote | none | about 1 in 100,000 votes (House), about 1 in 15,000 (state legislature; the body's 0.00006 is about 1 in 16,700); "Very close elections are more rare than the independent binomial model predicts." [S] https://www.nber.org/papers/w8590.pdf |
| Dowding (2005), quoting others | McLean (1987): 0.00000006, British general elections; Mueller (1989): 0.00006, a US presidential election; Carling (1995): "10⁻⁹⁰" if each vote has probability 0.499 (the extractor says the superscript was lost); Riker & Ordeshook "made it 10⁻⁸" (n. 6) | none | [S] The superscripts are the extractor's reconstruction; check at source. |
| Barnett (2020) | d ≥ 1/N whenever both candidates have at least a 10% chance (p. 432); d ≥ 10u/N with u the upset probability (p. 437) | B = b × N, whole public; stakes condition b > 2c | EB = ½·B·d; in his example "at least +$134.92, and probably much greater" (p. 441). [S] https://philosophersannual.org/40articles/barnett-why.pdf |
| SEP sec. 1.1 | binomial models | not stated | expected benefit "worth far less than a millionth of a penny"; "a 1 in 10 million chance of breaking a tie" in close states (Edlin et al.). [S] |
| VoteHub Voter Power Index (2026) | tipping-point probability of the seat for chamber control (Texas 19%, Senate) | none | an index, "not a literal probability that a vote is decisive"; "The top ten percent of voters hold roughly 60% [sic] of VPI". [S] |

**How B is chosen in these.** Edlin et al. set it by assumption with stated round numbers ($10,000 own stake; $10 per citizen; α = 0.1), which they call suggestive. Gelman et al. leave B qualitative. Barnett argues the stakes condition from examples (tax relief for below-median earners; the cost of the Iraq and Afghanistan wars, pp. 427-8) and sets the threshold at "more than twice" the cost. No study I read **measures** B. The survey tradition behind Riker & Ordeshook measures a *perceived party differential* (Sanders: "perceived differential in benefits offered the voter"); I read no measured values.

**Break-even [M].** The test pB > C is equivalent to B > C/p. Using C = $3.80 (6 minutes at $38/h, SPAE 2022 Election Day) and C = $12.03 (19 minutes), B* = C/p is:

| p (source) | B* at C = $3.80 | B* at C = $12.03 |
|---|---|---|
| 6.7×10⁻⁵ (1 in 15,000; Mulligan-Hunter, state legislatures) | $57,000 | $180,500 |
| 1×10⁻⁵ (1 in 100,000; Mulligan-Hunter, House) | $380,000 | $1.2 million |
| 1×10⁻⁷ (1 in 10 million; Gelman et al.) | $38 million | $120 million |
| 1.7×10⁻⁸ (1 in 60 million; Gelman, Silver & Edlin, average) | $228 million | $722 million |
| 1×10⁻⁹ (1 in a billion; NY/CA/TX) | $3.8 billion | $12 billion |

The Mulligan-Hunter p is an average over all votes cast in those elections (a historical frequency), not a forward-looking probability for a given voter, and it counts a single-vote-margin vote as fully pivotal with no ½. I show the numbers as a map of scale, not as an estimate for any election; choosing p belongs to the decisiveness-model research.

---

## 6. Where sources disagree, and open questions

1. **What D is** (citizen duty / expressive benefit / consumption), and therefore whether the owner's "civic duty" objection is a D-term claim (3.6, 1.1). Original Riker & Ordeshook unread.
2. **How large p is**: GKB/GSE (forecast-based, about 10⁻⁷ at best) versus Barnett (d ≥ 1/N under two assumptions) versus Mulligan-Hunter (historical frequency, with the binomial over-predicting). The JESP reply disputes Barnett on "one key premise" the extractor could not identify. Not reconciled by any source I read.
3. **SPAE >30-minute shares** (4.2): the 2022 report's 2020 comparison conflicts with the 2020 and 2024 reports.
4. **Mean or median** for the SPAE 2022 six- and four-minute waits (unstated).
5. **Is "B" the gain if decisive, or the expected gain (pB)?** The owner's wording fits either (2.3).
6. **Tie rule.** The ½ is for a fair-coin tie; recounts, courts and runoffs change it (2.2; GKB fn. 6). The owner's open point on a margin of one is this.
7. **Whose welfare is in B** (3.7). Edlin et al. and Barnett count others; the owner has said the question is premature. The sources show the answer changes whether his conclusion holds, so it is a material fork, not a detail.
8. **Does C belong in the isolated comparison?** In his thought experiment you go to the polls and cast the ballot in both arms, so the trip cost is common to both and drops out of the difference; the cost then enters at the decision to go. Whether the site's "cost" is the trip, the time at the booth, information, registration, or all of them is his to say. [I]
9. **Whether "held fixed" is causal or evidential** (3.4): the evidential reading is not excluded by "no one knows".
10. **No source states B for a chamber seat as a utility quantity** (2.5); only the probability side (VoteHub) exists in what I read.
11. **Edlin et al.'s year**: the brief says 2007; the NBER page lists *Rationality and Society* 19(3): 293-314, **2007** (resolved); one Wikipedia extract said 2008 (wrong or another print date).
12. **CoVI origin date**: 2018 (Phys.org, Wikipedia) versus "dates to 2020" (NIU). Not reconciled.

---

## 7. Summary (one paragraph)

Every source I could read writes the calculus of voting as **a probability of decisiveness times a benefit differential, minus a cost, with an outcome-independent term D added** (SEP `U_v = p[V(D)−V(R)] − C`; Geys `R = PB − C + D`; Edlin et al. `ΔU = pB − c`; Dowding `pB + D > C`), and the sources disagree on what D is (citizen duty, expression, consumption). The expected value of one vote is p × B where, with a fair-coin tie rule, p = ½[P(others tied) + P(your side one short)] (my algebra, matching Gelman et al.'s and Barnett's ½). B is a **perceived utility difference between two outcomes**; with three or more candidates it becomes a sum over pairwise pivot events; for a seat or a state it is the difference the unit makes to a larger outcome, with p taking a two-level shape. The frameworks sort by what they count as the vote mattering: **pivotality** (exact fit to the owner's setup; p about 10⁻⁷ at best in a US presidential race, with Barnett's d ≥ 1/N the main dissent); **causal contribution** and **expressive** views, which accept p is tiny and claim p is not the test (they give no expected-benefit number); **evidential** views, which the owner's "no one knows" does not exclude unless "held fixed" is read causally; **rule/group** views, which change the unit from one ballot to a rule; and **altruistic** views, which keep the counterfactual but put others' welfare in B, making p × B roughly independent of electorate size and so the one choice on which the owner's conclusion actually turns. On cost, the measured figures are small and variable: average waits of about 4 to 6 minutes (SPAE 2022) to 13 to 20 minutes (Pew 2012), a mean 19 minutes at the polls (smartphone data, 2016), a New Zealand travel cost of about US$1.60 per trip, a distance effect of 1 to 3 points of turnout per 0.245 mile in two states, and stated reasons for not voting; none of these is a dollar C for a person, the Cost of Voting Index ranks laws and does not give minutes or dollars, and I found no measured information cost. Every figure is from a WebFetch extract, not a whole-page read, and the key primary texts (Riker & Ordeshook, Downs, Ferejohn & Fiorina, Goldman, Tuck, Brennan & Lomasky) were not readable.

---

## 8. Unread list

**Not readable (paywall, no open text, or the host refused):**
- Riker & Ordeshook (1968) full text: Cambridge paywall ("Temporarily unavailable"). The `R = PB − C + D` form is therefore unconfirmed as theirs.
- Ferejohn & Fiorina (1974) full text: same. Regret tables and the voting condition unseen.
- Downs (1957) and his *J. Political Economy* 1957 article: no open text reached; the one candidate (`is.muni.cz`) served a proof-of-work bot challenge, not circumvented, no further requests to that host. A third-party "virtual library" PDF of the whole book appeared in search and was not used.
- Goldman (1999) body and Tuck (2008, *Free Riding*) body: Cambridge abstract page only; Tuck read only through a review.
- Brennan & Lomasky (1993), Brennan & Hamlin (1998) full text (record only), Brennan (2011) *The Ethics of Voting*.
- Quattrone & Tversky (1984) original; Grafstein (1991); Harsanyi (1980); Parfit (1984) *Reasons and Persons*; Lewis (1979); Nefsky.
- Fowler (2006) paper itself (only a magazine article about it and Geys's description); Gerber et al. (2016) body.
- Palfrey & Rosenthal (1983, 1985) bodies; Myerson & Weber (1993); Feddersen (2004, *JEP*; I used a URL built from memory that returned a different article, discarded); Feddersen & Sandroni (2006) published version (read an earlier draft); Coate & Conlin published *AER* version (read the NBER working paper).
- Brady & McNulty (2011) body (paywall); Li, Pomante & Schraufnagel (2018) body and CoVI index values (ranks only seen); Chen et al. dollar values (the paper gives none).
- Gelman, Silver & Edlin as published in *Economic Inquiry* (read a 2008 manuscript); Tullock (1967); Good & Mayer (1975); Banzhaf (1968); Gelman, Katz & Bafumi (2004); Barnett's reply authors (JESP page shows none).
- The SPAE microdata, the Election Lab's own wait-time pages (the 2016 EPI blog page returned no body text), BLS release read through an extract.

**Hosts the sandbox's network policy refused for `curl`** (all 403 on CONNECT; named by the proxy status): plato.stanford.edu, sites.stat.columbia.edu, en.wikipedia.org, arxiv.org, archive.org, www.jstor.org, papers.ssrn.com, core.ac.uk, electionlab.mit.edu, ideas.repec.org, api.crossref.org, api.openalex.org (my requests); www.nber.org and link.springer.com (seen in the proxy log from other sessions). If the maker wants wave 2 to read these whole, those are the hosts to add under "Allowed domains".

**Read only as abstract or record:** Riker & Ordeshook, Ferejohn & Fiorina, Aldrich, Goldman, Brady & McNulty, Brennan & Hamlin, Palfrey & Rosenthal 1983, Gerber et al. 2016, Coate & Conlin (NBER page, then the working paper), the Economic Inquiry record.

**Used with low confidence (secondary or aggregator copies):** Sanders 1980 (a copy on newschoolhistories.org), Salka 2017 (conference paper), Acevedo & Krueger (an aggregator copy), Geys (a UH-hosted copy), the 2025 arXiv review, Wikipedia (pointer only), the Froomkin blog post.
