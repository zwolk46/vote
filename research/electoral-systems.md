# How "one vote changes the outcome" works across electoral systems

*Research report (subagent "research-d", Sonnet 5.5), written 2026-11-06 UTC for the vote-importance site. Brief: how "one vote changes the outcome" works across electoral systems. Complete draft; every figure carries its source or its method.*

## 0. How this was read, and how far to trust it (read this first)

- **curl was refused for every host I tried.** One request each, spaced 3.5 s apart, to: `www.aceproject.org`, `www.idea.int`, `arxiv.org`, `www.cambridge.org`, `onlinelibrary.wiley.com`, `www.sciencedirect.com`, `academic.oup.com`, `pubs.aeaweb.org`, `mpra.ub.uni-muenchen.de`, `hal.science`, `eprints.lse.ac.uk`, `osf.io`, `www.econstor.eu`, `web.stanford.edu`, `www.electoral-reform.org.uk`, `commonslibrary.parliament.uk`. Every one ended `curl: (56) CONNECT tunnel failed, response 403`. The proxy status endpoint (`$HTTPS_PROXY/__agentproxy/status`) names the cause as "gateway answered 403 to CONNECT (policy denial or upstream failure)", and its list of recent refusals (from sibling subagents) adds `scholar.archive.org`, `core.ac.uk`, `www.semanticscholar.org`, `export.arxiv.org`, `statmodeling.stat.columbia.edu`, `www.researchgate.net`, `citeseerx.ist.psu.edu`, `www.pnas.org`, `projecteuclid.org`, `journals.sagepub.com`, `www.tandfonline.com`. This is the sandbox's egress policy (an allowlist), not the sites refusing us. I stopped at the first refusal for each host and did not route around it (no other proxy, no mirror of a blocked host through a reachable one). Per `read_documentation environment.network` the maker can widen "Allowed domains" in the cloud-environment settings; the hosts that mattered are in the unread list.
- **WebFetch was therefore used for the sources below, as the brief allows when curl is refused, and I say so here.** WebFetch returns a small model's answer to my prompt, not the page. I asked for short verbatim quotes each time. Every fact below is therefore **[stated via WebFetch]**: a source says it, per an extract I could not check against the raw page. Each such figure is one grade below a curl-read primary source; before it goes on the site it should be re-read raw.
- **Read first, as CLAUDE.md requires:** `CLAUDE.md`, `LAW.md` (still the unratified template), `the-law-for-agents.md`, `RULINGS.md`, `STATE.md`, `OPERATIONS.md` and `briefs/_COMMON.md`. There is no per-subagent brief file; my directive came in my prompt, and each of its rules came with its reason.
- **Computation:** Python with numpy only (no scipy). The scripts are in Appendix A. They define exactly what is counted, and a fresh reader can rerun them.
- **WebSearch** was used only to find URLs. Its result lists include mirrors and aggregators; I did not use those as sources unless I say so.
- Tags: **[stated via WebFetch]** (source and where), **[measured]** (I computed it; how shown), **[inferred]** (my reading). Nothing is from memory; where I know a source exists and did not read it, it is in the unread list and no formula from it is given.

Sections 1 to 9 take the nine systems in the order of the directive; section 10 is the summary, the disagreements among sources, and the unread list; Appendix A holds the code behind every [measured] number.

## 1. Plurality, three or more candidates

**What "decisive" means.** The voter changes who wins the single seat. With three or more candidates the vote is decisive only if, among the *other* voters, the leading candidates are tied or one vote apart. Which pair matters depends on the voter: it is a tie (or one-vote gap) for first place between two candidates, with the rest behind. Ties for lower places do not change the winner in plurality (they do in runoff systems, section 2). [inferred from Myatt & Fisher below]

**How the literature writes it.**
- Myatt & Fisher, "Everything Is Uncertain and Uncertainty Is Everything: Strategic Voting in Simple Plurality Elections", Oxford Dept of Economics Discussion Paper 115, July 2002, `https://ora.ox.ac.uk/objects/uuid:adeb8fa9-899c-4fbe-9594-5574db9c4d24/files/sv979v3563` (read by WebFetch). [stated via WebFetch]
  - Pivotal event: "She may only influence the identity of the winner in the context of a pivotal event" (Sec. 2.3, p. 7), concretely "a tie or near tie for the lead".
  - Outcome probability, Eq. 1 (as extracted): Pr[x] = integral of Pr[x|p] f(p) dp = (n!/prod x_j!) integral of prod p_j^{x_j} f(p) dp, where x_j is votes for candidate j, n the number of *other* voters, p the vector of true support, f(p) the voter's density (uncertainty) over p.
  - Proposition 1 (Sec. 2.2, p. 7): Pr[x] is approximately f(x/n) times 1/n^{m-1}, where m is the number of candidates.
  - Lemma 1 (Sec. 2.3, pp. 8-9, as extracted, possibly garbled): the two-way near-tie probability is of order 1/n; the three-way tie Pr[x1 = x2 = x3+1] is approximately (1/n^2) f(1/3,1/3,1/3). Quote: "the probability of a three-way tie vanishes at rate n^-2, whereas the probability of a two-way tie vanishes at rate n^-1" (Sec. 2.3, p. 9). Also: "three-way and near three-way ties are asymptotically irrelevant to voter i = 0" (p. 9).
  - The extractor flagged Table 1 and Eq. 4 as garbled; I do not reproduce them.
- Baltz, "The probability of casting a pivotal vote in an Instant Runoff Voting election", arXiv 2210.01657 (published Political Analysis 33(4):447-455, 2025, doi 10.1017/pan.2024.32), `https://arxiv.org/pdf/2210.01657` and `https://www.cambridge.org/core/journals/political-analysis/article/abs/probability-of-casting-a-pivotal-vote-in-an-instant-runoff-voting-election/AE30BADC8F23E0C7D7E5DBA9B501142B`. [stated via WebFetch] It uses, for single-member-district plurality (which it calls SMDP), "the Mebane et al. (2019) derivation" with Skellam-based pivot probabilities under Poisson voting games, and extends it to IRV. I did **not** read Mebane et al. (2019) itself (see unread list), so I give no formula from it.
- Gelman, Katz & Bafumi, "Standard Voting Power Indexes Do Not Work: An Empirical Analysis", British Journal of Political Science 34 (2004) 657-674, `https://sites.stat.columbia.edu/gelman/research/published/gelmankatzbafumi.pdf`. [stated via WebFetch; the extractor warned that radicals, pi and minus signs were lost] For two parties: Pr(decisive vote) is approximately p_{v_j}(0.5)/n_j (eq. 2 and Appendix eq. 3: Pr = E[Phi(v - 1/n) - Phi(v)]), where p_{v_j} is the density of the district's vote share v_j and n_j its number of voters. Under "random voting" (every voter 50-50) they give an approximation "of the form (2/sqrt(pi)) * (1/sqrt(n_j))" (as extracted; constants unverifiable). Sec. 2.3 forecast example: 10,000 voters, 52% forecast, 3% standard error gives decisiveness approximately 1.84/n_j (extractor could not verify the constant). Sec. 2.3 also cites the Good & Mayer / Chamberlain & Rothschild rule that decisiveness is proportional to 1/n_j when vote distributions are fixed. This is the two-candidate benchmark the other agents cover; I use it only as a comparator.

