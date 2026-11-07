// A figure that opens in place to its computation and its sources (design/DESIGN-SPEC.md §2.4; law 4 and 8). It opens
// at once, under the figure; its contents arrive with `reveal` (V7: 160 ms, opacity only, kept under reduced motion);
// it closes at once. Not a drawer: the figure and its arithmetic stay in one view (M-spec s.9: a drawer only where one
// is needed).
import { useLayoutEffect, useRef, useState } from 'preact/hooks';
import { play } from '../lib/motion.js';

let uid = 0;
export function useFold() {
  const [open, setOpen] = useState(false);
  const id = useRef(`fold-${++uid}`).current;
  return { open, id, toggle: () => setOpen(o => !o), btn: { 'aria-expanded': open ? 'true' : 'false', 'aria-controls': id } };
}

export function FoldBody({ fold, children, cls = '' }) {
  const ref = useRef(null);
  useLayoutEffect(() => { if (fold.open) play(ref.current, 'reveal', [{ opacity: 0 }, { opacity: 1 }]); }, [fold.open]);
  return <div ref={ref} id={fold.id} class={`fold ${cls}`} hidden={!fold.open}>{fold.open ? children : null}</div>;
}
