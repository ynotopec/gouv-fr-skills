---
name: gouv-fr-securite
description: "Sécurité : secrets, gitleaks, SQL, TLS, isolation VM."
category: security
version: 0.1.2
author: etalab-ia, Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [gouv-fr, security, secrets, gitleaks, sql-injection, tls, dependencies, vm-isolation, cryptography, auth]
    related_skills: [gouv-fr-projet-structure, gouv-fr-workflow-dev, gouv-fr-securite, gouv-fr-anssi-guides]
---

# Gouv-fr — Règles de sécurité

Règles de sécurité non négociables pour les applications gouv-fr-code-index.

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
