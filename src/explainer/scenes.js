// The explainer's pictures, drawn on one canvas (brief X2: one visual that changes as the reader moves, so the reader
// watches the same picture become the next idea). Each scene draws a state; between two beats of one scene the state
// is mixed, so the marks move; between scenes the old picture fades out and the new one in (text never travels across
// text, MOTION-SPEC). The words on the canvas are labels on marks only, drawn at the page's small type size as the
// reader has it (read from the page, so they grow with the reader's text), and wrapped to the room they have.
//
// S = { W, H, fs, ff, col, dpr }: the box, the small type's size and family, the page's colours (lib/media.js).
import { C0, TOWN, PA, TOP08, HOUSE, PEOPLE, WORTH, CURVE } from './beats.js';
import { money } from '../lib/format.js';

const TAU = Math.PI * 2;
const lerp = (a, b, f) => a + (b - a) * f;
const clamp01 = x => Math.max(0, Math.min(1, x));
const band = (k, at, w = 0.5) => clamp01(1 - Math.abs(k - at) / w);   // 1 at `at`, 0 from `w` away

function font(ctx, S, o) { ctx.font = `${o.weight || 400} ${Math.round((o.size || 1) * S.fs)}px ${S.ff}`; }
// One label; returns its width.
export function text(ctx, S, s, x, y, o = {}) {
  font(ctx, S, o);
  ctx.fillStyle = o.color || S.col.muted;
  ctx.textAlign = o.align || 'center';
  ctx.textBaseline = o.base || 'alphabetic';
  if (o.halo) { ctx.strokeStyle = S.col.bg; ctx.lineWidth = 4; ctx.lineJoin = 'round'; ctx.strokeText(s, x, y); }
  ctx.fillText(s, x, y);
  return ctx.measureText(s).width;
}
// A label broken into lines that fit a width.
function lines(ctx, S, s, maxW, o = {}) {
  font(ctx, S, o);
  const out = []; let cur = '';
  for (const w of s.split(' ')) {
    const t = cur ? `${cur} ${w}` : w;
    if (cur && ctx.measureText(t).width > maxW) { out.push(cur); cur = w; } else cur = t;
  }
  if (cur) out.push(cur);
  return out;
}
const lineH = (S, size = 1) => size * S.fs * 1.3;
function wrap(ctx, S, s, x, y, maxW, o = {}) {
  const ls = lines(ctx, S, s, maxW, o);
  ls.forEach((l, i) => text(ctx, S, l, x, y + i * lineH(S, o.size || 1), o));
  return ls.length * lineH(S, o.size || 1);
}
// A label's centre kept inside the box, so it is never cut at an edge.
function inside(ctx, S, s, x, o = {}) { font(ctx, S, o); const w = ctx.measureText(s).width; return Math.max(w / 2 + 1, Math.min(S.W - w / 2 - 1, x)); }
// Labels on rows under a line, each on the first row where it crosses no other; a label marked `drop` is left out
// rather than given a row of its own. Returns the rows used.
function rowsOf(ctx, S, items, y, o = {}) {
  const rows = [], lh = lineH(S, o.size || 1), gap = 8;
  for (const it of items) {
    font(ctx, S, { ...o, ...it });
    const w = ctx.measureText(it.s).width, x = inside(ctx, S, it.s, it.x, { ...o, ...it }), a = x - w / 2 - gap / 2, b = x + w / 2 + gap / 2;
    let r = 0;
    while (rows[r] && rows[r].some(([p, q]) => a < q && b > p)) r++;
    if (it.drop && r >= it.drop) continue;
    (rows[r] || (rows[r] = [])).push([a, b]);
    text(ctx, S, it.s, x, y + r * lh, { ...o, ...it });
  }
  return rows.length;
}
// Many dots of one colour in one path and one fill: a picture of thousands of dots drawn each frame of a scroll stays
// inside a frame's time on a slow phone (the motion check, 4x slowed).
function dots(ctx, pts, r, c) {
  if (!pts.length) return;
  ctx.fillStyle = c; ctx.beginPath();
  for (let i = 0; i < pts.length; i += 2) { ctx.moveTo(pts[i] + r, pts[i + 1]); ctx.arc(pts[i], pts[i + 1], r, 0, TAU); }
  ctx.fill();
}
function dot(ctx, x, y, r, c) { ctx.fillStyle = c; ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.fill(); }
function ring(ctx, x, y, r, c, w = 1.6) { ctx.strokeStyle = c; ctx.lineWidth = w; ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.stroke(); }
function half(ctx, x, y, r, c, side) {   // side −1: the left half, +1: the right
  ctx.fillStyle = c; ctx.beginPath();
  if (side < 0) ctx.arc(x, y, r, Math.PI / 2, Math.PI * 1.5); else ctx.arc(x, y, r, -Math.PI / 2, Math.PI / 2);
  ctx.closePath(); ctx.fill();
}
let tile = null;
function stipple(ctx, colour, dpr) {   // a point every 3 px, for a field too fine to draw dot by dot
  const k = `${colour}|${dpr}`;
  if (tile && tile.k === k) return tile.p;
  const n = Math.round(3 * dpr), c = document.createElement('canvas'); c.width = n; c.height = n;
  const x = c.getContext('2d'); x.fillStyle = colour; x.fillRect(0, 0, Math.max(1, Math.round(1.4 * dpr)), Math.max(1, Math.round(1.4 * dpr)));
  tile = { k, p: ctx.createPattern(c, 'repeat') };
  return tile.p;
}
// A grid of square dots as one fill: one cell, scaled to the grid's pitch, repeated. A field of thousands of dots in
// motion is drawn this way in one call, where a dot at a time dropped frames on the slow-phone check (M-motion s.4,
// rule 11: no gap over 50 ms at 4x slower CPU).
let cell = null;
function gridFill(ctx, colour, x0, y0, pitch) {
  if (!cell || cell.colour !== colour) {
    const c = document.createElement('canvas'); c.width = c.height = 20;
    const x = c.getContext('2d'); x.fillStyle = colour; x.fillRect(4.5, 4.5, 11, 11);   // 0.55 of the cell, centred
    cell = { colour, p: ctx.createPattern(c, 'repeat') };
  }
  const k = pitch / 20;
  cell.p.setTransform(new DOMMatrix([k, 0, 0, k, x0, y0]));
  return cell.p;
}
function stippleRect(ctx, S, x, y, w, h) {
  ctx.fillStyle = stipple(ctx, S.col.dot, S.dpr);
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.fillRect(Math.round(x * S.dpr), Math.round(y * S.dpr), Math.round(w * S.dpr), Math.round(h * S.dpr));
  ctx.restore();
}
// The same, under a turned frame (the seesaw's beam): the tile kept at 3 px of the screen.
function stippleTurned(ctx, S, x, y, w, h) {
  const p = stipple(ctx, S.col.dot, S.dpr);
  p.setTransform(new DOMMatrix([1 / S.dpr, 0, 0, 1 / S.dpr, 0, 0]));
  ctx.fillStyle = p; ctx.fillRect(x, y, w, h);
  p.setTransform(new DOMMatrix());
}

