#!/usr/bin/env python3
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LIMIT = 500 * 1024
RESUME_LIMIT = 8 * 1024 * 1024
ALLOWED_PREFIXES = ("resumes/current/", "resumes/archive/")
SKIP_DIRS = {".git", ".mypy_cache", ".pytest_cache", ".ruff_cache", ".tmp", ".venv", "__pycache__", "build", "dist"}


def tracked_or_present_files() -> list[Path]:
    try:
        output = subprocess.check_output(
            ["git", "ls-files", "--others", "--cached", "--exclude-standard"],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        )
        return [ROOT / line for line in output.splitlines() if line]
    except (subprocess.CalledProcessError, FileNotFoundError):
        return [
            path
            for path in ROOT.rglob("*")
            if path.is_file() and not any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts)
        ]


def main() -> int:
    errors: list[str] = []
    for path in tracked_or_present_files():
        if not path.exists() or not path.is_file():
            continue
        rel = path.relative_to(ROOT).as_posix()
        size = path.stat().st_size
        limit = RESUME_LIMIT if rel.startswith(ALLOWED_PREFIXES) else DEFAULT_LIMIT
        if size > limit:
            errors.append(f"{rel} is {size} bytes, limit is {limit}")
    if errors:
        print("Unexpected large files:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Large-file check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
