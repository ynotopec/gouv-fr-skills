# Arborescence du dépôt

### Vue.js (default)

```
src/
├── App.vue
├── components/          # Reusable across views
├── stores/              # Pinia stores
├── views/               # Page components (one folder each)
│   └── AppHome/
│       ├── AppHome.vue
│       ├── AppHome.cy.ts
│       ├── AppHome.spec.ts
│       └── components/  # View-specific
└── utils/
```

### Fastify

```
src/
├── index.ts             # Entry
├── app.ts               # Config
├── plugins/             # CORS, Swagger, Auth
├── routes/
│   └── cats/
│       ├── index.ts
│       ├── cats.schema.ts
│       └── cats.service.ts
└── utils/
test/routes/
```

### FastAPI

```
app/
├── main.py              # Entry
├── config.py            # Env vars
├── models/              # SQLAlchemy
├── schemas/             # Pydantic
├── routers/             # APIRouter
├── services/            # Business logic
└── utils/
tests/
```

### NestJS

```
src/modules/cats/
├── controllers/
├── providers/
├── entity/
└── cats.module.ts
```

