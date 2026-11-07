# Similar changes across the site: a plan for Zach to review

**W5, 2026-11-02 14:50 UTC; approved by the maker at 14:53 UTC** ("I approve these changes; let's leave the logo alone for now and I'll work on that on my own"), so sections 1 to 3 are to be built and section 4 is withdrawn: the logo is his own work, and logo B stays on the page until he brings his.

You asked (14:40) that we understand the reasoning behind the changes you wanted and make similar changes elsewhere, and that you review the plan first. This is that plan. Nothing in it is built yet. Your words are quoted; what I infer is marked [inferred].

---

## 1. The reasoning

Seven principles, from your rulings of 13:08 to 14:41.

**P1. One thing leads; the rest stands behind it.** "There's a LOT of text, and a lot of it looks the same." "More deliberate separation of elements (doesn't mean MORE, but deliberate)." The fix is not more decoration but fewer levels, each clearly different: big figures, small labels, numbers on one edge, space instead of boxes.

**P2. Text is there only if it must be read.** "Unless … I actually have to read it in order to understand what's going on, then include it. Otherwise, it is a characteristic of AI-generated websites." Bound (13:21): "the data itself is useful." So explanations, instructions, subtitles and the typeface line go; past results, counts, times and sources stay.

**P3. What matters is shown as the best version of itself.** The list of closing hours became a countdown and a timeline: "it should show things as beautifully and as coolly as it possibly can"; "be deliberate about how special the website is." The bars were "just rectangles … informationally, they work. But I don't know." So a thing that is right but plain is not finished. [Inferred: this applies in proportion to how much the thing matters, which is why the seat bars and the closings came first.]

**P4. The viewer must be able to tell what is true now.** "It is vital that I am aware what is current, what is recently updated, how old." The majority mark was "not the easiest to see." So recency is shown, and the one or two facts that decide a view are legible at a glance.

**P5. Real, human-made parts, not agents' imitations.** "TRUE menus and cards, and TRUE transitions, like human-made and human-perfected." "Real symbols/svg's/parts of svg's instead of an invented flag." "Components taken directly from sites with nice prebuilt components." Where a crafted thing exists, we use it as it is. [Inferred: this reaches every drawn glyph on the page, down to the check mark and the menu's three lines.]

**P6. Each screen has its own ways.** "For phone, I'd prefer a card come up from the bottom." A back button on the phone. A menu "that slides out from the side, like the Claude or ChatGPT or Gemini menus." Not the desktop's layout shrunk.

**P7. Nothing that does nothing, nothing twice, nothing uneven.** The state dropdown "does nothing." "It doesn't need to say governors twice." The hover outline "sometimes a thick outline sometimes a thin outline." Every control works, every heading is said once, and one kind of mark is drawn one way everywhere.

What you praised, so we keep doing it: the changes "broadly implement what I wanted"; the build is "looking pretty good"; the logo is "DEFINITELY better". [Inferred: you judge by looking at the preview, so every change below must be visible there.]

---

## 2. The plan, view by view

Each row: what is there now, the change, the principle. "Spec'd" means it is already in DESIGN-SPEC v1.1 (adopted 13:36) and waits only for W9 to build it; "new" means it is proposed here for your review. Where a row needs a crafted component, it says "W11", whose preview page of real components is due at 18:00.

### 2.1 Country view

