"""Migration of frozen, actually distributed catalogs (no Git/network needed)."""

import csv
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = Path(__file__).parent / 'fixtures/distributed-skill-catalogs.tsv'


class HistoricalMigrationTests(unittest.TestCase):
    def test_distributed_catalogs(self):
        rows = [row for row in csv.reader(FIXTURE.read_text().splitlines(), delimiter='\t')
                if row and not row[0].startswith('#')]
        for generation in ('french', 'english'):
            snapshot = [row for row in rows if row[0] == generation]
            self.assertEqual(len(snapshot), 43 if generation == 'french' else 42)
            for layout in ('grouped', 'flat', 'prefixed'):
                for flat_target in (False, True):
                    with self.subTest(generation=generation, layout=layout, flat=flat_target):
                        self.migrate(snapshot, layout, flat_target)

    def migrate(self, snapshot, layout, flat_target):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            destination = project / '.opencode/skills'
            originals = {}
            expected = set()
            for _, old_group, old_name, new_group, new_name in snapshot:
                relative = (f'{old_group}/{old_name}' if layout == 'grouped'
                            else f'gouv-fr-{old_name}' if layout == 'prefixed' else old_name)
                path = destination / relative
                path.mkdir(parents=True)
                contents = f'---\nname: {old_name}\n---\nlocal edit: {relative}\n'
                (path / 'SKILL.md').write_text(contents)
                originals[relative] = contents
                if new_name != '-':
                    expected.add(new_name if flat_target else f'{new_group}/{new_name}')
            personal = destination / 'personal-skill/SKILL.md'
            personal.parent.mkdir()
            personal.write_text('personal data')
            command = ['bash', str(ROOT / 'scripts/install-skills.sh'), '--agent', 'opencode',
                       '--scope', 'project', '--project', str(project), '--force']
            if flat_target:
                command.append('--flat')
            denied = subprocess.run(command, text=True, capture_output=True)
            self.assertNotEqual(denied.returncode, 0, denied.stdout + denied.stderr)
            for relative, content in originals.items():
                self.assertEqual((destination / relative / 'SKILL.md').read_text(), content)
            migrated = subprocess.run(command + ['--migrate'], text=True, capture_output=True)
            self.assertEqual(migrated.returncode, 0, migrated.stdout + migrated.stderr)
            active = {str(p.parent.relative_to(destination)) for p in destination.rglob('SKILL.md')}
            self.assertEqual(active, expected | {'personal-skill'})
            self.assertEqual(len(expected), 42)
            backups = list(destination.parent.glob('skills.backup-*'))
            self.assertEqual(len(backups), 1)
            for relative, content in originals.items():
                self.assertEqual((backups[0] / relative / 'SKILL.md').read_text(), content)
            self.assertEqual(personal.read_text(), 'personal data')
            repeated = subprocess.run(command + ['--migrate'], text=True, capture_output=True)
            self.assertEqual(repeated.returncode, 0, repeated.stdout + repeated.stderr)
            self.assertEqual(list(destination.parent.glob('skills.backup-*')), backups)


if __name__ == '__main__':
    unittest.main()
