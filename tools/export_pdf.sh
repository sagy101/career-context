#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOCX="$ROOT/resumes/current/Jordan_Example_Resume.docx"
OUT_DIR="$ROOT/resumes/current"

test -f "$DOCX"
soffice --headless --convert-to pdf --outdir "$OUT_DIR" "$DOCX" >/tmp/resume_export_pdf.log 2>&1
test -f "$OUT_DIR/Jordan_Example_Resume.pdf"
echo "$OUT_DIR/Jordan_Example_Resume.pdf"
