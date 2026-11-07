// pipeline/intake/render_scroll.cjs: render one public page in the installed headless Chromium, scrolling down until
// the page stops adding what it lists, and save what it shows.
//
//   node pipeline/intake/render_scroll.cjs URL OUT.html SELECTOR [WAIT_MS]
//
// Written 2026-11-07 by worker D3 for pipeline/intake/va_elect.py, on the orchestrator's ruling (08:00 UTC): a state
// site that has not refused us but serves only a script shell may be read as a browser reads it, in the Chromium that
// is installed in the session (require('playwright'); nothing is installed), one page at a time, through the session's
// proxy. It is pipeline/intake/render_page.cjs (worker D4's) with one addition: Virginia's results site lists the
// first 50 contests of an election and adds the rest as the reader scrolls down, so the page is scrolled to its end,
// and again, until the count of elements matching SELECTOR (one per contest) stops growing.
// What it does not do: no click, no form, no second address, no change of the browser's own user agent, no retry, no
// call of the site's data addresses (the page's own script makes those, as it does for any reader). A status of 400 or
// more, or a redirect to another site, exits 3 and writes nothing: the page is recorded as unread (_COMMON 6, 13).
// It prints "STATUS <http status> <final url> ITEMS <count>".
// *Reason:* getting round a site's refusal is not ours to do; a page that only needs a script run, or a scroll, is
// not a refusal.
const fs = require('fs');
const { chromium } = require('playwright');

(async () => {
  const [url, out, selector, waitArg] = process.argv.slice(2);
  if (!url || !out || !selector) {
    console.error('usage: node render_scroll.cjs URL OUT.html SELECTOR [WAIT_MS]');
    process.exit(2);
  }
  const wait = parseInt(waitArg || '5000', 10);
  const proxy = process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined;
  const browser = await chromium.launch({ proxy });
  try {
    const page = await (await browser.newContext({ viewport: { width: 1280, height: 2000 } })).newPage();
    const resp = await page.goto(url, { waitUntil: 'load', timeout: 90000 });
    try { await page.waitForLoadState('networkidle', { timeout: 30000 }); } catch (e) { /* never idles: go on */ }
    await page.waitForTimeout(wait);
    const status = resp ? resp.status() : 0;
    const finalUrl = page.url();
    const site = (u) => new URL(u).hostname.split('.').slice(-2).join('.');
    let last = -1;
    let n = 0;
    for (let i = 0; i < 100; i++) {   // 100 scrolls at most
      n = await page.evaluate((s) => document.querySelectorAll(s).length, selector);
      if (n === last) break;
      last = n;
      await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
      await page.waitForTimeout(2500);
    }
    console.log('STATUS ' + status + ' ' + finalUrl + ' ITEMS ' + n);
    if (status >= 400 || site(finalUrl) !== site(url)) { process.exit(3); }
    fs.writeFileSync(out, await page.content());
  } finally {
    await browser.close();
  }
})().catch((e) => { console.error('RENDER FAILED: ' + e.message); process.exit(1); });
