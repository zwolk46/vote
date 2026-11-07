// Candidate A, "Every contest on one ruler" (design/DESIGN-SPEC.md §5): the scale first. The lead figure and its
// working; the reader's cost and the chance, each opening to its sources; the two readings beside the figure; then the
// ruler of dollars with every contest a dot, in rows by level, the reader's cost a line through them, the named
// figures ringed; and the named figures as a list in order of their stakes, lowest first (law 1a), which is also how
// a contest is chosen without aiming at a dot.
import { useState } from 'preact/hooks';
import { ANCHORS, anchor, TOTAL, YEARS, UNIT } from '../data/real.js';
import { money } from '../lib/format.js';
import { useMedia, DESKTOP } from '../lib/media.js';
import { LeadFigure, CostRow, ChanceRow, ReadingSeg, ONE_Q, bstar, whenOf, sharedBy, SOURCES } from '../components/Lead.jsx';
import { Field, RECORD_KEY, leanKey } from '../components/Field.jsx';
import { Boundary } from '../components/Boundary.jsx';
import { Legend } from '../components/Legend.jsx';
import './ruler.css';

// The field's key: each mark as the field draws it (Legend.jsx)
const FIELD_KEY = [['dot', `= ${UNIT} contests`], ...RECORD_KEY, ['ring', 'a named figure'], ['line', 'your cost']];

export function Ruler({ C, minutes, wage, setCost, reading, setReading }) {
  const [sel, setSel] = useState('most');
  // In the reading "to each person", a figure the data give no population for has no place (its dots fade, and so
  // does it): the lead is then the highest chance's, and the reader's own choice comes back with the reading "to you"
  const per = reading === 'person', off = x => per && !x.pop;
  const a = off(anchor(sel)) ? anchor('most') : anchor(sel);
  const desk = useMedia(DESKTOP);
  return (
    <main class="page ra">
      <section class="ra-lead" aria-labelledby="ra-h">
        <h1 id="ra-h" data-sentence>How much would the outcome have to be worth for one vote to pay?</h1>
        <p class="contest"><span class="n">{a.name}</span><br /><span class="w">{whenOf(a)}</span></p>
        <LeadFigure a={a} C={C} reading={reading} />
        <ReadingSeg reading={reading} setReading={setReading} />
        <div class="key">
          <CostRow minutes={minutes} wage={wage} setCost={setCost} />
          <ChanceRow a={a} />
        </div>
        <p class="oneq" data-sentence>{ONE_Q}</p>
      </section>
      <section class="ra-field" aria-labelledby="ra-f">
        <div class="ra-fh"><h2 id="ra-f">Every contest</h2><span class="src num">{TOTAL.toLocaleString('en-US')} contests, {YEARS[0]}–{YEARS[1]}</span></div>
        <Legend items={FIELD_KEY} />
        <Boundary what="The field of contests" fallback={() => <p class="muted">The field could not be drawn.</p>}>
          <Field C={C} reading={reading} sel={a.id} onSel={setSel} desk={desk} />
        </Boundary>
      </section>
      <section class="ra-list" aria-labelledby="ra-l">
        <h2 id="ra-l" class="vh">The named figures</h2>
        <ul class="clist">
          {ANCHORS.map(x => (
            <li key={x.id} class={off(x) ? 'off' : null}><button type="button" aria-pressed={x.id === a.id ? 'true' : 'false'} disabled={off(x)} onClick={() => setSel(x.id)}>
              <span class="n">{x.short}</span>
              <span class="f">{off(x) ? '' : money(bstar(x, C, reading))}{x.lean && !off(x) ? <span class={`lg lg-lean${x.lean === 'low' ? ' low' : ''}`} role="img" aria-label={leanKey(x.lean)} /> : null}</span>
              <span class="w">{whenOf(x)}{per && x.pop ? `; ${sharedBy(x)}` : ''}</span>
            </button></li>
          ))}
        </ul>
        <p class="src" data-sentence>{SOURCES}</p>
      </section>
    </main>
  );
}
