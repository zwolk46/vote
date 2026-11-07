# Brief D4: The cost of voting, the share who vote by mail, and every state's tie and recount law

*Written 2026-11-07 by the orchestrator. Model: **Sonnet 5.5**, effort **xhigh**. Read `briefs/_COMMON.md` whole first; it is part of this brief. Sonnet because this is reading at source with a clear directive, and the choices that turn on judgment are already made in the model (`PROJECT-INSTRUCTIONS.md`). xhigh because every thread runs at xhigh, and max only on the maker's word.*

## Your sub-end

**Put into `data/` every input of the cost of voting, and every state's rule for a tie and a recount, each read at its source and dated, so that the site's cost and its tie rule rest on true figures in every state.**

*Why it matters:*
- **The cost.** Every break-even figure is the cost divided by p (model §2), so the cost scales every number the site shows. The default of $8.87 is 14 minutes at $38.00 an hour (model §6). The site lets each reader set their own cost, and needs measured figures beside it, by state where they exist.
- **Voting by mail.** A mail ballot has no trip and no line. That may be the case the maker's own claim sets aside ("unless the cost is basically negligible", model §6), so the share who vote by mail, by state and year, tells a reader how many voters that case covers.
- **Ties.** p counts a tie as half because a tie goes to a lot (model §3). That holds only where the law says lot. Where it says a new election or a legislature decides, p means something else, and the model says so. Eight states' laws have been read; the rest have not (model §10).

## Read first, whole

- `model/MODEL.md` §2, §3 ("ties"), §6 and §10, and `model/MATH.md` §0 and §1.1 (p under each tie rule).
- `research/frameworks-benefit-cost-v2.md` §4 (the cost figures already read, with their sources) and `research/historical-close-races-v2.md` (the tie laws already read).
- `plan/PLAN.md` §3 and §3a: the layout, and intake by script.
- `data/README.md` and `data/sources/*.md`: what the other data workers found, so you do not read a source twice.

## What to do

1. **An inventory first**, in `data/sources/cost.md` (`_COMMON.md` 4). List every standardized dataset for these inputs, with its publisher, coverage, format, licence, and whether this environment reaches it. These are leads to check, not facts:
   - the Election Assistance Commission's Election Administration and Voting Survey (EAVS): ballots cast by mode, by state and county, every even year;
   - MIT's Survey of the Performance of American Elections (SPAE): time in line, by state, 2008 to 2024;
   - the Census Bureau's Current Population Survey, Voting and Registration Supplement: how people voted, by state;
   - the Bureau of Labor Statistics: average hourly earnings, national (series CES0500000003) and by state (State and Metro Area CES);
   - Chen, Haggag, Pope and Rohla's replication data, if public, for time at the polls by state.
2. **One intake script per standardized source**, `pipeline/intake/<source>.py`, as plan §3a says. Download to a cache outside the repository, check row counts and a published total where one exists, and write the result.
3. **Write the cost inputs** to `data/cost/`:
   - the national default, each input with its source;
   - by state and year, where measured: time in line or at the polls, the hourly wage, and the share of ballots cast by mail, early in person, and on Election Day.

   *Reason:* the site shows a reader the cost in their own state, with its source, beside the default.
4. **Every state's tie and recount law**, for the 50 states and DC, in `data/law/ties.json` and `data/law/recounts.json`. For each:
   - what a tie triggers, by kind of office (federal, state, local, primary): a lot, a new election, a vote of the legislature, or something else;
   - the automatic recount threshold, and who may request one and at what margin;
   - the statute or constitution's citation, its URL at the state's own legislature or code site, and when you read it.

   Read each at the state's own code. A secondary summary (NCSL, Ballotpedia) may point you to the citation, but the text you record is the statute's own. Where a state's code cannot be reached, record the state as unread, with the reason. *Reason:* law 8, true things from true sources; and a summary of a law is not the law.
5. **Report** in `data/cost/REPORT.md`: what each source gives, what is measured and what is not, and how the site's default of $8.87 compares with the state figures.

## Path and constraints

- **Branch and pull requests.** Work on your own branch from `main`; push every turn. One pull request for the tie and recount laws, and one for the cost inputs.
- **Your files.** Touch only `data/cost/`, `data/law/`, `data/sources/cost.md`, your intake scripts, and new fields in `data/README.md`.
- **Figures.** Take no figure from memory (OPERATIONS §3). Mark every fact [measured], [stated] (with where), [vendor claim] or [inferred] (`_COMMON.md` 5).
- **Network.** web.archive.org is refused. If a host is refused, record it and tell the orchestrator; do not route around it (`_COMMON.md` 6). At most one request every few seconds to one host (`_COMMON.md` 13).
- **Outsiders.** Nothing bought. A dataset behind a sign-up that asks for the maker's name or email is his call (law 10): list it, and do not fill it in.

## Done when

1. Every source in the inventory that this environment reaches and its licence allows has an intake script.
2. The cost inputs are in `data/cost/`.
3. Every state's tie and recount law is recorded with its citation, or marked unread with the reason.
4. The pull requests are open, and you have reported to the orchestrator in at most fifteen lines.

Then stop (`_COMMON.md` 14).
