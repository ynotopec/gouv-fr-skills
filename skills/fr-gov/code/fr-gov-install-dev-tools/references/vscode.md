# Extensions VS Code

| Extension | Purpose |
|---|---|
| ESLint | JS/TS linting |
| Prisma | Schema highlighting |
| Python | Python support |
| Docker | Containers |
| REST Client | API testing |

### VS Code Settings

`.vscode/settings.json` :

```json
{
  "[javascript][typescript][vue]": {
    "editor.defaultFormatter": "dbaeumer.vscode-eslint",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": { "source.fixAll.eslint": "explicit" }
  },
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll": "explicit",
      "source.organizeImports": "explicit"
    }
  },
  "editor.rulers": [120, 140]
}
```

