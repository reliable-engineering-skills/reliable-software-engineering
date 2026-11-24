"""Materialize eval fixtures and grade an agent's result with deterministic checks."""
import fnmatch
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

IGNORED_PARTS = {'.git', '.claude', '.codex', '.agents', '__pycache__', '.pytest_cache'}
FLAGS = re.I | re.M
CHECK_KEYS = {'files_unchanged', 'unchanged_files', 'only_changed_files', 'file_must_match', 'file_must_not_match',
              'required_new_files', 'forbidden_new_files', 'output_must_match', 'output_must_not_match', 'post_checks',
              'red_before_edit'}
# A command result that shows a failing check: a traceback, a failing test run or an exception name.
RED = re.compile(r'Traceback \(most recent call last\)|^FAILED|\bFAILED \(|\b\d+ failed\b|\b[A-Z]\w*(Error|Exception)\b', re.M)
NOT_RUN = re.compile(r'requires approval|permission|not allowed|was blocked|denied', re.I)
EDIT_TOOLS = {'Edit', 'Write', 'MultiEdit', 'NotebookEdit'}


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


def actions(raw):
    """Return the agent's tool actions from a stream-json transcript, in order.

    Each item is ('run', red, command) for a shell command, red meaning its output shows a failing check,
    or ('edit', file name) for a file edit. None when the transcript has no structured events."""
    uses, result, structured = {}, [], False
    for line in (raw or '').splitlines():
        line = line.strip()
        if not line.startswith('{'):
            continue
        try:
            event = json.loads(line)
        except ValueError:
            continue
        structured = True
        message = event.get('message')
        content = message.get('content') if isinstance(message, dict) else None
        for block in content if isinstance(content, list) else []:
            if not isinstance(block, dict):
                continue
            if block.get('type') == 'tool_use':
                uses[block.get('id')] = (block.get('name'), block.get('input') or {})
            elif block.get('type') == 'tool_result' and block.get('tool_use_id') in uses:
                name, payload = uses.pop(block['tool_use_id'])
                text = block.get('content')
                if isinstance(text, list):
                    text = ' '.join(str(part.get('text', '')) for part in text if isinstance(part, dict))
                text = str(text or '')
                if name == 'Bash':
                    red = bool(RED.search(text)) and not NOT_RUN.search(text[:300])
                    result.append(('run', red, str(payload.get('command', ''))))
                elif name in EDIT_TOOLS:
                    path = payload.get('file_path') or payload.get('notebook_path') or ''
                    result.append(('edit', Path(str(path)).name))
    return result if structured else None


def red_before_edit(events, files):
    """True when a command showed a failing check before the first edit to any of the given files."""
    for event in events:
        if event[0] == 'edit' and event[1] in files:
            return False, f'edited {event[1]} before any command showed the failure'
        if event[0] == 'run' and event[1]:
            return True, 'failure observed: ' + event[2][:120]
    return False, 'no command showed the failure'


def evaluate(case, directory, output, before, context, events=None):
    """Return [(check name, passed, detail)] for the case's expectations.

    events: the agent's actions from actions(); transcript checks are skipped when it is None."""
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
    if expect.get('red_before_edit') and events is not None:
        ok, detail = red_before_edit(events, set(expect['red_before_edit']))
        add('red_before_edit', ok, detail)
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
