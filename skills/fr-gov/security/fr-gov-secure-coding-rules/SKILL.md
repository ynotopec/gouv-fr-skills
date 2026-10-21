---

name: fr-gov-secure-coding-rules
description: Mandatory Gitleaks, synthetic fixtures, TLS, SQL safety
version: 0.1.3
license: MIT
platforms: [linux, macos]
author: etalab-ia
metadata:
  hermes:
    tags: [gouv-fr, security, secrets, gitleaks, sql-injection, tls, dependencies, vm-isolation, cryptography, auth]
    related_skills: [fr-gov-set-up-project-layout, ship-a-dev-task, fr-gov-secure-coding-rules, fr-gov-find-cybersecurity-guide]
---

# Gouv-fr — Règles de sécurité

Règles de sécurité non négociables pour les applications de l'État.

## Quand utiliser

- Écrire du code pour l'État et appliquer les règles de sécurité non négociables.
- Trancher une question de secrets, de requêtes SQL, de TLS ou d'isolation.

Règles de fond, pas d'audit : pour un audit, voir `harden-repo-before-pentest`,
`audit-repo-safety` ou `redteam-llm-prompt-injection`.

## Principes

- **Aucun secret en dur** — jamais de clé API, token, mot de passe. `.env` uniquement, jamais commité
- **gitleaks obligatoire** — `--no-verify` interdit
- **Données sensibles** — pas de données personnelles, RH, médicales. Données synthétiques en fixtures
- **SQL injection** — utiliser des requêtes paramétrées, jamais de concaténation
- **Dépendances** — pas d'ajout non justifié, préférer la lib standard
- **TLS** — HTTPS par défaut, pas de désactivation vérification certificat
- **Secrets avec caractères spéciaux** (`$`) — utiliser `kubectl --from-literal='KEY=val'` avec guillemets simples (pas de substitution shell). Vérifier après injection (`base64 -d`, jamais afficher en clair dans chat/repo). Ne jamais écrire la clé dans des fixtures/datasets (utiliser un placeholder `[CLÉ PROTÉGÉE]` et référencer le secret K8S par nom).
- **Dataset de test synthétique** — pour vérifier conformité (DSFR/RGAA/RGPD) : générer des PDF image sans couche texte, sans données réelles, sans clé. Vérifier `grep -rni` sur le jeu de test avant livraison.
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
