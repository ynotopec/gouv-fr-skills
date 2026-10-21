#!/usr/bin/env python3
"""Smoke-test explicite : secrets en mémoire, sorties limitées aux statuts.

Utilise SMOKE_TOKEN ou forge le jeton avec INTERNAL_API_TOKEN depuis
l'environnement du processus. Ne suit aucun redirect et n'affiche ni secret
ni corps de réponse. Bibliothèque standard uniquement.

Le contrat d'API est paramétrable : le script vérifie par défaut une API de
type « liste de ressources / média / job asynchrone », mais les chemins, le
paramètre d'identifiant et les types de média sont fournis par l'appelant.
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

# Contrat par défaut : à adapter au projet via les options --*-path.
DEFAULT_LIST_PATH = '/api/meetings'
DEFAULT_ITEM_PATH = '/audio'
DEFAULT_JOB_PATH = '/api/transcription'
DEFAULT_ID_PARAM = 'meeting_id'
DEFAULT_MEDIA_TYPE = 'audio/webm'
DEFAULT_AUDIO_SUFFIX = '.m4a'
DEFAULT_AUDIO_CONTENT_TYPE = 'audio/mp4'


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
    if any(ord(c) <= 32 or ord(c) == 127 for c in base) or '\\' in base:
        raise SmokeError('Origine HTTPS invalide.')
    url = parse.urlsplit(base)
    if (url.scheme != 'https' or not url.hostname or url.username or url.password
            or url.query or url.fragment or url.path not in ('', '/')):
        raise SmokeError('Base invalide : origine HTTPS sans identifiant, chemin, query ou fragment requise.')
    return base.rstrip('/')


def endpoint_url(base, path):
    """Ne jamais laisser une option de chemin modifier l'origine autorisée."""
    if (not path.startswith('/') or path.startswith('//') or '\\' in path
            or any(ord(c) <= 32 or ord(c) == 127 for c in path)):
        raise SmokeError('Endpoint invalide : chemin absolu local requis.')
    endpoint = parse.urlsplit(path)
    if endpoint.scheme or endpoint.netloc or endpoint.fragment:
        raise SmokeError('Endpoint invalide : origine externe ou fragment interdit.')
    url = base + path
    origin, target = parse.urlsplit(base), parse.urlsplit(url)
    if (origin.scheme, origin.netloc) != (target.scheme, target.netloc):
        raise SmokeError('Endpoint hors de l’origine autorisée.')
    return url


def call(opener, base, path, token, expected, *, data=None, content_type=None,
         json_body=True, media_type=None):
    headers = {'Authorization': 'Bearer ' + token}
    if content_type:
        headers['Content-Type'] = content_type
    req = request.Request(endpoint_url(base, path), headers=headers, data=data)
    try:
        with opener.open(req, timeout=30) as response:
            if response.status != expected:
                raise SmokeError('Code HTTP inattendu.')
            if not json_body:
                returned = response.headers.get('Content-Type', '').split(';')[0].lower()
                if returned != media_type:
                    raise SmokeError('Type de média inattendu.')
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


def run(base, item_id, audio_file, environ, *, opener=None, list_path=DEFAULT_LIST_PATH,
        item_path=DEFAULT_ITEM_PATH, job_path=DEFAULT_JOB_PATH, id_param=DEFAULT_ID_PARAM,
        media_type=DEFAULT_MEDIA_TYPE, audio_suffix=DEFAULT_AUDIO_SUFFIX,
        audio_content_type=DEFAULT_AUDIO_CONTENT_TYPE, job_field='job_id',
        operation='transcription'):
    base = validate_base(base)
    # Vérifier les trois endpoints avant de lire un credential ou d'appeler le service.
    for path in (list_path, item_path, job_path):
        endpoint_url(base, path)
    audio = Path(audio_file)
    if audio.suffix.lower() != audio_suffix or not audio.is_file():
        raise SmokeError('Fournir un fichier de test ' + audio_suffix + ' existant.')
    with audio.open('rb') as source:
        content = source.read(MAX_BYTES + 1)
    if not content or len(content) > MAX_BYTES:
        raise SmokeError('Fichier de test vide ou trop volumineux (maximum 10 Mio).')
    token = get_token(environ)
    opener = opener or request.build_opener(NoRedirect())
    items = call(opener, base, list_path, token, 200)
    if not isinstance(items, list):
        raise SmokeError('Liste de ressources invalide.')
    print('Liste : OK (HTTP 200).')
    if not items:
        raise SmokeError('Liste vide : média et job non évalués ; utiliser des données de test.')
    query = parse.urlencode({id_param: item_id})
    separator = '&' if '?' in item_path else '?'
    call(opener, base, item_path + separator + query, token, 200, json_body=False,
         media_type=media_type)
    print('Média : OK (HTTP 200, ' + media_type + ').')
    boundary = 'smoke-' + secrets.token_hex(16)
    # Utiliser un vrai échantillon du format attendu : ne pas renommer des octets WebM en M4A.
    prefix = (
        '--' + boundary + '\r\nContent-Disposition: form-data; name="operation"\r\n\r\n'
        + operation + '\r\n--' + boundary + '\r\n'
        'Content-Disposition: form-data; name="file"; filename="smoke' + audio_suffix + '"\r\n'
        'Content-Type: ' + audio_content_type + '\r\n\r\n'
    ).encode()
    payload = prefix + content + ('\r\n--' + boundary + '--\r\n').encode()
    job = call(opener, base, job_path, token, 202, data=payload,
               content_type='multipart/form-data; boundary=' + boundary)
    if not isinstance(job, dict) or not job.get(job_field):
        raise SmokeError('Identifiant de job absent de la réponse.')
    print('Job : OK (HTTP 202, ' + job_field + ' présent).')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', required=True)
    parser.add_argument('--item-id', '--meeting-id', dest='item_id', required=True,
                        help='Identifiant de la ressource de test autorisée')
    parser.add_argument('--audio-file', required=True, help='Échantillon synthétique de test')
    parser.add_argument('--list-path', default=DEFAULT_LIST_PATH, help='Chemin de la liste des ressources')
    parser.add_argument('--item-path', default=DEFAULT_ITEM_PATH, help='Chemin de la ressource unitaire')
    parser.add_argument('--job-path', default=DEFAULT_JOB_PATH, help='Chemin du job asynchrone')
    parser.add_argument('--id-param', default=DEFAULT_ID_PARAM, help="Nom du paramètre d'identifiant")
    parser.add_argument('--media-type', default=DEFAULT_MEDIA_TYPE, help='Type de média attendu')
    parser.add_argument('--audio-suffix', default=DEFAULT_AUDIO_SUFFIX, help='Extension du fichier de test')
    parser.add_argument('--audio-content-type', default=DEFAULT_AUDIO_CONTENT_TYPE,
                        help='Type de contenu du fichier de test')
    parser.add_argument('--job-field', default='job_id', help="Champ contenant l'identifiant du job")
    parser.add_argument('--operation', default='transcription', help='Valeur du champ multipart operation')
    args = parser.parse_args(argv)
    try:
        run(args.base, args.item_id, args.audio_file, os.environ,
            list_path=args.list_path, item_path=args.item_path, job_path=args.job_path,
            id_param=args.id_param, media_type=args.media_type,
            audio_suffix=args.audio_suffix, audio_content_type=args.audio_content_type,
            job_field=args.job_field, operation=args.operation)
    except SmokeError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except (OSError, ValueError):
        print('Configuration ou entrée locale invalide.', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
