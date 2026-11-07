// How it is worked out (brief X2): the nine ideas from the question to the figure, carried by one picture that becomes
// the next idea. Two versions on the preview (?page=how&v=a, ?v=b):
//   A · Scroll: the picture is held in view while the steps scroll past it; between steps it moves with the reader's
//       finger, frame by frame, with no duration of its own (MOTION-SPEC: scroll-linked motion), and holds still while
//       a step is read.
//   B · Steps: the same pictures, one step at a time, moved on by a tap. The picture moves to the next state on the
//       `chart` token (450 ms on the spring) and the words change at once. For a person handed a phone: the pace is
//       theirs, nothing moves until they ask, and a step cannot be half-scrolled.
// Under reduced motion each step is drawn still and complete, and changes at once (MOTION-SPEC s.5).
import { useEffect, useLayoutEffect, useRef, useState } from 'preact/hooks';
import { BEATS, SRC } from './beats.js';
import { SCENES, ALT } from './scenes.js';
import { useColours, useMedia, DESKTOP } from '../lib/media.js';
import { reducedMotion, tween, play } from '../lib/motion.js';
import { useFold, FoldBody } from '../components/Fold.jsx';
import { Boundary } from '../components/Boundary.jsx';
import { ONE_Q } from '../components/Lead.jsx';
import './explainer.css';

export const XOPTIONS = [['a', 'A · Scroll'], ['b', 'B · Steps']];
const TITLE = 'How the figure is worked out';

const lerp = (a, b, f) => a + (b - a) * f;
const clamp01 = x => Math.max(0, Math.min(1, x));
const LOG = new Set(['n']);   // the crowd grows by tens: mixed on a log scale, so each tenfold takes the same scroll
function mix(a, b, f) {
  const o = {};
  for (const k in a) o[k] = typeof a[k] === 'number' && typeof b[k] === 'number' ? (LOG.has(k) ? Math.exp(lerp(Math.log(a[k]), Math.log(b[k]), f)) : lerp(a[k], b[k], f)) : (f < 0.5 ? a[k] : b[k]);
  return o;
}

// The picture between beats A and B, f of the way: one scene mixed, or two crossfaded (the old out before the new is
// fully in, so words on one never sit across words on the other at full strength).
function paint(el, layers, S, A, B, f) {
  const { dpr } = S, pw = Math.round(S.W * dpr), ph = Math.round(S.H * dpr);
  if (el.width !== pw || el.height !== ph) { el.width = pw; el.height = ph; }
  const ctx = el.getContext('2d');
  ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1; ctx.clearRect(0, 0, pw, ph);
  const one = (c, beat, st) => { c.setTransform(dpr, 0, 0, dpr, 0, 0); c.globalAlpha = 1; SCENES[beat.scene](c, S, st, beat); c.globalAlpha = 1; };
  if (A.scene === B.scene) { one(ctx, f < 0.5 ? A : B, mix(A.st, B.st, f)); return; }
  const parts = [[A, clamp01(1 - f * 1.6), 0], [B, clamp01((f - 0.375) * 1.6), 1]];
  for (const [beat, al, li] of parts) {
    if (al <= 0) continue;
    if (al >= 1) { one(ctx, beat, beat.st); continue; }
    const L = layers[li] || (layers[li] = document.createElement('canvas'));
    if (L.width !== pw || L.height !== ph) { L.width = pw; L.height = ph; }
    const c = L.getContext('2d'); c.setTransform(1, 0, 0, 1, 0, 0); c.clearRect(0, 0, pw, ph);
    one(c, beat, beat.st);
    ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = al; ctx.drawImage(L, 0, 0); ctx.globalAlpha = 1;
  }
}

// The key of marks, in words under the picture; it changes at once with the step nearest.
function Key({ items }) {
  if (!items) return <ul class="legend xp-key" aria-hidden="true" />;
  return <ul class="legend xp-key">{items.map(([k, t]) => <li key={k + t}><span class={`lg xk-${k}`} aria-hidden="true" />{t}</li>)}</ul>;
}

