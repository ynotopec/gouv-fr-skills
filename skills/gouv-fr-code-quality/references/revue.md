# Revue en trois niveaux

## Sommaire

- Méthode et statuts
- Niveau 1 : recevabilité et balayage critique
- Niveau 2 : qualité de fond
- Niveau 3 : statut et traçabilité
- Verdict global

## Méthode et statuts


Appliquer les trois niveaux **dans l'ordre**. Un échec au Niveau 1 stoppe la
revue : inutile de lire en détail un code qu'on ne peut pas assumer.

1. **Niveau 1 — Règles d'entrée** : vérifier *avant de lire le code* que la
   contribution est recevable et révisable. (Rétablit l'asymétrie coût.)
2. **Niveau 2 — Règles de fond** : vérifier la qualité *dans* le code.
3. **Niveau 3 — Règles de statut** : vérifier le *statut* du code (jetable vs
   durable) et sa traçabilité.

Pour chaque règle, attribuer :

- ✅ conforme — une preuve accessible soutient le critère ;
- ⚠️ à corriger — déficience réelle mais non bloquante ;
- ❌ bloquant — défaut confirmé qui empêche une fusion sûre ;
- ◻️ non évalué — la preuve ou l'accès manque ; ce n'est **pas** un défaut ;
- N/A — critère sans objet, avec justification.

**L'absence d'accès n'est jamais une preuve d'absence** : une information
inaccessible se cote ◻️ en disant ce qui manque, pas ❌. Puis rendre un
**verdict global motivé** (voir plus bas). Toujours citer des lignes/fichiers
précis — jamais un jugement vague.

Le détail exécutable de chaque point (questions à se poser, signaux d'alerte,
exemples) est dans `checklist.md`. Charger ce fichier lorsqu'une
revue complète et systématique est demandée.

---

## Niveau 1 — Règles d'entrée (avant de lire le code)

Un échec ici est en principe **bloquant** : on renvoie sans réviser.

Collecte des preuves selon le contexte :

- **PR GitHub** : `gh pr view <n> --json title,body,author,files` (intention,
  auteur), `gh pr diff <n> --stat` (taille et découpe), `gh pr checks <n>`
  (état des vérifications).
- **Branche / diff local** : `git log --format='%h %an %s' main..HEAD` et
  `git diff --stat main...HEAD` (adapter le nom de la branche principale).
- **Hors PR** (diff collé, fichier isolé) : les règles 1.1 et 1.2 se vérifient
  auprès de l'utilisateur — demander l'intention et qui assume ; coter **N/A**
  ce qui est sans objet (ex. la découpe d'une PR qui n'existe pas). Ne jamais
  inventer une intention ou un propriétaire pour combler un trou.

**Balayage critique, même si l'entrée échoue.** Une contribution non révisable
n'est pas renvoyée les yeux fermés : balayer le diff accessible à la recherche
des risques critiques évidents — secret exposé, injection, contrôle d'accès
affaibli, destruction de données ou migration irréversible, dépendance
suspecte — et les signaler. Sans présenter ce balayage comme une revue
complète.

1. **Intention déclarée** — La contribution énonce l'*effet recherché* (le
   « pourquoi »), pas seulement le diff. Pas d'intention lisible → refus.
2. **Propriétaire humain responsable** — Un humain nommé assume la PR. L'IA
   n'est jamais redevable ; un humain l'est toujours.
3. **Preuve de comportement** — Reproduction du bug, ou test qui échouait
   avant / passe après. On évalue un *comportement*, pas une esthétique.
4. **Coût de revue proportionné** — Une PR massive générée en minutes n'a pas
   droit à des heures de revue par défaut. Elle doit être rendue révisable :
   petite, ciblée, découpée, expliquée.

## Niveau 2 — Règles de fond (dans le code)

1. **Lisibilité / intention** — Le code se lit-il comme une explication de ce
   qu'il fait et pourquoi ? Nommage, structure, absence de complexité gratuite.
