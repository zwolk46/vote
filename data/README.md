# data/: the layout, and every field added to it

*The layout is the orchestrator's, `plan/PLAN.md` §3; this file records it, and every field a worker adds, by level. A field is never renamed or given a second meaning (plan §3).*

## The layout (plan §3, as written there)

**A source**, wherever a figure appears:

```json
{ "name": "...", "url": "https://...", "read_utc": "2026-11-07T04:00Z", "licence": "public record",
  "mark": "measured | stated | vendor | inferred", "via": null, "note": null }
```

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

`share.mean` is the Democrat's (candidate A's) share of the two-party vote. `p.event` is twice `p.value`, the chance the count without the ballot lands within one vote, always named (law 2b).

## Fields added by D2 (Senate, House, governor; `data/senate/`, `data/house/`, `data/governor/`)

**At the top of a contest file**
- `sources`: source blocks (plan §3 shape) named by key. The fields below that end in `_source`, and `checks[].against`, hold one of these keys rather than repeating the block in every contest.
- `missing_from_record`: contests the check source has and the source of record does not (mostly special elections held on other dates).
- `model`: the fitted terms of the model's own forecast used in the file: method version, years fitted, `b_lean`, `b_inc`, `s_e` (the race's own sd), `national_forecast` and `national_sd` (the year's swing and its sd), `rho`, and the commit.
- `chamber`: control of the chamber for the year. It holds the rule (`218 of 435`; `51, or 50 with the Vice President`), the seats modelled and fixed, `seats_not_up` by caucus, `vice_president` (P that the VP is a Democrat, with a `mark`), the expected Democratic seats, and the sds.

**In each contest**
- `special`: true for a special election, which fills the rest of a term.
- `two_party`: the two leading candidates, their votes, `n_other_voters` (their combined vote minus one: the n of model §3), and `share_first`.
- `ballot`: who was on the ballot. It gives the counts of Democratic (`D`) and Republican (`R`) nominees, the independents who caucus with the Democrats (`caucus_D`), and `others`. It is known before the election and decides how a seat the model does not compute enters control.
- `forecast_inputs`: what the model's own forecast is built from.
  - `lean`: the district's or state's Democratic two-party share in the presidential election before the race, minus the national share.
  - `pres_year`, `district_share_D` or `state_share_D`, `national_share_D`.
  - `incumbency`: +1 if a Democratic incumbent runs, −1 if a Republican one does, 0 otherwise.
  - `midterm`, `president_party`, and each one's `_source` key.
  - `lean_missing`: why there is no `lean`.
  - `lean_same_day`: the same day's presidential vote on the lines, marked inferred. It is used for control only and never for the seat's own p.
- `checks`: the same contest in a second source (`against`) and every difference between the two (plan §3a). The source of record wins.
- `forecasts[].method`: the version of the model's own method (`D2-v1`). `forecasts[].share.of` names whose share the mean is (`Democrat, two-party`).
- `p.not_computed`: why p is not computed (a structure the model does not compute yet, or a missing input); `null` when it is. `p.reason`: why p is 0 (one candidate). `p.method` (`exact` or `density`), `p.f_half` and `p.n` are pipeline/core.py's own outputs.
- `p.alongside`: p under the other tails (t4 with the same sd), with its own `event`.
- `p.control`: p for control of the chamber, which is p × `stage_two.inputs.P_decides_given_tie` (MATH §4.2), with its `event`.
- `stage_two.inputs`: how the seat enters control.
  - `entered_as` is `model`, `inferred` (the model's two-way forecast for a structure whose p is not computed, marked) or `fixed` (settled by who was on the ballot, never by the result).
  - `P_decides_given_tie` and `P_decides_unconditional` (what the usual shortcut would use).
  - In presidential years for the Senate, the same given a Democratic or a Republican Vice President.
- `stage_two.note`: why a contest is not part of control (a special that fills the old Congress's term).

## Fields added by D1 (the presidency; `data/president/`)

### Files


| Path | What | Written by |
|---|---|---|
| `data/president/<year>.json` | every presidential contest of that year, 1976 to 2024, one per state and one per Maine or Nebraska district where its count was read | `pipeline/president.py` |
| `data/president/inputs/*.json` | each standardized source, normalised, with its source blocks; the only thing `president.py` reads | `pipeline/intake/<source>.py`, one per source; MEDSL's and the National Archives' pages are D2's scripts, run as `medsl_dataverse.py president_detail` and `nara_electoral_college.py states` |
| `data/president/own_forecast_backtest.txt` | the back-test of the model's own forecast | `pipeline/own_forecast.py` |
| `data/president/REPORT.md` | sources, method and checks for the presidency | D1 |
| `data/sources/president.md` | every standardized dataset found, for any level, and whether this environment reaches it | D1 |

### Fields

**Source block**
- `sha256`: the SHA-256 of the exact file read. *Reason:* a figure's source is checkable only against the same bytes (law 8); URLs change content.

**File** (`data/president/<year>.json`): `about`, `year`, `computed_by`, `commit` (the commit of the code that wrote it), `summary` (`vote_weighted_mean_p`: the average voter's p over the states, weighted by two-party vote; `one_in`; `top`: the five states with the highest p; `states_with_p`), `contests` (the list).

**`result`**
- `two_party`: the two major-party nominees' votes combined. *Reason:* n, the other voters, is this less one (model §3).
- `dem`, `rep`: the nominees' votes in the count of record, repeated for the computation.
- `check`: the other source's figures for the same contest (`by`, `dem`, `rep`, `total`, the differences `dem_diff`, `rep_diff`, `total_diff`, other minus record, and its `source`). *Reason:* plan §3a: where two sources cover a contest both are read, the differences listed, the certified source wins.
- `candidates[].from`: "MEDSL" where a candidate other than the two nominees comes from MEDSL's list (the FEC workbooks used carry only the nominees); `candidates[].writein`: true where MEDSL marks every line of the candidate a write-in.
- `leading_two_not_nominees`: true where the two leading candidates were not the two major-party nominees (Maine and Utah in 1992). *Reason:* the model's two-candidate share is the leading two (plan §3); these contests are computed on the nominees and say so.
- `not_candidates`: rows MEDSL reports that are not candidates (blank, void, scattering, over- and undervotes), kept apart and never ranked.
- `note`: for a district, what the count does and does not include.

**`population_nation`**: `{value, of: "nation", source}`, the nation's population in the same year. *Reason:* the law's per-person reading names the jurisdiction the office serves, which for the presidency is the nation; the brief names the state's. Both are given, so the site can show either.

**`population.note`**: why a value is missing (district populations are not gathered yet).

**`forecasts[]`**
- `model`: 538's model name where it ran several (2016: polls-plus, polls-only, now-cast; 2020: polls-plus).
- `win_prob`: the forecaster's chance that the Democrat wins the unit, as published (538's made two-party: its Democratic chance over the sum of the two nominees' chances).
- `share.mean_mark`, `share.sd_mark`, `share.sd_how`: how each was obtained (stated, measured from draws, or inferred, and how).
- `share.low`, `share.high`: the Economist's published interval (the 2.5% and 97.5% points of its draws, measured).
- `share.sd_rel_error`: for 538, the estimated relative error of the sd its mean and chance imply (`value`), from the chance's sampling error (`from_chance`, `chance_se`, with `runs`, the simulation runs its printed chances count, and `runs_mark`, how that was inferred) and the rounding of the printed shares (`from_mean_rounding`, `mean_rounding`); `null` where unbounded. *Reason:* the orchestrator's rule of 2026-11-07 04:20 keeps 538's sd only where this is under 20%; where it is not, `share.sd` is `null`, `share.sd_how` says why and which sd the College stage used, and the contest's `p` is the model's own, marked in `notes`.
- `share.national_sd`, `share.state_sd`: for the model's own forecast, the two error sds whose sum of squares is `share.sd`; its `tails` is "normal national error + t4 state error".
- `unit_ev`: the electoral votes the unit's count decides in that forecaster's model (2 for Maine's and Nebraska's statewide count where districts are modelled; 4 or 5 where the forecaster treats the state whole).
- `p`: the p under this forecast, in the same shape as the contest's `p` (below). *Reason:* model §3, "where two forecasters published, the page shows both"; the contest's own `p` is the one shown first.
- `p_bound`: where a forecaster's draws are too few to fix p (the Economist, safe states in 2020), the 95% upper bound under its draws, `p_upper`, `one_in_at_least`, the draw counts and a note; `p` is then null.
- `note`: why a forecast carries no p (538's 2008 and 2012 files have chances only; 538's implied sd breaks down at that unit), or that its date is Election Day itself (538's 2008 file has no other).
- `as_of` for 538: the date of the forecast used, the last dated before Election Day (the orchestrator's rule of 04:12).

**`p`**
- `one_in`: 1 ÷ value, rounded.
- `p_state`: the first stage, the chance the unit's count is tied (our convention, a tie counted half).
- `W`: the second stage, the chance the unit's electoral votes decide the College given that tie, from a joint forecast (never the independence shortcut).
- `n_other_voters`: n, the nominees' certified votes less one (ex post, marked in `notes`).
- `method`: how p_state and W were computed, in words.
- `W_unconditional`: the unconditional chance the unit's votes decide, for the record only (the product formula the brief forbids; MATH §4 measures its error).
- `f_half`: the forecast density at one half (the model's own forecast).
- From the Economist's draws: `window_draws`, `window_weighted`, `window_width`, `relative_error` (1 ÷ √ of the decisive count), `ratio_to_published` (our p over its own `p_decisive_vote`), and the check `W_mvn`, `W_mvn_se`, `W_mvn_note`.

**`stage_two.inputs`** (Electoral College): `ev` (the electoral votes this contest's count decides: the state's, or 2 at large, or 1 for a district), `ev_state`, `total_ev`, `majority`, `pi_house` (one half: a 269 tie goes to the House, whose choice is counted as a fair lot, model §3), and, from the forecast that gives the contest's `p`: `W`, `W_unconditional`, `unit_ev`, `method`, `national_swing_sd` (the common swing stated), `districts_modelled`.

**In `data/president/inputs/fte_president_forecasts.json`**, for each year and model: `forecast_date`, `election_date`, `dated_election_day`, `note`, `probwin_step` (the step every printed chance is a whole multiple of, measured) and `runs_inferred` (one over it); for each candidate, `projected_voteshare_printed`, the share as printed. **In `fte_poll_averages.json`**: the snapshots `two_months_out` (9 September) and `eve` (the last average before Election Day).

**Contest ids for districts**: `<year>-president-ME-1`, with `place.district` "1" and `place.name` "Maine, congressional district 1".
