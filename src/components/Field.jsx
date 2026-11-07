// The field: every contest on one ruler of dollars, in rows by level (design/DESIGN-SPEC.md §2.1, §2.2), drawn as the
// midterms site draws its races: whole dots, stacked in their bin, moving together (the maker, 04:09 UTC 11-07, holding
// up the midterms graphs "with the dots that move together for each individual race"; zwolk46/midterms
// src/components/Prices.jsx and Swing.jsx, the binned beeswarm of lib/markets.js `swarm`, and Closest.jsx, the ruler of
// the closest races, whose marks are ringed dots). One dot is a group of UNIT contests at its group's middle N
// (src/data/build-field.mjs), so the federal rows are dots that can be seen and counted and the state legislatures'
// 92,000 contests a pile whose height is their density (DESIGN-SPEC §2.2); the named figures are ringed marks in a
// lane under their row.
//
// Two marks carry what the record says of a chance, without a sentence (the maker, 04:32): a dot whose p is an average
// race's, not its own (a state legislature's class C, a chamber's average district, or like past races; the
// orchestrator, 09:31: "mark it visually as a chamber average") is the same dot, lighter, stacked above the contests'
// own; and where a route's back-test leans one way (p.note, "so p may be low"), a dashed arrow points the way the
// figure may lie: on a named figure whose p carries the note, and in the row's count beside the number of its contests
// that carry it (in the House and the Senate, the routes of this site's own model; 538's carry none). In the reading
// "to each person", a contest the data give no population for has no place, so its dot fades where it stands and the
// row counts those that remain.
//
// Where a dot stands is the formula, not a layout: x = log10(B*) = log10(C) + log10(N), so the distance from the
// reader's cost to a dot is the size of N (§2.1). The stacks are binned from the reader's cost, so a new cost moves
// the whole field by one distance (V2, `chart`). The arrival (V1, `nav-in`) sends every dot from the cost line to its
// place, the nearest first, as the midterms swarms stagger theirs; the reading "to each person" (V3, `chart`) moves
// each dot to its own new place, staggered the same way. Every frame is drawn on one canvas (Prices.jsx: a canvas is
// what stays under 50 ms a frame at 4x CPU). Under reduced motion each is drawn at its end at once (MOTION-SPEC s.5).
import { useEffect, useLayoutEffect, useMemo, useRef, useState } from 'preact/hooks';
import { ANCHORS, LEVELS, FIELD, UNIT } from '../data/real.js';
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
// `kind` (the `avg` flags) marks the first and last dot of each kind in each bin (`e`), which thinning keeps.
export function stacks(rel, pw, r, kind) {
  const bw = 2 * r, at = new Array(rel.length), bins = new Map(), ends = new Map();
  let rows = 0;
  for (let i = 0; i < rel.length; i++) {
    if (!Number.isFinite(rel[i])) { at[i] = null; continue; }   // no place in this reading
    const dx = (Math.max(LO, Math.min(HI, rel[i])) / SPAN) * pw;
    const b = Math.floor(dx / bw);
    const k = bins.get(b) || 0; bins.set(b, k + 1);
    at[i] = { dx: (b + 0.5) * bw, k, e: false };
    rows = Math.max(rows, k + 1);
    const key = b * 2 + (kind ? kind[i] : 0), e = ends.get(key);
    if (!e) ends.set(key, [i, i]); else e[1] = i;   // a bin fills upward, so its first and last of a kind are these
  }
  for (const [a, z] of ends.values()) { at[a].e = true; at[z].e = true; }
  return { at, rows };
}
// Thinning a dense pile: where a stack's dots stand closer than a radius, drawing every one of them paints the same
// shape many times over. Every `step`-th dot, and the first and last of each kind in each stack, give the same pile to
// the pixel, at a tenth of the work or less, so the state legislatures' 9,000 dots move inside a frame on a slow phone
// (M-motion s.4 rule 12: no gap between frames over 50 ms at 4x CPU). Only dots that keep their bin in both readings
// (those with no population) are thinned; the rest are few.
export const thinStep = (pitch, r) => Math.max(1, Math.floor((0.8 * r) / Math.max(1e-6, pitch)));
// The dots a row draws and moves: every dot with a place "to each person", and the thinned rest. Each frame visits only
// these, so its work is the drawing's, not the data's.
export function liveOf(you, person, step) {
  const out = [];
  for (let i = 0; i < you.length; i++) if (person[i] !== null || you[i].e || you[i].k % step === 0) out.push(i);
  return Int32Array.from(out);
}
// The stacks' pitch: a dot's width, closer when the tallest stack would pass the strip (lib/markets.js pitchFor)
export const pitchFor = (rows, r, h) => (rows <= 1 ? 2 * r : Math.min(2 * r, (h - 2 * r) / (rows - 1)));
// The order the dots set off in: nearest the cost first, a ripple from the line outward (Closest.jsx)
// How light a dot whose p is an average race's is drawn (styles.css .lg-avg)
export const AVG_A = 0.38;
// The arrow of a route's back-test: dashed, from x toward where the figure may lie (dir +1 right, higher; -1 left)
export function leanArrow(ctx, x, y, dir, len, colour, lw = 1.25) {
  ctx.save(); ctx.strokeStyle = colour; ctx.lineWidth = lw; ctx.lineCap = 'round';
  ctx.setLineDash([2.2, 2.3]); ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + dir * (len - 1), y); ctx.stroke();
  ctx.setLineDash([]); ctx.beginPath(); ctx.moveTo(x + dir * (len - 3.6), y - 3.2); ctx.lineTo(x + dir * len, y); ctx.lineTo(x + dir * (len - 3.6), y + 3.2); ctx.stroke();
  ctx.restore();
}
export const leanDir = l => (l === 'high' ? 1 : l === 'low' ? -1 : 0);
// How many of a row's contests stand past the ruler's end at this cost and reading: counted beside the row's count,
// not dropped (a safe seat's 1 in 10^19 is a true figure, $10^20, a long way past $1 trillion)
export function pastEnd(R, C, reading) {
  const lim = HI - Math.log10(C), src = reading === 'person' ? R.person : R.you;
  let s = 0;
  for (let i = 0; i < src.length; i++) if (src[i] > lim) s += R.size[i];
  return s;
}
export const pastWords = n => (n ? ` · ${n.toLocaleString('en-US')} past $1T \u203a` : '');
// The key's items for the record's two marks, only where the data carry them: each way of leaning that a row or a
// named figure carries
const DIRS = ['high', 'low'].filter(d => LEVELS.some(l => l.lean?.[d]) || ANCHORS.some(a => a.lean === d));
export const leanKey = d => (d === 'low' ? 'may be lower' : 'may be higher');
export const RECORD_KEY = [
  ...(LEVELS.some(l => l.avgCount) ? [['avg', 'an average race’s chance, not its own']] : []),
  ...DIRS.map(d => [d === 'low' ? 'lean low' : 'lean', leanKey(d)]),
];
// A row's leaning contests, beside its count: the arrow and how many carry it (in the reading "to each person", how
// many of those with a place)
export const leanCounts = (r, per) => (r.lean ? Object.entries(r.lean).map(([d, v]) => [d, per ? v.withPop : v.n]).filter(([, n]) => n) : []);
export function orderOf(rel) {
  const o = new Float32Array(rel.length), idx = Array.from(rel, (_, i) => i).sort((a, b) => rel[a] - rel[b]);
  idx.forEach((i, k) => { o[i] = idx.length > 1 ? k / (idx.length - 1) : 0; });
  return o;
}

