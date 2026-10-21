# Standards de code

## Sommaire

- Structure et fonctions
- Erreurs, asynchronisme et imports
- Constantes et retours anticipés
- Dépendances, tests et lint


Appliquer ces repères uniquement en l’absence de convention du dépôt.
Les préférences de style ne constituent pas seules un défaut bloquant.

### Structure de fichier

- Suivre la configuration du dépôt ; à défaut viser 120 colonnes.
- `.editorconfig` à la racine (2 espaces, LF, UTF-8, trim trailing whitespace)
- Respecter les conventions du langage et du dépôt pour les noms de fichiers.

### Fonctions

- Viser un seul but par fonction. 20 lignes est un repère de lisibilité,
  pas un seuil bloquant ; ne pas découper artificiellement une fonction claire.
- Noms explicites ; pas de variable d'une seule lettre (sauf identité `x => x`)

### Erreurs

Ne jamais ignorer silencieusement :

```typescript
// ❌
try { await fetchData() } catch { }

// ✅
try { await fetchData() } catch (error) {
  logger.error(error, 'Erreur')
  throw error
}
```

- Créer des erreurs typées (`NotFoundError`, `ValidationError`)
- Ne pas se contenter d'un `Error` générique

### Async / await

- Préférer `async/await` si cela clarifie le flux ; respecter le style du projet.
- Paralléliser les opérations indépendantes avec `Promise.all()`
- Utiliser `async def` pour les I/O avec un client asynchrone ; déporter les
  appels bloquants selon le framework pour ne pas bloquer la boucle événementielle.

### Imports

Pour JS/TS sans configuration existante, ordre conseillé :

1. Modules Node.js natifs (`node:fs`)
2. Packages externes (`fastify`, `vue`)
3. Modules internes (alias `@/`, `~/`)
4. Modules relatifs (`./`, `../`)

### Constantes

Extraire les valeurs magiques dans des constantes nommées :

```typescript
// ❌
if (password.length < 8) { ... }

// ✅
const MIN_PASSWORD_LENGTH = 8
if (password.length < MIN_PASSWORD_LENGTH) { ... }
```

### Early return

Privilégier les retours anticipés pour éviter l'imbrication :

```typescript
if (!user) return
if (!user.isActive) return
// traitement...
```

### Dépendances

Avant d'ajouter une dépendance, évaluer :

1. Version courante (dernière stable majeure)
2. Popularité (téléchargements hebdo, étoiles GitHub)
3. Fréquence de mise à jour (12 mois sans commit = signal d'alerte)
4. Maintenance (issues ouvertes, réactivité, `SECURITY.md`)
5. Taille (bundlephobia.com pour npm)

### Tests adaptés au risque

- Vérifier le comportement et les risques du changement avec des tests pertinents.
- Composants avec Vue Testing Library ; E2E avec Playwright
- Suivre les outils du projet ; à défaut Vitest pour JS/TS, pytest pour Python.
- Suivre l’objectif de couverture du projet ; éviter les tests sans valeur comportementale.

### Configuration du lint

Voir `lint-format` (ESLint flat config, Ruff, EditorConfig) — ne pas
dupliquer la configuration ici.

### Vérification des standards

- Exécuter les commandes déclarées par le projet.
- Exemples si configurés : `pnpm lint`, `pnpm test` ; pour Python avec uv,
  `uv run ruff check`. Ne pas inventer un script `pnpm ruff`.

### Pièges

- ESLint remplace Prettier — ne pas installer les deux avec `@antfu/eslint-config`
- Flat config (`eslint.config.js`) depuis ESLint v9 — plus de `.eslintrc`
- Ruff remplace black, flake8, isort, pyupgrade — ne pas les cumuler
- Les tests se mettent à jour avec le code, pas après
