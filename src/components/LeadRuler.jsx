// The figure's working, drawn (the maker, 11-07 04:32: "as much explanation as possible to be visual"). The reader's
// cost and the figure are two marks on the site's one scale of dollars, 1 cent to 1 trillion, and the arrow from one to
// the other is the multiplication: × N, the odds against one vote changing who wins. So a longer arrow is a longer
// shot, and the figure for each contest sits as far right as its odds carry it. Per person, a second arrow divides the
// figure among the people the result touches. Every cold reader of 11-07 first read "$89 million to you" as a sum to
// be received, and none could say why the figure is the cost times N; this is the picture of both.
// The marks glide to their new places when the contest, the reading or the cost changes (`chart`, transform only).
// Where the route's back-test leans one way, a dashed arrow from the figure points the way it may lie (Field.jsx).
import { useLayoutEffect, useRef, useState } from 'preact/hooks';
import { money, oneIn, count } from '../lib/format.js';
import { play } from '../lib/motion.js';

const LO = -2, HI = 12, SPAN = HI - LO;
let ctx2d = null;
const measure = (t, font) => { ctx2d = ctx2d || document.createElement('canvas').getContext('2d'); ctx2d.font = font; return ctx2d.measureText(t).width; };

// labels in a row, each centred on its mark where it can be, kept 6 px apart and inside the box
function spread(items, w) {
  const s = [...items].sort((p, q) => p.x - q.x);
  for (const it of s) it.l = Math.max(0, Math.min(w - it.w, it.x - it.w / 2));
  for (let i = 1; i < s.length; i++) s[i].l = Math.max(s[i].l, s[i - 1].l + s[i - 1].w + 6);
  if (s.length) s[s.length - 1].l = Math.min(s[s.length - 1].l, w - s[s.length - 1].w);
  for (let i = s.length - 2; i >= 0; i--) s[i].l = Math.min(s[i].l, s[i + 1].l - s[i].w - 6);
  for (const it of s) it.l = Math.max(0, it.l);
  return items;
}

export function LeadRuler({ a, C, reading }) {
  const box = useRef(null);
  const [m, setM] = useState({ w: 0, font: '' });
  useLayoutEffect(() => {
    const ro = new ResizeObserver(() => {
      const st = getComputedStyle(box.current);
      setM({ w: box.current.clientWidth, font: `600 ${st.fontSize} ${st.fontFamily}` });
    });
    ro.observe(box.current);
    return () => ro.disconnect();
  }, []);
  const { w, font } = m;
  const per = reading === 'person';
  const X = lx => ((Math.max(LO, Math.min(HI, lx)) - LO) / SPAN) * w;
  const lc = Math.log10(C), lt = lc + Math.log10(a.N), lp = a.pop ? lt - Math.log10(a.pop.value) : lt;
  const xc = X(lc), xt = X(lt), xp = X(lp);
  const times = oneIn(a.N).replace(/^1 in /, '');
  const sized = (k, t, x, cls) => ({ k, t, x, cls, w: w ? measure(t, font) : 0 });
  const above = spread([sized('times', `× ${times}`, (xc + xt) / 2, 'lr-op')], w);
  // under the marks: the cost, the figure, and per person the share and the division; where they cannot all fit (a
  // narrow phone at large text) the division's word goes first, then the whole figure, then the cost
  let row = [
    sized('c', money(C), xc, 'lr-you'),
    sized('t', money(C * a.N), xt, per ? 'lr-dim' : ''),
    ...(per ? [sized('p', money((C * a.N) / a.pop.value), xp, ''), sized('div', `÷ ${count(a.pop.value)} people`, (xt + xp) / 2, 'lr-op')] : []),
  ];
  const fits = r => r.reduce((t, l) => t + l.w + 6, -6) <= w;
  if (per && !fits(row)) row = row.map(l => (l.k === 'div' ? sized('div', `÷ ${count(a.pop.value)}`, l.x, l.cls) : l));
  for (const k of ['t', 'c']) if (per && !fits(row)) row = row.filter(l => l.k !== k);
  const below = spread(row, w);

  // the glide: each placed element moves from where it stood to where it now stands
  const els = useRef({}), prev = useRef({});
  const T = {};
  const place = (k, tr) => { T[k] = tr; return { ref: el => { els.current[k] = el; }, style: { transform: tr } }; };
  useLayoutEffect(() => {
    for (const k in T) {
      const was = prev.current[k];
      if (was && was !== T[k] && els.current[k]) play(els.current[k], 'chart', [{ transform: was }, { transform: T[k] }], { kind: 'glide' });
    }
    prev.current = T;
  });

  const head = 7;
  return (
    <div class={`lr${per ? ' per' : ''}`} ref={box} aria-hidden="true">
      {w ? <>
        {[0, 3, 6, 9].map(p => <span class="lr-tick" style={{ transform: `translateX(${X(p)}px)` }} />)}
        <span class="lr-track" />
        <span class="lr-arrow" {...place('ax', `translateX(${xc}px) scaleX(${Math.max(0, xt - xc - head - 5)})`)} />
        <span class="lr-head" {...place('ah', `translateX(${xt - head - 5}px)`)} />
        {per ? <>
          <span class="lr-drop" {...place('dd', `translateX(${xt - 0.5}px)`)} />
          <span class="lr-arrow lr-div" {...place('dx', `translateX(${xp + head + 5}px) scaleX(${Math.max(0, xt - xp - head - 5)})`)} />
          <span class="lr-head lr-div lr-left" {...place('dh', `translateX(${xp + 5}px)`)} />
          <span class="lr-ring lr-div" {...place('pr', `translateX(${xp - 5}px)`)} />
        </> : null}
        <span class={`lr-ring${per ? ' lr-dim' : ''}`} {...place('tr', `translateX(${xt - 5}px)`)} />
        {a.lean ? <span class={`lr-lean${a.lean === 'low' ? ' low' : ''}${per ? ' lr-div' : ''}`} {...place('ln', `translateX(${Math.max(0, Math.min(w - 14, (per ? xp : xt) + (a.lean === 'low' ? -21 : 7)))}px)`)} /> : null}
        <span class="lr-dot" {...place('cd', `translateX(${xc - 4}px)`)} />
        {above.map(l => <span class={`lr-l lr-up ${l.cls}`} {...place(`l${l.k}`, `translateX(${l.l}px)`)}>{l.t}</span>)}
        {below.map(l => <span class={`lr-l lr-down ${l.cls}`} {...place(`l${l.k}`, `translateX(${l.l}px)`)}>{l.t}</span>)}
      </> : null}
    </div>
  );
}
