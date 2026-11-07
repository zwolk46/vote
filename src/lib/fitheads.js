// A heading steps down in size where its longest word cannot fit whole on its line, and only there (W23, 11-06).
//
// Why. At 2x text on a 320 px phone a race page's heading is 44 px and its line 288 px, and "Commissioner" is 289 px
// whole, so it broke before its last letter: "Commissione / r" (/tx/railroad-commissioner). The orchestrator, 05:27 UTC
// 11-06: "A heading word broken before its last letter reads as a fault, even though the check now passes it. Let the
// heading step down in size so its longest word fits whole. Keep that to headings only, and only where a word can't fit,
// so nothing changes at default text." The PR that brought this has W23's count of production's headings it changes.
//
// How. Each h1, h2 and h3 in the app is looked at when it is drawn, when its text or its width changes, when the text
// size changes and when the fonts arrive: each of its long words, where it stands, as the browser has laid it out. A word
// is whole when its pieces stand on one line and it is no wider than the line. Where one is not, the heading's own font
// size is set down to the largest size at which every word is whole (to a quarter pixel), checked in place; everywhere
// else nothing is set, so a heading that fits is untouched. It is done in the ResizeObserver's turn, after layout and
// before paint, so the first frame a reader sees is already fitted (no jump: W19).
// Read in place, not in a hidden copy: a copy is a box put into the page, and each one made the browser lay the page out
// again before it could be read. One pass over a state's 8 headings took 9 to 17 ms with the CPU slowed fourfold, the
// latency check's phone (W23, 07:45 UTC 11-06); a heading that fits now costs only reads of a layout already done.
// Never below half its own size: a word that needs more is not one a heading should print, and the fit check fails it.
// Words end where the browser may break a line: at a space, after a hyphen or a dash. A no-break space joins (the race
// heading's "District 12", RaceCard's keepNumber), and so does a slash, after which Chrome gives no break.
// Only text drawn at the heading's own size is looked at: a smaller aside inside one (the desk calls' "Calls · desk
// times are ...") wraps as body text does.

export const SEL = 'h1, h2, h3';
const WORD = /[^ \t\n\r\f\u200b\-\u2010\u2013\u2014]+[\-\u2010\u2013\u2014]*/g;
export const MIN = 0.5;

// Where each word of a text stands, as the browser may break it: [start, end] pairs.
export function spans(text) {
  return [...String(text || '').matchAll(WORD)].map(m => [m.index, m.index + m[0].length]);
}
// The words of a text, each once.
export function words(text) {
  const t = String(text || '');
  return [...new Set(spans(t).map(([a, b]) => t.slice(a, b)))];
}

// The size a heading takes: null (its own) while its widest word fits its line; else the largest size, to a quarter
// pixel, at which that word fits (text widens in step with its size), never below MIN of its own.
export function fitSize(size, line, widest) {
  if (!(size > 0) || !(line > 0) || !(widest > line)) return null;
  return Math.max(size * MIN, Math.floor((size * line / widest) * 4) / 4);
}

// A word can be wider than its line only if its letters could be: a letter of Plex at weight 600 is at most 0.9 em,
// so a word whose length times 1.1 em is within the line is not looked at.
export const mayOverflow = (w, size, line) => w.length * size * 1.1 > line;

// A word's pieces, line by line, from its client rects, and its width: the pieces' sum. A piece an ellipsis cuts is drawn
// twice on its line, whole and cut (Chrome, 11-06), so the wider one on a line counts.
export function piecesOf(rects) {
  const lines = [];
  for (const x of rects) {
    if (!(x.width > 0.5)) continue;
    const l = lines.find(l => Math.abs(l.top - x.top) <= 2);
    if (l) l.width = Math.max(l.width, x.width); else lines.push({ top: x.top, width: x.width });
  }
  return { lines: lines.length, width: lines.reduce((s, l) => s + l.width, 0) };
}

// Widths are read as computed values (a box's used width, in CSS px to a 64th): exact, and untouched by a transform on the
// way (the navigation's motion), where a client rect is not, and a client width is rounded to the pixel.
const px = v => parseFloat(v) || 0;
function lineOf(cs) {
  const w = parseFloat(cs.width);
  if (!(w > 0)) return 0;   // not a box (display: inline or contents), or not drawn
  return cs.boxSizing === 'border-box' ? w - px(cs.paddingLeft) - px(cs.paddingRight) - px(cs.borderLeftWidth) - px(cs.borderRightWidth) : w;
}
function borderBox(cs) {
  const w = parseFloat(cs.width);
  return cs.boxSizing === 'border-box' ? w : w + px(cs.paddingLeft) + px(cs.paddingRight) + px(cs.borderLeftWidth) + px(cs.borderRightWidth);
}