| | Now | Change | Principle |
|---|---|---|---|
| Senate list (35 rows), desktop and phone | "Alabama · U.S. Senate" over "Moore (R) 66.6% · Wess (D) 33.4%", status on the right | Spec'd (s.7): three columns, state and status on the left, two candidates stacked, shares on one right edge; "U.S. Senate" dropped from every row; the called winner alone in party colour | P1, P2, P7 |
| Chappaqua and Michigan | same form as above | Spec'd: the same rows, with the office in the place column | P1 |
| The calls column | "The night's calls" with a three-line explanation | Spec'd: "Calls", grouped by closing hour, the explanation gone, one source line at the foot | P2 |
| Map legend (6 keys, repeated under the phone's tiles) | "Called, Democrat · Called, Republican · Called, other · Calls differ · Not called · No race" | **New:** the first three fold into one key, "Called", shown as the three party swatches together; "Not called" and "No race" stay; "Calls differ" shows only when it occurs on the map. From six items to three or four | P2, P7 |
| Hole under the map (desktop) | an empty 132 px preview block until a hover | Spec'd (surface 8): a fixed panel beside the map that keeps the last state shown; no empty block | P1, P7 |
| Phone: latest-call strip | its own strip with "All calls" | Spec'd (s.6): the latest call is the timeline's caption line; pressing it opens the calls sheet | P1, P6 |
| Status words | "21% reporting", "No results yet" | Spec'd (R8): "21% in", "No votes yet"; the same place on every row | P1, P7 |

### 2.2 A state (`/mi`)

| | Now | Change | Principle |
|---|---|---|---|
| Statewide races | bordered, rounded boxes, each with its own source line | Spec'd (s.8.1): sections with a heading and one rule; the source line once | P1, P2 |
| House seats | 13 bordered boxes in a grid, each listing every candidate and "No results yet" and "This district in 2024 …" | Spec'd: list rows beside the sticky district map; the 2024 result stays (it is data), on the race's own view | P1, P2 |
| Phone | the district map fills the first screen; the first race starts 1,000 px down | Spec'd (s.9) and **new detail:** the state card's first screen is the Senate and Governor races; the map comes at full height, above the House rows it keys | P1, P6 |
| Subtitle | "Polls close 8 PM ET in part of the state, 9 PM ET in the rest" | **New:** "Polls close 8 PM ET · 9 PM in the west" until they close; then "Polls closed", 12 px, beside the name. After the night it goes | P2 |
| Breadcrumb "Country" | plain word | **New:** "‹ Country", the one way back on desktop; on the phone the card's "‹ Back" | P6, P7 |

### 2.3 A race (`/mi/senate`)

| | Now | Change | Principle |
|---|---|---|---|
| Candidates | names 16 px, shares 17 px, one hairline each | Spec'd (s.8.2): names at 19, shares at 19 / 600 on the right edge, a 4 px share bar under each name (party colour only when called) | P1, P3 |
| "83.3% reporting (civicAPI's own figure of precincts reporting; not a share of the expected vote)" | a parenthetical | Spec'd: "83% of precincts in · as of 10:36 PM ET" | P2 |
| "Candidates as printed on the state's official list: source." | a sentence | Spec'd: a link in the one source line | P2 |
| The call | a sentence in the footer | Spec'd: "Called for El-Sayed (D) by civicAPI at 10:10 PM" at the top in the party colour; a withdrawn or changed call said there in warn | P4 |
| The lower two-thirds of the page | empty | **New, for a later step:** this is the one view where law 3's fuller information belongs (how much is in by county, the last election, the incumbent). It depends on what the data path has (W10, and your 13:26 ruling on civicAPI's further data), so it is named here and not designed yet | P1, P3 |

### 2.4 Senate and Governors (`/senate`, `/governors`)

| | Now | Change | Principle |
|---|---|---|---|
| Races | a three-column grid of bordered boxes, each with a source line | Spec'd (s.8.3): list rows in one column, the country map in the chamber's layer beside them, sticky | P1, P2 |
| "Seats" subheading over the bar | a word the bar does not need | Spec'd: gone (the bar is the pill, with its figures on it) | P2, P7 |

### 2.5 The House (`/house`)

| | Now | Change | Principle |
|---|---|---|---|
| Table | "No results" in the In column; group rows plain | Spec'd (s.8.4): "No votes yet"; the state's name at 15 / 600, sticky while its rows scroll; the called leader in party colour with a 3 px rule | P1, P4, P7 |
| Instruction under the map ("Rest the pointer on a state's rows … to see its districts here") | if still present | **New:** goes | P2 |
| Phone | the same wide table | Spec'd: rows, no sideways scrolling | P6 |

