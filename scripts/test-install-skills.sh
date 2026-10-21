#!/usr/bin/env bash

set -euo pipefail

script_dir="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
installer="$script_dir/install-skills.sh"
skills_root="$script_dir/../skills/fr-gov"
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
test -f "$project/.opencode/skills/code/review-code/SKILL.md"

if "$installer" --agent opencode --scope project --project "$project" >/dev/null 2>&1; then
  echo "Échec: une installation existante aurait dû nécessiter --force" >&2
  exit 1
fi
"$installer" --agent opencode --scope project --project "$project" --force >/dev/null

# L'option --flat installe a plat, sans le dossier de groupe.
flat="$tmp/flat"
mkdir -p "$flat"
HOME="$tmp/home" HERMES_HOME="$flat/hermes" "$installer" --agent hermes --flat >/dev/null
test -f "$flat/hermes/skills/review-code/SKILL.md"
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
printf '%s\n' 'modification locale à conserver' > "$destination/gouv-fr-review-code/local-note.txt"

if "$installer" --agent opencode --scope project --project "$migration" --force >/dev/null 2>&1; then
  echo "Échec: --force seul ne doit pas laisser cohabiter les anciens et nouveaux noms" >&2
  exit 1
fi
test "$(find "$destination" -type f -name SKILL.md | wc -l)" -eq "$((expected_count + 1))"
test ! -d "$destination/code"

"$installer" --agent opencode --scope project --project "$migration" --migrate >/dev/null
test "$(find "$destination" -type f -name SKILL.md | wc -l)" -eq "$((expected_count + 1))"
test -f "$destination/code/review-code/SKILL.md"
test -f "$destination/personal-skill/SKILL.md"
test ! -e "$destination/gouv-fr-review-code"
backups=("$destination".backup-*)
test "${#backups[@]}" -eq 1
test "$(find "${backups[0]}" -type f -name SKILL.md | wc -l)" -eq "$expected_count"
test -f "${backups[0]}/gouv-fr-review-code/local-note.txt"

# Une nouvelle exécution n'accumule ni doublon ni nouvelle sauvegarde inutile.
"$installer" --agent opencode --scope project --project "$migration" --migrate --force >/dev/null
backups=("$destination".backup-*)
test "${#backups[@]}" -eq 1
test "$(find "$destination" -type f -name SKILL.md | wc -l)" -eq "$((expected_count + 1))"

# Un conflit de destination est détecté avant tout déplacement d'une ancienne copie.
conflict="$tmp/conflict"
mkdir -p "$conflict/.opencode/skills/code/review-code" "$conflict/.opencode/skills/gouv-fr-code-quality"
printf '%s\n' 'ancien' > "$conflict/.opencode/skills/gouv-fr-code-quality/SKILL.md"
printf '%s\n' 'déjà présent' > "$conflict/.opencode/skills/code/review-code/SKILL.md"
if "$installer" --agent opencode --scope project --project "$conflict" --migrate >/dev/null 2>&1; then
  echo "Échec: une destination existante doit rester protégée sans --force" >&2
  exit 1
fi
test -f "$conflict/.opencode/skills/gouv-fr-code-quality/SKILL.md"

# La migration conserve aussi les anciennes copies lors d'une installation à plat.
flat_migration="$tmp/flat-migration"
mkdir -p "$flat_migration/.opencode/skills/gouv-fr-code-quality"
printf '%s\n' 'ancien' > "$flat_migration/.opencode/skills/gouv-fr-code-quality/SKILL.md"
"$installer" --agent opencode --scope project --project "$flat_migration" --flat --migrate >/dev/null
test -f "$flat_migration/.opencode/skills/review-code/SKILL.md"
test ! -d "$flat_migration/.opencode/skills/code"
test ! -e "$flat_migration/.opencode/skills/gouv-fr-code-quality"

