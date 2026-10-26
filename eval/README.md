# Évaluation des skills

Depuis la racine du dépôt, avec Python 3.12+, `pyyaml`, `python-docx`,
`jq`, `curl` et `sh` (les mêmes dépendances que les tests existants) :

```sh
python3 eval/audit_skills.py
python3 eval/integration_tests.py
```

Les rapports JSON et HTML sont écrits dans `eval/generated/`, hors Git.
Les commandes acceptent `--root` et `--output-dir` ; le runner accepte
`--timeout` (120 secondes par suite par défaut).

- **Audit** : valide les sources présentes et réutilise
  `scripts/check-skill-catalog.py` pour les règles du catalogue, le routage,
  les liens et les migrations. Le contrôle des secrets est une heuristique
  limitée sur `SKILL.md`, pas un audit de sécurité.
- **Intégration** : exécute les suites réelles de rendu DOCX, de vérification
  DSFR, de workflows CPiN, de règles Helm, de smoke API et de catalogue ANSSI.
  Ces suites utilisent des fixtures locales sans appeler de fournisseur IA.
  Les tests de scaffolding multi-framework restent exécutés par le job
  `scaffolds` du workflow `Skills tests`.
- **PASS** : les contrôles exécutés ont réussi. **FAIL** : un contrôle a échoué.
  **ERROR** : l'exécution est impossible, expire ou ne lance aucun test.
  **SKIP** : pas de suite enregistrée ou suite partiellement ignorée ; aucune
  validation comportementale n'est revendiquée.

FAIL et ERROR produisent un code de sortie non nul. Les rapports distinguent
les contrôles structurels des tests comportementaux. Aucun score de qualité
LLM ni pourcentage de conformité métier n'est déduit de ces tests.

La CI exécute les deux commandes, teste leur gestion des régressions et publie
les rapports, même lorsqu'un contrôle échoue. Les anciens résultats figés ont
été retirés pour éviter de les confondre avec l'état du commit courant.
