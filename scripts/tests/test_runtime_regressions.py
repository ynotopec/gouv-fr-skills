"""Scénarios hors réseau : sauvegarde, génération isolée et nommage."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCAFFOLDS = ROOT / 'skills/fr-gov/code/fr-gov-scaffold-backend-api/scripts'

# Les doubles simulent uniquement les gestionnaires de paquets, pas les scripts
# testés. Les builds/HTTP des projets générés sont contrôlés dans un job CI dédié.
PACKAGE_TOOL = '''#!/usr/bin/env python3
import json, pathlib, sys
arguments = [a for a in sys.argv[1:] if a != '--yes']
cmd, *args = arguments
if cmd == 'init':
    if pathlib.Path(sys.argv[0]).name == 'uv':
        pathlib.Path(args[0]).mkdir()
        pathlib.Path(args[0], 'pyproject.toml').write_text('[project]\\nname="demo"\\nversion="0.1.0"\\n')
    else:
        pathlib.Path('package.json').write_text('{"name":"demo","version":"0.1.0"}')
elif cmd == 'add' and pathlib.Path('package.json').exists():
    path = pathlib.Path('package.json')
    pkg = json.loads(path.read_text())
    field = 'devDependencies' if '-D' in args else 'dependencies'
    pkg.setdefault(field, {}).update({a.rsplit('@',1)[0] if '@' in a[1:] else a:'*' for a in args if not a.startswith('-')})
    path.write_text(json.dumps(pkg))
elif cmd == '@nestjs/cli':
    project = pathlib.Path(args[1]); project.mkdir()
    (project/'package.json').write_text('{"name":"demo"}')
    (project/'tsconfig.json').write_text('{"compilerOptions":{"experimentalDecorators":true}}')
    (project/'eslint.config.mjs').write_text('// default Nest config')
'''


class Scaffolds(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name)
        tools = self.path / 'bin'
        tools.mkdir()
        for name in ('pnpm', 'uv', 'npx'):
            path = tools / name
            path.write_text(PACKAGE_TOOL)
            path.chmod(0o755)
        self.env = {**os.environ, 'PATH': str(tools) + os.pathsep + os.environ['PATH']}

    def generate(self, framework, target='new-api'):
        return subprocess.run(['bash', str(SCAFFOLDS / f'scaffold-{framework}.sh'), target],
                              cwd=self.path, env=self.env, capture_output=True, text=True)

    def test_fastapi_completes_in_requested_directory(self):
        result = self.generate('fastapi')
        self.assertEqual(result.returncode, 0, result.stderr)
        for name in ('app/main.py', 'tests/__init__.py', 'tests/test_cats.py', 'pyproject.toml'):
            self.assertTrue((self.path / 'new-api' / name).is_file(), name)
        self.assertFalse((self.path / 'app').exists())

    def test_fastify_completes_and_declares_production_dependencies(self):
        result = self.generate('fastify')
        self.assertEqual(result.returncode, 0, result.stderr)
        project = self.path / 'new-api'
        for name in ('src/utils/logger.ts', 'test/routes/cats.test.ts', 'src/app.ts'):
            self.assertTrue((project / name).is_file(), name)
        self.assertFalse((self.path / 'package.json').exists())
        pkg = json.loads((project / 'package.json').read_text())
        self.assertTrue({'@fastify/swagger', '@fastify/swagger-ui', '@sinclair/typebox', 'pino'} <= pkg['dependencies'].keys())
        self.assertIn('vitest', pkg['devDependencies'])

    def test_nestjs_production_dependencies_and_single_lint_config(self):
        result = self.generate('nestjs')
        self.assertEqual(result.returncode, 0, result.stderr)
        project = self.path / 'new-api'
        pkg = json.loads((project / 'package.json').read_text())
        self.assertTrue({'@nestjs/swagger', '@prisma/client'} <= pkg['dependencies'].keys())
        self.assertIn('@antfu/eslint-config', pkg['devDependencies'])
        self.assertEqual([p.name for p in project.glob('eslint.config.*')], ['eslint.config.mjs'])

    def test_existing_destination_is_never_modified(self):
        project = self.path / 'existing'
        project.mkdir()
        (project / 'keep').write_text('local work')
        for framework in ('fastapi', 'fastify', 'nestjs'):
            with self.subTest(framework=framework):
                self.assertNotEqual(self.generate(framework, 'existing').returncode, 0)
                self.assertEqual([p.name for p in project.iterdir()], ['keep'])
                self.assertEqual((project / 'keep').read_text(), 'local work')

    def test_symlink_destination_is_rejected(self):
        target = self.path / 'real'
        target.mkdir()
        (self.path / 'linked').symlink_to(target, target_is_directory=True)
        for framework in ('fastapi', 'fastify', 'nestjs'):
            self.assertNotEqual(self.generate(framework, 'linked').returncode, 0)
        self.assertEqual(list(target.iterdir()), [])


class Backup(unittest.TestCase):
    def test_snapshot_preserves_worktree_index_and_old_stash(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            def git(*args):
                return subprocess.check_output(['git', *args], cwd=path)
            git('init', '-b', 'main')
            git('config', 'user.name', 'Regression test')
            git('config', 'user.email', 'test@example.invalid')
            (path / 'tracked').write_text('base')
            (path / '.gitignore').write_text('ignored\n')
            git('add', '-A'); git('commit', '-m', 'initial')
            head = git('rev-parse', 'HEAD')
            (path / 'tracked').write_text('old unrelated work')
            git('stash', 'push', '-m', 'old stash')
            stash = git('stash', 'list', '--format=%H')
            # Un dépôt propre ne doit pas restaurer l'ancien stash.
            script = ROOT / '.github/workflows/save-workflow.sh'
            subprocess.run(['bash', str(script), 'clean'], cwd=path, check=True, capture_output=True)
            self.assertEqual(git('status', '--porcelain'), b'')
            self.assertEqual(git('stash', 'list', '--format=%H'), stash)
            (path / 'tracked').write_text('staged')
            git('add', 'tracked')
            (path / 'tracked').write_text('unstaged')
            (path / 'untracked').write_text('new work')
            (path / 'ignored').write_text('excluded')
            before = git('status', '--porcelain'), git('diff', '--cached'), git('diff')
            subprocess.run(['bash', str(script), 'dirty'], cwd=path, check=True, capture_output=True)
            self.assertEqual((git('status', '--porcelain'), git('diff', '--cached'), git('diff')), before)
            self.assertEqual(git('stash', 'list', '--format=%H'), stash)
            self.assertEqual(git('rev-parse', 'HEAD'), head)
            snapshots = git('for-each-ref', '--format=%(refname)', 'refs/heads/backup/').decode().splitlines()
            dirty = [ref for ref in snapshots if git('rev-parse', ref).strip() != head.strip()]
            self.assertEqual(len(dirty), 1)
            self.assertEqual(git('show', dirty[0] + ':tracked'), b'unstaged')
            self.assertEqual(git('show', dirty[0] + ':untracked'), b'new work')
            self.assertNotIn(b'ignored', git('ls-tree', '--name-only', dirty[0]))


class FolderCheck(unittest.TestCase):
    def check(self, files):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            for name in files:
                file = path / name
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_text('')
            return subprocess.run(['bash', str(ROOT / 'skills/fr-gov/code/fr-gov-project-conventions/scripts/check-folders.sh'), '.'],
                                  cwd=path, capture_output=True, text=True)

    def test_generated_and_hidden_trees_are_pruned(self):
        result = self.check(['src/main.ts', 'node_modules/SomeLibrary/Internal_File.js',
                             'dist/Generated_File.js', 'build/Other_File.js', '.cache/Hidden_File.js'])
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_project_violation_is_still_reported(self):
        self.assertNotEqual(self.check(['src/Bad_File.js']).returncode, 0)


if __name__ == '__main__':
    unittest.main()
