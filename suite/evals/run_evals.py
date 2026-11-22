#!/usr/bin/env python3
"""Run the behavioral cases against a real agent CLI, with and without the skills, and grade the results.

This calls a paid model for every case x config x run. Start with --cases and --runs 1.

  py -3 evals/run_evals.py --agent claude --runs 1 --cases core-review-is-read-only
  py -3 evals/run_evals.py --agent claude --runs 3            # full A/B comparison

Results land in evals/results/<timestamp>/ (summary.md, results.json, per-run output and diff).
Deterministic checks give a pass rate; rubric items are listed for human or LLM grading.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

if sys.version_info < (3, 9):
    sys.exit('Python 3.9 or newer is required')

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cases as suite  # noqa: E402
import harness  # noqa: E402

SKILLS = harness.find_skills_dir(HERE)
PROFILES = {
    # Claude Code CLI: project skills are read from .claude/skills in the working directory.
    'claude': {'argv': ['claude', '-p', '{prompt}', '--output-format', 'text',
                        '--permission-mode', 'acceptEdits', '--max-turns', '40'],
               'skills_subdir': '.claude/skills'},
    # Codex CLI: flags and the repo-level skills folder vary by version; confirm both before relying on results.
    'codex': {'argv': ['codex', 'exec', '--full-auto', '--skip-git-repo-check', '{prompt}'],
              'skills_subdir': '.agents/skills'},
}
SUFFIX = '\n\nReply in English.'  # grading regexes are English; user-level language preferences may differ.


def git(directory, *args):
    return subprocess.run(['git', '-c', 'user.name=eval', '-c', 'user.email=eval@localhost',
                           '-c', 'core.autocrlf=false', *args],
                          cwd=directory, capture_output=True, text=True, check=False).stdout


def run_once(case, config, profile, args, out_dir):
    with tempfile.TemporaryDirectory(prefix='rse-eval-') as tmp:
        harness.materialize(case, tmp)
        git(tmp, 'init', '-q')
        git(tmp, 'add', '-A')
        git(tmp, 'commit', '-qm', 'fixture')
        before = harness.snapshot(tmp)
        if config == 'with':
            target = Path(tmp) / profile['skills_subdir']
            target.mkdir(parents=True)
            for skill in SKILLS.iterdir():
                if (skill / 'SKILL.md').is_file():
                    shutil.copytree(skill, target / skill.name, ignore=shutil.ignore_patterns('tests', 'suite', '.git', '.github', '__pycache__'))
        prompt = case['prompt'] + args.suffix
        argv = [a.replace('{prompt}', prompt) for a in profile['argv']]
        located = shutil.which(argv[0])
        if located:
            argv[0] = located  # resolves claude.cmd / codex.cmd on Windows
        env = dict(os.environ, RSE_EVAL_CASE=case['id'])
        start = time.monotonic()
        try:
            proc = subprocess.run(argv, cwd=tmp, capture_output=True, text=True, encoding='utf-8',
                                  errors='replace', timeout=args.timeout, stdin=subprocess.DEVNULL, env=env)
            output, agent_exit = proc.stdout + ('\n' + proc.stderr if proc.stderr.strip() else ''), proc.returncode
        except subprocess.TimeoutExpired:
            output, agent_exit = '[agent timed out]', None
        except OSError as exc:
            sys.exit(f'Cannot start agent {argv[0]!r}: {exc}')
        seconds = round(time.monotonic() - start, 1)
        git(tmp, 'add', '-A', '--', '.', ':(exclude).claude', ':(exclude).agents', ':(exclude).codex')
        diff = git(tmp, 'diff', '--cached', 'HEAD')
        checks = harness.evaluate(case, tmp, output, before, harness.default_context(SKILLS))
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / 'output.txt').write_text(output, encoding='utf-8')
    (out_dir / 'diff.patch').write_text(diff, encoding='utf-8')
    return {'agent_exit': agent_exit, 'seconds': seconds, 'passed': all(ok for _, ok, _ in checks),
            'checks': [{'name': n, 'passed': ok, 'detail': det} for n, ok, det in checks]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--agent', default='claude', help='profile name (claude, codex) or a JSON argv list with {prompt}')
    parser.add_argument('--skills-subdir', help='where the agent reads project skills (overrides the profile)')
    parser.add_argument('--configs', default='with,without', help='comma list of: with, without')
    parser.add_argument('--cases', help='comma list of case ids (default: all)')
    parser.add_argument('--runs', type=int, default=1)
    parser.add_argument('--timeout', type=int, default=900, help='seconds per agent run')
    parser.add_argument('--suffix', default=SUFFIX, help='text appended to every prompt')
    parser.add_argument('--out', type=Path, default=HERE / 'results')
    args = parser.parse_args(argv)

    if args.agent in PROFILES:
        profile = dict(PROFILES[args.agent])
    else:
        profile = {'argv': json.loads(args.agent), 'skills_subdir': '.claude/skills'}
    if args.skills_subdir:
        profile['skills_subdir'] = args.skills_subdir
    configs = [c for c in args.configs.split(',') if c]
    if not set(configs) <= {'with', 'without'}:
        parser.error('configs must be with and/or without')
    selected = suite.CASES if not args.cases else [c for c in suite.CASES if c['id'] in args.cases.split(',')]
    if not selected:
        parser.error('no matching cases')

    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    root = args.out / stamp
    results = []
    for case in selected:
        for config in configs:
            for run in range(1, args.runs + 1):
                print(f'{case["id"]} [{config}] run {run}/{args.runs} ...', flush=True)
                record = run_once(case, config, profile, args, root / case['id'] / f'{config}-{run}')
                record.update(case=case['id'], config=config, run=run)
                results.append(record)
                print('   ', 'PASS' if record['passed'] else 'FAIL', f'({record["seconds"]}s)', flush=True)

    (root / 'results.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
    lines = ['# Eval results ' + stamp, '', f'Agent: `{" ".join(profile["argv"])}`', '',
             '| Case | ' + ' | '.join(configs) + ' |', '| --- |' + ' --- |' * len(configs)]
    totals = {c: [0, 0] for c in configs}
    for case in selected:
        cells = []
        for config in configs:
            runs = [r for r in results if r['case'] == case['id'] and r['config'] == config]
            passed = sum(r['passed'] for r in runs)
            totals[config][0] += passed
            totals[config][1] += len(runs)
            cells.append(f'{passed}/{len(runs)}')
        lines.append(f'| {case["id"]} | ' + ' | '.join(cells) + ' |')
    lines.append('| **total** | ' + ' | '.join(f'**{p}/{n}**' for p, n in totals.values()) + ' |')
    lines += ['', '## Rubric for manual or LLM grading', '']
    for case in selected:
        lines.append(f'- **{case["id"]}**: ' + ' '.join(case['rubric']))
    (root / 'summary.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('\n'.join(lines[4:5 + len(selected) + 1]))
    print(f'\nWrote {root}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
