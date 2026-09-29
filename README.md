# gouv-fr-skills

Répertoire de skills Hermes pour les projets de la Fabrique Numérique (Mission Interministérielle).

**40 skills**, tous préfixés `gouv-fr-`. Index complet : [`SKILLS.md`](SKILLS.md).

## Origines

- **Cloud Pi Native** — https://cloud-pi-native.fr (déploiement, Helm, ArgoCD)
- **Starter Kit OpenCode** (`dnum-mi/starter-kit-opencode`) — `.agents/skills` + `docs/okf`
- **gouv-fr-code-package-mi** (`ynotopec/gouv-fr-code-package-mi`) — core skills gouv-fr-code
- **IA-Generative/agent-skills** — dépôt privé (non clonable publiquement)
- **Skills locaux gouv-fr** — migrés et renommés, sauvegarde dans `backup-local-skills/`

## Skills

### Architecture

| Skill | Description |
|-------|-------------|
| [`gouv-fr-code-index`](skills/gouv-fr-code-index/SKILL.md) | Index de l'ensemble des skills |
| [`gouv-fr-monorepo-pnpm`](skills/gouv-fr-monorepo-pnpm/SKILL.md) | pnpm workspaces + Turborepo |
| [`gouv-fr-projet-structure`](skills/gouv-fr-projet-structure/SKILL.md) | Structure projet, CLI, OpenCode |
| [`gouv-fr-stack-technique`](skills/gouv-fr-stack-technique/SKILL.md) | Stack technique recommandée (Front/Back/Outils) |

### Workflow & conventions

| Skill | Description |
|-------|-------------|
| [`gouv-fr-adr`](skills/gouv-fr-adr/SKILL.md) | Rédaction d'ADR (Architecture Decision Record) |
| [`gouv-fr-bug-investigation`](skills/gouv-fr-bug-investigation/SKILL.md) | Hypothèses de cause avant tout fix |
| [`gouv-fr-conventions-nommage`](skills/gouv-fr-conventions-nommage/SKILL.md) | Conventions de nommage Fabrique Numérique |
| [`gouv-fr-outils-developpement`](skills/gouv-fr-outils-developpement/SKILL.md) | Git, Docker, pnpm, proto, VS Code, uv |
| [`gouv-fr-repo-init`](skills/gouv-fr-repo-init/SKILL.md) | Démarrer un repo proprement et sans fuite |
| [`gouv-fr-workflow-dev`](skills/gouv-fr-workflow-dev/SKILL.md) | Plan mode, task management |

### Backend

| Skill | Description |
|-------|-------------|
| [`gouv-fr-api-rest`](skills/gouv-fr-api-rest/SKILL.md) | API REST, OpenAPI, Swagger |
| [`gouv-fr-backend-fastify`](skills/gouv-fr-backend-fastify/SKILL.md) | Fastify, NestJS, FastAPI server |

### Frontend / DSFR

| Skill | Description |
|-------|-------------|
| [`gouv-fr-composants-vue`](skills/gouv-fr-composants-vue/SKILL.md) | VueDsfr — composants Vue 3 |
| [`gouv-fr-design-system`](skills/gouv-fr-design-system/SKILL.md) | DSFR — Système de Design de l'État |
| [`gouv-fr-frontend-vue3`](skills/gouv-fr-frontend-vue3/SKILL.md) | Vue 3, Nuxt 3 |
| [`gouv-fr-graphiques-DSFR`](skills/gouv-fr-graphiques-DSFR/SKILL.md) | Graphiques DSFR en web-components |
| [`gouv-fr-pictogrammes-DSFR`](skills/gouv-fr-pictogrammes-DSFR/SKILL.md) | Pictogrammes, icônes, visuels officiels |
| [`gouv-fr-templates-email`](skills/gouv-fr-templates-email/SKILL.md) | Templates email DSFR |

### Qualité & conformité

