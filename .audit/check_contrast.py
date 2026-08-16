#!/usr/bin/env python3
"""WCAG contrast audit for every colour pair the site actually renders.

Colour tokens are read from assets/site.css, so the check follows the stylesheet
instead of a hard-coded copy of it. Run:  python .audit/check_contrast.py
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSS = ROOT / 'assets' / 'site.css'


def linear(channel: float) -> float:
    channel /= 255
    return channel / 12.92 if channel <= 0.03928 else ((channel + 0.055) / 1.055) ** 2.4


def luminance(hex_colour: str) -> float:
    hex_colour = hex_colour.lstrip('#')
    r, g, b = (int(hex_colour[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * linear(r) + 0.7152 * linear(g) + 0.0722 * linear(b)


def ratio(fg: str, bg: str) -> float:
    a, b = luminance(fg), luminance(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def tokens_from(block: str) -> dict:
    return {name: value for name, value in re.findall(r'(--color-[\w-]+):\s*(#[0-9a-fA-F]{6})', block)}


def read_themes() -> dict:
    css = CSS.read_text(encoding='utf-8')
    light = tokens_from(re.search(r':root\s*\{(.*?)\}', css, re.S).group(1))
    dark = tokens_from(re.search(r':root\[data-theme="dark"\]\s*\{(.*?)\}', css, re.S).group(1))
    return {'LIGHT': light, 'DARK': {**light, **dark}}


# (label, foreground token, background token, required ratio)
CASES = [
    ('body text on page background',   '--color-text',         '--color-bg',            4.5),
    ('body text on card',              '--color-text',         '--color-card',          4.5),
    ('muted text on card',             '--color-muted',        '--color-card',          4.5),
    ('muted text on page background',  '--color-muted',        '--color-bg',            4.5),
    ('heading on card',                '--color-primary',      '--color-card',          4.5),
    ('link on card',                   '--color-accent-dark',  '--color-card',          4.5),
    ('footer link on page background', '--color-accent-dark',  '--color-bg',            4.5),
    ('active language button label',   '--color-on-accent',    '--color-accent-strong', 4.5),
    ('skip-link label',                '--color-on-accent',    '--color-accent-strong', 4.5),
    ('theme toggle hover label',       '--color-on-accent',    '--color-accent-strong', 4.5),
    ('focus ring vs page background',  '--color-accent-dark',  '--color-bg',            3.0),
    ('icon glyph vs gradient start',   '--color-on-accent',    '--color-icon-from',     3.0),
    ('icon glyph vs gradient end',     '--color-on-accent',    '--color-icon-to',       3.0),
    ('card border vs card',            '--color-border',       '--color-card',          1.0),
]


def main() -> int:
    themes = read_themes()
    failed = False
    for theme_name, tokens in themes.items():
        print(f'== {theme_name} ==')
        for label, fg, bg, need in CASES:
            if fg not in tokens or bg not in tokens:
                print(f'  FAIL {label:34} missing token {fg if fg not in tokens else bg}')
                failed = True
                continue
            value = ratio(tokens[fg], tokens[bg])
            ok = value >= need
            failed |= not ok
            print(f'  {"OK  " if ok else "FAIL"} {label:34} '
                  f'{tokens[fg]} on {tokens[bg]} = {value:5.2f}:1 (need {need})')
        print()
    print('contrast:', 'FAILED' if failed else 'all pairs meet their threshold')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
