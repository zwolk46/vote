# Senate, House and governor: sources, method and checks

*Worker D2 (`briefs/D2-data-congress.md`, amended 2026-11-07 03:13, 05:58, 06:36 and 07:04 UTC). Written 2026-11-07 and revised three times the same day (last at 07:20 UTC): for the follow-ups from M2 (§0.3), for the orchestrator's third round (§0.2) and for its fourth, the near-ties (§0.1). It covers every Senate and House race of the even years 2006 to 2024, and every governor race of the even years 1978 to 2024, that the sources hold, with p, and control of the Senate and the House.*

## 0. What each round changed

### 0.1 Round 4 (the orchestrator, 2026-11-07 07:04 UTC): the near-even shortfall

**What was asked.** Round 3's back-test found more races finishing within 49-51% than the forecasts expected: 113 against 89.3 in the House, 30 against 21.6 in the Senate. The orchestrator asked for D3's rule of #31: a near-tie calibration fitted on earlier years only, adopted only if it improves the out-of-sample test. *Reason, in its words:* "about 20% too few near-even finishes means p near even is about 20% low. That understates exactly the races law 1a says the site must show, and k cannot reach it because it moves the spread, not the shape."

**What was done** (§2.6).
- **The rule.** The forecast's density within one point of ½ is multiplied by a factor fitted on earlier years' out-of-sample near-ties, and the forecast renormalized. So the model's own p is multiplied by that factor over the renormalization.
- **The two schemes tested.** One factor per level, and a factor by band of |mean − ½|. Both were scored on 2010-2024 at 49-51, 48-52 and 45-55%, with coverage and log score.
- **Adopted: one factor per level, for the House and the Senate.** It raises the log score (House 1.5736 to 1.5743, Senate 1.2984 to 1.3017) and brings every count nearer the one seen. In the safe seats' band it stays below the count seen, so no safe seat's p is raised beyond what the record at its distance shows.
- **Not adopted for governors.** Both schemes lower their log score.
- **Where it applies.** 2,246 contests: the model's own p for the House and the Senate of 2010-2024. Each forecast records its `calibration` (factor, multiplier, fitting years), and p's `under` ends "calibrated to earlier years' near-ties".
- **538's forecasts are not calibrated.** They show no shortfall: where 538 stands first, 40 House races finished within 49-51% against 50.6 expected.

**Sums, before and after** (§5):

| Level | Sum of p, before | after | Control, before | after |
|---|---|---|---|---|
| House | 9.903e-3 | 1.0158e-2 | 1.371e-4 | 1.418e-4 |
| Senate | 4.413e-4 | 4.444e-4 | 4.799e-5 | 4.876e-5 |
| Governors | 9.893e-4 | 9.893e-4 | | |

- **Where p rises and falls.** The House of 2024 rises 26% (factor 1.295) and the Senate of 2024 21% (1.229). The House and Senate of 2010 fall 11%: the factor fitted on the years before 2010 is 0.886, since those years had fewer near-ties than expected.
- **What it does not reach.** The counts at 48-52% and 45-55% stay short (House 166.6 against 209, and 422.6 against 521). The House's results land about 1.5 points nearer ½ than its means in races 5 to 20 points from even. That is a question for the means, and it is left open (§7).

### 0.2 Round 3 (the orchestrator, 2026-11-07 06:36 UTC), each item with its reason

1. **Governors from 1978, from Algara and Amlani's county returns.** *Reason, in the orchestrator's words:* "the maker wants as much data as can be found, and this both adds races and restores p."
   - **The source.** Algara and Amlani's county returns for governor, 1865-2020 (Harvard Dataverse, CC0 1.0, no guestbook). They are taken by script (`algara_amlani.py`), and the file's MD5 is checked against the one Dataverse publishes. The file is R's own format, and this environment has no R, so `rdata_reader.py` reads it from R's published description of the format, with no package added.
   - **What is built from it.** The county returns are summed to the state, and the 327 governor races of the even years 1978-2004 are added as contests (`data/governor/1978.json` to `2004.json`).
   - **What it restores.** The governors' fit now reaches back to 1978, so 2006-2016 are fitted on earlier cycles: 2006 on the 14 cycles of 1978-2004. Governors with p go from 88 to 420.
   - **The last-race term is kept.** Before 2006 the last race comes from Algara and Amlani, odd years included.
   - **Why 1978.** It is the first even year whose earlier presidential vote (MEDSL, 1976 on) and sitting president (National Archives, 1976 on) are in the sources.
   - **Checked against Cha, Kuriwaki and Snyder** over 2006-2020 (§6). Missouri's rows fall short, so Missouri before 2006 is left out of every use (§3).
2. **House 2006-2012: the Senate's national terms, back-tested first.** *Reason:* the orchestrator's test. If the House on the Senate's terms keeps z sd and coverage within a few points of the House's own over 2014-2024, use it for the early years.
   - **It does** (§2.3). Over 2014-2024 (2,286 races) the result is:
     - z sd 0.748, against 0.770 on the House's own terms;
     - coverage 64 / 92 / 98.8%, against 61 / 91 / 98.5%;
     - log score 1.633, against 1.603.
   - So the House of 2008-2012 takes the Senate's national terms, fitted on the Senate's own earlier cycles. Its lean, incumbency and race-error terms are fitted on its own earlier cycles. Each such file's `model.national_from` marks it "national terms from the Senate's earlier cycles".
   - **The House of 2006 has no earlier House cycle** to fit those terms on, so it stays not computed. FEC 2004 would be needed (§7).
   - The House gains p for 1,116 contests, and its control is now computed for 2008-2012.
3. **The spread, calibrated on earlier cycles only.** *Reason, in the orchestrator's words:* "a forecast wider than the record supports understates p, which tilts the site toward the maker's own claim (law 1a). The forecast should be as sharp as the record allows and no sharper."
   - **What is done.** Each level's sd, both the national part and the race's own, is multiplied by k. k is the root mean square of the standardized errors of that level's earlier years, each year forecast out of sample from its own earlier cycles. It applies once three such years exist.
   - **What it improved.** The log score at every level, and z sd moved nearer 1 (§2.4).
   - **Two factors, no better.** A separate factor for the national part was tested. It improved nothing that matters, and it made the national misses worse.
   - **Narrowing does not raise every p.** It raises p in races within one sd of even and lowers it in the rest. So the House sum of 2024 fell 11% (§2.4).
   - **The governors' national z rms of 2.45 was the small sample** (§2.5). Over 1986-2024 it is 1.29. Counting the noise in an eleven-race year's own swing, it is 0.91. 2020 stands as the one real miss, at 2.6 sd.

**What changed, in totals** (round 2, on `main` at b00c55e, against now):

| | Contests | p computed | 538 first | p = 0 | Not computed |
|---|---|---|---|---|---|
| Round 2 | 4,997 | 2,650 | 1,064 | 178 | 2,169 |
| Now | 5,324 | 4,098 | 1,064 | 178 | 1,048 |

- **The House.** p for 3,362 contests (2,246 before). 873 are not computed, 368 of them for too few cycles (2006).
- **The Senate.** Unchanged at 316.
- **Governors.** 562 contests (235 before); p for 420 (88 before); 142 not computed. Of these 142:
  - 89 for too few cycles (1978-1984);
  - 7 for Missouri's count;
  - 9 where the others' total could hide a top-two candidate;
  - 2 with no last race;
  - 35 for the structures of §3.

The sums of p by level and year are in §5.

### 0.3 Round 2: the follow-ups from M2 (brief, amended 2026-11-07 05:58 UTC), each with its reason

M2 checked every p (`checks/M2-REPORT.md`) and the orchestrator decided its readings. These stand. Where round 3 changed a figure, it says so in brackets.

1. **The Vice President's tie vote in presidential years is the presidential chance**, not one half (§4). *Reason:* the Senate's control in a presidential year turns on who becomes Vice President.
   - It is 538's where 538's forecast stands first in D1's record of the year. In 2016 and 2020 that is its polls-plus chance that the Democratic ticket wins, 0.7137 and 0.8932.
   - Otherwise it is the model's own chance that the Democrat wins the College: 0.954 in 2008, 0.552 in 2012 and 0.529 in 2024.
