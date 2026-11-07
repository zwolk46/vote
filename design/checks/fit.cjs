// The fit check for the first-screen candidates (design/DESIGN-SPEC.md §6; brief X1, step 4), and for the explainer's
// (brief X2: the same checks). It loads each candidate
// in a real browser at the phone widths and text sizes and the desktop widths, light and dark, and measures it with the
// midterms probe (design/checks/probe.cjs, taken whole from inherited/design/code/fitcheck.cjs): a page that scrolls
// sideways, text or a picture past the screen's edge, text cut without an ellipsis, a word broken inside itself where
// it could fit whole, text drawn over text, controls or pictures crossing, a picture cut by its box. Each view is
// measured as it arrives and again with every fold open. *Reason:* the maker's corrections on midterms ("catch things
// like this yourself, cut off on mobile", 11-05 19:28 UTC) apply here as his defaults (inherited/design/ASK.md).
//
// Run: `npm run build && node design/checks/fit.cjs` (serves dist/ on a free port with Vite's preview).
// Options by the environment:
//   W=320,360,390,430,900,1000,1100,1280,1440   widths      S=1,1.3,1.6,2   phone text scales (a desktop is checked at 1)
//   SCHEMES=light,dark      FAST=1 (390 and 900 and 1280; 1x and 2x)      ONLY=a,b-set,how-a,how-b   views by name
//   SHOTS=dir               a screenshot of each failing view               MAX=8   findings printed per view
// The short screens 390 x 664, 360 x 640 and 1280 x 720 are run too, unless W is given.
// Playwright is the machine's (the cloud sessions have it); nothing is added to package.json.
const path = require('node:path');
const fs = require('node:fs');
const { execSync } = require('node:child_process');
let pw;
try { pw = require('playwright'); } catch { pw = require(path.join(execSync('npm root -g').toString().trim(), 'playwright')); }
const { scaleText, probe, openFolds, afterOpening } = require('./probe.cjs');

