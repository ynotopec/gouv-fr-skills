#!/usr/bin/env python3
"""Check active skill identities, routing, local links and migration targets."""

import csv
import re
from pathlib import Path


def check(root):
    errors = []
    skills = sorted((root / 'skills/gouv-fr').glob('*/*/SKILL.md'))
    names = {path.parent.name for path in skills}
    canonical = {str(path.parent.relative_to(root / 'skills/gouv-fr')) for path in skills}
    if len(names) != len(skills):
        errors.append('Duplicate skill names: flat installation would collide')
    for path in skills:
        source = path.read_text()
        frontmatter = source.split('---', 2)[1]
        name = re.search(r'^name: (.+)$', frontmatter, re.M)
        if not name or name[1] != path.parent.name:
            errors.append(f'{path}: name differs from folder')
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', path.parent.name):
            errors.append(f'{path}: invalid name')
        if path.parent.name == path.parent.parent.name:
            errors.append(f'{path}: name duplicates parent group')
        related = re.search(r'related_skills: \[([^\]]*)\]', frontmatter)
        if related:
            for target in related[1].split(','):
                if target.strip() not in names:
                    errors.append(f'{path}: unknown related skill {target.strip()}')

    catalog = (root / 'SKILLS.md').read_text()
    entries = re.findall(r'^\| \[`([^`]+)`\]\(([^)]+)\)', catalog, re.M)
    expected = {(path.parent.name, str(path.relative_to(root))) for path in skills}
    if len(entries) != len(expected) or set(entries) != expected:
        errors.append('SKILLS.md must list every skill once, at its current path')
    group = None
    for line in catalog.splitlines():
        heading = re.match(r'^## .*\(`([^`]+)`\)', line)
        if heading:
            group = heading[1]
        entry = re.match(r'^\| \[`[^`]+`\]\(skills/gouv-fr/([^/]+)/', line)
        if entry and entry[1] != group:
            errors.append(f'SKILLS.md: entry in wrong section: {line}')

    for path in [root / 'SKILLS.md', root / 'README.md', *skills]:
        for target in re.findall(r'\[[^\]]*\]\(([^)\s]+)\)', path.read_text()):
            target = target.split('#')[0]
            if not target or re.match(r'[a-z]+:|/', target):
                continue
            if not (path.parent / target).exists():
                errors.append(f'{path}: missing local link {target}')

    aliases, targets = set(), set()
    with (root / 'scripts/skill-renames.tsv').open() as stream:
        for row in csv.reader(stream, delimiter='\t'):
            if not row or row[0].startswith('#'):
                continue
            if len(row) != 4:
                errors.append(f'Invalid migration row: {row}')
                continue
            old_group, old_name, new_group, new_name = row
            alias, target = f'{old_group}/{old_name}', f'{new_group}/{new_name}'
            if alias in aliases:
                errors.append(f'Duplicate migration alias: {alias}')
            aliases.add(alias)
            targets.add(target)
            if target not in canonical:
                errors.append(f'Missing migration destination: {target}')
    if targets != canonical:
        errors.append('Migration table does not cover every current skill')
    return skills, errors


if __name__ == '__main__':
    skills, errors = check(Path(__file__).resolve().parent.parent)
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'OK: {len(skills)} skills; names, groups, routing, links and migrations')
