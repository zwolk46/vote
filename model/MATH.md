# The mathematics of a deciding vote: one derivation of p

*Worker M1, 2026-11-07, under `briefs/M1-math-check.md`. Scripts in `model/math/` (Python 3 with numpy, nothing else); `sh model/math/run_all.sh` writes `model/math/OUTPUT.txt`. Every number in this file is in `OUTPUT.txt` under the label cited beside it: (S1.3) is section 1.3 of `OUTPUT.txt`, printed by `s1_two_way.py`; S2 is `s2_conventions.py`, S4 `s4_two_stage.py`, S5 `s5_claims.py`, S6 `s6_simple_mode.py`, S7 `s7_systems.py`, S8 `s8_history.py`. R4's own scripts are copied verbatim into `model/math/r4/` and re-run by S7.*

**What this is.** One derivation of p, the probability that one ballot changes an election's outcome, in the convention the orchestrator fixed; every published formula and example the model cites, reconciled with it factor by factor; every mathematical claim in `model/MODEL-DRAFT.md` §2, 3, 7 and 8 checked; the simplest lay formula and its error over real election sizes; R4's stylised calculations for other systems checked; and what the historical frequencies estimate. I choose nothing for the site. Where two derivations are defensible I give both and name the assumption that separates them (§3.4, §6.1, §8.2).

**Fixed by the brief, not reopened.** The comparison is *counted against not counted*: your ballot for your side counted, against the same ballot not counted, everyone else unchanged. The A-against-B *swing* (your ballot for A replacing a ballot for B) is twice p; it is named wherever it appears and never used as p. Ties follow the jurisdiction's rule: a fair lot where the law says lot; where a new election or a legislature decides, §1.1 says what p means. The measure is ex ante, from a forecast; the historical frequency is the reality check (§8). *Reason, as the brief gives it:* a voter deciding whether to vote compares voting with staying home, not with voting for the other side; the law decides ties, not the model; the decision is made before the count.

**Two findings a reader of the draft should see first.** (i) The published literature's factor of 2 is real and resolves cleanly: Gelman–King–Boscardin's model, Gelman–Katz–Tuerlinckx, Gelman–Katz–Bafumi and Mulligan–Hunter report the *event* (an exact tie or a one-vote win among the others) or the *swing*, both twice our p; Edlin–Gelman–Kaplan, Barnett, GKB's rough formula and Gelman–Silver–Edlin as written are in our convention (§2). (ii) The draft's "1/2 appears in GKB 1998" is half right, and its "$230 million" should be $240 million; everything else in §2, 3, 7, 8 of the draft holds, most of it under a condition the draft should state (§5, §9).

---

## 0. Definitions

Everything below uses these, and `common.py` codes them in the same words.

- **n** is the number of *other* voters, your ballot excluded; each votes A or B. **X** is the number of them for A; **M = 2X − n** is A's margin among them. M has the parity of n: an exact tie (M = 0) needs n even, "A one short" (M = −1) needs n odd.
- **v** is a share: X/n once counted, or the forecast share before the election. The forecast is a density **f(v)**; **f(½)** is its value at a dead heat.
- **W(M)** is the probability that A wins given the others' margin M, under the tie rule: W = 1 for M > 0, 0 for M < 0, and at M = 0 it is **½** (fair lot), **1** (a tie goes to A), **0** (to B), or **π** (a new election or a body settles it, and A's chance in that settlement is π).
- **p**, the quantity the site needs: the rise in A's chance of winning when your ballot for A is counted rather than not counted,

  **p = Σ_M P(M) [W(M + 1) − W(M)].**

- **swing**, the rise when your ballot for A replaces a ballot for B: **swing = Σ_M P(M) [W(M + 1) − W(M − 1)].**
- **event**: "the others are exactly tied, or your side is exactly one short": P(M = 0) + P(M = −1); only one term can be non-zero at a given n.

