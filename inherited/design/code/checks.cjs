// Every check, one after another, against one build: `npm run checks`.
// Why: the orchestrator, 22:10 UTC 11-05, "The goal is for `npm run checks`, or whatever runs them all, to be green on
// main, so a red result means something." Each check takes its address its own way and some always failed, so a red
// one was read as the usual red; one command that runs them all, and fails when any fails, makes red the exception.
//
// It runs the unit tests (`npm test`), builds once (`npm run build`), serves dist/ with Vite's preview on a free port,
// and runs each browser check against that one server, each given the address the way it reads it (BASE in the
// environment, or its first argument; motion.check always serves dist/ itself, which is the same files).
// It prints a line for each check as it ends, and a failing check's FAIL lines under it. It exits 1 when any check
// fails by a FAIL line, a non-zero exit, a crash or its time running out, so a gate needs only the exit.
//
// Each check's own output goes to OUT/<name>.log and its pictures to OUT/<name>/ (OUT: the system's temp dir by
// default), so two checks never write over each other's files; the build's goes to OUT/build.log.
// Options, in the environment (named apart from the checks' own ONLY, S, W and CASES, which pass through to them):
//   CHECKS=pages,pane   only these checks, by the names below      CHECKS_SKIP=latency   all but these
//   NOBUILD=1           serve dist/ as it stands, no build          FIT=full   the whole fit check (about 13 minutes),
//                                                                              not its quick pass (FAST=1, about 130 s; both
//                                                                              measure each view again with its folds open)
// The checks run one at a time: latency and motion measure in ms with the CPU slowed, and another run beside them moves
// their numbers. Run it on a machine doing nothing else.
const { spawn, spawnSync } = require('node:child_process');
const { mkdirSync, createWriteStream, writeFileSync } = require('node:fs');
const { tmpdir } = require('node:os');
const path = require('node:path');

const ROOT = path.join(__dirname, '..');
const OUT = process.env.OUT || path.join(tmpdir(), 'midterms-checks');
const names = v => (v ? new Set(v.split(',').map(s => s.trim()).filter(Boolean)) : null);
const ONLY = names(process.env.CHECKS), SKIP = names(process.env.CHECKS_SKIP) || new Set();
const LIMIT = 30 * 60 * 1000;   // a check that runs past this has hung (the whole fit check takes about 13 minutes)
const npm = process.platform === 'win32' ? 'npm.cmd' : 'npm';

// name, then how it is run given the server's address: [command, args, env]. `dir` is the check's own OUT.
const CHECKS = [
  ['unit', () => [npm, ['test', '--silent'], {}]],
  ['review', (base, dir) => ['node', ['src/test/review.check.cjs'], { BASE: base, OUT: dir }]],
  ['replay.glide', (base, dir) => ['node', ['src/test/replay.glide.check.cjs'], { BASE: base, OUT: dir }]],
  ['pane', (base, dir) => ['node', ['src/test/pane.check.cjs', `${base}/?fixtures=script`], { OUT: dir }]],
  ['callbanner', (base, dir) => ['node', ['src/test/callbanner.check.cjs'], { BASE: base, SHOTS: dir }]],
  ['trail', (base, dir) => ['node', ['src/test/trail.check.cjs'], { BASE: base, OUT: dir }]],
  ['standin', (base, dir) => ['node', ['src/test/standin.check.cjs'], { BASE: base, OUT: dir }]],
  ['skeleton', (base, dir) => ['node', ['src/test/skeleton.check.cjs', base], { OUT: dir }]],
  ['pages', (base, dir) => ['node', ['src/test/pages.check.cjs'], { BASE: base, OUT: dir }]],
  ['motion', () => ['node', ['src/test/motion.check.cjs'], {}]],   // serves dist/ itself, on its own port
  ['latency', base => ['node', ['src/test/latency.check.cjs', base], {}]],
  // the fit check takes a BASE on localhost as this checkout's build, so it checks the door too (rendered from lib/gate)
  ['fit', base => ['node', ['scripts/fitcheck.cjs'], { BASE: base, ...(process.env.FIT === 'full' ? {} : { FAST: '1' }) }]],
];

