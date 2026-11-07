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
| The figure's label "is the least the result must be worth to you" | Refined to a label: "the least the result must be worth to you". |

### What stays

| Line | Option | Kind | What a reader fails without it | Why no visual carries it |
|---|---|---|---|---|
| "The grey dots are invented samples until the data lands." | A, B | sentence | Takes 48,828 invented contests for real ones (law 8: a sample is marked as a sample). | A mark cannot say that it is invented. |
| "How much would the outcome have to be worth for one vote to pay?" | A | heading, the site's question | Does not know what the figure answers. Every round-1 reader quoted it back as the page's claim. | It is the question itself. |
| "One trip to vote, every contest on the ballot" | B | heading | Does not know that the lines are one ballot and the trip one cost (round 1: "I didn't know what 'trip' meant for a long time"). | It names what the lines are. |
| "Only the chance of changing who wins is weighed here. Every other reason to vote, like duty or having your say, is set aside." | A, B | two sentences | Takes the figure for the whole case for voting (law 1b: what is set aside is said, once). A round-1 layperson asked what the other reasons are, hence the two named. | What is left out of a picture cannot be drawn. |
| The sources line (two citations and the date read) | A, B | citations | Cannot check a figure (law 4). | A source is a name. |
| Each fold's sources and the tie (behind the cost and the chance, closed until tapped): 4 sentences on the cost, 1 to 2 on the chance, plus the tie rule | A, B | sentences behind a fold | Cannot check the cost or the chance (law 4); the tie counts as half (law 2b). | They are sources and a rule, read only by a reader who asks. |

Labels kept, as labels: the contest's name and "From a study of the 2008 election"; "the least the result must be worth to you"; "Your cost of voting" with "14 minutes at the polls, at $38 an hour" (every round-1 reader asked what the $8.87 was made of); "Chance your ballot changes who wins"; "To you" / "To each person"; the key; the rows' names and counts; the scale; the named figures' names and their "From a study of…" or "An invented example, not a real race"; per person, "shared by 4,000 people (a round figure)"; B's "Where you vote for president", "No figure yet", "Its figure comes with the data", "Worth to you: drag to set", "repays 24% of the cost", "The trip".

### Sentences on the screen

- **A:** 4 (the preview note, the heading's question, the two on what is set aside), plus the citations line. Behind folds: the sources of the cost and the chance.
- **B:** 3 (the preview note and the two on what is set aside), plus the citations line. Behind folds: the same.

## The explainer, "How the figure is worked out", versions A and B

The page was written to the amended brief from its first build. Each of its 24 steps carries a heading, the step's one figure, and a line naming what is shown; a key under the picture names its marks. Nothing on it explains in sentences what a picture shows, so no sentence was cut. The changes to its words after each reading are recorded in `design/EXPLAINER-READINGS.md`.

### What stays

| Line | Kind | What a reader fails without it | Why no visual carries it |
|---|---|---|---|
| "Only the chance of changing who wins is weighed here. Every other reason to vote, like duty or having your say, is set aside." (A: after the last step; B: on the last step) | two sentences | Takes the figure for the whole case for voting (law 1b: what is set aside is said, once; brief X2, idea 9, "in one line"). | What is left out of a picture cannot be drawn. |
| Each step's "Source", closed until tapped: nine notes, 21 sentences in all (the town race 1; the tie rule 2; the model's curve 3; the closest states of 2008 1; Pennsylvania 2024 1; the cost 2; what it is worth to you 2; counting everyone 2; the ballot's example 7) | sentences behind a fold | Cannot check a figure (law 4). Without the tie rule's note, cannot check that a tie counts as half and the event is a tie or one short (law 2b). Round 1's readers 2 and 3 took the cost's makings, the 19 in 100 and the House's 1 in 180,000 from these notes. | A source is a name and a date. The notes are read only by a reader who asks. |
| The 24 headings ("Your ballot, counted and not", "Where one ballot changes who wins", "How likely a tie is", "More voters", "Less sure", "The presidency, step one: your state", "In 468 runs, 468 trips", "Counting what it is worth to everyone", "One trip votes in every race"…) | headings | Does not know which of the nine ideas the picture is at, or which race it is. Round 1's reader 3 named a step by its heading ("'Less sure' (step 10)"). | They name the step, as the maker's ruling of 04:37 and 04:38 allows. |

Labels kept, as labels: each step's figure ("Same winner", "Half + half", "1 in 468", "468 × $8.87 = $4,150", "Does not pay", "It pays: $9.36"…) and its sub ("a town race of 2,000 voters (stylised)", "a coin toss against a loss", "a trip: 14 minutes at the polls, at $38 an hour", "worth $1,000 to you (an example)"…); the keys of marks; the labels drawn in the pictures (counts, "Counted" and "Not counted", "your side's lead, not counting you", "how likely", "your side's share of the vote, as forecast", the seesaws' dollars, "level: they weigh the same", the blocks' dollars).

### Sentences on the page

- **A:** 2 (on what is set aside), after the last step. Behind folds: 21, in nine notes.
- **B:** 2 (on what is set aside), on the last step. Behind folds: the same 21.

The two versions have the same words; they differ in pace and motion only.
