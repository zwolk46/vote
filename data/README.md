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
- `missing_from_record`: contests the check source has and the source of record does not (mostly special elections held on other dates). They are added to `contests` with the check source as their record.
- `model`: the fitted terms of the model's own forecast used in the file, fitted on the level's earlier cycles only (D2-v3; `data/congress/REPORT.md` §2).
  - `method`, `fit_years`, `cycles`, `races`.
  - `b_lean`, `b_inc`, and `b_lag` for governors (the last governor race's term; null otherwise).
  - `s_e_fitted` (the race's own sd as fitted), `k` (the calibration factor) and `s_e` (the race's own sd used, k × `s_e_fitted`).
  - `calibration`: how k was found: `k`, the earlier `years` scored out of sample, their `races`, and a `note` (k = 1, "not calibrated", where fewer than three such years exist).
  - `s_a` (the national swing's spread about its terms), `c` (the terms c₀, c_mid, c_on) and `ZtZ_inv`.
  - `national_forecast` and `national_sd`: the year's swing and its prediction sd, k·s_a·√(1 + z(Z′Z)⁻¹z′).
  - `near_tie`: the year's near-tie calibration of p (round 4, REPORT §2.6): its `scheme` (`level`, `band`, or null where not adopted for the level, with a `note` why), `window`, `factor`, `of` (whose earlier years it is fitted on), `fitted_on` (`{level: [years]}`), and the `expected` and `seen` near-ties it rests on. Under scheme `band` (the House from round 5), `by_band` holds those for each band of |mean − ½|, from `band_from` to the next band's start; `of` null means no factor in that band. `taken_out` (the Senate since REPORT §0.3): round 4's factor where it passes round 4's test but fails the robustness test, so it is not in p. It gives the `scheme`, the year's `factor`, `of`, `fitted_on`, `expected` and `seen`, and where the test fails: `fails_without` (`{year left out: [what fails]}`) and `fails_on_every_year` (round 5's cells that fail on all years).
  - `variant` (round 5, REPORT §2.7): `of_record` (`none`, `shrink`, `t4`, `both` or `halflife`: what the test adopted for the level; `none` at every level since the robustness test, REPORT §0.4; the half-life k of §0.2 is not adopted either), `tails_first` (`normal` or `t4`: the tails of the forecast p comes from), `shrink` (null, or the shrinkage: `factor` λ, the earlier `years` and `races` it is fitted on, and `what`) and a `note`.
  - `national_from` (the House of 2008-2012 only): `level` (`senate`), the Senate's `years` whose fit gives `c`, `s_a` and `ZtZ_inv`, and a `note`: national terms from the Senate's earlier cycles, since the House has fewer than four of its own.
  - `sd` and `rho`.
  - `mean_is` and `sd_is`: the formulas that rebuild each forecast from the contest's `forecast_inputs`.
  - `commit`.
  - Where there are too few earlier cycles: `not_fitted`, the reason, with the `fit_years` that do exist.
- `chamber`: control of the chamber for the year.
  - The rule (`218 of 435`; `51, or 50 with the Vice President`), the seats modelled and fixed, `seats_not_up` by caucus, and the expected Democratic seats.
  - `common_swing_sd` and `own_sd` (the model's).
  - `seat_model`: the form each seat takes in the chamber stage.
  - `commit`.
  - `vice_president`: `P_democrat` with `by`, `as_of`, `source` and `note`. In presidential years it is the presidential chance from D1's record: 538's where it stands first, else the model's own College chance over the record's units, Maine's and Nebraska's districts apart where the record forecasts them.
  - `not_computed` (with `commit`) where the chamber stage cannot run (the House of 2006: no model of its own).
  - `seats_not_up_list`: each Senate seat not up, by state and class, with the year it was last elected, its caucus, the winner and the source key. `not_up_source` says where the winners come from.
  - `check`: the seats not up plus the seats won (counted from the check source's winners), against the division the new Congress opened with (`division`, with the chamber's own notes), and whether they `agree`.
- `fte_538`: how many of the file's races have a 538 forecast, in how many it comes first, why the others fell back (by kind), and which of 538's versions comes first, with why.

**In each contest**
- `special`: true for a special election, which fills the rest of a term.
- `two_party`: the two leading candidates, their votes, `n_other_voters` (their combined vote minus one: the n of model §3), and `share_first`.
- `ballot`: who was on the ballot. It gives the counts of Democratic (`D`) and Republican (`R`) nominees, the independents who caucus with the Democrats (`caucus_D`), and `others`. It is known before the election and decides how a seat the model does not compute enters control.
- `forecast_inputs`: what the model's own forecast is built from.
  - `lean`: the district's or state's Democratic two-party share in the presidential election before the race, minus the national share.
  - `pres_year`, `district_share_D` or `state_share_D`, `national_share_D`.
  - `incumbency`: +1 if the Democratic nominee is the incumbent, −1 if the Republican nominee is, 0 otherwise; the fit's definition (REPORT §2.2, §0.5). The Democratic nominee is the candidate with the most votes on a Democratic line, or the independent who caucuses with the Democrats; the Republican nominee is the candidate with the most votes on a Republican line. A nominee is an incumbent where Cha, Kuriwaki and Snyder code them 1; their codes 2 (elected in a special election) and 3 (appointed) count as not, as in the fit (REPORT §7). `incumbency_source` is `cha`, `record` (the source of record's own incumbent mark on that same nominee, where Cha does not hold them) or `algara_amlani` (governors before 2006, with the authors' `seat_status` as they wrote it).
  - `midterm`, `president_party`, and each one's `_source` key.
  - `lean_missing`: why there is no `lean`.
  - `lines`: for a House special, the lines its lean is taken on (the old Congress's, on which a special is held).
  - `lean_same_day`: the same day's presidential vote on the lines, marked inferred. It is used for control only and never for the seat's own p.
  - `last_governor_race` (governors): the state's last governor race before the year that a Democrat and a Republican led, with its `year`, `share_D` (two-party), `special` and `source` (`cha` from 2006, `algara_amlani` before). `last_governor_race_missing`: why there is none.
- `checks`: the same contest in a second source (`against`) and every difference between the two (plan §3a). The source of record wins. `against` is null for a contest only the check source holds; it is then the record, with no second source.
- `date`: null where the sources read here do not give the date (special elections only the check source holds); `result.certified` is null where the source does not say whether its count is the certified one. A note says so in each case.
- `forecasts[].method`: the version of the model's own method (`D2-v3`; for governors, `D2-v3 (with the last governor race)`). `forecasts[].share.of` names whose share the mean is (`Democrat, two-party`). `share.mean` and `share.sd` are at full precision, so that p recomputes from them exactly.
- A forecast `by` `"538"` (FiveThirtyEight's, published) also carries:
  - `version`: 538's version (`lite`, `classic`, `deluxe`; `polls-plus`, `polls-only`, `now-cast`; `only` where the file names none).
  - `chance`: 538's chance of winning by party, as published. `note` says when the forecast is dated Election Day.
  - `share.sd_from`: how the sd was found (implied by the chance under a normal; inferred).
  - `sd_relative_error`: the sd's estimated relative error.
  - `p_relative_error`: p's, which decides whether 538 comes first (under 20%); `z` = Φ⁻¹(chance), on which it rests.
  - `simulations` and `simulations_mark`: the run count the chances step by (inferred), which both errors rest on.
  - `unusable` and `unusable_kind`: why 538's forecast does not come first in this race (a sentence and a short class, such as `p's error 20% or more`); null when it does.
  - `source`: a key into the file's `sources` (`senate_538`, `house_538`, `governor_538`).
- `forecasts[].calibration` (the model's own, the House of 2010-2024; the Senate's too until REPORT §0.3): the near-tie calibration of p (round 4, REPORT §2.6). `factor` multiplies the forecast's density within the `window` of ½ (49-51%), and the forecast is renormalized. So p is multiplied by `multiplier` = factor ÷ (1 + (factor − 1)·q), where q is the forecast's own chance of the window. Also `scheme`, `of`, `fitted_on` (`{level: [years]}`, all before the race's year), `expected` and `seen` (the fitting years' near-ties) and `what`. `share.mean` and `share.sd` are the forecast before calibration.
- The first forecast with a usable share is the one `p.value` uses; `p.under` names it.
- `p.of_forecast`: the index in `forecasts` of the forecast p is computed from. `p.computed_by` and `p.commit`: the script and commit that set the block, whether it holds a value, p = 0 (`pipeline/intake/build_congress.py`) or a reason it is not computed (`pipeline/chambers.py`).
- `p.not_computed`: why p is not computed: a structure the model does not compute yet, a missing input, or too few earlier cycles for the model's own fit with no published forecast reachable. It is `null` when p is computed.
- `p.reason`: why p is 0 (one candidate).
- `forecasts[].shrink` and `forecasts[].share.mean_unshrunk` (the model's own, where a round 5 variant is of record; none is since REPORT §0.4): `share.mean` is the mean shrunk toward ½, ½ + λ·(`mean_unshrunk` − ½), with λ the `shrink.factor` fitted on the level's earlier years (`shrink.years`); `share.sd` is the sd with k refitted on the shrunk means. Where t4 is of record (none is since REPORT §0.4), the model's own forecast with `share.tails` "t4" stands first and the normal one beside it.
- `p.value_uncalibrated`: where p is calibrated to earlier years' near-ties (`p.under` ends so), p before it: what pipeline/core.py gives from the forecast's mean and sd. `p.value`, `p.event` and `p.f_half` are that times the forecast's `calibration.multiplier`, and so is each `p.alongside` entry of the model's own.
- `p.method` (`exact` or `density`) and `p.n` are pipeline/core.py's own outputs, and so is `p.f_half` where p is not calibrated. Where it is (`p.under` ends so), `p.f_half` is the calibrated density at ½: f(½) × `calibration.multiplier`, with f(½) the forecast's own density there. f(½) itself is `p.f_half` ÷ the multiplier. `p.sd`: for 538, the implied sd p used.
- `near_tie_not_of_record`, on `p` and on each `p.alongside` entry of the model's own (the Senate of 2010-2024, since REPORT §0.3): round 4's near-tie factor, taken out of p by the robustness test and shown beside it. It gives `factor`, `multiplier`, `scheme`, `value` (what p would be with it: p × `multiplier`) and a `note`.
- `note`, on `p` and on each `p.alongside` entry: the forecast's known lean near even, in the brief's words, uncorrected. Governors: on every p since REPORT §0.3, with its counts from `data/congress/history.json` (`governor_note`, within 5,000 votes, 2006-2024). House and Senate: on each p of the model's own normal forecast, standing first or beside 538's, since REPORT §0.1, with the back-test's counts within 1 point of ½ (49-51%), 2010-2024. 538's p there carry none.
- `p.alongside`: p under the other forecasts: the model's own with t4 tails (same sd), the model's own normal where 538's comes first, and 538's other versions. Each has its own `event`, `f_half`, `of_forecast`, its `control`, and for 538 the implied `sd`.
- `p.control`: p for control of the chamber, which is p × `P_decides_given_tie` (MATH §4.2), with its `event`. The chamber stage is the model's common swing and the other seats, with this seat entered under the forecast p is computed from (for 538, reading (c)); `p.control.under` says so.
- `stage_two.inputs`: how the seat enters control.
  - `entered_as` is `model`, `inferred` (the model's two-way forecast for a structure whose p is not computed, marked) or `fixed` (settled by who was on the ballot, never by the result).
  - `mean`, `own_sd` (s_e,i) and `swing_loading` (λ_i): the seat in y_i = mean_i + λ_i·d + e_i, with `common_swing_sd` the sd of d. `marginal` says whose forecast this is.
  - `marginal_note`: where 538's sd is not above the common swing's, the share of the swing the seat carries, so that its sd stays 538's.
  - `P_decides_given_tie` and `P_decides_unconditional` (what the usual shortcut would use).
  - In presidential years for the Senate, `P_decides_given_tie_if_VP_D` and `_if_VP_R`: the same given a Democratic or a Republican Vice President.
- `stage_two.note`: why a contest is not part of control (a special that fills the old Congress's term).
- **Governors of 1978-2004** (`data/governor/1978.json` to `2004.json`, from Algara and Amlani's county returns):
  - `result.certified` is null: the votes are the authors' county returns summed to the state, not a certified total. `result.votes_incomplete` is true where a county has no count in the source, or for Missouri, whose count is taken as incomplete (REPORT §3).
  - `result.candidates` names the two nominees; everyone else is one line, `"others (not named in the source)"` with `party` null, the county total less the two nominees.
  - `ballot.others` is null (the source does not say how many others ran). `ballot.D` and `ballot.R` count the nominees the source names.
  - `checks` is `[{"against": null, ...}]`: no second source is read for these years.
  - `date` is the general election day, inferred (the source gives the year); a note says so.

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
- `share.sd_rel_error`: for 538, the estimated relative error of the sd its mean and chance imply (`value`), from the chance's sampling error (`from_chance`, `chance_se`, with `runs`, the simulation runs its printed chances count, and `runs_mark`, how that was inferred) and the rounding of the printed shares (`from_mean_rounding`, `mean_rounding`), and `z` = Φ⁻¹(538's two-party chance); `null` where unbounded.
- `share.p_rel_error`: for 538, p's estimated relative error under that sd (`value`, `z`, `how`): the sd's error from the chance times \|z² − 1\|, combined with the mean's rounding at factor 1. *Reason:* the orchestrator's amendment of 2026-11-07 05:58 (after M2 3.9; the reader sees p, not the sd) keeps 538's sd only where this is under 20%, as D2 does for Congress; where it is not, `share.sd` is `null`, `share.sd_how` says why and which sd the College stage used, and the contest's `p` is the model's own, marked in `notes`.
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
- From the Economist's draws: `window_draws`, `window_weighted`, `window_width`, `relative_error` (1 ÷ √ of the decisive count), `ratio_to_published` (our p over its own `p_decisive_vote`), and the check `W_mvn`, `W_mvn_se`, `W_mvn_note`; `W_by_window`, W read at each of the four window half-widths counted (±0.0025, ±0.005, ±0.01, ±0.02); and `W_thin`, `W_thin_note` where the window holds fewer than 30 weighted decisive draws. *Reason:* the amendment of 05:58 (M2 2.4): there W moves by factors of 3 to 10 with the window's width, and the page must say so.

**`stage_two.inputs`** (Electoral College): `ev` (the electoral votes this contest's count decides: the state's, or 2 at large, or 1 for a district), `ev_state`, `total_ev`, `majority`, `pi_house` (one half: a 269 tie goes to the House, whose choice is counted as a fair lot, model §3), and, from the forecast that gives the contest's `p`: `W`, `W_unconditional`, `unit_ev`, `method`, `national_swing_sd` (the common swing stated), `districts_modelled`.

**In `data/president/inputs/fte_president_forecasts.json`**, for each year and model: `forecast_date`, `election_date`, `dated_election_day`, `note`, `probwin_step` (the step every printed chance is a whole multiple of, measured) and `runs_inferred` (one over it); for each candidate, `projected_voteshare_printed`, the share as printed. **In `fte_poll_averages.json`**: the snapshots `two_months_out` (9 September) and `eve` (the last average before Election Day).

**Contest ids for districts**: `<year>-president-ME-1`, with `place.district` "1" and `place.name` "Maine, congressional district 1".

## Fields added by D3 (state legislatures, primaries, local races, measures; `data/state-upper/`, `data/state-lower/`, `data/primary/`, `data/local/`, `data/measure/`)

**Files.** One file per level, year and state: `data/<level>/<year>/<ST>.json`, compact JSON with one contest per line. **An absent field means null** (the files leave nulls out to keep the repository small).

**At the top of a file**
- `level`, `year`, `state`: what every contest in the file shares.
- `chamber`: the chambers' names in that state (`state-upper`, `state-lower`).
- `sources`: source blocks by key, as D2's; `result.source` and `forecasts[].source` hold a key.
- `p_computed_by`, `p_commit`: the script and commit that computed every `p` in the file (in place of each contest's `p.computed_by` and `p.commit`).
- `party_codes`: for each source party code used in the file, the source codebook's own words (for Klarner, its codebook's Appendix C).

**In each contest**
- `election`: the kind of election in words (`general`, `general, for the rest of a term`, `Democratic primary`, or the source's own code where it has no words, such as `lafsettled`, Louisiana's first round).
- `seats`: the seats the contest fills, when more than one ("vote for k").
- `office` (primaries): the office the primary nominates for (`state-upper`, `state-lower`).
- `result.candidates[]`: `won` is `true`, `"to runoff"` or `"tied"` (absent for a loss); `incumbent` is `true` when the source marks the candidate as the sitting member; `party` is `D`, `R`, `write-in`, `nonpartisan`, a minor party's own name, or, where the source gives only a code, the code in words (`minor party or independent, party not named`, `no party`, `unknown`), with the code itself in `party_code`.
- `two_party`: as D2's, without the names: the votes of the two leading candidates (route b) or of the Democrat and the Republican (route a), `n_other_voters` (their votes minus one) and `share_first`.
- `boundary`: for a race that fills several seats, the same for the last winner and the first loser (model section 7).
- `forecasts[].route`: how the model's own forecast was built: `partisan` (the seat's last result, incumbency, the chamber's lean and the year's swing), `class` (like past races), `boundary`, or `runoff` (a runoff's second round, from like past runoffs). For `class`, `boundary` and `runoff`: `class` names the class, `like_races` how many races of the class in other years, `window` the share window and `in_window` how many of them finished in it, `q` their share; `note` says when the route is not yet checked.
- `forecast_inputs` (route `partisan`): `class` (`A` last result contested, `B` last result unopposed, `C` none on these lines), `incumbency` (+1 D incumbent, −1 R, 0 open), `lean` and `lean_year` (the chamber's mean Democratic share at its previous election, minus ½), `swing` (the year's forecast swing), `last_D` and `last_year` (the seat's previous Democratic two-party share) or `last_unopposed`.
- `p.forecast_scope` (route `partisan`, wherever p has a value from the model's own partisan forecast): what that forecast knows of the seat. `district (class A)` and `district (class B)` mean the seat's own last result, or whether it was last won unopposed, enters the forecast. `chamber average (class C)` means only the chamber's lean and the seat's incumbency do: the lean is the same for every district of the chamber, so p is that of an average district of its chamber, not of this one (REPORT §6). For local races between a Democrat and a Republican (route `partisan`, transferred), it is `the race's counties (class C's terms with the counties' US House lean)`.
- `p.not_computed`: why p is not computed for this contest, in words (for example a first round of a two-round system, or too few earlier years to fit on). `p.reason`: why p is 0 (one name on the ballot for each seat).
- `p.f_half`, `p.n`, `p.method`: f(½) of the forecast, the n p was computed at (the two candidates' votes minus one), and pipeline/core.py's method (`exact` or `density`).
- `p.alongside.t4`: p under the same forecast with Student-t tails (4 degrees of freedom, the same sd).
- `notes`: the source's own flags (Klarner's `dontuse`, its uncertainty marks), and where a candidate outside the two parties finished among the leading two.

**From MEDSL's precinct returns** (`pipeline/local_medsl.py`; 2018, 2020, 2022 and 2024):
- `result.source` is `medsl`. The votes are MEDSL's precinct counts added up to the contest. `won` is inferred from the count: the leading candidates on the ballot for the seats, and none at a tie for the last seat, since MEDSL does not mark winners. `votes_incomplete` is `true` where MEDSL redacts some precincts' counts.
- `office` (local): the office as MEDSL names it. `office_type`: the class of office the like-race classes use (`council, commission or board`, `school board`, `judge`, `prosecutor`, `sheriff or constable`, `mayor or executive`, `special district`, `clerk, treasurer or other county officer`, `other local office`).
- `office_scope` (`data/local/`): `local`, or `state` for the state's other offices (its courts, boards and statewide officers other than the governor), which plan §3 gives no level of their own; they are written in `data/local/` and classed apart from local offices.
- `place.counties`: the county FIPS codes the contest's precincts lie in (none for a statewide office). `place.position` (state legislatures): the seat's position where a district elects members one position at a time (Washington). `place.district` is `null` where the source gives no number (Rhode Island, 2024), with a note.
- `office_as_filed`: the office's name in the source where it differs from the level (Washington files its legislature as local offices named by district).
- `candidates[].lines`: where a candidate stands on several parties' lines (fusion, as in New York) or a county spells the name differently, each line with its votes; `votes` is their sum. `party` `D and R` is a candidate on both major parties' lines.
- `forecast_inputs` (local races between one Democrat and one Republican, route `partisan`, marked "transferred, not yet checked" in the forecast's note): `class` `C`, `incumbency` 0 (not matched), `lean` and `lean_year` (the Democrats' two-party share of the US House vote in the race's counties at the previous general, minus ½; `lean_of` says so), `swing`.
- `forecasts[].calibration` (local races, like-race and Democrat-against-Republican routes): `factor` (seen over expected near ½ in the fitting years' out-of-sample forecasts), `of` (the office type it was fitted for, or pooled), `fitted_on` (the years). p is multiplied by it, and `p.under` ends "calibrated to earlier years' near-ties". Since 2026-11-07 09:49 UTC no route is calibrated: the robustness test took the factor out (REPORT §7).
- `p.calibration_not_of_record` (local races, like-race and Democrat-against-Republican routes, 2022 and 2024): the factor the robustness test took out, shown beside p: `factor`, `of`, `fitted_on`, `what`, `value` (p with it) and a `note`.
- `p.exact_mass` (like-race p where pipeline/core.py took the exact sum, n under 1,000): the mass of the normal device (mean ½, density f at ½) on the exact sum's grid. p and the event are core's exact sum times it, so the measured f is kept, not raised by renormalising to (0, 1) (REPORT §7).
- `forecast_inputs.lines_unchanged_share` (2024 state legislatures): the share of the district's 2024 precincts that were also in it in 2022. At 0.8 or more the lines are taken as unchanged and the 2022 result is the last result; otherwise the class is `C`.
- **Measures** (`data/measure/`; 2016 to 2024, 2016 from MEDSL's older sets, questions only): `question.title`, `question.subject` (a retention's judge), `question.kind` (`measure` or `retention`), `question.scope` (`statewide`, `local`, or `partial`: a statewide question in a year whose source holds only part of the state's counties), `question.type` (`amendment`, `statute`, `bond`, `convention` or `advisory`, as the source's title states it; absent where the title does not say); `result.candidates` are the answers (`YES`, `NO`, ...); `result.yes_share` is Yes over Yes and No. A local question is counted per county (see its note).
- `threshold` (a statewide question whose state's law is read): `t`, the share of Yes among those voting on the question that the measure needs; `rule`, `citation`, `url`, `quote` (the law's own words) and `read_utc`, as read; `matched`, how the rule was matched to the question (by the type its title states, or because every rule read for the state sets the same threshold). Every state's rules, their exceptions and what could not be read are in `data/measure/thresholds.json`.
- `two_way`: `votes` (Yes, No), `n_other_voters` (their sum minus one) and `share_yes`.
- `forecasts[]` with route `like past measures`: `class` (`statewide measure` or `statewide retention`), `like_measures` (how many questions of the class in earlier years), `window` (around t), `in_window` (how many of them finished in it) and `q` (their share).
- `p` (model section 7, the threshold form): `yes`, about (1 − t) f(t) / n, the chance a Yes ballot decides; `no`, about t f(t) / n; `value`, the larger of the two, and `value_of`, which ballot it is (`either ballot` at t = ½); `event`, f(t) / n, the chance the count lands on the threshold; `threshold`, `f_t`, `n`, `under` and `method`; `note`, where the route's own back-test found more near-even finishes than it forecast, says so with the counts.

**From North Carolina's State Board of Elections** (`pipeline/intake/ncsbe.py`, `pipeline/local_ncsbe.py`; every election date from 2000 with a results file):
- `result.source` is `ncsbe`. The votes are the State Board's precinct counts, added up to the contest. The State Board names most contests in full, with their place ("CITY OF ARCHDALE MAYOR"), so its lines are joined across counties by that name. A county's own contests named without the county are joined within one county. That covers every county contest of 2010 to 2013 and, from 2014, those whose name carries no place ("SHERIFF (REP)"). These carry a `notes` line beginning "one county's own contest" where the name stands for several counties' contests on the date.
- `election`: which round, in words. The source does not say which round a date holds, so each is read from the ballots [inferred]:
  - a party's primary is a name that carries the party ("... - DEM"), or, before 2008, a contest whose candidates all carry one party code;
  - a second primary, or a first round followed by a later one, is the same contest's name on another ballot that year;
  - `deciding round after an earlier round on <date>` is a November contest whose name was on an earlier ballot that year, after a nonpartisan primary or a first round (the orchestrator, 2026-11-07 09:53 UTC). It is the round that elects, so p is computed by the route's classes. The same words mark the State Board's contests of this kind on MEDSL's general dates. The earlier round, and a second round on another date, are not computed (model section 7);
  - a question has no rounds: where one of the same title was on another ballot that year, its `election` says so after `general` or the date;
  - `general (odd year: municipal)` is a November date of an odd year.
- `seats`: the source's "vote for", given from 2014 only. Earlier contests with more than one name have no seat count, so `won` is left out and a note says so.
- `party`: `D` and `R` for the source's DEM and REP. Any other code is kept as the source writes it, in `party` and `party_code`, because its layout files give no codebook.
- `place.counties`: FIPS codes. The source names counties, and the codes come from the county_name and county_fips columns of MEDSL's 2024 North Carolina file (the `fips` source block).
- **Where MEDSL and the State Board hold the same contest** (North Carolina's local races and questions on MEDSL's general dates, 2016 to 2024), the State Board's counts are written in place of MEDSL's, by `pipeline/local_medsl.py`, with MEDSL's routes for p. The certified count wins (brief D3, step 2). The governor and Congress stay MEDSL's.
- `result.votes_source` (North Carolina's legislature): `ncsbe` where the contest is Klarner's or MEDSL's but its votes are the State Board's, because the two differ and the State Board's file passes its gate. Its first note gives both counts for each candidate that changed, and its file holds the `ncsbe` source block. These are 4 contests of 2002, 79 of 2016 and 22 of 2018 (Klarner's, by `pipeline/local.py`) and 46 of 2024 (MEDSL's, by `pipeline/local_medsl.py`). The other years keep their source's counts; `data/local/REPORT.md` §9 says which and why.
- **A file with two sources' contests.** One level, year and state can hold contests from two builds. For example, `data/local/2022/NC.json` holds MEDSL's general date and the State Board's other dates. Each build rewrites only its own contests and keeps the other's. A contest that carries its own `p.computed_by` and `p.commit` has them in place of the file's `p_computed_by` and `p_commit`.
- `forecasts[]` (the State Board's other dates, route `class` or `boundary`): as for MEDSL's like races, fitted on North Carolina's State Board contests of earlier years only (`fitted_on`), uncalibrated. The `note` gives the reason from the back-test's `calibration`: the factor fails the robustness test, with the cells it makes worse. Two classes are added: `<scope> <office type>, a Democrat against a Republican`, and primaries, `primary, <scope> <office type>, <n> candidates`, with p between the top two. The back-test is in `data/local/backtest-ncsbe.json`. Its `calibration` gives, for local races and for primaries, each scored year's pooled factor, the `test` over all scored years (expected before and after against seen, the deviance by office type, the tested cells made worse), `leave_one_year_out`, `robustness_rule` and `adopted`.
- `notes` names a date whose file falls short of the certified federal counts by more than 0.5%, which marks a file posted before the final count [inferred]. The 2000 and 2010 general elections are such dates (`data/local/check-ncsbe.json`, `gate`). Their counts are the State Board's posted ones.

**From Indiana's own certified results, 2024** (`pipeline/intake/in_enr.py`, `pipeline/local_in.py`; `data/<level>/2024/IN.json`):
- `result.source` is `in_enr`: the state's results site's archive (enr.indianavoters.in.gov/archive/2024General/), whose settings mark the results certified. It passes the gate against D1's and D2's certified federal counts, so it takes the place of MEDSL's Indiana file, which is held back (`data/local/check-in.json`; REPORT §10). The presidency, Congress and the governor stay D1's and D2's.
- `party`: the site's codes, read as `DEMOCRAT`, `REPUBLICAN`, `LIBERTARIAN`, `INDEPENDENT` and `NONPARTISAN` (its `N`, "Non Partisan"). Any other code is kept as the site writes it.
- `place.counties`: the counties the site lists for the race. A title that does not name its place takes its district's name from the site's jurisdiction ("SCHOOL BOARD MEMBER, DISTRICT - MILAN").
- The site lists no write-in lines. So `p = 0` for an unopposed race is not checked against a strong write-in, as it is for MEDSL's.
- `question.subject` is the question's ballot text, as the site gives it.

## Fields added by D4 (the cost of voting and how ballots are cast: `data/cost/`; each state's tie and recount law, `data/law/`, below)

**Marks.** Every number is [measured] (read here from the source's own file), [stated] (as a compilation or an agency guide says), [inferred] (my arithmetic or reading, said in the field's note) or [vendor claim]. **A `source` block** is as D2's: `name`, `url`, `read_utc`, `licence`, `mark`, `via`, `note` (bytes and sha256). Intake scripts, one per source, are in `pipeline/intake/`; `data/cost/REPORT.md` says what each gives and does not.

### `data/cost/`
- **`national-default.json`**: `default_cost_dollars` (8.87), `formula`, `inputs.minutes` (14, the median time at the polling place, with `replication_check`: the median, mean and share over 30 minutes computed from the authors' public file) and `inputs.hourly_wage` (BLS CES0500000003, latest month, via FRED), `with_the_mean`, `not_measured`, `national_mode_shares` (EAVS and CPS, by year), `states_with_mail_share_at_least_90_percent_eavs`.
- **`by-state.json`**: one record per state and DC: `wage` (series, latest month, November of each election year), `chen_2016` (mean, median, share over 30 minutes, n, se; absent for AK, CO, HI, OR, WA), `spae` by year (`mean_minutes_midpoint`, `mean_minutes_lower_bound`, `se_minutes`, `share_over_30_minutes`, `n_with_wait_answer`, `thin`), `eavs` by year (`total_ballots`, `mail_share`, `early_in_person_share`, `election_day_share`, `uocava_share`), `cps` by year (`voted_share`, `mail_share`, `early_in_person_share`, `election_day_share`, `n_voters_with_mode`), and `cost_dollars`: each basis (Chen median, Chen mean, SPAE 2022 and 2020 mean) as minutes x wage / 60, with the arithmetic in `formula_state_wage`.
- **`eavs-mode.json`** (`eavs.py`): per year, per state: `total_ballots` (F1a summed over jurisdictions), `by_mode` (counts of F1b to F1j under their names), `jurisdictions` and `jurisdictions_with_total`, `jurisdictions_not_reporting` (by item), `parts_sum_over_total`, and the four shares. `check_against_published_total` holds the file's total over every row, the part from the territories, the EAC report's printed total, `report_total_found_in_text` and the difference. `mail_share` is (F1d + F1g) / F1a; `election_day_share` is (F1b + F1e) / F1a; -88 and -77 read as zero, -99 and "Data not available" as not reported.
- **`cps-voting.json`** (`cps_voting.py`): per year, per state: `voted_share` (those who said they voted, over those who gave yes or no), the three mode shares among voters who gave a valid mode, each with a design-naive `_se_naive` (a floor), `n_citizens_asked`, `n_voters_with_mode`; `check_against_documentation_tallies` compares the unweighted counts with the technical documentation's.
- **`spae-waits.json`** (`spae.py`): per year, per state: the weighted shares of the five wait categories (`wait_shares`), `mean_minutes_midpoint` and `mean_minutes_lower_bound` (conventions, [inferred]), `se_minutes`, `share_over_30_minutes`, `n_with_wait_answer`, `thin` (under 60 answers), `mode_shares_survey`; per year also `pooled` (all in-person voters of the 50 states and DC with a wait answer, and by mode: `wait_shares`, `share_over_30_minutes`, `mean_minutes_midpoint`, the same with the top category at 90 minutes, `mean_minutes_lower_bound`) and `middle_state` (the median of the state means, with 60 or more answers and for all states, and with the top category at 90); `checks` holds `line_codes` (the line-length variable's five labels in each year's DDI codebook, and whether its counts equal the data file's), `questionnaire_2020` (Q14 as the 2020 questionnaire words it) and `published` (what MIT's 2020 and 2022 reports print, the phrases the script found in them, beside the pooled figure from the data file); `gated` lists SPAE 2024 (a guestbook).
- **`chen-waits.json`** (`chen_waits.py`): `states.<ST>`: `mean_minutes`, `median_minutes`, `sd_minutes`, `share_over_30_minutes`, `n_waits`, `se_minutes`, `mean_minutes_empirical_bayes`, `cces_survey_mean_minutes_empirical_bayes`; `national_all_filtered_waits`; `check` (the Ns equal the archive's 154,489); `states_absent`.
- **`wages.json`** (`bls_earnings.py`): `national` and `states.<ST>`: `series`, `title`, `units`, `latest` {year, month, value}, `by_election_year.<year>` {`november`, `mean_of_months`}; `source` names FRED as the carrier and BLS as the origin; `check_against_bls` lists the months compared with the BLS API and any difference.

### `data/law/`
- **`ties.json`** and **`recounts.json`**: `states.<ST>` for the 50 states and DC, each with `name`, `status` (`read`, `partly-read` or `unread`), `code` {name, edition, site, reached}, `sections` (key to citation, url, `read_at`, `render: true` where the page was read in headless Chromium, and `tree: {steps, open}` where it was read by opening a statute viewer's contents tree), `unread` (what was not read and the exact reason, url and time), `notes`, and `rules`.
- **A tie rule**: `kinds` (from `federal`, `presidential-electors`, `statewide`, `state-legislative`, `local` (state general law only), `primary`, `measure`), `applies_to`, `resolution` (`lot`, `new-election`, `legislature`, `runoff`, `recount-then-lot`, `recount-then-new-election`, `party-committee`, `court`, `other`, `none-found`, `unread`), `steps` (what happens, in the statute's order), `who`, `mark`, `note`.
- **A recount rule**: `kinds`, `type` (`automatic`, `requested`, `court`, `other`), `election`, `threshold` {`percent` (0.5 means one-half of one percent), `percent_of` (the statute's base), `votes`, `combine` (`or`, `and`, `lesser-of`, `greater-of`), `inclusive` (true for "or less"), `conditions`, `in_words`}, `no_margin_required` (a recount on request at any margin), `who_may_request`, `cost_bearer`, `mark`, `note`.
- **Every rule** has `sources`: `{section, quote}` where `quote` is the statute's (or the agency guide's) own words, and `source_blocks` (url, `read_utc`, `sha256` of the page, `licence`, `via` and `origin` where a compilation was used), `quotations_verified` (true when `pipeline/intake/state_law.py` found every quotation word for word in the page it fetched). A `mark` of `measured` is the state's own text; `stated` is an agency guide or compilation (a lower grade, named in `sections.<key>.read_at`); `inferred` is a reading of what the text implies, said in `note`.
- `data/law/src/<ST>.json` are the curated readings the two files are built from (`python3 pipeline/intake/state_law.py build`).
