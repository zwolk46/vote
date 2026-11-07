# Cold reading B of law draft 1

*2026-11-07, a Sonnet 5.5 subagent at xhigh, in the role of a business-school graduate (an MBA) with no statistics and no knowledge of how websites are built, reading the text for a friend. It saw only the text of `law/LAW-DRAFT-1.md` and seven questions (what the site is for; its first screen; what each principle requires; words with two readings; principles in conflict; what it would ask; what seems wrong). Its response, verbatim:*

---

**Cold reading of the draft law of the vote-importance site**

**1. What the site is for and whom it serves**

The site lets its maker, Zach, show other people why he believes one vote almost never pays for itself. For most US races, the chance that a single ballot decides the outcome is so small that the expected benefit is less than the time, travel and effort of voting. It works this out for real US races, from president down to local offices. For each race it gives the tiny chance (p) and the "break-even stakes" (cost divided by that chance, meaning how valuable the outcome would have to be for the vote to be worth it), and it shows which races clear the bar and which don't. It is aimed at ordinary visitors with no statistics training, who should be able to follow the idea visually and check the sources and arithmetic. It is not meant to say that people should not vote, or that voting is bad. It is a narrow probability-and-dollars calculation that deliberately sets aside duty, self-expression and influence on other voters.

**2. The first screen, and what is left off**

The text never describes a first screen, so what follows is inference. The closest it comes is principle 2, which says that for each race the site "leads with B\*". I would expect the opening to pose the question and show a visualization whose headline figure is break-even stakes. Beside it would be that figure for the voter alone and per person affected. A plain note would say what is being measured and what is held fixed (principle 1b). The look would copy the maker's "midterms" site. The text does not say whether there is a map, a search box, a featured race, or any way for a reader to enter their own numbers.

Left off, by the text:
- any verdict on whether anyone should vote, or any claim that public voting is bad;
- any weighing of civic duty, expression, or a vote's influence on others;
- any party lean;
- figures from memory, from summaries, or from pages that only repeat a figure;
- figures whose publisher hasn't licensed their use;
- any unflagged assumption;
- any choice of whose welfare counts in B;
- a "p" calculated with hindsight from the result;
- two different quantities under the same name.

The draft says the site must not leave out the races where a vote does pay for itself. The "taste" items (no shadows, glows or decorative motion) are labelled evidence, not law. Ballot measures are undecided.

**3. What each principle requires of the builders**

(I include 7a, 7b, 7c and 9a with the numbered ones.)

