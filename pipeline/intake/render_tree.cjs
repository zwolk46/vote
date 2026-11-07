// pipeline/intake/render_tree.cjs: read a public statute viewer (Folio NXT) as a reader does, by opening its contents tree.
//
//   node pipeline/intake/render_tree.cjs URL LOG.txt STEP [STEP ...]
//   STEP is  expand:REGEX            open a folder node of the tree whose title matches, by its plus sign
//            more:REGEX=>UNTIL       press the tree's own "more" node under the node whose title matches REGEX, again and
//                                    again, until a node whose title matches UNTIL is in the tree (at most 90 presses)
//            open:REGEX=>OUT.html    click the title of the node that matches REGEX; the HTML of the document pane is
//                                    written to OUT.html
//
// Written 2026-11-07 by worker D4 for state_law.py, on the orchestrator's ruling of 08:41 UTC for New Jersey: the Legislature's
// viewer has not refused us, and opening its own contents tree is navigating a public page, as a reader would. Allowed: no
// sign-in, no form (the viewer's search box is never touched), no address typed or taken from a script, one action every few
// seconds. What it does: opens the one address (through the session's proxy, in the installed headless Chromium, with the
// browser's own user agent), then does the steps in order, TREE_WAIT_MS (default 5000) apart, each on a node that the tree
// itself shows. It writes to LOG.txt the titles of the visible nodes after each step. A node that is not in the tree, a status
// of 400 or more, a redirect to another site, or a page that no longer looks like the viewer stops the run (exit 3) with what
// was read so far: a refusal or a change of the site is recorded, never worked round (_COMMON 6, 13). Nothing is typed.
// *Reason:* the maker's rule that nothing is taken from a site that has said no, and nothing is given to a site.
const fs = require('fs');
const { chromium } = require('playwright');

const WAIT_MS = parseInt(process.env.TREE_WAIT_MS || '5000', 10);
const MAX_MORE = 90;

(async () => {
  const [url, logPath, ...steps] = process.argv.slice(2);
  if (!url || !logPath) { console.error('usage: node render_tree.cjs URL LOG.txt STEP...'); process.exit(2); }
  const proxy = process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined;
  const browser = await chromium.launch({ proxy });
  const log = [];
  const site = (u) => new URL(u).hostname.split('.').slice(-2).join('.');
  let code = 0;
  try {
    const page = await (await browser.newContext()).newPage();
    const resp = await page.goto(url, { waitUntil: 'load', timeout: 90000 });
    const settle = async () => {
      try { await page.waitForLoadState('networkidle', { timeout: 30000 }); } catch (e) { /* take what is there */ }
      await page.waitForTimeout(WAIT_MS);
    };
    await settle();
    const status = resp ? resp.status() : 0;
    log.push('STATUS ' + status + ' ' + page.url());
    console.log('STATUS ' + status + ' ' + page.url());
    if (status >= 400 || site(page.url()) !== site(url)) { code = 3; return; }
    const toc = () => page.frames().find((f) => f.url().includes('contents-frame'));
    const rows = async () => {
      const f = toc();
      if (!f) return [];
      return await f.evaluate(() => {
        const out = [];
        const walk = (ul, depth) => {
          for (const li of ul.children) {
            if (li.tagName !== 'LI') continue;
            const t = li.querySelector(':scope > span[class^="nodetext"]');
            const sub = li.querySelector(':scope > ul.childrennode');
            const mark = sub && sub.children.length ? '-' : (li.getAttribute('hc') === 'y' ? '+' : (li.classList.contains('morenode') ? '>' : ' '));
            out.push({ depth, mark, title: t ? (t.getAttribute('title') || t.textContent) : '', id: li.id });
            if (sub) walk(sub, depth + 1);
          }
        };
        const root = document.querySelector('#TOCCONTAINER ul');
        if (root) walk(root, 0);
        return out;
      });
    };
    const fmt = (r) => r.map((x) => ' '.repeat(x.depth * 2) + x.mark + ' ' + x.title + '  [' + x.id + ']').join('\n');
    // the li of the first node whose title matches, as a handle (null if none)
    const find = async (src) => (await toc().evaluateHandle((s) => {
      const re = new RegExp(s);
      const hit = [...document.querySelectorAll('#TOCCONTAINER span[class^="nodetext"]')].find((x) => re.test(x.getAttribute('title') || x.textContent));
      return hit ? hit.closest('li') : null;
    }, src)).asElement();
    log.push('--- tree at start\n' + fmt(await rows()));
    for (const step of steps) {
      const i = step.indexOf(':');
      const kind = step.slice(0, i);
      const arg = step.slice(i + 1);
      if (!toc()) { log.push('STOP: no contents frame'); code = 3; return; }
      if (kind === 'expand') {
        const el = await find(arg);
        if (!el) { log.push('STOP: no node matches ' + step); console.log('no node matches ' + step); code = 3; return; }
        const pm = await el.$(':scope > a.plusminus');
        if (!pm) { log.push('STOP: ' + step + ' has no plus sign'); code = 3; return; }
        await pm.click();
        await settle();
        log.push('--- after ' + step + '\n' + fmt(await rows()));
      } else if (kind === 'more') {
        const [parentRe, untilRe] = arg.split('=>');
        let n = 0;
        for (; n < MAX_MORE; n++) {
          if (!toc()) { log.push('STOP: no contents frame'); code = 3; return; }
          if (untilRe && await find(untilRe)) break;
          const parent = await find(parentRe);
          if (!parent) { log.push('STOP: no node matches ' + parentRe); code = 3; return; }
          const more = await parent.evaluateHandle((li) => [...li.querySelectorAll('li.morenode')].find((m) => {
            const c = m.querySelector(':scope > ul.childrennode');
            return c && !c.children.length;
          }) || null);
          const m = more.asElement();
          if (!m) break; // no "more" node left
          await (await m.$(':scope > a.plusminus')).click();
          await settle();
        }
        log.push('--- after ' + step + ' (' + n + ' presses)\n' + fmt(await rows()));
      } else if (kind === 'open') {
        const [nodeRe, outPath] = arg.split('=>');
        const el = await find(nodeRe);
        if (!el) { log.push('STOP: no node matches ' + step); console.log('no node matches ' + step); code = 3; return; }
        await (await el.$(':scope > span[class^="nodetext"]')).click();
        await settle();
        const parts = [];
        for (const fr of page.frames()) {
          if (fr === toc() || fr === page.mainFrame()) continue;
          try { parts.push('<!-- frame: ' + fr.url() + ' -->\n' + await fr.content()); } catch (e) { /* gone */ }
        }
        if (outPath) fs.writeFileSync(outPath, parts.join('\n'));
        log.push('--- opened ' + nodeRe + ' -> ' + (outPath || '(not saved)') + ' (' + parts.reduce((a, p) => a + p.length, 0) + ' bytes of HTML)');
      } else { log.push('STOP: unknown step ' + step); code = 2; return; }
    }
  } finally {
    fs.writeFileSync(logPath, log.join('\n'));
    await browser.close();
    process.exitCode = code;
  }
})().catch((e) => { console.error('RENDER FAILED: ' + e.message); process.exit(1); });