# Vérifier les trois générations réellement distribuées : anciens groupes,
# anciens noms à plat, et noms à plat préfixés gouv-fr-.
for layout in grouped flat prefixed; do
  migration="$tmp/catalog-$layout"
  destination="$migration/.opencode/skills"
  mkdir -p "$destination/personal-skill"
  printf '%s\n' 'personnel' > "$destination/personal-skill/SKILL.md"
  rows=0
  probe_rel=""
  while IFS=$'\t' read -r old_group old_name new_group new_name; do
    [[ "$old_group" == \#* || -z "$old_group" ]] && continue
    rows=$((rows + 1))
    source="$skills_root/$new_group/$new_name"
    test -f "$source/SKILL.md"
    case "$layout" in
      grouped) legacy="$destination/$old_group/$old_name" ;;
      flat) legacy="$destination/$old_name" ;;
      prefixed) legacy="$destination/gouv-fr-$old_name" ;;
    esac
    mkdir -p "$(dirname "$legacy")"
    mkdir -p "$legacy"
    cp -R "$source/." "$legacy/"
    if [[ "$new_group/$new_name" == "code/review-code" && -z "$probe_rel" ]]; then
      probe_rel="${legacy#"$destination"/}"
    fi
  done < "$script_dir/skill-renames.tsv"
  test "$rows" -ge "$expected_count"
  mapped_count="$(awk -F '\t' '!/^#/ && NF == 4 {print $3 "/" $4}' "$script_dir/skill-renames.tsv" | sort -u | wc -l)"
  test "$mapped_count" -eq "$expected_count"
  test -n "$probe_rel"
  printf '%s\n' 'modification utilisateur' >> "$destination/$probe_rel/SKILL.md"
  if "$installer" --agent opencode --scope project --project "$migration" --force >/dev/null 2>&1; then
    echo "Échec: le catalogue $layout doit exiger --migrate" >&2
    exit 1
  fi
  "$installer" --agent opencode --scope project --project "$migration" --migrate --force >/dev/null
  test "$(find "$destination" -type f -name SKILL.md | wc -l)" -eq "$((expected_count + 1))"
  test -f "$destination/code/fr-gov-scaffold-backend-api/SKILL.md"
  test -f "$destination/security/fr-gov-secure-coding-rules/SKILL.md"
  test -f "$destination/devops/fr-gov-set-up-cloud-pi-native-cicd/SKILL.md"
  test -f "$destination/devops/fr-gov-set-up-github-actions-ci/SKILL.md"
  test -f "$destination/devops/fr-gov-containerize-app-for-k8s/SKILL.md"
  test -f "$destination/code/detect-stale-service-names/SKILL.md"
  test -f "$destination/security/audit-llm-tool-identity/SKILL.md"
  test -f "$destination/devops/smoke-test-api/SKILL.md"
  test -f "$destination/design-system/fr-gov-set-up-design-system/SKILL.md"
  test ! -e "$destination/security/audit-openwebui"
  test ! -e "$destination/devops/smoke-test"
  test ! -e "$destination/devops/verification-renommage-services"
  test -f "$destination/personal-skill/SKILL.md"
  test ! -f "$destination/security/SKILL.md"
  test ! -d "$destination/anssi"
  test ! -d "$destination/dso"
  backups=("$destination".backup-*)
  test "${#backups[@]}" -eq 1
  grep -q 'modification utilisateur' "${backups[0]}/$probe_rel/SKILL.md"
  if grep -q 'modification utilisateur' "$destination/code/review-code/SKILL.md"; then
    echo "Échec: la destination doit contenir la version courante, l'ancienne restant sauvegardée" >&2
    exit 1
  fi
  "$installer" --agent opencode --scope project --project "$migration" --migrate --force >/dev/null
  backups=("$destination".backup-*)
  test "${#backups[@]}" -eq 1
done

echo "OK: $expected_count skills dans $expected_groups groupes, quatre agents ; migrations historiques et sauvegardes vérifiées"
