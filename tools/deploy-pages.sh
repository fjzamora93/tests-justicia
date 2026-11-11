#!/usr/bin/env bash
# Compila y publica la app en GitHub Pages (rama gh-pages).
# Uso: npm run deploy
set -euo pipefail
cd "$(dirname "$0")/.."
REMOTE=$(git remote get-url origin)
OUT=dist/angular-aplicacion-tests/browser
npx ng build --configuration production,github-pages
cp "$OUT/index.html" "$OUT/404.html"   # rutas SPA
touch "$OUT/.nojekyll"
cd "$OUT"
rm -rf .git
git init -q -b gh-pages
git add -A
git commit -q -m "Deploy $(date -Iseconds)"
git push -f "$REMOTE" gh-pages
rm -rf .git
echo "Publicado en https://fjzamora93.github.io/tests-justicia/"
