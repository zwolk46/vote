// The preview bar: the note that the fields of dots are samples (M-spec R1 keeps it: without it invented figures are
// taken for real ones), and, on previews only, the picker between the candidates (the design guidance, process step 2:
// switched by ?v=a, ?v=b, ?v=c, with a picker shown only on previews and never in production).
import { Seg } from './Seg.jsx';
import { sampleTotal } from '../data/sample.js';

export const OPTIONS = [['a', 'A · Ruler'], ['b', 'B · Ballot'], ['c', 'C · One in N']];

// A preview is any build that is not Vercel's production one. VITE_VERCEL_ENV is set by Vercel on its builds; the
// address is the second guard, so the picker cannot show on the production address whatever the build says.
export const isPreview = (import.meta.env.VITE_VERCEL_ENV || '') !== 'production' && (typeof location === 'undefined' || location.hostname !== 'vote-rho-pearl.vercel.app');

export function PreviewBar({ v, setV }) {
  return (
    <div class="prevbar" role="note">
      <div class="prevbar-in">
        <p>{isPreview ? 'Preview. ' : ''}The grey dots are {sampleTotal().toLocaleString('en-US')} sample contests, invented until the data lands. The named figures are real, with their sources.</p>
        {isPreview ? <Seg label="Candidate" options={OPTIONS} value={v} onChange={setV} /> : null}
      </div>
    </div>
  );
}
