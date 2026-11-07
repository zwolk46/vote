// The explainer's pictures, drawn on one canvas (brief X2: one visual that changes as the reader moves, so the reader
// watches the same picture become the next idea). Each scene draws a state; between two beats of one scene the state
// is mixed, so the marks move; between scenes the old picture fades out and the new one in (text never travels across
// text, MOTION-SPEC). The words on the canvas are labels on marks only, drawn at the page's small type size as the
// reader has it (read from the page, so they grow with the reader's text), and wrapped to the room they have.
//
// S = { W, H, fs, ff, col, dpr }: the box, the small type's size and family, the page's colours (lib/media.js).
import { C0, TOWN, PA, CLOSE08, HOUSE, PEOPLE, WORTH } from './beats.js';
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
// 1,040 of 2,000 are your side's with you (52%); yours is the last of them. Everyone else is the same in both.
function worlds(ctx, S) {
  const { W, H, col, fs } = S;
  const gap = Math.max(14, W * 0.05), pw = (W - gap) / 2, cols = 40, rows = 50;
  const top = lineH(S) + 6, bottom = lineH(S, 1.15) + 8;
  const pitch = Math.min(pw / cols, (H - top - bottom) / rows), r = Math.max(0.8, pitch * 0.36);
  const gw = cols * pitch, gh = rows * pitch, me = 1020;   // yours: in the middle of your side's last row
  const y0 = Math.max(0, (H - (top + gh + bottom)) / 2);
  for (let p = 0; p < 2; p++) {
    const x0 = p * (pw + gap) + (pw - gw) / 2, cx = p * (pw + gap) + pw / 2;
    text(ctx, S, p === 0 ? 'Counted' : 'Not counted', cx, y0 + fs, { weight: 600, color: col.fg });
    for (let k = 0; k < 2000; k++) {
      if (k === me) continue;
      ctx.globalAlpha = k < 1040 ? 0.9 : 0.75;
      dot(ctx, x0 + ((k % cols) + 0.5) * pitch, y0 + top + (Math.floor(k / cols) + 0.5) * pitch, r, k < 1040 ? col.fg : col.dot);
    }
    ctx.globalAlpha = 1;
    const mx = x0 + ((me % cols) + 0.5) * pitch, my = y0 + top + (Math.floor(me / cols) + 0.5) * pitch, rr = Math.max(6, r * 3.4);
    if (p === 0) dot(ctx, mx, my, Math.max(2.2, r * 1.4), col.accent);
    else dot(ctx, mx, my, rr - 1, col.bg);
    ring(ctx, mx, my, rr, col.accent);
    text(ctx, S, p === 0 ? '1,040 to 960' : '1,039 to 960', cx, y0 + top + gh + 6 + fs * 1.15, { weight: 600, color: col.fg, size: 1.15 });
  }
}

// ---- 2 and 3. everyone else's count, and the two where your ballot changes who wins ------------------------------
// Each column is one count of everyone else, by your side's lead among them. Each dot is who wins: your side (dark),
// theirs (grey), or a tie (half each), settled by lot. Counted, your ballot adds one to your side's lead.
const AXIS_M = 'your side’s lead among everyone else';
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
      ctx.globalAlpha = j;
      half(ctx, lerp(c1, mid, j), lerp(y1, yj, j), r, col.accent, -1);
      half(ctx, lerp(c2, mid, j), lerp(y1, yj, j), r, col.accent, 1);
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
  const lo = 0.3, hi = 0.7, top = fs * 0.6, base = H - (lineH(S) + 8 + axisH), ph = base - top;
  const X = v => ((v - lo) / (hi - lo)) * W, Y = d => base - (Math.min(d, Y_MAX * 1.02) / Y_MAX) * ph;
  const at = v => pdf(v, st.mu, st.sd) / st.n;
  const path = () => { for (let i = 0; i <= 240; i++) { const v = lo + ((hi - lo) * i) / 240; i ? ctx.lineTo(X(v), Y(at(v))) : ctx.moveTo(X(v), Y(at(v))); } };
  ctx.beginPath(); path(); ctx.lineTo(W, base); ctx.lineTo(0, base); ctx.closePath();
  ctx.fillStyle = col.dot; ctx.globalAlpha = 0.25; ctx.fill(); ctx.globalAlpha = 1;
  ctx.beginPath(); path(); ctx.strokeStyle = col.fg; ctx.lineWidth = 1.5; ctx.stroke();
  ctx.fillStyle = col.lineStrong; ctx.fillRect(0, base, W, 1);
  // the bar at 50–50: its outline the chance of a tie or one short, its filled half the chance your ballot changes
  // who wins
  const h = at(0.5), bw = Math.max(8, fs * 0.65), x = X(0.5), yT = Y(h), yH = Y(h / 2);
  ctx.fillStyle = col.accent; ctx.fillRect(x - bw / 2, yH, bw, base - yH);
  if (base - yT > 3) { ctx.strokeStyle = col.accent; ctx.lineWidth = 1.2; ctx.strokeRect(x - bw / 2 + 0.6, yT + 0.6, bw - 1.2, base - yT - 1.2); }
  if (beat.figIn) text(ctx, S, beat.figIn, x + bw / 2 + 6, Math.min(base - fs * 0.75, yH), { align: 'left', base: 'middle', color: col.accent, weight: 600, size: 1.1, halo: true });
  for (const [v, t] of [[0.4, '40%'], [0.5, '50–50'], [0.6, '60%']]) text(ctx, S, t, X(v), base + 4 + fs, { color: v === 0.5 ? col.accent : col.muted, weight: v === 0.5 ? 600 : 400 });
  wrap(ctx, S, AXIS_C, W / 2, base + 6 + fs + lineH(S), W - 4);
}

