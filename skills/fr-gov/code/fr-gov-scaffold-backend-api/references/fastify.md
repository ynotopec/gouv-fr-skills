# Gabarit Fastify

### Scaffolding

```shell
mkdir my-app && cd my-app
pnpm init
pnpm add fastify
pnpm add -D typescript @types/node tsx
```

### Project structure

```
src/
├── index.ts             # Entry point
├── app.ts               # Fastify instance
├── plugins/             # CORS, Swagger, Auth
├── routes/
│   ├── index.ts
│   └── cats/
│       ├── index.ts
│       ├── cats.schema.ts
│       └── cats.service.ts
└── utils/logger.ts
test/routes/cats.test.ts
```

### Plugin pattern

```typescript
import { FastifyPluginAsync } from 'fastify'
import fp from 'fastify-plugin'

const myPlugin: FastifyPluginAsync = async (fastify) => {
  fastify.decorate('myUtil', () => { /* ... */ })
}
export default fp(myPlugin, { name: 'my-plugin' })
```

### Validation with TypeBox

```typescript
import { Type, Static } from '@sinclair/typebox'

const CatSchema = Type.Object({
  id: Type.Number(),
  name: Type.String({ minLength: 1 }),
  age: Type.Number({ minimum: 0 }),
})
type Cat = Static<typeof CatSchema>

export const getCatOpts = {
  schema: {
    params: Type.Object({ id: Type.Number() }),
    response: { 200: CatSchema },
  },
}
```

### Routes

```typescript
const catsRoutes: FastifyPluginAsync = async (fastify) => {
  fastify.get('/', async () => catsService.findAll())
  fastify.get<{ Params: { id: number } }>('/:id', { schema: getCatOpts.schema }, async (req) =>
    catsService.findById(req.params.id))
  fastify.post<{ Body: Cat }>('/', async (req, reply) => {
    const cat = await catsService.create(req.body)
    return reply.code(201).send(cat)
  })
}
```

### Logging

Uses [pino](https://getpino.io/) by default:

```typescript
const fastify = Fastify({
  logger: {
    level: process.env.LOG_LEVEL ?? 'info',
    ...(process.env.NODE_ENV === 'development' && {
      transport: { target: 'pino-pretty' },
    }),
  },
})
```

### Error handler

```typescript
fastify.setErrorHandler((error, request, reply) => {
  request.log.error(error)
  const statusCode = error.statusCode ?? 500
  reply.status(statusCode).send({ statusCode, error: error.name, message: error.message, timestamp: new Date().toISOString() })
})
```

### OpenAPI

See [fr-gov-choose-tech-stack] for full setup. Use `@fastify/swagger` + `@fastify/swagger-ui`.

### Testing

```typescript
import { buildApp } from '../src/app'

it('GET /cats returns list', async () => {
  const app = await buildApp()
  const res = await app.inject({ method: 'GET', url: '/cats' })
  expect(res.statusCode).toBe(200)
})
```

**Gotcha**: Use `app.inject()` — no need to start a real server for tests.

