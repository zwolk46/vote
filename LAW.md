# The law of the vote-importance site

**Status.** In force as if ratified, by the maker's word of 2026-11-07 02:55 UTC: "assume it ratified and start building until you hear otherwise, if you hear otherwise at all." He has not yet read it. Whatever he says about it is a ruling, recorded beside it in `RULINGS.md`; its words are not otherwise changed. This is the second draft. The first (`law/LAW-DRAFT-1.md`) was read cold by two readers (`law/COLD-READING-A-draft-1.md`, `-B-`) and broken in 61 places (`law/BREAKS-draft-1.md`); this text takes those in, and the maker's design guidance of 02:54.

**How to read it.** Every term in Part A has the one meaning given there. Every principle in Part B is followed by its reason, and the reason is part of the law. In a case the words did not foresee, apply the principle by its reason. Where that does not settle the case, a worker escalates to the orchestrator, and the orchestrator to the maker. Quotations are the maker's own words, with the day and time (UTC) he wrote them; "[...]" marks a cut. A reason marked *the orchestrator's* is the system's reading or choice, not his words, and he may correct it.

---

## Part A. Terms

**The maker.** Zach, whose purpose the site serves. He alone ratifies this law and rules on how it applies.

**The orchestrator.** The agent that holds this law and the state of the work and directs the other agents, the workers.

**The site.** The website this law is for.

**A reader.** Anyone who visits the site.

**Phone and desktop.** The site is read on both. On a phone it is read at widths from 320 pixels, and with text up to twice its usual size.

**A contest.** One decision made by the ballots cast in a US election: an office (**a race**) or a ballot measure (**a measure**). For the presidency the race is the presidency itself, won through the voter's state, and who wins means who becomes president.

**A ballot.** What one voter casts in one election, with a choice in some or all of the contests on it.

**A vote.** The choice one ballot makes in one contest. The maker's "a vote", "the vote itself" and "an individual's vote" are read as this, with the ballot summed (2c).

**Counted and not counted.** The two worlds of the maker's thought experiment. In both, the voter casts the ballot, at the polls or by mail. In one, it is counted. In the other, it is quietly not counted, and nobody ever knows. Everyone else does the same in both worlds.

**Importance**, written **p**. What the maker calls "the chance it decides the outcome" (2026-11-06 19:32): for one vote in one contest, the chance that who wins differs between counted and not counted. Suppose the count without the ballot is tied, or the voter's side is one short, and a lot settles the tie. Then who wins differs half the time, so such a tie counts as half (see the open points).

**Benefit**, written **B**. How much better, in dollars, the outcome the voter chose is than the outcome that wins without the ballot, for whoever's welfare is counted (2).

**Cost**, written **C**. What it costs the voter, in dollars, to cast the ballot: the time, the travel and whatever else the voter gives up.

**Break-even stakes**, written **B\*** and said "B-star". C ÷ p: how much the outcome of a contest would have to be worth for the vote's expected benefit, p × B, to equal the cost.

**A forecast.** A statement of how likely each split of the votes in a contest is, made before the election or from only what was known before it.

**The model.** The document that says how p, B\* and C are computed, from which inputs and sources: `model/MODEL.md`, approved by the orchestrator under the maker's word of 2026-11-07 02:38. Later changes to it are recorded and marked as choices he can correct.

**A true source.** The party that counted, measured or computed a figure, read where that party publishes it: an election authority for results, a statistics agency for wages or populations, the authors of a study for its findings. A compilation of such counts also qualifies when its compiler names where each figure came from and its figures are checked against those origins where a reader would ask. A figure taken from memory, or from a summary, is not from a true source.

**The record.** The repository's notes on the work: the research, the rulings, the state of the work and its log.

