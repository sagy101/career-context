#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
import zipfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
VALIDATION_PATH = ROOT / "config/resume-validation.yaml"
DOCX_FORBIDDEN_PARTS = ("docProps/custom.xml",)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def tracked_resume_artifacts() -> list[Path]:
    try:
        output = subprocess.check_output(["git", "ls-files", "resumes"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL)
        return [ROOT / line for line in output.splitlines() if line.endswith((".docx", ".pdf", ".png"))]
    except (subprocess.CalledProcessError, FileNotFoundError):
        return sorted(path for path in (ROOT / "resumes").rglob("*") if path.suffix in {".docx", ".pdf", ".png"})


def load_patterns() -> list[re.Pattern[str]]:
    loaded = yaml.safe_load(VALIDATION_PATH.read_text(encoding="utf-8")) or {}
    raw_patterns = loaded.get("forbidden_docx_patterns", [])
    return [re.compile(pattern, re.IGNORECASE) for pattern in raw_patterns]


def check_docx(path: Path, patterns: list[re.Pattern[str]], errors: list[str]) -> None:
    if not zipfile.is_zipfile(path):
        errors.append(f"{rel(path)} is not a valid DOCX zip")
        return
    with zipfile.ZipFile(path) as zf:
        names = zf.namelist()
        for forbidden in DOCX_FORBIDDEN_PARTS:
            if forbidden.endswith("/"):
                if any(name.startswith(forbidden) for name in names):
                    errors.append(f"{rel(path)} contains forbidden DOCX part prefix: {forbidden}")
            elif forbidden in names:
                errors.append(f"{rel(path)} contains forbidden DOCX part: {forbidden}")

        for name in names:
            if not name.endswith((".xml", ".rels")):
                continue
            text = zf.read(name).decode("utf-8", errors="ignore")
            for pattern in patterns:
                if pattern.search(text):
                    errors.append(f"{rel(path)}:{name}: forbidden pattern {pattern.pattern}")


def main() -> int:
    errors: list[str] = []
    patterns = load_patterns()
    for path in tracked_resume_artifacts():
        if path.suffix == ".docx":
            check_docx(path, patterns, errors)
    if errors:
        print("Artifact safety check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Artifact safety check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
