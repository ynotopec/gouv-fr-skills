---
name: gouv-fr-code-index-index
description: "Index des skills gouv-fr-code pour construire une application de l'État."
version: 0.2.0
author: gouv-fr-code (etalab-ia), Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [gouv-fr-code, sovereign, france, etat, government, app, build, dsfr, rgaa, index]
    related_skills: [gouv-fr-code-project, gouv-fr-code-security, gouv-fr-code-compliance, gouv-fr-code-workflow, gouv-fr-code-git]
---

# gouv-fr — Index Skills

Package complet de skills gouv-fr pour construire, auditer et déployer des applications de l'administration française.

## Sources

- **starter-kit-opencode** (`.agents/skills/dev/*` + `dso/*`) — CoFabNum conventions, stack, CI/CD, CPiN
- **gouv-fr-code-package-mi** (`gouv-fr-code-*`) — Core skills gouv-fr-code
- **Local skills** (migrés) — DSFR, audit, référentiel données

## Installation

```bash
# Copier les skills dans le répertoire Hermes skills
cp -r gouv-fr-*/ ~/.hermes/skills/
```

## Verification

- Chaque répertoire contient un `SKILL.md` avec frontmatter YAML
- Tous les noms commencent par `gouv-fr-`
- Les skills ont des tags hermes metadata

## Ressources

- **Source** : `github.com/etalab-ia/albert-code`
- **OpenCode** : `https://opencode.ai/docs/fr`
- **Albert API** : `https://albert.api.etalab.gouv.fr`
- **agent-vm** : `https://github.com/sylvinus/agent-vm`
- **DSFR** : `https://www.systeme-de-design.gouv.fr/`
- **Skills of the State** : `https://github.com/etalab-ia/skills`
