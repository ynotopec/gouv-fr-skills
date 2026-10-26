"""Sondes des conteneurs applicatifs, init ordinaires et sidecars."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('cpin', Path(__file__).resolve().parents[1] / 'scripts/check-cpin-rules.py')
cpin = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cpin)


def container(name, **extra):
    return {'name': name, 'image': 'docker.io/library/busybox:1.37',
            'resources': {'limits': {'cpu': '100m', 'memory': '32Mi'},
                          'requests': {'cpu': '100m', 'memory': '32Mi'}}, **extra}


def deployment(init):
    return {'kind': 'Deployment', 'metadata': {'name': 'demo'}, 'spec': {'template': {
        'metadata': {'labels': {'app': 'demo', 'env': 'test', 'tier': 'api'}},
        'spec': {'containers': [container('app', readinessProbe={'exec': {'command': ['true']}})],
                 'initContainers': [init]}}}}


class ProbeRules(unittest.TestCase):
    def test_regular_init_container_does_not_need_probe(self):
        errors, _ = cpin.check_pod(deployment(container('prepare')))
        self.assertEqual(errors, [])

    def test_native_sidecar_still_needs_probe(self):
        errors, _ = cpin.check_pod(deployment(container('sidecar', restartPolicy='Always')))
        self.assertTrue(any('aucune probe' in e for e in errors))

    def test_app_still_needs_probe(self):
        doc = deployment(container('prepare'))
        doc['spec']['template']['spec']['containers'] = [container('app')]
        errors, _ = cpin.check_pod(doc)
        self.assertTrue(any('/app: aucune probe' in e for e in errors))


if __name__ == '__main__':
    unittest.main()
