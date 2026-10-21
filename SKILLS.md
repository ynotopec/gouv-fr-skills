# Index des skills fr-gov

**42 skills** répartis en **7 groupes**, sous `skills/fr-gov/<groupe>/<skill>/`.

Les skills propres aux pratiques, plateformes ou référentiels publics français
portent le préfixe `fr-gov-` ; les procédures réutilisables restent sans préfixe.
Un nom ne répète jamais celui de son groupe parent.

## Sécurité & audit (`security`)

Guides de référence, audits de sécurité et durcissement applicatif.

| Skill | Description |
|-----------|-------------|
| [`fr-gov-find-cybersecurity-guide`](skills/fr-gov/security/fr-gov-find-cybersecurity-guide/SKILL.md) | ANSSI publications, topic search, source citations |
| [`harden-repo-before-pentest`](skills/fr-gov/security/harden-repo-before-pentest/SKILL.md) | OWASP Top 10, pre-exposure audit, security remediation |
| [`audit-llm-tool-identity`](skills/fr-gov/security/audit-llm-tool-identity/SKILL.md) | SSO subject propagation, per-user vault, session isolation |
| [`audit-repo-safety`](skills/fr-gov/security/audit-repo-safety/SKILL.md) | Unknown repository, auto-execution, secret leak history |
| [`fr-gov-secure-coding-rules`](skills/fr-gov/security/fr-gov-secure-coding-rules/SKILL.md) | Mandatory Gitleaks, synthetic fixtures, TLS, SQL safety |
| [`redteam-llm-prompt-injection`](skills/fr-gov/security/redteam-llm-prompt-injection/SKILL.md) | LLM01, jailbreaks, canary exfiltration, guard evaluation |

## Développement & code (`code`)

Conventions, architecture, backend, frontend, outillage et workflow de développement.

| Skill | Description |
|-----------|-------------|
| [`write-adr`](skills/fr-gov/code/write-adr/SKILL.md) | Architecture decisions, alternatives, trade-offs |
| [`fr-gov-rest-api-conventions`](skills/fr-gov/code/fr-gov-rest-api-conventions/SKILL.md) | OpenAPI, HTTP status codes, pagination, error responses |
| [`fr-gov-scaffold-backend-api`](skills/fr-gov/code/fr-gov-scaffold-backend-api/SKILL.md) | Fastify, NestJS, FastAPI, logging, error handling |
| [`investigate-bug`](skills/fr-gov/code/investigate-bug/SKILL.md) | Root cause hypotheses, reproduction, fallback plan |
| [`review-code`](skills/fr-gov/code/review-code/SKILL.md) | PR review, technical debt, evidence, verdict |
| [`fr-gov-project-conventions`](skills/fr-gov/code/fr-gov-project-conventions/SKILL.md) | Naming, TypeScript strict, branches, commit conventions |
| [`fr-gov-build-vue-frontend`](skills/fr-gov/code/fr-gov-build-vue-frontend/SKILL.md) | Nuxt scaffolding, composables, frontend tests |
| [`fr-gov-configure-linting`](skills/fr-gov/code/fr-gov-configure-linting/SKILL.md) | ESLint flat config, Ruff, EditorConfig, typography |
| [`fr-gov-set-up-pnpm-monorepo`](skills/fr-gov/code/fr-gov-set-up-pnpm-monorepo/SKILL.md) | Workspaces, Turborepo, shared packages, build cache |
| [`fr-gov-install-dev-tools`](skills/fr-gov/code/fr-gov-install-dev-tools/SKILL.md) | Git, Docker, pnpm, proto, uv, environment diagnostics |
| [`fr-gov-set-up-project-layout`](skills/fr-gov/code/fr-gov-set-up-project-layout/SKILL.md) | OpenCode integration, project files, environment variables |
| [`init-repo`](skills/fr-gov/code/init-repo/SKILL.md) | New repository, gitignore, local secret blocking |
| [`fr-gov-choose-tech-stack`](skills/fr-gov/code/fr-gov-choose-tech-stack/SKILL.md) | Approved frameworks, Prisma, toolchain versions |
| [`detect-stale-service-names`](skills/fr-gov/code/detect-stale-service-names/SKILL.md) | Rename regressions, manifests, old-to-new mapping |
| [`ship-a-dev-task`](skills/fr-gov/code/ship-a-dev-task/SKILL.md) | Proportional workflow, implementation, checks, delivery |

## Conformité & documentation (`compliance`)

Conformité réglementaire, protection des données et production des documents d'homologation.

| Skill | Description |
|-----------|-------------|
| [`fr-gov-audit-app-compliance`](skills/fr-gov/compliance/fr-gov-audit-app-compliance/SKILL.md) | Application audit, applicable rules, evidence, gaps |
| [`fr-gov-configure-cookie-consent`](skills/fr-gov/compliance/fr-gov-configure-cookie-consent/SKILL.md) | Tarte au Citron, third-party cookies, consent theme |
| [`fr-gov-fill-technical-architecture-doc`](skills/fr-gov/compliance/fr-gov-fill-technical-architecture-doc/SKILL.md) | MirAI DAT, repository evidence, Markdown template |
| [`fr-gov-render-technical-architecture-docx`](skills/fr-gov/compliance/fr-gov-render-technical-architecture-docx/SKILL.md) | MirAI DAT, ministerial Word template, typography |
| [`fr-gov-check-web-compliance`](skills/fr-gov/compliance/fr-gov-check-web-compliance/SKILL.md) | RGAA accessibility, DSFR interface, GDPR checklist |

