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

# Simuler l'ancien catalogue et des modifications locales, sans toucher au profil réel.
migration="$tmp/migration"
destination="$migration/.opencode/skills"
mkdir -p "$destination/personal-skill"
printf '%s\n' 'skill personnel' > "$destination/personal-skill/SKILL.md"
for source in "$skills_root"/*/*/; do
  [[ -f "$source/SKILL.md" ]] || continue
  cp -R "$source" "$destination/gouv-fr-$(basename "$source")"
done
printf '%s\n' 'modification locale à conserver' > "$destination/gouv-fr-code-quality/local-note.txt"

if "$installer" --agent opencode --scope project --project "$migration" --force >/dev/null 2>&1; then
  echo "Échec: --force seul ne doit pas laisser cohabiter les anciens et nouveaux noms" >&2
  exit 1
fi
test "$(find "$destination" -type f -name SKILL.md | wc -l)" -eq "$((expected_count + 1))"
test ! -d "$destination/code"

"$installer" --agent opencode --scope project --project "$migration" --migrate >/dev/null
test "$(find "$destination" -type f -name SKILL.md | wc -l)" -eq "$((expected_count + 1))"
test -f "$destination/code/code-quality/SKILL.md"
test -f "$destination/personal-skill/SKILL.md"
test ! -e "$destination/gouv-fr-code-quality"
backups=("$destination".backup-*)
test "${#backups[@]}" -eq 1
test "$(find "${backups[0]}" -type f -name SKILL.md | wc -l)" -eq "$expected_count"
test -f "${backups[0]}/gouv-fr-code-quality/local-note.txt"

# Une nouvelle exécution n'accumule ni doublon ni nouvelle sauvegarde inutile.
"$installer" --agent opencode --scope project --project "$migration" --migrate --force >/dev/null
backups=("$destination".backup-*)
test "${#backups[@]}" -eq 1
test "$(find "$destination" -type f -name SKILL.md | wc -l)" -eq "$((expected_count + 1))"

# Un conflit de destination est détecté avant tout déplacement d'une ancienne copie.
conflict="$tmp/conflict"
mkdir -p "$conflict/.opencode/skills/code/code-index" "$conflict/.opencode/skills/gouv-fr-code-index"
printf '%s\n' 'ancien' > "$conflict/.opencode/skills/gouv-fr-code-index/SKILL.md"
printf '%s\n' 'déjà présent' > "$conflict/.opencode/skills/code/code-index/SKILL.md"
if "$installer" --agent opencode --scope project --project "$conflict" --migrate >/dev/null 2>&1; then
  echo "Échec: une destination existante doit rester protégée sans --force" >&2
  exit 1
fi
test -f "$conflict/.opencode/skills/gouv-fr-code-index/SKILL.md"

# La migration conserve aussi les anciennes copies lors d'une installation à plat.
flat_migration="$tmp/flat-migration"
mkdir -p "$flat_migration/.opencode/skills/gouv-fr-code-index"
printf '%s\n' 'ancien' > "$flat_migration/.opencode/skills/gouv-fr-code-index/SKILL.md"
"$installer" --agent opencode --scope project --project "$flat_migration" --flat --migrate >/dev/null
test -f "$flat_migration/.opencode/skills/code-index/SKILL.md"
test ! -d "$flat_migration/.opencode/skills/code"
test ! -e "$flat_migration/.opencode/skills/gouv-fr-code-index"

echo "OK: $expected_count skills dans $expected_groups groupes, quatre agents ; migrations et sauvegardes vérifiées"
