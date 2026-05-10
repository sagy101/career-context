#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="${PYTHON:-python3}"

"$ROOT/tools/doctor.sh"
"$PYTHON" "$ROOT/tools/check_template_safety.py"
"$PYTHON" "$ROOT/tools/validate_context.py"
"$PYTHON" "$ROOT/tools/build_context_indexes.py" --check
"$PYTHON" "$ROOT/tools/build_resume_docx.py"
"$ROOT/tools/export_pdf.sh"
"$ROOT/tools/render_resume.sh"
"$PYTHON" "$ROOT/tools/inspect_docx.py"
"$ROOT/tools/inspect_pdf.sh"
"$PYTHON" "$ROOT/tools/validate_resume.py"
"$PYTHON" "$ROOT/tools/check_large_files.py"
"$PYTHON" "$ROOT/tools/check_artifact_safety.py"
"$PYTHON" "$ROOT/tools/validate_review_prompts.py"
"$PYTHON" "$ROOT/tools/validate_market_scans.py"
echo "All resume checks passed"
