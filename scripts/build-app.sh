#!/bin/bash
# Build one app: name, accent, dir, prompt
NAME="$1"
ACCENT="$2"
DIR="$3"
PROMPT_BRIEF="$4"

APP_DIR="/Users/nebulalumino/.openclaw/workspace/$DIR"

if [ -d "$APP_DIR" ]; then
  echo "SKIP $DIR (exists)"
  return 0 2>/dev/null || exit 0
fi

echo "BUILDING $DIR..."

cd /Users/nebulalumino/.openclaw/workspace

npx create-next-app@latest "$DIR" \
  --typescript --tailwind --eslint --app --src-dir \
  --import-alias "@/*" --no-git --yes 2>/dev/null | tail -3

if [ ! -d "$APP_DIR/src/app" ]; then
  echo "FAILED to create $DIR"
  return 1 2>/dev/null || exit 1
fi

echo "Done creating $DIR, now customizing..."
