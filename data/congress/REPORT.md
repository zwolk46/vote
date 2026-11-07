# Senate, House and governor: sources, method and checks

*Worker D2 (`briefs/D2-data-congress.md`, amended 2026-11-07 03:13 and 05:58 UTC). Written 2026-11-07 and revised the same day for the follow-ups from M2 (§0). It covers every Senate, House and governor race of the even years 2006 to 2024 that the sources hold, with p, and control of the Senate and the House.*

## 0. The follow-ups from M2 (brief, amended 2026-11-07 05:58 UTC), each with its reason

M2 checked every p (`checks/M2-REPORT.md`) and the orchestrator decided its readings. What was done:

1. **The Vice President's tie vote in presidential years is the presidential chance**, not one half. It is 538's where 538's forecast stands first in D1's record of the year: in 2016 and 2020, its polls-plus chance that the Democratic ticket wins, 0.7137 and 0.8932. Otherwise it is the model's own chance that the Democrat wins the College: 0.954 in 2008, 0.552 in 2012 and 0.529 in 2024 (§4). *Reason:* the Senate's control in a presidential year turns on who becomes Vice President.
2. **The model's own forecast is fitted on earlier cycles only** (method D2-v2), never leaving one cycle out, and its national sd comes from those cycles too.
   - The Senate's fit now reaches back to 1982 through MEDSL.
   - A fit needs four cycles, with presidents of both parties among them (the back-test, §2.3). So the House has a forecast of its own from 2014, and governors from 2020.
   - Earlier years have p only where 538's forecast stands first. There are none, because 538's files for those years give chances without shares.

   *Reason:* the model's own forecast is fitted to like past races, from what was known before the election (MODEL §3); a coefficient fitted partly on later years is something no voter knew.
3. **538 is kept on p's error, not the sd's**: it stands first where p's estimated relative error is under 20% (§2.1). This moves 155 House, 7 Senate and 2 governor races to the model's own forecast, the counts M2 found. *Reason:* the reader sees p, and at z = 3.94 a 7% error in the sd is a 105% error in p (M2 3.9).
4. **Control under 538, reading (c).** A seat whose p is 538's enters the chamber stage with 538's mean and sd as its marginal. Its own error is √(sd₅₃₈² − s_a²).
   - Where 538's sd is not above the common swing's (23 seats), the seat carries a share of the swing at the model's own correlation, so that its sd stays 538's. These seats are marked in `marginal_note` (§4).

   *Reason:* one forecast of the seat throughout its figure (M2 2.6).
5. **Governors carry the state's last governor race** as a predictor (M2's A4: log score 1.064 → 1.143).
   - The back-test covers 2020-2024, 58 races, the only years with enough earlier cycles that have the term. Its z sd is 1.11, and its coverage is 64 / 79 / 91% at 50 / 80 / 95% (§2.3).
   - The governors' p may be shown (the orchestrator): M2 found the 0 of 4.4 specific to the 5,000-vote line, and the forecast slightly too wide (M2 3.1, 3.2).
6. **The files reproduce themselves.**
   - Mean and sd are at full precision.
   - Every p block holds f(½) and names the forecast it is computed from (`of_forecast`).
   - The p = 0 blocks name their script and commit.

   *Reason:* law 4: a reader recomputing p from the file gets the file's p.
7. **One fetch and one FEC intake.**
   - Every D2 intake script downloads through D1's `pipeline/fetch.py`, which refuses a redirect to another site.
   - D1's `fec_president.py` is now `fec_federal_elections.py president`. Its parsers are unchanged, and its output is identical: the same values, and the same SHA-256 for every workbook.

   *Reason:* one implementation of each thing.
8. **Senate 2014's chances stand as exact**, as recorded, because they have no step at any plausible run count (M2 3.7).

**What changed, in totals.**
- p is computed for 2,650 contests (4,264 before), 1,064 of them under 538 (1,228 before).
- 178 contests have p = 0.
- 2,169 are not computed, 1,614 of them for too few earlier cycles.

The sums of p by level and year are in §5.

## 1. Sources taken in by script

Each source is read by one script in `pipeline/intake/`.
- Every download goes through `pipeline/fetch.py`, into a cache outside the repository: `$VOTE_CACHE`, else `~/.cache/vote-intake`. These files were built with `VOTE_CACHE=/tmp/vote-cache`.
- It records the URL, read time, size and SHA-256 of every file. It stops at an HTTP error, or at a redirect to a site other than the URL's own or a storage host named at the call.
- Each script checks sums against the source's own totals and normalizes.
- Rerunning any of them gives the same inputs.

