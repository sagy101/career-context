#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PDF="${1:-$ROOT/resumes/current/Jordan_Example_Resume.pdf}"
TEXT="$(mktemp)"
trap 'rm -f "$TEXT"' EXIT
PYTHON="${PYTHON:-python3}"

test -f "$PDF"
INFO="$(pdfinfo "$PDF")"
if ! printf '%s\n' "$INFO" | rg "Pages:\\s+1" >/dev/null; then
  printf '%s\n' "$INFO" >&2
  echo "PDF is not one page" >&2
  exit 1
fi
if ! printf '%s\n' "$INFO" | rg "Encrypted:\\s+no" >/dev/null; then
  printf '%s\n' "$INFO" >&2
  echo "PDF is encrypted" >&2
  exit 1
fi
pdftotext "$PDF" "$TEXT"
"$PYTHON" - "$ROOT/config/resume-validation.yaml" "$TEXT" <<'PY'
import re
import sys

import yaml

config_path, text_path = sys.argv[1:]
config = yaml.safe_load(open(config_path, encoding="utf-8")) or {}
text = open(text_path, encoding="utf-8", errors="ignore").read()
for pattern in config.get("forbidden_output_patterns", []):
    if re.search(pattern, text):
        raise SystemExit(f"Forbidden pattern in PDF extraction: {pattern}")
for value in config.get("forbidden_pdf_text", []):
    if value in text:
        raise SystemExit(f"Forbidden text in PDF extraction: {value}")
PY
echo "PDF inspection passed: $PDF"
