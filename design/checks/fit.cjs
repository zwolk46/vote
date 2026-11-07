// The fit check for the first-screen candidates (design/DESIGN-SPEC.md §6; brief X1, step 4). It loads each candidate
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
//   SCHEMES=light,dark      FAST=1 (390 and 900 and 1280; 1x and 2x)      ONLY=a,b-set   views by name
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
const MAX = Number(process.env.MAX || 8);
const SHOTS = process.env.SHOTS || null;
const DESK = 900;
const SHORT = [[390, 664], [360, 640], [1280, 720]];

// The views: each candidate as it arrives, and in the state where it shows the most (the other reading; stakes set and
// the trip filled; the field scrolled to a stop), since what a state shows is only measured when it is shown.
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
  { name: 'c', v: 'c' },
  { name: 'c-stop', v: 'c', act: page => page.evaluate(() => document.querySelectorAll('.oc-step')[2].scrollIntoView({ block: 'center' })) },
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
          await page.goto(`${base}/?v=${v.v}`, { waitUntil: 'networkidle' });
          await page.waitForTimeout(900);
          if (v.act) { await v.act(page); await page.waitForTimeout(700); }
          const res = await page.evaluate(probe, { scope: null, squeeze: false });
          let n = 0;
          for (let i = 0; i < 3; i++) { const k = await page.evaluate(openFolds, null); if (!k) break; n += k; await page.waitForTimeout(150); }
          if (n) {
            await page.evaluate(afterOpening, null);
            if (v.act && v.name === 'c-stop') await v.act(page);
            const more = await page.evaluate(probe, { scope: null, squeeze: false });
            const key = f => `${f.kind}|${f.el}|${f.what}`, had = new Set(res.out.map(key));
            res.out.push(...more.out.filter(f => !had.has(key(f))).map(f => ({ ...f, folds: true })));
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
