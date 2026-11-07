// Motion, per research/design/motion/MOTION-SPEC.md (W8; v1.1 adopted 12:03 UTC). Each surface calls `play` with
// its own token on its own property; nothing here is applied globally (spec s.2, s.4.3). The still version is the
// default: `play` does nothing unless motion is allowed for this render (spec s.5; catch-up, s.3 surface 28).
import { useLayoutEffect, useRef } from 'preact/hooks';
import { live } from './live.js';
import { navBusy } from './navstate.js';

const SPRING = 'linear(0, 0.005 1.3%, 0.019 2.5%, 0.08 5.5%, 0.163 8.5%, 0.457 18.3%, 0.549 21.8%, 0.63 25.3%, 0.694 28.5%, 0.753 32%, 0.805 35.8%, 0.846 39.5%, 0.886 44%, 0.919 49%, 0.944 54.5%, 0.964 60.8%, 0.988 75.5%, 1)';
// The spring's stops as [value, time fraction] (spec s.2, v1.3), and the time at which it reaches a fraction of its
// movement (surface 3's majority mark). Without linear() the curve is OUT_STRONG; the stops then read a little late.
const SPRING_STOPS = [[0, 0], [.005, .013], [.019, .025], [.08, .055], [.163, .085], [.457, .183], [.549, .218], [.63, .253], [.694, .285], [.753, .32], [.805, .358], [.846, .395], [.886, .44], [.919, .49], [.944, .545], [.964, .608], [.988, .755], [1, 1]];
export function springTimeAt(f, duration) {
  for (let i = 1; i < SPRING_STOPS.length; i++) {
    const [v1, t1] = SPRING_STOPS[i], [v0, t0] = SPRING_STOPS[i - 1];
    if (f <= v1) return duration * (t0 + (t1 - t0) * (f - v0) / (v1 - v0));
  }
  return duration;
}
// The spring's value at a fraction of its time (the inverse of the above), for a script that draws each frame itself
// (the markets chart's lines, which move by their path and not by a transform: no keyframes can say that).
export function springValue(f) {
  if (f <= 0) return 0;
  for (let i = 1; i < SPRING_STOPS.length; i++) {
    const [v1, t1] = SPRING_STOPS[i], [v0, t0] = SPRING_STOPS[i - 1];
    if (f <= t1) return v0 + (v1 - v0) * (f - t0) / (t1 - t0);
  }
  return 1;
}
const OUT_STRONG = 'cubic-bezier(.17, .84, .44, 1)';
const SHEET = 'cubic-bezier(.32, .72, 0, 1)';
const hasLinear = typeof CSS !== 'undefined' && CSS.supports && CSS.supports('transition-timing-function', 'linear(0, 1)');
const spring = hasLinear ? SPRING : OUT_STRONG;   // spec s.2: browsers without linear() get the closing curve

// The tokens (spec s.2). A token is used only on the surfaces section 3 names for it.
export const TOKENS = {
  'nav-in': { duration: 680, easing: spring },
  'nav-back': { duration: 450, easing: OUT_STRONG },
  count: { duration: 240, easing: OUT_STRONG },
  call: { duration: 680, easing: spring },
  'call-color': { duration: 300, easing: spring },
  uncall: { duration: 450, easing: OUT_STRONG },
  insert: { duration: 510, easing: spring },
  chart: { duration: 450, easing: spring },          // the markets chart changing range or market: the lines, axis and volume move to the new state (drawn each frame by components/Markets.jsx with springValue)
  reorder: { duration: 410, easing: spring },
  tour: { duration: 450, easing: spring },           // the first-visit tour's ring and card gliding from one step's place to the next (components/Tour.jsx; no row in MOTION-SPEC s.3 yet, the orchestrator adds it); under reduced motion the component does not glide at all
  reveal: { duration: 160, easing: 'ease-out' },
  sheet: { duration: 500, easing: SHEET },
  drawer: { duration: 400, easing: SHEET },          // the Zag drawer's own token (the cards, the night card); closing is 300 ms. The side menu it carried went with the dock (surface 34, v1.8.21).
  // surface 35 (changing page): each in two phases that never overlap, the old view out and then the new one in
  'fade-through': { duration: 200, easing: 'ease-out' }, 'fade-through-out': { duration: 100, easing: 'ease-in' },
  axis: { duration: 240, easing: OUT_STRONG }, 'axis-out': { duration: 120, easing: 'ease-in' },
  // the call announcement's bar (DESIGN-SPEC s.31.1; W8's frame, research s.74): in from under the header, out up
  'banner-in': { duration: 250, easing: 'cubic-bezier(0, 0, .2, 1)' }, 'banner-out': { duration: 200, easing: 'cubic-bezier(.4, 0, 1, 1)' },
  // option B's moment (s.31.2; W8's s.74.1): the card in and out by opacity alone, and its fold into the banner by its
  // own height (and width), which lays out only itself; scaleY would squash its words
  'moment-in': { duration: 250, easing: 'cubic-bezier(0, 0, .2, 1)' }, 'moment-out': { duration: 200, easing: 'cubic-bezier(.4, 0, 1, 1)' },
  fold: { duration: 250, easing: 'cubic-bezier(.4, 0, .2, 1)' },
  // the desktop search palette (surface 38 as W21 rewrote it under the maker's 19:00 UTC 11-05 ask, Search.jsx): in, the scrim's
  // fade and the dialog's 8 px rise with its fade on details.so's closing curve; out, shorter, accelerating away (the
  // banner's out curve), so a choice is never kept waiting on the palette. Under reduced motion the fades alone, 0.6 as long.
  'palette-in': { duration: 220, easing: OUT_STRONG }, 'palette-out': { duration: 150, easing: 'cubic-bezier(.4, 0, 1, 1)' },
};

