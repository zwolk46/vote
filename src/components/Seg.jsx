// The segmented control (M-spec s.17's form and motion, built here within the principles: the maker's 02:45 UTC 11-07
// correction; the midterms form it follows is src/components/Switch.jsx there, Base UI Tabs with its Indicator).
// One object with one moving part: the indicator under the chosen option slides to the newly chosen one (V8:
// `segment`, 300 ms on the spring); the words stay where they are and change colour at once. Equal columns, so the
// indicator moves on translate alone. Arrows move the choice, as a radio group. `still`: no slide (Appearance, M-spec
// s.15: the scheme changes at once and so does its control).
// `fit`: when a label's longest word cannot fit its column whole, as at 2x text
// on a 320 px phone, the options stand in a column instead, and the indicator moves down rather than across. *Reason:*
// a label cut to "Clos..." cannot be read (by eye, 11-07), and a word broken inside itself reads worse.
import { useLayoutEffect, useRef, useState } from 'preact/hooks';
import { play } from '../lib/motion.js';

const across = i => `translateX(calc(${i} * (100% + 2px)))`, down = i => `translateY(calc(${i} * (100% + 2px)))`;
let ruler = null;

export function Seg({ options, value, onChange, label, size = 'src', still = false, cls = '', fit = false }) {
  const n = options.length;
  const i = Math.max(0, options.findIndex(([v]) => v === value));
  const ind = useRef(null), prev = useRef(i), root = useRef(null);
  const [vert, setVert] = useState(false);
  const at = vert ? down : across;
  useLayoutEffect(() => {
    if (prev.current !== i && !still) play(ind.current, 'segment', [{ transform: at(prev.current) }, { transform: at(i) }]);
    prev.current = i;
  }, [i]);
  useLayoutEffect(() => {
    if (!fit) return;
    const el = root.current;
    const check = () => {
      const bs = [...el.querySelectorAll('.seg-t')];
      const box = el.parentElement, ps = getComputedStyle(box), room = box.clientWidth - parseFloat(ps.paddingLeft) - parseFloat(ps.paddingRight);
      if (!bs.length || !room) return;
      ruler = ruler || document.createElement('canvas').getContext('2d');
      const st = getComputedStyle(bs[0]), pad = parseFloat(st.paddingLeft) + parseFloat(st.paddingRight);
      ruler.font = `600 ${st.fontSize} ${st.fontFamily}`;
      let need = 0;
      for (const b of bs) for (const w of b.textContent.split(/\s+/)) need = Math.max(need, ruler.measureText(w).width);
      setVert(need + pad + 2 > (room - 4 - (n - 1) * 2) / n);
    };
    check();
    const ro = new ResizeObserver(check);
    ro.observe(el); ro.observe(el.parentElement);
    return () => ro.disconnect();
  }, [fit, n]);
  const key = e => {
    const d = e.key === 'ArrowRight' || e.key === 'ArrowDown' ? 1 : e.key === 'ArrowLeft' || e.key === 'ArrowUp' ? -1 : 0;
    if (!d) return;
    e.preventDefault();
    const j = (i + d + n) % n;
    onChange(options[j][0]);
    requestAnimationFrame(() => root.current?.querySelectorAll('.seg-t')[j]?.focus());
  };
  return (
    <div ref={root} class={`seg seg-${size}${vert ? ' seg-v' : ''} ${cls}`} role="radiogroup" aria-label={label} onKeyDown={key}>
      {options.map(([v, name]) => (
        <button key={v} type="button" role="radio" class="seg-t" aria-checked={v === value ? 'true' : 'false'} tabIndex={v === value ? 0 : -1} onClick={() => v !== value && onChange(v)}>{name}</button>
      ))}
      <span ref={ind} class="seg-ind" aria-hidden="true" style={vert ? { height: `calc((100% - 4px - ${(n - 1) * 2}px) / ${n})`, transform: at(i) } : { width: `calc((100% - 4px - ${(n - 1) * 2}px) / ${n})`, transform: at(i) }} />
    </div>
  );
}
