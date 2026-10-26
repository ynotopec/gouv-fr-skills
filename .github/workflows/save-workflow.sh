#!/usr/bin/env bash
# Snapshot sans modifier le working tree, l'index ni les stashes existants.
set -euo pipefail

BACKUP_MSG="${1:?Usage: save-workflow.sh <motif>}"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)-$$
BACKUP_BRANCH="backup/$TIMESTAMP"
ROOT=$(git rev-parse --show-toplevel)
cd "$ROOT"
HEAD_SHA=$(git rev-parse --verify HEAD)

# Un index temporaire inclut aussi les fichiers non suivis, hors gitignore.
# Ne jamais stasher/pop, ni modifier l'index de l'utilisateur.
TASK_INDEX=$(mktemp)
rm -f "$TASK_INDEX"
trap 'rm -f "$TASK_INDEX" "$TASK_INDEX.lock"' EXIT
GIT_INDEX_FILE="$TASK_INDEX" git read-tree "$HEAD_SHA"
GIT_INDEX_FILE="$TASK_INDEX" git add -A -- .
TREE=$(GIT_INDEX_FILE="$TASK_INDEX" git write-tree)
if [[ "$TREE" == "$(git rev-parse "$HEAD_SHA^{tree}")" ]]; then
    SNAPSHOT="$HEAD_SHA"
else
    SNAPSHOT=$(printf '%s\n' "backup: $BACKUP_MSG [$TIMESTAMP]" | git commit-tree "$TREE" -p "$HEAD_SHA")
fi
git branch "$BACKUP_BRANCH" "$SNAPSHOT"
printf 'Backup créé : %s (%s)\n' "$BACKUP_BRANCH" "$SNAPSHOT"
printf 'Working tree, index et stashes conservés.\n'
