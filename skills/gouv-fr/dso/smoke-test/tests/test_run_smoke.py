"""Tests avec credentials synthétiques et transport simulé, sans appel réseau."""

import base64
import contextlib
import hashlib
import hmac
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from urllib.error import HTTPError
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'run_smoke.py'
spec = importlib.util.spec_from_file_location('run_smoke', SCRIPT)
smoke = importlib.util.module_from_spec(spec)
spec.loader.exec_module(smoke)


class Response:
    def __init__(self, status, body, media='application/json'):
        self.status = status
        self.headers = {'Content-Type': media}
        self.body = io.BytesIO(json.dumps(body).encode())

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.body.close()

    def read(self, size):
        return self.body.read(size)


class Opener:
    def __init__(self, responses):
        self.responses = list(responses)
        self.requests = []

    def open(self, req, timeout):
        self.requests.append(req)
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response


def replies():
    return [Response(200, [{'id': 'fixture'}]), Response(200, None, 'audio/webm'),
            Response(202, {'job_id': 'synthetic-job'})]


class SmokeTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.audio = Path(self.directory.name) / 'fixture.m4a'
        self.audio.write_bytes(b'synthetic multipart fixture')

    def run_smoke(self, opener, environ, **kwargs):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            smoke.run('https://example.invalid', 'fixture', self.audio, environ,
                      opener=opener, **kwargs)
        return stdout.getvalue()

    def test_signature_matches_historical_token_format(self):
        key = 'synthetic-key'
        with patch.object(smoke.time, 'time', return_value=100):
            token = smoke.get_token({'INTERNAL_API_TOKEN': key})
        body, signature = token.split('.')
        expected = hmac.new(key.encode(), body.encode(), hashlib.sha256).hexdigest()
        self.assertEqual(signature, expected)
        claims = json.loads(base64.urlsafe_b64decode(body + '=' * (-len(body) % 4)))
        self.assertEqual(claims['retention_until'], 3700)
        self.assertEqual(claims['qr_token'], 'smoke-test')
        self.assertTrue(claims['device_id'].startswith('smoke-'))

    def test_injected_token_takes_precedence(self):
        self.assertEqual(smoke.get_token({'SMOKE_TOKEN': 'synthetic-token',
                                        'INTERNAL_API_TOKEN': 'unused'}), 'synthetic-token')

    def test_pipeline_keeps_credentials_and_response_bodies_out_of_output(self):
        opener = Opener(replies())
        output = self.run_smoke(opener, {'SMOKE_TOKEN': 'synthetic-token'})
        self.assertEqual(len(opener.requests), 3)
        for req in opener.requests:
            self.assertEqual(req.get_header('Authorization'), 'Bearer synthetic-token')
        self.assertNotIn('synthetic-token', output)
        self.assertNotIn('synthetic-job', output)
        self.assertNotIn('fixture', output)
        self.assertIn('HTTP 202', output)
        self.assertIn(b'filename="smoke.m4a"', opener.requests[2].data)
        self.assertIn(self.audio.read_bytes(), opener.requests[2].data)

    def test_missing_credential_does_not_send_a_request(self):
        opener = Opener([])
        with self.assertRaises(smoke.SmokeError):
            self.run_smoke(opener, {})
        self.assertEqual(opener.requests, [])

    def test_empty_list_does_not_post_a_job(self):
        opener = Opener([Response(200, [])])
        with self.assertRaisesRegex(smoke.SmokeError, 'non évalués'):
            self.run_smoke(opener, {'SMOKE_TOKEN': 'synthetic'})
        self.assertEqual(len(opener.requests), 1)

    def test_unsafe_base_is_rejected(self):
        for base in ['http://example.invalid', 'https://user:pass@example.invalid',
                     'https://example.invalid/path', 'https://example.invalid?token=x']:
            with self.subTest(base=base), self.assertRaises(smoke.SmokeError):
                smoke.validate_base(base)

    def test_redirect_policy_refuses_forwarding(self):
        self.assertIsNone(smoke.NoRedirect().redirect_request(
            None, None, 302, '', {}, 'https://other.invalid'))

    def test_http_error_does_not_echo_server_data_or_credential(self):
        secret = 'synthetic-secret'
        failure = HTTPError('https://example.invalid/' + secret, 403, secret,
                            {'Authorization': secret}, io.BytesIO(secret.encode()))
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch.dict(smoke.os.environ, {'SMOKE_TOKEN': secret}, clear=True), \
                patch.object(smoke.request, 'build_opener', return_value=Opener([failure])), \
                contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            result = smoke.main(['--base', 'https://example.invalid', '--item-id', 'fixture',
                                 '--audio-file', str(self.audio)])
        self.assertEqual(result, 1)
        self.assertIn('403', stderr.getvalue())
        self.assertNotIn(secret, stdout.getvalue() + stderr.getvalue())

    def test_job_without_identifier_fails(self):
        responses = replies()
        responses[2] = Response(202, {})
        with self.assertRaisesRegex(smoke.SmokeError, 'job absent'):
            self.run_smoke(Opener(responses), {'SMOKE_TOKEN': 'synthetic'})

    def test_api_contract_is_configurable(self):
        """Les chemins et types de média sont fournis par l'appelant, pas figés."""
        opener = Opener([Response(200, [{'id': 'x'}]), Response(200, None, 'application/json'),
                          Response(202, {'task_id': 'synthetic-task'})])
        self.run_smoke(opener, {'SMOKE_TOKEN': 'synthetic'},
                       list_path='/api/records', item_path='/api/records/one',
                       job_path='/api/records/one/process', id_param='record_id',
                       media_type='application/json', job_field='task_id')
        urls = [req.full_url for req in opener.requests]
        self.assertEqual(urls[0], 'https://example.invalid/api/records')
        self.assertEqual(urls[1], 'https://example.invalid/api/records/one?record_id=fixture')
        self.assertEqual(urls[2], 'https://example.invalid/api/records/one/process')

    def test_media_type_mismatch_is_rejected(self):
        opener = Opener([Response(200, [{'id': 'x'}]), Response(200, None, 'text/html')])
        with self.assertRaisesRegex(smoke.SmokeError, 'Type de média'):
            self.run_smoke(opener, {'SMOKE_TOKEN': 'synthetic'}, media_type='application/json')
        self.assertEqual(len(opener.requests), 2)


if __name__ == '__main__':
    unittest.main()
