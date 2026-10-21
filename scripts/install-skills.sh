#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Installe les skills gouv-fr pour un assistant de code.

Usage: scripts/install-skills.sh [options]

Les skills sont organizees par groupe dans skills/gouv-fr/<groupe>/<skill>/.
Par defaut, ils sont installes a plat dans <destination>/<groupe>/<skill>/ :
le dossier de groupe est conserve, ce qui evite toute collision de nom entre
groupes.

Options:
  --agent <nom>    hermes, opencode, kilo, claude ou all (defaut: all)
  --scope <portee> user ou project (defaut: user)
  --project <dir>  racine du projet pour --scope project (defaut: repertoire courant)
  --flat            installe a plat dans <destination>/<skill>/ (sans le groupe)
  --force           remplace les skills gouv-fr deja installes
  --migrate         archive les anciennes copies gouv-fr-* hors du dossier actif
  -h, --help        affiche cette aide
EOF
}

agent="all"
scope="user"
project_root="$PWD"
force=false
flat=false
migrate=false

while (($#)); do
  case "$1" in
    --agent)
      [[ $# -ge 2 ]] || { echo "Erreur: --agent attend une valeur" >&2; exit 2; }
      agent="$2"
      shift 2
      ;;
    --scope)
      [[ $# -ge 2 ]] || { echo "Erreur: --scope attend une valeur" >&2; exit 2; }
      scope="$2"
      shift 2
      ;;
    --project)
      [[ $# -ge 2 ]] || { echo "Erreur: --project attend un chemin" >&2; exit 2; }
      project_root="$2"
      shift 2
      ;;
    --flat)
      flat=true
      shift
      ;;
    --force)
      force=true
      shift
      ;;
    --migrate)
      migrate=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Erreur: option inconnue: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

case "$agent" in
  hermes|opencode|kilo|claude|all) ;;
  *) echo "Erreur: agent inconnu: $agent" >&2; exit 2 ;;
esac

case "$scope" in
  user|project) ;;
  *) echo "Erreur: portee inconnue: $scope" >&2; exit 2 ;;
esac

script_dir="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(dirname "$script_dir")"
skills_root="$repo_root/skills/gouv-fr"

destination_for() {
  local current_agent="$1"

  if [[ "$scope" == "project" ]]; then
    case "$current_agent" in
      hermes) echo "$project_root/.hermes/skills" ;;
      opencode) echo "$project_root/.opencode/skills" ;;
      kilo) echo "$project_root/.kilocode/skills" ;;
      claude) echo "$project_root/.claude/skills" ;;
    esac
  else
    case "$current_agent" in
      hermes) echo "${HERMES_HOME:-$HOME/.hermes}/skills" ;;
      opencode) echo "${XDG_CONFIG_HOME:-$HOME/.config}/opencode/skills" ;;
      kilo) echo "${KILO_HOME:-$HOME/.kilocode}/skills" ;;
      claude) echo "${CLAUDE_HOME:-$HOME/.claude}/skills" ;;
    esac
  fi
}

install_for() {
  local current_agent="$1"
  local destination
  local source
  local target
  local group
  local legacy
  local backup
  local -a sources=() targets=() legacy_paths=()
  destination="$(destination_for "$current_agent")"

  # Préparer et vérifier tout le plan avant de remplacer ou déplacer un fichier.
  for group in "$skills_root"/*/; do
    [[ -d "$group" ]] || continue
    group="$(basename "$group")"
    for source in "$skills_root/$group"/*/; do
      [[ -d "$source" && -f "$source/SKILL.md" ]] || continue
      if [[ "$flat" == true ]]; then
        target="$destination/$(basename "$source")"
      else
        target="$destination/$group/$(basename "$source")"
      fi
      sources+=("$source")
      targets+=("$target")
      legacy="$destination/gouv-fr-$(basename "$source")"
      if [[ -e "$legacy" || -L "$legacy" ]]; then
        legacy_paths+=("$legacy")
      fi
      if [[ -e "$target" || -L "$target" ]]; then
        if [[ "$force" != true ]]; then
          echo "Erreur: $target existe déjà (utilisez --force pour le remplacer)" >&2
          return 1
        fi
      fi
    done
  done

  if (( ${#legacy_paths[@]} )) && [[ "$migrate" != true ]]; then
    echo "Erreur: anciennes copies détectées dans $destination ; relancez avec --migrate (sauvegarde conservée)." >&2
    return 1
  fi

  mkdir -p "$destination"
  local index
  for index in "${!sources[@]}"; do
    target="${targets[$index]}"
    mkdir -p "$(dirname "$target")"
    if [[ -e "$target" || -L "$target" ]]; then
      rm -rf "$target"
    fi
    cp -R "${sources[$index]}" "$target"
  done

  # Les nouvelles copies sont posées avant l'archivage. Ne jamais supprimer les anciennes.
  if (( ${#legacy_paths[@]} )); then
    backup="$(mktemp -d "${destination}.backup-XXXXXX")"
    for legacy in "${legacy_paths[@]}"; do
      mv "$legacy" "$backup/"
    done
    printf '%s: anciennes copies conservées dans %s\n' "$current_agent" "$backup"
  fi

  printf '%s: skills installés dans %s\n' "$current_agent" "$destination"
}

if [[ "$agent" == "all" ]]; then
  for current_agent in hermes opencode kilo claude; do
    install_for "$current_agent"
  done
else
  install_for "$agent"
fi