// ---- 5. a field of runs of the election, one dot for each; the ringed one is a run your ballot decides ----------
// A square of n runs, side D, centred at (cx, cy); `inner` outlines the smaller fields inside it.
function fieldOf(ctx, S, n, cx, cy, D, inner = []) {
  const { col } = S;
  const side = Math.sqrt(n), pitch = D / side;
  if (pitch >= 2.5) {
    const cols = Math.ceil(side), rows = Math.ceil(n / cols), x0 = cx - (cols * pitch) / 2, y0 = cy - (rows * pitch) / 2, s = Math.max(1, pitch * 0.55);
    ctx.globalAlpha = 0.75; ctx.fillStyle = col.dot;
    for (let k = 0; k < n; k++) {
      const x = x0 + ((k % cols) + 0.5) * pitch, y = y0 + (Math.floor(k / cols) + 0.5) * pitch;
      if (pitch > 7) dot(ctx, x, y, s / 2, col.dot); else ctx.fillRect(x - s / 2, y - s / 2, s, s);
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
  const D = Math.min(W * 0.56, H - 4);
  const cx = lerp(lerp(W / 2, D / 2 + 2, g), W / 2, b), cy = H / 2;
  const n = Math.exp(lerp(Math.log(PA.state), Math.log(PA.N), b));
  fieldOf(ctx, S, n, cx, cy, D, b > 0 ? [PA.state] : []);
  const a = g * (1 - b);
  if (a > 0) {
    const room = W - D - 4, gw = Math.max(40, Math.min(room - fs * 1.6, H - 8)), p = gw / 10, x0 = W - gw, y0 = cy - gw / 2;
    ctx.globalAlpha = a;
    for (let i = 0; i < 100; i++) dot(ctx, x0 + ((i % 10) + 0.5) * p, y0 + (Math.floor(i / 10) + 0.5) * p, p * 0.33, i < 19 ? col.accent : col.dot);
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
// k 4: the presidency's $89 million shared by 300 million people (a round figure): 30¢ each.
// k 5: the scale of dollars of the first page: your cost, × 468 and × 10 million.
const LO = -2, HI = 12;
// the beam's turn: up at the result's end when the trips weigh more (a > 0), down when the result does
const turn = (cost, worth) => Math.max(-0.24, Math.min(0.24, 0.32 * (Math.log10(cost) - Math.log10(worth))));
function trips(ctx, S, st) {
  const { W, H, col, fs } = S;
  const k = st.k, m = clamp01(k);                    // 0: the grid; 1: the trips on the seesaw
  const T1 = C0 * TOWN.N, T2 = C0 * CLOSE08, ME = 9 * 26 + 13;
  if (k < 3.5) {
    const tA = k <= 3 ? 1 : clamp01(1 - (k - 3) * 2);
    const balA = tA * clamp01(k * 1.5 - 0.5);
    const cols = 26, rows = 18, gp = Math.min((W - 8) / cols, (H - 8) / rows), gx = (W - cols * gp) / 2, gy = (H - rows * gp) / 2;
    // the seesaw: the beam turns with the reader from one weighing to the next
    const pivX = W / 2, pivY = H * 0.6, arm = Math.min(W * 0.44, H * 0.9), standH = Math.min(H * 0.22, H - pivY - lineH(S) - 6);
    let a = turn(T1, WORTH.lo);
    if (k > 1) a = lerp(a, turn(T1, WORTH.hi), clamp01(k - 1));
    if (k > 2) a = lerp(turn(T1, WORTH.hi), turn(T2, WORTH.hi), clamp01(k - 2));
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
    for (let i = 0; i < TOWN.N; i++) {
      if (i === ME) continue;
      const gxI = gx + ((i % cols) + 0.5) * gp, gyI = gy + (Math.floor(i / cols) + 0.5) * gp;
      const [hx, hy] = at(L, s0 + ((i % hc) + 0.5) * hp, 2.5 + (Math.floor(i / hc) + 0.5) * hp);
      ctx.globalAlpha = tA * (1 - big);
      dot(ctx, lerp(gxI, hx, m), lerp(gyI, hy, m), lerp(gp * 0.34, hp * 0.4, m), col.dot);
    }
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
    ctx.globalAlpha = tA;
    dot(ctx, ox, oy, lerp(gp * 0.34, 5.5, m), col.accent);
    ring(ctx, ox, oy, lerp(Math.max(7, gp * 0.9), 10.5, m), col.accent, 2);
    // the two ends' figures, under the beam
    if (m > 0.5) {
      ctx.globalAlpha = tA * clamp01(m * 2 - 1);
      const lx = at(L, s0 + heapW / 2, 0), rx = at(R, -arm * 0.2, 0);
      text(ctx, S, k > 2.5 ? money(T2) : money(T1), lx[0], Math.max(lx[1], rx[1]) + lineH(S) + 4, { color: col.fg, weight: 600 });
      text(ctx, S, k > 1.5 ? money(WORTH.hi) : money(WORTH.lo), rx[0], Math.max(lx[1], rx[1]) + lineH(S) + 4, { color: col.accent, weight: 600 });
    }
    ctx.globalAlpha = 1;
  }
  // the presidency's $89 million shared by 300 million people: each dot a million people, 30¢ each
  const sA = band(k, 4, 0.5);
  if (sA > 0) {
    ctx.globalAlpha = sA;
    const cols = 20, rows = 15, p = Math.min((W - 8) / cols, (H - lineH(S, 1.1) - 10) / rows), x0 = (W - cols * p) / 2;
    const y0 = Math.max(2, (H - (rows * p + lineH(S, 1.1) + 6)) / 2);
    for (let i = 0; i < 300; i++) dot(ctx, x0 + ((i % cols) + 0.5) * p, y0 + (Math.floor(i / cols) + 0.5) * p, p * 0.3, col.fg);
    text(ctx, S, `${money(T2 / PEOPLE)} each`, W / 2, y0 + rows * p + fs * 1.3, { color: col.accent, weight: 600, size: 1.1 });
    ctx.globalAlpha = 1;
  }
  // the scale of dollars: your cost, × 468 and × 10 million
  const rA = clamp01((k - 4.5) * 2);
  if (rA > 0) {
    ctx.globalAlpha = rA;
    const pad = Math.max(24, fs * 2.4), X = lx => pad + ((lx - LO) / (HI - LO)) * (W - 2 * pad), y = H * 0.55;
    ctx.fillStyle = col.lineStrong; ctx.fillRect(0, y, W, 1);
    for (const [p, t] of [[0, '$1'], [3, '$1,000'], [6, '$1M'], [9, '$1B']]) { ctx.fillStyle = col.lineStrong; ctx.fillRect(X(p), y - 3, 1, 7); text(ctx, S, t, X(p), y + fs * 1.5 + lineH(S, 1.1), { size: 0.9 }); }
    const c = Math.log10(C0), t1 = c + Math.log10(TOWN.N), t2 = c + Math.log10(CLOSE08);
    const arrow = (x1, x2, yy, label) => {
      ctx.strokeStyle = col.accent; ctx.fillStyle = col.accent; ctx.lineWidth = 2.5;
      ctx.beginPath(); ctx.moveTo(x1, yy); ctx.lineTo(x2 - 8, yy); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(x2, yy); ctx.lineTo(x2 - 10, yy - 5.5); ctx.lineTo(x2 - 10, yy + 5.5); ctx.closePath(); ctx.fill();
      text(ctx, S, label, (x1 + x2) / 2, yy - 8, { color: col.accent, weight: 600, size: 1.1 });
    };
    arrow(X(c), X(t1), y - lineH(S, 1.1) * 1.6, '× 468');
    arrow(X(c), X(t2), y - lineH(S, 1.1) * 3.4, '× 10 million');
    dot(ctx, X(c), y, 5.5, col.accent);
    for (const t of [t1, t2]) { dot(ctx, X(t), y, 6, col.bg); ring(ctx, X(t), y, 6, col.fg, 2.2); }
    text(ctx, S, '$8.87', X(c), y + fs * 1.6, { color: col.accent, weight: 600, size: 1.1 });
    text(ctx, S, '$4,150', X(t1), y + fs * 1.6, { color: col.fg, weight: 600, size: 1.1 });
    text(ctx, S, '$89M', X(t2), y + fs * 1.6, { color: col.fg, weight: 600, size: 1.1 });
    ctx.globalAlpha = 1;
  }
}

// ---- 8. one trip, the whole ballot: each race repays its share of the trip; the shares together fill it -----------
// An example of what the result might be worth to a reader: the presidency $45 million (closest states, 2008, whose
// figure is $89 million), a House race $400,000 (the average race, $1.6 million), the town race $1,200 ($4,150).
export const EXAMPLE = [
  { name: 'President', B: 45e6, Bs: C0 * CLOSE08 },
  { name: 'U.S. House', B: 400e3, Bs: C0 * HOUSE },
  { name: 'Town race', B: 1200, Bs: C0 * TOWN.N },
];
function ballot(ctx, S, st) {
  const { W, H, col, fs } = S;
  const f = st.fill, barH = Math.max(9, fs * 0.7), rowH = fs * 1.4 + barH + 16, bw = (W - 4) * 0.84;
  const shades = [col.accent, col.fg, col.dot];
  const used = 3 * rowH + lineH(S) + 14 + barH + fs * 1.6, y0 = Math.max(0, (H - used) / 2);
  const ty = y0 + 3 * rowH + lineH(S) + 14;
  let cum = 0;
  EXAMPLE.forEach((l, i) => {
    const sh = l.B / l.Bs, y = y0 + i * rowH + fs;
    text(ctx, S, l.name, 2, y, { align: 'left', color: col.fg, weight: 600 });
    text(ctx, S, `${Math.round(sh * 100)}%`, 2 + bw, y, { align: 'right', color: col.fg });
    ctx.fillStyle = col.track || col.line; ctx.fillRect(2, y + 6, bw, barH);
    // each share slides down into the trip, after the one before it
    const x = lerp(2, 2 + cum * bw, f), yy = lerp(y + 6, ty, f);
    ctx.fillStyle = shades[i]; ctx.fillRect(x, yy, sh * bw, barH);
    cum += sh;
  });
  text(ctx, S, 'The trip', 2, ty - 7, { align: 'left', color: col.fg, weight: 600 });
  ctx.strokeStyle = col.lineStrong; ctx.lineWidth = 1; ctx.strokeRect(2.5, ty - 0.5, bw - 1, barH + 1);
  // the trip's end: 100%, its cost repaid
  ctx.fillStyle = col.fg; ctx.fillRect(2 + bw - 1, ty - 7, 2, barH + 14);
  const tot = EXAMPLE.reduce((s, l) => s + Math.round((l.B / l.Bs) * 100), 0);
  text(ctx, S, f > 0.5 ? `${tot}%` : '100%', 2 + bw, ty + barH + fs * 1.6, { align: 'center', color: f > 0.5 ? col.accent : col.muted, weight: 600 });
}

export const SCENES = { worlds, margins, curve, field, stages, trips, ballot };

// What each scene shows, for a screen reader (the canvas is one image).
export const ALT = {
  worlds: 'Two blocks of the town’s 2,000 ballots, the same in both but for yours: counted on the left, not counted on the right. Your side wins both, 1,040 to 960 and 1,039 to 960.',
  margins: 'A row of possible counts of everyone else, by your side’s lead, from three behind to three ahead; for each, who wins with your ballot counted and without it. They differ only at a tie and at one vote short, where a lot decides: each gives half a change, and the halves make one.',
  curve: 'A forecast curve of the chance of each count of your side’s votes. At 50–50 a bar: its outline the chance of a tie or one short, its filled half the chance your ballot changes who wins.',
  field: 'A square field of dots, one for each run of the election; one, ringed, is a run your ballot decides.',
  stages: 'The presidency in two steps: a field for the chance your ballot changes Pennsylvania’s winner, then a hundred dots, nineteen lit, for the times its electoral votes then decide the College, then the larger field of both.',
  trips: 'A trip of $8.87 in each of the town race’s 468 runs; the trips on a balance against what the result is worth to you; the presidency’s 10 million trips; its $89 million shared by 300 million people; and your cost carried to both figures on a scale of dollars.',
  ballot: 'Three races on one ballot, each repaying a share of the trip; the shares slide into one bar, and together they pass its end.',
};
