"""Expose les verifications typographiques de test_render_docx.py a unittest.

Le script `test_render_docx.py` reste utilisable en ligne de commande ; ce
module le branche sur unittest afin que la suite soit reellement executee par
la CI (`unittest discover`), et non seulement disponible a la main.

Usage : `python -m unittest discover -s skills/fr-gov/compliance/fr-gov-render-technical-architecture-docx/tests -v`
"""

import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import test_render_docx as tr  # noqa: E402


class TypographyTests(unittest.TestCase):
    def test_all_typography_checks_pass(self):
        failed = tr.run_checks()
        self.assertEqual(failed, 0, f"{failed} verification(s) typographique(s) en echec")


if __name__ == "__main__":
    unittest.main()
