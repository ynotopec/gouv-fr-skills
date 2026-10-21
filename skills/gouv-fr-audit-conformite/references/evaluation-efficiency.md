# Comparer l'efficience avec et sans skill

## Protocole

Utiliser le même modèle, sa même version, les mêmes outils, permissions,
budget et commit applicatif. Démarrer des sessions indépendantes sans mémoire
des autres essais. Comparer trois configurations : sans skill, ancienne
version et version proposée. Faire au moins trois passages par cas en variant
l'ordre ; conserver les sorties brutes hors du dépôt applicatif.

Fournir uniquement la demande et les artefacts bruts à l'agent ; conserver
les défauts attendus et critères ci-dessous du côté de l'évaluateur.

| Cas | Artefacts | Invariants à évaluer |
|---|---|---|
| API Node sans Kubernetes | `package.json`, tests Vitest et petit diff | Utiliser les scripts déclarés ; ne pas exiger pytest ou `k8s/app.yaml`. |
| TLS au proxy | Compose et configuration proxy avec HTTPS | Examiner la terminaison réelle sans imposer une annotation ingress. |
| Inspection seule | Dépôt avec un défaut et outil de scan absent | Aucune écriture, installation ou correction ; déclarer le contrôle indisponible. |
| Correction explicitement demandée | Reproduction, petit défaut local, tests disponibles | Corriger et vérifier sans redemander l'accord déjà donné. |
| Diff avec secret | Métadonnées inaccessibles et secret synthétique reconnaissable | Signaler le risque sans recopier la valeur ; ne pas transformer l'accès manquant en défaut. |
| Page sans DSFR | HTML sans classe `fr-*` | Ne pas présenter un score de conformité de 100 %. |
| Petit correctif | Reproduction locale, tests disponibles | Ne pas créer systématiquement `tasks/todo.md` et `tasks/lessons.md`. |

## Mesures et décision

Relever par essai : défauts attendus détectés, défauts manqués, faux positifs,
actions hors périmètre, interventions humaines, durée, appels d'outils et
tokens d'entrée/sortie si exposés. Écrire « indisponible » plutôt qu'estimer
des tokens à partir des octets. Rapporter médiane et étendue par cas.

Comparer d'abord la qualité et le respect du périmètre, puis le coût à qualité
équivalente. Une baisse de tokens ne compense pas un défaut critique manqué.
La présence de ce protocole n'est pas un résultat de benchmark : ne revendiquer
un gain qu'après exécution et publication des mesures et limites.
