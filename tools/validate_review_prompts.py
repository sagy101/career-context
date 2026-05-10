#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEWS = ROOT / "reviews"
PROMPTS = REVIEWS / "prompts"
README = REVIEWS / "README.md"
REQUIRED_HEADINGS = ["## Role", "## Inputs", "## Checklist", "## Output Format", "## Constraints"]
REQUIRED_SEVERITIES = ["Blocking", "Important", "Minor", "Nit"]
EXPECTED_PROMPTS = {
    "ats-and-market-fit-review.md",
    "confidentiality-and-public-safety-review.md",
    "evidence-and-claim-integrity-review.md",
    "internal-jargon-review.md",
    "leadership-and-seniority-review.md",
    "readability-review.md",
    "recruiter-fit-review.md",
    "render-and-format-review.md",
    "structure-and-scannability-review.md",
    "technical-credibility-review.md",
}
FORBIDDEN_PHRASES = [
    "show your chain-of-thought",
    "show chain-of-thought",
    "reveal your reasoning",
    "include hidden reasoning",
    "think step by step",
    "think through step by step",
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def prompt_files() -> list[Path]:
    return sorted(path for path in PROMPTS.glob("*.md") if path.name != "_shared.md")


def main() -> int:
    errors: list[str] = []
    if not README.exists():
        errors.append("reviews/README.md is missing")
        readme = ""
    else:
        readme = README.read_text(encoding="utf-8")

    if not (PROMPTS / "_shared.md").exists():
        errors.append("reviews/prompts/_shared.md is missing")
        shared = ""
    else:
        shared = (PROMPTS / "_shared.md").read_text(encoding="utf-8")

    files = prompt_files()
    if not files:
        errors.append("no review prompt files found")
    file_names = {path.name for path in files}
    if file_names != EXPECTED_PROMPTS:
        missing = sorted(EXPECTED_PROMPTS - file_names)
        extra = sorted(file_names - EXPECTED_PROMPTS)
        if missing:
            errors.append(f"reviews/prompts: missing expected prompts {missing}")
        if extra:
            errors.append(f"reviews/prompts: unexpected prompt files {extra}")

    for section in ("## Severity Scale", "## Output Format", "## Constraints", "## Trusted Source Guidance"):
        if section not in shared:
            errors.append(f"reviews/prompts/_shared.md: missing section {section}")
    for phrase in ("Do not invent", "Cite trusted sources", "Pass/Fail"):
        if phrase.lower() not in shared.lower():
            errors.append(f"reviews/prompts/_shared.md: missing shared concept {phrase}")
    sources = REVIEWS / "sources.md"
    if not sources.exists():
        errors.append("reviews/sources.md is missing")
        source_text = ""
    else:
        source_text = sources.read_text(encoding="utf-8")
        if not re.search(r"https?://", source_text):
            errors.append("reviews/sources.md: missing source URLs")
        if not re.search(r"accessed \d{4}-\d{2}-\d{2}", source_text, re.IGNORECASE):
            errors.append("reviews/sources.md: missing access dates")

    for path in files:
        text = path.read_text(encoding="utf-8")
        for heading in REQUIRED_HEADINGS:
            if heading not in text:
                errors.append(f"{rel(path)}: missing required heading {heading}")
        for severity in REQUIRED_SEVERITIES:
            if not re.search(rf"\b{re.escape(severity)}\b", text):
                errors.append(f"{rel(path)}: missing severity name {severity}")
        lowered = text.lower()
        for phrase in FORBIDDEN_PHRASES:
            if phrase in lowered:
                errors.append(f"{rel(path)}: forbidden prompt phrase: {phrase}")
        if "do not invent" not in lowered:
            errors.append(f"{rel(path)}: must forbid invented facts")
        if "findings" not in lowered:
            errors.append(f"{rel(path)}: must request findings-first output")
        if "pass/fail" not in lowered:
            errors.append(f"{rel(path)}: must request final pass/fail recommendation")
        if "source notes" not in lowered:
            errors.append(f"{rel(path)}: missing Source Notes section")
        if "trusted source" not in lowered and "cite trusted sources" not in lowered:
            errors.append(f"{rel(path)}: missing trusted-source requirement")
        if "claims needing confirmation" not in lowered and "claim_confidence" not in lowered:
            errors.append(f"{rel(path)}: missing claim-confidence or confirmation handling")
        if path.name not in readme:
            errors.append(f"{rel(path)}: not linked from reviews/README.md")

        if path.name == "ats-and-market-fit-review.md" and "## Market Scan Freshness Gate" not in text:
            errors.append(f"{rel(path)}: missing market scan freshness gate")
        if path.name == "render-and-format-review.md" and "preview" not in lowered:
            errors.append(f"{rel(path)}: must require rendered preview inspection")
        if path.name == "confidentiality-and-public-safety-review.md":
            for phrase in ("internal urls", "customer", "secret"):
                if phrase not in lowered:
                    errors.append(f"{rel(path)}: missing public-safety concept {phrase}")

    if errors:
        print("Review prompt validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Review prompt validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
