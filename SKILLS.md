# Index des skills gouv-fr

**43 skills** répartis en **7 groupes**, sous `skills/gouv-fr/<groupe>/<skill>/`.

Le nom d'un skill ne porte pas le préfixe `gouv-fr-` : il ne doit pas répéter
le nom de son dossier parent. Le groupe suffit à le qualifier.

## Sécurité & audit (`securite`)

Guides de référence, audits de sécurité et durcissement applicatif.

| Skill | Description |
|-----------|-------------|
| [`anssi-guides`](skills/gouv-fr/securite/anssi-guides/SKILL.md) | Trouver et consulter le bon guide ANSSI via l'API MesServicesCyber : catalogue des guides français et des publications anglaises sans équivalent, aiguillage et citation de la source. Sécurité hors développement (réseau, pare-feu, Active Directory, Wi-Fi, virtualisation, gestion de crise, EBIOS, cryptographie post-quantique). |
| [`audit-openwebui`](skills/gouv-fr/securite/audit-openwebui/SKILL.md) | Audite et conçoit les outils per-user derrière OpenWebUI (ou autre passerelle LLM/MCP) — continuité d'identité SSO (le sub Keycloak de bout en bout), coffre-fort de credentials (MyVault), contrôle d'accès et hygiène de session. Vérifie que l'identité de l'utilisateur arrive de façon FIABLE jusqu'au tool et au coffre-fort, sans mélange de sessions. Lecture seule par défaut : produit un verdict + un plan de remédiation exécutable en mode plan. |
| [`audit-durcissement`](skills/gouv-fr/securite/audit-durcissement/SKILL.md) | Audit & durcissement sécurité avant pen-test. Identifie et corrige les failles évidentes/classiques (OWASP Top 10 + OWASP LLM Top 10, dont prompt injection) du repo courant, sans casser le fonctionnement. À lancer avant tout test d'intrusion ou exposition publique. |
| [`redteam-llm`](skills/gouv-fr/securite/redteam-llm/SKILL.md) | Mène une campagne red-team / prompt-injection (OWASP LLM01) contre un service adossé à un LLM — wizard, route /api, agent, connecteur MCP. Mesure si la garde bloque les attaques (entrée ET sortie), avec un modèle-juge, et écrit TOUS les rapports dans private/redteam-reports/ (jamais committés). Lecture seule sur le code ; n'exécute que des requêtes de test contre une cible autorisée. |
| [`audit-securite-depot`](skills/gouv-fr/securite/audit-securite-depot/SKILL.md) | Vérifie qu'une base de code peut être ouverte / travaillée sans risque AVANT de s'y plonger. Trois contrôles — (1) ouverture sûre (aucun exécutable auto au open : hooks git, tâches VSCode, scripts de lifecycle, devcontainer) ; (2) anti-leak en place (gitleaks/pre-commit, .gitignore durci) ; (3) rien de sensible n'a fuité (secrets & infos privées dans le working tree, l'historique et les messages/heads de commit). Lecture seule : produit un rapport et le PLAN de remédiation exécutable en mode plan. |
| [`developpement-securise`](skills/gouv-fr/securite/developpement-securise/SKILL.md) | Sécurité : secrets, gitleaks, SQL, TLS, isolation VM. |

## Développement & code (`code`)

Conventions, architecture, backend, frontend, outillage et workflow de développement.