**Published estimates.**
- Baltz (arXiv version, simulation section; Fig. 1): 100 runs per setting, 3, 4 and 5 candidates, "a community of 1,000 voters" (caption). Power-law preferences ("half of the population holds one preference order, and the other half has a uniformly random preference order"): SMDP pivotal probabilities "about 10^-7", IRV "about 10^-6". Uniform preferences: IRV may be slightly higher for 3 candidates; for 4 or 5 "neither is clearly larger". No ratios printed. The paper itself calls these "out-of-equilibrium pivotal probabilities". [stated via WebFetch] **Caution** [inferred]: values this small, at N = 1,000, most likely arise because the stylised electorates have fixed preference structures that are far from a tie (in Myerson/Bouton's terms the pivot event is then exponentially unlikely), so they are not comparable with the 1/N-scale values below or with real elections. I did not see the paper's Fig. 1 data.
- I found no published estimate of single-vote decisiveness for a real multi-candidate plurality election in the sources I could read. (Mulligan & Hunter and Gelman et al. 1998 cover two-party US races and belong to the other agents.)

**Size relative to a two-candidate race of the same electorate.**
- Myatt & Fisher imply the same order, 1/n, for a two-way near-tie with a third candidate trailing, and 1/n^2 for a three-way tie. [stated via WebFetch, Lemma 1] Hence a third candidate does not change the order of magnitude for a voter choosing between the top two; it matters only for a voter whose candidate is within a vote or two of the lead (a close three-way race), and then by a smaller factor.
- **[measured]** exact calculation by me, script `plur.py`/`plur3.py` (kept in my scratchpad, not in the repository). Q_j = P(j wins if this voter votes for j) minus P(j wins if the voter abstains), ties broken uniformly among tied leaders; others' votes either multinomial with known shares ("knife-edge") or Dirichlet-multinomial with forecast shares mu and concentration kappa = 400 (so a candidate with 40% has share sd about 2.4 points). "N" = number of *other* voters.

| Case | N = 1,000 | N = 10,000 |
|---|---|---|
| 2 candidates, known shares (.5,.5) | Q = 0.01261 | Q = 0.003989 (= 1/sqrt(2 pi N) to 5 digits) |
| 3 candidates, known shares (1/3,1/3,1/3) | Q = 0.01549 (1.23x) | Q = 0.004890 (1.23x) |
| 3 candidates, known (.4,.4,.2) | Q1 = Q2 = 0.01410 (1.12x) | Q1 = Q2 = 0.004460 (1.12x) |
| 3 candidates, known (.45,.45,.10) | 0.01329 (1.05x) | 0.004205 (1.05x) |
| 2 candidates, forecast (.51,.49), kappa 400 | Q_A = 0.006363 (N*Q = 6.4) | Q_A = 0.000724 (N*Q = 7.2) |
| 3 candidates, forecast (.40,.38,.22) | Q1 = 0.00707, Q2 = 0.00712, Q3 = 3e-7 | Q1 = 0.000802, Q2 = 0.000803, Q3 = 1.6e-9 |
| 3 candidates, forecast (.36,.34,.30) | Q1 = 0.00801, Q2 = 0.00755, Q3 = 0.00250 | Q1 = 0.000895, Q2 = 0.000846, Q3 = 0.000207 |
| 3 candidates, forecast (.45,.45,.10) | Q1 = Q2 = 0.00710, Q3 about 0 | Q1 = Q2 = 0.000824 |

  Reading [inferred from the table]: with the same forecast uncertainty, the top-two candidates' Q is within about 1.05x to 1.26x of the two-candidate Q, and Q scales as 1/N (10x more voters gives about 10x smaller Q) when support is uncertain, but as 1/sqrt(N) when shares are known exactly. A candidate who is expected to finish far behind (Q3 about 1e-7 to 1e-9) has essentially no chance of being made the winner by one vote. The ratio is not a general constant: it depends on the forecast and its uncertainty; the table is illustrative of the structure only, not an estimate for any election. The known-shares rows show the effect of the "only top-two votes enter the margin" factor, 1/sqrt(p1+p2): for (.4,.4,.2) that is 1/sqrt(.8) = 1.118 [measured, matches].

## 2. Two-round runoffs

**What "decisive" means.** A voter has two votes in two different contests and can be decisive in either. Second round: she breaks or makes a tie between the two finalists. First round: she changes who reaches the second round, or whether a second round is held at all. Bouton lists the first-round events explicitly (below). The outcome she can change is thus "which candidate wins", but through a longer chain: first-round vote, then who is in the runoff, then who wins it.

**How the literature writes it.** Bouton, "A Theory of Strategic Voting in Runoff Elections", American Economic Review 103(4): 1248-88 (2013); the version read is the author's draft, first draft March 2006, revision February 2012, `https://economics.sas.upenn.edu/sites/default/files/filevault/event_papers/Runoff.pdf`. [stated via WebFetch; the extractor warned several formulas and Appendix A2 proofs were garbled or absent]
- Setup (Sec. 2): three candidates {A,B,C}, Poisson-distributed electorate with mean n, twelve voter types; round 1 actions {A,B,C,abstain}; if no candidate passes threshold theta a second round is held between the top two; ties by alphabetical order (results also hold with a fair coin).
- Second-round pivot event (Sec. 3.1): piv^2_PQ is the event that P "trails behind Q by exactly one vote"; a tie piv^2_QP also pivots because of the tie-break. Payoff: G_2(P|t) = Pr(piv^2_PQ) [U(P|t) - U(Q|t)].
- First-round pivot events (Sec. 3.1, Table 1), four kinds: (i) "threshold pivotal" i=ij: candidate i "lacks one vote (or less) to pass the threshold" with others below; (ii) threshold pivotal ij=i: a ballot against i keeps i below the threshold, forcing a runoff with j; (iii) above-threshold pivotal i=j: i and j both above the threshold and nearly tied; (iv) second-rank pivotal ki=kj: k is first and i, j tie for second place. First-round payoff G_1(i|t) (eq. 4) sums pivot probabilities times expected second-round utility differences.
- Sizes (Sec. 3 and App. A1): pivot events are compared by "magnitude", mag(E) = lim log Pr(E)/n. Lemma 2 (second round): "for a ballot to be pivotal, candidates have to receive (almost) the same number of votes" (App. intuition); the magnitude is a negative function of the candidates' expected vote shares and is zero only when they are equal (extracted formula garbled; constants not given). Illustrative magnitudes (Sec. 4.2, Tables 2-4): in Table 2 (theta = 0.5), mag(piv^1_CA=CB) = -0.0014 is the largest listed and threshold events are much smaller, e.g. mag(piv^1_B=BC) = -0.1227. These are per-voter exponents, not probabilities, and are for the paper's stylised type distributions.

**Published estimates of the probability.** None found. Bouton gives exponents (above), not a probability for any electorate size. [stated via WebFetch] I did not find an empirical estimate for a real two-round election.

**Real cases of a first-round vote changing who reached the runoff (data, not a probability).**
- France, first round 2002: Le Pen 4,804,713 votes (16.86%), Jospin 4,610,113 (16.18%); Le Pen went to the runoff, Jospin did not. Published by the Conseil constitutionnel (president Yves Guena) and reproduced by Maire-info, 25 April 2002, `https://maire-info.com/les-resultats-officiels-annonces-par-le-conseil-constitutionnel-article2-1774`. [stated via WebFetch, secondary reproduction of the official result] The gap is 194,600 votes [measured: 4,804,713 - 4,610,113]. I did not read the Conseil constitutionnel's own page (not tried; see unread).
- France, first round 2022: percentages Macron 27.84%, Le Pen 23.15%, Melenchon 21.95%, Zemmour 7.07%, from LCP's report of the Interior Ministry's definitive results, `https://lcp.fr/index%2ephp/actualites/premier-tour-decouvrez-les-resultats-definitifs-109262`. [stated via WebFetch] Gap Le Pen minus Melenchon = 1.20 points [measured: 23.15 - 21.95]. The page gave no vote counts for Le Pen; the vote gap is therefore not stated here. (`info.gouv.fr` returned a client error.)

**Monotonicity paradoxes exist in runoffs too (frequency, not per-ballot probability).** Lepelley, Chantreuil & Berg, "The likelihood of monotonicity paradoxes in run-off elections", Mathematical Social Sciences 31 (1996) 133-146, copy at `https://www.rangevoting.org/LepelleyBergRunoffMonoParadox.pdf` (third-party copy, read by WebFetch, not checked against the journal). [stated via WebFetch] Three candidates only ("limited to the three-alternative cases"), "impartial anonymous culture" (random preference profiles). For plurality run-off, in the limit of many voters (Cor. 1 and 3, Sec. 3.1): the proportion of profiles with the "more-is-less" paradox (M1) is 13/288 = 0.0451; the "less-is-more" paradox (M2) 17/864 = 0.0197; either 397/6912 = 0.0574. For anti-plurality run-off: 1/18 = 0.0556, 7/108 = 0.0648, 151/1296 = 0.1165. Finite electorates (Table 2, plurality run-off, M1): n = 24, 0.01152; n = 60, 0.02781; n = 120, 0.03568; n = 192, 0.03903. Abstract: "A monotonicity paradox occurs when a voting system reacts in a perverse way to a change in individual opinions." These are shares of random profiles in which *some* change of opinions would cause the paradox, not the chance that one ballot does; they show that the sign of a vote's effect in a two-round system is not always monotone, which matters for the "benefit" sign in the model. The text extractor flagged an OCR typo ("70.1165") in the anti-plurality global value. [inferred] for the sign remark.

**Size relative to a two-candidate plurality race of the same electorate.** Not quantified in any source I read. [inferred] (a) The second-round pivot probability is the two-candidate probability for the two finalists, so it equals the plurality case if the finalists' expected shares and uncertainty are those of a head-to-head. (b) The voter has additional first-round pivot chances (second-place tie, threshold). Each has its own probability and its own benefit (the benefit is the expected second-round difference, conditional on the runoff pairing), so the total is a sum of products, not a simple multiple of the plurality value. (c) The relative weights of the events depend on the forecast: Bouton's Tables 2-4 show that which first-round event dominates changes with the type distribution and threshold. No general ratio can be given from these sources.

## 3. Ranked-choice / instant-runoff voting (RCV, IRV)

**What "decisive" means.** The ballot changes the final winner, but it can do so in two ways, both defined in Baltz (2025). [stated via WebFetch]
- *Direct pivotality*: the ballot makes a candidate it ranks win, either by breaking a first-place tie ("one vote short of winning") or by creating one (with a fair tie-break, factor 1/2).
- *Indirect pivotality*: the ballot "can change the winner of the election without causing that specific candidate to win": ranking candidate c changes the drop (elimination) sequence from A to A', so the final winner changes though c does not win. "These are the only two ways to be pivotal, and they are mutually exclusive."
- Baltz: indirect pivotality is "closely related to some well-studied phenomena (especially IRV's failure of the monotonicity criterion, and also the no-show paradox), but it is not the same as either one."

**How the literature writes it.** Baltz, arXiv 2210.01657 / Political Analysis 33(4) (2025), links in section 1. Notation as extracted (typesetting garbled by the extractor, structure kept): kappa candidates, L ballot length, beta a ballot, S a drop sequence, A = [S_1,...,S_{kappa-1}, c] (c the candidate in question, last), y the index of c in A, A' an alternative drop sequence agreeing with A up to c's position, V_x the cumulative expected vote total of x given earlier drops.
- p = p_direct + p_indirect.
- p_direct(beta) = sum over i = 1..L, sum over drop sequences S of the other candidates consistent with the ballot, of [ product over rounds l = 1..kappa-2 and later-dropped candidates r of P(V_{A_l}^{(l)} < V_{A_r}^{(l)}) ] x [ (1/2) P(V_{A_{kappa-1}} = V_i) + (1/2) P(V_{A_{kappa-1}} = 1 + V_i) ].
- p_indirect(beta) = sum over i, sum over sequences A consistent with the ballot, of [ product over l = 2..kappa, h < l of P(v_{A_l} > v_{A_h}) ] x sum over A' in the set formed by prepending A_{1:y} to alternative tails G, of [ product over d, h < d of P(v_{G_d} > v_{G_h}) ] x [ (1/2) P(v_c^y = v_t^y) + (1/2) P(v_c^y = v_t^y - 1) ].
- Expected utility multiplies each by the payoff difference: u(i) - u(S_{-1}) for direct, u(A'_{-1}) - u(A_{-1}) for indirect pivotality.
- Modelling: Skellam-based probabilities under Poisson voting games following Mebane et al. (2019), with Assumptions 1 and 2 (independence of pairwise comparisons within and across rounds), "which it describes as simplifying"; the paper says the apparent faster decline in IRV as candidates increase "may be attributable to the varying quality of Assumption 2."
- The supplementary file of the published paper (`https://static.cambridge.org/content/id/urn%3Acambridge.org%3Aid%3Aarticle%3AS1047198724000329/resource/name/S1047198724000329sup001.pdf`) was listed by search but not read.

**Published estimates of the probability.** Baltz's simulations only (see section 1): 100 runs, 3-5 candidates, 1,000 voters; "IRV has very slightly higher pivotal probabilities than SMDP (averaging about 10^-6 compared to about 10^-7 with these particular preference structures)" for the power-law structure; for uniform support IRV "may be slightly higher ... when there are only 3 candidates, but when there are 4 or 5 candidates neither is clearly larger". Abstract: "These simulations produce similar estimated pivotal probabilities in the two systems." [stated via WebFetch] No estimate for a real election.

**How often monotonicity fails (frequency of the phenomenon, not the per-ballot probability).**
- Ornstein & Norman, "Frequency of monotonicity failure under Instant Runoff Voting: estimates based on a spatial model of elections", Public Choice 161 (2014) 1-9, `https://www.rangevoting.org/OrnsteinNormanMonotonicityIRV.pdf` (a copy on a third-party site, read by WebFetch; I did not check it against the journal). [stated via WebFetch] Definition (Sec. 1/3): upward failure is where "the IRV winner would lose if ranked higher by some subset of voters". Method (Sec. 4): 2-D spatial model, three adaptive candidates, 1,001 voters, four voter distributions, 5,000 elections each. Results (Sec. 5): failures occur in "anywhere from 0.7 % to 51 % of all cases", "between 15 % and 51 % of competitive elections (excluding ties, which account for approximately 1.1 % of simulated elections)"; abstract: "lower bound estimate of 15 % for competitive elections". The paper's "competitive" is a vote-count condition (c > (V+2)/4), not a margin. It contrasts Allard (1996), who estimated failure "only about once per century" for a UK general election. It reports no per-ballot frequency; its Burlington example moves 750 rankings.
- Graham-Squire & McCune, "An Examination of Ranked Choice Voting in the United States, 2004-2022", arXiv 2301.12075 (the version read is the arXiv text; I did not check which version), `https://arxiv.org/pdf/2301.12075`. [stated via WebFetch; the extractor flagged some internal inconsistencies in the paper's Table 7] Database of 182 elections for political office, all without an initial majority winner. Counts and rates as printed: upward monotonicity failure 3 of 182 (1.6%), downward 2 of 182 (1.1%), no-show 1 (0.5%), Condorcet failure 2 of 181 (1.1%), spoiler effect 3 (1.6%), compromise voting 7 (3.8%), "majoritarian failure" (winner without a majority of ballots cast, because of exhausted ballots) 95 of 182 (printed 52.5%, text count gives 52.2%). Abstract: "RCV's weaknesses are rarely observed in real-world elections". Named upward cases: Burlington VT mayor 2009 (the paper: "450 voters who voted only for Wright and 300 voters who ranked Wright first and Kiss second" in the example shift); Minneapolis Ward 2 council 2021; Alaska US House special 2022 (the extractor says the Alaska example in Sec. 2 is a hypothetical shift of 6,000 ballots); downward: San Francisco District 7 supervisors 2020 (Melgar 18,561 to Engardio 16,370; shift 800 ballots) and Minneapolis Ward 2.
- Ornstein & Norman on the case: Burlington 2009 final count 4,314 to 4,067, a margin of 247 votes. [stated via WebFetch]
- McCune & Graham-Squire, "Monotonicity anomalies in Scottish local government elections", Social Choice and Welfare 63 (2024) 69-101, `https://link.springer.com/article/10.1007/s00355-024-01522-5`. [stated via WebFetch, abstract page] "In 62 of the 1079 elections we found some kind of monotonicity anomaly" (30 single-winner, 1,049 multiwinner STV); the authors state their results are a lower bound. This is the largest empirical count I found; see also section 5.

**Size relative to a two-candidate plurality race of the same electorate.** [stated via WebFetch, Baltz] "similar" in simulations of 1,000 voters with 3-5 candidates; [inferred] IRV's total is p_direct + p_indirect, and indirect pivotality has no counterpart in plurality; in Baltz's stylised cases the totals come out similar, so the extra route does not change the order of magnitude there. The empirical frequency work (above) says non-monotonic outcomes are rare in real elections but not negligible in close three-way races (Ornstein & Norman, lower bound 15% of simulated competitive three-candidate elections have a monotonicity failure available to *some subset* of voters). The two are different quantities: Ornstein & Norman's 15% is about whether some group of voters could change the winner by ranking the winner higher, not the probability that *one* ballot does.

**Non-monotonicity and the sign of the benefit.** In a non-monotonic election a ballot that ranks the winner *higher* (upward) can make the winner lose. For the cost-benefit model this means that for a voter with a given preference, the sign of "benefit from my vote" is not guaranteed positive for every ballot she could cast; in the indirect-pivotality term, Baltz's expected-utility rule u(A'_{-1}) - u(A_{-1}) can be negative for a given ballot. [inferred] How often the sign is wrong for one ballot is not in any source I read.

## 4. Proportional representation (PR) and mixed systems

**What "decisive" means.** There is no single winner; a vote can change several different things, each with its own probability and its own benefit. From the sources:
1. *A seat moves between parties.* The vote changes how many seats a party gets by one: "one abstaining voter could change the allocation of seats between parties by voting" (Lyytikainen & Tukiainen, Sec. 4.2). The Luechinger-Schelker-Schmid "closeness" is "the minimal necessary movement along both margins to gain or lose a seat", holding "the votes of all other parties and candidates" fixed (Sec. 1, p. 102).
2. *A party crosses a threshold.* One vote decides whether a party gets any seats at all, which moves many seats at once (examples below). [inferred; the German and New Zealand rules are stated below]
3. *Who gets the party's seat* (open or flexible lists): "one voter could change which of the party's candidates gets the last seat of the party" (Lyytikainen & Tukiainen, Sec. 4.2); in Luechinger et al. this is the "candidate margin".
4. *In mixed systems,* two ballots: the constituency vote decides a plurality race (section 1 applies); the party vote sets the party's overall share. In Germany's current system a constituency winner whose party's second votes do not "cover" the seat is not seated: "those candidates with the lowest percentages of first votes are not assigned a seat" (BVerfG press release, 30 July 2024).
5. *Beyond the seat:* which coalition governs depends on the seat count. No source I read models that stage; it is the "chamber control" structure of section 8 plus coalition bargaining.

**Rules (as stated by the electoral authorities).**
- New Zealand (MMP): "The 120 highest numbers (which are called quotients) determine both the number of seats for each party"; the party vote is "divided by successive odd numbers starting with 1" (Sainte-Lague); a party needs "at least 5% of the total number of party votes" or an electorate seat; overhang: "the size of the Parliament is increased by that number of seats" (in 2014 Parliament had 121 seats). Source: Electoral Commission results site `https://www.electionresults.govt.nz/sainte_lague.html`. [stated via WebFetch] (The Electoral Commission's `elections.nz` page returned a bot-protection stub; not circumvented, listed as unread.)
- Germany: 2025 final result, 5% threshold; BSW 4.981%; the new Bundestag has 630 members; "7,425 higher than in the provisional result" (final count). Source: Bundeswahlleiterin press release 29/25, 14 March 2025, `https://bundeswahlleiterin.de/en/info/presse/mitteilungen/bundestagswahl-2025/29_25_endgueltiges-ergebnis.html`. [stated via WebFetch] The Federal Constitutional Court (30 July 2024, 2 BvF 1/23 and others) held the second-vote-coverage procedure compatible with the Basic Law (vote unanimous), held the 5% threshold "in its current form unconstitutional" (7:1) but left it in force until a new law, and left in force the rule that parties under 5% still take part if "their candidates win a majority of first votes in at least three constituencies". `https://bundesverfassungsgericht.de/SharedDocs/Pressemitteilungen/EN/2024/bvg24-064.html`. [stated via WebFetch]

**How the literature writes it.** Luechinger, Schelker & Schmid, "Measuring Closeness in Proportional Representation Systems", Political Analysis 32 (2024) 101-114 (online 24 July 2023), doi 10.1017/pan.2023.22, `https://core-prod.cambridgecore.org/core/services/aop-cambridge-core/content/view/C033EC7E886BAEEC6163A718D2D824A6/S1047198723000220a.pdf/measuring_closeness_in_proportional_representation_systems.pdf`. [stated via WebFetch; the extractor warned the formulas are partly garbled, so check against the PDF before use]
- Highest-average (D'Hondt), p. 104: party margin_{i,j} = votes_j - i x ( votes_{-j} / i~ )_{(n(J-1) - (n - i))}, where votes_j is party j's votes, votes_{-j} the other parties' votes, n seats, J parties, i the index of j's potential seat, i~ the index for other parties, and (.)_{(k)} the k-th order statistic of the D'Hondt ratios. In words: the vote change at which party j's i-th ratio equals the (n-i+1)-th highest ratio of the other parties, "so that the i-th seat is decided by a coin flip" (the extractor's paraphrase). Sainte-Lague, modified Sainte-Lague and Imperiali "only differ by the denominator used to calculate the ratios" (footnote 5).
- Largest remainder (Hare-Niemeyer), pp. 105-106: quota = (votes_j + sum of votes_{-j})/n; formulas garbled in extraction.
- Candidate margin (open lists), p. 106; overall vote margin = max over i of min{party margin, candidate margin}, p. 107.
- Worked example (hypothetical), D'Hondt, 3 seats, parties with 45, 35, 20 votes: P2's party margins are 15 (i=1), -10 (i=2), -100 (i=3).
- "In contrast to plurality systems, closeness in PR systems cannot be directly inferred from votes" (Abstract). The paper reports no real-election figure for how many votes would change a seat, and gives no pivotal *probability*; it supplies the *margin*, which is the input to one. Not treated: the Droop quota.

**Published estimates.**
- Lyytikainen & Tukiainen, "Are Voters Rational?", VATT Working Papers 50/2016 (Jan 2016 version; original Sept 2013), `https://www.doria.fi/bitstream/10024/148789/1/wp50.pdf`. [stated via WebFetch; the PDF text is scrambled in places] Finnish municipal elections (proportional open list, D'Hondt), 1,747 municipality-elections, five elections 1996-2012, municipal populations 234 to 44,804 (mean 7,506), council sizes 13 to 51 (mean 27), turnout mean 0.646. Method (Sec. 4.2): resample votes with replacement at the observed vote shares, same number of votes as cast, 1,000 repetitions; a pivotal event is where the draw is a tie "(in which case a lottery would determine who gets elected) and also when giving one more vote creates a draw or a different seat allocation directly". Results (Table 2, counterfactual): election-level pivotality (a vote-share-weighted average of within- and between-party measures, "the probability that a randomly drawn voter would be pivotal") mean 0.063, sd 0.031, min 0.006, max 0.193 (N = 1,746); party-election between-party pivotality mean 0.020 (sd 0.020, max 0.130; N = 10,171); within-party mean 0.006 (Table 2) or 0.028 (Table A1, candidate-election, N = 146,234; the paper says the gap "arise[s] mainly from the weighting"). They cite, in footnote 1, Mulligan & Hunter's "one out of 89,000 in U.S. Congressional elections" and Gelman et al.'s "at best one out of 1 million for close U.S. national elections". **Caution:** this is a bootstrap of the realised result (an ex-post closeness measure), not a forecast model, and the extractor could not read electorate sizes, tie-break details or the aggregation formula.
- Germany: a vote that was never "decisive" in the usual sense can still change the result. Press release 3 July 2008, 2 BvC 1/07, `https://www.bundesverfassungsgericht.de/SharedDocs/Pressemitteilungen/EN/2008/bvg08-068.html`: "if roughly 19,500 fewer second votes had been cast for the SPD, this party could as a result have claimed one more seat in the Deutscher Bundestag" (the "negative voting weight" effect); "it is also possible that not casting a voter's vote is beneficial to the party to be supported"; the court held the provisions "unconstitutional insofar as the effect of negative voting weight is facilitated thereby" and gave the legislature until 30 June 2011; there were 16 overhang mandates in the 16th Bundestag. [stated via WebFetch] The 2023 reform (second-vote coverage) was designed to remove overhang seats; I did not read a source on whether negative weight can still occur under it.
- Threshold example: BSW, Bundestag 2025. Final share 4.981% (Bundeswahlleiterin, above). In the provisional result BSW had 2,468,670 of 49,642,087 valid second votes and lacked "exakt 13.435 Zweitstimmen" (Stuttgarter Zeitung, from Bundeswahlleiterin data, `https://www.stuttgarter-zeitung.de/panorama/13000-stimmen-zu-wenig-fuer-das-bsw-78867876.html`); the final count added 4,277 valid second votes for BSW (t-online, `https://www.t-online.de/nachrichten/deutschland/id_100636312/bsw-auch-nach-endgueltigem-ergebnis-nicht-im-bundestag.html`). [stated via WebFetch] So the final shortfall was roughly 9,000 to 10,000 votes [inferred: 13,435 - 4,277 = 9,158, ignoring the small rise of the 5% line from the larger total; I did not read the final totals]. The 5% rule is the pivot: about 9,000 more votes (about 0.02 points) would have put a party of 2.5 million voters into the Bundestag.

**Size relative to a two-candidate plurality race of the same electorate.**
- **[measured]** by me (script `pr.py`, cross-checked against a brute-force D'Hondt simulation `pr_check.py`, agreement within Monte Carlo error: analytic 0.00626 / 0.01035 / 0.00862 vs brute force 0.00623 / 0.0112 / 0.00893 for three parties at N = 400, M = 5). Q_j = probability that one extra vote for party j adds a seat to j (ties by lot count 1/2), D'Hondt; party shares have Dirichlet uncertainty with concentration 400 (a 30% party has share sd about 2.3 points), votes Poisson. N = valid votes.

| Case | Q_j for the parties listed | M/N | Two-candidate plurality, same N, forecast .51/.49, same uncertainty |
|---|---|---|---|
| council-sized, M = 27, N = 4,000, shares .30/.25/.20/.15/.10 | 0.0052, 0.0056, 0.0059, 0.0062, 0.0067 | 0.0067 | Q_A = 0.00177 |
| district, M = 5, N = 50,000, shares .35/.30/.20/.10/.05 | 2.4e-5, 4.7e-5, 4.5e-6, 2.1e-5, about 0 | 1.0e-4 | Q_A = 1.47e-4 |
| district, M = 10, N = 100,000, same shares | 5.8e-5, 6.2e-5, 4.4e-5, 9.1e-5, 9.8e-6 | 1.0e-4 | Q_A = 7.3e-5 |
| national list, M = 150, N = 5,000,000, shares .30/.25/.20/.15/.10 | 2.1e-5, 2.4e-5, 2.5e-5, 2.6e-5, 2.7e-5 | 3.0e-5 | Q_A = 1.47e-6 (N x Q = 7.36 at N = 1,000,000, used here) |

  Reading [inferred from the table and the mechanism]: a party's seat count is a step function of its votes with one step per "votes per seat" (about N/M). When the uncertainty in the party's vote total spans several such steps (council and national cases), the chance that one vote sits exactly on a step is about (1/(N/M)) = M/N, within a factor 0.7 to 1.0 in the table, whatever the party's share. Then Q is about M times 0.7-1.0 over N, versus about 7 over N for the two-candidate race with the same forecast spread (Q_A x N = 7.0 to 7.4 in my plurality calculations), so a PR vote changes a seat about 3 times as often as the plurality vote changes the winner at M = 27, and about 14 to 18 times at M = 150. When the uncertainty is narrower than one step (the M = 5 and M = 10 districts), Q falls well below M/N for parties far from a step (4e-6 to 9e-5) and depends on closeness exactly as in plurality. **What the larger Q buys is one seat out of M, not the whole outcome**: the benefit per event is smaller by about 1/M of the chamber's seats (plus, for the seat that is the majority-maker, the chamber-control stage of section 8). The product of probability and benefit is therefore not obviously larger or smaller than in plurality; that comparison belongs to the benefit model, which no source here supplies.
- Lyytikainen & Tukiainen's party-election means (0.020 between-party; council M = 27 on average; roughly 4,000 voters in an average municipality if about 80% of residents are eligible [my assumption; the paper prints populations and turnout but not electorates] and turnout is 65%) sit in the same range as my council-sized row (about 0.005 to 0.007 per party), a factor of 3 to 4 higher; the difference could be the ex-post bootstrap, party sizes, or tie rules. Treat as order-of-magnitude agreement, not validation.
- Thresholds create a second, much larger-benefit pivot (many seats at once) with a probability of the same 1/N scale as a two-candidate race at the threshold: Pr(party's share within one vote of 5%) is about (density of the party's share at 5%) divided by N. [inferred from Gelman-type density formula; I did not find a published estimate.]

**Non-monotonicity in PR.** The German "negative voting weight" (above) is the documented real case I found in a PR-based system; the press release attributes it to second votes for parties that win overhang mandates in a Land (it "may arise in certain constellations"), and [inferred] it is therefore a property of the mixed system's overhang rules rather than of the divisor method. For the divisor and quota methods themselves (D'Hondt, Sainte-Lague, Hare-Niemeyer) I have no source in hand on monotonicity in the vote-to-seat step; **not asserted either way**.

## 5. Single transferable vote (STV)

**What "decisive" means.** STV elects M winners from ranked ballots. A ballot is decisive if adding or removing it changes *which set of M candidates is elected* (not just one name). It can do so directly (it completes a quota for a candidate it ranks) or indirectly through the order of eliminations and transfers, as in IRV (section 3), of which single-winner IRV is the M = 1 case ("a multiwinner version of IRV" is how Fox & Bruyns describe STV, Social Choice and Welfare 67 (2026) 143-166, `https://link.springer.com/10.1007/s00355-025-01638-2`; [stated via WebFetch] that paper analyses single-winner data only). [inferred] for the structure; I found no source that writes an explicit pivot-probability formula for multi-winner STV. Baltz's formulas (section 3) are for single-winner IRV; whether they extend to M > 1 is not shown in any source I read.

**Published frequencies of ballot-sensitivity anomalies (not per-ballot probabilities).**
- McCune & Graham-Squire, "Monotonicity anomalies in Scottish local government elections", Social Choice and Welfare 63 (2024) 69-101, `https://link.springer.com/article/10.1007/s00355-024-01522-5`. [stated via WebFetch, abstract page] 1,079 STV elections (30 single-winner, 1,049 multiwinner). Anomalies found: any kind, 62 elections; committee-size 9 (0.86% of multiwinner); upward 23 (2.1%); downward 17 (1.6%); no-show 39 (3.6%); "Most STV anomalies we find are the first of their kind to be documented in real-world multiwinner elections." The authors say their results are a lower bound and "similar to prior empirical research and much lower than most theoretical research"; the extractor noted the intro states "on the order of 1-4% for each type", which does not exactly match the 0.86% committee-size rate.
- Laird, Malmskog, Pixler & Rodbell, "Simulating Single Transferable Voting for the Colorado House of Representatives", arXiv 2607.25105v1 (27 Jul 2026), `https://arxiv.org/pdf/2607.25105`. [stated via WebFetch] Defines the anomaly as "decreased support for a candidate can improve their chances of getting elected"; says STV "does, in rare cases, violate the monotonicity criterion"; argues the algorithm's complexity "makes it unlikely for any one voter to take advantage of this anomaly" (a qualitative claim). It reports no pivotality or frequency number.
- Ordeshook & Zeng, "Some Properties of Hare Voting with Strategic Voters", Public Choice 78(1) (1994) 87-101 (Caltech working paper 772, 1991), `https://authors.library.caltech.edu/records/ev76a-f2977`. [stated via WebFetch, abstract page only] "strategic voting does not ensure the selection of Condorcet winning candidates". The page shows no pivot analysis; the PDF body was not read.

**Real case of a handful of votes deciding an STV seat.** Australian Electoral Commission v Johnston [2014] HCA 5, High Court of Australia, judgment summary 18 February 2014, `https://mta-sts.hcourt.gov.au/assets/publications/judgment-summaries/2014/hca5-2014-02-18.pdf`. [stated via WebFetch] "1,370 ballot papers had been lost between the earlier counts and the re-count"; before the re-count one of the two candidates for the last Western Australia Senate place was "14 votes ahead of the other at the determinative point"; the re-count result was "12 votes ahead at the determinative point". The summary gives no final order; it says a further hearing on 20 February 2014 would "determine the final disposition of the petitions". Not read: the judgment itself, the electorate size, and what happened next.

**Size relative to a two-candidate plurality race of the same electorate.** Nothing quantitative in the sources. [inferred] The decisive "determinative point" is a close contest for the last seat, in which a margin of a few votes in a large electorate is the same kind of event as a close two-candidate race. The 14-vote margin in the WA case is a data point for how small the margin can be, not a probability. I did not read a source stating the Droop quota formula, so none is given.

## 6. Referendums and ballot measures (including supermajority and quorum rules)

**What "decisive" means.** A referendum is a two-outcome contest (pass or fail), so with a simple-majority rule it is the two-candidate case of the other agents' work: a vote is decisive if the other votes are tied or one apart. Three rules change *where* the knife-edge sits:
- *Supermajority* (pass needs a share q above 50%): the vote is decisive where the others' Yes share is just below (or at) q, not at 50%. [inferred from the Gelman-type formula p(threshold)/N; see [measured] below]
- *Participation quorum* (turnout must exceed a threshold): Italian Constitution, Art. 75: a referendum is valid only if "the majority of those with voting rights have voted" and passes if "a majority of votes validly cast has been reached" (English excerpt at `https://legislationline.org/taxonomy/term/12983`). [stated via WebFetch] A voter can then be pivotal for the quorum, not only the majority.
- *Approval quorum* (Yes must be a share of all eligible voters): not read in any source other than as a lab treatment (below).

**How the literature writes it.**
- Aguiar-Conraria, Magalhaes & Vanberg, "Experimental evidence that quorum rules discourage turnout and promote election boycotts", NIPE WP 14/2013, `https://core.ac.uk/download/55624987.pdf`. [stated via WebFetch; Table 1 and Table 4 garbled] Lab model: 9 electors, binary choice, majority rule, voting costs c_i uniform on [0,c]. Quote (Sec. 2): "a supporter of Change is pivotal if her vote is necessary either to reach the majority of the votes or to meet the quorum." For Opponents the pivotal event "has two conflicting forms": "She may be pivotal, in a desirable way, if her vote is necessary to reach majority for the Status Quo, but she may pivotal too to meet the quorum", and "Under participation quora, Opponents may actually hurt themselves by voting." Appendix 1 gives the cut-off conditions with rho(v_o, v_s) the probability a voter attaches to the others' counts (v_o No, v_s Yes), b the supporters' benefit, x the opponents' benefit, gamma_s and gamma_o the cut-off costs: Supporter, participation quorum: [ sum_{v=2..4} rho(v,v)/2 + sum_{v=1..3} rho(v+1,v)/2 + rho(1,2) + rho(0,3) ] b = gamma_s; Opponent: [ sum_{v=2..4} rho(v,v)/2 + sum_{v=2..3} rho(v+1,v)/2 - rho(1,2)/2 - rho(0,3) ] x = gamma_o. The negative terms are the self-harming pivotal case. These are for the experiment's quorum design, with 9 electors, not for real referendums. Turnout in the lab: 53.8% (+-4.0, 95% CI) with no quorum, 39.9% (+-4.1) with a participation quorum, 47.0% (+-4.5) with an approval quorum (Sec. 4.1).
- Herrera & Mattozzi, "Quorum and Turnout in Referenda", working paper (versions 2005-06), `https://igier.unibocconi.eu/sites/default/files/media/attach/HerreraPAPER.pdf`. [stated via WebFetch] Models party mobilisation, not the individual pivotal voter ("The paper does not use the classic 'pivotal voter' concept"); decisive event with a quorum: P = Pr(vR >= vS and vR + vS >= q). Cites an Italian referendum where "the status quo party got only 12% of the votes but the total turnout was only 26%" (Sec. 1, p. 2; year not read).
- Foellmi, Heim & Schmid, "Voter Turnout and Selective Abstention in Concurrent Votes", online appendix, 16 June 2025, `https://static.cambridge.org/content/id/urn%3Acambridge.org%3Aid%3Aarticle%3AS2049847025100332/resource/name/S2049847025100332sup001.pdf`. [stated via WebFetch] Swiss concurrent referendums; "it is challenging to directly estimate this parameter [the probability of being decisive] because we cannot observe how individuals perceive the closeness of the referendums in advance"; they use ex-post distance of the Yes share from 50% as a proxy (coefficient on distance -0.020 (SE 0.008) without, -0.021 (SE 0.009) with voting-day fixed effects, 228 observations). No estimate of p itself.
- Two further candidate sources were not readable: a docx appendix, "The mathematics of the pivotal voter model with quorum requirements" (Cambridge, `...S1386415716010267sup001.docx`, binary file the extractor could not open) and Hizen & Shinmyo, "Imposing a turnout threshold in referendums", Public Choice 148(3) (2011) 491-503 (abstract not shown). I could not obtain the "pivotal voter model" formulas for quorum from either.

**Published estimates.** None found for the probability of a decisive vote in a real referendum or under a real supermajority or quorum rule. I did not read Mulligan & Hunter's paper itself, so I do not know whether it covers ballot measures.

**Real data point: the 2016 UK EU referendum.** Leave 17,410,742 (51.89%), Remain 16,141,241 (48.11%), turnout 33,551,983 (72.15%), electorate 46,500,001 (electionpolling.co.uk, `https://www.electionpolling.co.uk/results/2016eu`; the page does not name its original source; I could not read the Electoral Commission page, which returned a client error). [stated via WebFetch] Margin 1,269,501 votes [measured: 17,410,742 - 16,141,241], 3.78% of the votes cast [measured: 1,269,501 / 33,551,983 = 0.03784].

**[measured]** decisiveness of a single ballot under a pass threshold q on Yes/(Yes + No), N about 10,000 other voters, Beta-binomial uncertainty with concentration 400 (share sd about 2.5 points at 50%), averaged over N = 10,000 to 10,029 to avoid lattice artefacts (a threshold of 0.6 with exactly 10,000 voters gives zero for a Yes ballot only because 6,000/10,000 is already a pass; I removed that artefact by averaging). Q_yes = P(pass | I vote Yes) - P(pass | I abstain); Q_no = P(pass | I abstain) - P(pass | I vote No). Script `ref.py`/`ref2.py`.

| Forecast Yes share | majority (q = .5): Q_yes / Q_no | q = .6: Q_yes / Q_no | q = 2/3: Q_yes / Q_no |
|---|---|---|---|
| .500 | 7.8e-4 / 7.8e-4 | 2.6e-7 / 3.8e-7 | 9e-14 / 1.8e-13 |
| .550 | 1.1e-4 / 1.1e-4 | 9.0e-5 / 1.3e-4 | 7.8e-9 / 1.5e-8 |
| .600 | 3.3e-7 / 3.3e-7 | 6.4e-4 / 9.6e-4 | 1.4e-5 / 2.7e-5 |
| .667 | 2.3e-13 / 2.3e-13 | 1.5e-5 / 2.3e-5 | 5.5e-4 / 1.1e-3 |

  Reading [inferred from the table]: (a) a supermajority rule moves the knife-edge: the ballot is only about as decisive as in a majority race when the forecast Yes share is within a point or two of q (6.4e-4 at forecast = q = .6 vs 7.8e-4 at forecast = q = .5), and falls by orders of magnitude when the forecast is several forecast-sds from q (a 50% forecast with q = .6 gives 2.6e-7, a 55% forecast with q = .6 gives about 1e-4, against 1.1e-4 for a 55% forecast under simple majority). (b) The No ballot is more decisive than the Yes ballot under a supermajority in these rows (9.6e-4 vs 6.4e-4 at q = .6, forecast .6; 1.1e-3 vs 5.5e-4 at q = 2/3, forecast .667). [inferred] The ratio matches t/(1-t): a Yes ballot changes the pass condition Y >= t(Y+X) over a window of (1-t) votes and a No ballot over a window of t votes, since a Yes adds to both numerator and denominator and a No only to the denominator; 0.6/0.4 = 1.5 and (2/3)/(1/3) = 2.0, as in the table. (c) For the simple majority row the size is the two-candidate plurality case by construction; N x Q is about 7.8 at N = 10,000 here and 7.2 at N = 10,000 for a .51 forecast in section 1, so the "same electorate" comparison is a matter of distance from the threshold, not of the number of options. (d) At the national scale (N about 3.4e7 for the 2016 UK referendum) the same forecast spread would put Q at roughly 7 to 8 divided by N, about 2e-7, if the forecast were centred on 50%; a forecast centred where the result fell (Leave 51.89%, 1.89 points from 50%) with an sd of 2.5 points would lower it by a factor exp(-0.76^2/2) = 0.75 [arithmetic]. [inferred from N x Q scaling, which I checked in section 1 for N = 1,000 to 100,000 only; not recomputed at 3.4e7]

**Size relative to a two-candidate plurality race.** Same order when the forecast is at the threshold (the majority row above); for a supermajority the comparison depends on how far the forecast is from q (the table); a quorum adds a second pivot event whose probability depends on the turnout forecast (not computed; no readable formula). [measured / inferred as marked]

## 7. Primaries and multi-stage nominations

**What "decisive" means.** In a primary the vote can change *who the party's nominee is*; the nominee then (second stage) faces the general election, so the vote matters for the final outcome only through "the nominee changes the general-election winner". With sequential state primaries (US presidential), a third stage exists: early results change later ones, so a single vote can matter through delegate counts and through changes in the field. [inferred; no source I read gives a formula for primaries]

**Chain.** [inferred] The two-stage decomposition printed for the Electoral College by Gelman, King & Boscardin (1998), eq. 1, is "Pr(your vote matters) = Pr(your vote is decisive in your state) x Pr(your state is decisive | your vote is decisive in your state)" (`https://core.ac.uk/download/28933611.pdf`; [stated via WebFetch]; the extractor's formula for the first factor, approximately f_{v_i}(.5)/n_i, is a reconstruction). For a primary, by analogy: P(my vote makes or breaks a tie between the two leading contenders) x [P(the party's candidate wins the general | nominee A) - P(... | nominee B)] x (value of the general-election outcome). The bracket is the "electability difference" of the two contenders; I found no published estimate of it and none is asserted. In a many-candidate primary, the first factor is the plurality-with-three-or-more case (section 1), or a runoff or ranked-ballot case if the state uses one.

**Published material read (none gives a pivot probability for primaries).**
- Cooper & Munger, "The (Un)Predictability of Primaries with Many Candidates: Simulation Evidence", Public Choice 103(3-4) (2000) 337-355, `https://ideas.repec.org/a/kap/pubcho/v103y2000i3-4p337-55.html`. [stated via WebFetch, abstract page] Simulation of 10,000 voters, ten random candidates per party's closed primary; outcomes "varied widely, by as much as two standard deviations from the median partisan voter"; "the way we choose candidates may amount to a lottery". It does not study pivotal voting.
- Ballotpedia, "A look back at 2025 state primary election competitiveness", `https://news.ballotpedia.org/2025/07/02/a-look-back-at-2025-state-primary-election-competitiveness/`. [stated via WebFetch] State legislative and executive primaries in New Jersey, Virginia and Wisconsin in 2025: "51 primaries out of a possible 289 for the 185 total seats", i.e. contested primaries 17.6% (2011-2023 average 19.7%); incumbents contested 22.4%; open seats 5.9%. **No margin-of-victory or close-race statistics** in the article. The data show only that in most primaries there is no contest at all, so the decisive-vote probability is zero for the majority of seats; they say nothing about how close contested ones are.
- Not found: a published estimate of the probability a vote is decisive in a primary, or a source on the vote's decisiveness through sequential effects. I did not read any dataset of primary margins.

**Size relative to a two-candidate plurality race of the same electorate.** Not available from sources. [inferred] Three structural differences: (a) many seats have no contested primary (above); (b) the electorate is smaller, which raises the tie probability for a given spread (section 9); (c) the benefit term is the electability difference times the general-election benefit, which is a fraction of the general-election benefit by construction, so even a larger first-stage probability multiplies a smaller second-stage difference. The relative size therefore turns on three quantities no source here provides.

## 8. Chamber control (a seat, then the majority)

**What "decisive" means.** Two stages in sequence, as for the Electoral College. Stage one: the vote makes the seat's result (a tie in the district). Stage two: the seat is the one that gives a party the majority. The vote changes who controls the chamber only if both hold. FiveThirtyEight's definition of the second stage for the US House: "The 218th seat is the tipping-point seat because it is the House's median seat by partisanship" (`https://fivethirtyeight.com/features/house-tipping-point-districts/`, 2022 forecast as of Oct. 14, 40,000 simulations; "Republicans have a 70-in-100 chance of taking control of the House"; their tipping-probability column is in a CSV I did not open). [stated via WebFetch]

**How the literature writes it.**
- Gelman, King & Boscardin (1998), `https://core.ac.uk/download/28933611.pdf`, [stated via WebFetch; formula reconstruction flagged]: Pr(your vote matters) = Pr(decisive in your state) x Pr(your state is decisive | your vote is decisive in your state). The first factor for even n_i is approximately f_{v_i}(.5)/n_i (f the forecast density of the vote share); the second is a conditional forecast of the other states' electoral votes: Pr(E_{P_i} in (.5 e_total - e_i, .5 e_total) | v_i = .5), with a factor 1/2 because a vote that ties the national election is half as decisive.
- Gelman, Katz & Bafumi (2004), section 1 above: the same two-factor decomposition (Sec. 2.2); the second factor is, per the extract, roughly proportional to e_j (each jurisdiction's weight) for a body of weighted jurisdictions, and the linear approximation "has a relative error of less than 10 per cent for all states" (Sec. 2.2.1). Banzhaf index: probability a vote is decisive when everyone votes 50-50 (Sec. 2.1). Their empirical result (Sec. 4, Fig. 3; US state lower houses and senates, US House, US Senate, European national elections): the spread of the vote share falls with the number of voters far more slowly than random voting predicts (fitted exponents "all closer to 0 than to" the random-voting value, which is -0.5), so the decisive-vote probability is roughly proportional to 1/n (fits near n^-0.9; the minus signs were lost in extraction and I read the sign from the abstract's "approximately proportional to 1/n") rather than to n^-0.5; random voting "overestimates the probability of close elections in larger jurisdictions". [stated via WebFetch]
- Gelman, Katz & Tuerlinckx (2002), "The Mathematics and Statistics of Voting Power", Statistical Science 17(4), Caltech working paper 1141, `https://authors.library.caltech.edu/records/hpnm8-cmw66`. [stated via WebFetch, abstract page] "voting power ... is the probability that a single vote is decisive"; discusses two-stage elections; I did not read the body.
- For a chamber (not the EC): I found no source writing the second-stage probability for a legislature in a closed form. The seats-to-majority stage is, by its definition, Pr(the other seats give the party exactly 217 of 435, so this seat is the 218th). [inferred]

**Published estimates.** None found for chamber control. Gelman, King & Boscardin (Sec. 6.1) give Electoral College (not chamber) numbers: about 1 in 10 million for a close national election such as 1992, 1 in 3.5 million in Vermont, as high as about 1 in 1.5 million for some small states in close elections, "on the order of 1 in hundreds of millions" in landslides, and "1 in 10,000" as an upper bound for a typical 200,000-voter congressional race, with an empirical House frequency of about .5/20,597 per election. [stated via WebFetch] Those belong to the other agents; they are the seat-level (stage one) values.

**[measured, stylised]** my own calculation of the stage-two factor for a 435-seat chamber (script `chamber.py`, mean of three random draws of the baseline margins). The other 434 seats have baseline Democratic margins drawn from a normal distribution with sd 14 points, each seat has an idiosyncratic election-day sd of 3 points, and a common national swing with sd sigma. P(tip | tied) = P(the other seats give the party exactly 217) so that this seat's winner has the majority.

| national swing sd | expected seats for D in the other 434 | sd of that seat count | P(tip given this seat tied) |
|---|---|---|---|
| 1 point | 209 | 12.9 | 0.0257 (1 in 39) |
| 1 point | 245 | 12.7 | 0.0029 (1 in 341) |
| 2 points | 209 | 24.4 | 0.0155 (1 in 64) |
| 2 points | 245 | 24.0 | 0.0084 (1 in 118) |
| 2 points | 279 | 23.0 | 0.0005 (1 in 1,884) |
| 3 points | 209 | 35.9 | 0.0108 (1 in 93) |
| 3 points | 244 | 35.4 | 0.0082 (1 in 123) |
| 3 points | 279 | 33.8 | 0.0023 (1 in 431) |
(A row with the party expected to win 280 of 434 and swing sd 1 point gives about 1e-8, omitted from the table; the 209 rows are near a toss-up chamber, since 217 would be exact.)

  Reading [inferred from the table]: when the chamber is close to a toss-up and national uncertainty is a couple of points, the second stage is a factor of about 1% to 2.5% (1 in 40 to 1 in 100), so the chance that one vote decides control is about 1/40 to 1/100 of the chance it decides the seat. When the party is expected to win about 28 seats above the majority line the factor is 0.3% to 0.8% (the 245 rows), and about 60 seats above it is 0.05% to 0.2% (the 279 rows). Together with the seat-level probability this is a product of two small numbers; relative to a two-candidate race of the same *electorate*, the chamber-control probability is smaller by this factor, and the benefit (control) is larger. The stylised parameters are mine, not a forecast.

**Size relative to a two-candidate plurality race of the same electorate.** Smaller by the stage-two factor (about 0.01 to 0.03 for a near-toss-up chamber in the table above), in exchange for a benefit that is the whole chamber's difference in control rather than one seat. Whether the product exceeds the single-seat product depends on how the benefit scales, which no source here addresses. [measured table, inferred reading]

## 9. Very small electorates (local offices, school boards, special districts, workplace votes)

**What "decisive" means.** The same as in the plurality or binary cases above, with N small enough that the exact count (not an approximation) matters and that ties are not rare. Ties are decided by lot or by a rule; Farber notes that in union certification "unions lose ties" and in decertification "the union wins ties" (footnotes 5 and 9), so the tie rule decides whose vote a tie-making ballot helps.

**How the literature writes it.**
- Farber, "Rational Choice and Voter Turnout: Evidence from Union Representation Elections", NBER WP 16160 (July 2010), `https://www.nber.org/system/files/working_papers/w16160/w16160.pdf` (abstract page `https://www.nber.org/papers/w16160`). [stated via WebFetch] Multinomial model: for a pro-union worker, Delta W+ = Pr(n_p = n_c) (eq. 12, as a sum over i = 0 to INT(n/2) of terms weighted by p_p^i, p_c^i, p_a^(n-2i)); for an anti-union worker Delta W- = Pr(n_p = n_c + 1) (eq. 13); n = N - 1 other eligible voters; p_p = mu G(b Delta W+), p_c = (1 - mu) G(b Delta W-), p_a = 1 - p_v; mu the expected pro-union fraction, G the cost distribution. (The extractor warned the OCR of the summation limits is garbled.) Data: 75,300 on-site elections 1972-2009, 2,014,616 eligible voters in total (Table 1 note); "38 percent have 10 or fewer, 62 percent have 20 or fewer, and 74 percent have 30 or fewer eligible voters"; the paper prints both "averaging 50 to 75 eligible voters" (Sec. 1.2) and "from 24 to 30 between 1972 and 2008" (Sec. 6.2) without reconciling them. Abstract: "most individuals (over 80 percent) vote in these elections independent of consideration" of whether they will be pivotal, and many elections "have sufficiently few eligible voters" that a single vote can have a substantial chance of being decisive; for the rest, turnout rises with the chance of being pivotal (smaller electorates, closer expected elections). It does not print the pivotal probabilities themselves.
- Lyytikainen & Tukiainen (section 4 above): Finnish municipalities as small as 234 residents; election-level mean pivotality 0.063, min 0.006, max 0.193.
- Gelman, Katz & Bafumi (section 1 above): the 1/sqrt(n) vs 1/n distinction and the Good-Mayer / Chamberlain-Rothschild rule.

**Real data on how often small races are decided by a handful of votes.** Ballotpedia, "Races decided by 10 votes or fewer", `https://ballotpedia.org/Races_decided_by_10_votes_or_fewer`, [stated via WebFetch; the extractor's reading may be incomplete]: 2018-2026, "out of 150,010 elections in Ballotpedia's coverage scope", 734 elections were decided by 10 or fewer votes, 496 by fewer than five votes, 104 by a single vote; most visible rows are local or school-board races; smallest total vote count 13 (a 2024 Constitution Party primary in South Carolina's 4th district, 8 to 5); largest visible total 23,525 (a 2022 Massachusetts House race). The page prints the share as "0.004%"; 734 / 150,010 is 0.49% [measured], so one of the two figures on the page is misprinted or means something else; the page also says "the 660 elections" in one place. The page does not define its coverage scope or its method of finding races, so these counts are lower bounds on an unknown base.

**[measured]** exact decisiveness for small N (script `ref.py`; binary contest, simple majority, ties by fair coin; Q = P(win | my Yes vote) - P(win | I abstain)). N = number of *other* voters.

| N others | known 50-50 shares (binomial) | 1/sqrt(2 pi N) | uncertain share (Beta-binomial, concentration 20, i.e. share sd about 11 points), forecast .5 | same, forecast .6 |
|---|---|---|---|---|
| 9 | 0.1230 | 0.1330 | 0.1036 | 0.0783 |
| 19 | 0.0881 | 0.0915 | 0.0635 | 0.0462 |
| 29 | 0.0722 | 0.0741 | 0.0463 | 0.0329 |
| 99 | 0.0398 | 0.0401 | 0.0162 | 0.0110 |
| 999 | 0.0126 | 0.0126 | 0.0017 | 0.0011 |
| 9,999 | 0.0040 | 0.0040 | (not computed) | (not computed) |

  Reading [inferred from the table]: for a 10-voter workplace vote one ballot raises the winning probability of the side it supports by about 10% to 12% (Q, relative to abstaining; voting the other way instead of abstaining roughly doubles the swing) when preferences are a coin flip; this falls to about 4% at 100 voters and 1.3% at 1,000 (known shares). The 1/sqrt(2 pi N) approximation is about 8% too high at N = 9 and within 1% from N = 99. With realistic uncertainty about the split (the right-hand columns), the probability falls roughly like 1/N rather than 1/sqrt(N): from 0.0162 at N = 99 to 0.0017 at N = 999 is a factor of 9.5 for 10x the voters. A small electorate matters only if the race is also close in expectation; at N = 999 a forecast of .6 versus .5 lowers Q by about 35% under this wide uncertainty, and far more under narrower uncertainty (compare section 6's table at N = 10,000). The Q for known shares is the upper envelope.

**Size relative to a two-candidate plurality race of the same electorate.** Same formula, different N; the numbers above are the plurality case at small N. For a given close forecast the scaling is about 1/N, so a school-board seat decided by 5,000 voters has a probability about 2,000 times that of a national election of 10 million at the same forecast spread [inferred from the scaling; 10,000,000/5,000 = 2,000], and a 10-voter workplace vote about 500 times higher again, about a million times the national figure [inferred; 10,000,000 / 10 = 10^6]. Real small races also have less well-defined forecasts (smaller polls, if any), which widens the spread and lowers the effective Q (the right-hand columns).

## 10. Summary, what each system asks of the model, disagreements, unread

### 10.1 Summary (one paragraph)

In every system I looked at, "one vote changes the outcome" is the same event: the other voters leave the result within one vote of a boundary at which the outcome flips, and the voter's ballot is the one that moves it across (a tie counts half). What differs is what flips and how many boundaries there are. With three or more candidates in plurality the relevant boundary is still the tie for first, of the same 1/N order as in a two-candidate race: my exact calculations give a top-two voter 1.05 to 1.26 times the two-candidate value, and a voter for a candidate far behind essentially zero, while three-way ties are of order 1/N^2 (Myatt & Fisher). Two-round, ranked-choice and single-transferable-vote systems add boundaries (second place, thresholds, elimination order), so there are more ways to be decisive, including "indirect pivotality" in IRV (Baltz 2025) and real non-monotonic outcomes, where ranking a candidate higher can make them lose (1.6% of 182 US elections in the empirical count; 62 of 1,079 Scottish STV elections; 15% or more of simulated competitive three-candidate IRV elections), so the sign of a ballot's effect is not always the intuitive one. In list proportional representation the vote can change a seat, a threshold or a candidate's place, and when forecast uncertainty spans several seats the chance a vote adds a seat to a party is about M/N, three to eighteen times the plurality figure in my cases, but each such event moves one seat of M, not the whole outcome. Referendums are the two-candidate case with the threshold q in place of 50%: a supermajority rule shifts the knife-edge to q, and a turnout quorum creates a second pivot event in which, in the only model I read, voting can harm a voter's own side. Chamber control multiplies a seat-level probability by a stage-two factor that I compute at about 1% to 2.5% for a near-toss-up 435-seat chamber and far less if lopsided. Very small electorates raise the probability sharply (10% to 12% at 9 other voters with a coin-flip split, falling like 1/N once the split is uncertain), and the real-data counts of races decided by a handful of votes are consistent with that. I found no published single-vote pivot probability for a real election outside the two-party cases the other agents cover, except the Finnish municipal bootstrap; every other probability in this report is either a model's exponent or order of magnitude, or a number I computed under stated assumptions.

### 10.2 What each system asks of the model (candidates, not choices)

| System | Quantities the probability depends on, per the sources | Evidence grade |
|---|---|---|
| Plurality, 3+ candidates | N; forecast shares of the top two; forecast uncertainty; which pair the voter's preference is between; tie rule | formula in Myatt & Fisher (Prop. 1, Lemma 1); my exact table |
| Two-round | the above for round 2; for round 1: thresholds (theta), second-place gap, probability of a runoff | event list in Bouton; no estimate |
| IRV/RCV | full distribution of ranked ballots (not just first choices); drop sequences; ballot length | formulas in Baltz; simulation only |
| PR / mixed | N, seats M, divisor or quota method, party shares and their uncertainty, threshold rule, list type (open or closed), overhang rules | margin formulas in Luechinger et al.; Finnish estimate; my M/N table |
| STV | as IRV plus M and the quota rule | frequencies only; no pivot formula |
| Referendum | Yes-share forecast and its spread, the pass threshold q, turnout forecast and quorum | my table; quorum only as a lab model |
| Primary | contest exists or not; field size and rule; electability difference; sequential effects | no source |
| Chamber control | seat-level probability; distribution of the other seats; national swing | decomposition in Gelman et al.; my stylised table |
| Small electorate | exact N (not an approximation); tie rule; split forecast | Farber formulas; my exact table |

### 10.3 Open questions where sources disagree or are internally inconsistent

1. **Size of the tie constant.** Gelman, Katz & Bafumi (extract) give the random-voting probability as "of the form (2/sqrt(pi)) * (1/sqrt(n_j))"; my exact calculation gives, for a 50-50 binary race, P(win | I vote) - P(win | I abstain) = 1/sqrt(2 pi N) to five digits at N = 10,000 and, for a vote for one side versus the other, twice that, sqrt(2/(pi N)); the extract's form is 2/sqrt(pi) = 1.128 divided by sqrt(n), mine is 0.399 divided by sqrt(N) for Q and 0.798 divided by sqrt(N) for the full swing, so the extract is 1.41 times my swing and 2.83 times my Q. The difference could be a convention (versus abstaining or versus voting the other way; n counting the voter or not) or an extraction error. Unresolved from the extract alone; check the raw PDF before the constant is used.
2. **How often non-monotonicity matters.** Ornstein & Norman: 15% to 51% of simulated competitive three-candidate IRV elections have an upward failure available to some group of voters; Graham-Squire & McCune: 1.6% of 182 real US elections; McCune & Graham-Squire: about 1-4% per type of anomaly in Scottish STV. The measures differ (simulated competitive subset versus all real elections, any subset of voters versus observed profiles), so they are not in conflict, but no source puts them on one scale, and none gives the per-ballot probability.
3. **Graham-Squire & McCune internal inconsistencies** (extractor): Table 7 prints 52.5% for majoritarian failure but 95 of 182 is 52.2%; the text says six compromise-voting elections but lists seven; the Alaska upward-monotonicity example is a hypothetical shift. Which version of the paper was read is not known (arXiv text).
4. **Baltz's simulated probabilities** (about 1e-7 for plurality and 1e-6 for IRV at 1,000 voters) versus the 1/N-scale values in this report (about 0.006 to 0.016 at N = 1,000, depending on whether shares are uncertain or known): reconciling them needs the paper's Fig. 1 data and its Assumptions 1 and 2, which I did not see. Treat the Baltz values as comparisons between the two systems on one stylised electorate, not as levels.
5. **Lyytikainen & Tukiainen** (extractor): within-party pivotality is 0.006 in Table 2 but 0.028 in Table A1; the minimum municipal population is 234 in Table 3 but the text says the smallest mainland municipality has "roughly 800 inhabitants"; the PDF text is scrambled in places. The election-level mean 0.063 is also a weighted average that mixes party-level and candidate-level events.
6. **Ballotpedia, races decided by 10 votes or fewer**: prints "0.004%" as the share of 150,010 elections, but 734 / 150,010 = 0.49%; the page also says "the 660 elections" and "734" without reconciling them.
7. **Farber**: average election size "50 to 75 eligible voters" (Sec. 1.2) versus "from 24 to 30" (Sec. 6.2).
8. **Aguiar-Conraria, Magalhaes & Vanberg**: boycott effect of a participation quorum "more than 40 percentage points" in the Introduction versus "57 to 70" in Sec. 4.3 and 5.
9. **McCune & Graham-Squire (Scottish STV)**: "on the order of 1-4% for each type" in the introduction versus a committee-size rate of 0.86%.
10. **BSW shortfall**: 13,435 votes in the provisional count (Stuttgarter Zeitung) and 4,277 more votes in the final count (t-online); I could not read the final totals, so the final shortfall (about 9,000 to 10,000) is my subtraction, not a stated figure. The English Bundeswahlleiterin release prints 4.981%, the Stuttgarter Zeitung 4.97293758% (provisional); the two are not the same count.
11. **Brexit referendum counts** come from a secondary site that does not name its source; the Electoral Commission page was not readable.
12. **What I did not find:** a published estimate of the probability of a decisive vote for (i) a real multi-candidate plurality election, (ii) a real runoff, (iii) a real PR election other than the Finnish bootstrap, (iv) STV, (v) a real referendum, supermajority or quorum, (vi) a primary, (vii) chamber control, (viii) a small local election. Gaps (vi) and (vii) are the largest.

### 10.4 Unread list (sources named in this report or in search results that I did not read, with the reason)

*Hosts refused by the sandbox's egress policy for curl (HTTP 403 on CONNECT; not circumvented). Note that WebFetch did reach some of these hosts (for example `www.cambridge.org`, `arxiv.org`, `www.nber.org`, `link.springer.com`), so "refused" below means refused to curl; the facts read through WebFetch are one grade below a curl read, as section 0 says:* `www.aceproject.org` (ACE Electoral Knowledge Network), `www.idea.int` (IDEA), `arxiv.org`, `www.cambridge.org`, `onlinelibrary.wiley.com`, `www.sciencedirect.com`, `academic.oup.com`, `pubs.aeaweb.org`, `mpra.ub.uni-muenchen.de`, `hal.science`, `eprints.lse.ac.uk`, `osf.io`, `www.econstor.eu`, `web.stanford.edu`, `www.electoral-reform.org.uk`, `commonslibrary.parliament.uk`; plus the sibling agents' list (nber.org, ideas.repec.org, link.springer.com, fairvote.org, en.wikipedia.org, jstor.org, ssrn.com and others, see section 0). Consequence: the ACE and IDEA electoral-system references the directive suggested could not be read at all; every threshold, quota and formula rule above comes from national electoral authorities (New Zealand, Germany, Italy's Constitution) read by WebFetch.

*Read only by WebFetch and refused or empty:* `elections.nz` (returned a bot-protection stub; not circumvented), `www.econbiz.de` (Anubis bot check), `www.info.gouv.fr` (client error, twice), `www.electoralcommission.org.uk` (client error), the Cambridge supplementary docx "The mathematics of the pivotal voter model with quorum requirements" (binary file the extractor could not open), `https://commbarmatters.com.au/?p=609` (redirected to an unrelated page; not followed).

*Known to exist (named by a source I read) but not read:*
- Mebane, Baltz & Vasselai (2019), "Using agent-based models to simulate strategic behavior in elections", conference presentation (the source of the plurality formulas Baltz uses); Myerson (1998), "Population uncertainty and Poisson games", International Journal of Game Theory 27:385-392; Myerson & Weber (1993), "A theory of voting equilibria", American Political Science Review (found in search; page not read); Myerson (2000), "Large Poisson Games", Journal of Economic Theory (found in search; page not read).
- Cox (1994), "Strategic Voting Equilibria under the Single Nontransferable Vote" (APSR 88(3):608-621; abstract only, which states the "M + 1 rule") and Cox (1997), "Making Votes Count", ch. 7 (publisher summary only).
- Bouton & Gratton (appeared in search results); Bouton, "A Theory of Strategic Voting in Runoff Elections" (journal version, AER 2013; I read the 2012 draft); Myatt (2007), "On the theory of strategic voting", Review of Economic Studies (appeared in search results); Allard (1996) (cited by Ornstein & Norman for "once per century").
- Good & Mayer (1975), Chamberlain & Rothschild (1981), Mulligan & Hunter (2003), Gelman, Silver & Edlin (2012) (cited, not read; covered by the other agents).
- Baltz (2025) supplementary file `S1047198724000329sup001.pdf`.
- The Droop quota formula and any STV-specific pivot treatment; the Conseil constitutionnel's own pages (2002, 2022 results); the Electoral Commission's referendum results; Italian referendum quorum outcomes; the 538 tipping-point CSV; FiveThirtyEight's methodology; any dataset of primary margins; the final 2025 Bundestag vote counts.
- ACE Electoral Knowledge Network and IDEA pages (blocked, above).

---

## Appendix A. Code behind the [measured] numbers

*Python 3 with numpy only. Run with `python3 -I`. These were run from a scratch directory outside the repository; they are reproduced here so a fresh reader can check the numbers. They use no data from the web. The definitions in the text (Q = change in the probability that the voter's side wins, ties by coin) are the ones coded.*

**plur.py**

```python
# Exact decisiveness calculations for plurality, 2 and 3 candidates. All [measured] here.
# Q_j = P(j wins | one more vote for j) - P(j wins | that voter abstains); ties broken uniformly among tied leaders.
import math, sys
import numpy as np

def lg_table(N, a=None):
    if a is None:
        return np.array([math.lgamma(i+1) for i in range(N+1)])
    return np.array([math.lgamma(i+a) for i in range(N+1)])

def two_cand(N, mu, kappa=None):
    # others' votes for A ~ Binomial(N, mu) (kappa None) or Beta-Binomial with alpha=kappa*mu
    x = np.arange(N+1)
    lf = lg_table(N)
    if kappa is None:
        logp = lf[N]-lf[x]-lf[N-x] + x*math.log(mu[0]) + (N-x)*math.log(mu[1])
    else:
        a0, a1 = kappa*mu[0], kappa*mu[1]
        la0, la1 = lg_table(N, a0), lg_table(N, a1)
        logp = lf[N]-lf[x]-lf[N-x] + la0[x] + la1[N-x] - math.lgamma(a0) - math.lgamma(a1) + math.lgamma(kappa) - math.lgamma(N+kappa)
    p = np.exp(logp)
    def w(a, b):  # A's win prob
        return np.where(a > b, 1.0, np.where(a == b, 0.5, 0.0))
    QA = float(np.sum(p*(w(x+1, N-x) - w(x, N-x))))
    return QA

def three_cand(N, mu, kappa=None):
    # returns Q_1, Q_2, Q_3
    lf = lg_table(N)
    if kappa is not None:
        a = [kappa*m for m in mu]
        la = [lg_table(N, ai) for ai in a]
        const = math.lgamma(kappa) - math.lgamma(N+kappa) - sum(math.lgamma(ai) for ai in a)
    Q = np.zeros(3)
    x2 = np.arange(N+1)
    for x1 in range(N+1):
        x2v = x2[:N-x1+1]
        x3v = N - x1 - x2v
        if kappa is None:
            logp = lf[N]-lf[x1]-lf[x2v]-lf[x3v] + x1*math.log(mu[0]) + x2v*math.log(mu[1]) + x3v*math.log(mu[2])
        else:
            logp = lf[N]-lf[x1]-lf[x2v]-lf[x3v] + la[0][x1] + la[1][x2v] + la[2][x3v] + const
        p = np.exp(logp)
        c = np.stack([np.full_like(x2v, x1), x2v, x3v])  # counts, shape 3 x m
        def win(c, j):
            m = c.max(axis=0)
            tied = (c == m).sum(axis=0)
            return np.where(c[j] == m, 1.0/tied, 0.0)
        for j in range(3):
            c2 = c.copy(); c2[j] += 1
            Q[j] += float(np.sum(p*(win(c2, j) - win(c, j))))
    return Q

if __name__ == "__main__":
    print("== two candidates, known shares (0.5,0.5): exact Q_A vs sqrt(2/(pi N))/2 style comparison")
    for N in [100, 1000, 10000, 100000, 1000000]:
        q = two_cand(N, (0.5, 0.5))
        print(N, "Q_A=%.6g" % q, " 1/sqrt(2 pi N)=%.6g" % (1/math.sqrt(2*math.pi*N)), " sqrt(2/(pi N))=%.6g" % math.sqrt(2/(math.pi*N)))
    print("== two candidates, uncertain shares, Beta-Binomial, mu=(.51,.49)")
    for kappa in [100, 400, 2500]:
        for N in [1000, 10000, 100000]:
            q = two_cand(N, (0.51, 0.49), kappa)
            sd = math.sqrt(.51*.49/(kappa+1))
            print("kappa=%d sd_share=%.4f N=%d Q_A=%.6g  N*Q_A=%.4g" % (kappa, sd, N, q, N*q))
```

**plur3.py**

```python
import math, sys
sys.path.insert(0, "<directory holding these files>")
from plur import two_cand, three_cand
cases = [
 ("3 cand, forecast (.40,.38,.22), kappa=400", (0.40,0.38,0.22), 400),
 ("3 cand, forecast (.36,.34,.30), kappa=400", (0.36,0.34,0.30), 400),
 ("3 cand, forecast (.45,.45,.10), kappa=400", (0.45,0.45,0.10), 400),
]
for N in [1000, 10000]:
    q2 = two_cand(N, (0.51,0.49), 400)
    print("N=%d two-cand (.51,.49) kappa=400: Q_A=%.6g N*Q=%.3f" % (N, q2, N*q2))
    for name, mu, kappa in cases:
        Q = three_cand(N, mu, kappa)
        print("N=%d %s: Q1=%.6g Q2=%.6g Q3=%.6g  N*Q=%s" % (N, name, Q[0], Q[1], Q[2], ["%.3f" % (N*q) for q in Q]))
    # knife-edge, known shares
    for mu in [(1/3,1/3,1/3), (0.4,0.4,0.2), (0.45,0.45,0.10)]:
        Q = three_cand(N, mu, None)
        q2k = two_cand(N, (0.5,0.5))
        print("N=%d known shares %s: Q1=%.6g Q2=%.6g Q3=%.6g | two-cand known (.5,.5) Q_A=%.6g" % (N, tuple(round(m,3) for m in mu), Q[0], Q[1], Q[2], q2k))
```

**pr.py**

```python
# [measured] Probability that one extra vote for party j adds a seat to j under D'Hondt (ties by lot ~ 1/2).
# Model: shares ~ Dirichlet(kappa*mu); others' votes ~ Poisson(N*share_i); party j's own count ~ Poisson(N*share_j), integrated analytically.
import math, sys
import numpy as np
lg = np.vectorize(math.lgamma)

def q_party(N, M, mu, kappa, draws=20000, seed=1, chunk=2000):
    rng = np.random.default_rng(seed)
    K = len(mu)
    out = np.zeros(K)
    for j in range(K):
        tot = 0.0; n = 0
        others = [i for i in range(K) if i != j]
        while n < draws:
            m = min(chunk, draws-n)
            sh = rng.dirichlet(np.array(mu)*kappa, size=m)       # m x K
            lam = N*sh
            vo = rng.poisson(lam[:, others]).astype(np.int64)    # m x (K-1)
            d = np.arange(1, M+1)
            # all quotients of others: m x (K-1) x M
            quo = vo[:, :, None] / d[None, None, :]
            flat = quo.reshape(m, -1)
            order = np.argsort(-flat, axis=1)[:, :M]             # top M quotient indices
            top_idx = order                                       # r-th largest = top_idx[:, r-1]
            # for s=1..M need the (M-s+1)-th largest quotient among others
            r = M - np.arange(1, M+1) + 1                         # M..1
            sel = np.take_along_axis(top_idx, (r-1)[None, :].repeat(m, 0), axis=1)  # m x M indices into flat
            party = sel // M                                      # which other party
            dd = (sel % M) + 1                                    # divisor
            vq = np.take_along_axis(vo, party, axis=1)            # votes of that party
            s = np.arange(1, M+1)[None, :]
            num = s * vq                                          # T = num/dd
            T_floor = num // dd
            is_int = (num % dd == 0)
            lam_j = lam[:, j][:, None]
            def logpmf(k):
                k = np.maximum(k, 0)
                return k*np.log(lam_j) - lam_j - lg(k+1)
            # non-integer T: c=1 at v=floor(T). integer T: c=1/2 at v=T and v=T-1
            p_nonint = np.exp(logpmf(T_floor))
            p_int = 0.5*np.exp(logpmf(T_floor)) + 0.5*np.exp(logpmf(T_floor-1))
            contrib = np.where(is_int, p_int, p_nonint).sum(axis=1)
            tot += contrib.sum(); n += m
        out[j] = tot/n
    return out

if __name__ == "__main__":
    cases = [
      ("council-sized: M=27, N=4,000 valid votes", 4000, 27, (.30,.25,.20,.15,.10)),
      ("district: M=5, N=50,000", 50000, 5, (.35,.30,.20,.10,.05)),
      ("district: M=10, N=100,000", 100000, 10, (.35,.30,.20,.10,.05)),
      ("national list: M=150, N=5,000,000", 5000000, 150, (.30,.25,.20,.15,.10)),
    ]
    for name, N, M, mu in cases:
        for kappa in [400]:
            q = q_party(N, M, mu, kappa, draws=6000 if M>50 else 20000)
            print(name, "kappa=%d" % kappa)
            print("   shares", mu)
            print("   Q_j (P that one more vote adds a seat):", ["%.3g" % x for x in q])
            print("   M/N = %.3g ; Q_j / (M/N) = %s" % (M/N, ["%.2f" % (x/(M/N)) for x in q]))
```

**pr_check.py**

```python
# Independent brute-force check of pr.py: direct D'Hondt with ties by lot, adding one vote to party j.
import sys, math
import numpy as np
sys.path.insert(0, "<directory holding these files>")
from pr import q_party

def dhondt_seats(v, M, rng):
    # v: array K ints. returns seats array; ties at last seat broken by lot
    K = len(v)
    quo = []
    for i in range(K):
        for d in range(1, M+1):
            quo.append((v[i]/d, i))
    quo.sort(key=lambda t: -t[0])
    seats = np.zeros(K, dtype=int)
    cutoff = quo[M-1][0]
    sure = [q for q in quo if q[0] > cutoff]
    tied = [q for q in quo if q[0] == cutoff]
    for q in sure: seats[q[1]] += 1
    need = M - len(sure)
    idx = rng.permutation(len(tied))[:need]
    for t in idx: seats[tied[t][1]] += 1
    return seats

def brute(N, M, mu, kappa, j, draws, seed=5):
    rng = np.random.default_rng(seed)
    K = len(mu); gains = 0.0
    for _ in range(draws):
        sh = rng.dirichlet(np.array(mu)*kappa)
        v = rng.poisson(N*sh)
        s0 = dhondt_seats(v, M, rng)[j]
        v2 = v.copy(); v2[j] += 1
        s1 = dhondt_seats(v2, M, rng)[j]
        gains += (s1 - s0)
    return gains/draws

N, M, mu, kappa = 400, 5, (.35,.30,.20,.10,.05), 400
print("analytic:", q_party(N, M, mu, kappa, draws=40000, seed=2))
print("brute j=0:", brute(N, M, mu, kappa, 0, 60000))
print("brute j=1:", brute(N, M, mu, kappa, 1, 60000))
print("brute j=3:", brute(N, M, mu, kappa, 3, 60000))
```

**ref.py**

```python
# [measured] referendum / supermajority / small-electorate decisiveness. Binary contest, N other voters, all vote Yes or No.
import math
import numpy as np
def lgt(N, a=None):
    return np.array([math.lgamma(i+1) if a is None else math.lgamma(i+a) for i in range(N+1)])
def dist(N, mu=None, kappa=None):
    # distribution of Y (yes votes among N others). mu = expected yes share. kappa None -> binomial (known share)
    x = np.arange(N+1); lf = lgt(N)
    if kappa is None:
        logp = lf[N]-lf[x]-lf[N-x] + x*math.log(mu) + (N-x)*math.log(1-mu)
    else:
        a, b = kappa*mu, kappa*(1-mu)
        logp = lf[N]-lf[x]-lf[N-x] + lgt(N,a)[x] + lgt(N,b)[N-x] - math.lgamma(a)-math.lgamma(b)+math.lgamma(kappa)-math.lgamma(N+kappa)
    return x, np.exp(logp)
def passes(Y, X, t):
    # proposal passes if Y/(Y+X) >= t for t>0.5 ; for t=0.5 simple majority with fair coin on tie ; returns prob
    tot = Y + X
    if abs(t-0.5) < 1e-12:
        return np.where(Y > X, 1.0, np.where(Y == X, 0.5, 0.0))
    return np.where(Y >= t*tot - 1e-9, 1.0, 0.0)
def Q(N, mu, kappa, t):
    x, p = dist(N, mu, kappa)
    Y = x; X = N - x
    yes = float(np.sum(p*(passes(Y+1, X, t) - passes(Y, X, t))))     # effect of a Yes ballot on passage vs abstain
    no  = float(np.sum(p*(passes(Y, X, t) - passes(Y, X+1, t))))      # effect of a No ballot on blocking, vs abstain
    return yes, no
if __name__ == "__main__":
    print("== known shares (binomial), simple majority, mu=0.5: Q_yes ~ 1/sqrt(2 pi N)")
    for N in [9, 19, 29, 99, 999, 9999]:
        y, n = Q(N, 0.5, None, 0.5)
        print("N=%d  Q_yes=%.4f Q_no=%.4f  1/sqrt(2piN)=%.4f" % (N, y, n, 1/math.sqrt(2*math.pi*N)))
    print("== uncertain share (kappa=400, sd 2.5pts at mu=.5), N=10,000 others; thresholds 0.5, 0.6, 2/3")
    N = 10000
    for mu in [0.50, 0.55, 0.60, 0.667]:
        row = []
        for t in [0.5, 0.6, 2/3]:
            y, n = Q(N, mu, 400, t)
            row.append("t=%.3f: Q_yes=%.3g Q_no=%.3g" % (t, y, n))
        print("forecast yes share %.3f | " % mu + " | ".join(row))
    print("== small electorates, uncertain share kappa=20 (sd ~11pts), forecast .5 and .6; simple majority")
    for N in [9, 19, 29, 99, 999]:
        out = []
        for mu in [0.5, 0.6]:
            y, n = Q(N, mu, 20, 0.5)
            out.append("mu=%.1f Q_yes=%.4f" % (mu, y))
        print("N=%d " % N + " ".join(out))
```

**ref2.py**

```python
import math, sys
sys.path.insert(0, "<directory holding these files>")
from ref import Q
def Qavg(N0, mu, kappa, t, width=30):
    ys = []; ns = []
    for N in range(N0, N0+width):
        y, n = Q(N, mu, kappa, t); ys.append(y); ns.append(n)
    return sum(ys)/width, sum(ns)/width
print("Referendum with threshold t on Yes/(Yes+No); others N~10,000 (averaged over N=10000..10029 to avoid lattice artefacts); Dirichlet-style uncertainty kappa=400 (sd 2.5 pts at 50%)")
print("Q_yes = P(pass | I vote Yes) - P(pass | I abstain); Q_no = P(pass | abstain) - P(pass | I vote No)")
for mu in [0.50, 0.55, 0.60, 0.667]:
    row = []
    for t in [0.5, 0.6, 2/3]:
        y, n = Qavg(10000, mu, 400, t)
        row.append("t=%.3f: yes=%.3g no=%.3g" % (t, y, n))
    print("forecast Yes %.3f | " % mu + " | ".join(row))
```

**chamber.py**

```python
# [measured, stylised] P(a given seat's outcome decides majority control | that seat is exactly tied), 435-seat chamber.
import math
import numpy as np
def Phi(x): return 0.5*(1+np.vectorize(math.erf)(x/math.sqrt(2)))
def run(m0, base_sd=14.0, tau=3.0, sig_nat=2.0, seed=0, nS=61):
    rng = np.random.default_rng(seed)
    m = rng.normal(m0, base_sd, 434)      # baseline Democratic margin (points) of the other 434 seats
    ss = np.linspace(-4, 4, nS)*sig_nat; w = np.exp(-0.5*np.linspace(-4,4,nS)**2); w /= w.sum()
    pk = np.zeros(435); ed = 0.0; ed2 = 0.0
    for s, ws in zip(ss, w):
        p = Phi((m + s)/tau)
        dp = np.zeros(435); dp[0] = 1.0
        for pj in p:
            dp[1:] = dp[1:]*(1-pj) + dp[:-1]*pj
            dp[0] *= (1-pj)
        pk += ws*dp
        mean = p.sum(); ed += ws*mean; ed2 += ws*(mean**2 + (p*(1-p)).sum())
    # pk[k] = P(D wins exactly k of the other 434). Seat i decides control iff k = 217 (D reaches 218 only with i).
    sd = math.sqrt(ed2 - ed**2)
    return pk[217], ed, sd, pk[216:219]
print("Stylised chamber: 434 other seats, baseline margins ~ N(m0, 14 pts), idiosyncratic sd 3 pts, national swing sd sigma_nat.")
for sig in [1.0, 2.0, 3.0]:
    for m0 in [0.0, 3.0, 6.0]:
        vals = [run(m0, sig_nat=sig, seed=s) for s in range(3)]
        p = np.mean([v[0] for v in vals]); ed = np.mean([v[1] for v in vals]); sd = np.mean([v[2] for v in vals])
        print("sigma_nat=%.1f m0=%+.1f: expected D seats among others=%.0f (sd %.1f)  P(tip | seat tied)=%.4f  (1 in %.0f)" % (sig, m0, ed, sd, p, 1/p if p>0 else float('inf')))
```
