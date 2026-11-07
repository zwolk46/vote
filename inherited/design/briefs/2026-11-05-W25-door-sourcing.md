# W25: find the door's real components (sourcing, not building)

Written by the orchestrator at 21:10 UTC on 11-05. Read these first:
- `LAW.md`, `the-law-for-agents.md`, `RULINGS.md` (whole), `STATE.md` and `briefs/_COMMON.md`;
- `research/plan/2026-11-05-A-maker-principles.md`, his taste with his own words;
- `briefs/2026-11-05-W18-door.md`.

Model: Opus 5.5, max effort. *Reason:* the maker asked for more depth than the last plan had (21:03), and he calls the door the site's most deliberate page (18:35).

## The case

The maker, 21:03 UTC on 11-05 (verbatim in RULINGS.md):

> So there's a danger here. Because it's so design specific and each component has to be absolutely perfect, I've noticed that making your own components is hardly ever the best thing to do. So I don't even want you to come up with the ideas yourself. I don't think the orchestrator should. I think another agent should, after receiving like guidance on what the principles behind why we would include something or something like that, and then it should go through the sites, MCPs, and connectors I have access to and pull actual components. So I think like 21st.dev is great. Details.so has real components. Mobin has screens, so you can take ideas from like the flow or the screen or something like that and how maybe a scroll works. But I want you to think even more deeply about this than you did, because I'm not sure enough time was put in before a plan was fixed. So take this autonomously.

At 21:00 the orchestrator had planned a picker of three heroes and four backgrounds. The builder (W18) was going to invent most of them. **That plan is withdrawn.** You are the agent he describes.

Your output is a sourced catalogue and a reasoned shortlist. It is not code for the site.

W18 builds only what comes out of your work. W18 has been told to stop inventing variants and to keep only neutral work:
- its fixes;
- a preview-only switcher (`?hero=&bg=`);
- a slot API for dropping a found component in.

## What the door is for, and why something earns a place

These are principles and their reasons. They are not designs. Each comes from a ruling you can read in RULINGS.md.

1. **Coolness first, and it must be the best page on the site.** The door is the first thing a stranger sees. (19:09 "one of the primary goals is actually coolness"; 18:32 "visually the most excellent page to ever exist on the site".)
2. **Large, loud, deliberate, in sequence.**
   - Each element appears on purpose, in turn.
   - The hero plays alone first.
   - Nothing snaps at the end.
   - There is always some latent motion.
   - Scrolling drives animation: for example, the dots scatter out, up and to the sides, and the logo pulses or shimmers. That is his suggestion, not a requirement. Find what real sites do.

   (18:25; 16:23; 20:58.)
3. **It shows what the site does, with election-specific content.** That means the House and Senate picture, races, the map and the desk reader. Use showpieces made for the door, not screenshots of the site (18:32, 19:09).
4. **No party leaning.** Use red, white and blue together, never red alone. It is "just a data displayer, it's not right or left" (20:58).
5. **True things only (law 7).**
   - Dots that look like seats never settle in a party's colour and never read as a count, unless they are the real count with its time.
   - Any figure shown comes from the site's feeds, or is plainly marked as a sample.
   - Nothing members-only appears.
6. **The form comes first on the phone.** Someone with a passcode never scrolls past the showcase to use it. The first name, passcode and Enter controls are "very deliberate" real controls (18:32, 20:58).
7. **Real components beat home-made ones.**
   - He praised what was real and perfect on its first run: the Details Morphing Navigation and Reveal Navigation, the Cupertino Pane, and the 21st glass reveal he chose himself (17:47).
   - He criticised invented UI, stock icons and generic "AI tells": glows, pulsing dots that mean nothing, filler text.

   See the principles file, sections 1, 2a and 2d.
