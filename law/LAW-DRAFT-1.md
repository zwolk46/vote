# The law of the vote-importance site: draft 1

**Status.** Draft 1, not ratified. The orchestrator wrote it from the maker's brainstorm of 2026-11-06 and 2026-11-07 and the decisions he made in it. Nothing here binds until the maker writes that it is ratified. Once it is ratified, its words are not changed; his rulings go beside it in `RULINGS.md`.

**How to read it.** Every term in Part A has the one meaning given there. Every principle in Part B is followed by its reason, and the reason is part of the law. In a case the words did not foresee, apply the principle by its reason; where that does not settle the case, escalate to the orchestrator. Quotations are the maker's own words, with the day and time (UTC) he wrote them. Points marked *open* are not yet settled by him.

---

## Part A. Terms

**The maker.** Zach, whose purpose the site serves. He alone ratifies this law and rules on how it applies.

**The site.** The website this law is for. It is served from the `main` branch of the GitHub repository zwolk46/vote, by the Vercel project `vote`, at https://vote-rho-pearl.vercel.app until the maker names another address.

**A reader.** Anyone who visits the site.

**A race.** One contest decided by the ballots cast in a US election: an office at any level, from president to a local office, in a general election or a primary.

**A ballot.** What one voter casts in one election, with a choice in each race on it.

**A vote.** The choice one ballot makes in one race. "One vote" and "an individual's vote", in the maker's words, mean this.

**Counted and not counted.** The two worlds of the maker's thought experiment. In both, the voter goes to the polls and casts the ballot. In one, it is counted. In the other, it is quietly not counted, and nobody ever knows. Everyone else does exactly the same in both worlds.

**Importance**, written **p**. What the maker calls "the chance it decides the outcome" (2026-11-06 19:32): for one ballot in one race, the chance that who wins differs between counted and not counted.

**Benefit**, written **B**. How much better, in dollars, the outcome the voter chose in a race is than the other outcome.

**Cost**, written **C**. What it costs the voter, in dollars, to cast the ballot: time, travel and effort.

**Break-even stakes**, written **B\***. C ÷ p: how much the outcome of a race would have to be worth for the vote's expected benefit, p × B, to equal its cost.

**A forecast.** A statement, made before an election, of how likely each split of the votes in a race is.

**The model.** The document that says how p, B\* and C are computed, from which inputs and sources. It is `model/MODEL-DRAFT-3.md` until the maker approves a version, and then the version he approves.

**A true source.** The party that counted or measured a figure, read where that party publishes it: an election authority for results, a statistics agency for wages or populations, the authors of a study for its findings. A figure taken from memory, from a summary, or from a page that only repeats it is not from a true source.

---

## Part B. The law

### The end

**1.** The site exists so that the maker can show why he says an individual vote doesn't matter: that one vote's expected benefit, by itself, in most cases does not outweigh what it costs to cast. It shows, for real US races, in which cases the benefit is greater than the cost and in which it is less.

*Reason.* The maker's words: "I want to be able to demonstrate why I say what I say, which is that voting doesn't matter"; "an individual's vote [...] the vote itself [...] the expected benefit cannot possibly in any case probably outweigh the cost. However, [...] unless the cost is basically negligible"; "In which cases would the benefit be greater than something? In which cases would it be less?" (all 2026-11-06 19:32). He asked for "a really nice visualization of the importance of a vote, like the statistical importance of a vote" (2026-11-06 15:34).

**1a.** The site shows what the standard of review (2) gives for every race it covers, including the races where a vote pays for itself.

*Reason.* The maker asked in which cases the benefit is greater and in which it is less, and asked that nothing untrue be assumed (9a). A demonstration that left out the cases against his claim would show nothing about the claim.

**1b.** The site does not say whether anyone should vote, and does not say that voting by the public is a bad thing. It does not weigh civic duty, the expression of a view, or a vote's influence on others. Importance holds those fixed by its definition, and the site says so.

*Reason.* "I don't say it to mean [...] the fact that the populace votes the idea is bad. I don't think that"; "We're totally eliminating any other potential factor"; "As many people as you would have convinced to go voting with you, you do in either case" (2026-11-06 19:32). The arguments he means to answer are duty and influence (same message). A reader who does not see them held out will take p as an answer to a question it does not ask.

