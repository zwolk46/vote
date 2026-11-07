# Breaks of model draft 2

*Worker B1, 2026-11-07, under `briefs/B1-break-the-model.md` (Fable 5.1, xhigh). Read whole and in order: `CLAUDE.md`, `LAW.md`, `the-law-for-agents.md`, `RULINGS.md`, `STATE.md`, `OPERATIONS.md`, `briefs/_COMMON.md`, the brief; then `model/MODEL-DRAFT-2.md` (the draft), `model/MODEL-DRAFT.md`, both brainstorm transcripts, `model/MATH.md`, and every section of the four `research/*-v2.md` reports that a figure or quotation in the draft rests on. `model/math/run_all.sh` was re-run (Python 3.13.18, numpy 2.5.3, 84 s): its output is byte-identical to the committed `OUTPUT.txt` [measured]. The draft is not edited; the orchestrator decides what changes (`_COMMON.md` 3). No subagent was run and nothing was fetched: every figure checked was reachable in the v2 reports and `OUTPUT.txt`, so no source needed re-reading.*

**How to read this.** Every break has a number, a kind (intention, fact, mathematics, reading, missing), a severity and a fix. Severity: **G** changes what gets made; **N** changes a number the draft shows; **W** wording. A break of intention is made as the general law 16b says: one variable moved, the rest held still, and the question whether the draft still says what the maker means, with his words quoted from the transcripts. "Draft §n" is a section of `MODEL-DRAFT-2.md`, "MATH §n" of `MATH.md`, "Sn.m" of `OUTPUT.txt`; R1 to R4 are the v2 reports (decisiveness models, close races, frameworks and cost, electoral systems). Numbers I computed are marked [measured]; they use `model/math/common.py`'s exact sums with the inputs stated, so anyone can re-run them. Section 6 lists what was checked and found sound; section 7 what this check did not do.

---

## 0. The breaks that matter most, in order

1. **#41 (missing, G): one trip casts a whole ballot.** The draft tests one race's p × B against the cost of the trip. A general-election ballot carries many contests; the trip's benefit is the sum over them, and the small local contests on it have p thousands of times the presidential p. Whether his claim is per race or per ballot is his to say; the draft forecloses it without saying so.
2. **#1 (intention, N): the half at a tie is a reading of his word "decides", not his word, and it halves or doubles every p and B\*.** The leading paper on exactly his experiment counts the tie at weight one. The draft's header puts the half under "Settled by Zach".
3. **#3 and #10 (intention, fact; G): "ex ante, from a forecast a voter could have seen" leaves almost no election computable**, and the Economist tables the draft offers for 2008 to 2016 are back-tests of its 2020 model, which no voter saw.
4. **#21 (mathematics, N): simple mode for a presidential state gives the chance the state ties, not the chance the ballot decides the presidency** (3 times too high for Florida in the one case computed).
5. **#9 (fact, N): GSE's "1 in 10 million" is asserted to be "our convention"**; MATH gives two defensible readings, and the other halves p and doubles the headline B\*.
6. **#20 (mathematics, N): the referendum formula is wrong for any threshold but one half** (at two thirds, a No ballot is twice as likely to decide as a Yes).
7. **#8 and #28 (fact, mathematics; N): the $4 cost rests on a figure R3 says not to present as measured, and "tens or hundreds of millions" for B\* is up to hundreds of billions on the draft's own p's.**
8. **#42 (missing, G): voting by mail has no trip**, and the draft's C is the cost of a trip.
9. **#2 (intention, W): the draft tells the maker that what he called B is p × B**; R3 says that is his to say.
10. **#6 and #7 (fact; W, N): the draft's two sentences on one-vote races contradict each other, and the one House case was six votes on the later count.**
11. **#30 (reading, N): the label "the chance it comes down to you" over p shows a stranger half of what the words mean.**

The rest are wording, and each has a fix beside it.

---

## 1. Breaks of intention

