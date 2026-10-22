# Vérification sans navigateur

Quand `browser_exec` échoue (Chromium manquant, libs système absentes type `libglib-2.0`, pas de sudo), vérifier la conformité DSFR par analyse textuelle — sans jamais inventer de liste de classes « attendues ».

## Principe

La source de vérité est le CSS OFFICIEL (`dsfr.min.css` + `utility.min.css`), pas la mémoire du modèle. Toute classe `fr-*` utilisée dans le HTML mais absente des sélecteurs du CSS officiel est suspecte (`fr-skip-links`, `fr-btn--primary`, `fr-artwork-ministery` sont des exemples réels d'erreurs de ce type).

## Méthode

1. `python3 ../scripts/verify_dsfr.py index.html` (stdlib seule ; télécharge et met en cache le CSS officiel, ou `--css` avec des fichiers locaux).
   - Critère de fin : code retour 0 = zéro classe `fr-*` inconnue, zéro asset manquant.
2. Tester chaque ressource relative servie en HTTP : `python3 -m http.server 8080` puis HEAD request (`curl -sI http://localhost:8080/chemin`) sur CSS, JS, polices, SVG → tous en 200.
3. Ponctuellement, comparer un sélecteur précis au CSS officiel (rechercher `fr-<nom>` dans le fichier CSS téléchargé).

## Limites

- Ne vérifie pas le rendu visuel (couleurs exactes, positions, tailles).
- Un CSS logique faux mais syntaxiquement conforme (ex. un style custom qui écrase `fr-btn--secondary` avec un fond bleu primaire) passe inaperçu sans comparaison visuelle.
- Les classes injectées par le JS DSFR au runtime (états ouverts/fermés, `fr-collapse`, etc.) peuvent être signalées si le CSS lié est incomplet : vérifier d'abord que `dsfr.min.css` ET `utility.min.css` sont tous deux fournis à `--css`.

## Alternative si un navigateur existe

Playwright headless (`pip3 install playwright && python3 -m playwright install chromium`) pour screenshots et styles calculés. Si l'installation échoue (souvent sans sudo), rester sur la méthode textuelle ci-dessus.

## Test front exécuté sans navigateur (jsdom)

Au-delà des classes, on peut exécuter réellement le JS de l'interface et vérifier le rendu :

1. **Node sans sudo** : tarball officiel — `uname -m` = `aarch64` → URL `linux-arm64`, extrait dans
   le scratch (`https://nodejs.org/dist/<v>/node-<v>-linux-arm64.tar.xz`). Sert aussi pour
   `node --check app.js` (validation de syntaxe en 1 s).
2. **`npm install --save-dev jsdom` DANS LE PROJET** — Node résout les imports depuis le dossier
   du script (`tests/`), pas depuis le cwd : installer ailleurs donne `ERR_MODULE_NOT_FOUND`.
3. Serveur local de l'app (`uvicorn`, base fraîche), puis `tests/test-front.mjs` :
   `new JSDOM(html, { url, runScripts: "outside-only" })`, injecter
   `window.fetch = (u, o) => globalThis.fetch(u.startsWith("http") ? u : BASE + u, o)`, évaluer
   `app.js` via `window.eval`, puis `document.dispatchEvent(new Event("DOMContentLoaded"))`.
4. **Assertions DOM** : lignes de table, valeurs des tuiles, options des `<select>`, classes des
   badges, ouverture de formulaire au clic, création réelle (POST → +1 ligne), filtre actif, et
   `window.addEventListener("error")` pour capturer les erreurs JS silencieuses.
5. **Piège de test** : avec un filtre semaine actif par défaut, un élément créé hors semaine
   n'apparaît pas dans la table — lever le filtre avant de compter, sinon le test échoue à tort.

Critère : 0 échec + 0 erreur JS capturée (exemple réel : 17 vérifications sur l'app `permanences`).