// ---- 1. two worlds: the town's 2,000 ballots twice; yours counted in one, not in the other -----------------------
// The 2,000 ballots are drawn once into a grid of each colour, at the screen's pixels, and each frame shows the part of
// each grid its side holds: 4,000 dots a frame are one copy each, so the first step's move keeps inside a frame on a slow
// phone (the motion check, 4x slowed: drawn dot by dot, the first frame after the tap ran past 50 ms).
// Each grid is drawn at its panel's own fraction of a pixel and copied at the whole pixel, so every dot falls on the
// screen's pixels exactly as when it was drawn dot by dot.
const GRIDS = [];
function grids(S, p, x, y, cols, rows, pitch, r) {
  const dx = x * S.dpr, dy = y * S.dpr, fx = dx - Math.floor(dx), fy = dy - Math.floor(dy);
  const key = [S.dpr, fx, fy, cols, rows, pitch, r, S.col.fg, S.col.dot].join();
  const c = GRIDS[p] || (GRIDS[p] = {});
  if (c.key !== key) {
    const w = Math.ceil(cols * pitch * S.dpr + 1), h = Math.ceil(rows * pitch * S.dpr + 1);
    const one = colour => {
      const el = document.createElement('canvas'); el.width = w; el.height = h;
      const g = el.getContext('2d'); g.setTransform(S.dpr, 0, 0, S.dpr, fx, fy);
      const pts = [];
      for (let k = 0; k < cols * rows; k++) pts.push(((k % cols) + 0.5) * pitch, (Math.floor(k / cols) + 0.5) * pitch);
      dots(g, pts, r, colour);
      return el;
    };
    Object.assign(c, { key, a: one(S.col.fg), b: one(S.col.dot) });
  }
  // where to copy them: the whole pixel, in the page's units
  return [c.a, c.b, Math.floor(dx) / S.dpr, Math.floor(dy) / S.dpr];
}
function worlds(ctx, S, st) {
  const { W, H, col, fs } = S;
  const gap = Math.max(14, W * 0.05), pw = (W - gap) / 2, cols = 40, rows = 50;
  const ours = Math.round(lerp(1040, 1000, st.k));   // your side's ballots, yours among them
  const me = Math.floor((ours - 1) / cols) * cols + cols / 2;   // yours: in the middle of your side's last row
  const close = st.k >= 0.5;
  const tally = [[`${(ours).toLocaleString('en-US')}`, `to ${(2000 - ours).toLocaleString('en-US')}`], [`${(ours - 1).toLocaleString('en-US')}`, `to ${(2000 - ours).toLocaleString('en-US')}`]];
  const who = close ? ['a tie: a coin toss', 'the other side wins'] : ['your side wins', 'your side wins'];
  // the words first, each wrapped to its block's width: the titles, and the counts and winners under the blocks
  const titles = ['Counted', 'Not counted'].map(t => lines(ctx, S, t, pw, { weight: 600 }));
  const tl = tally.map(([a, b]) => (lines(ctx, S, `${a} ${b}`, pw, { weight: 600, size: 1.15 }).length > 1 ? [a, b] : [`${a} ${b}`]));
  const wl = who.map(t => lines(ctx, S, t, pw));
  const top = Math.max(...titles.map(t => t.length)) * lineH(S) + 6;
  const bottom = Math.max(...tl.map(t => t.length)) * lineH(S, 1.15) + Math.max(...wl.map(t => t.length)) * lineH(S) + 10;
  const pitch = Math.min(pw / cols, (H - top - bottom) / rows), r = Math.max(0.8, pitch * 0.36);
  const gw = cols * pitch, gh = rows * pitch;
  const y0 = Math.max(0, (H - (top + gh + bottom)) / 2);
  for (let p = 0; p < 2; p++) {
    const x0 = p * (pw + gap) + (pw - gw) / 2, cx = p * (pw + gap) + pw / 2;
    titles[p].forEach((t, i) => text(ctx, S, t, cx, y0 + fs + i * lineH(S), { weight: 600, color: col.fg }));
    // the ballots: your side's, the first `ours`, from the dark grid, and the rest from the grey, each cut at the
    // boundary between two dots (yours is drawn over its place below)
    const gx = x0, gy = y0 + top, full = Math.floor(ours / cols), part = ours % cols;
    const [ga, gb, cx0, cy0] = grids(S, p, gx, gy, cols, rows, pitch, r);
    ctx.save(); ctx.beginPath(); ctx.rect(gx - 1, gy - 1, gw + 2, full * pitch + 1); ctx.rect(gx - 1, gy + full * pitch, part * pitch + 1, pitch);
    ctx.clip(); ctx.globalAlpha = 0.9; ctx.drawImage(ga, cx0, cy0, ga.width / S.dpr, ga.height / S.dpr); ctx.restore();
    ctx.save(); ctx.beginPath(); ctx.rect(gx + part * pitch, gy + full * pitch, (cols - part) * pitch + 1, pitch); ctx.rect(gx - 1, gy + (full + 1) * pitch, gw + 2, (rows - full - 1) * pitch + 1);
    ctx.clip(); ctx.globalAlpha = 0.75; ctx.drawImage(gb, cx0, cy0, gb.width / S.dpr, gb.height / S.dpr); ctx.restore();
    ctx.globalAlpha = 1;
    const mx = x0 + ((me % cols) + 0.5) * pitch, my = y0 + top + (Math.floor(me / cols) + 0.5) * pitch, rr = Math.max(7, r * 3.6);
    if (p === 0) dot(ctx, mx, my, Math.max(2.5, r * 1.5), col.accent);
    else dot(ctx, mx, my, rr - 1, col.bg);
    ring(ctx, mx, my, rr, col.accent, 2);
    let y = y0 + top + gh + 6 + fs * 1.15;
    tl[p].forEach(t => { text(ctx, S, t, cx, y, { weight: 600, color: col.fg, size: 1.15 }); y += lineH(S, 1.15); });
    // the winners, the one that differs in the accent: the change your ballot makes
    wl[p].forEach(t => { text(ctx, S, t, cx, y, { color: close ? (p === 0 ? col.fg : col.accent) : col.muted, weight: close ? 600 : 400 }); y += lineH(S); });
  }
}

