"""Regression tests for truthful evaluation results and process exit codes."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'eval'))
import audit_skills as audit
import integration_tests as integration
import report


class Evaluation(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.skill = self.root / 'skills/fr-gov/devops/fr-gov-create-helm-chart'
        self.skill.mkdir(parents=True)
        self.source = self.skill / 'SKILL.md'
        self.source.write_text('---\nname: fr-gov-create-helm-chart\ndescription: Helm chart\n---\n## Quand utiliser\nCréer un chart.\n')
        (self.root / 'SKILLS.md').write_text('## Devops (`devops`)\n| [`fr-gov-create-helm-chart`](skills/fr-gov/devops/fr-gov-create-helm-chart/SKILL.md) |\n')
        (self.root / 'README.md').write_text('# Example\n')
        (self.root / 'scripts').mkdir()
        (self.root / 'scripts/skill-renames.tsv').write_text('devops\told-chart\tdevops\tfr-gov-create-helm-chart\n')
        (self.root / 'scripts/skill-retirements.tsv').write_text('')
        self.output = self.root / 'reports'

    def test_valid_catalogue(self):
        self.assertEqual(report.exit_code(audit.evaluate(self.root)), 0)

    def test_invalid_yaml_is_reported(self):
        for fm in ('- list', 'null', 'name: [unterminated', '42'):
            with self.subTest(frontmatter=fm):
                self.source.write_text('---\n' + fm + '\n---\nBody\n')
                rows = audit.evaluate(self.root)
                self.assertEqual(rows[0]['status'], 'fail')
                report.write_report(rows, self.output, 'audit')
                self.assertEqual(report.exit_code(rows), 1)

    def test_missing_skill_still_generates_report(self):
        self.source.unlink()
        self.assertEqual(audit.main(['--root', str(self.root), '--output-dir', str(self.output)]), 1)
        self.assertTrue((self.output / 'audit.html').is_file())
        self.assertEqual(integration.evaluate(self.root)[0]['status'], 'fail')

    def test_secret_is_failure_and_not_echoed(self):
        self.source.write_text(self.source.read_text() + 'password = abcdefghijklmnop\n')
        rows = audit.evaluate(self.root)
        self.assertEqual(rows[0]['status'], 'fail')
        self.assertNotIn('abcdefghijklmnop', json.dumps(rows))

    def test_empty_skills_cannot_pass(self):
        self.source.write_text('')
        self.assertEqual(audit.evaluate(self.root)[0]['status'], 'fail')
        self.assertEqual(integration.evaluate(self.root)[0]['status'], 'fail')

    def test_no_skills_is_failure(self):
        empty = self.root / 'empty'
        empty.mkdir()
        self.assertEqual(report.exit_code(audit.evaluate(empty)), 1)
        self.assertEqual(report.exit_code(integration.evaluate(empty)), 1)

    def test_unregistered_behavior_is_skipped(self):
        renamed = self.skill.with_name('another-skill')
        self.skill.rename(renamed)
        (renamed / 'SKILL.md').write_text('---\nname: another-skill\ndescription: Example\n---\n## Quand utiliser\nExample\n')
        self.assertEqual(integration.evaluate(self.root)[0]['status'], 'skip')

    def make_suite(self):
        tests = self.skill / 'tests'
        tests.mkdir()
        (tests / 'test_behavior.py').write_text(
            'import unittest\nfrom pathlib import Path\n'
            'class Behavior(unittest.TestCase):\n'
            ' def test_real_output(self):\n'
            '  implementation = Path(__file__).resolve().parent.parent / "implementation.py"\n'
            '  scope = {}\n'
            '  exec(implementation.read_text(), scope)\n'
            '  self.assertEqual(scope["result"], 42)\n')
        implementation = self.skill / 'implementation.py'
        implementation.write_text('result = 42\n')
        return implementation

    def test_implementation_mutation_changes_result(self):
        implementation = self.make_suite()
        self.assertEqual(integration.evaluate(self.root)[0]['status'], 'pass')
        implementation.write_text('result = 0\n')
        self.assertEqual(integration.evaluate(self.root)[0]['status'], 'fail')

    def test_missing_suite_is_error(self):
        rows = integration.evaluate(self.root)
        self.assertEqual(rows[0]['status'], 'error')
        self.assertEqual(report.exit_code(rows), 1)

    def test_zero_discovered_tests_is_error(self):
        tests = self.skill / 'tests'
        tests.mkdir()
        (tests / 'test_empty.py').write_text('# no tests\n')
        self.assertEqual(integration.evaluate(self.root)[0]['status'], 'error')

    def test_skipped_tests_are_not_pass(self):
        tests = self.skill / 'tests'
        tests.mkdir()
        (tests / 'test_skipped.py').write_text(
            'import unittest\n@unittest.skip("unavailable")\n'
            'class Example(unittest.TestCase):\n def test_example(self): pass\n')
        self.assertEqual(integration.evaluate(self.root)[0]['status'], 'skip')

    def test_timeout_and_launch_error_are_nonzero(self):
        self.make_suite()
        for error in (subprocess.TimeoutExpired('test', 1), OSError('cannot launch')):
            with self.subTest(error=error), mock.patch.object(integration.subprocess, 'run', side_effect=error):
                rows = integration.evaluate(self.root)
                self.assertEqual(rows[0]['status'], 'error')
                self.assertEqual(report.exit_code(rows), 1)

    def test_html_escapes_untrusted_details(self):
        report.write_report([{'skill': '<script>', 'status': 'error', 'detail': '<img onerror="x">'}], self.output, 'test')
        source = (self.output / 'test.html').read_text()
        self.assertNotIn('<script>', source)
        self.assertIn('&lt;img', source)

    def test_cli_exit_codes(self):
        for script in ('audit_skills.py', 'integration_tests.py'):
            with self.subTest(script=script):
                if script == 'audit_skills.py':
                    self.source.write_text('invalid')
                else:
                    self.set_valid_source()
                result = subprocess.run(
                    [sys.executable, str(ROOT / 'eval' / script), '--root', str(self.root),
                     '--output-dir', str(self.output)], capture_output=True, text=True, check=False)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                stem = 'audit' if script == 'audit_skills.py' else 'integration'
                self.assertTrue((self.output / (stem + '.json')).is_file())
                self.assertNotIn('Traceback', result.stderr)

    def set_valid_source(self):
        self.source.write_text('---\nname: fr-gov-create-helm-chart\ndescription: Helm chart\n---\n## Quand utiliser\nCréer un chart.\n')


if __name__ == '__main__':
    unittest.main()
