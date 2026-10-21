"""CLI regression tests using local CSS only; no network required."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'verify_dsfr.py'


class VerifyDsfrTests(unittest.TestCase):
    def check_page(self, html, css='.fr-btn{color:blue}.fr-text--lead{font-size:2em}', assets=()):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            (base / 'index.html').write_text(html)
            (base / 'dsfr.css').write_text(css)
            for asset in assets:
                (base / asset).write_text('fixture')
            return subprocess.run(
                [sys.executable, str(SCRIPT), str(base / 'index.html'),
                 '--css', str(base / 'dsfr.css')],
                text=True, capture_output=True, check=False,
            )

    def test_no_dsfr_classes_is_not_a_success(self):
        result = self.check_page('<main>Hello</main>')
        self.assertEqual(result.returncode, 1)
        self.assertIn('non evalue', result.stdout)
        self.assertNotIn('100.0%', result.stdout)

    def test_data_attributes_are_not_classes(self):
        result = self.check_page('<main data-fr-btn="true">Hello</main>')
        self.assertEqual(result.returncode, 1)
        self.assertIn('non evalue', result.stdout)

    def test_known_classes_with_local_asset(self):
        result = self.check_page(
            '<a class="fr-btn" href="page.html?x=1#anchor">Suite</a>',
            assets=('page.html',),
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('Classes reconnues : 100.0%', result.stdout)
        self.assertIn('ni audit RGAA', result.stdout)

    def test_unknown_class_is_a_failure(self):
        result = self.check_page('<button class="fr-btn--invented">OK</button>')
        self.assertEqual(result.returncode, 1)
        self.assertIn('INCONNU  fr-btn--invented', result.stdout)

    def test_missing_local_asset_is_a_failure(self):
        result = self.check_page('<a class="fr-btn" href="missing.html">Suite</a>')
        self.assertEqual(result.returncode, 1)
        self.assertIn('ASSET MANQUANT  missing.html', result.stdout)

    def test_remote_assets_are_explicitly_out_of_scope(self):
        result = self.check_page('<a class="fr-btn" href="https://example.invalid/">Suite</a>')
        self.assertEqual(result.returncode, 0)
        self.assertIn('ni verification des URLs distantes', result.stdout)

    def test_non_http_schemes_are_not_missing_assets(self):
        # tel:, mailto: et les URL protocol-relative ne sont pas des assets locaux :
        # les traiter comme manquants produit un faux positif.
        result = self.check_page(
            '<a class="fr-btn" href="tel:+33123456789">Appeler</a>'
            '<a class="fr-btn" href="mailto:contact@example.invalid">Ecrire</a>'
            '<a class="fr-btn" href="//cdn.example.invalid/x.css">CDN</a>'
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn('ASSET MANQUANT', result.stdout)
        self.assertIn('Classes reconnues : 100.0%', result.stdout)

    def test_missing_input_returns_usage_error(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(Path(directory) / 'missing.html')],
                text=True, capture_output=True, check=False,
            )
        self.assertEqual(result.returncode, 2)
        self.assertIn('introuvable', result.stderr)


if __name__ == '__main__':
    unittest.main()
