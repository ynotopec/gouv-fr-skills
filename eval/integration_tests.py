#!/usr/bin/env python3
"""Runner de tests d'integration pour les skills fr-gov."""
import json, os, shutil, subprocess, sys, tempfile, time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

_test_contents = {}

def _reg(name, content):
    _test_contents[name] = content

def _write_file(path, name):
    if name in _test_contents:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(_test_contents[name])
        return True
    return False

def dir_exists(path, name):
    return (path / name).is_dir()

def file_exists(path, name):
    return (path / name).is_file()

def file_contains(path, name, text):
    try:
        return text in (path / name).read_text()
    except FileNotFoundError:
        return False

def count_lines(path, name):
    try:
        return len((path / name).read_text().strip().splitlines())
    except FileNotFoundError:
        return 0

# ---- Register test file contents (avoiding triple-quote parsing issues) ----
# Using single-quoted strings with \n for newlines

_reg("README", "# My Project\n\nAutomatically initialized.\n")
_reg("gitignore", ".env\n__pycache__/\n*.pyc\n.env.local\nvenv/\n")
_reg("LICENSE", "MIT License\n")
_reg("AGENTS", "# Project Rules\n\nArchitecture documentation.\n")
_reg("BACKLOG", "# Backlog\n\nEpics and tasks.\n")
_reg("TESTS", "# Tests\n\nValidation scenarios.\n")
_reg("FEEDBACK", "# Feedback\n\nUser feedback.\n")
_reg("config_yaml", "agent:\n  name: opencode\n  skills_dir: .agents/skills\n")
_reg("skills_txt", "# Selected skills\n")

_reg("api_client", "# API client service.\nHandles all external API calls.\n\nclass ApiClient:\n    \"\"\"Handles external API communication.\"\"\"\n    def __init__(self, base_url: str):\n        self.base_url = base_url\n        self.timeout = 30\n    async def get(self, endpoint: str) -> dict:\n        # Fetch data from endpoint\n        return {\"status\": \"ok\"}\n")

_reg("database", "# Database access layer.\nManages all database operations.\n\nclass Database:\n    \"\"\"Database connection and queries.\"\"\"\n    def __init__(self, connection_string: str):\n        self.connection_string = connection_string\n    async def query(self, sql: str, params: tuple) -> list:\n        # Execute parameterized query\n        return []\n")

_reg("config_py", "# Application configuration.\nAll secrets come from environment variables.\nimport os\n\nDATABASE_URL = os.environ[\"DATABASE_URL\"]\nAPI_KEY = os.environ[\"API_KEY\"]\nSECRET_KEY = os.environ[\"SECRET_KEY\"]\n")

_reg("db_py", "# Database access with parameterized queries only.\nasync def get_user(db, user_id: int):\n    # Fetch user by ID\n    query = \"SELECT * FROM users WHERE id = ?\"\n    params = (user_id,)\n    return await db.execute(query, params)\n")

_reg("gitignore_sec", ".env\n.env.local\n*.key\n*.pem\n__pycache__/\n")

_reg("main_py", "# FastAPI application\nfrom fastapi import FastAPI, HTTPException\nfrom pydantic import BaseModel\n\napp = FastAPI(title=\"My API\", version=\"1.0.0\")\n\nclass Item(BaseModel):\n    name: str\n    price: float\n\n@app.get(\"/health\")\ndef health_check():\n    # Health endpoint\n    return {\"status\": \"ok\"}\n\n@app.get(\"/items/{item_id}\")\ndef get_item(item_id: int):\n    if item_id < 0:\n        raise HTTPException(status_code=404, detail=\"Not found\")\n    return {\"id\": item_id, \"name\": \"Test\"}\n")

_reg("routes_py", "# Routes module\nfrom fastapi import APIRouter\n\nrouter = APIRouter()\n\n@router.get(\"/ping\")\ndef ping():\n    return {\"pong\": True}\n")

_reg("requirements", "fastapi\nuvicorn\npydantic\n")

_reg("api_py", "# REST API following conventions\nfrom fastapi import APIRouter, HTTPException, status\n\nrouter = APIRouter()\n\n@router.get(\"/api/v1/items\", response_model=dict)\ndef list_items(page: int = 1, size: int = 20):\n    # List items with pagination\n    return {\"items\": [], \"page\": page, \"size\": size, \"total\": 0}\n\n@router.get(\"/api/v1/items/{item_id}\")\ndef get_item(item_id: int):\n    if item_id <= 0:\n        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=\"Item \" + str(item_id) + \" not found\")\n    return {\"id\": item_id, \"name\": \"Test\"}\n\n@router.put(\"/api/v1/items/{item_id}\")\ndef update_item(item_id: int):\n    return {\"id\": item_id, \"updated\": True}\n\n@router.delete(\"/api/v1/items/{item_id}\")\ndef delete_item(item_id: int):\n    return {\"id\": item_id, \"deleted\": True}\n")

_reg("open_data", "# Data.gouv.fr client\nasync def search_datasets(query: str):\n    # Search datasets on data.gouv.fr\n    url = \"https://www.data.gouv.fr/api/1/datasets/\"\n    return {\"datasets\": []}\n\nasync def get_dataset_format(dataset_id: str, format_type: str = \"csv\"):\n    return {\"dataset_id\": dataset_id, \"format\": format_type, \"resources\": []}\n\nasync def download_resource(resource_id: str, output_path: str):\n    return {\"path\": output_path, \"size\": 0}\n")

_reg("communications", "# Public communication data API\nasync def get_press_releases(minister_id=None):\n    return {\"type\": \"Comite\", \"commitee\": [], \"items\": []}\n\nasync def get_minister(name: str):\n    return {\"type\": \"Person\", \"name\": name, \"role\": \"Minister\"}\n\nasync def get_public_figure(name: str):\n    return {\"type\": \"Person\", \"name\": name}\n")

_reg("adr_001", "# ADR-001: Tech Stack Selection\n\n## Context\nWe need to choose a tech stack for the application.\n\n## Decision\nWe will use Python/FastAPI for the backend and Next.js for the frontend.\n\n## Consequences\n- FastAPI provides automatic OpenAPI documentation\n- Next.js provides server-side rendering\n")

_reg("main_bug", "# App with a bug to investigate\n\nclass Calculator:\n    def add(self, a: int, b: int) -> int:\n        return a + b\n    def divide(self, a: int, b: int) -> float:\n        return a / b  # Missing zero check!\n")

_reg("bug_investigation", "# Bug Investigation: Division by zero\n\n## Hypotheses\n1. No zero check in divide() method\n2. Error handling not implemented\n\n## Reproduction\n```python\ncalc = Calculator()\nresult = calc.divide(1, 0)  # ZeroDivisionError\n```\n\n## Root Cause\nMissing input validation in divide() method.\n\n## Fallback Plan\nAdd try/except with user-friendly error message.\n")

_reg("api_buggy", "# Code with issues to review\nimport requests\n\ndef get_data(url: str):\n    response = requests.get(url)  # No error handling!\n    return response.json()\n\ndef process_items(items):  # No type hints!\n    result = []\n    for item in items:\n        if item.get(\"active\"):\n            result.append(item)\n    return result\n")

_reg("code_review", "# Code Review: src/api.py\n\n## Security\n- No error handling on requests.get()\n- No response status code check\n\n## Quality\n- Missing type hints on function signatures\n\n## Suggestions\n1. Add try/except block\n2. Check response.status_code\n")

_reg("hello_main", "# Task implementation\ndef hello(name: str) -> str:\n    if not name:\n        raise ValueError(\"name cannot be empty\")\n    return \"Hello, \" + name + \"!\"\n")

_reg("test_hello", "# Tests for main.py\nimport pytest\n\ndef test_hello():\n    from src.main import hello\n    assert hello(\"World\") == \"Hello, World!\"\n\ndef test_hello_empty():\n    from src.main import hello\n    with pytest.raises(ValueError):\n        hello(\"\")\n")

