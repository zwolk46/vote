// SAMPLE CONTESTS, NOT DATA. Until the data workers' contests land (D1, D2, D3), the fields of dots on the preview are
// drawn from these: invented electorates and forecasts, run through the model's own formula, p = f(½) ÷ (2n)
// (model §3), with a Student-t forecast of 4 degrees of freedom matched on its spread (model §9.5), and for the
// presidency an invented second stage. The counts per level are invented too, of the order the sources hold
// (Klarner's state-legislative file alone has 109,093 contests, model §4). The page marks every one of them as a
// sample (design/DESIGN-SPEC.md §2.2). Seeded, so every load draws the same field.

function rng(seed) {
  let a = seed >>> 0;
  return () => { a = (a + 0x6d2b79f5) >>> 0; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
}
const logU = (r, lo, hi) => lo * (hi / lo) ** r();
const gauss = r => { const u = Math.max(1e-12, r()), v = r(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); };

// The density at a dead heat of a Student-t (4 df) forecast with mean mu and standard deviation tau.
function f4(mu, tau) {
  const s = tau / Math.SQRT2, z = (0.5 - mu) / s;
  return (0.375 * (1 + z * z / 4) ** -2.5) / s;
}

// [level, count, electorate (lo, hi), lead's spread, forecast sd (lo, hi), population per voter, second stage]
const SPEC = [
  ['president', 663, [2e5, 1.4e7], 0.07, [0.02, 0.04], null, [0.01, 0.25]],
  ['senate', 841, [2.5e5, 1.2e7], 0.09, [0.03, 0.05], [1.9, 2.4], null],
  ['governor', 452, [2.5e5, 1.2e7], 0.09, [0.03, 0.05], [1.9, 2.4], null],
  ['house', 10875, [9e4, 3.6e5], 0.14, [0.04, 0.07], [700000, 780000], null],
  ['state', 24112, [2500, 9e4], 0.15, [0.05, 0.08], [2.2, 3.2], null],
  ['local', 11885, [150, 6e4], 0.12, [0.04, 0.1], [2.5, 4], null],
];

let cache = null;
// For each level: { count, logN: Float32Array (p is 1 in 10^logN), logPop: Float32Array, u: Float32Array (0..1) }
export function sampleField() {
  if (cache) return cache;
  const r = rng(20261107);
  const out = {};
  for (const [level, count, [nlo, nhi], spread, [slo, shi], popRule, stage] of SPEC) {
    const logN = new Float32Array(count), logPop = new Float32Array(count), u = new Float32Array(count);
    for (let i = 0; i < count; i++) {
      const n = logU(r, nlo, nhi);
      const mu = 0.5 + Math.abs(gauss(r)) * spread;
      const tau = slo + (shi - slo) * r();
      let p = f4(mu, tau) / (2 * n);
      if (stage) p *= logU(r, stage[0], stage[1]);
      p = Math.min(p, 0.5);
      logN[i] = -Math.log10(p);
      const pop = popRule == null ? 300e6 : popRule[0] > 1000 ? logU(r, popRule[0], popRule[1]) : n * (popRule[0] + (popRule[1] - popRule[0]) * r());
      logPop[i] = Math.log10(pop);
      u[i] = r();
    }
    out[level] = { count, logN, logPop, u };
  }
  cache = out;
  return out;
}
export const sampleTotal = () => Object.values(sampleField()).reduce((s, l) => s + l.count, 0);
