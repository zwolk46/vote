// Candidate C, "One in N, made visible" (design/DESIGN-SPEC.md §5): the chance first. A field of dots, one for each
// time the election might be run; the ringed one is the time your ballot changes who wins. Scrolling moves the field
// from the lead contest (1 in 10 million) in to a town race, where each of 468 dots can be seen, and out again through
// the House, the closest states, the average voter and the safest states (1 in a billion); at each stop the figure is
// your cost × N. The earlier fields stay as outlined squares inside the larger. Breadth is a count at each stop: how
// many of the sample contests have a better chance than this.
//
// Motion (§4, V6): the field's scale follows the scroll frame by frame, with no duration of its own; under reduced
// motion each stop is drawn still and the field changes at once between them. No idle motion.
import { useEffect, useLayoutEffect, useMemo, useRef, useState } from 'preact/hooks';
import { anchor, TIE } from '../data/real.js';
import { sampleField, sampleTotal } from '../data/sample.js';
import { money, moneyParts, oneIn, count, digits } from '../lib/format.js';
import { useMedia, DESKTOP, useColours } from '../lib/media.js';
import { reducedMotion } from '../lib/motion.js';
import { LeadFigure, CostRow, ChanceRow, ReadingSeg, ONE_Q, bstar } from '../components/Lead.jsx';
import { Boundary } from '../components/Boundary.jsx';
import { useFold, FoldBody } from '../components/Fold.jsx';
import './onein.css';

const STOPS = ['town', 'house', 'close', 'avg', 'safe'];
const LEAD = 'close';
const CAP = {
  town: '468 runs of a town race of 2,000 voters (stylised)',
  house: '180,000 runs of a House race, on average',
  close: '10 million runs of the presidential election, in the closest states',
  avg: '60 million runs, for the average voter',
  safe: 'A billion runs, in the safest states',
};
const half = n => Math.log10(n) / 2;   // log10 of the side of a square of n dots

// How many sample contests have a better chance than 1 in N (their N is smaller), and the bands for the last step.
function useBreadth() {
  return useMemo(() => {
    const all = []; for (const l of Object.values(sampleField())) for (const x of l.logN) all.push(x);
    all.sort((a, b) => a - b);
    const below = lx => { let lo = 0, hi = all.length; while (lo < hi) { const m = (lo + hi) >> 1; if (all[m] < lx) lo = m + 1; else hi = m; } return lo; };
    return { below, total: all.length };
  }, []);
}

export function OneInN({ C, minutes, wage, setCost, reading, setReading }) {
  const desk = useMedia(DESKTOP);
  const lead = anchor(LEAD);
  const br = useBreadth();
  const steps = useRef([]);
  const leadRef = useRef(null);
  return (
    <main class="page oc">
      <div class="oc-text">
        <section class="oc-intro" aria-labelledby="oc-h">
          <h1 id="oc-h">How often does one ballot change who wins?</h1>
          {desk ? <p class="oc-say">Picture the same election run again and again, the same voters, each time a little different. In a few of those runs the count without you lands where your ballot decides it. The chance is how rare those runs are.</p> : null}
        </section>
        {desk ? null : <div class="oc-stage-slot"><Stage steps={steps} leadRef={leadRef} desk={desk} /></div>}
        {desk ? null : <p class="oc-say">Picture the same election run again and again, the same voters, each time a little different. In a few of those runs the count without you lands where your ballot decides it. The chance is how rare those runs are.</p>}
        <section class="oc-lead" ref={leadRef} aria-labelledby="oc-l">
          <h2 id="oc-l" class="vh">The lead contest</h2>
          <p class="contest"><span class="n">{lead.name}</span><br /><span class="w">{lead.when}</span></p>
          <LeadFigure a={lead} C={C} reading={reading} />
          <ReadingSeg reading={reading} setReading={setReading} />
          <div class="key">
            <CostRow minutes={minutes} wage={wage} setCost={setCost} />
            <ChanceRow a={lead} />
          </div>
          <p class="oneq">{ONE_Q}</p>
        </section>
        <section class="oc-steps" aria-labelledby="oc-s">
          <h2 id="oc-s" class="oc-sh">From one town to the whole country</h2>
          <ol class="oc-list">
            {STOPS.map((id, i) => <Step key={id} a={anchor(id)} C={C} reading={reading} br={br} refFn={el => { steps.current[i] = el; }} />)}
            <li class="oc-step oc-last" ref={el => { steps.current[STOPS.length] = el; }}>
              <h3>Every contest</h3>
              <p class="oc-txt">Each contest has its own N. Of the <span class="num">{br.total.toLocaleString('en-US')}</span> sample contests:</p>
              <ul class="oc-bands">
                {[[0, 3, 'Better than 1 in 1,000'], [3, 6, '1 in 1,000 to 1 in a million'], [6, 9, '1 in a million to 1 in a billion'], [9, 99, 'Rarer than 1 in a billion']].map(([lo, hi, t]) => (
                  <li><span>{t}</span><span class="num">{(br.below(hi) - br.below(lo)).toLocaleString('en-US')}</span></li>
                ))}
              </ul>
              <p class="src">Sample contests, invented until the data lands; the counts will change.</p>
            </li>
          </ol>
          <p class="src oc-srcs">Gelman, Silver and Edlin, Economic Inquiry, 2012 (the presidency, 2008). Mulligan and Hunter, Public Choice, 2003 (the House). The town race is the model’s stylised example. Read 7 November 2026.</p>
        </section>
      </div>
      {desk ? <div class="oc-stage-col"><Stage steps={steps} leadRef={leadRef} desk={desk} /></div> : null}
    </main>
  );
}

