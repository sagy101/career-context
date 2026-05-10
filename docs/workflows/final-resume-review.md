# Final Resume Review Workflow

Use this only for final or near-final resume candidates.

## Trigger

Run this workflow when the candidate says the resume is final, ready to send, ready to apply, or asks for final review. For normal edits, use `docs/workflows/update-resume.md`.

If the resume appears near-final but the candidate has not explicitly asked for final review, ask whether to run this gate.

## Steps

1. Confirm target role family, seniority, geography, and any specific job posting.
2. Check `guidance/market-scans/` for the newest relevant scan.
3. Refresh or create a market scan if required by `guidance/market-scans/README.md`.
4. Run review sub-agents using the default prompt set listed in `reviews/README.md`.
5. Add conditional prompts when the target requires them, and record skipped conditional reviews with a reason:
   - technical credibility for AI, agentic, ML infrastructure, platform, full-stack AI, and deeply technical roles
   - leadership and seniority for senior, staff, lead, principal, ownership-heavy, or award/mentorship-heavy resumes
   - readability when the resume is dense, heavily rewritten, or received readability/scannability findings in another review
6. Synthesize findings across sub-agents:
   - findings first
   - deduplicate overlapping comments
   - keep only actionable issues
   - preserve honest claims and source boundaries
7. Fix blocking and important issues.
8. Run `tools/check.sh`.
9. Inspect `resumes/current/preview.png`.
10. Summarize what changed and any remaining confirmation questions.

## Market Refresh

Create a new dated scan automatically when:

- no scan exists for the target role family
- the latest AI / agentic / ML infrastructure scan is older than 45 days
- the latest general full-stack / platform scan is older than 90 days
- the latest ATS/format fundamentals scan is older than 180 days
- target role family, seniority, geography, company, job description, or job posting changed

## Sub-Agent Dispatch

Default final review sub-agents:

- recruiter fit
- ATS and market fit
- internal jargon
- structure and scannability
- evidence and claim integrity
- confidentiality and public safety
- render and format

Conditional sub-agents:

- technical credibility
- leadership and seniority
- readability

Each sub-agent should receive `reviews/prompts/_shared.md`, the relevant review prompt from `reviews/prompts/`, the current resume Markdown, the latest relevant market scan, and any context files needed to verify claims.
