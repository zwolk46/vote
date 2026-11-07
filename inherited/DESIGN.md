# The midterms look and feel: what to carry over

*Written 2026-11-06 by the midterms orchestrator for the vote-importance site, which the maker wants "very similar looking in feel and style to the midterm site" (15:34 UTC). Evidence, not law: the new law and the maker's rulings decide. Paths are in zwolk46/midterms.*

## The sources, in order of weight

1. **The maker's rulings** (`RULINGS.md`, 11-02 to 11-06). Those that are about taste, not about elections, carry over as evidence of what he likes; they are summarised below with their dates.
2. **`research/design/DESIGN-SPEC.md`** (W5, 275 KB). Read sections 0 and 1 (what he does not want, and the rules for every view) whole. The rest is election-specific; read a section only when its surface is needed (19, icons and inspiration; 15, light and dark; 23, the case that does not fit).
3. **`research/design/motion/MOTION-SPEC.md`** (W8, 130 KB). Read sections 1, 2, 4, 5 and 6 whole: the rule, the tokens, how to build, reduced motion, and "never". The tokens are in `src/lib/motion.js`.
4. **`src/styles.css`**: the colour tokens (light and dark), the type scale, Plex. Its first 90 lines are copied into `starter/src/styles.css`.

## What makes it look like itself

- **One typeface:** IBM Plex Sans, variable, weights 400 and 600 only, widths 85 to 100%. Files: `public/fonts/plex-sans-var-latin.woff2` and `-latin-ext.woff2`, licence `public/fonts/IBM-Plex-Sans-OFL.txt`.
- **Five sizes, two weights** (DESIGN-SPEC R2): figure 32/26 px, head 24/22, sub 19, body 15, source 12. Each step about 1.25 times the next, so each reads as a rank.
- **Figures** in tabular numerals on a shared right edge, never inside a sentence (R3).
- **Colour carries meaning, never decoration** (R4): ink, muted, faint for text; strong colour only for what the data says. The page is a warm off-white (`#fbfaf8`) and a near-black dark scheme (`#121314`), both kept by the viewer's choice (system, light, dark).
- **Separation without boxes** (R5): space on a 4, 8, 16, 24, 40, 64 scale; one strong rule opens a list, hairlines between rows; no bordered cards, no shadows anywhere.
- **Text only if it must be read** (R1): no subtitles explaining headings, no instructions, no filler. Test: cover the line; if nothing is now misread, it goes.
- **A heading is said once** (R6); **one source line per section** (R7); **statuses in short words** (R8).
- **Motion only on a real event** (MOTION-SPEC 1): a spring for navigation and decisive events, nothing on timers, no stagger, no pulse, no shimmer, no bounce on figures; only transform and opacity move; reduced motion written first.

## The maker's taste, from his rulings (dates UTC)

- **Components: his picks, or designed within the principles.** On midterms he required found components only (11-03 20:40, 21:20; 11-05 20:58 to 21:03). On 11-07 02:45 he corrected that as too strict: found parts rarely fit together, so build from a component he names, and otherwise let the design worker design within the principles, using Details, 21st.dev and Mobbin as references (`design/README.md`, step 1).
- **What he named as faults:** soft drop shadows between cards ("peak AI default design", 10-23); hover glows, moving arrows, pulsing dots, scrolling text, numbers on things not in sequence, filler text (DESIGN-SPEC preamble); text that "looks the same" at one level (11-03 13:08); bars that are "just rectangles" (13:21).
- **What he loves:** details.so's navigation menus: precise, fluid, natural, integrated with the page (10-24).
- **Non-partisan:** "red and white AND blue … it's just a data displayer, it's not right or left" (11-05 20:58). A vote site about the weight of a vote should not lean either way in colour.
- **A standard for some applies to all** (11-05 20:35).
- **No jumping while loading** (11-05, W19's brief): nothing on the page moves when data arrives; skeletons hold the space.
- **Light and dark, by the viewer's choice** (11-03 20:40).
- **Design workers run at max effort** (11-05 22:09). This costs: on 11-06 he asked to wind down for usage, so ask him before starting one at max.

## What to copy, and what not

| Copy when needed | Leave |
|---|---|
| Plex fonts and licence (initialization does this) | candidate photos, faces, portraits |
| the tokens in `starter/src/styles.css` | party colours as meaning, unless the formula needs parties |
| `src/lib/motion.js` (the tokens and `play`), adapted: it imports `live.js` and `navstate.js`, which the new site will not have | results feeds, ingest (`lib/ingest/`), `api/` |
| `src/lib/fitheads.js` (a heading steps down a size where its longest word cannot fit) | the door (`middleware.js`, `lib/gate/`) and its passcode |
| `src/components/Boundary.jsx` (one broken part does not blank a page) | Supabase, Vercel Blob, the midterms Vercel project and its environment |
| `scripts/fitcheck.cjs` as a model for a fit check across phone widths 320 to 430 and text 1× to 2× | district boundaries, unless the formula needs geography; then `data/static/` holds Census-sourced files, with their sources in `research/races/` |
| the link-preview renderer (`lib/og/`, `api/og.js`, #251) if the site needs share cards | |