function Step({ a, C, reading, br, refFn }) {
  const v = bstar(a, C, reading);
  const [n, w] = moneyParts(v);
  const per = reading === 'person';
  const k = br.below(Math.log10(a.N));
  const f = useFold();
  return (
    <li class="oc-step" ref={refFn}>
      <p class="oc-k">{a.when === 'stylised' ? 'Stylised, ' : ''}{a.short}{a.when !== 'stylised' ? `, ${a.when}` : ''}</p>
      <p class="oc-n"><button type="button" class="fig-btn" {...f.btn} onClick={f.toggle}>{oneIn(a.N)}</button></p>
      <FoldBody fold={f}>
        {a.mark ? <p><span class="k">{a.mark}</span></p> : null}
        <p>{a.src}</p>
        <p>{TIE} The chance the count without you lands within one vote is twice this: {oneIn(a.N / 2)}.</p>
      </FoldBody>
      <p class="oc-b"><span class="oc-bf num">{n}{w ? ` ${w}` : ''}</span> <span class="muted">{per ? `to each person in ${a.pop.of}` : 'to you'}</span></p>
      <p class="working">{per ? `${money(C * a.N)} ÷ ${count(a.pop.value)} people (a sample population)` : `${money(C)} × ${digits(a.N)}`}</p>
      <p class="oc-txt">{k === 0 ? 'None' : <span class="num">{k.toLocaleString('en-US')}</span>} of the {br.total.toLocaleString('en-US')} sample contests have a better chance than this.</p>
    </li>
  );
}

// A tile of one point every 3 px, for a field too fine to draw dot by dot.
let tile = null;
function stipple(ctx, colour, dpr) {
  const k = `${colour}|${dpr}`;
  if (tile && tile.k === k) return tile.p;
  const n = Math.round(3 * dpr), c = document.createElement('canvas'); c.width = n; c.height = n;
  const x = c.getContext('2d'); x.fillStyle = colour; x.fillRect(0, 0, Math.max(1, Math.round(1.4 * dpr)), Math.max(1, Math.round(1.4 * dpr)));
  tile = { k, p: ctx.createPattern(c, 'repeat') };
  return tile.p;
}