| Script | Source | Covers | Licence | Read |
|---|---|---|---|---|
| `fec_federal_elections.py` | FEC, *Federal Elections* workbooks | House and Senate general results with incumbent marks, 2006-2022. With `president`, the presidential results by state, 1996-2024 (D1's, folded in) | none printed; federal record | 2026-11-07 |
| `clerk_statistics.py` | Clerk of the House, *Statistics of the Presidential and Congressional Election* (PDF) | House and Senate, 2024 (the FEC has no 2024 congressional volume yet) | none printed; House publication | 2026-11-07 |
| `medsl_dataverse.py` | MIT Election Data and Science Lab, Harvard Dataverse | Senate 1976-2024 (the seats not up, and the Senate's fit from 1982); President by state 1976-2024 | CC0 1.0 | 2026-11-07 |
| `candidates_american_general_elections.py` | Cha, Kuriwaki and Snyder, *Candidates in American General Elections*, doi:10.7910/DVN/DGDRDT, v4.1 | House, Senate, **governor** 2006-2024 (odd years too), hand-coded incumbency | CC0 1.0 | 2026-11-07 |
| `downballot_pres_by_cd.py` | The Downballot, presidential vote by congressional district (public Google Sheets) | 2000-2024 presidential vote on the lines of each House election 2006-2024 | none printed | 2026-11-07 |
| `fec_ballot_candidates.py` | FEC, 2024 general election ballot candidates | who sat in Congress in 2024 | none printed; federal record | 2026-11-07 |
| `nara_electoral_college.py` | National Archives, Electoral College pages | president and VP elected, 1976-2024 | federal record | 2026-11-07 |
| `census_acs_population.py` | Census Bureau, ACS 1-year, table B01003 (www2.census.gov table files) | population of each state and district, 2022 and 2024 | federal record | 2026-11-07 |
| `party_divisions.py` | U.S. Senate, *Party Division*; House History, *Party Divisions of the House* | seats by party at the opening of each Congress, with the chambers' notes | none printed; chamber publications | 2026-11-07 |
| `fivethirtyeight_checking_our_work.py` | FiveThirtyEight, `checking-our-work-data` (raw.githubusercontent.com, commit f6d5b2e) | 538's published forecasts by race and day: Senate 2008-2022, House 2010 and 2018-2022, governors 2010, 2018, 2022 | CC BY 4.0 | 2026-11-07 |
| `build_congress.py` | the caches above | builds `data/senate|house|governor/<year>.json` | | |

**Source of record and check.** For 2006-2022 the FEC's volume is the record; for 2024 it is the Clerk's. Cha, Kuriwaki and Snyder check every House and Senate contest, and the differences are kept in `checks` (§6). Governors have one standardized source here (Cha), so they are not checked yet. MEDSL's state-office precinct files for 2022 and 2024 (CC0, no guestbook) are the lead for a check.

**Not taken.** MEDSL's House file sits behind a Dataverse guestbook that asks for a name and email; filling it is the maker's call (law 10). 538's own forecast pages redirect to abcnews.com. The full inventory is `data/sources/congress.md`.

## 2. The forecasts

### 2.1 538's published forecast, first where it can be used

The orchestrator's words of 03:46 put "a reachable published forecast" first, with ours as the check; the rules below are his of 04:12 and 04:20. 538's `checking-our-work-data` keeps every race it forecast, each day and each version, with the projected vote share and the chance of winning.

- **Which forecast.** The last one dated before Election Day, recorded as `as_of`. In 2008 and 2010 the file holds one forecast per race, dated Election Day, and it is marked so.
- **Which version.** 538 showed one version by default. No source read here names it: its pages redirect, and its data READMEs do not say. So the version listed first in the repository's rows comes first, and the others stand beside it in `forecasts`. That is *lite* in 2018-2022, *polls-plus* in 2016 and the only version in 2014. This is an orchestrator choice the maker may correct.
- **Mean and sd.** The mean is the Democrat's projected share of the two leading parties' projected vote. The sd is the one a normal needs to give 538's chance: sd = (mean − ½) ÷ Φ⁻¹(chance), marked inferred. 538's own distribution is not normal, so this sd is "the normal that agrees with 538's mean and chance", not 538's.
- **When it is used.** 538 comes first when three things hold:
  - **p's** estimated relative error is under 20% (the brief, item 3; before, the rule was on the sd's error);
  - no chance is exactly 0 or 1;
  - other candidates hold under 1% of the chance.
- **Where the error comes from.**
  - *The chance's sampling error*, √(q(1−q)/N). N is the number of simulation runs the chances step by: 50,000 in 2018, 40,000 in 2020 and 2022, and 20,000 in 2016, marked inferred. 2014's chances have no step at any plausible run count and are taken as exact (M2 3.7). The chance is moved one standard error either side and carried through Φ⁻¹ at both ends, not linearized. A chance one run from 0 or 1 is unbounded and falls back.
  - *The rounding of the printed shares.*
- **How each error reaches p.** p = φ(z) ÷ (2n·sd), with z = Φ⁻¹(chance) and sd = (mean − ½) ÷ z.
  - An error in the chance moves z. It moves p by |z² − 1| times its relative error in z, which is the sd's. At z near 1, p hardly depends on it; at z = 3.9, the error is multiplied by 14.
  - The mean's rounding moves only the sd, since z is fixed by the chance. So it moves p by its own relative size.
  - The two are added in quadrature, as `p_relative_error`, beside `sd_relative_error` and `z`. The brief's words are "|z² − 1| × the sd's". The mean's part is carried with a factor of one, because that is how p depends on it.
- **Otherwise** ours comes first, with 538's forecast beside it and the reason in `unusable` (a sentence) and `unusable_kind` (a short class).
- **Control of the chamber.** 538's file gives no joint distribution, so the chamber stage is the model's: its common swing and the other seats. A seat whose p is 538's enters it with 538's mean and sd as its marginal (reading (c), §4).

| Level | Races with a 538 forecast | 538 first | Ours first: no share in the file (2008-2012 Senate; 2010) | chance 0 or 1 | p's error 20% or more | other |
|---|---|---|---|---|---|---|
| House | 1,566 | 853 | 400 | 111 | 200 | 2 |
| Senate | 251 | 147 | 94 | 0 | 9 | 1 |
| Governor | 99 | 64 | 32 | 0 | 3 | 0 |

Under the rule on the sd's error, the same column held 45, 2 and 1. The rule on p moves 155 House, 7 Senate and 2 governor races to the model's own forecast, the counts M2 found (3.9).

The two "other" House cases are a 538 Democrat not on our ballot (South Carolina 5th, 2018, where 538 names April Freeman and the record has Archie Parnell) and one race with no Democrat or Republican in 538's rows.

### 2.2 The model's own forecast (method D2-v2)

D2-v2 is D2-v1 (approved by the orchestrator 2026-11-07 03:46 UTC), fitted on earlier cycles only and with the governors' last race (the brief, 05:58). It is used where no published forecast can be, and it is always kept beside 538's as the check. For a race in year t, with y the Democrat's share of the two-party vote:

> y = ½ + a_t + b_lean × lean + b_inc × inc [+ b_lag × (lag − ½), governors only] + e

- **lean**: the Democrat's two-party share of the last presidential vote before year t, minus that election's national share (MEDSL).
  - For the House it is taken on the lines in use in year t (The Downballot); for the Senate and governors, in the state (MEDSL).
  - A House special is held on the old Congress's lines, so its lean is taken on the lines of t − 2. Pennsylvania's 7th and 15th specials of 2018 are the cases where this matters.
- **inc**: +1 if a Democratic incumbent runs, −1 if a Republican one does, 0 for an open seat. It comes from Cha, Kuriwaki and Snyder, and for the Senate before 2006 it is inferred (below).
- **lag** (governors only): the Democrat's two-party share in the state's last governor race before year t that a Democrat and a Republican led (Cha, odd years and specials included). It is recorded in `forecast_inputs.last_governor_race`. *Reason:* item 5 of §0.
- **a_t**: the year's national swing. It is forecast from whether t is a midterm and from the sitting president's party (National Archives): a_t = c₀ + c_mid·M·P + c_on·(1−M)·P + d.
- **e**: the race's own error, independent across races given a_t.

**Earlier cycles only.** The forecast for year t is fitted on the level's cycles before t and nothing later (*reason:* item 2 of §0).
- Its national sd is the regression's own prediction sd from those cycles, s_a·√(1 + z(Z′Z)⁻¹z′). This counts both the swing's spread about the national terms and the terms' own uncertainty when few cycles fit them.
- The forecast is normal, with sd √(national sd² + s_e²). A Student-t with 4 degrees of freedom and the same sd stands beside it.
- Every year's fitted terms are in the file's `model`, with the formulas for the mean and the sd (`mean_is`, `sd_is`), so a reader can rebuild each forecast.

**How far back each fit reaches.**
- **Senate, from 1982.**
  - MEDSL's U.S. Senate 1976-2024 adds 380 races of 1982-2004 to Cha's 319 of 2006-2024.
  - 1982 is the first year whose seats' previous regular election, six years before, is in MEDSL, and incumbency is inferred from it. A candidate is the incumbent if their last name is that of the winner of the seat's previous regular election, or of a special in the state in the years between.
  - MEDSL marks no incumbents, so this is **inferred**. On the 295 Senate races of 2006-2024 where both exist, it agrees with Cha's hand coding in 286 (96.9%). The nine that differ are listed in `backtest.json`.
  - Left out before 2006: specials, since whose seat it was, and who held it, is not in the record; and Georgia and Louisiana races whose leader had under half the vote.
- **House, from 2006.** The Downballot's district presidential vote begins on the 2006 lines. Its 2006-2010 sheet also gives the 2000 vote on those lines. But which states kept the same lines in 2002 and 2004 is not stated in any source read here, so 2002 and 2004 are not added.
- **Governors, from 2010**, the first even year in which most states' last governor race is in Cha, which begins in 2006. Of 2008's eleven races, only New Hampshire's and Vermont's have one.

**What each year's fit gives** (2024's, on every earlier cycle):