// ---- 2 and 3. everyone else's count, and the two where your ballot changes who wins ------------------------------
// Each column is one count of everyone else, by your side's lead among them. Each dot is who wins: your side (dark),
// theirs (grey), or a tie (half each), settled by lot. Counted, your ballot adds one to your side's lead.
const AXIS_M = 'your side’s lead, not counting you';
function margins(ctx, S, st) {
  const { W, H, col, fs } = S;
  const M = [-3, -2, -1, 0, 1, 2, 3], cw = W / M.length;
  const lab = lineH(S) + 4, numH = lineH(S) + 4, axisH = lines(ctx, S, AXIS_M, W - 4).length * lineH(S);
  // the words' room first, then the dots in what is left: two rows, and the joined dot below
  const words = lab * 2 + numH + axisH + 30;
  const r = Math.max(5, Math.min(cw * 0.34, fs * 1.25, (H - words) / 6.6));
  const used = words + 6.6 * r, y0 = Math.max(0, (H - used) / 2);
  const y1 = y0 + lab + r + 4, y2 = y1 + r + 10 + lab + r;
  const win = m => (m > 0 ? 'yours' : m < 0 ? 'theirs' : 'tie');
  const mark = (x, y, who, a) => {
    ctx.globalAlpha = a;
    if (who === 'tie') { half(ctx, x, y, r, col.fg, -1); half(ctx, x, y, r, col.dot, 1); } else dot(ctx, x, y, r, who === 'yours' ? col.fg : col.dot);
    ctx.globalAlpha = 1;
  };
  text(ctx, S, 'Counted', 2, y1 - r - 8, { align: 'left', weight: 600, color: col.fg });
  text(ctx, S, 'Not counted', 2, y2 - r - 8, { align: 'left', weight: 600, color: col.fg });
  const fade = 1 - 0.6 * st.hl;
  M.forEach((m, j) => {
    const x = j * cw + cw / 2, key = m === 0 || m === -1;
    mark(x, y1, win(m + 1), 1);
    mark(x, y2, win(m), 1);
    ctx.globalAlpha = key ? 1 : fade;
    text(ctx, S, m > 0 ? `+${m}` : m < 0 ? `−${-m}` : '0', x, y2 + r + fs * 1.3, { color: key ? col.fg : col.muted, weight: key ? 600 : 400 });
    ctx.globalAlpha = 1;
  });
  const axisY = y2 + r + numH + fs;
  wrap(ctx, S, AXIS_M, W / 2, axisY, W - 4);
  // the two counts where the rows differ: a tie, and one short
  if (st.hl > 0) {
    ctx.globalAlpha = st.hl; ctx.strokeStyle = col.accent; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.roundRect(2 * cw + 3, y1 - r - 6, 2 * cw - 6, y2 - y1 + 2 * r + 12, 8); ctx.stroke();
    ctx.globalAlpha = 1;
  }
  // what your ballot changes in each: half a win (a tie it makes, which the lot gives your side half the time; a tie
  // it breaks, which the lot gave the other side half the time). The halves are lit, then join below into one.
  if (st.join > 0) {
    const a = clamp01(st.join * 2), j = clamp01(st.join * 2 - 1);
    const c1 = 2 * cw + cw / 2, c2 = 3 * cw + cw / 2, mid = (c1 + c2) / 2;
    const yj = Math.min(H - r - 2, axisY + axisH + r);
    ctx.globalAlpha = a;
    half(ctx, c1, y1, r, col.accent, -1);
    half(ctx, c2, y1, r, col.accent, 1);
    if (j > 0) {
      // the halves' paths, dashed, so a still picture shows where the whole came from
      ctx.globalAlpha = j * 0.7; ctx.strokeStyle = col.accent; ctx.lineWidth = 1.2; ctx.setLineDash([3, 4]);
      ctx.beginPath(); ctx.moveTo(c1 - r * 0.5, y1 + r + 3); ctx.lineTo(lerp(c1, mid, j) - r * 0.5, lerp(y1, yj, j) - r - 3);
      ctx.moveTo(c2 + r * 0.5, y1 + r + 3); ctx.lineTo(lerp(c2, mid, j) + r * 0.5, lerp(y1, yj, j) - r - 3); ctx.stroke(); ctx.setLineDash([]);
      ctx.globalAlpha = 1; wrap(ctx, S, AXIS_M, W / 2, axisY, W - 4, { halo: true });
      ctx.globalAlpha = j;
      half(ctx, lerp(c1, mid, j), lerp(y1, yj, j), r, col.accent, -1);
      half(ctx, lerp(c2, mid, j), lerp(y1, yj, j), r, col.accent, 1);
      ctx.globalAlpha = clamp01(j * 3 - 2);
      const t = '= one change', lx = mid + r + 8;
      font(ctx, S, { weight: 600 });
      if (lx + ctx.measureText(t).width <= W) text(ctx, S, t, lx, yj, { align: 'left', base: 'middle', color: col.accent, weight: 600 });
      else if (yj + r + 3 + fs * 1.15 <= H) text(ctx, S, t, inside(ctx, S, t, mid, { weight: 600 }), yj + r + 3, { base: 'top', color: col.accent, weight: 600, halo: true });
    }
    ctx.globalAlpha = 1;
  }
}

