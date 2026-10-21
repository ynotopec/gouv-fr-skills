# Provenance historique des skills

Les noms historiques ci-dessous sont conservés pour attribution. Les identifiants
actuels et la correspondance de migration figurent dans
[`scripts/skill-renames.tsv`](scripts/skill-renames.tsv).

Les skills sont maintenus directement dans `gouv-fr-skills`. Ces sources
documentent l’origine des contenus, sans imposer de validation ou de
synchronisation externe. Toute reprise future est facultative et passe par
une revue locale ; préserver les adaptations et les attributions de licence.

Suivi historique de la correspondance entre nos skills (`gouv-fr-*`) et les skills upstream
(`.agents/skills/<groupe>/`), dont les **noms diffèrent**.

**Dernier upstream vérifié** : commit `9d9cfbf` (2026-09-24)
— *refactor(skills): recentrer ci-cd et deploiement (dev), renvoyer vers le groupe dso (#16)*

## Correspondance des noms

### Groupe `dev`

| Upstream | Notre skill |
|----------|-------------|
| `dev/ci-cd` | `code/github-actions-ci` |
| `dev/conventions-cofabnum` | `code/fr-gov-project-conventions` |
| `dev/deploiement` | `code/deployment-docker-k8s` |
| `dev/environnement-installation` | `code/fr-gov-install-dev-tools` *(fusionné)* |
| `dev/outils-dev` | `code/fr-gov-install-dev-tools` *(fusionné)* |
| `dev/monorepo` | `code/fr-gov-set-up-pnpm-monorepo` |
| `dev/recettes-client` | `code/fr-gov-build-vue-frontend` |
| `dev/recettes-serveur` | `code/backend-fastify` |
| `dev/stack-technique` | `code/fr-gov-choose-tech-stack` |

### Groupe `dso`

| Upstream | Notre skill |
|----------|-------------|
| `dso/cicd-fabnum` | `dso/github-actions-reusable` |
| `dso/deploiement-cpin` | `dso/deployment-cloud-pi-native` |
| `dso/helm-chart-cpin` | `dso/helm-chart` |

## Écarts assumés

- **`dev/outils-dev` + `dev/environnement-installation` fusionnés** en un seul
  skill `code/fr-gov-install-dev-tools`. Les deux contenus upstream sont couverts
  (installation machine, proto, WSL/Homebrew, Git, Docker, pnpm, uv, VS Code).
- **Noms francophones explicites** au lieu des noms courts upstream, pour rester
  lisibles par une personne externe.
- **`dso/index.json`** non repris : c'est un index de groupe propre au dépôt
  upstream, redondant avec notre `SKILLS.md`.

## Fichiers annexes — état historique lors de l’import

| Upstream | Notre emplacement | SHA-256 (12) |
|----------|-------------------|--------------|
| `dso/cicd-fabnum/references/ci.yml` | `dso/github-actions-reusable`/references/ci.yml | `e84207a541ee` |
| `dso/cicd-fabnum/references/cd.yml` | `dso/github-actions-reusable`/references/cd.yml | `070c12d63c60` |
| `dso/cicd-fabnum/references/workflows.md` | `dso/github-actions-reusable`/references/workflows.md | `77602ec42313` |
| `dso/deploiement-cpin/references/depannage.md` | `dso/deployment-cloud-pi-native`/references/depannage.md | `ae57d1362d57` |
| `dso/deploiement-cpin/references/gitlab-ci-dso.yml` | `dso/deployment-cloud-pi-native`/references/gitlab-ci-dso.yml | `30e1acf26acf` |
| `dso/helm-chart-cpin/references/values-cpin.yaml` | `dso/helm-chart`/references/values-cpin.yaml | `8391e8d66f9d` |
| `dso/helm-chart-cpin/references/vault-secret.yaml` | `dso/helm-chart`/references/vault-secret.yaml | `c48cf3c9b14f` |
| `dso/helm-chart-cpin/scripts/check-cpin-rules.py` | `dso/helm-chart`/scripts/check-cpin-rules.py | `f0041b35c5b8` |

## Modifications upstream intégrées

- **#16** `9d9cfbf` — `ci-cd` et `deploiement` recentrés (renvoi vers le groupe
  `dso`) :
  - `code/github-actions-ci` : description, `name: CI` du gabarit, règle
    `@v0.20` / jamais `@main`
  - `code/deployment-docker-k8s` : règle UID OpenShift
    (`chown -R <uid>:0`, `chmod -R g=u`), règle de tag (`latest` bloqué par
    Kyverno, digest), `COPY --from=build`, suppression des sections Helm/CPiN
    déplacées vers le groupe `dso`
  - `dso/helm-chart` : suffixe par type de ressource (`-svc`, `-dep`,
    `-sts`, `-cm`, `-cj`, `-pvc`) et environnement en préfixe