8. **The page's limits.**
   - Scripts run under the per-request CSP nonce, with no third-party script hosts.
   - The page works without script.
   - It stays fast.
   - It honours reduced motion.
   - It fits from 320 to 1440 px wide, and at 2× text (W23's fit check).

   A candidate that cannot meet these limits, even after a faithful port, is out. Say why.

## The job, in phases

Work in phases (P-19 in designsystembrain). Push your file at the end of each phase. *Reason:* the thread can end at any time, and the maker reviews the direction.

1. **Ground.**
   - Read the record above.
   - Read the door as it stands: production `lib/gate/page.js` and `lib/gate/glass.js`, and W18's preview. Ask the orchestrator for W18's notes on what worked and what the glass costs.
   - Read what earlier workers already searched: `research/design/2026-11-02-W5-*`, `2026-11-02-W11-components.md` and the W18 thread's research file.
   - Write down the door's **slots**. Each slot is a role a component could fill: the hero mark, the background or field, the scroll sequence, the latent motion, the form controls, the feature showpieces, and the transition into the site. Add any other slot you find real sites using.
   - Write the selection criteria for each slot **before** searching, from the principles above. *Reason:* criteria written after seeing the candidates bend to fit a favourite.
2. **Search wide, in every source he has.**
   - **21st.dev** through its MCP or API (key in env as `API_KEY_21st`; never print it). Use `search` freely. Use `get_component` only on finalists, because the free installs are limited. Never use `generate` (paid credits). Mobbin's deep mode is allowed and wanted (maker, 22:07); stop it only at a rate- or credit-limit notice.
   - **Details**:
     - `search_inspirations`, then `get_inspiration` for the finalists;
     - `search_vault` and `get_vault_resource` for its real components.
   - **Mobbin**: `search_screens`, `search_flows` and `search_sections`. Look at sign-in, onboarding, launch and splash screens, and scroll-driven landing pages, from data and news apps and from the best consumer apps. Take ideas from the flow, the screen and the scroll, never the look of a brand.
   - Look also at award-site scroll landings you can reach with `curl` or a shallow clone, such as public repositories of the components you find.

   Run many queries per slot, at least ten, in different words. Log every query and every candidate seen, kept or rejected, with a one-line reason. *Reason:* the log is what shows the depth he asked for, and it lets the next agent continue.
3. **See each finalist running.**
   - Open the real demo, using Playwright with its frames or a recording.
   - Measure what matters: bytes, frame time on a phone profile, CSP fit, how it behaves under reduced motion, and whether it can carry the site's three colours.
   - Store shots and short recordings in `/mnt/project-files/design/door-sourcing/`.
   - Rate each one against the slot's criteria. *Reason:* a still from a catalogue hides snapping and jank. He caught both on the glass.
4. **Shortlist and present.**
   - For each slot, give two to four sourced candidates. Each one comes with:
     - its source link and licence;
     - a recording;
     - how it would carry the door's content and colours;
     - its cost in bytes and effort;
     - what a port would have to change, kept to the minimum, because a heavy adaptation is a home-made component again.
   - Then give one or two **whole-door combinations** that cohere, each with a reason, as recommendations only. *Reason:* the maker picks (21:00 "select between different components"). Details' own rule is to present options and let the person choose.
   - Build a viewing page where he can see the candidates running as found: a preview on `probe/door-sourcing` (Vercel) or a claude.ai artifact, whichever shows them more faithfully. Give the orchestrator the link.
   - Do not build the door.

## Where things go

Record:
- `research/design/2026-11-05-W25-door-sourcing.md` on your thread branch, pushed after each phase: slots, criteria, the query log, candidates and shortlist.

Report to the orchestrator thread:
- after phase 1, the slots and criteria, so the direction can be corrected early;
- after phase 4, the shortlist.

Do not message the maker; the orchestrator relays.

## Answers given (21:25 UTC)

- A pause control is a plus, not a bar. Reduced motion must be honoured. The choice goes to the maker with the shortlist.
- The passcode is of variable length; no field with one box per character.
- A change to the policy or matcher is a cost to name, not a bar.

## Rules that bind you

- Read web pages with `curl -sSL` into a scratch file outside the repository and search them. Use WebFetch only if curl is refused, and say so.
- Spend no money and no AI credits.
- Never write the passcode or any key to a file. If you need the passcode for a preview, read the maker's message `cmsg_012gZsfgtrnEcQeCcujWaxp337WSF4ftSfcvhjDFMAy4hF` with `read_messages_by_id` and use it only as an env var at run time.
- Do not recreate a brand's look. Take the mechanism, not the identity. *Reason:* trade dress belongs to its owner, the site needs its own identity, and the standing rule forbids recreating another product's look.
- Subagents run on Sonnet or Haiku, and their briefs carry these rules.
- If a connector you depend on fails (21st, Details, Mobbin, GitHub, Vercel), stop and tell the orchestrator at once.
