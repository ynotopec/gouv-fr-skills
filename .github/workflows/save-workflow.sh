#!/bin/bash
# Script de sauvegarde avant gros changements
# Usage: bash .github/workflows/save-workflow.sh "message de sauvegarde"

set -euo pipefail

BRANCH=$(git branch --show-current)
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BACKUP_BRANCH="backup/$TIMESTAMP"
BACKUP_MSG="$1"

echo "=== Sauvegarde avant changement ==="
echo "Branche: $BRANCH"
echo "Message: $BACKUP_MSG"

# 1. Stash les modifications non commit
if [[ -n "$(git status --porcelain)" ]]; then
    echo "⚠️ Modifications non commit détectées, sauvegarde en stash..."
    git stash push -m "auto-backup-$TIMESTAMP"
fi

# 2. Commit tout ce qui est prêt
git add -A
git diff --cached --quiet || {
    echo "📦 Commit: $BACKUP_MSG"
    git commit -m "backup: $BACKUP_MSG [$TIMESTAMP]"
}

# 3. Créer une branche de backup
git branch "$BACKUP_BRANCH"

# 4. Retourner à la branche originale
if [[ -n "$(git stash list 2>/dev/null)" ]]; then
    git stash pop
    echo "📥 Stash restauré"
fi

echo ""
echo "=== Backup créé ==="
echo "  Branche de backup: $BACKUP_BRANCH"
echo "  Commit: $(git rev-parse HEAD)"
echo "  Date: $(date -d @$(git log -1 --format=%ct) '+%Y-%m-%d %H:%M')"
echo ""
echo "Pour restaurer: git checkout $BACKUP_BRANCH"
echo "Pour supprimer: git branch -D $BACKUP_BRANCH"
