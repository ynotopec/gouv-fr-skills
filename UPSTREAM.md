# Alignement upstream — `dnum-mi/starter-kit-opencode`

Suivi de la correspondance entre nos skills (`gouv-fr-*`) et les skills upstream
(`.agents/skills/<groupe>/`), dont les **noms diffèrent**.

**Dernier upstream vérifié** : commit `9d9cfbf` (2026-09-24)
— *refactor(skills): recentrer ci-cd et deploiement (dev), renvoyer vers le groupe dso (#16)*

## Correspondance des noms

### Groupe `dev`

| Upstream | Notre skill |
|----------|-------------|
| `dev/ci-cd` | `gouv-fr-github-actions-ci` |
| `dev/conventions-cofabnum` | `gouv-fr-conventions-nommage` |
| `dev/deploiement` | `gouv-fr-deployment-docker-k8s` |
| `dev/environnement-installation` | `gouv-fr-outils-developpement` *(fusionné)* |
| `dev/outils-dev` | `gouv-fr-outils-developpement` *(fusionné)* |
| `dev/monorepo` | `gouv-fr-monorepo-pnpm` |
| `dev/recettes-client` | `gouv-fr-frontend-vue3` |
| `dev/recettes-serveur` | `gouv-fr-backend-fastify` |
| `dev/stack-technique` | `gouv-fr-stack-technique` |

### Groupe `dso`

| Upstream | Notre skill |
|----------|-------------|
| `dso/cicd-fabnum` | `gouv-fr-github-actions-reusable` |
| `dso/deploiement-cpin` | `gouv-fr-deployment-cloud-pi-native` |
| `dso/helm-chart-cpin` | `gouv-fr-helm-chart` |

## Écarts assumés

- **`dev/outils-dev` + `dev/environnement-installation` fusionnés** en un seul
  skill `gouv-fr-outils-developpement`. Les deux contenus upstream sont couverts
  (installation machine, proto, WSL/Homebrew, Git, Docker, pnpm, uv, VS Code).
- **Noms francophones explicites** au lieu des noms courts upstream, pour rester
  lisibles par une personne externe.
- **`dso/index.json`** non repris : c'est un index de groupe propre au dépôt
  upstream, redondant avec notre `SKILLS.md`.

## Fichiers annexes — vérifiés byte-identiques à l'upstream

| Upstream | Notre emplacement | SHA-256 (12) |
|----------|-------------------|--------------|
| `dso/cicd-fabnum/references/ci.yml` | `gouv-fr-github-actions-reusable/references/ci.yml` | `e84207a541ee` |
| `dso/cicd-fabnum/references/cd.yml` | `gouv-fr-github-actions-reusable/references/cd.yml` | `070c12d63c60` |
| `dso/cicd-fabnum/references/workflows.md` | `gouv-fr-github-actions-reusable/references/workflows.md` | `77602ec42313` |
| `dso/deploiement-cpin/references/depannage.md` | `gouv-fr-deployment-cloud-pi-native/references/depannage.md` | `ae57d1362d57` |
| `dso/deploiement-cpin/references/gitlab-ci-dso.yml` | `gouv-fr-deployment-cloud-pi-native/references/gitlab-ci-dso.yml` | `30e1acf26acf` |
| `dso/helm-chart-cpin/references/values-cpin.yaml` | `gouv-fr-helm-chart/references/values-cpin.yaml` | `8391e8d66f9d` |
| `dso/helm-chart-cpin/references/vault-secret.yaml` | `gouv-fr-helm-chart/references/vault-secret.yaml` | `c48cf3c9b14f` |
| `dso/helm-chart-cpin/scripts/check-cpin-rules.py` | `gouv-fr-helm-chart/scripts/check-cpin-rules.py` | `f0041b35c5b8` |

## Modifications upstream intégrées

- **#16** `9d9cfbf` — `ci-cd` et `deploiement` recentrés (renvoi vers le groupe
  `dso`) :
  - `gouv-fr-github-actions-ci` : description, `name: CI` du gabarit, règle
    `@v0.20` / jamais `@main`
  - `gouv-fr-deployment-docker-k8s` : règle UID OpenShift
    (`chown -R <uid>:0`, `chmod -R g=u`), règle de tag (`latest` bloqué par
    Kyverno, digest), `COPY --from=build`, suppression des sections Helm/CPiN
    déplacées vers le groupe `dso`
  - `gouv-fr-helm-chart` : suffixe par type de ressource (`-svc`, `-dep`,
    `-sts`, `-cm`, `-cj`, `-pvc`) et environnement en préfixe
- **#7** `17b887f` — `recettes-client` : setup `@gouvfr/dsfr`, grille/typo/tokens
  DSFR, rappel `getRandomId`
- **#4** `5715782` — `recettes-client` : checklist avant implémentation,
  référence `DsfrInput`, piège Playwright `--no-sandbox` (Onyxia)

## Contrôle de fraîcheur

```bash
git clone https://github.com/dnum-mi/starter-kit-opencode.git /tmp/sk
cd /tmp/sk && git log -1 --format='%H %ci %s'
# comparer les fichiers de .agents/skills/ avec skills/gouv-fr-*/ (voir tableau ci-dessus)
```
