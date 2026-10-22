# Docker

### Container rules

- Lightweight base : `*-alpine`, `*-slim`, `distroless`
- Non-root user (UID ≥ 1000)
- Multi-stage builds
- Non-privileged port (≥ 1024)
- **Never** use `latest` tag in production

### Docker Compose

Default for local development.

```yaml
version: '3.8'
services:
  app:
    build: .
    ports: ["3000:3000"]
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
```

### Kubernetes local (optional)

| Tool | When to use |
|---|---|
| [Kind](https://kind.sigs.k8s.io/) | Test K8s manifests locally |
| [k3d](https://k3d.io/) | Lightweight K8s in Docker |
| [Minikube](https://minikube.sigs.k8s.io/) | Local cluster with GUI |

Tester l'image en lecture seule avant de livrer : `docker run --read-only <image>`.

