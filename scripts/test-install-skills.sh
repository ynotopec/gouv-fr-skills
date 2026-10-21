#!/usr/bin/env bash

set -euo pipefail

script_dir="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
installer="$script_dir/install-skills.sh"
skills_root="$script_dir/../skills/gouv-fr"
expected_count="$(find "$skills_root" -mindepth 2 -maxdepth 2 -type d | wc -l)"
expected_groups="$(find "$skills_root" -mindepth 1 -maxdepth 1 -type d | wc -l)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

HOME="$tmp/home" XDG_CONFIG_HOME="$tmp/config" \
  HERMES_HOME="$tmp/home/.hermes" \
  KILO_HOME="$tmp/home/.kilocode" \
  CLAUDE_HOME="$tmp/home/.claude" \
  "$installer" --agent all

for destination in \
  "$tmp/home/.hermes/skills" \
  "$tmp/config/opencode/skills" \
  "$tmp/home/.kilocode/skills" \
  "$tmp/home/.claude/skills"; do
  actual_count="$(find "$destination" -mindepth 3 -maxdepth 3 -type f -name SKILL.md | wc -l)"
  [[ "$actual_count" -eq "$expected_count" ]] || {
    echo "Échec: $destination contient $actual_count skills au lieu de $expected_count" >&2
    exit 1
  }
  actual_groups="$(find "$destination" -mindepth 1 -maxdepth 1 -type d | wc -l)"
  [[ "$actual_groups" -eq "$expected_groups" ]] || {
    echo "Échec: $destination contient $actual_groups groupes au lieu de $expected_groups" >&2
    exit 1
  }
  # Aucun skill ne doit porter le nom de son groupe parent.
  while read -r skill_md; do
    group="$(basename "$(dirname "$(dirname "$skill_md")")")"
    skill="$(basename "$(dirname "$skill_md")")"
    if [[ "$skill" == "$group" || "$skill" == gouv-fr-$group ]]; then
      echo "Échec: $skill_md porte le nom de son groupe parent ($group)" >&2
      exit 1
    fi
  done < <(find "$destination" -mindepth 3 -maxdepth 3 -type f -name SKILL.md)
done

project="$tmp/project"
mkdir -p "$project"
"$installer" --agent opencode --scope project --project "$project"
test -f "$project/.opencode/skills/code/code-index/SKILL.md"

if "$installer" --agent opencode --scope project --project "$project" >/dev/null 2>&1; then
  echo "Échec: une installation existante aurait dû nécessiter --force" >&2
  exit 1
fi
"$installer" --agent opencode --scope project --project "$project" --force >/dev/null

# L'option --flat installe a plat, sans le dossier de groupe.
flat="$tmp/flat"
mkdir -p "$flat"
HOME="$tmp/home" HERMES_HOME="$flat/hermes" "$installer" --agent hermes --flat >/dev/null
test -f "$flat/hermes/skills/code-index/SKILL.md"
if [[ -d "$flat/hermes/skills/code" ]]; then
  echo "Échec: --flat ne doit pas créer de dossier de groupe" >&2
  exit 1
fi

echo "OK: $expected_count skills dans $expected_groups groupes testés pour Hermes, OpenCode, Kilo Code et Claude Code"
