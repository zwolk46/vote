# The model of one vote's importance: draft 2

*Orchestrator, 2026-11-07. Replaces draft 1 (`model/MODEL-DRAFT.md`, kept as the record). Every figure here has now been read at its source: `research/*-v2.md`, about 200 corrections to the first pass. Every formula has been derived and checked by script: `model/MATH.md`, whose 338 numbers `model/math/run_all.sh` reproduces. The orchestrator re-ran it and got the same output. Section marks like (MATH §1.1) point there.*

*Settled by Zach so far: importance is the chance one counted ballot changes the winner, with everything else fixed (2026-11-06 19:32). The page leads with break-even stakes and shows both readings of B (2026-11-07 00:24).*

---

## 1. The question

You go to the polls and fill in a ballot. In one world it is counted. In the other it is quietly not counted, and nobody ever knows. Everyone else's behaviour is the same in both. **How much more likely is your side to win in the world where your ballot counts?** That number is **p**, the importance of a vote. **And is p times what the outcome is worth more than what voting cost you?**

## 2. The standard of review

> **A vote pays for itself when p × B > C, that is, when B > C ÷ p.**

- **p** is the rise in your side's chance of winning when your ballot is counted rather than not.
- **B** is how much better the outcome you voted for is than the other one.
- **C** is what voting cost you.