// Each level's dots as typed arrays: `you` log10 N, `person` log10 (N ÷ population) or NaN where there is none,
// `avg` 1 where the p is an average race's, `size` the contests in the dot
export function useGroups() {
  return useMemo(() => FIELD.levels.map(l => ({
    ...LEVELS.find(L => L.id === l.id),
    you: Float32Array.from(l.g.you), person: Float32Array.from(l.g.per, x => (x == null ? NaN : x)),
    avg: Uint8Array.from(l.g.avg), size: Uint16Array.from(l.g.size),
  })), []);
}

// Row geometry: on the phone the row's name sits on its own line above its stacks; on the desktop in a column at the
// left. Under the stacks, a lane for the named figures' marks.
// A row's stacks are as tall as they need to be, up to stripH, so a level of a few dots takes a thin row and the
// levels with thousands of contests take the room (the breadth is in the heights too).
// The heights that hold words follow the reader's text size (fs, the small type's size as drawn), so at large text a
// row's name never covers its own dots.
function geometry(w, desk, fs) {
  const left = desk ? 168 : 0, right = desk ? 8 : 0, line = Math.ceil(fs * 1.4);
  return { w, left, pw: Math.max(10, w - left - right), labelH: desk ? 0 : Math.max(20, line + 3), stripH: desk ? 60 : 46, minH: desk ? Math.max(46, Math.ceil(fs * 1.25 * 1.4) + line + 6) : 0, lane: 18, gap: desk ? 10 : 8, topH: Math.max(22, line + 6), axisH: Math.max(30, line + 14), r: desk ? 3 : 2.1, fs };
}

