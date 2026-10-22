---

name: fr-gov-project-conventions
description: Naming, TypeScript strict, branches, commit conventions
version: 0.2.0
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [gouv-fr, conventions, nommage, architecture, typescript, fr-gov-rest-api-conventions]
    related_skills: [fr-gov-set-up-project-layout, fr-gov-configure-linting, fr-gov-choose-tech-stack]
---
# Gouv-fr — Conventions de développement

Best practices for all Fabrique Numérique projects. Language-agnostic unless noted.

## Quand utiliser

- Démarrer un projet et fixer nommage, architecture des dossiers, TypeScript.
- Trancher une question de convention transversale en revue.

Ne pas utiliser pour l'outillage (`fr-gov-install-dev-tools`), le lint seul
(`fr-gov-configure-linting`), l'API seule (`fr-gov-rest-api-conventions`) ni la revue (`review-code`).

## Référence rapide
| Topic | Key Rule |
|-------|----------|
| Branches | `<type>/<kebab-desc>#<ticket>` |
| Commits | Conventional Commits (French OK) |
| Files/folders | `kebab-case` (Vue files: PascalCase) |
| TypeScript | strict mode, no `enum`/`namespace` |
| API routes | nouns only, plural, no verbs |
| Functions | max 20 lines, one purpose |
| Lint JS/TS | `@antfu/eslint-config` |
| Lint Python | `ruff` |
| Docker | multi-stage, non-root, pinned tags |
| Deploy | Helm charts on K8s/OpenShift |

## Scripts disponibles

- **`scripts/validate-branch.sh`** — Validates branch name format
  - Usage: `bash scripts/validate-branch.sh` (current branch)
  - Usage: `bash scripts/validate-branch.sh feat/my-feature#123`
  - Returns exit code 0 if valid, 1 if invalid
- **`scripts/check-folders.sh`** — Checks folder/file naming conventions
  - Usage: `bash scripts/check-folders.sh` (current directory)
  - Usage: `bash scripts/check-folders.sh src/`
  - Reports kebab-case violations and Vue PascalCase issues

Progress:
- [ ] `README.md` — prerequisites, quick start, scripts table
- [ ] `CONTRIBUTING.md` — if external contributors
- [ ] User docs — step-by-step guide, features, FAQ, contact

### README.md template

```markdown
# Project Name

> Short description

## Prérequis

- Node.js 24.x (via proto)
- pnpm 10.x
- Docker

## Quick Start

pnpm install
pnpm dev

## Scripts

| Command | Description |
|---------|-------------|
| `pnpm dev` | Dev server |
| `pnpm build` | Build |
| `pnpm test` | Tests |
| `pnpm lint` | Lint |

## Architecture

See folder architecture conventions.
```

## Naming

### Git branches

```
<type>/<kebab-description>#<ticket>
```

Types: `feat`, `fix`, `hotfix`, `tech`, `docs`, `refactor`

Examples: `feat/worker-logs#353`, `refactor/reorganize-backend#360`

### Commit messages

Conventional Commits format. French is acceptable.

### Files and folders

**All files/folders**: `kebab-case`.
**Vue component files**: `PascalCase`, at least 2 words (except `App.vue`).

### Variables

- Boolean: `isXxx` or `hasXxx` in `camelCase`
- Date: `xxxDate` or `xxxAt` in `camelCase`
- Class: `PascalCase`
- Function/variable: `camelCase`
- Constant: `SCREAMING_SNAKE_CASE`

Names must be explicit. Avoid single-character names. Prefer English; French allowed when translation is confusing
(`demarche`, `affaire`).

## Renvois

Les conventions détaillées ne sont plus dupliquées ici :

- Routes, codes HTTP, réponses d'erreur, OpenAPI, fichiers `.rest` : skill
  `fr-gov-rest-api-conventions` (source unique).
- ESLint (flat config), Ruff, EditorConfig : skill `fr-gov-configure-linting`.
- Arborescence du dépôt : [arborescence](references/arborescence.md).
- TypeScript strict (tsconfig, types) : [typescript](references/typescript.md).

## Code Quality

Progress:
- [ ] Lines ≤ 120 (≤ 140 forbidden)
- [ ] Functions ≤ 20 lines
- [ ] One function = one purpose
- [ ] No silent error swallowing
- [ ] async/await over .then()
- [ ] Named constants, no magic numbers
- [ ] Early return over deep nesting
- [ ] Dependency evaluation checklist

### Never silently ignore errors

```typescript
try { await fetch() } catch (error) {
  logger.error(error, 'Failed to fetch')
  throw error
}
```

### Use typed errors

```typescript
class NotFoundError extends Error {
  constructor(resource: string, id: string) {
    super(`${resource} with id ${id} not found`)
    this.name = 'NotFoundError'
  }
}
```

### Dependency evaluation checklist

Before adding any dependency:

- [ ] Latest stable major version (never `@latest`/`@master` in prod)
- [ ] Popular (downloads, stars)
- [ ] Actively maintained (commits in last 12 months)
- [ ] Security.md present
- [ ] Bundle size acceptable ([bundlephobia.com](https://bundlephobia.com))

**Security rule**: épingler chaque GitHub Action par **SHA de commit** (un tag est
mutable) ; à défaut, un tag majeur explicite (`@v6`). Jamais `@master`, `@main`
ni `@latest`. Détail et gabarit : `fr-gov-set-up-github-actions-ci`.

## POC → Production

Progress:
- [ ] Modular architecture, API decoupled from AI logic
- [ ] Pydantic validation (FastAPI) or Prisma (NestJS/Fastify)
- [ ] Async for I/O, queue for CPU-intensive
- [ ] CORS restricted, JWT/OAuth2 auth
- [ ] Docker: lightweight, multi-stage, non-root, healthchecks
- [ ] Unit + integration tests from day 1
- [ ] Structured JSON logs, request_id correlation
- [ ] Health endpoints: `/health`, `/readiness`
- [ ] OpenAPI/Swagger docs auto-generated
- [ ] Rollback plan documented
- [ ] DB migrations configured

## Pièges

- **Vue components need 2+ words** — `BadgeTypeOrganisme.vue` not `Badge.vue` (except `App.vue`)
- **Folders are kebab-case but Vue files are PascalCase** — don't mix them
- **`enum` and `namespace` are banned** — they emit JS runtime code, breaking the "remove types = valid JS" philosophy
- **ESLint replaces Prettier** — with `@antfu/eslint-config`, don't install Prettier separately
- **Ruff replaces 4 tools** — black, flake8, isort, pyupgrade are all replaced by `ruff check` + `ruff format`
- **Never modify migration files manually** — always use `prisma migrate dev`
- **Branch naming must include ticket number** — `feat/description` is incomplete, use `feat/description#123`
- **Log messages in French for French projects** — but keep structured fields (keys) in English
- **Cloud Pi Native is the default target** — design for K8s/OpenShift rootless from day one
