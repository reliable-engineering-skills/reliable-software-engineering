#!/usr/bin/env python3
"""Run the behavioral cases against a real agent, with and without the skills, and grade the results.

Every case x arm x run is a paid model session. Check isolation first, then start with one case:

  py -3 suite/evals/run_evals.py --check                                   # no model call
  py -3 suite/evals/run_evals.py --cases core-review-is-read-only          # 2 sessions, needs --confirm
  py -3 suite/evals/run_evals.py --runs 5 --confirm --max-cost-usd 40      # full A/B baseline

Isolation (Claude Code). The no-skill arm must not see the skills through user-level installs,
CLAUDE.md, auto memory, user settings, hooks or MCP servers; otherwise the comparison is meaningless.
  profile  (default) a dedicated Claude Code profile via CLAUDE_CONFIG_DIR that holds no skills, plus
           --setting-sources project,local, --strict-mcp-config and CLAUDE.md/memory disabled. Uses a
           subscription login made once inside that profile (see --check for the command).
  bare     claude --bare: skips all auto-discovery and loads skills only from --add-dir. Needs
           ANTHROPIC_API_KEY (bare mode never reads subscription OAuth credentials).
A run is marked CONTAMINATED, and the whole run stops, if the no-skill arm invokes or lists a suite skill.

Results land in suite/evals/results/<timestamp>/: summary.md, results.json, and per run the final
answer, the raw event stream and the diff. Rubric items are listed for human or LLM grading.
"""
import argparse
import json
import os
import re
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
SUITE_NAMES = sorted(p.name for p in SKILLS.iterdir()
                     if (p / 'SKILL.md').is_file() and (p.name == 'reliable-software-engineering' or p.name.startswith('rse-')))
COPY_IGNORE = shutil.ignore_patterns('tests', 'suite', '.git', '.github', '__pycache__')
STREAM = ['--output-format', 'stream-json', '--verbose', '--permission-mode', 'acceptEdits', '--max-turns', '40']
# --allow-exec: let the agent run Python and pytest (tests, reproductions) inside the session's temporary repo.
EXEC_RULES = ['Bash(python:*)', 'Bash(python3:*)', 'Bash(py:*)', 'Bash(pytest:*)']
PROFILES = {
    'claude': {'argv': ['claude', '-p', '{prompt}', *STREAM], 'skills_subdir': '.claude/skills', 'isolation': 'profile',
               'exec_argv': ['--allowedTools', *EXEC_RULES]},
    # Codex: flags, skills folder and isolation are unverified for current versions; results are indicative only.
    'codex': {'argv': ['codex', 'exec', '--full-auto', '--skip-git-repo-check', '{prompt}'],
              'skills_subdir': '.agents/skills', 'isolation': 'none'},
}
ISOLATION_ENV = {
    'CLAUDE_CODE_DISABLE_CLAUDE_MDS': '1',            # no user/project CLAUDE.md or auto-memory files in context
    'CLAUDE_CODE_DISABLE_AUTO_MEMORY': '1',
    'CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC': '1',  # no auto-update or telemetry during measurement
}
DEFAULT_PROFILE_DIR = Path.home() / '.rse-eval-claude-profile'


class Contaminated(Exception):
    pass


class AgentUnavailable(Exception):
    """The agent answered with a service message (usage limit, auth, API error) instead of doing the task."""


# Service messages, matched against the final answer only. Keep them specific: broad words such as
# "rate limit" also appear in legitimate task content.
UNAVAILABLE = re.compile(r"^(You've hit your [\w-]+ limit|You've reached your|Credit balance is too low|"
                         r"Invalid API key|Please run /login|API Error: (401|403|429|5\d\d))", re.I)


def git(directory, *args):
    return subprocess.run(['git', '-c', 'user.name=eval', '-c', 'user.email=eval@localhost',
                           '-c', 'core.autocrlf=false', *args],
                          cwd=directory, capture_output=True, text=True, check=False).stdout


