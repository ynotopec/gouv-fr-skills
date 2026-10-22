---

name: fr-gov-set-up-project-layout
description: Project layout, agent integration, environment variables
version: 0.3.0
license: MIT
author: ynotopec
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [gouv-fr, project, structure, layout, open-code, opencode, mcp, environment]
    related_skills: [fr-gov-secure-coding-rules, fr-gov-check-web-compliance, ship-a-dev-task, init-repo]
---

# Gouv-fr — Structure de projet

Layout de dépôt, intégration d'un agent de code et variables d'environnement.
Ce skill est **autonome** : il ne dépend d'aucun CLI interne ni d'une plateforme
d'exécution particulière, et ne suppose pas un agent donné.

Les exemples nomment OpenCode (le plus répandu dans la Fabrique), mais chaque
agent a son équivalent : `config.yaml` + répertoire de skills pour Hermes,
`.claude/` pour Claude Code, `.agents/skills` pour le Starter Kit. Remplacer le
nom du fichier de configuration, pas la structure.

## Quand utiliser

- Poser le layout d'un dépôt et son intégration à un agent de code.
- Documenter les variables d'environnement attendues par le projet.

Ne pas utiliser pour initialiser le dépôt lui-même : voir `init-repo`.

## Project Layout

```
my-app/
├── AGENTS.md                 # Règles projet + architecture
├── BACKLOG.md                # Tickets (epics → tasks, 🔴🟠🟡)
├── TESTS.md                  # Scénarios de validation
├── FEEDBACK.md               # Retours utilisateurs
├── <config-agent>            # Config de l'agent (opencode.jsonc, config.yaml, …)
├── .agents/
│   └── skills.txt            # Skills sélectionnées pour ce projet (optionnel)
└── src/
    ├── components/            # Composants DSFR
    ├── pages/                 # Pages / routes
    ├── services/              # API calls, services métier
    └── styles/                # Custom styles
```

## Comment l'agent charge les skills

1. **Config** — l'agent lit sa configuration projet (`opencode.jsonc` pour
   OpenCode, `.hermes/` ou `config.yaml` pour Hermes, `.claude/` pour Claude
   Code). Les permissions y sont déclarées explicitement ; ne jamais élargir
   `write` par défaut.
2. **MCP** — les connectors sont **opt-in** : `data-gouv` (données publiques),
   `context7` (documentation des librairies), `playwright` (navigateur headless),
   `chrome-devtools` (inspection DOM).
3. **Skills** — le catalogue est disponible à la demande ; si l'agent accepte une
   liste explicite par projet (`skills.txt`, réglage `skills` de la config), n'y
   mettre que les skills nécessaires.
4. **Règles** — l'agent lit `AGENTS.md`. Toute zone générée automatiquement
   doit être délimitée par des marqueurs explicites, pour être réécrite sans
   casser le reste du fichier.

## Variables d'environnement

| Variable | Défaut | Rôle |
|---|---|---|
| `AGENT_PROVIDER_URL` | — | Endpoint du modèle (self-hosted ou API interne) |
| `AGENT_MODEL` | — | Identifiant du modèle à utiliser |
| `AGENT_SKILLS_FILE` | `.agents/skills.txt` | Liste des skills activées |
| `AGENT_CONFIG` | selon l'agent | Fichier de configuration de l'agent |

Ne jamais inscrire de valeur de secret dans ces variables : utiliser le
mécanisme de secrets de l'environnement (voir la skill `fr-gov-secure-coding-rules`).

## Ressources

- **OpenCode** : `https://opencode.ai/docs/fr`
- **Hermes** : `https://hermes-agent.nousresearch.com/docs`
- **DSFR** : `https://www.systeme-de-design.gouv.fr/` → skill `fr-gov-set-up-design-system`
- **Skills of the State** : `https://github.com/etalab-ia/skills`
