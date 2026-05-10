#!/usr/bin/env python3
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

import yaml
from docx import Document

ROOT = Path(__file__).resolve().parents[1]
DOCX = ROOT / "resumes/current/Jordan_Example_Resume.docx"
VALIDATION_PATH = ROOT / "config/resume-validation.yaml"


def load_validation() -> dict:
    loaded = yaml.safe_load(VALIDATION_PATH.read_text(encoding="utf-8")) or {}
    if not isinstance(loaded, dict):
        raise SystemExit(f"Validation config must be a mapping: {VALIDATION_PATH}")
    return loaded


VALIDATION = load_validation()
EXPECTED_LINK_PARTS = VALIDATION.get("expected_docx_link_parts", [])
EXPECTED_TEXT = VALIDATION.get("expected_docx_text", [])


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DOCX
    if not path.exists():
        raise SystemExit(f"Missing DOCX: {path}")

    if not zipfile.is_zipfile(path):
        raise SystemExit(f"Not a valid DOCX zip: {path}")

    doc = Document(path)
    text = "\n".join(p.text for p in doc.paragraphs)
    missing = [phrase for phrase in EXPECTED_TEXT if phrase not in text]
    if missing:
        raise SystemExit(f"DOCX missing expected text: {missing}")

    rels = "\n".join(rel.target_ref for rel in doc.part.rels.values() if rel.is_external)
    missing_links = [part for part in EXPECTED_LINK_PARTS if part not in rels]
    if missing_links:
        raise SystemExit(f"DOCX missing expected links: {missing_links}")

    with zipfile.ZipFile(path) as zf:
        styles = zf.read("word/styles.xml").decode("utf-8", errors="ignore")
        if "Calibri" not in styles:
            raise SystemExit("DOCX styles do not reference Calibri")

    print(f"DOCX inspection passed: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
