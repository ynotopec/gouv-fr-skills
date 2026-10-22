# gouv-fr-skills

Répertoire de skills compatibles **Hermes**, **OpenCode**, **Kilo Code** et
**Claude Code** pour les projets de la Fabrique Numérique (Mission Interministérielle).

**42 skills** répartis en **7 groupes**, sous `skills/fr-gov/<groupe>/<skill>/`.
Index complet : [`SKILLS.md`](SKILLS.md).

## Origines

- **Cloud Pi Native** — https://cloud-pi-native.fr (déploiement, Helm, ArgoCD)
- **Starter Kit OpenCode** (`dnum-mi/starter-kit-opencode`) — `.agents/skills`
- **gouv-fr-code-package-mi** (`ynotopec/gouv-fr-code-package-mi`) — core skills fr-gov-code
- **Skills de l'État** (`etalab-ia/skills`) — référentiel DINUM/IAE. **4 skills adaptées** : `fr-gov-build-react-design-system`, `fr-gov-build-collab-suite-ui`, `fr-gov-find-cybersecurity-guide`, `fr-gov-query-open-data-api`. Les 3 autres (`rgaa`, `securite-developpement`, `usage-ia-agents-etat`) ne sont pas reprises ; voir [`UPSTREAM.md`](UPSTREAM.md) § *Référentiels externes*.

## Organisation

Les skills sont regroupés par usage, sous un unique arbre `fr-gov/` :

| Groupe | Contenu |
|---------|---------|
| [`security`](skills/fr-gov/security/) | Guides ANSSI, audits de sécurité, durcissement |
| [`code`](skills/fr-gov/code/) | Architecture, conventions, backend, frontend, outillage, workflow |
| [`compliance`](skills/fr-gov/compliance/) | RGAA, RGPD, cookies, documents d'homologation |
| [`data`](skills/fr-gov/data/) | APIs data.gouv.fr, données ouvertes du SIG |
| [`design-system`](skills/fr-gov/design-system/) | Design system de l'État, composants, pictogrammes, templates |
| [`devops`](skills/fr-gov/devops/) | CI/CD, conteneurs, Kubernetes, Cloud Pi Native, tests de fumée |
| [`lasuite`](skills/fr-gov/lasuite/) | Interfaces React LaSuite |

Les skills propres aux pratiques, plateformes ou référentiels publics français
portent le préfixe **`fr-gov-`**, y compris en installation à plat. Les procédures
réutilisables sans contexte institutionnel restent sans préfixe : `review-code`,
`investigate-bug`, `init-repo` ou `smoke-test-api`.

### Noms explicites

Un nom anglais décrit l'usage réel. Après `fr-gov-`, ne pas répéter `french`,
`gouv`, `gouvernement`, `state` ou `government`. Le nom doit rester compréhensible
sans connaissance des sigles français : `fr-gov-build-react-design-system`,
`fr-gov-find-cybersecurity-guide`, `fr-gov-query-public-communication-data`.
Les marques et identifiants techniques réels (packages npm, APIs, URLs, classes
CSS) restent inchangés dans les procédures.

| Ancien nom | Nom actuel |
|---|---|
| `backend-fastify` | `fr-gov-scaffold-backend-api` |
| `lint-eslint` | `fr-gov-configure-linting` |
| `code-index` | *(supprimé — skill routeur, non conforme)* |
| `audit-safety` | `audit-repo-safety` |
| `audit-redteam` | `redteam-llm-prompt-injection` |
| `audit-pentest` | `harden-repo-before-pentest` |
| `repo-cicd` | `fr-gov-set-up-cloud-pi-native-cicd` |
| `dat-homologation` | `fr-gov-fill-technical-architecture-doc` |
| `dat-word` | `fr-gov-render-technical-architecture-docx` |
| `service-names` | `detect-stale-service-names` |
| `security` | `fr-gov-secure-coding-rules` |
| `conventions-nommage` | `fr-gov-project-conventions` |
| `compliance-rgaa` | `fr-gov-check-web-compliance` |
| `donnees-ouvertes` | `fr-gov-query-public-communication-data` |
| `audit-openwebui` | `audit-llm-tool-identity` |
| `smoke-test` | `smoke-test-api` |
| `composants-vue` | `fr-gov-build-vue-design-system` |
| `design-system` | `fr-gov-set-up-design-system` |
| `templates-email` | `fr-gov-build-design-system-emails` |

Les groupes `anssi` et `dso` deviennent `security` et `devops`. `fr-gov-containerize-app-for-k8s` et `fr-gov-set-up-github-actions-ci` passent de `code` à `devops` ;
`detect-stale-service-names` passe de `devops` à `code`.
La [table de migration](scripts/skill-renames.tsv) conserve les correspondances
des générations historiques vers les 42 skills actifs. Les routeurs retirés
(`code-index`, `skills-router`) sont déclarés dans la
[table des retraits](scripts/skill-retirements.tsv) : `--migrate` archive leurs
copies hors du catalogue actif et conserve les modifications locales.
Les références externes doivent être mises à jour d'après ces tables.

## Installation

Le script installe chaque dossier de skill sans en modifier le format, en
conservant le dossier de groupe :

