"""Vérifie les inputs et permissions effectives des appels fabnum-cicd.

Usage : python3 verif-appels.py <clone-fabnum-au-tag> <workflow.yml> [...]
Lecture/parsing uniquement. Permissions dépôt implicites : non démontrées,
considérées absentes ; déclarer explicitement les permissions requises.
"""
import argparse
from pathlib import Path
import re

import yaml

RANK = {"none": 0, "read": 1, "write": 2}
SCOPES = {
    "actions", "artifact-metadata", "attestations", "checks", "contents",
    "deployments", "discussions", "id-token", "issues", "models", "packages",
    "pages", "pull-requests", "security-events", "statuses",
}


def permissions(value):
    if value in ("read-all", "write-all"):
        level = value.split('-')[0]
        return {p: ("none" if p == "id-token" and level == "read" else level) for p in SCOPES}
    if not isinstance(value, dict) or any(level not in RANK for level in value.values()):
        raise ValueError('permissions doit être une table ou read-all/write-all')
    return value


def effective(workflow, job):
    # Une table de job remplace intégralement celle du workflow, même vide.
    return permissions(job['permissions'] if 'permissions' in job else workflow.get('permissions', {}))


def check(fab, workflows):
    ok = True
    for wf in workflows:
        y = yaml.safe_load(Path(wf).read_text())
        for job, jd in y['jobs'].items():
            match = re.fullmatch(r'dnum-mi/fabnum-cicd/\.github/workflows/([^/]+\.ya?ml)@(.+)', jd.get('uses', ''))
            if not match:
                continue
            target = fab / '.github/workflows' / match[1]
            if not target.is_file():
                print(f'✗ {wf}:{job} fichier absent {match[1]}')
                ok = False
                continue
            called = yaml.safe_load(target.read_text())
            trigger = called.get('on', called.get(True, {}))
            contract = trigger['workflow_call'] or {}
            inputs, given = contract.get('inputs') or {}, jd.get('with') or {}
            for key in given:
                if key not in inputs:
                    print(f'✗ {wf}:{job} input inconnu {key}')
                    ok = False
            for key, value in inputs.items():
                if value.get('required') and key not in given:
                    print(f'✗ {wf}:{job} input requis manquant {key}')
                    ok = False
            need = {}
            for child in called['jobs'].values():
                for scope, level in effective(called, child).items():
                    if RANK[level] > RANK.get(need.get(scope), 0):
                        need[scope] = level
            have = effective(y, jd)
            for scope, level in need.items():
                if RANK.get(have.get(scope), 0) < RANK[level]:
                    print(f'✗ {wf}:{job} permission {scope}:{level} manquante (a {have.get(scope)})')
                    ok = False
            extra = sorted(p for p, level in have.items() if RANK[level] > RANK.get(need.get(p), 0))
            if extra:
                print(f'⚠ {wf}:{job} permissions en trop {extra}')
    print('OK' if ok else 'ÉCARTS')
    return 0 if ok else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('clone', type=Path)
    parser.add_argument('workflows', nargs='+')
    args = parser.parse_args()
    try:
        return check(args.clone, args.workflows)
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError) as exc:
        print(f'ÉCARTS : fichier ou contrat invalide ({type(exc).__name__})')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
