---

name: smoke-test
description: "Smoke-test d'une API en lecture et job asynchrone, sans exposer de secret. Vérifie liste, média et job avec un credential injecté dans l'environnement. Le contrat d'API est paramétrable ; à lancer uniquement sur demande explicite (appels réseau vers un environnement réel)."
version: 1.2.1
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [gouv-fr, smoke-test, api, credentials, pipeline]
    related_skills: [repo-cicd, securite]
---

# Gouv-fr — Smoke-test d'une API

Patron de vérification d'une API en trois contrôles : **liste** des
ressources, **média** associé, **job** asynchrone. Le contrat d'API (chemins,
paramètre d'identifiant, types de média) est fourni par l'appelant : le skill
ne dépend d'aucun projet particulier.

Exécuter uniquement sur demande explicite, sur l'environnement autorisé.
Le test inclut la création d'un job ; ne pas le traiter comme une
inspection en lecture seule.

## Préparer les entrées

1. Résoudre l'origine HTTPS dans la configuration du dépôt applicatif et la
   demande. Si elle reste inconnue, demander l'information manquante ; ne pas
   déduire un domaine ou un environnement depuis une mémoire non fournie.
2. Choisir une ressource de test autorisée et un échantillon synthétique du
   format attendu, valide, non vide, de 10 Mio maximum. Ne pas renommer un
   fichier d'un format en un autre (un WebM renommé en M4A n'est pas un M4A).
3. Utiliser les credentials déjà injectés dans l'environnement du processus :
   `SMOKE_TOKEN` en priorité, sinon `INTERNAL_API_TOKEN`. Avec ce dernier,
   le script forge en mémoire un jeton valable une heure, puis le réutilise
   pour les trois appels.

## Credentials et autonomie

L'agent peut lancer le script autorisé sans voir la valeur du secret : la
lecture de l'environnement, la signature et les en-têtes restent dans le
processus Python. Ne pas afficher l'environnement, utiliser `set -x`, recopier
un token dans la commande, la conversation, un journal ou un fichier.
Aucune génération manuelle systématique n'est requise.

Un export dans un autre shell n'est pas automatiquement disponible ici.
Si aucun credential n'est injecté, le script s'arrête avant tout appel réseau :
faire configurer l'injection par le mécanisme de secrets de l'environnement,
sans demander de coller la valeur dans la conversation.

## Exécuter

Charger `scripts/run_smoke.py` depuis le répertoire de ce skill. Bibliothèque
standard Python uniquement ; aucune installation supplémentaire.

```bash
python3 <chemin-du-skill>/scripts/run_smoke.py \
  --base https://api.environnement.example \
  --item-id identifiant-ressource-de-test \
  --audio-file /chemin/echantillon-synthetique.m4a
```

Les valeurs ci-dessus sont des exemples à remplacer par les entrées
autorisées ; ne jamais exécuter un exemple tel quel.

### Adapter le contrat d'API

| Option | Défaut | Rôle |
|---|---|---|
| `--list-path` | `/api/meetings` | Endpoint de la liste des ressources |
| `--item-path` | `/audio` | Endpoint de la ressource unitaire |
| `--job-path` | `/api/transcription` | Endpoint du job asynchrone |
| `--id-param` | `meeting_id` | Nom du paramètre d'identifiant |
| `--media-type` | `audio/webm` | Type de média attendu |
| `--audio-suffix` | `.m4a` | Extension du fichier de test |
| `--audio-content-type` | `audio/mp4` | Type de contenu du fichier de test |
| `--job-field` | `job_id` | Champ contenant l'identifiant du job |
| `--operation` | `transcription` | Valeur du champ multipart `operation` |

Les trois chemins doivent commencer par un unique `/`, sans origine externe,
fragment, antislash ou caractère de contrôle. Les paramètres de query sont
autorisés. Tous les endpoints sont validés avant lecture des credentials ou
appel réseau : ils restent sur l'origine HTTPS fournie par `--base`.

`--meeting-id` reste accepté comme alias de `--item-id`. Le contrat historique
`operation=transcription` est conservé par défaut ; adapter `--operation` au
contrat du service si nécessaire.

| Appel | Validation |
|---|---|
| Liste | HTTP 200 et tableau JSON non vide |
| Média | HTTP 200 et Content-Type conforme à `--media-type` |
| Job | Multipart, HTTP 202 et le champ `--job-field` présent |

Le script n'affiche que les statuts. Il ne suit aucune redirection, maintient
la vérification TLS et n'affiche pas les corps de réponse, URLs d'erreur ou
en-têtes. Il ne passe aucun token en argument de processus et n'écrit aucun
credential sur disque. Une liste vide interrompt la suite : les deux autres
contrôles sont non évalués, pas conformes.

## Verdict et limites

Code 0 : les trois contrôles passent. Code 1 : échec ou contrôle non évalué ;
rapporter le statut et les informations manquantes, sans secret ni corps brut.

Le job peut créer un traitement, écrire en stockage et consommer des
ressources. Respecter les données de test et la politique de nettoyage du
projet ; ne pas lancer de suppression sans autorisation. Ce test ne mesure pas
la qualité du traitement et ne valide pas un déploiement à lui seul.

## Vérifier une modification du skill

```
python3 -m unittest discover -s skills/gouv-fr/dso/smoke-test/tests -v
```

Les tests utilisent des credentials synthétiques et un transport simulé ;
ils ne prouvent pas la compatibilité avec un environnement réel. Vérifier le
contrat d'authentification du projet avant la première exécution réelle.

---

**Env cible** : $ARGUMENTS

Si l'agent ne substitue pas les arguments, les prendre dans la demande.
