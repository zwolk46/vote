// A part of a page that throws while it is drawn gives way to its own plain form, the error is logged, and the rest of the
// page carries on (the orchestrator, 09:44 UTC 11-06: "One bad field should never blank a whole page, so wrap each race
// card, or the view, in an error boundary. The boundary should draw that card's plain fallback and log the error, while
// the rest of the page carries on"). With nothing to catch it, a throw anywhere in a view took the whole view down and
// it never came back: one waiting row's null party blanked /oh, /ky and the page of each of 26 races on a cold load (#241).
//   `what`: the part, named in the log line;
//   `fallback(error)`: what stands in the part's place (nothing when it is not given);
//   `resetOn`: values the part is drawn from; when one of them changes (a race's next figures), the part is drawn again,
//   so a fault in one answer lasts until the next one, not until a reload.
// The log is console.error, which the checks count (pages.check, skeleton.check), so a part that falls back is a FAIL
// there even though the page still stands.
import { Component } from 'preact';

const changed = (a = [], b = []) => a.length !== b.length || a.some((x, i) => x !== b[i]);

export class Boundary extends Component {
  constructor(props) { super(props); this.state = { error: null, on: props.resetOn }; }
  static getDerivedStateFromError(error) { return { error }; }
  static getDerivedStateFromProps(props, state) { return changed(state.on, props.resetOn) ? { error: null, on: props.resetOn } : null; }
  componentDidCatch(error) { console.error(`${this.props.what || 'A part of the page'} could not be drawn; its plain form stands in its place.`, error); }
  render({ children, fallback }, { error }) { return error ? (fallback ? fallback(error) : null) : children; }
}
