"""End-to-end tests of run_evals.py with a fake agent that speaks Claude Code's stream-json; no model is called."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent

# The fake agent applies the case's reference solution (or nothing when RSE_FAKE_IDLE is set) and reports
# like `claude -p --output-format stream-json`: an init event, a Skill tool call in the with-arm, a result.
FAKE_AGENT = '''
import json, os, sys
sys.path.insert(0, {evals!r})
import cases, harness
case = next(c for c in cases.CASES if c["id"] == os.environ["RSE_EVAL_CASE"])
arm = os.environ["RSE_EVAL_ARM"]
emit = lambda event: print(json.dumps(event), flush=True)
emit({{"type": "system", "subtype": "init", "model": "fake-model"}})
skill = case["skill"] if arm == "with" else (case["skill"] if os.environ.get("RSE_FAKE_CONTAMINATE") else None)
if skill:
    emit({{"type": "assistant", "message": {{"content": [
        {{"type": "tool_use", "name": "Skill", "input": {{"skill": skill}}}}]}}}})
text = ""
if not os.environ.get("RSE_FAKE_IDLE"):
    harness.materialize({{"files": case["reference"].get("files", {{}})}}, ".")
    text = case["reference"].get("output", "")
emit({{"type": "result", "subtype": "success", "result": text, "total_cost_usd": 1.0, "num_turns": 3}})
'''


class RunnerTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.agent = self.root / 'fake_agent.py'
        self.agent.write_text(FAKE_AGENT.format(evals=str(HERE)), encoding='utf-8')

    def run_suite(self, *extra, env_extra=None, expect=0):
        argv = json.dumps([sys.executable, str(self.agent), '{prompt}'])
        env = {**os.environ, 'RSE_FAKE_IDLE': '', 'RSE_FAKE_CONTAMINATE': '', **(env_extra or {})}
        proc = subprocess.run([sys.executable, '-B', str(HERE / 'run_evals.py'), '--agent', argv,
                               '--out', str(self.root / 'results'), *extra],
                              capture_output=True, text=True, timeout=900, env=env)
        self.assertEqual(proc.returncode, expect, proc.stdout + proc.stderr)
        dirs = list((self.root / 'results').iterdir()) if (self.root / 'results').exists() else []
        if not dirs:
            return None, None, proc.stdout
        result_dir = dirs[0]
        return json.loads((result_dir / 'results.json').read_text(encoding='utf-8')), result_dir, proc.stdout

    def test_reference_agent_passes_every_case_and_triggers_its_skill(self):
        results, result_dir, _ = self.run_suite('--configs', 'with', '--confirm', '--max-cost-usd', '1000')
        failed = [(r['case'], [c for c in r['checks'] if not c['passed']]) for r in results if not r['passed']]
        self.assertEqual(failed, [])
        self.assertTrue(all(r['triggered'] for r in results))
        self.assertTrue(all(r['cost_usd'] == 1.0 and r['model'] == 'fake-model' for r in results))
        summary = (result_dir / 'summary.md').read_text(encoding='utf-8')
        self.assertIn('mean USD/session', summary)
        diff = (result_dir / 'core-small-change-stays-small' / 'with-1' / 'diff.patch').read_text(encoding='utf-8')
        self.assertIn('+  <button type="submit">Send</button>', diff)
        self.assertNotIn('.claude/skills', diff, 'installed skills leaked into the graded diff')

    def test_idle_agent_fails_every_case(self):
        results, _, _ = self.run_suite('--configs', 'without', '--confirm', '--max-cost-usd', '1000',
                                       env_extra={'RSE_FAKE_IDLE': '1'})
        self.assertEqual([r['case'] for r in results if r['passed']], [])

    def test_contaminated_no_skill_arm_stops_the_run(self):
        results, result_dir, out = self.run_suite('--configs', 'without', '--cases', 'core-review-is-read-only',
                                                  env_extra={'RSE_FAKE_CONTAMINATE': '1'}, expect=3)
        self.assertEqual(results, [])
        self.assertIn('CONTAMINATED', (result_dir / 'summary.md').read_text(encoding='utf-8'))

    def test_more_than_one_session_needs_confirm(self):
        results, _, out = self.run_suite('--cases', 'core-review-is-read-only', expect=2)
        self.assertIsNone(results)
        self.assertIn('without --confirm', out)

    def test_spend_cap_stops_new_sessions(self):
        results, result_dir, _ = self.run_suite('--configs', 'with', '--confirm', '--max-cost-usd', '2.5')
        self.assertEqual(len(results), 3)  # $1 each: the cap is checked before every new session
        self.assertIn('spend cap', (result_dir / 'summary.md').read_text(encoding='utf-8'))

    def test_check_reports_missing_profile_without_calling_a_model(self):
        missing = self.root / 'no-such-profile'
        proc = subprocess.run([sys.executable, '-B', str(HERE / 'run_evals.py'), '--check',
                               '--isolation', 'profile', '--profile-dir', str(missing)],
                              capture_output=True, text=True, timeout=60)
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn('NOT READY', proc.stdout)
        self.assertIn('CLAUDE_CONFIG_DIR', proc.stdout)


if __name__ == '__main__':
    unittest.main()
