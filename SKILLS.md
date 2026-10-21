# Index des skills gouv-fr

**43 skills** répartis en **7 groupes**, sous `skills/gouv-fr/<groupe>/<skill>/`.

Le nom d'un skill ne porte pas le préfixe `gouv-fr-` : il ne doit pas répéter
le nom de son dossier parent. Le groupe suffit à le qualifier.

## Sécurité & audit (`securite`)

Guides de référence, audits de sécurité et durcissement applicatif.

| Skill | Description |
|-----------|-------------|
| [`anssi-guides`](skills/gouv-fr/securite/anssi-guides/SKILL.md) | Trouve et cite le bon guide ANSSI. |
| [`audit-durcissement`](skills/gouv-fr/securite/audit-durcissement/SKILL.md) | Durcit un dépôt avant pen-test (OWASP Top 10). |
| [`audit-identite-outils-llm`](skills/gouv-fr/securite/audit-identite-outils-llm/SKILL.md) | Vérifie l'identité SSO des outils LLM per-user. |
| [`audit-securite-depot`](skills/gouv-fr/securite/audit-securite-depot/SKILL.md) | Vérifie qu'un dépôt peut être ouvert sans risque. |
| [`developpement-securise`](skills/gouv-fr/securite/developpement-securise/SKILL.md) | Règles de sécurité à appliquer en écrivant du code. |
| [`redteam-llm`](skills/gouv-fr/securite/redteam-llm/SKILL.md) | Mène un red-team prompt-injection contre un LLM. |

## Développement & code (`code`)

Conventions, architecture, backend, frontend, outillage et workflow de développement.

| Skill | Description |
|-----------|-------------|
| [`adr`](skills/gouv-fr/code/adr/SKILL.md) | Trace une décision d'architecture en ADR. |
| [`api-rest`](skills/gouv-fr/code/api-rest/SKILL.md) | Conventions REST, OpenAPI et tests d'API. |
| [`backend-api`](skills/gouv-fr/code/backend-api/SKILL.md) | Échafaude une API Fastify, NestJS ou FastAPI. |
| [`bug-investigation`](skills/gouv-fr/code/bug-investigation/SKILL.md) | Éprouve 2-3 hypothèses de cause avant de corriger. |
| [`code-quality`](skills/gouv-fr/code/code-quality/SKILL.md) | Revue de code et dette, avec preuves et verdict. |
| [`conventions-developpement`](skills/gouv-fr/code/conventions-developpement/SKILL.md) | Nommage et architecture d'un projet Fabrique Numérique. |
| [`frontend-vue3`](skills/gouv-fr/code/frontend-vue3/SKILL.md) | Frontend Vue 3 ou Nuxt 3 conforme au DSFR. |
| [`lint-format`](skills/gouv-fr/code/lint-format/SKILL.md) | Configure ESLint, Ruff et EditorConfig. |
| [`monorepo-pnpm`](skills/gouv-fr/code/monorepo-pnpm/SKILL.md) | Monorepo pnpm workspaces et Turborepo. |
| [`outils-developpement`](skills/gouv-fr/code/outils-developpement/SKILL.md) | Installe Git, Docker, pnpm, uv, VS Code et gh. |
| [`projet-structure`](skills/gouv-fr/code/projet-structure/SKILL.md) | Layout de dépôt, agent de code et variables d'env. |
| [`repo-init`](skills/gouv-fr/code/repo-init/SKILL.md) | Initialise un dépôt avec anti-fuite git et private/. |
| [`skills-router`](skills/gouv-fr/code/skills-router/SKILL.md) | Choisit les skills gouv-fr adaptés à la demande. |
| [`stack-technique`](skills/gouv-fr/code/stack-technique/SKILL.md) | Stack recommandée pour une application de l'État. |
| [`verification-renommage-services`](skills/gouv-fr/code/verification-renommage-services/SKILL.md) | Détecte le retour d'anciens noms de services. |
| [`workflow-dev`](skills/gouv-fr/code/workflow-dev/SKILL.md) | Organise une tâche de dev, un correctif ou une PR. |

## Conformité & documentation (`conformite`)

Conformité réglementaire, protection des données et production des documents d'homologation.

| Skill | Description |
|-----------|-------------|
| [`audit-conformite`](skills/gouv-fr/conformite/audit-conformite/SKILL.md) | Audite la conformité d'une app aux skills gouv-fr. |
| [`cookies-rgpd`](skills/gouv-fr/conformite/cookies-rgpd/SKILL.md) | Gère les cookies d'un site DSFR avec Tarte au Citron. |
| [`document-homologation`](skills/gouv-fr/conformite/document-homologation/SKILL.md) | Remplit un DAT MirAI depuis le code et les manifestes. |
| [`homologation-word`](skills/gouv-fr/conformite/homologation-word/SKILL.md) | Rend un DAT MirAI en Word au modèle ministériel. |
| [`regles-conformite-web`](skills/gouv-fr/conformite/regles-conformite-web/SKILL.md) | Checklist RGAA, DSFR et RGPD avant livraison. |

