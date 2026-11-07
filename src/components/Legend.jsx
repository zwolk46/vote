// A key of marks, each drawn as it is drawn in the chart beside its label (the maker, 11-07 04:32: a mark explains,
// a sentence about it does not): the grey dot of contests, the ring of a named figure, the reader's cost.
export function Legend({ items }) {
  return (
    <ul class="legend" aria-label="Key">
      {items.map(([k, t]) => <li key={k}><span class={`lg lg-${k}`} aria-hidden="true" />{t}</li>)}
    </ul>
  );
}