2. **The model's own forecast is fitted on earlier cycles only.** It never leaves one cycle out, and its national sd comes from those cycles too. The Senate's fit reaches back to 1982 through MEDSL. A fit needs four cycles, with presidents of both parties among them (§2.3).
   - [Round 3: governors are fitted from 1978, and the House of 2008-2012 is on the Senate's national terms. So only the House of 2006 and the governors of 1978-1984 lack a forecast of the model's own.]

   *Reason:* the model's own forecast is fitted to like past races, from what was known before the election (MODEL §3). A coefficient fitted partly on later years is something no voter knew.
3. **538 is kept on p's error, not the sd's.** It stands first where p's estimated relative error is under 20% (§2.1). *Reason:* the reader sees p, and at z = 3.94 a 7% error in the sd is a 105% error in p (M2 3.9).
4. **Control under 538, reading (c).** A seat whose p is 538's enters the chamber stage with 538's mean and sd as its marginal (§4). *Reason:* one forecast of the seat throughout its figure (M2 2.6).
5. **Governors carry the state's last governor race** as a predictor. It took the log score from 1.064 to 1.143 (M2's A4).
   - [Round 3: the back-test now covers 1986-2024, 448 races (§2.3).]
6. **The files reproduce themselves.** Mean and sd are at full precision. Every p block holds f(½) and names the forecast it is computed from (`of_forecast`). The p = 0 blocks name their script and commit. *Reason:* law 4: a reader recomputing p from the file gets the file's p.
7. **One fetch and one FEC intake.**
   - Every D2 intake script downloads through `pipeline/fetch.py`.
   - D1's `fec_president.py` is now `fec_federal_elections.py president`, with output identical to before.

   *Reason:* one implementation of each thing.
8. **Senate 2014's chances stand as exact**, because they have no step at any plausible run count (M2 3.7).

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
| `candidates_american_general_elections.py` | Cha, Kuriwaki and Snyder, *Candidates in American General Elections*, doi:10.7910/DVN/DGDRDT, v4.1 | House, Senate, governor 2006-2024 (odd years too), hand-coded incumbency | CC0 1.0 | 2026-11-07 |
| `algara_amlani.py governors` (with `rdata_reader.py`) | Algara and Amlani, *Replication Data for: Partisanship & Nationalization in American Elections*, doi:10.7910/DVN/DGUMFI, v1.1: county returns for governor, 1865-2020 | **governors 1978-2004** (the record), the last governor race before 2006, and the check on Cha's governors of 2006-2020 | CC0 1.0 | 2026-11-07 |
| `downballot_pres_by_cd.py` | The Downballot, presidential vote by congressional district (public Google Sheets) | 2000-2024 presidential vote on the lines of each House election 2006-2024 | none printed | 2026-11-07 |
| `fec_ballot_candidates.py` | FEC, 2024 general election ballot candidates | who sat in Congress in 2024 | none printed; federal record | 2026-11-07 |
| `nara_electoral_college.py` | National Archives, Electoral College pages | president and VP elected, 1976-2024 | federal record | 2026-11-07 |
| `census_acs_population.py` | Census Bureau, ACS 1-year, table B01003 (www2.census.gov table files) | population of each state and district, 2022 and 2024 | federal record | 2026-11-07 |
| `party_divisions.py` | U.S. Senate, *Party Division*; House History, *Party Divisions of the House* | seats by party at the opening of each Congress, with the chambers' notes | none printed; chamber publications | 2026-11-07 |
| `fivethirtyeight_checking_our_work.py` | FiveThirtyEight, `checking-our-work-data` (raw.githubusercontent.com, commit f6d5b2e) | 538's published forecasts by race and day: Senate 2008-2022, House 2010 and 2018-2022, governors 2010, 2018, 2022 | CC BY 4.0 | 2026-11-07 |
| `build_congress.py` | the caches above | builds `data/senate|house|governor/<year>.json` | | |

**Source of record and check.**
- **The House and Senate.** For 2006-2022 the FEC's volume is the record; for 2024 it is the Clerk's. Cha, Kuriwaki and Snyder check every contest, and the differences are kept in `checks` (§6).
- **Governors of 2006-2024.** Cha is the record.
- **Governors of 1978-2004.** Algara and Amlani's county sums are the record, with `certified` null and no second source. Their `checks` say so.
- **The cross-check.** The two governor sources are compared over 2006-2020 (§6). MEDSL's state-office precinct files for 2022 and 2024 (CC0, no guestbook) remain the lead for a third.

**Algara and Amlani, what the record is.**
- **What it holds.** One row per county and election, with the Democratic and Republican nominees' votes, the county's total vote, and the seat's status: an incumbent's party and re-election bid, or an open seat. The authors coded the status from Congressional Quarterly (the dataset's manual, 2021-08-30).
- **What the files show.** The two nominees by name and votes. The rest appear as one line, "others (not named in the source)", which is the county total less the two nominees, so `ballot.others` is null.
- **What it lacks.** Alaska is not in it, since it has no consistent counties. Seven of the 327 races have a county with no count, marked `votes_incomplete`.
- **The date** is the general election day, inferred; the source gives the year.

**Not taken.**
- MEDSL's House file sits behind a Dataverse guestbook that asks for a name and email. Filling it is the maker's call (law 10).
- 538's own forecast pages redirect to abcnews.com.

The full inventory is `data/sources/congress.md`.

## 2. The forecasts

### 2.1 538's published forecast, first where it can be used

The orchestrator's words of 03:46 put "a reachable published forecast" first, with ours as the check; the rules below are his of 04:12 and 04:20. 538's `checking-our-work-data` keeps every race it forecast, each day and each version, with the projected vote share and the chance of winning.

- **Which forecast.** The last one dated before Election Day, recorded as `as_of`. In 2008 and 2010 the file holds one forecast per race, dated Election Day, and it is marked so.
- **Which version.** 538 showed one version by default. No source read here names it: its pages redirect, and its data READMEs do not say. So the version listed first in the repository's rows comes first, and the others stand beside it in `forecasts`. That is *lite* in 2018-2022, *polls-plus* in 2016 and the only version in 2014. This is an orchestrator choice the maker may correct.
- **Mean and sd.** The mean is the Democrat's projected share of the two leading parties' projected vote. The sd is the one a normal needs to give 538's chance: sd = (mean − ½) ÷ Φ⁻¹(chance), marked inferred. 538's own distribution is not normal, so this sd is "the normal that agrees with 538's mean and chance", not 538's.
- **When it is used.** 538 comes first when three things hold:
  - p's estimated relative error is under 20%;
  - no chance is exactly 0 or 1;
  - other candidates hold under 1% of the chance.
- **Where the error comes from.**
  - *The chance's sampling error*, √(q(1−q)/N). N is the number of simulation runs the chances step by: 50,000 in 2018, 40,000 in 2020 and 2022, and 20,000 in 2016, marked inferred. 2014's chances have no step at any plausible run count and are taken as exact (M2 3.7). The chance is moved one standard error either side and carried through Φ⁻¹ at both ends, not linearized. A chance one run from 0 or 1 is unbounded and falls back.
  - *The rounding of the printed shares.*
- **How each error reaches p.** p = φ(z) ÷ (2n·sd), with z = Φ⁻¹(chance) and sd = (mean − ½) ÷ z.
  - An error in the chance moves z. It moves p by |z² − 1| times its relative error in z, which is the sd's.
  - The mean's rounding moves only the sd, so it moves p by its own relative size.
  - The two are added in quadrature, as `p_relative_error`, beside `sd_relative_error` and `z`.
- **Otherwise** ours comes first, with 538's forecast beside it and the reason in `unusable` (a sentence) and `unusable_kind` (a short class).
- **Control of the chamber.** 538's file gives no joint distribution, so the chamber stage is the model's: its common swing and the other seats. A seat whose p is 538's enters it with 538's mean and sd as its marginal (reading (c), §4).

| Level | Races with a 538 forecast | 538 first | Ours first: no share in the file (2008-2012 Senate; 2010) | chance 0 or 1 | p's error 20% or more | other |
|---|---|---|---|---|---|---|
| House | 1,566 | 853 | 400 | 111 | 200 | 2 |
| Senate | 251 | 147 | 94 | 0 | 9 | 1 |
| Governor | 99 | 64 | 32 | 0 | 3 | 0 |

The table is unchanged by round 3. The 2010 House and governor races that 538 forecast without a share now have p under the model's own forecast (governors on their own earlier cycles, the House on the Senate's terms), with 538's chance beside it.

