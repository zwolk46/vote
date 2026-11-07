// Candidate B, "Your ballot, line by line" (design/DESIGN-SPEC.md §5): the decision first. One trip to the polls
// casts a vote on every line of the ballot, so the trip pays when the lines' shares add to 100% (law 2c; §2.3). Each
// line has its B* at the right edge and a track on which the reader sets what that outcome is worth to them; behind
// each track, faint, every contest of its kind (the sample field, marked). The lead figure is the line in focus.
//
// Motion (§4): V2 a new cost moves every line's contests and its B* mark by one distance (`chart`, one transform per
// line); V3 the reading moves each dot by its own population (`chart`, drawn frame by frame); V5 a stake follows the
// finger with no easing; V4 a figure changes at once. Under reduced motion each is at its end at once.
import { useEffect, useLayoutEffect, useMemo, useRef, useState } from 'preact/hooks';
import { anchor } from '../data/real.js';
import { sampleTotal } from '../data/sample.js';
import { money, oneIn, pct, count, tick, tickShort } from '../lib/format.js';
import { useMedia, DESKTOP, useColours } from '../lib/media.js';
import { tween, play } from '../lib/motion.js';
import { LeadFigure, CostRow, ChanceRow, ReadingSeg, ONE_Q, bstar } from '../components/Lead.jsx';
import { useRows, LO, HI } from '../components/Field.jsx';
import { Seg } from '../components/Seg.jsx';
import { Boundary } from '../components/Boundary.jsx';
import './ballot.css';

const SPAN = HI - LO;
// a stake to two significant figures, as a reader would name it ($5,000, not $5,010)
const snap = lx => { const v = 10 ** lx, d = 10 ** (Math.floor(Math.log10(v)) - 1); return Math.log10(Math.max(0.01, Math.round(v / d) * d)); };
// a share as the reader says it: "<1%", "24%", "140%", "9 times over", "71,000 times over"
const share = x => (x < 10 ? pct(x * 100) : `${count(Math.round(x))} times`);
const at = lx => ((lx - LO) / SPAN) * 100;          // percent of the track
const shift = d => `translateX(${(d / SPAN) * 100}%)`;

// The ballot, top line to bottom. A line without a figure of record says so; its contests are still behind it.
const WHERE = [['close', 'Closest states'], ['avg', 'Average'], ['safe', 'Safest states']];
const LINES = [
  { level: 'president', name: 'President' },
  { level: 'senate', name: 'U.S. Senate' },
  { level: 'governor', name: 'Governor' },
  { level: 'house', name: 'U.S. House', a: 'house', ctx: 'On average, 1898–1992' },
  { level: 'state', name: 'State legislature' },
  { level: 'local', name: 'Town race', a: 'town', ctx: 'Stylised, 2,000 voters' },
];

export function Ballot({ C, minutes, wage, setCost, reading, setReading }) {
  const desk = useMedia(DESKTOP);
  const [where, setWhere] = useState('close');
  const [focus, setFocus] = useState('president');
  // level -> log10 of the stake, for each reading apart (worth to you and worth to each person are different
  // questions); none by default (no default B)
  const [allStakes, setAll] = useState({ you: {}, person: {} });
  const stakes = allStakes[reading];
  const setStakes = f => setAll(s => ({ ...s, [reading]: f(s[reading]) }));
  const lines = LINES.map(L => {
    const id = L.level === 'president' ? where : L.a;
    const a = id ? anchor(id) : null;
    return { ...L, a, ctx: L.level === 'president' ? `${WHERE.find(w => w[0] === where)[1]}, 2008` : L.ctx };
  });
  const fl = lines.find(l => l.level === focus) || lines[0];
  const shares = lines.map(l => (l.a && stakes[l.level] != null ? 10 ** stakes[l.level] / bstar(l.a, C, reading) : 0));
  const total = shares.reduce((s, x) => s + x, 0);
  const anySet = Object.keys(stakes).length > 0;

  const lead = (
    <div class="bt-lead">
      <p class="contest"><span class="n">{fl.a.name}</span><br /><span class="w">{fl.a.when === 'stylised' ? 'Stylised' : fl.a.when}</span></p>
      <LeadFigure a={fl.a} C={C} reading={reading} />
      <ReadingSeg reading={reading} setReading={setReading} />
      <div class="key">
        <CostRow minutes={minutes} wage={wage} setCost={setCost} />
        <ChanceRow a={fl.a} />
      </div>
    </div>
  );
  const trip = <Trip lines={lines} shares={shares} total={total} anySet={anySet} C={C} reading={reading} />;

  return (
    <main class="page bt">
      <div class="bt-main">
        <section class="bt-intro" aria-labelledby="bt-h">
          <h1 id="bt-h">One trip, every contest on the ballot</h1>
          <p class="bt-say">Each line’s figure is what its outcome would have to be worth for one vote on it to pay. Set what each is worth to you; the trip pays when the shares add to 100%.</p>
        </section>
        {desk ? null : lead}
        {desk ? null : <p class="oneq">{ONE_Q}</p>}
        <section class="bt-ballot" aria-labelledby="bt-b">
          <div class="bt-bh">
            <h2 id="bt-b">Your ballot</h2>
            <span class="src num">{sampleTotal().toLocaleString('en-US')} sample contests behind its lines</span>
          </div>
          <div class="bt-where"><span class="src">Where you vote for president</span><Seg label="Where you vote for president" options={WHERE} value={where} onChange={setWhere} /></div>
          <Boundary what="The ballot" fallback={() => <p class="muted">The ballot could not be drawn.</p>}>
            <Lines lines={lines} C={C} reading={reading} desk={desk} stakes={stakes} setStakes={setStakes} shares={shares} focus={focus} setFocus={setFocus} />
          </Boundary>
          {desk ? null : trip}
        </section>
      </div>
      {desk ? <aside class="bt-side" aria-label="The line in focus and the trip">{lead}{trip}<p class="oneq">{ONE_Q}</p></aside> : null}
    </main>
  );
}

