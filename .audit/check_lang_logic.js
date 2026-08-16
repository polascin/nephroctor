/* Language-resolution audit.
 *
 * Extracts initialLang() straight out of index.html and exercises the documented
 * precedence: ?lang= in the URL -> stored choice -> browser language -> Slovak.
 *
 * Run:  node .audit/check_lang_logic.js
 */
'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
const main = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map((m) => m[1]).pop();
const source = main.slice(main.indexOf('const translations'), main.indexOf('let currentLang'));

function run({ search, stored, languages }) {
  // Node exposes a read-only `navigator`; defineProperty is the only way to stub it.
  Object.defineProperty(globalThis, 'navigator', {
    value: { languages, language: languages[0] },
    configurable: true,
  });
  global.window = { location: { search, pathname: '/' } };
  const bag = {};
  if (stored) bag['nephroctor-lang'] = stored;
  global.localStorage = {
    getItem: (k) => (k in bag ? bag[k] : null),
    setItem: () => {},
  };
  return eval(source + '; initialLang();');
}

const CASES = [
  ['?lang= wins over everything',       { search: '?lang=fr', stored: 'de',  languages: ['it-IT'] },                'fr'],
  ['stored choice beats browser',       { search: '',         stored: 'de',  languages: ['it-IT'] },                'de'],
  ['browser language as fallback',      { search: '',         stored: null,  languages: ['it-IT', 'it'] },          'it'],
  ['region tag stripped (pt-BR)',       { search: '',         stored: null,  languages: ['pt-BR'] },                'pt'],
  ['first supported entry wins',        { search: '',         stored: null,  languages: ['ja-JP', 'nb-NO', 'hu'] }, 'hu'],
  ['unsupported browser lang -> sk',    { search: '',         stored: null,  languages: ['ja-JP', 'zh-CN'] },       'sk'],
  ['bogus ?lang= ignored',              { search: '?lang=zz', stored: null,  languages: ['sv-SE'] },                'sv'],
  ['bogus stored value ignored',        { search: '',         stored: 'zz',  languages: ['el-GR'] },                'el'],
  ['no signal at all -> sk',            { search: '',         stored: null,  languages: [] },                       'sk'],
];

let failures = 0;
for (const [label, input, expected] of CASES) {
  let actual;
  try {
    actual = run(input);
  } catch (err) {
    actual = 'THREW: ' + err.message;
  }
  const ok = actual === expected;
  if (!ok) failures++;
  console.log(`  ${ok ? 'OK  ' : 'FAIL'} ${label.padEnd(34)} -> ${actual}${ok ? '' : `  (expected ${expected})`}`);
}

console.log('\nlanguage resolution:', failures ? `FAILED (${failures})` : 'all cases correct');
process.exit(failures ? 1 : 0);