## Données (`data`)

Consommation des APIs de données ouvertes et schémas du SIG.

| Skill | Description |
|-----------|-------------|
| [`fr-gov-query-open-data-api`](skills/fr-gov/data/fr-gov-query-open-data-api/SKILL.md) | data.gouv.fr, Tabular CSV, datasets, usage metrics |
| [`fr-gov-query-public-communication-data`](skills/fr-gov/data/fr-gov-query-public-communication-data/SKILL.md) | Press releases, ministers, public figures, JSONL schemas |

## DSFR & design system (`design-system`)

Design system de l'État : composants, web-components, pictogrammes et templates.

| Skill | Description |
|-----------|-------------|
| [`fr-gov-build-design-system-charts`](skills/fr-gov/design-system/fr-gov-build-design-system-charts/SKILL.md) | DSFR Chart, statistical web components, accessible data |
| [`fr-gov-set-up-design-system`](skills/fr-gov/design-system/fr-gov-set-up-design-system/SKILL.md) | DSFR install, CSS assets, HTML checks, NPM or CDN |
| [`fr-gov-add-design-system-icons`](skills/fr-gov/design-system/fr-gov-add-design-system-icons/SKILL.md) | DSFR pictograms, SVG artwork, official icon classes |
| [`fr-gov-build-react-design-system`](skills/fr-gov/design-system/fr-gov-build-react-design-system/SKILL.md) | react-dsfr, Next.js App Router, theme flash prevention |
| [`fr-gov-build-design-system-emails`](skills/fr-gov/design-system/fr-gov-build-design-system-emails/SKILL.md) | DSFR Mail, HTML templates, Outlook, responsive layout |
| [`fr-gov-build-vue-design-system`](skills/fr-gov/design-system/fr-gov-build-vue-design-system/SKILL.md) | VueDsfr components, SFC imports, Nuxt integration |

## DevOps & déploiement (`devops`)

Intégration continue, conteneurs, Kubernetes, déploiement Cloud Pi Native et tests de fumée.

| Skill | Description |
|-----------|-------------|
| [`fr-gov-set-up-cloud-pi-native-cicd`](skills/fr-gov/devops/fr-gov-set-up-cloud-pi-native-cicd/SKILL.md) | fabnum-cicd setup, workflow pinning, mirror prerequisites |
| [`fr-gov-deploy-to-cloud-pi-native`](skills/fr-gov/devops/fr-gov-deploy-to-cloud-pi-native/SKILL.md) | DSO console, GitLab mirror, ArgoCD, Vault, Kyverno |
| [`fr-gov-containerize-app-for-k8s`](skills/fr-gov/devops/fr-gov-containerize-app-for-k8s/SKILL.md) | Rootless Docker, multi-stage builds, OpenShift UID |
| [`fr-gov-set-up-github-actions-ci`](skills/fr-gov/devops/fr-gov-set-up-github-actions-ci/SKILL.md) | Basic lint-test-build pipeline, CI strategy |
| [`fr-gov-write-digital-factory-workflows`](skills/fr-gov/devops/fr-gov-write-digital-factory-workflows/SKILL.md) | fabnum-cicd YAML, scans, release-please, Helm publishing |
| [`fr-gov-create-helm-chart`](skills/fr-gov/devops/fr-gov-create-helm-chart/SKILL.md) | CPiN values, Kyverno rules, MIOM labels, Vault secrets |
| [`smoke-test-api`](skills/fr-gov/devops/smoke-test-api/SKILL.md) | Resource listing, media download, async job, credentials |

## LaSuite (`lasuite`)

Interfaces React pour les applications LaSuite.

| Skill | Description |
|-----------|-------------|
| [`fr-gov-build-collab-suite-ui`](skills/fr-gov/lasuite/fr-gov-build-collab-suite-ui/SKILL.md) | LaSuite, Cunningham, React sharing and navigation |

---

## Sources

- **Cloud Pi Native** — https://cloud-pi-native.fr
- **starter-kit-opencode** — `dnum-mi/starter-kit-opencode` (`.agents/skills` + `docs/okf`)
- **gouv-fr-code-package-mi** — https://github.com/ynotopec/gouv-fr-code-package-mi
- **IA-Generative/agent-skills** — dépôt privé (non clonable publiquement)
- **etalab-ia/skills** — https://github.com/etalab-ia/skills (4 skills adaptées : fr-gov-build-react-design-system, fr-gov-build-collab-suite-ui, fr-gov-find-cybersecurity-guide, fr-gov-query-open-data-api)
- **Skills locaux gouv-fr** — migrés et renommés (voir `backup-local-skills/`)

Voir [`UPSTREAM.md`](UPSTREAM.md) pour la correspondance avec l'upstream.
