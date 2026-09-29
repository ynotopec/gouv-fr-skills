# gouv-fr-skills

Répertoire de skills Hermes pour les projets de la Fabrique Numérique (Mission Interministérielle).

## Origines

- **Starter Kit OpenCode** (`dnum-mi/starter-kit-opencode`) — CoFabNum conventions, stack, CI/CD, CPiN
- **gouv-fr-code-package-mi** (`ynotopec/gouv-fr-code-package-mi`) — Core skills gouv-fr-code
- **Skills locaux gouv-fr** — DSFR, audit, référentiel données (migrés)

## Liste des skills

```
# Core
skills/gouv-fr-code/            # Index
skills/gouv-fr-code-project/    # Structure projet, CLI, OpenCode
skills/gouv-fr-code-security/   # Sécurité, secrets, gitleaks, TLS
skills/gouv-fr-code-compliance/ # RGAA, DSFR, RGPD
skills/gouv-fr-code-workflow/   # Plan mode, task management
skills/gouv-fr-code-api/        # API REST, OpenAPI, Swagger
skills/gouv-fr-code-lint/       # ESLint, Ruff, EditorConfig
skills/gouv-fr-code-quality/    # Bonnes pratiques, tests
skills/gouv-fr-code-audit/      # Audit de conformité

# Development
skills/gouv-fr-stack/           # Stack technique recommandée (Front/Back/Outils)
skills/gouv-fr-monorepo/        # pnpm workspaces + Turborepo
skills/gouv-fr-outils-dev/      # Git, Docker, pnpm, proto, VS Code, uv
skills/gouv-fr-deploiement/     # Docker rootless, K8s securityContext
skills/gouv-fr-conventions/     # Conventions CoFabNum complètes
skills/gouv-fr-ci-cd/           # CI GitHub Actions minimal
skills/gouv-fr-cicd-fabnum/     # Workflows fabnum-cicd réutilisables
skills/gouv-fr-recettes-serveur/ # Fastify, NestJS, FastAPI server
skills/gouv-fr-recettes-client/  # Vue 3, VueDsfr, Nuxt 3

# Cloud Pi Native
skills/gouv-fr-deploiement-cpin/ # Déploiement Cloud Pi Native complet (console, pipeline, ArgoCD)
skills/gouv-fr-helm-chart-cpin/  # Helm chart CPiN (OpenShift, Kyverno)

# DSFR
skills/gouv-fr-dsfr/            # DSFR Système de Design
skills/gouv-fr-dsfr-artwork/    # Pictogrammes, icônes, visuels DSFR
skills/gouv-fr-dsfr-chart/      # Graphiques DSFR Vue.js
skills/gouv-fr-dsfr-mail/       # Templates email DSFR
skills/gouv-fr-dsfr-theme-tarteaucitron/ # Gestion cookies Tarte au Citron
skills/gouv-fr-dsfr-vue/        # VueDsfr composants Vue 3

# Données
skills/gouv-fr-referentiel-donnees/  # Données ouvertes SIG
```

## Installation

```bash
# Copier les skills dans le répertoire Hermes
cp -r skills/gouv-fr-*/ ~/.hermes/skills/
```

## Vérification

- Chaque skill dans `skills/gouv-fr-*/` contient un `SKILL.md` avec frontmatter YAML
- Tous les noms commencent par `gouv-fr-`
- `skills/gouv-fr-code/SKILL.md` est l'index
