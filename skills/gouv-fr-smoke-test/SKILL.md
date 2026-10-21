---
name: gouv-fr-smoke-test
description: Smoke-test rapide du pipeline mirai-mesreunions (gateway + auth + ingester). Vérifie GET /api/meetings, GET /audio, POST /transcription avec un device_token synthétique. Spécifique projet mirai-mesreunions. À lancer uniquement sur demande explicite de l’utilisateur (appels réseau vers un environnement réel).
category: devops
version: 1.1.0
license: MIT
author: Hermes Agent
platforms: [linux, macos]
metadata:
  hermes:
    tags: [gouv-fr, smoke-test, mirai, pipeline, gateway, ingester]
    related_skills: [gouv-fr-service-names, gouv-fr-repo-cicd]
---

# Gouv-fr — Smoke-test du pipeline mirai-mesreunions

Exécuter uniquement sur demande explicite, sur l'environnement autorisé.
Le test inclut une création de job de transcription ; ne pas le traiter
comme une inspection en lecture seule.

## Préparer les entrées

1. Résoudre l'origine HTTPS dans la configuration du dépôt applicatif et la
   demande. Si elle reste inconnue, demander l'information manquante ; ne pas
   déduire un domaine ou un environnement depuis une mémoire non fournie.
2. Choisir une réunion de test autorisée et un échantillon synthétique M4A
   valide, non vide, de 10 Mio maximum. Ne pas renommer un WebM en M4A.
3. Utiliser les credentials déjà injectés dans l'environnement du processus :
   `SMOKE_TOKEN` en priorité, sinon `INTERNAL_API_TOKEN`. Avec ce dernier,
   le script forge en mémoire un device_token HMAC valable une heure, puis
   le réutilise pour les trois appels. Il ne sonde pas Keycloak.

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
python3 <chemin-du-skill>/scripts/run_smoke.py   --base https://api.environnement.example   --meeting-id identifiant-reunion-de-test   --audio-file /chemin/echantillon-synthetique.m4a
```

L'origine et les chemins ci-dessus sont des exemples à remplacer par les
entrées autorisées ; ne jamais exécuter un exemple tel quel.

| Appel | Validation |
|---|---|
| `GET /api/meetings` | HTTP 200 et liste JSON non vide |
| `GET /audio?meeting_id=…` | HTTP 200 et Content-Type `audio/webm` |
| `POST /api/transcription` | Multipart M4A, HTTP 202 et `job_id` présent |

Le script n'affiche que les statuts. Il ne suit aucune redirection, maintient
la vérification TLS et n'affiche pas les corps de réponse, URLs d'erreur ou
en-têtes. Il ne passe aucun token en argument de processus et n'écrit aucun
credential sur disque. Une liste vide interrompt la suite : les deux autres
contrôles sont non évalués, pas conformes.

## Verdict et limites

Code 0 : les trois contrôles passent. Code 1 : échec ou contrôle non évalué ;
rapporter le statut et les informations manquantes, sans secret ni corps brut.

Le POST peut créer un job, écrire en stockage et consommer des ressources.
Respecter les données de test et la politique de nettoyage du projet ; ne
pas lancer de suppression sans autorisation. Ce test ne mesure pas la qualité
ni la fin de la transcription et ne valide pas un déploiement à lui seul.

## Vérifier une modification du skill

`python3 -m unittest discover -s skills/gouv-fr-smoke-test/tests -v`

Les tests utilisent des credentials synthétiques et un transport simulé ;
ils ne prouvent pas la compatibilité avec un environnement réel. Vérifier le
contrat d'authentification du projet avant la première exécution réelle.

---

**Env cible** : $ARGUMENTS

Si l'agent ne substitue pas les arguments, les prendre dans la demande.