- 1: Build the site to demonstrate that one vote's expected benefit usually falls short of its cost, and to show, for real races, which cases fall on which side.
- 1a: Show the results for every race covered, including those where a vote pays for itself, not only the ones that support the maker.
- 1b: Never say whether anyone should vote or that voting is bad. State plainly that duty, expression and influence on others are held fixed and not weighed.
- 1c: Plain, real, broad and beautiful are balanced together, but truth beats each of them, and the end beats everything.
- 2: Lead each race with the break-even stakes, show it for the voter alone and per person affected, and do not pick whose welfare counts.
- 2a: Calculate p as it stood before the election, using a named forecast. That is a published one, or one the model builds from pre-election information and labels as its own. Actual results serve only to check p.
- 2b: Never present two different quantities under one name. The two look-alikes (the chance the count lands within one vote, and the effect of a vote for one side against a vote for the other) must be named for what they are and never called p.
- 2c: Show p and break-even stakes for each race, but judge whether the trip to vote pays across the whole ballot. It pays when the races' B ÷ B\* shares sum to more than 100%.
- 3: Make the demonstration understandable to someone with no statistics training.
- 4: Let any reader reach the inputs, sources and exact formula behind any figure, through a simple mode and a full mode.
- 5: Cover as many real US races, at every level, as true sources allow.
- 6: Make the site a really nice visualization.
- 7: The model of how every number is computed is the orchestrator's job, and the maker must approve it before the site is built on it.
- 7a: Work in order (standard, data, design, build), and put the data plan to the maker once before data work starts.
- 7b: Build in the repository's starter (Preact, Vite, IBM Plex Sans, midterms style), deploy from `main` through Vercel, and let code reach `main` only through pull requests the orchestrator checks.
- 7c: Take only three things to the maker (the plan, questions the law can't settle, and money or outside-party requests), and make each specific and material.
- 8: Every number must be true, come from a named true source, and have its inputs sourced too. Computed figures must be checked and shown, and a figure not read at its source must not be presented as if it were.
- 9: Don't show a figure whose publisher hasn't licensed its use unless the maker gets the publisher's permission.
- 9a: Assume nothing. Each foundation must be sourced, or derived and checked, or flagged as a choice the maker can correct, and no option the maker might want is closed without his word.
- 10: Buy nothing and contact no outside party without the maker's word, open free accounts and keys as needed, and never commit a secret.
- 11: Make the site look and feel very like the midterms site, unless that conflicts with the end.
- 12: Work rigorously and assign each AI model where it fits best, as a separate instructions file sets out.

**4. Words and phrases that can be read more than one way**

- **"the chance it decides the outcome" / "decides".** It could mean strictly breaking or making a tie, or it could count a tie as a coin flip. The open-points section says ties count as half, and I take that to be meant. But Part A's definition never mentions ties, while the open point says "(Part A)" contains the half-tie rule, which it doesn't.
- **"Benefit … how much better … the outcome the voter chose".** Better for whom: the voter, the country, everyone affected? Principle 2 refuses to say, yet B must be a dollar figure. I read it as deliberately left open, with break-even stakes shown both ways.
- **"per person the outcome affects".** It could mean dividing the break-even stakes among all affected people, or the stakes for a typical affected person. I take the first. "Affected" is not defined (district, state, nation?).
- **"pays for itself".** Principle 2 uses it for one race, with the whole cost charged to that race. Principle 2c uses it for the whole trip, with the cost paid once. I read 2 as a yardstick per race and 2c as the actual verdict.
- **"Cost … to cast the ballot".** In dollars, but whose time is valued, at what wage, and for which voter? Not said.
- **"the standard of review".** A legal phrase for how a court examines a decision. Here I take it to mean the test in principle 2 for when a vote pays, because 1a says "what the standard of review (2) gives".
- **"the model".** Part A says it is a document. Principle 2a says "the model builds" a forecast, as if it were software, and principle 4 says "the model provides two modes". Principle 12 says "each model is assigned", which the quoted reason shows means the AI models (Sonnet, Opus, Fable). That is at least three senses of one word, though Part A promises "one meaning".
- **"measures".** Principles 3 to 6 are called "the measures", but the open points speak of "ballot measures", meaning referendums. I take these to be different things.
- **"the end".** It may mean principle 1 only, or 1 to 1c, or the site's overall purpose. "Governs all" might even mean it governs truth (8), though the reason suggests truth is the top rule.
- **"true" in "Every number … is true and comes from a true source".** A probability from a forecast isn't "true" the way a vote count is. I read it as accurately sourced, correctly computed and checked.
- **"licensed" (9).** It could mean an explicit licence, or merely not forbidden. Much public data is free to use, but the wording would seem to exclude it.
- **"no outside party is contacted" (10).** I can't tell whether downloading from an election office's website counts. I assume it means emailing, asking permission or negotiating, because free accounts are allowed.
- **"the orchestrator", "the system".** Never defined. I guess it is a lead AI agent coordinating other agents, but the text doesn't say.
- **"past races are inputs through such forecasts" and "results … are the check on p".** I can't tell what these mean in practice. One election result can't confirm or refute a probability.
- **"within one vote".** Within one vote of what? I assume of a tie.
- **"where a reader would ask" (8).** A judgement call that could be read broadly or narrowly.
- **"Real".** I think it means checkable, not just "actual races".
- **"very like" the midterms site.** The degree of similarity is open, and I haven't seen that site.
- **"once" (7a).** It could mean a single time or after something. I take it as a single approval.
- **Past versus future races.** Phrases like "historical data" and "past races" suggest only completed elections. It is not clear whether the site handles upcoming ones.

**5. Principles that seem to pull against each other**

- **Purpose against neutrality (1 against 1a, 1b, 9a).** Principle 1 starts from a conclusion the maker already holds ("in most cases does not outweigh"). Principles 1a, 1b and 9a require showing the opposite cases and assuming nothing. The text settles this through 1c and 8: truth wins, and the against-the-claim cases must be shown. But "the end governs all" could be read as putting the maker's thesis above the data.
- **Per race against whole ballot (2 and 1 against 2c).** Principles 1 and 2 test one vote "by itself" against the whole cost of the trip. Principle 2c says the cost is paid once for all the races, so races must be summed. The maker settled this by choosing "each race, and the ballot summed", so the per-race figure is a yardstick and the ballot sum is the verdict. It also quietly concedes that the "by itself" test is the harshest possible.
- **Plain against real, truthful and rigorous (3 against 2b, 2c, 4, 8).** Many caveats (look-alike quantities, three versions of break-even stakes, ballot sums, forecasts) must stay readable by a non-statistician. The text settles this only by the two modes (simple and full) and by letting truth override. It never ranks plain against real against beautiful, and 2b says the look-alikes must be named "whenever they are shown", which weighs on the simple mode.
- **Only three things go to the maker (7c) against the model going to him (7).** Principle 7 sends the model back to him for approval, which is not one of the three things in 7c or in "The maker's part after ratification". The text does not settle this. The only way out is to treat 7c as limiting questions, not approvals, and that is a stretch.
- **Broad and "no assumptions" (5, 2a against 8, 9, 9a).** Wide coverage needs forecasts the model builds itself for races with no published forecast. Principle 8 wants every number from a true source. The text settles it by requiring such forecasts to be marked as the model's own and checked, and by limiting coverage to what true sources allow.

**6. What I would ask my friend**

1. Does the site ever put a dollar figure on the benefit B for a real race, or does it show only the break-even stakes and let the reader judge? Without a B, how can it say which races pay and which don't?
2. Can the reader enter their own cost, or their own view of the stakes, or are the numbers fixed?
3. Who is the intended audience, and what should a visitor walk away believing? Are you comfortable if the data show that voting pays in many cases?
4. Are the orchestrator, the maker and the models people or AI agents? Is this law written for AI agents, and why does it include stack, workflow and model-assignment rules?
5. Does the site cover upcoming elections, or only past ones?
6. How is the cost of voting put in dollars, and how are "people affected" counted?
7. Are ballot measures in or out?
8. Why can't the words change after ratification when open points, such as the tie rule, remain? Does "rulings beside the law" amount to amending it?
9. How do I reconcile "only three things go to the maker" with the model needing his approval?
10. Can the site be seen by the public yet? The text says visitors currently have to sign in to Vercel.

**7. What seems wrong, unsupported by its own reason, or unnecessary**

- **No B, but a claim about B.** The end says the site will show where the benefit exceeds the cost. Yet principle 2 refuses to say whose welfare B counts, and nothing says how B is estimated. Only the cost-side threshold is actually specified.
- **The comparison is stacked against voting.** The maker's own quote says the claim holds "unless the cost is basically negligible". For a person already at the polls, the extra cost of one more race is close to zero. The text addresses this only partly, through the ballot sum in 2c. The mismatch of units (a vote is one race, but cost is per ballot) is built into Part A.
- **Principle 2b settles what the open points leave open.** It states flatly that the look-alikes are "twice p". But the same text lists the tie-as-half rule, which that doubling depends on, as unsettled, and the tie rule assumes ties are decided by lot, though real tie-breaking varies. Its supporting reason also cites sections of the model I can't see.
- **Weak support in 2a.** "Published forecasts exist for few races besides the presidency" has no source, which principle 8 demands, and it seems overstated for Senate, House and governor races. "Results after the election are the check on p" is unexplained.
- **A term used without a definition.** "The orchestrator" appears throughout but is not in Part A, though the text says Part A defines every term.
- **Principle 9 may be too blunt.** Public election results and wages are generally free to use. The wording as written might bar the very data the site needs, or invite overcaution.
- **Unnecessary, or not about the site.** Principles 7b and 12 govern tooling and staffing, not the demonstration, and a non-technical reader can't act on them. Principle 12 sends me to a file I can't see and defines "rigorous" only by assertion. The "Decided cases" and "The maker's part after ratification" sections largely repeat principles 2, 2c, 5, 7a, 7c and 10.
- **"Considerations, not decisions"** says it is not law yet sits inside the law, which may confuse builders about whether it binds.
- **The reasons are part of the law.** Informal quotes from the maker's speech therefore become binding text, which is risky for loose phrasing.
- **Several references go to documents I can't see.** These are the model's sections 3, 4 and 9.2, the instructions file, the design file and the frameworks research file. Some of the law's support therefore can't be checked from the text alone.
