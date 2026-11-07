// The header: the mark and the name (design/DESIGN-SPEC.md §2.11, a proposal), and Appearance (M-spec s.15). No menu
// yet: there is no other page to go to, and a control that goes nowhere is a named fault (TASTE, 11-03 11:50).
import { useState } from 'preact/hooks';
import { Seg } from './Seg.jsx';

// The mark: a navy tile holding a 3 × 3 grid of white dots, one of them red: one vote among many, in the site's own
// mark (the dot). Red, white and navy as the midterms flag tile; the white solid in both schemes (the maker, 11-04
// 21:59). Decorative: the words beside it say the name.
export function Mark({ size = 22 }) {
  const dots = [];
  for (let r = 0; r < 3; r++) for (let c = 0; c < 3; c++) {
    const one = r === 1 && c === 1;
    dots.push(<circle key={`${r}${c}`} cx={6 + c * 5} cy={6 + r * 5} r={one ? 1.9 : 1.55} fill={one ? 'var(--logo-red)' : 'var(--logo-white)'} />);
  }
  return (
    <svg width={size} height={size} viewBox="0 0 22 22" aria-hidden="true">
      <rect width="22" height="22" rx="5.5" fill="var(--logo-navy)" />
      {dots}
      <rect x=".5" y=".5" width="21" height="21" rx="5" fill="none" stroke="var(--logo-edge)" />
    </svg>
  );
}

const KEY = 'vote.theme';
function readTheme() { try { const t = localStorage.getItem(KEY); return t === 'light' || t === 'dark' ? t : 'system'; } catch { return 'system'; } }
function applyTheme(t) {
  const el = document.documentElement;
  if (t === 'system') el.removeAttribute('data-theme'); else el.setAttribute('data-theme', t);
  try { if (t === 'system') localStorage.removeItem(KEY); else localStorage.setItem(KEY, t); } catch {}
  // the browser's own colour follows the page (M-spec s.15: the theme-color metas follow the attribute)
  for (const m of document.querySelectorAll('meta[name="theme-color"]')) {
    const dark = (m.getAttribute('media') || '').includes('dark');
    if (!m.dataset.c) m.dataset.c = m.getAttribute('content');
    m.setAttribute('content', t === 'system' ? m.dataset.c : t === 'dark' ? '#121314' : '#fbfaf8');
    if (t !== 'system') m.dataset.forced = dark ? 'd' : 'l';
  }
}

export function Header() {
  const [theme, setTheme] = useState(readTheme);
  return (
    <header class="hdr">
      <a class="logo" href="/" aria-label="One vote, home"><Mark /><span class="wm"><span>One</span><span class="wm-2">vote</span></span></a>
      <div class="appear">
        <span class="lbl" id="appear-l">Appearance</span>
        <Seg label="Appearance" still options={[['system', 'System'], ['light', 'Light'], ['dark', 'Dark']]} value={theme} onChange={t => { setTheme(t); applyTheme(t); }} />
      </div>
    </header>
  );
}
