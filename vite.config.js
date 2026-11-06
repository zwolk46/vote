// Vite with Preact's JSX through oxc, as the midterms site builds (zwolk46/midterms vite.config.js): no Babel preset,
// so the build stays small and fast.
import { defineConfig } from 'vite';

export default defineConfig({
  oxc: { jsx: { runtime: 'automatic', importSource: 'preact' } },
  resolve: { alias: { react: 'preact/compat', 'react-dom': 'preact/compat' } },
  build: { target: 'es2020', outDir: 'dist', assetsInlineLimit: 0, modulePreload: { polyfill: false } },
});