The two "other" House cases are a 538 Democrat not on our ballot (South Carolina 5th, 2018, where 538 names April Freeman and the record has Archie Parnell) and one race with no Democrat or Republican in 538's rows.

### 2.2 The model's own forecast (method D2-v3)

D2-v3 is D2-v2 (round 2, §0.3) with governors fitted from 1978, the House of 2008-2012 on the Senate's national terms, and each level's sd calibrated on its earlier years (round 3, §0.2). It is used where no published forecast can be, and it is always kept beside 538's as the check. For a race in year t, with y the Democrat's share of the two-party vote:

> y = ½ + a_t + b_lean × lean + b_inc × inc [+ b_lag × (lag − ½), governors only] + e

- **lean**: the Democrat's two-party share of the last presidential vote before year t, minus that election's national share (MEDSL).
  - For the House it is taken on the lines in use in year t (The Downballot); for the Senate and governors, in the state (MEDSL).
  - A House special is held on the old Congress's lines, so its lean is taken on the lines of t − 2.
- **inc**: +1 if a Democratic incumbent runs, −1 if a Republican one does, 0 for an open seat.
  - From 2006 it comes from Cha, Kuriwaki and Snyder's hand coding.
  - For the Senate before 2006 it is inferred from MEDSL (below).
  - For governors before 2006 it is Algara and Amlani's seat status: "Democratic Incumbent" +1, "Republican Incumbent" −1, else 0. It is recorded in `forecast_inputs.seat_status`.
- **lag** (governors only): the Democrat's two-party share in the state's last governor race before year t that a Democrat and a Republican led. Odd years and specials are included. It comes from Cha from 2006 and from Algara and Amlani before, and is recorded in `forecast_inputs.last_governor_race`, with its `source`.
- **a_t**: the year's national swing. It is forecast from whether t is a midterm and from the sitting president's party (National Archives): a_t = c₀ + c_mid·M·P + c_on·(1−M)·P + d.
- **e**: the race's own error, independent across races given a_t.

**Earlier cycles only.** The forecast for year t is fitted on the level's cycles before t and nothing later.
- Its national sd is the regression's own prediction sd from those cycles, s_a·√(1 + z(Z′Z)⁻¹z′). This counts both the swing's spread about the national terms and the terms' own uncertainty when few cycles fit them.
- The forecast is normal, with sd k·√(national sd² + s_e²), where k is the calibration factor (§2.4). A Student-t with 4 degrees of freedom and the same sd stands beside it.
- Every year's fitted terms are in the file's `model`, with the formulas for the mean and the sd (`mean_is`, `sd_is`), so a reader can rebuild each forecast.
  - `s_e_fitted` is the fit's race error and `s_e` the one used (k × `s_e_fitted`).
  - `calibration` gives k's years, races and rule.

**How far back each fit reaches.**
- **Senate, from 1982.**
  - MEDSL's U.S. Senate 1976-2024 adds 380 races of 1982-2004 to Cha's 319 of 2006-2024.
  - 1982 is the first year whose seats' previous regular election, six years before, is in MEDSL. A candidate is the incumbent if their last name is that of the winner of the seat's previous regular election, or of a special in the state in the years between.
  - MEDSL marks no incumbents, so this is **inferred**. On the 295 Senate races of 2006-2024 where both exist, it agrees with Cha's hand coding in 286 (96.9%). The nine that differ are listed in `backtest.json`.
  - Left out before 2006: specials, since whose seat it was, and who held it, is not in the record; and Georgia and Louisiana races whose leader had under half the vote.
- **Governors, from 1978.**
  - Algara and Amlani's county returns add 327 races of 1978-2004, of which 311 enter the fit, to Cha's 230 of 2006-2024 that have a last race.
  - A race enters only where both nominees had votes and the others' total is below the smaller nominee's, so no unnamed candidate can have been in the top two. 9 such races are left out of the fit.
  - Missouri is left out before 2006 (§3).
- **House, from 2006.** The Downballot's district presidential vote begins on the 2006 lines. Its 2006-2010 sheet also gives the 2000 vote on those lines. But which states kept the same lines in 2002 and 2004 is not stated in any source read here, so 2002 and 2004 are not added.
  - **The House of 2008-2012 on the Senate's national terms** (round 3, item 2). It has one to three earlier cycles of its own, fewer than the four a fit of the national terms needs.
    - c₀, c_mid, c_on, s_a and (Z′Z)⁻¹ are the Senate's raw fit on its cycles before t (1982 on).
    - b_lean, b_inc and s_e are fitted on the House's cycles before t.
    - The file's `model.national_from` names the Senate's years.
  - The House of 2006 has no earlier House cycle for the second stage, so it is not computed.

**What each year's fit gives** (2024's, on every earlier cycle; and the House of 2008, the first year on the Senate's terms):

| Level, year | Cycles | Races fitted | b_lean | b_inc | b_lag | s_e fitted | k | s_e used | national sd | sd | ρ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| House 2024 | 2006-2022 (9) | 3,424 | 0.807 | 0.056 | | 0.0504 | 0.873 | 0.0440 | 0.0164 | 0.047 | 0.12 |
| Senate 2024 | 1982-2022 (21) | 667 | 0.574 | 0.091 | | 0.0745 | 0.911 | 0.0679 | 0.0213 | 0.071 | 0.09 |
| Governor 2024 | 1978-2022 (23) | 530 | 0.298 | 0.072 | 0.118 | 0.0790 | 0.936 | 0.0739 | 0.0247 | 0.078 | 0.10 |
| House 2008 | 2006 (1), national terms the Senate's of 1982-2006 | 373 | 0.631 | 0.097 | | 0.0600 | 1 | 0.0600 | 0.0245 | 0.065 | 0.14 |

- **The governors' b_lean** is 0.298 on 1978-2022, against 0.393 on 2010-2022 in round 2, and b_lag is 0.118 against 0.206. Governor races of the 1980s and 1990s followed the presidential vote less closely, as the Senate's did.
- **The House of 2008's b_inc** (0.097) is larger than the House's on more cycles (0.056). It is fitted on 2006 alone.

### 2.3 The back-test, and the fewest cycles a fit needs

Every year is forecast from a fit on its earlier cycles only, with the calibration of §2.4. This is the method of record (`chambers.py backtest`; `backtest.json`, scheme `earlier_calibrated`; `earlier` is the same before calibration). Each forecast is scored against the result:

| Level | Years | Races | z sd | 50 / 80 / 95% coverage | Mean log score | National swing's misses, z rms (with the year's own noise) | Within 49-51%: expected, seen |
|---|---|---|---|---|---|---|---|
| House | 2008-2024 | 3,432 | 0.90 | 56 / 86 / 96.9% | 1.53 | 0.96 (0.95) | 89.3, 113 |
| Senate | 1996-2024 | 474 | 0.91 | 53 / 86 / 97.3% | 1.18 | 1.00 (0.88) | 21.6, 30 |
| Governor | 1986-2024 | 448 | 0.95 | 55 / 82 / 95.5% | 1.09 | 1.29 (0.91) | 30.9, 30 |

On 2006-2024 alone, the Senate's z sd is 0.85 (319 races) and the governors' 0.94 (230 races).

**The House on the Senate's terms** (round 3, item 2). The test asks whether the Senate's national terms serve the House where both can be scored: 2014-2024, where the House has four cycles of its own. Stage one is on the House's cycles in every scheme. The table is from `backtest.json`, `house_on_senate_terms`, before calibration.

| House 2014-2024, 2,286 races | z sd | 50 / 80 / 95% coverage | Log score | National z rms |
|---|---|---|---|---|
| the House's own terms | 0.770 | 61 / 91 / 98.5% | 1.603 | 0.76 |
| the Senate's terms | 0.748 | 64 / 92 / 98.8% | 1.633 | 0.28 |
| the Senate's terms, stage one on the last cycle only | 0.836 | 62 / 88 / 97.4% | 1.836 | 0.28 |
| the Senate's terms, stage one on the last 2 cycles | 0.797 | 65 / 90 / 97.8% | 1.820 | 0.28 |
| the Senate's terms, stage one on the last 3 cycles | 0.765 | 65 / 91 / 98.3% | 1.790 | 0.28 |

