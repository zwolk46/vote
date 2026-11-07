# DESIGN-SPEC: how the vote-importance site looks, reads and moves

*X1, version 1, 2026-11-07. A proposal for the orchestrator: nothing here is decided by X1 (`briefs/_COMMON.md` 3). Every rule carries its reason. Read with `LAW.md`, `model/MODEL.md`, `plan/PLAN.md` and the design guidance it builds on, `inherited/design/` (README, `TASTE.md`, `specs/DESIGN-SPEC.md` written "M-spec s.N" here, `specs/MOTION-SPEC.md` written "M-motion s.N"). Where this spec and the law differ, the law governs (law 6).*

*The first screen's two or three candidates are built on the preview branch and described in §5; the maker picks one (law 9b).*

---

## 0. What the site has to do on a screen

The law gives the page four jobs at once (law 1c): **plain** (3), **full** (4), **broad** (5), **beautiful** (6), with truth (8) governing each. In design terms that is:

1. **Lead with B\*, the break-even stakes** (law 2): "how much the outcome would have to be worth for one vote to pay", in dollars, for a real contest, with its source.
2. **Make the scale felt.** B\* runs from thousands of dollars in a town race to billions in a safe state: about six orders of magnitude between figures already sourced in the model (§2, §4), more once the data lands. A reader with no statistics must feel that distance, not read it.
3. **Make the breadth felt** (the maker, 03:13: "the amount of data that's available [...] for someone to say, wow"). Tens of thousands of contests, every level, as far back as standardized sources go. The design shows that volume, not a handful of cases.
4. **Show the cases against the claim** (law 1a): the contests where B\* is lowest are on the same page, at the same weight, as the highest.
5. **Say the one question** (law 1b): one vote's effect on who wins, against its cost; every other reason to vote is set aside.
6. **Behind every figure, its computation and source** (law 4, 8), without burying the page.

A design that is beautiful and misses 2b (the tie as half, the event at twice p) or 1a fails the law however it looks (brief X1).

---

## 1. What carries over from midterms, as it stands

Each of these stands here as the maker's default (`inherited/design/README.md`, the rule). They are not restated; a builder reads them at their source.

| From | What | Note for this site |
|---|---|---|
| M-spec s.0 | the faults: text that all looks alike, figures inside sentences, every row one shape, uniform separation, repeated words | applies to every page |
| M-spec R1 | text only if it must be read; the cover test | the 1b line passes the test (a reader who misses it takes p as an answer to a question it does not ask); so does the preview's sample banner |
| M-spec R2 | five sizes, two weights (Plex Sans 400 and 600) | plus one display size for the lead figure, §2.1 |
| M-spec R3 | figures in tabular numerals on a shared right edge, never in a sentence | in a list of contests the B\* column is the right edge |
| M-spec R4 | colour carries meaning only | no party colours: this site's data has no sides (§2.10) |
| M-spec R5 | separation without boxes; space 4, 8, 16, 24, 40, 64; one strong rule opens a list, hairlines between rows; no shadows | as it stands |
| M-spec R6, R7, R8 | a heading said once; one source line per section; statuses in short words | R7 is extended for figures, §2.5 |
| M-spec R9, s.19 | one icon set, Phosphor Regular, every glyph named; no key legends; every component cites the example it is drawn from | the first screen uses no glyph at all |
| M-spec s.15 | Appearance: System, Light, Dark, remembered on the device (`vote.theme`), set before the first paint, switched at once with no fade | the hook is already in `index.html` |
| M-spec s.17 | a segmented control: one object, one moving part (the indicator, 300 ms on the spring), equal columns, arrows move the choice | built here within the principles (§4), the maker's 02:45 correction |
| M-spec s.12, s.26 | page states and skeletons | little waits here: everything ships from the repository (the maker, 03:13: "We don't need live data at all"). A skeleton only where a contest set is fetched as its own file (§3) |
| M-spec s.23 | the check includes the case that does not fit | §6 |
| M-motion s.1, 2, 4, 5, 6 | motion only on a real event, per surface; the tokens; transform and opacity only; interruptible; no stagger; text never travels across text; reduced motion written first; the never list | the new surfaces are in §4 |
| `TASTE.md` | his rulings, as defaults | the ones that bear most here: dots that glide between states ("the transitions like with dots were super super nice", 11-05 16:15); creative, data-faithful transformations (the bar to semicircle, 13:50); the first page "visually the most excellent page" (18:32); no jumping (18:28); visual keys over paragraphs (14:21) |
| `inherited/design/code/` | `Boundary.jsx`, `fitheads.js`, `motion.js` (tokens and `play`, without `live.js` and `navstate.js`), `fitcheck.cjs` and `checks.cjs` as models for the checks | adapted copies live in `src/lib/` and `design/checks/` |