| Level | Cycles | Races fitted | b_lean | b_inc | b_lag | s_e | national sd, 2024 | sd | ρ |
|---|---|---|---|---|---|---|---|---|---|
| House | 2006-2022 (9) | 3,424 | 0.807 | 0.056 | | 0.050 | 0.019 | 0.054 | 0.12 |
| Senate | 1982-2022 (21) | 667 | 0.574 | 0.091 | | 0.074 | 0.023 | 0.078 | 0.09 |
| Governor | 2010-2022 (7) | 175 | 0.393 | 0.050 | 0.206 | 0.066 | 0.022 | 0.069 | 0.10 |

The Senate's b_lean is lower and its s_e higher than in D2-v1's fit on 2006-2024 alone (0.746 and 0.058). On these figures, Senate races of the 1980s and 1990s followed the presidential vote less closely, and a fit on earlier cycles carries that.

### 2.3 The back-test, and the fewest cycles a fit needs

Every year is forecast from a fit on its earlier cycles only, which is the method of record (`chambers.py backtest`; `backtest.json`, scheme `earlier`), and scored against the result:

| Level | Years | Races | z sd | 50 / 80 / 95% coverage | Mean log score | National swing's misses, z rms | Within 49-51%: expected, seen |
|---|---|---|---|---|---|---|---|
| House | 2014-2024 | 2,286 | 0.77 | 61 / 91 / 98.5% | 1.60 | 0.76 | 58.8, 76 |
| Senate | 2006-2024 | 319 | 0.83 | 56 / 90 / 98% | 1.24 | 0.96 | 14.0, 21 |
| Governor | 2020-2024 | 58 | 1.11 | 64 / 79 / 91% | 1.14 | 2.45 | 3.8, 2 |

