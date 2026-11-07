# Cold reading A of law draft 1

*2026-11-07, a Sonnet 5.5 subagent at xhigh, in the role of a web designer and developer hired to build the site, with no statistics. It saw only the text of `law/LAW-DRAFT-1.md` and seven questions (what the site is for; its first screen; what each principle requires; words with two readings; principles in conflict; what it would ask; what seems wrong). Its response, verbatim:*

---

COLD READING A: my first response, from the text alone.

1. What the site is for and whom it serves

The site is a visual demonstration made for its maker, Zach, to show why he says one person's vote usually does not pay for itself: its expected benefit, taken alone, is usually smaller than what it costs the voter to cast it. For real US races at every level, it shows the chance that one ballot decides the winner (p) and the "break-even stakes" (B*, the cost divided by p). B* is how much the result would have to be worth for that one vote to be worth its cost. It shows this for every race, including the races where a vote does pay for itself. It serves any visitor, with no statistics training, who wants to see this and check it for themselves. It deliberately does not say whether anyone should vote.

2. The first screen, and what I would leave off

The text never describes the first screen, so what follows is my inference. Principle 2 says to lead with B*, so I would open on one race. It would show B* as the big number, in plain words and with its source named beside it (principle 8). Under it would go what B* means for the voter alone and per person the outcome affects. The picture would put the tiny chance of deciding the race against the large stakes needed. One plain line would say what is held fixed: only whether this ballot changes the winner, with duty, expression and influence on others set aside (1b). There would be a way to pick another race, a light/dark choice, and a visible way into the full computation. I am unsure whether the ballot-sum view (2c) or a single race comes first.

I would leave off:
- any advice or verdict about whether to vote, and any sentence saying voting is pointless or bad;
- any dollar value of B that I or the site invented, since the site "does not choose whose welfare B counts";
- any figure without a named true source, and any figure whose publisher has not licensed its use;
- the two "twice p" quantities presented as p;
- ballot measures (the text leaves them open);
- shadows, glows and decorative motion, and party-coded politics, which the text lists only as the maker's taste;
- analytics, trackers, third-party embeds and anything paid or needing an outside party (principle 10);
- analogies or comparisons from outside the sourced data, such as lottery odds, since they would be unsourced numbers.

3. What each principle requires

Principle 1: Build the site as a demonstration of the maker's claim that one vote's expected benefit alone usually falls short of its cost, shown race by race for real US races, saying plainly which cases come out each way.

Principle 1a: Show the standard of review for every race I cover, including races where a vote pays for itself, and never hide those cases.

Principle 1b: Never tell anyone whether to vote and never call public voting bad. State on the site that duty, expression and influence on others are held fixed by the definition of importance.

Principle 1c: When plainness, realness, breadth and beauty conflict, truth wins over all of them, and the site's end wins over everything.

Principle 2: For each race, lead with B* and put beside it what B* means for the voter alone and per affected person, without picking whose welfare counts in B.

Principle 2a: Show p as the chance before the election under a named forecast, either a published one or one the model builds from pre-election information and labels as its own. Use results afterward only as a check.

Principle 2b: Never label anything p except p. When showing the "within one vote" chance or the "vote for one side against a vote for the other" effect, name each one clearly and say that each is twice p.

Principle 2c: Show each race's own p and B*, and also a ballot-level view where the races' shares of B divided by B* are added up, with the trip paying when the total passes 100%.

Principle 3: Write and design every explanation so that someone with no statistics training can follow what is measured, the chance, the break-even stakes and what they mean.

Principle 4: Behind every figure, give a path to its inputs, their sources and its exact formula, using a simple mode and a full mode.

Principle 5: Cover as many real US races as true sources allow, at every level from president (state by state) down to local offices, so a reader sees p grow as races shrink.

Principle 6: Make the site a really nice visualization.

Principle 7: Do not build number-bearing parts of the site on the model until the maker has approved it. The model document defines how every number is computed.

Principle 7a: Work in the order of standard of review, then data, then design, then build, and expect the plan to go to the maker once before data work starts.

Principle 7b: Build in the repository's Preact, Vite and IBM Plex Sans starter in the midterms site's style, deploy through Vercel from main, and get code to main only through pull requests the orchestrator checks.

Principle 7c: Send nothing to the maker myself. Only the plan, questions the law cannot settle, and requests for his word on money or outside parties go to him, and each question must be specific and bear materially on the end.

Principle 8: Show only true numbers from true sources, name the source on the page, cover every input to a formula too, check and show the computation of anything computed, and never present a figure as read at its source when it was not.

Principle 9: Do not show a figure whose publisher has not licensed its use unless the maker has obtained the publisher's leave.

