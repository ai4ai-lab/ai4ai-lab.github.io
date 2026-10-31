#!/usr/bin/env bash
# Weekly publication update, run on your own computer (Google Scholar blocks
# GitHub's servers but not ordinary connections). Pulls the repo, adds new
# Scholar papers to _bibliography/papers.bib, makes a thumbnail from Figure 1
# of each new paper, and pushes, which redeploys the site.
set -euo pipefail
cd "$(dirname "$0")/.."

git pull --quiet --rebase
PKGS="requests beautifulsoup4 pymupdf pillow"
python3 -m pip install --quiet --user $PKGS 2>/dev/null \
  || python3 -m pip install --quiet --user --break-system-packages $PKGS
python3 bin/scholar_sync.py
python3 bin/make_thumbnails.py || echo "Thumbnails step failed; publications are still synced."
[ -f _bibliography/.thumbnail_skipped.json ] || echo "[]" > _bibliography/.thumbnail_skipped.json

git add _bibliography/papers.bib _bibliography/.scholar_seen.json \
  _bibliography/.thumbnail_skipped.json assets/img/publication_preview
if git diff --cached --quiet; then
  echo "$(date '+%F %T') No new publications."
else
  git commit --quiet -m "Sync publications from Google Scholar"
  git push --quiet
  echo "$(date '+%F %T') New publications pushed; the site will redeploy."
fi
