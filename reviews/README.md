# Final Resume Reviews

Use these prompts only for final or near-final resume candidates. Ordinary resume edits should stay lightweight: update the Markdown resume, regenerate artifacts, and run `tools/check.sh`.

Run the final review gate when the user says the resume is final, ready to send, ready to apply, or asks for a final review. If the agent believes the resume is close to final but the user has not said so, ask whether to run the final review gate.

## Review Flow

1. Confirm the target role family, seniority, geography, and any specific job posting.
2. Check `guidance/market-scans/` for a fresh market scan.
3. Refresh or create a market scan when the freshness rules in `guidance/market-scans/README.md` require it.
4. Dispatch focused sub-agents with the relevant prompts from `reviews/prompts/`.
5. Synthesize findings, remove duplicates, and fix only high-signal issues.
6. Regenerate artifacts with `tools/check.sh`.
7. Inspect `resumes/current/preview.png` before claiming the resume is ready.

## Default Final Review Set

- `recruiter-fit-review.md`
- `ats-and-market-fit-review.md`
- `internal-jargon-review.md`
- `structure-and-scannability-review.md`
- `evidence-and-claim-integrity-review.md`
- `confidentiality-and-public-safety-review.md`
- `render-and-format-review.md`

## Conditional Review Set

Use these when the target role or edit scope makes them relevant, and record why any applicable review was skipped:

- `technical-credibility-review.md`: required for AI, agentic, ML infrastructure, platform, full-stack AI, and deeply technical roles.
- `leadership-and-seniority-review.md`: required for senior, staff, lead, principal, manager-adjacent, or ownership-heavy targets, and whenever the resume claims mentoring, awards, cross-team influence, platform stewardship, or project leadership.
- `readability-review.md`: required when the resume is dense, heavily rewritten, or received readability/scannability findings in another review.

## Source Standard

Reviewer claims about market fit, ATS behavior, or best practices should cite trusted sources. Prefer official job postings, reputable university career guidance, official technology documentation, official prompt-engineering docs, and NIST AI RMF/AIRC guidance for AI safety and trustworthiness.

Do not let review agents invent missing facts. They should identify missing evidence and ask for confirmation or suggest safer wording.

Use `reviews/sources.md` as the prompt-source registry for reusable prompt design. Use the newest relevant file under `guidance/market-scans/` as the source of truth for target-role market expectations during an actual final review.