// ---- 4. the forecast: the chance of each exact count of your side's votes. At 50–50 it is the chance of a tie or one
// short; half of it (the tie's lot) is the chance your ballot changes who wins. More voters spread the same forecast
// over more counts, so each is lower; a forecast off even leaves little at 50–50; a less sure one spreads it out.
const pdf = (x, mu, sd) => Math.exp(-0.5 * ((x - mu) / sd) ** 2) / (sd * Math.sqrt(TAU));
const Y_MAX = 11 / 2000;
const AXIS_C = 'your side’s share of the vote, as forecast';
function curve(ctx, S, st, beat) {
  const { W, H, col, fs } = S;
  const axisH = lines(ctx, S, AXIS_C, W - 4).length * lineH(S);
  const lo = 0.3, hi = 0.7, top = fs * 1.6, base = H - (lineH(S) + 13 + axisH), ph = base - top;
  const X = v => ((v - lo) / (hi - lo)) * W, Y = d => base - (Math.min(d, Y_MAX * 1.02) / Y_MAX) * ph;
  const at = v => pdf(v, st.mu, st.sd) / st.n;
  const path = (f = at) => { for (let i = 0; i <= 240; i++) { const v = lo + ((hi - lo) * i) / 240; i ? ctx.lineTo(X(v), Y(f(v))) : ctx.moveTo(X(v), Y(f(v))); } };
  // the first forecast, dashed, while another is shown: what changed is seen against it
  const B0 = CURVE.base, at0 = v => pdf(v, B0.mu, B0.sd) / B0.n;
  const away = Math.abs(Math.log(st.n / B0.n)) + Math.abs(st.mu - B0.mu) * 40 + Math.abs(st.sd - B0.sd) * 40;
  if (away > 0.01) {
    ctx.globalAlpha = Math.min(1, away * 3) * 0.8; ctx.strokeStyle = col.muted; ctx.lineWidth = 1.2; ctx.setLineDash([4, 4]);
    ctx.beginPath(); path(at0); ctx.stroke(); ctx.setLineDash([]); ctx.globalAlpha = 1;
  }
  // what the height is: named at the top, over its arrow
  ctx.strokeStyle = col.muted; ctx.fillStyle = col.muted; ctx.lineWidth = 1;
  ctx.beginPath(); ctx.moveTo(4, base - 4); ctx.lineTo(4, top - fs * 0.2); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(4, top - fs * 0.6); ctx.lineTo(0.5, top); ctx.lineTo(7.5, top); ctx.closePath(); ctx.fill();
  text(ctx, S, 'how likely', 12, top - fs * 0.15, { align: 'left', size: 0.92, halo: true });
  ctx.beginPath(); path(); ctx.lineTo(W, base); ctx.lineTo(0, base); ctx.closePath();
  ctx.fillStyle = col.dot; ctx.globalAlpha = 0.25; ctx.fill(); ctx.globalAlpha = 1;
  ctx.beginPath(); path(); ctx.strokeStyle = col.fg; ctx.lineWidth = 1.5; ctx.stroke();
  ctx.fillStyle = col.lineStrong; ctx.fillRect(0, base, W, 1);
  // the give or take: the forecast's width, a bracket across the curve from one give or take below its centre to one
  // above, while the curve stands high enough to hold it
  const pk0 = at(st.mu), gA = clamp01(((base - Y(pk0)) / ph - 0.25) * 5);
  if (gA > 0) {
    const g1 = X(st.mu - st.sd), g2 = X(st.mu + st.sd), gy = Y(at(st.mu + st.sd));
    ctx.globalAlpha = gA; ctx.strokeStyle = col.fg; ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.moveTo(g1, gy); ctx.lineTo(g2, gy); ctx.moveTo(g1, gy - 4); ctx.lineTo(g1, gy + 4); ctx.moveTo(g2, gy - 4); ctx.lineTo(g2, gy + 4); ctx.stroke();
    ctx.globalAlpha = 1;
  }
  // the bar at 50–50: its outline the chance of a tie or one short, its filled half the chance your ballot changes
  // who wins
  const h = at(0.5), bw = Math.max(8, fs * 0.65), x = X(0.5), yT = Y(h), yH = Y(h / 2);
  ctx.fillStyle = col.accent; ctx.fillRect(x - bw / 2, yH, bw, base - yH);
  if (base - yT > 3) { ctx.strokeStyle = col.accent; ctx.lineWidth = 1.2; ctx.strokeRect(x - bw / 2 + 0.6, yT + 0.6, bw - 1.2, base - yT - 1.2); }
  // too small to see: a mark under the axis points to it
  if (base - yT < 5) { ctx.fillStyle = col.accent; ctx.beginPath(); ctx.moveTo(x, base + 2); ctx.lineTo(x - 5, base + 9); ctx.lineTo(x + 5, base + 9); ctx.closePath(); ctx.fill(); }
  // the outline named at its top, where there is room beside the curve
  if (base - yT > fs * 2.4) {
    const t = 'a tie or one short';
    font(ctx, S, { size: 0.92 });
    if (x - bw / 2 - 6 - ctx.measureText(t).width >= 0) text(ctx, S, t, x - bw / 2 - 6, yT + fs * 0.4, { align: 'right', base: 'middle', size: 0.92, color: col.accent, halo: true });
  }
  // the forecast's centre, named at the curve's top, while the curve stands high enough to hold it
  const pk = at(st.mu);
  if (base - Y(pk) > ph * 0.35 && Math.abs(X(st.mu) - x) > fs * 3) text(ctx, S, `${Math.round(st.mu * 100)}%`, X(st.mu), Y(pk) - 6, { size: 0.92, color: col.fg, weight: 600, halo: true });
  if (beat.figIn) {
    font(ctx, S, { weight: 600, size: 1.1 });
    // beside the bar, on the right, or the left; where neither has room, over the bar
    const lw = ctx.measureText(beat.figIn).width, o = { base: 'middle', color: col.accent, weight: 600, size: 1.1, halo: true }, ly = Math.min(base - fs * 0.75, yH);
    if (x + bw / 2 + 6 + lw <= W) text(ctx, S, beat.figIn, x + bw / 2 + 6, ly, { ...o, align: 'left' });
    else if (x - bw / 2 - 6 - lw >= 0) text(ctx, S, beat.figIn, x - bw / 2 - 6, ly, { ...o, align: 'right' });
    else text(ctx, S, beat.figIn, inside(ctx, S, beat.figIn, x, o), Math.min(ly, yT) - fs * 1.1, o);
  }
  for (const [v, t] of [[0.4, '40%'], [0.5, '50–50'], [0.6, '60%']]) text(ctx, S, t, X(v), base + 9 + fs, { color: v === 0.5 ? col.accent : col.muted, weight: v === 0.5 ? 600 : 400 });
  wrap(ctx, S, AXIS_C, W / 2, base + 11 + fs + lineH(S), W - 4);
}

