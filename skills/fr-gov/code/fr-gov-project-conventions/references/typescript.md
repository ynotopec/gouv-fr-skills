# TypeScript strict

Progress:
- [ ] Enable strict mode
- [ ] No `enum`, no `namespace`
- [ ] No `any` (extremely rare)
- [ ] No `object` type
- [ ] Runtime validation with Zod

### Use unions instead of enums

```typescript
// ✅
type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE';
```

### interface vs type

- `interface` — objects, API contracts, component props
- `type` — unions, intersections, utility types

### as const for literals

```typescript
const ROLES = ['admin', 'editor'] as const
type Role = typeof ROLES[number]
```

### Discriminated unions

```typescript
type Result<T> =
  | { ok: true; data: T }
  | { ok: false; error: string }
```

### Runtime validation

See [fr-gov-choose-tech-stack] for Zod examples.

