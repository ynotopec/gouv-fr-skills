# Passe d’hygiène


La revue décide de ce qui entre ; le rituel s'occupe de ce qui est déjà entré.
À lancer **à intervalle régulier** (hebdomadaire recommandé), pas seulement à
la fusion.

Trois niveaux d'autorisation — appliquer le moins permissif compatible avec
la demande :

- **AUDIT** (défaut) : inspecter et mesurer sans modifier l'arbre de travail —
  rapports et caches d'outils dirigés hors du dépôt, pas d'installation, pas
  de `--fix`, pas de commit ; comparer l'état git avant/après la passe et
  signaler toute mutation inattendue ;
- **JOURNAL** : créer ou compléter `hygiene-log.md`, si c'est demandé ;
- **REMÉDIATION** : refactoriser dans le périmètre demandé, puis re-tester et
  re-mesurer — livraison selon la section correspondante de `../SKILL.md`.

Déroulé en quatre temps :

1. **Mesurer l'état de la base.** Produire les métriques de dette avec des
   commandes reproductibles — consigner pour chacune l'outil, sa version et la
   ligne de commande exacte :
   - duplication : `npx jscpd --min-tokens 50 .` (multi-langages) ; à défaut
     `pylint --disable=all --enable=duplicate-code` (Python) ou `pmd cpd` ;
   - complexité cyclomatique : `radon cc -s -a .` ou `lizard` (Python /
     multi-langages), règle `complexity` d'ESLint (JS/TS) — repère : signaler
     les fonctions au-dessus de 15 ;
   - couverture de tests : l'outil du projet (`pytest --cov`,
     `npx vitest run --coverage`, `go test -cover`…) ;
   - vulnérabilités : `npm audit --audit-level=high`, `pip-audit` ou
     `trivy fs .` — mesure **contextuelle** : la base d'avis évolue chaque
     jour, noter sa date et ne pas intégrer ce compte à la courbe comparée ;
   - volume : `git ls-files | wc -l` (fichiers) et
     `git ls-files | xargs wc -l | tail -1` (lignes), ou `cloc` si disponible.

   En AUDIT, utiliser uniquement les outils disponibles sans téléchargement
   implicite : `npx`, `pipx run` et `uvx` peuvent installer du code. Outil absent :
   mesure indisponible. Installer uniquement si la demande l’autorise.

2. **Comparer à la passe précédente.** Chercher le relevé antérieur (fichier
   `hygiene-log.md` à la racine du projet, au format défini dans
   `hygiene-log-format.md`). Première passe → c'est l'état zéro ;
   le créer seulement en mode JOURNAL ou si la REMÉDIATION autorise ce suivi.
   En AUDIT, rendre l’état zéro dans le rapport sans créer de fichier. D'une passe à l'autre : **mêmes outils, mêmes flags** — sinon la
   courbe est incomparable et il faut le signaler.

3. **Recommander les passes de refactorisation ciblées.** À partir des
   mesures, proposer 1 à 3 actions *bornées et vérifiables*, les plus
   rentables d'abord — typiquement : « refactorise toutes les instanciations
   de X en une seule implémentation », « extrais l'utilitaire dupliqué dans
   N fichiers », « ajoute des tests sur le module le moins couvert avant de
   le toucher ». Chaque action recommandée doit être accompagnée de tests qui
   protègent le comportement pendant la refactorisation.

4. **Re-mesurer et tracer la courbe.** Après une REMÉDIATION, refaire les mesures ;
   consigner dans le journal seulement si ce suivi est autorisé, sinon dans
   le rapport (date, métriques, actions menées), et dire si la
   courbe descend, stagne ou monte. C'est la courbe — pas l'impression — qui
   dit si la dette dégonfle.

Règle du rituel : petit et régulier bat gros et rare. Une passe d'une heure
par semaine qui fait baisser la duplication de 1 % vaut mieux qu'un grand
nettoyage annuel que personne n'ose lancer.
