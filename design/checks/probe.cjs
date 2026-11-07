// The fit probe, taken whole from the midterms fit check (inherited/design/code/fitcheck.cjs, lines 132 to 461 as
// inherited: scaleText, probe, openFolds, afterOpening), so this site is measured by the same rules the maker's
// corrections made there (the reasons for each finding are in its comments). Nothing in these functions is changed;
// design/checks/fit.cjs is this site's driver for them. Regenerate with the extraction in fit.cjs's header if the
// inherited file changes.
function scaleText(s) {
  if (s === 1) return 0;
  let n = 0;
  const done = window.__fitScaled || (window.__fitScaled = new WeakSet());
  const rel = /^(inherit|initial|unset|revert|smaller|larger)$|^[\d.]+(em|%)$/;
  const walk = rules => { for (const r of rules) {
    if (r.cssRules) walk(r.cssRules);
    if (!r.style) continue;
    const v = r.style.getPropertyValue('font-size');
    if (v && !rel.test(v.trim())) { r.style.setProperty('font-size', `calc((${v}) * ${s})`, r.style.getPropertyPriority('font-size')); n++; }
  } };
  for (const sh of document.styleSheets) { if (done.has(sh)) continue; try { walk(sh.cssRules); done.add(sh); } catch { /* another origin's sheet, or not loaded yet */ } }
  if (!document.documentElement.dataset.fitScaled) { document.documentElement.dataset.fitScaled = '1'; document.documentElement.style.fontSize = `calc(${parseFloat(getComputedStyle(document.documentElement).fontSize) || 16}px * ${s})`; }
  // inline sizes the page's script writes: scaled once each time the script writes one (the value we wrote is remembered)
  const mine = window.__fitInline || (window.__fitInline = new WeakMap());
  for (const el of document.querySelectorAll('body [style*="font-size"]')) { const v = el.style.fontSize; if (v && !rel.test(v) && mine.get(el) !== v) { el.style.fontSize = `calc((${v}) * ${s})`; mine.set(el, el.style.fontSize); } }
  return n;
}

