# Git

### Branch naming

```
<type>/<kebab-description>#<ticket>
```

Types : `feat`, `fix`, `hotfix`, `tech`, `docs`, `refactor`

### Commit messages

Conventional Commits. Français acceptable.

```
feat: ajouter authentification JWT#123
fix: corriger le nommage de la variable user#124
tech: mise à jour des dépendances#125
```

### Pull Requests

- Une PR = une intention
- Jamais de `--force` sur les branches partagées
- Review obligatoire avant merge

### Trailer obligatoire

Le trailer de co-auteur est une convention du projet : l'identifiant et
l'adresse de contact sont ceux de l'équipe, à renseigner selon la charte
interne. Ne pas utiliser d'adresse personnelle.

```
Co-Authored-By: <equipe> (<id>) <noreply@numerique.gouv.fr>
```

### Configuration Git

```shell
git config --global init.defaultBranch main
git config --global user.name "Your Name"
git config --global user.email "email@example.com"
```

### zsh aliases

Ajouter à `~/.zshrc` :

```zsh
alias gfeat='git switch -c feat/$1 && ding'
alias gfix='git switch -c fix/$1 && ding'
alias gtech='git switch -c tech/$1 && ding'

ding() {
  [ "$(uname -s)" = "Darwin" ] && afplay /System/Library/Sounds/Glass.aiff &>/dev/null &
  [ "$(uname -s)" != "Darwin" ] && play /path/to/ok.mp3 &>/dev/null &
}
```

### Alias zsh (méthode alternative)

```bash
createFeatBranch() { (git switch -c "feat/$1" && ding) || dong }
createFixBranch() { (git switch -c "fix/$1" && ding) || dong }
createTechBranch() { (git switch -c "tech/$1" && ding) || dong }

alias gfeat='createFeatBranch'
alias gfix='createFixBranch'
alias gtech='createTechBranch'
```