- **The result.** z sd and coverage stay within three points of the House's own, and the log score is higher. So the Senate's terms are used for 2008-2012.
- **Fewer cycles for stage one** (the last three rows) match 2008-2012, which have one to three earlier House cycles. Those rows score better still, because a fit on few recent cycles carries the recent race error.
- **Scored directly on 2008-2012** (1,146 races): z sd 0.97, coverage 53 / 82 / 95.2%, log score 1.32, national z rms 1.14. 2008's national swing missed by 1.7 sd.
- **Found, not changed.** The Senate's terms also score better than the House's own over 2014-2024. The House's own terms are kept there, since the orchestrator's item asked only about the early years.

**The fewest cycles.**
- **Why at least four.** A fit of the national terms cannot have fewer than four cycles: three for the terms and one degree of freedom for their spread.
- **Why both parties.** Its cycles must hold presidents of both parties, or the midterm and presidential-year terms cannot both be fitted. A Republican was in office in every Senate cycle of 1982-1992.
  - So the Senate is first forecast in 1996, after 1994 brings a Democratic president into its cycles.
  - Governors are first forecast in 1986, the first year with four earlier cycles (1978-1984, under Carter and Reagan).
- **What the back-test shows.** It was run with fits on only the k cycles before each year, for k = 4 to 12. `backtest.json` keeps the windows of 4, 5, 6, 8 and 10 cycles.
  - *Race forecasts.* No k from four up gives race forecasts that are too narrow.
  - *The national swing* is less well judged on few cycles. Its z rms is 1.1 to 2.8 on four to seven cycles, and about 1 from eight. That matters more to control than to a seat's p.
- **The choice.** Four cycles, with presidents of both parties, is the fewest a fit needs (`K_MIN`). Each year uses every earlier cycle, as D1 and D3 do.

**What the back-test says of the forecasts.**
- **More races finish within 49-51% than the forecast expects.**
  - The House: 113 against 89.3, 2.5 Poisson sds above.
  - The Senate: 30 against 21.6, 1.8 above.
  - Governors: 30 against 30.9.

  The expected count is the forecasts' density near even, summed. So this says that, in aggregate, the model's own p of the House and the Senate is low by up to a quarter where races are close. The history by votes (§5) shows a smaller excess for the House, 108 against 99 within 5,000 votes.
  - A single calibration factor cannot fix this. It narrows every race alike, and most races are far from even, so it lowered the expected count (91.9 to 89.3).
  - Why, is open. The close races' means may be better than the model knows, or the error may not be normal in shape. Round 4 calibrates p for it (§2.6).
- **Seats.** Among contested races, the Democrats' seats fell outside their 80% interval five times in 19 chamber-years:
  - the House in 2008 (219 won, 196.6 expected), 2010 (190 won, 226.6 expected) and 2020 (203 won, 221.5 expected);
  - the Senate in 2006 and 2008 (22 and 19 won, 16.6 and 13.6 expected).

  2008 and 2010 are on the Senate's terms, with stage one fitted on one and two cycles. The reading, not tested: an incumbency term fitted on 2006 and 2008 alone (0.097, 0.094) overstated the Democrats' newly won seats in 2010.

**Marked.** *No polls are used*, so the model's own forecast carries less than forecasters then knew. Where 538's forecast stands first, the polls are in.

### 2.4 Calibration of the spread (round 3, item 3)

**The rule.** For year t, k(t) is the root mean square of z = (y − mean) ÷ sd over the level's earlier years. Each of those years is forecast from its own earlier cycles, before calibration (`chambers.py`, `calibration`).
- It applies when at least three such years exist (`CAL_MIN`); otherwise k = 1.
- It multiplies both the national sd and s_e, so the correlation ρ between races is unchanged.
- *Reason:* the orchestrator's: "the forecast should be as sharp as the record allows and no sharper", and the record used is only what came before t.

**k by year:**
- **House:** 2014 0.984, 2016 0.931, 2018 0.904, 2020 0.897, 2022 0.892, 2024 0.873.
- **Senate:** from 1.049 in 2002 to 0.911 in 2024.
- **Governors:** from 0.965 in 1992 to 0.936 in 2024.

Each year's k is in its file's `model.calibration`.

**Before and after,** on the years calibrated:

| Level | Years | Races | z sd | 50 / 80 / 95% coverage | Log score | National z rms |
|---|---|---|---|---|---|---|
| House | 2014-2024 | 2,286 | 0.770 → 0.846 | 61 / 91 / 98.5 → 57 / 87 / 97.7% | 1.603 → 1.632 | 0.76 → 0.85 |
| Senate | 2002-2024 | 378 | 0.856 → 0.865 | 56 / 89 / 97.4 → 55 / 88 / 98.1% | 1.212 → 1.223 | 0.98 → 0.99 |
| Governor | 1992-2024 | 371 | 0.919 → 0.948 | 57 / 83 / 96.0 → 55 / 82 / 95.4% | 1.099 → 1.101 | 1.33 → 1.39 |

- **Adopted at every level.** Each moves z sd nearer 1, coverage nearer 50 / 80 / 95, and raises the log score.
- **Why z sd stays below 1** (a reading). k is fitted on earlier years, and the race error has kept falling, so each year's k is a little larger than the next year's would want.
- **Two factors**, one for the national part and one for the race's own, were tested (scratch script; the same years):
  - log score 1.627, 1.224 and 1.102 for the House, Senate and governors;
  - national z rms 0.84, 1.10 and 2.60.

  The national factor, fitted on a few years' national misses, went to its floor of 0.5 for governors. So one factor is kept.
- **What calibration does to p.** For a normal forecast, d ln p ÷ d ln sd = z² − 1 at the race's z = (½ − mean) ÷ sd.
  - So narrowing raises p in races within one sd of even and lowers it in safer ones.
  - Most House races are safe, so the House's 2024 sum fell 11% at k = 0.873 (5.97 → 5.32 × 10⁻⁴).
  - Its largest p rose: California 22 went from 1 in 45,994 to 1 in 40,376.

### 2.5 The governors' national swing: the small sample, and one real miss

Round 2's back-test gave the governors' national misses a z rms of 2.45 over 2020-2024, on fits of five to seven cycles (2010 on). Two things made it large:
- **The small sample.** Three years, on fits whose s_a had two to four degrees of freedom. With 1978 on, the national sd of 2020 is 0.020 (calibrated 0.019), against 0.012 before.
- **The yardstick's own noise.** The miss is measured against the year's swing as a fit on every cycle estimates it. In an eleven-race presidential year that estimate has noise of about s_e ÷ √11 ≈ 0.024, as large as the national sd itself. `z_with_year_noise` divides by √(national sd² + s_e²/n_races) instead.

Over 1986-2024 (20 years, 448 races) the z rms is 1.29 with calibration, and 0.91 with the year's noise.

**2020 is a real miss.** The model forecast a Democratic year of +1.7 points among the eleven governors, and the year came out −6.4.
- That is −3.9 national sds, or −2.6 counting the year's noise.
- At least one year in twenty beyond 2.6 sd has a chance of about one in five (P(|z| > 2.56) ≈ 1% a year).
- So the record does not show the governors' national term too narrow overall. 2020 is its one large miss.

### 2.6 Near-tie calibration of p (round 4)

*Reason:* the orchestrator's of 07:04, quoted in §0.1.

**The rule.** It is D3's of #31, for the model's own forecast (`chambers.py`, `near_tie_test` and `near_tie`).
- **What it does to the forecast.** The density within one point of ½ (49-51%) is multiplied by a factor F, and the forecast renormalized: Z = 1 + (F − 1)·q, where q is the forecast's own chance of that window.
  - p, the density at ½, is then multiplied by F ÷ Z, recorded as the forecast's `calibration.multiplier`.
  - The forecast's mean and sd are unchanged. So a reader recomputing p from them gets the file's `p.value_uncalibrated`, and that times the multiplier is `p.value`.
