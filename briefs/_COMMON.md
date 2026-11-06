# What every worker brief shares (cited by each brief; read whole)

*A brief cites this file rather than restating it, so a change here reaches every worker at once. Adapted from zwolk46/midterms `briefs/_COMMON.md`. Every rule carries its reason; if one does not, say so in your report.*

1. **Read first, whole:** `CLAUDE.md`, `LAW.md`, `the-law-for-agents.md`, `RULINGS.md`, `STATE.md`, this file, then your brief. *Reason:* the law's words alone carry its meaning.
2. **Your brief is your law**: it states your sub-end and why. Where it is unclear on a small point, read it the way that best serves the sub-end; otherwise escalate to the orchestrator. *Reason:* an agent fills a gap with a confident guess unless told where to look.
3. **You choose nothing for the site** unless your brief says so. Bring candidates, each with what it gives toward the end, its costs, its licence and its evidence. *Reason:* choices are the orchestrator's and return to the maker in the plan.
4. **Breadth first, then narrow.** *Reason:* a model is confident on little context and cannot know, without searching, whether more exists.
5. **Mark every fact** [measured], [stated] (with where), [vendor claim] or [inferred]. *Reason:* the orchestrator must know which facts are true things from true sources.
6. **Web pages:** `curl -sSL` into a scratch file outside the repository; prefer `.md` or `llms.txt`; a shallow `git clone` for a repository; WebFetch only when curl is refused, and say so. A page behind a bot check is recorded as unread and not circumvented. *Reason:* WebFetch returns a summary; getting around a site's refusal is not ours to do.
7. **Money and outsiders.** Free accounts and keys as needed, recorded in your report. Paid options: read every published price; do not contact the seller. No message to any outside party, no post, no purchase. *Reason:* a message to a seller is a message in the maker's name.
8. **Code goes through a pull request** from your own branch. Merge `main` into it; never rebase or force-push a pushed branch, never amend a pushed commit. The orchestrator gates and merges. *Reason:* other threads read your branch while you write it; a rewritten history loses what they read, and a pushed rebase needs a force push.
9. **Write where your brief says; push every turn.** Touch only your own files. *Reason:* a sandbox can be lost between turns.
10. **Report to the orchestrator** by message, in at most fifteen lines: what you found or built, the path or PR, what you could not do and why, your questions. Batch: one report per result, not per step. *Reason:* the orchestrator holds the state, and a thread can send only about 120 messages a day to other threads.
11. **Escalate to the orchestrator, never to the maker.** Keep working on what the question does not block.
12. **Subagents** on Sonnet 5.5 or Haiku 5.5, never Fable; give each rules 6 and 7 with their reasons. *Reason:* a subagent knows only its prompt.
13. **No bursts against a source:** at most one request every few seconds to one host, and stop at the first refusal (403, 429, a challenge). *Reason:* a source that blocks us is lost (midterms, 11-02: Clarity blocked a sandbox after about 40 requests in a minute).
14. **Stop when your brief is done**, report, and start nothing new without the orchestrator's word. *Reason:* the maker's usage limit (11-06); an idle worker looking for work spends it.
15. **Never put the maker's email** in a request, a User-Agent or code.
