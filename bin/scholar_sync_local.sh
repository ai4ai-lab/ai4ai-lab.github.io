#!/usr/bin/env bash
# Weekly publication update, run on your own computer (Google Scholar blocks
# GitHub's servers but not ordinary connections). Pulls the repo, adds new
# Scholar papers to _bibliography/papers.bib, and pushes, which redeploys the site.
set -euo pipefail
cd "$(dirname "$0")/.."

git pull --quiet --rebase
python3 -m pip install --quiet --user requests beautifulsoup4 2>/dev/null \
  || python3 -m pip install --quiet --user --break-system-packages requests beautifulsoup4
python3 bin/scholar_sync.py

git add _bibliography/papers.bib _bibliography/.scholar_seen.json
if git diff --cached --quiet; then
  echo "$(date '+%F %T') No new publications."
else
  git commit --quiet -m "Sync publications from Google Scholar"
  git push --quiet
  echo "$(date '+%F %T') New publications pushed; the site will redeploy."
fi
