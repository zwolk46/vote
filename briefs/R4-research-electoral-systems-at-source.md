# Brief R4: Decisiveness across electoral systems, read at source

*Written 2026-11-06 by the orchestrator. Model: **Sonnet 5.5**, effort **xhigh** (research with a clear directive, `PROJECT-INSTRUCTIONS.md`). Read `briefs/_COMMON.md` whole first; it is part of this brief.*

## Your sub-end

Establish, from the sources themselves, what a decisive vote is and how its probability is modelled under each electoral system the first pass covered, so that the model does not quietly assume a two-candidate US race.

*Why it matters:* the maker wants to show, from the chance that one vote changes an election's outcome, that an individual vote's expected benefit rarely outweighs its cost (`brainstorm/2026-11-06-transcript.md`, his words of 19:32 and 19:39 UTC). The model the site will rest on is built from these facts, and every figure the site shows must come from a named true source that was read (`CLAUDE.md`). The first pass at this topic, `research/electoral-systems.md`, was made while the network refused curl to every source, so its facts came through WebFetch extracts or were left unread. They are one grade below a read at source, and nothing may rest on them until they are re-read.

## What to do

1. **Check that curl reaches the sources.** Fetch one page from a host the first pass was refused (for example `https://sites.stat.columbia.edu/` or `https://plato.stanford.edu/`). If curl is still refused (403 at CONNECT), stop and report that at once to the orchestrator thread. *Reason:* this brief exists only because the network has been opened; without it you would repeat the first pass.
2. **Re-read at source every fact in `research/electoral-systems.md`**, with `curl -sSL` (PDFs through `pdftotext` or python), whole where the fact decides something. For each fact, mark it **confirmed** (with the URL and a short exact quote, or the page and equation number), **corrected** (give the right value and the source), or **unread** (with the reason). *Reason:* a fact decided from an extract is a guess.
3. **Fill what the first pass left unread**, from its unread list and its open questions, as far as the sources allow. The first pass reports that its WebFetch extracts often garbled formulas: re-read every formula at source, exactly as printed. Re-run each [measured] calculation in its Appendix A against the corrected formulas and say whether its result stands. Read ACE and IDEA if reachable, Myerson & Weber and Cox beyond their abstracts, and Baltz (2025) whole, reconciling his simulated values with the 1/N scale if the paper allows.
4. **Write the result** as `research/electoral-systems-v2.md`: the same sections as the first report, each fact with its new mark, then a table of every correction (old, new, source), then what is still unread and why. Keep the first report as it is. *Reason:* the record keeps what was believed and when.

## Path and constraints

- Work on your own branch from `main`, merge `main` into it if it moves, and open a pull request that adds only `research/electoral-systems-v2.md`. Push every turn. The orchestrator gates and merges (`_COMMON.md` 8).
- Scratch files go under `/tmp/` outside the repository (`_COMMON.md` 6).
- You may run subagents on Sonnet 5.5 to read sources in parallel, each with `_COMMON.md` rules 6, 7 and 13 and their reasons, but no two on the same host at once. *Reason:* parallel reading is faster; two readers on one host make a burst.
- Choose nothing for the model or the site: where sources disagree, give each with its source (`_COMMON.md` 3).

## Done when

Every fact in the first report carries confirmed, corrected or unread, the fill items are done as far as the sources allow, the pull request is open, and you have reported to the orchestrator thread in at most fifteen lines. Then stop (`_COMMON.md` 14).
