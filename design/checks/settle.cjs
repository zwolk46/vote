// The settle check (design/DESIGN-SPEC.md §6; brief X1, step 4: "nothing jumping while loading"; brief X2: the same
// checks for the explainer, ?page=how&v=a and &v=b). Each candidate is
// loaded at 390 x 844 (the network and CPU slowed, as a phone on a fair connection) and at 1280 x 900, light and dark,
// and every layout shift from the first paint to three seconds after load is summed, as the browser's Cumulative
// Layout Shift counts them, with the elements that moved. *Reason:* a figure that moves under the reader's eye as the
// page builds is read wrong or lost; M-motion s.1 allows no motion that is not the reader's.
// Run: `npm run build && node design/checks/settle.cjs`. It fails a view whose sum passes LIMIT (0.01 by default).
const path = require('node:path');
const { execSync } = require('node:child_process');
let pw;
try { pw = require('playwright'); } catch { pw = require(path.join(execSync('npm root -g').toString().trim(), 'playwright')); }

const LIMIT = Number(process.env.LIMIT || 0.01);
const INIT = `(() => { window.__cls = 0; window.__moved = [];
  new PerformanceObserver(l => { for (const e of l.getEntries()) { if (e.hadRecentInput) continue; window.__cls += e.value;
    for (const s of e.sources || []) { const n = s.node; window.__moved.push((n && n.nodeType === 1 ? (n.className || n.tagName) : n ? n.nodeName : '?') + ' ' + e.value.toFixed(4)); } } })
    .observe({ type: 'layout-shift', buffered: true }); })();`;

(async () => {
  const { preview } = await import('vite');
  const server = await preview({ preview: { port: 0, host: '127.0.0.1' }, build: { outDir: process.env.DIST || 'dist' }, logLevel: 'silent' });
  const base = server.resolvedUrls.local[0].replace(/\/$/, '');
  const browser = await pw.chromium.launch();
  let fails = 0;
  for (const [w, h, slow] of [[390, 844, true], [1280, 900, false]]) {
    for (const scheme of ['light', 'dark']) {
      for (const v of ['a', 'b', 'page=how&v=a', 'page=how&v=b']) {
        const ctx = await browser.newContext({ viewport: { width: w, height: h }, colorScheme: scheme, deviceScaleFactor: 1 });
        await ctx.addInitScript(INIT);
        const page = await ctx.newPage();
        if (slow) {
          const cdp = await ctx.newCDPSession(page);
          await cdp.send('Network.enable');
          await cdp.send('Network.emulateNetworkConditions', { offline: false, latency: 150, downloadThroughput: (1.6 * 1024 * 1024) / 8, uploadThroughput: (750 * 1024) / 8 });
          await cdp.send('Emulation.setCPUThrottlingRate', { rate: 4 });
        }
        await page.goto(`${base}/?${v.includes('=') ? v : `v=${v}`}`, { waitUntil: 'load' });
        await page.waitForTimeout(3000);
        const r = await page.evaluate(() => ({ cls: window.__cls, moved: window.__moved.slice(0, 6) }));
        const bad = r.cls > LIMIT;
        if (bad) fails++;
        console.log(`${bad ? 'FAIL' : 'ok  '} ${v} ${w}px ${scheme}: layout shift ${r.cls.toFixed(4)}${r.moved.length ? ` (${r.moved.join('; ')})` : ''}`);
        await ctx.close();
      }
    }
  }
  await browser.close();
  await new Promise(r => server.httpServer.close(r));
  console.log(fails ? `FAIL: ${fails} views shift past ${LIMIT}` : `ok: every view under ${LIMIT}`);
  process.exit(fails ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