// The lines, each with its contests behind it. A new cost redraws the dots at their new places and moves each line's
// layer from where it stood, one transform per line (V2); the reading redraws the dots frame by frame (V3).
function Lines({ lines, C, reading, desk, stakes, setStakes, shares, focus, setFocus }) {
  const rows = useRows();
  const colours = useColours();
  const first = useRef(null);
  const [w, setW] = useState(0);
  useLayoutEffect(() => {
    const ro = new ResizeObserver(e => setW(Math.round(e[0].contentRect.width)));
    ro.observe(first.current);
    return () => ro.disconnect();
  }, []);
  const wide = useMedia('(min-width: 1100px)');   // the line in one row (ballot.css)
  const H = wide ? 36 : 30;
  const cvs = useRef([]), layers = useRef([]), ticks = useRef([]);
  const m = useRef(reading === 'person' ? 1 : 0);
  const owner = useRef({});
  const lc = Math.log10(C);

  const draw = () => {
    if (!w || !colours) return;
    const dpr = Math.min(2, window.devicePixelRatio || 1);
    const s = desk ? 1.8 : 1.5, sc = colours.dotA / 0.32, mm = m.current;
    lines.forEach((l, i) => {
      const el = cvs.current[i]; if (!el) return;
      if (el.width !== Math.round(w * dpr) || el.height !== Math.round(H * dpr)) { el.width = Math.round(w * dpr); el.height = Math.round(H * dpr); }
      const ctx = el.getContext('2d');
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, w, H);
      const r = rows.find(x => x.id === l.level);
      ctx.fillStyle = colours.dot; ctx.globalAlpha = Math.min(0.3, Math.max(0.03, 5 / Math.sqrt(r.count))) * sc;   // faint: behind the line, not the line
      const { logN, logPop, yU, yP } = r, cy = H / 2, hh = H - 4;
      for (let k = 0; k < logN.length; k++) {
        const x = (at(lc + logN[k] - mm * logPop[k]) / 100) * w, y = cy + (yU[k] + (yP[k] - yU[k]) * mm) * hh;
        ctx.fillRect(x - s / 2, y - s / 2, s, s);
      }
      const t = ticks.current[i];
      if (t && l.a) t.style.left = `${at(lc + Math.log10(l.a.N) - mm * Math.log10(l.a.pop.value))}%`;
    });
  };
  useEffect(draw, [w, H, desk, colours, lines.map(l => l.a?.id).join()]);

  // V3: the reading
  const firstRun = useRef(true);
  useEffect(() => {
    if (firstRun.current) { firstRun.current = false; return; }
    const from = m.current, to = reading === 'person' ? 1 : 0;
    tween(owner.current, 'chart', f => { m.current = from + (to - from) * f; draw(); });
  }, [reading]);

  // V2: the cost moves each line's layer by one distance
  const prevLc = useRef(lc);
  useLayoutEffect(() => {
    // drawn at the new cost at once, then each layer moved from where it stood to rest (no layer is left cut by its
    // track at rest)
    if (prevLc.current !== lc) { draw(); layers.current.forEach(el => el && play(el, 'chart', [{ transform: shift(prevLc.current - lc) }, { transform: shift(0) }], { kind: 'shift' })); }
    prevLc.current = lc;
  }, [lc]);

  const axis = [0, 3, 6, 9];
  return (
    <>
      <div class="bt-axis" aria-hidden="true">
        <span class="bt-axis-in">{axis.map(p => <span class={`bt-t${p === HI ? ' last' : ''}`} style={{ left: `${at(p)}%` }}>{desk ? tick(p) : tickShort(p)}</span>)}</span>
      </div>
      <ol class="bt-lines">
        {lines.map((l, i) => {
          const r = rows.find(x => x.id === l.level);
          const v = stakes[l.level];
          const B = l.a ? bstar(l.a, C, reading) : null;
          const per = reading === 'person';
          return (
            <li class={`bt-line${l.level === focus ? ' on' : ''}`} key={l.level}>
              <span class="bt-name">{l.name}</span>
              {l.a
                ? <button type="button" class="bt-fig" aria-pressed={l.level === focus ? 'true' : 'false'} aria-label={`${l.name}: ${money(B)}. Show in focus`} onClick={() => setFocus(l.level)}>{money(B)}</button>
                : <span class="bt-fig none">No figure yet</span>}
              <span class="bt-ctx">{l.a ? `${l.ctx} · ${oneIn(l.a.N)}` : 'Its figure comes with the data'}<span class="bt-n"><span class="sep"> · </span><span class="num">{r.count.toLocaleString('en-US')}</span> sample contests</span></span>
              <div class="bt-track" ref={i === 0 ? first : null}>
                <div class="bt-layer" ref={el => { layers.current[i] = el; }}>
                  <canvas ref={el => { cvs.current[i] = el; }} class="bt-c" style={{ width: `${w}px`, height: `${H}px` }} aria-hidden="true" />
                  {l.a ? <span class="bt-bstar" ref={el => { ticks.current[i] = el; }} style={{ left: `${at(lc + Math.log10(l.a.N) - m.current * Math.log10(l.a.pop.value))}%` }} aria-hidden="true" /> : null}
                </div>
                {l.a
                  ? <input type="range" class={`bt-range${v == null ? ' unset' : ''}`} min={LO} max={HI} step="0.01" value={v ?? LO}
                    aria-label={`What the outcome of the ${l.name} line is worth ${per ? 'to each person' : 'to you'}`} aria-valuetext={v == null ? 'Not set' : money(10 ** v)}
                    onInput={e => { const x = snap(parseFloat(e.currentTarget.value)); setStakes(s => ({ ...s, [l.level]: x })); setFocus(l.level); }} />
                  : null}
              </div>
              {l.a
                ? <span class="bt-worth">{v == null ? <span class="muted">{per ? 'Worth to each person: drag to set' : 'Worth to you: drag to set'}</span> : <>{per ? 'Worth to each person' : 'Worth to you'} <b class="num">{money(10 ** v)}</b></>}</span>
                : <span class="bt-worth" />}
              <span class="bt-share num">{l.a && v != null ? (shares[i] < 10 ? `${share(shares[i])} of the trip` : `${share(shares[i])} the trip`) : ''}</span>
            </li>
          );
        })}
      </ol>
      <p class="src bt-srcs">Gelman, Silver and Edlin, Economic Inquiry, 2012 (the presidency, 2008). Mulligan and Hunter, Public Choice, 2003 (the House). The town race is the model’s stylised example. The faint dots behind each line are sample contests, invented until the data lands; the mark on each track is its figure. Read 7 November 2026.</p>
    </>
  );
}

