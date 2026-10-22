---

name: fr-gov-scaffold-backend-api
description: Fastify, NestJS, FastAPI, logging, error handling
version: 0.2.1
license: MIT
author: ynotopec
platforms: [linux, macos]
metadata:
  hermes:
    tags: [gouv-fr, backend, fastify, nestjs, fastapi, api, tests]
    related_skills: [fr-gov-rest-api-conventions, fr-gov-choose-tech-stack, fr-gov-secure-coding-rules]
---

# Gouv-fr — Backend (Fastify, NestJS, FastAPI)

Node.js/TypeScript: **Fastify** or **NestJS**. Python: **FastAPI**.

## Quand utiliser

- Créer une API ou un service backend : échafaudage, structure, journalisation,
  gestion d'erreurs, documentation OpenAPI, tests.
- Reprendre un backend existant pour l'aligner sur les conventions Fabrique Numérique.

Ne pas utiliser pour l'interface : voir `fr-gov-build-vue-frontend` ou `fr-gov-build-react-design-system`.

## Scripts disponibles

- **`scripts/scaffold-nestjs.sh`** — Creates a NestJS project with CoFabNum conventions
  - Usage: `bash scripts/scaffold-nestjs.sh <project-name>`
  - Installs nestjs-pino, @nestjs/swagger, configures ESLint for NestJS
  - Sets up tsconfig with decorator support
- **`scripts/scaffold-fastify.sh`** — Creates a Fastify project with CoFabNum conventions
  - Usage: `bash scripts/scaffold-fastify.sh <project-name>`
  - Full project structure: plugins, routes, schemas, error handler, logger, tests
  - Configures @fastify/swagger, @fastify/cors, @sinclair/typebox
- **`scripts/scaffold-fastapi.sh`** — Creates a FastAPI project with CoFabNum conventions
  - Usage: `bash scripts/scaffold-fastapi.sh <project-name>`
  - Full project structure: routers, schemas, services, models, utils
  - Configures ruff, pytest, lifespan pattern

### Scaffolding

```shell
npx @nestjs/cli new my-app
```

### Project structure

```
src/
└── modules/
    └── cats/
        ├── controllers/cats.controller.ts
        ├── providers/cats.service.ts
        ├── entity/cats.entity.ts
        └── cats.module.ts
```

Modules and files **plural**: `CatsModule`, `CatsService`, `CatsController`.

### Logging (nestjs-pino)

```shell
pnpm add nestjs-pino pino-http
```

```typescript
// app.module.ts
import { LoggerModule } from 'nestjs-pino';
@Module({ imports: [LoggerModule.forRoot()] })
class AppModule {}

// main.ts
import { Logger } from 'nestjs-pino';
async function bootstrap() {
  const app = await NestFactory.create(AppModule, { bufferLogs: true })
  app.useLogger(app.get(Logger))
  await app.listen(3000)
}
```

**Gotcha**: Pass `{ bufferLogs: true }` to `NestFactory.create()`, otherwise logs are lost before pino is set up.

### Error filter

```typescript
@Catch(HttpException)
export class HttpExceptionFilter implements ExceptionFilter {
  constructor(private readonly logger: LoggerService) {}
  catch(exception: HttpException, host: ArgumentsHost) {
    const ctx = host.switchToHttp()
    const response = ctx.getResponse<Response>()
    const status = exception.getStatus()
    this.logger.error(exception.getResponse())
    response.status(status).json({
      ...(exception.getResponse() as any),
      timestamp: new Date().toISOString(),
    })
  }
}
```

### OpenAPI

See [fr-gov-choose-tech-stack] for full setup. Use `@nestjs/swagger`.

### Pièges

- Use `nestjs-pino` not the built-in NestJS logger — it outputs JSON automatically
- The `HttpExceptionFilter` must be registered in `main.ts`: `app.useGlobalFilters(new HttpExceptionFilter(logger))`
- Enable `experimentalDecorators` and `emitDecoratorMetadata` in `tsconfig.json` or ESLint errors

## Renvois

Gabarits détaillés, à ouvrir quand un projet doit être créé :

- [Fastify](references/fastify.md) — Node.js/TypeScript, plugins, routes, tests.
- [FastAPI](references/fastapi.md) — Python, Pydantic, async, tests.

## Pièges

- **NestJS**: Always register the global exception filter in `main.ts`, not just the class definition
- **Fastify**: JSON Schema validation is mandatory, not optional. Use `@sinclair/typebox` for type inference
- **FastAPI**: Use `async` for I/O endpoints but `def` (sync) for CPU-bound work — mixing them up blocks the event loop
- **FastAPI**: `lifespan` replaces `@app.on_event` — using the old pattern generates deprecation warnings
- **All**: Always return proper HTTP status codes (201 for POST create, not 200)
- **All**: Error messages should be in French or use dictionary keys understood by the client
- **All**: Log response time on every request
- **All**: Use structured JSON logs (stdout) for container collection