Principle 9a: Assume nothing the site rests on. Each such thing must come from a true source, be derived and checked, or be marked as a choice the maker can correct, and I must not close off any option he might want.

Principle 10: Buy nothing, contact no outside party without the maker's word, open free accounts and keys as needed, and never commit a secret.

Principle 11: Make the site look and feel very like the midterms site, except where that would work against the site's end.

Principle 12: Work rigorously, and assign each model where it is most reasonable, as PROJECT-INSTRUCTIONS.md sets out. This is process, and I do not have that file.

4. Words and phrases I could read more than one way

"Importance" and "the chance it decides the outcome". The site's name is "vote-importance", and "importance" in everyday speech means general significance. The text gives it one narrow meaning: the chance that the winner differs with versus without this ballot. I would act on the narrow meaning. In the simple view I would label it "the chance your vote decides the race" rather than "importance", because a visitor will read the everyday word as a claim about worth.

"president (state by state)" and "who wins differs". For the presidency, "who wins" could mean the winner of the state's contest or the winner of the presidency. A race is defined as "decided by the ballots cast", which fits a state contest, but B is the worth of the outcome, which only makes sense for the presidency. I would provisionally treat the outcome as the presidency, because nobody values a state's winner for itself. I cannot be sure this is meant, and I would not publish presidential figures until someone confirms.

"the other outcome" in the definition of Benefit. This reads as two-way. Many races have more than two candidates, and some have primaries, runoffs or ranked choice. I would act on a plain two-way reading (my chosen candidate winning versus the main rival winning) for now, and ask.

"what it costs the voter" (Cost, C). Which voter: a typical one, the reader, or a range? B* = C ÷ p needs a number for C. I would build a reader-adjustable C with a sourced default that is marked as a choice (9a), because the text neither supplies nor forbids it.

"what B* means for the voter alone and what it means per person the outcome affects". "The voter alone" presumably means the plain B*. "Per person affected" presumably means B* divided by the number of people the outcome affects, but the text does not say so. Who counts as affected (residents, voters, everyone nationally for a House seat) is also unstated. I would divide by the population the office governs, from a statistics agency, and mark it as a choice.

"the ballot summed" and "the races' shares B ÷ B*". Which ballot? A real ballot for a given address, a typical one, or one the reader builds? It also needs a B for each race, which the site is told not to choose. I would let the reader build a ballot and enter or see B, but this is a guess.

"A true source": "the party that counted or measured a figure, read where that party publishes it". The text does not say whether a university or news compilation of official results counts. I would act on the strict reading and use only the authority's own publication, and hold back anything else until told.

Principle 8's last sentence ("Where a true source cannot be read, the record says where the figure was read instead, and the site does not present it as read at its source"). This seems to allow showing a figure read elsewhere, while the first sentence says every number comes from a true source. I would act on the first sentence and not show such figures until told. Also, "the record" is not defined.

"has not licensed its use". It could mean "has not expressly granted a licence" or "has forbidden use". Most government election pages state no licence. The strict reading would remove nearly everything, and the loose reading risks the text's intent. I would treat official government results as usable and require explicit permission for private compilations and forecasters' products, but I would ask.

"a forecast ... published" versus "the model builds ... as its own". A forecaster's published forecast may itself be unlicensed (9). Then the model's own forecast would carry most races. I would show model-built forecasts clearly labelled as the model's own.

"two modes" and "The model provides two modes". The model is described as a document, so it cannot provide modes. I would read it as a simple/full toggle on the site, with the content of each defined in the model, and make the simple view the default.

"Plain" ("a reader with no training in statistics can follow"). It sets no test or reading level. I would write for a general adult reader, use symbols like p and B* only in full mode, and have a non-specialist read it. It is unclear whether "written p" means the symbol appears on the site.

"Beautiful" and "a really nice visualization". The text does not say what is being visualised or how nice is nice enough. I would treat it as a call to make real design effort with a clear central picture, but I cannot check it against anything.

"very like the midterms site". How much is "very like", and does it include layout or only style? I have not seen that site.

"The model" has two senses. Part A means the document that says how p, B* and C are computed. Principle 12 and its reason mean AI models (Sonnet, Opus, Fable). I would take principle 12 as not about the site.

"outside party" (10). It does not say whether Google Fonts, a CDN, or an election authority's server counts. I would self-host fonts and assets, include no analytics or embeds, and treat reading a public web page as not contact.

