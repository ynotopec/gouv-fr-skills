#!/usr/bin/env bash
# Builds et HTTP réels ; requiert uv/pnpm/npx et un accès aux registres de paquets.
set -euo pipefail
framework="${1:?Usage: test-scaffold-integration.sh fastapi|fastify|nestjs}"
root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
case "$framework" in fastapi|fastify|nestjs) ;; *) exit 2 ;; esac
task_dir=$(mktemp -d)
server_pid=''
cleanup() {
  if [[ -n "$server_pid" ]]; then
    kill "$server_pid" 2>/dev/null || true
    wait "$server_pid" 2>/dev/null || true
  fi
  rm -rf "$task_dir"
}
trap cleanup EXIT
cd "$task_dir"
bash "$root/skills/fr-gov/code/fr-gov-scaffold-backend-api/scripts/scaffold-$framework.sh" app
cd app
case "$framework" in
  fastapi)
    uv run pytest
    uv run ruff check --select F .
    uv sync --frozen --no-dev
    .venv/bin/fastapi run app/main.py --host 127.0.0.1 --port 3000 > "$task_dir/server.log" 2>&1 &
    endpoint='http://127.0.0.1:3000/cats/'
    ;;
  fastify)
    pnpm build
    pnpm test
    pnpm prune --prod
    NODE_ENV=production node dist/index.js > "$task_dir/server.log" 2>&1 &
    endpoint='http://127.0.0.1:3000/api/v1/cats/'
    ;;
  nestjs)
    pnpm build
    pnpm test --runInBand
    pnpm prune --prod
    NODE_ENV=production node dist/main.js > "$task_dir/server.log" 2>&1 &
    endpoint='http://127.0.0.1:3000/'
    ;;
esac
server_pid=$!
for attempt in {1..30}; do
  if curl --fail --silent "$endpoint" > "$task_dir/response"; then
    echo "OK: $framework build, tests et HTTP avec dépendances de production seules"
    exit 0
  fi
  if ! kill -0 "$server_pid" 2>/dev/null; then break; fi
  sleep 1
done
cat "$task_dir/server.log" >&2
exit 1
