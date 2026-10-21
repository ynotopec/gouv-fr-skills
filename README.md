# gouv-fr-skills

Répertoire de skills compatibles **Hermes**, **OpenCode**, **Kilo Code** et
**Claude Code** pour les projets de la Fabrique Numérique (Mission Interministérielle).

**43 skills** répartis en **7 groupes**, sous `skills/gouv-fr/<groupe>/<skill>/`.
Index complet : [`SKILLS.md`](SKILLS.md).

## Origines

- **Cloud Pi Native** — https://cloud-pi-native.fr (déploiement, Helm, ArgoCD)
- **Starter Kit OpenCode** (`dnum-mi/starter-kit-opencode`) — `.agents/skills` + `docs/okf`
- **gouv-fr-code-package-mi** (`ynotopec/gouv-fr-code-package-mi`) — core skills gouv-fr-code
- **IA-Generative/agent-skills** — dépôt privé (non clonable publiquement)
- **Skills de l'État** (`etalab-ia/skills`) — référentiel DINUM/IAE. **4 skills adaptées** : `react-dsfr`, `lasuite-ui-kit`, `anssi-guides`, `datagouv-apis`. Les 3 autres (`rgaa`, `securite-developpement`, `usage-ia-agents-etat`) ne sont pas reprises ; voir [`UPSTREAM.md`](UPSTREAM.md) § *Référentiels externes*.
- **Skills locaux gouv-fr** — migrés et renommés, sauvegarde dans `backup-local-skills/`

## Organisation

Les skills sont regroupés par usage, sous un unique arbre `gouv-fr/` :

| Groupe | Contenu |
|---------|---------|
| [`anssi`](skills/gouv-fr/anssi/) | Guides ANSSI, audits de sécurité, durcissement |
| [`code`](skills/gouv-fr/code/) | Architecture, conventions, backend, frontend, outillage, workflow |
| [`conformite`](skills/gouv-fr/conformite/) | RGAA, RGPD, cookies, documents d'homologation |
| [`data`](skills/gouv-fr/data/) | APIs data.gouv.fr, données ouvertes du SIG |
| [`dsfr`](skills/gouv-fr/dsfr/) | Design system de l'État, composants, pictogrammes, templates |
| [`dso`](skills/gouv-fr/dso/) | CI/CD, conteneurs, Kubernetes, Cloud Pi Native, tests de fumée |
| [`lasuite`](skills/gouv-fr/lasuite/) | Interfaces React LaSuite |

Le nom d'un skill ne porte pas le préfixe `gouv-fr-` : il ne doit pas répéter le
nom de son dossier parent. `skills/gouv-fr/code/code-index/` est conforme ;
`skills/gouv-fr/code/gouv-fr-code-index/` ne l'est pas.

## Installation

Le script installe chaque dossier de skill sans en modifier le format, en
conservant le dossier de groupe :

```bash
# Installer les 43 skills pour les quatre agents, dans le profil utilisateur
./scripts/install-skills.sh

# Installer pour un seul agent
./scripts/install-skills.sh --agent hermes
./scripts/install-skills.sh --agent opencode
./scripts/install-skills.sh --agent kilo
./scripts/install-skills.sh --agent claude
```

Les destinations utilisateur sont :

| Agent | Destination |
|-------|-------------|
| Hermes | `${HERMES_HOME:-~/.hermes}/skills/` |
| OpenCode | `${XDG_CONFIG_HOME:-~/.config}/opencode/skills/` |
| Kilo Code | `${KILO_HOME:-~/.kilocode}/skills/` |
| Claude Code | `${CLAUDE_HOME:-~/.claude}/skills/` |

Les skills sont posés dans `<destination>/<groupe>/<skill>/`. Pour une
installation à plat (sans dossier de groupe), ajouter `--flat`.

Pour une installation limitée à un dépôt, utiliser `--scope project`. Le script
écrit alors respectivement dans `.hermes/skills/`, `.opencode/skills/`,
`.kilocode/skills/` ou `.claude/skills/` :

```bash
./scripts/install-skills.sh --agent claude --scope project
./scripts/install-skills.sh --agent all --scope project --project /chemin/du/projet
```

Par sécurité, une installation existante n'est pas écrasée. Ajouter `--force`
pour mettre à jour les copies déjà présentes. `./scripts/install-skills.sh --help`
affiche toutes les options.

## Vérification

