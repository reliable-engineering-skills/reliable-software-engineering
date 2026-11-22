"""End-to-end test of run_evals.py with a fake agent; no model is called."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent

# The fake agent applies the case's reference solution, or does nothing when RSE_FAKE_IDLE is set.
FAKE_AGENT = '''
import os, sys
sys.path.insert(0, {evals!r})
import cases, harness
case = next(c for c in cases.CASES if c["id"] == os.environ["RSE_EVAL_CASE"])
if not os.environ.get("RSE_FAKE_IDLE"):
    harness.materialize({{"files": case["reference"].get("files", {{}})}}, ".")
    print(case["reference"].get("output", ""))
'''


class RunnerTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.agent = self.root / 'fake_agent.py'
        self.agent.write_text(FAKE_AGENT.format(evals=str(HERE)), encoding='utf-8')

    def run_suite(self, idle):
        argv = json.dumps([sys.executable, str(self.agent), '{prompt}'])
        env = dict(__import__('os').environ, RSE_FAKE_IDLE='1' if idle else '')
        proc = subprocess.run([sys.executable, '-B', str(HERE / 'run_evals.py'), '--agent', argv,
                               '--configs', 'with', '--out', str(self.root / 'results')],
                              capture_output=True, text=True, timeout=600, env=env)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        result_dir = next((self.root / 'results').iterdir())
        return json.loads((result_dir / 'results.json').read_text(encoding='utf-8')), result_dir

    def test_reference_agent_passes_every_case_and_writes_reports(self):
        results, result_dir = self.run_suite(idle=False)
        failed = [(r['case'], [c for c in r['checks'] if not c['passed']]) for r in results if not r['passed']]
        self.assertEqual(failed, [])
        self.assertTrue((result_dir / 'summary.md').is_file())
        diff = (result_dir / 'core-small-change-stays-small' / 'with-1' / 'diff.patch').read_text(encoding='utf-8')
        self.assertIn('+  <button type="submit">Send</button>', diff)
        self.assertNotIn('.claude/skills', diff, 'installed skills leaked into the graded diff')

    def test_idle_agent_fails_every_case(self):
        results, _ = self.run_suite(idle=True)
        self.assertEqual([r['case'] for r in results if r['passed']], [])


if __name__ == '__main__':
    unittest.main()