// The stage: the canvas sized to its box, its labels at the reader's small type size (read from the page), its colours
// the page's. `api.current.draw(i, j, f)` draws the picture between beats i and j.
function Stage({ api, onTap }) {
  const box = useRef(null), cvs = useRef(null), probe = useRef(null), layers = useRef([null, null]);
  const col = useColours();
  const [S, setS] = useState(null);
  const [near, setNear] = useState(0);
  const last = useRef([0, 0, 0]), nearRef = useRef(0);
  useLayoutEffect(() => {
    const m = () => {
      const r = box.current.getBoundingClientRect(), cs = getComputedStyle(probe.current);
      setS(s => {
        const n = { W: Math.floor(r.width), H: Math.floor(r.height), fs: parseFloat(cs.fontSize) || 13, ff: cs.fontFamily };
        return s && s.W === n.W && s.H === n.H && s.fs === n.fs && s.ff === n.ff ? s : n;
      });
    };
    const ro = new ResizeObserver(m); ro.observe(box.current); ro.observe(probe.current); m();
    return () => ro.disconnect();
  }, []);
  const draw = (i, j, f) => {
    last.current = [i, j, f];
    const el = cvs.current; if (!el || !S || !col || !S.W || !S.H) return;
    paint(el, layers.current, { ...S, col, dpr: Math.min(2, window.devicePixelRatio || 1) }, BEATS[i], BEATS[j], f);
    const n = f < 0.5 ? i : j;
    if (n !== nearRef.current) { nearRef.current = n; setNear(n); }
  };
  api.current = { draw };
  useLayoutEffect(() => { draw(...last.current); }, [S, col]);
  const b = BEATS[near];
  return (
    <div class="xp-stage">
      <div class="xp-box" ref={box} onClick={onTap}>
        <span class="xp-fs" ref={probe} aria-hidden="true">0</span>
        <Boundary what="The picture" fallback={() => <p class="muted">The picture could not be drawn.</p>}>
          <canvas ref={cvs} class="xp-c" role="img" aria-label={ALT[b.scene]} />
        </Boundary>
      </div>
      <Key items={b.key} />
    </div>
  );
}

// Every step's key and words, laid out unseen at the page's width, for their tallest (B's room on a phone).
function Measure({ r }) {
  return (
    <div class="xp-measure" ref={r} aria-hidden="true" inert>
      {BEATS.map(b => (
        <div key={b.id}>
          <Key items={b.key} />
          <div class="xp-mw">
            <h2 class="xp-h">{b.head}</h2>
            {b.fig ? <p class="xp-fig">{b.fig}</p> : null}
            {b.sub ? <p class="xp-sub">{b.sub}</p> : null}
            <span class="xp-srcb">Source</span>
          </div>
        </div>
      ))}
    </div>
  );
}

function Words({ b }) {
  const f = useFold();
  return (
    <>
      <h2 class="xp-h">{b.head}</h2>
      {b.fig ? <p class="xp-fig">{b.fig}</p> : null}
      {b.sub ? <p class="xp-sub">{b.sub}</p> : null}
      <button type="button" class="xp-srcb" {...f.btn} onClick={f.toggle}>Source</button>
      <FoldBody fold={f}><p data-sentence>{SRC[b.src]}</p></FoldBody>
    </>
  );
}

export function Explainer({ v }) {
  return v === 'b' ? <Steps /> : <Scroll />;
}

// ---- A · Scroll ------------------------------------------------------------------------------------------------------
function Scroll() {
  const desk = useMedia(DESKTOP);
  const api = useRef(null), cards = useRef([]), slot = useRef(null), main = useRef(null), meas = useRef(null);
  // On a phone the picture and its key are held at the top while the words pass under them. At a large text size the
  // key grows, so the picture gives up height to keep the room for the words at no less than two fifths of the screen;
  // the key's room is the tallest step's, so the picture does not change size between steps.
  useLayoutEffect(() => {
    const m = () => main.current && meas.current && main.current.style.setProperty('--xp-keyh', `${Math.ceil(Math.max(0, ...[...meas.current.querySelectorAll('.xp-key')].map(e => e.getBoundingClientRect().height)))}px`);
    const ro = new ResizeObserver(m); ro.observe(meas.current); m();
    return () => ro.disconnect();
  }, []);
  useEffect(() => {
    // where the reader is: the step whose middle is nearest the reading line (below the held picture on a phone, the
    // screen's middle on a desktop), and how far towards the next
    const where = () => {
      const els = cards.current.slice(0, BEATS.length);
      if (els.some(e => !e)) return 0;
      const sb = slot.current.getBoundingClientRect();
      const F = desk ? innerHeight * 0.5 : sb.bottom + (innerHeight - sb.bottom) * 0.5;
      const c = els.map(e => { const r = e.getBoundingClientRect(); return r.top + r.height / 2; });
      if (F <= c[0]) return 0;
      for (let i = 0; i < c.length - 1; i++) if (F < c[i + 1]) return i + (F - c[i]) / (c[i + 1] - c[i]);
      return c.length - 1;
    };
    let raf = 0, drawn = '';
    const frame = () => {
      raf = 0;
      let t = where();
      if (reducedMotion()) t = Math.round(t);
      const i = Math.min(BEATS.length - 2, Math.floor(t));
      // the picture holds still while a step is read, and moves between steps; a frame that would draw the same
      // picture again is not drawn
      const f = clamp01((t - i - 0.3) / 0.4), at = f === 0 ? `${i}` : f === 1 ? `${i + 1}` : `${i}:${f}`;
      if (api.current && at !== drawn) { drawn = at; api.current.draw(i, i + 1, f); }
    };
    const on = () => { if (!raf) raf = requestAnimationFrame(frame); };
    frame();
    addEventListener('scroll', on, { passive: true });
    addEventListener('resize', on);
    return () => { removeEventListener('scroll', on); removeEventListener('resize', on); cancelAnimationFrame(raf); };
  }, [desk]);
  return (
    <main class="page xp xp-a" ref={main}>
      <h1 class="xp-title">{TITLE}</h1>
      <Measure r={meas} />
      <div class="xp-slot" ref={slot}><Stage api={api} /></div>
      <ol class="xp-list">
        {BEATS.map((b, i) => <li key={b.id} class="xp-card" ref={el => { cards.current[i] = el; }}><Words b={b} /></li>)}
      </ol>
      <p class="oneq xp-oneq" data-sentence>{ONE_Q}</p>
    </main>
  );
}

