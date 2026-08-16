#!/usr/bin/env python3
"""HTML structure audit: tag balance, duplicate ids, heading order, link integrity,
rel=noopener on target=_blank, dangling fragments.

Run from the repository root:  python .audit/check_structure.py
Exits non-zero if anything fails.
"""
import pathlib
import re
import sys
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link',
        'meta', 'param', 'source', 'track', 'wbr'}


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.errors, self.ids, self.links, self.headings = [], [], [], [], []
        self.imgs_without_alt = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.append(a['id'])
        if tag == 'a' and 'href' in a:
            self.links.append((a['href'], a.get('target'), a.get('rel')))
        if tag == 'link' and 'href' in a:
            self.links.append((a['href'], None, None))
        if tag in ('script', 'img', 'source'):
            ref = a.get('src') or a.get('srcset')
            if ref:
                self.links.append((ref, None, None))
        if tag == 'img' and not a.get('alt') and a.get('alt') != '':
            self.imgs_without_alt += 1
        if re.fullmatch(r'h[1-6]', tag):
            self.headings.append(int(tag[1]))
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(f'stray </{tag}>')
        elif self.stack[-1] != tag:
            self.errors.append(f'</{tag}> closes <{self.stack[-1]}>')
            if tag in self.stack:
                while self.stack and self.stack.pop() != tag:
                    pass
        else:
            self.stack.pop()


def audit(path: pathlib.Path):
    page = Page()
    page.feed(path.read_text(encoding='utf-8'))
    problems = list(page.errors)

    if page.stack:
        problems.append(f'unclosed tags: {page.stack}')

    dupes = sorted({i for i in page.ids if page.ids.count(i) > 1})
    if dupes:
        problems.append(f'duplicate ids: {dupes}')

    if page.imgs_without_alt:
        problems.append(f'{page.imgs_without_alt} <img> without alt')

    # Legal pages carry two h1 elements (the SK and EN versions of one document);
    # only one of them is ever visible.
    expected_h1 = 1 if path.name == 'index.html' else 2
    if page.headings.count(1) != expected_h1:
        problems.append(f'h1 count is {page.headings.count(1)}, expected {expected_h1}')

    previous = 0
    for level in page.headings:
        if previous and level > previous + 1:
            problems.append(f'heading level jumps h{previous} -> h{level}')
        previous = level

    for href, target, rel in page.links:
        if target == '_blank' and (not rel or 'noopener' not in rel):
            problems.append(f'target=_blank without rel=noopener: {href}')

    for href, _, _ in page.links:
        if href.startswith(('http://', 'https://', 'mailto:', 'tel:', 'data:')):
            continue
        if href.startswith('#'):
            if href[1:] and href[1:] not in page.ids:
                problems.append(f'dangling fragment: {href}')
            continue
        target_path = (path.parent / href.split('?')[0].split('#')[0]).resolve()
        if not target_path.exists():
            problems.append(f'broken internal link: {href}')

    return problems


def main():
    pages = [ROOT / 'index.html'] + sorted((ROOT / 'legal').glob('*.html'))
    failed = False
    for path in pages:
        problems = audit(path)
        failed |= bool(problems)
        print(f'  {"FAIL" if problems else "OK  "} {path.relative_to(ROOT)}')
        for problem in problems:
            print(f'        - {problem}')
    print('\nstructure:', 'FAILED' if failed else 'clean')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