- **#7** `17b887f` — `recettes-client` : setup `@gouvfr/dsfr`, grille/typo/tokens
  DSFR, rappel `getRandomId`
- **#4** `5715782` — `recettes-client` : checklist avant implémentation,
  référence `DsfrInput`, piège Playwright `--no-sandbox` (Onyxia)

## Référentiels externes — non synchronisés

### `etalab-ia/skills` (référentiel Skills de l'État, DINUM/IAE)

**Vérifié** : commit `c791677` (2026-09-29) — 7 skills officielles + `.experimental/`.

**4 skills adaptées** (préfixe `gouv-fr-`, frontmatter canonique du dépôt, `references/` et
`scripts/` repris tels quels, `README.md` source retiré pour rester homogène) :

| Leur skill | Notre skill | Adaptation |
|------------|-------------|------------|
| `fr-gov-build-react-design-system` | `dsfr/fr-gov-build-react-design-system` | intégrale — `references/components.md`, `references/setup.md` |
| `fr-gov-build-collab-suite-ui` | `lasuite/fr-gov-build-collab-suite-ui` | intégrale — `references/{components,cunningham,setup}.md` |
| `fr-gov-find-cybersecurity-guide` | `anssi/anssi-guides` | intégrale — `references/catalogue.md`, `scripts/` (3 fichiers) |
| `fr-gov-query-open-data-api` | `data/fr-gov-query-open-data-api` | intégrale |

**3 skills non reprises** :

| Leur skill | Équivalent chez nous | Raison |
|------------|----------------------|--------|
| `rgaa` | `fr-gov-check-web-compliance` | doublon partiel : notre skill couvre déjà RGAA/DSFR/RGPD en checklist ; leur outil d'audit 106 critères (5 fichiers de référence) n'a pas été repris |
| `securite-developpement` | `security` | doublon partiel : 14 domaines DINUM/ANSSI détaillés, non repris — `fr-gov-find-cybersecurity-guide` y renvoie par URL |
| `usage-ia-agents-etat` | `audit-redteam` | périmètre différent (cadre d'usage vs test d'attaque) |

Compatibilité de nommage : leurs skills n'ont pas de préfixe (`rgaa`, `fr-gov-build-react-design-system`…),
les nôtres aussi — le préfixe `gouv-fr-` a été retiré lors du regroupement en
groupes, pour qu'aucun skill ne porte le nom de son dossier parent. Les deux
jeux coexistent dans Hermes, dans des groupes distincts. Formats de
frontmatter différents (eux : `name` + `description` seuls ; nous : `version`,
`license`, `platforms`, `metadata.hermes`, et `author` pour les skills dont
l'attribution humaine est connue).

Renvois croisés : les liens de `fr-gov-find-cybersecurity-guide` vers la skill upstream
`securite-developpement` pointent vers les URLs GitHub d'`etalab-ia/skills` (les chemins
relatifs `../../securite-developpement/` seraient cassés ici).
