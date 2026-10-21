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
  --migrate         archive les anciens noms/groupes hors du dossier actif
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
renames_file="$script_dir/skill-renames.tsv"
retirements_file="$script_dir/skill-retirements.tsv"
[[ -f "$renames_file" ]] || { echo "Erreur: table locale des renommages absente" >&2; exit 1; }
[[ -f "$retirements_file" ]] || { echo "Erreur: table locale des retraits absente" >&2; exit 1; }

legacy_candidates_for() {
  local destination="$1" current_group="$2" current_name="$3"
  local old_group old_name new_group new_name
  printf '%s\n' "$destination/gouv-fr-$current_name"
  # Détecter aussi le passage entre les installations groupée et à plat.
  printf '%s\n' "$destination/$current_group/$current_name" "$destination/$current_name"
  while IFS=$'\t' read -r old_group old_name new_group new_name; do
    [[ "$old_group" == \#* || -z "$old_group" ]] && continue
    if [[ "$new_group" == "$current_group" && "$new_name" == "$current_name" ]]; then
      printf '%s\n' "$destination/$old_group/$old_name" \
        "$destination/$old_name" "$destination/gouv-fr-$old_name"
    fi
  done < "$renames_file"
}

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
  local known relative duplicate
  local -a sources=() targets=() legacy_paths=() distinct_legacy=()
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
      while IFS= read -r legacy; do
        [[ "$legacy" == "$target" ]] && continue
        [[ -f "$legacy/SKILL.md" ]] || continue
        duplicate=false
        for known in "${legacy_paths[@]}"; do
          [[ "$known" == "$legacy" ]] && duplicate=true
        done
        [[ "$duplicate" == true ]] || legacy_paths+=("$legacy")
      done < <(legacy_candidates_for "$destination" "$group" "$(basename "$source")")
      if [[ -e "$target" || -L "$target" ]]; then
        if [[ "$force" != true ]]; then
          echo "Erreur: $target existe déjà (utilisez --force pour le remplacer)" >&2
          return 1
        fi
      fi
    done
  done

  # Les skills retirés n'ont pas de cible, mais ne doivent pas rester actifs.
  # Archiver leurs copies connues comme les renommages, sans toucher aux autres.
  local retired_group retired_name
  while IFS=$'\t' read -r retired_group retired_name; do
    [[ "$retired_group" == \#* || -z "$retired_group" ]] && continue
    for legacy in "$destination/$retired_group/$retired_name" \
      "$destination/$retired_name" "$destination/gouv-fr-$retired_name"; do
      [[ -f "$legacy/SKILL.md" ]] || continue
      duplicate=false
      for known in "${legacy_paths[@]}"; do
        [[ "$known" == "$legacy" ]] && duplicate=true
      done
      [[ "$duplicate" == true ]] || legacy_paths+=("$legacy")
    done
  done < "$retirements_file"

  # Une ancienne copie à plat peut contenir un chemin qui devient un groupe.
  # Archiver son dossier complet une seule fois, sans déplacer ensuite ses enfants.
  for legacy in "${legacy_paths[@]}"; do
    duplicate=false
    for known in "${legacy_paths[@]}"; do
      [[ "$legacy" == "$known/"* ]] && duplicate=true
    done
    [[ "$duplicate" == true ]] || distinct_legacy+=("$legacy")
  done
  legacy_paths=("${distinct_legacy[@]}")

  if (( ${#legacy_paths[@]} )) && [[ "$migrate" != true ]]; then
    echo "Erreur: anciennes copies détectées dans $destination ; relancez avec --migrate (sauvegarde conservée)." >&2
    return 1
  fi

  mkdir -p "$destination"
  if (( ${#legacy_paths[@]} )); then
    backup="$(mktemp -d "${destination}.backup-XXXXXX")"
    printf '%s: sauvegarde de migration dans %s\n' "$current_agent" "$backup"
    # Archiver avant la copie : un ancien skill à plat peut devenir un groupe.
    for legacy in "${legacy_paths[@]}"; do
      relative="${legacy#"$destination/"}"
      mkdir -p "$backup/$(dirname "$relative")"
      mv "$legacy" "$backup/$relative"
      rmdir "$(dirname "$legacy")" 2>/dev/null || true
    done
    # Préserver aussi les destinations déjà présentes qui seront mises à jour.
    for target in "${targets[@]}"; do
      if [[ -e "$target" || -L "$target" ]]; then
        relative="${target#"$destination/"}"
        mkdir -p "$backup/$(dirname "$relative")"
        cp -RP "$target" "$backup/$relative"
      fi
    done
  fi
  local index
  for index in "${!sources[@]}"; do
    target="${targets[$index]}"
    mkdir -p "$(dirname "$target")"
    if [[ -e "$target" || -L "$target" ]]; then
      rm -rf "$target"
    fi
    cp -R "${sources[$index]}" "$target"
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
