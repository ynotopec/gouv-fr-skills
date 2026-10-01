#!/usr/bin/env bash

set -euo pipefail

script_dir="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
installer="$script_dir/install-skills.sh"
expected_count="$(find "$script_dir/../skills" -mindepth 1 -maxdepth 1 -type d -name 'gouv-fr-*' | wc -l)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

HOME="$tmp/home" XDG_CONFIG_HOME="$tmp/config" "$installer" --agent all

for destination in \
  "$tmp/home/.hermes/skills" \
  "$tmp/config/opencode/skills" \
  "$tmp/home/.kilocode/skills" \
  "$tmp/home/.claude/skills"; do
  actual_count="$(find "$destination" -mindepth 2 -maxdepth 2 -type f -name SKILL.md | wc -l)"
  [[ "$actual_count" -eq "$expected_count" ]] || {
    echo "Échec: $destination contient $actual_count skills au lieu de $expected_count" >&2
    exit 1
  }
done

project="$tmp/project"
mkdir -p "$project"
"$installer" --agent opencode --scope project --project "$project"
test -f "$project/.opencode/skills/gouv-fr-code-index/SKILL.md"

if "$installer" --agent opencode --scope project --project "$project" >/dev/null 2>&1; then
  echo "Échec: une installation existante aurait dû nécessiter --force" >&2
  exit 1
fi
"$installer" --agent opencode --scope project --project "$project" --force >/dev/null

echo "OK: $expected_count skills testés pour Hermes, OpenCode, Kilo Code et Claude Code"