**The fewest cycles.**
- **Why at least four.** A fit cannot have fewer than four cycles: three for the national swing's terms and one degree of freedom for its spread.
- **Why both parties.** Its cycles must hold presidents of both parties, or the midterm and presidential-year terms cannot both be fitted. Obama was in office in every governor cycle of 2010-2016, and a Republican in every Senate cycle of 1982-1992.
- **What the back-test shows.** It was run with fits on only the k cycles before each year, for k = 4 to 12. `backtest.json` keeps the windows of 4, 5, 6, 8 and 10 cycles.
  - *Race forecasts.* For the House and the Senate, no k from four up gives race forecasts that are too narrow. The 95% interval held at least 96% of races under every k, and the House's one four-cycle fit of record (2014) held 98.6%, with z sd 0.74.
  - *The national swing* is less well judged on few cycles. Its z rms is 1.1 to 2.8 on four to seven cycles, and about 1 from eight. That matters more to control than to a seat's p.
- **The choice.** So four cycles, with presidents of both parties, is the fewest a fit needs (`K_MIN`). Each year uses every earlier cycle, as D1 and D3 do.

**What the back-test says of the forecasts.**
- **The House and the Senate run wide.** Their z sd is 0.77 and 0.83, and the 95% interval holds 98-99% of races.
  - The early fits have the wider race error of the past: the House's s_e was 0.0568 in M2's first earlier-cycles fit, against 0.0489 on all cycles (M2 §2.3), and the Senate's fit carries the 1980s and 1990s.
  - A forecast too wide puts too little density at a close race's centre, so p is if anything a little low.
  - A fit on only the last five or six cycles scores better on races: a log score of 1.72 against 1.63 for the House over 2016-2024, and 1.30 against 1.21 for the Senate over 2002-2024. The price is a national swing judged overconfident (z rms 1.1 to 2.8). Not adopted; for the orchestrator to weigh.
- **Governors run slightly narrow** on their 58 races, with z sd 1.11 and 91% in the 95% interval.
  - Their national swing runs narrow by a long way. 2020's swing missed by 3.8 national sds: fitted on five cycles, the national sd was 0.012.
  - The sample is three years.
- **Seats.** Among contested races, the Democrats' seats fell outside their 80% interval three times: in the House in 2020 (203 won, 221.8 expected), and in the Senate in 2006 and 2008 (22 and 19 won, 16.6 and 13.6 expected).

**Marked.** *No polls are used*, so the model's own forecast carries less than forecasters then knew. Where 538's forecast stands first, the polls are in.

**Found since D2-v1's approval, not changed.** The fit takes 44 House specials with the year's own lines, not the old Congress's. Refitting D2-v1 without them moved b_lean from 0.814 to 0.812. The forecasts in the files use the old lines (above).

## 3. Structures, and where p is not computed

