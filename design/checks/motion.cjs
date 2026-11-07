// The motion check for the first-screen candidates (design/DESIGN-SPEC.md §4 and §6; brief X1, step 4: "motion
// measured with the motion.js tokens"), and for the explainer's (brief X2: the same checks). *Reason:* M-motion's rules (inherited/design/specs/MOTION-SPEC.md) are the
// maker's defaults here, and a motion is only known to keep them when it is measured in a browser.
//
// What it measures, at 390 x 844 with the CPU slowed 4x (a mid phone) and at 1280 x 900 unslowed:
//   tokens    every animation the page starts carries its token's duration (segment 300, chart 450, reveal 160), and
//             animates transform or opacity only;
//   frames    the canvas motions drawn frame by frame (V1 the arrival, 680 ms; V2 and V3, 450 ms): the
//             gaps between frames, their 95th percentile and the longest, and the motion's length end to end;
//   reduced   with reduced motion, no transform animation starts, and the canvas is at its end in the first frame;
//   idle      three seconds after arrival nothing moves: no animation running and no frame requested.
// Run: `npm run build && node design/checks/motion.cjs`. FAIL lines name a breach; the rest is the measure.
const path = require('node:path');
const { execSync } = require('node:child_process');
let pw;
try { pw = require('playwright'); } catch { pw = require(path.join(execSync('npm root -g').toString().trim(), 'playwright')); }

const TOKENS = { 'nav-in': 680, chart: 450, segment: 300, reveal: 160 };
const ALLOWED = new Set(['transform', 'opacity', 'offset', 'easing', 'composite', 'computedOffset']);
let fails = 0;
const fail = s => { fails++; console.log(`FAIL ${s}`); };

// In the page before its scripts: a record of every animation started and every frame requested.
const INIT = `(() => {
  window.__anims = []; window.__frames = 0;
  const animate = Element.prototype.animate;
  Element.prototype.animate = function (k, o) { const a = animate.call(this, k, o); const kf = Array.isArray(k) ? k : [];
    window.__anims.push({ id: a.id || '', dur: typeof o === 'object' ? o.duration : o, props: [...new Set(kf.flatMap(f => Object.keys(f)))], cls: this.className && this.className.baseVal === undefined ? String(this.className) : '' });
    setTimeout(() => { window.__anims[window.__anims.length - 1].id = a.id || ''; }, 0); return a; };
  const raf = window.requestAnimationFrame.bind(window);
  window.__stamps = []; window.__t0 = null;
  for (const t of ['pointerdown', 'keydown', 'change', 'input', 'wheel']) addEventListener(t, () => { if (window.__t0 == null) window.__t0 = performance.now(); }, true);
  window.requestAnimationFrame = cb => { window.__frames++; return raf(t => { window.__stamps.push(t); cb(t); }); };
})();`;

const gaps = st => { const g = []; for (let i = 1; i < st.length; i++) g.push(st[i] - st[i - 1]); g.sort((a, b) => a - b); return g; };
const p95 = g => (g.length ? g[Math.min(g.length - 1, Math.floor(g.length * 0.95))] : 0);
const fmt = (st, t0) => { const g = gaps(st); return st.length < 2 ? 'no frames' : `${t0 != null ? `first frame ${Math.round(st[0] - t0)} ms after the press, ` : ''}${st.length} frames over ${Math.round(st[st.length - 1] - st[0])} ms, gaps p95 ${p95(g).toFixed(1)} ms, longest ${g[g.length - 1].toFixed(1)} ms`; };
// M-motion s.4.11 and 12, as DESIGN-SPEC §6 reads them: the first moved frame within 150 ms of the press on the phone
// profile (100 on the desktop), and no gap between frames over 50 ms
const judge = (tag, what, st, t0, phone) => {
  if (st.length < 2) return;
  const g = gaps(st), longest = g[g.length - 1], lim = phone ? 150 : 100;
  if (longest > 50) fail(`${tag} ${what}: a gap of ${longest.toFixed(1)} ms between frames (over 50)`);
  if (t0 != null && st[0] - t0 > lim) fail(`${tag} ${what}: first frame ${Math.round(st[0] - t0)} ms after the press (over ${lim})`);
};

