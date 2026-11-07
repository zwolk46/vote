// The first screen, in the candidate the address names (?v=a, ?v=b, ?v=c; design/DESIGN-SPEC.md §5). The reader's
// cost and reading are held here, so they carry from one candidate to the next on the preview and each candidate is
// judged on the same inputs. Each candidate stands inside a Boundary: one broken part never blanks the page
// (inherited/design/code/Boundary.jsx; midterms #241).
import { useEffect, useState } from 'preact/hooks';
import { Header } from './components/Header.jsx';
import { PreviewBar, OPTIONS, isPreview } from './components/PreviewBar.jsx';
import { Boundary } from './components/Boundary.jsx';
import { COST } from './data/real.js';
import { Ruler } from './options/Ruler.jsx';
import { Ballot } from './options/Ballot.jsx';
import { OneInN } from './options/OneInN.jsx';

const readV = () => { const v = new URLSearchParams(location.search).get('v'); return OPTIONS.some(([k]) => k === v) ? v : 'a'; };
const VIEWS = { a: Ruler, b: Ballot, c: OneInN };

export function App() {
  const [v, setVState] = useState(readV);
  const [minutes, setMinutes] = useState(COST.minutes);
  const [wage, setWage] = useState(COST.wage);
  const [reading, setReading] = useState('you');
  const setV = k => {
    const u = new URL(location.href); u.searchParams.set('v', k);
    history.replaceState(null, '', u);
    setVState(k);
    window.scrollTo(0, 0);
  };
  useEffect(() => { const f = () => setVState(readV()); addEventListener('popstate', f); return () => removeEventListener('popstate', f); }, []);
  const View = VIEWS[v];
  const props = { minutes, wage, C: (minutes / 60) * wage, setCost: (m, w) => { setMinutes(m); setWage(w); }, reading, setReading };
  return (
    <>
      <PreviewBar v={v} setV={setV} />
      <Header />
      <Boundary what={`Candidate ${v.toUpperCase()}`} resetOn={[v]} fallback={() => <main class="page"><p class="muted">This part of the page could not be drawn.</p></main>}>
        <View key={v} {...props} />
      </Boundary>
    </>
  );
}
export { isPreview };
