---

name: developpement-securise
description: Règles de sécurité à appliquer en écrivant du code.
version: 0.1.3
license: MIT
platforms: [linux, macos]
author: etalab-ia
metadata:
  hermes:
    tags: [gouv-fr, security, secrets, gitleaks, sql-injection, tls, dependencies, vm-isolation, cryptography, auth]
    related_skills: [projet-structure, workflow-dev, developpement-securise, anssi-guides]
---

# Gouv-fr — Règles de sécurité

Règles de sécurité non négociables pour les applications de l'État.

## Quand utiliser

- Écrire du code pour l'État et appliquer les règles de sécurité non négociables.
- Trancher une question de secrets, de requêtes SQL, de TLS ou d'isolation.

Règles de fond, pas d'audit : pour un audit, voir `audit-durcissement`,
`audit-securite-depot` ou `redteam-llm`.

## Principes

- **Aucun secret en dur** — jamais de clé API, token, mot de passe. `.env` uniquement, jamais commité
- **gitleaks obligatoire** — `--no-verify` interdit
- **Données sensibles** — pas de données personnelles, RH, médicales. Données synthétiques en fixtures
- **SQL injection** — utiliser des requêtes paramétrées, jamais de concaténation
- **Dépendances** — pas d'ajout non justifié, préférer la lib standard
- **TLS** — HTTPS par défaut, pas de désactivation vérification certificat
- **Incertitude** — poursuivre les contrôles indépendants ; demander seulement si une information indispensable manque ou si une action dépasse le périmètre autorisé.

## Isolation VM

- Vérifier l’isolation réellement fournie (VM, conteneur ou sandbox) et ses permissions ; ne pas supposer une VM Lima.
- Réduire l’accès aux fichiers personnels et credentials hôte par des permissions effectives.
- Utiliser la connexion GitHub autorisée (application, connecteur ou jeton dédié).
- Pas de sudo sans explication ; pas de chemins en dur

## Prompt Injection

L'agent peut tenter des appels réseau. Mitigations :
- Clés dédiées et révocabiles
- Review humaine obligatoire pour les PR
- Privilégier les appels en sortie uniquement
