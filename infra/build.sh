#!/usr/bin/env bash
# Build lambda.zip from the repo root:  bash infra/build.sh
# Result: build/lambda.zip with handler.py, risk/, households.json at the zip root.
set -euo pipefail
rm -rf build && mkdir -p build/pkg
cp src/lambda/handler.py build/pkg/
cp -r src/risk build/pkg/risk
find build/pkg -name "__pycache__" -type d -prune -exec rm -rf {} +
cp data/households.json build/pkg/
(cd build/pkg && python3 -m zipfile -c ../lambda.zip .)
echo "built build/lambda.zip"
