import { render } from 'preact';
import { App } from './app.jsx';
import { watchHeadings } from './lib/fitheads.js';
import './styles.css';

const root = document.getElementById('app');
render(<App />, root);
// A heading steps down only where its longest word cannot fit whole (inherited/design/code/fitheads.js, W23).
watchHeadings(root);
