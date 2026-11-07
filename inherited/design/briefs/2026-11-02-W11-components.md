# W11: components from the field, and a page to preview them

*Brief written by the orchestrator, 2026-11-02 14:47 UTC, on the maker's ruling of 14:40 UTC (`RULINGS.md`). Read `briefs/_COMMON.md` first; it is part of this brief, except items 3, 9 and 12 where this brief says otherwise.*

**Model and effort: Opus 5.5, high.** *Reason:* which components fit this site is a judgment of fit and quality (law 1a, 4, 5; `OPERATIONS.md` 4), and the maker may spend money on the answer.

## Your sub-end

1. **A preview page** of real components pulled directly from good component sources online, each shown working, in the site's colours and type and with its real content (seat counts, a race row, a call, a state card, the countdown, the menu, search), so that the maker can see and choose.
2. **A short written answer** on what to buy, if anything, with prices and licence terms read at the source. details.so's top tier comes first, then anything else worth paying for.

*Why this is a condition of the end:* the maker asked for it (14:40 UTC: "preview a page with components pulled directly from online … find the best tailored components … I might be open to buying more"; 13:08 UTC: "I don't feel like I'm seeing lots of components taken directly from sites with nice prebuilt components"). Law 1a asks for the best in beauty and ease, and law 7a puts every paid choice before him with its costs and benefits.

## Constraints

- **details.so first.** Before the maker buys:
  - Read details.so's pricing, its licence and terms, and what the top tier ("Max", or whatever it is called) delivers: code or design files, framework, how it is downloaded, whether it may be used on a public site and kept after the subscription ends, and whether more than one person may use it.
  - Say plainly whether it fits Vite and Preact (React code needs `preact/compat`: measure the weight that adds) and what it would give this site that it has not got.
  - Say how the maker can hand it over without a password reaching an agent or the repository. For example, he downloads the files and uploads them to the project, or adds the files to the repository himself.

  *Reason:* law 7a (the price and the licence are deciding facts, read whole at the source); `CLAUDE.md` (never commit a secret).
- **Search far and wide** (`_COMMON.md` 4). The kinds of source are:
  - libraries of copy-in components, such as shadcn/ui and its registries, 21st.dev, Origin UI, Magic UI, Aceternity, Motion Primitives, React Bits, Tremor and others;
  - headless primitives, such as Zag (already adopted), Ark, Radix, Base UI and Headless UI;
  - paid collections, such as details.so and others;
  - specialist pieces for this site: seat bars and hemicycles, results tables, maps, countdowns, timelines, search palettes (for example cmdk), drawers and menus.

  W5's survey (`research/design/2026-11-02-W5-design-field.md`) is evidence to check, not a limit.
- **Fit before beauty alone.** Every candidate must meet these conditions:
  - It runs under Preact, natively or via compat with its weight measured.
  - It fits the budget: the first view under 300 KB compressed on a phone, JavaScript about 100 KB (W6 s.6). JS is about 40 KB gzip today.
  - It has a licence that allows a public site.
  - It obeys the decided cases: no hover glows, no drop shadows between cards, no moving arrows, no pulsing dots, no scrolling text, no filler text (`RULINGS.md`).
  - Its motion is reconciled with `research/design/motion/MOTION-SPEC.md`: say where its built-in motion differs.

  *Reason:* law 2, 4, 5, 7a; the decided cases (general law 1d).
- **Free accounts** as needed (law 7a). No purchase and no message to any outside party (for example a vendor's sales address). *Reason:* law 7a.
- **The preview page.** Put it on branch **`probe/components`**, as `components/index.html` plus one page per surface or a single page.
  - No framework build is needed if the components can be shown standalone. If they need a build, keep it inside `components/` with its own `package.json`, and never touch the site's own files.
  - Vercel builds `probe/*` branches. The preview is open without login since 14:25 UTC at https://midterms-git-probe-components-zachs-projects-74dd78e7.vercel.app/components/.
  - Label each component with its source, licence, price (or free), weight under Preact, and the surface it would serve.
  - Show figures from `src/fixtures/` or invented figures, with a one-line banner saying the figures are for display only.

  *Reason:* the maker wants to look and choose; a probe branch keeps the site's build untouched (one writer per file); law 7 (shown figures must not pass for results).
- **You choose nothing for the site** (`_COMMON.md` 3): you recommend one component per surface, with alternatives and evidence. The orchestrator puts the choices to the maker. *Reason:* law 6b; the maker chooses what he buys.

## The path fixed for you

1. **details.so** (pricing, licence, delivery, fit, hand-over). Report it by **15:30 UTC**, because the maker is ready to buy now.
2. **The field, breadth first**, then the best two or three candidates per surface. The surfaces are those of DESIGN-SPEC s.11, plus search (the maker's 14:40 ruling: candidates, states, districts and more).
3. **The preview page**, best candidates first, by **18:00 UTC**.
4. **The written answer:** `research/design/2026-11-02-W11-components.md` (the field, the candidates, licences, prices, weights, and recommendations), kept on `main`.

## Report and escalate

As `_COMMON.md` 10 and 11. Report times are 15:30 UTC for details.so, and 18:00 UTC for the page and the written answer. After that, keep deepening what the orchestrator names. Questions for the maker go to the orchestrator, who asks them. *Reason:* law 6; the maker gets one voice (`OPERATIONS.md` 1).

## Addition (orchestrator, 2026-11-02 14:49 UTC): true menus, cards and transitions

The maker added this at 14:41 UTC: "some of the things I want are TRUE menus and cards, and TRUE transitions, like human-made and human-perfected".

**Menus, cards (the phone's bottom card and sheets) and page transitions come first among the surfaces.** For each of them, find the components whose motion and behaviour were made and tuned by people and published as they are. Examples to check are Vaul (Emil Kowalski), the drawers and menus of details.so, Radix and Base UI, Motion's own examples and the View Transitions patterns, together with others you find. Show each one on the preview page **with its own motion unchanged**, beside what the site has now: Zag's drawer under MOTION-SPEC values, W9's build on build/site.

For each one, give:
- its weight under Preact;
- where its motion differs from MOTION-SPEC;
- whether it keeps rule 12 (press to motion under 150 ms on a 4x-throttled phone; W8's latency.check).

Vaul was rejected at 13:31 UTC (about 26 KB, needs compat, README says unmaintained). Check that again, at the source.

*Reason:* the maker's words. A component built by agents to imitate a crafted one is what he has ruled against. Where the spec and a crafted component's own motion disagree, the orchestrator decides with both in view.
