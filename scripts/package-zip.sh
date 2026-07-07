#!/usr/bin/env bash
# Build a claude.ai-ready zip: the zip must contain the skill FOLDER at its root.
set -euo pipefail
cd "$(dirname "$0")/.."

rm -rf dist
mkdir -p dist/powerclaw
cp SKILL.md dist/powerclaw/
cp -R references dist/powerclaw/
(cd dist && zip -rq powerclaw.zip powerclaw)
echo "Built dist/powerclaw.zip"
echo "Upload at claude.ai: Settings > Capabilities > enable Skills > upload zip"
