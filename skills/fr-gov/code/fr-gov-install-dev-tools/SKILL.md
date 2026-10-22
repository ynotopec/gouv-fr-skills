---

name: fr-gov-install-dev-tools
description: Git, Docker, pnpm, proto, uv, environment diagnostics
version: 0.2.0
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [gouv-fr, dev-tools, git, docker, pnpm, proto, vscode, github-cli, uv, shell]
    related_skills: [fr-gov-choose-tech-stack, fr-gov-containerize-app-for-k8s, fr-gov-project-conventions]
---

# Gouv-fr — Outils de développement

Travailler avec les outils de développement utilisés dans les projets Fabrique Numérique : installation, configuration,
Git, Docker, pnpm, proto, VS Code, GitHub CLI, etc.

## Quand utiliser
- Configurer ou dépanner son environnement de développement
- Installer et configurer les outils requis (Git, Docker, pnpm, proto, VS Code)
- Automatiser la vérification de l'environnement
- Gérer les workflows Git (branches, commits, PRs)

## Scripts disponibles
- **`scripts/check-environment.sh`** — Vérifie tous les outils requis et optionnels
  - Usage : `bash scripts/check-environment.sh` (rapport en lecture seule)
  - Usage : `bash scripts/check-environment.sh --fix` (inclut les commandes d'installation)

## Renvois

- Nommage des fichiers, dossiers et variables : skill `fr-gov-project-conventions`
  (§ Naming) — plus dupliqué ici.
- `.gitignore`, secrets, premier commit : skill `init-repo`.
- Installation détaillée par outil : [machine](references/installation-machine.md),
  [git](references/git.md), [docker](references/docker.md), [vscode](references/vscode.md).

## pnpm

```shell
pnpm install            # Install all deps
pnpm add <pkg>          # Add dependency
pnpm add -D <pkg>       # Add dev dependency
pnpm store path         # Cache path for CI
```

Voir [fr-gov-set-up-pnpm-monorepo] pour les workspaces.

## proto

```shell
proto install node@24        # ligne LTS 24 (24.22.1 au 2026-10-22)
proto install python@3.12
proto ls                  # List installed
```

Créer `.prototools` à la racine du projet pour le switching automatique.

## GitHub CLI

```shell
gh auth login
gh pr create --title "feat: new feature#123"
gh pr list
gh pr checkout <number>
gh pr review --approve
gh pr review --comment --body "LGTM"
```

## uv (Python)

```shell
uv init my-project
uv add fastapi
uv add --dev ruff pytest httpx
uv run fastapi dev
uv run pytest
uv run ruff check .
```

Files : `pyproject.toml` (metadata), `uv.lock` (locked deps).

## Pièges
- **Branches incluent le ticket** — `feat/description` est incomplet, utiliser `feat/description#123`
- **pnpm store caching** — utiliser la sortie `pnpm store path` pour la clé de cache CI, pas un chemin hardcodé
- **Docker group on Linux** — `usermod -aG docker` nécessite une reconnexion
- **proto versions override system** — les versions proto ont la priorité sur les installations système
- **Never commit `.turbo/`** — c'est un cache local
- **GitHub Actions pin versions** — SHA de commit, ou à défaut un tag majeur (`@v6`) ; jamais `@latest`, `@main` ni `@master`
- **WSL2 memory** — si Docker est lent sur WSL, augmenter la mémoire dans `.wslconfig`
- **Windows developers MUST use WSL** — pas de développement natif Windows
- **Docker requires re-login** — les changements de groupe docker ne s'appliquent pas aux sessions existantes
- **Noto fonts** — installer `fonts-noto` pour le rendu Unicode correct dans les terminaux
- **Ne pas utiliser `master` comme branche par défaut** — `main` seulement
- **Ne pas mélanger kebab-case et camelCase** dans les noms de fichiers