2. **Pas de duplication** — Cible n°1 du code IA (blocs clonés en forte hausse
   depuis l'arrivée des assistants). Est-ce refactorisé, ou copié-collé ?
3. **Justesse vérifiée ≠ « les tests passent »** — Les tests testent-ils le bon
   comportement, ou ont-ils été écrits pour verdir ? Se méfier de la « triche »
   (optimiser la mesure, pas l'intention).
4. **API et fonctions réelles** — Le code appelle-t-il uniquement ce qui existe
   vraiment ? Traquer les hallucinations (appels, méthodes, options inventés).
5. **Erreurs et cas limites** — Chemin nominal soigné mais bords négligés :
   entrées vides/nulles, concurrence, échecs réseau, valeurs extrêmes.
6. **Sécurité, secrets, dépendances** — Secrets en dur, dépendances hallucinées
   ou vulnérables, entrées non validées, injection.
7. **Surface de maintenance** — Ce code crée-t-il une dette qu'un humain devra
   porter longtemps ? Le gain justifie-t-il le poids ajouté ?

## Niveau 3 — Règles de statut (méta)

1. **Marquer le jetable comme jetable** — Tout prototype naît avec une « date
   de mort » ou une étiquette *non maintenu*. Le sacrificiel non étiqueté qui
   devient fondation par accident est la source réelle de dette.
2. **Une porte unique** — Le code d'un dirigeant ou d'une IA passe par la même
   revue que celui de n'importe qui. Aucun passe-droit hiérarchique ou
   technologique. (C'est la règle du noyau Linux.)
3. **Tracer l'origine IA** — Marquer le code généré (à la manière du tag
   `Assisted-by` du noyau Linux), non pour l'interdire, mais pour mesurer son
   taux de défaut réel dans le temps.

   *Calibration* : sur un dépôt qui ne trace encore rien, cette règle est
   **consultative** à la première application — ⚠️ au maximum, jamais ❌ ; on
   recommande d'instaurer la convention, on ne bloque pas. Dès qu'une
   convention existe (modèle de PR, CONTRIBUTING, trailer `Assisted-by`), elle
   devient **bloquante** : une contribution générée non déclarée est un ❌.
   Sans cette calibration, aucun dépôt réel n'atteindrait jamais ACCEPTER.

---

## Verdict global

Conclure toute revue par l'un des quatre verdicts, **motivé et actionnable**.
Appliquer la **première condition satisfaite**, dans cet ordre :

1. **REFUSER** — Des preuves suffisantes montrent que l'intention ou
   l'approche est fondamentalement mauvaise (justesse fausse, hallucination
   d'API confirmée, faille) et qu'une correction locale ne suffit pas.
   Expliquer pourquoi, brièvement, avec respect.
2. **NON RÉVISABLE** — Une information indispensable manque ou reste
   inaccessible (règle d'entrée en ❌ ou ◻️) et empêche une décision sûre.
   Fusion bloquée : rapporter le résultat du balayage critique, marquer les
   contrôles restants ◻️, et lister exactement ce qu'il faut fournir ou
   découper pour reprendre. Ne pas punir d'un REFUSER une information
   simplement inaccessible.
3. **CORRIGER** — Recevable sur le fond mais au moins un point ⚠️/❌ précis,
   réparable avant fusion. Lister chaque point avec fichier:ligne et l'action
   attendue.
4. **ACCEPTER** — Niveau 1 conforme, Niveau 2 sans ❌, Niveau 3 conforme *en
   tenant compte de la calibration de la règle 3.3* (consultative à la
   première application), et aucun contrôle indispensable resté ◻️. Réserves
   ⚠️ mineures listées mais non bloquantes.

Toujours : citer des emplacements précis, distinguer le bloquant du cosmétique,
et se rappeler que **refuser proprement fait partie du travail de qualité** —
la gentillesse est de dire non clairement plutôt que de laisser entrer une dette
que quelqu'un paiera en silence.

Enfin, identifier le réviseur et le modèle seulement s’il est exposé par
l’environnement ; sinon écrire « non exposé par l’environnement ».
