---
name: gouv-fr-code-naming
description: Conventions de nommage de branches, commits, variables et fichiers pour Fabrique Numérique.
version: 0.1.0
author: gouv-fr-code (etalab-ia), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [gouv-fr-code, naming, conventions, git, branches, variables, files]
    related_skills: [gouv-fr-code, gouv-fr-code-git, gouv-fr-code-project]
---

# Gouv-fr — Conventions de Nomage

Conventions de nommage pour les branches Git, commits, variables, fonctions et fichiers.

## When to Use
- Créer une nouvelle branche Git
- Écrire un message de commit
- Nommer des variables, fonctions ou fichiers dans le code
- Renommer des dossiers

## Prerequisites
- Git configuré (`git init` avec `main` comme branche par défaut)
- GitHub CLI (`gh`) installé

## How to Run
- `git switch -c feat/description#123` pour une nouvelle branche
- `git commit -m "feat: description courte"`
- Aliases zsh : `gfeat`, `gfix`, `gtech`

## Quick Reference — Branches Git

### Branche par défaut
- `main` (pas `master`)
- Configuration globale : `git config --global init.defaultBranch main`

### Format des noms de branches
`<type>/<description>#<ticket>`

| Type | Description |
|---|---|
| `feat` | Nouvelle fonctionnalité |
| `fix` | Correction d'anomalie ou graphie |
| `hotfix` | Correction urgente déjà en prod |
| `tech` | Amélioration technique (dette technique, script, build) |
| `docs` | Modification de documentation |
| `refactor` | Remaniement sans changement de comportement |

**Exemples :**
- `feat/worker-logs#353`
- `refactor/reorganize-backend#360`
- `fix/auth-error#42`
- `hotfix/critical-bug#99`

### Alias zsh (à ajouter dans `~/.zshrc`)
```bash
createFeatBranch() { (git switch -c "feat/$1" && ding) || dong }
createFixBranch() { (git switch -c "fix/$1" && ding) || dong }
createTechBranch() { (git switch -c "tech/$1" && ding) || dong }

alias gfeat='createFeatBranch'
alias gfix='createFixBranch'
alias gtech='createTechBranch'
```

## Quick Reference — Messages de commit

### Conventional Commits (obligatoire)
`type(scope): description courte`

Types : `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Les messages peuvent être en **français**. En anglais, vérifier le vocabulaire.

## Quick Reference — Noms de fichiers et dossiers

### Dossiers et fichiers
- **Impérativement kebab-case**
- Exception : noms de composants Vue (au moins 2 mots, CamelCase) + `App.vue`

### Structure de projet (kebab-case)
```
my-app/
├── src/
│   ├── index.ts              # Point d'entrée
│   ├── app.ts                # Config Fastify/NestJS
│   ├── plugins/              # Plugins Fastify
│   │   ├── cors.ts
│   │   └── swagger.ts
│   ├── routes/               # Routes
│   │   └── cat-routes.ts
│   ├── services/             # Logique métier
│   └── utils/                # Utilitaires
└── tests/
    └── routes/
        └── cat-routes.test.ts
```

## Quick Reference — Noms de variables

| Type | Convention | Exemple |
|---|---|---|
| Variable booléenne | `is*`, `has*`, `should*`, `can*` + camelCase | `isActive`, `hasPermission` |
| Variable date | camelCase + suffixe `Date` ou `At` | `startDate`, `lastModifiedAt` |
| Fonction/class | camelCase / PascalCase | `getUser()`, `UserService` |
| Constante | SCREAMING_SNAKE_CASE | `MAX_RETRIES` |
| Variable générale | camelCase, explicite | `userEmail`, `appConfig` |

### Règles
- Noms en **anglais** par défaut
- Français autorisé si traduction prête à confusion ou mot réservé (`dossier`, `affaire`)
- **Proscrit** : variables d'une seule lettre (sauf identité `x => x`)
- Noms explicites : potentiellement longs, mais pas excessifs

## Pitfalls
- Ne pas utiliser `master` comme branche par défaut — `main` seulement
- Ne pas mélanger kebab-case et camelCase dans les noms de fichiers
- Ne pas utiliser `enum` TypeScript (utilisez les unions) — cf. skill `gouv-fr-code-stack`
- Les messages de commit : vérifier l'anglais si écrit en anglais (faux-amis courants)
- Branches : toujours inclure le ticket GitHub (`#123`)

## Verification
- `git log --oneline` affiche des messages Conventional Commits valides
- Aucun dossier/fichier en snake_case ou PascalCase (sauf composants Vue)
- Aucune variable à une seule lettre dans le code (sauf cas évidents)