"Considerations, not decisions" (the maker's taste). The text says this is "evidence of what he likes, not law". I would follow it as default style, since 11 pulls the same way, and yield if it conflicts with the end.

5. Principles that pull against each other

Principle 1 against 1a, 1b, 1c. Principle 1 exists "so that the maker can show why he says" voting does not matter, which sounds like the conclusion is fixed. Yet the site must show every race neutrally, including ones against him, and may not say whether anyone should vote. I would settle it with 1c and 1a. The site presents the numbers and the break-even comparison, makes no claim beyond them, and states the narrow thing measured. If the data show a vote paying for itself in a case, the site shows that.

Principle 2 against 2c. The site "does not choose whose welfare B counts", but the ballot sum needs B for each race. I would settle it by showing B* alone for each race and letting the reader supply B in the ballot view. The site would never pick a B itself. That uses 9a, which says to mark such things as choices instead of assuming them.

Principle 2a against 9, with 8. Principle 2a prefers a published forecast, but principle 9 may bar showing it for lack of a licence. Then the model's own forecast must carry the race, but principle 8 wants every number from a true source. I would settle it with 8's own text. A computed figure is allowed if it is checked and its computation is shown. Its inputs (past results) come from true sources, and the forecast is marked as the model's own.

Principle 3 against 4 and 2b. Plain explanation and full realness, plus the extra named quantities from 2b, could clutter the page. The simple/full modes are the intended answer. Simple mode shows one number and a plain sentence. The extra quantities and formulas appear only in full mode, and 2b's naming rule applies wherever they do appear.

Principle 5 against 8 and 9. Breadth is limited by "as true sources allow", and 1c puts truth first, so fewer races is the right answer when sources or licences fall short.

Principle 6 and 11 against the end. Principle 11 already says the end wins. I would keep the midterms look, but draw a new chart if the demonstration needs one.

Principle 9a ("No option the maker might want is closed without his word") against 7c (only three things go to the maker). Every design choice closes some option. I would settle it by choosing reversible defaults, marking them as choices, and asking only when a choice bears materially on the end.

6. What I would have to ask before starting

- Is the model (model/MODEL-DRAFT-3.md) approved, and where are the data? Principle 7 says number-bearing work waits for approval. I cannot compute p or B* myself, so I need to know if I receive data files, and in what form.
- What is my part and which stage are we in: design only, or build as well? Principle 7a puts design after the data work.
- Who is "the orchestrator", and how do I reach them? I cannot tell whether it is a person or a program, and the text names it without defining it.
- For the presidency, is the outcome the state's winner or the presidency?
- What is C: one default, a reader input, or a range, and from which source?
- How are "per person the outcome affects" and the ballot sum to be computed, and who supplies B in the ballot view?
- What does "simple mode" and "full mode" contain, and which is the default?
- What copy do I write? There is no wording, headline, or race list, and I do not know how readers find a race (search, map, list).
- Are ballot measures in or out, and what is the address readers will use, and when is the Vercel sign-in lifted?
- Is a model-built forecast shown at the same prominence as a published one?
- May I see the midterms site and `inherited/DESIGN.md`? Principle 11 depends on them.
- What are the mobile, accessibility and browser requirements? The text is silent.

7. What seems wrong, unsupported, or unnecessary

- Part A's definition of importance has no tie rule, but the Open points section says "importance counts a tie as half (Part A)". The half-tie rule is not in Part A, and it assumes ties are settled by lot, which is not true of every race.
- In 2a, the reason says "Published forecasts exist for few races besides the presidency". This is a factual claim with no source, which principle 8 would normally demand. If it is wrong, it changes how many races depend on the model's own forecast.
- In 2a, "Results after the election are the check on p" is unclear. A single result cannot confirm or refute a probability, so I do not know what check is meant.
- In 2b, "Each is twice p" and "differ ... by a factor of two" rest on "model §3 and §4", which I cannot see. The reason does not carry itself.
- The reasons for 6, 11 and 12 mostly repeat the maker's words and give no guidance for a case the words did not foresee, which the law itself says the reasons are for.
- Principles 7, 7a, 7c and 12, part of 7b, and the "maker's part after ratification" section are about how the agents work, not what the site is. They repeat each other (7c, 10 and the closing section all list what goes to the maker), and they would be easier to use in an operations document. The "Decided cases" section also repeats reasons already given under 2, 2c and 5.
- Principle 10 says "Free accounts and keys are opened as needed" but also "no outside party is contacted without the maker's word". Opening an account is contacting a party, so the two sentences need a line drawn between them.
- Principle 8 says "a figure the model computes is checked", but by whom and how is not said.
- "Importance" is an ordinary word with a very narrow meaning, and the site's name and the maker's phrase "voting doesn't matter" invite the wider reading. Principle 1b guards against this, but the name itself works against it.

Note: I opened only the task file, as instructed, and no other file.
