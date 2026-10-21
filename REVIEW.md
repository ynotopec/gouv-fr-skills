# Revue complète du dépôt gouv-fr-skills

**Date** : 2026-09-29 · **Périmètre** : 39 skills (40 avant consolidation), index, documentation, infrastructure Git
**Verdict global** : le dépôt était **cassé sur 12 points bloquants** ; tous corrigés dans ce commit.

---

## Passe de correction du 2026-10-21

Une seconde passe, issue de la revue du catalogue consolidé
(`dnum-mi/starter-kit-opencode`#42), a corrigé **4 défauts de fond** et
**2 manques d'infrastructure**. Les régressions ciblées sont couvertes par des tests ; les cas positifs
vérifient aussi les comportements qui fonctionnaient déjà. Les corrections
documentaires sont vérifiées séparément, sans prétendre à une preuve rouge→vert
pour chaque nouveau test.

### 🔴 Bloquants

#### 1. `gouv-fr-dat-word` : le modèle Word par défaut n'existait pas
`render_docx.py` visait `../dat-generation/dat/MODELE_DAT_MirAI.docx` — un
dossier **inexistant** dans ce dépôt. Tout appel sans `--model` échouait sur
`Modèle introuvable`, alors que le modèle est présent dans la skill sœur
`gouv-fr-dat-homologation`.

**Correction** : le chemin par défaut pointe vers `gouv-fr-dat-homologation`.
Couvert par `skills/gouv-fr-dat-word/tests/test_default_model.py`.

#### 2. `gouv-fr-repo-cicd` : les niveaux de permission n'étaient pas comparés
`verif-appels.py` ne comparait que la *présence* d'une permission et le cas
particulier `write`. Un job appelant accordant `contents: none` à un job
appelé exigeant `contents: read` **passait sans remarque**.

**Correction** : comparaison par rang `none < read < write`. Couvert par
`skills/gouv-fr-repo-cicd/tests/test_verif_appels.py` (5 cas).

### 🟠 Majeurs

#### 3. `gouv-fr-design-system` : `tel:` et `//` signalés comme assets manquants
`verify_dsfr.py` ignorait `http:`, `https:`, `data:`, `#` et `mailto:` — mais
pas `tel:` ni les URL protocol-relative (`//cdn…`). Un simple lien
« Appeler » suffisait à faire échouer la vérification avec un faux positif
`ASSET MANQUANT`.

**Correction** : les deux schémas sont ignorés. Couvert par
`test_non_http_schemes_are_not_missing_assets`.

#### 4. `gouv-fr-lint-eslint` : configuration Ruff refusée par Ruff
La section « Configuration (`ruff.toml`) » contenait en réalité la syntaxe
`pyproject.toml` (`[tool.ruff]`). Copié tel quel dans un `ruff.toml`, Ruff
échoue : `unknown field 'tool'`. Le bloc `[project.scripts]` était présenté
comme un `package.toml`, qui n'est pas un format de configuration reconnu.

**Correction** : la section est étiquetée `pyproject.toml`, la variante
`ruff.toml` est explicitée (retirer le préfixe `tool.ruff`), et les scripts
sont remplacés par les commandes réelles (`uv run ruff check .`).

#### 5. `gouv-fr-smoke-test` : le jeton était affiché
La recette imprimait le jeton produit par HMAC, l'exposant à la sortie de l'outil
et à la conversation. Lire le secret dans un processus autorisé n'implique
pas d'en exposer la valeur au modèle.

**Correction** : un script Python local utilise les credentials injectés
(`SMOKE_TOKEN` ou `INTERNAL_API_TOKEN`) et n'affiche que les statuts. Il forge
et réutilise le jeton en mémoire, sans étape humaine systématique, argument de
processus secret, fichier de credential ni redirection HTTP. Il exige des
données de test explicites et documente les effets du POST de transcription.
Neuf tests à transport simulé couvrent ce comportement, sans appeler de service réel.

#### 6. `scripts/test-install-skills.sh` : écriture hors du bac à sable
Le test isolait `HOME` et `XDG_CONFIG_HOME`, mais pas `HERMES_HOME`,
`KILO_HOME` ni `CLAUDE_HOME`. Sur une machine où ces variables sont
définies, le test **installait les 43 skills dans le répertoire de skills réel
de l'utilisateur**, en plus d'échouer.

**Correction** : les trois variables sont isolées vers le répertoire
temporaire. Le test n'écrit plus rien hors de `$TMPDIR`.

### 🟡 Infrastructure

#### 7. Deux suites de tests n'étaient jamais exécutées
Seul `skills/gouv-fr-design-system/tests` était branché sur la CI. Les tests
de `gouv-fr-dat-word` (typographie) et ceux de `gouv-fr-repo-cicd` (absents)
ne tournaient nulle part. `test_render_docx.py` appelait `sys.exit()` à
l'import, ce qui rendait son dossier **indécouvrable** par
`unittest discover`.

**Correction** : les vérifications de `test_render_docx.py` sont encapsulées
dans `run_checks()` et ne s'exécutent qu'en script ; `test_typography.py`
les branche sur unittest. Nouvelle CI `Skills tests` qui lance les trois
suites plus le test d'installation.

### Vérifications passées après correction

```
✅ 4 suites unittest : 26 tests au vert
✅ Test d'installation : 43 skills × 4 agents
✅ Cas de régression et cas positifs distingués ; aucune affirmation rouge→vert universelle
✅ Ruff 0.17 : la configuration documentée est acceptée dans les deux formes
✅ 0 écriture hors du répertoire temporaire lors du test d'installation
```

---

## Résumé exécutif (passe du 2026-09-29)

| Sévérité | Avant | Après |
|----------|-------|-------|
| 🔴 Bloquant (skill ne charge pas / contenu perdu) | 12 | 0 |
| 🟠 Majeur (documentation fausse, liens cassés) | 15 | 0 |
| 🟡 Mineur (incohérences de forme) | 20 | 0 |

Les skills étaient **fonctionnels en apparence** mais l'analyse a révélé des fichiers tronqués, du YAML invalide, des références croisées mortes et un index mensonger.

---

## 🔴 Problèmes bloquants (corrigés)

### 1. Cinq skills au corps vide

Contenu perdu lors d'un nettoyage automatique antérieur (`aaf26a6`), ne restait que le frontmatter.

| Skill | Taille avant | Restauration |
|-------|--------------|--------------|
| `gouv-fr-outils-developpement` | 0 car. | 8 275 car. (depuis `5c5d3e9`) |
| `gouv-fr-deployment-docker-k8s` | 0 car. | 6 047 car. |
| `gouv-fr-monorepo-pnpm` | 0 car. | 5 131 car. |

*Aucune invention : contenu récupéré de l'historique Git.*

### 2. Trois frontmatters YAML invalides

`description:` contenait `: ` sans guillemets → parsing YAML en échec, skill non indexable par Hermes.

- `gouv-fr-deployment-docker-k8s`
- `gouv-fr-monorepo-pnpm`
- `gouv-fr-stack-technique`

**Correction** : descriptions entre guillemets.

### 3. `gouv-fr-test-app` dans `skills/`

Un rapport de vérification (README seul, aucun SKILL.md) polluait le répertoire des skills.
**Correction** : déplacé vers `examples/test-app-verification/`.

### 4. `SKILLS.md` : 12 liens cassés sur 13

L'index utilisait les noms **d'avant renommage** (`gouv-fr-code`, `gouv-fr-code-project`,
`gouv-fr-code-security`…), tous inexistants depuis la refonte.
**Correction** : index régénéré depuis les 40 skills réels, groupés par catégorie.

### 5. `README.md` : 2 liens cassés + ligne parasite

- `gouv-fr-deploiement-docker-k8s` → `gouv-fr-deployment-docker-k8s`
- `gouv-fr-deploiement-cloud-pi-native` → `gouv-fr-deployment-cloud-pi-native`
- Ligne orpheline `# 🎯 gouv-fr-skills — 27 skills...` (compte obsolète : 40)
- 14 skills absents du README
**Correction** : README réécrit intégralement.

---

## 🟠 Problèmes majeurs (corrigés)

### 6. Vingt skills avec des références croisées périmées

Le champ `related_skills` (et les mentions dans le corps) pointait vers des noms supprimés :
`gouv-fr-code-project`, `gouv-fr-code-security`, `gouv-fr-code-compliance`, `gouv-fr-code-git`,
`gouv-fr-dsfr`, `gouv-fr-stack`, `gouv-fr-deploiement`, `gouv-fr-monorepo`, `gouv-fr-code-lint`…

**Correction** : 25 références réalignées sur les noms actuels
(`gouv-fr-projet-structure`, `gouv-fr-securite`, `gouv-fr-compliance-rgaa`, `gouv-fr-design-system`, etc.).

> ⚠️ Piège rencontré : un remplacement naïf par préfixe a produit des corruptions
> (`gouv-fr-code-index-quality`). Corrigé avec une regex token-entier `(?![-\w])`.

### 7. Noms périmés sans préfixe dans les corps

`helm-chart-cpin`, `cicd-fabnum`, `repo-cicd-cpin`, `audit-tool-owui`, `dat-generation`,
`conventions-cofabnum`, `environnement-installation`, `audit-pentest-prep` utilisaient encore
les noms d'origine.
**Correction** : réécrits vers les noms actuels (les noms de dépôts externes légitimes,
comme `dsfr-theme-tarteaucitron` ou `referentiel-donnees-communication-publique`, sont conservés).

### 8. Titres H1 incohérents

Plusieurs skills affichaient un titre ne correspondant plus à leur identifiant
(`# audit-tool-owui`, `# repo-cicd-cpin`, `# CoFabNum Server Recipes`, `# DSFR Artwork`…).
**Correction** : titres alignés sur le nom du skill.

---

## 🟡 Problèmes mineurs (corrigés)

### 9. Headers en anglais

Hermes reconnaît les sections en français. Des headers `## When to Use`, `## How to Run`,
`## Usage`, `## Prerequisites` subsistaient (dont dans les skills restaurés).
**Correction** : traduits (`## Quand utiliser`, `## Comment lancer`, `## Utilisation`, `## Prérequis`).

### 10. Catégorie non normalisée

`gouv-fr-securite` portait `category: securite` alors que tous les autres skills de sécurité
portent `category: security`.
**Correction** : harmonisé.

### 11. Contradiction `.gitignore`

`.gitignore` listait `backup-local-skills/` en ignoré, alors que ce répertoire **est**
versionné (souhait explicite de conserver la sauvegarde des skills locaux).
**Correction** : ligne retirée, commentaire explicitant le choix.

---

## Points d'attention non bloquants

### Doublon résolu : `gouv-fr-code-quality` / `gouv-fr-qualite-code`

Les deux traitaient de la qualité de code avec un recouvrement net (tests, erreurs,
dépendances) et des **noms quasi identiques** — source de confusion.

| Skill | Angle | Taille | Décision |
|-------|-------|--------|----------|
| `gouv-fr-code-quality` | Grille de revue + standards | 16 664 car. | **Conservé et enrichi** |
| `gouv-fr-qualite-code` | Lint, formattage, tests | 4 182 car. | **Fusionné puis supprimé** |

**Résolution** : les règles au quotidien (`qualite-code`) ont été intégrées dans
`gouv-fr-code-quality` sous la section « Standards de code — règles au quotidien »
(structure de fichier, fonctions, erreurs, async/await, imports, constantes,
early return, dépendances, tests). La configuration lint, déjà couverte par
`gouv-fr-lint-eslint`, n'a pas été dupliquée : renvoi croisé à la place.
Catégorie corrigée `devops` → `qualite`. Le nom unique lève l'ambiguïté.

### Fichiers référencés en exemple

Quatre chemins (`scripts/check-cpin-rules.py`, `templates/validation.yaml`, etc.) sont des
**faux positifs** : ils désignent la structure de charts générés ou des scripts d'autres skills,
pas des fichiers attendus dans le skill lui-même. Aucune action.

### Forme des frontmatters

`gouv-fr-code-quality` utilise un frontmatter plus ancien (pas de bloc `metadata.hermes`,
`tags: []` vide) contrairement aux autres.
**Recommandation** : aligner lors d'une prochaine passe (non bloquant).

---

## Vérifications passées après correction

```
✅ 39/39 skills : SKILL.md présent
✅ 39/39 : frontmatter YAML valide
✅ 39/39 : name == nom du répertoire
✅ 39/39 : description et category renseignées
✅ 39/39 : corps non vide (> 100 caractères)
✅ 39/39 : aucun header de section en anglais
✅ 39/39 : related_skills pointent vers des skills existants
✅ 39/39 : mentions gouv-fr-* dans le corps résolues
✅ 0 lien cassé dans README.md et SKILLS.md
✅ Hermes resynchronisé (39 skills)
```

## État Git

- Branche : `main`
- Sauvegardes disponibles : `backup/20260929-170614`
- Script de sauvegarde : `.github/workflows/save-workflow.sh`
