// The field: every contest one dot on one ruler of dollars, in rows by level (design/DESIGN-SPEC.md §2.1, §2.2).
// Drawn on a canvas, every dot, so tens of thousands cost one draw; the words (row names, counts, the ruler's ticks,
// the cost's label) are text in the page, so they can be read, fitted and checked.
//
// Where a dot stands is the formula, not a layout: x = log10(B*) = log10(C) + log10(N), so the distance from the
// reader's cost to a contest is the size of N (§2.1). Motion (§4): V1 the arrival, every dot from the cost to its B*
// together (`nav-in`); V2 a new cost moves every dot by one distance (`chart`); V3 the reading "to each person"
// moves each dot by its own population (`chart`). Each is drawn frame by frame on the spring (MOTION-SPEC s.2), on
// the reader's event only; under reduced motion each is drawn at its end at once (s.5).
import { useEffect, useLayoutEffect, useMemo, useRef, useState } from 'preact/hooks';
import { sampleField } from '../data/sample.js';
import { ANCHORS, LEVELS } from '../data/real.js';
import { tween, reducedMotion } from '../lib/motion.js';
import { tick, tickShort } from '../lib/format.js';
import { useColours } from '../lib/media.js';

export const LO = -2, HI = 12;   // 1 cent to 1 trillion dollars: both readings on one ruler, so switching moves the dots, not the ruler
const BIN = 0.04;
const NB = Math.ceil((HI - LO) / BIN);

// The y of each dot inside its row, so the row's outline is its density (a sina plot): a dot sits within a band as
// wide as the share of contests near it. One array per reading.
function spread(lx, u) {
  const h = new Float32Array(NB);
  for (let i = 0; i < lx.length; i++) { const b = Math.floor((lx[i] - LO) / BIN); if (b >= 0 && b < NB) h[b]++; }
  const s = new Float32Array(NB); let max = 0;
  for (let b = 0; b < NB; b++) { let t = 0, wsum = 0; for (let d = -4; d <= 4; d++) { const j = b + d; if (j < 0 || j >= NB) continue; const w = 5 - Math.abs(d); t += h[j] * w; wsum += w; } s[b] = t / wsum; if (s[b] > max) max = s[b]; }
  const y = new Float32Array(lx.length);
  for (let i = 0; i < lx.length; i++) { const b = Math.min(NB - 1, Math.max(0, Math.floor((lx[i] - LO) / BIN))); y[i] = (u[i] - 0.5) * (0.14 + 0.86 * (max ? s[b] / max : 0)); }
  return y;
}

export function useRows() {
  return useMemo(() => {
    const f = sampleField();
    return LEVELS.map(L => {
      const d = f[L.id];
      const lxY = d.logN, lxP = new Float32Array(d.count);
      for (let i = 0; i < d.count; i++) lxP[i] = d.logN[i] - d.logPop[i];
      // positions are relative to log10(C), which moves them all alike; the spread is computed at the default cost
      // (a shift does not change it)
      const c0 = Math.log10(8.87);
      const sh = a => { const o = new Float32Array(a.length); for (let i = 0; i < a.length; i++) o[i] = a[i] + c0; return o; };
      return { ...L, count: d.count, logN: d.logN, logPop: d.logPop, yU: spread(sh(lxY), d.u), yP: spread(sh(lxP), d.u), alpha: Math.min(0.7, Math.max(0.16, 8 / Math.sqrt(d.count))) };
    });
  }, []);
}

// Row geometry: on the phone the row's name sits on its own line above its strip; on the desktop in a column at the left.
function geometry(w, desk) {
  const left = desk ? 168 : 0, right = desk ? 8 : 0;
  const labelH = desk ? 0 : 20, stripH = desk ? 46 : 30, gap = desk ? 14 : 12;
  const rowH = labelH + stripH + gap, topH = 22;
  return { w, left, pw: Math.max(10, w - left - right), labelH, stripH, gap, rowH, topH, axisH: 30, h: topH + LEVELS.length * rowH + 30 };
}