- **How F is fitted.** On earlier years only: F makes the expected count in the window equal the count seen, over the earlier years' out-of-sample forecasts. Each of those forecasts is from its own earlier cycles, with k.
- **Whose F.** A level takes its own F where those years expected 30 or more near-ties (D3's minimum, the orchestrator's of 07:37). Otherwise it takes the F of every level's earlier years pooled, again with 30 or more expected. Otherwise no factor applies.
- **The band scheme.** Bands of |mean − ½| are 0-0.05, 0.05-0.10, and 0.10 up. A band takes its own F by level, else pooled over levels, else none. So no safe seat's p is raised on support from closer races.
- **When a scheme is adopted for a level.** It must meet three tests, on the years it reaches:
  - it raises the mean log score;
  - it brings the count within 49-51% nearer the count seen;
  - it does not move the safe seats' count (|mean − ½| of 0.10 or more) further from the one seen.

  Of two schemes that pass, the better log score is adopted.

**The test**, 2010-2024, the years either scheme reaches (`backtest.json`, `near_tie`). Each window cell is expected against seen:

| Level, races | Scheme | Log score | 50 / 80 / 95% coverage | 49-51% | 48-52% | 45-55% | Safe seats, 49-51% |
|---|---|---|---|---|---|---|---|
| House, 3,047 | none | 1.5736 | 56.8 / 86.6 / 97.5 | 78.7 vs 105 | 158.7 vs 209 | 417.1 vs 521 | 13.4 vs 17 |
| | one factor | **1.5743** | 57.0 / 86.9 / 97.5 | 87.5 | 166.6 | 422.6 | 14.5 |
| | by band | 1.5743 | 56.9 / 86.8 / 97.5 | 85.3 | 164.5 | 420.8 | 13.4 |
| Senate, 256 | none | 1.2984 | 54.3 / 91.0 / 98.8 | 11.1 vs 17 | 22.2 vs 34 | 55.9 vs 69 | 2.8 vs 4 |
| | one factor | **1.3017** | 54.3 / 90.2 / 98.8 | 12.1 | 23.2 | 56.6 | 3.1 |
| | by band | 1.2992 | 53.9 / 90.6 / 98.8 | 11.8 | 22.8 | 56.3 | 2.8 |
| Governors, 186 | none | **1.1780** | 59.1 / 86.0 / 96.8 | 12.8 vs 16 | 25.5 vs 31 | 62.1 vs 70 | 1.2 vs 2 |
| | one factor | 1.1752 | 59.1 / 86.0 / 96.8 | 13.7 | 26.3 | 62.8 | 1.3 |
| | by band | 1.1768 | 59.1 / 86.0 / 96.8 | 13.7 | 26.3 | 62.7 | 1.2 |

**What the test shows.**
- **The House and the Senate.** One factor per level passes all three tests and is adopted. The band scheme passes too but scores no better: the same log score for the House to four places with a count further from the one seen, and a lower one for the Senate.
  - In the safe seats' band the one factor moves the House's count from 13.4 to 14.5 against 17 seen, and the Senate's from 2.8 to 3.1 against 4. So the record at their distance supports the raise.
- **Governors.** Both schemes lower the log score, so neither is adopted.
  - In most years their factor would be the pooled one, fitted mostly on House races.
  - Their own earlier years give 0.996 by 2024: 30 near-ties seen against 30.1 expected over 1986-2022.

**The factors.**
- **House.** 2010: 0.886 and 2012: 1.079, both pooled. Then its own: 1.128 in 2014, 1.126, 1.120, 1.220, 1.253 and 1.295 in 2024.
- **Senate.** Pooled throughout, since its own years never expect 30 near-ties: 0.886 in 2010, 1.079, 1.100, 1.120, 1.127, 1.178, 1.199 and 1.229 in 2024.
- **2008 and before.** No factor: the fitting years expected fewer than 30.
- **2010's factor is below one.** The years before 2010 had fewer near-ties than expected, so the rule lowers p in 2010 by about 11%. It is kept, since the rule takes earlier years only.

**What it does not reach.**
- **The wider windows.** The counts at 48-52% and 45-55% stay short, so the excess is not only at the centre.
- **The House's means.** Its results land about 1.5 points nearer ½ than its means, in races 5 to 20 points from even (a reading from the back-test's residuals). Their p may be understated more than any factor at ½ can show. It is open (§7).

**Control.** p for control is the calibrated p times P(decides | tie), which the calibration does not change. The other seats enter the chamber stage under their uncalibrated forecasts. The change is under half a percentage point in a close seat's chance of winning.

## 3. Structures, and where p is not computed

- **Uncontested** (one candidate on the ballot): p = 0, said so.
- **No Democrat or no Republican among the top two**: not computed, since both forecasts are of a Democrat against a Republican.
  - This covers an independent or minor party second, and two candidates of one party (California and Washington top-two; Connecticut 2006, where Lieberman ran on a Democratic and a third-party line).
  - An independent who caucuses with the Democrats (Sanders, King) stands as the Democrat, as in 538's rows.
- **Runoffs and the legislature.**
  - **Georgia** (a majority is required, else a runoff): not computed with three or more candidates.
  - **Louisiana**'s open primary: not computed.
  - **Ranked choice** in Maine (2018 on) and Alaska (2022 on): not computed.
  - **Vermont governor**, which the legislature chooses if no one has a majority: not computed with a third candidate on the ballot.

  The result is recorded in every case, and 538's forecast is kept where it has one.
- **Algara and Amlani's races (1978-2004).** The source names only the two nominees.
  - Where the others' total is at least the smaller nominee's, an unnamed candidate may have been in the top two, so p is not computed (8 races).
  - Where a nominee had no votes, who the top two were is not known (1 race).
  - Georgia and Vermont with any other votes are not computed, as above.
- **Missouri before 2006.** Algara and Amlani's Missouri rows fall short of Cha's totals by 7% for the Democrat and 2% for the Republican in each of 2008, 2012 and 2016.
  - That is what a missing Kansas City would do: it reports apart from Jackson County. This is inferred, since the rows hold 115 jurisdictions, the 114 counties and St. Louis City.
  - The count is taken as incomplete. Missouri's seven races of 1980-2004 have no p, no fit row and no last-race value.
  - So Missouri 2008, whose last race is 2004's, has no forecast of the model's own either.
- **Missing district input**: no 2020 presidential vote on the 2024 lines in Alabama, Louisiana and North Carolina; none for 2008 on California's 2012 lines; none for 2012 on Florida's 2016 lines.
- **Too few earlier cycles** (§2.3): the House of 2006 (368 contests) and the governors of 1978-1984 (89). 538's files hold neither, so p is not computed, with that reason.
  - Control of the House in 2006 is not computed either, since the chamber stage needs the model's common swing.
  - The chamber check (§4) is still made.
- **No last governor race.** Two races get no forecast of the model's own: Alaska 2006, since Alaska is not in Algara and Amlani, and Missouri 2008.
- **Specials held apart from November.** The November record leaves out specials held on other dates.
  - Cha, Kuriwaki and Snyder hold 42 such House contests and Massachusetts's Senate special of January 2010. They are added with Cha as their record (`certified` null, with no second source) and p not computed, since both forecasts are of November's general election.
  - Their dates are not in the sources read here, except Massachusetts's: 19 January 2010, from Senate.gov.
  - Eight of 2024's are among them (CA-20, CO-04, NJ-10, NY-03, NY-26, OH-06, TX-18, WI-08). The FEC has no 2024 volume, so they come from Cha, as the orchestrator agreed for want of the FEC.

## 4. Control of the chamber (exact form, MATH §4.2)

