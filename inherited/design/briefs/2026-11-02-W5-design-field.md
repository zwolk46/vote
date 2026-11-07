# W5: the field of components, maps, motion and typefaces

*Brief written by the orchestrator, 2026-11-02 04:00 UTC. Read `briefs/_COMMON.md` first; it is part of this brief.*

**Model and effort: Opus 5.5, high.** *Reason:* whether a component is refined and fits the rest of a site, and whether it serves the room watching results, is judgment (law 4, 5; `OPERATIONS.md` 4).

## Your sub-end

The orchestrator can choose, separately for desktop and for phone, the site's components, maps, motion and typefaces from a field it knows: what kinds exist, where the best examples are catalogued, the best examples of each kind, how each would serve the room watching results arrive, and what each costs and how it is licensed.

*Why this is a condition of the end:* ease and beauty are half of what "best" means (law 1a, 4, 5); components and ways of moving are chosen deliberately for each kind of screen (law 4); none of them is fixed before the field is known (law 6b).

## Constraints

- **The decided cases in `RULINGS.md` are evidence of what the maker means:** the navigation menus of details.so (loved: precise, fluid, natural, integrated with the page); the faults he listed (hover glows and shadows, moving arrows, dots that pulse for nothing live, text scrolling across the screen, numbers on things not in sequence, filler text, soft drop shadows between cards). Read the source of these, `research/reviews/2026-10-24-ui-principles-behind-the-goal.md` in `zwolk46/designsystembrain`, whole. *Reason:* general law 1d: a new case is read as the maker read the most like decided cases.
- **Fit over flash.** Record each candidate with how it fits a site for watching results, not only how it looks alone (law 5: "beautiful in the context of the rest of the site"; "a component copied without its fit is a skin").
- **Motion that signals an event is information only when the event is real** (law 5). Note for each moving component what real event it would signal.
- Typefaces and component kits that cost money are weighed alike with free ones, with the seller's stated web licence and price (law 7a).
- You build nothing for the site. Throwaway prototypes in scratch, outside the repository, are allowed where watching a motion is the only way to judge it; record what you learned, not the code. *Reason:* the build begins only after the maker's word on the plan (law 6a).

## The path fixed for you

