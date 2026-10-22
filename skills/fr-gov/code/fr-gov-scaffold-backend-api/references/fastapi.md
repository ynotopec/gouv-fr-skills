# Gabarit FastAPI

### Scaffolding

```shell
uv init my-api && cd my-api
uv add "fastapi[standard]"
uv run fastapi dev
```

### Project structure

```
app/
├── main.py              # Entry
├── config.py            # Env vars (BaseSettings)
├── models/              # SQLAlchemy
├── schemas/             # Pydantic
├── routers/             # APIRouter
├── services/            # Business logic
└── utils/
tests/
```

### Pydantic schemas

```python
from pydantic import BaseModel, Field

class CatBase(BaseModel):
    name: str = Field(min_length=1, description="Nom du chat")
    age: int = Field(ge=0)

class CatCreate(CatBase): pass

class CatResponse(CatBase):
    id: int
    model_config = {"from_attributes": True}
```

### Routes

```python
from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/cats", tags=["cats"])

@router.get("/", response_model=list[CatResponse])
async def get_cats():
    return await CatsService.find_all()

@router.post("/", response_model=CatResponse, status_code=status.HTTP_201_CREATED)
async def create_cat(cat: CatCreate):
    return await CatsService.create(cat)
```

### Async vs sync

```python
# ✅ I/O operations — async
@router.get("/cats")
async def get_cats():
    return await db.fetch_all(query)

# ✅ CPU-bound — sync
@router.get("/compute")
def compute():
    return heavy_computation()
```

### Logging with lifespan

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("App started")
    yield
    logger.info("App stopped")

app = FastAPI(lifespan=lifespan)
```

**Gotcha**: Use `lifespan` context manager, not `@app.on_event("startup")` (deprecated since FastAPI 0.93+).

### Error handling

```python
class AppException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

@app.exception_handler(AppException)
async def handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
```

### OpenAPI

Auto-generated at `/docs` (Swagger) and `/redoc`.

### Testing

```shell
uv add --dev pytest httpx
```

```python
from fastapi.testclient import TestClient

def test_get_cats():
    assert client.get("/cats").status_code == 200
```

### Dockerfile template

See `fr-gov-containerize-app-for-k8s` for the optimized multi-stage Dockerfile template with `uv`.