// ---- 5. a field of runs of the election, one dot for each; the ringed one is a run your ballot decides ----------
// A square of n runs, side D, centred at (cx, cy); `inner` outlines the smaller fields inside it.
function fieldOf(ctx, S, n, cx, cy, D, inner = []) {
  const { col } = S;
  const side = Math.sqrt(n), pitch = D / side;
  if (pitch >= 2.5) {
    const cols = Math.ceil(side), rows = Math.ceil(n / cols), x0 = cx - (cols * pitch) / 2, y0 = cy - (rows * pitch) / 2, s = Math.max(1, pitch * 0.55);
    ctx.globalAlpha = 0.75; ctx.fillStyle = col.dot;
    if (pitch > 7) {
      const pts = [];
      for (let k = 0; k < n; k++) pts.push(x0 + ((k % cols) + 0.5) * pitch, y0 + (Math.floor(k / cols) + 0.5) * pitch);
      dots(ctx, pts, s / 2, col.dot);
    } else {
      // full rows, then the last row's part
      const m = Math.round(n), full = Math.floor(m / cols), rest = m - full * cols;
      ctx.fillStyle = gridFill(ctx, col.dot, x0, y0, pitch);
      ctx.fillRect(x0, y0, cols * pitch, full * pitch);
      if (rest > 0) ctx.fillRect(x0, y0 + full * pitch, rest * pitch, pitch);
    }
  } else { ctx.globalAlpha = 0.6; stippleRect(ctx, S, cx - D / 2, cy - D / 2, D, D); }
  ctx.globalAlpha = 1;
  ctx.strokeStyle = col.fg; ctx.lineWidth = 1.2;
  for (const N of inner) { const sd = Math.sqrt(N) * pitch; if (sd < D - 1 && sd >= 5) ctx.strokeRect(Math.round(cx - sd / 2) + 0.5, Math.round(cy - sd / 2) + 0.5, Math.round(sd), Math.round(sd)); }
  dot(ctx, cx, cy, Math.max(2.5, Math.min(6, pitch * 0.3)), col.accent);
  ring(ctx, cx, cy, Math.max(9, pitch * 0.6), col.accent, 2);
}
function field(ctx, S, st) {
  const D = Math.min(S.W, S.H) - 4;
  fieldOf(ctx, S, 10 ** (2 * st.ls), S.W / 2, S.H / 2, D, [TOWN.N]);
}