def parse_stream(raw):
    """Extract the final answer, invoked skills, listed skills and usage from a stream-json transcript.

    Returns None for fields the agent did not report (plain-text agents, older CLIs)."""
    info = {'text': None, 'skills_invoked': [], 'skills_listed': None, 'cost_usd': None,
            'turns': None, 'model': None, 'structured': False, 'is_error': False, 'result_seen': False}
    for line in raw.splitlines():
        line = line.strip()
        if not line.startswith('{'):
            continue
        try:
            event = json.loads(line)
        except ValueError:
            continue
        info['structured'] = True
        kind = event.get('type')
        if kind == 'system' and event.get('subtype') == 'init':
            info['model'] = event.get('model')
            if isinstance(event.get('skills'), list):
                info['skills_listed'] = [s if isinstance(s, str) else s.get('name') for s in event['skills']]
        elif kind == 'assistant':
            for block in (event.get('message') or {}).get('content') or []:
                if isinstance(block, dict) and block.get('type') == 'tool_use' and block.get('name') == 'Skill':
                    payload = block.get('input') or {}
                    name = payload.get('skill') or payload.get('name') or payload.get('command')
                    if name:
                        info['skills_invoked'].append(str(name).lstrip('/').split(':')[-1])
        elif kind == 'result':
            info['text'] = event.get('result')
            info['cost_usd'] = event.get('total_cost_usd')
            info['turns'] = event.get('num_turns')
            info['result_seen'] = True
            info['is_error'] = bool(event.get('is_error')) or str(event.get('subtype', '')).startswith('error')
    return info


def isolation_env(mode, args):
    env = dict(os.environ)
    if mode in ('profile', 'bare'):
        env.update(ISOLATION_ENV)
    if mode == 'profile':
        env['CLAUDE_CONFIG_DIR'] = str(args.profile_dir)
    return env


def exec_environment(env):
    """Put the interpreter running the evals first on PATH, ahead of stubs such as the Windows Store python.exe."""
    env = dict(env)
    env['PATH'] = os.pathsep.join([str(Path(sys.executable).parent), env.get('PATH', '')])
    return env


def check_isolation(mode, args):
    """Return a list of problems that make a measurement untrustworthy; empty means ready."""
    problems = []
    if mode == 'profile':
        profile = args.profile_dir
        if not profile.is_dir() or not any(profile.iterdir()):
            problems.append(f'profile {profile} is missing or empty. Log in once inside it:\n'
                            f'  PowerShell: $env:CLAUDE_CONFIG_DIR="{profile}"; claude   (then /login, then exit)\n'
                            f'  bash:       CLAUDE_CONFIG_DIR="{profile}" claude')
        else:
            leaked = [n for n in SUITE_NAMES if (profile / 'skills' / n).exists()]
            if leaked:
                problems.append(f'profile {profile} has suite skills installed: {", ".join(leaked)}')
    elif mode == 'bare':
        if not os.environ.get('ANTHROPIC_API_KEY'):
            problems.append('bare mode needs ANTHROPIC_API_KEY (it never reads subscription credentials)')
    return problems


def install_skills(target, fixture_skills, with_suite):
    target.mkdir(parents=True, exist_ok=True)
    if fixture_skills.is_dir():
        for skill in fixture_skills.iterdir():
            if not (target / skill.name).exists():
                shutil.copytree(skill, target / skill.name)
    if with_suite:
        for name in SUITE_NAMES:
            shutil.copytree(SKILLS / name, target / name, ignore=COPY_IGNORE)


