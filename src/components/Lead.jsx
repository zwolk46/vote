// The pieces every candidate's lead is made of (design/DESIGN-SPEC.md §2.1, §2.4 to §2.9): the lead figure with its
// working, the key of the two inputs (the reader's cost, the chance), each opening in place to its sources, the two
// readings, and the one question. One component each, so a standard set once holds on every candidate (TASTE, 11-05
// 20:35).
import { useEffect, useState } from 'preact/hooks';
import { money, moneyParts, oneIn, digits, count } from '../lib/format.js';
import { COST, TIE } from '../data/real.js';
import { useFold, FoldBody } from './Fold.jsx';
import { Seg } from './Seg.jsx';
import { LeadRuler } from './LeadRuler.jsx';

// B*, or null in the reading "to each person" where the data give no population yet (none is filled in); the
// candidates then show no such figure (its mark fades, and the lead is another's)
export const bstar = (a, C, reading) => (reading === 'person' ? (a.pop ? (C * a.N) / a.pop.value : null) : C * a.N);

// Which election, and why this one is named: "2024 · the highest chance of any state", "2024 · the lowest of 34"
export const whenOf = a => `${a.when} · ${a.role}`;
// the people a per-person figure is shared among
// (nothing where the data give no population: its mark fades without words, the orchestrator 12:01, the maker 04:32)
export const sharedBy = a => (a.pop ? `shared by ${count(a.pop.value)} people in ${a.pop.of}` : '');
// A route's back-test, in the reader's words: the record's note, its "p" said as the chance, and what that does to
// the figure (p.note; data/congress/REPORT.md §5)
export const leanWords = a => {
  const s = (a.note || '').replace(/so p may be (high|low)$/, (_, d) => `so this chance may be too ${d}, and the figure too ${d === 'high' ? 'low' : 'high'}`);
  return s ? `${s[0].toUpperCase()}${s.slice(1)}.` : '';
};

// The figure the page leads with, B*, in the display size, the unit word lighter; under it what it is, in a label
// (every cold reader of 11-07 first took "$89 million to you" for a sum they would receive); the working as figures;
// and the working drawn, the cost carried to the figure by the odds (LeadRuler), which is what explains it.
// A figure with no population is never led with "to each person" (the candidates lead with another's), so that
// reading falls back to "to you" here only as a guard.
export function LeadFigure({ a, C, reading, id }) {
  const per = reading === 'person' && !!a.pop;
  reading = per ? 'person' : 'you';
  const [n, w] = moneyParts(bstar(a, C, reading));
  return (
    <div class="lead" id={id}>
      <p class="lead-fig"><span>{n}{w ? <span class="w"> {w}</span> : null}</span><span class="to">{per ? `the least the result must be worth to each person in ${a.pop.of}` : 'the least the result must be worth to you'}</span></p>
      <p class="working">{per ? `${money(C * a.N)} ÷ ${count(a.pop.value)} people` : `${money(C)} × ${digits(a.N)}`}</p>
      <LeadRuler a={a} C={C} reading={reading} />
    </div>
  );
}

// The reader's cost: a figure that opens to two fields and their product (§2.8). Any change moves every contest by
// the same factor (V2).
export function CostRow({ minutes, wage, setCost }) {
  const f = useFold();
  const C = (minutes / 60) * wage;
  const [m, setM] = useState(String(minutes)), [w, setW] = useState(wage.toFixed(2));
  useEffect(() => { setM(String(minutes)); setW(wage.toFixed(2)); }, [minutes, wage]);
  const commit = (mm, ww) => {
    const a = Math.min(600, Math.max(1, parseFloat(mm))), b = Math.min(1000, Math.max(0.5, parseFloat(ww)));
    if (Number.isFinite(a) && Number.isFinite(b)) setCost(a, b);
  };
  const changed = minutes !== COST.minutes || wage !== COST.wage;
  return (
    <>
      <div class="key-row"><span class="l">Your cost of voting<span class="sub">{minutes} minutes at the polls, at {money(wage)} an hour</span></span><button type="button" class="f fig-btn" {...f.btn} onClick={f.toggle}>{money(C)}</button></div>
      <FoldBody fold={f} cls="key-fold">
        <div class="cost-ed">
          <label>Minutes<input type="number" inputmode="decimal" min="1" max="600" step="1" value={m} onInput={e => setM(e.currentTarget.value)} onChange={e => commit(e.currentTarget.value, w)} /></label>
          <span class="op">×</span>
          <label>Dollars an hour<input type="number" inputmode="decimal" min="0.5" max="1000" step="0.5" value={w} onInput={e => setW(e.currentTarget.value)} onChange={e => commit(m, e.currentTarget.value)} /></label>
          <span class="op">=</span>
          <span class="res">{money(C)}</span>
          {changed ? <button type="button" class="reset" onClick={() => setCost(COST.minutes, COST.wage)}>Default</button> : null}
        </div>
        <p><span class="k">14 minutes</span> is the median time at the polling place in 2016, waiting and voting; the mean is 19 ({money(costOf(19))}). It leaves out travel. Chen, Haggag, Pope and Rohla, arXiv 1909.00024, from smartphone location data on 154,489 likely voters.</p>
        <p><span class="k">$38.00 an hour</span> is the average hourly earnings of private employees, October 2026, preliminary. Bureau of Labor Statistics, series CES0500000003. Valuing your time at the average wage is a convention; set your own.</p>
      </FoldBody>
    </>
  );
}
const costOf = min => (min / 60) * COST.wage;

// The chance: "1 in N", opening to its source, its mark, and the tie and the event named (law 2b; §2.6).
export function ChanceRow({ a }) {
  const f = useFold();
  useEffect(() => { if (f.open) f.toggle(); }, [a.id]);   // a fold belongs to the figure it opened from
  return (
    <>
      <div class="key-row"><span class="l">Chance your ballot changes who wins</span><button type="button" class="f fig-btn" {...f.btn} onClick={f.toggle}>{oneIn(a.N)}</button></div>
      <FoldBody fold={f} cls="key-fold">
        {a.mark ? <p><span class="k">{a.mark}</span></p> : null}
        {a.lean ? <p class="lean-p"><span class={`lg lg-lean${a.lean === 'low' ? ' low' : ''}`} aria-hidden="true" /> {leanWords(a)}</p> : null}
        <p>{a.src}</p>
        {a.pop ? <p>{`Population, for the reading "to each person": ${digits(a.pop.value)}, ${a.pop.of}; ${a.pop.src}.`}</p> : null}
        <p>{TIE} The chance the count without you lands within one vote is twice this: {oneIn(a.N / 2)}.</p>
      </FoldBody>
    </>
  );
}

export function ReadingSeg({ reading, setReading, size = 'body' }) {
  return <Seg fit label="Whose stakes" size={size} options={[['you', 'To you'], ['person', 'To each person']]} value={reading} onChange={setReading} />;
}

// Where the chances come from, in one line under the named figures; each figure's own sources open from its chance
export const SOURCES = 'Chances from this site’s model, or 538’s forecast where 538 published one, on the certified counts (the Federal Election Commission; the MIT Election Data and Science Lab; Cha, Kuriwaki and Snyder; Klarner). Populations from the Census Bureau. Read 7 November 2026.';

export const ONE_Q = 'Only the chance of changing who wins is weighed here. Every other reason to vote, like duty or having your say, is set aside.';
