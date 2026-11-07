# W5: hierarchy and components (Continuation 2): research

**W5, 2026-11-02, from 13:09 UTC.** This is the evidence for `DESIGN-SPEC.md`, which cites it as "R s.N". The brief is `briefs/2026-11-02-W5-design-field.md`, "Continuation 2". The rulings are the maker's of 13:08, 13:17 and 13:21 UTC (`RULINGS.md`, read whole). Every fact is marked [measured], [stated], [vendor claim] or [inferred].

## 1. Method

- **The build.** `build/site` was checked out as a worktree in W5's scratch space: first at 8b41189, then at fd9e65c (13:16 UTC), which includes W9's outline fix 819c125 and the shoreline boundaries c5a3b6f. It was built with `npm ci` and `vite build` and served with `vite preview`.
- **What was shot.** Each view with `?fixtures`: `/`, `/mi`, `/mi/senate`, `/senate`, `/house`.
  - Desktop at 1280 × 900 (dpr 1).
  - Phone at 390 × 844 (dpr 2, touch, isMobile).
  - Both in Playwright's Chromium, full page.
- **The type audit (s.2).** Each visible text node's computed `font-size`, `font-weight` and `font-variant-numeric` were read, weighted by character count.
- **The weights (s.4).** Each candidate was bundled with esbuild (`--minify`, `--format=esm`), aliased to `preact/compat` where it is a React component, then compressed with `gzip -9`.

## 2. Type on the built page [measured]

Size / weight, then characters set in it. `tab` means tabular figures.

| view | combinations | sizes in px | largest |
|---|---|---|---|
| country, desktop | 16 | 10.5, 11, 12, 13, 14, 15, 16, 16.8 | 16.8 / 600 (section headings, 70 characters) |
| country, phone | 15 | 11, 12, 13, 14, 14.4, 15, 16, 16.8 | 16.8 / 600 |
| state `/mi`, desktop | 13 | 11 … 16.8, 25.6 | 25.6 / 600 (the name, 8 characters) |
| race `/mi/senate`, desktop | 9 | 13 … 17, 25.6 | 17 / 600 tab (the shares) |
| Senate, desktop | 12 | 12 … 16, 25.6 | |
| House, desktop | 15 | 11 … 16.8, 25.6 | |

- **Country, desktop, most used first:**
  - 14 / 400: 1,781
  - 13 / 400: 1,093
  - 15 / 600: 667
  - 13 / 400 tab: 545
  - 14 / 400 tab: 495
  - 15 / 400: 386
  - 12 / 400: 296
  - 14 / 700: 215 (the seat counts "Dem 35")
  - 16 / 400: 139
  - 10.5 / 500: 82 (map codes)
  - 14 / 600 tab: 77
  - 16.8 / 600: 70
  - 14 / 600: 55
  - 13 / 600: 51
  - 16 / 600: 28
  - 11 / 400: 18
- The same figures are set both tabular and not (13 / 400 and 13 / 400 tab, for example).
- `styles.css` declares the face at `font-weight: 400 600`, so the 700 above is outside the loaded range.
- The raw output is the session's `typeaudit.js` run, 13:19 UTC.

## 3. The views as built, desktop and phone [measured: shots; stated where read in source]

- **Country, desktop.**
  - Order: header (wordmark, four tabs, a State select); the fixture banner; a row holding only "Pause updates"; three seat bars; then two columns.
  - The left column holds "Where the races are" (the map, a legend of six keys, a two-line instruction, a credit) and "Senate races".
  - The right column holds "Chappaqua and Michigan" and "The night's calls" (a three-line explanation, then hour groups).
  - The footer has three lines, the last naming the typeface.
  - Rows are "State · U.S. Senate" over a run-on line "Moore (R) 66.6% · Wess (D) 33.4%", with the status on the right.
- **Country, phone.**
  - Order: header (wordmark, three tabs, select), banner, Pause row, three bars, a "Latest call" strip, Chappaqua and Michigan, "Where the races are" as an 11-column tile grid with a legend, then "Senate races".
  - The calls sheet exists in the page (`div.sheet[role=dialog]`).
- **State `/mi`, desktop.** "Country" as a breadcrumb; the state's name at 25.6 px with its poll closing; the district map on the left; on the right, the Senate and Governor races in bordered rounded boxes, each with a source and time line and a last-election line; then "U.S. House" as a three-column grid of bordered boxes, one per district.
- **Michigan's map.** At 8b41189 Michigan's map lacked the Upper Peninsula's shape (district 1 drawn as one polygon over the lakes). At fd9e65c, after c5a3b6f, it is right (`shots` not kept; seen 13:16).
- **Race `/mi/senate`.** A breadcrumb, the race's name, then the candidates (name 16, party 13 muted, votes 14 muted, share 17 / 600). Under them, in 13 px:
  - "83.3% reporting (civicAPI's own figure of precincts reporting; not a share of the expected vote) · civicAPI, as of 10:36 PM ET";
  - the last election;
  - "Candidates as printed on the state's official list: source.";
  - "Incumbent: Gary Peters.".

  The page ends with the three-line footer. Below the race, the page is empty.
- **Senate, desktop.** A three-column grid of bordered boxes, one per race. Each has a source line, and the called ones have a tinted winner row.
- **House, desktop.** A table (Seat, Leading, Share, Next, In) grouped by state, with the state's map in a sticky panel on the right.

## 4. Bottom-card components, weighed [measured unless marked]

| entry | gzip bytes | over Preact |
|---|---|---|
| Preact alone (`pbase`) | 5,329 | – |
| Vaul 1.1.2 via preact/compat | 31,363 | about 26 KB |
| Zag drawer 1.47.0 with `@zag-js/preact` 1.47.0 | 34,053 | about 29 KB |
| Base UI `@base-ui/react` 1.9.0 Drawer via preact/compat | 47,267 | about 42 KB |
| NumberFlow 0.6.2 (web component) | 5,212 | (alone) |
| d3-scale 4.0.2 with d3-time (`scaleTime`, `timeHour`) | 9,926 | (alone) |
| Zag drawer plus `@zag-js/radio-group` 1.47.0 | 38,046 | about 4 KB more than the drawer alone |

- **Licences** [stated: package.json and npm metadata]: Vaul MIT; Zag MIT; Base UI MIT; NumberFlow MIT; d3 ISC.
- **Vaul's README** says "This repo is unmaintained" [stated].
- **NumberFlow's site** (curl, 13:21) has a countdown example and a `respectMotionPreference` option [stated].

## 5. Zag's drawer, read in its source (`dist/*.mjs` and the types, 1.47.0) [stated]

- **Anatomy:** positioner, content, title, description, trigger, backdrop, grabber, grabberIndicator, closeTrigger, swipeArea.
- **`snapPoints`:** `number | string`; numbers are fractions, and px strings are accepted.
- **`swipeDirection`:** `"up" | "down" | "start" | "end"`. "start" serves the side menu.
- **Thresholds:** `swipeVelocityThreshold` defaults to 700 and is in px/s. `closeThreshold` defaults to 0.25. `snapToSequentialPoints` and `preventDragOnScroll` (default true) also exist.
- **`modal`** defaults to true, and the machine derives `trapFocus` and `preventScroll` from it when the drawer opens (`drawer.machine.mjs`, lines 39–44). So a drawer that is modal only at full height needs `modal: false` plus our own inert background.
- **Data attributes:**
  - `data-expanded` is set when the active snap point's offset is 0 (full height);
  - `data-swiping` and `data-dragging` are set during gestures;
  - `transitionDuration: "0s"` is set inline while dragging.
- **CSS variables:** `--drawer-translate(-x/-y)`, `--drawer-snap-point-offset-*`, `--drawer-swipe-movement-*`, `--drawer-swipe-strength`, `--drawer-swipe-progress`, `--nested-drawers`, `--drawer-height`, `--drawer-frontmost-height`.
- **Reduced motion:** there is no reduced-motion code; no match for "reduce" or "prefers" in `dist` [measured: grep]. The open and close motion is the author's CSS transition on the translate, so reduced motion is ours to write.
- **Focus:** `initialFocusEl`, `finalFocusEl`, `restoreFocus` (default true), `closeOnEscape`, `closeOnInteractOutside`.
- **Open state:** `open` and `onOpenChange` allow a controlled state bound to the router.
- **Agreement.** These were sent to W8 at 13:16 UTC. W8 wrote them into MOTION-SPEC v1.6 surfaces 10 P and 13 P (commit af62c4c).

## 6. Countdowns and timelines: published and prebuilt

- **NumberFlow** (MIT): a countdown example with per-digit rolling and a `trend` option, so a countdown's digits roll one step [stated: its site]. It was set aside because W8's motion (13:21, agreed 13:27) replaces the whole number each second with no roll. That leaves nothing for it to do, and it costs 5.2 KB.
- **d3-scale and d3-time** (ISC): a time scale with hour ticks, 9.9 KB. Set aside because the timeline's scale is fixed for the night, so `x = (t − 6 PM) / 7 h × width` is all it needs.
- **Published poll-closing pages, read 13:40 UTC with curl and an honest User-Agent:**
  - **270toWin, `/poll-closing-times`** (HTTP 200) [stated: page text and markup]:
    - It shows the hours as plain striped tables (`table text-center table-striped`, five of them), with no countdown and no timeline on that page. Its menu links to a separate "Countdown Clocks" page, which was not read.
    - It gives a note, in Eastern Standard Time, of the states whose closing varies by congressional district: Indiana (1 and 8 at 7 PM, the rest 6 PM); Kentucky (1 and 2 at 7 PM, the rest 6 PM); Florida (1 and 2 at 8 PM, the rest 7 PM); **Kansas (district 1 at 9 PM, the rest 8 PM)**; Michigan (1 at 9 PM, the rest 8 PM); Texas (16 and 23 at 9 PM, the rest 8 PM); Idaho (2 at 10 PM, 1 at 11 PM).
    - Against `races.json` (W4, from state authorities), all agree except Kansas. `races.json` gives Kansas one hour, 01:00Z (8 PM ET), with no later part. 270toWin is not a true source for this (it is a publisher repeating it), so this is a question for W4 to settle at Kansas's own authority, not a correction. Sent to the orchestrator.
    - What the page shows by contrast: a plain list of hours is what the maker called not special (13:17). The district-level note is the useful part, and the site already carries it as "part of".
  - **The New York Times' 2024 poll-closing page:** HTTP 403 with a captcha. Recorded as unread and not retried.
  - **Ballotpedia, `Poll_closing_times`:** HTTP 202 with an empty body (a bot check). Recorded as unread.
  - **Decision Desk HQ's home page** (HTTP 200): no countdown or closing timeline in its markup [measured: grep]. Its results pages were not read.
- Nothing in the specification rests on these pages.

## 7. W9's outline fix, checked (fd9e65c, 13:16 UTC) [measured]

- **Hover.** TX, MA, HI, VA and NJ were hovered at desktop 1280 × 900. Each gave exactly one `svg.map path.outline`, stroke 1.5 px, `rgb(22, 24, 27)`, `vector-effect: non-scaling-stroke`, `stroke-linejoin: miter`. MI hovered at its bounding box's centre lands in Lake Michigan and gives no outline, which is correct.
- **Keyboard.** Texas was focused by Tab. The link's computed `outline` is solid 2 px (the global `:focus-visible` rule, `styles.css` line 64), and the state's own path stroke is 2 px (line 306). Together with the single outline, the result is three marks, the rectangle outermost. Shot: `shots/c2-check-w9-outline-keyboard-focus-TX.png`.
- **Pointer over Oklahoma while Texas has focus.** ~~Still one outline, on Texas.~~ **Withdrawn, 13:58 UTC:** the test placed the pointer at 30% / 30% of Oklahoma's bounding box, which lies in the Texas panhandle. It was W5's error, not the page's.
- **Recheck at `38ce7b5` (W9's f9809d6), 13:58 UTC:**
  - Tab to Texas: one outline, 1.5 px, `stroke-linejoin: round`; the link's `outline` is `none`; the path's stroke is 0.75 px.
  - Pointer moved in steps to 60–70% across and 40–45% down Oklahoma's box: the outline moves to Oklahoma, still exactly one.
- **The band, with `?fixtures=tick` at `38ce7b5`:**
  - On load: no band, which is right (MOTION-SPEC 11).
  - 8 s in: four rows' `.r-line.banded` with `--b: 1`, background #faf2d8.
  - 40 s in: strengths 1, 0.94 and 0.81, stepped.
  - `document.getAnimations()` is 0 throughout, so the band is set, not animated. **Passes.**
  - It lies on the run-on line today. It moves to the figures column with s.7's rows.
- **Coasts.** Along the Texas Gulf coast and the Chesapeake, the 1.5 px stroke reads heavier than on straight borders (`shots/c2-check-w9-outline-hover-VA.png`) [measured: shot; the cause, vertex density of the 500k shoreline at this scale, inferred].

## 8. The Northwestern Hawaiian Islands [measured]

- **Hawaii's district file** (`data/static/boundaries/congressional-districts/HI.topojson`, from `cb_2025_us_cd119_500k`): 2 features, 9 polygons, centroids from 160.16° W (Niihau, 185 km²) to 155.52° W (Hawaii, 10,480 km²). None lies west of 161° W.
- **The country file for desktop** (`states-country-desktop-3pct.topojson`, from `cb_2025_us_state_500k`): Hawaii has 9 polygons. One lies west of 161° W, at 171.74° W, 25.77° N: Laysan, 3.96 km², 2.2 × 2.9 km.
- **The phone file** (`-phone-1pct`): 8 polygons, none west of 161° W.
- **Scale.** d3's `geoAlbersUsa` at the site's scale (1300, view box 975 × 610) gives 0.206 units per km near Oahu. On a desktop map about 790 px wide that is 0.167 px per km, so Laysan is about 0.37 × 0.48 px.
- **The credit line.** `Maps.jsx` line 87's credit, "Hawaii's Northwestern Hawaiian Islands are not drawn on this map; they are on Hawaii's", is contradicted by the district file above.

## 9. Status

- **13:16.** Zag's drawer was recommended to W8, item by item.
- **13:27.** The countdown and timeline motion were agreed with W8.
- **13:45.** `DESIGN-SPEC.md` v1 and this file were written, with:
  - the specimen `specimens/c2-country-top.html`;
  - the logo `specimens/c2-logo-b-flag-tile.svg`;
  - the shots `shots/c2-*`.
- **13:40.** v1.1 added DESIGN-SPEC s.8 (the state, race, chamber and House views) and the remaining rows of s.11.
- **Still open:**
  - specimens of the side menu and the state card, if the orchestrator wants them drawn before W9 builds;
  - the published countdowns and timelines, if wanted.

## 10. Check of the deployed preview at 7dcf244 (14:30 UTC) [measured: shots `shots/c2-check-7dcf244-*`]

Checked on `midterms-git-build-site-…vercel.app/?fixtures`, open without login since 14:25 UTC, at 1280 and 390.

**Passes:**
- s.2 header: countdown, chips, "Checked", Pause on desktop.
- s.3 logo B.
- s.4 menu: overlay, filter, the room's races, sections with the current one ruled, states, Pause in the phone menu.
- s.5 seat bars: figures at the ends, pill, post with "51 for control", "to call", "paler: not up this year".
- s.6 timeline: ticks hollow, filled and next, state counts, now line, the "after" column, party bins.

**Differences, sent to W9:**
1. s.4: the room's races are one run-on line ("Chappaqua Governor · Attorney General · …"), the form R3 and s.0 name as the fault. Use one per line, with "Chappaqua" as a small label above them.
2. s.4: "Commonwealth of the Northern Mariana Islands" takes three lines; use "Northern Mariana Islands".
3. s.5 on the phone: the Governors bar keeps the empty label row for a post it does not have, which leaves a hole of about 26 px. Alignment matters only side by side, so drop the reserve on the phone.
4. s.6 on the phone: the latest call is still a separate strip ("Latest call … All calls"), not the timeline's caption line.
5. s.6 desktop: the "after" label touches "1 AM".
6. s.2 on the phone: the countdown (`span.cd`) is not pressable; the night card is not built yet.

**Not yet landed:** s.9 cards (a tile press still navigates to the `/mi` page) and s.7 and s.8 rows, plus the 13:38 items (R6, R8, s.8.2, the empty preview block).

**Not the site's:** a round black button at the right edge, over the content on both screens. It is the Vercel Toolbar, which Vercel adds to preview deployments [inferred from its form; the production domain will not carry it]. The maker sees it on the preview. Sent to the orchestrator, since turning it off is a project setting.

## 11. Continuation 3 (14:52 brief): the plan, search, the logo

- **14:50 UTC.** `SIMILAR-CHANGES-PLAN.md` written for the maker. Its measurements:
  - **Search index** [measured: built from `races.json` in Python, gzip -9]: 9,965 entries (3,148 races, 6,255 candidate entries, 562 incumbents) as plain JSON 814 KB raw, **125 KB gzip**; a compact array form 97 KB gzip; federal and governor entries only (2,450) 28 KB gzip. `races.json` itself is 7.8 MB raw, 372 KB gzip, so the index must be a separate file.
  - **Counts** [measured]: 55 states and territories; types: 2,176 state-legislature seats, 435 House, 220 statewide-other, 146 ballot measures, 88 legislature chambers, 39 governors, 33 Senate + 2 special, 5 delegates, 4 local; 340 distinct office names; 6,212 distinct candidate names.
  - **Census relationship files** [measured: directory listings fetched with curl, HTTP 200]: `rel2020/cd-sld/` holds `tab20_cd11820_place20_natl.txt` (place to 118th-Congress district) and per-state files; `rel2020/zcta520/` holds ZCTA to county, county subdivision, place, tract and block, but no ZCTA-to-district file; `TIGER2025/ZCTA520/tl_2025_us_zcta520.zip` exists. So ZIP to district needs a build-time match of ZCTA shapes against W7's districts.
- **Logo sources** [stated: each read at the source with curl]:
  - Wikimedia Commons `Flag_of_the_United_States.svg` (upload.wikimedia.org, 823 bytes): viewBox 7410 × 3900, red #b31942, blue #0a3161, star path `#s` reused by `<use>`. Its file page (`?action=raw`) carries `{{PD-USGov}}` and `{{PD-flag}}`. Fetched once each, HTTP 200, no refusal.
  - lipis/flag-icons `flags/1x1/us.svg` (650 bytes), LICENSE: MIT, Copyright (c) 2013 Panayiotis Lipiridis.
  - Phosphor `assets/fill/star-fill.svg`, LICENSE: MIT, Copyright (c) 2023 Phosphor Icons.
  - Also read, not used: Lucide `star.svg` (ISC; its LICENSE says the Feather-derived icons are MIT), Heroicons `star` (MIT), Tabler `star` filled (MIT).
  - Direction A crops the Wikimedia flag by viewBox (2590 1300 960 960) and clips with a rounded rectangle; the geometry and colours are untouched. B wraps flag-icons unchanged. C recolours Phosphor's path to the flag's red, nothing else.
- **Model.** This thread switched to Fable 5.1 at 14:47 UTC on the orchestrator's decision (`research/ops/2026-11-02-model-choice.md`); s.11 onwards is written on it.

## 12. Continuation 4 (15:16 brief, on the maker's 14:54 ruling): pinned races, the race in its state, where cards fit

- **15:05 UTC.** DESIGN-SPEC v1.3, s.13, with specimen `specimens/c4/index.html` (`?view=country|state|card`, `&empty=1`) and shots `shots/c4-*` at 1280 and 390 [measured: Playwright, Chromium, the specimen served locally; figures invented and marked so on the page].
- **County shapes** [stated: copied from W7's `data/static/boundaries/counties/NY.topojson` on `build/site`, object `co-NY-src`, 62 geometries, property `NAME`]. The specimen decodes the topology inline and draws a plain equirectangular projection; the site uses W9's d3-geo path, not this.
- **Icons** [stated: Phosphor `push-pin-fill`, `push-pin`, `dots-six-vertical`, MIT; LICENSE copied beside them].
- **The decision in 13.2** (a race opens within its state view on desktop, the card on the phone) is a design candidate for the orchestrator to adopt; the alternative (a filled standalone race page) and the reasons against it are in the section. Nothing in s.13 is decided by W5.
- **Specimen fixes before the shots** [measured on the first shots]: the grip and pin overlapped the status word (moved into the card's top row; hidden until hover or focus on desktop, always shown on the phone); the Pin button's icon was unsized on the phone sheet (12 px); the heading and status crowded on the phone (status wraps to its own line); the "By county" head lost its grid because the sheet's `.head` rule matched it (class renamed `thead`).
- **15:47 UTC.** s.13 adopted by the orchestrator as written, candidate (a) included; W9 builds it after the cards. v1.3.1 (15:50) adds the one exception to R4 the orchestrator asked for: the race-in-focus county map's fills show who is leading, allowed because the legend says "Leading" in words.
- **15:52 UTC, header fault recorded for the recheck** [measured: deployed preview, bundle `index-G1Bge0OB.js`, header innerText]: "First polls close Tue 4 AM ET · Checked 10:08:24 AM · Pause". The first closing on the night is 6 PM ET Tuesday (s.2; `races.json`), so "Tue 4 AM ET" is wrong, ~~and "Checked" carries seconds where s.12.3 gives "as of 9:04 PM"~~ (withdrawn 15:58: the seconds are the orchestrator's 13:36 condition and s.12.3 line 403 already says so; "as of 9:04 PM" is a row's stale time, a different place. My note misread my own spec.) The "4 AM ET" fault is W9's; to be checked again when the fix lands.

## 13. Check of W9's phone cards and header correction at fe3f914 (16:05–16:20 UTC) [measured: deployed preview, Playwright, 390 × 844 at 2× and 1280; shots `shots/c5-check-fe3f914-*`]

**Passes against s.9 and MOTION-SPEC 10 P / 13 P:** the state card's medium stop is 55% (top at 379 px of 844); at that stop the scrim is at opacity 0 with `pointer-events: none` and `elementFromPoint` on the country hits the seat bar, so the country stays usable; the head (`.cardhead`) is sticky and holds the grip, "‹ Back" (15 px) and "New York" with "Polls close 9 PM ET", with no ×; the card scrolls (2,644 px of content in 814); a race pressed in the card stacks a race card over it and the state card stays beneath; Back goes race → state → country; the address `/ny` on the phone renders the country with the card open at the medium stop; under `prefers-reduced-motion: reduce` the transition is 0 s; the content's transition is 0.5 s. The header before any closing now reads "First polls close Tue 4 AM ET in the Northern Mariana Islands" at both widths (true to `races.json`; s.2 corrected in v1.3.2).

**Differences, sent to W9 16:22:**
1. At the medium stop the first screen is the district map, then Governor; s.9 (2) puts the statewide races first and the map at full height (3).
2. The race blocks are boxes (`article.card`, 1 px border, rounded; four measured in the card) where R5 and s.9 (2) say blocks parted by 24 px and a hairline. Only the pinned cards (s.13.1) box a race.
3. Type off R2's scale: the card's h1 25.6 px (24); section heads "U.S. House", "Other statewide offices" 16.8 px (19 or 15); "Governor" 16 px (15); the race card's shares 17 px (s.9: 19 / 600); votes 14 px (12); status 13 px (12).
4. The race card's status reads "48% reporting (civicAPI's own figure of precincts reporting; not a share of the expected vote) · civicAPI, as of 10:37 PM ET": the parenthesis is read by nobody in the room (R1); "48% of precincts in" says it in words, and the definition belongs once in the source line's title or the methods page.
5. The race card's source is split over three lines ("· source" as plain text, not a link; "Names: official list." on its own line); R7 asks for one source line per section, with the links in it.
6. The race card at full height is about 45% blank under the map: the fault the maker named for the desktop, on the phone. v1.3.2 amends s.9: the race card opens at the medium stop and rises only when its content asks.
7. After Back from the race card the address is `//ny?fixtures=…` (a doubled slash; the router joins base and path).
8. At full height `main` carries no `inert`: the scrim takes the pointer, but keyboard focus and a screen reader still reach the country beneath (s.9: "our own inert background at full height").
9. On the phone the header's pre-closing line wraps to two lines in the 48 px row; v1.3.2 gives the phone the short form without the place.
10. Party as a word ("Dem", "Rep") in the card's race blocks and as a letter ("(R)") in the House table on the same card: one form per card (R8's spirit).
11. Governor tickets as "Kathy C. Hochul / Adrienne E. Adams" wrap every row; the surname or the governor's name with the running mate in the 12 px line would hold the row to one line (a data form for W4/W9).

- **15:39 UTC (orchestrator).** v1.3.2 adopted: the race card at the medium stop is the 14:54 ruling applied, not a new decision; the phone header without the place is fine. W9 takes differences 1–3 first (figures before the map, blocks out of boxes, type to R2), the rest as reached. W9 told 16:25.

## 14. Check of W9's 12be0ae: the Pinned shelf, the race within its state, the three card corrections (16:45–17:00 UTC) [measured: deployed preview, bundle `index-CEQwxTH1.js`, Playwright at 1280 and 390 × 844 at 2×; shots `shots/c6-check-12be0ae-*`]

**Passes.** "Chappaqua and Michigan" is gone from the page and the menu; the **Pinned** shelf sits under the night (top 481 px at 1280), four cards across (284 px each), each a 1 px `--line` box with 8 px corners and no shadow, a called race with the 3 px rule and "Called" in the party colour; grip and pin buttons carry their names ("Move this race…", "Unpin Governor"); the menu lists "Pinned" in the pinned order before Country; `localStorage["midterms.pins"]` absent means the defaults; the empty line and "Show all N" are the spec's words (read in `Pinned.jsx`). **The race within its state:** `/ny/attorney-general` renders New York (h1 24 px) with Attorney General in focus (h2 19 px, "Pinned" button), the map in a sticky column (`.focus-map`, `position: sticky; top: 72px`, held at y = 72 after a 700 px scroll) with the line "The state's U.S. House districts." under it, and the other races as rows under "New York's other races"; the page's leaves are on R2's scale but for three (14, 14, 13 px). **The phone's state card** shows Governor before the map at the medium stop, with no boxes; its h1 is 22 px (the phone's override). **The race card** opens at the medium stop (top 380 px), head "‹ New York", "Pinned" button.

**Differences, sent to W9 17:02:**
1. The pinned card's lines are in the wrong order and the candidates are cut: the status ("6% reporting") is the first line and the place and office the second; the two candidates share one line and are truncated ("Komatireddy (R) 50.2% · Jam…", "Hernand…"), so the second name and share are lost. s.13.1: the place and office first with the status on the right of that line; the candidates stacked with the shares on one right edge (R3).
2. The card's office is 16 px (R2: 15).
3. The grip and pin are always shown on the desktop (s.13.1: on hover or focus; always on the phone). Twenty icons on ten quiet cards.
4. Defaults are ten; the orchestrator (15:57) ruled six, law 10's. W9 told.
5. The focus block has no "Last election … · Incumbent …" line (s.13.2). If `races.json` holds the 2022 result and the incumbent for the statewide races, show them; if not, it is W4's.
6. The phone card's House table is 14 px and 13 px throughout (about 130 cells; R2: 15 or 12).
7. In the phone card's DOM the map still precedes the Governor block (CSS order puts it after), so a screen reader meets the map first; s.9's order is the content's order.
8. The phone's Pinned list has no "Reorder" toggle (s.13.1); the grips are shown, which is the phone's rule, so this waits for W11's sortable.
Items 4 and 5 of s.13 (the status parenthesis; the source over three lines) remain, as W9 said.

- **17:25 UTC.** W9 (93b7040 pushed) reports the desktop map zoom at 50–56 ms a frame against rule 12's 50, traced to the layout space the Pinned shelf adds above the map [stated by W9]. W9 offers one row of pinned cards or the shelf below the map on the desktop and holds for the orchestrator. My reading, sent to both 17:25: (1) the cause first (`contain: layout paint` on the shelf, the zoom as a transform on the map's layer), because the maker may pin twelve races and the cost would return with every pin; (2) only if it stays, the shelf below the map on the desktop rather than one row, because one row hides two of law 10's six behind "Show all" (law 10: fewest steps). The phone keeps its order. The composition is the orchestrator's; v1.3.3 to follow the ruling.

- **16:29 UTC (orchestrator, superseding a 16:26 note that handed me the composition with a lean to one row).** Decided as my reading: (1) W9 tries the cause once more, the zoom as a transform on a map layer isolated from the shelf (`contain: layout paint` alone changed nothing, W9 says; the map promoted on its own layer is the new part), measured; (2) if the cost stays over 50 ms, the shelf goes below the map on the desktop, the phone keeps its order. v1.3.3 to s.13.1 once W9's measure says which branch.

## 15. Judgement of details.so Vault menu-01 "Liquid Popover" as a candidate for "F, the desktop race panel" (17:50 UTC; the orchestrator's ask of 16:34, W11's note of 17:45)

Read [stated: `/mnt/project-files/vault/details-so/menu-01/` — `SOURCE.md`, `index.html`, the head of `style.css` and `implementation.md`, the structure of `script.js`; nothing of it copied here, per its licence]: a popover whose surface is an SVG blob traced each frame from the trigger, the panel clipped to the same outline; `role="menu"` with `role="menuitem"` buttons of 42 px, `min-width 188px; max-width min(280px, 100vw − 40px)`, a filled surface (`--menu-bg`, a warm grey) with a 1 px stroke; settles in about 720–800 ms [W11, measured]; its implementation prompt forbids replacing the algorithm, the menu roles or the clipped panel ("non-negotiable"). W11's measures accepted as stated: desktop start 1–10 ms, gaps 20–24; phone gaps 46–97, not its surface.

**Judgement.**
1. **F itself is superseded.** W11's F ("a race panel on the desktop", a popover beside the row, the platform `popover` recommended) was written before s.13 was adopted (15:47). s.13.2 answers the 14:54 ruling with the race opening **in place** within its state view, and s.13.3 says why not a popover: a race in focus is read deeply, so it is a section; a floating panel would hide the state that gives the race its context and be a third way of opening things (P7). So there is no F to fill on the desktop, with the platform popover or with anything else. W9 has built s.13.2 (12be0ae; checked in s.14).
2. **menu-01 is an action menu, not a panel for figures.** Its ARIA is menu and menuitem, its width is capped at 280 px, its rows are 42 px buttons; a race's content (two to four candidates with votes and shares on one right edge, the status, the last election, a county table) does not fit its contract, and the contract may not be reduced. Its surface is a filled, stroked blob: a box (R5), with a morph that runs most of a second for a thing that should be read at once (law 5's "nothing moves that need not"; MOTION-SPEC never list does not name it, but the spec's rule for text is that it never travels).
3. **What W9 takes of it: nothing now.** Where it would fit is a per-item **action menu** with more than two actions, and the site has none: a pinned card's two actions are two glyphs (grip, pin), a row's one action is the pin, and law 10's fewest steps counts against a menu that hides them. If such a surface ever arises on the desktop (three or more actions on one thing), menu-01 is the crafted candidate and the platform popover the plain one; the phone is not its surface.
4. Whether the maker wants to see it is the orchestrator's call; shown, it should be shown as what it is (an action menu), not as a race panel.

- **17:45 UTC (W9's zoom measure, four cases, four runs each, 1366 × 900, gap between painted frames):** shelf as built 52–66 ms; shelf hidden 23–39; hidden with an empty 361 px spacer above the map 51–67; the same spacer below the map 23–30; containment of the shelf and the map on its own layer 51–64. So the cost is the layout space above the map, whatever fills it; my point 1 (cure the cause) does not reach it, and the orchestrator's branch (2) applies. **v1.3.3 (18:05):** the desktop's Pinned shelf goes directly below "Where the races are", above the Senate list; the phone keeps its order. W9 builds it in one commit and measures for W8.
- **W9's two unruled choices on the phone card (752c25d, f08d016), read 18:05:** (1) the House table's reporting column headed "Precincts in" with the bare figure in the cells, because "37% of precincts in" on every row wrapped the leader and said five words 29 times (R1, R8: the word once, in the head) — right; the desktop House table's head is "In", so the two should share one head ("Precincts in" on both; the desktop has the room). (2) "Incumbent: X" on a full card only where no row carries the mark (R6, said once) — right.

## 16. Check of W9's 93b7040, 752c25d and f08d016 on the deployed preview (18:15 UTC; bundle `index-BcqgfGdM.js`; shots `shots/c7-check-f08d016-*`) [measured: Playwright, 1280 and 390 × 844 at 2×]

**Passes:** six default pins (Governor, Attorney General, House 17, State Senate 40, County Legislator, Michigan Senate); the pinned card's place and office first (15 px) with the status on the right of that line (12 px) and the two candidates stacked, shares on the card's right edge (x = 619 for the status and both shares, R3); "7% of precincts in" everywhere; party letters "(R)" in the focus block, the race card and the phone card's blocks; tickets as the name with the running mate on a 12 px line under it; the phone card's type 15/12 (22 and 19 for the heads) with no 14 or 13 left; the phone card's House table headed "Seat · Leading · Share · Precincts in" with the bare figure in the cells; Governor before the map in the DOM; at the card's full stop the header, banner and `main` carry `inert`; the race card's source as one line "civicAPI, as of 10:36 PM ET" with "Incumbent: Kathy Hochul" under it; Back from the race card leaves `/ny?…` (the doubled slash is gone). The desktop state view's House seats are rows, not a table, so there is no second table head to match: my 18:05 note on "In" against "Precincts in" was mistaken and is withdrawn.

**Remaining, small:**
1. The card's office is the full name ("NY State Senate, District 40", "Westchester County Legislator, District 4"), which wraps to three and four lines in a 284 px card beside the status. The menu's short forms ("State Senate 40", "County Legislator", "House 17") hold one line; s.13.1's example was "N.Y. · Attorney General". And the place reads "NY" where the rows and the latest-call strip read "N.Y." (one form, R8's spirit).
2. The grip and pin were not visible on the desktop cards in the shot, hovered or not (their computed visibility was `visible`, opacity 0.75 and 1, before and after a hover), so either they sit where the shot does not show them or they are hidden another way; s.13.1: shown on hover or focus on the desktop, always on the phone.
3. "Names: official list." stays a line of its own under a rule (desktop) or at the foot (phone); R7 would fold it into the source line ("civicAPI, as of 10:39 PM ET · names: official list").
4. Still open from before: "Last election …" in the focus block (W4's data), the phone "Reorder" toggle (W11's sortable).

- **17:13 UTC (orchestrator), on the night card's closings list opening with 4 AM and 5 AM ET (raised through W8):** the two stay first in time order, and name the day on those two entries alone ("Tue 4 AM ET · Northern Mariana Islands", "Tue 5 AM ET · Guam"). Written as v1.3.4 in s.2 (phone row); W9 told 18:25.

## 17. Check of W9's f33323b, a1f0d98 and 13480d7 (the shelf below the map, the cards' four items, the night card) on the deployed preview (18:45 UTC; bundle `index-BEqxz222.js`; shots `shots/c8-check-13480d7-*`) [measured: Playwright, 1280 and 390 × 844 at 2×]

**Passes:** on the desktop the Pinned shelf now follows "Where the races are" and precedes "Senate races" (v1.3.3); on the phone it stays between the night's calls and the tiles; the cards' titles are the short forms with the AP place ("N.Y. · State Senate 40", "N.Y. · Westchester County Legislator 4", "Mich. · U.S. Senate"), one line but for the county legislator; the grip and pin appear on hover and are hidden otherwise (my 18:18 doubt withdrawn: the hover shot shows them, the plain shot does not); the focus block's source line reads "civicAPI, as of 10:39 PM ET · names: official list" with "Incumbent" under it (R7); the phone's countdown raises the night card at the medium stop with "‹ Back", "The night", the timeline and "When polls close" as a list in time order from 4 AM ET.

**Differences:**
1. At 1280 the shelf below the map sits in the map's column (two cards across, 385 px each, x 48–835; the right column under the night's calls is empty), so six cards take three rows. s.13.1: a full-width section, four across at 1280. The space it now occupies is below the map, so the zoom is unaffected either way.
2. The closings list does not yet name the day on the first two entries: v1.3.4 (18:25) wants "Tue 4 AM ET · Northern Mariana Islands", "Tue 5 AM ET · Guam"; today it reads "4 AM ET · the Northern Mariana Islands". 13480d7 may predate the text.
3. "The night" heading showed a focus rectangle on opening (the card gives it focus on open, as the state card does). The press was a scripted click, which Chromium can treat as keyboard focus; if a real tap also shows it, the programmatic focus on a `tabindex="-1"` heading wants `outline: none` (the ring is for keyboard users, who get it from `:focus-visible` on the Back button).
4. The phone's countdown is a `span.cd` with no role: it opens the card on a press but is not a button to the keyboard or a screen reader (s.2: pressing the countdown raises the night card). A `<button>` with the same look.
- **18:50 UTC (W9, 838b77c and 006aed9):** the shelf is its own full-width row below the map, four across at 1280; **the zoom's gap with the shelf there: 24 / 29 / 28 ms** against rule 12's 50 (52–66 with the shelf above; the four cases of 17:45) [stated by W9, three runs]. The closings list names the day on the first two rows (v1.3.4). The heading's ring is gone. My item 4 of s.17 was wrong: the countdown is a `<button aria-haspopup="dialog">` carrying the sentence for a screen reader, and the `span.cd` I inspected is its aria-hidden text; withdrawn. A state is now served in two files (New York's first screen 1.0 KB, was 200 KB); the card's overshoot past its stop is fixed (rests at 380 px, 0 past).
- **v1.3.5 (19:00), on W9's question:** with four cards across, a title sharing its line with the status wrapped to two and four lines. Decided in s.13.1: the title takes the full width and the status becomes the card's last line, 12 px on the shares' right edge (R3), as the race block orders it (s.8.2); four across stays. W9 told.