// The probe, in the page. Returns findings [{kind, what, at}] and the document's widths.
function probe({ scope = null, squeeze = false } = {}) {
  // Every box drawn as a reader scrolling to it sees it. A box under content-visibility: auto that is off the screen keeps
  // the size it had when last drawn (the House page's folds hold one), and the check reads the whole page at once from its
  // top: rows that changed after the fold was last drawn read as cut by it, 17 px, on production (360 px, 23:20 UTC 11-05),
  // and not again in two runs after. On the screen the box is drawn at its true size, as here. Only "auto" is undone: a box
  // a script hides with "hidden" (navmotion.js, the page being left) stays hidden.
  for (const e of document.querySelectorAll('body *')) if (getComputedStyle(e).contentVisibility === 'auto') e.style.setProperty('content-visibility', 'visible', 'important');
  const root = (scope && document.querySelector(scope)) || document.body;
  const vw = document.documentElement.clientWidth;
  const out = [];
  const seenKey = new Set();
  const add = (kind, el, what, rect) => {
    const key = `${kind}|${desc(el)}|${what}`;
    if (seenKey.has(key)) return; seenKey.add(key);
    out.push({ kind, el: desc(el), what, y: rect ? Math.round(rect.top + (document.querySelector('.page-content')?.scrollTop || 0)) : null });
  };
  function desc(el) {
    const parts = [];
    for (let e = el, i = 0; e && e !== document.body && i < 3; e = e.parentElement, i++) {
      const c = typeof e.className === 'string' && e.className.trim() ? '.' + e.className.trim().split(/\s+/).slice(0, 2).join('.') : '';
      parts.unshift(e.tagName.toLowerCase() + c);
    }
    return parts.join(' > ');
  }
  // Not seen, so not checked: display none, visibility hidden, opacity 0 on the way up, inert, aria-hidden (a closed drawer,
  // a rolled label's second copy), and the visually hidden text for screen readers (.sr, .sr-live: a 1 px box that clips).
  const hiddenCache = new Map();
  const hidden = el => {
    if (!el || el === document.documentElement) return false;
    if (hiddenCache.has(el)) return hiddenCache.get(el);
    let h = false;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || cs.visibility === 'collapse' || parseFloat(cs.opacity) < 0.05) h = true;
    else if (el.inert || el.getAttribute('aria-hidden') === 'true' && el.closest('nav,dialog,[role=dialog],.drawer,[data-drawer-navigation]') && !el.closest('[aria-hidden=false]')) h = true;
    else if (el.matches('.sr, .sr-live, .sr-only, .visually-hidden') || (cs.clip && cs.clip !== 'auto' && /rect\(0/.test(cs.clip))) h = true;
    else if (cs.clipPath && /inset\(100%|inset\(50%/.test(cs.clipPath)) h = true;
    else if (el.parentElement?.tagName === 'DETAILS' && !el.parentElement.open && el.tagName !== 'SUMMARY') h = true;   // a closed details' body
    else h = hidden(el.parentElement);
    hiddenCache.set(el, h);
    return h;
  };
  // The boxes that clip an element, nearest first: overflow hidden or clip in an axis. A box that scrolls (auto, scroll)
  // does not cut: what is in it is reached by scrolling it, so the walk stops at the first one.
  const clippers = (el, self = false) => {   // self: the element's own box clips (it holds the text)
    const list = [];
    for (let a = self ? el : el.parentElement; a && a !== document.documentElement; a = a.parentElement) {
      const cs = getComputedStyle(a);
      if (/auto|scroll/.test(cs.overflowX) || /auto|scroll/.test(cs.overflowY)) break;
      if (a.matches('.pane-el')) break;   // a sheet's window (Pane.jsx): pulled up, its content scrolls inside it   // a scroller: what is out of its view is scrolled to, and the boxes above it clip only its window
      const x = /hidden|clip/.test(cs.overflowX), y = /hidden|clip/.test(cs.overflowY);
      if (x || y) list.push({ a, x, y, cs });
      if (cs.position === 'fixed') break;
    }
    return list;
  };
  // An ellipsis that is drawn: text-overflow ellipsis, with overflow that is not visible, on the box whose lines hold the
  // text, which is the nearest box above it that is not an inline (a block, an inline-block, a flex or grid item). An
  // ellipsis further up draws nothing for it, since that box's lines hold the inner box, not its text: a race's vote count
  // in its own block under the name was cut by the name's box with no ellipsis (320 px at 2x text, 23:40 UTC 11-05), and an
  // ellipsis on a flex or grid box is on no line at all. A wrapping block ends its overflowing line in one too.
  const ellipsisBox = (el, upto) => {
    for (let e = el; e; e = e.parentElement) {
      const cs = getComputedStyle(e);
      if (cs.display === 'inline' || cs.display === 'contents') { if (e === upto) break; continue; }
      return cs.textOverflow === 'ellipsis' && cs.overflowX !== 'visible' && /^(block|inline-block|list-item|table-cell|flow-root)$/.test(cs.display) ? e : null;
    }
    return null;
  };
  const ellipsisOn = (el, upto) => Boolean(ellipsisBox(el, upto));
  // inside a box that scrolls sideways and stands within the screen (a row of chips that scrolls): reached by scrolling it
  const inScroller = el => { for (let a = el.parentElement; a && a !== document.body; a = a.parentElement) { if (/auto|scroll/.test(getComputedStyle(a).overflowX) && a.scrollWidth > a.clientWidth + 1) { const b = a.getBoundingClientRect(); if (b.left >= -1 && b.right <= vw + 1) return true; } } return false; };
  // the widest line a text's part of the page could give it: the screen (or the surface checked), less the padding, borders
  // and margins of every box the text stands in, up to the page (main) or the surface. A column's own width is not taken
  // off: columns give way (the brief, s.2), the gutters stay (a phone's 16 px each side).
  const widestLine = el => {
    const top = root !== document.body ? root : null;
    let inset = 0;
    for (let a = el; a && a !== document.body && a.tagName !== 'MAIN'; a = a.parentElement) {
      const cs = getComputedStyle(a);
      if (cs.display !== 'inline' && cs.display !== 'contents') for (const p of ['paddingLeft', 'paddingRight', 'borderLeftWidth', 'borderRightWidth', ...(a === top ? [] : ['marginLeft', 'marginRight'])]) inset += parseFloat(cs[p]) || 0;
      if (a === top) break;
    }
    return Math.max(0, (top ? Math.min(vw, top.getBoundingClientRect().width) : vw) - inset);
  };
  // a word's width set whole on one line in its own box's style: a hidden span of it in that box, measured and taken out
  // at once (unset of the box's own rules for a span, so only what the word inherits counts: its font, letter-spacing,
  // text-transform). The broken parts' boxes added up, with a pixel's give, are not it: "Commissioner" is 288.8 px whole,
  // so a 288 px heading can never hold it (320 px, 2x text, /tx/railroad-commissioner), yet its parts came within the
  // pixel and it failed (W23's sweep of production's race pages, 03:30 UTC 11-06). Null where no span can stand (SVG).
  const wholeWidth = (el, word) => {
    if (!(el instanceof HTMLElement)) return null;
    const sp = document.createElement('span');
    sp.style.cssText = 'all: unset; position: absolute; visibility: hidden; white-space: nowrap;';
    sp.textContent = word;
    el.appendChild(sp);
    const w = sp.getBoundingClientRect().width;
    sp.remove();
    return w;
  };
  // a number as the site writes one: a count, a share, a sum of money, a margin ("103,171", "58.8%", "$4.17M", "+1.2")
  const NUMBER = /^\s*[(]?[-−+]?[$]?\d[\d,.]*\s*(?:[KMB%]|pts?)?[)]?\s*$/;
  const partly = (r, lo, hi, axis) => {
    const a = axis === 'x' ? r.left : r.top, b = axis === 'x' ? r.right : r.bottom;
    const inside = Math.min(b, hi) - Math.max(a, lo);
    return inside > 0.5 && (a < lo - 1 || b > hi + 1);
  };

  // 1. Sideways scroll: the document, and the page's frame (the window does not scroll on this site; .page-content does).
  const de = document.documentElement;
  if (de.scrollWidth > de.clientWidth + 1) add('scroll', de, `the page is ${de.scrollWidth} px wide in ${de.clientWidth}`);
  for (const f of document.querySelectorAll('.page-content, main, body')) if (f.scrollWidth > f.clientWidth + 1 && /auto|scroll/.test(getComputedStyle(f).overflowX)) add('scroll', f, `${f.scrollWidth} px of content in ${f.clientWidth}`);

  // What passes under a bar fixed or stuck to the screen (the header, the sections' bar) is hidden by it, not drawn over:
  // a box that meets one, from outside it, is left out of the overlap checks (the hover views scroll a row into view, and
  // the rows above it go under the header).
  const layers = [...document.querySelectorAll('body *')].filter(e => { const p = getComputedStyle(e).position; return (p === 'fixed' || p === 'sticky') && !hidden(e); }).map(e => ({ e, b: e.getBoundingClientRect() })).filter(l => !scope && l.b.width > 40 && l.b.height > 8);   // a surface over the page (scope) is the top layer itself
  const under = (el, r) => layers.some(l => !l.e.contains(el) && Math.min(r.right, l.b.right) - Math.max(r.left, l.b.left) > 0 && Math.min(r.bottom, l.b.bottom) - Math.max(r.top, l.b.top) > 0);

  // 2-4. Text: past the screen, cut by a clipping box, broken inside a word.
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, { acceptNode: n => /\S/.test(n.data) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT });
  const textRects = [];
  const range = document.createRange();
  for (let n; (n = walker.nextNode());) {
    const el = n.parentElement;
    if (!el || el.closest('script,style,noscript,template,svg title') || hidden(el)) continue;
    range.selectNodeContents(n);
    const rects = [...range.getClientRects()].filter(r => r.width > 0.5 && r.height > 0.5);
    if (!rects.length) continue;
    const word = n.data.trim().slice(0, 40);
    const cl = clippers(el, true);
    // wholly outside a box that clips it (a folded accordion, a rolled label's other copy): not seen, so not checked
    const boxes = cl.map(c => ({ c, b: c.a.getBoundingClientRect() }));
    const seenRect = r => boxes.every(({ c, b }) => !((c.x && (r.right <= b.left + 0.5 || r.left >= b.right - 0.5)) || (c.y && (r.bottom <= b.top + 0.5 || r.top >= b.bottom - 0.5))));
    for (const r of rects.filter(seenRect)) {
      // the screen's edges (a fixed box that is wholly off the screen is a parked sheet, not a cut)
      if (partly(r, 0, vw, 'x') && !inScroller(el) && !cl.some(c => c.x && c.a.getBoundingClientRect().right <= vw + 1 && c.a.getBoundingClientRect().left >= -1)) add('past', el, `"${word}" runs ${r.left < 0 ? `${Math.round(-r.left)} px past the left edge` : `${Math.round(r.right - vw)} px past the right edge`}`, r);
      for (const { c, b } of boxes) {
        if (b.width < 2 || b.height < 2) continue;   // a 1 px box: visually hidden on purpose
        const cx = c.x && partly(r, b.left, b.right, 'x'), cy = c.y && partly(r, b.top, b.bottom, 'y');
        // An ellipsis says that the text goes on, which a name may do (the brief, s.2). A number may not: what is left of
        // "103,171" or "$4.17M" reads as another number (the live run of 23:40 UTC 11-05: a race's vote counts at 320 px,
        // 2x text). SQUEEZE=1 also fails a name left under three letters' width (3 of its em) of a longer text: "I…" for
        // "Indiana District 8" (the Surprises readout, the same run).
        const eb = cx ? ellipsisBox(el, c.a) : null, ell = Boolean(eb);
        if (ell) {
          const fs = parseFloat(getComputedStyle(el).fontSize) || 16, vis = Math.min(r.right, b.right) - Math.max(r.left, b.left);
          // drawn only where the box's line runs past it in whole pixels: a glyph's side bearing a pixel over the edge
          // ("NBC Tue 10:12 PM +1" in its 150 px) leaves the "1" whole on the screen and no ellipsis (1280 px, 00:50 UTC 11-06)
          if (r.width > vis + 1 && eb.scrollWidth > eb.clientWidth && NUMBER.test(n.data)) { add('cut', el, `"${word}", a number, is cut short by its ellipsis (${Math.round(vis)} px of its ${Math.round(r.width)} shown)`, r); break; }
          if (squeeze && vis < 3 * fs && r.width > vis + fs) { add('squeezed', el, `"${word}" shows ${Math.round(vis)} px of its ${Math.round(r.width)} before the ellipsis`, r); break; }
        }
        if ((cx || cy) && !ell) { add('cut', el, `"${word}" is cut by ${desc(c.a)} (${cx ? `${Math.round(Math.max(r.right - b.right, b.left - r.left))} px sideways` : `${Math.round(Math.max(r.bottom - b.bottom, b.top - r.top))} px down`})`, r); break; }
      }
      // what is drawn of it: the rect cut to the boxes that clip it (an ellipsis's hidden tail is not over its neighbour)
      let d = { left: r.left, right: r.right, top: r.top, bottom: r.bottom, width: 0, height: 0 };
      for (const { c, b } of boxes) { if (c.x) { d.left = Math.max(d.left, b.left); d.right = Math.min(d.right, b.right); } if (c.y) { d.top = Math.max(d.top, b.top); d.bottom = Math.min(d.bottom, b.bottom); } }
      d.width = d.right - d.left; d.height = d.bottom - d.top;
      if (d.width > 0.5 && d.height > 0.5 && !under(el, d)) textRects.push({ r: d, el });
    }
    // a word broken over two lines: a word's own rects on two lines. Words are split on spaces, hyphens, dashes and
    // slashes, where a break is a break between words. A word wider than any line its part of the page could give it
    // (widestLine) has no line to stand on whole, and its break is how it is shown whole rather than cut: the last part of
    // a web address on a 320 px phone at 2x text, "federalelections2020.xlsx", 343 px where the widest box is 320 (the race
    // page's sources, 01:35 UTC 11-06). A name in a narrow column, as the maker's "Hickenloo / per" was, has a line to
    // stand on once the columns give way, so it still fails. A heading (h1, h2, h3) has no such leave: it steps down in
    // size until its longest word fits whole (src/lib/fitheads.js), so a heading's word broken is a fault wherever it is.
    // Why: the orchestrator, 05:27 UTC 11-06, of "Commissioner" in a race page's heading, 289 px in a 288 px line at
    // 320 px and 2x text: "A heading word broken before its last letter reads as a fault, even though the check now
    // passes it."
    if (rects.length > 1) {
      const re = /[^\s\-‐–—/·|,]+/g;
      for (let m; (m = re.exec(n.data));) {
        if (m[0].length < 2) continue;
        range.setStart(n, m.index); range.setEnd(n, m.index + m[0].length);
        const wr = [...range.getClientRects()].filter(r => r.width > 0.5);
        if (!(wr.length > 1 && Math.abs(wr[wr.length - 1].top - wr[0].top) > 2)) continue;
        const whole = wholeWidth(el, m[0]) ?? wr.reduce((s, r) => s + r.width, 0);
        if (whole <= widestLine(el) || el.closest('h1, h2, h3')) add('broken', el, `"${m[0]}" breaks over two lines`, wr[0]);
      }
    }
  }
  // Faces and pictures partly past the screen or cut by a clipping box that is not their own frame.
  for (const el of root.querySelectorAll('img, .face, svg.map, canvas, video')) {
    if (hidden(el)) continue;
    const r = el.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) continue;
    if (partly(r, 0, vw, 'x') && !inScroller(el) && !clippers(el).some(c => c.x && c.a.getBoundingClientRect().right <= vw + 1 && c.a.getBoundingClientRect().left >= -1)) add('past', el, `a ${el.tagName.toLowerCase()} runs ${r.left < 0 ? `${Math.round(-r.left)} px past the left edge` : `${Math.round(r.right - vw)} px past the right edge`}`, r);
  }

  // 6. Overlap and clipped. What is drawn of a box is its rect cut to the boxes that clip it; a box wholly cut away is not
  // seen (a closed fold's rows), so not checked.
  const drawn = el => {
    const r = el.getBoundingClientRect(); const d = { left: r.left, right: r.right, top: r.top, bottom: r.bottom };
    for (const { a, x, y } of clippers(el)) { const b = a.getBoundingClientRect(); if (x) { d.left = Math.max(d.left, b.left); d.right = Math.min(d.right, b.right); } if (y) { d.top = Math.max(d.top, b.top); d.bottom = Math.min(d.bottom, b.bottom); } }
    return d.right - d.left > 0.5 && d.bottom - d.top > 0.5 ? { r, d } : null;
  };
  const cross = (a, b, min = 0.5) => Math.min(a.right, b.right) - Math.max(a.left, b.left) > min && Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top) > min;
  const related = (a, b) => a === b || a.contains(b) || b.contains(a);
  // a control wholly inside another's box is placed there on purpose (a pinned card's grip and pin in its corner)
  // a small control set over a larger one where the larger has no text (a pinned card's pin in its corner, the row's
  // title kept clear of it by its padding): the smaller is the one pressed there, and nothing of the larger is hidden
  const onNothing = (sm, lg) => (sm.d.right - sm.d.left) * (sm.d.bottom - sm.d.top) < (lg.d.right - lg.d.left) * (lg.d.bottom - lg.d.top) / 4 && !textRects.some(t => lg.el.contains(t.el) && !sm.el.contains(t.el) && cross(t.r, sm.d, 0.5));
  const inside = (a, b) => a.left >= b.left - 0.5 && a.right <= b.right + 0.5 && a.top >= b.top - 0.5 && a.bottom <= b.bottom + 0.5;
  const pics = [], ctrls = [], marks = [];
  for (const el of root.querySelectorAll('img, .face, canvas, video')) {
    if (hidden(el) || el.parentElement?.closest('.face')) continue;
    const v = drawn(el); if (!v || v.r.width < 4 || v.r.height < 4) continue;
    // a drawn layer beneath the page's words (a canvas that takes no pointer, such as the door's glass, which is see-through
    // where it holds no glass and sits under the wordmark; W18, 22:34 UTC 11-05), or any picture marked data-fit-under, is a
    // background: it is still checked for being cut, but not for crossing the text and faces drawn over it
    const under_ = el.closest('[data-fit-under]') || (el.tagName === 'CANVAS' && getComputedStyle(el).pointerEvents === 'none');
    if (!under_ && !under(el, v.d)) pics.push({ el, d: v.d });
    // a face cut by a box that clips it, partly (wholly cut is not seen); a scroller's window is not a cut
    const cut = Math.max(v.d.left - v.r.left, v.r.right - v.d.right, v.d.top - v.r.top, v.r.bottom - v.d.bottom);
    if (cut > 0.5 && !inScroller(el)) add('clipped', el, `a ${el.matches('.face') ? 'face' : el.tagName.toLowerCase()} is cut ${cut.toFixed(1)} px by the box round it`, v.r);
  }
  for (const el of root.querySelectorAll('a[href], button, input:not([type=hidden]), select, textarea, [role=button], [role=tab], [role=radio], [role=switch]')) {
    if (hidden(el) || el.closest('[aria-hidden=true]') || el.closest('svg')) continue;   // a shape in a map: its box is not its outline
    const v = drawn(el); if (!v || v.r.width < 4 || v.r.height < 4 || under(el, v.d)) continue;
    if (getComputedStyle(el).display === 'inline') { for (const r of el.getClientRects()) if (r.width > 2) ctrls.push({ el, d: r }); }
    else ctrls.push({ el, d: v.d });
  }
  // drawn marks: a box's ::before or ::after placed on its own (absolute), filled, and thin (a call's stripe, a tick)
  for (const el of root.querySelectorAll('*')) {
    for (const ps of ['::before', '::after']) {
      const cs = getComputedStyle(el, ps);
      if (cs.content === 'none' || cs.position !== 'absolute' || cs.display === 'none' || cs.visibility === 'hidden' || parseFloat(cs.opacity) < 0.05) continue;
      const bg = cs.backgroundColor; if (!bg || bg === 'transparent' || /rgba\([^)]*,\s*0\)$/.test(bg)) continue;
      const w = parseFloat(cs.width), h = parseFloat(cs.height); if (!(w > 0 && h > 0) || Math.min(w, h) > 6) continue;
      if (hidden(el)) continue;
      const es = getComputedStyle(el), b = el.getBoundingClientRect(), bl = parseFloat(es.borderLeftWidth) || 0, bt = parseFloat(es.borderTopWidth) || 0;
      const left = b.left + bl + (cs.left !== 'auto' ? parseFloat(cs.left) : (b.width - bl - (parseFloat(cs.right) || 0) - w));
      const top = b.top + bt + (cs.top !== 'auto' ? parseFloat(cs.top) : (b.height - bt - (parseFloat(cs.bottom) || 0) - h));
      marks.push({ el, ps, d: { left, top, right: left + w, bottom: top + h } });
    }
  }
  const tag = el => el.matches('.face') ? 'a face' : el.matches('img') ? 'a picture' : `"${(el.getAttribute('aria-label') || el.textContent || el.tagName).trim().slice(0, 24)}"`;
  // Pairs of boxes that share a band of the page, found by a sweep down the page: the boxes sorted by their top, each one
  // compared only with the boxes still open at its top. Comparing every box with every other took minutes on a deployment's
  // longer pages (the home page holds some 36,000 nodes), and on a phone, where all text starts at one left edge, the old
  // sweep by the left edge compared nearly every pair. `bs` given: pairs of one box from each list, in the order (a, b).
  const sweep = (as, ra, bs, rb, fn) => {
    const ev = as.map(x => ({ x, r: ra(x), s: 0 }));
    if (bs) for (const x of bs) ev.push({ x, r: rb(x), s: 1 });
    ev.sort((p, q) => p.r.top - q.r.top);
    let open = [];
    for (const e of ev) {
      if (open.length > 64) open = open.filter(o => o.r.bottom > e.r.top);
      for (const o of open) {
        if (o.r.bottom <= e.r.top) continue;
        if (!bs) fn(o.x, e.x); else if (o.s !== e.s) { if (o.s === 0) fn(o.x, e.x); else fn(e.x, o.x); }
      }
      open.push(e);
    }
  };
  sweep(pics, p => p.d, null, null, (p, q) => { if (!related(p.el, q.el) && cross(p.d, q.d)) add('overlap', p.el, `${tag(p.el)} and ${tag(q.el)} (${desc(q.el)}) cross`, p.d); });
  sweep(ctrls, c => c.d, null, null, (p, q) => { if (!related(p.el, q.el) && !inside(p.d, q.d) && !inside(q.d, p.d) && !onNothing(p, q) && !onNothing(q, p) && cross(p.d, q.d, 1)) add('overlap', p.el, `the controls ${tag(p.el)} and ${tag(q.el)} (${desc(q.el)}) cross`, p.d); });
  sweep(marks, m => m.d, ctrls, c => c.d, (m, c) => { if (!related(c.el, m.el) && cross(m.d, c.d)) add('overlap', c.el, `${tag(c.el)} is over the mark ${desc(m.el)}${m.ps}`, c.d); });
  sweep(pics, p => p.d, textRects, t => t.r, (p, t) => { if (!related(p.el, t.el) && cross(p.d, t.r, 1)) add('overlap', t.el, `${tag(p.el)} and the text "${(t.el.textContent || '').trim().slice(0, 24)}" cross`, t.r); });

  // 5. Text over text: two pieces of text whose boxes cross by more than a sliver, neither inside the other.
  sweep(textRects, t => t.r, null, null, (p, q) => {
    const w = Math.min(p.r.right, q.r.right) - Math.max(p.r.left, q.r.left);
    if (w <= 3) return;
    const h = Math.min(p.r.bottom, q.r.bottom) - Math.max(p.r.top, q.r.top);
    if (h <= Math.min(p.r.height, q.r.height) * 0.4) return;
    if (p.el === q.el || p.el.contains(q.el) || q.el.contains(p.el)) return;
    add('covers', p.el, `"${(p.el.textContent || '').trim().slice(0, 24)}" and "${(q.el.textContent || '').trim().slice(0, 24)}" (${desc(q.el)}) are drawn over each other`, p.r);
  });
  return { vw, sw: de.scrollWidth, out };
}

