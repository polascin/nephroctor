#!/usr/bin/env python3
"""Formatting audit against the convention this project actually uses.

Prettier is deliberately not the gate. Measured in Beh #8: running it would
rewrite 2034 of 918 lines in index.html, i.e. impose a different style rather
than fix formatting. A check that can only ever fail trains you to ignore it,
so this checks the conventions the repository really follows.

Line endings are read through git, not from the working tree: on Windows the
checkout is CRLF by design while the repository stores LF, and comparing the
working tree would report a problem that does not exist.

Run:  python .audit/check_format.py
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Hand-maintained site files: 4-space indent is the convention.
SITE = ['index.html', 'assets/site.css', 'assets/legal.js'] + \
       [f'legal/{p.name}' for p in sorted((ROOT / 'legal').glob('*.html'))]
# Config and tooling: whitespace hygiene only, each has its own idiom.
OTHER = ['robots.txt', 'site.webmanifest', 'sitemap.xml', '.htaccess'] + \
        [f'.audit/{p.name}' for p in sorted((ROOT / '.audit').glob('*.py'))] + \
        [f'.audit/{p.name}' for p in sorted((ROOT / '.audit').glob('*.js'))]


def repo_line_endings() -> dict:
    """Map path -> index eol as git records it."""
    try:
        out = subprocess.run(['git', 'ls-files', '--eol'], cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout
    except Exception:                                           # noqa: BLE001
        return {}
    endings = {}
    for line in out.splitlines():
        parts = line.split('\t')
        if len(parts) == 2:
            attrs = parts[0].split()
            index = next((a for a in attrs if a.startswith('i/')), '')
            endings[parts[1].strip()] = index
    return endings


def mask_comments(lines, suffix):
    """Blank out comment bodies, keeping line numbering intact."""
    opener, closer = ('<!--', '-->') if suffix == '.html' else ('/*', '*/')
    out, inside = [], False
    for line in lines:
        stripped = line.strip()
        if inside:
            out.append('')
            if closer in line:
                inside = False
            continue
        if opener in line and closer not in line:
            inside = True
            out.append('')
            continue
        if stripped.startswith(opener) or stripped.startswith('//'):
            out.append('')
            continue
        out.append(line)
    return out


def audit(rel: str, eols: dict, check_indent: bool):
    path = ROOT / rel
    if not path.exists():
        return [f'missing']

    text = path.read_text(encoding='utf-8')
    normalised = text.replace('\r\n', '\n')
    lines = normalised.split('\n')
    problems = []

    if '\t' in normalised:
        problems.append(f'contains {normalised.count(chr(9))} tab character(s)')

    eol = eols.get(rel.replace('\\', '/'))
    if eol and eol not in ('i/lf', 'i/none'):
        problems.append(f'repository line ending is {eol}, expected i/lf')

    if not normalised.endswith('\n'):
        problems.append('no trailing newline')
    elif normalised.endswith('\n\n'):
        problems.append('blank line at end of file')

    trailing = [i for i, l in enumerate(lines, 1) if l != l.rstrip()]
    if trailing:
        problems.append(f'trailing whitespace on {len(trailing)} line(s), first at line {trailing[0]}')

    if check_indent:
        # Only whole-tag/declaration lines. Continuation lines inside a text run,
        # an attribute list or a comment align to something other than a 4-step,
        # so comment bodies are masked out before the indent is measured.
        code = mask_comments(lines, path.suffix)
        odd = [i for i, l in enumerate(code, 1)
               if l.strip().startswith(('<', '.', '#', '@', ':', '}'))
               and (len(l) - len(l.lstrip(' '))) % 4]
        if odd:
            problems.append(f'indent not a multiple of 4 on {len(odd)} line(s), first at line {odd[0]}')

    return problems


def main() -> int:
    eols = repo_line_endings()
    failed = False
    for group, files, indent in (('site files', SITE, True), ('config and tooling', OTHER, False)):
        print(f'== {group} ==')
        for rel in files:
            problems = audit(rel, eols, indent)
            if problems:
                failed = True
                print(f'  FAIL {rel}')
                for p in problems:
                    print(f'        - {p}')
            else:
                n = len((ROOT / rel).read_text(encoding='utf-8').replace('\r\n', '\n').split('\n'))
                print(f'  OK   {rel:38} {n:>4} lines')
        print()

    print('formatting:', 'FAILED' if failed else 'consistent with the project convention')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