1. **Breadth: catalogues.** Where refined components and motion are catalogued (galleries, component libraries, motion libraries, design inspiration sites, the Mobbin and Figma connectors, the 21st.dev skill in this session), and where election and data-graphics work is catalogued. Say which are worth depth and why.
2. **Election-specific components** across the field: scoreboards and seat bars, race cards, calls timelines, expected-vote and "how much is in" displays, needles and probability displays, swing displays, tables of races, navigation between national, state and district views. The inherited survey (S1, `inherited/README.md`) covers 21 sites; check it and go beyond it (sites it could not read, data desks' own write-ups, award-winning election graphics).
3. **Maps.** Kinds (geographic, tile and hex cartograms, district maps, insets for small states and districts) and the tools that draw them (for example d3-geo, MapLibre, deck.gl, and others), with licences, costs, phone performance, and how each handles hover on desktop and touch on phone. The ideas of law 11 (a national map of where the contests are; hover a state to see its races; click into a state to see its districts) are each to be justified toward the end or dropped; give the evidence for both sides.
4. **Motion.** Libraries and techniques (spring physics, layout animation, view transitions, and others), with what makes motion feel exact and natural. Read the details.so menus first-hand (Playwright is installed: capture, and read the CSS and scripts for durations, curves and springs) and say what makes them what the maker loves.
5. **Typefaces** for a results site: legibility of numbers (tabular figures), sizes from scoreboard to table, on desktop and phone. Free and paid, each with its licence and price.
6. **Desktop and phone separately:** for each kind above, which belongs to one kind of screen, which to both, and how a way of moving differs between them (law 4).
7. Background, read-only: `research/sweeps/S1-parts.md`, `research/census/TAXONOMY.md`, `research/vocabulary/DICTIONARY.md` in `zwolk46/designsystembrain`. Nothing in them is fixed for this site.

## Where you write

`research/design/2026-11-02-W5-design-field.md`, and screenshots under `research/design/shots/` (each under about 300 KB). Scratch work stays outside the repository.

## Report and escalate

As `_COMMON.md` 10 to 12.

## Continuation (orchestrator, 2026-11-02 04:12 UTC, in the project "Midterms")

You continue the W5 who stopped at 04:01 UTC (`_COMMON.md` 16). Start from section 9 of your file. Breadth is done; this is depth for the second report:

1. **The few candidates per kind**, for desktop and for phone separately (law 4): the site's way of moving between national, state and race views; the race card; the seat count; "how much is in" and expected vote; calls and their timeline; the map (or no map) and its tool; the typefaces. For each: what it serves for the room watching, the real event any motion signals (law 5), its weight against W6's proposed budgets (section 6 of `research/stack/2026-11-02-W6-build-and-live-updates.md`: first view about 300 KB compressed, JavaScript about 100 KB), its licence and price. *Reason:* the plan names the site's components for each screen (law 6a), and a component the page cannot carry fast on a phone fails ease and speed together (law 2, 4).
2. **Watch the motion before recommending it**: throwaway prototypes in scratch, outside the repository (a seat bar crossing its majority mark; a count changing; moving from the country to a state), judged against what you measured of the details.so menus. Record the timings and curves you would propose and why, not the code. *Reason:* law 5 asks for motion exact in timing and natural in feel, which is judged by watching.
3. **Prices still unread** (GT America, ABC Diatype, Graphik web licences; any paid component kit) at the seller's page; the Downballot hexmap's files and terms. Do not contact sellers (law 7a).
4. **The second report by 09:00 UTC** in the form of `_COMMON.md` 10 and 12.

## Continuation 2 (orchestrator, 2026-11-02 13:09 UTC): hierarchy and prebuilt components, on the maker's ruling of 13:08 UTC

The build has begun (the maker's approval, 11:36 UTC). W9 builds the page on `build/site` (thread `cmsg_012gZsfgtrnEcQeCcujWaxp38md1nLmgmfmUcjrV3oG2GL`); W8 owns motion (`research/design/motion/MOTION-SPEC.md`, thread `cmsg_012gZsfgtrnEcQeCcujWaxp3Xz5x71yCcxJ6ccurZ91LEb`). Read the maker's ruling of 13:08 UTC in `RULINGS.md` whole first. *Reason:* it is the case you serve now (general law 1d).

**Your sub-end now:** W9 can give every view a deliberate visual hierarchy and use well-made prebuilt components where they fit, from a written specification you make by looking at the page as built.

1. **Hierarchy and separation** ("a LOT of text, and a lot of it looks the same … deliberate separation of elements (doesn't mean MORE, but deliberate, and some could have different formatting, as truly relevant)"). Build `build/site` locally (the Vercel connector cannot open previews; Playwright is installed), look at every view on desktop and phone, and write, view by view: what the room needs first, second and third; what is primary (size, weight, figure style), what is secondary (quieter), what can go behind a press; how groups are separated (space, a rule, alignment) without adding boxes or the named faults; which text is a label, which a figure, which a source line, and how each is set (type scale, weights, colour roles, tabular figures). *Reason:* his words; law 4 and 5 (beautiful in the context of the rest of the site; ease).
2. **Prebuilt components** ("I don't feel like I'm seeing lots of components taken directly from sites with nice prebuilt components … Even if it's like a popup mobile card"). From the catalogues you surveyed (s.1; for example Vaul's drawer, Radix and Base UI primitives, shadcn/ui, Ark UI, 21st.dev, and others), choose, per surface, the component that fits (the phone's bottom card first: he asked for "a card come up from the bottom" on the phone), with its licence, its weight under Preact (`preact/compat` where it is a React component) against the 300 KB first view, and what it must be changed to obey (MOTION-SPEC; the named faults). Recommend one per surface; the orchestrator adopts. *Reason:* his words; law 7a for licences; law 2 for weight.
3. **The hover outline** ("sometimes a thick outline sometimes a thin outline and sometimes combined for a single state; shouldn't be that way") is W9's to fix; check the fix when it lands. *Reason:* his words.

**Model and effort:** Opus 5.5, high (judgment; `OPERATIONS.md` 4). **Where you write:** `research/design/2026-11-02-W5-hierarchy-and-components.md` on `main` (research), the specification as `research/design/DESIGN-SPEC.md`. **Report** as `_COMMON.md` 10 to W9 and the orchestrator: the phone bottom card and the country view's hierarchy **by 15:30 UTC**, the rest **by 19:00 UTC**. Take every time from `date -u`. *Reason:* the site goes public Tuesday morning Eastern (law 6); the deadline orders the work and shrinks none of it (law 8).

## Continuation 3 (orchestrator, 2026-11-02 14:52 UTC): the plan of similar changes, search, the logo

On the maker's rulings of 14:40 and 14:41 UTC (`RULINGS.md`, read whole). He calls the changes "EXCELLENT". He asks that we "understand the reasoning behind the changes I wanted made" and make "similar kinds of changes … elsewhere in the app, as relevant", and he reviews the plan first.

Write `research/design/SIMILAR-CHANGES-PLAN.md` for the maker to read, short and plain:

1. **The reasoning.** The principles behind each ruling from 13:08 to 14:41: what he objected to, and what he praised. Use his words where they carry the meaning, and mark what you infer.
2. **The plan.** Every other place where the same reasoning applies, view by view, on desktop and phone. For each: what is there now, the change, and the principle it serves. Include what is not built yet: the House table, the race view, the chamber views, the rehearsal and stale states, errors, loading, and the empty states before the polls close.
3. **Search** ("search anything relevant (candidates, states, districts? Others?)"):
   - **What it covers.** Consider candidates, states, districts by number and by place, offices, measures, counties, towns (for example Chappaqua), ZIP code to district, and incumbents.
   - **The data for each.** What we hold (races.json, W7's boundaries) and what we would need (Census relationship files).
   - **Weight and loading.** The index's weight, and how it loads lazily, outside the first view.
   - **Where it lives.** The menu's field, a command palette, a desktop shortcut.
4. **The logo.** "Real symbols/svg's/parts of svg's instead of an invented flag with a single star". Give two or three directions built from real, existing SVGs, for example:
   - the U.S. flag's own geometry from a public-domain source;
   - an established icon set's star (Lucide, Phosphor, Heroicons, Tabler);
   - lipis/flag-icons (MIT).

   Read each one's source and licence at the source, and draw each direction in `specimens/`. en.wikipedia.org gave 429 to W4, so try upload.wikimedia.org or Commons only once, and stop on refusal.

Leave components and transitions out: they go to W11 (`briefs/2026-11-02-W11-components.md`). Say where the plan depends on W11's outcome.

**Due:** the plan by 16:15 UTC; the logo specimens with it, or by 17:00 at the latest. Then return to checking W9's pieces.

*Reason:* he asked to review this plan before more is built in this direction, and the build cannot wait long (law 6).

## Continuation 4 (orchestrator, 2026-11-02 15:16 UTC): pinned races, and no blank race view

On the maker's ruling of 14:54 UTC (`RULINGS.md`, read whole, with the orchestrator's reading against law 10). Write it as a short addition to DESIGN-SPEC (s.13; s.12 is the page's states, v1.2), with specimens at 1280 and 390, by **16:30 UTC**, so W9 can build it tonight.

1. **"Pinned" replaces "Chappaqua and Michigan"** on the country view (s.7) and in the menu (s.4). Law 10's six races are the default pins; any race can be pinned from its row or its view, unpinned, and reordered; pins live in the viewer's browser (localStorage, no account). Say how a pin is marked on a row, where the pin control sits so it never crowds the figures (R3), and how reordering works on desktop and on the phone (the component is W11's; name what you need from it). The section is empty only if the viewer unpins everything, and then it says one line, not a blank.
2. **A race never opens on a mostly blank page.** Decide, with reasons, between (a) a race panel that opens within the state view on desktop, keeping the state's map and other races in view, with the race's own address still working as a deep link; and (b) a race page filled with the race in its context. Recommend one. Either way the race's content is: candidates with votes and shares; how much is in; the call; the last election and the incumbent; the county or unit parts where W10's `parts[]` has them (law 3: where the count comes from), with the map showing the race's place. The phone keeps the card (s.9).
3. **Cards:** say where a card fits and where it does not, in his words ("consider that in light of what they might be used for"), so W9 does not reach for cards elsewhere.

*Reason:* his ruling; law 10 read as in `RULINGS.md`; law 3.
