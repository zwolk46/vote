# W5: the field of components, maps, motion and typefaces

*Worker W5 (Opus 5.5, high), brief `briefs/2026-11-02-W5-design-field.md`, started 2026-11-02 03:40 UTC. Nothing here is chosen for the site: these are candidates for the orchestrator (law 6b; `_COMMON.md` 3). Facts are marked [measured], [stated] (with where), [vendor claim] or [inferred] (`_COMMON.md` 6).*

**Status: breadth done (first report, 2026-11-02 ~04:05 UTC). Resumed 2026-11-02 04:10 UTC** by the continuation W5 in the project "Midterms" (`_COMMON.md` 16): depth for the second report, from section 9; new work in sections 10 onward.

## 1. Catalogues (breadth)

Where refined components and motion are catalogued, and whether each is worth depth for this site. "Depth" means: its items can be read first-hand (code, timings) and it has items that bear on watching results.

| Catalogue | What it holds | Readable here? | Worth depth? |
|---|---|---|---|
| **details.so** (Inspo library and Vault) | Inspo: details captured from live sites in 80+ categories (Navigation 251, Dropdown 77, Stats 60, Timeline 21, Contextual Transition 25, Morphing 25 inspirations) [stated, `details.so/llms.txt`]. Vault: production code in 10 categories, 16 resources free; Navigation has 8, one free (Reveal Navigation) [stated, `vault/category/navigation.md`] | Every public page has a `.md` twin; preview videos (60 fps, 1280 px) are public for all Vault items; live previews are public only for free items (`preview-access="public"`), gated for Max items [measured] | **Yes**: the maker's named example of what he loves. Read in section 4. |
| **Mobbin** (connector) | Screens and flows of shipped iOS/web apps | Yes, through the connector [measured] | **Narrowly.** A search for an election results screen returned no election app; nearest were polls (Instagram, Runna, Commons), sports results (Premier League, Formula 1) and prediction-market rows in Perplexity Finance [measured, 2026-11-02 03:50 UTC]. Useful for phone patterns of live lists and polls, not for election graphics. |
| **Motion's examples** (`motion.dev`, `examples.motion.dev`) | Hundreds of React/JS motion examples; `llms.txt` and a free docs MCP [stated, `motion.dev/llms.txt`] | Yes, `llms.txt` | Yes for technique (layout animation, springs, number animation). |
| **Writers on interaction craft**: Emil Kowalski (`emilkowal.ski/ui`), Rauno Freiberg (`rauno.me/craft`), Vercel's Web Interface Guidelines | Principles with measured examples (durations, frequency, interruptibility) | Yes, curl [measured] | Yes, as the reasons behind motion choices (section 4). |
| **Design-system motion specs**: IBM Carbon, Material 3, Apple HIG | Token tables of easings and durations; Carbon splits "productive" from "expressive" motion | Carbon yes; Material 3 and Apple pages return mostly script shells to curl [measured] | Carbon yes (its split maps onto this site: see 4.3). |
| **21st.dev** (skill in this session) | Community React components, installable | Yes, through the skill | **Low.** Inferred from the inherited principles review: generated-component galleries are where the tells the maker named come from (glows, marquees, pulsing dots). Kept as a source of parts to inspect, not of finish [inferred]. |
| **Godly, Awwwards, Land-book, Refero, SiteInspire** | Galleries of whole sites | Not yet read | Low for this site: they catalogue marketing sites, not live data. |
| **Election and data-graphics catalogues** | Award galleries (SND, Malofiej, Sigma, Online Journalism Awards), data desks' write-ups and open-source election rigs | Being read by a helper (section 2) | Yes: this is where election components live. |

## 2. Election components across the field