export function Field({ C, reading, sel, onSel, desk }) {
  const wrap = useRef(null), cvs = useRef(null), costL = useRef(null);
  const rows = useRows();
  const colours = useColours();
  const [w, setW] = useState(0);
  useLayoutEffect(() => {
    const ro = new ResizeObserver(e => setW(Math.round(e[0].contentRect.width)));
    ro.observe(wrap.current);
    return () => ro.disconnect();
  }, []);
  const g = useMemo(() => geometry(w, desk), [w, desk]);
  const X = lx => g.left + ((lx - LO) / (HI - LO)) * g.pw;
  // what is drawn now; tweens move it toward the target
  const cur = useRef({ lc: Math.log10(C), m: reading === 'person' ? 1 : 0, k: 0 });
  const owner = useRef({});
  const arrived = useRef(false);

  const draw = () => {
    const el = cvs.current; if (!el || !w || !colours) return;
    const dpr = Math.min(2, window.devicePixelRatio || 1);
    const H = g.h;
    if (el.width !== Math.round(w * dpr) || el.height !== Math.round(H * dpr)) { el.width = Math.round(w * dpr); el.height = Math.round(H * dpr); }
    const ctx = el.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, w, H);
    const { lc, m, k } = cur.current;
    const plotTop = g.topH - 4, plotBot = g.topH + LEVELS.length * g.rowH - g.gap;
    // the ruler's decades: a hairline each, a stronger one at each thousandfold (where the words are)
    for (let p = LO; p <= HI; p++) {
      const x = Math.round(X(p)) + 0.5;
      ctx.strokeStyle = (p % 3 === 0) ? colours.lineStrong : colours.line;
      ctx.globalAlpha = 1; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(x, plotTop); ctx.lineTo(x, plotBot + 6); ctx.stroke();
    }
    const s = desk ? 2 : 1.6;
    ctx.fillStyle = colours.dot;
    const sc = colours.dotA / 0.32;
    rows.forEach((r, ri) => {
      const top = g.topH + ri * g.rowH + g.labelH, cy = top + g.stripH / 2, hh = g.stripH - 2;
      ctx.globalAlpha = Math.min(0.9, r.alpha * sc);
      const { logN, logPop, yU, yP } = r;
      for (let i = 0; i < logN.length; i++) {
        let lx = lc + logN[i] - m * logPop[i];
        if (k < 1) lx = lc + (lx - lc) * k;
        const x = X(lx), y = cy + (yU[i] + (yP[i] - yU[i]) * m) * hh;
        ctx.fillRect(x - s / 2, y - s / 2, s, s);
      }
    });
    ctx.globalAlpha = 1;
    // the named figures: a ring each; the one in focus in the accent, larger (R4: the accent means "you")
    for (const a of ANCHORS) {
      const ri = LEVELS.findIndex(L => L.id === a.level);
      let lx = lc + Math.log10(a.N) - m * Math.log10(a.pop.value);
      if (k < 1) lx = lc + (lx - lc) * k;
      const x = X(lx), y = g.topH + ri * g.rowH + g.labelH + g.stripH / 2;
      const on = a.id === sel;
      ctx.beginPath(); ctx.arc(x, y, on ? 7 : 5, 0, Math.PI * 2);
      ctx.fillStyle = colours.bg; ctx.globalAlpha = on ? 0.9 : 0.75; ctx.fill(); ctx.globalAlpha = 1;
      ctx.lineWidth = on ? 2 : 1.25; ctx.strokeStyle = on ? colours.accent : colours.fg; ctx.stroke();
      ctx.beginPath(); ctx.arc(x, y, on ? 2.6 : 1.8, 0, Math.PI * 2); ctx.fillStyle = on ? colours.accent : colours.fg; ctx.fill();
    }
    // the reader's cost: a line through every row, in the accent; on the reading "to each person" it has no place
    // (the cost is the voter's, the stakes are each person's), so it fades as the dots move (opacity, kept under reduce)
    const cx = Math.round(X(lc)) + 0.5;
    ctx.globalAlpha = Math.max(0, 1 - m);
    ctx.strokeStyle = colours.accent; ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.moveTo(cx, plotTop); ctx.lineTo(cx, plotBot + 6); ctx.stroke();
    ctx.globalAlpha = 1;
    if (costL.current) { costL.current.style.transform = `translateX(${cx}px)`; costL.current.style.opacity = String(Math.max(0, 1 - m)); }
  };

  // the arrival (V1), once, when the field first has a width; not in a hidden tab (catch-up: MOTION-SPEC s.1)
  useEffect(() => {
    if (!w || !colours) return;
    if (!arrived.current) {
      arrived.current = true;
      if (reducedMotion() || document.hidden || cur.current.m === 1) { cur.current.k = 1; draw(); return; }
      tween(owner.current, 'nav-in', f => { cur.current.k = f; draw(); });
      return;
    }
    draw();
  }, [w, desk, colours, sel]);

  // V2 and V3: from what is drawn now to the new cost and reading
  useEffect(() => {
    if (!arrived.current) { cur.current.lc = Math.log10(C); cur.current.m = reading === 'person' ? 1 : 0; return; }
    const from = { ...cur.current }, to = { lc: Math.log10(C), m: reading === 'person' ? 1 : 0 };
    if (from.lc === to.lc && from.m === to.m) return;
    tween(owner.current, 'chart', f => { cur.current.lc = from.lc + (to.lc - from.lc) * f; cur.current.m = from.m + (to.m - from.m) * f; cur.current.k = from.k + (1 - from.k) * f; draw(); });
  }, [C, reading]);

  const pick = e => {
    const r = cvs.current.getBoundingClientRect(), px = e.clientX - r.left, py = e.clientY - r.top;
    let best = null, bd = 18;
    for (const a of ANCHORS) {
      const ri = LEVELS.findIndex(L => L.id === a.level);
      const x = X(Math.log10(C) + Math.log10(a.N) - (reading === 'person' ? Math.log10(a.pop.value) : 0)), y = g.topH + ri * g.rowH + g.labelH + g.stripH / 2;
      const d = Math.hypot(px - x, py - y); if (d < bd) { bd = d; best = a.id; }
    }
    if (best) onSel(best);
  };

  const ticks = [-2, 0, 3, 6, 9, 12];
  return (
    <div class="field" ref={wrap} style={{ height: `${g.h}px` }}>
      <canvas ref={cvs} class="field-c" data-fit-under style={{ width: `${w}px`, height: `${g.h}px` }} role="img" onClick={pick}
        aria-label={`Every contest as a dot on one scale of dollars, from 1 cent to 1 trillion, in rows: ${rows.map(r => `${r.name}, ${r.count.toLocaleString('en-US')}`).join('; ')}. These are sample contests. The named figures are listed below.`} />
      {rows.map((r, ri) => (
        <div class="field-row" style={{ top: `${g.topH + ri * g.rowH}px`, height: `${g.labelH + g.stripH}px`, width: desk ? `${g.left - 16}px` : '100%' }} aria-hidden="true">
          <span class="field-n">{r.name}</span><span class="field-k num">{r.count.toLocaleString('en-US')}</span>
        </div>
      ))}
      <span ref={costL} class="field-cost" aria-hidden="true">Your cost</span>
      <div class="field-axis" style={{ top: `${g.topH + LEVELS.length * g.rowH - g.gap + 8}px` }} aria-hidden="true">
        {ticks.map(p => <span class={`field-t${p === LO ? ' first' : p === HI ? ' last' : ''}`} style={{ left: `${X(p)}px` }}>{p === -2 ? '1¢' : (g.pw * 3) / (HI - LO) >= 96 ? tick(p) : tickShort(p)}</span>)}
      </div>
    </div>
  );
}
