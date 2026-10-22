"""Tests du validateur de catalogue : liste related_skills et propreté du catalogue réel."""

import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'check-skill-catalog.py'
spec = importlib.util.spec_from_file_location('check_skill_catalog', SCRIPT)
catalog = importlib.util.module_from_spec(spec)
spec.loader.exec_module(catalog)

NAMES = {'alpha', 'beta'}
PATH = Path('/tmp/skills/fr-gov/groupe/alpha/SKILL.md')


class RelatedSkills(unittest.TestCase):
    def test_unknown_target(self):
        errors = catalog.check_related(PATH, 'related_skills: [beta, gamma]', NAMES)
        self.assertEqual(len(errors), 1)
        self.assertIn('unknown related skill gamma', errors[0])

    def test_self_reference(self):
        errors = catalog.check_related(PATH, 'related_skills: [alpha, beta]', NAMES)
        self.assertEqual(len(errors), 1)
        self.assertIn('references itself', errors[0])

    def test_duplicate(self):
        errors = catalog.check_related(PATH, 'related_skills: [beta, beta]', NAMES)
        self.assertEqual(len(errors), 1)
        self.assertIn('duplicate related skill beta', errors[0])

    def test_valid_list(self):
        self.assertEqual(catalog.check_related(PATH, 'related_skills: [beta]', NAMES), [])

    def test_missing_list(self):
        self.assertEqual(catalog.check_related(PATH, 'name: alpha', NAMES), [])

    def test_self_and_duplicate_reported_together(self):
        errors = catalog.check_related(PATH, 'related_skills: [beta, beta, alpha]', NAMES)
        self.assertEqual(len(errors), 2)
        self.assertTrue(any('duplicate related skill beta' in e for e in errors))
        self.assertTrue(any('references itself' in e for e in errors))


class RealCatalog(unittest.TestCase):
    def test_catalog_is_clean(self):
        _, errors = catalog.check(Path(__file__).resolve().parents[2])
        self.assertEqual(errors, [])


if __name__ == '__main__':
    unittest.main()
