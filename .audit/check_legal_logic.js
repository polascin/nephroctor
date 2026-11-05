/* Legal-document language switch audit.
 *
 * Runs assets/legal.js against a DOM stub and asserts that every site language
 * lands on the right document version: Slovak (the binding original) for sk/cs,
 * English for everyone else.
 *
 * Run:  node .audit/check_legal_logic.js
 */
'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const SOURCE = fs.readFileSync(path.join(ROOT, 'assets', 'legal.js'), 'utf8');

function el(attrs = {}) {
  return {
    _attrs: { ...attrs }, hidden: false, innerHTML: '', textContent: '', _listeners: {},
    children: [],
    setAttribute(k, v) { this._attrs[k] = String(v); },
    getAttribute(k) { return k in this._attrs ? this._attrs[k] : null; },
    addEventListener(ev, fn) { (this._listeners[ev] = this._listeners[ev] || []).push(fn); },
    appendChild(child) { this.children.push(child); return child; },
    click() { (this._listeners.click || []).forEach((f) => f()); },
  };
}

const skBlock = el({ 'data-lang-block': 'sk' });
const enBlock = el({ 'data-lang-block': 'en' });
const skNav = el({ 'data-lang-block': 'sk' });
const enNav = el({ 'data-lang-block': 'en' });
const btnSk = el({ 'data-doc-lang': 'sk' });
const btnEn = el({ 'data-doc-lang': 'en' });
const toggle = el({});
const body = el({
  'data-title-sk': 'Dokument | Nephroctor',
  'data-title-en': 'Document | Nephroctor',
});
const docEl = el({});

function run({ search, saved }) {
  [skBlock, enBlock, skNav, enNav].forEach((b) => {
    b.hidden = b._attrs['data-lang-block'] === 'en';
  });
  docEl.lang = 'sk';

  const bag = saved ? { 'nephroctor-lang': saved } : {};
  global.localStorage = {
    getItem: (k) => (k in bag ? bag[k] : null),
    setItem: (k, v) => { bag[k] = v; },
  };
  global.window = {
    location: { search, pathname: '/legal/cookies.html' },
    matchMedia: () => ({ matches: false }),
  };
  global.history = { replaceState() {} };
  global.requestAnimationFrame = (fn) => fn();
  const bodyNode = el();
  global.document = {
    documentElement: docEl,
    body: bodyNode,
    title: '',
    createElement: () => el(),
    getElementById: (id) => (id === 'theme-toggle' ? toggle : null),
    querySelector: (sel) => {
      const m = sel.match(/^\[data-title-(\w+)\]$/);
      return m && body._attrs['data-title-' + m[1]] ? body : null;
    },
    querySelectorAll: (sel) => {
      if (sel === '[data-lang-block]') return [skBlock, enBlock, skNav, enNav];
      if (sel === '[data-doc-lang]') return [btnSk, btnEn];
      return [];
    },
  };

  eval(SOURCE);
  const live = bodyNode.children.find(
    (n) => n.getAttribute('role') === 'status' && n.getAttribute('aria-live') === 'polite',
  );
  return {
    visible: skBlock.hidden ? 'en' : 'sk',
    navVisible: skNav.hidden ? 'en' : 'sk',
    lang: docEl.lang,
    title: global.document.title,
    liveRegion: live || null,
    pressed: [btnSk, btnEn]
      .filter((b) => b.getAttribute('aria-pressed') === 'true')
      .map((b) => b.getAttribute('data-doc-lang')),
  };
}

const CASES = [
  ['no params, nothing stored',    { search: '',           saved: null }, 'sk'],
  ['?lang=en',                     { search: '?lang=en',   saved: null }, 'en'],
  ['?lang=sk',                     { search: '?lang=sk',   saved: null }, 'sk'],
  ['?lang=de -> English version',  { search: '?lang=de',   saved: null }, 'en'],
  ['?lang=el -> English version',  { search: '?lang=el',   saved: null }, 'en'],
  ['?lang=cs -> Slovak original',  { search: '?lang=cs',   saved: null }, 'sk'],
  ['bogus ?lang= falls through',   { search: '?lang=zz',   saved: null }, 'sk'],
  ['bogus ?lang= + stored fr',     { search: '?lang=zz',   saved: 'fr' }, 'en'],
  ['stored fr -> English version', { search: '',           saved: 'fr' }, 'en'],
  ['stored cs -> Slovak original', { search: '',           saved: 'cs' }, 'sk'],
  ['stored sk -> Slovak original', { search: '',           saved: 'sk' }, 'sk'],
];

let failures = 0;
for (const [label, input, expected] of CASES) {
  let result;
  try {
    result = run(input);
  } catch (err) {
    result = { visible: 'THREW: ' + err.message };
  }
  const ok = result.visible === expected
    && result.navVisible === expected
    && result.lang === expected
    && result.pressed.length === 1
    && result.pressed[0] === expected
    && result.liveRegion
    && result.liveRegion.textContent === '';
  if (!ok) failures++;
  console.log(`  ${ok ? 'OK  ' : 'FAIL'} ${label.padEnd(31)} `
    + `shows=${result.visible} nav=${result.navVisible} lang=${result.lang} pressed=${result.pressed}`
    + (ok ? '' : `  (expected ${expected})`));
}

/* User-initiated switch must announce; re-clicking the same language must not. */
{
  const label = 'click EN announces once';
  try {
    const result = run({ search: '', saved: null });
    btnEn.click();
    const first = result.liveRegion && result.liveRegion.textContent;
    btnEn.click();
    const second = result.liveRegion && result.liveRegion.textContent;
    const shows = skBlock.hidden ? 'en' : 'sk';
    const ok = shows === 'en'
      && first === 'Document language: English'
      && second === first;
    if (!ok) failures++;
    console.log(`  ${ok ? 'OK  ' : 'FAIL'} ${label.padEnd(31)} shows=${shows} announce=${JSON.stringify(first)}`);
  } catch (err) {
    failures++;
    console.log(`  FAIL ${label.padEnd(31)} THREW: ${err.message}`);
  }
}
{
  const label = 'click SK announces Slovak';
  try {
    const result = run({ search: '?lang=en', saved: null });
    btnSk.click();
    const shows = skBlock.hidden ? 'en' : 'sk';
    const announce = result.liveRegion && result.liveRegion.textContent;
    const ok = shows === 'sk' && announce === 'Jazyk dokumentu: slovenčina';
    if (!ok) failures++;
    console.log(`  ${ok ? 'OK  ' : 'FAIL'} ${label.padEnd(31)} shows=${shows} announce=${JSON.stringify(announce)}`);
  } catch (err) {
    failures++;
    console.log(`  FAIL ${label.padEnd(31)} THREW: ${err.message}`);
  }
}

console.log('\nlegal document switch:', failures ? `FAILED (${failures})` : 'all cases correct');
process.exit(failures ? 1 : 0);
