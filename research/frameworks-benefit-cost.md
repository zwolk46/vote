# Frameworks for "does one vote matter": the benefit term and the cost term

*Status: DRAFT 1, written as the research proceeds (saved early so nothing is lost). Researcher: Sonnet 5.5 subagent, 2026-11-06. Sections marked TODO are not yet researched.*

## 0. How this was read (read this first)

- **curl was refused for every academic host.** Each request through `curl -sSL` to plato.stanford.edu, sites.stat.columbia.edu, nber.org, link.springer.com, arxiv.org, wikipedia.org, archive.org, jstor.org, ssrn.com, core.ac.uk, electionlab.mit.edu, ideas.repec.org, api.crossref.org and api.openalex.org ended in `CONNECT tunnel failed, response 403`. The proxy status endpoint names the cause: "gateway answered 403 to CONNECT (policy denial or upstream failure)". This is the sandbox's network policy (egress allowlist), not the sites refusing us. I did not retry, and did not route around it by any technical means. Only github.com and raw.githubusercontent.com answered, and they carry none of these sources. Per `read_documentation environment.network` the maker can widen "Allowed domains" in the project's cloud-environment settings; the hosts that mattered are listed in the unread list.
- **WebFetch was therefore used for every source below, as the brief allows when curl is refused.** WebFetch returns a small model's reading of the page, not the page. So: **every fact here is [stated, via WebFetch extract]**, not a whole-page read. The extractor also refused to reproduce long passages, so quotes are short fragments (under about 25 words). Where the extractor said it could not see something (paywalled full text, garbled symbols), I say so rather than fill it in. Nothing in this report is from my memory; where I know a source exists but did not read it, it is in the unread list, and the formula for it is not given.
- **Corroboration tags.** [stated] = one extract. [stated x2] = two independent sources agree. [inferred] = my reading across sources. [measured] = I computed it (none yet).
- **Search results** (WebSearch) were used only to find URLs. Result lists included mirror and proxy sites (for example a Chinese university web-VPN copy of a Sage article, `remotevs.com` copies of Gelman's site, `adambrown.info` notes); I did not use those as sources.

## 1. The calculus of voting and its paradox

### 1.1 What each source writes

| Source | Formula as the source's text gives it | Terms | Read at |
|---|---|---|---|
| Stanford Encyclopedia of Philosophy, "The Ethics and Rationality of Voting", sec. 1.1 | `U_v = p[V(D) - V(R)] - C` | p "the probability that Sally's vote is decisive"; V(D) - V(R) "the difference in the expected value of the two candidates"; C "the opportunity cost of voting" | https://plato.stanford.edu/entries/voting/ [stated, WebFetch extract] |
| Edlin, Gelman & Kaplan (2007), eq. 1 | `ΔU = pB - c` | p probability a single vote is decisive; B "relative benefit of the voter's preferred candidate winning"; c net cost = "the costs, minus the direct benefit of voting" (p. 4) | https://www.nber.org/papers/w13562.pdf [stated, WebFetch extract] |
| Dowding (2005), "Is it rational to vote? Five types of answer and a suggestion", BJPIR 7: 442-459 | `pB > C`; with D: `pB + D > C` | p probability of someone's vote being decisive; B "the benefit gained through the voter's favoured party winning"; C the cost of voting; D "can cover all sorts of private motivations" and is "an 'expressive benefit'" | https://core.ac.uk/download/156636542.pdf (pp. 442-443) [stated, WebFetch extract] |
| arXiv 2510.24344 (2025 review of behavioural approaches to turnout), sec. 3.1 | `ΔU = PB - C`; D "adding the parameter D as a civic duty", attributed to Riker & Ordeshook | P prob. a vote can be decisive; B "the gain of the individual candidate's victory"; C "the net cost incurred by the individual in the voting process" | https://arxiv.org/pdf/2510.24344 [stated, WebFetch extract; a secondary source] |
| Riker & Ordeshook (1968), APSR 62(1): 25-42 | **Not read.** Cambridge page shows only abstract and footnote fragments; full text paywalled. The formula `R = PB - C + D` is the one in the owner's brief; **I could not confirm it from a source I read.** | Footnote fragments suggest B in "utiles", C cost, D a citizen-duty term (the extractor flagged this as its inference) | https://www.cambridge.org/core/journals/american-political-science-review/article/abs/theory-of-the-calculus-of-voting/F32A6F556750C8207E920CE9D0850A2E [stated: abstract only] |
| Downs (1957) | **Not read** (book). Known only through Dowding's quotations (below). | | |
| Ferejohn & Fiorina (1974), APSR 68(2): 525-536 | **Full text not visible** (Cambridge, "temporarily unavailable"). Abstract only. | see 1.3 | https://www.cambridge.org/core/services/aop-cambridge-core/content/view/0F89DD7019DEC0A1D8B0F4F33CB69CBE/S0003055400117368a.pdf/ [stated: abstract + some footnotes] |

**What the sources agree on.** [stated x3] The expected-utility rule is a probability of decisiveness times a benefit, minus a cost: three independent sources (SEP, Edlin et al., Dowding) write it so; the D term is an additive extra that is not multiplied by p. This is the structure the owner described.

### 1.2 The paradox as the sources state it

- Riker & Ordeshook abstract: "voting is an irrational act in that it usually costs more to vote than one can expect to get in return" and "we present empirical evidence that citizens actually behave as if they employed this calculus." The abstract adds that the reinterpreted calculus makes voting reasonable for those who vote and abstaining reasonable for those who abstain. [stated, Cambridge abstract page]
- Downs, as quoted by Dowding: "the party which eventually wins will probably be elected no matter how he casts his ballot" and "the vote value, which is nearly infinitesimal under most circumstances." [stated, via Dowding p. 443-448 extract; Downs's own text not read]
- SEP: voting "has opportunity costs... for most individuals, voting does not maximize expected utility, which gives rise to the 'paradox of voting' (Downs 1957)" (extract, paraphrase). [stated]
- Dowding classifies the replies into five types, in his words: the marginalist solution ("rational choice is good at predicting at the margin"); the C-term solution; the B-term solution ("By making the B term massive"); the p-term solutions ("the p term is defective and needs to be replaced"); D-term solutions ("the work in utility terms is done by 'D'"). [stated, Dowding p. 443]. **Use:** this five-way split is a ready map of the owner's question: his claim is that p is right, so the only escapes are B, C, D and the marginalist/other-decision-rule replies.

### 1.3 Ferejohn & Fiorina (minimax regret)

- Abstract: minimax regret "specifies voting under quite general conditions"; covers two- and three-candidate plurality elections; "a minimax regret decision maker never votes for their second choice in a three-candidate election, while expected utility maximizers sometimes do." [stated, abstract; paraphrased by extractor, partly in quotation marks]
- Footnote fragment: they assume the utility cost is below half the utility gap between preferred candidate winning and losing ("c < 1/2"), "without this assumption, abstaining would dominate voting." [stated, extract of fn. 12; the full regret table and the exact voting condition were NOT visible]
- Dowding's objection: minimax regret "cannot explain higher turnout in close elections" and "elections are not that uncertain" (p. 449). [stated]
- **Fit with the owner's setup:** minimax regret is a rule for deciding without probabilities; it ignores p entirely, so it does not measure "importance of a vote" as probability of decisiveness. [inferred]

## 2. What B is  -- TODO (draft 2)

## 3. Frameworks under which "your vote mattered" is evaluated -- partial (see below)

*(draft 2 will hold the full section; items read so far are noted here)*

- Causal responsibility (Goldman 1999), as described by Ridge (2021, J. Political Philosophy) from core.ac.uk/download/391332717.pdf: "Non-swing voters in a massive election make causal contributions"; "it is not true that if they had not voted as they did that the outcome would have differed," yet the vote has causal influence; it "does not rely on the delusional idea that voting in massive elections is likely enough to determine the outcome." Goldman's own text not read. [stated, via a secondary source]
- Tuck (2008), via S. M. Amadae's review in *Ethics* (Oct 2008, 198-202), https://philarchive.org/archive/AMABRR-2: "the existence of a threshold within a practice such as an election gives us reason to participate"; "each ballot could be a member of the efficacious set"; denying voting's rationality "is to deny the causal efficacy that each vote has." Tuck's own text not read. [stated, via a review]
- Expressive voting: Brennan & Hamlin (1998), abstract via Southampton eprints https://eprints.soton.ac.uk/32947: instrumental account treats the vote as "a revelation of preference over possible electoral outcomes"; expressive as "expressing support for one or other electoral options," compared to cheering at a football match. Full text not visible.

## 4. Cost term C -- TODO

## 5. Published p x B calculations -- partial

- Edlin, Gelman & Kaplan (2007), https://www.nber.org/papers/w13562.pdf [stated, extract]: B = B_self + αN·B_soc (eq. 2); p = K/n (eq. 3); worked example: ±6% vote differential gives p ≈ 1/(0.12n); with n = 1 million and B_self worth $10,000 the expected gain is "less than 10 cents" (p. 6); B_soc = $10 per citizen and α = 0.1 gives $10N/(0.12n), $250 in expected social value when n/N = 1/3, so voting pays if c < $25 (p. 6); "10/n" as the approximate probability in close elections; footnote 3: "10^-7 or 10^-8 are more reasonable values for U.S. Presidential elections"; abstract: "the expected utility of voting is approximately independent of the size of the electorate". The paper gives no empirical estimate of c.
- Gelman, Silver & Edlin, 2008 manuscript of "What is the probability your vote will make a difference?" (https://www.stat.berkeley.edu/~aldous/157/Papers/vote.pdf; the extractor could not confirm the Economic Inquiry 2012 attribution from the manuscript itself): best states (New Mexico, Virginia, New Hampshire, Colorado) "approximate 1 in 10 million chance"; "a voter in America has a 1 in 60 million chance of being decisive" (turnout-weighted); NY, CA, TX "closer to 1 in a billion"; method = P(state pivotal in Electoral College) x P(tie | pivotal), tie density from a Student-t with 4 d.f. fitted to simulated margins. [stated, extract]
- Dowding (2005) p estimates quoted from others: McLean (1987) 0.00000006 British general elections; Mueller (1989) 0.00006 US presidential; Riker & Ordeshook "made it 10^-8" (n. 6); Gelman et al. (1998) "around 1 in 10 million" nationally and "as low as 1 in 1.5 million in some swing states". [stated, Dowding pp. 448, 456]

## Unread list (running)

- Riker & Ordeshook 1968 full text (Cambridge paywall). Ferejohn & Fiorina 1974 full text (same). Downs 1957 (book; no open text found yet).
- Hosts refused by the sandbox network policy for curl: see section 0.