function run(name, [cmd, args, env]) {
  return new Promise(resolve => {
    const log = createWriteStream(path.join(OUT, `${name}.log`));
    const t0 = Date.now();
    let text = '', timedOut = false;
    const child = spawn(cmd, args, { cwd: ROOT, env: { ...process.env, ...env } });
    const timer = setTimeout(() => { timedOut = true; child.kill('SIGKILL'); }, LIMIT);
    const take = d => { text += d; log.write(d); };
    child.stdout.on('data', take); child.stderr.on('data', take);
    let done = false;
    child.on('error', e => { take(`\n${e.stack || e}\n`); finish(-1, null); });   // could not start: 'close' may never come
    child.on('close', (code, signal) => finish(code, signal));
    function finish(code, signal) {
      if (done) return; done = true;
      clearTimeout(timer); log.end();
      const lines = text.split('\n');
      const fails = lines.filter(l => /^FAIL\b/.test(l) || /^not ok\b/.test(l));
      const oks = lines.filter(l => /^ok\b/.test(l)).length;
      const tap = k => { const m = text.match(new RegExp(`^# ${k} (\\d+)`, 'm')); return m ? Number(m[1]) : null; };
      const last = lines.map(l => l.trim()).filter(Boolean).pop() || '';
      const bad = timedOut || code !== 0 || fails.length > 0;
      const said = tap('pass') !== null ? `${tap('pass')} pass, ${tap('fail')} fail`
        : oks || fails.length ? `${oks} ok, ${fails.length} FAIL` : bad ? 'no result line' : last.slice(0, 90);
      const how = timedOut ? `ran past ${LIMIT / 60000} min, stopped` : signal ? `killed by ${signal}` : `exit ${code}`;
      console.log(`${bad ? 'FAIL' : 'ok  '} ${name.padEnd(13)} ${String(Math.round((Date.now() - t0) / 1000)).padStart(5)} s   ${said}; ${how}`);
      for (const l of fails.slice(0, 12)) console.log(`       ${l.slice(0, 200)}`);
      if (fails.length > 12) console.log(`       ... and ${fails.length - 12} more (${path.join(OUT, `${name}.log`)})`);
      // a crash ends on Node's version line: say the error itself (the first line naming one), then where the log is
      const why = lines.map(l => l.trim()).find(l => /\b(\w*Error|Timeout|exceeded|ECONNREFUSED|ENOENT)\b/.test(l) && !/^(at |node:internal|name: )/.test(l)) || last;
      if (bad && !fails.length) console.log(`       ${why.slice(0, 200)} (${path.join(OUT, `${name}.log`)})`);
      resolve({ name, bad });
    }
  });
}

(async () => {
  mkdirSync(OUT, { recursive: true });
  const todo = CHECKS.filter(([n]) => (!ONLY || ONLY.has(n)) && !SKIP.has(n));
  const unknown = [...(ONLY || []), ...SKIP].filter(n => !CHECKS.some(([c]) => c === n));
  if (unknown.length) { console.error(`no check named ${unknown.join(', ')}; the checks are ${CHECKS.map(([n]) => n).join(', ')}`); process.exit(2); }
  const results = [];
  let server = null;
  try {
    for (const [name, how] of todo.filter(([n]) => n === 'unit')) results.push(await run(name, how()));
    const browser = todo.filter(([n]) => n !== 'unit');
    if (browser.length) {
      if (!process.env.NOBUILD) {
        // the build's own words (Vite's chunk-size and "use client" warnings, 30 KB of them) go to its log, not between the
        // checks' lines; a failed build fails the run, as no browser check can stand without it
        const t0 = Date.now();
        const b = spawnSync(npm, ['run', 'build', '--silent'], { cwd: ROOT, encoding: 'utf8', maxBuffer: 256 * 1024 * 1024 });
        writeFileSync(path.join(OUT, 'build.log'), `${b.stdout || ''}${b.stderr || ''}${b.error ? `\n${b.error.stack}\n` : ''}`);
        const secs = String(Math.round((Date.now() - t0) / 1000)).padStart(5);
        if (b.status !== 0) {
          console.log(`FAIL ${'build'.padEnd(13)} ${secs} s   exit ${b.status} (${path.join(OUT, 'build.log')})`);
          for (const l of `${b.stderr || ''}${b.error ? b.error.message : ''}`.trim().split('\n').slice(-12)) console.log(`       ${l.slice(0, 200)}`);
          process.exit(1);
        }
        console.log(`ok   ${'build'.padEnd(13)} ${secs} s   built dist/ (its log: ${path.join(OUT, 'build.log')})`);
      }
      const { preview } = await import('vite');
      server = await preview({ root: ROOT, preview: { port: 0, host: '127.0.0.1' }, logLevel: 'silent' });
      const base = server.resolvedUrls.local[0].replace(/\/$/, '');
      for (const [name, how] of browser) {
        const dir = path.join(OUT, name); mkdirSync(dir, { recursive: true });
        results.push(await run(name, how(base, dir)));
      }
    }
  } finally {
    if (server) await new Promise(r => server.httpServer.close(r));
  }
  const bad = results.filter(r => r.bad).map(r => r.name);
  console.log(bad.length ? `\n${bad.length} of ${results.length} checks failed: ${bad.join(', ')} (logs in ${OUT})` : `\nall ${results.length} checks pass (logs in ${OUT})`);
  process.exit(bad.length ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
