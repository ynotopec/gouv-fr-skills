---

name: projet-structure
description: "Structure de projet, intégration agent et variables d'env."
version: 0.3.0
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [gouv-fr, project, structure, layout, open-code, opencode, mcp, environment]
    related_skills: [developpement-securise, compliance-rgaa, workflow-dev, repo-init]
---

# Gouv-fr — Structure de projet

Layout de dépôt, intégration d'un agent de code (OpenCode ou équivalent) et
variables d'environnement. Ce skill est **autonome** : il ne dépend d'aucun
CLI interne ni d'une plateforme d'exécution particulière.

## Project Layout

```
my-app/
├── AGENTS.md                 # Règles projet + architecture
├── BACKLOG.md                # Tickets (epics → tasks, 🔴🟠🟡)
├── TESTS.md                  # Scénarios de validation
├── FEEDBACK.md               # Retours utilisateurs
├── opencode.jsonc            # Config de l'agent (provider, MCP, permissions)
├── .agents/
│   └── skills.txt            # Skills sélectionnées pour ce projet
└── src/
    ├── components/            # Composants DSFR
    ├── pages/                 # Pages / routes
    ├── services/              # API calls, services métier
    └── styles/                # Custom styles
```

## Comment l'agent charge les skills

1. **Config** — l'agent lit `opencode.jsonc` (niveau projet). Les permissions y
   sont déclarées explicitement ; ne jamais élargir `write` par défaut.
2. **MCP** — les connectors sont **opt-in** : `data-gouv` (données publiques),
   `context7` (documentation des librairies), `playwright` (navigateur headless),
   `chrome-devtools` (inspection DOM).
3. **Skills** — seules les skills listées dans `skills.txt` sont activées pour
   le projet ; le reste du catalogue est disponible à la demande.
4. **Règles** — l'agent lit `AGENTS.md`. Toute zone générée automatiquement
   doit être délimitée par des marqueurs explicites, pour être réécrite sans
   casser le reste du fichier.

## Variables d'environnement

| Variable | Défaut | Rôle |
|---|---|---|
| `AGENT_PROVIDER_URL` | — | Endpoint du modèle (self-hosted ou API interne) |
| `AGENT_MODEL` | — | Identifiant du modèle à utiliser |
| `AGENT_SKILLS_FILE` | `.agents/skills.txt` | Liste des skills activées |
| `AGENT_CONFIG` | `opencode.jsonc` | Fichier de configuration de l'agent |

Ne jamais inscrire de valeur de secret dans ces variables : utiliser le
mécanisme de secrets de l'environnement (voir la skill `developpement-securise`).

## Ressources

- **OpenCode** : `https://opencode.ai/docs/fr`
- **DSFR** : `https://www.systeme-de-design.gouv.fr/` → skill `design-system`
- **Skills of the State** : `https://github.com/etalab-ia/skills`
