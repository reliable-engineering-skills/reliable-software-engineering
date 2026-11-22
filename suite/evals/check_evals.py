#!/usr/bin/env python3
"""Validate the eval suite itself, offline and without any agent.

For every case: the schema is valid, an agent that does nothing FAILS, and the reference result PASSES.
This proves each case discriminates and is satisfiable. It does not measure any agent.
"""
import sys
import tempfile
from pathlib import Path

if sys.version_info < (3, 9):
    sys.exit('Python 3.9 or newer is required')

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cases as suite  # noqa: E402
import harness  # noqa: E402

SKILLS = harness.find_skills_dir(HERE)
CASE_KEYS = {'id', 'skill', 'rules', 'prompt', 'files', 'expect', 'rubric', 'reference'}


def validate_schema(errors):
    ids, rules_seen, skills_seen = set(), set(), set()
    installed = {p.name for p in SKILLS.iterdir() if (p / 'SKILL.md').is_file()}
    for case in suite.CASES:
        cid = case.get('id', '?')
        if set(case) != CASE_KEYS:
            errors.append(f'{cid}: fields must be exactly {sorted(CASE_KEYS)}')
            continue
        if cid in ids:
            errors.append(f'{cid}: duplicate id')
        ids.add(cid)
        if case['skill'] not in installed:
            errors.append(f'{cid}: unknown skill {case["skill"]}')
        skills_seen.add(case['skill'])
        unknown_rules = set(case['rules']) - set(suite.RULES)
        if not case['rules'] or unknown_rules:
            errors.append(f'{cid}: rules must be a nonempty subset of R1-R7')
        rules_seen.update(case['rules'])
        unknown_checks = set(case['expect']) - harness.CHECK_KEYS
        if not case['expect'] or unknown_checks:
            errors.append(f'{cid}: unknown expectation keys {sorted(unknown_checks)}')
        if not case['rubric'] or not case['files'] or not case['prompt'].strip():
            errors.append(f'{cid}: prompt, files and rubric are required')
    for rule in sorted(set(suite.RULES) - rules_seen):
        errors.append(f'rule {rule} ({suite.RULES[rule]}) has no case')
    for skill in sorted(installed - skills_seen):
        errors.append(f'skill {skill} has no case')


def run(case, apply_reference):
    context = harness.default_context(SKILLS)
    with tempfile.TemporaryDirectory() as tmp:
        harness.materialize(case, tmp)
        before = harness.snapshot(tmp)
        output = ''
        if apply_reference:
            ref = case['reference']
            harness.materialize({'files': ref.get('files', {})}, tmp)
            output = ref.get('output', '')
        return harness.evaluate(case, tmp, output, before, context)


def main():
    errors = []
    validate_schema(errors)
    if not errors:
        for case in suite.CASES:
            idle = run(case, apply_reference=False)
            if all(ok for _, ok, _ in idle):
                errors.append(f'{case["id"]}: an agent that does nothing would pass; the case cannot discriminate')
            reference = run(case, apply_reference=True)
            for name, ok, detail in reference:
                if not ok:
                    errors.append(f'{case["id"]}: reference fails {name}: {detail}')
            status = 'ok' if all(ok for _, ok, _ in reference) else 'BROKEN'
            failing_idle = sum(not ok for _, ok, _ in idle)
            print(f'{status:6} {case["id"]:45} checks={len(reference):2} idle-failures={failing_idle}')
    if errors:
        print('\n'.join(['', f'{len(errors)} problem(s):'] + errors))
        return 1
    print(f'\n{len(suite.CASES)} cases valid; rules covered: {", ".join(sorted(suite.RULES))}.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