export function Field({ C, reading, sel, onSel, desk }) {
  const wrap = useRef(null), cvs = useRef(null), costL = useRef(null);
  const rows = useGroups();
  const colours = useColours();
  const [w, setW] = useState(0), [fs, setFs] = useState(12);
  useLayoutEffect(() => {
    const ro = new ResizeObserver(() => {
      setW(Math.round(wrap.current.getBoundingClientRect().width));
      setFs(parseFloat(getComputedStyle(costL.current).fontSize) || 12);
    });
    ro.observe(wrap.current); ro.observe(costL.current);
    return () => ro.disconnect();
  }, []);
  const g = useMemo(() => geometry(w, desk, fs), [w, desk, fs]);
  // on the phone a row's name may take two lines (a long name at large text): each row's label is measured, and its
  // stacks start under it
  const labs = useRef([]);
  const [lh, setLh] = useState([]);
  useLayoutEffect(() => {
    if (desk || !w) return;
    const hs = labs.current.map(el => (el ? Math.ceil(el.getBoundingClientRect().height) + 3 : 0));
    if (hs.join() !== lh.join()) setLh(hs);
  });
  const X = lx => g.left + ((lx - LO) / SPAN) * g.pw;
  // both readings laid out at once, so a row's pitch is the same in each and only the dots move (Prices.jsx)
  const lay = useMemo(() => {
    if (!w) return null;
    let y = g.topH;
    const L = rows.map((R, ri) => {
      const you = stacks(R.you, g.pw, g.r, R.avg), person = stacks(R.person, g.pw, g.r, R.avg);
      const n = Math.max(you.rows, person.rows);
      const strip = Math.max(g.minH - g.lane, Math.min(g.stripH, n * 2 * g.r + 3));
      const top = y, base = top + (desk ? 0 : Math.max(g.labelH, lh[ri] || 0)) + strip;
      y = base + g.lane + g.gap;
      const pitch = pitchFor(n, g.r, strip - 3);
      const step = thinStep(pitch, g.r);
      return { you: you.at, person: person.at, pitch, step, live: liveOf(you.at, person.at, step), order: orderOf(R.you), top, strip, base, lane: base + g.lane / 2 + 1 };
    });
    L.end = y - g.gap;
    L.h = L.end + g.axisH;
    return L;
  }, [rows, w, g, lh.join()]);

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

  const drawRef = useRef(null);
  const draw = () => drawRef.current && drawRef.current();
  drawRef.current = () => {
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
    const r = g.r, right = g.left + g.pw;
    // how far the dots are toward the reading "to each person", on average: a dot with no population fades by it
    let mix = 0, n = 0;
    lay.forEach((L, ri) => { const M = cur.current.m[ri]; for (const i of L.live) { mix += M[i]; n++; } });
    const mm = n ? mix / n : 0;
    cur.current.mm = mm;
    lay.forEach((L, ri) => {
      const base = L.base, R = rows[ri];
      ctx.strokeStyle = colours.lineStrong; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(g.left, Math.round(base) + 0.5); ctx.lineTo(right, Math.round(base) + 0.5); ctx.stroke();
      ctx.fillStyle = colours.dot;
      const M = cur.current.m[ri], K = cur.current.k[ri];
      // the contests' own p first, then the averages, lighter; each with a place "to each person", then without (one
      // path and one fill a pass, so the 9,000 dots of the state legislatures stay inside a frame)
      for (const avg of [0, 1]) for (const has of [true, false]) {
        const al = (avg ? AVG_A : 1) * (has ? 1 : 1 - mm);
        if (al < 0.02) continue;
        ctx.globalAlpha = al; ctx.beginPath();
        for (const i of L.live) {
          if (R.avg[i] !== avg || (L.person[i] !== null) !== has) continue;
          const a = L.you[i], b = L.person[i] || a, m = has ? M[i] : 0, k = K[i];
          const x = cx0 + (a.dx + (b.dx - a.dx) * m) * k;
          const y = base - r - 1.5 - (a.k + (b.k - a.k) * m) * L.pitch * k;
          if (x > right + r || x < g.left - r) continue;
          ctx.moveTo(x + r, y); ctx.arc(x, y, r, 0, 6.2832);
        }
        ctx.fill();
      }
      ctx.globalAlpha = 1;
    });
    // the named figures: a ringed mark each in the lane under its row (Closest.jsx's marks: a ring round a dot); the one
    // in focus in the accent (R4: the accent means "you")
    const kA = cur.current.k[0]?.length ? cur.current.k[0].reduce((s, x) => s + x, 0) / cur.current.k[0].length : 1;
    // the one in focus drawn last, over a neighbour it touches
    for (const a of [...ANCHORS].sort((p, q) => (p.id === sel) - (q.id === sel))) {
      const ri = LEVELS.findIndex(L => L.id === a.level);
      const rel = Math.max(LO, Math.min(HI, Math.log10(a.N) - (a.pop ? mm * Math.log10(a.pop.value) : 0)));
      const x = cx0 + (rel / SPAN) * g.pw * kA;
      const y = lay[ri].lane;
      const on = a.id === sel, R1 = desk ? 6.5 : 6, R0 = on ? (desk ? 3.5 : 3.2) : 2.4, col = on ? colours.accent : colours.fg;
      ctx.globalAlpha = a.pop ? 1 : Math.max(0, 1 - mm);
      if (ctx.globalAlpha < 0.02) continue;
      ctx.beginPath(); ctx.arc(x, y, R1, 0, 6.2832); ctx.fillStyle = colours.bg; ctx.fill();
      ctx.lineWidth = on ? 2 : 1.25; ctx.strokeStyle = col; ctx.stroke();
      ctx.beginPath(); ctx.arc(x, y, R0, 0, 6.2832); ctx.fillStyle = col; ctx.fill();
      if (a.lean) leanArrow(ctx, x + leanDir(a.lean) * (R1 + 2.5), y, leanDir(a.lean), 13, col);
    }
    ctx.globalAlpha = 1;
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
    if (reducedMotion() || document.hidden) { lay.forEach((L, ri) => { for (const i of L.live) set(ri, i, 1); }); draw(); return; }
    const t0 = performance.now();
    const step = t => {
      const e = t - t0; let live = false;
      lay.forEach((L, ri) => {
        for (const i of L.live) {
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
      if (reading === 'person' && !a.pop) continue;
      const ri = LEVELS.findIndex(L => L.id === a.level);
      const x = X(Math.log10(C) + Math.max(LO, Math.min(HI, Math.log10(a.N) - (reading === 'person' ? Math.log10(a.pop.value) : 0)))), y = lay[ri].lane;
      const d = Math.hypot(px - x, py - y); if (d < bd) { bd = d; best = a.id; }
    }
    if (best) onSel(best);
  };

  // The scale's labels: long ones where they fit, else short; then, at large text on a narrow phone, a label that would
  // touch a kept one is left out, the dollar decades first kept and the cent last.
  const long = (g.pw * 3) / SPAN >= 96;
  // between the dollar marks, the step itself ("×1,000"), where it fits: the round-1 readers found the steps uneven
  // and unexplained, and a label on the scale says it without a sentence
  const label = p => (p % 3 === 1.5 ? '×1,000' : p === -2 ? '1¢' : long ? tick(p) : tickShort(p));
  const ticks = useMemo(() => {
    const ext = p => { const wd = label(p).length * g.fs * (p % 3 === 1.5 ? 0.5 : 0.6), x = X(p); return p === LO ? [x, x + wd] : p === HI ? [x - wd, x] : [x - wd / 2, x + wd / 2]; };
    const kept = [];
    for (const p of [0, 12, 6, 3, 9, -2, 1.5, 4.5, 7.5, 10.5]) { const [a, b] = ext(p); if (kept.every(q => { const [c, d] = ext(q); return b + 5 <= c || d + 5 <= a; })) kept.push(p); }
    return kept.sort((a, b) => a - b);
  }, [g, long]);
  return (
    <div class="field" ref={wrap} style={{ height: `${lay ? lay.h : 400}px` }}>
      <canvas ref={cvs} class="field-c" data-fit-under style={{ width: `${w}px`, height: `${lay ? lay.h : 400}px` }} role="img" onClick={pick}
        aria-label={`Every contest with a chance from ${FIELD.years[0]} to ${FIELD.years[1]}, on one scale of dollars from 1 cent to 1 trillion, in rows: ${rows.map(r => `${r.name}, ${r.count.toLocaleString('en-US')} from ${r.years[0]}`).join('; ')}. Each dot is ${UNIT} contests; a lighter dot's chance is an average race's, not its own. The named figures are ringed, and listed below.`} />
      {lay && rows.map((r, ri) => (
        <div class="field-row" ref={el => { labs.current[ri] = el; }} style={{ top: `${lay[ri].top}px`, height: desk ? `${lay[ri].base + g.lane - lay[ri].top}px` : 'auto', width: desk ? `${g.left - 16}px` : '100%' }} aria-hidden="true">
          <span class="field-n">{r.name}</span>
          <span class="field-k num"><span class="field-c-n">{reading === 'person' && r.withPop < r.count ? `${r.withPop.toLocaleString('en-US')} of ${r.count.toLocaleString('en-US')}` : r.count.toLocaleString('en-US')}</span>{leanCounts(r, reading === 'person').map(([d, n]) => <span class="field-lean" key={d}>{' · '}<span class={`lg lg-lean${d === 'low' ? ' low' : ''}`} /> {n.toLocaleString('en-US')}</span>)}{pastWords(pastEnd(r, C, reading))}</span>
        </div>
      ))}
      <span ref={costL} class="field-cost" aria-hidden="true">Your cost</span>
      <div class="field-axis" style={{ top: `${lay ? lay.end + 8 : 0}px` }} aria-hidden="true">
        {ticks.map(p => <span class={`field-t${p === LO ? ' first' : p === HI ? ' last' : ''}${p % 3 === 1.5 ? ' mid' : ''}`} style={{ left: `${X(p)}px` }}>{label(p)}</span>)}
      </div>
    </div>
  );
}
