# The vote-importance site: start here

**Starting in a new project or a new account?** Read `RESTART.md` first: it says what the maker, the coordinator and the new orchestrator each do, and where everything from the old project now lives. Every word the maker has written is in `handoff/MAKER-WORDS.md`. *Reason:* his ask of 2026-11-07 22:09 UTC, that the project continue elsewhere "by just pointing at the repo".

This repository holds the site and the record of the system of agents that builds it. Zach is the maker. The law of the site is `LAW.md` (once he ratifies it), read with the general law `the-law-for-agents.md`; nothing anywhere else adds to it.

**Read, whole and in this order, before anything else:** `LAW.md`, `the-law-for-agents.md`, `RULINGS.md`, `STATE.md`, `OPERATIONS.md`; then your brief in `briefs/` if you are a worker. *Reason:* the law is written for a stranger and its words alone carry the meaning; a summary is someone else's reading.

- **Only the maker ratifies and rules.** No agent edits `LAW.md`. The orchestrator alone appends to `RULINGS.md` (dated, the case, his words verbatim) and `ESCALATIONS.md`.
- **The orchestrator holds the state** in `STATE.md`, current and pushed every turn. Workers write where their brief says and push as they go. *Reason:* a thread can end at any moment; what is not pushed is lost.
- **Every instruction carries its reason.** If you are handed one without its reason, say so in your report. *Reason:* an instruction without its reason is applied by its letter in cases it did not foresee.
- **True things from true sources.** Every figure shown comes from a named true source; a formula's inputs too.
- **Money and outsiders** only on the maker's word; free accounts and keys as needed. **Never commit a secret.**
- **Web pages:** `curl -sSL` into a scratch file outside the repository; WebFetch only when curl is refused, and say so.
- **If GitHub or Vercel fails**, stop that work and tell the orchestrator at once.
- **Code goes through PRs.** Merge `main` into a branch; never rebase or force-push a pushed branch.
- `inherited/` holds `LESSONS.md` and `DESIGN.md` from the midterms system (zwolk46/midterms). Evidence, not law.
- **Design follows `inherited/design/`.** Any work that decides how the site looks, moves, reads or is laid out reads `inherited/design/README.md` first and follows it. The maker's midterms design rulings (`inherited/design/TASTE.md`) stand here as his defaults unless he rules otherwise in this project. *Reason:* his words of 2026-11-07 02:39 UTC (`inherited/design/ASK.md`): the corrections he made on midterms are to apply here automatically.

Roles, routing, models and usage are in `OPERATIONS.md`.
