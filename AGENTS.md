# Agent Instructions

This repo is a long-lived career context and resume operations workspace. Optimize for future updates across years, not only for the current resume.

## Start Here

For any substantive resume update:

1. Read this file.
2. Read `README.md`.
3. Read the relevant workflow in `docs/workflows/`.
4. Use `context/index.md` and generated indexes to find context.
5. Edit `resumes/current/Jordan_Example_Resume.md` first.
6. Regenerate and validate artifacts with `tools/check.sh`.
7. Inspect `resumes/current/preview.png` before claiming completion.

## Source Of Truth

`resumes/current/Jordan_Example_Resume.md` is canonical. `tools/build_resume_docx.py` is only a renderer. Do not put resume prose directly in build scripts.

## Market And ATS Freshness

Refresh current market signals when target role, positioning, skills, or ATS terms matter. Prefer trusted, dated sources:

- official job postings from target companies
- reputable university career guidance
- official technology documentation

Record dated findings in `guidance/market-scans/`.

During final resume review, refresh or create a market scan automatically when no scan exists for the target role family, the latest AI / agentic / ML infrastructure scan is older than 45 days, the latest general full-stack / platform scan is older than 90 days, the latest ATS/format fundamentals scan is older than 180 days, target role family, seniority, geography, company, job description, or job posting changed, or the user provides a specific job posting.

## Context Hygiene

When adding or updating career context, capture structured facts instead of raw prompts or copied internal docs. For each role, project, or initiative, include stack, ownership, leadership/team scope, adoption, metrics, source coverage, claims needing confirmation, and explicit "do not include" boundaries.

Keep target metrics separate from achieved outcomes. If a source is a design draft, proposal, or phased plan, label unshipped capabilities as targets or candidates.

## Public Safety

Use structured context instead of copying internal docs. Do not commit proprietary code, copied Confluence text, credentials, customer data, endpoints, confidential diagrams, or unsafe internal implementation details.

## Final Resume Review Gate

Do not run the full final review gate for every small edit. Run it when the user says the resume is final, ready to send, ready to apply, or asks for final review. If the resume seems near-final but the user has not said so, ask whether to run final review.

For final review:

1. Confirm target role family, seniority, geography, and any specific job posting.
2. Refresh or create market guidance if the freshness rules require it.
3. Dispatch sub-agents using the review prompts in `reviews/prompts/`.
4. Use the default final review set from `reviews/README.md`; add optional reviews when relevant.
5. Synthesize findings, deduplicate, and fix blocking/important issues only.
6. Regenerate with `tools/check.sh`.
7. Inspect `resumes/current/preview.png`.

## Completion Rule

Never claim the resume is complete until `tools/check.sh` passes and the rendered preview has been inspected.
