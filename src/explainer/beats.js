// The explainer's content: the nine ideas of brief X2 in its order, each as one or more beats. A beat is a state of one
// picture and the few words that name what the reader is looking at (the maker, 11-07 04:32: the picture carries the
// idea; words name, they do not explain). Every figure is real or marked (law 8), and each beat names its source.
//
// The model's own illustrations are exact sums by the model's code (model/math/common.py, normalmix_pmf and
// p_from_pmf: a forecast of the share as a normal, the count binomial on it), run 2026-11-07 for this page.
// The town race is the model's stylised example (model §2). The presidency of 2008 is Gelman, Silver and Edlin (2012);
// the two stages are D1's figures for Pennsylvania in 2024 under the model's own forecast (data/president/2024.json).
import { COST } from '../data/real.js';

export const C0 = (COST.minutes / 60) * COST.wage;   // $8.87

export const SRC = {
  town: 'The town race is the model’s stylised example: 2,000 voters, a forecast of 52–48 give or take 4 points; the chance your ballot changes who wins is 1 in 468 (model §2).',
  rule: 'Your ballot changes who wins only when everyone else’s votes leave a tie or your side one short. A tie goes to a lot, which your side would have won half the time anyway; so each of the two counts is half a change, and the chance your ballot changes who wins is half the chance of the two counts (model §3).',
  model: 'The model’s own illustration: exact sums by its code (model/math/common.py), the forecast a normal curve of your side’s share. The curve is the chance of each exact count; at 50–50 it is the chance of a tie or one short, and half of that is the chance your ballot changes who wins.',
  gse: 'The closest states of 2008: about 1 in 10 million (Gelman, Silver and Edlin, “What is the probability your vote will make a difference?”, Economic Inquiry 50(2), 2012).',
  pa: 'Pennsylvania, 2024, under the model’s own forecast: your ballot changes the state’s winner 1 in 1,396,136; given that, the state’s electoral votes decide the College 18.6% of the time; both, 1 in 7,499,626 (data/president/2024.json).',
  cost: 'Your cost of voting: 14 minutes at the polls (the median, Chen, Haggag, Pope and Rohla, 2016 data) at $38.00 an hour (BLS, October 2026, preliminary): $8.87 (model §6). The least the result must be worth to you is your cost × N, where the chance is 1 in N (model §2).',
  worth: 'What the result is worth to you is yours to say; $1,000 and $10,000 are examples. The cost and the chances are the model’s (model §2).',
  pop: 'Counting what the result is worth to each person it touches: the least it must be worth to each is your cost × N ÷ the people. 300 million is a round figure for the country (model §5).',
  ballot: 'An example. The presidency, closest states, 2008: 1 in 10 million (Gelman, Silver and Edlin, 2012). A House race at the average of 1898–1992: 1 in 180,000 (Mulligan and Hunter, Public Choice, 2003). The town race: 1 in 468 (stylised). What each result is worth to you, $50 million, $400,000 and $1,000, is an example. Each race repays what it is worth to you ÷ N of each trip: $5.00, $2.22 and $2.14, together $9.36, more than the trip’s $8.87; the shares add (law 2c).',
};

// p for each forecast the curve shows (1 in N), exact
export const CURVE = {
  base: { n: 2000, mu: 0.52, sd: 0.04, N: 468 },
  n20k: { n: 20000, mu: 0.52, sd: 0.04, N: 4558 },
  n200k: { n: 200000, mu: 0.52, sd: 0.04, N: 45460 },
  mu56: { n: 2000, mu: 0.56, sd: 0.04, N: 1183 },
  mu60: { n: 2000, mu: 0.60, sd: 0.04, N: 7563 },
  sd8: { n: 2000, mu: 0.52, sd: 0.08, N: 836 },
};

export const PA = { state: 1396136, W: 0.18616, N: 7499626 };
export const TOWN = { N: 468, voters: 2000 };
export const CLOSE08 = 10e6;
export const HOUSE = 180000;
export const PEOPLE = 300e6;
export const WORTH = { lo: 1000, hi: 10000 };

