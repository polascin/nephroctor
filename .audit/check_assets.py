#!/usr/bin/env python3
"""Asset, CSS and metadata audit.

Checks the CSS token graph, the @font-face files, JSON-LD, the web manifest, the
sitemap, and — most importantly — that the site loads nothing from a third-party
origin (the GDPR property established in Beh #7).

Run:  python .audit/check_assets.py
"""
import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent
OWN_HOSTS = {'nephroctor.com'}

failed = False


def check(label, ok, extra=''):
    global failed
    if not ok:
        failed = True
    print(f'  {"OK  " if ok else "FAIL"} {label}{extra}')


def check_css():
    css = (ROOT / 'assets' / 'site.css').read_text(encoding='utf-8')
    stripped = re.sub(r'/\*.*?\*/', '', css, flags=re.S)

    check('CSS braces balanced', stripped.count('{') == stripped.count('}'),
          f' ({stripped.count("{")} open / {stripped.count("}")} close)')

    # Beh #5 shipped ":root[...] .x, @media (...) { ... }" — invalid, silently dropped.
    check('no at-rule inside a selector list', not re.search(r',\s*@(media|supports)', stripped))

    declared = set(re.findall(r'(--[\w-]+)\s*:', css))
    used = set(re.findall(r'var\((--[\w-]+)\)', css))
    check('no undefined custom properties', used <= declared, f' -> {sorted(used - declared)}')

    # --color-accent is kept deliberately as the brand reference colour.
    unused = declared - used - {'--color-accent'}
    check('no dead custom properties', not unused, f' -> {sorted(unused)}')

    fonts = re.findall(r"url\('(fonts/[^']+)'\)", css)
    missing = [f for f in fonts if not (ROOT / 'assets' / f).exists()]
    check('every @font-face file exists', not missing, f' ({len(fonts)} subsets)' if not missing else f' -> {missing}')


def check_metadata():
    html = (ROOT / 'index.html').read_text(encoding='utf-8')

    match = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    if not match:
        check('JSON-LD present', False)
    else:
        try:
            data = json.loads(match.group(1))
            check('JSON-LD parses', True)
            types = [node['@type'] for node in data['@graph']]
            check('JSON-LD graph has WebSite + Person + ProfessionalService',
                  types == ['WebSite', 'Person', 'ProfessionalService'], f' -> {types}')
            check('JSON-LD lists 24 languages', len(data['@graph'][0]['inLanguage']) == 24)
        except Exception as exc:                                # noqa: BLE001
            check('JSON-LD parses', False, f' -> {exc}')

    try:
        manifest = json.loads((ROOT / 'site.webmanifest').read_text(encoding='utf-8'))
        check('web manifest parses', True)
        for icon in manifest['icons']:
            check(f'manifest icon exists {icon["src"]}', (ROOT / icon['src'].lstrip('/')).exists())
        check('manifest declares a maskable icon',
              any(i.get('purpose') == 'maskable' for i in manifest['icons']))
    except Exception as exc:                                    # noqa: BLE001
        check('web manifest parses', False, f' -> {exc}')

    try:
        ET.parse(ROOT / 'sitemap.xml')
        check('sitemap.xml is well-formed XML', True)
        sitemap = (ROOT / 'sitemap.xml').read_text(encoding='utf-8')
        locs = [loc for loc in re.findall(r'<loc>https://nephroctor\.com/(.*?)</loc>', sitemap) if loc]
        missing = [loc for loc in locs if not (ROOT / loc).exists()]
        check('every sitemap <loc> maps to a real file', not missing, f' -> {missing}')
    except Exception as exc:                                    # noqa: BLE001
        check('sitemap.xml is well-formed XML', False, f' -> {exc}')


def check_no_third_party():
    """No subresource may come from another origin: that is what keeps the site
    free of a consent banner and keeps visitor IPs off third-party servers."""
    sources = [ROOT / 'index.html'] + sorted((ROOT / 'legal').glob('*.html'))
    sources += [ROOT / 'assets' / 'site.css', ROOT / 'assets' / 'legal.js']

    loaded, linked = set(), set()
    for path in sources:
        text = path.read_text(encoding='utf-8')
        # subresources: src=, and href= on <link> only (anchors are outbound links)
        for url in re.findall(r'\ssrc=["\'](https?://[^"\']+)', text):
            loaded.add(url.split('/')[2])
        for url in re.findall(r'<link[^>]+href=["\'](https?://[^"\']+)', text):
            loaded.add(url.split('/')[2])
        for url in re.findall(r'url\((https?://[^)]+)', text):
            loaded.add(url.split('/')[2])
        for url in re.findall(r'<a[^>]+href=["\'](https?://[^"\']+)', text):
            linked.add(url.split('/')[2])

    third_party = loaded - OWN_HOSTS
    check('no third-party subresource origin', not third_party, f' -> {sorted(third_party)}')
    print(f'       outbound link hosts (not loaded): {", ".join(sorted(linked))}')

    css = (ROOT / 'assets' / 'site.css').read_text(encoding='utf-8')
    check('no Google Fonts reference in CSS', 'fonts.googleapis' not in css and 'fonts.gstatic' not in css)


def check_icons():
    expected = ['favicon.ico', 'favicon-16.png', 'favicon-32.png', 'apple-touch-icon.png',
                'icon-192.png', 'icon-512.png', 'icon-maskable-512.png', 'og-image.jpg']
    for name in expected:
        path = ROOT / 'assets' / name
        check(f'asset present {name}', path.exists() and path.stat().st_size > 0)
    check('root favicon.ico present (implicit browser request)', (ROOT / 'favicon.ico').exists())


def main() -> int:
    print('== CSS ==');       check_css()
    print('\n== metadata =='); check_metadata()
    print('\n== icons ==');    check_icons()
    print('\n== third-party origins =='); check_no_third_party()
    print('\nassets:', 'FAILED' if failed else 'clean')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
