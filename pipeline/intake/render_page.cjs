// pipeline/intake/render_page.cjs: render one public page in the installed headless Chromium and save what it shows.
//
//   node pipeline/intake/render_page.cjs URL OUT.html [WAIT_MS]
//
// Written 2026-11-07 by worker D4 for state_law.py, on the orchestrator's ruling (08:00 UTC): a state site that has not
// refused us but serves only a script shell may be read as a browser reads it, in the Chromium that is installed in the
// session (require('playwright'); nothing is installed), one request at a time, through the session's proxy.
// What it does: opens the one address, waits for the page and its frames to settle, writes the HTML of the page and of
// every frame (so text a script put there is in the file) to OUT.html, and prints a line "STATUS <http status> <final url>".
// What it does not do: no click, no form, no second address, no change of the browser's own user agent, no retry. A status
// of 400 or more, or a redirect to another site, exits 3 and writes nothing: the page is recorded as unread (_COMMON 6, 13).
// *Reason:* getting round a site's refusal is not ours to do; a page that only needs a script run is not a refusal.
const fs = require('fs');
const { chromium } = require('playwright');

(async () => {
  const [url, out, waitArg] = process.argv.slice(2);
  if (!url || !out) { console.error('usage: node render_page.cjs URL OUT.html [WAIT_MS]'); process.exit(2); }
  const wait = parseInt(waitArg || '4000', 10);
  const proxy = process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined;
  const browser = await chromium.launch({ proxy });
  try {
    const page = await (await browser.newContext()).newPage();
    const resp = await page.goto(url, { waitUntil: 'load', timeout: 90000 });
    try { await page.waitForLoadState('networkidle', { timeout: 30000 }); } catch (e) { /* a page that never idles: take what is there */ }
    await page.waitForTimeout(wait);
    const status = resp ? resp.status() : 0;
    const finalUrl = page.url();
    const site = (u) => new URL(u).hostname.split('.').slice(-2).join('.');
    console.log('STATUS ' + status + ' ' + finalUrl);
    if (status >= 400 || site(finalUrl) !== site(url)) { process.exit(3); }
    const parts = [];
    for (const f of page.frames()) {
      try { parts.push('<!-- frame: ' + f.url() + ' -->\n' + await f.content()); } catch (e) { /* a frame that went away */ }
    }
    fs.writeFileSync(out, parts.join('\n'));
  } finally {
    await browser.close();
  }
})().catch((e) => { console.error('RENDER FAILED: ' + e.message); process.exit(1); });
