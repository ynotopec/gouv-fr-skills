---
name: gouv-fr-code-stack
description: Stack technique recommandée pour les projets Fabrique Numérique.
version: 0.1.0
author: gouv-fr-code (etalab-ia), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [gouv-fr-code, stack, framework, vue, nestjs, fastify, fastapi, prisma]
    related_skills: [gouv-fr-code, gouv-fr-code-project, gouv-fr-code-lint, gouv-fr-code-monorepo]
---

# Gouv-fr — Stack Technique

La Fabrique Numérique (Mission Interministérielle) recommande une stack technique unifiée pour l'ensemble de ses applications d'État. Cette stack garantit interopérabilité, maintenance à long terme et conformité aux standards du numérique public. Adoptez-la dès la création d'un nouveau projet ou lors d'un onboarding.

## When to Use

- Lancer un nouveau projet Fabrique Numérique
- Choisir une librairie ou un framework pour un projet existant
- Onboarding d'un développeur sur un projet

## Prerequisites

- **pnpm** installé (`corepack enable pnpm` ou `npm i -g pnpm`)
- **proto** — gestionnaire de toolchain (Node, Python, Go, etc.)
- **uv** — gestionnaire Python (v0.4+)

## How to Run

| Stack | Commande |
|-------|----------|
| Vue 3 / DSFR | `pnpm create vue-dsfr mon-app` |
| FastAPI (Python) | `uv init mon-api` |
| NestJS (Node.js) | `pnpm create nest-app mon-api` |
| Fastify (Node.js) | `pnpm create fastify-app mon-api` |

## Quick Reference — Stack recommandée

### Front

| Catégorie | Choix |
|-----------|-------|
| Framework | Vue 3 ou Nuxt 3 |
| DSFR | `@gouvminint/vue-dsfr` (portage Vue actif) |
| Router | VueRouter |
| State | Pinia |
| Build | Vite |
| Icônes | oh-vue-icons ou UnoCSS |
| Style | UnoCSS |
| Tests unitaires | Vitest + Vue Testing Library + Jest DOM |
| Tests e2e | Playwright |
| UI / Design | Storybook |
| Dates | date-fns — toujours UTC en interne, conversion locale à l'affichage |

### Back — Node.js

| Catégorie | Choix |
|-----------|-------|
| Framework | Fastify (préféré) ou NestJS |
| ORM | Prisma (type-safe, migrations intégrées) |
| Validation | `@sinclair/typebox` (JSON Schema + inférence TS) |
| Logging | pino (Fastify) ou nestjs-pino (NestJS) |
| OpenAPI | `@fastify/swagger` + `@fastify/swagger-ui` (Fastify) ou `@nestjs/swagger` (NestJS) |

### Back — Python

| Catégorie | Choix |
|-----------|-------|
| Framework | FastAPI |
| ORM | SQLAlchemy ou Tortoise |
| Validation | Pydantic v2 |
| Gestionnaire | uv (fichiers `pyproject.toml` + `uv.lock`) |

### TypeScript (obligatoire, strict)

- **`enum` proscrit** — utiliser les unions de littéraux à la place (génère du JS inutile)
- **`namespace` proscrit**
- **`any` proscrit** — privilégier `Record<string, unknown>` à `object`
- **`as const`** pour les littéraux immuables
- **Zod** pour la validation runtime (entrées API, variables d'environnement)
- **Interface** pour les contrats objet, **type** pour les unions et types utilitaires

### Monorepo

- **pnpm workspaces** — structure `apps/` (applications) + `packages/` (librairies partagées)
- **Turborepo** — orchestration des tâches avec cache distribué
- **Partagé** — `eslint-config`, `tsconfig`, types partagés dans `packages/`

### Outils de dev

| Outil | Usage |
|-------|-------|
| proto | Gestionnaire de versions (Node, Python, Go…) — remplace nvm / pyenv |
| pnpm | Gestionnaire de paquets (v10.x) |
| uv | Gestionnaire Python (v0.4+) |
| Docker | Conteneurisation |
| GitHub CLI (`gh`) | PR, issues, repos |
| VS Code | Éditeur recommandé (extension ESLint indispensable) |
| zsh + oh-my-zsh | Shell |

### Versions recommandées

| Langue / Outil | Version |
|----------------|---------|
| Node.js | 24.x LTS (épinglé via `.prototools`) |
| pnpm | 10.x |
| TypeScript | dernier stable, mode `strict` |
| Python | 3.12+ |

## Pitfalls

- Ne pas utiliser `enum` TypeScript — il génère du JavaScript inutile. Privilégier les unions de littéraux.
- Toujours épingler les versions dans `.prototools`, `package.json` et `pyproject.toml` / `uv.lock`.
- Utiliser `pnpm` et **jamais** `npm` (cohérence Fabrique Numérique).
- Les dates : toujours stockées et comparées en UTC, conversion locale uniquement au moment de l'affichage.
- **Prisma 7+** : le générateur par défaut est `prisma-client` (l'ancien `prisma-client-js` est déprécié) ; le chemin `output` dans `schema.prisma` doit être explicite.

## Verification

1. **Projet Vue** : `pnpm create vue-dsfr` crée un projet fonctionnel avec Vue 3 + VueDsfr
2. **TypeScript** : `npx tsc --noEmit` ne renvoie aucune erreur en mode strict
3. **Prisma** : `npx prisma validate` passe sans erreur