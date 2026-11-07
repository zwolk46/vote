// The field: every contest on one ruler of dollars, in rows by level (design/DESIGN-SPEC.md §2.1, §2.2), drawn as the
// midterms site draws its races: whole dots, stacked in their bin, moving together (the maker, 04:09 UTC 11-07, holding
// up the midterms graphs "with the dots that move together for each individual race"; zwolk46/midterms
// src/components/Prices.jsx and Swing.jsx, the binned beeswarm of lib/markets.js `swarm`, and Closest.jsx, the ruler of
// the closest races, whose marks are ringed dots). One dot is a group of 100 sample contests (data/sample.js
// sampleGroups), so each can be seen and counted; the named figures are ringed marks in a lane under their row.
//
// Where a dot stands is the formula, not a layout: x = log10(B*) = log10(C) + log10(N), so the distance from the
// reader's cost to a dot is the size of N (§2.1). The stacks are binned from the reader's cost, so a new cost moves
// the whole field by one distance (V2, `chart`). The arrival (V1, `nav-in`) sends every dot from the cost line to its
// place, the nearest first, as the midterms swarms stagger theirs; the reading "to each person" (V3, `chart`) moves
// each dot to its own new place, staggered the same way. Every frame is drawn on one canvas (Prices.jsx: a canvas is
// what stays under 50 ms a frame at 4x CPU). Under reduced motion each is drawn at its end at once (MOTION-SPEC s.5).
import { useEffect, useLayoutEffect, useMemo, useRef, useState } from 'preact/hooks';
import { sampleGroups, UNIT } from '../data/sample.js';
import { ANCHORS, LEVELS } from '../data/real.js';
import { TOKENS, springValue, reducedMotion } from '../lib/motion.js';
import { tick, tickShort } from '../lib/format.js';
import { useColours } from '../lib/media.js';

export const LO = -2, HI = 12;   // 1 cent to 1 trillion dollars: both readings on one ruler, so switching moves the dots, not the ruler
const SPAN = HI - LO;
// first dot to last (Prices.jsx STAGGER, 240 ms); the rest of the token's duration is each dot's own slide
export const STAGGER = { 'nav-in': 240, chart: 150 };

// A row's stacks: each dot in the bin of its x, counted from the cost, stacked up from the row's base. `rel` is each
// dot's log10(N) (or log10(N ÷ population)), so the layout does not depend on the cost. Returns, per dot, its offset in
// px from the cost line and its place in its stack.
export function stacks(rel, pw, r) {
  const bw = 2 * r, at = new Array(rel.length), bins = new Map();
  let rows = 0;
  for (let i = 0; i < rel.length; i++) {
    const dx = (Math.max(LO, Math.min(HI, rel[i])) / SPAN) * pw;
    const b = Math.floor(dx / bw);
    const k = bins.get(b) || 0; bins.set(b, k + 1);
    at[i] = { dx: (b + 0.5) * bw, k };
    rows = Math.max(rows, k + 1);
  }
  return { at, rows };
}
// The stacks' pitch: a dot's width, closer when the tallest stack would pass the strip (lib/markets.js pitchFor)
export const pitchFor = (rows, r, h) => (rows <= 1 ? 2 * r : Math.min(2 * r, (h - 2 * r) / (rows - 1)));
// The order the dots set off in: nearest the cost first, a ripple from the line outward (Closest.jsx)
export function orderOf(rel) {
  const o = new Float32Array(rel.length), idx = Array.from(rel, (_, i) => i).sort((a, b) => rel[a] - rel[b]);
  idx.forEach((i, k) => { o[i] = idx.length > 1 ? k / (idx.length - 1) : 0; });
  return o;
}

export function useGroups() {
  return useMemo(() => { const g = sampleGroups(); return LEVELS.map(L => ({ ...L, ...g[L.id] })); }, []);
}

