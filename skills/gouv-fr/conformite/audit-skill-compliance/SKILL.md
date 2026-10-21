---

name: audit-skill-compliance
description: Audite la conformité d'une app aux skills gouv-fr.
version: 0.1.1
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [gouv-fr, audit, conformance]
    related_skills: [secure-coding-rules, check-web-compliance, init-repo]
---

# Gouv-fr — Audit de conformité d'une application

## Quand utiliser

- Auditer la conformité d'une application ou d'une PR aux skills gouv-fr.
- Vérifier qu'un livrable respecte les règles avant mise en production.

Audit en lecture seule par défaut : ne corrige que si la correction est demandée.

## Périmètre et mode

Auditer en **lecture seule par défaut** : ne pas installer d'outil, corriger,
créer de journal, committer ou réécrire l'historique sur une simple demande
de vérification. Une demande explicite de correction ou de PR autorise les
changements nécessaires dans ce périmètre ; ne pas redemander cet accord.
Inspecter les déclencheurs d'exécution avant de lancer les outils du projet
(voir `audit-repo-safety`). Ne jamais exécuter un script inconnu pour le découvrir.

1. Lire les consignes du dépôt et relever la stack, les points d'entrée, le
   déploiement réel et les commandes de validation déclarées.
2. Définir le périmètre : diff/PR, état courant ou historique demandé.
3. Appliquer uniquement les contrôles pertinents du tableau ci-dessous.
4. Rendre les constats avant toute remédiation ; poursuivre les contrôles
   indépendants même si l'un échoue. Arrêter seulement une exécution dangereuse.

## Contrôles adaptatifs

| Contrôle | Preuves à rechercher |
|---|---|
| Secrets | Scanner disponible/configuré, fichiers suivis et configuration. Distinguer références de secrets, fixtures synthétiques et valeurs réelles ; ne pas exclure une ligne sur la seule présence de `os.environ` ou `secretKeyRef`. Ne jamais reproduire la valeur d'un secret. |
| Historique | Scanner l'historique lorsque demandé ou nécessaire pour rechercher une fuite passée. Signaler toute limite d'accès ; ne pas imposer de nouveaux trailers aux anciens commits. |
| SQL | Si SQL existe : suivre les entrées jusqu'aux requêtes et vérifier la paramétrisation. Une recherche textuelle est un indice, pas une preuve d'injection ni d'absence de faille. |
| TLS et isolation | Suivre la terminaison TLS et le runtime réellement utilisés : proxy, ingress, chart, manifests, Compose ou service hôte. Ne pas exiger `k8s/app.yaml`, une annotation ingress précise ou un UID fixé. |
| RGAA / DSFR | Si interface concernée : consulter `check-web-compliance` et `set-up-french-state-design-system`. Vérifier classes, structure, clavier et rendu selon les moyens disponibles ; un contrôle CSS ne prouve pas la conformité globale. |
| Données personnelles | Si présentes : examiner justification, minimisation, conservation, accès et mécanismes de suppression applicables. Ne pas interdire un champ à cause de son seul nom, ni conclure sur la seule présence d'une route `DELETE`. |
| Git | Appliquer les conventions du dépôt aux commits de la contribution. Relever l'état initial ; préserver les modifications préexistantes. Ne pas réécrire l'historique pour rendre un audit vert. |
| Tests | Utiliser les commandes déclarées par le projet et adaptées au changement : pytest, Vitest, Go, etc. Ne pas imposer pytest à une autre stack. Outil absent ou exécution bloquée : non évalué. |

## Résultats et remédiation

Pour chaque contrôle : **conforme**, **écart confirmé**, **non évalué**
(preuve ou accès manquant), ou **sans objet** (raison explicite).
Citer fichier/ligne ou commande, résultat, impact et correction proposée.
Ne jamais transformer une absence d'accès en défaut confirmé ou en conformité.
Prioriser les risques concrets ; distinguer les préférences de style.

Si la correction est demandée : travailler sur une branche dédiée, préserver
l'existant, corriger les causes et lancer les tests ciblés, puis les contrôles
transversaux concernés. Rejouer la suite complète si le changement ou les
consignes du dépôt le justifient. Livrer la PR et les limites de vérification.
Ne pas modifier d'autres skills ou systèmes sans lien avec la demande.

## Évaluer une évolution du skill

Utiliser `references/evaluation-efficiency.md` pour comparer les résultats
sans skill, avec la version précédente et avec la version proposée.
Ne pas revendiquer un gain de temps ou de tokens sans mesures comparables.
