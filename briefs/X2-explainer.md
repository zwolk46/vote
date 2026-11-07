# Brief X2: How it works, shown to a person with no statistics

*Written 2026-11-07 by the orchestrator, for X1's thread to take up once X1 has sent its first-screen options. Model: **Opus 5.5**, effort **xhigh**. Read `briefs/_COMMON.md` whole first; it is part of this brief (rule 16 above all). Opus because design turns on judgment (`PROJECT-INSTRUCTIONS.md`). It goes to X1's thread because the explainer draws on the ruler, the dots and the motion X1 has just designed (`design/DESIGN-SPEC.md`).*

## Your sub-end

**Make the page that lets a person with no statistics understand, from its visuals, how the importance of one vote and the break-even stakes are worked out, so that the maker can show it to such a person and they follow it. Build it as two or three whole versions he can pick from.**

*Why it matters:* the maker, 2026-11-07 04:06 UTC (`RULINGS.md`):

> One thing crucial to get right is the expanded explanation of how the formula or model works, but not necessarily technically. I want to be able to show it to a non technical person and because of the beautifully crafted and well thought through visuals they are able to understand. Probably a scroll animation? but you decide

It also serves law 3 (Plain: a reader with no statistics follows why p is what it is), law 4 (Full: the exact computation sits behind every number), law 6 (Beautiful) and law 9b (a surface that matters goes to him as two or three whole options).

## What a reader must come away understanding

These ideas, in this order, are the content. How they are shown is yours. Each is the model's own idea, and the model is the source (`model/MODEL.md`):
1. **The two worlds** (§1). Your ballot is counted in one world and quietly not counted in the other, and everyone else does the same in both. Importance is how likely it is that who wins differs between them.
2. **Only a tie or one vote short can change it** (§3). Every other count of the others' votes comes out the same either way.
3. **A tie counts as half** (§3; law 2b). A tie goes to a lot, which would have gone your side's way half the time anyway. The chance of the tie or the one-short count itself, the event, is twice p. It is named and never shown as p.
4. **How likely a tie is** (§3). It depends on three things: how many vote, how close the race is expected to be, and how sure that expectation is. It falls as more people vote, and it falls steeply as the race moves off even. Use the forecast curve and its height at 50-50, or the plain rule that p is about 25 × (chance of a finish between 49% and 51%) ÷ voters. Pick whichever the visual makes plain.
5. **Small races against large ones.** The stylised town race has 2,000 voters at 52-48 with a 4-point spread, and its p is 1 in 468 (§2, marked stylised). The closest presidential states of 2008 were about 1 in 10 million (§4, Gelman, Silver & Edlin). Show the gap between the two, and why it is there.
6. **The presidency has two steps** (§3, "Two stages"): your state ties, and then your state's electoral votes decide the College. Use D1's real figures if they have landed (`data/president/`); until then use the model's own illustrations, marked as such.
7. **The break-even stakes** (§2). B\* is your cost × N, where p is 1 in N. The cost is $8.87, 14 minutes at $38.00 an hour (§6). For the town race B\* is about $4,150; for a 1-in-10-million state, about $89 million. Show both readings: for you alone, and per person affected (§5).
8. **One trip pays for the whole ballot** (law 2c). Each race's share of the trip adds up.
9. **What is set aside** (law 1b): every other reason to vote. One line, once.

*Reason:* this is the chain from the question to the number. A reader who misses a link takes the number on trust, and the site exists so that a doubting reader need not (law 4).

## The form