// The beats, in order. `scene` names the picture and `st` its state. `head` orients (a heading); `fig` is the beat's one
// figure, unless the picture carries it on its mark (`figIn`); `sub` names what is shown; `key` is the picture's key of
// marks. `src` points into SRC, for the fold.
export const BEATS = [
  { id: 'worlds', idea: 1, scene: 'worlds', st: { k: 0 }, head: 'Your ballot, counted and not', fig: 'Same winner', sub: 'a town race of 2,000 voters (stylised)', key: [['yours', 'your side'], ['theirs', 'the other side'], ['you', 'your ballot']], src: 'town' },
  { id: 'worlds2', idea: 1, scene: 'worlds', st: { k: 1 }, head: 'A closer run of the same race', fig: 'Different winners', sub: 'your ballot changes who wins', key: [['yours', 'your side'], ['theirs', 'the other side'], ['you', 'your ballot']], src: 'town' },
  { id: 'margins', idea: 2, scene: 'margins', st: { hl: 1, join: 0 }, head: 'Where one ballot changes who wins', fig: 'A tie, or one vote short', key: [['yours', 'your side wins'], ['theirs', 'the other side wins'], ['tie', 'a tie: by lot']], src: 'rule' },
  { id: 'coin', idea: 3, scene: 'margins', st: { hl: 1, join: 1 }, head: 'A tie goes to a lot', fig: 'Half + half', sub: 'one change', key: [['yours', 'your side wins'], ['theirs', 'the other side wins'], ['tie', 'a tie: by lot'], ['change', 'what your ballot changes']], src: 'rule' },
  { id: 'curve', idea: 4, scene: 'curve', st: CURVE.base, figIn: '1 in 468', head: 'How likely a tie is', sub: '2,000 voters · forecast 52–48, give or take 4', key: [['bar', 'a tie, or one short'], ['barfill', 'your ballot changes who wins']], src: 'town' },
  { id: 'crowd1', idea: 4, scene: 'curve', st: CURVE.n20k, figIn: '1 in 4,558', head: 'More voters', sub: '20,000 voters', key: [['bar', 'a tie, or one short'], ['barfill', 'your ballot changes who wins']], src: 'model' },
  { id: 'crowd2', idea: 4, scene: 'curve', st: CURVE.n200k, figIn: '1 in 45,460', head: 'More voters', sub: '200,000 voters', key: [['bar', 'a tie, or one short'], ['barfill', 'your ballot changes who wins']], src: 'model' },
  { id: 'off1', idea: 4, scene: 'curve', st: CURVE.mu56, figIn: '1 in 1,183', head: 'Further from even', sub: '2,000 voters · forecast 56–44', key: [['bar', 'a tie, or one short'], ['barfill', 'your ballot changes who wins']], src: 'model' },
  { id: 'off2', idea: 4, scene: 'curve', st: CURVE.mu60, figIn: '1 in 7,563', head: 'Further from even', sub: 'forecast 60–40', key: [['bar', 'a tie, or one short'], ['barfill', 'your ballot changes who wins']], src: 'model' },
  { id: 'unsure', idea: 4, scene: 'curve', st: CURVE.sd8, figIn: '1 in 836', head: 'Less sure', sub: 'forecast 52–48, give or take 8', key: [['bar', 'a tie, or one short'], ['barfill', 'your ballot changes who wins']], src: 'model' },
  { id: 'town', idea: 5, scene: 'field', st: { ls: Math.log10(TOWN.N) / 2 }, head: 'Each dot, one run of the election', fig: '1 in 468', sub: 'the town race', key: [['run', 'one run of the election'], ['you', 'a run your ballot decides']], src: 'town' },
  { id: 'pres', idea: 5, scene: 'field', st: { ls: Math.log10(CLOSE08) / 2 }, head: 'The presidency, closest states, 2008', fig: '1 in 10 million', sub: 'millions of voters', key: [['run', 'one run of the election'], ['you', 'a run your ballot decides']], src: 'gse' },
  { id: 'stage1', idea: 6, scene: 'stages', st: { k: 0 }, head: 'The presidency, step one: your state', fig: '1 in 1.4 million', sub: 'your ballot changes Pennsylvania’s winner, 2024', key: [['run', 'one run'], ['you', 'your ballot changes the state’s winner']], src: 'pa' },
  { id: 'stage2', idea: 6, scene: 'stages', st: { k: 1 }, head: 'Step two: your state decides the College', fig: '19 in 100', sub: 'of those runs', key: [['youdot', 'the state decides the College'], ['theirs', 'it does not']], src: 'pa' },
  { id: 'stage3', idea: 6, scene: 'stages', st: { k: 2 }, head: 'Both steps', fig: '1 in 7.5 million', sub: 'Pennsylvania, 2024', key: [['run', 'one run'], ['you', 'your ballot decides the presidency']], src: 'pa' },
  { id: 'trips', idea: 7, scene: 'trips', st: { k: 0 }, head: 'A trip to vote in every run', fig: '468 × $8.87 = $4,150', sub: 'a trip: 14 minutes at the polls, at $38 an hour', key: [['trip', 'one trip to vote: $8.87'], ['you', 'the run your ballot decides']], src: 'cost' },
  { id: 'weighLo', idea: 7, scene: 'trips', st: { k: 1 }, head: 'Weighed against what the result is worth to you', fig: 'Does not pay', sub: 'worth $1,000 to you (an example)', key: [['trip', 'your trips'], ['you', 'the result: what it is worth to you']], src: 'worth' },
  { id: 'weighHi', idea: 7, scene: 'trips', st: { k: 2 }, head: 'Worth more than $4,150', fig: 'It pays', sub: 'worth $10,000 to you (an example)', key: [['trip', 'your trips'], ['you', 'the result: what it is worth to you']], src: 'worth' },
  { id: 'presW', idea: 7, scene: 'trips', st: { k: 3 }, head: 'The presidency: 10 million trips for one', fig: 'Does not pay', sub: '$89 million against the same $10,000 · closest states, 2008', key: [['trip', 'your trips'], ['you', 'the result: what it is worth to you']], src: 'gse' },
  { id: 'share', idea: 7, scene: 'trips', st: { k: 4 }, head: 'Counting what it is worth to everyone', fig: '30¢ each', sub: '$89 million ÷ 300 million people (a round figure)', key: [['trip', 'your trips'], ['person', 'a million people, each at 30¢']], src: 'pop' },
  { id: 'ruler', idea: 7, scene: 'trips', st: { k: 5 }, head: 'The least the result must be worth to you', fig: 'Your cost × N', sub: 'where the chance is 1 in N', key: [['youdot', 'your cost'], ['fig', 'your cost × N'], ['arrow', '× N']], src: 'cost' },
  { id: 'ballot1', idea: 8, scene: 'ballot', st: { n: 1 }, head: 'One trip votes in every race', fig: '$5.00 of the $8.87', sub: 'the presidency, worth $50 million to you (an example)', key: [['trip', 'one trip: $8.87'], ['pres', 'President: $50 million ÷ 10 million trips']], src: 'ballot' },
  { id: 'ballot2', idea: 8, scene: 'ballot', st: { n: 2 }, head: 'The House race too', fig: '$7.22 of the $8.87', sub: 'worth $400,000 to you (an example)', key: [['trip', 'one trip: $8.87'], ['pres', 'President'], ['house', 'House: $400,000 ÷ 180,000 trips']], src: 'ballot' },
  { id: 'ballot3', idea: 8, scene: 'ballot', st: { n: 3 }, head: 'And the town race', fig: 'It pays: $9.36', sub: 'worth $1,000 to you (an example); alone, none of the three pays', key: [['trip', 'one trip: $8.87'], ['pres', 'President'], ['house', 'House'], ['town', 'Town: $1,000 ÷ 468 trips']], src: 'ballot' },
];