---

## 2. What this site needs that midterms did not

### 2.1 The scale: one ruler of dollars, each step ten times the last

**Rule.** Every comparison of B\* across contests is drawn on **one logarithmic scale of dollars**, where each power of ten takes the same length. Ticks sit at powers of ten and are labelled in words a reader says: "$10", "$1,000", "$1 million", "$1 billion". No scientific notation, anywhere. *Reason:* the figures already sourced run from $4,150 (a town race, stylised) to about $9 billion (the safest states of 2008), a ratio of two million; on a linear scale every contest but the top one is a dot at zero. A log scale is the only drawing in which all of them, and the reader's own cost, are visible at once. The midterms "Closest" chart already drew a log scale of margins (10, 1, 0.1, tie) and the maker praised its dots (11-05 18:57).

**The reader's cost is on the same ruler.** C (about $9, §2.8) is a mark on the scale like any contest. B\* = C × N, where p is 1 in N, so on the log scale **the distance from the cost to a contest is exactly the size of N**: the length a reader sees between "your cost" and "the presidency" is the length of "1 in 10 million". *Reason:* this is the formula drawn, not decorated (law 3, 4): the picture and the arithmetic are the same thing.

**Figures in words.** Money: under $10 with cents ($8.87); under $1,000 in whole dollars; under $1 million to three significant figures with commas ($4,150; $180,000); from $1 million, two significant figures and the word ($1.6 million, $89 million, $530 million, $8.9 billion). Chances: "1 in 468", "1 in 180,000", "1 in 10 million", "1 in a billion"; never a percentage below 1% and never a decimal like 0.0000001. *Reason:* R3, and the reader the law names (1, 3): no training in statistics. "1 in a billion" is how Gelman, Silver and Edlin put it, and how people say it.

**The lead figure** takes one size above R2's: **`--t-display`, 52 px desktop, 40 px phone, 600, tabular**, used once per page, for the B\* the page leads with. *Reason:* law 2 says the page leads with B\*; at `--t-fig` (32/26) the lead figure is the same size as every other figure on a page that has many, so nothing leads (M-spec s.0's first fault). One clearly larger level keeps R2's reason (each step reads as a rank).

### 2.2 The breadth: every contest is one dot

**Rule.** Across the site **a contest is a dot**: the same mark, the same size class, wherever contests are shown together. A set of contests is a field of dots placed by their B\* on the ruler (§2.1), in rows by level (president by state, Senate, governor, House, state legislature, local, ballot measures). Tens of thousands of dots are drawn, all of them, on a canvas; where they pile up, the pile is the density. Counts sit at the row's end, in figures. *Reason:* the maker's 03:13 ruling (the amount of data is itself a cool aspect); dots are his favourite mark ("because they were dots I think it's easy enough for you to control them well through code", 11-05 22:29), and a unit chart shows volume without a word. A table of tens of thousands of rows shows a scroll bar, not a volume.

