# gouv-fr-skills

Répertoire de skills Hermes pour les projets de la Fabrique Numérique (Mission Interministérielle).

## Origines

- **Starter Kit OpenCode** (`dnum-mi/starter-kit-opencode`) — CoFabNum conventions, stack, CI/CD, CPiN
- **gouv-fr-code-package-mi** (`ynotopec/gouv-fr-code-package-mi`) — Core skills gouv-fr-code
- **Skills locaux gouv-fr** — DSFR, audit, référentiel données (migrés)

## Liste des skills

### Core

| Skill | Description |
|-------|-------------|
| `skills/gouv-fr-api-rest/` | API REST, OpenAPI, Swagger |
| `skills/gouv-fr-audit-conformite/` | Audit de conformité |
| `skills/gouv-fr-code-index/` | Index de l'ensemble des skills |
| `skills/gouv-fr-compliance-rgaa/` | RGAA, DSFR, RGPD |
| `skills/gouv-fr-lint-eslint/` | ESLint, Ruff, EditorConfig |
| `skills/gouv-fr-projet-structure/` | Structure projet, CLI, OpenCode |
| `skills/gouv-fr-qualite-code/` | Bonnes pratiques, tests |
| `skills/gouv-fr-securite/` | Sécurité, secrets, gitleaks, TLS |
| `skills/gouv-fr-workflow-dev/` | Plan mode, task management |

### Développement

| Skill | Description |
|-------|-------------|
| `skills/gouv-fr-backend-fastify/` | Fastify, NestJS, FastAPI server |
| `skills/gouv-fr-conventions-nommage/` | Conventions CoFabNum complètes |
| `skills/gouv-fr-deploiement-docker-k8s/` | Docker rootless, K8s securityContext |
| `skills/gouv-fr-frontend-vue3/` | Vue 3, VueDsfr, Nuxt 3 |
| `skills/gouv-fr-github-actions-ci/` | CI GitHub Actions minimal |
| `skills/gouv-fr-github-actions-reusable/` | Workflows fabnum-cicd réutilisables |
| `skills/gouv-fr-monorepo-pnpm/` | pnpm workspaces + Turborepo |
| `skills/gouv-fr-outils-developpement/` | Git, Docker, pnpm, proto, VS Code, uv |
| `skills/gouv-fr-stack-technique/` | Stack technique recommandée (Front/Back/Outils) |

### Cloud Pi Native

| Skill | Description |
|-------|-------------|
| `skills/gouv-fr-deploiement-cloud-pi-native/` | Déploiement Cloud Pi Native complet (console, pipeline, ArgoCD) |
| `skills/gouv-fr-helm-chart/` | Helm chart CPiN (OpenShift, Kyverno) |

### DSFR

| Skill | Description |
|-------|-------------|
| `skills/gouv-fr-cookies-rgpd/` | Gestion cookies Tarte au Citron |
| `skills/gouv-fr-composants-vue/` | VueDsfr composants Vue 3 |
| `skills/gouv-fr-design-system/` | DSFR Système de Design |
| `skills/gouv-fr-graphiques-DSFR/` | Graphiques DSFR Vue.js |
| `skills/gouv-fr-pictogrammes-DSFR/` | Pictogrammes, icônes, visuels DSFR |
| `skills/gouv-fr-templates-email/` | Templates email DSFR |

### Données

| Skill | Description |
|-------|-------------|
| `skills/gouv-fr-donnees-ouvertes/` | Données ouvertes SIG |

## Installation

```bash
# Copier les skills dans le répertoire Hermes
cp -r skills/gouv-fr-*/ ~/.hermes/skills/
```

## Vérification

- Chaque skill dans `skills/gouv-fr-*/` contient un `SKILL.md` avec frontmatter YAML
- Tous les noms commencent par `gouv-fr-`
# 🎯 gouv-fr-skills — 27 skills restaurés et corrigés