Full evidence: `notes/2026-11-02-W5-election-components-helper.md` (by component kind, a motion and faults table, the best three to six examples of each kind, galleries, sources with times); screenshots `shots/el-*.png` (NPR 2024 president, Senate, House, Pennsylvania and Alaska pages; Guardian 2024 and its 2026 control-of-Congress page; Texas Tribune 2022; The Hill with DDHQ; Al Jazeera; desktop and phone). This goes beyond the inherited survey S1 mainly through **open-source election code** (NPR's `elections22` and `elections24-general`, read whole), the Guardian's open code, Texas Tribune, and the Washington Post's open live model, which show *rules* no screenshot shows. The NYT, AP, Reuters, Bloomberg, FT, Economist, Axios and WSJ still refused (section 7).

The best examples of each kind (evidence, not choice):

- **Seat bars.** NPR's Senate bar is 100 wide and starts from the seats not up this year (a hand-kept sheet), with "51 seats for majority", a "GOP +4" change chip and a check mark at majority [measured, code and `shots/el-npr2024-senate-desktop.png`]. Politico names holdovers in words ("28 seats not up"). The Guardian's House line: "215 +1 | 218 to win | 220 −1" and "435/435 races called"; its Senate hex map draws two hexes per state, the seat not up a white "No election" hex [measured].
- **Race cards and tables.** NPR's card footer: "AP estimate: x% in • Last updated • Winner called: <date> at <time>", with footnotes only when they are true (uncontested, certified, ranked-choice pending, a win threshold); its Senate board groups races as Likely Democratic / Competitive / Likely Republican, with FLIP, R.O. (runoff) and RCV (ranked choice) cells and an incumbent dot [measured]. Politico's cards say Winner and "Flip / GOP held / Dems held" in words.
- **Calls.** The Guardian's "Latest results" strip of call cards is the only true calls feed read; NPR instead stamps each race with its call time. The Washington Post's graphics (built with Development Seed) used "freshies" notifications on new data and subtle highlights when a race is tight or called [stated].
- **How much is in.** AP: the expected-vote figure is an estimate that "can and will fluctuate", and 99% of precincts reporting can still leave votes uncounted [stated, AP's own pages]. NPR never shows 0 or 100: "<1" and ">99" [measured, code]. NPR shades a leader only after 50% of the expected vote is in [measured in code; stated in its 2020 write-up].
- **Probability and needles.** The NYT needle is unread (blocked). Decision Desk HQ shows a probability as one sentence with a percent chip and a timestamp, no gauge [measured, via The Hill]. Open needle code exists (`jtannen/election_needle`) and so does a critique of it (Brad Templeton). [Note: a forecast is information only if a true source publishes it; the site may not compute one itself without a source (law 7) — inferred.]
- **Swing.** The Guardian's 2020 county swing map: one static arrow per county, direction the party, length the log of the swing [measured, code]. Politico's Pennsylvania page: a strip of past margins.
- **Leading versus won, flips, runoffs, ranked choice.** NPR: pale tint leading, solid tint winner, two greys for "no results" and "early results", FLIP, R.O., RCV; its 2022 House code suppressed flips because redistricting made "the same seat" ambiguous [measured]. The Guardian: hatched for lead, solid for hold, two-colour stripe for flip, grey for undeclared. AP's v3 fields include `raceCallStatus` (with "Awaiting Ranked Choice Results") and `eevp`; NPR notes a call can be withdrawn, so a page must be able to remove a check mark [stated].
- **Navigation.** NPR: top tabs and an all-states dropdown; every board row links to its state page; state pages have section tabs; the phone gets shortened labels and its key drops from three columns to one. Politico: the same balance strip on every page plus tabs and a state menu.

**Motion seen on these pages, against law 5** [measured]: NPR's president bar has a 0.4 s width transition (a real change: seats moving). A Texas Tribune repository pulses its live dot only when data is under 15 minutes old (a real condition). **Faults found:** the Guardian's 2024 page runs an endless 1.5 s pulse on a dot beside "LIVE" two years after the night, with 435/435 races called (the named fault of a dot that pulses for nothing live); Al Jazeera shows empty "| %" under a static banner and scrolls sideways on a phone; NPR and The Hill put a large ad above the score (`shots/el-npr2024-senate-desktop.png`); the Guardian's cookie banner covers half of the phone's first screen (`shots/el-guardian-midterm-control-phone.png`). No marquee was seen on any results page.

**Election-graphics catalogues worth depth:** `github.com/nprapps` (open, current, readable); Datawrapper's weekly "Data Vis Dispatch" (links to NYT, Bloomberg, FT, WSJ, Reuters election graphics, which could themselves be followed where not blocked); Source (OpenNews) "elections" tag; the NPR Visuals blog; Online Journalism Awards entries; SND results. Malofiej, Sigma and Information is Beautiful winner lists were not reached.

## 3. Maps

Full evidence: `notes/2026-11-02-W5-maps-helper.md` (map kinds, about 25 tools with licence, version, size, renderer, cost, hover and touch; evidence on the three ideas of law 11; URLs with times).

### 3.1 Kinds

| Kind | Serves | Costs the room | Where its shapes come from (law 7) |
|---|---|---|---|
| Geographic state map (Albers USA; Alaska and Hawaii inset) | Familiar; "familiarity in many cases is more important to us" (a data journalist in Cai and Kay, CHI 2024) [stated] | Land outweighs people ("land doesn't vote"); at 360 px wide DC is about 1 px², Rhode Island 5 × 7 px, Delaware 7 × 12 px, all below WCAG 2.2's 24 px target [measured from us-atlas]; Alaska drawn at 0.35× area by `geoAlbersUsa` [stated, d3 docs] | Census cartographic boundary files, already generalised by the Census ("small holes or discontiguous parts … not included") [stated, GENZ2025 description] |
| Same, with callout boxes for the north-eastern states and DC | Keeps the familiar shape and makes small states tappable | A second layout to draw | Census shapes plus a hand-placed box layout |
| Square tile grid, one tile per state | Equal weight, every state tappable; WSJ: "You can actually interact better with a cartogram that's more blocky" on small phones [stated, Storybench] | Positions approximate, some neighbours wrong; no shape inside a state | Hand-made layouts (NPR's, WaPo's `statebins`, Pitch tilegrams on Natural Earth, public domain) [stated] |
| Two-hexagon state tile map (Senate: two seats per state) | Shows both seats of a state; fits a Senate night where a few states elect both | As tile grid | The Downballot "50 State Tile Map", "you are free to use them" [stated] |
| Hex cartogram of all 435 House districts | Every seat the same size, so urban seats are visible | Placement is approximate: their own example puts NYC and Long Island across half of upstate New York [stated, Daily Kos 2022]; 435 targets exceed the about 100 a phone can make easily tappable [stated, NZZ/Zurich, ICA 2023] | Daily Kos Elections / The Downballot hexmap (Daniel Donner, 2015 onward; v1.x CC BY-SA 4.0; a 2026 update for the ten states that redrew is reported, its files and terms not yet read) [stated] |
| Dot or bubble map | Weight without land bias (FT 2016, NPR 2020) [stated] | Overlap in the north-east | Census centroids |
| District map inside a state | The natural drill-down; least distorted at state scale | Urban districts are "unidentifiable black smudges" (DKE) [stated]; pre-made district maps go stale (Highcharts' are the 113th Congress) [measured] | Census `cb_2025_us_cd119_*` (500k, 5m, 20m) and state legislative upper and lower files exist; **no cd120 file and no county-legislature layer** [measured, GENZ2025 listing]; whether cd119 carries the 2025–26 redraws is for W4 |
| Chip grid or list of districts (no map) | Equal weight, labelled, tappable; 270toWin added a table view because 435 districts are hard to read on its map [stated] | No geography | n/a |

### 3.2 Tools (the deciding columns; the rest in the notes)

- **No base-map service needed, so no tile bill and no third party on the night:** d3-geo (ISC, 13 KB gz) with topojson-client; react-simple-maps (MIT, SVG); visx geo; Observable Plot (`albers-usa`); ECharts (Apache-2.0; its docs advise SVG on phones for memory); MapLibre GL JS (BSD-3, 296 KB gz, WebGL) fed with our own GeoJSON or a PMTiles file. Preprocessing: mapshaper (MPL-2.0; `keep-shapes` stops small polygons vanishing; builds topology so shared borders stay shared) and topojson-simplify [stated/measured, notes section 2].
- **Need a tile service (money or terms):** Mapbox GL JS (proprietary since v2; 50,000 map loads a month free, then US$5 per 1,000) [stated, mapbox.com/pricing]; MapTiler and Stadia (free tiers exclude commercial use).
- **Hosted or licensed:** Datawrapper (free plan embeds; maps can refresh from an external CSV every minute for 24 hours after publishing, then hourly) [stated]; Flourish (live data only on a tier with no price shown); Highcharts Maps (public sites need a paid SaaS licence; districts 113th Congress); amCharts (free only with its logo; no district files).
- **Poor fits:** deck.gl (its own docs warn phones are "more sensitive to memory pressure … resulting in browser restarts") [stated]; Kepler.gl (an analyst's tool); Leaflet (no stable release since 2023) [measured].
- [inferred] For shapes we draw from Census files ourselves, an SVG path per state or district (d3-geo) is the simplest route to exact, styleable, animatable shapes; WebGL earns its weight only with pan-and-zoom over thousands of features (CNN uses Mapbox tiles for that) [S1].

### 3.3 The ideas of law 11, with the evidence on each side

**(a) A national map showing where the contests are.** *For:* it is the convention; Cai and Kay found maps and balance-of-power bars "at the tops of pages to communicate a simple, holistic overview"; readers prefer familiar maps (Houtman, ICA 2022 abstract, 240 people). *Against:* land bias (Cai and Kay, DKE, NPR); in the same Houtman abstract block cartograms were more accurate on whole-picture questions and the geographic choropleth worst there; small states fall below tap size on a phone. *Gap:* no study found of a map of *where contests are* as opposed to who won; on a midterm night only some states have a Senate or governor race, so a presence map is a different object from the presidential map most evidence is about [inferred].

**(b) Hovering a state to see its races.** *For, on desktop:* an established pattern (Chicago Tribune 2012, with the same details duplicated in a table below); hover suits supplementary detail (NN/g). *Against:* NN/g: tooltips "are not normally available on touchscreens"; WCAG 1.4.13 requires hover content to be dismissible, hoverable and persistent, and keyboard reachable. *What replaces it on a phone:* tap to select, with a persistent panel or the table beneath (Tribune pattern); WSJ's blocky cartogram and "cells" for phones. The details.so drawer itself confines hover to `@media (hover: hover)` (4.1) [measured].

**(c) Clicking into a state to see its districts.** *For:* the standard navigation, "double encoded" from map, table row or dropdown (Cai and Kay); NPR 2020 kept drill-down fast on phones (PageSpeed mobile in the 80s on election night, per-state data lazy-loaded) [stated]; a state is where a true district map is least distorted. *Against:* navigation is a named difficulty ("easy to get back to where you were", Cai and Kay challenge 8); urban districts are smudges; district files go stale and ten states redrew since 2024, so this is where law 7 bites hardest. No usability study found comparing click-in with a list of districts.

## 4. Motion, and what details.so's menus do

### 4.1 The details.so navigation menus, read first-hand

The Vault's eight navigation items: Navigation Dropdown, Top Morphing Navigation, Reveal Navigation 3.0, Morphing Navigation, Reveal Navigation (free), Reveal Navigation 2.0, Top Drawer Navigation, Navigation Drawer [stated, `details.so/vault/category/navigation.md`, read 03:45 UTC]. The code of the seven Max items is behind the paid plan and their live previews are marked `gated`; I did not try to open them. What was read:

- **The free one, "Reveal Navigation" (its page title: "Recess Drawer Navigation"), read whole and measured in Chromium** (`/vault-previews/navigation-06/index.html`, public; its CSS and its 72 KB script, which bundles GSAP). [measured]
  - *What happens.* Pressing the "Menu" pill does not slide a drawer over the page. The page itself shrinks: it is clipped to a card with a 16 px margin and 16 px rounded corners, its content slides 100 px left (40 px on a phone), and it dims to 40% under a cover; the drawer is revealed behind it. The menu's text block slides in 80 px from the right, and a hairline divider draws itself from the right. All of it starts on the same frame; nothing is staggered. The pill's "Menu" label fades and its "+" turns 45° into "×".
  - *Timing.* Opening: 0.8 s on a `linear()` curve, which is how CSS writes a spring: `linear(0, .005, .02 2.1%, .081 4.7%, .467 15.7%, … .961 50.3%, … .994 72.3%, 1)`, so almost half the distance is covered in the first 126 ms and the rest settles slowly, with no overshoot. Measured on the phone layout: 21% at 91 ms, 43% at 141 ms, 75% at 243 ms, 92% at 362 ms, 99% by 560 ms. Closing is faster, 0.51 s, `cubic-bezier(.17,.84,.44,1)` (a strong ease-out). The text slides with GSAP `power4.out` over 0.94 s; the divider with `power2.out` over 0.48 s; the dim with `ease-out` over 0.35 s; the pill's icon turns over 0.6 s on `cubic-bezier(.165,.84,.44,1)`.
  - *Desktop versus phone.* Desktop: a 450 px drawer, the page kept visible as a dimmed card beside it (so you can see where you were), 100 px parallax. Phone (under 600 px): the drawer is the full width, the page is clipped away entirely, 40 px parallax. Hover effects (the label rolling up a line, the "+" turning to 135°) exist only under `@media (hover: hover)`, so a phone never gets a stuck hover state.
  - *Care that does not show.* Escape closes it and returns focus to the button; the page underneath is made `inert` while open; `aria-expanded` and the button's label change; a resize mid-animation re-measures and resumes from the same progress; images fade in only once loaded; `prefers-reduced-motion` is read. The toggle uses `corner-shape: superellipse(1.2)`, a squircle corner rather than a circle.
  - Screenshots: `shots/detailsso-nav06-desk-closed.png`, `-desk-open.png`, `-phone-closed.png`, `-phone-open.png`.
- **The seven paid ones, from their public preview videos** (60 fps; per-frame change measured with ffmpeg; contact sheets looked at) [measured, inferred where marked]:
  - *Top Morphing Navigation:* a small pill at the top grows into the menu panel (the thing pressed becomes the thing that opens); once the panel has its size, the links appear one after another about 80 ms apart, then an image fades in. Opening motion about 1.2 s end to end including the stagger.
  - *Morphing Navigation:* a bar at the bottom grows upward into a panel; on close the text fades first and then the shape shrinks; on open the shape grows first and the lines of text rise into place one by one from behind a mask.
  - *Navigation Dropdown:* a top bar whose dropdown shows an image that changes with the item under the pointer; on scroll the full-width bar compacts into a floating pill.
  - *Reveal Navigation 2.0:* two coloured layers sweep in a few frames apart before the menu, the page sliding aside; each open or close about 0.45 to 0.65 s, the motion front-loaded (the largest change in the first fifth, then a long settle) [measured profile].
  - Across all eight, every open or close measured has the same shape: the biggest movement in the first 10 to 25% of the time and a long, slowing tail [measured, per-frame change profiles].

**What makes them what the maker loves** (my reading, for the orchestrator; the maker's own words are "precisely elegant", "fluid and natural", "integrate well into those types of websites") [inferred]:
1. **Response at once, rest slowly.** A spring-shaped curve (or a strong ease-out) gives a visible change within the first frame or two, so the menu feels caused by the press, and a long settle, so it never stops abruptly. That is "precise" (it answers the hand) and "natural" (things in the world decelerate).
2. **Continuity.** The thing pressed, or the page itself, becomes the menu; nothing appears from nowhere. In the free one the page you were on is still there, smaller and dimmed, so your place is never lost.
3. **Layers at different speeds, started together.** Page, content and dim move at different distances and durations from one start, which reads as depth without decoration. Where there is a stagger (the morphing ones), it is short, about 80 ms, and in reading order.
4. **Closing is quicker than opening.** 0.51 s against 0.8 s: getting out of the way matters more than arriving.
5. **Each kind of screen gets its own version.** Different widths, distances and hover rules for desktop and phone, as law 4 asks.
6. **Nothing decorative.** No glow, no shadow, no bounce, no idle motion: every movement answers a press.

### 4.2 The motion field: libraries and techniques

| Candidate | What it does | Licence and cost | Bears on this site |
|---|---|---|---|
| **CSS transitions with `linear()` springs** | A spring written as a CSS easing; runs off the main thread | Free; `linear()` easing is in current browsers (the details.so drawer uses it) [measured] | Panels, menus, state changes. Vercel's guidelines put CSS first, then the Web Animations API, then libraries [stated, `vercel-labs/web-interface-guidelines`]. |
| **View Transitions API** | Animates between two states of the page (same-document) or two pages (cross-document), the browser morphing shared elements | Free; same-document supported in Chrome 111+, Safari 18+, Firefox 144+, 92.9% of global usage; cross-document Chrome 126+, Safari 18.2+, no Firefox, 86.8% [stated, caniuse data, `Fyrd/caniuse` 2026-11-02] | Moving between national, state and race views with the pressed thing becoming the next view (continuity, 4.1 point 2). |
| **Motion** (`motion`, formerly Framer Motion) | Springs, layout animation (an element animates to its new place when the layout changes), shared-element transitions, gestures; React, Vue and plain JS | `motion`, `motion/react`, `motion-v` free and MIT [stated, `motion.dev/llms.txt`]. **Motion+** paid: one-time Solo licence, US$399 per developer in the page's structured data [stated, `motion.dev/plus` JSON-LD; the visible price renders client-side]; includes `AnimateNumber`, `Ticker`, `AnimateView` | Layout animation fits a table of races re-ordering as results arrive. |
| **GSAP** | Timelines and tweens; the details.so drawer uses it | Free for everyone, including plugins, under the "no charge" Standard License, since Webflow's support; not for tools that let users build animations without code in competition with Webflow [stated, `gsap.com/standard-license`] | Choreographed sequences; heavier than CSS for simple states. |
| **NumberFlow** (`number-flow`, by Maxwell Barvian) | Animates a number from one value to the next digit by digit; React, Vue, Svelte, plain JS | MIT, v0.6.2 [stated, its `package.json`]. Also the free "Number Flow" item in the details.so Vault, whose preview runs it with transform 900 ms on a spring `linear()` curve and opacity 450 ms ease-out, and a `trend` setting (digits roll up when the number rises, down when it falls); respects reduced motion [measured, `vault-previews/number-flow`] | **Directly**: vote counts and percentages changing when a real batch of votes arrives. The roll direction is information (up or down). |
| **react-spring**, **anime.js** (v4.5.0, MIT), **AutoAnimate** (FormKit) | Spring physics; general tweening; one-line list animations | All free (anime.js MIT [stated, its `package.json`]) | Alternatives; AutoAnimate is the cheapest way to animate rows entering a list. |
| **Web Animations API** | The browser's own animation engine, scriptable | Free | Where CSS cannot express a sequence. |

**What the craft writers say makes motion feel exact** (each read at source) [stated]:
- Emil Kowalski: ease-out for responsiveness ("starts fast and slows down"); "animations should also usually be shorter than 300ms"; consider "how often the user will see it"; "never animate keyboard initiated actions" (`emilkowal.ski/ui/great-animations`). The details.so drawer (0.8 s) breaks the 300 ms rule, which it can because a site menu is opened rarely; a results table refreshed every minute is opened constantly, so the rule applies there [inferred].
- Rauno Freiberg: great interactions are "interruptible", gestures "retain momentum", and high-frequency actions should not animate (macOS context menus appear without motion) (`rauno.me/craft/interaction-design`).
- Vercel's guidelines: honour `prefers-reduced-motion`; animate only to "clarify cause & effect" or for deliberate delight; interruptible; avoid autoplay; anchor `transform-origin` where the motion physically starts; never `transition: all`.
- IBM Carbon: two kinds, **productive** motion ("efficiency and responsiveness, while remaining subtle", for dropdowns, data tables and visualisations; `cubic-bezier(0.2, 0, 0.38, 0.9)`) and **expressive** motion ("for significant moments … or when the movement itself conveys a meaning", reserved "for occasional, important moments"; `cubic-bezier(0.4, 0.14, 0.3, 1)`) (`carbondesignsystem.com/elements/motion/overview`).

### 4.3 Motion on a results site: which real events there are

Law 5: motion that signals an event is information when the event is real and decoration when it is not. The events a results site actually has, and what each could carry [inferred, from the law and the sources above; candidates only]:

| Real event | How often on the night | Candidate motion | Kind (Carbon's terms) |
|---|---|---|---|
| A race is **called** | A few hundred times, each once | The most salient change on the page (Cai and Kay: calls take "the highest visual salience"); the race's colour fills and its card or map shape settles; a calls list gains a row | Expressive: rare and meaningful |
| A **seat changes party** (flip) | Tens of times | Same as a call, plus the seat moving across the seat bar from one side to the other | Expressive |
| **Control of a chamber** is decided (51 Senate, 218 House) | Once or twice | The seat bar crossing its marker | Expressive, the night's single largest moment |
| A **new batch of votes** arrives for a race | Thousands of times | Numbers roll to their new values (NumberFlow-like, direction shown); the "how much is in" bar extends | Productive: quick, small, never on a loop |
| The **lead changes** in a race | Tens to hundreds | Order of candidates swaps with a layout animation (the row moves, so the eye can follow) | Productive |
| **Polls close** in a state | About 15 times across the evening | That state's races become active (from "polls close 8 PM" to counting) | Productive |
| The person **opens** a state or race | Whenever they choose | The pressed thing becomes the view (view transition or shared-element morph), spring-shaped like the details.so menus, closing faster than opening | Productive by frequency; may be expressive only on first open [inferred] |
| Nothing new arrived | Most of the time | No motion. A "last updated" time can change silently; a pulsing dot for liveness is a named fault (`RULINGS.md` 2026-10-24) and journalists warned it "could potentially create anxiety" (Cai and Kay, in the inherited survey) | none |

## 5. Typefaces

Full evidence: `notes/2026-11-02-W5-typefaces-helper.md` (28 candidates, 53 free font files checked with fontTools, 111 logged fetches), specimens `shots/typefaces-free_a.png`, `-free_b.png`, `-zero.png` (the strings `1,234,567 51.3% 87% in 218` and `1,111,111 / 8,888,888` set with tabular figures on).

**What decides a results face** [inferred]: digits of one width so columns and changing counts do not jitter (`tnum`, or digits that are tabular by default); a narrow or condensed width for tables on a 390 px phone; `1`, `l`, `I` and `0`, `O` told apart; legible at 13 to 15 px; weights from table text to scoreboard numerals.

**What the field shows** [measured, CSS read 2026-11-02 03:48 UTC; these are the desks' pages, not necessarily their tables]: the desks that could be read pair a text face with a **condensed or narrow sibling**: CNN Sans Display and CNN Sans Condensed; Politico's 2024 results, DIN 2014 and DIN 2014 Narrow (Adobe Fonts) with Söhne as fallback; NBC, Klim's Founders Grotesk Condensed, Text and Mono with Publico; ABC News, Klim's Tiempos; Decision Desk HQ, Inter; NPR and the Guardian, their own faces. NYT, AP, Bloomberg, Reuters, Washington Post refused.

**Free candidates** (SIL OFL 1.1, $0, self-hosted, no traffic limit) [measured]:
- *With a real width axis or condensed cut*: **IBM Plex Sans** (width 75 to 100; digits tabular by default; `l` and `I` distinct; slashed or dotted zero), **Archivo** (width 62 to 125, the widest range free; plus Archivo Narrow), **Mona Sans** and **Hubot Sans** (GitHub; width 75 to 125), **Roboto Flex** (width 25 to 151, optical size, grade), Barlow in three widths, Fira Sans Condensed, Instrument Sans (width 75 to 100), Sofia Sans Condensed.
- *One width, very legible*: **Inter** and Inter Tight (`tnum`, slashed zero; default `l`/`I` alike, fixed by its ss02), **Geist** (`tnum`; ss03/ss05 fix `l`/`I`), Source Sans 3 (tabular by default, distinct `l`), Atkinson Hyperlegible Next (built for legibility, slashed zero), Public Sans.
- *Fail the tabular test* (no `tnum`, proportional digits): Libre Franklin, DM Sans, Oswald, Fraunces, Lexend.
- Fontshare's free licence (Satoshi and others) **forbids subsetting and format conversion** [stated, ITF Free Font License v2.0].

**Paid candidates** (prices read in the seller's own cart in a browser where given) [stated]:
- **Klim** (Söhne, with Söhne Schmal narrow and Söhne Mono in the collection; National 2 with Narrow, Condensed, Compressed; Founders Grotesk with Condensed and Mono; Untitled Sans; Tiempos): Web licence at **5,000 monthly unique users: one style US$60; a 16-style family US$432 after the automatic 55% package discount (US$960 list)** [measured in Klim's cart, `klim.co.nz/buy/soehne/` and `/buy/national-2/`, 2026-11-02 03:54 UTC; nothing bought]. The meter is average monthly unique users over three months; one-off fee; WOFF2 only [stated, Klim web licence]. Söhne lists `tnum` and slashed zero.
- **Grilli GT America** (Compressed, Condensed, Standard, Extended, Expanded, Mono; tabular figures in its tester), metered by unique monthly visitors, one-time fee: **price unread** (script-driven shop).
- **Dinamo ABC Diatype** (Compressed, Condensed and more), per domain with **no traffic limit**, priced by the buyer's company size: price unread; `tnum` not stated on its page.
- **Commercial Type Graphik** (eight widths), metered by unique monthly visitors, third-party hosting prohibited, generative-AI clause in its EULA: price unread.
- **Pangram PP Neue Montreal** (`tnum`, variable): "Licenses start at $40", metered by pageviews.

*Bears on the choice* [inferred]: the site is open to anyone with the address (Part A), so a traffic-metered licence is a bet on how many people open it; the room alone is far under 5,000, a shared link is not. A per-domain or free licence removes that question.

## 6. Desktop and phone

Law 4: components and ways of moving are chosen deliberately for each kind of screen; a way of moving that belongs to one is not carried to the other unchanged. What the field and the evidence above say belongs where [stated where cited, otherwise inferred]:

| Kind of component | Desktop | Phone | Evidence |
|---|---|---|---|
| Hover to preview (a state's races, a candidate's details) | Belongs, as a preview of what a click opens, never the only route | Does not exist; replaced by tap to select with a persistent panel | NN/g on tooltips; MDN `hover: none`; details.so confines hover to `@media (hover: hover)` |
| Geographic national map | Fits: room for callout boxes for small states | Small states fall below tap size; a tile grid, a map with a list beside it, or no map | 3.1, measured sizes; WSJ on blocky maps for phones |
| District hex map (435) | Possible as an overview | Exceeds the about 100 easily tappable targets a phone holds; better as a list grouped by state | NZZ/Zurich ICA 2023 |
| Seat bar (Senate, House control) | Wide, both sides with counts | Same bar, full width; it is one-dimensional and survives narrowing | S1: the bar is on every national page, desktop and phone |
| Race card (candidates, votes, %, how much is in) | In a grid or beside a map | One column; the unit that survives every width | S1: all sites stack cards on phones |
| Tables of races | Many columns | Fewer columns, condensed type, or a card list; tabular figures matter more as width shrinks | Section 5; S1 (NPR's tables become one column) |
| Navigation between national, state, race | Persistent top bar or side list; a menu can stay open beside the content (the details.so desktop drawer keeps the page visible) | A full-screen drawer or a sheet from the bottom; a pill row that scrolls sideways (Fox) | 4.1 measured; S1 |
| Opening a view (state, race) | Spring-shaped, about 0.5 to 0.8 s, page kept in sight | Shorter distances (the details.so drawer moves 40 px on a phone, 100 px on desktop) and the new view takes the whole screen | 4.1 measured |
| Gestures | none | Swipe to dismiss a sheet, retaining momentum (Rauno) | rauno.me |
| Calls timeline | A column beside the map (Fox 2024) | A collapsed strip or its own tab | S1 |

A tablet is an open point of the law (whether it is a phone or a desktop for the choice of components). The evidence suggests deciding by input rather than width: the details.so drawer switches hover by `@media (hover: hover)` and layout by width separately, so a tablet with a pointer gets hover and a touch tablet does not [measured, 4.1; inferred as a reading].

## 7. What could not be read

- **Bot checks or refusals, recorded and not retried:** NYT, AP (`apnews.com`), Reuters, Bloomberg, FT, Economist, Axios, WSJ, Sky, VoteHub, RealClearPolling, Nieman Lab, Medium, `open.nytimes.com`, Cook, Sabato, FlowingData, NICAR/IRE, Berkeley Graphics, Frere-Jones (403); USA Today (402); Yahoo, Observable, Sharp Type (429); Politico in a browser (Cloudflare "Just a moment" on two pages: the helper stopped and deleted those captures; Politico is read from four pages that curl returned). Pennsylvania, Arizona, Wisconsin, Maine and Alaska election sites; `washingtonpost.com` (no connection).
- **Behind payment:** the code and live previews of the seven Max navigation items at details.so (read from their public videos only).
- **Prices not published in a page's HTML:** GT America (Grilli), ABC Diatype (Dinamo), Graphik (Commercial Type) web licences; Flourish's live-data tier; Highcharts and amCharts exact plans. Klim's were read in its own cart.
- **Not yet done:** nothing was tested on a real phone; no prototype of a component was built; the Downballot's 2026 hexmap files (TLS error on `thedownballot.com`) and their terms; whether Census `cd119` carries the 2025–26 redraws (W4's field).
- **Two lapses by helpers, reported:** the typefaces helper made a second request to `berkeleygraphics.com` (homepage) after a 403 bot check on another path, which it counts as a retry; and its first CSS run sent a custom User-Agent string ("…research") to the Guardian, AP and NYT before it removed it. Neither got past a check; both stopped.
- No WebFetch was used anywhere in this work.

## 8. Sources

Each helper's notes file lists every URL with its UTC time and status. Read by W5 directly (2026-11-02, 03:42 to 03:56 UTC, curl unless stated): `details.so/llms.txt`, `/vault/category/navigation.md`, `/vault/category/free.md`, the eight navigation items' `.md` pages and preview videos (`inspo-sec-9072.b-cdn.net/vault-media/…mp4`), `/vault-previews/navigation-06/index.html` and its script (also rendered in Chromium), `/vault-previews/number-flow/index.html` and its script; `gsap.com/standard-license/`; `motion.dev/llms.txt`, `motion.dev/plus`; `raw.githubusercontent.com/barvian/number-flow` README and `package.json`; `Fyrd/caniuse` `view-transitions.json`, `cross-document-view-transitions.json`; `juliangarnier/anime` `package.json`; `pmndrs/react-spring` and `formkit/auto-animate` READMEs; `carbondesignsystem.com/elements/motion/overview/`; `vercel-labs/web-interface-guidelines` README; `emilkowal.ski/ui/great-animations`, `/ui/you-dont-need-animations`; `rauno.me/craft/interaction-design`; `klim.co.nz/buy/soehne/`, `/buy/national-2/` (rendered in Chromium, web licence and one style selected in the cart to read the price; nothing bought); Mobbin connector search (one query). In the record: `zwolk46/designsystembrain` `research/reviews/2026-10-24-ui-principles-behind-the-goal.md` (whole) and `research/midterms-site/survey/2026-11-02-S1-election-sites.md` (whole).

Mobbin's connector returned this notice with the search, reproduced as it asks:

> **Your Mobbin AI usage is high this month**
>
> Usage is unlimited during beta. If your usage stays at this level, you may need to purchase more credits once limits take effect. [View usage and plan options](https://mobbin.com/settings/billing-and-usage)

## 9. Where W5 stopped (2026-11-02 04:01 UTC)

Stopped on the coordinator's instruction of 04:00 UTC, relaying the maker's word (03:59 UTC) that the midterms system must run in a new project, not this one. Done: breadth in every section of the brief (catalogues, election components, maps, motion with the details.so menus measured first-hand, typefaces, desktop and phone). **Remains for a continuation** (the brief's second report): depth on the few candidates per kind; prices unread for GT America, ABC Diatype and Graphik web licences (their carts render in a browser, as Klim's did); the Downballot 2026 hexmap's files and terms; a check of any component on a real phone; throwaway motion prototypes (e.g. a seat bar crossing its marker, a vote count rolling with NumberFlow) to judge timing by watching. Helpers' raw downloads stayed in scratch and are not kept; their findings are in `notes/`.

**Stopped for good at 04:03 UTC** on the maker's word "Stop all running processes" (relayed by the coordinator). One fact read just before, kept here: Dinamo ABC Diatype web licence for a company under 3 people, read in Dinamo's own quote page in Chromium (nothing added to a bag or bought): Complete Family, 16 styles with variable font, 784.00 EUR (list 2,240.00 EUR, "Save 65%"); Essentials, 6 styles, 504.00 EUR; one style 140.00 EUR; prices excl. VAT; per domain, no traffic limit [measured, `abcdinamo.com/buy/diatype`, 2026-11-02 04:02 UTC]. GT America's shop URLs returned "page not found"; its price remains unread.

---

# Continuation (W5 in the project "Midterms", resumed 2026-11-02 04:10 UTC)

Sections 10 onward are the depth the continuation section of the brief asks for. Sections 1 to 9 above are kept as they were written; where a fact below corrects one above, it says so.

## 10. Facts read since resuming: prices, weights, the Downballot hexmap

### 10.1 Prices read at the seller's own page (nothing added to a bag beyond reading a price; nothing bought; no seller contacted)

| Item | Licence read | Price | Where, when |
|---|---|---|---|
| **Commercial Type Graphik** | Web, 1 domain, **up to 15K unique visitors a month**, one-time fee, perpetual | one style from **US$50**; one width family (e.g. Graphik Family, or Graphik Condensed Family, 18 styles) **US$400**; the whole collection (8 widths) **US$1,300** | the cart panel on `commercialtype.com/catalog/graphik`, Web ticked, rendered in Chromium, 2026-11-02 04:13 UTC [measured] |
| Graphik, next tier | Web, **up to 500K unique visitors a month** | one family **US$1,200**; collection **US$3,900**; tiers offered: 15K, 500K, 1m, 2m, 3m, 5m, 10m, 20m, 50m, 100m, unlimited | same panel [measured] |
| Graphik terms | EULA: licence for the named licensee only; web licence counted by domains and unique visitors a month; "Use of the Font Software with Generative or other Artificial Intelligence ("AI") services or in other AI programming is expressly prohibited"; the EULA's own gloss: the AI clause forbids using the font as training data, and "Referencing the font in a style guide or using it in CSS t[…]" (cut off in what was read) | — | EULA shown in the same panel [stated]. Whether an agent writing the site's CSS falls under the AI clause is not settled by what was read; the gloss suggests it does not [inferred]. |
| **Grilli Type GT America** | Web only (desktop set to none), **50k monthly visitors** | one style **US$50**; one subfamily (e.g. Standard or Condensed, 14 styles) **US$420**; full family (6 widths, 84 styles) **US$630** | `grillitype.com/shops/gt-america`, rendered in Chromium, the shop's own selects, 2026-11-02 04:16 UTC [measured] |
| GT America, higher tiers | Web only | 110k: style US$100, subfamily US$840, family US$1,260; 260k: US$200 / 1,680 / 2,520; 1 million: US$500 / 4,200 / 6,300. Tiers offered from 50k to 20 million | same [measured]. (The shop's default, 1–3 desktop computers plus 50k web, shows US$75 / 630 / 945.) |
| **Dinamo ABC Diatype** | Web, per domain, **no traffic limit**, company under 3 people | one style **€140**; Essentials 6 styles **€504**; Complete 16 styles with variable **€784**; excl. VAT | read 04:02 UTC by the first W5, section 9 [measured] |
| **Klim** (Söhne, National 2, Founders Grotesk) | Web, 5,000 monthly unique users | one style US$60; 16-style family US$432 | section 5 [measured] |
| **Motion+** (paid layer of the Motion library) | one developer, one payment; code under MIT once added to a site | **US$399 once**, "Lifetime updates"; teams of two or more billed yearly per seat | `motion.dev/plus` rendered in Chromium, 2026-11-02 04:20 UTC [measured]. Confirms the JSON-LD figure in 4.2. |
| **details.so** | Pro (Inspo only) / Max (Inspo + Vault code) / Lifetime | yearly billing: **US$9** and **US$19** a month; **Lifetime US$490 one-time**, now offered with a "Get Lifetime" button (it showed "Sold out" on 2026-10-24); quarterly was US$12 and US$25 a month on 2026-10-24 (record, not re-read); no refunds | `details.so/pricing` rendered in Chromium, 2026-11-02 04:20 UTC [measured]; licence: client and commercial sites allowed, no reselling (record of 2026-10-24) |

*What bears on the choice* [inferred]: a traffic-metered licence is a bet on how many open the link (Part A: anyone with the address). Graphik's lowest web tier is 15K visitors and GT America's 50k; the room is a few people, a link shared on the night is not bounded. Dinamo's per-domain licence and the free OFL faces carry no such bet. No paid face is needed for any measured property in section 11.6 (the free ones have tabular figures, narrow widths and distinct `1 l I`); a paid face would be bought for its look alone, which is the maker's choice (law 7a).

### 10.2 Weight of each candidate, against W6's proposed budgets

W6 proposed (section 6 of `research/stack/2026-11-02-W6-build-and-live-updates.md`): first view about **300 KB compressed** including the national map (53 KB) and fonts; **JavaScript about 100 KB** compressed. Measured here by bundling each candidate with esbuild 0.28 (minified, ESM, tree-shaken to the imports a results page would use) and compressing with gzip -9, 2026-11-02 04:08 UTC [measured]:

| Candidate | What was imported | gzip |
|---|---|---|
| React 19.3 + react-dom client | `createRoot`, `createElement` | **68.8 KB** |
| Preact 11.1 | `render`, `h` | **4.7 KB** |
| Motion 14.9, `motion/mini` (plain JS, Web Animations API only) | `animate` | **3.3 KB** |
| Motion 14.9, plain JS with springs | `animate`, `spring` | 25.2 KB |
| Motion 14.9 for React, `LazyMotion` + `domAnimation` | `m.div` | 30.3 KB (plus React) |
| Motion 14.9 for React, with layout animation (`domMax`) | `m.div` | 45.0 KB (plus React) |
| Motion 14.9 for React, full `motion` | `motion`, `AnimatePresence`, `LayoutGroup` | 47.4 KB (plus React) |
| NumberFlow 0.6.2, plain web component | `number-flow` | **5.2 KB** |
| NumberFlow for React | `@number-flow/react` | 6.2 KB (plus React) |
| GSAP 3.15 core | `gsap.to` | 27.6 KB |
| d3-geo 3.1 + topojson-client 3.1 | `geoPath`, `geoAlbersUsa`, `geoIdentity`, `feature`, `mesh` | **10.1 KB** |
| d3-selection + d3-transition | `select().transition()` | 12.4 KB |
| MapLibre GL JS 6.16 | `Map` | **287 KB** (plus a 10 KB stylesheet and its worker) |

*What it means* [inferred]: MapLibre alone is nearly three times the whole JavaScript budget, so a WebGL map cannot be in the first view on a phone under W6's budget; an SVG map drawn with d3-geo (10 KB) can. React leaves about 30 KB of the 100 KB for everything else, so React plus full Motion (116 KB) already exceeds the budget before the site's own code; Preact or no framework, plus CSS for most motion, `motion/mini` or NumberFlow (3 to 5 KB each) for what CSS cannot do, keeps the motion inside about 10 KB. The framework is W6's and the orchestrator's choice; these figures are what it costs the motion candidates below.

**Fonts** (free OFL faces, subset to Latin with the features a results page uses: `kern liga calt tnum lnum zero case` and the stylistic sets that fix `l`/`I`; WOFF2; fontTools 4.68, 2026-11-02 04:10 UTC) [measured]:

| Face | Axes in the file | Digits | WOFF2, full axes | WOFF2, axes cut to what a results page uses |
|---|---|---|---|---|
| IBM Plex Sans | width 75–100, weight 100–700 | tabular by default (no `tnum` needed) | 61.8 KB | width 75–100, weight 400–700: **40.8 KB**; one width (85), weight 400–700: **28.2 KB** |
| Inter | optical size 14–32, weight 100–900 | `tnum` | 68.3 KB | weight 400–700, optical size kept: **42.2 KB**; optical size fixed at 14: 27.3 KB |
| Archivo | width 62–125, weight 100–900 | `tnum` | 77.3 KB | width 62–100, weight 400–800: **48.2 KB** |
| Mona Sans | width 75–125, weight 200–900 | `tnum` | 107.9 KB | width 75–100, weight 400–800: 74.1 KB |
| Hubot Sans | width 75–125, weight 200–900 | `tnum` | 107.4 KB | — |
| Instrument Sans | width 75–100, weight 400–700 | `tnum` | 68.1 KB | 66.2 KB |
| Geist | weight 100–900 | `tnum` | 26.8 KB | weight 400–700: **17.5 KB** |
| Geist Mono | weight 100–900 | tabular (monospaced) | 20.8 KB | — |
| Source Sans 3 | weight 200–900 | tabular by default | 25.6 KB | — |
| Atkinson Hyperlegible Next | weight 200–800 | `tnum` | 30.4 KB | — |
| Public Sans | weight 100–900 | `tnum` | 23.4 KB | — |

So one variable family with a width axis costs about 40 to 50 KB, and a single-width family about 17 to 30 KB, of the 300 KB first view [measured]. (Correction to section 5: IBM Plex Sans has no `tnum` feature because its digits are already tabular; Source Sans 3 likewise. Neither needs the feature switched on.)

### 10.3 The Downballot hexmap: files and terms, read

- **The site is `the-downballot.com`** (hyphenated); the earlier TLS error came from `thedownballot.com`, which is not theirs [measured: certificate name mismatch]. The maps index is a public Google Sheet linked from `the-downballot.com/p/data` ("Maps"), read as CSV and XLSX exports, 2026-11-02 04:18 UTC [measured].
- **Congressional District Hexmap, version 3.2 (2026)**, by Daniel Donner for The Downballot: "Valid for 2026 only. This version has updated districts for CA, FL, NC, OH, TN, UT, and TX. AL, LA, and MO have not been changed with the new districts" [stated, the sheet's own text]. Files: shapefiles (districts; delegate districts; states), Web Mercator shapefiles, SVG with and without labels, images.
- **Licence: Creative Commons Attribution 4.0 International.** "Please provide a link to this page (https://the-db.co/maps) in any published material … free for you to download and use as long as you cite us as your source and link back to the source files." Donations asked, not required [stated]. (Correction to section 3.1, which had v1.x as CC BY-SA 4.0: the current terms are CC BY 4.0.)
- **Measured:** the v3.2 district shapefile has **435 records** with `GEOID` in the Census form (state FIPS + district, e.g. `0101`), `CDLABEL`, `STATEAB`, `STATENAME`, in WGS84. As TopoJSON (quantised 1e4) it is **154 KB raw, 37 KB gzipped**, before dropping fields or simplifying [measured, mapshaper].
- **The 50-State Tile Map** (two hexagons per state, "made with the Senate in mind"; "Inspired by the NPR tile map"; DC not included), version 1.0: also CC BY 4.0 with the same attribution [stated].
- **What bears on law 7** [inferred]: the hexmap is a cartogram, so its hexes are placed, not surveyed. For Missouri its v3.2 arrangement follows the 2022 plan, which is the plan that governs (W4 section 0 item 5). For Alabama and Louisiana, the maker of the map judged the new districts did not need new placement; whether a hex for AL-2 or LA-6 sits where a viewer would expect under the 2026 plan has not been checked. A cartogram tells a viewer *which* district and *roughly where*; if it is used, the check is that no district's hex sits in a part of its state the district does not touch.

## 11. Motion watched before it is recommended (throwaway prototypes, in scratch)

**How it was watched.** One page in scratch (plain HTML, Web Animations API, NumberFlow 0.6.2 and d3-geo for the map, us-atlas 10m states and counties as stand-in shapes; nothing from it is kept). Each prototype was triggered in headless Chromium, every animation on the page (including those inside NumberFlow's shadow DOM) was paused and stepped to fixed times, and each step was captured; the frame strips were looked at, and frame times were measured in real playback with Chromium's CPU throttling as a stand-in for a phone. **Limits:** I looked at frames and measurements, not at the motion on a real screen; nothing was run on a real phone; the shapes and numbers are stand-ins (the bar's seat counts and the vote counts are invented for the prototype and appear nowhere else). [measured unless marked]

### 11.1 What details.so's curve is, exactly

The drawer's opening curve, `linear(0, .005, .02 2.1%, .081 4.7%, .467 15.7%, … .994 72.3%, 1)` over 0.8 s (section 4.1), is a **critically damped spring**: x(t) = 1 − (1 + ωt)e^(−ωt) with **ω = 12.5 rad/s** fits all fourteen of its stops with a root-mean-square error of **0.0006** (in a physics library's terms: mass 1, stiffness about 156, damping about 25; no overshoot) [measured: least-squares fit to the curve read from `details.so/vault-previews/navigation-06/index.html`, 2026-11-02 04:25 UTC]. It reaches 47% of the way at 126 ms, 96% at 400 ms, 99.3% at 560 ms; the last 240 ms of its 0.8 s are a settle under 1%.

*Why it matters* [inferred]: every critically damped spring has the same shape, scaled in time, so the site can carry the maker's loved curve to every motion with one number: how fast it settles. A spring that settles in about 600 ms is details.so's own; one that settles in 250 to 300 ms is the same feel for frequent, small changes. This turns "precise, fluid, natural" from taste into a reproducible parameter. In section 4.1 the per-frame profile measured on the phone layout (21% at 91 ms) was of the clipped page's position, not of the curve itself; the curve's value at 91 ms is 0.31.

### 11.2 A seat bar crossing its majority mark

Prototype: a 100-seat Senate bar, Democrats from the left, Republicans from the right, uncalled grey between, a mark at the centre with "51 for majority" beneath. Two events: one call moving one seat (50 → 51), and a poll-closing batch (41 → 45 and 44 → 51 at once). Curves compared: details.so's own (800 ms), the same spring at about 270 ms, details.so's closing ease-out (510 ms), IBM Carbon's productive curve (240 ms), an overshooting spring, no motion. Frames: `shots/proto-seatbar-jump-frames.png`.

- **One seat is about 7 px on a 700 px bar and about 3.5 px on a phone** [measured]. Whatever its curve, a one-seat move is close to invisible; the eye notices the number. So the *crossing* cannot be carried by the bar's motion alone: the count beside it and the state of the mark must change too [inferred from the frames].
- **An overshooting (bouncy) spring is false information on a bar with a threshold** [measured]: at 150 ms the Republican segment has passed the mark, at 250 ms it has fallen back short of it, then it crosses again. For a moment the bar says majority, then not, then again. Law 5 calls decoration that imitates information a fault; this is motion that imitates a *false* event. Every candidate below is critically damped or an ease-out with no overshoot.
- **Text crossfaded in place is unreadable mid-change** [measured]: "51 for majority" fading into "Majority reached" over 160 ms leaves both overprinted for several frames. A label that changes should be swapped at once or moved (old out one way, new in), never faded in place.
- **Timing** [judged from the frames, inferred]: for the batch (10 seats, about 70 px), details.so's 800 ms spring reads as one deliberate movement and has crossed the mark by about 150 ms; the 240 to 270 ms versions read as a jump. A call is rare and meaningful (Carbon's "expressive" kind, section 4.3), so the slower spring fits it.
- **Smoothness:** 60 frames a second held throughout, at normal speed and with the CPU slowed fourfold [measured: median 16.7 ms, no frame over 20 ms].
- **What the crossing should do** [inferred, a candidate]: the bar moves on the spring; the number beside it changes at the start; the mark itself changes state when the segment passes it (for instance from a hairline to a solid tick in the party's colour), with no pulse, glow or confetti; and the words "control" appear only when a true source says so. Control of the Senate is decided by called seats plus the vice president's tie-breaking vote; the site can add up calls (arithmetic on true facts), but it should show the caller's own call of control where the source publishes one (W3's field).

### 11.3 A count changing when a batch of votes arrives

Prototype: a race card with two candidates; a batch arrives that changes both counts and percentages, puts the second candidate in the lead and moves "% of expected vote in" from 64 to 71. Variants: NumberFlow at its Vault default (900 ms), 450 ms and 250 ms; the whole number sliding out and the new one in (220 ms); an instant swap. Frames: `shots/proto-count-change-frames.png`.

- **A digit roller shows numbers that are not true** [measured]. NumberFlow rolls each digit separately, so mid-roll frames show values that never existed: going from 48.7% to 50.5%, frames read "54.6", "53.6", "46.0"; vote counts show mixed digits like "1,245,61…". At 900 ms these false values are on screen for most of a second; at 250 ms for about 150 ms. Law 7 allows processing for display "while nothing a viewer can read from the result at the size shown is false"; a percentage a viewer can read mid-roll is exactly that. [The finding is about the technique, which NumberFlow shares with every per-digit roller; a roller that counts through intermediate *values* (1,234,567 → 1,234,568 → …) shows false counts too.]
- **The whole-number slide shows only the old and the new value**, each partly clipped while moving, and is done by about 100 ms [measured]. It says "this changed" and, with direction, "up" or "down", without showing a false number.
- **Smoothness on a slowed CPU** (four times, the stand-in for a phone): NumberFlow at 900 ms fell to about 20 frames a second (18 of 20 frames over 20 ms) with only four numbers changing; at 250 ms it dropped 6 frames; the slide and the swap held 60 frames a second [measured, `requestAnimationFrame` intervals]. A results page updating a dozen cards at once would be worse with a roller [inferred].
- **The lead change** (rows trading places, moved with the spring) is followable when the rows are opaque and the rising row passes over the other; without that the two names overprint for about 100 ms [measured]. With the numbers also moving in the same rows at the same moment, the card is busy for its first 100 ms [judged from frames]; the candidate below separates them.
- **Proposed** [inferred from the above]: numbers change by the whole-value slide at about 200 ms (the spring, settling) or by an instant swap; never a per-digit roll. When the order changes, the rows move after the numbers have changed (starting about 150 ms later), on the spring at about 300 to 400 ms. The "% in" bar extends on the same spring. None of it runs unless a new batch has actually arrived (law 5).

### 11.4 Moving from the country to a state

Prototype: a national state map (Albers USA, stand-in us-atlas shapes); pressing Michigan zooms the map to the state (a transform on one SVG group, strokes kept at constant width), other states fade to 12%, and Michigan's internal lines (counties, standing in for districts) fade in from 30% of the motion. Desktop 960 px with details.so's curve (800 ms); phone 390 px with the fast spring (270 ms). Frames: `shots/proto-country-to-state-desktop-frames.png`, `-phone-frames.png`.

- **Continuity works** [judged from frames]: the state pressed grows into the view, so where it sits in the country is never lost (the details.so point 2 of section 4.1). On desktop Michigan is legible by about 150 ms and settled by about 400 ms.
- **On the phone the 270 ms version is too abrupt for a fivefold zoom**: half the zoom happens in the first 33 ms, two frames [measured]. The details.so drawer keeps the same duration on the phone and shortens the *distance* (section 4.1); a zoom's distance cannot be shortened, so the phone should keep the slower spring for this navigation [inferred]. This is opened by a press, not by data, so it is "productive by frequency" but large in scale.
- **Smoothness:** 60 frames a second on desktop at four times slowed CPU; on the phone width at three times pixel density, one dropped frame at four times slowed and four at six times [measured]. An SVG map of 50 states and about 80 internal shapes zooms smoothly; the full 435-district national layer zooming at once was not tested.
- **A zoom is only true at rest**: mid-zoom the map is a picture of geography, not a claim about results, so it raises no law 7 question; the district shapes must come from the governing plan (W4 section 0 item 5) and be drawn only when the zoom settles [inferred].

### 11.5 The timings proposed, and why (candidates for the orchestrator, not chosen)

All are critically damped springs (no overshoot), given by the time they take to settle within 1%; all are skipped under `prefers-reduced-motion` (changes then happen at once), and none runs except on a real event or a person's press.

| Motion | Real event it signals | Proposed | Why |
|---|---|---|---|
| Opening a state or a race (zoom or the pressed thing becoming the view) | the person's press | spring settling in about **600 ms** (ω ≈ 12.5, details.so's own); same on phone | the maker's loved curve; continuity; the phone keeps the duration because a zoom's distance is fixed (11.4) |
| Closing, going back | the person's press | ease-out `cubic-bezier(.17,.84,.44,1)` about **450–500 ms**, or the spring at about 400 ms | details.so closes faster than it opens (4.1 point 4) |
| A call (race card fills, seat added to the bar) | a race called by the named caller | spring about **600 ms**; the mark changes state as the bar passes it; label swapped, not faded | rare and meaningful (Carbon "expressive"); no overshoot (11.2) |
| Control decided | the caller's call of control | the same as a call; nothing extra that moves on its own | the night's biggest moment needs to be unmistakable, which is a matter of what the page says, not of more motion [inferred] |
| New votes in a race | a new batch from the source | whole-number slide about **200 ms**, or instant | no false intermediate numbers (11.3); frequent, so short (Kowalski, Rauno, section 4.2) |
| Lead changes | the order of candidates changes in the source's numbers | rows move on the spring about **300–400 ms**, starting about 150 ms after the numbers | the eye can follow who passed whom (11.3) |
| "% in" bar | a new expected-vote figure | extend on the spring about **300 ms** | small and frequent |
| Polls close in a state | the hour, confirmed at the source | state changes at once (text and colour), no motion | about 15 times, predictable; motion would add nothing [inferred] |
| Nothing new | — | nothing moves; "updated" time changes silently | law 5; the maker's named fault of a dot that pulses for nothing live |

## 12. The few candidates per kind, for desktop and for phone

Each kind: two or three candidates, what each serves for the room, the real event any motion signals (law 5), its weight against W6's budgets (first view about 300 KB compressed, JavaScript about 100 KB), its licence and price, and the evidence. Nothing here is chosen (law 6b; `_COMMON.md` 3). Where I lean, it is marked as my reading, for the orchestrator to weigh.

Two measurements used throughout [measured, 2026-11-02 04:30 UTC]:
- **Tap size.** On a 390 px phone the Downballot hexmap's median district is about **9 px across** (smallest about 57 px²); at 1,280 px it is about 29 px. A national geographic map at 360 px leaves Rhode Island about 5 × 7 px and DC about 1 px² (section 3.1). Apple's and WCAG 2.2's minimum targets are 44 pt and 24 px. *(Hexmap figures from its own coordinates with a cos 38° correction of longitude; approximate to about 10%.)*
- **One seat on a seat bar.** Senate, 100 seats: about 7 px on a 700 px bar, 3.5 px on a 350 px phone bar. House, 435 seats: about 1.6 px and 0.8 px. A single call is carried by the number, not by the bar's movement (11.2).

### 12.1 Moving between national, state and race views

| Candidate | Desktop | Phone | Motion and its event | Weight, licence |
|---|---|---|---|---|
| **N1. One page that zooms: the national view's map or list *is* the menu; pressing a state zooms it into the state view; pressing a race opens its card in place** | map or tile grid with a list beside it; state view keeps a strip of the country in sight; back returns by reversing the zoom | the same, full width; the state view takes the whole screen; a bottom bar holds "Country / [state] / back" | the person's press; spring settling in about 600 ms open, about 450 ms back (11.4, 11.5); `prefers-reduced-motion` jumps | SVG transform with `motion/mini` or plain Web Animations, about 0–3 KB; free |
| **N2. Separate pages with the View Transitions API** (each state and race has its own address; the pressed shape or card morphs into the next page) | same-document transitions, or cross-document where supported | same; on browsers without support the page simply changes | the press; the same spring written as a CSS `linear()` easing | 0 KB of library; same-document 92.9% of global usage, cross-document 86.8%, not Firefox (section 4.2); free |
| **N3. A persistent menu of states and races in the details.so drawer pattern** (page shrinks aside, menu revealed) | a 450 px drawer with the page kept visible, dimmed (4.1) | a full-width drawer; the page clipped away | the press; details.so's curve exactly (11.1) | its free Reveal Navigation is plain HTML, CSS and GSAP (72 KB script, GSAP 27.6 KB gzip of it); the paid Vault items need the Max plan (US$19 a month yearly, US$490 lifetime) |

*Serves:* law 4's fewest steps, and law 10's races "reached in the fewest steps from where the site opens". In every candidate the opening view can hold the Chappaqua races and the Michigan Senate race in its first screen as ordinary rows of the race list, with nothing else made special [inferred from law 10]. *My reading:* N1 and N2 are the same idea (the thing pressed becomes the view; continuity, 4.1 point 2) built two ways, and every state having its own address (N2) lets the room share a link to "New York" on the night; N3 is the pattern the maker loves, but a menu of 50 states is a list to scroll, which N1's map or grid replaces with one press. They combine: N2's addresses, N1's zoom as the transition, and the drawer's curve.

### 12.2 The race card

| Candidate | Desktop | Phone | Motion and its event | Evidence |
|---|---|---|---|---|
| **C1. NPR-style card**: candidates in order of votes, party, votes, percent, a winner mark; a footer "x% of expected vote in · updated hh:mm · called by [caller] at hh:mm"; footnotes only when true | in a grid of 2–3 columns beside the map | one column, the full width; the count column in tabular figures | new batch: whole-number slide about 200 ms or instant; lead change: rows move about 300–400 ms after; call: the winner mark appears and the row tints, spring about 600 ms (11.3, 11.5) | NPR code and pages (section 2); `shots/el-npr2024-*` |
| **C2. A row in a table of races** (one line per race: name, leader, margin, % in, called by) | the main view for the House; sortable | collapses to name, leader, margin, % in; tap opens C1 | as C1, smaller; no row motion except reorder when a sort is active | NPR's Senate board groups (section 2); 270toWin's table view for 435 districts |
| **C3. A card with the candidates' side bars** (a horizontal bar per candidate's share) | where there is room | the bar under each name | the bar extends with a new batch, spring about 300 ms | common across S1; adds ink but shows margin at a glance |

*What a card must carry* (law 3) [stated in sections 2 and the AP pages read there]: who is running; votes and percent; how much is in, as the source states it (never 0 or 100% while counting continues: NPR's "<1" and ">99"); who called it and when, and a call can be withdrawn so the mark must be removable; runoff and ranked-choice states. *Weight:* HTML and CSS; no library. *Faults to avoid* (`RULINGS.md`): no drop shadow between cards (a hairline or space separates them), no pulsing "live" dot, no numbering of cards. *Phone:* C1 is the unit that survives every width (section 6); C2 is the faster scan on desktop for 435 House races.

### 12.3 The seat count (Senate, House, governors)

| Candidate | Desktop | Phone | Motion and its event | Evidence |
|---|---|---|---|---|
| **S1. A single bar**, party from each end, uncalled between, a mark at the centre, the counts and "51 for majority" / "218 for majority" in words; holdovers (seats not up) shown as a distinct, paler part of each side, named in words | wide, on every view (national, state) | the same bar full width, one line of counts above it | a call: the side grows on the spring (about 600 ms); the mark changes state when crossed; never an overshoot (11.2) | NPR (holdovers from a hand-kept sheet), Politico ("28 seats not up"), Guardian (section 2) |
| **S2. A row of seat squares or a parliament arc** (one mark per seat) | Senate (100) fits; House (435) is dense | Senate only; the House becomes 0.8 px marks | each seat fills when called; the fill can be per seat, so a call is visible as one square changing | common; the arc wastes the phone's width [inferred] |
| **S3. Numbers alone** ("Dem 45 · Rep 51 · 4 uncalled · 51 for majority") | beside S1 | as the primary on the smallest phones | none (the whole-number slide) | a call of one seat is read from the number anyway (11.2) |

*Real event:* a call by the named caller; control decided only on the caller's own call or the arithmetic of calls plus the tie-break (11.2). *Weight:* HTML and CSS, 0 KB. *My reading:* S1 with S3's numbers on both screens; S2 as the Senate's alternative on desktop, where its per-seat change makes one call visible, which S1 cannot do (one seat is 7 px).

### 12.4 How much is in, and expected vote

| Candidate | Both screens | Evidence and constraint |
|---|---|---|
| **E1. A thin bar plus words**: "71% of expected vote in (AP estimate)" | the bar under the card; the words carry the fact | the estimate "can and will fluctuate" (AP, section 2), so the bar can shrink; it must move both ways on the spring and never imply 100% before the source says so; NPR's "<1" and ">99" |
| **E2. Words only** | for the table rows (C2) and the phone | the cheapest truthful form |
| **E3. Shading the leader only after half the expected vote is in** | map fills and table rows | NPR's rule (section 2); prevents an early lead reading as a result |

*Constraint (law 7):* the measure is the source's own (AP's `eevp`, a state's "precincts reporting", civicAPI's equivalent per W3); different sources measure different things, and the label must say which [inferred]. *Weight:* 0 KB. *Motion:* a new figure from the source, the bar on the spring about 300 ms.

### 12.5 Calls and their timeline

| Candidate | Desktop | Phone | Motion and its event |
|---|---|---|---|
| **T1. A column of calls**, newest at top: "21:04 · Senate · Michigan · El-Sayed (D) wins · called by [caller]" | beside the map or the seat bar (Fox 2024, S1) | a strip under the seat bar showing the last call, opening to the full list as a sheet from the bottom | a real call: the new row slides in from the top on the spring (about 400 ms); the rows below move down; nothing else moves |
| **T2. Calls stamped on each card only** (NPR) | no list | no list | the card's own call motion (12.2) |
| **T3. A poll-closing schedule that turns into the calls list** ("20:00 polls close in 16 states" becomes the calls made at that hour) | the column of T1 grouped by the hour | the strip | the hour (confirmed at source, W4's `poll-closing-2026.csv`) changes the group's state at once; calls slide in as in T1 |

*Serves:* the room asks "what just happened?" more than any other question on the night [inferred]; the Guardian's call strip is the only true calls feed read in the field (section 2). *Fault to avoid:* text scrolling across the screen (a ticker), the maker's named fault; T1 is a list that grows, not a ticker. *Weight:* 0 KB. A withdrawn call is a real event too: the row is struck through and says so, not deleted [inferred, from NPR's note that a call can be withdrawn].

### 12.6 The map (or no map) and its tool

| Candidate | Desktop | Phone | Weight | Licence, source of shapes (law 7) |
|---|---|---|---|---|
| **M1. Geographic state map** (Albers USA, insets), coloured by where contests are and by result; small north-eastern states and DC given callout boxes | yes; hover a state for a preview of its races, click to open (N1) | the map as a picture with a list or grid beneath for tapping; small states only through the list | states 10m TopoJSON 29.5 KB gzip (us-atlas, from Census); d3-geo + topojson-client 10.1 KB | Census cartographic boundaries (public domain); us-atlas ISC |
| **M2. Tile grid** (one square per state, NPR or WaPo layout; or the Downballot two-hexagon Senate tile map, one hex per seat, the seat not up shown as such) | as an alternative overview | **fits the phone**: a tile grid 11 to 12 states wide on a 390 px screen gives tiles of about 30 to 32 px, above WCAG's 24 px minimum though under Apple's 44 pt [inferred: 358 px of usable width ÷ 11–12 columns] | a few KB of positions | Downballot tile map CC BY 4.0 with a link to `the-db.co/maps` (10.3); NPR's layout open in its repositories |
| **M3. House hex cartogram** (Downballot v3.2, 2026) | an overview of 435 seats at about 29 px each at 1,280 px | **not tappable** (about 9 px a district); a picture with the table (C2) for tapping, or not shown | 37 KB gzip as TopoJSON (10.3) | CC BY 4.0, attribution and link; AL and LA hexes not rearranged for 2026, MO follows the 2022 plan (10.3) |
| **M4. District map inside a state** (true shapes) | after the zoom (N1), districts drawn at rest | the same, full screen; urban districts become a list beside | per state on demand (W6: about 1 km detail; 53 KB for all House shapes at about 5 km) | Census `cd119` for 40 states and Missouri; TIGER 2026 simplified by us for the nine redrawn (W4, section 0 item 5) |
| **M5. No map: seat bars, calls list and a table** | possible | the most direct on a phone | 0 KB | none |

*Tools* (section 3.2 and 10.2): **d3-geo with TopoJSON drawn as SVG** costs 10 KB and draws shapes exactly from the files we choose, animates by transform (11.4, 60 frames a second at four-times slowed CPU on desktop) and styles with CSS; **MapLibre GL** is 287 KB, nearly three times the JavaScript budget, and earns it only with pan and zoom over thousands of shapes; Mapbox costs money past 50,000 loads a month; deck.gl warns of memory on phones. *Law 11's ideas*, as the evidence now stands [inferred from sections 3.3, 11.4 and the tap sizes above]: (a) a national map of where the contests are serves desktop (familiar, an overview; Cai and Kay), and on a phone a tile grid serves it better because states can be pressed; (b) hovering a state belongs to desktop only, as a preview of what a click opens, under `@media (hover: hover)`; (c) clicking into a state works on both, with the zoom keeping the state's place (11.4), and the district map is where law 7 bites (the governing plan; Missouri). Against all three: the House is 435 seats that no phone map can make pressable, so the House's phone view is the table whatever map is chosen.

### 12.7 Typefaces

Measured facts in sections 5 and 10.2. The width of "1,234,567" in tabular figures at 15 px, regular weight [measured, fontTools, 2026-11-02 04:31 UTC]: Inter 76.1 px; Public Sans 82.5; IBM Plex Sans 71.2 (width 100), 67.0 (85), 64.1 (75); Geist 69.0; Archivo 68.0 (100), 55.1 (75); Mona Sans 55.0 (75); Instrument Sans 58.9 (75); Source Sans 3 59.7. On a 390 px phone row with a name, a count and a percent, 20 px saved per count is the difference between a count fitting at 15 px or shrinking [inferred].

| Candidate | Why for this site | Weight | Licence, price |
|---|---|---|---|
| **F1. One family with a width axis: Archivo** (width 62–125) **or Mona Sans** (75–125) | condensed for phone tables and the scoreboard, normal for text, from one file; `tnum`; Archivo has a `zero` (slashed zero) feature, Mona Sans has none [measured: the fonts' GSUB tables; Inter and Plex have `zero`, Geist and Instrument Sans do not] | Archivo cut to width 62–100, weight 400–800: 48.2 KB; Mona Sans 75–100: 74.1 KB | SIL OFL 1.1, free |
| **F2. IBM Plex Sans** (width 75–100) | digits tabular by default, `1 l I` distinct, slashed or dotted zero; narrows letters more than digits | 40.8 KB (both axes cut); 28.2 KB at one width | OFL, free |
| **F3. Inter or Geist**, one width, with a narrow sibling for tables (Inter Tight; or Geist with Geist Mono for counts) | the most legible single-width faces measured; Geist is the lightest file | Inter 42.2 KB; Geist 17.5 KB | OFL, free |
| **F4. Paid: Graphik (with its condensed widths), GT America (Standard + Condensed), ABC Diatype, Söhne + Söhne Schmal** | a look the maker may prefer; all have tabular figures where stated | similar to the free ones per style | Graphik US$400 a width family at 15K visitors (US$1,200 at 500K); GT America US$420 a subfamily, US$630 all six widths at 50k visitors (US$2,520 at 260k); Diatype €504–784 per domain, no traffic limit; Klim US$432 a family at 5,000 users (10.1, section 5) |

*My reading:* the measurable properties (tabular figures, a narrow width for the phone, distinct `1 l I` and `0 O`, file size) are all met by free faces; a paid face would be chosen for its look, which is the maker's to decide with prices (law 7a), and only a per-domain licence (Diatype) carries no bet on traffic.

### 12.8 One candidate set, weighed against the budget (an example of what fits, not a choice)

First view on a phone, compressed: Preact 4.7 KB + `motion/mini` 3.3 KB + d3-geo and topojson-client 10.1 KB + the site's own code (unknown; W6 to measure) ≈ **18 KB of libraries**; a free variable face with a width axis 41–48 KB; national states 29.5 KB (or a tile grid, a few KB); results data per W6. That leaves most of the 300 KB for data and the site's own code [measured parts, inferred sum]. With React (68.8 KB) and Motion for React with layout animation (45.0 KB) the libraries alone are 124 KB, over the JavaScript budget before any of the site's own code. The motion proposed in 11.5 needs none of Motion's React layer: springs written as CSS `linear()` easings and the Web Animations API cover all of it, as the prototypes did.

## 13. What could not be done or read in the continuation, and where W5 stands (2026-11-02 04:30 UTC)

- **Second report made** at about 04:30 UTC (sections 10 to 12), to the orchestrator and in this thread.
- **Not done:** nothing was run on a real phone (Chromium's CPU throttling stood in for one, 11.3 and 11.4); the motion was judged from stepped frames and frame times, not watched on a screen by a person; the full 435-district layer was not zoomed; the hexmap's Alabama and Louisiana placement was not checked against the 2026 plans (10.3); the site's own code weight is W6's to measure.
- **Not read:** Commercial Type's EULA gloss was cut off mid-sentence where it addresses CSS use (10.1); the seven paid details.so navigation items remain read from their videos only.
- **A lapse, reported:** one batch of `curl` requests (Commercial Type and Grilli Type pages, 04:11 UTC) carried a browser's User-Agent string; no bot check was met or passed, and every later request used curl's own or Playwright's default.
- **Free accounts or keys opened:** none. **Purchases or messages to sellers:** none.
- **Instructions without a reason:** none found in the brief or `_COMMON.md`. One tension, not a missing reason: `_COMMON.md` 9 says to push to `main`, and this session's harness designates the branch `claude/project-thread-buk6pm`; W5 pushes each commit to both, so `main` carries the record as `_COMMON.md` asks.
- **Next** (named by the orchestrator at 04:30 UTC, done in section 14): the hexmap's AL and LA placement; a type specimen at phone sizes; a View Transitions version of country-to-state; a call landing and a count arriving, with a stale source and a withdrawn call.

## 14. Deepening named by the orchestrator (04:30 UTC): hexes, type at phone sizes, View Transitions, a call and a count truthfully

*From 2026-11-02 04:32 UTC every request is sent with an honest User-Agent (curl's own, or Playwright's default), on the orchestrator's word.*

### 14.1 The Downballot hexmap's Alabama and Louisiana against the 2026 plans

**Method** [measured, 2026-11-02 04:40 UTC]: for each state, the hexes' outline was fitted to the state's real extent (a linear stretch of its bounding box, longitude scaled by the cosine of the state's latitude), and each district's hex centre was then tested against the real districts of two plans: Census TIGER/Line 2025 `cd119` (the plan before) and TIGER/Line 2026 `cd120` (the plan for 2026, which W4 found right for AL and LA). Three scores: the hex centre falls inside its own district; the nearest real district centre is its own; and, for every pair of districts, whether the hexes keep the real east–west and north–south order. The stretch is crude, because a cartogram enlarges cities on purpose, so the scores compare plans with each other rather than grade the map. **The method was checked on Missouri**, whose hexes the map's maker drew for the 2022 plan: they agree better with the 2022 plan than with the 2025 plan (pairwise order 22 of 28 against 18 of 28; nearest centre 5 of 8 against 4 of 8), as they should.

How much each state's districts changed between the two files (area of difference ÷ area before) [measured]: Alabama 1: 44%, 2: 83%, 3–5: 0%, 6: 7%, 7: 39%; Louisiana 1: 22%, 2: 62%, 3: 21%, 4: 39%, 5: 55%, 6: 139%.

| State | Against the plan before (`cd119`) | Against the 2026 plan (`cd120`) | Reading |
|---|---|---|---|
| **Alabama**, 7 districts | inside own district 6 of 7; nearest own 7 of 7; pairwise order 19 of 21 | **the same**: 6 of 7; 7 of 7; 19 of 21 | the 2026 changes (districts 1, 2, 7) move district shapes but not where each district's *centre* lies relative to the others; the hexes place every district where it is under the 2026 plan (district 1's centre falls in Mobile Bay, outside every district, under both) [measured; inferred reading]. **Usable for 2026.** |
| **Louisiana**, 6 districts | inside own 5 of 6; nearest own 6 of 6; pairwise 11 of 15 | inside own **4 of 6**; nearest own **4 of 6**; pairwise 12 of 15 | under the 2026 plan, **the hex for LA-2 sits where LA-6 is, and the hex for LA-6 sits where LA-5 is** [measured]. A viewer reading the hexmap would put two of Louisiana's six districts in the wrong part of the state. |

*What bears on law 7* [inferred]: the hexmap is not a boundary, but a viewer can read "where in the state" from it, and for Louisiana under the 2026 plan two districts would be read wrongly. If the hexmap is used (desktop overview, M3), Louisiana's six hexes would have to be rearranged by us to the 2026 plan (moving labels among six hexes, a change of arrangement, not of shapes), or Louisiana shown without the within-state arrangement; and since the map is CC BY 4.0, an adaptation is allowed with attribution and a note of the change [stated, CC BY 4.0]. Alabama needs nothing; Missouri is right for 2026 as drawn.

### 14.2 The free faces at phone sizes

Specimen `shots/type-phone-specimen-free.png` (390 px, rendered at twice density; invented numbers, labelled as such): a Senate count at 34 px, a race card at 15 px, a footer at 12 px, two table rows at 13 px, and the test string `Il1| O0 8B 5S`, in Archivo (width 100 and 75), IBM Plex Sans (width 85), Inter, Mona Sans (width 75), Geist and Source Sans 3 [measured: rendered with the subset files of 10.2]. What it shows [judged from the specimen]:
- **IBM Plex Sans at width 85** keeps the most distinct `I`, `l`, `1` (serifed capital I, tailed l) and a clear `0`/`O` at 12 to 15 px, and fits the row with room; it reads as the most "data" of the set.
- **Source Sans 3** is narrow by default, tailed `l`, calm at 12 px; its capital `I` and `l` are distinct.
- **Archivo at width 75** fits the most in a row and is strong as the 34 px count, but its 12 px footer is tight; **at width 100** it is open and even, with `I` and `l` alike.
- **Mona Sans at width 75** is the most condensed; its zero is slashed by default (the specimen shows it, though the font has no `zero` feature), and its 12 px footer is hard to read at phone size.
- **Inter and Geist** are the widest: "1,327,410 50.5%" fills a 390 px row at 15 px, and `I` and `l` are alike unless a stylistic set is switched on.

So for a phone table, Plex Sans (85) and Source Sans 3 hold legibility best at the small sizes, and Archivo or Mona Sans at a narrow width serve the scoreboard numerals; a family with a width axis (Archivo, Plex) can do both from one file [inferred].

### 14.3 The View Transitions version of country-to-state (N2), against the zoom (N1)

Prototype: the national map with Michigan as a separate element named for the transition; the state view is a new DOM with Michigan large and its counties; `document.startViewTransition` with the group animated on the same critically damped spring (648 ms), the rest of the page crossfading in half that [measured]. Frames: `shots/proto-country-to-state-viewtransitions-desktop-frames.png`, `-phone-frames.png`.

- **What it looks like:** Michigan lifts out of the map and grows into place while the rest of the country **stays the same size and fades**; in the zoom (11.4) the whole country grows with Michigan, like a camera moving in. The zoom keeps the spatial relation (Ohio below, Wisconsin to the west, sliding off the edges); the view transition keeps only the state [judged from frames].
- **It crossfades two pictures:** the new state's county lines appear inside the small Michigan by 66 ms, dense and shrunk, while the old one fades; text in the same place overprints mid-change ("Michigan" over the old label at 100 ms), the fault seen in 11.2 [measured].
- **Smoothness:** on desktop at four times slowed CPU, 16 of 33 frames took over 20 ms (the zoom: none of 55); on the phone width, one long frame at the start (the snapshot), then 60 frames a second [measured; headless Chromium rasterises in software, so the view transition's compositing may cost less on a real GPU].
- **What it gives that the zoom does not:** it works between two *pages* (cross-document; Chrome 126+, Safari 18.2+, not Firefox, 86.8% of usage, section 4.2), so every state can have its own address with no script for the motion at all; where unsupported, the page simply changes.

*My reading* [inferred]: the zoom (N1) is the closer match to what the maker loves (continuity of the whole page, as the details.so drawer keeps the page in sight) and ran smoother; the view transition is the cheaper way to animate between real pages. They combine: separate addresses for sharing, and within the page the zoom as the transition (the state view can still be its own address with the History API).

### 14.4 A call landing and a count arriving, timed with the spring; a stale source; a withdrawn or changed call

Prototype: five copies of one phone race card (invented numbers, labelled), each given one event; all timings are the critically damped spring of 11.1 (a call's tint on ω = 13.5, settling in 600 ms; numbers on ω = 36, about 225 ms) or details.so's closing curve (450 ms). Frames: `shots/proto-race-card-events-frames.png` [measured unless marked].

| Event (what is real) | What the screen shows | Motion |
|---|---|---|
| **A batch of votes arrives** (the source's figure changed) | new counts and percentages; "% in" and "updated hh:mm" in the source's own time (W6 section 5: never the site's fetch time) | each changed number slides, old out, new in, about 225 ms; done by about 100 ms; nothing moves for a number that did not change |
| **The race is called** (the named caller's call appears) | a check mark beside the winner at once; the footer says "Called for [candidate] by [caller] at [time]" | the winner's row fills with a pale party tint from left to right on the 600 ms spring: half filled by 50 ms, settled by about 400 ms. The fill is the event; nothing repeats or pulses afterwards |
| **The call is withdrawn** (the caller retracts; AP's feed can, NPR noted) | the check mark goes at once; the footer keeps the history: "AP withdrew its call for [candidate] at 23:05. Not called." | the tint retracts on the 450 ms closing curve (closing faster than opening, 4.1) |
| **The caller changes its call** (civicAPI moved its `winner` flag with no marker, W3: VA HD-73, 43 minutes) | the site compares each poll with the last and, when the winner differs, says so in words: "civicAPI changed its call to [B] at 02:27 (it had called [A] at 01:44)"; civicAPI's history endpoint dates each flip (W3 section 6a), so the times are the source's own | A's tint retracts (450 ms), then B's fills (600 ms, starting 250 ms later), so the eye sees the call move from one to the other [judged from frames: readable as one movement] |
| **The source has gone quiet** | the figures stay, greyed, with a sentence: "No new count from the source since 21:47 (18 min). Figures are as of then." | **none**: nothing pulses, blinks or spins; the change is in words and in the grey (law 5; the maker's named fault of a dot that pulses for nothing live) |

*Two readings for the orchestrator* [inferred]:
- **"Stale" should distinguish two cases** that W6's rule (section 5: no answer *or* no change for longer than the normal cadence) treats alike: the site **cannot reach** the source (the site's own fetch fails or times out), which is a fault of the site's knowledge and is said as such ("Can't reach [source] since 21:47; showing figures from then"); and the source **answers but reports nothing new**, which is often true and normal (a county pausing its count for an hour), so saying "stale" would imply a fault that is not there. In the second case the source's own "as of" time already tells the truth; a note is warranted only when the source's *own* timestamp stops advancing while it claims to be live.
- **A call made by a desk the site relays carries the desk's name every time it is shown** (law 3; W3's finding that civicAPI's call can be wrong for 43 minutes): the tint says "called", the words say by whom. A withdrawn or changed call is a real event and gets the same weight of motion as a call, so the room is not left with a check mark that the source has taken back.

## 15. Paused (2026-11-02 04:36 UTC)

The orchestrator took in section 14 and asked W5 to stop until it names more work, with this thread kept open. Its draft plan now includes the stale rule from 14.4: a note appears only when the site cannot reach the source or the source's own clock stops. Everything is pushed. The throwaway prototypes stay in scratch and are not kept.