// The stage: the field of dots, sized to its box, its scale set by where the reader is in the steps.
function Stage({ steps, leadRef, desk }) {
  const box = useRef(null), cvs = useRef(null), cap = useRef(null);
  const colours = useColours();
  const [D, setD] = useState(0);
  useLayoutEffect(() => {
    const ro = new ResizeObserver(e => setD(Math.max(0, Math.floor(Math.min(e[0].contentRect.width, e[0].contentRect.height)))));
    ro.observe(box.current);
    return () => ro.disconnect();
  }, []);
  // the points the scroll moves between: the lead, the five stops, the last step (held at the last stop)
  const P = useMemo(() => [LEAD, ...STOPS, 'safe'].map(id => ({ id, ls: half(anchor(id).N) })), []);
  const caption = id => `${CAP[id]}. The ringed dot is a run your ballot decides.${id === 'town' ? '' : ' The squares inside are the smaller fields.'}`;

  const where = () => {
    const els = [leadRef.current, ...steps.current];
    if (els.some(e => !e)) return 0;
    const sb = box.current.getBoundingClientRect();
    const F = desk ? innerHeight * 0.5 : sb.bottom + (innerHeight - sb.bottom) * 0.45;
    const c = els.map(e => { const r = e.getBoundingClientRect(); return r.top + Math.min(r.height, innerHeight * 0.6) / 2; });
    if (F <= c[0]) return 0;
    for (let i = 0; i < c.length - 1; i++) if (F < c[i + 1]) return i + (F - c[i]) / (c[i + 1] - c[i]);
    return c.length - 1;
  };

  const draw = t => {
    const el = cvs.current; if (!el || !D || !colours) return;
    if (reducedMotion()) t = Math.round(t);
    // the field holds still at each stop while its words are read, and moves between them
    const i = Math.min(P.length - 2, Math.floor(t)), f = Math.min(1, Math.max(0, (t - i - 0.3) / 0.4));
    const ls = P[i].ls + (P[i + 1].ls - P[i].ls) * f;
    const S = 10 ** ls, n = Math.round(S * S);
    const dpr = Math.min(2, window.devicePixelRatio || 1);
    if (el.width !== D * dpr) { el.width = D * dpr; el.height = D * dpr; }
    const ctx = el.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, D, D);
    const pad = 12, inner = D - pad * 2, pitch = inner / S, mid = D / 2;
    const cols = Math.ceil(S), rows = Math.ceil(n / cols);
    const x0 = mid - (cols * pitch) / 2, y0 = mid - (rows * pitch) / 2;
    ctx.fillStyle = colours.dot;
    if (pitch >= 2.5) {
      // every run a dot
      const s = Math.max(1, pitch * (pitch > 8 ? 0.5 : 0.6));
      ctx.globalAlpha = pitch > 8 ? 0.55 : 0.5;
      for (let k = 0; k < n; k++) {
        const r = Math.floor(k / cols), c = k % cols;
        const x = x0 + (c + 0.5) * pitch, y = y0 + (r + 0.5) * pitch;
        if (pitch > 8) { ctx.beginPath(); ctx.arc(x, y, s / 2, 0, Math.PI * 2); ctx.fill(); } else ctx.fillRect(x - s / 2, y - s / 2, s, s);
      }
    } else {
      // too many to draw one by one: the same field as a stipple, each point standing for many runs
      ctx.globalAlpha = 0.5;
      ctx.fillStyle = stipple(ctx, colours.dot, dpr);
      ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.fillRect(Math.round((mid - inner / 2) * dpr), Math.round((mid - inner / 2) * dpr), Math.round(inner * dpr), Math.round(inner * dpr));
      ctx.restore(); ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    ctx.globalAlpha = 1;
    // the earlier fields, as outlined squares inside this one
    ctx.strokeStyle = colours.fg; ctx.lineWidth = 1;
    for (const id of STOPS) {
      const sd = 10 ** half(anchor(id).N) * pitch;
      if (sd >= inner - 1 || sd < 6) continue;
      ctx.globalAlpha = 0.7;
      ctx.strokeRect(Math.round(mid - sd / 2) + 0.5, Math.round(mid - sd / 2) + 0.5, Math.round(sd), Math.round(sd));
    }
    ctx.globalAlpha = 1;
    // the run your ballot decides: the dot at the centre, in the accent (R4: "you"), ringed so it is found at any scale
    const cr = Math.max(0, Math.floor(rows / 2)), cc = Math.floor(cols / 2);
    const mx = pitch >= 2.5 ? x0 + (cc + 0.5) * pitch : mid, my = pitch >= 2.5 ? y0 + (cr + 0.5) * pitch : mid;
    ctx.fillStyle = colours.accent;
    ctx.beginPath(); ctx.arc(mx, my, Math.max(2.5, Math.min(6, pitch * 0.3)), 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = colours.accent; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.arc(mx, my, Math.max(9, pitch * 0.6), 0, Math.PI * 2); ctx.stroke();
    // the caption names the nearest stop; it changes at once (text never travels)
    const near = P[Math.min(P.length - 1, Math.round(t))].id;
    if (cap.current && cap.current.dataset.id !== near) { cap.current.dataset.id = near; cap.current.textContent = caption(near); }
  };

  useEffect(() => {
    let raf = 0;
    const on = () => { if (!raf) raf = requestAnimationFrame(() => { raf = 0; draw(where()); }); };
    on();
    addEventListener('scroll', on, { passive: true });
    addEventListener('resize', on);
    return () => { removeEventListener('scroll', on); removeEventListener('resize', on); cancelAnimationFrame(raf); };
  }, [D, colours, desk]);

  return (
    <div class="oc-stage">
      <div class="oc-box" ref={box}>
        <Boundary what="The field of runs" fallback={() => <p class="muted">The field could not be drawn.</p>}>
          <canvas ref={cvs} class="oc-c" style={{ width: `${D}px`, height: `${D}px` }} role="img" aria-label="A square field of dots, one for each run of the election; one dot, ringed, is a run your ballot decides. As you scroll, the field grows from 468 dots to a billion." />
        </Boundary>
      </div>
      <p class="oc-cap src" ref={cap} data-id={LEAD}>{caption(LEAD)}</p>
    </div>
  );
}
