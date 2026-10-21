---

name: code-quality
description: Revue de code et dette, avec preuves et verdict.
version: 1.2.0
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [gouv-fr, quality, code-review, ia, dette-technique, lint, tests, standards]
    related_skills: [lint-format, conventions-developpement, projet-structure]
---

# Gouv-fr — Qualité de code et revue

## Quand utiliser

- Revoir une PR ou du code existant, mesurer la dette, guider une correction.
- Produire un verdict argumenté plutôt qu'une liste d'impressions.

Ne pas utiliser pour corriger un bug dont la cause est inconnue : commencer par
`bug-investigation`.

## Choisir le mode

| Demande | Référence à charger |
|---|---|
| Revoir une PR, un diff ou du code | `references/revue.md` : recevabilité, fond, statut, verdict |
| Mesurer ou réduire la dette | `references/rituel.md` : métriques et comparaisons reproductibles |
| Produire du code sans convention existante | `references/standards.md` : repères de style et tests |

Charger uniquement les références utiles au mode choisi. La revue ne déclenche
pas automatiquement une passe de dette ou une réécriture stylistique.

## Règles communes

- Respecter les consignes et la stack du dépôt. Proportionner les contrôles au risque.
- Sur une inspection seule, rester en lecture seule : aucun téléchargement,
  installation, journal, correction ou commit. Diriger les caches hors du dépôt
  si possible et relever l’état initial/final.
- Une demande de correction ou de PR autorise les changements nécessaires dans
  ce périmètre ; préserver les modifications préexistantes et ne pas redemander
  un accord déjà donné. Créer un journal seulement si demandé ou prévu par le dépôt.
- Distinguer conforme, écart confirmé, non évalué et sans objet, avec preuves
  précises. Une absence d’accès ne prouve ni défaut ni conformité.
- Rendre le compte rendu dans la langue de l’utilisateur. Ne pas bloquer une
  contribution sur une préférence de style ou un seuil de longueur seul.
- Conserver le balayage critique même si la contribution n’est pas révisable.
  Ne pas accepter avec un contrôle indispensable non évalué.

## Ressources complémentaires

- `references/checklist.md` : charger pour une revue exhaustive.
- `references/hygiene-log-format.md` : charger pour un suivi demandé ou existant.
- `references/pr-template.md` : charger pour livrer une correction.
- `references/evaluation-scenarios.md` : utiliser pour valider une évolution du skill.

## Livraison des changements

Travailler sur une branche dédiée, livrer une PR révisable avec intention,
propriétaire humain, preuves de comportement et limites de vérification.
Suivre les conventions du dépôt ; à défaut utiliser le modèle local
`references/pr-template.md`. Tracer l’assistance IA selon ces conventions ;
ne jamais inventer un identifiant de modèle non exposé. Ne pas auto-fusionner.

## Maintenance

Ce skill et ses références sont maintenus dans ce dépôt. Leur modification et
validation ne nécessitent aucune PR, installation de skill ou synchronisation
dans un dépôt tiers. L’origine historique est conservée dans `UPSTREAM.md`.
