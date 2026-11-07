// The figures the first screen shows: the reader's cost from its sources (model §6), and every contest, the lead and
// the named figures from data/, by src/data/build-field.mjs. The page multiplies each N by the reader's cost
// (B* = C × N, where p is 1 in N); that is the site's one computation on the first screen, and its inputs are these.
import FIELD from './field.json';

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

// The contests, the lead and the named figures, built from data/ by src/data/build-field.mjs (run it again after
// data/ changes). Every figure is the record's.
export { FIELD };
export const UNIT = FIELD.unit;
export const TOTAL = FIELD.total;
export const YEARS = FIELD.years;

// The named figures, in order of N (law 1a: the lowest first), all of 2024: the state with the highest chance, which
// leads (DESIGN-SPEC §7.2), the average voter and the state with the lowest chance beside it, and each level's lowest.
// `pop` is null where the data give no population yet; `lean` is "high" or "low" where the route's back-test leans
// that way (p.note).
export const ANCHORS = FIELD.cases;
export const anchor = id => ANCHORS.find(a => a.id === id);

// The words of the tie and the event (law 2b; design/DESIGN-SPEC.md §2.6).
export const TIE = 'A tie counts as half: a lot would have gone your way half the time anyway.';

// The levels of contest, top of the ballot to the bottom (design/DESIGN-SPEC.md §2.2). Local races and measures
// wait for M2's last check (the orchestrator, 09:26).
export const LEVELS = FIELD.levels.map(({ id, name, count, withPop, avgCount, years, lean }) => ({ id, name, count, withPop, avgCount, years, lean }));