const rm = typeof matchMedia !== 'undefined' ? matchMedia('(prefers-reduced-motion: reduce)') : null;
export const reducedMotion = () => Boolean(rm && rm.matches);

// Transform motion (zoom, slides, bars, tints, reorders, number slides) is removed under reduced motion; colour
// (`call-color`) and opacity (`reveal`) stay (spec s.5).
const KEEP_WHEN_REDUCED = new Set(['call-color', 'reveal', 'fade-through', 'fade-through-out']);   // 35 under reduce: the fades only

// Whether a data event may move now: it happened in front of the viewer (live.eventful) and the token is allowed.
// Data that lands while a navigation motion runs is written at once and does not move (spec s.4.5): the view is
// moving anyway, and the zoom's copy is replaced by the live view, in its final state, when it settles.
export function mayMove(token, { navigation = false } = {}) {
  if (reducedMotion() && !KEEP_WHEN_REDUCED.has(token)) return false;
  return navigation || (live.eventful && !navBusy());
}

// Run one token on one element. Returns the Animation or null. Interruptible: a running animation of the same
// element and kind is cancelled first (spec s.4.4).
export function play(el, token, keyframes, opts = {}) {
  if (!el || !el.animate) return null;
  if (!mayMove(token, opts)) return null;
  const t = TOKENS[token];
  const key = `_m_${opts.kind || token}`;
  if (el[key]) el[key].cancel();
  const a = el.animate(keyframes, { duration: opts.duration ?? t.duration, easing: t.easing, delay: opts.delay || 0, fill: opts.fill || 'backwards' });
  a.id = `motion:${token}`;
  el[key] = a;
  a.finished.then(() => { if (el[key] === a) el[key] = null; }, () => {});
  return a;
}

// Surfaces 7, 14 and 22 only (map shapes, district shapes, state tiles): when a poll calls an area, its fill changes to
// the called colour with `call-color`, every area of that poll in the same frame (no stagger, no sweep order). A fill
// that reverts (a call withdrawn) changes at once (surface 19). Elements carry data-k (the status key); `prop` is
// 'fill' for SVG or 'backgroundColor' for tiles. The colours are the page's own tokens (--dem, --rep, ...).
const CALLED = new Set(['dem', 'rep', 'oth', 'split']);
export function useCallColor(ref, status, prop, absent = 'none') {
  const prev = useRef(null);
  useLayoutEffect(() => {
    const before = prev.current;
    prev.current = { ...status };
    const root = ref.current;
    if (!before || !root || !mayMove('call-color')) return;
    const css = getComputedStyle(document.documentElement);
    const colour = k => css.getPropertyValue(`--${k}`).trim();
    for (const el of root.querySelectorAll('[data-k]')) {
      const k = el.getAttribute('data-k');
      const was = before[k] || absent, now = status[k] || absent;
      if (was === now || !CALLED.has(now)) continue;
      play(el, 'call-color', [{ [prop]: colour(was) }, { [prop]: colour(now) }], { kind: 'fill' });
    }
  });
}
