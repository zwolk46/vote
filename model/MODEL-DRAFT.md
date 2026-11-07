# The model of one vote's importance: draft 1

*Orchestrator, 2026-11-06. A draft framework for Zach to react to. The structure doesn't depend on the figures, but **no figure here is verified yet**: the first research pass could read its sources only through short extracts, because this session's network refuses them. Every number is marked **(unverified)** until the second pass re-reads it at source. Sources and full notes are in `research/`.*

---

## 1. The question

You go to the polls and fill in a ballot. In one world it is counted. In the other it is quietly not counted, and nobody ever knows. Everything else is identical in both: who else votes, whom you persuaded, what anyone thinks of you. **How much better off is the world where your ballot counted, and is that worth what it cost you to vote?**

That is your setup (brainstorm, 19:32). It has a precise name in the literature. It is the **pivotal**, or counterfactual, test, and every source agrees it fits your setup exactly (`research/frameworks-benefit-cost.md` §3.1).

## 2. The standard of review

The only way your counted ballot changes anything is by changing **who wins**. So:

> **Expected benefit of your ballot = p × B**
>
> **The vote pays for itself when p × B > C**, or equivalently when **B > C ÷ p**.

- **p** is the chance that your ballot changes the winner.
- **B** is how much better the outcome you voted for is than the one you'd otherwise get.
- **C** is what it cost you to vote.

Your phrase "the marginal difference between the outcome voted for and the expected outcome" is exactly **p × B**. The expected outcome when you vote, minus the expected outcome when you don't, equals p times B, and nothing else. B on its own is the gain *if* your ballot is the deciding one. So both of your intuitions are in the formula, one level apart.

**The standard of review that needs no number for B** is the last form, **B > C ÷ p**. For any election we can compute the *break-even stakes*: how much the outcome would have to be worth for the vote to pay. That answers your "in which cases would it be greater, in which less" without our choosing B for anyone. A reader holds their own sense of the stakes against a figure like "$100 million". That is the comparison your claim rests on, made visible.

Illustration only, with **unverified** inputs. Suppose p is 1 in 10 million, the published estimate for the best-placed US states in 2008 (Gelman, Silver & Edlin, *Economic Inquiry* 2012, quoted from their abstract). Suppose C is about $4 to $12, roughly 6 to 19 minutes at average US hourly earnings. Then B would have to exceed about **$40 to $120 million** for the vote to pay. For the average 2008 voter (p about 1 in 60 million, same source), it's about $230 to $720 million.

## 3. What p is, and what drives it

**Exactly:** with a fair coin breaking ties, p = ½ × [chance the other voters are exactly tied + chance your side is exactly one short]. Either way, your ballot moves the result half a win. The ½ appears in Gelman, King & Boscardin (1998) and Barnett (2020) (unverified).

**Approximately:** p ≈ (how likely the race is to land at dead even) ÷ (number of voters), up to a small constant. That splits p into the things that drive it:

| Driver | Effect on p | Why |
|---|---|---|
| **Number of voters** | p falls roughly as 1 ÷ N | the same uncertainty is spread over more possible margins |
| **Expected closeness** | p falls steeply, faster than exponentially, as the forecast moves away from 50-50 | a landslide almost never lands on a tie |
| **Forecast uncertainty** | it cuts both ways: more uncertainty helps a lopsided race and hurts a dead-even one | uncertainty spreads the chance over more margins, including the tie |
| **Structure** | multiplies stages | in a presidential race p = (chance your state is tied) × (chance your state then decides the Electoral College); the same holds for a seat and control of a chamber |
| **Electoral system** | changes what "the winner" is | §6 |

This one line, p ≈ closeness ÷ voters, is the heart of the simple mode (§8).

**Where p comes from for a real election.** There are two routes, and they answer different questions.

1. **Before the election (ex ante):** from the forecast a voter could have seen, meaning each state's expected share and its uncertainty. This is what a person deciding whether to vote actually faces. The published estimates use it, and the Economist's open model publishes these inputs for 2008, 2012 and 2016 (unverified reading of its columns).
2. **After the fact (historical frequency):** how often races of a given size actually came down to one vote. Mulligan & Hunter (2003) found **1 US House race decided by one vote in 16,577** (1898 to 1992), and 2 ties plus 7 one-vote races in 40,036 state legislative races (unverified).

**I recommend the first as the measure and the second as the reality check.** The cost-benefit decision is made before the election, with what can be known then. The historical record shows the model isn't fanciful: no statewide or federal general election in the record read so far was decided by one vote, while small local races occasionally are.

## 4. What B is: the one fork your conclusion turns on

The sources agree that B is a **difference between two outcomes, as valued by the voter**. They split on **whose welfare goes into that value**:

- **Only your own.** In a large election p × B is tiny next to C, so your claim holds almost everywhere except very small or very close races.
- **Yours plus everyone else's** (Edlin, Gelman & Kaplan 2007; Barnett 2020). If B counts the benefit to everyone the outcome affects, B grows with the population about as fast as p shrinks, and the product stops vanishing. In their worked example, voting pays at ordinary costs (figures unverified). This is the strongest published answer to your claim, and it keeps your setup intact. It changes nothing about p or the counterfactual, only what B counts.