**#1. The weight of a tie.** Intention, **N**.
- *Variable:* what "deciding" means when the others are exactly tied without you.
- *Case:* an even number of other voters, exactly tied. Counted, your ballot makes your side win outright; not counted, a lot decides. Or an odd number, your side one short: counted, your ballot makes a tie that a lot decides; not counted, your side loses.
- *The draft:* p is "the rise in your side's chance of winning" (§2), so each case counts one half: p = ½ × P(tied or one short) (§3). The header lists under "Settled by Zach so far: importance is the chance one counted ballot changes the winner". §9 names the A-against-B swing (twice p) as the alternative convention and not this one.
- *His words:* "when I say importance of a vote, I mean the chance it decides the outcome"; "make a difference means the vote itself flips" (19:32). "Decides" carries both readings: the ballot settled the result (the count without you was within one vote of a tie: weight one, MATH's *event*, twice p), or who wins differs because of it (one half under a lot: p). Gelman, King & Boscardin 1998, who state his experiment in his terms ("a person who will either vote for one candidate or not vote", R1 §3.1 A), count the event at weight one; Mulligan & Hunter's "pivotal vote" likewise; Edlin, Gelman & Kaplan and Barnett use the half (MATH §2). "Flips" leans to the draft's reading, "decides" to the other. The orchestrator fixed the comparison and the tie rule for M1; the half followed from defining p as a rise in probability, and he has not been shown it.
- *Fix:* add to §9: "p counts a tie as half a decision, so that p is the rise in your side's chance of winning; the chance that the count without you lands within one vote of a tie is twice p, and the page says which of the two it shows"; and let "Settled by Zach" carry his words, not the paraphrase.

**#2. His B.** Intention, **W**.
- *Variable:* which quantity his phrase names.
- *The draft (§2):* "Your phrase 'the marginal difference between the outcome voted for and the expected outcome' is p × B exactly."
- *His words (19:39):* "B, I've always thought, is like the marginal difference between it would be the magnitude obviously we're considering benefit given a magnitude given a probability of one, or something like that. But never mind. We're just considering the magnitude. Which I think would be the marginal difference between the outcome voted for and the outcome or the expected outcome. I forget exactly where this goes into the framework." He names it B, calls it "the magnitude", "given a probability of one", and offers two comparisons. "The magnitude at probability one" is our B. "The expected outcome with the ballot counted, minus without" is p × B. "The outcome voted for, minus the expected outcome" is neither: it is (1 − P(your side wins)) × B. R3 §2.3 found the first two readings both in the literature and wrote "That is his to say." Draft 1 said both are in the formula "one level apart"; draft 2 decides it and tells him that what he called B is p × B.
- *Fix:* "Your 'magnitude, given a probability of one' is B; the expected outcome with your ballot counted minus without is p × B; both are in the formula, one level apart."

**#3. Ex ante, from a forecast a voter could have seen.** Intention, **G**.
- *Variable:* which elections p can be computed for.
- *Case:* a state house race in 2014; a House race in 1950; any of Klarner's 52 near-ties; a town council.
- *The draft:* §9.2, "p is ex ante: the chance before the election, from a forecast a voter could have seen. The historical record is the check, not the measure." §10 lists forecast archives (538, unread) and the Economist's data as the inputs.
- *His words (19:32, 19:39):* "I would like to apply it to practical cases after"; "then we can find as much historical data as we possibly can"; "be really careful to not foreclose options". Published state-by-state forecast distributions exist for presidential races from 2008 (R1 §3.3); for everything else the sentence as worded yields no p, and the historical data he wants can only ever be "the check". Two of the sources are ex ante without a published forecast: GKB build the forecast from variables known before the election (poll standing two months out) by regression; Mulligan & Hunter take f(½) ≈ 2 as a prior from the distribution of past margins (R1 §3.1 E, §3.3).
- *Fix:* say in §9.2 what the forecast is where none was published (a distribution fitted to the margins of like races, as GKB and Mulligan & Hunter do), so that past races can be inputs and not only the check; or mark the variable open for him.

**#4. "Everything else fixed" and the evidential view.** Intention, **W**.
- *Variable:* where the evidential view is excluded.
- *The draft (§9.3):* "'Everything else fixed' also rules out the evidential view, the idea that your choice is evidence of how like-minded people vote. This was put to Zach on 2026-11-06 without reply."
- *His words (19:32):* the ballot counted or not "while no one sees you"; "counted exactly as it would had you not gone to the polls but no one knows it"; "As many people as you would have convinced to go voting with you, you do in either case". In his experiment your decision is the same in both worlds; the evidential view conditions on a decision, so it has nothing to condition on and is excluded by the construction, not by a reading of "fixed". It can arise only where the draft moves to "the real choice of whether to go" (§6), and there his sentence about the people you would have convinced fixes everyone else by assumption, which excludes it again.
- *Fix:* "The evidential view does not arise in your experiment, where your choice is the same in both worlds; the site's cost test compares going with staying home, and there everyone else is held fixed as you said, which excludes it too."

**#5. Whose hour, at what price.** Intention, **W**.
- *Variable:* the price of the reader's time.
- *Case:* a retiree; a salaried worker voting after work; a student.
- *The draft (§6):* the default values time at $38.00, average hourly earnings of private employees, and calls C "the reader's own number".
- *His words (19:39):* he does not want the cost factors one by one ("whether you work or not, random things like that"), and his claim holds "unless the cost is basically negligible". The default is right to show; charging non-work time at the full average private wage is a convention (R3 §4.3: Gibson et al. charge the full imputed wage; "other conventions exist"), and it is the one that makes C largest.
- *Fix:* name the convention beside the default ("an hour of your time at the average private wage, the convention Gibson et al. use") and let the reader set the price.

---

## 2. Breaks of fact

**#6.** Fact, **W**. Draft §4: "No statewide or federal general election in the record read was decided by one vote", four lines after "one race in 16,577 was decided by one vote (New York's 36th district, 1910)", a federal general election. R2 §2a lists eight House races of 1820 to 1910 with a one-vote margin at some stage of their count (NY-36 1910, IL-7 1854, VA-1 1882, NC-7 1868, IN-6 1847, KY-2 1829, NY-29 1822, MD-6 1820); R2's own summary sentence carries the same looseness, which the draft inherits. *Fix:* "No statewide election, and no federal election since 1910, in the record read was decided by one vote; the House races that were, 1820 to 1910, are in R2 §2a."

**#7.** Fact, **N**. Draft §4 presents NY-36 1910 as decided by one vote and reads it as "a p of about 1 in 180,000 per House ballot". Mulligan & Hunter's Table 3 records a later count of 20,690 to 20,684 ("both parties recognize that the election was not that close", R2 §1a); on their latest counts the US House sample holds no one-vote race, and their unweighted frequency halves. The draft's 1 in 180,000 rests on an event its own source discounts. *Fix:* "officially by one vote; a later count made it six, and Mulligan & Hunter's own later-count check halves their frequency"; show 1 in 180,000 as an upper figure.

**#8.** Fact, **N**. Draft §2: "a cost of $4 to $12". The $4 is $3.80, six minutes at $38.00, and the six minutes is SPAE 2022's "average Election Day wait", whose unit R3 §4.2 doubts (it equals the chart's 6% over 30 minutes; "do not present 6 and 4 as measured minutes"); R3 §5.1 calls that C "the first report's illustration, not a measured cost". Draft 2 keeps the number and drops what it is; its own §6 figures give a low end of $7.60 (12 minutes, the CCES Election Day mean, 2012) or $8.87 (14 minutes, the median time at the polls) [measured]. At 1 in 10 million the low B\* becomes $76 to $89 million, not $40 million. *Fix:* "a cost of $8 to $12, the median and mean time at the polls (§6)", or keep the $4 and say what it is.

**#9.** Fact and mathematics, **N**. Draft §4: "(Gelman, Silver & Edlin 2012, our convention)", and §2 builds its headline B\* on their 1 in 10 million. MATH §3.4: "Two readings are defensible: (a) take the words, so their '1 in 10 million' is in our convention; (b) assume they meant an exact tie, so it is twice ours. I give both; the site must say which it uses and why", plus a √2 ambiguity in the centre density by what their "scale" is. The draft states reading (a) as settled. Under (b), B\* is $80 to $240 million at the draft's costs [measured]. *Fix:* "(Gelman, Silver & Edlin 2012; their words put it in our convention; if they meant an exact tie, p is half and B\* double: MATH §3.4)".

**#10.** Fact, **G**. Draft §10: "The Economist's open model data covers 2008, 2012, 2016 and 2020." R1 S2: the 2008, 2012 and 2016 tables are labelled "economist (backtest)" and were run by the 2020 model with polls up to election day; the fitted model files are not in the repository; the repository holds no decisiveness output; the 2020 page's `p_decisive_vote` method is unread. Under the draft's own §9.2, a back-test is not "a forecast a voter could have seen". *Fix:* "The Economist's repository holds back-tests of its 2020 model on 2008, 2012 and 2016, which no voter saw; for those years no forecast a voter could have seen has been read."

**#11.** Fact, **W**, and a constraint for full mode. Draft §4: the Economist's "method isn't published, so its convention is unknown". R1 S2: the method is not stated on the page or in the public code, and is otherwise unread. The same section: the page's figures carry the Economist's copyright; its CC BY grant covers "the data generated by The Economist" in the repository and excludes "any Economist content", so showing the page's figures on the site is not shown to be licensed. *Fix:* "its method is not stated on the page or in its public code; the page's figures are its copyright, not under its data licence".

**#12.** Fact, **W**. Draft §4: "The closest presidential states were New Mexico 2000 (366) and Florida 2000 (537)." R2 §2b covers 2000 to 2024 only. *Fix:* "since 2000".

**#13.** Fact, **W**. Draft §4: "In 2024 the closest was New Hampshire, at 22,965." By raw votes; by share Wisconsin was closest (0.873%) and New Hampshire was 2.8% (R2 §2b). Closeness in share is what p turns on. *Fix:* "closest by votes; by share, Wisconsin at 0.9%".

**#14.** Fact, **W**. Draft §4: Minnesota's 2008 recount "changed 2,170 votes among 2.4 million". That is the gross change (1,528 added, 642 subtracted), net 264, among the 2,423,851 votes for the two leaders, excluding absentee-envelope rulings (R2 §4). *Fix:* "a gross change of 2,170 votes, net 264, among 2.4 million cast for the two leaders".

**#15.** Fact, **W**. Draft §10: "the 1975 to 1981 classics (paywalled; their results are rederived in MATH)". Beck, Good & Mayer, Chamberlain & Rothschild and Margolis are unread (R1 §3.1 E); what they derive is known only from one sentence in GKBafumi and from third parties; MATH names none of them. MATH §1.2 and §1.4 derive the regimes attributed to them (1/n with an uncertain share; 1/√n or exponentially small with a known one). *Fix:* "unread; the 1/n and 1/√n results attributed to them are derived afresh in MATH §1.2 and 1.4".

**#16.** Fact, **W**. Draft header: "Every figure here has now been read at its source" and "MATH.md, whose 338 numbers run_all.sh reproduces". The Economist's 2020 figures are read from its page with the method unread; Mulligan & Hunter is read in the working paper, the published text unread (R2 §1a); NY-36 1910 is secondary (R2 §2a). "338" is in no file of the record (MATH says "every number"; `OUTPUT.txt` carries no such count) [measured]. *Fix:* "read at its source or, where the reports mark it, at the nearest readable text", and drop the count or say where it was made.

**#17.** Fact, **W**. Draft §5: Edlin, Gelman & Kaplan's example, "voting is worthwhile for any cost under $25". R3 §5: the $25 is for a close election (p = 1/(0.12 n), an expected margin within ±6 points) with hypothetical round inputs ($10 per citizen, a third of the population voting, α = 0.1), and the same paper's voter-alone case gives "less than 10 cents" at n = 1 million. *Fix:* "in a close election, with round hypothetical inputs; for the voter alone the same paper gets under 10 cents".

**#18.** Fact, **W**. Draft §6: "Time at the polling place, waiting plus voting: mean 19 minutes". R3 §4.2: dwell time within 60 metres of the polling place, which the authors call wait plus casting; the mean runs 12 to 23 minutes by the radius chosen; 154,489 likely voters. And "Time in line: 13.3 minutes ... (Stewart)" is from the CCES (30,124 respondents), means of category midpoints. *Fix:* add "measured as time within 60 metres of the polling place, 12 to 23 minutes by the radius chosen" and "(CCES)".

---

## 3. Breaks of mathematics

**#19.** Mathematics, **W**. Draft §2: "when a tie is settled by something other than a fair lot, a small term for the value of the tie itself enters." With p computed under the rule's own π (MATH §1.1) and the tie valued at its expected outcome under that rule, the gain is p × B exactly for every rule and both parities [measured: n = 1,000 and 1,001, Beta-binomial forecast κ = 400, mean 0.51, π = 0.5, 0.3, 1, 0: gain ÷ (pB) = 1.0000 in every case]. MATH §5.1's 1.400 and 0.600 pair the lot p with a tie valued at 0.3, a tie worth something other than its expectation. So the condition is not the rule but the value; the term is not small (±40% in MATH's example) but averages out over parity; and MATH's finding 1 can be refined the same way. *Fix:* "if a tie is worth something other than its expected outcome to you (a new election has a cost of its own), the gain differs from p × B for a known parity by up to p × B itself, and averages to p × B before the election."

**#20.** Mathematics, **N**. Draft §7: referendums with a threshold t are "the two-way formula with t in place of ½. Sound to use." MATH §7 and S7.5: a Yes ballot decides with chance about (1 − t) f(t)/n and a No ballot about t f(t)/n, ratio t/(1 − t); f(t)/(2n) is their average and equals neither unless t = ½ [measured: n = 10,000, forecast centred on t with a 2.5-point sd: at t = 0.6, f/(2n) = 7.98e-4 against R4's Q_yes 6.37e-4 and Q_no 9.56e-4 (×1.25 and ×0.83); at t = ⅔, ×1.45 and ×0.73]. And at a known turnout one of the two is exactly zero by the lattice (S7.5), so the formula holds only averaged over turnout. MATH's "sound" verdict was on R4's ratio, not on this sentence. *Fix:* "a Yes ballot decides with chance about (1 − t) × f(t) ÷ n and a No ballot t × f(t) ÷ n, averaged over turnout; at a two-thirds threshold a No is twice as likely to decide as a Yes".

**#21.** Mathematics, **N**. Draft §8: simple mode takes "one election, three facts" and shows "the chance it comes down to you". For a presidential state the three facts give the chance the state ties; the chance the ballot decides the presidency is that times the chance the state decides the College (MATH §4.1; S6.5 is marked "stage one only"). Florida 2016 back-test: state tie 1 in 960,000; with the College factor 0.3263, 1 in 2.9 million [measured, S6.5 × S4]. *Fix:* "Simple mode is for a race its own count decides; for a presidential state it multiplies by the chance the state decides the College, which full mode computes."

**#22.** Mathematics, **W**. Draft §3 table: p falls as 1/n "once ... n × spread² > about 6, which every real election meets". A 300-voter race at a 5-point sd gives 0.75; 1,000 at 3 points, 0.9; 3,000 at 3 points, 2.7; 10,000 at 2 points, 4.0 [measured]; the draft's §7 includes tiny electorates. MATH §1.3: to 2% once nτ² > 6.25, to 10% once > 1.25. *Fix:* "which every race of more than about 10,000 voters meets at a forecast spread of 2.5 points or more; below that the site uses the exact sum, which is cheap".

**#23.** Mathematics, **W** (a factor-of-two trap). Draft §3 table: "more uncertainty raises p when the expected margin is larger than the uncertainty". MATH §5.8: helps iff |μ − ½| > τ, the forecast share's distance from 50%, which is half the margin (a 52-48 forecast is 2 points off and a 4-point margin). A builder who reads "margin" in the ordinary sense puts the line twice too far out. *Fix:* "when the forecast's lead over 50% is bigger than its standard deviation".

**#24.** Mathematics, **W**. Draft §3 table, recounts: "the zone a recount can swing (tens to hundreds of votes)". The draft's own example moved 2,170 votes gross and the margin by about a hundred (206 or 215 to 312, R2 §3c). MATH §5.10: gain ÷ p is 0.958 when the zone is a third of the forecast spread; Minnesota's 2,170 is 3 to 5% of a 2- to 3-point spread on 2.4 million votes [measured: nτ = 48,000 to 73,000]. The conclusion holds; the words do not match the example. *Fix:* "hundreds to a few thousand votes".

**#25.** Mathematics, **W**. Draft §3, two stages: the shortcut "is within 12 to 23% for states within 2 points of even, and wrong by large factors only in lopsided states, where p is negligible anyway". MATH §4.1: 2 to 3 points off, up to 1.46×; 3 to 10 points off, 0.86 to 16×; "within 2 points" means a forecast share in 0.48 to 0.52, a margin up to 4 points. A state 3 to 10 points off is not lopsided in ordinary speech, and its p is not negligible beside the 1-in-a-billion figures the draft shows. *Fix:* "within 12 to 23% for states whose forecast share is within 2 points of 50% (a 52-48 margin or closer), up to 1.5× for 2 to 3 points off, up to 16× further out, where p is 10 to 1,000 times smaller; the model computes the exact form".

**#26.** Mathematics, **W**. Draft §3: the lay form "is within 3%" for races of 10,000 or more "with ordinary forecast uncertainty". MATH §6.2: within 1.032 for τ ≥ 0.03; at τ = 0.02, the size of the Economist's state forecasts (0.0206 to 0.0223, MATH §4.1), within 4% (S6.2 rows at n ≥ 10,000: 0.960 to 1.000). *Fix:* "within 4% when the forecast's spread is 2 points or more".

**#27.** Mathematics, **W**. Draft §3: "A fixed 'K ÷ n' rule like '10 ÷ n' ... is off by up to 15 times". 15.43 is for 8.33/n; 10/n is off by up to 18.5 in the same table (S6.2, column K10) [measured]. *Fix:* "up to 18 times".

**#28.** Mathematics, **N**. Draft §5: "In a large race, B\* runs to tens or hundreds of millions of dollars." On the draft's own p's: 1 in a billion (New York, California, Texas 2008) gives $3.8 to $12 billion; 1 in 16 billion (California 2020) $61 to $192 billion [measured; R3 §5.1 carries the $3.8 to $12 billion row]. *Fix:* "from tens of millions of dollars in the closest states to hundreds of billions in the safest".

**#29.** Mathematics, **W**. Draft §9.4: "a normal distribution with the heavier-tailed result alongside". MATH §1.5: a t with 4 degrees of freedom matched on the same standard deviation has 1.33 times the normal's centre density, matched on the same scale 0.94; at 3 sd off, 1.4% of the even-race value against 5.3%, a factor 3.7 between the two matchings. *Fix:* "a Student-t with 4 degrees of freedom matched on the same standard deviation".

---

## 4. Breaks of reading

**#30.** Reading, **N** (by the label). Draft §8: "The chance it comes down to you", shown as p. A stranger reads "comes down to you" as the chance that the count without you was within one vote of a tie, which is twice p (see #1) [measured: q = 0.3, n = 100,000: p = 1 in 13,333; the count within one, 1 in 6,667]. *Fix:* label p "the chance your ballot changes who wins"; if "comes down to you" is kept, show twice p under it.

**#31.** Reading, **W**. Draft §3: "f(½) is how densely the forecast of your side's share is packed at exactly 50%". "Density" carries nothing for a reader without statistics. *Fix:* "f(½) is the height of the forecast curve at 50-50: about 50 times the chance the forecast puts your side within one point of 50%" (q₁ ≈ 0.02 f(½), MATH §6.1).

**#32.** Reading, **W**. Draft §3: "Why it works: a finish between 49% and 51% spans about 2% of n possible margins. The tie is one of them, and half of it goes to the coin." The arithmetic is right (MATH §6.1) and the sentence is not readable. *Fix:* "A finish between 49% and 51% covers about 2% of the n possible margins, so each of them, the exact tie included, carries about q ÷ (0.02 n) = 50 q ÷ n of the chance; a tie gives your side half a win, so p ≈ 25 q ÷ n."

**#33.** Reading, **W**. Draft §1 defines p as "How much more likely is your side to win in the world where your ballot counts?" beside his "the chance it decides the outcome". A stranger takes them for two questions; MATH §5.11 shows they are one number when ties are broken the same way in both worlds. *Fix:* add "which is also the chance that who wins differs between the two worlds".

**#34.** Reading, **W**. Draft §2's caveat on the value of a tie sits inside the standard of review and holds only for a known parity (#19). *Fix:* move it to §3 after the tie rules, or into a note.

**#35.** Reading, **W**. Draft §4: "(Gelman, King & Boscardin 1998, which prints the tie-or-one-short chance, twice our p)". A stranger cannot see why that is twice. *Fix:* "which counts a tie as a full decision where we count it as half".

**#36.** Reading, **W**. Draft §5: "Per person affected: divide B\* by the number of people the outcome affects." No example and no source for the divisor. *Fix:* carry one worked case ("at B\* of $120 million and N people, the outcome must be worth $120 million ÷ N to each"), with the Census as the source of N (see #43).

**#37.** Reading, **W**. Draft §6: "In the thought experiment you go to the polls in both worlds, so C cancels there. It enters at the real choice of whether to go." A stranger asks what the site then tests. *Fix:* "The site's test is for the trip: what your counted ballot is expected to gain, against what getting it counted costs."

**#38.** Reading, **W**. Draft §3 table: p "falls steeply ... faster than exponentially" with no anchor. *Fix:* "a 56-44 forecast with a 2-point spread is about a hundredth as likely to tie as 50-50; 60-40 about one in 300,000" [measured: exp(−4.5) = 0.011; exp(−12.5) = 3.7e-6; MATH §5.7].

**#39.** Reading, **W**. Draft §7: list PR, "a vote is more likely to move a seat". More likely than what. *Fix:* "more likely than to decide a two-way winner".

**#40.** Reading, **W**. Draft §4: California 2020 "1 in 16 billion" beside a state of about 17 million voters; a stranger asks how p can be below one in the number of voters. *Fix:* say beside it that this is the state tie times the chance California decides the College.

---

## 5. What is missing

**#41. One trip, many contests.** Missing, **G**. A ballot in a US general election carries the presidency, a Senate or House seat, state legislators, local offices and measures. The cost of the trip is paid once; the trip's expected benefit is the sum of p × B over the contests on the ballot. The draft's standard (§2) is p × B > C for one race against the whole trip's cost, so B\* overstates what any one race must be worth, and the page's verdict on a presidential vote ignores the local race on the same ballot: 2,000 voters at 52-48 with a 4-point spread give p about 1 in 470 (S6.5), against 1 in 10 million for the presidency, twenty thousand times more. His words: "the difference between voting and not voting and still putting the thing into the machine" (the ballot); "the vote itself ... the expected benefit cannot possibly in any case probably outweigh the cost" (19:32). Whether his claim is about one race or the ballot is his to say; the draft decides it without saying so. No source in the record raises it (grep across the v2 reports: nothing) [measured]. *Fix:* say in §2 that B\* is per contest and that the trip pays when the sum over the contests on the ballot exceeds C, and ask him whether the site's unit is the race or the ballot.

**#42. Voting by mail and early voting.** Missing, **G**. The draft's C is "the cost of a trip to vote" (§6). A mail ballot has no trip and no line (SPAE's wait series exclude mail voters, R3 §4.2; eight states are described as all vote-by-mail, R3 §4.4, secondary); the cost is minutes to fill in and return. This is his own carve-out, "unless the cost is basically negligible", and the share of voters it covers is large (not read; the Census P20-585 report R3 used for non-voters' reasons would carry it). *Fix:* add mail and early voting to §6 as a cost case, with the share of voters sourced, and say that the claim's cost is the trip's.

**#43. The divisor of the per-person reading.** Missing, **G**. "Per person the outcome affects" needs a number per office (the presidency: the population; a state seat: its district; a referendum: its jurisdiction) and a source; the draft names none, and full mode cannot show the reading without them. *Fix:* name the source (the Census for populations; districts from the state) and show one case (#36).

**#44. Which forecaster.** Missing, **W**. p is the chance under a named forecast; forecasters differ (the Economist and 538, the latter unread), and §9.4 covers tails only. *Fix:* "p is the chance under the forecast named beside it; where two forecasters published, the page shows both".

**#45. Primaries.** Missing, **W**. Draft §7 lists systems and not primaries, where a small electorate and an even forecast put p highest; R4 found no published estimate. *Fix:* list primaries under §7 as a two-way or plurality race with its own electorate, computed as the model's own.

---

## 6. Checked and found sound

- **The scripts.** `run_all.sh` reproduces `OUTPUT.txt` byte for byte [measured].
- **The formula and its forms.** p = f(½)/(2n), the margin's density at zero, the ex ante average over parity under every tie rule (MATH §1.1, §1.2; my check in #19 agrees), the lay form 25 q/n and its factor 1.22 for n ≥ 1,000 (S6.2), K/n off by up to 15 for 8.33/n (S6.2), the exact sum for small n.
- **The drivers table**, under the conditions in #22 to #25: 1/n (S5.6), closeness with the normal and t figures 1.1%, 1.4%, 5% (S5.7), uncertainty at |μ − ½| = τ (S5.8), structure (S4), recounts with w ≪ nτ (S5.10).
- **Two stages:** 12 to 23% for states within 2 share points of even at ρ = 0.3 to 0.7, the exact form in seconds, the chamber's need for the conditional form (MATH §4).
- **The published p's as quoted:** GSE 2008 (1 in 10 million for NM, VA, NH, CO; 1 in 60 million average; about 1 in a billion for NY, CA, TX), the Economist 2020 (PA 1 in 9 million to CA 1 in 16 billion), GKB 1992 ("about 1 in 10 million for all states", twice ours per MATH §2) (R1 §3.3, R3 §5).
- **The historical figures:** 16,577 House races 1898 to 1992 and NY-36 1910 (subject to #7); Klarner 52 of 109,093 contests, 1968 to 2022; NM 2000 366, FL 2000 537, NH 2024 22,965 by votes; Minnesota 2,170 gross in 2.4 million; Virginia HD94 2017 by lot (R2 §1, §2, §4).
- **The cost figures:** Chen et al. 19/14 minutes, 18% over 30, 154,489, 2016; Stewart 13.3 minutes, 2012; SPAE 2020 14% and 22%; BLS $38.00 (CES0500000003), October 2026 preliminary, via the documented API; Gibson et al. 5.1 minutes, New Zealand 2005; no measured figure for information or registration; 19 minutes = $12.03 (R3 §4).
- **EGK's $25:** 10 × N ÷ (0.12 × N/3) = $250, × 0.1 = $25 [measured].
- **B\*:** $40 to $120 million at 1 in 10 million and $4 to $12; $240 million at 1 in 60 million and $4 (S1.6, S5.2).
- **§7's other verdicts:** plurality with three or more (×1/√(p₁ + p₂)), list PR with its half-seat condition, tiny electorates exact, no number for runoff, IRV, STV and quorums (MATH §7).
- **§9.1:** the A-against-B swing is twice p (MATH §0, §2).
- **"About 200 corrections":** 20 + 46 + 89 + 44 = 199 (R1 to R4) [measured].
- **"Many states use a fair lot":** eight states' statutes read at source prescribe a lot (AK, KY, MN, WA, FL, IA, MI, VA), three a new or special election (IN, MA, TX), six unread (R2 §3a); the fifty-state tally stays unread.
- **The ruling of 00:24** is followed: B\* leads, both readings beside it.

## 7. What this check did not do

- Nothing was fetched: no figure needed a source re-read, since every one was in a v2 report or `OUTPUT.txt`; `_COMMON.md` 6, 7 and 13 were therefore not engaged.
- Not checked, because unread in the record: GSE's code, Mulligan & Hunter's published text, Beck, Good & Mayer, Chamberlain & Rothschild, 538's definitions.
- MATH's §7 verdicts on runoff, IRV, STV and quorums were taken as given; the draft's §7 states them faithfully.
- The checks marked [measured] were run from a script in this thread's scratch (not in the pull request, which adds only this file); each gives its inputs, and `model/math/common.py` has the functions (`betabinomial_pmf` for #19; the rest is arithmetic).