def run_once(case, arm, profile, mode, args, out_dir):
    with tempfile.TemporaryDirectory(prefix='rse-eval-') as tmp_root:
        work = Path(tmp_root) / 'repo'
        work.mkdir()
        harness.materialize(case, work)
        git(work, 'init', '-q')
        git(work, 'add', '-A')
        git(work, 'commit', '-qm', 'fixture')
        before = harness.snapshot(work)
        fixture_skills = work / '.claude' / 'skills'
        extra = []
        if mode == 'bare':
            # Bare mode ignores project skills; every skill, fixture ones included, comes from --add-dir.
            skills_root = Path(tmp_root) / 'skills-root'
            install_skills(skills_root / '.claude' / 'skills', fixture_skills, arm == 'with')
            extra = ['--add-dir', str(skills_root)]
        elif arm == 'with':
            install_skills(work / profile['skills_subdir'], Path('/nonexistent'), True)
        if mode == 'bare':
            argv = [profile['argv'][0], '--bare'] + profile['argv'][1:]
        else:
            argv = list(profile['argv'])
        if mode in ('profile', 'bare'):
            argv += ['--strict-mcp-config']
        if mode == 'profile':
            argv += ['--setting-sources', 'project,local']
        if args.user_instructions:
            # Stands in for ~/.claude/CLAUDE.md or Codex developer_instructions, which isolation disables.
            argv += ['--append-system-prompt-file', str(args.user_instructions)]
        if args.model:
            argv += ['--model', args.model]
        if args.allow_exec:
            argv += profile.get('exec_argv', [])
        prompt = case['prompt'] + args.suffix
        argv = [a.replace('{prompt}', prompt) for a in argv] + extra
        located = shutil.which(argv[0])
        if located:
            argv[0] = located  # resolves claude.cmd / codex.cmd on Windows
        env = isolation_env(mode, args)
        env.update(RSE_EVAL_CASE=case['id'], RSE_EVAL_ARM=arm)
        if args.allow_exec:
            env = exec_environment(env)
        start = time.monotonic()
        try:
            proc = subprocess.run(argv, cwd=work, capture_output=True, text=True, encoding='utf-8',
                                  errors='replace', timeout=args.timeout, stdin=subprocess.DEVNULL, env=env)
            raw, stderr, agent_exit = proc.stdout, proc.stderr, proc.returncode
        except subprocess.TimeoutExpired as exc:
            raw = exc.stdout if isinstance(exc.stdout, str) else ''
            stderr, agent_exit = '[agent timed out]', None
        except OSError as exc:
            sys.exit(f'Cannot start agent {argv[0]!r}: {exc}')
        seconds = round(time.monotonic() - start, 1)
        info = parse_stream(raw)
        answer = info['text'] if info['text'] is not None else raw
        git(work, 'add', '-A', '--', '.', ':(exclude).claude', ':(exclude).agents', ':(exclude).codex',
            ':(exclude,glob)**/__pycache__/**', ':(exclude,glob)**/.pytest_cache/**')
        diff = git(work, 'diff', '--cached', 'HEAD')
        checks = harness.evaluate(case, work, answer, before, harness.default_context(SKILLS),
                                  events=harness.actions(raw))
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / 'answer.txt').write_text(answer or '', encoding='utf-8')
    (out_dir / 'stream.jsonl').write_text(raw or '', encoding='utf-8')
    (out_dir / 'stderr.txt').write_text(stderr or '', encoding='utf-8')
    (out_dir / 'diff.patch').write_text(diff, encoding='utf-8')
    invoked_suite = sorted({s for s in info['skills_invoked'] if s in SUITE_NAMES})
    listed_suite = None if info['skills_listed'] is None else sorted(set(info['skills_listed']) & set(SUITE_NAMES))
    record = {'agent_exit': agent_exit, 'seconds': seconds, 'passed': all(ok for _, ok, _ in checks),
              'checks': [{'name': n, 'passed': ok, 'detail': det} for n, ok, det in checks],
              'structured': info['structured'], 'model': info['model'], 'cost_usd': info['cost_usd'],
              'turns': info['turns'], 'skills_invoked': info['skills_invoked'], 'allow_exec': args.allow_exec,
              'triggered': (case['skill'] in info['skills_invoked']) if info['structured'] else None}
    answer_head = (answer or '').strip()
    if info['structured'] and (info['is_error'] or not info['result_seen'] or UNAVAILABLE.match(answer_head)):
        raise AgentUnavailable(f'{case["id"]} [{arm}]: {answer_head[:160] or "no result event"}; see {out_dir}')
    if arm == 'without' and (invoked_suite or listed_suite):
        raise Contaminated(f'{case["id"]}: the no-skill arm saw suite skills '
                           f'(invoked {invoked_suite or "-"}, listed {listed_suite or "-"}); see {out_dir}')
    return record


