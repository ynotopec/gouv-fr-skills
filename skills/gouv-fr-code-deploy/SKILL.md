---
name: gouv-fr-code-deploy
description: Use when deploying Docker and K8s. Fabrique Numérique.
version: 0.1.0
author: gouv-fr-code (etalab-ia), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [gouv-fr-code, deploy, docker, kubernetes, helm, cpn, cloud-pi-native, container]
    related_skills: [gouv-fr-code, gouv-fr-code-project, gouv-fr-code-cicd]
---

# Gouv-fr — Déploiement

La plateforme de déploiement cible est Cloud Pi Native (PaaS open source sur Kubernetes/OpenShift). Tous les services doivent être conteneurisés.

## When to Use
- Créer un Dockerfile pour un projet Fabrique Numérique
- Déployer sur Kubernetes ou OpenShift
- Créer ou modifier un Helm chart
- Configurer un déploiement CPiN

## Prerequisites
- Docker installé pour le build local
- kubectl/kind/k3d pour le testing local K8s
- Helm installé pour la gestion des charts
- Dockerfile existant dans le projet

## How to Run
- Build : `docker build -t ghcr.io/org/app:tag .`
- Test local : `kind create cluster` ou `k3d cluster create`
- Deploy : `helm upgrade --install my-app ./helm`

## Quick Reference — Bonnes pratiques

### Docker (obligatoire, rootless)
- Utiliser des images de base légères : `*-alpine`, `*-slim`, `distroless`
- Exécuter avec un utilisateur non-root (UID ≥ 1000)
- Build multi-stage pour séparer build et production
- Ne pas embarquer de secrets, fichiers de dev ou outils inutiles
- Écouter sur un port non privilégié (≥ 1024, ex. 8080)
- Ne jamais utiliser `latest` en production — toujours épingler un tag

### Dockerfile optimisé (exemple Node.js)
```dockerfile
# Build stage
FROM docker.io/node:24-alpine AS build
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile
COPY . .
RUN pnpm build

# Production
FROM docker.io/nginxinc/nginx-unprivileged:1.29-alpine AS prod
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 8080
USER 1001
```

### Dockerfile optimisé (exemple Python/FastAPI)
```dockerfile
# Build stage
FROM docker.io/python:3.12-slim AS build
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install --no-cache-dir uv
RUN uv sync --frozen --no-dev
COPY . .

# Production
FROM docker.io/python:3.12-slim AS prod
WORKDIR /app
COPY --from=build /app/.venv /app/.venv
COPY --from=build /app/app /app/app
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8080
USER 1000
CMD ["fastapi", "run", "app/main.py"]
```

### Kubernetes — securityContext
```yaml
securityContext:
  runAsNonRoot: true
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
  capabilities:
    drop: [ALL]
```

### Helm — structure minimale
```
helm/
├── Chart.yaml          # Métadonnées (nom, version, appVersion)
├── values.yaml         # Valeurs par défaut
├── templates/
│   ├── _helpers.tpl    # Fonctions et labels réutilisables
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── hpa.yaml
│   └── serviceaccount.yaml
└── values/
    ├── dev.yaml
    ├── staging.yaml
    └── prod.yaml
```

### Helm — bonnes pratiques
- Utiliser les labels standards Kubernetes (`app.kubernetes.io/name`, etc.) via `_helpers.tpl`
- Rendre les ressources optionnelles avec `{{- if .Values.* }}`
- Ne jamais mettre de secrets en clair dans `values.yaml` — utiliser Sealed Secrets ou gestionnaire externe
- Versionner le chart indépendamment de l'application (`version` ≠ `appVersion`)
- Valider en CI : `helm lint` et `helm template`

### Cloud Pi Native (PaaS interne)
- Console simplifiée pour déployer sur clusters Kubernetes/OpenShift
- Orienté conteneurisation, privilèges minimum, compatibilité K8s & OpenShift
- Utiliser les Helm charts CPiN pour les déploiements

### Docker Compose (dev local)
- Pour le développement quotidien, Docker Compose suffit
- Plus simple que Kubernetes pour le dev local
- Reproduire les services de prod (DB, cache, etc.)

## Procedure — Créer un Dockerfile multi-stage

1. Identifier la stack (Node.js ou Python)
2. Créer un Dockerfile avec 2 stages (build + prod)
3. Utiliser une base légère (`alpine` ou `slim`)
4. Copier les lock files puis les dépendances avant le code source (cache layer)
5. Définir USER non-root
6. Exposer un port ≥ 1024
7. Tester : `docker build -t test-app . && docker run --rm test-app`

## Pitfalls
- Ne jamais utiliser `root` dans le conteneur de prod
- Ne jamais utiliser `latest` pour les images
- Les secrets doivent venir d'environnement ou de secrets gérés (pas dans le Dockerfile)
- Les volumes de dev (`node_modules`, `.venv`) ne doivent pas être montés en prod
- Helm `values.yaml` ne doit jamais contenir de secrets en clair
- `readOnlyRootFilesystem` peut casser les apps qui écrivent dans `/tmp` — vérifier les besoins

## Verification
- `docker build -t test .` passe sans erreur
- `docker run --rm test` démarre sans se crasher
- Trivy ne rapporte pas de CVE CRITICAL : `trivy image test`
- Helm chart valide : `helm lint ./helm` et `helm template test ./helm`
