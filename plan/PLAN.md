# PLAN: how the site gets built from here

*Written 2026-11-07 03:04 UTC by the orchestrator, under law 7a: "Before the data work begins, the orchestrator records its plan in the repository and tells the maker; it does not wait for his approval." He is told, not asked. Changes to this plan are logged in `STATE.md` and made here by the orchestrator only. Every step carries its reason; a step without one is a fault to report.*

## 1. Phases

| Phase | What | State |
|---|---|---|
| 1. The standard | the model (`model/MODEL.md`) and the law (`LAW.md`) | done: model approved 02:38, law in force as if ratified 02:55 |
| 2. Data, with design alongside | every input the model needs, from true sources, and p computed for every contest; the site's design spec and options for the first screen | **now** |
| 3. Build | the site's pages, from the data and the design the maker picks | after his pick of the first screen; parts may start as soon as their data and design are settled |
| 4. Check | Fable checks every computed p against the model; cold readers read the site's words; the fit check of the design guidance on every page | as each part is built |
| 5. Ready | the maker is told the site is ready; the address, the sign-in and the share cards are his (law, open points) | last |

*Reason:* law 7a: the standard first, then the data, with design and build alongside "wherever accuracy allows". Design does not wait for data because the first screen can be drawn from figures already sourced in the model (§2 and §4 of `model/MODEL.md`); the build waits for his pick because the first screen is a surface that matters (law 9b).

## 2. Which contests, in which order

1. **The presidency, state by state, with the Electoral College stage**, from 2024 back as far as standardized sources go, the most recent first. *Reason:* the only level with published estimates of p to check our computation against (model §4), and the case most readers bring.
2. **Senate, governor and House, with control of each chamber**, 2024 and 2022 first, then back as far as standardized sources go; 2026 once its counts are certified, and before that only as an unofficial count marked so. *Reason:* the most recent cycles are the ones readers remember; 2026 was held four days ago, and its counts are not final (law 8: a figure carries its source and date).
3. **State legislatures, local races, primaries and ballot measures.** *Reason:* these are where p is largest and B\* smallest, which law 1a says the site must show; their data is the hardest to gather, so it starts as soon as a worker is free.
4. **The cost of voting**: the share voting by mail, time in line by state where measured, wages, and the tie and recount laws of every state. *Reason:* C and the tie rules enter every contest (model §6, §10).

**Every contest the sources allow** (the maker, 03:13, `RULINGS.md`: "aggregating absolutely as much data as we can find"). The volume is itself part of what the site shows. Past contests only, for now. Whether the site covers an election before it is held is an open point of the law, so nothing is built that assumes it. *Reason:* law, open points; and an ex ante forecast of a past contest is already what the model computes (law 2a).

## 3. The data: one layout for every contest

Every input lives in `data/`, as JSON, one file per contest set (for example `data/president/2024.json`, `data/senate/2022.json`). The site never fetches a third party at run time; everything it shows ships from this repository. *Reason:* law 8 (every figure with its named source and date) is checkable only if the figure and its source sit side by side in the record; and a site that fetches others' servers breaks when they change.

**A source**, wherever a figure appears:

```json
{ "name": "Pennsylvania Department of State, 2024 General Election, certified results",
  "url": "https://...", "read_utc": "2026-11-07T04:00Z", "licence": "public record",
  "mark": "measured | stated | vendor | inferred", "via": null, "note": null }
```

`via` names a compilation and `url` its origin where the compilation names one (law, Part A, true source: compilations that name their origins count, and second-hand figures are flagged, law 8).

**A contest**:

```json
{ "id": "2024-president-PA", "year": 2024, "date": "2024-11-05",
  "level": "president | senate | governor | house | state-upper | state-lower | local | primary | measure",
  "place": { "state": "PA", "district": null, "name": "Pennsylvania" },
  "result": { "certified": true, "candidates": [ { "name": "...", "party": "...", "votes": 0 } ],
              "total_votes": 0, "source": {} },
  "forecasts": [ { "by": "538 | The Economist | the model's own | ...", "published": true,
                   "share": { "mean": 0.0, "sd": 0.0, "tails": "normal | t4 | published" },
                   "p_published": null, "convention": null, "as_of": "2024-11-05", "source": {} } ],
  "population": { "value": 0, "of": "state | district | place", "source": {} },
  "stage_two": { "of": "Electoral College | Senate control | House control | ...", "inputs": {}, "source": {} },
  "p": { "value": 0.0, "event": 0.0, "under": "538", "computed_by": "pipeline/president.py", "commit": "..." },
  "notes": [] }
```

Two-candidate share is the leading two candidates' share of their combined vote, as in the model (§3). `p.event` is the chance the count without the ballot lands within one vote, twice p, always named (law 2b, model §9.2). A field may be added by a worker in its own PR with a line in `data/README.md`; a field is never renamed or given a second meaning. *Reason:* two workers fill this layout at once, and the site reads one shape.

