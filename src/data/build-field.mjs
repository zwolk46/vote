// Builds src/data/field.json, the first screen's data, from the contests in data/ (data/README.md). Run it from the
// repository's root after data/ changes:  node src/data/build-field.mjs
//
// What it takes, and why (the orchestrator, 11-07 09:26 and 09:31):
// - Every contest with a chance (p > 0) at the levels M2 has checked: the presidency by state, the Senate, the House,
//   governors and both chambers of the state legislatures. Local races and measures wait for M2's last item. Breadth is
//   a goal of its own (the maker, 03:13), so every year the files hold is taken, not a sample of years.
// - A state legislative p is the district's own only where its forecast knows the district: p.forecast_scope
//   "district (class A)" or "(class B)". Class C is a chamber's average district, and the like-race routes (class,
//   boundary, runoff) an average of like races; both are kept in the field, marked, and never chosen as a case.
//   *Reason:* law 8; a figure shown for one district must be that district's (09:31).
// - The lead is the state with the highest chance in 2024 (design/DESIGN-SPEC.md §7.2, read with the orchestrator's
//   11:05 correction: Nevada had the highest chance, not the narrowest result, so it is named by its chance), and beside
//   it the average voter and the state with the lowest chance. A state is a state: not DC, not a district of Maine's or
//   Nebraska's.
// - The lowest-B* case of each level is that of 2024, the lead's own year, among the contests' own p (the orchestrator,
//   11:05: the reader compares like with like, and the history stays in the dots). It is chosen at the default cost,
//   $8.87, but B* = C × N is C times the same N for every contest, so the lowest B* is the highest p, at any cost.
// - Populations for the reading "to each person" only where D1 and D2 give them: the nation for the presidency
//   (population_nation), the contest's own population elsewhere, a state legislative district's from
//   data/population/ (2022 and 2024); none is filled in.
// - A route's back-test leaning one way (p.note: "so p may be high", "so p may be low") is carried as `lean`, so the
//   page can draw it (the maker, 04:32: visuals over prose); except the governors' and the Senate's (LEAN_OUT).
//
// The field is written as groups of UNIT contests, each at its group's middle (median) N, so the page draws whole
// dots that can be seen and moved (the midterms swarms) and the file stays small. Groups never mix a contest's own p
// with an average's, or a contest with a population with one without.
import { readFileSync, readdirSync, writeFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { execSync } from 'node:child_process';

const ROOT = process.cwd(), DATA = join(ROOT, 'data');
if (!existsSync(join(DATA, 'README.md'))) throw new Error('run from the repository root');
const UNIT = 10;
const C = (14 / 60) * 38;   // the default cost (model §6): 14 minutes at $38.00 an hour, $8.87

const read = f => JSON.parse(readFileSync(f, 'utf8'));
const files = dir => (existsSync(dir) ? readdirSync(dir).filter(f => f.endsWith('.json')).sort().map(f => join(dir, f)) : []);
const LEVELS = [
  { id: 'president', name: 'President, by state and year', dirs: ['president'] },
  { id: 'senate', name: 'U.S. Senate', dirs: ['senate'] },
  { id: 'governor', name: 'Governor', dirs: ['governor'] },
  { id: 'house', name: 'U.S. House', dirs: ['house'] },
  { id: 'state', name: 'State legislature', dirs: ['state-upper', 'state-lower'], nested: true },
];

// state codes to names, from the presidency's own place names
const STATES = {};
for (const f of files(join(DATA, 'president'))) for (const c of read(f).contests || []) if (c.place && !c.place.district && c.place.name) STATES[c.place.state] = c.place.name;

// The orchestrator's ruling of 11:05: a lean note stands only where the share test and the vote-count test of the same
// back-test lean the same way (each counted only with 5 or more expected). For governors they disagree (17 against 14.9
// within 1 point; 4 against 8.8 within 10,000 votes), and on M2's numbers (the orchestrator, 11:16) so do the Senate's:
// both notes are coming out of the data, and until they do they are not drawn. The House's note stands, and is drawn as
// the data carry it (and the statewide measures', when they are shown).
const LEAN_OUT = new Set(['governor', 'senate']);
const leanOf = (level, p) => { if (LEAN_OUT.has(level)) return null; const m = /so p may be (high|low)/.exec(p.note || ''); return m ? m[1] : null; };
const ownOf = (level, p) => (level !== 'state' ? true : /^district/.test(p.forecast_scope || ''));
// A state legislative district's population is D2's (data/population/state-legislative-<year>.json, the Census
// Bureau's 2020 count on each cycle's own lines, keyed by D3's contest id; nothing apportioned): 2022 and 2024. A
// contest it gives none has none here either.
const SLD = {};
for (const f of files(join(DATA, 'population'))) {
  const m = /state-legislative-(\d{4})\.json$/.exec(f); if (!m) continue;
  const d = read(f);
  for (const [id, r] of Object.entries(d.contests || {})) if (r.population?.value > 0) SLD[id] = { ...r.population, source: d.sources?.[r.population.source] || r.population.source, note: r.note || null };
}
const popOf = (level, c) => (level === 'president' ? c.population_nation : level === 'state' ? SLD[c.id] : c.population) || null;

const levels = [], all = {};
for (const L of LEVELS) {
  const rows = [];
  for (const d of L.dirs) {
    const fs = L.nested ? readdirSync(join(DATA, d)).sort().flatMap(y => files(join(DATA, d, y))) : files(join(DATA, d));
    for (const f of fs) {
      const doc = read(f);
      for (const c of doc.contests || []) {
        const p = c.p || {};
        if (!(p.value > 0)) continue;
        const pop = popOf(L.id, c);
        rows.push({ c, doc, sub: d, N: 1 / p.value, lN: -Math.log10(p.value), pop: pop && pop.value > 0 ? pop : null, own: ownOf(L.id, p), lean: leanOf(L.id, p) });
      }
    }
  }
  all[L.id] = rows;
  const parts = [[true, true], [true, false], [false, true], [false, false]].map(([own, hasPop]) => rows.filter(r => r.own === own && !!r.pop === hasPop).sort((a, b) => a.lN - b.lN));
  const med = a => { a = [...a].sort((x, y) => x - y); const k = a.length >> 1; return a.length % 2 ? a[k] : (a[k - 1] + a[k]) / 2; };
  const r2 = x => Math.round(x * 100) / 100;
  const groups = [];
  parts.forEach((part, pi) => {
    for (let i = 0; i < part.length; i += UNIT) {
      const m = part.slice(i, i + UNIT);
      groups.push({ you: r2(med(m.map(r => r.lN))), per: m[0].pop ? r2(med(m.map(r => r.lN - Math.log10(r.pop.value)))) : null, avg: pi >= 2 ? 1 : 0, size: m.length });
    }
  });
  // the own contests first, so in each bin they stack from the base and the averages above them
  const own = groups.filter(g => !g.avg).sort((a, b) => a.you - b.you), avg = groups.filter(g => g.avg).sort((a, b) => a.you - b.you);
  const gs = [...own, ...avg];
  const leans = rows.filter(r => r.lean);
  const years = rows.map(r => r.c.year);
  levels.push({
    id: L.id, name: L.name, count: rows.length, withPop: rows.filter(r => r.pop).length, avgCount: rows.filter(r => !r.own).length,
    years: [Math.min(...years), Math.max(...years)],
    // how many of the row's contests carry each way of leaning, in all and among those with a population
    lean: leans.length ? Object.fromEntries(['high', 'low'].map(d => [d, { n: leans.filter(r => r.lean === d).length, withPop: leans.filter(r => r.lean === d && r.pop).length }]).filter(([, v]) => v.n)) : null,
    g: { you: gs.map(g => g.you), per: gs.map(g => g.per), avg: gs.map(g => g.avg), size: gs.map(g => g.size) },
  });
}

// The words of a case, from its record. Every figure is the record's; the words name where each comes from.
const srcName = (doc, s) => (typeof s === 'string' ? doc.sources?.[s]?.name || s : s?.name || null);
const shortSrc = n => (n || '')
  .replace(/^Federal Election Commission, Federal Elections (\d{4}).*$/, "the Federal Election Commission's official results, $1")
  .replace(/^MIT Election Data and Science Lab, ([^,]+),.*$/, "the MIT Election Data and Science Lab's $1")
  .replace(/^Cha, Kuriwaki and Snyder, Candidates in American General Elections.*$/, 'Cha, Kuriwaki and Snyder, Candidates in American General Elections')
  .replace(/^Carl Klarner, State Legislative Election Returns, 1967-2022.*$/, "Carl Klarner's State Legislative Election Returns, 1967–2022")
  .replace(/^U\.S\. Census Bureau, 2020 Census (\d+)th Congressional District Summary File.*$/, "the Census Bureau's 2020 Census count on the district's lines (its $1th Congressional District Summary File)")
  .replace(/^U\.S\. Census Bureau, (.*)$/, 'the Census Bureau, $1');
const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
const day = iso => { const [y, m, d] = iso.split('-').map(Number); return `${d} ${MONTHS[m - 1]} ${y}`; };
const ofName = (level, c, pop) => (pop.of === 'nation' ? 'the United States' : pop.of === 'state' ? STATES[c.place.state] || c.place.state : 'the district');
function forecastWords(r) {
  const p = r.c.p, u = p.under || '';
  const f = (r.c.forecasts || [])[0] || {};
  if (/^538/.test(u)) return `Forecast: 538's${f.by === '538' && f.version && f.version !== 'only' ? ` (its ${f.version} version)` : ''}${f.by === '538' && f.as_of ? ` of ${day(f.as_of)}` : ''}, its spread read from the chance it gave; this site's own model stands beside it as the check`;
  if (r.c.level === 'president') return `Forecast: this site's own model, built only from what was known before the election${f.source?.note ? ` (${f.source.note})` : ''}`;
  if (/^the model's own \(D3/.test(u)) return `Forecast: this site's own model, from this district's last result, whether its member ran again and the chamber's lean, fitted on earlier years only`;
  return `Forecast: this site's own model, built only from what was known before the election (${u})`;
}
function placeWords(r) {
  const c = r.c, st = STATES[c.place.state] || c.place.state;
  if (r.sub === 'state-lower' || r.sub === 'state-upper') {
    const ch = r.sub === 'state-lower' ? 'house' : 'senate';
    return { name: `${st} state ${ch}, district ${c.place.district}`, short: `${st} state ${ch} ${c.place.district}`, place: `${st} ${ch} district ${c.place.district}` };
  }
  if (c.level === 'house') return { name: `U.S. House, ${c.place.name}`, short: `U.S. House, ${c.place.name.replace(/ (\d+)$/, '-$1')}`, place: c.place.name.replace(/ (\d+)$/, '-$1') };
  if (c.level === 'senate') return { name: `U.S. Senate, ${c.place.name}`, short: `Senate, ${c.place.name}`, place: c.place.name };
  if (c.level === 'governor') return { name: `Governor, ${c.place.name}`, short: `Governor, ${c.place.name}`, place: c.place.name };
  return { name: `President, in ${c.place.name}`, short: `President, ${c.place.name}`, place: c.place.name };
}
function caseOf(id, level, r, extra = {}) {
  const c = r.c, pw = placeWords(r);
  const res = c.result || {}, tp = c.two_party || {};
  const pop = r.pop ? { value: r.pop.value, of: ofName(level, c, r.pop), src: shortSrc(r.pop.source?.name) } : null;
  return {
    id, contest: c.id, level, year: c.year, N: Math.round(r.N), ...pw,
    when: String(c.year),
    votes: tp.votes || null,
    src: `${forecastWords(r)}. The count: ${shortSrc(srcName(r.doc, res.source)) || 'the record'}.`,
    pop, lean: r.lean, note: r.lean ? c.p.note : null,
    ...extra,
  };
}
const lowest = rows => rows.reduce((a, b) => (b.N < a.N ? b : a));
// the states of 2024: not DC, not a district (Maine's and Nebraska's are counted on their own)
const s24 = all.president.filter(r => r.c.year === 2024 && !r.c.place.district && r.c.place.state !== 'DC');
const lead = lowest(s24);
const least = s24.reduce((a, b) => (b.N > a.N ? b : a));
const doc24 = read(join(DATA, 'president', '2024.json'));
const cases = [
  caseOf('most', 'president', lead, { role: 'the highest chance of any state' }),
  { id: 'avg', contest: null, level: 'president', year: 2024, N: doc24.summary.one_in, name: 'President, for the average voter', short: 'President, average voter', place: 'the average voter', when: '2024', votes: null,
    src: `The chance of the average voter of 2024: each state's chance, weighted by its two-party vote, averaged over the ${doc24.summary.states_with_p} states with a chance. Forecast: this site's own model, as for each state.`,
    pop: { value: lead.c.population_nation.value, of: 'the United States', src: shortSrc(lead.c.population_nation.source?.name) }, lean: null, note: null, role: 'the average over the states',
    mark: 'An average over the states, not one contest.' },
  caseOf('least', 'president', least, { role: 'the lowest chance of any state' }),
];
for (const L of LEVELS) {
  if (L.id === 'president') continue;   // the presidency's highest chance of 2024 is the lead
  // the pool: this level's contests of 2024 whose p is their own
  const pool = all[L.id].filter(x => x.own && x.c.year === 2024);
  if (!pool.length) continue;
  const r = lowest(pool);
  cases.push(caseOf(`low-${L.id}`, L.id, r, { role: `the lowest of ${pool.length.toLocaleString('en-US')}${L.id === 'state' ? ' with a district forecast' : ''}` }));
}
cases.sort((a, b) => a.N - b.N);

// the nation's population each presidential year (D1's population_nation), for a page that names the country's
const nation = {};
for (const f of files(join(DATA, 'president'))) { const d = read(f), pn = (d.contests || []).find(c => c.population_nation)?.population_nation; if (pn) nation[d.year] = { value: pn.value, src: shortSrc(pn.source?.name) }; }

let commit = null;
try { commit = execSync('git rev-parse --short HEAD', { cwd: ROOT }).toString().trim(); } catch { /* not a repository */ }
const out = {
  about: 'The first screen\'s data, written by src/data/build-field.mjs from data/; do not edit by hand. Each field dot is a group of `unit` contests at its group\'s median N (p is 1 in N). `per` is log10 of N ÷ population, null where the data give no population. `avg` marks a p that is an average (a state legislative class C, a chamber\'s average district; or like past races), never the district\'s own.',
  built_from: commit ? `data/ at ${commit}` : 'data/', unit: UNIT, C: Math.round(C * 100) / 100,
  total: levels.reduce((s, l) => s + l.count, 0),
  years: [Math.min(...levels.map(l => l.years[0])), Math.max(...levels.map(l => l.years[1]))],
  levels, cases, nation,
};
writeFileSync(join(ROOT, 'src', 'data', 'field.json'), JSON.stringify(out));
console.log(`field.json: ${out.total} contests, ${levels.map(l => `${l.id} ${l.count} (${l.g.you.length} dots, ${l.withPop} with a population, ${l.avgCount} averages)`).join('; ')}`);
for (const c of cases) console.log(`  ${c.id}: ${c.name}, ${c.when}: 1 in ${c.N.toLocaleString('en-US')}, B* $${Math.round(C * c.N).toLocaleString('en-US')}${c.pop ? `, ${c.pop.of} ${c.pop.value.toLocaleString('en-US')}` : ', no population'}${c.lean ? `, may be ${c.lean}` : ''}`);
