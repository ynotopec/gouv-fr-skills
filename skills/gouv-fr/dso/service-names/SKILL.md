---

name: service-names
description: "Contrôle anti-régression des noms de services renommés."
version: 1.1.0
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [gouv-fr, rebranding, regression, service-names, nomenclature]
    related_skills: [repo-init, repo-cicd]
---

# Gouv-fr — Noms de services (anti-régression)

Après un renommage de services, les anciens noms peuvent réapparaître dans le
code, les manifests ou la documentation. Ce skill détecte cette régression à
partir d'une **table de correspondance** fournie par le projet.

## Préparer la table de correspondance

La table est un fichier du projet (ex. `reference_services_naming.yaml`, ou
une section d'un ADR de renommage). Format simple, une entrée par ligne :

```yaml
ancien: nouveau
```

| Ancien | Nouveau |
|---|---|
| `code-generator` | `mydevices-web` |
| `upload-portal` | `mobile-upload-pwa` |

Si le projet n'a pas de table, la demander : sans elle, le scan n'a aucun
référence et ne peut rien signaler.

## Scan

Construire la liste des anciens noms depuis la table, puis cibler les fichiers
susceptibles de contenir un nom de service (k8s, code, docs, scripts) :

```bash
# <table> = chemin du fichier de correspondance
awk -F': ' '!/^#/ && NF==2 {print $1}' <table> | sort -u > /tmp/anciens-noms.txt

rg -n --type-add 'k8s:*.{yaml,yml}' \
   --type-add 'cfg:*.{env,ini,toml,json}' \
   -t k8s -t cfg -t py -t js -t ts -t md -t sh \
   -f /tmp/anciens-noms.txt \
   .
```

## Restreindre au diff courant

Si seules les modifications en cours comptent :

```bash
git diff --name-only origin/main...HEAD | \
  xargs rg -f /tmp/anciens-noms.txt 2>/dev/null
```

## Faux positifs légitimes

- Anciennes ADRs / commits / changelog : conserver tel quel (historique).
- `docs/migration-*.md` : nommer explicitement l'ancien pour montrer la bascule.
- Logs / dashboards archivés.

→ Si une occurrence tombe dans ces catégories, l'annoter `<!-- legacy-name -->`
  ou la déplacer dans un fichier `*-legacy.md` pour qu'on l'exclue plus tard.

## Action si occurrences trouvées

1. Lister les fichiers + ligne + ancien nom.
2. Proposer la substitution (Edit ou sed) en confirmant chaque cas (un nom peut
   apparaître dans un commentaire historique légitime).
3. Re-scanner après remplacement pour confirmer 0 occurrence active.