**Computing p.** `pipeline/` holds Python (with numpy) that reads `data/`, computes p for every contest by the model's formulas, and writes the results back into each contest's `p`. It imports `model/math/common.py`, the functions the model's own figures were checked with, rather than writing them again. The site does not compute p for real contests; it reads it, and computes B\* = C ÷ p and the ballot's sum from the reader's own C. Simple mode (model §8) computes p in the page from the three facts a reader sets. *Reason:* one implementation of each formula, already checked by script and by Fable (`model/math/run_all.sh`); a second implementation would need a second check.

**The model's own forecast**, where no forecaster published one (model §3, "Which forecast"): fitted to like past races, from variables known before the election. Each data worker proposes its method for its level in its report, with a back-test on past cycles, before it computes p with it; the orchestrator approves it under the maker's word of 02:38, and the page marks the forecast as the model's own. *Reason:* the method decides every number below the presidency, so it is checked before it is used, and it stays the model's, not a forecaster's.

## 3a. Intake by script (the maker, 03:13)

Data comes in by script, not by an agent reading pages. For each standardized source (a CSV or spreadsheet release, a data repository, a documented download), a worker writes `pipeline/intake/<source>.py` once: it downloads the files to a cache outside the repository, checks them (row counts, totals against a published total where one exists), and converts them into the layout of §3, with the source block filled from the file's own metadata. Adding a year, a state or a whole source is then a run of a script. Agents spend their reading on choosing sources, on the forecasts, and on what no standardized source covers.

- **Breadth first, across sources.** Each data worker lists every standardized dataset it finds, for its level and any other, in `data/sources/<level>.md`: who publishes it, what it covers (levels, years, states, precinct or contest), its format, its licence, and whether this environment reaches it. *Reason:* one inventory lets the next worker start from what is known, and the maker's aim is everything that can be found.
- **One script per source, rerunnable.** The script and a small sample of its output are committed; the raw files are not, unless small and licensed for it. *Reason:* anyone can fetch the same files again and get the same `data/` (law 8), and the repository stays small.
- **Where two sources cover the same contest**, both are read and the differences listed; the certified source wins, and the other is the check. *Reason:* law 8, checked by another source.
- **No live data.** Nothing is fed to the site live; everything is a published dataset taken in by script (the maker, 03:13).

## 4. Who does what

At most three workers at once, plus the tracker (OPERATIONS §4; the tracker runs beside the limit at the maker's ask of 02:58, `RULINGS.md`). Models and effort from `PROJECT-INSTRUCTIONS.md`; every brief names its own.

| Brief | Work | Model, effort | Starts |
|---|---|---|---|
| `T1-tracker.md` | keeps the maker's tracker "Vote Work" current, with preview links | Sonnet 5.5, xhigh | now |
| `D1-data-president.md` | the presidency by state and the College stage; writes `pipeline/` core | Opus 5.5, xhigh | now |
| `D2-data-congress.md` | Senate, governor, House, and chamber control | Opus 5.5, xhigh | now |
| `X1-design.md` | the site's design spec, then two or three whole first-screen options on a preview branch | Opus 5.5, xhigh (max if the maker says so on the open card) | now |
| `X2-explainer.md` | how p and B\* are worked out, for a non-technical person, through visuals: a scroll-driven story, two or three versions | Opus 5.5, xhigh, in X1's thread | when X1 has sent its first-screen options (the maker, 04:06) |
| `D3-data-local.md` | state legislatures, local races, primaries, ballot measures, by script from standardized sources | Opus 5.5, xhigh | when one of D1, D2 ends |
| D4 | cost inputs, mail share, tie and recount laws | Sonnet 5.5, xhigh (clear directive, at source) | after D3 starts |
| M2 | Fable checks every computed p and the model's own forecasts against the model | Fable 5.1, xhigh | when D1's p are in |
| Build workers | the pages, after the maker's pick | Opus 5.5, xhigh | phase 3 |

*Reason:* data first because everything shown rests on it (law 7a); the presidency and Congress in parallel because they share nothing but the layout and the core; design alongside because it needs no new data; local races next because law 1a needs them most, but they wait for a free slot because usage is a real limit (OPERATIONS §4). A worker waiting on the maker's pick spends nothing, so it does not hold a slot. The explainer goes to X1's thread rather than a new one because it draws on the same ruler, dots and motion X1 has just designed, and because the maker calls it crucial (04:06): it takes X1's slot while X1 waits on his pick, so D3 waits for D1 or D2.

## 5. What goes to the maker

- This plan, as news (law 9b).
- The first-screen options, two or three whole builds on one preview link each, when X1 has them (law 9b; the design guidance, process step 2).
- The explainer's options, the same way, once a cold non-technical reader has understood them (the maker, 04:06).
- Questions only where an answer changes what gets made (law 9b). Batched now: whether to allow web.archive.org (538's archived forecast pages for past years, model §10), and whether to fill MEDSL's Dataverse guestbook with his name and email (an outside party, law 10).
- Word when the site is ready (phase 5).

The tracker shows him the rest as it happens. *Reason:* his words of 02:58, "I basically want to be able to just watch that until I have a comment that I need to make".
