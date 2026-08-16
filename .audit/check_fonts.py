#!/usr/bin/env python3
"""Font subset coverage audit.

Two questions the other checks cannot answer:

  1. Is every character the site actually renders covered by a shipped subset?
     A character outside all of them silently falls back to a system font.
  2. Is any shipped subset unused? Each one is dead weight in the deploy payload.

Run:  python .audit/check_fonts.py
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSS = ROOT / 'assets' / 'site.css'


def parse_ranges(spec: str):
    """Turn a CSS unicode-range value into a list of (low, high) codepoints."""
    out = []
    for token in spec.split(','):
        token = token.strip().removeprefix('U+')
        if '-' in token:
            low, high = token.split('-')
            out.append((int(low, 16), int(high, 16)))
        elif '?' in token:
            out.append((int(token.replace('?', '0'), 16), int(token.replace('?', 'F'), 16)))
        else:
            out.append((int(token, 16), int(token, 16)))
    return out


def subsets():
    css = CSS.read_text(encoding='utf-8')
    found = {}
    for block in re.findall(r'@font-face\s*\{(.*?)\}', css, re.S):
        src = re.search(r"url\('fonts/([^']+)'\)", block)
        rng = re.search(r'unicode-range:\s*([^;]+);', block)
        if src and rng:
            found[src.group(1)] = parse_ranges(rng.group(1))
    return found


def rendered_text() -> str:
    """Everything the browser will actually paint."""
    chunks = []

    index = (ROOT / 'index.html').read_text(encoding='utf-8')

    # translation values (rendered via textContent / attributes)
    block = index.split('const translations = ', 1)[1].split('\n        };', 1)[0] + '\n}'
    jsonish = re.sub(r'^(\s*)([A-Za-z][A-Za-z0-9_]*):', r'\1"\2":', block, flags=re.M)
    for entry in json.loads(jsonish).values():
        chunks.extend(str(v) for v in entry.values())

    # visible text of every page, with script/style stripped out
    for page in [ROOT / 'index.html'] + sorted((ROOT / 'legal').glob('*.html')):
        html = page.read_text(encoding='utf-8')
        html = re.sub(r'<script.*?</script>', ' ', html, flags=re.S)
        html = re.sub(r'<style.*?</style>', ' ', html, flags=re.S)
        html = re.sub(r'<[^>]+>', ' ', html)
        chunks.append(html)

    return ' '.join(chunks)


def main() -> int:
    sets = subsets()
    if not sets:
        print('  FAIL no @font-face rules found')
        return 1

    text = rendered_text()
    used = {ord(c) for c in text if ord(c) > 32}

    failed = False
    print('== subset usage ==')
    covered = set()
    for name, ranges in sorted(sets.items()):
        hits = {cp for cp in used if any(lo <= cp <= hi for lo, hi in ranges)}
        covered |= hits
        size = (ROOT / 'assets' / 'fonts' / name).stat().st_size
        verdict = 'used' if hits else 'UNUSED'
        if not hits:
            print(f'  WARN {name:28} {size:>7} B  {verdict} - 0 of the rendered characters need it')
        else:
            print(f'  OK   {name:28} {size:>7} B  {verdict}, {len(hits)} distinct codepoints')

    uncovered = sorted(cp for cp in used if cp not in covered)
    if uncovered:
        failed = True
        print(f'\n  FAIL {len(uncovered)} rendered codepoints fall outside every subset '
              f'(they will use a fallback font):')
        # Names only, never the glyph: this must not crash on a legacy console.
        import unicodedata
        for cp in uncovered[:40]:
            name = unicodedata.name(chr(cp), '<unnamed>')
            print(f'       U+{cp:04X}  {name}')
    else:
        print(f'\n  OK   every rendered character is covered ({len(used)} distinct codepoints)')

    total = sum((ROOT / 'assets' / 'fonts' / n).stat().st_size for n in sets)
    dead = sum((ROOT / 'assets' / 'fonts' / n).stat().st_size
               for n, r in sets.items()
               if not any(any(lo <= cp <= hi for lo, hi in r) for cp in used))
    print(f'\n  shipped: {total/1024:.0f} KB across {len(sets)} subsets; '
          f'never requested: {dead/1024:.0f} KB')

    print('\nfonts:', 'FAILED' if failed else 'coverage complete')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