| Skill | Description |
|-----------|-------------|
| [`adr`](skills/gouv-fr/code/adr/SKILL.md) | Rédige une nouvelle ADR (Architecture Decision Record) au format interne. Utiliser quand une décision d'archi a été prise et doit être tracée (choix de backend, refonte, breaking change, trade-off entre options). |
| [`api-rest`](skills/gouv-fr/code/api-rest/SKILL.md) | Conventions API RESTful, OpenAPI, Swagger et tests d'API pour Fabrique Numérique. |
| [`backend-api`](skills/gouv-fr/code/backend-api/SKILL.md) | Construit un serveur pour la Fabrique Numérique (Fastify, NestJS, FastAPI) — échafaudage, structure, journalisation, gestion d'erreurs, doc OpenAPI et tests. |
| [`bug-investigation`](skills/gouv-fr/code/bug-investigation/SKILL.md) | Force 2-3 hypothèses de cause + plan B avant tout fix de bug. Utiliser sur tout bug signalé, régression, comportement inattendu, ou avant de toucher au code "pour corriger". Inspiré du guide Karpathy §1. |
| [`skills-router`](skills/gouv-fr/code/skills-router/SKILL.md) | Choisir les skills gouv-fr pertinents pour une tâche de construction, audit ou déploiement ; utiliser pour une demande générale ou couvrant plusieurs domaines. |
| [`code-quality`](skills/gouv-fr/code/code-quality/SKILL.md) | Revoir une PR ou du code, mesurer la dette ou guider une correction avec preuves, verdict et contrôles adaptés au projet. |
| [`conventions-nommage`](skills/gouv-fr/code/conventions-nommage/SKILL.md) | Applique les conventions de nommage et d'architecture d'un projet Fabrique Numérique — dossiers, fichiers, TypeScript, API RESTful, lint, qualité, déploiement et documentation. |
| [`deployment-docker-k8s`](skills/gouv-fr/code/deployment-docker-k8s/SKILL.md) | Docker rootless, K8s securityContext, multi-stage, tags, local K8s dev. Pour Helm : helm-chart. Pour CPiN console/ArgoCD : deployment-cloud-pi-native. |
| [`frontend-vue3`](skills/gouv-fr/code/frontend-vue3/SKILL.md) | Construit un frontend Vue 3 / Nuxt 3 pour la Fabrique Numérique — conformité DSFR, échafaudage VueDsfr, composables (toaster) et mise en place des tests. |
| [`github-actions-ci`](skills/gouv-fr/code/github-actions-ci/SKILL.md) | Met en place une CI GitHub Actions de base (lint, tests, build) pour un projet Fabrique Numérique, ou aide à choisir entre pipeline maison et workflows réutilisables fabnum-cicd. Pour les workflows réutilisables, releases et synchro Cloud Pi Native, voir github-actions-reusable. |
| [`lint-format`](skills/gouv-fr/code/lint-format/SKILL.md) | Lint et formattage ESLint, Ruff et EditorConfig pour projets Fabrique Numérique. |
| [`monorepo-pnpm`](skills/gouv-fr/code/monorepo-pnpm/SKILL.md) | Architecture monorepo pnpm workspaces et Turborepo : structure, workspaces, turbo.json, cache, filters. |
| [`outils-developpement`](skills/gouv-fr/code/outils-developpement/SKILL.md) | Installation et configuration des outils dev (Git, Docker, pnpm, proto, VS Code, GitHub CLI, uv, zsh). Vérification d'environnement, branches, commits, Docker Compose. |
| [`projet-structure`](skills/gouv-fr/code/projet-structure/SKILL.md) | Structure de projet, intégration agent et variables d'env. |
| [`repo-init`](skills/gouv-fr/code/repo-init/SKILL.md) | Initialise un répertoire vide (ou un projet qui démarre) avec les précautions d'usage — git, .gitignore durci anti-fuite, un dossier private/ gitignoré pour les sorties sensibles, une structure logique lisible par un humain, et un anti-leak LOCAL bloquant (pre-commit gitleaks, binaire, sans licence). À lancer au tout début d'un nouveau repo, avant d'écrire du code ou de committer quoi que ce soit. |
| [`stack-technique`](skills/gouv-fr/code/stack-technique/SKILL.md) | Stack technique recommandée : Front (Vue 3, DSFR), Back (Fastify, NestJS, FastAPI), TS strict, Prisma, ESLint, monorepo. Outils de dev et versions. |
| [`workflow-dev`](skills/gouv-fr/code/workflow-dev/SKILL.md) | Organiser une tâche de développement, correction ou PR : processus proportionné, validation adaptée et suivi durable seulement si utile. |

