# W12 — the details.so vault

Written 2026-11-02 by the orchestrator. Read `LAW.md`, `the-law-for-agents.md`, `RULINGS.md`, `STATE.md` first, whole. Model: Fable 5.1 (the maker's 14:49 ruling: cost is 0, use Fable where it adds benefit; this work is judgment about licence, credits and fit).

## Why this thread exists

The maker bought details.so Max (ruling 15:19) so that this site can use its components. At 15:39 he said, verbatim (RULINGS): "I want you to try accessing the page. The MCP is connected but I couldn't figure it out for this project in particular. Also keep in mind that I'd like to download or have all of the components so I need not keep the subscription other than to access NEW components in the future. Also keep in mind MCP is limited to 1000 credits per month."

The connector "Details" is connected to the account but was not switched on for the threads running at 15:39; connectors are read when a thread starts (this is why you are a new thread). If the Details tools are not in your tool list at your start, say so in your first report and stop; do not work around it.

## The work, in order

1. **Learn what a credit buys before spending one.** Read details.so's documentation with `curl -sSL` into a scratch file outside the repository (prefer `.md` or `llms.txt`); find what one MCP call costs in credits, whether listing the catalogue costs, whether a pull of one item costs one credit or more, and what the month's reset date is. Reason: the budget is 1,000 credits a month and the maker wants the whole catalogue; a count before the first call is the only way to know whether it fits in one month. Record the findings with their source URL in `research/components/2026-11-02-W12-details-vault.md` s.1.

2. **List the catalogue** through the connector (one call if listing is free or cheap; otherwise the cheapest way the docs give). Record every item: name, kind (menu, card, transition, other), licence as the terms state it, and whether it is tied to React or any library. Reason: the choice of what to pull first is made from this list, and the record is what the maker keeps if the subscription ends.

3. **Pull, in this order, into the Vault:** first the items this site can use (menus, cards and sheets, page transitions, search, reorderable lists; W11's record `research/design/2026-11-02-W11-components.md` s.1.6 names the needs; the brief first cited a wrong path, corrected 16:11 UTC), then everything else, newest last. Each item goes to `/mnt/project-files/vault/details-so/<item>/` with its files as delivered and a `SOURCE.md` (item name, URL, date pulled, licence words verbatim, credits spent). Never into git: the licence allows use, not redistribution, and the repository may be public. Reason: W11's approved plan (STATE 15:26).

4. **Stop at the budget.** Keep a running count in your research file s.3. If the whole catalogue does not fit in this month's credits, pull the site's items first and record what remains and the reset date; do not spend the last 50 credits, so that a new item the site needs tonight can still be pulled. Reason: law 8 orders the work by what the site needs; a vault that is full of unneeded items and empty of a needed one is the wrong way round.

5. **Hand over.** Tell W11 (components) and the orchestrator what is in the Vault as each batch lands; W11 adapts, W9 builds. Reason: W11 is already the judge of fit against rule 12 and the spec.

## Rules that bind you

- Rule 17: no bursts against any source; at the first refusal stop and tell the orchestrator.
- Law 7: record what the terms say, in their words, not what you take them to mean.
- Law 7a: no spending beyond the subscription already bought; free accounts and keys as needed; never commit a secret.
- Every instruction you pass on carries its reason. If one you are handed does not, say so.
- Push your research file as you go; a thread can end at any moment.