```bash
# Installer les 42 skills pour les quatre agents, dans le profil utilisateur
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

### Migrer une installation existante

Les anciens noms, groupes et copies `gouv-fr-<nom>` sont détectés avant installation.
`--force` seul ne permet pas de les laisser cohabiter avec les nouveaux noms.
Utiliser `--migrate` pour archiver les anciennes copies dans un dossier frère
`skills.backup-XXXXXX`, hors du répertoire actif, avant d'installer le nouveau
catalogue. Le chemin de sauvegarde est affiché ; les modifications locales et
les skills tiers sont conservés. Les destinations déjà présentes qui seront
remplacées avec `--force` sont également sauvegardées pendant cette migration.

```bash
./scripts/install-skills.sh --agent all --migrate
# Si les nouvelles destinations existent déjà :
./scripts/install-skills.sh --agent all --migrate --force
```

La sauvegarde reste disponible pour récupérer les anciennes copies ; elle
n'est jamais supprimée par l'installateur. `--migrate` fonctionne aussi avec
`--scope project` et `--flat`.

## Vérification

- Chaque skill dans `skills/fr-gov/<groupe>/<skill>/` contient un `SKILL.md` avec frontmatter YAML valide
- La `description` tient en **60 caractères au plus**, selon la convention Hermes.
  Elle contient quelques termes discriminants en anglais, comme une requête de
  recherche précise : pas de phrase imposée, de point final obligatoire ni
  d'accumulation de synonymes. Privilégier les critères qui distinguent les skills
  voisins ; détailler les conditions et exclusions dans `## Quand utiliser`.
- Chaque skill porte une section `## Quand utiliser` (déclencheurs, et
  « Ne pas utiliser pour » quand un skill voisin traite le sujet)
- Le workflow `Security` analyse l'historique complet avec Gitleaks ; les fichiers de secrets et le répertoire local `private/` sont ignorés par Git
- Le champ `name:` de chaque skill correspond à son dossier, en kebab-case minuscule
  conforme au motif `^[a-z0-9]+(-[a-z0-9]+)*$` exigé par les validateurs de skills
  (opencode, albert-code, Claude Code). Aucune majuscule : `fr-gov-build-design-system-charts`,
  pas `graphiques-DSFR`. Les acronymes restent en majuscules **dans le titre H1
  et le texte**, jamais dans le nom.
- Aucun skill ne porte le nom de son groupe parent
- Les références croisées (`related_skills`, mentions dans le corps) pointent vers des skills existants
- Exemple d'application conforme : `examples/test-app-verification/`

Contrôle rapide de conformité :

```bash
# Aucun nom de skill ne doit reprendre le nom de son groupe
find skills/fr-gov -mindepth 2 -maxdepth 2 -type d \
  -exec sh -c '[ "$(basename "$1")" = "$(basename "$(dirname "$1")")" ] && echo "$1"' _ {} \;

./scripts/test-install-skills.sh
```

Voir [`REVIEW.md`](REVIEW.md) pour le rapport de revue complet.

### Audits adaptés au projet

Le catalogue et les `## Quand utiliser` de chaque skill orientent vers la fiche
pertinente sans charger tout le catalogue.
L'audit de conformité commence par identifier la stack et le déploiement réels ;
une vérification seule reste en lecture seule. Une demande de correction ou de
PR autorise les modifications correspondantes. Les preuves manquantes sont
« non évaluées », les contrôles hors périmètre sont « sans objet » : ni l'un ni
l'autre ne vaut conformité démontrée.

Le vérificateur DSFR contrôle les classes CSS et les assets locaux, pas la
conformité globale ni le RGAA. **Sans classe `fr-*`, il indique « non évalué »
et retourne 1**, au lieu d'un succès à 100 %. Ses tests s'exécutent hors réseau :

```bash
python3 -m unittest discover -s skills/fr-gov/design-system/fr-gov-set-up-design-system/tests -v
```

Le [protocole d'évaluation](skills/fr-gov/compliance/fr-gov-audit-app-compliance/references/evaluation-efficiency.md)
permet de comparer qualité, faux positifs, durée, tokens et interventions
humaines avec et sans skills. Il ne constitue pas un benchmark déjà exécuté.

## Tests

Quatre suites de non-régression s'exécutent hors réseau et sont lancées par la
CI (`Skills tests`) :

```bash
python -m pip install pyyaml python-docx

# Rendu DAT : typographie française et modèle Word par défaut
python3 -m unittest discover -s skills/fr-gov/compliance/fr-gov-render-technical-architecture-docx/tests -v

# Vérificateur DSFR : classes CSS et assets locaux
python3 -m unittest discover -s skills/fr-gov/design-system/fr-gov-set-up-design-system/tests -v

# Permissions des appels de workflows réutilisables
python3 -m unittest discover -s skills/fr-gov/devops/fr-gov-set-up-cloud-pi-native-cicd/tests -v

# Smoke-test : credentials synthétiques et transport simulé
python3 -m unittest discover -s skills/fr-gov/devops/smoke-test-api/tests -v

# Script d'installation (Hermes, OpenCode, Kilo Code, Claude Code)
python3 scripts/check-skill-catalog.py
./scripts/test-install-skills.sh
```

Le script d'installation s'exécute dans un répertoire temporaire : il n'écrit
rien dans le répertoire de skills réel de l'utilisateur.

## Maintenance autonome

Les skills sont maintenus et validés directement dans ce dépôt. Aucune PR ni
validation dans un dépôt d'origine n'est requise. Les fichiers `UPSTREAM.md`
documentent la provenance ; ils ne constituent pas une procédure de synchronisation
obligatoire. Les références internes sont embarquées avec chaque skill.

`review-code` charge uniquement la revue, le rituel ou les standards
nécessaires à la tâche. Son historique et ses adaptations sont décrits dans
son [`UPSTREAM.md`](skills/fr-gov/code/review-code/UPSTREAM.md).

L'installation des skills copie les fichiers locaux sans récupérer d'autres
skills. Les outils et services propres aux tâches (Helm, API data.gouv.fr,
workflows CI, etc.) restent des prérequis à vérifier selon le besoin.

## Workflow

Voir [`WORKFLOW.md`](WORKFLOW.md) — règle d'or : `bash .github/workflows/save-workflow.sh "<motif>"` avant tout gros changement.