p(control) = p(seat) × P(the other seats leave control to this one | this seat tied).
- **Each seat** is y_i = μ_i + λ_i·d + e_i. Here d ~ N(0, s_a²) is the common swing (s_a here is the year's calibrated national sd), and e_i ~ N(0, s_e,i²) is the seat's own error. `stage_two.inputs` gives μ_i (`mean`), s_e,i (`own_sd`) and λ_i (`swing_loading`).
- **The common swing is conditioned on the tie**: d | tie ~ N(λ·s_a²·(½ − μ)/sd², s_a²·s_e,i²/sd²), with sd² = λ²s_a² + s_e,i².
- **The other seats' distribution** is computed exactly, by dynamic programming over seats on a grid of the swing. Where the swing given a tie is narrower than three grid steps, the other seats are counted afresh on a fine grid around it. No seat needed it.

**Whose forecast of the seat** (reading (c); *reason:* one forecast of the seat throughout its figure, M2 2.6):
- **The model's own**: its mean, s_e,i = the model's calibrated s_e, and λ = 1.
- **538's**, where 538's p stands first: 538's mean and implied sd are the seat's marginal, with s_e,i = √(sd₅₃₈² − s_a²) and λ = 1, as the presidency treats 538's marginals.
- **Where 538's sd is not above s_a**, no seat can carry the whole swing and keep 538's sd.
  - Such a seat carries λ = sd₅₃₈·√ρ ÷ s_a of the swing, with s_e,i = sd₅₃₈·√(1 − ρ) and ρ the model's own s_a² ÷ (s_a² + s_e²).
  - Its sd stays 538's, and its correlation with the swing is the model's.
  - These seats are marked in `marginal_note`.
- **Each forecast in `p.alongside`** has its own `control`, with P(decides | tie) conditioned on that forecast's mean and sd. The t4 figure uses the normal with the same mean and sd. The other seats are the same for all of them.

What decides control:
- **House:** 218 of 435.
- **Senate:** 51, or 50 with the Vice President, with the seats not up and the independents counted by caucus. A Senate special whose term ends when the new Senate meets (California 2022 and 2024; Illinois 2010, in Senate.gov's words) is not part of control.

**How each seat enters** (`stage_two.inputs.entered_as`):
- *model*: the model's own forecast, sharing the common swing.
- *inferred*: a structure whose p is not computed, entered as the model's two-way forecast.
  - This covers Georgia's runoffs, Louisiana, and ranked choice (King in Maine from 2018 among them).
  - Seats with no earlier presidential vote on their lines use the same day's presidential vote, stated as same-day.
- *fixed*: settled by who was on the ballot, known before the election.
  - Only Democrats on the ballot is fixed D.
  - No Democrat and no caucusing independent is fixed not-D: a same-party top two, a Republican against minor parties, and Osborn and McMullin, who said they would join neither caucus.
  - No seat is ever fixed at its result.

**Seats not up** (Senate): each is held by the winner of its latest election before the year, counted by caucus. Winners come from Cha, Kuriwaki and Snyder from 2006 on, runoffs included, and from MEDSL's Senate returns for seats last elected in 2002 and 2004. Each is listed in `chamber.seats_not_up_list`.

**The check on every chamber-year** (`chamber.check`): the seats not up plus the seats won, against the division the new Congress opened with (Senate.gov; House History). All 20 agree but two, and each of the two is a seat vacant at the opening. The House of 2006 is checked although its control is not computed.
- Minnesota's Senate seat in January 2009, contested; Franken (D) was seated in July. We count 59 against 56 + 2 independents + 1 vacant.
- New York's 22nd in January 2021, uncertified; Tenney (R) was seated in February. We count 213 R against 212.

**The Vice President.** In midterms it is the sitting one: Cheney (R) in 2006, Biden (D) in 2010 and 2014, Pence (R) in 2018, Harris (D) in 2022. In presidential years the VP is elected the same day, and P(the VP is a Democrat) is the presidential chance (§0.3, item 1). It comes from D1's record of the year, in `chamber.vice_president`, with `by`, `as_of` and `note`:

| Year | P(VP Democrat) | Whose |
|---|---|---|
| 2008 | 0.954 | the model's own, on 538's national average of 3 November |
| 2012 | 0.552 | the model's own, on 538's national average of 5 November |
| 2016 | 0.7137 | 538, polls-plus, 7 November; any other ticket counts as not Democratic |
| 2020 | 0.8932 | 538, polls-plus, 2 November |
| 2024 | 0.529 | the model's own, on the 12 September average (D1's horizon for 2024, M2 3.5) |

- **Whose chance.** It is 538's where 538's forecast stands first in D1's record of the year. Otherwise it is the model's own chance that the Democrat wins the College (`pipeline/own_forecast.py`, `college_prob` on the approved forecast): states are counted whole, and a 269 tie counts half.
- **Independence.** It is taken as independent of the Senate's common swing.
- **How far it moves control** is shown in each seat's `P_decides_given_tie_if_VP_D` and `_if_VP_R`.

## 5. Results

| Year, level | Contests | p computed | 538 first | near-tie calibrated | p = 0 | not computed | largest p | largest p for control |
|---|---|---|---|---|---|---|---|---|
| 1978 Governor | 35 | 0 | 0 | 0 | 0 | 35 |  |  |
| 1980 Governor | 13 | 0 | 0 | 0 | 0 | 13 |  |  |
| 1982 Governor | 35 | 0 | 0 | 0 | 0 | 35 |  |  |
| 1984 Governor | 13 | 0 | 0 | 0 | 0 | 13 |  |  |
| 1986 Governor | 35 | 33 | 0 | 0 | 0 | 2 | Wyoming, 1 in 80,892 |  |
| 1988 Governor | 12 | 10 | 0 | 0 | 0 | 2 | Delaware, 1 in 124,851 |  |
| 1990 Governor | 34 | 30 | 0 | 0 | 0 | 4 | Wyoming, 1 in 101,750 |  |
| 1992 Governor | 12 | 9 | 0 | 0 | 0 | 3 | Delaware, 1 in 114,679 |  |
| 1994 Governor | 35 | 31 | 0 | 0 | 0 | 4 | Wyoming, 1 in 86,111 |  |
| 1996 Governor | 11 | 9 | 0 | 0 | 0 | 2 | Delaware, 1 in 170,487 |  |
| 1998 Governor | 35 | 31 | 0 | 0 | 0 | 4 | Rhode Island, 1 in 171,812 |  |
| 2000 Governor | 11 | 9 | 0 | 0 | 0 | 2 | Delaware, 1 in 141,467 |  |
| 2002 Governor | 35 | 33 | 0 | 0 | 0 | 2 | Wyoming, 1 in 79,672 |  |
| 2004 Governor | 11 | 9 | 0 | 0 | 0 | 2 | Montana, 1 in 180,231 |  |
| 2006 Senate | 33 | 31 | 0 | 0 | 0 | 2 | North Dakota, 1 in 131,113 | Rhode Island, 1 in 7,285,814 |
| 2006 House | 438 | 0 | 0 | 0 | 30 | 408 |  |  |
| 2006 Governor | 36 | 33 | 0 | 0 | 0 | 3 | Wyoming, 1 in 104,980 |  |
| 2008 Senate | 35 | 31 | 0 | 0 | 0 | 4 | Wyoming special, 1 in 165,466 | South Dakota, 1 in 3,186,288 |
| 2008 House | 443 | 370 | 0 | 0 | 24 | 49 | New York 13, 1 in 59,057 | Texas 27, 1 in 6,628,625 |
| 2008 Governor | 11 | 9 | 0 | 0 | 0 | 2 | Delaware, 1 in 172,157 |  |
| 2010 Senate | 39 | 32 | 0 | 32 | 1 | 6 | North Dakota, 1 in 132,701 | Delaware special, 1 in 8,607,745 |
| 2010 House | 441 | 402 | 0 | 402 | 10 | 29 | West Virginia 3, 1 in 57,259 | New York 13, 1 in 3,003,249 |
| 2010 Governor | 36 | 32 | 0 | 0 | 0 | 4 | Wyoming, 1 in 82,327 |  |
| 2012 Senate | 33 | 33 | 0 | 33 | 0 | 0 | North Dakota, 1 in 139,835 | North Dakota, 1 in 1,626,635 |
| 2012 House | 441 | 344 | 0 | 344 | 10 | 87 | Texas 34, 1 in 61,244 | Arizona 1, 1 in 13,139,317 |
| 2012 Governor | 11 | 10 | 0 | 0 | 0 | 1 | North Dakota, 1 in 147,500 |  |
| 2014 Senate | 36 | 32 | 32 | 0 | 1 | 3 | Alaska, 1 in 29,076 | Alaska, 1 in 119,757 |
| 2014 House | 440 | 358 | 0 | 358 | 27 | 55 | California 31, 1 in 34,134 | California 21, 1 in 3,813,136 |
| 2014 Governor | 35 | 33 | 0 | 0 | 0 | 2 | Rhode Island, 1 in 105,001 |  |
| 2016 Senate | 34 | 30 | 26 | 4 | 0 | 4 | Nevada, 1 in 116,765 | Nevada, 1 in 556,042 |
| 2016 House | 439 | 344 | 0 | 344 | 22 | 73 | California 21, 1 in 40,323 | California 21, 1 in 4,132,339 |
| 2016 Governor | 12 | 11 | 0 | 0 | 0 | 1 | North Dakota, 1 in 163,506 |  |
| 2018 Senate | 35 | 32 | 30 | 2 | 0 | 3 | Montana, 1 in 95,378 | North Dakota, 1 in 596,519 |
| 2018 House | 442 | 383 | 273 | 110 | 15 | 44 | New Mexico 2, 1 in 33,196 | California 10, 1 in 2,006,113 |
| 2018 Governor | 36 | 34 | 34 | 0 | 0 | 2 | South Dakota, 1 in 59,094 |  |
| 2020 Senate | 35 | 30 | 28 | 2 | 0 | 5 | Alaska, 1 in 87,769 | Alaska, 1 in 707,427 |
| 2020 House | 440 | 398 | 288 | 110 | 10 | 32 | Oklahoma 5, 1 in 49,401 | California 21, 1 in 11,635,575 |
| 2020 Governor | 11 | 11 | 0 | 0 | 0 | 0 | Vermont, 1 in 164,734 |  |
| 2022 Senate | 36 | 32 | 31 | 1 | 0 | 4 | New Hampshire, 1 in 95,632 | Nevada, 1 in 453,746 |
| 2022 House | 444 | 390 | 292 | 98 | 15 | 39 | New Hampshire 1, 1 in 20,079 | New Hampshire 1, 1 in 1,006,152 |
| 2022 Governor | 36 | 33 | 30 | 0 | 0 | 3 | Nevada, 1 in 134,249 |  |
| 2024 Senate | 35 | 33 | 0 | 33 | 0 | 2 | Delaware, 1 in 177,824 | Delaware, 1 in 2,039,000 |
| 2024 House | 443 | 373 | 0 | 373 | 13 | 57 | California 22, 1 in 32,693 | California 22, 1 in 762,787 |
| 2024 Governor | 11 | 10 | 0 | 0 | 0 | 1 | Delaware, 1 in 207,174 |  |

**In all.**
- 5,324 contests.
- 4,098 with p computed, 1,064 of them under 538's forecast.
- 178 with p = 0.
- 1,048 not computed, each with its reason. 457 of them are for too few earlier cycles: the House of 2006 and the governors of 1978-1984.
- 2,246 of the p computed are calibrated to earlier years' near-ties (§2.6): the model's own for the House (2,139) and the Senate (107) of 2010-2024.

p is under the normal forecast. The t4 figure and the other forecasts' figures sit beside it in `p.alongside`, each with its own `control`.

**Sums of p, before and after the near-tie calibration (round 4).** Before is round 3, on `main` at c301d58 (#32). Each cell sums p over a level and year's contests; control likewise. "Calibrated" counts the contests whose p is. The governors are unchanged (9.8925e-04 in all).

| Year | House: p before | now | control before | now | calibrated | Senate: p before | now | control before | now | calibrated |
|---|---|---|---|---|---|---|---|---|---|---|
| 2006 | 0 | 0 | 0 | 0 | 0 | 5.1336e-05 | 5.1336e-05 | 1.1552e-06 | 1.1552e-06 | 0 |
| 2008 | 8.5538e-04 | 8.5538e-04 | 9.8365e-06 | 9.8365e-06 | 0 | 3.9762e-05 | 3.9762e-05 | 1.7761e-06 | 1.7761e-06 | 0 |
| 2010 | 1.4899e-03 | 1.3307e-03 | 2.5821e-05 | 2.3063e-05 | 402 | 4.4674e-05 | 3.9908e-05 | 6.6501e-07 | 5.9349e-07 | 32 |
| 2012 | 8.8720e-04 | 9.5199e-04 | 5.6291e-06 | 6.0463e-06 | 344 | 3.8608e-05 | 4.1446e-05 | 3.9862e-06 | 4.2798e-06 | 33 |
| 2014 | 1.0720e-03 | 1.2003e-03 | 6.4949e-06 | 7.2900e-06 | 358 | 8.5495e-05 | 8.5495e-05 | 1.7498e-05 | 1.7498e-05 | 0 |
| 2016 | 6.1260e-04 | 6.8323e-04 | 6.5180e-06 | 7.2812e-06 | 344 | 2.6886e-05 | 2.7120e-05 | 5.3246e-06 | 5.3709e-06 | 4 |
| 2018 | 1.6702e-03 | 1.6759e-03 | 2.5351e-05 | 2.5407e-05 | 110 | 5.1473e-05 | 5.1511e-05 | 4.8993e-06 | 4.9006e-06 | 2 |
| 2020 | 1.0717e-03 | 1.0768e-03 | 3.8916e-06 | 3.9121e-06 | 110 | 4.4368e-05 | 4.4457e-05 | 5.2345e-06 | 5.2429e-06 | 2 |
| 2022 | 1.7124e-03 | 1.7129e-03 | 3.2611e-05 | 3.2612e-05 | 98 | 3.6458e-05 | 3.6504e-05 | 5.1294e-06 | 5.1333e-06 | 1 |
| 2024 | 5.3186e-04 | 6.7123e-04 | 2.0931e-05 | 2.6393e-05 | 373 | 2.2199e-05 | 2.6842e-05 | 2.3260e-06 | 2.8121e-06 | 33 |
| **All** | 9.9032e-03 | 1.0158e-02 | 1.3708e-04 | 1.4184e-04 | 2139 | 4.4126e-04 | 4.4438e-04 | 4.7994e-05 | 4.8762e-05 | 107 |

**Sums of p, round 2 and round 3.** Round 2 is D2-v2, on `main` at b00c55e (#29); round 3 is before the near-tie calibration. The governors of 1978-2004 had no file in round 2.

| Year | House: round 2 | round 3 | control, round 2 | round 3 | Senate: round 2 | round 3 | control, round 2 | round 3 | Governor: round 2 | round 3 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1978-1984 |  |  |  |  |  |  |  |  | (no file) | 0 |
| 1986 |  |  |  |  |  |  |  |  | (no file) | 9.4230e-05 |
| 1988 |  |  |  |  |  |  |  |  | (no file) | 3.4647e-05 |
| 1990 |  |  |  |  |  |  |  |  | (no file) | 7.9517e-05 |
| 1992 |  |  |  |  |  |  |  |  | (no file) | 3.2597e-05 |
| 1994 |  |  |  |  |  |  |  |  | (no file) | 7.9194e-05 |
| 1996 |  |  |  |  |  |  |  |  | (no file) | 2.4488e-05 |
| 1998 |  |  |  |  |  |  |  |  | (no file) | 5.9534e-05 |
| 2000 |  |  |  |  |  |  |  |  | (no file) | 2.7069e-05 |
| 2002 |  |  |  |  |  |  |  |  | (no file) | 8.2682e-05 |
| 2004 |  |  |  |  |  |  |  |  | (no file) | 2.2970e-05 |
| 2006 | 0 | 0 | 0 | 0 | 5.1168e-05 | 5.1336e-05 | 1.0845e-06 | 1.1552e-06 | 0 | 7.1799e-05 |
| 2008 | 0 | 8.5538e-04 | 0 | 9.8365e-06 | 3.9609e-05 | 3.9762e-05 | 1.7509e-06 | 1.7761e-06 | 0 | 1.8754e-05 |
| 2010 | 0 | 1.4899e-03 | 0 | 2.5821e-05 | 4.4840e-05 | 4.4674e-05 | 6.4503e-07 | 6.6501e-07 | 0 | 7.3832e-05 |
| 2012 | 0 | 8.8720e-04 | 0 | 5.6291e-06 | 3.8629e-05 | 3.8608e-05 | 3.9831e-06 | 3.9862e-06 | 0 | 2.6378e-05 |
| 2014 | 1.0883e-03 | 1.0720e-03 | 6.8564e-06 | 6.4949e-06 | 8.5495e-05 | 8.5495e-05 | 1.7482e-05 | 1.7498e-05 | 0 | 5.2825e-05 |
| 2016 | 6.4762e-04 | 6.1260e-04 | 8.0010e-06 | 6.5180e-06 | 2.6970e-05 | 2.6886e-05 | 5.2616e-06 | 5.3246e-06 | 0 | 2.6920e-05 |
| 2018 | 1.6685e-03 | 1.6702e-03 | 2.4589e-05 | 2.5351e-05 | 5.1602e-05 | 5.1473e-05 | 4.8308e-06 | 4.8993e-06 | 8.9209e-05 | 8.9209e-05 |
| 2020 | 1.0702e-03 | 1.0717e-03 | 5.0971e-06 | 3.8916e-06 | 4.4422e-05 | 4.4368e-05 | 4.9942e-06 | 5.2345e-06 | 2.0575e-05 | 2.0400e-05 |
| 2022 | 1.7145e-03 | 1.7124e-03 | 3.1041e-05 | 3.2611e-05 | 3.6584e-05 | 3.6458e-05 | 6.5364e-06 | 5.1294e-06 | 5.3741e-05 | 5.4290e-05 |
| 2024 | 5.9743e-04 | 5.3186e-04 | 2.1313e-05 | 2.0931e-05 | 2.2805e-05 | 2.2199e-05 | 2.2460e-06 | 2.3260e-06 | 1.4931e-05 | 1.7919e-05 |
| **All** | 6.7866e-03 | 9.9032e-03 | 9.6897e-05 | 1.3708e-04 | 4.4212e-04 | 4.4126e-04 | 4.8815e-05 | 4.7994e-05 | 1.7846e-04 | 9.8925e-04 |
| contests with p | 2,246 | 3,362 |  |  | 316 | 316 |  |  | 88 | 420 |

- **Where p is regained.** The House of 2008-2012 (1,116 contests) and the governors of 2006-2016 (128). The governors of 1986-2004 are new (204 contests with p).
- **Where p moves.**
  - Calibration narrows every level's forecast after the first scored years. So the sums fall a little where most races are safe: the House of 2024 by 11%, of 2016 by 5%; the Senate of 2024 by 3%.
  - The governors of 2020-2024 move with the fit from 1978: 2024 is 20% higher.
  - 538's seats are unchanged, but their control moves with the model's calibrated common swing: Senate 2022 falls from 6.54 to 5.13 × 10⁻⁶.

### Historical check (MATH §8.2 iv)

Over all contests with p, the expected number decided by k votes or fewer is computed under the forecast each p used (with its near-tie calibration, where it has one), and set against the number seen (`chambers.py history`, `history.json`). k = 1 is the event itself. Larger k test the same forecasts where there are cases to count.

| Level | Contests | within 1 vote | within 10 | within 100 | within 1,000 | within 5,000 | within 10,000 | within 20,000 |
|---|---|---|---|---|---|---|---|---|
| House, 2008-2024 | 3,362 | 0.020 vs 0 | 0.20 vs 1 | 2.0 vs 1 | 20.3 vs 25 | 101.6 vs 108 | 202.3 vs 192 | 407.4 vs 422 |
| Senate, 2006-2024 | 316 | 0.001 vs 0 | 0.009 vs 0 | 0.09 vs 0 | 0.89 vs 1 | 4.4 vs 5 | 8.8 vs 8 | 17.4 vs 18 |
| Governor, 1986-2024 | 420 | 0.002 vs 0 | 0.02 vs 0 | 0.20 vs 0 | 1.98 vs 1 | 9.9 vs 5 | 19.7 vs 14 | 39.3 vs 39 |

- **House and Senate.** The forecasts pass at every k.
  - The one House race within ten votes is Iowa's 2nd of 2020, at 6 votes.
  - The Senate race within 1,000 is Minnesota 2008, at 312.
- **Governors.**
  - The race within 1,000 is Washington 2004, at 129 votes in Algara and Amlani's county sums.
  - Within 5,000 votes, 5 finished against 9.9 expected (a Poisson chance of 7% for 5 or fewer). Within 10,000, 14 against 19.7 (12%). Within 20,000, 39 against 39.3.
  - Measured by share, the governors are not short: in the back-test, 30 finished within 49-51% against 30.9 expected (§2.3).
  - So the shortfall is at fixed vote margins only, which weight the small states. On these counts it is not significant.

## 6. Two sources, differences listed (plan §3a)

**House and Senate.** Every contest in the record is checked against Cha, Kuriwaki and Snyder, and the differences are kept in `checks`. The source of record wins.
- **Most differences** are small candidates (under ten votes) and blank or write-in lines, which the check source leaves out by design.
- **Real ones**: 2022 IL-03 (Ramirez 177,759 at the FEC, 121,764 in the check), 2024 Missouri Senate (W. C. Young 35,671 at the Clerk, 21,111 in the check), and 2012 AL-03 (Harris 98,141 at the FEC, 91,141 in the check).
- **Fixed in the record's reading**:
  - A fusion candidate's lines filed under two FEC ids are one candidate's. Connecticut's Senate race of 2010 is the case: Blumenthal's Democratic and Working Families lines now sum to 636,040, as the check has. Each merge is noted in the contest.
  - FEC rows with no candidate are not contests: a "California" row in 2018, and two Ohio rows in 2006.

**Governors, Algara and Amlani against Cha, Kuriwaki and Snyder, 2006-2020.** This is the check `algara_amlani.py` writes into its cache, nominee by nominee, on the even and odd years both hold.
- **The count.** 203 elections, with 61 differences, of which 27 are over 0.1%. Two elections are in Algara and Amlani only: Rhode Island 2010 and New Jersey 2017.
- **The large ones:**

| Election | Party | Algara and Amlani | Cha | Difference | Reading |
|---|---|---|---|---|---|
| Missouri 2008, 2012, 2016 | D | 1,560,588; 1,386,582; 1,179,024 | 1,680,611; 1,494,056; 1,277,360 | −7% each | a missing jurisdiction, inferred; Missouri left out before 2006 (§3) |
| Missouri 2008, 2012, 2016 | R | | | −2% each | the same |
| New York 2018 | R; D | 2,207,602; 3,635,340 | 1,926,485; 3,424,416 | +15%; +6% | fusion: Algara and Amlani sum the nominee's lines, Cha counts the party's line |
| Connecticut 2018 | R; D | 650,138; 694,510 | 624,750; 676,649 | +4%; +3% | fusion, the same |
| West Virginia 2012 | D; R | 335,468; 303,291 | 297,207; 273,130 | +13%; +11% | Cha appears low, not settled here |
| Utah 2008 | D; R | 186,503; 734,049 | 175,301; 700,565 | +6%; +5% | Cha appears low, not settled here |
| Maine 2010 | D | 109,087 | 103,387 | +5.5% | not settled here |
| Hawaii 2018 | R | 131,719 | 137,719 | −4.4% | not settled here |
| Louisiana 2011 | D | 182,925 | 288,161 | −37% | the open primary: several Democrats ran, and the check sums Cha's Democrats |

- **The rest** are under 0.7%.
- **The governor files of 2006-2024 keep Cha as the record.** Where the two differ beyond fusion, a third source (MEDSL's precinct files, or the states' own canvasses) is needed to settle which is right (§7).

## 7. Not yet

- **The House of 2006.** It needs an earlier House cycle for stage one. The FEC's 2004 volume, with The Downballot's 2000 vote on the 2006-2010 lines, would give one, if a source states which states kept their lines from 2004 to 2006.
- **The means of the House's safer races.** The near-tie factor (§2.6) reaches the centre. But the counts at 48-52% and 45-55% stay short, and the House's results land about 1.5 points nearer ½ than its means in races 5 to 20 points from even. A forecast mean shrunk toward ½ (or a smaller b_lean), fitted on earlier years, is the next test; it would raise those races' p further. A spread that depends on the expected margin (`D2_HETERO`) is the other.
- **The Senate's national terms for every House year.** They score better over 2014-2024 too (§2.3). This is a finding only, not adopted.
- **Earlier still.**
  - Algara and Amlani also hold county returns for President (1872 on) and the Senate (1908 on). Their presidential returns would let governor contests reach before 1978. Their Senate returns would extend the Senate's fit, with incumbency from their seat status rather than inferred.
  - Their Missouri rows would need the missing jurisdiction found first.
- **A third source for the governor disputes** of §6: MEDSL's precinct files (2016, 2022 and 2024), or the states' canvasses.
- **Population before 2022.** The ACS table-based files on www2.census.gov begin with 2021. The older sequence-based summary files there hold the same table and are the next step. The Census API wants a key, which needs an email, so it is not used.
- **Odd-year governors** (Virginia, New Jersey, Kentucky, Louisiana, Mississippi), which are in Cha and in Algara and Amlani.
- **2026.** Not built: no standardized source holds its count yet (held 2026-11-03). Once one does, the files carry it marked as an unofficial count with its date, until it is certified.
