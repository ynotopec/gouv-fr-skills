---
name: gouv-fr-code-monorepo
description: Architecture monorepo pnpm workspaces et Turborepo pour les projets Fabrique Numérique.
version: 0.1.0
author: gouv-fr-code (etalab-ia), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [gouv-fr-code, monorepo, pnpm, turbo, workspace, shared]
    related_skills: [gouv-fr-code, gouv-fr-code-project, gouv-fr-code-stack]
---

# Gouv-fr — Monorepo

Architecture monorepo avec pnpm workspaces et Turborepo pour les projets Fabrique Numérique.

## When to Use
- Un projet avec client + serveur + bibliothèques partagées
- Partager du code TypeScript entre le frontend et le backend
- Centraliser le lint, les tests et le build

## Prerequisites
- pnpm 10.x installé (`npm i -g pnpm` ou via proto)
- Node.js 24.x LTS (épinglé dans `.prototools`)
- git init dans le projet

## How to Run
- `pnpm install` — installe toutes les dépendances des workspaces
- `pnpm turbo build` — build tous les packages
- `pnpm turbo lint --filter=apps/client...` — lint uniquement les packages touchés

## Quick Reference — Structure

```
monorepo/
├── apps/                          # Applications
│   ├── client/                    # Vue 3 / Nuxt 3
│   │   ├── package.json
│   │   ├── vite.config.ts
│   │   └── src/
│   └── server/                    # Fastify / NestJS / FastAPI
│       ├── package.json
│       ├── tsconfig.json
│       └── src/
├── packages/                      # Packages partagés
│   ├── shared/                    # Types, utilitaires, DTOs
│   │   └── package.json
│   ├── eslint-config-fabnum/      # Config ESLint partagée
│   │   └── package.json
│   └── tsconfig/                  # tsconfig partagé
│       ├── package.json
│       └── tsconfig.json
├── pnpm-workspace.yaml            # Définition des workspaces
├── turbo.json                     # Config Turborepo
├── package.json                   # Dépendances racine (turborepo)
└── pnpm-lock.yaml                 # Lock unique global
```

## Quick Reference — pnpm workspaces

### `pnpm-workspace.yaml` (racine)
```yaml
packages:
  - "apps/**"
  - "packages/**"
```

### Package partagé (`packages/shared/package.json`)
```json
{
  "name": "@monorepo/shared",
  "version": "0.0.0",
  "private": true,
  "types": "index.ts"
}
```

### Référence entre workspaces (`apps/client/package.json`)
```json
{
  "dependencies": {
    "@monorepo/shared": "workspace:^"
  },
  "devDependencies": {
    "@monorepo/eslint-config-fabnum": "workspace:*"
  }
}
```

## Quick Reference — Turborepo

### Installation
```bash
pnpm add -Dw turbo
```

### `turbo.json` (racine)
```json
{
  "$schema": "https://turbo.build/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "lint": {
      "dependsOn": ["^build"]
    },
    "test": {
      "dependsOn": ["build"]
    }
  }
}
```

### Scripts package.json racine
```json
{
  "scripts": {
    "build": "turbo build",
    "dev": "turbo dev",
    "lint": "turbo lint",
    "test": "turbo test"
  }
}
```

### Turborepo — flags utiles
- `turbo build --filter=apps/client` — build uniquement client
- `turbo build --filter=apps/server...` — build server et ses dépendances
- `turbo lint --filter=[HEAD~1]` — lint uniquement les fichiers modifiés

## Pitfalls
- `.turbo` et `.pnpm-store` doivent être dans `.gitignore`
- Les packages partagés doivent avoir `"private": true`
- Utiliser `workspace:^` pour les dépendances de prod, `workspace:*` pour dev
- Le lockfile est unique à la racine — pas de lock par workspace
- Turborepo cache les résultats de build — si les `outputs` sont mal définis, le cache sera incorrect

## Verification
- `pnpm install` installe tous les workspaces sans erreur
- `pnpm turbo build` compile tous les packages dans le bon ordre
- `pnpm turbo test` lance les tests de tous les packages
- Le code partagé est accessible depuis les apps avec `@monorepo/shared`
