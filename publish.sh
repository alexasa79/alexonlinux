#!/usr/bin/env bash
set -euo pipefail

HUGO=${HUGO:-hugo}
REMOTE=${REMOTE:-origin}
PUBLISH_BRANCH=${PUBLISH_BRANCH:-pages}
SOURCE_BRANCH=${SOURCE_BRANCH:-main}
SOURCE_ROOT=$(git rev-parse --show-toplevel)
PUBLISH_DIR=${PUBLISH_DIR:-"$SOURCE_ROOT/../pages"}

cd "$SOURCE_ROOT"

rm -rf public
"$HUGO" -D

if git ls-remote --exit-code --heads "$REMOTE" "$PUBLISH_BRANCH" >/dev/null 2>&1; then
    git fetch "$REMOTE" "$PUBLISH_BRANCH:refs/remotes/$REMOTE/$PUBLISH_BRANCH"
fi

if [[ ! -d "$PUBLISH_DIR/.git" ]]; then
    if git show-ref --verify --quiet "refs/heads/$PUBLISH_BRANCH"; then
        git worktree add "$PUBLISH_DIR" "$PUBLISH_BRANCH"
    elif git show-ref --verify --quiet "refs/remotes/$REMOTE/$PUBLISH_BRANCH"; then
        git worktree add -B "$PUBLISH_BRANCH" "$PUBLISH_DIR" "$REMOTE/$PUBLISH_BRANCH"
    else
        git worktree add -b "$PUBLISH_BRANCH" "$PUBLISH_DIR" "$SOURCE_BRANCH"
        git -C "$PUBLISH_DIR" rm -rf .
    fi
fi

current_branch=$(git -C "$PUBLISH_DIR" branch --show-current)
if [[ "$current_branch" != "$PUBLISH_BRANCH" ]]; then
    echo "Publish worktree is on '$current_branch', expected '$PUBLISH_BRANCH'." >&2
    exit 1
fi

rsync -a --delete --exclude .git public/ "$PUBLISH_DIR/"
git -C "$PUBLISH_DIR" add -A
if git -C "$PUBLISH_DIR" diff --cached --quiet; then
    echo "No publish changes."
else
    git -C "$PUBLISH_DIR" commit -m "publish"
fi

git -C "$PUBLISH_DIR" push "$REMOTE" "HEAD:$PUBLISH_BRANCH"