(async () => {
  const { preview } = await import('vite');
  const server = await preview({ preview: { port: 0, host: '127.0.0.1' }, build: { outDir: process.env.DIST || 'dist' }, logLevel: 'silent' });
  const base = server.resolvedUrls.local[0].replace(/\/$/, '');
  const browser = await pw.chromium.launch();

  for (const [w, h, slow] of [[390, 844, 4], [1280, 900, 1]]) {
    for (const reduce of [false, true]) {
      const tag = `${w}px${slow > 1 ? ` cpu/${slow}` : ''}${reduce ? ' reduced' : ''}`;
      const ctx = await browser.newContext({ viewport: { width: w, height: h }, reducedMotion: reduce ? 'reduce' : 'no-preference', deviceScaleFactor: 1, hasTouch: w < 900 });
      await ctx.addInitScript(INIT);
      const open = async v => {
        const page = await ctx.newPage();
        if (slow > 1) { const cdp = await ctx.newCDPSession(page); await cdp.send('Emulation.setCPUThrottlingRate', { rate: slow }); }
        await page.goto(`${base}/?${v.includes('=') ? v : `v=${v}`}`, { waitUntil: 'load' });
        return page;
      };
      const stampsSince = async (page, fn, ms) => { await page.evaluate(() => { window.__stamps = []; window.__t0 = null; }); await fn(); await page.waitForTimeout(ms); const r = await page.evaluate(() => ({ st: window.__stamps.slice(), t0: window.__t0 })); const st = r.t0 == null ? r.st : r.st.filter(x => x >= r.t0 - 17); st.t0 = r.t0; return st; };
      const phone = w < 900;

      // A: the arrival (V1), the reading (V3), the cost (V2), the segment (V8), a fold (V7)
      {
        const page = await open('a');
        await page.waitForTimeout(1500);
        const arr = await page.evaluate(() => window.__stamps.slice());
        console.log(`${tag} A arrival (V1, nav-in 680): ${fmt(arr)}`);
        if (!reduce) judge(tag, 'A arrival', arr.slice(1), null, phone);
        if (reduce && arr.length > 3) fail(`${tag} A arrival: ${arr.length} frames drawn under reduced motion`);
        // the first frame recorded can be the page's own (Preact schedules its effects on a frame) before the arrival
        // starts; as the gap check above leaves it out, so does the length, when a long gap parts it from the rest
        const mv = arr.length > 2 && arr[1] - arr[0] > 50 ? arr.slice(1) : arr;
        if (!reduce && mv.length > 2 && mv[mv.length - 1] - mv[0] > 680 * 1.5) fail(`${tag} A arrival ran ${Math.round(mv[mv.length - 1] - mv[0])} ms, past 1.5 x its token`);
        const rd = await stampsSince(page, () => page.click('.seg-body .seg-t:nth-child(2)'), 900);
        console.log(`${tag} A reading (V3, chart 450): ${fmt(rd, rd.t0)}`);
        if (!reduce) judge(tag, 'A reading', rd, rd.t0, phone);
        if (reduce && rd.length > 3) fail(`${tag} A reading: ${rd.length} frames under reduced motion`);
        await page.click('.seg-body .seg-t:nth-child(1)'); await page.waitForTimeout(700);
        await page.click('.key-row .fig-btn');
        await page.waitForTimeout(300);
        const cv = await stampsSince(page, async () => { await page.fill('.cost-ed input', '30'); await page.press('.cost-ed input', 'Tab'); }, 900);
        console.log(`${tag} A cost (V2, chart 450): ${fmt(cv, cv.t0)}`);
        if (!reduce) judge(tag, 'A cost', cv, null, phone);
        await page.waitForTimeout(3000);
        const idle = await page.evaluate(async () => { const f0 = window.__frames; await new Promise(r => setTimeout(r, 1000)); return { frames: window.__frames - f0, running: document.getAnimations().filter(a => a.playState === 'running').length }; });
        console.log(`${tag} A idle: ${idle.frames} frames requested, ${idle.running} animations running in 1 s`);
        if (idle.frames || idle.running) fail(`${tag} A moves when nothing happens`);
        const an = await page.evaluate(() => window.__anims);
        for (const a of an) {
          const tok = Object.entries(TOKENS).find(([k]) => a.id === `motion:${k}`);
          const bad = a.props.filter(p => !ALLOWED.has(p));
          if (bad.length) fail(`${tag} A an animation moves ${bad.join(', ')}`);
          if (tok && a.dur !== tok[1]) fail(`${tag} A ${a.id} ran ${a.dur} ms, its token is ${tok[1]}`);
        }
        console.log(`${tag} A animations started: ${an.map(a => `${a.props.join('+')} ${a.dur} ms`).join('; ') || 'none'}`);
        if (reduce && an.some(a => a.props.includes('transform'))) fail(`${tag} A a transform animation ran under reduced motion`);
        await page.close();
      }
      // B: a stake (V5, no easing), the cost (V2 as one transform per line), the reading (V3)
      {
        const page = await open('b');
        await page.waitForTimeout(1200);
        await page.evaluate(() => { window.__anims = []; });
        const r = await page.$('.bt-range'); const box = await r.boundingBox();
        await page.mouse.move(box.x + box.width * 0.2, box.y + box.height / 2); await page.mouse.down();
        for (let i = 0; i < 10; i++) await page.mouse.move(box.x + box.width * (0.2 + i * 0.04), box.y + box.height / 2);
        await page.mouse.up();
        const drag = await page.evaluate(() => window.__anims.length);
        console.log(`${tag} B stake drag (V5, none): ${drag} animations started`);
        if (drag) fail(`${tag} B a stake drag started an animation`);
        await page.click('.key-row .fig-btn'); await page.waitForTimeout(300);
        await page.fill('.cost-ed input', '30'); await page.press('.cost-ed input', 'Tab'); await page.waitForTimeout(700);
        const an = await page.evaluate(() => window.__anims);
        const sh = an.filter(a => a.props.includes('transform') && a.dur === 450);
        console.log(`${tag} B cost (V2, chart 450): ${sh.length} line layers moved${an.length ? `; all started: ${an.map(a => `${a.props.join('+')} ${a.dur} ms`).join('; ')}` : ''}`);
        if (!reduce && sh.length < 3) fail(`${tag} B the cost moved ${sh.length} line layers, not 3`);
        if (reduce && sh.length) fail(`${tag} B the cost moved line layers under reduced motion`);
        const rd = await stampsSince(page, () => page.click('.seg-body .seg-t:nth-child(2)'), 900);
        console.log(`${tag} B reading (V3, chart 450): ${fmt(rd, rd.t0)}`);
        if (!reduce) judge(tag, 'B reading', rd, rd.t0, phone);
        await page.close();
      }
      // The explainer (brief X2). B: each step's picture moves on `chart` (450 ms) from the press, and its words arrive on
      // `reveal`; under reduced motion each step is drawn at once. A: the picture follows the scroll frame by frame with no
      // duration of its own; nothing moves once the scroll stops.
      {
        const page = await open('page=how&v=b');
        await page.waitForTimeout(1200);
        await page.evaluate(() => { window.__anims = []; });
        let worst = 0, worstAt = '', longRun = 0, n = 0, over = 0;
        for (let i = 0; i < 21; i++) {
          const st = await stampsSince(page, () => page.click('.xp-next'), 800);
          if (st.length < 2) continue;
          n++;
          const g = gaps(st), run = st[st.length - 1] - st[0];
          if (g[g.length - 1] > worst) { worst = g[g.length - 1]; worstAt = `step ${i + 1} to ${i + 2}`; }
          longRun = Math.max(longRun, run);
          if (!reduce) judge(tag, `explainer B step ${i + 1} to ${i + 2}`, st, st.t0, phone);
          if (reduce && st.length > 3) over++;
        }
        console.log(`${tag} explainer B steps (chart 450): ${n} steps drawn; longest gap ${worst.toFixed(1)} ms (${worstAt}); longest run ${Math.round(longRun)} ms`);
        if (!reduce && longRun > 450 * 1.5) fail(`${tag} explainer B a step ran ${Math.round(longRun)} ms, past 1.5 x its token`);
        if (reduce && over) fail(`${tag} explainer B ${over} steps drawn over several frames under reduced motion`);
        const an = await page.evaluate(() => window.__anims);
        for (const a of an) {
          const tok = Object.entries(TOKENS).find(([k]) => a.id === `motion:${k}`);
          const bad = a.props.filter(p => !ALLOWED.has(p));
          if (bad.length) fail(`${tag} explainer B an animation moves ${bad.join(', ')}`);
          if (tok && a.dur !== tok[1]) fail(`${tag} explainer B ${a.id} ran ${a.dur} ms, its token is ${tok[1]}`);
        }
        console.log(`${tag} explainer B animations started: ${[...new Set(an.map(a => `${a.props.join('+')} ${a.dur} ms`))].join('; ') || 'none'}`);
        await page.waitForTimeout(1500);
        const idle = await page.evaluate(async () => { const f0 = window.__frames; await new Promise(r => setTimeout(r, 1000)); return { frames: window.__frames - f0, running: document.getAnimations().filter(a => a.playState === 'running').length }; });
        if (idle.frames || idle.running) fail(`${tag} explainer B moves when nothing happens (${idle.frames} frames, ${idle.running} animations)`);
        await page.close();
      }
      {
        const page = await open('page=how&v=a');
        await page.waitForTimeout(1200);
        const box = page.viewportSize();
        await page.mouse.move(box.width / 2, box.height * 0.75);
        const st = await stampsSince(page, async () => { for (let i = 0; i < 90; i++) { await page.mouse.wheel(0, 90); await page.waitForTimeout(16); } }, 600);
        console.log(`${tag} explainer A scroll (no duration): ${fmt(st)}`);
        if (st.length > 2) { const g = gaps(st.slice(1)); if (g[g.length - 1] > 50) fail(`${tag} explainer A scroll: a gap of ${g[g.length - 1].toFixed(1)} ms between frames (over 50)`); }
        await page.waitForTimeout(1500);
        const idle = await page.evaluate(async () => { const f0 = window.__frames; await new Promise(r => setTimeout(r, 1000)); return { frames: window.__frames - f0, running: document.getAnimations().filter(a => a.playState === 'running').length }; });
        console.log(`${tag} explainer A idle: ${idle.frames} frames requested, ${idle.running} animations running in 1 s`);
        if (idle.frames || idle.running) fail(`${tag} explainer A moves when nothing happens`);
        await page.close();
      }
      await ctx.close();
    }
  }
  await browser.close();
  await new Promise(r => server.httpServer.close(r));
  console.log(fails ? `FAIL: ${fails} breaches` : 'ok: no breaches');
  process.exit(fails ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