- **A contest keeps its dot.** Where a page opens one contest from a field, its dot is the thing that moves (navigation, M-motion's `nav-in`), so the reader sees which of the many it was.
- **A dot is never a sample unless marked.** Until the data lands, the fields on the preview are sample contests (invented sizes and forecasts run through the model's formula, `src/data/sample.js`), drawn in the same mark and **labelled as a sample in the banner and the row counts**. The real figures the model already holds are drawn as labelled dots with a ring. *Reason:* the midterms rule that nothing reads as a real figure unless it is one (`TASTE.md`; the fixture banner, M-spec R1), and the brief's amendment of 03:13.

### 2.3 The ballot: one trip, the shares add up

A ballot casts every contest on it for one trip (law 2c). Wherever a ballot is shown:
- each contest is a row with **its own B\*** at the right edge (R3);
- the reader may set **what each outcome is worth to them** (B); the row then shows its **share of the trip, B ÷ B\***, as a percentage;
- the shares are drawn as **segments of one track, the trip**, which fills toward 100%; past 100% the trip pays, and the track says so in words ("Pays", not a colour alone).

The site sets **no B by default** (law 2c: "the site chooses no B"); a row with no stake shows its B\* and an empty share. *Reason:* law 2c and its reason, and the maker's ruling of 02:32.

### 2.4 Two modes, and the figure that opens to its computation

- **Simple mode** (model §8): three facts in (how many vote, how close it is expected to be, how sure the forecast is), two numbers out (p and B\*). It lives on its own page (§3, "Try a race") and as the first fold under a contest.
- **Full mode**: every contest's inputs, each with its source and date, the forecast named, the stages, and the exact computation. It is the contest's own page.
- **On any page, a figure a reader would doubt opens in place** to its computation: the formula with the figures in it ("$8.87 × 10,000,000 = $89 million"), each input's source, and the convention (§2.6). It opens under the figure, at once, its contents with `reveal` (160 ms, opacity), and closes at once. Not a drawer: a fold in the page. *Reason:* law 4 (behind every figure, the full computation) without leaving the page; M-spec s.9 says a drawer only where one is needed, and a fold keeps the figure and its arithmetic in one view.

**The receipt.** The plainest computation, shown with the lead figure on the first screen: `your cost × N = B*`, three figures on a shared right edge. *Reason:* the formula a person can say aloud is the one the reader can check (law 3, 4), and multiplication reads more easily than "C ÷ p".

### 2.5 Sources and dates, without burying the page

- **One source line per section** (R7), 12 px, `--faint`, naming the sources of the figures in it and their dates.
- **Every figure's own source** in its fold (§2.4): who counted or computed it, where it is published, the period it covers, and a mark when it is any of these, in words: **"stylised, not a real race"**, **"an average over 16,577 races"**, **"the model's own forecast"**, **"read at second hand, in …"**, **"sample"**. *Reason:* law 8 (the page says when a figure is second-hand, and where); the brief (stylised and sample figures marked plainly).
- **Copyright** (law 9): a published figure is quoted with its source, as a study's findings are; a publisher's tables are not reproduced. The Economist's 2020 figures are not shown until the maker rules (model §4). The candidates on the preview use none of them.

### 2.6 The tie counted as half, and the event at twice p

Wherever p is shown, its fold says, in these words or shorter: **"A tie counts as half: a lot would have gone your way half the time anyway. The chance the count without you lands within one vote is twice this: 1 in 5 million."** Where a published figure's convention is in doubt, its fold says that too ("If the authors meant an exact tie, p is half this, and the stakes double", model §4). The event is never drawn or labelled as p. *Reason:* law 2b and the open point on the tie; published figures differ by a factor of two on this alone.

### 2.7 The one question

Under the lead block of the first screen, and at the head of the method page, one line: **"This weighs one vote's effect on who wins against what it costs. Every other reason to vote is set aside."** Not on every page: once per page a stranger may land on. *Reason:* law 1b; R1 (said once).

### 2.8 The reader's cost

- **The default**: 14 minutes, the median time at the polling place in 2016 (Chen, Haggag, Pope and Rohla, arXiv 1909.00024), at $38.00 an hour, average hourly earnings of private employees, October 2026, preliminary (BLS series CES0500000003): **$8.87**. The fold gives the mean, 19 minutes ($12.03), and says the time excludes travel. *Reason:* model §6 gives the range $8.87 to $12.03; the lower end is the one that makes B\* lowest, which is the cautious choice for a page whose claim is that B\* is high (law 1a, 9a). **This is a choice open to the orchestrator** (§7).
- **The control**: the cost figure is a button; it opens in place to two fields, **minutes** and **dollars an hour**, and their product. Any change moves every dot on the ruler together (§4, V2), because B\* = C × N moves every contest by the same factor.
- **By mail**: a cost case of its own (model §6), with no measured figure yet; not on the first screen.

### 2.9 The two readings of B\*

A segmented control, **"To you" · "To each person"**, wherever B\* is the lead (law 2). "To you" shows B\*. "To each person" shows B\* ÷ the population the office serves (the country for the presidency, the state, the district, the town). Switching glides every dot to its new place (§4, V3), and the lead figure changes at once. The populations come from the Census Bureau in the data stage; **on the preview they are samples, and say so**. *Reason:* law 2 and the 00:24 ruling ("lead with break-even, show both"). The per-person reading is where the claim is weakest (pennies to dollars a person in a close presidential state); it is shown at the same weight (law 1a).

### 2.10 Colour

- The starter's neutral tokens (`--bg` warm off-white, `--fg`, `--muted`, `--faint`, `--line`, `--line-strong`, `--panel`, `--track`), light and dark, as midterms.
- **No party colours on any page.** Levels are told apart by their row, not by hue. *Reason:* the data has no sides; the maker, 11-05 20:58: "it's just a data displayer, it's not right or left".
- **One accent, `--accent`**, the logo's navy (#1f3a6e light; #8fb0ea dark, where navy on the dark page would vanish): it marks **you**, the reader's own cost and the contest in focus, and nothing else. *Reason:* R4, colour carries one meaning; the maker's brand direction "dark navy, red and white" (11-03 14:23).
- **`--dot`**: the contests' ink, `--fg` at a low alpha so density reads as darkness.
- The **warn** colour marks only the preview's sample banner.

### 2.11 The name and the mark (a proposal; the maker's to name)

The starter's title is **"One vote"**. The proposed mark is a 22 px navy tile, 5.5 px corners, holding a 3 × 3 grid of white dots with one red: one vote among many, in the site's own mark (the dot). Red, white and navy, as the midterms flag tile, so the two sites read as siblings (law 11), and no colour leans either way. The wordmark is "One" at 600 and "vote" at 400 in `--muted`, at the type's own word space (his midterms rulings on the logo, 11-04 21:58, 11-02 23:54). The mark's white is solid white in both schemes (11-04 21:59).

---

## 3. The pages (a proposal for the orchestrator)

| Page | What it is for | What leads | Notes |
|---|---|---|---|
| **Home** `/` | the claim, met by a stranger | the first screen (§5), then a way into each page below | the 1b line here |
| **Every contest** `/contests` | the breadth: every contest on the ruler, filtered by level, year and state | the field of dots (§2.2) with the counts | the "wow" page; a contest's dot opens its page |
| **A contest** `/c/<id>` | full mode for one contest | its B\*, both readings | p with its forecast named and its stages; the event named; inputs, sources, the formula; the record of like contests as the check |
| **Your ballot** `/ballot` | the trip, summed (law 2c) | the trip track (§2.3) | by state and year; later by address (law, considerations) |
| **Try a race** `/try` | simple mode (model §8) | the two numbers | three facts in; the forecast curve with the one-vote slice; what makes p larger or smaller (law 3) |
| **The record** `/record` | the check: how often contests have in fact ended within a vote | the counts, as dots | Mulligan and Hunter's House count, Klarner's state legislatures |
| **How it's computed** `/method` | the model in plain words | the one question (1b) | the tie as half, the event, the cost, what is set aside, every source |

**Navigation:** the midterms menu as the maker approved it ("New preview of the nav menu is perfect", 11-05 15:23), its pill at the top right; breadcrumbs on every page but the home (his 11-03 20:52); search over every contest (M-spec s.16's form). Not on the preview: nothing there yet to navigate to, and a link to a page that does not exist is a named fault (`TASTE.md`, 11-03 11:50).

---

## 4. Motion: the surfaces new to this site

Each follows M-motion s.1 (a motion runs only on a real event and serves its surface), s.4 (transform and opacity only, interruptible, no stagger, text never travels) and s.5 (the still version first; reduced motion keeps colour and opacity only). Durations are M-motion's tokens, as in `src/lib/motion.js`.

| # | Surface | Event | Motion | Token | Reduced |
|---|---|---|---|---|---|
| V1 | the field of contests on the first screen | the page's first arrival | every dot travels **from the reader's cost to its B\***, together, once: the multiplication C × N drawn | `nav-in` (680 ms, the spring), no stagger | drawn in place |
| V2 | every dot and the cost mark | the reader changes the cost | all move by one shared distance (B\* = C × N moves every contest by the same factor); one transform of the field | `chart` (450 ms, the spring) | at once |
| V3 | every dot | the reading switches (to you / to each person) | each dot glides to its new place; their order changes where populations differ | `chart` | at once |
| V4 | the lead figure, the receipt | a contest chosen | **at once** (M-motion s.4.8: text never travels); the chosen dot's ring at once | `feedback` (0 ms) | the same |
| V5 | a stake on a ballot row, the trip's segments | the reader drags | follows the finger, no easing; on release, nothing settles | none | the same |
| V6 | the zoom of the one-in-N field (candidate C) | the reader scrolls | the field's scale follows the scroll, frame by frame, with no duration of its own | none (scroll-linked) | each stop drawn still, no zoom |
| V7 | a fold (§2.4) | pressed | opens at once; its contents `reveal` | `reveal` (160 ms) | the same |
| V8 | a segmented control's indicator | pressed | slides to the chosen option | `segment` (300 ms) | jumps |

**Never** (M-motion s.6, read here): no counting up through intermediate values on the lead figure; no idle motion on the first screen (the maker's "latent" motion on the midterms door, 11-05 16:23, was for a door, not for figures, and M-motion's rule 1 governs a page of figures); no motion for what happened while the reader was away.

---

## 5. The first screen: three candidates (on the preview branch)

Each is a whole build on phone and desktop, light and dark, switched by `?v=a`, `?v=b`, `?v=c`, with a picker shown only on previews. Each takes a different idea of how to show the end. All three lead with B\* for a real contest, carry the receipt, the one question, the reader's cost, both readings, the tie named in the fold, and the cases where B\* is lowest.

- **A. "Every contest on one ruler."** The scale first. The lead figure and the receipt above; below them, the ruler of dollars with **every contest as a dot**, in rows by level, the reader's cost as a line at the left, and the real figures labelled. The cost and the reading move the whole field (V2, V3); the arrival draws the multiplication (V1). *Gives:* the scale and the breadth in one picture, the cases against the claim on the same line as the rest; closest to the midterms "Closest" chart, which the maker praised. *Costs:* the densest picture of the three; on a 320 px phone each power of ten is about 40 px wide.
- **B. "Your ballot, line by line."** The decision first. A ballot from the top line (president) to the bottom (a town race), each line with its B\* at the right edge and a track on which the reader sets what that outcome is worth to them; the trip's track at the foot fills with the shares toward 100% (§2.3). Behind each line, faint, every contest of its kind. *Gives:* law 2c as the reader lives it (one trip, many contests), and the bottom of the ballot, where B\* is lowest, in the same column as the top. *Costs:* the reader must act (set a stake) before the trip track says anything; the breadth is in the background.
- **C. "One in N, made visible."** The chance first. A field of dots, one for each time the election might be run; one of them is the time your ballot changes who wins. Scrolling zooms out through the contests, from the town race (468 dots, each visible) to the safest states (a billion), and at each stop B\* = your cost × N. The earlier fields stay as small squares inside the larger. *Gives:* what "1 in 10 million" means, felt, for a reader with no statistics (law 3); the most "cool" (his 11-05 19:09). *Costs:* breadth is a count per stop, not a field of contests; the story is read in order, so the safest states come last.

The orchestrator sends the links; the maker picks; the chosen one goes to `main` in its own PR, without the picker (brief X1).

---

## 6. The checks (before anything goes to the maker)

`design/checks/` holds the checks, adapted from `inherited/design/code/` (README process steps 3 to 6):
- **Fit** (`fit.cjs`, from `fitcheck.cjs`): every candidate at phone widths 320, 360, 390 and 430, text 1×, 1.3×, 1.6× and 2×; desktop at 900, 1000, 1100, 1280 and 1440; light and dark; fails on sideways scroll, text past the screen, text cut by a box, a word broken inside itself, text over text, controls overlapping; with every fold open as well as closed (the midterms W22 find). The short screens of M-spec s.23 (390 × 664, 360 × 640, 1280 × 720) are in it.
- **Motion** (`motion.cjs`): each surface of §4 measured against its token: animations' durations (the Web Animations API's own timing) and, for the canvas, the frames' gaps from a screencast on the phone profile (390 × 844, CPU slowed fourfold): first moved frame within 150 ms of the press (100 on the desktop), no gap over 50 ms (M-motion s.4.11, 12); reduced motion leaves no transform animation.
- **Settle** (`settle.cjs`): layout shift from the first paint to quiet is zero (no jumping, `TASTE.md` 11-05 18:28).
- **Boundary**: each part of a candidate is wrapped in `Boundary`; a part that throws leaves the rest of the page standing, logged.

---

## 7. Open, for the orchestrator (and the maker where it bears on the end)

1. **The default cost**: the median (14 minutes, $8.87, the cautious choice) or the mean (19 minutes, $12.03). Every B\* scales with it.
2. **The lead contest** of the first screen: the candidates lead with the presidency in the closest states of 2008 (Gelman, Silver and Edlin), the case most readers bring and the strongest real figure; the alternative is to lead with the lowest B\* (law 1a).
3. **`--t-display`** and **`--accent`**: two tokens beyond the midterms set (§2.1, §2.10).
4. **The name and the mark** (§2.11): the maker's to name.
5. **Populations** for the per-person reading come with D1 and D2; until then that reading is a sample on the preview.
6. **Dependencies**: none added for the candidates. The menu, the search and the drawer, when built, bring the midterms set (Base UI, cmdk, Cupertino Pane, Phosphor), each already measured there (M-spec s.16, s.17, s.9, s.19).