def summarize(results, selected, arms, header, stopped):
    lines = ['# Eval results', ''] + header + ['']
    if stopped:
        lines += [f'**Stopped early:** {stopped}', '']
    lines += ['| Case | ' + ' | '.join(f'{a} pass' for a in arms) + ' | skill triggered (with) |',
              '| --- |' + ' --- |' * (len(arms) + 1)]
    totals = {a: [0, 0] for a in arms}
    for case in selected:
        cells = []
        for arm in arms:
            runs = [r for r in results if r['case'] == case['id'] and r['config'] == arm]
            passed = sum(r['passed'] for r in runs)
            totals[arm][0] += passed
            totals[arm][1] += len(runs)
            cells.append(f'{passed}/{len(runs)}' if runs else '-')
        with_runs = [r for r in results if r['case'] == case['id'] and r['config'] == 'with' and r['triggered'] is not None]
        trig = f'{sum(r["triggered"] for r in with_runs)}/{len(with_runs)}' if with_runs else 'unknown'
        lines.append(f'| {case["id"]} | ' + ' | '.join(cells) + f' | {trig} |')
    lines.append('| **total** | ' + ' | '.join(f'**{p}/{n}**' for p, n in totals.values()) + ' | |')
    costs = {a: [r['cost_usd'] for r in results if r['config'] == a and r['cost_usd'] is not None] for a in arms}
    if any(costs.values()):
        lines += ['', '| Arm | sessions with cost | total USD | mean USD/session |', '| --- | --- | --- | --- |']
        for arm, values in costs.items():
            if values:
                lines.append(f'| {arm} | {len(values)} | {sum(values):.2f} | {sum(values) / len(values):.3f} |')
    lines += ['', '## Rubric for manual or LLM grading', '']
    lines += [f'- **{c["id"]}**: ' + ' '.join(c['rubric']) for c in selected]
    return lines


