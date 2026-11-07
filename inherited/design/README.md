# The design capital from midterms

*Copied on 2026-11-07 from zwolk46/midterms, by its orchestrator, at the maker's ask (02:39 UTC 11-07, verbatim in `ASK.md` here). The midterms site's look was refined over five days of his corrections. This folder carries those corrections here, so that agents apply them without his having to make them again.*

## The rule (why this folder binds by default)

**Any work that decides how this site looks, moves, reads or is laid out follows this folder.** Each of the maker's rulings in `TASTE.md` stands here as his default, unless he rules otherwise in this project. A worker whose brief touches design reads the files below before it draws anything. **One exception:** `TASTE.md`'s rulings that every component must be a found, real one are replaced by his 02:45 UTC 11-07 correction (process step 1 below). Where this folder and this project's `LAW.md` or `RULINGS.md` differ, those govern.

*Reason:* his words of 02:39 UTC 11-07: "ensure absolutely that whatever information is used here to very easily change designs or redo web pages … are automatically applied". A taste ruling is about him, not about elections, so it carries over. A ruling that only makes sense for elections was left out of `TASTE.md`; the full record is in midterms.

## Read, before any design work, in this order

1. **`TASTE.md`**, whole. His rulings on design, verbatim and dated, grouped, each with what it means for any site.
2. **`specs/DESIGN-SPEC.md`**, sections 0 (what he does not want) and 1 (the rules for every view: R1 to R9), whole. Then the sections for the kind of surface you are building: 9 (drawers), 12 and 26 (page states, skeletons), 15 (light and dark), 16 (search), 17 (switches and tabs as real components), 19 (icons and inspiration), 20 (bona fide uses for components), 23 (the case that does not fit).
3. **`specs/MOTION-SPEC.md`**, sections 1, 2, 4, 5 and 6 whole: the rule, the tokens, how to build, reduced motion, and the "never" list.
4. **`../DESIGN.md`**: a one-page summary, and what to copy and what to leave.

## How a design is made here (the process he settled on)

1. **Real components where they help; design freedom where they do not.** The maker's correction of 2026-11-07 02:45 UTC replaces the midterms rule that nothing is designed in-house (`ASK.md`): "I think I was too strict about using real components", and "it's impossible for the agent themselves to find components that actually work perfectly together". So:
   - **When the maker names a component** ("use this sidebar"), build from it. That worked well on midterms.
   - **Otherwise the design worker designs**, within the principles above (`TASTE.md`, DESIGN-SPEC sections 0 and 1, MOTION-SPEC). It may look at real examples on Details, 21st.dev and Mobbin for reference and use one when it fits the page as a whole, but it is not limited to them. A whole page that works together outranks a set of found parts that do not.
   - Never generate with 21st.dev's `generate` without his word (it costs).
   *Reason:* on midterms the sign-in page was held to found components only, and the found parts did not fit together or come with how they were meant to be used (his words, 02:45 UTC 11-07).
2. **Show him options side by side, never one.** For a surface that matters (the first screen, the hero), build two or three whole options on one preview branch, switched by a query parameter (for example `?v=a`, `?v=b`, `?v=c`), with a picker shown only on previews. Send him the links and let him pick. *Reason:* this is how the midterms door was redone (W25, `briefs/2026-11-05-W25-door-sourcing.md`; W18, `briefs/2026-11-05-W18-door.md`). Each option was a whole build he could try, not a mock-up.
3. **Motion is measured, not judged by eye.** Use the tokens in `code/motion.js`; check the press-to-motion time and frame gaps on a slowed phone profile (MOTION-SPEC 4, rule 11). *Reason:* `briefs/2026-11-02-W8-motion.md`.
4. **Every page is checked where it does not fit:** phone widths 320 to 430 at text 1× to 2×, desktop at the narrowest width of each layout, light and dark, with real data. `code/fitcheck.cjs` is the model, and `code/checks.cjs` runs every check. *Reason:* the maker, 11-03 12:50: "These are all things you should catch yourself"; `briefs/2026-11-05-W23-phone-fit.md`.
5. **Nothing jumps while loading.** Reserve the space for what is coming and measure layout shift on arrival. *Reason:* `briefs/2026-11-05-W19-settle.md`.
6. **One broken part never blanks a page.** Use `code/Boundary.jsx`. *Reason:* midterms #241 and #246.
7. **Design workers run at high effort**, and at max only when he asks: he asked for max on 11-05 22:09 and for less usage on 11-06 11:30.

## How to change or redo a page quickly

- **Change one rule everywhere.** Tokens live once, in `:root` (colour, the five type sizes, the space scale), and motion lives in one table (`code/motion.js` `TOKENS`). A change to the look is a change to a token, not to each page. *Reason:* DESIGN-SPEC R2 to R5; `specs/SIMILAR-CHANGES-PLAN.md` is the midterms plan for making one change reach every like surface.
- **A standard for some applies to all** (the maker, 11-05 20:35). When a fix lands on one page, find every like page and apply it there in the same PR.
- **Redo a page** by the process above: real sources, then options on a preview branch, then his pick, then the fit check, then merge.

## What else is here

| Path | What |
|---|---|
| `ASK.md` | the maker's ask, verbatim |
| `TASTE.md` | his design rulings, verbatim |
| `specs/` | DESIGN-SPEC, MOTION-SPEC, SIMILAR-CHANGES-PLAN, whole as of 11-06 |
| `briefs/` | the midterms design workers' briefs, as models for briefs here; `_COMMON.midterms.md` is the midterms version of the common rules |
| `research/` | W5's survey of the design field and its hierarchy study, and W11's component inventory |
| `code/` | `motion.js` (tokens and `play`; it imports two midterms modules, `live.js` and `navstate.js`, to adapt), `fitheads.js`, `Boundary.jsx`, `fitcheck.cjs`, `checks.cjs`, and the whole midterms stylesheet |
