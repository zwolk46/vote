# The model of one vote's importance: draft 3

*Orchestrator, 2026-11-07. Replaces draft 2; drafts 1 and 2 are kept as the record. Fable tried to break draft 2 and found 45 breaks (`model/BREAKS-draft-2.md`). Each one is taken in here, and §11 says where. Figures are read at their source or, where the research reports mark it, at the nearest readable text (`research/*-v2.md`). Formulas are derived and checked by script in `model/MATH.md`; `model/math/run_all.sh` reproduces its output exactly, re-run by the orchestrator and by Fable. Section marks like (MATH §1.1) point there.*

*Zach's words so far. Importance is "the chance it decides the outcome", with the ballot counted or not and everything else the same (2026-11-06 19:32). The page leads with break-even stakes and shows both readings of B (2026-11-07 00:24). The site covers US races at every level (01:59). Everything else here is the orchestrator's reading. §9 lists the readings he may correct, and §10 the one question put to him.*

---

## 1. The question

You go to the polls and fill in a ballot. In one world it is counted. In the other it is quietly not counted, and nobody ever knows. Everyone else behaves the same in both worlds. **How likely is it that who wins differs between the two worlds?** That number is **p**, the importance of your vote in a race. It is also how much more likely your side is to win in the world where your ballot counts: the two questions have one answer (MATH §5.11). **And is p times what the outcome is worth more than what voting cost you?**

## 2. The standard of review

> **A vote in a race pays for itself when p × B > C, that is, when B > C ÷ p.**

- **p** is the chance that your counted ballot changes who wins.
- **B** is how much better the outcome you voted for is than the other one.
- **C** is what voting cost you.

What you called "the magnitude, given a probability of one" is B. The expected outcome with your ballot counted, minus the expected outcome without it, is p × B. Both are in the formula, one level apart.