## Données (`data`)

Consommation des APIs de données ouvertes et schémas du SIG.

| Skill | Description |
|-----------|-------------|
| [`datagouv-apis`](skills/gouv-fr/data/datagouv-apis/SKILL.md) | Interroge les APIs de data.gouv.fr et la Tabular. |
| [`donnees-communication-publique`](skills/gouv-fr/data/donnees-communication-publique/SKILL.md) | Données ouvertes du SIG en JSONL et schémas. |

## DSFR & design system (`dsfr`)

Design system de l'État : composants, web-components, pictogrammes et templates.

| Skill | Description |
|-----------|-------------|
| [`graphiques-dsfr`](skills/gouv-fr/dsfr/graphiques-dsfr/SKILL.md) | Graphiques DSFR en web-components Vue.js. |
| [`integration-dsfr`](skills/gouv-fr/dsfr/integration-dsfr/SKILL.md) | Installe et vérifie le DSFR d'un projet. |
| [`pictogrammes-dsfr`](skills/gouv-fr/dsfr/pictogrammes-dsfr/SKILL.md) | Intègre pictogrammes et icônes officiels du DSFR. |
| [`react-dsfr`](skills/gouv-fr/dsfr/react-dsfr/SKILL.md) | Interfaces React avec @codegouvfr/react-dsfr. |
| [`templates-email-dsfr`](skills/gouv-fr/dsfr/templates-email-dsfr/SKILL.md) | Génère des templates email DSFR pour l'État. |
| [`vue-dsfr`](skills/gouv-fr/dsfr/vue-dsfr/SKILL.md) | Composants Vue 3 DSFR avec VueDsfr. |

## DevOps & déploiement (`devops`)

Intégration continue, conteneurs, Kubernetes, déploiement Cloud Pi Native et tests de fumée.

| Skill | Description |
|-----------|-------------|
| [`cicd-cloud-pi-native`](skills/gouv-fr/devops/cicd-cloud-pi-native/SKILL.md) | Pose la CI/CD CPiN via les workflows fabnum-cicd. |
| [`deployment-cloud-pi-native`](skills/gouv-fr/devops/deployment-cloud-pi-native/SKILL.md) | Déploie une app sur Cloud Pi Native (DSO, ArgoCD). |
| [`deployment-docker-k8s`](skills/gouv-fr/devops/deployment-docker-k8s/SKILL.md) | Docker rootless et K8s pour Cloud Pi Native. |
| [`github-actions-ci`](skills/gouv-fr/devops/github-actions-ci/SKILL.md) | Pose une CI GitHub Actions de base. |
| [`github-actions-reusable`](skills/gouv-fr/devops/github-actions-reusable/SKILL.md) | Écrit ci.yml et cd.yml sur fabnum-cicd. |
| [`helm-chart`](skills/gouv-fr/devops/helm-chart/SKILL.md) | Crée un chart Helm pour Cloud Pi Native. |
| [`smoke-test-api`](skills/gouv-fr/devops/smoke-test-api/SKILL.md) | Smoke-teste une API sans exposer de secret. |

## LaSuite (`lasuite`)

Interfaces React pour les applications LaSuite.

| Skill | Description |
|-----------|-------------|
| [`lasuite-ui-kit`](skills/gouv-fr/lasuite/lasuite-ui-kit/SKILL.md) | Interfaces React LaSuite avec @gouvfr-lasuite/ui-kit. |

---

## Sources

- **Cloud Pi Native** — https://cloud-pi-native.fr
- **starter-kit-opencode** — `dnum-mi/starter-kit-opencode` (`.agents/skills` + `docs/okf`)
- **gouv-fr-code-package-mi** — https://github.com/ynotopec/gouv-fr-code-package-mi
- **IA-Generative/agent-skills** — dépôt privé (non clonable publiquement)
- **etalab-ia/skills** — https://github.com/etalab-ia/skills (4 skills adaptées : react-dsfr, lasuite-ui-kit, anssi-guides, datagouv-apis)
- **Skills locaux gouv-fr** — migrés et renommés (voir `backup-local-skills/`)

Voir [`UPSTREAM.md`](UPSTREAM.md) pour la correspondance avec l'upstream.
