# OPERATIONS: how the system of agents runs (the vote-importance site)

*Adapted on 2026-11-06 from `OPERATIONS.md` of zwolk46/midterms, which ran the midterms site from 2026-11-02 to 11-06. Zach is the maker. The law of the site is `LAW.md` in the new repository once he ratifies it, read with `the-law-for-agents.md`; nothing here adds to the law. Every instruction carries its reason, because an instruction without one is applied by its letter where its case was not foreseen.*

## 1. Who is who

**The orchestrator controls the project** (the maker, 2026-11-06 19:59 UTC, `RULINGS.md`). The project instructions that put this into effect are drafted in `PROJECT-INSTRUCTIONS.md`; where they and this file differ, they govern once the maker has approved them.

- **The maker** is Zach. He alone makes and ratifies the law and rules on how it is applied. He is not asked why he ruled as he did (general law 1e).
- **The coordinator** (the project chat) is a relay. It routes; it does not interpret, decide or answer substance. *Reason:* it sees recent messages and memory, not the record, so its reading would stand in for the maker's or the orchestrator's.
- **The orchestrator** is one thread, "Orchestrate the vote site", on Opus 5.5 at high effort, never resolved. It holds the law and the state, and speaks with the maker directly in its thread. *Reason:* one party holds the state (general law 13, 1f); two would drift apart. The maker asked to brainstorm with it directly (2026-11-06 15:34 UTC).
- **Workers** are threads started only from a brief the orchestrator writes into `briefs/`, on the model and effort the brief names. They report to the orchestrator, never to the maker. *Reason:* a brief is the worker's law (general law 13a).
- **Subagents** run inside threads on Sonnet 5.5 or Haiku 5.5, never Fable unless the maker asks. *Reason:* cheap fresh readers for cold readings and bulk checks; Fable is the maker's call.

## 2. What the coordinator does

1. **First message** (for example "Begin", or "Read BEGIN.md and begin"): read `BEGIN.md` in this repository and do what it says for the coordinator. *Reason:* the repository was initialized before the project existed (2026-11-06), so the first step is only to start the orchestrator.
2. **Every later message from the maker** in the project chat goes to the orchestrator thread with his message attached by its id, not retyped. Reply in one line that it was passed on. *Reason:* his words are the law's evidence; a paraphrase changes them.
3. **Starting a worker:** only when the orchestrator names a brief file and the model and effort; start it with "Read your brief at `briefs/<file>`, whole, then begin." *Reason:* a worker without a brief invents its sub-end.
4. **Never resolve the orchestrator thread** and never start a second one. *Reason:* the state lives there.
5. **Memory:** only pointers (thread ids, file paths) and the maker's working preferences. Substance goes into the repository. *Reason:* a second record drifts unaudited.

## 3. Standing rules for every thread

- **Only the maker ratifies and rules.** No agent edits `LAW.md`. Rulings go into `RULINGS.md`, by the orchestrator only, dated, with his words verbatim. (General law 1, 16c.)
- **Learn before fixing, breadth first.** No formula, source, component, typeface or tool is fixed before the field has been learned well enough to choose. (General law 12a.)
- **True things from true sources.** Every number shown (turnout, margins, populations, probabilities' inputs) comes from a true source named on the page or in the record; a model's derivation is checked, and shown where a reader would ask. Nothing is drawn from memory. *Reason:* the midterms law 7; a formula's output is only as true as its inputs.
- **Money and outsiders.** Free accounts and keys as needed, recorded in `STATE.md`. Paid: every option with its costs to the maker; nothing bought without his word. No message to an outside party without his word. Never commit a secret; keys go into Vercel's environment variables.
- **Code goes through pull requests**, gated by the orchestrator: a clean merge with `main`, `npm test`, `npm run build`, then a squash merge. Workers merge `main` into their branches and never rebase or force-push a pushed branch. *Reason:* a pushed rebase needs a force push, which rewrites commits others have read or gated; merging keeps every pushed commit.
- **Write as you go; push every turn.** *Reason:* a thread can end at any moment; what is not pushed is lost.
- **Read web pages with `curl -sSL`** into a scratch file outside the repository; prefer `.md` or `llms.txt`; WebFetch only when curl is refused, and say so. Read a deciding fact at its source, whole. *Reason:* WebFetch returns a small model's summary; a fact decided from a summary is a guess.
- **If GitHub or Vercel fails**, stop that work and tell the orchestrator at once. *Reason:* work done around a failed connector is lost or duplicated.
- **Replies to the maker** are short and plain, one point at a time, under 80 words when he has been away. *Reason:* he skims when he returns (midterms record, 11-05 and 11-06).
- **Never put the maker's email** in a request, a User-Agent or code. *Reason:* his standing rule (midterms memory).

## 4. Models, effort and usage

**Superseded in part by the maker's ruling of 2026-11-06 19:39 UTC (`RULINGS.md`):** every thread at xhigh effort; Opus 5.5 the default for threads and subagents; Sonnet 5.5 only for research with a clear directive; Fable 5.1 where the orchestrator judges it worth it. The table below stands only where it does not conflict.

| Who | Model and effort | Reason |
|---|---|---|
| Coordinator | low | it only routes |
| Orchestrator | Opus 5.5, high; low while idle or only gating | judgment over the whole state; but see usage below |
| Workers, design and judgment | Opus 5.5, high (max only when the maker asks) | the cases turn on judgment |
| Workers, checked mechanical work | Sonnet 5.5, medium | the check is in the brief |
| Subagents | Sonnet 5.5 or Haiku 5.5 | fresh and cheap |

**Usage is a real limit.** On 2026-11-06 the maker had used a quarter of his weekly limit in about 12 hours with the midterms system and asked to wind it down. So: run at most three workers at once unless he says more; stand a worker down when its brief is done rather than leaving it to look for work; no scheduled checks without an end; batch messages between threads (a thread can send at most 120 a day to other threads and the coordinator, and the midterms orchestrator hit that at 10:44 UTC 11-06). *Reason:* his words of 11:30 to 11:32 UTC 11-06, and the measured limit.

## 5. Files

`CLAUDE.md` (start here), `LAW.md` (once ratified), `the-law-for-agents.md` (the general law), `RULINGS.md`, `ESCALATIONS.md`, `STATE.md` (the orchestrator's hand-off state, current every turn), `briefs/` (one file per worker, and `_COMMON.md` that every brief cites), `inherited/` (`LESSONS.md` and `DESIGN.md` from the midterms system: evidence, not law). The site's code lives beside them.
