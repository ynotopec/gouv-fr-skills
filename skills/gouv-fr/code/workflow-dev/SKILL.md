---

name: workflow-dev
description: "Organiser une tâche de développement, correction ou PR : processus proportionné, validation adaptée et suivi durable seulement si utile."
version: 0.1.2
license: MIT
platforms: [linux, macos]
author: etalab-ia
metadata:
  hermes:
    tags: [gouv-fr, workflow, plan-mode, task-management, self-improvement, bug-fixing, code-quality]
    related_skills: [projet-structure, securite, workflow-dev]
---

# Gouv-fr — Workflow de développement

## Choisir un processus proportionné

Lire les consignes du dépôt et la demande avant de choisir les étapes.
Pour une correction locale et réversible : inspecter, corriger, vérifier et
livrer directement. Respecter le style et les outils existants.

Pour un changement transversal ou une décision d'architecture : formuler un
plan court et le suivre. Utiliser le suivi de tâches déjà présent ; créer
`tasks/todo.md` seulement si demandé ou utile à une reprise durable.
Ne pas demander une nouvelle validation pour une action déjà autorisée.
Demander une précision uniquement si une information indispensable manque.

## Auditer et corriger

- Une demande d'audit seule reste en lecture seule : constats, preuves, limites.
- Une demande de correction ou de PR autorise les changements correspondants.
- Reproduire un bug lorsque possible, corriger sa cause et vérifier le comportement.
- Choisir les tests selon le risque ; éviter de créer des tests qui recopient
  l'implémentation ou d'imposer une suite étrangère à la stack.
- Conserver une leçon seulement si elle est réutilisable et si un journal est
  demandé ou prévu par le dépôt ; éviter un fichier après chaque petite correction.

## Livrer

1. Préserver les modifications préexistantes et travailler sur une branche dédiée.
2. Vérifier le changement avec les outils du projet.
3. Mettre à jour la documentation si le comportement change.
4. Respecter les conventions de commit et de PR du dépôt.
5. Résumer le résultat, les vérifications et les limites ; ne pas auto-fusionner.