// The trip: the lines' shares added, toward 100% (law 2c). It says nothing until a stake is set.
function Trip({ lines, shares, total, anySet, C, reading }) {
  let cum = 0;
  const segs = shares.map((s, i) => { const l = Math.min(100, cum * 100), wv = Math.max(0, Math.min(100, (cum + s) * 100) - l); cum += s; return { i, l, w: wv }; }).filter(x => x.w > 0);
  const pays = total >= 1;
  return (
    <section class="bt-trip" aria-labelledby="bt-tr" aria-live="polite">
      <div class="bt-trip-h">
        <h2 id="bt-tr" class="bt-trip-t">The trip</h2>
        <span class="bt-trip-f num">{!anySet ? `costs ${money(C)}` : pays ? (total < 10 ? `Pays: ${share(total)}` : `Pays ${share(total)} over`) : `${share(total)} of the way`}</span>
      </div>
      <div class="bt-bar" role="img" aria-label={anySet ? `The shares add to ${total < 10 ? share(total) : `${share(total)} over`} what the trip costs.` : 'No stake set yet.'}>
        {segs.map(s => <span class="bt-seg" style={{ left: `${s.l}%`, width: `${s.w}%` }} />)}
      </div>
      <p class="src bt-trip-s">{!anySet
        ? `Drag a line to say what its outcome is worth ${reading === 'person' ? 'to each person' : 'to you'}. Each line adds its share; the trip pays at 100%.`
        : `${lines.filter((l, i) => shares[i] > 0).length} of ${lines.filter(l => l.a).length} lines with a figure set. A share below 1% shows as <1%.`}</p>
    </section>
  );
}