// Every fold in the view opened, as a reader opens it, in the page (main) or in the surface the view is of (scope):
//   an Accordion's group (Accordion.jsx: its checkbox, pressed; the House's states, the closest rows, "26 more calls");
//   a <details> (a key's note, a profile's sources, the photos' stand-ins);
//   a button that says it is folded, aria-expanded="false", and opens in place: not one that opens a menu or a card over the
//   page (aria-haspopup), nor the menu's own (data-toggle) (a race card's other candidates, "All calls and closings");
//   the site's "Show all N" (button.toggle in the page: a state's sections of more than twelve races, the pinned shelf past
//   twelve), which shows the rest of a list where it stands.
// A box not drawn (display none, visibility hidden, inert) is left: what it holds is not on this page at this width. Each is
// pressed once (a re-render that has not landed yet would read as still closed, and a second press would close it).
// Returns how many it opened.
function openFolds(scope) {
  const root = (scope && document.querySelector(scope)) || document.querySelector('main') || document.body;
  const done = window.__fitOpened || (window.__fitOpened = new WeakSet());
  const drawn = el => { for (let e = el; e && e !== document.documentElement; e = e.parentElement) { const cs = getComputedStyle(e); if (cs.display === 'none' || cs.visibility === 'hidden' || e.inert) return false; } return true; };
  let n = 0;
  const open = (el, how) => { if (done.has(el) || !drawn(el)) return; done.add(el); how(el); n++; };
  for (const t of root.querySelectorAll('.accordion .item > input.toggle[type=checkbox]')) if (!t.checked) open(t, t => t.click());
  for (const d of root.querySelectorAll('details:not([open])')) open(d, d => { d.open = true; });
  for (const b of root.querySelectorAll('button[aria-expanded="false"]:not([aria-haspopup]):not([data-toggle]), button.toggle:not([aria-expanded]):not([data-toggle])')) if (!b.disabled) open(b, b => b.click());
  return n;
}

// What opening the folds set going, ended: what the presses render (two frames), what loads on sight (the frame run to its
// bottom and back, as settle does, to its end however long the opened page is), a list still loading (aria-busy: a state's
// legislature fetches its other seats), and the folds' own motion (510 ms). An animation with no end (a pulse) is not waited for.
async function afterOpening(scope) {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
  const root = (scope && document.querySelector(scope)) || document.querySelector('main') || document.body;
  for (let i = 0; i < 100 && root.querySelector('[aria-busy="true"]'); i++) await sleep(100);
  const f = document.querySelector('.page-content') || document.scrollingElement;
  for (let y = 0; y < 200 && f.scrollTop + f.clientHeight < f.scrollHeight - 1; y++) { f.scrollTop += 700; await sleep(30); }
  f.scrollTop = 0;
  await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
  const ends = document.getAnimations().filter(a => a.playState === 'running' && Number.isFinite(a.effect?.getComputedTiming().endTime));
  await Promise.race([Promise.all(ends.map(a => a.finished.catch(() => {}))), sleep(3000)]);
  await sleep(300);
}

module.exports = { scaleText, probe, openFolds, afterOpening };
