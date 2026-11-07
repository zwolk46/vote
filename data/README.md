# data/: what the fields mean

The layout of every contest is plan/PLAN.md §3. A worker may add a field in its own PR with a line here; no field is ever renamed or given a second meaning (plan §3).

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
