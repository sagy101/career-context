#!/usr/bin/env python3
from __future__ import annotations

import re
from datetime import date
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTEXT = ROOT / "context"
REQUIRED = {
    "type",
    "company",
    "title",
    "status",
    "confidentiality",
    "sensitivity",
    "resume_safe",
    "approved_for_resume",
    "claim_confidence",
    "evidence_level",
    "resume_relevance",
    "skills",
    "last_reviewed",
    "last_verified",
}
ALLOWED_TYPES = {"profile", "company", "role", "initiative", "project", "guidance", "resume"}
ALLOWED_STATUS = {"production", "adopted", "implementation", "archived", "draft", "active", "completed"}
ALLOWED_CONFIDENTIALITY = {"public", "private-career-context", "internal-reference-only", "do-not-use"}
ALLOWED_SENSITIVITY = {"public-safe", "private-career-context", "internal-reference-only", "do-not-use"}
ALLOWED_CONFIDENCE = {"confirmed", "user-stated", "source-backed", "estimated", "needs-confirmation"}
ALLOWED_EVIDENCE = {"public-link", "user-confirmed", "local-summary", "internal-source-summary", "none"}
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LOCAL_MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)#:]+(?:\.md)(?:#[^)]+)?)\)")
SAFETY_SCAN_GLOBS = ["README.md", "AGENTS.md", "docs/**/*.md", "guidance/**/*.md", "resumes/**/*.md"]
HIGH_CONFIDENCE_SECRETS = [
    re.compile(r"ghp_[A-Za-z0-9_]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
]
LOCAL_OR_INTERNAL_REFERENCE = re.compile(
    r"(/Users/[^/\s)]+|/home/[^/\s)]+|https?://[^\s)]+(?:\.atlassian\.net|\.corp|\.internal|\.local)\b)",
    re.IGNORECASE,
)


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


def context_files() -> list[Path]:
    return sorted(path for path in CONTEXT.rglob("*.md") if path.name != "log.md" and not path.name.startswith("index"))


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def line_section(line: str, current: str) -> str:
    if line.startswith("## "):
        return line[3:].strip()
    return current


def validate_metadata(path: Path, meta: dict[str, Any], errors: list[str]) -> None:
    if meta.get("type") not in ALLOWED_TYPES:
        errors.append(f"{rel(path)}: invalid type {meta.get('type')!r}")
    if meta.get("status") not in ALLOWED_STATUS:
        errors.append(f"{rel(path)}: invalid status {meta.get('status')!r}")
    if meta.get("confidentiality") not in ALLOWED_CONFIDENTIALITY:
        errors.append(f"{rel(path)}: invalid confidentiality {meta.get('confidentiality')!r}")
    if meta.get("sensitivity") not in ALLOWED_SENSITIVITY:
        errors.append(f"{rel(path)}: invalid sensitivity {meta.get('sensitivity')!r}")
    if meta.get("claim_confidence") not in ALLOWED_CONFIDENCE:
        errors.append(f"{rel(path)}: invalid claim_confidence {meta.get('claim_confidence')!r}")
    if meta.get("evidence_level") not in ALLOWED_EVIDENCE:
        errors.append(f"{rel(path)}: invalid evidence_level {meta.get('evidence_level')!r}")

    for key in ("resume_safe", "approved_for_resume"):
        if not isinstance(meta.get(key), bool):
            errors.append(f"{rel(path)}: {key} must be a boolean")
    for key in ("last_reviewed", "last_verified"):
        value = meta.get(key)
        if isinstance(value, date):
            continue
        if not isinstance(value, str) or not DATE_PATTERN.match(value):
            errors.append(f"{rel(path)}: {key} must be YYYY-MM-DD")


def main() -> int:
    errors: list[str] = []
    for path in context_files():
        try:
            meta, body = parse_frontmatter(path)
        except ValueError as exc:
            errors.append(f"{rel(path)}: {exc}")
            continue

        missing = sorted(REQUIRED - set(meta))
        if missing:
            errors.append(f"{rel(path)}: missing frontmatter keys {missing}")
        validate_metadata(path, meta, errors)

        for key in ("resume_relevance", "skills"):
            if not isinstance(meta.get(key), list) or not meta.get(key):
                errors.append(f"{rel(path)}: {key} must be a non-empty list")
        for key in ("related_roles", "related_projects", "source_paths", "public_links"):
            value = meta.get(key, [])
            if value is not None and not isinstance(value, list):
                errors.append(f"{rel(path)}: {key} must be a list")

        for linked in (meta.get("related_roles") or []) + (meta.get("related_projects") or []):
            linked_path = ROOT / str(linked)
            if not linked_path.exists():
                errors.append(f"{rel(path)}: related path does not exist: {linked}")

        if meta.get("type") in {"project", "initiative", "role"}:
            for heading in ("## Resume Bullet Bank", "## Claims Needing Confirmation", "## Do Not Include"):
                if heading not in body:
                    errors.append(f"{rel(path)}: missing section {heading}")

        section = ""
        for number, line in enumerate(body.splitlines(), start=1):
            section = line_section(line, section)
            for pattern in HIGH_CONFIDENCE_SECRETS:
                if pattern.search(line):
                    errors.append(f"{rel(path)}:{number}: high-confidence secret pattern")
            if LOCAL_OR_INTERNAL_REFERENCE.search(line) and section != "Source Notes":
                errors.append(f"{rel(path)}:{number}: internal URL/path outside Source Notes")
            if line.startswith("```") and meta.get("sensitivity") == "public-safe":
                errors.append(f"{rel(path)}:{number}: code block in public-safe context")

    for path in sorted(CONTEXT.glob("index*.md")):
        text = path.read_text(encoding="utf-8")
        for match in LOCAL_MARKDOWN_LINK.finditer(text):
            target = match.group(1).split("#", 1)[0]
            linked = (path.parent / target).resolve()
            try:
                linked.relative_to(ROOT)
            except ValueError:
                errors.append(f"{rel(path)}: link escapes repo: {target}")
                continue
            if not linked.exists():
                errors.append(f"{rel(path)}: broken markdown link: {target}")

    safety_files: set[Path] = set()
    for pattern in SAFETY_SCAN_GLOBS:
        safety_files.update(ROOT.glob(pattern))
    for path in sorted(safety_files):
        if not path.is_file():
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), start=1):
            for pattern in HIGH_CONFIDENCE_SECRETS:
                if pattern.search(line):
                    errors.append(f"{rel(path)}:{number}: high-confidence secret pattern")

    if errors:
        print("Context validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Context validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
