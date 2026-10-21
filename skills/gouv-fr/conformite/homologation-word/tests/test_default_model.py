"""Tests de non-régression pour le modèle Word par défaut de render_docx.py.

Le modèle `MODELE_DAT.docx` est maintenu dans la skill sœur
`document-homologation` : le chemin par défaut doit pointer dessus et
être un fichier réellement présent, sans quoi `render_docx.py` échoue sur
tout appel sans `--model`.

Usage : `python -m unittest discover -s skills/gouv-fr/conformite/homologation-word/tests -v`
Dépend de python-docx.
"""

import os
import pathlib
import subprocess
import sys
import tempfile
import unittest

SKILL_DIR = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = SKILL_DIR / "render_docx.py"
EXPECTED_MODEL = (
    SKILL_DIR.parent / "document-homologation" / "dat" / "MODELE_DAT.docx"
)


class DefaultModelTests(unittest.TestCase):
    def test_default_model_file_exists(self):
        self.assertTrue(
            EXPECTED_MODEL.is_file(),
            f"modèle par défaut introuvable : {EXPECTED_MODEL}",
        )

    def test_default_model_path_declared_in_script(self):
        source = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("document-homologation", source)
        self.assertNotIn(
            '"dat-generation", "dat"',
            source,
            "le chemin par défaut ne doit plus viser la skill « dat-generation », "
            "qui n'existe pas dans ce dépôt",
        )

    def test_render_without_model_succeeds(self):
        with tempfile.TemporaryDirectory() as directory:
            base = pathlib.Path(directory)
            source = base / "contenu.md"
            source.write_text("# Titre\n\nCorps.\n", encoding="utf-8")
            output = base / "sortie.docx"
            result = subprocess.run(
                [sys.executable, str(SCRIPT),
                 "--input", str(source), "--output", str(output)],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue(output.is_file(), "le .docx n'a pas été produit")


if __name__ == "__main__":
    unittest.main()
