// The figures the first screen shows as real: each one already sourced in the model of record (model/MODEL.md §2, §4,
// §6) and checked there (model/MATH.md). Nothing here is new: every figure, its source and its mark are the model's.
// The page multiplies them by the reader's cost (B* = C × N, where p is 1 in N); that is the site's one computation
// on the first screen, and its inputs are these.

// The reader's cost, by default (model §6; design/DESIGN-SPEC.md §2.8).
export const COST = {
  minutes: 14,          // the median time at the polling place, 2016
  minutesMean: 19,      // the mean (19.13 in the paper's Table A.1)
  wage: 38.0,           // dollars an hour, average hourly earnings of private employees, October 2026, preliminary
  sources: [
    { what: '14 minutes (median) and 19 (mean) at the polling place, 2016', who: 'Chen, Haggag, Pope and Rohla', where: 'arXiv 1909.00024 (v2), p. 9 and Table A.1', note: 'Smartphone location data on 154,489 likely voters: time within 60 metres of the polling place, waiting and voting. It leaves out travel, registering and becoming informed.' },
    { what: '$38.00 an hour', who: 'Bureau of Labor Statistics', where: 'series CES0500000003, average hourly earnings of all employees, total private, October 2026, preliminary; read through its public data service', note: 'Valuing your time at the average wage is a convention (Gibson et al.); set your own.' },
  ],
};
export const costOf = (minutes, wage) => (minutes / 60) * wage;

// Populations for the reading "to each person". The Census Bureau's figures come with the data stage (D1, D2); until
// then these are samples, and the page says so wherever they are used.
const US_SAMPLE = { value: 300e6, of: 'the United States', sample: true };

// The contests with a real figure for p (or, for the town race, a stylised one the model computed), in order of N.
// `N`: p is 1 in N. `event`: the chance the count without the ballot lands within one vote, twice p (law 2b).
export const ANCHORS = [
  {
    id: 'town', level: 'local', N: 468,
    name: 'A town race of 2,000 voters', short: 'Town race, 2,000 voters', when: 'stylised',
    mark: 'Stylised, not a real race.',
    src: 'A forecast of 52–48 with a 4-point spread, summed exactly by the model (model/MATH.md §6.2; model/math/OUTPUT.txt).',
    pop: { value: 4000, of: 'the town', sample: true },
  },
  {
    id: 'house', level: 'house', N: 180000,
    name: 'A U.S. House race, on average', short: 'U.S. House, average', when: '1898–1992',
    mark: 'An average over 16,577 races, and an upper figure.',
    src: 'Mulligan and Hunter, "The Empirical Frequency of a Pivotal Vote", Public Choice 116 (2003): one House race in 16,577 from 1898 to 1992 was decided by one vote on the official count (New York\'s 36th, 1910; a later count made it six). As a chance per ballot, about 1 in 180,000 (model/MATH.md §8.2); the record allows anything from about 1 in 32,000 to 1 in 7 million.',
    pop: { value: 700000, of: 'a district', sample: true },
  },
  {
    id: 'close', level: 'president', N: 1e7,
    name: 'President, in New Mexico, Virginia, New Hampshire or Colorado', short: 'President, closest states', when: '2008',
    mark: null,
    src: 'Gelman, Silver and Edlin, "What is the probability your vote will make a difference?", Economic Inquiry 50(2), 2012, p. 321: "an approximate 1 in 10 million chance of determining the national election outcome", from a forecast made before the election. If the authors meant an exact tie, the chance is half this and the stakes double (model §4).',
    pop: US_SAMPLE,
  },
  {
    id: 'avg', level: 'president', N: 6e7,
    name: 'President, for the average voter', short: 'President, average voter', when: '2008',
    mark: null,
    src: 'Gelman, Silver and Edlin, Economic Inquiry 50(2), 2012, p. 321: "On average, a voter in America had a 1 in 60 million chance of being decisive in the presidential election."',
    pop: US_SAMPLE,
  },
  {
    id: 'safe', level: 'president', N: 1e9,
    name: 'President, in New York, California or Texas', short: 'President, safest states', when: '2008',
    mark: null,
    src: 'Gelman, Silver and Edlin, Economic Inquiry 50(2), 2012: about 1 in a billion in New York, California and Texas, from the same forecast.',
    pop: US_SAMPLE,
  },
];
export const anchor = id => ANCHORS.find(a => a.id === id);

// The words of the tie and the event (law 2b; design/DESIGN-SPEC.md §2.6).
export const TIE = 'A tie counts as half: a lot would have gone your way half the time anyway.';

// The levels of contest, top of the ballot to the bottom (design/DESIGN-SPEC.md §2.2).
export const LEVELS = [
  { id: 'president', name: 'President, by state' },
  { id: 'senate', name: 'U.S. Senate' },
  { id: 'governor', name: 'Governor' },
  { id: 'house', name: 'U.S. House' },
  { id: 'state', name: 'State legislature' },
  { id: 'local', name: 'Local' },
];
