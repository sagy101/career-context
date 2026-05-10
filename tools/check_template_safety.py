#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
LOCAL_PATTERN_CONFIG = ROOT / "config/local-forbidden-patterns.yaml"

SKIP_DIRS = {
    ".cache",
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tmp",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "htmlcov",
    "node_modules",
    "site",
}
SKIP_FILES = {
    ".DS_Store",
    ".coverage",
    "config/local-forbidden-patterns.yaml",
}
TEXT_SUFFIXES = {
    ".cfg",
    ".css",
    ".csv",
    ".editorconfig",
    ".env",
    ".example",
    ".gitignore",
    ".html",
    ".ini",
    ".js",
    ".json",
    ".jsx",
    ".lock",
    ".md",
    ".py",
    ".sh",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}


@dataclass(frozen=True)
class SafetyPattern:
    label: str
    regex: re.Pattern[str]


GENERIC_PATTERNS = [
    SafetyPattern("local user path", re.compile(r"(?<![\w.-])/Users/[A-Za-z0-9._-]+(?:/|$)")),
    SafetyPattern("local user path", re.compile(r"(?<![\w.-])/home/[A-Za-z0-9._-]+(?:/|$)")),
    SafetyPattern("local user path", re.compile(r"[A-Za-z]:\\Users\\[A-Za-z0-9._-]+(?:\\|$)")),
    SafetyPattern(
        "internal URL", re.compile(r"https?://[^\s)]+(?:\.atlassian\.net|\.corp|\.internal|\.local)\b", re.I)
    ),
    SafetyPattern("GitHub token", re.compile(r"ghp_[A-Za-z0-9_]{20,}")),
    SafetyPattern("GitHub token", re.compile(r"github_pat_[A-Za-z0-9_]{20,}")),
    SafetyPattern("GitLab token", re.compile(r"glpat-[A-Za-z0-9_-]{20,}")),
    SafetyPattern("Slack token", re.compile(r"xox[baprs]-[A-Za-z0-9-]{20,}")),
    SafetyPattern("AWS access key", re.compile(r"AKIA[0-9A-Z]{16}")),
    SafetyPattern("private key", re.compile(r"-----BEGIN [A-Z0-9 ]{0,40}PRIVATE KEY-----")),
]


def rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def should_skip(root: Path, path: Path) -> bool:
    relative = rel(root, path)
    if relative in SKIP_FILES:
        return True
    return any(part in SKIP_DIRS for part in path.relative_to(root).parts)


def looks_like_text(path: Path) -> bool:
    return path.suffix in TEXT_SUFFIXES or path.name in {".gitignore", ".pre-commit-config.yaml"}


def iter_text_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if not path.is_file() or should_skip(root, path) or not looks_like_text(path):
            continue
        yield path


def load_local_patterns(root: Path) -> list[SafetyPattern]:
    config_path = root / LOCAL_PATTERN_CONFIG.relative_to(ROOT)
    if not config_path.exists():
        return []
    loaded = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    if not isinstance(loaded, dict):
        raise SystemExit(f"Local template safety config must be a mapping: {config_path}")
    patterns = loaded.get("patterns", [])
    if not isinstance(patterns, list):
        raise SystemExit(f"Local template safety patterns must be a list: {config_path}")
    return [SafetyPattern("local forbidden pattern", re.compile(str(pattern), re.I)) for pattern in patterns]


def scan_file(root: Path, path: Path, patterns: list[SafetyPattern]) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8", errors="ignore")
    for number, line in enumerate(text.splitlines(), start=1):
        for pattern in patterns:
            if pattern.regex.search(line):
                errors.append(f"{rel(root, path)}:{number}: {pattern.label}")
    return errors


def scan_paths(root: Path = ROOT) -> list[str]:
    root = root.resolve()
    patterns = [*GENERIC_PATTERNS, *load_local_patterns(root)]
    errors: list[str] = []
    for path in iter_text_files(root):
        errors.extend(scan_file(root, path, patterns))
    return errors


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check resume template files for generic safety issues.")
    parser.add_argument("root", nargs="?", default=str(ROOT), help="Repository root to scan.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    errors = scan_paths(Path(args.root))
    if errors:
        print("Template safety check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Template safety check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
