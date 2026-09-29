# 🎯 Workflow — Toujours sync avant gros changement

## Règle d'or

> **Avant tout gros changement : `bash .github/workflows/save-workflow.sh "<motif>"`**

Ce script crée une branche de backup (`backup/AAAA-MM-DD-HHMMSS`) qui permet de revenir en arrière.

## Workflow type

```bash
# 1. Sauvegarde avant changement
bash .github/workflows/save-workflow.sh "ajout d'un nouveau skill"

# 2. Travailler sur une branche dédiée
git checkout -b feature/mon-changement

# 3. Changer, modifier, tester...

# 4. Commiter
git add -A
git commit -m "feat: mon changement"

# 5. Push et PR
git push origin feature/mon-changement
# Créer la PR sur GitHub
```

## Restaurer un backup

```bash
# Voir les backups
git branch | grep backup/

# Restaurer un backup spécifique
git checkout backup/20260929-170135

# Ou créer une nouvelle branche à partir d'un backup
git checkout -b restore-20260929 backup/20260929-170135
```

## Supprimer un backup

```bash
git branch -D backup/20260929-170135
```

## Avant de push

```bash
git push origin main          # Pusher main
git push origin backup/*      # Pusher les backups (optionnel)
```

## Commandes utiles

| Commande | Usage |
|----------|-------|
| `bash .github/workflows/save-workflow.sh "motif"` | Créer un backup avant changement |
| `git branch \| grep backup` | Voir les backups existants |
| `git checkout backup/...` | Restaurer un backup |
| `git branch -D backup/...` | Supprimer un backup |
| `git status --short` | Vérifier les modifications |
| `git log --oneline -5` | Voir les 5 derniers commits |
