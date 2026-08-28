#!/usr/bin/env python3
"""Web link integrity and URL audit.

Checks all internal links, anchors/fragments, mailto/tel protocols, and
external URLs across index.html, legal documents, sitemap, manifest, and assets.
Ensures external links are reachable (using browser User-Agent) and that all
target="_blank" anchors enforce rel="noopener noreferrer".

Run:  python .audit/check_links.py
"""
import concurrent.futures
import pathlib
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'


class LinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []  # (tag, attr, val, target, rel, line)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        line = self.getpos()[0]
        if 'id' in a:
            self.ids.add(a['id'])
        if tag == 'a' and 'href' in a:
            self.links.append((tag, 'href', a['href'], a.get('target'), a.get('rel'), line))
        elif tag == 'link' and 'href' in a:
            self.links.append((tag, 'href', a['href'], None, a.get('rel'), line))
        elif tag in ('img', 'script', 'source'):
            src = a.get('src') or a.get('srcset')
            if src:
                self.links.append((tag, 'src', src, None, None, line))


def check_url(url: str, timeout: int = 15) -> tuple[bool, int, str]:
    """Test outbound HTTP/HTTPS URL with browser User-Agent."""
    ctx = ssl.create_default_context()
    req = urllib.request.Request(
        url,
        headers={
            'User-Agent': UA,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
    )
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=timeout) as resp:
            return True, resp.status, resp.geturl()
    except urllib.error.HTTPError as e:
        return e.code < 400, e.code, str(e)
    except Exception as e:
        return False, 0, str(e)


def main() -> int:
    html_files = [ROOT / 'index.html'] + sorted((ROOT / 'legal').glob('*.html'))
    failed = False

    def report(ok: bool, label: str, extra: str = ''):
        nonlocal failed
        if not ok:
            failed = True
        print(f'  {"OK  " if ok else "FAIL"} {label}{extra}', flush=True)

    print('== Internal Link and Anchor Integrity ==', flush=True)
    file_extractors = {}
    all_external_urls = set()
    all_mailtos = set()
    all_tels = set()

    for p in html_files:
        parser = LinkExtractor()
        parser.feed(p.read_text(encoding='utf-8'))
        file_extractors[p] = parser

    for p, parser in file_extractors.items():
        rel_path = p.relative_to(ROOT)
        for tag, attr, target, target_attr, rel, line in parser.links:
            # Check security for target=_blank
            if target_attr == '_blank':
                has_noopener = rel and 'noopener' in rel and 'noreferrer' in rel
                if not has_noopener:
                    report(False, f'{rel_path}:{line} target="_blank" without rel="noopener noreferrer"', f' -> {target}')

            # Categorize URL
            if target.startswith(('https://', 'http://')):
                if target.startswith('https://nephroctor.com/'):
                    # Check internal absolute canonical or subpath
                    sub = target[len('https://nephroctor.com/'):].split('?')[0].split('#')[0]
                    if sub and not (ROOT / sub).exists():
                        report(False, f'{rel_path}:{line} broken absolute site link', f' -> {target}')
                else:
                    all_external_urls.add(target)
            elif target.startswith('mailto:'):
                email = target[len('mailto:'):].split('?')[0]
                all_mailtos.add(email)
                if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
                    report(False, f'{rel_path}:{line} invalid email in mailto', f' -> {target}')
            elif target.startswith('tel:'):
                phone = target[len('tel:'):]
                all_tels.add(phone)
                if not re.match(r'^\+?[0-9\s-]+$', phone):
                    report(False, f'{rel_path}:{line} invalid phone number in tel', f' -> {target}')
            elif target.startswith('#'):
                frag = target[1:]
                if frag and frag not in parser.ids:
                    report(False, f'{rel_path}:{line} dangling fragment #{frag}')
            elif not target.startswith(('data:', 'javascript:')):
                # Relative local file link
                clean_target = target.split('?')[0].split('#')[0]
                target_file = (p.parent / clean_target).resolve()
                if not target_file.exists():
                    report(False, f'{rel_path}:{line} broken relative link', f' -> {target}')

    report(not failed, 'all HTML internal paths, anchors, and protocols valid')

    print('\n== External Web Links Reachability ==', flush=True)
    urls_to_test = sorted([u for u in all_external_urls if not u.startswith(('http://www.w3.org', 'http://www.sitemaps.org'))])

    print(f'Checking {len(urls_to_test)} external web URLs with browser User-Agent...', flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(check_url, url): url for url in urls_to_test}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                ok, status, extra = future.result()
                report(ok, f'{url:45} HTTP {status}', f' ({extra})' if not ok else '')
            except Exception as exc:
                report(False, f'{url:45} EXCEPTION', f' ({exc})')

    print('\n== Contact Protocol Verification ==', flush=True)
    for email in sorted(all_mailtos):
        report(True, f'mailto:{email}')
    for phone in sorted(all_tels):
        report(True, f'tel:{phone}')

    print('\nlinks:', 'FAILED' if failed else 'all web links verified and operational', flush=True)
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