## Conformité & documentation (`conformite`)

Conformité réglementaire, protection des données et production des documents d'homologation.

| Skill | Description |
|-----------|-------------|
| [`audit-conformite`](skills/gouv-fr/conformite/audit-conformite/SKILL.md) | Auditer la conformité d'une application ou d'une PR aux skills gouv-fr : contrôles adaptés à la stack, preuves et limites, lecture seule sauf correction demandée. |
| [`compliance-rgaa`](skills/gouv-fr/conformite/compliance-rgaa/SKILL.md) | Conformité État : RGAA, DSFR, RGPD. |
| [`cookies-rgpd`](skills/gouv-fr/conformite/cookies-rgpd/SKILL.md) | Gère les cookies d'un site DSFR avec Tarte au Citron. |
| [`document-homologation`](skills/gouv-fr/conformite/document-homologation/SKILL.md) | Pré-remplit un document d'homologation DAT (DAT, et à terme AIPD/dossier d'homologation) à partir du code et des manifestes du repo courant. Le modèle et le prompt de référence versionnés sont embarqués dans cette skill. Lecture seule sur le service, ne jamais inventer ni recopier de valeur réelle. |
| [`homologation-word`](skills/gouv-fr/conformite/homologation-word/SKILL.md) | Rend un document d'homologation DAT (DAT, et à terme AIPD/dossier d'homologation) au format Word (.docx) ministériel, en appliquant le modèle officiel avec typographie française, diagrammes mermaid et mise en page professionnelle. |

## Données (`data`)

Consommation des APIs de données ouvertes et schémas du SIG.

| Skill | Description |
|-----------|-------------|
| [`datagouv-apis`](skills/gouv-fr/data/datagouv-apis/SKILL.md) | Consommer les APIs de la plateforme data.gouv.fr : catalogue, métadonnées de datasets, organisations, téléchargement de fichiers, requêtes de lignes CSV (Tabular API), métriques d'usage (Metrics API) et dataservices (APIs externes). Exploration via MCP ou HTTP. |
| [`donnees-ouvertes`](skills/gouv-fr/data/donnees-ouvertes/SKILL.md) | Données ouvertes publiques du SIG (schémas, JSONL). |

## DSFR & design system (`dsfr`)

Design system de l'État : composants, web-components, pictogrammes et templates.

| Skill | Description |
|-----------|-------------|
| [`composants-vue`](skills/gouv-fr/dsfr/composants-vue/SKILL.md) | Installer et utiliser VueDsfr (composants Vue 3 DSFR). |
| [`design-system`](skills/gouv-fr/dsfr/design-system/SKILL.md) | Installer et vérifier le design system de l'État (DSFR). |
| [`graphiques-dsfr`](skills/gouv-fr/dsfr/graphiques-dsfr/SKILL.md) | Graphiques DSFR en web-components Vue.js (line, bar, pie…). |
| [`pictogrammes-dsfr`](skills/gouv-fr/dsfr/pictogrammes-dsfr/SKILL.md) | Intègre pictogrammes, icônes et visuels officiels du DSFR. |
| [`react-dsfr`](skills/gouv-fr/dsfr/react-dsfr/SKILL.md) | Créer des interfaces React conformes au Design System de l'État avec @codegouvfr/react-dsfr. Setup Next.js App Router (anti-flash thème), routing, icônes, couleurs, composants natifs (pas MUI), patterns de mise en page et de formulaire. |
| [`templates-email`](skills/gouv-fr/dsfr/templates-email/SKILL.md) | Génère des templates email DSFR pour l'État. |

## DevOps & déploiement (`devops`)

Intégration continue, conteneurs, Kubernetes, déploiement Cloud Pi Native et tests de fumée.