**1c.** The measures (3 to 6) are held together. Where they conflict, truth (8) governs every one of them, and the end governs all.

*Reason.* A false number defeats the demonstration, whatever else the page does well.

### The standard of review

**2.** A vote pays for itself in a race when p × B is greater than C, that is, when B is greater than B\*. For each race it shows, the site leads with B\*. Beside it, the site shows what B\* means for the voter alone and what it means per person the outcome affects. It does not choose whose welfare B counts.

*Reason.* "Let's first figure out the standard of review. In which cases would the benefit be greater than something? [...] Although we don't necessarily have to do a find a number for it to be greater or less than" (2026-11-06 19:32). B\* answers that question without choosing B for any reader. Asked whose welfare B counts, the maker chose "Lead with break-even, show both" (2026-11-07 00:24).

**2a.** p is the chance as it stood before the election, under a named forecast of the race. The forecast is one a forecaster published or, where none was published, one the model builds only from what was known before the election and marks as its own. Results after the election are the check on p, and past races are inputs through such forecasts.

*Reason.* The choice whether to vote is made before the election, with what could be known then. The maker wants the standard applied to "practical cases" and "as much historical data as we possibly can" (2026-11-06 19:32). Published forecasts exist for few races besides the presidency, so a p that needed one would leave out almost every past race.

**2b.** No two quantities are shown under one name. Two quantities that published sources often call by the same names as p are named whenever they are shown, and never shown as p. They are the chance that the count without the ballot lands within one vote, and the effect of a vote for one side against a vote for the other. Each is twice p.

*Reason.* Published estimates differ from one another by a factor of two in just this way (model §3 and §4). A reader who compares the site's p with a published one would otherwise be misled by half.

**2c.** Each race shows its own p and B\*. Whether a trip to vote pays is judged over the whole ballot it casts: the trip pays when the races' shares B ÷ B\* add up to more than 100%, that is, when p × B summed over the races on the ballot is greater than C.

*Reason.* One trip casts every race on the ballot, and its cost is paid once. Asked "Judge the trip against one race, or the whole ballot?", the maker chose "Each race, and the ballot summed" (2026-11-07 02:32).

### The measures

**3. Plain.** A reader with no training in statistics can follow the demonstration: what is measured, the chance for a race, its break-even stakes, and what they mean.

*Reason.* "The site that we eventually make is supposed to be a visual demonstration, so it should not be mathematically that complex" (2026-11-06 19:39).

**4. Real.** Behind every figure, a reader who wants it can reach the full computation: its inputs, their sources, and the exact formula. The model provides two modes for this, a simple mode and a full mode.

*Reason.* "Or it could be, to make it real, maybe there could be two modes or something" (2026-11-06 19:39). A demonstration that a doubting reader cannot check does not answer the doubt.

**5. Broad.** The site covers as many real US races, at every level, as true sources allow: president (state by state), Senate, House, state legislature and local.

*Reason.* "Then we can find as much historical data as we possibly can" (2026-11-06 19:32). Asked which elections the site covers, the maker chose "US races at every level" (2026-11-07 01:59), so a reader sees p grow as races shrink.

**6. Beautiful.** The site is a really nice visualization.

*Reason.* "A really nice visualization of the importance of a vote" (2026-11-06 15:34).

### The path

**7.** The model says how every number is computed. It is the orchestrator's work at the maker's ask, and it comes back to him for approval before the site is built on it.

*Reason.* "I want you to fully flesh out the model"; "I don't think that I need to think of the factors individually or discuss them with you" (2026-11-06 19:39). A path that the system chooses comes back to the maker before the system acts on it, because he bears the cost of a wrong one.

**7a.** The work goes in this order: the standard of review; then the data, as much as true sources allow; then the design; then the build. Before the data work begins, the orchestrator puts its plan to the maker once.

*Reason.* "Let's first figure out the standard of review [...] and then we can find as much historical data as we possibly can" (2026-11-06 19:32). The plan is the system's path, so it comes back to him (7).

**7b.** The site is built in the repository's starter (Preact, Vite and IBM Plex Sans, in the midterms site's style) and deployed by Vercel from `main`. Code reaches `main` only through pull requests that the orchestrator checks.

*Reason.* The maker set up the repository and its Vercel project for this site (2026-11-06 15:34). Checking each change before it reaches `main` keeps a broken change off the site.

