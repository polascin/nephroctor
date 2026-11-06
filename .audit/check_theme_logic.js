/* Theme-color must follow data-theme / stored preference, not only OS media.
   Explicit storage locks the theme; cleared storage follows the system without
   writing data-theme (so live prefers-color-scheme changes keep working). */
'use strict';

function isDark(docTheme, osDark) {
  if (docTheme === 'dark') return true;
  if (docTheme === 'light') return false;
  return !!osDark;
}

function syncMetas(metas, dark) {
  const color = dark ? '#0f172a' : '#f8fafc';
  if (!metas.length) return metas;
  const next = metas.slice();
  next[0] = { media: null, content: color };
  return [next[0]];
}

function applyStorage(newValue) {
  if (newValue === 'dark' || newValue === 'light') return newValue;
  return null;
}

function followSystem(osDark) {
  const docTheme = applyStorage(null);
  return syncMetas([
    { media: '(prefers-color-scheme: light)', content: '#f8fafc' },
    { media: '(prefers-color-scheme: dark)', content: '#0f172a' }
  ], isDark(docTheme, osDark))[0].content;
}

function assert(cond, msg) {
  if (!cond) {
    console.error('FAIL', msg);
    process.exit(1);
  }
  console.log('  OK  ', msg);
}

assert(isDark('light', true) === false, 'explicit light wins over dark OS');
assert(isDark('dark', false) === true, 'explicit dark wins over light OS');
assert(isDark(null, true) === true, 'no preference follows dark OS');
assert(isDark(null, false) === false, 'no preference follows light OS');

let metas = [
  { media: '(prefers-color-scheme: light)', content: '#f8fafc' },
  { media: '(prefers-color-scheme: dark)', content: '#0f172a' }
];
metas = syncMetas(metas, false);
assert(metas.length === 1 && metas[0].content === '#f8fafc' && metas[0].media === null,
  'light page collapses theme-color to #f8fafc');
metas = syncMetas([
  { media: '(prefers-color-scheme: light)', content: '#f8fafc' },
  { media: '(prefers-color-scheme: dark)', content: '#0f172a' }
], true);
assert(metas.length === 1 && metas[0].content === '#0f172a',
  'dark page collapses theme-color to #0f172a');

assert(applyStorage('light') === 'light', 'storage light applied');
assert(applyStorage('dark') === 'dark', 'storage dark applied');
assert(applyStorage(null) === null, 'cleared storage leaves system follow');
assert(followSystem(true) === '#0f172a', 'system follow dark OS syncs theme-color');
assert(followSystem(false) === '#f8fafc', 'system follow light OS syncs theme-color');

console.log('theme logic: all cases correct');