**The design guidance.** The folder `inherited/design/` (its `README.md`, the maker's design rulings in `TASTE.md`, and the specifications it names), carried from the midterms site.

---

## Part B. The law

### The end

**1.** The site exists so that the maker can show, for real US contests, what a vote is expected to be worth against what casting it costs. This is the reasoning behind his saying that an individual vote doesn't matter, in that isolated sense and unless the cost is next to nothing. For each contest and for a ballot as a whole, the site shows how much the outcome would have to be worth for the vote to pay, so that a reader sees how high that bar is in each case. It serves the people he says this to: readers who come with the civic-duty and influence arguments and a strong feeling about voting, and who have no training in statistics.

*Reason.* The maker's words: "I want to be able to demonstrate why I say what I say, which is that voting doesn't matter"; "an individual's vote at least in this isolated context [...] the expected benefit cannot possibly in any case probably outweigh the cost. However, [...] unless the cost is basically negligible"; "In which cases would the benefit be greater than something? In which cases would it be less? Although we don't necessarily have to do a find a number for it to be greater or less than, of course"; "I always am faced with the it's a civic duty, so one should do it anyway. Or your vote may influence others"; "There's something strong emotional connection to voting" (all 2026-11-06 19:32). He asked for "a really nice visualization of the importance of a vote, like the statistical importance of a vote" (2026-11-06 15:34). Who the readers are is *the orchestrator's* reading of those words.

**1a.** The site shows what the standard of review (2) gives for every contest it covers. That includes the contests where the break-even stakes are lowest, which tell against his claim.

*Reason.* He asked in which cases the benefit is greater and in which it is less, and asked that nothing untrue be assumed (9a). A demonstration that left out the cases against his claim would show nothing about the claim.

**1b.** The site answers one question: a vote's effect on who wins, against what casting it costs. It says that it leaves aside every other reason to vote, such as civic duty, influence on others, or any other. It does not say that voting by the public is a bad thing.

*Reason.* "I don't say it to mean the vote itself the final vote the outcome of the vote or the fact that the populace votes the idea is bad. I don't think that"; "We're totally eliminating any other potential factor. Or any consequence or things like that" (2026-11-06 19:32). A reader who does not see the other reasons set aside will take p as an answer to a question it does not ask.

**1c.** The site is judged on all four measures (3 to 6) at once, and none is traded away for another. Where they conflict, truth (8) governs each of them, and the end governs all.

*Reason.* A demonstration that is plain but false, or true but unreadable, shows nothing.

### The standard of review

**2.** A vote covers the cost of casting the ballot by itself when p × B is greater than C, that is, when B is greater than B\*. The standard weighs casting the ballot against not casting it. Everyone else is held fixed either way, so the only difference the voter makes is the count, and importance measures that difference. For each contest it shows, the site leads with B\*. Beside it, the site shows what B\* means for the voter alone and what it means per person in the jurisdiction the office or measure serves. The site does not choose whose welfare B counts. C on the page is a default built from true sources, and the reader may replace it with their own.

*Reason.* "[...] let's first figure out the standard of review. In which cases would the benefit be greater than something? In which cases would it be less?" (2026-11-06 19:32). B\* answers that without choosing B for any reader. Asked whose welfare B counts, the maker chose "Lead with break-even, show both" (2026-11-07 00:24).

**2a.** p is the chance as it stood before the election, under a named forecast of the contest. The forecast is one a forecaster published or, where none was published, one the model builds from only what was known before the election and marks as its own. How often contests like it have in fact ended within a vote is the check on p. Because the model's own forecasts are fitted to past contests, past contests are inputs too.

*Reason.* *The orchestrator's*, approved with the model under the maker's word of 02:38 (model §9.3). The choice whether to vote is made before the election, with what could be known then. The maker wants the standard applied to "practical cases" and "as much historical data as we possibly can" (2026-11-06 19:32). The research found published estimates of p only for the presidency (model §4), so a p that needed a published estimate would leave out almost every contest.

**2b.** No two quantities are shown under one name. Published sources often give two other quantities under names like p's. One is the chance that the count without the ballot lands within one vote of a tie. The other is how much likelier one side is to win for a vote cast for it rather than for the other side. Each is named whenever it is shown, and neither is shown as p.

*Reason.* *The orchestrator's*, from the research and the model's mathematics (model §3 and §4). Under the model's tie reading each of the two is twice p, and published estimates differ from one another by a factor of two in just this way. A reader who compares the site's p with a published one would otherwise be misled by half.

**2c.** Each contest shows its own p and B\*. Whether casting a ballot pays, by a trip or by mail, is judged over the whole ballot. It pays when p × B summed over the contests on it that the site covers is greater than C. Because the site chooses no B, it shows the ballot's own break-even under each reading of 2. A reader who sets stakes contest by contest sees the shares B ÷ B\* add up.

*Reason.* One trip, or one mail ballot, casts every contest on the ballot, and its cost is paid once. Asked "Judge the trip against one race, or the whole ballot?", the maker chose "Each race, and the ballot summed" (2026-11-07 02:32).

### The measures

**3. Plain.** A reader with no training in statistics, on a phone or a desktop, can follow the demonstration. That means what is counted and what is computed, the chance for a contest, its break-even stakes, and what they mean. It also means what makes the chance larger or smaller: how many vote, how close the contest is expected to be, how sure the forecast is, and the stages a contest passes through.

*Reason.* "[...] the site that we eventually make is supposed to be a visual demonstration, so it should not be mathematically that complex" (2026-11-06 19:39); "what are the actual underlying factors that modulate how much or if a vote matters, probably how much" (2026-11-06 19:32).

**4. Full.** Behind every figure, a reader who wants it can reach the full computation: its inputs, their sources, and the exact formula. How the site offers this is the model's to say (model §8: a simple mode and a full mode).

*Reason.* "Or it could be, to make it real, maybe there could be two modes or something" (2026-11-06 19:39). A demonstration that a doubting reader cannot check does not answer the doubt.

**5. Broad.** The site covers as many real US contests, at every level, as true sources allow.

*Reason.* "[...] and then we can find as much historical data as we possibly can" (2026-11-06 19:32). Asked which elections the site covers, the maker chose "US races at every level" (2026-11-07 01:59), so a reader sees p grow as contests shrink.

**6. Beautiful.** The site is a really nice visualization, made as the design guidance says. The maker's rulings in `TASTE.md` stand here as his defaults, read with his correction of 2026-11-07 02:45: components are his picks, or designed within the principles, not only found ones. Where the design guidance and this law differ, this law governs.

*Reason.* "[...] a really nice visualization of the importance of a vote" (2026-11-06 15:34). "We're going to follow the new design guidance" (2026-11-07 02:54). He wants the corrections he made on midterms "automatically applied" here (2026-11-07 02:39, `inherited/design/ASK.md`), so that he does not have to make them again.

### The path

**7.** The model says how every number is computed. It is the orchestrator's work at the maker's ask, and he left its approval to the orchestrator.

*Reason.* "I want you to fully flesh out the model"; "I don't think that I need to think of the factors individually or discuss them with you" (2026-11-06 19:39); "I trust your judgment to approve the model" (2026-11-07 02:38).

**7a.** The standard of review comes first, then the data. Design and build follow, alongside the data wherever accuracy allows. Before the data work begins, the orchestrator records its plan in the repository and tells the maker; it does not wait for his approval.

*Reason.* "[...] let's first figure out the standard of review [...] and then we can find as much historical data as we possibly can" (2026-11-06 19:32); "some of this stuff can probably be done at the same time while some of it requires the responses from previous agents [...] Without sacrificing any accuracy" (2026-11-06 19:50); "And then work autonomously" (2026-11-07 02:54).

**7b.** The site begins from the starter in the repository, in the midterms site's style (11), and is served by Vercel from the repository's `main` branch. What it is built with beyond that is the system's choice, made once the design work has learned enough to choose. Code reaches `main` only through pull requests that the orchestrator checks.

*Reason.* The maker said he would connect the repository to a Vercel project for this site (2026-11-06 15:34), and did. A tool fixed before the field is learned may not suit what the demonstration needs. Checking each change before it reaches `main` keeps a broken change off the site.

### Constraints

**8.** Every number on the site comes from a true source, read there. The page names the source and the date it was read or the period it covers. This covers every input to a formula. A figure the model computes is checked by an agent other than the one that computed it, and its computation is shown where a reader would ask. Where a figure could be read only at second hand, the page says so, and where.

*Reason.* "Without sacrificing any accuracy" (2026-11-06 19:50); "I want this to be really rigorous" (2026-11-06 19:59). "True things from true sources" is the midterms site's law, which this repository carries in its working rules. A formula's output is only as true as its inputs.

**9.** Figures are quoted with their source, as a study's findings are. A publisher's tables, pages or data are not reproduced beyond what its terms allow, and asking a publisher for more is the maker's word (10).

*Reason.* *The orchestrator's.* The research found published figures whose publisher keeps its copyright outside its data licence (model §4). Quoting a finding with its source is ordinary; copying another's work wholesale is not ours to do.

### Rules for the system

**9a.** Nothing that bears on whether the end is reached, or on what the end is, is assumed or closed without the maker's word. Each such thing is from a true source, or derived and checked, or marked as a choice he can correct.

*Reason.* "I want you to be really careful to not foreclose options or assume things that aren't true. Especially if the things to be assumed really bear on whether or not the goal is accomplished or what the goal is" (2026-11-06 19:39).

**9b.** These go to the maker:
- the plan, as news (7a);
- questions that this law and its end cannot settle, or that the orchestrator judges really important to the end;
- for a surface that matters, two or three whole options to pick from (the design guidance);
- requests for his word on money or outside parties (10);
- word that the site is ready.

Each question is specific.

*Reason.* "We also follow a process here so that I can be very hands off" (2026-11-06 15:34); "ensure that the questions are materially related to the goal or something else that you judge is really important towards the end that you now understand" (2026-11-06 19:39); "Then it lets me know once it's ready" (2026-11-06 15:34).

**10.** Nothing is bought, and no outside party is contacted, without the maker's word. Opening a free account or key with a service is not contacting a party, and it is done as needed. No secret is ever committed to the repository. Which AI model and effort each agent uses is set by `PROJECT-INSTRUCTIONS.md`, which the maker approved (2026-11-06 20:03).

*Reason.* He bears the cost and speaks for the project to others. A committed secret is public for good.

### Lesser ends

**11.** The site looks and feels very like the midterms site (zwolk46/midterms). Where that conflicts with the end, the end governs.

*Reason.* "[...] a site very similar looking in feel and style to the midterm site" (2026-11-06 15:34). It is a want along the way, not the end. A chart the demonstration needs is drawn even if the midterms site has none like it.

### Considerations, not decisions

*Evidence the system weighs. Nothing here binds.*

- **Feeling about voting.** "There's something strong emotional connection to voting" (2026-11-06 19:32). Readers come to the subject with it.
- **Other frameworks exist** that the site's question leaves aside: a vote as one of many causes of the result, and voting as expression (`research/frameworks-benefit-cost-v2.md`). A reader may ask about them.
- **A reader's own ballot.** "[...] if the vote is in a place where the vote is statistically more likely to make a difference" (2026-11-06 19:32). Whether a reader finds the contests on their own ballot, by state or by address, or reads a table, is the plan's to settle.

### The maker's part

He looks over this law, as he said he would, and rules on how it applies. He picks among the options shown to him (9b) and gives or withholds his word on money and outside parties (10). The address, the sign-in and share cards at launch are also his (open points). His rulings are recorded beside the law.

---

## Decided cases that bear on the site

- **2026-11-07 00:24, whose welfare is in B.** Asked "Count whose welfare in B, the value of the outcome?", he chose "Lead with break-even, show both" (2).
- **2026-11-07 01:59, which elections.** Asked "Choose which elections the site covers", he chose "US races at every level" (5).
- **2026-11-07 02:32, one race or the whole ballot.** Asked "Judge the trip against one race, or the whole ballot?", he chose "Each race, and the ballot summed" (2c).
- **2026-11-07 02:38, the model.** "I trust your judgment to approve the model" (7).
- **2026-11-07 02:54, design and autonomy.** "We're going to follow the new design guidance. [...] And then work autonomously" (6, 7a).
- **2026-11-07 02:55, this law.** "[...] assume it ratified and start building until you hear otherwise" (Status).

## Open points

- **A tie as half a decision.** Importance counts a tie settled by lot as half (Part A), because who wins then differs half the time. The chance that the count without the ballot lands within one vote, the event, is twice p. This is the orchestrator's reading of "decides" and "the vote itself flips" (2026-11-06 19:32). The nearest thing in the record to his word on it points the other way. At 19:34 the orchestrator defined p to him as "the chance your vote is decisive, meaning without it the count would be an exact tie or your side one short", the event, and he answered "So the math you went into is important. I agree" (19:39). Whether that reaches the definition is his to say. The site always says which of the two it shows (2b).
- **The model's other readings** (model §9) are settled by his leaving the model to the orchestrator (7), unless he rules otherwise:
  - counted against not counted;
  - p before the election (2a);
  - the evidential view, which does not arise;
  - forecast tails;
  - the default cost.
- **Ballot measures.** They are contests (Part A), and the model computes them. Whether the site covers them is not settled; until it is, the plan may include them where true sources allow.
- **An election before it is held.** Whether the site covers a coming election, under a forecast published for it, or past contests only.
- **Before launch.** The site's present address (https://vote-rho-pearl.vercel.app) asks visitors to sign in to Vercel, and a site behind a sign-in shows no link previews when shared. The address readers will use, when the sign-in is lifted, and whether share cards are needed are the maker's to settle.