Four exact distributions of X are available in `common.py`: binomial (a known share v₀), Beta-binomial (v ~ Beta), a normal forecast of v with the binomial folded in by numerical integration, and a Student-t(4) forecast likewise. "Exact p" below always means p computed from one of these by the lattice sum, to numerical precision. *Note (the orchestrator, 2026-11-07, from M2's second pass, `checks/M2-REPORT.md`):* the normal and t forecasts in `common.py` are truncated to (0, 1) and renormalised. That is right for a forecast of the share v, which cannot fall outside (0, 1). It is not right where a normal only stands in for a density measured near ½, as in the like-race route (MODEL §7), whose f(½) is a count of like races in a window: renormalising raises the density at ½ by the inverse of the normal's mass in (0, 1), up to 2× for a flat class (sd_eq > 0.3). There the exact sum uses the stand-in without renormalising, so that it keeps the measured f(½) and agrees with f(½)/(2n) as n grows.

---

## 1. The two-way race, exactly (S1)

### 1.1 p under each tie rule

W(M + 1) − W(M) is non-zero only where M + 1 > 0 ≥ M, that is at M = 0 and M = −1:

- at M = 0: W(1) − W(0) = 1 − π;
- at M = −1: W(0) − W(−1) = π.

So **p = (1 − π) P(M = 0) + π P(M = −1)**, and by parity only one of the two terms exists:

| tie rule | n even (M = 0 possible) | n odd (M = −1 possible) | average over parity |
|---|---|---|---|
| fair lot, π = ½ | ½ P(M = 0) | ½ P(M = −1) | ½ P(event) |
| tie to A, π = 1 | 0 | P(M = −1) | ½ P(event) |
| tie to B, π = 0 | P(M = 0) | 0 | ½ P(event) |
| new election or body, π | (1 − π) P(M = 0) | π P(M = −1) | ½ P(event) |

With the density approximation of §1.2, P(M = 0) ≈ P(M = −1) ≈ f(½)/n, so **under a lot p ≈ f(½)/(2n) for either parity**, and under any other rule p is 0 for one parity and ≈ f(½)/n for the other. Ex ante the parity of n is unknowable (turnout is uncertain by far more than one), so for every rule the ex ante p is f(½)/(2n). The swing has contributions at M = 0 (weight 1), M = 1 (1 − π) and M = −1 (π): ≈ f(½)/n for every parity and rule.

Numbers (S1.1; Beta-binomial forecast, κ = 400, mean 0.51, so the share's sd is 2.5 points): at n = 1,000, lot 0.006363, tie-to-A 0, tie-to-B 0.01273, π = 0.3 gives 0.008908, swing 0.01273; at n = 1,001, lot 0.006321, tie-to-A 0.01264, tie-to-B 0, π = 0.3 gives 0.003792. The lot value is the same for both parities; the deterministic rules alternate between 0 and twice it; the average of the π = 0.3 values is the lot value. At n = 100,000 and 100,001 the lot values are 7.347e-05 and 7.346e-05 against f(½)/(2n) = 7.359e-05.

**What p means where a new election or a legislature decides a tie.** p = (1 − π) P(M = 0) for an even n and π P(M = −1) for an odd n: your ballot either turns a tie (worth π to A) into a win, or a loss into a tie worth π. Ex ante this averages to f(½)/(2n) *whatever π is*, so the site needs π only if it wants to show a parity-specific number, which it cannot know. What the rule changes is not p but the value of the outcome at the tie, §5.1.

### 1.2 The two standard approximations and their constants

**(a) Share density.** P(X = k) = ∫ Bin(k; n, v) f(v) dv ≈ f(k/n)/n when f varies little over the binomial's width 1/(2√n). Hence P(M = 0) ≈ f(½)/n and p ≈ **f(½)/(2n)**. This is Mulligan–Hunter's f(½)/(v + 1) (with v + 1 for n, a convention of theirs) and GKB's "f/n" at the state, both of which are the *event*, not p.

**(b) Margin density.** The margin in votes m = 2X − n = n(2v − 1) has density g(m) = f((m + n)/(2n))/(2n), so **g(0) = f(½)/(2n) = p**: *p is exactly the density of the margin in votes at zero*, which is Gelman–Silver–Edlin's phrase. But m takes every *second* integer, so P(m = 0) ≈ 2 g(0) = f(½)/n. A reader who takes "the density at zero" for "the probability of an exact tie" is off by 2; the paper's words are in our convention, its intent is not stated (§3.4).

Numbers (S1.2; normal forecast with mean μ and sd τ): μ = 0.5, τ = 0.03, n = 10,000: f(½) = 13.2981, event 0.00133, p = f/(2n) = 0.0006649, exact p = 0.0006558 (ratio 0.9863). The 1992 popular vote as GKB set it (mean 0.515, sd 0.056, 92 million): f(½) = 6.8729, event 7.471e-08, p = 3.735e-08, exact 3.735e-08.

### 1.3 Size of the error

Folding the binomial into a normal forecast gives a normal with variance τ² + 1/(4n) (S1.3, "convolved"): at μ = ½ the exact p is f(½)/(2n) × τ/√(τ² + 1/(4n)), so the relative error of f(½)/(2n) is **+1/(8nτ²)** to first order, and the convolved form is within 1% everywhere in the table. From the table: 12.6% at nτ² = 1 (n = 100, τ = 0.1), 4.6% at 2.7 (n = 3,000, τ = 0.03), 1.4% at 9 (n = 10,000, τ = 0.03), 1.3% at 10 (n = 1,000, τ = 0.1); 411.2% at nτ² = 0.01 (n = 100, τ = 0.01), where the forecast is narrower than the count noise and the race is effectively one of known share. Off centre the sign reverses (the widening lifts a tail): −16.3% at n = 1,000, τ = 0.03, μ = 0.55.

*Condition for the site:* f(½)/(2n) is good to 2% once nτ² > 6.25 and to 10% once nτ² > 1.25 (first order); below that use the convolved form or the exact sum. *Note (M2, 2026-11-07, `checks/M2-REPORT.md` 1.8):* this condition is stated at μ = ½; away from it the density form's error also grows with z = (μ − ½)/τ (for Congress 2006–2024: within 0.4% where p ≥ 10⁻⁶, 1% where p ≥ 10⁻⁸, up to 6% at z = 8.8 where p ≈ 10⁻²¹), while the convolved form matches the exact sum to 0.11% everywhere. No figure the site shows is affected. nτ² > 6.25 says the forecast's spread in votes, nτ, is at least 5 times the count noise √n/2; a few hundred voters with a 10-point sd already qualify (n = 300, τ = 0.1: 4.4%).

### 1.4 A known share

With no forecast uncertainty (v₀ known): p = ½ C(n, n/2) v₀^{n/2} (1 − v₀)^{n/2} for n even and ½ C(n, (n−1)/2) v₀^{(n−1)/2} (1 − v₀)^{(n+1)/2} for n odd, both ≈ ½ √(2/(πn)) [4v₀(1 − v₀)]^{n/2}. At v₀ = ½ this is **1/√(2πn)**, half of the swing's √(2/(πn)); at any other v₀ it is exponentially small (S1.4: n = 999, v₀ = 0.5: 0.01261 against 1/√(2πn) = 0.01262; v₀ = 0.51: 0.01012; v₀ = 0.55: 7.534e-05; n = 999,999, v₀ = 0.51: 5.2e-91). This is the regime of every "random voting" formula in the literature (GKT's exact count, GKBafumi's √(2/π)/√n), and it is not the regime of any real election, where τ ≫ 1/(2√n).

### 1.5 A Student-t forecast

GSE use a t with 4 degrees of freedom. At the centre the t's density is 0.375/s for scale s and 0.530/sd for standard deviation sd, against the normal's 0.399/sd (S2.5), so the three ways of matching a t to a normal differ by up to 1.33 at the centre; in the tails they differ enormously (S1.5, n = 1,000,000, sd 0.03): at μ = 0.70 the normal gives 1.494e-15 and the t 3.402e-09 (same sd) or 1.225e-08 (same scale). GSE's District of Columbia example (normal 5e-85, t 2e-12) is this tail difference. Which tail a forecast has is a modelling choice the site must name; §5.7.

### 1.6 Break-even stakes

B* = C/p is a rearrangement of pB > C. With the event probability in place of p, B* is half what it should be. At p = 1e-7 (1 in 10 million) and C = $4 and $12, B* = $40,000,000 and $120,000,000; at p = 1 in 60 million and C = $4, B* = $240,000,000 (S1.6, S5.2).

---

## 2. The published conventions, factor by factor (S2)

Read at the page (R1's and R3's ledgers, and the PDFs in this thread's scratch), each source's p in our convention is:

| source and the quantity it prints | what it is | to get ours, multiply by |
|---|---|---|
| Gelman, King & Boscardin 1998, eqs. 1–3: the model's state term f/n, the College's ½ at the two tie end-points | the event at the state; the ½ belongs to the College tie, not to the ballot | **½** |
| GKB 1998 §5, the rough .008 e/n (its ½ is "for casting a vote, not switching a preference") | our p, by its own words | **1** |
| GKB 1998 §5, "20/n" (τ = 2%, μ = ½) and "1 in 13.3 million" (1992 popular vote) | the event; f(½) = 19.947 and 6.8729 | **½** (10/n; 1 in 26.6 million) |
| Gelman, Katz & Tuerlinckx 2002, the definition P(win \| vote A) − P(win \| vote B) and the exact count √(2/(πn)) | the swing | **½** |
| GKT 2002, eqs. (2) and (5) as printed: the density of the differential V = v_A − v_B at 0, over n | f_V(0) = f_v(½)/2, so f_V(0)/n = f_v(½)/(2n) = ours; inconsistent with the paper's own definition by 2 | **1** |
| GKT 2002, the binomial display for the exact count | omits 2^{−(n−1)}; with it, C(1000, 500)/2^1000 = 0.025225 = the swing | — |
| GKT 2002, eq. (6), 1/(n sd(V)) | drops the constant 1/√(2π) = 0.399 (a proportionality) | — |
| Gelman, Katz & Bafumi 2004, eq. (2) and √(2/π)/√n | the swing | **½** |
| GKBafumi 2004, p. 663, "1.84/n" | an arithmetic slip; the stated inputs give 10.65/n (swing) | **½ of 10.65** = 5.32/n; §3.1 |
| Gelman, Silver & Edlin 2012, "the density at 0" of the margin in votes (t₄, mean M, scale S) | as written, our p; if an exact-tie probability was intended, twice ours; the centre value is 0.375/S for a scale S and 0.530/S for an sd S | **1 as written**; ½ if a tie was meant; §3.4 |
| Edlin, Gelman & Kaplan 2007, p = K/n, the ±6% case 1/(0.12n), "half the probability that a single vote can make or break an exact tie" | our p: a differential uniform on ±6% has f_V(0) = 8.33, and f_v(½)/(2n) = 16.7/(2n) = 8.33/n | **1** |
| Barnett 2020, EB = ½ B d, d the one tie event possible for the parity; d ≥ 1/N | ½ d = our p; the bound is p ≥ 1/(2N) | **1** |
| Mulligan & Hunter 2003, f(½)/(v + 1), "2/v", "1 in 89,000" | the pivotal-ballot frequency = the event | **½** (1/v; 1 in 178,000) |
| Myatt & Fisher 2002, Lemma 1 eq. (2), "/(6n)" | a misprint for "/n"; the two-way constant is the integral over n | §3.3 |

Checks behind the table (S2.1–2.8): the random-voting constants by exact count at n = 10,000 are swing 0.007979 = √(2/(πn)) and p = 0.003989 = 1/√(2πn), so "2/√π = 1.1284" (an extraction error in the first-pass report) is neither; GKB's 1992 figure reproduces as 1 in 13,385,838 (event) and 1 in 26,771,675 (ours); their rough formula gives 0.00818 e/n, printed .008 e/n, and 1 in 24,444,444 at e = 10, n = 2,000,000, printed 1 in 25 million; M&H's Figure 5 gives f(½) = 2.222, printed "~ 2", and their footnote-14 value 10^−1108 reproduces as 10^−1107.0 from the normal density (the exact binomial is 10^−1079.9: the normal approximation is off by 27 orders of magnitude that far out, a warning for any tail figure); EGK's K = 10 is a differential uniform on ±5%; Barnett's $134.92 = ½ × $33e9/122,293,322.

**Why the ½ keeps appearing and disappearing.** Three different objects carry a ½ for three different reasons: (i) the ballot's effect at a tie is half a win under a lot (ours); (ii) a tie among *other* voters, M = 0, is only half of the decisive events, the other half being M = −1, and parity picks one; (iii) in the College, a 269–269 tie is worth half to each side, so the two end-points of the decisive window get weight ½ (GKB's eq. 3, our §4.1). A source that counts the *event* has no (i); one that counts the swing has none of them. The brief's "name the swing wherever it appears" is the right discipline because (ii) and (iii) survive in every convention and only (i) is the difference between p and the event.

---

## 3. The flagged examples, settled (S2.3–2.5)

### 3.1 Gelman, Katz & Bafumi's "1.84/n"

Their text: 10,000 voters, forecast 52% with standard error 3%. The printed expression [1/(√(2π) · 0.03)] exp(−½(0.05/0.03)²) evaluates to **3.316** (R1's figure). The stated inputs, with distance 0.02 = 0.52 − 0.50, give **10.648** (R4's figure, and GKB 1998's §5 formula). The printed **1.84** reproduces only as [1/√(2π · 0.03)] exp(−½(0.02/0.03)²) = 1.844, that is with the 3% standard error used as a variance in the normalising constant. So R1 and R4 disagree because R1 evaluated what is printed and R4 what was meant; the number itself is a slip. Under the stated inputs the density is 10.65: the event or swing is 10.65/n, our p is 5.32/n = 0.0005324 at n = 10,000, and the exact p for that forecast with the binomial folded in is 0.0005283 = 5.283/n.

### 3.2 Gelman, Katz & Tuerlinckx's eq. (2) and eq. (5)

Both write the power as the density of the *differential* V = v_A − v_B at zero, divided by n. Since V = 2v − 1, f_V(0) = f_v(½)/2 and f_V(0)/n = f_v(½)/(2n), which is our p and half of the paper's own definition (P(win | vote A) − P(win | vote B), the swing). Under random voting f_V(0)/n = 1/√(2πn) = 0.003989 at n = 10,001 while the exact swing printed beside it is √(2/(πn)) = 0.007978. Their binomial display omits 2^{−(n−1)}, and eq. (6)'s 1/(n sd(V)) drops the constant 0.399; neither affects their conclusions, which are about proportionality. The site should cite GKT for the shape (p ∝ f_V(0)/n) and take its constant from §1.

### 3.3 Myatt & Fisher's "6n"

Their Lemma 1 eq. (2) prints Pr[x₁ = x₂ > x₃] ≈ (∫_{1/3}^{1/2} f(z, z, 1 − 2z) dz)/(6n). With a uniform belief on the simplex (f = 2, every outcome of n voters equally likely) the exact count gives n · Pr = 0.33442, 0.33344, 0.33334 at n = 302, 3,002, 30,002, converging to the integral 1/3 = 0.33333, whereas "/(6n)" would give 0.05556. The three-way term is as printed: n² · Pr[x₁ = x₂ = x₃ + 1] → 1.9980 → f(⅓, ⅓, ⅓) = 2. So the two-way constant is the integral over n, not 6n; Proposition 1 and eq. (3) stand. (R4 flagged this; it is confirmed.)

### 3.4 Gelman, Silver & Edlin's density at zero, and their scale

Two separate questions. **Scale:** a t₄ with scale S has centre density 0.3750/S; a t₄ with *standard deviation* S (scale S/√2) has 0.5303/S; a normal with sd S has 0.3989/S. So depending on what GSE's "scale" is, their centre value is 0.94 or 1.33 of a normal's with the same sd: a spread of √2. **Convention:** as §1.2(b) shows, "the density at 0 of the margin in votes" is g(0) = f_v(½)/(2n) = our p, while an exact tie has probability 2g(0). The paper does not say which it intends. Two readings are defensible: (a) take the words, so their "1 in 10 million" is in our convention; (b) assume they meant an exact tie, so it is twice ours. I give both; the site must say which it uses and why. Their code was not read (not in any source read; R1's ledger).

---

## 4. Two stages (S4)

### 4.1 State, then Electoral College

Let E_{−i} be A's electoral votes from the other states and e_i your state's. The presidency: W_EC(E) = 1 for E ≥ 270, π_H for E = 269 (the House decides; ex ante ½), 0 for E ≤ 268. Your ballot's effect is

**p_i = Σ_{M_i} P(M_i) · E[ W_EC(E_{−i} + e_i) − W_EC(E_{−i}) | M_i ] · [W(M_i + 1) − W(M_i)],**

non-zero only at M_i ∈ {0, −1}, so **p_i = p_state,i × W_i** with p_state,i = f_i(½)/(2n_i) (§1) and **W_i = E[window | the state is tied]**, where the window weight is 1 for 270 − e_i ≤ E_{−i} ≤ 268, π_H at E_{−i} = 269 − e_i and 1 − π_H at 269: with π_H = ½ this is GKB's "½ at the two end-points". *This product is an identity.* The usual formula replaces the conditional W_i by the unconditional W′_i, which is exact only if the states are independent.

**What independence costs.** With the Economist's 2016 back-test means and intervals for the 51 states (sd = se × 1.68/1.96, from 0.0206 to 0.0223), the 2016 electoral votes and the 2016 two-party vote (128,369,958 in all), and a national swing δ shared by every state with a share ρ of the typical state's variance (v_i = μ_i + δ + ε_i), both W_i and W′_i are computed exactly by dynamic programming over states at each δ and integration over δ, with δ | (state i tied) from its posterior (S4.1–4.2). Results:

- ρ = 0: W = W′ exactly (the product formula is right when states are independent).
- states within 2 points of even (8 of them): W′/W between 0.937 and 1.111 at ρ = 0.3, 0.906 to 1.172 at 0.5, 0.880 to 1.229 at 0.7;
- 2 to 3 points off (5): 0.938 to 1.198, 0.919 to 1.325, 0.903 to 1.459;
- 3 to 10 points off (20): 0.86 to 2.70, 0.87 to 6.14, 0.88 to 16.00;
- 10 points or more: from 1.1 to 35 at ρ = 0.3 and up to 1.5e+03 at 0.5, with W | tie below 1e-6 for DC.

Utah (mean 0.375): W | tie falls from 0.0735 at ρ = 0 to 0.0044 at ρ = 0.5 while W′ is 0.0644: a tie in Utah implies a national swing that hands A nearly every state, so the College is no longer on a knife-edge. But p_state there is 3.68e-15; the error lands where p is negligible. For Florida (mean 0.496, p_state 1.04e-06) W | tie is 0.3545, 0.3177 at ρ = 0 and 0.5 against W′ 0.3263.

**Reading.** The product formula is safe where p matters and wrong where it does not. The national swing lowers every W (states move together, so the College is less often one state from 269) independently of the conditioning: the vote-weighted average p falls from 1 in 7,229,955 at ρ = 0 to 1 in 8,763,009 at ρ = 0.7 (S4.3), and the product formula's average is within 1% of the conditional one (1.149e-07 against 1.141e-07 at ρ = 0.7). The largest state p is Nevada's, 7.487e-07 at ρ = 0 and 6.559e-07 at ρ = 0.7. *These are the Economist's 2016 back-test, not a 2016 forecast anyone saw; they illustrate the structure and are not offered as the site's numbers.*

*Condition for the site:* use the product formula with the unconditional stage-two factor for states within 2 points of even, where it is within 12%, 17% and 23% at ρ = 0.3, 0.5 and 0.7; for the rest either compute the conditional factor (the DP in S4 does it in seconds) or accept that the product overstates p by a factor that grows with the state's lean and with ρ, on a p that is already tiny.

### 4.2 Seat, then chamber

With 435 seats, A's majority needs 218, and the flip of your seat decides control iff the other 434 give A exactly 217: a single lattice point, no half-weighted ends (R4's structural note is right). The same DP with a stylised chamber (the other 434 seats' means spread evenly from 0.30 to 0.70, sd 0.03, common swing share ρ; S4.4):

| your seat's mean | ρ | P(217 \| seat tied) | P(217) unconditional | ratio |
|---|---|---|---|---|
| 0.50 | 0 | 0.0931 | 0.0931 | 1.000 |
| 0.50 | 0.5 | 0.0239 | 0.0171 | 1.398 |
| 0.45 | 0.5 | 0.0064 | 0.0171 | 0.372 |
| 0.40 | 0.5 | 0.0001 | 0.0171 | 0.007 |

Conditioning bites harder than in the College because a tie in a seat that leans 10 points implies a swing that moves the expected seat count by tens of seats (to 271.2 at ρ = 0.5 for the 0.40 seat). R4's `chamber.py` reports the unconditional P(217) (its rows 0.0257, 0.0155, 0.0108 at its m₀ = 0 are the ρ > 0 unconditional column's order of magnitude); the model should use the conditional form, and the chamber inputs here are stylised, not a source.

---

## 5. The draft's claims (S5)

Verdicts are in the table of §9; the derivations the verdicts rest on:

- **5.1 "p × B and nothing else."** E[gain] = P(M = 0)(U_A − U_tie) + P(M = −1)(U_tie − U_B). This is pB when U_tie = (U_A + U_B)/2 (a tie by lot valued at its expectation), and under any deterministic rule. Otherwise there is a tie-value term: with U_A = 1, U_B = 0, U_tie = 0.3, the gain is 1.400 pB at n = 1,000 and 0.600 pB at n = 1,001, averaging to pB over parity.
- **5.6 "p falls as 1/N."** N·p at τ = 0.03 is 3.411, 5.878, 6.558, 6.640, 6.648 for N = 100 to 1,000,000: constant once Nτ² ≫ 1. With a known 50-50 split N·p is 3.979 to 398.942, growing as √N.
- **5.7 "faster than exponentially."** True for a normal forecast (p(3 sd)/p(0) = 0.0111 = exp(−4.5)); false for a t₄: 0.0141 (same sd) or 0.0525 (same scale) at 3 sd, and 0.00149 or 0.00707 at 5 sd against the normal's 3.74e-06.
- **5.8 "uncertainty cuts both ways."** p ∝ (1/τ) exp(−d²/(2τ²)) peaks at τ = d: at μ = 0.52 (n = 100,000) p is 2.8e-05, 6.05e-05, 5.32e-05, 3.68e-05, 1.95e-05 for τ = 0.01, 0.02, 0.03, 0.05, 0.10; at μ = 0.55 it is 9.96e-10, 4.45e-06, 1.66e-05, 2.42e-05, 1.76e-05. More uncertainty helps iff |μ − ½| > τ.
- **5.10 "the same p with recounts and noise."** With π(m) = P(A is declared the winner | counted margin m) a logistic of width w votes, the gain Σ P(M)[π(M + 1) − π(M)] telescopes to the density of the margin at zero, p, while w ≪ nτ: at n = 100,000, τ = 0.03 (spread 3,000 votes), gain/p is 1.000 at w = 10 and 100, 0.958 at 1,000, 0.760 at 3,000, 0.347 at 10,000 (μ = ½; at μ = 0.52: 0.975, 0.830, 0.420). Recount zones of a few hundred votes against forecast spreads of tens of thousands put every real election in the w ≪ nτ regime.
- **5.11 "the chance your ballot changes the winner."** With the tie-breaking coin the same in both worlds, P(the winner differs) = ½P(M = 0) + ½P(M = −1) = p under a lot, and = P(event) = p under a deterministic rule.

---

## 6. The simplest lay formula (S6)

### 6.1 Two defensible forms

(F) the full one-line formula **p = f(½)/(2n)**, with f the forecast density of the share at a dead heat; and (Q) **p ≈ 25 q₁/n**, with q₁ the forecast probability that the share lands within one point of 50-50. They agree because q₁ ≈ 0.02 f(½) when the forecast is wider than the one-point window: q₁/(0.02 f) is 0.856, 0.960, 0.982, 0.993 for τ = 0.01, 0.02, 0.03, 0.05 (S6.1). (Q) is the one a person can say and the one that maps onto the draft's "closeness ÷ voters"; (F) is the one the model should compute. A fixed constant K/n (Edlin–Gelman–Kaplan's 8.33/n, or "10/n") is not a candidate: it ranges from 0.84 to 15.43 of the exact p over the table (S6.2), because the closeness it drops varies by a factor of 7 between a 50-50 and a 60-40 race at a 5-point sd and by 90 for 65-35 (S6.3).

### 6.2 Error, shown numerically

Against the exact p (normal forecast, binomial folded in) over n from 300 to 16,000,000, μ from 0.50 to 0.60 and τ from 0.02 to 0.10 (S6.2):

- n ≥ 1,000: (F) within a factor 1.28, (Q) within 1.22;
- n ≥ 1,000 and τ ≥ 0.03: (Q) within 1.16;
- n ≥ 10,000 and τ ≥ 0.03: (Q) within 1.032.

The worst rows are small n with a narrow forecast (n = 300, τ = 0.02: (Q) 1.687), where §1.3's +1/(8nτ²) is large; there the exact lattice sum is cheap and should be used. Over the brief's range (S6.5): n = 300 (τ = 0.05) exact 0.01149 (1 in 87), (Q) 1.150 of it; a presidential state, Florida 2016 in the back-test (n = 9,122,861, mean 0.496, sd 0.0206), exact 1.042e-06 (1 in 960,105), (Q) 0.963 of it, before the stage-two factor of §4.

### 6.3 The draft's "closeness ÷ voters"

With closeness = q₁ the lay formula is 25 q₁/n; the *event* is 50 q₁/n; q₁/n with no constant is 1/25 of p. At q₁ = 0.3 and n = 100,000: p = 7.50e-05 (1 in 13,333), event 1.50e-04, q₁/n = 3.00e-06 (S6.4). The draft's line needs its constant and its definition of closeness.

---

## 7. Other systems: R4's stylised calculations (S7)

R4's seven scripts are re-run verbatim (S7.1) and reproduce their reported numbers. Checked by a different route:

| system | R4's calculation | check | verdict |
|---|---|---|---|
| plurality, 3 candidates, known shares | exact lattice sum (`plur.py`) | the top-two difference has variance n(p₁ + p₂), so Q ≈ two-way Q/√(p₁ + p₂): ratios 0.9997 to 1.0027 at n = 1,000, 1.0000 to 1.0009 at 10,000 (S7.2) | sound; usable as the model's own |
| plurality, 3 candidates, Dirichlet forecast | exact Dirichlet-multinomial sum | continuous route: for each rival j, D = v₁ − v_j = s(2r − 1) with s ~ Beta, r ~ Beta independent, f_D(0) = f_r(½) E[1[s > ⅔]/(2s)], noise folded in; ratios 0.956 to 1.000 at n = 1,000, 0.994 to 1.000 at 10,000 (S7.3) | sound; note x₁ − x₂ takes every integer, so Q ≈ f_D(0)/n with no further ½ |
| list PR, "about M/N" | Monte Carlo D'Hondt, five parties (`pr.py`): Q_j/(M/N) 0.76 to 0.99 at M = 27, 0.70 to 0.90 at M = 150, but 0.00 to 0.91 at M = 5 and 10 | two-party D'Hondt, exact: Q/(M/N) = 1.037 and 1.006 when the forecast spans 0.4 to 0.6 of a seat (M = 27), 0.324 when it spans 0.04 of a seat, 2.664 and 0.000 at M = 5 (S7.4) | sound as "about M/N" only when the forecast spans half a seat or more; and a seat is not a winner |
| referendum, threshold t | Q_no/Q_yes averaged over N (`ref2.py`) | Z = (1 − t)Y − tX decides; a Yes adds 1 − t, a No subtracts t, so Q_no/Q_yes = t/(1 − t): 1.500 and 1.989 at t = 0.6 and ⅔ (forecast 0.60), 1.508 and 2.000 (forecast ⅔) (S7.5) | sound; R4's averaging over N is legitimate: at a fixed N the lattice makes Q_yes 0 or 0.001596 by the fractional part of tN |
| quorum | structure only | Q_yes ≈ tie term + f_T(q)/R × P(pass \| quorum); a No ballot that completes the quorum helps the proposal; stylised: quorum term 9.903e-06 against tie term 3.113e-06 (S7.6) | structure only; no number offered |
| tiny electorates | exact binomial | p at N = 9 is 0.1230 against 1/√(2πN) = 0.1330, 8.1% high (S7.7) | sound; use the exact sum below a few hundred voters |
| runoff, IRV, STV | none; Baltz's closed forms unreliable (R4) | structure: sum over pairs or elimination orders of two-way p's with conditional forecasts | no number; compute by enumeration or simulation |
| chamber | `chamber.py`, unconditional P(217) | §4.2: conditional form | use the conditional form |

---

## 8. What the historical frequencies estimate (S8)

### 8.1 The figures

Mulligan & Hunter's "1 in 89,252" is 20,685 winner's ballots in the one US House race decided by one vote (NY-36, 1910) over 16,577 × 111,370 = 1,846,180,490 ballots; both finalists' ballots give 1 in 44,627. Their state figure, "1 in 15,444", counts all 61,328 ballots in nine pivot elections over 947,171,688; in the US treatment it would be 1 in 25,527. Klarner's data give 52 contests with a margin of 0 or 1 in 109,093 with a margin (1 in 2,098), 30 in 99,165 single-seat contests (1 in 3,306), and 5 in 23,830 seats for 2018–2024 (1 in 4,766). (R2's measurements, `research/historical-close-races-v2.md` §1a–1b.)

### 8.2 What they estimate

Ex ante, with parity unknown, election e has P(exact tie) ≈ f_e/(2N_e), P(one-vote win) ≈ f_e/N_e, p_e = f_e/(2N_e) and event_e ≈ f_e/N_e. "Ballots cast for a candidate who tied or won by one" number N_e in a tie and ≈ N_e/2 in a one-vote win, so E[count_e] ≈ f_e, and the per-ballot frequency F = Σ count_e / Σ N_e estimates **Σ f_e / Σ N_e, the ballot-weighted average of the event probability**, twice the ballot-weighted average of p. Counting every ballot in a pivot election gives 1.5 Σ f_e / Σ N_e (M&H's eq. 4), three times the average p. Hence the implied ballot-weighted average p is 1 in 178,504 (US), 1 in 46,333 (state, all ballots) or 1 in 51,055 (state, US treatment); the implied average density at a dead heat is f̄ = 1.25 (US) and 1.02 (state), against M&H's own "~ 2" from their Figure 5 and GKB's 4.5 for presidential-state forecasts (18% within 2 points): House and state races are on average less close. Two defensible readings of "what F is": the ballot-weighted average event probability (the derivation above), or, if one insists on p, half of it. Klarner's per-contest rate estimates the *contest*-average of P(margin 0 or 1) = 1.5 f_e/N_e, three times the contest-average p (0.0001589, 1 in 6,294); contest averages weight small districts, ballot averages large ones, so the two are not comparable.

### 8.3 How they relate to the ex ante p

(i) F is an average over a population of elections, lopsided ones included, not a probability for one; the ex ante p of one election ranges over orders of magnitude around it. (ii) F is a point estimate from a Poisson count: one US event has 95% interval [0.025, 5.57] for its expected count, so the rate is known to within a factor 5.6 above and 39.5 below, and the data are consistent with 1 in 16,019 and with 1 in 3,525,271; nine state events give [4.115, 17.08]; Klarner's 52 give [3.56e-04, 6.25e-04] per contest. (iii) F counts the first official margin; M&H's own later-count check cut their unweighted frequency by 50% and the vote-weighted one by 76%, so F overstates how often a ballot settled a result under §5.10's smoothed definition. *(Note, M2, 2026-11-07, `checks/M2-REPORT.md` 5.2: for an expected count within k votes, the density form 2pk holds while f is flat across the band; for the presidency it agrees with the cdf form within 0.4% up to k = 20,000 and understates it beyond 50,000, so a large k uses the cdf form.)* (iv) The reality check the model can pass: the sum of its event probabilities over a population of elections must land inside the Poisson interval of the observed count. That needs a forecast per contest, which no source read supplies; what can be checked now is the average density, F × N̄ = 1.25 and 1.02 against ~2.

---

## 9. Findings

Verdicts: **holds**; **holds under condition** (the condition is in the corrected statement); **wrong** (with the corrected statement). "Where" names the OUTPUT.txt section and its script.

| # | claim (source) | verdict | corrected or conditioned statement | where |
|---|---|---|---|---|
| 1 | Draft §2: the gain from voting equals p × B "and nothing else" | holds under condition | a tie is valued at the average of the two outcomes, or the tie rule is deterministic; otherwise a tie-value term is added (1.400 pB / 0.600 pB by parity at U_tie = 0.3) | S5.1 `s5_claims.py` |
| 2 | Draft §2: B* = $40 to $120 million at p = 1 in 10 million | holds | — | S5.2 |
| 3 | Draft §2: $230 to $720 million at p = 1 in 60 million | wrong | $240 to $720 million (C = $4 gives $240,000,000) | S5.2 |
| 4 | Draft §2: "p is the chance that your ballot changes the winner" | holds | with the tie coin the same in both worlds | S5.11 |
| 5 | Draft §3: p = ½ × [chance of a tie + chance of one short] | holds under condition | a fair lot; only one term is non-zero at a given n; under a deterministic rule p is 0 or P(event) by parity | S1.1, S5.3 |
| 6 | Draft §3: "the ½ appears in GKB 1998 and Barnett 2020" | holds in part | Barnett yes; GKB only in the §5 rough formula, not in the model (eqs. 1–3), whose ½ weights the College tie | S2.6, S5.4 |
| 7 | Draft §3: p ≈ closeness ÷ voters "up to a small constant" | holds under condition | p = f(½)/(2n), or 25 q₁/n with q₁ = P(within one point); error +1/(8nτ²) | S1.3, S6.1, S6.4 |
| 8 | Draft §3: p falls roughly as 1/N | holds under condition | nτ² ≫ 1; with a known 50-50 split p falls as 1/√N, with any other known split exponentially | S5.6, S1.4 |
| 9 | Draft §3: p falls faster than exponentially away from 50-50 | holds under condition | for a normal forecast; polynomial (slower than exponential beyond ~3 sd) for a t₄ | S5.7, S1.5 |
| 10 | Draft §3: more uncertainty helps a lopsided race and hurts a dead-even one | holds under condition | the line is \|μ − ½\| = τ: helps iff the expected margin exceeds one forecast sd | S5.8 |
| 11 | Draft §3: structure multiplies stages | holds under condition | exact with the conditional stage-two factor; the unconditional one is within 12% to 23% (ρ = 0.3 to 0.7) for states within 2 points of even, off by orders of magnitude (on negligible p) for lopsided states | S4.1–4.3 |
| 12 | Draft §7: with recounts and noise your ballot shifts the chance by about the same p | holds under condition | the noise zone w ≪ the forecast spread nτ (gain/p 0.958 at w = nτ/3, 0.760 at w = nτ) | S5.10 |
| 13 | Draft §8: the simple mode's one line, p ≈ closeness ÷ voters and B* = C ÷ p | holds under condition | constant and closeness as in 7; within a factor 1.2 of exact for n ≥ 1,000 and τ ≥ 0.02 | S6.2 |
| 14 | Draft §2, §3: GSE's 1 in 10 million and 1 in 60 million | holds under condition | in our convention as GSE's words stand; twice ours if they meant an exact tie; a √2 scale ambiguity at the centre | S2.5, S5.12 |
| 15 | GKB 1998 eqs. 1–3: the model's p | — | the event at the state (f/n); ours is half | S2.6, S2.9 |
| 16 | GKB 1998: "1 in 13.3 million", "20/n" | — | reproduce as 1 in 13,385,838 and 19.947/n (event); ours 1 in 26,771,675 and 10/n | S2.6 |
| 17 | GKB 1998 §5: .008 e/n, 1 in 25 million | — | reproduces as 0.00818 e/n and 1 in 24,444,444; already in our convention | S2.6 |
| 18 | GKT 2002: definition and exact count √(2/(πn)) | — | the swing; ours 1/√(2πn) (0.003989 at n = 10,000) | S2.1 |
| 19 | GKT 2002 eqs. (2), (5): density of the differential over n | — | equals our p; inconsistent with the paper's definition by 2 | S2.2 |
| 20 | GKT 2002: binomial display; eq. (6) | — | omits 2^{−(n−1)} (with it 0.025225 at n = 1,000); eq. (6) drops 0.399 | S2.1, S2.2 |
| 21 | GKBafumi 2004: √(2/π)/√n | — | the swing; ours half | S2.1 |
| 22 | GKBafumi 2004: "1.84/n" (R1 3.316, R4 10.65) | wrong in the source | printed expression 3.316; stated inputs 10.648 (swing); 1.844 only with the sd used as a variance; ours 5.32/n, exact 5.283/n | S2.3 |
| 23 | GSE 2012: "density at 0 of the t₄, mean M, scale S" | — | = our p as written; centre value 0.375/S (scale S) or 0.530/S (sd S) against 0.399/S normal | S2.5 |
| 24 | EGK 2007: p = K/n, 1/(0.12n) | — | our convention (8.33/n; K = 10 is ±5%) | S2.8 |
| 25 | Barnett 2020: EB = ½ B d; d ≥ 1/N | — | ½ d = our p; p ≥ 1/(2N); $134.92 reproduces | S2.8 |
| 26 | M&H 2003: f(½)/(v + 1), "2/v", "1 in 89,000" | — | the event; ours 1/v, 1 in 178,000 | S2.7, S8.2 |
| 27 | M&H footnote 14: 10^−1108 | holds as a normal density | 10^−1107.0 by the normal; the exact binomial is 10^−1079.9 | S2.7 |
| 28 | Myatt & Fisher eq. (2): "/(6n)" | wrong in the source | "/n"; Proposition 1 and eq. (3) as printed | S2.4 |
| 29 | R4: plurality-3, known shares | holds | Q ≈ two-way/√(p₁ + p₂) to 0.3% | S7.2 |
| 30 | R4: plurality-3, Dirichlet forecast (7.066/n at N = 1,000) | holds | continuous route within 5% at N = 1,000, 1% at 10,000 | S7.3 |
| 31 | R4: list PR "about M/N" | holds under condition | the forecast spans half a seat or more; otherwise 0 to 2.7 × M/N | S7.4 |
| 32 | R4: referendum thresholds, Q_no/Q_yes | holds | = t/(1 − t); averaging over N is legitimate | S7.5 |
| 33 | R4: quorum | structure only | quorum term can exceed the tie term (3.2 × in the stylised case) | S7.6 |
| 34 | R4: tiny electorates | holds | exact sum; approximation 8.1% high at N = 9 | S7.7, S1.4 |
| 35 | R4: runoff, IRV, STV | no calculation | structure only | S7.8 |
| 36 | R4: chamber, P(tip \| seat tied) | wrong label | it is the unconditional P(217); the conditional differs by 0.007 to 1.398 × in the stylised chamber | S4.4, S7.9 |
| 37 | M&H "1 in 89,252" | — | the ballot-weighted average event probability (2 × average p), one event, 95% factor 5.6 up and 39.5 down | S8.1–8.3 |
| 38 | Klarner 52 in 109,093 | — | the contest-average of P(margin 0 or 1) = 3 × contest-average p; not comparable to M&H's ballot weighting | S8.4 |
| 39 | Draft §2: "the expected outcome ... equals p × B" as the standard of review, B* = C/p | holds | p must be ours, not the event, or B* is half | S1.6 |

---

## 10. What this check did not do, and where two derivations stand side by side

- **Not read at source:** Baltz (2025); GSE's code; the published body of Mulligan & Hunter (paywalled; R2). Their verdicts above rest on R4's and R2's readings, as marked.
- **The Economist inputs are a back-test** of the 2020 model on 2016, read from the repository's copy of the README (diffed against the README by R1: 0 differences). The sd conversion se × 1.68/1.96 assumes a normal posterior and 95% intervals, as the README's columns say. n_i is the two-party vote; a reader who prefers all ballots scales p_state by the two-party share.
- **The chamber is stylised**; no seat forecasts were read.
- **Two derivations are given, not one, for:** the GSE convention (§3.4: words, or intent); the lay formula (§6.1: (F) or (Q)); the historical frequency (§8.2: event average, or half of it as a p average); the tie value where a legislature decides (§1.1 and §5.1: p is the same, the gain is not).
- **No scipy**: every special function is from the standard library or numpy; the Poisson intervals are by bisection on the exact cdf (S8).
- **Not a choice for the site.** Which convention to print, which tail, which lay form and which inputs are the maker's; this file gives the arithmetic each choice commits to.

## Files

`model/math/common.py` (definitions, exact sums, approximations), `s1_two_way.py`, `s2_conventions.py`, `s4_two_stage.py`, `s5_claims.py`, `s6_simple_mode.py`, `s7_systems.py`, `s8_history.py`, `run_all.sh` → `OUTPUT.txt`; `data/` (three CSVs with their sources and hashes in a header line) and `make_data.py` (rebuilds them from the fetched sources); `r4/` (R4's scripts verbatim, `r4/README.md`). There is no S3 script: §3's numbers are in S2.