export function fitHeading(h) {
  if (!h.isConnected) return;
  if (h.hasAttribute('data-fit')) { h.style.fontSize = ''; h.removeAttribute('data-fit'); }   // its own size, to look again
  if (!/\S/.test(h.textContent || '')) return;
  const cs = getComputedStyle(h);
  const size = parseFloat(cs.fontSize);
  const line = lineOf(cs);
  if (!(line > 8) || !(size > 0)) return;   // not drawn, or visually hidden (.sr)
  // the words that could be wider than the line, where they stand, in text drawn at the heading's own size
  const long = [];
  const tw = document.createTreeWalker(h, NodeFilter.SHOW_TEXT);
  for (let n; (n = tw.nextNode());) {
    const el = n.parentElement;
    if (!el || (el !== h && parseFloat(getComputedStyle(el).fontSize) !== size)) continue;
    for (const [a, b] of spans(n.data)) if (mayOverflow(n.data.slice(a, b), size, line)) long.push([n, a, b]);
  }
  if (!long.length) return;
  const range = document.createRange();
  // every long word whole, or the widest that is not, in layout pixels (the rects carry the motion's transform, k)
  const look = () => {
    const ln = lineOf(cs), bw = borderBox(cs);
    const k = bw > 0 ? h.getBoundingClientRect().width / bw : 1;
    let widest = 0;
    for (const [n, a, b] of long) {
      range.setStart(n, a); range.setEnd(n, b);
      const p = piecesOf(range.getClientRects());
      const w = k > 0 ? p.width / k : p.width;
      // a box as wide as its own text (a flex item) is as wide as its word: equal is whole, to a 64th of a pixel
      if (p.lines > 1 || w > ln + 1 / 32) widest = Math.max(widest, w);
    }
    return widest;
  };
  const widest = look();
  if (!widest) return;
  // Set as a share of its parent's size, not in pixels: a phone's text setting scales the parent, and this with it, as it
  // scales the heading's own rule (and the fit check's text scale leaves a share alone, where it scales a pixel size a
  // script writes: 87.5 px for 43.75 at 2x, W23's first try, 11-06).
  const parent = h.parentElement ? parseFloat(getComputedStyle(h.parentElement).fontSize) : 0;
  const put = v => { h.style.fontSize = parent > 0 ? `${((v / parent) * 100).toFixed(3)}%` : `${v}px`; };
  // Text does not widen exactly in step with its size (hinting, kerning, the headings' letter-spacing), so the size is
  // set on the heading and its words looked at again as it now draws them, a quarter pixel down while one is not whole.
  // Measured apart at the new size, "Representatives, 26A" came to 29.25 px and still broke on
  // /sd/sd-house-of-representatives-26a at 320 px with 1.6x text: 0.6 px too wide (W23, 06:45 UTC 11-06).
  let next = fitSize(size, line, widest) ?? size - 0.25;
  for (let i = 0; i < 8; i++) {
    put(next);
    if (next <= size * MIN || !look()) break;
    next = Math.max(size * MIN, next - 0.25);
  }
  put(next);
  h.setAttribute('data-fit', '');
}

// Watches every heading under `root` (the app): as it is drawn, as its text or width changes, as the text size changes
// (a 1 em mark in the body, observed with the headings) and as the fonts arrive.
export function watchHeadings(root) {
  if (!root || typeof ResizeObserver === 'undefined' || typeof MutationObserver === 'undefined') return () => {};
  const widths = new WeakMap();
  const mark = document.createElement('span');
  mark.setAttribute('aria-hidden', 'true');
  mark.style.cssText = 'position:absolute;visibility:hidden;width:1em;height:1em;left:0;top:0;pointer-events:none';
  document.body.appendChild(mark);
  let em = null;
  const all = () => root.querySelectorAll(SEL).forEach(fitHeading);
  const ro = new ResizeObserver(entries => {
    for (const e of entries) {
      if (e.target === mark) {
        const s = Math.round(e.contentRect.width * 100);
        const changed = em !== null && s !== em;
        em = s;
        if (changed) { all(); return; }
        continue;
      }
      // a change of height only is the heading's own (its lines, or its step down): its words and its line are as they were
      const w = Math.round(e.contentRect.width * 4);
      if (widths.get(e.target) === w) continue;
      widths.set(e.target, w);
      fitHeading(e.target);
    }
  });
  ro.observe(mark);
  const add = h => { if (!widths.has(h)) { widths.set(h, null); ro.observe(h); } };   // observing calls back once: the first fit
  root.querySelectorAll(SEL).forEach(add);
  const mo = new MutationObserver(recs => {
    const again = new Set();
    for (const r of recs) {
      const t = r.target.nodeType === 1 ? r.target : r.target.parentElement;
      if (!t) continue;
      for (const n of r.addedNodes) {
        if (n.nodeType !== 1) continue;
        if (n.matches(SEL)) add(n);
        n.querySelectorAll(SEL).forEach(add);
      }
      // a heading taken out is let go, and forgotten, so that one put back (a list re-ordered) is watched again
      const drop = x => { ro.unobserve(x); widths.delete(x); };
      for (const n of r.removedNodes) {
        if (n.nodeType !== 1) continue;
        if (n.matches(SEL)) drop(n);
        n.querySelectorAll(SEL).forEach(drop);
      }
      // text changed inside a heading already drawn (a page reused for another race, a name arriving)
      const h = t.closest && t.closest(SEL);
      if (h && widths.has(h)) again.add(h);
    }
    for (const h of again) fitHeading(h);
  });
  mo.observe(root, { childList: true, subtree: true, characterData: true });
  if (document.fonts && document.fonts.addEventListener) document.fonts.addEventListener('loadingdone', all);
  return () => { ro.disconnect(); mo.disconnect(); mark.remove(); if (document.fonts && document.fonts.removeEventListener) document.fonts.removeEventListener('loadingdone', all); };
}