The page leads with **B\* = C ÷ p, the break-even stakes**: how much the outcome would have to be worth for this vote to pay. B\* is the same test whichever welfare a reader counts in B. Beside it the page shows what B\* means **for you alone**, and **per person the outcome affects** (Zach's ruling, 00:24).

Your phrase "the marginal difference between the outcome voted for and the expected outcome" is p × B exactly. One caveat: when a tie is settled by something other than a fair lot, a small term for the value of the tie itself enters. It averages out before an election, because no one can know whether turnout will be odd or even (MATH §5.1).

**At the scale of a presidential race.** Take p = 1 in 10 million, Gelman, Silver & Edlin's figure for the best-placed states in 2008, and a cost of $4 to $12. Then B\* is **$40 million to $120 million**. Take p = 1 in 60 million, their average voter that year, and a cost of $4: B\* is **$240 million** (MATH §1.6).

## 3. What p is

**Exactly.** p is the chance that, without your ballot, your side would be exactly tied or exactly one vote short, weighted by the tie rule (MATH §1.1). Under a fair lot, which many states use for legislative ties, p is half that chance. Under any other tie rule (a new election, or a legislature deciding), p differs between an odd and an even number of voters. But **before the election it averages to the same value under every rule**, because turnout can't be known to the vote. So the site needs no tie rule to compute p.

**The one-line formula the model computes:**

> **p = f(½) ÷ (2n)**

Here n is the number of other voters, and f(½) is how densely the forecast of your side's share is packed at exactly 50% (MATH §1.2). Equivalently, **p is the density of the margin, in votes, at zero.**

**The form a person can say aloud** (MATH §6.1):

> **p ≈ 25 × q ÷ n**, where q is the chance the race finishes between 49% and 51%.

Why it works: a finish between 49% and 51% spans about 2% of n possible margins. The tie is one of them, and half of it goes to the coin. This lay form is within a factor of **1.22** of the exact p for every race of 1,000 voters or more that was tested. For races of 10,000 or more with ordinary forecast uncertainty, it is within **3%** (MATH §6.2). Below 1,000 voters the site computes the exact sum, which is cheap. A fixed "K ÷ n" rule like "10 ÷ n" is not used: it is off by up to 15 times, because it drops closeness (MATH §6.1).

**What drives p**, with the conditions now proved (MATH §5):

| Driver | What happens to p | Condition |
|---|---|---|
| **Number of voters n** | falls as 1 ÷ n | once the forecast's spread in votes is several times the counting noise (n × spread² > about 6), which every real election meets. Only in an artificial "known 50-50" race does it fall as 1 ÷ √n |
| **Expected closeness** | falls steeply as the forecast moves off 50-50 | faster than exponentially for a normal forecast. With heavier tails, which some forecasters use, much more slowly: at 3 standard deviations off, 1.4 to 5% of the even-race value against 1.1% |
| **Forecast uncertainty** | helps a lopsided race and hurts a close one | precisely, more uncertainty raises p when the expected margin is larger than the uncertainty, and lowers it when smaller |
| **Structure** | multiplies stages | presidency: (your state is tied) × (your state then decides the Electoral College) |
| **Recounts and counting error** | leave p unchanged | when the zone a recount can swing (tens to hundreds of votes) is much narrower than the forecast's spread (tens of thousands), true of every real statewide race. Your ballot shifts the *chance* your side is declared the winner by the same p (MATH §5.10) |

**Two stages** (MATH §4.1). For the presidency, p = (chance your state is tied) × (chance your state's electoral votes then decide the College, *given* that tie). The usual shortcut drops "given that tie". It is within 12 to 23% for states within 2 points of even, and wrong by large factors only in lopsided states, where p is negligible anyway. The model computes the exact form. It takes seconds. A seat and control of a chamber work the same way, but there the shortcut fails badly for a leaning seat, so the model must use the exact form (MATH §4.2).

## 4. What p is in real elections

As published, read at source (`research/decisiveness-models-v2.md` §3.3). The papers differ in convention by a factor of 2 (MATH §2), and each is marked:

- **2008 presidential** (Gelman, Silver & Edlin 2012, our convention): **about 1 in 10 million** in New Mexico, Virginia, New Hampshire and Colorado; **1 in 60 million** for the average voter; **about 1 in a billion** in New York, California and Texas.
- **2020 presidential** (The Economist's published forecast page, 3 November 2020; its method isn't published, so its convention is unknown): Pennsylvania **1 in 9 million**, Wisconsin 1 in 15 million, Florida 1 in 37 million, Texas 1 in 104 million, New York 1 in 6 billion, California **1 in 16 billion**.
- **1992 presidential** (Gelman, King & Boscardin 1998, which prints the tie-or-one-short chance, twice our p): "about 1 in 10 million for all states", so about 1 in 20 million as p.

**The historical record, as a reality check** (`research/historical-close-races-v2.md`; MATH §8):
- **US House 1898 to 1992:** one race in 16,577 was decided by one vote (New York's 36th district, 1910). Read as an average, that implies a p of about **1 in 180,000** per House ballot, with a wide margin of error because it rests on a single event.
- **State legislatures 1968 to 2022** (Klarner's data): 52 of 109,093 contests ended tied or one apart.
- **No statewide or federal general election** in the record read was decided by one vote. The closest presidential states were New Mexico 2000 (**366**) and Florida 2000 (**537**). In 2024 the closest was New Hampshire, at 22,965.
- **At one vote, the count doesn't decide.** Recounts, courts and tie rules do. Minnesota's 2008 Senate recount changed 2,170 votes among 2.4 million, and Virginia's 94th House district in 2017 was settled by drawing lots. This doesn't change p (see the table in §3), but the page should say it.

## 5. What B is

B is the difference between the two outcomes, as you value it. Following Zach's ruling, the page doesn't choose whose welfare counts. It shows B\* and reads it two ways:
- **For you alone:** compare B\* with what the outcome is worth to you personally. In a large race, B\* runs to tens or hundreds of millions of dollars.
- **Per person affected:** divide B\* by the number of people the outcome affects. This is the reading under which Edlin, Gelman & Kaplan (2007) argue a vote can pay. In their example, with a $10-per-person stake counted at a tenth of its weight, voting is worthwhile for any cost under $25 (`research/frameworks-benefit-cost-v2.md` §5).

## 6. What C is

The cost of a trip to vote, as measured (`research/frameworks-benefit-cost-v2.md` §4):
- **Time at the polling place, waiting plus voting:** mean **19 minutes**, median 14, with 18% over 30 minutes. This comes from smartphone location data, 154,489 voters, 2016 (Chen, Haggag, Pope & Rohla).
- **Time in line:** **13.3 minutes** on average in 2012 (Stewart). In 2020, 14% of Election Day and 22% of early in-person voters waited more than 30 minutes (MIT's Survey of the Performance of American Elections).
- **Value of an hour:** **$38.00**, average hourly earnings, private employees, October 2026, preliminary (Bureau of Labor Statistics, via its public data service).
- **Travel:** a mean travel time of about 5 minutes by car to the nearest polling place in New Zealand in 2005 (Gibson et al.). No US figure was found.
- **Becoming informed** and **registering:** no measured figure exists in what was read.

So **19 minutes at the polls is about $12 at average earnings, before travel**. The model treats C as the reader's own number. It shows a default built from these figures, with the source of each, and doesn't pretend to know any one person's cost. In the thought experiment you go to the polls in both worlds, so C cancels there. It enters at the real choice of whether to go.

## 7. Beyond a US two-way race (MATH §7)

The checked results:
- **Three or more candidates (plurality):** decisive only between the top two, at about a two-way race's size. A vote for a candidate far behind is worth about zero. This is sound to use.
- **List proportional representation:** a vote is more likely to move a seat, about seats ÷ voters when the forecast spans at least half a seat. But a seat is one of many. Sound to use.
- **Referendums with a threshold t** (50%, or a supermajority): the two-way formula with t in place of ½. Sound to use.
- **Tiny electorates:** computed exactly. Sound to use.
- **Runoffs, ranked choice, STV and turnout quorums:** the structure is understood, but no calculation checked is good enough to show as a number yet.

## 8. Two modes for the site

**Simple mode.** One election, three facts: how many vote, how close it is expected to be, and how sure the forecast is. Out come two numbers:
- **"The chance it comes down to you."** Shown as p, with the sentence behind it: about 25 × (chance it finishes between 49 and 51%) ÷ voters.
- **"What the outcome would have to be worth for your vote to pay."** Shown as B\*, with its two readings.

**Full mode.** Real elections, state by state and stage by stage, from published forecasts and certified results. Each input carries its source, the exact computation sits behind every number, and the historical record of near-ties sits alongside as the check.

## 9. Choices the orchestrator made, open to Zach's correction

These follow from Zach's setup. He can overrule any of them.
1. **The comparison is counted against not counted.** The "your vote against a vote for the other side" swing is twice as large. It is named wherever it appears and never shown as p.
2. **p is ex ante:** the chance before the election, from a forecast a voter could have seen. The historical record is the check, not the measure.
3. **"Everything else fixed" also rules out the evidential view**, the idea that your choice is evidence of how like-minded people vote. This was put to Zach on 2026-11-06 without reply.
4. **Forecast tails:** where a forecaster publishes its own p, the site shows theirs with its convention marked. Where the model computes p, it uses the forecaster's own distribution if published, and otherwise a normal distribution with the heavier-tailed result alongside (MATH §1.5).

## 10. What is not yet settled

- **Which elections the site covers** (a question for Zach).
- **Forecast archives for past years.** 538's archived pages need web.archive.org, which this environment's network refuses. The Economist's open model data covers 2008, 2012, 2016 and 2020.
- **Unread at source:** the 1975 to 1981 classics (paywalled; their results are rederived in MATH); Dave Leip's Atlas, Ballotpedia and NCSL (bot checks); the recount and tie statutes of 34 states.
