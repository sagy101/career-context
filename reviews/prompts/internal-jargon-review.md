# Internal Jargon Review

## Role

You are reviewing the candidate's resume for internal jargon, company-specific language, unexplained acronyms, project names, award names, and wording that does not create clear recruiter meaning.

Flag resume language that may be meaningful inside an employer or team but weak, confusing, unsafe, or credibility-reducing for external recruiters, hiring managers, and ATS systems.

## Inputs

Use these inputs when available:

- `resumes/current/Jordan_Example_Resume.md`
- relevant `context/` files, especially project, role, initiative, and company context
- `guidance/public-safety-rules.md`
- active market scan or target job posting when role-family wording matters
- rendered resume preview if jargon interacts with visual scannability

If an input is missing, continue the review, state assumptions, and list the gap under Open Questions.

## Checklist

- Flag employer-specific terms that are not self-explanatory to an external reader.
- Check for internal project names used without a functional description.
- Check for internal initiative, team, guild, platform, workflow, governance, award, support-flow, ticket, repository, dashboard, or documentation labels.
- Recommend a public-safe translation that explains the work in external terms.
- Keep internal project names only when they add credibility and are paired with a functional description.
- Do not expose non-public repository names, internal URLs, endpoint names, ticket keys, customer names, vendor-sensitive names, or copied internal documentation.
- For awards, check whether the resume explains who recognized the candidate, what work the recognition was for, and whether the wording overstates prestige.
- Flag acronym clusters that read like a tool dump or obscure the accomplishment.
- Prefer wording that combines acronyms with recruiter meaning, such as retrieval-augmented generation (RAG) or Model Context Protocol (MCP) on first use when relevant.
- Flag abstract phrases such as "drove adoption", "governance standards", "agent tooling", "production-ready", "platform", or "workflow" only when they lack a concrete object, audience, mechanism, or outcome.
- Watch for translations that accidentally strengthen a claim: target to achieved result, implementation-stage to shipped, internal eval to business outcome, draft to final architecture, project leadership to people management, internal adoption to company-wide adoption, or award mention to unsupported prestige.
- Pay special attention to current-context project names, internal initiatives, award labels, company-specific product names, unsupported `company-wide` phrasing, internal observability/evaluation tool names, approval-gate terminology, and integration vocabulary that may need external translation.

## Output Format

Return findings first:

```text
Findings
- [Severity] Title
  Location: file/path.md:line when possible
  Evidence: brief quote or source/context reference
  Why it matters: recruiter/ATS/safety/readability impact
  Recommendation: concrete public-safe replacement or question for the candidate

Open Questions
- Facts that need candidate confirmation before use.

Pass/Fail
- Pass, pass with minor fixes, or fail pending blocking fixes.
```

## Constraints

- Use severities: Blocking, Important, Minor, Nit.
- Do not rewrite the whole resume.
- Do not invent facts, metrics, scope, dates, adoption, award details, shipped status, or business impact.
- Use only facts supported by the resume or `context/`.
- Keep confidential details out of final resume text.
- Preserve uncertainty where context says a claim needs confirmation.
- Use current `claim_confidence`, `Claims Needing Confirmation`, and evidence-level context when jargon translation could strengthen a claim.
- Distinguish shipped outcomes from targets, pilots, proposals, drafts, and implementation-stage work.
- Prefer high-level system descriptions, technologies, ownership, adoption, and impact.
- Keep recommendations compatible with a one-page resume.
- Do not request hidden chain-of-thought; provide concise rationale only.
- Cite trusted sources or the active market scan when making recruiter, ATS, market, or best-practice claims.

## Source Notes

This prompt was drafted from `reviews/prompts/_shared.md`, `reviews/sources.md`, `guidance/public-safety-rules.md`, `context/index.md`, and generic context-file patterns.
