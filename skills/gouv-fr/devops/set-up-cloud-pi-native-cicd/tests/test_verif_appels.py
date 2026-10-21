"""Tests de non-régression pour verif-appels.py.

Couvre la comparaison des niveaux de permission GitHub Actions
(`none` < `read` < `write`) : un job appelant qui accorde moins que le job
appelé exige doit être signalé.

Usage : `python -m unittest discover -s skills/gouv-fr/devops/set-up-cloud-pi-native-cicd/tests -v`
Dépend de PyYAML.
"""

import pathlib
import subprocess
import sys
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "verif-appels.py"

CALLED = """
name: called
on:
  workflow_call:
    inputs: {}
jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
"""

CALLER = """
name: caller
on: push
jobs:
  build:
    uses: dnum-mi/fabnum-cicd/.github/workflows/called.yml@v1
    permissions:
      contents: {level}
"""


class VerifAppelsTests(unittest.TestCase):
    def check(self, called, caller):
        with tempfile.TemporaryDirectory() as directory:
            base = pathlib.Path(directory)
            clone = base / "clone"
            (clone / ".github" / "workflows").mkdir(parents=True)
            (clone / ".github" / "workflows" / "called.yml").write_text(called)
            (base / "caller.yml").write_text(caller)
            return subprocess.run(
                [sys.executable, str(SCRIPT), str(clone), str(base / "caller.yml")],
                text=True, capture_output=True, check=False,
            )

    def caller_with(self, level):
        return CALLER.format(level=level)

    def test_missing_permission_is_reported(self):
        # Le job appelé exige `contents: read`, l'appelant n'accorde que `none` :
        # l'écart doit être signalé et le code de retour non nul.
        result = self.check(CALLED, self.caller_with("none"))
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("permission contents:read manquante", result.stdout)

    def test_sufficient_permission_passes(self):
        result = self.check(CALLED, self.caller_with("read"))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("OK", result.stdout)

    def test_write_is_accepted_where_read_is_required(self):
        result = self.check(CALLED, self.caller_with("write"))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("OK", result.stdout)

    def test_write_requirement_is_not_satisfied_by_read(self):
        called = CALLED.replace("contents: read", "contents: write")
        result = self.check(called, self.caller_with("read"))
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("permission contents:write manquante", result.stdout)

    def test_absent_permission_is_treated_as_none(self):
        caller = """
name: caller
on: push
jobs:
  build:
    uses: dnum-mi/fabnum-cicd/.github/workflows/called.yml@v1
"""
        result = self.check(CALLED, caller)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("permission contents:read manquante", result.stdout)


if __name__ == "__main__":
    unittest.main()
