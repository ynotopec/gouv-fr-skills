#!/usr/bin/env python3
"""Run existing behavioral suites against real skill implementations, offline."""

import argparse
import re
import subprocess
import sys
from pathlib import Path

from audit_skills import ROOT, discover, skill_errors
from report import exit_code, write_report

# Other skills are explicitly SKIP: documentation alone is not a behavioral test.
UNITTEST_SKILLS = {
    'fr-gov-render-technical-architecture-docx',
    'fr-gov-set-up-design-system',
    'fr-gov-set-up-cloud-pi-native-cicd',
    'fr-gov-create-helm-chart',
    'smoke-test-api',
}
SHELL_SUITES = {
    'fr-gov-find-cybersecurity-guide': 'scripts/test-generate-catalogue.sh',
}


def run_skill(path, root, timeout):
    row = {'skill': path.name, 'status': 'skip', 'detail': 'Aucune suite comportementale automatisée enregistrée'}
    errors = skill_errors(path / 'SKILL.md')
    if errors:
        return dict(row, status='fail', detail='\n'.join(errors))
    unit = path.name in UNITTEST_SKILLS
    if unit:
        tests = path / 'tests'
        if not list(tests.glob('test_*.py')):
            return dict(row, status='error', detail='Suite unittest enregistrée mais absente ou vide')
        command = [sys.executable, '-m', 'unittest', 'discover', '-s', str(tests), '-v']
    elif path.name in SHELL_SUITES:
        script = path / SHELL_SUITES[path.name]
        if not script.is_file():
            return dict(row, status='error', detail='Suite shell enregistrée mais absente')
        # Check required tools (jq is needed by ANSSI guide scripts)
        try:
            subprocess.run(['jq', '--version'], capture_output=True, check=True, timeout=10)
        except (OSError, subprocess.TimeoutExpired):
            return dict(row, status='skip', detail='Suite shell requiert jq (absent)')
        except subprocess.CalledProcessError as exc:
            return dict(row, status='error', detail=f'jq --version a échoué (code {exc.returncode})')
        command = ['sh', str(script)]
    else:
        return row
    try:
        completed = subprocess.run(command, cwd=root, capture_output=True, text=True,
                                   encoding='utf-8', errors='replace', timeout=timeout, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return dict(row, status='error', detail=f'{type(exc).__name__}: {exc}')
    output = completed.stdout + completed.stderr
    # Discovery must execute tests; zero-test exit codes differ by Python version.
    counts = re.findall(r'Ran (\d+) tests? in ', output) if unit else []
    if unit and (not counts or int(counts[-1]) == 0):
        status = 'error'
        output = 'Aucun test unittest exécuté\n' + output
    elif completed.returncode:
        status = 'fail'
    elif unit and re.search(r'\bskipped=\d+', output):
        status = 'skip'
        output = 'Suite incomplète: tests ignorés\n' + output
    else:
        status = 'pass'
    return dict(row, status=status, detail=f'Commande: {" ".join(command)}\nCode: {completed.returncode}\n{output}')


def evaluate(root, timeout=120):
    paths = discover(root)
    if not paths:
        return [{'skill': 'catalogue', 'status': 'fail', 'detail': 'Aucun skill découvert'}]
    return [run_skill(path, root, timeout) for path in paths]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'eval/generated')
    parser.add_argument('--timeout', type=float, default=120, help='Seconds par suite')
    args = parser.parse_args(argv)
    if args.timeout <= 0:
        parser.error('--timeout doit être positif')
    results = evaluate(args.root.resolve(), args.timeout)
    write_report(results, args.output_dir, 'integration')
    return exit_code(results)


if __name__ == '__main__':
    raise SystemExit(main())