const FAST = !!process.env.FAST;
const WIDTHS = (process.env.W || (FAST ? '390,900,1280' : '320,360,390,430,900,1000,1100,1280,1440')).split(',').map(Number);
const SCALES = (process.env.S || (FAST ? '1,2' : '1,1.3,1.6,2')).split(',').map(Number);
const SCHEMES = (process.env.SCHEMES || 'light,dark').split(',');
const ONLY = process.env.ONLY ? new Set(process.env.ONLY.split(',')) : null;
// the explainer's steps, counted from its source, so a step added or taken away is still checked
const STEPS = (fs.readFileSync(path.join(__dirname, '../../src/explainer/beats.js'), 'utf8').match(/^  \{ id: '/gm) || []).length;
const MAX = Number(process.env.MAX || 8);
const SHOTS = process.env.SHOTS || null;
const DESK = 900;
const SHORT = [[390, 664], [360, 640], [1280, 720]];

// The views: each candidate as it arrives, and in the state where it shows the most (the other reading; stakes set and
// the trip filled), since what a state shows is only measured when it is shown.
const setStakes = async page => page.evaluate(() => {
  const rs = document.querySelectorAll('.bt-range');
  [4.3, 3.7, 3.0].forEach((v, i) => { if (rs[i]) { rs[i].value = v; rs[i].dispatchEvent(new Event('input', { bubbles: true })); } });
});
const VIEWS = [
  { name: 'a', v: 'a' },
  { name: 'a-person', v: 'a', act: page => page.click('.seg-body .seg-t:nth-child(2)') },
  { name: 'b', v: 'b' },
  { name: 'b-set', v: 'b', act: setStakes },
  { name: 'b-person', v: 'b', act: async page => { await page.click('.seg-body .seg-t:nth-child(2)'); await setStakes(page); } },
  // the explainer (brief X2): A at its top, at the tie's halves, at the weighing, at its end; B at every step, since its
  // words and the picture's key change at each
  { name: 'how-a', q: 'page=how&v=a', states: ['top', 2, 15, 'end'], to: async (page, s) => page.evaluate(s => {
    if (s === 'top') return scrollTo(0, 0);
    if (s === 'end') return scrollTo(0, document.documentElement.scrollHeight);
    const c = document.querySelectorAll('.xp-card')[s], slot = document.querySelector('.xp-slot'), desk = innerWidth >= 900;
    const sb = desk ? 0 : slot.offsetHeight, F = desk ? innerHeight * 0.5 : sb + (innerHeight - sb) * 0.5, r = c.getBoundingClientRect();
    scrollBy(0, r.top + r.height / 2 - F);
  }, s) },
  { name: 'how-b', q: 'page=how&v=b', states: Array.from({ length: STEPS }, (_, i) => i), to: async (page, i) => page.evaluate(i => document.querySelectorAll('.xp-dots button')[i].click(), i) },
].filter(v => !ONLY || ONLY.has(v.name));

const installScale = s => `(() => { const scale = ${scaleText.toString()}; const s = ${s}; if (s === 1) return;
  const run = () => scale(s);
  new MutationObserver(run).observe(document, { childList: true, subtree: true });
  document.addEventListener('load', e => { if (e.target.tagName === 'LINK') run(); }, true);
  document.addEventListener('readystatechange', run); })();`;

(async () => {
  const { preview } = await import('vite');
  const server = await preview({ preview: { port: 0, host: '127.0.0.1' }, build: { outDir: process.env.DIST || 'dist' }, logLevel: 'silent' });
  const base = server.resolvedUrls.local[0].replace(/\/$/, '');
  const browser = await pw.chromium.launch();
  let fails = 0, views = 0;
  const t0 = Date.now();
  for (const scheme of SCHEMES) {
    // each width at each of its text sizes, then the short screens (M-spec s.23) at 1x, where what is held in view (the
    // ballot's trip, the field of runs) takes the largest share of the screen
    const combos = [];
    for (const w of WIDTHS) for (const s of (w >= DESK ? [1] : SCALES)) combos.push([w, w >= DESK ? 900 : 760, s]);
    if (!process.env.W) combos.push(...SHORT.map(([w, h]) => [w, h, 1]));
    for (const [w, h, s] of combos) {
      {
        const ctx = await browser.newContext({ viewport: { width: w, height: h }, colorScheme: scheme, deviceScaleFactor: 1, hasTouch: w < DESK });
        await ctx.addInitScript(installScale(s));
        for (const v of VIEWS) {
          const page = await ctx.newPage();
          const errs = []; page.on('pageerror', e => errs.push(String(e))); page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
          await page.goto(`${base}/?${v.q || `v=${v.v}`}`, { waitUntil: 'networkidle' });
          await page.waitForTimeout(900);
          if (v.act) { await v.act(page); await page.waitForTimeout(700); }
          const res = { out: [] }, key = f => `${f.kind}|${f.el}|${f.what}`, had = new Set();
          for (const st of v.states || [null]) {
            if (st != null) { await v.to(page, st); await page.waitForTimeout(600); }
            const tag = st != null ? ` (at ${st})` : '';
            const first = await page.evaluate(probe, { scope: null, squeeze: false });
            for (const f of first.out) if (!had.has(key(f))) { had.add(key(f)); res.out.push({ ...f, what: f.what + tag }); }
            let n = 0;
            for (let i = 0; i < 3; i++) { const k = await page.evaluate(openFolds, null); if (!k) break; n += k; await page.waitForTimeout(150); }
            if (n) {
              await page.evaluate(afterOpening, null);
              const more = await page.evaluate(probe, { scope: null, squeeze: false });
              for (const f of more.out) if (!had.has(key(f))) { had.add(key(f)); res.out.push({ ...f, what: f.what + tag, folds: true }); }
            }
          }
          for (const e of errs) res.out.push({ kind: 'error', what: e.slice(0, 160) });
          views++;
          const label = `${v.name} ${w}x${h} ${s}x ${scheme}`;
          if (res.out.length) {
            fails++;
            console.log(`FAIL ${label}: ${res.out.length} finding${res.out.length > 1 ? 's' : ''}`);
            for (const f of res.out.slice(0, MAX)) console.log(`  ${f.kind}${f.folds ? ' (folds open)' : ''}: ${f.what}${f.el ? `  [${f.el}]` : ''}`);
            if (SHOTS) { fs.mkdirSync(SHOTS, { recursive: true }); await page.screenshot({ path: path.join(SHOTS, `${v.name}-${w}-${s}x-${scheme}.png`), fullPage: true }); }
          }
          await page.close();
        }
        await ctx.close();
      }
    }
  }
  await browser.close();
  await new Promise(r => server.httpServer.close(r));
  console.log(`${fails ? 'FAIL' : 'ok'}: ${views} views, ${fails} with findings, ${Math.round((Date.now() - t0) / 1000)} s`);
  process.exit(fails ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
