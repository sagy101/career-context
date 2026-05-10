#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="${PYTHON:-python3}"

missing=()
for command in soffice pdfinfo pdftotext pdftoppm rg git; do
  if ! command -v "$command" >/dev/null 2>&1; then
    missing+=("$command")
  fi
done

if [[ "${#missing[@]}" -gt 0 ]]; then
  printf 'Missing required system tools: %s\n' "${missing[*]}" >&2
  cat >&2 <<'EOF'

macOS:
  brew install --cask libreoffice
  brew install poppler ripgrep

Ubuntu:
  sudo apt-get update
  sudo apt-get install -y libreoffice poppler-utils ripgrep fonts-crosextra-carlito fonts-liberation
EOF
  exit 1
fi

"$PYTHON" - <<'PY'
import importlib.util
import sys

missing = [name for name in ("docx", "yaml") if importlib.util.find_spec(name) is None]
if missing:
    print(f"Missing required Python packages: {', '.join(missing)}", file=sys.stderr)
    print('Install with: python -m pip install -e ".[dev]"', file=sys.stderr)
    raise SystemExit(1)
PY

echo "Local resume tooling preflight passed"
