# Index des skills gouv-fr

**43 skills** répartis en **7 groupes**, sous `skills/gouv-fr/<groupe>/<skill>/`.

Le nom d'un skill ne porte pas le préfixe `gouv-fr-` : il ne doit pas répéter
le nom de son dossier parent. Le groupe suffit à le qualifier.

## Sécurité & audit (`securite`)

Guides de référence, audits de sécurité et durcissement applicatif.

| Skill | Description |
|-----------|-------------|
| [`find-anssi-guide`](skills/gouv-fr/securite/find-anssi-guide/SKILL.md) | Trouve et cite le bon guide ANSSI. |
| [`harden-repo-before-pentest`](skills/gouv-fr/securite/harden-repo-before-pentest/SKILL.md) | Durcit un dépôt avant pen-test (OWASP Top 10). |
| [`audit-llm-tool-identity`](skills/gouv-fr/securite/audit-llm-tool-identity/SKILL.md) | Vérifie l'identité SSO des outils LLM per-user. |
| [`audit-repo-safety`](skills/gouv-fr/securite/audit-repo-safety/SKILL.md) | Vérifie qu'un dépôt peut être ouvert sans risque. |
| [`secure-coding-rules`](skills/gouv-fr/securite/secure-coding-rules/SKILL.md) | Règles de sécurité à appliquer en écrivant du code. |
| [`redteam-llm-prompt-injection`](skills/gouv-fr/securite/redteam-llm-prompt-injection/SKILL.md) | Mène un red-team prompt-injection contre un LLM. |

## Développement & code (`code`)

Conventions, architecture, backend, frontend, outillage et workflow de développement.

| Skill | Description |
|-----------|-------------|
| [`write-adr`](skills/gouv-fr/code/write-adr/SKILL.md) | Trace une décision d'architecture en ADR. |
| [`rest-api-conventions`](skills/gouv-fr/code/rest-api-conventions/SKILL.md) | Conventions REST, OpenAPI et tests d'API. |
| [`scaffold-backend-api`](skills/gouv-fr/code/scaffold-backend-api/SKILL.md) | Échafaude une API Fastify, NestJS ou FastAPI. |
| [`investigate-bug`](skills/gouv-fr/code/investigate-bug/SKILL.md) | Éprouve 2-3 hypothèses de cause avant de corriger. |
| [`review-code`](skills/gouv-fr/code/review-code/SKILL.md) | Revue de code et dette, avec preuves et verdict. |
| [`project-conventions`](skills/gouv-fr/code/project-conventions/SKILL.md) | Nommage et architecture d'un projet Fabrique Numérique. |
| [`build-vue-frontend`](skills/gouv-fr/code/build-vue-frontend/SKILL.md) | Frontend Vue 3 ou Nuxt 3 conforme au DSFR. |
| [`configure-linting`](skills/gouv-fr/code/configure-linting/SKILL.md) | Configure ESLint, Ruff et EditorConfig. |
| [`set-up-pnpm-monorepo`](skills/gouv-fr/code/set-up-pnpm-monorepo/SKILL.md) | Monorepo pnpm workspaces et Turborepo. |
| [`install-dev-tools`](skills/gouv-fr/code/install-dev-tools/SKILL.md) | Installe Git, Docker, pnpm, uv, VS Code et gh. |
| [`set-up-project-layout`](skills/gouv-fr/code/set-up-project-layout/SKILL.md) | Layout de dépôt, agent de code et variables d'env. |
| [`init-repo`](skills/gouv-fr/code/init-repo/SKILL.md) | Initialise un dépôt avec anti-fuite git et private/. |
| [`choose-tech-stack`](skills/gouv-fr/code/choose-tech-stack/SKILL.md) | Stack recommandée pour une application de l'État. |
| [`detect-stale-service-names`](skills/gouv-fr/code/detect-stale-service-names/SKILL.md) | Détecte le retour d'anciens noms de services. |
| [`ship-a-dev-task`](skills/gouv-fr/code/ship-a-dev-task/SKILL.md) | Organise une tâche de dev, un correctif ou une PR. |

## Conformité & documentation (`conformite`)

Conformité réglementaire, protection des données et production des documents d'homologation.

| Skill | Description |
|-----------|-------------|
| [`audit-skill-compliance`](skills/gouv-fr/conformite/audit-skill-compliance/SKILL.md) | Audite la conformité d'une app aux skills gouv-fr. |
| [`configure-cookie-consent`](skills/gouv-fr/conformite/configure-cookie-consent/SKILL.md) | Gère les cookies d'un site DSFR avec Tarte au Citron. |
| [`fill-dat-form`](skills/gouv-fr/conformite/fill-dat-form/SKILL.md) | Remplit un DAT depuis le code et les manifestes. |
| [`render-dat-docx`](skills/gouv-fr/conformite/render-dat-docx/SKILL.md) | Rend un DAT en Word au modèle ministériel. |
| [`check-web-compliance`](skills/gouv-fr/conformite/check-web-compliance/SKILL.md) | Checklist RGAA, DSFR et RGPD avant livraison. |

