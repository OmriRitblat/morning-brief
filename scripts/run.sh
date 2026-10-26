#!/usr/bin/env bash
# Build, publish and send one issue. Usage: bash scripts/run.sh YYYY-MM-DD
set -euo pipefail
DATE="${1:?usage: run.sh YYYY-MM-DD}"
cd "$(dirname "$0")/.."

pip install -q -r requirements.txt 2>/dev/null || pip install -q --break-system-packages -r requirements.txt

python3 scripts/build.py "$DATE"
python3 scripts/podcast.py "$DATE" || echo "Podcast failed; sending the written issue only."

git add docs
git commit -q -m "Issue $DATE" || echo "Nothing new to commit"
git push -q origin HEAD:main

sleep 75   # let GitHub Pages deploy before the link goes out
python3 scripts/send_telegram.py "$DATE"