- **Uncontested** (one candidate on the ballot): p = 0, said so.
- **No Democrat or no Republican among the top two**: not computed, since both forecasts are of a Democrat against a Republican. This covers an independent or minor party second, and two candidates of one party (California and Washington top-two; Connecticut 2006, where Lieberman ran on a Democratic and a third-party line). An independent who caucuses with the Democrats (Sanders, King) stands as the Democrat, as in 538's rows.
- **Georgia** (a majority is required, else a runoff): not computed with three or more candidates. **Louisiana**'s open primary: not computed. **Ranked choice** in Maine (2018 on) and Alaska (2022 on): not computed. **Vermont governor**, which the legislature chooses if no one has a majority: not computed with a third candidate on the ballot. The result is recorded in every case, and 538's forecast is kept where it has one.
- **Missing district input**: no 2020 presidential vote on the 2024 lines in Alabama, Louisiana and North Carolina; none for 2008 on California's 2012 lines; none for 2012 on Florida's 2016 lines.
- **Too few earlier cycles** (§2.3). The House of 2006-2012 and the governors of 2006-2016 have no forecast of the model's own, and 538's files for those years give chances without shares, so p is not computed, with that reason.
  - Control of the House in 2006-2012 is not computed either, since the chamber stage needs the model's common swing.
  - The chamber check (§4) is still made.
- **No last governor race.** A governor race in a state with no earlier race in Cha that a Democrat and a Republican led gets no forecast of the model's own.
- **Specials held apart from November.** The November record leaves out specials held on other dates. Cha, Kuriwaki and Snyder hold 42 such House contests and Massachusetts's Senate special of January 2010. They are added with Cha as their record (`certified` null, with no second source) and p not computed, since both forecasts are of November's general election. Their dates are not in the sources read here, except Massachusetts's: 19 January 2010, from Senate.gov. Eight of 2024's are among them (CA-20, CO-04, NJ-10, NY-03, NY-26, OH-06, TX-18, WI-08). The FEC has no 2024 volume, so they come from Cha, as the orchestrator agreed for want of the FEC.

## 4. Control of the chamber (exact form, MATH §4.2)

