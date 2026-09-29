---
name: gouv-fr-frontend-vue3
description: Use when building Vue 3 or Nuxt 3 frontend projects for Fabrique Numérique
  — DSFR compliance, VueDsfr scaffolding, composable patterns like toaster, and testing
  setup
allowed-tools: Read Write Bash
---

---|------|---------|
| `modelValue` | `string \| number` | v-model |
| `label` | `string` | Field label |
| `labelVisible` | `boolean` | Show/hide label |
| `hint` | `string` | Help text |
| `isInvalid` | `boolean` | Error state (red border + error styling) |
| `isValid` | `boolean` | Success state |
| `isTextarea` | `boolean` | Render as `<textarea>` |
| `isWithWrapper` | `boolean` | Wrap in `.fr-input-group` |

```vue
<DsfrInput
  v-model="email"
  label="Email"
  :is-invalid="!!errors.email"
  :hint="errors.email ?? 'Format attendu : nom@domaine.fr'"
/>
```

There is **no `native-validators` prop** — validation/error state is driven by `isInvalid` + `hint`/`errorMessage`, handled in your own validation logic (e.g. VeeValidate, Zod).

## Layout, typo & tokens DSFR

Utilise les utilitaires et tokens DSFR **au lieu de réinventer le layout en CSS maison** :

- **Conteneur / grille** : `fr-container`, `fr-grid-row` (+ `fr-grid-row--center`, `fr-grid-row--gutters`) et colonnes `fr-col-12 fr-col-md-6`… (responsive par défaut).
- **Espacement** : utilitaires `fr-py-*w`, `fr-px-*w`, `fr-mt-*w`, `fr-mb-*w` (ex. `fr-py-6w`, `fr-mb-2w`).
- **Typographie** : `fr-h1`…`fr-h6`, `fr-display--md`, `fr-text--lg`, `fr-text--sm`, `fr-text--bold` — pas de `font-size`/`font-weight` codés en dur.
- **Couleurs / tokens** : toujours via les variables DSFR (`--bf-500`, `--red-marianne-425-625`, `--border-default-grey`, `--background-default-grey`, …) — jamais de valeurs hex en dur (`#000091`, `#ce0500`).

```vue
<section class="fr-container fr-py-6w">
  <div class="fr-grid-row fr-grid-row--center">
    <div class="fr-col-12 fr-col-md-6">
      <h1 class="fr-h3">Titre</h1>
      <p class="fr-text--lg">Sous-texte</p>
    </div>
  </div>
</section>
```

## Gotchas

- **DSFR is mandatory** — Ministry of Interior projects must use VueDsfr, not a generic component library
- **Package name is `@gouvminint/vue-dsfr`, not `@gouvfr/dsfr-vue`** — and components are prefixed `Dsfr*` (`DsfrInput`, `DsfrButton`), not `Fr*`. A plan referencing `@gouvfr/dsfr-vue`/`FrInput` is hallucinated — verify against `package.json` and `node_modules/@gouvminint/vue-dsfr` before coding (see the verification checklist in `AGENTS.md`)
- **Vue component files need 2+ words** — `LoginForm.vue` not `Form.vue` (exception: `App.vue`)
- **Jest DOM with Vitest** — do NOT install Jest, Jest DOM is compatible with Vitest directly
- **Toaster timeouts must clean up** — always `clearTimeout` on remove to prevent memory leaks
- **`getRandomId` from VueDsfr** — use the library's utility, don't generate your own IDs
- **Transition group needs CSS** — `pointer-events: none` on container but `pointer-events: all` on alerts so they're clickable
- **Playwright on Onyxia requires `--no-sandbox`** — the container runs as root without a sandbox; add `args: ['--no-sandbox']` to the browser launch options in `playwright.config.ts` or tests will fail to launch Chromium
