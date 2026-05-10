# Shared Resume Review Contract

## Required Inputs

The reviewer should receive:

- target role family, seniority, geography, and company or job posting when available
- `resumes/current/Jordan_Example_Resume.md`
- rendered PDF/DOCX/preview when relevant
- relevant `context/` files
- latest relevant market scan under `guidance/market-scans/`
- applicable formatting, ATS, and public-safety guidance under `guidance/`

## Severity Scale

- **Blocking:** likely to materially harm interview chances, create a false/unsafe claim, break ATS/rendering, or expose confidential information.
- **Important:** worth fixing before sending; improves clarity, credibility, positioning, or safety.
- **Minor:** useful polish, but not necessary before sending.
- **Nit:** tiny editorial preference; include sparingly.

## Output Format

Return findings first. Use this structure:

```text
Findings
- [Severity] Title
  Location: file/path.md:line when possible
  Evidence: brief quote or source/context reference
  Why it matters: recruiter/ATS/safety/readability impact
  Recommendation: concrete fix or question for the candidate

Open Questions
- Facts that need candidate confirmation before use.

Pass/Fail
- Pass, pass with minor fixes, or fail pending blocking fixes.
```

## Constraints

- Do not rewrite the whole resume.
- Do not invent facts, metrics, dates, adoption, awards, or shipped status.
- Distinguish achieved outcomes from targets, drafts, pilots, proposals, and claims needing confirmation.
- Prefer externally understandable wording over internal project names.
- Keep recommendations compatible with a one-page resume unless the user approved otherwise.
- Do not request hidden chain-of-thought. Provide concise rationale only.
- Cite trusted sources when making market, recruiter, ATS, or best-practice claims.

## Trusted Source Guidance

Use official job postings and company career pages for market language. Use reputable university career centers for resume structure and ATS guidance. Use official technology docs for skill names. Use OpenAI and Anthropic prompt-engineering guidance when reviewing prompt quality. Use NIST AI RMF/AIRC when reviewing AI safety, accountability, privacy, reliability, and trustworthiness framing.
