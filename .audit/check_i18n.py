#!/usr/bin/env python3
"""Translation and hreflang audit.

Verifies that every one of the 24 EU languages carries every translation key,
that LANG_ORDER matches the translations object, and that the hreflang
annotations in index.html and sitemap.xml describe the same language set.

Run:  python .audit/check_i18n.py
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

REQUIRED_KEYS = [
    'name', 'locale', 'subtitle', 'langTitle', 'heading', 'text', 'description',
    'themeDark', 'themeLight', 'contactTitle', 'labelPhone', 'skipLink', 'navLegal',
    'legalPrivacy', 'legalCookies', 'legalTerms', 'legalNotice',
    'legalAccessibility', 'legalDisclaimer',
]
EU_LANGUAGES = 24


def load_translations(html: str) -> dict:
    block = html.split('const translations = ', 1)[1].split('\n        };', 1)[0] + '\n}'
    jsonish = re.sub(r'^(\s*)([A-Za-z][A-Za-z0-9_]*):', r'\1"\2":', block, flags=re.M)
    return json.loads(jsonish)


def main() -> int:
    html = (ROOT / 'index.html').read_text(encoding='utf-8')
    failed = False

    def check(label, ok, extra=''):
        nonlocal failed
        if not ok:
            failed = True
        print(f'  {"OK  " if ok else "FAIL"} {label}{extra}')

    try:
        translations = load_translations(html)
    except Exception as exc:                                    # noqa: BLE001
        print(f'  FAIL translations object does not parse: {exc}')
        return 1

    order = re.findall(r"'(\w+)'", re.search(r'const LANG_ORDER = \[(.*?)\];', html, re.S).group(1))

    check(f'translations contains {EU_LANGUAGES} languages', len(translations) == EU_LANGUAGES,
          f' -> {len(translations)}')
    check('LANG_ORDER matches translations', sorted(order) == sorted(translations))

    for code in sorted(translations):
        entry = translations[code]
        missing = [k for k in REQUIRED_KEYS if k not in entry]
        extra = [k for k in entry if k not in REQUIRED_KEYS]
        empty = [k for k, v in entry.items() if not str(v).strip()]
        if missing or extra or empty:
            check(f'language {code}', False, f' missing={missing} extra={extra} empty={empty}')
    check(f'all {len(REQUIRED_KEYS)} keys present in every language',
          all(all(k in translations[c] for k in REQUIRED_KEYS) for c in translations))

    # og:locale must look like xx_XX and start with the language code
    bad_locales = [c for c in translations
                   if not re.fullmatch(r'[a-z]{2}_[A-Z]{2}', translations[c]['locale'])
                   or not translations[c]['locale'].startswith(c)]
    check('every og:locale is well formed', not bad_locales, f' -> {bad_locales}')

    # descriptions should stay inside the useful snippet length
    too_long = [c for c in translations if len(translations[c]['description']) > 200]
    check('meta descriptions <= 200 chars', not too_long, f' -> {too_long}')

    hreflang = re.findall(r'<link rel="alternate" hreflang="([\w-]+)"', html)
    check('index.html hreflang covers all languages + x-default',
          set(hreflang) == set(order) | {'x-default'}, f' -> {len(hreflang)} tags')
    check('no duplicate hreflang tags', len(hreflang) == len(set(hreflang)))

    sitemap = (ROOT / 'sitemap.xml').read_text(encoding='utf-8')
    home = re.findall(r'hreflang="([\w-]+)" href="https://nephroctor\.com/(?:\?lang=\w+)?"', sitemap)
    check('sitemap home entry matches index.html hreflang', set(home) == set(hreflang),
          f' -> {len(home)} entries')

    print('\ni18n:', 'FAILED' if failed else 'complete and consistent')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
