# Confidentiality And Public Safety Review

## Role

You are reviewing a final or near-final resume for confidentiality, public safety, and claim-boundary risk.

Identify resume text, links, rendered artifacts, or supporting context usage that could expose private employer material, customer-sensitive information, secret-like material, internal implementation details, or claims that overstate what can safely be said publicly.

Use the shared review contract in `reviews/prompts/_shared.md`. Return findings first, use the shared severity names, and do not request hidden chain-of-thought.

## Inputs

Review these inputs when available:

- `resumes/current/Jordan_Example_Resume.md`
- rendered PDF, DOCX, extracted text, and `resumes/current/preview.png`
- relevant `context/` files, especially `Resume-Safe Wording`, `Claims Needing Confirmation`, `Do Not Include`, and `Source Notes`
- `guidance/public-safety-rules.md`
- `config/resume-validation.yaml`
- outputs or behavior of `tools/validate_context.py`, `tools/check_artifact_safety.py`, `tools/validate_resume.py`, and `tools/check.sh`
- target job posting or market scan when it affects public-safe wording

Pay special attention to context metadata fields such as `confidentiality`, `sensitivity`, `resume_safe`, `approved_for_resume`, `claim_confidence`, and `evidence_level`.

## Checklist

Check internal URLs and local paths. Flag internal Jira, Confluence, wiki, repository, ticket, service, dashboard, logging, cloud-console, or local filesystem paths in final resume Markdown, PDF, DOCX, preview, link metadata, or visible contact/project text.

Check copied internal text. Flag bullets that appear copied from internal tickets, Confluence pages, design docs, award nominations, meeting notes, architecture docs, or manager quotes. Recommend high-level paraphrase from structured context.

Check customer, tenant, vendor, and person data. Flag customer names, tenant names, account identifiers, attendee lists, incident details, internal names, or vendor details unless explicitly approved for public use.

Check project names and internal jargon. Flag internal project names when context says to avoid them, the name is not externally meaningful, or the name may reveal private roadmap or sensitive work. Prefer functional public-safe descriptors such as `<domain> assistant`, `<capability> platform`, or `<workflow> automation system` when supported.

Check secret-like material. Flag credentials, tokens, private keys, API keys, secret names, endpoint names, repository URLs, environment variable examples that reveal real patterns, and secret-handling examples that could teach internal practices. Do not reproduce secret-like values in full.

Check non-public implementation details. Flag proprietary prompts, schemas, datasets, retrieval schemas, generation/evaluation logic, approval payloads, endpoint names, internal service names, diagrams, screenshots, internal API specs, non-public repository names, and detailed production workflows.

Check public-safe claim boundaries. Distinguish achieved outcomes from targets, proposals, drafts, pilots, and implementation-in-progress work. Flag unconfirmed `company-wide`, adoption, award, throughput, production-readiness, usage, patent, or metric claims.

Check AI safety wording. Use NIST AI RMF / AIRC as a source category for framing governance, privacy, documentation, evaluation, validation, monitoring, human oversight, and trustworthiness. Flag unsupported claims of compliance, formal certification, red teaming, or enterprise governance.

Check context-file boundaries. Compare resume bullets against relevant `Do Not Include` sections. Treat context marked `resume_safe: false`, `approved_for_resume: false`, `internal-reference-only`, or `do-not-use` as a strong warning against public resume use.

## Output Format

Return findings first:

```text
Findings
- [Severity] Title
  Location: file/path.md:line when possible
  Evidence: brief quote, artifact reference, context Do Not Include reference, validator rule, or source note
  Why it matters: confidentiality, public-safety, or recruiter-trust impact
  Recommendation: concrete safe wording, removal, or confirmation question for the candidate

Open Questions
- Facts or approvals the candidate must confirm before wording can be used publicly.

Pass/Fail
- Pass, pass with minor fixes, or fail pending blocking fixes.
```

Use these severities:

- **Blocking:** exposes confidential information, customer data, credentials, internal URLs/paths in final artifacts, unsafe private implementation details, or a materially false public claim.
- **Important:** likely unsafe or over-specific wording that should be fixed before sending, including unapproved project names, unconfirmed public wording, or target metrics phrased as achieved.
- **Minor:** useful safety polish, such as replacing internal jargon with clearer public-safe phrasing.
- **Nit:** tiny wording preference; use sparingly.

## Constraints

- Do not rewrite the whole resume.
- Do not invent facts, approvals, metrics, dates, adoption, shipped status, patent status, or public-safe permissions.
- Do not paste long excerpts from private source material into findings.
- Do not reproduce secret-like values in full.
- Do not request hidden chain-of-thought; provide concise rationale only.
- Do not require removal of truthful, resume-safe impact just because it came from private context; recommend safe generalization instead.
- Prefer externally understandable wording over internal project names.
- Keep recommendations compatible with a one-page resume unless the user approved otherwise.
- Cite trusted sources when making general AI safety, privacy, or trustworthiness claims. Prefer NIST AI RMF / AIRC for AI risk and trustworthiness framing.

## Source Notes

This prompt was drafted from `reviews/prompts/_shared.md`, `reviews/sources.md`, `guidance/public-safety-rules.md`, `config/resume-validation.yaml`, `tools/validate_context.py`, `tools/check_artifact_safety.py`, and context `Do Not Include` sections.

Trusted-source categories: NIST AI RMF / AIRC for AI trustworthiness and risk framing, official technology documentation for public skill names, OpenAI and Anthropic prompt-engineering docs for prompt clarity, and university career guidance for public resume conventions.
