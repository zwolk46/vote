// Candidate A, "Every contest on one ruler" (design/DESIGN-SPEC.md §5): the scale first. The lead figure and its
// working; the reader's cost and the chance, each opening to its sources; the two readings beside the figure; then the
// ruler of dollars with every contest a dot, in rows by level, the reader's cost a line through them, the named
// figures ringed; and the named figures as a list in order of their stakes, lowest first (law 1a), which is also how
// a contest is chosen without aiming at a dot.
import { useState } from 'preact/hooks';
import { ANCHORS, anchor } from '../data/real.js';
import { sampleTotal, UNIT } from '../data/sample.js';
import { money } from '../lib/format.js';
import { useMedia, DESKTOP } from '../lib/media.js';
import { LeadFigure, CostRow, ChanceRow, ReadingSeg, ONE_Q, bstar, whenOf, sharedBy } from '../components/Lead.jsx';
import { Field } from '../components/Field.jsx';
import { Boundary } from '../components/Boundary.jsx';
import { Legend } from '../components/Legend.jsx';
import './ruler.css';

export function Ruler({ C, minutes, wage, setCost, reading, setReading }) {
  const [sel, setSel] = useState('close');
  const a = anchor(sel);
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
        <div class="ra-fh"><h2 id="ra-f">Every contest</h2><span class="src num">{sampleTotal().toLocaleString('en-US')} sample contests</span></div>
        <Legend items={[['dot', `= ${UNIT} contests (samples)`], ['ring', 'a named figure'], ['line', 'your cost']]} />
        <Boundary what="The field of contests" fallback={() => <p class="muted">The field could not be drawn.</p>}>
          <Field C={C} reading={reading} sel={sel} onSel={setSel} desk={desk} />
        </Boundary>
      </section>
      <section class="ra-list" aria-labelledby="ra-l">
        <h2 id="ra-l" class="vh">The named figures</h2>
        <ul class="clist">
          {ANCHORS.map(x => (
            <li key={x.id}><button type="button" aria-pressed={x.id === sel ? 'true' : 'false'} onClick={() => setSel(x.id)}>
              <span class="n">{x.short}</span>
              <span class="f">{money(bstar(x, C, reading))}</span>
              <span class="w">{whenOf(x)}{reading === 'person' ? `; ${sharedBy(x)}` : ''}</span>
            </button></li>
          ))}
        </ul>
        <p class="src" data-sentence>Gelman, Silver and Edlin, Economic Inquiry, 2012 (the presidency, 2008). Mulligan and Hunter, Public Choice, 2003 (the House). Read 7 November 2026.</p>
      </section>
    </main>
  );
}
