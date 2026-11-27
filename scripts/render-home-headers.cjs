// Run after editing shared-header.js: node scripts/render-home-headers.cjs
// Keep one source for the header, but include homepage markup before first paint.
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const source = fs.readFileSync(path.join(root, 'assets/shared-header.js'), 'utf8');
for (const lang of ['en', 'ur']) {
  let header = '';
  const document = {
    currentScript: {src: 'https://www.dastak90807.com/assets/shared-header.js?v=13', insertAdjacentHTML: (_, html) => { header = html; }},
    documentElement: {lang}, querySelector: () => null, querySelectorAll: () => [],
    createElement: () => ({dataset: {}, setAttribute() {}}), head: {appendChild() {}}
  };
  vm.runInNewContext(source, {document, window: {}, URL, location: {pathname: `/${lang}/`, href: `https://www.dastak90807.com/${lang}/`}});
  if (!header.startsWith('<header')) throw new Error('Header generation failed');
  const file = path.join(root, lang, 'index.html');
  let html = fs.readFileSync(file, 'utf8');
  const marker = '<!-- Static shared header: regenerate with node scripts/render-home-headers.cjs -->';
  const block = `${marker}\n${header}\n<!-- End static shared header -->\n`;
  html = html.replace(/<!-- Static shared header:[\s\S]*?<!-- End static shared header -->\n?/, '');
  html = html.replace(/<script src="\/assets\/shared-header.js\?v=[^"]+"><\/script>/, block + '<script src="/assets/shared-header.js?v=13"></script>');
  // Match the existing stylesheet versions; preserve the final cascade order.
  const styles = '<link rel="stylesheet" href="/assets/shared-header.css?v=10"><link rel="stylesheet" href="/assets/lang-switch.css?v=4">';
  if (!html.includes('/assets/shared-header.css?v=10')) html = html.replace('</head>', styles + '</head>');
  fs.writeFileSync(file, html);
}
