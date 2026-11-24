"""Materialize eval fixtures and grade an agent's result with deterministic checks."""
import fnmatch
import hashlib
import re
import subprocess
import sys
from pathlib import Path

IGNORED_PARTS = {'.git', '.claude', '.codex', '.agents', '__pycache__', '.pytest_cache'}
FLAGS = re.I | re.M
CHECK_KEYS = {'files_unchanged', 'unchanged_files', 'only_changed_files', 'file_must_match', 'file_must_not_match',
              'required_new_files', 'forbidden_new_files', 'output_must_match', 'output_must_not_match', 'post_checks'}


def materialize(case, directory):
    directory = Path(directory)
    for rel, content in case['files'].items():
        path = directory / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content.encode('utf-8'))  # keeps LF exactly; write_text(newline=) needs Python 3.10


def snapshot(directory):
    directory = Path(directory)
    result = {}
    for path in directory.rglob('*'):
        rel = path.relative_to(directory)
        if path.is_file() and not (set(rel.parts) & IGNORED_PARTS) and path.suffix != '.pyc':
            result[rel.as_posix()] = hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest()
    return result


def read(directory, rel):
    path = Path(directory) / rel
    return path.read_text(encoding='utf-8', errors='replace') if path.is_file() else None


def fill(arg, context):
    return arg.replace('{python}', context['python']).replace('{skills}', context['skills'])


def evaluate(case, directory, output, before, context):
    """Return [(check name, passed, detail)] for the case's expectations."""
    expect = case['expect']
    after = snapshot(directory)
    changed = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
    new = sorted(k for k in after if k not in before)
    results = []

    def add(name, passed, detail=''):
        results.append((name, bool(passed), detail))

    if expect.get('files_unchanged'):
        add('files_unchanged', not changed, ', '.join(changed))
    for rel in expect.get('unchanged_files', []):
        add('unchanged:' + rel, before.get(rel) is not None and before.get(rel) == after.get(rel))
    if 'only_changed_files' in expect:
        extra = [c for c in changed if c not in expect['only_changed_files']]
        add('only_changed_files', not extra, ', '.join(extra))
    for rel, pattern in expect.get('file_must_match', {}).items():
        text = read(directory, rel)
        add('file_must_match:' + rel, text is not None and re.search(pattern, text, FLAGS), pattern)
    for rel, pattern in expect.get('file_must_not_match', {}).items():
        text = read(directory, rel)
        add('file_must_not_match:' + rel, text is not None and not re.search(pattern, text, FLAGS), pattern)
    for pattern in expect.get('required_new_files', []):
        add('required_new:' + pattern, any(fnmatch.fnmatch(n, pattern) for n in new))
    for pattern in expect.get('forbidden_new_files', []):
        hits = [n for n in new if fnmatch.fnmatch(n, pattern)]
        add('forbidden_new:' + pattern, not hits, ', '.join(hits))
    for pattern in expect.get('output_must_match', []):
        add('output_must_match', re.search(pattern, output, FLAGS), pattern)
    for pattern in expect.get('output_must_not_match', []):
        add('output_must_not_match', not re.search(pattern, output, FLAGS), pattern)
    for check in expect.get('post_checks', []):
        argv = [fill(a, context) for a in check['argv']] if 'argv' in check else \
            [context['python'], '-B', '-c', check['code']]
        try:
            proc = subprocess.run(argv, cwd=directory, capture_output=True, text=True, timeout=120,
                                  stdin=subprocess.DEVNULL)
            ok = proc.returncode == check.get('expect_exit', 0)
            detail = (proc.stdout + proc.stderr)[-400:].strip()
        except (OSError, subprocess.TimeoutExpired) as exc:
            ok, detail = False, str(exc)
        add('post_check:' + check['name'], ok, detail)
    return results


def find_skills_dir(here):
    """Locate the folder holding the suite skills.

    Order: RSE_SKILLS_DIR, a monorepo `skills/` sibling, or the folder the core skill repo sits in
    (suite/evals inside ~/.claude/skills/reliable-software-engineering when the repos are cloned side by side).
    """
    import os
    here = Path(here).resolve()
    candidates = [os.environ.get('RSE_SKILLS_DIR'), here.parent / 'skills', here.parents[2] if len(here.parents) > 2 else None]
    for candidate in candidates:
        if candidate and (Path(candidate) / 'reliable-software-engineering' / 'SKILL.md').is_file():
            return Path(candidate).resolve()
    raise SystemExit('Cannot find the skills folder; set RSE_SKILLS_DIR to the folder containing the four skills')


def default_context(skills_dir):
    return {'python': sys.executable, 'skills': str(Path(skills_dir).resolve())}
