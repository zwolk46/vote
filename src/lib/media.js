import { useEffect, useState } from 'preact/hooks';
// Layout by width (the midterms src/lib/media.js): 900 px and up is a desktop's layout, as there.
export function useMedia(q) {
  const mq = typeof matchMedia === 'undefined' ? null : matchMedia(q);
  const [m, set] = useState(mq ? mq.matches : false);
  useEffect(() => { if (!mq) return; const f = () => set(mq.matches); mq.addEventListener('change', f); f(); return () => mq.removeEventListener('change', f); }, [q]);
  return m;
}
export const DESKTOP = '(min-width: 900px)';

// The page's colours as the canvas needs them, read from the tokens and read again when the scheme changes
// (Appearance or the device), so a canvas follows the scheme as the words do (M-spec R9, the maker's 11-03 20:53).
export function readColours() {
  const cs = getComputedStyle(document.documentElement);
  const v = k => cs.getPropertyValue(k).trim();
  return { fg: v('--fg'), muted: v('--muted'), faint: v('--faint'), line: v('--line'), lineStrong: v('--line-strong'), bg: v('--bg'), accent: v('--accent'), dot: v('--dot'), dotA: parseFloat(v('--dot-a')) || 0.3, track: v('--track'), panel: v('--panel') };
}
export function useColours() {
  const [c, set] = useState(() => (typeof document === 'undefined' ? null : readColours()));
  useEffect(() => {
    const f = () => set(readColours());
    const mq = matchMedia('(prefers-color-scheme: dark)');
    mq.addEventListener('change', f);
    const mo = new MutationObserver(f);
    mo.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
    return () => { mq.removeEventListener('change', f); mo.disconnect(); };
  }, []);
  return c;
}
