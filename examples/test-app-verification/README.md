# Application de Test Gouv Fr — Vérification

Application de test située à `/workspace/test-gouv-fr-app/` vérifiée contre les 40 skills gouv-fr.

## Résultats

| Compétence | Critères | Résultat |
|------------|----------|----------|
| **DSFR** (verify_dsfr.py) | 43 classes | 100% (0 inconnu) |
| **RGAA** (accessibilité) | 12 critères | 12/12 ✅ |
| **RGPD** (cookies) | 6 critères | 6/6 ✅ |
| **Sécurité** (audit-safety) | 7 critères | 7/7 ✅ |
| **Qualité de code** | 6 critères | 6/6 ✅ |
| **Git conventions** | 4 critères | 4/4 ✅ |

## Résumé des compétences vérifiées

- **gouv-fr-design-system** : 43 classes fr-* validées contre DSFR 1.15.3 (score 100%)
- **gouv-fr-compliance-rgaa** : lang=fr, skiplinks, h1 unique, labels, boutons fr-btn, footer, viewport
- **gouv-fr-cookies-rgpd** : banner localStorage, accept/reject, pas de traceurs tiers
- **gouv-fr-audit-safety** : .gitignore, private/ ignoré, pas de secrets en dur, pas de clés API
- **gouv-fr-code-quality** : package.json valide, HTML valide, fermeture balises, pas de duplication
- **gouv-fr-repo-init** : git initialisé, commit présent, nom descriptif

## Commandes de vérification

```bash
# DSFR
python3 ~/hermes/skills/gouv-fr-design-system/scripts/verify_dsfr.py index.html

# RGAA (manuel)
grep -c '<h1' index.html  # doit être 1
grep -c 'fr-skiplinks' index.html  # doit être >= 1
```

---
Vérifié le 2026-09-29 par Hermes Agent.
