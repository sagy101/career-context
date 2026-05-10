#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PDF="$ROOT/resumes/current/Jordan_Example_Resume.pdf"
TMP_DIR="$ROOT/.tmp/rendered"
OUT="$ROOT/resumes/current/preview.png"

test -f "$PDF"
rm -rf "$TMP_DIR"
mkdir -p "$TMP_DIR"
pdftoppm -png -singlefile "$PDF" "$TMP_DIR/preview"
mv "$TMP_DIR/preview.png" "$OUT"
rmdir "$TMP_DIR"
rmdir "$ROOT/.tmp" 2>/dev/null || true
echo "$OUT"