// ---- 6. the presidency in two steps: your ballot changes your state's winner; then, of those runs, the state's
// electoral votes decide the College in 19 of 100; both together, the larger field ---------------------------------
function stages(ctx, S, st) {
  const { W, H, col, fs } = S;
  const g = clamp01(st.k), b = clamp01(st.k - 1);
  // the field's size is the count of runs: both steps' 7.5 million fill the box; step one's 1.4 million take less
  const n = Math.exp(lerp(Math.log(PA.state), Math.log(PA.N), b)), D = Math.min(W * 0.62, H - 4) * Math.sqrt(n / PA.N);
  const cx = lerp(lerp(W / 2, D / 2 + 2, g), W / 2, b), cy = H / 2;
  fieldOf(ctx, S, n, cx, cy, D, []);
  const a = g * (1 - b);
  if (a > 0) {
    const room = W - D - 4, gw = Math.max(40, Math.min(room - fs * 1.6, H - 8)), p = gw / 10, x0 = W - gw, y0 = cy - gw / 2;
    ctx.globalAlpha = a;
    const lit = [], not = [];
    for (let i = 0; i < 100; i++) (i < 19 ? lit : not).push(x0 + ((i % 10) + 0.5) * p, y0 + (Math.floor(i / 10) + 0.5) * p);
    dots(ctx, lit, p * 0.33, col.accent); dots(ctx, not, p * 0.33, col.dot);
    // the arrow from the ringed run to the hundred
    ctx.strokeStyle = col.accent; ctx.fillStyle = col.accent; ctx.lineWidth = 1.6;
    const ax = cx + 12, bx = x0 - 4;
    ctx.beginPath(); ctx.moveTo(ax, cy); ctx.lineTo(bx - 6, cy); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(bx, cy); ctx.lineTo(bx - 7, cy - 4); ctx.lineTo(bx - 7, cy + 4); ctx.closePath(); ctx.fill();
    ctx.globalAlpha = 1;
  }
}

