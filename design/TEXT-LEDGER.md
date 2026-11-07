# Text ledger

*The maker, 2026-11-07 04:32 UTC (`RULINGS.md`): "I want as much explanation as possible to be visual, because we must operate under the default assumption that AI-written prose will hardly at all serve the purpose of convincing or explaining by itself, at least without significant refinement. And the key idea that text should not be on the page given its cluttering nature unless truly needed to serve a purpose." Briefs X1 and X2, amended 04:35: every line of text on a screen, labels and figures aside, is entered here with what a reader fails without it and why no visual can carry it; a line with no entry is cut. Headings are judged by their purpose, and often fit (the maker, 04:37 and 04:38).*

*In the code every sentence carries `data-sentence`, so the reading of the visuals alone is made by removing exactly these lines.*

## The first screen, options A and B

### What was cut, and what carries it now

| Cut | What carries it now |
|---|---|
| "$8.87 × 10,000,000. Your vote changes who wins about once in 10 million races like this, so the result must be worth 10 million times what voting costs you." (added after round 1) | The working drawn under the figure (`src/components/LeadRuler.jsx`): the cost and the figure as two marks on the one scale of dollars, the arrow between them labelled "× 10 million". A longer arrow is a longer shot. |
| "Each contest sits at the least its result must be worth to you. The more people vote, and the less close the race, the less likely your vote is to change who wins, and the further right it sits." (A, added after round 1) | The same arrow, whose length changes with the contest chosen; the field's rows, where each contest's place is its figure. |
| "48,828 sample contests, a dot for each 100; ringed, the named figures below" (A) and "…behind its lines, a dot for each 100" (B) | A key of the marks, each drawn as in the chart: a grey dot "100 sample contests", a ring "a named figure", the blue line "your cost" (A); the dot, the upright "the line's figure", the knob "what it is worth to you" (B). |
| "From $1, each mark on the scale is 1,000 times the one before." (added after round 1) | "×1,000" written on the scale between the dollar marks, where it fits. |
| B's paragraph under its heading (three sentences on shares and the trip) | The line labels "Worth to you: drag to set" and "repays 24% of the cost", the trip's bar filling segment by segment, and its figure "24% repaid" / "172% repaid: it pays". |
| B's trip note ("Drag a line… the trip pays at 100%"; "1 of 3 lines with a figure set…") | The same labels and the bar. |
| "The town race is the model's stylised example." in the sources line | The town race's own label, "An invented example, not a real race". |
| The preview note's second sentence ("The named figures come from published studies, except the town race…") | Each named figure's label ("From a study of the 2008 election") and its sources line. |
| "The grey dots are invented samples until the data lands." (the preview note; cut 11-07 when the real contests replaced the samples) | Nothing needs to: every dot is a real contest (`src/data/build-field.mjs`). The bar stays on previews only, as "Preview" and the picker. |
| A sentence that a state legislature's class C chance is its chamber's average district's, and that like-race chances are averages (the orchestrator, 09:31) | The same dot, lighter, stacked above the contests' own; the key's "an average race's chance, not its own". |
| "This route's back-test shows more near-even finishes than it forecast, so p may be low" (the House's note on this site's own model's p; the governors' and the Senate's notes are out, on the orchestrator's ruling of 11:05 and M2's numbers, 11:16) | A dashed arrow toward where the figure may lie: beside a named figure whose p carries it, its list entry and B's line, and after the drawn working's ring; in a row's count, the arrow with how many of its contests carry it ("3,369 · ⇠ 2,514"); the key's "may be lower". The note itself is in the chance's fold, as a source. |
| "No figure yet" with "the data give no population for … yet", in the figure's place, per person (cut 11-07: text that serves no purpose, the orchestrator reading the maker's 04:32) | Every named figure now has its population (the state legislative districts' from D2's data/population/, 12:01). A dot, or a figure, with none fades in that reading without words, and a figure cannot then be chosen; the lead is then the highest chance's. The words "no population in the data yet" are cut too (the orchestrator, 12:01). |
| "Worth to you: drag to set" under every line of B (the same words five times; the orchestrator, 11:05) | The words once, under the first line, until a stake is set; the hollow knob on each track is the rest. |
| The figure's label "is the least the result must be worth to you" | Refined to a label: "the least the result must be worth to you". |

### What stays

| Line | Option | Kind | What a reader fails without it | Why no visual carries it |
|---|---|---|---|---|
| "How much would the outcome have to be worth for one vote to pay?" | A | heading, the site's question | Does not know what the figure answers. Every round-1 reader quoted it back as the page's claim. | It is the question itself. |
| "One trip to vote, every contest on the ballot" | B | heading | Does not know that the lines are one ballot and the trip one cost (round 1: "I didn't know what 'trip' meant for a long time"). | It names what the lines are. |
| "Only the chance of changing who wins is weighed here. Every other reason to vote, like duty or having your say, is set aside." | A, B | two sentences | Takes the figure for the whole case for voting (law 1b: what is set aside is said, once). A round-1 layperson asked what the other reasons are, hence the two named. | What is left out of a picture cannot be drawn. |
| The sources line (the forecasters, the counts' sources, the Census Bureau, the date read) | A, B | citations | Cannot check a figure (law 4). | A source is a name. |
| Each fold's sources and the tie (behind the cost and the chance, closed until tapped): 4 sentences on the cost; on the chance, its forecast and count, its population or that there is none, the back-test's note where there is one, and the tie rule | A, B | sentences behind a fold | Cannot check the cost or the chance (law 4); the tie counts as half (law 2b). | They are sources and a rule, read only by a reader who asks. |

Labels kept, as labels: the contest's name and its year and why it is named ("2024 · the highest chance of any state", "2024 · the lowest of 33"; Nevada is named by its chance, not as the closest state, which it was not: the orchestrator, 11:05); "the least the result must be worth to you"; "Your cost of voting" with "14 minutes at the polls, at $38 an hour" (every round-1 reader asked what the $8.87 was made of); "Chance your ballot changes who wins"; "To you" / "To each person"; the key; the rows' names and counts, and "189 past $1T ›" where a row's contests run past the scale's end; "96,801 contests, 1969–2024"; the scale; the named figures' names and their year and reason; per person, "shared by 340 million people in the United States", ("shared by 12,687 people in the district"); B's "Highest chance / Average voter / Lowest chance", the line's place and year, "the lowest of 33", "Worth to you: drag to set" once, "repays 24% of the cost", "The trip".

### Sentences on the screen

- **A:** 3 (the heading's question, the two on what is set aside), plus the citations line. Behind folds: the sources of the cost and the chance.
- **B:** 2 (the two on what is set aside), plus the citations line. Behind folds: the same.