| Skill | Description |
|-------|-------------|
| [`gouv-fr-audit-conformite`](skills/gouv-fr-audit-conformite/SKILL.md) | Audit de conformité d'une application |
| [`gouv-fr-code-quality`](skills/gouv-fr-code-quality/SKILL.md) | Grille de contrôle qualité (code généré IA) |
| [`gouv-fr-compliance-rgaa`](skills/gouv-fr-compliance-rgaa/SKILL.md) | RGAA, DSFR, RGPD |
| [`gouv-fr-cookies-rgpd`](skills/gouv-fr-cookies-rgpd/SKILL.md) | Cookies Tarte au Citron (RGPD) |
| [`gouv-fr-lint-eslint`](skills/gouv-fr-lint-eslint/SKILL.md) | ESLint, Ruff, EditorConfig |
| [`gouv-fr-qualite-code`](skills/gouv-fr-qualite-code/SKILL.md) | Bonnes pratiques, lint, tests |

### Sécurité & audit

| Skill | Description |
|-------|-------------|
| [`gouv-fr-audit-openwebui`](skills/gouv-fr-audit-openwebui/SKILL.md) | Identité SSO des tools derrière OpenWebUI |
| [`gouv-fr-audit-pentest`](skills/gouv-fr-audit-pentest/SKILL.md) | Préparation pen-test & durcissement |
| [`gouv-fr-audit-redteam`](skills/gouv-fr-audit-redteam/SKILL.md) | Red-team / prompt-injection LLM |
| [`gouv-fr-audit-safety`](skills/gouv-fr-audit-safety/SKILL.md) | Ouvrir une base de code sans risque |
| [`gouv-fr-dat-homologation`](skills/gouv-fr-dat-homologation/SKILL.md) | Pré-remplissage DAT (homologation MirAI) |
| [`gouv-fr-dat-word`](skills/gouv-fr-dat-word/SKILL.md) | Rendu .docx ministériel (DAT) |
| [`gouv-fr-securite`](skills/gouv-fr-securite/SKILL.md) | Secrets, gitleaks, SQL, TLS, isolation VM |

### DevOps & déploiement

| Skill | Description |
|-------|-------------|
| [`gouv-fr-deployment-cloud-pi-native`](skills/gouv-fr-deployment-cloud-pi-native/SKILL.md) | Déploiement Cloud Pi Native (console, pipeline, ArgoCD) |
| [`gouv-fr-deployment-docker-k8s`](skills/gouv-fr-deployment-docker-k8s/SKILL.md) | Docker rootless, K8s securityContext |
| [`gouv-fr-github-actions-ci`](skills/gouv-fr-github-actions-ci/SKILL.md) | CI GitHub Actions minimale |
| [`gouv-fr-github-actions-reusable`](skills/gouv-fr-github-actions-reusable/SKILL.md) | Workflows fabnum-cicd réutilisables |
| [`gouv-fr-helm-chart`](skills/gouv-fr-helm-chart/SKILL.md) | Helm chart CPiN (OpenShift, Kyverno) |
| [`gouv-fr-repo-cicd`](skills/gouv-fr-repo-cicd/SKILL.md) | Brancher un projet sur la CI/CD CPiN |
| [`gouv-fr-service-names`](skills/gouv-fr-service-names/SKILL.md) | Anti-régression des noms de services mcr |
| [`gouv-fr-smoke-test`](skills/gouv-fr-smoke-test/SKILL.md) | Smoke-test pipeline mirai-mesreunions |

### Données

| Skill | Description |
|-------|-------------|
| [`gouv-fr-donnees-ouvertes`](skills/gouv-fr-donnees-ouvertes/SKILL.md) | Données ouvertes publiques du SIG |

## Installation

```bash
cp -r skills/gouv-fr-*/ ~/.hermes/skills/gouv-fr/
```

## Vérification

- Chaque skill dans `skills/gouv-fr-*/` contient un `SKILL.md` avec frontmatter YAML valide
- Tous les noms commencent par `gouv-fr-` et correspondent au champ `name:`
- Les références croisées (`related_skills`, mentions dans le corps) pointent vers des skills existants
- Exemple d'application conforme : `examples/test-app-verification/`

Voir [`REVIEW.md`](REVIEW.md) pour le rapport de revue complet.

## Workflow

Voir [`WORKFLOW.md`](WORKFLOW.md) — règle d'or : `bash .github/workflows/save-workflow.sh "<motif>"` avant tout gros changement.