// ---- 7. the stakes: a trip in every run; weighed against the result; the presidency; shared by everyone; the scale
// k 0: the 468 runs, each a trip of $8.87, the one your ballot decides ringed.
// k 1, 2, 3: a seesaw: the trips heaped on one end, the result your ballot decides on the other, worth $1,000, then
//   $10,000 to you (examples); then the presidency's 10 million trips against the same $10,000. The heavier end goes
//   down: the trips' end, it does not pay; the result's end, it pays.
// k 4: the presidency's $89 million shared by the country's 304 million people of 2008: 29¢ each.
// k 5: the scale of dollars of the first page: your cost, × 468 and × 10 million.
const LO = -2, HI = 12;
// the beam's turn: up at the result's end when the trips weigh more (a > 0), down when the result does
const turn = (cost, worth) => Math.max(-0.24, Math.min(0.24, 0.32 * (Math.log10(cost) - Math.log10(worth))));
function trips(ctx, S, st) {
  const { W, H, col, fs } = S;
  const k = st.k, m = clamp01(k);                    // 0: the grid; 1: the trips on the seesaw
  const T1 = C0 * TOWN.N, T2 = C0 * TOP08, ME = 9 * 26 + 13;
  if (k < 4.5) {
    const tA = k <= 4 ? 1 : clamp01(1 - (k - 4) * 2), ev = clamp01(k - 3);   // ev: everyone's stakes on the right
    const balA = tA * clamp01(k * 1.5 - 0.5);
    const cols = 26, rows = 18, gp = Math.min((W - 8) / cols, (H - 8) / rows), gx = (W - cols * gp) / 2, gy = (H - rows * gp) / 2;
    // the seesaw: the beam turns with the reader from one weighing to the next
    const pivX = W / 2, pivY = H * 0.6, arm = Math.min(W * 0.44, H * 0.9), standH = Math.min(H * 0.22, H - pivY - lineH(S) - 6);
    let a = turn(T1, WORTH.lo);
    if (k > 1) a = lerp(a, turn(T1, WORTH.hi), clamp01(k - 1));
    if (k > 2) a = lerp(turn(T1, WORTH.hi), turn(T2, WORTH.hi), clamp01(k - 2));
    if (k > 3) a = lerp(turn(T2, WORTH.hi), 0, ev);   // 304 million people at 29¢ each weigh what 10 million trips do
    a *= m;
    const u = [Math.cos(a), -Math.sin(a)], nv = [-Math.sin(a), -Math.cos(a)];   // along the beam, and up from it
    const L = [pivX - arm * u[0], pivY - arm * u[1]], R = [pivX + arm * u[0], pivY + arm * u[1]];
    const at = (P, s, h) => [P[0] + s * u[0] + h * nv[0], P[1] + s * u[1] + h * nv[1]];
    if (balA > 0) {
      ctx.globalAlpha = balA;
      ctx.fillStyle = col.lineStrong;
      ctx.beginPath(); ctx.moveTo(pivX, pivY); ctx.lineTo(pivX - standH * 0.45, pivY + standH); ctx.lineTo(pivX + standH * 0.45, pivY + standH); ctx.closePath(); ctx.fill();
      ctx.strokeStyle = col.fg; ctx.lineWidth = 3; ctx.lineCap = 'round';
      ctx.beginPath(); ctx.moveTo(L[0], L[1]); ctx.lineTo(R[0], R[1]); ctx.stroke(); ctx.lineCap = 'butt';
      ctx.globalAlpha = 1;
    }
    // the trips: from the grid to a heap on the beam's left end; for the presidency, a block standing for 10 million
    const heapW = arm * 0.78, hp = Math.max(2.6, Math.min(gp * 0.7, heapW / 26)), hc = Math.max(1, Math.floor(heapW / hp)), big = clamp01(k - 2);
    const s0 = arm * 0.08;   // the heap's left edge, in from the beam's end
    const pts = [];
    for (let i = 0; i < TOWN.N; i++) {
      if (i === ME) continue;
      const gxI = gx + ((i % cols) + 0.5) * gp, gyI = gy + (Math.floor(i / cols) + 0.5) * gp;
      const [hx, hy] = at(L, s0 + ((i % hc) + 0.5) * hp, 2.5 + (Math.floor(i / hc) + 0.5) * hp);
      pts.push(lerp(gxI, hx, m), lerp(gyI, hy, m));
    }
    ctx.globalAlpha = tA * (1 - big);
    if (ctx.globalAlpha > 0) dots(ctx, pts, lerp(gp * 0.34, hp * 0.4, m), col.dot);
    if (big > 0) {
      const bh = lerp(Math.ceil(TOWN.N / hc) * hp, Math.min(pivY * 0.95, arm * 0.9), big), bw = lerp(hc * hp, heapW, big);
      ctx.save(); ctx.globalAlpha = tA * big * 0.8;
      ctx.translate(L[0], L[1]); ctx.rotate(-a);
      stippleTurned(ctx, S, s0, -2.5 - bh, bw, bh);
      ctx.restore();
    }
    // the run your ballot decides: from the grid to the beam's right end, where it stands for the result
    const g0 = [gx + ((ME % cols) + 0.5) * gp, gy + (Math.floor(ME / cols) + 0.5) * gp], e = at(R, -arm * 0.2, 13);
    const ox = lerp(g0[0], e[0], m), oy = lerp(g0[1], e[1], m);
    ctx.globalAlpha = tA * (1 - ev);
    dot(ctx, ox, oy, lerp(gp * 0.34, 5.5, m), col.accent);
    ring(ctx, ox, oy, lerp(Math.max(7, gp * 0.9), 10.5, m), col.accent, 2);
    // everyone's stakes: a dot for each million people, at 29¢ each, on the right end in its place
    if (ev > 0) {
      const pc = 20, pp = heapW / pc, pts = [];
      for (let i = 0; i < Math.round(PEOPLE / 1e6); i++) pts.push(...at(R, -s0 - heapW + ((i % pc) + 0.5) * pp, 2.5 + (Math.floor(i / pc) + 0.5) * pp));
      ctx.globalAlpha = tA * ev; dots(ctx, pts, pp * 0.32, col.fg);
    }
    // the two ends' figures, under the beam, each on a row of its own where they would cross
    if (m > 0.5) {
      ctx.globalAlpha = tA * clamp01(m * 2 - 1);
      const lx = at(L, s0 + heapW / 2, 0), rx = at(R, -arm * 0.2, 0);
      const ly = Math.max(lx[1], rx[1]) + lineH(S) + 4;
      const wl = k > 3.5 ? `${Math.round(PEOPLE / 1e6)} million × ${money(T2 / PEOPLE)}` : k > 1.5 ? money(WORTH.hi) : money(WORTH.lo);
      rowsOf(ctx, S, [{ s: k > 2.5 ? money(T2) : money(T1), x: lx[0], color: col.fg }, { s: wl, x: rx[0], color: k > 3.5 ? col.fg : col.accent }], ly, { weight: 600 });
      // the level beam, named over its pivot: the two ends weigh the same
      const lv = 'level: they weigh the same';
      if (ev > 0.5) { ctx.globalAlpha = tA * clamp01(ev * 2 - 1); wrap(ctx, S, lv, W / 2, fs * 1.2, W - 8, { color: col.accent, weight: 600, halo: true }); }
    }
    ctx.globalAlpha = 1;
  }
  // the scale of dollars: your cost, × 468 and × 10 million
  const rA = clamp01((k - 4.5) * 2);
  if (rA > 0) {
    ctx.globalAlpha = rA;
    const pad = Math.max(24, fs * 2.4), X = lx => pad + ((lx - LO) / (HI - LO)) * (W - 2 * pad), y = H * 0.55;
    ctx.fillStyle = col.lineStrong; ctx.fillRect(0, y, W, 1);
    const ticks = [[0, '$1'], [3, '$1,000'], [6, '$1 million'], [9, '$1 billion']];
    for (const [p] of ticks) ctx.fillRect(X(p), y - 3, 1, 7);
    const c = Math.log10(C0), t1 = c + Math.log10(TOWN.N), t2 = c + Math.log10(TOP08);
    const arrow = (x1, x2, yy, label) => {
      ctx.strokeStyle = col.accent; ctx.fillStyle = col.accent; ctx.lineWidth = 2.5;
      ctx.beginPath(); ctx.moveTo(x1, yy); ctx.lineTo(x2 - 8, yy); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(x2, yy); ctx.lineTo(x2 - 10, yy - 5.5); ctx.lineTo(x2 - 10, yy + 5.5); ctx.closePath(); ctx.fill();
      text(ctx, S, label, inside(ctx, S, label, (x1 + x2) / 2, { weight: 600, size: 1.1 }), yy - 8, { color: col.accent, weight: 600, size: 1.1 });
    };
    arrow(X(c), X(t1), y - lineH(S, 1.1) * 1.6, '× 468');
    arrow(X(c), X(t2), y - lineH(S, 1.1) * 3.4, '× 10 million');
    dot(ctx, X(c), y, 5.5, col.accent);
    for (const t of [t1, t2]) { dot(ctx, X(t), y, 6, col.bg); ring(ctx, X(t), y, 6, col.fg, 2.2); }
    // the figures under their marks, then the scale's steps on the row below, each left out where it would cross
    const used = rowsOf(ctx, S, [
      { s: '$8.87', x: X(c), color: col.accent }, { s: '$4,150', x: X(t1), color: col.fg }, { s: '$89 million', x: X(t2), color: col.fg },
    ], y + 6 + fs * 1.1, { weight: 600, size: 1.1 });
    rowsOf(ctx, S, ticks.map(([p, t]) => ({ s: t, x: X(p), drop: 1 })), y + 10 + used * lineH(S, 1.1) + fs, { size: 0.9 });
    ctx.globalAlpha = 1;
  }
}