// ---- B · Steps -------------------------------------------------------------------------------------------------------
function Steps() {
  const [i, setI] = useState(0);
  const api = useRef(null), cur = useRef(0), owner = useRef({}), words = useRef(null), shown = useRef([0, 0, 0]);
  const main = useRef(null), nav = useRef(null), meas = useRef(null);
  // On a phone one step is one screen: the title, the picture, its key, the words, and Back, the steps and Next held at
  // the foot, where a thumb finds Next without scrolling. The picture takes the room the rest leaves (M-spec s.23: what
  // is held in view on a short screen). The key and the words keep the room of the longest step's, measured from all
  // of them at the reader's text size, so the picture is the same size at every step and does not jump between them.
  // Where the text is too large for one screen, and at the last step, where the line on what is set aside follows the
  // words, the page scrolls, and keeps the controls' height free under its last line, so nothing is left behind them.
  useLayoutEffect(() => {
    const m = () => {
      const el = main.current; if (!el || !nav.current || !meas.current) return;
      const hi = sel => Math.max(0, ...[...meas.current.querySelectorAll(sel)].map(e => e.getBoundingClientRect().height));
      el.style.setProperty('--xp-nav', `${Math.ceil(nav.current.getBoundingClientRect().height)}px`);
      el.style.setProperty('--xp-keyh', `${Math.ceil(hi('.xp-key'))}px`);
      el.style.setProperty('--xp-wordsh', `${Math.ceil(hi('.xp-mw'))}px`);
      el.style.setProperty('--xp-top', `${Math.round(el.getBoundingClientRect().top + scrollY)}px`);
    };
    const ro = new ResizeObserver(m); ro.observe(nav.current); ro.observe(meas.current); ro.observe(document.body); m();
    return () => ro.disconnect();
  }, []);
  const draw = (a, b, f) => { shown.current = [a, b, f]; if (api.current) api.current.draw(a, b, f); };
  const go = j => {
    j = Math.max(0, Math.min(BEATS.length - 1, j));
    if (j === cur.current) return;
    // from what is on the screen now (a step interrupted half way starts from the nearer of its two)
    const [a, b, f] = shown.current, from = f < 0.5 ? a : b;
    cur.current = j; setI(j);
    tween(owner.current, 'chart', k => draw(from, j, k));
  };
  useLayoutEffect(() => { draw(0, 0, 0); }, []);
  useLayoutEffect(() => { if (words.current && i) play(words.current, 'reveal', [{ opacity: 0 }, { opacity: 1 }]); }, [i]);
  useEffect(() => {
    const k = e => {
      if (e.target.closest && e.target.closest('input, textarea, select')) return;
      if (e.key === 'ArrowRight') go(cur.current + 1); else if (e.key === 'ArrowLeft') go(cur.current - 1);
    };
    addEventListener('keydown', k);
    return () => removeEventListener('keydown', k);
  }, []);
  const b = BEATS[i], last = i === BEATS.length - 1;
  return (
    <main class="page xp xp-b" ref={main}>
      <h1 class="xp-title">{TITLE}</h1>
      <div class="xp-slot"><Stage api={api} onTap={() => go(cur.current + 1)} /></div>
      <div class="xp-side">
        <div class="xp-words" ref={words} aria-live="polite"><Words key={b.id} b={b} /></div>
        {last ? <p class="oneq xp-oneq" data-sentence>{ONE_Q}</p> : null}
        <Measure r={meas} />
        <div class="xp-nav" ref={nav}>
          <button type="button" class="xp-go" onClick={() => go(i - 1)} disabled={i === 0}>Back</button>
          <ol class="xp-dots" aria-label={`Step ${i + 1} of ${BEATS.length}`}>
            {BEATS.map((x, k) => <li key={x.id}><button type="button" class={k === i ? 'on' : k < i ? 'past' : ''} aria-label={`Step ${k + 1}: ${x.head}`} aria-current={k === i ? 'step' : null} onClick={() => go(k)} /></li>)}
          </ol>
          <button type="button" class="xp-go xp-next" onClick={() => go(i + 1)} disabled={last}>Next</button>
        </div>
      </div>
    </main>
  );
}
