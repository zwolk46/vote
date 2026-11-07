// The preview bar, on previews only: the picker between the candidates (the design guidance, process step 2: switched
// by ?v=a, ?v=b, with a picker shown only on previews and never in production). Every dot is now a real contest
// (src/data/build-field.mjs), so the bar no longer carries the samples' note (M-spec R1's reason for it is gone).
import { Seg } from './Seg.jsx';

// C, "one in N", was dropped from the first screen on 11-07: its field of millions of dots can only be a grey square
// on a phone (the maker, 04:09 UTC: "on mobile it looks awful"). Its idea goes to the explainer (brief X2).
export const OPTIONS = [['a', 'A · Ruler'], ['b', 'B · Ballot']];

// A preview is any build that is not Vercel's production one. VITE_VERCEL_ENV is set by Vercel on its builds; the
// address is the second guard, so the picker cannot show on the production address whatever the build says.
export const isPreview = (import.meta.env.VITE_VERCEL_ENV || '') !== 'production' && (typeof location === 'undefined' || location.hostname !== 'vote-rho-pearl.vercel.app');

export function PreviewBar({ v, setV }) {
  if (!isPreview) return null;
  return (
    <div class="prevbar" role="note">
      <div class="prevbar-in">
        <p>Preview</p>
        <Seg label="Candidate" options={OPTIONS} value={v} onChange={setV} />
      </div>
    </div>
  );
}