// ---- 8. one trip, the whole ballot: one trip on one end; on the other, what each race repays of it, the race's worth
// to you ÷ its N. The races arrive one at a time (n); the beam tips when together they outweigh the trip.
// An example: the presidency worth $50 million to you (2008, where the chance was highest, 1 in 10 million): $5.00 a trip; a House
// race worth $400,000 (the average race, 1 in 180,000): $2.22; the town race worth $1,000 (1 in 468): $2.14.
// Alone none pays; together, $9.36 against $8.87.
export const EXAMPLE = [
  { name: 'President', B: 50e6, N: TOP08 },
  { name: 'U.S. House', B: 400e3, N: HOUSE },
  { name: 'Town race', B: 1000, N: TOWN.N },
];
function ballot(ctx, S, st) {
  const { W, H, col, fs } = S;
  const per = EXAMPLE.map(l => l.B / l.N), on = EXAMPLE.map((_, i) => clamp01(st.n - i));
  const sum = per.reduce((t, v, i) => t + v * on[i], 0);
  const a = 0.24 * Math.tanh((6 * (C0 - sum)) / C0);
  const below = lineH(S) * 2 + 10;
  const pivX = W / 2, pivY = Math.min(H * 0.66, H - below - 20), arm = Math.min(W * 0.44, H * 0.9), standH = Math.max(12, Math.min(H * 0.2, H - pivY - below));
  const u = [Math.cos(a), -Math.sin(a)];
  const L = [pivX - arm * u[0], pivY - arm * u[1]], R = [pivX + arm * u[0], pivY + arm * u[1]];
  ctx.fillStyle = col.lineStrong;
  ctx.beginPath(); ctx.moveTo(pivX, pivY); ctx.lineTo(pivX - standH * 0.45, pivY + standH); ctx.lineTo(pivX + standH * 0.45, pivY + standH); ctx.closePath(); ctx.fill();
  ctx.strokeStyle = col.fg; ctx.lineWidth = 3; ctx.lineCap = 'round';
  ctx.beginPath(); ctx.moveTo(L[0], L[1]); ctx.lineTo(R[0], R[1]); ctx.stroke(); ctx.lineCap = 'butt';
  // dollars to height: the taller stack fits above the beam at its highest
  const bw = arm * 0.5, ppd = Math.max(4, (pivY - arm * Math.sin(0.24) - 14) / 9.6);
  // the trip: an open box, its cost; the races: solid blocks, each with what it repays, its dollars on it
  ctx.save(); ctx.translate(L[0], L[1]); ctx.rotate(-a);
  ctx.strokeStyle = col.fg; ctx.lineWidth = 2; ctx.strokeRect(arm * 0.12 + 1, -2 - C0 * ppd + 1, bw - 2, C0 * ppd - 2);
  ctx.restore();
  ctx.save(); ctx.translate(R[0], R[1]); ctx.rotate(-a);
  const shades = [col.accent, col.fg, col.dot], ink = [col.bg, col.bg, col.fg];
  let h = 2;
  per.forEach((v, i) => {
    if (on[i] <= 0) return;
    const ph = v * ppd, drop = (1 - on[i]) * 36, y = -h - ph - drop;
    ctx.globalAlpha = on[i]; ctx.fillStyle = shades[i];
    ctx.fillRect(-arm * 0.12 - bw, y, bw, ph - 1);
    const lab = '$' + v.toFixed(2), fit = [0.92, 0.78].find(z => { font(ctx, S, { weight: 600, size: z }); return ph > fs * z * 1.3 && ctx.measureText(lab).width <= bw - 6; });
    if (fit) text(ctx, S, lab, -arm * 0.12 - bw / 2, y + ph / 2, { base: 'middle', color: ink[i], weight: 600, size: fit });
    h += ph * on[i];
  });
  ctx.globalAlpha = 1; ctx.restore();
  const y = Math.max(L[1], R[1]) + lineH(S) + 4;
  rowsOf(ctx, S, [
    { s: money(C0), x: L[0] + (arm * 0.12 + bw / 2) * u[0], color: col.fg },
    { s: `$${sum.toFixed(2)}`, x: R[0] - (arm * 0.12 + bw / 2) * u[0], color: sum > C0 ? col.accent : col.fg },
  ], y, { weight: 600 });
}

export const SCENES = { worlds, margins, curve, field, stages, trips, ballot };

// What each scene shows, for a screen reader (the canvas is one image).
export const ALT = {
  worlds: 'Two blocks of the town’s 2,000 ballots, the same in both but for yours: counted on the left, not counted on the right. In one run your side wins both, 1,040 to 960 and 1,039 to 960; in a closer run, counted is a tie, 1,000 to 1,000, and not counted the other side wins, 999 to 1,000.',
  margins: 'A row of possible counts of everyone else, by your side’s lead, from three behind to three ahead; for each, who wins with your ballot counted and without it. They differ only at a tie and at one vote short, where a coin toss decides: each gives half a change, and the halves make one.',
  curve: 'A forecast curve of the chance of each count of your side’s votes. At 50–50 a bar: its outline the chance of a tie or one short, its filled half the chance your ballot changes who wins.',
  field: 'A square field of dots, one for each run of the election; one, ringed, is a run your ballot decides.',
  stages: 'The presidency in two steps: a field for the chance your ballot changes Pennsylvania’s winner, then a hundred dots, nineteen lit, for the times its electoral votes then decide the College, then the larger field of both.',
  trips: `A trip of $8.87 in each of the town race’s 468 runs; the trips on a seesaw against what the result is worth to you; the presidency’s 10 million trips; against them, ${Math.round(PEOPLE / 1e6)} million people at ${money(C0 * TOP08 / PEOPLE)} each; and your cost carried to both figures on a scale of dollars.`,
  ballot: 'A seesaw: one trip of $8.87 on one end; on the other, what each race repays of the trip, its worth to you divided by its N, added one race at a time. Together they outweigh the trip.',
};
