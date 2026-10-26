---

name: fr-gov-check-web-compliance
description: RGAA criteria, sample, DSFR interface, RGPD checklist
version: 0.2.0
license: MIT
author: etalab-ia
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [gouv-fr, compliance, rgaa, dsfr, rgpd, accessibility, etat, design-system, data-protection]
    related_skills: [fr-gov-set-up-design-system, fr-gov-set-up-project-layout, fr-gov-secure-coding-rules, fr-gov-configure-cookie-consent]
---

# Gouv-fr — Conformité web (RGAA, DSFR, RGPD)

Évaluer une application de l'État contre trois référentiels et **produire des constats
opposables**. Ce skill porte les listes exhaustives et la méthode d'évaluation ; il
ne rédige ni la déclaration d'accessibilité ni les preuves d'audit — pour cela, voir
`fr-gov-audit-app-compliance`.

## Quand utiliser

- Passer une application au crible avant livraison ou avant homologation.
- Cadrer les règles de conformité d'un nouveau projet.
- Répondre à « est-ce qu'on est conformes ? » avec un taux et une liste de critères, pas une impression.

Ne pas utiliser pour un audit officiel ou une déclaration d'accessibilité : l'échantillon, les
preuves et les limites de portée relèvent de `fr-gov-audit-app-compliance`.

## Ce qui rend une évaluation valide

Une case cochée vaut pour **tout l'échantillon**, jamais pour la page ouverte au moment du test.

- **Échantillon minimal** : accueil, contact, mentions légales, page d'accessibilité, plan du site,
  aide, authentification (celles qui existent), une page par type de service, un document
  téléchargeable par type de service, toutes les pages d'un processus, des pages de présentation
  distincte, et **au moins 10 % de pages tirées au hasard**.
- Un critère est **validé** s'il l'est sur toutes les pages de l'échantillon ; un seul élément en
  échec l'invalide. Un critère est **applicable** dès qu'il l'est sur une page.
- **Taux de conformité = critères validés / critères applicables.** Le taux moyen du service est la
  moyenne des taux par page : deux chiffres différents, ne pas les confondre dans un rapport.
- Un critère n'est **non applicable** que pour trois raisons : contenu absent, contenu exempté,
  dérogation pour charge disproportionnée **assortie** d'une alternative numérique accessible.

## 1. RGAA — 105 critères, 13 thématiques

Liste complète, intitulés officiels non reformulés : `references/rgaa-checklist.md`.
RGAA 4.1.2 en vigueur, RGAA 5 annoncé pour fin 2026 — revérifier la version avant un audit officiel.

| Thème | Critères | Thème | Critères |
|---|---|---|---|
| 1. Images | 9 | 8. Éléments obligatoires | 10 |
| 2. Cadres | 2 | 9. Structuration de l'information | 4 |
| 3. Couleurs | 3 | 10. Présentation de l'information | 13 |
| 4. Multimédia | 13 | 11. Formulaires | 13 |
| 5. Tableaux | 8 | 12. Navigation | 11 |
| 6. Liens | 2 | 13. Consultation | 12 |
| 7. Scripts | 5 | **Total** | **105** |

Les critères de la thématique Scripts exigent un **environnement de test** déclaré (navigateur +
technologies d'assistance). Sans environnement déclaré, ces critères sont *non évalués* — les
compter conformes est la faute la plus fréquente des audits internes.

## 2. DSFR

- Composants et tokens officiels uniquement ; toute personnalisation de couleur, d'espacement ou de
  typographie sort du DSFR et doit être justifiée.
- La source de vérité est le CSS officiel, pas une liste de classes mémorisée : `fr-gov-set-up-design-system`
  fournit `scripts/verify_dsfr.py`, qui compare chaque classe `fr-*` du HTML aux sélecteurs réels.
- Installation, versions et composants : `fr-gov-set-up-design-system` ; icônes et pictogrammes :
  `fr-gov-add-design-system-icons`.

## 3. RGPD

Checklist de 20 points avec les articles : `references/rgpd-checklist.md`. Les quatre manquements
qui reviennent le plus : base légale absente, durées de conservation non appliquées techniquement,
aucune procédure de violation à 72 h, données réelles en environnement de test.

Traceurs et bandeau : `fr-gov-configure-cookie-consent`.

## Vérification

Les outils automatisés ne valident qu'une partie des critères ; ils servent à **dégrossir**, pas à
conclure. Le reste est manuel (lecture du DOM, navigation clavier, technologies d'assistance).

```bash
# Accessibilité : erreurs WCAG 2 AA sur une page
npx pa11y https://exemple.gouv.fr --standard WCAG2AA --reporter cli

# Moteur axe (complémentaire, autres règles)
npx @axe-core/cli https://exemple.gouv.fr --exit

# Classes DSFR réellement définies dans le CSS officiel
python3 scripts/verify_dsfr.py dist/index.html

# Traceurs tiers déposés sans consentement
grep -rniE "googletagmanager|gtag\(|hotjar|facebook\.net|matomo" src/ public/ --include='*.html' --include='*.js'
```

Critère de sortie : rapport listant, par critère RGAA, `validé` / `non validé` / `non applicable` /
`non évalué`, avec le taux de conformité calculé sur les applicables — et la date de l'évaluation.

## Pièges

- **Une liste de bonnes pratiques n'est pas une checklist.** Six puces « contraste, clavier, alt,
  sémantique, ARIA, tests auto » ne couvrent pas 105 critères : cocher ces six lignes et annoncer
  « conforme RGAA » est un faux positif, pas une évaluation.
- **Le taux de conformité ne mesure pas l'accessibilité réelle** : 100 % sur un échantillon mal
  choisi reste non conforme. Documenter l'échantillon fait partie du résultat.
- **Un test automatisé vert ne dit rien des critères manuels** (ordre de lecture, pertinence des
  alternatives, cohérence des intitulés, pièges au clavier).
- **RGAA et RGPD ne se recouvrent pas** : deux référentiels, deux jeux de preuves, deux dates.
- **`non applicable` et `non évalué` ne sont pas synonymes** ; les additionner gonfle le taux.