p(control) = p(seat) × P(the other seats leave control to this one | this seat tied).
- **Each seat** is y_i = μ_i + λ_i·d + e_i. Here d ~ N(0, s_a²) is the common swing (s_a here is the year's national sd), and e_i ~ N(0, s_e,i²) is the seat's own error. `stage_two.inputs` gives μ_i (`mean`), s_e,i (`own_sd`) and λ_i (`swing_loading`).
- **The common swing is conditioned on the tie**: d | tie ~ N(λ·s_a²·(½ − μ)/sd², s_a²·s_e,i²/sd²), with sd² = λ²s_a² + s_e,i².
- **The other seats' distribution** is computed exactly, by dynamic programming over seats on a grid of the swing. Where the swing given a tie is narrower than three grid steps, the other seats are counted afresh on a fine grid around it. No seat of 2006-2024 needed it.

**Whose forecast of the seat** (the brief, item 4, reading (c); *reason:* one forecast of the seat throughout its figure, M2 2.6):
- **The model's own**: its mean, s_e,i = the model's s_e, and λ = 1.
- **538's**, where 538's p stands first: 538's mean and implied sd are the seat's marginal, with s_e,i = √(sd₅₃₈² − s_a²) and λ = 1, as the presidency treats 538's marginals. Before, the seat's chance of a tie was 538's, but what a tie told the chamber was the model's.
- **Where 538's sd is not above s_a**, no seat can carry the whole swing and keep 538's sd. This is 23 seats: New Hampshire's 1st in 2022, twelve Senate races of 2014, six of 2016 and four of 2022.
  - Such a seat carries λ = sd₅₃₈·√ρ ÷ s_a of the swing, with s_e,i = sd₅₃₈·√(1 − ρ) and ρ the model's own s_a² ÷ (s_a² + s_e²).
  - Its sd stays 538's, and its correlation with the swing is the model's.
  - These seats are marked in `marginal_note`.
- **Each forecast in `p.alongside`** has its own `control`, with P(decides | tie) conditioned on that forecast's mean and sd. The t4 figure uses the normal with the same mean and sd. The other seats are the same for all of them.

What decides control:
- **House:** 218 of 435.
- **Senate:** 51, or 50 with the Vice President, with the seats not up and the independents counted by caucus. A Senate special whose term ends when the new Senate meets (California 2022 and 2024; Illinois 2010, in Senate.gov's words) is not part of control.

**How each seat enters** (`stage_two.inputs.entered_as`):
- *model*: the model's own forecast, sharing the common swing.
- *inferred*: a structure whose p is not computed, entered as the model's two-way forecast. This covers Georgia's runoffs, Louisiana, and ranked choice (King in Maine from 2018 among them). Seats with no earlier presidential vote on their lines use the same day's presidential vote, stated as same-day.
- *fixed*: settled by who was on the ballot, known before the election. Only Democrats on the ballot is fixed D. No Democrat and no caucusing independent is fixed not-D: same-party top two, a Republican against minor parties, and Osborn and McMullin, who said they would join neither caucus. No seat is ever fixed at its result.

**Seats not up** (Senate): each is held by the winner of its latest election before the year, counted by caucus. Winners come from Cha, Kuriwaki and Snyder from 2006 on, runoffs included, and from MEDSL's Senate returns for seats last elected in 2002 and 2004. Each is listed in `chamber.seats_not_up_list`.

**The check on every chamber-year** (`chamber.check`): the seats not up plus the seats won, against the division the new Congress opened with (Senate.gov; House History). All 20 agree but two, and each of the two is a seat vacant at the opening. The House of 2006-2012 is checked although its control is not computed.
- Minnesota's Senate seat in January 2009, contested; Franken (D) was seated in July. We count 59 against 56 + 2 independents + 1 vacant.
- New York's 22nd in January 2021, uncertified; Tenney (R) was seated in February. We count 213 R against 212.

**The Vice President.** In midterms it is the sitting one: Cheney (R) in 2006, Biden (D) in 2010 and 2014, Pence (R) in 2018, Harris (D) in 2022. In presidential years the VP is elected the same day, and P(the VP is a Democrat) is the presidential chance (the brief, item 1). *Reason:* the Senate's control in a presidential year turns on who becomes Vice President. It comes from D1's record of the year, in `chamber.vice_president`, with `by`, `as_of` and `note`:

| Year | P(VP Democrat) | Whose |
|---|---|---|
| 2008 | 0.954 | the model's own, on 538's national average of 3 November |
| 2012 | 0.552 | the model's own, on 538's national average of 5 November |
| 2016 | 0.7137 | 538, polls-plus, 7 November; any other ticket counts as not Democratic |
| 2020 | 0.8932 | 538, polls-plus, 2 November |
| 2024 | 0.529 | the model's own, on the 12 September average (D1's horizon for 2024, M2 3.5) |

- **Whose chance.** It is 538's where 538's forecast stands first in D1's record of the year. Otherwise it is the model's own chance that the Democrat wins the College (`pipeline/own_forecast.py`, `college_prob` on the approved forecast): states are counted whole, and a 269 tie counts half.
- **Independence.** It is taken as independent of the Senate's common swing.
- **How far it moves control** is shown in each seat's `P_decides_given_tie_if_VP_D` and `_if_VP_R`. For Montana 2024, P(decides | tie) is 0.091 at 0.529, 0.115 with a Democratic VP and 0.064 with a Republican.

## 5. Results

| Year, level | Contests | p computed | 538 first | p = 0 | not computed | largest p | largest p for control |
|---|---|---|---|---|---|---|---|
| 2006 Senate | 33 | 31 | 0 | 0 | 2 | North Dakota, 1 in 129,966 | Rhode Island, 1 in 7,575,318 |
| 2006 House | 438 | 0 | 0 | 30 | 408 |  |  |
| 2006 Governor | 36 | 0 | 0 | 0 | 36 |  |  |
| 2008 Senate | 35 | 31 | 0 | 0 | 4 | Wyoming special, 1 in 165,138 | South Dakota, 1 in 3,171,475 |
| 2008 House | 443 | 0 | 0 | 24 | 419 |  |  |
| 2008 Governor | 11 | 0 | 0 | 0 | 11 |  |  |
| 2010 Senate | 39 | 32 | 0 | 1 | 6 | North Dakota, 1 in 117,368 | Delaware special, 1 in 7,817,401 |
| 2010 House | 441 | 0 | 0 | 10 | 431 |  |  |
| 2010 Governor | 36 | 0 | 0 | 0 | 36 |  |  |
| 2012 Senate | 33 | 33 | 0 | 0 | 0 | North Dakota, 1 in 149,071 | North Dakota, 1 in 1,743,485 |
| 2012 House | 441 | 0 | 0 | 10 | 431 |  |  |
| 2012 Governor | 11 | 0 | 0 | 0 | 11 |  |  |
| 2014 Senate | 36 | 32 | 32 | 1 | 3 | Alaska, 1 in 29,076 | Alaska, 1 in 119,759 |
| 2014 House | 440 | 358 | 0 | 27 | 55 | California 31, 1 in 38,498 | California 21, 1 in 4,114,717 |
| 2014 Governor | 35 | 0 | 0 | 0 | 35 |  |  |
| 2016 Senate | 34 | 30 | 26 | 0 | 4 | Nevada, 1 in 116,765 | Nevada, 1 in 560,252 |
| 2016 House | 439 | 344 | 0 | 22 | 73 | California 21, 1 in 47,094 | California 21, 1 in 3,982,191 |
| 2016 Governor | 12 | 0 | 0 | 0 | 12 |  |  |
| 2018 Senate | 35 | 32 | 30 | 0 | 3 | Montana, 1 in 95,378 | North Dakota, 1 in 591,168 |
| 2018 House | 442 | 383 | 273 | 15 | 44 | New Mexico 2, 1 in 33,196 | California 10, 1 in 1,974,163 |
| 2018 Governor | 36 | 34 | 34 | 0 | 2 | South Dakota, 1 in 59,094 |  |
| 2020 Senate | 35 | 30 | 28 | 0 | 5 | Alaska, 1 in 87,769 | Alaska, 1 in 734,565 |
| 2020 House | 440 | 398 | 288 | 10 | 32 | Oklahoma 5, 1 in 49,401 | California 21, 1 in 8,742,042 |
| 2020 Governor | 11 | 11 | 0 | 0 | 0 | Vermont, 1 in 131,259 |  |
| 2022 Senate | 36 | 32 | 31 | 0 | 4 | New Hampshire, 1 in 95,632 | Nevada, 1 in 379,004 |
| 2022 House | 444 | 390 | 292 | 15 | 39 | New Hampshire 1, 1 in 20,079 | New Hampshire 1, 1 in 1,057,210 |
| 2022 Governor | 36 | 33 | 30 | 0 | 3 | Nevada, 1 in 134,249 |  |
| 2024 Senate | 35 | 33 | 0 | 0 | 2 | Delaware, 1 in 226,306 | Delaware, 1 in 2,681,141 |
| 2024 House | 443 | 373 | 0 | 13 | 57 | California 22, 1 in 45,994 | California 22, 1 in 1,160,494 |
| 2024 Governor | 11 | 10 | 0 | 0 | 1 | Delaware, 1 in 224,785 |  |

**In all.**
- 4,997 contests.
- 2,650 with p computed, 1,064 of them under 538's forecast.
- 178 with p = 0.
- 2,169 not computed, each with its reason. 1,614 of them are for too few earlier cycles: the House of 2006-2012 and the governors of 2006-2016.

p is under the normal forecast. The t4 figure and the other forecasts' figures sit beside it in `p.alongside`, each with its own `control`.

**Sums of p, before and now.** Before is D2-v1, on `main` at #27. Each cell sums p over a level and year's contests; control likewise.

| Year | House: p before | now | control before | now | Senate: p before | now | control before | now | Governor: p before | now |
|---|---|---|---|---|---|---|---|---|---|---|
| 2006 | 2.3836e-03 | 0 | 2.4729e-05 | 0 | 6.2028e-05 | 5.1168e-05 | 6.5191e-06 | 1.0845e-06 | 8.4350e-05 | 0 |
| 2008 | 1.3355e-03 | 0 | 2.7653e-05 | 0 | 5.0764e-05 | 3.9609e-05 | 3.1441e-06 | 1.7509e-06 | 2.1183e-05 | 0 |
| 2010 | 1.9235e-03 | 0 | 4.7720e-05 | 0 | 4.1985e-05 | 4.4840e-05 | 4.1767e-07 | 6.4503e-07 | 6.0074e-05 | 0 |
| 2012 | 1.0298e-03 | 0 | 3.8930e-06 | 0 | 4.3513e-05 | 3.8629e-05 | 5.7387e-06 | 3.9831e-06 | 2.5555e-05 | 0 |
| 2014 | 1.1807e-03 | 1.0883e-03 | 1.2097e-06 | 6.8564e-06 | 8.5496e-05 | 8.5495e-05 | 1.2099e-05 | 1.7482e-05 | 4.5038e-05 | 0 |
| 2016 | 7.3922e-04 | 6.4762e-04 | 6.2895e-06 | 8.0010e-06 | 2.8091e-05 | 2.6970e-05 | 2.7267e-06 | 5.2616e-06 | 2.4344e-05 | 0 |
| 2018 | 1.6701e-03 | 1.6685e-03 | 3.6877e-05 | 2.4589e-05 | 5.1208e-05 | 5.1602e-05 | 4.2331e-06 | 4.8308e-06 | 8.9209e-05 | 8.9209e-05 |
| 2020 | 1.0723e-03 | 1.0702e-03 | 2.6549e-06 | 5.0971e-06 | 4.4909e-05 | 4.4422e-05 | 6.5634e-06 | 4.9942e-06 | 1.7934e-05 | 2.0575e-05 |
| 2022 | 1.7143e-03 | 1.7145e-03 | 3.1507e-05 | 3.1041e-05 | 3.6283e-05 | 3.6584e-05 | 6.2713e-06 | 6.5364e-06 | 5.3213e-05 | 5.3741e-05 |
| 2024 | 5.9776e-04 | 5.9743e-04 | 2.1241e-05 | 2.1313e-05 | 2.2470e-05 | 2.2805e-05 | 1.5766e-06 | 2.2460e-06 | 1.7088e-05 | 1.4931e-05 |
| **All** | 1.3647e-02 | 6.7866e-03 | 2.0377e-04 | 9.6897e-05 | 4.6675e-04 | 4.4212e-04 | 4.9289e-05 | 4.8815e-05 | 4.3799e-04 | 1.7846e-04 |
| contests with p | 3,730 | 2,246 |  |  | 316 | 316 |  |  | 218 | 88 |

- **Where p is lost.** The House of 2006-2012 and the governors of 2006-2016 now have no p (above).
- **Where p moves most.** The House of 2014 and 2016 is lower by 8% and 12%: this is the fit on earlier cycles, whose effect M2 measured (3.4). The Senate of 2006 and 2008 is lower by 18% and 22%: its fit now runs over 1982-2004, with a wider race error (s_e 0.081, against 0.053 under D2-v1 for 2006). Governors in 2020 are 15% higher and in 2024 13% lower, with the last race's term.
- **Control.** The control sums move with 538's seats entering under their own marginal. In a midterm whose seats are nearly all 538's, that is most of the change: Senate 2014 rises from 1.21 × 10⁻⁵ to 1.75 × 10⁻⁵. In presidential years the Vice President moves them too: Senate 2016 rises from 2.73 × 10⁻⁶ to 5.26 × 10⁻⁶.

### Historical check (MATH §8.2 iv), 2006-2024

Over all contests with p, the expected number decided by k votes or fewer is computed under the forecast each p used, and set against the number seen (`chambers.py history`, `history.json`). k = 1 is the event itself. Larger k test the same forecasts where there are cases to count.

| Level | Contests | within 1 vote | within 10 | within 100 | within 1,000 | within 5,000 | within 10,000 | within 20,000 |
|---|---|---|---|---|---|---|---|---|
| House | 2,246 | 0.014 vs 0 | 0.14 vs 1 | 1.4 vs 1 | 13.6 vs 16 | 67.9 vs 66 | 135.7 vs 125 | 272.6 vs 268 |
| Senate | 316 | 0.001 vs 0 | 0.009 vs 0 | 0.09 vs 0 | 0.88 vs 1 | 4.4 vs 5 | 8.8 vs 8 | 17.4 vs 18 |
| Governor | 88 | 0.000 vs 0 | 0.004 vs 0 | 0.04 vs 0 | 0.36 vs 0 | 1.8 vs 0 | 3.6 vs 0 | 7.1 vs 4 |

- **House and Senate.** The forecasts pass at every k. The one House race within ten votes is Iowa's 2nd of 2020, at 6 votes. The Senate race within 1,000 is Minnesota 2008, at 312.
- **Governors.** Among the 88 races left with p, none finished within 10,000 votes, against 3.6 expected (a Poisson chance of 3%), and 4 finished within 20,000, against 7.1 expected.
  - Before this round the count was 0 within 5,000 votes against 4.4 expected, over 218 races. M2 found that specific to the 5,000-vote line, and the forecast then slightly too wide (M2 3.1, 3.2).
  - On the 88 races left, the evidence is thinner either way.

## 6. Two sources, differences listed (plan §3a)

Every House and Senate contest in the record is checked against Cha, Kuriwaki and Snyder, and the differences are kept in `checks`. The source of record wins.
- **Most differences** are small candidates (under ten votes) and blank or write-in lines, which the check source leaves out by design.
- **Real ones**: 2022 IL-03 (Ramirez 177,759 at the FEC, 121,764 in the check), 2024 Missouri Senate (W. C. Young 35,671 at the Clerk, 21,111 in the check), and 2012 AL-03 (Harris 98,141 at the FEC, 91,141 in the check).
- **Fixed in the record's reading**:
  - A fusion candidate's lines filed under two FEC ids are one candidate's. Connecticut's Senate race of 2010 is the case: Blumenthal's Democratic and Working Families lines now sum to 636,040, as the check has. Each merge is noted in the contest.
  - FEC rows with no candidate are not contests: a "California" row in 2018, and two Ohio rows in 2006.

## 7. Not yet

- **Population before 2022.** The ACS table-based files on www2.census.gov begin with 2021. The older sequence-based summary files there hold the same table and are the next step. The Census API wants a key, which needs an email, so it is not used.
- **A second source for governors** (MEDSL precinct files, 2016, 2022 and 2024).
- **Odd-year governors** (Virginia, New Jersey, Kentucky, Louisiana, Mississippi), which are in Cha.
- **Earlier than 2006, for the fits.** The Senate's fit now reaches 1982 (§2.2).
  - *Governors.* Returns before 2006 would bring back the model's own forecast for 2014-2018 at least. Algara and Amlani's county returns (governor 1865-2020, CC0, an R file) are the lead. Klarner's Governors Dataset (CC0), read here, holds governors and terms but no vote counts.
  - *House.* The FEC's 2002 and 2004 volumes, with The Downballot's 2000 vote on the 2006-2010 lines, would add 2002 and 2004 if a source states which states kept their lines. That would bring back 2012, since 2002-2010 includes a Democratic president only in 2010.
- **The House of 2006-2012 and the governors of 2006-2016** have no p (§3). There are two ways to give them one, neither taken:
  - borrow the national swing's terms from a level with more cycles (the Senate's, fitted from 1982);
  - for governors, use a forecast without the last-race term, whose fits would reach 2014.
- **2026.** Not built: no standardized source holds its count yet (held 2026-11-03). Once one does, the files carry it marked as an unofficial count with its date, until it is certified.