| Skill | Description |
|-----------|-------------|
| [`deployment-cloud-pi-native`](skills/gouv-fr/devops/deployment-cloud-pi-native/SKILL.md) | Onboarde et déploie une application sur Cloud Pi Native — console DSO (projet, dépôts, environnements, quotas), sync du mirror, pipeline .gitlab-ci-dso vers Harbor, déploiement GitOps ArgoCD, secrets Vault, rejets Kyverno et diagnostic d'un déploiement bloqué. |
| [`github-actions-reusable`](skills/gouv-fr/devops/github-actions-reusable/SKILL.md) | Écrit ou révise des workflows GitHub Actions ci.yml/cd.yml s'appuyant sur les workflows réutilisables dnum-mi/fabnum-cicd — lint, scans Trivy/Gitleaks, build Docker, release-please, bump et publication du chart Helm, credentials GitHub App et déclencheur sync-cpin vers Cloud Pi Native. |
| [`helm-chart`](skills/gouv-fr/devops/helm-chart/SKILL.md) | Crée ou adapte un chart Helm pour déployer sur Cloud Pi Native (OpenShift + Kyverno) — gabarit this-is-tobi, values par environnement, securityContext et UID, labels MIOM, secrets Vault via extraObjects, tags d'image, versionnage du chart et publication OCI. |
| [`cicd-cloud-pi-native`](skills/gouv-fr/devops/cicd-cloud-pi-native/SKILL.md) | Pose une CI/CD « Cloud Pi Native » sur un projet GitHub existant en APPELANT les workflows réutilisables du dépôt public dnum-mi/fabnum-cicd — pipeline de pull request (lint, scans, build), pipeline de release (release-please, image, synchronisation du miroir GitLab CPiN), épinglage par tag exact et règle Renovate. Ne recopie rien de fabnum-cicd et ne connaît aucun input par cœur — il lit le dépôt au tag résolu à chaque lancement. Lecture seule par défaut — rapport + plan ; n'écrit qu'avec --setup. Ne crée aucun secret, ne pousse rien, n'ouvre aucune PR. |
| [`verification-renommage-services`](skills/gouv-fr/devops/verification-renommage-services/SKILL.md) | Contrôle anti-régression des noms de services renommés. |
| [`smoke-test`](skills/gouv-fr/devops/smoke-test/SKILL.md) | Smoke-test d'une API en lecture et job asynchrone, sans exposer de secret. Vérifie liste, média et job avec un credential injecté dans l'environnement. Le contrat d'API est paramétrable ; à lancer uniquement sur demande explicite (appels réseau vers un environnement réel). |

## LaSuite (`lasuite`)

Interfaces React pour les applications LaSuite.

| Skill | Description |
|-----------|-------------|
| [`lasuite-ui-kit`](skills/gouv-fr/lasuite/lasuite-ui-kit/SKILL.md) | Créer des interfaces React pour les applications LaSuite (Docs, Drive, People, Webinaire, Messagerie) avec @gouvfr-lasuite/ui-kit et @gouvfr-lasuite/cunningham-react. Layout applicatif, navigation, recherche rapide, badges, icônes Material, menus contextuels, partage et invitations. |

---

## Sources

- **Cloud Pi Native** — https://cloud-pi-native.fr
- **starter-kit-opencode** — `dnum-mi/starter-kit-opencode` (`.agents/skills` + `docs/interne`)
- **gouv-fr-code-package-mi** — https://github.com/ynotopec/gouv-fr-code-package-mi
- **organisation-archive/agent-skills** — dépôt privé (non clonable publiquement)
- **etalab-ia/skills** — https://github.com/etalab-ia/skills (4 skills adaptées : react-dsfr, lasuite-ui-kit, anssi-guides, datagouv-apis)
- **Skills locaux gouv-fr** — migrés et renommés (voir `backup-local-skills/`)

Voir [`UPSTREAM.md`](UPSTREAM.md) pour la correspondance avec l'upstream.
