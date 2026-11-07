// Figures in words a reader says (design/DESIGN-SPEC.md §2.1): money to two significant figures from a million, with
// the word; chances as "1 in N"; never scientific notation, never a percentage below 1%.

const sig = (x, n) => { if (x === 0) return 0; const d = Math.ceil(Math.log10(Math.abs(x))); const m = 10 ** (n - d); return Math.round(x * m) / m; };
const trim = s => s.replace(/\.0$/, '');
const WORDS = [[1e12, 'trillion'], [1e9, 'billion'], [1e6, 'million']];

// $8.87 · $29 · $4,150 · $180,000 · $1.6 million · $89 million · $8.9 billion · 30¢
export function money(x) {
  if (!(x > 0)) return '$0';
  if (x < 1) return `${Math.max(1, Math.round(x * 100))}¢`;
  if (x < 10) return `$${x.toFixed(2)}`;
  if (x < 1000) return `$${Math.round(x)}`;
  if (x < 1e6) return `$${sig(x, 3).toLocaleString('en-US')}`;
  for (const [v, w] of WORDS) if (x >= v * 0.9995) {
    const s = sig(x / v, 2);
    if (s >= 1000 && w !== 'trillion') continue;
    return `$${trim(s.toLocaleString('en-US', { maximumFractionDigits: 1 }))} ${w}`;
  }
  return `$${sig(x, 2).toLocaleString('en-US')}`;
}

// The money figure split for the display size: ['$89', 'million'], so the word can sit at a lighter weight.
export function moneyParts(x) {
  const s = money(x);
  const i = s.indexOf(' ');
  return i < 0 ? [s, ''] : [s.slice(0, i), s.slice(i + 1)];
}

// "10 million", "a billion", "180,000", "468"
export function count(n) {
  if (n < 1e6) return Math.round(n).toLocaleString('en-US');
  for (const [v, w] of WORDS) if (n >= v) {
    const s = sig(n / v, 2);
    if (s === 1 && w === 'billion') return 'a billion';
    return `${trim(s.toLocaleString('en-US', { maximumFractionDigits: 1 }))} ${w}`;
  }
  return String(n);
}
export const oneIn = n => `1 in ${count(n)}`;
// "10,000,000" for the receipt, where the multiplication is read digit by digit
export const digits = n => Math.round(n).toLocaleString('en-US');
export const pct = x => (x >= 10 ? `${Math.round(x)}%` : x >= 1 ? `${trim(x.toFixed(1))}%` : x > 0 ? '<1%' : '0%');

// Tick labels for the ruler: "$1", "$10", "$100", "$1,000", "$10,000", "$100,000", "$1 million", "$10 million", ...
export function tick(power) {
  if (power < 6) return `$${(10 ** power).toLocaleString('en-US')}`;
  if (power < 9) return `$${10 ** (power - 6)} million`;
  if (power < 12) return `$${10 ** (power - 9)} billion`;
  return `$${10 ** (power - 12)} trillion`;
}
// The short form where room is tight: "$1k", "$1M", "$1B"
export function tickShort(power) {
  if (power < 3) return `$${10 ** power}`;
  if (power < 6) return `$${10 ** (power - 3)}k`;
  if (power < 9) return `$${10 ** (power - 6)}M`;
  if (power < 12) return `$${10 ** (power - 9)}B`;
  return `$${10 ** (power - 12)}T`;
}
