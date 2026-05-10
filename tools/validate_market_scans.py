#!/usr/bin/env python3
from __future__ import annotations

import re
from datetime import date
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCANS = ROOT / "guidance" / "market-scans"
DATE_PATTERN = re.compile(r"^(\d{4}-\d{2}-\d{2})-[a-z0-9-]+\.md$")
URL_PATTERN = re.compile(r"https?://")
ACCESS_DATE_PATTERN = re.compile(r"accessed \d{4}-\d{2}-\d{2}", re.IGNORECASE)
REQUIRED_META = {
    "type",
    "scan_date",
    "target_role_family",
    "seniority",
    "geography",
    "max_age_days",
    "changes_since_previous",
}
REQUIRED_SECTIONS = [
    "## Sources",
    "## Recurring Skill Clusters",
    "## Required Vs Nice-To-Have Skills",
    "## Seniority And Leadership Signals",
    "## ATS And Resume Implications",
    "## Skills To De-Emphasize",
    "## Changes Since Previous Scan",
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def parse_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing frontmatter")
    end = text.find("\n---", 4)
    if end == -1:
        raise ValueError("unterminated frontmatter")
    meta = yaml.safe_load(text[4:end]) or {}
    if not isinstance(meta, dict):
        raise ValueError("frontmatter is not a mapping")
    return meta, text[end + 4 :]


def as_iso(value: Any) -> str | None:
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return value
    return None


def require_non_empty_list(path: Path, meta: dict[str, Any], key: str, errors: list[str]) -> None:
    value = meta.get(key)
    if not isinstance(value, list) or not value or not all(isinstance(item, str) and item for item in value):
        errors.append(f"{rel(path)}: {key} must be a non-empty list of strings")


def scan_files() -> list[Path]:
    return sorted(path for path in SCANS.glob("*.md") if path.name != "README.md")


def main() -> int:
    errors: list[str] = []
    files = scan_files()
    if not files:
        errors.append("guidance/market-scans: no dated market scans found")

    for path in files:
        match = DATE_PATTERN.match(path.name)
        if not match:
            errors.append(f"{rel(path)}: filename must be YYYY-MM-DD-target-role-slug.md")

        try:
            meta, body = parse_frontmatter(path)
        except ValueError as exc:
            errors.append(f"{rel(path)}: {exc}")
            continue

        missing = sorted(REQUIRED_META - set(meta))
        if missing:
            errors.append(f"{rel(path)}: missing frontmatter keys {missing}")

        if meta.get("type") != "market-scan":
            errors.append(f"{rel(path)}: type must be market-scan")

        scan_date = as_iso(meta.get("scan_date"))
        if not scan_date:
            errors.append(f"{rel(path)}: scan_date must be YYYY-MM-DD")
        elif match and scan_date != match.group(1):
            errors.append(f"{rel(path)}: scan_date must match filename date")

        max_age = meta.get("max_age_days")
        if not isinstance(max_age, int) or max_age <= 0:
            errors.append(f"{rel(path)}: max_age_days must be a positive integer")

        for key in ("target_role_family", "seniority", "geography"):
            require_non_empty_list(path, meta, key, errors)

        if not isinstance(meta.get("changes_since_previous"), str) or not meta.get("changes_since_previous"):
            errors.append(f"{rel(path)}: changes_since_previous must be a non-empty string")

        previous = meta.get("previous_scan")
        if previous:
            previous_path = (path.parent / str(previous)).resolve()
            try:
                previous_path.relative_to(SCANS.resolve())
            except ValueError:
                errors.append(f"{rel(path)}: previous_scan escapes market-scans directory")
            else:
                if not previous_path.exists():
                    errors.append(f"{rel(path)}: previous_scan does not exist: {previous}")

        for heading in REQUIRED_SECTIONS:
            if heading not in body:
                errors.append(f"{rel(path)}: missing section {heading}")

        if not URL_PATTERN.search(body):
            errors.append(f"{rel(path)}: must include source URLs")
        if not ACCESS_DATE_PATTERN.search(body):
            errors.append(f"{rel(path)}: sources must include access dates")

    if errors:
        print("Market scan validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Market scan validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