## Données (`data`)

Consommation des APIs de données ouvertes et schémas du SIG.

| Skill | Description |
|-----------|-------------|
| [`query-french-open-data-api`](skills/gouv-fr/data/query-french-open-data-api/SKILL.md) | Interroge les APIs de data.gouv.fr et la Tabular. |
| [`fetch-open-geodata`](skills/gouv-fr/data/fetch-open-geodata/SKILL.md) | Données ouvertes du SIG en JSONL et schémas. |

## DSFR & design system (`dsfr`)

Design system de l'État : composants, web-components, pictogrammes et templates.

| Skill | Description |
|-----------|-------------|
| [`build-french-state-design-system-charts`](skills/gouv-fr/dsfr/build-french-state-design-system-charts/SKILL.md) | Graphiques DSFR en web-components Vue.js. |
| [`set-up-french-state-design-system`](skills/gouv-fr/dsfr/set-up-french-state-design-system/SKILL.md) | Installe et vérifie le DSFR d'un projet. |
| [`add-french-state-design-system-icons`](skills/gouv-fr/dsfr/add-french-state-design-system-icons/SKILL.md) | Intègre pictogrammes et icônes officiels du DSFR. |
| [`build-react-french-state-design-system`](skills/gouv-fr/dsfr/build-react-french-state-design-system/SKILL.md) | Interfaces React avec @codegouvfr/react-dsfr. |
| [`build-french-state-design-system-emails`](skills/gouv-fr/dsfr/build-french-state-design-system-emails/SKILL.md) | Génère des templates email DSFR pour l'État. |
| [`build-vue-french-state-design-system`](skills/gouv-fr/dsfr/build-vue-french-state-design-system/SKILL.md) | Composants Vue 3 DSFR avec VueDsfr. |

## DevOps & déploiement (`devops`)

Intégration continue, conteneurs, Kubernetes, déploiement Cloud Pi Native et tests de fumée.

| Skill | Description |
|-----------|-------------|
| [`set-up-cloud-pi-native-cicd`](skills/gouv-fr/devops/set-up-cloud-pi-native-cicd/SKILL.md) | Pose la CI/CD CPiN via les workflows fabnum-cicd. |
| [`deploy-to-cloud-pi-native`](skills/gouv-fr/devops/deploy-to-cloud-pi-native/SKILL.md) | Déploie une app sur Cloud Pi Native (DSO, ArgoCD). |
| [`containerize-app-for-k8s`](skills/gouv-fr/devops/containerize-app-for-k8s/SKILL.md) | Docker rootless et K8s pour Cloud Pi Native. |
| [`set-up-github-actions-ci`](skills/gouv-fr/devops/set-up-github-actions-ci/SKILL.md) | Pose une CI GitHub Actions de base. |
| [`write-digital-factory-cicd-workflows`](skills/gouv-fr/devops/write-digital-factory-cicd-workflows/SKILL.md) | Écrit ci.yml et cd.yml sur fabnum-cicd. |
| [`create-helm-chart`](skills/gouv-fr/devops/create-helm-chart/SKILL.md) | Crée un chart Helm pour Cloud Pi Native. |
| [`smoke-test-api`](skills/gouv-fr/devops/smoke-test-api/SKILL.md) | Smoke-teste une API sans exposer de secret. |

## LaSuite (`lasuite`)

Interfaces React pour les applications LaSuite.

| Skill | Description |
|-----------|-------------|
| [`build-french-collab-suite-ui`](skills/gouv-fr/lasuite/build-french-collab-suite-ui/SKILL.md) | Interfaces React LaSuite avec @gouvfr-lasuite/ui-kit. |

---

## Sources

- **Cloud Pi Native** — https://cloud-pi-native.fr
- **starter-kit-opencode** — `dnum-mi/starter-kit-opencode` (`.agents/skills` + `docs/interne`)
- **gouv-fr-code-package-mi** — https://github.com/ynotopec/gouv-fr-code-package-mi
- **organisation-archive/agent-skills** — dépôt privé (non clonable publiquement)
- **etalab-ia/skills** — https://github.com/etalab-ia/skills (4 skills adaptées : build-react-french-state-design-system, build-french-collab-suite-ui, find-anssi-guide, query-french-open-data-api)
- **Skills locaux gouv-fr** — migrés et renommés (voir `backup-local-skills/`)

Voir [`UPSTREAM.md`](UPSTREAM.md) pour la correspondance avec l'upstream.