// Row geometry: on the phone the row's name sits on its own line above its stacks; on the desktop in a column at the
// left. Under the stacks, a lane for the named figures' marks.
// A row's stacks are as tall as they need to be, up to stripH, so a level of a few dots takes a thin row and the
// levels with thousands of contests take the room (the breadth is in the heights too).
function geometry(w, desk) {
  const left = desk ? 168 : 0, right = desk ? 8 : 0;
  return { w, left, pw: Math.max(10, w - left - right), labelH: desk ? 0 : 20, stripH: desk ? 60 : 46, minH: desk ? 46 : 0, lane: 18, gap: desk ? 10 : 8, topH: 22, axisH: 30, r: desk ? 3 : 2.1 };
}

export function Field({ C, reading, sel, onSel, desk }) {
  const wrap = useRef(null), cvs = useRef(null), costL = useRef(null);
  const rows = useGroups();
  const colours = useColours();
  const [w, setW] = useState(0);
  useLayoutEffect(() => {
    const ro = new ResizeObserver(e => setW(Math.round(e[0].contentRect.width)));
    ro.observe(wrap.current);
    return () => ro.disconnect();
  }, []);
  const g = useMemo(() => geometry(w, desk), [w, desk]);
  const X = lx => g.left + ((lx - LO) / SPAN) * g.pw;
  // both readings laid out at once, so a row's pitch is the same in each and only the dots move (Prices.jsx)
  const lay = useMemo(() => {
    if (!w) return null;
    let y = g.topH;
    const L = rows.map(R => {
      const you = stacks(R.you, g.pw, g.r), person = stacks(R.person, g.pw, g.r);
      const n = Math.max(you.rows, person.rows);
      const strip = Math.max(g.minH - g.lane, Math.min(g.stripH, n * 2 * g.r + 3));
      const top = y, base = top + g.labelH + strip;
      y = base + g.lane + g.gap;
      return { you: you.at, person: person.at, pitch: pitchFor(n, g.r, strip - 3), order: orderOf(R.you), top, strip, base, lane: base + g.lane / 2 + 1 };
    });
    L.end = y - g.gap;
    L.h = L.end + g.axisH;
    return L;
  }, [rows, w, g]);

  // What is drawn now: the cost (lc), and for each dot a mix between its places in the two readings (m) and between
  // the cost line and its place (k). A tween moves these toward their targets, from wherever they stand.
  const cur = useRef({ lc: Math.log10(C), m: null, k: null, mm: reading === 'person' ? 1 : 0 });
  const owner = useRef({ raf: 0 });
  const arrived = useRef(false);
  const mOf = rd => (rd === 'person' ? 1 : 0);
  const ensure = () => {
    const c = cur.current;
    if (lay && (!c.m || c.m.length !== lay.length)) {
      c.m = lay.map(L => new Float32Array(L.you.length).fill(c.mm));
      c.k = lay.map(L => new Float32Array(L.you.length).fill(arrived.current ? 1 : 0));
    }
  };

  const draw = () => {
    const el = cvs.current; if (!el || !w || !colours || !lay) return;
    ensure();
    const dpr = Math.min(2, window.devicePixelRatio || 1);
    const H = lay.h;
    if (el.width !== Math.round(w * dpr) || el.height !== Math.round(H * dpr)) { el.width = Math.round(w * dpr); el.height = Math.round(H * dpr); }
    const ctx = el.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, w, H);
    const { lc } = cur.current, cx0 = X(lc);
    const plotTop = g.topH - 4, plotBot = lay.end;
    // the ruler's decades: a hairline each, a stronger one at each thousandfold (where the words are)
    for (let p = LO; p <= HI; p++) {
      const x = Math.round(X(p)) + 0.5;
      ctx.strokeStyle = (p % 3 === 0) ? colours.lineStrong : colours.line; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(x, plotTop); ctx.lineTo(x, plotBot + 6); ctx.stroke();
    }
    const r = g.r;
    let mix = 0, n = 0;
    lay.forEach((L, ri) => {
      const base = L.base;
      ctx.strokeStyle = colours.lineStrong; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(g.left, Math.round(base) + 0.5); ctx.lineTo(g.left + g.pw, Math.round(base) + 0.5); ctx.stroke();
      ctx.fillStyle = colours.dot;
      const M = cur.current.m[ri], K = cur.current.k[ri];
      for (let i = 0; i < L.you.length; i++) {
        const a = L.you[i], b = L.person[i], m = M[i], k = K[i];
        mix += m; n++;
        const x = cx0 + (a.dx + (b.dx - a.dx) * m) * k;
        const y = base - r - 1.5 - (a.k + (b.k - a.k) * m) * L.pitch * k;
        if (x < g.left - r || x > g.left + g.pw + r) continue;
        ctx.beginPath(); ctx.arc(x, y, r, 0, 6.2832); ctx.fill();
      }
    });
    const mm = n ? mix / n : 0;
    cur.current.mm = mm;
    // the named figures: a ringed mark each in the lane under its row (Closest.jsx's marks: a ring round a dot); the one
    // in focus in the accent (R4: the accent means "you")
    const kA = cur.current.k[0]?.length ? cur.current.k[0].reduce((s, x) => s + x, 0) / cur.current.k[0].length : 1;
    for (const a of ANCHORS) {
      const ri = LEVELS.findIndex(L => L.id === a.level);
      const rel = Math.max(LO, Math.min(HI, Math.log10(a.N) - mm * Math.log10(a.pop.value)));
      const x = cx0 + (rel / SPAN) * g.pw * kA;
      const y = lay[ri].lane;
      const on = a.id === sel, R1 = desk ? 6.5 : 6, R0 = on ? (desk ? 3.5 : 3.2) : 2.4;
      ctx.beginPath(); ctx.arc(x, y, R1, 0, 6.2832); ctx.fillStyle = colours.bg; ctx.fill();
      ctx.lineWidth = on ? 2 : 1.25; ctx.strokeStyle = on ? colours.accent : colours.fg; ctx.stroke();
      ctx.beginPath(); ctx.arc(x, y, R0, 0, 6.2832); ctx.fillStyle = on ? colours.accent : colours.fg; ctx.fill();
    }
    // the reader's cost: a line through every row, in the accent; on the reading "to each person" it has no place (the
    // cost is the voter's, the stakes are each person's), so it fades as the dots move (opacity, kept under reduce)
    const cx = Math.round(cx0) + 0.5;
    ctx.globalAlpha = Math.max(0, 1 - mm);
    ctx.strokeStyle = colours.accent; ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.moveTo(cx, plotTop); ctx.lineTo(cx, plotBot + 6); ctx.stroke();
    ctx.globalAlpha = 1;
    if (costL.current) { costL.current.style.transform = `translateX(${cx}px)`; costL.current.style.opacity = String(Math.max(0, 1 - mm)); }
  };

  // Every dot on the spring, each starting `order × stagger` after the first (Prices.jsx's loop); `set(ri, i, v)` puts
  // dot i of row ri at the spring's value v of its own slide. One loop at a time: a new one starts from where the old
  // one left each dot (interruptible, MOTION-SPEC s.4.4).
  const run = (token, set) => {
    cancelAnimationFrame(owner.current.raf); owner.current.raf = 0;
    const total = TOKENS[token].duration, st = STAGGER[token] || 0, slide = total - st;
    if (reducedMotion() || document.hidden) { lay.forEach((L, ri) => { for (let i = 0; i < L.you.length; i++) set(ri, i, 1); }); draw(); return; }
    const t0 = performance.now();
    const step = t => {
      const e = t - t0; let live = false;
      lay.forEach((L, ri) => {
        for (let i = 0; i < L.you.length; i++) {
          const q = (e - L.order[i] * st) / slide;
          if (q < 1) live = true;
          set(ri, i, springValue(Math.max(0, Math.min(1, q))));
        }
      });
      draw();
      owner.current.raf = live ? requestAnimationFrame(step) : 0;
    };
    owner.current.raf = requestAnimationFrame(step);
  };

  // the arrival (V1), once, when the field first has a width; not in a hidden tab, not in the per-person reading
  useEffect(() => {
    if (!w || !colours || !lay) return;
    if (!arrived.current) {
      ensure();
      arrived.current = true;
      if (reducedMotion() || document.hidden || reading === 'person') { cur.current.k.forEach(K => K.fill(1)); draw(); return; }
      run('nav-in', (ri, i, v) => { cur.current.k[ri][i] = v; });
      return;
    }
    if (!owner.current.raf) draw();
  }, [w, desk, colours, sel, lay]);

  // V3: the reading; each dot from where it stands to its place in the new reading
  const firstReading = useRef(true);
  useEffect(() => {
    if (firstReading.current) { firstReading.current = false; return; }
    if (!arrived.current || !lay) return;
    ensure();
    const to = mOf(reading), fm = cur.current.m.map(M => Float32Array.from(M)), fk = cur.current.k.map(K => Float32Array.from(K));
    run('chart', (ri, i, v) => { cur.current.m[ri][i] = fm[ri][i] + (to - fm[ri][i]) * v; cur.current.k[ri][i] = fk[ri][i] + (1 - fk[ri][i]) * v; });
  }, [reading]);

  // V2: the cost; the whole field by one distance
  useEffect(() => {
    const to = Math.log10(C);
    if (!arrived.current || !lay) { cur.current.lc = to; return; }
    const from = cur.current.lc;
    if (from === to) return;
    cancelAnimationFrame(owner.current.raf); owner.current.raf = 0;
    cur.current.k.forEach(K => K.fill(1));
    if (reducedMotion()) { cur.current.lc = to; draw(); return; }
    const t0 = performance.now(), d = TOKENS.chart.duration;
    const step = t => { const f = Math.min(1, (t - t0) / d); cur.current.lc = from + (to - from) * springValue(f); draw(); owner.current.raf = f < 1 ? requestAnimationFrame(step) : 0; };
    owner.current.raf = requestAnimationFrame(step);
  }, [C]);
  useEffect(() => () => cancelAnimationFrame(owner.current.raf), []);

  const pick = e => {
    const r = cvs.current.getBoundingClientRect(), px = e.clientX - r.left, py = e.clientY - r.top;
    let best = null, bd = 22;
    for (const a of ANCHORS) {
      const ri = LEVELS.findIndex(L => L.id === a.level);
      const x = X(Math.log10(C) + Math.max(LO, Math.min(HI, Math.log10(a.N) - (reading === 'person' ? Math.log10(a.pop.value) : 0)))), y = lay[ri].lane;
      const d = Math.hypot(px - x, py - y); if (d < bd) { bd = d; best = a.id; }
    }
    if (best) onSel(best);
  };

  const ticks = [-2, 0, 3, 6, 9, 12];
  const long = (g.pw * 3) / SPAN >= 96;
  return (
    <div class="field" ref={wrap} style={{ height: `${lay ? lay.h : 400}px` }}>
      <canvas ref={cvs} class="field-c" data-fit-under style={{ width: `${w}px`, height: `${lay ? lay.h : 400}px` }} role="img" onClick={pick}
        aria-label={`Every contest on one scale of dollars, from 1 cent to 1 trillion, in rows: ${rows.map(r => `${r.name}, ${r.count.toLocaleString('en-US')}`).join('; ')}. Each dot is ${UNIT} sample contests. The named figures are ringed, and listed below.`} />
      {lay && rows.map((r, ri) => (
        <div class="field-row" style={{ top: `${lay[ri].top}px`, height: `${desk ? lay[ri].base + g.lane - lay[ri].top : g.labelH}px`, width: desk ? `${g.left - 16}px` : '100%' }} aria-hidden="true">
          <span class="field-n">{r.name}</span><span class="field-k num">{r.count.toLocaleString('en-US')}</span>
        </div>
      ))}
      <span ref={costL} class="field-cost" aria-hidden="true">Your cost</span>
      <div class="field-axis" style={{ top: `${lay ? lay.end + 8 : 0}px` }} aria-hidden="true">
        {ticks.map(p => <span class={`field-t${p === LO ? ' first' : p === HI ? ' last' : ''}`} style={{ left: `${X(p)}px` }}>{p === -2 ? '1¢' : long ? tick(p) : tickShort(p)}</span>)}
      </div>
    </div>
  );
}
