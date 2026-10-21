---
name: gouv-fr-code-index
description: "Choisir les skills gouv-fr pertinents pour une tâche de construction, audit ou déploiement ; utiliser pour une demande générale ou couvrant plusieurs domaines."
category: architecture
version: 0.2.1
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [gouv-fr, sovereign, france, etat, government, app, build, dsfr, rgaa, index]
    related_skills: [gouv-fr-projet-structure, gouv-fr-securite, gouv-fr-compliance-rgaa, gouv-fr-workflow-dev, gouv-fr-repo-init]
---

# Gouv-fr — Routage des skills

Choisir le skill le plus précis pour la demande. Ne pas charger tout le
catalogue ni tous les `related_skills` : ces liens indiquent des ressources,
pas une chaîne d'exécution obligatoire.

| Demande | Skill à charger en premier |
|---|---|
| Vérifier la sûreté d'un dépôt inconnu | `gouv-fr-audit-safety` |
| Auditer la conformité d'une application | `gouv-fr-audit-conformite` |
| Revoir une PR ou mesurer la dette | `gouv-fr-code-quality` |
| Diagnostiquer un bug | `gouv-fr-bug-investigation` |
| Organiser un changement transversal | `gouv-fr-workflow-dev` |
| Créer un dépôt ou choisir une stack | `gouv-fr-repo-init`, puis `gouv-fr-stack-technique` si nécessaire |
| Intégrer le DSFR | `gouv-fr-design-system` ; choisir `gouv-fr-react-dsfr` ou `gouv-fr-composants-vue` selon la stack |
| Préparer un chart CPiN | `gouv-fr-helm-chart` |
| Configurer la CI/CD CPiN | `gouv-fr-repo-cicd` |
| Examiner un tool derrière OpenWebUI | `gouv-fr-audit-openwebui` |
| Préparer un DAT | `gouv-fr-dat-homologation`, puis `gouv-fr-dat-word` pour le rendu |
| Consulter des guides ANSSI | `gouv-fr-anssi-guides` |
| Interroger data.gouv.fr | `gouv-fr-datagouv-apis` |

Pour un autre besoin, consulter les descriptions du catalogue `SKILLS.md`
à la racine du dépôt source. Charger les références longues uniquement
pour l'étape concernée. Appliquer les contrôles pertinents à la stack observée.