Your claim stands or falls on this choice, so it's the one question I'm putting to you (§10). The break-even form keeps it open. B > C ÷ p is the same test whichever welfare a reader counts. The site can show the break-even figure both as "to you" and as "per person affected".

## 5. What C is

The pieces the literature counts: **time waiting, time travelling, time at the booth, travel money, registration, and becoming informed.** Measured figures (all unverified):

- Average US waits of about 6 minutes on Election Day and 4 minutes early in 2022 (MIT Survey of the Performance of American Elections).
- Average waits of about 13 and 20 minutes in 2012 (Pew).
- A mean of about 19 minutes at the polling place in 2016, from smartphone location data.
- Travel cost of about US$1.60 a trip in New Zealand.

No source measures the cost of becoming informed. The Cost of Voting Index ranks states' laws but gives no minutes or dollars.

**In your thought experiment, C cancels.** You go to the polls in both worlds, so the experiment isolates p × B. Cost enters where it belongs: at the real choice of whether to go at all. The model keeps the two apart. **p × B is "the importance of a vote", and C is the bar it must clear.** Per your 19:39 message, I'll model the cost factors myself and not bring them to you one by one.

## 6. Beyond a US two-way race

The same event underlies every system. The other voters leave the result within one vote of a boundary, and your ballot pushes it across. What changes is what flips and how many boundaries there are (`research/electoral-systems.md`, unverified):

- **Three or more candidates (plurality):** decisive only between the top two, at about the same size as a two-way race. A vote for a candidate far behind is worth about zero.
- **Proportional representation:** a vote is more likely to move *a seat* (roughly seats ÷ voters), but a seat is one of many, so B is smaller.
- **Runoffs, ranked choice, STV:** more boundaries, so more ways to be decisive. Occasionally ranking someone higher makes them lose, so the sign of a vote's effect isn't always the intuitive one.
- **Referendums:** a two-way race with the threshold (50%, or a supermajority) in place of 50-50.
- **Control of a chamber:** two stages, like the Electoral College.
- **Tiny electorates:** p is large. With 9 other voters split by coin flip, it's about 10 to 12%.

No published decisiveness estimate exists for primaries or chamber control. We would compute those ourselves.

## 7. What happens at a margin of one

At one vote, the counted margin doesn't actually decide. Recount rules (about 21 states recount automatically), courts and tie-break rules do. About 28 states break a legislative tie by lot and 14 by a new election (unverified). Counting error is far larger than one vote: Minnesota's 2008 Senate recount changed 2,170 votes in 2.4 million, and statewide recounts shift margins by hundreds.

This doesn't break the model. With recounts and noise, your ballot still shifts the *chance* your side is declared the winner by about the same p. It nudges the whole distribution of possible outcomes by one vote, and the chance that the nudge crosses the line is the same "closeness ÷ voters" quantity. Gelman, King & Boscardin address this objection directly (unverified; to be read at source). The site should still say plainly that one vote never literally decided a statewide race.

## 8. Two modes for the site

**Simple mode: one picture, three dials.** Choose an election (or its size, its expected margin and how uncertain that is). The page shows **the chance it comes down to your vote**, as something a person can feel ("you are more likely to …"), and then **the break-even stakes: what the outcome would have to be worth for your vote to pay.** The arithmetic is one line: p ≈ closeness ÷ voters, and B* = C ÷ p.

**Full mode: the real model.** The forecast-based, two-stage computation for real past elections (state, then Electoral College; seat, then chamber). It shows each input and its source, the historical record of near-ties as the check, and the welfare choice in B made explicit. A reader who doubts the simple mode can open the full one and see the same answer derived.

## 9. Frameworks the model does not use, kept visible

So nothing is foreclosed, these exist, and each changes *the question*, not the answer to yours:

- **Causal contribution** (Goldman, Tuck): your vote is "among the causes" even when it isn't decisive. It accepts that p is tiny and denies that p is the test. It gives no expected-benefit number.
- **Evidential or correlated choice:** your choice is evidence that people like you choose the same way. This one is subtle, and §10 asks about it.
- **Rule or group views:** what matters is the rule "people like me vote", not one ballot. That contradicts holding everyone else fixed.
- **Expressive voting and duty (the "D" term):** the act itself is the benefit. You've excluded it by definition.

## 10. Questions for you

1. **Whose welfare is in B?** Only the voter's own, or also everyone the outcome affects (Edlin, Gelman & Kaplan; Barnett)? Your conclusion holds on the first and is contested on the second. **My recommendation:** the site leads with the break-even stakes, which holds for either, and states both readings beside it.
2. **"Everything else fixed": causally, or completely?** Your words fix everyone's *behaviour*: no one is persuaded and no one knows. The evidential view says your choice is still *evidence* about what like-minded people do, with no causal link at all. I'm reading your setup as excluding that, so others' choices are independent of yours. Tell me if that's wrong.

I'll take three points as decided unless you say otherwise: the ex ante forecast as the measure (§3), the break-even framing (§2), and C kept outside "importance" (§5).

## 11. What happens next

- When network access is open, four research threads re-read every source at its origin (`briefs/R1` to `R4`), and every figure here becomes verified or corrected.
- Fable then tries to break the model. I bring you the result, then draft the law from it.
