# Revue complète du dépôt gouv-fr-skills

**Date** : 2026-09-29 · **Périmètre** : 40 skills, index, documentation, infrastructure Git
**Verdict global** : le dépôt était **cassé sur 12 points bloquants** ; tous corrigés dans ce commit.

---

## Résumé exécutif

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

### Doublon partiel : `gouv-fr-code-quality` / `gouv-fr-qualite-code`

Les deux traitent de la qualité de code mais sous un angle distinct :

| Skill | Angle | Taille |
|-------|-------|--------|
| `gouv-fr-code-quality` | Grille de revue du code généré par IA (dette, maintenabilité) | 13 631 car. |
| `gouv-fr-qualite-code` | Bonnes pratiques concrètes : lint, formattage, tests | 4 182 car. |

**Recommandation** : conserver les deux mais croiser les renvois, ou fusionner dans
`gouv-fr-code-quality` si l'on veut réduire la surface. *Non tranché — décision utilisateur.*

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
✅ 40/40 skills : SKILL.md présent
✅ 40/40 : frontmatter YAML valide
✅ 40/40 : name == nom du répertoire
✅ 40/40 : description et category renseignées
✅ 40/40 : corps non vide (> 100 caractères)
✅ 40/40 : aucun header de section en anglais
✅ 40/40 : related_skills pointent vers des skills existants
✅ 40/40 : mentions gouv-fr-* dans le corps résolues
✅ 0 lien cassé dans README.md et SKILLS.md
✅ Hermes resynchronisé (40 skills)
```

## État Git

- Branche : `main`
- Sauvegardes disponibles : `backup/20260929-170614`
- Script de sauvegarde : `.github/workflows/save-workflow.sh`
