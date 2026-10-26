#!/usr/bin/env python3
"""Validate the real catalogue and skill sources; no synthetic quality score."""

import argparse
import importlib.util
import re
from pathlib import Path

import yaml

from report import exit_code, write_report

ROOT = Path(__file__).resolve().parent.parent
# Reuse the repository validator rather than maintaining a second catalogue policy.
_spec = importlib.util.spec_from_file_location('skill_catalog', ROOT / 'scripts/check-skill-catalog.py')
catalog = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(catalog)


def skill_errors(path):
    """Return actionable errors, including malformed or absent input."""
    try:
        source = path.read_text(encoding='utf-8')
    except (OSError, UnicodeError) as exc:
        return [f'SKILL.md illisible ou absent: {exc}']
    match = re.match(r'\A---\s*\n(.*?)\n---(?:\s*\n|$)', source, re.S)
    if not match:
        return ['Délimiteurs YAML absents ou invalides']
    try:
        frontmatter = yaml.safe_load(match[1])
    except yaml.YAMLError:
        return ['YAML invalide']
    if not isinstance(frontmatter, dict):
        return ['Le frontmatter YAML doit être un objet']
    errors = []
    if frontmatter.get('name') != path.parent.name:
        errors.append('Le nom doit correspondre au répertoire')
    description = frontmatter.get('description')
    if not isinstance(description, str) or not 1 <= len(description.strip()) <= 60:
        errors.append('La description doit contenir de 1 à 60 caractères')
    if not source[match.end():].strip():
        errors.append('Corps du skill vide')
    # A narrow heuristic, not a credential scanner or security certification.
    # Do not include the matching value in reports.
    if re.search(r'''(?:password|secret|token|api_key)\s*[:=]\s*["']?[A-Za-z0-9]{8,}''', source, re.I):
        errors.append('Valeur de secret potentielle en dur: vérifier ou remplacer par une référence')
    return errors


def discover(root):
    return sorted(path for path in (root / 'skills/fr-gov').glob('*/*') if path.is_dir())


def evaluate(root):
    results = []
    paths = discover(root)
    if not paths:
        results.append({'skill': 'catalogue', 'status': 'fail', 'detail': 'Aucun skill découvert'})
    for path in paths:
        errors = skill_errors(path / 'SKILL.md')
        results.append({'skill': path.name, 'status': 'fail' if errors else 'pass',
                        'detail': '\n'.join(errors) if errors else 'Source YAML, identité, description et corps valides'})
    try:
        _, errors = catalog.check(root)
        results.append({'skill': 'catalogue', 'status': 'fail' if errors else 'pass',
                        'detail': '\n'.join(errors) if errors else 'Noms, routage, liens et migrations valides'})
    except (OSError, UnicodeError, ValueError, TypeError, AttributeError, yaml.YAMLError) as exc:
        results.append({'skill': 'catalogue', 'status': 'error',
                        'detail': f'{type(exc).__name__}: {exc}'})
    return results


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'eval/generated')
    args = parser.parse_args(argv)
    results = evaluate(args.root.resolve())
    write_report(results, args.output_dir, 'audit')
    return exit_code(results)


if __name__ == '__main__':
    raise SystemExit(main())