The page leads with **B\* = C ÷ p, the break-even stakes**: how much the outcome would have to be worth for this vote to pay. B\* is the same test whichever welfare a reader counts in B. Beside it the page shows what B\* means **for you alone**, and **per person the outcome affects** (Zach's ruling, 00:24; §5).

**One trip, a whole ballot.** A US general-election ballot carries many races: the presidency, Congress, the state legislature, local offices and ballot measures. You pay for the trip once. So each race on the ballot pays for a share of the trip, **B ÷ B\***, and the trip pays when those shares add up to more than 100%. This is the same test, summed over the ballot: p₁B₁ + p₂B₂ + … > C. The model shows p and B\* race by race and the sum for the ballot. Which of the two carries the site's verdict is the question for Zach (§10).

**At the scale of a presidential race.** Take p = 1 in 10 million, Gelman, Silver & Edlin's figure for the best-placed states in 2008, and a cost of about $9 to $12 (§6). Then B\* is **about $89 million to $120 million**. For their average voter that year, at 1 in 60 million, it is **about $530 million to $720 million**. In the safest states, at about 1 in a billion, it is **about $9 billion to $12 billion** (B\* is C times the "1 in" figure; MATH §1.6).

**At the scale of a local race.** Take a town race of 2,000 voters, forecast at 52-48 with a 4-point spread. This is a stylised forecast, not a real race. Then p is 1 in 468 (MATH §6.2) and B\* is **about $4,150 to $5,630**. That is about twenty thousand times less than the presidency on the same ballot.

## 3. What p is

**Exactly.** Without your ballot, the count among everyone else is exactly tied, or leaves your side exactly one vote short, or is anything else. Only the first two can be changed by your ballot.
- If the others are tied, your ballot makes your side win. Without it, the state's tie rule decides.
- If your side is one short, your ballot makes a tie, which the tie rule decides. Without it, your side loses.

Under a fair lot, who wins differs in half of these cases, because the lot would have gone your way half the time anyway. So **p is half the chance that the count without you is tied or one short** (MATH §1.1). The full chance, that the count without you lands within one vote, is called **the event** here. It is twice p. The site names it whenever it shows it and never shows it as p (§9.2).

Under a tie rule other than a lot, such as a new election or a legislature deciding, p differs between an odd and an even number of voters. But **before the election it averages to the same value under every rule**, because no one can know turnout to the vote. So the site needs no tie rule to compute p.

**The value of a tie.** Suppose a tie is worth something to you other than its expected outcome, for instance because a new election has costs of its own. Then, for a known number of voters, your gain differs from p × B by as much as p × B itself. Before the election it averages to p × B exactly (MATH §5.1; Fable's check, `model/BREAKS-draft-2.md` #19).

**The one-line formula the model computes:**

> **p = f(½) ÷ (2n)**

Here n is the number of other voters. f(½) is the height of the forecast curve for your side's share at exactly 50-50. It is about 50 times the chance the forecast gives of a finish between 49% and 51% (MATH §6.1). Equivalently, **p is the density of the margin, in votes, at zero.**

**The form a person can say aloud** (MATH §6.1):

> **p ≈ 25 × q ÷ n**, where q is the chance the race finishes between 49% and 51%.

Why it works: a finish between 49% and 51% covers about 2% of the n possible margins. So each of them, the exact tie included, carries about q ÷ (0.02 × n) = 50 × q ÷ n of the chance. A tie gives your side half a win, so p ≈ 25 × q ÷ n.

How good it is: within a factor of **1.22** of the exact p for every race of 1,000 voters or more that was tested. For races of 10,000 voters or more with a forecast spread of 2 points or more, it is within **4%** (MATH §6.2). Below 1,000 voters the site computes the exact sum, which is cheap. A fixed "K ÷ n" rule like "10 ÷ n" is not used. It drops closeness, so it is off by up to **18 times** (MATH §6.1, S6.2).

**What drives p** (MATH §5):

| Driver | What happens to p | Condition |
|---|---|---|
| **Number of voters n** | falls as 1 ÷ n | once n × (forecast spread)² is above about 6, with the spread as a fraction (2.5 points is 0.025). Every race of more than about 10,000 voters meets this at a spread of 2.5 points or more; below that, the site uses the exact sum. Only in an artificial "known 50-50" race does p fall as 1 ÷ √n |
| **Expected closeness** | falls steeply as the forecast moves off 50-50 | with a normal forecast and a 2-point spread, a 56-44 race is about 1% as likely to tie as an even one, and a 60-40 race about 1 in 270,000 as likely. With heavier tails (a Student-t with 4 degrees of freedom, same spread) the fall is much slower: 1.4% and about 1 in 670. **For a safe race the choice of tails moves p by a factor of hundreds** (MATH §1.5, §5.7) |
| **Forecast uncertainty** | helps a lopsided race and hurts a close one | more uncertainty raises p when the forecast's lead over 50% is bigger than its standard deviation, and lowers it when smaller (MATH §5.8) |
| **Structure** | multiplies stages | presidency: (your state is tied) × (your state then decides the Electoral College); a seat, then control of the chamber |
| **Recounts and counting error** | leave p unchanged | when the zone a recount can swing (hundreds to a few thousand votes) is much narrower than the forecast's spread in votes (tens of thousands in a statewide race). Your ballot shifts the *chance* your side is declared the winner by the same p. At a zone a third the size of the spread, p is still 96% of its value (MATH §5.10). Minnesota's 2008 recount changed 2,170 votes gross, against a forecast spread of about 48,000 to 73,000 votes. In a small local race the two can be closer; the model checks this there when it has the data (§10) |

**Two stages** (MATH §4.1). For the presidency, p = (chance your state is tied) × (chance your state's electoral votes then decide the College, *given* that tie). The usual shortcut drops "given that tie". The shortcut is within 12 to 23% for states whose forecast share is within 2 points of 50% (a 52-48 margin or closer). It is off by up to 1.5 times for states 2 to 3 points off, and up to 16 times further out, where p is 10 to 1,000 times smaller. The model computes the exact form, which takes seconds. A seat and control of a chamber work the same way, but there the shortcut fails badly for a leaning seat, so the model must use the exact form (MATH §4.2).

**Which forecast.** p is always the chance under a named forecast.
- Where a forecaster published its own, the site uses it, with its own tails.
- Where two forecasters published, the page shows both.
- Where none published, which is almost every race below the presidency, the model builds a forecast from what was known before the election. It fits a distribution to the margins of like past races, as Gelman, King & Boscardin (by regression, from variables known before the election such as the polls two months out) and Mulligan & Hunter (from the spread of past margins) did (R1 §3.1 E, §3.3). This forecast is the model's own, and the page marks it so.

That last route is how past races become inputs, not only the check (§9.3).

## 4. What p is in real elections

**Published estimates**, as read at source (`research/decisiveness-models-v2.md` §3.3). The papers differ in convention by a factor of 2 (MATH §2), and each is marked:
- **2008 presidential** (Gelman, Silver & Edlin 2012): **about 1 in 10 million** in New Mexico, Virginia, New Hampshire and Colorado; **1 in 60 million** for the average voter; **about 1 in a billion** in New York, California and Texas. Their words put these in our convention. If they meant an exact tie, p is half and B\* double (MATH §3.4).
- **2020 presidential** (The Economist's published forecast page, 3 November 2020): Pennsylvania **1 in 9 million**, Wisconsin 1 in 15 million, Florida 1 in 37 million, Texas 1 in 104 million, New York 1 in 6 billion, California **1 in 16 billion**. Its method is not stated on the page or in its public code, so its convention is unknown. The page's figures are its copyright and not covered by its data licence (R1 S2), so whether the site may show them is not settled; asking The Economist would be Zach's call.
- **1992 presidential** (Gelman, King & Boscardin 1998): "about 1 in 10 million for all states". They count a tie as a full decision where we count it as half, so this is about 1 in 20 million as p.
- Figures like California's fall far below one in the number of voters because a lopsided state almost never ties: the height of the forecast curve at 50-50 is then tiny (§3).
- **Below the presidency**, no published estimate of p for a real race was found: none for a primary, a chamber, a small local election, a runoff or a supermajority ballot measure (R4). The model computes these itself (§3, "Which forecast").

**The historical record, as a check** (`research/historical-close-races-v2.md`; MATH §8):
- **US House, 1898 to 1992:** one race in 16,577 was decided by one vote on the official count: New York's 36th district, 1910. A later count made it six votes (20,690 to 20,684), and Mulligan & Hunter's own later-count check halves their frequency. Read as an average, the official count implies a p of about **1 in 180,000** per House ballot. That is an upper figure, and with a single event its margin of error is wide: the record is consistent with anything from about 1 in 32,000 to 1 in 7 million (MATH §8.3). At that upper figure, B\* for a House vote is about $1.6 million to $2.1 million.
- **US House, 1820 to 1910:** eight races had a one-vote margin at some stage of their count (R2 §2a).
- **State legislatures, 1968 to 2022** (Klarner's data): 52 of 109,093 contests ended tied or one vote apart.
- **No statewide election, and no federal election since 1910**, in the record read was decided by one vote. Since 2000 the closest presidential states were New Mexico 2000 (**366** votes) and Florida 2000 (**537**). In 2024 the closest was New Hampshire by votes (22,965) and Wisconsin by share (0.9%).
- **At one vote, the count doesn't decide.** Recounts, courts and tie rules do. Minnesota's 2008 Senate recount changed 2,170 votes gross (264 net) among 2.4 million cast for the two leaders. Virginia's 94th House district in 2017 was settled by drawing lots. This doesn't change p (§3), but the page says it.

## 5. What B is

B is the difference between the two outcomes, as valued. Following Zach's ruling, the page doesn't choose whose welfare counts. It shows B\* and reads it two ways:
- **For you alone:** compare B\* with what the outcome is worth to you personally. In a large race, B\* runs from tens of millions of dollars in the closest states to hundreds of billions in the safest: on The Economist's 1 in 16 billion for California in 2020, about $140 billion to $190 billion.
- **Per person affected:** divide B\* by the number of people the outcome affects, which is the population of the country, state, district or town. The source is the Census Bureau, to be read at source in the data stage. For illustration: at a B\* of $120 million in a state of 10 million people, the outcome would have to be worth $12 to each of them. This is the reading under which Edlin, Gelman & Kaplan (2007) argue a vote can pay. Their example is a close election with round hypothetical inputs ($10 per person, a third of people voting, others' welfare counted at a tenth of its weight). In it, voting is worthwhile at any cost under $25. For the voter alone, the same paper gets under 10 cents at a million voters (`research/frameworks-benefit-cost-v2.md` §5).

## 6. What C is

**In person: the trip** (`research/frameworks-benefit-cost-v2.md` §4).
- **Time at the polling place:** a mean of **19 minutes** and a median of 14, with 18% over 30 minutes. This is time spent within 60 metres of the polling place, which the authors read as waiting plus voting. By the radius chosen, the mean runs from 12 to 23 minutes. The source is smartphone location data on 154,489 likely voters in 2016 (Chen, Haggag, Pope & Rohla).
- **Time in line:** **13.3 minutes** on average in 2012 (Stewart, from the Cooperative Congressional Election Study). In 2020, 14% of Election Day voters and 22% of early in-person voters waited more than 30 minutes (MIT's Survey of the Performance of American Elections).
- **The value of an hour:** **$38.00**, average hourly earnings of private employees, October 2026, preliminary (Bureau of Labor Statistics, series CES0500000003, via its public data service). Valuing all your time at the average wage is a convention, the one Gibson et al. use. Other conventions value time off work lower, and the reader can set their own price.
- **Travel:** a mean of about 5 minutes by car to the nearest polling place, in New Zealand in 2005 (Gibson et al.). No US figure was found.
- **Becoming informed and registering:** no measured figure exists in what was read.

So **14 to 19 minutes at the polls is about $9 to $12 at the average wage, before travel** ($8.87 to $12.03). The model treats C as the reader's own number. It shows a default built from these figures, with the source of each, and doesn't pretend to know any one person's cost.

**By mail.** A mail ballot has no trip and no line; the wait figures above exclude mail voters. Its cost is the minutes to fill it in and send it back. No measured figure for those minutes was found, and the share of voters who vote by mail is to be read at source in the data stage. This may be the case Zach's claim already sets aside ("unless the cost is basically negligible"), so the site shows it as its own cost case.

**Where C enters.** In the thought experiment you go to the polls in both worlds, so C cancels there. The site's test is for the trip, or the mail ballot: what your counted ballot is expected to gain, against what getting it counted costs.

## 7. US races at every level (MATH §4, §7)

- **President:** two stages, your state and then the Electoral College (§3). States that award electoral votes by district are a further stage; which states do so is to be read at source.
- **Senate, governor and other statewide races:** one race, decided by its own count. Control of the Senate is a second stage, in the exact form (MATH §4.2).
- **House and state legislature:** one seat, decided by its own count. Control of the chamber is a second stage, in the exact form, which matters more here than in the College: a tie in a leaning seat implies a swing worth tens of seats.
- **Local races:** small electorates, computed exactly. With 9 other voters split by a coin, p is 12.3% (MATH §7). Races that fill several seats at once ("vote for three") are decided at the boundary between the last winner and the first loser. That case is the model's own and not yet checked.
- **Primaries:** a race with its own electorate, often small and often with several candidates. With three or more candidates under plurality, your ballot can decide only between the top two, at about a two-way race's size; a vote for a candidate far behind is worth about zero (MATH §7, checked and sound). No published estimate for a real primary was found (R4), so the model computes its own.
- **Ballot measures with a threshold t** (50%, or a supermajority where the law sets one): a Yes ballot decides with chance about (1 − t) × f(t) ÷ n, and a No ballot about t × f(t) ÷ n, averaged over turnout. At a two-thirds threshold a No is twice as likely to decide as a Yes (MATH §7, S7.5).
- **Runoffs and ranked-choice voting**, used in some US states and cities: the structure is understood (a sum over pairs, or over orders of elimination, of two-way p's with conditional forecasts). No calculation checked is good enough to show as a number yet; the model would compute them by enumeration or simulation, as its own.
- **Other countries' systems** (proportional representation and the rest) are out of scope by Zach's ruling of 01:59, and are dropped from the model.

## 8. Two modes for the site

**Simple mode.** One race, three facts: how many vote, how close it is expected to be, and how sure the forecast is. Out come two numbers:
- **"The chance your ballot changes who wins."** This is p, with the sentence behind it: about 25 × (chance it finishes between 49 and 51%) ÷ voters.
- **"What the outcome would have to be worth for your vote to pay."** This is B\*, with its two readings.

Simple mode is for a race its own count decides. For a presidential state it adds a second step, the chance your state then decides the College, taken from full mode and shown as its own line. For Florida in the 2016 back-test, the state tie is 1 in 960,000, and with the College step it is 1 in 2.9 million (MATH §4.1, §6.2).

**Full mode.** Real races at every level, state by state and stage by stage, from published forecasts where they exist and the model's own where they don't, with certified results. Each input carries its source, the exact computation sits behind every number, and the whole ballot is added up. The historical record of near-ties sits alongside as the check.

## 9. Choices the orchestrator made, open to Zach's correction

These follow from Zach's setup. He can overrule any of them.
1. **The comparison is counted against not counted.** The swing of "your vote against a vote for the other side" is twice as large. It is named wherever it appears and never shown as p.
2. **A tie counts as half a decision.** Under a lot, a counted ballot that breaks or makes a tie changes who wins half the time. So p is the chance who wins differs between the two worlds, which matches your "the vote itself flips". The event, that the count without you lands within one vote, is twice p. Gelman, King & Boscardin (1998), who state your experiment in your terms, count the event. This choice halves or doubles every number shown, and the page always says which of the two it shows.
3. **p is ex ante:** the chance before the election, under a forecast built from what was known then. Where no forecast was published, the model builds its own (§3). The historical record is the check, and through those forecasts its races are inputs too.
4. **The evidential view doesn't arise.** This is the idea that your choice is evidence of how like-minded people vote. In your experiment your choice is the same in both worlds, so there is nothing for it to be evidence of. At the real choice of whether to go, everyone else is held fixed, as you said ("As many people as you would have convinced to go voting with you, you do in either case"), which excludes it too.
5. **Forecast tails.** Where a forecaster publishes its own p or distribution, the site uses it. Otherwise the model uses a normal distribution, with a Student-t with 4 degrees of freedom, matched on the same spread, alongside. For safe races the two differ by a factor of hundreds (§3).
6. **The cost default** values your time at the average private wage (§6), and the reader sets their own.

## 10. What is not yet settled

- **For Zach: race or ballot.** Should the site judge one race against the whole cost of the trip, or the whole ballot, or show both (§2)?
- **Forecasts for past years.** 538's archived pages need web.archive.org, which this environment's network refuses. The Economist's repository holds back-tests of its 2020 model on 2008, 2012 and 2016, which no voter saw. For those years, no forecast a voter could have seen has been read.
- **For the data stage, after the law:**
  - certified results at every level;
  - populations (Census Bureau) and the share voting by mail;
  - the tie and recount laws of the states not yet read. Eight states' laws, read at source, prescribe a lot (Alaska, Florida, Iowa, Kentucky, Michigan, Minnesota, Virginia, Washington), and three a new or special election (Indiana, Massachusetts, Texas);
  - the size of the recount zone in small races (§3).
- **Unread at source:**
  - the 1975 to 1981 classics (paywalled). The 1/n and 1/√n results attributed to them are derived afresh in MATH §1.2 and §1.4;
  - Mulligan & Hunter's published text (the working paper was read);
  - Gelman, Silver & Edlin's code;
  - Dave Leip's Atlas, Ballotpedia and NCSL (bot checks).

## 11. Where each of Fable's breaks went

| Break | Where | Break | Where |
|---|---|---|---|
| #1 the half at a tie | §3, §9.2 | #24 recount zone | §3 table |
| #2 his B | §2 | #25 two-stage wording | §3 |
| #3 ex ante for past races | §3 "Which forecast", §9.3 | #26 lay form within 4% | §3 |
| #4 evidential view | §9.4 | #27 18 times | §3 |
| #5 the wage convention | §6, §9.6 | #28 B\* range | §2, §5 |
| #6 one-vote sentences | §4 | #29 t matched on spread | §9.5 |
| #7 NY-36 1910 | §4 | #30 the label | §8 |
| #8 the $4 cost | §2, §6 | #31 f(½) in words | §3 |
| #9 GSE convention | §4 | #32 why 25 q ÷ n | §3 |
| #10 Economist back-tests | §10 | #33 one question | §1 |
| #11 Economist licence | §4 | #34 tie-value caveat moved | §3 |
| #12 "since 2000" | §4 | #35 GKB's full decision | §4 |
| #13 closest by share | §4 | #36 per-person example | §5 |
| #14 Minnesota net 264 | §4 | #37 what the site tests | §6 |
| #15 classics | §10 | #38 anchor for closeness | §3 table |
| #16 header claims | header | #39 list PR | dropped (scope ruling) |
| #17 EGK's example | §5 | #40 below one in n | §4 |
| #18 Chen and CCES | §6 | #41 one trip, many races | §2, §10 |
| #19 the value of a tie | §3 | #42 voting by mail | §6 |
| #20 ballot measures | §7 | #43 per-person divisor | §5, §10 |
| #21 simple mode, president | §8 | #44 which forecaster | §3 |
| #22 1 ÷ n condition | §3 table | #45 primaries | §7 |
| #23 lead vs margin | §3 table | | |

The arithmetic added in this draft, beyond MATH: B\* = C × (the "1 in" figure), at C = $8.87 (14 minutes) and $12.03 (19 minutes) at $38.00 an hour. The Poisson range for the House record is half MATH §8.3's range for the event (1 in 16,019 to 1 in 3,525,271).
