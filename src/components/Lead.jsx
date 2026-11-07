// The pieces every candidate's lead is made of (design/DESIGN-SPEC.md §2.1, §2.4 to §2.9): the lead figure with its
// working, the key of the two inputs (the reader's cost, the chance), each opening in place to its sources, the two
// readings, and the one question. One component each, so a standard set once holds on every candidate (TASTE, 11-05
// 20:35).
import { useEffect, useState } from 'preact/hooks';
import { money, moneyParts, oneIn, digits, count } from '../lib/format.js';
import { COST, TIE } from '../data/real.js';
import { useFold, FoldBody } from './Fold.jsx';
import { Seg } from './Seg.jsx';

export const bstar = (a, C, reading) => (reading === 'person' ? (C * a.N) / a.pop.value : C * a.N);

// The figure the page leads with, B*, in the display size, the unit word lighter; under it the working, so the
// multiplication is on the page and not only behind it (§2.4, the receipt).
export function LeadFigure({ a, C, reading, id }) {
  const v = bstar(a, C, reading);
  const [n, w] = moneyParts(v);
  const per = reading === 'person';
  return (
    <div class="lead" id={id}>
      <p class="lead-fig"><span>{n}{w ? <span class="w"> {w}</span> : null}</span><span class="to">{per ? `to each person in ${a.pop.of}` : 'to you'}</span></p>
      <p class="working">{per
        ? `${money(C * a.N)} ÷ ${count(a.pop.value)} people${a.pop.sample ? ' (a sample population)' : ''}`
        : `${money(C)} × ${digits(a.N)}`}</p>
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
      <div class="key-row"><span class="l">Your cost</span><button type="button" class="f fig-btn" {...f.btn} onClick={f.toggle}>{money(C)}</button></div>
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
        <p>{a.src}</p>
        <p>{TIE} The chance the count without you lands within one vote is twice this: {oneIn(a.N / 2)}.</p>
      </FoldBody>
    </>
  );
}

export function ReadingSeg({ reading, setReading, size = 'body' }) {
  return <Seg label="Whose stakes" size={size} options={[['you', 'To you'], ['person', 'To each person']]} value={reading} onChange={setReading} />;
}

export const ONE_Q = 'This weighs one vote’s effect on who wins against what it costs. Every other reason to vote is set aside.';
