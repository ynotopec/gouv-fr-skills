---

name: skills-router
description: Choisit les skills gouv-fr adaptés à la demande.
version: 0.2.2
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [gouv-fr, sovereign, france, etat, government, app, build, dsfr, rgaa, index]
    related_skills: [projet-structure, developpement-securise, regles-conformite-web, workflow-dev, repo-init]
---

# Gouv-fr — Routage des skills

Choisir le skill le plus précis pour la demande. Ne pas charger tout le
catalogue ni tous les `related_skills` : ces liens indiquent des ressources,
pas une chaîne d'exécution obligatoire.

## Quand utiliser

- La demande est générale (« construis-moi cette app ») ou couvre plusieurs domaines.
- Il faut choisir le skill le plus précis avant de charger quoi que ce soit.

Ne charger qu'un skill à la fois : les liens `related_skills` indiquent des
ressources, pas une chaîne d'exécution.

| Demande | Skill à charger en premier |
|---|---|
| Vérifier la sûreté d'un dépôt inconnu | `audit-securite-depot` |
| Auditer la conformité d'une application | `audit-conformite` |
| Revoir une PR ou mesurer la dette | `code-quality` |
| Diagnostiquer un bug | `bug-investigation` |
| Organiser un changement transversal | `workflow-dev` |
| Créer un dépôt ou choisir une stack | `repo-init`, puis `stack-technique` si nécessaire |
| Intégrer le DSFR | `integration-dsfr` ; choisir `react-dsfr` ou `vue-dsfr` selon la stack |
| Préparer un chart CPiN | `helm-chart` |
| Configurer la CI/CD CPiN | `cicd-cloud-pi-native` |
| Examiner un tool derrière OpenWebUI | `audit-identite-outils-llm` |
| Préparer un DAT | `document-homologation`, puis `homologation-word` pour le rendu |
| Consulter des guides ANSSI | `anssi-guides` |
| Interroger data.gouv.fr | `datagouv-apis` |

Pour un autre besoin, consulter les descriptions du catalogue `SKILLS.md`
à la racine du dépôt source. Charger les références longues uniquement
pour l'étape concernée. Appliquer les contrôles pertinents à la stack observée.