## 18. Check of W9's 1313be0 and 6485e17 (the card to v1.3.5, the race's framed map) on the deployed preview (19:35 UTC; bundle `index-BtR9dWv7.js`; shots `shots/c9-check-6485e17-*`) [measured: Playwright, 1280 and 390 × 844 at 2×]

**Passes:** the pinned card is v1.3.5 at both widths: the title across the card ("N.Y. · Westchester County Legislator 4", two lines at 284 px, one on the phone), the candidates stacked with the shares on the right edge, the status as the last line on the same edge ("8% of precincts in", "No results yet"); the shelf is four across at 1280 below the map; `/ny/house-17` frames the district from its own boundary file (the district outlined at 1.5 px, the neighbours numbered, the Sound's shore true) with the focus block above the other races; "This district in 2024: …" and "Incumbent: Mike Lawler" under the block.

**Remaining, small:** "· source" at the end of the 2024 line is plain text, not a link (R7); "No results yet." in the focus block carries a full stop where the card and the rows have none (R8: one form). Open as before: "Last election …" for statewide races (W4's data) and the phone's "Reorder" toggle (W11's sortable).

## 19. s.14, the desks' calls (19:35 UTC; the orchestrator's ask of 19:12 on the maker's 18:52 words)

Written from W3 s.6 (read whole: 6a Bluesky's words, 6b the 2025 night's posts per desk with times, 6c the limits, 6d the shape proposed to W10) and W10's `docs/api.md` (`call`: `firstSeenAt` is the site's first sight, not the desk's time; `sourceCalledAt` read but not shown). The choices and their reasons are in the section: the desks appear as a "Calls" list on the race and as one muted line under each entry of the night's calls; rows, cards and the timeline carry the site's call only (R1, R4, R8, P7); civicAPI's time is a bracket in words or "by h:mm" where one instant must do (law 7); the three truths once per section in the source line (R7). Open for W10: a field for the bracket's earlier bound. No specimen yet; one follows if the orchestrator wants it before W9 builds.

## 20. Check of W9's 642795a, s.14 the desks' calls, on the deployed preview (20:35 UTC; bundle `index-CHQL9jEE.js`; shots `shots/c10-check-642795a-*`) [measured: Playwright at 1280 and 390 × 844 at 2×, W9's hooks: `__fixtures.deskCall`, `.call`, `.deskGone`, `__midtermsPoll` on `MI|U.S. Senate|Class 2`]

**Passes:** the "Calls" list on the race in focus and on the phone's race card, in time order: "NBC News · 8:27 PM ↗ · Smith", "CBS News · 8:43 PM ↗ · Smith post removed" struck through with the note in warn, "The Times · 8:54 PM ↗ · Smith, reports", "civicAPI · between 8:58 and 9:00 PM · El-Sayed"; columns 92 / 164 / rest px; each time a link to the post; the call line reads "between 8:58 and 9:00 PM"; the three truths in the race's source line and in the night's calls' source line, once each; the night's calls entries read "by 10:28 PM". W9's four departures from the specimen's letter (class name, 164 px, surname in the row, the list only once a desk has posted) are right and v1.4.2 has the last.

**Differences:**
1. Placement (W9's own question): the list sits after the source line and before "Last election"; v1.4.2: candidates, status, Calls, last election and incumbent, source line. W9 told 20:20.
2. The call line is 12 px muted ("Called for Abdul El-Sayed (D) by civicAPI decision desk between 8:58 and 9:00 PM"); s.8.2 gives it 15 px / 600 in the party colour. It is the one line that says the race is over.
3. The called winner's row carries a light party-colour background fill across the row (with the check and the 3 px rule); R4 gives the party colour to the name, check, share and rule only, and R5 no fills. Seen on both widths.
4. Not verified: the desks' line under the night's calls entry. The seeded call sits past "25 more calls" at the fixture's clock, and my press on that control did not reveal it; W9 to confirm by a shot, or give the hook a `minutesAgo` so a seeded call lands at the top.

- **20:50 UTC, surface 18 against R4/R5.** W9 (20:03) found the called winner's row fill is MOTION-SPEC surface 18's standing state (the tint sweeps in with `call` and stands), which cites my earlier s.14.4; DESIGN-SPEC R4/R5 (13:30) give the colour to the name, check, share and rule only, no fills. Two readings of mine; put to W8 with a proposal: the sweep stays as the moment's mark, then the tint goes (`uncall` ease, 450 ms, or a cut), leaving R4's standing state, because by midnight most rows are called and a standing tint on each means nothing and boxes the row. W8 measures and writes; W9 builds what W8 writes. W9's 1, 2 and 4 of s.20 are in the next push.

- **20:05 UTC (orchestrator):** surface 18's standing tint yields to R4/R5; the rule is drawn in the party colour with `call`, the name, check and share take the colour as it draws; W8 writes v1.8.8. R4 gains the line (v1.4.3). I told W8 the rule is vertical at the row's left edge, so the draw is top to bottom.

- **Clock correction (date -u 20:05).** W8 (20:05) notes my timestamps of the last hour run ahead of UTC: I wrote them by estimate. The times written as 19:35 to 21:00 in s.19, s.20 and the v1.4 to v1.4.3 headers are about 50 minutes ahead of the true UTC; the order of events is right. From here the times are read from `date -u`.

## 21. Check of W9's fc88c0a, surface 18 as v1.8.8 (the called row's rule drawn down, nothing filled), on the deployed preview (20:23 UTC by `date -u`; bundle `index-BdmhOQ3s.js`; shots `shots/c11-check-fc88c0a-*`) [measured: Playwright at 1280 and 390 × 844 at 2×, `?fixtures=script&now=2026-11-04T02:00:00Z`, `__fixtures.call(key)` then `__midtermsPoll()`, read each animation frame; the frame strips made by pausing the page's animations and seeking them to 0, 80, 160, 240, 340, 500 and 680 ms]

**Where the rule is.** Surface 18 lives in the race card's candidate rows (`.crow`, the state page's cards and the race in focus), not in the list rows of `RaceRow` (s.12.2 C2), which carry the standing 3 px rule by a background gradient and no draw (surface 11: in lists nothing but the call moves). On the phone the state page's House seats are a table (`.htable`), where a call sets the name to 600 and nothing else; so the House 9 call I sampled first showed nothing at 390, and the phone's read below is the Senate card (`MI|U.S. Senate|Class 2`), the desktop's the House 9 card.

**Passes, both widths.** From the frame the row changes: the rule (3 px, the row's 37 px, `transform-origin: top`) scales from 0 — at 1280 scaleY 0.13 at 58 ms, 0.42 at 125, 0.75 at 225, 0.90 at 325, 0.96 at 425; at 390 0.20 at 78 ms, 0.42 at 128, 0.75 at 228, 0.90 at 328, 0.99 at 528 — the spring's shape, visibly whole by about 300 ms. The name's colour goes from the ink to the party's over 300 ms (1280: rgb(22,24,27) → rgb(194,67,58) settled at 291 ms; 390: → rgb(45,98,184) settled at 328 ms); the check is present from the first frame, black for one or two frames before the colour reaches it. The row's and the card's background stay the page's rgb(251,250,248) throughout: nothing fills. Animations run: `motion:call` on the rule, `motion:call-color` on the name and share. The standing state at 390 (`c11-check-fc88c0a-called-card-390.png`): the rule, the check, the name and the share in the party colour; the call line under the candidates in 15 px / 600 in the party colour ("Called for Abdul El-Sayed (D) by civicAPI decision desk between 8:58 and 9:00 PM"), then "83.3% of precincts in", the last election, the source line. That is s.20's item 2 confirmed on the phone card, and the order of s.20's item 1 as far as a fixture without desk posts shows it (no "Calls" list is drawn, v1.4.2: the list only once a desk has posted).

**W8's question: is a 3 px rule drawn down a row's height noticed as the moment's mark in a list on the phone?** My reading from the frames at 390 (`c11-check-fc88c0a-call-frames-390.png`): on its own the rule's draw would be slight — a 3 × 37 px line at the card's left edge, most of its travel inside 250 ms. But it is not on its own: in the same frames the check appears at once at the row's left and the name turns the party's colour over 300 ms, and the three sit on the one line the eye reads first in a card, the leading candidate's. The moment is noticed by the three together, and the rule gives it its edge: the left edge of a card is where a reader scanning a list of cards runs their eye, so a mark that grows there is on the scan line. I would not add to it and I would not reach for a fill (R4, R5). What I would watch, with W8: the check's first frame is black before `call-color` reaches it; if the check is to be the party's colour from its first frame, it is the colour's keyframe start, not the design's concern. No difference against the spec at either width.

## 22. The Calls list with a seeded desk post, and the House table's called row (20:30 UTC by `date -u`; bundle `index-BdmhOQ3s.js`; shots `shots/c12-check-642795a-deskcalls-*`, `shots/c13-house-table-called-*`) [measured: Playwright at 1280 and 390 × 844 at 2×; W9's recipe of 20:27: `deskCall(k, 'NBC News', w, 12)`, `call(k)`, `deskCall(k, 'The Times', w, 0, 'reports')`, `await __midtermsPoll()` on `MI|U.S. Senate|Class 2`, then `call('MI|U.S. House|9')` for the table]

**s.20 item 1, the card's order, confirmed with a desk post at both widths.** The race in focus at 1280 and the race card at 390 read: candidates (y 210 / 466), the call line at 15 px / 600 in the party colour with "83.3% of precincts in" under it (368 / 665), the "Calls" list (422 / 739), last election and incumbent (520 / 854), the source line with the three truths (595 / 946). That is v1.4.2's order. The list: "NBC News · 8:48 PM ↗ · Abdul El-Sayed", "The Times · 9:00 PM ↗ · Abdul El-Sayed, reports", "civicAPI · between 8:58 and 9:00 PM · El-Sayed"; the times are links with the glyph, the bracket is never collapsed, and on the phone the bracket wraps to two lines inside its column, which is a wrap and not a collapse (14.2) and stands.

**Two things the seeded list showed that the spec had not said, now said (v1.4.4, s.14.1):**
1. civicAPI's line came after the Times' though its bracket's later bound (9:00) is the Times' minute: the spec said "in time order" and no more. Now: order by the instant each line can vouch for (a post's time, a bracket's later bound), and in a tie the bracket first, since its call was made by that minute and most likely before it. Here civicAPI's line would stand second.
2. The winner column read "Abdul El-Sayed", "Abdul El-Sayed, reports", "El-Sayed" down three lines (W9 prints the desks' `winner` as the data carries it, which the fixture gave in full; civicAPI's by the site's surname rule). Now: the surname on every line, as the lists print a name; "as the post names it" means which candidate, not the spelling.
Both are for W9, with the reason in the spec. Neither is a fault of the build against what was written.

**The House table's called row (W9's note of 20:27 that the table draws no rule, and his offer of a case).** The case is written: s.8.4, "A called leader gets a check mark and the party colour, and the row a 3 px rule in the party colour", and the phone's table is "the same rows in list form". Built, at 1280 on `/house` and at 390 in the state card's House table: the check and the colour on the name, no rule on the row. One difference, then: the rule, static as in the list rows (surface 11 keeps lists still; the draw of surface 18 is the card's and the race in focus's). Two small ones in the same rows: the status cell prints "Called" where the list rows print "Called by 9:08 PM" (14.2, R8: one status in the same words in the same place; the phone's cell has the width, the column is empty beside it); and the uncalled rows print "No results" where s.8.4 writes "No votes yet" (R8) and the list rows "No results yet" (s.18): one phrase for all three, the spec's being "No votes yet". None of these is new design; the check against 8.4 had not been made since the table's build.

## 23. Check of W9's 229f191, s.12's states, on the deployed preview (20:35 UTC by `date -u`; bundle `index-DOnI4OM4.js`; shots `shots/c14-check-229f191-*`) [measured: Playwright at 1280 and 390 × 844 at 2×; W9's recipe of 20:30: `/?fixtures&now=2026-11-03T22:30:00Z` (5:30 PM ET) and `now=2026-11-04T00:30:00Z` (7:30 PM); `?fixtures=script` with `__fixtures.call(k)` then `__fixtures.withdraw(k)`; `/xyz`]

**12.1 at 5:30 PM, passes at both widths.** The Senate list grouped by closing hour under heading rows at 15 / 600 ("7 PM ET · part of Alabama, New Hampshire and Florida"; "7:30 PM ET"), the rows without the status column and without figures; the six pinned cards reading "9 PM ET"; the seat bars with the not-up seats paler and no called segment but the fixture's Guam delegate (a fixture limit W9 named); the timeline's ticks hollow with their counts and no now line before 6 PM; the map in the "Not called" fill with the no-race states paler; the header's countdown to 6 PM with "VI · part of IN KY". The 6 PM group's heading stands with no row under it ("6 PM ET · part of Kentucky"): that is what 12.1 says, the part in the earlier heading and the row in the group of its last closing. **At 7:30 PM:** the thirteen rows whose states have closed stand above, alphabetical, with the status column ("No results yet"; North Carolina's fixture "Call withdrawn" in warn), and the hours still to come below under their headings; 12.1's two parts.

**Two things 12.1 had not foreseen, settled in the spec (v1.4.5):** W9's calls column carries, under the night's calls, "Still to close" and each hour with its states; 12.1 had said the hours are not listed again (R6). Read at 5:30 PM, the list is the one place on the desktop that names the states at each hour (the timeline gives counts, the header the next closing, the phone's night card the names), and it shrinks as the hours pass; it stands, and 12.1 now says so with the reason. The timeline's caption "First polls close 6 PM ET" was not built and is struck: the header's countdown says it beside it (R6). "No calls yet." could not be read on this fixture (Guam's calls carry morning times; W9's limit) and waits for the live page or a fixture `now` before 5:27 AM.

**12.4, one difference.** The list row: "Call withdrawn" in warn, the colour, check and rule gone (North Carolina on the fixture; the Michigan Senate card's rows after `withdraw`: no `won`, every rule at scaleY 0). The race card and the race in focus: after `call(k)` then `withdraw(k)` the status place shows "83.3% of precincts in" alone; 12.4's top line in warn, "Call withdrawn by civicAPI at 11:05 PM (it had called Collins (R) at 9:02).", is not drawn (`shots/c14-check-229f191-12.4-{card,focus}-1280.png`). Reason the line matters: the room that saw the call line a minute ago sees it gone and nothing in its place; the words say what happened (law 7, R8). A changed call ("Call changed", the new winner's colour) I could not seed: `__fixtures` has `call`, `withdraw`, `deskCall`, `deskGone`, `counts`, `one`, `shownUncalled`; W9 to say whether `call(k)` with another winner does it.

**12.10, passes with one note.** `/xyz` at both widths: "There is no page at /xyz." in the status line's place, the header and menu, and the page's footer line "Results and calls: civicAPI. Boundaries: U.S. Census Bureau." The footer is the page's chrome on every view, like the header; 12.10's "nothing else" meant no second sentence and no button, and the footer stands. The phone's calls button stays in its corner, as on every view.

**Not checked here:** 12.3's warn time (needs W10's `stale`; `?fixtures=tick` does not set it, W9), 12.5 and 12.6 (a blocked `/api` route; W9 says 12.6's "Retrying." is made true), 12.9.

## 24. The maker's 20:40 words into the spec (v1.5 to v1.5.2), specimen c6, and the check of W9's 8a91f13 (20:55 UTC by `date -u`)

**v1.5 (addca48, 20:50):** s.15 Appearance (System · Light · Dark in the side menu, remembered on the device, the attribute set before the first paint, the switch at once), s.16 Search (the desktop header's control and palette, the phone's menu field, grouped results in the row form), s.17 switches as real components (one indicator, no knobs; my candidate Zag's segmented control, read at zagjs.com/components/react/segmented-control 20:45: it is `@zag-js/radio-group` with an indicator part), s.18 the desktop menu's contents as the page's objects. The orchestrator adopted them as written (20:48). **v1.5.1 (b635e3d):** the maker's gallery picks of 20:45 written where each component lives: dnd-kit adopted for the shelf (13.3, s.11), the platform popover held (s.11), Silk, View Transitions and NumberFlow as his picks pending his word on their measured faults. **v1.5.2 (404f721):** on his 20:50 word ("I trust your judgment for all three") the orchestrator decided the passing one each time with the pick's look: the Zag drawer in Silk Sheet's look (s.9), surface 35 (8.5), surface 15's slide (s.11). W8's surfaces 36 (the scheme switches at once, measured: a 200 ms colour transition left the phone without a painted frame for 700 ms) and 37 (the indicator moves in 300 ms, labels at once) are cited in s.15 and s.17.

**Specimen c6** (`specimens/c6/index.html`, `?view=desktop|phone`, `&theme=dark`, `&part=palette`; shots `shots/c6-menu-{desktop,phone}-{light,dark}.png`, `-end` for the phone menu scrolled to its foot, `shots/c6-menu-phone-strip.png`, `shots/c6-palette-desktop-{light,dark}.png`) [measured: Playwright at 1280 × 900 and 390 × 844 at 2×]. What it shows: the header with s.16's "Search /" control after the chips; the menu of s.18 at 320 px: the search field, Pinned as six compact rows with the status at the right (Michigan's "Called by 9:33 PM" in the party colour, the title in ink: R4), the four views as one segmented control with the indicator under "Country", the states as tiles seven across (36 px, 6 px gaps; 51 and the five territories after a hairline; called tiles in the party colour, "no race" paler), then "Appearance" as a second segmented control, and on the phone "Pause". In the dark scheme the same, the indicator on "Dark". The palette: 560 px at 80 px from the top over the scrim, the query "mi", groups Pinned / States / Races / Candidates, the chosen row with the 3 px ink rule, a called candidate with check and colour, the key hints as a 12 px faint foot line. The desktop menu at 900 px tall holds everything without a scroll; the phone's scrolls, Appearance and Pause at its foot (the strip's second and third frames). Two faults fixed before the shots: the field's magnifier was painted under the input (a stacking order; z-index), and the pinned result's title had taken the party colour, which R4 gives the status alone. The tiles' order is by code (s.18); the preview's tiles are in the map's order, and the spec's reason for the code order in the menu is that the search above finds a state by name and a menu is scanned, not read as a map. The dark scheme's read on the preview: `shots/c6-dark-preview-country-{1280,390}.png`; no fault found against s.15's list (the party colours, the paler not-up seats, the two greys of the map, the warn banner all read).

**Check of W9's 8a91f13 on the preview** (bundle `index-oNMABBZD.js`; shots `shots/c15-check-8a91f13-*`) [measured: Playwright at 1280 and 390 × 844 at 2×; `?fixtures=script&now=2026-11-04T03:30:00Z`; `call(k,20)`, `change(k)`, `withdraw(k)` on `MI|U.S. Senate|Class 2`].
- **s.7's list rows, pass at both widths against c2's `.rw`:** the place at 600 with the status under it in 12 px muted (the two in the first column, 150 px at 1280 and 104 at 390), the two candidate lines with the leader first and the party letter in 12 px muted, "+N" in faint after the second, the shares column at the right (empty on this fixture before figures), hairlines between rows, the pin in the gutter at 1280. Row height 64 px. One word: the status reads "No results yet" where s.8.4's table now reads "No votes yet" (R8: one phrase for one state; the spec's is "No votes yet", s.22's note); the two stand side by side on the site now.
- **s.8.4's table, pass:** heads 12 px muted ("Seat · Leading · Share · Next · Precincts in"), the seat 15 / 600, "No votes yet", "Carl (R) vs Jones (D)" before results. The static rule on a called row and "Called by h:mm" were not reached on this fixture's clock (the 03:30 fixture carried no Michigan House call); W9 says built; to be read on the next shot with a call seeded.
- **12.4 on the race, pass:** after `change(k)` the card reads "civicAPI decision desk changed its call to Mike Rogers (R) between 8:58 and 9:00 PM (it had called Abdul El-Sayed (D) between 8:38 and 8:40 PM)." in the new winner's colour, the parenthesis muted, Rogers' row with the check and rule and El-Sayed's without; after `withdraw(k)` "Call withdrawn by civicAPI decision desk between 8:58 and 9:00 PM (it had called Mike Rogers (R) …)." in warn. One thing more than 12.4 asked: under the withdrawn line a second line gives the whole history ("civicAPI decision desk had called it for Abdul El-Sayed (D) (between 8:38 and 8:40 PM); changed …"). It is true and the night's column carries the same (surface 19); on the race one line was the spec's, and I would keep the one line and let the Calls column hold the history (R1). Not a fault; a composition note for W9.

## 25. Check of W9's 44b7a4b, s.15's Appearance control, on the deployed preview (21:00 UTC by `date -u`; bundle `index-D2PK6f7j.js`; shots `shots/c17-check-44b7a4b-appearance-{light,dark}-{1280,390}.png`) [measured: Playwright at 1280 and 390 × 844 at 2×, `colorScheme: light`; the menu opened by its button; the Dark item clicked; `data-theme`, `localStorage`, `getAnimations()`, the `theme-color` metas and `--bg` read; a reload read at `commit`; the System item clicked]

**Passes, both widths.** The block sits in the side menu above the states: "Appearance" at 12 px muted, then System · Light · Dark on Zag's radio group (`data-scope="radio-group"`, `role="radiogroup"`, arrow keys), in `.seg`'s frame, the chosen item on `--panel` at 600 in `--fg`, the others muted. Pressing Dark: `data-theme="dark"` on the root, `localStorage["midterms.theme"] = "dark"`, the body's background `rgb(18,19,20)` within 22 ms at 1280 and 31 at 390, `getAnimations()` empty (surface 36), both `theme-color` metas `#121314` with their `media` removed. A reload read at the commit of the document already carries `data-theme="dark"` and `--bg: #121314`: the attribute is set before the first paint. Pressing System removes the attribute and the key. The dark page behind the menu reads as s.15's list asks (`c17-check-44b7a4b-appearance-dark-1280.png`).

**Three differences, small, against c6 and s.17:**
1. The control is inline, about 160 px wide at 1280, where c6 draws it across the menu's width (288 px inside the 320): the frame's width is the row's, as the views' control in s.18 will be, so the two read as one kind of thing.
2. The items are at 12 px (`.seg`'s size for the map's switch); s.17 gives 15 px to the controls in the menu, which is the menu's text size.
3. On the phone the block sits under Pause; s.18's order has Appearance then Pause as the menu's last two. W9 takes s.18 next, so this one comes with it.

**v1.5.3 (88a48dc):** on W8's surface 36 the control itself moves nothing, no sliding indicator (the one segmented control without s.17's 300 ms), and s.15 says so with his measure as the reason; W9's build has no indicator and no transition, which is now the spec's.

## 26. Check of W9's b034a12, s.16's search, on the deployed preview (21:15 UTC by `date -u`; bundle `index-BVRGIDzA.js`; shots `shots/c18-check-b034a12-*`) [measured: Playwright at 1280 and 390 × 844 at 2×; the palette opened by `/` and by ⌘K, the query typed, the rows read; "oming" and "ny-17" typed for the matching; the menu's field at both widths]

**Passes.** The header's "Search /" control after the chips (12 px muted, the key cap on `--pend`), opening the palette; `/` and ⌘K open it, Escape closes it. The palette 558 × 593 px at (361, 81): 560 wide, 80 px down, over a 40% scrim, 1 px edge and rounded corners, **no shadow**. Before a keystroke: Pinned (the six races as rows with the status at the right) then States. "mi": twenty rows in Pinned · States · Races · Candidates with 12 px muted group labels; rows 36 px; the chosen row with the 3 px ink rule and no fill; the where and status at the right in 12 px muted. "oming" finds nothing (word-start, v1.5.4); "ny-17" finds N.Y. · House 17 (the code whole). Nothing found: "No state, race or candidate named that." at 12 px muted. The phone's and the desktop menu's field is the same search ("Search a state, race or candidate"), results in the menu's body in the same groups; no palette on the phone.

**Differences, four:**
1. **The name at 16 px**; s.16 and s.7 give the row's name 15 / 600 (`--t-body`). (If 16 is to keep iOS from zooming the field, that is the field's size, not the rows'.)
2. **Candidates match on their where:** "mi" lists Abdul El-Sayed, Lydia Christensen and the rest of Michigan's candidates, matched through "Michigan" in their where line. A candidate matches on the candidate's name alone (s.16: "candidates … by name"); Michigan's races are the Races group's to find. Reason: twenty rows are few, and a state's name should not spend them on every candidate in it.
3. **The pinned rows print the long forms** ("N.Y. · NY State Senate 40", "N.Y. · Westchester County Legislator 4"); 13.1 gives the menu's short forms ("State Senate 40", "County Legislator 4"), which c6 draws and the shelf uses.
4. **On the phone the district rows wrap mid-phrase** ("U.S. House, District / 1" against "Michigan · No votes / yet"): at 331 px the two sides fight for one line. On the phone (and in the desktop menu at 288 px) a row is two lines, as s.16's row form reads, the name on the first and the where and status on the second in 12 px muted; the one-line form with the where at the right is the 560 px palette's alone (v1.5.5 says so).

## 27. The maker's 21:20 words: real icons and real inspiration; the twelve palettes; the icon set (21:28 UTC by `date -u`; DESIGN-SPEC v1.6, R9 and s.19)

**His words, verbatim (in W5's thread, 21:20 UTC; RULINGS.md carries them with the orchestrator's reading):** "So again, this is a principle that applies across absolutely every single part of the site. In the search thing that pops up in the center of the screen, at the bottom, there are up and down arrows, the escape to close, and things like that. Those are like, they use the standard symbols that AI-generated content uses, and I do not want that. I want good icons, like maybe Hero UI icons, which I have access to, or something else. But like, avoid all that AI stuff. And like, maybe use the Mobin MCP or details.so to get inspiration for various components. So like, it could be the search, it could be even the bottom part of the search, it could be sections within the search, it could be drawers, menus, literally anything. Like, everything should have real inspiration."

What he saw: specimen c6's palette foot, `↑↓ move · ↵ open · esc close` (c6-palette-desktop-*.png as shot at v1.5), which W9 had built in b034a12 and removed in eff159a (21:25) on his words.

**The twelve palettes (Mobbin, `search_screens`, platform web, 21:21 UTC) [measured from the screens as Mobbin serves them, about 768 px wide]:**

| app | Mobbin address | foot | key caps elsewhere | row icon | chosen row |
|---|---|---|---|---|---|
| Vapi | mobbin.com/screens/593d7acd-2e16-4365-bcd6-02ce52f48f3b | "↑ ↓ to navigate · ↵ to select · ⌘0 Switch Organizations · 14 results" | ⌘0 at a row's right | yes | tint |
| Mintlify | mobbin.com/screens/7c7ad31f-9dfe-4be7-83d7-6002fe31d4d0 | "↵ Select · ↵ Open" as caps | ESC cap at the field's right | yes | tint |
| Replit | mobbin.com/screens/9bfad190-392c-4ad0-ba1b-6475cd1bd0d8 | none | ⌘⇧P and the like at rows' right | yes | tint |
| Juicebox | mobbin.com/screens/84169c57-5cd6-4495-bb71-93d37266f4c4 | "↵ to select · ↑ ↓ to navigate · Tab to jump sections · ⌘K to toggle" as caps | – | yes | **a bar at the row's left on a faint tint** |
| StackAI | mobbin.com/screens/bbcc94bb-f535-4dca-8532-56b135fce5c3 | caps: Select · Open · Open · Copy link | "Tab" at rows' right | yes | tint |
| Magnific | mobbin.com/screens/e22e26e2-f813-4f1e-beda-43c9ecf26419 | "↑↓ Navigate · ↵ Select · ESC Close · ⇧↵ Open in new tab" | ⌘K in the field; ⌘⇧S at rows' right | yes | tint |
| Navattic | mobbin.com/screens/c65971cf-c4ea-45e9-99a5-555930cb5d73 | "⌘ K to open", right-aligned | – | yes | tint |
| Gumloop | mobbin.com/screens/97f3400e-39b6-469b-b208-addb2d51e850 | none | ⌘K in the field; "Open ↵" on the hovered row only | yes | tint |
| Supabase | mobbin.com/screens/9b4725f5-e038-4fc7-98ad-64a59f74b4d7 | none | ⌥N at the Shortcuts rows' right | **Shortcuts group: none**; Queries, Actions: yes | tint |
| Base44 | mobbin.com/screens/675ecfd2-b7fc-4e8d-9078-3eeeaddda7c7 | none | ⌘K in the field | yes | tint |
| v0 | mobbin.com/screens/29db691c-e7fb-4ee3-9f4b-e16c4970b92a | none | none | yes | tint |
| Adaline | mobbin.com/screens/bc38c38f-ac41-4c92-b3e9-01c62bce816c | none | none | yes | tint |

Group labels: sentence case, 12-ish muted, at the left (Vapi, Mintlify, Replit, StackAI, Gumloop, Base44, v0, Adaline); letter-spaced small caps (Juicebox, Supabase); Magnific's and Navattic's are small sentence case too. Shadows: deep on Mintlify, StackAI, Magnific, Base44; slight on Supabase and v0 [inferred at the thumbnail's size]. The site's foot of key glyphs was in the common half of the field, which is why it read as generated: it is what every generator has seen. The half without one is as real.

**details.so (`search_inspirations`, "search command palette modal with grouped results and footer hints", 21:22 UTC):** ten results, all page footers (Buzzworthy, Mintlify's site footer, Good Is the New Cool, Ecopia, Alethia, Hut 8, Heron AI, RIPE, Yavorovskyi, Mantis); the catalogue is sections of marketing sites and has no palette. Not used for the palette. (The Vault is a different thing: W11's s.5 and the 67 items in `/mnt/project-files/vault/details-so/`.)

**The icon set [measured, curl, 21:22 to 21:24 UTC, saved under scratch `web/`]:**
- `heroui.com/icons` answers with the home page (`<title>HeroUI v3 (Previously NextUI)…`); its `llms.txt` names no icon package. "Hero UI icons" is read as Heroicons.
- `heroicons.com`: "316 icons", "MIT license", `github.com/tailwindlabs/heroicons`; 318 glyphs at `viewBox 0 0 24 24`, 321 paths at `stroke-width="1.5"`; present: `bars-3`, `magnifying-glass`, `check`, `x-mark`, `chevron-right`, `sun`, `moon`, `computer-desktop`, `pause`, `play`, `map-pin`, `bookmark`, `ellipsis-vertical`; **absent: `push-pin`, `grip`, `dots-six`**.
- Phosphor `@phosphor-icons/core` 2.1.1 (README: "1,248 icons and counting", six weights; `package.json` MIT): regular has `list`, `magnifying-glass`, `check`, `x`, `caret-right`, `caret-down`, `sun`, `moon`, `desktop`, `monitor`, `pause`, `play`, `push-pin`, `push-pin-slash`, `dots-six-vertical`, `bookmark-simple`, `sliders-horizontal`. The site already draws its pin and grip from it (build/site `src/components/Pin.jsx`, `styles.css` 484).
- Chosen: Phosphor Regular (s.19). The two sets at 16 px: both 1.5-stroke-at-24 grids [inferred]; a side-by-side is not shot; it is W5's to shoot if the maker asks for Heroicons' look.

**Specimen c6 at v1.6:** the foot removed; the header control's `/` cap removed; the drawn magnifier (a circle and a stroke) and the drawn menu glyph (three strokes) replaced by Phosphor's `magnifying-glass` and `list` SVGs, and the called candidate's text check "✓" by Phosphor's `check`; reshot `shots/c6-palette-desktop-{light,dark}.png` and `c6-menu-desktop-light.png`.

**To W11 (21:30):** references wanted for the side drawer, the desktop menu's contents (s.18), the bottom card (s.9), the list rows (s.7), the segmented switch (s.17), the Appearance control (s.15), the pinned shelf and its reorder (13.3); each screen with its Mobbin address beside the gallery's candidate.

## 28. Check of W9's eff159a (the palette's foot) and ce11053 (the shelf's reorder) on the deployed preview (21:33 UTC by `date -u`; bundle `index-Ck7dXJ_U.js`; shots `shots/c19-check-eff159a-palette-1280.png`, `c19-check-ce11053-{shelf,lift}-1280.png`, `c19-check-ce11053-{shelf,reorder}-390.png`) [measured: Playwright at 1280 and 390 × 844 at 2×, `?fixtures`; the palette opened by `/` with "mi"; the first grip focused, Space, ArrowRight, Space; the phone's Reorder tapped; `aria-live`, `localStorage`, the DOM read]

**Palette, as s.19 asks:** no foot, no `kbd`, no arrow or return character anywhere in the dialog; no icon on any row (0 `svg` in items); group labels "Pinned, States, Races, Candidates" in sentence case at the left; the chosen row's 3 px bar at the left, no tint. Still c6's drawn magnifier (`viewBox 0 0 16 16`) and the `/` cap on the header control: both wait on v1.6, sent to W9 21:30, not a difference.

**Reorder, as 13.3 and W9's note say:** six grips in the DOM, one per card, each a button "Move this race. Now N of 6."; the pin beside it "Unpin …"; on the desktop both appear on hover or focus. Keyboard: Space lifts, ArrowRight moves, Space drops; the live region says "Dropped at 2 of 6." and the order is saved at once in `localStorage["midterms.pins"]` (Attorney General now first). The lifted card keeps its look with the stronger edge and no shadow (W9's words; the shot `c19-check-ce11053-lift-1280.png` shows the focused grip in its ring). Phone: "Reorder" in the heading line as a 12 px bordered button, "Done" once pressed; in that state every grip (six dots, Phosphor's `dots-six-vertical`) and pin shows and the card has no link (`a` gone, so not pressable). All as specified.

**Differences, two:**
1. **An empty band above Pinned at 1280:** 206 px from the map legend's bottom (y 1027) to the Pinned heading (y 1233), and about 170 px below the right column's last object, the "All calls and closings" button. R1 and R5: nothing on the page is empty for its own sake. If this is the zoom's reserve (v1.3.3, the shelf below the map on W9's measure of the race zoom), W9 says so and it stands with its reason; if the overview's grid has a minimum height taller than its contents, the shelf moves up to the tallest column's end plus the section gap.
2. **The palette's field carries the 2 px dark focus ring for as long as the palette is open** (the field is focused on open and keeps focus while the arrows move the choice). Of the twelve cited palettes none draws a heavy ring on the field: Mintlify, Gumloop, v0 and Supabase show the field with a hairline or no edge, the focus being said by the palette itself. Candidate, under R5 (a box inside a box): inside the palette the field's focus style is its 1 px `--line-strong` edge, the ring kept for the menu's field and every other field on the page, where focus is not already said by a dialog. Not a build fault: a design line for s.16, written when W9 agrees it costs nothing for a keyboard user (the palette's open state is the focus state).

**To the spec:** s.16 takes (2) as a line once W9 answers; (1) waits on W9's reason.

## 29. Check of W9's c3d7830, s.18's desktop menu, on the deployed preview (21:35 UTC by `date -u`; bundle `index-Ck7dXJ_U.js`; shots `shots/c20-check-c3d7830-menu-{1280,390}.png` and `-end`) [measured: Playwright at 1280 (on /mi) and 390 × 844 (on /) at 2×, `?fixtures`; the menu opened by its button; the field, the rows, the tiles' boxes and the controls read from the DOM]

**As s.18 asks, at both widths:** the drawer 320 px; the search field first, full width (287 px inside), placeholder "Search a state, race or candidate"; **Pinned** as 13.1's compact rows with the short forms ("N.Y. · Governor · 6% in", "N.Y. · House 17 · No votes yet", "Mich. · U.S. Senate · 83.3% in"); **Country · Senate · House · Governors** as four links for now (the segmented control comes with Base UI, W9 21:25); **the tiles seven across, 36 px, 6 px gaps** (x 16, 58, 100 … 268 at 1280; the same at 390, the menu being 320 there too), 55 of them alphabetical by code with the territories AS GU MP VI after a hairline, the called states filled (GA, NJ blue; IA, MA red; WV other), the current state (MI) framed; then **Appearance** (System · Light · Dark); on the phone Pause follows. Nothing found against s.18's five points.

**Differences, two, the second small:**
1. **One short form for one race.** The menu's pinned row says "House 17" (short.js: 'NY|U.S. House|17' → 'House 17', as c6 drew it); the shelf's card for the same race says "N.Y. · U.S. House 17" (shot c19-check-ce11053-shelf-1280.png). 13.1 gives the pinned race one short form wherever it is compact; the shelf and the menu are the same object (s.18 (2): "a race pinned from the menu is reached the same way as from the shelf"). Either both say "House 17" (c6's form; the office's chamber is read from "17" with "N.Y." beside it) or both "U.S. House 17"; the spec's candidate is c6's "House 17", on R1.
2. **The field's focus ring on open:** the menu's field takes focus when the menu opens, so the 2 px dark ring sits on it in every opened menu (both shots). Same question as s.28 (2): where a surface opens with its field focused, the field's focus style is its 1 px `--line-strong` edge. Asked of W9 with s.28.

## 30. Check of W9's 7fbce7c, the Phosphor glyphs (s.19), the Base UI switch (s.17) and the two field edges, on the deployed preview (21:41 UTC by `date -u`; bundle `index-Cn9EOG5w.js`; shots `shots/c21-check-7fbce7c-switch-{0,100,200,300}.png`, `-palette-1280.png`, `-menu-1280.png`) [measured: Playwright at 1280 at 2×, `?fixtures`; every `svg`'s `viewBox` read; the Governors tab clicked with the animations paused on the next frame and seeked to 0, 100, 200, 300 ms; the focused field's computed outline and border read in the palette and in the menu]

**Glyphs:** the menu button, the header's control and the fields draw Phosphor's glyphs (`viewBox 0 0 256 256`; the control's magnifier 16 px, the button's list 20 px); eight `check`s on the called rows of the country view; the control reads "Search" with no key cap. **Switch:** the map's Senate / Governors is a `tablist` of two tabs, 76 px each (equal columns), with one animation on the indicator (`.seg-ind`): `transform`, 300 ms, a spring written as `linear()` (18 stops, reaching 0.96 at 61%); after the click Governors is selected, and the menu's four views are a second tablist with Country selected. The strip at 0/100/200/300 shows the indicator's travel. **The fields:** in the palette and in the menu the focused field has `outline: none` and its 1 px border, as v1.6.1 says; the shelf's card says "N.Y. · House 17" as the menu's row does. **Nothing to change.** v1.6.1 (d26a861) records all of it; the stamp written 21:42 was ahead of the clock by two minutes and is set to 21:40 here.

## 31. Check of W9's 5f617f3, 8.3 the chambers and 8.4 the phone's House, on the deployed preview (21:52 UTC by `date -u`; bundle `index-Chw3J72N.js`; shots `shots/c22-check-5f617f3-{senate,house}-{1280,390}.png`, `-senate-hover-1280.png`) [measured: Playwright at 1280 and 390 × 844 at 2×, `/senate`, `/house`, `/governors` with `?fixtures`; the DOM read for the title, the bar, the rows, the sticky heads, the source line, the map's outline on hover; `main.innerText` searched for "civicAPI" and "Results:"]

**As 8.3 and W9's note say.** Desktop: "Country" above, the title "Senate" with "35 races" aside in 12 muted; the seat bar full width (1,184 px); the rows in one column (632 px, 64 px tall, the state's name as the head at 15 / 600, the status under it, two candidates with party letters and shares at the right; a called row with the check and the colour, a changed call with "Call changed" in warn and the 3 px rule); the country map in the chamber's layer sticky beside them (520 px, `top: 72px`), a row under the pointer outlining its state (one outlined path on hover, measured), no preview panel drawn; no grid of boxes. Phone: the title once, the bar, the rows at 358 px, no map, no horizontal scroll. House on the phone: the rows under sticky state heads ("Alabama · new lines for 2026", 15 / 600, `top: 48px`), "District 1" as the row's head with the status under it, no table, no horizontal scroll; the desktop table stands, with the state's district map beside it.

**Differences, two:**
1. **No source line on any chamber view** (R7: "one line at the foot of a section, 12 px faint: Results: civicAPI. Called by civicAPI's decision desk; times are when this site first saw each call."): `main` holds no "civicAPI" and no "Results:" on /senate, /governors or /house at either width. W9's note says the per-box source lines are gone, which R7 asks; the one per section must stay, at the foot of the rows (and of the House table and list). Law 7: the source is said once wherever figures are.
2. **The status wraps on the phone**: "Polls close 1 AM ET" and "Polls close 11 PM ET" break onto two lines under "Alaska" and "Idaho" at 390 (the head column is about 200 px there). R8's phrase is **"Polls close 11 PM"**, without "ET": the header carries the zone once ("11 PM ET" beside the countdown), and the chamber's rows are all in one zone's words. With "ET" struck the status is one line at 390 [inferred from the widths: "Polls close 11 PM" is about 110 px at 12 px]. The same phrase in the search's rows and the state tiles' titles, wherever it is written with "ET".

## 32. Check of W9's f8c0367 (s.31's two differences) on the deployed preview (22:01 UTC by `date -u`; bundle `index-B3fKV8EI.js`; shots `shots/c23-check-f8c0367-src-{1280,390}.png`) [measured: Playwright at 1280 and 390, `/senate` and `/house` with `?fixtures`; `.src` read; `main.innerText` searched for "ET"; the stale status's box read]

R7's line is at the foot of each chamber view at both widths, the spec's words, 12 px, `rgb(138,143,150)` (`--faint`). No "ET" in any row, cell or status on either page. The stale status at 390 ("21% in" with "as of 10:38 PM" in warn) measures 102 × 32 px in the 104 px column: two lines, the break between the figure and the time. Ruled in v1.8.3: that break is the design at 390 (the two facts on two lines, never a break inside one); on the desktop one line. W9's reading of R8's reach confirmed and written into R8: statuses, not sentences or group heads. Nothing to change in the build. Surface 35 (cd540fa) is W8's to measure; its look is read when W8 reports.

## 33. Check of W9's 7bf9d22, ★3's accordion on the phone's House list and the calls' "more", on the deployed preview (22:27 UTC by `date -u`; bundle `index-DSLFMdEA.js`; shots `shots/c24-check-7bf9d22-house-390-{closed,ny,open}.png`, `-calls-1280-{closed,open}.png`) [measured: Playwright at 390 × 844 and 1280 at 2×, `?fixtures`; the 55 heads' boxes and styles read; Alabama opened by its label; the calls' label pressed; `getComputedStyle` of the panel]

**As v1.8.6.** 55 state groups, each a checkbox and a label (the Vault's CSS accordion), the head the toggle at 15 / 600 with the count in the status place at 12 muted; the count's phrases seen: "7 seats · none called", "1 seat · Polls close 1 AM", "9 seats · 3 called", "52 seats · Polls close 11 PM" (the four states of v1.8.7, bar "all called", which no fixture reaches); the mark Phosphor's `plus` (`data-icon="plus"`), rotated 45° when open; every group closed on arrival except New York (its pinned races); the open group's foot "Alabama: all races" at 12 muted; heads sticky at 48 px; the desktop table untouched. The calls: "26 more calls" a 12 px faint label with the plus, "Fewer calls" with the cross when open, the 26 rows in place, "All calls and closings" kept. **Pending from v1.8.7, which W9 has:** four heads at 62 px (two lines mid-phrase: California, North Carolina and Tennessee with the note beside the count; the Northern Mariana Islands' full name) take the two-line form and the short name. **Nothing else to change.**

**For W8:** the panel opens by a transition on `grid-template-rows` (510 ms, a `linear()` curve), the Vault item's own; that is a layout property (MOTION-SPEC rule 9), and the page below the group moves with it by design (the rows push the list down). W8 rules whether the accordion's open is the one place a layout transition is allowed, with the measure.

**W8's ruling (22:34 UTC, from W8's note of 22:31; surface 40 v1.8.14 and its Build column v1.8.16 s.30):** the layout transition is allowed as a dated exception to rule 9, the component's own 510 ms on `insert`'s curve, the text on opacity alone, no blur, no hover turn; it holds only while rule 12 holds at the phone's 4× profile. Measured on 7bf9d22: desktop calls line and phone at 1× pass; at 4× at the top of the 55-group list the body's height changes only every 65 to 70 ms (54 groups re-laid each frame, tasks 57 to 129 ms), a fail; at Texas it passes. W9's one knob is `content-visibility` and `contain` on the closed bodies and groups; the fallback is the body at once and the text on `reveal` 160 ms. Written into DESIGN-SPEC 8.4 (v1.8.8).

## 34. Check of W9's 09fa996, v1.8.7's three on the phone's House list, on the deployed preview (22:39 UTC by `date -u`; bundle `index-vIEv4Daj.js`; shots `shots/c25-check-09fa996-house-390.png` at California, `-ny.png` at the open New York) [measured: Playwright at 390 × 844 at 2×, `/house?fixtures`]

**As v1.8.7, pass.** 55 groups; every closed head is two lines at 59 px (the name at 15 / 600, then the count and the note in 12 muted), none overflows: "Alabama / 7 seats · none called · new lines for 2026", "California / 52 seats · Polls close 11 PM · new lines for 2026", "Northern Mariana Islands / 1 seat · none called" (the short name, s.16). The four phrases are all on the page in the fixture's hour: "Polls close 1 AM", "none called", "3 called", "all called" (Delaware's "1 seat · all called"), each with and without the note. The open New York head is 53 px with a 4 px bottom padding against the closed heads' 10, and its `scrollWidth` is 3 px over its box: both are the Vault item's own (the open question sits closer to its answer; the `plus` turned 45° overhangs by its diagonal, a transform, not layout), not faults. The head's cross, the rows in place, the list pushed down, as 8.4.

**One difference, for W9:** in the open group's rows at 390 the called row's status wraps mid-phrase, "Called by 10:07" / "PM" (District 1 of New York, the status cell about 190 px wide at 14 / 600). The time is one word: "10:07 PM" takes a no-break space (or `white-space: nowrap` on the time), so the status is "Called by" / "10:07 PM" at most. *Reason:* R8, one phrase in the status place; a time split across lines reads as two things. 12.3's two lines at 390 are by design; a break inside the time is not.

## 35. Check of W9's 318739c (the no-break time) and afbbfd6 (surface 37's stacked map cell) on the deployed preview (22:49 UTC by `date -u`; bundle `index-CM4XxWo5.js`; shots `shots/c26-check-afbbfd6-country-{1280,390}.png`, `-map-390.png`, `-map-gov-1280.png`) [measured: Playwright at 1280 × 900 and 390 × 844 at 2×, `?fixtures`]

**318739c, pass.** New York's called row at 390 reads "Called by 9:12 PM" on one line with the no-break space in the time; the header's "11 PM ET" carries it too; `document.body` holds no-break spaces where the times are. s.34's one difference is closed.

**afbbfd6, pass, no change to the look.** At 1280 the map cell holds two SVGs of 788 × 481 at the same top (522 px), one `visibility: hidden`, the other visible; after the Senate → Governors swap the two exchange and the shown one is the governors' colouring with the territories' row (VI, GU, MP) under it; nothing of the hidden layer shows at either state, the legend and the reserve under the map (13.3) as before. At 390 the section is the tile grid (no SVG), so the stacked cell does not apply there; the tiles and their legend as before.

**One read, not a fault, for W9 and W8 (b458145):** on Alabama's closed group the `.answer` computes `content-visibility: visible` and the group `contain: layout`; if the containment is on another element, W8's measure will say; the look is unchanged.

## 36. The maker's choice of the menu (23:54 UTC; RULINGS.md 23:51)

On the orchestrator's card "Which menu do you want, now that the measures are in?" the maker chose **"Bottom dock everywhere"** (the Vault's morphing dock, navigation-03, on phone and desktop, as built; the chamber figures stay on the page). The orchestrator's reading: surface 34 is the Vault's Morphing Navigation on both widths, built as DESIGN-SPEC 18.1 (a) specifies it, under its LICENCE note; the side drawer of 13:21 goes when the dock passes W8's measure on the preview; the top bar is not built.

**Written as v1.9:** 18.1 retitled and trimmed to the chosen one, (a) now "the menu, chosen" with two new paragraphs (what the panel holds on the desktop: the same objects, no Pause there, no tiles, 500 px wide, the height its content's capped at the viewport less 64 px, the list scrolling inside; the closed pill's sizes and the page's bottom inset of 86 / 70 px; what the drawer's removal changes: the header's menu button goes from both rows, s.4 goes when the dock passes W8's measure on the preview, the drawer's contents each placed, R5 and R6 read for the dock, the palette beside it, the night card over it, Escape and focus return as the Vault item has them), (b) kept as the record of the candidate not taken with the reason; s.2 and s.4 carry the supersession; s.15's place is the menu; s.19's `list` glyph goes with the drawer. The panel's figures stand as W8 measured them on the gallery until he re-measures on the site. **For W9:** build from 18.1 (a) and the two new paragraphs; the check of the look follows on the preview at 1280 and 390, closed and open, both schemes.

## 37. The maker's words of 23:54 on the logo and the faces gallery (23:57 UTC; RULINGS.md 23:54)

Verbatim, the parts for the design: "Five, I'm just gonna leave the logo that's there, except the only thing I want you to change for the logo is the 2026 is too far away from the word midterms. So I want that to be closer. Like it should be midterms, whatever, you figure it out. And then yeah, no more with the faces gallery."

**Measured on the preview (23:56 UTC, 1280, `shots/c27-logo-before-1280.png`, the header's left 420 px; and 390, `-390.png`):** `.logo` is a flex row with `gap: 9px` holding the 22 px tile, "Midterms" (17 px / 600, ends at x 196.5) and "2026" (17 px / 400 muted, `.yr`, starts at 205.5): the year's gap is the tile's gap, 9 px, 0.53 em. Plex Sans's space at 17 px measures 4.01 px at both weights (`measureText`). At 390 `.yr` is not displayed. **Written as DESIGN-SPEC v1.9.1, s.3:** the year at the type's own word space (0.24 em, 4 px at 17), one string "Midterms 2026" with the year's span for weight and colour, no flex gap between the words, the tile's 9 px gap kept; the phone unchanged. Mobbin, one search of eight web headers for a wordmark with a lighter second word: none carries one, so the measure rests on the type. **★2 closed as dropped** in s.20 and 20.3; W3's photo file stays as record.

## 38. Check of W9's 974c580, the dock as the menu (18.1 (a), v1.9 to v1.9.3) and the logo's year (s.3, v1.9.1), on the deployed preview (2026-11-03 00:38 UTC by `date -u`; bundle `index-lAgGjKzh.js`; shots `shots/c28-check-974c580-dock-{1280,390}-{light,dark}-{closed,open}.png` and `-390-{light,dark}-open-end.png`) [measured: Playwright at 1280 × 900 and 390 × 844 at 2×, `prefers-color-scheme` emulated, `/?fixtures`]

**The logo, pass.** The header's wordmark is one string, `Midterms <span class="yr">2026</span>`; the year's left edge is 3.8 px from the end of "Midterms" at 1280 (the type's space, 4 px by `measureText`; the 0.2 is the glyph's side bearing), 17 px, the year 400 muted; the tile's 9 px gap kept; at 390 the year is not shown, as before. The header's first child is the logo: the three-line button is gone from both rows.

**The dock, pass on both widths and both schemes, with two differences at 390 below.** Closed: `nav.dock`, 320 × 54 at x 480 and 32 px up at 1280; 250 × 54, 16 px up at 390; the logo at its left (with the year at 1280, without at 390) and the light "Menu" pill (78 × 46, #f5f5f5 on #0c0c0c) at its right; the surface dark in both schemes, as the maker saw it (the bar's wordmark white on the dark pill in the light scheme is that look, not a fault); `body` padding-bottom 86 / 70 px. Open: 500 wide at 1280 (x 390 to 890), 366 at 390 (x 12); the shell 558 px tall at 1280 (the content's: 54 + 24 + 456 + 24) and 566 at 390 (the cap, min(566, 844 − 96 = 748)); 32 and 28 px corners; the panel's top at 310 / 262. The content in order: the search field (placeholder "Search a state, race or candidate"; at 1280 focus lands in it on open, at 390 on the selected tab and no keyboard), Country · Senate · House · Governors as the Base UI control with Country chosen, a hairline, "Pinned" and the six pinned rows (place · office, status at the right), "Appearance" and System · Light · Dark, and at 390 Pause last; no state tiles. `aria-expanded` true on the toggle, which then reads "Close"; Escape closes (the surface back to 54) and focus returns to the toggle. Dark scheme: the surface carries an inset 1 px edge, rgb(61, 64, 70), the page's `--line-strong`, so the panel's edge is read on #121314. At 390 the content scrolls inside the panel (`.menu-content` 512 of 587 px, the end reached with 75 px of scroll).

**Two differences for W9, both at 390, both the panel's last rows:**
1. **The scroll box ends at the bar's top edge** (`.menu-content` bottom 774 = `.bar` top 774, padding-bottom 70), so before any scroll the last control, "Pause" (758 to 779), is cut five pixels into the bar's line and its word sits on the bar's logo (shot `-390-light-open.png`); after the scroll a 100 px hole stands between Pause and the bar (`-open-end.png`). **Rule:** the scroll box ends above the bar with the bar's own room, 16 px, and its cut edge is a 1 px hairline in the panel's line colour (the one already drawn under the segmented control), the list ending at that line; the padding-bottom inside the box is 16, not 70, so the end of the list and the hairline meet. *Reason:* R5, a separation drawn once with the lightest means; a word cut by a bar that holds another word is two things in one place, and a hole is a separation with nothing to separate.
2. **Pause is a bare word** (`button.pausebtn`, 15 / 400 white, no edge, no row), under the framed Appearance control, so it reads as a label, not a control (the same word in the header is a framed button, s.2). **Rule:** Pause takes the panel's control form: a full-width 40 px row with the 1 px edge and the radius the Appearance control has, the word at its left in 15 / 500, reading "Pause" or "Resume" (12.8), with the 16 px gap under Appearance that the blocks share. *Reason:* every other control in the panel has an edge (the field, the two segmented controls, the Close pill); the one that has none is read as text; the form is the one the panel already has, so nothing new is drawn.

**Small, for W9, not a look:** the header's logo and the dock's logo both define `<clipPath id="logo-r">`, a duplicate id in one document; the second resolves to the first, which happens to be the same shape, but it is invalid markup and breaks the moment one changes.

## 39. Check of W9's a6c928b, s.38's two differences and the duplicate id, on the deployed preview (2026-11-03 00:44 UTC by `date -u`; bundle `index-I-R7BWrf.js`; shots `shots/c29-check-a6c928b-dock-390-open.png`, `-open-end.png`, `-1280-open.png`) [measured: Playwright at 390 × 844 at 2× and 1280 × 900, light]

**Both pass; one remainder.** At 390 the scroll box ends at 758, 16 px above the bar's top at 774, with a 1 px hairline at rgba(255, 255, 255, 0.24) as its cut edge; the Pause row sits below the edge (759 to 799) and is reached by the scroll; nothing is cut by the bar. Pause is in the control form: 318 × 40, 15 / 500, a 1 px rgb(61, 64, 70) edge, 7 px radius, 17 px under Appearance (16 and the hairline). The two logos' clip paths are `logo-r` and `logo-r-dock`. **The remainder:** the box's padding-bottom at 390 computes 70 px, not the 16 the rule names (W9's note says 16), so after the scroll a hole of about 55 px stands under the Pause row above the hairline (`-open-end.png`); at 1280 it is 16. At 1280 the hairline shows and the box scrolls 5 px with the fixtures' six pinned rows (content 500 in a box of 495): the cap's doing, which **v1.9.4** removes (the cap is the viewport's height less 96 px alone; the Vault's 566 no longer caps), so with v1.9.4 built the 1280 panel is 570 tall and does not scroll with six pins.

## 40. The maker's words of 00:47 on the dock's pill; the ruling; the check's list grows (2026-11-03 00:51 UTC; RULINGS.md 00:47)

Verbatim: "Make sure things like this are centered and there should be space between the symbol and the word. And the logo should only exist in one place!! FIX ERRORS LIKE THIS" (with a photograph of the preview's closed dock).

**Measured on 974c580 at 1× (00:50; `shots/c30-pill-{390,1280}-1x.png`):** the dock's `.bar` is `flex; justify-content: space-between; padding 16px 4px`; the logo link inside it is `display: block`, so its `gap: 9px` does nothing: the tile's right edge and the word's left edge are both at x 108 at 390 (x 518 at 1280): **touching**. The pill keeps the Vault's width (250 / 320) and the pair is pushed to the walls: 61 px of nothing between the wordmark and the Menu pill at 390, 82 at 1280; the pair's centre is 6 px right of the pill's centre (201 against 195; 646 against 640). The logo also stood in the header: **twice on the page**.

**Ruled in DESIGN-SPEC v1.10:** (1) the logo lives in the dock alone (the pill closed, the panel's bar open, one element through the morph); the header loses it, and its countdown row starts at the left edge on both widths (s.2, s.3); (2) the pill hugs its content: 12 px, the tile, 9 px, the wordmark, 16 px, the Menu pill, 4 px; about 253 px at 1280 and 205 at 390, centred by construction; the logo's own form unchanged (23:54). Why the dock and not the header: the dock is the component he chose and its pill carries a brand by its own design; the header's logo was the duplicate; both are fixed on every scroll. W8's start width moves; his site measure decides.

**The check's list, grown (the orchestrator, 00:48, on the maker's capitals):** for every surface checked from now on, beside the measures already taken: (a) **the centring of every container's content** (the content's centre against the container's, in both axes, with the number); (b) **every pair of elements that touch** (adjacent rects with a gap of 0 or less, listed); (c) **the phone's surface at 1× as a photograph shows it** (a 1× shot read with the eye, not only the 2× measure); (d) **a thing shown twice** on one page (the same mark, word or control in two places, R6). s.38 passed the dock without (a), (b) or (d): the measures were of sizes and places, and the eye read the 2× shot at a size where 0 px and 9 px look alike. The next check carries the four.

## 41. Check of W9's 5d404d1 (a42bf01, 48f99d7, 5d404d1: v1.10's three), on the deployed preview, with s.40's four (2026-11-03 01:05 UTC by `date -u`; bundle `index-C0pwSo-u.js`; shots `shots/c31-check-5d404d1-{390,1280}-1x-{closed,pill,open}.png`) [measured: Playwright at 390 × 844 and 1280 × 900 **at 1×**, light]

**Pass on all three, at both widths.**
- **The pill's content (centring and spacing, s.40 a).** Closed, the pill is 210 × 54 at 390 (x 90 to 300) and 258 × 54 at 1280 (x 511 to 769), its centre the viewport's (195 / 640). Inside, left to right: wall to tile **12**, tile to word **9**, word to year **3.8** (1280 only), last to the Menu pill **16**, Menu pill to wall **4**: the rule's numbers. The tile's, the word's and the Menu pill's vertical centres are the pill's (801 / 841, within 0.9 px). The pair's centre sits 4 px right of the pill's, which is the 12 / 4 walls the rule sets; nothing in the pill is set apart by more than the 16, and the eye at 1× reads one object (`-pill.png`).
- **Touching pairs (s.40 b).** None in the pill or the header at either width (the probe lists adjacent rects with a gap of 0.5 px or less; its only hits were the pinned rows' "N.Y. ·" and "Governor" spans, which are one line of text with its own space, not two things). 
- **Shown twice (s.40 d).** One `svg.tile-logo` on the page and the wordmark in the dock alone; the header has no logo and no divider; the desktop row starts at its left edge with "Polls close in", the countdown, "11 PM ET", the chips; the phone row with "11 PM" and the countdown at the left, the right empty.
- **The photograph (s.40 c).** The 1× shots of the phone and the desktop read as the maker's photograph would: the tile, a space, the word, the light Menu pill, one dark object at the bottom centre over the page.
- **Open.** The panel is 570 tall at 1280 (box 298 to 798, 16 under Appearance) and 622 at 390 (box 206 to 758, 16 under the Pause row), neither scrolling with the fixtures' six pins; W9's fix of the content's height read at the open width is what removed the hole of s.39 (the 70 px padding is gone with it).

Nothing to change. W8's measure of the site's open and close on this commit (the start width now 210 / 258) is the gate that remains for the drawer's removal.

## 42. The maker's 11:33 words: the Reveal Navigation as a candidate menu; s.21 written (2026-11-03 11:40 UTC; RULINGS.md 11:33)

The orchestrator's part for the design (11:35): a candidate section deciding the drawer's order, the necessary buttons, the colours of the drawer and the put-away page, and the reading at both widths; then W9 builds on `probe/reveal` with the site's real contents, W8 measures, W5 checks at 1× with s.40's four. **Read:** the item's three files whole (`/mnt/project-files/vault/details-so/navigation-06/`, 14.8 KB: GSAP for the drawer's entrance and the divider, CSS `clip-path` and `linear()` for the page, a cover that closes on any press, inert and Escape and focus return built in; "no per-link stagger" and "retain the page's scroll ownership" are its own instructions); run on W11's gallery at 1280 and 390 (about 11:37): drawer 450 px at the right on #0c0a09, the page clipped `inset(16px 466px 16px 16px round 16px)` and shifted −100; at 390 the drawer is the screen and the page `inset(0 100% 0 0)` shifted −40; links Inter 48 / 38 px; the toggle 44 px at top 24 / 16, right 24 / 16; the cover black at 0.4. W8's measure of the item on its own page is in his s.? table (page 51 to 60 ms to first move, 850 to 860 long, gaps 35 to 47).

**Decided in DESIGN-SPEC v1.11 s.21 (candidate, not adopted):** the drawer holds, in order, the phone's search field (not the desktop's: the header's Search stays in view), the four views as the big links in the page's order with the current one marked by the item's own hover gesture standing (the line and the shift), the divider, Pinned as 17 px rows with the status at the right and no controls, Appearance as three words marked the same way (not the segmented control; said so he can choose), and the phone's Pause; the toggle is the one button, fixed at the top right (the header's row 56 px at both widths), the cover and Escape close, no Back and no second Close; the logo returns to the header on this branch and the dock goes; the drawer is the site's dark scheme in both schemes with no accent (the line in `currentColor`), the page keeps its scheme inside the card under the item's 0.4 dim, and the toggle is always the inverse of the ground it sits on (dark pill on the light page, light × on the dark drawer); the item's motion untouched, failing the page-still rule by design for the maker's ruling on W8's numbers.

## 43. W11's nine sheets for the phone's race card, looked at on a touch emulation at 390 × 844, 1× (2026-11-03 12:21 UTC; W11's note of 12:15, probe/components aefbea9, `components/sheets.html`; shots `shots/c32-sheet-<name>-{open,drag,afterflick,afterback}.png`, copies in `/mnt/project-files/design/sheets/`) [measured: Playwright Chromium, `isMobile`, `hasTouch`, touch events through CDP; two scripts, `sh1.js` and `sh2.js`]

**What this emulation can and cannot tell.** It can tell whether a sheet follows a slow finger and where it settles, whether a short drag snaps back and a flick closes, whether the browser's back closes the sheet, what the overscroll guard sets, and what the eye sees at 1×. It cannot tell iOS's feel (the settle curve, the rubber-band of the page), whether Chrome on a phone reads a slide as pull-to-refresh (the emulation has no browser chrome), nor the thumb's reach. Those stay for a device; the maker's own phone is the one that rules.

**Seen by eye at 1×, all seven library sheets (Silk, Base UI, the `dialog`, Zag, Vaul, react-modal-sheet, Cupertino):** the same card, as the site's own: the grip 36 × 4 in `--line-strong` at the top, 12 px corners, the head "Governor · New York · Pinned · test data", the two rows with the check and the party colour, the call line, "100% of precincts in", the incumbent, the source line; no Back and no × on any. **The one look fault they share:** at the 0.55 stop the sheet shows about 460 px and the card's content ends about 250 px in, so **165 to 218 px of empty sheet stand under the source line** (`emptyBelow` 164 to 218 measured; the shots). That blank half is the "messy" the maker named at 11:33 more than any library's doing; W11's second pass (the state's card 16 px behind) does not fill it, since it sits behind, not below. **The rule for it (for DESIGN-SPEC s.9 if the maker keeps a sheet):** a race card's stop is its content's height plus the grip and a 16 px foot, up to 0.55 of the screen; the 0.55 stop is for the state card, whose content outruns it. **The scrim:** Silk, the `dialog`, react-modal-sheet and Cupertino dim the page (grey; Cupertino's 0.4 black); Base UI, Zag and Vaul show no dim at all, so their sheets sit on the bright page with a hairline and the edge is weak (the dock's s.9 dim is the spec's). 

**Touch, per sheet** (a slow 120 px drag from the grip, sampled every 10 px; a 60 px slow drag; a 320 px flick; the browser's back after a reopen):
- **Silk:** follows the finger one to one (417 → 522) and snaps back to the stop on release; the flick and a 300 px slow drag did not close it in this emulation (it rides native scrolling, which the CDP touch may not drive); back: unverified here (the host element's box could not be read). 
- **Base UI:** follows (380 → 480), snaps back; the flick closes; back closes the sheet and the hash goes.
- **The browser's `dialog` (crafted):** a 60 px drag snaps back, a 120 px slow drag closes (the threshold is low: a quarter of the stop), the flick closes; **back leaves the page** (it went to `about:blank` with the sheet open: the dialog pushes no history entry).
- **Zag (as built minus the Back):** follows (380 → 500), snaps back; the flick closes (the content's transform to 0, the box at 844); back closes and the hash goes.
- **Vaul:** follows (415 → 526), snaps back; the flick closes; back closed it in the first run (hash gone).
- **react-modal-sheet:** resists the finger at first (454, 464, then back to 444 while the finger still moves: a rubber-band at the stop, not a follow); a 60 px drag snaps back; the flick closes; back closes.
- **Cupertino:** follows; **a 60 px slow drag closes it** (no snap back; too eager); the flick closes; back closes.
- **The dock morph (navigation-03-race):** no drag, the Close pill and back; the dark panel holds the card in light text, readable, the call line in the dark scheme's blue; **the bar's logo slot shows an empty light shape** at the left (the brand slot with nothing in it), a fault of the page, not the component; back: unverified.
- **The side drawer (section-03-race):** a white panel the height of the screen from the right, × at the top, "PINNED · N.Y." eyebrow, the card at the top and 395 px of empty panel under it; no drag; **back did not close it** in this run (the panel still in view after back).
- **The overscroll guard:** `overscroll-behavior: none` on `html` and `body` while every sheet is open, `auto` after it closes, on all nine.

**For the maker's eye on a device:** Base UI, Zag and Vaul behave alike here (follow, snap, flick, back); Silk's close by drag could not be driven; the `dialog` and Cupertino close too easily; react-modal-sheet does not follow. The look is the same card on all seven, and the blank under it is the thing to fix whichever he picks.

**Correction and the four within rule 12 (12:24 UTC; `sh3.js`, each sheet's own open state read: `dialog.open`, Zag's content box, navigation-03's `data-open`, section-03's `clip-path`).** Two lines above were wrong and are withdrawn: **the `dialog`'s back closes the sheet** (the hash goes, the page stays; the `about:blank` came from a run where no sheet was open), and **section-03's back closes the drawer** (its clip returns to `inset(0 -1px 0 100%)`; my earlier read used the panel's box, which does not move). So **back closes all four** that W8 leaves within rule 12 at 4× (his s.50: the `dialog`, Zag with the faults removed, the dock as a sheet, section-03). A tap on the page above the sheet closes the `dialog` and the dock; **not Zag** (its background is the site's own inert layer, `modal: false`, s.9, so the tap does nothing: for a native feel the scrim should close it, which Zag's `closeOnInteractOutside` gives); section-03 was not tested for it (the panel is the whole width but 16 px).

**The order of the four, for the orchestrator and the maker:**
1. **Zag, with the faults removed.** By thumb it is the native one of the four: it follows the finger one to one, snaps back from a short drag, closes on a flick and on back, and the grip is its handle. By eye it is the site's card with no dim: the scrim of s.9 is to be drawn (and to close on a tap), and the blank under the card closed by the content-height stop. It is the component already paid for.
2. **The browser's `dialog`, crafted.** The same card, dimmed by the browser's own backdrop, back closes it, a tap outside closes it; the drag is hand-written and closes on a 120 px slow drag (a quarter of the stop) where Zag snaps back, which is the one place a thumb will feel the difference; no drag library at all is its gain.
3. **The dock as a sheet (navigation-03).** The morph the maker likes, back and the Close pill close it; but a race card is a thing read and let go, and this has no drag, so the thumb's way out is a pill; the dark panel puts the card in the dark scheme over the light page (two schemes on one screen, and the call line in the dark blue), and the bar's logo slot shows an empty light shape. It fits the menu, not the card.
4. **section-03, the side drawer.** A full-height white panel from the right for a 250 px card: 395 px of empty panel, no drag, the × the way out; a side drawer is the desktop's idiom for a list, not the phone's for a card.

## 44. Check of W9's reveal preview, probe/reveal 6b4d266, against s.21, with s.40's four (2026-11-03 12:31 UTC; https://midterms-git-probe-reveal-zachs-projects-74dd78e7.vercel.app/?fixtures; bundle `index-BBqXTIUb.js`; shots `shots/c33-reveal-6b4d266-{1280,390}-{light,dark}-{closed,open}.png`, copies in `/mnt/project-files/design/`) [measured: Playwright at 1280 × 900 and 390 × 844, 1×, both schemes emulated]

**As s.21, with two faults of the spec's own figures (corrected in v1.11.2) and nothing of W9's.** Closed: the toggle 100 × 44 at top 6, right 24 (1280) and 16 (390), fill #16181b with #fbfaf8 glyphs in the light scheme and #ecebe7 with #121314 in the dark; the header 56 px (57 with its rule) at both widths; one tile-logo svg, the wordmark once, in the header; no dock, no body inset; the page scrolls inside `.page-content` (overflow auto, the viewport's height). Open: the drawer 450 wide at 1280 and the screen at 390, #121314 with #ecebe7 text; the page clipped `inset(16px 466px 16px 16px round 16px)` and shifted −100 at 1280, `inset(0 100% 0 0)` and −40 at 390; the cover black at 0.4; the toggle 44 wide, #ecebe7 with the × in #121314, "Close menu"; the four links Plex 500 at 48 / 38 px, Country marked (`aria-current="page"`, the line at scaleX 1, the word shifted 33.6 / 26.6 px); the divider; Pinned's six rows with the status at the right; Appearance's three words at 17 px with System marked the same way; at 390 the field first (placeholder as s.16, the 1 px #2a2c30 edge, no fill, not focused on open) and Pause last, below the fold (the drawer scrolls 70 px). Escape closes and focus returns to the toggle at both widths and schemes.

**By eye at 1×:** the drawer reads as the item with the site's words; the mark before the current word reads as a dash, which is the item's gesture and was the design's choice; the put-away page's header is cut at its left by the 100 px shift ("rms 2026" shows), the item's own behaviour on its demo, kept. **Centring:** the toggle's centre is the header row's (28 against 28.5). **Touching pairs:** none inside the drawer (the probe's only hits are the "N.Y. ·" and office spans of one line); **one in the header at 1280: the Pause button's right edge at 1156 is the pill's left edge**, a 0 px gap, which the eye reads at once in the closed shot. The spec's own figure caused it (21.2 said the items end 124 px before the edge, which is exactly the pill's width plus its offset); corrected to 140 px (16 px from the pill). **Twice:** nothing. **One more figure corrected:** at 1280 × 900 with six pins the drawer's content plus 96 px below ran 31 px past the viewport and scrolled for a third of a row; the bottom padding is 48 now.

**W9's four choices, confirmed in v1.11.2:** (a) the pinned status in the call's colour where a call stands (R4); (b) top-aligned while typing on the phone (rule 8); (c) the toggle hides under a phone card (the page is inert under it); (d) the item's breakpoints for the drawer, the site's 899 for the toggle's offset.

## 45. The phone's state and race: the survey's phone half, the native idioms, one recommendation (2026-11-03 12:45 UTC; the maker, 12:37 and 12:40; the orchestrator's brief of 12:39 as narrowed at 12:40: half an hour, one reading, no preview page; DESIGN-SPEC s.22)

**What was read** [measured: the brainstorm's survey, `designsystembrain/research/midterms-site/survey/2026-11-02-S1-election-sites.md`, its catalogue (Kinds 1 to 5), "What exists" and "Phase 2", and its 21 phone shots at 390 × 844 in `survey/shots/*-390.png`; six looked at whole at 2×: Fox's New York state page, 270toWin's New York page, Fox's Senate map page, NBC's and NPR's and CNN's president pages]. The timebox was kept: 12:41 to 12:45.

**How a state opens on a phone, site by site.**
- Fox (2026): the Senate map is a column of state circles; the page's own text says tap on phone; a state is **its own page** (`/state/new-york`), stacked sections House, Governor, Ballot measures, Polls; the browser's back [measured: `fox26senate-senate-390.png`, `fox26ny-state-ny-390.png`; the survey's row 1 and 3].
- 270toWin / DDHQ (2026): "Results By State" tab; New York is **its own page** with Overview, Governor, then the chambers; a breadcrumb "2026 Governor Battle for Control > New York" at the foot; the browser's back [measured: `t270-26ny-state-ny-390.png`].
- NBC (2024): "State results ⌄" dropdown in the strip, "State breakdown" tab; a state is a page [stated: the survey's row 4; the shot shows the strip].
- NPR / WBUR (2024): "STATE ▾" in the top bar, an A–Z list; a page [stated: row 9; `npr24-president-390.png` shows the bar].
- BBC (2024): "Browse all states A–Z"; a page [stated: row 10].
- CNN (2024): "Results by State ⌄" menu; a page [stated: row 6].
- Ballotpedia, Wikipedia: pages [stated: rows 18, 19].
- **No site** opens a state in a sheet, a modal, a drawer or an expanding tile on a phone [measured: none of the 21 shots shows one; the catalogue's Phone column names none].

**How a race opens on a phone.** Inline **on the state's page**, read by scrolling: Fox lists each House seat as a table block (candidates, votes, %; "Polls open at 6:00 AM ET"; "Source: The Associated Press") and then "Governor Race Results" with the candidates' portraits; 270toWin shows "Governor" with a consensus-forecast dial and DDHQ's race cards in one column [measured: the two New York shots]. National pages show races as cards or tables in one column (Fox's Hot Races, CNN's Key races, NPR's grouped tables) [stated: "What exists"]. No per-race sheet or modal was seen; the survey's "Left for a later pass" names race-detail pages for House districts as not read, so whether any site has a race page of its own on a phone is **unread**.

**The native idioms, weighed for this site.**
1. **A pushed page** (the platform's navigation stack: a title, a back control that names the previous place, the new page from the right, back to the right by the edge gesture): fits a thing that is read whole and has an address; the survey is unanimous; W8's v1 to v1.5 phone design was this and his reasons stand in MOTION-SPEC surface 10; `navmotion.js` still carries it (`nav-in` 680 ms spring, `nav-back` 450); the router's `goBack` already makes the back true from the shelf and from a shared link [measured: `src/lib/navmotion.js` 1–20, `src/lib/router.js` 40–66, read 12:43].
2. **A sheet** (short, handled, dismissed by a pull): fits the menu, the calls list and the night card; does not fit a state or a race: the maker's two complaints (11:33) are the idiom's drag and its invented back; s.43 saw them in all nine sheets; the 55% stop shows half of a page.
3. **Inline expansion** (an accordion row): fits short rows compared in a list (8.4's House groups); a race's block, parts table and map are a screen and a half, which carries the rest of the list away and gives no address to share.
4. A modal and a fade: set aside in s.22.3.

**The recommendation** is s.22: pushed pages for both, the desktop's views in one column with the desktop's title-row back ("‹ Country", "‹ New York"), the dock and header kept, W8's push as the transition, and `Cards.jsx`, `RaceCard.jsx`, the phone's `Race.jsx`, the 55% stop and the dock's hiding removed. What this removes was the maker's 13:08 word, withdrawn at 12:37; nothing asks him, by his 12:40.

**Not done, by the narrowed brief:** no preview page, no brief to W11, no Mobbin or details.so search (the survey and the site's own code answered the question; a search would have cost the half hour on things not evidence).

## 46. W9's two corrections on probe/reveal 8a390c1, the obvious check (2026-11-03 12:46 UTC; bundle `index-BpJzvxYx.js`; shots `shots/c34-reveal-8a390c1-{1280,390}-{closed,open}.png`) [measured: Playwright at 1280 × 900 and 390 × 844, 1×, light]

- **21.2, the header's right-hand items end before the pill.** At 1280 the last item ("Pause") ends at 1140, the pill starts at 1156: 16 px to the pill, 140 from the edge, as specified. At 390 the last item (the countdown "20:00") ends at 254, the pill at 274: 20 px to the pill, 136 from the edge; W9 read 16 and 132, so the 4 px is the countdown's own width at the moment measured or the box read (the countdown is tabular and its text changes), not a fault to act on.
- **21.1, the drawer's bottom at 1280.** The last row ("Dark") ends at 844 in a 900 drawer: 56 px below it (W9's 48 plus the row's own line box); six pins do not scroll at 1280 × 900; at 390 × 844 the drawer scrolls 70 px, as 21.1 allows.
- **By eye at 1× (s.40's four):** the open drawer reads as before (s.44); nothing new touches, nothing shown twice; the closed phone header has the pill at the right edge with the countdown before it.

Ready for the maker's eye; told the orchestrator 12:46.

## 47. The maker's 12:50 on the reveal: Appearance at the top, the drawer that did not scroll, and the case that does not fit (2026-11-03 12:54 UTC; DESIGN-SPEC v1.12.1: 21.1 revised, s.23 added)

His words (RULINGS.md 12:50): "I prefer the concept of the reveal sidebar, but far more work needs to be done. I want the appearance toggle at the top, not the bottom because it becomes invisible. Also if anything falls below the screen in the menu I cannot scroll down to see it. These are all things you should catch yourself."

**My miss, stated.** s.44 checked 8a390c1's predecessor at 390 × 844 and 1280 × 900 with the fixtures' six pins; s.46 wrote "at 390 × 844 the drawer scrolls 70 px, as 21.1 allows" from `scrollHeight` alone, without scrolling to and pressing the last control, and without a shorter screen. The check proved the case that fits.

**What the preview does under emulation** [measured: Playwright, `index-BpJzvxYx.js`, touch by CDP `Input.dispatchTouchEvent` on the phone, wheel on the desktop; scripts `rv3.js`, `rv4.js`]:
- 390 × 844: the drawer (`overflow-y: auto`, `touch-action: auto`, `position: absolute`, 844 tall) overflows 70 px; a touch drag scrolls it 70 and the last control (Pause) comes from 866 to 796.
- 390 × 664: overflows 250; scrolled 250; Pause from 866 to 616. 360 × 640: the same layout (Pause at 840–866, 200 px below the fold).
- 1280 × 720: overflows 163; the wheel scrolls it; Dark from 835 to 672.
- The content block is a flex column with `justify-content: center`; the first control's top is at 88 (phone) and 96 (desktop), so the top is not cut at these heights; the cover (`z-index 1`, pointer events on) lies over the page's side; `elementFromPoint` mid-drawer is the drawer's list.
So in emulation the drawer scrolls and the fault is **not reproduced here**; on his phone it did not [stated]. Candidates for W9 to trace on the device: iOS Safari's handling of a scroller inside the clipped, transformed page frame or with the body's scroll lock; a transform or `will-change` left on the scroller by the GSAP entrance; `justify-content: center` cutting the top once ten pins or larger text push the first control above the edge (not at these heights, but at 125% text it will). The spec now names the mechanism that is known to work (21.1, v1.12.1) and requires the reach on a real phone.

**Appearance at the top:** 21.1 item 0; one row of the three words if the mark reads on a row, else stacked; W9 says which.

**The check list grew** (s.23): a short screen (390 × 664, 360 × 640, 1280 × 720), the full load (ten pins, the fixtures night, long words), 125% text, and the last control reached and pressed in each, on a real phone where one is at hand. The reveal is checked against it when W9's next note comes.

## 48. The maker's 13:00: every drawer is Cupertino Pane, halfway by default (2026-11-03 13:05 UTC; DESIGN-SPEC v1.13, s.9 rewritten as the drawer rule)

His words (RULINGS.md 13:00): "If a drawer is needed anywhere on the site I want the Cupertino pane to be used. Also, where the drawer need not be opened in full screen to show more relevant information, open it halfway. It may be that the site doesn't use drawers anyway."

**What the rule rests on** (no new measuring; the facts are the record's):
- cupertino-pane 1.4.21, MIT, plain JavaScript, its own motion and drag; one instance per opening (a pane presented again after destroy stopped closing on a drag down) [stated and measured: W11's `s-cupertino.jsx` on probe/components, read whole 13:05].
- 23.8 KB gzip with Preact on W11's page, against Zag 43.9, Silk 51.8 [measured: W11 s.398].
- Under touch emulation it follows the finger, the flick closes, back closes; a 60 px slow drag closes it with no snap back, which s.43 called too eager [measured: my s.43].
- At the 0.55 stop every sheet showed 165 to 218 px of blank under a short card [measured: s.43]; hence the rule that the half is a ceiling and a short content's pane is content plus grip plus a 16 px foot.
- W8's gallery measure at 4×: one gap of 60 ms, no stall after the first frame (his s.50; MOTION-SPEC line 202).
- The pull-to-refresh guard: the library sets `overscroll-behavior: none` on the body while open; the site restores `auto` [measured: s.43, all nine].

**The rule as written (s.9.1 to 9.8):** the library and one instance per opening; the middle break at half the screen as the default, the half a ceiling for short content, the top break only when the first screen does not fit the half or the half hides what the press was for (applied: the calls sheet full, the night card halfway); scrim 0.4 with tap-to-close, the page inert and never scaled; the site's grip and corners, no Back and no × (the page's title row answers the 13:21 ruling); flick and far drag close, a short drag snaps back (W11 to set or patch the threshold, or say it cannot); one history entry per opening so back closes and never leaves the site; Escape, focus, `role="dialog"`; reduced motion `animate: false` both ways, the drag still following; W8 writes the figures into surfaces 6 and 32 P from the build; the check at 1× with s.23's cases.

**What this withdraws:** s.9's Zag card and its stops (the state and race are pages, s.22; the menu is the reveal); Zag leaves the bundle with its last user. Open to W11's inventory: whether any other drawer exists on the build (the dock's panel goes with the dock).

## 49. Check of W9's reveal preview d3a258c against the maker's 12:50 and s.23 (2026-11-03 13:11 UTC; https://midterms-git-probe-reveal-zachs-projects-74dd78e7.vercel.app/?fixtures; bundle `index-Dfv9-4Q4.js`; shots `shots/c35-reveal-d3a258c-*.png`, copies in `/mnt/project-files/design/`; script `rv5.js`) [measured: Playwright at 1×; touch by CDP on the phone sizes, wheel on the desktop; ten pins written to `localStorage["midterms.pins"]` (the six defaults plus GA, NC, ME and AK Senate); 125% text emulated as page zoom, a 312 × 531 viewport, since the site's type is in px and a root font size moves nothing]

**The two faults of 12:50.**
- **Appearance at the top:** the row "— System · Light · Dark" is in the first screen at every size: 195 px from the top on the phone (after the field), 132 on the desktop, words 32 px apart as W9 chose; the current one carries the line and the shift. Pressing "Dark" changes the scheme (not re-measured here; W9's).
- **The drawer reaches its last control:** with ten pins the drawer overflows 349 px at 390 × 664, 238 at 1280 × 720, 482 at 312 × 531 (125%), 223 at 360 × 640 with six; a finger drag (phone) or the wheel (desktop) scrolls it to the end in each, the last control (Pause on the phone, the tenth pinned race on the desktop) comes into view and takes the press: Pause toggles with the drawer open, the pinned race closes the drawer. The top is reachable again at scrollTop 0 (`margin-block: auto`, not centring). The page behind stays at 0.
- The six-pin case at 390 × 844 (overflow 19) and 390 × 664 (199) and 360 × 640 (223) passes the same way.

**By eye at 1× (s.40's four), one fault:** at the scrolled end on the phone, **"Pause" sits 12 px under "Mich. · U.S. Senate" in the same form and reads as a seventh pinned race** (`c35-reveal-d3a258c-390x664-open-end.png`). Spec 21.1 item 6 now gives it 24 px above (v1.13.2); W9's to apply. Nothing touches, nothing is twice; the desktop's open state reads as in s.44 with the Appearance row above the four words (`c35-reveal-d3a258c-1280x720-open-end.png`).

**Not done here:** a real phone (none at hand; W9 says the same), so the device fault of 12:50 is answered by the mechanism (21.1, v1.12.1) and emulation only; the maker's own phone is the check that rules.

**Addendum 13:16: e685b0b serves** (bundle `index-m2B1x1cu.js`): the gap above Pause measured 24, the rows 12 [measured: `rv7.js` at 390 × 664]. **Then the maker's 13:13** overruled two things in it: the drawer must follow the scheme (it was dark in both), and Appearance must be the site's segmented control, not a row of marked words ("that works vertically but not horizontally"). Spec v1.13.3: 21.1 item 0 (the control is `Appearance.jsx` as the dock had it, Zag's radio group in the `.seg` frame, 300 px on the desktop and the content width on the phone, instant switch per surface 36) and 21.3 (light: `--panel` ground, `--fg`, `--muted`, `--line-strong` edges, the control's chosen fill `--bg`; dark as before; the pill always the ground's ink; the dim 0.4 in both). My miss to state: the row of marked words was my 21.1 item 5's form carried sideways at 12:50, and the dark-in-both-schemes rule rested on a comparison with the dock that no longer exists; both were mine, and the horizontal row should not have passed my own eye at 1× in s.49 (it read as a list laid sideways, as he says).

## 50. Check of W11's drawers on Cupertino Pane, build/site 6c713bb, against s.9 (v1.13.1) and s.23 (2026-11-03 13:46 UTC; https://midterms-git-build-site-zachs-projects-74dd78e7.vercel.app/?fixtures; bundle `index-btfKwkK1.js`; shots `shots/c36-cup-6c713bb-{night,calls}-<size>-{open,up}.png`, copies in `/mnt/project-files/design/`; scripts `cup1.js`, `cup2.js`) [measured: Playwright at 1×, touch emulation (`isMobile`, `hasTouch`, drags by CDP `Input.dispatchTouchEvent`), the fixtures night; 390 × 664, 360 × 640, 390 × 844, and 312 × 531 as 125% text; no real phone]

**What passes (both drawers, every size):**
- **Opens at the half exactly:** the pane's top at innerHeight ÷ 2 (332 at 664, 320 at 640, 422 at 844, 265 at 531); hash `#night` / `#calls`; the dim `rgba(0,0,0,0.4)`; `#main` and the header inert; `overscroll-behavior: none` on html and body while open, `auto` after.
- **The look:** the grip 36 × 4 in `--line-strong`, 8 px from the top, centred (0 px off); 12 px corners; the title ("The night", "The night's calls") 26 px under the top edge; no Back, no ×; the content is taller than the half in both (the night card by 255 to 883 px, the calls by 2.5 to 3.7 k), so no blank stands under it (by eye: `c36-cup-6c713bb-night-390x664-open.png`, `…-calls-390x664-open.png`).
- **A 60 px slow drag snaps back** to the half (top unchanged) in every run; **a flick closes** at 390 × 664, 390 × 844 and 312 × 531 (the wrapper gone, the hash gone, inert off); **a drag up takes the pane to full** (top 26) and the content scrolls to its last line; **the browser's back closes** it and the address is the page's again; reopening by the trigger pushes the entry anew.

**One fault, at 360 × 640 only: a flick leaves the page blocked.** After a 320 px flick down from the grip, the night pane sits at top 640 (its bottom break, height 0, below the screen) but the wrapper stays visible, **the backdrop stays displayed at opacity 1 with pointer events on, the hash stays `#night`, `#main` stays inert**, and the trigger cannot be tapped (Playwright: "backdrop … intercepts pointer events", three seconds of retries); Escape does nothing because the pane has already "settled". The same flick at 390 × 664 closes cleanly. Reading [inferred]: the bottom break at height 0 is a break the release can settle on; at this height the release ended on it rather than past it, so the library moved the pane to the break and fired no dismiss, and the site's own close work (the hash, inert, the backdrop) waits on a dismiss that never comes. For W11: a settle on the bottom break must count as a close (destroy or hide, pop the entry, lift inert and the dim), or the bottom break goes back to disabled with another cure for the 60 px close (9.5). Checked after the fix at 360 × 640 and 390 × 664 again.

**Not seen here:** a real phone, iOS's pull-to-refresh and its rubber-band; the maker's phone rules.

## 51. Check of W9's reveal preview ceadeec against v1.13.3 (both schemes) and s.23 (2026-11-03 13:50 UTC; bundle on the preview; shots `shots/c37-reveal-ceadeec-{1280x720,390x664}-{light,dark}-{open,switched}.png`, copies in `/mnt/project-files/design/`; script `rv8.js`) [measured: Playwright at 1×, `colorScheme` emulated, ten pins in storage, touch on the phone size]

- **Colours, light:** ground rgb(242,241,237) = `--panel`; ink rgb(22,24,27) = `--fg`; eyebrows rgb(91,96,104) = `--muted`; the divider and the field's edge rgb(201,198,191) = `--line-strong`; the control's frame `--line-strong`, its chosen fill rgb(251,250,248) = `--bg`; the pill closed `--fg` with a `--bg` glyph, open `--fg` with the × in the drawer's ground. **Dark:** ground rgb(18,19,20), ink rgb(236,235,231), muted rgb(162,166,173), lines rgb(42,44,48), the control's frame rgb(61,64,70) = `--line-strong` dark, fill rgb(26,27,30) = `--panel` dark; the pill light with a dark glyph both ways. All as 21.3 (v1.13.3); no colour that is not a token.
- **The control:** 34 tall, 7 px corners, 2 px padding, three equal columns (97 px each in the 300 at 1280; 109 in the 338 at 390), 15 px, the chosen one 600 in `--fg` on the fill, the others `--muted`; 12 px under the eyebrow, 28 above "Country"; left at 854 on the desktop, at 20 on the phone. **Pressing another segment while the drawer is open** recolours the drawer, the page and the pill at once with the drawer open (`data-theme` set; measured both ways at both widths).
- **Reach (s.23):** ten pins; the last control (Pause on the phone, the tenth pin on the desktop) in view and pressable after a drag or the wheel at 390 × 664 and 1280 × 720, both schemes.
- **By eye at 1×:** the light drawer reads as the stone stage under the dimmed page card; the control reads as the dock's control and not as a list; nothing touches, nothing twice; the dark drawer as before with the control in it. **W9's width question:** the phone's content is 338, not the 358 I wrote, because the drawer's padding is 20 left and 32 right (the pill's room, v1.12.1); kept, and the spec corrected (v1.13.4).

Ready for the maker's eye.

**Addendum 13:57: build/site 30cad1f recheck** (bundle `index-BXyvwVv9.js`; shots `shots/c38-cup-30cad1f-{night,calls}-360x640-{open,up}.png`) [measured: `cup2.js`, `cup1.js`]. W11's reading of the library: a flick of the pane's own offset lands exactly on the bottom break, and the library's `destroy` then waits on a `transitionend` that never comes because there is no distance to travel; his fix finishes such a destroy by hand and runs the same dismiss path. At 360 × 640 the night and calls panes now open at 320 (the half), a 60 px slow drag snaps back, **the flick closes** (wrapper gone, hash empty, inert off, overscroll restored) and the trigger reopens the pane at the half; the drag up reaches full and the content scrolls; back closes. At 390 × 664 the flick close and the reopen pass as before (the longer run there stopped on a Playwright flake, the countdown's re-render detaching the trigger mid-scroll, not a site fault). The s.50 fault is closed. The drawers are ready for the maker's eye in emulation; a real phone is still unseen.


**Addendum 14:10: build/site def0c97 recheck** (bundle `index-BhJHBU_z.js`; shots `shots/c39-cup-def0c97-{night,calls}-{360x640,390x664}-{open,up}.png`) [measured: `cup1.js`]. With the night state moved to its own store and the settle work moved to the transition's end (W11, the orchestrator's 13:57 on W8's s.57), every state of the s.50 list holds at 360 × 640 and 390 × 664 for both drawers: open at the half (320 / 332), dim 0.4, grip 36 × 4 at 8 px centred, 12 px corners, inert and overscroll none after the settle, hash; the 60 px drag snaps back; the flick closes with the page freed; the trigger reopens at the half; the drag up reaches full (top 26) and the content scrolls; back closes and the address is the page's. Closed.

## 52. Reveal Navigation 2.0 (`navigation-07`) read whole, and the navy/red/white palette (2026-11-03 14:26 UTC; the maker, 14:23; DESIGN-SPEC s.24) [measured: the Vault folder `/mnt/project-files/vault/details-so/navigation-07/` (index.html 1,965 B, style.css 10,032 B, script.js 3,847 B, SOURCE.md), read 14:26; never into git]

**What 2.0 adds to 06:** two `.sheet` divs (`back`, white, depth 2; `front`, `--accent` #BC4A3D, depth 1) between the drawer (z 1) and the page (z 4), `pointer-events: none`, each clipped `inset(gap + step × depth, 0, gap + step × depth, gap, round 16px)` closed and, open, `inset(…, drawer-width + gap − step × depth, …)`, with the page's open ease (800 ms `linear()`) delayed 35 ms × depth and the 510 ms close; `--drawer-width` 482 (392 under 900; `100% − 64` under 600 with gap 8, step 8, page-shift −40). The script is 06's (GSAP timeline for the content's 80 px entrance and the divider; the cover click, Escape, the link click close; inert on the content). Nothing else differs from 06 in the files.

**Palette** (his words "dark navy red and white"; the site's `--rep` is #c2433a / #e46c60 and `--dem` #2d62b8 / #5d90e6):
| pair | ratio | use |
|---|---|---|
| white on #0f1f3d | 16.4 | text on the ground |
| #b8c0d0 on #0f1f3d | 8.9 | muted |
| #d6243f on #0f1f3d | 3.26 | the dash and the sheet's edge (non-text AA ≥ 3) |
| white on #d6243f | 5.0 | the chosen segment's word (text AA ≥ 4.5) |
| #2d62b8 on #0f1f3d | ≈2.5 | fails: no party colour on the navy (24.2) |
Candidates tried: navies #0b1a33, #10213f, #14264a, #1b2a4a; reds #c8102e (2.7 on the navy, fails as a mark), #e03a4e (3.8, nearer `--rep`'s brick), #dc2626. #0f1f3d and #d6243f keep both pairs above the lines with the red furthest from `--rep`.

**Open for the maker's eye, not for me:** whether the stacked edges read as "little panes" at 390 where the strip is 48 px; whether the red beside `--rep` in the pinned rows reads as two reds (it should: crimson against brick; if not, the status loses its colour as 24.2 already says).

## 53. The reveal on build/site 0e0ac33: both schemes, and the inner scroller (2026-11-03 14:45 UTC; https://midterms-git-build-site-zachs-projects-74dd78e7.vercel.app/?fixtures; bundle `index-C0xi5deH.js`; shots `shots/c40-reveal-site-0e0ac33-*.png`, copies in `/mnt/project-files/design/`; scripts `rv9.js`, `rv10.js`) [measured: Playwright at 1×, both schemes emulated, ten pins, touch on the phone]

**s.51's pass holds on the site's own build:** every colour the token named in both schemes, the control's numbers (300 / 338 wide, 34 tall, three equal columns), the switch while open, ten pins reached and pressed at 1280 × 720 and 390 × 664; the dock gone and the logo in the header alone (one `.logo`, no `.dock` in the DOM).

**The inner scroller (the orchestrator's 14:43):**
- **Which scrolls:** `.page-content` (100dvh, `overflow-y: auto`); the document's scrollable height is 0 at both widths. So the browser's scroll-linked behaviours see no document scroll.
- **Position kept:** scrolled to 1016 on the phone, the drawer's open and close leave it at 1016, a drag on the clipped page while the drawer is open moves nothing (the cover takes it), the night pane's open and the browser's back leave it at 1016, a state tile's press (`/ak`) and back leave it at 1218 (the card over the page; W9's pages later must keep this, s.22). Desktop the same at 600.
- **Pull-to-refresh:** the scroller's `overscroll-behavior-y` is **`auto`**; on Chrome for Android a pull at the top of an inner scroller chains to the viewport and can start the reload gesture the maker named (11:33). **Set `contain` on `.page-content`** (spec 21.4, v1.14.1); the drawer and the panes already set `none` on the body while open. Not measurable here (no browser chrome in emulation).
- **The address bar:** with no document scroll, iOS Safari and Chrome for Android never collapse their bars, so the viewport stays at its smaller height for the whole visit [inferred from the platforms' behaviour, not measured]: a cost of the frame to weigh on the maker's phone, not a fault of the build.
- **Edge-swipe back:** the UA's own; untouched by the scroller (surface 29 still applies to the push).
- **The gutter at 1280:** Chromium's classic scrollbar takes 15 px inside the frame (`clientWidth` 1265 of 1280), so the header and page are 1265 wide and the toggle sits 24 px from the viewport's edge as on the probe; with overlay scrollbars (macOS, phones) there is no gutter. Harmless; nothing moved against s.44's numbers.

**Pass, with the one setting (`overscroll-behavior-y: contain`) for W9 before the PR, and the address-bar cost said to the orchestrator.**


**Addendum 14:54: build/site d54e12b** (bundle `index-BdKav1ja.js`): `.page-content` computes `overscroll-behavior-y: contain` at 390 × 664, the document's stays `auto` and the document never scrolls (0). The s.53 setting is in; the pass stands.

## 54. Check of W11's Reveal 2.0 on probe/reveal2 93ee9a9 against s.24 and s.23, both schemes (2026-11-03 15:02 UTC; https://midterms-git-probe-reveal2-zachs-projects-74dd78e7.vercel.app/?fixtures; bundle `index-C85TmDIf.js`; shots `shots/c41-reveal2-93ee9a9-{1280x720,390x664,360x640,312x531}-{light,dark}-{open,end}.png`, copies in `/mnt/project-files/design/`; script `rv11.js`) [measured: Playwright at 1×, `colorScheme` emulated, ten pins, touch on the phone sizes; 312 × 531 as 125% text]

**The palette (24.1), both schemes, every size:** the drawer's ground rgb(15,31,61) = `--rv2-navy`; the words white; eyebrows and the pinned statuses rgb(184,192,208) = `--rv2-muted`; the divider and the field's edge white at 0.22; the control's frame white at 0.22, its chosen segment rgb(214,36,63) = `--rv2-red` with a white 600 word, the others muted on no fill; the dash before the current view red, **the word white**; the front sheet red, the back sheet white, both `pointer-events: none`, z 3 and 2 under the page's 4; the cover black at 0.4. **The drawer is navy in both of the page's schemes** and pressing another segment while open changes the page and leaves the drawer (24.3). **The toggle:** closed, the ground's ink (`--fg` fill, `--bg` glyph; the light pill in dark); open, white with a navy ×.

**The geometry (24.4):** 1280: the page's card `inset(16 498 16 16)`, the red sheet `inset(32 482 32 16)`, the white `inset(48 466 48 16)`: the card, a 16 px red edge, a 16 px white edge, the 482 px drawer. Phone (390, 360, 312): card `inset(8 calc(100% − 56) 8 8)`, red `inset(16 calc(100% − 64) 16 8)`, white `inset(24 calc(100% − 72) 24 8)`: a 48 px strip of the card, 8 px of red, 8 px of white, the drawer at screen − 64 (326 / 296 / 248). The control 300 wide at 1280, the content's width on the phone (274 / 244 / 196), 34 tall.

**The order (his "organized well"):** desktop: Appearance, the four views with the current one marked, the divider, Pinned (ten rows with the status at the right); phone: the field, Appearance, the views, the divider, Pinned, Pause last with its 24 px. As s.21.1. The two sheets hold nothing: they are the stacked cards behind the page, a depth cue that fans out on open (s.24; said to the orchestrator 14:26).

**Reach (s.23):** ten pins, the last control (Pause on the phone, the tenth pin on the desktop) in view and pressable in every size and scheme.

**By eye at 1×:** at 1280 the card, the red edge and the white edge read as three stacked panes beside the navy drawer, the item's gesture in his colours; at 390 the 48 px strip of the page with the red and white edges reads as the stack seen from the side, which is the "little panes"; the control reads as a control; the red is a mark only and sits apart from `--rep`'s brick in the dimmed card (`c41-reveal2-93ee9a9-1280x720-light-open.png`); nothing touches, nothing twice. In the phone "end" shots a dash shows before the first pinned row: the touch emulation's hover left where the drag ended, not a state of the build.

**Pass on the design and the order.** For W8: the three clip-path layers move at once, with the sheets 35 and 70 ms behind the page. For the maker's phone: whether the 8 px edges read on his screen.


**Addendum 15:17: probe/reveal2 44cb445 (the hover guard, PR #10)** (`index-DPsAcnTB.css`; shot `shots/c42-reveal2-44cb445-390x664-light-afterdrag.png`) [measured: `rv12.js`, light, 390 × 664, ten pins, a touch drag ending over a pinned row]: after the drag only "Country", the current view, carries the dash; no row matches `:hover`; the hover rules sit under `@media (hover: hover)`. The sticky dash of s.54's note is gone on a touch screen. Pass stands.

## 55. The maker's 15:21 on Reveal 2.0: the logo's room and the left gutter, before and after (2026-11-03 15:25 UTC; probe/reveal2 44cb445; his photo `shots/maker/2026-11-03-15-22-reveal2-left-edge.jpeg`; script `rv13.js`; DESIGN-SPEC v1.14.2, 24.7) [measured: Playwright at 1×]

**Before (44cb445):**
| | 1280 × 720 | 390 × 664 |
|---|---|---|
| header's logo, closed | left 41 (header padding 28 + the tile's own) | 16 |
| page-shift open | −100 on `.page-content` | −40 |
| card's left clip | 16 | 8 |
| logo open | −59 (cut by 75 px) | −24 (cut by 32) |
| drawer left / width | 798 / 482 | 64 / 326 |
| white sheet's right edge | 814 (16 px over the drawer) | 72 (8 over) |
| drawer content padding (T R B L) | 96 / 40 / 48 / 24 | (the phone's) 88 / 32 / 232 / 36 as the item |
| first words' left | 822 = **8 px from the white edge** | 84 = **12 px** |
| the current view's dash | at 822, on the edge; its word shifted 50 px | the same at 38 px type |

**His photo, by eye:** the desktop at the drawer's left edge: the words begin a few px from the white strip, "Country" indented by its mark while Senate, House, Governors and the pinned rows are not; the dash lies on the strip. The emulator's shots showed it (s.54's 1280 light open) and I passed it: a gap of 8 px beside a 16 px white band is the thing to see at 1×, and I saw the stack and not the gutter. Stated as my miss.

**After (24.7):** the header unshifted (logo 25 px from the card's border at 1280, 8 on the phone's sliver, closed unchanged); the content padding-left 96 at 1280 and 56 on the phone, so the column starts 80 / 48 px from the white edge, shared by the field, the control, the views, the divider, the pinned rows and Pause; the dash in the gutter, 38 px (0.8 em) ending 12 px before the word at 1280 and 19 px (0.5 em) ending 8 px before it on the phone; no word shifts, on current or on hover. The column: 346 px at 1280, 238 at 390. For W11; checked against these numbers and his photo's view when his note comes.

**Addendum 15:33: probe/reveal2 4cc3d37 checked against 24.7 and his photo** (CSS `index-BaenngIC.css`; shots `shots/c43-reveal2-4cc3d37-{1280x720,390x664}-open.png`, copies in `/mnt/project-files/design/`; script `rv14.js`) [measured: Playwright at 1×, ten pins]:
| | 1280 × 720 | 390 × 664 |
|---|---|---|
| header shift / main shift, open | 0 / −100 | 0 / −40 |
| logo open (room from the card's border) | 41 (25) | 16 (8) |
| content padding L / R | 96 / 40 | 56 / 32 |
| the column (field, control, eyebrow, views, divider, pins, Pause) | all at 894 = 80 from the white edge (814) | all at 120 = 48 from the white edge (72) |
| the dash | 38 wide, left at 844 (30 from the white edge), 12 before the word | 19 wide, 8 before the word |
| the current word | 894, on the column (no shift) | 120 |
**By eye at 1× against his photo:** at 1280 the logo stands whole with the card's inset beside it; the words stand on one edge 80 px from the white band with the red dash in the gutter before "Country"; nothing staggers; the preview banner's text is cut at the card's left ("ated figures, not results."), the body's put-away as before, the preview's banner only. At 390 the column is 48 px from the white edge, the dash in the gutter; the field's placeholder is cut at "candic" in the 238 px column: the spec now gives the phone "Search a state or race" under 600 (v1.14.3, 21.1 item 1). **Pass on 24.7; one word for W11 (the placeholder).**

**Addendum (15:41 UTC, c757860 on probe/reveal2, bundle index-DKr3WKDX.js) [measured].** The drawer's field: placeholder "Search a state or race" at 390 (field 238 wide), 360 (208) and 760 (256), none cut (scrollWidth ≤ clientWidth). At 1280 the drawer has no field; the header's Search button opens the palette, whose field is 534 wide and says "Search a state, race or candidate", not cut. W11's wider rule (under 900, wherever the drawer has the field) is in the spec as v1.14.4. Reveal 2.0 on probe/reveal2 passes every line I have measured; what remains is W8's measure of the three clip layers.

## 56. The phone's time indicator and the skeletons: what I measured before writing s.25 and s.26 (15:45 UTC; the maker, 15:39)

**The accent [measured, 390×664, build/site and probe/reveal2, the same on both].** `button.next.nextbtn`: 89 × 28 at left 169 top 14, `border-left: 1px solid rgb(227,225,220)` (`--line`), radius 6, padding 2 / 4, ground transparent; children "11 PM" (12 px, 34 wide), "19:59" (15 px, 40 wide); the pill at left 274, 100 × 44; 16 px between them; the logo's right at 116. The line he photographed is that border-left: the phone media query's `.next { border: 0 }` loses to the button's own selector [source: styles.css]. Shots `ph-header-site.png`, `ph-header-reveal2.png` in scratch (the header's first 64 px; not kept in the repo since s.25 names the numbers).

**A fault beside it [source: Header.jsx].** Paused, more-than-12-hours and all-closed states render `div.next`, not the button, so on the phone the night card has no way in while the viewer has pressed Pause or before 4 PM ET on the day. s.25 makes every state the button.

**12.2's old rule.** "No skeleton animation anywhere" was decided among the cases, not by a ruling; his 15:39 word governs, and 12.2 now points to s.26. The skeleton's colour is `--track`, the bar's empty track, so the site's "nothing yet" is one colour wherever it appears.

## 57. The pushed pages and the two buttons on build/site 17acf9d (bundle index-BRJHCucO.js), s.23's cases (16:45 UTC) [measured]

**Cases:** 390×844 (six default pins, and ten), 390×664 light and dark, 360×640 light and dark, 312×531 (125% text), ten pins, the fixtures night; Playwright 1×, touch, `pg2.js`/`pg3.js` in scratch; shots `c45-17acf9d-*.png`.

**Passes.** The state page: "‹ Country" 12 muted at (16, 107), the h1 at 130, the header sticky at 57, the pill at (274, 6) 100×44 at every width, the page's scroller is `.page-content` (the document never scrolls), no "By county", history state `{y, site, from:"/"}`; the last control (a 185 px measure row) reached in view at every height; the section's "Show all 2" pressed gives 13 rows. The race page (/ga/senate): "‹ Georgia", the Pin 55×25 → "Pinned" 75×25 and back. Back by the title row: race → state → country, the country's scroll restored to the tile's place (1325 to 1951). The night card over a state page: the pane at half (422 at 844, 332 at 664, 320 at 640), the pill above it at (274, 6), opacity 1, `elementFromPoint` the pill; a press on the pill closes the pane and opens the drawer in the one press. No page errors. **The time button:** running 102×36 at (156, 10), 1 px `--line-strong` on four sides, 6 px, `--bg`, padding 0 10, 16 px to the pill, centred on the pill's row, both schemes. **The drawer's Pause:** 75×44, 1 px rgba(255,255,255,.22), 6 px, no ground, white 15 px, padding 0 16, 24 px above; pressed → "Resume", ground rgba(255,255,255,.12); the night card opens from the paused button (the night pane at 422 / 320; the header's button `aria-expanded` true and ground `--panel`).

**Faults.** (1) **"Show all 2" is drawn as a second menu pill** at (274, 63) 100×44, absolute, ground `--fg`, over the preview banner (57–89), at every case: the item's `.navigation-07 .toggle` rules (styles.css 761–767) catch the site's `button.toggle` ("Show all N", Pinned.jsx 66 and State.jsx 165) inside the scope. Fix: the item's selectors to `.navigation-07 > .toggle` or `[data-toggle]`. Shot `390x664-dark-10pins-state-top`. (2) **The paused time button is 147 wide** ("Polls close at 11 PM ET"): 1 px from the pill at 390, **29 px under it at 360**, and the pill's centre then hits the button's span; at 312 the running state is already 32 under the pill and the paused 77 (the pill cannot be tapped: my script's tap timed out there). Spec v1.16.1 (25.1a): every state's label no wider than the running one, padding 0 8; under 350 px the tile alone. Shot `360x640-light-10pins-country-paused-top`. (3) **The race page's title row doubles its back**: "‹ Georgia" over the h1 "Georgia · Polls close 7 PM ET", then the race block's h2; s.22.2 has the title row with the Pin and then the race block, so the state's page-head goes on the race page and the race's heading is the h1 (R6). Shot `390x664-dark-10pins-race-top`. (4) **The drawer's Pause at 844 with the six default pins is cut 10 px by the screen's bottom** (810–854; the drawer scrolls 58 px, after which it stands at 752–796 with 48 below and is pressed); with ten pins at 844 it is 160 below, at 664 340, at 640 491, at 312×531 728, each reached by the drawer's scroll with 48 below. By 21.1 this passes (reached and pressed at every height); the cut button on the first screen at his phone's height with the defaults is for his eye. If he wants the first screen whole at 844: the top 88 → 64, the bottom 48 → 24, the two 24 px gaps (above "Pinned" and above Pause) → 16 give 6 px to spare [computed]. Shot `390x844-light-defpins-drawer-bottom`.

**Not measured:** the more-than-12-hours and all-closed states (the fixtures do not reach them; 25.1a gives their labels); the push's motion (W8's); a real phone.

**Addendum (16:54 UTC): the two unmeasured states, on build/buttons eedbfff built locally (`vite build`, `vite preview` at 4173; `bt1.js`; `?fixtures&now=2026-11-02T18:00:00Z` for the first closing, `&now=2026-11-04T12:00:00Z` for all closed) [measured].** The frame is as on 17acf9d in every state (four 1 px sides, 6 px, `--bg`, 36 tall, centred on the pill's row, both schemes). **More than 12 hours away:** the label "First polls close Tue 4 AM ET" at 11 px wraps inside the button: two lines at 390 (132 wide, 16 to the pill), three at 360 (102 wide), and at 312 five lines ("polls / close / Tue / 4 AM") spilling above and below the 36 px frame (54 wide): the old `.lab.first` rule (`white-space: normal`) meets a button that hugs. **All closed:** "All polls closed" 103 wide: 16 to the pill at 390, 15 at 360, 33 under it at 312. **Paused:** 147 wide as on 17acf9d (1 at 390, -29 at 360, -77 at 312). The night card opens from the button in every state where the pill does not cover it (the night pane at 332 / 320 / 265). 25.1a's labels ("Tue 4 AM" + "14 h"; "All closed"; "11 PM · Paused"; padding 0 8; the tile alone under 350) answer all three, with `white-space: nowrap` on every label inside the button. Shots `c46-eedbfff-390-light-first`, `-312-light-first`, `-360-light-closed`, `-360-light-paused`.

## 58. The two buttons on build/buttons ea00408 (W11), built locally and rechecked (17:08 UTC) [measured]

`vite build` of ea00408 served by `vite preview` at 4173; `bt1.js` (the time button, `?fixtures&now=` for the first-closing and all-closed states) and `bt2.js` (the drawer); 1x, touch; shots `c47-ea00408-*`.

**The time button, every state, 390 / 360 / 312, light and dark:** 36 tall, four 1 px `--line-strong` sides, 6 px corners, `--bg`, padding 0 8, centred on the pill's row, **16 px to the pill in every state at every width**; the night card opens from it in every state (the night pane at 332 / 320 / 265). Widths: running "11 PM | 19:59" 98; paused "11 PM | Paused" 98 (both 12 muted); first closing "Tue 4 AM | 15h" 96; all closed "All closed" 70. At 312 the logo is the tile alone (22 wide). **Pass.** One word: the hours read "15h" where the site's reduced countdown says "1 h 19 min" with the space (Header.jsx `countdown`); W11 chose "15h" (96) over "15 h" (99.6) to stay under my "no wider than the running state" (98), which was the wrong measure: the rule's point is the 16 px to the pill, which "15 h" keeps at 360 (room 102). So "15 h", one form (R6); 25.1a amended to say the measure is the 16 px.

**The drawer's Pause:** 75x44, 1 px rgba(255,255,255,.22), 6 px, no ground, 15 px, padding 0 16, 24 above; pressed → "Resume" on rgba(255,255,255,.12); the content's padding 64 / 24, the field at 64. **390x844 with the six default pins: whole without a scroll, 778-822, 22 px above the screen's bottom** (the drawer can still scroll 2 px: the content is 846 tall against 844, so a pull bounces 2 px; the bottom padding at 22, or one gap at 14, ends that). With ten pins: 844 → cut 128 then by the scroll at 776-820; 664 → 308, then 596-640; 640 → 459, then 572-616; 312x531 → 696, then 463-507; each with 24 below and pressed. **Pass by 21.1 and by the maker's 12:50 at his phone's height.**

**Addendum (17:16 UTC): build/buttons c8a1ad9 (W11's two lines), built locally after `npm ci` and rerun with the same scripts [measured].** The time button: as on ea00408 in every state, width and scheme (98 / 98 / 70; 16 px to the pill at 390, 360 and 312; the night card opens from each); the first closing now reads "Tue 4 AM | 15 h", 100 wide, 16 to the pill at all three widths. The drawer: padding 64 / 22; at 390x844 with the six default pins the content is exactly the screen (scrollHeight = clientHeight, no scroll, no bounce) and Pause stands whole at 778-822, 22 above the bottom edge; with ten pins reached by the scroll with 22 below at 844, 664, 640 and 312x531, pressed to "Resume" each time. **Pass; nothing left on the branch for the merge.**

**Addendum (18:26 UTC): build/site 8bc093f (bundle index-DmcstSwM.js), faults (1) and (3) of s.57 [measured at 390x664 light and 360x640 dark, `pg4.js`].** (1) "Show all 2" is the page's own control again: static, 55x17, underlined, no ground, at the House section's foot (top 2230 / 2291); the menu's pill rule now reaches `.navigation-07 > .toggle` alone (one match). (3) The race page: "‹ Georgia" above the h1 "U.S. Senate" (left 16, top 142), no state page-head, then "Georgia's other races". **Both pass.** The called pinned card (W9's 18:09 fix, his shots) is written into 13.1 as built, with one candidate for the maker's "be deliberate" (the rule as the card's own edge); shots `c49-8bc093f-*`. The pages' push (W8's rule-12 fault) is not in this measure.

## 59. The Pinned shelf on build/site 8bc093f (bundle index-DmcstSwM.js) at s.23's case, and fault 2 there (18:45 UTC) [measured]

`pg5.js`: 390x664 and 360x640, light and dark, ten pins (the six defaults plus Georgia, North Carolina, Maine and Alaska Senate), "Show all 10" pressed, the fixtures night at the real clock (Georgia called with a changed call; New York uncalled at 6 percent in; House 17 with no votes; Alaska with no candidates yet, an incumbent line only). Shots `c50-8bc093f-shelf-390-light`, `-shelf-360-dark`, `-called-390-light@2x`, `-called-390-dark@2x`.

**Positioning.** Every card 358 wide at 390 (16 to 374) and 328 at 360, 111 tall (89 for Alaska's one line), 1 px `--line`, 8 px corners, the page's ground. In every card the title, both names and the status's edge stand on the same two edges: text left at 29 (13 inside the card), shares' right at 361 (13 inside), at 360 29 and 331; the called card's loser and title on the same edges; no name or title cut (scrollWidth = clientWidth on all), "N.Y. · County Legislator 4" one line; the uppercase "CAMPOBASSO / GASHI" and the party-less "Dublin / Cooper" align the same. **The names' fault he named is gone.**

**The called card (Georgia).** The 3 px rule in the party colour (`--dem`, light 45,98,184 / dark 93,144,230) 1 px inside the card's left edge, 12 px below the card's top and 14 above its bottom, which is the text block's span (the title's line top to the status's line bottom), as the row's rule spans its row; the check, "Ossoff (D)" and "61.8%" in the party colour at 600; "Collins (R)" and "38.2%" unchanged; the last line "Call changed" in warn (12.4; in W9's shot of the earlier night, "Called by 10:40 PM" in the party colour). Both schemes the same. No fill, no box.

**"Deliberate", as a design.** The card reads as one with the list row: every part is the row's (s.7, 12.4) at the card's edges, and nothing is a leftover of the stacked grid. **One part is inherited rather than chosen: the winner's name is indented by the check** (the check at the column, the name 32 px after it), so it is the one name in the shelf off the column, while the loser's name and the title stand on it. The list rows do the same everywhere on the site, so the card is consistent; but his words were "the positioning of names is really off, particularly when there is a called winner", and after the 115 px push is gone, this indent is what "particularly when there is a called winner" still describes. If his eye says so, the fix is the idiom's, rows and cards alike: **the check goes before the share** ("Ossoff (D) … ✓ 61.8%"), so every name stands on one edge and the mark sits beside the figure that decided; the rule stays. Not built; for his word.

**Fault 2 on build/site: does not stand.** The header's paused button is 98 wide with 16 px to the pill at 390 and 360 (the buttons are in this bundle). Faults 1 and 3: pass (s.57 addendum).

**Addendum (19:08 UTC): build/site 3ae4e69 (bundle index-C3Ts8uDg.js), the check before the share [measured, `pg6.js` and a row script, 390x664 light and 360x640 dark, ten pins].** The shelf's cards: every name at 29 (the called winner's too), every share's right edge at 361 (390) / 331 (360); in the called card the check (14 px) sits at 298-312, 4 px before "61.8%", the name and share in the party colour at 600. The governors list (thirty rows, eleven called): the candidates' column at 130 in every row, the shares' right edge at 374 / 344 in every row, the check at 305-319 (275-289) 4 px before the share, each share on one line (the phone's share column `auto` with nowrap, as W9 said), rows 64 or 60 tall as before. **Pass:** the inherited part named in s.59 is gone; every name stands on one edge, called or not. Shots `c51-3ae4e69-govrows2-390-light`, `-govrows2-360-dark`, `-shelf-390-light`.

## 60. The skeletons (s.26) on build/site de548cb, W9's f1b1a09, checked on the preview (19:18 UTC) [measured]

`pg7.js` and `pg8.js`: 390x664 light and dark and 1280x720 light; the data slowed by a Playwright route (1.8 s on `/data/`, and on `/api/national` + the fixtures chunk for the country), then fast loads with no route, polled every 40 ms for `.sk`. W9's shots read first (research/build/shots/2026-11-03-skeletons). Shots `c52-skel-*`.

**The mechanism, pass.** Blocks at `--track` (234,232,227 light / 38,40,44 dark), 3 px corners, no edge, `aria-hidden`, 11 px for 15 px text and 9 for 12, the seat bars' figures 56x23; the region `aria-busy` while waiting and not after; on arrival every block gone and busy off; the fast loads showed no block at 390 light and 1280 (0 sightings over 7 s of polling across the country, a state, a race and the drawer); at 390 dark one run showed a page's blocks for a poll or two (49 sightings), which is a fetch over 150 ms on the network that run, allowed by 26.1, not a flash the build makes.

**The places.** (1) Country: 9 blocks on the phone (the three seat bars' figure and count places), 15 on the desktop with the calls' three rows; the tiles I did not single out. (2) State: 32 blocks (two sections of four rows); the first block at 204 and the first arrived candidate line at 203, so the top does not move; but the page's first things are the statewide race blocks and the skeleton's are rows, and at 1280 the rows stood under the map (649) while the content landed in the cards' column beside it (204): spec 26.2 item 2 amended (race blocks first, the desktop's column holds two block shapes). (3) Race: 4 blocks (two candidate lines) at 189; the route's heading as an aria-hidden h1 at 142 before and after, which becomes the real h1 on arrival without moving; the blocks gone at 3.7 s (three files in sequence). (4) Pins: W9's shot shows the drawer's two block rows per waiting key; in my runs the ten pinned races arrived with the fixtures before the drawer opened (0 blocks, 10 rows at 388 ms), so the shape is read from the source (PinRows, n = the keys still on their way) and his shot, not re-measured; a key that can never arrive (`ZZ|Nothing|1`) produced no block and no wait: ten rows, none busy, at 7 s. (5) Search: 5 rows of two blocks under the field, 8 results after; in the navy drawer the block is white at .10 (W9's choice; the spec now says .12, the drawer's one tint). (6) Night card's calls: not re-measured (the desktop's calls column showed its three rows).

**The case that does not fit.** The bundle's data holds no one-candidate race and no one-section state [measured over `dist/data/*.json`], so those two cases do not arise this year; a never-arriving key is above. **Verdict: pass on the mechanism and five of six places; one correction, item 2's shapes (and W9's own question answered: yes, two block shapes in the cards' column); one tint line.** Neither needs to hold the merge.

## 61. The first-pass review (the maker's 19:31; `research/reviews/2026-11-03-W15-review-package/returned/pass1/`): verdicts and the checks of the fixes on build/review (19:36 UTC)

**F-006 (the state page's race blocks have no Pin in their heading line; the race page's block has one) [the reviewer, seen live at 1363x936; confirmed in the source: RaceCard renders the heading's Pin only when `full`].** Verdict: the design is the Pin on the state page's blocks too. 13.1's "Pinning elsewhere" named the race's view and card and the list rows, and its empty-state words "Pin any race from its row or its page" assumed the block was covered; the block on the state page is the race page's own block (8.2, 13.2) with the same heading line, and the statewide races are the state page's first things, so without it they are the one kind of race that cannot be pinned where it is read (law 10). Spec v1.16.6 says so; a build gap, not a choice. W11 builds after tonight.

The other seven (F-001 title, F-002 internal notes, F-003 House winner colour, F-004 House call hides reporting, F-005 territory name cut, F-007 pin target, F-008 House office repeated) are W11's and W14's fixes on build/review; each is checked here as named, at 1280 and 390 in both schemes with s.23's case.

**F-001 on build/review 5d8e23d (W14), 19:55 UTC, local build (no Vercel preview for the branch; `vite build` + `vite preview`), 390x664 and 1280x720 [measured].** The tab's title on each route kind: "/" "Midterms 2026 results"; "/senate" "U.S. Senate · Midterms 2026 results"; "/governors" "Governors · …"; "/house" "U.S. House · …"; "/ny" "New York · …"; "/ny/governor" "New York · Governor · Midterms 2026 results"; "/ny/house-17" "New York · U.S. House, District 17 · …"; "/zz" "Page not found · Midterms 2026". The click from /ny to its governor sets the race's title; back restores the state's; forward the race's again; no page errors. The scheme does not enter (a title has no colour), so one run per width. The og:title cannot be checked on the local preview (the per-route shells are Vercel's rewrites; the SPA's index answers every address here), so the title's agreement with the preview rests on the one formatter in the source (`src/lib/pagetitle.js`, read) and W14's test. **Verdict: pass; the finding is cured.** One observation outside F-001: a wrong race address under a state ("/ny/nothing") shows the state's first race (the governor's) with the crumb and no heading, and its tab says "New York · Midterms 2026 results"; the page and the tab disagree there because the named race never resolves. Not of this fix; a line for W9 after tonight.

**W9's cure of that observation, build/site c59a22c (6f9446a), on the preview (bundle index-CKvhEoJA.js), 390 and 1280 [measured, 20:15 UTC]:** /ny/nothing shows "‹ New York" and "New York has no race at /ny/nothing." in muted, no race drawn, no skeleton left, the tab "New York · Midterms 2026". **Pass.** 5b81963 (the seat bars' second reveal off) on the same preview: no animation runs on the seat-bar region at 600 ms or at 3 s, the bars stand at their widths at opacity 1, the figures as the fixtures give them; nothing visible to flag.

**F-002, F-003, F-004, F-005, F-008 on build/review 35afcb6 (W11, one commit each), 20:15 UTC, local build, at 390x664, 360x640, 312x531 (125% text's case) and 1280x720, light and dark [measured].** F-002 (35afcb6): no "law 10", "Chappaqua", "for now" or "per-seat rows" text on /ny/ny-state-senate-district-40 or /ny/governor, and none in any file under dist/ (grep). Pass. F-003 (b8479e8): the House table's called row at 1280 shows the leader "B (R)" and the share "51.2%" in `--rep` (rgb(194,67,58) light, rgb(228,108,96) dark) at 600; the next candidate muted at 400. Pass. F-004 (588ba13): the House table's heads read Seat, Leading, Share, Next, Status; the Status cell reads "58% in" (R8's phrase), "No votes yet", "Called by 9:22 PM"; the table 732 in 732 at 1280, no overflow. Pass at 1280. F-005 (2944697): "Northern Mariana Islands" whole in the governors list, two lines in the 150 px column at 1280 (row 85), three lines in the 104 px column at 390 (row 106). Pass. F-008 (e1c78b7): the state's House cards at 1280 headed "District 1", "District 2", …; on the phone the House is the table, not cards. Pass.

**F-007, my word (spec v1.16.8, 13.1):** the Pin measures 75.5 x 24.8 at 390, 360 and 312, no pseudo-elements. The frame stays; on `hover: none` a `::before` of `inset: -10px 0` gives a 45 px hit region the frame's width, overlapping nothing (the rule above, the candidates below). Not an accuracy fix, so whether it rides before the freeze is the orchestrator's.

**W11's two faults, confirmed on 35afcb6 [measured]:** (1) the phone's House table on /ny is 384 px wide in a column of 358 at 390 (328 at 360, 280 at 312): the status cell ("No votes ye…") is cut at the page's edge and a called row's name wraps to two lines; spec v1.16.8 writes the table within its column (fixed layout, the status cell at `--t-src` nowrap with an ellipsis, as the list row's status). (2) On the desktop's governors and Senate lists a called row's share cell is 42 px tall: the check sits on a line above "54.0%" / "61.8%" in the 64 px column (the phone's `auto` column, 69 px, holds both on one line); spec v1.16.8 makes the column `auto` on both widths. Both are layout faults on main, not accuracy; the orchestrator decides whether they merge tonight.

**build/review cbb4e50 (W11's 7675b80 and cbb4e50), 20:19 UTC, local build [measured].** 7675b80, the phone's House table: on /ny and /az the table is 358 in 358 at 390 and 328 in 328 at 360, no cell past the page's edge, "No votes yet" whole (one line at 390, 36 px; two lines on /ny at 360, 57 px, since the cell wraps rather than cuts). **Pass at 390 and 360.** At 312 (s.23's case, 125% text) the table is still wider than its column: 313 in 280 on /ny (26 cells past the edge), 298 in 280 on /az (9); the pre-results cell was the first cause, the columns' own content widths are the rest. The spec's line (v1.16.8: fixed layout, the status cell at `--t-src` nowrap with an ellipsis) is the cure for that width; a layout fault, so the orchestrator's call tonight. cbb4e50, the notes: /ny, /ny/governor and /ny/ny-state-senate-district-40 carry no research mark, no "law N", no "for now"; the reader's notes stand ("civicAPI, as of 10:36 PM ET · names: official list"). **Pass.**

**build/morning cf27ae2 (W11's three cures of 20:19, for the morning's PR), 20:35 UTC, local build, at 390x664, 360x640, 312x531 and 1280x720, light and dark [measured].** (1) 4d73365, the state's House table: fixed layout; 358 in 358 at 390, 328 in 328 at 360, 280 in 280 at 312 on /ny and /az; no cell past the page's edge, no cell clipped; "Called by 10:07 PM", "58% in" and "No votes yet" whole at every width; rows 36 px, or 57 and 78 where a name wraps at 312. **Pass.** (2) cf27ae2, the share column `auto`: 69 px on both widths, every share cell one line (a Range's client rects: one line each, the tall cells are the place's wrapping, "Northern Mariana Islands" three lines at 390 and two at 1280, "New Hampshire" two at 390), the right edge one value per width (673 at 1280, as before; 374 at 390), the names' left edge one value (207 at 1280, 130 at 390). **Pass.** (3) e864127, F-007: under `hover: none` the button is `position: relative` with a `::before` of `inset: -10px 0`; a tap 9 px above the frame and 9 px below each pins or unpins, at 390 and 312 (aria-pressed toggled each time); on the desktop (`hover: hover`) no pseudo-element, the frame alone. **Pass, with one line for the morning:** the candidates' first row (`.crow`, `position: relative`, later in the DOM) begins 8.5 px under the frame and paints over the region's last 1.5 px (`elementFromPoint` at 9 px below answers the row, at 8 the button), so the region as painted is 43.3 px, not 45; `z-index: 1` on the button under the same media query lifts the region above the row and nothing else changes. The only other controls within 10 px are the drawer's three 1 x 1 visually hidden radios at y 170, which no finger reaches.

**Addendum, 20:39 UTC, build/morning 01602b6 (W11):** `z-index: 1` added; W11 measured every half pixel through the button's centre at 312, 360 and 390 with no miss inside the region [W11, stated]. W11's number: the region is 42.8 px (134.7 to 177.5 around the 143.7 to 168.5 frame), because `inset` is measured from the padding box, inside the 1 px border, so -10 reaches 9 px beyond the frame each side. My word: `inset: -11px 0`, 44.8 px, since the review's floor is 44 and 42.8 is under it (spec v1.16.9, 13.1). My own 20:35 line ("43.3, the row paints over 1.5 px") had the cause half right: the row covered the region's last part, and the region itself was 2.2 px shorter than I wrote. **build/morning f213f3f, 20:45 UTC, local build at 390 and 312 [measured]:** `inset: -11px`, `z-index: 1`; the region answered by `elementFromPoint` through the button's centre runs 133.2 to 178.0 around the 143.7 to 168.5 frame, 44.8 px, and a tap half a pixel inside each end pins or unpins. **Pass; F-007 is cured on the morning's tip.**

## 62. The check of build/site c14b145 (W9's four commits on the skeletons and the back), on the deployed preview, bundle index-LuXCnssy.js (19:48 UTC)

Measured at 390x664 and 1280x720, light and dark, deviceScaleFactor 1, with `/data/` slowed by a route; the hold with a MutationObserver on `main .sk` (the time a block is first added to the time the last is removed, by `performance.now()`); the back with ten pins at 390 light against the de548cb baseline shots c52-back-baseline-{120,400,1400}. Shots c53-c14b145-*.

**afa0ffa, the 250 ms hold.** Held 292, 255, 263 and 521 ms at route delays of 60, 140, 220 and 400 ms [measured]; with every delay the state page's wait passes 150 ms (its files load in turn, through the proxy), so the blocks showed every time, and in no case were they taken down under 250 ms. The arrived cards come in under `reveal`. **Pass.**

**293166a, the state skeleton's shapes.** At 390: the office block 160x11 at y 172 at the left gutter 16, over two candidate rows of 140x11 and 28x11, twice (the two statewide races), then four House rows (120x11 name, 160x11 office, 28x11 share) under a rule; the arrived first card's top is 174 and its first name's line at 212 [measured]; the swap moves nothing the eye would catch. At 1280: the two block shapes stand in the cards' column (x 645, 580 wide) beside the map (x 41, 580 wide), the House rows below the map, as 26.2 item 2 (v1.16.5) has it. Ground `--track` in both schemes (rgb(234,232,227) light, rgb(38,40,44) dark). The drawer's block in the Reveal 2.0 menu is white at .12 (ten blocks on a slowed search). **Pass.**

**f5120b6, the sweep.** A `::after` on each host (`.sk-rows`, `.sk-cand`, the others), `sk-sweep` 1.4 s linear infinite, the band `color-mix(--bg 50%, transparent)` at the gradient's middle, three hosts animated on the state page; under reduced motion no host animates and the 26 blocks stand still [measured]. **Pass on the mechanism.** On the band's colour in dark [computed, CIE L* of the band blended over `--track`]: light lifts the track from L* 92.0 to 95.1 (+3.1), a highlight; dark takes it from 16.1 to 11.1 (-4.9), a shadow crossing the block, the opposite of the idiom (a sheen is a lightening). White at 4% over the dark track gives +4.1 (to #2f3135), the nearest lift to the light scheme's; 5% gives +5.1, 6% +6.0. My candidate, written into 26.1 (v1.16.7): in dark the band is white at .04, light keeps `--bg` at .5. W8's surface, so W8 measures it; the colour alone is mine. Not a reason to hold the merge: the dark band is faint either way (a 5 L* dip), and the blocks' timing and shapes are right.

**64797d0, the country's return.** During the back slide the map's Senate / Governors switch is drawn still (`.seg-still`, `aria-busy`) from about 140 ms into the motion until it settles, then the Base UI component mounts in its place; the shelf's cards mount five a frame (0, 5, 10 across three frames of 60 ms) [measured]. The settled country page after the back against a fresh load at the same scroll: 0 px differ of 236,730 (the viewport below the header, 390x607); against the de548cb baseline frames: 0 px differ at 400 and 1400 ms, and the 120 ms frame differs only in the slide's position (c14b145's a few px further along; the switch is drawn in both). The pinned tile tapped (GA) stands at the viewport's centre again after the back, as before it. **Pass: nothing visible changes on the back.**

**Verdict to the orchestrator and W9: the four commits pass; the one line that follows (the dark band) is a candidate for W8, not a hold.**

**Addendum, 21:50 UTC: the sweep on build/site bed175f (W9's --sk-band, white at .04 in dark) FAILS, and my pass above was read from computed styles, not pixels.** On the deployed preview (bundle index-DE4H-QQP.js), 390 and 1280, dark and light, with `/data/` held and the sweep paused by the Web Animations API at the moment the band's centre crosses the first candidate block [measured, full-frame screenshot pixels, luminance of 255]: dark, the ground between the blocks 19 to 28 (+9 at the peak, 21 and 28 on the way), the block 40 at every moment; light, the block 232 and the ground 250 at every moment. The cause: the name block sits in `span.nm` with `position: relative; z-index: 1`, and the host's `::after` is `z-index: auto`, so the band passes beneath the blocks and lights only the ground; with the band painted red (`--sk-band: rgba(255,0,0,.9)`) the blocks stand as dark holes in it (shot c59-band-red.png). In light `--bg` over `--bg` is invisible, so light has had no sheen at all; in dark the old band (`--bg` at .5) darkened the gaps and the new one lightens them, never the blocks. The office line's block (160 x 11, above the candidate rows) lies outside every host and is never swept. My s.62 line "pass on the mechanism" rested on the animation's presence and the gradient's colour in the computed style; the pixel was not read. Spec v1.17.3 (26.1): the band paints above every block (`z-index` above the name span's 1) and every block stands in a host; the check is the block's own pixel, about +9 in both schemes. Cure named to W9 (CSS alone: `z-index: 2` on the seven `::after` rules; a host for the office block); the measure to W8. **W8's per-block read, 22:01 [W8, stated]:** the list rows' blocks (`.row .st`, no z-index) do lift under the band (dark 40 to 48, light 232 to 241); the race blocks do not (the office block has no host; the candidate blocks sit in `.nm` and `.pc`, whose spans paint above the band). On bed175f the state page's 26 blocks: 16 lift, 10 flat, both schemes; a race page 4 of 4 flat. So the fault is the race block's, on the state and race pages, and the lists' skeletons were right; MOTION-SPEC v1.8.56 makes row 41's check per block (21:53).

**Addendum 2 (22:11 UTC): W9's cure on build/site 356e738 (tip 7ea8b1d, bundle index-ZYQQxkxB.js) PASSES [measured].** Method: the preview with `/data/` held 25 s, the skeleton on the page, every `.sk` block on the first screen enumerated with its host, the sweep paused at twenty equal times across its 1.4 s and a full-frame screenshot at each, the block's own centre pixel read at every time; the block's base is its lowest reading and its peak the highest. Georgia's state page and its Senate race, 390 × 664 and 1280 × 720, dark and light: **104 blocks, 0 flat**. Dark: base 40, peak 46 to 48 (+6 to +8; the office blocks and the candidate names and shares in the cards' host alike, and the rows' blocks). Light: base 232, peak 239 to 242 (+7 to +10). The candidate blocks (`.nm`, `.pc`) that were flat on bed175f now lift with the rest; the office block has its host (`.sk-card`). One note, not a fault, for W8: in dark the band also lifts the host's own ground between the blocks, 19 to 26–28 (+7 to +9, read 3 px under each block), where in light the same ground moves 249 to 250; so in dark the sheen reads as a band across the host, blocks and ground, not on the blocks alone. 26.1 does not say which; if the blocks alone are wanted, the band is clipped to them (a mask of the blocks on the host's pseudo-element, or the band drawn on each block) and that is W8's and W9's to weigh against the cost.

## 63. The breadcrumb's measures, for s.28 (20:56 UTC; the maker, 20:52)

On production e466d51 at 390 (bundle index-CMylOwnb.js) [measured]: the back crumb "‹ Georgia" on /ga/governor is a 12 px `--muted` link (rgb(91,96,104)) at x 16, y 75, 48 x 15, in a `.crumbs` box with 18 px of padding-top under the 57 px header; the h1 "Governor" at y 110. Widths at 12 px in the site's Plex, by canvas `measureText` with the link's computed font: "Home" 32.3; "Home › New York › " 101.9; "Home › Northern Mariana Islands › " 188.2; "Home › Georgia › Governor" 142.1; "U.S. House, District 17" 120.4; "District 17" 55.9; "NY State Senate, District 40" 148.9; "Westchester County Legislator, District 4" 217.5; "NY Supreme Court Justice, 9th Judicial District (vote for three)" 334.3; "Attorney General" 91.6; " › " 9.3. At 15 px the two long chains are 313.5 and 295.2, which is why the chain keeps the back's 12 px and not the body's 15: at 360 the body size would cut the Westchester chain and at 312 every local race. Contrast [computed, WCAG]: `--muted` on `--bg` 6.1:1 light and 7.6:1 dark; `--faint` 3.4:1 light and 4.1:1 dark, enough for a separator glyph that carries no word.

The choices in s.28 that are mine, not the maker's, each with its reason there: "Home" over "Country" (his word); the race crumb in the state card's heading form (one name for one thing); the last crumb alone truncating (a cut link misnames its target); the row under the header rather than in it (25.1a's measure of the header's room); 44 px link boxes on the phone (F-007's floor); the chain on chamber pages too (one rule for every page but the front).

**Addendum, 21:34 UTC: the check of build/site 3e9c83a (W9's build of s.28), on the deployed preview, 390x664 light and dark, 360x640, 312x531, 1280x720 light and dark [measured].** `nav[aria-label="Breadcrumb"] > ol`, the last `li` `aria-current="page"` and not a link, the separators › in `--faint` `aria-hidden`; links `--muted` (rgb(91,96,104) light, rgb(162,166,173) dark), the last crumb `--fg`, 12 px; the text's line at y 107 under the 57 px header on every page, the h1 at 129 (state, chamber) or 141 (race) as before. Words: "Home › Georgia", "Home › New York › District 17", "Home › Georgia › Governor", "Home › New York › Westchester County Legislator, District 4", "Home › New York › NY Supreme Court Justice, 9th Judicial…", "Home › Senate", "Home › Northern Mariana Islands › Delegate to the U.S. House" (the card's heading keeps a delegate's words, F-008), "Home › New York" on /ny/nothing with New York a link. Phone: the link boxes 44 tall (Home 16 to 48.3, the state from 67.9), 19.6 px between boxes, so the targets do not touch; desktop link boxes 28. Truncation: only the last crumb cuts (`scrollWidth > clientWidth`): the Supreme Court race at 390, 360 and 312; the Delegate at 360 and 312, whole at 390 (368.5 of 374); the Westchester chain whole at 390 (356 of 374) and cut at 360 (W9's figure; my 28.3 wrote 320 before the separators' air); every link whole at every width, "Northern Mariana Islands" 137 px. The crumb to the entry before: from the country tapped to /ga, Home runs animations (five running in the next frames) and `history.length` is unchanged (5 to 5), the browser's back; /ga/governor loaded directly, Home goes to / with `history.length` unchanged, in this entry's place. The tab's title unchanged on every page (the one formatter). No page errors. **Pass; W9's three choices adopted into v1.17.2.** Shots c58-crumbs-*.

## 64. The dark-mode pass on production e466d51 (21:13 UTC; the maker, 20:53: "in dark mode, the pin icon is black, so it can barely be seen. There might be some other issues in dark mode that I'd want checked")

**Method.** Production (bundle index-CMylOwnb.js) at 390x664 (isMobile) and 1280x720, `colorScheme: dark`, ten pins. Two passes on every surface the orchestrator listed: (1) an in-page audit of every element with its own text (its colour against the nearest painted ground, blended through alphas, WCAG ratio against 4.5, or 3 for large text), every SVG background image (whether it sets a fill), every inline SVG and every framed control's border; (2) the eye, on scrolled shots of the whole of each page (the page's scroller, not the window). Surfaces: the country (seat bars, timeline, map and legend, the pinned shelf, the latest call, the Senate list), the time button running and paused, the menu (the Reveal 2.0 drawer, Appearance, the pinned rows, Pause), the search with results, the night pane (phone) and the night's calls column (desktop), the state (Georgia, New York), the race (Georgia's Senate), the chambers (Senate, Governors, House with its table), the skeleton (data slowed). Production stood before any poll closed, so the called states, the called rows, the called cards, the map's colours and the night's calls were taken on the build/site preview (index-CKvhEoJA.js, the same code as e466d51 by PR #21) with `?fixtures`, dark, both widths. Shots `research/design/shots/dark-2026-11-03/` (a selection) and `/mnt/project-files/design/dark-2026-11-03/`.

**Dark faults: one.** The pin, the pinned mark and the grip are SVG background images with no fill, black in both schemes [measured in the CSS and by the glyph's lightest pixel: 19 over a 19 ground at 3x]; in dark they vanish in four places: the race heading's Pin / Pinned button (`.pinb .gl`), the shelf card's pinned mark and its grip (`.pinmark.on`, `.grip-b`, shown on the phone, on hover on the desktop), the desktop list row's gutter mark. Spec v1.17.1 (R9): a glyph is drawn in the text's colour in both schemes. W11's 806fc6c (build/morning) cures it with masks filled with `--fg` at .75 (the pinned mark at 1), measured here on a local build: dark 181 (pinned 235) over 19 in every place, hovered or not; light 80 (pinned 24) over 250, as before. **Pass.**

**No worse in dark than in light [computed from the tokens]:** `--muted` on `--bg` 6.1 light / 7.6 dark; `--warn` 5.7 / 9.5; `--dem` 5.7 / 5.8; `--rep` 4.8 / 5.9; `--oth` 5.0 / 7.1; the frames `--line-strong` 1.6 / 1.8 and `--line` 1.25 / 1.33 (the time button, the Pinned button, the "Latest call" strip, the Reorder button); `--track` 1.17 / 1.26 (the skeleton's blocks, the seat bars' empty track); the map's `--pend` 1.4 / 1.7 and `--none` 1.1 / 1.2. The Reveal 2.0 drawer is navy in both schemes by design (24.2); its red on white 5.0. The focus ring is `--fg` in both. Seen and sound in dark: the seat bars' paler segments, the timeline's bars and ticks, the map's called fills and the district map's, the legend's five coloured chips, the called rows' rule, check and party-coloured names and shares, the called pinned card, the night pane's grip, headings, strike-through and "call withdrawn", the Appearance control, the search results, the paused time button's `--track` ground, the stale status in `--warn`, the House tables, the skeleton's blocks (the sweep's band is W8's, MOTION-SPEC v1.8.55).

**Two notes in both schemes, not dark faults (for the morning):** (1) the map's no-race tile code ("VT", "ND", "IN"…, 12 px 600, `--faint` on `--none`) is 2.8:1 light and 3.9:1 dark, under 4.5; spec v1.17.1 writes `--muted` (5.4 / 6.4). (2) The "No race" legend chip (`--none` on `--bg`, 1.1 / 1.2) is a swatch of the tile's own ground and carries no word; left as it is, the tile beside it is what the chip explains.

**Count to the orchestrator: 1 dark fault (4 places, cured on 806fc6c), 0 other dark faults, 2 both-scheme notes.**

## 65. W10's stale-note wording on build/live 3470e71, checked against 12.3 and 12.1 (22:08 UTC; the maker, 20:52) [measured]

**Method:** the build/site preview at 390 × 844 and 312 × 531, the stat cell's own font read from a live row (`.row .stat`: 12 px / 18 px Plex), the candidate phrases measured in a hidden span of that font; the line breaks read by injecting each form into a live cell and walking its text by character rects. 3470e71 itself has no preview (build/live), so the words were measured, not the commit's render.

| phrase | width at 12 px | the column | note |
|---|---|---|---|
| "as of 9:04 PM" (old) | 73.4 | 104 | |
| "last read 9:04 PM" | 94.6 | 104 | fits |
| "last read 10:14 PM" | 101.8 | 104 | fits, 2 px to spare; "12:04 AM" the same |
| "Polls close 7:30 PM" | 105.1 | 104 | wraps to "Polls close" / "7:30 PM" at ≤640 (the cell is `white-space: normal` there), as the Ohio and North Carolina rows show on the preview at 390 and 312 |
| "21% in" | 38.2 | | |

**Verdicts.** (1) The row's "last read 9:04 PM" for an unreachable source and "as of" for a stopped clock: pass; the time is the fact 12.3 asks for, and the figure's own date was not it. (2) The card's "Can't reach civicAPI. Last read 9:04 PM ET." one line; the source line's own "as of" is civicAPI's stated time: pass. (3) "Polls close 7:30 PM" / "7:30 PM" / "Polls close 7:30 PM ET." before the close with no vote and no precinct: 12.1's own words: pass.

**One pre-existing fault, improved and not a block.** At 390 the stat cell breaks by words, and the warn span is inline, so the old form read "21% in as of 9:04" / "PM": the break inside the time, against 12.3's "the figure on the first and the time on the second" (v1.8.3's claim was read on f8c0367, where the cell may have been otherwise). W10's reads "21% in last read" / "9:04 PM": the time whole on its line. The one-line cure, named to W10: `.row .stat .warn { white-space: nowrap }`, so the span drops whole to line 2 ("21% in" / "last read 10:14 PM", 101.8 in 104) and the desktop's one line is unchanged. Spec 12.3 amended to his words (v1.17.4).

## 66. The state page's first screen on the phone, for s.29 (22:08 UTC; the maker, 21:58) [measured]

The build/site preview (bundle index-ZYQQxkxB.js), `?fixtures`, five viewports, the state page's parts read from the DOM after the data landed. The map's top is where the eye first meets the state shape.

| width | state | blocks (px) | map top | map height | map bottom | first House row | row grid |
|---|---|---|---|---|---|---|---|
| 390 | Georgia | 292 + 155 | about 650 | 252 | about 902 | 1604 | 104 / 219 / 0 |
| 390 | Michigan | 322 + 363 (four candidates each) | 953 | 252 | 1205 | 1854 | 104 / 213 / 6 |
| 390 | New York | 185 (the governor alone) | 382 | 252 | 634 | 1751 | 104 / 167 / 52 |
| 360 | Michigan | 322 + 384 | 974 | 230 | 1204 | 1958 | |
| 312 | Michigan | 361 + 384 | 1013 | 194 | 1207 | 2172 | 104 / 135 / 6 |
| 430 | Michigan | 303 + 342 | 913 | 281 | 1194 | 1822 | 104 / 253 / 6 |
| 1280 | all three | beside the map | 174 | 425 | 599 | | 150 / … |

The breadcrumb stands at 89 (40 tall), the head at 129 (26; 73 on Michigan, whose poll-status line wraps), the state's top at 173 (220 on Michigan). A House row is 81 to 85 px tall at the phone widths (two candidate lines, the status on two lines where it wraps), 60 to 64 at 1280. Georgia's map top is computed from the blocks' heights (the selector caught a 14 px glyph there); the others are read. So at 390 × 844 Michigan's map is wholly under the first screen and Georgia's shows about 190 px of its 252; New York's is whole. With s.29's strip (two rows, about 170 px) the map's top would stand at about 343 at every width, its bottom at 595 / 573 / 537 / 624 (390 / 360 / 312 / 430).

## 67. The source display on production, PR #24 live (22:17 UTC; the orchestrator's 22:10 on the maker's 22:01: "how I will see all the data side by side, and I want it visually tested") [measured]

**Method:** production (midterms.zwolk.com, bundle index-BgrU44ea.js, which carries PR #24's "Last read" words), no fixtures, 390 × 844 and 1280 × 720, dark and light; three races reached from their state's own page: Michigan's U.S. Senate (`/mi/senate`, civicAPI), NY-17 (`/ny/house-17`, the official-sum race, today on civicAPI) and Georgia's U.S. Senate (`/ga/senate`, the state's feed); the race card's source line, its link, its status lines read from the DOM; the API read beside it (`/api/races?keys=…&parts=1`). Shots: `shots/sources-2026-11-03/` (twelve).

| race | source line as shown | link | status lines | verdict |
|---|---|---|---|---|
| MI Senate | "civicAPI, as of Mon 10:44 PM ET · names: official list" | civicapi.org race 87214 | "Polls close 9 PM ET (first 8 PM ET in part of the state)." | true; the "as of" is civicAPI's own time for a race with no votes (see 2) |
| NY-17 | "civicAPI, as of Oct 22, 6:23 PM ET · names: official list" | civicapi.org race 87319 | "Can't reach civicAPI. Last read 5:11 PM ET." in warn on 2 of 4 loads, then "Polls close 9 PM ET." | see 2 and 4 |
| GA Senate | "Georgia's official count (Secretary of State), as of 12:03 PM ET · names: official list" | **none on the source**; "official list" goes to Gwinnett County's sample ballot | "Polls close 7 PM ET." | see 1 and 3 |

The source line is 12 px `--muted` in both schemes (rgb 91 96 104 light, 162 166 173 dark), one line at 1280 and at 390 except Georgia's (two lines at 390). Nothing differs between the schemes but the colours.

**Faults and notes, in order of what the maker will see:**
1. **Georgia's candidates carry their party twice:** "Mike Collins (Rep) (R)", "Jon Ossoff (I) (Dem) (D)": the state feed's names carry the incumbent mark and the party, and the card adds the letter. True words, said twice on every Georgia race the state's feed counts (23), and "(I)" there is the incumbent mark, which a reader may take for Independent. Cure for W10/W11: strip a trailing "(I)" and "(Rep)/(Dem)/(Lib)…" from the official feed's name where the catalogue's party matches (the incumbent is already marked by the card's own line).
2. **"as of Oct 22, 6:23 PM ET" still stands on NY-17's source line** (and "as of Mon 10:44 PM ET" on Michigan's): civicAPI's own time for a race with no votes, the date of the row's making. It is labelled civicAPI's and true (14.3), and PR #24 rightly took it out of the status; but it is the same words the maker named at 20:52 ("0% as of October 22nd"), one line lower. Candidate: while no count has begun (W10's `countBegun`), the source line names the source and its link alone ("civicAPI"), and the "as of" joins it with the first count.
3. **Georgia's official count has no link** (`sourceUrl: null` by docs/api.md s.10, a sum's contract), so the line names its source and does not link it. For Georgia the sum is one part, the state's feed (results.sos.ga.gov), so a link exists; candidate for W10: the sum of one part takes its part's URL.
4. **NY-17's warn line comes and goes** between loads a minute apart ("Last read 5:11 PM ET" = 22:11 UTC, read at 22:14–22:16): W10's known slow round of NY's House rows (132 s against the 60 s floor, his 22:02 watch note) makes a true note blink; once his sweep fix deploys the round should sit under the floor. Not a wording fault.
5. **Before the close, Georgia's card shows "0" in the votes column** for both candidates (the state feed's zeros), where 12.1 asks for the candidates with no figures before the close; the status says "Polls close 7 PM ET." correctly.
6. Minor: NY-17's heading at 390 breaks "U.S. House, District" / "17", the number alone on line 2.

Nothing false was seen: each source is named, each time is that source's and labelled so, no total is mixed. The sources side by side (the card the orchestrator put to the maker) are not on any page yet; the API carries them (Georgia's parts: civicAPI's counties, each with its own stale note, then the state's count).

## 68. The desks' Calls block with desk posts seeded by fixture (22:27 UTC; the orchestrator's 22:27 on the maker's 22:24: "if in a single race it could show calls from all of those sources within minutes") [measured]

**Method:** the build/site preview (index-ZYQQxkxB.js) with `?fixtures=script`. The fixture's own `__fixtures.call` and `deskCall` / `deskGone` were used, then `__midtermsPoll()`, and the block was read from the DOM. Two cases. (a) Michigan's U.S. Senate: civicAPI's call 15 minutes back, with NBC News 22, CNN 19, CBS News 16 (then marked gone), AP 11 and The Times 8 ("reports"); that is six lines. (b) Georgia's governor: CNN 6 and NBC News 3, with no civicAPI call. Georgia's Senate race was not among the fixture's shown-uncalled races, so (a) stands for the called case. Viewports were 312 × 531, 390 × 844 and 1280 × 720, in dark and light. Shots: `shots/desks-2026-11-03/`, twelve.

**What passes.**
- **Order.** The lines run in time order by the instant each vouches for: NBC 10:18, CNN 10:21, CBS 10:24, civicAPI "between 10:23 and 10:25 PM", AP 10:29, Times 10:32. CBS stands before the bracket because 10:24 is before its later bound, which is 14.1's rule.
- **Links.** Each desk's time is a link to its post (`bsky.app/profile/…/post/…`) with the ↗ mark. civicAPI's line is not a link, since it is no post.
- **Winners.** Each line gives the winner by surname. The Times reads "El-Sayed, reports".
- **Removed post.** The CBS line is struck through, with "post removed" after it in warn.
- **No civicAPI call.** For Georgia's governor the block lists the two desks and nothing is coloured: no call line, no check, no rule (R4).
- **Called race.** The call line above the block is civicAPI's, in the party colour.
- **Truths sentence.** It stands once, faint, under the source line.
- **Schemes.** Both are the same but for the tokens.
- **Fit.** Six lines fit at 312 with no overflow (block 225 px tall); at 390 it is 174 px and at 1280 158 px.

**Faults.**
1. **The times are not labelled where they are read.** Under the heading "Calls", "NBC News · 10:18 PM" reads as NBC's call time. The only words saying it is the post's time are the faint sentence under the source line: 300 px below the block at 312, and off the first screen. 14.3 put them once in the source line by R1, and that was my reading. Seen with real-shaped data, it fails the orchestrator's test, "the post's time labelled as when the desk posted". **Candidate:** the heading line reads "Calls" and then, in 12 px faint, "· desk times are when each posted". civicAPI's own line already says "between …", so it labels itself. The full sentence stays in the source line.
2. **At 312, a removed post's line breaks inside the name:** "El-" / "Sayed" / "post removed", 56 px tall. **Cure:** at ≤640 the winner cell is `white-space: nowrap` for the name, and "post removed" goes on its own line (`display: block; margin-left: 0`). That makes the line 2 × 17 px.
3. **civicAPI's bracket wraps on the phone:** "between 10:23 and" / "10:25 PM" in the 110 px time column at 312 and at 390. It is two lines and readable, so this is a note and not a block. The time column is 110 px for the bracket alone, while the desks' times need about 70. If the line is to stay one line at 390, the site's line could span the time and winner columns (`grid-column: 2 / 4`) with the winner after a middle dot.

**Not tested here:** whether real posts reach `deskCalls[]` tonight. That is W10's reader of the desks' Bluesky accounts, and it is not a design question.

## 69. W14's fixes of s.67 on build/sources-fix 80c5dbe, checked (22:34 UTC) [measured]

**Method.** Two parts.
- **Page items.** W14's preview (index-6RtSGIYI.js, rehearsal mode) at 390 × 844 and 1280 × 720, dark and light, on Georgia's Senate race, NY-17 and Michigan's Senate race. The preview's rehearsal data carries counts and calls, so the no-count state was made by intercepting the page's `/api/` and `/data/` answers: every race's votes set to 0, reporting to 0, call and desk posts cleared, `sourceAsOf` set to Oct 22. The real clock is before every close, so this is the state the maker saw at 20:52.
- **Server items.** W14's tests run in a worktree, and the diff read.

**Verdicts.**
- **Item 2, no "as of" before a count: pass.** With no count, the source line reads "civicAPI · names: official list", linked, on all three races, both widths and both schemes. With a count (the preview's rehearsal data, and `?fixtures`) the line reads "civicAPI, as of 10:36 PM ET", as before.
- **Item 4, no figures before the close: pass.** The candidates' votes and shares cells are empty, and the status reads "Polls close 7 PM ET." / "9 PM ET." With a count, the figures stand.
- **Item 5, the heading's number: pass.** At 390 NY-17's h1 breaks "U.S. House," / "District 17", with the number kept with its word. At 1280 it is one line.
- **Items 1 and 3, Georgia's names and the one-part link: pass by test and by reading; not seen on a page.** Georgia's races read from civicAPI tonight on the preview and on production, so neither shows until the state's count is the source again.
  - Item 1: `splitPrintedName` drops a trailing party mark equal to the option's own party, and turns "(I)" into `isIncumbent: true`. "(Ind)" is a party and is not dropped. The printed name is kept in `nameAsPrinted`. W14 measured that all 15 "(I)" marks in the feed are the catalogue's incumbents.
  - Item 3: a sum of one part takes its part's `sourceUrl`; a sum of several keeps `null` (docs/api.md s.10).
  - W14's ingest and enhancedvoting tests: 45 of 45 pass.
  - One gain beyond the fault: Georgia's names now equal civicAPI's and the desks' ("Jon Ossoff"), so a call's winner matches by name.

**One note, pre-existing and not W14's.** In the zeroed state the state's list rows still set one candidate at 600, the leader's weight (NY's "LaLota" in District 1), with no count to lead. A row with no count could set both names at 400. This is for the morning.

## 70. W9's strip (s.29) on build/site c5fe637, checked on the preview (22:42 UTC) [measured]

**Method:** the preview (index-CmyIUDYN.js), `?fixtures`, Georgia, Michigan and New York, plus Michigan before the close (`&now=2026-11-03T23:30:00Z`); at 390 × 844, 390 × 664, 360 × 640, 312 × 531, 430 × 932 and 1280 × 720, dark at every size and light at 390, 312 and 1280. The strip's rows, the map's box and the first block were read from the DOM. The skeleton was read with `/data/` held, at 390 in both schemes, then compared with where the content landed. A strip row was pressed by touch, then back. Shots: `/mnt/project-files/design/strip-2026-11-03/`. (The first context's first two loads served the old bundle from the edge; they were read again.)

**The strip passes.**
- The row is s.7's: 104 / 1fr / auto, 64 px tall with figures. The status is on one line ("83.3% in"); 29.2's 81 to 85 assumed a two-line status.
- The office is in the place column: "Senate", "Governor", 104 px with no overflow.
- The called form: Georgia's "Call changed" row has the 3 px rule, the check before the share, and the winner in the party colour.
- No Pin on the strip row. The row is a link: pressing it pushed `/ga/senate`, and back returned to `/ga`.
- Before the close: "Polls close 9 PM" with no shares.
- No horizontal overflow at any width.
- The desktop is unchanged: the first block at 174, as in s.66.

**The map's place (top to bottom).**

| viewport | GA | MI | NY |
|---|---|---|---|
| 390 × 844 / 664 | 326–588 | 373–636 | 262–524 |
| 360 × 640 | 326–566 | 373–614 | 262–502 |
| 312 × 531 | 326–531 | 373–578 | 262–467 |
| 430 × 932 | 326–618 | 352–644 | 262–554 |

Every map is whole in the first screen except Michigan at 312 × 531. There its last 47 px lie under the edge, because Michigan's head wraps to three lines at that width; 29.4 said 6 px. The box holds its height before the map is drawn (W9: the blocks' top 612 before and after).

**The skeleton FAILS 29.6 by its height.** While the file is on its way at 390 the strip's skeleton rows stand at 160 and 208, 48 px each, and the map box at 256. The content lands at 174 and 238, 64 px each, and the box at 326. So on arrival the box and everything under it jump 70 px down (the skeleton's first block 518, the landed one 612), in both schemes. **Cure for W9:**
- The strip's skeleton rows take the row's landed height, `min-height: 64px` (the 10 / 11 padding, two 21 px lines and the rule).
- The skeleton's wrapper takes the 15 px the landed strip stands lower, the `.state-top` top margin it lacks, so its top is 174.
- Then the box lands at 326 as the content does. 26.1's rule is that the swap is a change of ink, not of layout.

## 71. W14's cure for s.68 items 1 and 2, build/fix-desk-times 50b371a, checked (22:45 UTC) [measured]

s.68's method, run on W14's preview: the same two seeded races, at 312, 390 and 1280, in both schemes. Shots are in `/mnt/project-files/design/desks2-2026-11-03/`. **PASS.**
- **Heading.** It reads "Calls · desk times are when each posted" on one line at every width, with the added words at 12 px, 400, faint.
- **Removed post.** At 312 and 390 its line is 40 px. The name "El-Sayed" is whole and struck through, and "post removed" stands on its own line in warn. At 1280 it is one line, as before.
- **Unchanged.** The order, the links, the bracket and the uncoloured lines are as in s.68. civicAPI's bracket still wraps to two lines on the phone; that is s.68's note 3, not a fault.

## 72. W11's source switcher on build/fix-night 57fb3c4, checked (23:14 UTC) [measured]

**Method.** The preview (index-7XU343Np.js) with `?fixtures=script`, on NY-17, State Senate 40, Georgia's Senate race, Michigan's Senate race and Alabama's Senate race. Every option was chosen in turn at 390 dark, and the card was read from the DOM after each choice. The control's form and hit region (`elementFromPoint`, scanned top to bottom at the select's centre and at the Pin's x) were read at 390 light, 312 dark and 1280 dark and light. Each page was reloaded once.

**Passes (30.12).**
- **When it shows.** The control appears only with two or more counts. Alabama has none.
- **Order and default.** 30.2's order holds, and the race's total is first and the default: civicAPI on NY-17; the official sum on State Senate 40; Georgia's count on its Senate race.
- **What each choice shows.** These all belong to the chosen source: the candidates, the votes, the shares (summing to 100 ±0.1 within that source), the reporting words, the stale line ("Can't reach civicAPI. Last read 9:45 PM ET.") and the source line with its link (Enhanced Voting, Clarity, Westchester BOE, civicAPI).
- **The line under the control.** It says what is shown ("Showing Putnam County's own count, not the race's.", "Showing civicAPI's count. The site's total is the official sum.").
- **A county.** Its rows carry no colour or check, and the call line stays above. A whole-race count keeps its colour and check.
- **No count yet.** Names only, with "No count yet from civicAPI for Dutchess (part)."
- **Reload and region.** A reload shows the default. The region is 45 px tall at 390 and 312. There is no overflow at 312.
- **Schemes.** Dark and light differ only by their tokens.

**Faults and a question.**
1. **The Pin overlaps the select.** Where the head is one line (Georgia, Michigan), the Pin's region overlaps the select's, and the select is 33 px tall at the Pin's x. Cure: about 11 px more top margin on the control row there, so the select's region starts at or under the Pin's (the frame's bottom plus 10).
2. **A withheld sum's option reads "· no count yet".** The card then says the sum is not shown because Westchester has not answered. The option should read "· not shown".
3. **Question for W10.** In the fixture, civicAPI's county parts print the race's reporting: Appling and the race both read 14%, and Kent, Wayne and the race all read 83.3%. If the real parts carry no county reporting, a county's card must print none, not the race's.

**Minor.** Rockland's option shows the feed's printed "11/3/2026 10:35 PM". It is true, and the source line labels it as printed.

**Also passed tonight.** W9's strip skeleton, build/site b05d3af (index-Cl6jYJKu.js). With the file held and then released, the skeleton and the landed page are equal to the pixel on GA, MI and NY: in both schemes at 390 × 844, and in dark at 360 × 640 and 312 × 531.

## 73. How a call is announced: research for the maker's 23:08 "new update indicator" (23:14 UTC)

**His words:** "something in the site that is like a new update indicator. So for example, if a call is made, maybe there is a banner that comes down or something like that … Maybe there's a whole screen animation … try to get at the heart of what I'm getting." And at 22:24: "if in a single race it could show calls from all of those sources within minutes that would be FUCKING AWESOME."

**What I read, with its standing.**
- **Apple's Live Activities guidance** (developer.apple.com HIG, read whole from its JSON, changed 2026-10-13) [stated]:
  - "Alert people only for essential updates that require their attention."
  - Alerts show "the expanded presentation in the Dynamic Island or a banner" and by default play the notification sound.
  - "avoid alerting people too often or with updates that aren't crucial".
  - Animations have "a maximum duration of two seconds".
  - "preserve as much of the existing layout as possible".
  - "Significant updates, like sports score changes" are its own example.
  - The rule I take from it: the alert is for the event that changes the outcome, not for every count. It is brief, and it expands from something that is already there.
- **WCAG 2.2 Understanding 2.2.2** (w3.org, read) [stated]: motion that "starts automatically" must stop within five seconds or be pausable. "Five seconds was chosen because it is long enough to get a user's attention, but not so long that a user cannot wait out the distraction."
- **WCAG 2.2 Understanding 4.1.3** (read) [stated]: status messages reach assistive technology "without receiving focus" and "in a way that doesn't unnecessarily interrupt". The site's status region already speaks the calls, so the banner must not be a second live region (W8's point 9).
- **Television** [stated, from search-result titles only; the pages were refused (403) and are not read]:
  - CNN's "Key Race Alert" is a full-screen graphic with a sound sting, famous enough to be a meme (Bustle, Romper, Refinery29, 2016).
  - NewscastStudio, 2008: "CNN 'projection' stinger too much of a good thing". This is the known cost of a full-screen moment repeated all night.
- **The Guardian's 2016 lock-screen notifications** [stated, titles only, pages refused]: "Web Notifications, Part 2: Auto-updating"; "live election results right on your phone's lock screen". One notification, updated in place as results came, not a new one each time. That is the pattern W8 proposes for a second call during a banner.
- **W8's measures** (his s.74, ca3c385) [measured]:
  - An overlay moved by transform and opacity is free on the phone at 4×: gaps of 18 to 33 ms, through an 81 ms live render.
  - A banner that pushes the page loses a third or more of its frames and moves the map. Avoid it.
  - A full-screen layer on opacity alone is free. With a backdrop blur, 11 to 14 of 15 frames drop. Avoid the blur.
- **W12's Vault** [stated]: no banner or toast component. The nearest are navigation-04 (a top drawer, CSS transform) and top-morphing-navigation (a pill morphing into a panel on a spring). Both are Max-plan items, for reference and not to copy.

**What I take to be the heart of it** [inferred from his words]: he wants to **feel the moment a race is decided**, the way television's projection lands, wherever he is on the site, and to **see the desks arrive one after another** for the races he cares about. Not a feed of changes: counts move all night, and a banner for each would be noise (Apple's rule; law 5). So the trigger is a call, and the excitement is the first word on a race and then the others agreeing (or not).

The rest is in DESIGN-SPEC s.31 (candidate): three options and my recommendation.

## 74. W11's build/fix-label 5565ae8 checked: the AI mark and the desks' posts not placed on a race (2026-11-04 00:11 UTC) [measured]

Read on the preview midterms-git-build-fix-label-zachs-projects-74dd78e7.vercel.app (bundle index-Dw9K_dLW.js, served 00:06:53 after BUILDING) at 312 × 531/640, 390 × 844 and 1280 × 720/800, light and dark, with `?fixtures=script`. Shots are in `shots/label-2026-11-04/` (mi-*: /mi/senate; home-*: the front, with the phone's calls sheet open).

**1. The AI mark: PASS, light and dark.** I seeded MI Senate with a call 15 minutes ago, NBC by rule 12, CNN `basis` reading 6, and CBS reading 4 then gone.
- 1280: "El-Sayed · matched by AI reading" on one 23 px line. The mark is 12 px, inline, light 138,143,150 and dark 122,127,134.
- 390: the mark is `display:block` under the winner; the CNN line is 40 px.
- 312: the winner column is 66 px wide and the mark wraps to two lines (CNN line 56 px). It is readable and the name does not break.
- The removed CBS line strikes the desk, time and winner. The mark is not struck, and "post removed" follows in warn.
- The truths sentence carries the clause word for word. The NBC rule line has no mark. Document width equals the viewport at every size.

**2. The unplaced list: PASS at 1280, two corrections.** It shows the fixture's 3 posts newest first: "10:36 PM ↗ NBC", "10:21 PM ↗ AP via PBS News", and "9:59 PM ↗ CNN" struck with "post removed". The warn is light 138,90,0 and dark 226,178,89.
- Rows are 27 px and links are 80 × 19, at least 24 px apart (WCAG 2.5.8's spacing).
- The head is 12 px, light 91,96,104 and dark 162,166,173. The closing note is 12 px faint.
- (a) On the desktop it sits between the night's calls (top 510, height 552) and their source line ("Calls: civicAPI's decision desk…", top 1240), so that line is cut off from the calls it describes. Move the list below it.
- (b) On the phone it is the sheet's last block: top 3778 at 390 and 4541 at 312, after the whole night. Put it at the top as one collapsed line with its count (spec 32).

**3. The night's calls' compact line** reads "NBC 10:28 · CNN 10:34" with no mark on CNN, which was placed by reading. Spec 14.1 v1.21 adds ", AI-matched".

Sent to the orchestrator and W11 at 00:09. Item 1 does not wait on 2 and 3.

**The maker's 00:07, relayed by the orchestrator:** "I want ALL calls to have the banner thing. I want to see, for instance, when decision desk calls before CivicAPI calls. I'd also like the time to be recorded, because on bluesky the time says 7:00 for the call made by decision desk tonight and it came in at 7:02, at least according to the site, about warner in virginia." Written as spec 31.7 (every call, grouped per poll, with line 2 naming the earlier callers) and 14.1a ("decided 7:00 PM · posted 7:02 PM ↗", using W10's `decidedAt`). DDHQ's post text "#DecisionMade: 7:00 PM EST" is [stated] by the orchestrator; I have not read it. The orchestrator read it at its source at 00:09: createdAt 00:02:01.989Z, text "#DecisionMade: 7:00 PM EST"; W10's parser gives decidedAt 00:00:00Z (build/log-cut 65fce54) [stated, orchestrator]. The orchestrator also corrected s.31 at 00:12: the maker picked B by card at 00:05 (RULINGS.md 00:05); spec v1.21.1 writes it as adopted.

**Addendum, the re-read of build/fix-label 721c437 (bundle index-DINeLSlY.js, served 00:21:01; written 00:22 UTC) [measured]: PASS, light and dark, at 312, 390 and 1280.** The shots are `shots/label-2026-11-04/v2-*`.
- (a) At 1280 the list now follows the calls' source line: source line top 1072, list 1185, "All calls and closings" 1349.
- (b) On the phone, the sheet's first line under "The night's calls" is "3 desk posts not placed on a race". It sits at top 377 at 312 and 479 at 390, and is 25 px tall closed.
  - Its toggle is the site's accordion (a checkbox and its label), 280 × 24.8 at 312 and 358 × 24.8 at 390, which meets WCAG 2.5.8's 24 px.
  - Tapped, it opens in place to 160 px, showing the 3 posts, the struck CNN with "post removed" in warn, and the note.
  - The night's list follows it. There is no sideways scroll.
- (c) The compact line reads "NBC 10:37 · CNN 10:38, AI-matched" on the desktop column and in the phone's sheet. The source line ends with the clause word for word.

**Addendum 2, the merge candidate build/fix-label-ship ecf0bf0 (W11's 721c437 joined with main 29d21ff), read on its own preview (bundle index-DINeLSlY.js, served 00:23:43; written 00:25 UTC) [measured]: PASS, light and dark, at 312, 390 and 1280.** Every figure of the addendum above is repeated:
- the race page's mark: inline at 1280, its own line at 312 and 390, kept on the removed line;
- the truths clause;
- the desktop order: source line 1072, list 1185, "All calls and closings" 1349;
- the phone's fold: first line at 377 and 479, 24.8 px, opening to 160 px;
- the compact line's ", AI-matched";
- no sideways scroll.

The client bundle is the same file as 721c437's. So the pieces from main (W14's leaner reader, W10's gate on AI-only placements) are server-side and are not seen by fixtures. I name that in the pass rather than claim it [inferred from the identical hash].

## 75. W9's call announcement (s.31, B, every call) on build/fix-alert ce29602, checked (2026-11-04 00:47 UTC) [measured]

Preview midterms-git-build-fix-alert-zachs-projects-74dd78e7.vercel.app, bundle index-CSDYBnH0.js (served 00:42:11). Shots are in `shots/banner-2026-11-04/`: cb-* from W9's check and m-* from mine.

- **W9's own check against the preview** (`src/test/callbanner.check.cjs`, BASE set to the preview): 173 pass, 0 fail. It covers 390 × 844, 312 × 531 and 1280 × 720 in both schemes, then away, chamber and reduced motion.
- **A desk alone** (the orchestrator's GA case; DDHQ on an uncalled Senate race, no civicAPI call) fires the banner: "Decision Desk HQ: Ossoff wins Alabama's Senate race" / "posted 10:40 PM". It has no rule and no colour. (The fixture's names are invented.)
- **The press region** is the whole bar: the link's hit runs 0 to 54 of 56 px at 10%, 40% and 70% of its width, at 312 and 1280. The × is 44 × 44 and labelled "Close".
- **The moment, settled at 700 ms:**
  - Opacity 1 on --bg (dark 18,19,20; light 251,250,248), no backdrop filter.
  - 263 px tall at 312, 365 at 390, 343 at 1280, under the 56 px header.
  - "Michigan's Senate race / Abdul El-Sayed (D) 50.2% / Called · civicAPI · 10:41 PM" reads cleanly in both schemes.
  - W9's cb-390-dark-moment shows the page through the card because it was taken mid-fade.
- **Line 2** in dark is 162,166,173 on 18,19,20, and in light 91,96,104 on 251,250,248.
- **FAIL, the phone:** at 312 and 390, in both schemes, line 1 is cut with an ellipsis on all 7 races fired (6 site calls and the desk-alone call), e.g. "Called: Shoffner (D) wins Ark…". The text is wider than the box (`scrollWidth > clientWidth`). The cut takes the race. At 1280 none is cut. Spec 31.1 v1.22.2: short form on ≤640, two lines allowed, never an ellipsis.
- **W9's readings:** (1) warnings lead a burst ahead of pins: yes. (2) A pin gets its card for its first word and civicAPI's call, and later desks get banners: yes. (4) As built. (5) The race words: yes.

## 76. W11's s.33 and 14.1a on build/fix-called f7f18df, checked (2026-11-04 01:01 UTC) [measured]

Preview midterms-git-build-fix-called-zachs-projects-74dd78e7.vercel.app, bundle index-CGfL_0Sv.js (served 00:55:23). I ran 33.4's steps cumulatively on Maine's Senate race (fixture names) on the race page, /senate's rows and the front. The steps: DDHQ alone (decided 8 and posted 6 minutes ago), then AP, then civicAPI, then DDHQ's post removed, then NBC naming the other candidate. Then, separately, an AI-reading post alone. Read at 1280 light (all steps), 1280 dark, 390 dark and 312 light and dark. Shots are in `shots/called-2026-11-04/`.

- **DDHQ alone colours the race** with no civicAPI call:
  - the winner's row is checked;
  - /senate's row is `called rep` with "DDHQ 10:32";
  - the front's map paints Maine `st-rep`, with the accessible name "Maine · U.S. Senate · Susan M. Collins (R) · called by DDHQ 10:32";
  - the night's entry reads "10:32 PM Maine Senate: Susan M. Collins (R) · DDHQ (posted 10:34)";
  - the map caption is as 33.2.
- **14.1a:** "DDHQ · decided 10:32 PM · posted 10:34 PM ↗ · Collins". Its neighbours write "posted". The decided line is 23 px at 1280 and 40 at 390 and 312. The heading reads "desk times are when each posted, unless marked decided". The truths sentence carries both clauses.
- **Callers added:** "DDHQ 10:32 +1", then "+2". The map name lists "DDHQ 10:32, AP 10:36, civicAPI by 10:38". The compact line reads "AP 10:36 · civicAPI by 10:38".
- **DDHQ removed:** the colour stays from AP, and the row reads "AP 10:36 +1". The night's entry moves to 10:36, with "DDHQ 10:34" struck through. The race's line is struck through with "post removed".
- **The conflict:**
  - The call line reads, in warn: "Calls differ: AP, Collins (R) 10:36 · civicAPI, Collins (R) by 10:38 · NBC, Jackson (D) 10:39".
  - The winner has no check. The row is `plain`, with "Calls differ" in a `.warn` span (light 138,90,0; dark 226,178,89).
  - The map fill is not-called (214,211,204), with a warn outline and the legend's "Desks disagree".
  - The Senate's Rep figure drops 32 to 31, and the seat line adds "Desks disagree on 1."
  - The night's entry reads "Calls differ" in warn, followed by each caller with its winner.
- **An AI-reading post alone:**
  - colours nothing: the row is `plain` and has no check;
  - the race's Calls line carries "matched by AI reading";
  - the night's entry reads "Matched by AI reading; no other caller yet, so the race is not coloured."
- **Status cell:** one line (21 px) at 312 in both schemes. There is no sideways scroll at any size.
- **W11's four choices:**
  - "DDHQ" in the Calls block: yes.
  - The desktop time column at 240 px only when a line has a decided time: yes.
  - The night's entry form and the reading-only sentence: yes.
  - The map panel's "Called by …", the full sentence as the accessible name, and the district map's centred stroke: yes.
- **Follow-up 1, the phone's tile map:** the tile is an `a` to /me (28 × 28) whose accessible name is only "Maine" at 312 and 390. 33.2 asks it to carry the callers' sentence, as the desktop's path does.
- **Follow-up 2, the two counts and a party-less call:** the server (`lib/ingest/views.js` `nationalView`) and the fixture handle a call with no `winnerParty` differently.
  - civicAPI's count buckets it "other". `byAnyCaller` counts it `unknownParty`, and the bar shows it as uncalled.
  - So on the fixture the any-desk bar reads "2 other" against civicAPI's "3 other", and the line under the bar shows "civicAPI's desk alone: …" and "1 called, party not found" even where no desk touched a race.
  - Each figure is stated, so it is not false. But the second figure was meant to appear only where a desk differs.
  - The fix: one rule for both counts, so the two differ only where a caller does.

**Addendum to s.75: build/fix-alert 0513813 re-read (bundle index-tjFaiAou.js, served 01:01:29; written 01:11 UTC) [measured]: PASS, light and dark, at 312, 390 and 1280.** Shots are in `shots/banner-2026-11-04/v2/`.
- On the phone, line 1 is whole (`scrollWidth ≤ clientWidth`) on all 7 races, in the short form: "Called: Shoffner (D) wins Ark. Senate", "Decision Desk HQ: Ossoff wins Ala. Senate". The bar is 75 px with two lines.
- At 1280 the long form is whole, and the bar is 61 px.
- Line 2 is never cut. The settled moment is opaque in both schemes.
- W8 passed its motion (W8 s.77).

**Addendum to s.76: build/fix-called 84ef245 (written 01:11 UTC): PASS.**
- The preview served index-CGfL_0Sv.js from 01:02 to 01:10, the same client bundle read on f7f18df. The diff f7f18df..84ef245 is server-only: lib/ingest/ledger.js, views.js, docs/api.md and tests, from W10's own-desk vouch, PR #38. So every surface read in s.76 stands.
- The vouch is server logic that the fixtures do not exercise, so its check is W10's tests, not this pass.
- The orchestrator's reason for urgency [stated]: civicAPI has answered 502 since 00:43. Every call is from a desk, and GA (Ossoff) and FL-14 (Castor) were missing from the night's calls until fix-called is on main.

**Addendum 2 to s.76: production after PR #40 (main b07eb93), read 01:22 UTC; and build/fix-called2 e950e11 (written 01:23 UTC) [measured].**
- **Production** serves index-BU_zz_xx.js, not the preview's Br3zZutX: production's build differs. I confirmed the served bundle contains "call-banner", "Desks disagree", "AI-matched" and "not placed on a race". Read at 1280 light and dark, 390 dark and 312 light (shots in `shots/called-2026-11-04/prod/`):
  - The night's calls hold "7:18 PM Ga. Senate: Jon Ossoff (D) · DDHQ (posted 7:18)" with "NBC 7:45 · CNN 7:58 · AP 7:59", and "7:48 PM Fla. U.S. House 14: Kathy Castor (D) · DDHQ (posted 7:52)", on the desktop and in the phone's sheet.
  - The GA map's name reads "called by DDHQ 7:18, NBC 7:45, CNN 7:58, AP 7:59". /ga/senate lists DDHQ "decided 7:18 PM posted 7:18 PM", civicAPI "between 7:40 and 7:42 PM", NBC, CNN and AP, with Ossoff checked.
  - Senate seats read 35 D, 2 other, 32 R, with the line "civicAPI's desk alone: 33 Dem, 31 Rep, 2 other."
  - No banner at load, no page errors, no sideways scroll. A banner firing on production was not seen, because no new call came while the page was open.
  - Follow-up to W11: GA's compact line omits civicAPI's call, which the race page shows.
- **fix-called2 e950e11** (bundle index-jqLpb2Px.js): PASS at 312 light, 390 dark and 1280 light.
  - The phone tiles' names carry 33.2's sentence ("Maine · Senate · Susan M. Collins (R) · called by DDHQ 10:32"; "Maine · Senate · calls differ").
  - After DDHQ, AP and civicAPI agree, the seat line reads only "Seats called by any desk. 1 called, party not found." "civicAPI's desk alone …" returns with a desk alone or a conflict.

## 77. W11's "Meanwhile" line (W10's `whileUnreachable`) on build/fix-meanwhile 342256a, checked (2026-11-04 01:36 UTC) [measured]

The maker, 01:12 [stated, orchestrator]: "Civic API being down is a massive problem for the site". Preview bundle index-CgzPKZEi.js. I ran /mi/senate?fixtures=script with `__fixtures.unreachable('MI|U.S. Senate|Class 2')` at 312, 390 and 1280, light and dark. Shots are in `shots/meanwhile-2026-11-04/`.

- **The line** reads: "Meanwhile, 1 of Michigan's 3 counties publishes its own count, read by this site. Added together, that county alone: El-Sayed 127,468 · Rogers 97,229 · Christensen 3,116 · Long 3,116. It cast 12.4% of Michigan's 2024 vote; this is not Michigan's count. Read 10:40 PM ET."
  - It is 13 px in --fg (dark 236,235,231; light 22,24,27), with no party-coloured element.
  - No candidate is checked and there is no call line.
  - It sits under "Can't reach civicAPI. Last read 10:40 PM ET." in warn.
  - It is gone after `unreachable(key, false)`.
  - No page errors, no sideways scroll.
- **The fold:** the head is 280 / 358 / 620 × 40. Open, it shows "Oakland El-Sayed 127,468 · Rogers 97,229 Clarity, read 10:40 PM ET" and "2024 vote: FIXTURE: invented share."
  - The county's name is a button, 45 × 45 on the phone and 45 × 17 on the desktop.
  - Pressed, it picks "Oakland · county's own feed · 10:38 PM" in the switcher, whose line reads "Showing Oakland County's own count, not the race's."
- **FAIL (a):** the closed head reads "The county's own count" and "Fewer" together (`innerText` holds both, in every case checked; screenshot mw-390-dark).
- **FAIL (b):** civicAPI's "83.3% of precincts in" falls under the block and its fold, where it reads as the counties' figure.
- **FAIL (c):** at 312 the press leaves the switcher at y = -17. The view shows Oakland's 55.2% with no label in sight (mw-312-light-picked). At 390 and 1280 it stays in view (133, 140).
- **Not read:** a county left out of the sum. The fixture always sends `left: []`. From `MeanwhileSum` it reads " Not added: {county} ({why})." in faint, and with none added there is no sum and no "not … count" sentence [inferred from the code].
- **W11's choices, confirmed:** the 13 px plain line with no colour; the fold's head words; each county's line (name, two leaders, source and read time); every candidate in the sum.

**Addendum to s.77: build/fix-meanwhile 31fce23 re-read (bundle index-BeLbdCBQ.js, served 01:42:36; written 01:44 UTC) [measured]: PASS, light and dark, at 312, 390 and 1280, with and without a left-out county.** Shots are in `shots/meanwhile-2026-11-04/v2/`.
- (a) The closed head reads only "The county's own count" or "The 2 counties' own counts". Open, it reads "Fewer".
- (b) The text order is the stale line at 324, "of precincts in" at 375, then "Meanwhile" at 391 (character offsets in the card).
- (c) Pressing Oakland puts the switcher at top 63 on the phone and 73 on the desktop, under the header's 57. The "Showing Oakland County's own count, not the race's." line sits at 102 to 119 (102 to 135 at 312).
- **The left-out case** (`unreachable(key, true, true)`) reads: "Meanwhile, 2 of Michigan's 4 counties publish their own counts, read by this site. Added together, that county alone: El-Sayed 127,468 · Rogers 97,229 · Christensen 3,116 · Long 3,116. Not added: Ingham ("Somebody Else" is not one of the race's candidates). It cast 12.4% of Michigan's 2024 vote; this is not Michigan's count. Oldest read 10:40 PM ET."
  - "Not added" is faint (dark 122,127,134; light 138,143,150).
  - Ingham is listed in the fold ("Rogers 10,803 · Else 4,321 Ingham County Clerk") with no press, since the switcher does not list it.
- **W8's shift facts (W8 s.78):**
  - The 159 px push when civicAPI becomes unreachable stands. It is the news itself, rare, and not of the reader's doing; reserving room for it would cost every page all night.
  - The 196 px rise at a county's press now happens out of view, because of (c).

