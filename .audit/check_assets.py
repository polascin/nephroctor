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
        site_manifest = ROOT / 'site.webmanifest'
        root_manifest = ROOT / 'manifest.webmanifest'
        manifest = json.loads(site_manifest.read_text(encoding='utf-8'))
        check('web manifest parses', True)
        for icon in manifest['icons']:
            check(f'manifest icon exists {icon["src"]}', (ROOT / icon['src'].lstrip('/')).exists())
        check('manifest declares a maskable icon',
              any(i.get('purpose') == 'maskable' for i in manifest['icons']))
        # Align with light theme-color / background_color (dark chrome uses HTML meta).
        check('manifest theme_color matches background_color',
              manifest.get('theme_color') == manifest.get('background_color') == '#f8fafc',
              f' -> theme={manifest.get("theme_color")!r} '
              f'bg={manifest.get("background_color")!r}')
        # Same pattern as root favicon / apple-touch: tools often probe this path.
        check('root manifest.webmanifest present (common probe path)',
              root_manifest.exists() and root_manifest.stat().st_size > 0)
        if root_manifest.exists() and site_manifest.exists():
            check('root manifest.webmanifest matches site.webmanifest',
                  root_manifest.read_bytes() == site_manifest.read_bytes())
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
    """Static markup must not hard-load third-party subresources. Consent-gated
    Clarity may appear only inside assets/clarity-consent.js after explicit OK."""
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
    check('no hard-coded third-party subresource origin', not third_party, f' -> {sorted(third_party)}')
    print(f'       outbound link hosts (not loaded): {", ".join(sorted(linked))}')

    css = (ROOT / 'assets' / 'site.css').read_text(encoding='utf-8')
    check('no Google Fonts reference in CSS', 'fonts.googleapis' not in css and 'fonts.gstatic' not in css)

    consent = (ROOT / 'assets' / 'clarity-consent.js').read_text(encoding='utf-8')
    clarity_hosts = sorted({
        url.split('/')[2]
        for url in re.findall(r'https?://[^\s"\'`]+', consent)
        if 'clarity.ms' in url
    })
    check('Clarity loads only from clarity-consent.js after consent',
          'www.clarity.ms' in clarity_hosts and 'clarity("consentv2"' in consent,
          f' -> {clarity_hosts}')
    check('Clarity advertising storage stays denied',
          'ad_Storage: "denied"' in consent)


def check_icons():
    expected = ['favicon.ico', 'favicon.svg', 'favicon-16.png', 'favicon-32.png',
                'apple-touch-icon.png', 'icon-192.png', 'icon-512.png',
                'icon-maskable-512.png', 'og-image.jpg']
    for name in expected:
        path = ROOT / 'assets' / name
        check(f'asset present {name}', path.exists() and path.stat().st_size > 0)
    check('root favicon.ico present (implicit browser request)', (ROOT / 'favicon.ico').exists())
    root_svg = ROOT / 'favicon.svg'
    assets_svg = ROOT / 'assets' / 'favicon.svg'
    check('root favicon.svg present (common probe / modern browsers)',
          root_svg.exists() and root_svg.stat().st_size > 0)
    if root_svg.exists() and assets_svg.exists():
        check('root favicon.svg matches assets copy',
              root_svg.read_bytes() == assets_svg.read_bytes())
    if assets_svg.exists():
        svg_text = assets_svg.read_text(encoding='utf-8')
        check('favicon.svg declares image/svg viewBox and dark-scheme swap',
              'viewBox="0 0 32 32"' in svg_text
              and 'prefers-color-scheme: dark' in svg_text
              and 'class="light"' in svg_text
              and 'class="dark"' in svg_text)
    browserconfig = ROOT / 'browserconfig.xml'
    check('root browserconfig.xml present (Windows tile / msapplication)',
          browserconfig.exists() and browserconfig.stat().st_size > 0)
    if browserconfig.exists():
        bc = browserconfig.read_text(encoding='utf-8')
        check('browserconfig.xml points at existing tile icons',
              '/assets/icon-192.png' in bc
              and '/assets/icon-512.png' in bc
              and '#0077b6' in bc
              and (ROOT / 'assets' / 'icon-192.png').exists()
              and (ROOT / 'assets' / 'icon-512.png').exists())
    root_ati = ROOT / 'apple-touch-icon.png'
    root_ati_pre = ROOT / 'apple-touch-icon-precomposed.png'
    assets_ati = ROOT / 'assets' / 'apple-touch-icon.png'
    check('root apple-touch-icon.png present (iOS home-screen request)',
          root_ati.exists() and root_ati.stat().st_size > 0)
    check('root apple-touch-icon-precomposed.png present (legacy iOS request)',
          root_ati_pre.exists() and root_ati_pre.stat().st_size > 0)
    if root_ati.exists() and assets_ati.exists():
        check('root apple-touch-icon.png matches assets copy',
              root_ati.read_bytes() == assets_ati.read_bytes())
    if root_ati_pre.exists() and assets_ati.exists():
        check('root apple-touch-icon-precomposed.png matches assets copy',
              root_ati_pre.read_bytes() == assets_ati.read_bytes())


def main() -> int:
    print('== CSS ==');       check_css()
    print('\n== metadata =='); check_metadata()
    print('\n== icons ==');    check_icons()
    print('\n== third-party origins =='); check_no_third_party()
    print('\nassets:', 'FAILED' if failed else 'clean')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
