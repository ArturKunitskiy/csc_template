#!/usr/bin/env bash
# Оновити форк з репозиторію викладача, не перезаписуючи student/ (merge=ours у .gitattributes).
set -euo pipefail

UPSTREAM_REMOTE="${UPSTREAM_REMOTE:-upstream}"
UPSTREAM_REPO="${UPSTREAM_REPO:-}"
BRANCH="${BRANCH:-}"

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "Запустіть скрипт у корені git-репозиторію."
  exit 1
fi

# Потрібно для .gitattributes (student/** merge=ours)
git config merge.ours.driver true

if ! git remote get-url "$UPSTREAM_REMOTE" >/dev/null 2>&1; then
  if [[ -z "$UPSTREAM_REPO" ]]; then
    echo "Додайте remote: git remote add upstream https://github.com/ВИКЛАДАЧ/csc_template.git"
    echo "Або: UPSTREAM_REPO=<url> bash scripts/sync_from_template.sh"
    exit 1
  fi
  git remote add "$UPSTREAM_REMOTE" "$UPSTREAM_REPO"
fi

git fetch "$UPSTREAM_REMOTE"

if [[ -z "$BRANCH" ]]; then
  if git rev-parse --verify "$UPSTREAM_REMOTE/main" >/dev/null 2>&1; then
    BRANCH=main
  else
    BRANCH=master
  fi
fi

echo "==> Merge $UPSTREAM_REMOTE/$BRANCH (student/** залишиться за вами)"
git merge "$UPSTREAM_REMOTE/$BRANCH" -m "Sync template from $UPSTREAM_REMOTE/$BRANCH"

echo ""
echo "Готово. Перевірте: git status"
echo "Далі: git push origin $(git branch --show-current)"
