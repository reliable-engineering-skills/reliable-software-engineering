#!/usr/bin/env python3
"""Lint the skill suite: frontmatter, relative links and anchors, size budgets, and banned residue."""
import os
import re
import sys
from pathlib import Path

if sys.version_info < (3, 9):
    sys.exit('Python 3.9 or newer is required')

CORE = 'reliable-software-engineering'


def find_root():
    """RSE_SKILLS_DIR, a monorepo skills/ sibling, or the folder the core repo is cloned into."""
    here = Path(__file__).resolve()
    candidates = [os.environ.get('RSE_SKILLS_DIR'), here.parents[1] / 'skills', here.parents[3] if len(here.parents) > 3 else None]
    for candidate in candidates:
        if candidate and (Path(candidate) / CORE / 'SKILL.md').is_file():
            return Path(candidate).resolve()
    sys.exit('Cannot find the skills folder; set RSE_SKILLS_DIR to the folder containing the four skills')


ROOT = find_root()
# Repository scaffolding next to a skill is not skill content: skip suite tooling, CI and VCS folders.
SKIP_PARTS = {'suite', '.github', '.git'}
LINK = re.compile(r'\]\(([^)\s]+)\)')
HEADING = re.compile(r'^#{1,6}\s+(.+?)\s*#*\s*$', re.M)
ANCHOR = re.compile(r'<a\s+id=["\']([^"\']+)["\']')
NAME = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')
# Residue that 3.0.0 removed on purpose; reintroducing it should be a deliberate decision.
BANNED = [
    (re.compile(r'\bArabic\b'), 'language policy belongs in user instructions, not a skill'),
    (re.compile(r'\b(Sonnet|Opus|Haiku|Fable)\s+\d'), 'pinned model name outside the sources list'),
    (re.compile(r'\bN[0-9]\b'), 'authoring-source ID (moved to docs/)'),
]
SKILL_MAX_LINES = 500


def slugs(text):
    seen, out = {}, set()
    for heading in HEADING.findall(text):
        base = re.sub(r'[^\w\- ]', '', heading.lower()).strip().replace(' ', '-')
        n = seen.get(base, 0)
        seen[base] = n + 1
        out.add(base if n == 0 else f'{base}-{n}')
    return out | set(ANCHOR.findall(text))


def frontmatter(text):
    if not text.startswith('---\n'):
        return None
    end = text.find('\n---\n', 4)
    if end < 0:
        return None
    fields = {}
    for line in text[4:end].splitlines():
        if line and not line.startswith(' ') and ':' in line:
            key, value = line.split(':', 1)
            fields[key.strip()] = value.strip().strip('"')
    return fields


def main():
    errors, report = [], []
    # Only this suite's skills: the folder may also hold unrelated skills (e.g. ~/.claude/skills).
    skills = sorted(p for p in ROOT.iterdir() if p.is_dir() and (p.name == CORE or p.name.startswith('rse-')))
    if CORE not in {p.name for p in skills}:
        errors.append(f'core skill {CORE} is missing')
    for skill in skills:
        entry = skill / 'SKILL.md'
        if not entry.is_file():
            errors.append(f'{skill.name}: missing SKILL.md')
            continue
        text = entry.read_text(encoding='utf-8')
        fm = frontmatter(text)
        if fm is None:
            errors.append(f'{skill.name}: SKILL.md has no YAML frontmatter')
            continue
        if fm.get('name') != skill.name or not NAME.match(skill.name) or len(skill.name) > 64:
            errors.append(f'{skill.name}: frontmatter name must equal the folder name (lowercase-hyphen, <=64)')
        description = fm.get('description', '')
        if not description or len(description) > 1024 or '<' in description or '>' in description:
            errors.append(f'{skill.name}: description must be 1-1024 chars without angle brackets')
        lines = text.count('\n')
        if lines > SKILL_MAX_LINES:
            errors.append(f'{skill.name}: SKILL.md has {lines} lines (budget {SKILL_MAX_LINES})')
        if skill.name != CORE and f'../{CORE}/' in text and not (ROOT / CORE).is_dir():
            errors.append(f'{skill.name}: depends on {CORE} which is absent')
        report.append(f'{skill.name}: {len(text.split())} words in SKILL.md, '
                      f'{sum(len(p.read_text(encoding="utf-8").split()) for p in skill.rglob("*.md"))} words total')
    for md in sorted(m for skill in skills for m in skill.rglob('*.md')):
        if SKIP_PARTS & set(md.relative_to(ROOT).parts):
            continue
        rel = md.relative_to(ROOT).as_posix()
        text = md.read_text(encoding='utf-8')
        # The sources list cites model docs, and the changelog records what was removed; both are history.
        if md.name != 'CHANGELOG.md' and (md.parts[-3:-1] != (CORE, 'references') or md.name != 'standards-sources.md'):
            for pattern, why in BANNED:
                for match in pattern.finditer(text):
                    line = text.count('\n', 0, match.start()) + 1
                    errors.append(f'{rel}:{line}: {match.group(0)!r} - {why}')
        if CORE in md.parts and f'../rse-' in text:
            errors.append(f'{rel}: core skill must not link into companion skills')
        for target in LINK.findall(text):
            if re.match(r'^[a-z][a-z0-9+.-]*:', target):
                continue  # absolute URL
            path_part, _, fragment = target.partition('#')
            dest = md if not path_part else (md.parent / path_part).resolve()
            line = text.count('\n', 0, text.find(target)) + 1
            if not dest.exists():
                errors.append(f'{rel}:{line}: broken link {target}')
                continue
            if not dest.resolve().is_relative_to(ROOT.resolve()):
                errors.append(f'{rel}:{line}: link escapes the skills folder {target}')
            if fragment and dest.suffix == '.md' and fragment not in slugs(dest.read_text(encoding='utf-8')):
                errors.append(f'{rel}:{line}: missing anchor {target}')
    print('\n'.join(report))
    if errors:
        print('\n'.join(['', f'{len(errors)} problem(s):'] + errors))
        return 1
    print('\nAll skills valid: frontmatter, links, anchors and residue checks passed.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
