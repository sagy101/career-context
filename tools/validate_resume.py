#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CURRENT = ROOT / "resumes/current"
SOURCE = CURRENT / "Jordan_Example_Resume.md"
DOCX = CURRENT / "Jordan_Example_Resume.docx"
PDF = CURRENT / "Jordan_Example_Resume.pdf"
PREVIEW = CURRENT / "preview.png"
VALIDATION_PATH = ROOT / "config/resume-validation.yaml"


def load_validation() -> dict:
    loaded = yaml.safe_load(VALIDATION_PATH.read_text(encoding="utf-8")) or {}
    if not isinstance(loaded, dict):
        raise SystemExit(f"Validation config must be a mapping: {VALIDATION_PATH}")
    return loaded


VALIDATION = load_validation()
EXPECTED_PHRASES = VALIDATION.get("expected_pdf_text", [])
EXPECTED_PUBLIC_LINKS = VALIDATION.get("expected_markdown_links", [])
FORBIDDEN_OUTPUT_PATTERNS = [re.compile(pattern) for pattern in VALIDATION.get("forbidden_output_patterns", [])]
FORBIDDEN_PDF_TEXT = VALIDATION.get("forbidden_pdf_text", [])


def run(command: list[str]) -> str:
    return subprocess.check_output(command, text=True, stderr=subprocess.STDOUT)


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> int:
    for path in (SOURCE, DOCX, PDF, PREVIEW):
        if not path.exists():
            fail(f"Missing resume artifact: {path}")

    source_mtime = SOURCE.stat().st_mtime
    if DOCX.stat().st_mtime + 1 < source_mtime:
        fail("Generated DOCX is older than canonical markdown")
    if PDF.stat().st_mtime + 1 < DOCX.stat().st_mtime:
        fail("Generated PDF is older than generated DOCX")
    if PREVIEW.stat().st_mtime + 1 < PDF.stat().st_mtime:
        fail("Generated preview is older than generated PDF")

    pdfinfo = run(["pdfinfo", str(PDF)])
    if not re.search(r"Pages:\s+1\b", pdfinfo):
        fail("PDF is not one page")
    if not re.search(r"Encrypted:\s+no\b", pdfinfo):
        fail("PDF is encrypted")

    pdf_text = run(["pdftotext", str(PDF), "-"])
    md_text = SOURCE.read_text(encoding="utf-8")
    for phrase in EXPECTED_PHRASES:
        if phrase not in pdf_text:
            fail(f"PDF text missing expected phrase: {phrase}")
    for pattern in FORBIDDEN_OUTPUT_PATTERNS:
        if pattern.search(pdf_text):
            fail(f"Forbidden pattern in PDF text: {pattern.pattern}")
    for text in FORBIDDEN_PDF_TEXT:
        if text in pdf_text:
            fail(f"Forbidden text in PDF extraction: {text}")

    for link in EXPECTED_PUBLIC_LINKS:
        if link not in md_text:
            fail(f"Markdown missing expected public link: {link}")

    print("Resume validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