**7c.** Only three things go to the maker: the plan (7a); questions that this law and its end cannot settle; and requests for his word on money or outside parties (10). Each question is specific and bears materially on the end.

*Reason.* "We also follow a process here so that I can be very hands off" (2026-11-06 15:34); "ensure that the questions are materially related to the goal" (2026-11-06 19:39).

### Constraints

**8.** Every number on the site is true and comes from a true source, and the page names that source. This covers every input to a formula. A figure the model computes is checked, and its computation is shown where a reader would ask. Where a true source cannot be read, the record says where the figure was read instead, and the site does not present it as read at its source.

*Reason.* A formula's output is only as true as its inputs. "True things from true sources" is the maker's standing rule for this repository.

**9.** Where a figure's publisher has not licensed its use, the site does not show it unless the maker obtains the publisher's leave.

*Reason.* Showing it otherwise uses another party's work without leave, and only the maker deals with outside parties (10).

**9a.** Nothing the model or the site rests on is assumed. Each such thing is from a true source, or derived and checked, or marked as a choice the maker can correct. No option the maker might want is closed without his word.

*Reason.* "I want you to be really careful to not foreclose options or assume things that aren't true. Especially if the things to be assumed really bear on whether or not the goal is accomplished or what the goal is" (2026-11-06 19:39).

**10.** Nothing is bought, and no outside party is contacted, without the maker's word. Free accounts and keys are opened as needed. No secret is ever committed to the repository.

*Reason.* He bears the cost and speaks for the project to others. A committed secret is public for good.

### Lesser ends

**11.** The site looks and feels very like the midterms site (zwolk46/midterms). Where that conflicts with the end, the end governs.

*Reason.* "A site very similar looking in feel and style to the midterm site" (2026-11-06 15:34). It is a want along the way, not the end. A chart the demonstration needs is drawn even if the midterms site has none like it.

**12.** The making is rigorous, and each model is assigned where it is most reasonable, as `PROJECT-INSTRUCTIONS.md` sets out.

*Reason.* "I want this to be really rigorous, so I'm willing to use usage, but still like Sonnet, Opus, and Fable should be assigned where they're most reasonable" (2026-11-06 19:59).

### Considerations, not decisions

- **The maker's taste**, as recorded in the midterms project (`inherited/DESIGN.md`): real components from real examples, never invented ones; no shadows, glows or decorative motion; colour that carries meaning; light and dark by the reader's choice; and a site that leans to no party ("it's just a data displayer, it's not right or left", midterms, 2026-11-05 20:58). This is evidence of what he likes, not law.
- **Feeling about voting.** "There's something strong emotional connection to voting" (2026-11-06 19:32). Readers come to the subject with it.
- **Other frameworks exist** that the site's question leaves aside: a vote as one of many causes of the result, and voting as expression (`research/frameworks-benefit-cost-v2.md`). A reader may ask about them.

### The maker's part after ratification

He approves the plan once (7a), answers the questions that come to him (7c), gives or withholds his word on money and outside parties (10), and rules on how this law applies. His rulings are recorded beside the law, and its words are not changed.

---

## Decided cases that bear on the site

- **2026-11-07 00:24, whose welfare is in B.** Asked "Count whose welfare in B, the value of the outcome?", he chose "Lead with break-even, show both" (principle 2).
- **2026-11-07 01:59, which elections.** Asked "Choose which elections the site covers", he chose "US races at every level" (principle 5).
- **2026-11-07 02:32, one race or the whole ballot.** Asked "Judge the trip against one race, or the whole ballot?", he chose "Each race, and the ballot summed" (principle 2c).

## Open points

- **A tie as half a decision.** Under a lot, a counted ballot that breaks or makes a tie changes who wins half the time, so importance counts a tie as half (Part A). The chance that the count without the ballot lands within one vote is twice p. This is the orchestrator's reading of "decides" and "the vote itself flips" (2026-11-06 19:32), open to the maker's correction (model §9.2).
- **Ballot measures.** Measures are on the same ballot as races, so they would enter the ballot's sum (2c). Whether the site covers them is not settled.
- **Before launch.** The address above asks visitors to sign in to Vercel. The address readers will use, and when the sign-in is lifted, are the maker's to settle.
