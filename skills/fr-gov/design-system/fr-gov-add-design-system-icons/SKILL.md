---

name: fr-gov-add-design-system-icons
description: DSFR pictograms, SVG artwork, official icon classes
version: 0.2.0
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [dsfr, artwork, pictogram, icon, svg, illustration]
    related_skills: [fr-gov-set-up-design-system, fr-gov-check-web-compliance]
---

# Gouv-fr — Pictogrammes et icônes DSFR

Les assets visuels du DSFR (pictogrammes SVG, icônes, motifs décoratifs) sont inclus dans le paquet `@gouvfr/dsfr` — pas
de dépôt séparé à installer.

## Quand utiliser

- Intégrer un pictogramme ou une icône officielle dans une application DSFR.
- Ajouter un motif décoratif ou une illustration institutionnelle.

Don't use for: créer des pictogrammes hors charte, usage commercial hors État, logo Marianne (celui-ci est la classe CSS
`fr-logo`, gérée par le skill principal).

## Référence rapide
```bash
npm install @gouvfr/dsfr
```

```html
<!-- Pictogramme SVG (chemin réel, vérifié dans dist 1.15.4) -->
<img src="node_modules/@gouvfr/dsfr/dist/artwork/pictograms/buildings/city-hall.svg" alt="Hôtel de ville">

<!-- Icône par classe fr-icon-* (1044 icônes définies en 1.15.4) -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@gouvfr/dsfr@1.15.4/dist/utility/icons/icons.min.css">
<button class="fr-btn fr-icon-add-line">Ajouter</button>
```

## Procédure

### Emplacement des assets (vérifié dans le paquet 1.15.4 : 106 fichiers `dist/artwork/`)

- `dist/artwork/pictograms/<thème>/*.svg` — **102** pictogrammes, thèmes réels :
  `accessibility`, `buildings`, `digital`, `document`, `environment`, `health`,
  `institutions`, `leisure`, `map`, `system` (pas `systeme`).
- `dist/artwork/background/ovoid.svg`, `dist/artwork/light.svg`, `dist/artwork/dark.svg`,
  `dist/artwork/system.svg` — fonds décoratifs.

### Classes artwork dans le CSS officiel

Familles réellement définies : `fr-artwork`, `fr-artwork-decorative`, `fr-artwork-background`, `fr-artwork-major`,
`fr-artwork-minor`, `fr-artwork-motif` (+ variantes de couleur `--blue-ecume`, `--green-bourgeon`, …). Les éléments
décoratifs portent `aria-hidden="true"`.

### Icônes

Les icônes ne sont **pas** dans `dsfr.min.css` : elles vivent dans une feuille
séparée, `dist/utility/icons/icons.min.css`, à importer explicitement. Elle
définit **1044** classes `fr-icon-*` (ex. `fr-icon-add-line`) ; `dsfr.min.css`
seul n'en définit aucune.

`fr-fi-*` est l'ancien nommage (DSFR ≤ 1.7) : il ne survit plus que comme
modificateurs de taille `fr-fi--sm` / `fr-fi--md` / `fr-fi--lg`. Une classe
comme `fr-fi-checkbox-line` **n'existe pas** — utiliser `fr-icon-checkbox-line`.

Vérifié le 2026-10-22 sur `@gouvfr/dsfr` 1.15.4.

## Pièges
- **Classes inventées** : `fr-artwork-ministery`, `fr-artwork-brand`, `fr-artwork-theme-*` n'existent PAS dans le CSS officiel. Toujours contrôler le nom dans le CSS (cf. `fr-gov-set-up-design-system/scripts/verify_dsfr.py`).
- Logo Marianne = classe `fr-logo` (SVG inline via le CSS), pas un fichier `marianne.svg` dans artwork.
- `alt` descriptif obligatoire sur les images signifiantes ; `alt=""` + `aria-hidden="true"` pour le purement décoratif.
- Les icônes sociales (Bluesky, etc.) sont ajoutées au fil des versions : vérifier la classe dans le CSS de la version épinglée.

## Vérification
- L'image s'affiche (chemin `dist/artwork/...` correct, asset en 200 en HTTP).
- Chaque classe `fr-*` utilisée est présente dans le CSS officiel (script `verify_dsfr.py`).
- `alt` présent et pertinent sur les pictogrammes porteurs de sens.