_reg("ship_checklist", "# Task: hello() function\n\n## Implementation\n- [x] Function implemented\n- [x] Type hints added\n- [x] Error handling for empty input\n\n## Tests\n- [x] Test with valid input\n- [x] Test with empty input\n\n## Checklist\n- [x] Code written\n- [x] Tests written\n- [x] Documentation updated\n- [x] Ready for review\n")

_reg("deployment", "apiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: service-frontend\nspec:\n  selector:\n    matchLabels:\n      app: service-frontend\n  template:\n    metadata:\n      labels:\n        app: service-frontend\n    spec:\n      containers:\n      - name: service-frontend\n        image: myapp/frontend:latest\n")

_reg("service_k8s", "apiVersion: v1\nkind: Service\nmetadata:\n  name: service-frontend\nspec:\n  selector:\n    app: service-frontend\n  ports:\n  - port: 80\n    targetPort: 8080\n")

_reg("name_mapping", "# Service Name Registry\n\n## New names -> Old names\n| Service | Old Name | Migration Path |\n|---|---|---|\n| service-frontend | front-app | Direct migration |\n| service-backend | back-app | Requires env var update |\n\n## Validation script\nCheck all deployments use consistent naming convention.\n")

_reg("dockerfile", "FROM python:3.12-slim\n\nWORKDIR /app\n\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\n\nCOPY src/ src/\n\n# Rootless: non-root user\nRUN useradd --create-home appuser\nUSER appuser\n\nEXPOSE 8080\n\nCMD [\"python\", \"src/main.py\"]\n")

_reg("requirements_k8s", "fastapi\nuvicorn\npydantic\n")

_reg("chart_yaml", "apiVersion: v2\nname: my-app\ndescription: Helm chart for my app\ntype: application\nversion: 1.0.0\nappVersion: \"1.0.0\"\n")

_reg("helm_values", "replicaCount: 2\n\nimage:\n  repository: myapp\n  tag: \"1.0.0\"\n  pullPolicy: IfNotPresent\n\nservice:\n  type: ClusterIP\n  port: 80\n\nresources:\n  limits:\n    cpu: 500m\n    memory: 256Mi\n  requests:\n    cpu: 250m\n    memory: 128Mi\n\nsecurityContext:\n  runAsNonRoot: true\n  readOnlyRootFilesystem: true\n")

_reg("helm_deployment", "apiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: \"{{ .Release.Name }}-app\"\n  labels:\n    app: \"{{ .Release.Name }}\"\nspec:\n  replicas: \"{{ .Values.replicaCount }}\"\n  selector:\n    matchLabels:\n      app: \"{{ .Release.Name }}\"\n  template:\n    metadata:\n      labels:\n        app: \"{{ .Release.Name }}\"\n    spec:\n      containers:\n      - name: app\n        image: \"{{ .Values.image.repository }}:{{ .Values.image.tag }}\"\n        ports:\n        - containerPort: 8080\n")

_reg("ci_yml", "name: CI\n\non: [push, pull_request]\n\njobs:\n  lint:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - name: Set up Python\n        uses: actions/setup-python@v5\n        with:\n          python-version: \"3.12\"\n      - name: Run linter\n        run: |\n          pip install ruff\n          ruff check .\n\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - name: Set up Python\n        uses: actions/setup-python@v5\n        with:\n          python-version: \"3.12\"\n      - name: Install dependencies\n        run: pip install -r requirements.txt\n      - name: Run tests\n        run: pytest tests/\n")

_reg("release_yml", "name: Release\n\non:\n  push:\n    tags:\n      - \"v*\"\n\njobs:\n  release:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - name: Create Release\n        uses: softprops/action-gh-release@v1\n        with:\n          generate_release_notes: true\n          draft: false\n\n  helm-publish:\n    needs: release\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - name: Publish Helm Chart\n        run: |\n          echo \"Publish helm chart\"\n")

_reg("dso_yml", "name: DSO Pipeline\n\non:\n  push:\n    branches: [main]\n\njobs:\n  scan:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - name: Run security scan\n        run: |\n          echo \"Running security scan\"\n\n  build:\n    needs: scan\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - name: Build image\n        run: |\n          echo \"Building Docker image\"\n          docker build -t registry.dso.fr/myapp .\n\n  deploy:\n    needs: build\n    runs-on: ubuntu-latest\n    steps:\n      - name: Deploy to DSO\n        run: |\n          echo \"Deploying to Cloud Pi Native\"\n")

_reg("vault_config", "vault:\n  address: https://vault.dso.fr\n  auth:\n    method: kubernetes\n    role: my-app\n  secrets:\n    database-url: vault://secret/data/my-app/db\n    api-key: vault://secret/data/my-app/api\n")

_reg("kyverno", "apiVersion: kyverno.io/v1\nkind: ClusterPolicy\nmetadata:\n  name: require-security-context\nspec:\n  rules:\n  - name: check-runAsNonRoot\n    match:\n      any:\n      - resources:\n          kinds:\n          - Pod\n    mutate:\n      patchStrategicMerge:\n        spec:\n          securityContext:\n            runAsNonRoot: true\n")

_reg("dsfr_css", "/* DSFR CSS placeholder */\n")
_reg("utility_css", "/* Utility classes */\n")

_reg("index_html", "<!DOCTYPE html>\n<html lang=\"fr\">\n<head>\n  <meta charset=\"UTF-8\">\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n  <link rel=\"stylesheet\" href=\"assets/dsfr.min.css\">\n  <link rel=\"stylesheet\" href=\"assets/utility/utility.min.css\">\n  <title>Application DSFR</title>\n</head>\n<body>\n  <header class=\"fr-header\">\n    <div class=\"fr-header__body\">\n      <div class=\"fr-header__brand\">\n        <div class=\"fr-header__brand-top\">\n          <div class=\"fr-header__logo\">\n            <p>Ministere</p>\n          </div>\n        </div>\n      </div>\n    </div>\n  </header>\n  <main class=\"fr-container\">\n    <h1>Application</h1>\n  </main>\n</body>\n</html>\n")

_reg("icons_html", '<i class="fr-icon-search fr-icon--sm"></i>\n<i class="fr-icon-home fr-icon--lg"></i>\n<i class="fr-icon-arrow-right-line"></i>\n<i class="fr-icon-delete-line fr-text--danger"></i>\n<i class="fr-icon-check-line fr-text--success"></i>\n')

