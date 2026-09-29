---
name: gouv-fr-code-quality
description: Bonnes pratiques de code, lint, formattage et tests pour Fabrique Numérique.
version: 0.1.0
author: gouv-fr-code (etalab-ia), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [gouv-fr-code, quality, lint, format, testing, code-quality]
    related_skills: [gouv-fr-code, gouv-fr-code-project, gouv-fr-code-lint]
---

# Gouv-fr — Qualité de Code

Bonnes pratiques de code, règles de lint, formattage et tests pour les projets Fabrique Numérique.

## When to Use
- Écrire du code selon les standards de la Fabrique Numérique
- Configurer le lint et le formattage d'un projet
- Ajouter ou modifier des tests

## Prerequisites
- VS Code avec les extensions ESLint et Ruff installées
- ESLint installé (projet JS/TS) ou Ruff (projet Python)
- Vitest installé pour les tests

## How to Run
- `pnpm lint` pour le lint JS/TS
- `pnpm lint:fix` pour auto-corriger
- `pnpm test` pour lancer les tests Vitest
- `pnpm ruff check` pour le lint Python
- `pnpm ruff format` pour le formattage Python

## Quick Reference — Règles de code

### Structure de fichier
- Lignes ≤ 120 colonnes ; > 140 **proscrites**
- `.editorconfig` à la racine (2 spaces, LF, UTF-8, trim trailing whitespace)
- Dossiers et fichiers en **kebab-case** (sauf composants Vue)

### Fonctions
- **≤ 20 lignes**
- Une fonction = un but
- Noms explicites, pas de variables d'une seule lettre (sauf identité `x => x`)

### Erreurs
- Ne jamais ignorer silencieusement :
  ```typescript
  // ❌
  try { await fetchData() } catch { }

  // ✅
  try { await fetchData() } catch (error) {
    logger.error(error, 'Erreur')
    throw error
  }
  ```
- Créer des erreurs typées (`NotFoundError`, `ValidationError`)
- Ne pas utiliser `Error` générique

### Async/Await
- Toujours `async/await` plutôt que `.then()`/`.catch()`
- Paralléliser les opérations indépendantes avec `Promise.all()`
- `async def` pour les endpoints qui font de l'I/O

### Imports
1. Modules Node.js natifs (`node:fs`)
2. Packages externes (`fastify`, `vue`)
3. Modules internes (alias `@/`, `~/`)
4. Modules relatifs (`./`, `../`)
- Chaque groupe séparé par une ligne vide

### Constantes
- Extraire les valeurs magiques dans des constantes nommées :
  ```typescript
  // ❌
  if (password.length < 8) { ... }

  // ✅
  const MIN_PASSWORD_LENGTH = 8
  if (password.length < MIN_PASSWORD_LENGTH) { ... }
  ```

### Early Return
- Privilégier les retours anticipés pour éviter l'imbrication :
  ```typescript
  // ✅
  if (!user) return
  if (!user.isActive) return
  // traitement...
  ```

### Dépendances
Avant d'ajouter une dépendance, évaluer :
1. Version courante (utiliser la dernière stable majeure)
2. Popularité (downloads hebdo, stars GitHub)
3. Fréquence de mise à jour (12 mois sans commit = signal d'alerte)
4. Maintenance (issues ouvertes, réactivité mainteneurs, SECURITY.md)
5. Taille (bundlephobia.com pour npm)

### Tests (obligatoires)
- Tests unitaires dès le début
- Tests d'intégration pour les endpoints API
- Test de composants avec Vue Testing Library
- E2E avec Playwright
- Vitest pour JS/TS, pytest pour Python
- Couverture : ≥ 80% recommandé

## Procedure — Configurer le lint

### JS/TS (ESLint)
1. `pnpm add -D eslint @antfu/eslint-config`
2. Créer `eslint.config.js` avec la config Antfu
3. Surcharger : `style/comma-dangle`, `no-irregular-whitespace`
4. Ajouter dans `.vscode/settings.json` l'auto-format

### Python (Ruff)
1. `uv add --dev ruff`
2. Créer `ruff.toml` ou config dans `pyproject.toml`
3. Règles : `E, W, F, I, N, UP, B, C4, SIM`
4. Ligne max : 88 (équivalent black)

## Pitfalls
- ESLint remplace Prettier — ne pas installer Prettier séparément avec `@antfu/eslint-config`
- Flat config (`eslint.config.js`) depuis ESLint v9 — pas de `.eslintrc`
- Ruff remplace black, flake8, isort, pyupgrade — ne pas les installer tous ensemble
- Les tests doivent être mis à jour avec le code, pas après
- Ne pas ignorer une erreur avec un `catch` vide — au minimum logger

## Verification
- `pnpm lint` ne rapporte aucune erreur
- `pnpm test` passe pour tous les cas
- `pnpm ruff check` (Python) sans erreur
- Couverture de tests ≥ 80%
