/* Theme-color must follow data-theme / stored preference, not only OS media.
   Also verify cross-tab storage applies dark/light and clears back to system. */
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

function applyStorage(newValue, osDark) {
  if (newValue === 'dark' || newValue === 'light') return newValue;
  return osDark ? 'dark' : null;
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

assert(applyStorage('light', true) === 'light', 'storage light applied under dark OS');
assert(applyStorage('dark', false) === 'dark', 'storage dark applied under light OS');
assert(applyStorage(null, true) === 'dark', 'cleared storage restores dark OS');
assert(applyStorage(null, false) === null, 'cleared storage under light OS leaves unset');

console.log('theme logic: all cases correct');
