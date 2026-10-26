"""Shared result format and static, escaped HTML reports."""

import html
import json
from pathlib import Path


def summarize(results):
    return {status: sum(row['status'] == status for row in results)
            for status in ('pass', 'fail', 'error', 'skip')}


def exit_code(results):
    counts = summarize(results)
    return int(bool(counts['fail'] or counts['error']))


def write_report(results, output_dir, name):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    summary = summarize(results)
    payload = {'summary': summary, 'results': results}
    (output_dir / f'{name}.json').write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    rows = []
    for row in results:
        cells = ''.join('<td>' + html.escape(str(row[key])) + '</td>'
                        for key in ('skill', 'status', 'detail'))
        rows.append('<tr>' + cells + '</tr>')
    document = '''<!doctype html><html lang="fr"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Évaluation des skills</title><style>
body{font:16px system-ui;max-width:1100px;margin:2rem auto;padding:1rem}
table{border-collapse:collapse;width:100%}td,th{border:1px solid #aaa;padding:.6rem;text-align:left}
td{white-space:pre-wrap;overflow-wrap:anywhere}p{line-height:1.6}
</style><h1>Évaluation des skills — ''' + html.escape(name) + '</h1><p>'
    document += html.escape(', '.join(f'{count} {status}' for status, count in summary.items()))
    document += '''</p><p>PASS indique uniquement la réussite des contrôles exécutés.
SKIP indique une absence de test comportemental, jamais une validation du skill.
Ces contrôles ne mesurent pas les performances d’un agent ou d’un modèle.</p>
<table><thead><tr><th>Skill / contrôle</th><th>Statut</th><th>Preuve / détail</th></tr></thead><tbody>'''
    document += ''.join(rows) + '</tbody></table></html>\n'
    (output_dir / f'{name}.html').write_text(document, encoding='utf-8')
    print(f'{name}: ' + ', '.join(f'{count} {status}' for status, count in summary.items()))
    print(f'Rapport: {output_dir / (name + ".html")}')
