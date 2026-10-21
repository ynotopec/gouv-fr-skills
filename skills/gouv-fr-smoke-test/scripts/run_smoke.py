#!/usr/bin/env python3
"""Smoke-test explicite : secrets en mémoire, sorties limitées aux statuts.

Utilise SMOKE_TOKEN ou forge le jeton avec INTERNAL_API_TOKEN depuis
l'environnement du processus. Ne suit aucun redirect et n'affiche ni secret
ni corps de réponse. Bibliothèque standard uniquement.
"""

import argparse
import base64
import hashlib
import hmac
import json
import os
import secrets
import sys
import time
from pathlib import Path
from urllib import error, parse, request

MAX_BYTES = 10 * 1024 * 1024


class SmokeError(Exception):
    """Message fixe ne contenant aucune donnée du service ou credential."""


class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def get_token(environ):
    token = environ.get('SMOKE_TOKEN')
    if token:
        return token
    key = environ.get('INTERNAL_API_TOKEN')
    if not key:
        raise SmokeError('Credential absent : injecter SMOKE_TOKEN ou INTERNAL_API_TOKEN dans le processus.')
    claims = {
        'qr_token': 'smoke-test',
        'device_id': 'smoke-' + secrets.token_hex(8),
        'retention_until': int(time.time()) + 3600,
    }
    body = base64.urlsafe_b64encode(json.dumps(claims).encode()).rstrip(b'=').decode()
    signature = hmac.new(key.encode(), body.encode(), hashlib.sha256).hexdigest()
    return body + '.' + signature


def validate_base(base):
    url = parse.urlsplit(base)
    if (url.scheme != 'https' or not url.hostname or url.username or url.password
            or url.query or url.fragment or url.path not in ('', '/')):
        raise SmokeError('Base invalide : origine HTTPS sans identifiant, chemin, query ou fragment requise.')
    return base.rstrip('/')


def call(opener, base, path, token, expected, *, data=None, content_type=None, json_body=True):
    headers = {'Authorization': 'Bearer ' + token}
    if content_type:
        headers['Content-Type'] = content_type
    req = request.Request(base + path, headers=headers, data=data)
    try:
        with opener.open(req, timeout=30) as response:
            if response.status != expected:
                raise SmokeError('Code HTTP inattendu.')
            if not json_body:
                media_type = response.headers.get('Content-Type', '').split(';')[0].lower()
                if media_type != 'audio/webm':
                    raise SmokeError('Type audio inattendu.')
                return None
            payload = response.read(MAX_BYTES + 1)
            if len(payload) > MAX_BYTES:
                raise SmokeError('Réponse trop volumineuse.')
            return json.loads(payload)
    except error.HTTPError as exc:
        # Ne pas lire le corps ni afficher l'URL, les en-têtes ou le texte d'erreur.
        code = exc.code
        exc.close()
        raise SmokeError('Échec HTTP ' + str(code) + ' ; aucune redirection suivie.') from None
    except (error.URLError, OSError, ValueError):
        raise SmokeError('Échec réseau, TLS ou réponse JSON invalide.') from None


def run(base, meeting_id, audio_file, environ, *, opener=None):
    base = validate_base(base)
    audio = Path(audio_file)
    if audio.suffix.lower() != '.m4a' or not audio.is_file():
        raise SmokeError('Fournir un fichier de test .m4a existant.')
    with audio.open('rb') as source:
        content = source.read(MAX_BYTES + 1)
    if not content or len(content) > MAX_BYTES:
        raise SmokeError('Fichier de test vide ou trop volumineux (maximum 10 Mio).')
    token = get_token(environ)
    opener = opener or request.build_opener(NoRedirect())
    meetings = call(opener, base, '/api/meetings', token, 200)
    if not isinstance(meetings, list):
        raise SmokeError('Liste de réunions invalide.')
    print('Liste : OK (HTTP 200).')
    if not meetings:
        raise SmokeError('Liste vide : audio et transcription non évalués ; utiliser des données de test.')
    query = parse.urlencode({'meeting_id': meeting_id})
    call(opener, base, '/audio?' + query, token, 200, json_body=False)
    print('Audio : OK (HTTP 200, audio/webm).')
    boundary = 'smoke-' + secrets.token_hex(16)
    # Utiliser un vrai échantillon .m4a : ne pas renommer des octets WebM en M4A.
    prefix = (
        '--' + boundary + '\r\nContent-Disposition: form-data; name="operation"\r\n\r\n'
        'transcription\r\n--' + boundary + '\r\n'
        'Content-Disposition: form-data; name="file"; filename="smoke.m4a"\r\n'
        'Content-Type: audio/mp4\r\n\r\n'
    ).encode()
    payload = prefix + content + ('\r\n--' + boundary + '--\r\n').encode()
    job = call(opener, base, '/api/transcription', token, 202, data=payload,
               content_type='multipart/form-data; boundary=' + boundary)
    if not isinstance(job, dict) or not job.get('job_id'):
        raise SmokeError('Identifiant de job absent de la réponse.')
    print('Transcription : OK (HTTP 202, job_id présent).')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', required=True)
    parser.add_argument('--meeting-id', required=True, help='Réunion de test autorisée')
    parser.add_argument('--audio-file', required=True, help='Échantillon synthétique .m4a')
    args = parser.parse_args(argv)
    try:
        run(args.base, args.meeting_id, args.audio_file, os.environ)
    except SmokeError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except (OSError, ValueError):
        print('Configuration ou entrée locale invalide.', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