- **A scroll-driven story is the starting idea**, since the maker suggests it and leaves it to you. One idea per step, and one visual that changes as the reader scrolls, so the reader watches the same picture become the next idea. Dots are his favourite mark (`TASTE.md`, 11-05 16:15 and 22:29), and X1's spec makes every contest a dot and every comparison a ruler of dollars. If a version works better without scroll-driven motion, it may be one of your two or three, and you say why.
- **Words are few and plain.** No formula appears in the story itself, except "your cost × N" if it reads plainly. Every technical form sits behind its step in a fold (X1's spec §2.4), for the reader who wants it. *Reason:* "not necessarily technically".
- **Motion follows `inherited/design/specs/MOTION-SPEC.md`.** Scroll-linked motion follows the scroll frame by frame, with no duration of its own. Text never travels across text. Draw the still version first: under reduced motion each step is drawn still and complete. Nothing jumps while loading. The same checks apply as for the first screen (X1's spec §6).
- **Phone first.** The maker will show it to someone on a phone as often as on a desktop.
- **Every figure is real, or marked** (law 8): the stylised town race as stylised, a sample as a sample, the model's own forecast as the model's own. Each figure's source sits in its fold.
- **Its address** is X1's spec's "How it's computed" page, or a page of its own that the spec's page links to. Propose which in your report.

## The test before he sees it

**A cold reading by a person with no statistics.** Run a Sonnet 5.5 subagent at xhigh (`PROJECT-INSTRUCTIONS.md`: cold readings of the site's words). Tell it it has a broad education and no statistics. Give it only screenshots of each step at phone width and the page's text, never this brief or the model. Ask it to explain in its own words:
- what the chance its vote matters means;
- why a tie matters and counts as half;
- why a big, lopsided race gives a smaller chance than a small, close one;
- what the break-even stakes are and where they come from;
- why the presidency's chance is so small.

**A second cold reading, by a total layperson** (the maker, 04:09 UTC). Run a second Sonnet 5.5 subagent at xhigh, told that it has no technical understanding at all. It does not know what a cost-benefit analysis is. It has never weighed a small chance of a large gain against a sure cost, and it does not know that such a weighing is how one decides whether something "pays". It reads only the same screenshots and text. Ask it the five questions above, and one more: why paying a small, sure cost for a tiny chance of a large gain can pay in one race and not in another. The page must teach this reader the weighing itself, not assume it.

Where either reader gets one wrong or cannot say, the page has failed there. Fix it, then read again with fresh subagents of both kinds, once. Put all the readings, verbatim, in `design/EXPLAINER-READINGS.md`.

*Reason:* the maker's test is a non-technical person who understands. A reader who has seen this brief or the model cannot stand in for one, so the readers see only the page. His words of 04:09: "it should also be checked by an agent specifically instructed to lack some technical understanding and as a total layperson, who doesn't even understand the fundamental correct nature of a cost-benefit analysis"

## Path and constraints

- **Branch and options.** Work on your branch. Put the options on a preview branch, with `?v=a`, `?v=b` and `?v=c` on the explainer's own page and the picker only on previews, as for the first screen.
- **Report** to the orchestrator: each option's preview link, what it gives and what it costs, the checks, and the two cold readings. The orchestrator sends them to the maker. After his pick, the chosen version goes to `main` in its own PR, without the picker.
- **Spending.** Nothing bought, and never 21st.dev's `generate`. Name any new dependency in your report with its licence and size.

## Done when

Two or three versions are on one preview branch, with the checks passed and the cold readings recorded, and you have reported to the orchestrator in at most fifteen lines. Then wait for the maker's pick through the orchestrator, merge his pick, and stop (`_COMMON.md` 14).

## Amended 2026-11-07 04:35 UTC: the visual explains; text only where truly needed

The maker, 04:32 (`RULINGS.md`): "I want as much explanation as possible to be visual, because we must operate under the default assumption that AI-written prose will hardly at all serve the purpose of convincing or explaining by itself, at least without significant refinement. And the key idea that text should not be on the page given its cluttering nature unless truly needed to serve a purpose."

This changes "Words are few and plain" above into a harder rule. *Reason:* his words; and the explainer is where prose is most tempting, since each of the nine ideas could be said in a sentence.
- **Each of the nine ideas is carried by the picture.** A step's words, if any, name what the reader is looking at; they do not explain it. If a step only works with its sentence, the step's visual is redesigned first. Examples of the kind of thing meant, not a list to keep to: the two worlds as two counts side by side that differ by one ballot; the tie as a coin; the chance of a tie as the height of the forecast curve at 50-50, falling as the crowd grows; the break-even stakes as the cost stacked N times.
- **A text ledger**, in `design/TEXT-LEDGER.md` beside the first screen's: every sentence in each version, what a reader fails without it, and why no visual carries it. A sentence with no entry is cut.
- **What stays is refined**, word by word, not left as drafted.
- **Headings stay** (the maker, 04:37): a simple heading that names what is shown, such as "Senate", "House", "U.S. Senate" or "U.S. House", is needed text. Choose its form for its place: the short form where the context already says the level, the full form where it does not. Its ledger entry is "orients". *Reason:* his words: such headings "count as text that is necessary and proper to satisfy a bona fide purpose". The cut is of prose that explains, not of the words that tell a reader where they are.
- **A third cold reading, of the visuals alone**, before the two in "The test before he sees it": a fresh layperson reader sees each step's screenshots with every sentence removed (labels, figures and axes kept) and explains the five questions as best it can. Where it fails, improve the visual, then add a word only if the visual cannot be made to carry it. Record it verbatim in `design/EXPLAINER-READINGS.md`, and report how many sentences each version has.