def cli_version(profile):
    exe = shutil.which(profile['argv'][0])
    if not exe:
        return None
    try:
        return subprocess.run([exe, '--version'], capture_output=True, text=True, timeout=30).stdout.strip() or None
    except (OSError, subprocess.TimeoutExpired):
        return None


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--agent', default='claude', help='profile name (claude, codex) or a JSON argv list with {prompt}')
    parser.add_argument('--isolation', choices=('profile', 'bare', 'none'),
                        help='default: profile for claude, none for codex and custom agents')
    parser.add_argument('--profile-dir', type=Path, default=DEFAULT_PROFILE_DIR,
                        help=f'dedicated CLAUDE_CONFIG_DIR for --isolation profile (default {DEFAULT_PROFILE_DIR})')
    parser.add_argument('--skills-subdir', help='where the agent reads project skills (overrides the profile)')
    parser.add_argument('--model', help='pin the model for every session (recommended for comparisons)')
    parser.add_argument('--user-instructions', type=Path,
                        help='file appended to the system prompt in every session, to measure user-level instructions')
    parser.add_argument('--allow-exec', action='store_true',
                        help='let the agent run python/py/pytest in its temporary repo (arbitrary code as your user)')
    parser.add_argument('--configs', default='with,without', help='comma list of: with, without')
    parser.add_argument('--cases', help='comma list of case ids (default: all)')
    parser.add_argument('--runs', type=int, default=1)
    parser.add_argument('--timeout', type=int, default=900, help='seconds per agent run')
    parser.add_argument('--suffix', default='', help='text appended to every prompt (default: none)')
    parser.add_argument('--max-cost-usd', type=float, default=10.0,
                        help='stop starting sessions once reported spend reaches this (default 10)')
    parser.add_argument('--confirm', action='store_true', help='required to run more than one session')
    parser.add_argument('--check', action='store_true', help='only verify isolation and the plan; no model call')
    parser.add_argument('--out', type=Path, default=HERE / 'results')
    args = parser.parse_args(argv)

    if args.agent in PROFILES:
        profile = dict(PROFILES[args.agent])
    else:
        profile = {'argv': json.loads(args.agent), 'skills_subdir': '.claude/skills', 'isolation': 'none'}
    if args.skills_subdir:
        profile['skills_subdir'] = args.skills_subdir
    mode = args.isolation or profile['isolation']
    if args.user_instructions:
        args.user_instructions = args.user_instructions.resolve()
        if not args.user_instructions.is_file():
            parser.error(f'--user-instructions file not found: {args.user_instructions}')
    arms = [c for c in args.configs.split(',') if c]
    if not set(arms) <= {'with', 'without'}:
        parser.error('configs must be with and/or without')
    selected = suite.CASES if not args.cases else [c for c in suite.CASES if c['id'] in args.cases.split(',')]
    if not selected:
        parser.error('no matching cases')
    sessions = len(selected) * len(arms) * args.runs

    problems = check_isolation(mode, args)
    print(f'Plan: {len(selected)} case(s) x {len(arms)} arm(s) x {args.runs} run(s) = {sessions} session(s); '
          f'isolation={mode}; exec={"python allowed" if args.allow_exec else "denied"}; spend cap ${args.max_cost_usd:.2f}; suite skills: {", ".join(SUITE_NAMES)}')
    if args.allow_exec and 'exec_argv' not in profile:
        print('WARNING: --allow-exec only puts Python on PATH for this agent; its own permission settings decide.')
    if mode == 'none':
        print('WARNING: no isolation; user-level skills, CLAUDE.md or memory may leak into the no-skill arm.')
    for problem in problems:
        print('NOT READY:', problem)
    if args.check:
        return 1 if problems else 0
    if problems:
        return 2
    if sessions > 1 and not args.confirm:
        print(f'Refusing to start {sessions} paid sessions without --confirm.')
        return 2

    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    root = args.out / stamp
    results, spent, stopped, code = [], 0.0, None, 0
    try:
        for case in selected:
            for arm in arms:
                for run in range(1, args.runs + 1):
                    if spent >= args.max_cost_usd:
                        stopped = f'spend cap ${args.max_cost_usd:.2f} reached after ${spent:.2f}'
                        raise StopIteration
                    print(f'{case["id"]} [{arm}] run {run}/{args.runs} ...', flush=True)
                    record = run_once(case, arm, profile, mode, args, root / case['id'] / f'{arm}-{run}')
                    record.update(case=case['id'], config=arm, run=run)
                    results.append(record)
                    spent += record['cost_usd'] or 0.0
                    cost = f', ${record["cost_usd"]:.3f}' if record['cost_usd'] is not None else ''
                    print(f'    {"PASS" if record["passed"] else "FAIL"} ({record["seconds"]}s{cost})', flush=True)
    except StopIteration:
        pass
    except Contaminated as exc:
        stopped, code = f'CONTAMINATED - isolation failed, results invalid. {exc}', 3
    except AgentUnavailable as exc:
        stopped, code = (f'AGENT UNAVAILABLE (usage limit, login or API error). That session is excluded; '
                         f'the {len(results)} sessions before it are valid. Resume later with the remaining cases. {exc}'), 4
    header = [f'- Agent: `{" ".join(profile["argv"])}`', f'- Isolation: {mode}',
              f'- User instructions: {args.user_instructions or "none"}',
              f'- Command execution: {"python, py and pytest allowed in the temporary repo" if args.allow_exec else "denied (edits only)"}',
              f'- CLI: {cli_version(profile) or "unknown"}; model: '
              f'{args.model or next((r["model"] for r in results if r["model"]), "unknown")}',
              f'- Sessions: {len(results)} of {sessions}; reported spend ${spent:.2f}']
    lines = summarize(results, selected, arms, header, stopped)
    root.mkdir(parents=True, exist_ok=True)
    (root / 'results.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
    (root / 'summary.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('\n'.join(line for line in lines if line.startswith('|') or line.startswith('**Stopped')))
    print(f'\nWrote {root}')
    return code


if __name__ == '__main__':
    sys.exit(main())
