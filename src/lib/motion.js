// Motion, per the midterms MOTION-SPEC (inherited/design/specs/MOTION-SPEC.md) as this site's spec reads it
// (design/DESIGN-SPEC.md §4). Adapted from inherited/design/code/motion.js: the tokens and `play` are the same; the
// midterms live feed and navigation state it imported are gone (this site has no live data: the maker, 03:13 UTC
// 11-07). Each surface runs its own token on its own property; nothing here is applied globally (MOTION-SPEC s.4.3).
import { useEffect, useState } from 'preact/hooks';

const SPRING = 'linear(0, 0.005 1.3%, 0.019 2.5%, 0.08 5.5%, 0.163 8.5%, 0.457 18.3%, 0.549 21.8%, 0.63 25.3%, 0.694 28.5%, 0.753 32%, 0.805 35.8%, 0.846 39.5%, 0.886 44%, 0.919 49%, 0.944 54.5%, 0.964 60.8%, 0.988 75.5%, 1)';
// The spring's stops as [value, time fraction] (MOTION-SPEC s.2).
const SPRING_STOPS = [[0, 0], [.005, .013], [.019, .025], [.08, .055], [.163, .085], [.457, .183], [.549, .218], [.63, .253], [.694, .285], [.753, .32], [.805, .358], [.846, .395], [.886, .44], [.919, .49], [.944, .545], [.964, .608], [.988, .755], [1, 1]];
// The spring's value at a fraction of its time, for a script that draws each frame itself (a canvas of dots, which
// no keyframes can say: the midterms markets chart drew its lines the same way).
export function springValue(f) {
  if (f <= 0) return 0;
  for (let i = 1; i < SPRING_STOPS.length; i++) {
    const [v1, t1] = SPRING_STOPS[i], [v0, t0] = SPRING_STOPS[i - 1];
    if (f <= t1) return v0 + (v1 - v0) * (f - t0) / (t1 - t0);
  }
  return 1;
}
const OUT_STRONG = 'cubic-bezier(.17, .84, .44, 1)';
const hasLinear = typeof CSS !== 'undefined' && CSS.supports && CSS.supports('transition-timing-function', 'linear(0, 1)');
const spring = hasLinear ? SPRING : OUT_STRONG;   // MOTION-SPEC s.2: browsers without linear() get the closing curve

// The tokens this site uses (DESIGN-SPEC §4). A token is used only on the surfaces named for it there.
export const TOKENS = {
  'nav-in': { duration: 680, easing: spring },     // V1: the field's arrival, cost to B*
  chart: { duration: 450, easing: spring },        // V2, V3: the field moving with the reader's cost or reading
  segment: { duration: 300, easing: spring },      // V8: a segmented control's indicator
  reveal: { duration: 160, easing: 'ease-out' },   // V7: a fold's contents
};

const rm = typeof matchMedia !== 'undefined' ? matchMedia('(prefers-reduced-motion: reduce)') : null;
export const reducedMotion = () => Boolean(rm && rm.matches);
// The setting can change while the page is open (MOTION-SPEC s.5).
export function useReducedMotion() {
  const [r, set] = useState(reducedMotion());
  useEffect(() => { if (!rm) return; const f = () => set(rm.matches); rm.addEventListener('change', f); return () => rm.removeEventListener('change', f); }, []);
  return r;
}

// Transform motion is removed under reduced motion; opacity (`reveal`) stays (MOTION-SPEC s.5).
const KEEP_WHEN_REDUCED = new Set(['reveal']);
export function mayMove(token) { return !(reducedMotion() && !KEEP_WHEN_REDUCED.has(token)); }

// Run one token on one element. Interruptible: a running animation of the same element and kind is cancelled first
// (MOTION-SPEC s.4.4).
export function play(el, token, keyframes, opts = {}) {
  if (!el || !el.animate || !mayMove(token)) return null;
  const t = TOKENS[token];
  const key = `_m_${opts.kind || token}`;
  if (el[key]) el[key].cancel();
  const a = el.animate(keyframes, { duration: opts.duration ?? t.duration, easing: t.easing, fill: opts.fill || 'backwards' });
  a.id = `motion:${token}`;
  el[key] = a;
  a.finished.then(() => { if (el[key] === a) el[key] = null; }, () => {});
  return a;
}

// A frame-by-frame tween on the spring for a canvas: calls draw(k) with k from 0 to 1 over the token's duration and
// resolves when done. A new tween on the same owner cancels the old one, which stops where it stood (interruptible).
// The clock starts on the first frame presented (MOTION-SPEC s.4.12), not at the call.
export function tween(owner, token, draw) {
  if (owner._tw) owner._tw.cancel();
  const d = TOKENS[token].duration;
  let raf = 0, t0 = 0, done;
  const p = new Promise(r => { done = r; });
  const step = now => {
    if (!t0) t0 = now;
    const f = Math.min(1, (now - t0) / d);
    draw(springValue(f));
    if (f < 1) raf = requestAnimationFrame(step); else { owner._tw = null; done(true); }
  };
  owner._tw = { cancel: () => { cancelAnimationFrame(raf); owner._tw = null; done(false); } };
  if (!mayMove(token)) { draw(1); owner._tw = null; done(true); return p; }
  raf = requestAnimationFrame(step);
  return p;
}
