---
name: gouv-fr-helm-chart
description: Use when creating or adapting a Helm chart to deploy on Cloud Pi Native
  (OpenShift + Kyverno) — starting from the this-is-tobi template, values per environment,
  securityContext and UID, MIOM labels, Vault secrets via extraObjects, image tags,
  chart versioning and OCI publication
allowed-tools: Bash Read Write
---

----|-------|
| UID/GID | mettre `runAsUser`, `runAsGroup`, `fsGroup` (pod et conteneur) à `null` ; garder `runAsNonRoot`, `drop: [ALL]`, `readOnlyRootFilesystem` ; ajouter `seccompProfile: {type: RuntimeDefault}` comme le fait `ocr-api` (absent des défauts du template) |
| Image | registre Harbor du projet, tag versionné ou digest (`digest` prime sur `tag`), **jamais `latest`** ; l'image doit grouper root (`chown -R <uid>:0` dans le Dockerfile) car l'UID est aléatoire |
| Labels | `commonLabels` : `app`, `env`, `tier` (exigés), `criticality`, `component` (MIOM) |
| Pull secret | `imagePullSecrets: [{name: registry-pull-secret}]` (créé par la console dans chaque namespace) |
| Ressources | `requests` et `limits` CPU+mémoire sur tous les conteneurs ; QoS Guaranteed conseillé ; la somme des `limits` compte pour le quota du namespace, dépendances comprises |
| Probes | au moins une par conteneur ; les défauts du template pointent `/` : régler le chemin réel |
| Service | `ClusterIP` (pas de NodePort) ; port d'écoute du conteneur > 1024 |
| Écriture | FS en lecture seule : `emptyDir` pour `/tmp` et autres chemins inscriptibles |
| Réseau | namespace en deny-all ; Kyverno injecte same-namespace, ingress, logging, monitoring ; déclarer le reste via `networkPolicy.create: true` + `ingress`/`egress` (egress via proxy : `HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY`) |
| Secrets | jamais dans `values.yaml` ni en ConfigMap ; `VaultStaticSecret` via `extraObjects` ([`references/vault-secret.yaml`](references/vault-secret.yaml)), `vaultAuthRef: vault-auth` |

Un fichier par environnement : `values-<env>.yaml` (la console remplace `<env>` par le nom de l'environnement).

## Vérifier

```bash
helm lint . -f values-cpin.yaml
helm template <release> . -f values-cpin.yaml -f values-<env>.yaml \
  | uv run --with pyyaml scripts/check-cpin-rules.py
```

`check-cpin-rules.py` contrôle labels, resources, probes, image (tag, registre), NodePort, hostPath, credentials en ConfigMap, et signale les UID figés.
Sortie 1 s'il reste des erreurs. Ce n'est pas Kyverno : les règles sont en **audit** en dev/preprod et **bloquantes en prod**, donc un rendu propre ici évite la surprise à la mise en prod, sans la garantir.

## Versions et publication

- `version` (chart) ≠ `appVersion` (application). Dans le dépôt applicatif, ne pas les bumper à la main : `update-helm-chart` (`RUN_MODE: local`) le fait au release (skill `cicd-fabnum`).
- Régénérer le README (helm-docs) : `lint-helm` échoue si le README diffère du rendu.
- Publication OCI : `release-helm-local` (ghcr.io) ; le pipeline DSO refait `helm dependency update`, `helm package` puis `helm push` vers Harbor.
- Dépendances (postgres, redis, CNPG) : `alias` + `condition: <alias>.enabled`, et `HELM_REPOS`/`chart-repos` pour celles en HTTP. Registres autorisés côté cluster : docker.io, harbor, registry.redhat.io, quay.io, bitnami, ghcr.io.

## Pièges

1. Renommage incomplet du template → `nil pointer evaluating interface {}.deploymentType` dans `NOTES.txt`.
2. `runAsUser: null` : Helm supprime la clé du défaut ; `{}` ou l'omission ne suffit pas (les défauts sont fusionnés).
3. Override d'une liste (`volumes`, `imagePullSecrets`) : Helm remplace la liste, ne la fusionne pas ; réécrire les entrées à garder (par exemple le volume `tmp`).
4. `service.nodePort` existe dans le template : ne pas l'utiliser, Kyverno interdit NodePort.
5. `enabled: false` ne désactive pas les sous-charts : ils ont leur propre `enabled`.
6. Tag inchangé = aucun redéploiement (ArgoCD ne voit pas de diff) ; le tag doit bouger à chaque livraison.
7. Noms de ressources trop longs : peuvent bloquer le déploiement sur OpenShift ; rester court, avec un suffixe par type (`-svc`, `-dep`, `-sts`, `-cm`, `-cj`, `-pvc`) et l'environnement en préfixe.

## Pour aller plus loin

- Doc interne : `docs/okf/helm/` (anatomie, conventions de values, sécurité et OpenShift, publication), `docs/okf/cloud-pi-native/contraintes-runtime.md` (table Kyverno), `docs/okf/decisions/dependances-chart.md`.
- Exemple complet : `IA-Generative/ocr-api/helm`.
- Skills liés (groupe `dso`) : `cicd-fabnum` (bump et publication du chart), `deploiement-cpin` (environnements, ArgoCD, secrets, quotas).