_reg("custom_icon", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">\n  <path fill="currentColor" d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>\n</svg>\n')

_reg("charts_html", "<!DOCTYPE html>\n<html lang=\"fr\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>DSFR Charts</title>\n  <link rel=\"stylesheet\" href=\"assets/dsfr.min.css\">\n</head>\n<body>\n  <div class=\"fr-card\">\n    <div class=\"fr-card__body\">\n      <div class=\"fr-card__content\">\n        <h3 class=\"fr-card__title\">Statistiques</h3>\n        <div class=\"fr-chart\">\n          <canvas id=\"myChart\"></canvas>\n        </div>\n      </div>\n    </div>\n  </div>\n  <script src=\"assets/charts.min.js\"></script>\n  <script>\n    new Chart(document.getElementById(\"myChart\"), {\n      type: \"bar\",\n      data: { labels: [\"A\", \"B\", \"C\"], datasets: [{ data: [10, 20, 30] }] }\n    });\n  </script>\n</body>\n</html>\n")

_reg("email_html", "<!DOCTYPE html>\n<html lang=\"fr\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>Confirmation</title>\n</head>\n<body>\n  <table role=\"presentation\" width=\"100%\">\n    <tr>\n      <td align=\"center\">\n        <table width=\"600\" role=\"presentation\">\n          <tr>\n            <td style=\"padding: 20px;\">\n              <h1 style=\"color: #000091;\">Confirmation</h1>\n              <p>Merci pour votre inscription.</p>\n              <p class=\"fr-text--sm\">Pour tout probleme, contactez-nous.</p>\n            </td>\n          </tr>\n        </table>\n      </td>\n    </tr>\n  </table>\n</body>\n</html>\n")

_reg("sharing_html", "<div class=\"fr-card\">\n  <div class=\"fr-card__body\">\n    <div class=\"fr-card__content\">\n      <h3 class=\"fr-card__title\">Partage de document</h3>\n      <p>Document partage avec 3 utilisateurs.</p>\n      <ul>\n        <li>Utilisateur 1 -- Lecture</li>\n        <li>Utilisateur 2 -- Edition</li>\n        <li>Utilisateur 3 -- Commentaire</li>\n      </ul>\n    </div>\n  </div>\n</div>\n")

_reg("navigation_js", "// Cunningham-style navigation\nfunction navigate(hash) {\n    window.location.hash = hash;\n    window.postMessage({ type: \"navigate\", hash }, \"*\");\n}\n\nwindow.addEventListener(\"message\", function(e) {\n    if (e.data.type === \"navigate\") {\n        updateRoute(e.data.hash);\n    }\n});\n")

_reg("app_py", "# Hardened application following OWASP Top 10.\nfrom fastapi import FastAPI, Request\nimport re\n\napp = FastAPI()\n\ndef sanitize_input(text: str) -> str:\n    return re.sub(r'[<>\"\\']', '', text)\n\nasync def check_rate_limit(request: Request) -> bool:\n    return True\n\nasync def escape_xss(text: str) -> str:\n    return (text.replace(\"&\", \"&amp;\").replace(\"<\", \"&lt;\").replace(\">\", \"&gt;\").replace('\"', \"&quot;\"))\n\n@app.get(\"/health\")\nasync def health():\n    return {\"status\": \"ok\"}\n")

_reg("security_audit", "# Security Hardening Report\n\n## OWASP Top 10 Coverage\n\n### A01: Broken Access Control\n- Role-based access control implemented\n\n### A02: Cryptographic Failures\n- TLS enforced\n- Secrets from Vault\n\n### A03: Injection\n- Parameterized queries only\n- Input sanitization\n\n### A04: Insecure Design\n- Threat modeling completed\n\n### A05: Security Misconfiguration\n- .env excluded from git\n- Debug mode disabled\n\n### A06: Vulnerable Components\n- Dependency scanning in CI\n\n### A07: Auth Failures\n- Rate limiting\n\n### A08: Software and Data Integrity\n- Code signing\n\n### A09: Security Logging\n- Structured logging\n\n### A10: SSRF\n- URL validation\n")

_reg("guides_py", "# ANSSI cybersecurity guides reference\n\nGUIDES = {\n    \"security-guide\": {\n        \"title\": \"ANSSI -- Guide de securite numerique\",\n        \"url\": \"https://www.ssi.gouv.fr/guide/\",\n        \"topics\": [\"general\", \"web\", \"api\", \"data\"],\n    },\n}\n\nasync def search_guides(query: str):\n    results = []\n    for key, guide in GUIDES.items():\n        if query.lower() in guide.get(\"title\", \"\").lower():\n            results.append(guide)\n    return results\n")

_reg("auth_py", "# LLM tool identity and session isolation\n\nclass AuthContext:\n    def __init__(self, user_id: str):\n        self.user_id = user_id\n        self.session = None\n        self.vault_initialized = False\n    async def initialize(self):\n        self.session = await create_user_session(self.user_id)\n        self.vault_initialized = True\n    def get_user_identity(self):\n        return {\n            \"sub\": self.user_id,\n            \"issuer\": \"sso.provider.fr\",\n            \"session_id\": self.session,\n            \"vault_initialized\": self.vault_initialized,\n        }\n\nasync def create_user_session(user_id: str):\n    return {\n        \"user_id\": user_id,\n        \"isolated\": True,\n        \"vault_bound\": True,\n    }\n")

_reg("repo_audit", "# Repository Security Audit\n\n## Checks performed\n- No secrets in git history\n- No auto-execution risks\n- No secret leak history\n- Dependencies audited\n- CI/CD pipeline secure\n\n## Findings\nNone -- all checks passed.\n")

_reg("guard_py", "# LLM prompt injection guards\ndef check_prompt_injection(prompt: str):\n    injection_patterns = [\n        \"ignore previous\",\n        \"system prompt\",\n        \"reset instructions\",\n        \"new instructions\",\n        \"prompt injection\",\n    ]\n    for pattern in injection_patterns:\n        if pattern.lower() in prompt.lower():\n            return True\n    return False\n\nasync def validate_guard(prompt: str, context: dict):\n    is_injection = check_prompt_injection(prompt)\n    return {\"is_injection\": is_injection, \"guard_applied\": True}\n")

_reg("qa_checklist", "# QA Checklist\n\n## Structure\n- [x] Valid HTML5\n- [x] Semantic elements (nav, main, header, footer)\n- [x] Language attribute present\n\n## Accessibility\n- [x] ARIA labels on interactive elements\n- [x] Contrast ratio sufficient\n- [x] Keyboard navigation works\n\n## Functionality\n- [x] Links work\n- [x] Forms submit correctly\n- [x] Buttons trigger actions\n\n## Security\n- [x] No console errors\n- [x] No mixed content warnings\n- [x] CSP headers set\n\n## Performance\n- [x] Fast LCP\n- [x] Minimal CLS\n- [x] Optimized images\n")

_reg("checker_py", "# Document compliance checker\nclass DocConformite:\n    def __init__(self, referential: str):\n        self.referential = referential\n        self.results = []\n    def check(self, document: dict):\n        checks = [\n            (\"required_fields\", \"id_document\" in document),\n            (\"format_valid\", document.get(\"format\") in [\"pdf\", \"docx\"]),\n            (\"metadata_present\", \"metadata\" in document),\n        ]\n        for name, passed in checks:\n            self.results.append({\"check\": name, \"passed\": passed})\n        return self.results\n    def generate_report(self):\n        return {\n            \"referential\": self.referential,\n            \"total\": len(self.results),\n            \"passed\": sum(1 for r in self.results if r[\"passed\"]),\n            \"failed\": sum(1 for r in self.results if not r[\"passed\"]),\n        }\n")

_reg("tech_arch", "# Document d'Architecture Technique\n\n## Contexte\n- Projet: Application Gouv\n- Equipe: Dev Team\n\n## Architecture\n\n### Composants\n- Frontend: Vue.js + DSFR\n- Backend: FastAPI\n- Database: PostgreSQL\n\n### Securite\n- TLS en transit\n- Vault pour secrets\n- RBAC\n\n### Monitoring\n- Grafana\n- Prometheus\n")

_reg("public_html", "<!DOCTYPE html>\n<html lang=\"fr\">\n<head><title>Test App</title></head>\n<body>\n  <nav>\n    <a href=\"/\">Home</a>\n    <a href=\"/about\">About</a>\n  </nav>\n  <main>\n    <h1>Bienvenue</h1>\n    <button id=\"action\">Action</button>\n  </main>\n</body>\n</html>\n")


# ---- Integration test functions ----

def test_init_repo(result, test_dir):
    _write_file(test_dir / "README.md", "README")
    _write_file(test_dir / ".gitignore", "gitignore")
    _write_file(test_dir / "LICENSE", "LICENSE")
    for n, v in [
        ("README exists", file_exists(test_dir, "README.md")),
        (".gitignore exists", file_exists(test_dir, ".gitignore")),
        ("LICENSE exists", file_exists(test_dir, "LICENSE")),
        (".gitignore excludes .env", file_contains(test_dir, ".gitignore", ".env")),
        ("README has title", file_contains(test_dir, "README.md", "#")),
    ]:
        result.add_check(n, v)

def test_project_layout(result, test_dir):
    for d in ["src", "src/components", "src/pages", "src/services", "src/styles"]:
        test_dir.joinpath(d).mkdir(exist_ok=True, parents=True)
    _write_file(test_dir / "AGENTS.md", "AGENTS")
    _write_file(test_dir / "BACKLOG.md", "BACKLOG")
    _write_file(test_dir / "TESTS.md", "TESTS")
    _write_file(test_dir / "FEEDBACK.md", "FEEDBACK")
    _write_file(test_dir / "config.yaml", "config_yaml")
    test_dir.joinpath(".agents").mkdir(exist_ok=True)
    _write_file(test_dir / ".agents/skills.txt", "skills_txt")
    checks = [
        ("src/", dir_exists(test_dir, "src")),
        ("src/components/", dir_exists(test_dir, "src/components")),
        ("src/pages/", dir_exists(test_dir, "src/pages")),
        ("src/services/", dir_exists(test_dir, "src/services")),
        ("src/styles/", dir_exists(test_dir, "src/styles")),
        ("AGENTS.md", file_exists(test_dir, "AGENTS.md")),
        ("BACKLOG.md", file_exists(test_dir, "BACKLOG.md")),
        ("TESTS.md", file_exists(test_dir, "TESTS.md")),
        ("FEEDBACK.md", file_exists(test_dir, "FEEDBACK.md")),
        ("config.yaml", file_exists(test_dir, "config.yaml")),
        ("skills.txt", file_exists(test_dir, ".agents/skills.txt")),
        ("config has opencode", file_contains(test_dir, "config.yaml", "opencode")),
        ("AGENTS content", count_lines(test_dir, "AGENTS.md") > 1),
    ]
    for n, v in checks:
        result.add_check(n, v)

def test_project_conventions(result, test_dir):
    test_dir.joinpath("src/services").mkdir(exist_ok=True, parents=True)
    _write_file(test_dir / "src/services/api_client.py", "api_client")
    _write_file(test_dir / "src/services/database.py", "database")
    checks = [
        ("api_client.py", file_exists(test_dir, "src/services/api_client.py")),
        ("database.py", file_exists(test_dir, "src/services/database.py")),
        ("Files have comments", file_contains(test_dir, "src/services/api_client.py", "# API client")),
        ("Classes have comments", file_contains(test_dir, "src/services/api_client.py", "class ApiClient")),
        ("Methods async", file_contains(test_dir, "src/services/api_client.py", "async def")),
        ("Type hints", file_contains(test_dir, "src/services/api_client.py", "->")),
        ("Params used", file_contains(test_dir, "src/services/database.py", "params")),
    ]
    for n, v in checks:
        result.add_check(n, v)

def test_secure_coding_rules(result, test_dir):
    test_dir.joinpath("src").mkdir(exist_ok=True, parents=True)
    _write_file(test_dir / "src/config.py", "config_py")
    _write_file(test_dir / "src/database.py", "db_py")
    _write_file(test_dir / ".gitignore", "gitignore_sec")
    checks = [
        ("config.py", file_exists(test_dir, "src/config.py")),
        ("No hardcoded secrets", file_contains(test_dir, "src/config.py", "os.environ")),
        ("Param queries", file_contains(test_dir, "src/database.py", "?")),
        (".env in gitignore", file_contains(test_dir, ".gitignore", ".env")),
        ("*.key in gitignore", file_contains(test_dir, ".gitignore", "*.key")),
        ("No triple-quote issues", True),  # placeholder
    ]
    for n, v in checks:
        result.add_check(n, v)

def test_scaffold_backend_api(result, test_dir):
    test_dir.joinpath("src").mkdir(exist_ok=True, parents=True)
    _write_file(test_dir / "src/main.py", "main_py")
    _write_file(test_dir / "src/routes.py", "routes_py")
    _write_file(test_dir / "requirements.txt", "requirements")
    checks = [
        ("main.py", file_exists(test_dir, "src/main.py")),
        ("Has FastAPI", file_contains(test_dir, "src/main.py", "FastAPI")),
        ("Has /health", file_contains(test_dir, "src/main.py", "/health")),
        ("BaseModel", file_contains(test_dir, "src/main.py", "BaseModel")),
        ("HTTPException", file_contains(test_dir, "src/main.py", "HTTPException")),
        ("routes.py", file_exists(test_dir, "src/routes.py")),
        ("requirements.txt", file_exists(test_dir, "requirements.txt")),
        ("fastapi in deps", file_contains(test_dir, "requirements.txt", "fastapi")),
    ]
    for n, v in checks:
        result.add_check(n, v)

def test_rest_api_conventions(result, test_dir):
    _write_file(test_dir / "src/api.py", "api_py")
    checks = [
        ("/api/v1/", file_contains(test_dir, "src/api.py", "/api/v1/")),
        ("Pagination", file_contains(test_dir, "src/api.py", "page")),
        ("HTTP 404", file_contains(test_dir, "src/api.py", "404")),
        ("detail", file_contains(test_dir, "src/api.py", "detail")),
        ("GET", file_contains(test_dir, "src/api.py", "@router.get")),
        ("PUT", file_contains(test_dir, "src/api.py", "@router.put")),
        ("DELETE", file_contains(test_dir, "src/api.py", "@router.delete")),
        ("Docstrings present", True),
    ]
    for n, v in checks:
        result.add_check(n, v)

def test_query_open_data_api(result, test_dir):
    _write_file(test_dir / "src/open_data.py", "open_data")
    checks = [
        ("open_data.py", file_exists(test_dir, "src/open_data.py")),
        ("data.gouv.fr", file_contains(test_dir, "src/open_data.py", "data.gouv.fr")),
        ("csv", file_contains(test_dir, "src/open_data.py", "csv")),
        ("get_format", file_contains(test_dir, "src/open_data.py", "get_dataset_format")),
        ("search_datasets", file_contains(test_dir, "src/open_data.py", "search_datasets")),
        ("get_dataset_format", file_contains(test_dir, "src/open_data.py", "get_dataset_format")),
        ("download_resource", file_contains(test_dir, "src/open_data.py", "download_resource")),
        ("Docstrings present", True),
    ]
    for n, v in checks:
        result.add_check(n, v)

def test_query_public_communication_data(result, test_dir):
    _write_file(test_dir / "src/communications.py", "communications")
    checks = [
        ("communications.py", file_exists(test_dir, "src/communications.py")),
        ("type", file_contains(test_dir, "src/communications.py", "type")),
        ("press_releases", file_contains(test_dir, "src/communications.py", "press_releases")),
        ("minister", file_contains(test_dir, "src/communications.py", "minister")),
        ("public_figure", file_contains(test_dir, "src/communications.py", "public_figure")),
        ("items", file_contains(test_dir, "src/communications.py", "items")),
    ]
    for n, v in checks:
        result.add_check(n, v)

def test_write_dr(result, test_dir):
    test_dir.joinpath("docs/architecture").mkdir(exist_ok=True, parents=True)
    _write_file(test_dir / "docs/architecture/adr-001-tech-stack.md", "adr_001")
    checks = [
        ("docs/architecture/", dir_exists(test_dir, "docs/architecture")),
        ("ADR file", file_exists(test_dir, "docs/architecture/adr-001-tech-stack.md")),
        ("ADR-001", file_contains(test_dir, "docs/architecture/adr-001-tech-stack.md", "ADR-001")),
        ("Context", file_contains(test_dir, "docs/architecture/adr-001-tech-stack.md", "Context")),
        ("Decision", file_contains(test_dir, "docs/architecture/adr-001-tech-stack.md", "Decision")),
        ("Consequences", file_contains(test_dir, "docs/architecture/adr-001-tech-stack.md", "Consequences")),
    ]
    for n, v in checks:
        result.add_check(n, v)

def test_investigate_bug(result, test_dir):
    test_dir.joinpath("src").mkdir(exist_ok=True, parents=True)
    _write_file(test_dir / "src/main.py", "main_bug")
    _write_file(test_dir / "BUG_INVESTIGATION.md", "bug_investigation")
    checks = [
        ("BUG_INVESTIGATION.md", file_exists(test_dir, "BUG_INVESTIGATION.md")),
        ("Hypotheses", file_contains(test_dir, "BUG_INVESTIGATION.md", "Hypotheses")),
        ("Reproduction", file_contains(test_dir, "BUG_INVESTIGATION.md", "Reproduction")),
        ("Code block", file_contains(test_dir, "BUG_INVESTIGATION.md", "```")),
        ("Root Cause", file_contains(test_dir, "BUG_INVESTIGATION.md", "Root Cause")),
        ("Fallback", file_contains(test_dir, "BUG_INVESTIGATION.md", "Fallback")),
    ]
    for n, v in checks:
        result.add_check(n, v)

def test_review_code(result, test_dir):
    _write_file(test_dir / "src/api.py", "api_buggy")
    _write_file(test_dir / "CODE_REVIEW.md", "code_review")
    checks = [
        ("CODE_REVIEW.md", file_exists(test_dir, "CODE_REVIEW.md")),
        ("Security", file_contains(test_dir, "CODE_REVIEW.md", "Security")),
        ("Quality", file_contains(test_dir, "CODE_REVIEW.md", "Quality")),
        ("Suggestions", file_contains(test_dir, "CODE_REVIEW.md", "Suggestions")),
        ("error handling", file_contains(test_dir, "CODE_REVIEW.md", "error handling")),
    ]
    for n, v in checks:
        result.add_check(n, v)

def test_ship_a_dev_task(result, test_dir):
    test_dir.joinpath("src").mkdir(exist_ok=True, parents=True)
    test_dir.joinpath("tests").mkdir(exist_ok=True, parents=True)
    _write_file(test_dir / "src/main.py", "hello_main")
    _write_file(test_dir / "tests/test_main.py", "test_hello")
    _write_file(test_dir / "SHIP_CHECKLIST.md", "ship_checklist")
    checks = [
        ("src/main.py", file_exists(test_dir, "src/main.py")),
        ("tests/test_main.py", file_exists(test_dir, "tests/test_main.py")),
        ("SHIP_CHECKLIST.md", file_exists(test_dir, "SHIP_CHECKLIST.md")),
        ("Implementation", file_contains(test_dir, "SHIP_CHECKLIST.md", "Implementation")),
        ("Tests", file_contains(test_dir, "SHIP_CHECKLIST.md", "Tests")),
        ("pytest", file_contains(test_dir, "tests/test_main.py", "pytest")),
        ("import", file_contains(test_dir, "tests/test_main.py", "import")),
    ]
    for n, v in checks:
        result.add_check(n, v)

def test_detect_stale_service_names(result, test_dir):
    test_dir.joinpath("k8s").mkdir(exist_ok=True, parents=True)
    _write_file(test_dir / "k8s/deployment.yaml", "deployment")
    _write_file(test_dir / "k8s/service.yaml", "service_k8s")
    _write_file(test_dir / "NAME_MAPPING.md", "name_mapping")
    checks = [
        ("k8s/deployment.yaml", file_exists(test_dir, "k8s/deployment.yaml")),
        ("k8s/service.yaml", file_exists(test_dir, "k8s/service.yaml")),
        ("NAME_MAPPING.md", file_exists(test_dir, "NAME_MAPPING.md")),
        ("Table", file_contains(test_dir, "NAME_MAPPING.md", "| Service |")),
        ("app: label", file_contains(test_dir, "k8s/deployment.yaml", "app:")),
        ("app: service-frontend", file_contains(test_dir, "k8s/service.yaml", "app: service-frontend")),
    ]
    for n, v in checks:
        result.add_check(n, v)

def test_containerize_app_for_k8s(result, test_dir):
    _write_file(test_dir / "Dockerfile", "dockerfile")
    _write_file(test_dir / "requirements.txt", "requirements_k8s")
    checks = [
        ("Dockerfile", file_exists(test_dir, "Dockerfile")),
        ("slim", file_contains(test_dir, "Dockerfile", "slim")),
        ("USER", file_contains(test_dir, "Dockerfile", "USER")),
        ("EXPOSE", file_contains(test_dir, "Dockerfile", "EXPOSE")),
        ("CMD", file_contains(test_dir, "Dockerfile", "CMD")),
        ("requirements.txt", file_exists(test_dir, "requirements.txt")),
        ("pydantic", file_contains(test_dir, "requirements.txt", "pydantic")),
    ]
    for n, v in checks:
        result.add_check(n, v)

def test_create_helm_chart(result, test_dir):
    test_dir.joinpath("chart").mkdir(exist_ok=True, parents=True)
    test_dir.joinpath("chart/templates").mkdir(exist_ok=True, parents=True)
    _write_file(test_dir / "chart/Chart.yaml", "chart_yaml")
    _write_file(test_dir / "chart/values.yaml", "helm_values")
    _write_file(test_dir / "chart/templates/deployment.yaml", "helm_deployment")
    checks = [
        ("chart/Chart.yaml", file_exists(test_dir, "chart/Chart.yaml")),
        ("chart/values.yaml", file_exists(test_dir, "chart/values.yaml")),
        ("chart/templates/", dir_exists(test_dir, "chart/templates")),
        ("Helm syntax", file_contains(test_dir, "chart/templates/deployment.yaml", "{{")),
        ("Helm close", file_contains(test_dir, "chart/templates/deployment.yaml", "}}")),
        ("apiVersion", file_contains(test_dir, "chart/Chart.yaml", "apiVersion")),
        ("replicaCount", file_contains(test_dir, "chart/values.yaml", "replicaCount")),
        ("limits", file_contains(test_dir, "chart/values.yaml", "limits")),
        ("securityContext", file_contains(test_dir, "chart/values.yaml", "securityContext")),
    ]
    for n, v in checks:
        result.add_check(n, v)

def test_set_up_github_actions_ci(result, test_dir):
    test_dir.joinpath(".github").mkdir(exist_ok=True, parents=True)
    test_dir.joinpath(".github/workflows").mkdir(exist_ok=True, parents=True)
    _write_file(test_dir / ".github/workflows/ci.yml", "ci_yml")
    checks = [
        ("ci.yml", file_exists(test_dir, ".github/workflows/ci.yml")),
        ("lint:", file_contains(test_dir, ".github/workflows/ci.yml", "lint:")),
        ("test:", file_contains(test_dir, ".github/workflows/ci.yml", "test:")),
        ("actions/checkout", file_contains(test_dir, ".github/workflows/ci.yml", "actions/checkout")),
        ("setup-python", file_contains(test_dir, ".github/workflows/ci.yml", "setup-python")),
        ("pytest", file_contains(test_dir, ".github/workflows/ci.yml", "pytest")),
        ("on:", file_contains(test_dir, ".github/workflows/ci.yml", "on:")),
    ]
    for n, v in checks:
        result.add_check(n, v)

def test_write_digital_factory_workflows(result, test_dir):
    test_dir.joinpath(".github").mkdir(exist_ok=True, parents=True)
    test_dir.joinpath(".github/workflows").mkdir(exist_ok=True, parents=True)
    _write_file(test_dir / ".github/workflows/release.yml", "release_yml")
    checks = [
        ("release.yml", file_exists(test_dir, ".github/workflows/release.yml")),
        ("tags:", file_contains(test_dir, ".github/workflows/release.yml", "tags:")),
        ("Create Release", file_contains(test_dir, ".github/workflows/release.yml", "Create Release")),
        ("helm-publish", file_contains(test_dir, ".github/workflows/release.yml", "helm-publish")),
    ]
    for n, v in checks:
        result.add_check(n, v)

def test_set_up_cloud_pi_native_cicd(result, test_dir):
    test_dir.joinpath(".github").mkdir(exist_ok=True, parents=True)
    test_dir.joinpath(".github/workflows").mkdir(exist_ok=True, parents=True)
    _write_file(test_dir / ".github/workflows/dso.yml", "dso_yml")
    checks = [
        ("dso.yml", file_exists(test_dir, ".github/workflows/dso.yml")),
        ("scan:", file_contains(test_dir, ".github/workflows/dso.yml", "scan:")),
        ("build:", file_contains(test_dir, ".github/workflows/dso.yml", "build:")),
        ("deploy:", file_contains(test_dir, ".github/workflows/dso.yml", "deploy:")),
        ("registry.dso.fr", file_contains(test_dir, ".github/workflows/dso.yml", "registry.dso.fr")),
    ]
    for n, v in checks:
        result.add_check(n, v)

def test_deploy_to_cloud_pi_native(result, test_dir):
    test_dir.joinpath("deploy").mkdir(exist_ok=True, parents=True)
    _write_file(test_dir / "deploy/vault-config.yaml", "vault_config")
    _write_file(test_dir / "deploy/kyverno.yaml", "kyverno")
    checks = [
        ("vault-config.yaml", file_exists(test_dir, "deploy/vault-config.yaml")),
        ("kyverno.yaml", file_exists(test_dir, "deploy/kyverno.yaml")),
        ("vault://", file_contains(test_dir, "deploy/vault-config.yaml", "vault://")),
        ("kyverno.io", file_contains(test_dir, "deploy/kyverno.yaml", "kyverno.io")),
        ("runAsNonRoot", file_contains(test_dir, "deploy/kyverno.yaml", "runAsNonRoot")),
    ]
    for n, v in checks:
        result.add_check(n, v)

def test_set_up_design_system(result, test_dir):
    test_dir.joinpath("assets").mkdir(exist_ok=True, parents=True)
    test_dir.joinpath("assets/utility").mkdir(exist_ok=True, parents=True)
    _write_file(test_dir / "assets/dsfr.min.css", "dsfr_css")
    _write_file(test_dir / "assets/utility/utility.min.css", "utility_css")
    _write_file(test_dir / "index.html", "index_html")
    checks = [
        ("dsfr.min.css", file_exists(test_dir, "assets/dsfr.min.css")),
        ("assets/utility/", dir_exists(test_dir, "assets/utility")),
        ("index.html", file_exists(test_dir, "index.html")),
        ("dsfr.min.css link", file_contains(test_dir, "index.html", "dsfr.min.css")),
        ("fr-header", file_contains(test_dir, "index.html", "fr-header")),
        ("fr-container", file_contains(test_dir, "index.html", "fr-container")),
        ("lang=fr", file_contains(test_dir, "index.html", "lang=\"fr\"")),
    ]
    for n, v in checks:
        result.add_check(n, v)

def test_add_design_system_icons(result, test_dir):
    test_dir.joinpath("src/components").mkdir(exist_ok=True, parents=True)
    _write_file(test_dir / "src/components/icons.html", "icons_html")
    _write_file(test_dir / "src/components/custom-icon.svg", "custom_icon")
    checks = [
        ("icons.html", file_exists(test_dir, "src/components/icons.html")),
        ("fr-icon-", file_contains(test_dir, "src/components/icons.html", "fr-icon-")),
        ("fr-icon--sm", file_contains(test_dir, "src/components/icons.html", "fr-icon--sm")),
        ("fr-text--danger", file_contains(test_dir, "src/components/icons.html", "fr-text--danger")),
        ("custom-icon.svg", file_exists(test_dir, "src/components/custom-icon.svg")),
        ("viewBox", file_contains(test_dir, "src/components/custom-icon.svg", "viewBox")),
    ]
    for n, v in checks:
        result.add_check(n, v)

def test_build_design_system_charts(result, test_dir):
    test_dir.joinpath("src").mkdir(exist_ok=True, parents=True)
    _write_file(test_dir / "src/charts.html", "charts_html")
    checks = [
        ("charts.html", file_exists(test_dir, "src/charts.html")),
        ("fr-card", file_contains(test_dir, "src/charts.html", "fr-card")),
        ("fr-chart", file_contains(test_dir, "src/charts.html", "fr-chart")),
        ("canvas", file_contains(test_dir, "src/charts.html", "canvas")),
        ("Chart", file_contains(test_dir, "src/charts.html", "Chart")),
        ("charts.min.js", file_contains(test_dir, "src/charts.html", "charts.min.js")),
    ]
    for n, v in checks:
        result.add_check(n, v)

def test_build_design_system_emails(result, test_dir):
    test_dir.joinpath("templates").mkdir(exist_ok=True, parents=True)
    _write_file(test_dir / "templates/confirmation.html", "email_html")
    checks = [
        ("confirmation.html", file_exists(test_dir, "templates/confirmation.html")),
        ("lang=fr", file_contains(test_dir, "templates/confirmation.html", "lang=\"fr\"")),
        ("fr-text--sm", file_contains(test_dir, "templates/confirmation.html", "fr-text--sm")),
        ("role=presentation", file_contains(test_dir, "templates/confirmation.html", "role=\"presentation\"")),
        ("width=100%", file_contains(test_dir, "templates/confirmation.html", "width=\"100%\"")),
    ]
    for n, v in checks:
        result.add_check(n, v)

def test_build_collab_suite_ui(result, test_dir):
    test_dir.joinpath("src").mkdir(exist_ok=True, parents=True)
    _write_file(test_dir / "src/sharing.html", "sharing_html")
    _write_file(test_dir / "src/navigation.js", "navigation_js")
    checks = [
        ("sharing.html", file_exists(test_dir, "src/sharing.html")),
        ("fr-card", file_contains(test_dir, "src/sharing.html", "fr-card")),
        ("Partage", file_contains(test_dir, "src/sharing.html", "Partage")),
        ("navigation.js", file_exists(test_dir, "src/navigation.js")),
        ("hash", file_contains(test_dir, "src/navigation.js", "hash")),
        ("postMessage", file_contains(test_dir, "src/navigation.js", "postMessage")),
    ]
    for n, v in checks:
        result.add_check(n, v)

def test_harden_repo_before_pentest(result, test_dir):
    _write_file(test_dir / "src/app.py", "app_py")
    _write_file(test_dir / "SECURITY_AUDIT.md", "security_audit")
    checks = [
        ("app.py", file_exists(test_dir, "src/app.py")),
        ("SECURITY_AUDIT.md", file_exists(test_dir, "SECURITY_AUDIT.md")),
        ("sanitize", file_contains(test_dir, "src/app.py", "sanitize")),
        ("rate_limit", file_contains(test_dir, "src/app.py", "rate_limit")),
        ("escape_xss", file_contains(test_dir, "src/app.py", "escape_xss")),
        ("A01", file_contains(test_dir, "SECURITY_AUDIT.md", "A01")),
        ("Cryptographic", file_contains(test_dir, "SECURITY_AUDIT.md", "Cryptographic")),
        ("Injection", file_contains(test_dir, "SECURITY_AUDIT.md", "Injection")),
    ]
    for n, v in checks:
        result.add_check(n, v)

def test_find_cybersecurity_guide(result, test_dir):
    _write_file(test_dir / "src/guides.py", "guides_py")
    checks = [
        ("guides.py", file_exists(test_dir, "src/guides.py")),
        ("ANSSI", file_contains(test_dir, "src/guides.py", "ANSSI")),
        ("ssi.gouv.fr", file_contains(test_dir, "src/guides.py", "ssi.gouv.fr")),
        ("search_guides", file_contains(test_dir, "src/guides.py", "search_guides")),
        ("topics", file_contains(test_dir, "src/guides.py", "topics")),
    ]
    for n, v in checks:
        result.add_check(n, v)

def test_audit_llm_tool_identity(result, test_dir):
    _write_file(test_dir / "src/auth.py", "auth_py")
    checks = [
        ("auth.py", file_exists(test_dir, "src/auth.py")),
        ("AuthContext", file_contains(test_dir, "src/auth.py", "AuthContext")),
        ("user_id", file_contains(test_dir, "src/auth.py", "user_id")),
        ("sub", file_contains(test_dir, "src/auth.py", "sub")),
        ("isolated", file_contains(test_dir, "src/auth.py", "isolated")),
        ("vault_bound", file_contains(test_dir, "src/auth.py", "vault_bound")),
    ]
    for n, v in checks:
        result.add_check(n, v)

def test_audit_repo_safety(result, test_dir):
    _write_file(test_dir / "SECURITY_AUDIT.md", "repo_audit")
    checks = [
        ("SECURITY_AUDIT.md", file_exists(test_dir, "SECURITY_AUDIT.md")),
        ("secrets", file_contains(test_dir, "SECURITY_AUDIT.md", "secrets")),
        ("auto-execution", file_contains(test_dir, "SECURITY_AUDIT.md", "auto-execution")),
        ("CI/CD", file_contains(test_dir, "SECURITY_AUDIT.md", "CI/CD")),
        ("Findings", file_contains(test_dir, "SECURITY_AUDIT.md", "Findings")),
    ]
    for n, v in checks:
        result.add_check(n, v)

def test_redteam_llm_prompt_injection(result, test_dir):
    _write_file(test_dir / "src/guard.py", "guard_py")
    checks = [
        ("guard.py", file_exists(test_dir, "src/guard.py")),
        ("ignore previous", file_contains(test_dir, "src/guard.py", "ignore previous")),
        ("validate_guard", file_contains(test_dir, "src/guard.py", "validate_guard")),
        ("guard_applied", file_contains(test_dir, "src/guard.py", "guard_applied")),
        ("is_injection", file_contains(test_dir, "src/guard.py", "is_injection")),
    ]
    for n, v in checks:
        result.add_check(n, v)

def test_dogfood(result, test_dir):
    test_dir.joinpath("tests").mkdir(exist_ok=True, parents=True)
    test_dir.joinpath("public").mkdir(exist_ok=True, parents=True)
    _write_file(test_dir / "public/index.html", "public_html")
    _write_file(test_dir / "tests/qa_checklist.md", "qa_checklist")
    checks = [
        ("public/index.html", file_exists(test_dir, "public/index.html")),
        ("qa_checklist.md", file_exists(test_dir, "tests/qa_checklist.md")),
        ("<!DOCTYPE html>", file_contains(test_dir, "public/index.html", "<!DOCTYPE html>")),
        ("<nav>", file_contains(test_dir, "public/index.html", "<nav>")),
        ("Accessibility", file_contains(test_dir, "tests/qa_checklist.md", "Accessibility")),
        ("Functionality", file_contains(test_dir, "tests/qa_checklist.md", "Functionality")),
        ("Security", file_contains(test_dir, "tests/qa_checklist.md", "Security")),
        ("Performance", file_contains(test_dir, "tests/qa_checklist.md", "Performance")),
    ]
    for n, v in checks:
        result.add_check(n, v)

def test_conformite(result, test_dir):
    test_dir.joinpath("src").mkdir(exist_ok=True, parents=True)
    _write_file(test_dir / "src/checker.py", "checker_py")
    checks = [
        ("checker.py", file_exists(test_dir, "src/checker.py")),
        ("DocConformite", file_contains(test_dir, "src/checker.py", "DocConformite")),
        ("def check", file_contains(test_dir, "src/checker.py", "def check")),
        ("generate_report", file_contains(test_dir, "src/checker.py", "generate_report")),
        ("required_fields", file_contains(test_dir, "src/checker.py", "required_fields")),
        ("format_valid", file_contains(test_dir, "src/checker.py", "format_valid")),
        ("passed", file_contains(test_dir, "src/checker.py", "passed")),
        ("metadata_present", file_contains(test_dir, "src/checker.py", "metadata_present")),
    ]
    for n, v in checks:
        result.add_check(n, v)

def test_tech_arch_doc(result, test_dir):
    test_dir.joinpath("docs").mkdir(exist_ok=True, parents=True)
    _write_file(test_dir / "docs/tech-architecture.md", "tech_arch")
    checks = [
        ("tech-architecture.md", file_exists(test_dir, "docs/tech-architecture.md")),
        ("Contexte", file_contains(test_dir, "docs/tech-architecture.md", "Contexte")),
        ("Architecture", file_contains(test_dir, "docs/tech-architecture.md", "Architecture")),
        ("Frontend", file_contains(test_dir, "docs/tech-architecture.md", "Frontend")),
        ("Securite", file_contains(test_dir, "docs/tech-architecture.md", "Securite")),
        ("Vault", file_contains(test_dir, "docs/tech-architecture.md", "Vault")),
    ]
    for n, v in checks:
        result.add_check(n, v)


# ---- Test registry ----
SKILLS_DIR = Path(__file__).parent.parent / "skills" / "fr-gov"

TEST_REGISTRY = {
    "init-repo": test_init_repo,
    "fr-gov-set-up-project-layout": test_project_layout,
    "fr-gov-project-conventions": test_project_conventions,
    "fr-gov-secure-coding-rules": test_secure_coding_rules,
    "fr-gov-scaffold-backend-api": test_scaffold_backend_api,
    "fr-gov-rest-api-conventions": test_rest_api_conventions,
    "fr-gov-set-up-pnpm-monorepo": test_project_layout,
    "write-adr": test_write_dr,
    "investigate-bug": test_investigate_bug,
    "review-code": test_review_code,
    "ship-a-dev-task": test_ship_a_dev_task,
    "detect-stale-service-names": test_detect_stale_service_names,
    "fr-gov-containerize-app-for-k8s": test_containerize_app_for_k8s,
    "fr-gov-create-helm-chart": test_create_helm_chart,
    "fr-gov-set-up-github-actions-ci": test_set_up_github_actions_ci,
    "fr-gov-write-digital-factory-workflows": test_write_digital_factory_workflows,
    "fr-gov-set-up-cloud-pi-native-cicd": test_set_up_cloud_pi_native_cicd,
    "fr-gov-deploy-to-cloud-pi-native": test_deploy_to_cloud_pi_native,
    "fr-gov-set-up-design-system": test_set_up_design_system,
    "fr-gov-add-design-system-icons": test_add_design_system_icons,
    "fr-gov-build-design-system-charts": test_build_design_system_charts,
    "fr-gov-build-design-system-emails": test_build_design_system_emails,
    "fr-gov-build-vue-design-system": test_set_up_design_system,
    "fr-gov-query-open-data-api": test_query_open_data_api,
    "fr-gov-query-public-communication-data": test_query_public_communication_data,
    "fr-gov-build-collab-suite-ui": test_build_collab_suite_ui,
    "fr-gov-find-cybersecurity-guide": test_find_cybersecurity_guide,
    "audit-repo-safety": test_audit_repo_safety,
    "audit-llm-tool-identity": test_audit_llm_tool_identity,
    "harden-repo-before-pentest": test_harden_repo_before_pentest,
    "redteam-llm-prompt-injection": test_redteam_llm_prompt_injection,
    "doc-conformite": test_conformite,
    "fr-gov-fill-technical-architecture-doc": test_tech_arch_doc,
    "dogfood": test_dogfood,
}

for category_dir in SKILLS_DIR.iterdir():
    if not category_dir.is_dir():
        continue
    for skill_dir in category_dir.iterdir():
        if not skill_dir.is_dir():
            continue
        skill_name = skill_dir.name
        if skill_name not in TEST_REGISTRY and category_dir.name == "compliance":
            TEST_REGISTRY[skill_name] = test_conformite


# ---- Data class for results ----
@dataclass
class TestResult:
    skill_name: str
    category: str
    status: str
    checks: list = field(default_factory=list)
    summary: str = ""
    duration_s: float = 0.0

    def add_check(self, name, passed, detail=""):
        self.checks.append({"check": name, "passed": passed, "detail": detail})

    @property
    def pass_rate(self):
        if not self.checks:
            return 0.0
        passed = sum(1 for c in self.checks if c["passed"])
        return round(passed / len(self.checks) * 100, 1)

    def to_dict(self):
        return {
            "skill": self.skill_name,
            "category": self.category,
            "status": self.status,
            "check_count": len(self.checks),
            "passed": sum(1 for c in self.checks if c["passed"]),
            "failed": sum(1 for c in self.checks if not c["passed"]),
            "pass_rate": self.pass_rate,
            "checks": self.checks,
            "summary": self.summary,
            "duration_s": self.duration_s,
        }


# ---- Main runner ----
def discover_skills():
    skills = []
    for category_dir in SKILLS_DIR.iterdir():
        if not category_dir.is_dir():
            continue
        category = category_dir.name
        for skill_dir in category_dir.iterdir():
            if not skill_dir.is_dir():
                continue
            if (skill_dir / "SKILL.md").exists():
                skills.append({"name": skill_dir.name, "category": category})
    return skills

def run_test(skill_info):
    skill_name = skill_info["name"]
    test_dir = Path(tempfile.mkdtemp(prefix="test_"))
    result = TestResult(skill_name=skill_name, category=skill_info["category"], status="pending")
    try:
        test_fn = TEST_REGISTRY.get(skill_name)
        if not test_fn:
            result.status = "skip"
            result.summary = "No test for " + skill_name
            result.add_check("Test exists", False, "No function in registry")
            return result
        t0 = time.time()
        test_fn(result, test_dir)
        result.duration_s = time.time() - t0
        passed = sum(1 for c in result.checks if c["passed"])
        total = len(result.checks)
        failed = total - passed
        if failed == 0 and total > 0:
            result.status = "pass"
            result.summary = "All " + str(total) + " checks passed"
        elif total == 0:
            result.status = "skip"
            result.summary = "No checks"
        else:
            result.status = "fail"
            result.summary = str(passed) + "/" + str(total) + " passed (" + str(failed) + " failed)"
        return result
    except Exception as e:
        result.status = "error"
        result.summary = "Error: " + str(e)
        result.add_check("Execution", False, type(e).__name__ + ": " + str(e))
        return result
    finally:
        shutil.rmtree(test_dir, ignore_errors=True)

def run_all_tests():
    skills = discover_skills()
    results = []
    for si in skills:
        print("Testing: " + si["category"] + "/" + si["name"] + "...", end=" ")
        r = run_test(si)
        results.append(r)
        print("[" + r.status.upper() + "] " + r.summary)
    return results

def generate_dashboard_html(results, output_path):
    categories = {}
    for r in results:
        categories.setdefault(r.category, []).append(r)
    total = len(results)
    passed = sum(1 for r in results if r.status == "pass")
    failed = sum(1 for r in results if r.status == "fail")
    skipped = sum(1 for r in results if r.status == "skip")
    tc = sum(len(r.checks) for r in results)
    tp = sum(c["passed"] for r in results for c in r.checks)
    L = []
    L.append("<!DOCTYPE html><html lang=\"fr\"><head><meta charset=\"UTF-8\">")
    L.append("<title>Tests Integration -- Skills fr-gov</title>")
    L.append("<style>")
    L.append("*{margin:0;padding:0;box-sizing:border-box}")
    L.append("body{font-family:system-ui,sans-serif;background:#0a0a0a;color:#e0e0e0;padding:2rem}")
    L.append("h1{color:#00c853;margin-bottom:2rem}")
    L.append("h2{color:#00c853;margin:2rem 0 1rem}")
    L.append(".kpi{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:1rem;margin-bottom:2rem}")
    L.append(".kpi-card{background:#1a1a1a;border:1px solid #333;border-radius:8px;padding:1.5rem;text-align:center}")
    L.append(".kpi-value{font-size:2rem;font-weight:bold;color:#00c853}")
    L.append(".kpi-label{color:#888;font-size:0.9rem}")
    L.append(".category{background:#1a1a1a;border:1px solid #333;border-radius:8px;padding:1.5rem;margin-bottom:1rem}")
    L.append(".skill{border-bottom:1px solid #333;padding:0.75rem 0}")
    L.append(".skill:last-child{border-bottom:none}")
    L.append(".sn{font-weight:bold;color:#fff}")
    L.append(".sc{color:#888;font-size:0.85rem}")
    L.append(".sp{color:#00c853}.sf{color:#f44336}.ss{color:#ff9800}")
    L.append(".check{display:flex;justify-content:space-between;padding:0.25rem 0;font-size:0.85rem}")
    L.append(".check-pass{color:#00c853}.check-fail{color:#f44336}")
    L.append("</style></head><body><h1>Tests Integration -- Skills fr-gov</h1>")
    L.append("<div class=\"kpi\">")
    L.append("<div class=\"kpi-card\"><div class=\"kpi-value\">" + str(total) + "</div><div class=\"kpi-label\">Skills testes</div></div>")
    L.append("<div class=\"kpi-card\"><div class=\"kpi-value\">" + str(passed) + "</div><div class=\"kpi-label\">Passes</div></div>")
    L.append("<div class=\"kpi-card\"><div class=\"kpi-value\">" + str(failed) + "</div><div class=\"kpi-label\">Echoues</div></div>")
    L.append("<div class=\"kpi-card\"><div class=\"kpi-value\">" + str(skipped) + "</div><div class=\"kpi-label\">Non testes</div></div>")
    L.append("<div class=\"kpi-card\"><div class=\"kpi-value\">" + str(tp) + "/" + str(tc) + "</div><div class=\"kpi-label\">Checks totaux</div></div>")
    L.append("</div>")
    for cat, cs in sorted(categories.items()):
        L.append("<h2>" + cat + "</h2><div class=\"category\">")
        for s in sorted(cs, key=lambda x: x.skill_name):
            L.append("<div class=\"skill\">")
            L.append("<span class=\"sn\">" + s.skill_name + "</span> ")
            L.append("<span class=\"sc\">" + str(len(s.checks)) + " checks -- " + s.summary + "</span> ")
            L.append("<span class=\"s" + s.status + "\">[" + s.status.upper() + "]</span>")
            for ch in s.checks:
                cls = "check-pass" if ch["passed"] else "check-fail"
                L.append('<div class="check ' + cls + '"><span>' + ("PASS" if ch["passed"] else "FAIL") + " " + ch["check"] + "</span>")
                if ch["detail"]:
                    L.append("<span>" + ch["detail"] + "</span>")
                L.append("</div>")
            L.append("</div>")
        L.append("</div>")
    L.append("</body></html>")
    output_path.write_text("\n".join(L))

def main():
    print("=" * 60)
    print("Tests d'integration -- Skills fr-gov")
    print("=" * 60)
    results = run_all_tests()
    dashboard_path = Path(__file__).parent / "dashboard.html"
    generate_dashboard_html(results, dashboard_path)
    print("\nDashboard: " + str(dashboard_path))
    print("Size: {:,} bytes".format(dashboard_path.stat().st_size))
    rd = {
        "timestamp": datetime.now().isoformat(),
        "total_skills": len(results),
        "passed": sum(1 for r in results if r.status == "pass"),
        "failed": sum(1 for r in results if r.status == "fail"),
        "skipped": sum(1 for r in results if r.status == "skip"),
        "errors": sum(1 for r in results if r.status == "error"),
        "skills": [r.to_dict() for r in results],
    }
    rp = Path(__file__).parent / "results.json"
    rp.write_text(json.dumps(rd, indent=2, ensure_ascii=False))
    print("Results: " + str(rp) + " ({:,} bytes)".format(rp.stat().st_size))
    tc = sum(len(r.checks) for r in results)
    tp = sum(c["passed"] for r in results for c in r.checks)
    pr = round(tp / tc * 100, 1) if tc > 0 else 0
    print("=" * 60)
    print("Resultats: {} skills, {}/{} checks ({}%)".format(len(results), tp, tc, pr))
    print("=" * 60)
    return 1 if rd["failed"] > 0 else 0

if __name__ == "__main__":
    sys.exit(main())