- Chaque skill dans `skills/gouv-fr/<groupe>/<skill>/` contient un `SKILL.md` avec frontmatter YAML valide
- Le workflow `Security` analyse l'historique complet avec Gitleaks ; les fichiers de secrets et le répertoire local `private/` sont ignorés par Git
- Le champ `name:` de chaque skill correspond à son dossier, en kebab-case minuscule
  conforme au motif `^[a-z0-9]+(-[a-z0-9]+)*$` exigé par les validateurs de skills
  (opencode, albert-code, Claude Code). Aucune majuscule : `graphiques-dsfr`,
  pas `graphiques-DSFR`. Les acronymes restent en majuscules **dans le titre H1
  et le texte**, jamais dans le nom.
- Aucun skill ne porte le nom de son groupe parent
- Les références croisées (`related_skills`, mentions dans le corps) pointent vers des skills existants
- Exemple d'application conforme : `examples/test-app-verification/`

Contrôle rapide de conformité :

```bash
# Aucun nom de skill ne doit reprendre le nom de son groupe
find skills/gouv-fr -mindepth 2 -maxdepth 2 -type d \
  -exec sh -c '[ "$(basename "$1")" = "$(basename "$(dirname "$1")")" ] && echo "$1"' _ {} \;

./scripts/test-install-skills.sh
```

Voir [`REVIEW.md`](REVIEW.md) pour le rapport de revue complet.

### Audits adaptés au projet

`code-index` oriente vers le skill pertinent sans charger tout le catalogue.
L'audit de conformité commence par identifier la stack et le déploiement réels ;
une vérification seule reste en lecture seule. Une demande de correction ou de
PR autorise les modifications correspondantes. Les preuves manquantes sont
« non évaluées », les contrôles hors périmètre sont « sans objet » : ni l'un ni
l'autre ne vaut conformité démontrée.

Le vérificateur DSFR contrôle les classes CSS et les assets locaux, pas la
conformité globale ni le RGAA. **Sans classe `fr-*`, il indique « non évalué »
et retourne 1**, au lieu d'un succès à 100 %. Ses tests s'exécutent hors réseau :

```bash
python3 -m unittest discover -s skills/gouv-fr/dsfr/design-system/tests -v
```

Le [protocole d'évaluation](skills/gouv-fr/conformite/audit-conformite/references/evaluation-efficiency.md)
permet de comparer qualité, faux positifs, durée, tokens et interventions
humaines avec et sans skills. Il ne constitue pas un benchmark déjà exécuté.

## Tests

Quatre suites de non-régression s'exécutent hors réseau et sont lancées par la
CI (`Skills tests`) :

```bash
python -m pip install pyyaml python-docx

# Rendu DAT : typographie française et modèle Word par défaut
python3 -m unittest discover -s skills/gouv-fr/conformite/dat-word/tests -v

# Vérificateur DSFR : classes CSS et assets locaux
python3 -m unittest discover -s skills/gouv-fr/dsfr/design-system/tests -v

# Permissions des appels de workflows réutilisables
python3 -m unittest discover -s skills/gouv-fr/dso/repo-cicd/tests -v

# Smoke-test : credentials synthétiques et transport simulé
python3 -m unittest discover -s skills/gouv-fr/dso/smoke-test/tests -v

# Script d'installation (Hermes, OpenCode, Kilo Code, Claude Code)
./scripts/test-install-skills.sh
```

Le script d'installation s'exécute dans un répertoire temporaire : il n'écrit
rien dans le répertoire de skills réel de l'utilisateur.

## Maintenance autonome

Les skills sont maintenus et validés directement dans ce dépôt. Aucune PR ni
validation dans un dépôt d'origine n'est requise. Les fichiers `UPSTREAM.md`
documentent la provenance ; ils ne constituent pas une procédure de synchronisation
obligatoire. Les références internes sont embarquées avec chaque skill.

`code-quality` charge uniquement la revue, le rituel ou les standards
nécessaires à la tâche. Son historique et ses adaptations sont décrits dans
son [`UPSTREAM.md`](skills/gouv-fr/code/code-quality/UPSTREAM.md).

L'installation des skills copie les fichiers locaux sans récupérer d'autres
skills. Les outils et services propres aux tâches (Helm, API data.gouv.fr,
workflows CI, etc.) restent des prérequis à vérifier selon le besoin.

## Workflow

Voir [`WORKFLOW.md`](WORKFLOW.md) — règle d'or : `bash .github/workflows/save-workflow.sh "<motif>"` avant tout gros changement.