### 2.6 Header and menu (every view)

| | Now | Change | Principle |
|---|---|---|---|
| Menu's room races | one run-on line | Sent to W9 (14:31): one per line under a small "Chappaqua" label | P1 |
| "Find a state" | states only | **New (s.3 below):** search of everything | P3, P7 |
| The glyphs: menu lines, check mark, ×, chevrons, grip | drawn by hand in the page | **New:** every glyph from one real icon set, used as published. Phosphor (MIT) if logo C is chosen, since its star is Phosphor's; otherwise Lucide (ISC), which is what most crafted component sets ship with. W11's choice of components may settle which | P5, P7 |
| Menu, cards, sheets, transitions, the Senate/Governors toggle, Pause | Zag's drawer under our motion; our own buttons | W11: crafted components with their own motion, shown beside what we have, for you to choose | P5 |

### 2.7 The states the page is in that are not built yet

These matter because the site will spend most of Tuesday in them.

| State | Now | Change | Principle |
|---|---|---|---|
| **Before any polls close** (all of Tuesday until 6 PM ET) | every one of 35 Senate rows says "Polls close 7 PM ET"; the calls column is a list of closing hours; the bars show the not-up seats | **New:** the list groups by closing hour, with one heading per hour ("Polls close 7 PM ET", then the states' rows) and no status column, so the same words are not said 35 times; the calls column is one line, "No calls yet"; the timeline shows its ticks and the now line; the header's countdown carries the moment. Seat bars show the not-up seats and "35 to call" | P1, P2, P7 |
| **Loading** (first second) | "Loading results…" after 1 s | **New:** the page draws its structure at once from what is in the bundle (every race's name and candidates), with the figures' places empty, and the figures arrive into it. Never a spinner, never a pulsing placeholder. "Loading results…" stays as the one status line only if nothing has arrived after 1 s | P4, P7 |
| **A source gone quiet** (stale) | a sentence in a card's footer | Spec'd (R8) and **new detail:** the row's status says "as of 9:04 PM" in the warn colour once the figure is older than the source's normal interval; the band's absence already says it has not changed. In the race in focus, one line: "No new count from civicAPI since 9:04 PM" | P4 |
| **A call withdrawn or changed** | a sentence | Spec'd: "Call withdrawn" in the status place; the history in one line on the race view; the row loses its party colour at once | P4 |
| **The site cannot reach its own data** | one status line under the header | Keep as is: one line, no toast, no modal. **New detail:** the figures keep their last values and their "as of" times; nothing greys out | P4, P7 |
| **A state's or race's data fails to load** | "This state's races could not be loaded. Try again in a moment." | **New:** the view still draws the names (they are in the bundle); the status place says "Couldn't load Michigan's figures. Retrying." and the next poll retries, so there is no button that does what the page already does | P7 |
| **Figures held back** (the source's test flag) | "Figures held back" / a sentence | Keep: it must be read (law 7). Shorten to the status place | P2 |
| **Paused** | "Updates paused. Figures are as of 10:36 PM." | Keep, one line; the Pause button reads "Resume" | P4, P7 |
| **After every federal race is called** | the bars say "0 to call" | **New:** the "to call" line goes; the header keeps only the checked time; the timeline is complete | P7 |
| **Rehearsal and fixture previews** | a banner | Keep: it must be read (law 7) | P2 |
| **A wrong address** | a not-found page | Keep to one line and the menu | P2 |

---

## 3. Search

You asked that search "be able to search anything relevant (candidates, states, districts? Others?)".

**What it covers, and the data for each** [measured in `data/static/races.json` unless marked]:

| Kind | Count | We hold it | Needed |
|---|---|---|---|
| States and territories | 55 | yes | – |
| Senate, House, governors, delegates | 35 + 435 + 39 + 5 | yes, with closing hours | – |
| Other statewide offices (attorney general, secretary of state, courts …) | 220 | yes | – |
| State legislature seats | 2,176 | yes | – |
| Ballot measures | 146 | yes, with their titles | – |
| Candidates, by name | 6,212 names | yes, from the states' official lists | – |
| Incumbents | 562 named | yes | – |
| Districts by number ("NY-17", "17th") | 435 | yes | – |
| Districts by place ("Chappaqua", "Ann Arbor") | about 32,000 Census places | no | the Census 2020 place-to-district relationship file (`tab20_cd11820_place20_natl.txt`, public domain; confirmed present at www2.census.gov), with W7's plan-in-force check for the states that redrew since |
| ZIP code to district | about 33,000 ZCTAs | no | the Census ZCTA shapes (TIGER 2025, present) matched once, at build time, against W7's district boundaries. A ZIP that spans two districts shows both. [Inferred: a day's work; a ZIP is not exactly a ZCTA, which the result must say] |
| Counties | 3,100; W7 holds the boundaries | boundaries only | county results, which depend on the data path (W10) and your 13:26 ruling on civicAPI's further data |

**Weight and loading** [measured by building the index from `races.json`]: an index of every race, candidate and incumbent (9,965 entries) is **125 KB gzip** as plain JSON and 97 KB in a compact form; federal and governor entries alone are 28 KB. Places would add about 150 KB and ZIPs about 100 KB [inferred]. None of it is in the first view: the index is fetched when the search field is first focused, or in idle time after the first view has painted, whichever comes first. Matching 10,000 entries needs no library; a normalised substring match runs in well under a frame [inferred].

**Where it lives:** the menu's field becomes **Search**, for everything above. On desktop, pressing **/** or **⌘K** anywhere opens the same search as a palette; on the phone, the menu's field. Results are grouped, in this order: the room's races, states, districts, candidates, measures, other offices, places. Each result follows the spec's row form: the name at 15 / 600, the race or state under it in 12 px muted. A candidate opens the race; a state opens the state; a place or ZIP opens its district's race. The palette component itself (cmdk or another crafted one) is W11's.

---

## 4. The logo, from real SVGs (withdrawn 14:53 UTC: the maker is doing the logo himself; kept as a record)

You asked for "real symbols/svg's/parts of svg's instead of an invented flag with a single star". Three directions, each built from a published SVG whose geometry is unchanged, with the source and licence read at the source. Files are in `research/design/specimens/logo-c3/`; the comparison shot is `shots/c3-logo-directions.png`.

| | Source | Licence | What it is |
|---|---|---|---|
| **A. A corner of the flag** (recommended) | Wikimedia Commons, `File:Flag_of_the_United_States.svg` (the official 10:19 geometry; colours Old Glory red #b31942 and blue #0a3161) | public domain (PD-USGov, PD-flag on its file page) | a 22 px tile cropped by viewBox to where the canton meets the stripes: two of the flag's own stars, its own stripes. At 22 px it reads as the flag without being the whole flag, which at that size turns to noise (direction B) |
| **B. The whole flag** | lipis/flag-icons, `flags/1x1/us.svg`, unchanged | MIT | the square flag in a rounded tile. The 50 stars become a texture at 22 px |
| **C. The wordmark with a star** | Phosphor Icons, `star-fill.svg`, unchanged, in the flag's red | MIT | "Midterms ★ 2026": the quietest. The star is an icon set's, not the flag's |

Recommendation: **A**. It is the real flag, part of it, at the size where its parts are still legible; it serves as the favicon and home-screen icon; and it costs under 2 KB. C is the fallback if A reads as too much flag beside the party colours of the bars.

---

## 5. What this plan depends on

- **W11's components** (menus, cards, sheets, transitions, the search palette, the toggle, the icon set), due 18:00: rows marked W11 take their final form from what you choose there.
- **The data path** (W10) and your 13:26 ruling: the race view's lower half, counties, and ZIP-to-district.
- **W9's build order:** the spec'd rows are in progress; the new rows wait for your word on this plan.
