# Installation machine

### Windows

#### WSL

```shell
# PowerShell (Admin)
wsl --install
# Recommandé : Ubuntu
wsl --install -d Ubuntu
```

#### Installer dans WSL

```shell
sudo apt update && sudo apt install -y git zsh docker.io
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
curl proto.sh | sh
```

#### VS Code

Utiliser **l'extension WSL** — ouvrir les dossiers dans WSL, pas dans Windows.

### macOS

#### Homebrew

```shell
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Installer

```shell
brew install git zsh proto docker
```

#### VS Code

```shell
code --install-extension dbaeumer.vscode-eslint
code --install-extension ms-vscode.vscode-docker
code --install-extension Prisma.prisma
```

### Ubuntu

```shell
sudo apt update
sudo apt install -y git zsh docker.io
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
curl proto.sh | sh
```

```shell
# Docker : ajouter l'utilisateur au groupe
sudo usermod -aG docker $USER
# Reconnexion requise
```

### Proto Setup

Créer `.prototools` à la racine du projet :

```
node 24.13.1
pnpm 10.0.0
```

Proto bascule automatiquement les versions au changement de répertoire.

