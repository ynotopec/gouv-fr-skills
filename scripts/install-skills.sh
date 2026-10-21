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
  -h, --help        affiche cette aide
EOF
}

agent="all"
scope="user"
project_root="$PWD"
force=false
flat=false

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
  destination="$(destination_for "$current_agent")"
  mkdir -p "$destination"

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
      mkdir -p "$(dirname "$target")"
      if [[ -e "$target" || -L "$target" ]]; then
        if [[ "$force" != true ]]; then
          echo "Erreur: $target existe déjà (utilisez --force pour le remplacer)" >&2
          return 1
        fi
        rm -rf "$target"
      fi
      cp -R "$source" "$target"
    done
  done

  printf '%s: skills installés dans %s\n' "$current_agent" "$destination"
}

if [[ "$agent" == "all" ]]; then
  for current_agent in hermes opencode kilo claude; do
    install_for "$current_agent"
  done
else
  install_for "$agent"
fi
